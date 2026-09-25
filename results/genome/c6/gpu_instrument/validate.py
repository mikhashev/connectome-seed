"""Validate the GPU batched BF fitter against the registered CPU instrument's saved reference
outputs (45 synthetic worlds, knockout ('ko') arm, BF_1..BF_4).

Reads ONLY the pre-run reference file (read-only, treated as ground truth):
  connectome-seed-data/knockout_regrow/synthetic_rev3_prerun/raw_fits.json.gz

Never touches the real block. Never runs knockout_regrow.py.
"""
import gzip
import json
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "results" / "genome" / "c6"))
sys.path.insert(0, str(ROOT / "results" / "genome" / "c6" / "checks"))

import harness as H
import knockout_regrow as K
import gpu_bf

REF = (ROOT.parent / "connectome-seed-data" / "knockout_regrow" / "synthetic_rev3_prerun"
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
    terms = K.degree_terms()   # N1 fit on the REAL KNOCKOUT view only (no block cells) -- the
                                # synthetic worlds' own construction step, per registration 3.6
    specs = K.world_specs()

    rows = []
    t0 = time.time()
    for spec in specs:
        bank = K.make_world(spec, terms)
        view = H.make_view(bank, K.MASKS["ko"])
        key_prefix = f"world:{spec['family']}:{spec['j']}||ko||"
        for r in (1, 2, 3, 4):
            ref_key = key_prefix + f"BF:{r}"
            if ref_key not in ref:
                continue
            refv = ref[ref_key]
            t1 = time.time()
            n1 = gpu_bf.gpu_fit_bf(view, r)
            secs = time.time() - t1
            p = gpu_bf.p_exist_on_block_cells(n1)
            y = np.asarray(refv["y"], bool)
            lam_gpu = float(n1["bf_lambda"][0])
            lam_ref = float(refv["lam"])
            p_ref = np.asarray(refv["p"])
            auc_gpu = auc(p, y)
            auc_ref = auc(p_ref, y)
            labels_gpu = p >= 0.5
            labels_ref = p_ref >= 0.5
            rows.append({
                "family": spec["family"], "seed": spec["seed"], "r": r,
                "lam_gpu": lam_gpu, "lam_ref": lam_ref, "lam_match": lam_gpu == lam_ref,
                "auc_gpu": auc_gpu, "auc_ref": auc_ref, "auc_diff": abs(auc_gpu - auc_ref),
                "max_abs_p_diff": float(np.max(np.abs(p - p_ref))),
                "label_mismatches": int(np.sum(labels_gpu != labels_ref)),
                "secs_gpu": secs,
            })
            print(rows[-1], flush=True)
    total = time.time() - t0

    out = HERE / "validation_results.json"
    out.write_text(json.dumps({"rows": rows, "total_secs": total}, indent=2))

    n = len(rows)
    lam_mismatches = [r for r in rows if not r["lam_match"]]
    max_auc_diff = max((r["auc_diff"] for r in rows), default=float("nan"))
    max_p_diff = max((r["max_abs_p_diff"] for r in rows), default=float("nan"))
    total_label_mismatches = sum(r["label_mismatches"] for r in rows)
    print("\n==== SUMMARY ====")
    print(f"fits compared: {n}")
    print(f"lambda mismatches: {len(lam_mismatches)}")
    for r in lam_mismatches:
        print("  ", r["family"], r["seed"], r["r"], r["lam_gpu"], "vs", r["lam_ref"])
    print(f"max |AUC diff|: {max_auc_diff:.6g}")
    print(f"max |p diff|: {max_p_diff:.6g}")
    print(f"total label mismatches (of {n*64}): {total_label_mismatches}")
    print(f"total GPU wall time for {n} fit_bf calls: {total:.1f}s")


if __name__ == "__main__":
    main()
