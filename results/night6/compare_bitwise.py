"""Bitwise comparison of two training runs — the executable form of night 6's reading of (a).

Compares, with no tolerance at all:

  1. every logged loss array the run wrote to disk (`loss.h5`, `loss_flow.h5`, and the
     `training/`, `training_batch/`, `validation/`, `validation_batch/` sub-directories'
     `loss.h5` / `loss_flow.h5` / `iteration.h5`), by raw bytes, and on a difference the
     first differing index — which is the first iteration of divergence;
  2. every held-out `val_loss` the run recorded in its own json — the rung hooks
     (`rung_metrics`) and flyvis's own checkpoint passes (`checkpoint_metrics`) — by exact
     float equality on the stored values. These reach further into the run than the h5
     arrays do, because flyvis flushes those only up to the last checkpoint;
  3. every tensor of the last shared checkpoint, by sha256 over the tensor's own bytes.

`time` in a checkpoint is a wall-clock string written by flyvis at save time. It differs
between any two runs by construction and is reported separately, never as a tensor
difference. Nothing else is excused.

Usage:  compare_bitwise.py <dirA> <dirB> [--json-a run_a.json --json-b run_b.json] [--out report.json]
Exit 0 = identical, 3 = differ, 1 = usage/IO error.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import h5py
import numpy as np
import torch

H5_FIELDS = [
    "loss.h5", "loss_flow.h5",
    "training/loss.h5", "training/loss_flow.h5", "training/iteration.h5",
    "training_batch/loss.h5", "training_batch/loss_flow.h5", "training_batch/iteration.h5",
    "validation/loss.h5", "validation/loss_flow.h5", "validation/iteration.h5",
    "validation_batch/loss.h5", "validation_batch/loss_flow.h5", "validation_batch/iteration.h5",
]
TIME_KEYS = {"time"}


def read_h5(path: Path):
    with h5py.File(path, "r") as f:
        return np.array(f["data"][()])


def tensor_digests(ckpt_path: Path):
    sd = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    out = {}

    def walk(prefix, obj):
        if torch.is_tensor(obj):
            t = obj.detach().cpu().contiguous()
            out[prefix] = hashlib.sha256(t.numpy().tobytes()).hexdigest()
        elif isinstance(obj, dict):
            for k, v in obj.items():
                walk(f"{prefix}.{k}" if prefix else str(k), v)
        elif isinstance(obj, (list, tuple)):
            for i, v in enumerate(obj):
                walk(f"{prefix}[{i}]", v)
        else:
            out[prefix] = "scalar:" + repr(obj)[:160]

    walk("", sd)
    return out


def last_chkpt(d: Path):
    cps = sorted((d / "chkpts").glob("chkpt_*"))
    if not cps:
        raise SystemExit(f"no checkpoint in {d / 'chkpts'}")
    return cps[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--json-a", default=None, help="run_individual.py json for run a")
    ap.add_argument("--json-b", default=None, help="run_individual.py json for run b")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    A, B = Path(args.a), Path(args.b)
    rep = {"a": str(A), "b": str(B), "h5": {}, "differences": []}

    # ---- 1. the logged loss arrays on disk ----
    for field in H5_FIELDS:
        pa, pb = A / field, B / field
        if not (pa.exists() and pb.exists()):
            continue
        va, vb = read_h5(pa), read_h5(pb)
        ha = hashlib.sha256(va.tobytes()).hexdigest()
        hb = hashlib.sha256(vb.tobytes()).hexdigest()
        entry = {"n": [int(va.size), int(vb.size)], "dtype": str(va.dtype),
                 "sha256": [ha, hb], "identical": ha == hb and va.size == vb.size}
        if not entry["identical"]:
            n = min(va.size, vb.size)
            diff = [i for i in range(n) if va[i].tobytes() != vb[i].tobytes()]
            entry["first_divergence_index_1based"] = int(diff[0] + 1) if diff else None
            entry["n_differing"] = len(diff)
            rep["differences"].append(f"h5 {field}")
        rep["h5"][field] = entry

    # ---- 2. the val_loss values the runs recorded in their own jsons ----
    if args.json_a and args.json_b:
        da = json.loads(Path(args.json_a).read_text())
        db = json.loads(Path(args.json_b).read_text())
        for block in ("rung_metrics", "checkpoint_metrics"):
            ra = [(m["iteration"], repr(m["val_loss"])) for m in da.get(block, [])]
            rb = [(m["iteration"], repr(m["val_loss"])) for m in db.get(block, [])]
            ok = ra == rb
            rep[block] = {"n": [len(ra), len(rb)], "identical": ok,
                          "iterations": [i for i, _ in ra]}
            if not ok:
                rep[block]["first_difference"] = next(
                    (str((x, y)) for x, y in zip(ra, rb) if x != y), "length differs")
                rep["differences"].append(block)
        rep["final_iteration"] = [da.get("final_iteration"), db.get("final_iteration")]
        rep["determinism"] = [da.get("determinism"), db.get("determinism")]
        rep["nondeterministic_ops"] = [da.get("nondeterministic_ops"),
                                       db.get("nondeterministic_ops")]

    # ---- 3. the last shared checkpoint, tensor by tensor ----
    ca, cb = last_chkpt(A), last_chkpt(B)
    dga, dgb = tensor_digests(ca), tensor_digests(cb)
    keys = sorted(set(dga) | set(dgb))
    same, differ, only, time_differ = [], [], [], []
    for k in keys:
        if k not in dga or k not in dgb:
            only.append(k)
        elif dga[k] == dgb[k]:
            same.append(k)
        elif k.split(".")[-1] in TIME_KEYS:
            time_differ.append({"key": k, "a": dga[k], "b": dgb[k]})
        else:
            differ.append(k)
    rep["checkpoint"] = {
        "file": [ca.name, cb.name],
        "entries_total": len(keys),
        "entries_identical": len(same),
        "entries_differing": len(differ),
        "entries_on_one_side_only": only,
        "differing_names": differ[:40],
        "wall_clock_fields_excluded_and_differing": time_differ,
        "file_sha256": [hashlib.sha256(ca.read_bytes()).hexdigest(),
                        hashlib.sha256(cb.read_bytes()).hexdigest()],
    }
    if differ or only:
        rep["differences"].append("checkpoint tensors")

    rep["verdict"] = "BITWISE IDENTICAL" if not rep["differences"] else "DIFFER"
    print(json.dumps(rep, indent=1))
    if args.out:
        Path(args.out).write_text(json.dumps(rep, indent=1), encoding="utf-8")
    return 0 if not rep["differences"] else 3


if __name__ == "__main__":
    sys.exit(main())
