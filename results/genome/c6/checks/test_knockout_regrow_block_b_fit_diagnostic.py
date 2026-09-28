"""Tests of knockout_regrow_block_b_fit_diagnostic.py (plan docs/plans/2026-09-28-block-b-fit-
diagnostic.md). Fixture banks only: no test reads block B's cells of the real bank or fits on it.

Run: PYTHONUTF8=1 tools/.venv/Scripts/python.exe -m pytest -p no:cacheprovider -v
results/genome/c6/checks/test_knockout_regrow_block_b_fit_diagnostic.py
"""
import sys
from pathlib import Path

import numpy as np
import pytest

CHECKS = Path(__file__).resolve().parent
sys.path.insert(0, str(CHECKS))
import knockout_regrow_block_b_fit_diagnostic as D  # noqa: E402

B, H = D.B, D.H
FIX_TERMS = (-2.5, np.zeros(65), np.zeros(65))
FIX_STARTS = 2                               # the registered 10 would only be slower


@pytest.fixture(scope="module")
def bank():
    """A synthetic world (fixture degree terms) with its 20/20 block permuted: no real block cell."""
    w = B.make_world(B.spec_of("M0.75", 0), FIX_TERMS)
    return B.permute_block(w, np.random.default_rng(7).permutation(B.N_BLOCK), "fixture_real")


@pytest.fixture(scope="module")
def runs(bank):
    out = {}
    for pk in D.PRED_KEYS:
        fit = D.recorded_block_fit(pk, bank, starts=FIX_STARTS)
        out[pk] = (fit, D.per_fold_table(fit, bank))
    return out


@pytest.mark.parametrize("pk", D.PRED_KEYS)
def test_totals_select_the_lambda_the_fit_chose(bank, runs, pk):
    """The per-lambda totals the diagnostic prints give, under the tie rule, the lambda the
    registered fit selected; for rule #2.1 they equal the fit's own inner_ll bit for bit."""
    fit, table = runs[pk]
    sel, _ = D.select(table["totals"], table["grid"])
    assert sel == fit["lam"]
    folds = sorted(set(H.inner_folds(H.make_view(bank, B.MASKS["block"])).tolist()))
    assert [r["fold"] for r in table["folds"]] == folds
    assert sum(r["n_cells"] for r in table["folds"]) == B.N_BLOCK
    if pk == "rule":
        assert {float(k): v for k, v in fit["inner_ll"].items()} == table["totals"]
    same = {"lambda": fit["lam"], "ceiling_block": fit["ceiling_block"]}
    assert D.reproduction(fit, table, same, None) == []


@pytest.mark.parametrize("pk", D.PRED_KEYS)
def test_recording_does_not_change_the_fit(bank, runs, pk):
    """The recorder is transparent: an unrecorded fit gives the same p_exist on the 40 cells."""
    B._w_init(FIX_STARTS, None, False)
    P = B._pred(pk)
    p = np.asarray(P.decode(P.train(bank, B.MASKS["block"]), B.BLOCK_CELLS)["p_exist"])
    assert np.array_equal(p, runs[pk][0]["p"])


def test_reproduction_catches_a_changed_total_or_value(runs):
    """A table whose total differs from the fit's inner_ll, or a registered value that differs,
    fails reproduction (so the check can tell the two worlds apart)."""
    fit, table = runs["rule"]
    bad = {**table, "totals": {**table["totals"]}}
    bad["totals"][table["grid"][0]] += 1e-6
    same = {"lambda": fit["lam"], "ceiling_block": fit["ceiling_block"]}
    assert D.reproduction(fit, bad, same, None)
    assert D.reproduction(fit, table, {**same, "ceiling_block": same["ceiling_block"] - 1e-12},
                          None)
    assert D.reproduction(fit, table, same, {"p": (fit["p"] + 1e-15).tolist(), "lam": fit["lam"]})


def test_select_tie_rule():
    """The tie rule at LAMBDA_TIE / 2 (a tie) and 2 * LAMBDA_TIE (no tie)."""
    grid = [1.0, 3.0, 10.0, 30.0, 100.0]
    ll = {1.0: -10.0, 3.0: -11.0, 10.0: -12.0, 30.0: -13.0, 100.0: -10.0 - 5e-10}
    assert D.select(ll, grid) == (100.0, [1.0, 100.0])
    ll[100.0] = -10.0 - 2e-9
    assert D.select(ll, grid) == (1.0, [1.0])


def _table(rows):
    grid = [1.0, 3.0, 10.0, 30.0, 100.0]
    folds = []
    for f, (npres, nabs, ll) in enumerate(rows):
        d = dict(zip(grid, ll))
        sel, tied = D.select(d, grid)
        folds.append({"fold": f, "n_cells": npres + nabs, "n_present": npres, "n_absent": nabs,
                      "single_class": npres == 0 or nabs == 0, "ll": d, "selected": sel,
                      "tied": tied, "uv_max": {l: 0.0 for l in grid}})
    tot = D.sums_without({"folds": folds, "grid": grid}, set())
    return {"folds": folds, "grid": grid, "totals": tot}


def _read(rows):
    t = _table(rows)
    return D.read_outcome(D.summarise(t), t)[0]


def test_reading_rules_each_branch():
    """Revision 1 (E1): the reading reads the margin m = total(100) - total(1), in the plan's
    order: |m| <= LAMBDA_TIE, then m without the single-class folds, then the two-class folds."""
    flat = [-2.0] * 5
    up = [-2.0, -1.9, -1.8, -1.7, -1.6]            # lambda = 100 best
    down = [-1.6, -1.7, -1.8, -1.9, -2.0]          # lambda = 1 best
    # indifferent: all folds flat
    assert _read([(1, 1, flat), (2, 2, flat)]) == "(a) tie rule"
    # lambda = 100 wins only through the one-cell single-class fold
    assert _read([(1, 0, [-5, -4, -3, -2, -0.5]), (1, 1, down), (2, 1, down)]) ==         "(a) fold geometry"
    # lambda = 100 wins in most two-class folds
    assert _read([(1, 0, down), (1, 1, up), (2, 1, up), (1, 2, up)]) == "(b) data"
    # lambda = 100 wins the two-class sum through one fold only
    assert _read([(1, 1, [-9, -8, -7, -6, -1]), (2, 1, down), (1, 2, down)]) ==         "(c) carried by few folds"
    # the collapse seen on fixtures: lambda >= 3 give one fit (tied), lambda = 1 differs
    col_up = [-2.0, -1.5, -1.5, -1.5, -1.5]
    col_down = [-1.5, -2.0, -2.0, -2.0, -2.0]
    assert _read([(1, 0, col_down), (1, 1, col_up), (2, 1, col_up), (1, 2, col_up)]) == "(b) data"
    assert _read([(1, 0, [-3, -0.1, -0.1, -0.1, -0.1]), (1, 1, col_down), (2, 1, col_down)]) ==         "(a) fold geometry"
    assert _read([(1, 1, [-9, -1, -1, -1, -1]), (2, 1, col_down), (1, 2, col_down)]) ==         "(c) carried by few folds"
    # the all-fold selection is not lambda = 100
    assert _read([(1, 1, down)]) == "not applicable"


def test_margin_decides_not_membership():
    """A collapsed tail whose in-tail spread (1e-13) moves the argmax from 100 to 3 when the
    single-class fold is dropped (inside T): the margin over lambda = 1 stays positive, so the reading is
    (b), not (a) fold geometry; and a margin within LAMBDA_TIE is read as indifferent."""
    e = 1e-13
    single = [-3.0, -0.5, -0.5, -0.5, -0.5 + 2 * e]
    two = [-2.0, -1.5 + e, -1.5, -1.5, -1.5]
    rows = [(1, 0, single), (1, 1, two), (2, 1, two), (1, 2, two)]
    t = _table(rows)
    s = D.summarise(t)
    assert s["all folds"]["selected"] == 100.0
    w = s["without single-class folds"]
    assert max(w["totals"], key=w["totals"].get) == 3.0          # the argmax moved inside T
    assert w["tied"] == [3.0, 10.0, 30.0, 100.0]
    assert s["without single-class folds"]["margin_reading"] == "top preferred"
    assert D.read_outcome(s, t)[0] == "(b) data"
    # with a collapsed tail, margin_tied_over_rest and m agree within the tail's spread;
    # margin_top_over_rest is the spread itself, not the decision number
    a = s["all folds"]
    assert abs(a["margin_tied_over_rest"] - a["margin_top_over_low"]) <= 1e-12
    assert abs(a["margin_top_over_rest"]) <= 1e-12
    half = D.LAMBDA_TIE / 2
    assert D.margin_reading(half) == "indifferent" and D.margin_reading(-half) == "indifferent"
    assert D.margin_reading(2 * D.LAMBDA_TIE) == "top preferred"
    assert D.margin_reading(-2 * D.LAMBDA_TIE) == "lambda = 1 preferred"
    assert _read([(1, 1, [-2.0, -3, -3, -3, -2.0 - half]), (2, 1, [-2.0] * 5)]) == "(a) tie rule"


def test_leave_one_fold_out_names_the_flipping_folds():
    """Revision 1 (E5): a re-sum without each fold in turn; the fold that carries lambda = 100
    alone is named as flipping the choice, the others are not."""
    down = [-1.6, -1.7, -1.8, -1.9, -2.0]
    t = _table([(1, 1, [-9, -8, -7, -6, -1]), (2, 1, down), (1, 2, down)])
    s = D.summarise(t)
    assert [x["fold"] for x in s["leave_one_out"]] == [0, 1, 2]
    assert s["folds_flipping_choice"] == [0]
    assert s["folds_flipping_reading"] == [0]
    x0 = s["leave_one_out"][0]
    assert x0["selected"] == 1.0 and x0["margin_reading"] == "lambda = 1 preferred"
    assert x0["margin_top_over_low"] == pytest.approx(-0.8)
    assert "[0]" in D.read_outcome(s, t)[1]


def test_tail_report_and_the_predictor_sentence():
    """Revision 1 (E4): the collapsed tail by max |u.v| per lambda, and the sentence that fires
    only when rule #2.1's lambda is in its tail and BF_1's is not."""
    t = _table([(1, 1, [-2.0, -1.5, -1.5, -1.5, -1.5]), (2, 1, [-2.0, -1.5, -1.5, -1.5, -1.5])])
    for r in t["folds"]:
        r["uv_max"] = {1.0: 0.3, 3.0: 1e-14, 10.0: 0.0, 30.0: 0.0, 100.0: 0.0}
    t["final_uv_max"] = 0.0
    x = D.tail_report(t, 100.0)
    assert x["collapsed_tail"] == [3.0, 10.0, 30.0, 100.0] and x["chosen_in_tail"]
    y = D.tail_report(t, 1.0)
    assert not y["chosen_in_tail"]
    assert "two model classes" in D.compare_predictors({"rule": x, "BF:1": y})[-1]
    assert "not split" in D.compare_predictors({"rule": x, "BF:1": x})[-1]


@pytest.mark.parametrize("pk", D.PRED_KEYS)
def test_tail_report_on_the_fixture_fits(runs, pk):
    fit, table = runs[pk]
    x = D.tail_report(table, fit["lam"])
    assert x["chosen_in_tail"] == (x["uv_max_folds"][fit["lam"]] <= D.UV_ZERO)
    assert x["uv_max_final"] == fit["calls"][-1]["uv_max"]


def test_tie_tolerance_carriers():
    """Revision 1 (E6): LAMBDA_TIE is fit.py's; harness.fit_bf's literal is read and equals it;
    a changed or missing literal is caught."""
    assert D.LAMBDA_TIE == D.FIT["LAMBDA_TIE"] == 1e-9
    assert D.harness_tie_literal() == D.LAMBDA_TIE
    line = "    lam = max(l for l in BF_LAMBDAS if ll[l] >= best - {})"
    assert D.harness_tie_literal(line.format("1e-12")) == 1e-12
    with pytest.raises(RuntimeError):
        D.harness_tie_literal("    lam = max(BF_LAMBDAS)")


def test_out_dir_refusal():
    assert D.out_dir_refusal(D.REGISTERED_RUN_DIR / "x")
    assert D.out_dir_refusal(B.ROOT / "results" / "x")
    assert D.out_dir_refusal(B.PRERUN_DIR)
    assert D.out_dir_refusal(B.PRIVATE_ROOT / "blockB_fit_diagnostic_test_never_made") is None


def test_dirty_tree_refused_before_any_fit(monkeypatch):
    monkeypatch.setattr(B, "tree_state", lambda: " M results/genome/c6/harness.py")
    monkeypatch.setattr(B, "real_bank", lambda: pytest.fail("the real bank was read"))
    with pytest.raises(SystemExit):
        D.main()


def test_console_lines_on_the_fixture_fits(runs):
    """The printing path (tables, leave-one-fold-out lines, the predictor sentence) runs on the
    fixture fits; a smoke test of main's output code, not of its values."""
    tails = {}
    for pk in D.PRED_KEYS:
        fit, table = runs[pk]
        s = D.summarise(table)
        lines = D.fmt_table(pk, table, s)
        assert sum(ln.startswith("without fold") for ln in lines) == len(table["folds"])
        tails[pk] = D.tail_report(table, fit["lam"])
    assert len(D.compare_predictors(tails)) == 3
    assert D.read_outcome(D.summarise(runs["rule"][1]), runs["rule"][1])[0]
