"""The second candidate rule: N1 + a rank-1 bilinear term + field groups and target-side offset
sets. The LEARNER (uncharged).

Specification: docs/plans/2026-09-23-second-rule-proposal.md, registered at commit c3f996d.
  section 2.2  the model (decode.py in this directory; charged under C6 A5)
  section 2.3  the learner, implemented here
  section 2.4  the data arrays and their A5 cost
  section 6    the spread log: one file per fit
Every place where the text had to be read one way rather than another is listed in README.md
under "Readings"; each is marked below with [R<n>].

This file is also a C6 rule module in the harness's plug-in form (harness.py docstring): it
defines NAME, PROGRAM_FILES, RANK and fit(view, starts=...). The harness passes its --starts k
to `starts`. The proposal names the harness's own algorithms (fit_n1, bf_als, ridge_logistic,
the nested schemes of BF_r and N_EB), so the learner imports them from harness.py rather than
copying them [R1]. It reads nothing about the bank but the view; the one exception is the bank's
NAME, read from the caller's frame, and only to name the spread-log file [R10].
"""

import hashlib
import inspect
import json
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
C6 = HERE.parents[1]
if str(C6) not in sys.path:
    sys.path.insert(0, str(C6))
import harness as H  # noqa: E402

NAME = "second_rule_r1"
PROGRAM_FILES = [HERE / "decode.py"]
RANK = 1                     # section 1: r = round((130 + 16) / 130) = 1, by A11's arithmetic

# ---- constants fixed by the proposal (sections 2.3 and 2.4) --------------------------------
DEFAULT_STARTS = 10
ROUNDS = 3                   # alternating rounds of (u, v) and W
MU = 1.0                     # ridge penalty on the 16 entries of W; fixed, never tuned
LAMBDAS = list(H.BF_LAMBDAS)  # {1, 3, 10, 30, 100}, the harness's BF_r grid
EB_ALPHAS = list(H.EB_ALPHAS)  # N_EB's grid
SYM, ZERO = 32, 16           # 5-bit symmetric symbols: value = scale * (q - 16) / 16
M_TOP = 31                   # 5-bit symbols on [0, max m]: value = scale * q / 31 [R12]
LIB_MAX_SETS = 32
LIB_MAX_BITS = 800
LIB_MAX_OFFSETS = 48
LEVELS = 8                   # concentration levels 0..7 = min(7, floor(8 * value))
TOL = 1e-9                   # "falls by more than 1e-9"
EB_TIE = 1e-12               # the harness's tie tolerance in eb_choose and fit_neb
LAMBDA_TIE = 1e-9            # the harness's tie tolerance in fit_bf
DECODE_MAX_BYTES = 600       # section 2.5, G-size
DL_CAP_BITS = 9375           # section 2.4, worst case
SPREAD_ENV = "SECOND_RULE_SPREAD_DIR"

LAST_FIT = {}                # diagnostics of the last fit (uncharged; also written to the spread log)


def f32(x):
    """The value the decoder will see: the harness casts every float array to float32 (A5)."""
    return float(np.float32(x))


def groups(type_fields):
    """Section 2.1: field group G = 3 if stride_u > 1, else the role code (0, 1, 2)."""
    tf = np.asarray(type_fields)
    return np.where(tf[:, 0] > 1, 3, tf[:, 2]).astype(np.int64)


# ==========================================================================================
# Existence: N1 + u.v + W[G(s), G(t)]   (section 2.3, "Existence", steps 1-4)
# ==========================================================================================
def group_design(cells, G):
    X = np.zeros((len(cells), 16))
    X[np.arange(len(cells)), G[cells[:, 0]] * 4 + G[cells[:, 1]]] = 1.0
    return X


def fit_uvw(O, Y, M, G, lam, starts, rounds=ROUNDS, x_on=True):
    """Step 2: `rounds` alternating rounds from W = 0. (i) u, v by the harness's bf_als at rank 1
    with offset O + W[G, G]; (ii) W by ridge logistic on the 16 group-pair indicators, offset
    O + u.v, penalty MU, no intercept. With x_on False, step (ii) is skipped and W stays 0."""
    W = np.zeros((4, 4))
    cells = np.argwhere(M > 0)                    # training cells, (s, t) row-major [R2]
    X16 = group_design(cells, G)
    y = Y[cells[:, 0], cells[:, 1]]
    U = V = None
    for _ in range(rounds):
        off = O + W[np.ix_(G, G)] if x_on else O
        U, V = H.bf_als(off, Y, M, 1, lam, starts=starts)
        if x_on:
            z = (O + U @ V.T)[cells[:, 0], cells[:, 1]]
            W = H.ridge_logistic(X16, y, z, np.ones(16), lam=MU).reshape(4, 4)
    return U, V, W


def logit_grid(O, U, V, W, G, x_on=True):
    return O + U @ V.T + W[np.ix_(G, G)] if x_on else O + U @ V.T


def fit_existence(view, starts, rounds=ROUNDS, x_on=True):
    """Steps 1-4: N1's existence fit, then lambda by the harness's nested scheme for BF_r
    (inner folds, inner held-out log-likelihood, ties to the larger lambda), with steps 1-2
    inside every inner fit; then the final fit at the chosen lambda on the whole view."""
    G = groups(view.type_fields)
    n1 = H.fit_n1(view)
    M, Y = H._grid(view)
    inner = H.inner_folds(view)
    folds = sorted(set(inner.tolist()))
    ll = {lam: 0.0 for lam in LAMBDAS}
    for f in folds:
        keep = inner != f
        sv = H.subview(view, keep)
        Oi = H._n1_logit_grid(H.fit_n1(sv))
        Mi, _ = H._grid(sv)
        test = np.zeros((65, 65), bool)
        hc = view.cells[~keep]
        test[hc[:, 0], hc[:, 1]] = True
        for lam in LAMBDAS:
            U, V, W = fit_uvw(Oi, Y, Mi, G, lam, starts, rounds, x_on)
            p = np.clip(H._sig(logit_grid(Oi, U, V, W, G, x_on)), *H.CLIP)
            ll[lam] += float(np.sum(np.where(Y > 0, np.log(p), np.log(1 - p))[test]))
    best = max(ll.values())
    lam = max(l for l in LAMBDAS if ll[l] >= best - LAMBDA_TIE)
    O = H._n1_logit_grid(n1)
    U, V, W = fit_uvw(O, Y, M, G, lam, starts, rounds, x_on)
    return {"n1": n1, "O": O, "M": M, "Y": Y, "G": G, "lam": lam, "U": U, "V": V, "W": W,
            "inner_ll": ll}


# ---- quantisation (section 2.3, "Quantisation of the existence terms") ---------------------
def sym_scale(*xs):
    """max|x| * 16/15, so that both ends are representable [R3]; float32 as the decoder sees it."""
    mx = max(float(np.max(np.abs(x))) if np.size(x) else 0.0 for x in xs)
    return f32(mx * 16.0 / 15.0)


def to_sym(x, scale):
    """Nearest symbol, numpy's rint (half to even) [R11]; clipped to 0..31."""
    if scale == 0.0:
        return np.full(np.shape(x), ZERO, dtype=np.int64)
    return np.clip(np.rint(16.0 * np.asarray(x) / scale) + ZERO, 0, SYM - 1).astype(np.int64)


def from_sym(q, scale):
    return scale * (np.asarray(q, np.float64) - ZERO) / 16.0


def _loss(z, y):
    """Log-loss per cell in nats, log(1 + e^z) - y z (the unclipped training loss) [R4]."""
    return np.logaddexp(0.0, z) - y * z


class ExistQ:
    """The quantised existence model and its penalised training objective:
    sum of training log-loss + (1/2)(|a|^2 + |b|^2) + (lam/2)(|u|^2 + |v|^2) + (MU/2)|W|^2 [R5]."""

    def __init__(self, ex):
        n1 = ex["n1"]
        self.M, self.Y, self.G, self.lam = ex["M"] > 0, ex["Y"], ex["G"], ex["lam"]
        a, b, c = n1["ex_a"], n1["ex_b"], float(n1["ex_c"][0])
        u, v = ex["U"][:, 0], ex["V"][:, 0]
        mu_, mv_ = float(np.max(np.abs(u))), float(np.max(np.abs(v)))
        kappa = math.sqrt(mv_ / mu_) if mu_ > 0 and mv_ > 0 else 1.0
        u, v = u * kappa, v / kappa                       # max|u| = max|v|
        self.kappa = kappa
        self.s_ab, self.s_uv, self.s_w = sym_scale(a, b), sym_scale(u, v), sym_scale(ex["W"])
        self.q = {"a": to_sym(a, self.s_ab), "b": to_sym(b, self.s_ab),
                  "u": to_sym(u, self.s_uv), "v": to_sym(v, self.s_uv),
                  "W": to_sym(ex["W"].ravel(), self.s_w)}
        self.scale = {"a": self.s_ab, "b": self.s_ab, "u": self.s_uv, "v": self.s_uv,
                      "W": self.s_w}
        self.pen = {"a": 0.5, "b": 0.5, "u": 0.5 * self.lam, "v": 0.5 * self.lam, "W": 0.5 * MU}
        self.c = c
        self.moves = 0

    def val(self, k):
        return from_sym(self.q[k], self.scale[k])

    def grid(self):
        a, b, u, v, W = (self.val(k) for k in ("a", "b", "u", "v", "W"))
        return self.c + a[:, None] + b[None, :] + u[:, None] * v[None, :] + \
            W.reshape(4, 4)[np.ix_(self.G, self.G)]

    def objective(self):
        z = self.grid()
        ll = float(np.sum(_loss(z, self.Y)[self.M]))
        return ll + sum(self.pen[k] * float(np.sum(self.val(k) ** 2)) for k in self.q)

    def _delta(self, k, i, nq, Z):
        """Change of the objective if symbol i of block k moves to nq (Z = current logit grid)."""
        s = self.scale[k]
        old, new = s * (self.q[k][i] - ZERO) / 16.0, s * (nq - ZERO) / 16.0
        d = new - old
        if k == "a":
            sel, dz = (i, slice(None)), d
        elif k == "b":
            sel, dz = (slice(None), i), d
        elif k == "u":
            sel, dz = (i, slice(None)), d * self.val("v")
        elif k == "v":
            sel, dz = (slice(None), i), d * self.val("u")
        else:
            g, h = divmod(i, 4)
            rows, cols = np.flatnonzero(self.G == g), np.flatnonzero(self.G == h)
            sel, dz = np.ix_(rows, cols), d
        z0, y, m = Z[sel], self.Y[sel], self.M[sel]
        z1 = z0 + dz
        dl = float(np.sum((_loss(z1, y) - _loss(z0, y))[m]))
        return dl + self.pen[k] * (new * new - old * old), sel, z1

    def descend(self):
        """One pass, in the order a, b, u, v, W: each symbol tries q - 1 and q + 1 and keeps the
        better move if the objective falls by more than TOL (a tie between the two goes to q - 1)
        [R6]."""
        Z = self.grid()
        for k in ("a", "b", "u", "v", "W"):
            for i in range(len(self.q[k])):
                best = None
                for nq in (self.q[k][i] - 1, self.q[k][i] + 1):
                    if nq < 0 or nq > SYM - 1:
                        continue
                    dobj, sel, z1 = self._delta(k, i, nq, Z)
                    if dobj < -TOL and (best is None or dobj < best[0]):
                        best = (dobj, nq, sel, z1)
                if best is not None:
                    self.q[k][i] = best[1]
                    Z[best[2]] = best[3]
                    self.moves += 1

    def refit_c(self):
        """c refitted as a float by Newton on the training log-loss, everything else fixed."""
        rest = self.grid() - self.c
        z0, y = rest[self.M], self.Y[self.M]
        c = self.c
        for _ in range(200):
            p = H._sig(z0 + c)
            g = float(np.sum(p - y))
            if abs(g) < H.NEWTON_TOL:
                break
            c -= g / float(np.sum(p * (1 - p)))
        else:
            raise RuntimeError("Newton on c did not converge")
        self.c = f32(c)                               # stored as float32 [R13]


# ==========================================================================================
# Offset sets: a library, a source side and a target side (section 2.3, "Offset sets")
# ==========================================================================================
def set_key(s):
    return (len(s), s)                              # A4: smaller set, then lexicographic


def library_list(sets_in_cells):
    """Step 1: exact sets in decreasing frequency (A4 tie rule); add a set if the library then
    holds <= 32 sets, costs <= 800 bits under A5, and has <= 48 distinct offsets; else skip it."""
    cnt = Counter(sets_in_cells)
    lib = []
    for s in sorted(cnt, key=lambda k: (-cnt[k], len(k), k)):
        cand = lib + [s]
        if (len(cand) <= LIB_MAX_SETS and len({o for q in cand for o in q}) <= LIB_MAX_OFFSETS
                and H.data_bits({"L": pack_library(cand)}) <= LIB_MAX_BITS):
            lib = cand
    return lib


def pack_library(lib):
    out = []
    for s in lib:
        out += [len(s)] + [o[0] for o in s] + [o[1] for o in s]
    return np.array(out, dtype=np.int64)


def side_choose(J, cell_sid, cell_side, train, alpha, cand):
    """N_EB's formula for one side: p_x(S) = (c_x(S) + alpha g(S)) / (n_x + alpha) over all
    observed training sets S; the chosen set is the candidate (library) set A maximising
    sum_S p_x(S) J(A, S), first maximum in A4 order (the harness's eb_choose tolerance).
    Returns the chosen set id and the maximised expected Jaccard, per type."""
    tr_sid, tr_side = cell_sid[train], cell_side[train]
    obs = np.unique(tr_sid)
    g = np.bincount(tr_sid, minlength=J.shape[0])[obs] / len(tr_sid)
    Jc = J[np.ix_(cand, obs)]
    choice = np.zeros(65, dtype=int)
    value = np.zeros(65)
    n = np.zeros(65, dtype=int)
    for x in range(65):
        m = tr_side == x
        c = np.bincount(tr_sid[m], minlength=J.shape[0])[obs]
        p = (c + alpha * g) / (m.sum() + alpha)
        ej = Jc @ p
        j = int(np.flatnonzero(ej >= ej.max() - EB_TIE)[0])
        choice[x], value[x], n[x] = cand[j], ej[j], int(m.sum())
    return choice, value, n


def fit_offsets(view):
    """Steps 1-4 of "Offset sets"."""
    uniq, J, cell_sid, cell_src, cell_fold = H.eb_tables(view)   # uniq in A4 order
    keys = sorted(view.content)
    cell_tar = np.array([k[1] for k in keys])
    sid = {s: i for i, s in enumerate(uniq)}

    def lib_ids(train):
        lib = library_list([uniq[i] for i in cell_sid[train]])
        return lib, np.array(sorted(sid[s] for s in lib), dtype=int)   # candidates, A4 order

    folds = sorted(set(cell_fold.tolist()))
    inner_libs = {}
    for f in folds:
        train, test = cell_fold != f, cell_fold == f
        if test.any() and train.any():
            inner_libs[f] = lib_ids(train)[1]           # [R7] rebuilt on the inner training cells
    alphas = {}
    for side, cell_side in (("src", cell_src), ("tar", cell_tar)):
        best, best_alpha = -1.0, None
        for alpha in EB_ALPHAS:                          # N_EB's nested scheme (A18)
            tot, n = 0.0, 0
            for f, cand in inner_libs.items():
                train, test = cell_fold != f, cell_fold == f
                ch, _, _ = side_choose(J, cell_sid, cell_side, train, alpha, cand)
                tot += J[ch[cell_side[test]], cell_sid[test]].sum()
                n += int(test.sum())
            score_a = tot / n
            if score_a >= best - EB_TIE:                 # ties go to the larger alpha
                best, best_alpha = score_a, alpha
        alphas[side] = best_alpha
    lib, cand = lib_ids(np.ones(len(cell_sid), bool))
    pos = {s: i for i, s in enumerate(lib)}                 # index in storage order
    everything = np.ones(len(cell_sid), bool)
    out = {"lib": lib, "alpha_src": alphas["src"], "alpha_tar": alphas["tar"]}
    for side, cell_side, idx, lvl in (("src", cell_src, "A", "e"), ("tar", cell_tar, "B", "f")):
        ch, value, n = side_choose(J, cell_sid, cell_side, everything, alphas[side], cand)
        out[idx] = np.array([pos[uniq[i]] for i in ch], dtype=np.int64)
        out[lvl] = np.where(n > 0, np.minimum(LEVELS - 1, np.floor(LEVELS * value)), 0
                            ).astype(np.int64)
        out[lvl + "_value"] = value
    return out


# ==========================================================================================
# The fit
# ==========================================================================================
def fit(view, starts=DEFAULT_STARTS):
    """Section 2.3 in full; returns the data arrays of section 2.4."""
    ex = fit_existence(view, starts)
    q = ExistQ(ex)
    obj_rounded = q.objective()
    q.descend()
    obj_descended = q.objective()
    q.refit_c()
    off = fit_offsets(view)
    n1 = ex["n1"]
    # counts: N1's terms; m kept for the library's offsets only, in sorted offset order
    lib_offs = sorted({o for s in off["lib"] for o in s})
    m_all = {(a, b): v for a, b, v in zip(n1["m_du"].tolist(), n1["m_dv"].tolist(),
                                          n1["m_val"].tolist())}
    m = np.array([m_all[o] for o in lib_offs], dtype=np.float64)
    s_m = f32(float(m.max())) if m.size else 0.0
    q_m = (np.clip(np.rint(M_TOP * m / s_m), 0, M_TOP).astype(np.int64) if s_m > 0
           else np.zeros(len(m), np.int64))
    s_cnt = sym_scale(n1["cnt_a"], n1["cnt_b"])
    # sign: N1's per-source majority with N1's fallback (N0's majority) already resolved [R9]
    n0_sign = 1 if n1["n0_sign__sym2"][0] == 1 else -1
    sym = n1["src_sign__sym3"]
    sign = np.where(sym == 0, -1, np.where(sym == 1, 1, n0_sign)) == 1
    Q = np.concatenate([q.q["a"], q.q["b"], q.q["u"], q.q["v"], to_sym(n1["cnt_a"], s_cnt),
                        to_sym(n1["cnt_b"], s_cnt), off["A"], off["B"], q.q["W"], q_m])
    data = {"Q__sym32": Q.astype(np.int64),
            "c": np.array([q.c, q.s_ab, q.s_uv, s_cnt, q.s_w, s_m], dtype=np.float64),
            "L": pack_library(off["lib"]),
            "e__sym8": np.concatenate([off["e"], off["f"]]).astype(np.int64),
            "s": np.asarray(sign, dtype=bool)}
    assert Q.min() >= 0 and Q.max() < SYM and len(off["lib"]) <= LIB_MAX_SETS
    LAST_FIT.clear()
    LAST_FIT.update({
        "k": int(starts), "lambda": float(ex["lam"]), "inner_ll": {str(k): v for k, v in
                                                                  ex["inner_ll"].items()},
        "W_float": ex["W"].round(6).tolist(), "kappa": q.kappa,
        "objective_rounded": obj_rounded, "objective_descended": obj_descended,
        "objective_final": q.objective(), "cd_moves": q.moves,
        "alpha_src": off["alpha_src"], "alpha_tar": off["alpha_tar"],
        "n_library_sets": len(off["lib"]), "n_library_offsets": len(lib_offs),
        "library_bits": H.data_bits({"L": data["L"]}),
        "data_bits": H.data_bits(data),
        "cells_taking_target_side": int(np.sum(off["f"][None, :] > off["e"][:, None])),
        "e_levels": off["e"].tolist(), "f_levels": off["f"].tolist(),
    })
    if os.environ.get(SPREAD_ENV):
        _log_spread(os.environ[SPREAD_ENV], view)
    return data


# ==========================================================================================
# The spread log: one file per fit (section 6), never a shared file
# ==========================================================================================
def mask_sha256(view):
    """sha256 of the 65 x 65 training mask, rebuilt from the view's cells (the harness builds the
    view from exactly that mask)."""
    m = np.zeros((65, 65), bool)
    m[view.cells[:, 0], view.cells[:, 1]] = True
    return hashlib.sha256(m.tobytes()).hexdigest()


def caller_bank_name():
    """[R10] The harness hands fit() no bank name. Predictor.train(self, bank, train_mask) is on
    the call stack; its `bank.name` is read to name the file, and for nothing else."""
    f = inspect.currentframe()
    try:
        while f is not None:
            b = f.f_locals.get("bank")
            if b is not None and isinstance(getattr(b, "name", None), str):
                return b.name
            f = f.f_back
    finally:
        del f
    return "unknown"


def spread_file_name(bank_name, mask_sha):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", bank_name) + "__" + mask_sha[:16] + ".json"


def _log_spread(directory, view):
    d = Path(directory)
    d.mkdir(parents=True, exist_ok=True)
    bank, sha = caller_bank_name(), mask_sha256(view)
    rec = {"bank": bank, "train_mask_sha256": sha, "n_train_cells": int(len(view.cells)),
           "n_train_nonempty": int(np.sum(view.exists)), "pid": os.getpid()}
    rec.update(LAST_FIT)
    p = d / spread_file_name(bank, sha)
    tmp = p.with_suffix(f".tmp{os.getpid()}")
    tmp.write_text(json.dumps(rec, default=float) + "\n", encoding="utf-8", newline="\n")
    os.replace(tmp, p)
