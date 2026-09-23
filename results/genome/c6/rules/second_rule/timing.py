"""The timing cap of docs/plans/2026-09-23-second-rule-proposal.md section 1:

    k = 10 starts, unless the projected wall time is over 12 hours. Projection: time the rule's
    fits of folds 0-9 of shuffled bank 0 at k = 10, and scale their mean to the 1,341 rule fits
    the harness makes (1,250 cross-validation, 65 leave-one-type-out, 26 in-sample) at the run's
    worker count. If over 12 hours, k = 3 for every fit of the run. [...] No score is computed on
    shuffled bank 0 for this.

Shuffled bank 0 is harness.shuffled_bank(REAL, 0). Fold f's training view is every cell whose
fold (folds.csv, by cell position) is not f. The ten fits run at the same time, one per process
(one BLAS thread each). Nothing is decoded and nothing is scored: only the fit's wall time is
kept, with a hash of its data for the record.

Usage (from the repository root):
    tools/.venv/Scripts/python.exe results/genome/c6/rules/second_rule/timing.py [WORKERS]
WORKERS is the run's worker count (default: the harness's default, cpu_count - 2). Writes
timing_k10.json next to this file and prints the decision.
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

K = 10
N_RULE_FITS = 1341           # 1,250 cv + 65 leave-one-type-out + 26 in-sample
CAP_HOURS = 12.0


def data_hash(d):
    h = hashlib.sha256()
    for k in sorted(d):
        a = np.ascontiguousarray(d[k])
        h.update(k.encode() + str(a.dtype).encode() + str(a.shape).encode() + a.tobytes())
    return h.hexdigest()[:16]


def one(fold):
    os.environ.pop("SECOND_RULE_SPREAD_DIR", None)
    import harness as H
    import fit as R
    bank, inv = H.shuffled_bank(H.REAL, 0)
    assert inv["n_nonempty"] == 604 and inv["out_degrees_kept"] and inv["in_degrees_kept"]
    view = H.make_view(bank, H.FOLD != fold)
    t0 = time.perf_counter()
    d = R.fit(view, starts=K)
    sec = time.perf_counter() - t0
    return {"fold": fold, "seconds": sec, "data_hash16": data_hash(d), "pid": os.getpid()}


def main():
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else max(1, (os.cpu_count() or 2) - 2)
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=10) as ex:
        rows = list(ex.map(one, range(10)))
    wall = time.time() - t0
    mean = float(np.mean([r["seconds"] for r in rows]))
    proj_h = mean * N_RULE_FITS / workers / 3600.0
    k = 10 if proj_h <= CAP_HOURS else 3
    import harness as H
    rec = {"what": "Timing cap of the second rule (proposal section 1): the rule's fits of folds "
                   "0-9 of shuffled bank 0 at k = 10, ten at once, one per process. No decode "
                   "and no score of any kind.",
           "git_head": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                                      text=True).stdout.strip(),
           "fit_sha256_lf": H.sha256_lf(HERE / "fit.py"),
           "harness_sha256_lf": H.sha256_lf(C6 / "harness.py"),
           "cpu_count": os.cpu_count(), "k_timed": K, "per_fit": rows,
           "mean_seconds_per_fit": mean, "max_seconds_per_fit": max(r["seconds"] for r in rows),
           "wall_seconds_10_fits": wall, "rule_fits_in_run": N_RULE_FITS,
           "run_workers": workers,
           "projection": f"{mean:.3f} s x {N_RULE_FITS} fits / {workers} workers",
           "projected_hours": proj_h, "cap_hours": CAP_HOURS, "decision_k": k}
    (HERE / "timing_k10.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8",
                                          newline="\n")
    print(json.dumps({k_: v for k_, v in rec.items() if k_ != "per_fit"}, indent=1))


if __name__ == "__main__":
    main()
