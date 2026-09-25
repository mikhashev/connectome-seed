"""Positive control for the verdict text of knockout_regrow.py (registration
docs/plans/2026-09-24-knockout-regrow-registration.md, revision 3.2, item A2; Johnny, DPC Research
chat, 2026-09-25 12:46-12:48 UTC; extended in revision 3.3).

The failed-fit branch of U (rule #2.1's ceiling_block below the gate) never ran in the pre-run:
ceiling_block was 1.0 in all 225 rule and BF rows. These tests call label_text directly with
injected reasons, and once through read_label, and check:
  (i)   a ceiling_block reason gives the failed-fit text;
  (ii)  the same with the U rule's rename still gives the failed-fit text;
  (iii) a threshold U without that reason gives the threshold text (or the renamed text);
  (iv)  the G text is revision 3.1's apart from A5 (it names its gate variable) and the
        vocabulary of item C ("leg P").
Also: the mechanism description names rule #2.1's ceiling_full (A5), and the reproduction gate
(csv_compare, A1) gives outcomes 1, 2 and 3 on hand-made tables.
Revision 3.3: a ceiling_block that was not measured gives its own U text, not the failed fit
(A4); the printed cuts move when GATE_CUT and MECHANISM_CUT move (A5); the U rule counts threshold
U only (A3); csv_compare matches rows by key, reports order and missing rows apart, splits outcome
3 into parts (a) and (b), and checks column 8 against revision 3.2's rename (items 27, F1, C5);
and --out is refused at or inside a pre-run folder, on a byte copy of it, and with --arm (A2). The
refusal tests use a temporary folder with monkeypatched PRERUN_DIR and PRERUN_SHA256; they never
touch the real pre-run folder.

It imports the script as a module (which reads the pins and imports the harness, both read-only)
and fits nothing. Run: tools/.venv/Scripts/python.exe -m pytest -p no:cacheprovider -v
results/genome/c6/checks/test_knockout_regrow_labels.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import knockout_regrow as K  # noqa: E402


def fake_worlds():
    """Dense-grid worlds shaped like the pre-run table: gamma*_P = 0.6, gamma_R = 0.75."""
    labels = {"M0.5": "RGGGG", "M0.6": "RRUUU", "M0.75": "RRRRR", "M0.85": "RRRRR",
              "M1.0": "RRRRR"}
    seen = {"M0.5": 1, "M0.6": 3, "M0.75": 5, "M0.85": 5, "M1.0": 5}
    out = []
    for fam, labs in labels.items():
        for j, lab in enumerate(labs):
            p = 0.0001 if j < seen[fam] else 0.5
            rows = {pk: {"p_P": p, "auc": 0.8, "lambda_ko": 3.0} for pk in K.LIMIT_KEYS}
            out.append({"family": fam, "seed": 90000 + j, "label": lab, "rows": rows})
    return out


DL = K.detection_limits(fake_worlds(), 10)
U_KEPT = {"renamed": False}
U_RENAMED = {"renamed": True}
FAILED = f"U: {K.FAILED_FIT_TEXT}"
LEGS = "the legs disagree for rule #2.1: leg S n_ge = 0 of 99, leg P p_P = 0.0308"


def test_fixture_limits():
    assert DL["leg_P"]["gamma"] == 0.6 and DL["R"]["gamma"] == 0.75


def test_i_ceiling_block_reason_gives_failed_fit():
    assert K.label_text("U", DL, U_KEPT, [K.ceiling_block_reason(0.85)]) == FAILED
    # whatever else is listed
    assert K.label_text("U", DL, U_KEPT, [LEGS, K.ceiling_block_reason(0.85)]) == FAILED


def test_ii_rename_never_applies_to_failed_fit():
    assert K.label_text("U", DL, U_RENAMED, [K.ceiling_block_reason(0.85)]) == FAILED
    assert K.label_text("U", DL, U_RENAMED, [LEGS, K.ceiling_block_reason(0.85)]) == FAILED


def test_ii_not_measured_is_not_a_failed_fit():
    """Revision 3.3 (A4): a missing ceiling_block has its own reason and its own U text; it is
    not "n/a is below 0.90", not the failed fit, and the U rule's rename never applies to it."""
    r = K.ceiling_block_reason(None)
    assert r == K.CEILING_BLOCK_NOT_MEASURED and "n/a" not in r and "below" not in r
    assert not r.startswith(K.CEILING_BLOCK_REASON)
    nm = f"U: {K.NOT_MEASURED_TEXT}"
    for u in (U_KEPT, U_RENAMED):
        assert K.label_text("U", DL, u, [r, LEGS]) == nm != FAILED
    # a failed fit still wins over a not-measured reason
    assert K.label_text("U", DL, U_KEPT, [r, K.ceiling_block_reason(0.85)]) == FAILED


def test_iii_threshold_u_without_the_reason():
    t = K.label_text("U", DL, U_KEPT, [LEGS])
    assert t == (f"U: {K.U_THRESHOLD} (at the leg-P detection limit gamma*_P = 0.6; "
                 f"transition band {DL['band']['text']})")
    assert K.FAILED_FIT_TEXT not in t
    assert K.label_text("U", DL, U_RENAMED, [LEGS]) == (
        f"U: {K.U_UNCALIBRATED}; never read as a finding")
    assert K.label_text("U", DL, U_KEPT, []).startswith(f"U: {K.U_THRESHOLD}")


def test_iv_g_text():
    g = K.label_text("G", DL, U_KEPT, [], 1.0)
    gate = "gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; "
    assert g == f"G: not detected at the R level above gamma_R ({gate}{K.limits_text(DL)})"
    # Without the A5 clause it is revision 3.1's G text (with "leg P" for "weak leg", item C).
    assert g.replace(gate, "") == (
        f"G: not detected at the R level above gamma_R ({K.limits_text(DL)})")
    assert "leg P from gamma*_P = 0.6" in g and "weak" not in g
    # reasons never change G
    assert K.label_text("G", DL, U_RENAMED, [K.ceiling_block_reason(0.5)], 1.0) == g


def test_read_label_failed_fit_end_to_end():
    """read_label on hand-made rows with ceiling_block = 0.85 and no predictor near leg P."""
    rows = {pk: {"leg_S_passes": False, "p_P": 0.5, "n_ge": 40, "n_valid_shuffles": 99,
                 "ceiling_block": 0.85 if pk == "rule" else 1.0, "ceiling_full": 0.95}
            for pk in K.PRED_KEYS}
    lab = K.read_label(rows)
    assert lab["label"] == "U"
    assert lab["U_reasons"] == [K.ceiling_block_reason(0.85)]
    assert lab["U_reasons"][0] == ("rule #2.1's ceiling_block = 0.8500 is below 0.90: the rule "
                                   "cannot hold the block even when trained on it alone")
    assert K.label_text(lab["label"], DL, U_RENAMED, lab["U_reasons"], 0.85) == FAILED
    rows["rule"]["ceiling_block"] = 1.0
    lab = K.read_label(rows)
    assert lab["label"] == "G"
    assert lab["mechanism_description"] == (
        "no information (rule #2.1's ceiling_full = 0.9500 >= 0.90)")


def test_mechanism_description_names_rule_ceiling_full(monkeypatch):
    assert K.mechanism_description({"ceiling_full": 0.5088}) == (
        "orthogonal (rule #2.1's ceiling_full = 0.5088 < 0.90)")
    # Revision 3.3 (A5): a probe, not an equality pin. Move each cut to 0.95 and the printed
    # text must move with it; monkeypatch restores both afterwards.
    before_g = K.ceiling_block_reason(0.85)
    before_t = K.label_text("G", DL, U_KEPT, [], 1.0)
    assert K.mechanism_description({"ceiling_full": 0.92}) == (
        "no information (rule #2.1's ceiling_full = 0.9200 >= 0.90)")
    monkeypatch.setattr(K, "MECHANISM_CUT", 0.95)
    monkeypatch.setattr(K, "GATE_CUT", 0.95)
    assert K.mechanism_description({"ceiling_full": 0.92}) == (
        "orthogonal (rule #2.1's ceiling_full = 0.9200 < 0.95)")
    moved_g = K.ceiling_block_reason(0.85)
    assert moved_g != before_g and "is below 0.95" in moved_g
    g = K.label_text("G", DL, U_KEPT, [], 1.0)
    assert g != before_t and "ceiling_block = 1.0000 >= 0.95" in g


def test_u_rule_counts_threshold_u_only():
    """Revision 3.3 (A3): failed-fit and not-measured U neither keep nor rename U."""
    def worlds(reasons):
        return [{"family": "M0.6", "seed": 90160 + j, "label": "U", "U_reasons": r}
                for j, r in enumerate(reasons)]
    failed = worlds([[K.ceiling_block_reason(0.85)], [K.ceiling_block_reason(None)]])
    ur = K.u_rule(failed)
    assert (ur["n_u_threshold"], ur["n_u_failed"], ur["n_u_not_measured"]) == (0, 1, 1)
    assert ur["renamed"] and ur["dense_grid_U"] == 2
    ur = K.u_rule(failed + worlds([[LEGS]]))
    assert ur["n_u_threshold"] == 1 and not ur["renamed"]


def _csv(rows):
    import csv
    import io
    fh = io.StringIO(newline="")
    w = csv.writer(fh)
    w.writerow(K.WORLDS_CSV_HEADER)
    for r in rows:
        w.writerow([r[c] for c in K.WORLDS_CSV_HEADER])
    return fh.getvalue().encode("utf-8")


def _row(**kw):
    r = {c: "0.5" for c in K.WORLDS_CSV_HEADER}
    r.update(family="Nf", j=0, seed=90110, predictor="rule #2.1", label="G",
             mechanism_description="orthogonal (ceiling_full 0.5088 < 0.90)", D=0.123456789)
    r.update(kw)
    return r


def test_csv_compare_outcomes():
    ref = _csv([_row()])
    same = K.csv_compare(ref, ref)
    assert same["outcome"] == 1 and same["passed"] and same["byte_identical"]
    mech = K.csv_compare(ref, _csv([_row(mechanism_description="orthogonal (rule #2.1's "
                                                               "ceiling_full = 0.5088 < 0.90)")]))
    assert mech["outcome"] == 1 and mech["passed"] and not mech["byte_identical"]
    assert mech["mechanism_description_differences"] == 1
    # revision 3.3 (C5): that difference is exactly revision 3.2's rename
    assert mech["mechanism_description_explained_by_rename_3_2"] == 1
    assert mech["mechanism_description_all_explained_by_rename_3_2"]
    other = K.csv_compare(ref, _csv([_row(mechanism_description="orthogonal (rule #2.1's "
                                                                "ceiling_full = 0.5000 < 0.90)")]))
    assert other["outcome"] == 1 and other["mechanism_description_unexplained"] == 1
    assert not other["mechanism_description_all_explained_by_rename_3_2"]
    tiny = K.csv_compare(ref, _csv([_row(D=0.123456789 + 5e-10)]))
    assert tiny["outcome"] == 2 and tiny["passed"] and "D" in tiny["continuous_within_tolerance"]
    big = K.csv_compare(ref, _csv([_row(D=0.123456789 + 1e-6)]))
    assert big["outcome"] == 3 and not big["passed"] and big["outcome_3_parts"] == ["b"]
    lat = K.csv_compare(ref, _csv([_row(p_P="0.0107")]))
    assert lat["outcome"] == 3 and lat["first_exact_differences"][0]["columns"] == ["p_P"]
    assert lat["outcome_3_parts"] == ["a"]
    both = K.csv_compare(ref, _csv([_row(p_P="0.0107", D=0.123456789 + 1e-6)]))
    assert both["outcome_3_parts"] == ["a", "b"]
    lab = K.csv_compare(ref, _csv([_row(label="U")]))
    assert lab["outcome"] == 3
    dup = K.csv_compare(ref, _csv([_row(), _row()]))
    assert dup["outcome"] == 3 and dup["n_duplicate_keys"] == 1


def test_csv_compare_by_key():
    """Revision 3.3 (item 27): rows are matched by (family, j, seed, predictor). A change of
    row order is recorded and is not outcome 3; a missing row on either side is."""
    r1, r2 = _row(), _row(predictor="BF_1", D=0.5)
    ref = _csv([r1, r2])
    swapped = K.csv_compare(ref, _csv([r2, r1]))
    assert swapped["outcome"] == 1 and swapped["row_order_differs"]
    assert swapped["exact_differences"] == 0 and not swapped["byte_identical"]
    assert not K.csv_compare(ref, ref)["row_order_differs"]
    short = K.csv_compare(ref, _csv([r1]))
    assert short["outcome"] == 3 and short["outcome_3_parts"] == ["a"]
    assert short["rows_missing_now"] == [["Nf", "0", "90110", "BF_1"]]
    extra = K.csv_compare(_csv([r1]), ref)
    assert extra["outcome"] == 3 and extra["n_rows_missing_prerun"] == 1
    assert K.repro_fail_treatment(["b"]) != K.repro_fail_treatment(["a"])
    assert "layer (2) is not the cause" in K.repro_fail_treatment(["b"])


def _fake_prerun(tmp_path, monkeypatch):
    """A throwaway pre-run folder with made-up files; PRERUN_DIR and PRERUN_SHA256 point at it."""
    import hashlib
    ref = tmp_path / "prerun"
    ref.mkdir()
    pins = {}
    for n in K.PRERUN_SHA256:
        (ref / n).write_bytes(f"fake {n}".encode())
        pins[n] = hashlib.sha256(f"fake {n}".encode()).hexdigest()
    monkeypatch.setattr(K, "PRERUN_DIR", ref)
    monkeypatch.setattr(K, "PRERUN_SHA256", pins)
    return ref


def test_out_guard_refusals(tmp_path, monkeypatch):
    """Revision 3.3 (A2, C4): the --out guard, on a temporary folder only."""
    import shutil
    ref = _fake_prerun(tmp_path, monkeypatch)
    assert K.out_dir_refusal(None) is None
    assert "reference folder or inside it" in K.out_dir_refusal(ref)
    assert "inside it" in K.out_dir_refusal(ref / "sub" / "dir")
    assert "inside it" in K.out_dir_refusal(ref / ".." / ref.name)
    assert "with --arm" in K.out_dir_refusal(tmp_path / "new", arm="flyvis65")
    # a byte copy elsewhere is refused; one pinned-name file is enough
    copy = tmp_path / "copy"
    shutil.copytree(ref, copy)
    assert "byte copy" in K.out_dir_refusal(copy)
    one = tmp_path / "one"
    one.mkdir()
    shutil.copy2(ref / "raw_fits.json.gz", one / "raw_fits.json.gz")
    assert "byte copy" in K.out_dir_refusal(one)
    # a present pinned-name file that differs makes the folder writable; missing is not different
    (copy / "raw_fits.json.gz").write_bytes(b"a fresh gzip with another mtime")
    assert K.out_dir_refusal(copy) is None
    (tmp_path / "empty").mkdir()
    assert K.out_dir_refusal(tmp_path / "empty") is None
    assert K.out_dir_refusal(tmp_path / "does_not_exist") is None
    other = tmp_path / "other"
    other.mkdir()
    (other / "notes.txt").write_text("unrelated")
    assert K.out_dir_refusal(other) is None


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main(["-p", "no:cacheprovider", "-v", __file__]))
