#!/usr/bin/env python3
"""
Window-integral cheap statistic — computation for
docs/briefs/2026-09-17-window-integral-cheap-statistic.md (v1.1).

Computes exactly the quantities that brief's section 5 pre-registers, from the
stored run jsons listed in its section 2, plus section 5's v1.1 additions
(shifted-window rank stability, 703's onset calibration, the named 0.5x
within-seed-spread factor). CPU only, reads only.

Do-not (brief section 6, unchanged by v1.1): no GPU, no writes to
connectome-seed-data, no change to docs/preregistration-cheap-vs-expensive.md,
no ---rho reported as a test/p-value/reject-accept decision, no numeric gate
built from a single run, no promotion of the window statistic to a registered
rung.

Spearman rho: Pearson correlation of midranks (ties averaged), the same
construction as docs/prereg-scripts/rho_ci.py's spearman(), reproduced here in
pure stdlib for the same reason that script gives (no numpy/scipy dependency
on the numbers that get written into a brief).

Run:
    C:/Users/mikha/AppData/Local/Programs/Python/Python312/python.exe window_integral.py
Writes window_readings.json next to this script.
"""
import hashlib
import json
import math
import statistics
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]  # results/diagnostics/window -> repo root

ONSET_LEVEL = 1200.0
CKPT_INTERVAL = 3600  # nominal spacing of the checkpoint grid (offset +12 in practice)

# ---------------------------------------------------------------------------
# Section 2 of the brief: exactly these files, exactly these roles.
# ---------------------------------------------------------------------------
INDIVIDUALS = {
    0: "results/night1/night1_9991-000.slim.json",
    1: "results/night2/night2_9991-001.slim.json",
    2: "results/night2/night2b_9991-002.slim.json",
    3: "results/night3/night3_9991-003.slim.json",
    4: "results/night3/night3_9991-004.slim.json",
    5: "results/night4/night4_9991-005.slim.json",
}
REPLICATES = {
    "0prime": "results/night1/rep_9991-900.slim.json",  # seed 0 replicate
    "3prime": "results/night4/rep_9991-903.slim.json",  # seed 3 replicate
}
DIAGNOSTIC_703 = "results/diagnostics/c3/partA/jitter_9991-703.json"

# Deviation from the brief's section 2 wording, recorded here and in the README:
# the brief names these files "night1_9991-000.json" etc.; on disk (this repo,
# read-only for this script) they exist only as "*.slim.json" with the same base
# name. Read as the same run record; no other file with the bare ".json" name
# and this content exists in the repository.

# Checkpoint-grid windows (brief section 4(A) and section 5's v1.1 addition).
WINDOWS = {
    "A_narrow_20k_30k": [21612, 25212, 28812],
    "A_wide_18012_32412": [18012, 21612, 25212, 28812, 32412],
    "W1_18012_25212": [18012, 21612, 25212],
    "W2_21612_28812": [21612, 25212, 28812],  # identical set to A_narrow, named per Ark's spec
    "W3_25212_32412": [25212, 28812, 32412],
}


def load(path):
    return json.loads((REPO_ROOT / path).read_text(encoding="utf-8"))


def rung_map(doc):
    """iteration -> val_loss, from rung_metrics (the evaluation-hook reads)."""
    return {r["iteration"]: r["val_loss"] for r in doc["rung_metrics"]}


def ckpt_map(doc):
    """iteration -> val_loss, from checkpoint_metrics (the checkpoint-grid reads)."""
    return {c["iteration"]: c["val_loss"] for c in doc["checkpoint_metrics"]}


def window_mean(cmap, iters):
    """Mean of cmap[i] for i in iters that are actually present. Returns
    (mean_or_None, used_iterations, missing_iterations)."""
    used = [i for i in iters if i in cmap]
    missing = [i for i in iters if i not in cmap]
    if not used:
        return None, used, missing
    return statistics.fmean(cmap[i] for i in used), used, missing


def onset_crossing(points, level=ONSET_LEVEL):
    """points: list of (iteration, val_loss) sorted or not. Returns
    (onset_iteration_or_None, bracket_or_None) for the FIRST downward crossing
    of `level` (val >= level at bracket[0], val < level at bracket[1]), by
    linear interpolation between the two bracketing points."""
    pts = sorted(points, key=lambda p: p[0])
    for (i0, v0), (i1, v1) in zip(pts, pts[1:]):
        if v0 >= level > v1:
            frac = (v0 - level) / (v0 - v1)
            return i0 + frac * (i1 - i0), (i0, i1)
    return None, None


def midranks(values):
    """Ranks, ascending (rank 1 = smallest value = lowest loss), ties averaged.
    Same construction as docs/prereg-scripts/rho_ci.py:midranks."""
    n = len(values)
    order = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def pearson(xs, ys):
    n = len(xs)
    mx = statistics.fmean(xs)
    my = statistics.fmean(ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 0.0 or syy <= 0.0:
        return None
    return sxy / math.sqrt(sxx * syy)


def spearman(a, b):
    if len(a) != len(b) or len(a) < 3:
        return None
    return pearson(midranks(a), midranks(b))


def sample_sd(values):
    """Sample standard deviation (n-1 denominator). n=2: |x1-x2|/sqrt(2)."""
    if len(values) < 2:
        return None
    return statistics.stdev(values)


def main():
    script_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out = {
        "script_sha256_note": "hash of this script BEFORE this run appended it below "
        "(computed pre-write; the written window_readings.json necessarily postdates it)",
        "script_sha256": script_sha256,
        "windows": WINDOWS,
        "onset_level": ONSET_LEVEL,
        "ckpt_interval": CKPT_INTERVAL,
    }

    # ---- load everything -------------------------------------------------
    docs = {}
    for seed, path in INDIVIDUALS.items():
        docs[f"seed{seed}"] = load(path)
    for tag, path in REPLICATES.items():
        docs[tag] = load(path)
    docs["703"] = load(DIAGNOSTIC_703)

    rungs = {k: rung_map(d) for k, d in docs.items()}
    ckpts = {k: ckpt_map(d) for k, d in docs.items()}

    run_keys = list(INDIVIDUALS.keys())
    run_keys_str = [f"seed{s}" for s in run_keys]
    all_keys = run_keys_str + ["0prime", "3prime", "703"]

    # ---- per-run table -----------------------------------------------------
    per_run = {}
    for k in all_keys:
        rm = rungs[k]
        cm = ckpts[k]
        entry = {
            "point_25000_hook": rm.get(25000),
            "point_250000_hook": rm.get(250000),  # None for 703
            "checkpoints_in_window": {},
            "window_means": {},
        }
        for wname, iters in WINDOWS.items():
            mean, used, missing = window_mean(cm, iters)
            entry["window_means"][wname] = {
                "mean": mean,
                "used_iterations": used,
                "missing_iterations": missing,
                "n_points": len(used),
            }
        # onset estimate: 703 from dense rung_metrics; the 7 full runs from
        # checkpoint_metrics by linear interpolation (brief section 5, (C)).
        if k == "703":
            pts = list(rm.items())
            onset_iter, bracket = onset_crossing(pts)
            entry["onset_estimate"] = {
                "iteration": onset_iter,
                "bracket": bracket,
                "source": "dense rung_metrics (1000-26000)",
            }
        else:
            pts = list(cm.items())
            onset_iter, bracket = onset_crossing(pts)
            entry["onset_estimate"] = {
                "iteration": onset_iter,
                "bracket": bracket,
                "source": "checkpoint_metrics (linear interpolation)",
            }
        per_run[k] = entry
    out["per_run"] = per_run

    # ---- 703 onset calibration (section 5, v1.1, Ark) ----------------------
    dense_onset, dense_bracket = onset_crossing(list(rungs["703"].items()))
    subsample_onset, subsample_bracket = onset_crossing(list(ckpts["703"].items()))
    diff = None
    if dense_onset is not None and subsample_onset is not None:
        diff = subsample_onset - dense_onset
    reliable = None
    if diff is not None:
        reliable = abs(diff) <= CKPT_INTERVAL
    out["run703_onset_calibration"] = {
        "dense_onset_iteration": dense_onset,
        "dense_bracket": dense_bracket,
        "checkpoint_subsample_onset_iteration": subsample_onset,
        "checkpoint_subsample_bracket": subsample_bracket,
        "difference_subsample_minus_dense": diff,
        "one_checkpoint_interval": CKPT_INTERVAL,
        "onset_estimate_on_seven_full_runs_reliable": reliable,
    }

    # ---- within-seed vs individual spread (section 5, and v1.1 0.5x factor) -
    def stat_values(keys, statname):
        vals = []
        for k in keys:
            if statname == "point_25000_hook":
                vals.append(per_run[k]["point_25000_hook"])
            else:
                vals.append(per_run[k]["window_means"][statname]["mean"])
        return vals

    stat_names = ["point_25000_hook"] + list(WINDOWS.keys())
    within_seed = {}
    for statname in stat_names:
        # seed 0 pair: always both full runs, no missing-data issue.
        seed0_vals = stat_values(["seed0", "0prime"], statname)
        seed0_sd = sample_sd(seed0_vals) if None not in seed0_vals else None

        # seed 3 trio, "both ways" when 703 has an incomplete window (brief
        # section 4(A): "report both ways if 703 is included at all").
        trio_keys = ["seed3", "3prime", "703"]
        trio_vals_incl = stat_values(trio_keys, statname)
        trio_sd_incl = sample_sd(trio_vals_incl) if None not in trio_vals_incl else None
        pair_keys = ["seed3", "3prime"]
        pair_vals_excl = stat_values(pair_keys, statname)
        pair_sd_excl = sample_sd(pair_vals_excl) if None not in pair_vals_excl else None

        # individuals n=6
        indiv_vals = stat_values(run_keys_str, statname)
        indiv_sd = sample_sd(indiv_vals) if None not in indiv_vals else None

        within_seed[statname] = {
            "seed0_pair_values": seed0_vals,
            "seed0_pair_sd": seed0_sd,
            "seed3_trio_values_703_included": trio_vals_incl,
            "seed3_trio_sd_703_included": trio_sd_incl,
            "seed3_pair_values_703_excluded": pair_vals_excl,
            "seed3_pair_sd_703_excluded": pair_sd_excl,
            "individuals_n6_values": indiv_vals,
            "individuals_n6_sd": indiv_sd,
        }
        # 0.5x factor, section 5 v1.1 (Ark): condition (i) needs sd(window) <=
        # 0.5 * sd(point) for BOTH the seed-0 pair and the seed-3 set. Applied
        # to every statname including "point_25000_hook" itself for reference
        # (ratio 1.0 there by construction).
        pt = within_seed["point_25000_hook"]
        ratio_seed0 = (seed0_sd / pt["seed0_pair_sd"]) if (seed0_sd is not None and pt["seed0_pair_sd"]) else None
        ratio_seed3_incl = (
            trio_sd_incl / pt["seed3_trio_sd_703_included"]
            if (trio_sd_incl is not None and pt["seed3_trio_sd_703_included"])
            else None
        )
        ratio_seed3_excl = (
            pair_sd_excl / pt["seed3_pair_sd_703_excluded"]
            if (pair_sd_excl is not None and pt["seed3_pair_sd_703_excluded"])
            else None
        )
        within_seed[statname]["ratio_to_point_seed0"] = ratio_seed0
        within_seed[statname]["ratio_to_point_seed3_703_included"] = ratio_seed3_incl
        within_seed[statname]["ratio_to_point_seed3_703_excluded"] = ratio_seed3_excl
        within_seed[statname]["clears_0.5x_seed0"] = (
            ratio_seed0 <= 0.5 if ratio_seed0 is not None else None
        )
        within_seed[statname]["clears_0.5x_seed3_703_included"] = (
            ratio_seed3_incl <= 0.5 if ratio_seed3_incl is not None else None
        )
        within_seed[statname]["clears_0.5x_seed3_703_excluded"] = (
            ratio_seed3_excl <= 0.5 if ratio_seed3_excl is not None else None
        )
    out["within_seed_spread"] = within_seed

    # ---- rank stability across shifted windows, n=6 individuals (section 5,
    # v1.1, Ark) -------------------------------------------------------------
    shift_names = ["W1_18012_25212", "W2_21612_28812", "W3_25212_32412"]
    shift_values = {
        w: [per_run[k]["window_means"][w]["mean"] for k in run_keys_str] for w in shift_names
    }
    shift_ranks = {w: midranks(shift_values[w]) for w in shift_names}
    pairwise_rho = {}
    for i in range(len(shift_names)):
        for j in range(i + 1, len(shift_names)):
            a, b = shift_names[i], shift_names[j]
            pairwise_rho[f"{a}__vs__{b}"] = spearman(shift_values[a], shift_values[b])
    out["rank_stability_shifted_windows"] = {
        "individuals_seed_order": run_keys,
        "values": shift_values,
        "midranks": shift_ranks,
        "pairwise_spearman_rho": pairwise_rho,
        "n": len(run_keys_str),
        "critical_rho_n6_prereg_table": 0.829,
    }

    # ---- rho with the 250,000 hook, point and each window (section 5) ------
    target_250k = [per_run[k]["point_250000_hook"] for k in run_keys_str]
    rho_vs_top = {}
    point_25k = [per_run[k]["point_25000_hook"] for k in run_keys_str]
    rho_vs_top["point_25000_hook"] = spearman(point_25k, target_250k)
    for wname in WINDOWS:
        wv = [per_run[k]["window_means"][wname]["mean"] for k in run_keys_str]
        rho_vs_top[wname] = spearman(wv, target_250k) if None not in wv else None
    out["rho_with_250000_hook"] = {
        "n": len(run_keys_str),
        "target_250000_hook_values": target_250k,
        "critical_rho_n6_prereg_table": 0.829,
        "rho_by_statistic": rho_vs_top,
    }

    # ---- promotion criterion, applied exactly as section 5 fixes it (with
    # v1.1's 0.5x factor and using the 703-included trio numbers where a full
    # window is not available for 703, reported alongside the excluded-pair
    # alternative computed above) ------------------------------------------
    promotion = {}
    for wname in WINDOWS:
        ws = within_seed[wname]
        cond_i_incl = ws["clears_0.5x_seed0"] and ws["clears_0.5x_seed3_703_included"]
        cond_i_excl = ws["clears_0.5x_seed0"] and ws["clears_0.5x_seed3_703_excluded"]
        rho_w = rho_vs_top[wname]
        rho_pt = rho_vs_top["point_25000_hook"]
        cond_ii = (rho_w is not None and rho_pt is not None and rho_w >= rho_pt)
        promotion[wname] = {
            "condition_i_both_seed_sets_0.5x_703_included": cond_i_incl,
            "condition_i_both_seed_sets_0.5x_703_excluded_pair": cond_i_excl,
            "condition_ii_rho_not_lower_than_point": cond_ii,
            "rho_window": rho_w,
            "rho_point": rho_pt,
        }
    out["promotion_criterion"] = promotion

    # ---- (B) train-loss window mean (section 4(B)/5) -----------------------
    # Deviation from the brief's section 2, recorded here: `train_loss_per_iter`
    # exists in the stored json only for 703 (25,212 entries, index i = training
    # iteration i). It does NOT exist in the 7 full-run *.slim.json files; those
    # carry only `train_loss_last1000_*.csv`, the final 1,000 iterations
    # (~iteration 249,009-250,008), nowhere near the 18k-32k window. (B) is
    # therefore computed here for 703 only; for the other 7 it is reported as
    # not available at this window, not silently skipped.
    b_train_loss = {}
    tlpi = docs["703"].get("train_loss_per_iter")
    n_tlpi = len(tlpi) if tlpi else 0
    for wname, iters in WINDOWS.items():
        lo, hi = min(iters), max(iters)
        idx_hi = min(hi, n_tlpi - 1)
        if tlpi and lo <= idx_hi:
            window_slice = tlpi[lo : idx_hi + 1]
            b_train_loss[wname] = {
                "mean": statistics.fmean(window_slice),
                "sd": statistics.stdev(window_slice) if len(window_slice) > 1 else None,
                "n_iterations_used": len(window_slice),
                "requested_range": [lo, hi],
                "available_range_of_train_loss_per_iter": [0, n_tlpi - 1],
                "note": "hi clipped to available range" if idx_hi < hi else None,
            }
        else:
            b_train_loss[wname] = {"mean": None, "note": "window entirely outside available range"}
    out["option_B_train_loss_window_mean_703_only"] = {
        "available_for": ["703"],
        "not_available_for": run_keys_str + ["0prime", "3prime"],
        "not_available_reason": (
            "train_loss_per_iter is absent from the 7 full-run *.slim.json files; "
            "they carry only the final 1000 iterations (train_loss_last1000_*.csv), "
            "which does not cover the 18012-32412 window"
        ),
        "by_window": b_train_loss,
    }

    out["deviations_from_brief"] = [
        "Section 2 names the full-run files 'night1_9991-000.json' etc.; on disk in this "
        "repository they exist only as '*.slim.json' with the same base name (e.g. "
        "'night1_9991-000.slim.json'). Read as the same run record; no bare '.json' file "
        "with this content exists.",
        "Section 2 states train_loss_per_iter 'exists for all 8'. On disk it exists only "
        "for 703; the 7 full runs have only train_loss_last1000_*.csv (final 1000 "
        "iterations). Option (B) is therefore computed for 703 only (see "
        "option_B_train_loss_window_mean_703_only); reported here rather than silently "
        "matching the brief's wording.",
    ]

    # ---- write ---------------------------------------------------------
    out_path = SCRIPT_DIR / "window_readings.json"
    out_path.write_text(json.dumps(out, indent=2, sort_keys=False), encoding="utf-8")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
