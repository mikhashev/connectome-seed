"""Engine v2 of the GPU instrument (2026-09-26): many independent harness.bf_als problems in one
batch. A separate instrument, not reviewed; the registered CPU run does not use it.

Differences from gpu_bf.py (v1), which is kept unchanged for the earlier validation:
  * the (65, 65) grids are not repeated per (lambda, start): every batch row points at its
    problem's grid by an index;
  * a per-row lambda, so a final fit needs no grouping by the chosen lambda;
  * per-row active-set compaction in the Newton loop: only rows that have not met
    harness._newton_rows's break condition are computed in each iteration (v1 computed every row
    and froze the converged ones, so each iteration cost the whole batch);
  * the Hessian as one batched matmul of W with the (65, r*r) outer products of V (v1 used a
    three-operand einsum);
  * the CPU-side inputs (N1 fits, grids, held-out masks) are computed once per view and shared
    by all four ranks (prep.prepare_view), instead of once per rank.
Per-row semantics are those of harness._newton_rows / harness.bf_als, unchanged: up to
BF_NEWTON_ITERS iterations, break when the max row-gradient norm < BF_TOL (checked before the
step), BF_SWEEPS alternating sweeps, the SVD start and the PCG64(PERTURB_SEED_BASE + j) perturbed
starts built in numpy by the same expressions as bf_als, and the best start by the penalised
training objective with ties to the lower j. All GPU arithmetic is float64.

Never reads, fits or scores the real block.
"""
import numpy as np
import torch

from gpu_bf import DEVICE, DTYPE, H  # noqa: F401  (H: harness, read-only)

_DRAWS = {}


def _perturb_draws(r, j):
    if (r, j) not in _DRAWS:
        g = np.random.Generator(np.random.PCG64(H.PERTURB_SEED_BASE + j))
        zu = g.standard_normal((65, r))
        zv = g.standard_normal((65, r))
        _DRAWS[(r, j)] = (zu, zv)
    return _DRAWS[(r, j)]


def start_factors(O, Y, M, r, starts):
    """harness.bf_als's starts for one grid, built in numpy by the same expressions."""
    E = np.where(M > 0, Y - H._sig(O), 0.0)
    u, sv, vt = np.linalg.svd(E)
    U0 = u[:, :r] * np.sqrt(sv[:r])
    V0 = vt[:r].T * np.sqrt(sv[:r])
    eps = max(0.5 * float(np.sqrt(np.mean(np.concatenate([U0.ravel(), V0.ravel()]) ** 2))), 0.05)
    Us = np.empty((starts, 65, r))
    Vs = np.empty((starts, 65, r))
    Us[0], Vs[0] = U0, V0
    for j in range(1, starts):
        zu, zv = _perturb_draws(r, j)
        Us[j] = U0 + eps * zu
        Vs[j] = V0 + eps * zv
    return Us, Vs


def newton_rows_compact(Og, Yg, Mg, item, V, U, lam, iters, tol):
    """harness._newton_rows for every batch row b on grid item[b] (Og/Yg/Mg: (n_grids, 65, 65),
    already in this half-sweep's orientation). A row leaves the active set at the CPU's break;
    only active rows are computed."""
    r = U.shape[-1]
    U = U.clone()
    idx = torch.arange(U.shape[0], device=U.device)
    eye = torch.eye(r, dtype=U.dtype, device=U.device)
    for _ in range(iters):
        if idx.numel() == 0:
            break
        it = item[idx]
        Ua, Va, la = U[idx], V[idx], lam[idx].view(-1, 1, 1)
        Ma = Mg[it]
        P = torch.sigmoid(Og[it] + Ua @ Va.transpose(-1, -2))
        G = ((P - Yg[it]) * Ma) @ Va + la * Ua
        gn = torch.sqrt((G ** 2).sum(-1)).amax(-1)
        go = ~(gn < tol)                        # the CPU breaks only when max < tol (NaN goes on)
        n_go = int(go.sum())
        if n_go == 0:
            break
        if n_go < idx.numel():
            idx, P, G, Ma, Ua, Va, la = idx[go], P[go], G[go], Ma[go], Ua[go], Va[go], la[go]
        n = idx.numel()
        Wt = Ma * P * (1 - P)
        VV = (Va.unsqueeze(-1) * Va.unsqueeze(-2)).reshape(n, 65, r * r)
        Hm = (Wt @ VV).reshape(n, 65, r, r) + la.unsqueeze(-1) * eye
        step = torch.linalg.solve(Hm, G.unsqueeze(-1)).squeeze(-1)
        U[idx] = Ua - step
    return U


def _objective_rows(Og, Yg, Mg, item, U, V, lam, chunk=8192):
    """harness._bf_objective per batch row."""
    out = []
    for a in range(0, U.shape[0], chunk):
        sl = slice(a, a + chunk)
        it = item[sl]
        P = torch.clamp(torch.sigmoid(Og[it] + U[sl] @ V[sl].transpose(-1, -2)), 1e-300,
                        1 - 1e-16)
        Y, M = Yg[it], Mg[it]
        ll = -torch.sum(M * (Y * torch.log(P) + (1 - Y) * torch.log(1 - P)), dim=(1, 2))
        reg = 0.5 * lam[sl] * (torch.sum(U[sl] ** 2, dim=(1, 2)) + torch.sum(V[sl] ** 2,
                                                                                dim=(1, 2)))
        out.append(ll + reg)
    return torch.cat(out)


def bf_als_problems(O, Y, M, r, lam, starts, row_chunk=40000):
    """Solve many independent harness.bf_als(O[i], Y[i], M[i], r, lam[i], starts) problems.
    O, Y, M: (n, 65, 65) numpy; lam: (n,) numpy. Returns U, V as (n, 65, r) numpy: per problem,
    the start with the lowest penalised training objective (ties to the lower start index).
    Problems go to the GPU in blocks of at most row_chunk // starts problems (memory bound)."""
    n = O.shape[0]
    per = max(1, row_chunk // starts)
    U_out = np.empty((n, 65, r))
    V_out = np.empty((n, 65, r))
    for a in range(0, n, per):
        b = min(n, a + per)
        k = b - a
        Us = np.empty((k, starts, 65, r))
        Vs = np.empty((k, starts, 65, r))
        for i in range(k):
            Us[i], Vs[i] = start_factors(O[a + i], Y[a + i], M[a + i], r, starts)
        Og = torch.tensor(O[a:b], dtype=DTYPE, device=DEVICE)
        Yg = torch.tensor(Y[a:b], dtype=DTYPE, device=DEVICE)
        Mg = torch.tensor(M[a:b], dtype=DTYPE, device=DEVICE)
        OgT = Og.transpose(-1, -2).contiguous()
        YgT = Yg.transpose(-1, -2).contiguous()
        MgT = Mg.transpose(-1, -2).contiguous()
        item = torch.arange(k, device=DEVICE).repeat_interleave(starts)
        lam_t = torch.tensor(np.repeat(np.asarray(lam[a:b], np.float64), starts), dtype=DTYPE,
                             device=DEVICE)
        Ut = torch.tensor(Us.reshape(k * starts, 65, r), dtype=DTYPE, device=DEVICE)
        Vt = torch.tensor(Vs.reshape(k * starts, 65, r), dtype=DTYPE, device=DEVICE)
        for _ in range(H.BF_SWEEPS):
            Ut = newton_rows_compact(Og, Yg, Mg, item, Vt, Ut, lam_t, H.BF_NEWTON_ITERS,
                                     H.BF_TOL)
            Vt = newton_rows_compact(OgT, YgT, MgT, item, Ut, Vt, lam_t, H.BF_NEWTON_ITERS,
                                     H.BF_TOL)
        obj = _objective_rows(Og, Yg, Mg, item, Ut, Vt, lam_t).cpu().numpy().reshape(k, starts)
        jb = np.argmin(obj, axis=1)                      # first minimum = lower j on ties
        Un = Ut.cpu().numpy().reshape(k, starts, 65, r)
        Vn = Vt.cpu().numpy().reshape(k, starts, 65, r)
        U_out[a:b] = Un[np.arange(k), jb]
        V_out[a:b] = Vn[np.arange(k), jb]
        del Og, Yg, Mg, OgT, YgT, MgT, Ut, Vt
    return U_out, V_out


def choose_lambda(ll_by_lam, lambdas=None, tie=1e-9):
    """fit_bf's rule (harness.py:727-728): the largest lambda within 1e-9 of the best."""
    lambdas = list(H.BF_LAMBDAS) if lambdas is None else lambdas
    best = max(ll_by_lam.values())
    return max(l for l in lambdas if ll_by_lam[l] >= best - tie)


def inner_ll(Oi, Y, test, U, V, extra=None):
    """One inner fold's held-out log-likelihood, as fit_bf computes it."""
    z = Oi + U @ V.T if extra is None else Oi + U @ V.T + extra
    p = np.clip(H._sig(z), *H.CLIP)
    return float(np.sum(np.where(Y > 0, np.log(p), np.log(1 - p))[test]))


def gpu_fit_bf_prepared(preps, r, starts=None, row_chunk=40000):
    """harness.fit_bf(view, r) for every prepared view (prep.prepare_view output), as two
    batched stages: all (view x fold x lambda) inner fits, then every view's final fit at its
    chosen lambda. Returns (list of n1-dicts as fit_bf returns them, list of inner-ll dicts)."""
    starts = H.STARTS if starts is None else starts
    lambdas = list(H.BF_LAMBDAS)
    O, Y, M, lam, owner = [], [], [], [], []
    for vi, pp in enumerate(preps):
        for fi in range(len(pp["folds"])):
            for l in lambdas:
                O.append(pp["Oi"][fi])
                Y.append(pp["Y"])
                M.append(pp["Mi"][fi])
                lam.append(float(l))
                owner.append((vi, fi, l))
    U, V = bf_als_problems(np.stack(O), np.stack(Y), np.stack(M), r, np.array(lam), starts,
                           row_chunk)
    ll = [{l: 0.0 for l in lambdas} for _ in preps]
    for q, (vi, fi, l) in enumerate(owner):        # folds outer, lambdas inner, as fit_bf
        pp = preps[vi]
        ll[vi][l] += inner_ll(pp["Oi"][fi], pp["Y"], pp["test"][fi], U[q], V[q])
    lam_ch = [choose_lambda(d) for d in ll]
    U, V = bf_als_problems(np.stack([pp["O"] for pp in preps]),
                           np.stack([pp["Y"] for pp in preps]),
                           np.stack([pp["M"] for pp in preps]), r, np.array(lam_ch, float),
                           starts, row_chunk)
    out = []
    for vi, pp in enumerate(preps):
        n1 = {k: np.array(v, copy=True) for k, v in pp["n1"].items()}
        n1.update({"bf_U": U[vi], "bf_V": V[vi], "bf_lambda": np.array([float(lam_ch[vi])])})
        out.append(n1)
    return out, ll
