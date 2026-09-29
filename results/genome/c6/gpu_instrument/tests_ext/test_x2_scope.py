"""T-X2: keys, masks, the output guard and the extension digest.

(i) Only base views world:<family>:<j> and only the masks block and ko1 are accepted.
(ii) The output guard refuses A's pinned folder, B's pinned pre-run folder and B's registered run
folder (and anything inside them); a scratch folder passes.
(iii) The composition identity (G18): the extension's composition axis changes with the mask,
the key order, the key set, starts and the rank order; the arm enters through the world and
script axes, never the digest (V1 and V8 L and R carry the same registered digest).
"""
import pathlib

import pytest

import instrument as I
import ext_scope as XS

KEYS = ["world:R:0", "world:R:1", "world:W:0"]


@pytest.mark.parametrize("bad", ["real", "real|sh:0", "world:R:0|sh:0", "world:R:0|pc:0",
                                 "world:R:0|leak", "world:R", "R:0", ""])
def test_x2_base_keys_only(bad):
    with pytest.raises(ValueError):
        XS.check_base_key(bad)


@pytest.mark.parametrize("bad", ["ko", "full", "ko1#hash", "cv:0"])
def test_x2_masks(bad):
    with pytest.raises(ValueError):
        XS.check_mask(bad)


def test_x2_record_keys():
    assert XS.record_key("world:M0.5:3", "block", 2) == "world:M0.5:3||block||BF:2"
    assert XS.planned(KEYS[:2], "ko1", (1, 4)) == [
        "world:R:0||ko1||BF:1", "world:R:1||ko1||BF:1",
        "world:R:0||ko1||BF:4", "world:R:1||ko1||BF:4"]


def test_x2_output_guard(K_A, K_B, tmp_path):
    for d in (pathlib.Path(K_A.PRERUN_DIR), pathlib.Path(K_B.PRERUN_DIR), XS.B_REGISTERED_DIR):
        assert XS.ext_out_dir_refusal(d) is not None
        assert XS.ext_out_dir_refusal(d / "sub") is not None
    assert XS.ext_out_dir_refusal(tmp_path / "x") is None


def test_x2_extension_identity():
    """G18 for extension X: the composition axis moves with the mask, the key order and set,
    starts and ranks, not with the arm; the arm moves the identity through its world axis (the
    degree-term digest) and its script axis (the module), each refused alone."""
    d = XS.ext_composition_digest("block", KEYS, 10, (1, 2, 3, 4))
    variants = [XS.ext_composition_digest("ko1", KEYS, 10, (1, 2, 3, 4)),
                XS.ext_composition_digest("block", KEYS[::-1], 10, (1, 2, 3, 4)),
                XS.ext_composition_digest("block", KEYS[:2], 10, (1, 2, 3, 4)),
                XS.ext_composition_digest("block", KEYS, 9, (1, 2, 3, 4)),
                XS.ext_composition_digest("block", KEYS, 10, (4, 3, 2, 1))]
    assert len({d, *variants}) == 6
    idB = XS.ext_composition_identity("block", KEYS, 10, (1, 2, 3, 4), "b" * 64,
                                      "knockout_regrow_block_b")
    idA = XS.ext_composition_identity("block", KEYS, 10, (1, 2, 3, 4), "a" * 64,
                                      "knockout_regrow")
    assert idA["composition"] == idB["composition"] == d
    assert I.check_composition_identity(idB, idB)["passed"] is True
    with pytest.raises(ValueError, match="world.*script|script.*world"):
        I.check_composition_identity(idA, idB)
    same_world = dict(idA, world=idB["world"])
    with pytest.raises(ValueError, match=r"\['script'\]"):
        I.check_composition_identity(same_world, idB)


def test_x2_registered_digest_is_arm_blind():
    """V1 (A) and V8 (male L, R) manifests carry one registered digest; recomputed here from the
    same key list (A's world_specs order, 99 shuffles, then the base views)."""
    import knockout_regrow as K
    worlds = [f"{w['family']}:{w['j']}" for w in K.world_specs()]
    keys = [f"world:{w}|sh:{sd}" for w in worlds for sd in range(99)] + \
        [f"world:{w}" for w in worlds]
    assert I.composition_digest(keys, 10, (1, 2, 3, 4)) == \
        "a6a8a0dfd445f0dcc69fe29602af50b074e4534418082d37757c4580fdd72e8e"
