"""Extension X (block mask and fixed lambda; draft, not registered): the validation driver.
Entry: run_ext.py (imports gpu_env first). Validation runs only; no arm may use it before the
revision that registers extension X (D11).

Plan: docs/plans/2026-09-29-gpu-instrument-extension-x-plan.md (draft for review).
One run fits BF_1..BF_4 of one arm (A or B) on one mask ("block" or "ko1") for the arm's 45 base
views, and writes, as the registered driver does (gpu_stage.py; G4-G6, G15, G16):
  raw_fits_gpu.json.gz   records "<bank>||<mask>||BF:<r>" in the arm's store schema
  fit_hashes.json        per fit, the sha256 of the raw float64 U, V, lambda and the decoded p
  census.json.gz         per fit, the tie census (ext_census; no reference: no flip count)
  manifest.json          stamp and its check, settings, threads, head and tree, the composition
                         identity (G18: the extension digest of mask, keys, starts, ranks; the
                         degree-term digest; the arm module), row_chunk,
                         near-ties (block), the census with its scope label, timings, VRAM
  SHA256SUMS.txt
into connectome-seed-data/gpu_instrument/<label>_<arm>_<mask>_<UTC>_<head 12>/ (or --out;
refused at or in any reference folder: instrument.out_dir_refusal plus B's two folders).

The checks it keeps from the registered driver: G1 (gpu_env first), G8 (v1, v2 and the rule port
refused: gpu_stage is imported, which installs the import refusal), R1 (the registered stamp, or
R2, R3, R7 (a clean tree, or --allow-dirty, which
marks the run NOT FROM A COMMITTED HEAD), G11 (extended), D10 (degree-term digest in every
worker), the VRAM preflight against the registered need at row_chunk (12,526 MiB at 40,000;
too little stops the run, no fallback). Labels: VX0 (smoke, one world), VX1 (the V1 scheme: run
three times), VX6 (--bf-tol 1e-5, the comparator's negative control), VX7 (--poison-real-block).

Usage (torch venv, instrument.TORCH_PY), after llama-server is stopped on Mike's word:
  python run_ext.py --label VX1 --arm B --mask block
"""
import sys

if "gpu_env" not in sys.modules:
    raise RuntimeError("REFUSED (G1): ext_gpu_stage loaded without gpu_env imported first; run "
                       "run_ext.py")
import gpu_env  # noqa: E402

import argparse  # noqa: E402
import os  # noqa: E402
import pathlib  # noqa: E402
import time  # noqa: E402
import json  # noqa: E402
from concurrent.futures import ProcessPoolExecutor  # noqa: E402

import numpy as np  # noqa: E402
import torch  # noqa: E402

import gpu_stage as GS  # noqa: E402  (installs G8's import refusal; SmiSampler, log)
import instrument as I  # noqa: E402
import prep  # noqa: E402
import harness as H  # noqa: E402
import gpu_bf3  # noqa: E402
import ext_scope as XS  # noqa: E402
import ext_prep as XP  # noqa: E402
import ext_census as XC  # noqa: E402
import ext_engine as XE  # noqa: E402

EXT_LABELS = ("VX0", "VX1", "VX6", "VX7")
log = GS.log


def refusals(a):
    why = []
    if a.label not in EXT_LABELS:
        why.append(f"label {a.label!r}; one of {EXT_LABELS} (validation only)")
    if gpu_env.FLAGS_OFF:
        why.append("GPU_INSTRUMENT_FLAGS_OFF in an extension-X run")
    if a.bf_tol is not None and a.label != "VX6":
        why.append("--bf-tol outside VX6")
    if a.poison_real_block and a.label != "VX7":
        why.append("--poison-real-block outside VX7")
    if os.environ.get("GPU_INSTRUMENT_DEVICE", "cuda") != "cuda":
        why.append("a device other than cuda")
    if why:
        raise SystemExit("REFUSED: " + "; ".join(why))


def compose_keys(K, a):
    worlds = ([f"{w['family']}:{w['j']}" for w in K.world_specs()] if a.worlds == "all"
              else a.worlds.split(","))
    keys = [XS.check_base_key(f"world:{w}") for w in worlds]
    if len(set(keys)) != len(keys):
        raise ValueError("REFUSED: a key appears twice in the composition")
    return keys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--arm", choices=sorted(XS.ARMS), required=True)
    ap.add_argument("--mask", choices=XS.EXT_MASKS, required=True)
    ap.add_argument("--worlds", default="all")
    ap.add_argument("--ranks", default="1,2,3,4")
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--row-chunk", type=int, default=40000)
    ap.add_argument("--stamp-unregistered", action="store_true")
    ap.add_argument("--allow-dirty", action="store_true")
    ap.add_argument("--bf-tol", type=float, default=None)
    ap.add_argument("--poison-real-block", action="store_true")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    t_start = time.time()
    refusals(a)
    ranks = tuple(int(r) for r in a.ranks.split(","))
    if not ranks or any(r not in XS.RANKS for r in ranks) or len(set(ranks)) != len(ranks):
        raise SystemExit(f"REFUSED: ranks {a.ranks!r}")
    arm_name = XS.ARMS[a.arm]
    K = prep.set_arm(arm_name, None)
    keys = compose_keys(K, a)

    head = I.git_head()
    dirty = I.tree_dirty_paths(exclude_validation=True)
    if dirty and not a.allow_dirty:
        raise SystemExit("REFUSED (R7): uncommitted changes under results/genome/c6/ or "
                         "docs/plans/:\n" + "\n".join(dirty))
    out = (pathlib.Path(a.out) if a.out else
           I.private_run_dir(f"{a.label}_{a.arm}_{a.mask}", head))
    why = XS.ext_out_dir_refusal(out)
    if why:
        raise SystemExit(why)
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"REFUSED: {out} exists and is not empty")

    file_hashes = I.instrument_file_hashes()
    env = gpu_env.environment_record()
    stamp = gpu_env.stamp(env)
    try:
        stamp_check = I.check_stamp(stamp, allow_unregistered=a.stamp_unregistered)
    except ValueError as e:
        raise SystemExit(str(e))
    log(f"GPU instrument, extension X (draft, unregistered): {a.label} arm {a.arm} "
        f"({arm_name}) mask {a.mask}; head {head[:12]}"
        f"{' (DIRTY: NOT FROM A COMMITTED HEAD)' if dirty else ''}")
    log(f"R1 stamp: {stamp_check['status']}; {json.dumps(stamp, sort_keys=True)}")

    overrides = {"bf_tol": None, "poison_real_block": None}
    if a.bf_tol is not None:
        overrides["bf_tol"] = {"registered": H.BF_TOL, "set_in_gpu_process": a.bf_tol}
        H.BF_TOL = a.bf_tol
    if a.poison_real_block:
        overrides["poison_real_block"] = prep.poison_real_block()

    prep.restrict_grid(K)
    terms = K.degree_terms()
    terms_digest = I.degree_terms_digest(terms)
    K._w_init(10, terms, True)
    starts = H.STARTS
    identity = XS.ext_composition_identity(a.mask, keys, starts, ranks, terms_digest, arm_name)
    digest = identity["composition"]
    log(f"D10 degree terms digest {terms_digest}; extension digest {digest} "
        f"({len(keys)} base views, ranks {list(ranks)}, starts {starts}); row_chunk "
        f"{a.row_chunk} (recorded)")

    smi = GS.SmiSampler()
    smi.start()
    marks = {}
    pool = ProcessPoolExecutor(max_workers=a.workers, initializer=prep.init_arm_worker,
                               initargs=(arm_name, None, terms, bool(a.poison_real_block)))
    try:
        list(pool.map(int, range(a.workers)))
        worker_env = pool.submit(prep.worker_record).result()
        if worker_env["degree_terms_digest"] != terms_digest:
            raise SystemExit("REFUSED (D10): a prep worker's degree terms differ")
        marks["prep_start"] = time.time()
        preps = list(pool.map(XP.prepare_key_ext, keys, [a.mask] * len(keys), chunksize=2))
        marks["prep_end"] = time.time()
        need = I.REGISTERED_VRAM_NEED_MIB.get(a.row_chunk)
        if need is None:
            raise SystemExit(f"REFUSED (R4): no registered VRAM need for row_chunk {a.row_chunk}")
        free, total = torch.cuda.mem_get_info()
        vram = {"free_mib_before_upload": free / 2 ** 20, "total_mib": total / 2 ** 20,
                "registered_need_mib": need}
        if free / 2 ** 20 < need:
            raise SystemExit(f"REFUSED (R4): {free / 2 ** 20:.0f} MiB free, the registered need "
                             f"is {need} MiB; no fallback (is llama-server still running?)")
        marks["gpu_start"] = time.time()
        results, info = XE.run_core(keys, preps, a.mask, ranks, starts, a.row_chunk,
                                    lambda t: pool.submit(XP.decode_records_ext, t),
                                    sync=torch.cuda.synchronize, log=log)
        marks["gpu_end"] = time.time()
        vram["torch_peak_alloc_mib"] = torch.cuda.max_memory_allocated() / 2 ** 20
    finally:
        pool.shutdown()
        smi.stop()
    GS.assert_no_unregistered_engine()

    records, hashes = {}, {}
    for r, (rk, rec, h) in results:
        rec["secs"] = info["rank_secs"][r] / len(keys)
        records[rk], hashes[rk] = rec, h
    planned = XS.planned(keys, a.mask, ranks)
    assert sorted(records) == sorted(planned), "records do not match the planned keys"
    p_n1 = {pp["key"]: pp["p_n1"] for pp in preps}
    entries = [(rk, XC.census_fit(records[rk]["p"], records[rk]["y"], *rk.split("||")[:2],
                                  p_n1=p_n1[rk.split("||")[0]])) for rk in planned]
    scope = (f"arm {a.arm} {a.mask}-mask BF fits of this run ({len(planned)} fits, "
             f"{len(keys)} base views)")
    fam = XC.family_summary_scoped(entries, scope)
    risk = XC.at_risk_list(entries, names=[f"{s}->{t}" for s, t in K.BLOCK_NAMES])

    out.mkdir(parents=True, exist_ok=False)
    I.write_json_gz(out / "raw_fits_gpu.json.gz", {rk: records[rk] for rk in planned})
    I.write_json(out / "fit_hashes.json", {rk: hashes[rk] for rk in planned})
    I.write_json_gz(out / "census.json.gz", {rk: c for rk, c in entries})
    manifest = {
        "instrument": "GPU instrument, engine v3, extension X driver run_ext.py (draft, "
                      "unregistered; validation only)",
        "plan": "docs/plans/2026-09-29-gpu-instrument-extension-x-plan.md",
        "registration": I.REGISTRATION, "revision": I.REGISTRATION_REVISION,
        "label": a.label, "argv": sys.argv[1:], "arm": {"name": a.arm, "module": arm_name},
        "mask": a.mask, "git_head": head, "not_from_a_committed_head": bool(dirty),
        "tree_dirty_paths": dirty, "file_sha256_lf": file_hashes,
        "environment_main": env, "environment_prep_worker": worker_env,
        "stamp": stamp, "stamp_check": stamp_check,
        "determinism_settings": gpu_env.SETTINGS, "threads": gpu_env.thread_record(),
        "overrides": overrides, "keys": keys, "ranks": list(ranks), "starts": starts,
        "extension_digest": digest, "composition_identity": identity,
        "registration_text": I.REGISTRATION_TEXT,
        "registered_digest_for_comparison": I.composition_digest(keys, starts, ranks),
        "row_chunk": a.row_chunk, "n_folds": info["n_folds"], "grids_per_bank": info["per"],
        "degree_terms_digest": terms_digest,
        "near_ties_by_rank": {str(r): v for r, v in info["near_ties"].items()},
        "lambda_by_rank": {str(r): v for r, v in info["lambda_by_rank"].items()},
        "secs": {"prep": marks["prep_end"] - marks["prep_start"],
                 "gpu_ranks": {str(r): v for r, v in info["rank_secs"].items()},
                 "gpu_and_decode": marks["gpu_end"] - marks["gpu_start"],
                 "end_to_end_wall": time.time() - t_start},
        "vram": vram,
        "gpu_util": {"gpu": smi.stats(marks["gpu_start"], marks["gpu_end"])},
        "census": {"by_column_family": fam, "at_risk": risk, "band": XC.BAND,
                   "fits_p_differs_from_n1": sum(1 for _, c in entries
                                                 if c["p_equals_n1"] is False)},
        "files": {"records": "raw_fits_gpu.json.gz", "hashes": "fit_hashes.json",
                  "census": "census.json.gz"}}
    I.write_json(out / "manifest.json", manifest)
    I.write_sha256sums(out)
    log(f"census ({scope}): {json.dumps(fam['families'], sort_keys=True)}")
    log(f"at risk: {len(risk)}; wrote {out}")
    print(f"RUN_DIR={out}", flush=True)
