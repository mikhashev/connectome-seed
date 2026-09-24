#!/usr/bin/env python3
"""P3 of BF_1 alone, "as a rule", on the real bank and its 99 shuffles.

Registered in docs/plans/2026-09-24-bf1-p3-registration.md.
Usage: tools/.venv/Scripts/python.exe results/genome/c6/checks/bf1_p3.py [--workers N]
       tools/.venv/Scripts/python.exe results/genome/c6/checks/bf1_p3.py --real-only --out DIR
"""
import argparse
import csv
import json
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
C6 = HERE.parent
ROOT = C6.parents[1]
DEFAULT_OUT = HERE / "bf1_p3"
REGISTRATION = "docs/plans/2026-09-24-bf1-p3-registration.md"
RECORD = C6 / "rule_runs" / "second_rule_v21_r1" / "result.json"
EXPECTED_HARNESS_SHA = "6fc809527c69ee84aadebfc15c0ba755c189ddc93c80c05c0fa11d969a8d7297"
MACHINE_CHECK_TOL = 1e-9  # harness.TAU; see registration section 5

sys.path.insert(0, str(C6))
import harness as H  # noqa: E402


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
            sys.exit("REFUSED: uncommitted changes in the working tree; this run's registration "
                      f"({REGISTRATION}) and this script must both be committed first.\n" + d)
    got_sha = H.sha256_lf(C6 / "harness.py")
    if got_sha != EXPECTED_HARNESS_SHA:
        sys.exit(f"REFUSED: harness.py sha256_lf is {got_sha}, expected {EXPECTED_HARNESS_SHA} "
                 f"(the sha {REGISTRATION} was written against); this needs a new registration, "
                 f"not a silent re-run.")


def real_margin_and_check(pred, log):
    rec = json.loads(RECORD.read_text(encoding="utf-8"))
    recorded = rec["exam"]["P4"]["bf"]["margin"]
    recorded_rank = rec["exam"]["P4"]["rank"]
    recorded_k = rec["stamp"]["starts_k"]
    assert recorded_rank == 1, f"record's P4 rank is {recorded_rank}, expected 1"
    if H.STARTS != recorded_k:
        log(f"NOTE: this run's STARTS={H.STARTS} differs from the record's starts_k="
            f"{recorded_k}; the machine check is not a valid identity check in that case.")
    rule_s = H.cv(pred, H.REAL)
    n1_s = H.cv(H.N1, H.REAL)
    real_m = {f: H.margin(rule_s, n1_s, f) for f in H.FIELDS}
    diff = real_m["existence"] - recorded
    ok = abs(diff) <= MACHINE_CHECK_TOL
    check = {"recorded_P4_bf_margin": recorded, "recorded_starts_k": recorded_k,
             "this_run_existence_margin": real_m["existence"], "difference": diff,
             "tolerance": MACHINE_CHECK_TOL, "passed": bool(ok)}
    return real_m, rule_s, n1_s, check


def shuffle_margin(sd):
    # Module level so ProcessPoolExecutor can pickle it on Windows (spawn start method).
    pred = H.bf_predictor(1)
    b, inv = H.shuffled_bank(H.REAL, sd)
    assert inv["out_degrees_kept"] and inv["in_degrees_kept"], \
        f"shuffle {sd} did not preserve degree as expected"
    rs, ns = H.cv(pred, b), H.cv(H.N1, b)
    m = {f: H.margin(rs, ns, f) for f in H.FIELDS}
    per_fold = [ns[k]["existence"] - rs[k]["existence"] for k in range(H.N_FOLDS)]
    return sd, m, per_fold


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=max(1, (__import__("os").cpu_count() or 2) - 2))
    ap.add_argument("--out", default=None)
    ap.add_argument("--real-only", action="store_true")
    ap.add_argument("--allow-dirty", action="store_true")
    a = ap.parse_args()

    refuse_if_unsafe(a.allow_dirty)

    out = Path(a.out) if a.out else DEFAULT_OUT
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    log = lambda m: print(m, flush=True)

    pred = H.bf_predictor(1)
    log(f"BF_1 = {pred.name}, rank={pred.rank}, STARTS={H.STARTS}")

    real_m, rule_s_real, n1_s_real, check = real_margin_and_check(pred, log)
    log(f"machine check: {check}")
    if not check["passed"]:
        summary = {"machine_check": check, "stopped_before_shuffles": True,
                   "registration": REGISTRATION, "git_head": git_head(),
                   "harness_sha256_lf": H.sha256_lf(C6 / "harness.py"),
                   "runtime_s": time.time() - t0}
        (out / "summary.json").write_text(json.dumps(summary, indent=2))
        sys.exit("MACHINE CHECK FAILED. No shuffled-bank number was computed. "
                 f"Details: {check}\nWritten to {out / 'summary.json'}.")

    if a.real_only:
        summary = {"machine_check": check, "mode": "real_only_smoke_test",
                   "real_margin": real_m, "registration": REGISTRATION, "git_head": git_head(),
                   "harness_sha256_lf": H.sha256_lf(C6 / "harness.py"),
                   "runtime_s": time.time() - t0}
        (out / "summary.json").write_text(json.dumps(summary, indent=2))
        log(json.dumps(summary, indent=2))
        log(f"SMOKE TEST (real bank only): existence margin {real_m['existence']:.15f}, "
            f"machine check passed={check['passed']}, {time.time() - t0:.1f}s total.")
        return

    fields = list(H.FIELDS)
    rows = [{"bank": "real", "seed": None, "kind": "real",
             **{f: real_m[f] for f in fields},
             **{f"existence_fold{k}": (n1_s_real[k]["existence"] - rule_s_real[k]["existence"])
                for k in range(H.N_FOLDS)}}]
    per_field_margin = {f: {"real": real_m[f]} for f in fields}

    log(f"fitting BF_1 on {H.N_SHUFFLES} shuffled banks, workers={a.workers} ...")
    if a.workers <= 1:
        results = [shuffle_margin(sd) for sd in range(H.N_SHUFFLES)]
    else:
        with ProcessPoolExecutor(max_workers=a.workers) as ex:
            results = list(ex.map(shuffle_margin, range(H.N_SHUFFLES)))
    for sd, m, per_fold in sorted(results, key=lambda x: x[0]):
        row = {"bank": f"shuffle{sd}", "seed": sd, "kind": "shuffle", **m}
        for k in range(H.N_FOLDS):
            row[f"existence_fold{k}"] = per_fold[k]
        rows.append(row)
        for f in fields:
            per_field_margin[f][f"shuffle{sd}"] = m[f]

    fieldnames = ["bank", "seed", "kind"] + fields + [f"existence_fold{k}" for k in range(H.N_FOLDS)]
    with open(out / "per_shuffle.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    summary_fields = {}
    for f in fields:
        real_v = per_field_margin[f]["real"]
        sh_v = [per_field_margin[f][f"shuffle{sd}"] for sd in range(H.N_SHUFFLES)]
        n_ge = sum(1 for v in sh_v if v >= real_v)
        p = (1 + n_ge) / (1 + H.N_SHUFFLES)
        strictly_above_all = all(real_v - v > H.TAU for v in sh_v)
        summary_fields[f] = {
            "real_margin": real_v, "shuffled_min": float(min(sh_v)),
            "shuffled_mean": float(sum(sh_v) / len(sh_v)), "shuffled_max": float(max(sh_v)),
            "n_shuffled_ge_real": n_ge, "strictly_above_all": bool(strictly_above_all),
            "p_one_sided": p,
        }

    ex = summary_fields["existence"]
    gap = ex["real_margin"] - ex["shuffled_max"]
    if ex["strictly_above_all"] and ex["n_shuffled_ge_real"] == 0:
        branch = "A: BF_1 separates"
    elif ex["p_one_sided"] >= 0.05:
        branch = "B: BF_1 does not separate"
    else:
        branch = "C: in between"

    summary = {
        "question": "Does the trained rank-1 bilinear term BF_1, alone, separate the real bank "
                     "from its 99 shuffles on existence? Offset/counts/sign carry no reading "
                     "(0 by construction; registration section 3).",
        "registration": REGISTRATION, "decision_field": "existence",
        "machine_check": check, "branch": branch,
        "gap_real_minus_shuffled_max_existence": gap,
        "fields": summary_fields, "n_shuffles": H.N_SHUFFLES, "n_folds": H.N_FOLDS,
        "starts_k": H.STARTS, "rank": pred.rank, "predictor_name": pred.name,
        "git_head": git_head(), "harness_sha256_lf": H.sha256_lf(C6 / "harness.py"),
        "folds_sha256_lf": H.sha256_lf(C6 / "folds.csv"),
        "runtime_s": time.time() - t0,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    log(json.dumps(summary, indent=2))

    md = [
        "# BF_1 alone: P3 against the 99 shuffled banks",
        "",
        f"Registration: `{REGISTRATION}`. Machine check: {check['passed']} "
        f"(this run {check['this_run_existence_margin']:.15f} vs recorded "
        f"{check['recorded_P4_bf_margin']:.15f}, difference {check['difference']:.2e}).",
        "",
        "## Existence (the decision field)",
        "",
        "| real margin | shuffled mean | shuffled max | n shuffled >= real | p (one-sided) | "
        "gap (real - shuffled max) | branch |",
        "|---|---|---|---|---|---|---|",
        f"| {ex['real_margin']:+.5f} | {ex['shuffled_mean']:+.5f} | {ex['shuffled_max']:+.5f} | "
        f"{ex['n_shuffled_ge_real']} | {ex['p_one_sided']:.2f} | {gap:+.5f} | **{branch}** |",
        "",
        "## Other fields (reported, no reading -- 0 by construction, registration section 3)",
        "",
        "| field | real margin | shuffled mean | shuffled max | n shuffled >= real | p |",
        "|---|---|---|---|---|---|",
    ]
    for f in ("offset", "counts", "sign"):
        s = summary_fields[f]
        md.append(f"| {f} | {s['real_margin']:+.5f} | {s['shuffled_mean']:+.5f} | "
                  f"{s['shuffled_max']:+.5f} | {s['n_shuffled_ge_real']} | "
                  f"{s['p_one_sided']:.2f} |")
    md += ["", f"n_shuffles={H.N_SHUFFLES}, n_folds={H.N_FOLDS}, starts_k={H.STARTS}, "
           f"git_head={summary['git_head']}, runtime={summary['runtime_s']:.1f}s.", ""]
    (out / "RESULT.md").write_text("\n".join(md), encoding="utf-8", newline="\n")
    log(f"done in {time.time() - t0:.1f}s; branch: {branch}")


if __name__ == "__main__":
    main()
