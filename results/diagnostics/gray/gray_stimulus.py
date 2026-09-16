"""Gray-stimulus control -- 6 runs x 2 checkpoints x 4 input conditions on the 16 held-out items.

PREVIEW DIAGNOSTIC -- NOT A TEST.  The protocol is fixed in
`docs/briefs/2026-09-16-step1-gray-stimulus.md` (v3.1, commit 54823c4; v2 after review by Ark and
Zcode, v3/v3.1 after the v2 run stopped at the copy-fidelity gate).  The v2 launch (Mike's word,
2026-09-16 19:50:18Z) stopped at that gate (README_v2_gate_stop.md).  The v3.1 run was launched on
Mike's explicit word in the DPC Research chat, 2026-09-16 20:14:03Z: «@CC_windows запускай шаг 1».

WHAT THIS SCRIPT DOES NOT DO: it never trains, never writes into
connectome-seed-data/results/flow/9991/*, never calls solver.checkpoint() or
solver.test(track_loss=True), and never registers an ablation hook (`net._state_hooks == ()` is
asserted before and after every evaluation).  The solver lives in a scratch datamate root; the six
runs' checkpoints are read with torch.load only.  Nothing under results/night2/ or results/night3/
is written.

NOTHING OF THE EVALUATION PATH IS RE-IMPLEMENTED.  `build_solver`, `chkpt_table`,
`load_checkpoint`, `hook_eval`, `per_item_eval`, `val_item_names` come from
`../../night2/diagnostics/diag1_eval_paths.py`; the seven eval_rung invariants from
`../../night2/diagnostics/rowB/rowB.py` (byte-identical to
`../../night3/diagnostics/rowB/rowB.py`, sha256 recorded for both), wrapped exactly as
`../../night3/diagnostics/ablation/ablation_night3.py:96-102`; `ablation.py` is imported only so
its sha256 can be recorded and so that the "no hook" assertion uses the same attribute the
ablation used.

The ONE thing this script adds is `per_item_eval_transformed` below: a line-for-line copy of
`diag1_eval_paths.py:176-201` `per_item_eval` in which the argument of line 191
(`solver.network.stimulus.add_input(data["lum"])`) is replaced by `transform(data["lum"], _i)`.
Everything else in the copy -- `t_pre=0.25`, `value=0.5` (:183-184), `augmentation(False)` (:187),
the decoder call (:196), the loss call (:198) -- is byte-identical.  The only other textual
difference is the loop variable `_` -> `_i` on the `for` of :188, needed to index the per-item
frame permutation of condition (d); it is recorded here and in README.md as a deviation from
"only the argument of line 191 changes".  Copy fidelity is measured, not assumed, by
--task control (brief v3.1 Sec 6): the copy with the identity transform (A) against each of FIVE
calls B_1..B_5 of D.per_item_eval on the same loaded checkpoint; the floor is the maximum
per-item |B_j - B_k| over all 10 pairs; pass iff max_k max per-item |A - B_k| <= floor, and at
iteration 0 equality must be bitwise.

v3.1 CHANGES TO THIS SCRIPT (after the v2 gate stop; conditions, the transform line and the
evaluator reuse are untouched): `copy_fidelity_control` (five-call floor, used by --task control
and --task main); --task main stops before the sweep if that control fails; --task repeat gates
max |delta loss_16| per checkpoint against 3 x the in-process floor on the 16-item mean recorded
in gray_controls.json and reports <= 1e-4 separately; --task readings implements brief Sec 7 v3 --
reading (ii) `excess_cond = L_trained,cond - L_untrained_gray`, >= 10 gain_s explodes /
<= 0.1 gain_s returns / else between (the v2 executor's provisional 3062.6 threshold is removed);
reading (iii) void when the two references lie within 0.2 gain_s.
"""

import os
import sys

# Same two environment variables, set the same way and in the same place as
# night/run_individual.py:46-49, diag1_eval_paths.py:27-32, ablation.py:22-26,
# ablation_night3.py:30-33.
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
os.environ.setdefault(
    "FLYVIS_ROOT_DIR", "C:/Users/mikha/Documents/dpc-research/connectome-seed-data"
)

CS = "C:/Users/mikha/Documents/dpc-research/connectome-seed"
DIAG_DIR = os.path.join(CS, "results/night2/diagnostics")
N2_ABL = os.path.join(DIAG_DIR, "ablation")
N2_ROWB = os.path.join(DIAG_DIR, "rowB")
N3_ROWB = os.path.join(CS, "results/night3/diagnostics/rowB")
N3_ABL = os.path.join(CS, "results/night3/diagnostics/ablation")
sys.path.insert(0, DIAG_DIR)
sys.path.insert(0, N2_ABL)
sys.path.insert(0, N2_ROWB)

import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np
import torch

import diag1_eval_paths as D          # the evaluator, reused verbatim
import ablation as ABL                # imported for provenance + the no-hook attribute
import rowB as RB                     # the seven eval_rung invariants, reused verbatim

# ---------------------------------------------------------------- fixed protocol constants
RUNS6 = {"000": "seed0", "900": "seed0prime", "001": "seed1",
         "002": "seed2", "003": "seed3", "004": "seed4"}
LABELS6 = ["seed0", "seed0prime", "seed1", "seed2", "seed3", "seed4"]
# checkpoint index -> solver iteration, rowB.py:56-57 NAMED_CHKPTS; asserted at run time
CHKPTS = {0: 0, 71: 250008}                      # chkpt_00000 / chkpt_00071
CHKPT_NAMES = {0: "chkpt_00000", 71: "chkpt_00071"}
CONDITIONS = ["real", "gray", "zero", "shuffled"]
GRAY_VALUE = 0.5                                 # brief Sec 4
ZERO_VALUE = 0.0
SHUFFLE_SEED = 20260916                          # brief Sec 1/3: fixed, recorded here
P0_TOL = 1e-4                                    # brief Sec 6
FRESH_PROCESS_TOL = 1e-4                         # brief Sec 6 (reported separately, v3)
FRESH_PROCESS_FLOOR_MULT = 3.0                   # brief Sec 6 v3: gate <= 3 x in-process floor
N_FLOOR_CALLS = 5                                # brief Sec 6 v3.1: five calls, all 10 pairs
BAND_FRACTION = 0.1                              # brief Sec 7 (i)/(iii): 0.1 * gain_s
EXPLODE_MULT = 10.0                              # brief Sec 7 (ii) v3: excess >= 10 gain_s
RETURN_FRACTION = 0.1                            # brief Sec 7 (ii) v3: excess <= 0.1 gain_s
VOID_FRACTION = 0.2                              # brief Sec 7 (iii) v3: refs within 0.2 gain_s
# brief Sec 7 (ii), pre-registered reference numbers
PREREG_SEED2_R2_DELTA = 21157.5
PREREG_SEED2_R1R8_CLAMP_EXCESS = 30626.0

STATUS = ("PREVIEW DIAGNOSTIC -- NOT A TEST (gray-stimulus control, brief "
          "docs/briefs/2026-09-16-step1-gray-stimulus.md v3.1; n=6 individuals)")


def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


SCRIPT_HASHES = {
    "results/diagnostics/gray/gray_stimulus.py": sha256_file(__file__),
    "results/night2/diagnostics/diag1_eval_paths.py": sha256_file(
        os.path.join(DIAG_DIR, "diag1_eval_paths.py")),
    "results/night2/diagnostics/ablation/ablation.py": sha256_file(
        os.path.join(N2_ABL, "ablation.py")),
    "results/night2/diagnostics/rowB/rowB.py": sha256_file(
        os.path.join(N2_ROWB, "rowB.py")),
    "results/night3/diagnostics/rowB/rowB.py": sha256_file(
        os.path.join(N3_ROWB, "rowB.py")),
    "results/night3/diagnostics/ablation/ablation_night3.py": sha256_file(
        os.path.join(N3_ABL, "ablation_night3.py")),
}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--task", required=True,
                   choices=["control", "floor", "main", "repeat", "readings"])
    p.add_argument("--out-dir", required=True)
    p.add_argument("--netdir-root", required=False)
    return p.parse_args()


# ---------------------------------------------------------------- the four input conditions
def frame_permutation(item_index, n_frames):
    """Fixed per-item permutation of the frame axis (condition d).

    Derived from (SHUFFLE_SEED, item_index) alone -- not from a global RNG stream -- so it is
    the same permutation in every process, for every run and every checkpoint.
    """
    return np.random.default_rng([SHUFFLE_SEED, int(item_index)]).permutation(int(n_frames))


def make_transform(condition):
    if condition == "real":
        return lambda lum, i: lum
    if condition == "gray":
        return lambda lum, i: torch.full_like(lum, GRAY_VALUE)
    if condition == "zero":
        return lambda lum, i: torch.zeros_like(lum)
    if condition == "shuffled":
        def _t(lum, i):
            perm = frame_permutation(i, lum.shape[1])
            return lum[:, torch.as_tensor(np.asarray(perm), device=lum.device)]
        return _t
    raise ValueError(condition)


CONDITION_DEFS = {
    "real": ("condition (c): the unmodified data['lum'] -- the identity transform; "
             "diag1_eval_paths.py:191 unchanged"),
    "gray": ("condition (a): torch.full_like(data['lum'], 0.5) -- every input element 0.5, "
             "flyvis's own resting/background value (network.py:548-586, moving_bar.py:194)"),
    "zero": ("condition (b): torch.zeros_like(data['lum']) -- every input element 0.0, "
             "full-field black; NOT the resting state"),
    "shuffled": ("condition (d): data['lum'] with its frame axis (dim 1) permuted by "
                 "numpy.random.default_rng([SHUFFLE_SEED, item_index]).permutation(n_frames), "
                 "SHUFFLE_SEED=%d; content and per-frame image statistics preserved, temporal "
                 "ordering destroyed; the target is NOT permuted" % SHUFFLE_SEED),
}


# ---------------------------------------------------------------- the copied evaluator
def per_item_eval_transformed(solver, transform, t_pre=0.25):
    """diag1_eval_paths.py:176-201 `per_item_eval`, copied line for line; the ONLY changes are
    the argument of :191 (`data["lum"]` -> `transform(data["lum"], _i)`) and the loop variable
    `_` -> `_i` on :188."""
    task, dataloader = solver.task, solver.task.val_data
    solver._eval()
    solver.scheduler(solver.iteration)  # solver.py:504
    initial_state = solver.network.steady_state(
        t_pre=t_pre, dt=task.dataset.dt, batch_size=dataloader.batch_size, value=0.5)
    losses = {t: [] for t in task.dataset.tasks}
    with torch.no_grad():
        with task.dataset.augmentation(False):
            for _i, data in enumerate(dataloader):
                n_samples, n_frames, _, _ = data["lum"].shape
                solver.network.stimulus.zero(n_samples, n_frames)
                solver.network.stimulus.add_input(transform(data["lum"], _i))
                activity = solver.network(solver.network.stimulus(), task.dataset.dt,
                                          state=initial_state)
                for t in task.dataset.tasks:
                    y = data[t]
                    y_est = solver.decoder[t](activity)
                    losses[t].append(
                        task.loss(y_est, y, t, **data.get("loss_kwargs", {}))
                        .detach().cpu().item())
    solver._train()
    return losses


def eval_condition(solver, condition):
    """One 16-item evaluation under one input condition, wrapped in the seven eval_rung
    invariants (ablation_night3.py:96-102) and the no-ablation-hook assertion
    (ablation.py:104, 111)."""
    net = solver.network
    assert net._state_hooks == (), net._state_hooks
    before = RB.snapshot_state(solver)
    t0 = time.perf_counter()
    losses = per_item_eval_transformed(solver, make_transform(condition))
    wall = time.perf_counter() - t0
    inv = RB.invariants(before, RB.snapshot_state(solver))
    assert net._state_hooks == (), net._state_hooks
    if not all(inv.values()):
        print("INVARIANT FAILURE", condition, json.dumps(inv), flush=True)
        raise SystemExit("eval_rung invariant False -- stopping (brief Sec 10.9)")
    return np.array(losses["flow"], dtype=np.float64), inv, wall


def load_named(solver, run, chkpt_index):
    """rowB.py:287-295 load_named, reused in spirit: the index -> iteration mapping is asserted
    against chkpt_table at run time, never assumed."""
    tab = D.chkpt_table(run)
    assert len(tab) == 72, (run, len(tab))
    hit = [r for r in tab if r[0] == chkpt_index]
    assert len(hit) == 1, (run, chkpt_index)
    ci, stored_it, solver_it, path = hit[0]
    assert solver_it == CHKPTS[chkpt_index], (chkpt_index, solver_it)
    assert path.name == CHKPT_NAMES[chkpt_index], (path.name, chkpt_index)
    info = D.load_checkpoint(solver, path)
    return solver_it, path, info


def copy_fidelity_control(solver, run, ci):
    """Brief Sec 6 v3.1: copy fidelity against the evaluator's own five-call floor, plus P0.

    A = the copy with the identity transform; B_1..B_5 = five calls of the ORIGINAL
    D.per_item_eval on the same loaded checkpoint, in the same process.  floor = max per-item
    |B_j - B_k| over all 10 pairs.  Pass iff max_k max per-item |A - B_k| <= floor; at iteration 0
    the floor must be 0.0 and A must equal every B_k bitwise.  P0: mean(A) - stored val_loss and
    mean(A) - hook_eval() both <= 1e-4.
    """
    solver_it, path, info = load_named(solver, run, ci)
    net = solver.network
    assert net._state_hooks == (), net._state_hooks
    a_items = np.array(
        per_item_eval_transformed(solver, make_transform("real"))["flow"],
        dtype=np.float64)                                 # the copy, identity transform
    assert net._state_hooks == (), net._state_hooks
    B = []
    for _k in range(N_FLOOR_CALLS):
        B.append(np.array(D.per_item_eval(solver)["flow"], dtype=np.float64))   # the original
        assert net._state_hooks == (), net._state_hooks
    B = np.stack(B)
    hook = D.hook_eval(solver)
    assert net._state_hooks == (), net._state_hooks
    pairs = [(j, k) for j in range(N_FLOOR_CALLS) for k in range(j + 1, N_FLOOR_CALLS)]
    assert len(pairs) == 10, len(pairs)
    pair_item = {f"B{j + 1}-B{k + 1}": float(np.max(np.abs(B[j] - B[k]))) for j, k in pairs}
    pair_mean = {f"B{j + 1}-B{k + 1}": float(abs(float(B[j].mean()) - float(B[k].mean())))
                 for j, k in pairs}
    floor_item = max(pair_item.values())
    floor_mean = max(pair_mean.values())
    a_vs_item = {f"A-B{k + 1}": float(np.max(np.abs(a_items - B[k])))
                 for k in range(N_FLOOR_CALLS)}
    a_vs_mean = {f"A-B{k + 1}": float(a_items.mean()) - float(B[k].mean())
                 for k in range(N_FLOOR_CALLS)}
    worst_key = max(a_vs_item, key=lambda k: a_vs_item[k])
    worst = a_vs_item[worst_key]
    bitwise = {f"A==B{k + 1}": bool(np.array_equal(a_items, B[k])) for k in range(N_FLOOR_CALLS)}
    if solver_it == 0:
        cf_pass = bool(floor_item == 0.0 and all(bitwise.values()))
        cf_rule = "iteration 0: floor must be 0.0 and A must equal every B_k bitwise"
    else:
        cf_pass = bool(worst <= floor_item)
        cf_rule = ("max_k max per-item |A - B_k| <= floor "
                   "(max per-item |B_j - B_k| over all 10 pairs)")
    p0 = float(a_items.mean()) - info["stored_val_loss"]
    p0h = float(a_items.mean()) - hook
    p0_pass = bool(abs(p0) <= P0_TOL and abs(p0h) <= P0_TOL)
    rec = {
        "run": run, "chkpt": path.name, "solver_iteration": solver_it,
        "n_original_calls": N_FLOOR_CALLS, "n_pairs": len(pairs),
        "floor_max_abs_per_item_diff_over_10_pairs": repr(floor_item),
        "floor_max_abs_mean_diff_over_10_pairs": repr(floor_mean),
        "floor_per_pair_max_abs_per_item_diff": {k: repr(v) for k, v in pair_item.items()},
        "floor_per_pair_abs_mean_diff": {k: repr(v) for k, v in pair_mean.items()},
        "original_means_B1_to_B5": [repr(float(x)) for x in B.mean(axis=1)],
        "n_distinct_original_means": len(set(B.mean(axis=1).tolist())),
        "copy_A_mean": repr(float(a_items.mean())),
        "copy_vs_each_original_max_abs_per_item": {k: repr(v) for k, v in a_vs_item.items()},
        "copy_vs_each_original_mean_diff": {k: repr(v) for k, v in a_vs_mean.items()},
        "copy_vs_each_original_bitwise_equal": bitwise,
        "copy_worst_pair": worst_key,
        "copy_worst_max_abs_per_item": repr(worst),
        "copy_fidelity_rule": cf_rule,
        "copy_fidelity_pass": cf_pass,
        "stored_checkpoint_val_loss": repr(info["stored_val_loss"]),
        "P0_per_item_mean": repr(float(a_items.mean())),
        "P0_mean_minus_stored": repr(p0),
        "P0_hook_path_value": repr(hook),
        "P0_per_item_mean_minus_hook": repr(p0h),
        "P0_pass_1e-4": p0_pass,
    }
    return rec, bool(cf_pass and p0_pass)


def item_short(n):
    """rowB.py:296-297."""
    return n.replace("sequence_", "")


# ---------------------------------------------------------------- constant-output null
def constant_output_null(solver):
    """Brief Sec 6: the loss a constant prediction would incur on the 16 items, from the targets
    alone, with the evaluator's own `task.loss` (l2norm, flyvis/task/objectives.py:10-22).

    (i) per-item mean of y_gt over frames and hexals (the best possible constant per item) --
        this is `constant_output_null`;
    (ii) zero against y_gt -- weaker, illustrative only, NOT constant_output_null.
    """
    task, dataloader = solver.task, solver.task.val_data
    per_item_mean, per_item_zero = [], []
    with torch.no_grad():
        with task.dataset.augmentation(False):
            for _i, data in enumerate(dataloader):
                for t in task.dataset.tasks:
                    y = data[t]
                    # (i) best possible constant: the per-item mean over frames (dim 1) and
                    #     hexals (dim 3), kept per flow component (dim 2)
                    y_mean = y.mean(dim=(1, 3), keepdim=True).expand_as(y)
                    per_item_mean.append(
                        task.loss(y_mean, y, t, **data.get("loss_kwargs", {}))
                        .detach().cpu().item())
                    # (ii) zero
                    per_item_zero.append(
                        task.loss(torch.zeros_like(y), y, t, **data.get("loss_kwargs", {}))
                        .detach().cpu().item())
    m = np.array(per_item_mean, dtype=np.float64)
    z = np.array(per_item_zero, dtype=np.float64)
    return {
        "definition_i_per_item_mean": (
            "l2norm(y_gt.mean(dim=(1,3),keepdim=True).expand_as(y_gt), y_gt) via task.loss, "
            "16-item mean -- the tighter, best-possible-constant comparator"),
        "definition_ii_zero": (
            "l2norm(zeros_like(y_gt), y_gt) via task.loss, 16-item mean -- weaker, "
            "illustrative only, NOT constant_output_null"),
        "constant_output_null": repr(float(m.mean())),
        "constant_output_null_per_item": [repr(float(x)) for x in m],
        "zero_prediction_null": repr(float(z.mean())),
        "zero_prediction_null_per_item": [repr(float(x)) for x in z],
    }


# ---------------------------------------------------------------- csv
def write_losses_csv(path, rows, item_names, sha):
    hdr = (["run", "label", "checkpoint_iter", "condition", "loss_16"]
           + [f"loss_item_{item_short(n)}" for n in item_names])
    lines = ["# " + STATUS,
             f"# script_sha256={sha}",
             ",".join(hdr)]
    for r in rows:
        line = [r["run"], r["label"], str(r["checkpoint_iter"]), r["condition"],
                repr(float(r["loss_16"]))]
        line += [repr(float(x)) for x in r["per_item"]]
        lines.append(",".join(line))
    Path(path).write_text("\n".join(lines) + "\n")


def read_losses_csv(path):
    lines = [ln for ln in Path(path).read_text(encoding="utf-8").strip().split("\n")
             if not ln.startswith("#")]
    hdr = lines[0].split(",")
    out = {}
    for ln in lines[1:]:
        parts = ln.split(",")
        assert len(parts) == len(hdr), (len(parts), len(hdr))
        row = dict(zip(hdr, parts))
        key = (row["label"], int(row["checkpoint_iter"]), row["condition"])
        assert key not in out, f"duplicate key {key!r} -- refusing"
        out[key] = {"run": row["run"], "loss_16": float(row["loss_16"]),
                    "per_item": np.array([float(row[c]) for c in hdr[5:]],
                                         dtype=np.float64)}
    return out


# ---------------------------------------------------------------- the sweep
def sweep(solver, item_names, print_tag):
    """All 48 cells: 6 runs x 2 checkpoints x 4 conditions."""
    rows, per_cell = [], {}
    first_real_wall = None
    for run, label in RUNS6.items():
        for ci in sorted(CHKPTS):
            solver_it, path, info = load_named(solver, run, ci)
            for cond in CONDITIONS:
                items, inv, wall = eval_condition(solver, cond)
                if cond == "real" and first_real_wall is None:
                    first_real_wall = wall
                mean = float(items.mean())
                rows.append({"run": run, "label": label, "checkpoint_iter": solver_it,
                             "condition": cond, "loss_16": mean, "per_item": items})
                per_cell[(label, solver_it, cond)] = {
                    "run": run, "chkpt": path.name,
                    "stored_checkpoint_val_loss": repr(info["stored_val_loss"]),
                    "loss_16": repr(mean),
                    "wall_s": repr(wall),
                    "eval_rung_invariants": inv,
                }
                if cond == "real":
                    per_cell[(label, solver_it, cond)]["P0_mean_minus_stored"] = repr(
                        mean - info["stored_val_loss"])
                print(print_tag, label, solver_it, cond, repr(mean),
                      "wall", repr(round(wall, 3)), flush=True)
    return rows, per_cell, first_real_wall


# ---------------------------------------------------------------- tasks
def task_control(a):
    """Brief Sec 6 v3.1, step 1: copy fidelity (five-call floor) + P0 reproduction.  Writes
    nothing."""
    solver = D.build_solver(Path(a.netdir_root))
    import flyvis
    print("CONTROL META", json.dumps({
        "flyvis": flyvis.__version__, "torch": torch.__version__,
        "python": sys.version.split()[0],
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "device": str(flyvis.device), "netdir": str(solver.dir.path),
        "pid": os.getpid(),
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}), flush=True)
    ok = True
    for run in ("000",):
        for ci in sorted(CHKPTS):
            rec, passed = copy_fidelity_control(solver, run, ci)
            print("CONTROL", json.dumps(rec), flush=True)
            ok = ok and passed
    print("CONTROL VERDICT", "PASS" if ok else "FAIL", flush=True)
    return 0 if ok else 3


def task_floor(a):
    """Diagnosis of a --task control failure, added 2026-09-16 after the step-1 gate did not
    pass bitwise at chkpt_00071.  Writes nothing.

    5 repeats of D.per_item_eval (the ORIGINAL, no copy involved) and 5 repeats of the copy with
    the identity transform, interleaved, at both checkpoints of run 000.  If the original's
    repeat-to-repeat spread equals the copy-vs-original spread, the brief's "exactly equal"
    control is unsatisfiable at that checkpoint by a property of the evaluator, not of the copy.
    """
    solver = D.build_solver(Path(a.netdir_root))
    import flyvis
    print("FLOOR META", json.dumps({
        "flyvis": flyvis.__version__, "torch": torch.__version__,
        "python": sys.version.split()[0],
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "device": str(flyvis.device), "pid": os.getpid(),
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}), flush=True)
    for ci in sorted(CHKPTS):
        solver_it, path, info = load_named(solver, "000", ci)
        orig, copy = [], []
        for _ in range(5):
            assert solver.network._state_hooks == ()
            orig.append(np.array(D.per_item_eval(solver)["flow"], dtype=np.float64))
            copy.append(np.array(
                per_item_eval_transformed(solver, make_transform("real"))["flow"],
                dtype=np.float64))
        O = np.stack(orig)
        C = np.stack(copy)

        def spread(M):
            return float(np.max(np.abs(M[:, None, :] - M[None, :, :])))

        def cross(A, B):
            return float(np.max(np.abs(A[:, None, :] - B[None, :, :])))

        rec = {
            "run": "000", "chkpt": path.name, "solver_iteration": solver_it,
            "stored_checkpoint_val_loss": repr(info["stored_val_loss"]),
            "n_repeats_each": 5,
            "original_vs_original_max_abs_per_item": repr(spread(O)),
            "copy_vs_copy_max_abs_per_item": repr(spread(C)),
            "copy_vs_original_max_abs_per_item": repr(cross(C, O)),
            "original_means": [repr(float(x)) for x in O.mean(axis=1)],
            "copy_means": [repr(float(x)) for x in C.mean(axis=1)],
            "original_mean_spread": repr(float(O.mean(axis=1).max() - O.mean(axis=1).min())),
            "copy_mean_spread": repr(float(C.mean(axis=1).max() - C.mean(axis=1).min())),
            "mean_of_means_copy_minus_original": repr(
                float(C.mean() - O.mean())),
            "n_distinct_original_means": len(set(O.mean(axis=1).tolist())),
            "n_distinct_copy_means": len(set(C.mean(axis=1).tolist())),
            "any_copy_bitwise_equal_to_any_original": bool(
                any(np.array_equal(c, o) for c in C for o in O)),
            "n_copy_original_bitwise_pairs": int(
                sum(1 for c in C for o in O if np.array_equal(c, o))),
        }
        print("FLOOR", json.dumps(rec), flush=True)
    return 0


def task_main(a):
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    t_start = time.perf_counter()
    solver = D.build_solver(Path(a.netdir_root))
    import flyvis
    item_names = D.val_item_names(solver)
    assert len(item_names) == 16, item_names
    n2_meta = json.loads(
        (Path(N2_ABL) / "ablation_controls.json").read_text())["meta"]
    assert n2_meta["val_items"] == item_names, "evaluation set differs from night 2"

    meta = {
        "status": STATUS,
        "brief": "docs/briefs/2026-09-16-step1-gray-stimulus.md (v3.1, commit 54823c4)",
        "launch": ("Mike's explicit word in the DPC Research chat, "
                   "2026-09-16T20:14:03Z: «@CC_windows запускай шаг 1»"),
        "script_sha256": SCRIPT_HASHES,
        "flyvis": flyvis.__version__, "torch": torch.__version__,
        "python": sys.version.split()[0],
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "netdir": str(solver.dir.path), "device": str(flyvis.device),
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "pid": os.getpid(),
        "runs": RUNS6, "labels": LABELS6,
        "checkpoints": {CHKPT_NAMES[k]: v for k, v in CHKPTS.items()},
        "checkpoint_index_to_solver_iteration": {str(k): v for k, v in CHKPTS.items()},
        "conditions": CONDITION_DEFS,
        "shuffle_seed": SHUFFLE_SEED,
        "shuffle_derivation": ("numpy.random.default_rng([SHUFFLE_SEED, item_index])"
                               ".permutation(n_frames), item_index = the dataloader "
                               "enumeration index 0..15; identical in every process"),
        "val_items": item_names,
        "batch_size": int(solver.task.val_data.batch_size),
        "dt": float(solver.task.dataset.dt),
        "t_pre": 0.25, "steady_state_value": 0.5, "augmentation": False,
        "ablation_hook_registered": False,
        "copy_note": ("per_item_eval_transformed is a line-for-line copy of "
                      "diag1_eval_paths.py:176-201; only the argument of :191 and the loop "
                      "variable `_`->`_i` on :188 differ"),
    }
    print("META", json.dumps({k: v for k, v in meta.items() if k != "val_items"}), flush=True)

    # ------------------------------------------------------------------ controls (re-run here)
    controls = {}
    ctrl_ok = True
    for run in ("000",):
        for ci in sorted(CHKPTS):
            rec, passed = copy_fidelity_control(solver, run, ci)
            controls[f"{run}@{rec['solver_iteration']}"] = rec
            print("CONTROL", json.dumps(rec), flush=True)
            ctrl_ok = ctrl_ok and passed
    if not ctrl_ok:
        print("CONTROL VERDICT FAIL (in --task main) -- stopping before the sweep; "
              "nothing written", flush=True)
        return 3

    null = constant_output_null(solver)
    print("NULL constant_output_null", null["constant_output_null"],
          "zero_prediction_null", null["zero_prediction_null"], flush=True)

    # ------------------------------------------------------------------ the 48 cells
    rows, per_cell, first_real_wall = sweep(solver, item_names, "CELL")
    assert len(rows) == 48, len(rows)
    write_losses_csv(out / "gray_losses.csv", rows, item_names,
                     SCRIPT_HASHES["results/diagnostics/gray/gray_stimulus.py"])

    # per-item frame permutations actually used (recorded, not assumed)
    perms = {}
    with torch.no_grad():
        with solver.task.dataset.augmentation(False):
            for _i, data in enumerate(solver.task.val_data):
                nf = int(data["lum"].shape[1])
                p = frame_permutation(_i, nf)
                perms[item_short(item_names[_i])] = {
                    "item_index": _i, "n_frames": nf,
                    "permutation": [int(x) for x in p],
                    "is_identity": bool(np.array_equal(p, np.arange(nf)))}

    p0_all = {k: v["P0_mean_minus_stored"] for k, v in per_cell.items()
              if v.get("P0_mean_minus_stored") is not None}
    ctrl = {
        "meta": meta,
        "copy_fidelity_and_P0": controls,
        "constant_output_null": null,
        "P0_mean_minus_stored_all_12_checkpoints": {
            f"{k[0]}@{k[1]}": v for k, v in p0_all.items()},
        "P0_max_abs_mean_minus_stored": repr(
            max(abs(float(v)) for v in p0_all.values())),
        "P0_all_within_1e-4": bool(
            all(abs(float(v)) <= P0_TOL for v in p0_all.values())),
        "frame_permutations": perms,
        "cells": {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in per_cell.items()},
        "n_evaluations": len(rows),
        "first_evaluation_real_wall_s": repr(first_real_wall),
        "wall_s_total": repr(time.perf_counter() - t_start),
    }
    (out / "gray_controls.json").write_text(json.dumps(ctrl, indent=1))
    print("P0 MAX ABS", ctrl["P0_max_abs_mean_minus_stored"],
          "all_within_1e-4", ctrl["P0_all_within_1e-4"], flush=True)
    print("FIRST REAL EVAL WALL S", ctrl["first_evaluation_real_wall_s"], flush=True)
    print("TOTAL WALL S", ctrl["wall_s_total"], flush=True)
    return 0


def task_repeat(a):
    """Brief Sec 6 'Fresh process': all 48 cells again, in a second process."""
    out = Path(a.out_dir)
    t_start = time.perf_counter()
    solver = D.build_solver(Path(a.netdir_root))
    import flyvis
    item_names = D.val_item_names(solver)
    rows, per_cell, first_real_wall = sweep(solver, item_names, "REPEAT")
    assert len(rows) == 48, len(rows)
    write_losses_csv(out / "gray_losses_repeat.csv", rows, item_names,
                     SCRIPT_HASHES["results/diagnostics/gray/gray_stimulus.py"])

    first = read_losses_csv(out / "gray_losses.csv")
    second = read_losses_csv(out / "gray_losses_repeat.csv")
    assert set(first) == set(second), "cell sets differ"
    deltas = {f"{k[0]}|{k[1]}|{k[2]}": second[k]["loss_16"] - first[k]["loss_16"]
              for k in first}
    per_item_max = {f"{k[0]}|{k[1]}|{k[2]}":
                    float(np.max(np.abs(second[k]["per_item"] - first[k]["per_item"])))
                    for k in first}
    worst = max(deltas, key=lambda k: abs(deltas[k]))
    # brief Sec 6 v3: gate per checkpoint against 3 x the in-process floor (16-item mean) of that
    # checkpoint, as measured by copy_fidelity_control in the --task main process
    first_ctrl = json.loads((out / "gray_controls.json").read_text(encoding="utf-8"))
    floors = {}
    for rec in first_ctrl["copy_fidelity_and_P0"].values():
        floors[int(rec["solver_iteration"])] = {
            "run": rec["run"], "chkpt": rec["chkpt"],
            "floor_max_abs_mean_diff_over_10_pairs": float(
                rec["floor_max_abs_mean_diff_over_10_pairs"]),
            "floor_max_abs_per_item_diff_over_10_pairs": float(
                rec["floor_max_abs_per_item_diff_over_10_pairs"])}
    per_ckpt = {}
    for it in sorted(floors):
        keys = [k for k in first if k[1] == it]
        assert len(keys) == 24, (it, len(keys))
        wk = max(keys, key=lambda k: abs(second[k]["loss_16"] - first[k]["loss_16"]))
        mx = abs(second[wk]["loss_16"] - first[wk]["loss_16"])
        thr = FRESH_PROCESS_FLOOR_MULT * floors[it]["floor_max_abs_mean_diff_over_10_pairs"]
        per_ckpt[str(it)] = {
            "in_process_floor_source": {k: (repr(v) if isinstance(v, float) else v)
                                        for k, v in floors[it].items()},
            "gate_threshold_3x_floor": repr(thr),
            "max_abs_delta_loss_16": repr(mx),
            "max_abs_delta_cell": f"{wk[0]}|{wk[1]}|{wk[2]}",
            "n_cells": len(keys),
            "n_cells_bitwise_identical_loss_16": int(sum(
                1 for k in keys if second[k]["loss_16"] == first[k]["loss_16"])),
            "gate_pass_le_3x_floor": bool(mx <= thr),
            "also_le_1e-4": bool(mx <= FRESH_PROCESS_TOL),
        }
    cell_gate = {}
    for k in first:
        d = abs(second[k]["loss_16"] - first[k]["loss_16"])
        thr = FRESH_PROCESS_FLOOR_MULT * floors[k[1]]["floor_max_abs_mean_diff_over_10_pairs"]
        cell_gate[f"{k[0]}|{k[1]}|{k[2]}"] = {
            "abs_delta_loss_16": repr(d), "threshold_3x_floor": repr(thr),
            "pass_le_3x_floor": bool(d <= thr), "pass_le_1e-4": bool(d <= FRESH_PROCESS_TOL)}
    rep = {
        "status": STATUS,
        "script_sha256": SCRIPT_HASHES,
        "pid": os.getpid(),
        "flyvis": flyvis.__version__, "torch": torch.__version__,
        "python": sys.version.split()[0],
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "gate": ("brief Sec 6 v3: per checkpoint, max |delta loss_16| between the two processes "
                 "<= 3 x the in-process floor of that checkpoint on the 16-item mean (max over "
                 "10 pairs of five D.per_item_eval calls on run 000, gray_controls.json); "
                 "<= 1e-4 reported separately"),
        "per_checkpoint": per_ckpt,
        "per_cell_gate": cell_gate,
        "max_abs_delta_loss_16": repr(max(abs(v) for v in deltas.values())),
        "max_abs_delta_cell": worst,
        "n_cells_bitwise_identical_loss_16": int(sum(1 for v in deltas.values() if v == 0.0)),
        "max_abs_per_item_delta": repr(max(per_item_max.values())),
        "gate_pass": bool(all(v["gate_pass_le_3x_floor"] for v in per_ckpt.values())),
        "also_all_le_1e-4": bool(max(abs(v) for v in deltas.values()) <= FRESH_PROCESS_TOL),
        "delta_loss_16_per_cell": {k: repr(v) for k, v in deltas.items()},
        "max_abs_per_item_delta_per_cell": {k: repr(v) for k, v in per_item_max.items()},
        "first_evaluation_real_wall_s": repr(first_real_wall),
        "wall_s_total": repr(time.perf_counter() - t_start),
    }
    (out / "gray_repeat_controls.json").write_text(json.dumps(rep, indent=1))
    print("REPEAT MAX ABS DELTA", rep["max_abs_delta_loss_16"], rep["max_abs_delta_cell"],
          "gate_pass", rep["gate_pass"], "also_all_le_1e-4", rep["also_all_le_1e-4"], flush=True)
    print("REPEAT PER CHECKPOINT", json.dumps(per_ckpt), flush=True)
    print("TOTAL WALL S", rep["wall_s_total"], flush=True)
    return 0


# ---------------------------------------------------------------- the pre-registered readings
def reading_ii_text(cls_gray, cls_zero):
    """Brief Sec 7 (ii) branches, verbatim; 'between' and 'returns' both count as not exploding."""
    expl_gray = cls_gray == "explodes"
    expl_zero = cls_zero == "explodes"
    if expl_gray and expl_zero:
        return "fragility to absence of drive is real"
    if not expl_gray and not expl_zero:
        return ("explosion only under the ablation's forced-zero state, i.e. neither (a) nor (b) "
                "explode -> the ablation deltas -- +21,158 (R2 single-type clamp-to-0) and "
                "+30,626 (full R1-R8 clamp-to-0) -- measure the dynamics' fragility to a zero "
                "clamp specifically, an instrument artefact, not a vision dependence, and the R2 "
                "ablation finding must be reworded accordingly")
    return ("only one of (a) gray and (b) zero explodes -- neither pre-registered branch "
            "applies; recorded as measured, no branch selected")


def task_readings(a):
    """Brief Sec 7, evaluated mechanically from gray_losses.csv.  No GPU, no interpretation."""
    out = Path(a.out_dir)
    f = read_losses_csv(out / "gray_losses.csv")
    U, T = 0, 250008                     # untrained / trained solver iterations

    def L(label, it, cond):
        return f[(label, it, cond)]["loss_16"]

    readings = {
        "status": STATUS,
        "script_sha256": SCRIPT_HASHES,
        "source": "gray_losses.csv (this directory)",
        "rule_source": "docs/briefs/2026-09-16-step1-gray-stimulus.md Sec 7, verbatim",
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "band_fraction": BAND_FRACTION,
        "per_seed": {},
    }
    for lab in LABELS6:
        gain = L(lab, U, "real") - L(lab, T, "real")
        band = BAND_FRACTION * gain
        d_i = L(lab, T, "gray") - L(lab, U, "gray")
        holds_i = bool(abs(d_i) <= band)
        d_iii_real = L(lab, T, "shuffled") - L(lab, T, "real")
        d_iii_gray = L(lab, T, "shuffled") - L(lab, U, "gray")
        near_real = bool(abs(d_iii_real) <= band)
        near_gray = bool(abs(d_iii_gray) <= band)
        # brief Sec 7 (iii) v3: exclusive branches; void when the two references lie within
        # 0.2 * gain_s of each other
        ref_sep = L(lab, T, "real") - L(lab, U, "gray")
        void_iii = bool(abs(ref_sep) <= VOID_FRACTION * gain)
        nearer = "L_trained_real" if abs(d_iii_real) <= abs(d_iii_gray) else "L_untrained_gray"
        if void_iii:
            text_iii = ("between -- void for this seed (the two references lie within "
                        "0.2 * gain_s of each other)")
        elif near_real and not near_gray:
            text_iii = "not about motion"
        elif near_gray and not near_real:
            text_iii = "about temporal content"
        else:
            text_iii = "between"
        # brief Sec 7 (ii) v3, computed for every seed (the pre-registered reading is seed 2)
        ii = {}
        for cond in ("gray", "zero"):
            exc = L(lab, T, cond) - L(lab, U, "gray")
            if exc >= EXPLODE_MULT * gain:
                cls = "explodes"
            elif exc <= RETURN_FRACTION * gain:
                cls = "returns"
            else:
                cls = "between"
            ii[cond] = {"L_trained": repr(L(lab, T, cond)),
                        "excess_over_untrained_gray": repr(exc),
                        "excess_in_units_of_gain_s": repr(exc / gain),
                        "class": cls}
        readings["per_seed"][lab] = {
            "L_untrained_real": repr(L(lab, U, "real")),
            "L_trained_real": repr(L(lab, T, "real")),
            "L_untrained_gray": repr(L(lab, U, "gray")),
            "L_trained_gray": repr(L(lab, T, "gray")),
            "L_untrained_zero": repr(L(lab, U, "zero")),
            "L_trained_zero": repr(L(lab, T, "zero")),
            "L_untrained_shuffled": repr(L(lab, U, "shuffled")),
            "L_trained_shuffled": repr(L(lab, T, "shuffled")),
            "gain_s": repr(gain),
            "band_0.1_gain_s": repr(band),
            "reading_i_delta_trained_gray_minus_untrained_gray": repr(d_i),
            "reading_i_abs_delta": repr(abs(d_i)),
            "reading_i_holds": holds_i,
            "reading_i_text": ("gray removes >= 90% of the learned gain"
                               if holds_i else
                               "gray does NOT remove >= 90% of the learned gain "
                               "(|L_trained_gray - L_untrained_gray| > 0.1 * gain_s)"),
            "control_untrained_gray_minus_untrained_real": repr(
                L(lab, U, "gray") - L(lab, U, "real")),
            "reading_iii_delta_to_trained_real": repr(d_iii_real),
            "reading_iii_delta_to_untrained_gray": repr(d_iii_gray),
            "reading_iii_within_band_of_trained_real": near_real,
            "reading_iii_within_band_of_untrained_gray": near_gray,
            "reading_iii_reference_separation_trained_real_minus_untrained_gray": repr(ref_sep),
            "reading_iii_void_threshold_0.2_gain_s": repr(VOID_FRACTION * gain),
            "reading_iii_void": void_iii,
            "reading_iii_nearer_reference": nearer,
            "reading_iii_text": text_iii,
            "reading_ii_excess_explodes_threshold_10_gain_s": repr(EXPLODE_MULT * gain),
            "reading_ii_excess_returns_threshold_0.1_gain_s": repr(RETURN_FRACTION * gain),
            "reading_ii_a_gray": ii["gray"],
            "reading_ii_b_zero": ii["zero"],
            "reading_ii_text": reading_ii_text(ii["gray"]["class"], ii["zero"]["class"]),
        }

    # ---- reading (ii): seed 2, on (a) gray and (b) zero separately (brief Sec 7 (ii) v3)
    p2 = readings["per_seed"]["seed2"]
    readings["reading_ii_seed2"] = {
        "definition": ("excess_cond(s) = L_trained,cond(s) - L_untrained_gray(s), cond in "
                       "{gray, zero}; >= 10 * gain_s -> explodes; <= 0.1 * gain_s -> returns; "
                       "otherwise between (brief Sec 7 (ii) v3, pre-registered at the gate stop)"),
        "seed2_L_untrained_gray": p2["L_untrained_gray"],
        "seed2_L_trained_real": p2["L_trained_real"],
        "seed2_gain_s": p2["gain_s"],
        "explodes_threshold_10_gain_s": p2["reading_ii_excess_explodes_threshold_10_gain_s"],
        "returns_threshold_0.1_gain_s": p2["reading_ii_excess_returns_threshold_0.1_gain_s"],
        "a_gray": p2["reading_ii_a_gray"],
        "b_zero": p2["reading_ii_b_zero"],
        "other_five_trained_real": {lab: repr(L(lab, T, "real"))
                                    for lab in LABELS6 if lab != "seed2"},
        "prereg_reference_R2_single_type_clamp_delta_16": PREREG_SEED2_R2_DELTA,
        "prereg_reference_R1_R8_clamp_excess": PREREG_SEED2_R1R8_CLAMP_EXCESS,
        "reading_ii_text": p2["reading_ii_text"],
    }
    readings["reading_i_summary"] = {
        "n_seeds_holding": int(sum(1 for lab in LABELS6
                                   if readings["per_seed"][lab]["reading_i_holds"])),
        "seeds_holding": [lab for lab in LABELS6
                          if readings["per_seed"][lab]["reading_i_holds"]],
    }
    readings["reading_iii_summary"] = {
        lab: readings["per_seed"][lab]["reading_iii_text"] for lab in LABELS6}
    (out / "gray_readings.json").write_text(json.dumps(readings, indent=1))
    for lab in LABELS6:
        p = readings["per_seed"][lab]
        print("READING_I", lab, "gain", p["gain_s"], "band", p["band_0.1_gain_s"],
              "|delta|", p["reading_i_abs_delta"], "holds", p["reading_i_holds"], flush=True)
    for lab in LABELS6:
        p = readings["per_seed"][lab]
        print("READING_III", lab, "d_real", p["reading_iii_delta_to_trained_real"],
              "d_untrained_gray", p["reading_iii_delta_to_untrained_gray"],
              "->", p["reading_iii_text"], flush=True)
    for lab in LABELS6:
        p = readings["per_seed"][lab]
        print("READING_II", lab, "gray", json.dumps(p["reading_ii_a_gray"]),
              "zero", json.dumps(p["reading_ii_b_zero"]), flush=True)
    print("READING_II_SEED2", json.dumps(readings["reading_ii_seed2"]), flush=True)
    return 0


def main():
    a = parse_args()
    return {"control": task_control, "floor": task_floor, "main": task_main,
            "repeat": task_repeat, "readings": task_readings}[a.task](a)


if __name__ == "__main__":
    sys.exit(main())
