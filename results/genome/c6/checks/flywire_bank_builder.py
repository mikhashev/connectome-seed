#!/usr/bin/env python3
"""Build the FlyWire right-optic-lobe, 30-type bank.

Type set decided by Mike, chat 2026-09-24 07:28 UTC: the 30 column-assigned, name-matched types
only ("no imputation"). The 18 name-matched types without a column assignment and the 17
unmatched types are both dropped -- for different reasons, both recorded below.

Registered in docs/plans/2026-09-24-flywire-bf-p3-registration.md section 3. NOT RUN beyond
--inspect-only during drafting. Output belongs under connectome-seed-data/FlyWire/derived/
(outside the repo; never committed -- registration section 1). Only this script and a manifest of
hashes/thresholds/diagnostic counts belong in the repository.

Environment: this script needs pyarrow (to read proofread_connections_783.feather), which must
NOT be installed into tools/.venv -- that environment's digest is pinned by night 6 gate 8
(docs/briefs/2026-09-20-night6-deterministic-pairs.md) and a change would void the nights 1-5
comparison. Run this script in a separate, throwaway environment instead, e.g.:

    uv run --no-project --with pyarrow --with numpy --with pandas python \
        results/genome/c6/checks/flywire_bank_builder.py [--out DIR] [--inspect-only]

The run script (flywire_bf_p3.py) stays on tools/.venv/Scripts/python.exe: it only reads the
built bank's CSV output, never the feather file, so it needs no pyarrow.
"""
import argparse
import csv
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C6 = HERE.parent
ROOT = C6.parents[2]                                   # the repository root
REGISTRATION = "docs/plans/2026-09-24-flywire-bf-p3-registration.md"
DATA_ROOT = ROOT.parent / "connectome-seed-data" / "FlyWire"
DEFAULT_OUT = DATA_ROOT / "derived"

# All four decided by Mike, chat 2026-09-24 07:28 UTC ("we have to start somewhere"): starting
# choices, recorded as such, not derived from anything in this repo.
SYNAPSE_THRESHOLD = 2      # registration section 3.2
MEAN_PRUNE_BELOW = 1.0     # registration section 3.5 (flyvis's own equation 8, re-applied)
APPLY_HULL_FILL = False    # registration section 3.5
PLACEHOLDER_SIGN = 1       # registration section 3.7 (unread by the existence-only P3 test)

FLYVIS_NAMES = [
    "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "L1", "L2", "L3", "L4", "L5",
    "Lawf1", "Lawf2", "Am", "C2", "C3", "CT1(Lo1)", "CT1(M10)",
    "Mi1", "Mi2", "Mi3", "Mi4", "Mi9", "Mi10", "Mi11", "Mi12", "Mi13", "Mi14", "Mi15",
    "T1", "T2", "T2a", "T3", "T4a", "T4b", "T4c", "T4d", "T5a", "T5b", "T5c", "T5d",
    "Tm1", "Tm2", "Tm3", "Tm4", "Tm5Y", "Tm5a", "Tm5b", "Tm5c", "Tm9", "Tm16", "Tm20",
    "Tm28", "Tm30", "TmY3", "TmY4", "TmY5a", "TmY9", "TmY10", "TmY13", "TmY14", "TmY15", "TmY18",
]
assert len(FLYVIS_NAMES) == 65

# 17 names not found under any spelling checked in any FlyWire type-name vocabulary (registration
# section 2).
UNMATCHED_NO_NAME = {"R1", "R2", "R3", "R4", "R5", "R6", "CT1(Lo1)", "CT1(M10)", "Mi3", "Mi11",
                      "Mi12", "Tm28", "Tm30", "Tm5Y", "TmY9", "TmY13", "TmY18"}
# 18 names matched (registration section 2's 48), but column_assignment.csv.gz has no column
# position for them (only 31 FlyWire types are column-assigned at all) -- dropped by Mike's
# decision rather than imputed (registration section 3.1, open decision #1, resolved: option (a)).
UNMATCHED_NO_COLUMN = {"Lawf1", "Lawf2", "Mi2", "Mi10", "Mi13", "Mi14", "Mi15", "Tm16", "Tm5a",
                        "Tm5b", "Tm5c", "TmY3", "TmY4", "TmY5a", "TmY10", "TmY14", "TmY15", "Am"}
UNMATCHED = UNMATCHED_NO_NAME | UNMATCHED_NO_COLUMN
assert len(UNMATCHED_NO_NAME) == 17 and len(UNMATCHED_NO_COLUMN) == 18 and len(UNMATCHED) == 35

FLYWIRE_NAME_OF = {n: n for n in FLYVIS_NAMES if n not in UNMATCHED}
assert len(FLYWIRE_NAME_OF) == 30


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dirty_tree():
    return subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True,
                           text=True, check=True).stdout.strip()


def refuse_if_unsafe(allow_dirty):
    if not allow_dirty:
        d = dirty_tree()
        if d:
            sys.exit(f"REFUSED: uncommitted changes; commit {REGISTRATION} first.\n" + d)
    if not DATA_ROOT.exists():
        sys.exit(f"REFUSED: data root not found: {DATA_ROOT}")


def read_neuron_table(log):
    p = DATA_ROOT / "murthylab-visual-system-parts-list@0d8574d" / "neuron_table.csv"
    with open(p, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    log(f"neuron_table.csv: {len(rows)} rows, sha256={sha256_file(p)}")
    return rows, p


COLUMN_ASSIGNMENT_DOWNLOAD_DATE = "2026-09-23 UTC"  # per connectome-seed-data/FlyWire/SOURCE.md


def column_assignment_manifest_entry(p):
    """Section 3, item 4 of the review (2026-09-24): the column file is a load-bearing input
    that cannot be rebuilt from the repo, so its identity must be recorded in full, not just its
    row count."""
    return {"file": p.name, "size_bytes": p.stat().st_size, "sha256": sha256_file(p),
            "downloaded": COLUMN_ASSIGNMENT_DOWNLOAD_DATE, "source": "SOURCE.md"}


def read_column_assignment(log):
    p = DATA_ROOT / "column_assignment.csv.gz"
    with gzip.open(p, "rt", encoding="utf-8") as fh:
        r = csv.DictReader(fh)
        expected = {"root_id", "hemisphere", "type", "column_id", "x", "y", "p", "q"}
        if not expected.issubset(set(r.fieldnames)):
            sys.exit(f"REFUSED: column_assignment.csv.gz columns are {r.fieldnames}, "
                     f"expected at least {sorted(expected)}")
        rows = list(r)
    entry = column_assignment_manifest_entry(p)
    log(f"column_assignment.csv.gz: {len(rows)} rows, manifest_entry={entry}")
    return rows, p, entry


def inspect_connections_schema(log):
    p = DATA_ROOT / "proofread_connections_783.feather"
    try:
        import pandas as pd
    except ImportError:
        sys.exit("REFUSED: pandas not available")
    try:
        df = pd.read_feather(p)
    except ImportError as e:
        sys.exit(f"REFUSED: cannot read {p.name} ({e}); install pyarrow first "
                 "(registration section 8).")
    cols = list(df.columns)
    log(f"proofread_connections_783.feather: {len(df)} rows, columns={cols}, "
        f"sha256={sha256_file(p)}")
    pre = [c for c in cols if "pre" in c.lower() and "root" in c.lower()]
    post = [c for c in cols if "post" in c.lower() and "root" in c.lower()]
    syn = [c for c in cols if "syn" in c.lower()]
    if not pre or not post or not syn:
        sys.exit(f"REFUSED: could not identify pre/post/synapse columns in {cols}")
    log(f"  candidates: pre={pre}, post={post}, syn={syn}")
    return df, {"pre": pre[0], "post": post[0], "syn": syn[0]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    ap.add_argument("--allow-dirty", action="store_true")
    ap.add_argument("--inspect-only", action="store_true")
    a = ap.parse_args()

    refuse_if_unsafe(a.allow_dirty)
    out = Path(a.out) if a.out else DEFAULT_OUT

    log = lambda m: print(m, flush=True)
    log(f"registration: {REGISTRATION}")
    log(f"30 types (decided by Mike, chat 2026-09-24 07:28 UTC): {sorted(FLYWIRE_NAME_OF)}")
    log(f"17 unmatched, no name found (dropped): {sorted(UNMATCHED_NO_NAME)}")
    log(f"18 name-matched but no column assignment (dropped, no imputation): "
        f"{sorted(UNMATCHED_NO_COLUMN)}")
    log(f"synapse threshold: >= {SYNAPSE_THRESHOLD}, mean_prune_below={MEAN_PRUNE_BELOW}, "
        f"hull_fill={APPLY_HULL_FILL}, placeholder_sign={PLACEHOLDER_SIGN}")

    read_neuron_table(log)
    read_column_assignment(log)  # logs its own manifest entry (name/size/sha256/download date)
    inspect_connections_schema(log)

    if a.inspect_only:
        log("--inspect-only: stopping before any offset table is built.")
        return

    build(out, log)


def git_head():
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                           text=True, check=True).stdout.strip()


def build(out, log):
    """Registration section 3, as amended before the build (section 3a). Every step is named
    there; nothing here is chosen after seeing a number."""
    import pandas as pd

    # 3.1 Neurons: right hemisphere of column_assignment.csv.gz, type among the 30. The type is
    # taken from that file; a neuron without a column row takes no part.
    col_rows, col_path, col_entry = read_column_assignment(lambda m: None)
    pos, type_of = {}, {}
    for r in col_rows:
        if r["hemisphere"] != "right" or r["type"] not in FLYWIRE_NAME_OF:
            continue
        rid = int(r["root_id"])
        if rid in pos:
            sys.exit(f"REFUSED: root_id {rid} has two right-hemisphere column rows")
        pos[rid] = (int(r["p"]), int(r["q"]))
        type_of[rid] = r["type"]
    n_of_type = {t: 0 for t in FLYWIRE_NAME_OF}
    for t in type_of.values():
        n_of_type[t] += 1
    missing = sorted(t for t, n in n_of_type.items() if n == 0)
    if missing:
        sys.exit(f"REFUSED: types with no right-hemisphere column rows: {missing}")
    log(f"neurons: {len(pos)} right-hemisphere, column-assigned, in the 30 types")

    # 3.2 Connections: synapses summed over neuropil rows for each (pre, post) root pair, both
    # ends among the neurons above; a pair is kept at >= SYNAPSE_THRESHOLD synapses.
    feather = DATA_ROOT / "proofread_connections_783.feather"
    df = pd.read_feather(feather, columns=["pre_pt_root_id", "post_pt_root_id", "syn_count"])
    ids = pd.Index(list(pos))
    df = df[df.pre_pt_root_id.isin(ids) & df.post_pt_root_id.isin(ids)]
    df = df.groupby(["pre_pt_root_id", "post_pt_root_id"], as_index=False)["syn_count"].sum()
    n_pairs_all = len(df)
    df = df[df.syn_count >= SYNAPSE_THRESHOLD]
    log(f"neuron pairs among them: {n_pairs_all}; at >= {SYNAPSE_THRESHOLD} synapses: {len(df)}")

    # 3.3 Offsets, post minus pre, in the file's own (p, q). 3.4 Column averaging: summed
    # synapses per (s, t, du, dv), divided by the number of column-assigned neurons of type t.
    sums = {}
    for pre, post, n in df.itertuples(index=False):
        s, t = type_of[pre], type_of[post]
        du, dv = pos[post][0] - pos[pre][0], pos[post][1] - pos[pre][1]
        k = (s, t, du, dv)
        sums[k] = sums.get(k, 0) + int(n)
    rows, n_pruned, n_autapse = [], 0, 0
    for (s, t, du, dv), total in sorted(sums.items()):
        mean = total / n_of_type[t]
        # 3.5 Pruning: the self offset of a type onto itself is dropped; a mean below 1 is dropped.
        if s == t and (du, dv) == (0, 0):
            n_autapse += 1
            continue
        if mean < MEAN_PRUNE_BELOW:
            n_pruned += 1
            continue
        rows.append({"src": s, "tar": t, "du": du, "dv": dv, "n_syn": repr(mean),
                     "sign": PLACEHOLDER_SIGN})

    # 3.6 Existence: a type pair exists iff at least one offset row survives.
    pairs = sorted({(r["src"], r["tar"]) for r in rows})
    out.mkdir(parents=True, exist_ok=True)
    offsets_file = "flywire_ol_right_30_offsets.csv"
    with open(out / offsets_file, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["src", "tar", "du", "dv", "n_syn", "sign"])
        w.writeheader()
        w.writerows(rows)
    out_deg = {t: sum(1 for s, _ in pairs if s == t) for t in FLYWIRE_NAME_OF}
    in_deg = {t: sum(1 for _, u in pairs if u == t) for t in FLYWIRE_NAME_OF}
    manifest = {
        "registration": REGISTRATION, "git_head": git_head(),
        "builder_sha256": sha256_file(Path(__file__)),
        "inputs": {"column_assignment": col_entry,
                   "proofread_connections_783.feather": {"sha256": sha256_file(feather),
                                                          "size_bytes": feather.stat().st_size}},
        "thresholds": {"synapses_per_neuron_pair_min": SYNAPSE_THRESHOLD,
                       "mean_prune_below": MEAN_PRUNE_BELOW, "hull_fill": APPLY_HULL_FILL,
                       "placeholder_sign": PLACEHOLDER_SIGN},
        "types": sorted(FLYWIRE_NAME_OF), "neurons_per_type": n_of_type,
        "columns_right_hemisphere": len({(p, q) for p, q in pos.values()}),
        "neuron_pairs_among_types": n_pairs_all, "neuron_pairs_kept": int(len(df)),
        "offset_rows_before_pruning": len(sums), "offset_rows_autapse_dropped": n_autapse,
        "offset_rows_pruned_mean_below_1": n_pruned, "offset_rows_kept": len(rows),
        "nonempty_type_pairs": len(pairs), "out_degree": out_deg, "in_degree": in_deg,
        "offsets_file": offsets_file, "offsets_sha256": sha256_file(out / offsets_file),
    }
    (out / "bank.meta.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    log(f"bank written to {out}: {len(rows)} offset rows, {len(pairs)} nonempty type pairs")


if __name__ == "__main__":
    main()
