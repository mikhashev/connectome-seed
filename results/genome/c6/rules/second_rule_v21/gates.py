"""The single re-gate of rule #2.1: rule #2's gates (../second_rule/gates.py) as amended by
docs/plans/2026-09-23-rule-2-1-registration.md, run once. Changes against rule #2's script
(registration section 9, step 3): two hard asserts before G-size and before any bank is built
(the pinned decoder; worst-case DL at the caps <= fit.DL_LIMIT_BITS), G-e+ on the fold mean (S1),
and gate banks from seed 80000 only (section 3). A failed assert is not a gate result.

  G-size  the decode program compresses to <= 600 bytes (A5's lzma rule, the file alone) and
          imports only numpy and the standard library. Checked FIRST, before any fit.
  G-det   two fits of the same training view give byte-identical data (GB1, fold 0).
  G-bf    with X off (W = 0, one round) and no quantisation, the learner's (u, v) and existence
          predictions equal the harness's BF_1 on shuffled bank 0, all 10 folds, to 1e-9.
  G-e+    on GB1, the mean over 10 folds of (rule's existence margin over N1 - BF_1's) > +0.002.
  G-e0    on GB0, mean held-out existence margin over N1 of the rule minus BF_1's is <= +0.002.
  G-o+    on GB1, the rule's held-out offset Jaccard beats N_EB's in >= 9 of 10 folds.
  G-o0    on GB0, mean held-out offset Jaccard of the rule minus N_EB's is in [-0.010, +0.010].

Nothing here fits or scores the real bank or a real fold. Shuffled bank 0 is used only by G-bf,
which compares predictions (u, v, lambda, p) and computes no score. A failed gate stops the work
(section 2.5; registration section 4): this script records it and exits non-zero; it does not
tune anything.

Usage (from the repository root):
    tools/.venv/Scripts/python.exe results/genome/c6/rules/second_rule_v21/gates.py [N_PROC]
Writes gates.json next to this file.
"""

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import hashlib
import json
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
C6 = HERE.parents[1]
ROOT = C6.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(C6))

K = 10                        # the run's expected k (section 1, timing cap)
TAU = 1e-9
BF_TOL = 1e-9
E0_MAX = 0.002
O0_BAND = 0.010
MIN_WINS = 9
E_PLUS_MIN = 0.002            # S1: G-e+ passes only if the fold mean exceeds the P4 tie band
GATE_SEED = 80000             # registration section 3: the lowest unused seed of 80000-80999
DECODE_SHA256_LF = "39a049013af18a1e89e534d9d378a5f59a772b894d7fab5b79f82f702723a15a"


def data_bytes(d):
    h = hashlib.sha256()
    for k in sorted(d):
        a = np.ascontiguousarray(d[k])
        h.update(k.encode() + str(a.dtype).encode() + str(a.shape).encode() + a.tobytes())
    return h.hexdigest()


def _init():
    os.environ.pop("SECOND_RULE_SPREAD_DIR", None)          # gates write no spread log
    import harness as H
    H.STARTS = K


def _bank(name):
    import harness as H
    if name == "shuffle0":
        b, inv = H.shuffled_bank(H.REAL, 0)
        assert inv["n_nonempty"] == 604 and inv["out_degrees_kept"] and inv["in_degrees_kept"]
        return b
    return _gate_bank(name, GATE_SEED)


def _gate_bank(name, seed):
    """GB1 or GB0 from gate_banks.py (rule #2's file), with the registered seed and no other."""
    if seed != GATE_SEED:
        raise SystemExit(f"seed {seed} refused: the registration fixes seed {GATE_SEED} (section 3)")
    assert name in ("GB1", "GB0")
    import gate_banks
    gate_banks.SEED = seed          # gate_bank() reads the module's SEED when it is called
    return gate_banks.gate_bank(name)


def bank_content_sha256(b):
    """The same content hash as ../second_rule/diagnosis.py's bank_record."""
    return hashlib.sha256(json.dumps(sorted((k[0], k[1], sorted(v["offsets"].items()), v["sign"])
                                            for k, v in b.content.items())).encode()).hexdigest()


def _pred(key):
    import harness as H
    import fit as R
    if key == "rule":
        return H.Predictor(R.NAME, R.PROGRAM_FILES, R.fit, rank=R.RANK)
    return {"N1": H.N1, "N_EB": H.NEB, "BF1": H.bf_predictor(1)}[key]


def task_cv(job):
    """One held-out fold of one predictor on a GATE bank (GB1 / GB0 only)."""
    bank_name, key, f = job
    assert bank_name in ("GB1", "GB0")
    import harness as H
    return job, H.cv_fold(_pred(key), _bank(bank_name), f)


def task_bf(f):
    """G-bf on shuffled bank 0, fold f: predictions only, no score."""
    import harness as H
    import fit as R
    bank = _bank("shuffle0")
    held = H.FOLD == f
    view = H.make_view(bank, ~held)
    t0 = time.perf_counter()
    ex = R.fit_existence(view, K, rounds=1, x_on=False)
    t1 = time.perf_counter()
    bf = H.fit_bf(view, 1)
    t2 = time.perf_counter()
    cells = H.ALL_CELLS[held[H.ALL_CELLS[:, 0], H.ALL_CELLS[:, 1]]]
    s, t = cells[:, 0], cells[:, 1]
    p_rule = H._sig(R.logit_grid(ex["O"], ex["U"], ex["V"], ex["W"], ex["G"], False)[s, t])
    p_bf = H._sig((H._n1_logit_grid(bf) + bf["bf_U"] @ bf["bf_V"].T)[s, t])
    return {"fold": f, "lambda_rule": float(ex["lam"]), "lambda_bf": float(bf["bf_lambda"][0]),
            "max_abs_diff_u": float(np.max(np.abs(ex["U"] - bf["bf_U"]))),
            "max_abs_diff_v": float(np.max(np.abs(ex["V"] - bf["bf_V"]))),
            "max_abs_diff_p_heldout": float(np.max(np.abs(p_rule - p_bf))),
            "W_is_zero": bool(np.all(ex["W"] == 0)),
            "seconds_learner": round(t1 - t0, 2), "seconds_harness_bf": round(t2 - t1, 2)}


def main():
    n_proc = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    _init()
    import harness as H
    import fit as R

    # ---- the two hard asserts of registration section 9 step 3, before G-size and any bank --
    if not (R.PROGRAM_FILES == [HERE / "decode.py"]
            and H.sha256_lf(HERE / "decode.py") == DECODE_SHA256_LF):
        raise AssertionError("decode.py is not the decoder pinned by the registration (1.2)")
    worst = {"Q__sym32": np.zeros(6 * 65 + 16 + R.LIB_MAX_OFFSETS, np.int64),
             "AB__sym64": np.zeros(130, np.int64), "c": np.zeros(6),
             "e__sym8": np.zeros(130, np.int64), "s": np.zeros(65, bool)}
    worst_data = H.data_bits(worst) + R.LIB_MAX_BITS
    worst_dl = worst_data + H.program_bits(R.PROGRAM_FILES)
    if not worst_dl <= R.DL_LIMIT_BITS:
        raise AssertionError(f"worst-case DL {worst_dl} > {R.DL_LIMIT_BITS}")

    t_start = time.time()
    rec = {"what": "Rule #2.1 re-gate (rule #2 proposal section 2.5, amended by the rule #2.1 "
                   "registration), run once. Scores are on the synthetic gate banks GB1/GB0 "
                   "(seed 80000) only; G-bf compares predictions on shuffled bank 0 and computes "
                   "no score.",
           "proposal_commit": "c3f996d", "registration_commit": "15da501", "k": K,
           "gate_seed": GATE_SEED,
           "preflight_asserts": {"decode_sha256_lf_pinned": DECODE_SHA256_LF,
                                 "worst_case_data_bits": worst_data,
                                 "worst_case_dl_bits": worst_dl,
                                 "dl_limit_bits": R.DL_LIMIT_BITS, "pass": True},
           "git_head": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                                      text=True).stdout.strip(),
           "harness_sha256_lf": H.sha256_lf(C6 / "harness.py"),
           "fit_sha256_lf": H.sha256_lf(HERE / "fit.py"),
           "decode_sha256_lf": H.sha256_lf(HERE / "decode.py"),
           "gate_banks_sha256_lf": H.sha256_lf(HERE / "gate_banks.py"),
           "gates": {}}
    out_path = HERE / "gates.json"

    def save():
        rec["runtime_s"] = round(time.time() - t_start, 1)
        out_path.write_text(json.dumps(rec, indent=1, default=float) + "\n", encoding="utf-8",
                            newline="\n")

    # ---- G-size, before any fit ---------------------------------------------------------
    try:
        H.check_imports(R.PROGRAM_FILES)
        imports_ok = True
    except ValueError as e:
        imports_ok = str(e)
    bits = H.program_bits(R.PROGRAM_FILES)
    g = {"bytes": bits // 8, "bits": bits, "cap_bytes": R.DECODE_MAX_BYTES,
         "imports_ok": imports_ok}
    g["pass"] = bool(bits // 8 <= R.DECODE_MAX_BYTES and imports_ok is True)
    rec["gates"]["G-size"] = g
    print("G-size", g, flush=True)
    save()
    if not g["pass"]:
        sys.exit("G-size FAILED: stop (section 2.5)")

    banks = {nm: _bank(nm) for nm in ("GB1", "GB0")}
    rec["gate_banks"] = {nm: {"seed": GATE_SEED, "n_nonempty": len(b.content),
                              "content_sha256": bank_content_sha256(b)}
                         for nm, b in banks.items()}

    # ---- G-det --------------------------------------------------------------------------
    view = H.make_view(banks["GB1"], H.FOLD != 0)
    t0 = time.perf_counter()
    d1 = R.fit(view, starts=K)
    t1 = time.perf_counter()
    d2 = R.fit(H.make_view(banks["GB1"], H.FOLD != 0), starts=K)
    h1, h2 = data_bytes(d1), data_bytes(d2)
    P = _pred("rule")
    g = {"sha256_fit_1": h1, "sha256_fit_2": h2, "pass": h1 == h2,
         "seconds_one_fit": round(t1 - t0, 2),
         "dl_bits": P.dl(d1), "data_bits": H.data_bits(d1), "program_bits": P.prog_bits}
    rec["gates"]["G-det"] = g
    print("G-det", g, flush=True)
    save()

    # ---- the pooled work: G-bf folds, and held-out folds on GB1 / GB0 ---------------------
    jobs = [(nm, key, f) for nm in ("GB1", "GB0") for key in ("rule", "BF1", "N1", "N_EB")
            for f in range(H.N_FOLDS)]
    with ProcessPoolExecutor(max_workers=n_proc, initializer=_init) as ex:
        bf_fut = [ex.submit(task_bf, f) for f in range(H.N_FOLDS)]
        cv_res = dict(ex.map(task_cv, jobs))
        bf_rows = [x.result() for x in bf_fut]

    worst = max(max(r["max_abs_diff_u"], r["max_abs_diff_v"], r["max_abs_diff_p_heldout"])
                for r in bf_rows)
    g = {"bank": "harness.shuffled_bank(REAL, 0)", "per_fold": bf_rows,
         "max_abs_diff_any": worst, "tolerance": BF_TOL,
         "lambdas_equal": all(r["lambda_rule"] == r["lambda_bf"] for r in bf_rows),
         "pass": bool(worst <= BF_TOL and all(r["lambda_rule"] == r["lambda_bf"]
                                              and r["W_is_zero"] for r in bf_rows))}
    rec["gates"]["G-bf"] = g
    print("G-bf max diff", worst, "pass", g["pass"], flush=True)

    per = {nm: {key: [cv_res[(nm, key, f)] for f in range(H.N_FOLDS)]
                for key in ("rule", "BF1", "N1", "N_EB")} for nm in ("GB1", "GB0")}
    rec["per_fold_scores_gate_banks"] = per

    def wins(a, b, f):
        return int(sum(H.cmp(x, y, f) == 1 for x, y in zip(a, b)))

    gb1, gb0 = per["GB1"], per["GB0"]
    m_rule = H.margin(gb1["rule"], gb1["N1"], "existence")
    m_bf = H.margin(gb1["BF1"], gb1["N1"], "existence")
    rec["gates"]["G-e+"] = {"bank": "GB1", "rule_margin_over_N1": m_rule,
                            "BF1_margin_over_N1": m_bf, "difference": m_rule - m_bf,
                            "min_exclusive": E_PLUS_MIN,
                            "rule_wins_vs_BF1_existence_descriptive":
                                wins(gb1["rule"], gb1["BF1"], "existence"),
                            "pass": m_rule - m_bf > E_PLUS_MIN}
    m_rule = H.margin(gb0["rule"], gb0["N1"], "existence")
    m_bf = H.margin(gb0["BF1"], gb0["N1"], "existence")
    rec["gates"]["G-e0"] = {"bank": "GB0", "rule_margin_over_N1": m_rule,
                            "BF1_margin_over_N1": m_bf, "difference": m_rule - m_bf,
                            "max": E0_MAX, "pass": m_rule - m_bf <= E0_MAX}
    w = wins(gb1["rule"], gb1["N_EB"], "offset")
    rec["gates"]["G-o+"] = {"bank": "GB1", "rule_wins_vs_N_EB_offset": w, "min": MIN_WINS,
                            "rule_offset_mean": float(np.mean([s["offset"] for s in gb1["rule"]])),
                            "N_EB_offset_mean": float(np.mean([s["offset"] for s in gb1["N_EB"]])),
                            "pass": w >= MIN_WINS}
    d = H.margin(gb0["rule"], gb0["N_EB"], "offset")
    rec["gates"]["G-o0"] = {"bank": "GB0", "rule_minus_N_EB_offset_mean": d,
                            "band": [-O0_BAND, O0_BAND], "pass": -O0_BAND <= d <= O0_BAND}
    rec["all_pass"] = all(x["pass"] for x in rec["gates"].values())
    save()
    for k, v in rec["gates"].items():
        print(k, "PASS" if v["pass"] else "FAIL",
              {a: b for a, b in v.items() if a not in ("per_fold", "pass")}, flush=True)
    print("all gates pass:", rec["all_pass"])
    if not rec["all_pass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
