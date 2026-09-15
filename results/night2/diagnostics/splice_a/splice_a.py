"""Hypothesis (a) COMPOSITION package -- splice cell type T2's module from B (seed 1)
into A (seed 0), on the saved checkpoints at iteration 250,008.

Registered test: `docs/preregistration-cheap-vs-expensive.md` Sec 2 (the module and the
pair) and Sec 5 (a) (the criterion).  Ark's null-shift calibration (Sec 4 of the brief,
2026-09-15 07:33) is NOT registered and is recorded here as a calibration, written to
disk BEFORE the real splice is evaluated.

WHAT THIS SCRIPT DOES NOT DO: it never trains, never writes into
connectome-seed-data/results/flow/9991/*, never calls solver.checkpoint() and never calls
solver.test(track_loss=True).  The solver lives in a throw-away datamate root in the
session scratchpad (--netdir-root), built by diag1_eval_paths.build_solver; the two runs'
checkpoints are read with torch.load only.  Every parameter change is made in memory on
that throw-away solver.

REUSE (brief's instruction): the evaluator and the parameter loading are imported, not
re-implemented, from `results/night2/diagnostics/diag1_eval_paths.py` --
  build_solver()   the solver in a scratch datamate root
  chkpt_table()    checkpoint index -> csv iteration mapping (stored iter + 1)
  load_checkpoint()  recover_network / recover_decoder + scheduler at that iteration
  hook_eval()      THE RUNG HOOK, night/run_individual.py:531-546 verbatim -- the
                   registered evaluator; its value on chkpt_00071 of seed 0 reproduces
                   the stored checkpoint val_loss to 1.03e-4 (diag1a_paths.json)
  per_item_eval()  the 16 per-item losses (a copy of flyvis/solver.py:474-556); NOT the
                   hook path, used only for the per-item column beside every aggregate
  val_item_names() the 16 held-out item names

Stages, run as separate processes in this order, each writing its file before the next
runs (--stage):
  indices    -> t2_module_indices.json
  reference  -> reference.json
  self       -> self_splice.json
  calib      -> calibration.json
  splice     -> splice_result.json
  extra      -> extra_unregistered.json   (NOT part of the registered test)
  percsv     -> per_item.csv              (assembles the per-item columns already written)
"""

import os
import sys
from pathlib import Path

REPO = Path("C:/Users/mikha/Documents/dpc-research/connectome-seed")
DIAG = REPO / "results" / "night2" / "diagnostics"
OUT = DIAG / "splice_a"

# diag1_eval_paths.py sets CUBLAS_WORKSPACE_CONFIG and FLYVIS_ROOT_DIR with setdefault at
# import time, in the same place and the same way as night/run_individual.py:46-49.
sys.path.insert(0, str(DIAG))

import argparse  # noqa: E402
import json  # noqa: E402
import time  # noqa: E402

import numpy as np  # noqa: E402
import torch  # noqa: E402

from diag1_eval_paths import (  # noqa: E402
    build_solver,
    chkpt_table,
    hook_eval,
    load_checkpoint,
    per_item_eval,
    val_item_names,
)

RUN_A = "000"  # A = seed 0
RUN_B = "001"  # B = seed 1
TARGET_ITER = 250008  # csv iteration of chkpt_00071 (chkpt_iter.h5 250007 + 1)

# The 24 incoming source types listed in the pre-registration Sec 2 (fixed 2026-09-13,
# Ark), pasted here verbatim as the control for step 1.
PREREG_SOURCES = [
    "C2", "C3", "L4", "L5", "Mi1", "Mi13", "Mi2", "Mi3", "Mi9", "T2", "T3", "T5b",
    "T5d", "Tm1", "Tm16", "Tm2", "Tm3", "Tm4", "TmY13", "TmY15", "TmY18", "TmY3",
    "TmY4", "TmY5a",
]
TYPE = "T2"
K = 26

FLOOR_REL = 3 * 1.1104 / 100.0      # 3.3313 % -- Sec 5 (a), filled 2026-09-15
BOUND_REL = 5.0 / 100.0             # 5 % -- Sec 5 (a), fixed 2026-09-13
BASIS_PREREG = 1146.1958            # the number Sec 5 (a) names literally (hook@250,000)
FLOOR_ABS_PREREG = 38.18            # Sec 5 (a), as written
BOUND_ABS_PREREG = 57.31            # Sec 5 (a), as written
STORED_LA = 1148.8074851036072      # stored checkpoint val_loss, chkpt_00071, run 000


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def meta(solver, stage):
    import flyvis
    return {
        "flyvis": flyvis.__version__,
        "torch": torch.__version__,
        "python": sys.version.split()[0],
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "netdir": str(solver.dir.path) if solver is not None else None,
        "stage": stage,
        "utc": utc(),
    }


def chkpt_path(run):
    hit = [r for r in chkpt_table(run) if r[2] == TARGET_ITER]
    assert len(hit) == 1, (run, TARGET_ITER, hit)
    return hit[0][3]


# ------------------------------------------------------------------ module identification
def module_spec(solver):
    """The 26 (state-dict key, flat index) pairs of cell type T2's free parameters.

    Ordering source, cited:
      nodes_bias / nodes_time_const -- flyvis/network/network.py:167 registers the raw
        values of each node Parameter under "nodes_<name>"; the per-entry order is
        Parameter.keys, built in flyvis/network/initialization.py:345-356
        (RestingPotential: nodes.groupby(param_config.groupby, sort=False).first(),
        keys = param_config["type"].tolist()).
      edges_syn_strength -- flyvis/network/network.py:199 registers "edges_<name>"; the
        per-entry order is flyvis/network/initialization.py:496-515
        (SynapseStrength: edges.groupby(param_config.groupby, sort=False).mean(),
        keys = list(zip(source_type, target_type))).
    """
    net = solver.network
    bias_keys = list(net.node_params.bias.keys)
    tc_keys = list(net.node_params.time_const.keys)
    syn_keys = [tuple(k) for k in net.edge_params.syn_strength.keys]
    assert len(bias_keys) == 65, len(bias_keys)
    assert bias_keys == tc_keys, "node groupings differ between bias and time_const"
    assert len(syn_keys) == 604, len(syn_keys)

    i_type = bias_keys.index(TYPE)
    edge_idx = [j for j, (s, t) in enumerate(syn_keys) if t == TYPE]
    sources = [syn_keys[j][0] for j in edge_idx]

    spec = [("nodes_bias", i_type), ("nodes_time_const", i_type)]
    spec += [("edges_syn_strength", j) for j in edge_idx]
    return spec, bias_keys, syn_keys, i_type, edge_idx, sources


def get_module_from_state(net_sd, spec):
    return np.array(
        [float(net_sd[k].reshape(-1)[i].item()) for k, i in spec], dtype=np.float64
    )


def get_module_live(network, spec):
    return np.array(
        [float(getattr(network, k).data.view(-1)[i].item()) for k, i in spec],
        dtype=np.float64,
    )


def set_module_live(network, spec, vec):
    assert len(vec) == len(spec)
    with torch.no_grad():
        for (k, i), val in zip(spec, vec):
            getattr(network, k).data.view(-1)[i] = float(val)
    got = get_module_live(network, spec)
    # float32 storage: the write must round-trip to float32 precision
    assert np.allclose(got, np.asarray(vec, dtype=np.float64), rtol=0, atol=1e-6), (
        got - np.asarray(vec)
    )


def evaluate(solver, names):
    """Aggregate by the registered hook path; per-item beside it."""
    t = time.perf_counter()
    hook = hook_eval(solver)
    wall = time.perf_counter() - t
    per = per_item_eval(solver)["flow"]
    assert len(per) == len(names) == 16, (len(per), len(names))
    return {
        "hook": hook,
        "per_item": [float(x) for x in per],
        "per_item_mean": float(np.mean(per)),
        "per_item_mean_minus_hook": float(np.mean(per) - hook),
        "eval_wall_s": round(wall, 3),
    }


def write(path, obj):
    Path(path).write_text(json.dumps(obj, indent=1), encoding="utf-8")
    print("WROTE", path, flush=True)


# ------------------------------------------------------------------ stages
def stage_indices(solver):
    spec, bias_keys, syn_keys, i_type, edge_idx, sources = module_spec(solver)
    prereg = sorted(PREREG_SOURCES)
    found = sorted(sources)
    match = prereg == found
    rec = {
        "meta": meta(solver, "indices"),
        "cell_type": TYPE,
        "k_expected": K,
        "k_found": len(spec),
        "ordering_source": {
            "nodes_bias/nodes_time_const": (
                "flyvis/network/network.py:167 register_parameter('nodes_'+name); order = "
                "Parameter.keys from flyvis/network/initialization.py:345-356"
            ),
            "edges_syn_strength": (
                "flyvis/network/network.py:199 register_parameter('edges_'+name); order = "
                "Parameter.keys from flyvis/network/initialization.py:496-515"
            ),
        },
        "n_node_types": len(bias_keys),
        "n_edge_types": len(syn_keys),
        "node_type_index_of_T2": i_type,
        "node_types_order": bias_keys,
        "module": [
            {"slot": n, "key": k, "flat_index": i,
             "label": (TYPE if k.startswith("nodes_") else f"{syn_keys[i][0]}->{syn_keys[i][1]}")}
            for n, (k, i) in enumerate(spec)
        ],
        "incoming_source_types_found": sources,
        "incoming_source_types_prereg_sec2": PREREG_SOURCES,
        "sets_match": match,
        "only_in_found": sorted(set(found) - set(prereg)),
        "only_in_prereg": sorted(set(prereg) - set(found)),
        "symmetry_masks_present": {
            k: len(v) for k, v in solver.network.symmetry_config.items()
        },
        "clamp_config": {
            k: (str(v) if v is not None else None)
            for k, v in solver.network.clamp_config.items()
        },
        "note_clamp": (
            "Network.clamp() (flyvis/network/network.py:480-507) is called in training "
            "only; solver.test() does not call it, so neither clamping nor the symmetry "
            "averaging is applied by any evaluation in this package."
        ),
    }
    write(OUT / "t2_module_indices.json", rec)
    assert len(spec) == K, f"module size {len(spec)} != {K}"
    if not match:
        print("MISMATCH between found source types and the pre-registration Sec 2 list")
        return 2
    print("OK k =", len(spec), "T2 node index", i_type, "edge indices", edge_idx)
    return 0


def stage_reference(solver):
    spec, *_ = module_spec(solver)
    names = val_item_names(solver)
    info = load_checkpoint(solver, chkpt_path(RUN_A))
    ev = evaluate(solver, names)
    rec = {
        "meta": meta(solver, "reference"),
        "run": RUN_A, "label": "A = seed 0", "solver_iteration": info["solver_iteration"],
        "stored_checkpoint_val_loss": info["stored_val_loss"],
        "L_A": ev["hook"],
        "L_A_minus_stored": ev["hook"] - info["stored_val_loss"],
        "reproduces_stored_to_1e-3": abs(ev["hook"] - STORED_LA) < 1e-3,
        "val_items": names,
        "eval": ev,
        "T2_module_A": get_module_live(solver.network, spec).tolist(),
    }
    write(OUT / "reference.json", rec)
    assert rec["reproduces_stored_to_1e-3"], rec["L_A"]
    print("L_A", repr(ev["hook"]))
    return 0


def stage_self(solver):
    spec, *_ = module_spec(solver)
    names = val_item_names(solver)
    load_checkpoint(solver, chkpt_path(RUN_A))
    base = evaluate(solver, names)                      # same-process baseline
    mod_a = get_module_live(solver.network, spec)
    set_module_live(solver.network, spec, mod_a)        # A <- A, the instrument control
    after = evaluate(solver, names)
    ref = json.loads((OUT / "reference.json").read_text(encoding="utf-8"))
    rec = {
        "meta": meta(solver, "self"),
        "what": "instrument control A<-A (registered, Sec 2 / Sec 7); never an (a) outcome",
        "baseline_same_process": base,
        "after_self_splice": after,
        "delta_vs_same_process_baseline": after["hook"] - base["hook"],
        "delta_vs_reference_json_L_A": after["hook"] - ref["L_A"],
        "module_unchanged_bitwise": bool(
            np.array_equal(get_module_live(solver.network, spec), mod_a)
        ),
        "per_item_delta_vs_baseline": [
            a - b for a, b in zip(after["per_item"], base["per_item"])
        ],
    }
    write(OUT / "self_splice.json", rec)
    print("SELF delta", repr(rec["delta_vs_same_process_baseline"]))
    return 0


def stage_calib(solver):
    """Ark's null-shift calibration -- NOT registered.  Written before the real splice."""
    spec, *_ = module_spec(solver)
    names = val_item_names(solver)
    a_sd = torch.load(chkpt_path(RUN_A), map_location="cpu", weights_only=False)["network"]
    b_sd = torch.load(chkpt_path(RUN_B), map_location="cpu", weights_only=False)["network"]
    t2_a = get_module_from_state(a_sd, spec)
    t2_b = get_module_from_state(b_sd, spec)
    v = t2_b - t2_a
    r = float(np.linalg.norm(v))

    load_checkpoint(solver, chkpt_path(RUN_A))
    base = evaluate(solver, names)
    ref = json.loads((OUT / "reference.json").read_text(encoding="utf-8"))

    draws = []
    for seed in range(20):
        rng = np.random.default_rng(seed)
        u = rng.standard_normal(K)
        u = u / np.linalg.norm(u) * r
        load_checkpoint(solver, chkpt_path(RUN_A))   # full reset before every draw
        set_module_live(solver.network, spec, t2_a + u)
        ev = evaluate(solver, names)
        d = ev["hook"] - base["hook"]
        shifted = t2_a + u
        draws.append({
            "seed": seed, "u": u.tolist(), "norm_u": float(np.linalg.norm(u)),
            # edges_syn_strength carries clamp 'non_negative' in training
            # (flyvis/network/network.py:490-500); clamp() is not called at evaluation,
            # so a draw may sit at raw values training could not have reached.
            "n_syn_strength_slots_negative": int((shifted[2:] < 0).sum()),
            "L": ev["hook"], "delta_vs_base": d, "abs_delta": abs(d),
            "delta_vs_reference_json_L_A": ev["hook"] - ref["L_A"],
            "per_item": ev["per_item"],
            "per_item_delta_vs_base": [
                x - y for x, y in zip(ev["per_item"], base["per_item"])
            ],
        })
        print("CALIB", seed, repr(d), flush=True)

    refs = {}
    for name, shift in (("minus_v", -v), ("plus_2v", 2 * v)):
        load_checkpoint(solver, chkpt_path(RUN_A))
        set_module_live(solver.network, spec, t2_a + shift)
        ev = evaluate(solver, names)
        d = ev["hook"] - base["hook"]
        refs[name] = {
            "shift_norm": float(np.linalg.norm(shift)),
            "L": ev["hook"], "delta_vs_base": d, "abs_delta": abs(d),
            "delta_vs_reference_json_L_A": ev["hook"] - ref["L_A"],
            "per_item": ev["per_item"],
            "per_item_delta_vs_base": [
                x - y for x, y in zip(ev["per_item"], base["per_item"])
            ],
        }
        print("REFSHIFT", name, repr(d), flush=True)

    ad = np.array([d["abs_delta"] for d in draws])
    rec = {
        "meta": meta(solver, "calib"),
        "what": ("Ark's null-shift calibration, DPC Research chat 2026-09-15 07:33. "
                 "NOT part of the registered test; recorded before the real splice is "
                 "evaluated."),
        "val_items": names,
        "T2_module_A": t2_a.tolist(),
        "T2_module_B": t2_b.tolist(),
        "v_B_minus_A": v.tolist(),
        "r_norm_v": r,
        "per_slot_scale": [
            {"slot": n, "key": k, "flat_index": i, "A": float(t2_a[n]),
             "B": float(t2_b[n]), "v": float(v[n])}
            for n, (k, i) in enumerate(spec)
        ],
        "baseline_same_process": base,
        "floor_abs_prereg_basis": FLOOR_ABS_PREREG,
        "draws": draws,
        "summary_abs_delta": {
            "n": int(ad.size), "mean": float(ad.mean()), "median": float(np.median(ad)),
            "max": float(ad.max()), "min": float(ad.min()), "std": float(ad.std(ddof=1)),
            "n_above_floor_38.18": int((ad > FLOOR_ABS_PREREG).sum()),
            "values": ad.tolist(),
        },
        "reference_shifts": refs,
    }
    write(OUT / "calibration.json", rec)
    return 0


def stage_calibsummary(_solver):
    """Added to calibration.json AFTER --stage calib and BEFORE --stage splice, because
    four of the twenty draws diverged (two inf, two > 1e11) and inf poisons the mean /
    median / max of `summary_abs_delta`.  Adds fields only; changes nothing already
    written."""
    p = OUT / "calibration.json"
    cal = json.loads(p.read_text(encoding="utf-8"))
    assert not (OUT / "splice_result.json").exists(), "splice already evaluated"
    ad = np.array([d["abs_delta"] for d in cal["draws"]], dtype=np.float64)
    finite = np.isfinite(ad)
    # "diverged" = not finite, or more than 10x the largest of the two real-direction
    # reference shifts; the rule is stated here, applied once, before the splice.
    refmax = max(cal["reference_shifts"][k]["abs_delta"] for k in cal["reference_shifts"])
    ok = finite & (ad <= 10 * refmax)
    sub = ad[ok]
    cal["summary_abs_delta_finite_subset"] = {
        "utc": utc(),
        "rule": ("a draw is EXCLUDED from this subset if its |delta| is not finite or "
                 f"exceeds 10x the largest real-direction reference shift ({refmax}); "
                 "the full 20-value list in summary_abs_delta is unchanged"),
        "excluded_seeds": [int(s) for s in np.where(~ok)[0]],
        "excluded_values": [repr(float(x)) for x in ad[~ok]],
        "n_kept": int(sub.size), "mean": float(sub.mean()),
        "median": float(np.median(sub)), "max": float(sub.max()),
        "min": float(sub.min()), "std": float(sub.std(ddof=1)),
        "n_above_floor_38.18": int((sub > FLOOR_ABS_PREREG).sum()),
        "n_above_floor_38.18_of_all_20": int((ad > FLOOR_ABS_PREREG).sum()),
        "values": sub.tolist(),
    }
    write(p, cal)
    return 0


def stage_splice(solver):
    spec, *_ = module_spec(solver)
    names = val_item_names(solver)
    b_sd = torch.load(chkpt_path(RUN_B), map_location="cpu", weights_only=False)["network"]
    t2_b = get_module_from_state(b_sd, spec)

    load_checkpoint(solver, chkpt_path(RUN_A))
    base = evaluate(solver, names)
    t2_a = get_module_live(solver.network, spec)
    set_module_live(solver.network, spec, t2_b)
    after = evaluate(solver, names)

    ref = json.loads((OUT / "reference.json").read_text(encoding="utf-8"))
    L_A = ref["L_A"]
    d_base = after["hook"] - base["hook"]
    d_ref = after["hook"] - L_A

    def categorise(delta, floor_abs, bound_abs):
        a = abs(delta)
        if a <= floor_abs:
            return "effect not measurable on this module - uninformative"
        if a >= bound_abs:
            return "does not compose"
        return "composes predictably for this pair"

    floor_on_LA = FLOOR_REL * L_A
    bound_on_LA = BOUND_REL * L_A
    rec = {
        "meta": meta(solver, "splice"),
        "what": "THE REGISTERED SPLICE: T2_A <- T2_B, A = seed 0, B = seed 1, all 26",
        "val_items": names,
        "T2_module_A_before": t2_a.tolist(),
        "T2_module_B_written": t2_b.tolist(),
        "baseline_same_process": base,
        "after_splice": after,
        "L_A_reference_json": L_A,
        "L_A_from_B": after["hook"],
        "delta_vs_reference_L_A": d_ref,
        "delta_vs_same_process_baseline": d_base,
        "abs_delta_over_L_A_percent": 100.0 * abs(d_ref) / L_A,
        "abs_delta_over_1146.1958_percent": 100.0 * abs(d_ref) / BASIS_PREREG,
        "per_item_delta_vs_baseline": [
            a - b for a, b in zip(after["per_item"], base["per_item"])
        ],
        "basis_prereg_literal_1146.1958": {
            "basis": BASIS_PREREG,
            "floor_abs": FLOOR_ABS_PREREG, "bound_5pct_abs": BOUND_ABS_PREREG,
            "abs_delta": abs(d_ref),
            "category": categorise(d_ref, FLOOR_ABS_PREREG, BOUND_ABS_PREREG),
        },
        "basis_L_A_same_weights": {
            "basis": L_A,
            "floor_rel_pct": 100 * FLOOR_REL, "bound_rel_pct": 100 * BOUND_REL,
            "floor_abs": floor_on_LA, "bound_5pct_abs": bound_on_LA,
            "abs_delta": abs(d_ref),
            "category": categorise(d_ref, floor_on_LA, bound_on_LA),
        },
    }
    write(OUT / "splice_result.json", rec)
    print("SPLICE delta", repr(d_ref))
    return 0


def stage_extra(solver):
    """NOT part of the registered test: the reverse splice A -> B and B <- B."""
    spec, *_ = module_spec(solver)
    names = val_item_names(solver)
    a_sd = torch.load(chkpt_path(RUN_A), map_location="cpu", weights_only=False)["network"]
    t2_a = get_module_from_state(a_sd, spec)

    load_checkpoint(solver, chkpt_path(RUN_B))
    base_b = evaluate(solver, names)
    t2_b = get_module_live(solver.network, spec)

    set_module_live(solver.network, spec, t2_b)          # B <- B
    self_b = evaluate(solver, names)

    load_checkpoint(solver, chkpt_path(RUN_B))
    set_module_live(solver.network, spec, t2_a)          # B <- A
    rev = evaluate(solver, names)

    rec = {
        "meta": meta(solver, "extra"),
        "what": ("NOT part of the registered (a) test -- extra context only: the reverse "
                 "splice B<-A and the B<-B self-splice."),
        "val_items": names,
        "L_B_reference": base_b["hook"],
        "baseline_B": base_b,
        "self_splice_B": self_b,
        "delta_self_B": self_b["hook"] - base_b["hook"],
        "reverse_splice_B_from_A": rev,
        "delta_reverse": rev["hook"] - base_b["hook"],
        "abs_delta_reverse_over_L_B_percent":
            100.0 * abs(rev["hook"] - base_b["hook"]) / base_b["hook"],
        "per_item_delta_reverse": [
            a - b for a, b in zip(rev["per_item"], base_b["per_item"])
        ],
    }
    write(OUT / "extra_unregistered.json", rec)
    print("REVERSE delta", repr(rec["delta_reverse"]), "B<-B", repr(rec["delta_self_B"]))
    return 0


def stage_percsv(_solver):
    ref = json.loads((OUT / "reference.json").read_text(encoding="utf-8"))
    slf = json.loads((OUT / "self_splice.json").read_text(encoding="utf-8"))
    cal = json.loads((OUT / "calibration.json").read_text(encoding="utf-8"))
    spl = json.loads((OUT / "splice_result.json").read_text(encoding="utf-8"))
    ext = json.loads((OUT / "extra_unregistered.json").read_text(encoding="utf-8"))
    names = ref["val_items"]
    cd = np.array([d["per_item_delta_vs_base"] for d in cal["draws"]], dtype=np.float64)
    # the 16 kept draws of summary_abs_delta_finite_subset (rule stated there); the
    # all-20 columns are kept beside them and carry inf where a draw diverged
    keep = [i for i in range(cd.shape[0])
            if i not in cal["summary_abs_delta_finite_subset"]["excluded_seeds"]]
    cdf = cd[keep]
    cols = [
        ("item", names),
        ("L_A", ref["eval"]["per_item"]),
        ("A_self_splice", slf["after_self_splice"]["per_item"]),
        ("A_self_delta", slf["per_item_delta_vs_baseline"]),
        ("A_from_B", spl["after_splice"]["per_item"]),
        ("A_from_B_delta", spl["per_item_delta_vs_baseline"]),
        ("calib_mean_delta", cd.mean(axis=0).tolist()),
        ("calib_min_delta", cd.min(axis=0).tolist()),
        ("calib_max_delta", cd.max(axis=0).tolist()),
        ("calib_mean_abs_delta", np.abs(cd).mean(axis=0).tolist()),
        ("calib16_mean_delta", cdf.mean(axis=0).tolist()),
        ("calib16_min_delta", cdf.min(axis=0).tolist()),
        ("calib16_max_delta", cdf.max(axis=0).tolist()),
        ("calib16_mean_abs_delta", np.abs(cdf).mean(axis=0).tolist()),
        ("minus_v_delta", cal["reference_shifts"]["minus_v"]["per_item_delta_vs_base"]),
        ("plus_2v_delta", cal["reference_shifts"]["plus_2v"]["per_item_delta_vs_base"]),
        ("L_B", ext["baseline_B"]["per_item"]),
        ("B_from_A_delta", ext["per_item_delta_reverse"]),
    ]
    lines = [",".join(c[0] for c in cols)]
    for i in range(len(names)):
        row = []
        for name, vals in cols:
            v = vals[i]
            row.append(v if isinstance(v, str) else repr(round(float(v), 6)))
        lines.append(",".join(row))
    agg = ["AGGREGATE_hook",
           repr(ref["L_A"]), repr(slf["after_self_splice"]["hook"]),
           repr(slf["delta_vs_same_process_baseline"]),
           repr(spl["L_A_from_B"]), repr(spl["delta_vs_reference_L_A"]),
           repr(float(np.mean([d["delta_vs_base"] for d in cal["draws"]]))),
           repr(float(np.min([d["delta_vs_base"] for d in cal["draws"]]))),
           repr(float(np.max([d["delta_vs_base"] for d in cal["draws"]]))),
           repr(float(np.mean([d["abs_delta"] for d in cal["draws"]]))),
           repr(float(np.mean([cal["draws"][i]["delta_vs_base"] for i in keep]))),
           repr(float(np.min([cal["draws"][i]["delta_vs_base"] for i in keep]))),
           repr(float(np.max([cal["draws"][i]["delta_vs_base"] for i in keep]))),
           repr(float(np.mean([cal["draws"][i]["abs_delta"] for i in keep]))),
           repr(cal["reference_shifts"]["minus_v"]["delta_vs_base"]),
           repr(cal["reference_shifts"]["plus_2v"]["delta_vs_base"]),
           repr(ext["L_B_reference"]), repr(ext["delta_reverse"])]
    lines.append(",".join(agg))
    (OUT / "per_item.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("WROTE", OUT / "per_item.csv")
    return 0


STAGES = {
    "indices": stage_indices, "reference": stage_reference, "self": stage_self,
    "calib": stage_calib, "calibsummary": stage_calibsummary, "splice": stage_splice,
    "extra": stage_extra, "percsv": stage_percsv,
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--stage", required=True, choices=list(STAGES))
    p.add_argument("--netdir-root", required=False)
    a = p.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if a.stage in ("percsv", "calibsummary"):
        return STAGES[a.stage](None)
    assert a.netdir_root, "--netdir-root required"
    solver = build_solver(Path(a.netdir_root))
    print("META", json.dumps(meta(solver, a.stage)), flush=True)
    return STAGES[a.stage](solver)


if __name__ == "__main__":
    sys.exit(main())
