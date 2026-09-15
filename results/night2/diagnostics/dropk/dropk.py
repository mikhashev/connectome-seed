#!/usr/bin/env python
"""
Ranking robustness to item composition (drop-k), proposed by Ark 2026-09-15 06:47,
recorded in docs/next-session-plan.md Section 4.

Reads (read-only):
    results/night2/diagnostics/per_item_250008.csv
    results/night2/diagnostics/per_item_25212.csv

Writes (this directory only):
    dropk_results.json
    dropk_summary.md

Pure stdlib, no GPU, no third-party deps.

Usage:
    python dropk.py
"""
import csv
import itertools
import json
import statistics
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DIAG_DIR = HERE.parent
RUNGS = {
    "250008": DIAG_DIR / "per_item_250008.csv",
    "25212": DIAG_DIR / "per_item_25212.csv",
}
SEEDS = ["seed0", "seed1", "seed2"]  # seed0prime handled separately (twin)


def scene_of(item: str) -> str:
    # item looks like "sequence_02_ambush_2_split_00" -> scene "sequence_02_ambush_2"
    return item.rsplit("_split_", 1)[0]


def load_rung(path: Path):
    items = []
    vals = {s: {} for s in SEEDS}
    twin_diff = {}
    with open(path, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            it = row["item"]
            items.append(it)
            for s in SEEDS:
                vals[s][it] = float(row[s])
            twin_diff[it] = float(row["seed0prime_minus_seed0"])
    return items, vals, twin_diff


def order_for_subset(items_subset, vals):
    """Return seeds sorted ascending by mean over items_subset (lower loss = better),
    as a tuple of seed-index ints, e.g. (1, 2, 0)."""
    means = {s: statistics.fmean(vals[s][it] for it in items_subset) for s in SEEDS}
    ordered = sorted(SEEDS, key=lambda s: means[s])
    return tuple(int(s.replace("seed", "")) for s in ordered), means


def order_label(order_tuple):
    return " < ".join(str(x) for x in order_tuple)


def kendall_tau_distance_3(order_a, order_b):
    """Number of pairwise-order disagreements between two total orders over 3 items."""
    pairs_a = {(order_a[i], order_a[j]) for i in range(len(order_a)) for j in range(i + 1, len(order_a))}
    pairs_b = {(order_b[i], order_b[j]) for i in range(len(order_b)) for j in range(i + 1, len(order_b))}
    return len(pairs_a - pairs_b)


def analyze_rung(rung_name, path):
    items, vals, twin_diff = load_rung(path)
    n_items = len(items)
    scenes = {}
    for it in items:
        scenes.setdefault(scene_of(it), []).append(it)
    scene_names = sorted(scenes.keys())

    out = {"rung": rung_name, "n_items": n_items, "scenes": {s: scenes[s] for s in scene_names}}

    # 1. Full-set order
    full_order, full_means = order_for_subset(items, vals)
    out["full_set"] = {
        "order": list(full_order),
        "order_label": order_label(full_order),
        "means": full_means,
    }
    full_best = full_order[0]

    # 2. Exhaustive drop-k for k=1,2,3
    dropk = {}
    for k in (1, 2, 3):
        n_subsets = 0
        n_preserve_exact = 0
        n_best_preserved = 0
        perm_counts = Counter()
        pairwise_wins = {"1_beats_0": 0, "2_beats_0": 0, "1_beats_2": 0}
        flips = []  # (dropped_items, order, tau_distance_from_full)
        for combo in itertools.combinations(items, k):
            dropped = set(combo)
            remaining = [it for it in items if it not in dropped]
            order, means = order_for_subset(remaining, vals)
            n_subsets += 1
            perm_counts[order_label(order)] += 1
            if order == full_order:
                n_preserve_exact += 1
            if order[0] == full_best:
                n_best_preserved += 1
            if means["seed1"] < means["seed0"]:
                pairwise_wins["1_beats_0"] += 1
            if means["seed2"] < means["seed0"]:
                pairwise_wins["2_beats_0"] += 1
            if means["seed1"] < means["seed2"]:
                pairwise_wins["1_beats_2"] += 1
            if order != full_order:
                tau = kendall_tau_distance_3(full_order, order)
                flips.append({"dropped": list(combo), "order": list(order), "order_label": order_label(order), "tau_distance": tau})

        entry = {
            "n_subsets": n_subsets,
            "frac_preserve_exact": n_preserve_exact / n_subsets,
            "frac_best_preserved": n_best_preserved / n_subsets,
            "order_distribution": dict(perm_counts),
            "pairwise_win_fractions": {k2: v / n_subsets for k2, v in pairwise_wins.items()},
        }

        if k == 1:
            # all 16, one per dropped item
            per_item = []
            for combo in itertools.combinations(items, 1):
                dropped_item = combo[0]
                remaining = [it for it in items if it != dropped_item]
                order, means = order_for_subset(remaining, vals)
                per_item.append({
                    "dropped": dropped_item,
                    "order": list(order),
                    "order_label": order_label(order),
                    "flips": order != full_order,
                })
            entry["all_16_drop_one"] = per_item
        if k == 3:
            flips_sorted = sorted(flips, key=lambda d: (-d["tau_distance"], d["dropped"]))
            entry["top_10_most_different_triples"] = flips_sorted[:10]
        if k == 2:
            # keep it lighter: just count of flipping pairs, not full 120-row dump
            entry["n_flipping_pairs"] = len(flips)

        dropk[str(k)] = entry
    out["dropk"] = dropk

    # 3. Scene-level drop: drop each scene entirely
    scene_drops = []
    for sc in scene_names:
        dropped_items = set(scenes[sc])
        remaining = [it for it in items if it not in dropped_items]
        order, means = order_for_subset(remaining, vals)
        scene_drops.append({
            "scene_dropped": sc,
            "n_items_dropped": len(dropped_items),
            "n_items_remaining": len(remaining),
            "order": list(order),
            "order_label": order_label(order),
            "flips": order != full_order,
        })
    out["scene_level_drop"] = scene_drops

    # 4. Twin sign robustness over drop-k subsets (k=1,2,3), using seed0prime_minus_seed0 column
    twin = {}
    for k in (1, 2, 3):
        n_subsets = 0
        n_pos = 0
        for combo in itertools.combinations(items, k):
            dropped = set(combo)
            remaining = [it for it in items if it not in dropped]
            m = statistics.fmean(twin_diff[it] for it in remaining)
            n_subsets += 1
            if m > 0:
                n_pos += 1
        twin[str(k)] = {"n_subsets": n_subsets, "frac_positive": n_pos / n_subsets}
    full_twin_mean = statistics.fmean(twin_diff[it] for it in items)
    out["twin_sign_robustness"] = {
        "full_set_mean_diff": full_twin_mean,
        "full_set_sign_positive": full_twin_mean > 0,
        "by_k": twin,
    }

    # 5. Per-item pairwise counts (no aggregation) over the full 16 items
    pairwise_counts = {
        "seed1_lt_seed0": sum(1 for it in items if vals["seed1"][it] < vals["seed0"][it]),
        "seed2_lt_seed0": sum(1 for it in items if vals["seed2"][it] < vals["seed0"][it]),
        "seed1_lt_seed2": sum(1 for it in items if vals["seed1"][it] < vals["seed2"][it]),
        "n_items": n_items,
    }
    out["per_item_pairwise_counts"] = pairwise_counts

    # 6. Leave-scene-in: order by each single scene alone
    leave_scene_in = []
    for sc in scene_names:
        its = scenes[sc]
        order, means = order_for_subset(its, vals)
        leave_scene_in.append({
            "scene": sc,
            "n_items": len(its),
            "order": list(order),
            "order_label": order_label(order),
            "matches_full": order == full_order,
        })
    out["leave_scene_in"] = leave_scene_in

    return out


def main():
    results = {}
    for rung_name, path in RUNGS.items():
        results[rung_name] = analyze_rung(rung_name, path)

    out_json = HERE / "dropk_results.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    write_summary(results, HERE / "dropk_summary.md")
    print(f"Wrote {out_json}")
    print(f"Wrote {HERE / 'dropk_summary.md'}")


def write_summary(results, out_path):
    lines = []
    lines.append("# Drop-k ranking robustness - summary\n")
    lines.append("Generated by `dropk.py`. Inputs: `per_item_250008.csv`, `per_item_25212.csv` "
                  "(3 seeds x 16 items, seed0' excluded from the ranking, tracked separately as the twin).\n")
    for rung_name in ("250008", "25212"):
        r = results[rung_name]
        lines.append(f"\n## Rung {rung_name}\n")
        lines.append(f"- Full-set order (16 items): **{r['full_set']['order_label']}**  "
                      f"(means: seed0={r['full_set']['means']['seed0']:.4f}, "
                      f"seed1={r['full_set']['means']['seed1']:.4f}, "
                      f"seed2={r['full_set']['means']['seed2']:.4f})\n")
        for k in ("1", "2", "3"):
            d = r["dropk"][k]
            top_alt = None
            for label, cnt in sorted(d["order_distribution"].items(), key=lambda kv: -kv[1]):
                if label != r["full_set"]["order_label"]:
                    top_alt = (label, cnt)
                    break
            lines.append(f"- k={k}: n_subsets={d['n_subsets']}, "
                          f"frac_preserve_exact={d['frac_preserve_exact']:.4f}, "
                          f"frac_best_preserved={d['frac_best_preserved']:.4f}, "
                          f"most common alternative order={top_alt[0] if top_alt else 'none'} "
                          f"(n={top_alt[1] if top_alt else 0})\n")
        lines.append("- Scene-level drop (drop each scene entirely):\n")
        for sd in r["scene_level_drop"]:
            lines.append(f"    - drop {sd['scene_dropped']} ({sd['n_items_dropped']} items) -> "
                          f"{sd['order_label']}{' [FLIP]' if sd['flips'] else ''}\n")
        lines.append(f"- Twin sign (seed0'-seed0) fraction positive: "
                      f"full={r['twin_sign_robustness']['full_set_sign_positive']}, "
                      f"k=1: {r['twin_sign_robustness']['by_k']['1']['frac_positive']:.4f}, "
                      f"k=2: {r['twin_sign_robustness']['by_k']['2']['frac_positive']:.4f}, "
                      f"k=3: {r['twin_sign_robustness']['by_k']['3']['frac_positive']:.4f}\n")
        lines.append("- Leave-scene-in orders:\n")
        for ls in r["leave_scene_in"]:
            lines.append(f"    - {ls['scene']} ({ls['n_items']} item(s)) alone -> {ls['order_label']}"
                          f"{' [matches full]' if ls['matches_full'] else ' [differs]'}\n")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
