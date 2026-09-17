"""C3 Part B -- evaluator floor by path x state x repeat (and B' on run 703).

PREVIEW DIAGNOSTIC -- NOT A TEST.
Protocol: docs/briefs/2026-09-17-c3-jitter-and-evaluator-floor.md v1.2 (commit 97b48bb), Sec 2.

WHAT THIS SCRIPT DOES NOT DO: it never trains, never writes into
connectome-seed-data/results/flow/*, and never calls solver.checkpoint() or
solver.test(track_loss=True).  The solver lives in a scratch datamate root
(D.build_solver asserts "scratchpad" in the path and deletes that root); checkpoints are
read with torch.load only (D.load_checkpoint via RB.load_named).

NOTHING OF THE EVALUATION IS RE-IMPLEMENTED HERE.  Imports exactly as
results/night3/diagnostics/ablation/ablation_night3.py:30-53:
  E1 = D.hook_eval(solver)                      (rung-hook path; 16-item mean only)
  E2 = D.per_item_eval(solver)["flow"]          (copy of flyvis test; P0 path)
  E3 = ABL.eval_items(solver, ABL.make_mask(types_arr, set(), device))
                                                (E2 with the ablation state hook, all-ones mask)
Every call is wrapped in RB.snapshot_state / RB.invariants (all seven must be True).

--task proc   : one process; for each (run, checkpoint): load once, five rounds E1,E2,E3.
--task floor  : CPU only; reads the proc jsons, writes c3B_floor.json and c3B_means.csv.
All floats are written as repr(float(x)); nothing is rounded.
"""

import os
import sys

sys.dont_write_bytecode = True  # do not touch __pycache__ next to D / ABL / RB

os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
os.environ.setdefault(
    "FLYVIS_ROOT_DIR", "C:/Users/mikha/Documents/dpc-research/connectome-seed-data"
)

DIAG_DIR = "C:/Users/mikha/Documents/dpc-research/connectome-seed/results/night2/diagnostics"
N2_ABL = os.path.join(DIAG_DIR, "ablation")
N2_RB = os.path.join(DIAG_DIR, "rowB")

import argparse
import hashlib
import itertools
import json
import math
import time
from pathlib import Path

import numpy as np

STATUS = "PREVIEW DIAGNOSTIC -- NOT A TEST"
BRIEF = "docs/briefs/2026-09-17-c3-jitter-and-evaluator-floor.md v1.2 (commit 97b48bb), Sec 2"
P0_TOL = 1e-4  # brief Sec 2 gate: |mean of the five E2 16-item means - stored val_loss| <= 1e-4, in P1
EVALS = ["E1", "E2", "E3"]
# checkpoint index -> solver iteration; 0/8/71 are also asserted by RB.load_named (NAMED_CHKPTS)
EXPECTED_ITER = {0: 0, 7: 21612, 8: 25212, 71: 250008}


def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


SCRIPT_HASHES = {
    "results/diagnostics/c3/c3_evaluator_floor.py": sha256_file(__file__),
    "results/night2/diagnostics/diag1_eval_paths.py": sha256_file(os.path.join(DIAG_DIR, "diag1_eval_paths.py")),
    "results/night2/diagnostics/ablation/ablation.py": sha256_file(os.path.join(N2_ABL, "ablation.py")),
    "results/night2/diagnostics/rowB/rowB.py": sha256_file(os.path.join(N2_RB, "rowB.py")),
}


def r(x):
    return repr(float(x))


def finite_all(xs):
    return all(math.isfinite(float(x)) for x in xs)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--task", required=True, choices=["proc", "floor"])
    p.add_argument("--proc", type=int, default=1)
    p.add_argument("--runs", default="003,903")
    p.add_argument("--chkpts", default="0,8,71")
    p.add_argument("--out-dir", required=True)
    p.add_argument("--out-name", default=None)
    p.add_argument("--netdir-root", default=None)
    p.add_argument("--p0-gate", action="store_true",
                   help="apply the P0 gate in this process (brief: P1)")
    p.add_argument("--proc-files", default="c3B_proc1.json,c3B_proc2.json,c3B_proc3.json")
    p.add_argument("--floor-name", default="c3B_floor.json")
    p.add_argument("--csv-name", default="c3B_means.csv")
    return p.parse_args()


def pair_stats(vecs_a, vecs_b, pairs, largest):
    """pairs: list of (i, j) indexes into vecs_a / vecs_b.  Returns max |d mean| and, if per-item
    vectors exist, max per-item |d| and the same in float32 ulps of `largest` (rowB.py:365-367)."""
    dm = [abs(float(np.mean(vecs_a[i])) - float(np.mean(vecs_b[j]))) for i, j in pairs]
    out = {"n_pairs": len(pairs), "max_abs_delta_16_item_mean": r(max(dm))}
    if vecs_a[0].size > 1:
        di = [float(np.max(np.abs(vecs_a[i] - vecs_b[j]))) for i, j in pairs]
        ulp = float(np.spacing(np.float32(largest)))
        out["max_abs_delta_per_item"] = r(max(di))
        out["float32_ulp_of_largest_per_item_value"] = r(ulp)
        out["max_abs_delta_per_item_in_float32_ulps"] = r(max(di) / ulp)
    return out


# ------------------------------------------------------------------------------ proc
def task_proc(a):
    sys.path.insert(0, DIAG_DIR)
    sys.path.insert(0, N2_ABL)
    sys.path.insert(0, N2_RB)
    import torch
    import diag1_eval_paths as D
    import ablation as ABL
    import rowB as RB

    out_dir = Path(a.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / (a.out_name or f"c3B_proc{a.proc}.json")
    assert not out_path.exists(), f"refusing to overwrite {out_path}"
    netroot = Path(a.netdir_root)
    runs = [x.strip() for x in a.runs.split(",") if x.strip()]
    chkpts = [int(x) for x in a.chkpts.split(",") if x.strip()]

    doc = {"status": STATUS, "brief": BRIEF, "script_sha256": SCRIPT_HASHES, "task": "proc",
           "proc": a.proc, "pid": os.getpid(), "argv": sys.argv[1:],
           "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "netdir_root": str(netroot), "p0_gate_applied": bool(a.p0_gate), "p0_tol": P0_TOL,
           "cells": [], "gate_failures": [], "exit": "running"}

    def dump():
        tmp = out_path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(doc, indent=1))
        os.replace(tmp, out_path)

    t0 = time.perf_counter()
    solver = D.build_solver(netroot)
    import flyvis
    device = flyvis.device
    doc["build_solver_wall_s"] = time.perf_counter() - t0
    doc["env"] = {"flyvis": flyvis.__version__, "torch": torch.__version__,
                  "numpy": np.__version__, "python": sys.version.split()[0],
                  "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
                  "device": str(device), "cudnn_deterministic": torch.backends.cudnn.deterministic,
                  "cudnn_benchmark": torch.backends.cudnn.benchmark,
                  "CUBLAS_WORKSPACE_CONFIG": os.environ.get("CUBLAS_WORKSPACE_CONFIG"),
                  "FLYVIS_ROOT_DIR": os.environ.get("FLYVIS_ROOT_DIR"),
                  "netdir": str(solver.dir.path), "dt": float(solver.task.dataset.dt),
                  "val_batch_size": int(solver.task.val_data.batch_size)}
    types_arr = ABL.node_type_array(solver.network)
    doc["val_items"] = D.val_item_names(solver)
    assert len(doc["val_items"]) == 16
    dump()

    def one_call(ev):
        net = solver.network
        assert net._state_hooks == (), net._state_hooks
        before = RB.snapshot_state(solver)
        torch.cuda.synchronize()
        t = time.perf_counter()
        if ev == "E1":
            val = D.hook_eval(solver)
            items = None
            mean = float(val)
        elif ev == "E2":
            items = np.array(D.per_item_eval(solver)["flow"], dtype=np.float64)
            mean = float(np.mean(items))
        else:
            items = ABL.eval_items(solver, ABL.make_mask(types_arr, set(), device))
            mean = float(np.mean(items))
        torch.cuda.synchronize()
        wall = time.perf_counter() - t
        after = RB.snapshot_state(solver)
        assert net._state_hooks == (), net._state_hooks
        inv = RB.invariants(before, after)
        return mean, items, inv, wall

    stop = False
    for run in runs:
        for ci in chkpts:
            solver_it, info = RB.load_named(solver, run, ci)
            assert solver_it == EXPECTED_ITER[ci], (run, ci, solver_it)
            cell = {"run": run, "chkpt_index": ci, "solver_iteration": solver_it,
                    "stored_iteration": info["stored_iteration"],
                    "stored_val_loss": r(info["stored_val_loss"]), "calls": []}
            vals = {e: [] for e in EVALS}
            items = {e: [] for e in EVALS}
            for rnd in range(5):
                for ev in EVALS:
                    mean, it, inv, wall = one_call(ev)
                    c = {"round": rnd + 1, "evaluator": ev, "mean_16": r(mean),
                         "invariants": inv, "all_seven_true": bool(all(inv.values())),
                         "wall_s": wall,
                         "stored_minus_this": r(info["stored_val_loss"] - mean)}
                    if it is not None:
                        c["per_item"] = [r(x) for x in it]
                    cell["calls"].append(c)
                    vals[ev].append(mean)
                    items[ev].append(it if it is not None else np.array([mean]))
                    fin = finite_all([mean] + ([] if it is None else list(it)))
                    if not fin:
                        doc["gate_failures"].append(f"NaN/inf: run {run} chkpt {ci} round {rnd+1} {ev}")
                    if not c["all_seven_true"]:
                        doc["gate_failures"].append(f"invariant False: run {run} chkpt {ci} round {rnd+1} {ev} {inv}")
            if not math.isfinite(info["stored_val_loss"]):
                doc["gate_failures"].append(f"NaN/inf stored val_loss: run {run} chkpt {ci}")
            # within-process floors per evaluator (10 pairs)
            pairs10 = list(itertools.combinations(range(5), 2))
            cell["within_process"] = {}
            for ev in EVALS:
                largest = float(max(np.max(np.abs(v)) for v in items[ev]))
                cell["within_process"][ev] = pair_stats(items[ev], items[ev], pairs10, largest)
                cell["within_process"][ev]["means"] = [r(x) for x in vals[ev]]
                cell["within_process"][ev]["n_distinct_means"] = len(set(vals[ev]))
            # same-state path differences over all 25 call pairs
            cell["path_differences"] = {}
            pairs25 = list(itertools.product(range(5), range(5)))
            for x, y in [("E1", "E2"), ("E1", "E3"), ("E2", "E3")]:
                d = [vals[x][i] - vals[y][j] for i, j in pairs25]
                pd = {"values_25": [r(v) for v in d], "min": r(min(d)), "max": r(max(d)),
                      "max_abs": r(max(abs(v) for v in d)),
                      "same_round_values_5": [r(vals[x][i] - vals[y][i]) for i in range(5)]}
                if x == "E2":
                    largest = float(max(np.max(np.abs(v)) for v in items["E2"] + items["E3"]))
                    di = [float(np.max(np.abs(items[x][i] - items[y][j]))) for i, j in pairs25]
                    ulp = float(np.spacing(np.float32(largest)))
                    pd["max_abs_delta_per_item"] = r(max(di))
                    pd["max_abs_delta_per_item_in_float32_ulps"] = r(max(di) / ulp)
                    pd["n_call_pairs_bitwise_equal_per_item"] = int(sum(
                        bool(np.array_equal(items[x][i], items[y][j])) for i, j in pairs25))
                cell["path_differences"][f"{x}-{y}"] = pd
            # P0
            e2_mean5 = float(np.mean(vals["E2"]))
            p0 = e2_mean5 - info["stored_val_loss"]
            cell["P0"] = {"mean_of_five_E2_means": r(e2_mean5),
                          "mean_of_five_E2_minus_stored": r(p0),
                          "abs": r(abs(p0)), "tol": P0_TOL, "within_tol": bool(abs(p0) <= P0_TOL),
                          "single_call_E2_minus_stored": [r(v - info["stored_val_loss"]) for v in vals["E2"]],
                          "single_call_E1_minus_stored": [r(v - info["stored_val_loss"]) for v in vals["E1"]],
                          "mean_of_five_E1_minus_stored": r(float(np.mean(vals["E1"])) - info["stored_val_loss"])}
            if a.p0_gate and not abs(p0) <= P0_TOL:
                doc["gate_failures"].append(f"P0: run {run} chkpt {ci} |{p0!r}| > {P0_TOL}")
            doc["cells"].append(cell)
            dump()
            print(f"run {run} chkpt {ci} it {solver_it}: stored {info['stored_val_loss']!r} "
                  f"E1 {vals['E1']} E2 {vals['E2']} E3 {vals['E3']} P0 {p0!r}", flush=True)
            if doc["gate_failures"]:
                stop = True
                break
        if stop:
            break
    doc["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    doc["total_wall_s"] = time.perf_counter() - t0
    doc["exit"] = "gate_failed" if doc["gate_failures"] else "ok"
    dump()
    print("EXIT", doc["exit"], doc["gate_failures"], flush=True)
    return 3 if doc["gate_failures"] else 0


# ------------------------------------------------------------------------------ floor (CPU)
def task_floor(a):
    out_dir = Path(a.out_dir)
    files = [out_dir / f for f in a.proc_files.split(",")]
    procs = [json.loads(f.read_text()) for f in files]
    for p in procs:
        assert p["exit"] == "ok", (p["proc"], p["exit"])
    keys = [(c["run"], c["chkpt_index"]) for c in procs[0]["cells"]]
    for p in procs[1:]:
        assert [(c["run"], c["chkpt_index"]) for c in p["cells"]] == keys
    doc = {"status": STATUS, "brief": BRIEF, "script_sha256": SCRIPT_HASHES, "task": "floor",
           "inputs": {f.name: sha256_file(f) for f in files},
           "definitions": {
               "within_process": "all 10 call pairs within each process, max over processes (30 pairs)",
               "cross_process": "all 5x5 call pairs between each pair of processes (75 pairs)",
               "ulps": "max per-item |delta| / np.spacing(np.float32(largest |per-item value| of the cell's "
                       "vectors across all processes)), as rowB.py:365-367",
               "path_differences": "E1-E2, E1-E3, E2-E3 on the 16-item mean, all 25 call pairs per process, "
                                   "pooled over processes (75)"},
           "cells": []}
    for ki, (run, ci) in enumerate(keys):
        cells = [p["cells"][ki] for p in procs]
        stored = {c["stored_val_loss"] for c in cells}
        assert len(stored) == 1, stored
        out = {"run": run, "chkpt_index": ci, "solver_iteration": cells[0]["solver_iteration"],
               "stored_val_loss": cells[0]["stored_val_loss"], "evaluators": {}, "path_differences": {},
               "P0_by_process": {str(p["proc"]): c["P0"] for p, c in zip(procs, cells)}}
        vecs = {}
        for ev in EVALS:
            per_proc = []
            for c in cells:
                cs = [x for x in c["calls"] if x["evaluator"] == ev]
                per_proc.append([np.array([float(v) for v in x["per_item"]]) if "per_item" in x
                                 else np.array([float(x["mean_16"])]) for x in cs])
            vecs[ev] = per_proc
            largest = float(max(np.max(np.abs(v)) for pp in per_proc for v in pp))
            w = [pair_stats(pp, pp, list(itertools.combinations(range(5), 2)), largest) for pp in per_proc]
            cross = []
            for pa, pb in itertools.combinations(range(len(per_proc)), 2):
                cross.append(pair_stats(per_proc[pa], per_proc[pb],
                                        list(itertools.product(range(5), range(5))), largest))
            e = {"within_process_max_abs_delta_16_item_mean": r(max(float(x["max_abs_delta_16_item_mean"]) for x in w)),
                 "within_process_n_pairs": sum(x["n_pairs"] for x in w),
                 "within_process_by_process_max_abs_delta_16_item_mean": [x["max_abs_delta_16_item_mean"] for x in w],
                 "cross_process_max_abs_delta_16_item_mean": r(max(float(x["max_abs_delta_16_item_mean"]) for x in cross)),
                 "cross_process_n_pairs": sum(x["n_pairs"] for x in cross),
                 "all_15_means": [r(float(np.mean(v))) for pp in per_proc for v in pp],
                 "n_distinct_means_of_15": len({float(np.mean(v)) for pp in per_proc for v in pp})}
            if ev != "E1":
                e["within_process_max_abs_delta_per_item"] = r(max(float(x["max_abs_delta_per_item"]) for x in w))
                e["within_process_max_abs_delta_per_item_in_float32_ulps"] = r(max(float(x["max_abs_delta_per_item_in_float32_ulps"]) for x in w))
                e["cross_process_max_abs_delta_per_item"] = r(max(float(x["max_abs_delta_per_item"]) for x in cross))
                e["cross_process_max_abs_delta_per_item_in_float32_ulps"] = r(max(float(x["max_abs_delta_per_item_in_float32_ulps"]) for x in cross))
                e["float32_ulp_of_largest_per_item_value"] = w[0]["float32_ulp_of_largest_per_item_value"]
            out["evaluators"][ev] = e
        for name in ["E1-E2", "E1-E3", "E2-E3"]:
            vals = [float(v) for c in cells for v in c["path_differences"][name]["values_25"]]
            pd = {"n": len(vals), "min": r(min(vals)), "max": r(max(vals)),
                  "max_abs": r(max(abs(v) for v in vals)), "mean": r(float(np.mean(vals)))}
            if name == "E2-E3":
                pd["max_abs_delta_per_item"] = r(max(float(c["path_differences"][name]["max_abs_delta_per_item"]) for c in cells))
                pd["max_abs_delta_per_item_in_float32_ulps"] = r(max(float(c["path_differences"][name]["max_abs_delta_per_item_in_float32_ulps"]) for c in cells))
                pd["n_call_pairs_bitwise_equal_per_item"] = sum(c["path_differences"][name]["n_call_pairs_bitwise_equal_per_item"] for c in cells)
            out["path_differences"][name] = pd
        doc["cells"].append(out)
    (out_dir / a.floor_name).write_text(json.dumps(doc, indent=1))
    with open(out_dir / a.csv_name, "w", newline="") as f:
        f.write("# PREVIEW DIAGNOSTIC -- NOT A TEST\n")
        f.write(f"# script_sha256={SCRIPT_HASHES['results/diagnostics/c3/c3_evaluator_floor.py']}\n")
        f.write("run,chkpt_index,solver_iteration,process,evaluator,round,mean_16,stored_val_loss\n")
        for p in procs:
            for c in p["cells"]:
                for x in c["calls"]:
                    f.write(f"{c['run']},{c['chkpt_index']},{c['solver_iteration']},{p['proc']},"
                            f"{x['evaluator']},{x['round']},{x['mean_16']},{c['stored_val_loss']}\n")
    print("wrote", out_dir / a.floor_name, out_dir / a.csv_name)
    return 0


def main():
    a = parse_args()
    if a.task == "proc":
        return task_proc(a)
    return task_floor(a)


if __name__ == "__main__":
    sys.exit(main())
