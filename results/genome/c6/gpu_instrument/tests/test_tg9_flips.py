"""T-G9 (G9, G16; an injected flip is caught): (i) a tied present x absent pair of a D1 shuffle
moved by one float64 step: E2-II counts as many flips as that cell had ties in S(f), names each,
refuses; (ii) in a tie-free fit, a present and an absent cell adjacent in order exchanged: one
opposite order, named; (iii) in one of the 9 base views of D1 whose ties are all same-label pairs,
one member of such a tie moved by one step: the AUC is unchanged and E2-II still counts and names
the flip; (iv) a move that changes no order state: 0 flips, passes; (v) two tied present x absent
pairs of one shuffle, one turned into "present above" and one into "absent above": AUC unchanged,
E1 passes, E2-II counts both and refuses. And the census over the whole pinned store reproduces
M20 under each definition."""
import copy

import numpy as np
import pytest

import census as C
import gpu_equivalence as G


def _summ(ents):
    return G.summarise(ents, {}, {}, {}, {"bf_active": 0}, {"label": "test"}, {}, "test")


def _vals(rec):
    return np.asarray(rec["p"], np.float64), np.asarray(rec["y"], bool)


def test_i_tied_pair_moved_one_step(pinned, d1_keys):
    for rk in d1_keys:
        if "|sh:" not in rk:
            continue
        p, y = _vals(pinned[rk])
        for i in np.flatnonzero(y):
            up = np.nextafter(p[i], 1.0)
            partners = [j for j in np.flatnonzero(~y) if p[j] == p[i]]
            if partners and not np.any(p == up):
                got = copy.deepcopy(pinned[rk])
                got["p"][int(i)] = float(up)
                e = G.compare_fit(rk, got, pinned[rk])
                assert e["n_flips"] == len(partners)
                assert sorted(f["cells"][1] for f in e["flips"]) == sorted(int(j) for j in partners)
                assert all(f["state_ref"] == 0 and f["state_got"] == 1 for f in e["flips"])
                assert _summ([e])["outcome"] != 1
                return
    pytest.fail("no D1 shuffle with a tied present x absent pair found")


def test_ii_tie_free_adjacent_swap(pinned, d1_keys):
    for rk in d1_keys:
        p, y = _vals(pinned[rk])
        if len(np.unique(p)) != 64 or "|sh:" not in rk:
            continue
        o = np.argsort(p)
        for a, b in zip(o[:-1], o[1:]):
            if y[a] != y[b]:
                got = copy.deepcopy(pinned[rk])
                got["p"][int(a)], got["p"][int(b)] = float(p[b]), float(p[a])
                e = G.compare_fit(rk, got, pinned[rk])
                assert e["n_flips"] == 1
                f = e["flips"][0]
                assert set(f["cells"]) == {int(a), int(b)}
                assert f["state_ref"] == -f["state_got"] != 0
                assert _summ([e])["outcome"] != 1
                return
    pytest.fail("no tie-free D1 shuffle found")


def test_iii_same_label_flip_on_a_base_view(pinned, d1_keys):
    same_label_only = []
    for rk in d1_keys:
        if "|" in rk.split("||")[0]:
            continue
        p, y = _vals(pinned[rk])
        c = C.census_fit(p, y, *rk.split("||")[:2])
        if c["all"]["tied"] > 0 and c["pa"]["tied"] == 0:
            same_label_only.append(rk)
    assert len(same_label_only) == 9                    # M20: 41 all-pairs, 32 pa
    for rk in same_label_only:
        p, y = _vals(pinned[rk])
        for i in range(64):
            up = np.nextafter(p[i], 1.0)
            twins = [j for j in range(64) if j != i and p[j] == p[i]]
            if twins and not np.any(p == up):
                got = copy.deepcopy(pinned[rk])
                got["p"][i] = float(up)
                e = G.compare_fit(rk, got, pinned[rk])
                assert e["e1"]["auc_equal"]
                assert e["n_flips"] == len(twins) >= 1
                assert all(fl["labels"][0] == fl["labels"][1] for fl in e["flips"])
                assert _summ([e])["outcome"] == 2
                return
    pytest.fail("no movable same-label tie found")


def test_iv_no_order_change_passes(pinned):
    rk = "world:M0.5:3|sh:12||ko||BF:4"
    p, y = _vals(pinned[rk])
    i = int(np.argmax(p))
    got = copy.deepcopy(pinned[rk])
    got["p"][i] = float(np.nextafter(p[i], 1.0))       # the largest p moves up: no order change
    e = G.compare_fit(rk, got, pinned[rk])
    assert e["n_flips"] == 0 and e["e1"]["passed"]
    assert _summ([e])["outcome"] == 1


def _clean_tie_pairs(p, y):
    """Present/absent cell pairs (a, b) whose value is held by exactly these two cells, with no
    cell at one float64 step above or below."""
    out = []
    for a in np.flatnonzero(y):
        grp = np.flatnonzero(p == p[a])
        if len(grp) == 2:
            b = int(grp[grp != a][0])
            if not y[b] and not np.any(p == np.nextafter(p[a], 1.0)) \
                    and not np.any(p == np.nextafter(p[a], 0.0)):
                out.append((int(a), b))
    return out


def test_v_two_cancelling_flips(pinned, d1_keys):
    for rk in d1_keys:
        if "|sh:" not in rk:
            continue
        p, y = _vals(pinned[rk])
        pairs = _clean_tie_pairs(p, y)
        if len(pairs) >= 2:
            (a, b), (c, d) = pairs[:2]
            got = copy.deepcopy(pinned[rk])
            got["p"][a] = float(np.nextafter(p[a], 1.0))      # present above
            got["p"][c] = float(np.nextafter(p[c], 0.0))      # absent above
            e = G.compare_fit(rk, got, pinned[rk])
            assert e["auc_got"] == e["auc_ref"] and e["e1"]["passed"]
            assert e["n_flips"] == 2
            assert {tuple(f["cells"]) for f in e["flips"]} == {(a, b), (c, d)}
            rep = _summ([e])
            assert rep["outcome"] == 2 and rep["n_flipped_pairs"] == 2
            return
    pytest.fail("no D1 shuffle with two clean tied present x absent pairs")


def test_census_reproduces_m20(pinned, d1_keys):
    ent = {rk: C.census_fit(v["p"], v["y"], *rk.split("||")[:2], all_pairs=True)
           for rk, v in pinned.items()}
    assert len(ent) == 28665
    pa = [c["pa"] for c in ent.values()]
    al = [c["all"] for c in ent.values()]
    assert (sum(x["tied"] > 0 for x in pa), sum(x["tied"] for x in pa)) == (27123, 782376)
    small = [x for x in pa if x["gap"] is not None and x["gap"] < 1e-5]
    assert len(small) == 438 and sum(x["tied"] == 0 for x in small) == 32
    assert (sum(x["tied"] > 0 for x in al), sum(x["tied"] for x in al)) == (27563, 1851770)
    d1 = [ent[rk] for rk in d1_keys]
    assert (sum(c["pa"]["tied"] > 0 for c in d1), sum(c["pa"]["tied"] for c in d1)) == \
        (17604, 423777)
    assert (sum(c["all"]["tied"] > 0 for c in d1), sum(c["all"]["tied"] for c in d1)) == \
        (17617, 885354)
    assert (sum(c["tied_S"] > 0 for c in d1), sum(c["tied_S"] for c in d1)) == (17613, 424535)
    store_risk = sorted(rk for rk, c in ent.items() if c["at_risk"])
    assert len(store_risk) == 6
    assert sorted(rk for rk in d1_keys if ent[rk]["at_risk"]) == \
        [f"world:M0.85:2|sh:79||ko||BF:{r}" for r in (1, 2, 3, 4)]
    g = ent["world:M0.85:2|sh:79||ko||BF:1"]
    assert g["gap_S"] == pytest.approx(9.079e-8, rel=1e-3) and g["pair_S"]["cells"] == [50, 59]
