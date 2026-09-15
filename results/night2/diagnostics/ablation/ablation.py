"""Cell-type ablation profiles of the four saved end states.

UNREGISTERED DIAGNOSTIC (Ark 2026-09-15 07:39, Zcode 07:43, Mike's word 07:43). Not a test
of hypothesis (b) or (b2). The protocol is fixed in README.md, which was written and saved
before this script was run for the first time.

WHAT THIS SCRIPT DOES NOT DO: it never trains, never writes into
connectome-seed-data/results/flow/9991/*, and never calls solver.checkpoint() or
solver.test(track_loss=True). The solver lives in a scratch datamate root; the four runs'
checkpoints are read with torch.load only.

The evaluator is REUSED from ../diag1_eval_paths.py (build_solver, chkpt_table,
load_checkpoint, hook_eval, per_item_eval, val_item_names) -- nothing about the evaluation
path is re-implemented here. The only thing this script adds is the ablation hook.
"""

import os
import sys

# Same two environment variables, set the same way and in the same place as
# night/run_individual.py:46-49 and diag1_eval_paths.py:27-32 (before torch / flyvis).
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
os.environ.setdefault(
    "FLYVIS_ROOT_DIR", "C:/Users/mikha/Documents/dpc-research/connectome-seed-data"
)

DIAG_DIR = "C:/Users/mikha/Documents/dpc-research/connectome-seed/results/night2/diagnostics"
sys.path.insert(0, DIAG_DIR)

import argparse
import itertools
import json
import time
from pathlib import Path

import numpy as np
import torch

import diag1_eval_paths as D  # the evaluator, reused verbatim

RUNS = D.RUNS  # {"000": "seed0", "900": "seed0prime", "001": "seed1", "002": "seed2"}
CHKPT = "chkpt_00071"  # iteration 250,008 in the csv convention
CLAMP_VALUE = 0.0  # fixed in README.md Sec 3 before running


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--out-dir", required=True)
    p.add_argument("--netdir-root", required=True)
    p.add_argument(
        "--repeat-only", action="store_true",
        help="POST-HOC control, added after the profiles were computed (README Sec 9): "
             "recompute the 65 single-type profiles a second time in a fresh process and "
             "write ablation_repeatability.json. Writes NOTHING else -- the profiles, "
             "controls and distances files are produced by the run WITHOUT this flag.")
    return p.parse_args()


# ---------------------------------------------------------------- the ablation hook
_HOOK_SEEN = []


def ablate_hook(state, mask):
    """Clamp the activity of the masked nodes to CLAMP_VALUE.

    Called from Network._state_api (flyvis/network/network.py:430-433), which runs at the
    end of _next_state (network.py:413), i.e. AFTER the Euler update (network.py:404-411)
    and BEFORE the source/target gathers that feed the next step (network.py:435-440); the
    activity yielded to the decoder (network.py:540) is this hooked value.  Also called at
    the end of _initial_state (network.py:375), so the grey steady state is clamped too.

    `mask` is 1.0 on kept nodes and 0.0 on ablated nodes, shape (n_nodes,), broadcast over
    the batch dimension.  CLAMP_VALUE is 0.0, so the multiplication is the clamp; the
    expression below is written as mask*x + (1-mask)*CLAMP_VALUE only in spirit -- with
    CLAMP_VALUE == 0.0 it reduces to the product, and the assert keeps that honest.
    """
    assert CLAMP_VALUE == 0.0
    if not _HOOK_SEEN:
        # PPNeuronIGRSynapses has exactly one node state variable; if a future config had
        # more, clamping only `activity` would be a silent half-ablation.
        _HOOK_SEEN.append((sorted(state.nodes.keys()), sorted(state.edges.keys())))
        assert _HOOK_SEEN[0] == (["activity"], []), _HOOK_SEEN[0]
    state.nodes.activity = state.nodes.activity * mask
    return state


def node_type_array(net):
    raw = net.connectome.nodes.type[:]
    return np.array([x.decode() if isinstance(x, bytes) else str(x) for x in raw])


def make_mask(types_arr, ablate_types, device):
    m = np.ones(len(types_arr), dtype=np.float32)
    if ablate_types:
        sel = np.isin(types_arr, np.array(list(ablate_types)))
        assert sel.sum() > 0, ablate_types
        m[sel] = 0.0
    return torch.as_tensor(m, device=device)


def eval_items(solver, mask):
    """16 per-item losses under the given mask (mask=None -> no hook registered at all)."""
    net = solver.network
    assert net._state_hooks == (), net._state_hooks
    if mask is not None:
        net.register_state_hook(ablate_hook, mask=mask)
    try:
        losses = D.per_item_eval(solver)
    finally:
        net.clear_state_hooks()
    assert net._state_hooks == ()
    return np.array(losses["flow"], dtype=np.float64)


# ---------------------------------------------------------------- statistics
def rankdata(x):
    """Average-tie ranks, so no scipy dependency is introduced."""
    x = np.asarray(x, dtype=np.float64)
    order = np.argsort(x, kind="mergesort")
    ranks = np.empty(len(x), dtype=np.float64)
    ranks[order] = np.arange(1, len(x) + 1, dtype=np.float64)
    # average ties
    sx = x[order]
    i = 0
    while i < len(sx):
        j = i
        while j + 1 < len(sx) and sx[j + 1] == sx[i]:
            j += 1
        if j > i:
            ranks[order[i : j + 1]] = np.mean(ranks[order[i : j + 1]])
        i = j + 1
    return ranks


def pearson(a, b):
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    a = a - a.mean()
    b = b - b.mean()
    return float(a @ b / np.sqrt((a @ a) * (b @ b)))


def spearman(a, b):
    return pearson(rankdata(a), rankdata(b))


def euclid(a, b):
    return float(np.sqrt(np.sum((np.asarray(a) - np.asarray(b)) ** 2)))


# ---------------------------------------------------------------- main
def main():
    a = parse_args()
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    t_start = time.perf_counter()

    solver = D.build_solver(Path(a.netdir_root))
    import flyvis

    net = solver.network
    device = flyvis.device
    types_arr = node_type_array(net)
    unique_types = list(dict.fromkeys(types_arr.tolist()))  # connectome order
    assert len(unique_types) == 65, len(unique_types)
    input_types = [
        x.decode() if isinstance(x, bytes) else str(x)
        for x in net.connectome.input_cell_types[:]
    ]
    output_types = [
        x.decode() if isinstance(x, bytes) else str(x)
        for x in net.connectome.output_cell_types[:]
    ]
    item_names = D.val_item_names(solver)
    assert len(item_names) == 16, item_names

    meta = {
        "flyvis": flyvis.__version__,
        "torch": torch.__version__,
        "python": sys.version.split()[0],
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "netdir": str(solver.dir.path),
        "device": str(device),
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "chkpt": CHKPT,
        "clamp_value": CLAMP_VALUE,
        "clamped_quantity": "state.nodes.activity (membrane voltage, PPNeuronIGRSynapses)",
        "hook_site": "flyvis/network/network.py:430-433 (_state_api), via register_state_hook:444-469",
        "n_nodes": int(net.n_nodes),
        "n_types": len(unique_types),
        "types": unique_types,
        "type_counts": {t: int((types_arr == t).sum()) for t in unique_types},
        "input_cell_types": input_types,
        "output_cell_types": output_types,
        "val_items": item_names,
        "activation": repr(net.dynamics.activation),
    }
    print("META", json.dumps({k: v for k, v in meta.items() if k not in ("types", "type_counts")}))

    # item subsets for the Zcode caveat
    idx16 = list(range(16))
    idx13 = [i for i, n in enumerate(item_names) if "ambush_2" not in n]
    idx10 = [i for i, n in enumerate(item_names) if "ambush_2" not in n and "bandage_1" not in n]
    assert len(idx13) == 13 and len(idx10) == 10, (len(idx13), len(idx10))

    if a.repeat_only:
        rep = {"meta": meta, "runs": {}}
        for run, label in RUNS.items():
            D.load_checkpoint(solver, D.FLOW_DIR / run / "chkpts" / CHKPT)
            base = eval_items(solver, None)
            b = float(base.mean())
            v = {}
            for T in unique_types:
                m = make_mask(types_arr, {T}, device)
                v[T] = float(eval_items(solver, m).mean() - b)
                print("REPEAT", label, T, repr(v[T]), flush=True)
            rep["runs"][label] = {"base_loss_16": repr(b),
                                  "delta_16": {k: repr(x) for k, x in v.items()}}
        (out / "ablation_repeatability.json").write_text(json.dumps(rep, indent=1))
        print("REPEAT WROTE", str(out / "ablation_repeatability.json"))
        return 0

    controls = {"meta": meta, "runs": {}}
    profiles = {}  # label -> {"base": (16,), "types": {T: (16,)}}

    for run, label in RUNS.items():
        path = D.FLOW_DIR / run / "chkpts" / CHKPT
        tab = D.chkpt_table(run)
        hit = [r for r in tab if r[3].name == CHKPT]
        assert len(hit) == 1
        _, stored_it, solver_it, _ = hit[0]
        info = D.load_checkpoint(solver, path)

        # ---- P0: no ablation at all (no hook registered)
        t0 = time.perf_counter()
        base_items = eval_items(solver, None)
        t_one = time.perf_counter() - t0
        base_mean = float(base_items.mean())
        hook_val = D.hook_eval(solver)  # the rung hook path, for the record

        # ---- P1: ablating the empty set (all-ones mask) must be a no-op
        m_none = make_mask(types_arr, set(), device)
        p1_items = eval_items(solver, m_none)
        p1_mean = float(p1_items.mean())

        # ---- P2: sets known to be essential to the readout
        m_p2a = make_mask(types_arr, set(input_types), device)
        p2a_items = eval_items(solver, m_p2a)
        m_p2b = make_mask(types_arr, set(output_types), device)
        p2b_items = eval_items(solver, m_p2b)

        controls["runs"][label] = {
            "run": run,
            "chkpt": CHKPT,
            "solver_iteration": solver_it,
            "stored_checkpoint_val_loss": repr(info["stored_val_loss"]),
            "P0_no_ablation_per_item_mean": repr(base_mean),
            "P0_hook_path_value": repr(hook_val),
            "P0_per_item_mean_minus_stored": repr(base_mean - info["stored_val_loss"]),
            "P0_hook_minus_stored": repr(hook_val - info["stored_val_loss"]),
            "P0_per_item_mean_minus_hook": repr(base_mean - hook_val),
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
        }
        print("CONTROLS", label, json.dumps({
            k: v for k, v in controls["runs"][label].items()
            if k not in ("P0_per_item", "P2a_types", "P2b_types")}), flush=True)

        # ---- the 65 single-type profiles
        per_type = {}
        for T in unique_types:
            m = make_mask(types_arr, {T}, device)
            per_type[T] = eval_items(solver, m)
            print("ABL", label, T, repr(float(per_type[T].mean() - base_mean)), flush=True)
        profiles[label] = {"base": base_items, "types": per_type}

    (out / "ablation_controls.json").write_text(json.dumps(controls, indent=1))

    # ---------------------------------------------------------------- csv
    hdr = (["run", "label", "type", "base_loss_16", "delta_16", "delta_norm_16",
            "delta_13", "delta_10"]
           + [f"delta_item_{n}" for n in item_names])
    lines = [",".join(hdr)]
    for run, label in RUNS.items():
        base = profiles[label]["base"]
        for T in unique_types:
            ab = profiles[label]["types"][T]
            d = ab - base
            row = [run, label, T, repr(float(base.mean())),
                   repr(float(ab.mean() - base.mean())),
                   repr(float((ab.mean() - base.mean()) / base.mean())),
                   repr(float(ab[idx13].mean() - base[idx13].mean())),
                   repr(float(ab[idx10].mean() - base[idx10].mean()))]
            row += [repr(float(x)) for x in d]
            lines.append(",".join(row))
    (out / "ablation_profiles.csv").write_text("\n".join(lines) + "\n")

    # ---------------------------------------------------------------- distances
    labels = ["seed0", "seed0prime", "seed1", "seed2"]
    pairs = [("seed0", "seed0prime"), ("seed0", "seed1"), ("seed0", "seed2"),
             ("seed1", "seed2"), ("seed0prime", "seed1"), ("seed0prime", "seed2")]
    subsets = {"16": idx16, "13_no_ambush2": idx13, "10_no_ambush2_no_bandage1": idx10}

    dist = {"meta": meta, "pairs": [f"{a}|{b}" for a, b in pairs], "subsets": {}}
    vecs_by_subset = {}
    for sname, idx in subsets.items():
        vec = {}
        vecn = {}
        for lab in labels:
            base = profiles[lab]["base"][idx]
            b = float(base.mean())
            v = np.array([float(profiles[lab]["types"][T][idx].mean() - b)
                          for T in unique_types])
            vec[lab] = v
            vecn[lab] = v / b
        vecs_by_subset[sname] = vec
        block = {}
        for x, y in pairs:
            block[f"{x}|{y}"] = {
                "euclidean": repr(euclid(vec[x], vec[y])),
                "euclidean_normalized_profiles": repr(euclid(vecn[x], vecn[y])),
                "spearman_rho": repr(spearman(vec[x], vec[y])),
                "spearman_distance_1_minus_rho": repr(1.0 - spearman(vec[x], vec[y])),
                "pearson_r": repr(pearson(vec[x], vec[y])),
            }
        twin_e = euclid(vec["seed0"], vec["seed0prime"])
        twin_s = 1.0 - spearman(vec["seed0"], vec["seed0prime"])
        e01 = euclid(vec["seed0"], vec["seed1"])
        e02 = euclid(vec["seed0"], vec["seed2"])
        s01 = 1.0 - spearman(vec["seed0"], vec["seed1"])
        s02 = 1.0 - spearman(vec["seed0"], vec["seed2"])
        block["twin_trap"] = {
            "euclidean_pass": bool(twin_e < e01 and twin_e < e02),
            "spearman_pass": bool(twin_s < s01 and twin_s < s02),
            "d_twin_euclid": repr(twin_e), "d_0_1_euclid": repr(e01),
            "d_0_2_euclid": repr(e02),
            "d_twin_spearman": repr(twin_s), "d_0_1_spearman": repr(s01),
            "d_0_2_spearman": repr(s02),
        }
        # sign agreement and top-10
        M = np.stack([vec[lab] for lab in labels])  # (4, 65)
        same_sign = np.all(M > 0, axis=0) | np.all(M < 0, axis=0)
        block["n_types_same_sign_all_four_runs"] = int(same_sign.sum())
        block["types_same_sign_all_four_runs"] = [
            unique_types[i] for i in range(65) if same_sign[i]]
        block["n_types_positive_all_four"] = int(np.all(M > 0, axis=0).sum())
        block["n_types_negative_all_four"] = int(np.all(M < 0, axis=0).sum())
        block["top10_by_abs_delta"] = {
            lab: [[unique_types[i], repr(float(vec[lab][i]))]
                  for i in np.argsort(-np.abs(vec[lab]))[:10]]
            for lab in labels}
        block["item_indices"] = idx
        dist["subsets"][sname] = block

    # profile magnitude, for context
    dist["profile_scale"] = {
        lab: {"l2_norm_16": repr(float(np.linalg.norm(vecs_by_subset["16"][lab]))),
              "max_abs_16": repr(float(np.max(np.abs(vecs_by_subset["16"][lab])))),
              "mean_abs_16": repr(float(np.mean(np.abs(vecs_by_subset["16"][lab]))))}
        for lab in labels}
    dist["wall_s_total"] = round(time.perf_counter() - t_start, 1)
    (out / "ablation_distances.json").write_text(json.dumps(dist, indent=1))
    print("DISTANCES", json.dumps({s: dist["subsets"][s]["twin_trap"] for s in subsets}))
    print("TOTAL WALL S", dist["wall_s_total"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
