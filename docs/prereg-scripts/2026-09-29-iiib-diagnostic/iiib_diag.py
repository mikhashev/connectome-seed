"""(iii-b) diagnostic on ALREADY-RECORDED fits (post-data; read-only; no fit is run).

Object: option (iii-b) of docs/plans/2026-09-29-failed-fit-branch-calibration-registration.md
section 13: "AUC of the fitted u_s v_t term alone, or the full score's AUC minus its additive
part's". Zcode (DPC Research chat, 2026-09-29): "the AUC of the u.v term on N1's residual".

The stored records hold p (sigmoid of the block logit) and y only; U, V, W are not stored.
What p allows, read-only (the checks below verify each premise on every board):
  * rule #2.1's float logit at lambda: z = O + u_s v_t + W[G(s),G(t)], with O = N1's fixed
    offset c + a_s + b_t (fit.py fit_uvw; harness _n1_logit_grid; float_p in
    failed_fit_calibration.py). On block B (5 sources L1-L5 x 8 targets) every source has the
    same group, so W is a column effect w_g(t) (registration section 3).
  * N1's p (record "block||N1") is sigmoid(O) on the same view, so
    logit(p_float) - logit(p_N1) = u_s v_t + w_g(t) exactly (checked: after centring each column
    over the 5 sources this residual is rank 1 to ~1e-15 on every board with an N1 record).
  * The double-centred block logit (row and column means removed over the 5 x 8 grid) equals
    (u_s - mean u)(v_t - mean v): every additive term (c, a, b, W's column effect, and the
    quantised a, b, c) drops out.

Readings computed (names used in the output and CSV):
  R0  AUC of u_s v_t alone, in the fitter's own gauge. NOT COMPUTABLE: needs U, V (not stored);
      from p only u v + w_g(t) is identified, and u -> u + k shifts k v_t into the column effect.
  R1a full AUC minus the AUC of the additive part taken as N1's offset O (W not counted as
      additive). Float fit: exact for the float score. Quantised fit: approximate, because the
      quantised model's additive part is quantised a, b and a refitted c, not O.
      Needs a block||N1 record: fresh boards and calibration worlds only (not the permuted 99).
  R1b full AUC minus the AUC of the additive projection of the full logit (row + column means),
      i.e. the additive part taken as everything additive including W's column effect.
  R2  AUC of logit(p_float) - logit(p_N1) = u_s v_t + w_g(t): Zcode's "u.v on N1's residual".
      Float fits only (the quantised residual carries the quantisation error of a, b, c).
      Needs a block||N1 record.
  R3  AUC of the double-centred logit = AUC of (u_s - mean u)(v_t - mean v): the u.v term with
      its additive gauge removed; invariant to all additive terms. Float and quantised.

Every AUC is given exact and under TAU = 1e-9 (harness.py:66), counted over the 20 x 20 pairs.
For R1a/R2/R3/R1b the TAU is applied to the object's own scale (logit units for R2, R3 and the
additive projection; p for the full scores and N1, as registered).

Usage: PYTHONUTF8=1 python iiib_diag.py > iiib_diag_out.txt   (writes iiib_diag_boards.csv)
"""
import csv
import gzip
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

DATA = Path(r"C:\Users\mikha\Documents\dpc-research\connectome-seed-data\knockout_regrow")
REP = DATA / "natural_fit_failure_replication_20260929T143137Z_a9f1c82"
CAL = DATA / "failed_fit_calibration_20260929T094748Z_255a03d"
SHA = {REP / "raw_fits.json.gz": "ca7bf71c10965f65fa74cd0285002f1db9a50af6c06a95d8961acd34be8621f0",
       REP / "boards.csv": "38f9c4fdd0bbff6c4dd360630ff1e8e762990d1fff5f7e9901e144931609c201",
       CAL / "raw_fits.json.gz": "3b053b705eb7dddc7b98e92685585f18906a7bd1a115bab9a3af247f213afd04",
       CAL / "permuted_reference.csv": "b88a7c3326ac8ad78d912064983b6dfd012c2cbae4e0f3876c717cc64e1c68e2",
       CAL / "worlds.csv": "60dd12359a9f3ecc3c9e925c16eae6e6994e39e4d4745d5d7b18b8ca7a5d7be2"}
HERE = Path(__file__).resolve().parent
TAU = 1e-9
CUT = 0.90
NS, NT = 5, 8                     # block B: SOURCES x TARGETS, row-major (B script lines 212-228)
DECODER_SPLIT = ["fresh:145", "fresh:161", "fresh:266"]


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def auc(score, y):
    s, y = np.asarray(score, np.float64), np.asarray(y, bool)
    d = s[y][:, None] - s[~y][None, :]
    n = d.size
    w, t = int((d > 0).sum()), int((d == 0).sum())
    wt, tt = int((d > TAU).sum()), int((np.abs(d) <= TAU).sum())
    return {"exact": (w + 0.5 * t) / n, "tau": (wt + 0.5 * tt) / n,
            "twice": 2 * w + t, "twice_tau": 2 * wt + tt, "n": n}


def logit(p):
    p = np.asarray(p, np.float64)
    return np.log(p) - np.log1p(-p)


def dcentre(z):
    g = np.asarray(z, np.float64).reshape(NS, NT)
    return (g - g.mean(0, keepdims=True) - g.mean(1, keepdims=True) + g.mean()).ravel()


def addproj(z):
    return np.asarray(z, np.float64) - dcentre(z)


def objects(p_float, p_quant, y, p_n1, tag, checks):
    """All readings for one fit pair (float, quantised) at one lambda."""
    o = {}
    zf, zq = logit(p_float), logit(p_quant)
    full_f, full_q = auc(p_float, y), auc(p_quant, y)
    o[f"full_float_{tag}"], o[f"full_quant_{tag}"] = full_f, full_q
    o[f"R3_float_{tag}"] = auc(dcentre(zf), y)
    o[f"R3_quant_{tag}"] = auc(dcentre(zq), y)
    o[f"R1b_float_{tag}"] = diff(full_f, auc(addproj(zf), y))
    o[f"R1b_quant_{tag}"] = diff(full_q, auc(addproj(zq), y))
    o[f"R3_float_{tag}_sv2"] = float(np.linalg.svd(dcentre(zf).reshape(NS, NT),
                                                   compute_uv=False)[1])
    o[f"R3_float_{tag}_maxabs"] = float(np.abs(dcentre(zf)).max())
    if p_n1 is not None:
        n1 = auc(p_n1, y)
        r = zf - logit(p_n1)
        rc = r.reshape(NS, NT) - r.reshape(NS, NT).mean(0, keepdims=True)
        sv = np.linalg.svd(rc, compute_uv=False)
        checks.append(float(sv[1]))          # premise: column-centred residual is rank 1
        o[f"R2_float_{tag}"] = auc(r, y)
        o[f"R1a_float_{tag}"] = diff(full_f, n1)
        o[f"R1a_quant_{tag}"] = diff(full_q, n1)
    return o


def diff(a, b):
    return {"exact": a["exact"] - b["exact"], "tau": a["tau"] - b["tau"]}


def load():
    for p, h in SHA.items():
        got = sha256(p)
        assert got == h, (str(p), got)
    rep = json.load(gzip.open(REP / "raw_fits.json.gz"))
    cal = json.load(gzip.open(CAL / "raw_fits.json.gz"))
    bcsv = {r["key"]: r for r in csv.DictReader(open(REP / "boards.csv", encoding="utf-8"))}
    pcsv = {f"perm:{r['j']}": r for r in
            csv.DictReader(open(CAL / "permuted_reference.csv", encoding="utf-8"))}
    wcsv = {f"cal:{r['family']}:{r['j']}": r for r in
            csv.DictReader(open(CAL / "worlds.csv", encoding="utf-8"))}
    return rep, cal, bcsv, pcsv, wcsv


def board_rows(rep, cal, bcsv, pcsv, wcsv):
    rows, checks, regchk = [], [], []
    sources = [("fresh", rep, k) for k in bcsv] + [("seen", cal, k) for k in pcsv] + \
              [("world", cal, k) for k in wcsv]
    for group, raw, key in sources:
        sep = raw[f"{key}||sep||rule"]
        y = np.asarray(sep["y"], bool)
        n1rec = raw.get(f"{key}||block||N1")
        p_n1 = None
        if n1rec is not None:
            assert n1rec["y"] == sep["y"], key
            p_n1 = np.asarray(n1rec["p"], np.float64)
        row = {"key": key, "group": group, "lambda_c": float(sep["lambda_c"]),
               "grid": "/".join(str(g) for g in sep["grid"])}
        row.update(objects(sep["ceil1_float_p"], sep["ceil1_p"], y, p_n1, "l1", checks))
        row.update(objects(sep["reg_float_p"], sep["reg_p"], y, p_n1, "lc", checks))
        row["n1"] = auc(p_n1, y) if p_n1 is not None else None
        # self-check: the recomputed AUCs equal the registered carriers' values
        ref = bcsv.get(key) or pcsv.get(key) or wcsv.get(key)
        for mine, col in (("full_quant_l1", "ceil_1"), ("full_float_l1", "ceil_1_float"),
                          ("full_float_lc", "ceil_lambda_c_float")):
            regchk.append(abs(row[mine]["exact"] - float(ref[col])) < 5e-7)
        if group == "fresh":
            regchk.append(abs(row["n1"]["exact"] - float(ref["n1_block"])) < 5e-7)
            regchk.append(abs(row["full_quant_lc"]["exact"] - float(ref["ceiling_block"])) < 5e-7)
            row["flags"] = ref["flags"]
        else:
            row["flags"] = ref.get("flags", "")
        rows.append(row)
    return rows, checks, regchk


# ------------------------------------------------------------------------------------------
# Printing.

def q(vals):
    v = np.sort(np.asarray(vals, float))
    pct = [0, 5, 25, 50, 75, 95, 100]
    return " ".join(f"{np.percentile(v, x):7.4f}" for x in pct)


def gaps(vals, top=3):
    v = np.unique(np.round(np.asarray(vals, float), 12))
    if len(v) < 2:
        return "one value"
    d = np.diff(v)
    idx = np.argsort(d)[::-1][:top]
    arr = np.round(np.asarray(vals, float), 12)
    return "; ".join(f"{d[i]:.4f} between {v[i]:.4f} and {v[i + 1]:.4f} "
                     f"({int((arr <= v[i]).sum())} boards at or below, "
                     f"{int((arr >= v[i + 1]).sum())} at or above)" for i in sorted(idx))


def mw(a, b):
    """Share of (a, b) pairs with a > b (ties half): how far the object orders class a above b."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = a[:, None] - b[None, :]
    return ((d > 0).sum() + 0.5 * (d == 0).sum()) / d.size


def hist(vals, lo, hi, step):
    edges = np.round(lo + step * np.arange(int(round((hi - lo) / step)) + 1), 10)
    v = np.asarray(vals, float)
    out = []
    for i in range(len(edges) - 1):
        a, b = edges[i], edges[i + 1]
        n = int(((v >= a) & ((v < b) if i < len(edges) - 2 else (v <= b))).sum())
        out.append(f"    [{a:6.3f},{b:6.3f}{')' if i < len(edges) - 2 else ']'} {n:4d} {'#' * n}")
    below, above = int((v < lo).sum()), int((v > hi).sum())
    if below:
        out.insert(0, f"    below {lo:.3f}: {below}")
    if above:
        out.append(f"    above {hi:.3f}: {above}")
    return "\n".join(out)


def val(row, name, which):
    x = row.get(name)
    return None if x is None else x[which]


def main():
    rep, cal, bcsv, pcsv, wcsv = load()
    rows, checks, regchk = board_rows(rep, cal, bcsv, pcsv, wcsv)
    P = print
    P("(iii-b) DIAGNOSTIC ON ALREADY-RECORDED FITS -- POST-DATA, READ-ONLY, NO FIT RUN")
    P("Any future (iii-b) registration is NOT blind to these numbers.")
    P("")
    P("Inputs (sha256 verified):")
    for p, h in SHA.items():
        P(f"  {h}  {p.parent.name}/{p.name}")
    P("")
    P("Premise checks:")
    P(f"  recomputed AUCs equal the carriers' ceil_1, ceil_1_float, ceil_lambda_c_float, "
      f"n1_block, ceiling_block: {sum(regchk)} of {len(regchk)}")
    P(f"  column-centred (logit p_float - logit p_N1) rank 1: max 2nd singular value over "
      f"{len(checks)} fits = {max(checks):.2e}")
    P("")

    fresh = [r for r in rows if r["group"] == "fresh"]
    seen = [r for r in rows if r["group"] == "seen"]
    worlds = [r for r in rows if r["group"] == "world"]
    f_pass = [r for r in fresh if r["full_quant_l1"]["exact"] >= CUT]
    s_pass = [r for r in seen if r["full_quant_l1"]["exact"] >= CUT]
    f_hi = [r for r in f_pass if r["n1"]["exact"] >= CUT]
    f_lo = [r for r in f_pass if r["n1"]["exact"] < CUT]
    lam100 = [r for r in fresh if r["lambda_c"] == 100.0 and r["full_quant_lc"]["exact"] >= CUT]
    P(f"Sets: fresh {len(fresh)}; fresh passing ceil_1 >= 0.90 (lambda = 1, quantised): "
      f"{len(f_pass)}; of these N1 >= 0.90: {len(f_hi)}, N1 < 0.90: {len(f_lo)}. "
      f"Seen (permuted) {len(seen)}; passing ceil_1: {len(s_pass)} "
      f"(no N1 record: R1a, R2 not available). Worlds {len(worlds)}. "
      f"Fresh passes at lambda_c = 100: {len(lam100)}.")
    P("")

    objs = [("R3_float_l1", "R3: AUC of double-centred logit, float fit, lambda = 1"),
            ("R3_quant_l1", "R3: same, quantised fit (the registered decode), lambda = 1"),
            ("R2_float_l1", "R2: AUC of logit(p_float) - logit(p_N1) = u.v + w_g(t), lambda = 1"),
            ("R1a_float_l1", "R1a: ceil_1_float - n1_block (additive part = N1 offset)"),
            ("R1a_quant_l1", "R1a: ceil_1 - n1_block (quantised; approximate)"),
            ("R1b_float_l1", "R1b: ceil_1_float - AUC(additive projection of float logit)"),
            ("R1b_quant_l1", "R1b: ceil_1 - AUC(additive projection of quantised logit)")]
    P("=" * 100)
    P("1. DISTRIBUTIONS AT lambda = 1 (percentiles 0 5 25 50 75 95 100)")
    P("=" * 100)
    for name, desc in objs:
        P(f"\n{desc}   [{name}]")
        for lab, S in (("fresh pass 294", f_pass), ("  N1>=0.90 (21)", f_hi),
                       ("  N1< 0.90 (273)", f_lo), ("seen pass 98", s_pass)):
            for which in ("exact", "tau"):
                v = [val(r, name, which) for r in S]
                if any(x is None for x in v):
                    P(f"  {lab:16s} {which:5s}  not available (no N1 record)")
                    continue
                P(f"  {lab:16s} {which:5s}  {q(v)}")
        v_hi = [val(r, name, "tau") for r in f_hi]
        v_lo = [val(r, name, "tau") for r in f_lo]
        P(f"  N1>=0.90 vs N1<0.90 (tau): range hi [{min(v_hi):.4f}, {max(v_hi):.4f}], "
          f"range lo [{min(v_lo):.4f}, {max(v_lo):.4f}]; P(hi > lo) = {mw(v_hi, v_lo):.4f}; "
          f"lo boards inside hi's range: {sum(min(v_hi) <= x <= max(v_hi) for x in v_lo)} of "
          f"{len(v_lo)}")
        P(f"  three largest gaps between adjacent distinct tau values of the 294: "
          f"{gaps([val(r, name, 'tau') for r in f_pass])}")
        if not name.startswith("R1"):
            P(f"  for orientation only (not a proposed cut): tau >= 0.90 on "
              f"{sum(val(r, name, 'tau') >= CUT for r in f_pass)} of 294 fresh, "
              f"{sum(val(r, name, 'tau') >= CUT for r in f_hi)} of 21 N1>=0.90"
              + ("" if val(s_pass[0], name, 'tau') is None else
                 f", {sum(val(r, name, 'tau') >= CUT for r in s_pass)} of 98 seen"))

    P("")
    P("=" * 100)
    P("2. HISTOGRAMS (tau), fresh 294 passing at lambda = 1, then the N1 >= 0.90 subset")
    P("=" * 100)
    for name, lo, hi, step in (("R3_float_l1", 0.5, 1.0, 0.025), ("R2_float_l1", 0.5, 1.0, 0.025),
                               ("R1a_float_l1", -0.1, 0.5, 0.025)):
        P(f"\n  {name}, all 294:")
        P(hist([val(r, name, "tau") for r in f_pass], lo, hi, step))
        P(f"  {name}, N1 >= 0.90 (21):")
        P(hist([val(r, name, "tau") for r in f_hi], lo, hi, step))
    P(f"\n  R3_float_l1, seen 98:")
    P(hist([val(r, "R3_float_l1", "tau") for r in s_pass], 0.5, 1.0, 0.025))

    def pr(r):
        def g(n, w="tau"):
            x = val(r, n, w)
            return "   -   " if x is None else f"{x:7.4f}"
        rank = (100.0 * np.mean([val(o, "R3_float_l1", "tau") < val(r, "R3_float_l1", "tau")
                                 for o in f_pass]))
        P(f"  {r['key']:12s} lc={r['lambda_c']:5.0f} ceil1={g('full_quant_l1')} "
          f"n1={'   -   ' if r['n1'] is None else format(r['n1']['tau'], '7.4f')} | l=1: "
          f"R3f={g('R3_float_l1')}/{g('R3_float_l1', 'exact')} R3q={g('R3_quant_l1')} "
          f"R2={g('R2_float_l1')} R1a={g('R1a_float_l1')} R1b={g('R1b_float_l1')} "
          f"| lc: full={g('full_quant_lc')} R3f={g('R3_float_lc')}/{g('R3_float_lc', 'exact')} "
          f"R3q={g('R3_quant_lc')} R2={g('R2_float_lc')} R1a={g('R1a_float_lc')} "
          f"maxabs(dc)={r['R3_float_lc_maxabs']:.1e} | R3f_l1 pct-rank in 294: {rank:5.1f}")

    P("")
    P("=" * 100)
    P("3. NAMED BOARDS (tau; R3f shown tau/exact)")
    P("=" * 100)
    P("\nCalibration worlds (FC = board z, grid forced to [100]; FN1, FN2):")
    for r in worlds:
        pr(r)
    P("\nDECODER_SPLIT_AT_LC boards:")
    for k in DECODER_SPLIT:
        pr(next(r for r in fresh if r["key"] == k))
    P("\nThe 15 fresh passes at lambda_c = 100:")
    for r in lam100:
        pr(r)
    P("\nSeen permuted board 89 (the one seen board failing ceil_1):")
    pr(next(r for r in seen if r["key"] == "perm:89"))
    P("\nFresh boards failing ceil_1 (6):")
    for r in fresh:
        if r["full_quant_l1"]["exact"] < CUT:
            pr(r)
    P("")
    P("=" * 100)
    P("4. AT THE CHOSEN lambda_c (fresh 294 passing at lambda = 1, split by lambda_c)")
    P("=" * 100)
    for lc in (1.0, 100.0):
        S = [r for r in f_pass if r["lambda_c"] == lc]
        P(f"\n  lambda_c = {lc:g}: {len(S)} boards")
        for name in ("R3_float_lc", "R3_quant_lc", "R2_float_lc", "R1a_float_lc", "R1a_quant_lc"):
            for which in ("exact", "tau"):
                P(f"    {name:14s} {which:5s} {q([val(r, name, which) for r in S])}")
        P(f"    max |double-centred float logit|: "
          f"{q([r['R3_float_lc_maxabs'] for r in S])}")
    other = sorted({r["lambda_c"] for r in f_pass} - {1.0, 100.0})
    P(f"  other lambda_c among the 294: {other if other else 'none'}")
    return rows


def write_csv(rows):
    names = ["full_quant_l1", "full_float_l1", "n1", "R3_float_l1", "R3_quant_l1", "R2_float_l1",
             "R1a_float_l1", "R1a_quant_l1", "R1b_float_l1", "R1b_quant_l1",
             "full_quant_lc", "full_float_lc", "R3_float_lc", "R3_quant_lc", "R2_float_lc",
             "R1a_float_lc", "R1a_quant_lc", "R1b_float_lc", "R1b_quant_lc"]
    head = ["key", "group", "grid", "lambda_c", "flags"]
    for n in names:
        head += [n, n + "_tau"]
    head += ["R3_float_lc_maxabs", "R3_float_l1_sv2"]
    with open(HERE / "iiib_diag_boards.csv", "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(head)
        for r in rows:
            line = [r["key"], r["group"], r["grid"], f"{r['lambda_c']:g}", r["flags"]]
            for n in names:
                x = r.get(n)
                line += (["", ""] if x is None else [f"{x['exact']:.6f}", f"{x['tau']:.6f}"])
            line += [f"{r['R3_float_lc_maxabs']:.3e}", f"{r['R3_float_l1_sv2']:.3e}"]
            w.writerow(line)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    write_csv(main())
