"""Tests of natural_fit_failure_replication.py (registration
docs/plans/2026-09-29-natural-fit-failure-replication-registration.md, rev 1.1, section 8).

No test fits a fresh board. Flows use stand-in fits and certs on the calibration's SEEN boards
(--fixture); the few real fits are on seen boards. Every refusal test runs under the tripwire.

Run: PYTHONUTF8=1 timeout 200 tools/.venv/Scripts/python.exe -m pytest
results/genome/c6/checks/test_natural_fit_failure_replication.py -q
"""
import csv
import hashlib
import json
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

CHECKS = Path(__file__).resolve().parent
sys.path.insert(0, str(CHECKS))
import natural_fit_failure_replication as R  # noqa: E402

C, K, H = R.C, R.K, R.H
PY = sys.executable
Z = K.board_y("z")
CAL_OUT = CHECKS / "failed_fit_calibration"
PREDICTION_COMMIT = "b5513e3fd50c32caf9a1a30c01f6fb4423d4fa7b"


# ------------------------------------------------------------------------------------------
# The tripwire: no refusal test may fit, search or open a pool, in this process or a worker.

def tripwire(mp):
    def no(*a, **k):
        raise AssertionError("tripwire: a fit, a search, a pool or the run body was reached")

    class NoPool:
        def __init__(self, *a, **k):
            raise AssertionError("tripwire: a process pool was opened")
    for mod, names in (
            (R, ("fit_task", "cert_task", "cert_fresh", "run_pool", "_run", "_rw_group",
                 "_rw_init", "estimate")),
            (C, ("fit_task", "cert_task", "cert_search", "run_groups", "_run", "_cw_group",
                 "_cw_init", "separator_fits", "bf_block_lambda1", "forced_block_fit")),
            (K, ("_fit_one", "degree_terms", "run_groups", "_w_group"))):
        for n in names:
            mp.setattr(mod, n, no)
    for mod in (R, C, K, H):
        if hasattr(mod, "ProcessPoolExecutor"):
            mp.setattr(mod, "ProcessPoolExecutor", NoPool)


def test_tripwire_catches_an_unrefused_run(tmp_path, monkeypatch):
    """The tripwire is live: a fixture run that nothing refuses hits it."""
    tripwire(monkeypatch)
    monkeypatch.setattr(K, "tree_state", lambda: "")
    with pytest.raises(AssertionError, match="tripwire"):
        R.main(FLOW_ARGS + ["--out", str(tmp_path / "run")])
    with pytest.raises(AssertionError, match="tripwire"):
        R.run_pool([[("seen:0", "cert", "cert")]], 2, (10, C.CERT_BUDGET_TINY), "x")


# ------------------------------------------------------------------------------------------
# Stand-ins.

def low_block_p(y, m=4):
    y = np.asarray(y, bool)
    p = np.zeros(len(y))
    p[np.flatnonzero(y)[:m]] = 1.0
    return p


def make_fake(fail_js=(1,), overrides=None):
    """Rule #2.1 fails (240/400 at lambda 100, ceil_1 = 1) on boards fail_js, passes (lambda 1)
    elsewhere; BF passes; N1 is constant. overrides: {(j, field): fn(y)} on the sep record."""
    ov = overrides or {}

    def fake(bk, mk, pk, bank):
        y = bank.exists[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]]
        j = R.key_j(bk)
        fail = j in fail_js
        yf = y.astype(float)
        if mk == "sep":
            reg = low_block_p(y) if fail else yf
            out = {"grid": [1, 3, 10, 30, 100], "lambda_c": 100.0 if fail else 1.0,
                   "reg_p": reg.tolist(), "reg_float_p": reg.tolist(), "ceil1_p": yf.tolist(),
                   "ceil1_float_p": yf.tolist(), "ceil1_s100_p": yf.tolist(),
                   "ceil1_s100_float_p": yf.tolist(), "y": y.tolist(), "secs": 0.0}
            for (oj, field), fn in ov.items():
                if oj == j:
                    out[field] = fn(y)
            return out
        if mk == "blk1":
            return {"p": yf.tolist(), "lam": 1.0, "y": y.tolist(), "secs": 0.0}
        if pk == "rule":
            return {"p": (low_block_p(y) if fail else yf).tolist(), "lam": 100.0 if fail else 1.0,
                    "y": y.tolist(), "secs": 0.0}
        if pk == "N1":
            return {"p": [0.5] * K.N_BLOCK, "lam": None, "y": y.tolist(), "secs": 0.0}
        return {"p": yf.tolist(), "lam": 1.0, "y": y.tolist(), "secs": 0.0}
    return fake


def fake_cert(key, frac="1/1", agree=True):
    fr = Fraction(frac)
    return {"n_pairs": 400, "count_search": float(fr * 400), "count_fraction": float(fr * 400),
            "count_registered_auc": float(fr * 400), "counts_agree": agree, "exact": float(fr),
            "fraction": f"{fr.numerator}/{fr.denominator}", "tau": float(fr),
            "registered_auc_exact": float(fr), "ulp_sensitive": False, "rerun_spread": 0.0,
            "reruns": [], "stages": {}, "budget": {}, "member": {}}


FLOW_ARGS = ["--fixture", "--workers", "1", "--smoke-n", "4", "--cert-budget", "tiny"]


def flow_setup(patch, fake=None, cert=None):
    patch(R, "fit_task", fake or make_fake())
    patch(R, "cert_task", cert or fake_cert)
    patch(K, "tree_state", lambda: "")


def run_flow(tmp, patch, fake=None, cert=None):
    flow_setup(patch, fake, cert)
    out = Path(tmp) / "run"
    return out, R.main(FLOW_ARGS + ["--out", str(out)])


# ------------------------------------------------------------------------------------------
# S-R1, S-R2.

@pytest.mark.parametrize("j", [0, 49, 89])
def test_SR1_construction_equals_perm_ref_y(j):
    assert np.array_equal(R.board_y_seeded(C.SEED_PERM_REF + j), C.perm_ref_y(j))
    assert np.array_equal(R.fresh_y(j), R.board_y_seeded(94000 + j))


def test_SR2_seeds_pass_and_patterns_fresh():
    r = R.assert_seeds_rep(R.N_BOARDS, 10)
    assert r["passed"], r
    p = R.assert_patterns_fresh(R.N_BOARDS)
    assert p["passed"] and p["n_seen_patterns"] >= 1 + 1 + 11 + 99, p


@pytest.mark.parametrize("bad", [93250, 93300, 93130, 93100, 91000, 92500, 5, 30050, 12345,
                                 20260929, 61000])
def test_SR2_a_seen_seed_is_refused(monkeypatch, bad):
    monkeypatch.setattr(R, "LITERAL_CERT_SEEDS", R.LITERAL_CERT_SEEDS | {bad})
    monkeypatch.setattr(R, "SEED_CERT_DEEP", R.SEED_CERT_DEEP + (bad,))
    assert not R.assert_seeds_rep(R.N_BOARDS, 10)["passed"]


def test_SR2_board_seeds_on_the_calibration_are_refused(monkeypatch):
    monkeypatch.setattr(R, "SEED_BOARD", C.SEED_PERM_REF)
    r = R.assert_seeds_rep(10, 10)
    assert not r["passed"] and not r["checks"]["boards_within_literal"]


def test_SR2_a_seen_pattern_is_refused_before_any_folder(tmp_path, monkeypatch):
    orig = R.fresh_y
    monkeypatch.setattr(R, "fresh_y", lambda j: C.perm_ref_y(5) if j == 2 else orig(j))
    p = R.assert_patterns_fresh(4)
    assert not p["passed"] and p["collisions"] == ["fresh:2 = perm:5"]
    tripwire(monkeypatch)
    monkeypatch.setattr(K, "tree_state", lambda: "")
    out = tmp_path / "run"
    with pytest.raises(SystemExit) as e:
        R.main(FLOW_ARGS + ["--out", str(out)])
    assert "FRESH PATTERN" in str(e.value.code) and not out.exists()


# ------------------------------------------------------------------------------------------
# S-R3: the cert seed swap.

def test_SR3_swap_restores_the_calibration_globals():
    before = (C.SEED_CERT_STAGE1, C.SEED_CERT_REFINE, C.SEED_CERT_DEEP)
    assert before == (93300, tuple(range(93301, 93306)), (93306, 93307))
    with R.fresh_cert_seeds():
        assert (C.SEED_CERT_STAGE1, C.SEED_CERT_REFINE, C.SEED_CERT_DEEP) == (
            94500, tuple(range(94501, 94506)), (94506, 94507))
    assert (C.SEED_CERT_STAGE1, C.SEED_CERT_REFINE, C.SEED_CERT_DEEP) == before
    with pytest.raises(RuntimeError):
        with R.fresh_cert_seeds():
            raise RuntimeError("inside")
    assert (C.SEED_CERT_STAGE1, C.SEED_CERT_REFINE, C.SEED_CERT_DEEP) == before


def test_SR3_cert_fresh_searches_with_94500_94507(monkeypatch):
    seen, orig = [], C.SV["best_auc"]

    def spy(*a, seed, **k):
        seen.append(seed)
        return orig(*a, seed=seed, **k)
    monkeypatch.setitem(C.SV, "best_auc", spy)
    R.cert_fresh(Z, C.CERT_BUDGET_TINY)
    assert seen == R.cert_seeds() == list(range(94500, 94508))
    assert C.SEED_CERT_STAGE1 == 93300


def test_SR3_swap_with_cal_seeds_reproduces_cal_cert_on_board_z():
    """With CAL's seeds swapped in, the call equals CAL's own cert_search on board z (tiny
    budget); and at the registered stage-1 budget the member equals CAL-OUT's stored member."""
    cal_seeds = (93300, range(93301, 93306), (93306, 93307))
    with R.fresh_cert_seeds(*cal_seeds):
        swapped = C.cert_search(Z, C.CERT_BUDGET_TINY)
    assert swapped == C.cert_search(Z, C.CERT_BUDGET_TINY)
    stage1 = {"K1": 100, "steps1": 500, "K2": 1, "steps2": 1, "deep_K": 1, "deep_steps": 1}
    with R.fresh_cert_seeds(*cal_seeds):
        c = C.cert_search(Z, stage1)
    stored = json.loads((CAL_OUT / "cert_members.json").read_text(encoding="utf-8"))[
        hashlib.sha256(Z.tobytes()).hexdigest()[:16]]
    assert c["fraction"] == stored["fraction"] == "1/1"
    assert c["member"] == stored["member"]


def test_SR3_the_swap_acts_inside_worker_processes():
    """A two-worker pool certifies two seen boards; each result equals cert_fresh in this
    process and differs from the CAL-seeded search, so the swap ran in the worker."""
    budget = C.CERT_BUDGET_TINY
    res = R.run_pool([[("seen:0", "cert", "cert")], [("seen:1", "cert", "cert")]], 2,
                     (10, budget), "cert test")
    for key in ("seen:0", "seen:1"):
        here = R.cert_fresh(R.pattern_of(key), budget)
        assert res[(key, "cert", "cert")]["member"] == here["member"]
        assert C.cert_search(R.pattern_of(key), budget)["member"] != here["member"]


# ------------------------------------------------------------------------------------------
# S-R5: rows and flags.

def p_auc(y, m):
    """p = 1 on the present cells and on m absent ones: AUC = (400 - 10 m) / 400 on 20 / 20."""
    y = np.asarray(y, bool)
    p = y.astype(float)
    p[np.flatnonzero(~y)[:m]] = 1.0
    return p.tolist()


def synthetic_F(key, cb, c1, c1f, clcf, s100, bf_cb=0, bf_c1=0):
    y = R.pattern_of(key)
    F = {(key, "block", "rule"): {"p": p_auc(y, cb), "lam": 100.0, "y": y.tolist()},
         (key, "sep", "rule"): {"lambda_c": 100.0, "reg_p": p_auc(y, cb), "reg_float_p":
                                p_auc(y, clcf), "ceil1_p": p_auc(y, c1),
                                "ceil1_float_p": p_auc(y, c1f), "ceil1_s100_p": p_auc(y, s100),
                                "ceil1_s100_float_p": p_auc(y, s100), "y": y.tolist()},
         (key, "block", "N1"): {"p": [0.5] * 40, "lam": None, "y": y.tolist()}}
    for pk in K.BF_KEYS:
        F[(key, "block", pk)] = {"p": p_auc(y, bf_cb), "lam": 100.0, "y": y.tolist()}
        F[(key, "blk1", pk)] = {"p": p_auc(y, bf_c1), "lam": 1.0, "y": y.tolist()}
    return F


@pytest.mark.parametrize("ms,frac,row", [
    ((0, 0, 0, 0, 0), "1/1", "gate passed"),
    ((4, 16, 16, 16, 16), "1/1", "gate passed"),                          # 0.90 at the cut
    ((16, 0, 0, 0, 0), "719/800", "not separated: rank limit or fit"),
    ((16, 0, 0, 16, 0), "9/10", "fit failure, FF-sel"),                   # cert at the cut
    ((16, 4, 16, 16, 16), "1/1", "fit failure, FF-sel"),                  # ceil_1 at the cut
    ((16, 0, 0, 4, 0), "1/1", "fit failure, FF-sel; and FF-quant at lambda_c"),
    ((16, 5, 4, 16, 16), "1/1", "fit failure, FF-quant (at lambda = 1)"),
    ((16, 5, 5, 16, 4), "1/1", "fit failure, FF-struct or FF-opt, not separated; ceil_1_starts100"),
    ((16, 5, 5, 16, 5), "1/1", R.J89_ROW)])
def test_SR5_separator_rows_per_board(ms, frac, row):
    key = "seen:3"
    F = synthetic_F(key, *ms)
    certs = {R.pattern_of(key).tobytes(): fake_cert(key, frac)}
    b = R.read_board(key, F, certs)
    assert b["reading"].startswith(row)
    if row in ("fit failure, FF-sel", R.J89_ROW):
        assert b["reading"] == row
    assert b["block_fit_reproduced"] and not b["stops"]
    assert b["cert_ok"] == (Fraction(frac) >= Fraction(9, 10))


def test_SR5_cert_at_the_cut_reads_by_the_float_route():
    """9/10 is certified; the Fraction and the float route agree (a Fraction passed to
    separator_reading would read Fraction(9, 10) < 0.9 and not separate)."""
    assert R.cert_ok(fake_cert("x", "9/10"))
    assert not R.cert_ok(fake_cert("x", "719/800"))
    assert Fraction(9, 10) < 0.9                       # why the float route is used


@pytest.mark.parametrize("r,cb,c1,row", [
    (1, 0.95, 0.5, "gate passed"), (1, 0.90, 0.5, "gate passed"),
    (2, 0.85, 0.90, "BF fit failure, selection"), (3, 0.85, 0.89, "BF: not separated"),
    (4, 0.85, 0.89, "BF fit failure, not selection"), (4, 0.85, 0.95, "BF fit failure, selection")])
def test_SR5_bf_row_table(r, cb, c1, row):
    assert R.bf_reading(r, cb, c1) == row


def _o(x, t=None):
    return {"exact": x, "tau": x if t is None else t}


def test_SR5_flags_including_decoder_split_on_j49():
    one = {**_o(1.0), "fraction": "1/1", "counts_agree": True}
    # j = 49 as seen: ceiling_block 0.915 at lambda 100, ceil_lambda_c_float 0.895, ceil_1 0.9775
    assert R.flags_of(_o(0.915), _o(0.9775), one, _o(0.895)) == ["DECODER_SPLIT_AT_LC"]
    assert R.flags_of(_o(0.73), _o(0.895), one, _o(0.73)) == []
    assert "GATE_ULP_SPLIT" in R.flags_of(_o(0.90, 0.895), _o(1.0), one, _o(0.9))
    assert "CEIL_1_ULP_SPLIT" in R.flags_of(_o(0.7), _o(0.90, 0.895), one, _o(0.7))
    low = {**_o(0.89875), "fraction": "719/800", "counts_agree": True}
    assert R.flags_of(_o(0.7), _o(1.0), low, _o(0.7)) == ["CERT_BELOW_CUT"]
    split = {"exact": 0.9, "tau": 0.89875, "fraction": "9/10", "counts_agree": True}
    assert R.flags_of(_o(0.95), _o(1.0), split, _o(0.95)) == ["CERT_ULP_SPLIT"]
    dis = {**one, "counts_agree": False}
    assert R.flags_of(_o(0.95), _o(1.0), dis, _o(0.95)) == ["CERT_COUNTS_DISAGREE"]


# ------------------------------------------------------------------------------------------
# J89: the seen board j = 89, read by hand.

def j89_seen_values():
    with open(CAL_OUT / "permuted_reference.csv", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    r = rows[89]                                       # line 91 of the file
    assert r["j"] == "89" and r["seed"] == "93289"
    return {k: float(r[k]) for k in ("ceiling_block", "cert", "ceil_1", "ceil_1_float",
                                     "ceil_lambda_c_float", "lambda_c")}


def j89_board(s100):
    s = j89_seen_values()
    row, sub = C.separator_reading(s["ceiling_block"], s["cert"], s["ceil_1"], s["ceil_1_float"],
                                   s["ceil_lambda_c_float"], s100)
    return {"key": "seen:89", "cert_ok": R.cert_ok({"fraction": "79/80", "exact": s["cert"]}),
            "ceiling_block": _o(s["ceiling_block"]), "reading": row, "subkinds": sub,
            "lambda_block": s["lambda_c"], "ceil_1": _o(s["ceil_1"])}


def test_J89_seen_values_classify_as_reproduced():
    s = j89_seen_values()
    assert (s["ceiling_block"], s["ceil_1"], s["ceil_1_float"], s["cert"]) == (
        0.73, 0.895, 0.895, 0.9875)
    b = j89_board(0.895)                               # ceil_1_starts100 read in section 1
    assert b["reading"] == R.J89_ROW
    out = R.j89_outcome([b])
    assert out["label"] == "J89-reproduced" and out["same_row_as_j89"] == ["seen:89"]


def test_J89_ff_opt_named_does_not_reproduce():
    b = j89_board(0.92)
    assert b["subkinds"] == ["FF-opt"]
    out = R.j89_outcome([b])
    assert out["label"] == "J89-not-reproduced" and out["ff_opt_named"] == ["seen:89"]


# ------------------------------------------------------------------------------------------
# S-R7: predictions and labels at their boundaries.

def mb(fail, lam=None, sub=None, bf_fail=None, cert=True, reading=None, c1=1.0):
    lam = lam if lam is not None else (100.0 if fail else 1.0)
    sub = sub if sub is not None else (["FF-sel"] if fail else [])
    reading = reading or ("gate passed" if not fail else
                          "fit failure, FF-sel" if sub == ["FF-sel"] else R.J89_ROW)
    bff = fail if bf_fail is None else bf_fail
    return {"key": "b", "cert_ok": cert, "ceiling_block": _o(0.6 if fail else 0.95),
            "lambda_block": lam, "subkinds": sub, "reading": reading, "ceil_1": _o(c1),
            "bf": {pk: {"ceiling_block": _o(0.6 if (bff[pk] if isinstance(bff, dict) else bff)
                                            else 0.95)} for pk in K.BF_KEYS}}


def boards(n_fail, n=300, n_nonsel=0, **kw):
    out = [mb(True, sub=["FF-struct-or-FF-opt"]) for _ in range(n_nonsel)]
    out += [mb(True) for _ in range(n_fail - n_nonsel)]
    return out + [mb(False) for _ in range(n - n_fail)]


@pytest.mark.parametrize("k,holds", [(119, False), (120, True), (180, True), (181, False)])
def test_P1_boundaries(k, holds):
    assert R.evaluate_predictions(boards(k))["P1"]["holds"] is holds


@pytest.mark.parametrize("m,holds,rejects", [(10, True, False), (11, False, False),
                                             (15, False, False), (16, False, True)])
def test_P2b_decision_line_10_and_the_printed_test(m, holds, rejects):
    P = R.evaluate_predictions(boards(150, n_nonsel=m))
    assert P["P2b"]["holds"] is holds and P["P2b"]["count"] == m
    assert P["P2b"]["test_5pct"]["rejects"] is rejects and not P["P2b"]["test_5pct"]["decides"]
    line = next(x for x in R.prediction_lines(P) if x.startswith("P2b"))
    assert ("hold" if holds else "fail") in line and "deciding nothing" in line


def test_P2b_counts_ff_opt_and_ff_quant_too():
    bs = boards(150) + [mb(True, sub=["FF-opt"]), mb(True, sub=["FF-quant"]),
                        mb(True, sub=["FF-sel", "FF-quant@lambda_c"])]
    assert R.evaluate_predictions(bs)["P2b"]["count"] == 2


def test_P2a_is_a_design_check():
    P = R.evaluate_predictions(boards(150))
    assert P["P2a"]["holds"] and P["P2a"]["design_check"]
    assert "design check" in R.prediction_lines(P)[1]
    bad = boards(150) + [mb(True, reading="not separated: rank limit or fit (x)")]
    assert not R.evaluate_predictions(bad)["P2a"]["holds"]


@pytest.mark.parametrize("n_rule,n_bf,holds", [(150, 74, False), (150, 75, True),
                                              (100, 200, True), (100, 201, False)])
def test_P3_band(n_rule, n_bf, holds):
    bs = []
    for i in range(300):
        fail = i < n_rule
        bff = {pk: (i < n_bf if pk == "BF:2" else fail) for pk in K.BF_KEYS}
        bs.append(mb(fail, bf_fail=bff))
    P = R.evaluate_predictions(bs)
    assert P["P3"]["per_r"]["BF:2"]["holds"] is holds and P["P3"]["holds"] is holds
    t = P["P3"]["per_r"]["BF:2"]["table_2x2"]
    assert sum(t.values()) == 300


@pytest.mark.parametrize("n100,holds", [(10, True), (11, False)])
def test_P4prime_at_90_percent(n100, holds):
    bs = [mb(True) for _ in range(200)] + [mb(False, lam=100.0) for _ in range(n100)] + [
        mb(False) for _ in range(100 - n100)]
    P = R.evaluate_predictions(bs)
    assert P["P4p"]["holds"] is holds and P["P4p"]["passes_lambda_not_1"] == n100
    assert "P4" not in P                               # withdrawn, not evaluated


@pytest.mark.parametrize("pass100,holds_i", [(10, True), (11, False)])
def test_P5_part_i(pass100, holds_i):
    bs = [mb(True) for _ in range(100 - pass100)] + [mb(False, lam=100.0)
                                                     for _ in range(pass100)]
    bs += [mb(False) for _ in range(300 - len(bs))]
    P = R.evaluate_predictions(bs)
    assert P["P5"]["i"]["holds"] is holds_i and P["P5"]["ii"]["holds"]
    assert P["P5"]["ff_sel_count"] == 100 - pass100


@pytest.mark.parametrize("fail_other,holds_ii", [(5, True), (6, False)])
def test_P5_part_ii(fail_other, holds_ii):
    bs = [mb(True) for _ in range(100 - fail_other)] + [mb(True, lam=3.0)
                                                         for _ in range(fail_other)]
    bs += [mb(False) for _ in range(200)]
    P = R.evaluate_predictions(bs)
    assert P["P5"]["ii"]["holds"] is holds_ii and P["P5"]["i"]["holds"]


def labels_of(bs, stops=()):
    return R.outcome_labels(bs, R.evaluate_predictions(bs), list(stops))


def test_labels_at_their_boundaries():
    assert labels_of(boards(150)) == ["RP1"]
    assert labels_of(boards(119)) == ["RP2"]
    assert labels_of(boards(30)) == ["RP2"]
    assert labels_of(boards(29)) == ["RP4"]
    assert labels_of(boards(150, n_nonsel=11)) == ["RP3"]
    assert labels_of(boards(20, n_nonsel=11)) == ["RP3", "RP4"]
    below = mb(True, cert=False, reading="not separated: rank limit or fit (x)", sub=[])
    assert labels_of(boards(150) + [below]) == ["RP1", "RP5"]
    assert labels_of(boards(150), stops=["a stop"]) == ["RP6"]


def test_cert_below_cut_leaves_the_denominators():
    below = mb(True, cert=False, reading="not separated: rank limit or fit (x)", sub=[])
    P = R.evaluate_predictions(boards(150) + [below])
    assert P["N"] == 301 and P["N_c"] == 300 and P["failures"] == 150


# ------------------------------------------------------------------------------------------
# Real fits on a SEEN board (seconds): the registered block fit reproduces CAL-OUT's row.

def test_real_fits_on_seen_board_89_reproduce_cal_out():
    R._rw_init(10, C.CERT_BUDGET_TINY)
    key = "seen:89"
    bank = R.build_bank_rep(key)
    y = R.pattern_of(key)
    rule = R.fit_task(key, "block", "rule", bank)
    bf1 = R.fit_task(key, "block", "BF:1", bank)
    assert rule["lam"] == 100.0 and C.auc_counts(rule["p"], y)["exact"] == 0.73
    assert C.auc_counts(bf1["p"], y)["exact"] == 0.725


# ------------------------------------------------------------------------------------------
# Flows (stand-in fits on seen boards): outputs and stops.

def test_flow_completes_with_outputs_and_sums(tmp_path, monkeypatch):
    out, res = run_flow(tmp_path, monkeypatch.setattr)
    assert res["completed"] and res["labels"] == ["RP2"]
    assert not K.verify_sha256sums(out)
    names = {p.name for p in out.iterdir()}
    assert {"SHA256SUMS.txt", "REPLICATION.md", "boards.csv", "replication.json", "stdout.log",
            "cert_members.json", "raw_fits.json.gz"} <= names and R.STOP_RECORD_NAME not in names
    header = (out / "boards.csv").read_text(encoding="utf-8").splitlines()[0]
    assert header == ",".join(R.BOARDS_HEADER) and header.isascii()
    js = json.loads((out / "replication.json").read_text(encoding="utf-8"))
    assert js["manifest"]["not_registered"].startswith(R.NOT_REGISTERED_TEXT)
    assert [b["key"] for b in js["boards"]] == ["seen:0", "seen:1", "seen:2", "seen:3"]
    log = (out / "stdout.log").read_text(encoding="utf-8")
    for tag in ("P1:", "P2a (a design check", "P2b:", "P3:", "P4':", "P5 (a label",
                "FF-sel among lambda_c = 100", "(iii) population", "SECONDARY", "OUTCOME"):
        assert tag in log, tag
    assert "P4:" not in log
    md = (out / "REPLICATION.md").read_text(encoding="utf-8")
    assert "Passes at lambda = 100 (separate)" in md and "(iii): passes at lambda = 1" in md
    assert (out / "boards.csv").read_bytes().count(b"\r") == 0


@pytest.mark.parametrize("ov", [{(2, "reg_p"): lambda y: low_block_p(y, 5).tolist()},
                                {(2, "lambda_c"): lambda y: 3.0}])
def test_script_defect_stops_with_record_and_no_sums(tmp_path, monkeypatch, ov):
    """S-R6: a refit that differs from the registered block fit, or its lambda, stops (RP6)."""
    fake = make_fake(overrides=ov)
    with pytest.raises(SystemExit) as e:
        run_flow(tmp_path, monkeypatch.setattr, fake=fake)
    assert e.value.code == 1
    out = tmp_path / "run"
    rec = json.loads((out / R.STOP_RECORD_NAME).read_text(encoding="utf-8"))
    assert "SCRIPT DEFECT" in rec["stop"] and rec["outcome"] == "RP6"
    assert not (out / "SHA256SUMS.txt").exists() and (out / "boards.csv").exists()


def test_cert_counts_disagree_is_a_flag_not_a_stop(tmp_path, monkeypatch):
    """Rev 1.2 (CAL section 6a, 14a A-3): the Fraction count is the certificate; a disagreement
    of the three counts is flagged CERT_COUNTS_DISAGREE and the run completes."""
    out, res = run_flow(tmp_path, monkeypatch.setattr,
                        cert=lambda key: fake_cert(key, agree=key != "seen:1"))
    assert res["completed"] and not res["stops"] and "RP6" not in res["labels"]
    flagged = [b["key"] for b in res["boards"] if "CERT_COUNTS_DISAGREE" in b["flags"]]
    assert flagged == ["seen:1"] and res["flag_counts"]["CERT_COUNTS_DISAGREE"] == 1
    assert not K.verify_sha256sums(out) and not (out / R.STOP_RECORD_NAME).exists()
    assert "CERT_COUNTS_DISAGREE rows: 1" in (out / "REPLICATION.md").read_text(encoding="utf-8")


def test_estimate_times_a_seen_board_only(monkeypatch):
    keys = []

    def fake_fit(bk, mk, pk, bank):
        keys.append(bk)
        return {}
    monkeypatch.setattr(R, "fit_task", fake_fit)
    monkeypatch.setattr(R, "cert_fresh", lambda y, b: {})
    monkeypatch.setattr(R, "_rw_init", lambda *a: None)
    r = R.main(["--estimate", "--fixture", "--cert-budget", "tiny", "--workers", "30"])["estimate"]
    assert set(keys) == {"seen:0"} and r["n_boards"] == 300 and len(r["timings_s"]) == 12


# ------------------------------------------------------------------------------------------
# S-R9: refusals before any folder, all under the tripwire.

def test_registered_form_refusals_leave_no_folder(tmp_path, monkeypatch):
    tripwire(monkeypatch)
    out = tmp_path / "reg"
    monkeypatch.setattr(R, "REGISTRATION_SHA256_LF_PINNED", None)
    monkeypatch.setattr(R, "PREDICTION_COMMIT_PINNED", PREDICTION_COMMIT)
    monkeypatch.setattr(K, "tree_state", lambda: "")
    with pytest.raises(SystemExit) as e:               # the registration is not pinned
        R.main(["--out", str(out)])
    assert "registration is not pinned" in str(e.value.code) and not out.exists()
    monkeypatch.setattr(R, "REGISTRATION_SHA256_LF_PINNED", K.sha256_lf(R.ROOT / R.REGISTRATION))
    monkeypatch.setattr(R, "PREDICTION_COMMIT_PINNED", None)
    with pytest.raises(SystemExit) as e:               # the prediction commit is not pinned
        R.main(["--out", str(out)])
    assert "prediction commit is not pinned" in str(e.value.code) and not out.exists()
    monkeypatch.setattr(R, "PREDICTION_COMMIT_PINNED", "0" * 40)
    with pytest.raises(SystemExit) as e:               # an unknown commit
        R.main(["--out", str(out)])
    assert "merge-base failed" in str(e.value.code) and not out.exists()
    monkeypatch.setattr(R, "PREDICTION_COMMIT_PINNED", PREDICTION_COMMIT)
    monkeypatch.setattr(R, "git_is_ancestor", lambda c: (False, f"{c} is not an ancestor of HEAD"))
    with pytest.raises(SystemExit) as e:               # not an ancestor of HEAD
        R.main(["--out", str(out)])
    assert "not an ancestor" in str(e.value.code) and not out.exists()
    monkeypatch.undo()
    tripwire(monkeypatch)
    monkeypatch.setattr(R, "REGISTRATION_SHA256_LF_PINNED", K.sha256_lf(R.ROOT / R.REGISTRATION))
    monkeypatch.setattr(R, "PREDICTION_COMMIT_PINNED", PREDICTION_COMMIT)
    monkeypatch.setattr(K, "tree_state", lambda: " M results/genome/c6/x.py")
    with pytest.raises(SystemExit) as e:               # a dirty tree
        R.main(["--out", str(out)])
    assert "uncommitted" in str(e.value.code) and not out.exists()


def test_git_is_ancestor_on_the_real_history():
    assert R.git_is_ancestor(PREDICTION_COMMIT) == (True, "")
    assert R.git_is_ancestor("4de54af20d16c6b432da4f8b9bdc64214635ff66")[0]
    ok, why = R.git_is_ancestor("f" * 40)
    assert not ok and "merge-base failed" in why


@pytest.mark.parametrize("form", [["--dry-run"], ["--estimate", "--fixture"],
                                  FLOW_ARGS + ["--out", "OUT"]])
def test_run_outside_the_repo_root_is_refused(tmp_path, monkeypatch, form):
    tripwire(monkeypatch)
    monkeypatch.chdir(tmp_path)
    argv = [str(tmp_path / "o") if x == "OUT" else x for x in form]
    with pytest.raises(SystemExit) as e:
        R.main(argv)
    assert "repository root" in str(e.value.code) and not (tmp_path / "o").exists()


def test_out_refusals(tmp_path, monkeypatch):
    tripwire(monkeypatch)
    monkeypatch.setattr(K, "tree_state", lambda: "")
    exists = tmp_path / "exists"
    exists.mkdir()
    with pytest.raises(SystemExit) as e:
        R.main(FLOW_ARGS + ["--out", str(exists)])
    assert "exists" in str(e.value.code)
    with pytest.raises(SystemExit) as e:
        R.main(FLOW_ARGS + ["--out", str(CAL_OUT / "inside")])
    assert "calibration's reference folder" in str(e.value.code)
    assert not (CAL_OUT / "inside").exists()
    ref = tmp_path / "refB"
    monkeypatch.setattr(K, "PRERUN_DIR", ref)
    with pytest.raises(SystemExit) as e:
        R.main(FLOW_ARGS + ["--out", str(ref / "inside")])
    assert "reference folder" in str(e.value.code) and not ref.exists()


def test_script_pins_refuse(tmp_path, monkeypatch):
    assert K.sha256_lf(R.ROOT / R.CAL_SCRIPT) == R.CAL_SCRIPT_SHA256_LF == \
        "220201c229800097aed62afba242a7e3593d9f7205274fc015207ab795d3af43"
    tripwire(monkeypatch)
    monkeypatch.setattr(R, "CAL_SCRIPT_SHA256_LF", "0" * 64)
    with pytest.raises(SystemExit) as e:
        R.main(FLOW_ARGS + ["--out", str(tmp_path / "new")])
    assert "failed_fit_calibration.py has LF sha256" in str(e.value.code)
    assert not (tmp_path / "new").exists()


def test_dry_run_writes_nothing_and_lists_the_refusals(tmp_path, monkeypatch):
    tripwire(monkeypatch)
    monkeypatch.setattr(K, "tree_state", lambda: "")
    r = R.main(["--dry-run", "--out", str(tmp_path / "x")])
    assert r["dry_run"] and not (tmp_path / "x").exists()
    assert r["keys"][0] == "fresh:0" and len(r["keys"]) == 300
    refs = r["gate"]["refusals_of_a_run"]
    assert any("registration is not pinned" in s for s in refs)
    assert any("prediction commit is not pinned" in s for s in refs)


def test_pins_are_unset_in_this_revision():
    assert R.REGISTRATION_SHA256_LF_PINNED is None and R.PREDICTION_COMMIT_PINNED is None


# ------------------------------------------------------------------------------------------
# Windows encoding: a cp1252 child with its stdout redirected to a file.

def encoding_child(tmp):
    def patch(obj, name, value):
        setattr(obj, name, value)
    run_flow(tmp, patch)


def test_encoding_cp1252_redirected_stdout(tmp_path):
    env = {k: x for k, x in os.environ.items() if not k.startswith("PYTHON")}
    env.update(PYTHONUTF8="0", PYTHONIOENCODING="cp1252:strict")
    log = tmp_path / "child_stdout.txt"
    code = (f"import sys; sys.path.insert(0, {str(CHECKS)!r}); "
            f"import test_natural_fit_failure_replication as T; T.encoding_child({str(tmp_path)!r})")
    with open(log, "wb") as fh:
        p = subprocess.run([PY, "-c", code], stdout=fh, stderr=subprocess.PIPE, env=env,
                           cwd=str(R.ROOT), timeout=150)
    assert p.returncode == 0, p.stderr.decode("utf-8", "replace")[-3000:]
    out = tmp_path / "run"
    assert not K.verify_sha256sums(out)
    for f in ("stdout.log", "boards.csv", "REPLICATION.md", "replication.json"):
        assert (out / f).read_bytes().isascii(), f
    assert log.read_bytes().isascii() and b"OUTCOME" in log.read_bytes()
    man = json.loads((out / "replication.json").read_text(encoding="utf-8"))["manifest"]
    assert man["log_output_errors"] == 0
