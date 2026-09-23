"""Post-run script of the second rule (docs/plans/2026-09-23-second-rule-proposal.md sections 1,
4.2, 5.2 and 6). It runs AFTER the harness has written the run's record and the record has been
committed. It changes no harness file and no verdict.

What it does, in order:
 1. The spread-log check (section 6; Mike, 2026-09-23 14:40 UTC): counts the per-fit files
    against the 1,341 rule fits the harness makes and writes spread_log_validation.json. A
    mismatch marks the spread log unreliable and DOES NOT void the verdict; it is flagged in the
    first lines of RESULT.md.
 2. Deterministic refits with the harness's own functions (harness._w_init / _w_task, the same
    code the harness's precompute runs), at the record's k:
      - BF_1, BF_2, BF_3, BF_4 per fold (bf_predictor(r));
      - RP_1 per fold, all 20 seeds x 2 sides;
      - leave-one-type-out per type, for the rule and for N1.
    Checks: the mean BF_1 margin must equal the record's P4.bf.margin to 1e-12 (else the paired
    read is void); the RP_1 maximum must equal the record's rp_threshold to 1e-12; at k = 10,
    BF_3 and BF_4 must reproduce harness_controls.json's +0.04034 and +0.03972 (to 1e-12); the
    per-type LOTO means must equal the record's loto means (to 1e-12).
 3. The mandatory BF_1..BF_4 line, the registered P4 tie-band reading, and S2-8's paired read,
    inserted into RESULT.md directly under the harness's verdict line (the verdict line itself is
    printed verbatim and not altered). Also post_run.json, per_fold_opponents.csv and
    loto_per_type.csv.

Usage (from the repository root), after the run's record is committed:
    tools/.venv/Scripts/python.exe results/genome/c6/rules/second_rule/post_run.py [--workers N]
        [--run-dir results/genome/c6/rule_runs/second_rule_r1]
    tools/.venv/Scripts/python.exe results/genome/c6/rules/second_rule/post_run.py --selftest
The self-test builds a stand-in record on the synthetic bank ST0 (gate_banks.py: GB0's
construction with seed 61000, not a gate bank) at k = 1 in a temporary directory and runs every
step on it. It touches no real-bank cell.
"""

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import csv
import json
import math
import re
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
C6 = HERE.parents[1]
ROOT = C6.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(C6))

SPREAD_ENV = "SECOND_RULE_SPREAD_DIR"
N_RULE_FITS = 1341
TIE_BAND = 0.002
REAL_AMOUNT_MIN = 0.005
EXACT = 1e-12
BF_RANKS = (1, 2, 3, 4)
# harness_controls.json (harness 6fc80952..., k = 10): "real/N1 as a rule" (r = 3) and
# "real/PR" (r = 4), P4.bf.margin
CONTROLS_BF_K10 = {3: 0.04034078611097054, 4: 0.039723750076924115}
BLOCK_START = "<!-- second-rule post-run: start -->"
BLOCK_END = "<!-- second-rule post-run: end -->"


# ==========================================================================================
# 1. The spread-log check
# ==========================================================================================
def expected_spread_counts(bank="real"):
    """The rule fits of one harness rule run, by bank name (harness.precompute)."""
    exp = {bank: 10 + 65 + 1}
    for sd in range(99):
        exp[f"{bank}.shuffle{sd}"] = 10
    for fi in range(5):
        for sd in range(5):
            exp[f"{bank}.dial{fi}_{sd}" if fi else f"{bank}.dial0_{sd}"] = 11
    assert sum(exp.values()) == N_RULE_FITS
    return exp


def spread_check(spread_dir, bank="real"):
    d = Path(spread_dir)
    files = sorted(d.glob("*.json")) if d.is_dir() else []
    tmp_left = sorted(p.name for p in d.glob("*.tmp*")) if d.is_dir() else []
    parsed, bad, by_bank = 0, [], {}
    for p in files:
        try:
            rec = json.loads(p.read_text(encoding="utf-8"))
            parsed += 1
            by_bank[rec["bank"]] = by_bank.get(rec["bank"], 0) + 1
        except (ValueError, KeyError):
            bad.append(p.name)
    exp = expected_spread_counts(bank)
    diff = {b: [by_bank.get(b, 0), n] for b, n in exp.items() if by_bank.get(b, 0) != n}
    diff.update({b: [n, 0] for b, n in by_bank.items() if b not in exp})
    ok = len(files) == N_RULE_FITS and not bad and not diff and not tmp_left
    return {"spread_dir": str(d.relative_to(ROOT).as_posix()) if d.is_absolute()
            and ROOT in d.parents else str(d),
            "files": len(files), "files_parsing_as_json": parsed, "files_not_parsing": bad,
            "temporary_files_left": tmp_left, "rule_fits_made_by_harness": N_RULE_FITS,
            "per_bank_mismatches_found_vs_expected": diff,
            "file_count_equals_fit_count": len(files) == N_RULE_FITS,
            "spread_log_reliable": bool(ok),
            "note": "Checked after the record was written and committed. A mismatch marks the "
                    "spread log unreliable and does not void the verdict (Mike, 2026-09-23 "
                    "14:40 UTC; proposal section 6)."}


# ==========================================================================================
# 2. Deterministic refits through the harness's own worker functions
# ==========================================================================================
def _init(rule_path, k, bank):
    os.environ.pop(SPREAD_ENV, None)            # refits write no spread files
    import harness as H
    H._w_init(rule_path, k)
    if bank != "real":                          # self-test only: the synthetic bank ST0
        from gate_banks import gate_bank
        H._W["banks"][bank] = gate_bank(bank)


def _task(task):
    import harness as H
    return task, H._w_task(task)


def refit_tasks(bank, rank):
    tasks = [("cv", f"BF:{r}", bank, f) for r in BF_RANKS for f in range(10)]
    tasks += [("cv", f"RP:{rank}:{1000 + j}:{side}", bank, f) for j in range(20)
              for side in (0, 1) for f in range(10)]
    tasks += [("loto", pk, bank, i) for pk in ("rule", "N1") for i in range(65)]
    return tasks


def run_refits(rule_path, k, bank, rank, workers):
    tasks = refit_tasks(bank, rank)
    with ProcessPoolExecutor(max_workers=workers, initializer=_init,
                             initargs=(str(rule_path), k, bank)) as ex:
        return dict(ex.map(_task, tasks, chunksize=2))


# ==========================================================================================
# 3. Readings
# ==========================================================================================
def fold_margin(pred_scores, n1_scores):
    """Per-fold existence margin over N1 (larger = better), as harness.margin averages it."""
    return [n["existence"] - p["existence"] for p, n in zip(pred_scores, n1_scores)]


def tie_band_reading(delta, harness_pass):
    """Section 1: Delta = rule margin - P4 threshold. Within +-0.002 a tie; P4 counts for this
    registration only if Delta > +0.002."""
    if delta > TIE_BAND:
        reading = "passed (Delta > +0.002)"
    elif delta >= -TIE_BAND:
        reading = "tie (|Delta| <= 0.002): not a pass for this registration"
    else:
        reading = "fail (Delta < -0.002)"
    note = ""
    if harness_pass and delta <= TIE_BAND:
        note = ("The harness prints P4 as passed with 0 < Delta <= +0.002; this registration "
                "reads it as a tie.")
    return {"delta": delta, "reading": reading, "counts_as_pass": bool(delta > TIE_BAND),
            "harness_P4_pass": bool(harness_pass), "note": note}


def s28_reading(per_fold_delta):
    """S2-8: Delta = rule margin - BF_1 margin; the real-amount bar is max(+0.005, 2 x the
    paired standard error of the ten per-fold Deltas)."""
    x = np.asarray(per_fold_delta, float)
    se = float(np.std(x, ddof=1) / math.sqrt(len(x)))
    bar = max(REAL_AMOUNT_MIN, 2 * se)
    d = float(np.mean(x))
    if d <= TIE_BAND:
        zone = "Delta <= +0.002: a P4 fail or a registered tie; refutes S2-8's claim"
    elif d < bar:
        zone = "+0.002 < Delta < bar: P4 passed under the tie band, not a real amount"
    else:
        zone = "Delta >= bar: a real amount"
    return {"delta_mean": d, "per_fold_delta": x.tolist(), "paired_se": se, "bar": bar,
            "zone": zone}


def fmt(x):
    return f"{x:+.5f}"


def render_block(spread, bfline, tie, s28, checks):
    L = [BLOCK_START, ""]
    if not spread["spread_log_reliable"]:
        L += [f"**FLAG: spread log unreliable.** {spread['files']} per-fit files for "
              f"{spread['rule_fits_made_by_harness']} rule fits (details: "
              f"`spread_log_validation.json`). The verdict stands: no verdict number derives "
              f"from the spread log (Mike, 2026-09-23 14:40 UTC).", ""]
    else:
        L += [f"Spread log: {spread['files']} per-fit files for "
              f"{spread['rule_fits_made_by_harness']} rule fits; all parse.", ""]
    L += [f"**Margins against BF_1-BF_4 (mandatory; k = {bfline['k']}):** rule margin over N1 "
          f"{fmt(bfline['rule_margin'])}. " + "; ".join(
              f"rule - BF_{r} = {fmt(bfline['rule_minus_bf'][str(r)])} (BF_{r} "
              f"{fmt(bfline['bf_margin'][str(r)])})" + (" **the decision**" if r == 1
                                                         else " context only")
              for r in BF_RANKS) + ".", "",
          f"**P4 tie band (registered):** Delta = rule margin - P4 threshold = "
          f"{fmt(tie['delta'])} (threshold {fmt(tie['threshold'])}); reading: "
          f"**{tie['reading']}**. Harness P4 pass: {tie['harness_P4_pass']}. {tie['note']}".rstrip(),
          ""]
    if checks["bf1_matches_record"]:
        L += [f"S2-8 paired read: Delta = rule - BF_1 = {fmt(s28['delta_mean'])}, paired SE "
              f"{s28['paired_se']:.5f}, real-amount bar {s28['bar']:.5f}; {s28['zone']}.", ""]
    else:
        L += ["S2-8 paired read: **void** (the refitted BF_1 margin does not equal the record's "
              "P4.bf.margin to 1e-12).", ""]
    L += ["Reproduction checks: " + "; ".join(f"{k} {v}" for k, v in checks.items()) + ".",
          "Written by `rules/second_rule/post_run.py` after the record was committed; details "
          "in `post_run.json`.", "", BLOCK_END]
    return "\n".join(L)


def insert_block(md_text, block):
    """Put the block directly under the verdict line (the first bold line), replacing an older
    block. The verdict line is not touched."""
    if BLOCK_START in md_text:
        md_text = re.sub(re.escape(BLOCK_START) + r".*?" + re.escape(BLOCK_END) + r"\n\n?", "",
                         md_text, flags=re.S)
    lines = md_text.split("\n")
    i = next(j for j, x in enumerate(lines) if x.startswith("**C6 verdict for "))
    return "\n".join(lines[:i + 1] + ["", block] + lines[i + 1:])


def main(run_dir, workers, spread_dir=None, bank="real", controls_check=True):
    t0 = time.time()
    run_dir = Path(run_dir)
    rec = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
    e, st = rec["exam"], rec["stamp"]
    k, rank = int(st["starts_k"]), int(e["P4"]["rank"])
    assert rank == 1, "the registration computes r = 1 (section 1)"
    rule_path = ROOT / st["rule_file"] if not Path(st["rule_file"]).is_absolute() \
        else Path(st["rule_file"])
    # ---- 1. spread log
    spread = spread_check(spread_dir or (run_dir / "spread"), bank)
    (run_dir / "spread_log_validation.json").write_text(json.dumps(spread, indent=1) + "\n",
                                                        encoding="utf-8", newline="\n")
    print("spread log:", {x: spread[x] for x in ("files", "spread_log_reliable")}, flush=True)
    # ---- 2. refits
    import harness as H
    res = run_refits(rule_path, k, bank, rank, workers)
    n1 = e["per_fold_N1"]
    bf = {r: [res[("cv", f"BF:{r}", bank, f)] for f in range(10)] for r in BF_RANKS}
    bf_margin = {r: H.margin(bf[r], n1, "existence") for r in BF_RANKS}
    rp = {}
    for j in range(20):
        for side in (0, 1):
            rp[(1000 + j, side)] = [res[("cv", f"RP:{rank}:{1000 + j}:{side}", bank, f)]
                                    for f in range(10)]
    rp_margin = {key: H.margin(v, n1, "existence") for key, v in rp.items()}
    rp_best = max(rp_margin, key=lambda key: (rp_margin[key], -key[0], -key[1]))
    loto_rule = [res[("loto", "rule", bank, i)] for i in range(65)]
    loto_n1 = [res[("loto", "N1", bank, i)] for i in range(65)]
    checks = {
        "bf1_matches_record": abs(bf_margin[1] - e["P4"]["bf"]["margin"]) <= EXACT,
        "rp_max_matches_record": abs(rp_margin[rp_best] - e["P4"]["rp_threshold"]) <= EXACT,
        "loto_means_match_record": all(
            abs(float(np.nanmean([x[f] for x in loto_rule])) - e["loto"][f]["rule_mean"]) <= EXACT
            and abs(float(np.nanmean([x[f] for x in loto_n1])) - e["loto"][f]["n1_mean"]) <= EXACT
            for f in H.FIELDS),
    }
    if controls_check and k == 10:
        for r, v in CONTROLS_BF_K10.items():
            checks[f"bf{r}_reproduces_controls"] = abs(bf_margin[r] - v) <= EXACT
    # ---- 3. readings
    rule_m = e["P4"]["rule_margin_existence"]
    bfline = {"k": k, "rule_margin": rule_m,
              "bf_margin": {str(r): bf_margin[r] for r in BF_RANKS},
              "rule_minus_bf": {str(r): rule_m - bf_margin[r] for r in BF_RANKS}}
    tie = tie_band_reading(rule_m - e["P4"]["threshold"], e["P4"]["pass"])
    tie["threshold"] = e["P4"]["threshold"]
    s28 = s28_reading([r - b for r, b in zip(fold_margin(e["per_fold_rule"], n1),
                                             fold_margin(bf[1], n1))])
    out = {"what": "Second rule post-run (proposal sections 1, 4.2, 5.2, 6). Descriptive; no "
                   "verdict is changed.",
           "record": str((run_dir / "result.json").as_posix()), "k": k, "rank": rank,
           "verdict_line": rec["verdict_line"], "git_head": subprocess.run(
               ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True
           ).stdout.strip(),
           "spread_log": spread, "bf_line": bfline, "p4_tie_band": tie, "s2_8": s28,
           "checks": checks,
           "rp_threshold_argmax": {"seed": rp_best[0], "side": rp_best[1],
                                   "margin": rp_margin[rp_best]},
           "runtime_s": None}
    with open(run_dir / "per_fold_opponents.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["fold", "rule", "N1"] + [f"BF_{r}" for r in BF_RANKS] + ["RP_1_argmax"])
        for f in range(10):
            w.writerow([f, repr(e["per_fold_rule"][f]["existence"]), repr(n1[f]["existence"])]
                       + [repr(bf[r][f]["existence"]) for r in BF_RANKS]
                       + [repr(rp[rp_best][f]["existence"])])
    with open(run_dir / "loto_per_type.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["type_index", "type_name"] + [f"rule_{f}" for f in H.FIELDS]
                   + [f"N1_{f}" for f in H.FIELDS])
        for i in range(65):
            w.writerow([i, H.NAMES[i]] + [repr(loto_rule[i][f]) for f in H.FIELDS]
                       + [repr(loto_n1[i][f]) for f in H.FIELDS])
    out["runtime_s"] = round(time.time() - t0, 1)
    (run_dir / "post_run.json").write_text(json.dumps(out, indent=1, default=float) + "\n",
                                           encoding="utf-8", newline="\n")
    md = run_dir / "RESULT.md"
    md.write_text(insert_block(md.read_text(encoding="utf-8"),
                               render_block(spread, bfline, tie, s28, checks)),
                  encoding="utf-8", newline="\n")
    print(render_block(spread, bfline, tie, s28, checks))
    return out


# ==========================================================================================
# Self-test on the synthetic bank ST0 (k = 1), never on a gate bank: a stand-in record, then
# every step
# ==========================================================================================
def _selftest_cv(job):
    key, f = job
    import harness as H
    return job, H._w_task(("cv", key, "ST0", f))


def selftest(workers):
    import harness as H
    import fit as R
    tmp = Path(tempfile.mkdtemp(prefix="second_rule_post_run_selftest_"))
    rule_file = HERE / "fit.py"
    with ProcessPoolExecutor(max_workers=workers, initializer=_init,
                             initargs=(str(rule_file), 1, "ST0")) as ex:
        jobs = [(key, f) for key in ("rule", "N1", "BF:1") for f in range(10)]
        cvr = dict(ex.map(_selftest_cv, jobs))
        loto_jobs = [("loto", pk, "ST0", i) for pk in ("rule", "N1") for i in range(65)]
        lres = dict(ex.map(_task, loto_jobs))
        rp_jobs = [("cv", f"RP:1:{1000 + j}:{side}", "ST0", f) for j in range(20)
                   for side in (0, 1) for f in range(10)]
        rres = dict(ex.map(_task, rp_jobs))
    per = {key: [cvr[(key, f)] for f in range(10)] for key in ("rule", "N1", "BF:1")}
    rp_thr = max(H.margin([rres[("cv", f"RP:1:{1000 + j}:{side}", "ST0", f)] for f in range(10)],
                          per["N1"], "existence") for j in range(20) for side in (0, 1))
    bfm = H.margin(per["BF:1"], per["N1"], "existence")
    rm = H.margin(per["rule"], per["N1"], "existence")
    thr = max(rp_thr, bfm)
    loto = {f: {"rule_mean": float(np.nanmean([lres[("loto", "rule", "ST0", i)][f]
                                               for i in range(65)])),
                "n1_mean": float(np.nanmean([lres[("loto", "N1", "ST0", i)][f]
                                             for i in range(65)]))} for f in H.FIELDS}
    rec = {"verdict_line": "C6 verdict for second_rule_r1 (k = 1 starts, r = 1): SELFTEST",
           "stamp": {"starts_k": 1, "rule_file": str(rule_file)},
           "exam": {"name": R.NAME, "per_fold_rule": per["rule"], "per_fold_N1": per["N1"],
                    "P4": {"rank": 1, "rule_margin_existence": rm, "rp_threshold": rp_thr,
                           "bf": {"margin": bfm}, "threshold": thr,
                           "pass": bool(rm - thr > H.TAU)}, "loto": loto}}
    (tmp / "result.json").write_text(json.dumps(rec, default=float), encoding="utf-8")
    (tmp / "RESULT.md").write_text("# C6 run: selftest\n\n**" + rec["verdict_line"] +
                                   "**\n\nVerdict labels ...\n", encoding="utf-8")
    spread = tmp / "spread"
    spread.mkdir()
    for i in range(3):                                   # a deliberately short spread log
        (spread / f"x{i}.json").write_text(json.dumps({"bank": "ST0"}), encoding="utf-8")
    out = main(tmp, workers, spread_dir=spread, bank="ST0", controls_check=False)
    assert out["checks"]["bf1_matches_record"] and out["checks"]["rp_max_matches_record"]
    assert out["checks"]["loto_means_match_record"]
    assert not out["spread_log"]["spread_log_reliable"]
    md = (tmp / "RESULT.md").read_text(encoding="utf-8")
    assert md.index("**C6 verdict") < md.index("FLAG: spread log unreliable") < \
        md.index("Verdict labels")
    again = insert_block(md, render_block(out["spread_log"], out["bf_line"], out["p4_tie_band"],
                                          out["s2_8"], out["checks"]))
    assert again.count(BLOCK_START) == 1
    print(f"SELFTEST PASSED ({tmp})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", default=str(C6 / "rule_runs" / "second_rule_r1"))
    ap.add_argument("--spread-dir", default=None)
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest(a.workers)
    else:
        main(a.run_dir, a.workers, a.spread_dir)
