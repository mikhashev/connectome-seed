"""Cell-type ablation profiles of seeds 3 and 4 (night 3), and the six-run analysis.

UNREGISTERED DIAGNOSTIC, same instrument as `results/night2/diagnostics/ablation/`. The
reading applied to the output is PRE-REGISTERED in `docs/next-session-plan.md` Sec 2a
(written 2026-09-15, before the night-3 launch).

WHAT THIS SCRIPT DOES NOT DO: it never trains, never writes into
connectome-seed-data/results/flow/9991/*, and never calls solver.checkpoint() or
solver.test(track_loss=True).  The solver lives in a scratch datamate root; the six runs'
checkpoints are read with torch.load only.  Nothing under results/night2/ is written.

NOTHING OF THE PROTOCOL IS RE-IMPLEMENTED HERE.  The evaluator comes from
`../../../night2/diagnostics/diag1_eval_paths.py` (build_solver, chkpt_table,
load_checkpoint, hook_eval, per_item_eval, val_item_names), the ablation hook and the rank
statistics from `../../../night2/diagnostics/ablation/ablation.py` (ablate_hook,
node_type_array, make_mask, eval_items, rankdata, pearson, spearman, euclid), and the seven
eval_rung invariants from `../../../night2/diagnostics/rowB/rowB.py` (snapshot_state,
invariants; hardening item 1).  This file adds only: the two new run ids, the six-run
distance table, and the pre-registered reading.

Hardening item 9: the sha256 of this script and of every module it reuses is written into
every output json.
"""

import os
import sys

# Same two environment variables, set the same way and in the same place as
# night/run_individual.py:46-49, diag1_eval_paths.py:27-32, ablation.py:22-26.
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
os.environ.setdefault(
    "FLYVIS_ROOT_DIR", "C:/Users/mikha/Documents/dpc-research/connectome-seed-data"
)

DIAG_DIR = "C:/Users/mikha/Documents/dpc-research/connectome-seed/results/night2/diagnostics"
N2_ABL = os.path.join(DIAG_DIR, "ablation")
sys.path.insert(0, DIAG_DIR)
sys.path.insert(0, N2_ABL)
sys.path.insert(0, os.path.join(DIAG_DIR, "rowB"))

import argparse
import csv
import hashlib
import json
import time
from pathlib import Path

import numpy as np
import torch

import diag1_eval_paths as D          # the evaluator, reused verbatim
import ablation as ABL                # the ablation hook + statistics, reused verbatim
import rowB as RB                     # the seven eval_rung invariants, reused verbatim

NEW_RUNS = {"003": "seed3", "004": "seed4"}          # night 3
OLD_RUNS = {"000": "seed0", "900": "seed0prime", "001": "seed1", "002": "seed2"}
LABELS6 = ["seed0", "seed0prime", "seed1", "seed2", "seed3", "seed4"]
CHKPT = ABL.CHKPT                                    # "chkpt_00071"
TWIN_PAIR = ("seed0", "seed0prime")
SAMEWAVE_PAIR = ("seed3", "seed4")
NOISE_BAND = 2e-3                                    # 002 Sec 5f, 2026-09-15 note
# Pre-registered reading, docs/next-session-plan.md Sec 2a (Ark 08:23/08:28, Zcode 08:24)
PREREG_TWIN_MAX_DISCREPANCY = 2863.0                 # max_T |d_T(0) - d_T(0')| , T2a
PREREG_SEED2_R2 = 21157.5
PREREG_R2 = {"seed0": 459.2, "seed0prime": 679.8, "seed1": -1.0, "seed2": 21157.5}

STATUS = ("UNREGISTERED DIAGNOSTIC; the READING is pre-registered in "
          "docs/next-session-plan.md Sec 2a (before the night-3 launch). "
          "A repeated observation is not a test.")


def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


SCRIPT_HASHES = {
    "ablation_night3.py": sha256_file(__file__),
    "night2/diagnostics/ablation/ablation.py": sha256_file(os.path.join(N2_ABL, "ablation.py")),
    "night2/diagnostics/diag1_eval_paths.py": sha256_file(
        os.path.join(DIAG_DIR, "diag1_eval_paths.py")),
    "night2/diagnostics/rowB/rowB.py": sha256_file(
        os.path.join(DIAG_DIR, "rowB", "rowB.py")),
}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--out-dir", required=True)
    p.add_argument("--netdir-root", required=True)
    p.add_argument("--repeat-only", action="store_true",
                   help="repeatability control (g): recompute the 65 single-type profiles of "
                        "seed 3 in a fresh process; writes ONLY ablation_repeatability.json")
    return p.parse_args()


def eval_with_invariants(solver, mask):
    """ABL.eval_items wrapped in the seven eval_rung invariants (hardening item 1)."""
    before = RB.snapshot_state(solver)
    items = ABL.eval_items(solver, mask)
    inv = RB.invariants(before, RB.snapshot_state(solver))
    assert all(inv.values()), inv          # hardening item 15 / rule R4: the witness vetoes
    return items, inv


def load_night2_profiles(types, item_names):
    """The four night-2 profiles from results/night2/diagnostics/ablation/ablation_profiles.csv.

    delta_13 / delta_10 are recomputed from the 16 per-item delta columns and checked against
    the stored delta_13 / delta_10 columns, so the subset definition used here is verified
    against night 2's own, not assumed.
    """
    path = Path(N2_ABL) / "ablation_profiles.csv"
    rows = list(csv.DictReader(path.open()))
    assert len(rows) == 4 * 65, len(rows)
    cols = [f"delta_item_{n}" for n in item_names]
    idx13 = [i for i, n in enumerate(item_names) if "ambush_2" not in n]
    idx10 = [i for i, n in enumerate(item_names)
             if "ambush_2" not in n and "bandage_1" not in n]
    out = {}
    maxdev = 0.0
    for r in rows:
        lab = r["label"]
        d = out.setdefault(lab, {"base": float(r["base_loss_16"]), "16": {}, "13": {}, "10": {}})
        per_item = np.array([float(r[c]) for c in cols])
        d["16"][r["type"]] = float(r["delta_16"])
        d["13"][r["type"]] = float(r["delta_13"])
        d["10"][r["type"]] = float(r["delta_10"])
        maxdev = max(maxdev, abs(per_item.mean() - float(r["delta_16"])),
                     abs(per_item[idx13].mean() - float(r["delta_13"])),
                     abs(per_item[idx10].mean() - float(r["delta_10"])))
    assert set(out) == set(OLD_RUNS.values()), sorted(out)
    for lab in out:
        assert list(out[lab]["16"]) == list(types), lab
    return out, maxdev


def main():
    a = parse_args()
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    t_start = time.perf_counter()

    solver = D.build_solver(Path(a.netdir_root))
    import flyvis

    net = solver.network
    device = flyvis.device
    types_arr = ABL.node_type_array(net)
    types = list(dict.fromkeys(types_arr.tolist()))
    assert len(types) == 65, len(types)
    input_types = [x.decode() if isinstance(x, bytes) else str(x)
                   for x in net.connectome.input_cell_types[:]]
    output_types = [x.decode() if isinstance(x, bytes) else str(x)
                    for x in net.connectome.output_cell_types[:]]
    item_names = D.val_item_names(solver)
    assert len(item_names) == 16, item_names

    # the evaluation set must be night 2's, item for item (hardening item 8: state labelled)
    n2_meta = json.loads((Path(N2_ABL) / "ablation_controls.json").read_text())["meta"]
    assert n2_meta["val_items"] == item_names, "evaluation set differs from night 2"
    assert n2_meta["types"] == types, "cell-type order differs from night 2"
    assert float(n2_meta["clamp_value"]) == ABL.CLAMP_VALUE == 0.0

    meta = {
        "status": STATUS,
        "script_sha256": SCRIPT_HASHES,
        "flyvis": flyvis.__version__, "torch": torch.__version__,
        "python": sys.version.split()[0],
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "netdir": str(solver.dir.path), "device": str(device),
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "chkpt": CHKPT, "state_label": "checkpoint 250,008 (chkpt_00071), per-item path",
        "clamp_value": ABL.CLAMP_VALUE,
        "clamped_quantity": "state.nodes.activity (membrane voltage, PPNeuronIGRSynapses)",
        "hook_site": "flyvis/network/network.py:430-433 (_state_api), via register_state_hook:444-469",
        "n_nodes": int(net.n_nodes), "n_types": len(types), "types": types,
        "type_counts": {t: int((types_arr == t).sum()) for t in types},
        "input_cell_types": input_types, "output_cell_types": output_types,
        "val_items": item_names, "activation": repr(net.dynamics.activation),
        "new_runs": NEW_RUNS, "night2_runs": OLD_RUNS,
        "noise_band": NOISE_BAND,
        "prereg_twin_max_discrepancy": PREREG_TWIN_MAX_DISCREPANCY,
    }
    print("META", json.dumps({k: v for k, v in meta.items()
                              if k not in ("types", "type_counts")}), flush=True)

    idx = {"16": list(range(16)),
           "13_no_ambush2": [i for i, n in enumerate(item_names) if "ambush_2" not in n],
           "10_no_ambush2_no_bandage1": [
               i for i, n in enumerate(item_names)
               if "ambush_2" not in n and "bandage_1" not in n]}
    assert len(idx["13_no_ambush2"]) == 13 and len(idx["10_no_ambush2_no_bandage1"]) == 10

    # ------------------------------------------------------------------ (g) repeatability
    if a.repeat_only:
        run, label = "003", "seed3"
        D.load_checkpoint(solver, D.FLOW_DIR / run / "chkpts" / CHKPT)
        base, _ = eval_with_invariants(solver, None)
        b = float(base.mean())
        v = {}
        for T in types:
            m = ABL.make_mask(types_arr, {T}, device)
            it, _ = eval_with_invariants(solver, m)
            v[T] = float(it.mean() - b)
            print("REPEAT", label, T, repr(v[T]), flush=True)
        rep = {"meta": meta, "runs": {label: {
            "run": run, "pid": os.getpid(), "base_loss_16": repr(b),
            "delta_16": {k: repr(x) for k, x in v.items()}}}}
        # compare against the first process
        rows = [r for r in csv.DictReader((out / "ablation_profiles.csv").open())
                if r["label"] == label]
        assert len(rows) == 65, len(rows)
        d1 = {r["type"]: float(r["delta_16"]) for r in rows}
        dd = {T: v[T] - d1[T] for T in types}
        order = sorted(types, key=lambda T: -abs(dd[T]))
        rep["comparison_to_first_process"] = {
            "base_loss_first": rows[0]["base_loss_16"],
            "base_loss_second_minus_first": repr(b - float(rows[0]["base_loss_16"])),
            "max_abs_delta_delta": repr(max(abs(x) for x in dd.values())),
            "max_abs_delta_delta_type": order[0],
            "median_abs_delta_delta": repr(float(np.median([abs(x) for x in dd.values()]))),
            "euclidean_between_repeats": repr(ABL.euclid(
                [v[T] for T in types], [d1[T] for T in types])),
            "spearman_between_repeats": repr(ABL.spearman(
                [v[T] for T in types], [d1[T] for T in types])),
            "top5_abs_delta_delta": [[T, repr(dd[T])] for T in order[:5]],
        }
        (out / "ablation_repeatability.json").write_text(json.dumps(rep, indent=1))
        print("REPEAT", json.dumps(rep["comparison_to_first_process"]))
        return 0

    # ------------------------------------------------------------------ profiles, seeds 3 & 4
    controls = {"meta": meta, "runs": {}}
    profiles = {}
    for run, label in NEW_RUNS.items():
        path = D.FLOW_DIR / run / "chkpts" / CHKPT
        tab = D.chkpt_table(run)
        assert len(tab) == 72, len(tab)
        hit = [r for r in tab if r[3].name == CHKPT]
        assert len(hit) == 1
        _, stored_it, solver_it, _ = hit[0]
        info = D.load_checkpoint(solver, path)

        t0 = time.perf_counter()
        base_items, inv0 = eval_with_invariants(solver, None)          # P0
        t_one = time.perf_counter() - t0
        base_mean = float(base_items.mean())
        hook_before = RB.snapshot_state(solver)
        hook_val = D.hook_eval(solver)
        inv_hook = RB.invariants(hook_before, RB.snapshot_state(solver))
        assert all(inv_hook.values()), inv_hook

        p1_items, inv1 = eval_with_invariants(                          # P1
            solver, ABL.make_mask(types_arr, set(), device))
        p2a_items, inv2a = eval_with_invariants(                        # P2a
            solver, ABL.make_mask(types_arr, set(input_types), device))
        p2b_items, inv2b = eval_with_invariants(                        # P2b
            solver, ABL.make_mask(types_arr, set(output_types), device))
        p1_mean = float(p1_items.mean())

        controls["runs"][label] = {
            "run": run, "chkpt": CHKPT, "chkpt_iter_h5": stored_it,
            "solver_iteration": solver_it,
            "stored_checkpoint_val_loss": repr(info["stored_val_loss"]),
            "P0_no_ablation_per_item_mean": repr(base_mean),
            "P0_hook_path_value": repr(hook_val),
            "P0_per_item_mean_minus_stored": repr(base_mean - info["stored_val_loss"]),
            "P0_hook_minus_stored": repr(hook_val - info["stored_val_loss"]),
            "P0_per_item_mean_minus_hook": repr(base_mean - hook_val),
            "P0_pass_1e-3": bool(abs(base_mean - info["stored_val_loss"]) < 1e-3),
            "P0_per_item": [repr(x) for x in base_items],
            "P1_empty_set_per_item_mean": repr(p1_mean),
            "P1_minus_P0": repr(p1_mean - base_mean),
            "P1_max_abs_per_item_diff": repr(float(np.max(np.abs(p1_items - base_items)))),
            "P1_bitwise_identical": bool(np.array_equal(p1_items, base_items)),
            "P2a_types": input_types,
            "P2a_per_item_mean": repr(float(p2a_items.mean())),
            "P2a_delta": repr(float(p2a_items.mean()) - base_mean),
            "P2a_delta_normalized": repr((float(p2a_items.mean()) - base_mean) / base_mean),
            "P2b_types": output_types,
            "P2b_per_item_mean": repr(float(p2b_items.mean())),
            "P2b_delta": repr(float(p2b_items.mean()) - base_mean),
            "P2b_delta_normalized": repr((float(p2b_items.mean()) - base_mean) / base_mean),
            "one_evaluation_wall_s": round(t_one, 3),
            "eval_rung_invariants": {"P0": inv0, "P0_hook_path": inv_hook, "P1": inv1,
                                     "P2a": inv2a, "P2b": inv2b},
        }
        print("CONTROLS", label, json.dumps({
            k: v for k, v in controls["runs"][label].items()
            if k not in ("P0_per_item", "P2a_types", "P2b_types")}), flush=True)

        per_type, inv_all = {}, True
        for T in types:
            m = ABL.make_mask(types_arr, {T}, device)
            per_type[T], inv = eval_with_invariants(solver, m)
            inv_all = inv_all and all(inv.values())
            print("ABL", label, T, repr(float(per_type[T].mean() - base_mean)), flush=True)
        controls["runs"][label]["eval_rung_invariants"]["all_65_single_type_pass"] = bool(inv_all)
        profiles[label] = {"base": base_items, "types": per_type}

    (out / "ablation_controls.json").write_text(json.dumps(controls, indent=1))

    # ------------------------------------------------------------------ csv (seeds 3 and 4)
    hdr = (["run", "label", "type", "base_loss_16", "delta_16", "delta_norm_16",
            "delta_13", "delta_10"] + [f"delta_item_{n}" for n in item_names])
    lines = [",".join(hdr)]
    for run, label in NEW_RUNS.items():
        base = profiles[label]["base"]
        for T in types:
            ab = profiles[label]["types"][T]
            d = ab - base
            row = [run, label, T, repr(float(base.mean())),
                   repr(float(ab.mean() - base.mean())),
                   repr(float((ab.mean() - base.mean()) / base.mean())),
                   repr(float(ab[idx["13_no_ambush2"]].mean()
                              - base[idx["13_no_ambush2"]].mean())),
                   repr(float(ab[idx["10_no_ambush2_no_bandage1"]].mean()
                              - base[idx["10_no_ambush2_no_bandage1"]].mean()))]
            row += [repr(float(x)) for x in d]
            lines.append(",".join(row))
    (out / "ablation_profiles.csv").write_text("\n".join(lines) + "\n")

    # ------------------------------------------------------------------ six-run vectors
    n2, n2_maxdev = load_night2_profiles(types, item_names)
    vec = {s: {} for s in idx}          # subset -> label -> (65,)
    vecn = {s: {} for s in idx}
    base_by_subset = {s: {} for s in idx}
    for s, ii in idx.items():
        key = {"16": "16", "13_no_ambush2": "13", "10_no_ambush2_no_bandage1": "10"}[s]
        for lab in OLD_RUNS.values():
            v = np.array([n2[lab][key][T] for T in types])
            b = n2[lab]["base"]          # 16-item base; night 2 divided by the subset base
            vec[s][lab] = v
            base_by_subset[s][lab] = b
        for lab in NEW_RUNS.values():
            base = profiles[lab]["base"][ii]
            b = float(base.mean())
            vec[s][lab] = np.array(
                [float(profiles[lab]["types"][T][ii].mean() - b) for T in types])
            base_by_subset[s][lab] = b
    # night 2 stored only the 16-item base per run; the normalized profile for the 13/10
    # subsets therefore uses the run's subset base only for the new runs.  To keep the six
    # runs on ONE definition, the normalized profile is defined on the 16-item base for all
    # six (the 16-item base is the only base recorded for all six runs).
    for s in idx:
        for lab in LABELS6:
            vecn[s][lab] = vec[s][lab] / base_by_subset["16"][lab]

    pairs15 = [(LABELS6[i], LABELS6[j]) for i in range(6) for j in range(i + 1, 6)]
    assert len(pairs15) == 15

    dist = {"meta": meta, "night2_csv_recompute_max_dev": repr(n2_maxdev),
            "pairs": [f"{x}|{y}" for x, y in pairs15],
            "normalized_profile_base": "16-item base loss of the run (all six runs)",
            "subsets": {}}
    for s, ii in idx.items():
        block = {}
        for x, y in pairs15:
            rho = ABL.spearman(vec[s][x], vec[s][y])
            block[f"{x}|{y}"] = {
                "euclidean": repr(ABL.euclid(vec[s][x], vec[s][y])),
                "euclidean_normalized_profiles": repr(ABL.euclid(vecn[s][x], vecn[s][y])),
                "spearman_rho": repr(rho),
                "spearman_distance_1_minus_rho": repr(1.0 - rho),
                "pearson_r": repr(ABL.pearson(vec[s][x], vec[s][y])),
            }
        sp = {p: 1.0 - ABL.spearman(vec[s][p[0]], vec[s][p[1]]) for p in pairs15}
        eu = {p: ABL.euclid(vec[s][p[0]], vec[s][p[1]]) for p in pairs15}
        foreign = [p for p in pairs15 if p != TWIN_PAIR]
        near_s = min(foreign, key=lambda p: sp[p])
        near_e = min(foreign, key=lambda p: eu[p])
        cross = [p for p in pairs15 if p not in (TWIN_PAIR, SAMEWAVE_PAIR)]
        block["twin_trap_15_pairs"] = {
            "twin_spearman_distance": repr(sp[TWIN_PAIR]),
            "twin_is_global_min_spearman": bool(all(sp[TWIN_PAIR] < sp[p] for p in foreign)),
            "nearest_foreign_pair_spearman": [f"{near_s[0]}|{near_s[1]}", repr(sp[near_s])],
            "twin_euclidean": repr(eu[TWIN_PAIR]),
            "twin_is_global_min_euclidean": bool(all(eu[TWIN_PAIR] < eu[p] for p in foreign)),
            "nearest_foreign_pair_euclidean": [f"{near_e[0]}|{near_e[1]}", repr(eu[near_e])],
            "ranked_spearman": [[f"{p[0]}|{p[1]}", repr(sp[p])]
                                for p in sorted(pairs15, key=lambda p: sp[p])],
            "ranked_euclidean": [[f"{p[0]}|{p[1]}", repr(eu[p])]
                                 for p in sorted(pairs15, key=lambda p: eu[p])],
        }
        block["same_wave_pair_3_4"] = {
            "spearman_distance": repr(sp[SAMEWAVE_PAIR]),
            "euclidean": repr(eu[SAMEWAVE_PAIR]),
            "rank_among_15_spearman": 1 + sorted(pairs15, key=lambda p: sp[p]).index(SAMEWAVE_PAIR),
            "rank_among_15_euclidean": 1 + sorted(pairs15, key=lambda p: eu[p]).index(SAMEWAVE_PAIR),
            "cross_wave_pairs_spearman_min": repr(min(sp[p] for p in cross)),
            "cross_wave_pairs_spearman_median": repr(float(np.median([sp[p] for p in cross]))),
            "cross_wave_pairs_spearman_max": repr(max(sp[p] for p in cross)),
            "cross_wave_pairs_euclidean_min": repr(min(eu[p] for p in cross)),
            "cross_wave_pairs_euclidean_median": repr(float(np.median([eu[p] for p in cross]))),
            "cross_wave_pairs_euclidean_max": repr(max(eu[p] for p in cross)),
            "note": ("cross-wave = the 13 pairs that are neither the twins (0,0'), night 1, "
                     "nor the night-3 same-wave pair (3,4). seed1 (wave night2) and seed2 "
                     "(wave night2b, solo re-run) are NOT a same-wave pair."),
        }
        M = np.stack([vec[s][lab] for lab in LABELS6])
        same = np.all(M > 0, axis=0) | np.all(M < 0, axis=0)
        block["n_types_same_sign_all_six_runs"] = int(same.sum())
        block["types_same_sign_all_six_runs"] = [types[i] for i in range(65) if same[i]]
        block["n_types_positive_all_six"] = int(np.all(M > 0, axis=0).sum())
        block["n_types_negative_all_six"] = int(np.all(M < 0, axis=0).sum())
        M4 = np.stack([vec[s][lab] for lab in LABELS6[:4]])
        same4 = np.all(M4 > 0, axis=0) | np.all(M4 < 0, axis=0)
        block["n_types_same_sign_night2_four_runs_recomputed"] = int(same4.sum())
        block["top10_by_abs_delta"] = {
            lab: [[types[i], repr(float(vec[s][lab][i]))]
                  for i in np.argsort(-np.abs(vec[s][lab]))[:10]] for lab in LABELS6}
        block["ranked_full"] = {
            lab: [[types[i], repr(float(vec[s][lab][i]))]
                  for i in np.argsort(-np.abs(vec[s][lab]))] for lab in LABELS6}
        # hardening item 7: the band a sign claim is read against
        block["noise_band"] = NOISE_BAND
        block["min_abs_delta"] = {lab: repr(float(np.min(np.abs(vec[s][lab]))))
                                  for lab in LABELS6}
        block["n_types_inside_noise_band"] = {
            lab: int((np.abs(vec[s][lab]) < NOISE_BAND).sum()) for lab in LABELS6}
        block["types_inside_noise_band"] = {
            lab: [types[i] for i in range(65) if abs(vec[s][lab][i]) < NOISE_BAND]
            for lab in LABELS6}
        block["item_indices"] = ii
        dist["subsets"][s] = block

    dist["profile_scale"] = {
        lab: {"base_loss_16": repr(base_by_subset["16"][lab]),
              "l2_norm_16": repr(float(np.linalg.norm(vec["16"][lab]))),
              "max_abs_16": repr(float(np.max(np.abs(vec["16"][lab])))),
              "mean_abs_16": repr(float(np.mean(np.abs(vec["16"][lab])))),
              "median_16": repr(float(np.median(vec["16"][lab]))),
              "sd_16": repr(float(np.std(vec["16"][lab], ddof=1))),
              "n_negative_16": int((vec["16"][lab] < 0).sum())} for lab in LABELS6}
    dist["wall_s_total"] = round(time.perf_counter() - t_start, 1)
    (out / "ablation_distances.json").write_text(json.dumps(dist, indent=1))

    # ------------------------------------------------------------------ the registered reading
    v16 = vec["16"]
    reading = {"meta": meta,
               "rule_source": "docs/next-session-plan.md Sec 2a (Ark 08:23/08:28, Zcode 08:24)",
               "rule": ("negative: if NEITHER seed 3 nor seed 4 shows a single-type dependence "
                        "of the size seen in seed 2, seed 2's R2 finding remains a single "
                        "observation. positive: a type whose excess exceeds 2863 (the largest "
                        "twin per-type discrepancy, T2a) in seed 3 OR seed 4 makes it a "
                        "repeated observation -- still not a test."),
               "threshold_abs": PREREG_TWIN_MAX_DISCREPANCY,
               "seed2_reference_R2": PREREG_SEED2_R2,
               "per_seed": {}}
    for lab in LABELS6:
        v = v16[lab]
        order = np.argsort(-v)                 # excess = signed delta, "cost of silencing"
        top = [(types[i], float(v[i])) for i in order[:3]]
        order_abs = np.argsort(-np.abs(v))
        reading["per_seed"][lab] = {
            "max_delta_type": top[0][0], "max_delta": repr(top[0][1]),
            "second_delta_type": top[1][0], "second_delta": repr(top[1][1]),
            "third_delta_type": top[2][0], "third_delta": repr(top[2][1]),
            "ratio_max_over_second": repr(top[0][1] / top[1][1]) if top[1][1] != 0 else None,
            "order_of_magnitude_above_next": bool(top[1][1] != 0 and top[0][1] / top[1][1] >= 10),
            "exceeds_2863": bool(top[0][1] > PREREG_TWIN_MAX_DISCREPANCY),
            "top3_by_abs": [[types[i], repr(float(v[i]))] for i in order_abs[:3]],
            "delta_R2": repr(float(v[types.index("R2")])),
        }
    s3 = reading["per_seed"]["seed3"]
    s4 = reading["per_seed"]["seed4"]
    reading["verdict"] = {
        "seed3_positive": s3["exceeds_2863"], "seed4_positive": s4["exceeds_2863"],
        "positive_reading_triggered": bool(s3["exceeds_2863"] or s4["exceeds_2863"]),
        "text": ("POSITIVE: a single-type dependence exceeding 2863 appears in seed 3 or seed 4 "
                 "-> the R2 finding becomes a REPEATED OBSERVATION, still not a test."
                 if (s3["exceeds_2863"] or s4["exceeds_2863"]) else
                 "NEGATIVE: neither seed 3 nor seed 4 shows a single-type dependence exceeding "
                 "2863 -> seed 2's R2 finding REMAINS A SINGLE OBSERVATION and is not "
                 "interpreted as a property of individuals."),
    }
    reading["R2_across_six_runs"] = {
        lab: repr(float(v16[lab][types.index("R2")])) for lab in LABELS6}
    reading["R2_prereg_recorded_night2"] = PREREG_R2
    reading["R2_night2_recompute_check"] = {
        lab: repr(abs(float(v16[lab][types.index("R2")]) - PREREG_R2[lab]))
        for lab in PREREG_R2}
    (out / "ablation_reading.json").write_text(json.dumps(reading, indent=1))
    print("READING", json.dumps(reading["verdict"]))
    print("R2", json.dumps(reading["R2_across_six_runs"]))
    print("TOTAL WALL S", dist["wall_s_total"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
