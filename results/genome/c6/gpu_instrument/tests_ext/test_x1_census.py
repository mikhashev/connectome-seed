"""T-X1: ext_census is census.py on a 64-cell block, and works on B's 40-cell block.

(i) On A's pinned store (64 cells), census_fit and order_flips of ext_census return exactly what
census.py returns, on every base-view ko, ko1 and block record, on the four at-risk shuffles of
D1 and on 2,000 other shuffle records; family counts equal census.family_summary's.
(ii) On B's pinned store (40 cells), census.py cannot build the all-pairs set of a base view
(its index is the 64-cell triu), while ext_census counts 780 pairs.
"""
import numpy as np
import pytest

import census as C
import ext_census as XC

AT_RISK = [f"world:M0.85:2|sh:79||ko||BF:{r}" for r in (1, 2, 3, 4)]


def _sample(ref):
    base = [rk for rk in ref if "|" not in rk.split("||")[0]
            and rk.split("||")[1] in ("ko", "ko1", "block")]
    sh = sorted(rk for rk in ref if "|sh:" in rk)
    rng = np.random.default_rng(0)
    pick = [sh[i] for i in rng.choice(len(sh), 2000, replace=False)]
    return base + AT_RISK + pick


def test_x1_equal_to_census_on_64_cells(ref_A):
    ref, _ = ref_A
    keys = _sample(ref)
    ents_c, ents_x = [], []
    for rk in keys:
        bk, mk, _ = rk.split("||")
        p, y = ref[rk]["p"], ref[rk]["y"]
        a = C.census_fit(p, y, bk, mk, all_pairs=True)
        b = XC.census_fit(p, y, bk, mk, all_pairs=True)
        assert a == b, rk
        ents_c.append((rk, C.census_fit(p, y, bk, mk)))
        ents_x.append((rk, XC.census_fit(p, y, bk, mk)))
        # a perturbed copy: flips must be the same list
        q = np.asarray(p, np.float64).copy()
        q[3] = np.nextafter(q[3], 2.0)
        q[10] = q[11]
        assert C.order_flips(q, p, y, bk, mk) == XC.order_flips(q, p, y, bk, mk), rk
    fc = C.family_summary(ents_c)
    fx = XC.family_summary_scoped(ents_x, "T-X1 sample")["families"]
    for old, new in (("auc (pa pairs, every fit)",
                      "auc family, present x absent pairs, every fit in scope"),
                     ("auc_null (all pairs, base ko/ko1)",
                      "auc_null family, all pairs, the base-view ko/ko1 fits in scope")):
        assert fc[old] == fx[new]
    s_old = {k: v for k, v in fc["S(f)"].items() if k != "fits_gap_below_band"}
    s_new = {k: v for k, v in fx["S(f), every fit in scope"].items()
             if k != "fits_gap_below_band"}
    assert s_old == s_new
    assert XC.at_risk_list(ents_x) == C.at_risk_list(ents_c)
    assert sorted(e["key"] for e in XC.at_risk_list(ents_x)) == AT_RISK


def test_x1_forty_cells(ref_B):
    ref, _ = ref_B
    rk = "world:R:0||ko1||BF:1"
    p, y = ref[rk]["p"], ref[rk]["y"]
    assert len(p) == 40
    with pytest.raises(IndexError):
        C.census_fit(p, y, "world:R:0", "ko1")
    c = XC.census_fit(p, y, "world:R:0", "ko1")
    assert c["S"] == "all" and c["n_pairs_S"] == 780
    assert c["pa"]["n_pairs"] == int(np.sum(y)) * int(np.sum(~np.asarray(y, bool)))
    q = np.asarray(p, np.float64).copy()
    i, j = np.flatnonzero(~np.asarray(y, bool))[:2]
    q[j] = q[i]                                            # a same-label tie
    c2 = XC.census_fit(q, y, "world:R:0", "ko1")
    assert c2["tied_S"] == c["tied_S"] + 1 and c2["pa"]["tied"] == c["pa"]["tied"]
    blk = XC.census_fit(ref["world:R:0||block||BF:1"]["p"], y, "world:R:0", "block")
    assert blk["S"] == "pa"
