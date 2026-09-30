#!/usr/bin/env python3
"""The symmetric pair: block A at lambda = 100 (a new fit) and block B's verdict with the block
lambda at 1 (a reading, no fit).

Implements docs/plans/2026-09-30-symmetric-lambda-pair-registration.md, revision 1 (section numbers
below refer to it). Nothing registered or hashed is edited; no fit, search, AUC, tie rule or label
function is re-implemented: block_b_ceil1.py (B1), the calibration (C), the replication's refusals
(R), block B's script (K) and block A's script (KA) are imported.

Object 1: rule #2.1's block-only fit on the real block A at lambda 100 (ceil_100_A, quantised and
float) and cert_A; control: the same route at lambda = 1 must equal A's stored ceiling_block.
Object 2: KA.read_label / K.read_label with their label_text are called on each block's stored
verdict objects (summary.json) with ONLY rule #2.1's ceiling_block replaced (B by ceil_1 from
block_b_ceil1/result.json, A by ceil_100_A).

C's fit and cert functions read block B's shapes from K (K.MASKS, K.BLOCK_CELLS, K.N_SOURCES,
K.N_TARGETS) at call time, so as_block_A swaps those K names to block A's for one call and restores
them; fit.py and the harness are untouched.

Run forms (PYTHONUTF8=1, from the repository root; the second needs the owner's yes):
    tools/.venv/Scripts/python.exe results/genome/c6/checks/symmetric_lambda_pair.py --dry-run
    tools/.venv/Scripts/python.exe results/genome/c6/checks/symmetric_lambda_pair.py
Refuses while REGISTRATION_SHA256_LF_PINNED or PREDICTION_COMMIT_PINNED is None or differs, while
`git status --porcelain` is not empty, and if an output exists. Order: refusals, input hashes, gate
and the two reading controls (no fit), CONTROL (else CONTROL_FAILED, nothing else computed), cert_A,
ceil_100_A, section 3.1, section 3.2, outputs (with git HEAD and the porcelain text). ASCII output.
"""
import sys

import argparse
import contextlib
import copy
import gzip
import hashlib
import json
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import block_b_ceil1 as B1  # noqa: E402  (imports C, R, K; sets UTF-8 streams)
import knockout_regrow as KA  # noqa: E402  (block A's script; imports the same harness H)

C, R, K, H = B1.C, B1.R, B1.K, B1.H
ROOT = C.ROOT

REGISTRATION = "docs/plans/2026-09-30-symmetric-lambda-pair-registration.md"
REGISTRATION_REVISION = "1"
# None = the script refuses; set in the script pin commit (section 7).
REGISTRATION_SHA256_LF_PINNED = "8865753ee1c7d9c946d434e08d7227c1f29ae0500fef6339f1b22e55fe507808"
PREDICTION_COMMIT_PINNED = "e7d973f63cf2d1ae49013d376bb9aaf8f0401a8b"

A_SCRIPT = "results/genome/c6/checks/knockout_regrow.py"
A_SCRIPT_SHA256_LF = "113c4526000f77d773b5db57890554e8a8797587683ce3f31f991d9cc77bb9dc"
B1_SCRIPT = "results/genome/c6/checks/block_b_ceil1.py"
B1_SCRIPT_SHA256_LF = "e4b85ff168f33614c8bb7c9132267054024153752bac26dc50d1263d6355391b"
B_SUMMARY = "results/genome/c6/checks/knockout_regrow_block_b/summary.json"
B_SUMMARY_SHA256_LF = "a43e0319bf040d421e6a7d1ef5f7e34131bb4d862b34cf4fa4e1441c2592f520"
A_SUMMARY = "results/genome/c6/checks/knockout_regrow/summary.json"
A_SUMMARY_SHA256_LF = "1337c57728bb54ed27a1413e78a0107bc6b874dbf96a61d5c25fc2fe7760a82c"
B_CEIL1_RESULT = "results/genome/c6/checks/block_b_ceil1/result.json"
B_CEIL1_RESULT_SHA256_LF = "3c1e6d32a7a0aca60a482f0621d47d1bbecfe9706ae64b97250a691ea6aa0249"
B_CEIL1_EXACT_EXPECTED = 384 / 399                     # quantised ceil_1 of block B
RAW_STORE = (KA.PRIVATE_ROOT / "flyvis65_20260925T171656Z_74de0401a21f" / "raw_fits_real.json.gz")
RAW_STORE_SHA256 = "3c20e837d07ebba10db20963712bf87a8633c410e8a483ac4b10d65c737e6006"
STORE_KEY = "real||block||rule"

OUT = HERE / "symmetric_lambda_pair"
RESULT_MD, RESULT_JSON, STOP_JSON = "RESULT.md", "result.json", C.STOP_RECORD_NAME

STARTS = 10                                            # A's real run: --starts 10
LAMBDA_REGISTERED_A = 1.0                              # the lambda A's block-only fit chose
LAMBDA_FORCED_A = 100.0                                # Object 1
N_PRESENT_A, N_CELLS_A = 32, 64
N_PAIRS_A = N_PRESENT_A * (N_CELLS_A - N_PRESENT_A)    # 1024
CONTROL_CEILING = 1024 / 1024                          # stored: 1024 wins, 0 ties of 1024 pairs
CONTROL_TWICE = 2048
CUT = KA.GATE_CUT
AT_CUT_BAND = B1.AT_CUT_BAND
CONTROL_FAILED = "CONTROL_FAILED"
READING_CONTROL_FAILED = "READING_CONTROL_FAILED"
GATE_ULP_SPLIT = C.GATE_ULP_SPLIT
EXPECTED_B_LABEL = "G"                                 # section 3.2: frozen before the reading

BRANCH_A = "(a) rank limit of the class on block A"
BRANCH_B = "(b) A would fail at lambda = 100 as B did"
BRANCH_C = "(c) A survives the collapse"
BRANCH_D = "(d) DECODER SPLIT"
BRANCH_TEXT = {
    BRANCH_A: ("cert_A < 0.90: a rank limit of the class on block A, the first on a real bank; "
               "this outranks the lambda reading."),
    BRANCH_B: ("cert_A >= 0.90 and ceil_100_A < 0.90: A would fail at lambda = 100 as B did: the "
               "A/B pair differs by the lambda choice, not shown to differ by the block."),
    BRANCH_C: ("cert_A >= 0.90, ceil_100_A >= 0.90 and ceil_100_A_float >= 0.90: A survives the "
               "collapse; the population analogy is weaker than assumed."),
    BRANCH_D: ("ceil_100_A (quantised) and ceil_100_A_float fall on opposite sides of 0.90: the "
               "verdict is decided by the 5-bit decoder, not the fit; neither (b) nor (c)."),
}

side = B1.side
cert_ok_of = B1.cert_ok_of
at_cut = B1.at_cut
min_gap = B1.min_gap
decoder_direction = B1.decoder_direction


# ------------------------------------------------------------------------------------------
# Section 3.1: the reading tree of Object 1, on values (pure).

def tree(cert_ok, c100, c100f):
    """The branch name on three numbers, in the order (a), (d), (b)/(c)."""
    if not cert_ok:
        return BRANCH_A
    q, f = side(c100), side(c100f)
    if q != f:
        return BRANCH_D
    return BRANCH_C if q else BRANCH_B


def read_tree(cert, c100, c100f, uv_max=None):
    """Section 3.1 on the EXACT values (calibration section 6a); the TAU branch is computed beside
    it and flagged if it differs. The rider prints 'at the cut' for ceil_100_A in [0.88, 0.92], on
    a branch (b) or (c) only."""
    ok_exact = cert_ok_of(cert)
    ok_tau = cert["tau"] >= CUT
    branch = tree(ok_exact, c100["exact"], c100f["exact"])
    branch_tau = tree(ok_tau, c100["tau"], c100f["tau"])
    flags = []
    if C.split_at_cut(c100):
        flags.append(GATE_ULP_SPLIT)
    if C.split_at_cut(c100f):
        flags.append("CEIL_100_A_FLOAT_ULP_SPLIT")
    if ok_exact != ok_tau:
        flags.append("CERT_ULP_SPLIT")
    if not cert.get("counts_agree", True):
        flags.append("CERT_COUNTS_DISAGREE")
    if branch_tau != branch:
        flags.append("TAU_READING_DIFFERS")
    cut_band = at_cut(c100["exact"])
    qualified = branch in (BRANCH_B, BRANCH_C) and cut_band
    text = BRANCH_TEXT[branch]
    if branch == BRANCH_D:
        text += " Direction: " + decoder_direction(c100["exact"], c100f["exact"]) + "."
    if qualified:
        text += (f" AT THE CUT: ceil_100_A = {c100['exact']:.6f} lies in [{AT_CUT_BAND[0]}, "
                 f"{AT_CUT_BAND[1]}]; the reading is 'at the cut', not a side.")
    if GATE_ULP_SPLIT in flags:
        text += (" GATE_ULP_SPLIT: the exact and TAU readings of ceil_100_A lie on different "
                 "sides of 0.90; the branch follows the registered exact value.")
    return {"branch": branch, "branch_tau": branch_tau, "at_the_cut": cut_band,
            "qualified": qualified, "flags": flags, "text": text, "cert_ok": ok_exact,
            "ceil_100_A_side": side(c100["exact"]), "ceil_100_A_float_side": side(c100f["exact"]),
            "decoder_direction": decoder_direction(c100["exact"], c100f["exact"]),
            "uv_max_diagnostic": uv_max}


def control_verdict(auc):
    """Passes only if the exact ceiling equals the stored literal bit for bit AND the exact and
    TAU readings are equal (section 2). Returns (passed, reasons)."""
    reasons = []
    if auc.get("exact") is None or auc["exact"] != CONTROL_CEILING:
        reasons.append(f"exact ceiling {auc.get('exact')!r} != {CONTROL_CEILING!r}")
    if auc.get("exact") != auc.get("tau"):
        reasons.append(f"exact {auc.get('exact')!r} != TAU reading {auc.get('tau')!r}")
    return not reasons, reasons


# ------------------------------------------------------------------------------------------
# Section 3.2: Object 2, the reading. Pure functions on stored verdict objects.

def substituted_rows(rows, ceiling_block):
    """A deep copy of the stored rows with rule #2.1's ceiling_block replaced and nothing else."""
    out = copy.deepcopy(rows)
    out["rule"]["ceiling_block"] = ceiling_block
    return out


def bf_rows_ok(rows):
    """True iff p_P and leg_S_passes are stored for the primary and BF_1..BF_4: what the G
    condition 'every BF_r has p_P > 0.10' and read_label need."""
    return all(isinstance(rows.get(k, {}).get("p_P"), (int, float))
               and "leg_S_passes" in rows[k] for k in ("rule",) + KA.BF_KEYS)


def label_of(mod, summary, ceiling_block):
    """The block's own label function on its stored verdict objects with only ceiling_block
    substituted. mod is K (block B: read_label with S38's not-readable U) or KA (block A)."""
    real = summary["real"]
    rows = substituted_rows(real["rows"], ceiling_block)
    if mod is K:
        ev = K.read_label(rows, n_present=real["block_present"],
                          readable=real["smallest_passing_auc"] is not None)
    else:
        ev = KA.read_label(rows)
    syn = summary["synthetic"]
    text = mod.label_text(ev["label"], syn["limits"], syn["u_rule"], ev["U_reasons"], ceiling_block)
    return {"label": ev["label"], "text": text, "U_reasons": list(ev["U_reasons"]),
            "mechanism_description": ev["mechanism_description"],
            "reading_A_rule": ev["reading_A_rule"], "reading_B_BF1": ev["reading_B_BF1"],
            "ceiling_block_used": ceiling_block, "rows": rows}


def deciding_clause(lab):
    """Which clause of the section 4 row decides, in words, from the label call's own outputs."""
    rows = lab["rows"]
    pps = {KA.PRED_NAME[k]: rows[k]["p_P"] for k in ("rule",) + KA.BF_KEYS}
    lo = min(pps, key=pps.get)
    gate = f"rule #2.1's ceiling_block = {KA.fmt(lab['ceiling_block_used'])}"
    if lab["label"] == "G":
        return (f"G clause: not R and not W (rule #2.1 -> {lab['reading_A_rule']['letter']}, "
                f"BF_1 -> {lab['reading_B_BF1']['letter']}); every p_P > 0.10 (smallest: {lo} "
                f"{pps[lo]:.4f}); the gate is passed ({gate} >= {CUT:.2f}).")
    if lab["label"] == "U":
        return ("U clause: " + "; ".join(lab["U_reasons"]) + f". (The gate reads {gate}; every "
                f"p_P: {', '.join(f'{k} {x:.4f}' for k, x in pps.items())}.)")
    return f"{lab['label']} clause: R or W on both D1 candidates."


def reading_control(mod, summary):
    """Section 2, control 2 (no fit): with the STORED ceiling_block the label function must give
    the stored label letter and the stored label_text, and the p_P rows must be stored."""
    stored = summary["real"]["rows"]["rule"]["ceiling_block"]
    present = bf_rows_ok(summary["real"]["rows"])
    if not present:
        return False, {"stored_ceiling_block": stored, "p_P_rows_present": False}
    lab = label_of(mod, summary, stored)
    text_equal = lab["text"] == summary["real"]["label_text"]
    ok = lab["label"] == summary["real"]["label"] and text_equal
    return ok, {"stored_ceiling_block": stored, "label": lab["label"],
                "stored_label": summary["real"]["label"], "text_equal": text_equal,
                "p_P_rows_present": present}


def lambda_provenance(summary):
    """The selected lambda of every stored fit behind a verdict input: per predictor (knockout /
    full / block) and, for the leg-S shuffle fits, a count per lambda. Read from the stored object."""
    real = summary["real"]
    per = {k: {"ko": r["lambda_ko"], "full": r["lambda_full"], "block": r["lambda_block"]}
           for k, r in real["rows"].items()}
    shuf = {}
    for k in ("rule",) + KA.BF_KEYS:
        cnt = {}
        for row in real["per_shuffle"]:
            lam = row.get(f"lam_{k}")
            key = "none" if lam is None else f"{lam:g}"
            cnt[key] = cnt.get(key, 0) + 1
        shuf[k] = cnt
    return {"per_predictor_ko_full_block": per, "leg_S_shuffle_fits_selected_lambda": shuf}


def reading_object2(summary_b, summary_a, ceil_1_b, ceil_100_a):
    """Section 3.2: B's label with ceiling_block := ceil_1 and A's with ceiling_block :=
    ceil_100_A, each by the block's own label function; the pair table gives the gate clause and
    the label for both blocks at both lambdas (A at 1 and B at 100 are the stored values)."""
    lb = label_of(K, summary_b, ceil_1_b)
    la = label_of(KA, summary_a, ceil_100_a)
    b_reg = summary_b["real"]["rows"]["rule"]["ceiling_block"]
    a_reg = summary_a["real"]["rows"]["rule"]["ceiling_block"]

    def cell(block, lam, cb, label, text):
        return {"block": block, "lambda_block": lam, "ceiling_block": cb, "gate_passed": cb >= CUT,
                "label": label, "label_text": text}
    pair_table = [cell("A", 1, a_reg, summary_a["real"]["label"], summary_a["real"]["label_text"]),
                  cell("A", 100, ceil_100_a, la["label"], la["text"]),
                  cell("B", 1, ceil_1_b, lb["label"], lb["text"]),
                  cell("B", 100, b_reg, summary_b["real"]["label"],
                       summary_b["real"]["label_text"])]
    b_out = {k: x for k, x in lb.items() if k != "rows"}
    b_out.update(deciding_clause=deciding_clause(lb), expected_label=EXPECTED_B_LABEL,
                 as_expected=lb["label"] == EXPECTED_B_LABEL)
    a_out = {k: x for k, x in la.items() if k != "rows"}
    a_out.update(deciding_clause=deciding_clause(la))
    return {"B_at_lambda_1": b_out, "A_at_lambda_100": a_out, "pair_table": pair_table,
            "lambda_provenance_B": lambda_provenance(summary_b),
            "lambda_provenance_A": lambda_provenance(summary_a)}


# ------------------------------------------------------------------------------------------
# Seams: everything that touches the real block or a file goes through these (tests replace them).

@contextlib.contextmanager
def as_block_A():
    """Block A's geometry in K's module globals for one call (see the header)."""
    with C.swapped_globals(K.__dict__, MASKS=KA.MASKS, BLOCK_CELLS=KA.BLOCK_CELLS, BLOCK=KA.BLOCK,
                           N_BLOCK=KA.N_BLOCK, N_SOURCES=len(KA.SOURCES),
                           N_TARGETS=len(KA.TARGETS)):
        yield


def real_bank_A():
    return H.REAL


def real_block_y_A():
    bank = real_bank_A()
    return np.asarray(bank.exists[KA.BLOCK_CELLS[:, 0], KA.BLOCK_CELLS[:, 1]], bool)


def load_stored():
    with gzip.open(RAW_STORE, "rt", encoding="utf-8") as fh:
        return json.load(fh)[STORE_KEY]


def load_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def load_verdicts():
    """The stored verdict objects: (block B summary, block A summary, block_b_ceil1 result)."""
    return load_json(B_SUMMARY), load_json(A_SUMMARY), load_json(B_CEIL1_RESULT)


def git_state():
    """Section 7: (git rev-parse HEAD, git status --porcelain of the whole repository)."""
    return K.git("rev-parse", "HEAD"), K.git("status", "--porcelain")


HASHED_FILES = (*K.PINS, REGISTRATION, A_SCRIPT, C.B_SCRIPT, B1.CAL_SCRIPT, B1.REP_SCRIPT,
                B1_SCRIPT, C.SURVEY_PY, A_SUMMARY, B_SUMMARY, B_CEIL1_RESULT)


def input_hashes():
    """Section 2: every input hashed, printed first."""
    raw = hashlib.sha256(RAW_STORE.read_bytes()).hexdigest() if RAW_STORE.is_file() else None
    files = {f: K.sha256_lf(ROOT / f) for f in HASHED_FILES}
    return {"raw_store": str(RAW_STORE), "raw_store_sha256": raw,
            "raw_store_pinned": RAW_STORE_SHA256, "files_sha256_lf": files,
            "this_script_sha256_lf": K.sha256_lf(Path(__file__)),
            "registration_sha256_lf": files[REGISTRATION],
            "registration_pinned": REGISTRATION_SHA256_LF_PINNED}


def fit_at_A(lam):
    """Rule #2.1's block-only fit on the real block A, lambda forced (C.train_shortcut), decoded as
    the registered path decodes (P.decode) and as a float (C.float_p), with the diagnostic max
    |u.v| = max over the block cells of |U V^T| of the final fit. Returns lists."""
    K._w_init(STARTS, None, False)
    P = K._pred("rule")
    g = P.fit.__globals__
    with as_block_A():
        data, ex = C.train_shortcut(P, real_bank_A(), lam)
        cells = KA.BLOCK_CELLS
        p = np.asarray(P.decode(data, cells)["p_exist"], np.float64).tolist()
        p_float = C.float_p(g, ex).tolist()
        uv = np.asarray(ex["U"]) @ np.asarray(ex["V"]).T
        uv_max = float(np.max(np.abs(uv[cells[:, 0], cells[:, 1]])))
    return {"lambda": float(lam), "starts": STARTS, "p": p, "p_float": p_float, "uv_max": uv_max}


def cert_real_A(y):
    with as_block_A():
        return C.cert_search(y, C.CERT_BUDGET_REGISTERED)


# ------------------------------------------------------------------------------------------
# Refusals (before any fit and before any folder).

def dirty_refusal():
    head, porcelain = git_state()
    if porcelain.strip():
        return ("REFUSED: git status --porcelain is not empty; the run must be tied to a clean "
                f"commit (HEAD {head}).\n" + porcelain)
    return None


def pin_refusal():
    """The registration pin, the prediction commit and the tree; None if all hold."""
    now = K.sha256_lf(ROOT / REGISTRATION)
    if REGISTRATION_SHA256_LF_PINNED is None:
        return ("REFUSED: the registration is not pinned (REGISTRATION_SHA256_LF_PINNED is None); "
                "pin it in the script pin commit (section 7)")
    if now != REGISTRATION_SHA256_LF_PINNED:
        return (f"REFUSED: {REGISTRATION} has LF sha256 {now}, pinned "
                f"{REGISTRATION_SHA256_LF_PINNED}")
    pc = R.prediction_commit_refusal(PREDICTION_COMMIT_PINNED)
    if pc:
        return pc
    return dirty_refusal()


def out_refusal(out):
    out = Path(out)
    for name in (RESULT_MD, RESULT_JSON, STOP_JSON):
        if (out / name).exists():
            return f"REFUSED: {out / name} exists; the run never overwrites a result (section 7)"
    return None


def file_pin_checks():
    """The LF sha256 of every existing file this run reads; sys.exit on the first difference."""
    out = {}
    for key, path, pin in (("b_script", C.B_SCRIPT, C.B_SCRIPT_SHA256_LF),
                           ("a_script", A_SCRIPT, A_SCRIPT_SHA256_LF),
                           ("cal_script", B1.CAL_SCRIPT, B1.CAL_SCRIPT_SHA256_LF),
                           ("rep_script", B1.REP_SCRIPT, B1.REP_SCRIPT_SHA256_LF),
                           ("b1_script", B1_SCRIPT, B1_SCRIPT_SHA256_LF),
                           ("b_summary", B_SUMMARY, B_SUMMARY_SHA256_LF),
                           ("a_summary", A_SUMMARY, A_SUMMARY_SHA256_LF),
                           ("b_ceil1_result", B_CEIL1_RESULT, B_CEIL1_RESULT_SHA256_LF)):
        now = K.sha256_lf(ROOT / path)
        if now != pin:
            sys.exit(f"REFUSED: {path} has LF sha256 {now}, pinned {pin}")
        out[key + "_sha256_lf"] = now
    return out


def gate_checks():
    """Pins, block A and its mask, the AUC function, file hashes, the survey copy, the raw store,
    the stored control, and the two reading controls (no fit); sys.exit on any failure."""
    out = {"pins": K.check_pins(), "block_and_mask_A": KA.check_block_and_mask(),
           "auc_function": K.check_auc_function(), **file_pin_checks()}
    sv = C.check_survey_copy()
    if not sv["passed"]:
        sys.exit(f"REFUSED: the copied survey search does not match: {sv}")
    out["survey_copy"] = sv
    raw = hashlib.sha256(RAW_STORE.read_bytes()).hexdigest()
    if raw != RAW_STORE_SHA256:
        sys.exit(f"REFUSED: {RAW_STORE} has sha256 {raw}, pinned {RAW_STORE_SHA256}")
    out["raw_store_sha256"] = raw
    stored = load_stored()
    sc = C.auc_counts(stored["p"], stored["y"])
    if not (sc["exact"] == CONTROL_CEILING and sc["exact"] == sc["tau"]
            and sc["n_pairs"] == N_PAIRS_A and sc["twice"] == CONTROL_TWICE
            and int(sum(stored["y"])) == N_PRESENT_A and len(stored["y"]) == N_CELLS_A
            and float(stored["lam"]) == LAMBDA_REGISTERED_A):
        sys.exit(f"REFUSED: the stored block-only record of A does not give the registered "
                 f"control {CONTROL_CEILING!r} (lambda 1, 32/32): {sc}, lam {stored['lam']}")
    out["stored_control"] = {"exact": sc["exact"], "twice": sc["twice"], "n_pairs": sc["n_pairs"],
                             "lam": stored["lam"], "levels": sc["levels"]}
    sb, sa, res = load_verdicts()
    for name, mod, s in (("B", K, sb), ("A", KA, sa)):
        ok, detail = reading_control(mod, s)
        out[f"reading_control_{name}"] = {"passed": ok, **detail}
        if not ok:
            sys.exit(f"{READING_CONTROL_FAILED}: the label function of block {name} on its stored "
                     f"verdict objects does not give the stored label: {detail}")
    c1 = res["result"]["ceil_1"]
    if c1["exact"] != B_CEIL1_EXACT_EXPECTED or c1["exact"] != c1["tau"]:
        sys.exit(f"REFUSED: block_b_ceil1's ceil_1 is {c1['exact']!r}, expected "
                 f"{B_CEIL1_EXACT_EXPECTED!r} with exact == TAU")
    return out


# ------------------------------------------------------------------------------------------
# The run.

def v(x, d=6):
    return "n/a" if x is None else f"{x:.{d}f}"


def pair(o):
    return f"{v(o['exact'])} (tau {v(o['tau'])})"


def measure(y):
    """The whole measurement after the gate; returns (result dict, stop message or None)."""
    stored = load_stored()
    y = np.asarray(y, bool)
    ctl = fit_at_A(LAMBDA_REGISTERED_A)
    ca = C.auc_counts(ctl["p"], y)
    passed, reasons = control_verdict(ca)
    p_equal = [float(x) for x in ctl["p"]] == [float(x) for x in stored["p"]]
    if not p_equal:  # section 2 item 1: on A an AUC of 1.0 is weak alone; p equality is a stop
        passed = False
        reasons.append("the 64 p values are not bit-equal to the stored block record")
    control = {"lambda": LAMBDA_REGISTERED_A, "ceiling_block": ca, "expected": CONTROL_CEILING,
               "min_gap_p": min_gap(ctl["p"]), "p_bit_equal_to_store": p_equal,
               "stored_lambda": stored["lam"], "passed": passed, "reasons": reasons}
    K.log(f"CONTROL (A, lambda = 1): ceiling_block {ca['exact']!r} (tau {ca['tau']!r}); expected "
          f"{CONTROL_CEILING!r}; min gap between p levels {control['min_gap_p']}; p bit-equal to "
          f"the store: {p_equal}")
    if not passed:
        msg = f"{CONTROL_FAILED}: " + "; ".join(reasons)
        K.log(msg)
        return {"control": control}, msg
    K.log("CONTROL passed")
    cert = cert_real_A(y)
    K.log(f"cert_A: {cert['fraction']} = {v(cert['exact'])} (tau {v(cert['tau'])}); counts agree: "
          f"{cert['counts_agree']}; rerun spread {cert['rerun_spread']}")
    f100 = fit_at_A(LAMBDA_FORCED_A)
    c100, c100f = C.auc_counts(f100["p"], y), C.auc_counts(f100["p_float"], y)
    K.log(f"ceil_100_A (quantised) {pair(c100)}; ceil_100_A_float {pair(c100f)}; "
          f"max |u.v| (diagnostic) {f100['uv_max']!r}")
    reading = read_tree(cert, c100, c100f, f100["uv_max"])
    K.log(f"BRANCH: {reading['branch']}; flags: {', '.join(reading['flags']) or '-'}")
    K.log(reading["text"])
    sb, sa, res = load_verdicts()
    ceil_1_b = res["result"]["ceil_1"]["exact"]
    obj2 = reading_object2(sb, sa, ceil_1_b, c100["exact"])
    for k in ("B_at_lambda_1", "A_at_lambda_100"):
        K.log(f"OBJECT 2, {k}: {obj2[k]['text']}")
        K.log(f"  deciding clause: {obj2[k]['deciding_clause']}")
    K.log(f"B reading as expected ({EXPECTED_B_LABEL}): {obj2['B_at_lambda_1']['as_expected']}")
    res_out = {"control": control, "cert_A": {k: cert[k] for k in R.CERT_FIELDS},
               "ceil_100_A": c100, "ceil_100_A_float": c100f, "uv_max_diagnostic": f100["uv_max"],
               "reading": reading, "object2": obj2, "n_present": int(y.sum()),
               "n_pairs": c100["n_pairs"],
               "levels": {"ceil_100_A": c100["levels"], "ceil_100_A_float": c100f["levels"]},
               "ceil_1_B_used": ceil_1_b}
    return res_out, None


def porcelain_text(inputs):
    p = inputs["git_status_porcelain"]
    return "(empty)" if not p.strip() else p


def report_md(r, inputs):
    c, rd, o2 = r["cert_A"], r["reading"], r["object2"]
    L = ["# The symmetric pair: block A at lambda 100, block B's verdict at lambda 1 (post-data)",
         "", f"Registration: {REGISTRATION}, revision {REGISTRATION_REVISION}. Every AUC object is "
         "printed exact (tau).", "",
         f"git HEAD: {inputs['git_head']}. `git status --porcelain`: {porcelain_text(inputs)}.", "",
         "## Object 1: branch of section 3.1", "", f"**{rd['branch']}**", "", rd["text"], "",
         f"Flags: {', '.join(rd['flags']) or 'none'}. Branch under the TAU reading: "
         f"{rd['branch_tau']}.", "",
         "## Values", "", "| object | exact | tau | pairs | levels |", "|---|---|---|---|---|"]
    ctl = r["control"]["ceiling_block"]
    L.append(f"| control ceiling_block, A at lambda 1 | {v(ctl['exact'], 15)} | "
             f"{v(ctl['tau'], 15)} | {N_PAIRS_A} | |")
    L.append(f"| cert_A | {c['fraction']} = {v(c['exact'])} | {v(c['tau'])} | {c['n_pairs']} | |")
    for k in ("ceil_100_A", "ceil_100_A_float"):
        o = r[k]
        L.append(f"| {k} | {v(o['exact'])} | {v(o['tau'])} | {o['n_pairs']} | {o['levels']} |")
    L += ["", f"cert counts agree: {c['counts_agree']}; rerun spread {c['rerun_spread']}. max |u.v| "
          "of the lambda = 100 fit on the block cells (diagnostic, decides nothing): "
          f"{r['uv_max_diagnostic']!r}.", "",
          "## Control (section 2)", "",
          f"ceiling_block of A at lambda = 1 = {ctl['exact']!r}; expected {CONTROL_CEILING!r}; min "
          f"gap between adjacent p levels {r['control']['min_gap_p']}; p bit-equal to the store: "
          f"{r['control']['p_bit_equal_to_store']}.", "",
          "## Object 2: the reading (section 3.2), no fit", ""]
    for k, title in (("B_at_lambda_1", "Block B, block lambda at 1 (ceiling_block := ceil_1)"),
                     ("A_at_lambda_100",
                      "Block A, block lambda at 100 (ceiling_block := ceil_100_A)")):
        o = o2[k]
        L += [f"### {title}", "", f"Label: **{o['label']}**", "", o["text"], "",
              f"Deciding clause: {o['deciding_clause']}", ""]
        if k == "B_at_lambda_1":
            L += [f"Expected under the reading: {o['expected_label']}; as expected: "
                  f"{o['as_expected']}.", ""]
    L += ["### Pair table (the gate clause, both blocks, both lambdas)", "",
          "| block | block lambda | ceiling_block | gate >= 0.90 | label |", "|---|---|---|---|---|"]
    for t in o2["pair_table"]:
        L.append(f"| {t['block']} | {t['lambda_block']} | {v(t['ceiling_block'], 4)} | "
                 f"{t['gate_passed']} | {t['label']} |")
    L += ["", "### Lambda provenance of block B's stored verdict inputs", "",
          "Selected lambda per predictor (knockout / full / block):", ""]
    for k, d in o2["lambda_provenance_B"]["per_predictor_ko_full_block"].items():
        L.append(f"- {k}: {d['ko']} / {d['full']} / {d['block']}")
    L += ["", "Selected lambda of the 99 leg-S shuffle fits (count per lambda): "
          + json.dumps(o2["lambda_provenance_B"]["leg_S_shuffle_fits_selected_lambda"]), "",
          "## Inputs", "", f"- raw store sha256 {inputs['raw_store_sha256']}",
          f"- registration LF sha256 {inputs['registration_sha256_lf']}",
          f"- this script LF sha256 {inputs['this_script_sha256_lf']}",
          f"- git HEAD {inputs['git_head']}", ""]
    return "\n".join(L)


def write_outputs(out, result, inputs, msg=None):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    doc = {"registration": REGISTRATION, "revision": REGISTRATION_REVISION, "inputs": inputs,
           "git_head": inputs["git_head"], "git_status_porcelain": inputs["git_status_porcelain"],
           "result": result, "stop": msg, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    if msg:
        K.write_text_synced(out / STOP_JSON, K.dump_json(doc) + "\n")
        return
    K.write_text_synced(out / RESULT_JSON, K.dump_json(doc) + "\n")
    K.write_text_synced(out / RESULT_MD, report_md(result, inputs))


def parse(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="print the input hashes and the refusals; fit nothing, write nothing")
    ap.add_argument("--out", default=str(OUT), help="output folder (default: symmetric_lambda_pair/)")
    return ap.parse_args(argv)


def main(argv=None):
    a = parse(argv)
    K._LOG["buffer"].clear()
    K._LOG["output_errors"] = 0
    r = R.cwd_refusal()
    if r:
        sys.exit(r)
    refusal = pin_refusal()
    if a.dry_run:
        inputs = input_hashes()
        K.log("INPUTS " + json.dumps(inputs, indent=1))
        K.log("DRY RUN: nothing fitted, nothing written; a run now would be: "
              + (refusal.splitlines()[0] if refusal else "not refused"))
        return {"dry_run": True, "refusal": refusal, "inputs": inputs}
    if refusal:
        sys.exit(refusal)
    r = out_refusal(a.out)
    if r:
        sys.exit(r)
    inputs = input_hashes()
    inputs["git_head"], inputs["git_status_porcelain"] = git_state()
    K.log("INPUTS " + json.dumps(inputs, indent=1))
    gate = gate_checks()
    K.log("gate checks passed: pins, block A and mask, AUC function, file hashes, survey copy, "
          "raw store, stored control, the two reading controls")
    y = real_block_y_A()
    if not (int(y.sum()) == N_PRESENT_A and len(y) == N_CELLS_A):
        sys.exit(f"REFUSED: the real block A has {int(y.sum())} of {len(y)} present, registered "
                 f"{N_PRESENT_A} of {N_CELLS_A}")
    result, stop = measure(y)
    inputs["gate"] = gate
    write_outputs(a.out, result, inputs, stop)
    if stop:
        sys.exit(1)
    K.log("done")
    return result


if __name__ == "__main__":
    main()
