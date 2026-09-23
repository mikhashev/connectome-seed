"""Unit tests of rule #2.1 (rule #2 with fix W1), on synthetic data only: the self-test bank ST0
(gate_banks.py: GB0's construction with seed 61000) and small hand-made inputs. Nothing here
fits or scores the real bank, a real fold, the gate banks GB1/GB0 (seed 60000), a diagnostic
seed (70000-70999) or a reserved seed (80000-80999).

Adapted from ../second_rule/test_fit.py: the bank is ST0 wherever rule #2's tests used GB1 or
GB0, and the layout and DL tests follow W1's caps and its AB__sym64 array.

Run from the repository root:
    tools/.venv/Scripts/python.exe -m pytest -q results/genome/c6/rules/second_rule_v21/test_fit.py
"""

import hashlib
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]))
os.environ.pop("SECOND_RULE_SPREAD_DIR", None)

import harness as H  # noqa: E402
import fit as R  # noqa: E402
from gate_banks import gate_bank as _gate_bank  # noqa: E402

K_TEST = 2                        # starts in the tests (speed); the run uses the harness's k
_CACHE = {}


def gate_bank(name):
    """The tests may build ST0 only."""
    assert name == "ST0", name
    return _gate_bank(name)


def rule():
    return H.Predictor(R.NAME, R.PROGRAM_FILES, R.fit, rank=R.RANK)


def fitted(bank_name="ST0", fold=0):
    key = (bank_name, fold)
    if key not in _CACHE:
        b = gate_bank(bank_name)
        view = H.make_view(b, H.FOLD != fold)
        d = R.fit(view, starts=K_TEST)
        _CACHE[key] = (b, view, d, dict(R.LAST_FIT))
    return _CACHE[key]


def test_decoder_size():
    H.check_imports(R.PROGRAM_FILES)
    assert H.program_bits(R.PROGRAM_FILES) // 8 <= R.DECODE_MAX_BYTES


def test_rank_is_registered_value():
    assert R.RANK == 1
    _, _, d, _ = fitted()
    assert H.rank_of(rule(), d) == 1


def test_data_layout_and_dl():
    b, view, d, info = fitted()
    assert set(d) == {"Q__sym32", "AB__sym64", "c", "L", "e__sym8", "s"}
    n_m = info["n_library_offsets"]
    assert d["Q__sym32"].shape == (6 * 65 + 16 + n_m,) and n_m <= R.LIB_MAX_OFFSETS
    assert d["Q__sym32"].min() >= 0 and d["Q__sym32"].max() <= 31
    assert d["AB__sym64"].shape == (130,) and d["AB__sym64"].min() >= 0
    assert d["AB__sym64"].max() < info["n_library_sets"] <= R.LIB_MAX_SETS
    assert d["c"].shape == (6,) and np.all(d["c"] == d["c"].astype(np.float32))
    assert d["e__sym8"].shape == (130,) and d["e__sym8"].max() <= 7
    assert d["s"].shape == (65,) and d["s"].dtype == bool
    assert H.data_bits({"L": d["L"]}) <= R.LIB_MAX_BITS
    assert info["n_library_sets"] <= R.LIB_MAX_SETS
    assert rule().dl(d) <= R.DL_CAP_BITS < R.DL_LIMIT_BITS


def test_worst_case_array_costs_w1():
    """W1's table (README.md): Q 2,436, AB 872, c 210, L 1,400, e 466, s 91 bits at the caps,
    plus the decode program as measured (3,904 bits = 488 bytes): 9,379 bits, under 9,481.2."""
    worst = {"Q__sym32": np.zeros(6 * 65 + 16 + R.LIB_MAX_OFFSETS, np.int64),
             "AB__sym64": np.zeros(130, np.int64), "c": np.zeros(6),
             "e__sym8": np.zeros(130, np.int64), "s": np.zeros(65, bool)}
    assert [H.data_bits({k: v}) for k, v in worst.items()] == [2436, 872, 210, 466, 91]
    prog = H.program_bits(R.PROGRAM_FILES)
    assert prog == 3904
    dl = 2436 + 872 + 210 + R.LIB_MAX_BITS + 466 + 91 + prog
    assert dl == R.DL_CAP_BITS == 9379 and dl < R.DL_LIMIT_BITS


def test_decode_matches_learner():
    """The decoder reproduces the learner's quantised model on every cell."""
    b, view, d, info = fitted()
    P = rule()
    out = P.decode(d, H.ALL_CELLS)
    Q = d["Q__sym32"].astype(float) - 16
    c = d["c"].astype(np.float32).astype(float)
    a, bb, u, v = (Q[i * 65:(i + 1) * 65] / 16 * c[[1, 1, 2, 2][i]] for i in range(4))
    G = R.groups(H.TYPE_FIELDS)
    W = (Q[390:406] / 16 * c[4]).reshape(4, 4)
    s, t = H.ALL_CELLS.T
    z = c[0] + a[s] + bb[t] + u[s] * v[t] + W[G[s], G[t]]
    assert np.allclose(out["p_exist"], 1 / (1 + np.exp(-z)), atol=1e-12, rtol=0)
    # offset sets: the target's set iff f_t > e_s
    lib, i = [], 0
    L = d["L"].tolist()
    while i < len(L):
        n = L[i]
        lib.append(set(zip(L[i + 1:i + 1 + n], L[i + 1 + n:i + 1 + 2 * n])))
        i += 1 + 2 * n
    A, B = d["AB__sym64"][:65], d["AB__sym64"][65:]
    e, f = d["e__sym8"][:65], d["e__sym8"][65:]
    for k, (si, ti) in enumerate(H.ALL_CELLS.tolist()):
        want = lib[B[ti]] if f[ti] > e[si] else lib[A[si]]
        assert set(out["offsets"][k]) == want


def test_decode_reads_indices_above_31():
    """A hand-made data dict with a 64-set library: every index 0..63 decodes to its own set,
    on both sides of the switch, and the counts use m of the right offset."""
    lib = [((i // 8 - 4, i % 8 - 4),) for i in range(64)]           # 64 one-offset sets
    offs = sorted({o for s in lib for o in s})
    A = np.arange(65) % 64
    B = (63 - np.arange(65)) % 64
    e = np.full(65, 3)
    f = np.where(np.arange(65) % 2 == 0, 5, 1)                      # even targets: target side
    d = {"Q__sym32": np.concatenate([np.full(406, 16), np.arange(len(offs)) % 32]).astype(np.int64),
         "AB__sym64": np.concatenate([A, B]).astype(np.int64),
         "c": np.array([0.0, 1.0, 1.0, 1.0, 1.0, 1.0]),
         "L": R.pack_library(lib), "e__sym8": np.concatenate([e, f]).astype(np.int64),
         "s": np.ones(65, bool)}
    assert len(offs) <= R.LIB_MAX_OFFSETS
    out = rule().decode(d, H.ALL_CELLS)
    m = {o: (q % 32) / 31 for q, o in enumerate(offs)}
    for k, (si, ti) in enumerate(H.ALL_CELLS.tolist()):
        want = lib[B[ti]] if f[ti] > e[si] else lib[A[si]]
        assert set(out["offsets"][k]) == set(want)
        (o, n), = out["offsets"][k].items()
        assert abs(np.log1p(n) - m[o]) <= 1e-6


def test_sign_equals_n1_everywhere():
    """Section 1: the decoded sign is identical to N1's on every cell (by construction)."""
    b, view, d, _ = fitted()
    n1 = H.N1.decode(H.fit_n1(view), H.ALL_CELLS)
    assert np.array_equal(rule().decode(d, H.ALL_CELLS)["sign"], n1["sign"])


def test_counts_are_n1_terms_on_the_step():
    b, view, d, _ = fitted()
    n1 = H.fit_n1(view)
    out = rule().decode(d, H.ALL_CELLS)
    m = {(x, y): val for x, y, val in zip(n1["m_du"].tolist(), n1["m_dv"].tolist(),
                                          n1["m_val"].tolist())}
    # the quantisation error of m (<= max m / 62) plus alpha and beta (<= scale / 32 each)
    c = d["c"].astype(np.float32).astype(float)
    bound = c[5] / 62 + 2 * c[3] / 32 + 1e-9
    for k, (si, ti) in enumerate(H.ALL_CELLS.tolist()[:400]):
        for o, n in out["offsets"][k].items():
            exact = m[o] + n1["cnt_a"][si] + n1["cnt_b"][ti]
            assert abs(np.log1p(n) - exact) <= bound


def test_coordinate_descent_never_raises_objective():
    b, view, d, info = fitted()
    assert info["objective_descended"] <= info["objective_rounded"] + 1e-9
    assert info["objective_final"] <= info["objective_descended"] + 1e-9


def test_determinism():
    b, view, d, _ = fitted()
    d2 = R.fit(H.make_view(b, H.FOLD != 0), starts=K_TEST)
    assert set(d) == set(d2)
    for k in d:
        assert d[k].dtype == d2[k].dtype and np.array_equal(d[k], d2[k])


def test_x_off_one_round_is_harness_bf1():
    """G-bf in miniature (ST0, fold 1, k = 2): X off and one round is the harness's BF_1."""
    old = H.STARTS
    H.STARTS = K_TEST
    try:
        b = gate_bank("ST0")
        view = H.make_view(b, H.FOLD != 1)
        ex = R.fit_existence(view, K_TEST, rounds=1, x_on=False)
        bf = H.fit_bf(view, 1)
    finally:
        H.STARTS = old
    assert ex["lam"] == bf["bf_lambda"][0]
    assert np.max(np.abs(ex["U"] - bf["bf_U"])) <= 1e-9
    assert np.max(np.abs(ex["V"] - bf["bf_V"])) <= 1e-9


def test_library_caps_and_order():
    sets = [((0, 0),)] * 5 + [((0, 0), (1, 0))] * 5 + [((2, 2),)] * 3 + \
        [tuple((i, j) for i in range(4) for j in range(4))] * 2
    lib = R.library_list(sets)
    assert lib[0] == ((0, 0),) and lib[1] == ((0, 0), (1, 0))     # tie: smaller set first
    big = [tuple((i, j) for j in range(10)) for i in range(40)]      # 400 offsets in all
    lib = R.library_list(big)
    assert len({o for s in lib for o in s}) <= R.LIB_MAX_OFFSETS
    assert H.data_bits({"L": R.pack_library(lib)}) <= R.LIB_MAX_BITS
    # W1: more than 32 sets fit, and no cap is exceeded
    small = [((i % 3, j),) for i in range(3) for j in range(30)] + \
        [((0, 0), (1, j)) for j in range(20)]                        # 110 distinct sets
    lib = R.library_list(small)
    assert 32 < len(lib) <= R.LIB_MAX_SETS
    assert len({o for s in lib for o in s}) <= R.LIB_MAX_OFFSETS
    assert H.data_bits({"L": R.pack_library(lib)}) <= R.LIB_MAX_BITS


def test_caps_are_w1():
    assert (R.LIB_MAX_SETS, R.LIB_MAX_BITS, R.LIB_MAX_OFFSETS, R.AB_SYM) == (64, 1400, 64, 64)


def test_gate_bank_generator_is_rule_2s():
    """The bank generator is rule #2's gate_banks.py, byte for byte (proposal section 2.5)."""
    def h(p):
        return hashlib.sha256(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    assert h(HERE / "gate_banks.py") == h(HERE.parent / "second_rule" / "gate_banks.py")


def test_groups_from_fields():
    G = R.groups(H.TYPE_FIELDS)
    assert sorted(np.bincount(G, minlength=4).tolist()) == [2, 8, 21, 34]


def test_spread_log_one_file_per_fit(tmp_path, monkeypatch):
    b = gate_bank("ST0")
    P = rule()
    base = None
    monkeypatch.setenv(R.SPREAD_ENV, str(tmp_path / "spread"))
    old = H.STARTS
    H.STARTS = 1
    try:
        for f in (0, 1):
            d = P.train(b, H.FOLD != f)
            if base is None:
                base = d
        files = sorted(p.name for p in (tmp_path / "spread").iterdir())
        assert len(files) == 2 and all(x.startswith("ST0__") for x in files)
        monkeypatch.delenv(R.SPREAD_ENV)
        d0 = P.train(b, H.FOLD != 0)
    finally:
        H.STARTS = old
    assert len(list((tmp_path / "spread").iterdir())) == 2
    for k in d0:
        assert np.array_equal(d0[k], base[k])                       # logging changes no data
