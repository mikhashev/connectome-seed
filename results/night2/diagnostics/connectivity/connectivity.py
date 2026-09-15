"""Linear mode connectivity between saved flyvis end states.

Design: `docs/next-session-plan.md` Sec 4 (bullet "Linear mode connectivity", sub-bullet
"Design (Ark 06:52, Zcode 07:05)"), which fixes: variant 2 primary (interpolate the 8,161
trainable parameters, RECOMPUTE the BatchNorm running statistics on training data, evaluate
in eval mode), variant 1 in the same run (interpolate the 8,161 parameters AND the 17
BatchNorm buffers, evaluate directly), variant 3 rejected, self-path A->A as the control
that isolates buffer-recompute artefacts, (0,1) as the different-seed control.

WHAT THIS SCRIPT DOES NOT DO: it never trains, never writes into
connectome-seed-data/results/flow/9991/*, never calls solver.checkpoint() and never calls
solver.test(track_loss=True).  The solver lives in a scratch datamate root (--netdir-root).
Checkpoints are read with torch.load only.

The evaluator is REUSED from `diag1_eval_paths.py` in the parent directory (imported, not
re-implemented): build_solver(), hook_eval() (= night/run_individual.py:531-546 verbatim),
per_item_eval() (= flyvis/solver.py:474-556 with the 16 per-item losses returned),
val_item_names(), chkpt_table().

Sub-commands (--task):
  run        evaluate one or more paths at a list of alphas, append rows to a jsonl
  summarize  read the jsonl, write connectivity_profiles.csv and connectivity_summary.json
"""

import os
import sys

# Same two environment variables, set the same way and in the same place as
# night/run_individual.py:46-49 and diag1_eval_paths.py:30-33 (before torch / flyvis).
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
os.environ.setdefault(
    "FLYVIS_ROOT_DIR", "C:/Users/mikha/Documents/dpc-research/connectome-seed-data"
)

import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from diag1_eval_paths import (  # noqa: E402
    build_solver,
    chkpt_table,
    hook_eval,
    per_item_eval,
    val_item_names,
)

# ---------------------------------------------------------------- key sets
# Verified, not assumed: `diag2_requires_grad.json` (printed from requires_grad) and
# `diag2_weight_distance.py:36-44`.
CORE_TRAIN = ["nodes_bias", "nodes_time_const", "edges_syn_strength"]          # 734
CORE_FIXED = ["edges_sign", "edges_syn_count"]                                 # 2,959
DEC_TRAIN = ["base.0.weight", "base.0.bias", "base.1.weight", "base.1.bias",
             "decoder.0.weight", "decoder.0.bias"]                             # 7,427
DEC_BUFFERS = ["base.1.running_mean", "base.1.running_var",
               "base.1.num_batches_tracked"]                                   # 17
N_TRAINABLE = 8161

# path name -> (run A, run B)
PATHS = {
    "main_0_to_0prime": ("000", "900"),
    "control_0_to_1": ("000", "001"),
    "self_0_to_0": ("000", "000"),
    "extra_0prime_to_1": ("900", "001"),
}
TARGET_SOLVER_ITER = 250008  # = chkpt_00071; chkpt_iter.h5 value 250007 + 1


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--task", required=True, choices=["run", "summarize"])
    p.add_argument("--out-dir", required=True)
    p.add_argument("--netdir-root", default=None)
    p.add_argument("--rows-file", default="rows.jsonl")
    p.add_argument("--paths", default=",".join(PATHS))
    p.add_argument("--alphas", default=",".join(f"{i * 0.05:.6g}" for i in range(21)))
    p.add_argument("--variants", default="1,2")
    return p.parse_args()


# ---------------------------------------------------------------- checkpoint loading
def endpoint_state(run: str):
    """The last checkpoint (solver iteration 250,008) of one run, on CPU."""
    hit = [r for r in chkpt_table(run) if r[2] == TARGET_SOLVER_ITER]
    assert len(hit) == 1, (run, hit)
    ci, stored_it, solver_it, path = hit[0]
    sd = torch.load(path, map_location="cpu", weights_only=False)
    net, dec = sd["network"], sd["decoder"]["flow"]
    assert sorted(net.keys()) == sorted(CORE_TRAIN + CORE_FIXED), sorted(net.keys())
    assert sorted(dec.keys()) == sorted(DEC_TRAIN + DEC_BUFFERS), sorted(dec.keys())
    n = sum(net[k].numel() for k in CORE_TRAIN) + sum(dec[k].numel() for k in DEC_TRAIN)
    assert n == N_TRAINABLE, n
    nb = sum(dec[k].numel() for k in DEC_BUFFERS)
    assert nb == 17, nb
    return {"run": run, "chkpt_index": ci, "chkpt_path": str(path),
            "solver_iteration": solver_it, "dt": float(sd["dt"]),
            "val_loss": float(sd["val_loss"]), "network": net, "decoder": dec}


def lerp(a: torch.Tensor, b: torch.Tensor, alpha: float) -> torch.Tensor:
    """(1-alpha)*a + alpha*b, computed in float64 and cast back to a's dtype.

    Integer tensors (num_batches_tracked) are interpolated in float64 and rounded to
    nearest.  At alpha == 0.0 / 1.0 the float64 expression is exactly a / b, which the
    caller asserts bit-for-bit.
    """
    if a.dtype.is_floating_point:
        return ((1.0 - alpha) * a.double() + alpha * b.double()).to(a.dtype)
    return torch.round((1.0 - alpha) * a.double() + alpha * b.double()).to(a.dtype)


def interpolated_state(sa, sb, alpha: float, variant: int):
    """Build the state dict for one point of one variant.

    variant 2: the 8,161 trainable parameters are interpolated; the 17 BatchNorm buffers
               are set to endpoint A's values and then OVERWRITTEN by the recompute.
    variant 1: the 8,161 parameters AND the 17 buffers are interpolated.
    The 2,959 fixed core parameters (edges_sign, edges_syn_count) are asserted identical
    between the two endpoints and copied through.
    """
    net, dec = {}, {}
    for k in CORE_TRAIN:
        net[k] = lerp(sa["network"][k], sb["network"][k], alpha)
    for k in CORE_FIXED:
        assert torch.equal(sa["network"][k], sb["network"][k]), k
        net[k] = sa["network"][k].clone()
    for k in DEC_TRAIN:
        dec[k] = lerp(sa["decoder"][k], sb["decoder"][k], alpha)
    for k in DEC_BUFFERS:
        if variant == 1:
            dec[k] = lerp(sa["decoder"][k], sb["decoder"][k], alpha)
        else:
            dec[k] = sa["decoder"][k].clone()
    if alpha == 0.0:
        for k in CORE_TRAIN:
            assert torch.equal(net[k], sa["network"][k]), ("alpha0", k)
        for k in DEC_TRAIN:
            assert torch.equal(dec[k], sa["decoder"][k]), ("alpha0", k)
    if alpha == 1.0:
        for k in CORE_TRAIN:
            assert torch.equal(net[k], sb["network"][k]), ("alpha1", k)
        for k in DEC_TRAIN:
            assert torch.equal(dec[k], sb["decoder"][k]), ("alpha1", k)
    return {"network": net, "decoder": {"flow": dec}}


def load_into_solver(solver, state, iteration: int, dt: float):
    """Same shape as diag1_eval_paths.load_checkpoint(): set the iteration, apply the real
    scheduler at that iteration, then recover network and decoder."""
    from flyvis.utils.chkpt_utils import recover_decoder, recover_network

    solver.iteration = int(iteration)
    solver.scheduler(solver.iteration)
    recover_network(solver.network, {"network": state["network"]})
    recover_decoder(solver.decoder, {"decoder": dict(state["decoder"])}, strict=True)
    assert float(solver.task.dataset.dt) == float(dt), (solver.task.dataset.dt, dt)


# ---------------------------------------------------------------- BN recompute
def build_bn_loader(solver, batch_size=4):
    """Deterministic pass over the TRAINING split, every item exactly once.

    CHOICE (stated in the README): flyvis's own training loader is
    `DataLoader(dataset, batch_size=4, sampler=SubsetRandomSampler(train_seq_index),
    drop_last=True)` (flyvis/task/tasks.py:85-90) -- a random order that drops 3 of the 51
    items per epoch and draws from an unseeded global RNG.  A random, partial pass would
    make the recompute stochastic and would put noise into the self-path control, so the
    recompute here uses `IndexSampler(train_seq_index)` (the same sampler flyvis uses for
    its validation loader, tasks.py:104-107) with batch_size 4 and drop_last=False:
    13 batches, 12 of 4 items + 1 of 3, covering all 51 training items exactly once in a
    fixed order.
    """
    from torch.utils.data import DataLoader

    from flyvis.utils.dataset_utils import IndexSampler

    idx = list(solver.task.train_seq_index)
    return DataLoader(solver.task.dataset, batch_size=batch_size,
                      sampler=IndexSampler(idx), drop_last=False), len(idx)


def recompute_bn(solver, loader):
    """Reset the decoder's BatchNorm running statistics and re-estimate them by forward
    passes over the training split, no gradient, BatchNorm in train mode, momentum None
    (cumulative average over batches).

    CHOICES (stated in the README):
      * augmentation OFF -- `dataset.augmentation(False)`.  flyvis trains under
        `augmentation(True)` (flyvis/solver.py:294) and its augmentations draw from
        UNSEEDED global RNGs (flyvis/datasets/augmentation/hex.py:103-104, 205-206, 320,
        386), which would make the recompute stochastic and the self-path control noisy.
      * t_pre = 0.5 for the steady state, i.e. the TRAINING value
        (`config.get("t_pre_train", 0.5)`, flyvis/solver.py:300), not test()'s 0.25
        (flyvis/solver.py:479) -- this forward pass is the training-side one.
      * the final batch has 3 items, so a second steady state is computed at batch_size 3
        (flyvis's steady state is built for a fixed batch size,
        flyvis/network/network.py:548-586).
      * momentum None means the cumulative average weights each of the 13 batches equally,
        so the 3-item batch counts like a 4-item batch.  Deterministic and identical at
        every alpha, so it is a fixed estimator, not a per-point artefact.
    """
    task = solver.task
    bn = solver.decoder["flow"].base[1]
    assert isinstance(bn, torch.nn.modules.batchnorm._BatchNorm), type(bn)
    bn.reset_running_stats()
    bn.momentum = None
    solver._train()
    n_batches = 0
    n_items = 0
    steady = {}
    with torch.no_grad():
        with task.dataset.augmentation(False):
            for _, data in enumerate(loader):
                n_samples, n_frames, _, _ = data["lum"].shape
                if n_samples not in steady:
                    steady[n_samples] = solver.network.steady_state(
                        t_pre=0.5, dt=task.dataset.dt, batch_size=n_samples, value=0.5)
                solver.network.stimulus.zero(n_samples, n_frames)
                solver.network.stimulus.add_input(data["lum"])
                activity = solver.network(solver.network.stimulus(), task.dataset.dt,
                                          state=steady[n_samples])
                for t in task.dataset.tasks:
                    solver.decoder[t](activity)
                n_batches += 1
                n_items += n_samples
    solver._eval()
    return {"bn_batches": n_batches, "bn_items": n_items,
            "bn_num_batches_tracked": int(bn.num_batches_tracked.item()),
            "bn_running_mean": [float(x) for x in bn.running_mean.detach().cpu()],
            "bn_running_var": [float(x) for x in bn.running_var.detach().cpu()]}


# ---------------------------------------------------------------- run
def run(a):
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows_path = out / a.rows_file
    solver = build_solver(Path(a.netdir_root))
    import flyvis

    meta = {"flyvis": flyvis.__version__, "torch": torch.__version__,
            "python": sys.version.split()[0],
            "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            "netdir": str(solver.dir.path),
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "argv": sys.argv}
    print("META", json.dumps(meta), flush=True)

    items = val_item_names(solver)
    assert len(items) == 16, items
    loader, n_train_items = build_bn_loader(solver)
    print("BN_LOADER", json.dumps({"n_train_items": n_train_items,
                                   "batch_size": loader.batch_size,
                                   "n_batches": len(loader),
                                   "sampler": type(loader.sampler).__name__,
                                   "drop_last": loader.drop_last}), flush=True)

    states = {}
    for run_id in {r for name in a.paths.split(",") for r in PATHS[name.strip()]}:
        states[run_id] = endpoint_state(run_id)
        print("ENDPOINT", json.dumps({k: v for k, v in states[run_id].items()
                                      if k not in ("network", "decoder")}), flush=True)

    alphas = [float(x) for x in a.alphas.split(",")]
    variants = [int(v) for v in a.variants.split(",")]
    t0 = time.perf_counter()
    with open(rows_path, "a", encoding="utf-8") as fh:
        for path_name in [p.strip() for p in a.paths.split(",")]:
            ra, rb = PATHS[path_name]
            sa, sb = states[ra], states[rb]
            assert sa["dt"] == sb["dt"]
            for variant in variants:
                for alpha in alphas:
                    t = time.perf_counter()
                    st = interpolated_state(sa, sb, alpha, variant)
                    load_into_solver(solver, st, TARGET_SOLVER_ITER, sa["dt"])
                    bn = {}
                    if variant == 2:
                        bn = recompute_bn(solver, loader)
                    agg = hook_eval(solver)
                    per_item = per_item_eval(solver)["flow"]
                    assert len(per_item) == 16
                    row = {"path": path_name, "run_a": ra, "run_b": rb,
                           "variant": variant, "alpha": alpha,
                           "aggregate_hook": agg,
                           "aggregate_per_item_mean": float(np.mean(per_item)),
                           "per_item": [float(x) for x in per_item],
                           "stored_val_loss_a": sa["val_loss"],
                           "stored_val_loss_b": sb["val_loss"],
                           "wall_s": round(time.perf_counter() - t, 3)}
                    row.update({k: v for k, v in bn.items()
                                if k in ("bn_batches", "bn_items",
                                         "bn_num_batches_tracked")})
                    if alpha in (0.0, 1.0) and variant == 2:
                        row["bn_running_mean"] = bn["bn_running_mean"]
                        row["bn_running_var"] = bn["bn_running_var"]
                    fh.write(json.dumps(row) + "\n")
                    fh.flush()
                    print("PT", path_name, "v%d" % variant, f"{alpha:g}",
                          repr(agg), repr(float(np.mean(per_item))),
                          row["wall_s"], flush=True)
    print("RUN DONE", round(time.perf_counter() - t0, 1), "s", flush=True)
    (out / ("run_meta_%s.json" % time.strftime("%H%M%S", time.gmtime()))).write_text(
        json.dumps({"meta": meta, "val_items": items,
                    "bn_loader": {"n_train_items": n_train_items,
                                  "batch_size": loader.batch_size,
                                  "n_batches": len(loader),
                                  "sampler": type(loader.sampler).__name__,
                                  "drop_last": loader.drop_last},
                    "wall_s": round(time.perf_counter() - t0, 1)}, indent=1))
    return 0


# ---------------------------------------------------------------- summarize
def summarize(a):
    out = Path(a.out_dir)
    rows = [json.loads(ln) for ln in (out / a.rows_file).read_text().splitlines() if ln.strip()]
    metas = sorted(out.glob("run_meta_*.json"))
    items = json.loads(metas[0].read_text())["val_items"]

    # de-duplicate (path, variant, alpha), keeping the LAST row written
    uniq = {}
    for r in rows:
        uniq[(r["path"], r["variant"], round(r["alpha"], 6))] = r
    rows = sorted(uniq.values(), key=lambda r: (r["path"], r["variant"], r["alpha"]))

    hdr = (["path", "run_a", "run_b", "variant", "alpha", "aggregate_hook",
            "aggregate_per_item_mean", "hook_minus_per_item_mean",
            "bn_batches", "wall_s"] + ["item_%s" % n for n in items])
    lines = [",".join(hdr)]
    for r in rows:
        vals = [r["path"], r["run_a"], r["run_b"], str(r["variant"]), repr(r["alpha"]),
                repr(r["aggregate_hook"]), repr(r["aggregate_per_item_mean"]),
                repr(r["aggregate_hook"] - r["aggregate_per_item_mean"]),
                str(r.get("bn_batches", "")), repr(r["wall_s"])]
        vals += [repr(x) for x in r["per_item"]]
        lines.append(",".join(vals))
    (out / "connectivity_profiles.csv").write_text("\n".join(lines) + "\n")

    summary = {"val_items": items, "n_rows": len(rows), "paths": {}}
    for path_name in sorted({r["path"] for r in rows}):
        summary["paths"][path_name] = {}
        for variant in sorted({r["variant"] for r in rows if r["path"] == path_name}):
            sel = [r for r in rows if r["path"] == path_name and r["variant"] == variant]
            sel.sort(key=lambda r: r["alpha"])
            al = [r["alpha"] for r in sel]
            ag = [r["aggregate_hook"] for r in sel]
            e0 = [r for r in sel if r["alpha"] == 0.0][0]
            e1 = [r for r in sel if r["alpha"] == 1.0][0]
            imax = int(np.argmax(ag))
            imin = int(np.argmin(ag))
            ends = max(e0["aggregate_hook"], e1["aggregate_hook"])
            steps = [(ag[i + 1] - ag[i], al[i], al[i + 1]) for i in range(len(ag) - 1)]
            big = max(steps, key=lambda s: abs(s[0]))
            # per-item barrier: max along path - max(endpoints), per item
            pi = np.array([r["per_item"] for r in sel])            # (n_alpha, 16)
            pi_ends = np.maximum(np.array(e0["per_item"]), np.array(e1["per_item"]))
            pi_bar = pi.max(axis=0) - pi_ends
            summary["paths"][path_name][f"variant_{variant}"] = {
                "run_a": sel[0]["run_a"], "run_b": sel[0]["run_b"],
                "n_points": len(sel), "alphas": al,
                "loss_alpha0": e0["aggregate_hook"],
                "loss_alpha1": e1["aggregate_hook"],
                "stored_val_loss_a": e0["stored_val_loss_a"],
                "stored_val_loss_b": e0["stored_val_loss_b"],
                "endpoint_repro_err_a": e0["aggregate_hook"] - e0["stored_val_loss_a"],
                "endpoint_repro_err_b": e1["aggregate_hook"] - e1["stored_val_loss_b"],
                "max_loss": ag[imax], "alpha_at_max": al[imax],
                "min_loss": ag[imin], "alpha_at_min": al[imin],
                "max_of_endpoints": ends,
                "barrier": ag[imax] - ends,
                "largest_inter_point_change": big[0],
                "largest_inter_point_change_between": [big[1], big[2]],
                "max_abs_inter_point_change": max(abs(s[0]) for s in steps),
                "range_along_path": max(ag) - min(ag),
                "per_item_barrier": [float(x) for x in pi_bar],
                "profile": [[al[i], ag[i]] for i in range(len(ag))],
            }
    (out / "connectivity_summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps({p: {v: {k: d[k] for k in
                              ("loss_alpha0", "loss_alpha1", "max_loss", "alpha_at_max",
                               "barrier", "min_loss", "largest_inter_point_change",
                               "endpoint_repro_err_a", "endpoint_repro_err_b")}
                          for v, d in vs.items()}
                      for p, vs in summary["paths"].items()}, indent=1))
    return 0


def main():
    a = parse_args()
    return run(a) if a.task == "run" else summarize(a)


if __name__ == "__main__":
    sys.exit(main())
