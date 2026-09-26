"""Validate the GPU port of rule #2.1's existence fit (gpu_rule) on the knockout view, fit by fit
against the registered run's store of synthetic fits (read-only):
  connectome-seed-data/knockout_regrow/flyvis65_20260925T171656Z_74de0401a21f/raw_fits.json.gz
keys "world:<family>:<j>[|sh:<sd>]||ko||rule". Everything after the existence fit is the rule's
own fit.py code (in pool workers); p is decoded by the rule's own decode.py through
Predictor.decode, and the four scores by harness.score, as knockout_regrow._w_group does.

Real block: never read, fit or scored; raw_fits_real.json.gz is never opened.

Usage:
  python validate_rule.py --worlds all --base --tag base45           # the 45 worlds' ko fits
  python validate_rule.py --worlds R:0 --n-sh 99 --tag sh_R0          # one world's shuffles
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import gzip  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import pathlib  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from concurrent.futures import ProcessPoolExecutor  # noqa: E402

import numpy as np  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import prep  # noqa: E402
import harness as H  # noqa: E402
import knockout_regrow as K  # noqa: E402

REF = (HERE.parents[4] / "connectome-seed-data" / "knockout_regrow"
       / "flyvis65_20260925T171656Z_74de0401a21f" / "raw_fits.json.gz")
SCORE_KEYS = ("existence", "offset", "counts", "sign", "sign_n", "n_ne")


def same(a, b):
    if isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b):
        return True
    return a == b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--worlds", default="R:0")
    ap.add_argument("--n-sh", type=int, default=99)
    ap.add_argument("--base", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--worlds-per-batch", type=int, default=45)
    ap.add_argument("--tag", default="run")
    a = ap.parse_args()

    t_all = time.time()
    terms = K.degree_terms()
    K._w_init(10, terms, True)
    assert H.STARTS == 10
    import torch
    import gpu_rule

    g = H.load_rule(K.RULE_PATH).fit.__globals__        # constants and helpers of fit.py
    ref = json.load(gzip.open(REF))
    worlds = ([f"{w['family']}:{w['j']}" for w in K.world_specs()] if a.worlds == "all"
              else a.worlds.split(","))
    batches = [worlds[i:i + a.worlds_per_batch] for i in range(0, len(worlds), a.worlds_per_batch)]
    rows, timing = [], []
    pool = ProcessPoolExecutor(max_workers=a.workers, initializer=prep.init_rule_worker,
                               initargs=(terms,))
    try:
        for wb in batches:
            keys = ([f"world:{w}" for w in wb] if a.base
                    else [f"world:{w}|sh:{sd}" for w in wb for sd in range(a.n_sh)])
            for k_ in gpu_rule.TIMES:
                gpu_rule.TIMES[k_] = 0.0
            t0 = time.time()
            preps = list(pool.map(prep.prepare_key, keys, chunksize=2))
            t1 = time.time()
            exs = gpu_rule.batched_fit_existence(preps, g, H.STARTS)
            t2 = time.time()
            res = list(pool.map(prep.rule_post_key, list(zip(keys, exs)), chunksize=1))
            t3 = time.time()
            tm = {"worlds": wb, "n_banks": len(keys), "prep_secs": t1 - t0,
                  "existence_secs": t2 - t1, "existence_bf_als_gpu_secs":
                  gpu_rule.TIMES["bf_als_gpu"], "existence_ridge_cpu_secs":
                  gpu_rule.TIMES["ridge_cpu"], "post_cpu_secs": t3 - t2,
                  "post_worker_secs_sum": sum(r["secs"] for r in res), "total_secs": t3 - t0}
            timing.append(tm)
            for key, rr in zip(keys, res):
                refv = ref[f"{key}||ko||rule"]
                p, pr = rr["p"], np.asarray(refv["p"], np.float64)
                y = np.asarray(refv["y"], bool)
                ag, ar = K.auc(p, y), K.auc(pr, y)
                rows.append({
                    "key": key, "y_match": bool((rr["y"] == y).all()),
                    "lam_gpu": rr["lam"], "lam_ref": refv["lam"],
                    "auc_gpu": ag, "auc_ref": ar,
                    "auc_diff": None if ag is None or ar is None else abs(ag - ar),
                    "max_abs_p_diff": float(np.max(np.abs(p - pr))),
                    "p_bit_equal": bool(np.array_equal(p, pr)),
                    "label_mismatches": int(np.sum((p >= 0.5) != (pr >= 0.5))),
                    "score_equal": all(same(rr["score"][k], refv["score"][k]) for k in SCORE_KEYS
                                       if k in refv["score"]),
                    "ref_secs": refv["secs"]})
            sub = rows[-len(keys):]
            print(f"{len(keys)} banks ({wb[0]}..{wb[-1]}): prep {tm['prep_secs']:.1f}s, existence "
                  f"{tm['existence_secs']:.1f}s (GPU bf_als {tm['existence_bf_als_gpu_secs']:.1f}s,"
                  f" ridge {tm['existence_ridge_cpu_secs']:.1f}s), rest of fit {tm['post_cpu_secs']:.1f}s;"
                  f" bit-equal {sum(x['p_bit_equal'] for x in sub)}/{len(sub)}, lam mismatches "
                  f"{sum(x['lam_gpu'] != x['lam_ref'] for x in sub)}, max|dp| "
                  f"{max(x['max_abs_p_diff'] for x in sub):.2e}", flush=True)
    finally:
        pool.shutdown()

    diffs = [x["auc_diff"] for x in rows if x["auc_diff"] is not None]
    summary = {
        "fits": len(rows), "y_mismatch": sum(not x["y_match"] for x in rows),
        "lam_mismatches": sum(x["lam_gpu"] != x["lam_ref"] for x in rows),
        "p_bit_equal": sum(x["p_bit_equal"] for x in rows),
        "max_abs_p_diff": max(x["max_abs_p_diff"] for x in rows),
        "max_auc_diff": max(diffs) if diffs else None,
        "label_mismatches": sum(x["label_mismatches"] for x in rows), "labels_total": 64 * len(rows),
        "score_equal": sum(x["score_equal"] for x in rows),
        "total_secs": sum(t["total_secs"] for t in timing), "wall_secs": time.time() - t_all,
        "cpu_ref_fit_secs_sum": sum(x["ref_secs"] for x in rows), "workers": a.workers,
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu"}
    out = HERE / f"validation_rule_{a.tag}.json"
    out.write_text(json.dumps({"summary": summary, "timing": timing, "rows": rows}, indent=1))
    print(json.dumps(summary, indent=1))
    for x in sorted(rows, key=lambda x: -x["max_abs_p_diff"])[:10]:
        print("worst:", x["key"], x["lam_gpu"], x["lam_ref"], f"{x['max_abs_p_diff']:.3e}",
              x["label_mismatches"], x["auc_diff"], x["score_equal"])


if __name__ == "__main__":
    main()
