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
    flat = [-2.0] * 5
    up = [-2.0, -1.9, -1.8, -1.7, -1.6]            # lambda = 100 best
    down = [-1.6, -1.7, -1.8, -1.9, -2.0]          # lambda = 1 best
    # tie: all folds flat
    assert _read([(1, 1, flat), (2, 2, flat)]) == "(a) tie rule"
    # lambda = 100 wins only through the one-cell single-class fold
    assert _read([(1, 0, [-5, -4, -3, -2, -0.5]), (1, 1, down), (2, 1, down)]) == \
        "(a) fold geometry"
    # lambda = 100 wins in most two-class folds
    assert _read([(1, 0, down), (1, 1, up), (2, 1, up), (1, 2, up)]) == "(b) data"
    # lambda = 100 wins the two-class sum through one fold only
    assert _read([(1, 1, [-9, -8, -7, -6, -1]), (2, 1, down), (1, 2, down)]) == \
        "(c) carried by few folds"
    # the collapse seen on fixtures: lambda >= 3 give one fit (tied), lambda = 1 differs
    col_up = [-2.0, -1.5, -1.5, -1.5, -1.5]
    col_down = [-1.5, -2.0, -2.0, -2.0, -2.0]
    assert _read([(1, 0, col_down), (1, 1, col_up), (2, 1, col_up), (1, 2, col_up)]) == "(b) data"
    assert _read([(1, 0, [-3, -0.1, -0.1, -0.1, -0.1]), (1, 1, col_down), (2, 1, col_down)]) ==         "(a) fold geometry"
    assert _read([(1, 1, [-9, -1, -1, -1, -1]), (2, 1, col_down), (1, 2, col_down)]) ==         "(c) carried by few folds"
    # the all-fold selection is not lambda = 100
    assert _read([(1, 1, down)]) == "not applicable"


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
