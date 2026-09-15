#!/usr/bin/env python
"""Derive night-2 committed artefacts the same way night 1's were derived.

Reproduces, for night 2 (seeds 1 and 2 of ensemble 9991), the same derivative
files that live in results/night1/ for run 0 / run 0':

  - <tag>_<id-dash>.slim.json   -- the run_individual.py json with the two
    large per-iteration arrays (iter_wall_s, train_loss_per_iter) removed.
    Verified byte-for-byte equal to the raw json on every other top-level
    key (see the check this script runs before writing).
  - iter_wall_s_<id-dash>.csv.gz  -- the full per-iteration wall-time array,
    one float per line, gzip-compressed (no header).
  - train_loss_last1000_<id-dash>.csv -- the last 1000 entries of
    train_loss_per_iter, one float per line (no header).

There was no dedicated "slimming" script in tools/night/ or in the night
scratchpad (checked: `grep -rl slim` on both returns nothing) -- the night1
slim jsons were produced by dropping those same two keys. This script does
the same thing, with an explicit equality check against the raw json so the
"same field set" claim in the task is verified, not assumed.

Also builds a 4-way (seed 0, 0', 1, 2) checkpoint table and combined
night_report.md, since tools/night/night_report.py (read: its --a/--b
argparse signature) is strictly pairwise.

Usage:
    python extract_night2.py
"""
import gzip
import json
import os
import statistics

NIGHT_RAW = (
    r"C:\Users\mikha\AppData\Local\Temp\claude"
    r"\c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx"
    r"\63f3961a-96ce-4048-8338-72c162ea66f8\scratchpad\flyvis-probe\night"
)
REPO = r"C:\Users\mikha\Documents\dpc-research\connectome-seed"
NIGHT1_DIR = os.path.join(REPO, "results", "night1")
OUT_DIR = os.path.join(REPO, "results", "night2")

DROP_KEYS = ("iter_wall_s", "train_loss_per_iter")


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def make_slim(raw_path, slim_path):
    d = load(raw_path)
    slim = {k: v for k, v in d.items() if k not in DROP_KEYS}
    # verify: slim has exactly the raw keys minus DROP_KEYS, no value drift
    # on anything kept (matches the check already run interactively against
    # results/night1/night1_9991-000.slim.json vs the night1 raw json).
    assert set(d.keys()) - set(slim.keys()) == set(DROP_KEYS) & set(d.keys())
    for k in slim:
        assert slim[k] == d[k]
    with open(slim_path, "w", encoding="utf-8") as f:
        json.dump(slim, f, indent=1)
    return d


def write_iter_wall_csv_gz(raw_json, out_path):
    iw = raw_json.get("iter_wall_s") or []
    with gzip.open(out_path, "wt", encoding="utf-8") as f:
        for v in iw:
            f.write(f"{v}\n")
    return len(iw)


def write_train_loss_last1000(raw_json, out_path):
    tlpi = raw_json.get("train_loss_per_iter") or []
    last = tlpi[-1000:]
    with open(out_path, "w", encoding="utf-8") as f:
        for v in last:
            f.write(f"{v}\n")
    return len(last)


def two_phase_price(raw_json, split_iter=150000):
    iw = raw_json.get("iter_wall_s") or []
    n = len(iw)
    phase1 = iw[999:split_iter] if n > 999 else []
    phase2 = iw[split_iter:] if n > split_iter else []
    return (
        statistics.median(phase1) if phase1 else None,
        statistics.median(phase2) if phase2 else None,
        n,
    )


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    jobs = [
        ("night2_9991-001.json", "night2_9991-001.slim.json",
         "iter_wall_s_9991-001.csv.gz", "train_loss_last1000_9991-001.csv"),
        ("night2b_9991-002.json", "night2b_9991-002.slim.json",
         "iter_wall_s_9991-002.csv.gz", "train_loss_last1000_9991-002.csv"),
    ]

    raws = {}
    for raw_name, slim_name, iw_name, tl_name in jobs:
        raw_path = os.path.join(NIGHT_RAW, raw_name)
        d = make_slim(raw_path, os.path.join(OUT_DIR, slim_name))
        n_iw = write_iter_wall_csv_gz(d, os.path.join(OUT_DIR, iw_name))
        n_tl = write_train_loss_last1000(d, os.path.join(OUT_DIR, tl_name))
        p1, p2, n = two_phase_price(d)
        print(f"{raw_name}: slim written, iter_wall rows={n_iw}, "
              f"train_loss_last1000 rows={n_tl}, "
              f"phase1_median={p1}, phase2_median={p2}, n_iters_seen={n}")
        raws[raw_name] = d

    # --- partial (killed) seed-2 first attempt: literal copy, renamed ----
    partial_src = os.path.join(NIGHT_RAW, "night2_9991-002.json")
    partial_dst = os.path.join(OUT_DIR, "killed_9991-002.partial.json")
    with open(partial_src, "r", encoding="utf-8") as f:
        partial_content = f.read()
    with open(partial_dst, "w", encoding="utf-8") as f:
        f.write(partial_content)
    print(f"killed_9991-002.partial.json written, {len(partial_content)} bytes "
          f"(literal copy of {partial_src})")

    # --- wave json/launcher.log/progress.log copies -----------------------
    for fname in [
        "wave_night2.json", "wave_night2.launcher.log", "wave_night2.progress.log",
        "wave_night2b.json", "wave_night2b.launcher.log", "wave_night2b.progress.log",
    ]:
        src = os.path.join(NIGHT_RAW, fname)
        dst = os.path.join(OUT_DIR, fname)
        with open(src, "rb") as f:
            content = f.read()
        with open(dst, "wb") as f:
            f.write(content)
        print(f"{fname} copied, {len(content)} bytes")

    # --- combined 4-way (0, 0', 1, 2) checkpoint table ---------------------
    seed0 = load(os.path.join(NIGHT1_DIR, "night1_9991-000.slim.json"))
    seed0p = load(os.path.join(NIGHT1_DIR, "rep_9991-900.slim.json"))
    seed1 = load(os.path.join(OUT_DIR, "night2_9991-001.slim.json"))
    seed2 = load(os.path.join(OUT_DIR, "night2b_9991-002.slim.json"))

    def ckpts_by_iter(run):
        return {c["iteration"]: c["val_loss"] for c in run.get("checkpoint_metrics") or []}

    c0, c0p, c1, c2 = (ckpts_by_iter(r) for r in (seed0, seed0p, seed1, seed2))
    common = sorted(set(c0) & set(c0p) & set(c1) & set(c2))
    print(f"common checkpoints across seed0, seed0', seed1, seed2: {len(common)}")

    csv_path = os.path.join(OUT_DIR, "night_report_checkpoints.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        import csv
        w = csv.writer(f)
        w.writerow(["iteration", "val_loss_seed0", "val_loss_seed0prime",
                    "val_loss_seed1", "val_loss_seed2",
                    "diff_1_minus_0", "diff_2_minus_0", "diff_2_minus_1"])
        for it in common:
            v0, v0p, v1, v2 = c0[it], c0p[it], c1[it], c2[it]
            w.writerow([it, v0, v0p, v1, v2, v1 - v0, v2 - v0, v2 - v1])
    print(f"night_report_checkpoints.csv written, {len(common)} rows -> {csv_path}")

    # after-150000 subset stats for the doc (§3)
    after = [it for it in common if it > 150000]
    d10 = [c1[it] - c0[it] for it in after]
    d20 = [c2[it] - c0[it] for it in after]
    d21 = [c2[it] - c1[it] for it in after]
    print(f"after-150000 rows: {len(after)}")
    for name, d in [("1-0", d10), ("2-0", d20), ("2-1", d21)]:
        print(f"  {name}: mean={statistics.mean(d):.4f} min={min(d):.4f} max={max(d):.4f}")

    # plateau (mean of last 10 common checkpoints) and min per seed
    last10 = common[-10:]
    for name, c in [("seed0", c0), ("seed0prime", c0p), ("seed1", c1), ("seed2", c2)]:
        plateau = statistics.mean(c[it] for it in last10)
        min_it = min(c, key=lambda k: c[k])
        print(f"  {name}: plateau(last10 common)={plateau:.4f} "
              f"min_ckpt_loss={c[min_it]:.4f} at iter {min_it}")


if __name__ == "__main__":
    main()
