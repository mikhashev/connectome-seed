"""C3 Part A readings (a) (a') (b) (c) (d) (e) (f) (g) (h) of run 703 -- CPU only.

PREVIEW DIAGNOSTIC -- NOT A TEST.  Descriptive readings, no thresholds, no verdicts.
Protocol: docs/briefs/2026-09-17-c3-jitter-and-evaluator-floor.md v1.2 (commit 97b48bb), Sec 5.
Written before A1 was launched; its sha256 is in partA/SHA256.txt, recorded before the launch.

v(k) = rung_metrics[k].val_loss of run 703; c(i) = checkpoint_metrics val_loss at iteration i.
All floats written as repr(float(x)); nothing rounded.

Operationalisations the brief leaves to the executor (named here, before the data exist):
 - (a) "each also / 0.3365 and / 56.7791": slope, residual sd and max |residual| are each divided
   by the two constants exactly as written in the brief; the full-precision source values of the
   constants are recorded beside them (0.3365 is the registered 4-decimal figure itself).
 - (b) "distance to the nearer edge": min(|x - min B|, |x - max B|), with inside yes/no beside it.
 - (g) "local linear trend": the OLS line of (a') over the 81 step-25 reads 24,000..26,000;
   lags 25/50/75/100 = index lags 1..4 on that grid; |delta residual| over all pairs at that lag;
   slope = OLS of log(median |delta|) on log(lag) over the four lags; lag-8 expectation =
   exp(intercept + slope * log 8).
 - (h) seeds 2/4/5 band = [min, max] of their recorded hook values at 25,000 (night2b 002,
   night3 004, night4 005 slim jsons).
"""

import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

CS = Path("C:/Users/mikha/Documents/dpc-research/connectome-seed")
C3 = CS / "results/diagnostics/c3"
STATUS = "PREVIEW DIAGNOSTIC -- NOT A TEST"
BRIEF = "docs/briefs/2026-09-17-c3-jitter-and-evaluator-floor.md v1.2 (commit 97b48bb), Sec 5"
REG_C3_REPLICATE = 0.3365      # pre-registration Sec 4/Sec 7, as written
SEED3_GAIN_BRIEF = 56.7791     # brief Sec 5 (a), 004 Sec 3
N3_V25000 = 1192.585838317871  # brief Sec 5 (b)
N4_V25000 = 1187.4011011123657
C0_PRECONDITION = "1212.549735546112"

REFS = {
    "003": CS / "results/night3/night3_9991-003.slim.json",
    "903": CS / "results/night4/rep_9991-903.slim.json",
    "002": CS / "results/night2/night2b_9991-002.slim.json",
    "004": CS / "results/night3/night3_9991-004.slim.json",
    "005": CS / "results/night4/night4_9991-005.slim.json",
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def r(x):
    return repr(float(x))


def rel(p):
    try:
        return str(Path(p).relative_to(CS)).replace("\\", "/")
    except ValueError:
        return str(p).replace("\\", "/")


def nodup_map(rows, key, val):
    out = {}
    for m in rows:
        k = int(m[key])
        if k in out:
            raise SystemExit(f"duplicate {key} {k} -- refusal (checklist rule 7)")
        out[k] = float(m[val])
    return out


def ols(x, y):
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    A = np.vstack([x, np.ones_like(x)]).T
    (slope, icpt), *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - (slope * x + icpt)
    return float(slope), float(icpt), res


def fit_block(ks, v):
    y = [v[k] for k in ks]
    slope, icpt, res = ols(ks, y)
    sd = float(np.std(res, ddof=2))
    i = int(np.argmax(np.abs(res)))
    out = {"n": len(ks), "k_first": ks[0], "k_last": ks[-1],
           "slope_per_iteration": r(slope), "intercept": r(icpt),
           "residual_sd_ddof2": r(sd), "max_abs_residual": r(abs(res[i])),
           "max_abs_residual_signed": r(res[i]), "max_abs_residual_at_k": ks[i]}
    for name, c in [("div_0.3365", REG_C3_REPLICATE), ("div_56.7791", SEED3_GAIN_BRIEF)]:
        out[name] = {"slope": r(slope / c), "residual_sd": r(sd / c), "max_abs_residual": r(abs(res[i]) / c)}
    return out, slope, icpt, res


def main():
    run_json = C3 / "partA" / "jitter_9991-703.json"
    d = json.loads(run_json.read_text())
    refs = {k: json.loads(p.read_text()) for k, p in REFS.items()}
    v = nodup_map(d["rung_metrics"], "iteration", "val_loss")
    c = nodup_map(d["checkpoint_metrics"], "iteration", "val_loss")
    out = {"status": STATUS, "brief": BRIEF,
           "script_sha256": {"results/diagnostics/c3/c3_jitter_reading.py": sha(__file__)},
           "inputs_sha256": {rel(run_json): sha(run_json), **{rel(p): sha(p) for p in REFS.values()}}}

    # ---------------- controls (brief Sec 6), recorded
    ref3 = refs["003"]
    argv = d["argv"]

    def argmap(a):
        m, i = {}, 0
        while i < len(a):
            if a[i].startswith("--"):
                if i + 1 < len(a) and not a[i + 1].startswith("--"):
                    m[a[i]] = a[i + 1]
                    i += 2
                else:
                    m[a[i]] = True
                    i += 1
            else:
                i += 1
        return m
    a703, a3 = argmap(argv), argmap(ref3["argv"])
    argdiff = {k: [a3.get(k), a703.get(k)] for k in sorted(set(a703) | set(a3)) if a3.get(k) != a703.get(k)}
    all_checks = [all(m["checks"].values()) for m in d["rung_metrics"]]
    c0 = next(m for m in d["checkpoint_metrics"] if int(m["iteration"]) == 0)
    out["controls"] = {
        "exit": d["exit"], "stopped_after_iter": d.get("stopped_after_iter"),
        "final_iteration": d.get("final_iteration"), "errors": d["errors"],
        "nondeterministic_ops": d["nondeterministic_ops"],
        "n_rungs_recorded": len(d["rung_metrics"]), "n_rungs_requested": len(d["rungs"]),
        "all_rung_invariants_true": bool(all(all_checks)),
        "n_rungs_with_a_false_invariant": int(sum(not x for x in all_checks)),
        "precondition_c0_repr": repr(float(c0["val_loss"])),
        "precondition_c0_equals_1212.549735546112": repr(float(c0["val_loss"])) == C0_PRECONDITION,
        "argv_diff_vs_night3_9991-003 [night3, 703]": argdiff,
        "connectome_sha256_equal_003_903": d["connectome_sha256"] == ref3["connectome_sha256"] == refs["903"]["connectome_sha256"],
        "versions_equal_003_903": d["versions"] == ref3["versions"] == refs["903"]["versions"],
        "determinism": d["determinism"],
        "total_train_wall_s": d.get("total_train_wall_s"),
        "wall_s_since_start_at_hook_25000": next((m["wall_s_since_start"] for m in d["rung_metrics"] if m["iteration"] == 25000), None),
        "lr_net_at_iter_25000": d["schedule"]["lr_net_at_iter"].get("25000"),
        "schedule_stop_iter": d["schedule"]["stop_iter"],
        "checkpoint_iterations": [int(m["iteration"]) for m in d["checkpoints"]],
    }

    grid100 = list(range(20000, 26001, 100))                 # 61
    grid25 = list(range(24000, 26001, 25))                   # 81
    assert len(grid100) == 61 and len(grid25) == 81
    missing = [k for k in grid100 + grid25 + [1000, 5000, 21612, 25212] if k not in v]
    if missing:
        raise SystemExit(f"rungs missing from run 703: {missing}")

    # ---------------- (a)
    a_blk, slope, icpt, res = fit_block(grid100, v)
    out["a_amplitude"] = a_blk
    cm3 = nodup_map(ref3["checkpoint_metrics"], "iteration", "val_loss")
    out["a_amplitude"]["constants_source"] = {
        "0.3365": "pre-registration Sec 4/Sec 7, registered as written",
        "56.7791": "brief; from 003 c(0) - c(250008) = " + r(cm3[0] - cm3[250008])}

    # ---------------- (b)
    band_ks = list(range(24500, 25501, 100))
    assert len(band_ks) == 11
    lo, hi = min(v[k] for k in band_ks), max(v[k] for k in band_ks)
    fit25000 = slope * 25000 + icpt
    sd = float(np.std(res, ddof=2))
    b = {"band_ks": band_ks, "B_min": r(lo), "B_max": r(hi), "B_width": r(hi - lo),
         "fitted_line_at_25000": r(fit25000)}
    for name, x in [("night3_003_v25000", N3_V25000), ("night4_903_v25000", N4_V25000)]:
        b[name] = {"value": r(x), "inside_B": bool(lo <= x <= hi),
                   "distance_to_nearer_edge": r(min(abs(x - lo), abs(x - hi))),
                   "value_minus_fit_at_25000_div_residual_sd": r((x - fit25000) / sd)}
    out["b_band"] = b

    # ---------------- (c)
    out["c_autocorrelation"] = {"n_pairs": len(res) - 1,
                                "lag1_pearson_of_a_residuals": r(np.corrcoef(res[:-1], res[1:])[0, 1])}

    # ---------------- (d)
    out["d_same_state_in_process"] = {
        "c21612": r(c[21612]), "v21612": r(v[21612]), "c21612_minus_v21612": r(c[21612] - v[21612]),
        "c25212": r(c[25212]), "v25212": r(v[25212]), "c25212_minus_v25212": r(c[25212] - v[25212]),
        "v25000": r(v[25000]),
        "c25212_minus_v25000": r(c[25212] - v[25000]),
        "movement_v25212_minus_v25000": r(v[25212] - v[25000]),
        "path_c25212_minus_v25212": r(c[25212] - v[25212]),
        "sum_check_abs": r(abs((v[25212] - v[25000]) + (c[25212] - v[25212]) - (c[25212] - v[25000]))),
        "rung_hook_solver_iteration_at_21612": next(m["solver_iteration_at_hook"] for m in d["rung_metrics"] if m["iteration"] == 21612),
        "rung_hook_solver_iteration_at_25212": next(m["solver_iteration_at_hook"] for m in d["rung_metrics"] if m["iteration"] == 25212),
    }

    # ---------------- (a')
    ap, slope25, icpt25, res25 = fit_block(grid25, v)
    steps = [abs(v[k + 25] - v[k]) for k in grid25[:-1]]
    ch3 = cm3[250008] - nodup_map(ref3["rung_metrics"], "iteration", "val_loss")[250000]
    cm9 = nodup_map(refs["903"]["checkpoint_metrics"], "iteration", "val_loss")
    ch9 = cm9[250008] - nodup_map(refs["903"]["rung_metrics"], "iteration", "val_loss")[250000]
    ap["abs_step25_differences"] = {"n": len(steps), "median": r(np.median(steps)), "max": r(max(steps)),
                                    "max_at_k_to_k_plus_25": grid25[int(np.argmax(steps))]}
    ap["beside_checkpoint_minus_hook_at_250k"] = {"003_c250008_minus_v250000": r(ch3),
                                                  "903_c250008_minus_v250000": r(ch9)}
    out["a_prime_fine_window"] = ap

    # ---------------- (f)
    v3 = nodup_map(ref3["rung_metrics"], "iteration", "val_loss")
    v9 = nodup_map(refs["903"]["rung_metrics"], "iteration", "val_loss")
    out["f_third_throw_seed3"] = {
        "hook_25000": {"003": r(v3[25000]), "903": r(v9[25000]), "703": r(v[25000]),
                       "903_minus_003": r(v9[25000] - v3[25000]), "703_minus_003": r(v[25000] - v3[25000]),
                       "703_minus_903": r(v[25000] - v9[25000])},
        "checkpoint_25212": {"003": r(cm3[25212]), "903": r(cm9[25212]), "703": r(c[25212]),
                             "903_minus_003": r(cm9[25212] - cm3[25212]), "703_minus_003": r(c[25212] - cm3[25212]),
                             "703_minus_903": r(c[25212] - cm9[25212])}}

    # ---------------- (g)
    g = {"trend": "OLS line of (a') over the 81 step-25 reads", "lags": {}}
    lx, ly = [], []
    for lag_i, lag in [(1, 25), (2, 50), (3, 75), (4, 100)]:
        dd = np.abs(res25[lag_i:] - res25[:-lag_i])
        med = float(np.median(dd))
        g["lags"][str(lag)] = {"n_pairs": int(dd.size), "median_abs_delta_residual": r(med),
                               "max_abs_delta_residual": r(float(np.max(dd)))}
        lx.append(math.log(lag))
        ly.append(math.log(med))
    gs, gi, _ = ols(lx, ly)
    g["slope_log_median_abs_delta_on_log_lag"] = r(gs)
    g["intercept"] = r(gi)
    g["extrapolated_median_abs_delta_at_lag_8"] = r(math.exp(gi + gs * math.log(8)))
    g["beside"] = {"003_c250008_minus_v250000": r(ch3), "903_c250008_minus_v250000": r(ch9)}
    g["brief_wording"] = "~0.5 random walk; ~0 mean reversion (descriptive)"
    out["g_lag_scaling"] = g

    # ---------------- (h)
    lag = {s: nodup_map(refs[s]["rung_metrics"], "iteration", "val_loss")[25000] for s in ["002", "004", "005"]}
    blo, bhi = min(lag.values()), max(lag.values())
    grid1000 = [k for k in [1000] + list(range(5000, 26001, 1000)) if k in v]
    out["h_transient"] = {
        "v703_25000": r(v[25000]), "minus_003_1192.585838317871": r(v[25000] - v3[25000]),
        "minus_903_1187.4011011123657": r(v[25000] - v9[25000]),
        "seeds_2_4_5_hook_25000": {s: r(x) for s, x in lag.items()},
        "band_2_4_5_min": r(blo), "band_2_4_5_max": r(bhi),
        "v703_25000_position": ("inside" if blo <= v[25000] <= bhi else ("below" if v[25000] < blo else "above")),
        "v703_on_1000_step_grid": {str(k): r(v[k]) for k in grid1000},
        "003_903_common_points": {str(k): [r(v3[k]), r(v9[k])] for k in [1000, 5000, 25000]}}

    # ---------------- (e)
    ck_iters = sorted(i for i in c if i <= 25212)
    out["e_recorded"] = {
        "v1000": {"703": r(v[1000]), "003": r(v3[1000]), "903": r(v9[1000])},
        "v5000": {"703": r(v[5000]), "003": r(v3[5000]), "903": r(v9[5000])},
        "checkpoints_0_to_25212": {str(i): {"703": r(c[i]), "003": r(cm3[i]), "903": r(cm9[i])} for i in ck_iters},
        "c12_bitwise_equal_003": repr(c[12]) == repr(cm3[12]),
        "c12_bitwise_equal_903": repr(c[12]) == repr(cm9[12]),
        "c0_bitwise_equal_003_903": repr(c[0]) == repr(cm3[0]) == repr(cm9[0])}

    # ---------------- B' (offline E1/E2/E3 on 703's checkpoints 7 and 8), if present
    bp = C3 / "partB" / "c3Bprime_proc1.json"
    if bp.exists():
        j = json.loads(bp.read_text())
        out["inputs_sha256"][rel(bp)] = sha(bp)
        bpo = {}
        for cell in j["cells"]:
            it = cell["solver_iteration"]
            e = {ev: [float(x["mean_16"]) for x in cell["calls"] if x["evaluator"] == ev] for ev in ["E1", "E2", "E3"]}
            bpo[str(it)] = {
                "stored_val_loss": cell["stored_val_loss"],
                "in_process_c": r(c[it]), "in_process_v": r(v[it]),
                "offline_means": {ev: [r(x) for x in xs] for ev, xs in e.items()},
                "offline_mean_of_five": {ev: r(np.mean(xs)) for ev, xs in e.items()},
                "in_process_v_minus_offline_E1_mean_of_five": r(v[it] - np.mean(e["E1"])),
                "in_process_c_minus_offline_E2_mean_of_five": r(c[it] - np.mean(e["E2"])),
                "within_process_max_abs_delta": {ev: cell["within_process"][ev]["max_abs_delta_16_item_mean"] for ev in e},
                "path_differences_max_abs": {k: x["max_abs"] for k, x in cell["path_differences"].items()},
                "P0": cell["P0"]}
        out["B_prime"] = bpo

    (C3 / "readings.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
