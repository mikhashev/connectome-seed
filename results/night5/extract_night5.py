#!/usr/bin/env python
"""Derive night-5 committed artefacts the same way nights 1-4's were derived.

Reproduces, for night 5 (0" = seed 0 rerun as id 9992/000 and 3''' = seed 3 rerun as
id 9992/003, both tag `night5`, ensemble 9992), the same derivative files that live in
results/night1 .. results/night4:

  - night5_<id-dash>.slim.json          the run json with the two large per-iteration
    arrays removed, asserted equal to the raw json on every other key and asserted to
    carry the same key set as a night-4 slim json.
  - iter_wall_s_<id-dash>.csv.gz        the full per-iteration wall-time array.
  - train_loss_last1000_<id-dash>.csv   the last 1000 per-iteration training losses.
  - night_report_checkpoints.csv        a TEN-run checkpoint table, extending night 4's
    eight-run one with the two new runs.

Two differences from extract_night4.py, both stated rather than left to be noticed:

  1. **The raw jsons are in the repository, not a scratchpad.** Night 4's script reads
     from `%LOCALAPPDATA%\\Temp\\claude\\...\\flyvis-probe\\night`, because that is where
     the runnable tree lived. Night 5 ran from `tools/.venv` with `--out-dir` defaulting
     to the launcher's own directory, so its raw files are `tools/night/night5_*.json`,
     gitignored by name. This script is what moves them into history; until it runs, the
     night exists only on this disk.
  2. **Two new columns, under a stated generalisation of the existing grammar.** The
     eight existing column names are kept byte-identical for continuity. The new ones are
     `val_loss_seed0primeprime` and `val_loss_seed3primeprimeprime`, reading the rule as
     "`seed<N>` followed by k `prime` tokens is the (k+1)-th run of seed N" -- which the
     existing eight already obey with k of 0 or 1. The frozen v1 reading script is not
     affected: it reads night 4's file by a pinned hash and never looks here.

Usage:
    python results/night5/extract_night5.py
"""

import csv
import gzip
import io
import json
import math
import os
import statistics

REPO = r"C:\Users\mikha\Documents\dpc-research\connectome-seed"
RAW_DIR = os.path.join(REPO, "tools", "night")
NIGHT4_DIR = os.path.join(REPO, "results", "night4")
OUT_DIR = os.path.join(REPO, "results", "night5")

DROP_KEYS = ("iter_wall_s", "train_loss_per_iter")
MACHINE_STATE_KEYS = {"machine_state_start", "machine_state_end"}
FINAL_IT = 250008

# (raw file stem, run id, dashed id, column name in the ten-run table, label)
NEW_RUNS = [
    ("night5_9992-000", "9992/000", "9992-000", "val_loss_seed0primeprime", '0"'),
    ("night5_9992-003", "9992/003", "9992-003", "val_loss_seed3primeprimeprime", "3'''"),
]

# 95% chi-squared quantiles, from scipy.stats.chi2.ppf, recorded rather than recomputed
# inline so the numbers in the README can be checked against a named source.
CHI2 = {
    3: (0.2158, 9.3484),
    4: (0.4844, 11.1433),
    5: (0.8312, 12.8325),
}


def load(path):
    with io.open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def make_slim(raw_path, slim_path, reference_keys):
    d = load(raw_path)
    slim = {k: v for k, v in d.items() if k not in DROP_KEYS}
    assert set(d.keys()) - set(slim.keys()) == set(DROP_KEYS) & set(d.keys())
    for k in slim:
        assert slim[k] == d[k]
    # Night 5 is the FIRST run to carry machine_state_start/end: the field was added to
    # run_individual.py on 2026-09-17 and had never been exercised by a run, which was its
    # own backlog entry. So exactly those two keys may be new, and nothing else may be --
    # the check is narrowed, not dropped, and a missing key still fails.
    extra = set(slim.keys()) - reference_keys
    missing = reference_keys - set(slim.keys())
    assert extra <= MACHINE_STATE_KEYS and not missing, (
        "%s: key set differs from the night-4 slim reference beyond the declared new "
        "machine-state fields\n"
        "  unexpected new : %s\n"
        "  missing        : %s"
        % (slim_path, sorted(extra - MACHINE_STATE_KEYS), sorted(missing)))
    with io.open(slim_path, "w", encoding="utf-8") as fh:
        json.dump(slim, fh, indent=1)
    return d


def write_iter_wall_csv_gz(raw, out_path):
    iw = raw.get("iter_wall_s") or []
    with gzip.open(out_path, "wt", encoding="utf-8") as fh:
        for v in iw:
            fh.write("%s\n" % v)
    return len(iw)


def write_train_loss_last1000(raw, out_path):
    tl = (raw.get("train_loss_per_iter") or [])[-1000:]
    with io.open(out_path, "w", encoding="utf-8") as fh:
        for v in tl:
            fh.write("%s\n" % v)
    return len(tl)


def read_night4_table():
    path = os.path.join(NIGHT4_DIR, "night_report_checkpoints.csv")
    with io.open(path, encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    k = 0
    comments = []
    while rows[k] and rows[k][0].startswith("#"):
        comments.append(rows[k])
        k += 1
    return comments, rows[k], rows[k + 1:]


def sd(values):
    n = len(values)
    m = sum(values) / n
    return math.sqrt(sum((v - m) ** 2 for v in values) / (n - 1))


def chi2_ci(sigma, df):
    lo_q, hi_q = CHI2[df]
    return sigma * math.sqrt(df / hi_q), sigma * math.sqrt(df / lo_q)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    ref = set(load(os.path.join(NIGHT4_DIR, "night4_9991-005.slim.json")).keys())
    raws = {}
    for stem, rid, dashed, col, label in NEW_RUNS:
        raw_path = os.path.join(RAW_DIR, stem + ".json")
        raw = make_slim(raw_path, os.path.join(OUT_DIR, stem + ".slim.json"), ref)
        raws[rid] = raw
        n_iw = write_iter_wall_csv_gz(
            raw, os.path.join(OUT_DIR, "iter_wall_s_%s.csv.gz" % dashed))
        n_tl = write_train_loss_last1000(
            raw, os.path.join(OUT_DIR, "train_loss_last1000_%s.csv" % dashed))
        print("%-6s %s  slim written | iter_wall_s %d | train_loss_last1000 %d"
              % (label, rid, n_iw, n_tl))

    # ---- the ten-run checkpoint table -------------------------------------------
    comments, header, rows = read_night4_table()
    iters = [int(r[0]) for r in rows]
    new_cols = []
    for stem, rid, dashed, col, label in NEW_RUNS:
        by_it = {c["iteration"]: c["val_loss"] for c in raws[rid]["checkpoint_metrics"]}
        missing = [it for it in iters if it not in by_it]
        assert not missing, "%s lacks checkpoints %s" % (rid, missing[:5])
        new_cols.append((col, [by_it[it] for it in iters]))

    out_path = os.path.join(OUT_DIR, "night_report_checkpoints.csv")
    with io.open(out_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["# FULL FLOAT from the run jsons' checkpoint_metrics -- same "
                    "convention as results/night4/night_report_checkpoints.csv, "
                    "extended from eight runs to TEN (adds 0\" = 9992/000 and "
                    "3''' = 9992/003)."])
        w.writerow(["# column grammar: val_loss_seed<N> followed by k 'prime' tokens is "
                    "the (k+1)-th run of seed N; the eight night-4 names are unchanged. "
                    "# script: results/night5/extract_night5.py"])
        w.writerow(header + [c for c, _v in new_cols])
        for i, row in enumerate(rows):
            w.writerow(row + ["%r" % vals[i] for _c, vals in new_cols])
    print("ten-run checkpoint table: %s (%d data rows, %d columns)"
          % (out_path, len(rows), len(header) + len(new_cols)))

    # ---- the statistics the record needs ----------------------------------------
    finals = {}
    idx = {name: i for i, name in enumerate(header)}
    last = rows[-1]
    assert int(last[0]) == FINAL_IT
    for name, i in idx.items():
        if name.startswith("val_loss_"):
            finals[name] = float(last[i])
    for col, vals in new_cols:
        finals[col] = vals[-1]

    seed_runs = {
        0: ["val_loss_seed0", "val_loss_seed0prime", "val_loss_seed0primeprime"],
        3: ["val_loss_seed3", "val_loss_seed3prime", "val_loss_seed3primeprimeprime"],
    }
    canonical = ["val_loss_seed%d" % s for s in range(6)]

    print()
    print("final val_loss at %d:" % FINAL_IT)
    for name in sorted(finals):
        print("   %-32s %.4f" % (name, finals[name]))

    ss, df = 0.0, 0
    for seed, cols in seed_runs.items():
        vals = [finals[c] for c in cols]
        m = sum(vals) / len(vals)
        ss += sum((v - m) ** 2 for v in vals)
        df += len(vals) - 1
        print("   seed %d: n=%d  SD %.4f  range %.4f"
              % (seed, len(vals), sd(vals), max(vals) - min(vals)))
    s_rep = math.sqrt(ss / df)
    s_bet = sd([finals[c] for c in canonical])
    lo_r, hi_r = chi2_ci(s_rep, df)
    lo_b, hi_b = chi2_ci(s_bet, 5)
    print()
    print("   replicate SD (pooled, all run-to-run) %.4f on %d df, 95%% CI %.4f..%.4f"
          % (s_rep, df, lo_r, hi_r))
    print("   between-individual SD (six canonical) %.4f on 5 df, 95%% CI %.4f..%.4f"
          % (s_bet, lo_b, hi_b))
    print("   ratio between/replicate = %.3f" % (s_bet / s_rep))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
