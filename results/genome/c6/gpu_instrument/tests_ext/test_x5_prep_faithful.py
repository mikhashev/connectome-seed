"""T-X5: extension X's preparation and decode are the CPU's own path (numpy only, no torch).

With ext_prep's arrays, the harness's own bf_als (numpy, in this process) reproduces the pinned
CPU record bit for bit, through ext_prep.decode_records_ext:
  * ko1: one bf_als on grid 0 at lambda 1 (train_fixed_lambda), ranks 1 and 4;
  * block: fit_bf's nested lambda choice re-executed from the prepared inner-fold grids (10 folds
    x 5 lambdas, the same held-out sum and tie rule), then the final bf_als, rank 1.
So everything the GPU stage takes from the CPU (bank, view, N1, grids, folds, held-out masks, SVD
start, decode, score) is the CPU's, and a GPU run can differ from the reference only through
engine v3's bf_als arithmetic, which VX1 and VX2 measure. Arms A (64 cells) and B (40 cells),
world R:0.
"""
import numpy as np
import pytest

import prep
import ext_prep as XP
import ext_scope as XS

H = prep.H
KEY = "world:R:0"


def _init(arm):
    name = XS.ARMS[arm]
    K = prep.set_arm(name, None)
    terms = K.degree_terms()
    prep.init_arm_worker(name, None, terms)
    assert H.STARTS == 10
    return K


def _record(pp, mask, r, U, V, lam):
    data = dict(pp["n1"])
    data.update({"bf_U": U, "bf_V": V, "bf_lambda": np.array([float(lam)])})
    [(rk, rec, h)] = XP.decode_records_ext(
        (r, mask, [(pp["key"], data, pp["y_block"], pp["block_content"], pp["outside_density"])]))
    return rk, rec


def _same(rec, ref):
    assert rec["p"] == ref["p"]
    assert rec["y"] == ref["y"]
    assert rec["lam"] == ref["lam"]
    assert rec["outside_density"] == ref["outside_density"]
    for k in ("existence", "offset", "counts", "sign", "n_ne"):
        assert rec["score"][k] == ref["score"][k], k


@pytest.mark.parametrize("arm", ["A", "B"])
def test_x5_ko1(arm, ref_A, ref_B):
    ref = {"A": ref_A, "B": ref_B}[arm][0]
    _init(arm)
    pp = XP.prepare_key_ext(KEY, "ko1")
    assert pp["O"].shape == (1, 65, 65) and pp["n_folds"] == 0
    Y, M = pp["Y"].astype(np.float64), pp["M"][0].astype(np.float64)
    for r in (1, 4):
        U, V = H.bf_als(pp["O"][0], Y, M, r, XS.FIXED_LAMBDA, starts=H.STARTS)
        rk, rec = _record(pp, "ko1", r, U, V, XS.FIXED_LAMBDA)
        assert rk == f"{KEY}||ko1||BF:{r}"
        _same(rec, ref[rk])
    assert np.array_equal(pp["p_n1"], np.asarray(ref[f"{KEY}||ko||N1"]["p"], np.float64))


@pytest.mark.parametrize("arm", ["A", "B"])
def test_x5_block(arm, ref_A, ref_B):
    ref = {"A": ref_A, "B": ref_B}[arm][0]
    K = _init(arm)
    pp = XP.prepare_key_ext(KEY, "block")
    assert pp["O"].shape == (11, 65, 65) and pp["n_folds"] == 10
    assert int(pp["M"][0].sum()) == len(K.BLOCK_CELLS)     # the block view: block cells only
    Y = pp["Y"].astype(np.float64)
    r = 1
    ll = {lam: 0.0 for lam in H.BF_LAMBDAS}
    for f in range(pp["n_folds"]):
        Oi, Mi, test = pp["O"][1 + f], pp["M"][1 + f].astype(np.float64), pp["test"][1 + f]
        for lam in H.BF_LAMBDAS:
            U, V = H.bf_als(Oi, Y, Mi, r, lam)
            p = np.clip(H._sig(Oi + U @ V.T), *H.CLIP)
            ll[lam] += float(np.sum(np.where(Y > 0, np.log(p), np.log(1 - p))[test]))
    best = max(ll.values())
    lam = max(x for x in H.BF_LAMBDAS if ll[x] >= best - 1e-9)
    U, V = H.bf_als(pp["O"][0], Y, pp["M"][0].astype(np.float64), r, lam)
    rk, rec = _record(pp, "block", r, U, V, lam)
    assert rk == f"{KEY}||block||BF:1"
    _same(rec, ref[rk])
    assert np.array_equal(pp["p_n1"], np.asarray(ref[f"{KEY}||block||N1"]["p"], np.float64))
