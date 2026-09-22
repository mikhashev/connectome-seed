"""The first candidate rule: named labels, named rules, named motifs. The LEARNER (uncharged).

Specification: docs/plans/2026-09-23-first-rule-proposal.md, registered at commit 5a46886.
  section 2.1  the genome and its quantisation grids
  section 2.2  the decoder (decode.py in this directory; charged under C6 A5)
  section 2.4  the fitting procedure (stages 1-4), implemented here
  section 4.3  the random-label arm (labels="random")
Every place where the text had to be read one way rather than another is listed in README.md
under "Readings and deviations"; each is marked below with [R<n>].

This file is also a C6 rule module in the harness's plug-in form (harness.py docstring): it
defines NAME, PROGRAM_FILES, RANK and fit(view, starts=...). The harness passes its --starts k
to `starts`. It imports nothing from the harness and reads nothing but the view.
"""

from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
NAME = "first_rule_k12"
PROGRAM_FILES = [HERE / "decode.py"]
RANK = 12                                   # section 2.6: r = k = 12

# ---- constants fixed by the proposal (section 2.5 "Fixed before any data") ----------------
N_LABELS = 12
R_MAX = 40
M_MAX = 16
O_MAX = 64
RULE_BITS = 25                              # section 2.4: one rule's data cost in J
MAX_SWEEPS = 50
DEFAULT_STARTS = 10
RIDGE_LAMBDA = 1e-3
RANDOM_LABEL_SEED = 20260923                # section 4.3
P_INIT = 0.25
CLIP = (0.001, 0.999)                       # section 2.2 step 2
TOL = 1e-9                                  # [R1] "J falls" means falls by more than 1e-9 bits

# ---- quantisation grids (section 2.1) ------------------------------------------------------
RHO = (np.arange(16) + 0.5) / 16
LOG1M_RHO = np.log1p(-RHO)                  # log(1 - rho) per level
EPS = 2.0 ** -(1 + np.arange(16) / 2)
W_STEP, W_LEVELS = 0.17, 32
AB_STEP, AB_LEVELS, AB_ZERO = 0.25, 16, 8
PI_STEP, PI_LEVELS = 0.35, 16

LAST_FIT = {}                               # diagnostics of the last fit (uncharged, section 4.4)


# ==========================================================================================
# Stage 1: labels, rules, reliabilities, leak (existence only)
# ==========================================================================================
def cell_cost(S, eps, Y):
    """-log2 P(observed existence) per cell, with S = sum over firing rules of log(1 - rho)."""
    p = np.clip(1.0 - (1.0 - eps) * np.exp(S), *CLIP)      # [R2] J uses the clipped p
    return -np.log2(np.where(Y, p, 1.0 - p))


def grid(view):
    M = np.zeros((65, 65), bool)
    Y = np.zeros((65, 65), bool)
    M[view.cells[:, 0], view.cells[:, 1]] = True
    Y[view.cells[:, 0], view.cells[:, 1]] = view.exists
    return M, Y


def initial_labels(seed, n_labels=N_LABELS):
    """e_t[l] ~ Bernoulli(0.25), types in index order (row-major draw). [R3]"""
    return np.random.default_rng(seed).random((65, n_labels)) < P_INIT


def eps_level_nearest(M, Y):
    base = Y[M].mean()
    return int(np.argmin(np.abs(EPS - base)))               # [R4] nearest in value, ties low


def total_J(S, eps_q, M, Y, n_rules):
    return float(np.sum(np.where(M, cell_cost(S, EPS[eps_q], Y), 0.0)) + RULE_BITS * n_rules)


def rule_matrix(P, Q):
    return np.where(P, LOG1M_RHO[Q], 0.0)


def stage1(M, Y, E0, fix_labels=False, trace=None):
    """One restart of section 2.4 stage 1. Returns (E, P, Q, eps_q, J, per-sweep J list, sweeps).

    E (65, K) bool expression; P (K, K) bool rule present; Q (K, K) int rho level; eps_q int.
    """
    K = E0.shape[1]
    E = E0.astype(bool).copy()
    Ef = E.astype(np.float64)
    P = np.zeros((K, K), bool)
    Q = np.zeros((K, K), np.int64)
    eq = eps_level_nearest(M, Y)
    n_rules = 0
    S = Ef @ rule_matrix(P, Q) @ Ef.T
    C = np.where(M, cell_cost(S, EPS[eq], Y), 0.0)
    traj = [total_J(S, eq, M, Y, n_rules)]
    sweeps = 0
    for _ in range(MAX_SWEEPS):
        sweeps += 1
        changed = False
        eps = EPS[eq]
        # (a) toggle each ordered label pair, in index order
        for i in range(K):
            rows = np.flatnonzero(E[:, i])
            for j in range(K):
                if not P[i, j] and n_rules >= R_MAX:
                    continue                                 # an add could not be kept
                cols = np.flatnonzero(E[:, j])
                ix = np.ix_(rows, cols)
                Sb, Cb, Mb, Yb = S[ix], C[ix], M[ix], Y[ix]
                if P[i, j]:
                    Sn = Sb - LOG1M_RHO[Q[i, j]]
                    Cn = np.where(Mb, cell_cost(Sn, eps, Yb), 0.0)
                    d = float(np.sum(Cn - Cb)) - RULE_BITS
                    if d < -TOL:
                        P[i, j] = False
                        n_rules -= 1
                        S[ix], C[ix] = Sn, Cn
                        changed = True
                        if trace is not None:
                            trace.append(("del", i, j, d))
                else:
                    Sn = Sb[None] + LOG1M_RHO[:, None, None]
                    Cn = np.where(Mb[None], cell_cost(Sn, eps, Yb[None]), 0.0)
                    d = (Cn - Cb[None]).sum(axis=(1, 2)) + RULE_BITS
                    q = int(np.argmin(d))                    # best of 16 levels, ties low
                    if d[q] < -TOL:
                        P[i, j], Q[i, j] = True, q
                        n_rules += 1
                        S[ix], C[ix] = Sn[q], Cn[q]
                        changed = True
                        if trace is not None:
                            trace.append(("add", i, j, q, float(d[q])))
        # (a, end) re-choose rho of every present rule, in index order
        for i in range(K):
            rows = np.flatnonzero(E[:, i])
            for j in range(K):
                if not P[i, j]:
                    continue
                cols = np.flatnonzero(E[:, j])
                ix = np.ix_(rows, cols)
                Sb, Cb, Mb, Yb = S[ix], C[ix], M[ix], Y[ix]
                Sn = (Sb - LOG1M_RHO[Q[i, j]])[None] + LOG1M_RHO[:, None, None]
                Cn = np.where(Mb[None], cell_cost(Sn, eps, Yb[None]), 0.0)
                d = (Cn - Cb[None]).sum(axis=(1, 2))
                q = int(np.argmin(d))
                if d[q] < d[Q[i, j]] - TOL:                  # [R5] change only if J falls
                    Q[i, j] = q
                    S[ix], C[ix] = Sn[q], Cn[q]
                    changed = True
                    if trace is not None:
                        trace.append(("rho", i, j, q, float(d[q])))
        # (b) flip each expression bit, types in index order, labels in index order
        if not fix_labels:
            L = rule_matrix(P, Q)
            used = P.any(axis=0) | P.any(axis=1)
            for t in range(65):
                for l in range(K):
                    if not used[l]:
                        continue                             # flip changes no cell: d = 0
                    E[t, l] = not E[t, l]
                    Ef[t, l] = 1.0 - Ef[t, l]
                    srow = Ef @ (Ef[t] @ L)                  # S'[t, :]  (as column vector)
                    scol = Ef @ (L @ Ef[t])                  # S'[:, t]
                    scol[t] = srow[t]
                    crow = np.where(M[t], cell_cost(srow, eps, Y[t]), 0.0)
                    ccol = np.where(M[:, t], cell_cost(scol, eps, Y[:, t]), 0.0)
                    d = float(np.sum(crow - C[t]) + np.sum(ccol - C[:, t])
                              - (ccol[t] - C[t, t]))
                    if d < -TOL:
                        S[t, :], S[:, t] = srow, scol
                        C[t, :], C[:, t] = crow, ccol
                        changed = True
                        if trace is not None:
                            trace.append(("flip", t, l, d))
                    else:
                        E[t, l] = not E[t, l]
                        Ef[t, l] = 1.0 - Ef[t, l]
        # (c) re-choose the leak
        Cs = np.where(M[None], cell_cost(S[None], EPS[:, None, None], Y[None]), 0.0)
        d = Cs.sum(axis=(1, 2))
        q = int(np.argmin(d))
        if d[q] < d[eq] - TOL:
            eq = q
            changed = True
            if trace is not None:
                trace.append(("eps", q))
        # end of sweep: the state is recomputed from the genome alone
        S = Ef @ rule_matrix(P, Q) @ Ef.T
        C = np.where(M, cell_cost(S, EPS[eq], Y), 0.0)
        traj.append(total_J(S, eq, M, Y, n_rules))
        if not changed:
            break
    return E, P, Q, eq, traj[-1], traj, sweeps


def rules_list(P, Q):
    """Present rules as (i, j, rho level), in (i, j) index order."""
    return [(int(i), int(j), int(Q[i, j])) for i, j in zip(*np.nonzero(P))]


# ==========================================================================================
# D6 on the hex lattice (regularity.py rot, refl, d6_images; image 2q = rot^q, 2q+1 = refl o rot^q)
# ==========================================================================================
def image(pts, g):
    out = []
    for u, v in pts:
        for _ in range(g // 2):
            u, v = u + v, -u
        if g % 2:
            u, v = v, u
        out.append((u, v))
    return out


def canon(pts):
    return min(tuple(sorted(image(pts, g))) for g in range(12))


def shape_str(shape):
    return ";".join(f"{u},{v}" for u, v in shape)


def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if (a | b) else 1.0


def best_orientation(shape, cell):
    """Lowest g maximising Jaccard(g(shape), cell); returns (g, Jaccard)."""
    js = [jaccard(image(shape, g), cell) for g in range(12)]
    g = int(np.argmax(js))
    return g, js[g]


def winner(E, rules, s, t):
    """section 2.2 step 3: argmax rho among firing rules, ties to the lowest (i, j)."""
    best = None
    for r, (i, j, q) in enumerate(rules):
        if E[s, i] and E[t, j] and (best is None or q > rules[best][2]):
            best = r
    return best


# ==========================================================================================
# Stage 2: motifs; stage 3: strengths; stage 4: signs
# ==========================================================================================
def stage2(E, rules, content):
    keys = sorted(content)
    won = {r: [] for r in range(len(rules))}
    for k in keys:
        r = winner(E, rules, *k)
        if r is not None:
            won[r].append(k)
    offs = {k: sorted(content[k]["offsets"]) for k in keys}
    shp = {k: canon(offs[k]) for k in keys}
    counts = Counter(shp[k] for r in won for k in won[r])
    order = sorted(counts, key=lambda s: (-counts[s], shape_str(s)))
    lib, total = [], 0
    for s in order:
        if len(lib) >= M_MAX or total + len(s) > O_MAX:
            break                                            # [R6] "stop adding", not skip
        lib.append(s)
        total += len(s)
    # pi: mean over the motif's won cells of the D6-aligned, sum-normalised n_syn profile
    won_cells = [k for r in won for k in won[r]]
    pis = []
    for s in lib:
        prof = []
        for k in won_cells:
            if shp[k] != s:
                continue
            cell = set(offs[k])
            g = next(g for g in range(12) if set(image(s, g)) == cell)   # [R7] lowest g
            n = np.array([content[k]["offsets"][o] for o in image(s, g)], float)
            prof.append(n / n.sum())
        pbar = np.mean(prof, axis=0)
        q = np.round((np.log(pbar) - np.log(pbar.max())) / PI_STEP) + (PI_LEVELS - 1)
        pis.append(np.clip(q, 0, PI_LEVELS - 1).astype(np.int64))       # [R8] max at level 15
    # each rule's motif and orientation
    m_r = [None] * len(rules)
    g_r = [0] * len(rules)
    for r in range(len(rules)):
        cells = won[r]
        if not cells or not lib:
            continue
        c = Counter(shp[k] for k in cells)
        top = min(c, key=lambda s: (-c[s], shape_str(s)))
        if top in lib:
            m = lib.index(top)
        else:                                                            # [R9]
            mj = [np.mean([best_orientation(sh, offs[k])[1] for k in cells]) for sh in lib]
            m = int(np.argmax(mj))
        go = Counter(best_orientation(lib[m], offs[k])[0] for k in cells)
        g_r[r] = min(go, key=lambda g: (-go[g], g))                      # [R10]
        m_r[r] = m
    fb = fallback_motif(lib, [m for m in m_r if m is not None])
    for r in range(len(rules)):
        if m_r[r] is None:                                               # [R11]
            m_r[r], g_r[r] = fb, 0
    return lib, pis, m_r, g_r, won


def fallback_motif(lib, assigned):
    if not lib:
        return 0
    if ((0, 0),) in lib:
        return lib.index(((0, 0),))
    c = np.bincount(np.asarray(assigned, np.int64), minlength=len(lib) + 1)
    return int(np.argmax(c))


def stage3(E, rules, content, won):
    rows = [(r, s, t, np.log(sum(content[(s, t)]["offsets"].values())))
            for r in won for (s, t) in won[r]]
    nR = len(rules)
    X = np.zeros((len(rows), nR + 130))
    y = np.zeros(len(rows))
    for n, (r, s, t, v) in enumerate(rows):
        X[n, r] = X[n, nR + s] = X[n, nR + 65 + t] = 1.0
        y[n] = v
    beta = np.linalg.solve(X.T @ X + RIDGE_LAMBDA * np.eye(nR + 130), X.T @ y)
    wq = np.clip(np.round(beta[:nR] / W_STEP), 0, W_LEVELS - 1).astype(np.int64)
    aq = np.clip(np.round(beta[nR:nR + 65] / AB_STEP) + AB_ZERO, 0, AB_LEVELS - 1).astype(np.int64)
    bq = np.clip(np.round(beta[nR + 65:] / AB_STEP) + AB_ZERO, 0, AB_LEVELS - 1).astype(np.int64)
    ri = np.array([x[0] for x in rows], np.int64)
    si = np.array([x[1] for x in rows], np.int64)
    ti = np.array([x[2] for x in rows], np.int64)

    def sse():
        pred = W_STEP * wq[ri] + AB_STEP * (aq[si] - AB_ZERO) + AB_STEP * (bq[ti] - AB_ZERO)
        return float(np.sum((y - pred) ** 2))

    for arr, n_lv in [(wq, W_LEVELS), (aq, AB_LEVELS), (bq, AB_LEVELS)]:
        for x in range(len(arr)):                    # rules in index order, then a, then b
            cur = arr[x]
            errs = []
            for lv in range(n_lv):
                arr[x] = lv
                errs.append(sse())
            best = int(np.argmin(errs))
            arr[x] = best if errs[best] < errs[cur] - 1e-12 else cur        # [R12]
    all_tot = [np.log(sum(c["offsets"].values())) for c in content.values()]
    w0 = int(np.clip(np.round(np.mean(all_tot) / W_STEP), 0, W_LEVELS - 1)) if all_tot else 0
    return wq, aq, bq, w0


def stage4(content):
    """section 2.3: majority sign of the source's training cells; tie/none: training majority,
    and a tie there gives +1 (N1's rule, C6 A4)."""
    signs = [c["sign"] for c in content.values()]
    maj = 1 if sum(x == 1 for x in signs) >= sum(x == -1 for x in signs) else -1
    out = np.full(65, maj == 1)
    for s in range(65):
        sg = [c["sign"] for (a, _), c in content.items() if a == s]
        pos, neg = sum(x == 1 for x in sg), sum(x == -1 for x in sg)
        if pos != neg:
            out[s] = pos > neg
    return out


# ==========================================================================================
# The fit
# ==========================================================================================
def pack(E, rules, lib, pis, m_r, g_r, wq, aq, bq, w0, eq, sign):
    R = np.array([[i, j, m, g, q] for (i, j, q), m, g in zip(rules, m_r, g_r)],
                 np.int64).reshape(-1, 5)
    return {"E": E.astype(bool), "S": sign.astype(bool),
            "R__sym16": R,
            "W__sym32": np.concatenate([wq, [w0]]).astype(np.int64),
            "A__sym16": np.concatenate([aq, bq, [eq]]).astype(np.int64),
            "L": np.array([len(s) for s in lib], np.int64),
            "O": np.array([o for s in lib for o in s], np.int64).reshape(-1, 2),
            "P__sym16": np.concatenate(pis).astype(np.int64) if pis else np.zeros(0, np.int64)}


def fit(view, starts=DEFAULT_STARTS, labels="learned", n_labels=N_LABELS, stage1_fn=None):
    """section 2.4. `starts` restarts use seeds 0 .. starts-1 [R13]; the lowest training J wins,
    ties to the lower seed. labels="random" is the section 4.3 arm (expression frozen)."""
    M, Y = grid(view)
    runs = []
    if labels == "random":
        E0s = [np.random.default_rng(RANDOM_LABEL_SEED).random((65, n_labels)) < P_INIT]
    else:
        E0s = [initial_labels(sd, n_labels) for sd in range(starts)]
    if stage1_fn is None:
        runs = [stage1(M, Y, E0, fix_labels=(labels == "random")) for E0 in E0s]
    else:
        runs = stage1_fn(M, Y, E0s, labels == "random")
    best = min(range(len(runs)), key=lambda x: (runs[x][4], x))
    E, P, Q, eq, J, traj, sweeps = runs[best]
    rules = rules_list(P, Q)
    lib, pis, m_r, g_r, won = stage2(E, rules, view.content)
    wq, aq, bq, w0 = stage3(E, rules, view.content, won)
    sign = stage4(view.content)
    LAST_FIT.clear()
    LAST_FIT.update({
        "best_start": best, "J_per_start": [r[4] for r in runs],
        "sweeps_per_start": [r[6] for r in runs], "traj_per_start": [r[5] for r in runs],
        "rules_per_start": [rules_list(r[1], r[2]) for r in runs],
        "E_per_start": [r[0].copy() for r in runs],
        "n_rules": len(rules), "n_motifs": len(lib), "n_offsets": int(sum(map(len, lib))),
        "duplicate_label_sets": int(sum(1 for a in range(E.shape[1]) for b in range(a)
                                        if (E[:, a] == E[:, b]).all())),
    })
    return pack(E, rules, lib, pis, m_r, g_r, wq, aq, bq, w0, eq, sign)
