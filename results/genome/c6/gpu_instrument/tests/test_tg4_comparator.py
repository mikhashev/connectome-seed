"""T-G4 (G9; the comparator separates both worlds): on the pinned records, an injected dp of
1.01 x s(p) on one cell that reorders no pair of S(f) passes E2 and is printed as a diagnostic; a
lambda changed on one fit fails E1; a label flipped fails E1; a D moved just beyond its E3 bound
fails E3 and one moved just within it passes; the denominators of the counts per cell read from
the pinned store are 37, 164, 4,299 and 13,500; the unmodified records pass all three.
Also: E3's table of section 5 reproduces from the pinned p; Ark's point 1 (12:09 UTC), the
BF-active classification from the pinned store alone."""
import copy

import numpy as np
import pytest

import gpu_equivalence as G
import census as C


def _summ(ents):
    return G.summarise(ents, {}, {}, {}, {"bf_active": 0}, {"label": "test"}, {}, "test")


def test_unmodified_records_pass_all_three(pinned, d1_keys):
    ents = []
    for rk in d1_keys:
        bk, mk, _ = rk.split("||")
        n1 = pinned[f"{bk}||{mk}||N1"]["p"]
        ents.append(G.compare_fit(rk, pinned[rk], pinned[rk], n1))
    rep = _summ(ents)
    assert len(ents) == 18000
    assert rep["outcome"] == 1 and rep["n_not_bit_equal"] == 0 and rep["n_flipped_pairs"] == 0
    assert [e["key"] for e in rep["at_risk"]] == [f"world:M0.85:2|sh:79||ko||BF:{r}"
                                                   for r in (1, 2, 3, 4)]
    assert all(e["p_equals_n1_ref"] for e in rep["at_risk"])


def test_denominators(pinned, d1_keys):
    _, groups = G.denominators(pinned, d1_keys)
    assert groups == {"rank 1, lambda {1, 3}, base": 37, "rank 1, lambda {1, 3}, shuffle": 164,
                      "rank 1, lambda 100": 4299, "ranks 2-4, any lambda": 13500}


def _isolated_cell(p, far):
    """A cell whose distance to every other cell exceeds `far`, away from 0.5."""
    for i in np.argsort(-np.abs(p - 0.5)):
        d = np.abs(np.delete(p, i) - p[i])
        if d.min() > far and abs(p[i] - 0.5) > far:
            return int(i)
    return None


def test_small_dp_passes_e2_and_is_a_diagnostic(pinned):
    rk = "world:R:0||ko||BF:1"                      # a base view: E3 is evaluated too
    ref = pinned[rk]
    p = np.asarray(ref["p"], np.float64)
    i = _isolated_cell(p, 1e-6)
    assert i is not None
    s = float(np.spacing(np.float32(p[i])))
    got = copy.deepcopy(ref)
    got["p"][i] = float(p[i] + 1.01 * s)
    e = G.compare_fit(rk, got, ref)
    assert e["n_flips"] == 0 and e["e1"]["passed"] and e["e3"]["passed"]
    assert not e["bit_equal"]
    assert e["diag"]["cell"] == i and e["diag"]["ratio_to_s_p"] == pytest.approx(1.01, rel=1e-6)
    assert _summ([e])["outcome"] == 1


def test_lambda_changed_fails_e1(pinned):
    rk = "world:M0.6:1|sh:5||ko||BF:3"
    got = copy.deepcopy(pinned[rk])
    got["lam"] = 30.0
    e = G.compare_fit(rk, got, pinned[rk])
    assert not e["e1"]["lam_equal"] and not e["e1"]["passed"]
    assert _summ([e])["outcome"] == 3


def test_label_flipped_fails_e1(pinned):
    rk = "world:No:2||ko||BF:2"
    got = copy.deepcopy(pinned[rk])
    p = np.asarray(got["p"])
    i = int(np.argmin(np.abs(p - 0.5)))
    got["p"][i] = 0.4999999 if p[i] >= 0.5 else 0.5
    e = G.compare_fit(rk, got, pinned[rk])
    assert e["e1"]["label_diffs"] == 1 and not e["e1"]["passed"]
    assert _summ([e])["outcome"] == 3


def test_e3_bound_just_beyond_fails_just_within_passes(pinned):
    rk = "world:M1.0:0||ko||BF:1"
    ref = pinned[rk]
    b = G.e3_bounds(ref["p"], ref["y"], 2.333e-8)
    D = G.D_of(ref["p"], ref["y"])
    ll = ref["score"]["existence"]
    assert G.e3_check(b, D, D + b["D_bound"] * (1 - 1e-9), ll, ll)["passed"]
    assert not G.e3_check(b, D, D + b["D_bound"] * (1 + 1e-9), ll, ll)["passed"]
    assert G.e3_check(b, D, D, ll, ll - b["logloss_bound"] * (1 - 1e-9))["passed"]
    assert not G.e3_check(b, D, D, ll, ll - b["logloss_bound"] * (1 + 1e-9))["passed"]
    # a bit-equal fit must be exact
    assert G.e3_check(None, D, D, ll, ll)["passed"]
    assert not G.e3_check(None, D, D + 1e-15, ll, ll)["passed"]


# Section 5's table: delta, q_min, D bound, tighter form, m_min, logloss bound.
E3_TABLE = {"world:M1.0:0||ko||BF:1": (2.333e-8, 0.0311, 1.50e-6, 3.13e-7, 0.0901, 2.59e-7),
            "world:M0.85:0||ko||BF:1": (2.937e-8, 0.0296, 1.99e-6, 4.28e-7, 0.147, 2.00e-7),
            "world:M0.75:0||ko||BF:1": (1.631e-8, 0.0617, 5.29e-7, 2.16e-7, 0.134, 1.22e-7),
            "world:M0.85:2||ko||BF:1": (5.632e-8, 0.0616, 1.83e-6, 6.52e-7, 0.171, 3.30e-7),
            "world:M1.0:4||ko||BF:1": (3.156e-8, 0.1145, 5.51e-7, 3.25e-7, 0.152, 2.08e-7)}


@pytest.mark.parametrize("rk", sorted(E3_TABLE))
def test_e3_table_reproduces(pinned, rk):
    delta, q, Db, tight, m, llb = E3_TABLE[rk]
    b = G.e3_bounds(pinned[rk]["p"], pinned[rk]["y"], delta)
    assert b["q_min"] == pytest.approx(q, rel=6e-3)
    assert b["D_bound"] == pytest.approx(Db, rel=6e-3)
    assert b["D_tighter_diagnostic"] == pytest.approx(tight, rel=6e-3)
    assert b["m_min"] == pytest.approx(m, rel=6e-3)
    assert b["logloss_bound"] == pytest.approx(llb, rel=6e-3)
    assert b["cells_clipped_by_logit_of"] == 0


def test_ark_point1_bf_active_classification(pinned, d1_keys):
    act = G.bf_active(pinned, d1_keys)
    s = G.bf_active_summary(pinned, d1_keys, act)
    assert s["bf_active"] == 359 and s["p_equals_n1"] == 17641 and s["no_n1_record"] == 0
    assert s["lambda_below_100_all_active"] is True
    assert sorted(s["active_at_lambda_100"]) == [f"world:W:4|sh:84||ko||BF:{r}" for r in (2, 3, 4)]
    assert s["lambda_below_100"] == 356


def test_ark_point2_per_fit_denominators(pinned, d1_keys):
    ents = [(rk, C.census_fit(pinned[rk]["p"], pinned[rk]["y"], *rk.split("||")[:2]))
            for rk in d1_keys]
    fam = C.family_summary(ents)
    pa = sum(int(np.sum(pinned[rk]["y"])) * (64 - int(np.sum(pinned[rk]["y"]))) for rk in d1_keys)
    assert fam["auc (pa pairs, every fit)"]["pairs_denominator_sum"] == pa
    assert pa != 1024 * 18000
    assert fam["auc_null (all pairs, base ko/ko1)"]["pairs_denominator_sum"] == 2016 * 180
