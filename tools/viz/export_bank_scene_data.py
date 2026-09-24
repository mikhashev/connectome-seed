"""Export the data for the Blender scene "real bank vs shuffled bank" (tools/viz/bank_scene.py).

Explanatory figure only: it reads, it registers nothing, and it writes nothing inside the repository.

What it reads
  * The real bank exactly as the C6 harness builds it: `REAL` in results/genome/c6/harness.py
    (lines 135-169: offsets.csv rows with provenance "in_json" -> offsets, "hull_filled" -> hull,
    "dropped" rows skipped; 604 non-empty (source type, target type) cells, 2,117 offset rows).
  * The shuffled bank from the harness's own function, `shuffled_bank(REAL, seed)`
    (results/genome/c6/harness.py:907), imported, not re-implemented. SEED = 0 is the first of the
    harness's 99 shuffles (`make_env`, harness.py:1227-1228) and the bank the harness names
    "real.shuffle0" (harness.py:1550).
  * Type grouping from results/genome/bank/types.csv (column `layout`, which is flyvis's own
    retina / intermediate / output layout, flyvis/connectome/connectome.py:196-221), in that
    file's row order (flyvis connectome node order).
  * flyvis's hex-to-pixel convention (flyvis/utils/hex_utils.py:70-71, mode "default") for the
    kernel insets.

Importing the harness runs its own integrity checks (folds, spec and acceptance hashes); it
exits if any registered file changed. Nothing in the harness is modified.

Run from the repository root:
    tools/.venv/Scripts/python.exe tools/viz/export_bank_scene_data.py [out.json]
"""

import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HARNESS = ROOT / "results" / "genome" / "c6" / "harness.py"
TYPES_CSV = ROOT / "results" / "genome" / "bank" / "types.csv"
DEFAULT_OUT = ROOT.parent / "connectome-seed-data" / "renderings" / "bank_scene" / "scene_data.json"
SEED = 0
FOCUS_EDGE = ("Mi9", "T4d")        # Lappalainen et al. 2024, Fig. 1e uses this pair as its example


def load_harness():
    spec = importlib.util.spec_from_file_location("c6_harness", HARNESS)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["c6_harness"] = mod
    spec.loader.exec_module(mod)
    return mod


def hex_xy(u, v):
    # flyvis/utils/hex_utils.py:70-71, mode "default"
    return 1.5 * v, -math.sqrt(3) * (u + v / 2)


def cell_record(H, key, c):
    s, t = key
    offs = sorted(c["offsets"].items())
    return {
        "src": H.NAMES[s], "tar": H.NAMES[t], "sign": int(c["sign"]),
        "n_syn_total": float(sum(n for _, n in offs)),
        "n_offsets": len(offs), "n_hull": len(c["hull"]),
    }


def kernel_record(c):
    return {
        "sign": int(c["sign"]),
        "offsets": [{"du": du, "dv": dv, "n_syn": float(n), "xy": hex_xy(du, dv)}
                    for (du, dv), n in sorted(c["offsets"].items())],
        "hull": [{"du": du, "dv": dv, "xy": hex_xy(du, dv)} for (du, dv) in sorted(c["hull"])],
    }


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    H = load_harness()
    real = H.REAL
    shuf, inv = H.shuffled_bank(real, SEED)

    # type order and groups: flyvis node order and flyvis layout, from types.csv
    T = H.read_csv(TYPES_CSV)
    types = [{"name": r.type_name, "group": r.layout, "role": r.role,
              "flyvis_order": int(r.node_order_index)} for r in T.itertuples(index=False)]
    assert sorted(t["name"] for t in types) == sorted(H.NAMES)

    # follow one content object: where did the focus edge's kernel land in the shuffled bank?
    fk = (H.IDX[FOCUS_EDGE[0]], H.IDX[FOCUS_EDGE[1]])
    focus_content = real.content[fk]
    landed = [k for k, v in shuf.content.items() if v is focus_content]
    assert len(landed) == 1
    landed = landed[0]

    data = {
        "provenance": {
            "harness": str(HARNESS.relative_to(ROOT)).replace("\\", "/"),
            "harness_sha256_lf": H.sha256_lf(HARNESS),
            "function": "shuffled_bank(REAL, seed) at harness.py:907 (rewire_and_permute at :871)",
            "seed": SEED, "swaps_per_edge": H.SWAPS_PER_EDGE,
            "bank_source": "results/genome/bank/offsets.csv (flyvis 1.2.0 fib25-fib19_v2.2.json)",
            "invariants_reported_by_harness": inv,
        },
        "types": types,
        "real": [cell_record(H, k, c) for k, c in sorted(real.content.items())],
        "shuffled": [cell_record(H, k, c) for k, c in sorted(shuf.content.items())],
        "focus": {
            "content_from": list(FOCUS_EDGE),
            "real_cell": list(FOCUS_EDGE),
            "shuffled_cell": [H.NAMES[landed[0]], H.NAMES[landed[1]]],
            "real_cell_in_shuffled": fk in shuf.content,
            "kernel": kernel_record(focus_content),
        },
    }
    assert len(data["real"]) == len(data["shuffled"]) == 604
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=1), encoding="utf-8")
    print(f"wrote {out}  ({out.stat().st_size} bytes)")
    print(f"seed {SEED}; invariants {inv}")
    print(f"focus kernel {FOCUS_EDGE} -> shuffled cell {data['focus']['shuffled_cell']}; "
          f"{FOCUS_EDGE} non-empty in shuffled: {data['focus']['real_cell_in_shuffled']}")


if __name__ == "__main__":
    main()
