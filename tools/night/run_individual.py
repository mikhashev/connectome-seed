"""One flyvis individual = one full training run, with held-out evaluation rungs.

Composes the default `flow` config exactly as `flyvis train-single` does
(flyvis_cli/training/train_single.py: initialize_config_dir(CONFIG_PATH) +
compose("solver.yaml", overrides) + prepare_config + MultiTaskSolver + train),
then adds, without modifying flyvis/datamate on disk:

  * seed control     -- `network.node_config.bias.seed=<seed>` (the only seeded
                        parameter init in flyvis: network/initialization.py:154-164,
                        config/network/node_config/bias/bias.yaml:7) plus
                        torch.manual_seed / numpy / random for decoder init, data
                        order (torch SubsetRandomSampler, tasks.py:91) and
                        augmentation (np.random in datasets/augmentation/hex.py,
                        torch.randn_like in PixelNoise.transform).
  * determinism      -- cudnn.deterministic=True, benchmark=False,
                        torch.use_deterministic_algorithms(True, warn_only=True)
                        with CUBLAS_WORKSPACE_CONFIG=:4096:8; every
                        non-deterministic-op warning is recorded by op name.
  * rung hook        -- after the penalty step of iteration k (solver.py:350),
                        i.e. after k completed iterations (solver.py:370 increments
                        afterwards), runs solver.test() on task.val_data with the
                        scheduler swapped for a no-op (test() calls
                        self.scheduler(self.iteration) at solver.py:504), track_loss
                        False (no h5 writes), all RNG states saved/restored, and
                        asserts lr / train-mode / dt unchanged afterwards.
  * checkpoint list  -- flyvis's own checkpoint() already computes the held-out
                        loss: solver.py:427-429
                            val_loss = self.test(
                                dataloader=self.task.val_data, subdir="validation",
                                track_loss=True)
                        That call is intercepted (solver.test wrapped on the
                        instance) and stored as `checkpoint_metrics`; no second pass.
  * timing           -- per-iteration wall time; torch.cuda.synchronize() only every
                        --sync-every-th iteration and at rungs. flyvis itself calls
                        .detach().cpu().item() on the loss and activity every
                        iteration (solver.py:353-363), which already synchronises.

Outputs: <out-dir>/<tag>_<id with / -> ->.json (partial json at every rung and
checkpoint) and <out-dir>/<tag>_<id>.log.
"""
import os
import sys

# Both must be set before torch / flyvis are imported: flyvis resolves root_dir at
# import (flyvis/__init__.py:45-54) and cuBLAS reads the workspace config at first use.
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
os.environ.setdefault(
    "FLYVIS_ROOT_DIR", "C:/Users/mikha/Documents/dpc-research/connectome-seed-data"
)

import argparse
import hashlib
import json
import logging
import random
import re
import statistics
import subprocess
import time
import traceback
import warnings
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent


def parse_args():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--id", required=True, help="ENSEMBLE/NETWORK, e.g. 9990/000")
    p.add_argument("--n-iters", type=int, default=250_000)
    p.add_argument("--rungs", default="1000,5000,25000,250000")
    p.add_argument("--tag", required=True)
    p.add_argument("--out-dir", default=str(HERE))
    p.add_argument("--sync-every", type=int, default=100)
    p.add_argument("--no-determinism", action="store_true",
                   help="A/B control: skip cudnn.deterministic and torch.use_deterministic_algorithms "
                        "(seeds are still set). Default: determinism ON, as the pre-registration s7 prescribes.")
    p.add_argument("--resume", action="store_true",
                   help="Continue an interrupted run: network dir and json must exist; Hydra override "
                        "resume=true; the last checkpoint on disk is restored the way flyvis_cli "
                        "train_single.py:77-85 does; earlier rung/checkpoint metrics are kept.")
    p.add_argument("--progress-every", type=int, default=100,
                   help="append one ASCII progress line (iter/elapsed/s-per-iter/ETA/vram) to the progress "
                        "file and stdout every N iterations; RUNG / CHECKPOINT / DONE lines are always written")
    p.add_argument("--progress-file", default=None,
                   help="progress log path (appended); default <out-dir>/<tag>_<id>.progress.log")
    p.add_argument("--override", action="append", default=[],
                   help="extra Hydra override KEY=VAL, repeatable; appended after the built-in overrides")
    p.add_argument("--stop-after-iter", type=int, default=None,
                   help="diagnostic only (docs/briefs/2026-09-17-c3-jitter-and-evaluator-floor.md): stop training "
                        "right after the rung hook of completed iteration K (K must be one of --rungs, K < --n-iters, "
                        "no --resume). --n-iters is NOT changed, so the lr schedule (flyvis solver.py:995, stepwise "
                        "over task.n_iters) and the epoch count stay the night runs'. Default None: no effect.")
    return p.parse_args()


class _StopAfterIter(Exception):
    """Raised by the iteration hook when --stop-after-iter is reached; only ever raised under that flag."""


# ---------------- progress lines (output only; nothing here touches training or the json) ----------------
_PROG = {"path": None, "prefix": ""}


def _hms(seconds):
    s = int(max(0.0, float(seconds)))
    return f"{s // 3600}:{(s % 3600) // 60:02d}:{s % 60:02d}"


def progress(line):
    """One ASCII line -> progress file (append, closed = flushed) and stdout (flushed)."""
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    msg = " ".join(x for x in (ts, _PROG["prefix"], line) if x)
    msg = msg.replace("\r", " ").replace("\n", " | ").encode("ascii", "replace").decode("ascii")
    if _PROG["path"]:
        try:
            with open(_PROG["path"], "a", encoding="ascii", errors="replace") as pf:
                pf.write(msg + "\n")
        except OSError as e:  # noqa: BLE001
            print(f"progress-file write failed ({e!r})", flush=True)
    print(msg, flush=True)


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def nvidia_smi_used_mib():
    """Driver's view of total GPU memory used (per-process is N/A under WDDM)."""
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=20,
        )
        return int(out.stdout.strip().splitlines()[0])
    except Exception as e:  # noqa: BLE001
        return f"error: {e!r}"


def scene_of(item_name: str) -> str:
    """'sequence_01_ambush_2_split_00' -> 'ambush_2' (name format: sintel.py:157)."""
    m = re.match(r"^sequence_\d+_(.+)_split_\d+$", item_name)
    if not m:
        raise ValueError(f"unexpected sintel item name {item_name!r}")
    return m.group(1)


class _NoopScheduler:
    """Stands in for solver.scheduler while the rung hook runs solver.test()."""

    def __call__(self, iteration):
        return None


def main():
    a = parse_args()
    rungs = sorted({int(x) for x in a.rungs.split(",") if x.strip()})
    if a.stop_after_iter is not None and (a.stop_after_iter not in rungs or a.resume
                                          or not 0 < a.stop_after_iter < a.n_iters):
        print(f"refused: --stop-after-iter {a.stop_after_iter} must be one of --rungs, < --n-iters, "
              f"and not combined with --resume", flush=True)
        return 2
    out_dir = Path(a.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{a.tag}_{a.id.replace('/', '-')}"
    json_path = out_dir / f"{stem}.json"
    log_path = out_dir / f"{stem}.log"
    _PROG["path"] = Path(a.progress_file) if a.progress_file else out_dir / f"{stem}.progress.log"
    _PROG["prefix"] = f"{a.tag} {a.id}"

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(name)s:%(lineno)d] %(message)s",
        handlers=[logging.FileHandler(log_path, encoding="utf-8"),
                  logging.StreamHandler(sys.stdout)],
    )
    log = logging.getLogger("run_individual")

    rec = {
        "tag": a.tag, "id": a.id, "seed": a.seed, "n_iters": a.n_iters, "rungs": rungs,
        "argv": sys.argv[1:], "pid": os.getpid(),
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "exit": "running", "rung_metrics": [], "checkpoint_metrics": [], "checkpoints": [],
        "iter_wall_s": [], "nondeterministic_ops": {}, "warnings": [], "errors": [],
    }

    def dump():
        tmp = json_path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(rec, indent=1, default=str))
        os.replace(tmp, json_path)

    if a.resume:
        if not json_path.exists():
            rec["exit"] = f"refused: --resume but json does not exist: {json_path}"
            rec["errors"].append(rec["exit"])
            dump()
            log.error(rec["exit"])
            progress(f"DONE final_iteration - total 0:00:00 exit {rec['exit']}")
            return 2
        prev = json.loads(json_path.read_text())
        fresh = rec
        rec = prev  # dump()/showwarning close over the name `rec`, so they follow this rebinding
        rec.setdefault("resume_history", []).append(
            {k: prev.get(k) for k in ("argv", "pid", "started_utc", "exit", "final_iteration", "finished_utc")})
        rec["resume_count"] = int(rec.get("resume_count", 0)) + 1
        for k in ("rung_metrics", "checkpoint_metrics", "checkpoints", "iter_wall_s", "warnings", "errors"):
            rec.setdefault(k, [])
        rec.setdefault("nondeterministic_ops", {})
        rec.update({k: fresh[k] for k in ("tag", "id", "seed", "n_iters", "rungs", "argv", "pid", "started_utc", "exit")})
        log.info("RESUME requested: json re-opened, resume_count=%d, kept %d rung_metrics / %d checkpoint_metrics",
                 rec["resume_count"], len(rec["rung_metrics"]), len(rec["checkpoint_metrics"]))

    # ---------------- determinism, before anything touches the GPU ----------------
    random.seed(a.seed)
    np.random.seed(a.seed)
    torch.manual_seed(a.seed)  # seeds CPU and every CUDA generator
    torch.backends.cudnn.deterministic = not a.no_determinism
    torch.backends.cudnn.benchmark = False
    det = {"requested": not a.no_determinism,
           "cublas_workspace_config": os.environ.get("CUBLAS_WORKSPACE_CONFIG"),
           "cudnn_deterministic": torch.backends.cudnn.deterministic,
           "cudnn_benchmark": torch.backends.cudnn.benchmark}
    if a.no_determinism:
        det["use_deterministic_algorithms"] = False
    else:
        try:
            torch.use_deterministic_algorithms(True, warn_only=True)
            det["use_deterministic_algorithms"] = True
            det["warn_only"] = True
        except Exception as e:  # noqa: BLE001
            det["use_deterministic_algorithms"] = False
            det["error"] = repr(e)
    det["mode_query"] = torch.are_deterministic_algorithms_enabled()
    det["warn_only_query"] = torch.is_deterministic_algorithms_warn_only_enabled()
    det["tf32_matmul"] = torch.backends.cuda.matmul.allow_tf32
    det["tf32_cudnn"] = torch.backends.cudnn.allow_tf32
    rec["determinism"] = det

    def showwarning(message, category, filename, lineno, file=None, line=None):
        msg = str(message)
        key = f"{category.__name__}: {msg}"
        if "does not have a deterministic implementation" in msg or "nondeterministic" in msg.lower():
            op = msg.split(" does not have")[0].strip()
            d = rec["nondeterministic_ops"].setdefault(
                op, {"count": 0, "where": f"{filename}:{lineno}", "message": msg})
            d["count"] += 1
            if d["count"] == 1:
                log.warning("NONDETERMINISTIC OP under use_deterministic_algorithms(warn_only): %s (%s:%s)",
                            op, filename, lineno)
        else:
            if key not in rec["warnings"]:
                rec["warnings"].append(key)
                log.warning("%s (%s:%s)", key, filename, lineno)

    warnings.showwarning = showwarning
    # Default filter ("once per message+site"): each non-deterministic op is still named once per
    # call site; the per-call count is not kept, so the warning machinery costs nothing per iteration.

    # ---------------- flyvis imports (root_dir / default device fixed at import) ----
    import flyvis
    from flyvis import results_dir
    from flyvis.solver import MultiTaskSolver
    import flyvis_cli.training.train_single as ts
    from hydra import compose, initialize_config_dir
    from omegaconf import OmegaConf
    from datamate import set_root_context

    rec["versions"] = {"flyvis": flyvis.__version__, "torch": torch.__version__,
                       "numpy": np.__version__, "python": sys.version.split()[0],
                       "cuda": torch.version.cuda, "cudnn": torch.backends.cudnn.version(),
                       "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None}
    rec["flyvis_root_dir"] = str(flyvis.root_dir)
    rec["flyvis_device"] = str(flyvis.device)
    conn = Path(flyvis.connectome_file)
    rec["connectome_file"] = str(conn)
    rec["connectome_sha256"] = sha256_of(conn)
    log.info("flyvis %s torch %s connectome %s sha256 %s",
             flyvis.__version__, torch.__version__, conn, rec["connectome_sha256"])

    # ---------------- compose the config exactly like `flyvis train-single` ----------
    overrides = [
        f"ensemble_and_network_id={a.id}",
        "task_name=flow",
        "train=true",
        "resume=true" if a.resume else "resume=false",
        f"task.n_iters={a.n_iters}",
        f"description={a.tag}",
        f"network.node_config.bias.seed={a.seed}",
    ] + list(a.override)
    rec["hydra_overrides"] = overrides
    with initialize_config_dir(config_dir=ts.CONFIG_PATH, version_base="1.1"):
        args = compose(config_name="solver.yaml", overrides=overrides)
    config = ts.prepare_config(args)
    rec["resolved_config_yaml"] = OmegaConf.to_yaml(args, resolve=True)
    rec["solver_config"] = config
    log.info("Resolved config:\n%s", rec["resolved_config_yaml"])

    network_dir = results_dir / "flow" / a.id
    rec["network_dir"] = str(network_dir)
    if a.resume and not network_dir.exists():
        rec["exit"] = f"refused: --resume but network dir does not exist: {network_dir}"
        rec["errors"].append(rec["exit"])
        dump()
        log.error(rec["exit"])
        progress(f"DONE final_iteration - total 0:00:00 exit {rec['exit']}")
        return 2
    if not a.resume and network_dir.exists():
        rec["exit"] = ("refused: network dir exists (datamate raises FileExistsError on "
                       "incompatible config; nothing deleted)")
        rec["errors"].append(rec["exit"])
        dump()
        log.error(rec["exit"])
        progress(f"DONE final_iteration - total 0:00:00 exit {rec['exit']} ({network_dir})")
        return 2

    # ---------------- build solver (seeded) ----------------
    t0 = time.perf_counter()
    if a.resume:
        # datamate pops delete_if_exists from a passed config only when the path already exists
        # (datamate/directory.py:222-237) while MultiTaskSolver stored it at creation (solver.py:110), so a
        # re-open under enforce_config_match raises FileExistsError
        # (passed=['-delete_if_exists'], stored=['+delete_if_exists: False']). Relax the in-process
        # datamate flag for the re-open only; datamate then warns (recorded in rec["warnings"]) and does not
        # touch _meta.yaml (directory.py:1436-1451).
        import datamate
        datamate.enforce_config_match(False)
    try:
        with set_root_context(results_dir):
            solver = MultiTaskSolver(config=config, delete_if_exists=False)
    finally:
        if a.resume:
            datamate.enforce_config_match(True)
    rec["solver_init_s"] = time.perf_counter() - t0
    rec["network_dir"] = str(solver.dir.path)
    task, ds, net = solver.task, solver.task.dataset, solver.network
    rec["n_params"] = {
        "network_trainable": sum(p.numel() for p in net.parameters() if p.requires_grad),
        "decoder_trainable": sum(p.numel() for d in solver.decoder.values()
                                 for p in d.parameters() if p.requires_grad)}
    rec["bias_seed_in_network_config"] = int(net.config.node_config.bias.seed)
    assert rec["bias_seed_in_network_config"] == a.seed, (rec["bias_seed_in_network_config"], a.seed)

    # ---------------- resume: restore the last checkpoint on disk ----------------
    if a.resume:
        from flyvis.utils.chkpt_utils import (recover_decoder, recover_network, recover_optimizer,
                                              recover_penalty_optimizers, resolve_checkpoints)
        rec["checkpoints_on_disk_before_resume"] = [int(i) for i in solver.checkpoints]
        try:
            # exactly the call flyvis_cli/training/train_single.py:77-85 makes for resume=true
            solver.recover(network=True, decoder=True, optimizer=True, penalty=True,
                           checkpoint=-1, strict=True, force=False)
            rec["resume_method"] = "flyvis MultiTaskSolver.recover(checkpoint=-1)"
            cps = resolve_checkpoints(solver.dir)
            ck_path = cps.paths[cps.indices.index(int(solver._curr_chkpt_ind))]
        except Exception:
            rec["flyvis_recover_error"] = traceback.format_exc()
            log.error("flyvis solver.recover() raised; using in-script replica of solver.py:598-638\n%s",
                      rec["flyvis_recover_error"])
            # Replica of MultiTaskSolver.recover (solver.py:598-638) for checkpoint=-1 (= last on disk),
            # built from flyvis's own helpers; nothing in site-packages is modified.
            cps = resolve_checkpoints(solver.dir)
            if not cps.indices:
                rec["exit"] = f"refused: --resume but no checkpoint in {solver.checkpoint_path}"
                rec["errors"].append(rec["exit"])
                dump()
                log.error(rec["exit"])
                progress(f"DONE final_iteration - total 0:00:00 exit {rec['exit']}")
                return 2
            ck_path = cps.paths[-1]
            solver._last_chkpt_ind = int(cps.indices[-1])   # solver.py:612
            solver._curr_chkpt_ind = int(cps.indices[-1])   # solver.py:613 (checkpoint=-1 -> last)
            sd = torch.load(ck_path, map_location=flyvis.device, weights_only=False)  # solver.py:616
            solver.iteration = sd.get("iteration", None)    # solver.py:619
            solver.scheduler(solver.iteration)              # solver.py:623
            solver._val_loss = sd.pop("val_loss", float("inf"))  # solver.py:627
            recover_network(solver.network, sd)             # solver.py:630
            recover_decoder(solver.decoder, sd, strict=True)  # solver.py:632
            recover_optimizer(solver.optimizer, sd)         # solver.py:634
            recover_penalty_optimizers(solver.penalty.optimizers, sd)  # solver.py:636
            rec["resume_method"] = "in-script replica of solver.py:598-638 (flyvis recover() raised)"
        rec["resumed_from_iteration"] = int(solver.iteration)
        rec["resumed_checkpoint"] = {"path": str(ck_path), "chkpt_index": int(solver._curr_chkpt_ind),
                                     "last_chkpt_ind": int(solver._last_chkpt_ind),
                                     "val_loss_in_checkpoint": float(solver._val_loss)}
        rec["resume_rng_note"] = ("restored: network, decoder, optimizer, penalty optimizers, iteration, "
                                  "scheduler(iteration); NOT restored: any RNG state (solver.py has no "
                                  "get/set_rng_state) -> post-resume data order/augmentation/dropout stream "
                                  "restarts from --seed, it is not the original run's stream")
        log.info("RESUMED from %s: solver.iteration=%d chkpt_index=%d via %s", ck_path,
                 solver.iteration, solver._curr_chkpt_ind, rec["resume_method"])

    # ---------------- held-out / train sequence lists (names, not indices) ----------
    names = list(ds.arg_df.name)
    train_items = [names[i] for i in task.train_seq_index]
    val_items = [names[i] for i in task.val_seq_index]
    train_scenes = sorted({scene_of(n) for n in train_items})
    val_scenes = sorted({scene_of(n) for n in val_items})
    scene_intersection = sorted(set(train_scenes) & set(val_scenes))
    item_intersection = sorted(set(train_items) & set(val_items))
    used = set(task.train_seq_index) | set(task.val_seq_index)
    unused = [n for i, n in enumerate(names) if i not in used]
    rec["split"] = {
        "original_split": bool(config["task"].get("original_split")),
        "n_items_total": len(names),
        "train_items": train_items, "val_items": val_items,
        "train_scenes": train_scenes, "val_scenes": val_scenes,
        "scene_intersection": scene_intersection, "item_intersection": item_intersection,
        "items_in_neither_list": unused,
        "train_seq_index": list(map(int, task.train_seq_index)),
        "val_seq_index": list(map(int, task.val_seq_index)),
    }
    log.info("HELD-OUT scenes (%d): %s", len(val_scenes), val_scenes)
    log.info("HELD-OUT items (%d): %s", len(val_items), val_items)
    log.info("TRAIN scenes (%d): %s", len(train_scenes), train_scenes)
    log.info("TRAIN items (%d): %s", len(train_items), train_items)
    log.info("items in neither list (%d): %s", len(unused), unused)
    log.info("INTERSECTION scenes=%s items=%s", scene_intersection, item_intersection)
    if scene_intersection or item_intersection:
        rec["exit"] = f"refused: held-out/train intersection not empty: {scene_intersection} {item_intersection}"
        rec["errors"].append(rec["exit"])
        dump()
        log.error(rec["exit"])
        progress(f"DONE final_iteration - total 0:00:00 exit {rec['exit']}")
        return 2

    # ---------------- augmentation facts ----------------
    aug_keys = ["temporal_crop", "jitter", "rotate", "flip", "noise",
                "piecewise_resample", "linear_interpolate", "gamma_correct"]

    def aug_state():
        s = {k: bool(getattr(ds, k).augment) for k in aug_keys}
        s["temporal_crop.random"] = bool(ds.temporal_crop.random)
        s["dataset.augment"] = bool(ds.augment)
        return s

    # train(): solver.py:294 `with self.task.dataset.augmentation(augment)`, augment = not overfit
    with ds.augmentation(True):
        aug_train = aug_state()
    # test():  solver.py:514 `with self.task.dataset.augmentation(False)`
    with ds.augmentation(False):
        aug_val = aug_state()
    rec["augmentation"] = {
        "params": {k: getattr(ds, k) for k in [
            "augment", "random_temporal_crop", "all_frames", "resampling", "interpolate",
            "p_flip", "p_rot", "contrast_std", "brightness_std", "gaussian_white_noise",
            "gamma_std", "flip_axes", "n_frames", "dt"]},
        "train_loader_context_augmentation(True)": aug_train,
        "val_loader_context_augmentation(False)": aug_val,
        "note": ("piecewise_resample/linear_interpolate are frame-rate resampling, not augmentation; "
                 "sintel.py augment.setter: 'these two are not affected by augment'"),
        "loaders": {
            "train_data": {"batch_size": task.train_data.batch_size,
                           "sampler": type(task.train_data.sampler).__name__,
                           "drop_last": task.train_data.drop_last,
                           "len_batches": len(task.train_data),
                           "num_workers": task.train_data.num_workers},
            "val_data": {"batch_size": task.val_data.batch_size,
                         "sampler": type(task.val_data.sampler).__name__,
                         "drop_last": task.val_data.drop_last,
                         "len_batches": len(task.val_data),
                         "num_workers": task.val_data.num_workers},
        },
    }
    log.info("augmentation train ctx: %s", aug_train)
    log.info("augmentation val ctx:   %s", aug_val)

    # ---------------- schedule facts ----------------
    sch = solver.scheduler
    lr_arr = sch.scheduled_params["lr_net"].array
    rec["schedule"] = {
        "chkpt_every_epoch": int(solver.config.scheduler.chkpt_every_epoch),
        "iters_per_epoch": len(task.train_data),
        "iters_between_checkpoints_nominal": int(solver.config.scheduler.chkpt_every_epoch) * len(task.train_data),
        "stop_iter": int(sch.stop_iter),
        "lr_net_array_len": int(len(lr_arr)),
        "lr_net_unique": sorted({float(x) for x in lr_arr}, reverse=True),
        "lr_net_at_iter": {str(i): float(lr_arr[i]) for i in [0] + [r for r in rungs if r < len(lr_arr)]},
        "lr_now": [g["lr"] for g in solver.optimizer.param_groups],
        "activity_penalty_stop_iter": solver.penalty.activity_penalty_stop_iter,
    }
    dump()

    # ---------------- hooks ----------------
    state = {"train_start": None, "last_t": None, "n_done": 0}

    def rng_save():
        return (torch.get_rng_state(), torch.cuda.get_rng_state_all(),
                np.random.get_state(), random.getstate())

    def rng_restore(s):
        torch.set_rng_state(s[0])
        torch.cuda.set_rng_state_all(s[1])
        np.random.set_state(s[2])
        random.setstate(s[3])

    orig_test = solver.test  # bound method; checkpoint() looks up self.test -> instance attr wins

    def test_wrapped(dataloader, subdir="validation", track_loss=False, t_pre=0.25):
        t = time.perf_counter()
        r = orig_test(dataloader, subdir=subdir, track_loss=track_loss, t_pre=t_pre)
        if track_loss and subdir == "validation" and dataloader is task.val_data:
            # flyvis's own held-out pass inside checkpoint(): solver.py:427-429. Reused, no second pass.
            rec["checkpoint_metrics"].append({
                "iteration": int(solver.iteration), "val_loss": float(r),
                "chkpt_index": int(solver._last_chkpt_ind),
                "wall_s_since_start": ((time.perf_counter() - state["train_start"])
                                       if state["train_start"] else None),
                "test_wall_s": time.perf_counter() - t,
                **({"resume_count": rec["resume_count"]} if a.resume else {}),
            })
        return r

    solver.test = test_wrapped

    orig_checkpoint = solver.checkpoint

    def checkpoint_wrapped():
        t = time.perf_counter()
        r = orig_checkpoint()
        rec["checkpoints"].append({
            "chkpt_index": int(solver._last_chkpt_ind), "iteration": int(solver.iteration),
            "duration_s": time.perf_counter() - t,
            "wall_s_since_start": ((time.perf_counter() - state["train_start"])
                                   if state["train_start"] else None)})
        if state["train_start"]:
            state["last_t"] = time.perf_counter()  # keep checkpoint time out of the next iteration's wall time
        dump()
        cm = rec["checkpoint_metrics"][-1] if rec["checkpoint_metrics"] else None
        if cm and cm["chkpt_index"] == int(solver._last_chkpt_ind):
            progress(f"CHECKPOINT {int(solver.iteration)} val_loss {cm['val_loss']:.4f}")
        else:
            progress(f"CHECKPOINT {int(solver.iteration)} val_loss n/a")
        return r

    solver.checkpoint = checkpoint_wrapped

    def eval_rung(k):
        torch.cuda.synchronize()
        t = time.perf_counter()
        lr_before = [g["lr"] for g in solver.optimizer.param_groups]
        pen_lr_before = [g["lr"] for o in solver.penalty.optimizers.values()
                         if o is not None for g in o.param_groups]
        dt_before, sched_iter_before = ds.dt, sch._current_iteration
        training_before = (net.training, [d.training for d in solver.decoder.values()])
        rng = rng_save()
        solver.scheduler = _NoopScheduler()  # test() calls self.scheduler(self.iteration) (solver.py:504)
        try:
            with torch.no_grad():  # test() is already @torch.no_grad(); belt and braces
                val = float(solver.test(dataloader=task.val_data, subdir="validation", track_loss=False))
        finally:
            solver.scheduler = sch
            rng_restore(rng)
        lr_after = [g["lr"] for g in solver.optimizer.param_groups]
        pen_lr_after = [g["lr"] for o in solver.penalty.optimizers.values()
                        if o is not None for g in o.param_groups]
        checks = {
            "lr_unchanged": bool(lr_before == lr_after),
            "pen_lr_unchanged": bool(pen_lr_before == pen_lr_after),
            "dt_unchanged": bool(ds.dt == dt_before),
            "scheduler_iter_unchanged": bool(sch._current_iteration == sched_iter_before),
            "back_in_train_mode": bool(net.training and all(d.training for d in solver.decoder.values())),
            "was_in_train_mode_before": bool(training_before[0] and all(training_before[1])),
            "dataset_augment_restored": bool(ds.augment) is True,
        }
        torch.cuda.synchronize()
        m = {"iteration": k, "val_loss": val,
             "wall_s_since_start": t - state["train_start"],
             "torch_max_memory_allocated_MiB": torch.cuda.max_memory_allocated() / 2**20,
             "torch_max_memory_reserved_MiB": torch.cuda.max_memory_reserved() / 2**20,
             "nvidia_smi_memory_used_MiB": nvidia_smi_used_mib(),
             "hook_wall_s": time.perf_counter() - t,
             "solver_iteration_at_hook": int(solver.iteration),
             "checks": checks}
        if a.resume:
            m["resume_count"] = rec["resume_count"]
        rec["rung_metrics"].append(m)
        if not all(checks.values()):
            rec["errors"].append(f"rung {k}: state check failed {checks}")
            log.error("RUNG %d STATE CHECK FAILED %s", k, checks)
        log.info("RUNG %d val_loss=%.6f wall=%.1fs vram_alloc=%.0fMiB hook=%.2fs", k, val,
                 m["wall_s_since_start"], m["torch_max_memory_allocated_MiB"], m["hook_wall_s"])
        dump()
        progress(f"RUNG {k} val_loss {val:.4f}")

    rung_set = set(rungs)
    if a.resume:
        rung_set = {r for r in rungs if r > rec["resumed_from_iteration"]}
        log.info("rungs after resume (> %d): %s", rec["resumed_from_iteration"], sorted(rung_set))

    def on_iteration_end(iteration_pre_increment):
        k = iteration_pre_increment + 1  # completed iterations; solver.py:370 increments after penalty
        if k % a.sync_every == 0 or k in rung_set:
            torch.cuda.synchronize()
        now = time.perf_counter()
        rec["iter_wall_s"].append(round(now - state["last_t"], 6))
        state["last_t"] = now
        state["n_done"] = k
        if k % a.sync_every == 0:
            log.info("iter %d done, last %.4fs", k, rec["iter_wall_s"][-1])
        if a.progress_every > 0 and k % a.progress_every == 0:
            progress_line(k)
        if k in rung_set:
            eval_rung(k)
            state["last_t"] = time.perf_counter()  # exclude the hook from the next iteration's time
        if a.stop_after_iter is not None and k == a.stop_after_iter:
            raise _StopAfterIter(k)  # after the penalty step and the hook of iteration k; caught below

    def progress_line(k):
        # elapsed = wall since the training loop started; s/iter = mean of the existing per-iteration
        # wall times over the last --progress-every iterations (no cuda sync); vram = torch peak, no sync
        it = rec["iter_wall_s"][-a.progress_every:]
        spi = (sum(it) / len(it)) if it else float("nan")
        elapsed = time.perf_counter() - state["train_start"]
        eta = max(0, a.n_iters - k) * spi
        fin = time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime(time.time() + eta))
        vram = torch.cuda.max_memory_allocated() / 2**20
        progress(f"iter {k}/{a.n_iters} ({100.0 * k / a.n_iters:.1f}%) elapsed {_hms(elapsed)} "
                 f"s/iter {spi:.4f} ETA {_hms(eta)} (fin ~{fin}) vram {vram:.0f}MiB")

    PenCls = type(solver.penalty)

    class PenaltyHooked(PenCls):  # instance-level class swap; _chkpt/optimizers untouched
        def __call__(self_, activity, iteration):
            r = PenCls.__call__(self_, activity=activity, iteration=iteration)
            on_iteration_end(iteration)
            return r

    solver.penalty.__class__ = PenaltyHooked

    # ---------------- train ----------------
    random.seed(a.seed)
    np.random.seed(a.seed)
    torch.manual_seed(a.seed)  # data order / augmentation stream
    torch.cuda.reset_peak_memory_stats()
    torch.cuda.synchronize()
    state["train_start"] = state["last_t"] = time.perf_counter()
    rec["exit"] = "training"
    dump()
    exc_line = None
    try:
        solver.train(overfit=False)
        torch.cuda.synchronize()
        rec["exit"] = "ok"
    except _StopAfterIter as e:  # reachable only under --stop-after-iter
        torch.cuda.synchronize()
        rec["exit"] = "ok"
        rec["stopped_after_iter"] = int(e.args[0])  # solver.iteration stays k-1: solver.py increments after the batch
    except BaseException as e:  # noqa: BLE001
        rec["exit"] = f"error: {e!r}"
        rec["errors"].append(traceback.format_exc())
        log.error("TRAINING FAILED\n%s", traceback.format_exc())
        exc_line = traceback.format_exception_only(type(e), e)[0].strip()
    finally:
        end = time.perf_counter()
        rec["total_train_wall_s"] = end - state["train_start"]
        rec["final_iteration"] = int(solver.iteration)
        it = rec["iter_wall_s"]
        n_ep = len(task.train_data)
        # iterations 1000..2000 inclusive (1-based); it[i] is the wall time of iteration i+1
        rec["iter_wall_median_1000_2000_s"] = statistics.median(it[999:2000]) if len(it) >= 2000 else None
        rec["iter_wall_median_all_s"] = statistics.median(it) if it else None
        rec["iter_wall_median_after_first_epoch_s"] = statistics.median(it[n_ep:]) if len(it) > n_ep else None
        rec["vram"] = {"torch_max_memory_allocated_MiB": torch.cuda.max_memory_allocated() / 2**20,
                       "torch_max_memory_reserved_MiB": torch.cuda.max_memory_reserved() / 2**20,
                       "nvidia_smi_memory_used_MiB_at_end": nvidia_smi_used_mib()}
        ck_iters = [c["iteration"] for c in rec["checkpoints"]]
        rec["checkpoint_cadence_observed"] = {
            "checkpoint_iterations": ck_iters,
            "iters_between_checkpoints": [b - x for x, b in zip(ck_iters, ck_iters[1:])],
            "iters_per_epoch": n_ep}
        try:
            if a.resume and "train_loss_per_iter" in rec:
                rec["train_loss_per_iter_before_resume"] = rec["train_loss_per_iter"]
            rec["train_loss_per_iter"] = [float(x) for x in solver.dir.loss[()]]
        except Exception as e:  # noqa: BLE001
            rec["train_loss_error"] = repr(e)
        rec["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        dump()
        log.info("EXIT %s final_iteration=%s total_wall=%.1fs json=%s", rec["exit"],
                 rec["final_iteration"], rec["total_train_wall_s"], json_path)
        if exc_line:
            progress(f"ERROR {exc_line}")
        progress(f"DONE final_iteration {rec['final_iteration']} total {_hms(rec['total_train_wall_s'])} "
                 f"exit {rec['exit']}")
    return 0 if rec["exit"] == "ok" else 1


if __name__ == "__main__":
    try:
        rc = main()
    except SystemExit:
        raise
    except BaseException as e:  # noqa: BLE001  (crash before/outside the training try: import, config, solver build)
        progress("ERROR " + traceback.format_exception_only(type(e), e)[0].strip())
        progress("DONE final_iteration - total - exit crashed")
        raise
    sys.exit(rc)
