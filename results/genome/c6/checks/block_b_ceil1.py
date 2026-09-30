#!/usr/bin/env python3
"""Block B, real block: rule #2.1's block-only fit at a FIXED lambda = 1 (ceil_1) and cert.

Implements docs/plans/2026-09-30-block-b-ceil1-registration.md, revision 1 ("the registration";
section numbers below refer to it). Post-data: block B's verdict (U, failed fit, ceiling_block
0.7744 at lambda = 100) is known. This file is NEW and imports the calibration's script (C =
failed_fit_calibration.py) and the replication's refusals (R), as those import block B's script
(K). No fit, search, AUC or tie rule is re-implemented here; only the wiring to the REAL block and
the reading tree of section 3 are new. Nothing registered or hashed is edited.

Wiring (file:line at the commit that adds this file):
  bank      K.real_bank() = H.REAL (knockout_regrow_block_b.py:204), the bank block B's real arm fitted
            (K.build_bank("real", ...), :1159-1162); the mask is K.MASKS["block"] (:245).
  starts    K._w_init(10, None, False) (:1187-1191): H.STARTS = 10, rule #2.1 loaded from RULE_PATH,
            the real arm's --starts 10 (:3440, :3465-3475). No new seed is used by the fits.
  fits      C.train_shortcut (failed_fit_calibration.py:495-516) with lambda forced: [1] for ceil_1,
            [100] for the control, [1] with 100 starts for the diagnostic ceil_1_starts100.
            Its float twin: C.float_p (:451-456). This is the route of C.separator_fits (:541-562).
  cert      C.cert_search (:393-431) with C.CERT_BUDGET_REGISTERED and the calibration's cert seeds
            93300-93307 (a new pattern, so no new seed is needed).
  AUC       C.auc_counts (:209-225): exact and TAU readings, ulp_sensitive.

Run forms (always PYTHONUTF8=1; run from the repository root):
    PYTHONUTF8=1 tools/.venv/Scripts/python.exe results/genome/c6/checks/block_b_ceil1.py --dry-run
    PYTHONUTF8=1 tools/.venv/Scripts/python.exe results/genome/c6/checks/block_b_ceil1.py
The second form is the registered run. It refuses while REGISTRATION_SHA256_LF_PINNED (or
PREDICTION_COMMIT_PINNED) is None or differs, and it refuses if RESULT.md already exists. Order:
input hashes printed -> gate checks -> CONTROL (lambda = 100 must reproduce ceiling_block
0.7744360902255639 (= 309/399; 0.774436090225564 to 15 digits) bit for bit, exact == TAU) -> cert -> ceil_1 (quantised + float) -> the branch of
section 3, read mechanically -> outputs. If the control fails: CONTROL_FAILED, nothing else is
computed. Output text is ASCII; K reconfigures stdout to UTF-8 (S23).
"""
import sys

import argparse
import gzip
import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import failed_fit_calibration as C  # noqa: E402  (imports K, which sets UTF-8 streams)
import natural_fit_failure_replication as R  # noqa: E402  (cwd / prediction-commit refusals)

K = C.K
H = C.H
ROOT = C.ROOT

REGISTRATION = "docs/plans/2026-09-30-block-b-ceil1-registration.md"
REGISTRATION_REVISION = "1"
# Two-commit order (section 7): the registration commit is the prediction commit; the script pin
# commit follows it and sets both values below; then the run. None = the script refuses.
REGISTRATION_SHA256_LF_PINNED = "bea61287c426dd893deb1a331a8e24f4d525b22a2299b121b1f061d055ed2e5b"
PREDICTION_COMMIT_PINNED = "86238a66f985301765fd4f0f190f0c4975def312"
CAL_SCRIPT = R.CAL_SCRIPT
CAL_SCRIPT_SHA256_LF = R.CAL_SCRIPT_SHA256_LF
B_SCRIPT = C.B_SCRIPT
B_SCRIPT_SHA256_LF = C.B_SCRIPT_SHA256_LF
REP_SCRIPT = "results/genome/c6/checks/natural_fit_failure_replication.py"
REP_SCRIPT_SHA256_LF = "a802afa984c95345a5efd69fd8df2016df25edc1b90d6d76130549544f0f2fee"

# The pinned raw store of block B's real run (raw bytes; equals its line of SHA256SUMS.txt).
RAW_STORE = (K.PRIVATE_ROOT / "flyvis65_blockB_20260928T143258Z_7a10d88ec95e"
             / "raw_fits_real.json.gz")
RAW_STORE_SHA256 = "2461d921048b39479926878a9761aaf34bb4c5bedfc8a9e1c17882fd4ee398c6"
STORE_KEYS = {"rule": "real||block||rule", "N1": "real||block||N1",
              **{pk: f"real||block||{pk}" for pk in K.BF_KEYS}}

OUT = HERE / "block_b_ceil1"
RESULT_MD, RESULT_JSON, STOP_JSON = "RESULT.md", "result.json", C.STOP_RECORD_NAME

STARTS = 10
LAMBDA_REGISTERED = 100.0                              # the registered block-only choice on B
LAMBDA_FIXED = C.LAMBDA_CAP                            # 1.0
CONTROL_CEILING = 309 / 399                            # section 2: 0.7744360902255639 (15 digits: 0.774436090225564); 303 wins + 12 ties of 399
CONTROL_TWICE = 618                                    # 2 * 303 + 12
N_PAIRS = 399                                          # 19 present x 21 absent
CUT = K.GATE_CUT
CUT_FR = Fraction(9, 10)
AT_CUT_BAND = (0.88, 0.92)                             # section 3 rider
CONTROL_FAILED = "CONTROL_FAILED"
GATE_ULP_SPLIT = C.GATE_ULP_SPLIT

BRANCH_A = "(a) rank limit of the class on a real block"
BRANCH_B = "(b) label stands; FF-struct / FF-opt / FF-quant not separated"
BRANCH_C = "(c) FF-sel on the real block"
BRANCH_D = "(d) DECODER SPLIT"
BRANCH_TEXT = {
    BRANCH_A: ("cert < 0.90: a rank limit of the class on a real block, the first on a real "
               "bank; this outranks the lambda reading."),
    BRANCH_B: ("cert >= 0.90 and ceil_1 < 0.90: the label stands; the sub-kind FF-struct / "
               "FF-opt / FF-quant is not separated (calibration section 6)."),
    BRANCH_C: ("cert >= 0.90, ceil_1 >= 0.90 and ceil_1_float >= 0.90: FF-sel on the real "
               "block; the U is the lambda choice; the word 'cannot' in B's label is wider "
               "than the measurement."),
    BRANCH_D: ("ceil_1 (quantised) and ceil_1_float fall on opposite sides of 0.90: the verdict "
               "is decided by the 5-bit decoder, not the fit; neither (b) nor (c)."),
}


# ------------------------------------------------------------------------------------------
# Section 3: the reading tree, on values (pure; the tests drive it by hand).

def side(x):
    return C.ge(x)


def cert_ok_of(cert):
    """The exact Fraction against 9/10 (R.cert_ok's route), on the cert dict."""
    return Fraction(cert["fraction"]) >= CUT_FR


def tree(cert_ok, c1, c1f):
    """Section 3 on three numbers: the branch name, in the order (a), (d), (b)/(c). (d) is read
    before (b)/(c) because it is defined as neither of them (float >= 0.90 > quantised is (d), not
    (b))."""
    if not cert_ok:
        return BRANCH_A
    q, f = side(c1), side(c1f)
    if q != f:
        return BRANCH_D
    return BRANCH_C if q else BRANCH_B


def decoder_direction(c1, c1f):
    q, f = side(c1), side(c1f)
    if q == f:
        return None
    return ("float < 0.90 <= quantised" if q else "quantised < 0.90 <= float (FF-quant direction)")


def at_cut(c1):
    return c1 is not None and AT_CUT_BAND[0] <= c1 <= AT_CUT_BAND[1]


def read_tree(cert, c1, c1f, c1s100=None):
    """Section 3, mechanically. cert is the dict of C.cert_search (fraction, exact, tau);
    c1, c1f are C.auc_counts dicts of ceil_1 (quantised) and ceil_1_float. The branch is read on
    the EXACT values (the registered form, calibration section 6a); the TAU reading is computed
    beside it and, if it differs, the row is flagged GATE_ULP_SPLIT (ceil_1 and cert, section 6a)
    and the TAU branch is printed as a caveat. The rider prints 'at the cut' when ceil_1 is in
    [0.88, 0.92]."""
    ok_exact = cert_ok_of(cert)
    ok_tau = cert["tau"] >= CUT
    branch = tree(ok_exact, c1["exact"], c1f["exact"])
    branch_tau = tree(ok_tau, c1["tau"], c1f["tau"])
    flags = []
    if C.split_at_cut(c1):
        flags.append(GATE_ULP_SPLIT)
    if C.split_at_cut(c1f):
        flags.append("CEIL_1_FLOAT_ULP_SPLIT")
    if ok_exact != ok_tau:
        flags.append("CERT_ULP_SPLIT")
    if not cert.get("counts_agree", True):
        flags.append("CERT_COUNTS_DISAGREE")
    if branch_tau != branch:
        flags.append("TAU_READING_DIFFERS")
    cut_band = at_cut(c1["exact"])
    qualified = branch in (BRANCH_B, BRANCH_C) and cut_band
    text = BRANCH_TEXT[branch]
    if branch == BRANCH_D:
        text += " Direction: " + decoder_direction(c1["exact"], c1f["exact"]) + "."
    if qualified:
        text += (f" AT THE CUT: ceil_1 = {c1['exact']:.6f} lies in [{AT_CUT_BAND[0]}, "
                 f"{AT_CUT_BAND[1]}]; the reading is 'at the cut', not a side.")
    if GATE_ULP_SPLIT in flags:
        text += (" GATE_ULP_SPLIT: the exact and TAU readings of ceil_1 lie on different sides "
                 "of 0.90; the branch follows the registered exact value.")
    return {"branch": branch, "branch_tau": branch_tau, "at_the_cut": cut_band,
            "qualified": qualified, "flags": flags, "text": text,
            "cert_ok": ok_exact, "ceil_1_side": side(c1["exact"]),
            "ceil_1_float_side": side(c1f["exact"]), "decoder_direction":
            decoder_direction(c1["exact"], c1f["exact"]),
            "starts100_float": None if c1s100 is None else c1s100["exact"]}


# ------------------------------------------------------------------------------------------
# Section 2: the control (pure part).

def min_gap(p):
    u = np.unique(np.asarray(p, np.float64))
    return float(np.min(np.diff(u))) if len(u) > 1 else None


def control_verdict(auc):
    """The control passes only if the exact ceiling equals the literal bit for bit AND the exact
    and TAU readings are equal (section 2). Returns (passed, reasons)."""
    reasons = []
    if auc.get("exact") is None or auc["exact"] != CONTROL_CEILING:
        reasons.append(f"exact ceiling {auc.get('exact')!r} != {CONTROL_CEILING!r}")
    if auc.get("exact") != auc.get("tau"):
        reasons.append(f"exact {auc.get('exact')!r} != TAU reading {auc.get('tau')!r}")
    return not reasons, reasons


# ------------------------------------------------------------------------------------------
# Seams: everything that touches the real block goes through these (the tests replace them).

def real_block_y():
    bank = K.real_bank()
    return np.asarray(bank.exists[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]], bool)


def load_stored(key):
    with gzip.open(RAW_STORE, "rt", encoding="utf-8") as fh:
        return json.load(fh)[STORE_KEYS[key]]


def input_hashes():
    """Section 2: every input hashed, printed first."""
    raw = hashlib.sha256(RAW_STORE.read_bytes()).hexdigest() if RAW_STORE.is_file() else None
    files = {f: K.sha256_lf(ROOT / f) for f in (*K.PINS, REGISTRATION, B_SCRIPT, CAL_SCRIPT,
                                                REP_SCRIPT, C.SURVEY_PY)}
    return {"raw_store": str(RAW_STORE), "raw_store_sha256": raw,
            "raw_store_pinned": RAW_STORE_SHA256, "files_sha256_lf": files,
            "this_script_sha256_lf": K.sha256_lf(Path(__file__)),
            "registration_sha256_lf": files[REGISTRATION],
            "registration_pinned": REGISTRATION_SHA256_LF_PINNED}


def fit_at(lam, starts=None):
    """Rule #2.1's block-only fit on the real block, lambda forced (C.train_shortcut), decoded as
    the registered path decodes (P.decode) and as a float (C.float_p). Returns lists."""
    K._w_init(STARTS, None, False)
    P = K._pred("rule")
    g = P.fit.__globals__
    data, ex = C.train_shortcut(P, K.real_bank(), lam, starts=starts)
    return {"lambda": float(lam), "starts": STARTS if starts is None else starts,
            "p": np.asarray(P.decode(data, K.BLOCK_CELLS)["p_exist"], np.float64).tolist(),
            "p_float": C.float_p(g, ex).tolist()}


def cert_real(y):
    return C.cert_search(y, C.CERT_BUDGET_REGISTERED)


# ------------------------------------------------------------------------------------------
# Refusals (before any fit and before any folder).

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
    dirty = K.tree_state()
    if dirty:
        return ("REFUSED: uncommitted changes under results/genome/c6/ or docs/plans/; the run "
                "must be tied to a commit.\n" + dirty)
    return None


def out_refusal(out):
    out = Path(out)
    for name in (RESULT_MD, STOP_JSON):
        if (out / name).exists():
            return f"REFUSED: {out / name} exists; the run never overwrites a result (section 7)"
    return None


def gate_checks():
    """K.check_pins, K.check_block_and_mask, K.check_auc_function, the three script hashes, the
    survey copy and the raw store's pin; sys.exit on any failure."""
    out = {"pins": K.check_pins(), "block_and_mask": K.check_block_and_mask(),
           "auc_function": K.check_auc_function()}
    for key, path, pin in (("b_script", B_SCRIPT, B_SCRIPT_SHA256_LF),
                           ("cal_script", CAL_SCRIPT, CAL_SCRIPT_SHA256_LF),
                           ("rep_script", REP_SCRIPT, REP_SCRIPT_SHA256_LF)):
        now = K.sha256_lf(ROOT / path)
        if now != pin:
            sys.exit(f"REFUSED: {path} has LF sha256 {now}, pinned {pin}")
        out[key + "_sha256_lf"] = now
    sv = C.check_survey_copy()
    if not sv["passed"]:
        sys.exit(f"REFUSED: the copied survey search does not match: {sv}")
    out["survey_copy"] = sv
    raw = hashlib.sha256(RAW_STORE.read_bytes()).hexdigest()
    if raw != RAW_STORE_SHA256:
        sys.exit(f"REFUSED: {RAW_STORE} has sha256 {raw}, pinned {RAW_STORE_SHA256}")
    out["raw_store_sha256"] = raw
    return out


# ------------------------------------------------------------------------------------------
# The run.

def v(x, d=6):
    return "n/a" if x is None else f"{x:.{d}f}"


def pair(o):
    return f"{v(o['exact'])} (tau {v(o['tau'])})"


def measure(y):
    """The whole measurement after the gate; returns (result dict, stop message or None)."""
    stored = load_stored("rule")
    y = np.asarray(y, bool)
    ctl = fit_at(LAMBDA_REGISTERED)
    ca = C.auc_counts(ctl["p"], y)
    passed, reasons = control_verdict(ca)
    p_equal = [float(x) for x in ctl["p"]] == [float(x) for x in stored["p"]]
    control = {"lambda": LAMBDA_REGISTERED, "ceiling_block": ca, "expected": CONTROL_CEILING,
               "min_gap_p": min_gap(ctl["p"]), "p_bit_equal_to_store": p_equal,
               "stored_lambda": stored["lam"], "passed": passed, "reasons": reasons}
    K.log(f"CONTROL (lambda = 100): ceiling_block {ca['exact']!r} (tau {ca['tau']!r}); expected "
          f"{CONTROL_CEILING!r}; min gap between p levels {control['min_gap_p']}; p bit-equal to "
          f"the store: {p_equal}")
    if not passed:
        msg = f"{CONTROL_FAILED}: " + "; ".join(reasons)
        K.log(msg)
        return {"control": control}, msg
    K.log("CONTROL passed")
    cert = cert_real(y)
    K.log(f"cert: {cert['fraction']} = {v(cert['exact'])} (tau {v(cert['tau'])}); counts agree: "
          f"{cert['counts_agree']}; rerun spread {cert['rerun_spread']}")
    f1 = fit_at(LAMBDA_FIXED)
    c1, c1f = C.auc_counts(f1["p"], y), C.auc_counts(f1["p_float"], y)
    K.log(f"ceil_1 (quantised) {pair(c1)}; ceil_1_float {pair(c1f)}")
    f100 = fit_at(LAMBDA_FIXED, starts=C.STARTS_100)
    c100 = C.auc_counts(f100["p_float"], y)
    c100q = C.auc_counts(f100["p"], y)
    K.log(f"ceil_1_starts100 (diagnostic, decides nothing) float {pair(c100)}; quantised "
          f"{pair(c100q)}")
    reading = read_tree(cert, c1, c1f, c100)
    K.log(f"BRANCH: {reading['branch']}; flags: {', '.join(reading['flags']) or '-'}")
    K.log(reading["text"])
    res = {"control": control, "cert": {k: cert[k] for k in R.CERT_FIELDS}, "ceil_1": c1,
           "ceil_1_float": c1f, "ceil_1_starts100_float": c100,
           "ceil_1_starts100_quantised": c100q, "reading": reading,
           "n_present": int(y.sum()), "n_pairs": c1["n_pairs"],
           "levels": {"ceil_1": c1["levels"], "ceil_1_float": c1f["levels"]},
           "registered_lambda_choice": LAMBDA_REGISTERED}
    return res, None


def report_md(r, inputs):
    c = r["cert"]
    rd = r["reading"]
    L = ["# Block B, real block: ceil_1 and cert (post-data)", "",
         f"Registration: {REGISTRATION}, revision {REGISTRATION_REVISION}. Every AUC object is "
         "printed exact (tau).", "",
         "## Branch (section 3)", "", f"**{rd['branch']}**", "", rd["text"], "",
         f"Flags: {', '.join(rd['flags']) or 'none'}. Branch under the TAU reading: "
         f"{rd['branch_tau']}.", "",
         "## Values", "", "| object | exact | tau | pairs | levels |", "|---|---|---|---|---|"]
    L.append(f"| control ceiling_block (lambda 100) | {v(r['control']['ceiling_block']['exact'], 15)}"
             f" | {v(r['control']['ceiling_block']['tau'], 15)} | {N_PAIRS} | |")
    L.append(f"| cert | {c['fraction']} = {v(c['exact'])} | {v(c['tau'])} | {c['n_pairs']} | |")
    for k in ("ceil_1", "ceil_1_float", "ceil_1_starts100_float", "ceil_1_starts100_quantised"):
        o = r[k]
        L.append(f"| {k} | {v(o['exact'])} | {v(o['tau'])} | {o['n_pairs']} | {o['levels']} |")
    L += ["", f"cert counts agree: {c['counts_agree']}; rerun spread {c['rerun_spread']}; "
          "ceil_1_starts100 is a diagnostic and decides nothing.", "",
          "## Control (section 2)", "",
          f"ceiling_block at lambda = 100 = {r['control']['ceiling_block']['exact']!r}; expected "
          f"{CONTROL_CEILING!r}; min gap between adjacent p levels "
          f"{r['control']['min_gap_p']}; p bit-equal to the store: "
          f"{r['control']['p_bit_equal_to_store']}.", "",
          "## Inputs", "", f"- raw store sha256 {inputs['raw_store_sha256']}",
          f"- registration LF sha256 {inputs['registration_sha256_lf']}",
          f"- this script LF sha256 {inputs['this_script_sha256_lf']}", ""]
    return "\n".join(L)


def write_outputs(out, result, inputs, msg=None):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    doc = {"registration": REGISTRATION, "revision": REGISTRATION_REVISION, "inputs": inputs,
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
    ap.add_argument("--out", default=str(OUT), help="output folder (default: block_b_ceil1/)")
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
    K.log("INPUTS " + json.dumps(inputs, indent=1))
    gate = gate_checks()
    K.log("gate checks passed: pins, block and mask, AUC function, script hashes, survey copy, "
          "raw store")
    y = real_block_y()
    if not (int(y.sum()) == 19 and len(y) == K.N_BLOCK):
        sys.exit(f"REFUSED: the real block has {int(y.sum())} of {len(y)} present, registered 19 "
                 "of 40")
    result, stop = measure(y)
    inputs["gate"] = gate
    write_outputs(a.out, result, inputs, stop)
    if stop:
        sys.exit(1)
    K.log("done")
    return result


if __name__ == "__main__":
    main()
