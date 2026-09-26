"""Engine v3 of the GPU instrument (2026-09-26): the streamed pipeline. A separate instrument,
not reviewed; the registered CPU run does not use it.

Built on engine v2 (gpu_bf2), with the host work taken off the GPU's critical path:
  * every grid of every prepared bank (the whole view and its inner-fold training views) is
    uploaded to the GPU once (GridStore); a problem refers to its grid by index, so the grids
    are never repeated per (lambda, start) and never re-uploaded per rank;
  * the SVD start of harness.bf_als is taken from the preparation (prep.prepare_key_compact,
    one SVD per grid instead of one per (grid, lambda, rank)); the perturbed starts are
    U0 + eps * z with eps computed in numpy by bf_als's expression and the PCG64 draws of
    gpu_bf2, multiplied and added on the GPU as two separate (correctly rounded) float64 ops,
    as numpy does them;
  * M, Y and the held-out masks are bool on the GPU; the Newton step uses torch.where on them,
    which gives the same float64 values as the 0/1 products of harness._newton_rows;
  * the inner held-out log-likelihood of every (bank, fold, lambda) problem is computed on the
    GPU (float64; sums over the ten folds are then taken in fold order on the host), so ranks
    run back to back with no per-problem host loop. The lambda rule (ties within 1e-9 to the
    larger lambda) is applied on the host; near-ties are counted for audit.
Per-row Newton semantics are those of gpu_bf2 (harness._newton_rows's break, BF_SWEEPS sweeps,
best start by the penalised objective with ties to the lower j).

Never reads, fits or scores the real block.
"""
import numpy as np
import torch

from gpu_bf2 import DEVICE, DTYPE, H, _perturb_draws


class GridStore:
    """All grids of all prepared banks, resident on the GPU. Grid (b, 0) is bank b's whole
    view; grids (b, 1..n_folds) are its inner-fold training views, in fit_bf's fold order."""

    def __init__(self, preps):
        self.n_banks = len(preps)
        self.per = preps[0]["O"].shape[0]
        assert all(pp["O"].shape[0] == self.per for pp in preps)
        O = np.concatenate([pp["O"] for pp in preps])
        M = np.concatenate([pp["M"] for pp in preps])
        Y = np.concatenate([np.broadcast_to(pp["Y"], (self.per, 65, 65)) for pp in preps])
        T = np.concatenate([pp["test"] for pp in preps])
        self.A4 = np.concatenate([pp["A4"] for pp in preps])
        self.B4 = np.concatenate([pp["B4"] for pp in preps])
        self.O = torch.tensor(O, dtype=DTYPE, device=DEVICE)
        self.OT = self.O.transpose(-1, -2).contiguous()
        self.M = torch.tensor(M, device=DEVICE)
        self.MT = self.M.transpose(-1, -2).contiguous()
        self.Y = torch.tensor(Y, device=DEVICE)
        self.YT = self.Y.transpose(-1, -2).contiguous()
        self.T = torch.tensor(T, device=DEVICE)
        self._eps = {}
        self._AB = {}

    def start_factors(self, r):
        """The rank-r SVD starts (first r columns of the rank-4 ones) on the GPU."""
        if r not in self._AB:
            self._AB[r] = (torch.tensor(np.ascontiguousarray(self.A4[:, :, :r]), dtype=DTYPE,
                                        device=DEVICE),
                           torch.tensor(np.ascontiguousarray(self.B4[:, :, :r]), dtype=DTYPE,
                                        device=DEVICE))
        return self._AB[r]

    def grid(self, b, k):
        return b * self.per + k

    def eps(self, r):
        """bf_als's eps for every grid at rank r, by its numpy expression."""
        if r not in self._eps:
            e = np.empty(len(self.A4))
            for i in range(len(self.A4)):
                U0, V0 = self.A4[i][:, :r], self.B4[i][:, :r]
                e[i] = max(0.5 * float(np.sqrt(np.mean(np.concatenate([U0.ravel(), V0.ravel()])
                                                       ** 2))), 0.05)
            self._eps[r] = e
        return self._eps[r]


def newton_rows_v3(Og, Yg, Mg, item, V, U, lam, iters, tol):
    """gpu_bf2.newton_rows_compact with bool Y, M grids."""
    r = U.shape[-1]
    U = U.clone()
    idx = torch.arange(U.shape[0], device=U.device)
    eye = torch.eye(r, dtype=U.dtype, device=U.device)
    zero = torch.zeros((), dtype=U.dtype, device=U.device)
    for _ in range(iters):
        if idx.numel() == 0:
            break
        it = item[idx]
        Ua, Va, la = U[idx], V[idx], lam[idx].view(-1, 1, 1)
        Ma = Mg[it]
        P = torch.sigmoid(Og[it] + Ua @ Va.transpose(-1, -2))
        G = torch.where(Ma, torch.where(Yg[it], P - 1, P), zero) @ Va + la * Ua
        gn = torch.sqrt((G ** 2).sum(-1)).amax(-1)
        go = ~(gn < tol)
        n_go = int(go.sum())
        if n_go == 0:
            break
        if n_go < idx.numel():
            idx, P, G, Ma, Ua, Va, la = idx[go], P[go], G[go], Ma[go], Ua[go], Va[go], la[go]
        n = idx.numel()
        Wt = torch.where(Ma, P * (1 - P), zero)
        VV = (Va.unsqueeze(-1) * Va.unsqueeze(-2)).reshape(n, 65, r * r)
        Hm = (Wt @ VV).reshape(n, 65, r, r) + la.unsqueeze(-1) * eye
        step = torch.linalg.solve(Hm, G.unsqueeze(-1)).squeeze(-1)
        U[idx] = Ua - step
    return U


def _objective_v3(S, gi, U, V, lam):
    P = torch.clamp(torch.sigmoid(S.O[gi] + U @ V.transpose(-1, -2)), 1e-300, 1 - 1e-16)
    term = torch.where(S.M[gi], torch.where(S.Y[gi], torch.log(P), torch.log(1 - P)),
                       torch.zeros((), dtype=P.dtype, device=P.device))
    ll = -torch.sum(term, dim=(1, 2))
    return ll + 0.5 * lam * (torch.sum(U ** 2, dim=(1, 2)) + torch.sum(V ** 2, dim=(1, 2)))


def _heldout_ll(S, gi, U, V):
    """fit_bf's inner-fold term: sum over held-out cells of log p (present) / log(1-p)."""
    p = torch.clamp(torch.sigmoid(S.O[gi] + U @ V.transpose(-1, -2)), *H.CLIP)
    term = torch.where(S.T[gi], torch.where(S.Y[gi], torch.log(p), torch.log(1 - p)),
                       torch.zeros((), dtype=p.dtype, device=p.device))
    return torch.sum(term, dim=(1, 2))


def solve_problems(S, grid_idx, lam, r, starts, row_chunk=40000, want="uv"):
    """bf_als on grid grid_idx[i] at lam[i], rank r, for every problem i. want='uv' returns the
    winning (U, V) per problem as numpy; want='ll' returns the winner's held-out log-lik."""
    n = len(grid_idx)
    per = max(1, row_chunk // starts)
    eps_all = S.eps(r)
    ZU = np.stack([np.zeros((65, r))] + [_perturb_draws(r, j)[0] for j in range(1, starts)])
    ZV = np.stack([np.zeros((65, r))] + [_perturb_draws(r, j)[1] for j in range(1, starts)])
    ZU_t = torch.tensor(ZU, dtype=DTYPE, device=DEVICE)
    ZV_t = torch.tensor(ZV, dtype=DTYPE, device=DEVICE)
    A_t, B_t = S.start_factors(r)
    out_U, out_V, out_ll = [], [], []
    for a in range(0, n, per):
        b = min(n, a + per)
        k = b - a
        g = torch.tensor(np.asarray(grid_idx[a:b], np.int64), device=DEVICE)
        e = torch.tensor(eps_all[np.asarray(grid_idx[a:b])], dtype=DTYPE, device=DEVICE)
        U0, V0 = A_t[g], B_t[g]                                    # (k, 65, r)
        # start j = 0: U0 itself; j >= 1: U0 + eps * z_j (mul, then add)
        Ut = torch.where(torch.arange(starts, device=DEVICE).view(1, starts, 1, 1) == 0,
                         U0.unsqueeze(1), U0.unsqueeze(1) + e.view(k, 1, 1, 1) * ZU_t.unsqueeze(0))
        Vt = torch.where(torch.arange(starts, device=DEVICE).view(1, starts, 1, 1) == 0,
                         V0.unsqueeze(1), V0.unsqueeze(1) + e.view(k, 1, 1, 1) * ZV_t.unsqueeze(0))
        Ut = Ut.reshape(k * starts, 65, r).contiguous()
        Vt = Vt.reshape(k * starts, 65, r).contiguous()
        item = g.repeat_interleave(starts)
        lam_t = torch.tensor(np.repeat(np.asarray(lam[a:b], np.float64), starts), dtype=DTYPE,
                             device=DEVICE)
        for _ in range(H.BF_SWEEPS):
            Ut = newton_rows_v3(S.O, S.Y, S.M, item, Vt, Ut, lam_t, H.BF_NEWTON_ITERS, H.BF_TOL)
            Vt = newton_rows_v3(S.OT, S.YT, S.MT, item, Ut, Vt, lam_t, H.BF_NEWTON_ITERS,
                                H.BF_TOL)
        obj = torch.cat([_objective_v3(S, item[c:c + 8192], Ut[c:c + 8192], Vt[c:c + 8192],
                                       lam_t[c:c + 8192]) for c in range(0, k * starts, 8192)])
        obj = obj.view(k, starts).cpu().numpy()
        jb = torch.tensor(np.argmin(obj, axis=1), device=DEVICE)     # first minimum: lower j
        rows = torch.arange(k, device=DEVICE) * starts + jb
        Ub, Vb = Ut[rows], Vt[rows]
        if want == "ll":
            out_ll.append(_heldout_ll(S, g, Ub, Vb).cpu().numpy())
        else:
            out_U.append(Ub.cpu().numpy())
            out_V.append(Vb.cpu().numpy())
        del Ut, Vt, U0, V0
    if want == "ll":
        return np.concatenate(out_ll)
    return np.concatenate(out_U), np.concatenate(out_V)


def fit_bf_all(S, n_folds, r, starts=None, row_chunk=40000, tie=1e-9, near=1e-7):
    """harness.fit_bf(view, r) for every bank in the store. Returns (lam_chosen (n_banks,),
    U (n_banks, 65, r), V, ll (n_banks, n_lambdas), near_tie_banks)."""
    starts = H.STARTS if starts is None else starts
    lambdas = np.array(H.BF_LAMBDAS, dtype=np.float64)
    nl, nb = len(lambdas), S.n_banks
    # problem order: bank, fold, lambda
    b_idx = np.repeat(np.arange(nb), n_folds * nl)
    f_idx = np.tile(np.repeat(np.arange(n_folds), nl), nb)
    l_idx = np.tile(np.arange(nl), nb * n_folds)
    grid_idx = b_idx * S.per + 1 + f_idx
    llp = solve_problems(S, grid_idx, lambdas[l_idx], r, starts, row_chunk, want="ll")
    llp = llp.reshape(nb, n_folds, nl)
    ll = np.zeros((nb, nl))
    for f in range(n_folds):                                       # fold order, as fit_bf
        ll += llp[:, f, :]
    best = ll.max(axis=1, keepdims=True)
    ok = ll >= best - tie
    lam_ch = np.array([lambdas[np.flatnonzero(o)].max() for o in ok])
    near_tie = int(np.sum(np.any((np.abs(ll - (best - tie)) < near) & (ll != best), axis=1)))
    U, V = solve_problems(S, np.arange(nb) * S.per, lam_ch, r, starts, row_chunk, want="uv")
    return lam_ch, U, V, ll, near_tie
