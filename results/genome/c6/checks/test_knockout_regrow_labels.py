"""Positive control for the verdict text of knockout_regrow.py (registration
docs/plans/2026-09-24-knockout-regrow-registration.md, revision 3.2, item A2; Johnny, DPC Research
chat, 2026-09-25 12:46-12:48 UTC).

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
    assert K.label_text("U", DL, U_RENAMED, [K.ceiling_block_reason(None), LEGS]) == FAILED


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


def test_mechanism_description_names_rule_ceiling_full():
    assert K.mechanism_description({"ceiling_full": 0.5088}) == (
        "orthogonal (rule #2.1's ceiling_full = 0.5088 < 0.90)")
    assert K.GATE_CUT == K.MECHANISM_CUT == 0.90


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
    tiny = K.csv_compare(ref, _csv([_row(D=0.123456789 + 5e-10)]))
    assert tiny["outcome"] == 2 and tiny["passed"] and "D" in tiny["continuous_within_tolerance"]
    big = K.csv_compare(ref, _csv([_row(D=0.123456789 + 1e-6)]))
    assert big["outcome"] == 3 and not big["passed"]
    lat = K.csv_compare(ref, _csv([_row(p_P="0.0107")]))
    assert lat["outcome"] == 3 and lat["first_exact_differences"][0]["columns"] == ["p_P"]
    lab = K.csv_compare(ref, _csv([_row(label="U")]))
    assert lab["outcome"] == 3
    assert K.csv_compare(ref, _csv([_row(), _row()]))["outcome"] == 3


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main(["-p", "no:cacheprovider", "-v", __file__]))
