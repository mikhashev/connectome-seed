"""Tests of failed_fit_calibration.py (registration
docs/plans/2026-09-29-failed-fit-branch-calibration-registration.md, revision 1.8, section 14).

Fixtures only. No test fits on the real bank: every flow uses fixture degree terms (--fixture) and
a deterministic stand-in for the world fits (C.fit_task); the real fits here are block-only fits
on constructed 40-cell banks (seconds each). No test runs the registered calibration.

Run: PYTHONUTF8=1 tools/.venv/Scripts/python.exe -m pytest -p no:cacheprovider -v
results/genome/c6/checks/test_failed_fit_calibration.py
"""
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
import failed_fit_calibration as C  # noqa: E402

K, H = C.K, C.H
PY = sys.executable
Z = K.board_y("z")


# ------------------------------------------------------------------------------------------
# Stand-in fits for the flows.

def low_block_p(y, m=4):
    """p = 1 on the first m present cells, 0 elsewhere: 2 wins + ties = 400 + 20 m on 20/20."""
    y = np.asarray(y, bool)
    p = np.zeros(len(y))
    p[np.flatnonzero(y)[:m]] = 1.0
    return p


def make_fake(overrides=None):
    """A deterministic stand-in for fit_task. Knockout, full, permuted-ceiling and shuffle fits
    are uninformative (constant p), so no world reads R or W. Rule #2.1's block fit is low
    (240/400) on FC and FN1 and equals y on FN2; the separator's ceil_1 fits equal y; BF's block
    fits equal y. overrides: {(family, field): value} changes one field of FC's records."""
    ov = overrides or {}

    def fake(bk, mk, pk, bank):
        y = bank.exists[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]]
        base = bk.split("|")[0]
        fam = base.split(":")[1] if base.startswith("cal:") else "perm"
        low = fam in ("FC", "FN1") and "|" not in bk
        rec = {"y": y.tolist(), "secs": 0.0, "outside_density": float(bank.exists[~K.BLOCK].mean()),
               "score": {"existence": 0.5, "offset": float("nan"), "counts": float("nan"),
                         "sign": float("nan"), "sign_n": 0, "n_ne": int(y.sum())}}
        if mk == "sep":
            reg = low_block_p(y) if low else y.astype(float)
            out = {"grid": [100.0] if fam == "FC" else [1, 3, 10, 30, 100],
                   "lambda_c": 100.0 if low else 1.0, "reg_p": reg.tolist(),
                   "reg_float_p": reg.tolist(), "ceil1_p": y.astype(float).tolist(),
                   "ceil1_float_p": y.astype(float).tolist(),
                   "ceil1_s100_p": y.astype(float).tolist(),
                   "ceil1_s100_float_p": y.astype(float).tolist(), "y": y.tolist(), "secs": 0.0}
            for (f, field), val in ov.items():
                if f == fam and field in out:
                    out[field] = val(y) if callable(val) else val
            return out
        if mk == "blk1":
            return {"p": y.astype(float).tolist(), "lam": 1.0, "y": y.tolist(), "secs": 0.0}
        if mk == "block" and pk == "rule":
            p = low_block_p(y) if low else y.astype(float)
            lam = 100.0 if low else 1.0
            r = {**rec, "p": p.tolist(), "lam": lam}
            for (f, field), val in ov.items():
                if f == fam and field in ("block_p", "block_lam"):
                    r["p" if field == "block_p" else "lam"] = val(y) if callable(val) else val
            return r
        if mk == "block":
            return {**rec, "p": y.astype(float).tolist(), "lam": 1.0}
        lam = None if pk == "N1" else 3.0
        if mk == "ko1":
            lam = 1.0
        return {**rec, "p": [0.5] * K.N_BLOCK, "lam": lam}
    return fake


def fake_cert(key):
    y = C.pattern_of(key)
    Y = np.asarray(y, bool).reshape(5, 8)
    zs = np.array([K.Z_BLOCK[H.IDX[s]] for s in K.SOURCES])
    zt = np.array([K.Z_BLOCK[H.IDX[t]] for t in K.TARGETS])
    a, b, u, v = np.zeros(5), np.zeros(8), zs.astype(float), zt.astype(float)
    frac = C.SV["frac_count"](Y.astype(int), a, b, u, v)
    fr = Fraction(int(round(2 * frac)), 800)
    return {"n_pairs": 400, "count_search": frac, "count_fraction": frac,
            "count_registered_auc": frac, "counts_agree": True, "exact": float(fr),
            "fraction": f"{fr.numerator}/{fr.denominator}", "tau": float(fr),
            "registered_auc_exact": float(fr), "ulp_sensitive": False, "rerun_spread": 0.0,
            "reruns": [], "stages": {}, "budget": {}, "member": {"a": a.tolist(), "b": b.tolist(),
                                                                 "u": u.tolist(), "v": v.tolist()}}


FLOW_ARGS = ["--fixture", "--workers", "1", "--smoke-worlds", "1", "--smoke-shuffles", "2",
             "--smoke-perm-ceilings", "1", "--smoke-perm-ref", "1", "--cert-budget", "tiny"]


def flow_setup(patch, overrides=None, cert=None):
    patch(C, "fit_task", make_fake(overrides))
    patch(C, "cert_task", cert or fake_cert)
    patch(K, "tree_state", lambda: "")


def run_flow(tmp, patch, overrides=None, cert=None, extra=()):
    flow_setup(patch, overrides, cert)
    out = Path(tmp) / "run"
    return out, C.main(FLOW_ARGS + ["--out", str(out)] + list(extra))


# ------------------------------------------------------------------------------------------
# S-C11, S-C6 (the copy), S-C1, S-C2, section 5.

def test_SC11_seeds_pass_and_equal_literals():
    r = C.assert_seeds_cal(10)
    assert r["passed"], r
    assert {w["seed"] for w in C.world_specs_cal()} == C.LITERAL_WORLD_SEEDS


@pytest.mark.parametrize("bad", [{91000}, {5}, {30050}, {93130}, {20260929}, {93250}])
def test_SC11_a_colliding_seed_fails(monkeypatch, bad):
    """Fails if a cert seed that collides with B's, the shuffles, the ALS starts (with 100
    starts), an unused family index, a design seed or the permuted reference is not caught."""
    monkeypatch.setattr(C, "LITERAL_CERT_SEEDS", C.LITERAL_CERT_SEEDS | bad)
    monkeypatch.setattr(C, "SEED_CERT_DEEP", C.SEED_CERT_DEEP + tuple(bad))
    assert not C.assert_seeds_cal(10)["passed"]


def test_SC6_survey_copy_matches_pinned_file(monkeypatch):
    assert C.check_survey_copy()["passed"]
    monkeypatch.setattr(C, "SURVEY_SEARCH_SRC", C.SURVEY_SEARCH_SRC.replace("0.05", "0.06"))
    assert not C.check_survey_copy()["passed"]


def test_SC1_FC_world_equals_B_make_world():
    """The FC world is K.make_world's world for the same seed, board z and the Nf outside."""
    terms = C.FIXTURE_TERMS
    for j in (0, 3):
        spec = C.spec_cal("FC", j)
        a = C.make_world_cal(spec, terms)
        b = K.make_world({**spec, "family": "FC"}, terms)
        assert np.array_equal(a.exists, b.exists) and a.content == b.content


@pytest.mark.parametrize("fam,k", [("FN1", 1), ("FN2", 2)])
def test_SC2_FN_boards(fam, k):
    """Swaps keep 20/40, move exactly k cells each way, vary with the seed, and leave the
    outside as K.make_world draws it."""
    terms = C.FIXTURE_TERMS
    ys = []
    for j in range(5):
        spec = C.spec_cal(fam, j)
        y = C.world_block_y(spec)
        assert y.sum() == 20 and int((y & ~Z).sum()) == k and int((~y & Z).sum()) == k
        bank = C.make_world_cal(spec, terms)
        ref = K.make_world({**spec, "board": "z"}, terms)
        assert np.array_equal(bank.exists[~K.BLOCK], ref.exists[~K.BLOCK])
        assert np.array_equal(bank.exists[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]], y)
        ys.append(y.tobytes())
    assert len(set(ys)) > 1


def test_section5_planted_value_depends_only_on_k():
    rng = np.random.default_rng(1)
    for k in (0, 1, 2, 3):
        for _ in range(5):
            assert C.planted_value(C.fn_swap(Z, k, rng)) == C.planted_formula(k)
    assert [C.planted_formula(k) for k in (0, 1, 2)] == [1, Fraction(19, 20), Fraction(9, 10)]


# ------------------------------------------------------------------------------------------
# S-C12: tau, ulp_sensitive, the split.

def test_SC12_auc_counts_and_tau():
    y = np.array([1, 1, 0, 0], bool)
    p = np.array([np.nextafter(0.5, 1.0), 0.9, 0.5, 0.1])    # one 1-ulp win
    r = C.auc_counts(p, y)
    assert r["exact"] == K.auc(p, y) and r["ulp_sensitive"] and r["tau"] < r["exact"]
    q = np.array([0.9, 0.8, 0.2, 0.1])
    assert C.auc_counts(q, y)["exact"] == C.auc_counts(q, y)["tau"] == 1.0


def test_SC12_gate_ulp_split():
    """A 1-ulp split that puts the exact value at the cut and the tau value below it."""
    y = np.zeros(40, bool)
    y[:20] = True
    p = np.zeros(40)
    p[:20] = 1.0
    p[20:24] = 1.0                                     # 80 ties: 320 + 40 = 360 -> 0.90
    ex = C.auc_counts(p, y)
    assert ex["exact"] == 0.9 and not C.split_at_cut(ex)
    p2 = p.copy()
    p2[:20] = np.nextafter(1.0, 2.0)                   # the 80 ties become 1-ulp wins
    p2[20:28] = 1.0                                    # 8 absent at 1.0: 20*8 = 160 near-ties
    r = C.auc_counts(p2, y)
    assert r["exact"] >= 0.9 > r["tau"] and C.split_at_cut(r)


# ------------------------------------------------------------------------------------------
# Section 6: the separator table; section 7: the outcome labels; section 8: the gate options.

@pytest.mark.parametrize("args,row", [
    ((0.95, 1.0, 0.5, 0.5, 0.5, 0.5), "gate passed"),
    ((0.6, 0.85, 1.0, 1.0, 1.0, 1.0), "not separated"),
    ((0.6, 1.0, 1.0, 0.5, 0.95, 0.5), "fit failure, FF-sel; and FF-quant at lambda_c"),
    ((0.6, 1.0, 1.0, 0.5, 0.6, 0.5), "fit failure, FF-sel"),
    ((0.6, 1.0, 0.8, 0.92, 0.6, 0.5), "fit failure, FF-quant (at lambda = 1)"),
    ((0.6, 1.0, 0.8, 0.85, 0.6, 0.95), "fit failure, FF-struct or FF-opt, not separated; "),
    ((0.6, 1.0, 0.8, 0.85, 0.6, 0.5), "fit failure, FF-struct or FF-opt, not separated"),
    ((0.6, 0.9, 0.9, 0.5, 0.5, 0.5), "fit failure, FF-sel")])
def test_section6_separator_rows(args, row):
    got, _ = C.separator_reading(*args)
    assert got.startswith(row)
    if row == "fit failure, FF-sel":
        assert got == row


def _w(fam, met, reading, subk, cert=1.0, c1=1.0):
    return {"family": fam, "key": fam, "branch_met": met,
            "sep": {"reading": reading, "subkinds": subk, "cert": {"exact": cert},
                    "ceil_1": {"exact": c1}}}


def test_section7_outcome_labels():
    fc = [_w("FC", True, "fit failure, FF-sel", ["FF-sel"])]
    fn_met = _w("FN1", True, "fit failure, FF-sel", ["FF-sel"])
    fn_g = _w("FN2", False, "gate passed", [])
    assert C.outcome_labels(fc + [fn_met, fn_g], [])["labels"] == ["C1", "C6"]
    assert C.outcome_labels(fc + [fn_g], [])["labels"] == ["C2", "C6"]
    c3 = _w("FN1", True, "fit failure, FF-struct or FF-opt, not separated",
            ["FF-struct-or-FF-opt"], c1=0.8)
    assert C.outcome_labels(fc + [c3], [])["labels"] == ["C1", "C3", "C6"]
    assert C.outcome_labels(fc + [fn_g], ["a stop"])["labels"] == ["C5", "C6"]


def _ev(cbs, pP=0.5):
    rows = {pk: {"ceiling_block": cbs.get(pk, 1.0), "p_P": pP} for pk in ("rule",) + K.BF_KEYS}
    return {"label": "U", "label_before_readability": "U", "rows": rows, "readable": True,
            "reading_A_rule": {"letter": "-"}, "reading_B_BF1": {"letter": "-"}}


def test_section8_gate_options():
    ev = _ev({"rule": 0.6})                           # FC's row of section 8's table
    got = {o: C.label_under_option(ev, o) for o in C.GATE_OPTIONS}
    assert got == {"v-a": "U, failed fit", "v-b": "U (the D1 candidates disagree on the gate)",
                   "v-c": "G", "v-d": "U, failed fit"}
    ev = _ev({"BF:4": 0.5})
    assert C.label_under_option(ev, "v-a") == "G" and C.label_under_option(ev, "v-d") != "G"


# ------------------------------------------------------------------------------------------
# Real block-only fits on constructed banks (seconds): S-C4b, S-C3/A1, A2, S-C4a.

@pytest.fixture(scope="module")
def rule():
    H.STARTS = 10
    return H.load_rule(K.RULE_PATH)


@pytest.mark.parametrize("which", ["z", "FN1"])
def test_SC4b_shortcut_equals_full_path_bit_for_bit(rule, which):
    """Zcode's shortcut (no fold loop) against the full path at grid [1] (fold loop runs): the
    data arrays and the decoded p are identical bit for bit, on board z and on an FN board."""
    y = Z if which == "z" else C.world_block_y(C.spec_cal("FN1", 0))
    bank = C.constructed_bank(y, f"t.{which}")
    full = C.train_full_path_fixed(rule, bank, 1.0)
    short, ex = C.train_shortcut(rule, bank, 1.0)
    assert K.data_sha256(full) == K.data_sha256(short)
    pf = rule.decode(full, K.BLOCK_CELLS)["p_exist"]
    ps = rule.decode(short, K.BLOCK_CELLS)["p_exist"]
    assert np.array_equal(pf, ps)
    assert ex["lam"] == 1.0 and ex["inner_ll"] == {}


def test_SC3_A1_A2_FC_numbers_on_board_z(rule, monkeypatch):
    """FC's registered number (0.600000 = 240/400, lambda 100) through the forced K._fit_one, and
    ceil_1 = 1.0 exactly (A2), on the constructed z board (SURVEY fc_anchor_out.txt)."""
    monkeypatch.setitem(K._W, "rule", rule)
    bank = C.constructed_bank(Z, "t.z")
    rec = C.forced_block_fit("cal:FC:0", bank)
    cb = C.auc_counts(rec["p"], Z)
    assert rec["lam"] == 100.0 and cb["twice"] == C.FC_REGISTERED_TWICE_COUNT
    assert cb["exact"] == 0.6 and not cb["ulp_sensitive"]
    d1, _ = C.train_shortcut(rule, bank, 1.0)
    assert C.auc_counts(rule.decode(d1, K.BLOCK_CELLS)["p_exist"], Z)["exact"] == 1.0
    assert rule.fit.__globals__["LAMBDAS"] == list(H.BF_LAMBDAS)      # the swap was restored


def test_SC4a_capture_is_the_registered_fit(rule):
    """train_capturing returns the same data as P.train and the float fit of that very fit."""
    y = C.world_block_y(C.spec_cal("FN2", 1))
    bank = C.constructed_bank(y, "t.fn2")
    g = rule.fit.__globals__
    data, ex, lam = C.train_capturing(rule, bank, [100.0])
    with C.swapped_globals(g, LAMBDAS=[100.0]):
        ref = rule.train(bank, K.MASKS["block"])
    assert K.data_sha256(data) == K.data_sha256(ref) and lam == 100.0 == ex["lam"]
    assert g["fit_existence"].__name__ == "fit_existence"


def test_SC6_cert_search_tiny_budget():
    """The copied search on board z and an FN2 board: the three counts agree and reach the planted
    value; the Fraction value is the certificate."""
    for y, planted in ((Z, Fraction(1)), (C.world_block_y(C.spec_cal("FN2", 0)), Fraction(9, 10))):
        c = C.cert_search(y, C.CERT_BUDGET_TINY)
        assert c["counts_agree"] and Fraction(c["fraction"]) >= planted
        assert len(c["reruns"]) == 7


# ------------------------------------------------------------------------------------------
# Flows on fixtures (stand-in fits): outputs, refusals, stops.

def test_flow_completes_C1_with_sums(tmp_path, monkeypatch):
    out, res = run_flow(tmp_path, monkeypatch.setattr)
    assert res["completed"] and res["outcome"]["labels"] == ["C1", "C6"]
    fc = next(w for w in res["worlds"] if w["family"] == "FC")
    assert fc["label"] == "U" and fc["u_kind"] == "failed_fit" and fc["sep"]["reading"] == \
        "fit failure, FF-sel"
    assert not K.verify_sha256sums(out)
    names = {p.name for p in out.iterdir()}
    assert {"SHA256SUMS.txt", "calibration.json", "worlds.csv", "bf_block.csv",
            "permuted_reference.csv", "cert_members.json", "raw_fits.json.gz", "CALIBRATION.md",
            "stdout.log"} <= names
    header = (out / "worlds.csv").read_text(encoding="utf-8").splitlines()[0]
    assert header == ",".join(C.WORLDS_HEADER) and header.isascii()
    man = json.loads((out / "calibration.json").read_text(encoding="utf-8"))["manifest"]
    assert man["not_registered"].startswith(C.NOT_REGISTERED_TEXT)


@pytest.mark.parametrize("ov,needle", [
    ({("FC", "block_lam"): 3.0, ("FC", "block_p"): lambda y: y.astype(float) * 0 + 0.5},
     "(a) LAST_FIT lambda != 100"),
    ({("FC", "block_p"): lambda y: y.astype(float)}, "FC does not read failed fit"),
    ({("FC", "block_p"): lambda y: low_block_p(y, 5)}, "(c) not named by the registration"),
    ({("FC", "ceil1_p"): lambda y: low_block_p(y)}, "reproduction (A2) failed"),
    ({("FC", "reg_p"): lambda y: low_block_p(y, 5)}, "SCRIPT DEFECT")])
def test_section6_FC_stop_rows(tmp_path, monkeypatch, ov, needle):
    """Each FC stop row fires, the run exits 1, writes its outputs and stop_record.json, and no
    SHA256SUMS.txt."""
    with pytest.raises(SystemExit) as e:
        run_flow(tmp_path, monkeypatch.setattr, overrides=ov)
    assert e.value.code == 1
    out = tmp_path / "run"
    rec = json.loads((out / C.STOP_RECORD_NAME).read_text(encoding="utf-8"))
    assert needle in rec["stop"] and not (out / "SHA256SUMS.txt").exists()


def test_FC_stop_branch_b(tmp_path, monkeypatch):
    """Branch (b): the forcing acted (lambda 100) and the value is >= 0.90."""
    ov = {("FC", "block_p"): lambda y: y.astype(float)}
    with pytest.raises(SystemExit):
        run_flow(tmp_path, monkeypatch.setattr, overrides=ov)
    rec = json.loads((tmp_path / "run" / C.STOP_RECORD_NAME).read_text(encoding="utf-8"))
    assert "(b) the forcing acted and the value is >= 0.90" in rec["stop"]


def test_A3_cert_below_planted_stops_before_any_fit(tmp_path, monkeypatch):
    calls = []

    def low_cert(key):
        c = fake_cert(key)
        return {**c, "fraction": "1/2", "exact": 0.5}

    def no_fit(*a):
        calls.append(a)
        raise AssertionError("a fit was made")
    flow_setup(monkeypatch.setattr, cert=low_cert)
    monkeypatch.setattr(C, "fit_task", no_fit)
    monkeypatch.setattr(K, "degree_terms", no_fit)
    with pytest.raises(SystemExit):
        C.main(FLOW_ARGS + ["--out", str(tmp_path / "run")])
    rec = json.loads((tmp_path / "run" / C.STOP_RECORD_NAME).read_text(encoding="utf-8"))
    assert "(A3)" in rec["stop"] and not calls
    assert not (tmp_path / "run" / "SHA256SUMS.txt").exists()


def test_gate_refusals_leave_no_folder(tmp_path, monkeypatch):
    monkeypatch.setattr(K, "tree_state", lambda: "")
    out = tmp_path / "reg"
    with pytest.raises(SystemExit) as e:              # registered form, registration not pinned
        C.main(["--out", str(out)])
    assert "not pinned" in str(e.value.code) and not out.exists()
    monkeypatch.setattr(C, "REGISTRATION_SHA256_LF_PINNED",
                        K.sha256_lf(C.ROOT / C.REGISTRATION))
    monkeypatch.setattr(K, "tree_state", lambda: " M results/genome/c6/x.py")
    with pytest.raises(SystemExit) as e:              # registered form, dirty tree
        C.main(["--out", str(out)])
    assert "uncommitted" in str(e.value.code) and not out.exists()
    out.mkdir()
    with pytest.raises(SystemExit) as e:              # the folder exists before the run
        C.main(FLOW_ARGS + ["--out", str(out)])
    assert "exists" in str(e.value.code)
    monkeypatch.setattr(C, "B_SCRIPT_SHA256_LF", "0" * 64)
    with pytest.raises(SystemExit) as e:
        C.main(FLOW_ARGS + ["--out", str(tmp_path / "new")])
    assert "LF sha256" in str(e.value.code) and not (tmp_path / "new").exists()


def test_out_inside_a_reference_is_refused(tmp_path, monkeypatch):
    ref = tmp_path / "refB"
    monkeypatch.setattr(K, "PRERUN_DIR", ref)
    with pytest.raises(SystemExit) as e:
        C.main(FLOW_ARGS + ["--out", str(ref / "inside")])
    assert "reference folder" in str(e.value.code)


def test_dry_run_writes_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(K, "tree_state", lambda: "")
    r = C.main(["--dry-run", "--out", str(tmp_path / "x")])
    assert r["dry_run"] and not (tmp_path / "x").exists()
    assert any("not pinned" in s for s in r["gate"]["refusals_of_a_run"])


# ------------------------------------------------------------------------------------------
# Windows encoding: the output path with stdout redirected under a cp1252 strict environment.

def encoding_child(tmp):
    def patch(obj, name, value):
        setattr(obj, name, value)
    run_flow(tmp, patch)


def test_encoding_cp1252_redirected_stdout(tmp_path):
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    env.update(PYTHONUTF8="0", PYTHONIOENCODING="cp1252:strict")
    log = tmp_path / "child_stdout.txt"
    code = (f"import sys; sys.path.insert(0, {str(CHECKS)!r}); "
            f"import test_failed_fit_calibration as T; T.encoding_child({str(tmp_path)!r})")
    with open(log, "wb") as fh:
        p = subprocess.run([PY, "-c", code], stdout=fh, stderr=subprocess.PIPE, env=env,
                           cwd=str(C.ROOT), timeout=600)
    assert p.returncode == 0, p.stderr.decode("utf-8", "replace")[-3000:]
    out = tmp_path / "run"
    assert not K.verify_sha256sums(out)
    for f in ("stdout.log", "worlds.csv", "bf_block.csv", "permuted_reference.csv",
              "CALIBRATION.md", "calibration.json"):
        assert (out / f).read_bytes().isascii(), f
    assert log.read_bytes().isascii() and b"OUTCOME" in log.read_bytes()
    man = json.loads((out / "calibration.json").read_text(encoding="utf-8"))["manifest"]
    assert man["log_output_errors"] == 0
