"""T-G10 (an at-risk fit with a changed AUC is listed and refused): from a pinned D1-scope fit, a
reference copy made at risk (a present cell at an absent cell's p plus 3e-8, smallest gap 3e-8 <
2^-23); a GPU copy equal to it passes and lists the fit as at risk; a GPU copy with that present
cell at the absent cell's p minus 3e-8 changes the AUC by 1 / (n_pos n_neg) and is refused by E1
and E2-II, with the at-risk list naming the fit (E2-III refuses nothing); a reference copy with
smallest gap 1.1e-7 is listed as at risk, and one with 1.3e-7 is not."""
import copy

import numpy as np
import pytest

import census as C
import gpu_equivalence as G

RK = "world:R:1|sh:7||ko||BF:2"


def _summ(ents):
    return G.summarise(ents, {}, {}, {}, {"bf_active": 0}, {"label": "test"}, {}, "test")


def _setup(pinned, gap):
    rec = pinned[RK]
    p = np.asarray(rec["p"], np.float64)
    y = np.asarray(rec["y"], bool)
    # an absent cell j whose value is isolated by more than 1e-5 from every other cell, and a
    # present cell i isolated too, so that moving i next to j creates only the one small gap
    for j in np.flatnonzero(~y):
        if np.delete(np.abs(p - p[j]), j).min() < 1e-5:
            continue
        for i in np.flatnonzero(y):
            if np.delete(np.abs(p - p[i]), i).min() < 1e-5:
                continue
            ref = copy.deepcopy(rec)
            ref["p"][int(i)] = float(p[j] + gap)
            c = C.census_fit(ref["p"], y, *RK.split("||")[:2])
            if c["gap_S"] == pytest.approx(gap, rel=1e-6) and c["pair_S"]["cells"] == [i, j]:
                return ref, int(i), int(j), y
    pytest.fail("no isolated present/absent pair in the fixture fit")


def test_at_risk_listed_and_equal_copy_passes(pinned):
    ref, i, j, y = _setup(pinned, 3e-8)
    e = G.compare_fit(RK, copy.deepcopy(ref), ref)
    rep = _summ([e])
    assert rep["outcome"] == 1
    assert [x["key"] for x in rep["at_risk"]] == [RK]
    assert rep["at_risk"][0]["auc_equal"] is True


def test_changed_auc_refused_by_e1_and_e2(pinned):
    ref, i, j, y = _setup(pinned, 3e-8)
    got = copy.deepcopy(ref)
    got["p"][i] = float(ref["p"][j] - 3e-8)
    e = G.compare_fit(RK, got, ref)
    n = int(y.sum()) * int((~y).sum())
    assert e["auc_ref"] - e["auc_got"] == pytest.approx(1.0 / n, rel=1e-12)
    assert not e["e1"]["auc_equal"] and e["n_flips"] == 1
    assert e["flips"][0]["cells"] == [i, j]
    rep = _summ([e])
    assert rep["outcome"] == 3
    assert [x["key"] for x in rep["at_risk"]] == [RK] and rep["at_risk"][0]["auc_equal"] is False


def test_band_edges(pinned):
    ref, *_ = _setup(pinned, 1.1e-7)
    assert G.compare_fit(RK, copy.deepcopy(ref), ref)["at_risk"] is True
    ref, *_ = _setup(pinned, 1.3e-7)
    assert G.compare_fit(RK, copy.deepcopy(ref), ref)["at_risk"] is False
