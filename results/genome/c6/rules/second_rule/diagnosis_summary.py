"""Aggregates of the gate diagnosis (diagnosis.py). Reads diagnosis_registered.json,
diagnosis_power_rows.json, diagnosis_gb0_rows.json and gates.json; writes diagnosis_summary.json
and diagnosis_banks.json. Synthetic banks only.

Sign conventions (as the harness's margin()): existence is a log-loss, lower is better.
  "margin over N1"      = N1 - model            (positive = the model is better than N1)
  "advantage over BF_1" = BF_1 - model          (positive = the model beats BF_1)
  a fold is WON against BF_1 if the advantage is > tau = 1e-9 (harness.cmp).
  offset is a Jaccard, higher is better: "rule - N_EB" positive = the rule is better.

Usage: tools/.venv/Scripts/python.exe results/genome/c6/rules/second_rule/diagnosis.py summary
"""

import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
TAU = 1e-9
MIN_WINS = 9
E0_MAX = 0.002
O0_BAND = 0.010
DL_LIMIT = 9481.2
EXIST_MODELS = ["rule", "rule_float", "rule_mu0_float", "oracle_Wstar", "oracle_ML_W",
                "oracle_true"]
MODEL_TEXT = {
    "rule": "the registered rule (quantised), as gated",
    "rule_float": "the rule's unquantised float model (mu = 1)",
    "rule_mu0_float": "the rule's float model with X_e by plain ML (mu = 1e-6, damped Newton)",
    "oracle_Wstar": "O-W*: knows W* exactly; c, a, b (N1 ridge) and u, v (BF_1 algorithm, "
                    "nested lambda) fitted",
    "oracle_ML_W": "O-ML-W: knows the planted c, a, b, u, v exactly; W by plain ML (mu = 1e-6, "
                   "damped Newton)",
    "oracle_true": "O-true: the generating probabilities themselves"}


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def sd(x):
    x = np.asarray(x, float)
    return float(np.std(x, ddof=1)) if len(x) > 1 else float("nan")


def binom_ge(p, k=MIN_WINS, n=10):
    return float(sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1)))


def fold_table(rows):
    """Per-fold existence of every model and its advantage over BF_1, for one bank."""
    rows = sorted(rows, key=lambda r: r["fold"])
    out = {"per_fold": [], "models": {}}
    for r in rows:
        d = {"fold": r["fold"], "N1": r["N1"], "BF1": r["BF1"], "BF1_lambda": r["BF1_lambda"],
             "rule_lambda": r.get("rule_lambda"), "oracle_Wstar_lambda": r.get("oracle_Wstar_lambda"),
             "BF1_margin_over_N1": r["N1"] - r["BF1"]}
        for m in EXIST_MODELS:
            if m in r:
                d[m] = r[m]
                d[m + "_margin_over_N1"] = r["N1"] - r[m]
                d[m + "_advantage_over_BF1"] = r["BF1"] - r[m]
        out["per_fold"].append(d)
    for m in EXIST_MODELS:
        if m not in rows[0]:
            continue
        adv = [r["BF1"] - r[m] for r in rows]
        out["models"][m] = {
            "what": MODEL_TEXT[m],
            "folds_beating_BF1": int(sum(a > TAU for a in adv)),
            "passes_9_of_10": bool(sum(a > TAU for a in adv) >= MIN_WINS),
            "mean_advantage_over_BF1": float(np.mean(adv)),
            "sd_advantage_over_BF1_per_fold": sd(adv),
            "paired_t": float(np.mean(adv) / (sd(adv) / math.sqrt(len(adv)))),
            "min_advantage": float(min(adv)), "worst_fold": int(rows[int(np.argmin(adv))]["fold"]),
            "mean_margin_over_N1": float(np.mean([r["N1"] - r[m] for r in rows]))}
    out["BF1_mean_margin_over_N1"] = float(np.mean([r["N1"] - r["BF1"] for r in rows]))
    return out


def by_bank(rows, keys):
    out = {}
    for r in rows:
        out.setdefault(tuple(r[k] for k in keys), []).append(r)
    return out


def power(rows):
    res = {}
    for st in sorted({r["strength"] for r in rows}):
        banks = by_bank([r for r in rows if r["strength"] == st], ["seed"])
        crashed = {k[0]: [r["fold"] for r in v if "rule_crashed" in r] for k, v in banks.items()}
        crashed = {k: v for k, v in crashed.items() if v}
        banks = {k: v for k, v in banks.items() if k[0] not in crashed}
        blk = {"n_banks": len(banks), "banks_excluded_rule_crashed": crashed, "models": {}}
        for m in EXIST_MODELS:
            wins, means, sds, ts = [], [], [], []
            for rr in banks.values():
                adv = [r["BF1"] - r[m] for r in rr]
                wins.append(sum(a > TAU for a in adv))
                means.append(np.mean(adv))
                sds.append(sd(adv))
                ts.append(np.mean(adv) / (sd(adv) / math.sqrt(10)))
            wins = np.array(wins)
            p_fold = float(np.mean(wins) / 10)
            blk["models"][m] = {
                "what": MODEL_TEXT[m],
                "pass_rate_9_of_10": float(np.mean(wins >= MIN_WINS)),
                "wins_distribution": {str(k): int(np.sum(wins == k)) for k in range(11)},
                "pass_rate_at_least": {str(k): float(np.mean(wins >= k)) for k in range(6, 11)},
                "per_fold_win_rate": p_fold,
                "binomial_P_ge_9_at_that_rate": binom_ge(p_fold),
                "mean_advantage_over_BF1": float(np.mean(means)),
                "sd_of_bank_mean_advantage": sd(means),
                "mean_within_bank_sd_per_fold": float(np.mean(sds)),
                "pass_rate_paired_t_gt_2": float(np.mean(np.array(ts) > 2)),
                "pass_rate_mean_advantage_gt_0": float(np.mean(np.array(means) > TAU)),
                "pass_rate_mean_advantage_gt_tie_band_0.002": float(np.mean(np.array(means) > E0_MAX)),
                "bank_mean_advantage_min": float(np.min(means)),
                "bank_mean_advantage_quantiles_5_50_95": [float(q) for q in
                                                          np.quantile(means, [0.05, 0.5, 0.95])]}
        # the rule's lambda: 10, 30 and 100 all switch the rank-1 term off (see the lambda sweep)
        lam = np.array([r["rule_lambda"] for rr in banks.values() for r in rr])
        lamb = np.array([r["BF1_lambda"] for rr in banks.values() for r in rr])
        blk["rule_lambda_share"] = {str(l): float(np.mean(lam == l)) for l in (1, 3, 10, 30, 100)}
        blk["BF1_lambda_share"] = {str(l): float(np.mean(lamb == l)) for l in (1, 3, 10, 30, 100)}
        blk["BF1_mean_margin_over_N1"] = float(np.mean([r["N1"] - r["BF1"] for rr in banks.values()
                                                        for r in rr]))
        blk["rule_mean_margin_over_N1"] = float(np.mean([r["N1"] - r["rule"] for rr in banks.values()
                                                         for r in rr]))
        ow = [sum(r["offset_rule"] - r["offset_N_EB"] > TAU for r in rr) for rr in banks.values()]
        blk["G_o_plus"] = {"pass_rate_9_of_10": float(np.mean(np.array(ow) >= MIN_WINS)),
                           "min_wins": int(min(ow)),
                           "mean_rule_minus_N_EB": float(np.mean([r["offset_rule"] - r["offset_N_EB"]
                                                                  for rr in banks.values()
                                                                  for r in rr]))}
        allr = [r for rr in banks.values() for r in rr]
        blk["n_rows"] = len(allr)
        blk["n_nonempty_mean"] = float(np.mean([sum(r["n_heldout_ne"] for r in rr)
                                                for rr in banks.values()]))
        res[f"Wstar_x{st:g}"] = blk
    return res


def gb0_bank_summary(rr):
    """G-e0 and G-o0 quantities of one GB0-type bank (10 folds)."""
    rr = sorted(rr, key=lambda r: r["fold"])
    reg = [r["caps"][0] for r in rr]                       # the registered caps (32, 800, 48)
    neb = np.array([r["offset_N_EB"] for r in rr])
    neb_ra = np.array([r["offset_N_EB_at_rule_alpha"] for r in rr])
    src = np.array([c["source_side_only"] for c in reg])
    rule = np.array([c["rule"] for c in reg])
    out = {
        "G_e0_rule_minus_BF1_margin": float(np.mean([r["BF1"] - r["rule"] for r in rr])),
        "G_e0_float_minus_BF1_margin": float(np.mean([r["BF1"] - r["rule_float"] for r in rr])),
        "G_e0_rule_wins_vs_BF1": int(sum(r["BF1"] - r["rule"] > TAU for r in rr)),
        "G_e0_rule_adv_sd_per_fold": sd([r["BF1"] - r["rule"] for r in rr]),
        "N_EB_mean": float(neb.mean()),
        "G_o0_rule_minus_N_EB": float((rule - neb).mean()),
        "G_o0_rule_minus_N_EB_sd_per_fold": sd(rule - neb),
        "part_alpha_choice": float((neb_ra - neb).mean()),
        "part_library_restriction": float((src - neb_ra).mean()),
        "part_side_switch": float((rule - src).mean()),
        "N_EB_equivalent_minus_N_EB": float((neb_ra - neb).mean()),
        "N_EB_equivalent_minus_N_EB_sd_per_fold": sd(neb_ra - neb),
        "heldout_sets_in_library": float(np.mean([c["heldout_sets_in_library"] for c in reg])),
        "heldout_cells_on_target_side": float(np.mean([c["heldout_cells_on_target_side"]
                                                       for c in reg])),
        "library_sets_range": [min(c["n_sets"] for c in reg), max(c["n_sets"] for c in reg)],
        "caps": []}
    for j in range(len(rr[0]["caps"])):
        cs = [r["caps"][j] for r in rr]
        dl = [dl_estimate(c["n_sets"], c["n_offsets"], c["library_bits"]) for c in cs]
        out["caps"].append({
            "cap_sets": cs[0]["cap_sets"], "cap_bits": cs[0]["cap_bits"],
            "cap_offsets": cs[0]["cap_offsets"],
            "rule_minus_N_EB": float(np.mean([c["rule"] for c in cs]) - neb.mean()),
            "source_side_minus_N_EB": float(np.mean([c["source_side_only"] for c in cs]) - neb.mean()),
            "n_sets_max": max(c["n_sets"] for c in cs), "n_offsets_max": max(c["n_offsets"] for c in cs),
            "library_bits_max": max(c["library_bits"] for c in cs), "dl_estimate_max": max(dl),
            "heldout_sets_in_library": float(np.mean([c["heldout_sets_in_library"] for c in cs]))})
    return out


def dl_estimate(n_sets, n_offsets, library_bits):
    import diagnosis
    return diagnosis.dl_estimate(n_sets, n_offsets, library_bits)


def gb0(rows):
    banks = by_bank(rows, ["seed"])
    per = {str(k[0]): gb0_bank_summary(v) for k, v in banks.items()}
    vals = list(per.values())

    def col(k):
        return np.array([v[k] for v in vals])

    e0 = col("G_e0_rule_minus_BF1_margin")
    o0 = col("G_o0_rule_minus_N_EB")
    neq = col("N_EB_equivalent_minus_N_EB")
    out = {"n_banks": len(vals),
           "G_e0": {"pass_rate": float(np.mean(e0 <= E0_MAX)), "mean": float(e0.mean()),
                    "sd_across_banks": sd(e0), "max": float(e0.max()),
                    "float_model_mean": float(col("G_e0_float_minus_BF1_margin").mean()),
                    "rule_pass_rate_of_G_e_plus_criterion_on_null": float(np.mean(
                        col("G_e0_rule_wins_vs_BF1") >= MIN_WINS)),
                    "rule_pass_rate_of_8_of_10_on_null": float(np.mean(
                        col("G_e0_rule_wins_vs_BF1") >= 8)),
                    "rule_pass_rate_of_mean_advantage_gt_tie_band_on_null": float(np.mean(
                        e0 > E0_MAX)),
                    "rule_wins_vs_BF1_distribution_on_null": {
                        str(k): int(np.sum(col("G_e0_rule_wins_vs_BF1") == k)) for k in range(11)}},
           "G_o0": {"pass_rate": float(np.mean(np.abs(o0) <= O0_BAND)), "mean": float(o0.mean()),
                    "sd_across_banks": sd(o0), "min": float(o0.min()), "max": float(o0.max()),
                    "parts_mean": {k: float(col(k).mean()) for k in
                                   ("part_alpha_choice", "part_library_restriction",
                                    "part_side_switch")},
                    "parts_sd_across_banks": {k: sd(col(k)) for k in
                                              ("part_alpha_choice", "part_library_restriction",
                                               "part_side_switch")},
                    "heldout_sets_in_library_mean": float(col("heldout_sets_in_library").mean()),
                    "heldout_cells_on_target_side_mean": float(
                        col("heldout_cells_on_target_side").mean())},
           "N_EB_noise": {
               "N_EB_mean_jaccard_mean": float(col("N_EB_mean").mean()),
               "N_EB_mean_jaccard_sd_across_banks": sd(col("N_EB_mean")),
               "N_EB_equivalent_minus_N_EB_mean": float(neq.mean()),
               "N_EB_equivalent_minus_N_EB_sd_across_banks": sd(neq),
               "N_EB_equivalent_minus_N_EB_abs_max": float(np.abs(neq).max()),
               "N_EB_equivalent_within_band_rate": float(np.mean(np.abs(neq) <= O0_BAND)),
               "rule_minus_N_EB_sd_per_fold_mean": float(col("G_o0_rule_minus_N_EB_sd_per_fold").mean()),
               "N_EB_equivalent_sd_per_fold_mean": float(col(
                   "N_EB_equivalent_minus_N_EB_sd_per_fold").mean())},
           "caps": []}
    for j in range(len(vals[0]["caps"])):
        cs = [v["caps"][j] for v in vals]
        r = np.array([c["rule_minus_N_EB"] for c in cs])
        sside = np.array([c["source_side_minus_N_EB"] for c in cs])
        out["caps"].append({
            "cap_sets": cs[0]["cap_sets"], "cap_bits": cs[0]["cap_bits"],
            "cap_offsets": cs[0]["cap_offsets"],
            "rule_minus_N_EB_mean": float(r.mean()), "rule_minus_N_EB_min": float(r.min()),
            "G_o0_pass_rate": float(np.mean(np.abs(r) <= O0_BAND)),
            "source_side_minus_N_EB_mean": float(sside.mean()),
            "source_side_pass_rate": float(np.mean(np.abs(sside) <= O0_BAND)),
            "n_sets_max": max(c["n_sets_max"] for c in cs),
            "n_offsets_max": max(c["n_offsets_max"] for c in cs),
            "library_bits_max": max(c["library_bits_max"] for c in cs),
            "dl_estimate_max": max(c["dl_estimate_max"] for c in cs),
            "dl_fits_limit_in_every_fold": bool(max(c["dl_estimate_max"] for c in cs) <= DL_LIMIT),
            "heldout_sets_in_library_mean": float(np.mean([c["heldout_sets_in_library"]
                                                           for c in cs]))})
    return out, per


def lambda_block(lam_rows):
    out = []
    for r in sorted(lam_rows, key=lambda r: (r["bank"], r["fold"])):
        off = [l for l, v in r["rule_rms_uv_at_lambda"].items() if v < 1e-6]
        out.append({"bank": r["bank"], "fold": r["fold"], "rule_lambda": r["rule_lambda"],
                    "BF1_lambda": r["BF1_lambda"],
                    "rule_uv_switched_off_at_lambda": off,
                    "rule_heldout_at_lambda": r["rule_heldout_at_lambda"],
                    "BF1_heldout_at_lambda": r["BF1_heldout_at_lambda"],
                    "rule_inner_ll": r["rule_inner_ll"], "BF1_inner_ll": r["BF1_inner_ll"],
                    "rule_rms_uv_at_lambda": r["rule_rms_uv_at_lambda"]})
    return out


def registered_rank(gb1_reg, rows):
    """Where the registered GB1 (seed 60000) sits among the diagnostic GB1 draws at W* x 1."""
    banks = by_bank([r for r in rows if r["strength"] == 1.0], ["seed"])
    out = {}
    for m in ("rule", "oracle_Wstar"):
        means = np.array([np.mean([r["BF1"] - r[m] for r in rr]) for rr in banks.values()])
        wins = np.array([sum(r["BF1"] - r[m] > TAU for r in rr) for rr in banks.values()])
        reg = gb1_reg["models"][m]
        out[m] = {"registered_mean_advantage": reg["mean_advantage_over_BF1"],
                  "share_of_draws_with_mean_advantage_at_or_below": float(np.mean(
                      means <= reg["mean_advantage_over_BF1"])),
                  "registered_wins": reg["folds_beating_BF1"],
                  "share_of_draws_with_wins_at_or_below": float(np.mean(
                      wins <= reg["folds_beating_BF1"]))}
    bfm = np.array([np.mean([r["N1"] - r["BF1"] for r in rr]) for rr in banks.values()])
    rm = np.array([np.mean([r["N1"] - r["rule"] for r in rr]) for rr in banks.values()])
    out["BF1_margin_over_N1"] = {"registered": gb1_reg["BF1_mean_margin_over_N1"],
                                 "diagnostic_mean": float(bfm.mean()), "diagnostic_sd": sd(bfm)}
    out["rule_margin_over_N1"] = {"registered": gb1_reg["models"]["rule"]["mean_margin_over_N1"],
                                  "diagnostic_mean": float(rm.mean()), "diagnostic_sd": sd(rm)}
    return out


def worst_case_dl():
    """DL(rule) at the caps (the registered way of bounding it, proposal section 2.4) for the
    registered caps and for candidate library caps. The decoder is taken at its measured 494 bytes;
    a wider index array would need a few more bytes of decoder (not measured)."""
    import diagnosis as D
    out = []
    for sets, bits, offs in ((32, 800, 48), (32, 1100, 48), (32, 1400, 48), (32, 1600, 48),
                             (64, 1200, 64), (64, 1400, 64), (64, 1600, 64)):
        dl = D.dl_estimate(sets, offs, bits)
        out.append({"cap_sets": sets, "cap_bits": bits, "cap_offsets": offs,
                    "dl_worst_case": dl, "headroom_to_limit": round(DL_LIMIT - dl, 1)})
    return out


def main():
    import diagnosis as D
    reg = load("diagnosis_registered.json")
    gates = load("gates.json")
    per = gates["per_fold_scores_gate_banks"]
    # reproduction of the gate run
    repro = {}
    for kind in ("GB1", "GB0"):
        rows = sorted(reg[kind], key=lambda r: r["fold"])
        repro[kind] = {
            k: float(max(abs(r[k] - per[kind][g][r["fold"]]["existence"]) for r in rows))
            for k, g in (("rule", "rule"), ("BF1", "BF1"), ("N1", "N1"))}
        repro[kind]["offset_N_EB"] = float(max(abs(r["offset_N_EB"] - per[kind]["N_EB"][r["fold"]]["offset"])
                                               for r in rows))
    repro["GB1"]["offset_rule"] = float(max(abs(r["offset_rule"] - per["GB1"]["rule"][r["fold"]]["offset"])
                                            for r in reg["GB1"]))
    repro["GB0"]["offset_rule"] = float(max(abs(r["caps"][0]["rule"] - per["GB0"]["rule"][r["fold"]]["offset"])
                                            for r in reg["GB0"]))
    gb1_reg = fold_table(reg["GB1"])
    f2 = [d for d in gb1_reg["per_fold"] if d["fold"] == 2][0]
    f9 = [d for d in gb1_reg["per_fold"] if d["fold"] == 9][0]
    small_numbers = {
        "fold2_float_model_minus_BF1": f2["rule_float"] - f2["BF1"],
        "fold2_registered_rule_minus_BF1": f2["rule"] - f2["BF1"],
        "fold9_float_model_minus_BF1": f9["rule_float"] - f9["BF1"],
        "fold9_registered_rule_minus_BF1": f9["rule"] - f9["BF1"],
        "reading": "0.00008 is the unquantised float model's held-out loss minus BF_1's in GB1 "
                   "fold 2 (gate_diagnostics.json). 0.00068 is the registered (quantised) rule's "
                   "held-out loss minus BF_1's in the same fold (gates.json): the number the gate "
                   "actually judged."}
    gb0_reg_rows = reg["GB0"]
    gb0_reg = gb0_bank_summary(gb0_reg_rows)
    gb0_reg["existence"] = fold_table(gb0_reg_rows)
    pw = load("diagnosis_power_rows.json")
    g0 = load("diagnosis_gb0_rows.json")
    gb0_diag, gb0_per_bank = gb0(g0["rows"])
    out = {"what": "Aggregates of the rule #2 gate diagnosis (diagnosis.py). Synthetic banks "
                   "only. Not a gate, not a fix.",
           "sources": {"diagnosis_sha256_lf": reg["diagnosis_sha256_lf"],
                       "harness_sha256_lf": reg["harness_sha256_lf"],
                       "fit_sha256_lf": reg["fit_sha256_lf"]},
           "seed_discipline": {"registered_gate_banks": 60000,
                               "diagnostic_range": reg["diagnostic_seed_range"],
                               "diagnostic_seeds_used": [min(D.DIAG_SEEDS), max(D.DIAG_SEEDS)],
                               "reserved_for_future_regate_not_touched":
                                   reg["reserved_seed_range_not_touched"]},
           "reproduction_of_gates_json_max_abs_diff": repro,
           "registered_GB1": gb1_reg, "small_numbers": small_numbers,
           "registered_GB0": gb0_reg,
           "lambda_sweep_registered": lambda_block(reg["lambda_sweep"]),
           "power_GB1_diagnostic": power(pw["rows"]),
           "registered_GB1_within_diagnostic_x1": registered_rank(gb1_reg, pw["rows"]),
           "GB0_diagnostic": gb0_diag, "dl_worst_case_at_caps": worst_case_dl(),
           "registered_GB0_within_diagnostic": {
               "registered_rule_minus_N_EB": gb0_reg["G_o0_rule_minus_N_EB"],
               "share_of_draws_at_or_below": float(np.mean(
                   [v["G_o0_rule_minus_N_EB"] <= gb0_reg["G_o0_rule_minus_N_EB"]
                    for v in gb0_per_bank.values()])),
               "registered_G_e0": gb0_reg["G_e0_rule_minus_BF1_margin"],
               "share_of_draws_G_e0_at_or_below": float(np.mean(
                   [v["G_e0_rule_minus_BF1_margin"] <= gb0_reg["G_e0_rule_minus_BF1_margin"]
                    for v in gb0_per_bank.values()]))}, "GB0_diagnostic_per_bank": gb0_per_bank}
    (HERE / "diagnosis_summary.json").write_text(json.dumps(out, indent=1) + "\n",
                                                 encoding="utf-8", newline="\n")
    banks = [D.bank_record("GB1", 60000, 1.0), D.bank_record("GB0", 60000)]
    banks += [D.bank_record("GB1", s, st) for st in D.STRENGTHS for s in D.DIAG_SEEDS]
    banks += [D.bank_record("GB0", s) for s in D.DIAG_SEEDS]
    (HERE / "diagnosis_banks.json").write_text(json.dumps(
        {"what": "Every bank the diagnosis built. GB1-type: W* x scale and target flags on; "
                 "GB0-type: W* = 0, flags off. All from gate_banks.draws(seed).",
         "reserved_for_future_regate_not_touched": reg["reserved_seed_range_not_touched"],
         "banks": banks}, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: out[k] for k in ("reproduction_of_gates_json_max_abs_diff",
                                          "small_numbers")}, indent=1))


if __name__ == "__main__":
    main()
