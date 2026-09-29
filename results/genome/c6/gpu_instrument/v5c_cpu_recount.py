"""V5 (c) of the GPU instrument registration (revision 1.5 draft, Zcode's review of 2026-09-29):
a cheap float64 CPU recount of M3's five differing base fits and five controls. CPU only,
tools/.venv, one BLAS thread; no torch, no GPU. A statement, never a gate (non-blocking).

For each fit (A's base view, ko mask, BF_1, at its pinned lambda), with the harness's own calls:
  (i)   the registered fit: harness.bf_als at BF_TOL = 1e-6, decoded; must equal the pinned p
        bit for bit (the recount reproduces the reference);
  (ii)  the same fit with the Newton stop tightened to BF_TOL = 1e-8 and 1e-10: the float64
        change of the logit's BF term U V^T on the 64 block cells, and whether the decoded p
        moves. This measures the optimiser's own stopping envelope: how far the float64 answer
        sits from where a stricter stop takes it;
  (iv)  where V1's first GPU run is present (its raw_fits_gpu.json.gz, read only), each variant's
        decoded p against the GPU p: max |dp| and bit-equality;
  (iii) the float32 cast margin of U and V (decode casts every float array to float32): for each
        entry, its distance to the nearest float32 rounding boundary in float32 steps (0 = on
        a boundary, 0.5 = at a representable value); the fit's smallest margin.
The five differed from the CPU by 1.4e-9 to 3.8e-8 in the float64 accessor (M5) and by one or
more float32 steps after decode (M3). If the stopping envelope of (ii) is of that size on the
five and orders of magnitude smaller on the controls, the differences sit inside the optimiser's
own envelope, which any change of reduction order can move; that is the reading (ii) tests.

Usage: tools/.venv/Scripts/python.exe v5c_cpu_recount.py --out <dir outside every reference>
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import json  # noqa: E402
import pathlib  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402

import numpy as np  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import instrument as I  # noqa: E402
import knockout_regrow as K  # noqa: E402
import harness as H  # noqa: E402

FIVE = ["world:M1.0:0", "world:M1.0:4", "world:M0.75:0", "world:M0.85:0", "world:M0.85:2"]
CONTROLS = ["world:R:0", "world:R:1", "world:R:2", "world:R:3", "world:R:4"]   # V5 (b)'s
TOLS = (1e-8, 1e-10, 1e-12)
V1_RUN = I.DATA_ROOT / "V1_run_20260926T132024Z_a0e16b696389"


def cast_margin(x):
    """Smallest distance, in float32 steps, from any entry of x to a float32 rounding boundary."""
    x = np.asarray(x, np.float64).ravel()
    f = x.astype(np.float32).astype(np.float64)
    up = np.nextafter(x.astype(np.float32), np.float32(np.inf)).astype(np.float64)
    dn = np.nextafter(x.astype(np.float32), np.float32(-np.inf)).astype(np.float64)
    nb = np.where(x >= f, up, dn)
    step = np.abs(nb - f)
    mid = (f + nb) / 2
    m = np.abs(mid - x) / np.where(step > 0, step, 1.0)
    return float(m.min()), float(np.abs(mid - x).min())


def fit_one(bank, lam, tol):
    saved = H.BF_TOL
    H.BF_TOL = tol
    try:
        view = H.make_view(bank, K.MASKS["ko"])
        n1 = H.fit_n1(view)
        M, Y = H._grid(view)
        U, V = H.bf_als(H._n1_logit_grid(n1), Y, M, 1, lam)
    finally:
        H.BF_TOL = saved
    n1.update({"bf_U": U, "bf_V": V, "bf_lambda": np.array([float(lam)])})
    p = np.asarray(K._pred("BF:1").decode(n1, K.BLOCK_CELLS)["p_exist"], np.float64)
    bc = K.BLOCK_CELLS
    Z = (U @ V.T)[bc[:, 0], bc[:, 1]]
    return {"p": p, "Z": Z, "U": U, "V": V}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    why = I.out_dir_refusal(out)
    if why:
        raise SystemExit(why)
    chk = K.check_prerun_files()
    if not chk["passed"]:
        raise SystemExit(f"REFUSED: pinned pre-run folder does not verify: {chk['reason']}")
    ref = I.read_store(pathlib.Path(K.PRERUN_DIR) / "raw_fits.json.gz")
    t0 = time.time()
    terms = K.degree_terms()
    K._w_init(10, terms, True)
    gpu = (I.read_store(V1_RUN / "raw_fits_gpu.json.gz")
           if (V1_RUN / "raw_fits_gpu.json.gz").is_file() else None)
    rows = []
    for bk in FIVE + CONTROLS:
        rk = f"{bk}||ko||BF:1"
        lam = float(ref[rk]["lam"])
        bank = K.build_bank(bk, terms, True)
        base = fit_one(bank, lam, H.BF_TOL)
        pr = np.asarray(ref[rk]["p"], np.float64)
        row = {"key": rk, "group": "M3 five" if bk in FIVE else "control", "lam": lam,
               "registered_fit_equals_pinned": bool(np.array_equal(base["p"], pr)),
               "cast_margin_U_V_float32_steps": cast_margin(np.concatenate(
                   [base["U"].ravel(), base["V"].ravel()]))[0],
               "cast_margin_U_V_abs": cast_margin(np.concatenate(
                   [base["U"].ravel(), base["V"].ravel()]))[1],
               "tighter_stop": {}}
        pg = None if gpu is None else np.asarray(gpu[rk]["p"], np.float64)
        if pg is not None:
            row["gpu_V1"] = {"registered_fit": {"max_abs_dp": float(np.max(np.abs(base["p"] - pg))),
                                                "bit_equal": bool(np.array_equal(base["p"], pg))}}
        for tol in TOLS:
            t = fit_one(bank, lam, tol)
            if pg is not None:
                row["gpu_V1"][f"{tol:g}"] = {"max_abs_dp": float(np.max(np.abs(t["p"] - pg))),
                                             "bit_equal": bool(np.array_equal(t["p"], pg))}
            row["tighter_stop"][f"{tol:g}"] = {
                "max_abs_dZ_float64": float(np.max(np.abs(t["Z"] - base["Z"]))),
                "max_abs_dp_decoded": float(np.max(np.abs(t["p"] - base["p"]))),
                "decoded_p_bit_equal": bool(np.array_equal(t["p"], base["p"]))}
        rows.append(row)
        print(json.dumps(row), flush=True)
    summ = {}
    for g in ("M3 five", "control"):
        rs = [r for r in rows if r["group"] == g]
        summ[g] = {tol: {"max_abs_dZ_range": [min(r["tighter_stop"][tol]["max_abs_dZ_float64"]
                                                  for r in rs),
                                              max(r["tighter_stop"][tol]["max_abs_dZ_float64"]
                                                  for r in rs)],
                         "decoded_p_moved": sum(not r["tighter_stop"][tol]["decoded_p_bit_equal"]
                                                for r in rs)}
                   for tol in (f"{x:g}" for x in TOLS)}
        summ[g]["all_reproduce_pinned"] = all(r["registered_fit_equals_pinned"] for r in rs)
        summ[g]["cast_margin_min_steps"] = min(r["cast_margin_U_V_float32_steps"] for r in rs)
    rep = {"what": "V5 (c): float64 CPU recount of M3's five and five controls (statement)",
           "reference": {"path": str(pathlib.Path(K.PRERUN_DIR) / "raw_fits.json.gz"),
                         "check_prerun_files": chk["reason"]},
           "registered_BF_TOL": H.BF_TOL, "tighter_tols": list(TOLS),
           "secs": time.time() - t0, "summary": summ, "rows": rows}
    out.mkdir(parents=True, exist_ok=True)
    I.write_json(out / "v5c.json", rep)
    print(json.dumps({"summary": summ, "secs": rep["secs"]}, indent=1), flush=True)


if __name__ == "__main__":
    main()
