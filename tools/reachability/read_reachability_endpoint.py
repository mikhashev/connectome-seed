#!/usr/bin/env python3
"""Reading script for docs/preregistration-reachability-endpoint.md — must be committed
BEFORE the reading; run ONCE; output recorded verbatim. Do not rerun under changed
constants.

Merge provenance (2026-09-18): this file is the single MERGE of two independently
written, untracked scripts, per the registration's own §10 requirement that "the
reading is executed by a script" (singular) — two scripts on disk would each make any
result "one of two readings", which is worse than none. The registration names this
path (§10: "The script is tools/reachability/read_reachability_endpoint.py"), so the
merge lands here. The other author's script, tools/night/read_reachability.py, is left
on disk untouched and is not committed; nothing below removes or edits it.

What was taken from tools/night/read_reachability.py (1108 lines, its author's
prefix "9991/xxx" run-id convention kept for continuity with its wave-json records):
  * the run -> column resolver built from the wave-json job records (scan_nights,
    build_candidates, assign_runs, and the id/token-matching helpers below) — it
    refuses (exit 2) and lists everything unmapped rather than hard-coding which CSV
    column carries which run;
  * the three review statistics (kink at iteration 150,000, cost regimes by OS boot
    session, straddle report) — printed statistics, never gating the verdict (§10);
  * the §10 JSON record and its "printed §10 quantities" table.
What was taken from tools/reachability/read_reachability_endpoint.py (the prior
version of this file, 508 lines): printing the script's own sha256 and the input
file(s)' sha256 at the head of the output, before any §3 grid constant or crossing
time; the strict literal-header guard (EXPECTED_NIGHT4_HEADER below) as a second line
of defense alongside the resolver's own per-file structural checks; the
"refuse loudly, no papering over defaults" discipline for a degenerate (empty) grid.
Newly implemented here, present in neither source, per the registration text as
reviewed (§4, §5): symmetric disqualification (see disqualify_level below) and the
exact rank statistic (see exact_rank_statistic below) — both cite the registration
section that requires them at the point they are implemented.

What this script is
--------------------
The §10 "reading executed by a script" artifact for the reachability-endpoint
pre-registration.  It executes §3's steps 1-5 in that order, prints the reading as it
goes (the verbatim stdout IS the reading), and writes every §10 recorded quantity to
reachability_reading.json.  Deterministic; stdlib only (argparse, csv, hashlib,
itertools, json, re, sys, datetime, pathlib); no numpy; no GPU; no interpolation
anywhere (§2, §11).

The registered numbers (the only loss-domain constants in this file):
  L0       COMPUTED at read time (§3 v2) = min over runs and control iterations;
           v1 used the published 1212.5556 and the top grid level then violated §6 prong 2
  step     = 2.0        (registered choice, §3) grid step in loss units
  one_step = 3600        (registered choice, §5) one checkpoint step, in iterations
The printed-only review statistics below add two iteration-domain constants (the
150000 kink boundary and the 1000 head cut), declared by that review before reading.
No hook-field number (§7) enters any computation; in v2 no loss value is hardcoded as an
anchor at all — both Lmin and L0 are computed from the substrate (§3).

The eight runs, their seeds/roles/nights are registered facts (§4, §10); which CSV
*column* carries each run is NOT hardcoded.  It is resolved at runtime from the wave
jsons (results/night{N}/wave_night{N}*.json — metadata records only) plus the
checkpoint-CSV headers, and the script REFUSES (exit 2) unless all eight runs map to
exactly one column each.  The refusal path is a feature: a wrong mapping silently
misreads the test.  A second, independent guard (§10, from the prior single-file
version of this script) pins the exact published column order of the one file the
registration names explicitly — results/night4/night_report_checkpoints.csv — and
refuses (exit 3) if that file's header does not match it verbatim, even though the
resolver above would already have derived the same mapping structurally.

Runtime column resolution
  * combined file night_report_checkpoints.csv — val_loss_seed<S> maps to the
    registered canonical run of seed <S>, val_loss_seed<S>prime to the registered
    replicate of seed <S>, provided a wave job of that night binds to that run (the
    column name must match a job seed; unmatched columns are recorded, not used);
  * pairwise file night_report_checkpoints_<X>v<Y>.csv — val_loss_A / val_loss_B map
    to the runs resolved from the filename tokens X and Y (id segment, canonical seed
    number, or 9<seed> / <seed>prime for replicates) among that night's bound jobs;
  * multiple candidates for one run must carry identical 72-point curves
    (corroboration is recorded); any disagreement, any run mappable only outside its
    registered night, any unresolvable metadata, or any unmapped run is a refusal.

Exit codes
  0  completed reading (verdict ACCEPT, FAIL, or TEST UNREADABLE)
  2  mapping refusal (the reading did not happen; nothing written)
  3  layout mismatch vs the published schema, including the night4 literal-header
     guard (the reading did not happen)
  4  §6 positive-control failure — the test is void (the report is still written)
  5  constants unresolved — the frozen grid (§3 step 3) is empty, so no multiple of
     the registered step lies strictly inside (Lmin, L0) (the reading did not happen)

Pre-reading choices recorded here because the registration does not order them:
  * verdict precedence is CONTROL FAIL (§6) > TEST UNREADABLE (§5 whole-test rule) >
    the §4 criterion — a voided test has no pass/fail/unreadable outcome to report;
  * an empty frozen grid (§3 step 3, before any exclusion) is a refusal (exit 5), not
    a verdict — distinct from an empty ACCEPTED-level set after exclusion (§4) and
    disqualification (§5), which the registration itself governs via §5's whole-test
    rule and is reported as the TEST UNREADABLE verdict, not a refusal;
  * on a control failure, the criterion-side statistics (between-gap, margins,
    loss-resolution, the rank statistic) are not computed (§6: "the criterion is then
    not read"); twin-gap and between-gap are already on the record as the §5
    disqualification quantities;
  * loss-resolution (§10 recorded statistic, not a criterion input) at an accepted
    level L = mean over the eight runs of the median per-checkpoint-step
    |d val_loss| within ±2 checkpoints of that run's crossing of L.

Printed-only review statistics (declared before reading per Ark's external review,
2026-09-17 21:47 UTC; recorded in the same single pass as everything else, never
criteria, never gating the verdict):
  * kink at iteration 150000 — per run, the least-squares slope of val_loss per
    iteration over the checkpoints with 1000 <= iteration <= 150000 (the (0,12) head
    excluded) and separately over the checkpoints with iteration > 150000; per-run
    ratio after/before, plus the pooled medians;
  * the same before/after slopes pooled separately for the two OS boot sessions of
    §10 (session A: 9991/000, 9991/900, 9991/001, 9991/002; session B: 9991/003,
    9991/903, 9991/004, 9991/005) — four pooled medians;
  * straddle report — for every accepted level, the min and max crossing iteration
    over the eight runs and whether the 150000 boundary lies strictly between them
    (some runs cross before the step, some after); plus the straddling count.

Registered printed statistic added by the 2026-09-17 review, not gating the verdict:
  * the exact rank statistic (§4, "Resolved... adopted from CC's review") — the
    positions of the 2 twin differences among the 15 between-individual differences
    at each accepted level, with the exact one-sided p from the hypergeometric/rank
    enumeration. It is printed beside twin-gap(L)/between-gap(L), never in place of
    the §4 criterion sentence, which remains the sole ACCEPT/fail rule.
"""

import argparse
import csv
import hashlib
import itertools
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------- registered constants

# L0 is COMPUTED in v2, not published: the registration's §3 anchors it to the minimum
# over the eight runs AND over CONTROL_ITERATIONS, so that §6's second prong is empty by
# construction. v1 used seed 0's iteration-0 value (1212.5556) and the top grid level then
# passed §3 while violating prong 2 (Ark, 2026-09-17). The expected value on the registered
# substrate is 1211.5978 (seed 4 at iteration 12); it is recomputed at read time, not trusted.
L0_V1_PUBLISHED = 1212.5556   # kept only to report what v1 would have used
WITHDRAWN_LEVELS = (1210.0, 1208.0)  # §11 caveat: knowledge about these is not structural
STEP = 2.0          # (registered choice, §3) loss units
ONE_STEP = 3600     # (registered choice, §5) iterations — one checkpoint step

# ------------------------------------------------------------- published layout anchors

FINAL_ITERATION = 250008            # [PUBLISHED §5] last checkpoint iteration
CONTROL_ITERATIONS = (0, 12)        # [PUBLISHED §5/§6] the two pre-step checkpoints
EXPECTED_ROWS = 72                  # [PUBLISHED §2/§5] data rows per checkpoints CSV
NIGHT_NUMBERS = (1, 2, 3, 4)        # [PUBLISHED §10]
ITERATION_COLUMN = "iteration"
COMBINED_CSV_NAME = "night_report_checkpoints.csv"
CSV_GLOB = "night_report_checkpoints*.csv"
WAVE_GLOB_TEMPLATE = "wave_night{n}*.json"
JSON_NAME = "reachability_reading.json"
REGISTRATION_DOC = "docs/preregistration-reachability-endpoint.md"
SCRIPT_REL_PATH = "tools/reachability/read_reachability_endpoint.py"

RE_SEED_COL = re.compile(r"^val_loss_seed(\d+)$")
RE_SEED_PRIME_COL = re.compile(r"^val_loss_seed(\d+)prime$")
RE_PAIRWISE_NAME = re.compile(r"^night_report_checkpoints_(.+)v(.+)\.csv$")

# Second line of defense (§10, from the prior single-file version of this script):
# the literal published header of the one file the registration names by path in its
# "four operational choices" bullet — results/night4/night_report_checkpoints.csv —
# which the registration records as carrying two leading comment lines before this
# exact header row. The resolver's structural checks (load_checkpoint_file, below)
# already guard every file it reads (one 'iteration' column, val_loss* columns, no
# duplicates, the published anchors present); this check additionally pins the exact
# column order of this specific named file and refuses loudly on any deviation.
EXPECTED_NIGHT4_HEADER = (
    "iteration",
    "val_loss_seed0",
    "val_loss_seed0prime",
    "val_loss_seed1",
    "val_loss_seed2",
    "val_loss_seed3",
    "val_loss_seed4",
    "val_loss_seed3prime",
    "val_loss_seed5",
)

# The eight runs: (run_id, id_segment, seed, role, night).
# Registered facts (§4 replicate pairs; §10 "the eight runs, by night"); the CSV
# column for each run is resolved at runtime, never hardcoded.
RUN_SPECS = [
    ("9991/000", "000", 0, "canonical", 1),   # seed 0
    ("9991/900", "900", 0, "replicate", 1),   # replicate 0-prime
    ("9991/001", "001", 1, "canonical", 2),   # seed 1
    ("9991/002", "002", 2, "canonical", 2),   # seed 2 (the night2b restart)
    ("9991/003", "003", 3, "canonical", 3),   # seed 3
    ("9991/903", "903", 3, "replicate", 4),   # replicate 3-prime
    ("9991/004", "004", 4, "canonical", 3),   # seed 4
    ("9991/005", "005", 5, "canonical", 4),   # seed 5
]
RUN_IDS = [s[0] for s in RUN_SPECS]
RUN_BY_ID = {s[0]: s for s in RUN_SPECS}
SEGMENT_TO_RUN = {s[1]: s[0] for s in RUN_SPECS}
TWIN_PAIRS = (("9991/000", "9991/900"), ("9991/003", "9991/903"))
CANONICAL_SIX = ("9991/000", "9991/001", "9991/002", "9991/003", "9991/004", "9991/005")
CANONICAL_PAIRS = list(itertools.combinations(CANONICAL_SIX, 2))   # 15 pairs

# -------- printed-only review statistics (Ark, external review, 2026-09-17 21:47 UTC)
# Never criteria, never gating the verdict; declared before reading.

KINK_ITERATION = 150000        # iteration boundary of the schedule signature (printed only)
SLOPE_MIN_ITERATION = 1000     # the "before" slope fit uses checkpoints from the first rung >= this
SESSION_A = ("9991/000", "9991/900", "9991/001", "9991/002")   # §10 OS boot session A
SESSION_B = ("9991/003", "9991/903", "9991/004", "9991/005")   # §10 OS boot session B


class LayoutMismatch(Exception):
    """The files on disk do not match the published layout (exit 3)."""


class MappingRefusal(Exception):
    """The resolver could not map all eight runs to exactly one column each (exit 2)."""


class ConstantsUnresolved(Exception):
    """A §3 grid constant cannot be resolved from the registration's stated order,
    e.g. the frozen grid at §3 step 3 is empty (exit 5)."""


# ---------------------------------------------------------------------------- helpers

def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fmt(x, nd=2):
    if x is None:
        return "-"
    if isinstance(x, int):
        return str(x)
    if x == int(x):
        return str(int(x))
    return "{:.{}f}".format(x, nd)


def rel(path, repo):
    try:
        return path.relative_to(repo).as_posix()
    except ValueError:
        return path.as_posix()


def mean(xs):
    return sum(xs) / len(xs)


def median(xs):
    s = sorted(xs)
    n = len(s)
    if n == 0:
        return None
    if n % 2 == 1:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2.0


def median_of(values):
    """Median over the non-None entries; None if there are none."""
    present = [v for v in values if v is not None]
    return median(present) if present else None


def lsq_slope(points):
    """Simple least-squares slope dy/dx over (x, y) points; None if degenerate."""
    n = len(points)
    if n < 2:
        return None
    xbar = sum(p[0] for p in points) / n
    ybar = sum(p[1] for p in points) / n
    sxx = sum((p[0] - xbar) ** 2 for p in points)
    if sxx == 0:
        return None
    return sum((p[0] - xbar) * (p[1] - ybar) for p in points) / sxx


def build_grid(lmin, l0):
    """All L = m*STEP, integer m, strictly inside the open interval (lmin, l0) (§3, v2).

    Both anchors are computed at read time in v2: lmin from the curve minima, l0 from the
    control iterations. The two levels of WITHDRAWN_LEVELS are removed here, by the §11
    caveat written before the reading -- not on any result.
    """
    levels = []
    m = int(lmin // STEP) + 1
    while m * STEP <= lmin:
        m += 1
    while m * STEP < l0:
        levels.append(m * STEP)
        m += 1
    kept = [L for L in levels if L not in WITHDRAWN_LEVELS]
    return kept, [L for L in levels if L in WITHDRAWN_LEVELS]


def first_index_at_or_below(values, level):
    """Index of the FIRST checkpoint whose value is <= level; None if never (§2)."""
    for i, v in enumerate(values):
        if v <= level:
            return i
    return None


def exact_rank_statistic(twin_diffs, between_diffs):
    """§4 (Resolved, raised by Ark, 2026-09-17; adopted from CC's review, 2026-09-17):
    the exact rank statistic -- the positions of the 2 twin differences among the 15
    between-individual differences, with the exact one-sided p from the
    hypergeometric/rank enumeration. This is a PRINTED, REGISTERED statistic (§4,
    §10) -- it does NOT replace the §4 criterion sentence, which remains the
    deterministic ACCEPT/fail rule; the rank statistic is reported beside it, never
    instead of it.

    Method: pool the 2 twin differences and 15 between differences (17 values total,
    for one accepted level), rank them 1..17 ascending (ties, if any, broken by a
    fixed twin-before-between order -- documented, not hidden, since it is not
    decidable from the registration text which convention to use in the tied case),
    and compute the one-sided exact p-value as the fraction of the C(17,2) = 136 ways
    of choosing 2 of the 17 rank positions whose rank sum is <= the observed twin
    rank sum -- the standard exact two-sample Wilcoxon/Mann-Whitney enumeration for
    n1=2, n2=15 under the null that the twin/between label is exchangeable across the
    17 differences (there is no other null model available here: §4, "a permutation
    null over which runs are declared twins is not available").

    With 2 against 15 the smallest attainable one-sided p is 1/C(17,2) = 1/136
    ~= 0.0074 (registration §4) -- attained only when both twin differences occupy
    the two smallest ranks (1 and 2), the unique rank pair with the minimum possible
    sum (1 + 2 = 3).
    """
    labeled = [(v, 0) for v in twin_diffs] + [(v, 1) for v in between_diffs]
    ordered = sorted(range(len(labeled)), key=lambda i: (labeled[i][0], labeled[i][1]))
    rank_of = {}
    for rank, idx in enumerate(ordered, start=1):
        rank_of[idx] = rank
    twin_ranks = sorted(rank_of[i] for i in range(len(twin_diffs)))
    observed_sum = sum(twin_ranks)
    n_total = len(labeled)
    n_twin = len(twin_diffs)
    combos = list(itertools.combinations(range(1, n_total + 1), n_twin))
    at_least_as_extreme = sum(1 for combo in combos if sum(combo) <= observed_sum)
    return {
        "twin_ranks": twin_ranks,
        "rank_sum_twin": observed_sum,
        "n_total": n_total,
        "n_twin": n_twin,
        "total_combinations": len(combos),
        "at_least_as_extreme": at_least_as_extreme,
        "one_sided_p": at_least_as_extreme / len(combos),
    }


# ------------------------------------------------------------------ file reading layer

def read_table(path):
    """CSV with '#' comment lines, then a header row, then data rows.

    Reads the raw bytes once and returns their sha256 alongside the parsed table
    (§10, "its own sha256 and the input file's sha256 are printed at the head of its
    output" -- generalised here to every substrate checkpoint CSV the resolver
    validates, since the resolver, unlike the prior single-file script, reads more
    than one file).
    """
    try:
        raw_bytes = path.read_bytes()
    except OSError as exc:
        raise LayoutMismatch("cannot read {}: {}".format(path, exc)) from exc
    digest = hashlib.sha256(raw_bytes).hexdigest()
    try:
        text = raw_bytes.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise LayoutMismatch("{}: not valid UTF-8 text: {}".format(path, exc)) from exc
    raw = list(csv.reader(text.splitlines()))
    table = []
    for row in raw:
        if not row or all(str(cell).strip() == "" for cell in row):
            continue
        if str(row[0]).lstrip().startswith("#"):
            continue
        table.append([str(cell) for cell in row])
    if not table:
        raise LayoutMismatch("{}: no header row found below the '#' comments".format(path))
    return table[0], table[1:], digest


def load_checkpoint_file(path):
    """Validate one checkpoints CSV against the published layout and index its columns."""
    header_raw, rows, digest = read_table(path)
    header = [h.strip() for h in header_raw]

    # Second line of defense (§10): the one file the registration names explicitly by
    # path gets its exact published column order pinned and checked, on top of the
    # structural checks below that apply to every file the resolver reads.
    if path.name == COMBINED_CSV_NAME and path.parent.name == "night4":
        if tuple(header) != EXPECTED_NIGHT4_HEADER:
            raise LayoutMismatch(
                "{}: header does not match the registration's §10 published layout "
                "for this specific file exactly.\n  expected: {}\n  found:    {}".format(
                    path, EXPECTED_NIGHT4_HEADER, tuple(header)))

    if header.count(ITERATION_COLUMN) != 1:
        raise LayoutMismatch(
            "{}: expected exactly one '{}' column; header is {}".format(
                path, ITERATION_COLUMN, header))
    it_idx = header.index(ITERATION_COLUMN)
    if len(rows) != EXPECTED_ROWS:
        raise LayoutMismatch(
            "{}: expected {} data rows after the header, found {}".format(
                path, EXPECTED_ROWS, len(rows)))
    iterations = []
    for rnum, row in enumerate(rows, start=1):
        cell = row[it_idx].strip() if it_idx < len(row) else ""
        try:
            it = float(cell)
        except ValueError:
            raise LayoutMismatch(
                "{}: data row {}: iteration cell {!r} is not a number".format(
                    path, rnum, cell)) from None
        if it != int(it):
            raise LayoutMismatch(
                "{}: data row {}: iteration {!r} is not an integer".format(path, rnum, cell))
        iterations.append(int(it))
    for i in range(len(iterations) - 1):
        if iterations[i] >= iterations[i + 1]:
            raise LayoutMismatch(
                "{}: iteration column not strictly increasing ({} -> {} at data row {})".format(
                    path, iterations[i], iterations[i + 1], i + 2))
    for anchor in CONTROL_ITERATIONS + (FINAL_ITERATION,):
        if anchor not in iterations:
            raise LayoutMismatch(
                "{}: iteration {} absent from the checkpoint grid (read what is there, "
                "but the endpoints of §5/§6 are required)".format(path, anchor))
    loss_cols = {}
    for idx, name in enumerate(header):
        if idx == it_idx or not name.startswith("val_loss"):
            continue
        if name in loss_cols:
            raise LayoutMismatch("{}: duplicate val_loss column {!r}".format(path, name))
        loss_cols[name] = idx
    if not loss_cols:
        raise LayoutMismatch("{}: no val_loss* columns in header {}".format(path, header))
    return {"path": path, "name": path.name, "iterations": iterations,
            "loss_cols": loss_cols, "rows": rows, "sha256": digest}


def column_values(fileinfo, column, repo):
    idx = fileinfo["loss_cols"][column]
    values = []
    for rnum, row in enumerate(fileinfo["rows"], start=1):
        cell = row[idx].strip() if idx < len(row) else ""
        if cell == "":
            raise LayoutMismatch("{}: empty cell in column {!r}, data row {}".format(
                rel(fileinfo["path"], repo), column, rnum))
        try:
            values.append(float(cell))
        except ValueError:
            raise LayoutMismatch("{}: column {!r}, data row {}: {!r} is not a number".format(
                rel(fileinfo["path"], repo), column, rnum, cell)) from None
    return values


# ------------------------------------------------------------------- wave json layer

def extract_job_records(node):
    """Tolerant walk: every dict carrying both 'id' and 'seed' is a job record."""
    records = []
    if isinstance(node, dict):
        if "id" in node and "seed" in node:
            records.append(node)
        for value in node.values():
            records.extend(extract_job_records(value))
    elif isinstance(node, list):
        for value in node:
            records.extend(extract_job_records(value))
    return records


def load_wave_jobs(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise LayoutMismatch("cannot parse wave json {}: {}".format(path, exc)) from exc
    jobs, seen = [], set()
    for rec in extract_job_records(data):
        jid = str(rec.get("id", "")).strip()
        try:
            seed = int(rec.get("seed"))
        except (TypeError, ValueError):
            seed = None
        tag = str(rec.get("tag") or "").strip()
        key = (jid, seed, tag)
        if jid == "" or key in seen:
            continue
        seen.add(key)
        jobs.append({"id": jid, "seed": seed, "tag": tag, "wave": path.name})
    if not jobs:
        raise LayoutMismatch("{}: no job records carrying id and seed found".format(path))
    return jobs


def id_segments(jid):
    return [seg for seg in re.split(r"[\\/]+", jid) if seg]


def bind_job_to_run(job):
    """Bind a wave job to a registered run by id segments, rightmost first."""
    for seg in reversed(id_segments(job["id"])):
        rid = SEGMENT_TO_RUN.get(seg)
        if rid is not None:
            return rid
    return None


# ----------------------------------------------------------------------- the resolver

def scan_nights(repo):
    """Inventory nights: wave jsons, bound jobs, validated checkpoint CSVs."""
    problems = []
    nights = {}
    validated = []
    unrecognized = []
    for n in NIGHT_NUMBERS:
        ndir = repo / "results" / ("night{}".format(n))
        if not ndir.is_dir():
            raise LayoutMismatch("missing directory {}".format(ndir))
        wave_paths = sorted(ndir.glob(WAVE_GLOB_TEMPLATE.format(n=n)))
        if not wave_paths:
            raise LayoutMismatch("{}: no wave jsons matching '{}'".format(
                ndir, WAVE_GLOB_TEMPLATE.format(n=n)))
        jobs = []
        for wp in wave_paths:
            jobs.extend(load_wave_jobs(wp))
        bound = {}
        unbound = []
        for job in jobs:
            rid = bind_job_to_run(job)
            if rid is None:
                unbound.append(job)
                continue
            _, _, seed, role, _ = RUN_BY_ID[rid]
            if job["seed"] is not None and job["seed"] != seed:
                problems.append(
                    "night {}, wave {}: job id {!r} declares seed {} but registered run "
                    "{} has seed {}".format(n, job["wave"], job["id"], job["seed"], rid, seed))
            is_rep_tag = "rep" in job["tag"].lower()
            if job["tag"] and is_rep_tag != (role == "replicate"):
                problems.append(
                    "night {}, wave {}: job id {!r} tag {!r} disagrees with the registered "
                    "role of {} ({})".format(n, job["wave"], job["id"], job["tag"], rid, role))
            bound.setdefault(rid, []).append(job)
        csv_paths = sorted(ndir.glob(CSV_GLOB))
        if not csv_paths:
            raise LayoutMismatch("{}: no checkpoint CSVs matching '{}'".format(ndir, CSV_GLOB))
        combined, pairwise = [], []
        for cp in csv_paths:
            if cp.name == COMBINED_CSV_NAME:
                fi = load_checkpoint_file(cp)
                combined.append(fi)
                validated.append(fi)
                continue
            m = RE_PAIRWISE_NAME.match(cp.name)
            if m:
                fi = load_checkpoint_file(cp)
                pairwise.append((fi, m.group(1), m.group(2)))
                validated.append(fi)
            else:
                unrecognized.append(rel(cp, repo))
        nights[n] = {"dir": ndir, "wave_paths": wave_paths, "jobs": jobs,
                     "bound": bound, "unbound": unbound,
                     "combined": combined, "pairwise": pairwise}
    grids = {tuple(fi["iterations"]) for fi in validated}
    if len(grids) != 1:
        names = sorted({rel(fi["path"], repo) for fi in validated})
        raise LayoutMismatch(
            "checkpoint files do not share one iteration grid: " + "; ".join(names))
    return nights, validated, list(next(iter(grids))), unrecognized, problems


def spec_for(seed, role):
    for s in RUN_SPECS:
        if s[2] == seed and s[3] == role:
            return s
    return None


def resolve_token(token, info):
    """Resolve a pairwise filename token to a registered run via this night's bound jobs."""
    hits = set()
    for rid, joblist in info["bound"].items():
        for job in joblist:
            if token in id_segments(job["id"]):
                hits.add(rid)
    if len(hits) == 1:
        return hits.pop()
    seeds = {rid for rid in info["bound"]
             if RUN_BY_ID[rid][3] == "canonical" and str(RUN_BY_ID[rid][2]) == token}
    if len(seeds) == 1:
        return seeds.pop()
    reps = {rid for rid in info["bound"]
            if RUN_BY_ID[rid][3] == "replicate"
            and token in ("9{}".format(RUN_BY_ID[rid][2]), "{}prime".format(RUN_BY_ID[rid][2]))}
    if len(reps) == 1:
        return reps.pop()
    return None


def build_candidates(repo, nights):
    candidates = {rid: [] for rid in RUN_IDS}
    unmapped_columns = []
    pairwise_notes = []

    def add_unmapped(fi, col, reason):
        unmapped_columns.append(
            {"file": rel(fi["path"], repo), "column": col, "reason": reason})

    for n in sorted(nights):
        info = nights[n]
        for fi in info["combined"]:
            for col in sorted(fi["loss_cols"], key=lambda c: fi["loss_cols"][c]):
                m = RE_SEED_PRIME_COL.match(col)
                if m:
                    seed = int(m.group(1))
                    spec = spec_for(seed, "replicate")
                    if spec is not None and spec[0] in info["bound"]:
                        candidates[spec[0]].append({
                            "night": n, "file": fi, "column": col,
                            "col_idx": fi["loss_cols"][col], "kind": "combined",
                            "how": "val_loss_seed{}prime <-> bound replicate job of seed {} "
                                   "in night {}".format(seed, seed, n)})
                    else:
                        add_unmapped(fi, col, "no bound replicate job of seed {} in night "
                                              "{}'s waves".format(seed, n))
                    continue
                m = RE_SEED_COL.match(col)
                if m:
                    seed = int(m.group(1))
                    spec = spec_for(seed, "canonical")
                    if spec is not None and spec[0] in info["bound"]:
                        candidates[spec[0]].append({
                            "night": n, "file": fi, "column": col,
                            "col_idx": fi["loss_cols"][col], "kind": "combined",
                            "how": "val_loss_seed{} <-> bound canonical job of seed {} in "
                                   "night {}".format(seed, seed, n)})
                    else:
                        add_unmapped(fi, col, "no bound canonical job of seed {} in night "
                                              "{}'s waves".format(seed, n))
                    continue
                add_unmapped(fi, col, "column name matches no registered grammar")
        for fi, xtok, ytok in info["pairwise"]:
            if not ("val_loss_A" in fi["loss_cols"] and "val_loss_B" in fi["loss_cols"]):
                raise LayoutMismatch(
                    "{}: pairwise file lacks val_loss_A/val_loss_B (val_loss columns: {})".format(
                        rel(fi["path"], repo), sorted(fi["loss_cols"])))
            xrun = resolve_token(xtok, info)
            yrun = resolve_token(ytok, info)
            label = "{}v{}".format(xtok, ytok)
            if xrun is None or yrun is None:
                bad = xtok if xrun is None else ytok
                pairwise_notes.append(
                    "{}: token {!r} matches no bound job of night {}; file unused".format(
                        rel(fi["path"], repo), bad, n))
                continue
            candidates[xrun].append({
                "night": n, "file": fi, "column": "val_loss_A",
                "col_idx": fi["loss_cols"]["val_loss_A"], "kind": "pairwise",
                "how": "pairwise {}: side A token {!r}".format(label, xtok)})
            candidates[yrun].append({
                "night": n, "file": fi, "column": "val_loss_B",
                "col_idx": fi["loss_cols"]["val_loss_B"], "kind": "pairwise",
                "how": "pairwise {}: side B token {!r}".format(label, ytok)})
            for col in sorted(fi["loss_cols"], key=lambda c: fi["loss_cols"][c]):
                if col not in ("val_loss_A", "val_loss_B"):
                    add_unmapped(fi, col, "extra val_loss column in a pairwise file")
    return candidates, unmapped_columns, pairwise_notes


def describe_candidate(c, repo):
    return "{}:{} (night {}, {}; {})".format(
        rel(c["file"]["path"], repo), c["column"], c["night"], c["kind"], c["how"])


def assign_runs(repo, candidates, problems):
    """All eight runs must map to exactly one column each, or refuse (batched message)."""
    assignment = {}
    corroboration = {rid: [] for rid in RUN_IDS}
    failures = list(problems)
    for rid in RUN_IDS:
        reg_night = RUN_BY_ID[rid][4]
        on_night = [c for c in candidates[rid] if c["night"] == reg_night]
        off_night = [c for c in candidates[rid] if c["night"] != reg_night]
        if not on_night:
            if off_night:
                failures.append(
                    "{}: no candidate column in its registered night {}; only off-night "
                    "candidates seen: {}".format(
                        rid, reg_night,
                        "; ".join(describe_candidate(c, repo) for c in off_night)))
            else:
                failures.append("{}: no candidate column found in any night".format(rid))
            continue
        on_night.sort(key=lambda c: (0 if c["kind"] == "combined" else 1,
                                     c["file"]["name"], c["col_idx"]))
        off_night.sort(key=lambda c: (c["night"], c["file"]["name"], c["col_idx"]))
        loaded = [(c, column_values(c["file"], c["column"], repo))
                  for c in on_night + off_night]
        base_c, base_vals = loaded[0]
        agree = True
        for c, vals in loaded[1:]:
            if vals != base_vals:
                failures.append(
                    "{}: candidate columns disagree on the curve — {} differs from {}".format(
                        rid, describe_candidate(c, repo), describe_candidate(base_c, repo)))
                agree = False
        if not agree:
            continue
        assignment[rid] = {"candidate": on_night[0], "values": base_vals}
        corroboration[rid] = [c for c, _ in loaded[1:]]
    if failures:
        raise MappingRefusal(
            "mapping refusal — the resolver will not guess (a wrong mapping silently "
            "misreads the test). Not all eight runs map to exactly one column each:\n  - "
            + "\n  - ".join(failures))
    seen = {}
    for rid, a in assignment.items():
        c = a["candidate"]
        key = (str(c["file"]["path"]), c["column"])
        if key in seen:
            raise MappingRefusal("column {}:{} was assigned to both {} and {}".format(
                c["file"]["path"], c["column"], seen[key], rid))
        seen[key] = rid
    if len(assignment) != len(RUN_IDS):
        raise MappingRefusal("internal error: assignment incomplete after all checks")
    return assignment, corroboration


# --------------------------------------------------------------------- the reading

def print_banner(repo, started, script_sha256, validated_files):
    print("=" * 78)
    print("Reachability endpoint reading — " + REGISTRATION_DOC)
    print("Executed by this script, run once; this output is the reading (§10).")
    print("UTC started : " + started)
    print("Repo root   : " + str(repo))
    print("Script path : " + str(Path(__file__).resolve()))
    print("Script sha256: " + script_sha256)
    print("Input file(s) sha256 (§10: 'its own sha256 and the input file's sha256 are "
          "printed at the head of its output' — generalised here to every substrate "
          "checkpoint CSV the resolver validated, since this reading covers more than "
          "the single file the phrase names):")
    for fi in sorted(validated_files, key=lambda f: rel(f["path"], repo)):
        print("  {} : {}".format(rel(fi["path"], repo), fi["sha256"]))
    print("Constants   : step = {} [registered, §3], one_step = {} iterations "
          "[registered, §5]; Lmin and L0 are COMPUTED at read time in v2 (§3) and are "
          "printed in §3 step 2 below, not here".format(STEP, ONE_STEP))
    print("No interpolation is used anywhere; no hook-field number enters any "
          "computation (§7, §11).")
    print("=" * 78)


def section(title):
    print("\n" + "-" * 78)
    print(title)
    print("-" * 78)


def run_reading(repo, started):
    script_sha256 = hashlib.sha256(Path(__file__).resolve().read_bytes()).hexdigest()

    # Resolve the run->column mapping and validate every substrate file first, so
    # that provenance (script + every input file's sha256, §10) can be printed at the
    # very head of the output, before any §3 grid constant or crossing time exists.
    nights, validated_files, iterations, unrecognized, problems = scan_nights(repo)

    print_banner(repo, started, script_sha256, validated_files)

    # ---- §3 step 1: mapping + the eight iteration-250008 values ------------------
    section("§3 step 1 — resolved run->column mapping; the eight "
            "iteration-{} values".format(FINAL_ITERATION))
    candidates, unmapped_columns, pairwise_notes = build_candidates(repo, nights)
    assignment, corroboration = assign_runs(repo, candidates, problems)

    curves = {rid: assignment[rid]["values"] for rid in RUN_IDS}
    pos = {it: i for i, it in enumerate(iterations)}
    end_pos = pos[FINAL_ITERATION]

    print("wave metadata (json records only; no curve values are read from them):")
    for n in NIGHT_NUMBERS:
        info = nights[n]
        print("  night {}: {}".format(
            n, ", ".join(rel(wp, repo) for wp in info["wave_paths"])))
        pieces = []
        for rid in RUN_IDS:
            if rid in info["bound"]:
                job = info["bound"][rid][0]
                pieces.append("{} (seed {}, tag {})".format(rid, job["seed"],
                                                            job["tag"] or "-"))
        print("    bound jobs: " + ("; ".join(pieces) if pieces else "(none of the eight)"))

    print("\ncheckpoint CSVs scanned and validated against the published layout "
          "({} data rows, one '{}' column):".format(EXPECTED_ROWS, ITERATION_COLUMN))
    for fi in validated_files:
        print("  {}  (val_loss columns: {})".format(
            rel(fi["path"], repo), ", ".join(sorted(fi["loss_cols"]))))

    print("\nrun -> column assignment (all eight runs, exactly one column each):")
    for rid in RUN_IDS:
        c = assignment[rid]["candidate"]
        spec = RUN_BY_ID[rid]
        print("  {}  seed {}  {:<10}  night {}  {}:{}  [{}]".format(
            rid, spec[2], spec[3], spec[4], rel(c["file"]["path"], repo),
            c["column"], c["kind"]))
        for extra in corroboration[rid]:
            print("    corroborated by {}:{} (identical 72-point curve)".format(
                rel(extra["file"]["path"], repo), extra["column"]))
    if unmapped_columns:
        print("\ncolumns seen but NOT mapped (recorded, unused):")
        for u in unmapped_columns:
            print("  {}:{} — {}".format(u["file"], u["column"], u["reason"]))
    if pairwise_notes:
        print("\npairwise files not used:")
        for note in pairwise_notes:
            print("  " + note)
    if unrecognized:
        print("\nfiles matching the checkpoint glob but no registered name pattern "
              "(recorded, not parsed):")
        for u in unrecognized:
            print("  " + u)
    unbound_all = [(n, j) for n in NIGHT_NUMBERS for j in nights[n]["unbound"]]
    if unbound_all:
        print("\nwave jobs not bound to any of the eight registered runs (recorded, unused):")
        for n, j in unbound_all:
            print("  night {} {}: id {!r} seed {} tag {!r}".format(
                n, j["wave"], j["id"], j["seed"], j["tag"]))

    print("\niteration grid as read (recorded, not assumed) — {} points, first {}, "
          "second {}, last {}:".format(len(iterations), iterations[0], iterations[1],
                                       iterations[-1]))
    print("  " + ", ".join(str(it) for it in iterations))

    end_values = {rid: curves[rid][end_pos] for rid in RUN_IDS}
    print("\nthe eight iteration-{} curve values:".format(FINAL_ITERATION))
    for rid in RUN_IDS:
        print("  {} : {:.4f}".format(rid, end_values[rid]))

    # ---- §3 step 2: the two anchors (v2) -------------------------------------------
    section("§3 step 2 — Lmin and L0, both computed")
    # Lmin governs §4's exclusion rule, which fires when a run NEVER crosses a level --
    # decided by each run's CURVE MINIMUM, not by its final value. v1 used the minimum of
    # the finals and lost 8 of 34 levels by construction (Ark, 2026-09-17; §3 v2).
    curve_min = {rid: min(curves[rid]) for rid in RUN_IDS}
    print("curve minimum per run (the quantity §4's exclusion rule actually depends on):")
    for rid in RUN_IDS:
        print("  {} : {:.4f}".format(rid, curve_min[rid]))
    lmin = max(curve_min.values())
    lmin_runs = [rid for rid in RUN_IDS if curve_min[rid] == lmin]
    print("Lmin = MAX over the eight curve minima = {:.4f} (attained by {})".format(
        lmin, ", ".join(lmin_runs)))
    print("  (v1 would have used min over the finals = {:.4f} -- the wrong quantity)".format(
        min(end_values.values())))
    # L0 must clear §6 prong 2, which tests against CONTROL_ITERATIONS of ALL runs.
    side_vals = {(rid, it): curves[rid][pos[it]] for rid in RUN_IDS for it in CONTROL_ITERATIONS}
    l0 = min(side_vals.values())
    l0_at = [k for k, v in side_vals.items() if v == l0]
    print("L0 = MIN over runs and control iterations {} = {:.4f} (attained by {})".format(
        list(CONTROL_ITERATIONS), l0,
        ", ".join("{}@{}".format(rid, it) for rid, it in l0_at)))
    print("  (v1 would have used seed 0's iteration-0 value = {} -- above prong 2's own "
          "minimum, so the top level passed §3 and violated the control)".format(L0_V1_PUBLISHED))

    # ---- §3 step 3: the frozen grid ------------------------------------------------
    section("§3 step 3 — the frozen grid")
    grid, withdrawn = build_grid(lmin, l0)
    if withdrawn:
        print("withdrawn by the §11 caveat, written before the reading: {}".format(
            ", ".join(fmt(L) for L in withdrawn)))
    print("all levels L = m * {} strictly inside (Lmin, L0) = ({:.4f}, {:.4f}):".format(
        STEP, lmin, l0))
    print("  {} level(s): {}".format(
        len(grid), ", ".join(fmt(L) for L in grid) if grid else "(none)"))
    if not grid:
        raise ConstantsUnresolved(
            "the frozen grid (§3 step 3) is empty — no multiple of step={} lies "
            "strictly inside the open interval (Lmin={:.4f}, L0={:.4f}); the grid "
            "constants cannot be resolved from the registration's stated order (§3) "
            "on this input".format(STEP, lmin, l0))
    print("this list is frozen here; nothing below recomputes or adjusts it (§3, §11)")

    # ---- §3 step 4: crossing times (only now) --------------------------------------
    section("§3 step 4 — crossing times (computed only now)")
    print("cross(r, L) := the FIRST checkpoint iteration whose curve value is <= L; "
          "no interpolation anywhere (§2, §11)")
    cross_idx = {}
    for L in grid:
        for rid in RUN_IDS:
            cross_idx[(rid, L)] = first_index_at_or_below(curves[rid], L)
    print("computed for {} runs x {} levels = {} crossing times; they enter the record "
          "only through the §10 quantities".format(len(RUN_IDS), len(grid),
                                                   len(RUN_IDS) * len(grid)))

    # ---- §3 step 5: the rules, in order ---------------------------------------------
    section("§3 step 5 — exclusion (§4), disqualification (§5), whole-test rule (§5), "
            "positive control (§6), criterion (§4)")

    def cross_iter(rid, L):
        return iterations[cross_idx[(rid, L)]]

    print("(5a) exclusion rule (§4): a level where any of the eight runs never crosses "
          "is excluded; the exclusion count is reported")
    level_records = []
    for L in grid:
        never = [rid for rid in RUN_IDS if cross_idx[(rid, L)] is None]
        rec = {"level": L, "status": None, "never_crossed": never, "twin_gap": None,
               "between_gap": None, "margin": None, "twin_diffs": None,
               "between_diffs": None, "disqualified_side": None,
               "rank_statistic": None, "loss_resolution": None}
        if never:
            rec["status"] = "excluded"
            print("  L={}: EXCLUDED — never crossed by {}".format(fmt(L), ", ".join(never)))
        else:
            rec["status"] = "candidate"
        level_records.append(rec)
    excluded_count = sum(1 for r in level_records if r["status"] == "excluded")
    print("  excluded levels: {} of {}".format(excluded_count, len(grid)))

    # (5b) disqualification rule — SYMMETRIC (registration §5, "Disqualification rule
    # — symmetric, fixed after review (CC's review, 2026-09-17, adopted)"): a level is
    # UNREADABLE if EITHER twin-gap(L) OR between-gap(L) is <= one checkpoint step.
    # The rule as first registered dropped a level only when twin-gap(L) sat at or
    # below one step, while a level whose between-gap(L) sat at or below one step was
    # left to fail the §4 criterion instead of being dropped — the same resolution
    # limit treated as "unreadable" on the twin side and as a substantive result on
    # the between side, which biased the whole test toward failing. This requires
    # computing between-gap(L) for every level surviving exclusion, not only for
    # levels that go on to be accepted (contrast the pre-merge scripts, which both
    # computed between-gap only after disqualification, because both were asymmetric).
    print("\n(5b) disqualification rule (§5, SYMMETRIC — CC's review, 2026-09-17, "
          "adopted; registration §5 'Disqualification rule — symmetric, fixed after "
          "review'): a level is UNREADABLE if EITHER twin-gap(L) OR between-gap(L) is "
          "<= one checkpoint step ({} iterations) — dropped, not scored as weak or as "
          "failing, and the drop is reported together with which side (twin, between, "
          "or both) triggered it".format(ONE_STEP))
    print("  twin-gap = mean |cross(a) - cross(b)| over the replicate pairs {}".format(
        ", ".join("({},{})".format(a, b) for a, b in TWIN_PAIRS)))
    print("  between-gap = mean |cross(i) - cross(j)| over the 15 unordered pairs of "
          "the canonical six {} (first runs of seeds 0-5; primes excluded)".format(
              ", ".join(CANONICAL_SIX)))
    for rec in level_records:
        if rec["status"] != "candidate":
            continue
        L = rec["level"]
        twin_diffs = [abs(cross_iter(a, L) - cross_iter(b, L)) for a, b in TWIN_PAIRS]
        between_diffs = [abs(cross_iter(a, L) - cross_iter(b, L)) for a, b in CANONICAL_PAIRS]
        tg = mean(twin_diffs)
        bg = mean(between_diffs)
        rec["twin_gap"] = tg
        rec["between_gap"] = bg
        rec["twin_diffs"] = twin_diffs
        rec["between_diffs"] = between_diffs
        twin_trig = tg <= ONE_STEP
        between_trig = bg <= ONE_STEP
        if twin_trig or between_trig:
            rec["status"] = "unreadable"
            side = "both" if (twin_trig and between_trig) else ("twin" if twin_trig else "between")
            rec["disqualified_side"] = side
            print("  L={}: UNREADABLE — twin-gap={}, between-gap={} (triggered by {}); "
                  "dropped".format(fmt(L), fmt(tg, 1), fmt(bg, 1), side))
        else:
            rec["status"] = "accepted"
            rec["margin"] = bg - tg
    unreadable_count = sum(1 for r in level_records if r["status"] == "unreadable")
    accepted_records = [r for r in level_records if r["status"] == "accepted"]
    print("  unreadable levels: {}; accepted levels remaining: {}".format(
        unreadable_count, len(accepted_records)))

    print("\n(5c) whole-test rule (§5): if more than half of the grid as constructed at "
          "step 3 leaves the test, the whole test is unreadable (not a fail, not a pass)")
    dropped = excluded_count + unreadable_count
    grid_size = len(grid)
    whole_test_triggered = dropped * 2 > grid_size
    print("  dropped = {} excluded + {} unreadable = {} of {} grid levels "
          "; the rule fires at {} of that many (the absolute threshold, not only the "
          "proportion: the same proportion on a smaller grid is a different number): {}".format(
              excluded_count, unreadable_count, dropped, grid_size,
              grid_size // 2 + 1,
              "MORE THAN HALF — whole test unreadable" if whole_test_triggered
              else "not more than half"))

    print("\n(5d) positive control (§6), applied before the criterion")
    prong1_failures = []
    bands_checked = 0
    for rid in RUN_IDS:
        for L in grid:
            if end_values[rid] < L < l0:
                bands_checked += 1
                if cross_idx[(rid, L)] is None:
                    prong1_failures.append({"run": rid, "level": L})
    prong1_outcome = "fail" if prong1_failures else "pass"
    print("  prong 1 (finiteness -- a completeness check, NOT a control: it cannot fail, "
          "since a run's own final checkpoint is at or below any level above its final "
          "value (§6 v2)): every grid level strictly between a run's "
          "iteration-{} value and L0 must be crossed finitely — {} (run, level) band(s) "
          "checked: {}".format(FINAL_ITERATION, bands_checked,
                               "PASS" if prong1_outcome == "pass" else "FAIL"))
    for f in prong1_failures:
        print("    FAIL: {} never crosses L={}".format(f["run"], fmt(f["level"])))

    untrained_side = {rid: {it: curves[rid][pos[it]] for it in CONTROL_ITERATIONS}
                      for rid in RUN_IDS}
    side_items = [(rid, it, v) for rid in RUN_IDS for it, v in untrained_side[rid].items()]
    min_side = min(v for _, _, v in side_items)
    min_binding = [(rid, it) for rid, it, v in side_items if v == min_side]
    prong2_failures = [rec for rec in accepted_records if not (rec["level"] < min_side)]
    prong2_outcome = "fail" if prong2_failures else "pass"
    if accepted_records:
        print("  prong 2 (untrained below every accepted level): every accepted level "
              "must be strictly below ALL iteration-{} values of all eight runs; the "
              "binding minimum = {:.4f} ({})".format(
                  "/".join(str(it) for it in CONTROL_ITERATIONS), min_side,
                  "; ".join("{} @ iteration {}".format(rid, it)
                            for rid, it in min_binding)))
        for rec in prong2_failures:
            print("    FAIL: accepted level L={} is not strictly below it".format(
                fmt(rec["level"])))
        print("  prong 2: {}".format("PASS" if prong2_outcome == "pass"
                                     else "FAIL — test void"))
    else:
        print("  prong 2: no accepted levels — vacuous pass")
    control_outcome = ("fail" if (prong1_outcome == "fail" or prong2_outcome == "fail")
                       else "pass")
    print("  positive control outcome: {}".format(
        "PASS" if control_outcome == "pass" else "FAIL"))

    verdict = None
    if control_outcome == "fail":
        detail = []
        if prong1_outcome == "fail":
            detail.append("prong 1 (layout completeness — not a control)")
        if prong2_outcome == "fail":
            detail.append("prong 2 (untrained below accepted levels)")
        verdict = ("CONTROL FAIL — TEST VOID (§6: {}). The §4 criterion is not "
                   "read.".format(" and ".join(detail)))
        print("\n(5e) criterion (§4): NOT READ — the control failure voids the test (§6)")
    else:
        print("\n(5e) criterion (§4): ACCEPT only if between-gap > twin-gap for EVERY "
              "accepted level; any other outcome is a fail")
        if accepted_records:
            print("\n  recorded §10 quantities for the accepted levels (twin-gap and "
                  "between-gap were computed once, in step 5b, under the symmetric "
                  "disqualification rule):")
            print("  {:<12} {:>14} {:>16} {:>14}".format(
                "level", "twin-gap(it)", "between-gap(it)", "margin(it)"))
            for rec in accepted_records:
                print("  {:<12} {:>14} {:>16} {:>14}".format(
                    fmt(rec["level"]), fmt(rec["twin_gap"], 1), fmt(rec["between_gap"], 1),
                    fmt(rec["margin"], 1)))

            # Exact rank statistic (§4, resolved by the 2026-09-17 review): a printed,
            # registered statistic reported beside twin-gap/between-gap; it never
            # feeds the criterion sentence above or the verdict below.
            print("\n  exact rank statistic (§4, printed only — never a criterion): "
                  "positions of the 2 twin differences among the 15 between-individual "
                  "differences (1 = smallest of the pooled 17), and the exact one-sided "
                  "p from the hypergeometric/rank enumeration (smallest attainable "
                  "one-sided p = 1/C(17,2) = 1/136 ~= 0.0074):")
            for rec in accepted_records:
                rank_stat = exact_rank_statistic(rec["twin_diffs"], rec["between_diffs"])
                rec["rank_statistic"] = rank_stat
                print("    L={}: twin ranks = {} of {}, rank-sum(twin) = {}, one-sided p "
                      "= {}/{} = {:.4f}".format(
                          fmt(rec["level"]), rank_stat["twin_ranks"], rank_stat["n_total"],
                          rank_stat["rank_sum_twin"], rank_stat["at_least_as_extreme"],
                          rank_stat["total_combinations"], rank_stat["one_sided_p"]))

            print("\n  loss-resolution near each accepted level (§10 recorded statistic, "
                  "not a criterion input): mean over the eight runs of the median "
                  "per-checkpoint-step |d val_loss| within ±2 checkpoints of the crossing")
            for rec in accepted_records:
                L = rec["level"]
                medians = []
                for rid in RUN_IDS:
                    i = cross_idx[(rid, L)]
                    lo = max(0, i - 2)
                    hi = min(len(curves[rid]) - 1, i + 2)
                    deltas = [abs(curves[rid][k + 1] - curves[rid][k])
                              for k in range(lo, hi)]
                    med = median(deltas)
                    if med is not None:
                        medians.append(med)
                rec["loss_resolution"] = mean(medians) if medians else None
                lr = rec["loss_resolution"]
                print("    L={}: {}".format(
                    fmt(L), "{:.6f} loss units per checkpoint step".format(lr)
                    if lr is not None else "n/a"))
        else:
            print("  (no accepted levels — nothing to record at this step)")

        if whole_test_triggered:
            verdict = ("TEST UNREADABLE (§5 whole-test rule: {} of {} grid levels left "
                       "the test — more than half). Not a fail, not a pass; the criterion "
                       "is not read as a verdict.".format(dropped, grid_size))
            print("\n  -> " + verdict)
        else:
            weak = [rec for rec in accepted_records
                    if not (rec["between_gap"] > rec["twin_gap"])]
            if not accepted_records:
                # Not reachable in practice when whole_test_triggered is False and
                # grid_size > 0 (an empty accepted set means dropped == grid_size,
                # which is always more than half of a non-empty grid) — kept as an
                # explicit branch because the registration itself calls it out (§4:
                # "If no accepted level remains ... the outcome is governed by §5's
                # whole-test rule, not by this sentence").
                verdict = ("TEST UNREADABLE (no accepted level remains; §4 hands the "
                           "outcome to §5's whole-test rule)")
            elif weak:
                verdict = ("FAIL (§4: between-gap <= twin-gap at {} of {} accepted "
                           "levels: {})".format(len(weak), len(accepted_records),
                                                ", ".join(fmt(r["level"]) for r in weak)))
            else:
                verdict = ("ACCEPT (§4: between-gap > twin-gap at every accepted level "
                           "— {} of {})".format(len(accepted_records),
                                                len(accepted_records)))
            print("\n  -> " + verdict)

    # ---- printed-only review statistics (Ark, 2026-09-17 21:47 UTC) ----------------
    # Recorded in the same single pass; never criteria; never gating the verdict.
    section("review statistics (Ark, 2026-09-17 21:47 UTC) — printed only; never "
            "criteria, never gating the verdict")

    def fmt_sci(x):
        return "{:.6e}".format(x) if x is not None else "n/a"

    def fmt_ratio(x):
        return "{:.3f}".format(x) if x is not None else "n/a"

    kink_per_run = {}
    for rid in RUN_IDS:
        pts = list(zip(iterations, curves[rid]))
        before_pts = [(x, y) for x, y in pts
                      if SLOPE_MIN_ITERATION <= x <= KINK_ITERATION]
        after_pts = [(x, y) for x, y in pts if x > KINK_ITERATION]
        s_before = lsq_slope(before_pts)
        s_after = lsq_slope(after_pts)
        if s_before is not None and s_before != 0 and s_after is not None:
            ratio = s_after / s_before
        else:
            ratio = None
        kink_per_run[rid] = {"slope_before": s_before, "slope_after": s_after,
                             "ratio_after_before": ratio,
                             "n_points_before": len(before_pts),
                             "n_points_after": len(after_pts)}
    kink_pooled = {
        "median_slope_before": median_of([v["slope_before"]
                                          for v in kink_per_run.values()]),
        "median_slope_after": median_of([v["slope_after"]
                                         for v in kink_per_run.values()]),
        "median_ratio_after_before": median_of([v["ratio_after_before"]
                                                for v in kink_per_run.values()]),
    }
    print("(1) kink at iteration {} — rationale: s/iter halves at iteration {} in 8/8 "
          "runs (schedule signature); whether the loss trajectory itself changes slope "
          "there decides whether grid levels on either side are the same task; this is "
          "printed, not judged".format(KINK_ITERATION, KINK_ITERATION))
    print("    least-squares slope of val_loss per iteration; 'before' over checkpoints "
          "with {} <= iteration <= {} (the (0,12) head excluded), 'after' over "
          "checkpoints with iteration > {}".format(SLOPE_MIN_ITERATION, KINK_ITERATION,
                                                    KINK_ITERATION))
    for rid in RUN_IDS:
        v = kink_per_run[rid]
        print("    {}: slope_before = {}, slope_after = {}, ratio after/before = {}".format(
            rid, fmt_sci(v["slope_before"]), fmt_sci(v["slope_after"]),
            fmt_ratio(v["ratio_after_before"])))
    print("    pooled medians: slope_before = {}, slope_after = {}, "
          "ratio after/before = {}".format(
              fmt_sci(kink_pooled["median_slope_before"]),
              fmt_sci(kink_pooled["median_slope_after"]),
              fmt_ratio(kink_pooled["median_ratio_after_before"])))

    kink_by_session = {}
    print("\n(2) slopes by session mode — the same two slopes pooled separately for the "
          "two OS boot sessions of §10 (printed only)")
    for label, members in (("session_A", SESSION_A), ("session_B", SESSION_B)):
        kink_by_session[label] = {
            "runs": list(members),
            "median_slope_before": median_of([kink_per_run[r]["slope_before"]
                                              for r in members]),
            "median_slope_after": median_of([kink_per_run[r]["slope_after"]
                                             for r in members]),
        }
        print("    {} ({}): median slope_before = {}, median slope_after = {}".format(
            label, ", ".join(members),
            fmt_sci(kink_by_session[label]["median_slope_before"]),
            fmt_sci(kink_by_session[label]["median_slope_after"])))

    # The v2 anchors moved the whole band (v1: 1146.0-1212.0; v2: 1162.0-1210.0, less the
    # two levels withdrawn by the §11 caveat), and a level higher in loss is crossed
    # earlier. So WHICH levels straddle the boundary is a property of the v2 grid and is
    # not comparable with any figure computed for v1 (Ark, 2026-09-17; §3 v2).
    straddle_per_level = []
    print("\n(3) straddle report — for every accepted level, min/max crossing iteration "
          "over the eight runs and whether the {} boundary lies strictly between them "
          "(some runs cross before the step, some after)".format(KINK_ITERATION))
    for rec in accepted_records:
        L = rec["level"]
        crossing_iterations = [cross_iter(rid, L) for rid in RUN_IDS]
        cmin = min(crossing_iterations)
        cmax = max(crossing_iterations)
        straddles = cmin < KINK_ITERATION < cmax
        straddle_per_level.append({"level": L, "cross_min": cmin, "cross_max": cmax,
                                   "straddles_150000": straddles})
        print("    L={}: cross min = {}, max = {}, {} strictly between: {}".format(
            fmt(L), cmin, cmax, KINK_ITERATION, "yes" if straddles else "no"))
    straddle_count = sum(1 for s in straddle_per_level if s["straddles_150000"])
    if accepted_records:
        print("    accepted levels straddling the {} boundary: {} of {}".format(
            KINK_ITERATION, straddle_count, len(accepted_records)))
    else:
        print("    (no accepted levels)")

    section("verdict")
    print(verdict)
    finished = utc_now()
    print("\nreading finished (UTC): " + finished)

    mapping_json = {
        "runs": [
            {"run_id": rid,
             "seed": RUN_BY_ID[rid][2],
             "role": RUN_BY_ID[rid][3],
             "registered_night": RUN_BY_ID[rid][4],
             "file": rel(assignment[rid]["candidate"]["file"]["path"], repo),
             "column": assignment[rid]["candidate"]["column"],
             "assigned_via": assignment[rid]["candidate"]["how"],
             "corroborated_by": [{"file": rel(c["file"]["path"], repo),
                                  "column": c["column"]}
                                 for c in corroboration[rid]]}
            for rid in RUN_IDS],
        "wave_jsons": {str(n): [rel(wp, repo) for wp in nights[n]["wave_paths"]]
                       for n in NIGHT_NUMBERS},
        "bound_jobs": {str(n): {rid: [{"id": j["id"], "seed": j["seed"],
                                       "tag": j["tag"], "wave": j["wave"]}
                                      for j in nights[n]["bound"][rid]]
                                for rid in RUN_IDS if rid in nights[n]["bound"]}
                       for n in NIGHT_NUMBERS},
        "unbound_jobs": [{"night": n, "id": j["id"], "seed": j["seed"], "tag": j["tag"]}
                         for n in NIGHT_NUMBERS for j in nights[n]["unbound"]],
        "unmapped_columns": unmapped_columns,
        "unused_pairwise_files": pairwise_notes,
        "unrecognized_files": unrecognized,
    }
    return {
        "registration": REGISTRATION_DOC,
        "script": SCRIPT_REL_PATH,
        "script_sha256": script_sha256,
        "input_files_sha256": {rel(fi["path"], repo): fi["sha256"]
                               for fi in validated_files},
        "utc_started": started,
        "utc_finished": finished,
        "repo_root": str(repo),
        "constants": {"L0_computed": l0, "Lmin_computed": lmin,
                      "L0_v1_published_not_used": L0_V1_PUBLISHED,
                      "withdrawn_levels": list(WITHDRAWN_LEVELS),
                      "withdrawn_reason": ("reviewer exposure before the reading "
                                           "(§11 disclosure, Ark 2026-09-17): a "
                                           "provenance exclusion, NOT a data outcome; "
                                           "never to be recorded as a level that failed"),
                      "step": STEP, "one_step_iterations": ONE_STEP,
                      "final_iteration": FINAL_ITERATION,
                      "control_iterations": list(CONTROL_ITERATIONS),
                      "expected_checkpoint_rows": EXPECTED_ROWS},
        "mapping": mapping_json,
        "iteration_grid": iterations,
        "end_values": end_values,
        "Lmin": lmin,
        "Lmin_attained_by": lmin_runs,
        "grid_levels": grid,
        "untrained_side_values": {rid: {str(it): untrained_side[rid][it]
                                        for it in CONTROL_ITERATIONS}
                                  for rid in RUN_IDS},
        "levels": [{"level": r["level"],
                    "status": r["status"],
                    "never_crossed": (r["never_crossed"] if r["status"] == "excluded"
                                      else []),
                    "twin_gap": r["twin_gap"],
                    "between_gap": r["between_gap"],
                    "margin": r["margin"],
                    "disqualified_side": r["disqualified_side"],
                    "rank_statistic": r["rank_statistic"],
                    "loss_resolution": r["loss_resolution"]}
                   for r in level_records],
        "counts": {"grid_size": grid_size,
                   "excluded": excluded_count,
                   "unreadable": unreadable_count,
                   "accepted": len(accepted_records),
                   "dropped": dropped},
        "whole_test_rule": {"dropped": dropped, "grid_size": grid_size,
                            "more_than_half": whole_test_triggered},
        "control": {"prong1_finiteness": {"outcome": prong1_outcome,
                                          "bands_checked": bands_checked,
                                          "failures": prong1_failures},
                    "prong2_untrained_below_accepted": {
                        "outcome": prong2_outcome,
                        "min_untrained_side_value": min_side,
                        "binding": ["{} @ iteration {}".format(rid, it)
                                    for rid, it in min_binding],
                        "failures": [rec["level"] for rec in prong2_failures]},
                    "outcome": control_outcome},
        "review_statistics": {
            "declared_by": "Ark, external review, 2026-09-17 21:47 UTC",
            "printed_only": True,
            "kink_per_run": kink_per_run,
            "kink_pooled": kink_pooled,
            "kink_by_session": kink_by_session,
            "straddle": {
                "boundary_iteration": KINK_ITERATION,
                "straddling_accepted_levels": straddle_count,
                "accepted_levels": len(accepted_records),
                "per_accepted_level": straddle_per_level,
            },
        },
        "verdict": verdict,
    }


# ------------------------------------------------------------------------- CLI

def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="read_reachability_endpoint.py",
        description="One-pass reading of the pre-registered reachability endpoint test "
                    "(" + REGISTRATION_DOC + "). Run once; record the output verbatim.")
    parser.add_argument("--repo", metavar="ROOT", default=None,
                        help="repository root (default: the root of the repository "
                             "this script lives in)")
    parser.add_argument("--out", metavar="DIR", default="results/diagnostics/reachability",
                        help="output directory for " + JSON_NAME + " (default: "
                             "%(default)s; relative paths resolve against the repo root)")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    repo = Path(args.repo).resolve() if args.repo else Path(__file__).resolve().parents[2]
    out_dir = Path(args.out)
    if not out_dir.is_absolute():
        out_dir = repo / out_dir
    started = utc_now()
    try:
        report = run_reading(repo, started)
    except MappingRefusal as exc:
        print("\nMAPPING REFUSAL (exit 2) — the reading did not happen:\n{}".format(exc),
              file=sys.stderr)
        return 2
    except LayoutMismatch as exc:
        print("\nLAYOUT MISMATCH (exit 3) — the reading did not happen:\n{}".format(exc),
              file=sys.stderr)
        return 3
    except ConstantsUnresolved as exc:
        print("\nCONSTANTS UNRESOLVED (exit 5) — the reading did not happen:\n{}".format(exc),
              file=sys.stderr)
        return 5
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / JSON_NAME
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
        fh.write("\n")
    print("\nJSON report written to: {}".format(json_path))
    if report["control"]["outcome"] == "fail":
        print("Exit code 4: §6 positive-control failure — the test is void "
              "(report written).")
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(main())
