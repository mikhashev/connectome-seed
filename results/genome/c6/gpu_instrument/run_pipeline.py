"""The streamed pipeline (engine v3): prepare everything first, then stream it to the GPU.

  1. prep: every bank (45 worlds x 99 shuffles, and with --base the 45 worlds' own knockout
     views) is built and prepared in a process pool (prep.prepare_key_compact: N1 fits, grids,
     held-out masks, one SVD start per grid);
  2. GPU: all grids are uploaded once (gpu_bf3.GridStore); BF_1..BF_4 run back to back over all
     banks, each rank as one stream of large row chunks (inner fits -> held-out log-lik on the
     GPU -> lambda -> final fits), with no per-bank host loop;
  3. decode/compare: each rank's fits go to the same pool as soon as that rank is done
     (prep.decode_compare: the harness's own decode, compared with the registered store's
     entries, which the main process passes in), overlapping the next rank's GPU work.

Reference (read-only): connectome-seed-data/knockout_regrow/flyvis65_20260925T171656Z_74de0401a21f/
raw_fits.json.gz (synthetic fits only). Real block: never read, fit or scored.

It samples nvidia-smi (utilization, memory) every 500 ms and the system's used RAM every 1 s,
and reports them per phase.

Usage:
  python run_pipeline.py --worlds all --n-sh 99 --base --workers 24 --tag all45
  python run_pipeline.py --worlds R:0 --n-sh 99 --workers 24 --tag one_world
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import gzip  # noqa: E402
import json  # noqa: E402
import pathlib  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
import threading  # noqa: E402
import time  # noqa: E402
from concurrent.futures import ProcessPoolExecutor  # noqa: E402

import numpy as np  # noqa: E402
import psutil  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import prep  # noqa: E402
import harness as H  # noqa: E402
import knockout_regrow as K  # noqa: E402

REF = (HERE.parents[4] / "connectome-seed-data" / "knockout_regrow"
       / "flyvis65_20260925T171656Z_74de0401a21f" / "raw_fits.json.gz")


class RamSampler(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.base = psutil.virtual_memory().used
        self.samples = []
        self.stop = False

    def run(self):
        while not self.stop:
            self.samples.append((time.time(), psutil.virtual_memory().used - self.base))
            time.sleep(1.0)


def phase_stats(gpu_samples, t0, t1):
    u = [s[1] for s in gpu_samples if t0 <= s[0] <= t1]
    m = [s[2] for s in gpu_samples if t0 <= s[0] <= t1]
    if not u:
        return None
    u = np.array(u, float)
    return {"n_samples": len(u), "util_mean": float(u.mean()), "util_median": float(np.median(u)),
            "share_below_20pct": float(np.mean(u < 20)), "share_at_least_90pct": float(np.mean(u >= 90)),
            "mem_used_max_mib": float(max(m))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--worlds", default="all")
    ap.add_argument("--n-sh", type=int, default=99)
    ap.add_argument("--base", action="store_true")
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--row-chunk", type=int, default=40000)
    ap.add_argument("--tag", default="run")
    a = ap.parse_args()

    smi_path = HERE / f"pipeline_{a.tag}_nvsmi.csv"
    smi = subprocess.Popen(["nvidia-smi", "--query-gpu=utilization.gpu,memory.used",
                            "--format=csv,noheader,nounits", "-lms", "500"],
                           stdout=subprocess.PIPE, text=True)
    gpu_samples = []

    def read_smi():
        for line in smi.stdout:
            try:
                u, m = (float(x) for x in line.strip().split(","))
                gpu_samples.append((time.time(), u, m))
            except ValueError:
                pass
    threading.Thread(target=read_smi, daemon=True).start()
    ram = RamSampler()
    ram.start()

    t_start = time.time()
    terms = K.degree_terms()
    K._w_init(10, terms, True)
    assert H.STARTS == 10
    import torch
    import gpu_bf3

    worlds = ([f"{w['family']}:{w['j']}" for w in K.world_specs()] if a.worlds == "all"
              else a.worlds.split(","))
    keys = [f"world:{w}|sh:{sd}" for w in worlds for sd in range(a.n_sh)]
    if a.base:
        keys += [f"world:{w}" for w in worlds]
    ref = json.load(gzip.open(REF))
    marks = {}

    pool = ProcessPoolExecutor(max_workers=a.workers, initializer=prep.init_rule_worker,
                               initargs=(terms,))
    try:
        list(pool.map(int, range(a.workers)))                  # start the workers
        marks["prep_start"] = time.time()
        preps = list(pool.map(prep.prepare_key_compact, keys, chunksize=8))
        marks["prep_end"] = time.time()
        prep_bytes = sum(sum(v.nbytes for v in pp.values() if isinstance(v, np.ndarray))
                         for pp in preps)
        n_folds = preps[0]["n_folds"]

        torch.cuda.synchronize()
        marks["upload_start"] = time.time()
        S = gpu_bf3.GridStore(preps)
        torch.cuda.synchronize()
        marks["gpu_start"] = time.time()
        futs, rank_secs, near_ties = [], {}, {}
        for r in (1, 2, 3, 4):
            t1 = time.time()
            lam, U, V, ll, near = gpu_bf3.fit_bf_all(S, n_folds, r, row_chunk=a.row_chunk)
            torch.cuda.synchronize()
            rank_secs[r] = time.time() - t1
            near_ties[r] = near
            by_world = {}
            for i, (key, pp) in enumerate(zip(keys, preps)):
                data = dict(pp["n1"])
                data.update({"bf_U": U[i], "bf_V": V[i], "bf_lambda": np.array([float(lam[i])])})
                by_world.setdefault(key.split("|")[0], []).append(
                    (key, data, ref[f"{key}||ko||BF:{r}"], pp["y_block"]))
            futs += [pool.submit(prep.decode_compare, (r, items)) for items in by_world.values()]
            print(f"BF_{r}: {len(keys)} banks in {rank_secs[r]:.1f}s (near-ties {near})", flush=True)
        marks["gpu_end"] = time.time()
        rows = [x for f in futs for x in f.result()]
        marks["decode_end"] = time.time()
        vram_peak = torch.cuda.max_memory_allocated() / 2 ** 20
    finally:
        pool.shutdown()
        ram.stop = True
        smi.terminate()
    t_end = time.time()

    n = len(rows)
    diffs = [x["auc_diff"] for x in rows if x["auc_diff"] is not None]
    summary = {
        "banks": len(keys), "fits": n,
        "y_mismatch": sum(not x["y_match"] for x in rows),
        "lam_mismatches": sum(x["lam_gpu"] != x["lam_ref"] for x in rows),
        "p_bit_equal": sum(x["p_bit_equal"] for x in rows),
        "max_abs_p_diff": max(x["max_abs_p_diff"] for x in rows),
        "max_auc_diff": max(diffs) if diffs else None,
        "label_mismatches": sum(x["label_mismatches"] for x in rows), "labels_total": 64 * n,
        "near_ties_by_rank": near_ties,
        "secs": {"setup_before_prep": marks["prep_start"] - t_start,
                 "prep": marks["prep_end"] - marks["prep_start"],
                 "upload": marks["gpu_start"] - marks["upload_start"],
                 "gpu_ranks": rank_secs, "gpu_total": marks["gpu_end"] - marks["gpu_start"],
                 "decode_tail_after_gpu": marks["decode_end"] - marks["gpu_end"],
                 "prep_to_last_decode": marks["decode_end"] - marks["prep_start"],
                 "end_to_end_wall": t_end - t_start},
        "cpu_ref_fit_secs_sum": sum(x["ref_secs"] for x in rows),
        "prep_arrays_mib": prep_bytes / 2 ** 20,
        "ram_used_increase_peak_mib": max(s[1] for s in ram.samples) / 2 ** 20,
        "main_peak_wset_mib": getattr(psutil.Process().memory_info(), "peak_wset", 0) / 2 ** 20,
        "vram_torch_peak_alloc_mib": vram_peak,
        "gpu_util": {"prep": phase_stats(gpu_samples, marks["prep_start"], marks["prep_end"]),
                     "gpu": phase_stats(gpu_samples, marks["gpu_start"], marks["gpu_end"]),
                     "decode_tail": phase_stats(gpu_samples, marks["gpu_end"], marks["decode_end"])},
        "workers": a.workers, "row_chunk": a.row_chunk,
        "gpu_name": torch.cuda.get_device_name(0)}
    by_r = {}
    for r in (1, 2, 3, 4):
        rr = [x for x in rows if x["r"] == r]
        by_r[r] = {"fits": len(rr), "lam_mismatches": sum(x["lam_gpu"] != x["lam_ref"] for x in rr),
                   "p_bit_equal": sum(x["p_bit_equal"] for x in rr),
                   "max_abs_p_diff": max(x["max_abs_p_diff"] for x in rr),
                   "label_mismatches": sum(x["label_mismatches"] for x in rr)}
    summary["by_rank"] = by_r
    with open(smi_path, "w") as fh:
        fh.write("t_rel,util,mem_mib\n")
        for t, u, m in gpu_samples:
            fh.write(f"{t - t_start:.2f},{u:.0f},{m:.0f}\n")
    out = HERE / f"validation_pipeline_{a.tag}.json"
    out.write_text(json.dumps({"summary": summary, "marks_rel": {k: v - t_start for k, v in
                                                                  marks.items()}, "rows": rows},
                              indent=1))
    print(json.dumps(summary, indent=1))
    for x in sorted(rows, key=lambda x: -x["max_abs_p_diff"])[:8]:
        print("worst:", x["key"], x["lam_gpu"], x["lam_ref"], f"{x['max_abs_p_diff']:.3e}",
              x["label_mismatches"], x["auc_diff"])


if __name__ == "__main__":
    main()
