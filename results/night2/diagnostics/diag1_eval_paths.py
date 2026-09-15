"""Diagnostic 1 -- one saved checkpoint through both reporting paths, plus evaluation noise.

Reviewers' request: `docs/experiments/002-night2-seeds-1-and-2.md` Sec 5a items 7 and 10,
`docs/next-session-plan.md` Sec 3/4.

WHAT THIS SCRIPT DOES NOT DO: it never trains, never writes into
connectome-seed-data/results/flow/9991/*, and never calls solver.checkpoint() or
solver.test(track_loss=True) (the only two calls that write into a network dir).
The solver it builds lives in a scratch datamate root (--netdir-root), created with
datamate.set_root_context; the four runs' checkpoints are read with torch.load only.

The evaluation used here is the rung hook of night/run_individual.py, copied VERBATIM
(see hook_eval() below, which is run_individual.py:531-546 (the body of eval_rung down to
the rng restore) with the telemetry lines
dropped and nothing else changed).

Sub-commands (--task):
  paths      (a) last checkpoint of each of the four runs through the hook path
  noise5     (b) 5 hook evaluations of seed 0 / chkpt 250,008 in ONE process
  noise1     (b) 1 hook evaluation, for running in fresh processes (--rep N labels it)
  items      (c) per-item (16 items) losses for all four runs at two checkpoints
  traj       (d) hook path over all 72 checkpoints of seed 0 and seed 0'
"""

import os
import sys

# Same two environment variables, set the same way and in the same place as
# night/run_individual.py:46-49 (before torch / flyvis are imported).
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
os.environ.setdefault(
    "FLYVIS_ROOT_DIR", "C:/Users/mikha/Documents/dpc-research/connectome-seed-data"
)

import argparse
import json
import random
import shutil
import time
from pathlib import Path

import h5py
import numpy as np
import torch

RUNS = {"000": "seed0", "900": "seed0prime", "001": "seed1", "002": "seed2"}
FLOW_DIR = Path(os.environ["FLYVIS_ROOT_DIR"]) / "results" / "flow" / "9991"


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--task", required=True,
                   choices=["paths", "noise5", "noise1", "items", "traj"])
    p.add_argument("--out-dir", required=True)
    p.add_argument("--netdir-root", required=True,
                   help="scratch datamate root for the throw-away solver directory")
    p.add_argument("--rep", type=int, default=0, help="label for --task noise1")
    return p.parse_args()


# ---------------------------------------------------------------- checkpoint index
def chkpt_table(run: str):
    """[(chkpt_index, stored_chkpt_iter, solver_iteration, path)] for one run.

    flyvis writes `chkpt_iter` as `self.iteration - 1` (flyvis/solver.py:463) and stores
    `"iteration": self.iteration - 1` inside the checkpoint file (solver.py:453), while
    night/run_individual.py records `int(solver.iteration)` in its json / the committed
    night_report_checkpoints.csv (run_individual.py:498). So
        solver_iteration (== the csv's "iteration") = stored_chkpt_iter + 1.
    """
    d = FLOW_DIR / run
    with h5py.File(d / "chkpt_index.h5", "r") as f:
        idx = [int(x) for x in f["data"][()]]
    with h5py.File(d / "chkpt_iter.h5", "r") as f:
        its = [int(x) for x in f["data"][()]]
    assert len(idx) == len(its)
    return [(i, it, it + 1, d / "chkpts" / f"chkpt_{i:05}") for i, it in zip(idx, its)]


# ---------------------------------------------------------------- solver
def build_solver(netdir_root: Path):
    """Compose the config exactly as night/run_individual.py:275-323 does, but put the
    datamate NetworkDir in a scratch root so nothing under connectome-seed-data is
    touched.  Config is the night runs' config with seed 0 (the initial parameters are
    overwritten by every recover_network() call, so the seed only affects the throw-away
    initialisation)."""
    random.seed(0)
    np.random.seed(0)
    torch.manual_seed(0)
    # The night runs ran with --no-determinism (night/start_night.ps1:65), i.e.
    # run_individual.py:211-218 with a.no_determinism True:
    torch.backends.cudnn.deterministic = False
    torch.backends.cudnn.benchmark = False

    import flyvis  # noqa: F401
    from flyvis.solver import MultiTaskSolver
    import flyvis_cli.training.train_single as ts
    from hydra import compose, initialize_config_dir
    from datamate import set_root_context

    overrides = [
        "ensemble_and_network_id=9991/000",
        "task_name=flow",
        "train=true",
        "resume=false",
        "task.n_iters=250000",
        "description=diag1",
        "network.node_config.bias.seed=0",
    ]
    with initialize_config_dir(config_dir=ts.CONFIG_PATH, version_base="1.1"):
        args = compose(config_name="solver.yaml", overrides=overrides)
    config = ts.prepare_config(args)
    # The throw-away NetworkDir must not already exist (datamate refuses to re-open a
    # dir whose stored config carries delete_if_exists, directory.py:1433), so the
    # scratch root is wiped first.  Guard: it must be a scratchpad path.
    assert "scratchpad" in str(netdir_root).replace("\\", "/"), netdir_root
    if netdir_root.exists():
        shutil.rmtree(netdir_root)
    netdir_root.mkdir(parents=True, exist_ok=True)
    with set_root_context(netdir_root):
        solver = MultiTaskSolver(config=config, delete_if_exists=False)
    return solver


class _NoopScheduler:
    """run_individual.py:147-151, verbatim."""

    def __call__(self, iteration):
        return None


def load_checkpoint(solver, path: Path):
    """Put one saved checkpoint's network+decoder state into the solver, and put the
    solver into the state flyvis's own checkpoint-time evaluation had: iteration set
    from the checkpoint and the real scheduler applied at that iteration (flyvis's
    test() does `self.scheduler(self.iteration)`, solver.py:504; the rung hook swaps a
    no-op in because training had already applied the scheduler at that iteration)."""
    import flyvis
    from flyvis.utils.chkpt_utils import recover_decoder, recover_network

    sd = torch.load(path, map_location=flyvis.device, weights_only=False)
    solver.iteration = int(sd["iteration"]) + 1  # csv convention, see chkpt_table()
    solver.scheduler(solver.iteration)
    recover_network(solver.network, sd)
    recover_decoder(solver.decoder, sd, strict=True)
    assert float(solver.task.dataset.dt) == float(sd["dt"]), (solver.task.dataset.dt, sd["dt"])
    return {"stored_val_loss": float(sd["val_loss"]), "stored_iteration": int(sd["iteration"]),
            "solver_iteration": int(solver.iteration), "dt": float(sd["dt"])}


def hook_eval(solver):
    """THE RUNG HOOK, copied verbatim from night/run_individual.py:531-546 (the
    measurement lines of eval_rung); only the telemetry/state-assertion lines that
    follow it (run_individual.py:547-577) are dropped, since they record wall time and
    VRAM, not the value."""
    sch = solver.scheduler
    task = solver.task
    torch.cuda.synchronize()
    rng = (torch.get_rng_state(), torch.cuda.get_rng_state_all(),
           np.random.get_state(), random.getstate())
    solver.scheduler = _NoopScheduler()
    try:
        with torch.no_grad():
            val = float(solver.test(dataloader=task.val_data, subdir="validation",
                                    track_loss=False))
    finally:
        solver.scheduler = sch
        torch.set_rng_state(rng[0])
        torch.cuda.set_rng_state_all(rng[1])
        np.random.set_state(rng[2])
        random.setstate(rng[3])
    torch.cuda.synchronize()
    return val


def per_item_eval(solver, t_pre=0.25):
    """A copy of flyvis/solver.py:474-556 `MultiTaskSolver.test` with track_loss removed
    and the per-item losses returned instead of only their mean.  NOT the hook path --
    used only for the per-item breakdown (c); its mean is checked against hook_eval()."""
    task, dataloader = solver.task, solver.task.val_data
    solver._eval()
    solver.scheduler(solver.iteration)  # solver.py:504
    initial_state = solver.network.steady_state(
        t_pre=t_pre, dt=task.dataset.dt, batch_size=dataloader.batch_size, value=0.5)
    losses = {t: [] for t in task.dataset.tasks}
    with torch.no_grad():
        with task.dataset.augmentation(False):
            for _, data in enumerate(dataloader):
                n_samples, n_frames, _, _ = data["lum"].shape
                solver.network.stimulus.zero(n_samples, n_frames)
                solver.network.stimulus.add_input(data["lum"])
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


def val_item_names(solver):
    names = list(solver.task.dataset.arg_df.name)
    return [names[i] for i in solver.task.val_seq_index]


# ---------------------------------------------------------------- tasks
def main():
    a = parse_args()
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    solver = build_solver(Path(a.netdir_root))
    import flyvis
    meta = {"flyvis": flyvis.__version__, "torch": torch.__version__,
            "python": sys.version.split()[0],
            "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            "netdir": str(solver.dir.path), "task": a.task,
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    print("META", json.dumps(meta))

    if a.task == "paths":
        rows = []
        for run, label in RUNS.items():
            tab = chkpt_table(run)
            ci, stored_it, solver_it, path = tab[-1]
            info = load_checkpoint(solver, path)
            t = time.perf_counter()
            hook = hook_eval(solver)
            dt_wall = time.perf_counter() - t
            rows.append({
                "run": run, "label": label, "chkpt_index": ci,
                "chkpt_file": path.name,
                "chkpt_iter_h5": stored_it, "solver_iteration": solver_it,
                "hook_path_value": repr(hook),
                "stored_checkpoint_val_loss": repr(info["stored_val_loss"]),
                "hook_minus_stored": repr(hook - info["stored_val_loss"]),
                "eval_wall_s": round(dt_wall, 3)})
            print("PATHS", json.dumps(rows[-1]))
        (out / "diag1a_paths.json").write_text(json.dumps({"meta": meta, "rows": rows}, indent=1))

    elif a.task == "noise5":
        tab = chkpt_table("000")
        ci, stored_it, solver_it, path = tab[-1]
        info = load_checkpoint(solver, path)
        vals = []
        for i in range(5):
            v = hook_eval(solver)
            vals.append(v)
            print("NOISE5", i, repr(v))
        rec = {"meta": meta, "run": "000", "chkpt_index": ci,
               "solver_iteration": solver_it,
               "stored_checkpoint_val_loss": repr(info["stored_val_loss"]),
               "values": [repr(v) for v in vals],
               "min": repr(min(vals)), "max": repr(max(vals)),
               "spread": repr(max(vals) - min(vals)),
               "n_distinct": len(set(vals))}
        (out / "diag1b_noise_inprocess.json").write_text(json.dumps(rec, indent=1))
        print("NOISE5 SPREAD", rec["spread"], "distinct", rec["n_distinct"])

    elif a.task == "noise1":
        tab = chkpt_table("000")
        ci, stored_it, solver_it, path = tab[-1]
        info = load_checkpoint(solver, path)
        v = hook_eval(solver)
        rec = {"meta": meta, "rep": a.rep, "pid": os.getpid(), "run": "000",
               "chkpt_index": ci, "solver_iteration": solver_it,
               "stored_checkpoint_val_loss": repr(info["stored_val_loss"]),
               "value": repr(v)}
        (out / f"diag1b_noise_proc{a.rep}.json").write_text(json.dumps(rec, indent=1))
        print("NOISE1", a.rep, repr(v))

    elif a.task == "items":
        names = val_item_names(solver)
        result = {"meta": meta, "val_items": names, "checkpoints": {}}
        for target_solver_iter in (250008, 25212):
            block = {}
            for run, label in RUNS.items():
                tab = chkpt_table(run)
                hit = [r for r in tab if r[2] == target_solver_iter]
                assert len(hit) == 1, (run, target_solver_iter, hit)
                ci, stored_it, solver_it, path = hit[0]
                info = load_checkpoint(solver, path)
                losses = per_item_eval(solver)
                per_item = losses["flow"]
                mean = float(np.mean(per_item))
                hook = hook_eval(solver)
                block[label] = {
                    "run": run, "chkpt_index": ci, "solver_iteration": solver_it,
                    "stored_checkpoint_val_loss": repr(info["stored_val_loss"]),
                    "hook_path_value": repr(hook),
                    "per_item_mean": repr(mean),
                    "per_item_mean_minus_hook": repr(mean - hook),
                    "per_item": [repr(x) for x in per_item]}
                print("ITEMS", target_solver_iter, label, "mean", repr(mean),
                      "hook", repr(hook))
            result["checkpoints"][str(target_solver_iter)] = block
        (out / "diag1c_per_item.json").write_text(json.dumps(result, indent=1))
        # csv
        for target in ("250008", "25212"):
            block = result["checkpoints"][target]
            lines = ["item,seed0,seed0prime,seed1,seed2,seed0prime_minus_seed0"]
            for i, nm in enumerate(names):
                a0 = float(block["seed0"]["per_item"][i])
                ap = float(block["seed0prime"]["per_item"][i])
                a1 = float(block["seed1"]["per_item"][i])
                a2 = float(block["seed2"]["per_item"][i])
                lines.append(f"{nm},{a0!r},{ap!r},{a1!r},{a2!r},{ap - a0!r}")
            (out / f"per_item_{target}.csv").write_text("\n".join(lines) + "\n")

    elif a.task == "traj":
        tab0 = chkpt_table("000")
        tabp = chkpt_table("900")
        assert [r[2] for r in tab0] == [r[2] for r in tabp]
        rows = []
        for (ci, sit, it, p0), (_, _, _, pp) in zip(tab0, tabp):
            i0 = load_checkpoint(solver, p0)
            h0 = hook_eval(solver)
            ip = load_checkpoint(solver, pp)
            hp = hook_eval(solver)
            rows.append({"iteration": it, "chkpt_index": ci,
                         "hook_val_0": h0, "hook_val_0prime": hp,
                         "stored_ckpt_val_0": i0["stored_val_loss"],
                         "stored_ckpt_val_0prime": ip["stored_val_loss"]})
            print("TRAJ", it, repr(h0), repr(i0["stored_val_loss"]),
                  repr(hp), repr(ip["stored_val_loss"]), flush=True)
        hdr = ("iteration,chkpt_index,hook_val_0,hook_val_0prime,"
               "stored_ckpt_val_0,stored_ckpt_val_0prime")
        lines = [hdr] + [
            f"{r['iteration']},{r['chkpt_index']},{r['hook_val_0']!r},"
            f"{r['hook_val_0prime']!r},{r['stored_ckpt_val_0']!r},"
            f"{r['stored_ckpt_val_0prime']!r}" for r in rows]
        (out / "hook_path_trajectory_0_vs_0prime.csv").write_text("\n".join(lines) + "\n")
        diffs = [abs(r["hook_val_0"] - r["stored_ckpt_val_0"]) for r in rows] + \
                [abs(r["hook_val_0prime"] - r["stored_ckpt_val_0prime"]) for r in rows]
        late = [r for r in rows if r["iteration"] > 150000]
        d_late = [r["hook_val_0prime"] - r["hook_val_0"] for r in late]
        summ = {"meta": meta, "n_checkpoints": len(rows), "n_evaluations": 2 * len(rows),
                "max_abs_hook_minus_stored": repr(max(diffs)),
                "n_late_checkpoints": len(late),
                "late_hook_0prime_minus_0_mean": repr(float(np.mean(d_late))),
                "late_hook_0prime_minus_0_min": repr(min(d_late)),
                "late_hook_0prime_minus_0_max": repr(max(d_late))}
        (out / "diag1d_trajectory_summary.json").write_text(json.dumps(summ, indent=1))
        print("TRAJ SUMMARY", json.dumps(summ))

    return 0


if __name__ == "__main__":
    sys.exit(main())
