"""Diagnostics AFTER the gate run failed (G-e+ and G-o0; gates.json). Not a gate, not a fix, and
nothing in the rule is changed by it. Synthetic gate banks GB1/GB0 only; no real-bank cell.

Question: is either failure an implementation fault, or the registered rule's own behaviour?
  offset (G-o0): split the rule's held-out Jaccard into the library restriction and the side
    switch, and check that side_choose with unrestricted candidates reproduces harness.eb_choose;
  existence (G-e+): held-out log-loss of the unquantised float model, after rounding, after the
    coordinate-descent pass and after c's refit, beside BF_1 (from gates.json).

Usage (from the repository root):
    tools/.venv/Scripts/python.exe results/genome/c6/rules/second_rule/gate_diagnostics.py
Writes gate_diagnostics.json next to this file.
"""

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
os.environ.pop("SECOND_RULE_SPREAD_DIR", None)

import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]))
K = 10


def _jac(pred_sets, bank, cells):
    out = []
    for (s, t), ps in zip(cells.tolist(), pred_sets):
        if (s, t) in bank.content:
            a, b = set(ps), set(bank.content[(s, t)]["offsets"])
            out.append(len(a & b) / len(a | b) if a | b else 1.0)
    return float(np.mean(out))


def _ll(p, y):
    import harness as H
    p = np.clip(p, *H.CLIP)
    return float(np.mean(-(y * np.log(p) + (~y) * np.log(1 - p))))


def one(job):
    import harness as H
    import fit as R
    from gate_banks import gate_bank
    name, f = job
    b = gate_bank(name)
    held = H.FOLD == f
    view = H.make_view(b, ~held)
    cells = H.ALL_CELLS[held[H.ALL_CELLS[:, 0], H.ALL_CELLS[:, 1]]]
    s, t = cells[:, 0], cells[:, 1]
    # ---- offsets
    off = R.fit_offsets(view)
    lib = off["lib"]
    uniq, J, sid, src, _ = H.eb_tables(view)
    everything = np.ones(len(sid), bool)
    ch, _, _ = R.side_choose(J, sid, src, everything, off["alpha_src"], np.arange(len(uniq)))
    held_ne = [(a, c) for a, c in zip(s.tolist(), t.tolist()) if (a, c) in b.content]
    neb = H.NEB.decode(H.fit_neb(view), cells)
    row = {"bank": name, "fold": f,
           "eb_choose_reproduced_when_unrestricted": bool(np.array_equal(
               ch, H.eb_choose(J, sid, src, everything, off["alpha_src"]))),
           "offset_rule": _jac([lib[off["B"][y]] if off["f"][y] > off["e"][x] else
                                lib[off["A"][x]] for x, y in zip(s, t)], b, cells),
           "offset_source_side_library": _jac([lib[off["A"][x]] for x in s], b, cells),
           "offset_target_side_library": _jac([lib[off["B"][y]] for y in t], b, cells),
           "offset_source_side_unrestricted": _jac([uniq[ch[x]] for x in s], b, cells),
           "offset_N_EB": _jac([list(o) for o in neb["offsets"]], b, cells),
           "n_library_sets": len(lib), "n_library_offsets": len({o for q in lib for o in q}),
           "library_bits": H.data_bits({"L": R.pack_library(lib)}),
           "heldout_sets_in_library": sum(tuple(sorted(b.content[k]["offsets"])) in set(lib)
                                          for k in held_ne) / len(held_ne),
           "heldout_cells_on_target_side": float(np.mean([off["f"][y] > off["e"][x]
                                                          for x, y in held_ne]))}
    # ---- existence
    y = b.exists[s, t]
    ex = R.fit_existence(view, K)
    q = R.ExistQ(ex)
    row.update({"lambda": ex["lam"],
                "existence_float_model": _ll(H._sig(R.logit_grid(ex["O"], ex["U"], ex["V"],
                                                                 ex["W"], ex["G"])[s, t]), y),
                "existence_rounded": _ll(H._sig(q.grid()[s, t]), y)})
    q.descend()
    row["existence_after_descent"] = _ll(H._sig(q.grid()[s, t]), y)
    q.refit_c()
    row["existence_after_c_refit"] = _ll(H._sig(q.grid()[s, t]), y)
    return row


def main():
    import harness as H
    with ProcessPoolExecutor(20) as ex:
        rows = list(ex.map(one, [(n, f) for n in ("GB1", "GB0") for f in range(10)]))
    g = json.loads((HERE / "gates.json").read_text(encoding="utf-8"))
    per = g["per_fold_scores_gate_banks"]
    for r in rows:
        r["existence_BF1_from_gates"] = per[r["bank"]]["BF1"][r["fold"]]["existence"]
        r["existence_rule_from_gates"] = per[r["bank"]]["rule"][r["fold"]]["existence"]
    summary = {}
    for n in ("GB1", "GB0"):
        rr = [r for r in rows if r["bank"] == n]
        keys = [k for k in rr[0] if isinstance(rr[0][k], float)]
        summary[n] = {k: float(np.mean([r[k] for r in rr])) for k in keys}
        summary[n]["folds_float_model_beats_BF1_by_tau"] = int(sum(
            r["existence_BF1_from_gates"] - r["existence_float_model"] > H.TAU for r in rr))
        summary[n]["rule_scores_reproduce_gates_json"] = all(
            abs(r["existence_after_c_refit"] - r["existence_rule_from_gates"]) < 1e-12
            and abs(r["offset_rule"] - per[n]["rule"][r["fold"]]["offset"]) < 1e-12 for r in rr)
    out = {"what": "Diagnostics after the gate run failed (G-e+, G-o0). Not a gate; nothing in "
                   "the rule is changed. Synthetic gate banks only.",
           "fit_sha256_lf": H.sha256_lf(HERE / "fit.py"), "k": K, "summary": summary,
           "per_fold": rows}
    (HERE / "gate_diagnostics.json").write_text(json.dumps(out, indent=1) + "\n",
                                                encoding="utf-8", newline="\n")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
