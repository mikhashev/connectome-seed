"""Validate gpu_bf.gpu_fit_bf_many (cross-fit batched: many worlds x one rank, one GPU call for
fold-selection, one for the final fit) against raw_fits.json.gz for all 45 synthetic worlds x
BF_1..BF_4 on the knockout ('ko') arm, and measure the batched wall time.

Real block: never read. knockout_regrow.py: never run as a script (only its data/world functions
are imported, which live outside __main__).
"""
import gzip
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

REF = (HERE.parents[4] / "connectome-seed-data" / "knockout_regrow" / "synthetic_rev3_prerun"
       / "raw_fits.json.gz")


def auc(p, y):
    p, y = np.asarray(p), np.asarray(y, bool)
    pos, neg = p[y], p[~y]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    greater = (pos[:, None] > neg[None, :]).sum()
    ties = (pos[:, None] == neg[None, :]).sum()
    return float((greater + 0.5 * ties) / (len(pos) * len(neg)))


def main():
    ref = json.load(gzip.open(REF))
    terms = K.degree_terms()
    specs = K.world_specs()
    banks = [K.make_world(spec, terms) for spec in specs]
    views = [H.make_view(b, K.MASKS["ko"]) for b in banks]

    rows = []
    t_total = 0.0
    for r in (1, 2, 3, 4):
        t0 = time.time()
        n1s = gpu_bf.gpu_fit_bf_many(views, r)
        secs = time.time() - t0
        t_total += secs
        print(f"rank {r}: {len(views)} worlds fitted in one batched call, {secs:.2f}s", flush=True)
        for spec, n1 in zip(specs, n1s):
            ref_key = f"world:{spec['family']}:{spec['j']}||ko||BF:{r}"
            if ref_key not in ref:
                continue
            refv = ref[ref_key]
            p = gpu_bf.p_exist_on_block_cells(n1)
            y = np.asarray(refv["y"], bool)
            p_ref = np.asarray(refv["p"])
            lam_gpu = float(n1["bf_lambda"][0])
            lam_ref = float(refv["lam"])
            row = {
                "family": spec["family"], "seed": spec["seed"], "r": r,
                "lam_gpu": lam_gpu, "lam_ref": lam_ref, "lam_match": lam_gpu == lam_ref,
                "auc_gpu": auc(p, y), "auc_ref": auc(p_ref, y),
                "max_abs_p_diff": float(np.max(np.abs(p - p_ref))),
                "label_mismatches": int(np.sum((p >= 0.5) != (p_ref >= 0.5))),
            }
            row["auc_diff"] = abs(row["auc_gpu"] - row["auc_ref"])
            rows.append(row)

    out = HERE / "validation_batched_results.json"
    out.write_text(json.dumps({"rows": rows, "batched_total_secs": t_total}, indent=2))

    n = len(rows)
    lam_mismatches = [r for r in rows if not r["lam_match"]]
    max_auc_diff = max((r["auc_diff"] for r in rows), default=float("nan"))
    max_p_diff = max((r["max_abs_p_diff"] for r in rows), default=float("nan"))
    total_label_mismatches = sum(r["label_mismatches"] for r in rows)
    print("\n==== BATCHED SUMMARY (45 worlds x 4 ranks, vs raw_fits.json.gz) ====")
    print(f"fits compared: {n}")
    print(f"lambda mismatches: {len(lam_mismatches)}")
    for row in lam_mismatches:
        print("  ", row["family"], row["seed"], row["r"], row["lam_gpu"], "vs", row["lam_ref"])
    print(f"max |AUC diff|: {max_auc_diff:.3g}")
    print(f"max |p diff|: {max_p_diff:.3g}")
    print(f"total label mismatches (of {n*64}): {total_label_mismatches}")
    print(f"TOTAL batched GPU wall time, all 45 worlds x 4 ranks: {t_total:.1f}s")


if __name__ == "__main__":
    main()
