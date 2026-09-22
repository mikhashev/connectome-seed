"""The gates of docs/plans/2026-09-23-first-rule-search-criterion.md (sections 4-6).

Planted tables: generator PG1 (planted.py). Shuffled tables: harness.shuffled_bank(REAL, s) with
s OUTSIDE the exam's null 0..98. Held-out split for seed s: FOLD == s mod 10. Nothing here fits or
scores the real bank or a real fold.

Usage (from the repository root):
    tools/.venv/Scripts/python.exe results/genome/c6/rules/first_rule/gates.py SET SEARCH [N_PROC]
SET is "dev" (planted 3000-3009, shuffled 1100-1109) or "gate" (planted 2000-2019, shuffled
1000-1019). SEARCH is "v1" or "v2". Writes gates_<SET>_<SEARCH>.json next to this file.
"""

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]))

TAU = 1e-9
J_TOL = 0.01
STARTS = 10
SETS = {"dev": {"planted": list(range(3000, 3010)), "shuffled": list(range(1100, 1110))},
        "gate": {"planted": list(range(2000, 2020)), "shuffled": list(range(1000, 1020))}}
POSITIVE_MIN = 15
NEGATIVE_MAX = 1
FIELDS = ("existence", "offset", "counts", "sign")


def evaluate(job):
    kind, seed, search = job
    import fit as FR
    import harness as H
    from planted import pg1
    assert not (kind == "shuffled" and 0 <= seed <= 98), "the exam's own null"
    t0 = time.perf_counter()
    if kind == "planted":
        g = pg1(seed)
        bank = H.Bank(f"PG1.{seed}", g["content"])
    else:
        bank, _ = H.shuffled_bank(H.REAL, seed)
    f = seed % 10
    view = H.make_view(bank, H.FOLD != f)
    t1 = time.perf_counter()
    data = FR.fit(view, starts=STARTS, search=search)
    t_fit = time.perf_counter() - t1
    info = dict(FR.LAST_FIT)
    held = H.ALL_CELLS[(H.FOLD == f)[H.ALL_CELLS[:, 0], H.ALL_CELLS[:, 1]]]
    P = H.Predictor("first_rule", FR.PROGRAM_FILES, lambda v: data)
    s_rule = H.score(P.decode(data, held), bank, held)
    s_n1 = H.score(H.N1.decode(H.fit_n1(view), held), bank, held)
    out = {"kind": kind, "seed": seed, "search": search, "heldout_fold": f,
           "J_best": min(info["J_per_start"]), "J_per_start": info["J_per_start"],
           "rules_per_start": [len(r) for r in info["rules_per_start"]],
           "sweeps_per_start": info["sweeps_per_start"],
           "restarts_with_zero_rules": sum(len(r) == 0 for r in info["rules_per_start"]),
           "best_has_zero_rules": info["n_rules"] == 0, "n_rules": info["n_rules"],
           "n_motifs": info["n_motifs"], "data_bits": H.data_bits(data),
           "heldout_rule": {k: s_rule[k] for k in FIELDS},
           "heldout_N1": {k: s_n1[k] for k in FIELDS},
           "beats_N1_existence": bool(s_n1["existence"] - s_rule["existence"] > TAU),
           "fit_seconds": t_fit, "total_seconds": time.perf_counter() - t0}
    if kind == "planted":
        M, Y = FR.grid(view)
        E, Pp, Qp, eq = g["stage1"]
        Ef = E.astype(np.float64)
        Jp = FR.total_J(Ef @ FR.rule_matrix(Pp, Qp) @ Ef.T, eq, M, Y, int(Pp.sum()))
        out.update({"J_planted": Jp, "planted_data_bits": g["data_bits"],
                    "planted_density": g["density"], "planted_attempts": g["attempts"],
                    "F1_J": bool(out["J_best"] <= Jp + J_TOL * Jp),
                    "F2_beats_N1": out["beats_N1_existence"]})
        out["finds"] = out["F1_J"] and out["F2_beats_N1"]
    return out


def summary(rows):
    pl = [r for r in rows if r["kind"] == "planted"]
    sh = [r for r in rows if r["kind"] == "shuffled"]
    allr = pl + sh
    s = {"planted_tables": len(pl), "shuffled_tables": len(sh),
         "finds": sum(r["finds"] for r in pl),
         "F1_only": sum(r["F1_J"] for r in pl), "F2_only": sum(r["F2_beats_N1"] for r in pl),
         "false_finds": sum(r["beats_N1_existence"] for r in sh),
         "restart_stall_rate_planted": sum(r["restarts_with_zero_rules"] for r in pl)
         / max(1, STARTS * len(pl)),
         "restart_stall_rate_shuffled": sum(r["restarts_with_zero_rules"] for r in sh)
         / max(1, STARTS * len(sh)),
         "tables_best_zero_rules_planted": sum(r["best_has_zero_rules"] for r in pl),
         "tables_best_zero_rules_shuffled": sum(r["best_has_zero_rules"] for r in sh),
         "mean_fit_seconds": float(np.mean([r["fit_seconds"] for r in allr])),
         "max_fit_seconds": float(np.max([r["fit_seconds"] for r in allr]))}
    s["positive_gate"] = {"expected": f">= {POSITIVE_MIN} of {len(pl)}", "got": s["finds"],
                          "pass": s["finds"] >= POSITIVE_MIN}
    s["negative_gate"] = {"expected": f"<= {NEGATIVE_MAX} of {len(sh)}", "got": s["false_finds"],
                          "pass": s["false_finds"] <= NEGATIVE_MAX}
    return s


if __name__ == "__main__":
    import multiprocessing as mp
    which, search = sys.argv[1], sys.argv[2]
    n_proc = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    jobs = [(k, s, search) for k in ("planted", "shuffled") for s in SETS[which][k]]
    t0 = time.perf_counter()
    with mp.Pool(n_proc) as pool:
        rows = pool.map(evaluate, jobs, chunksize=1)
    res = {"criterion": "docs/plans/2026-09-23-first-rule-search-criterion.md", "set": which,
           "search": search, "starts": STARTS, "wall_seconds": time.perf_counter() - t0,
           "summary": summary(rows), "tables": rows}
    print(json.dumps(res["summary"], indent=1))
    for r in rows:
        print(r["kind"], r["seed"], "finds" if r.get("finds") else "", "beatsN1"
              if r["beats_N1_existence"] else "", "rules", r["rules_per_start"],
              "J", round(r["J_best"], 1), "Jpl", round(r.get("J_planted", float("nan")), 1),
              f"{r['fit_seconds']:.1f}s")
    (HERE / f"gates_{which}_{search}.json").write_text(json.dumps(res, indent=1) + "\n",
                                                        encoding="utf-8", newline="\n")
