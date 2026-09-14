#!/usr/bin/env python
"""Morning report for a flyvis night run pair.

Reads two run_individual.py json outputs (a complete "run 0" and its
in-progress / complete replicate "run 0'"), and prints a Markdown report.
Handles a missing or partial `--b` file: prints whatever is present.

Usage:
    python night_report.py --a night/night1_9991-000.json --b night/rep_9991-900.json
"""

import argparse
import csv
import json
import os
import statistics
import sys


PHASE_SPLIT_ITER = 150000  # flyvis activity_penalty.stop_iter
RUNG_ITERS_OF_INTEREST = [1000, 5000, 25000, 250000]
CHECKPOINT_TARGETS = [25000, 50000, 100000, 150000, 200000, 250000]


# ---------------------------------------------------------------- loading --

def safe_load_json(path):
    """Load a json file. Returns (data, error_str). data is None on failure.

    Tolerant of a file that is mid-write (the night runner rewrites the
    partial run's json at every rung/checkpoint) or absent entirely.
    """
    if not path:
        return None, "no path given"
    if not os.path.exists(path):
        return None, f"file does not exist: {path}"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f), None
    except json.JSONDecodeError as e:
        # Most likely caught the file mid-write by the live run. Do not
        # retry in a loop (this file is read-only to us); report as-is.
        return None, f"json decode error (file likely mid-write): {e}"
    except OSError as e:
        return None, f"os error reading file: {e}"


# --------------------------------------------------------------- helpers --

def fmt_hms(seconds):
    if seconds is None:
        return "n/a"
    seconds = float(seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:d}:{m:02d}:{s:07.4f}"


def r4(x):
    """Format to a fixed 4 decimal places; 'n/a' for None; pass through
    non-numeric values unchanged."""
    if x is None:
        return "n/a"
    try:
        return f"{float(x):.4f}"
    except (TypeError, ValueError):
        return x


def rungs_by_iter(run):
    if not run:
        return {}
    return {r["iteration"]: r for r in run.get("rung_metrics", []) or []}


def checkpoints_by_iter(run):
    if not run:
        return {}
    return {c["iteration"]: c for c in run.get("checkpoint_metrics", []) or []}


def nearest_checkpoint(run, target_iter):
    """Return the checkpoint_metrics entry whose iteration is closest to
    target_iter, or None if the run has no checkpoints yet."""
    cps = (run or {}).get("checkpoint_metrics") or []
    if not cps:
        return None
    return min(cps, key=lambda c: abs(c["iteration"] - target_iter))


def median_or_na(values):
    values = list(values)
    if not values:
        return None
    return statistics.median(values)


def two_phase_price(run):
    """Return dict with phase1_median, phase2_median, overall_median (s/iter,
    over iter_wall_s, 1-indexed iteration = list index + 1) and phase1_sum,
    phase2_sum (wall-clock seconds), all None-safe for a partial run."""
    iw = (run or {}).get("iter_wall_s") or []
    n = len(iw)
    if n == 0:
        return dict(phase1_median=None, phase2_median=None, overall_median=None,
                    phase1_sum=None, phase2_sum=None, n_iters_seen=0)

    # iw[i] is the wall time of iteration i+1 (1-indexed).
    # "iterations 1,000-150,000" -> list indices 999 .. min(149999, n-1)
    phase1_slice = iw[999:PHASE_SPLIT_ITER] if n > 999 else []
    phase2_slice = iw[PHASE_SPLIT_ITER:] if n > PHASE_SPLIT_ITER else []

    return dict(
        phase1_median=median_or_na(phase1_slice),
        phase2_median=median_or_na(phase2_slice),
        overall_median=median_or_na(iw),
        phase1_sum=sum(iw[:PHASE_SPLIT_ITER]) if n > 0 else None,
        phase2_sum=sum(iw[PHASE_SPLIT_ITER:]) if n > PHASE_SPLIT_ITER else None,
        n_iters_seen=n,
    )


# ---------------------------------------------------------------- report --

def print_header(label, path, run, err, lines):
    lines.append(f"### Run {label}: `{path}`")
    if run is None:
        lines.append(f"- **status: unavailable** ({err})")
        lines.append("")
        return
    n_ckpt = len(run.get("checkpoint_metrics") or [])
    n_err = len(run.get("errors") or [])
    vram = run.get("vram")
    vram_peak = vram.get("torch_max_memory_allocated_MiB") if isinstance(vram, dict) else None
    total_wall = run.get("total_train_wall_s")
    h_run = (total_wall / 3600.0) if total_wall is not None else None

    lines.append(f"- id: `{run.get('id')}`")
    lines.append(f"- seed: {run.get('seed')}")
    lines.append(f"- exit: `{run.get('exit')}`")
    lines.append(f"- final_iteration: {run.get('final_iteration')}")
    lines.append(f"- started_utc: {run.get('started_utc')}")
    lines.append(f"- finished_utc: {run.get('finished_utc')}")
    lines.append(f"- total_train_wall_s: {r4(total_wall)}  (h:mm:ss = {fmt_hms(total_wall)})")
    lines.append(f"- h_run (computed, total_train_wall_s/3600): {r4(h_run)}")
    lines.append(f"- VRAM torch_max_memory_allocated_MiB: {r4(vram_peak) if vram_peak is not None else 'n/a (not finished / vram not yet recorded)'}")
    lines.append(f"- n checkpoints so far: {n_ckpt}")
    lines.append(f"- errors: {n_err}")
    lines.append("")


def print_two_phase(label_a, label_b, run_a, run_b, lines):
    lines.append("## Two-phase price (activity_penalty.stop_iter = 150000)")
    lines.append("")
    lines.append(f"| run | median s/iter [1,000-150,000] | median s/iter [150,001-end] | overall median s/iter | wall sum <=150,000 (s) | wall sum >150,000 (s) | iterations seen |")
    lines.append("|---|---|---|---|---|---|---|")
    for label, run in [(label_a, run_a), (label_b, run_b)]:
        if run is None:
            lines.append(f"| {label} | n/a | n/a | n/a | n/a | n/a | 0 (file unavailable) |")
            continue
        p = two_phase_price(run)
        p1m = r4(p["phase1_median"]) if p["phase1_median"] is not None else "n/a (no iterations >=1,000 yet)"
        p2m = r4(p["phase2_median"]) if p["phase2_median"] is not None else "n/a (no iterations >150,000 yet)"
        om = r4(p["overall_median"]) if p["overall_median"] is not None else "n/a"
        s1 = r4(p["phase1_sum"]) if p["phase1_sum"] is not None else "n/a"
        s2 = r4(p["phase2_sum"]) if p["phase2_sum"] is not None else "n/a (no iterations >150,000 yet)"
        lines.append(f"| {label} | {p1m} | {p2m} | {om} | {s1} | {s2} | {p['n_iters_seen']} |")
    lines.append("")
    lines.append("(Note: precomputed `iter_wall_median_all_s` / `iter_wall_median_1000_2000_s` in the json, "
                  "when present, cover different windows than this table; this table's medians/sums are "
                  "computed here from `iter_wall_s` over the windows stated in the header.)")
    for label, run in [(label_a, run_a), (label_b, run_b)]:
        if run is not None and "iter_wall_median_all_s" in run:
            lines.append(f"- {label} json field iter_wall_median_all_s: {r4(run.get('iter_wall_median_all_s'))}")
        if run is not None and "iter_wall_median_1000_2000_s" in run:
            lines.append(f"- {label} json field iter_wall_median_1000_2000_s: {r4(run.get('iter_wall_median_1000_2000_s'))}")
    lines.append("")


def print_rung_table(label_a, label_b, run_a, run_b, lines):
    lines.append("## Rung table")
    lines.append("")
    lines.append(f"| iteration | val_loss {label_a} | val_loss {label_b} | {label_b} - {label_a} | relative ({label_b}-{label_a})/{label_a} |")
    lines.append("|---|---|---|---|---|")
    ra = rungs_by_iter(run_a)
    rb = rungs_by_iter(run_b)
    for it in RUNG_ITERS_OF_INTEREST:
        a_entry = ra.get(it)
        b_entry = rb.get(it)
        a_loss = a_entry["val_loss"] if a_entry else None
        b_loss = b_entry["val_loss"] if b_entry else None
        if a_loss is None and b_loss is None:
            lines.append(f"| {it} | pending | pending | pending | pending |")
        elif b_loss is None:
            lines.append(f"| {it} | {r4(a_loss)} | pending | pending | pending |")
        elif a_loss is None:
            lines.append(f"| {it} | pending | {r4(b_loss)} | pending | pending |")
        else:
            diff = b_loss - a_loss
            rel = diff / a_loss if a_loss else None
            lines.append(f"| {it} | {r4(a_loss)} | {r4(b_loss)} | {r4(diff)} | {r4(rel) if rel is not None else 'n/a'} |")
    lines.append("")


def print_replicate_at_250k(label_a, label_b, run_a, run_b, lines):
    lines.append("## Replicate difference at iteration 250,000 (pre-registration section 7 tolerance: < 1%)")
    lines.append("")
    ra = rungs_by_iter(run_a)
    rb = rungs_by_iter(run_b)
    a_entry = ra.get(250000)
    b_entry = rb.get(250000)
    if not a_entry or not b_entry:
        missing = []
        if not a_entry:
            missing.append(label_a)
        if not b_entry:
            missing.append(label_b)
        lines.append(f"- pending (rung at iteration 250,000 not yet present for: {', '.join(missing)})")
        lines.append("")
        return
    a_loss = a_entry["val_loss"]
    b_loss = b_entry["val_loss"]
    pct = abs(a_loss - b_loss) / a_loss * 100.0
    flag = "PASS (< 1%)" if pct < 1.0 else "FAIL (>= 1%)"
    lines.append(f"- |{label_a}-{label_b}|/{label_a} at 250,000 = {r4(pct)}%  -> {flag}")
    lines.append("")


def print_checkpoint_trajectory(label_a, label_b, run_a, run_b, csv_path, lines):
    lines.append("## Checkpoint trajectory")
    lines.append("")

    ca_list = (run_a or {}).get("checkpoint_metrics") or []
    cb_list = (run_b or {}).get("checkpoint_metrics") or []
    ca = checkpoints_by_iter(run_a)
    cb = checkpoints_by_iter(run_b)

    # union of iterations, in order of appearance in A then any B-only ones,
    # sorted by iteration.
    all_iters = sorted(set(ca.keys()) | set(cb.keys()))

    lines.append(f"Compact view (every 5th checkpoint by A's index; full {len(all_iters)}-row list -> `{csv_path}`):")
    lines.append("")
    lines.append(f"| iteration | val_loss {label_a} | val_loss {label_b} |")
    lines.append("|---|---|---|")
    # step through A's own checkpoint ordering (chkpt_index) every 5th, plus
    # always include the last one A has.
    a_sorted = sorted(ca_list, key=lambda c: c["chkpt_index"]) if ca_list else []
    shown_iters = set()
    for i, c in enumerate(a_sorted):
        if i % 5 == 0 or i == len(a_sorted) - 1:
            it = c["iteration"]
            shown_iters.add(it)
    # also show any B checkpoints not covered (e.g. B is short and has few)
    for c in cb_list:
        shown_iters.add(c["iteration"])
    for it in sorted(shown_iters):
        a_loss = ca.get(it, {}).get("val_loss")
        b_loss = cb.get(it, {}).get("val_loss")
        lines.append(f"| {it} | {r4(a_loss) if a_loss is not None else 'pending'} | {r4(b_loss) if b_loss is not None else 'pending'} |")
    lines.append("")

    # write full CSV
    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["iteration", f"val_loss_{label_a}", f"val_loss_{label_b}"])
            for it in all_iters:
                a_loss = ca.get(it, {}).get("val_loss")
                b_loss = cb.get(it, {}).get("val_loss")
                w.writerow([it, r4(a_loss) if a_loss is not None else "", r4(b_loss) if b_loss is not None else ""])
        lines.append(f"(full checkpoint list written to `{csv_path}`, {len(all_iters)} rows)")
    except OSError as e:
        lines.append(f"(could not write `{csv_path}`: {e})")
    lines.append("")

    # Run-A-only detail: min held-out loss, losses at fixed iterations, plateau check
    lines.append(f"### Run {label_a} checkpoint detail")
    lines.append("")
    if not ca_list:
        lines.append("- n/a (no checkpoints)")
    else:
        min_entry = min(ca_list, key=lambda c: c["val_loss"])
        lines.append(f"- iteration of minimum held-out (checkpoint) val_loss: {min_entry['iteration']} (val_loss={r4(min_entry['val_loss'])})")
        for target in CHECKPOINT_TARGETS:
            nc = nearest_checkpoint(run_a, target)
            if nc is None:
                lines.append(f"- loss near iteration {target}: n/a")
            else:
                lines.append(f"- loss near iteration {target}: {r4(nc['val_loss'])} (nearest checkpoint at iteration {nc['iteration']})")

        final_target = CHECKPOINT_TARGETS[-1]
        earlier_target = final_target - 50000
        final_cp = nearest_checkpoint(run_a, final_target)
        earlier_cp = nearest_checkpoint(run_a, earlier_target)
        if final_cp is not None and earlier_cp is not None and earlier_cp["val_loss"]:
            rel_change = (final_cp["val_loss"] - earlier_cp["val_loss"]) / earlier_cp["val_loss"]
            if abs(rel_change) < 0.01:
                trend = "plateauing"
            elif rel_change < 0:
                trend = "still decreasing"
            else:
                trend = "still increasing"
            lines.append(
                f"- relative change of held-out loss over the last 50,000 iterations "
                f"(checkpoint near {earlier_target} -> checkpoint near {final_target}, "
                f"positive = rose): {r4(rel_change)} "
                f"({r4(earlier_cp['val_loss'])} -> {r4(final_cp['val_loss'])}; "
                f"{trend} by a <1% heuristic)"
            )
        else:
            lines.append(
                "- relative change of held-out loss over the last 50,000 iterations "
                "(positive = rose): n/a (missing checkpoints)"
            )

        # rung@250000 vs checkpoint@final_iteration discrepancy
        ra = rungs_by_iter(run_a)
        rung_250k = ra.get(250000)
        final_iter = run_a.get("final_iteration")
        final_cp_exact = ca.get(final_iter) if final_iter is not None else None
        if rung_250k is not None and final_cp_exact is not None:
            disc = final_cp_exact["val_loss"] - rung_250k["val_loss"]
            lines.append(
                f"- discrepancy: rung val_loss at iteration 250,000 ({r4(rung_250k['val_loss'])}) vs "
                f"checkpoint val_loss at iteration {final_iter} ({r4(final_cp_exact['val_loss'])}) "
                f"= {r4(disc)} over {final_iter - 250000} extra iteration(s)"
            )
        else:
            lines.append("- discrepancy rung@250,000 vs checkpoint@final_iteration: n/a (one or both missing)")

        tlpi = run_a.get("train_loss_per_iter") or []
        if len(tlpi) >= 2:
            last100 = tlpi[-100:]
            lines.append(
                f"- training-loss (train_loss_per_iter) std over last {len(last100)} iterations: "
                f"{r4(statistics.pstdev(last100))} (mean {r4(statistics.mean(last100))}) "
                f"-- for judging whether the discrepancy above is within iteration-to-iteration noise"
            )
        else:
            lines.append("- training-loss std over last 100 iterations: n/a (train_loss_per_iter absent or too short)")
    lines.append("")

    lines.append(f"### Run {label_b} checkpoint detail")
    lines.append("")
    if not cb_list:
        lines.append("- n/a (no checkpoints yet)")
    else:
        min_entry = min(cb_list, key=lambda c: c["val_loss"])
        lines.append(f"- iteration of minimum held-out (checkpoint) val_loss so far: {min_entry['iteration']} (val_loss={r4(min_entry['val_loss'])})")
        tlpi = (run_b or {}).get("train_loss_per_iter") or []
        if len(tlpi) >= 2:
            last100 = tlpi[-100:]
            lines.append(f"- training-loss std over last {len(last100)} iterations: {r4(statistics.pstdev(last100))}")
        else:
            lines.append("- training-loss std over last 100 iterations: n/a (train_loss_per_iter absent or empty)")
    lines.append("")


def print_replicate_diffs(label_a, label_b, run_a, run_b, lines):
    lines.append("## Per-rung / per-checkpoint replicate differences (section 7 instrument-floor input)")
    lines.append("")
    ra = rungs_by_iter(run_a)
    rb = rungs_by_iter(run_b)
    ca = checkpoints_by_iter(run_a)
    cb = checkpoints_by_iter(run_b)

    rung_diffs = []
    lines.append("Rungs:")
    common_rungs = sorted(set(ra.keys()) & set(rb.keys()))
    if not common_rungs:
        lines.append("- pending (no common rungs yet)")
    else:
        for it in common_rungs:
            d = abs(ra[it]["val_loss"] - rb[it]["val_loss"])
            rung_diffs.append(d)
            lines.append(f"- iteration {it}: |A-B| = {r4(d)}")
    lines.append("")

    ckpt_diffs = []
    common_ckpts = sorted(set(ca.keys()) & set(cb.keys()))
    lines.append(f"Common checkpoints ({len(common_ckpts)}):")
    if not common_ckpts:
        lines.append("- pending (no common checkpoint iterations yet)")
    else:
        for it in common_ckpts:
            d = abs(ca[it]["val_loss"] - cb[it]["val_loss"])
            ckpt_diffs.append(d)
            lines.append(f"- iteration {it}: |A-B| = {r4(d)}")
    lines.append("")

    all_diffs = rung_diffs + ckpt_diffs
    if all_diffs:
        lines.append(f"- max |A-B| across rungs+common checkpoints: {r4(max(all_diffs))}")
        lines.append(f"- median |A-B| across rungs+common checkpoints: {r4(statistics.median(all_diffs))}")
    else:
        lines.append("- max/median |A-B|: pending (no overlapping rungs or checkpoints yet)")
    lines.append("")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--a", required=True, help="path to run 0 json (e.g. night/night1_9991-000.json)")
    ap.add_argument("--b", required=True, help="path to run 0' json (e.g. night/rep_9991-900.json)")
    ap.add_argument(
        "--checkpoints-csv",
        default=None,
        help="where to write the full checkpoint CSV (default: night_report_checkpoints.csv "
             "next to this script; NOT inside night/, which is treated read-only while a run "
             "is in progress there)",
    )
    args = ap.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = args.checkpoints_csv or os.path.join(script_dir, "night_report_checkpoints.csv")

    run_a, err_a = safe_load_json(args.a)
    run_b, err_b = safe_load_json(args.b)

    label_a, label_b = "A", "B"

    lines = []
    lines.append("# Flyvis night report")
    lines.append("")
    print_header(label_a, args.a, run_a, err_a, lines)
    print_header(label_b, args.b, run_b, err_b, lines)
    print_two_phase(label_a, label_b, run_a, run_b, lines)
    print_rung_table(label_a, label_b, run_a, run_b, lines)
    print_replicate_at_250k(label_a, label_b, run_a, run_b, lines)
    print_checkpoint_trajectory(label_a, label_b, run_a, run_b, csv_path, lines)
    print_replicate_diffs(label_a, label_b, run_a, run_b, lines)

    print("\n".join(lines))


if __name__ == "__main__":
    main()
