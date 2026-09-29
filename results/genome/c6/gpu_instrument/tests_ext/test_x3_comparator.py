"""T-X3: the comparator separates both worlds, on A's (64 cells) and B's (40 cells) pinned
block-mask and fixed-lambda records (the T-G4 / T-G9 / T-G10 pattern for extension X).

  * the unmodified records pass (outcome 1, 0 flips, every fit bit-equal);
  * a p moved by one float64 step that reorders no pair passes, and is counted as not bit-equal;
  * a lambda changed fails E1 (outcome 3); on ko1 a lambda other than 1.0 fails on both counts;
  * a label flipped fails E1;
  * on a block record, a present cell moved below an absent one changes the AUC (ceiling_block)
    and fails E1, and its flipped pairs are named;
  * on a ko1 record, a same-label tie turned into an order by one float64 step is a flipped pair
    of the all-pairs set that leaves the AUC unchanged: E2-II counts and names it (outcome 2, or
    3 if p_P_fixed_lambda1 moved with it);
  * the E3 statement is printed, never a pass or fail.
"""
import copy

import numpy as np
import pytest

import ext_compare as XK
import ext_scope as XS

WORLDS = ["world:R:0", "world:M0.5:1", "world:W:4"]


def _cmp(got, ref, K, mask, ranks=(1, 2, 3, 4)):
    planned = XS.planned(WORLDS, mask, ranks)
    sub = {rk: got[rk] for rk in planned}
    return XK.compare_records(sub, ref, K, planned, scope=f"T-X3 {mask}")


@pytest.fixture(params=["A", "B"])
def arm(request, ref_A, ref_B, K_A, K_B):
    return {"A": (ref_A[0], K_A), "B": (ref_B[0], K_B)}[request.param]


@pytest.mark.parametrize("mask", ["block", "ko1"])
def test_x3_unmodified_passes(arm, mask):
    ref, K = arm
    rep = _cmp(ref, ref, K, mask)
    assert rep["outcome"] == 1 and rep["n_flipped_pairs"] == 0 and rep["n_not_bit_equal"] == 0
    assert rep["e3"].startswith("E3 not applicable")
    assert rep["bf_active"]["bf_active"] == len(WORLDS) * 4


@pytest.mark.parametrize("mask", ["block", "ko1"])
def test_x3_one_step_no_reorder_passes(arm, mask):
    ref, K = arm
    got = copy.deepcopy({rk: ref[rk] for rk in XS.planned(WORLDS, mask)})
    rk = f"{WORLDS[0]}||{mask}||BF:2"
    p = np.asarray(got[rk]["p"], np.float64)
    order = np.argsort(p)
    i = int(order[len(order) // 2])
    q = p.copy()
    q[i] = np.nextafter(q[i], 2.0)
    import ext_census as XC
    assert XC.order_flips(q, p, got[rk]["y"], WORLDS[0], mask) == []   # no pair of S(f) moves
    got[rk]["p"] = q.tolist()
    rep = _cmp(got, ref, K, mask)
    assert rep["outcome"] == 1 and rep["n_not_bit_equal"] == 1
    assert rep["differing_fits"][0]["key"] == rk


@pytest.mark.parametrize("mask", ["block", "ko1"])
def test_x3_lambda_and_label_fail(arm, mask):
    ref, K = arm
    got = copy.deepcopy({rk: ref[rk] for rk in XS.planned(WORLDS, mask)})
    got[f"{WORLDS[1]}||{mask}||BF:1"]["lam"] = 3.0
    rep = _cmp(got, ref, K, mask)
    assert rep["outcome"] == 3 and rep["e1_failures"][0]["lam_equal"] is False
    if mask == "ko1":
        assert rep["e1_failures"][0]["lam_is_fixed"] is False
    got = copy.deepcopy({rk: ref[rk] for rk in XS.planned(WORLDS, mask)})
    rk = f"{WORLDS[2]}||{mask}||BF:3"
    p = np.asarray(got[rk]["p"], np.float64)
    i = int(np.argmin(np.abs(p - 0.5)))
    p[i] = 1.0 - p[i] if p[i] != 0.5 else 0.4
    got[rk]["p"] = p.tolist()
    rep = _cmp(got, ref, K, mask)
    assert rep["outcome"] == 3 and any(e["key"] == rk and e["label_diffs"] >= 1
                                       for e in rep["e1_failures"])


def test_x3_block_ceiling_move_is_refused(arm):
    ref, K = arm
    got = copy.deepcopy({rk: ref[rk] for rk in XS.planned(WORLDS, "block")})
    rk = f"{WORLDS[0]}||block||BF:4"
    p = np.asarray(got[rk]["p"], np.float64)
    y = np.asarray(got[rk]["y"], bool)
    lo_present = int(np.flatnonzero(y)[np.argmin(p[y])])
    hi_absent = int(np.flatnonzero(~y)[np.argmax(p[~y])])
    p[lo_present] = p[hi_absent] - 1e-3            # one present cell below the top absent one
    got[rk]["p"] = p.tolist()
    rep = _cmp(got, ref, K, "block")
    assert rep["outcome"] == 3
    f = [e for e in rep["e1_failures"] if e["key"] == rk][0]
    assert f["auc_equal"] is False
    assert rep["n_flipped_pairs"] >= 1 and rep["flipped_pairs"][0]["key"] == rk


def test_x3_ko1_same_label_tie_flip_is_counted(arm):
    ref, K = arm
    planned = XS.planned(WORLDS, "ko1")
    rk = f"{WORLDS[1]}||ko1||BF:1"
    p = np.asarray(ref[rk]["p"], np.float64)
    y = np.asarray(ref[rk]["y"], bool)
    ab = np.flatnonzero(~y)
    # the closest pair of absent cells: tie them in the reference copy
    d = np.abs(p[ab][:, None] - p[ab][None, :]) + np.eye(len(ab)) * 9
    a, b = np.unravel_index(np.argmin(d), d.shape)
    i, j = int(ab[a]), int(ab[b])
    ref2 = {k: copy.deepcopy(ref[k]) for k in planned}
    for k in list(ref):
        if k.endswith("||N1") and k.split("||")[0] in WORLDS:
            ref2[k] = ref[k]
    q = p.copy()
    q[j] = q[i]
    ref2[rk]["p"] = q.tolist()
    got = copy.deepcopy(ref2)
    g = q.copy()
    g[j] = np.nextafter(g[i], 2.0)
    got[rk]["p"] = g.tolist()
    rep = XK.compare_records({k: got[k] for k in planned}, ref2, K, planned, scope="T-X3 tie")
    assert rep["n_flipped_pairs"] == 1
    fl = rep["flipped_pairs"][0]
    assert fl["key"] == rk and sorted(fl["flips"][0]["cells"]) == sorted([i, j])
    assert fl["flips"][0]["labels"] == [False, False]
    assert rep["outcome"] in (2, 3)
    ent = [e for e in rep["per_fit"] if e["key"] == rk][0]
    assert ent["n_flips"] == 1
    aucs = [e for e in rep["e1_failures"] if e["key"] == rk]
    assert not aucs or aucs[0]["auc_equal"] is True      # the AUC never moves on this flip
