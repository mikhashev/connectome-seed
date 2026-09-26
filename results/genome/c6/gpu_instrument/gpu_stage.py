"""The registered GPU stage of the hybrid synthetic step (engine v3 only); entry: run_registered.py.

docs/plans/2026-09-26-gpu-instrument-registration.md, revision 1.3 (ec5cbc0): D1 (a), D2 (a),
D5 (a), D6 (a), D7 (i), D8 (I2), D10 (a); R1-R7 of section 6; G1-G8, G11, G15, G16 of section 10.
The GPU stage fits BF_1..BF_4 on the ko mask of synthetic base views and shuffles and writes:
  raw_fits_gpu.json.gz   the BF ko records in A's store schema (G4): p, y, lam, score,
                         outside_density, secs ("apportioned": the rank's GPU wall time / banks)
  fit_hashes.json        per fit, the sha256 of the raw float64 U, V, lambda and the decoded p (G6)
  census.json.gz         per fit, the tie census of G16 (no reference: no flip count)
  manifest.json          G2 (environment, stamp and its check), R2 (settings), R3 (threads), G3
                         (composition: refusal digest; row_chunk and chunk boundaries recorded),
                         D10 (degree-term digest), G15 (near-ties by rank), G16 (census by column
                         family, the at-risk list), timings, the file hashes, the keys
  SHA256SUMS.txt         over the files above (G5)
into a private folder connectome-seed-data/gpu_instrument/<tag>_<UTC>_<head 12>/ (section 7), or
--out (refused at or in a reference folder, G11). The arm's CPU stage checks this folder
(hybrid_arm.check_gpu_stage, G13) and fits everything else on the CPU in tools/.venv (D8 (I2)).

Run kinds:
  --kind arm         an arm's GPU pre-run or registered run: a registered stamp is required (R1),
                     an expected composition digest is required (R4), a clean tree at the head
                     (R7); no override of any kind.
  --kind validation  V0-V8 of section 7 (launched by validation.py): --label names the run;
                     --stamp-unregistered is accepted while no stamp is registered (the manifest
                     says so); the overrides below are accepted only for their run.
Overrides (validation only): GPU_INSTRUMENT_FLAGS_OFF=1 (label V0-off: V0's flag-free comparison
run); --bf-tol 1e-5 (label V6); --poison-real-block (labels V7, T-G5); GPU_INSTRUMENT_DEVICE=cpu
(label V5b); --allow-dirty (the run is marked NOT FROM A COMMITTED HEAD).

The real block: never read, fit or scored. Keys are world:<family>:<j>[|sh:<sd>] only (R6). The
harness import builds REAL at module level as in every harness process; the one real-bank fit is
the degree terms on the real knockout view (outside-block cells), as A's --synthetic-only makes it.

Entry point: run_registered.py, which imports gpu_env first and then this module (so that the
prep workers, which Windows spawns by re-running the entry script as __mp_main__, import neither
torch nor this module). This module refuses to load unless gpu_env was imported before it.

Usage (torch venv; paths in instrument.TORCH_PY):
  python run_registered.py --kind validation --label V0 --worlds R:0 --n-sh 99 --base \
      --stamp-unregistered --allow-dirty
"""
import sys

if "gpu_env" not in sys.modules:
    raise RuntimeError("REFUSED (G1): gpu_stage loaded without gpu_env imported first; run "
                       "run_registered.py")
import gpu_env  # noqa: E402  (G1: already imported first by run_registered.py)

import argparse  # noqa: E402
import importlib.abc  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import pathlib  # noqa: E402
import subprocess  # noqa: E402
import threading  # noqa: E402
import time  # noqa: E402
from concurrent.futures import ProcessPoolExecutor  # noqa: E402

import numpy as np  # noqa: E402
import torch  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

# G8 / D2: v1, v2 and the rule port are never loaded by the registered driver.
FORBIDDEN_ENGINES = ("gpu_bf", "gpu_bf2", "gpu_rule")


class _RefuseUnregisteredEngines(importlib.abc.MetaPathFinder):
    def find_spec(self, name, path=None, target=None):
        if name in FORBIDDEN_ENGINES:
            raise ImportError(f"REFUSED (G8, D2): the registered driver never imports {name} "
                              "(engines v1, v2 and the rule port are unregistered history)")
        return None


def assert_no_unregistered_engine():
    bad = [m for m in FORBIDDEN_ENGINES if m in sys.modules]
    if bad:
        raise RuntimeError(f"REFUSED (G8): unregistered engine modules loaded: {bad}")


assert_no_unregistered_engine()
sys.meta_path.insert(0, _RefuseUnregisteredEngines())

import instrument as I  # noqa: E402
import census as C  # noqa: E402
import prep  # noqa: E402
import harness as H  # noqa: E402
import gpu_bf3  # noqa: E402  (engine v3; imports gpu_common, not gpu_bf2 or gpu_bf)

assert_no_unregistered_engine()

VALIDATION_LABELS = ("V0", "V0-off", "V1", "V4a", "V4b", "V4c", "V4d", "V5b", "V6", "V7", "V8",
                     "T-G5", "T-G5-poison", "T-G7", "smoke")


class SmiSampler(threading.Thread):
    """nvidia-smi utilisation and memory every 500 ms (as run_pipeline.py)."""

    def __init__(self):
        super().__init__(daemon=True)
        self.samples = []
        self.proc = None

    def run(self):
        try:
            self.proc = subprocess.Popen(["nvidia-smi", "--query-gpu=utilization.gpu,memory.used",
                                          "--format=csv,noheader,nounits", "-lms", "500"],
                                         stdout=subprocess.PIPE, text=True)
            for line in self.proc.stdout:
                try:
                    u, m = (float(x) for x in line.strip().split(","))
                    self.samples.append((time.time(), u, m))
                except ValueError:
                    pass
        except Exception:
            pass

    def stop(self):
        if self.proc is not None:
            self.proc.terminate()

    def stats(self, t0, t1):
        u = [s[1] for s in self.samples if t0 <= s[0] <= t1]
        m = [s[2] for s in self.samples if t0 <= s[0] <= t1]
        if not u:
            return None
        u = np.array(u, float)
        return {"n_samples": len(u), "util_mean": float(u.mean()),
                "util_median": float(np.median(u)), "mem_used_max_mib": float(max(m))}


def log(m=""):
    print(m, flush=True)


def compose_keys(K, a):
    """The ordered key list: --keys-file (one key per line, in order), or as run_pipeline.py
    composes it: every world's shuffles 0..n_sh-1 (world order of K.world_specs()), then, with
    --base, the base views; --base-only gives the base views alone."""
    if a.keys_file:
        keys = [ln.strip() for ln in pathlib.Path(a.keys_file).read_text(encoding="utf-8")
                .splitlines() if ln.strip()]
    elif a.keys:
        keys = [k.strip() for k in a.keys.split(",") if k.strip()]
    else:
        worlds = ([f"{w['family']}:{w['j']}" for w in K.world_specs()] if a.worlds == "all"
                  else a.worlds.split(","))
        keys = [] if a.base_only else [f"world:{w}|sh:{sd}" for w in worlds
                                       for sd in range(a.n_sh)]
        if a.base or a.base_only:
            keys += [f"world:{w}" for w in worlds]
    for k in keys:
        I.check_key(k)                                      # R6, before any work
    if len(set(keys)) != len(keys):
        raise ValueError("REFUSED: a key appears twice in the composition")
    return keys


def refusals(a):
    """Which run may use which override (validation only), and the arm run's requirements."""
    why = []
    lab = a.label
    if a.kind == "arm":
        if gpu_env.FLAGS_OFF:
            why.append("GPU_INSTRUMENT_FLAGS_OFF in an arm run")
        if a.bf_tol is not None or a.poison_real_block or a.allow_dirty or a.stamp_unregistered:
            why.append("an override (--bf-tol, --poison-real-block, --allow-dirty, "
                       "--stamp-unregistered) in an arm run")
        if a.expect_digest is None:
            why.append("an arm run needs --expect-digest (R4: the registered composition)")
        if os.environ.get("GPU_INSTRUMENT_DEVICE", "cuda") != "cuda":
            why.append("an arm run on a device other than cuda")
    else:
        if lab not in VALIDATION_LABELS:
            why.append(f"unknown validation label {lab!r}; one of {VALIDATION_LABELS}")
        if gpu_env.FLAGS_OFF and lab != "V0-off":
            why.append("GPU_INSTRUMENT_FLAGS_OFF outside V0's comparison run (label V0-off)")
        if lab == "V0-off" and not gpu_env.FLAGS_OFF:
            why.append("label V0-off needs GPU_INSTRUMENT_FLAGS_OFF=1")
        if a.bf_tol is not None and lab != "V6":
            why.append("--bf-tol outside V6")
        if a.poison_real_block and lab not in ("V7", "T-G5-poison"):
            why.append("--poison-real-block outside V7 / T-G5")
        if os.environ.get("GPU_INSTRUMENT_DEVICE", "cuda") != "cuda" and lab != "V5b":
            why.append("GPU_INSTRUMENT_DEVICE other than cuda outside V5b")
    if why:
        raise SystemExit("REFUSED: " + "; ".join(why))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", choices=["arm", "validation"], required=True)
    ap.add_argument("--label", required=True, help="validation: V0..V8; arm: the arm's run name")
    ap.add_argument("--arm-module", default=prep.DEFAULT_ARM)
    ap.add_argument("--lobe", default=None)
    ap.add_argument("--worlds", default="all")
    ap.add_argument("--n-sh", type=int, default=99)
    ap.add_argument("--base", action="store_true")
    ap.add_argument("--base-only", action="store_true")
    ap.add_argument("--keys", default=None, help="comma-separated ordered keys")
    ap.add_argument("--keys-file", default=None)
    ap.add_argument("--ranks", default="1,2,3,4")
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--row-chunk", type=int, default=40000)
    ap.add_argument("--expect-digest", default=None)
    ap.add_argument("--stamp-unregistered", action="store_true")
    ap.add_argument("--allow-dirty", action="store_true")
    ap.add_argument("--bf-tol", type=float, default=None)
    ap.add_argument("--poison-real-block", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--tag", default=None)
    a = ap.parse_args()
    t_start = time.time()
    refusals(a)
    ranks = tuple(int(r) for r in a.ranks.split(","))
    if not ranks or any(r not in (1, 2, 3, 4) for r in ranks) or len(set(ranks)) != len(ranks):
        raise SystemExit(f"REFUSED: ranks {a.ranks!r}")

    # The arm module in the main process (G7), then the keys (R6) before any work.
    K = prep.set_arm(a.arm_module, a.lobe)
    keys = compose_keys(K, a)

    # R7: head and tree.
    head = I.git_head()
    dirty = I.tree_dirty_paths(exclude_validation=(a.kind == "validation"))
    if dirty and not a.allow_dirty:
        raise SystemExit("REFUSED (R7): uncommitted changes under results/genome/c6/ or "
                         "docs/plans/:\n" + "\n".join(dirty))
    out = pathlib.Path(a.out) if a.out else I.private_run_dir(a.tag or a.label, head)
    refusal = I.out_dir_refusal(out)                         # G11, before any write
    if refusal:
        raise SystemExit(refusal)
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"REFUSED: {out} exists and is not empty")

    # R1-R3: environment, stamp, settings, threads.
    file_hashes, a_pinned = I.instrument_file_hashes(), I.a_pinned_file_hashes()  # G2, at start
    if not a_pinned["pins_equal"]:
        raise SystemExit("REFUSED: A's pinned files (knockout_regrow.PINS) differ from their pins")
    env = gpu_env.environment_record()
    stamp = gpu_env.stamp(env)
    try:
        stamp_check = I.check_stamp(stamp, allow_unregistered=a.stamp_unregistered)
    except ValueError as e:
        raise SystemExit(str(e))
    log(f"GPU instrument, registered driver (engine v3): {a.kind} {a.label}; registration "
        f"{I.REGISTRATION} revision {I.REGISTRATION_REVISION} ({I.REGISTRATION_COMMIT}); "
        f"head {head[:12]}{' (DIRTY: NOT FROM A COMMITTED HEAD)' if dirty else ''}")
    log(f"R1 stamp: {stamp_check['status']}; {json.dumps(stamp, sort_keys=True)}")
    log(f"R2 settings: {json.dumps(gpu_env.SETTINGS, sort_keys=True)}")
    log(f"R3 threads: {json.dumps(gpu_env.thread_record(), sort_keys=True)}")

    # Overrides (validation only; refusals() has checked which run may use which).
    overrides = {"flags_off": gpu_env.FLAGS_OFF, "bf_tol": None, "poison_real_block": False,
                 "device": os.environ.get("GPU_INSTRUMENT_DEVICE", "cuda")}
    if a.bf_tol is not None:
        overrides["bf_tol"] = {"registered": H.BF_TOL, "set_in_gpu_process": a.bf_tol}
        H.BF_TOL = a.bf_tol                               # read at call time by gpu_bf3
        log(f"OVERRIDE (V6): harness.BF_TOL = {a.bf_tol} in the GPU process only")
    poison = None
    if a.poison_real_block:
        poison = prep.poison_real_block()
        overrides["poison_real_block"] = poison
        log(f"OVERRIDE ({a.label}): harness.REAL block cells flipped in the main process and "
            f"every prep worker: {poison}")

    # D10: degree terms, as A's --synthetic-only computes them, and their digest.
    prep.restrict_grid(K)
    terms = K.degree_terms()
    terms_digest = I.degree_terms_digest(terms)
    log(f"D10 degree terms (N1 on the knockout view of the arm's real bank, outside-block cells "
        f"only): digest {terms_digest}")
    K._w_init(10, terms, True)
    assert H.STARTS == 10
    starts = H.STARTS

    # R4 / G3: the composition and its refusal digest.
    n_lambdas = len(H.BF_LAMBDAS)
    comp_digest = I.composition_digest(keys, starts, ranks)
    try:
        comp_check = I.check_composition(comp_digest, a.expect_digest)
    except ValueError as e:
        raise SystemExit(str(e))
    log(f"R4 composition: {len(keys)} banks, ranks {list(ranks)}, starts {starts}; refusal "
        f"digest {comp_digest} ({comp_check['status']}); row_chunk {a.row_chunk} (recorded)")

    smi = SmiSampler()
    smi.start()
    marks = {}
    pool = ProcessPoolExecutor(max_workers=a.workers, initializer=prep.init_arm_worker,
                               initargs=(a.arm_module, a.lobe, terms, bool(a.poison_real_block)))
    try:
        list(pool.map(int, range(a.workers)))                  # start the workers
        worker_env = pool.submit(prep.worker_record).result()   # G2: one prep worker
        if worker_env["degree_terms_digest"] != terms_digest:
            raise SystemExit("REFUSED (D10): a prep worker's degree terms differ from the main "
                             "process's")
        marks["prep_start"] = time.time()
        preps = list(pool.map(prep.prepare_key_compact, keys, chunksize=8))
        marks["prep_end"] = time.time()
        n_folds = preps[0]["n_folds"]
        if any(pp["n_folds"] != n_folds for pp in preps):
            raise SystemExit("REFUSED: banks with different numbers of inner folds")
        comp_rec = I.composition_record(keys, starts, ranks, a.row_chunk, n_folds, n_lambdas)
        prep_bytes = sum(sum(v.nbytes for v in pp.values() if isinstance(v, np.ndarray))
                         for pp in preps)

        # R4: VRAM preflight against the registered need; no automatic chunk fallback.
        vram = {"device": str(gpu_bf3.DEVICE)}
        if gpu_bf3.DEVICE.type == "cuda":
            need = I.REGISTERED_VRAM_NEED_MIB.get(a.row_chunk)
            if need is None:
                raise SystemExit(f"REFUSED (R4): no registered VRAM need for row_chunk "
                                 f"{a.row_chunk} (registered: {I.REGISTERED_VRAM_NEED_MIB})")
            free, total = torch.cuda.mem_get_info()
            vram.update(free_mib_before_upload=free / 2 ** 20, total_mib=total / 2 ** 20,
                        registered_need_mib=need)
            if free / 2 ** 20 < need:
                raise SystemExit(f"REFUSED (R4): {free / 2 ** 20:.0f} MiB free, the registered "
                                 f"need at row_chunk {a.row_chunk} is {need} MiB; no fallback")
            torch.cuda.synchronize()
        marks["upload_start"] = time.time()
        S = gpu_bf3.GridStore(preps)
        if gpu_bf3.DEVICE.type == "cuda":
            torch.cuda.synchronize()
        marks["gpu_start"] = time.time()
        futs, rank_secs, near_ties, lam_by_rank = [], {}, {}, {}
        for r in ranks:
            t1 = time.time()
            lam, U, V, ll, near = gpu_bf3.fit_bf_all(S, n_folds, r, row_chunk=a.row_chunk)
            if gpu_bf3.DEVICE.type == "cuda":
                torch.cuda.synchronize()
            rank_secs[r] = time.time() - t1
            near_ties[r] = near                                 # G15
            lam_by_rank[r] = {str(x): int((lam == x).sum()) for x in sorted(set(lam.tolist()))}
            by_world = {}
            for i, (key, pp) in enumerate(zip(keys, preps)):
                data = dict(pp["n1"])
                data.update({"bf_U": U[i], "bf_V": V[i], "bf_lambda": np.array([float(lam[i])])})
                by_world.setdefault(key.split("|")[0], []).append(
                    (key, data, pp["y_block"], pp["block_content"], pp["outside_density"]))
            futs += [(r, pool.submit(prep.decode_records, (r, items)))
                     for items in by_world.values()]
            log(f"BF_{r}: {len(keys)} banks in {rank_secs[r]:.1f}s; lambda {lam_by_rank[r]}; "
                f"near-ties {near} (G15: this run's own count)")
        marks["gpu_end"] = time.time()
        results = [(r, x) for r, f in futs for x in f.result()]
        marks["decode_end"] = time.time()
        vram_peak = (torch.cuda.max_memory_allocated() / 2 ** 20
                     if gpu_bf3.DEVICE.type == "cuda" else None)
    finally:
        pool.shutdown()
        smi.stop()
    assert_no_unregistered_engine()

    # G4: records, secs apportioned per rank; G6: the hash sidecar.
    records, hashes = {}, {}
    nb = len(keys)
    for r, (rk, rec, h) in results:
        rec["secs"] = rank_secs[r] / nb
        records[rk] = rec
        hashes[rk] = h
    planned = [I.bf_record_key(k, r) for r in ranks for k in keys]
    assert sorted(records) == sorted(planned), "records do not match the planned keys"

    # G16: the census of every fit (no reference: no flip count).
    p_n1 = {pp["key"]: pp["p_n1"] for pp in preps}
    entries = []
    for rk in planned:
        bk, mk, _ = I.split_record_key(rk)
        entries.append((rk, C.census_fit(records[rk]["p"], records[rk]["y"], bk, mk,
                                         p_n1=p_n1[bk])))
    fam = C.family_summary(entries)
    risk = C.at_risk_list(entries, names=[f"{s}->{t}" for s, t in K.BLOCK_NAMES])
    bf_active = sum(1 for _, c in entries if c["p_equals_n1"] is False)

    out.mkdir(parents=True, exist_ok=False)
    rec_path = out / "raw_fits_gpu.json.gz"
    I.write_json_gz(rec_path, {rk: records[rk] for rk in planned})
    I.write_json(out / "fit_hashes.json", {rk: hashes[rk] for rk in planned})
    I.write_json_gz(out / "census.json.gz", {rk: c for rk, c in entries})
    t_end = time.time()
    secs = {"setup_before_prep": marks["prep_start"] - t_start,
            "prep": marks["prep_end"] - marks["prep_start"],
            "upload": marks["gpu_start"] - marks["upload_start"],
            "gpu_ranks": {str(r): v for r, v in rank_secs.items()},
            "gpu_total": marks["gpu_end"] - marks["gpu_start"],
            "decode_tail_after_gpu": marks["decode_end"] - marks["gpu_end"],
            "end_to_end_wall": t_end - t_start}
    manifest = {
        "instrument": "GPU instrument, engine v3, registered driver run_registered.py",
        "registration": I.REGISTRATION, "revision": I.REGISTRATION_REVISION,
        "registration_commit": I.REGISTRATION_COMMIT, "applied_ahead": I.APPLIED_AHEAD,
        "kind": a.kind, "label": a.label, "argv": sys.argv[1:],
        "not_from_a_committed_head": bool(dirty), "tree_dirty_paths": dirty,
        "tree_check_excludes": I.VALIDATION_EXCLUDED if a.kind == "validation" else None,
        "git_head": head,
        "file_sha256_lf": file_hashes, "a_pinned": a_pinned,
        "environment_main": env, "environment_prep_worker": worker_env,
        "stamp": stamp, "stamp_check": stamp_check,
        "determinism_settings": gpu_env.SETTINGS, "threads": gpu_env.thread_record(),
        "overrides": overrides,
        "arm": {"module": a.arm_module, "lobe": a.lobe,
                "worker_init": worker_env.get("arm")},
        "composition": comp_rec, "composition_check": comp_check,
        "keys": keys, "planned_record_keys_order": "for each rank in rank order, keys in order",
        "degree_terms_digest": terms_digest,
        "near_ties_by_rank": {str(r): v for r, v in near_ties.items()},
        "near_ties_note": "this run's own count (G15); never carried over from another run",
        "lambda_by_rank": {str(r): v for r, v in lam_by_rank.items()},
        "secs": secs,
        "secs_field": ("apportioned: each record's secs is its rank's GPU wall time divided by "
                       "the number of banks (G4)"),
        "vram": {**vram, "torch_peak_alloc_mib": vram_peak},
        "gpu_util": {"prep": smi.stats(marks["prep_start"], marks["prep_end"]),
                     "gpu": smi.stats(marks["gpu_start"], marks["gpu_end"])},
        "prep_arrays_mib": prep_bytes / 2 ** 20,
        "census": {"by_column_family": fam, "at_risk": risk, "band": C.BAND,
                   "fits_p_differs_from_n1": bf_active,
                   "note": ("no reference in this run: ties, gaps and the at-risk list only; "
                            "no flip count (section 5, E2-II)")},
        "files": {"records": rec_path.name, "hashes": "fit_hashes.json",
                  "census": "census.json.gz"},
        "file_sha256": {n: I.sha256_file(out / n) for n in
                        ("raw_fits_gpu.json.gz", "fit_hashes.json", "census.json.gz")},
        "unregistered_engines_absent": all(m not in sys.modules for m in FORBIDDEN_ENGINES)}
    I.write_json(out / "manifest.json", manifest)
    I.write_sha256sums(out)

    log(f"G16 census by column family: {json.dumps(fam, sort_keys=True)}")
    log(f"E2-III at-risk list (smallest gap on S(f) < 2^-23; a list, not a gate): "
        f"{len(risk)} fits")
    for e in risk:
        log(f"  at risk: {e['key']} gap {e['gap']:.4g} cells {e['cell_names']} labels "
            f"{e['labels']} p {e['p']} p_equals_n1 {e['p_equals_n1']}")
    log(f"fits whose p differs from their view's N1 p: {bf_active} of {len(entries)}")
    log(f"G15 near-ties by rank: {manifest['near_ties_by_rank']}")
    log(f"secs: {json.dumps(secs)}; torch peak {vram_peak} MiB")
    log(f"wrote {out}")
    print(f"RUN_DIR={out}", flush=True)
