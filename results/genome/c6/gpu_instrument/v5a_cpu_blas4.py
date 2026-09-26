"""V5 (a) of the GPU instrument registration (revision 1.3, section 7): CPU only, tools/.venv.

harness.fit_bf on the 180 base views of A's 45 worlds (BF_1..BF_4, ko mask, k = 10), fitted by
A's own worker code (knockout_regrow._w_init / run_groups / _w_group, read-only imports) with
OPENBLAS_NUM_THREADS=4 exported before launch (another BLAS reduction order), compared with A's
pinned pre-run store (after check_prerun_files). No GPU, no torch. The launcher (validation.py V5)
sets OPENBLAS_NUM_THREADS=4 in the environment; this script refuses if it did not.

Usage: OPENBLAS_NUM_THREADS=4 tools/.venv/Scripts/python.exe v5a_cpu_blas4.py --out <dir>
"""
import os

FOUND = os.environ.get("OPENBLAS_NUM_THREADS")

import argparse  # noqa: E402
import json  # noqa: E402
import pathlib  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import instrument as I  # noqa: E402
import knockout_regrow as K  # noqa: E402  (its setdefault keeps the exported 4)
import numpy as np  # noqa: E402


def _blas_info(_=None):
    import threadpoolctl
    return [{k: i.get(k) for k in ("internal_api", "num_threads", "version")}
            for i in threadpoolctl.threadpool_info()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    if FOUND != "4":
        raise SystemExit(f"REFUSED (V5 (a)): OPENBLAS_NUM_THREADS found {FOUND!r}; export 4 "
                         "before launch")
    out = pathlib.Path(a.out)
    refusal = I.out_dir_refusal(out)
    if refusal:
        raise SystemExit(refusal)
    out.mkdir(parents=True, exist_ok=True)
    chk = K.check_prerun_files()
    if not chk["passed"]:
        raise SystemExit(f"REFUSED: pinned pre-run folder does not verify: {chk['reason']}")
    ref = I.read_store(pathlib.Path(K.PRERUN_DIR) / "raw_fits.json.gz")
    t0 = time.time()
    terms = K.degree_terms()
    banks = [f"world:{w['family']}:{w['j']}" for w in K.world_specs()]
    groups = [[(bk, "ko", pk) for pk in K.BF_KEYS] for bk in banks]
    res = K.run_groups(groups, a.workers, (10, terms, True), "V5 (a) BF on base views, "
                       "OPENBLAS_NUM_THREADS=4")
    rows, moved = [], []
    for (bk, mk, pk), rec in sorted(res.items()):
        rk = f"{bk}||{mk}||{pk}"
        pr = np.asarray(ref[rk]["p"], np.float64)
        pg = np.asarray(rec["p"], np.float64)
        be = bool(np.array_equal(pr, pg))
        rows.append({"key": rk, "lam_ref": ref[rk]["lam"], "lam": rec["lam"], "bit_equal": be,
                     "max_abs_dp": float(np.max(np.abs(pr - pg)))})
        if not be:
            moved.append(rk)
    rep = {"what": "V5 (a): harness.fit_bf on the 180 base views, OPENBLAS_NUM_THREADS=4",
           "thread_env_found": {v: K.THREAD_ENV_FOUND[v] for v in K.THREAD_VARS},
           "thread_env_in_effect": {v: os.environ.get(v) for v in K.THREAD_VARS},
           "blas_main": _blas_info(), "machine_record": K.machine_record(),
           "reference": {"path": str(pathlib.Path(K.PRERUN_DIR) / "raw_fits.json.gz"),
                         "check_prerun_files": chk["reason"]},
           "fits": len(rows), "moved": moved, "n_moved": len(moved),
           "secs": time.time() - t0, "rows": rows}
    I.write_json(out / "v5a.json", rep)
    print(json.dumps({k: rep[k] for k in ("fits", "n_moved", "moved", "secs")}, indent=1),
          flush=True)


if __name__ == "__main__":
    main()
