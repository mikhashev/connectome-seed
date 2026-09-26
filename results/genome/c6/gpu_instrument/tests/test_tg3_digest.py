"""T-G3 (R4, D5, G3): the refusal digest changes when the key order, the key set, starts or the
rank order changes, and not when row_chunk changes (which is recorded); a mismatch refuses."""
import pytest

import instrument as I

KEYS = ["world:R:0|sh:0", "world:R:0|sh:1", "world:R:0"]


def test_digest_changes_with_what_it_covers():
    d0 = I.composition_digest(KEYS, 10, (1, 2, 3, 4))
    assert I.composition_digest(list(reversed(KEYS)), 10, (1, 2, 3, 4)) != d0      # key order
    assert I.composition_digest(KEYS[:2], 10, (1, 2, 3, 4)) != d0                  # key set
    assert I.composition_digest(KEYS + ["world:R:1"], 10, (1, 2, 3, 4)) != d0
    assert I.composition_digest(KEYS, 3, (1, 2, 3, 4)) != d0                      # starts
    assert I.composition_digest(KEYS, 10, (4, 3, 2, 1)) != d0                     # rank order
    assert I.composition_digest(KEYS, 10, (1, 2, 3)) != d0
    assert I.composition_digest(list(KEYS), 10, [1, 2, 3, 4]) == d0               # same


def test_row_chunk_recorded_not_in_digest():
    a = I.composition_record(KEYS, 10, (1, 2, 3, 4), 40000, 10, 5)
    b = I.composition_record(KEYS, 10, (1, 2, 3, 4), 100000, 10, 5)
    assert a["refusal_digest"] == b["refusal_digest"]
    assert a["recorded_not_refused"]["row_chunk"] == 40000
    assert b["recorded_not_refused"]["row_chunk"] == 100000
    ca = a["recorded_not_refused"]["chunks_per_rank"]["inner"]
    assert ca["per_block"] == 4000 and ca["problems"] == 3 * 10 * 5
    assert ca["boundaries"] == [0, 150]


def test_chunk_boundaries_full_scale():
    c = I.chunk_boundaries(4500 * 10 * 5, 40000, 10)
    assert c["per_block"] == 4000 and c["boundaries"][:3] == [0, 4000, 8000]
    assert c["boundaries"][-1] == 225000 and len(c["boundaries"]) == 58
    c2 = I.chunk_boundaries(4500 * 10 * 5, 100000, 10)
    assert c2["per_block"] == 10000
    assert set(c["boundaries"][1:-1]) - set(c2["boundaries"])   # V4 (c) moves boundaries


def test_mismatch_refuses():
    d = I.composition_digest(KEYS, 10, (1, 2, 3, 4))
    assert I.check_composition(d, d)["passed"] is True
    assert I.check_composition(d, None)["passed"] is None
    with pytest.raises(ValueError, match="REFUSED"):
        I.check_composition(d, I.composition_digest(KEYS[::-1], 10, (1, 2, 3, 4)))
