"""Generate the C6 fold file: which of 10 folds each cell of the 65 x 65 ordered-pair grid is in.

Specification: docs/plans/2026-09-23-c6-control-specification.md, section 4.1 "Folds" as
clarified by Amendment A2 (2026-09-23).

    strata  non-empty = the 604 ordered type pairs present in the compiled bank
            empty     = the other 3,621 cells (Lawf1->Lawf1, in the json but never compiled,
                        is an empty cell and is flagged)
    key     sha256("C6-v1:" + pair_birth_id), hex; pair_birth_id is the content-derived id of
            results/genome/bank/REGISTRY.md (Revision v1), defined for every cell of the grid
    fold    within each stratum, cells sorted by key ascending; fold = rank mod 10 (rank from 0)

Reads only results/genome/bank/types.csv, offsets.csv and birth_ids.csv. No randomness, no
rule, no score. Writes folds.csv and folds.meta.json next to this file, UTF-8 with "\n" line
ends. Refuses to overwrite an existing folds.csv whose content would change: the fold file is
generated once and never regenerated for a rule.

Usage (from the repository root):
    tools/.venv/Scripts/python.exe results/genome/c6/make_folds.py
"""

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BANK = ROOT / "results" / "genome" / "bank"
SPEC = ROOT / "docs" / "plans" / "2026-09-23-c6-control-specification.md"
N_FOLDS = 10
FOLD_KEY_PREFIX = "C6-v1:"
BIRTH_ID_VERSION = "cs-birth-v1"
BIRTH_ID_HEX = 12


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_lf(path):
    """sha256 of a text file with CRLF normalised to LF: the content git stores
    (core.autocrlf may give a checkout CRLF line ends; the hash must not depend on that)."""
    return sha256_bytes(Path(path).read_bytes().replace(b"\r\n", b"\n"))


def pair_birth_id(src, tar):
    return sha256_bytes(f"{BIRTH_ID_VERSION}|pair|{src}->{tar}".encode("utf-8"))[:BIRTH_ID_HEX]


def type_birth_id(name):
    return sha256_bytes(f"{BIRTH_ID_VERSION}|type|{name}".encode("utf-8"))[:BIRTH_ID_HEX]


def read_csv(path):
    return pd.read_csv(path, skiprows=1, dtype=str, keep_default_na=False, encoding="utf-8")


T = read_csv(BANK / "types.csv")
O = read_csv(BANK / "offsets.csv")
B = read_csv(BANK / "birth_ids.csv")
assert len(T) == 65

# The type ids and the registered pair ids must agree with the rule re-derived here.
for r in T.itertuples(index=False):
    assert r.birth_id == type_birth_id(r.type_name), r.type_name
reg_pair = {r.birth_key[5:]: r.birth_id for r in B.itertuples(index=False) if r.kind == "pair"}
for key, bid in reg_pair.items():
    s, t = key.split(">")
    assert bid == pair_birth_id(s, t), key

types = sorted(T.type_name)  # Unicode code point order: the row order of folds.csv only
tid = {t: type_birth_id(t) for t in types}
compiled = O[O.provenance.isin(["in_json", "hull_filled"])]
nonempty = set(zip(compiled.src, compiled.tar))
assert len(nonempty) == 604
json_only = {(s, t) for s, t in (k.split(">") for k in reg_pair)} - nonempty
assert json_only == {("Lawf1", "Lawf1")}, json_only

cells = []
for s in types:
    for t in types:
        pid = pair_birth_id(s, t)
        cells.append(dict(
            src=s, tar=t, src_birth_id=tid[s], tar_birth_id=tid[t], pair_birth_id=pid,
            stratum="nonempty" if (s, t) in nonempty else "empty",
            flag="json_pair_never_compiled" if (s, t) in json_only else "",
            fold_key_sha256=sha256_bytes((FOLD_KEY_PREFIX + pid).encode("utf-8")),
        ))
assert len(cells) == 65 * 65
assert len({c["pair_birth_id"] for c in cells}) == len(cells)
assert len({c["fold_key_sha256"] for c in cells}) == len(cells)  # no ties in the sort

for stratum in ("nonempty", "empty"):
    members = sorted((c for c in cells if c["stratum"] == stratum),
                     key=lambda c: c["fold_key_sha256"])
    for rank, c in enumerate(members):
        c["fold"] = rank % N_FOLDS
        c["rank_in_stratum"] = rank

cols = ["src", "tar", "src_birth_id", "tar_birth_id", "pair_birth_id", "stratum", "flag",
        "fold_key_sha256", "rank_in_stratum", "fold"]
SCRIPT_SHA = sha256_lf(__file__)
SPEC_SHA = sha256_lf(SPEC)
header = (f"# C6 folds; spec=docs/plans/2026-09-23-c6-control-specification.md "
          f"sha256={SPEC_SHA} (LF-normalised); generator=results/genome/c6/make_folds.py "
          f"sha256={SCRIPT_SHA} (LF-normalised); key=sha256('{FOLD_KEY_PREFIX}'+pair_birth_id); "
          f"fold=rank mod {N_FOLDS} within stratum; see folds.meta.json")
lines = [header, ",".join(cols)] + [",".join(str(c[k]) for k in cols) for c in cells]
text = "\n".join(lines) + "\n"
body = "\n".join(lines[1:]) + "\n"  # everything but the provenance comment line

out = HERE / "folds.csv"
if out.exists():
    old = out.read_bytes().replace(b"\r\n", b"\n").decode("utf-8")
    if old.split("\n", 1)[1] != body:
        sys.exit("REFUSED: folds.csv exists and the fold assignment would change. The fold file "
                 "is generated once (spec §4.1, Amendment A2). Nothing was overwritten.")
out.write_text(text, encoding="utf-8", newline="\n")

# Balance check
per = Counter((c["stratum"], c["fold"]) for c in cells)
by_fold = {f: dict(nonempty=per[("nonempty", f)], empty=per[("empty", f)],
                   total=per[("nonempty", f)] + per[("empty", f)]) for f in range(N_FOLDS)}
ne = [by_fold[f]["nonempty"] for f in range(N_FOLDS)]
em = [by_fold[f]["empty"] for f in range(N_FOLDS)]
balance_ok = (max(ne) - min(ne) <= 1 and max(em) - min(em) <= 1
              and sum(ne) == 604 and sum(em) == 3621)
assert balance_ok
flag_fold = [c["fold"] for c in cells if c["flag"]]

meta = dict(
    what="C6 fold assignment over the full 65 x 65 ordered type-pair grid, empty cells included. "
         "No rule, no score.",
    spec=dict(path="docs/plans/2026-09-23-c6-control-specification.md",
              sha256_lf_normalised=SPEC_SHA, sections="4.1 Folds; Amendment A1, A2"),
    generator=dict(path="results/genome/c6/make_folds.py", sha256_lf_normalised=SCRIPT_SHA,
                   python=sys.version.split()[0], pandas=pd.__version__),
    inputs={n: sha256_lf(BANK / n) for n in ("types.csv", "offsets.csv", "birth_ids.csv")},
    output=dict(path="results/genome/c6/folds.csv", sha256_lf_normalised=sha256_lf(out),
                n_rows=len(cells), row_order="(src, tar) by Unicode code point of the names"),
    rule=dict(
        pair_birth_id=f"first {BIRTH_ID_HEX} hex of sha256('{BIRTH_ID_VERSION}|pair|<src>-><tar>')",
        fold_key=f"sha256('{FOLD_KEY_PREFIX}' + pair_birth_id), hex",
        strata="nonempty = the 604 pairs of the compiled bank; empty = the other 3,621 cells",
        fold=f"within each stratum, sort by fold_key ascending; fold = rank mod {N_FOLDS}"),
    n_folds=N_FOLDS,
    counts_per_fold=by_fold,
    balance=dict(nonempty_min=min(ne), nonempty_max=max(ne), empty_min=min(em),
                 empty_max=max(em), ok=balance_ok,
                 rule="each stratum's per-fold counts differ by at most 1"),
    flagged=dict(cell="Lawf1->Lawf1", reason="json pair that never compiles; an empty cell",
                 fold=flag_fold[0]),
    checks=dict(type_ids_rederived=True, registered_pair_ids_rederived=True,
                pair_ids_distinct_over_grid=True, fold_keys_distinct=True),
)
(HERE / "folds.meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8",
                                      newline="\n")
print(json.dumps(dict(balance=meta["balance"], folds_sha256=meta["output"]["sha256_lf_normalised"],
                      spec_sha256=SPEC_SHA), indent=1))
