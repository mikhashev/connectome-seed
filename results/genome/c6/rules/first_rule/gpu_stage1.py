"""Stage 1 of the first rule on the GPU (torch, float64), for the CPU-vs-GPU timing only.

Why it is batched over chains and not over candidates. Stage 1 (proposal section 2.4) is a
sequential greedy search: toggle (i, j) is judged on the state left by every toggle before it,
and flip (t, l) on the state left by every flip before it. Evaluating all 144 toggles (or all 780
flips) against one state and accepting the improving ones together would be a different
algorithm (Jacobi instead of Gauss-Seidel) and would give a different genome. So this version
keeps the order exactly and batches over what is independent:
  - the 16 rho levels (and 16 leak levels) of one candidate, and
  - the chains: every restart of a fit, and optionally many fits, advanced in lockstep, each
    accepting or rejecting its own candidate with its own state (torch.where, no host sync).
Within one chain the sequence of decisions is the CPU one, step for step. The only difference is
floating-point rounding of exp/log/sums (CUDA vs numpy), which the 1e-9-bit acceptance tolerance
[R1] absorbs; the J trajectories are compared with the CPU's in benchmark().
"""

import time

import numpy as np
import torch

import fit as FR


def stage1_batch(Ms, Ys, E0s, fix_labels=False, device="cuda"):
    dt = torch.float64
    dev = torch.device(device)
    B = len(E0s)
    K = E0s[0].shape[1]
    M = torch.as_tensor(np.stack(Ms), device=dev)
    Y = torch.as_tensor(np.stack(Ys), device=dev)
    E = torch.as_tensor(np.stack(E0s).astype(np.float64), device=dev)
    LQ = torch.as_tensor(FR.LOG1M_RHO, dtype=dt, device=dev)
    EPS = torch.as_tensor(FR.EPS, dtype=dt, device=dev)
    P = torch.zeros((B, K, K), dtype=torch.bool, device=dev)
    Q = torch.zeros((B, K, K), dtype=torch.long, device=dev)
    eq = torch.as_tensor([FR.eps_level_nearest(m, y) for m, y in zip(Ms, Ys)], device=dev)
    nR = torch.zeros(B, dtype=torch.long, device=dev)
    active = torch.ones(B, dtype=torch.bool, device=dev)
    ar = torch.arange(B, device=dev)
    zero = torch.zeros((), dtype=dt, device=dev)

    def cost(S, eps, Yb):
        p = torch.clamp(1.0 - (1.0 - eps) * torch.exp(S), *FR.CLIP)
        return -torch.log2(torch.where(Yb, p, 1.0 - p))

    def Lmat():
        return torch.where(P, LQ[Q], zero)

    def full_state():
        S = E @ Lmat() @ E.transpose(1, 2)
        C = torch.where(M, cost(S, EPS[eq][:, None, None], Y), zero)
        return S, C

    S, C = full_state()
    trajs = [(C.sum((1, 2)) + FR.RULE_BITS * nR).cpu().numpy()]
    sweeps = np.zeros(B, np.int64)
    for _ in range(FR.MAX_SWEEPS):
        if not bool(active.any()):
            break
        sweeps += active.cpu().numpy()
        changed = torch.zeros(B, dtype=torch.bool, device=dev)
        eps = EPS[eq][:, None, None]
        eps4 = eps[:, None]
        # (a) toggles, in index order
        for i in range(K):
            for j in range(K):
                A = (E[:, :, i, None] * E[:, None, :, j]).bool() & M
                pres = P[:, i, j]
                cur = LQ[Q[:, i, j]]
                # removal
                Sr = torch.where(A, S - cur[:, None, None], S)
                Cr = torch.where(M, cost(Sr, eps, Y), zero)
                dr = (Cr - C).sum((1, 2)) - FR.RULE_BITS
                # addition at each of 16 levels
                Sa = torch.where(A[:, None], S[:, None] + LQ[None, :, None, None], S[:, None])
                Ca = torch.where(M[:, None], cost(Sa, eps4, Y[:, None]), zero)
                da = (Ca - C[:, None]).sum((2, 3)) + FR.RULE_BITS
                qa = torch.argmin(da, dim=1)
                dmin = da[ar, qa]
                acc_r = active & pres & (dr < -FR.TOL)
                acc_a = active & ~pres & (nR < FR.R_MAX) & (dmin < -FR.TOL)
                S = torch.where(acc_r[:, None, None], Sr,
                                torch.where(acc_a[:, None, None], Sa[ar, qa], S))
                C = torch.where(acc_r[:, None, None], Cr,
                                torch.where(acc_a[:, None, None], Ca[ar, qa], C))
                P[:, i, j] = torch.where(acc_r, False, torch.where(acc_a, True, pres))
                Q[:, i, j] = torch.where(acc_a, qa, Q[:, i, j])
                nR = nR - acc_r.long() + acc_a.long()
                changed |= acc_r | acc_a
        # (a, end) re-choose rho of present rules, in index order
        for i in range(K):
            for j in range(K):
                pres = P[:, i, j] & active
                A = (E[:, :, i, None] * E[:, None, :, j]).bool() & M
                cur = LQ[Q[:, i, j]]
                Sa = torch.where(A[:, None], (S - cur[:, None, None])[:, None]
                                 + LQ[None, :, None, None], S[:, None])
                Ca = torch.where(M[:, None], cost(Sa, eps4, Y[:, None]), zero)
                da = (Ca - C[:, None]).sum((2, 3))
                qa = torch.argmin(da, dim=1)
                acc = pres & (da[ar, qa] < da[ar, Q[:, i, j]] - FR.TOL)
                S = torch.where(acc[:, None, None], Sa[ar, qa], S)
                C = torch.where(acc[:, None, None], Ca[ar, qa], C)
                Q[:, i, j] = torch.where(acc, qa, Q[:, i, j])
                changed |= acc
        # (b) flips, types then labels in index order
        if not fix_labels:
            L = Lmat()
            used = P.any(1) | P.any(2)                       # (B, K)
            for t in range(65):
                for l in range(K):
                    En = E.clone()
                    En[:, t, l] = 1.0 - En[:, t, l]
                    et = En[:, t]                              # (B, K)
                    srow = torch.einsum("buj,bj->bu", En, torch.einsum("bk,bkj->bj", et, L))
                    scol = torch.einsum("buk,bk->bu", En, torch.einsum("bkj,bj->bk", L, et))
                    scol[:, t] = srow[:, t]
                    crow = torch.where(M[:, t], cost(srow, eps[:, :, 0], Y[:, t]), zero)
                    ccol = torch.where(M[:, :, t], cost(scol, eps[:, :, 0], Y[:, :, t]), zero)
                    d = ((crow - C[:, t]).sum(1) + (ccol - C[:, :, t]).sum(1)
                         - (ccol[:, t] - C[:, t, t]))
                    acc = active & used[:, l] & (d < -FR.TOL)
                    a3 = acc[:, None]
                    E = torch.where(acc[:, None, None], En, E)
                    S[:, t] = torch.where(a3, srow, S[:, t])
                    S[:, :, t] = torch.where(a3, scol, S[:, :, t])
                    C[:, t] = torch.where(a3, crow, C[:, t])
                    C[:, :, t] = torch.where(a3, ccol, C[:, :, t])
                    changed |= acc
        # (c) leak
        Cs = torch.where(M[:, None], cost(S[:, None], EPS[None, :, None, None], Y[:, None]), zero)
        d = Cs.sum((2, 3))
        qe = torch.argmin(d, dim=1)
        acc = active & (d[ar, qe] < d[ar, eq] - FR.TOL)
        eq = torch.where(acc, qe, eq)
        changed |= acc
        S, C = full_state()
        trajs.append((C.sum((1, 2)) + FR.RULE_BITS * nR).cpu().numpy())
        active &= changed
    torch.cuda.synchronize()
    En, Pn, Qn, en = (E.cpu().numpy() > 0.5), P.cpu().numpy(), Q.cpu().numpy(), eq.cpu().numpy()
    out = []
    for b in range(B):
        tr = [float(x[b]) for x in trajs[:sweeps[b] + 1]]
        out.append((En[b], Pn[b], Qn[b], int(en[b]), tr[-1], tr, int(sweeps[b])))
    return out


def gpu_stage1_fn(M, Y, E0s, fix_labels):
    return stage1_batch([M] * len(E0s), [Y] * len(E0s), E0s, fix_labels)


def benchmark(view_for, n_multi=32):
    torch.cuda.init()
    res = {"device": torch.cuda.get_device_name(0), "torch": torch.__version__}
    # one fit (fold 0), 10 restarts: CPU stage 1 vs GPU stage 1, and the trajectories
    v = view_for(0)
    M, Y = FR.grid(v)
    E0s = [FR.initial_labels(sd) for sd in range(10)]
    stage1_batch([M], [Y], E0s[:1])                          # warm-up (CUDA context, kernels)
    t0 = time.perf_counter()
    cpu = [FR.stage1(M, Y, e) for e in E0s]
    t_cpu = time.perf_counter() - t0
    t0 = time.perf_counter()
    gpu = stage1_batch([M] * 10, [Y] * 10, E0s)
    t_gpu = time.perf_counter() - t0
    same_state = all(np.array_equal(c[0], g[0]) and np.array_equal(c[1], g[1])
                     and np.array_equal(c[2] * c[1], g[2] * g[1]) and c[3] == g[3]
                     and c[6] == g[6] for c, g in zip(cpu, gpu))
    max_dJ = max(max(abs(a - b) for a, b in zip(c[5], g[5])) if len(c[5]) == len(g[5])
                 else float("inf") for c, g in zip(cpu, gpu))
    res["one_fit_k10"] = {"cpu_stage1_seconds": t_cpu, "gpu_stage1_seconds": t_gpu,
                          "same_final_state_every_restart": bool(same_state),
                          "same_sweep_count_every_restart": all(c[6] == g[6]
                                                                for c, g in zip(cpu, gpu)),
                          "max_abs_J_difference_along_trajectories_bits": max_dJ,
                          "sweeps_per_restart": [c[6] for c in cpu]}
    # whole fits (stages 1-4) through fit(), CPU vs GPU stage 1: same data?
    import timing
    t0 = time.perf_counter()
    d_cpu = FR.fit(v, starts=10)
    t_fc = time.perf_counter() - t0
    t0 = time.perf_counter()
    d_gpu = FR.fit(v, starts=10, stage1_fn=gpu_stage1_fn)
    t_fg = time.perf_counter() - t0
    res["one_fit_k10"].update({"cpu_full_fit_seconds": t_fc, "gpu_full_fit_seconds": t_fg,
                               "same_fitted_data": timing.data_hash(d_cpu)
                               == timing.data_hash(d_gpu)})
    # many fits batched: n_multi fold-style splits x 10 restarts in one lockstep batch
    Ms, Ys, Es = [], [], []
    for n in range(n_multi):
        m, y = FR.grid(view_for(n % 10))
        for sd in range(10):
            Ms.append(m)
            Ys.append(y)
            Es.append(FR.initial_labels(sd))
    t0 = time.perf_counter()
    gb = stage1_batch(Ms, Ys, Es)
    t_multi = time.perf_counter() - t0
    t0 = time.perf_counter()
    cb = [FR.stage1(m, y, e) for m, y, e in zip(Ms[:100], Ys[:100], Es[:100])]
    t_c100 = time.perf_counter() - t0
    agree = all(np.array_equal(c[1], g[1]) and np.array_equal(c[0], g[0]) and c[3] == g[3]
                for c, g in zip(cb, gb[:100]))
    res["batched_fits"] = {"n_fits": n_multi, "chains": len(Es),
                           "gpu_stage1_seconds_total": t_multi,
                           "gpu_stage1_seconds_per_fit": t_multi / n_multi,
                           "cpu_stage1_seconds_per_fit_1_core (first 10 fits)": t_c100 / 10,
                           "first_100_chains_same_final_state_as_cpu": bool(agree)}
    print(res, flush=True)
    return res
