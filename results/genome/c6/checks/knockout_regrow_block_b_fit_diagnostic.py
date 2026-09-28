#!/usr/bin/env python3
"""Block B, the fit diagnostic: why rule #2.1's block-only fit chose lambda = 100.

Plan: docs/plans/2026-09-28-block-b-fit-diagnostic.md. It decides nothing about block B's label.

The registered block-only fits of rule #2.1 and BF_1 run unchanged; a recorder around the
function that makes each inner fit (fit.py's fit_uvw; harness.bf_als) keeps its logit grid, from
which the per-fold, per-lambda inner held-out log-likelihood is computed with the fit's own
expression. A refit that does not reproduce the registered one writes a stop record only.

    PYTHONUTF8=1 tools/.venv/Scripts/python.exe results/genome/c6/checks/knockout_regrow_block_b_fit_diagnostic.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
# First, as in the registered run: UTF-8 streams and one BLAS thread are set before numpy loads.
import knockout_regrow_block_b as B  # noqa: E402

import gzip  # noqa: E402
import inspect  # noqa: E402
import json  # noqa: E402
import time  # noqa: E402

import numpy as np  # noqa: E402

H = B.H
ARM = "blockB_fit_diagnostic"
STARTS = 10                                  # the registered command's --starts
TIE = 1e-9                                   # fit.py LAMBDA_TIE, harness fit_bf's tolerance
PRED_KEYS = ("rule", "BF:1")
PLAN = "docs/plans/2026-09-28-block-b-fit-diagnostic.md"
# summary.json real.rows.<key>.lambda_block / ceiling_block of the registered run
REGISTERED = {"rule": {"lambda": 100.0, "ceiling_block": 0.7744360902255639},
              "BF:1": {"lambda": 1.0, "ceiling_block": 0.9649122807017544}}
REGISTERED_RUN_DIR = B.PRIVATE_ROOT / "flyvis65_blockB_20260928T143258Z_7a10d88ec95e"
RAW_REAL = REGISTERED_RUN_DIR / "raw_fits_real.json.gz"
SUMS = ("all folds", "without the one-cell fold(s)", "without single-class folds")


# ------------------------------------------------------------------------------------------
# The recorded fit: the registered fit, unchanged, with its inner fits' logit grids kept.

def _recorder(pk, P):
    """(namespace, name, the inner-fit function, its logit) for predictor pk."""
    if pk == "rule":
        g = P.fit.__globals__
        inner, lg = g["fit_uvw"], g["logit_grid"]

        def logit(ba, out):                   # fit.py line 139
            U, V, W = out
            return lg(ba["O"], U, V, W, ba["G"], ba["x_on"])
        return g, "fit_uvw", inner, logit
    g = vars(H)

    def logit(ba, out):                       # harness.py line 724
        U, V = out
        return ba["O"] + U @ V.T
    return g, "bf_als", g["bf_als"], logit


def recorded_block_fit(pk, bank, starts=STARTS):
    """B._fit_one's block-only fit of pk on bank, with every inner-fit call recorded in order
    as (training mask, lambda, logit grid)."""
    B._w_init(starts, None, False)
    P = B._pred(pk)
    g, name, inner, logit = _recorder(pk, P)
    sig = inspect.signature(inner)
    calls = []

    def rec(*args, **kwargs):
        out = inner(*args, **kwargs)
        ba = sig.bind(*args, **kwargs)
        ba.apply_defaults()
        ba = ba.arguments
        calls.append({"M": np.array(ba["M"], copy=True), "lam": float(ba["lam"]),
                      "z": np.array(logit(ba, out), copy=True),
                      "uv_max": float(np.max(np.abs(out[0] @ out[1].T)))})
        return out

    g[name] = rec
    try:
        data = P.train(bank, B.MASKS["block"])
    finally:
        g[name] = inner
    p = np.asarray(P.decode(data, B.BLOCK_CELLS)["p_exist"], np.float64)
    y = bank.exists[B.BLOCK_CELLS[:, 0], B.BLOCK_CELLS[:, 1]].astype(bool)
    rule = pk == "rule"
    return {"pk": pk, "lam": B._lambda_of(pk, P, data), "p": p, "y": y,
            "ceiling_block": B.auc(p, y), "calls": calls,
            "inner_ll": dict(P.fit.__globals__["LAST_FIT"]["inner_ll"]) if rule else None,
            "grid": [float(x) for x in (P.fit.__globals__["LAMBDAS"] if rule else H.BF_LAMBDAS)]}


# ------------------------------------------------------------------------------------------
# The per-fold table and the selection.

def select(ll, grid):
    """fit.py line 142 / harness.py line 728: argmax, ties within 1e-9 to the larger lambda.
    Returns (selected, the lambdas within 1e-9 of the best)."""
    best = max(ll[l] for l in grid)
    tied = [l for l in grid if ll[l] >= best - TIE]
    return max(tied), tied


def per_fold_table(fit, bank):
    """Each recorded call matched to its fold by its training mask; the held-out log-likelihood
    per fold and lambda as fit.py lines 139-140 compute it; totals summed in the fit's order."""
    view = H.make_view(bank, B.MASKS["block"])
    inner = H.inner_folds(view)
    folds = sorted(set(inner.tolist()))
    M_full, Y = H._grid(view)
    grid, calls = fit["grid"], fit["calls"]
    if len(calls) != len(folds) * len(grid) + 1:
        raise RuntimeError(f"{len(calls)} inner calls, expected {len(folds) * len(grid) + 1}")
    rows, tot = [], {l: 0.0 for l in grid}
    for i, f in enumerate(folds):
        keep = inner != f
        Mi, _ = H._grid(H.subview(view, keep))
        test = np.zeros((65, 65), bool)
        hc = view.cells[~keep]
        test[hc[:, 0], hc[:, 1]] = True
        yf = Y[test] > 0
        row = {"fold": int(f), "n_cells": int(test.sum()), "n_present": int(yf.sum()),
               "n_absent": int((~yf).sum()), "ll": {}, "p_test": {}, "clipped": {}, "uv_max": {},
               "cells": hc.tolist()}
        row["single_class"] = row["n_present"] == 0 or row["n_absent"] == 0
        for j, lam in enumerate(grid):
            c = calls[i * len(grid) + j]
            if c["lam"] != lam or not np.array_equal(c["M"], Mi):
                raise RuntimeError(f"inner call {i * len(grid) + j} is not fold {f}, lambda {lam}")
            raw = H._sig(c["z"])
            p = np.clip(raw, *H.CLIP)
            v = float(np.sum(np.where(Y > 0, np.log(p), np.log(1 - p))[test]))
            row["ll"][lam] = v
            row["p_test"][lam] = p[test].tolist()
            row["uv_max"][lam] = c["uv_max"]
            row["clipped"][lam] = int(np.sum((raw[test] <= H.CLIP[0]) | (raw[test] >= H.CLIP[1])))
            tot[lam] += v
        row["selected"], row["tied"] = select(row["ll"], grid)
        rows.append(row)
    last = calls[-1]
    if not np.array_equal(last["M"], M_full) or last["lam"] != fit["lam"]:
        raise RuntimeError("the final call is not the full-view fit at the selected lambda")
    return {"folds": rows, "totals": tot, "grid": grid}


def sums_without(table, drop):
    """Per-lambda totals over the folds not in drop: a re-sum, not a refit."""
    tot = {l: 0.0 for l in table["grid"]}
    for r in table["folds"]:
        if r["fold"] not in drop:
            for l in table["grid"]:
                tot[l] += r["ll"][l]
    return tot


def summarise(table):
    grid = table["grid"]
    top = max(grid)
    single = [r["fold"] for r in table["folds"] if r["single_class"]]
    one_cell = [r["fold"] for r in table["folds"] if r["n_cells"] == 1]
    out = {}
    for name, drop in zip(SUMS, ([], one_cell, single)):
        tot = sums_without(table, set(drop))
        sel, tied = select(tot, grid)
        rest = [l for l in grid if l not in tied]
        out[name] = {"dropped": drop, "totals": tot, "selected": sel, "tied": tied,
                     "tie_rule_acted": len(tied) > 1,
                     "margin_top_over_rest": tot[top] - max(tot[l] for l in grid if l != top),
                     "margin_tied_over_rest": (min(tot[l] for l in tied)
                                               - max(tot[l] for l in rest)) if rest else None}
    two = [r for r in table["folds"] if not r["single_class"]]
    out["two_class_folds"] = len(two)
    out["two_class_folds_choosing_top"] = sum(r["selected"] == top for r in two)
    out["two_class_folds_by_choice"] = {l: [r["fold"] for r in two if r["selected"] == l]
                                        for l in grid}
    return out


def read_outcome(s, table):
    """The plan's reading rules, in the plan's order. T is the set of lambdas within 1e-9 of the
    best all-fold total (the tie rule picks max T); the contest is T against the other lambdas."""
    grid = table["grid"]
    top, low = max(grid), min(grid)
    a = s["all folds"]
    T = a["tied"]
    if a["selected"] != top:
        return "not applicable", f"the all-fold selection is {a['selected']:g}, not {top:g}"
    same = all(abs(r["ll"][l] - r["ll"][top]) <= TIE for r in table["folds"] for l in T)
    tset = (f"T = {T} (the same held-out value in every fold within 1e-9: {same}; "
            f"max |u.v| in T: {max(r['uv_max'][l] for r in table['folds'] for l in T):.3g})")
    if low in T:
        return "(a) tie rule", f"lambda = {low:g} is tied with {top:g}; {tset}"
    t = s["without single-class folds"]
    if not set(t["tied"]) <= set(T):
        return "(a) fold geometry", (f"without the single-class fold(s) {t['dropped']} the best "
                                     f"is {t['tied']}, outside T; {tset}")
    two = [r for r in table["folds"] if not r["single_class"]]
    k = sum(set(r["tied"]) <= set(T) for r in two)
    why = (f"T wins the two-class sum by {t['margin_tied_over_rest']:.6g} nats and is the "
           f"choice of {k} of {len(two)} two-class folds; {tset}")
    if 2 * k > len(two):
        return "(b) data", why
    return "(c) carried by few folds", why


# ------------------------------------------------------------------------------------------
# Reproduction against the registered run.

def stored_record(pk):
    """The registered run's raw record real||block||<pk>, read-only; None if the file is absent."""
    if not RAW_REAL.is_file():
        return None
    with gzip.open(RAW_REAL, "rt", encoding="utf-8") as fh:
        return json.load(fh).get(f"real||block||{pk}")


def reproduction(fit, table, registered, stored):
    """The failures (empty when the refit is the registered fit)."""
    bad = []
    sel, _ = select(table["totals"], table["grid"])
    if sel != fit["lam"]:
        bad.append(f"selection from the per-fold sums {sel} != the fit's lambda {fit['lam']}")
    if fit["inner_ll"] is not None:
        mine = {float(k): v for k, v in table["totals"].items()}
        theirs = {float(k): v for k, v in fit["inner_ll"].items()}
        if mine != theirs:
            bad.append(f"per-fold sums {mine} != the fit's inner_ll {theirs}")
    if fit["lam"] != registered["lambda"]:
        bad.append(f"lambda {fit['lam']} != registered {registered['lambda']}")
    if fit["ceiling_block"] != registered["ceiling_block"]:
        bad.append(f"ceiling_block {fit['ceiling_block']!r} != registered "
                   f"{registered['ceiling_block']!r}")
    if stored is not None:
        d = float(np.max(np.abs(fit["p"] - np.asarray(stored["p"], np.float64))))
        if d != 0.0 or stored.get("lam") != fit["lam"]:
            bad.append(f"stored record: max |p - p_stored| = {d!r}, lam {stored.get('lam')}")
    return bad


# ------------------------------------------------------------------------------------------
# Output.

def out_dir_refusal(out):
    """A new folder, outside the repository, the registered run's folder and every reference."""
    t = Path(out).resolve()
    for g in [B.ROOT, REGISTERED_RUN_DIR] + [d for _, d, _ in B.protected_references()]:
        g = Path(g).resolve()
        if t == g or t.is_relative_to(g):
            return f"REFUSED: {t} is at or inside {g}"
    if t.exists():
        return f"REFUSED: {t} exists; the diagnostic writes a new folder"
    return None


def fmt_table(pk, table, s):
    grid = table["grid"]
    lines = [f"{B.PRED_NAME[pk]}: inner held-out log-likelihood (nats) by fold and lambda",
             "fold  cells  pres  abs  " + "  ".join(f"{l:>11g}" for l in grid)
             + "  choice  clipped@choice"]
    for r in table["folds"]:
        lines.append(f"{r['fold']:>4}  {r['n_cells']:>5}  {r['n_present']:>4}  {r['n_absent']:>3}  "
                     + "  ".join(f"{r['ll'][l]:>11.6f}" for l in grid)
                     + f"  {r['selected']:>6g}{' tie' if len(r['tied']) > 1 else ''}"
                     + f"  {r['clipped'][r['selected']]}"
                     + ("  single-class" if r["single_class"] else ""))
    for name in SUMS:
        x = s[name]
        lines.append(f"{name:<30} " + "  ".join(f"{x['totals'][l]:>11.6f}" for l in grid)
                     + f"  -> {x['selected']:g} (within 1e-9: {x['tied']}; their worst minus "
                     f"the best other = {x['margin_tied_over_rest']})")
    lines.append(f"two-class folds by choice: {s['two_class_folds_by_choice']}")
    return lines


def main():
    t0 = time.time()
    B.refuse_if_dirty(False)
    checks = B.check_pins()
    head = B.git("rev-parse", "HEAD")
    out = B.private_run_dir(ARM, head)
    why = out_dir_refusal(out)
    if why:
        sys.exit(why)
    bank = B.real_bank()
    B.log(f"block B fit diagnostic at {head[:12]}; plan {PLAN}; k = {STARTS}; output {out}")
    fits, tables, summ, repro = {}, {}, {}, {}
    for pk in PRED_KEYS:
        t = time.time()
        fits[pk] = recorded_block_fit(pk, bank)
        tables[pk] = per_fold_table(fits[pk], bank)
        summ[pk] = summarise(tables[pk])
        repro[pk] = reproduction(fits[pk], tables[pk], REGISTERED[pk], stored_record(pk))
        B.log(f"{B.PRED_NAME[pk]}: refit in {time.time() - t:.1f}s; lambda {fits[pk]['lam']}, "
              f"ceiling_block {fits[pk]['ceiling_block']!r}; reproduction "
              f"{'passed' if not repro[pk] else 'FAILED'}")
    out.mkdir(parents=True, exist_ok=False)
    failed = {pk: v for pk, v in repro.items() if v}
    manifest = {"git_head": head, "plan": PLAN, "script_sha256_lf": B.sha256_lf(Path(__file__)),
                "starts": STARTS, "checks": checks, "registered": REGISTERED,
                "stored_record_file": str(RAW_REAL) if RAW_REAL.is_file() else None}
    if failed:
        rec = {"manifest": manifest, "stop": "reproduction failed; nothing is read",
               "failures": failed,
               "refit": {pk: {"lambda": fits[pk]["lam"],
                              "ceiling_block": fits[pk]["ceiling_block"]} for pk in PRED_KEYS}}
        (out / "STOP.json").write_text(B.dump_json(rec) + "\n", encoding="utf-8", newline="\n")
        B.log("STOP: the refit does not reproduce the registered fit; no table is written. "
              + json.dumps(failed))
        B.write_sha256sums(out)
        return 1
    lines = []
    for pk in PRED_KEYS:
        lines += fmt_table(pk, tables[pk], summ[pk]) + [""]
    label, why = read_outcome(summ["rule"], tables["rule"])
    lines += [f"reading (plan, rule #2.1 only): {label}: {why}",
              "block B's label is unchanged (U, failed fit)"]
    for ln in lines:
        B.log(ln)
    res = {"manifest": manifest,
           "fits": {pk: {"lambda": fits[pk]["lam"], "ceiling_block": fits[pk]["ceiling_block"],
                         "p": fits[pk]["p"].tolist(), "y": fits[pk]["y"].tolist(),
                         "inner_ll_of_the_fit": fits[pk]["inner_ll"]} for pk in PRED_KEYS},
           "tables": tables, "summary": summ,
           "reading_rule_2_1": {"outcome": label, "why": why}, "runtime_s": time.time() - t0}
    (out / "diagnostic.json").write_text(B.dump_json(res) + "\n", encoding="utf-8", newline="\n")
    (out / "console.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    B.write_sha256sums(out)
    B.log(f"written {out} in {time.time() - t0:.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
