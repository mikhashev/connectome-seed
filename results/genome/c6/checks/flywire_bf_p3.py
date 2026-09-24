#!/usr/bin/env python3
"""BF_r (r=1..4) on two 30-type banks, each against its own 99 native shuffles.

Arm "flywire30": the FlyWire right-optic-lobe bank (flywire_bank_builder.py output). Arm
"flyvis30": harness.py's own H.REAL restricted to the same 30 types. Registered in
docs/plans/2026-09-24-flywire-bf-p3-registration.md. NOT RUN.

Usage: tools/.venv/Scripts/python.exe results/genome/c6/checks/flywire_bf_p3.py [--workers N]
       tools/.venv/Scripts/python.exe results/genome/c6/checks/flywire_bf_p3.py --machine-check-only
"""
import argparse
import csv
import json
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
C6 = HERE.parent
ROOT = C6.parents[2]                                   # the repository root
DEFAULT_OUT = HERE / "flywire_bf_p3"
REGISTRATION = "docs/plans/2026-09-24-flywire-bf-p3-registration.md"
EXPECTED_HARNESS_SHA = "6fc809527c69ee84aadebfc15c0ba755c189ddc93c80c05c0fa11d969a8d7297"
MACHINE_CHECK_TOL = 1e-9
FLYVIS_RECORDED_BF1_MARGIN = 0.028150051052145946
RANKS = (1, 2, 3, 4)
BONFERRONI_ALPHA = 0.05 / len(RANKS)
MIN_TOTAL_PAIRS = 100

sys.path.insert(0, str(C6))
import harness as H  # noqa: E402

from flywire_bank_builder import FLYWIRE_NAME_OF  # noqa: E402

# The flyvis bank, captured at import, before any arm repoints H.REAL. The flyvis30 arm is cut
# from this object, never from H.REAL, which holds the FlyWire bank once that arm has run.
FLYVIS_REAL = H.REAL
assert FLYVIS_REAL.name == "real", f"harness REAL is {FLYVIS_REAL.name!r} at import, expected 'real'"

FLYWIRE_TYPES = sorted(FLYWIRE_NAME_OF)          # single source of truth for the type set (30)
FLYWIRE_IDX = sorted(H.IDX[n] for n in FLYWIRE_TYPES)
MANIFEST_PATH = ROOT.parent / "connectome-seed-data" / "FlyWire" / "derived" / "bank.meta.json"

ARM_BANK_NAME = {"flywire30": "flywire_ol_right_30", "flyvis30": "flyvis_restricted_30"}
ARMS = tuple(ARM_BANK_NAME)


def git_head():
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                           text=True, check=True).stdout.strip()


def dirty_tree():
    return subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True,
                           text=True, check=True).stdout.strip()


def refuse_if_unsafe(allow_dirty):
    if not allow_dirty:
        d = dirty_tree()
        if d:
            sys.exit(f"REFUSED: uncommitted changes; commit {REGISTRATION} first.\n" + d)
    got_sha = H.sha256_lf(C6 / "harness.py")
    if got_sha != EXPECTED_HARNESS_SHA:
        sys.exit(f"REFUSED: harness.py sha256_lf is {got_sha}, expected {EXPECTED_HARNESS_SHA}; "
                 "this needs a new registration, not a silent re-run.")


def restrict_to_30_grid():
    """H.FOLD, H.TYPE_FIELDS, H.PAIR_ID, H.NAMES/H.IDX are left untouched, for either arm."""
    H.ALL_CELLS = np.array([(s, t) for s in FLYWIRE_IDX for t in FLYWIRE_IDX], dtype=np.int64)


def manifest_sha256():
    if not MANIFEST_PATH.exists():
        sys.exit(f"REFUSED: no built FlyWire bank at {MANIFEST_PATH}; run "
                 "flywire_bank_builder.py (full build, not --inspect-only) first.")
    return H.hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest()


def load_flywire_bank():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    offsets_path = MANIFEST_PATH.parent / manifest["offsets_file"]
    content = {}
    with open(offsets_path, newline="", encoding="utf-8") as fh:
        r = csv.DictReader(fh)
        for row in r:
            k = (H.IDX[row["src"]], H.IDX[row["tar"]])
            c = content.setdefault(k, {"offsets": {}, "hull": [], "sign": int(row["sign"])})
            c["offsets"][(int(row["du"]), int(row["dv"]))] = float(row["n_syn"])
    bad = ({s for s, t in content} | {t for s, t in content}) - set(FLYWIRE_IDX)
    if bad:
        sys.exit(f"REFUSED: bank content references type indices outside the 30-type set: {bad}")
    return H.Bank(ARM_BANK_NAME["flywire30"], content), manifest


def build_flyvis30_bank():
    """No new data: every offset row is copied unchanged from harness.py's own REAL_CONTENT."""
    content = {(s, t): c for (s, t), c in FLYVIS_REAL.content.items()
               if s in set(FLYWIRE_IDX) and t in set(FLYWIRE_IDX)}
    return H.Bank(ARM_BANK_NAME["flyvis30"], content)


def load_bank_for_arm(arm):
    if arm == "flywire30":
        return load_flywire_bank()
    if arm == "flyvis30":
        return build_flyvis30_bank(), None
    raise ValueError(f"unknown arm {arm!r}")


def worker_init(arm, expected_manifest_sha):
    """Windows spawn: each worker re-imports this module and must be re-patched here."""
    if arm == "flywire30":
        got = manifest_sha256()
        if got != expected_manifest_sha:
            sys.exit(f"REFUSED (worker, arm={arm}): bank manifest sha {got} != parent's "
                     f"{expected_manifest_sha}.")
    bank, _ = load_bank_for_arm(arm)
    restrict_to_30_grid()
    H.REAL = bank


def diagnose(bank, log):
    ex = bank.exists
    total = int(sum(ex[s, t] for s in FLYWIRE_IDX for t in FLYWIRE_IDX))
    per_fold = {}
    for f in range(H.N_FOLDS):
        held = H.FOLD == f
        cells = H.ALL_CELLS[held[H.ALL_CELLS[:, 0], H.ALL_CELLS[:, 1]]]
        n = int(sum(ex[s, t] for s, t in cells.tolist()))
        per_fold[f] = n
    out_deg = {n: int(ex[H.IDX[n]].sum()) for n in FLYWIRE_TYPES}
    in_deg = {n: int(ex[:, H.IDX[n]].sum()) for n in FLYWIRE_TYPES}
    diag = {"total_nonempty_pairs": total, "density": total / len(H.ALL_CELLS),
            "per_outer_fold_nonempty": per_fold,
            "out_degree_by_type": out_deg, "in_degree_by_type": in_deg}
    log(f"  diagnostics: total_nonempty_pairs={total}, density={diag['density']:.4f}")
    log(f"  per-outer-fold nonempty: {per_fold}")
    return diag


def stop_reason(diag):
    if diag["total_nonempty_pairs"] < MIN_TOTAL_PAIRS:
        return (f"fewer than {MIN_TOTAL_PAIRS} nonempty pairs "
                f"({diag['total_nonempty_pairs']})")
    empty_folds = [f for f, n in diag["per_outer_fold_nonempty"].items() if n == 0]
    if empty_folds:
        return f"outer fold(s) {empty_folds} have 0 nonempty test pairs"
    return None


def machine_check(log):
    pred = H.bf_predictor(1)
    rule_s = H.cv(pred, H.REAL)
    n1_s = H.cv(H.N1, H.REAL)
    m = H.margin(rule_s, n1_s, "existence")
    diff = m - FLYVIS_RECORDED_BF1_MARGIN
    ok = abs(diff) <= MACHINE_CHECK_TOL
    check = {"recorded": FLYVIS_RECORDED_BF1_MARGIN, "this_run": m, "difference": diff,
             "tolerance": MACHINE_CHECK_TOL, "passed": bool(ok)}
    log(f"machine check (wrapper on flyvis bank, unpatched grid): {check}")
    return check


def shuffle_margins(args):
    arm, rank, seed = args
    expected_name = ARM_BANK_NAME[arm]
    assert H.REAL.name == expected_name, \
        f"worker (arm={arm}) has H.REAL={H.REAL.name!r}, expected {expected_name!r}"
    assert len(H.ALL_CELLS) == len(FLYWIRE_TYPES) ** 2, \
        f"worker (arm={arm}) has len(H.ALL_CELLS)={len(H.ALL_CELLS)}, expected " \
        f"{len(FLYWIRE_TYPES) ** 2}"
    pred = H.bf_predictor(rank)
    b, inv = H.shuffled_bank(H.REAL, seed)
    assert inv["out_degrees_kept"] and inv["in_degrees_kept"]
    rs, ns = H.cv(pred, b), H.cv(H.N1, b)
    m = {f: H.margin(rs, ns, f) for f in H.FIELDS}
    lambdas = [rs[k].get("bf_lambda") for k in range(H.N_FOLDS)]
    return rank, seed, m, lambdas


def real_margins(rank):
    pred = H.bf_predictor(rank)
    rs, ns = H.cv(pred, H.REAL), H.cv(H.N1, H.REAL)
    m = {f: H.margin(rs, ns, f) for f in H.FIELDS}
    lambdas = [rs[k].get("bf_lambda") for k in range(H.N_FOLDS)]
    return m, lambdas


def run_arm(arm, bank, bank_manifest, bank_manifest_sha, out, workers, log):
    arm_out = out / arm
    arm_out.mkdir(parents=True, exist_ok=True)

    diag = diagnose(bank, log)
    reason = stop_reason(diag)
    if reason is not None:
        return {"diagnostics": diag, "stopped": True, "stop_reason": reason, "per_rank": None}

    per_rank = {}
    for rank in RANKS:
        log(f"[{arm}] rank {rank}: real bank ...")
        real_m, real_lambdas = real_margins(rank)
        log(f"[{arm}] rank {rank}: fitting {H.N_SHUFFLES} shuffles, workers={workers} ...")
        tasks = [(arm, rank, sd) for sd in range(H.N_SHUFFLES)]
        if workers <= 1:
            results = [shuffle_margins(t) for t in tasks]
        else:
            with ProcessPoolExecutor(max_workers=workers, initializer=worker_init,
                                     initargs=(arm, bank_manifest_sha)) as ex:
                results = list(ex.map(shuffle_margins, tasks))
        rows = [{"bank": "real", "seed": None, "kind": "real", "rank": rank,
                 **real_m, "bf_lambda_per_fold": real_lambdas}]
        for _, sd, m, lambdas in sorted(results, key=lambda x: x[1]):
            rows.append({"bank": f"shuffle{sd}", "seed": sd, "kind": "shuffle", "rank": rank,
                         **m, "bf_lambda_per_fold": lambdas})

        ex_field = "existence"
        real_v = real_m[ex_field]
        sh_v = [r[ex_field] for r in rows[1:]]
        n_ge = sum(1 for v in sh_v if v >= real_v)
        p = (1 + n_ge) / (1 + H.N_SHUFFLES)
        strictly_above_all = all(real_v - v > H.TAU for v in sh_v)
        if strictly_above_all and n_ge == 0:
            branch = "A: BF_r separates"
        elif p >= 0.05:
            branch = "B: BF_r does not separate"
        else:
            branch = "C: in between"

        max_lam = max(H.BF_LAMBDAS)
        real_frac_max_lambda = sum(1 for lam in real_lambdas if lam == max_lam) / len(real_lambdas)
        shuffle_lambdas = [lam for r in rows[1:] for lam in r["bf_lambda_per_fold"]]
        shuffle_frac_max_lambda = (sum(1 for lam in shuffle_lambdas if lam == max_lam) /
                                    len(shuffle_lambdas))

        per_rank[rank] = {
            "real_margin": real_v, "shuffled_min": float(min(sh_v)),
            "shuffled_mean": float(sum(sh_v) / len(sh_v)), "shuffled_max": float(max(sh_v)),
            "n_shuffled_ge_real": n_ge, "strictly_above_all": bool(strictly_above_all),
            "p_one_sided": p, "bonferroni_alpha": BONFERRONI_ALPHA,
            "survives_bonferroni": bool(p < BONFERRONI_ALPHA), "branch": branch,
            "gap": real_v - max(sh_v),
            "real_frac_folds_at_max_lambda": real_frac_max_lambda,
            "shuffle_frac_folds_at_max_lambda": shuffle_frac_max_lambda,
            # Registration section 5: the two readings of a B, cut fixed before any FlyWire value.
            "negative_reading": (None if not branch.startswith("B") else
                                 "absent: CV switches the term off in most real folds"
                                 if real_frac_max_lambda >= 0.5 else
                                 "present but not bank-specific: fitted, shuffles do as well"),
        }
        with open(arm_out / f"per_shuffle_rank{rank}.csv", "w", newline="") as fh:
            fieldnames = ["bank", "seed", "kind", "rank"] + list(H.FIELDS) + ["bf_lambda_per_fold"]
            w = csv.DictWriter(fh, fieldnames=fieldnames)
            w.writeheader()
            for row in rows:
                row = dict(row)
                row["bf_lambda_per_fold"] = json.dumps(row["bf_lambda_per_fold"])
                w.writerow(row)
        log(f"[{arm}] rank {rank}: branch {branch}, p={p:.3f}, "
            f"real_frac_max_lambda={real_frac_max_lambda:.2f}")

    return {"diagnostics": diag, "stopped": False, "per_rank": per_rank,
            "bank_manifest": bank_manifest, "bank_name": bank.name}


def joint_reading(flywire_branch, flyvis_branch):
    """Registration section 5a. Branch labels start with "A", "B" or "C"."""
    fw, fv = flywire_branch[0], flyvis_branch[0]
    if fv == "A" and fw == "A":
        return "both banks separate: the pattern is present in the second brain."
    if fv == "A" and fw == "B":
        return ("flyvis-30 separates, FlyWire-30 does not: the pattern did not carry over to "
                "the second brain.")
    if fv == "A" and fw == "C":
        return ("flyvis-30 separates, FlyWire-30 is in between: weak or partial carry-over; "
                "neither 'present' nor 'did not carry over' is supported.")
    if fv != "A" and fw != "A":
        return ("flyvis-30 does not separate on the 30-type grid: the substrate is too narrow for "
                "this test to show anything -- read as the test failing, not as evidence about "
                "the hypothesis, whatever FlyWire-30 shows short of A.")
    if fv != "A" and fw == "A":
        return ("FlyWire-30 separates, flyvis-30 does not: an unexpected direction -- read as a "
                "flag to re-examine both fits before drawing a substantive conclusion.")
    raise ValueError(f"unhandled branch pair {flywire_branch!r}, {flyvis_branch!r}")


SENSITIVITY = HERE / "flywire_sensitivity" / "summary.json"


def sensitivity_label():
    """Registration section 3b: the label is fixed by the sensitivity builds, before any BF value."""
    if not SENSITIVITY.exists():
        sys.exit(f"REFUSED: {SENSITIVITY} is missing; run flywire_sensitivity.py and commit it "
                 "before this run (registration section 3b).")
    return json.loads(SENSITIVITY.read_text(encoding="utf-8"))["primary_verdict_label"]


def write_result_md(out, summary, arm_results):
    """RESULT.md for a reader who has not opened the registration: every number, both arms,
    every rank, the joint reading and, for any B, which negative reading applies (section 5)."""
    md = ["# BF_r on FlyWire-30 and flyvis-30: P3 against each bank's own 99 shuffles", "",
          f"Registration: `{REGISTRATION}`. Machine check (unpatched wrapper, flyvis full bank): "
          f"{summary['machine_check']['passed']} (difference "
          f"{summary['machine_check']['difference']:.2e}).", "",
          f"**Headline, r = 1:** FlyWire-30 {summary['headline_r1']['flywire30_branch']}; "
          f"flyvis-30 {summary['headline_r1']['flyvis30_branch']}. "
          f"**Joint reading:** {summary['headline_r1']['joint_reading']}", "",
          "| arm | r | real margin | shuffled mean | shuffled max | n >= real | p | "
          "p < 0.0125 | gap | real folds at lambda=100 | shuffle folds at lambda=100 | branch | "
          "negative reading |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for arm in ARMS:
        for rank in RANKS:
            q = arm_results[arm]["per_rank"][rank]
            md.append(f"| {arm} | {rank} | {q['real_margin']:+.5f} | {q['shuffled_mean']:+.5f} | "
                      f"{q['shuffled_max']:+.5f} | {q['n_shuffled_ge_real']} | "
                      f"{q['p_one_sided']:.2f} | {q['survives_bonferroni']} | {q['gap']:+.5f} | "
                      f"{q['real_frac_folds_at_max_lambda']:.2f} | "
                      f"{q['shuffle_frac_folds_at_max_lambda']:.2f} | {q['branch']} | "
                      f"{q['negative_reading'] or '-'} |")
    label = sensitivity_label()
    md[4] = md[4] + f" **Label (registration section 3b):** {label}."
    full65 = json.loads((HERE / "bf1_p3" / "summary.json").read_text(encoding="utf-8"))["branch"]
    if not summary["headline_r1"]["flyvis30_branch"].startswith("A") and full65.startswith("A"):
        md += ["", "**Also (registration section 5a, printed, not a branch):** the full-65 flyvis "
               f"BF_1 was {full65!r}, but flyvis-30 is not A at r = 1: the separating structure "
               "does not live in the 30 column-assigned types alone; some of the 35 dropped types "
               "carry it."]
    md += ["", "## Joint reading per rank", "", "| r | FlyWire-30 | flyvis-30 | reading |",
           "|---|---|---|---|"]
    for rank in RANKS:
        j = summary["per_rank_joint"][rank]
        md.append(f"| {rank} | {j['flywire30_branch']} | {j['flyvis30_branch']} | "
                  f"{j['joint_reading']} |")
    md += ["", summary["note_flyvis30_vs_full_65_bf1"], "",
           f"git_head={summary['git_head']}, runtime={summary['runtime_s']:.1f}s.", ""]
    (out / "RESULT.md").write_text("\n".join(md), encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=max(1, (__import__("os").cpu_count() or 2) - 2))
    ap.add_argument("--out", default=None)
    ap.add_argument("--allow-dirty", action="store_true")
    ap.add_argument("--machine-check-only", action="store_true")
    a = ap.parse_args()

    refuse_if_unsafe(a.allow_dirty)
    out = Path(a.out) if a.out else DEFAULT_OUT
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    log = lambda m: print(m, flush=True)

    log(f"sensitivity label (registration section 3b): {sensitivity_label()}")
    check = machine_check(log)
    if not check["passed"]:
        (out / "summary.json").write_text(json.dumps(
            {"machine_check": check, "stopped_before_bank_load": True,
             "registration": REGISTRATION, "git_head": git_head()}, indent=2))
        sys.exit(f"MACHINE CHECK FAILED: {check}")
    if a.machine_check_only:
        log("machine check passed; stopping (--machine-check-only).")
        return

    flywire_manifest_sha = manifest_sha256()

    arm_results = {}
    for arm in ARMS:
        log(f"=== arm {arm} ===")
        bank, bank_manifest = load_bank_for_arm(arm)
        restrict_to_30_grid()
        H.REAL = bank
        manifest_sha = flywire_manifest_sha if arm == "flywire30" else None
        arm_results[arm] = run_arm(arm, bank, bank_manifest, manifest_sha, out, a.workers, log)

    for arm, res in arm_results.items():
        if res["stopped"]:
            summary = {"machine_check": check, "arm": arm, "diagnostics": res["diagnostics"],
                       "stopped": True, "stop_reason": res["stop_reason"],
                       "registration": REGISTRATION, "git_head": git_head()}
            (out / arm / "summary.json").write_text(json.dumps(summary, indent=2))
            log(f"DEGENERATE BANK, arm {arm}: {res['stop_reason']}.")

    if any(res["stopped"] for res in arm_results.values()):
        overview = {"machine_check": check, "arms": arm_results, "registration": REGISTRATION,
                    "git_head": git_head(), "runtime_s": time.time() - t0}
        (out / "summary.json").write_text(json.dumps(overview, indent=2, default=str))
        sys.exit("At least one arm was degenerate; see summary.json per arm. "
                 "No joint reading is computed when either arm did not run.")

    fw_headline = arm_results["flywire30"]["per_rank"][1]["branch"]
    fv_headline = arm_results["flyvis30"]["per_rank"][1]["branch"]
    joint = joint_reading(fw_headline, fv_headline)

    per_rank_joint = {
        rank: {
            "flywire30_branch": arm_results["flywire30"]["per_rank"][rank]["branch"],
            "flyvis30_branch": arm_results["flyvis30"]["per_rank"][rank]["branch"],
            "joint_reading": joint_reading(arm_results["flywire30"]["per_rank"][rank]["branch"],
                                           arm_results["flyvis30"]["per_rank"][rank]["branch"]),
        }
        for rank in RANKS
    }

    summary = {
        "question": "Does BF_r, r=1..4, separate the FlyWire 30-type right-optic-lobe bank from "
                     "its own 99 shuffles on existence, and does the flyvis bank restricted to "
                     "the same 30 types separate from its own 99 shuffles the same way?",
        "registration": REGISTRATION, "machine_check": check,
        "headline_r1": {"flywire30_branch": fw_headline, "flyvis30_branch": fv_headline,
                        "joint_reading": joint},
        "per_rank_joint": per_rank_joint,
        "arms": {arm: {"diagnostics": res["diagnostics"], "per_rank": res["per_rank"],
                      "bank_name": res["bank_name"]}
                for arm, res in arm_results.items()},
        "note_flyvis30_vs_full_65_bf1": (
            "flyvis30 is its own run (30 of 65 types, its own fold subset, its own shuffles), "
            "not a repeat or a subset of the full-65 BF_1 result in "
            "results/genome/c6/checks/bf1_p3/summary.json (real margin 0.028150051052145946)."),
        "matched_types": FLYWIRE_TYPES, "n_shuffles": H.N_SHUFFLES,
        "n_folds": H.N_FOLDS, "starts_k": H.STARTS,
        "flywire_bank_manifest": arm_results["flywire30"]["bank_manifest"],
        "git_head": git_head(), "harness_sha256_lf": H.sha256_lf(C6 / "harness.py"),
        "runtime_s": time.time() - t0,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    write_result_md(out, summary, arm_results)
    log(json.dumps(summary, indent=2))
    log(f"done in {time.time() - t0:.1f}s; r=1: flywire30={fw_headline}, flyvis30={fv_headline}")
    log(f"joint reading (r=1): {joint}")


if __name__ == "__main__":
    main()
