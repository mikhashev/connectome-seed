"""Export the data drawn in scene 5 of the project video (two 30-type banks and their ranks).

Explanatory figure only: it reads, it registers nothing, and it writes nothing inside the
repository. Scenes 1, 2 and 4 read the 65-type bank from scene_data.json, written by
tools/viz/export_bank_scene_data.py; this script adds what scene 5 needs.

What it reads
  * The two 30-type banks exactly as results/genome/c6/checks/flywire_bf_p3.py builds them,
    through that module's own functions (imported, not re-implemented):
      - "flyvis30"  = build_flyvis30_bank(): the harness's REAL restricted to the 30 types;
      - "flywire30" = load_flywire_bank(): connectome-seed-data/FlyWire/derived (outside the repo).
    For each: one (source, target) cell per connection with its offsets. FlyWire signs are a
    placeholder (+1 for every cell, flywire_bank_builder.py PLACEHOLDER_SIGN), so the video
    draws no sign on either 30-type stack.
  * One degree-preserving shuffle of each, from the harness's own shuffled_bank(bank, seed=0),
    to show what a shuffle does (the run used seeds 0..98).
  * The per-rank values actually tested: results/genome/c6/checks/flywire_bf_p3/{arm}/
    per_shuffle_rank{1..4}.csv, column `existence` (the P3 margin on the existence field): the
    row kind=real and the 99 rows kind=shuffle. The video shows these as heights only; no value
    is printed.

Importing the harness runs its own integrity checks; nothing is modified.

Run from the repository root:
    tools/.venv/Scripts/python.exe tools/viz/project_video/export_project_video_data.py [out.json]
"""

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CHECKS = ROOT / "results" / "genome" / "c6" / "checks"
P3_DIR = CHECKS / "flywire_bf_p3"
DEFAULT_OUT = (ROOT.parent / "connectome-seed-data" / "renderings" / "project_video"
               / "project_data.json")
SEED = 0


def hex_dist(du, dv):
    # axial hex distance on flyvis's (u, v) lattice
    return max(abs(du), abs(dv), abs(du + dv))


def bank_record(H, bank, names):
    cells = []
    for (s, t), c in sorted(bank.content.items()):
        offs = sorted(c["offsets"].items())
        cells.append({
            "src": H.NAMES[s], "tar": H.NAMES[t],
            "n_syn_total": float(sum(n for _, n in offs)),
            "offsets": [[du, dv, float(n)] for (du, dv), n in offs],
            "max_hex_dist": max(hex_dist(du, dv) for (du, dv), _ in offs),
        })
    return cells


def ranks(arm):
    out = {}
    for r in (1, 2, 3, 4):
        with open(P3_DIR / arm / f"per_shuffle_rank{r}.csv", newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        real = [float(x["existence"]) for x in rows if x["kind"] == "real"]
        sh = [float(x["existence"]) for x in rows if x["kind"] == "shuffle"]
        assert len(real) == 1 and len(sh) == 99, (arm, r, len(real), len(sh))
        out[str(r)] = {"real": real[0], "shuffles": sh}
    return out


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    sys.path.insert(0, str(CHECKS))
    import flywire_bf_p3 as P  # noqa: E402  (imports harness.py; its main() does not run)
    H = P.H
    names = list(P.FLYWIRE_TYPES)
    types_csv = H.read_csv(ROOT / "results" / "genome" / "bank" / "types.csv")
    layout = {r.type_name: (r.layout, int(r.node_order_index))
              for r in types_csv.itertuples(index=False)}
    types = sorted(({"name": n, "group": layout[n][0], "flyvis_order": layout[n][1]}
                    for n in names), key=lambda t: t["flyvis_order"])

    fv = P.build_flyvis30_bank()
    fw, manifest = P.load_flywire_bank()
    data = {"provenance": {
        "script": "tools/viz/project_video/export_project_video_data.py",
        "banks": "flywire_bf_p3.py build_flyvis30_bank() / load_flywire_bank()",
        "shuffle": f"harness.shuffled_bank(bank, seed={SEED})",
        "ranks": "results/genome/c6/checks/flywire_bf_p3/{arm}/per_shuffle_rank{r}.csv, "
                 "column existence",
        "flywire_signs": "placeholder +1 (flywire_bank_builder.py PLACEHOLDER_SIGN); not drawn"},
        "types": types, "arms": {}}
    for arm, bank in (("flyvis30", fv), ("flywire30", fw)):
        shuf, inv = H.shuffled_bank(bank, SEED)
        assert inv["out_degrees_kept"] and inv["in_degrees_kept"], inv
        data["arms"][arm] = {
            "cells": bank_record(H, bank, names),
            "shuffle0": [[H.NAMES[s], H.NAMES[t]] for (s, t) in sorted(shuf.content)],
            "ranks": ranks(arm),
        }
        print(f"{arm}: {len(bank.content)} cells; shuffle seed {SEED}: {inv}")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=1), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
