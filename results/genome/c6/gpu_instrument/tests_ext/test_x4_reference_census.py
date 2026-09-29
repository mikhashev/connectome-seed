"""T-X4: the reference census of the plan (section X.4 of the revision 1.5 draft), reproduced from
the pinned stores; every number with its scope label.

A (64 cells) and B (40 cells), 45 base views each, 180 BF fits per mask:
  * block: lambda 1 on all 180; 180 BF-active (p differs from the block view's N1 p); 0 ties;
    smallest present x absent gap 0.7499999928 (A, world:No:0 BF:3) and 0.6547167014 (B,
    world:No:0 BF:2): no pair of S(f) within 2^-23, so no flip is possible at any |dp| below
    those gaps; the block records' only readers are ceiling_block (AUC) and lambda_block;
  * ko1: lambda 1 on all 180; 180 BF-active (p differs from the ko view's N1 p); 29 copied from
    the ko fit (reused_from_ko) in each arm; 0 ties; smallest S(f) gap 5.0399e-7 (A,
    world:M0.6:0 BF:3) and 1.6154e-6 (B, world:Nf:1 BF:2), 0 at risk.
B's registered run's synthetic store gives the same census (a fresh CPU refit, p equal).
"""
import pytest

import ext_scope as XS

EXPECT = {
    ("A", "block"): (0.7499999928382761, "world:No:0||block||BF:3", 0, 184320),
    ("B", "block"): (0.654716701428136, "world:No:0||block||BF:2", 0, 72000),
    ("A", "ko1"): (5.039887790714292e-07, "world:M0.6:0||ko1||BF:3", 29, 362880),
    ("B", "ko1"): (1.6153523991202512e-06, "world:Nf:1||ko1||BF:2", 29, 140400),
}


@pytest.mark.parametrize("arm,mask", sorted(EXPECT))
def test_x4_reference_census(arm, mask, ref_A, ref_B):
    ref = {"A": ref_A, "B": ref_B}[arm][0]
    rc = XS.reference_census(ref, mask, scope_arm=f"arm {arm}")
    gap, at, reused, denom = EXPECT[(arm, mask)]
    assert rc["n_fits"] == 180 and rc["n_cells"] == (64 if arm == "A" else 40)
    assert rc["scope"] == f"arm {arm} {mask}-mask BF_1-BF_4 fits of the 45 base views (180 fits)"
    assert rc["lambda_by_rank"] == {f"BF:{r}": {"1.0": 45} for r in (1, 2, 3, 4)}
    assert rc["bf_active"] == {"bf_active": 180, "p_equals_n1": 0, "no_n1": 0}
    assert rc["reused_from_ko"] == reused
    S = rc["census"]["families"]["S(f), every fit in scope"]
    assert S["fits_with_tie"] == 0 and S["tied_pairs"] == 0
    assert S["smallest_gap"] == gap and S["smallest_gap_at"] == at
    assert S["pairs_denominator_sum"] == denom
    assert S["fits_gap_below_band"] == 0 and rc["at_risk"] == []
    assert rc["census"]["scope"] == rc["scope"]


def test_x4_registered_equals_pinned(ref_B, ref_B_registered):
    a, b = ref_B[0], ref_B_registered[0]
    for mask in XS.EXT_MASKS:
        for rk in XS.planned(XS.base_keys_of(a), mask):
            assert a[rk]["p"] == b[rk]["p"] and a[rk]["lam"] == b[rk]["lam"], rk
        assert XS.reference_census(a, mask)["census"]["families"] == \
            XS.reference_census(b, mask)["census"]["families"]
