"""CPU-side preparation for the GPU instrument, runnable in a small process pool.

For one bank key (synthetic worlds only: "world:<family>:<j>" with an optional "|sh:<sd>"), this
builds the bank exactly as the CPU instrument does (knockout_regrow.build_bank with
synthetic_only=True, which refuses any "real" key), takes its knockout view, and computes every
input that fit_bf (and rule #2.1's fit_existence) derives from the view before the ALS starts:
N1 on the whole view and on each inner-fold training subview (harness.fit_n1, the exact CPU call),
the N1 logit grids (harness._n1_logit_grid), the training grids (harness._grid) and the held-out
masks. These are the same calls, in the same order, as harness.fit_bf; nothing is reimplemented.

This module imports numpy, harness and knockout_regrow only (no torch), so pool workers start
fast. It sets one BLAS thread per process before numpy loads, as knockout_regrow does.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import pathlib  # noqa: E402
import sys  # noqa: E402

import numpy as np  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
C6 = HERE.parent
for _p in (str(C6), str(C6 / "checks")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import harness as H          # noqa: E402  (read-only import)
import knockout_regrow as K  # noqa: E402  (read-only import; its arms live under __main__)

_TERMS = {}


def init_worker(terms):
    _TERMS["t"] = terms


def prepare_view(view, n1_full=None):
    """Everything fit_bf computes from the view before its first bf_als call, as a dict of
    numpy arrays. `folds` is in fit_bf's order (sorted fold ids)."""
    n1 = H.fit_n1(view) if n1_full is None else n1_full
    M, Y = H._grid(view)
    inner = H.inner_folds(view)
    folds = sorted(set(inner.tolist()))
    Oi, Mi, test = [], [], []
    for f in folds:
        keep = inner != f
        sv_ = H.subview(view, keep)
        Oi.append(H._n1_logit_grid(H.fit_n1(sv_)))
        m_, _ = H._grid(sv_)
        Mi.append(m_)
        t = np.zeros((65, 65), bool)
        hc = view.cells[~keep]
        t[hc[:, 0], hc[:, 1]] = True
        test.append(t)
    return {"n1": n1, "O": H._n1_logit_grid(n1), "M": M, "Y": Y, "folds": folds,
            "Oi": np.stack(Oi), "Mi": np.stack(Mi), "test": np.stack(test)}


def prepare_key(key, mask="ko"):
    """Worker entry point: build the bank for `key` and prepare its view under `mask`."""
    if key.split("|")[0] == "real":
        raise RuntimeError("REFUSED: the GPU instrument never builds the real bank")
    bank = K.build_bank(key, _TERMS["t"], True)
    view = H.make_view(bank, K.MASKS[mask])
    out = prepare_view(view)
    out["key"] = key
    out["y_block"] = bank.exists[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]].copy()
    return out


# ------------------------------------------------------------------------------------------
# Rule #2.1: the CPU part of its fit, after the (GPU) existence fit. Worker side, torch-free.

def init_rule_worker(terms):
    """As the registered run's workers: knockout_regrow._w_init(10, terms, True) sets
    harness.STARTS = 10 and loads rule #2.1 through harness.load_rule into this process."""
    _TERMS["t"] = terms
    K._w_init(10, terms, True)


def install_existence(P, ex, cells, exists, starts):
    """Make P.fit (a rule #2.1 module object loaded by harness.load_rule in THIS process) use
    the precomputed existence fit `ex` for the one view whose cells/exists equal the given
    arrays; any other view, starts value or option raises. fit.py on disk is not touched; only
    the name fit_existence in this process's module object is rebound. Returns a restore
    function."""
    g = P.fit.__globals__
    orig = g["fit_existence"]
    rounds_default = g["ROUNDS"]

    def fit_existence_from_gpu(view, st, rounds=rounds_default, x_on=True):
        if not (st == starts and rounds == rounds_default and x_on is True
                and np.array_equal(view.cells, cells) and np.array_equal(view.exists, exists)):
            raise RuntimeError("GPU existence fit does not belong to this view/options")
        return ex

    g["fit_existence"] = fit_existence_from_gpu

    def restore():
        g["fit_existence"] = orig
    return restore


def rule_post_key(args):
    """(bank key, existence dict) -> the rule's own fit() with that existence fit, decoded and
    scored exactly as knockout_regrow._w_group does for the 'ko' mask."""
    import time
    key, ex = args
    if key.split("|")[0] == "real":
        raise RuntimeError("REFUSED: the GPU instrument never builds the real bank")
    t0 = time.time()
    bank = K.build_bank(key, _TERMS["t"], True)
    P = K._pred("rule")
    view = H.make_view(bank, K.MASKS["ko"])
    restore = install_existence(P, ex, view.cells, view.exists, H.STARTS)
    try:
        data = P.train(bank, K.MASKS["ko"])
    finally:
        restore()
    lam = float(P.fit.__globals__["LAST_FIT"]["lambda"])
    dec = P.decode(data, K.BLOCK_CELLS)
    sc = H.score(dec, bank, K.BLOCK_CELLS)
    return {"key": key, "p": np.asarray(dec["p_exist"], np.float64),
            "y": bank.exists[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]].copy(), "lam": lam,
            "score": {k: sc[k] for k in ("existence", "offset", "counts", "sign", "sign_n",
                                         "n_ne")},
            "secs": time.time() - t0}


# ------------------------------------------------------------------------------------------
# Compact preparation for the streamed pipeline (gpu_bf3 / run_pipeline.py). Same calls as
# prepare_view; in addition the SVD start of harness.bf_als is computed here, once per grid:
# bf_als's E, u, sv, vt depend on (O, Y, M) only, not on r or lambda, so the rank-r start
# U0 = u[:, :r] * sqrt(sv[:r]) is, element for element, the first r columns of the rank-4 one.
# Grids are stored as bool where they are 0/1 (M, Y, test) to save memory.

def _svd_start4(O, Y, M):
    E = np.where(M > 0, Y - H._sig(O), 0.0)
    u, sv, vt = np.linalg.svd(E)
    return u[:, :4] * np.sqrt(sv[:4]), vt[:4].T * np.sqrt(sv[:4])


def prepare_key_compact(key, mask="ko"):
    if key.split("|")[0] == "real":
        raise RuntimeError("REFUSED: the GPU instrument never builds the real bank")
    bank = K.build_bank(key, _TERMS["t"], True)
    view = H.make_view(bank, K.MASKS[mask])
    pv = prepare_view(view)
    O = np.concatenate([pv["O"][None], pv["Oi"]])            # grid 0: whole view; 1..: folds
    M = np.concatenate([pv["M"][None], pv["Mi"]])
    A4 = np.empty((len(O), 65, 4))
    B4 = np.empty((len(O), 65, 4))
    for i in range(len(O)):
        A4[i], B4[i] = _svd_start4(O[i], pv["Y"], M[i])
    test = np.concatenate([np.zeros((1, 65, 65), bool), pv["test"]])
    return {"key": key, "n1": pv["n1"], "O": O, "M": M.astype(bool), "Y": pv["Y"].astype(bool),
            "test": test, "A4": A4, "B4": B4, "n_folds": len(pv["folds"]),
            "y_block": bank.exists[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]].copy()}


def decode_compare(task):
    """Pool worker: decode BF_r fits through the harness's own decode and compare with the
    stored reference entries (passed in; the worker never opens a store)."""
    r, items = task
    P = K._pred(f"BF:{r}")
    rows = []
    for key, data, refv, y_block in items:
        dec = P.decode(data, K.BLOCK_CELLS)
        p = np.asarray(dec["p_exist"], np.float64)
        pr = np.asarray(refv["p"], np.float64)
        y = np.asarray(refv["y"], bool)
        ag, ar = K.auc(p, y), K.auc(pr, y)
        rows.append({"key": f"{key}||ko||BF:{r}", "r": r, "y_match": bool((y_block == y).all()),
                     "lam_gpu": float(data["bf_lambda"][0]), "lam_ref": refv["lam"],
                     "auc_gpu": ag, "auc_ref": ar,
                     "auc_diff": None if ag is None or ar is None else abs(ag - ar),
                     "max_abs_p_diff": float(np.max(np.abs(p - pr))),
                     "p_bit_equal": bool(np.array_equal(p, pr)),
                     "label_mismatches": int(np.sum((p >= 0.5) != (pr >= 0.5))),
                     "ref_secs": refv["secs"]})
    return rows
