"""Read-only: permuted board j = 89 (seed 93289) of the failed-fit calibration's registered run.

Asked for by Ark and Zcode (Q-A2 of the natural fit-failure replication registration, rev 1.1),
before the prediction commit. It fits nothing and writes nothing: it opens the run's stored raw
fits (raw_fits.json.gz), its cert_members.json and permuted_reference.csv, read-only, and prints
the separator values stored for board j = 89, with every AUC recomputed from the stored p and y
twice: an exact count (win d > 0, tie d == 0, as K.auc and failed_fit_calibration.auc_counts) and
the _tau count (|d| <= TAU is a tie). The counts are also taken with fractions.Fraction.

Key naming (results/genome/c6/checks/failed_fit_calibration.py):
- plan_perm_ref(j): tasks (f"perm:{j}", "sep", "rule") and (f"perm:{j}", "block", pk) for the BF
  keys; write_raw joins the key tuple with "||" (knockout_regrow_block_b.py write_raw).
- read_perm_board(j): ceiling_block = auc(sep.reg_p), ceil_1 = auc(sep.ceil1_p), ceil_1_float =
  auc(sep.ceil1_float_p), ceil_lambda_c_float = auc(sep.reg_float_p); read_world adds
  ceil_1_starts100 = auc(sep.ceil1_s100_float_p) (the FLOAT value the separator reads, A-5) and
  ceil_1_starts100_quantised = auc(sep.ceil1_s100_p).
- cert: cert_members.json keyed by sha256(y as bool bytes)[:16] (write_outputs).

Run from anywhere with PYTHONUTF8=1: python j89_read.py
"""
import gzip
import hashlib
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

J = 89
SEED = 93200 + J
DATA = Path(r"C:\Users\mikha\Documents\dpc-research\connectome-seed-data\knockout_regrow"
            r"\failed_fit_calibration_20260929T094748Z_255a03d")
REPO = Path(__file__).resolve().parents[3]
TAU = 1e-9  # harness.py:66, asserted below
CUT = 0.90
BF_KEYS = ("BF:1", "BF:2", "BF:3", "BF:4")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def counts(p, y):
    p, y = np.asarray(p, np.float64), np.asarray(y, bool)
    pos, neg = p[y], p[~y]
    n = len(pos) * len(neg)
    d = pos[:, None] - neg[None, :]
    wins, ties = int((d > 0).sum()), int((d == 0).sum())
    wins_t, ties_t = int((d > TAU).sum()), int((np.abs(d) <= TAU).sum())
    # the same exact count with Fraction on the stored floats
    fw = ft = 0
    for a in pos:
        for b in neg:
            dd = Fraction(float(a)) - Fraction(float(b))
            fw += dd > 0
            ft += dd == 0
    assert (fw, ft) == (wins, ties), ((fw, ft), (wins, ties))
    exact = Fraction(2 * wins + ties, 2 * n)
    tau = Fraction(2 * wins_t + ties_t, 2 * n)
    return {"exact": exact, "tau": tau, "wins": wins, "ties": ties, "wins_tau": wins_t,
            "ties_tau": ties_t, "n": n, "levels": int(len(np.unique(p)))}


def line(name, c):
    flag = "  ULP_SENSITIVE" if c["exact"] != c["tau"] else ""
    side = ">= 0.90" if c["exact"] >= Fraction(9, 10) else "<  0.90"
    return (f"  {name:<30} exact {float(c['exact']):.6f} ({c['exact']})  tau {float(c['tau']):.6f}"
            f"  wins {c['wins']} ties {c['ties']} / {c['n']}  levels {c['levels']}  {side}{flag}")


def main():
    sys.stdout.reconfigure(newline="\n")  # LF output when redirected on Windows
    harness = (REPO / "results/genome/c6/harness.py").read_text(encoding="utf-8")
    assert re.search(r"^TAU = 1e-9$", harness, re.M), "harness.py TAU changed"

    raw = DATA / "raw_fits.json.gz"
    sums = (DATA / "SHA256SUMS.txt").read_text(encoding="utf-8")
    h = sha256(raw)
    print(f"raw_fits.json.gz sha256 {h}; listed in the run's SHA256SUMS.txt: {h in sums}")
    with gzip.open(raw, "rt", encoding="utf-8") as fh:
        F = json.load(fh)
    key = f"perm:{J}"
    sp = F[f"{key}||sep||rule"]
    y = np.asarray(sp["y"], bool)
    print(f"board j = {J}, seed {SEED}, key {key}: present {int(y.sum())} of {len(y)}")
    print(f"  rule #2.1 separator record: grid {sp['grid']}, lambda_c {sp['lambda_c']}")

    rows = [("ceiling_block (reg_p)", "reg_p"), ("ceil_lambda_c_float", "reg_float_p"),
            ("ceil_1 (quantised)", "ceil1_p"), ("ceil_1_float", "ceil1_float_p"),
            ("ceil_1_starts100 (float)", "ceil1_s100_float_p"),
            ("ceil_1_starts100_quantised", "ceil1_s100_p")]
    got = {}
    for name, fld in rows:
        got[fld] = counts(sp[fld], y)
        print(line(name, got[fld]))

    print("  BF block fits (K._fit_one, block mask, nested lambda):")
    for pk in BF_KEYS:
        r = F[f"{key}||block||{pk}"]
        assert np.array_equal(np.asarray(r["y"], bool), y)
        print(line(f"{pk} ceiling_block, lambda {r['lam']}", counts(r["p"], y)))
    print("  (BF ceil_1 at lambda = 1 was not fitted for permuted boards: plan_perm_ref)")

    certs = json.loads((DATA / "cert_members.json").read_text(encoding="utf-8"))
    ck = hashlib.sha256(y.tobytes()).hexdigest()[:16]
    c = certs[ck]
    assert c["y"] == y.astype(int).tolist()
    m = {k: np.asarray(v, np.float64) for k, v in c["member"].items()}
    score = (m["a"][:, None] + m["b"][None, :] + m["u"][:, None] * m["v"][None, :]).ravel()
    cc = counts(score, y)
    print(f"  cert (cert_members.json key {ck}): stored exact {c['exact']} ({c['fraction']}), "
          f"tau {c['tau']}, rerun spread {c['rerun_spread']}, counts_agree {c['counts_agree']}")
    print(line("cert recounted from member", cc))

    # the printed CSV row, for comparison
    with open(DATA / "permuted_reference.csv", encoding="utf-8") as fh:
        hdr, *body = [ln.rstrip("\n").split(",") for ln in fh]
    row = dict(zip(hdr, next(b for b in body if b[0] == str(J))))
    print(f"  permuted_reference.csv row: ceiling_block {row['ceiling_block']}, ceil_1 "
          f"{row['ceil_1']}, ceil_1_float {row['ceil_1_float']}, ceil_lambda_c_float "
          f"{row['ceil_lambda_c_float']}, cert {row['cert']}")
    for fld, col in (("reg_p", "ceiling_block"), ("ceil1_p", "ceil_1"),
                     ("ceil1_float_p", "ceil_1_float"), ("reg_float_p", "ceil_lambda_c_float")):
        assert f"{float(got[fld]['exact']):.6f}" == row[col], (fld, col)
    print("  the recomputed values equal the CSV row on its four separator columns")

    # CAL section 6 table (separator_reading), on the exact values
    ge = lambda x: x >= Fraction(9, 10)
    cb, c1, c1f = got["reg_p"]["exact"], got["ceil1_p"]["exact"], got["ceil1_float_p"]["exact"]
    clcf, c1s = got["reg_float_p"]["exact"], got["ceil1_s100_float_p"]["exact"]
    if ge(cb):
        rd = "gate passed"
    elif not ge(cc["exact"]):
        rd = "not separated: rank limit or fit (no witness either way)"
    elif ge(c1):
        rd = "fit failure, FF-sel" + ("; and FF-quant at lambda_c" if ge(clcf) else "")
    elif ge(c1f):
        rd = "fit failure, FF-quant (at lambda = 1)"
    elif ge(c1s):
        rd = "fit failure, FF-struct or FF-opt, not separated; ceil_1_starts100 >= 0.90 names FF-opt"
    else:
        rd = "fit failure, FF-struct or FF-opt, not separated"
    print(f"CAL section 6 row for j = {J}: {rd}")


if __name__ == "__main__":
    main()
