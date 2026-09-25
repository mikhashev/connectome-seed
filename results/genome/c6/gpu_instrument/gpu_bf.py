"""Batched GPU reproduction of harness.bf_als / harness.fit_bf (results/genome/c6/harness.py).

THIS IS A SEPARATE INSTRUMENT, NOT A REWRITE OF THE REGISTERED CPU ONE. It imports the CPU
harness and knockout_regrow modules read-only, for data/world construction and for the N1 fit
(cheap, unbatched, kept exactly as the CPU instrument computes it), and re-implements only the
expensive inner loop -- bf_als's ALS/Newton optimisation over (fold x lambda x start) -- as one
batched PyTorch computation on the GPU. It NEVER reads, fits or scores the real block (harness.REAL
restricted to BLOCK cells); the only real-bank read is harness.fit_n1 on the real KNOCKOUT view,
which is the synthetic worlds' own "degree_terms" step defined by the registration (section 3.6)
and used only to build synthetic worlds, exactly as knockout_regrow.py --synthetic-only does.

It must not be run as knockout_regrow.py's real or synthetic-only arm, and it does not import
anything that runs those arms (both live under `if __name__ == "__main__":` in that file).
"""
import sys
import time
import json
import pathlib

import numpy as np
import torch

HERE = pathlib.Path(__file__).resolve().parent
C6 = HERE.parent  # results/genome/c6
sys.path.insert(0, str(C6))
sys.path.insert(0, str(C6 / "checks"))

import harness as H          # noqa: E402  (read-only import; not modified, not copy-edited)
import knockout_regrow as K  # noqa: E402  (read-only import; module-level code only defines data)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DTYPE = torch.float64


def _sig_t(z):
    return torch.sigmoid(z)


def _bcast3(x):
    """(65,65) -> (1,65,65); (B,65,65) unchanged. Lets the batched ops below broadcast a single
    shared grid across a batch (one fold/one world) OR carry a DIFFERENT grid per batch item
    (many worlds/folds at once), from the same code path."""
    return x if x.dim() == 3 else x.unsqueeze(0)


def batched_newton_rows(O, Y, M, V, U, lam, iters, tol):
    """Batched version of harness._newton_rows, WITH the CPU's per-fit early-stop reproduced
    per batch item (this matters: rows with few training cells, e.g. T5a/T5c, give a
    near-singular per-row Hessian, and iterating past convergence on those amplifies
    floating-point noise into a random walk away from the optimum. Running the batch's full
    `iters` unconditionally, as a first version of this function did, reproduced the CPU's
    selected lambda but diverged in AUC/p by up to 0.4 on some worlds -- traced to exactly this.
    A batch item that has converged (max row-gradient norm < tol) is frozen for the rest of the
    call, exactly reproducing harness._newton_rows's `if ...: break`.)."""
    r = U.shape[-1]
    B = U.shape[0]
    Ob, Yb, Mb = _bcast3(O), _bcast3(Y), _bcast3(M)      # (1,65,65) or (B,65,65)
    eye = torch.eye(r, dtype=U.dtype, device=U.device).expand(B, r, r)
    lam_ = lam.view(B, 1, 1) if torch.is_tensor(lam) else lam
    active = torch.ones(B, dtype=torch.bool, device=U.device)
    for _ in range(iters):
        if not active.any():
            break
        P = _sig_t(Ob + U @ V.transpose(-1, -2))          # (B,65,65)
        G = torch.einsum("bst,btk->bsk", (P - Yb) * Mb, V) + lam_ * U
        gnorm = torch.sqrt((G ** 2).sum(-1)).amax(dim=-1)              # (B,) max over rows
        newly_converged = gnorm < tol
        W = Mb * P * (1 - P)                               # (B,65,65)
        H_ = torch.einsum("bst,btk,btl->bskl", W, V, V) + lam_.unsqueeze(-1) * eye.unsqueeze(1)
        step = torch.linalg.solve(H_, G.unsqueeze(-1)).squeeze(-1)
        upd = active & ~newly_converged
        U = torch.where(upd.view(B, 1, 1), U - step, U)
        active = active & ~newly_converged
    return U


def batched_objective(O, Y, M, U, V, lam):
    Ob, Yb, Mb = _bcast3(O), _bcast3(Y), _bcast3(M)
    P = torch.clamp(_sig_t(Ob + U @ V.transpose(-1, -2)), 1e-300, 1 - 1e-16)
    ll = -torch.sum((Mb * (Yb * torch.log(P) + (1 - Yb) * torch.log(1 - P))), dim=(1, 2))
    reg = 0.5 * lam * (torch.sum(U ** 2, dim=(1, 2)) + torch.sum(V ** 2, dim=(1, 2)))
    return ll + reg


def batched_bf_als(O_np, Y_np, M_np, r, lambdas, starts):
    """Batched harness.bf_als over ALL (lambda, start) pairs at once, for ONE (O, Y, M) grid.
    Returns dict lam -> (U, V) numpy arrays, the winner (by penalised training objective, ties
    to the lower start index j, exactly as harness.bf_als) for each lambda."""
    E = np.where(M_np > 0, Y_np - 1.0 / (1.0 + np.exp(-O_np)), 0.0)
    u, sv, vt = np.linalg.svd(E)
    U0 = u[:, :r] * np.sqrt(sv[:r])
    V0 = vt[:r].T * np.sqrt(sv[:r])
    eps = max(0.5 * float(np.sqrt(np.mean(np.concatenate([U0.ravel(), V0.ravel()]) ** 2))), 0.05)

    n_lam = len(lambdas)
    Us = np.zeros((n_lam, starts, 65, r))
    Vs = np.zeros((n_lam, starts, 65, r))
    for j in range(starts):
        if j == 0:
            Uj, Vj = U0, V0
        else:
            g = np.random.Generator(np.random.PCG64(H.PERTURB_SEED_BASE + j))
            Uj = U0 + eps * g.standard_normal((65, r))
            Vj = V0 + eps * g.standard_normal((65, r))
        for li in range(n_lam):
            Us[li, j] = Uj
            Vs[li, j] = Vj

    B = n_lam * starts
    Ut = torch.tensor(Us.reshape(B, 65, r), dtype=DTYPE, device=DEVICE)
    Vt = torch.tensor(Vs.reshape(B, 65, r), dtype=DTYPE, device=DEVICE)
    Ot = torch.tensor(O_np, dtype=DTYPE, device=DEVICE)
    Yt = torch.tensor(Y_np, dtype=DTYPE, device=DEVICE)
    Mt = torch.tensor(M_np, dtype=DTYPE, device=DEVICE)
    lam_t = torch.tensor(np.repeat(np.array(lambdas, dtype=np.float64), starts), dtype=DTYPE, device=DEVICE)

    for _ in range(H.BF_SWEEPS):
        Ut = batched_newton_rows(Ot, Yt, Mt, Vt, Ut, lam_t, H.BF_NEWTON_ITERS, H.BF_TOL)
        Vt = batched_newton_rows(Ot.T, Yt.T, Mt.T, Ut, Vt, lam_t, H.BF_NEWTON_ITERS, H.BF_TOL)

    obj = batched_objective(Ot, Yt, Mt, Ut, Vt, lam_t).cpu().numpy().reshape(n_lam, starts)
    Ut_np = Ut.detach().cpu().numpy().reshape(n_lam, starts, 65, r)
    Vt_np = Vt.detach().cpu().numpy().reshape(n_lam, starts, 65, r)

    out = {}
    for li, lam in enumerate(lambdas):
        j_best = int(np.argmin(obj[li]))  # ties -> lower j (argmin returns first)
        out[lam] = (Ut_np[li, j_best], Vt_np[li, j_best])
    return out


def batched_bf_als_multi(O_np, Y_np, M_np, r, lambdas, starts):
    """The cross-FIT batched version: O_np, Y_np, M_np are (n_items, 65, 65) -- e.g. n_items =
    n_worlds * n_folds, or n_worlds for a final fit. One GPU call optimises ALL
    (item x lambda x start) combinations as a single batch (batch size n_items*len(lambdas)*
    starts). This is the actual point of the instrument (per registration section 7: bf_als's
    cost is numpy dispatch overhead on many small matrices; batching across fits, not just
    within one fit_bf call, is what removes that overhead). Returns dict lam ->
    (U, V) numpy arrays of shape (n_items, 65, r), the per-item, per-lambda winner across
    starts (ties -> lower start index, exactly as harness.bf_als)."""
    n_items = O_np.shape[0]
    n_lam = len(lambdas)
    Us = np.zeros((n_items, n_lam, starts, 65, r))
    Vs = np.zeros((n_items, n_lam, starts, 65, r))
    for i in range(n_items):
        E = np.where(M_np[i] > 0, Y_np[i] - 1.0 / (1.0 + np.exp(-O_np[i])), 0.0)
        u, sv, vt = np.linalg.svd(E)
        U0 = u[:, :r] * np.sqrt(sv[:r])
        V0 = vt[:r].T * np.sqrt(sv[:r])
        eps = max(0.5 * float(np.sqrt(np.mean(np.concatenate([U0.ravel(), V0.ravel()]) ** 2))),
                   0.05)
        for j in range(starts):
            if j == 0:
                Uj, Vj = U0, V0
            else:
                g = np.random.Generator(np.random.PCG64(H.PERTURB_SEED_BASE + j))
                Uj = U0 + eps * g.standard_normal((65, r))
                Vj = V0 + eps * g.standard_normal((65, r))
            for li in range(n_lam):
                Us[i, li, j] = Uj
                Vs[i, li, j] = Vj

    B = n_items * n_lam * starts
    Ut = torch.tensor(Us.reshape(B, 65, r), dtype=DTYPE, device=DEVICE)
    Vt = torch.tensor(Vs.reshape(B, 65, r), dtype=DTYPE, device=DEVICE)
    # O/Y/M repeated across (lambda, start) for each item, matching the batch's flat order
    Ob = np.repeat(O_np, n_lam * starts, axis=0)
    Yb = np.repeat(Y_np, n_lam * starts, axis=0)
    Mb = np.repeat(M_np, n_lam * starts, axis=0)
    Ot = torch.tensor(Ob, dtype=DTYPE, device=DEVICE)
    Yt = torch.tensor(Yb, dtype=DTYPE, device=DEVICE)
    Mt = torch.tensor(Mb, dtype=DTYPE, device=DEVICE)
    lam_t = torch.tensor(np.tile(np.repeat(np.array(lambdas, dtype=np.float64), starts), n_items),
                          dtype=DTYPE, device=DEVICE)

    for _ in range(H.BF_SWEEPS):
        Ut = batched_newton_rows(Ot, Yt, Mt, Vt, Ut, lam_t, H.BF_NEWTON_ITERS, H.BF_TOL)
        Vt = batched_newton_rows(Ot.transpose(-1, -2), Yt.transpose(-1, -2), Mt.transpose(-1, -2),
                                  Ut, Vt, lam_t, H.BF_NEWTON_ITERS, H.BF_TOL)

    obj = batched_objective(Ot, Yt, Mt, Ut, Vt, lam_t).cpu().numpy().reshape(n_items, n_lam, starts)
    Ut_np = Ut.detach().cpu().numpy().reshape(n_items, n_lam, starts, 65, r)
    Vt_np = Vt.detach().cpu().numpy().reshape(n_items, n_lam, starts, 65, r)

    out = {}
    for li, lam in enumerate(lambdas):
        j_best = np.argmin(obj[:, li, :], axis=-1)                # (n_items,)
        Ubest = Ut_np[np.arange(n_items), li, j_best]              # (n_items,65,r)
        Vbest = Vt_np[np.arange(n_items), li, j_best]
        out[lam] = (Ubest, Vbest)
    return out


def gpu_fit_bf(view, r, starts=None):
    """Batched reproduction of harness.fit_bf(view, r)."""
    starts = H.STARTS if starts is None else starts
    n1 = H.fit_n1(view)                       # unbatched, exact CPU call
    M, Y = H._grid(view)
    folds = sorted(set(H.inner_folds(view).tolist()))
    lambdas = H.BF_LAMBDAS

    # --- one batched GPU call per fold, over all lambdas x starts at once ---
    ll = {lam: 0.0 for lam in lambdas}
    for f in folds:
        keep = H.inner_folds(view) != f
        sv_ = H.subview(view, keep)
        Oi = H._n1_logit_grid(H.fit_n1(sv_))
        Mi, _ = H._grid(sv_)
        test = np.zeros((65, 65), bool)
        hc = view.cells[~keep]
        test[hc[:, 0], hc[:, 1]] = True

        fits = batched_bf_als(Oi, Y, Mi, r, lambdas, starts)
        for lam in lambdas:
            U, V = fits[lam]
            p = np.clip(1.0 / (1.0 + np.exp(-(Oi + U @ V.T))), *H.CLIP)
            ll[lam] += float(np.sum(np.where(Y > 0, np.log(p), np.log(1 - p))[test]))

    best = max(ll.values())
    lam = max(l for l in lambdas if ll[l] >= best - 1e-9)

    final = batched_bf_als(H._n1_logit_grid(n1), Y, M, r, [lam], starts)
    U, V = final[lam]
    n1.update({"bf_U": U, "bf_V": V, "bf_lambda": np.array([float(lam)])})
    return n1


def gpu_fit_bf_many(views, r, starts=None):
    """Cross-fit batched harness.fit_bf: fits BF_r on MANY views (e.g. one per world, or one per
    (world, shuffle)) as one instrument run. Fold-selection is one batched GPU call across ALL
    (view x fold x lambda x start); the final fit is one batched GPU call across ALL
    (view x start). Returns a list of n1-dicts (one per view, same shape as harness.fit_bf's
    return), in the same order as `views`."""
    starts = H.STARTS if starts is None else starts
    lambdas = H.BF_LAMBDAS
    n_views = len(views)

    n1s = [H.fit_n1(v) for v in views]                 # cheap, unbatched, exact CPU calls
    Ms, Ys = zip(*(H._grid(v) for v in views))
    Ms, Ys = np.stack(Ms), np.stack(Ys)

    folds_per_view = [sorted(set(H.inner_folds(v).tolist())) for v in views]
    n_folds = len(folds_per_view[0])
    assert all(len(f) == n_folds for f in folds_per_view), "views must share the fold structure"

    # --- build one big (n_views * n_folds, 65, 65) batch for fold-selection ---
    Oi_all, Mi_all, test_all = [], [], []
    for vi, v in enumerate(views):
        for f in folds_per_view[vi]:
            keep = H.inner_folds(v) != f
            sv_ = H.subview(v, keep)
            Oi_all.append(H._n1_logit_grid(H.fit_n1(sv_)))
            Mi, _ = H._grid(sv_)
            Mi_all.append(Mi)
            test = np.zeros((65, 65), bool)
            hc = v.cells[~keep]
            test[hc[:, 0], hc[:, 1]] = True
            test_all.append(test)
    Oi_all = np.stack(Oi_all)                            # (n_views*n_folds, 65, 65)
    Mi_all = np.stack(Mi_all)
    test_all = np.stack(test_all)
    Y_rep = np.repeat(Ys, n_folds, axis=0)                # each view's Y, once per its fold

    fits = batched_bf_als_multi(Oi_all, Y_rep, Mi_all, r, lambdas, starts)
    ll = {lam: np.zeros(n_views) for lam in lambdas}
    for lam in lambdas:
        U, V = fits[lam]                                  # (n_views*n_folds, 65, r) each
        logit = Oi_all + np.einsum("nsk,ntk->nst", U, V)
        p = np.clip(1.0 / (1.0 + np.exp(-logit)), *H.CLIP)
        term = np.where(Y_rep > 0, np.log(p), np.log(1 - p))
        term = np.where(test_all, term, 0.0)
        contrib = term.reshape(n_views, n_folds, 65, 65).sum(axis=(1, 2, 3))
        ll[lam] += contrib

    lams_chosen = []
    for vi in range(n_views):
        best = max(ll[lam][vi] for lam in lambdas)
        lams_chosen.append(max(l for l in lambdas if ll[l][vi] >= best - 1e-9))

    # --- final fit: one batched call per distinct lambda value across the views that chose it ---
    out_U = [None] * n_views
    out_V = [None] * n_views
    Os_full = np.stack([H._n1_logit_grid(n1) for n1 in n1s])
    by_lam = {}
    for vi, lam in enumerate(lams_chosen):
        by_lam.setdefault(lam, []).append(vi)
    for lam, idxs in by_lam.items():
        sub_O = Os_full[idxs]
        sub_Y = Ys[idxs]
        sub_M = Ms[idxs]
        fits = batched_bf_als_multi(sub_O, sub_Y, sub_M, r, [lam], starts)
        U, V = fits[lam]
        for k, vi in enumerate(idxs):
            out_U[vi] = U[k]
            out_V[vi] = V[k]

    for vi, n1 in enumerate(n1s):
        n1.update({"bf_U": out_U[vi], "bf_V": out_V[vi],
                   "bf_lambda": np.array([float(lams_chosen[vi])])})
    return n1s


def p_exist_on_block(n1data):
    """Row-major order (boolean-mask order over K.BLOCK). For comparison against
    raw_fits.json.gz use p_exist_on_block_cells, which matches K.BLOCK_CELLS order."""
    logit = H._n1_logit_grid(n1data) + n1data["bf_U"] @ n1data["bf_V"].T
    p = 1.0 / (1.0 + np.exp(-logit))
    return p[K.BLOCK]


def p_exist_on_block_cells(n1data):
    """K.BLOCK_CELLS order (NOT row-major) -- matches raw_fits.json.gz's 'p'/'y' order."""
    logit = H._n1_logit_grid(n1data) + n1data["bf_U"] @ n1data["bf_V"].T
    p = 1.0 / (1.0 + np.exp(-logit))
    return p[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]]
