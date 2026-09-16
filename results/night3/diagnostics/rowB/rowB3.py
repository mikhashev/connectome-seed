"""Row B for night 3 (seeds 3 and 4) + the six-run analysis.

PREVIEW DIAGNOSTIC, NOT A TEST.  n = 6 individuals; the critical rho at N = 4-6 is 0.90-1.00
(docs/proposals/mi-axis-per-cell-type-design.md Sec 6, and the N >= 8 rule of
docs/next-session-plan.md Sec 5 "Do not read row B as a test at N < 8").  No number produced by
this script may be read as a test, today or later.  The label is written into every output json.

THIS FILE IS A DRIVER, NOT A RE-IMPLEMENTATION.  The measurement is
`rowB.py`, copied BYTE-IDENTICALLY from results/night2/diagnostics/rowB/rowB.py
(sha256 195a89b555bedf3a0ff00a4c4e0542eafa6370243fbf9ed954f5fe8fbf7f4082, verified with `cmp`),
imported here as a module.  Its `task_profiles`, `task_p2` and `task_traj` are called unchanged;
only the module-level table of runs is re-pointed at 9991/003 and 9991/004.

The three deliberate differences from night 2, each stated before the first run:

  D1  `rowB.RUNS`   {"003": "seed3", "004": "seed4"} instead of the four night-1/night-2 runs.
      `rowB.PAIRS` / `rowB.FOREIGN` follow (used only by `rowB.task_analyze`, which this file
      does NOT call -- the six-run analysis below replaces it).
  D2  `rowB.STATUS` says n=6 instead of n=4.  It is a label; it is written into every csv header
      and every json, and saying "n=4" in a night-3 file would be false.
  D3  `task_repro3` is `rowB.task_repro` with the run identifier as a variable (seed 3 instead of
      the hard-coded seed 0) -- the floor must be measured for the NEW seeds (rule R1 / hardening
      item 13: each metric brings its own measured floor, inheritance forbidden).  The body is
      otherwise line-for-line the same; the diff is printed by `--task diff`.

Everything else -- the evaluator (`diag1_eval_paths.py`), the ablation hook
(`ablation.py`), the recorder, the purity check with the 2026-09-15T12:07Z amendment of
rowB/README.md Sec 2 (tolerance 1e-4 on THE 16-item LOSS, per-item figures recorded beside it
with their own no-hook floor), the seven eval_rung invariants, the duplicate-key refusal, the
scratch datamate root, `torch.load`-only reads -- is night 2's code running unchanged.

WHAT THIS SCRIPT DOES NOT DO: it never trains, never writes into
connectome-seed-data/results/flow/9991/*, and never calls solver.checkpoint() or
solver.test(track_loss=True).
"""

import os
import sys

# Same two environment variables, set the same way and in the same place as
# rowB.py:29-32 / night/run_individual.py:46-49 (before torch / flyvis are imported).
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
os.environ.setdefault(
    "FLYVIS_ROOT_DIR", "C:/Users/mikha/Documents/dpc-research/connectome-seed-data"
)

import argparse
import difflib
import hashlib
import itertools
import json
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import rowB as rb  # the night-2 measurement, byte-identical copy

N2DIR = Path("C:/Users/mikha/Documents/dpc-research/connectome-seed/results/night2/"
             "diagnostics/rowB")
N3ABL = Path("C:/Users/mikha/Documents/dpc-research/connectome-seed/results/night3/"
             "diagnostics/ablation/ablation_profiles.csv")

# ------------------------------------------------------------------ D1 / D2
RUNS3 = {"003": "seed3", "004": "seed4"}
LABELS3 = ["seed3", "seed4"]
STATUS3 = "PREVIEW DIAGNOSTIC -- NOT A TEST (n=6, critical rho 0.90-1.00; N>=8 rule)"

rb.RUNS = RUNS3
rb.LABELS = LABELS3
rb.PAIRS = [("seed3", "seed4")]
rb.FOREIGN = []
rb.STATUS = STATUS3

# ------------------------------------------------------------------ six-run bookkeeping
LAB6 = ["seed0", "seed0prime", "seed1", "seed2", "seed3", "seed4"]
RUN6 = {"seed0": "000", "seed0prime": "900", "seed1": "001", "seed2": "002",
        "seed3": "003", "seed4": "004"}
# wave membership, read from results/night{1,2,3}/wave_*.json (jobs[].seed / jobs[].id)
WAVE = {"seed0": "night1", "seed0prime": "night1", "seed1": "night2",
        "seed2": "night2b", "seed3": "night3", "seed4": "night3"}
PAIRS15 = list(itertools.combinations(LAB6, 2))
TWIN = ("seed0", "seed0prime")

spearman = rb.spearman
pearson = rb.pearson


def sha_of(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def shas():
    return {"rowB.py_sha256": sha_of(HERE / "rowB.py"),
            "rowB3.py_sha256": sha_of(Path(__file__).resolve())}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--task", required=True,
                   choices=["profiles", "repro", "p2", "traj", "analyze", "diff"])
    p.add_argument("--out-dir", required=True)
    p.add_argument("--scratch-dir", required=True)
    p.add_argument("--netdir-root", required=False)
    p.add_argument("--rep", type=int, default=0)
    return p.parse_args()


def stamp(path):
    """Add both script sha256s to a json written by rowB.py (an addition, nothing removed)."""
    d = json.loads(Path(path).read_text())
    d["driver"] = {"script": "rowB3.py", "status": STATUS3, **shas()}
    Path(path).write_text(json.dumps(d, indent=1))


# ------------------------------------------------------------------ D3: the floor for seed 3
def task_repro3(a, out, scratch):
    """rowB.task_repro (rowB.py:403-421) with the run identifier as a variable.

    Night 2 measured the floor on seed 0 @ 250,008; night 3 measures it on SEED 3 @ 250,008,
    because a floor is not inherited (README Sec 5, rule R1 / hardening item 13).
    """
    run, label, ci = "003", "seed3", 71
    solver, device, types_arr, unique_types, rec_ctx, item_names, input_types, meta = rb.setup(a)
    solver_it, info = rb.load_named(solver, run, ci)
    li, means, stds, inv, ncalls = rb.eval_rowB(solver, rec_ctx)
    s = rb.summarise(means, stds)
    rec = {"meta": meta, "driver": {"script": "rowB3.py", "status": STATUS3, **shas()},
           "rep": a.rep, "pid": os.getpid(),
           "run": run, "label": label, "solver_iteration": solver_it,
           "stored_checkpoint_val_loss": repr(info["stored_val_loss"]),
           "per_item_mean": repr(float(li.mean())),
           "eval_rung_invariants": inv, "n_state_hook_calls": ncalls,
           "mean_window_aggregate": {T: repr(float(s["mean_window"][:, i].mean()))
                                     for i, T in enumerate(unique_types)},
           "last_step_aggregate": {T: repr(float(s["last_step"][:, i].mean()))
                                   for i, T in enumerate(unique_types)}}
    assert all(inv.values()), inv
    (Path(scratch) / f"rowB3_repro_proc{a.rep}.json").write_text(json.dumps(rec, indent=1))
    print("REPRO3", a.rep, label, "loss", repr(float(li.mean())))
    return 0


def task_diff(a, out, scratch):
    """Print the literal diff of task_repro3 against rowB.task_repro (D3), so that the only
    hand-written measurement code in this directory is auditable in one screen."""
    import inspect
    x = inspect.getsource(rb.task_repro).splitlines()
    y = inspect.getsource(task_repro3).splitlines()
    print("\n".join(difflib.unified_diff(x, y, "rowB.task_repro", "rowB3.task_repro3",
                                         lineterm="")))
    return 0


# ================================================================== six-run analysis
def load_six(fname, n3dir):
    """Merge the night-2 profile csv (4 runs, NOT recomputed -- cited) with the night-3 one."""
    t2, l2, P2, I2, c2 = rb.load_profile_csv(N2DIR / fname)
    t3, l3, P3, I3, c3 = rb.load_profile_csv(Path(n3dir) / fname)
    assert t2 == t3, "cell-type order differs between night 2 and night 3 csvs"
    assert c2 == c3, "held-out item order differs between night 2 and night 3 csvs"
    assert l2 == ["seed0", "seed0prime", "seed1", "seed2"], l2
    assert l3 == ["seed3", "seed4"], l3
    P = rb.NoDupDict()
    I = rb.NoDupDict()
    for src_p, src_i in ((P2, I2), (P3, I3)):
        for lab in src_p:
            P[lab] = src_p[lab]
            I[lab] = src_i[lab]
    return t2, dict(P), dict(I), c2


def d15(vecs):
    return {f"{x}|{y}": 1.0 - spearman(vecs[x], vecs[y]) for x, y in PAIRS15}


def task_analyze(a, out, scratch):
    base = {"status": STATUS3, "script": "rowB3.py + rowB.py (byte-identical copy)", **shas(),
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "measure": "Spearman rho over the 65 types; distance = 1 - rho "
                       "(rowB/README.md Sec 4, fixed before the first look)",
            "primary_summary": "mean over the whole simulation window, all 65 types",
            "secondary_summary": "value at the last simulation step",
            "item_composition": "all 16 (primary); 13 without ambush_2 and 10 without "
                                "bandage_1 are context only",
            "n": 6, "individuals": LAB6, "runs": RUN6, "wave": WAVE,
            "night2_profiles_reused_not_recomputed": [
                str(N2DIR / "rowB_profiles_250008.csv"),
                str(N2DIR / "rowB_profiles_25212.csv"),
                str(N2DIR / "rowB_profiles_iter0.csv")],
            "night2_rowB_script_sha256":
                "195a89b555bedf3a0ff00a4c4e0542eafa6370243fbf9ed954f5fe8fbf7f4082"}

    types, P250, I250, item_cols = load_six("rowB_profiles_250008.csv", out)
    _, P25, I25, _ = load_six("rowB_profiles_25212.csv", out)
    _, P0, I0, _ = load_six("rowB_profiles_iter0.csv", out)
    idx13 = [i for i, n in enumerate(item_cols) if "ambush_2" not in n]
    idx10 = [i for i, n in enumerate(item_cols)
             if "ambush_2" not in n and "bandage_1" not in n]
    assert len(idx13) == 13 and len(idx10) == 10
    assert len(types) == 65

    V16 = {l: P250[l]["mean_window"] for l in LAB6}
    V13 = {l: I250[l][idx13].mean(axis=0) for l in LAB6}
    V10 = {l: I250[l][idx10].mean(axis=0) for l in LAB6}
    W16 = {l: P25[l]["mean_window"] for l in LAB6}
    Z16 = {l: P0[l]["mean_window"] for l in LAB6}

    # ---------------- invariants + eval records of the new seeds
    er = json.loads((Path(out) / "rowB_eval_records.json").read_text())
    inv_names = ["lr_unchanged", "pen_lr_unchanged", "dt_unchanged",
                 "scheduler_iter_unchanged", "back_in_train_mode",
                 "was_in_train_mode_before", "dataset_augment_restored"]
    inv_seen, inv_n = set(), 0
    purity = {}
    for it, blk in er["checkpoints"].items():
        for lab, r in blk.items():
            for k in ("eval_rung_invariants_with_hook", "eval_rung_invariants_without_hook"):
                inv_n += 1
                assert sorted(r[k]) == sorted(inv_names), r[k]
                inv_seen.add(tuple(sorted(r[k].items())))
                assert all(r[k].values()), (it, lab, k, r[k])
            purity[f"{lab}@{it}"] = {
                kk: r[kk] for kk in (
                    "purity_abs_diff_of_the_16_item_loss", "purity_tol", "purity_pass",
                    "purity_bitwise_identical_per_item",
                    "per_item_max_abs_diff_hook_vs_nohook",
                    "per_item_max_abs_diff_nohook_vs_nohook_FLOOR",
                    "per_item_max_abs_diff_hook_vs_nohook_in_float32_ulps",
                    "per_item_mean_with_hook", "per_item_mean_without_hook",
                    "n_state_hook_calls", "steps_steady_state")}
            purity[f"{lab}@{it}"]["steps_per_item_unique"] = \
                sorted(set(r["steps_per_item"]))

    # ---------------- controls
    repro = [json.loads((Path(scratch) / f"rowB3_repro_proc{r}.json").read_text())
             for r in (1, 2, 3)]
    assert all(x["label"] == "seed3" and x["solver_iteration"] == 250008 for x in repro)
    assert list(repro[0]["mean_window_aggregate"].keys()) == types
    for x in repro:
        assert sorted(x["eval_rung_invariants"]) == sorted(inv_names), x["eval_rung_invariants"]
        assert all(x["eval_rung_invariants"].values()), x["eval_rung_invariants"]
        inv_n += 1
    rowc = json.loads((Path(scratch) / "rowC_meta.json").read_text())
    RV = [np.array([float(x["mean_window_aggregate"][T]) for T in types]) for x in repro]
    rho_pairs = {f"proc{i+1}|proc{j+1}": spearman(RV[i], RV[j])
                 for i in range(3) for j in range(i + 1, 3)}
    dB_pairs = {f"proc{i+1}|proc{j+1}": float(np.max(np.abs(RV[i] - RV[j])))
                for i in range(3) for j in range(i + 1, 3)}
    floor_rho = float(max(1.0 - r for r in rho_pairs.values()))
    floor_dB = float(max(dB_pairs.values()))

    ladder0 = {}
    for x, y in PAIRS15:
        u, v = Z16[x], Z16[y]
        ladder0[f"{x}|{y}"] = {
            "spearman_rho": repr(spearman(u, v)),
            "distance_1_minus_rho": repr(1.0 - spearman(u, v)),
            "max_abs_deltaB": repr(float(np.max(np.abs(u - v)))),
            "bitwise_identical": bool(np.array_equal(u, v)),
            "new_pair_in_night3": bool("seed3" in (x, y) or "seed4" in (x, y))}

    p2 = json.loads((Path(scratch) / "rowB3_p2.json").read_text())
    for lab, r in p2["runs"].items():
        for k in ("eval_rung_invariants_base", "eval_rung_invariants_ablated"):
            assert all(r[k].values()), (lab, k)
            inv_n += 1

    controls = dict(base)
    controls["eval_rung_invariants"] = {
        "the_seven": inv_names,
        "n_evaluations_with_all_seven_recorded_and_asserted_true": inv_n,
        "of_which": "12 in the profiles task (6 evaluations x with-hook/without-hook), "
                    "4 in P2 (2 runs x base/ablated), 3 in the repro processes",
        "row_C_trajectory_evaluations": {
            "n_rows": rowc["n_rows"], "all_invariants_pass": rowc["all_invariants_pass"],
            "note": "asserted per evaluation in rowB.task_traj:480-481; the aggregate flag "
                    "is carried here from the scratch rowC_meta.json"},
        "total_evaluations_with_the_seven_asserted": inv_n + rowc["n_rows"],
        "note": "hardening item 1; recorded per evaluation in rowB_eval_records.json "
                "(profiles), in the P2 block and in each repro json",
        "distinct_invariant_tuples_observed": len(inv_seen)}
    controls["hook_purity_new_seeds"] = purity
    controls["hook_purity_rule"] = (
        "rowB/README.md Sec 2 with its 2026-09-15T12:07Z amendment: the 1e-4 tolerance applies "
        "to THE 16-item loss; the per-item max difference, the same figure in float32 ULPs and "
        "its own no-hook-vs-no-hook floor are recorded beside it, measured not assumed")
    controls["P0_ladder_iteration_0_all_15_pairs"] = ladder0
    controls["P0_ladder_250008_for_contrast"] = {k: repr(v) for k, v in d15(V16).items()}
    controls["floor_new_seeds"] = {
        "what": "seed 3 @ 250,008 evaluated in 3 fresh processes; measured for THIS metric at "
                "THIS state on the NEW seeds, not inherited from night 2 (rule R1 / hardening "
                "item 13, README Sec 5)",
        "spearman_rho_between_processes": {k: repr(v) for k, v in rho_pairs.items()},
        "floor_1_minus_rho": repr(floor_rho),
        "max_per_type_abs_deltaB": {k: repr(v) for k, v in dB_pairs.items()},
        "floor_max_abs_deltaB": repr(floor_dB),
        "per_item_mean_loss_per_process": [x["per_item_mean"] for x in repro],
        "pids": [x["pid"] for x in repro],
        "night2_floor_seed0_for_reference": {"floor_1_minus_rho": "0.0",
                                             "floor_max_abs_deltaB": "8.251646477219765e-08",
                                             "source": str(N2DIR / "rowB_controls.json")},
        "caveat": "a rank floor of exactly 0.0 makes 'margin exceeds the floor' trivially "
                  "satisfiable (002 Sec 5i review item 1); the load-bearing figure is the "
                  "value-level max|dB|"}
    controls["P2_silence_R1_R8_new_seeds"] = p2["runs"]
    controls["P2_ablated_types"] = p2["ablated_types"]
    (Path(out) / "rowB_controls.json").write_text(json.dumps(controls, indent=1))

    # ---------------- (a) 15 pairwise distances + twin trap restated
    def blk(vecs):
        return {f"{x}|{y}": {"spearman_rho": repr(spearman(vecs[x], vecs[y])),
                             "distance_1_minus_rho": repr(1.0 - spearman(vecs[x], vecs[y])),
                             "pearson_r_context_only": repr(pearson(vecs[x], vecs[y])),
                             "wave_x": WAVE[x], "wave_y": WAVE[y],
                             "same_wave": WAVE[x] == WAVE[y],
                             "same_seed": (x, y) == TWIN}
                for x, y in PAIRS15}

    D16 = d15(V16)
    d_twin = D16[f"{TWIN[0]}|{TWIN[1]}"]
    foreign = {k: v for k, v in D16.items() if k != f"{TWIN[0]}|{TWIN[1]}"}
    nearest = min(foreign, key=foreign.get)

    per_item = {}
    twin_min_items = 0
    for k, nm in enumerate(item_cols):
        vi = {l: I250[l][k] for l in LAB6}
        di = d15(vi)
        dt_ = di[f"{TWIN[0]}|{TWIN[1]}"]
        fo = {kk: vv for kk, vv in di.items() if kk != f"{TWIN[0]}|{TWIN[1]}"}
        nr = min(fo, key=fo.get)
        ok = all(dt_ < v for v in fo.values())
        twin_min_items += int(ok)
        per_item[nm] = {"d_twin": repr(dt_), "nearest_foreign_pair": nr,
                        "d_nearest_foreign": repr(fo[nr]),
                        "twin_is_minimum_of_15": bool(ok),
                        "pairs": {kk: repr(vv) for kk, vv in di.items()}}

    dist = dict(base)
    dist["floor_1_minus_rho_seed3"] = repr(floor_rho)
    dist["subsets"] = {"16": blk(V16),
                       "13_no_ambush2_CONTEXT_ONLY": blk(V13),
                       "10_no_ambush2_no_bandage1_CONTEXT_ONLY": blk(V10)}
    dist["twin_trap_restated_at_n6"] = {
        "rule": "d(0,0') must be the minimum of the pairs AND below the nearest foreign pair "
                "by more than the measured floor (rowB/README.md Sec 6), now over 15 pairs "
                "instead of 6",
        "d_twin": repr(d_twin),
        "is_minimum_of_15": bool(all(d_twin < v for v in foreign.values())),
        "nearest_foreign_pair": nearest,
        "d_nearest_foreign": repr(foreign[nearest]),
        "margin": repr(foreign[nearest] - d_twin),
        "floor_1_minus_rho_seed3": repr(floor_rho),
        "margin_exceeds_floor": bool((foreign[nearest] - d_twin) > floor_rho),
        "n_items_twin_is_minimum_of_15": twin_min_items,
        "n_items": len(item_cols),
        "night2_values_for_comparison": {"d_twin": "0.34873251748251743",
                                         "nearest_foreign_of_6": "seed0|seed2",
                                         "d_nearest_foreign": "0.545541958041958",
                                         "margin": "0.1968", "n_items_min": "16/16"},
        "reading": "the load-bearing statement of night 2 (002 Sec 5i review item 1) is "
                   "'the twin pair is the minimum in every item', not the margin over a "
                   "rank floor of 0.0",
        "note": STATUS3}
    dist["per_item_16"] = per_item
    dist["secondary_last_step_16"] = blk({l: P250[l]["last_step"] for l in LAB6})
    dist["secondary_57_without_R1_R8"] = blk(
        {l: np.array([v for t, v in zip(types, P250[l]["mean_window"])
                      if not (t.startswith("R") and t[1:].isdigit())]) for l in LAB6})

    # ---------------- (b) same-wave vs cross-wave
    same_wave = {k: v for k, v in D16.items()
                 if WAVE[k.split("|")[0]] == WAVE[k.split("|")[1]]}
    cross = {k: v for k, v in D16.items() if k not in same_wave}
    cv = np.array(sorted(cross.values()))
    ordered = sorted(D16.items(), key=lambda kv: kv[1])
    dist["same_wave_vs_cross_wave"] = {
        "what": "the FIRST comparison with two same-wave pairs: (0,0') is twins AND same wave "
                "(night1); (3,4) is different seeds AND same wave (night3); the other 13 pairs "
                "are different seeds AND different waves",
        "same_wave_pairs": {k: {"d": repr(v), "wave": WAVE[k.split('|')[0]],
                                "same_seed": k == f"{TWIN[0]}|{TWIN[1]}"}
                            for k, v in sorted(same_wave.items(), key=lambda kv: kv[1])},
        "cross_wave_pairs_sorted": {k: repr(v)
                                    for k, v in sorted(cross.items(), key=lambda kv: kv[1])},
        "cross_wave_n": len(cross),
        "cross_wave_min": repr(float(cv.min())), "cross_wave_median": repr(float(np.median(cv))),
        "cross_wave_mean": repr(float(cv.mean())), "cross_wave_max": repr(float(cv.max())),
        "cross_wave_sd": repr(float(cv.std(ddof=1))),
        "d_3_4": repr(D16["seed3|seed4"]),
        "rank_of_d_3_4_among_15_ascending": 1 + [k for k, _ in ordered].index("seed3|seed4"),
        "rank_of_d_twin_among_15_ascending": 1 + [k for k, _ in ordered].index(
            f"{TWIN[0]}|{TWIN[1]}"),
        "n_cross_wave_below_d_3_4": int(sum(1 for v in cross.values() if v < D16["seed3|seed4"])),
        "all_15_ascending": [[k, repr(v), "same_wave" if k in same_wave else "cross_wave"]
                             for k, v in ordered],
        "note": "numbers only, no verdict (n = 6, two same-wave pairs, one of them twins)"}
    (Path(out) / "rowB_distances.json").write_text(json.dumps(dist, indent=1))

    # ---------------- (c)/(d) exploratory axes
    ti = {T: i for i, T in enumerate(types)}
    ax1 = {}
    for T in ("T5c", "T5d", "T2"):
        i = ti[T]
        vals = {l: float(V16[l][i]) for l in LAB6}
        ax1[T] = {"mean_window": {l: repr(vals[l]) for l in LAB6},
                  "ratio_seed3_over_seed4": repr(vals["seed3"] / vals["seed4"])
                  if vals["seed4"] != 0 else "div0",
                  "abs_ratio_max_over_min_in_pair_3_4": repr(
                      max(abs(vals["seed3"]), abs(vals["seed4"]))
                      / min(abs(vals["seed3"]), abs(vals["seed4"])))
                  if min(abs(vals["seed3"]), abs(vals["seed4"])) > 0 else "div0",
                  "abs_ratio_max_over_min_in_twins_0_0prime": repr(
                      max(abs(vals["seed0"]), abs(vals["seed0prime"]))
                      / min(abs(vals["seed0"]), abs(vals["seed0prime"])))
                  if min(abs(vals["seed0"]), abs(vals["seed0prime"])) > 0 else "div0"}
    def band(x, y):
        u, v = V16[x], V16[y]
        d = np.abs(u - v)
        o = np.argsort(-d)
        return {"pair": f"{x}|{y}",
                "max_per_type_abs_deltaB": repr(float(d.max())),
                "median_per_type_abs_deltaB": repr(float(np.median(d))),
                "top8_per_type": [[types[i], repr(float(u[i])), repr(float(v[i])),
                                   repr(float(d[i]))] for i in o[:8]],
                "argmax_type_x": types[int(np.argmax(u))],
                "max_x": repr(float(u.max())),
                "argmax_type_y": types[int(np.argmax(v))],
                "max_y": repr(float(v.max())),
                "ratio_of_the_two_profile_maxima": repr(float(u.max() / v.max()))}

    expl = dict(base)
    expl["twin_amplitude_band_recomputed"] = {
        "why": "002 Sec 5i second pass item 3 states the twin amplitude band as 'T5c 41.6 vs "
               "23.8 (1.75x)'. Recomputed from "
               "night2/diagnostics/rowB/rowB_profiles_250008.csv, column mean_window: seed 0's "
               "T5c is 41.6183 and seed 0-prime's T5c is -0.0365; 23.8381 is seed 0-prime's "
               "Tm4, which is that profile's maximum. 1.7459 is therefore the ratio of the two "
               "profiles' MAXIMA, which sit on DIFFERENT types -- not a per-type T5c ratio. "
               "The number is right for what it measures; the type label attached to it is "
               "not. Reported, not corrected in the night-2 file.",
        "seed0_T5c": repr(float(V16["seed0"][ti["T5c"]])),
        "seed0prime_T5c": repr(float(V16["seed0prime"][ti["T5c"]])),
        "seed0prime_Tm4": repr(float(V16["seed0prime"][ti["Tm4"]])),
        "ratio_of_profile_maxima_0_over_0prime": repr(
            float(V16["seed0"].max() / V16["seed0prime"].max())),
        "profile_sd_ratio_0_over_0prime_unaffected": repr(
            float(V16["seed0"].std() / V16["seed0prime"].std())),
        "per_type_band_twins": band("seed0", "seed0prime"),
        "per_type_band_pair_3_4": band("seed3", "seed4"),
        "consequence_stated_not_decided": "the per-type twin amplitude band is max|dB| = 41.65 "
            "(T5c 41.62 -> -0.04 between two runs of ONE seed), not a factor of 1.75; a "
            "threshold of the form 'exceed 1.75x to be a real per-type difference' is therefore "
            "more permissive than the twin data support. Whether the rule of 002 Sec 5i second "
            "pass item 3 should be restated is Mike's and the reviewers' call, not this "
            "diagnostic's. The qualitative conclusion it was written to support -- amplitude "
            "floats between twins, rank does not -- is unchanged and is strengthened.",
        "note": STATUS3}
    expl["axis_1_activity_on_T5c_T5d_T2"] = {
        "declared": "docs/next-session-plan.md Sec 2a 'Exploratory axes for night 3 (Ark 10:25)' "
                    "-- named BEFORE the launch; exploratory, no verdict",
        "twin_amplitude_band_as_published": "T5c 41.62 vs 23.84 between the two runs of seed 0 "
                               "= 1.75x (002 Sec 5i second pass item 3); profile sd 7.38 vs "
                               "5.22 = 1.42x; the band is the measured non-determinism floor of "
                               "row B in AMPLITUDE (rank is unaffected: twin minimum in 16/16 "
                               "items)",
        "twin_amplitude_band_see_also": "twin_amplitude_band_recomputed in this file -- 23.84 is "
                               "seed 0-prime's Tm4, not its T5c (which is -0.0365); the 1.42x sd "
                               "figure is unaffected",
        "types": ax1}
    prof = {}
    for l in LAB6:
        v = V16[l]
        prof[l] = {"sd_65": repr(float(v.std(ddof=1))), "sd_65_population": repr(float(v.std())),
                   "min": repr(float(v.min())), "max": repr(float(v.max())),
                   "range": repr(float(v.max() - v.min())),
                   "mean": repr(float(v.mean())),
                   "argmax_type": types[int(np.argmax(v))],
                   "argmin_type": types[int(np.argmin(v))],
                   "n_types_abs_below_1e-3": int((np.abs(v) < 1e-3).sum()),
                   "wave": WAVE[l]}
    expl["axis_2_profile_compression"] = {
        "declared": "docs/next-session-plan.md Sec 2a; exploratory, no verdict",
        "night2_published_sd": {"seed0": "7.38", "seed0prime": "5.22", "seed1": "2.44",
                                "seed2": "2.72",
                                "source": "002 Sec 5i CC check (iii), population sd over the 65 "
                                          "mean_window values"},
        "per_individual": prof,
        "within_pair_amplitude_ratio_3_4": {
            "sd_ratio": repr(max(float(V16['seed3'].std()), float(V16['seed4'].std()))
                             / min(float(V16['seed3'].std()), float(V16['seed4'].std()))),
            "range_ratio": repr(max(float(V16['seed3'].max() - V16['seed3'].min()),
                                    float(V16['seed4'].max() - V16['seed4'].min()))
                                / min(float(V16['seed3'].max() - V16['seed3'].min()),
                                      float(V16['seed4'].max() - V16['seed4'].min()))),
            "twin_reference_sd_ratio_0_0prime": repr(
                max(float(V16['seed0'].std()), float(V16['seed0prime'].std()))
                / min(float(V16['seed0'].std()), float(V16['seed0prime'].std()))),
            "note": "(3,4) are DIFFERENT seeds in one wave; (0,0') are the SAME seed in one "
                    "wave -- the two ratios are not the same quantity"},
        "confound_named_before_night_3": "002 Sec 5i second pass item 5 (Ark): compression "
                                         "splits by NIGHT, not by individual, with two nights; "
                                         "night 3 adds a third night and a second same-wave pair"}
    (Path(out) / "rowB_exploratory.json").write_text(json.dumps(expl, indent=1))

    # ---------------- (e) B vs A
    va = dict(base)
    va["row_A_source_night3"] = str(N3ABL)
    if N3ABL.exists():
        abl = rb.read_csv_nodup(N3ABL, ("label", "type"))
        labs_a = sorted({k[0] for k in abl})
        A = {}
        missing = []
        for l in ("seed3", "seed4"):
            if all((l, T) in abl for T in types):
                A[l] = np.array([float(abl[(l, T)]["delta_16"]) for T in types])
            else:
                missing.append(l)
        va["row_A_labels_found"] = labs_a
        va["primary_i_within_individual"] = {
            l: {"spearman_rho_B_vs_deltaT": repr(spearman(V16[l], A[l])),
                "pearson_r_context_only": repr(pearson(V16[l], A[l])),
                "spearman_absB_vs_absdeltaT": repr(spearman(np.abs(V16[l]), np.abs(A[l])))}
            for l in A}
        va["A_side_missing"] = missing
        va["night2_within_individual_for_reference"] = {
            "seed0": "0.38933566433566436", "seed0prime": "0.4811188811188811",
            "seed1": "0.5629807692307692", "seed2": "0.6532342657342657",
            "source": str(N2DIR / "rowB_vs_rowA.json")}
    else:
        va["A_side_status"] = "PENDING -- the night-3 ablation profiles did not exist when this " \
                              "analysis ran; the B side is complete and is in " \
                              "rowB_profiles_250008.csv"
        va["primary_i_within_individual"] = None
    va["B_side_seed3_seed4"] = {l: {T: repr(float(V16[l][i])) for i, T in enumerate(types)}
                                for l in ("seed3", "seed4")}
    (Path(out) / "rowB_vs_rowA.json").write_text(json.dumps(va, indent=1))

    # ---------------- (f)/(g) preview 25k -> 250k
    D25 = d15(W16)
    keys = [f"{x}|{y}" for x, y in PAIRS15]
    self_cons = {l: spearman(W16[l], V16[l]) for l in LAB6}
    order = sorted(self_cons, key=self_cons.get)
    prev = dict(base)
    prev["within_run_B25212_vs_B250008"] = {
        l: {"spearman_rho": repr(self_cons[l]),
            "max_abs_deltaB": repr(float(np.max(np.abs(W16[l] - V16[l])))),
            "wave": WAVE[l],
            "source": "night2 csv (not recomputed)" if l in ("seed0", "seed0prime", "seed1",
                                                             "seed2") else "night3 csv"}
        for l in LAB6}
    prev["self_consistency_ranking_ascending"] = [[l, repr(self_cons[l])] for l in order]
    prev["seed2_0_36_in_context"] = {
        "seed2": repr(self_cons["seed2"]),
        "seed3": repr(self_cons["seed3"]), "seed4": repr(self_cons["seed4"]),
        "rank_of_seed2_ascending": 1 + order.index("seed2"),
        "rank_of_seed3_ascending": 1 + order.index("seed3"),
        "rank_of_seed4_ascending": 1 + order.index("seed4"),
        "n": 6,
        "night2_open_question": "002 Sec 5i second pass item 4: 'why seed 2's self-consistency "
                                "is 0.36 -- no explanation'; this is context for it, not an answer"}
    prev["between_run_distances_15_pairs"] = {
        "pairs": keys,
        "at_25212": [repr(D25[k]) for k in keys],
        "at_250008": [repr(D16[k]) for k in keys],
        "spearman_over_the_15_distances": repr(
            spearman(np.array([D25[k] for k in keys]), np.array([D16[k] for k in keys]))),
        "pearson_over_the_15_distances_context_only": repr(
            pearson(np.array([D25[k] for k in keys]), np.array([D16[k] for k in keys]))),
        "twin_is_minimum_of_15_at_25212": bool(
            all(D25[f"{TWIN[0]}|{TWIN[1]}"] < v for k, v in D25.items()
                if k != f"{TWIN[0]}|{TWIN[1]}")),
        "night2_value_over_6_distances": "0.6",
        "note": "the 15 distances are derived from 6 objects and are not independent "
                "(002 Sec 5i second pass item 6)"}
    prev["iteration_0_for_reference"] = {k: repr(v) for k, v in d15(Z16).items()}
    prev["note"] = "preview, not a test (" + STATUS3 + ")"
    (Path(out) / "rowB_preview.json").write_text(json.dumps(prev, indent=1))

    print("ANALYZE3 DONE")
    print("FLOOR(seed3) 1-rho", repr(floor_rho), "max|dB|", repr(floor_dB))
    print("TWIN", json.dumps(dist["twin_trap_restated_at_n6"]))
    print("SAMEWAVE", json.dumps(dist["same_wave_vs_cross_wave"]["all_15_ascending"]))
    return 0


def main():
    a = parse_args()
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    scratch = Path(a.scratch_dir)
    scratch.mkdir(parents=True, exist_ok=True)
    if a.task == "profiles":
        rc = rb.task_profiles(a, out, scratch)
        stamp(out / "rowB_eval_records.json")
        return rc
    if a.task == "repro":
        return task_repro3(a, out, scratch)
    if a.task == "p2":
        rc = rb.task_p2(a, out, scratch)
        # rowB.task_p2 writes rowB_p2.json into the scratch dir; rename to the night-3 name
        src = scratch / "rowB_p2.json"
        d = json.loads(src.read_text())
        d["driver"] = {"script": "rowB3.py", "status": STATUS3, **shas()}
        (scratch / "rowB3_p2.json").write_text(json.dumps(d, indent=1))
        src.unlink()
        return rc
    if a.task == "traj":
        rc = rb.task_traj(a, out, scratch)
        stamp(scratch / "rowC_meta.json")
        return rc
    if a.task == "analyze":
        return task_analyze(a, out, scratch)
    if a.task == "diff":
        return task_diff(a, out, scratch)
    raise SystemExit(2)


if __name__ == "__main__":
    sys.exit(main())
