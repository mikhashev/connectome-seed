#!/usr/bin/env python3
"""Does N1 alone separate the real bank from the 99 shuffled banks on existence?

Registered in docs/plans/2026-09-23-n1-alone-check-registration.md. Reuses harness.py's cv(),
N1, REAL, shuffled_bank(), FIELDS, LOWER_IS_BETTER, N_FOLDS, N_SHUFFLES.
"""
import csv
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
C6 = HERE.parent
ROOT = C6.parents[1]
OUT = HERE / "n1_alone"

sys.path.insert(0, str(C6))
import harness as H  # noqa: E402


def git_head():
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                           text=True, check=True).stdout.strip()


def field_mean(scores, f):
    import numpy as np
    return float(np.mean([s[f] for s in scores]))


def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)

    fields = list(H.FIELDS)

    banks = [("real", 0, H.REAL)]
    for sd in range(H.N_SHUFFLES):
        b, inv = H.shuffled_bank(H.REAL, sd)
        assert inv["out_degrees_kept"] and inv["in_degrees_kept"], \
            f"shuffle {sd} did not preserve degree as expected"
        banks.append((f"shuffle{sd}", sd, b))

    rows = []
    per_bank_field_mean = {f: {} for f in fields}

    for bank_id, seed, bank in banks:
        scores = H.cv(H.N1, bank)
        row = {"bank": bank_id, "seed": seed, "kind": "real" if bank_id == "real" else "shuffle"}
        for f in fields:
            m = field_mean(scores, f)
            per_bank_field_mean[f][bank_id] = m
            row[f] = m
        for k in range(H.N_FOLDS):
            row[f"existence_fold{k}"] = scores[k]["existence"]
        rows.append(row)
        print(f"{bank_id}: existence={row['existence']:.5f} offset={row['offset']:.5f} "
              f"counts={row['counts']:.5f} sign={row['sign']:.5f}", flush=True)

    fieldnames = ["bank", "seed", "kind"] + fields + \
        [f"existence_fold{k}" for k in range(H.N_FOLDS)]
    with open(OUT / "per_shuffle.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    summary_fields = {}
    for f in fields:
        real_v = per_bank_field_mean[f]["real"]
        sh_v = [per_bank_field_mean[f][f"shuffle{sd}"] for sd in range(H.N_SHUFFLES)]
        lower_better = H.LOWER_IS_BETTER[f]
        n_ge = sum(1 for v in sh_v if (v <= real_v if lower_better else v >= real_v))
        p = (1 + n_ge) / (1 + H.N_SHUFFLES)
        summary_fields[f] = {
            "lower_is_better": lower_better,
            "real": real_v,
            "shuffled_min": float(min(sh_v)),
            "shuffled_mean": float(sum(sh_v) / len(sh_v)),
            "shuffled_max": float(max(sh_v)),
            "n_shuffled_ge_real": n_ge,
            "p_one_sided": p,
            "separates": n_ge == 0,
        }

    consistency = {"checked": False}
    hc_path = C6 / "harness_controls.json"
    if hc_path.exists():
        hc = json.loads(hc_path.read_text())
        cd = hc.get("control_d_shuffled_banks")
        if cd:
            def close(a, b, tol=1e-6):
                return abs(a - b) <= tol
            ex_sh = cd["N1_existence_logloss_shuffled_min_mean_max"]
            off_sh = cd["N1_offset_jaccard_shuffled_min_mean_max"]
            consistency = {
                "checked": True,
                "source": "results/genome/c6/harness_controls.json:control_d_shuffled_banks",
                "existence_real_matches": close(summary_fields["existence"]["real"],
                                                 cd["N1_existence_logloss_real"]),
                "existence_shuffled_min_mean_max_matches": (
                    close(summary_fields["existence"]["shuffled_min"], ex_sh[0]) and
                    close(summary_fields["existence"]["shuffled_mean"], ex_sh[1]) and
                    close(summary_fields["existence"]["shuffled_max"], ex_sh[2])),
                "offset_real_matches": close(summary_fields["offset"]["real"],
                                              cd["N1_offset_jaccard_real"]),
                "offset_shuffled_min_mean_max_matches": (
                    close(summary_fields["offset"]["shuffled_min"], off_sh[0]) and
                    close(summary_fields["offset"]["shuffled_mean"], off_sh[1]) and
                    close(summary_fields["offset"]["shuffled_max"], off_sh[2])),
            }
            consistency["all_match"] = all(
                v for k, v in consistency.items() if k.endswith("_matches"))
            print(f"consistency vs harness_controls.json: {consistency}", flush=True)

    verdict_existence = "N1 separates" if summary_fields["existence"]["separates"] \
        else "N1 does not separate"

    summary = {
        "question": "Does N1 alone separate the real bank from the 99 shuffled banks on "
                     "existence? (registered decision field; other fields descriptive only)",
        "registration": "docs/plans/2026-09-23-n1-alone-check-registration.md",
        "decision_field": "existence",
        "verdict_existence": verdict_existence,
        "fields": summary_fields,
        "n_shuffles": H.N_SHUFFLES,
        "n_folds": H.N_FOLDS,
        "git_head": git_head(),
        "harness_sha256_lf": H.sha256_lf(C6 / "harness.py"),
        "folds_sha256_lf": H.sha256_lf(C6 / "folds.csv"),
        "consistency_check_vs_harness_controls_json": consistency,
        "runtime_s": time.time() - t0,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    print(f"done in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
