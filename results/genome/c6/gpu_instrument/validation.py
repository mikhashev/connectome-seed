"""The validation runner for V0-V8 of the GPU instrument registration (tools/.venv).

docs/plans/2026-09-26-gpu-instrument-registration.md, revision 1.4 (e2fab47), section 7; Ark's
review of revision 1.3 (chat 12:09 UTC), point 3 (V6 draws its fits from the BF-active subset;
"uninformative" is a recorded outcome in the table), is part of revision 1.4.

Each command launches the registered GPU stage (run_registered.py, in the torch venv,
instrument.TORCH_PY) and/or the CPU side (this venv), and codes each run's outcome as section 7
writes it. Private run folders go to connectome-seed-data/gpu_instrument/ (an index of them in
validation_index.json there); each run's committed aggregate goes to
results/genome/c6/gpu_instrument/validation/<run>.json, and the table of outcomes to
validation/table.json (printed after every run).

Order (section 7): V0; V6 and V7; V1; V2; V3; V5; V4. V8 per lobe when that lobe's male CPU
pre-run store exists (refuses cleanly, exit 2, until then).

  python validation.py V0 [--allow-dirty]   one world (R:0 base + 99 shuffles), settings on, and
                                           the same composition with them off; hashes compared,
                                           overhead recorded
  python validation.py V1                  three full runs of the registered composition (resumes)
  python validation.py V2                  V1's first run against A's pinned store (E1, E2)
  python validation.py V3                  A's script on a hybrid store (E1 on the CSV, E3, D9 (b))
  python validation.py V4 [--parts a,b,c,d]
  python validation.py V5 [--parts a,b]
  python validation.py V6                  BF_TOL = 1e-5 on the BF-active banks; comparator vs recount
  python validation.py V7                  the poisoned block, against V0's settings-on run
  python validation.py V8 --lobe L|R [--male-store <folder or raw_fits.json.gz>]
                          [--male-store-sha256 <hex>] [--inputs-only]
                                           the male worlds of one lobe (45 worlds, base + 99
                                           shuffles, BF_1..BF_4 ko) against that lobe's male CPU
                                           pre-run store (default instrument.MALE_PRERUN_STORES);
                                           --inputs-only verifies the inputs and prints the
                                           BF-active classification, without the GPU stage
"""
import argparse
import csv
import io
import json
import os
import pathlib
import re
import subprocess
import sys
import time

# One BLAS thread before numpy loads, as A's script, the male script and the prep workers set it:
# the CPU fits made in this process (V3's D9 (b) refits, V8's degree terms through the adapter)
# depend on the BLAS thread count in their last bits (measured: the male lobe L degree terms under
# 24 OpenBLAS threads differ from those under 1, and so would the worlds built on them).
THREAD_VARS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")
THREAD_ENV_FOUND = {_v: os.environ.get(_v) for _v in THREAD_VARS}
for _v in THREAD_VARS:
    os.environ.setdefault(_v, "1")

import numpy as np  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import instrument as I  # noqa: E402
import census as C  # noqa: E402
import gpu_equivalence as G  # noqa: E402
import recount as RC  # noqa: E402
import knockout_regrow as K  # noqa: E402  (read-only)

INDEX = I.DATA_ROOT / "validation_index.json"
TABLE = I.VALIDATION_DIR / "table.json"
M3_FIVE = ("world:M1.0:0||ko||BF:1", "world:M1.0:4||ko||BF:1", "world:M0.75:0||ko||BF:1",
           "world:M0.85:0||ko||BF:1", "world:M0.85:2||ko||BF:1")
FLAGS_OFF_V3_ONE_WORLD = HERE / "validation_pipeline_one_world_R0.json"
MALE_SCRIPT = I.C6 / "checks" / "knockout_regrow_male_cns.py"


def log(m=""):
    print(m, flush=True)


# ------------------------------------------------------------------------------------------
# Bookkeeping.

def load_index():
    if INDEX.is_file():
        return json.loads(INDEX.read_text(encoding="utf-8"))
    return {}


def add_index(label, run_dir):
    idx = load_index()
    idx.setdefault(label, []).append(str(run_dir))
    I.DATA_ROOT.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(json.dumps(idx, indent=1), encoding="utf-8", newline="\n")


def runs_at_head(tag, allow_dirty=False):
    """The indexed runs of `tag` made at the current head (and, unless allow_dirty, from a
    clean tree), oldest first: a run of another head is never reused."""
    head = I.git_head()
    out = []
    for r in load_index().get(tag) or []:
        m = pathlib.Path(r) / "manifest.json"
        if not m.is_file():
            continue
        man = json.loads(m.read_text(encoding="utf-8"))
        if man.get("git_head") == head and (allow_dirty or not man.get("not_from_a_committed_head")):
            out.append(r)
    return out


def last_run(label, allow_dirty=False):
    runs = runs_at_head(label, allow_dirty)
    return pathlib.Path(runs[-1]) if runs else None


def record(run, outcome, text, details):
    """The committed aggregate of one validation run, and its row of the table."""
    I.VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    head = I.git_head()
    dirty = I.tree_dirty_paths(exclude_validation=True)
    row = {"run": run, "outcome": outcome, "text": text, "head": head,
           "not_from_a_committed_head": bool(dirty),
           "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "registration": f"{I.REGISTRATION} revision {I.REGISTRATION_REVISION} "
                           f"({I.REGISTRATION_COMMIT}; {I.REGISTRATION_NOTE})",
           "applied_ahead": I.APPLIED_AHEAD}
    I.write_json(I.VALIDATION_DIR / f"{run}.json", {**row, "details": details})
    table = json.loads(TABLE.read_text(encoding="utf-8")) if TABLE.is_file() else {}
    table[run] = row
    I.write_json(TABLE, table)
    log("")
    log("validation table (section 7):")
    for k in sorted(table):
        log(f"  {k:4s} {table[k]['outcome']:<40s} {table[k]['utc']}  head {table[k]['head'][:12]}"
            + ("  (NOT FROM A COMMITTED HEAD)" if table[k].get("not_from_a_committed_head") else ""))
    log(f"{run}: {outcome}: {text}")


def run_gpu(label, extra, env_extra=None, tag=None, allow_dirty=False):
    """Launch the registered GPU stage; returns (returncode, run_dir or None, output)."""
    args = [str(I.TORCH_PY), str(HERE / "run_registered.py"), "--kind", "validation",
            "--label", label, "--tag", tag or label] + list(extra)
    if I.REGISTERED_STAMP is None:
        args.append("--stamp-unregistered")
    if allow_dirty:
        args.append("--allow-dirty")
    env = dict(os.environ)
    for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS",
              "CUBLAS_WORKSPACE_CONFIG", "GPU_INSTRUMENT_FLAGS_OFF", "GPU_INSTRUMENT_DEVICE"):
        env.pop(v, None)
    env.update(env_extra or {})
    log(f"$ {' '.join(args)}" + (f"   [env {env_extra}]" if env_extra else ""))
    t0 = time.time()
    p = subprocess.Popen(args, cwd=HERE, env=env, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True)
    out = []
    for line in p.stdout:
        out.append(line)
        print(line, end="", flush=True)
    rc = p.wait()
    text = "".join(out)
    m = re.search(r"^RUN_DIR=(.+)$", text, re.M)
    run_dir = pathlib.Path(m.group(1).strip()) if m else None
    log(f"[{label}] exit {rc} in {time.time() - t0:.0f}s; run dir {run_dir}")
    if run_dir is not None and rc == 0:
        add_index(tag or label, run_dir)
    return rc, run_dir, text


def hashes_of(run_dir):
    return json.loads((pathlib.Path(run_dir) / "fit_hashes.json").read_text(encoding="utf-8"))


def manifest_of(run_dir):
    return json.loads((pathlib.Path(run_dir) / "manifest.json").read_text(encoding="utf-8"))


def compare_hashes(a, b, keys=None):
    """Per fit, the four hashes (U, V, lambda, p) of two runs; over the common keys or `keys`."""
    ks = sorted(set(a) & set(b)) if keys is None else list(keys)
    diff = [k for k in ks if a[k] != b[k]]
    by_field = {f: sum(1 for k in ks if a[k][f] != b[k][f]) for f in ("U", "V", "lambda", "p")}
    return {"compared": len(ks), "differ": len(diff), "differing": diff[:200],
            "differing_by_field": by_field}


def a45_args():
    return ["--worlds", "all", "--n-sh", "99", "--base"]


def r0_args():
    return ["--worlds", "R:0", "--n-sh", "99", "--base"]


# ------------------------------------------------------------------------------------------
# V0.

def v0(a):
    rc_on, run_on, out_on = run_gpu("V0", r0_args(), tag="V0_on", allow_dirty=a.allow_dirty)
    # D6 (a): a RuntimeError from a non-deterministic operation (torch names the operation and
    # "use_deterministic_algorithms" in its message), or a settings refusal of gpu_env (R2).
    raised = rc_on != 0 and ("use_deterministic_algorithms" in out_on
                             or "REFUSED (R2)" in out_on or "REFUSED (G1" in out_on)
    details = {"run_on": str(run_on), "rc_on": rc_on}
    if rc_on != 0 or run_on is None:
        outcome = ("REFUSED: D6 (a) cannot be met" if raised else "ERROR (not a settings error)")
        record("V0", outcome, "the settings-on run did not complete; see the log", details)
        return
    rc_off, run_off, out_off = run_gpu("V0-off", r0_args(), tag="V0_off",
                                       env_extra={"GPU_INSTRUMENT_FLAGS_OFF": "1"},
                                       allow_dirty=a.allow_dirty)
    m_on = manifest_of(run_on)
    details.update(run_off=str(run_off), rc_off=rc_off,
                   settings=m_on["determinism_settings"], stamp=m_on["stamp"],
                   stamp_check=m_on["stamp_check"]["status"], composition=m_on["composition"],
                   secs_on=m_on["secs"], near_ties_on=m_on["near_ties_by_rank"],
                   vram_on=m_on["vram"])
    if rc_off == 0 and run_off is not None:
        m_off = manifest_of(run_off)
        details["secs_off"] = m_off["secs"]
        details["hashes_on_vs_off"] = compare_hashes(hashes_of(run_on), hashes_of(run_off))
        details["overhead_gpu_total"] = m_on["secs"]["gpu_total"] / m_off["secs"]["gpu_total"]
        details["overhead_end_to_end"] = (m_on["secs"]["end_to_end_wall"]
                                          / m_off["secs"]["end_to_end_wall"])
    if FLAGS_OFF_V3_ONE_WORLD.is_file():
        s = json.loads(FLAGS_OFF_V3_ONE_WORLD.read_text(encoding="utf-8"))["summary"]
        banks = s["banks"]
        details["flags_off_v3_earlier_run"] = {
            "file": FLAGS_OFF_V3_ONE_WORLD.name, "banks": banks, "secs": s["secs"],
            "gpu_secs_per_bank": s["secs"]["gpu_total"] / banks}
        details["gpu_secs_per_bank_on"] = m_on["secs"]["gpu_total"] / len(m_on["keys"])
    rep = G.compare_run(run_on)
    details["against_pinned"] = {k: rep[k] for k in ("outcome", "outcome_text", "n_fits",
                                                     "n_not_bit_equal", "n_flipped_pairs")}
    details["against_pinned"]["e1_failures"] = len(rep["e1_failures"])
    text = (f"R1-R4 passed with the settings on (stamp: {m_on['stamp_check']['status']}); "
            f"no RuntimeError from deterministic mode; "
            f"hashes on vs off: {details.get('hashes_on_vs_off', {}).get('differ')} of "
            f"{details.get('hashes_on_vs_off', {}).get('compared')} fits differ; "
            f"GPU {m_on['secs']['gpu_total']:.1f}s on vs "
            f"{details.get('secs_off', {}).get('gpu_total', float('nan')):.1f}s off; against "
            f"the pinned store: {rep['n_fits'] - rep['n_not_bit_equal']} / {rep['n_fits']} "
            f"bit-equal, outcome {rep['outcome']}")
    record("V0", "PASS", text, details)


# ------------------------------------------------------------------------------------------
# V1, V2.

def v1(a):
    runs = runs_at_head("V1_run", a.allow_dirty)
    while len(runs) < 3:
        n = len(runs) + 1
        rc, run_dir, _ = run_gpu("V1", a45_args(), tag="V1_run", allow_dirty=a.allow_dirty)
        if rc != 0 or run_dir is None:
            record("V1", "ERROR", f"run {n} did not complete", {"runs": runs})
            return
        runs = runs_at_head("V1_run", a.allow_dirty)
    runs = runs[:3]
    hs = [hashes_of(r) for r in runs]
    c12, c13 = compare_hashes(hs[0], hs[1]), compare_hashes(hs[0], hs[2])
    m1 = manifest_of(runs[0])
    ref, _ = G.load_reference()
    got = I.read_store(pathlib.Path(runs[0]) / "raw_fits_gpu.json.gz")
    base_diff = sorted(rk for rk in got if I.is_base_view(I.split_record_key(rk)[0])
                       and not np.array_equal(np.asarray(got[rk]["p"]), np.asarray(ref[rk]["p"])))
    digests = {manifest_of(r)["composition"]["refusal_digest"] for r in runs}
    stamps = [manifest_of(r)["stamp"] for r in runs]
    details = {"runs": runs, "run1_vs_run2": c12, "run1_vs_run3": c13,
               "fits_per_run": len(hs[0]),
               "base_fits_differing_from_cpu_under_D6": base_diff,
               "flag_free_set_M3": list(M3_FIVE),
               "same_as_M3": sorted(base_diff) == sorted(M3_FIVE),
               "stamp_measured": stamps[0], "stamps_equal_across_runs":
                   all(s == stamps[0] for s in stamps),
               "stamp_to_register_in_instrument_REGISTERED_STAMP": stamps[0],
               "composition_digests": sorted(digests),
               "near_ties_by_run": [manifest_of(r)["near_ties_by_rank"] for r in runs],
               "secs_by_run": [manifest_of(r)["secs"] for r in runs]}
    if c12["differ"] == 0 and c13["differ"] == 0 and len(digests) == 1:
        outcome, text = "PASS", (f"all {len(hs[0])} x 3 per-fit hashes equal; base fits differing "
                                 f"from the CPU under D6: {len(base_diff)} "
                                 f"({'the same as' if details['same_as_M3'] else 'not'} M3's "
                                 f"five); stamp measured (register it: D7)")
    else:
        outcome, text = "NOT DETERMINISTIC", (f"hashes differ: run1 vs run2 {c12['differ']}, "
                                              f"run1 vs run3 {c13['differ']}")
    log(f"stamp measured in V1 (to become the registered stamp of D7):\n"
        f"{json.dumps(stamps[0], indent=1, sort_keys=True)}")
    log(f"composition refusal digest of the registered composition: {sorted(digests)}")
    record("V1", outcome, text, details)


def v1_first_run(allow_dirty=False):
    runs = runs_at_head("V1_run", allow_dirty)
    if not runs:
        raise SystemExit("V1 has not run at this head: no V1_run of this head in the index")
    return pathlib.Path(runs[0])


def v2(a):
    run = v1_first_run(a.allow_dirty)
    rep = G.compare_run(run)
    G.print_report(rep)
    out = rep_path = I.DATA_ROOT / f"V2_report_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.json"
    I.write_json(rep_path, rep)
    groups = rep["not_bit_equal_by_M18_group"]
    den = {g: v["denominator"] for g, v in groups.items()}
    details = {k: v for k, v in rep.items() if k not in ("per_fit",)}
    details["full_report"] = str(out)
    details["denominators_M18"] = den
    code = {1: "PASS (outcome 1)", 2: "REFUSED (outcome 2)", 3: "REFUSED (outcome 3)"}
    record("V2", code[rep["outcome"]], rep["outcome_text"], details)


# ------------------------------------------------------------------------------------------
# V3.

def _read_csv(path):
    rows = list(csv.DictReader(io.StringIO(pathlib.Path(path).read_bytes().decode("utf-8"),
                                           newline="")))
    return {tuple(r[c] for c in K.CSV_KEY_COLUMNS): r for r in rows}


def _run_a(from_raw, out):
    args = [str(I.CPU_PY), str(I.C6 / "checks" / "knockout_regrow.py"), "--synthetic-only",
            "--starts", "10", "--workers", "30", "--from-raw", str(from_raw), "--out", str(out)]
    log(f"$ {' '.join(args)}")
    p = subprocess.run(args, cwd=I.ROOT, capture_output=True, text=True)
    (pathlib.Path(out).parent / (pathlib.Path(out).name + ".log")).write_text(
        p.stdout + p.stderr, encoding="utf-8")
    return p.returncode, p.stdout + p.stderr


def v3(a):
    run = v1_first_run(a.allow_dirty)
    d = I.DATA_ROOT / f"V3_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}_{I.git_head()[:12]}"
    import hybrid_store
    import hybrid_arm
    ref, info = G.load_reference()
    prov = hybrid_store.build_hybrid(run, d / "hybrid", ref, info)
    log(f"hybrid store: {prov}")
    rc_ref, out_ref = _run_a(pathlib.Path(K.PRERUN_DIR) / "raw_fits.json.gz", d / "ref_pass")
    rc_hyb, out_hyb = _run_a(d / "hybrid" / "raw_fits.json.gz", d / "hybrid_pass")
    details = {"gpu_run": str(run), "folder": str(d), "hybrid": prov,
               "a_rc_reference_pass": rc_ref, "a_rc_hybrid_pass": rc_hyb}
    hyb = I.read_store(d / "hybrid" / "raw_fits.json.gz")
    # D9 (b): the path check for GPU-made BF records, CPU refits in this process.
    terms = K.degree_terms()
    K._w_init(10, terms, True)
    Ft = {tuple(k.split("||")): v for k, v in hyb.items()}
    base_keys = [f"world:{w['family']}:{w['j']}" for w in K.world_specs()]

    def refit(bk, pk):
        return dict(K._w_group([(bk, "ko1", pk)]))[(bk, "ko1", pk)]
    pc = hybrid_arm.fixed_lambda_path_check_hybrid(Ft, base_keys, refit)
    details["path_check_D9b"] = pc
    a_exact_failed = "FIXED-LAMBDA PATH DIFFERS" in out_hyb
    details["a_exact_path_check_failed"] = a_exact_failed
    csv_h, csv_r = d / "hybrid_pass" / "synthetic_worlds.csv", d / "ref_pass" / "synthetic_worlds.csv"
    if not (csv_h.is_file() and csv_r.is_file()):
        record("V3", "NOT DECIDED", "A's script wrote no synthetic_worlds.csv on one pass"
               + (" (A's exact fixed-lambda path check, D9 (a), stopped it; D9 (b) "
                  f"{'passed' if pc.get('passed') else 'did not pass'})" if a_exact_failed
                  else ""), details)
        return
    H_rows, R_rows = _read_csv(csv_h), _read_csv(csv_r)
    P_rows = _read_csv(pathlib.Path(K.PRERUN_DIR) / "synthetic_worlds.csv")
    exact_bad, e3_bad, e3_rows = [], [], []
    for key in sorted(set(H_rows) | set(R_rows) | set(P_rows)):
        h, r, pn = H_rows.get(key), R_rows.get(key), P_rows.get(key)
        if h is None or r is None or pn is None:
            exact_bad.append({"row": key, "missing_in": [n for n, x in (("hybrid", h), ("ref", r),
                                                                          ("pinned", pn)) if x is None]})
            continue
        for col in K.CSV_EXACT_COLUMNS:
            for other, name in ((pn, "pinned"), (r, "reference pass")):
                if not K._cells_equal(h[col], other[col]):
                    exact_bad.append({"row": key, "column": col, "hybrid": h[col],
                                      "against": name, "value": other[col]})
        if h["mechanism_description"] != r["mechanism_description"]:
            exact_bad.append({"row": key, "column": "mechanism_description",
                              "hybrid": h["mechanism_description"],
                              "against": "reference pass",
                              "value": r["mechanism_description"]})
        # E3 on the continuous columns, against the reference pass.
        fam, j, _, pred = key
        bk = f"world:{fam}:{j}"
        pk = {"rule #2.1": "rule", "N1": "N1"}.get(pred, pred.replace("BF_", "BF:"))
        rk = f"{bk}||ko||{pk}"
        pr = np.asarray(ref[rk]["p"], np.float64)
        pg = np.asarray(hyb[rk]["p"], np.float64)
        bit = bool(np.array_equal(pr, pg))
        bounds = None if bit else G.e3_bounds(pr, ref[rk]["y"], float(np.max(np.abs(pg - pr))))
        f = lambda s: None if s in ("", None) else float(s)   # noqa: E731
        chk = G.e3_check(bounds, f(r["D"]), f(h["D"]), f(r["logloss"]), f(h["logloss"]),
                         dp=None if bit else np.abs(pg - pr))
        mr, mh = f(r["logloss_margin_over_N1"]), f(h["logloss_margin_over_N1"])
        m_ok = (mr == mh) if bit else abs(mh - mr) <= bounds["logloss_bound"]
        rs_ok = all(K._cells_equal(h[c], r[c]) for c in ("regrown_share_full",
                                                          "regrown_share_block"))
        ok = chk["passed"] and m_ok and rs_ok
        e3_rows.append({"row": key, "bit_equal": bit, "bounds": bounds, "check": chk,
                        "margin_ok": m_ok, "regrown_share_exact": rs_ok, "passed": ok})
        if not ok:
            e3_bad.append(e3_rows[-1])
    syn_h = json.loads((d / "hybrid_pass" / "synthetic_only.json").read_text(encoding="utf-8"))
    syn_r = json.loads((d / "ref_pass" / "synthetic_only.json").read_text(encoding="utf-8"))
    vl_bad = [w["family"] + ":" + str(w["j"]) for w, v in zip(syn_h["worlds"], syn_r["worlds"])
              if (w["verdict_line"], w["label"]) != (v["verdict_line"], v["label"])]
    ko1 = syn_h["fits"]["ko1_count"]["counted"]
    ko1_ok = (ko1["copied_from_ko"], ko1["fitted"]) == (47, 178)
    details.update(exact_differences=exact_bad, verdict_or_label_differs=vl_bad, ko1_count=ko1,
                   ko1_equal_47_178=ko1_ok, e3_failures=e3_bad,
                   e3_rows_not_bit_equal=[x for x in e3_rows if not x["bit_equal"]],
                   a_prediction_outcome_3b=syn_h["two_world_check"].get("prerun_reproduction",
                                                                        {}).get("outcome"))
    if exact_bad or vl_bad or not ko1_ok:
        outcome, text = "REFUSED: an exact column or a string differs", (
            f"{len(exact_bad)} exact-column/mechanism differences, {len(vl_bad)} verdict or label "
            f"differences, ko1 count {ko1}")
    elif e3_bad:
        outcome, text = "REFUSED: E3 exceeded", f"{len(e3_bad)} rows beyond their E3 bounds"
    elif not pc.get("passed"):
        outcome, text = "REFUSED: the path check fails under D9 (b)", json.dumps(pc)[:500]
    else:
        outcome, text = "PASS", (f"E1 (exact columns, mechanism, verdict lines and labels, ko1 "
                                 f"47/178), E3 on {len(details['e3_rows_not_bit_equal'])} "
                                 f"differing rows, and the D9 (b) path check "
                                 f"({pc.get('bank')}) hold")
    record("V3", outcome, text, details)


# ------------------------------------------------------------------------------------------
# V4.

def v4(a):
    parts = a.parts.split(",") if a.parts else ["a", "b", "c", "d"]
    v1r = v1_first_run(a.allow_dirty)
    h1 = hashes_of(v1r)
    details, flags = {}, []
    todo = []
    if "a" in parts:
        todo.append(("V4a", ["--worlds", "all", "--base-only"], "V4a"))
    if "b" in parts:
        for w in ("M1.0:0", "M0.85:2", "M0.75:0"):
            todo.append(("V4b", ["--keys", f"world:{w}"], f"V4b_{w.replace(':', '-')}"))
    if "c" in parts:
        todo.append(("V4c", a45_args() + ["--row-chunk", "100000"], "V4c"))
    if "d" in parts:
        todo.append(("V4d", ["--worlds", "all", "--base-only", "--ranks", "1,4"], "V4d"))
    for label, args, tag in todo:
        rc, run, out = run_gpu(label, args, tag=tag, allow_dirty=a.allow_dirty)
        if rc != 0 or run is None:
            details[tag] = {"rc": rc, "error": "did not complete"}
            continue
        hc = compare_hashes(hashes_of(run), h1, keys=sorted(hashes_of(run)))
        rep = G.compare_run(run)
        details[tag] = {"run": str(run), "hashes_vs_V1_run1": hc,
                        "E": {k: rep[k] for k in ("outcome", "outcome_text", "n_not_bit_equal",
                                                  "n_flipped_pairs")},
                        "differing_fits": [x["key"] for x in rep["differing_fits"]]}
        if rep["outcome"] == 3:
            flags.append(f"E1 FAILS under composition {tag}: reported; D5 (a) is then the only "
                         "safe option")
        if tag == "V4c" and hc["differ"]:
            flags.append("(c) MOVED A HASH: row_chunk returns to the refusal digest (D5)")
        if tag == "V4d":
            m = manifest_of(run)
            hdr = {"stamp": m["stamp"], "det": m["determinism_settings"]
                   ["use_deterministic_algorithms"], "script": "run_registered.py / gpu_stage.py",
                   "script_sha256_lf": {k: v for k, v in m["file_sha256_lf"].items()
                                        if k.endswith(("gpu_stage.py", "run_registered.py",
                                                       "gpu_bf3.py"))},
                   "row_chunk": m["composition"]["recorded_not_refused"]["row_chunk"]}
            hs = hashes_of(run)
            probe = {f"{w}||BF:{r}": {f: hs[f"world:{w}||ko||BF:{r}"][f]
                                      for f in ("U", "V", "lambda")}
                     for w in ("M1.0:0", "M0.85:2", "M0.75:0") for r in (1, 4)}
            details[tag]["header"] = hdr
            details[tag]["probe_hashes"] = probe
            log(f"V4 (d) header: {json.dumps(hdr, sort_keys=True)}")
            for k, v in probe.items():
                log(f"  {k}: {v}")
    text = ("; ".join(f"{t}: {d.get('hashes_vs_V1_run1', {}).get('differ')} of "
                      f"{d.get('hashes_vs_V1_run1', {}).get('compared')} hashes differ from V1, "
                      f"E outcome {d.get('E', {}).get('outcome')}" for t, d in details.items())
            + ("; " + "; ".join(flags) if flags else ""))
    record("V4", "STATEMENT" + (" WITH FLAGS" if flags else ""), text,
           {"parts": details, "flags": flags})


# ------------------------------------------------------------------------------------------
# V5.

def v5(a):
    parts = a.parts.split(",") if a.parts else ["a", "b"]
    details = {}
    d = I.DATA_ROOT / f"V5_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}_{I.git_head()[:12]}"
    if "a" in parts:
        env = dict(os.environ)
        env["OPENBLAS_NUM_THREADS"] = "4"
        for v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
            env.pop(v, None)
        args = [str(I.CPU_PY), str(HERE / "v5a_cpu_blas4.py"), "--out", str(d / "a")]
        log(f"$ OPENBLAS_NUM_THREADS=4 {' '.join(args)}")
        p = subprocess.run(args, cwd=HERE, env=env, capture_output=True, text=True)
        log(p.stdout[-3000:] + p.stderr[-3000:])
        if p.returncode == 0:
            ra = json.loads((d / "a" / "v5a.json").read_text(encoding="utf-8"))
            moved = ra["moved"]
            small = [k for k in moved if k.endswith("BF:1") and I.is_base_view(k.split("||")[0])
                     and next(r["lam_ref"] for r in ra["rows"] if r["key"] == k) in (1, 1.0, 3,
                                                                                      3.0)]
            details["a"] = {"moved": moved, "n_moved": len(moved),
                            "moved_in_M3_five": sorted(set(moved) & set(M3_FIVE)),
                            "moved_rank1_small_lambda": small,
                            "rest_bit_equal_share": (ra["fits"] - len(moved)) / ra["fits"]}
        else:
            details["a"] = {"error": p.returncode}
    if "b" in parts:
        v1r = v1_first_run(a.allow_dirty)
        ref, _ = G.load_reference()
        g1 = I.read_store(v1r / "raw_fits_gpu.json.gz")
        controls = []
        for w in K.world_specs():
            rk = f"world:{w['family']}:{w['j']}||ko||BF:1"
            if rk in M3_FIVE or float(ref[rk]["lam"]) not in (1.0, 3.0):
                continue
            if np.array_equal(np.asarray(g1[rk]["p"]), np.asarray(ref[rk]["p"])):
                controls.append(rk)
            if len(controls) == 5:
                break
        keys = [rk.split("||")[0] for rk in list(M3_FIVE) + controls]
        rc, run, _ = run_gpu("V5b", ["--keys", ",".join(keys), "--ranks", "1"], tag="V5b",
                             env_extra={"GPU_INSTRUMENT_DEVICE": "cpu"},
                             allow_dirty=a.allow_dirty)
        if rc == 0 and run is not None:
            gb = I.read_store(run / "raw_fits_gpu.json.gz")
            per = {}
            for rk in list(M3_FIVE) + controls:
                pc = np.asarray(gb[rk]["p"])
                per[rk] = {"equals_cpu_harness": bool(np.array_equal(pc, np.asarray(ref[rk]["p"]))),
                           "equals_V1_gpu": bool(np.array_equal(pc, np.asarray(g1[rk]["p"]))),
                           "control": rk in controls}
            details["b"] = {"run": str(run), "per_fit": per,
                            "M3_five_differ_from_cpu_harness":
                                sum(not per[k]["equals_cpu_harness"] for k in M3_FIVE),
                            "M3_five_equal_to_V1_gpu": sum(per[k]["equals_V1_gpu"] for k in M3_FIVE)}
        else:
            details["b"] = {"error": rc}
    A, B = details.get("a", {}), details.get("b", {})
    if "moved" in A and "per_fit" in B:
        a_none = not A["moved_in_M3_five"]
        b_repro = B["M3_five_differ_from_cpu_harness"] == 5
        if a_none and b_repro:
            outcome, text = "REFUSED: the differences come from the GPU code", (
                "(a) moved none of M3's five and (b) reproduced all five on the torch CPU device")
        elif (A["moved_in_M3_five"] and len(A["moved_rank1_small_lambda"]) * 2 > A["n_moved"]
              and A["rest_bit_equal_share"] > 0.5):
            outcome, text = "EXPLAINED", (
                f"(a) moved {A['n_moved']} fits, {len(A['moved_in_M3_five'])} of M3's five, "
                f"{len(A['moved_rank1_small_lambda'])} rank-1 small-lambda base fits; "
                f"{A['rest_bit_equal_share']:.3f} of the fits stay bit-equal")
        else:
            outcome, text = "STATEMENT (neither refused nor explained)", json.dumps(
                {"a": {k: A[k] for k in ("n_moved", "moved_in_M3_five")},
                 "b": {k: B[k] for k in ("M3_five_differ_from_cpu_harness",
                                         "M3_five_equal_to_V1_gpu")}})
    else:
        outcome, text = "INCOMPLETE", "a part did not complete"
    record("V5", outcome, text, details)


# ------------------------------------------------------------------------------------------
# V6, V7.

def v6(a):
    ref, info = G.load_reference()
    order = ([f"world:{w['family']}:{w['j']}|sh:{sd}" for w in K.world_specs()
              for sd in range(99)] + [f"world:{w['family']}:{w['j']}" for w in K.world_specs()])
    planned = [I.bf_record_key(k, r) for r in (1, 2, 3, 4) for k in order]
    act = G.bf_active(ref, planned)
    banks = [k for k in order if any(act[I.bf_record_key(k, r)] for r in (1, 2, 3, 4))]
    d = I.DATA_ROOT / "V6_keys"
    d.mkdir(parents=True, exist_ok=True)
    kf = d / f"V6_keys_{I.git_head()[:12]}.txt"
    kf.write_text("\n".join(banks) + "\n", encoding="utf-8", newline="\n")
    log(f"V6: {len(banks)} banks carry the {sum(bool(v) for v in act.values())} BF-active fits")
    rc, run, _ = run_gpu("V6", ["--keys-file", str(kf), "--bf-tol", "1e-5"], tag="V6",
                         allow_dirty=a.allow_dirty)
    if rc != 0 or run is None:
        record("V6", "ERROR", "the GPU run did not complete", {"rc": rc})
        return
    only = {rk for rk, v in act.items() if v}
    rep = G.compare_run(run, ref, info, only=only)
    G.print_report(rep)
    got = I.read_store(run / "raw_fits_gpu.json.gz")
    ok, mism = RC.agree(rep["per_fit"], got, ref)
    moved = [r for r in rep["per_fit"] if not r["bit_equal"]]
    details = {"run": str(run), "banks": len(banks), "bf_active_fits_compared": len(only),
               "comparator": {k: v for k, v in rep.items() if k != "per_fit"},
               "recount_agrees": ok, "mismatches": mism[:100],
               "bf_active_fits_not_bit_equal": len(moved)}
    if not ok:
        outcome, text = "REFUSED: comparator differs from recount", f"{len(mism)} fits differ"
    elif not moved:
        outcome, text = "UNINFORMATIVE", ("BF_TOL = 1e-5 moved no BF-active fit's p; T-G4, T-G9 "
                                          "and T-G10 remain the only tests that the comparator "
                                          "refuses")
    else:
        outcome, text = "PASS", (f"comparator equals the brute-force recount on all "
                                 f"{len(rep['per_fit'])} BF-active fits; {len(moved)} not "
                                 f"bit-equal; comparator outcome {rep['outcome']} "
                                 f"({len(rep['e1_failures'])} E1, {rep['n_flipped_pairs']} "
                                 f"flipped pairs)")
    record("V6", outcome, text, details)


def v7(a):
    base = last_run("V0_on", a.allow_dirty)
    if base is None:
        raise SystemExit("V7 needs V0's settings-on run at this head (the unpoisoned run of the "
                         "same composition); run V0 first")
    rc, run, _ = run_gpu("V7", r0_args() + ["--poison-real-block"], tag="V7",
                         allow_dirty=a.allow_dirty)
    if rc != 0 or run is None:
        record("V7", "REFUSED: a code path reads a real block cell (the run failed)",
               "the poisoned run did not complete", {"rc": rc})
        return
    hc = compare_hashes(hashes_of(run), hashes_of(base))
    same_terms = manifest_of(run)["degree_terms_digest"] == manifest_of(base)["degree_terms_digest"]
    details = {"run": str(run), "unpoisoned": str(base), "hashes": hc,
               "degree_terms_digest_equal": same_terms,
               "poison": manifest_of(run)["overrides"]["poison_real_block"]}
    if hc["differ"] == 0 and same_terms and hc["compared"] == len(hashes_of(base)):
        record("V7", "PASS", f"all {hc['compared']} per-fit hashes and the degree-term digest "
               "equal to the unpoisoned run", details)
    else:
        record("V7", "REFUSED: a code path reads a real block cell",
               f"{hc['differ']} fits differ; degree terms equal {same_terms}", details)


# ------------------------------------------------------------------------------------------
# V8.

MALE_ARM = "knockout_regrow_male_cns"
V8_FOR = ("the GPU instrument, for future arms that would name it (D11): a flipped pair (E2-II) or "
          "an E1 difference refuses it for every such arm (section 7, V8). An unregistered "
          "cross-check (male D13 (iii)): never an input to a male gate, reference or registered "
          "value")
MALE_STORE_MANIFEST_REQUIRED = {"mode": "synthetic-only", "smoke": False, "starts": 10,
                                "worlds_per_family": 5, "shuffles": 99}


def male_store_paths(lobe, store_arg=None):
    """The lobe's male CPU pre-run folder and its raw_fits.json.gz: --male-store (a folder or the
    store file) or instrument.MALE_PRERUN_STORES[lobe]."""
    p = pathlib.Path(store_arg) if store_arg else I.MALE_PRERUN_STORES[lobe]
    if p.name == "raw_fits.json.gz":
        return p.parent, p
    return p, p / "raw_fits.json.gz"


def male_keys(M):
    """V8's composition (run_registered's --worlds all --n-sh 99 --base on the male arm): every
    world's shuffles 0..98 in the male world_specs() order, then the 45 base views."""
    worlds = [f"{w['family']}:{w['j']}" for w in M.world_specs()]
    return ([f"world:{w}|sh:{sd}" for w in worlds for sd in range(99)]
            + [f"world:{w}" for w in worlds])


def check_male_store(folder, store, lobe, sha_arg=None):
    """V8's reference, before any fit: the folder verifies against its SHA256SUMS.txt (the male
    write_synthetic_outputs writes it last, so a pre-run still writing has none);
    raw_fits.json.gz and synthetic_only.json are listed there (raw_fits equal to
    --male-store-sha256 if given); synthetic_only.json's manifest is a full synthetic-only run of
    this lobe (starts 10, 5 worlds per family, 99 shuffles, all nine families, no smoke) made by
    the male script whose LF sha256 equals this head's; the digest (D10) of its degree terms is
    returned, for the comparison with the adapter's."""
    why, out = [], {"folder": str(folder), "store": str(store)}
    ok, detail = I.check_sha256sums(folder)
    if not ok:
        why.append(f"the folder does not verify against its SHA256SUMS.txt: {detail}")
        return {**out, "passed": False, "reasons": why}
    listed = {}
    for ln in (pathlib.Path(folder) / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        if ln.strip():
            h, name = ln.split(maxsplit=1)
            listed[name.lstrip("*")] = h
    for n in ("raw_fits.json.gz", "synthetic_only.json"):
        if n not in listed:
            why.append(f"{n} is not listed in SHA256SUMS.txt")
    sha = listed.get("raw_fits.json.gz")
    if sha_arg and sha != sha_arg:
        why.append(f"raw_fits.json.gz sha256 {sha}, --male-store-sha256 {sha_arg}")
    if why:
        return {**out, "passed": False, "reasons": why}
    man = json.loads((pathlib.Path(folder) / "synthetic_only.json")
                     .read_text(encoding="utf-8"))["manifest"]
    for k, v in MALE_STORE_MANIFEST_REQUIRED.items():
        if man.get(k) != v:
            why.append(f"manifest {k} = {man.get(k)!r}, V8 needs {v!r}")
    if man.get("lobes") != [lobe]:
        why.append(f"manifest lobes {man.get('lobes')!r}, not [{lobe!r}]")
    families = ["R", "Nf", "No", "W", "M0.5", "M1.0", "M0.6", "M0.75", "M0.85"]
    if man.get("families") != families:
        why.append(f"manifest families {man.get('families')!r}, V8 needs all nine")
    script_now = I.sha256_lf(MALE_SCRIPT)
    if man.get("script_sha256_lf") != script_now:
        why.append(f"the store was made by the male script {man.get('script_sha256_lf')}, this "
                   f"head's is {script_now}: the adapter could build other banks")
    t = (man.get("degree_terms") or {}).get(lobe)
    digest = None
    if t is None:
        why.append(f"the manifest has no degree terms for lobe {lobe}")
    else:
        digest = I.degree_terms_digest((float(t["c"]), np.asarray(t["a"], np.float64),
                                        np.asarray(t["b"], np.float64)))
    return {**out, "passed": not why, "reasons": why, "sha256": sha,
            "degree_terms_digest": digest, "male_script_sha256_lf": script_now,
            "store_git_head": man.get("git_head"), "not_a_reference": man.get("not_a_reference"),
            "reference_mode": man.get("reference_mode")}


def v8(a):
    """V8 of section 7 for one lobe: an unregistered cross-check (male D13 (iii); D11)."""
    run = f"V8_{a.lobe}" if a.lobe in ("L", "R") else "V8"

    def refuse(outcome, why, details):
        log(f"V8 (lobe {a.lobe}): {outcome}: {'; '.join(why)}")
        if not a.inputs_only:
            record(run, outcome, "; ".join(why), {**details, "reasons": why, "for": V8_FOR})
        sys.exit(2)

    why = []
    if a.lobe not in ("L", "R"):
        why.append("--lobe L or R is required (V8 runs per lobe)")
    if not MALE_SCRIPT.is_file():
        why.append(f"the male arm's script {MALE_SCRIPT.relative_to(I.ROOT)} does not exist "
                   "(its S1)")
    folder = store = None
    if not why:
        folder, store = male_store_paths(a.lobe, a.male_store)
        if not store.is_file() or not (folder / "SHA256SUMS.txt").is_file():
            why.append(f"the male arm's CPU pre-run store of lobe {a.lobe} is absent or not "
                       f"finished ({store}; its SHA256SUMS.txt is written last)")
    if why:
        refuse("REFUSED CLEANLY: inputs absent", why, {"store": str(store) if store else None})

    chk = check_male_store(folder, store, a.lobe, a.male_store_sha256)
    if not chk["passed"]:
        refuse("REFUSED CLEANLY: the male store does not verify", chk["reasons"], {"store": chk})
    log(f"V8 (lobe {a.lobe}): male CPU pre-run store {store}, sha256 {chk['sha256']} (listed in "
        f"its SHA256SUMS.txt), made at head {chk['store_git_head']}; male script LF sha256 "
        f"{chk['male_script_sha256_lf']} (equal to this head's)"
        + (f"; {chk['not_a_reference']}" if chk.get("not_a_reference") else ""))

    # The adapter in this process: the lobe's degree terms as the GPU stage computes them (the
    # restriction, then the lobe's outside file, pin-checked), against the store's.
    import male_arm as MA
    MA.set_lobe(a.lobe)
    terms_digest = I.degree_terms_digest(MA.degree_terms())
    if terms_digest != chk["degree_terms_digest"]:
        refuse("REFUSED CLEANLY: the adapter's inputs differ from the pre-run's",
               [f"degree-term digest {terms_digest} (adapter) vs {chk['degree_terms_digest']} "
                "(the store's manifest): the GPU would fit other banks (one known cause: a BLAS "
                "thread count other than 1 in this process; thread variables in effect "
                f"{ {v: os.environ.get(v) for v in THREAD_VARS} })"], {"store": chk})
    log(f"D10: the adapter's degree terms equal the pre-run's (digest {terms_digest})")

    ref, info = G.load_reference(store, chk["sha256"])
    keys = male_keys(MA)
    planned = [I.bf_record_key(k, r) for r in (1, 2, 3, 4) for k in keys]
    missing = ([rk for rk in planned if rk not in ref]
               + [f"{k}||ko||N1" for k in keys if f"{k}||ko||N1" not in ref])
    if missing:
        refuse("REFUSED CLEANLY: the male store lacks planned records",
               [f"{len(missing)} records missing, e.g. {missing[:3]}"], {"store": chk})
    act = G.bf_active(ref, planned)
    act_sum = G.bf_active_summary(ref, planned, act)
    log(f"V8 (lobe {a.lobe}), before the GPU stage: the BF-active classification of the male "
        f"worlds ({len(keys)} banks, {len(planned)} BF ko fits), from the CPU store alone:")
    G.print_bf_active(act_sum)
    if a.inputs_only:
        log(f"V8 (lobe {a.lobe}): inputs verified; --inputs-only: no GPU stage, nothing recorded")
        return

    rc, run_dir, _ = run_gpu("V8", a45_args() + ["--arm-module", MALE_ARM, "--lobe", a.lobe],
                             tag=run, allow_dirty=a.allow_dirty)
    details = {"store": chk, "bf_active_before_gpu": act_sum, "for": V8_FOR,
               "degree_terms_digest_adapter": terms_digest}
    if rc != 0 or run_dir is None:
        record(run, "ERROR", "the GPU run did not complete", {**details, "rc": rc})
        return
    m = manifest_of(run_dir)
    details.update(gpu_run=str(run_dir),
                   gpu_degree_terms_digest_equal=(m["degree_terms_digest"]
                                                  == chk["degree_terms_digest"]),
                   gpu_keys_equal_composition=(m["keys"] == keys),
                   adapter_worker=m["arm"].get("worker_init"),
                   census_gpu_run=m["census"])
    rep = G.compare_run(run_dir, ref, info, arm=MA)
    G.print_report(rep)
    rep_path = I.DATA_ROOT / f"{run}_report_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.json"
    I.write_json(rep_path, rep)
    details.update({k: v for k, v in rep.items() if k != "per_fit"})
    details["full_report"] = str(rep_path)
    if not (details["gpu_degree_terms_digest_equal"] and details["gpu_keys_equal_composition"]):
        outcome = "ERROR: the GPU run's inputs are not the pre-run's"
    elif rep["outcome"] == 1:
        outcome = "CROSS-CHECK: EQUIVALENT (outcome 1)"
    else:
        outcome = f"CROSS-CHECK: REFUSES THE INSTRUMENT FOR FUTURE ARMS (outcome {rep['outcome']})"
    record(run, outcome,
           f"{rep['outcome_text']}; E1 failures {len(rep['e1_failures'])}, flipped pairs "
           f"{rep['n_flipped_pairs']}, E3 failures {len(rep['e3_failures'])}, at risk "
           f"{len(rep['at_risk'])}; fits not bit-equal {rep['n_not_bit_equal']}, of which carry "
           f"ties {rep['differing_fits_that_carry_ties']}; at-risk fits whose p differs from N1 "
           f"{rep['at_risk_fits_whose_p_differs_from_n1']}; decides nothing for the male arm "
           "(its D13 (iii))", details)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run", choices=["V0", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8"])
    ap.add_argument("--allow-dirty", action="store_true",
                    help="GPU runs from an uncommitted tree (marked NOT FROM A COMMITTED HEAD)")
    ap.add_argument("--parts", default=None)
    ap.add_argument("--male-store", default=None)
    ap.add_argument("--male-store-sha256", default=None)
    ap.add_argument("--lobe", default=None)
    ap.add_argument("--inputs-only", action="store_true",
                    help="V8: verify the inputs and print the BF-active classification; no GPU")
    a = ap.parse_args()
    {"V0": v0, "V1": v1, "V2": v2, "V3": v3, "V4": v4, "V5": v5, "V6": v6, "V7": v7,
     "V8": v8}[a.run](a)


if __name__ == "__main__":
    main()
