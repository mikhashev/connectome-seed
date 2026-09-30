"""Tests of symmetric_lambda_pair.py (registration docs/plans/2026-09-30-symmetric-lambda-pair-registration.md).

No test fits a block, searches a capacity, opens a pool or reads a real store. An autouse fixture (a)
forces the registration and prediction-commit pins to None, so nothing can start the real run, and
(b) trips every fitter, the cert search and any pool. The flow tests replace the seams of the script
(fit_at_A, cert_real_A, real_block_y_A, load_stored, load_verdicts, input_hashes, gate_checks,
pin_refusal, git_state) by stand-ins; the label functions are called only on hand-made verdict objects.

Run: PYTHONUTF8=1 timeout 200 tools/.venv/Scripts/python.exe -m pytest
results/genome/c6/checks/test_symmetric_lambda_pair.py -q
"""
import copy
import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

CHECKS = Path(__file__).resolve().parent
sys.path.insert(0, str(CHECKS))
import symmetric_lambda_pair as S  # noqa: E402

B1, C, K, H, R, KA = S.B1, S.C, S.K, S.H, S.R, S.KA


def _no(*a, **k):
    raise AssertionError("tripwire: a fit, a search, a pool or the run body was reached")


class NoPool:
    def __init__(self, *a, **k):
        raise AssertionError("tripwire: a process pool was opened")


@pytest.fixture(autouse=True)
def guard(monkeypatch):
    monkeypatch.setattr(S, "REGISTRATION_SHA256_LF_PINNED", None)
    monkeypatch.setattr(S, "PREDICTION_COMMIT_PINNED", None)
    monkeypatch.setattr(R, "cwd_refusal", lambda: None)
    for mod, names in (
            (S, ("fit_at_A", "cert_real_A")),
            (B1, ("fit_at", "cert_real")),
            (C, ("train_shortcut", "train_capturing", "train_full_path_fixed", "forced_block_fit",
                 "separator_fits", "bf_block_lambda1", "cert_search", "cert_task", "fit_task",
                 "run_groups", "_run", "_cw_group", "_cw_init")),
            (R, ("cert_fresh", "run_pool", "_run", "_rw_group", "_rw_init", "estimate")),
            (K, ("_fit_one", "_w_init", "degree_terms", "run_groups", "_w_group",
                 "train_fixed_lambda")),
            (KA, ("_w_init", "degree_terms", "run_groups", "_w_group", "train_fixed_lambda"))):
        for n in names:
            monkeypatch.setattr(mod, n, _no)
    for mod in (S, B1, C, R, K, KA, H):
        if hasattr(mod, "ProcessPoolExecutor"):
            monkeypatch.setattr(mod, "ProcessPoolExecutor", NoPool)


# ------------------------------------------------------------------------------------------
# Stand-ins.

def auc(exact, tau=None):
    return {"exact": exact, "tau": exact if tau is None else tau, "n_pairs": 1024, "levels": 30,
            "twice": 0, "ulp_sensitive": tau is not None and tau != exact}


def cert(frac="1/1", tau=None, agree=True):
    fr = Fraction(frac)
    return {"fraction": f"{fr.numerator}/{fr.denominator}", "exact": float(fr),
            "tau": float(fr) if tau is None else tau, "counts_agree": agree, "ulp_sensitive": False,
            "rerun_spread": 0.0, "n_pairs": 1024, "count_search": 0.0, "count_fraction": 0.0,
            "count_registered_auc": 0.0}


Y = np.zeros(64, bool)
Y[:32] = True


def p_with_auc(wins_first):
    """Scores on Y: the first `wins_first` positives above every negative, the rest below."""
    p = np.zeros(64)
    p[:32] = 0.1
    p[:wins_first] = 0.9
    p[32:] = 0.5
    return p


def make_rows(cb, p_P=(0.4795, 0.404, 0.2704, 0.2698, 0.2442), leg_s=False):
    rows = {}
    for k, pp in zip(("rule",) + KA.BF_KEYS, p_P):
        rows[k] = {"p_P": pp, "leg_S_passes": leg_s, "n_ge": 68, "n_valid_shuffles": 99,
                   "ceiling_block": 1.0, "ceiling_full": 0.63, "lambda_ko": 1.0,
                   "lambda_full": 1.0, "lambda_block": 1.0}
    rows["rule"]["ceiling_block"] = cb
    rows["rule"]["lambda_block"] = 100.0 if cb < 0.9 else 1.0
    rows["N1"] = {"p_P": 0.4, "leg_S_passes": False, "n_ge": 99, "n_valid_shuffles": 99,
                  "ceiling_block": 0.79, "ceiling_full": 0.63, "lambda_ko": None,
                  "lambda_full": None, "lambda_block": None}
    return rows


DL = {"leg_P": {"text": "0.75", "bracket_text": "(0.6, 0.75]"},
      "R": {"text": "0.75", "bracket_text": "(0.6, 0.75]"}, "family": {"text": "0.75"},
      "band": {"text": "[0.6, 0.75)"}, "curve_text": "0.5: 1/5, 1/5", "instrument": "hand-made"}
UR = {"renamed": False}


def make_summary(mod, cb, block_present=19, spa=0.71, p_P=None, leg_s=False):
    """A hand-made summary.json whose stored label is what the block's own label function gives
    on the stored ceiling_block (so the reading control passes on it)."""
    rows = make_rows(cb, **({} if p_P is None else {"p_P": p_P}), leg_s=leg_s)
    if mod is K:
        ev = K.read_label(rows, n_present=block_present, readable=spa is not None)
    else:
        ev = KA.read_label(rows)
    text = mod.label_text(ev["label"], DL, UR, ev["U_reasons"], cb)
    per = [{"lam_rule": 100.0 if i < 97 else 3.0, "lam_BF:1": 1.0, "lam_BF:2": 1.0,
            "lam_BF:3": 3.0, "lam_BF:4": None} for i in range(99)]
    return {"real": {"rows": rows, "label": ev["label"], "label_text": text,
                     "block_present": block_present, "smallest_passing_auc": spa,
                     "per_shuffle": per},
            "synthetic": {"limits": DL, "u_rule": UR}}


# ------------------------------------------------------------------------------------------
# Section 3.1: the reading tree of Object 1.

@pytest.mark.parametrize("c100,c100f", [(0.99, 0.99), (0.5, 0.5), (0.95, 0.5)])
def test_a_cert_below_cut_outranks_everything(c100, c100f):
    assert S.read_tree(cert("919/1024"), auc(c100), auc(c100f))["branch"] == S.BRANCH_A


def test_cert_exactly_at_nine_tenths_is_a_pass():
    assert S.cert_ok_of(cert("9/10")) is True
    assert S.cert_ok_of(cert("919/1024")) is False          # 0.8975


def test_b_a_would_fail_as_b_did():
    r = S.read_tree(cert(), auc(0.55), auc(0.55))
    assert r["branch"] == S.BRANCH_B and not r["qualified"] and r["flags"] == []
    assert "differs by the lambda choice, not shown to differ by the block" in r["text"]


def test_c_a_survives():
    r = S.read_tree(cert(), auc(0.97), auc(0.96))
    assert r["branch"] == S.BRANCH_C and not r["qualified"]
    assert "population analogy is weaker than assumed" in r["text"]


@pytest.mark.parametrize("q,f,direction", [
    (0.95, 0.85, "float < 0.90 <= quantised"),
    (0.85, 0.95, "quantised < 0.90 <= float (FF-quant direction)")])
def test_d_decoder_split_both_directions(q, f, direction):
    r = S.read_tree(cert(), auc(q), auc(f))
    assert r["branch"] == S.BRANCH_D and r["decoder_direction"] == direction
    assert direction in r["text"]


def test_d_is_not_read_when_cert_fails():
    assert S.read_tree(cert("1/2"), auc(0.95), auc(0.85))["branch"] == S.BRANCH_A


@pytest.mark.parametrize("x,branch,qualified", [
    (0.88, S.BRANCH_B, True), (0.879, S.BRANCH_B, False), (0.8999, S.BRANCH_B, True),
    (0.90, S.BRANCH_C, True), (0.92, S.BRANCH_C, True), (0.921, S.BRANCH_C, False),
    (0.9649, S.BRANCH_C, False)])
def test_rider_at_the_cut(x, branch, qualified):
    r = S.read_tree(cert(), auc(x), auc(x))
    assert r["branch"] == branch and r["qualified"] is qualified
    assert ("AT THE CUT" in r["text"]) is qualified


def test_rider_does_not_qualify_a_or_d():
    assert not S.read_tree(cert("1/2"), auc(0.89), auc(0.89))["qualified"]
    assert not S.read_tree(cert(), auc(0.91), auc(0.85))["qualified"]


def test_ulp_split_follows_exact_and_is_flagged():
    r = S.read_tree(cert(), auc(0.9047, tau=0.8997), auc(0.95))
    assert S.GATE_ULP_SPLIT in r["flags"] and "TAU_READING_DIFFERS" in r["flags"]
    assert r["branch"] == S.BRANCH_C and r["branch_tau"] == S.BRANCH_D
    r = S.read_tree(cert("1/1", tau=0.85), auc(0.95), auc(0.95))
    assert "CERT_ULP_SPLIT" in r["flags"] and r["branch"] == S.BRANCH_C
    assert r["branch_tau"] == S.BRANCH_A


def test_counts_disagree_flag_and_uv_diagnostic_carried():
    r = S.read_tree(cert(agree=False), auc(0.95), auc(0.95), uv_max=1.2e-15)
    assert "CERT_COUNTS_DISAGREE" in r["flags"] and r["uv_max_diagnostic"] == 1.2e-15
    assert S.read_tree(cert(), auc(0.95), auc(0.95))["flags"] == []


# ------------------------------------------------------------------------------------------
# Section 2: the control.

def test_control_literal_is_1024_over_1024():
    assert S.CONTROL_CEILING == 1.0 and S.CONTROL_TWICE == 2 * 1024
    assert S.N_PAIRS_A == 32 * 32 == 1024 and S.STARTS == 10


def test_control_verdict():
    ok, why = S.control_verdict(auc(1.0))
    assert ok and why == []
    ok, why = S.control_verdict(auc(0.9990234375))
    assert not ok and len(why) == 1
    ok, why = S.control_verdict(auc(1.0, tau=0.999))
    assert not ok and len(why) == 1
    assert not S.control_verdict({"exact": None, "tau": None})[0]


# ------------------------------------------------------------------------------------------
# Section 3.2: the substitution on hand-made verdict objects.

def test_b_at_stored_ceiling_reproduces_stored_label_and_reading_control_passes():
    sb = make_summary(K, 0.7744360902255639)
    assert sb["real"]["label"] == "U" and "failed fit" in sb["real"]["label_text"]
    ok, detail = S.reading_control(K, sb)
    assert ok and detail["text_equal"] and detail["p_P_rows_present"]


def test_b_substitution_gives_g_with_the_g_clause():
    sb = make_summary(K, 0.7744360902255639)
    lab = S.label_of(K, sb, 384 / 399)
    assert lab["label"] == "G" and lab["text"].startswith("G: not detected at the R level")
    assert "ceiling_block = 0.9624 >= 0.90" in lab["text"]
    assert lab["mechanism_description"].startswith("orthogonal")
    cl = S.deciding_clause(lab)
    assert cl.startswith("G clause: not R and not W") and "every p_P > 0.10" in cl
    assert "smallest: BF_4 0.2442" in cl and "gate is passed" in cl


def test_only_ceiling_block_is_replaced_and_input_is_not_mutated():
    sb = make_summary(K, 0.7744360902255639)
    before = copy.deepcopy(sb)
    lab = S.label_of(K, sb, 0.9624)
    assert sb == before
    diff = [(k, f) for k in lab["rows"] for f in lab["rows"][k]
            if lab["rows"][k][f] != sb["real"]["rows"][k][f]]
    assert diff == [("rule", "ceiling_block")]


def test_gate_boundary_on_the_substitution():
    sb = make_summary(K, 0.77)
    assert S.label_of(K, sb, 0.9)["label"] == "G"
    lab = S.label_of(K, sb, 0.8999999)
    assert lab["label"] == "U" and "failed fit" in lab["text"]
    assert S.deciding_clause(lab).startswith("U clause:")


def test_b_not_readable_precedes_the_gate():
    sb = make_summary(K, 0.77, spa=None)
    assert "not readable" in sb["real"]["label_text"]
    lab = S.label_of(K, sb, 0.99)
    assert lab["label"] == "U" and lab["text"].startswith("U: not readable")


def test_substitution_cannot_hide_a_low_p_P():
    sb = make_summary(K, 0.77, p_P=(0.4795, 0.404, 0.08, 0.2698, 0.2442))
    lab = S.label_of(K, sb, 0.99)
    assert lab["label"] == "U" and any("BF_2: p_P = 0.0800" in r for r in lab["U_reasons"])


def test_a_substitution_uses_a_own_label_function():
    sa = make_summary(KA, 1.0, block_present=32, spa=0.666)
    assert sa["real"]["label"] == "G"
    assert S.reading_control(KA, sa)[0]
    lab = S.label_of(KA, sa, 0.5)
    assert lab["label"] == "U" and lab["text"].startswith("U: failed fit")
    assert S.label_of(KA, sa, 0.93)["label"] == "G"
    # block A's function has no not-readable clause: an unreadable flag is ignored by A
    sa2 = make_summary(KA, 1.0, block_present=32, spa=None)
    assert S.label_of(KA, sa2, 0.99)["label"] == "G"


def test_r_reading_is_unaffected_by_the_substitution():
    sb = make_summary(K, 0.77, p_P=(0.001, 0.4, 0.4, 0.4, 0.4), leg_s=True)
    assert S.label_of(K, sb, 0.99)["label"] == "U"        # D1 candidates disagree (rule R, BF_1 not)


def test_reading_control_fails_on_a_wrong_stored_text_or_a_missing_p_P():
    sb = make_summary(K, 0.7744360902255639)
    sb["real"]["label_text"] = "U: something else"
    assert not S.reading_control(K, sb)[0]
    sb = make_summary(K, 0.7744360902255639)
    del sb["real"]["rows"]["BF:3"]["p_P"]
    assert not S.bf_rows_ok(sb["real"]["rows"]) and not S.reading_control(K, sb)[0]
    sb = make_summary(K, 0.7744360902255639)
    sb["real"]["label"] = "G"
    assert not S.reading_control(K, sb)[0]


def test_lambda_provenance_reports_the_stored_lambdas():
    sb = make_summary(K, 0.7744360902255639)
    lp = S.lambda_provenance(sb)
    assert lp["per_predictor_ko_full_block"]["rule"] == {"ko": 1.0, "full": 1.0, "block": 100.0}
    assert lp["leg_S_shuffle_fits_selected_lambda"]["rule"] == {"100": 97, "3": 2}
    assert lp["leg_S_shuffle_fits_selected_lambda"]["BF:4"] == {"none": 99}


def test_object2_pair_table_and_expected_label():
    sb, sa = make_summary(K, 0.7744360902255639), make_summary(KA, 1.0, 32, 0.666)
    o = S.reading_object2(sb, sa, 384 / 399, 0.55)
    assert o["B_at_lambda_1"]["label"] == "G" and o["B_at_lambda_1"]["as_expected"] is True
    assert o["A_at_lambda_100"]["label"] == "U"
    cells = {(t["block"], t["lambda_block"]): (t["gate_passed"], t["label"])
             for t in o["pair_table"]}
    assert cells == {("A", 1): (True, "G"), ("A", 100): (False, "U"),
                     ("B", 1): (True, "G"), ("B", 100): (False, "U")}
    o = S.reading_object2(sb, sa, 0.5, 0.95)
    assert o["B_at_lambda_1"]["as_expected"] is False and o["A_at_lambda_100"]["label"] == "G"


# ------------------------------------------------------------------------------------------
# The block A wiring: the swap and its restore (no fit).

def test_as_block_A_swaps_and_restores_including_on_error():
    saved = {n: getattr(K, n) for n in ("MASKS", "BLOCK_CELLS", "BLOCK", "N_BLOCK", "N_SOURCES",
                                        "N_TARGETS")}
    with S.as_block_A():
        assert K.MASKS is KA.MASKS and K.BLOCK_CELLS is KA.BLOCK_CELLS and K.BLOCK is KA.BLOCK
        assert (K.N_BLOCK, K.N_SOURCES, K.N_TARGETS) == (64, 8, 8)
        assert K.BLOCK_CELLS.shape == (64, 2) and int(K.MASKS["block"].sum()) == 64
    with pytest.raises(RuntimeError):
        with S.as_block_A():
            raise RuntimeError("boom")
    assert all(getattr(K, n) is v for n, v in saved.items())
    assert K.N_BLOCK == 40 and K.N_SOURCES == 5 and K.N_TARGETS == 8


def test_block_A_geometry_is_registered():
    assert len(KA.SOURCES) == len(KA.TARGETS) == 8 and KA.N_BLOCK == 64
    assert S.N_CELLS_A == 64 and S.CUT == 0.9 == K.GATE_CUT


# ------------------------------------------------------------------------------------------
# Refusals; the tripwire is live.

def test_tripwire_is_live():
    with pytest.raises(AssertionError, match="tripwire"):
        S.fit_at_A(1.0)
    with pytest.raises(AssertionError, match="tripwire"):
        S.cert_real_A(Y)
    with pytest.raises(AssertionError, match="tripwire"):
        C.train_shortcut(None, None, 1.0)
    with pytest.raises(AssertionError, match="tripwire"):
        C.cert_search(Y, C.CERT_BUDGET_REGISTERED)
    with pytest.raises(AssertionError, match="tripwire"):
        K._fit_one("real", "block", "rule", None)
    with pytest.raises(AssertionError, match="tripwire"):
        KA._w_group(None)
    with pytest.raises(AssertionError, match="tripwire"):
        C.ProcessPoolExecutor(2)
    with pytest.raises(AssertionError, match="tripwire"):
        R.run_pool()
    with pytest.raises(AssertionError, match="tripwire"):
        C._run()


def test_the_swap_is_restored_when_a_tripwire_fires_inside_it():
    with pytest.raises(AssertionError, match="tripwire"):
        S.cert_real_A(Y)
    assert K.N_SOURCES == 5 and K.N_BLOCK == 40


def test_pin_none_refuses_before_anything(tmp_path):
    with pytest.raises(SystemExit) as e:
        S.main(["--out", str(tmp_path / "o")])
    assert "not pinned" in str(e.value) and not (tmp_path / "o").exists()


def test_pin_mismatch_refuses(monkeypatch, tmp_path):
    monkeypatch.setattr(S, "REGISTRATION_SHA256_LF_PINNED", "0" * 64)
    monkeypatch.setattr(K, "sha256_lf", lambda p: "1" * 64)
    with pytest.raises(SystemExit) as e:
        S.main(["--out", str(tmp_path / "o")])
    assert "REFUSED" in str(e.value) and "pinned" in str(e.value)


def test_prediction_commit_none_refuses(monkeypatch, tmp_path):
    monkeypatch.setattr(S, "REGISTRATION_SHA256_LF_PINNED", "a" * 64)
    monkeypatch.setattr(K, "sha256_lf", lambda p: "a" * 64)
    with pytest.raises(SystemExit) as e:
        S.main(["--out", str(tmp_path / "o")])
    assert "prediction commit" in str(e.value)


def test_dirty_tree_refuses_and_records_nothing(monkeypatch, tmp_path):
    monkeypatch.setattr(S, "REGISTRATION_SHA256_LF_PINNED", "a" * 64)
    monkeypatch.setattr(S, "PREDICTION_COMMIT_PINNED", "HEAD")
    monkeypatch.setattr(K, "sha256_lf", lambda p: "a" * 64)
    monkeypatch.setattr(R, "prediction_commit_refusal", lambda pinned: None)
    monkeypatch.setattr(S, "git_state", lambda: ("deadbeef", "?? untracked.txt"))
    with pytest.raises(SystemExit) as e:
        S.main(["--out", str(tmp_path / "o")])
    assert "not empty" in str(e.value) and "untracked.txt" in str(e.value)
    assert not (tmp_path / "o").exists()


def test_clean_tree_passes_the_dirty_check(monkeypatch):
    monkeypatch.setattr(S, "git_state", lambda: ("deadbeef", ""))
    assert S.dirty_refusal() is None


@pytest.mark.parametrize("name", [S.RESULT_MD, S.RESULT_JSON, S.STOP_JSON])
def test_existing_output_is_never_overwritten(monkeypatch, tmp_path, name):
    monkeypatch.setattr(S, "pin_refusal", lambda: None)
    (tmp_path / name).write_text("x")
    with pytest.raises(SystemExit) as e:
        S.main(["--out", str(tmp_path)])
    assert "never overwrites" in str(e.value)
    assert (tmp_path / name).read_text() == "x"


def test_dry_run_fits_nothing(monkeypatch, tmp_path):
    monkeypatch.setattr(S, "input_hashes", lambda: {"fake": 1})
    r = S.main(["--dry-run", "--out", str(tmp_path / "o")])
    assert r["dry_run"] and "not pinned" in r["refusal"] and not (tmp_path / "o").exists()


# ------------------------------------------------------------------------------------------
# The flow, on stand-ins.

def flow(monkeypatch, ctl_p, p100, p100f, cert_value=None, calls=None, ctl_stored_p=None):
    calls = calls if calls is not None else []

    def fit_at_A(lam):
        calls.append(("fit", lam))
        first = lam == S.LAMBDA_REGISTERED_A
        return {"lambda": lam, "starts": 10, "p": list(map(float, ctl_p if first else p100)),
                "p_float": list(map(float, ctl_p if first else p100f)), "uv_max": 1.5e-15}

    def cert_real_A(y):
        calls.append(("cert",))
        return cert_value or cert()
    sb, sa = make_summary(K, 0.7744360902255639), make_summary(KA, 1.0, 32, 0.666)
    res = {"result": {"ceil_1": auc(384 / 399)}}
    stored_p = ctl_p if ctl_stored_p is None else ctl_stored_p
    monkeypatch.setattr(S, "pin_refusal", lambda: None)
    monkeypatch.setattr(S, "fit_at_A", fit_at_A)
    monkeypatch.setattr(S, "cert_real_A", cert_real_A)
    monkeypatch.setattr(S, "real_block_y_A", lambda: Y.copy())
    monkeypatch.setattr(S, "load_stored", lambda: {"p": list(map(float, stored_p)), "lam": 1.0})
    monkeypatch.setattr(S, "load_verdicts", lambda: (sb, sa, res))
    monkeypatch.setattr(S, "git_state", lambda: ("cafef00d" * 5, ""))
    monkeypatch.setattr(S, "input_hashes", lambda: {"raw_store_sha256": "r",
                                                    "registration_sha256_lf": "g",
                                                    "this_script_sha256_lf": "s"})
    monkeypatch.setattr(S, "gate_checks", lambda: {"fake": True})
    return calls


PERFECT = Y.astype(float)


def test_full_flow_branch_b_writes_outputs_with_git_record(monkeypatch, tmp_path):
    calls = flow(monkeypatch, PERFECT, p_with_auc(10), p_with_auc(10))
    out = tmp_path / "o"
    res = S.main(["--out", str(out)])
    assert res["reading"]["branch"] == S.BRANCH_B
    assert calls == [("fit", 1.0), ("cert",), ("fit", 100.0)]           # control first
    assert res["object2"]["B_at_lambda_1"]["label"] == "G"
    assert res["object2"]["A_at_lambda_100"]["label"] == "U"
    md = (out / S.RESULT_MD).read_text(encoding="utf-8")
    assert S.BRANCH_B in md and md.isascii() and "git HEAD: " + "cafef00d" * 5 in md
    assert "`git status --porcelain`: (empty)" in md and "Deciding clause: G clause" in md
    js = json.loads((out / S.RESULT_JSON).read_text(encoding="utf-8"))
    assert js["git_head"] == "cafef00d" * 5 and js["git_status_porcelain"] == ""
    assert js["inputs"]["git_head"] == js["git_head"] and js["stop"] is None
    assert js["result"]["uv_max_diagnostic"] == 1.5e-15
    with pytest.raises(SystemExit):                                       # never overwritten
        S.main(["--out", str(out)])


def test_full_flow_branch_c(monkeypatch, tmp_path):
    flow(monkeypatch, PERFECT, PERFECT, PERFECT)
    res = S.main(["--out", str(tmp_path / "o")])
    assert res["reading"]["branch"] == S.BRANCH_C
    assert res["object2"]["A_at_lambda_100"]["label"] == "G"


def test_full_flow_branch_d_and_a(monkeypatch, tmp_path):
    flow(monkeypatch, PERFECT, PERFECT, p_with_auc(10))
    assert S.main(["--out", str(tmp_path / "d")])["reading"]["branch"] == S.BRANCH_D
    flow(monkeypatch, PERFECT, PERFECT, PERFECT, cert_value=cert("919/1024"))
    assert S.main(["--out", str(tmp_path / "a")])["reading"]["branch"] == S.BRANCH_A


def test_control_failure_stops_and_computes_nothing_else(monkeypatch, tmp_path, capsys):
    calls = flow(monkeypatch, p_with_auc(30), PERFECT, PERFECT)          # control ceiling != 1.0
    with pytest.raises(SystemExit) as e:
        S.main(["--out", str(tmp_path / "o")])
    assert e.value.code == 1
    assert calls == [("fit", 1.0)]                                       # no cert, no ceil_100_A
    assert S.CONTROL_FAILED in capsys.readouterr().out
    assert (tmp_path / "o" / S.STOP_JSON).is_file() and not (tmp_path / "o" / S.RESULT_MD).exists()
    stop = json.loads((tmp_path / "o" / S.STOP_JSON).read_text(encoding="utf-8"))
    assert stop["git_head"] == "cafef00d" * 5 and stop["stop"].startswith(S.CONTROL_FAILED)


def test_control_failure_on_tau_split_stops(monkeypatch, tmp_path):
    calls = flow(monkeypatch, PERFECT, PERFECT, PERFECT)
    monkeypatch.setattr(S, "control_verdict", lambda a: (False, ["forced"]))
    with pytest.raises(SystemExit):
        S.main(["--out", str(tmp_path / "o")])
    assert calls == [("fit", 1.0)]


def test_p_bit_inequality_is_a_stop(monkeypatch, tmp_path, capsys):
    """Section 2 item 1: on A an AUC of 1.0 alone is weak, so p unequal to the store stops."""
    other = np.where(np.arange(64) < 32, 0.8, 0.1)                       # AUC 1.0, other levels
    calls = flow(monkeypatch, other, PERFECT, PERFECT, ctl_stored_p=PERFECT)
    with pytest.raises(SystemExit) as e:
        S.main(["--out", str(tmp_path / "o")])
    assert e.value.code == 1 and calls == [("fit", 1.0)]
    out = capsys.readouterr().out
    assert S.CONTROL_FAILED in out and "not bit-equal" in out


def test_wrong_block_refuses_before_fitting(monkeypatch, tmp_path):
    calls = flow(monkeypatch, PERFECT, PERFECT, PERFECT)
    monkeypatch.setattr(S, "real_block_y_A", lambda: np.ones(64, bool))
    with pytest.raises(SystemExit) as e:
        S.main(["--out", str(tmp_path / "o")])
    assert "registered 32 of 64" in str(e.value) and calls == []


def test_tripwire_catches_an_unstubbed_run(monkeypatch, tmp_path):
    """Pin, gate and inputs stubbed, but the fitters are not: the run reaches the tripwire."""
    monkeypatch.setattr(S, "pin_refusal", lambda: None)
    monkeypatch.setattr(S, "input_hashes", lambda: {})
    monkeypatch.setattr(S, "gate_checks", lambda: {})
    monkeypatch.setattr(S, "git_state", lambda: ("h", ""))
    monkeypatch.setattr(S, "real_block_y_A", lambda: Y.copy())
    monkeypatch.setattr(S, "load_stored", lambda: {"p": [0.0] * 64, "lam": 1.0})
    with pytest.raises(AssertionError, match="tripwire"):
        S.main(["--out", str(tmp_path / "o")])


def test_docstring_documents_utf8_and_texts_are_ascii():
    assert "PYTHONUTF8=1" in S.__doc__
    assert all(t.isascii() for t in S.BRANCH_TEXT.values())
