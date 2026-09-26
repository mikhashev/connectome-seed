"""Validate the GPU batched BF fitter (engine v1) against the on-disk CPU harness (harness.fit_bf),
run fresh on the SAME synthetically-built worlds, in the same process.

Corrected 2026-09-26 (GPU instrument registration, ledger row G-(6)): this docstring used to call
connectome-seed-data/knockout_regrow/synthetic_rev3_prerun/raw_fits.json.gz "stale" and to say
that harness.fit_n1 "already disagrees with that file's stored N1 predictions". Both were wrong:
the store reproduces bit for bit; the claim came from a wrong key and a wrong cell order in the
comparison script (knockout-and-regrow registration, section 3.3, facts (a) and (c), and its
section 12, row CC (1); README.md, "v1: Validation"). This script remains what it was: a
file-free check of engine v1 against a live harness.fit_bf on the same inputs.

Real block: never read. This script only builds synthetic worlds (knockout_regrow.make_world) and
fits BF_1..BF_4 in the knockout ('ko') arm.
"""
import json
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / "checks"))

import harness as H
import knockout_regrow as K
import gpu_bf


def auc(p, y):
    p, y = np.asarray(p), np.asarray(y, bool)
    pos, neg = p[y], p[~y]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    greater = (pos[:, None] > neg[None, :]).sum()
    ties = (pos[:, None] == neg[None, :]).sum()
    return float((greater + 0.5 * ties) / (len(pos) * len(neg)))


def main(limit_worlds=None):
    terms = K.degree_terms()
    specs = K.world_specs()
    if limit_worlds:
        specs = specs[:limit_worlds]

    rows = []
    t_cpu_total = 0.0
    t_gpu_total = 0.0
    for spec in specs:
        bank = K.make_world(spec, terms)
        view = H.make_view(bank, K.MASKS["ko"])
        y = view.exists[K.BLOCK[view.cells[:, 0], view.cells[:, 1]]] if False else None
        y_block = bank.exists[K.BLOCK]
        for r in (1, 2, 3, 4):
            t0 = time.time()
            cpu_fit = H.fit_bf(view, r)
            t_cpu = time.time() - t0
            t0 = time.time()
            gpu_fit = gpu_bf.gpu_fit_bf(view, r)
            t_gpu = time.time() - t0
            t_cpu_total += t_cpu
            t_gpu_total += t_gpu

            p_cpu = gpu_bf.p_exist_on_block(cpu_fit)
            p_gpu = gpu_bf.p_exist_on_block(gpu_fit)
            lam_cpu = float(cpu_fit["bf_lambda"][0])
            lam_gpu = float(gpu_fit["bf_lambda"][0])
            row = {
                "family": spec["family"], "seed": spec["seed"], "r": r,
                "lam_cpu": lam_cpu, "lam_gpu": lam_gpu, "lam_match": lam_cpu == lam_gpu,
                "auc_cpu": auc(p_cpu, y_block), "auc_gpu": auc(p_gpu, y_block),
                "max_abs_p_diff": float(np.max(np.abs(p_cpu - p_gpu))),
                "label_mismatches": int(np.sum((p_cpu >= 0.5) != (p_gpu >= 0.5))),
                "secs_cpu": t_cpu, "secs_gpu": t_gpu,
            }
            row["auc_diff"] = abs(row["auc_cpu"] - row["auc_gpu"])
            rows.append(row)
            print(row, flush=True)

    out = HERE / "validation_vs_cpu_results.json"
    out.write_text(json.dumps({"rows": rows, "t_cpu_total": t_cpu_total,
                                "t_gpu_total": t_gpu_total}, indent=2))

    n = len(rows)
    lam_mismatches = [r for r in rows if not r["lam_match"]]
    max_auc_diff = max((r["auc_diff"] for r in rows), default=float("nan"))
    max_p_diff = max((r["max_abs_p_diff"] for r in rows), default=float("nan"))
    total_label_mismatches = sum(r["label_mismatches"] for r in rows)
    print("\n==== SUMMARY (GPU vs CURRENT CPU harness.fit_bf, same worlds) ====")
    print(f"fits compared: {n}")
    print(f"lambda mismatches: {len(lam_mismatches)}")
    for r in lam_mismatches:
        print("  ", r["family"], r["seed"], r["r"], r["lam_cpu"], "vs", r["lam_gpu"])
    print(f"max |AUC diff|: {max_auc_diff:.3g}")
    print(f"max |p diff|: {max_p_diff:.3g}")
    print(f"total label mismatches (of {n*64}): {total_label_mismatches}")
    print(f"CPU total: {t_cpu_total:.1f}s   GPU total: {t_gpu_total:.1f}s"
          f"   speedup: {t_cpu_total / max(t_gpu_total, 1e-9):.1f}x")


if __name__ == "__main__":
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    main(lim)
