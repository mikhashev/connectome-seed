"""Extension X (block mask and fixed lambda; draft, not registered): the fits on engine v3.

Plan: docs/plans/2026-09-29-gpu-instrument-extension-x-plan.md (draft for review).
No new arithmetic: both fits are engine v3's own functions (gpu_bf3.py is not modified).
  * "block": gpu_bf3.fit_bf_all on a GridStore of block-view preparations (ext_prep): the nested
    lambda choice of harness.fit_bf (10 folds x 5 lambdas, ties within 1e-9 to the larger), then
    the final bf_als at the chosen lambda.
  * "ko1": gpu_bf3.solve_problems on grid 0 of every bank at lambda = 1 (want="uv"): the
    harness.bf_als call of train_fixed_lambda (offset = the ko view's N1 logit grid, k = STARTS).
run_core() is the part of the driver between the preparations and the records, written as a
function so that it runs on the torch CPU device in the tests (GPU_INSTRUMENT_DEVICE=cpu) on
fixture banks; the driver (ext_gpu_stage.py) wraps it with the registered driver's checks.
"""
import time

import numpy as np

import gpu_bf3
import ext_scope as XS


def fit_fixed_lambda_all(S, r, lam, starts, row_chunk=40000):
    """train_fixed_lambda's bf_als for every bank of the store (grid 0), at lambda `lam`."""
    nb = S.n_banks
    U, V = gpu_bf3.solve_problems(S, np.arange(nb) * S.per, np.full(nb, float(lam)), r, starts,
                                  row_chunk, want="uv")
    return np.full(nb, float(lam)), U, V


def run_core(keys, preps, mask, ranks, starts, row_chunk, decode_submit, sync=lambda: None,
             log=print):
    """Fit every bank of `preps` (ext_prep.prepare_key_ext outputs, in key order) on `mask` at
    every rank; hand each rank's fits, grouped by world, to decode_submit((r, mask, items)),
    which returns a future-like object (or a list) of ext_prep.decode_records_ext output.
    Returns (results, info): results a list of (r, (record_key, record, hashes)); info the
    per-rank seconds, lambda counts and near-ties (block only)."""
    XS.check_mask(mask)
    n_folds = preps[0]["n_folds"]
    if any(pp["n_folds"] != n_folds for pp in preps):
        raise SystemExit("REFUSED: banks with different numbers of inner folds")
    if [pp["key"] for pp in preps] != list(keys):
        raise SystemExit("REFUSED: the preparations are not in key order")
    S = gpu_bf3.GridStore(preps)
    sync()
    pending, rank_secs, near_ties, lam_by_rank = [], {}, {}, {}
    for r in ranks:
        t1 = time.time()
        if mask == "block":
            lam, U, V, _ll, near = gpu_bf3.fit_bf_all(S, n_folds, r, starts=starts,
                                                      row_chunk=row_chunk)
            near_ties[r] = near
        else:
            lam, U, V = fit_fixed_lambda_all(S, r, XS.FIXED_LAMBDA, starts, row_chunk)
            near_ties[r] = None                          # no lambda choice at a fixed lambda
        sync()
        rank_secs[r] = time.time() - t1
        lam_by_rank[r] = {str(x): int((lam == x).sum()) for x in sorted(set(lam.tolist()))}
        by_world = {}
        for i, (key, pp) in enumerate(zip(keys, preps)):
            data = dict(pp["n1"])
            data.update({"bf_U": U[i], "bf_V": V[i], "bf_lambda": np.array([float(lam[i])])})
            by_world.setdefault(key, []).append(
                (key, data, pp["y_block"], pp["block_content"], pp["outside_density"]))
        pending += [(r, decode_submit((r, mask, items))) for items in by_world.values()]
        log(f"BF_{r} [{mask}]: {len(keys)} banks in {rank_secs[r]:.2f}s; lambda "
            f"{lam_by_rank[r]}; near-ties {near_ties[r]}")
    results = []
    for r, f in pending:
        out = f.result() if hasattr(f, "result") else f
        results += [(r, x) for x in out]
    return results, {"rank_secs": rank_secs, "near_ties": near_ties, "lambda_by_rank": lam_by_rank,
                     "n_folds": n_folds, "per": S.per}
