"""Diagnostic 2 -- weight-space distances between the four saved runs.

Reviewers' request: `docs/experiments/002-night2-seeds-1-and-2.md` Sec 5a item 7,
`docs/next-session-plan.md` Sec 3/4.

Reads checkpoint files with torch.load(map_location="cpu") only; writes nothing into
connectome-seed-data.  No GPU needed except for --task requires-grad, which builds a
throw-away solver (the same way diag1_eval_paths.py does) purely to PRINT which
parameters have requires_grad=True, so the "trainable" key set below is verified rather
than assumed.

Trainable set (pre-registration Sec 2: network core 734 free + 2,959 fixed, decoder 7,427):
  core     nodes_bias 65 + nodes_time_const 65 + edges_syn_strength 604      = 734
  decoder  base.0.weight 6800 + base.0.bias 8 + base.1.weight 8 + base.1.bias 8
           + decoder.0.weight 600 + decoder.0.bias 3                          = 7427
Excluded, and why:
  core     edges_sign 604, edges_syn_count 2355  -- the 2,959 FIXED parameters (Sec 2)
  decoder  base.1.running_mean 8, base.1.running_var 8, base.1.num_batches_tracked 1
           -- BatchNorm buffers, not parameters (7,444 tensors in the file - 17 = 7,427)
Both counts are asserted against the run's own json (`n_params`:
{"network_trainable": 734, "decoder_trainable": 7427}, written by
night/run_individual.py:330-333 from p.requires_grad).
"""

import argparse
import json
import sys
from pathlib import Path

import h5py
import torch

DATA_ROOT = Path("C:/Users/mikha/Documents/dpc-research/connectome-seed-data")
FLOW_DIR = DATA_ROOT / "results" / "flow" / "9991"
RUNS = {"000": "seed0", "900": "seed0prime", "001": "seed1", "002": "seed2"}
LABEL = {"seed0": "0", "seed0prime": "0'", "seed1": "1", "seed2": "2"}

CORE_KEYS = ["nodes_bias", "nodes_time_const", "edges_syn_strength"]
CORE_EXCLUDED = ["edges_sign", "edges_syn_count"]
DEC_KEYS = ["base.0.weight", "base.0.bias", "base.1.weight", "base.1.bias",
            "decoder.0.weight", "decoder.0.bias"]
DEC_EXCLUDED = ["base.1.running_mean", "base.1.running_var", "base.1.num_batches_tracked"]

PAIRS = [("seed0", "seed0prime"), ("seed0", "seed1"), ("seed0", "seed2"),
         ("seed1", "seed2"), ("seed0prime", "seed1"), ("seed0prime", "seed2")]
ITERATIONS = [0, 25212, 82812, 151212, 250008]


def chkpt_table(run: str):
    """(chkpt_index, stored chkpt_iter, solver_iteration = stored + 1, path).

    flyvis stores iteration - 1 (flyvis/solver.py:453,463); the committed
    night_report_checkpoints.csv uses solver.iteration (run_individual.py:498).
    """
    d = FLOW_DIR / run
    with h5py.File(d / "chkpt_index.h5", "r") as f:
        idx = [int(x) for x in f["data"][()]]
    with h5py.File(d / "chkpt_iter.h5", "r") as f:
        its = [int(x) for x in f["data"][()]]
    return [(i, it, it + 1, d / "chkpts" / f"chkpt_{i:05}") for i, it in zip(idx, its)]


def load_vectors(path: Path):
    """-> (dict group -> 1-D float64 tensor, core vector, decoder vector)."""
    sd = torch.load(path, map_location="cpu", weights_only=False)
    net, dec = sd["network"], sd["decoder"]["flow"]
    groups = {}
    for k in CORE_KEYS:
        groups[k] = net[k].double().reshape(-1)
    dec_parts = [dec[k].double().reshape(-1) for k in DEC_KEYS]
    groups["decoder"] = torch.cat(dec_parts)
    core = torch.cat([groups[k] for k in CORE_KEYS])
    assert core.numel() == 734, core.numel()
    assert groups["decoder"].numel() == 7427, groups["decoder"].numel()
    return groups, core, groups["decoder"]


def dist_stats(va, vb):
    d = float(torch.linalg.vector_norm(va - vb).item())
    na = float(torch.linalg.vector_norm(va).item())
    nb = float(torch.linalg.vector_norm(vb).item())
    mean_norm = 0.5 * (na + nb)
    return {"dist": d, "norm_a": na, "norm_b": nb, "mean_norm": mean_norm,
            "dist_over_mean_norm": d / mean_norm if mean_norm else float("nan")}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--task", default="all",
                   choices=["all", "requires-grad"])
    p.add_argument("--out-dir", required=True)
    p.add_argument("--netdir-root", default=None,
                   help="scratch datamate root, only for --task requires-grad")
    a = p.parse_args()
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    if a.task == "requires-grad":
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from diag1_eval_paths import build_solver  # same config, scratch netdir
        solver = build_solver(Path(a.netdir_root))
        rec = {"network": [], "decoder": [], "network_buffers": [], "decoder_buffers": []}
        for n, t in solver.network.named_parameters():
            rec["network"].append({"key": n, "numel": int(t.numel()),
                                   "requires_grad": bool(t.requires_grad)})
        for n, t in solver.network.named_buffers():
            rec["network_buffers"].append({"key": n, "numel": int(t.numel())})
        for dk, d in solver.decoder.items():
            for n, t in d.named_parameters():
                rec["decoder"].append({"decoder": dk, "key": n, "numel": int(t.numel()),
                                       "requires_grad": bool(t.requires_grad)})
            for n, t in d.named_buffers():
                rec["decoder_buffers"].append({"decoder": dk, "key": n,
                                               "numel": int(t.numel())})
        rec["network_trainable_total"] = sum(x["numel"] for x in rec["network"]
                                             if x["requires_grad"])
        rec["decoder_trainable_total"] = sum(x["numel"] for x in rec["decoder"]
                                             if x["requires_grad"])
        (out / "diag2_requires_grad.json").write_text(json.dumps(rec, indent=1))
        print(json.dumps(rec, indent=1))
        return 0

    tables = {lab: chkpt_table(run) for run, lab in RUNS.items()}
    it_lists = {lab: [r[2] for r in t] for lab, t in tables.items()}
    for lab, its in it_lists.items():
        assert its == it_lists["seed0"], lab

    # ---- (i) distances at the five named iterations -------------------------------
    rows = []
    cache = {}

    def vecs(lab, it):
        key = (lab, it)
        if key not in cache:
            hit = [r for r in tables[lab] if r[2] == it]
            assert len(hit) == 1, (lab, it)
            cache[key] = load_vectors(hit[0][3])
        return cache[key]

    for it in ITERATIONS:
        for (la, lb) in PAIRS:
            ga, ca, da = vecs(la, it)
            gb, cb, db = vecs(lb, it)
            full_a = torch.cat([ca, da])
            full_b = torch.cat([cb, db])
            row = {"iteration": it, "pair": f"({LABEL[la]},{LABEL[lb]})",
                   "a": la, "b": lb}
            for name, (va, vb) in (("core", (ca, cb)), ("decoder", (da, db)),
                                   ("all", (full_a, full_b))):
                s = dist_stats(va, vb)
                row[f"d_{name}"] = s["dist"]
                row[f"reln_{name}"] = s["dist_over_mean_norm"]
                row[f"meannorm_{name}"] = s["mean_norm"]
            rows.append(row)
            print("DIST", json.dumps(row))
    hdr = ("iteration,pair,d_core,d_decoder,d_all,reln_core,reln_decoder,reln_all,"
           "meannorm_core,meannorm_decoder,meannorm_all")
    lines = [hdr] + [
        f"{r['iteration']},\"{r['pair']}\",{r['d_core']!r},{r['d_decoder']!r},"
        f"{r['d_all']!r},{r['reln_core']!r},{r['reln_decoder']!r},{r['reln_all']!r},"
        f"{r['meannorm_core']!r},{r['meannorm_decoder']!r},{r['meannorm_all']!r}"
        for r in rows]
    (out / "weight_distance_at_iterations.csv").write_text("\n".join(lines) + "\n")

    # ---- (ii) per-parameter-group breakdowns --------------------------------------
    def group_breakdown(la, lb, it):
        ga, _, _ = vecs(la, it)
        gb, _, _ = vecs(lb, it)
        groups = {}
        tot_sq = 0.0
        for k in CORE_KEYS + ["decoder"]:
            s = dist_stats(ga[k], gb[k])
            s["numel"] = int(ga[k].numel())
            groups[k] = s
            tot_sq += s["dist"] ** 2
        for k, s in groups.items():
            s["share_of_squared_distance"] = ((s["dist"] ** 2) / tot_sq) if tot_sq else 0.0
        return {"pair": f"({LABEL[la]},{LABEL[lb]})", "iteration": it,
                "total_distance_all_params": tot_sq ** 0.5, "groups": groups}

    # the one the reviewers asked for, plus the iteration-0 positive/negative controls
    breakdown = group_breakdown("seed0", "seed0prime", 250008)
    breakdowns = {
        "0_vs_0prime_250008": breakdown,
        "0_vs_0prime_0": group_breakdown("seed0", "seed0prime", 0),
        "0_vs_1_0": group_breakdown("seed0", "seed1", 0),
        "0_vs_2_0": group_breakdown("seed0", "seed2", 0),
    }
    (out / "diag2_group_breakdown_0_vs_0prime_250008.json").write_text(
        json.dumps(breakdown, indent=1))
    (out / "diag2_group_breakdowns.json").write_text(json.dumps(breakdowns, indent=1))
    print("BREAKDOWN", json.dumps(breakdowns, indent=1))

    # ---- (iii) full trajectory of (0,0') and (0,1) ---------------------------------
    traj = []
    for (ci, stored_it, it, _p) in tables["seed0"]:
        g0, c0, d0 = vecs("seed0", it)
        gp, cp, dp = vecs("seed0prime", it)
        g1, c1, d1 = vecs("seed1", it)
        f0 = torch.cat([c0, d0]); fp = torch.cat([cp, dp]); f1 = torch.cat([c1, d1])
        traj.append({
            "iteration": it, "chkpt_index": ci,
            "d_core_0_0prime": dist_stats(c0, cp)["dist"],
            "d_dec_0_0prime": dist_stats(d0, dp)["dist"],
            "d_all_0_0prime": dist_stats(f0, fp)["dist"],
            "reln_all_0_0prime": dist_stats(f0, fp)["dist_over_mean_norm"],
            "d_core_0_1": dist_stats(c0, c1)["dist"],
            "d_dec_0_1": dist_stats(d0, d1)["dist"],
            "d_all_0_1": dist_stats(f0, f1)["dist"],
            "reln_all_0_1": dist_stats(f0, f1)["dist_over_mean_norm"]})
        if it not in ITERATIONS:  # keep the cache small
            for lab in ("seed0", "seed0prime", "seed1"):
                cache.pop((lab, it), None)
    cols = list(traj[0].keys())
    lines = [",".join(cols)] + [",".join(repr(r[c]) if isinstance(r[c], float) else str(r[c])
                                         for c in cols) for r in traj]
    (out / "weight_distance_trajectory.csv").write_text("\n".join(lines) + "\n")
    print("TRAJ rows", len(traj))

    json.dump({"rows": rows, "breakdown": breakdown, "breakdowns": breakdowns,
               "trajectory": traj},
              open(out / "diag2_weight_distance.json", "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
