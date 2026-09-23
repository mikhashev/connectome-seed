"""Determinism and DL sanity check of rule #2.1 on the self-test bank ST0 only (gate_banks.py:
GB0's construction with seed 61000). No score of any kind: nothing is decoded against held-out
cells. Not a gate.

For each of the 10 folds, the rule is fitted at k = 10 on ST0's training view; its data bits,
DL and library size are recorded. Fold 0 is fitted twice and the two data dicts must be
byte-identical.

Usage (from the repository root):
    tools/.venv/Scripts/python.exe results/genome/c6/rules/second_rule_v21/selftest_st0.py [N_PROC]
Writes selftest_st0.json next to this file.
"""

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
os.environ.pop("SECOND_RULE_SPREAD_DIR", None)

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

K = 10
BANK = "ST0"


def data_sha(d):
    h = hashlib.sha256()
    for k in sorted(d):
        a = np.ascontiguousarray(d[k])
        h.update(k.encode() + str(a.dtype).encode() + str(a.shape).encode() + a.tobytes())
    return h.hexdigest()


def one(job):
    fold, rep = job
    import harness as H
    import fit as R
    from gate_banks import gate_bank
    H.STARTS = K
    b = gate_bank(BANK)
    view = H.make_view(b, H.FOLD != fold)
    t0 = time.perf_counter()
    d = R.fit(view, starts=K)
    sec = time.perf_counter() - t0
    info = dict(R.LAST_FIT)
    P = H.Predictor(R.NAME, R.PROGRAM_FILES, R.fit, rank=R.RANK)
    return {"fold": fold, "repeat": rep, "data_sha256": data_sha(d), "seconds": round(sec, 2),
            "dl_bits": P.dl(d), "program_bits": P.prog_bits, "data_bits": H.data_bits(d),
            "array_bits": {k: H.data_bits({k: v}) for k, v in d.items()},
            "n_library_sets": info["n_library_sets"],
            "n_library_offsets": info["n_library_offsets"],
            "library_bits": info["library_bits"], "lambda": info["lambda"],
            "max_index_AB": int(d["AB__sym64"].max())}


def main():
    n_proc = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    import harness as H
    import fit as R
    t0 = time.time()
    jobs = [(f, 0) for f in range(10)] + [(0, 1)]
    with ProcessPoolExecutor(max_workers=n_proc) as ex:
        rows = list(ex.map(one, jobs))
    first = next(r for r in rows if r["fold"] == 0 and r["repeat"] == 0)
    again = next(r for r in rows if r["fold"] == 0 and r["repeat"] == 1)
    folds = [r for r in rows if r["repeat"] == 0]
    rec = {"what": "Rule #2.1 on the self-test bank ST0 (seed 61000) only: determinism and DL. "
                   "No score. Not a gate.",
           "git_head": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                                      text=True).stdout.strip(),
           "harness_sha256_lf": H.sha256_lf(C6 / "harness.py"),
           "fit_sha256_lf": H.sha256_lf(HERE / "fit.py"),
           "decode_sha256_lf": H.sha256_lf(HERE / "decode.py"),
           "gate_banks_sha256_lf": H.sha256_lf(HERE / "gate_banks.py"),
           "k": K, "bank": BANK, "per_fold": folds, "fold0_repeat": again,
           "deterministic_fold0": first["data_sha256"] == again["data_sha256"],
           "dl_max_bits": max(r["dl_bits"] for r in folds),
           "dl_worst_case_at_caps_bits": R.DL_CAP_BITS, "dl_limit_bits": R.DL_LIMIT_BITS,
           "all_folds_within_worst_case": all(r["dl_bits"] <= R.DL_CAP_BITS for r in folds),
           "runtime_s": round(time.time() - t0, 1)}
    (HERE / "selftest_st0.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8",
                                            newline="\n")
    print(json.dumps({k: v for k, v in rec.items() if k not in ("per_fold", "fold0_repeat")},
                     indent=1))
    for r in folds:
        print(r["fold"], r["dl_bits"], r["n_library_sets"], r["n_library_offsets"],
              r["library_bits"], r["lambda"], r["seconds"])
    if not (rec["deterministic_fold0"] and rec["all_folds_within_worst_case"]):
        sys.exit(1)


if __name__ == "__main__":
    main()
