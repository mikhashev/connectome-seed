"""T-X7: VX6's direct recount, and Zcode's rider on the ko1 copies (CPU only).

(i) direct_recount agrees with the comparator on unmodified records ("uninformative": no p
moved), on one-step moves, on a changed lambda and on a label flip, B's ko1 records.
(ii) A difference on a ko1 record copied from the ko fit (reused_from_ko) is found and its CPU
path check passes: the arm's own train_fixed_lambda, decoded, equals the stored copy bit for bit
(B, the first reused BF record; one CPU fit).
"""
import copy

import numpy as np

import ext_compare as XK
import ext_scope as XS

WORLDS = ["world:R:0", "world:M0.5:1", "world:W:4"]


def _run(got, ref, K):
    planned = XS.planned(WORLDS, "ko1")
    sub = {rk: got[rk] for rk in planned}
    rep = XK.compare_records(sub, ref, K, planned, scope="T-X7")
    return rep, XK.recount_agrees(rep, XK.direct_recount(sub, ref, K, planned))


def test_x7_recount(ref_B, K_B):
    ref = ref_B[0]
    rep, rc = _run(ref, ref, K_B)
    assert rc["agrees"] and rc["uninformative"]
    got = copy.deepcopy({rk: ref[rk] for rk in XS.planned(WORLDS, "ko1")})
    k1, k2, k3 = (f"{WORLDS[0]}||ko1||BF:2", f"{WORLDS[1]}||ko1||BF:3", f"{WORLDS[2]}||ko1||BF:4")
    p = np.asarray(got[k1]["p"], np.float64)
    p[7] = np.nextafter(p[7], 2.0)
    got[k1]["p"] = p.tolist()
    got[k2]["lam"] = 3.0
    q = np.asarray(got[k3]["p"], np.float64)
    i = int(np.argmin(np.abs(q - 0.5)))
    q[i] = 1.0 - q[i]
    got[k3]["p"] = q.tolist()
    rep, rc = _run(got, ref, K_B)
    assert rc["agrees"] and not rc["uninformative"]
    assert rc["direct_not_bit_equal"] == 2 and set(rc["direct_e1"]) >= {k2, k3}


def test_x7_reused_cell_path_check(ref_B):
    ref = ref_B[0]
    reused = sorted(rk for rk in XS.planned(XS.base_keys_of(ref), "ko1")
                    if ref[rk].get("reused_from_ko"))
    assert len(reused) == 29
    rk = reused[0]
    chk = XK.cpu_path_check("B", rk, ref)
    assert chk["passed"] and chk["max_abs_dp"] == 0.0
