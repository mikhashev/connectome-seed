"""Row B -- per-cell-type activity profiles of the saved checkpoints.

PREVIEW DIAGNOSTIC, NOT A TEST.  n = 4 individuals; critical rho at N = 4-5 is 0.90-1.00
(docs/proposals/mi-axis-per-cell-type-design.md Sec 6).  No number produced by this script may
be read as a test, today or later.  The label is written into every output json.

Design: docs/proposals/mi-axis-per-cell-type-design.md (Ark 2026-09-15 08:09 + Addendum 08:13).
Mike's word «do row B» (translated from Russian), 2026-09-15 09:56.  The protocol is fixed in README.md Sec 1-8, which
was written and saved before this script was run for the first time.

WHAT THIS SCRIPT DOES NOT DO: it never trains, never writes into
connectome-seed-data/results/flow/9991/*, and never calls solver.checkpoint() or
solver.test(track_loss=True).  The solver lives in a scratch datamate root; the four runs'
checkpoints are read with torch.load only.  The recording hook returns the state it was given,
unchanged.

The evaluator is REUSED from ../diag1_eval_paths.py (build_solver, chkpt_table, load_checkpoint,
per_item_eval, val_item_names) and the ablation hook from ../ablation/ablation.py -- nothing
about the evaluation path is re-implemented here.  The only thing this script adds is a READ-ONLY
state hook that accumulates per-cell-type activity, and a forward pre-hook on the Network module
that marks item boundaries (phase 0 = the steady state, phases 1..16 = the 16 held-out items).
"""

import os
import sys

# Same two environment variables, set the same way and in the same place as
# night/run_individual.py:46-49, diag1_eval_paths.py:27-32 and ablation.py:22-26.
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
os.environ.setdefault(
    "FLYVIS_ROOT_DIR", "C:/Users/mikha/Documents/dpc-research/connectome-seed-data"
)

DIAG_DIR = "C:/Users/mikha/Documents/dpc-research/connectome-seed/results/night2/diagnostics"
sys.path.insert(0, DIAG_DIR)
sys.path.insert(0, os.path.join(DIAG_DIR, "ablation"))

import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np
import torch

import diag1_eval_paths as D  # the evaluator, reused verbatim
import ablation as ABL  # the ablation hook and the rank statistics, reused verbatim

RUNS = D.RUNS  # {"000": "seed0", "900": "seed0prime", "001": "seed1", "002": "seed2"}
LABELS = ["seed0", "seed0prime", "seed1", "seed2"]
PAIRS = [("seed0", "seed0prime"), ("seed0", "seed1"), ("seed0", "seed2"),
         ("seed1", "seed2"), ("seed0prime", "seed1"), ("seed0prime", "seed2")]
FOREIGN = [p for p in PAIRS if p != ("seed0", "seed0prime")]

# checkpoint index -> solver iteration (README Sec 3); verified at run time against chkpt_table
NAMED_CHKPTS = {0: 0, 8: 25212, 71: 250008}

STATUS = "PREVIEW DIAGNOSTIC -- NOT A TEST (n=4, critical rho 0.90-1.00)"
PURITY_TOL = 1e-4  # README Sec 2


def script_sha256():
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--task", required=True,
                   choices=["profiles", "repro", "p2", "traj", "analyze"])
    p.add_argument("--out-dir", required=True)
    p.add_argument("--scratch-dir", required=True)
    p.add_argument("--netdir-root", required=False)
    p.add_argument("--rep", type=int, default=0, help="label for --task repro")
    return p.parse_args()


# ---------------------------------------------------------------- duplicate key = refusal
class NoDupDict(dict):
    """Hardening item 12: a duplicate key is a refusal, never 'the latest one wins'."""

    def __setitem__(self, k, v):
        if k in self:
            raise KeyError(f"duplicate key {k!r} -- refusing (README Sec 8)")
        super().__setitem__(k, v)


def read_csv_nodup(path, key_cols):
    """CSV reader that refuses a duplicate key instead of overwriting it."""
    lines = [ln for ln in Path(path).read_text(encoding="utf-8").strip().split("\n")
             if not ln.startswith("#")]
    hdr = lines[0].split(",")
    out = NoDupDict()
    for ln in lines[1:]:
        parts = ln.split(",")
        assert len(parts) == len(hdr), (path, len(parts), len(hdr))
        row = dict(zip(hdr, parts))
        out[tuple(row[c] for c in key_cols)] = row
    return out


# ---------------------------------------------------------------- the read-only recorder
class Recorder:
    """Accumulates per-cell-type mean and std of state.nodes.activity at every Euler step.

    The state hook is called from Network._state_api (flyvis/network/network.py:430-433) -- the
    same site the ablation clamps at.  This hook READS and returns the state object it was
    given, unchanged (no attribute of `state` is assigned).

    Phases are marked by a forward pre-hook on the Network module: per_item_eval
    (diag1_eval_paths.py:200-225) calls network.steady_state() once (phase 0) and then
    network(...) once per item (phases 1..16), so the phase index is the item index.
    """

    def __init__(self, type_index, counts, n_types):
        self.type_index = type_index          # (n_nodes,) int64 on device
        self.counts = counts                  # (n_types,) float64 on device
        self.n_types = n_types
        self.phase = -1
        self.cur = None
        self.phases = []                      # list of (T, n_types) float64 arrays: means
        self.phases_std = []
        self.n_calls = 0

    def new_phase(self, *a, **kw):
        self._flush()
        self.phase += 1
        self.cur = ([], [])

    def _flush(self):
        if self.cur is not None:
            m = torch.stack(self.cur[0]).double().cpu().numpy()
            s = torch.stack(self.cur[1]).double().cpu().numpy()
            self.phases.append(m)
            self.phases_std.append(s)
        self.cur = None

    def finish(self):
        self._flush()
        return self.phases, self.phases_std

    def hook(self, state):
        x = state.nodes.activity
        assert x.shape[0] == 1, x.shape          # batch 1 (README Sec 2)
        v = x[0].detach().double()
        s1 = torch.zeros(self.n_types, dtype=torch.float64, device=v.device)
        s2 = torch.zeros(self.n_types, dtype=torch.float64, device=v.device)
        s1.index_add_(0, self.type_index, v)
        s2.index_add_(0, self.type_index, v * v)
        mean = s1 / self.counts
        var = torch.clamp(s2 / self.counts - mean * mean, min=0.0)
        if self.cur is None:                      # a forward outside the marked phases
            self.new_phase()
        self.cur[0].append(mean)
        self.cur[1].append(torch.sqrt(var))
        self.n_calls += 1
        return state                              # unchanged


# ---------------------------------------------------------------- the seven invariants
def snapshot_state(solver):
    net = solver.network
    ds = solver.task.dataset
    sch = solver.scheduler
    pen = []
    try:
        pen = [g["lr"] for o in solver.penalty.optimizers.values()
               if o is not None for g in o.param_groups]
    except Exception as e:  # noqa: BLE001
        pen = [repr(e)]
    return {
        "lr": [g["lr"] for g in solver.optimizer.param_groups],
        "pen_lr": pen,
        "dt": float(ds.dt),
        "sched_iter": getattr(sch, "_current_iteration", None),
        "training": (bool(net.training),
                     [bool(d.training) for d in solver.decoder.values()]),
        "augment": bool(ds.augment),
    }


def invariants(before, after):
    """The seven post-evaluation invariants of eval_rung (run_individual.py:550-558),
    recorded verbatim (hardening item 1)."""
    return {
        "lr_unchanged": bool(before["lr"] == after["lr"]),
        "pen_lr_unchanged": bool(before["pen_lr"] == after["pen_lr"]),
        "dt_unchanged": bool(before["dt"] == after["dt"]),
        "scheduler_iter_unchanged": bool(before["sched_iter"] == after["sched_iter"]),
        "back_in_train_mode": bool(after["training"][0] and all(after["training"][1])),
        "was_in_train_mode_before": bool(before["training"][0] and all(before["training"][1])),
        "dataset_augment_restored": bool(after["augment"]) is True,
    }


# ---------------------------------------------------------------- one evaluation with row B
def eval_rowB(solver, rec_ctx, extra_hook=None, extra_kwargs=None):
    """One 16-item evaluation with the recorder attached.

    Returns (per_item_losses, means, stds, invariants, n_hook_calls).
    `means[p]` is a (T_p, 65) array for phase p (0 = steady state, 1..16 = items).
    """
    net = solver.network
    assert net._state_hooks == (), net._state_hooks     # README Sec 2
    rec = Recorder(*rec_ctx)
    if extra_hook is not None:
        net.register_state_hook(extra_hook, **(extra_kwargs or {}))
    net.register_state_hook(rec.hook)
    ph = net.register_forward_pre_hook(rec.new_phase)
    before = snapshot_state(solver)
    try:
        losses = D.per_item_eval(solver)
    finally:
        ph.remove()
        net.clear_state_hooks()
    after = snapshot_state(solver)
    assert net._state_hooks == ()
    means, stds = rec.finish()
    return (np.array(losses["flow"], dtype=np.float64), means, stds,
            invariants(before, after), rec.n_calls)


def summarise(means, stds, n_items=16):
    """Phases 1..16 -> per-item summaries.  Primary = mean over the whole simulation window;
    secondary = the value at the last step (README Sec 1)."""
    assert len(means) == n_items + 1, len(means)      # phase 0 = steady state
    mw = np.stack([m.mean(axis=0) for m in means[1:]])        # (16, 65)
    ls = np.stack([m[-1] for m in means[1:]])                 # (16, 65)
    sw = np.stack([s.mean(axis=0) for s in stds[1:]])         # (16, 65)
    sl = np.stack([s[-1] for s in stds[1:]])                  # (16, 65)
    return {"mean_window": mw, "last_step": ls, "std_window": sw, "std_last_step": sl,
            "steps_per_item": [int(m.shape[0]) for m in means[1:]],
            "steps_steady_state": int(means[0].shape[0])}


# ---------------------------------------------------------------- setup shared by all tasks
def setup(a):
    netroot = Path(a.netdir_root) if a.netdir_root else \
        Path(a.scratch_dir) / f"netdir_{a.task}_{a.rep}"
    solver = D.build_solver(netroot)
    import flyvis

    net = solver.network
    device = flyvis.device
    types_arr = ABL.node_type_array(net)
    unique_types = list(dict.fromkeys(types_arr.tolist()))
    assert len(unique_types) == 65, len(unique_types)
    t2i = {t: i for i, t in enumerate(unique_types)}
    type_index = torch.as_tensor(np.array([t2i[t] for t in types_arr]),
                                 dtype=torch.long, device=device)
    counts = torch.as_tensor(
        np.array([float((types_arr == t).sum()) for t in unique_types]),
        dtype=torch.float64, device=device)
    item_names = D.val_item_names(solver)
    assert len(item_names) == 16, item_names
    bs = solver.task.val_data.batch_size
    assert bs == 1, bs
    input_types = [x.decode() if isinstance(x, bytes) else str(x)
                   for x in net.connectome.input_cell_types[:]]
    meta = {
        "status": STATUS,
        "script_sha256": script_sha256(),
        "script": "rowB.py",
        "task": a.task,
        "flyvis": flyvis.__version__, "torch": torch.__version__,
        "python": sys.version.split()[0],
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "netdir": str(solver.dir.path), "device": str(device),
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "pid": os.getpid(),
        "quantity": "state.nodes.activity read (not modified) in Network._state_api "
                    "(flyvis/network/network.py:430-433)",
        "primary_summary": "mean over the whole simulation window, all 65 types",
        "secondary_summary": "value at the last simulation step",
        "measure": "Spearman rho over the 65 types; distance = 1 - rho",
        "n_nodes": int(net.n_nodes), "n_types": 65, "types": unique_types,
        "type_counts": {t: int((types_arr == t).sum()) for t in unique_types},
        "input_cell_types": input_types,
        "val_items": item_names,
        "batch_size": int(bs),
        "dt": float(solver.task.dataset.dt),
    }
    return solver, device, types_arr, unique_types, (type_index, counts, 65), item_names, \
        input_types, meta


def load_named(solver, run, chkpt_index):
    tab = D.chkpt_table(run)
    hit = [r for r in tab if r[0] == chkpt_index]
    assert len(hit) == 1, (run, chkpt_index)
    ci, stored_it, solver_it, path = hit[0]
    if chkpt_index in NAMED_CHKPTS:
        assert solver_it == NAMED_CHKPTS[chkpt_index], (chkpt_index, solver_it)
    info = D.load_checkpoint(solver, path)
    return solver_it, info


def item_short(n):
    return n.replace("sequence_", "")


# ---------------------------------------------------------------- csv writers
def write_profile_csv(path, blocks, unique_types, item_names, sha, iteration):
    hdr = (["run", "label", "chkpt_iteration", "type",
            "mean_window", "last_step", "std_window", "std_last_step"]
           + [f"mean_window_item_{item_short(n)}" for n in item_names])
    lines = ["# " + STATUS,
             f"# script_sha256={sha} chkpt_iteration={iteration} "
             f"primary=mean_window(aggregate over the 16 items)",
             ",".join(hdr)]
    for run, label in RUNS.items():
        b = blocks[label]
        for i, T in enumerate(unique_types):
            row = [run, label, str(iteration), T,
                   repr(float(b["mean_window"][:, i].mean())),
                   repr(float(b["last_step"][:, i].mean())),
                   repr(float(b["std_window"][:, i].mean())),
                   repr(float(b["std_last_step"][:, i].mean()))]
            row += [repr(float(x)) for x in b["mean_window"][:, i]]
            lines.append(",".join(row))
    Path(path).write_text("\n".join(lines) + "\n")


# ---------------------------------------------------------------- statistics (reused)
spearman = ABL.spearman
pearson = ABL.pearson


# ================================================================ tasks
def task_profiles(a, out, scratch):
    solver, device, types_arr, unique_types, rec_ctx, item_names, input_types, meta = setup(a)
    t0 = time.perf_counter()
    records = {"meta": meta, "checkpoints": {}}
    npz_store = {}
    for ci, iteration in sorted(NAMED_CHKPTS.items(), key=lambda kv: kv[1]):
        blocks = NoDupDict()
        block_rec = NoDupDict()
        for run, label in RUNS.items():
            solver_it, info = load_named(solver, run, ci)
            # purity: the same evaluation without the recorder
            before = snapshot_state(solver)
            plain = np.array(D.per_item_eval(solver)["flow"], dtype=np.float64)
            inv_plain = invariants(before, snapshot_state(solver))
            # floor for the per-item comparison: the same state, no hook, evaluated twice
            plain2 = np.array(D.per_item_eval(solver)["flow"], dtype=np.float64)
            t1 = time.perf_counter()
            li, means, stds, inv, ncalls = eval_rowB(solver, rec_ctx)
            wall = time.perf_counter() - t1
            s = summarise(means, stds)
            blocks[label] = s
            block_rec[label] = {
                "run": run, "chkpt_index": ci, "solver_iteration": solver_it,
                "stored_checkpoint_val_loss": repr(info["stored_val_loss"]),
                "per_item_mean_with_hook": repr(float(li.mean())),
                "per_item_mean_without_hook": repr(float(plain.mean())),
                "purity_abs_diff_of_the_16_item_loss": repr(
                    float(abs(li.mean() - plain.mean()))),
                "purity_tol": PURITY_TOL,
                "purity_pass": bool(abs(li.mean() - plain.mean()) < PURITY_TOL),
                "purity_bitwise_identical_per_item": bool(np.array_equal(li, plain)),
                "per_item_max_abs_diff_hook_vs_nohook": repr(
                    float(np.max(np.abs(li - plain)))),
                "per_item_max_abs_diff_nohook_vs_nohook_FLOOR": repr(
                    float(np.max(np.abs(plain2 - plain)))),
                "per_item_max_abs_diff_hook_vs_nohook_in_float32_ulps": repr(
                    float(np.max(np.abs(li - plain)) /
                          float(np.spacing(np.float32(np.max(np.abs(plain))))))),
                "nohook_vs_nohook_abs_diff_of_the_16_item_loss": repr(
                    float(abs(plain2.mean() - plain.mean()))),
                "eval_rung_invariants_with_hook": inv,
                "eval_rung_invariants_without_hook": inv_plain,
                "n_state_hook_calls": ncalls,
                "steps_steady_state": s["steps_steady_state"],
                "steps_per_item": s["steps_per_item"],
                "eval_wall_s": round(wall, 3),
            }
            assert block_rec[label]["purity_pass"], block_rec[label]
            assert all(inv.values()), inv
            print("ROWB", iteration, label, "loss", repr(float(li.mean())),
                  "purity(16-item)", block_rec[label]["purity_abs_diff_of_the_16_item_loss"],
                  "per-item hook", block_rec[label]["per_item_max_abs_diff_hook_vs_nohook"],
                  "per-item floor",
                  block_rec[label]["per_item_max_abs_diff_nohook_vs_nohook_FLOOR"],
                  flush=True)
            for k in ("mean_window", "last_step", "std_window", "std_last_step"):
                npz_store[f"{label}_{iteration}_{k}"] = s[k]
            # row C-in-time, saved whole (README Sec 3)
            for p, m in enumerate(means):
                npz_store[f"ts_{label}_{iteration}_phase{p}_mean"] = m
        records["checkpoints"][str(iteration)] = dict(block_rec)
        tag = "iter0" if iteration == 0 else str(iteration)
        write_profile_csv(out / f"rowB_profiles_{tag}.csv", blocks, unique_types,
                          item_names, meta["script_sha256"], iteration)
    npz_store["_types"] = np.array(unique_types)
    npz_store["_items"] = np.array(item_names)
    np.savez_compressed(out / "rowB_timeseries.npz", **npz_store)
    records["wall_s_total"] = round(time.perf_counter() - t0, 1)
    (out / "rowB_eval_records.json").write_text(json.dumps(records, indent=1))
    print("PROFILES DONE", records["wall_s_total"])
    return 0


def task_repro(a, out, scratch):
    """Reproducibility floor: seed 0 @ 250,008, one fresh process per --rep."""
    solver, device, types_arr, unique_types, rec_ctx, item_names, input_types, meta = setup(a)
    solver_it, info = load_named(solver, "000", 71)
    li, means, stds, inv, ncalls = eval_rowB(solver, rec_ctx)
    s = summarise(means, stds)
    rec = {"meta": meta, "rep": a.rep, "pid": os.getpid(),
           "run": "000", "label": "seed0", "solver_iteration": solver_it,
           "stored_checkpoint_val_loss": repr(info["stored_val_loss"]),
           "per_item_mean": repr(float(li.mean())),
           "eval_rung_invariants": inv, "n_state_hook_calls": ncalls,
           "mean_window_aggregate": {T: repr(float(s["mean_window"][:, i].mean()))
                                     for i, T in enumerate(unique_types)},
           "last_step_aggregate": {T: repr(float(s["last_step"][:, i].mean()))
                                   for i, T in enumerate(unique_types)}}
    assert all(inv.values()), inv
    (Path(scratch) / f"rowB_repro_proc{a.rep}.json").write_text(json.dumps(rec, indent=1))
    print("REPRO", a.rep, "loss", repr(float(li.mean())))
    return 0


def task_p2(a, out, scratch):
    """P2 sanity: silence R1-R8 with the ablation hook; B of downstream types must move."""
    solver, device, types_arr, unique_types, rec_ctx, item_names, input_types, meta = setup(a)
    rec = {"meta": meta, "ablated_types": input_types, "runs": NoDupDict()}
    mask = ABL.make_mask(types_arr, set(input_types), device)
    for run, label in RUNS.items():
        solver_it, info = load_named(solver, run, 71)
        li_b, m_b, s_b, inv_b, _ = eval_rowB(solver, rec_ctx)
        li_p, m_p, s_p, inv_p, _ = eval_rowB(solver, rec_ctx,
                                             extra_hook=ABL.ablate_hook, extra_kwargs={"mask": mask})
        B0 = summarise(m_b, s_b)["mean_window"].mean(axis=0)
        B2 = summarise(m_p, s_p)["mean_window"].mean(axis=0)
        d = B2 - B0
        down = [i for i, T in enumerate(unique_types) if T not in set(input_types)]
        order = np.argsort(-np.abs(d))
        order_down = [i for i in order if i in set(down)]
        rec["runs"][label] = {
            "run": run, "solver_iteration": solver_it,
            "base_loss_16": repr(float(li_b.mean())),
            "ablated_loss_16": repr(float(li_p.mean())),
            "loss_delta": repr(float(li_p.mean() - li_b.mean())),
            "eval_rung_invariants_base": inv_b, "eval_rung_invariants_ablated": inv_p,
            "max_abs_deltaB": repr(float(np.max(np.abs(d)))),
            "n_types_moved_gt_1e-3": int((np.abs(d) > 1e-3).sum()),
            "top10_changed_types": [[unique_types[i], repr(float(d[i])),
                                     repr(float(B0[i])), repr(float(B2[i]))]
                                    for i in order[:10]],
            "top10_changed_downstream_types": [[unique_types[i], repr(float(d[i])),
                                                repr(float(B0[i])), repr(float(B2[i]))]
                                               for i in order_down[:10]],
            "spearman_B_base_vs_ablated": repr(spearman(B0, B2)),
        }
        print("P2", label, json.dumps({k: v for k, v in rec["runs"][label].items()
                                       if not k.startswith("top10")}), flush=True)
    rec["runs"] = dict(rec["runs"])
    (Path(scratch) / "rowB_p2.json").write_text(json.dumps(rec, indent=1))
    return 0


def task_traj(a, out, scratch):
    """Row C: row B at all 72 checkpoints of each run, aggregate over the 16 items."""
    solver, device, types_arr, unique_types, rec_ctx, item_names, input_types, meta = setup(a)
    t0 = time.perf_counter()
    hdr = ["run", "label", "chkpt_index", "iteration", "per_item_mean_loss"] + list(unique_types)
    lines = ["# " + STATUS,
             f"# script_sha256={meta['script_sha256']} "
             f"value=mean_window aggregated over the 16 held-out items",
             ",".join(hdr)]
    seen = NoDupDict()
    inv_all = True
    for run, label in RUNS.items():
        tab = D.chkpt_table(run)
        assert len(tab) == 72, len(tab)
        for ci, stored_it, solver_it, path in tab:
            D.load_checkpoint(solver, path)
            li, means, stds, inv, _ = eval_rowB(solver, rec_ctx)
            inv_all = inv_all and all(inv.values())
            assert all(inv.values()), (label, ci, inv)
            v = summarise(means, stds)["mean_window"].mean(axis=0)
            seen[(label, ci)] = True
            lines.append(",".join([run, label, str(ci), str(solver_it),
                                   repr(float(li.mean()))]
                                  + [repr(float(x)) for x in v]))
            print("TRAJ", label, ci, solver_it, repr(float(li.mean())), flush=True)
    (out / "rowC_trajectory.csv").write_text("\n".join(lines) + "\n")
    (Path(scratch) / "rowC_meta.json").write_text(json.dumps(
        {"meta": meta, "n_rows": len(seen), "all_invariants_pass": bool(inv_all),
         "wall_s_total": round(time.perf_counter() - t0, 1)}, indent=1))
    print("TRAJ DONE", round(time.perf_counter() - t0, 1))
    return 0


# ---------------------------------------------------------------- analysis (no GPU)
def load_profile_csv(path, item_names=None):
    rows = read_csv_nodup(path, ("label", "type"))
    labels, types = [], []
    for (lab, T) in rows:
        if lab not in labels:
            labels.append(lab)
        if T not in types:
            types.append(T)
    assert len(types) == 65, len(types)
    out = {}
    per_item = {}
    for lab in labels:
        out[lab] = {k: np.array([float(rows[(lab, T)][k]) for T in types])
                    for k in ("mean_window", "last_step", "std_window", "std_last_step")}
        cols = [c for c in rows[(lab, types[0])] if c.startswith("mean_window_item_")]
        per_item[lab] = np.array([[float(rows[(lab, T)][c]) for T in types] for c in cols])
    return types, labels, out, per_item, [c[len("mean_window_item_"):] for c in cols]


def task_analyze(a, out, scratch):
    sha = script_sha256()
    base = {"status": STATUS, "script_sha256": sha, "script": "rowB.py",
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "measure": "Spearman rho over the 65 types; distance = 1 - rho",
            "primary_summary": "mean over the whole simulation window, all 65 types",
            "item_composition": "all 16 (primary); 13 without ambush_2 and 10 without "
                                "bandage_1 are context only"}
    types, labels, P250, PI250, item_cols = load_profile_csv(out / "rowB_profiles_250008.csv")
    _, _, P25, PI25, _ = load_profile_csv(out / "rowB_profiles_25212.csv")
    _, _, P0, PI0, _ = load_profile_csv(out / "rowB_profiles_iter0.csv")
    idx13 = [i for i, n in enumerate(item_cols) if "ambush_2" not in n]
    idx10 = [i for i, n in enumerate(item_cols)
             if "ambush_2" not in n and "bandage_1" not in n]
    assert len(idx13) == 13 and len(idx10) == 10

    # ---------------- controls
    repro = []
    for r in (1, 2, 3):
        p = Path(scratch) / f"rowB_repro_proc{r}.json"
        repro.append(json.loads(p.read_text()))
    rkeys = list(repro[0]["mean_window_aggregate"].keys())
    assert rkeys == types, "type order differs between repro and csv"
    RV = [np.array([float(x["mean_window_aggregate"][T]) for T in types]) for x in repro]
    rho_pairs = {f"proc{i+1}|proc{j+1}": spearman(RV[i], RV[j])
                 for i in range(3) for j in range(i + 1, 3)}
    dB_pairs = {f"proc{i+1}|proc{j+1}": float(np.max(np.abs(RV[i] - RV[j])))
                for i in range(3) for j in range(i + 1, 3)}
    floor_rho = float(max(1.0 - r for r in rho_pairs.values()))
    floor_dB = float(max(dB_pairs.values()))

    # P0 graduated ladder at iteration 0
    ladder = {}
    for x, y in PAIRS:
        v = P0[x]["mean_window"], P0[y]["mean_window"]
        ladder[f"{x}|{y}"] = {
            "spearman_rho": repr(spearman(*v)),
            "distance_1_minus_rho": repr(1.0 - spearman(*v)),
            "max_abs_deltaB": repr(float(np.max(np.abs(v[0] - v[1])))),
            "bitwise_identical": bool(np.array_equal(v[0], v[1])),
        }
    p2 = json.loads((Path(scratch) / "rowB_p2.json").read_text())
    controls = dict(base)
    controls["P0_ladder_iteration_0"] = ladder
    controls["P0_ladder_250008_for_contrast"] = {
        f"{x}|{y}": repr(1.0 - spearman(P250[x]["mean_window"], P250[y]["mean_window"]))
        for x, y in PAIRS}
    controls["floor"] = {
        "what": "same checkpoint (seed 0, 250,008) evaluated in 3 fresh processes; "
                "measured for THIS metric at THIS state, not inherited (rule R1)",
        "spearman_rho_between_processes": {k: repr(v) for k, v in rho_pairs.items()},
        "floor_1_minus_rho": repr(floor_rho),
        "max_per_type_abs_deltaB": {k: repr(v) for k, v in dB_pairs.items()},
        "floor_max_abs_deltaB": repr(floor_dB),
        "per_item_mean_loss_per_process": [x["per_item_mean"] for x in repro],
        "pids": [x["pid"] for x in repro],
    }
    controls["P2_silence_R1_R8"] = p2["runs"]
    controls["P2_ablated_types"] = p2["ablated_types"]
    controls["eval_rung_invariants_note"] = (
        "recorded per evaluation in rowB_eval_records.json and in the P2 block; every "
        "evaluation asserted all seven true before writing")
    (out / "rowB_controls.json").write_text(json.dumps(controls, indent=1))

    # ---------------- distances / twin trap
    def dist_block(vecs):
        return {f"{x}|{y}": {"spearman_rho": repr(spearman(vecs[x], vecs[y])),
                             "distance_1_minus_rho": repr(1.0 - spearman(vecs[x], vecs[y])),
                             "pearson_r_context_only": repr(pearson(vecs[x], vecs[y]))}
                for x, y in PAIRS}

    V16 = {lab: P250[lab]["mean_window"] for lab in labels}
    V13 = {lab: PI250[lab][idx13].mean(axis=0) for lab in labels}
    V10 = {lab: PI250[lab][idx10].mean(axis=0) for lab in labels}
    dist = dict(base)
    dist["floor_1_minus_rho"] = repr(floor_rho)
    dist["subsets"] = {"16": dist_block(V16),
                       "13_no_ambush2_CONTEXT_ONLY": dist_block(V13),
                       "10_no_ambush2_no_bandage1_CONTEXT_ONLY": dist_block(V10)}
    d_twin = 1.0 - spearman(V16["seed0"], V16["seed0prime"])
    foreign = {f"{x}|{y}": 1.0 - spearman(V16[x], V16[y]) for x, y in FOREIGN}
    nearest = min(foreign, key=foreign.get)
    dist["twin_trap"] = {
        "rule": "d(0,0') must be the minimum of the six pairs AND below the nearest foreign "
                "pair by more than the measured floor (README Sec 6)",
        "d_twin": repr(d_twin),
        "nearest_foreign_pair": nearest,
        "d_nearest_foreign": repr(foreign[nearest]),
        "margin": repr(foreign[nearest] - d_twin),
        "floor_1_minus_rho": repr(floor_rho),
        "is_minimum_of_six": bool(all(d_twin < v for v in foreign.values())),
        "margin_exceeds_floor": bool((foreign[nearest] - d_twin) > floor_rho),
        "verdict": ("PASS" if all(d_twin < v for v in foreign.values())
                    and (foreign[nearest] - d_twin) > floor_rho else "FAIL"),
        "note": STATUS,
    }
    per_item = {}
    for k, nm in enumerate(item_cols):
        vi = {lab: PI250[lab][k] for lab in labels}
        dt_ = 1.0 - spearman(vi["seed0"], vi["seed0prime"])
        fo = {f"{x}|{y}": 1.0 - spearman(vi[x], vi[y]) for x, y in FOREIGN}
        per_item[nm] = {"pairs": {kk: repr(vv) for kk, vv in
                                  {f"{x}|{y}": 1.0 - spearman(vi[x], vi[y])
                                   for x, y in PAIRS}.items()},
                        "twin_is_minimum": bool(all(dt_ < v for v in fo.values()))}
    dist["per_item_16"] = per_item
    dist["n_items_twin_is_minimum"] = int(sum(v["twin_is_minimum"] for v in per_item.values()))
    dist["secondary_last_step_16"] = dist_block(
        {lab: P250[lab]["last_step"] for lab in labels})
    dist["secondary_57_without_R1_R8"] = dist_block(
        {lab: np.array([v for t, v in zip(types, P250[lab]["mean_window"])
                        if not (t.startswith("R") and t[1:].isdigit())])
         for lab in labels})
    (out / "rowB_distances.json").write_text(json.dumps(dist, indent=1))

    # ---------------- B vs A
    abl = read_csv_nodup(Path(DIAG_DIR) / "ablation" / "ablation_profiles.csv",
                         ("label", "type"))
    A = {lab: np.array([float(abl[(lab, T)]["delta_16"]) for T in types]) for lab in labels}
    va = dict(base)
    va["row_A_source"] = "../ablation/ablation_profiles.csv, column delta_16"
    va["primary_i_within_individual"] = {
        lab: {"spearman_rho_B_vs_deltaT": repr(spearman(V16[lab], A[lab])),
              "pearson_r_context_only": repr(pearson(V16[lab], A[lab])),
              "spearman_absB_vs_absdeltaT": repr(spearman(np.abs(V16[lab]), np.abs(A[lab])))}
        for lab in labels}
    dB = [1.0 - spearman(V16[x], V16[y]) for x, y in PAIRS]
    dA = [1.0 - spearman(A[x], A[y]) for x, y in PAIRS]
    va["preview_ii_between_individuals"] = {
        "pairs": [f"{x}|{y}" for x, y in PAIRS],
        "distance_B_1_minus_rho": [repr(v) for v in dB],
        "distance_A_1_minus_rho": [repr(v) for v in dA],
        "spearman_over_the_6_distances": repr(spearman(dB, dA)),
        "note": "6 distances, N=4 -- preview only, no inference (README Sec 7)",
    }
    (out / "rowB_vs_rowA.json").write_text(json.dumps(va, indent=1))

    # ---------------- preview 25k -> 250k
    W16 = {lab: P25[lab]["mean_window"] for lab in labels}
    d25 = [1.0 - spearman(W16[x], W16[y]) for x, y in PAIRS]
    prev = dict(base)
    prev["within_run_B25212_vs_B250008"] = {
        lab: {"spearman_rho": repr(spearman(W16[lab], V16[lab])),
              "max_abs_deltaB": repr(float(np.max(np.abs(W16[lab] - V16[lab]))))}
        for lab in labels}
    prev["between_run_distances"] = {
        "pairs": [f"{x}|{y}" for x, y in PAIRS],
        "at_25212": [repr(v) for v in d25],
        "at_250008": [repr(v) for v in dB],
        "spearman_over_the_6_distances": repr(spearman(d25, dB)),
        "twin_is_minimum_at_25212": bool(all(d25[0] < v for v in d25[1:])),
    }
    prev["iteration_0_for_reference"] = {
        "pairs": [f"{x}|{y}" for x, y in PAIRS],
        "distances": [repr(1.0 - spearman(P0[x]["mean_window"], P0[y]["mean_window"]))
                      for x, y in PAIRS]}
    prev["note"] = "preview, not a test (" + STATUS + ")"
    (out / "rowB_preview.json").write_text(json.dumps(prev, indent=1))
    print("ANALYZE DONE")
    print("FLOOR 1-rho", repr(floor_rho), "max|dB|", repr(floor_dB))
    print("TWIN", json.dumps(dist["twin_trap"]))
    return 0


def main():
    a = parse_args()
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    scratch = Path(a.scratch_dir)
    scratch.mkdir(parents=True, exist_ok=True)
    return {"profiles": task_profiles, "repro": task_repro, "p2": task_p2,
            "traj": task_traj, "analyze": task_analyze}[a.task](a, out, scratch)


if __name__ == "__main__":
    sys.exit(main())


# TRANSLATION NOTE, 2026-09-23 (appended at the end so that every line number cited elsewhere
# stays valid): the one Russian line of the module docstring (Mike's launch word) was translated
# into English on Mike's word.  The Russian original is in git history at commit
# 2488ecb72d14aa5398149d9a727b58852873a091.  The recorded script_sha256
# 195a89b555bedf3a0ff00a4c4e0542eafa6370243fbf9ed954f5fe8fbf7f4082 (rowB, ablation, gray and c3B
# records; night3 SHA256.txt; rowB3.py) refers to that original revision as checked out with CRLF
# line endings and reproduces there, not from this revision.  No executable line changed.  Old and
# new hashes and the citing records: docs/notes/2026-09-23-translated-pinned-files.md.
