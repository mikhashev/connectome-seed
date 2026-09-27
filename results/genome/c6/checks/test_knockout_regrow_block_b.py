"""Tests of knockout_regrow_block_b.py, block B on flyvis-65 (registration
docs/plans/2026-09-25-knockout-regrow-block-b-registration.md, revision 1.4.1, section 7: S1-S39).

Fixture banks and synthetic worlds only. No test reads block B's cells of the real bank, and no
test fits on the real bank (D3 (ii)): every flow puts a fixture bank in place of the real one
(K.real_bank), fixture degree terms in place of degree_terms (whose one fit is on the real bank),
and a deterministic stand-in for every fit (K._fit_one); check 8 (a C6 run on the real bank) is
stubbed. The one computation on the real bank is S6's: the section 1.4 table's hash from
presence OUTSIDE block B (as revision 1.3 recomputed it), of which only the hash, the inferable
count and the mirrors are compared; no count is printed.

T-A   copies of A's 17 label tests (test_knockout_regrow_labels.py), adapted to block B (S22).
S1-S39  one or more tests each, named test_S<nn>_...; each can fail (the docstring says how).

Run: PYTHONUTF8=1 tools/.venv/Scripts/python.exe -m pytest -p no:cacheprovider -v
results/genome/c6/checks/test_knockout_regrow_block_b.py
"""
import csv
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pytest

CHECKS = Path(__file__).resolve().parent
sys.path.insert(0, str(CHECKS))
import knockout_regrow_block_b as K  # noqa: E402

H = K.H
ROOT = K.ROOT
PY = sys.executable
REG = ROOT / K.REGISTRATION


# ------------------------------------------------------------------------------------------
# Fixtures shared by the flows.

FIX_TERMS = (-2.5, np.zeros(65), np.zeros(65))        # fixture degree terms (no real-bank fit)


def fake_fit_one(bk, mk, pk, bank):
    """A deterministic stand-in for a fit: p carries the block's labels plus noise seeded by the
    key; a hash-only fit hashes the knockout view (so check 6 sees exactly what a rule would); a
    ko1 record repeats its ko record at lambda = 1."""
    if mk.startswith("cv:"):
        return {"score": {"existence": 0.5}, "secs": 0.0}
    if "#hash" in mk:
        v = H.make_view(bank, K.MASKS["ko"])
        h = hashlib.sha256(v.cells.tobytes() + v.exists.tobytes()
                           + repr(sorted(v.content.items())).encode())
        return {"data_sha256": h.hexdigest(), "secs": 0.0}
    y = bank.exists[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]]
    base_mk = "ko" if mk == "ko1" else mk
    seed = int(hashlib.sha256(f"{bk}|{base_mk}|{pk}".encode()).hexdigest()[:8], 16)
    p = 0.3 * np.random.default_rng(seed).random(K.N_BLOCK) + 0.4 * y
    lam = None if pk == "N1" else (1.0 if mk == "ko1" or seed % 2 else 3.0)
    return {"p": p.tolist(), "y": y.tolist(), "lam": lam,
            "score": {"existence": 0.5, "offset": float("nan"), "counts": float("nan"),
                      "sign": float("nan"), "sign_n": 0, "n_ne": int(y.sum())},
            "outside_density": float(bank.exists[~K.BLOCK].mean()), "secs": 0.0}


def fixture_real_bank(n_present=None):
    """A fixture in place of the real bank: a synthetic world (fixture degree terms) whose block
    is replaced by a permutation of its 20/20 board, or by the first n_present cells present."""
    w = K.make_world(K.spec_of("M0.75", 0), FIX_TERMS)
    if n_present is None:
        return K.permute_block(w, np.random.default_rng(7).permutation(K.N_BLOCK), "fixture_real")
    content = {k: v for k, v in w.content.items() if not K.BLOCK[k]}
    for i, (s, t) in enumerate(K.BLOCK_CELLS.tolist()):
        if i < n_present:
            content[(s, t)] = {"offsets": {(0, 0): 1.0}, "hull": [], "sign": 1}
    return H.Bank("fixture_real", content)


def flow_setup(tmp, patch, real=None):
    """Patch the module for a flow on fixtures (patch(obj, name, value) is monkeypatch.setattr in
    a test, setattr in a subprocess): fake fits, a fixture real bank, fixture degree terms, a
    clean tree, check 8 stubbed, the registered sizes shrunk (2 shuffles, 1 permuted-block
    ceiling, 1 world per family), every requirement row met (the fake fits are not a science),
    the private root and the committed folder in tmp, the pre-data table registered from the
    fixture, and the row-and-column cache kept."""
    real = fixture_real_bank() if real is None else real
    patch(K, "_fit_one", fake_fit_one)
    patch(K, "real_bank", lambda: real)
    patch(K, "degree_terms", lambda: FIX_TERMS)
    patch(K, "tree_state", lambda: "")
    patch(K, "check_harness_identity", lambda a, terms: {"stub": True, "passed": True})
    patch(K, "N_SHUFFLES", 2)
    patch(K, "N_PERM_CEILINGS", 1)
    patch(K, "WORLDS_PER_FAMILY", 1)
    orig = K.two_world_check

    def met(worlds, repro):
        c = orig(worlds, repro)
        stop = repro["passed"] is False
        return {**c, "stop": stop, "passed": not stop}
    patch(K, "two_world_check", met)
    patch(K, "PRIVATE_ROOT", Path(tmp) / "private")
    patch(K, "OUT", Path(tmp) / "committed")
    patch(K, "PRERUN_DIR", Path(tmp) / "no_reference_here")
    t = K.pre_data_tables(real)
    patch(K, "ENDPOINTS_SHA256", t["endpoints_sha256"])
    patch(K, "INFERABLE_EXPECTED", t["inferable"])
    patch(K, "MIRRORS_EXPECTED", set(map(tuple, t["mirrors"])))
    return real


SYN_ARGS = ["--synthetic-only", "--starts", "10", "--workers", "1"]
ARM_ARGS = ["--arm", "flyvis65_blockB", "--starts", "10", "--workers", "1"]


def make_reference(tmp, patch):
    """A fixture reference: --synthetic-only (pre-run mode) into tmp/ref, then pinned by its own
    SHA256SUMS.txt, with the head and the script that wrote it (S17, S37)."""
    ref = Path(tmp) / "ref"
    K.main(SYN_ARGS + ["--out", str(ref)])
    sums = dict(reversed(ln.split(" *")) for ln in
                (ref / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines())
    man = json.loads((ref / "synthetic_only.json").read_text(encoding="utf-8"))["manifest"]
    patch(K, "PRERUN_DIR", ref)
    patch(K, "PRERUN_SHA256", sums)
    patch(K, "PRERUN_WORLDS_CSV_SHA256", sums["synthetic_worlds.csv"])
    patch(K, "PRERUN_GIT_HEAD", man["git_head"])
    patch(K, "PRERUN_SCRIPT_SHA256_LF", man["script_sha256_lf"])
    return ref


def rehearsal_child(tmp):
    """S26's child process: the real-arm path, end to end, on fixtures, under the caller's
    environment (PYTHONUTF8=0, PYTHONIOENCODING=ascii:strict, stdout redirected)."""
    def patch(obj, name, value):
        setattr(obj, name, value)
    flow_setup(tmp, patch)
    make_reference(tmp, patch)
    K.main(ARM_ARGS)


def run_rehearsal(tmp):
    """Runs rehearsal_child in a subprocess with a strict ASCII stdout redirected to a file."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    env.update(PYTHONUTF8="0", PYTHONIOENCODING="ascii:strict")
    out = Path(tmp) / "child_stdout.txt"
    code = (f"import sys; sys.path.insert(0, {str(CHECKS)!r}); "
            f"import test_knockout_regrow_block_b as T; T.rehearsal_child({str(tmp)!r})")
    with open(out, "wb") as fh:
        p = subprocess.run([PY, "-c", code], stdout=fh, stderr=subprocess.PIPE, env=env,
                           cwd=str(ROOT), timeout=900)
    return p, out


@pytest.fixture(scope="module")
def rehearsal(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("rehearsal")
    p, out = run_rehearsal(tmp)
    return {"tmp": tmp, "proc": p, "stdout": out, "private": tmp / "private",
            "committed": tmp / "committed"}


# ------------------------------------------------------------------------------------------
# T-A (S22): copies of A's 17 label tests, adapted to block B (seeds 91..., block B's CSV
# columns, no revision 3.2 rename check, block B's pre-run mode, four references in the guard).

def fake_worlds():
    """Dense-grid worlds shaped like A's pre-run table: gamma*_P = 0.6, gamma_R = 0.75."""
    labels = {"M0.5": "RGGGG", "M0.6": "RRUUU", "M0.75": "RRRRR", "M0.85": "RRRRR",
              "M1.0": "RRRRR"}
    seen = {"M0.5": 1, "M0.6": 3, "M0.75": 5, "M0.85": 5, "M1.0": 5}
    out = []
    for fam, labs in labels.items():
        for j, lab in enumerate(labs):
            p = 0.0001 if j < seen[fam] else 0.5
            rows = {pk: {"p_P": p, "auc": 0.8, "lambda_ko": 3.0} for pk in K.LIMIT_KEYS}
            out.append({"family": fam, "seed": 91000 + j, "label": lab, "rows": rows})
    return out


DL = K.detection_limits(fake_worlds(), 10)
U_KEPT = {"renamed": False}
U_RENAMED = {"renamed": True}
FAILED = f"U: {K.FAILED_FIT_TEXT}"
LEGS = "the legs disagree for rule #2.1: leg S n_ge = 0 of 99, leg P p_P = 0.0308"


def test_A01_fixture_limits():
    assert DL["leg_P"]["gamma"] == 0.6 and DL["R"]["gamma"] == 0.75


def test_A02_i_ceiling_block_reason_gives_failed_fit():
    assert K.label_text("U", DL, U_KEPT, [K.ceiling_block_reason(0.85)]) == FAILED
    assert K.label_text("U", DL, U_KEPT, [LEGS, K.ceiling_block_reason(0.85)]) == FAILED


def test_A03_ii_rename_never_applies_to_failed_fit():
    assert K.label_text("U", DL, U_RENAMED, [K.ceiling_block_reason(0.85)]) == FAILED
    assert K.label_text("U", DL, U_RENAMED, [LEGS, K.ceiling_block_reason(0.85)]) == FAILED


def test_A04_ii_not_measured_is_not_a_failed_fit():
    r = K.ceiling_block_reason(None)
    assert r == K.CEILING_BLOCK_NOT_MEASURED and "n/a" not in r and "below" not in r
    assert not r.startswith(K.CEILING_BLOCK_REASON)
    nm = f"U: {K.NOT_MEASURED_TEXT}"
    for u in (U_KEPT, U_RENAMED):
        assert K.label_text("U", DL, u, [r, LEGS]) == nm != FAILED
    assert K.label_text("U", DL, U_KEPT, [r, K.ceiling_block_reason(0.85)]) == FAILED


def test_A05_iii_threshold_u_without_the_reason():
    t = K.label_text("U", DL, U_KEPT, [LEGS])
    assert t == (f"U: {K.U_THRESHOLD} (at the leg-P detection limit gamma*_P = 0.6; "
                 f"transition band {DL['band']['text']})")
    assert K.FAILED_FIT_TEXT not in t
    assert K.label_text("U", DL, U_RENAMED, [LEGS]) == (
        f"U: {K.U_UNCALIBRATED}; never read as a finding")
    assert K.label_text("U", DL, U_KEPT, []).startswith(f"U: {K.U_THRESHOLD}")


def test_A06_iv_g_text():
    g = K.label_text("G", DL, U_KEPT, [], 1.0)
    gate = f"gate: rule #2.1's ceiling_block = 1.0000 >= {K.GATE_CUT:.2f}; "
    assert g == f"G: not detected at the R level above gamma_R ({gate}{K.limits_text(DL)})"
    assert g.replace(gate, "") == (
        f"G: not detected at the R level above gamma_R ({K.limits_text(DL)})")
    assert "leg P from gamma*_P = 0.6" in g and "weak" not in g
    assert K.label_text("G", DL, U_RENAMED, [K.ceiling_block_reason(0.5)], 1.0) == g


def test_A07_read_label_failed_fit_end_to_end():
    rows = {pk: {"leg_S_passes": False, "p_P": 0.5, "n_ge": 40, "n_valid_shuffles": 99,
                 "ceiling_block": 0.85 if pk == "rule" else 1.0, "ceiling_full": 0.95}
            for pk in K.PRED_KEYS}
    lab = K.read_label(rows)
    assert lab["label"] == "U"
    assert lab["U_reasons"] == [K.ceiling_block_reason(0.85)]
    assert lab["U_reasons"][0] == (f"rule #2.1's ceiling_block = 0.8500 is below {K.GATE_CUT:.2f}: "
                                   "the rule cannot hold the block even when trained on it alone")
    assert K.label_text(lab["label"], DL, U_RENAMED, lab["U_reasons"], 0.85) == FAILED
    rows["rule"]["ceiling_block"] = 1.0
    lab = K.read_label(rows)
    assert lab["label"] == "G"
    assert lab["mechanism_description"] == (
        f"no information (rule #2.1's ceiling_full = 0.9500 >= {K.MECHANISM_CUT:.2f})")


def _cut_texts():
    return {"mechanism": K.mechanism_description({"ceiling_full": 0.92}),
            "reason": K.ceiling_block_reason(0.85),
            "gate": K.label_text("G", DL, U_KEPT, [], 1.0)}


def test_A08_mechanism_description_names_rule_ceiling_full():
    assert K.mechanism_description({"ceiling_full": 0.5088}) == (
        f"orthogonal (rule #2.1's ceiling_full = 0.5088 < {K.MECHANISM_CUT:.2f})")
    assert K.mechanism_description({"ceiling_full": 0.92}) == (
        f"no information (rule #2.1's ceiling_full = 0.9200 >= {K.MECHANISM_CUT:.2f})")


def test_A09_probe_mechanism_cut_moves_only_the_mechanism_text(monkeypatch):
    before = _cut_texts()
    monkeypatch.setattr(K, "MECHANISM_CUT", 0.95)
    after = _cut_texts()
    assert after["mechanism"] != before["mechanism"]
    assert after["reason"] == before["reason"] and after["gate"] == before["gate"]


def test_A10_probe_gate_cut_moves_only_the_gate_texts(monkeypatch):
    before = _cut_texts()
    monkeypatch.setattr(K, "GATE_CUT", 0.95)
    after = _cut_texts()
    assert after["reason"] != before["reason"] and after["gate"] != before["gate"]
    assert f"is below {K.GATE_CUT:.2f}" in after["reason"]
    assert after["mechanism"] == before["mechanism"]


def test_A11_u_rule_counts_threshold_u_only():
    """A revision 3.3 (A3); S38: a not-readable U is counted apart too."""
    def worlds(reasons):
        return [{"family": "M0.6", "seed": 91160 + j, "label": "U", "U_reasons": r}
                for j, r in enumerate(reasons)]
    failed = worlds([[K.ceiling_block_reason(0.85)], [K.ceiling_block_reason(None)],
                     [K.not_readable_reason(1)]])
    ur = K.u_rule(failed)
    assert (ur["n_u_threshold"], ur["n_u_failed"], ur["n_u_not_measured"],
            ur["n_u_not_readable"]) == (0, 1, 1, 1)
    assert ur["renamed"] and ur["dense_grid_U"] == 3
    ur = K.u_rule(failed + worlds([[LEGS]]))
    assert ur["n_u_threshold"] == 1 and not ur["renamed"]


def _csv(rows):
    fh = io.StringIO(newline="")
    w = csv.writer(fh)
    w.writerow(K.WORLDS_CSV_HEADER)
    for r in rows:
        w.writerow([r[c] for c in K.WORLDS_CSV_HEADER])
    return fh.getvalue().encode("utf-8")


def _row(**kw):
    r = {c: "0.5" for c in K.WORLDS_CSV_HEADER}
    r.update(family="Nf", j=0, seed=91110, predictor="rule #2.1", label="G",
             mechanism_description="orthogonal (rule #2.1's ceiling_full = 0.5088 < 0.90)",
             D=0.123456789)
    r.update(kw)
    return r


def test_A12_csv_compare_outcomes():
    ref = _csv([_row()])
    same = K.csv_compare(ref, ref)
    assert same["outcome"] == 1 and same["passed"] and same["byte_identical"]
    mech = K.csv_compare(ref, _csv([_row(mechanism_description="other text")]))
    assert mech["outcome"] == 1 and mech["passed"] and not mech["byte_identical"]
    assert mech["mechanism_description_differences"] == 1
    assert "mechanism_description_explained_by_rename_3_2" not in mech    # S17: not carried
    tiny = K.csv_compare(ref, _csv([_row(D=0.123456789 + 5e-10)]))
    assert tiny["outcome"] == 2 and tiny["passed"] and "D" in tiny["continuous_within_tolerance"]
    big = K.csv_compare(ref, _csv([_row(D=0.123456789 + 1e-6)]))
    assert big["outcome"] == 3 and not big["passed"] and big["outcome_3_parts"] == ["b"]
    lat = K.csv_compare(ref, _csv([_row(p_P="0.0107")]))
    assert lat["outcome"] == 3 and lat["first_exact_differences"][0]["columns"] == ["p_P"]
    both = K.csv_compare(ref, _csv([_row(p_P="0.0107", D=0.123456789 + 1e-6)]))
    assert both["outcome_3_parts"] == ["a", "b"]
    assert K.csv_compare(ref, _csv([_row(label="U")]))["outcome"] == 3
    dup = K.csv_compare(ref, _csv([_row(), _row()]))
    assert dup["outcome"] == 3 and dup["n_duplicate_keys"] == 1


def test_A13_csv_compare_by_key():
    r1, r2 = _row(), _row(predictor="BF_1", D=0.5)
    ref = _csv([r1, r2])
    swapped = K.csv_compare(ref, _csv([r2, r1]))
    assert swapped["outcome"] == 1 and swapped["row_order_differs"]
    assert not K.csv_compare(ref, ref)["row_order_differs"]
    short = K.csv_compare(ref, _csv([r1]))
    assert short["outcome"] == 3 and short["rows_missing_now"] == [["Nf", "0", "91110", "BF_1"]]
    assert K.csv_compare(_csv([r1]), ref)["n_rows_missing_prerun"] == 1
    assert "layer (2) is not the cause" in K.repro_fail_treatment(["b"])


def test_A14_smallest_passing_auc_check():
    """Block B's values do not exist yet (B section 3.3): in pre-run mode the check reads its
    values from the boards' labels (board_smallest_passing_auc); one layout per board (D4 (i));
    a wrong or a missing value fails."""
    assert not K.check_prerun_files()["passed"]               # pre-run mode: no reference
    reg = K.board_smallest_passing_auc()
    entries = [{"world": "world:R:0", "board": "z", "y": K.board_y("z")},
               {"world": "world:No:0", "board": "z'", "y": K.board_y("z'")}]
    ok = K.check_smallest_passing_auc(entries, reg)
    assert ok["passed"] and ok["n_equal"] == 2
    wrong = K.check_smallest_passing_auc(entries, {"z": reg["z"], "z'": reg["z"] + 0.0025})
    assert not wrong["passed"] and [m["world"] for m in wrong["mismatches"]] == ["world:No:0"]
    missing = K.check_smallest_passing_auc(entries, {"z": reg["z"]})
    assert not missing["passed"] and missing["mismatches"][0]["registered"] is None


def test_A15_derive_smallest_passing_auc(tmp_path):
    def fixture(name, worlds):
        path = tmp_path / name
        path.write_text(json.dumps({"worlds": worlds}), encoding="utf-8")
        return K.derive_smallest_passing_auc(path)
    one = fixture("one.json", [{"seed": 1, "board": "z", "smallest_passing_auc": 0.5},
                               {"seed": 2, "board": "z'", "smallest_passing_auc": 0.75}])
    assert one["passed"] and one["by_board"] == {"z": 0.5, "z'": 0.75}
    two = fixture("two.json", [{"seed": 1, "board": "z", "smallest_passing_auc": 0.5},
                               {"seed": 2, "board": "z", "smallest_passing_auc": 0.625}])
    assert not two["passed"] and "board 'z' carries 2 values" in two["reason"]
    assert not fixture("none.json", [])["passed"]


def test_A16_ko1_count_control():
    ref = {("world:W:0", "ko1", "rule"): {"lam": 1.0},
           ("world:R:0", "ko1", "rule"): {"lam": 1.0, "reused_from_ko": True},
           ("world:R:0", "ko1", "BF:1"): {"lam": 3.0},
           ("world:R:0|sh:1", "ko", "rule"): {"lam": 1.0},
           ("real", "ko1", "rule"): {"lam": 1.0, "reused_from_ko": True}}
    reg = K.registered_ko1_count(ref)
    assert reg == {"ko1_records": 3, "copied_from_ko": 1, "fitted": 2}
    assert K.check_ko1_count(dict(reg), reg, comparable=True, reread=False)["passed"] is True
    other = {"ko1_records": 3, "copied_from_ko": 2, "fitted": 1}
    assert K.check_ko1_count(other, reg, comparable=True, reread=False)["passed"] is False
    assert K.check_ko1_count(other, reg, comparable=True, reread=True)["passed"] is None
    pre = K.check_ko1_count(other, None, comparable=True, reread=False, prerun=True)
    assert pre["passed"] is None and "pre-run mode" in pre["status"]


def test_A17_out_guard_on_four_references(tmp_path, monkeypatch):
    """S18: A's and the two male references by path and pins, block B's by path only."""
    refs, pin = {}, {}
    for name in ("A", "B", "L", "R"):
        d = tmp_path / f"ref_{name}"
        d.mkdir()
        (d / "synthetic_worlds.csv").write_bytes(f"reference {name}".encode())
        refs[name] = d
        pin[name] = {"synthetic_worlds.csv": hashlib.sha256(f"reference {name}".encode())
                     .hexdigest()}
    monkeypatch.setattr(K, "A_PRERUN_DIR", refs["A"])
    monkeypatch.setattr(K, "A_PRERUN_SHA256", pin["A"])
    monkeypatch.setattr(K, "PRERUN_DIR", refs["B"])
    monkeypatch.setattr(K, "PRERUN_SHA256", None)
    monkeypatch.setattr(K, "MALE_PRERUN_DIR", {"L": refs["L"], "R": refs["R"]})
    monkeypatch.setattr(K, "MALE_PRERUN_SHA256", {"L": pin["L"], "R": pin["R"]})
    assert K.out_dir_refusal(None) is None
    assert "with --arm" in K.out_dir_refusal(tmp_path / "new", arm="flyvis65_blockB")
    for d in refs.values():
        assert "reference folder or inside it" in K.out_dir_refusal(d)
        assert "reference folder or inside it" in K.out_dir_refusal(d / "sub")
    for name in ("A", "L", "R"):
        copy = tmp_path / f"copy_{name}"
        copy.mkdir()
        (copy / "synthetic_worlds.csv").write_bytes(f"reference {name}".encode())
        assert "byte copy" in K.out_dir_refusal(copy)
    copy_b = tmp_path / "copy_B"
    copy_b.mkdir()
    (copy_b / "synthetic_worlds.csv").write_bytes(b"reference B")
    assert K.out_dir_refusal(copy_b) is None                  # B: no pins yet, path only
    (tmp_path / "empty").mkdir()
    assert K.out_dir_refusal(tmp_path / "empty") is None     # B section 3.3 (a)


# ------------------------------------------------------------------------------------------
# S1-S22.

def test_S01_a_copy_beside_A_and_A_and_male_unchanged():
    """S1, D13 (i): block B's file exists beside A's; A's script and the male script are byte-
    unchanged against the registration's commit 3e5f2da."""
    assert Path(K.__file__).name == "knockout_regrow_block_b.py"
    p = subprocess.run(["git", "diff", "--quiet", "3e5f2da", "--",
                        "results/genome/c6/checks/knockout_regrow.py",
                        "results/genome/c6/checks/knockout_regrow_male_cns.py"], cwd=ROOT)
    assert p.returncode == 0


def test_S02_registrations_and_A_pin(monkeypatch):
    """S2: this registration and revision; A's LF sha256 after Amendment 1 is checked in every
    mode (a changed pin stops: "A changed"); the text of A's verdict is recorded."""
    assert K.REGISTRATION == "docs/plans/2026-09-25-knockout-regrow-block-b-registration.md"
    assert K.REGISTRATION_REVISION == "1.4.1"
    assert K.A_REGISTRATION_SHA256_LF_AMENDED == (
        "fc41505690365ff6d82fa618b00b482cc992bb36d708ed3b6fbbe6f54f96dbec")
    assert K.A_REGISTRATION_SHA256_LF_FLYVIS65 == (
        "409184dead0a8f9b971bd4b480043725d4a0d1a3c53c20c35734a944a63facd6")
    pins = K.check_pins()
    assert pins["a_registration_sha256_lf"] == K.A_REGISTRATION_SHA256_LF_AMENDED
    assert pins["pins"]["results/genome/bank/offsets.csv"].startswith("8c45e850")
    assert pins["pins"]["results/genome/bank/types.csv"].startswith("237a195a")
    assert pins["pins"]["results/genome/c6/harness.py"].startswith("6fc80952")
    assert K.quote_row("G").startswith("| **G: not detected at the R level above γ_R**")
    monkeypatch.setattr(K, "A_REGISTRATION_SHA256_LF_AMENDED", "0" * 64)
    with pytest.raises(SystemExit, match="A changed"):
        K.check_pins()


def test_S03_the_block():
    assert K.SOURCES == ("L1", "L2", "L3", "L4", "L5")
    assert K.TARGETS == ("Mi1", "Tm3", "Mi4", "Mi9", "Tm1", "Tm2", "Tm4", "Tm9")
    assert K.N_BLOCK == 40 == len(K.BLOCK_NAMES) == int(K.BLOCK.sum())
    assert K.BLOCK_NAMES[:3] == [("L1", "Mi1"), ("L1", "Tm3"), ("L1", "Mi4")]
    assert not (K.BLOCK & K.BLOCK_A).any() and int(K.BLOCK_A.sum()) == 64
    assert not hasattr(K, "BOARD") and not hasattr(K, "X_SIGN") and not hasattr(K, "W_SIGN")


def test_S04_six_strata():
    assert list(K.STRATA) == ["L1 x ON", "L1 x OFF", "L2 x ON", "L2 x OFF", "L3-L5 x ON",
                              "L3-L5 x OFF"]
    assert [len(v) for v in K.STRATA.values()] == [4, 4, 4, 4, 12, 12]
    assert not hasattr(K, "QUADRANTS")


def test_S05_training_cells():
    assert K.N_TRAIN_CELLS == 4185 and not hasattr(K, "N_TRAIN_PRESENT")


def test_S06_pre_data_table_hash_outside_block_B(monkeypatch):
    """S6 (D2 (ii)): the section 1.4 table's canonical hash, recomputed from presence OUTSIDE
    block B of the real bank (as revision 1.3 did), equals aa092028...f7705; 40 / 40 inferable;
    the 9 mirrors. Only the hash, the inferable count and the mirrors are compared; nothing is
    printed. In --synthetic-only the check returns no count; a wrong hash stops."""
    assert K.ENDPOINTS_SHA256 == ("aa0920288e6d38230c6a275c1690614120fdaf9104476264d42208ecf04f7705")
    real = K.real_bank()                                    # H.REAL, read outside block B only
    keep = K.endpoint_table(real)
    ok_hash = K.endpoint_table_sha256(keep) == K.ENDPOINTS_SHA256
    ok_inf = sum(keep[s][0] >= K.INFERABLE_MIN and keep[t][0] >= K.INFERABLE_MIN
                 for s, t in K.BLOCK_NAMES) == 40
    ex = real.exists & ~K.BLOCK
    ok_mir = {(t, s) for s, t in K.BLOCK_NAMES if ex[H.IDX[t], H.IDX[s]]} == K.MIRRORS_EXPECTED
    del keep, ex
    assert ok_hash and ok_inf and ok_mir and len(K.MIRRORS_EXPECTED) == 9
    t = {"endpoints_sha256": K.ENDPOINTS_SHA256, "inferable": 40,
         "mirrors": sorted(K.MIRRORS_EXPECTED), "endpoints": {"L1": [0, 0]},
         "training_present": 0}                             # a fixture of the check's input
    c = K.check_pre_data_tables(t, real_arm=False)
    assert c["passed"] and "endpoints" not in c and "training_present" not in c
    assert "endpoints" in K.check_pre_data_tables(t, real_arm=True)
    # the canonical form, in form only (B section 1.4): keys in sorted order, lists of ints
    keep = K.endpoint_table(fixture_real_bank())
    canon = json.dumps({"endpoints": keep}, sort_keys=True, separators=(",", ":"))
    assert canon.startswith('{"endpoints":{"L1":[') and list(json.loads(canon)["endpoints"]) == [
        "L1", "L2", "L3", "L4", "L5", "Mi1", "Mi4", "Mi9", "Tm1", "Tm2", "Tm3", "Tm4", "Tm9"]
    monkeypatch.setattr(K, "ENDPOINTS_SHA256", "0" * 64)
    with pytest.raises(SystemExit):
        K.check_pre_data_tables(t, real_arm=False)


def test_S07_check_2(monkeypatch):
    c = K.check_block_and_mask()
    assert c["training_cells"] == 4185 and c["block_A_cells_in_training"] == 64
    ko = K.MASKS["ko"].copy()
    ko[K.H.IDX["Mi1"], K.H.IDX["T4a"]] = False             # a block-A cell out of training
    monkeypatch.setitem(K.MASKS, "ko", ko)
    with pytest.raises(SystemExit, match="BLOCK OR MASK DIFFERS"):
        K.check_block_and_mask()


def test_S08_check_3_prints_and_stops_only_without_an_AUC(capsys):
    y = np.zeros(40, bool)
    y[[0, 5, 9, 17, 33]] = True
    c3 = K.check_block_print(y)
    assert c3["present"] == 5 and c3["has_auc"] and c3["strata"]["L1 x ON"] == "1 of 4"
    assert "check 3 (block print): present 5 of 40" in capsys.readouterr().out
    for k in (0, 40):
        yy = np.zeros(40, bool)
        yy[:k] = True
        with pytest.raises(SystemExit):
            K.check_block_print(yy)
        assert "BLOCK HAS NO AUC" in capsys.readouterr().out
    one = np.zeros(40, bool)
    one[3] = True
    assert K.check_block_print(one)["passed"]                  # 1 of 40: no stop (S38 reads it)


def test_S09_check_5_is_a_print():
    """S9 (D6 (i)): D(N1 logit) is printed with passed None and never stops, also when it is far
    from 0 (it cannot be 0 on a non-degenerate 5 x 8 block)."""
    bank = fixture_real_bank()
    n1 = H.fit_n1(H.make_view(bank, K.MASKS["ko"]))
    y = bank.exists[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]]
    c5 = K.check_n1_parity(n1, y)
    assert c5["passed"] is None and c5["D_N1_logit"] is not None
    assert "decides nothing" in c5["status"]


def test_S10_auc_function_with_an_unbalanced_40_cell_case():
    c = K.check_auc_function()
    assert c["hand_cases"][-1] == 0.9 and c["got"][-1] == 0.9 and c["rank_path"][-1] == 0.9


def test_S11_permutations():
    u = K.uniform_perms()
    assert u.shape == (9999, 40)
    rng = np.random.default_rng(91000)
    assert np.array_equal(u[0], rng.permutation(40)) and np.array_equal(u[1], rng.permutation(40))
    assert np.array_equal(K.perm_ceiling_perm(3), np.random.default_rng(91013).permutation(40))


def test_S12_row_and_column_on_5_x_8(capsys, monkeypatch):
    """S12: A's reshape(8, 8) raises on 40 labels; block B's null keeps the row and column counts
    on (5, 8); a nested pattern has one pattern ("n/a"); the cap stops (S39's record is tested
    below)."""
    with pytest.raises(ValueError):
        np.zeros(40, bool).reshape(8, 8)
    y = K.board_y("z")
    r = K.rc_patterns(y)
    assert r["status"] == "complete" and r["patterns"].shape == (9999, 40)
    P = r["patterns"].reshape(-1, 5, 8)
    Y = y.reshape(5, 8)
    assert (P.sum(2) == Y.sum(1)).all() and (P.sum(1) == Y.sum(0)).all()
    assert r["max_attempts"] <= K.RC_CAP_FACTOR * K.RC_SWAPS
    nested = np.array([[c <= r_ for c in range(8)] for r_ in range(5)]).ravel()
    assert not K.has_checkerboard(nested.reshape(5, 8))
    one = K.rc_patterns(nested)
    assert one["patterns"] is None and one["text"] == "n/a: the row-and-column null has one pattern"
    monkeypatch.setattr(K, "_RUN", {"folder": None, "arm": "t", "head": "h"})
    two = np.zeros(40, bool)
    two[[0, 9]] = True                                     # (0,0), (1,1): one swappable square
    with pytest.raises(SystemExit):
        K.rc_patterns(two, n_chains=20)
    assert "ROW-AND-COLUMN NULL: ATTEMPT CAP REACHED (chain " in capsys.readouterr().out


def test_S13_seeds(monkeypatch):
    s = K.assert_seeds_unique(10)
    assert s["new_seeds"] == 67 and s["world_seeds"] == [91100, 91184]
    assert (K.SEED_PERM, K.SEED_RC, K.SEED_PERM_CEIL, K.SEED_WORLD) == (91000, 91001, 91010, 91100)
    r = K.reserved_seeds(10)
    assert {90000, 90184, 92000, 92184, 92010} <= r
    monkeypatch.setattr(K, "SEED_PERM", 92000)                 # a male seed
    with pytest.raises(SystemExit, match="SEEDS NOT UNIQUE"):
        K.assert_seeds_unique(10)
    monkeypatch.setattr(K, "SEED_PERM", 90001)                 # an A seed
    with pytest.raises(SystemExit, match="SEEDS NOT UNIQUE"):
        K.assert_seeds_unique(10)


def test_S14_worlds_20_of_40_and_the_exact_half_of_No():
    """S14 (D4, D5): both boards hold 20 of 40, each L row 4 of 8; the No world's pure z score
    has AUC exactly 0.5 under board z'; W's rank-1 z1 scores board z at exactly 0.5; 52 others;
    make_world sets the board (asserted 20)."""
    z, zp = K.board_y("z"), K.board_y("z'")
    assert int(z.sum()) == int(zp.sum()) == 20
    assert (z.reshape(5, 8).sum(1) == 4).all() and (zp.reshape(5, 8).sum(1) == 4).all()
    score_z = np.outer(K.Z_BLOCK, K.Z_BLOCK)[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]]
    assert K.auc(score_z, zp) == 0.5
    score_z1 = np.outer(K.ZPRIME, K.ZPRIME)[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]]
    assert K.auc(score_z1, z) == 0.5
    assert K.auc(score_z, z) == 1.0
    assert len(K.OTHERS) == 52
    zs = [K.Z_BLOCK[K.H.IDX[s]] for s in K.SOURCES]
    assert zs == [1, -1, 1, -1, 1]
    zps = [K.ZPRIME[K.H.IDX[s]] for s in K.SOURCES]
    assert zps == [1, 1, -1, -1, 1]
    for fam in ("R", "No", "W"):
        w = K.make_world(K.spec_of(fam, 0), FIX_TERMS)
        assert int(w.exists[K.BLOCK].sum()) == 20
        y = w.exists[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]]
        assert np.array_equal(y, zp if fam == "No" else z)


def test_S15_precision_and_columns():
    y = np.zeros(40, bool)
    y[:4] = True
    p = np.linspace(1, 0, 40)
    assert K.precision_at_n_present(p, y) == 1.0
    assert K.precision_at_n_present(p[::-1], y) == 0.0
    assert K.precision_at_n_present(p, np.zeros(40, bool)) is None
    assert "precision_at_n_present" in K.WORLDS_CSV_HEADER and "auc_other_31" in K.CSV_FIELDS
    assert "precision_at_32" not in K.WORLDS_CSV_HEADER and len(K.WORLDS_CSV_HEADER) == 33


def test_S16_smallest_passing_auc_grid():
    assert "k / (n_p n_a)" in K.smallest_passing_auc.__doc__
    perms = K.uniform_perms()
    for k in (0, 40):
        y = np.zeros(40, bool)
        y[:k] = True
        assert K.smallest_passing_auc(y, y[perms]) is None
    y = K.board_y("z")
    a = K.smallest_passing_auc(y, y[perms])
    assert a is not None and round(a * 400) == a * 400          # on the grid k / 400


def test_S17_prerun_placeholders_and_the_real_arm_refuses():
    assert K.PRERUN_SHA256 is None and K.PRERUN_WORLDS_CSV_SHA256 is None
    assert K.PRERUN_GIT_HEAD is None and K.PRERUN_SCRIPT_SHA256_LF is None
    assert str(K.PRERUN_DIR).endswith("synthetic_blockB_prerun")
    assert not K.reference_mode()
    assert set(K.placeholders_unset()) == {"PRERUN_SHA256", "PRERUN_WORLDS_CSV_SHA256",
                                          "PRERUN_GIT_HEAD", "PRERUN_SCRIPT_SHA256_LF"}
    with pytest.raises(SystemExit, match="still placeholders"):
        K.main(["--arm", "flyvis65_blockB"])
    assert not hasattr(K, "_mech_renamed_32") and not hasattr(K, "PRERUN_REV2_FAMILIES")
    ref = {("world:R:0", "ko", "rule"): {"p": [0.1] * 40, "y": [True] * 40, "lam": 1.0},
           ("world:R:0|sh:0", "ko", "rule"): {"p": [0.1] * 40, "y": [True] * 40, "lam": 1.0}}
    d = K.raw_fits_diagnostic({}, ref=ref)
    assert set(d["kinds"]) == {"ko", "sh"} and d["total"]["missing_now"] == 2


def test_S19_S20_S21_names():
    assert K.OUT.name == "knockout_regrow_block_b"
    assert K.private_run_dir("flyvis65_blockB", "a" * 40).name.startswith("flyvis65_blockB_")
    assert "about 2.7 of 40 cells" in K.WITHIN_FLY_NOTE
    with pytest.raises(SystemExit):
        K.main(["--arm", "flyvis65"])                          # A's arm name is not B's


# ------------------------------------------------------------------------------------------
# S23-S39.

def test_S23_utf8_at_the_top(tmp_path):
    """S23: import and a print of A's quoted G row (it holds gamma) with PYTHONUTF8=0 and
    PYTHONIOENCODING=cp1252:strict, stdout redirected: exit 0, UTF-8, gamma present. Without the
    reconfigure at the top the print raises UnicodeEncodeError (cp1252 has no gamma)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    env.update(PYTHONUTF8="0", PYTHONIOENCODING="cp1252:strict")
    out = tmp_path / "o.txt"
    code = (f"import sys; sys.path.insert(0, {str(CHECKS)!r}); "
            "import knockout_regrow_block_b as K; print(K.quote_row('G'))")
    with open(out, "wb") as fh:
        p = subprocess.run([PY, "-c", code], stdout=fh, stderr=subprocess.PIPE, env=env,
                           cwd=str(ROOT))
    assert p.returncode == 0, p.stderr.decode("utf-8", "replace")
    text = out.read_bytes().decode("utf-8")
    assert "γ" in text and text.startswith("| **G: not detected")


class _Raising:
    """A console whose write raises UnicodeEncodeError (the male arm's run 1)."""
    encoding = "ascii"

    def write(self, s):
        raise UnicodeEncodeError("ascii", str(s), 0, 1, "fixture")

    def flush(self):
        pass


def test_S24_log_cannot_kill_a_run(tmp_path, monkeypatch):
    monkeypatch.setitem(K._LOG, "output_errors", 0)
    monkeypatch.setitem(K._LOG, "buffer", [])
    fh = K.tee_to(tmp_path / "stdout.log")
    try:
        K.log("γ", stream=_Raising())                         # returns, never raises
        monkeypatch.setattr(sys, "stdout", _Raising())
        K.log("second γ")
    finally:
        monkeypatch.undo()
        K.untee()
    text = (tmp_path / "stdout.log").read_text(encoding="utf-8")
    assert "γ\n" in text and "second γ" in text
    assert fh.closed


def test_S24_counter(monkeypatch):
    monkeypatch.setitem(K._LOG, "output_errors", 0)
    monkeypatch.setitem(K._LOG, "buffer", [])
    K.log("γ", stream=_Raising())
    assert K._LOG["output_errors"] == 1


def test_S25_synthetic_outputs_before_the_tables_synthetic_only(tmp_path, monkeypatch):
    """S25 (revision 1.3), --synthetic-only: print_synthetic raises on its first call; the
    synthetic outputs exist and hold every world. Under the male order (print before write)
    nothing would be written."""
    flow_setup(tmp_path, monkeypatch.setattr)

    def boom(syn):
        raise RuntimeError("print_synthetic patched to raise")
    monkeypatch.setattr(K, "print_synthetic", boom)
    out = tmp_path / "out"
    with pytest.raises(RuntimeError):
        K.main(SYN_ARGS + ["--out", str(out)])
    for n in ("raw_fits.json.gz", "synthetic_only.json", "synthetic_worlds.csv"):
        assert (out / n).is_file(), n
    so = json.loads((out / "synthetic_only.json").read_text(encoding="utf-8"))
    assert len(so["worlds"]) == len(K.FAMILIES)
    keys = {k[0] for k in K.read_raw(out / "raw_fits.json.gz")}
    assert {f"world:{f[0]}:0" for f in K.FAMILIES} <= keys
    assert not (out / "SHA256SUMS.txt").exists()                # a stopped run: no sums


def test_S25_real_fits_and_verdict_on_disk_before_any_print(tmp_path, monkeypatch):
    """S25: in the real arm, print_synthetic raising leaves the synthetic outputs in the private
    folder; log raising on its first call after the real fits leaves raw_fits_real.json.gz and
    verdict.json, whose line equals the unpatched run's."""
    flow_setup(tmp_path, monkeypatch.setattr)
    make_reference(tmp_path, monkeypatch.setattr)
    full = K.main(ARM_ARGS)
    want = full["real"]["verdict_line"]
    # the real fits and verdict
    monkeypatch.setattr(K, "PRIVATE_ROOT", tmp_path / "private2")
    armed = {"on": False}
    ev0, log0 = K.evaluate_bank, K.log

    def ev(base_key, *a, **k):
        r = ev0(base_key, *a, **k)
        if base_key == "real":
            armed["on"] = True
        return r

    def log(*a, **k):
        if armed["on"]:
            raise RuntimeError("log patched to raise after the real fits")
        return log0(*a, **k)
    monkeypatch.setattr(K, "evaluate_bank", ev)
    monkeypatch.setattr(K, "log", log)
    with pytest.raises(RuntimeError):
        K.main(ARM_ARGS)
    private = next((tmp_path / "private2").iterdir())
    assert (private / "raw_fits_real.json.gz").is_file()
    v = json.loads((private / "verdict.json").read_text(encoding="utf-8"))
    assert v["verdict_line"] == want and v["quoted_row"].startswith("| **")
    assert not (private / "SHA256SUMS.txt").exists()
    # the synthetic step in the real arm
    monkeypatch.setattr(K, "log", log0)
    monkeypatch.setattr(K, "evaluate_bank", ev0)
    monkeypatch.setattr(K, "PRIVATE_ROOT", tmp_path / "private3")

    def boom(syn):
        raise RuntimeError("print_synthetic patched to raise")
    monkeypatch.setattr(K, "print_synthetic", boom)
    with pytest.raises(RuntimeError):
        K.main(ARM_ARGS)
    private = next((tmp_path / "private3").iterdir())
    for n in ("raw_fits.json.gz", "synthetic_only.json", "synthetic_worlds.csv"):
        assert (private / n).is_file(), n


def test_S26_ascii_rehearsal_of_the_real_arm(rehearsal):
    """S26: the end of the real-arm path on a fixture bank, in a subprocess with PYTHONUTF8=0,
    PYTHONIOENCODING=ascii:strict and stdout redirected: exit 0; RESULT.md holds A's quoted row
    with gamma in UTF-8; the sums verify (S29)."""
    p = rehearsal["proc"]
    assert p.returncode == 0, p.stderr.decode("utf-8", "replace")[-3000:]
    md = (rehearsal["committed"] / "RESULT.md").read_text(encoding="utf-8")
    assert md.startswith("# Knock out and regrow: block B on flyvis-65")
    assert "> | **" in md and "γ" in md
    assert K.BLOCK_B_HEADER_LINE in md
    out = rehearsal["stdout"].read_bytes().decode("utf-8")
    assert "VERDICT: " in out


def test_S27_earlier_runs_three_outcomes(tmp_path, monkeypatch):
    arm = "flyvis65_blockB"
    miss = K.find_earlier_runs(tmp_path / "nope", arm)
    assert miss["outcome"] == "missing" and miss["text"].startswith("root does not exist: ")
    root = tmp_path / "root"
    root.mkdir()
    zero = K.find_earlier_runs(root, arm)
    assert zero["outcome"] == "read" and "; 0 found" in zero["text"] and zero["folders"] == []
    assert f"folders `{arm}_*`" in zero["text"]
    run = root / f"{arm}_20260101T000000Z_abcdef123456"
    run.mkdir()
    (root / f"{arm}_20260102T000000Z_nomarker0000").mkdir()   # no marker: not a started arm
    (run / K.REAL_ARM_MARKER).write_text("{}", encoding="utf-8")
    one = K.find_earlier_runs(root, arm)
    assert one["folders"] == [run.name] and f"1 found: {run.name}" in one["text"]

    def denied(self):
        raise PermissionError("fixture: cannot list")
    monkeypatch.setattr(Path, "iterdir", denied)
    bad = K.find_earlier_runs(root, arm)
    assert bad["outcome"] == "unreadable" and "cannot be read" in bad["text"]
    for r in (miss, bad):
        assert "0 found" not in r["text"] and r["folders"] is None


def test_S27_no_unmeasurable_status_word():
    """S27: no output text constant of the script holds the word the male RESULT.md printed from
    a constant (a status the run cannot measure)."""
    src = Path(K.__file__).read_text(encoding="utf-8")
    assert not re.search(r"\bintact\b", src, flags=re.IGNORECASE)


def test_S27_the_real_arm_records_the_search(rehearsal):
    s = json.loads((rehearsal["committed"] / "summary.json").read_text(encoding="utf-8"))
    er = s["manifest"]["earlier_real_arm_runs"]
    assert er["outcome"] in ("missing", "read")
    md = (rehearsal["committed"] / "RESULT.md").read_text(encoding="utf-8")
    assert f"Earlier real-arm runs of this arm (S27): {er['text']}." in md
    private = next(rehearsal["private"].iterdir())
    assert (private / K.REAL_ARM_MARKER).is_file()


def _env_child(tmp_path, extra):
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    env.update(extra)
    code = (f"import sys, json; sys.path.insert(0, {str(CHECKS)!r}); "
            "import knockout_regrow_block_b as K; print(json.dumps(K.command_environment()))")
    p = subprocess.run([PY, "-c", code], capture_output=True, env=env, cwd=str(ROOT))
    assert p.returncode == 0, p.stderr.decode("utf-8", "replace")
    return json.loads(p.stdout.decode("utf-8").strip().splitlines()[-1])


def test_S28_command_environment(tmp_path):
    e = _env_child(tmp_path, {"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"})
    assert e["PYTHONUTF8"] == "1" and e["PYTHONIOENCODING"] == "utf-8"
    assert set(e["thread_env"]) == set(K.THREAD_VARS) and "argv" in e
    assert e["stdout_encoding"] and "stream_encoding_found_at_import" in e
    e0 = _env_child(tmp_path, {})
    assert e0["PYTHONUTF8"] is None and e0["PYTHONIOENCODING"] is None
    assert e0["PYTHONHASHSEED"] is None


def test_S29_sums_last_and_verified(rehearsal):
    """S29: every SHA256SUMS.txt the rehearsal wrote verifies, stdout.log included (it holds the
    run's last line, so nothing was logged after the sums)."""
    private = next(rehearsal["private"].iterdir())
    for d in (private, rehearsal["committed"], rehearsal["tmp"] / "ref"):
        assert K.verify_sha256sums(d) == [], d
    names = (private / "SHA256SUMS.txt").read_text(encoding="utf-8")
    assert "*stdout.log" in names
    assert "wall-clock" in (private / "stdout.log").read_text(encoding="utf-8").splitlines()[-1]


def _ev(label, reasons=(), readable=True):
    return {"label": label, "U_reasons": list(reasons), "readable": readable,
            "rows": {"N1": {"p_P": 0.1234}}}


def test_S30_conditional_texts():
    """S30: each conditional text is printed only under its condition (table-driven over the
    four labels and the U kinds) or states its condition."""
    ur = {"n_u_threshold": 2}
    cases = [(_ev("R"), set()), (_ev("W"), set()), (_ev("G"), {"a_literals"}),
             (_ev("U", [LEGS]), {"a_literals", "additive_channel_note", "n1_p_P"}),
             (_ev("U", [K.ceiling_block_reason(0.5)]),
              {"a_literals", "failed_fit_reading", "additive_channel_note", "n1_p_P"}),
             (_ev("U", [K.not_readable_reason(1)], readable=False),
              {"a_literals", "additive_channel_note", "n1_p_P"})]
    for ev, want in cases:
        got = dict(K.conditional_lines(ev, DL, ur, 40))
        assert set(got) == want, (ev["label"], set(got))
        if "a_literals" in got:
            assert got["a_literals"].startswith("Block A's literal")
        if "failed_fit_reading" in got:
            assert "a failed fit or a rank limit, not separated" in got["failed_fit_reading"]
        if "n1_p_P" in got:
            assert got["n1_p_P"].endswith("0.1234") and "beside this U" in got["n1_p_P"]
        if "additive_channel_note" in got:
            assert "Beside this U" in got["additive_channel_note"]
    nr = dict(K.conditional_lines(cases[-1][0], DL, ur, 40))["a_literals"]
    assert "not readable" in nr
    assert K.a_literals_line(_ev("G"), DL, ur, 40).count("40/40 inferable") == 1


SECTION_3_5_VALUE = {
    "strata_means": lambda real: [f"{real['rows']['rule']['strata_mean_p'][k]:.3f}"
                                  for k in K.STRATA],
    "precision_at_n_present": lambda real: [K.fmt(real["rows"]["rule"]["precision_at_n_present"],
                                                  3)],
    "mirror_partners": lambda real: [f"{v:.3f}" for v in
                                     real["rows"]["rule"]["mirror_partners_p"].values()],
    "auc_other_31": lambda real: [K.fmt(real["rows"]["rule"]["auc_other_31"])],
    "per_type": lambda real: [K.fmt(real["rows"]["rule"]["per_type_auc"][n], 2)
                              for n in K.SOURCES + K.TARGETS],
    "perm_ceilings": lambda real: [K.fmt(x, 3) for x in real["perm_ceilings_full_rule"]],
    "fixed_lambda": lambda real: [K.fmt(real["fixed_lambda"]["rule"]["auc"])],
    "D_N1_logit": None,
    "n1_p_P_beside_U": lambda real: [f"{real['rows']['N1']['p_P']:.4f}"]}


def test_S31_section_3_5_columns_in_RESULT(rehearsal):
    """S31: every B section 3.5 item has its header in RESULT.md, and its values equal
    summary.json's; N1's p_P beside a U is present exactly when the label is U."""
    md = (rehearsal["committed"] / "RESULT.md").read_text(encoding="utf-8")
    s = json.loads((rehearsal["committed"] / "summary.json").read_text(encoding="utf-8"))
    real = s["real"]
    for item, header in K.SECTION_3_5_HEADERS.items():
        if item == "n1_p_P_beside_U":
            assert (header in md) == (real["label"] == "U")
            if real["label"] != "U":
                continue
        assert header in md, item
        f = SECTION_3_5_VALUE[item]
        if f is None:
            d = s["checks"]["5_n1_parity"]["D_N1_logit"]
            assert f"{K.SECTION_3_5_HEADERS['D_N1_logit']}:** {K.fmt(d, 6)}" in md
            continue
        for v in f(real):
            assert v in md, (item, v)
    rule_row = next(ln for ln in md.splitlines()
                    if ln.startswith("| rule #2.1 | ") and "L1 x ON" not in ln
                    and ln.count("|") == len(K.STRATA) + 2)
    assert rule_row == ("| rule #2.1 | " + " | ".join(SECTION_3_5_VALUE["strata_means"](real))
                        + " |")


def test_S32_u_rule_paragraph_is_block_Bs_own():
    """S32: U worlds below block B's gamma*_P: the paragraph says so and does not describe block B
    with A's literal; at gamma*_P it says the position is A's."""
    ws = []
    labels = {"M0.5": "UUGGG", "M0.6": "RRRGG", "M0.75": "RRRRR", "M0.85": "RRRRR",
              "M1.0": "RRRRR"}
    seen = {"M0.5": 0, "M0.6": 1, "M0.75": 5, "M0.85": 5, "M1.0": 5}
    for fam, labs in labels.items():
        for j, lab in enumerate(labs):
            p = 0.0001 if j < seen[fam] else 0.5
            ws.append({"family": fam, "seed": 91140 + j, "label": lab,
                       "U_reasons": [LEGS] if lab == "U" else [],
                       "rows": {pk: {"p_P": p, "auc": 0.8, "lambda_ko": 3.0}
                                for pk in K.LIMIT_KEYS}})
    dl = K.detection_limits(ws, 10)
    assert dl["leg_P"]["gamma"] == 0.75
    syn = {"u_rule": K.u_rule(ws), "limits": dl, "worlds": ws}
    text = "\n".join(K.u_rule_paragraph(syn))
    assert "0 at it, 2 below it, 0 above it" in text and "do not all lie at gamma*_P" in text
    assert "sit at γ = 0.6 = γ*_P" not in text and "sit at" not in text
    assert "Not-readable U (S38; counted apart, never a threshold U): 0 of 25" in text
    real_nr = "\n".join(K.u_rule_paragraph(syn, {"readable": False}))
    assert "the real block: 1 of 1 (not readable)" in real_nr


def test_S33_per_shuffle_header_unique(rehearsal):
    with open(rehearsal["committed"] / "per_shuffle.csv", encoding="utf-8") as fh:
        cols = next(csv.reader(fh))
    assert len(set(cols)) == len(cols) and cols.count("auc_N1") == 1


def test_S34_filters_state_their_denominator():
    rows = [{"predictor": "BF_1", "p": 0.001}, {"predictor": "BF_1", "p": 0.5},
            {"predictor": "rule", "p": 0.001}]
    with pytest.raises(SystemExit, match="FILTER MATCHED NOTHING: BF:1"):
        K.count_where(rows, "predictor", "BF:1", lambda r: r["p"] <= 0.01)
    c = K.count_where(rows, "predictor", "BF_1", lambda r: r["p"] <= 0.01)
    assert c == {"k": 1, "n": 2, "text": "1 of 2"}


def test_S35_fenced_drafts_are_marked():
    """S35: every fence of this registration is marked (it holds none at 1.4.1); a fixture with
    an unmarked fence fails the checker; a heading inside a fence is not the file's heading."""
    text = REG.read_text(encoding="utf-8")
    assert K.unmarked_fences(text) == []
    bad = "# T\n\nSome text.\n\n```\n## 13. Amendment 1\n```\n"
    assert K.unmarked_fences(bad) == [5]
    good = "# T\n\n" + K.FENCE_MARKER + "\n```\n## 13. Amendment 1\n```\n"
    assert K.unmarked_fences(good) == []
    assert K.headings(bad) == ["# T"]
    tilde = "x\n~~~\n## h\n~~~\n"
    assert K.unmarked_fences(tilde) == [2]


def _ev_with_shuffles(n_deg):
    """A fixture evaluation on the board z: every predictor but N1 ranks it perfectly and N1 is
    noise; n_deg shuffles have no AUC; on the rest no margin reaches the real one."""
    y = K.board_y("z")
    rng = np.random.default_rng(5)
    F = {}
    rec = {"y": y.tolist(), "score": {"existence": 0.3, "offset": 1.0, "counts": 0.5, "sign": 1.0},
           "outside_density": 0.17}
    p_n1 = rng.random(40).tolist()
    for mk in ("ko", "full", "block", "ko1"):
        for pk in K.PRED_KEYS:
            F[("b", mk, pk)] = {**rec, "p": p_n1 if pk == "N1" else (0.2 + 0.6 * y).tolist(),
                                "lam": None if pk == "N1" else 1.0}
    for sd in range(99):
        ys = np.zeros(40, bool) if sd < n_deg else y
        for pk in K.PRED_KEYS:
            p = (0.2 + 0.6 * ys) if pk == "N1" else rng.random(40)
            F[(f"b|sh:{sd}", "ko", pk)] = {**rec, "y": ys.tolist(), "p": list(p), "lam": 1.0}
    return K.evaluate_bank("b", F, 99, 0)


def test_S36_p_S_mark():
    ev = _ev_with_shuffles(1)
    r = ev["rows"]["rule"]
    assert r["n_deg"] == 1 and r["n_ge"] == 0 and r["leg_S_passes"] and r["n_valid_shuffles"] == 98
    line = K.verdict_line(ev, DL, U_KEPT)
    assert ("p_S = 0.0101 [leg S decided by the count: n_ge = 0 of 98] (n_ge = 0 of 98, "
            "n_deg = 1)") in line
    assert "| 0.0101 [leg S decided by the count: n_ge = 0 of 98] |" in "\n".join(
        K.md_bank_table(ev))
    ev0 = _ev_with_shuffles(0)
    line0 = K.verdict_line(ev0, DL, U_KEPT)
    assert "p_S = 0.01 (n_ge = 0 of 99, n_deg = 0)" in line0 and "[leg S" not in line0


def test_S37_prerun_provenance(tmp_path, monkeypatch):
    """S37: a reference whose manifest names the registered head and script passes although the
    running script's hash differs; a manifest naming another script stops the registered run
    with "PRE-RUN PROVENANCE DIFFERS" before the first fit (fit functions that raise are never
    called)."""
    flow_setup(tmp_path, monkeypatch.setattr)
    make_reference(tmp_path, monkeypatch.setattr)
    pv = K.prerun_provenance("f" * 40, "e" * 64)
    assert pv["passed"] and not pv["same_script"] and "different code by design" in pv["text"]
    assert pv["prerun_script_sha256_lf"] == K.PRERUN_SCRIPT_SHA256_LF
    monkeypatch.setattr(K, "PRERUN_SCRIPT_SHA256_LF", "0" * 64)
    assert not K.prerun_provenance("f" * 40, "e" * 64)["passed"]
    fits = []

    def no_fit(*a, **k):
        fits.append(a)
        raise AssertionError("a fit was made before the provenance check")
    monkeypatch.setattr(K, "_fit_one", no_fit)
    monkeypatch.setattr(K, "degree_terms", no_fit)
    monkeypatch.setattr(K, "machine_checks_real", no_fit)
    with pytest.raises(SystemExit):
        K.main(ARM_ARGS)
    with pytest.raises(SystemExit):
        K.main(SYN_ARGS + ["--out", str(tmp_path / "again")])
    assert fits == []
    log = next((tmp_path / "private").iterdir()) / "stdout.log"
    assert K.PROVENANCE_DIFFERS_TEXT in log.read_text(encoding="utf-8")


def test_S38_not_readable(capsys):
    """S38: with n_p = 1 and rows that would read R (and W, and G), the label is U, its first
    reason is block B's literal "of 40", u_kind is not_readable and the rename leaves it; with
    n_p = 2 the ordinary branch is read. With A's read_label(rows) the first case reads R."""
    perms = K.uniform_perms()
    lit = "not readable: leg P cannot reach p_P <= 0.01 on this block (n_present = 1 of 40)"
    for k in (1, 39):
        y = np.zeros(40, bool)
        y[:k] = True
        assert K.smallest_passing_auc(y, y[perms]) is None
    y2 = np.zeros(40, bool)
    y2[:2] = True
    assert K.smallest_passing_auc(y2, y2[perms]) is not None

    def rows(p_P, leg_s, cb=1.0, bf_pass=None):
        out = {pk: {"leg_S_passes": leg_s, "p_P": p_P, "n_ge": 0 if leg_s else 40,
                    "n_valid_shuffles": 99, "ceiling_block": cb, "ceiling_full": 0.95}
               for pk in K.PRED_KEYS}
        if bf_pass:
            out["rule"].update(leg_S_passes=False, p_P=0.5)
            out[bf_pass].update(leg_S_passes=True, p_P=0.001)
        return out
    variants = {"R": rows(0.001, True), "W": rows(0.5, False, bf_pass="BF:2"),
                "G": rows(0.5, False)}
    for want, rr in variants.items():
        assert K.read_label(rr)["label"] == want
        lab = K.read_label(rr, n_present=1, readable=False)
        assert lab["label"] == "U" and lab["U_reasons"][0] == lit
        assert lab["label_before_readability"] == want
        assert K.u_kind(lab["U_reasons"]) == "not_readable"
        for u in (U_KEPT, U_RENAMED):
            assert K.label_text("U", DL, u, lab["U_reasons"], 1.0) == "U: " + lit
        assert K.read_label(rr, n_present=2, readable=True)["label"] == want
    assert "of 64" not in K.NOT_READABLE_REASON


def test_S39_stop_record(tmp_path, monkeypatch, capsys):
    """S39: a fixture 5 x 8 pattern with one swappable square and a lowered cap: the run exits
    non-zero, stop_record.json exists in the run folder, its chain/succ/att/arm/head equal the
    printed ones; the folder holds no SHA256SUMS.txt."""
    folder = tmp_path / "run"
    monkeypatch.setattr(K, "_RUN", {"folder": folder, "arm": "flyvis65_blockB", "head": "c0ffee"})
    monkeypatch.setattr(K, "RC_CAP_FACTOR", 1)
    two = np.zeros(40, bool)
    two[[0, 9]] = True
    with pytest.raises(SystemExit) as e:
        K.rc_patterns(two, n_chains=30)
    assert e.value.code not in (0, None)
    rec = json.loads((folder / K.STOP_RECORD_NAME).read_text(encoding="utf-8"))
    out = capsys.readouterr().out
    m = re.search(r"ATTEMPT CAP REACHED \(chain (\d+), successes (\d+), attempts (\d+)\); arm "
                  r"(\S+), head (\S+);", out)
    assert m and (rec["chain"], rec["succ"], rec["att"]) == tuple(int(x) for x in m.groups()[:3])
    assert (rec["arm"], rec["head"]) == (m.group(4).rstrip(","), m.group(5).rstrip(";"))
    assert rec["att"] == K.RC_SWAPS and rec["succ"] < K.RC_SWAPS
    assert not (folder / "SHA256SUMS.txt").exists()


def test_S39_a_stopped_synthetic_run_has_a_record_and_no_sums(tmp_path, monkeypatch):
    """S39 end to end: --synthetic-only with --out and a cap of 0 attempts stops at the first
    row-and-column null; the --out folder holds stop_record.json and no SHA256SUMS.txt."""
    flow_setup(tmp_path, monkeypatch.setattr)
    monkeypatch.setattr(K, "_RC_CACHE", {})
    monkeypatch.setattr(K, "RC_CAP_FACTOR", 0)
    out = tmp_path / "out"
    with pytest.raises(SystemExit) as e:
        K.main(SYN_ARGS + ["--out", str(out)])
    assert e.value.code not in (0, None)
    rec = json.loads((out / K.STOP_RECORD_NAME).read_text(encoding="utf-8"))
    assert rec["arm"] == "synthetic-only" and rec["att"] == 0
    assert not (out / "SHA256SUMS.txt").exists()
    assert K.RC_CAP_STOP_TEXT.split(" (")[0] in (out / "stdout.log").read_text(encoding="utf-8")


def test_S38_counted_apart_in_RESULT(rehearsal):
    md = (rehearsal["committed"] / "RESULT.md").read_text(encoding="utf-8")
    assert "Not-readable U (S38; counted apart, never a threshold U): " in md
    assert "the real block: " in md


def test_S19_S37_RESULT_header(rehearsal):
    md = (rehearsal["committed"] / "RESULT.md").read_text(encoding="utf-8")
    assert "Code (S37): pre-run made by head " in md and "; this run by head " in md
    s = json.loads((rehearsal["committed"] / "summary.json").read_text(encoding="utf-8"))
    assert s["manifest"]["prerun_provenance"]["passed"]
    ce = s["manifest"]["command_environment"]
    assert ce["PYTHONUTF8"] == "0" and ce["PYTHONIOENCODING"] == "ascii:strict"   # S28


if __name__ == "__main__":
    sys.exit(pytest.main(["-p", "no:cacheprovider", "-v", __file__]))
