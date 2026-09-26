"""Tests of knockout_regrow_male_cns.py, the male CNS arm (registration
docs/plans/2026-09-26-knockout-regrow-male-cns-arm-registration.md, revision 1.1, section 7.3,
tests T1-T12). Fixtures and synthetic banks only: no test opens, hashes, counts or sizes a
sealed file of the build folder. An autouse guard points SEALED_DIR at an empty temporary folder
for every test and records every call of open_sealed and verify_sealed_pins; a test that uses
fixture sealed files (builder format, written to a temporary folder) says so, and every other
test must end with zero calls.

T1   copies of A's 17 label tests (test_knockout_regrow_labels.py), adapted to the arm.
T2   the grid: 2,961 / 3,025 / 64 views; a pool worker reports 3,025; the loader's refusals.
T3   the seal: zero open_sealed calls in --synthetic-only and in the pre-unseal part of the real
     arm; the unseal protocol's order on fixture files; the hash before any parse; check 11.
T4   the leak (check 6): the knockout fit's data dict under three block fillings (real fits).
T5   the existence bank: six predictors train, decode and score on a world with male
     existence content at --starts 3 (real fits).
T6   the worlds: unplaced cells absent, 39 others, 32/32 boards, the No algebra's exact 0.5.
T7   rc_patterns: the board completes (A's draws), one pattern, the attempt cap in both modes.
T8   readability: 1 and 63 present read "not readable"; 0 and 64 have no AUC.
T9   the lobe rules: male_reading on 16 pairs and the one-lobe cases; the split classes; k*.
T10  seeds; --allow-dirty with --arm malecns refused; out_dir_refusal on four references.
T11  checks 3 and 5 are prints.
T12  the p_S print (S28).
T13  revision 1.2 (section 3.3.1): the registered references of both lobes verify in reference
     mode (their pins, smallest_passing_auc, ko1 count and manifests); only A's amended hash is
     still a placeholder. Reads the reference folders (synthetic worlds), never a sealed file.
T14  revision 1.3: S29 (the male U reading with an empty band), S30 (the pre-run's and this
     run's code), S31 (the instrument's numbers beside a male G), S32 (the two notions of split),
     on fixtures and, where the reference folders exist, on the registered references.

The fits of T3's flows are replaced by a deterministic fake (_fit_one, in-process, workers = 1);
T4 and T5 make real fits. Run: tools/.venv/Scripts/python.exe -m pytest -p no:cacheprovider -v
results/genome/c6/checks/test_knockout_regrow_male_cns.py
"""
import csv
import hashlib
import io
import json
import sys
import time
import types
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import knockout_regrow_male_cns as K  # noqa: E402

H = K.H


# ------------------------------------------------------------------------------------------
# The seal guard (T3), for every test.

class SealGuard:
    def __init__(self):
        self.calls = []
        self.fixture_dir = None


@pytest.fixture(autouse=True)
def seal_guard(monkeypatch, tmp_path):
    g = SealGuard()
    empty = tmp_path / "no_sealed_files_here"
    monkeypatch.setattr(K, "SEALED_DIR", empty)
    monkeypatch.setitem(K._UNSEAL, "allowed", False)
    real_open, real_verify = K.open_sealed, K.verify_sealed_pins

    def not_the_build_folder():
        for lobe in K.LOBES:
            p = K.sealed_path(lobe).resolve()
            assert not p.is_relative_to(K.MALE_BUILD_DIR.resolve()), p

    def spy_open(lobe):
        g.calls.append(("open_sealed", lobe))
        not_the_build_folder()
        return real_open(lobe)

    def spy_verify():
        g.calls.append(("verify_sealed_pins", None))
        not_the_build_folder()
        return real_verify()

    monkeypatch.setattr(K, "open_sealed", spy_open)
    monkeypatch.setattr(K, "verify_sealed_pins", spy_verify)
    yield g
    if g.fixture_dir is None:
        assert g.calls == [], f"a sealed-file reader was called: {g.calls}"


BOARD_Z = None


def board(b="z"):
    return K.board_y(b)


def write_sealed_fixture(path, x):
    """A sealed file in the builder's fixed-width format (male_cns_bank_builder.py write_sealed),
    from 64 values of x in block cell order (W = round(800 x), n_tar = 800)."""
    lines = ["src,tar,W,n_tar,x,present"]
    for (s, t), xv in zip(K.BLOCK_NAMES, x):
        n = 800
        W = int(round(float(xv) * n))
        xx = W / n
        lines.append(f"{s},{t},{W:012d},{n:012d},{xx:.6e},{int(xx >= K.C_STAR and xx > 0)}")
    lines.append("# cross_lobe_block_weight_total=000000000000")
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


@pytest.fixture
def fixture_sealed(seal_guard, monkeypatch, tmp_path):
    """Fixture sealed files for both lobes in a temporary folder, with their pins; the guard is
    told that this test reads fixture files. Lobe L: the board z at x = 6 (present) and 0.8
    (absent). Lobe R: the same, with four cells turned over."""
    d = tmp_path / "fixture_sealed"
    d.mkdir()
    yL = board("z")
    xL = np.where(yL, 6.0, 0.8)
    xR = xL.copy()
    xR[[0, 9]] = 0.2                                   # two present cells turned absent
    xR[[4, 13]] = 7.0                                  # two absent cells turned present
    pins = {"L": write_sealed_fixture(d / K.SEALED_NAME["L"], xL),
            "R": write_sealed_fixture(d / K.SEALED_NAME["R"], xR)}
    monkeypatch.setattr(K, "SEALED_DIR", d)
    monkeypatch.setattr(K, "SEALED_SHA256", pins)
    seal_guard.fixture_dir = d
    return {"dir": d, "x": {"L": xL, "R": xR}}


# ------------------------------------------------------------------------------------------
# T1: copies of A's 17 label tests, adapted to the arm (seeds 92..., the male CSV columns, no
# revision 3.2 rename check, the male references in the --out guard).

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
            out.append({"family": fam, "seed": 92000 + j, "label": lab, "rows": rows})
    return out


DL = K.detection_limits(fake_worlds(), 10)
U_KEPT = {"renamed": False}
U_RENAMED = {"renamed": True}
FAILED = f"U: {K.FAILED_FIT_TEXT}"
LEGS = "the legs disagree for rule #2.1: leg S n_ge = 0 of 99, leg P p_P = 0.0308"


def test_T1_fixture_limits():
    assert DL["leg_P"]["gamma"] == 0.6 and DL["R"]["gamma"] == 0.75


def test_T1_i_ceiling_block_reason_gives_failed_fit():
    assert K.label_text("U", DL, U_KEPT, [K.ceiling_block_reason(0.85)]) == FAILED
    assert K.label_text("U", DL, U_KEPT, [LEGS, K.ceiling_block_reason(0.85)]) == FAILED


def test_T1_ii_rename_never_applies_to_failed_fit():
    assert K.label_text("U", DL, U_RENAMED, [K.ceiling_block_reason(0.85)]) == FAILED
    assert K.label_text("U", DL, U_RENAMED, [LEGS, K.ceiling_block_reason(0.85)]) == FAILED


def test_T1_ii_not_measured_is_not_a_failed_fit():
    r = K.ceiling_block_reason(None)
    assert r == K.CEILING_BLOCK_NOT_MEASURED and "n/a" not in r and "below" not in r
    assert not r.startswith(K.CEILING_BLOCK_REASON)
    nm = f"U: {K.NOT_MEASURED_TEXT}"
    for u in (U_KEPT, U_RENAMED):
        assert K.label_text("U", DL, u, [r, LEGS]) == nm != FAILED
    assert K.label_text("U", DL, U_KEPT, [r, K.ceiling_block_reason(0.85)]) == FAILED


def test_T1_iii_threshold_u_without_the_reason():
    t = K.label_text("U", DL, U_KEPT, [LEGS])
    assert t == (f"U: {K.U_THRESHOLD} (at the leg-P detection limit gamma*_P = 0.6; "
                 f"transition band {DL['band']['text']})")
    assert K.FAILED_FIT_TEXT not in t
    assert K.label_text("U", DL, U_RENAMED, [LEGS]) == (
        f"U: {K.U_UNCALIBRATED}; never read as a finding")
    assert K.label_text("U", DL, U_KEPT, []).startswith(f"U: {K.U_THRESHOLD}")


def test_T1_iv_g_text():
    g = K.label_text("G", DL, U_KEPT, [], 1.0)
    gate = f"gate: rule #2.1's ceiling_block = 1.0000 >= {K.GATE_CUT:.2f}; "
    assert g == f"G: not detected at the R level above gamma_R ({gate}{K.limits_text(DL)})"
    assert g.replace(gate, "") == (
        f"G: not detected at the R level above gamma_R ({K.limits_text(DL)})")
    assert "leg P from gamma*_P = 0.6" in g and "weak" not in g
    assert K.label_text("G", DL, U_RENAMED, [K.ceiling_block_reason(0.5)], 1.0) == g


def test_T1_read_label_failed_fit_end_to_end():
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


def test_T1_mechanism_description_names_rule_ceiling_full():
    assert K.mechanism_description({"ceiling_full": 0.5088}) == (
        f"orthogonal (rule #2.1's ceiling_full = 0.5088 < {K.MECHANISM_CUT:.2f})")
    assert K.mechanism_description({"ceiling_full": 0.92}) == (
        f"no information (rule #2.1's ceiling_full = 0.9200 >= {K.MECHANISM_CUT:.2f})")


def test_T1_probe_mechanism_cut_moves_only_the_mechanism_text(monkeypatch):
    before = _cut_texts()
    monkeypatch.setattr(K, "MECHANISM_CUT", 0.95)
    after = _cut_texts()
    assert after["mechanism"] != before["mechanism"]
    assert after["mechanism"] == (
        f"orthogonal (rule #2.1's ceiling_full = 0.9200 < {K.MECHANISM_CUT:.2f})")
    assert after["reason"] == before["reason"] and after["gate"] == before["gate"]


def test_T1_probe_gate_cut_moves_only_the_gate_texts(monkeypatch):
    before = _cut_texts()
    monkeypatch.setattr(K, "GATE_CUT", 0.95)
    after = _cut_texts()
    assert after["reason"] != before["reason"] and after["gate"] != before["gate"]
    assert f"is below {K.GATE_CUT:.2f}" in after["reason"]
    assert f"ceiling_block = 1.0000 >= {K.GATE_CUT:.2f}" in after["gate"]
    assert after["mechanism"] == before["mechanism"]


def test_T1_u_rule_counts_threshold_u_only():
    def worlds(reasons):
        return [{"family": "M0.6", "seed": 92160 + j, "label": "U", "U_reasons": r}
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
    r.update(family="Nf", j=0, seed=92110, predictor="rule #2.1", label="G",
             mechanism_description="orthogonal (rule #2.1's ceiling_full = 0.5088 < 0.90)",
             D=0.123456789)
    r.update(kw)
    return r


def test_T1_csv_compare_outcomes():
    """Adapted: the male CSV has precision_at_n_present and auc_other_61; column 8 is reported
    and never checked against A's revision 3.2 rename (S17)."""
    assert "precision_at_n_present" in K.WORLDS_CSV_HEADER
    assert "auc_other_61" in K.WORLDS_CSV_HEADER and len(K.WORLDS_CSV_HEADER) == 33
    ref = _csv([_row()])
    same = K.csv_compare(ref, ref)
    assert same["outcome"] == 1 and same["passed"] and same["byte_identical"]
    mech = K.csv_compare(ref, _csv([_row(mechanism_description="orthogonal (rule #2.1's "
                                                               "ceiling_full = 0.5000 < 0.90)")]))
    assert mech["outcome"] == 1 and mech["passed"] and not mech["byte_identical"]
    assert mech["mechanism_description_differences"] == 1
    assert mech["first_mechanism_description_differences"][0]["now"].endswith("0.5000 < 0.90)")
    assert "mechanism_description_explained_by_rename_3_2" not in mech
    tiny = K.csv_compare(ref, _csv([_row(D=0.123456789 + 5e-10)]))
    assert tiny["outcome"] == 2 and tiny["passed"] and "D" in tiny["continuous_within_tolerance"]
    big = K.csv_compare(ref, _csv([_row(D=0.123456789 + 1e-6)]))
    assert big["outcome"] == 3 and not big["passed"] and big["outcome_3_parts"] == ["b"]
    lat = K.csv_compare(ref, _csv([_row(p_P="0.0107")]))
    assert lat["outcome"] == 3 and lat["first_exact_differences"][0]["columns"] == ["p_P"]
    assert lat["outcome_3_parts"] == ["a"]
    both = K.csv_compare(ref, _csv([_row(p_P="0.0107", D=0.123456789 + 1e-6)]))
    assert both["outcome_3_parts"] == ["a", "b"]
    assert K.csv_compare(ref, _csv([_row(label="U")]))["outcome"] == 3
    dup = K.csv_compare(ref, _csv([_row(), _row()]))
    assert dup["outcome"] == 3 and dup["n_duplicate_keys"] == 1


def test_T1_csv_compare_by_key():
    r1, r2 = _row(), _row(predictor="BF_1", D=0.5)
    ref = _csv([r1, r2])
    swapped = K.csv_compare(ref, _csv([r2, r1]))
    assert swapped["outcome"] == 1 and swapped["row_order_differs"]
    assert swapped["exact_differences"] == 0 and not swapped["byte_identical"]
    assert not K.csv_compare(ref, ref)["row_order_differs"]
    six = [_row(seed=92110 + j, predictor=pk, D=0.1 * j) for j, pk in
           enumerate(("rule #2.1", "BF_1", "BF_2", "BF_3", "BF_4", "N1"))]
    perm = K.csv_compare(_csv(six), _csv([six[i] for i in (3, 0, 5, 1, 4, 2)]))
    assert perm["outcome"] == 1 and perm["passed"] and perm["row_order_differs"]
    short = K.csv_compare(ref, _csv([r1]))
    assert short["outcome"] == 3 and short["outcome_3_parts"] == ["a"]
    assert short["rows_missing_now"] == [["Nf", "0", "92110", "BF_1"]]
    extra = K.csv_compare(_csv([r1]), ref)
    assert extra["outcome"] == 3 and extra["n_rows_missing_prerun"] == 1
    assert K.repro_fail_treatment(["b"]) != K.repro_fail_treatment(["a"])
    assert "layer (2) is not the cause" in K.repro_fail_treatment(["b"])


def test_T1_smallest_passing_auc_check():
    """Adapted: the male registered values do not exist yet (section 3.3). In pre-run mode they
    are computed from the boards' labels (board_smallest_passing_auc); each is on the lattice
    k / 1024 and the check passes with them, fails with a wrong or a missing one. Once a lobe's
    reference is registered, the values derived from it must equal them (both lobes)."""
    reg = K.board_smallest_passing_auc()
    assert set(reg) == {"z", "z'"}
    for v in reg.values():
        assert v is not None and (v * 1024) == int(v * 1024) and 0.5 < v < 1
    entries = [{"world": "world:R:0", "board": "z", "y": board("z")},
               {"world": "world:No:0", "board": "z'", "y": board("z'")}]
    ok = K.check_smallest_passing_auc(entries, reg)
    assert ok["passed"] and ok["n_equal"] == 2 and not ok["mismatches"]
    wrong = K.check_smallest_passing_auc(entries, {"z": reg["z"], "z'": reg["z"] + 1 / 1024})
    assert not wrong["passed"] and [m["world"] for m in wrong["mismatches"]] == ["world:No:0"]
    missing = K.check_smallest_passing_auc(entries, {"z": reg["z"]})
    assert not missing["passed"] and missing["mismatches"][0]["registered"] is None
    assert not K.check_smallest_passing_auc([], reg)["passed"]
    for lobe in K.LOBES:
        if K.reference_mode(lobe):
            assert K.check_prerun_files(lobe)["passed"]
            d = K.derive_smallest_passing_auc(K.PRERUN_DIR[lobe] / "synthetic_only.json")
            assert d["passed"] and d["by_board"] == reg


def test_T1_derive_smallest_passing_auc(tmp_path):
    def fixture(name, worlds):
        path = tmp_path / name
        path.write_text(json.dumps({"worlds": worlds}), encoding="utf-8")
        return K.derive_smallest_passing_auc(path)

    one = fixture("one.json", [{"seed": 1, "board": "z", "smallest_passing_auc": 0.5},
                               {"seed": 2, "board": "z", "smallest_passing_auc": 0.5},
                               {"seed": 3, "board": "z'", "smallest_passing_auc": 0.75}])
    assert one["passed"] and one["by_board"] == {"z": 0.5, "z'": 0.75}
    two = fixture("two.json", [{"seed": 1, "board": "z", "smallest_passing_auc": 0.5},
                               {"seed": 2, "board": "z", "smallest_passing_auc": 0.625}])
    assert not two["passed"] and two["boards_with_several_values"] == {"z": [0.5, 0.625]}
    gap = fixture("gap.json", [{"seed": 1, "board": "z", "smallest_passing_auc": None}])
    assert not gap["passed"] and gap["worlds_without_board_or_value"] == [1]
    assert not fixture("none.json", [])["passed"]


def test_T1_ko1_count_control():
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
    assert K.check_ko1_count(other, None, comparable=False, reread=False)["passed"] is None
    pre = K.check_ko1_count(other, None, comparable=True, reread=False, prerun=True)
    assert pre["passed"] is None and "pre-run mode" in pre["status"]
    assert "reused_from_ko" in K.STORE_FIELDS_COMPARED


def _fake_reference(tmp_path, monkeypatch, name, lobe="L"):
    ref = tmp_path / name
    ref.mkdir()
    pins = {}
    for n in K.PRERUN_FILES:
        (ref / n).write_bytes(f"fake {n}".encode())
        pins[n] = hashlib.sha256(f"fake {n}".encode()).hexdigest()
    monkeypatch.setitem(K.PRERUN_DIR, lobe, ref)
    monkeypatch.setitem(K.PRERUN_SHA256, lobe, pins)
    return ref


def test_T1_out_guard_refusals(tmp_path, monkeypatch):
    """Adapted: the guard on a temporary male reference (lobe L), never a real one."""
    import shutil
    ref = _fake_reference(tmp_path, monkeypatch, "prerun")
    assert K.out_dir_refusal(None) is None
    assert "reference folder or inside it" in K.out_dir_refusal(ref)
    assert "inside it" in K.out_dir_refusal(ref / "sub" / "dir")
    assert "inside it" in K.out_dir_refusal(ref / ".." / ref.name)
    assert "with --arm" in K.out_dir_refusal(tmp_path / "new", arm="malecns")
    copy = tmp_path / "copy"
    shutil.copytree(ref, copy)
    assert "byte copy" in K.out_dir_refusal(copy)
    one = tmp_path / "one"
    one.mkdir()
    shutil.copy2(ref / "raw_fits.json.gz", one / "raw_fits.json.gz")
    assert "byte copy" in K.out_dir_refusal(one)
    (copy / "raw_fits.json.gz").write_bytes(b"a fresh gzip with another mtime")
    assert K.out_dir_refusal(copy) is None
    (tmp_path / "empty").mkdir()
    assert K.out_dir_refusal(tmp_path / "empty") is None
    assert K.out_dir_refusal(tmp_path / "does_not_exist") is None


# ------------------------------------------------------------------------------------------
# T2: the grid and the loader.

OUTSIDE_HEADER = "src,tar,du,dv,n_syn,sign\n"


def test_T2_views_on_the_placed_grid():
    K.restrict_to_placed_grid()
    geo = H.Bank("g", {})
    n = {k: len(H.make_view(geo, K.MASKS[k]).cells) for k in ("ko", "full", "block")}
    assert n == {"ko": 2961, "full": 3025, "block": 64}
    assert K.check_block_and_mask()["passed"]
    assert K.check_grid()["passed"]
    assert len(K.OTHERS) == 39 and len(K.PLACED_NAMES) == 55


def test_T2_pool_workers_report_their_grid():
    """A worker started by the pool (Windows spawn) reports 3,025 after _w_init; check 8's pool,
    which does not restrict, reports the full grid."""
    with ProcessPoolExecutor(max_workers=1, initializer=K._w_init,
                             initargs=(3, None, True, "L", True, None)) as ex:
        assert ex.submit(K._w_grid_size).result() == 3025
    with ProcessPoolExecutor(max_workers=1, initializer=K._w_init,
                             initargs=(3, None, True, None, False, None)) as ex:
        assert ex.submit(K._w_grid_size).result() == 65 * 65


def test_T2_loader_refusals(tmp_path, capsys):
    def load(text):
        p = tmp_path / "fixture_outside.csv"
        p.write_text(OUTSIDE_HEADER + text, encoding="utf-8", newline="\n")
        return K.load_male_bank("L", path=p)

    ok = load("Tm5Y,Tm5Y,0,0,12.5,1\nMi1,Mi14,0,0,3.5,1\n")
    assert len(ok.content) == 2 and ok.content[(H.IDX["Mi1"], H.IDX["Mi14"])] == {
        "offsets": {(0, 0): 3.5}, "hull": [], "sign": 1}
    with pytest.raises(SystemExit, match="outside the 55 placed types"):
        load("Mi3,Tm5Y,0,0,4.0,1\n")                  # Mi3 is not placed
    with pytest.raises(SystemExit, match="outside the 55 placed types"):
        load("Tm5Y,R2,0,0,4.0,1\n")                   # R2 is pooled into R1
    with pytest.raises(SystemExit, match="BLOCK ROW IN OUTSIDE FILE"):
        load("Mi1,T4a,0,0,9.0,1\n")
    with pytest.raises(SystemExit, match="offset"):
        load("Tm5Y,Tm5Y,1,0,12.5,1\n")
    with pytest.raises(SystemExit, match="sign"):
        load("Tm5Y,Tm5Y,0,0,12.5,-1\n")
    with pytest.raises(SystemExit, match="twice"):
        load("Tm5Y,Tm5Y,0,0,12.5,1\nTm5Y,Tm5Y,0,0,12.5,1\n")
    for lobe, n in (("L", 496), ("R", 526)):
        b = K.load_male_bank(lobe)
        assert len(b.content) == n and not (b.exists & ~K.PLACED_GRID).any()
        assert not (b.exists & K.BLOCK).any()


# ------------------------------------------------------------------------------------------
# T3: the seal.

def fake_fit_one(bk, mk, pk, bank):
    """A deterministic stand-in for a fit (T3's flows): p carries the block's labels plus noise
    seeded by the key; the hash of a knockout fit is the hash of the knockout view, so it sees
    exactly what the rule would see; a ko1 record repeats its ko record at lambda = 1."""
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
    p = 0.3 * np.random.default_rng(seed).random(64) + 0.4 * y
    lam = None if pk == "N1" else (1.0 if mk == "ko1" or seed % 2 else 3.0)
    return {"p": p.tolist(), "y": y.tolist(), "lam": lam,
            "score": {"existence": 0.5, "offset": float("nan"), "counts": float("nan"),
                      "sign": float("nan"), "sign_n": 0, "n_ne": int(y.sum())},
            "outside_density": float(bank.exists[~K.BLOCK & K.PLACED_GRID].mean()),
            "secs": 0.0}


SMOKE = ["--starts", "3", "--workers", "1", "--smoke-families", "M0.5", "--smoke-worlds", "1",
         "--smoke-shuffles", "2", "--smoke-perm-ceilings", "1"]


def test_T3_synthetic_only_never_touches_a_sealed_file(seal_guard, monkeypatch, tmp_path):
    monkeypatch.setattr(K, "_fit_one", fake_fit_one)
    # revision 1.2: the pins are registered; this test keeps exercising pre-run mode (the mode
    # the pre-run ran in), independent of the real reference folders (T13 covers those).
    monkeypatch.setitem(K.PRERUN_SHA256, "L", None)
    monkeypatch.setitem(K.PRERUN_WORLDS_CSV_SHA256, "L", None)
    syn = K.main(["--synthetic-only", "--lobe", "L", *SMOKE, "--out", str(tmp_path / "out")])
    assert syn["lobe"] == "L" and not syn["reference_mode"]
    assert (tmp_path / "out" / "synthetic_worlds.csv").is_file()
    man = json.loads((tmp_path / "out" / "synthetic_only.json").read_text(encoding="utf-8"))
    assert man["manifest"]["sealed_files_touched"] is False
    assert seal_guard.calls == []


def test_T3_open_sealed_hash_first_and_check_11(fixture_sealed, monkeypatch, tmp_path, capsys):
    with pytest.raises(RuntimeError, match="only by the registered real arm"):
        K.open_sealed("L")                             # the gate is not open
    monkeypatch.setitem(K._UNSEAL, "allowed", True)
    got = K.open_sealed("L")
    assert np.array_equal(got["y"], board("z")) and len(got["present_cells"]) == 32
    assert got["check_11"]["passed"] and got["cross_lobe_line"].startswith("# cross_lobe")
    # a wrong pin: refused before anything is parsed
    parsed = []
    real_parse = K.parse_sealed
    monkeypatch.setattr(K, "parse_sealed", lambda *a, **k: parsed.append(1) or real_parse(*a, **k))
    monkeypatch.setitem(K.SEALED_SHA256, "R", "0" * 64)
    with pytest.raises(SystemExit):
        K.open_sealed("R")
    assert parsed == [] and "SEALED FILE PIN DIFFERS" in capsys.readouterr().out
    with pytest.raises(SystemExit):
        K.verify_sealed_pins()
    assert parsed == []
    # check 11: a row whose present contradicts x and c*
    text = (fixture_sealed["dir"] / K.SEALED_NAME["L"]).read_text(encoding="utf-8")
    lines = text.split("\n")
    s, t, W, n, x, pr = lines[1].split(",")
    lines[1] = ",".join([s, t, W, n, x, str(1 - int(pr))])
    with pytest.raises(SystemExit):
        real_parse("\n".join(lines), "L")
    assert "SEALED FILE INCONSISTENT" in capsys.readouterr().out
    # and a missing row, and a non-block name
    with pytest.raises(SystemExit):
        real_parse("\n".join(lines[:1] + lines[2:]), "L")
    bad = text.replace("Mi1,T4a,", "Mi1,Mi14,", 1)
    with pytest.raises(SystemExit):
        real_parse(bad, "L")


def _flow_args():
    return types.SimpleNamespace(
        starts=3, workers=1, allow_dirty=False, from_raw=None, worlds_per_family=1, shuffles=2,
        perm_ceilings=1, families=["M0.5"], out=None, lobe=None, arm="malecns",
        synthetic_only=False)


@pytest.fixture
def real_arm_setup(fixture_sealed, monkeypatch, tmp_path):
    """The real-arm path against fixture files: fixture references for both lobes, made by
    --synthetic-only with the fake fits and pinned here; the amended A's hash set to A's
    current hash; the private and committed outputs in temporary folders; the tree check and
    check 8 stubbed (check 8's pool runs on the full grid, which earlier tests restricted)."""
    monkeypatch.setattr(K, "_fit_one", fake_fit_one)
    for lobe in K.LOBES:
        out = tmp_path / f"ref_{lobe}"
        K.main(["--synthetic-only", "--lobe", lobe, *SMOKE, "--out", str(out)])
        sums = dict(reversed(ln.split(" *")) for ln in
                    (out / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines())
        monkeypatch.setitem(K.PRERUN_DIR, lobe, out)
        monkeypatch.setitem(K.PRERUN_SHA256, lobe, {n: sums[n] for n in K.PRERUN_FILES})
        monkeypatch.setitem(K.PRERUN_WORLDS_CSV_SHA256, lobe, sums["synthetic_worlds.csv"])
    monkeypatch.setattr(K, "A_REGISTRATION_SHA256_LF_AMENDED",
                        K.sha256_lf(K.ROOT / K.A_REGISTRATION))
    # S30: the fixture references were made at this head by this script
    monkeypatch.setattr(K, "PRERUN_GIT_HEAD", K.git("rev-parse", "HEAD"))
    monkeypatch.setattr(K, "PRERUN_SCRIPT_SHA256_LF", K.sha256_lf(Path(K.__file__)))
    monkeypatch.setattr(K, "PRIVATE_ROOT", tmp_path / "private")
    monkeypatch.setattr(K, "OUT", tmp_path / "committed")
    monkeypatch.setattr(K, "refuse_if_dirty", lambda: "")
    monkeypatch.setattr(K, "check_harness_identity", lambda a: {"stub": True, "passed": True})
    events = []
    for name in ("run_synthetic", "checks_before_unsealing", "verify_sealed_pins", "open_sealed"):
        f = getattr(K, name)

        def spy(*a, _f=f, _n=name, **k):
            events.append((_n, a[1] if _n in ("run_synthetic", "checks_before_unsealing")
                           else (a[0] if a else None)))
            return _f(*a, **k)
        monkeypatch.setattr(K, name, spy)
    return events


def test_T3_real_arm_unseals_only_after_both_lobes_gates(real_arm_setup, seal_guard, tmp_path):
    events = real_arm_setup
    summary = K.run_real_arm(_flow_args(), time.time(), smoke=True)
    names = [e[0] for e in events]
    first_open = names.index("verify_sealed_pins")
    before = events[:first_open]
    assert ("run_synthetic", "L") in before and ("run_synthetic", "R") in before
    assert ("checks_before_unsealing", "L") in before and ("checks_before_unsealing", "R") in before
    assert [e for e in events if e[0] == "open_sealed"] == [("open_sealed", "L"),
                                                           ("open_sealed", "R")]
    assert all(n != "open_sealed" for n in names[:first_open])
    assert (tmp_path / "committed" / "RESULT.md").is_file()
    assert (tmp_path / "committed" / "per_shuffle_L.csv").is_file()
    assert summary["male_reading"]["label"] in ("R", "W", "G", "U", "split", "one lobe only")
    assert summary["lobe_comparison"]["k"] == 4
    private = next((tmp_path / "private").iterdir())
    assert (private / "stdout.log").is_file() and (private / "block_A_cells.json").is_file()
    committed = (tmp_path / "committed" / "summary.json").read_text(encoding="utf-8")
    assert '"x_L_in_band"' not in committed            # per-cell band flags stay private
    assert sys.stdout.__class__.__name__ != "_Tee"
    # revision 1.3: S30's provenance is recorded and printed; S32's two notions are printed
    prov = summary["manifest"]["prerun_provenance"]
    assert set(prov) == {"L", "R"} and all(prov[lobe]["passed"] for lobe in K.LOBES)
    assert prov["L"]["this_run_script_sha256_lf"] == K.sha256_lf(Path(K.__file__))
    assert summary["split_notions"]["by_block"]["k"] == 4
    md = (tmp_path / "committed" / "RESULT.md").read_text(encoding="utf-8")
    assert "Code (S30): lobe L: pre-run made by head " in md
    assert "The two notions of split (S32): Split by reading (section 4.2, D3): " in md


def test_T3_a_failed_synthetic_step_keeps_both_seals(real_arm_setup, seal_guard, monkeypatch):
    events = real_arm_setup
    spied = K.run_synthetic

    def failing(a, lobe, *rest, **k):
        syn, F = spied(a, lobe, *rest, **k)
        if lobe == "R":
            syn["two_world_check"]["passed"] = False
        return syn, F
    monkeypatch.setattr(K, "run_synthetic", failing)
    with pytest.raises(SystemExit):
        K.run_real_arm(_flow_args(), time.time(), smoke=True)
    assert not [e for e in events if e[0] in ("open_sealed", "verify_sealed_pins")]
    assert not [e for e in events if e[0] == "checks_before_unsealing"]


def test_T3_a_leak_before_unsealing_keeps_both_seals(real_arm_setup, monkeypatch):
    events = real_arm_setup
    real = K._fit_one

    def leaky(bk, mk, pk, bank):
        rec = real(bk, mk, pk, bank)
        if "#hash" in mk and "fill:z" in bk:
            rec = {**rec, "data_sha256": "leak"}
        return rec
    monkeypatch.setattr(K, "_fit_one", leaky)
    with pytest.raises(SystemExit):
        K.run_real_arm(_flow_args(), time.time(), smoke=True)
    assert not [e for e in events if e[0] in ("open_sealed", "verify_sealed_pins")]


# ------------------------------------------------------------------------------------------
# T4, T5: real fits at --starts 3.

@pytest.fixture(scope="module")
def lobe_L():
    K.restrict_to_placed_grid()
    bank = K.load_male_bank("L")
    return bank, K.degree_terms(bank)


def test_T4_block_fillings_do_not_leak(lobe_L):
    """Check 6 on a synthetic lobe bank: rule #2.1's knockout data dict is byte-identical with
    the block all absent, the board z, and a random third filling."""
    bank, terms = lobe_L
    K._w_init(3, terms, True, "L", True, None)
    h = {}
    for key in ("outside", "outside|fill:z", "outside|fill:rand7"):
        b = K.build_bank(key, K._W)
        assert (b.exists[K.BLOCK].sum() > 0) == (key != "outside")
        h[key] = K._fit_one(key, "ko#hash#0", "rule", b)["data_sha256"]
    assert len(set(h.values())) == 1, h


def test_T5_existence_bank_runs_every_predictor(lobe_L):
    """A world with male existence content (a fixture content pool of five existence rows): N1,
    rule #2.1 and BF_1..BF_4 train, decode and score on the ko, full and block masks at
    --starts 3; the existence log-loss is finite; the offset, count and sign fields exist and
    are labelled meaningless."""
    _, terms = lobe_L
    pool = [{"offsets": {(0, 0): x}, "hull": [], "sign": 1} for x in (3.1, 4.7, 12.0, 6.5, 3.3)]
    world = K.make_world(K.spec_of("R", 0), terms, pool)
    K._w_init(3, terms, True, "L", True, None)
    F = {}
    for mk in ("ko", "full", "block"):
        for pk in K.PRED_KEYS:
            rec = K._fit_one("world:R:0", mk, pk, world)
            assert np.isfinite(rec["score"]["existence"])
            assert set(rec["score"]) >= {"offset", "counts", "sign"}
            assert np.all(np.isfinite(rec["p"])) and len(rec["p"]) == 64
            F[("world:R:0", mk, pk)] = rec
    for pk in ("rule",) + K.BF_KEYS:
        F[("world:R:0", "ko1", pk)] = {**F[("world:R:0", "ko", pk)], "lam": 1.0}
    ev = K.evaluate_bank("world:R:0", F, 0, 0, "synthetic")
    for pk in K.PRED_KEYS:
        oc = ev["rows"][pk]["present_cells_offset_counts_sign"]
        assert oc["label"] == "meaningless on an existence bank"
        assert set(oc["values"]) == {"offset", "counts", "sign"}


# ------------------------------------------------------------------------------------------
# T6: the worlds.

def test_T6_worlds_on_the_placed_grid(lobe_L):
    bank, terms = lobe_L
    pool = K.content_pool(bank)
    assert len(pool) == 496
    z = np.outer(K.Z_BLOCK, K.Z_BLOCK)[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]]
    for spec in K.world_specs():
        w = K.make_world(spec, terms, pool)
        assert not (w.exists & ~K.PLACED_GRID).any()
        y = w.exists[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]]
        assert y.sum() == 32 and np.array_equal(y, board(spec["board"]))
        assert all(c == {"offsets": {(0, 0): c["offsets"][(0, 0)]}, "hull": [], "sign": 1}
                   for c in w.content.values() if c is not None)
    assert len(K.OTHERS) == 39 and not set(K.OTHERS) & set(K.BLOCK_TYPES)
    assert all(K.PLACED[i] for i in K.OTHERS)
    # the No algebra: the pure z score has AUC exactly 0.5 on the board z', and 1 on z
    assert K.auc(z, board("z'")) == 0.5 and K.auc(z, board("z")) == 1.0


# ------------------------------------------------------------------------------------------
# T7: rc_patterns.

def _a_rc_chains(y, seed):
    """A's rc_patterns loop (knockout_regrow.py:596-624 at 74db080), with the seed given."""
    rng = np.random.default_rng(seed)
    yb = np.asarray(y, bool).reshape(8, 8)
    B = np.broadcast_to(yb, (K.N_PERM, 8, 8)).copy()
    succ = np.zeros(K.N_PERM, np.int64)
    n = np.arange(K.N_PERM)
    while (succ < K.RC_SWAPS).any():
        a = rng.integers(8, size=(K.N_PERM, 4))
        i, j, k, l = a[:, 0], a[:, 1], a[:, 2], a[:, 3]
        x11, x12, x21, x22 = B[n, i, k], B[n, i, l], B[n, j, k], B[n, j, l]
        ok = ((succ < K.RC_SWAPS) & (i != j) & (k != l) & (x11 == x22) & (x12 == x21)
              & (x11 != x12))
        m = n[ok]
        for r, c in ((i, k), (i, l), (j, k), (j, l)):
            B[m, r[ok], c[ok]] = ~B[m, r[ok], c[ok]]
        succ += ok
    return B.reshape(K.N_PERM, 64)


def test_T7_board_completes_with_As_draws():
    res = K.rc_patterns(board("z"), "synthetic")
    assert res["status"] == "complete" and res["patterns"].shape == (9999, 64)
    assert np.array_equal(res["patterns"], _a_rc_chains(board("z"), K.SEED_RC))


def test_T7_one_pattern_and_the_cap(capsys):
    nested = np.array([[c <= r for c in range(8)] for r in range(8)]).ravel()
    assert not K.has_checkerboard(nested.reshape(8, 8))
    for mode in ("synthetic", "real"):
        r = K.rc_patterns(nested, mode)
        assert r["patterns"] is None and r["text"] == "n/a: the row-and-column null has one pattern"
    two = np.zeros(64, bool)
    two[[0, 9]] = True                                 # (0,0) and (1,1): swappable, ~0.1 % success
    assert K.has_checkerboard(two.reshape(8, 8))
    real = K.rc_patterns(two, "real", n_chains=50)
    assert real["patterns"] is None and real["status"] == "cap"
    assert real["text"].startswith("n/a (attempt cap reached: chain ")
    assert real["attempts"] == 100 * 640 and real["successes"] < 640
    with pytest.raises(SystemExit):
        K.rc_patterns(two, "synthetic", n_chains=50)
    assert "ROW-AND-COLUMN NULL: ATTEMPT CAP REACHED (chain " in capsys.readouterr().out


# ------------------------------------------------------------------------------------------
# T8: readability.

def _rows(p_P=0.5, cb=1.0, leg_s=False):
    return {pk: {"leg_S_passes": leg_s, "p_P": p_P, "n_ge": 40, "n_valid_shuffles": 99,
                 "ceiling_block": cb, "ceiling_full": 0.95} for pk in K.PRED_KEYS}


def test_T8_not_readable_and_no_auc(capsys):
    perms = K.uniform_perms()
    for k in (1, 63):
        y = np.zeros(64, bool)
        y[:k] = True
        assert K.smallest_passing_auc(y, y[perms]) is None
        lab = K.read_label(_rows(), n_present=k, readable=False)
        assert lab["label"] == "U" and not lab["readable"]
        t = K.label_text("U", DL, U_RENAMED, lab["U_reasons"], 1.0)
        assert t == (f"U: not readable: leg P cannot reach p_P <= 0.01 on this block "
                     f"(n_present = {k} of 64)")
        # it takes precedence over G, and over a failed fit
        assert K.read_label(_rows(), n_present=k, readable=False)["label_before_readability"] == "G"
        lab2 = K.read_label(_rows(cb=0.5), n_present=k, readable=False)
        assert K.u_kind(lab2["U_reasons"]) == "not_readable"
        assert K.label_text("U", DL, U_KEPT, lab2["U_reasons"], 0.5) == t
    y2 = np.zeros(64, bool)
    y2[:2] = True
    assert K.smallest_passing_auc(y2, y2[perms]) is not None
    for k in (0, 64):
        y = np.zeros(64, bool)
        y[:k] = True
        c3 = K.check_block_print(y, "L")
        assert c3["stops_lobe"] and not c3["has_auc"] and K.smallest_passing_auc(y, y[perms]) is None
        assert "BLOCK HAS NO AUC" in capsys.readouterr().out
        st = K.lobe_status(None, k)
        assert not st["readable"] and st["letter"] is None


# ------------------------------------------------------------------------------------------
# T9: the lobe rules.

def st(letter, readable=True, reason=None):
    return {"letter": letter, "readable": readable, "reason": reason, "W_ranks": ["BF_2"]}


def test_T9_male_reading_all_pairs():
    for a in K.LABELS:
        for b in K.LABELS:
            m = K.male_reading({"L": st(a), "R": st(b)})
            if a == b:
                assert m["label"] == a
            else:
                assert m["label"] == "split"
                assert m["text"].startswith(f"split: lobe L reads {a}, lobe R reads {b}")
    assert K.male_reading({"L": st("R"), "R": st("R")})["text"] == (
        "R: regrows in both lobes of one animal")
    one = K.male_reading({"L": st("R"), "R": st(None, False, "BLOCK HAS NO AUC (0 of 64 present)")})
    assert one["label"] == "one lobe only" and "Not a male R" in one["text"]
    assert one["text"].startswith("one lobe only: lobe L reads R; lobe R cannot be read")
    nr = K.male_reading({"L": st("U", False, K.not_readable_reason(1)), "R": st("U")})
    assert nr["label"] == "one lobe only" and "lobe R reads U" in nr["text"]
    none = K.male_reading({"L": st(None, False, "x"), "R": st("U", False, "y")})
    assert none["label"] == "none"
    assert K.joint_reading({"label": "G"})["text"].endswith(
        "Power of the male R not calibrated; this G does not by itself exclude averaging as the "
        "explanation of flyvis-65's G")
    assert K.joint_reading({"label": "split"})["A_D13_row"] == "any other pair"
    assert K.joint_reading({"label": "R"})["A_D13_row"] == "R on the male CNS only: a flag"


def test_T9_split_classes():
    assert K.k_star() == 4
    tails = [K.binomial_tail(k, 64, 36 / 2961) for k in (1, 2, 3, 4)]
    assert [round(t, 3) for t in tails[:3]] == [0.543, 0.183, 0.043] and round(tails[3], 4) == 0.0078
    c = K.C_STAR
    yL = board("z")
    far = np.where(yL, 3 * c, 0.3 * c)                  # every cell outside [0.5 c*, 2 c*]
    assert K.lobe_split_class(yL, yL, far, far)["class"] == "S0"
    yR = yL.copy()
    yR[[0, 1, 2]] = ~yR[[0, 1, 2]]
    xR = np.where(yR, 3 * c, 0.3 * c)
    s1 = K.lobe_split_class(yL, yR, far, xR)
    assert s1["class"] == "S1" and s1["k"] == 3
    yR[3] = ~yR[3]
    xR = np.where(yR, 3 * c, 0.3 * c)
    s2a = K.lobe_split_class(yL, yR, far, xR)
    assert s2a["class"] == "S2a" and s2a["k"] == 4 and s2a["j_near_cut"] == 0
    xR2 = xR.copy()
    xR2[3] = 1.5 * c                                   # one differing cell inside the band, lobe R only
    s2b = K.lobe_split_class(yL, yR, far, xR2)
    assert s2b["class"] == "S2b" and s2b["j_near_cut"] == 1
    assert s2b["text"].startswith("Block A differs between the lobes in 4 of 64 cells")
    assert s2b["direction"]["outside_R_only"] == 33
    com = K.split_class_committed(s2b)
    assert set(com["differing_cells"][0]) == {"cell", "present_L", "present_R"}


# ------------------------------------------------------------------------------------------
# T10: seeds and refusals.

def test_T10_seeds(monkeypatch):
    s = K.assert_seeds_unique(10)
    assert s["new_seeds"] == 67 and s["world_seeds"] == [92100, 92184]
    assert (K.SEED_PERM, K.SEED_RC, K.SEED_PERM_CEIL, K.SEED_WORLD) == (92000, 92001, 92010, 92100)
    assert not {92000, 92001} & (K.A_SEEDS | K.B_SEEDS)
    monkeypatch.setattr(K, "SEED_PERM", 90000)         # an A seed
    with pytest.raises(SystemExit, match="SEEDS NOT UNIQUE"):
        K.assert_seeds_unique(10)


def test_T10_refusals(monkeypatch):
    called = []
    monkeypatch.setattr(K, "check_pins", lambda *a, **k: called.append(1))
    with pytest.raises(SystemExit, match="--allow-dirty is refused with --arm malecns"):
        K.main(["--arm", "malecns", "--allow-dirty"])
    with pytest.raises(SystemExit, match="--lobe is for --synthetic-only"):
        K.main(["--arm", "malecns", "--lobe", "L"])
    with pytest.raises(SystemExit, match="needs --lobe"):
        K.main(["--synthetic-only"])
    with pytest.raises(SystemExit, match="runs as registered"):
        K.main(["--arm", "malecns", "--smoke-worlds", "1"])
    with pytest.raises(SystemExit, match="still placeholders"):
        K.main(["--arm", "malecns"])                   # the pins of the pre-run are not set
    assert called == []


def test_T10_out_guard_on_four_references(tmp_path, monkeypatch):
    refs = {}
    for name in ("A", "B", "L", "R"):
        d = tmp_path / f"ref_{name}"
        d.mkdir()
        (d / "synthetic_worlds.csv").write_bytes(f"reference {name}".encode())
        refs[name] = d
    pin = {n: {"synthetic_worlds.csv": hashlib.sha256(f"reference {n}".encode()).hexdigest()}
           for n in refs}
    monkeypatch.setattr(K, "A_PRERUN_DIR", refs["A"])
    monkeypatch.setattr(K, "A_PRERUN_SHA256", pin["A"])
    monkeypatch.setattr(K, "B_PRERUN_DIR", refs["B"])
    monkeypatch.setattr(K, "B_PRERUN_SHA256", None)
    for lobe in K.LOBES:
        monkeypatch.setitem(K.PRERUN_DIR, lobe, refs[lobe])
        monkeypatch.setitem(K.PRERUN_SHA256, lobe, pin[lobe])
    for name, d in refs.items():
        assert "reference folder or inside it" in K.out_dir_refusal(d)
        assert "reference folder or inside it" in K.out_dir_refusal(d / "x")
    for name in ("A", "L", "R"):                       # B has no pins: path guard only
        copy = tmp_path / f"copy_{name}"
        copy.mkdir()
        (copy / "synthetic_worlds.csv").write_bytes(f"reference {name}".encode())
        assert "byte copy" in K.out_dir_refusal(copy)
    copyB = tmp_path / "copy_B"
    copyB.mkdir()
    (copyB / "synthetic_worlds.csv").write_bytes(b"reference B")
    assert K.out_dir_refusal(copyB) is None
    assert K.out_dir_refusal(tmp_path / "fresh") is None


# ------------------------------------------------------------------------------------------
# T11: checks 3 and 5 are prints.

def test_T11_checks_3_and_5_print(lobe_L, capsys):
    bank, _ = lobe_L
    y = np.zeros(64, bool)
    y[[0, 3, 5, 9, 17, 20, 33, 40, 41, 50, 60, 63]] = True   # not a board, not balanced
    c3 = K.check_block_print(y, "R")
    assert not c3["stops_lobe"] and c3["has_auc"] and not c3["y_equals_x_times_w"]
    assert c3["present"] == 12 and not c3["balanced"]
    assert sum(c3["quadrants"].values()) == 12 and sum(c3["row_counts"].values()) == 12
    assert "check 3 (block print, lobe R): present 12/64" in capsys.readouterr().out
    n1 = H.fit_n1(H.make_view(K.fill_block(bank, y, "t11"), K.MASKS["ko"]))
    c5 = K.check_n1_parity(n1, y)
    assert c5["D_N1_logit"] is not None and c5["passed"] is None and not c5["balanced"]
    assert K.block_pattern(board("z"))["balanced"] and K.block_pattern(board("z"))["y_equals_x_times_w"]


# ------------------------------------------------------------------------------------------
# T12: the p_S print (S28).

def _ev_with_shuffles(n_deg):
    """A fixture evaluation: the block is the board z; every predictor but N1 ranks it
    perfectly and N1 is noise, so the real margin is large; of the 99 shuffles, n_deg have no
    AUC (all absent), and on the rest N1 is perfect and the others are noise, so no shuffle's
    margin reaches the real one (n_ge = 0)."""
    y = board("z")
    rng = np.random.default_rng(5)
    F = {}
    rec = {"y": y.tolist(), "score": {"existence": 0.3, "offset": 1.0, "counts": 0.5, "sign": 1.0},
           "outside_density": 0.17}
    p_n1 = rng.random(64).tolist()
    for mk in ("ko", "full", "block", "ko1"):
        for pk in K.PRED_KEYS:
            F[("b", mk, pk)] = {**rec, "p": p_n1 if pk == "N1" else (0.2 + 0.6 * y).tolist(),
                                "lam": None if pk == "N1" else 1.0}
    for sd in range(99):
        ys = np.zeros(64, bool) if sd < n_deg else y
        for pk in K.PRED_KEYS:
            p = (0.2 + 0.6 * ys) if pk == "N1" else rng.random(64)
            F[(f"b|sh:{sd}", "ko", pk)] = {**rec, "y": ys.tolist(), "p": list(p), "lam": 1.0}
    return K.evaluate_bank("b", F, 99, 0, "synthetic")


def test_T12_p_S_print():
    ev = _ev_with_shuffles(1)
    r = ev["rows"]["rule"]
    assert r["n_deg"] == 1 and r["n_ge"] == 0 and r["leg_S_passes"] and r["n_valid_shuffles"] == 98
    line = K.verdict_line(ev, DL, U_KEPT)
    assert ("p_S = 0.0101 [leg S decided by the count: n_ge = 0 of 98] (n_ge = 0 of 98, "
            "n_deg = 1)") in line
    assert "0.0101 [leg S decided by the count" in "\n".join(K.md_bank_table(ev))
    ev0 = _ev_with_shuffles(0)
    line0 = K.verdict_line(ev0, DL, U_KEPT)
    assert "p_S = 0.01 (n_ge = 0 of 99, n_deg = 0)" in line0 and "[leg S" not in line0
    lob = K.verdict_line(ev0, DL, U_KEPT, lobe="L")
    assert lob.startswith("male CNS, lobe L (existence bank at c* = 2.99436): ")


# ------------------------------------------------------------------------------------------
# T13 (revision 1.2, section 3.3.1): the registered references themselves.

KO1_REGISTERED = {"L": {"ko1_records": 225, "copied_from_ko": 46, "fitted": 179},
                  "R": {"ko1_records": 225, "copied_from_ko": 49, "fitted": 176}}


def test_T13_the_registered_references_verify():
    """The real pinned references of both lobes (outside the repository; synthetic worlds only,
    no sealed file is read, and the seal guard checks it) are accepted by the registered run's
    reference mode: every file listed in SHA256SUMS.txt matches its listed and pinned sha256
    and nothing else lies in the folder; the worlds CSV pin is the listed one; the registered
    smallest_passing_auc (equal in both lobes) and ko1 count derive from them; each was made by
    a full, clean pre-run at a0e16b6 that touched no sealed file; --out is refused at the
    reference and at the pre-run folder it was copied from; and the only placeholder left is
    A's amended hash, so --arm malecns still refuses (D15 step 4)."""
    for lobe in K.LOBES:
        d = K.PRERUN_DIR[lobe]
        if not d.is_dir():
            pytest.skip(f"the reference folder {d} is not on this machine")
        assert K.reference_mode(lobe)
        files = K.check_prerun_files(lobe)
        assert files["passed"] and files["unlisted"] == [], files["reason"]
        assert set(files["files"]) == set(K.PRERUN_FILES)
        assert K.PRERUN_WORLDS_CSV_SHA256[lobe] == K.PRERUN_SHA256[lobe]["synthetic_worlds.csv"]
        spa = K.derive_smallest_passing_auc(d / "synthetic_only.json")
        assert spa["passed"] and spa["by_board"] == {"z": 0.671875, "z'": 0.669921875}
        assert spa["by_board"] == K.board_smallest_passing_auc()
        assert spa["n_worlds_by_board"] == {"z": 40, "z'": 5}
        assert K.registered_ko1_count(K.read_raw(d / "raw_fits.json.gz")) == KO1_REGISTERED[lobe]
        man = json.loads((d / "synthetic_only.json").read_text(encoding="utf-8"))["manifest"]
        assert man["git_head"] == "a0e16b696389fb796a9f3b95c308358b52dd9dc8"
        assert man["tree_dirty_under_c6_or_plans"] is False and man["allow_dirty"] is False
        assert man["sealed_files_touched"] is False and man["not_a_reference"] is None
        assert man["smoke"] is False and man["starts"] == 10 and man["lobes"] == [lobe]
        assert man["reference_mode"] is False and man["from_raw"] is None
        assert "reference folder or inside it" in K.out_dir_refusal(d)
        origin = K.PRIVATE_ROOT / f"malecns_prerun_{lobe}_20260926T131249Z"
        if origin.is_dir():
            assert "byte copy" in K.out_dir_refusal(origin)
    left = K.placeholders_unset()
    assert len(left) == 1 and left[0].startswith("A_REGISTRATION_SHA256_LF_AMENDED")
    with pytest.raises(SystemExit, match="still placeholders: A_REGISTRATION_SHA256_LF_AMENDED"):
        K.check_registered_constants()


# ------------------------------------------------------------------------------------------
# T14 (revision 1.3): S29-S32.

def male_like_worlds():
    """Dense-grid worlds shaped like lobe L's pre-run: gamma*_P = gamma_R = family limit = 0.75
    (the band is empty); U at 0.5 (3), 0.6 (3), 0.75 (1); one W and one G at 0.85."""
    labels = {"M0.5": "GUUGU", "M0.6": "GURUU", "M0.75": "RRRUR", "M0.85": "RRRWG",
              "M1.0": "RRRRR"}
    seen = {"M0.5": 0, "M0.6": 2, "M0.75": 5, "M0.85": 4, "M1.0": 5}
    fam_i = {f[0]: i for i, f in enumerate(K.FAMILIES)}
    out = []
    for fam, labs in labels.items():
        for j, lab in enumerate(labs):
            p = 0.0001 if j < seen[fam] else 0.5
            rows = {pk: {"p_P": p, "auc": 0.525390625 if lab == "G" else 0.8, "lambda_ko": 3.0,
                         "n_ge": 1 if lab == "W" else 0, "n_valid_shuffles": 99}
                    for pk in K.LIMIT_KEYS}
            out.append({"family": fam, "j": j, "seed": 92100 + 10 * fam_i[fam] + j,
                        "board": "z", "label": lab, "rows": rows,
                        "U_reasons": [LEGS] if lab == "U" else []})
    return out


def _reference_json(lobe):
    d = K.PRERUN_DIR[lobe]
    if not d.is_dir():
        pytest.skip(f"the reference folder {d} is not on this machine")
    return json.loads((d / "synthetic_only.json").read_text(encoding="utf-8"))


def test_T14_S29_u_reading_with_an_empty_band():
    ws = male_like_worlds()
    dl = K.detection_limits(ws, 10)
    assert dl["leg_P"]["gamma"] == dl["R"]["gamma"] == dl["family"]["gamma"] == 0.75
    assert dl["band"]["steps"] == 0
    u = {"label": "U", "U_reasons": [LEGS]}
    line = K.male_u_reading_line(u, "L", dl, U_KEPT, ws)
    assert "7 dense-grid U worlds lie at gamma 0.5: 3, 0.6: 3, 0.75: 1" in line
    assert ": 1 at it, 0 above it)" in line and "The band is empty" in line
    assert "\"not detected at the R level: the two legs, or the two D1 candidates, disagree\"" in line
    assert "does not hold on this lobe" in line
    # other U kinds keep their own texts; a renamed U, a G or an R gets no line
    assert K.male_u_reading_line({"label": "U", "U_reasons": [K.ceiling_block_reason(0.5)]},
                                 "L", dl, U_KEPT, ws) is None
    assert K.male_u_reading_line({"label": "U", "U_reasons": [K.not_readable_reason(1)]},
                                 "L", dl, U_KEPT, ws) is None
    assert K.male_u_reading_line(u, "L", dl, U_RENAMED, ws) is None
    assert K.male_u_reading_line({"label": "G", "U_reasons": []}, "L", dl, U_KEPT, ws) is None
    # A's shape (a one-step band): the frozen male reading is not claimed
    a_line = K.male_u_reading_line(u, "L", DL, U_KEPT, fake_worlds())
    assert "The band is not empty on this lobe" in a_line and "does not hold" not in a_line


def test_T14_S29_on_the_registered_references():
    want = {"L": "7 dense-grid U worlds lie at gamma 0.5: 3, 0.6: 3, 0.75: 1",
            "R": "5 dense-grid U worlds lie at gamma 0.5: 2, 0.6: 1, 0.75: 2"}
    for lobe in K.LOBES:
        so = _reference_json(lobe)
        line = K.male_u_reading_line({"label": "U", "U_reasons": [LEGS]}, lobe, so["limits"],
                                     so["u_rule"], so["worlds"])
        assert want[lobe] in line and "The band is empty" in line, line


def test_T14_S31_instrument_line_beside_a_male_g():
    ws = male_like_worlds()
    syn = {"limits": K.detection_limits(ws, 10), "worlds": ws}
    line = K.male_g_instrument_line("L", syn)
    assert "0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5" in line
    assert f"(A: {K.A_CURVE_TEXT})" in line and "gamma*_P = 0.75 (A 0.6)" in line
    assert "M0.85 seed 92184 (rule #2.1 AUC 0.5254, p_P 0.5000)" in line
    assert "M0.85 seed 92183 (rule #2.1 n_ge = 1 of 99)" in line


def test_T14_S31_on_the_registered_references():
    want = {"L": ("0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5",
                  "M0.85 seed 92184 (rule #2.1 AUC 0.5254, p_P 0.3695)",
                  "read W: M0.85 seed 92183 (rule #2.1 n_ge = 1 of 99)"),
            "R": ("0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5",
                  "M0.85 seed 92184 (rule #2.1 AUC 0.5420, p_P 0.2872)", "read W: none")}
    for lobe in K.LOBES:
        so = _reference_json(lobe)
        line = K.male_g_instrument_line(lobe, so)
        assert all(x in line for x in want[lobe]), line


def _pair_syn(lab_L, lab_R):
    def worlds(labs):
        return [{"family": fam, "seed": sd, "board": b, "label": lab}
                for (fam, sd, b), lab in zip(SEEDS_T14, labs)]
    return {"L": {"worlds": worlds(lab_L)}, "R": {"worlds": worlds(lab_R)}}


SEEDS_T14 = [("R", 92100, "z"), ("No", 92120, "z'"), ("M0.5", 92142, "z"), ("M0.85", 92183, "z")]


def test_T14_S32_two_notions_of_split():
    syn = _pair_syn("RGUW", "RGRR")
    reading = K.male_reading({"L": st("U"), "R": st("R")})
    yL = board("z")
    same = K.lobe_split_class(yL, yL, np.where(yL, 9.0, 0.2), np.where(yL, 9.0, 0.2))
    n = K.split_notions(reading, same, syn)
    assert n["by_reading"]["split"] and n["by_block"]["class"] == "S0"
    assert n["by_block"]["blocks_differ"] is False and n["by_block"]["k"] == 0
    assert ("2 of 2 dense-grid world pairs split by reading (seed 92142 U/R, seed 92183 W/R), "
            "0 of 2 axis-family pairs; every world pair has k = 0") in n["text"]
    assert n["text"].startswith("Split by reading (section 4.2, D3): yes: split: lobe L reads U")
    assert "Block difference (section 4.3, by block): class S0, k = 0 of 64 cells differ" in n["text"]
    agree = K.split_notions(K.male_reading({"L": st("G"), "R": st("G")}), None, syn)
    assert not agree["by_reading"]["split"] and agree["by_block"]["class"] is None


def test_T14_S32_on_the_registered_references():
    syn = {lobe: _reference_json(lobe) for lobe in K.LOBES}
    n = K.split_notions(K.male_reading({"L": st("G"), "R": st("G")}), None, syn)
    assert n["worlds"]["text"] == (
        "5 of 25 dense-grid world pairs split by reading (seed 92142 U/R, seed 92161 U/G, seed "
        "92164 U/R, seed 92172 R/U, seed 92183 W/R), 0 of 20 axis-family pairs; every world pair "
        "has k = 0 (the same board in both lobes)")


def test_T14_S30_prerun_provenance(monkeypatch):
    for lobe in K.LOBES:
        if not K.PRERUN_DIR[lobe].is_dir():
            pytest.skip(f"the reference folder {K.PRERUN_DIR[lobe]} is not on this machine")
        pv = K.prerun_provenance(lobe, "f" * 40, "e" * 64)
        assert pv["passed"] and not pv["same_script"]
        assert pv["prerun_git_head"] == K.PRERUN_GIT_HEAD == (
            "a0e16b696389fb796a9f3b95c308358b52dd9dc8")
        assert pv["prerun_script_sha256_lf"] == K.PRERUN_SCRIPT_SHA256_LF == (
            "7a09f9fdfee38d93596fe0be9ffd4daab5b82cb287acdfa4a16bbdd4a3a281fc")
        assert pv["text"].startswith(f"lobe {lobe}: pre-run made by head a0e16b6, script "
                                     "7a09f9fd (LF sha256 7a09f9fd")
        assert "; this run by head fffffff, script eeeeeeee (LF sha256 " in pv["text"]
        assert "different code" in pv["text"]
    monkeypatch.setattr(K, "PRERUN_SCRIPT_SHA256_LF", "0" * 64)
    bad = K.prerun_provenance("L", "f" * 40, "e" * 64)
    assert not bad["passed"] and "registered" in bad["reason"]


if __name__ == "__main__":
    sys.exit(pytest.main(["-p", "no:cacheprovider", "-v", __file__]))
