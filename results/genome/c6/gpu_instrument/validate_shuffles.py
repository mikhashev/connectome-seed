"""Validate engine v2 (gpu_bf2) on the shuffled banks: BF_1..BF_4 on the knockout view of the
"world:<family>:<j>|sh:<sd>" banks, fit by fit against the registered run's store of synthetic
fits (read-only):
  connectome-seed-data/knockout_regrow/flyvis65_20260925T171656Z_74de0401a21f/raw_fits.json.gz
Comparison goes through the harness's own decode (knockout_regrow._pred(pk).decode(data,
BLOCK_CELLS)), so p is comparable bit for bit with the stored p.

Banks are built exactly as the CPU instrument builds them (knockout_regrow.build_bank with the
"|sh:" key and synthetic_only=True, after knockout_regrow._w_init(10, degree_terms(), True)).
Real block: never read, fit or scored; raw_fits_real.json.gz is never opened.

Usage:
  python validate_shuffles.py --worlds R:0 --n-sh 99 --workers 8 --tag one_world
  python validate_shuffles.py --worlds all --n-sh 99 --workers 8 --tag all_worlds
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import gzip  # noqa: E402
import json  # noqa: E402
import pathlib  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from concurrent.futures import ProcessPoolExecutor  # noqa: E402

import numpy as np  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import prep  # noqa: E402  (puts c6 and c6/checks on sys.path)
import harness as H  # noqa: E402
import knockout_regrow as K  # noqa: E402

REF = (HERE.parents[4] / "connectome-seed-data" / "knockout_regrow"
       / "flyvis65_20260925T171656Z_74de0401a21f" / "raw_fits.json.gz")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--worlds", default="R:0", help="comma list of <family>:<j>, or 'all'")
    ap.add_argument("--n-sh", type=int, default=99)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--row-chunk", type=int, default=25000)
    ap.add_argument("--worlds-per-batch", type=int, default=1)
    ap.add_argument("--tag", default="run")
    ap.add_argument("--base", action="store_true",
                    help="fit the worlds' own knockout views (keys world:<f>:<j>), not shuffles")
    a = ap.parse_args()

    t_all = time.time()
    terms = K.degree_terms()
    K._w_init(10, terms, True)                  # H.STARTS = 10, as the registered run's workers
    assert H.STARTS == 10
    import gpu_bf2                              # torch loads here, after the pool-free setup
    import torch

    ref = json.load(gzip.open(REF))
    if a.worlds == "all":
        worlds = [f"{w['family']}:{w['j']}" for w in K.world_specs()]
    else:
        worlds = a.worlds.split(",")
    batches = [worlds[i:i + a.worlds_per_batch] for i in range(0, len(worlds), a.worlds_per_batch)]

    rows, timing = [], []
    pool = ProcessPoolExecutor(max_workers=a.workers, initializer=prep.init_worker,
                               initargs=(terms,))
    try:
        for wb in batches:
            keys = ([f"world:{w}" for w in wb] if a.base
                    else [f"world:{w}|sh:{sd}" for w in wb for sd in range(a.n_sh)])
            torch.cuda.synchronize()
            t0 = time.time()
            preps = list(pool.map(prep.prepare_key, keys, chunksize=4))
            t_prep = time.time() - t0
            tr = {}
            for r in (1, 2, 3, 4):
                torch.cuda.synchronize()
                t1 = time.time()
                fits, _ = gpu_bf2.gpu_fit_bf_prepared(preps, r, row_chunk=a.row_chunk)
                torch.cuda.synchronize()
                tr[r] = time.time() - t1
                P = K._pred(f"BF:{r}")
                for key, pp, data in zip(keys, preps, fits):
                    rk = f"{key}||ko||BF:{r}"
                    refv = ref[rk]
                    dec = P.decode(data, K.BLOCK_CELLS)
                    p = np.asarray(dec["p_exist"], np.float64)
                    pr = np.asarray(refv["p"], np.float64)
                    y = np.asarray(refv["y"], bool)
                    a_g, a_r = K.auc(p, y), K.auc(pr, y)
                    rows.append({
                        "key": rk, "r": r,
                        "y_match": bool((pp["y_block"] == y).all()),
                        "lam_gpu": float(data["bf_lambda"][0]), "lam_ref": refv["lam"],
                        "auc_gpu": a_g, "auc_ref": a_r,
                        "auc_diff": (None if a_g is None or a_r is None else abs(a_g - a_r)),
                        "max_abs_p_diff": float(np.max(np.abs(p - pr))),
                        "p_bit_equal": bool(np.array_equal(p, pr)),
                        "label_mismatches": int(np.sum((p >= 0.5) != (pr >= 0.5))),
                        "ref_secs": refv["secs"]})
            timing.append({"worlds": wb, "n_banks": len(keys), "prep_secs": t_prep,
                           "gpu_secs_by_rank": tr, "gpu_secs": sum(tr.values())})
            sub = [x for x in rows if x["key"].split("||")[0].split("|")[0][6:] in wb]
            print(f"{','.join(wb)}: {len(keys)} banks; prep {t_prep:.1f}s; GPU "
                  + ", ".join(f"BF_{r} {tr[r]:.1f}s" for r in tr)
                  + f"; fits {len(sub)}, lam mismatches {sum(x['lam_gpu'] != x['lam_ref'] for x in sub)}"
                  + f", max|dp| {max(x['max_abs_p_diff'] for x in sub):.2e}"
                  + f", bit-equal {sum(x['p_bit_equal'] for x in sub)}", flush=True)
    finally:
        pool.shutdown()

    n = len(rows)
    diffs = [x["auc_diff"] for x in rows if x["auc_diff"] is not None]
    summary = {
        "fits": n,
        "y_mismatch_banks": sum(not x["y_match"] for x in rows),
        "lam_mismatches": sum(x["lam_gpu"] != x["lam_ref"] for x in rows),
        "p_bit_equal": sum(x["p_bit_equal"] for x in rows),
        "max_abs_p_diff": max(x["max_abs_p_diff"] for x in rows),
        "max_auc_diff": max(diffs) if diffs else None,
        "auc_none_both": sum(x["auc_gpu"] is None and x["auc_ref"] is None for x in rows),
        "label_mismatches": sum(x["label_mismatches"] for x in rows),
        "labels_total": 64 * n,
        "prep_secs": sum(t["prep_secs"] for t in timing),
        "gpu_secs": sum(t["gpu_secs"] for t in timing),
        "wall_secs_total": time.time() - t_all,
        "workers": a.workers, "row_chunk": a.row_chunk, "worlds_per_batch": a.worlds_per_batch,
        "cpu_ref_fit_secs_sum": sum(x["ref_secs"] for x in rows),
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
    }
    by_r = {}
    for r in (1, 2, 3, 4):
        rr = [x for x in rows if x["r"] == r]
        by_r[r] = {"fits": len(rr), "lam_mismatches": sum(x["lam_gpu"] != x["lam_ref"] for x in rr),
                   "p_bit_equal": sum(x["p_bit_equal"] for x in rr),
                   "max_abs_p_diff": max(x["max_abs_p_diff"] for x in rr),
                   "max_auc_diff": max((x["auc_diff"] for x in rr if x["auc_diff"] is not None),
                                       default=None),
                   "label_mismatches": sum(x["label_mismatches"] for x in rr)}
    summary["by_rank"] = by_r
    out = HERE / f"validation_shuffles_{a.tag}.json"
    out.write_text(json.dumps({"summary": summary, "timing": timing, "rows": rows}, indent=1))
    print(json.dumps(summary, indent=1))
    worst = sorted(rows, key=lambda x: -x["max_abs_p_diff"])[:10]
    for x in worst:
        print("worst:", x["key"], x["lam_gpu"], x["lam_ref"], f"{x['max_abs_p_diff']:.3e}",
              x["label_mismatches"], x["auc_diff"])


if __name__ == "__main__":
    main()
