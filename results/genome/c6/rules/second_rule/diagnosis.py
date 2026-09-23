"""Diagnosis of the two failed gates of rule #2 (G-e+ and G-o0; gates.json). NOT a gate, NOT a fix.

Mike's question (DPC Research group chat, 2026-09-23 16:41 UTC): why do "the scales" (the gates of
docs/plans/2026-09-23-second-rule-proposal.md section 2.5) fail, and how could they be made to work?
For each failed gate: is the fault in the gate (miscalibrated or underpowered, so that even a
model that knows the planted truth could not pass it reliably) or in the rule?

Nothing here touches the real bank, a real fold or shuffled bank 0. Nothing in fit.py, decode.py,
gate_banks.py, gates.py or harness.py is changed; constants of fit.py are patched only inside this
script's own worker processes, and only for the library-cap sweep and the plain-ML variant
(fit.fit_uvw swapped for fit_uvw_damped).

Seed discipline
  * the registered gate banks (seed 60000) are re-used, since the gate run has already seen them;
  * DIAGNOSTIC seeds: 70000-70099 (DIAG_SEEDS), drawn from the documented range 70000-70999;
  * RESERVED for a future re-gate: 80000-80999. Never generated, fitted or scored here.
  Every bank this script builds is listed, with a sha256 of its content, in diagnosis_banks.json.

Stages (run from the repository root with tools/.venv/Scripts/python.exe):
  diagnosis.py registered [N_PROC]  seed 60000: per-fold table, oracles, fixed-lambda sweep,
                                    offset decomposition and library-cap sweep
                                    -> diagnosis_registered.json
  diagnosis.py power [N_PROC]       GB1 draws on the diagnostic seeds at W* x 1, 2, 4
                                    -> diagnosis_power_rows.json
  diagnosis.py gb0 [N_PROC]         GB0 draws on the diagnostic seeds: G-e0, G-o0, N_EB spread,
                                    library-cap sweep -> diagnosis_gb0_rows.json
  diagnosis.py summary              aggregates -> diagnosis_summary.json, diagnosis_banks.json
"""

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
os.environ.pop("SECOND_RULE_SPREAD_DIR", None)

import functools
import hashlib
import json
import math
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
C6 = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(C6))

K = 10
REGISTERED_SEED = 60000
DIAG_RANGE = (70000, 70999)
RESERVED_RANGE = (80000, 80999)          # for a future re-gate: never touched here
DIAG_SEEDS = list(range(70000, 70100))
STRENGTHS = [1.0, 2.0, 4.0]
MU_ML = 1e-6                             # "plain maximum likelihood": mu -> 0 (1e-6 keeps Newton finite)
# At mu = 1e-6 a separated group pair (all its training cells empty) drives an entry of W far out,
# and the harness's undamped Newton overflows. The two plain-ML variants therefore use
# damped_logistic below (Newton with step halving on the penalised objective). The registered
# rule, BF_1, N1 and N_EB never use it.
INF = float("inf")
# library caps (max sets, max bits, max distinct offsets); the first is the registered one
CAPS = [(32, 800, 48)] + [(INF, b, INF) for b in (800, 1000, 1200, 1400, 1600, 1800, 2000,
                                                  2400, 3200, 4800)] + \
       [(32, INF, INF), (INF, INF, INF)]


def _cap(v):
    return None if v == INF else v          # None = no cap (json has no infinity)


def _assert_seed(seed):
    assert seed == REGISTERED_SEED or DIAG_RANGE[0] <= seed <= DIAG_RANGE[1], seed
    assert not RESERVED_RANGE[0] <= seed <= RESERVED_RANGE[1]


# ------------------------------------------------------------------------------------------
# banks
# ------------------------------------------------------------------------------------------
@functools.lru_cache(maxsize=8)
def bank(kind, seed, strength=1.0):
    """GB1-type (W* x strength, target flags on) or GB0-type (W* = 0, flags off), built exactly as
    gate_banks.gate_bank, from gate_banks.draws(seed). Returns (Bank, true logit grid)."""
    import harness as H
    from fit import groups
    from gate_banks import draws, BASE, NOISE, W_STAR
    _assert_seed(seed)
    d = draws(seed)
    real = sorted(H.REAL_CONTENT)
    G = groups(H.TYPE_FIELDS)
    Wst = W_STAR * strength if kind == "GB1" else np.zeros((4, 4))
    pi = d["pi"] if kind == "GB1" else np.zeros(65, bool)
    logit = BASE + d["a"][:, None] + d["b"][None, :] + np.outer(d["u"], d["v"]) + \
        Wst[np.ix_(G, G)]
    p = 1.0 / (1.0 + np.exp(-logit))
    content = {}
    for s in range(65):
        for t in range(65):
            if not d["u1"][s, t] < p[s, t]:
                continue
            if d["u2"][s, t] < NOISE:
                src = real[d["pool"][s, t]]
            else:
                src = real[d["tmpl"][t, 1]] if pi[t] else real[d["tmpl"][s, 0]]
            content[(s, t)] = {"offsets": dict(H.REAL_CONTENT[src]["offsets"]), "hull": [],
                               "sign": int(d["sign"][s])}
    name = f"{kind}x{strength:g}_seed{seed}"
    return H.Bank(name, content), logit, Wst, logit - Wst[np.ix_(G, G)]


def bank_record(kind, seed, strength=1.0):
    b = bank(kind, seed, strength)[0]
    h = hashlib.sha256(json.dumps(sorted((k[0], k[1], sorted(v["offsets"].items()), v["sign"])
                                         for k, v in b.content.items())).encode()).hexdigest()
    return {"kind": kind, "seed": seed, "W_star_scale": strength if kind == "GB1" else 0.0,
            "n_nonempty": len(b.content), "content_sha256": h}


# ------------------------------------------------------------------------------------------
# existence helpers
# ------------------------------------------------------------------------------------------
def ll(p, y):
    import harness as H
    p = np.clip(p, *H.CLIP)
    return float(np.mean(-(y * np.log(p) + (~y) * np.log(1 - p))))


def held_cells(f):
    import harness as H
    held = H.FOLD == f
    return held, H.ALL_CELLS[held[H.ALL_CELLS[:, 0], H.ALL_CELLS[:, 1]]]


def n1_with_offset(view, E):
    """N1's ridge logistic (lambda = 1, intercept unpenalised) with a fixed extra offset E[s, t]
    (damped Newton: at W* x 4 the harness's undamped Newton overflows on this offset)."""
    s, t = view.cells[:, 0], view.cells[:, 1]
    X = np.zeros((len(s), 131))
    X[:, 0] = 1
    X[np.arange(len(s)), 1 + s] = 1
    X[np.arange(len(s)), 66 + t] = 1
    pen = np.ones(131)
    pen[0] = 0
    w = damped_logistic(X, view.exists.astype(float), E[s, t], 1.0, pen)
    return w[0] + w[1:66][:, None] + w[66:131][None, :]


def oracle_wstar(view, E):
    """O-W*: knows the planted group table exactly (E = W*[G, G]); c, a, b are N1's ridge fit with
    E as a fixed offset, and u, v are BF_1's algorithm with offset O + E, lambda by BF's nested
    scheme (inner folds, ties to the larger lambda). Returns the logit grid and lambda."""
    import harness as H
    M, Y = H._grid(view)
    inner = H.inner_folds(view)
    lls = {lam: 0.0 for lam in H.BF_LAMBDAS}
    for f in sorted(set(inner.tolist())):
        keep = inner != f
        sv = H.subview(view, keep)
        Oi = n1_with_offset(sv, E) + E
        Mi, _ = H._grid(sv)
        test = np.zeros((65, 65), bool)
        hc = view.cells[~keep]
        test[hc[:, 0], hc[:, 1]] = True
        for lam in H.BF_LAMBDAS:
            U, V = H.bf_als(Oi, Y, Mi, 1, lam, starts=K)
            p = np.clip(H._sig(Oi + U @ V.T), *H.CLIP)
            lls[lam] += float(np.sum(np.where(Y > 0, np.log(p), np.log(1 - p))[test]))
    best = max(lls.values())
    lam = max(l for l in H.BF_LAMBDAS if lls[l] >= best - 1e-9)
    O = n1_with_offset(view, E) + E
    U, V = H.bf_als(O, Y, M, 1, lam, starts=K)
    return O + U @ V.T, lam


def damped_logistic(X, y, offset, lam, pen=None):
    """Ridge logistic, penalty lam * pen_j on coefficient j (pen = 1 by default), by Newton with
    step halving on the penalised objective; stops when |gradient| < 1e-8 or the objective stops
    falling. Same optimum as harness.ridge_logistic where that converges."""
    pen = np.ones(X.shape[1]) if pen is None else np.asarray(pen, float)

    def obj(w):
        z = X @ w + offset
        return float(np.sum(np.logaddexp(0.0, z) - y * z) + 0.5 * lam * np.sum(pen * w * w))
    w = np.zeros(X.shape[1])
    f = obj(w)
    for _ in range(2000):
        z = X @ w + offset
        p = 0.5 * (1.0 + np.tanh(0.5 * z))
        g = X.T @ (p - y) + lam * pen * w
        if np.linalg.norm(g) < 1e-8:
            return w
        Hm = X.T @ (X * (p * (1 - p))[:, None]) + lam * np.diag(pen)
        step = np.linalg.solve(Hm, g)
        t = 1.0
        while t > 1e-12:
            fn = obj(w - t * step)
            if fn <= f:
                break
            t *= 0.5
        if f - fn <= 1e-13 * max(1.0, abs(f)):
            return w - t * step
        w, f = w - t * step, fn
    return w


def fit_uvw_damped(O, Y, M, G, lam, starts, rounds=3, x_on=True):
    """fit.fit_uvw with the W step by damped_logistic at mu = MU_ML (plain ML)."""
    import harness as H
    import fit as R
    W = np.zeros((4, 4))
    cells = np.argwhere(M > 0)
    X16 = R.group_design(cells, G)
    y = Y[cells[:, 0], cells[:, 1]]
    U = V = None
    for _ in range(rounds):
        U, V = H.bf_als(O + W[np.ix_(G, G)], Y, M, 1, lam, starts=starts)
        z = (O + U @ V.T)[cells[:, 0], cells[:, 1]]
        W = damped_logistic(X16, y, z, MU_ML).reshape(4, 4)
    return U, V, W


def oracle_ml_w(view, Z0, G):
    """O-ML-W: knows the planted c, a, b, u, v exactly (Z0 = the true logit without W*); fits the
    16 entries of W by plain maximum likelihood (mu = 1e-6) on the training cells."""
    import harness as H
    from fit import group_design
    X = group_design(view.cells, G)
    W = damped_logistic(X, view.exists.astype(float), Z0[view.cells[:, 0], view.cells[:, 1]],
                        MU_ML).reshape(4, 4)
    return Z0 + W[np.ix_(G, G)], W


def rule_existence(view, plain_ml=False):
    """The rule's existence fit; returns (float logit grid, quantised logit grid, lambda, W,
    inner log-likelihoods). plain_ml swaps fit.fit_uvw for fit_uvw_damped (X_e by plain ML) in
    this process only, and restores it."""
    import fit as R
    old = R.fit_uvw
    try:
        if plain_ml:
            R.fit_uvw = fit_uvw_damped
        ex = R.fit_existence(view, K)
    finally:
        R.fit_uvw = old
    zf = R.logit_grid(ex["O"], ex["U"], ex["V"], ex["W"], ex["G"])
    if plain_ml:
        return zf, None, ex["lam"], ex["W"], ex["inner_ll"]
    q = R.ExistQ(ex)
    q.descend()
    q.refit_c()
    return zf, q.grid(), ex["lam"], ex["W"], ex["inner_ll"]


# ------------------------------------------------------------------------------------------
# offset helpers
# ------------------------------------------------------------------------------------------
def jac(pred_sets, b, cells):
    out = []
    for (s, t), ps in zip(cells.tolist(), pred_sets):
        if (s, t) in b.content:
            a, c = set(ps), set(b.content[(s, t)]["offsets"])
            out.append(len(a & c) / len(a | c) if a | c else 1.0)
    return float(np.mean(out))


def offsets_at_caps(view, b, cells, caps):
    """The rule's offset part (fit.fit_offsets) under the given library caps; fit.py's constants
    are patched in this process only and restored."""
    import harness as H
    import fit as R
    s, t = cells[:, 0], cells[:, 1]
    held_ne = [(x, y) for x, y in zip(s.tolist(), t.tolist()) if (x, y) in b.content]
    old = (R.LIB_MAX_SETS, R.LIB_MAX_BITS, R.LIB_MAX_OFFSETS)
    out = []
    try:
        for cap in caps:
            R.LIB_MAX_SETS, R.LIB_MAX_BITS, R.LIB_MAX_OFFSETS = cap
            off = R.fit_offsets(view)
            lib = off["lib"]
            libset = set(lib)
            out.append({
                "cap_sets": _cap(cap[0]), "cap_bits": _cap(cap[1]), "cap_offsets": _cap(cap[2]),
                "rule": jac([lib[off["B"][y]] if off["f"][y] > off["e"][x] else lib[off["A"][x]]
                             for x, y in zip(s, t)], b, cells),
                "source_side_only": jac([lib[off["A"][x]] for x in s], b, cells),
                "n_sets": len(lib), "n_offsets": len({o for q in lib for o in q}),
                "library_bits": H.data_bits({"L": R.pack_library(lib)}) if lib else 0,
                "heldout_sets_in_library": float(np.mean(
                    [tuple(sorted(b.content[k]["offsets"])) in libset for k in held_ne])),
                "heldout_cells_on_target_side": float(np.mean(
                    [off["f"][y] > off["e"][x] for x, y in held_ne])),
                "alpha_src": off["alpha_src"], "alpha_tar": off["alpha_tar"]})
    finally:
        R.LIB_MAX_SETS, R.LIB_MAX_BITS, R.LIB_MAX_OFFSETS = old
    return out


def dl_estimate(n_sets, n_offsets, library_bits):
    """DL(rule) in bits for a library of this size, with the registered layout otherwise, at the
    registered decode program's 3,952 bits (a decoder that reads a wider index would change it
    by a few bytes; not measured). Up to 32 sets, A and B stay 5-bit symbols in Q__sym32; above
    that they move to their own array 'AB__sym<2^k>'."""
    import harness as H
    n_m = n_offsets
    data = {"c": np.zeros(6), "e__sym8": np.zeros(130, np.int64), "s": np.zeros(65, bool)}
    if n_sets <= 32:
        data["Q__sym32"] = np.zeros(8 * 65 + 16 + n_m, np.int64)
    else:
        data["Q__sym32"] = np.zeros(6 * 65 + 16 + n_m, np.int64)
        data[f"AB__sym{2 ** math.ceil(math.log2(n_sets))}"] = np.zeros(130, np.int64)
    return 3952 + H.data_bits(data) + library_bits


# ------------------------------------------------------------------------------------------
# jobs
# ------------------------------------------------------------------------------------------
def job_gb1(job):
    """One fold of a GB1-type bank: every existence model, and the offsets for G-o+."""
    import harness as H
    import fit as R
    seed, strength, f = job
    b, Z, Wst, Z0 = bank("GB1", seed, strength)
    held, cells = held_cells(f)
    view = H.make_view(b, ~held)
    s, t = cells[:, 0], cells[:, 1]
    y = b.exists[s, t]
    G = R.groups(H.TYPE_FIELDS)
    bf = H.cv_fold(H.bf_predictor(1), b, f)
    n1 = H.cv_fold(H.N1, b, f)
    neb = H.cv_fold(H.NEB, b, f)
    try:
        zf, zq, lam, W, _ = rule_existence(view)
    except RuntimeError as e:          # the registered rule itself crashed: recorded, not hidden
        return {"seed": seed, "strength": strength, "fold": f, "rule_crashed": str(e),
                "N1": n1["existence"], "BF1": bf["existence"]}
    zm, _, lam_m, W_m, _ = rule_existence(view, plain_ml=True)
    zo, lam_o = oracle_wstar(view, Wst[np.ix_(G, G)])
    zml, W_ml = oracle_ml_w(view, Z0, G)
    off = R.fit_offsets(view)
    lib = off["lib"]
    return {"seed": seed, "strength": strength, "fold": f,
            "N1": n1["existence"], "BF1": bf["existence"], "BF1_lambda": bf["bf_lambda"],
            "rule": ll(H._sig(zq[s, t]), y), "rule_float": ll(H._sig(zf[s, t]), y),
            "rule_lambda": lam, "rule_W": np.round(W, 6).tolist(),
            "rule_mu0_float": ll(H._sig(zm[s, t]), y), "rule_mu0_lambda": lam_m,
            "rule_mu0_W": np.round(W_m, 4).tolist(),
            "oracle_Wstar": ll(H._sig(zo[s, t]), y), "oracle_Wstar_lambda": lam_o,
            "oracle_ML_W": ll(H._sig(zml[s, t]), y), "oracle_ML_W_W": np.round(W_ml, 4).tolist(),
            "oracle_true": ll(H._sig(Z[s, t]), y),
            "offset_rule": jac([lib[off["B"][yy]] if off["f"][yy] > off["e"][x] else
                                lib[off["A"][x]] for x, yy in zip(s, t)], b, cells),
            "offset_N_EB": neb["offset"], "n_heldout": int(len(cells)), "n_heldout_ne": int(y.sum())}


def job_gb0(job):
    """One fold of a GB0-type bank: G-e0's existence numbers, and G-o0 with the library sweep."""
    import harness as H
    seed, f = job
    b, Z, _, _ = bank("GB0", seed)
    held, cells = held_cells(f)
    view = H.make_view(b, ~held)
    s, t = cells[:, 0], cells[:, 1]
    y = b.exists[s, t]
    bf = H.cv_fold(H.bf_predictor(1), b, f)
    n1 = H.cv_fold(H.N1, b, f)
    neb = H.cv_fold(H.NEB, b, f)
    zf, zq, lam, W, _ = rule_existence(view)
    # an N_EB-equivalent: N_EB's own choice (harness.eb_choose, unrestricted candidates) at the
    # alpha the rule's source side chose; its gap to N_EB is the alpha-choice noise only
    import fit as R
    uniq, J, sid, src, _ = H.eb_tables(view)
    every = np.ones(len(sid), bool)
    off = R.fit_offsets(view)
    ch = H.eb_choose(J, sid, src, every, off["alpha_src"])
    return {"seed": seed, "fold": f,
            "N1": n1["existence"], "BF1": bf["existence"], "BF1_lambda": bf["bf_lambda"],
            "rule": ll(H._sig(zq[s, t]), y), "rule_float": ll(H._sig(zf[s, t]), y),
            "rule_lambda": lam, "oracle_true": ll(H._sig(Z[s, t]), y),
            "offset_N_EB": neb["offset"], "offset_N_EB_alpha": neb["eb_alpha"],
            "offset_N_EB_at_rule_alpha": jac([uniq[ch[x]] for x in s], b, cells),
            "caps": offsets_at_caps(view, b, cells, CAPS),
            "n_heldout_ne": int(y.sum())}


def job_lambda(job):
    """Registered banks: held-out log-loss of the rule's float model and of BF_1 at each fixed
    lambda, and both nested schemes' inner log-likelihoods (the lambda = 100 question)."""
    import harness as H
    import fit as R
    kind, f = job
    b = bank(kind, REGISTERED_SEED)[0]
    held, cells = held_cells(f)
    view = H.make_view(b, ~held)
    s, t = cells[:, 0], cells[:, 1]
    y = b.exists[s, t]
    G = R.groups(view.type_fields)
    n1 = H.fit_n1(view)
    O = H._n1_logit_grid(n1)
    M, Y = H._grid(view)
    rule_fixed, bf_fixed, rule_W, rule_uv = {}, {}, {}, {}
    for lam in H.BF_LAMBDAS:
        U, V, W = R.fit_uvw(O, Y, M, G, lam, K)
        rule_fixed[lam] = ll(H._sig(R.logit_grid(O, U, V, W, G)[s, t]), y)
        rule_W[lam] = np.round(W, 4).tolist()
        rule_uv[lam] = float(np.sqrt(np.mean((U @ V.T) ** 2)))
        Ub, Vb = H.bf_als(O, Y, M, 1, lam, starts=K)
        bf_fixed[lam] = ll(H._sig((O + Ub @ Vb.T)[s, t]), y)
    ex_rule = R.fit_existence(view, K)
    ex_bf = R.fit_existence(view, K, rounds=1, x_on=False)   # = the harness's BF_1 (gate G-bf)
    return {"bank": kind, "fold": f, "rule_heldout_at_lambda": rule_fixed,
            "BF1_heldout_at_lambda": bf_fixed, "rule_W_at_lambda": rule_W,
            "rule_rms_uv_at_lambda": rule_uv,
            "rule_inner_ll": ex_rule["inner_ll"], "rule_lambda": ex_rule["lam"],
            "BF1_inner_ll": ex_bf["inner_ll"], "BF1_lambda": ex_bf["lam"]}


def _init():
    import harness as H
    H.STARTS = K


def run(fn, jobs, n_proc):
    with ProcessPoolExecutor(max_workers=n_proc, initializer=_init) as ex:
        return list(ex.map(fn, jobs, chunksize=1))


def dump(path, obj):
    path.write_text(json.dumps(obj, indent=1, default=float) + "\n", encoding="utf-8",
                    newline="\n")


def header():
    import harness as H
    return {"harness_sha256_lf": H.sha256_lf(C6 / "harness.py"),
            "fit_sha256_lf": H.sha256_lf(HERE / "fit.py"),
            "gate_banks_sha256_lf": H.sha256_lf(HERE / "gate_banks.py"),
            "diagnosis_sha256_lf": H.sha256_lf(HERE / "diagnosis.py"), "k": K,
            "diagnostic_seed_range": DIAG_RANGE, "reserved_seed_range_not_touched": RESERVED_RANGE}


def main():
    stage = sys.argv[1]
    n_proc = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    _init()
    t0 = time.time()
    if stage == "registered":
        # the registered banks re-built by this script must equal gate_banks.gate_bank's
        from gate_banks import gate_bank
        for kind in ("GB1", "GB0"):
            assert bank(kind, REGISTERED_SEED)[0].content == gate_bank(kind).content
        gb1 = run(job_gb1, [(REGISTERED_SEED, 1.0, f) for f in range(10)], n_proc)
        gb0 = run(job_gb0, [(REGISTERED_SEED, f) for f in range(10)], n_proc)
        lam = run(job_lambda, [(k, f) for k in ("GB1", "GB0") for f in range(10)], n_proc)
        out = dict(header(), what="Registered gate banks (seed 60000), re-used: per-fold "
                   "existence of every model, oracles, fixed-lambda sweep, offset decomposition "
                   "and library-cap sweep.", GB1=gb1, GB0=gb0, lambda_sweep=lam,
                   runtime_s=round(time.time() - t0, 1))
        dump(HERE / "diagnosis_registered.json", out)
    elif stage == "power":
        jobs = [(sd, st, f) for st in STRENGTHS for sd in DIAG_SEEDS for f in range(10)]
        rows = run(job_gb1, jobs, n_proc)
        dump(HERE / "diagnosis_power_rows.json",
             dict(header(), what="GB1-type banks on the diagnostic seeds, W* scaled by 1, 2 and "
                  "4; one row per (seed, strength, fold).", rows=rows,
                  runtime_s=round(time.time() - t0, 1)))
    elif stage == "gb0":
        rows = run(job_gb0, [(sd, f) for sd in DIAG_SEEDS for f in range(10)], n_proc)
        dump(HERE / "diagnosis_gb0_rows.json",
             dict(header(), what="GB0-type banks on the diagnostic seeds; one row per (seed, "
                  "fold).", caps=[[_cap(v) for v in c] for c in CAPS], rows=rows, runtime_s=round(time.time() - t0, 1)))
    elif stage == "summary":
        import diagnosis_summary
        diagnosis_summary.main()
    else:
        sys.exit(f"unknown stage {stage}")


if __name__ == "__main__":
    main()
