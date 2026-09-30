"""Tests of block_b_ceil1.py (registration docs/plans/2026-09-30-block-b-ceil1-registration.md).

No test fits the real block, searches a capacity or opens a pool. An autouse fixture (a) forces the
registration and prediction-commit pins to None, so nothing can start the real run, and (b) trips
every fitter, the cert search and any pool. The flow tests replace the seams of block_b_ceil1 (fit_at,
cert_real, real_block_y, load_stored, input_hashes, gate_checks, pin_refusal) by stand-ins.

Run: PYTHONUTF8=1 timeout 200 tools/.venv/Scripts/python.exe -m pytest
results/genome/c6/checks/test_block_b_ceil1.py -q
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

CHECKS = Path(__file__).resolve().parent
sys.path.insert(0, str(CHECKS))
import block_b_ceil1 as B  # noqa: E402

C, K, H, R = B.C, B.K, B.H, B.R


def _no(*a, **k):
    raise AssertionError("tripwire: a fit, a search, a pool or the run body was reached")


class NoPool:
    def __init__(self, *a, **k):
        raise AssertionError("tripwire: a process pool was opened")


@pytest.fixture(autouse=True)
def guard(monkeypatch):
    monkeypatch.setattr(B, "REGISTRATION_SHA256_LF_PINNED", None)
    monkeypatch.setattr(B, "PREDICTION_COMMIT_PINNED", None)
    monkeypatch.setattr(R, "cwd_refusal", lambda: None)
    for mod, names in (
            (B, ("fit_at", "cert_real")),
            (C, ("train_shortcut", "train_capturing", "train_full_path_fixed", "forced_block_fit",
                 "separator_fits", "bf_block_lambda1", "cert_search", "cert_task", "fit_task",
                 "run_groups", "_run", "_cw_group", "_cw_init")),
            (R, ("cert_fresh", "run_pool", "_run", "_rw_group", "_rw_init", "estimate")),
            (K, ("_fit_one", "_w_init", "degree_terms", "run_groups", "_w_group",
                 "train_fixed_lambda"))):
        for n in names:
            monkeypatch.setattr(mod, n, _no)
    for mod in (B, C, R, K, H):
        if hasattr(mod, "ProcessPoolExecutor"):
            monkeypatch.setattr(mod, "ProcessPoolExecutor", NoPool)


# ------------------------------------------------------------------------------------------
# Stand-ins.

def auc(exact, tau=None):
    return {"exact": exact, "tau": exact if tau is None else tau, "n_pairs": 399, "levels": 30,
            "twice": 0, "ulp_sensitive": tau is not None and tau != exact}


def cert(frac="1/1", tau=None, agree=True):
    fr = Fraction(frac)
    return {"fraction": f"{fr.numerator}/{fr.denominator}", "exact": float(fr),
            "tau": float(fr) if tau is None else tau, "counts_agree": agree, "ulp_sensitive": False,
            "rerun_spread": 0.0, "n_pairs": 399, "count_search": 0.0, "count_fraction": 0.0,
            "count_registered_auc": 0.0}


Y = np.zeros(K.N_BLOCK, bool)
Y[:19] = True


def p_with_auc(wins_first):
    """Scores on Y: the first `wins_first` positives above every negative, the rest below."""
    p = np.zeros(K.N_BLOCK)
    p[:19] = 0.1
    p[:wins_first] = 0.9
    p[19:] = 0.5
    return p


# ------------------------------------------------------------------------------------------
# The reading tree (section 3).

@pytest.mark.parametrize("c1,c1f", [(0.99, 0.99), (0.5, 0.5), (0.95, 0.5)])
def test_a_cert_below_cut_outranks_everything(c1, c1f):
    r = B.read_tree(cert("359/399"), auc(c1), auc(c1f))
    assert r["branch"] == B.BRANCH_A


def test_cert_at_nine_tenths_exactly_is_a_pass():
    assert B.cert_ok_of(cert("9/10")) is True
    assert B.cert_ok_of(cert("359/399")) is False


def test_b_label_stands():
    r = B.read_tree(cert(), auc(0.80), auc(0.80))
    assert r["branch"] == B.BRANCH_B and not r["qualified"] and r["flags"] == []


def test_c_ff_sel():
    r = B.read_tree(cert(), auc(0.97), auc(0.96))
    assert r["branch"] == B.BRANCH_C and not r["qualified"] and "cannot" in r["text"]


@pytest.mark.parametrize("q,f,direction", [
    (0.95, 0.85, "float < 0.90 <= quantised"),
    (0.85, 0.95, "quantised < 0.90 <= float (FF-quant direction)")])
def test_d_decoder_split_both_directions(q, f, direction):
    r = B.read_tree(cert(), auc(q), auc(f))
    assert r["branch"] == B.BRANCH_D and r["decoder_direction"] == direction
    assert direction in r["text"]


def test_d_is_not_read_when_cert_fails():
    assert B.read_tree(cert("1/2"), auc(0.95), auc(0.85))["branch"] == B.BRANCH_A


@pytest.mark.parametrize("x,branch,qualified", [
    (0.88, B.BRANCH_B, True), (0.879, B.BRANCH_B, False), (0.8999, B.BRANCH_B, True),
    (0.90, B.BRANCH_C, True), (0.92, B.BRANCH_C, True), (0.921, B.BRANCH_C, False),
    (0.9649, B.BRANCH_C, False)])
def test_rider_at_the_cut(x, branch, qualified):
    r = B.read_tree(cert(), auc(x), auc(x))
    assert r["branch"] == branch and r["qualified"] is qualified and r["at_the_cut"] is (
        0.88 <= x <= 0.92)
    assert ("AT THE CUT" in r["text"]) is qualified


def test_rider_does_not_qualify_a_or_d():
    assert not B.read_tree(cert("1/2"), auc(0.89), auc(0.89))["qualified"]
    assert not B.read_tree(cert(), auc(0.91), auc(0.85))["qualified"]


def test_ulp_split_on_ceil_1_follows_exact_and_is_flagged():
    r = B.read_tree(cert(), auc(0.9047, tau=0.8997), auc(0.95))
    assert B.GATE_ULP_SPLIT in r["flags"] and "TAU_READING_DIFFERS" in r["flags"]
    assert r["branch"] == B.BRANCH_C and r["branch_tau"] == B.BRANCH_D
    assert "GATE_ULP_SPLIT" in r["text"]


def test_ulp_split_the_other_way_and_on_cert():
    r = B.read_tree(cert(), auc(0.8997, tau=0.9047), auc(0.85))
    assert B.GATE_ULP_SPLIT in r["flags"] and r["branch"] == B.BRANCH_B
    r = B.read_tree(cert("1/1", tau=0.85), auc(0.95), auc(0.95))
    assert "CERT_ULP_SPLIT" in r["flags"] and r["branch"] == B.BRANCH_C
    assert r["branch_tau"] == B.BRANCH_A


def test_no_split_no_flags_and_counts_disagree_flag():
    assert B.read_tree(cert(), auc(0.95), auc(0.95))["flags"] == []
    assert "CERT_COUNTS_DISAGREE" in B.read_tree(cert(agree=False), auc(0.95), auc(0.95))["flags"]


# ------------------------------------------------------------------------------------------
# The control (section 2).

def test_control_literal_is_309_over_399():
    assert B.CONTROL_CEILING == 309 / 399 == 0.7744360902255639
    assert f"{B.CONTROL_CEILING:.15g}" == "0.774436090225564"
    assert 0.774436090225564 != B.CONTROL_CEILING        # the 15-digit rendering is not the float
    assert B.CONTROL_TWICE == 2 * 303 + 12 and B.N_PAIRS == 19 * 21


def test_control_verdict():
    ok, why = B.control_verdict(auc(B.CONTROL_CEILING))
    assert ok and why == []
    ok, why = B.control_verdict(auc(0.7744))
    assert not ok and len(why) == 1
    ok, why = B.control_verdict(auc(B.CONTROL_CEILING, tau=0.7))
    assert not ok and len(why) == 1
    assert not B.control_verdict({"exact": None, "tau": None})[0]
    assert not B.control_verdict(auc(np.nextafter(B.CONTROL_CEILING, 1.0)))[0]


def test_min_gap():
    assert B.min_gap([0.1, 0.1, 0.4, 0.7]) == pytest.approx(0.3)
    assert B.min_gap([0.5, 0.5]) is None


# ------------------------------------------------------------------------------------------
# Refusals; the tripwire is live.

def test_tripwire_is_live():
    with pytest.raises(AssertionError, match="tripwire"):
        B.fit_at(1.0)
    with pytest.raises(AssertionError, match="tripwire"):
        B.cert_real(Y)
    with pytest.raises(AssertionError, match="tripwire"):
        C.train_shortcut(None, None, 1.0)
    with pytest.raises(AssertionError, match="tripwire"):
        K._fit_one("real", "block", "rule", None)
    with pytest.raises(AssertionError, match="tripwire"):
        C.ProcessPoolExecutor(2)


def test_pin_none_refuses_before_anything(tmp_path):
    assert B.REGISTRATION_SHA256_LF_PINNED is None
    with pytest.raises(SystemExit) as e:
        B.main(["--out", str(tmp_path / "o")])
    assert "not pinned" in str(e.value)
    assert not (tmp_path / "o").exists()


def test_pin_mismatch_refuses(monkeypatch, tmp_path):
    monkeypatch.setattr(B, "REGISTRATION_SHA256_LF_PINNED", "0" * 64)
    with pytest.raises(SystemExit) as e:
        B.main(["--out", str(tmp_path / "o")])
    assert "pinned" in str(e.value) and "REFUSED" in str(e.value)


def test_prediction_commit_none_refuses(monkeypatch, tmp_path):
    monkeypatch.setattr(B, "REGISTRATION_SHA256_LF_PINNED", K.sha256_lf(B.ROOT / B.REGISTRATION))
    with pytest.raises(SystemExit) as e:
        B.main(["--out", str(tmp_path / "o")])
    assert "prediction commit" in str(e.value)


def test_dirty_tree_refuses(monkeypatch, tmp_path):
    monkeypatch.setattr(B, "REGISTRATION_SHA256_LF_PINNED", K.sha256_lf(B.ROOT / B.REGISTRATION))
    monkeypatch.setattr(B, "PREDICTION_COMMIT_PINNED", "HEAD")
    monkeypatch.setattr(K, "tree_state", lambda: " M docs/plans/x.md")
    with pytest.raises(SystemExit) as e:
        B.main(["--out", str(tmp_path / "o")])
    assert "uncommitted" in str(e.value)


def test_existing_result_is_never_overwritten(monkeypatch, tmp_path):
    monkeypatch.setattr(B, "pin_refusal", lambda: None)
    (tmp_path / B.RESULT_MD).write_text("x")
    with pytest.raises(SystemExit) as e:
        B.main(["--out", str(tmp_path)])
    assert "never overwrites" in str(e.value)
    assert (tmp_path / B.RESULT_MD).read_text() == "x"


def test_dry_run_fits_nothing(monkeypatch, tmp_path):
    monkeypatch.setattr(B, "input_hashes", lambda: {"fake": 1})
    r = B.main(["--dry-run", "--out", str(tmp_path / "o")])
    assert r["dry_run"] and "not pinned" in r["refusal"] and not (tmp_path / "o").exists()


# ------------------------------------------------------------------------------------------
# The flow, on stand-ins.

def flow(monkeypatch, ctl_p, one_p, one_pf, cert_value=None, calls=None):
    calls = calls if calls is not None else []

    def fit_at(lam, starts=None):
        calls.append(("fit", lam, starts))
        p = ctl_p if lam == B.LAMBDA_REGISTERED else one_p
        pf = ctl_p if lam == B.LAMBDA_REGISTERED else one_pf
        return {"lambda": lam, "starts": starts, "p": list(map(float, p)),
                "p_float": list(map(float, pf))}

    def cert_real(y):
        calls.append(("cert",))
        return cert_value or cert()
    monkeypatch.setattr(B, "pin_refusal", lambda: None)
    monkeypatch.setattr(B, "fit_at", fit_at)
    monkeypatch.setattr(B, "cert_real", cert_real)
    monkeypatch.setattr(B, "real_block_y", lambda: Y.copy())
    monkeypatch.setattr(B, "load_stored", lambda key: {"p": list(map(float, ctl_p)), "lam": 100.0})
    monkeypatch.setattr(B, "input_hashes", lambda: {"raw_store_sha256": "r",
                                                    "registration_sha256_lf": "g",
                                                    "this_script_sha256_lf": "s"})
    monkeypatch.setattr(B, "gate_checks", lambda: {"fake": True})
    return calls


def test_full_flow_branch_c_writes_outputs(monkeypatch, tmp_path):
    ctl = p_with_auc(15)
    monkeypatch.setattr(B, "CONTROL_CEILING", C.auc_counts(ctl, Y)["exact"])
    calls = flow(monkeypatch, ctl, Y.astype(float), Y.astype(float))
    out = tmp_path / "o"
    res = B.main(["--out", str(out)])
    assert res["reading"]["branch"] == B.BRANCH_C
    assert [c[0] for c in calls] == ["fit", "cert", "fit", "fit"]        # control first
    assert calls[0][1] == 100.0 and calls[2][1] == 1.0 and calls[3][2] == C.STARTS_100
    md = (out / B.RESULT_MD).read_text(encoding="utf-8")
    assert B.BRANCH_C in md and md.isascii()
    js = json.loads((out / B.RESULT_JSON).read_text(encoding="utf-8"))
    assert js["result"]["reading"]["branch"] == B.BRANCH_C and js["stop"] is None
    with pytest.raises(SystemExit):                                        # never overwritten
        B.main(["--out", str(out)])


def test_full_flow_branch_d_and_b(monkeypatch, tmp_path):
    ctl = p_with_auc(15)
    monkeypatch.setattr(B, "CONTROL_CEILING", C.auc_counts(ctl, Y)["exact"])
    flow(monkeypatch, ctl, Y.astype(float), ctl)
    assert B.main(["--out", str(tmp_path / "d")])["reading"]["branch"] == B.BRANCH_D
    flow(monkeypatch, ctl, ctl, ctl)
    assert B.main(["--out", str(tmp_path / "b")])["reading"]["branch"] == B.BRANCH_B


def test_control_failure_stops_and_computes_nothing_else(monkeypatch, tmp_path, capsys):
    ctl = p_with_auc(15)
    calls = flow(monkeypatch, ctl, Y.astype(float), Y.astype(float))       # literal not patched
    with pytest.raises(SystemExit) as e:
        B.main(["--out", str(tmp_path / "o")])
    assert e.value.code == 1
    assert calls == [("fit", 100.0, None)]                                 # no cert, no ceil_1
    assert B.CONTROL_FAILED in capsys.readouterr().out
    assert (tmp_path / "o" / B.STOP_JSON).is_file() and not (tmp_path / "o" / B.RESULT_MD).exists()


def test_control_failure_on_tau_split_stops(monkeypatch, tmp_path):
    ctl = p_with_auc(15)
    monkeypatch.setattr(B, "CONTROL_CEILING", C.auc_counts(ctl, Y)["exact"])
    ctl2 = ctl.copy()
    ctl2[19:] = 0.5 + 5e-10                                                # within TAU of positives'
    ctl2[:19] = np.where(np.arange(19) < 15, 0.9, 0.5)                     # ties within TAU
    calls = flow(monkeypatch, ctl2, Y.astype(float), Y.astype(float))
    monkeypatch.setattr(B, "control_verdict", lambda a: (False, ["forced"]))
    with pytest.raises(SystemExit):
        B.main(["--out", str(tmp_path / "o")])
    assert calls == [("fit", 100.0, None)]


def test_wrong_block_refuses_before_fitting(monkeypatch, tmp_path):
    calls = flow(monkeypatch, p_with_auc(15), Y.astype(float), Y.astype(float))
    monkeypatch.setattr(B, "real_block_y", lambda: ~Y)
    with pytest.raises(SystemExit) as e:
        B.main(["--out", str(tmp_path / "o")])
    assert "registered 19" in str(e.value) and calls == []


def test_tripwire_catches_an_unstubbed_run(monkeypatch, tmp_path):
    """Pin, gate and inputs stubbed, but the fitters are not: the run reaches the tripwire."""
    monkeypatch.setattr(B, "pin_refusal", lambda: None)
    monkeypatch.setattr(B, "input_hashes", lambda: {})
    monkeypatch.setattr(B, "gate_checks", lambda: {})
    monkeypatch.setattr(B, "real_block_y", lambda: Y.copy())
    monkeypatch.setattr(B, "load_stored", lambda key: {"p": [0.0] * 40, "lam": 100.0})
    with pytest.raises(AssertionError, match="tripwire"):
        B.main(["--out", str(tmp_path / "o")])


def test_docstring_documents_utf8_and_texts_are_ascii():
    assert "PYTHONUTF8=1" in B.__doc__
    assert all(t.isascii() for t in B.BRANCH_TEXT.values())
