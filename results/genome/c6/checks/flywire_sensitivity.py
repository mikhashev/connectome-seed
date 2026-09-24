#!/usr/bin/env python3
"""Registration section 3b: compare the FlyWire bank variants with flyvis-30, before any BF value.

Reads the primary bank and the two diagnostic variants from connectome-seed-data/FlyWire/derived/
and the flyvis bank from results/genome/bank/offsets.csv (json rows only, no hull rows), restricted
to the 30 types. Writes results/genome/c6/checks/flywire_sensitivity/summary.json and RESULT.md.
Usage: tools/.venv/Scripts/python.exe results/genome/c6/checks/flywire_sensitivity.py
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C6 = HERE.parent
ROOT = C6.parents[2]                                   # the repository root
DERIVED = ROOT.parent / "connectome-seed-data" / "FlyWire" / "derived"
OUT = HERE / "flywire_sensitivity"
REGISTRATION = "docs/plans/2026-09-24-flywire-bf-p3-registration.md"
sys.path.insert(0, str(HERE))
from flywire_bank_builder import FLYWIRE_NAME_OF  # noqa: E402

TYPES = set(FLYWIRE_NAME_OF)
VARIANTS = {"primary": DERIVED, "geo": DERIVED / "sensitivity_geo",
            "geo_interior": DERIVED / "sensitivity_geo_interior"}
RECOVERY_CUT = 50        # registration section 3b, Johnny's reading rule
FAR = 3                  # an offset row with max(|du|, |dv|) >= 3


def far(du, dv):
    return max(abs(du), abs(dv))


def describe(rows):
    pairs = {(s, t) for s, t, _, _ in rows}
    spectrum = {}
    for _, _, du, dv in rows:
        k = min(far(du, dv), FAR)
        spectrum[k] = spectrum.get(k, 0) + 1
    return {"offset_rows": len(rows), "nonempty_pairs": len(pairs),
            "rows_by_max_abs_offset": {("%d+" % FAR if k == FAR else str(k)): v
                                       for k, v in sorted(spectrum.items())},
            "rows_at_or_beyond_far": sum(1 for _, _, du, dv in rows if far(du, dv) >= FAR),
            "max_abs_offset": max((far(du, dv) for _, _, du, dv in rows), default=0)}, pairs


def read_flywire(d):
    meta = json.loads((d / "bank.meta.json").read_text(encoding="utf-8"))
    with open(d / meta["offsets_file"], newline="", encoding="utf-8") as fh:
        rows = [(r["src"], r["tar"], int(r["du"]), int(r["dv"])) for r in csv.DictReader(fh)]
    return rows, meta


def read_flyvis30():
    with open(ROOT / "results" / "genome" / "bank" / "offsets.csv", newline="",
              encoding="utf-8") as fh:
        lines = [ln for ln in fh if not ln.startswith("#")]
    rows = [(r["src"], r["tar"], int(r["du"]), int(r["dv"])) for r in csv.DictReader(lines)
            if r["provenance"] == "in_json" and r["src"] in TYPES and r["tar"] in TYPES]
    return rows


def main():
    fv_desc, fv_pairs = describe(read_flyvis30())
    out = {"registration": REGISTRATION, "flyvis30_json_rows_only": fv_desc, "variants": {}}
    primary_pairs = None
    for name, d in VARIANTS.items():
        rows, meta = read_flywire(d)
        desc, pairs = describe(rows)
        if name == "primary":
            primary_pairs = pairs
            missing = sorted(fv_pairs - pairs)
            out["missing_in_primary"] = len(missing)
            out["only_in_primary"] = len(pairs - fv_pairs)
        desc["variant_in_manifest"] = meta.get("variant")
        desc["recovered_of_missing"] = len(set(missing) & pairs) if name != "primary" else 0
        desc["flyvis30_pairs_present"] = len(fv_pairs & pairs)
        out["variants"][name] = desc
    diag = [out["variants"][v] for v in ("geo", "geo_interior")]
    contaminated = any(v["recovered_of_missing"] >= RECOVERY_CUT and v["rows_at_or_beyond_far"] > 0
                       for v in diag)
    out["reading_rule"] = (f"primary verdict labelled pipeline-contaminated iff a diagnostic "
                           f"variant recovers >= {RECOVERY_CUT} of the pairs missing from the "
                           f"primary bank AND has an offset row with max(|du|,|dv|) >= {FAR}")
    out["primary_verdict_label"] = ("pipeline-contaminated, reading not final" if contaminated
                                    else "support difference real, reading stands")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    md = ["# FlyWire bank variants against flyvis-30 (registration section 3b)", "",
          f"Pairs of flyvis-30 missing from the primary FlyWire bank: {out['missing_in_primary']}; "
          f"pairs only in the primary FlyWire bank: {out['only_in_primary']}.", "",
          "| bank | offset rows | nonempty pairs | rows by max(abs du, abs dv) | rows at >= 3 | "
          "max | flyvis-30 pairs present | recovered of the missing |",
          "|---|---|---|---|---|---|---|---|",
          f"| flyvis-30 (json rows) | {fv_desc['offset_rows']} | {fv_desc['nonempty_pairs']} | "
          f"{fv_desc['rows_by_max_abs_offset']} | {fv_desc['rows_at_or_beyond_far']} | "
          f"{fv_desc['max_abs_offset']} | - | - |"]
    for name, v in out["variants"].items():
        md.append(f"| FlyWire {name} | {v['offset_rows']} | {v['nonempty_pairs']} | "
                  f"{v['rows_by_max_abs_offset']} | {v['rows_at_or_beyond_far']} | "
                  f"{v['max_abs_offset']} | {v['flyvis30_pairs_present']} | "
                  f"{v['recovered_of_missing']} |")
    md += ["", f"Reading rule: {out['reading_rule']}.", "",
           f"**Label for the primary verdict: {out['primary_verdict_label']}.**", ""]
    (OUT / "RESULT.md").write_text("\n".join(md), encoding="utf-8", newline="\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
