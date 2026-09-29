"""Extension X (block mask and fixed lambda; draft, not registered): the CPU preparation and the
decode of the two new BF fits, as pool-worker functions. torch-free.

Plan: docs/plans/2026-09-29-gpu-instrument-extension-x-plan.md (draft for review).
Built on prep.py (G7's arm machinery: prep.init_arm_worker sets the arm module, its _w_init and
the degree terms in every worker; prep._TERMS, prep.arm(), prep.prepare_view, prep._svd_start4,
prep.outside_density); prep.py is not modified, and its registered path (prepare_key_compact,
decode_records) keeps refusing every mask but ko (D1 (a)).

  * mask "block" (the CPU's P.train(bank, MASKS["block"]) = harness.fit_bf(make_view(bank,
    BLOCK), r)): the same calls as prepare_key_compact, on the block view: N1 on the view and on
    its inner-fold training views, the logit and training grids, the held-out masks, the SVD
    start of bf_als per grid. Engine v3's fit_bf_all then chooses lambda as fit_bf does.
  * mask "ko1" (the CPU's train_fixed_lambda(BF:r, P, bank, 1.0): n1 = fit_n1(view on the ko
    mask), bf_als(_n1_logit_grid(n1), Y, M, r, 1.0, starts=STARTS)): only grid 0 is prepared (the
    whole ko view; no inner fold, no lambda choice), and its SVD start. Engine v3's
    solve_problems then fits it at lambda = 1 (ext_engine.fit_fixed_lambda_all).
The block-cell labels, the content of the present block cells and outside_density are taken as
prepare_key_compact takes them, so decode_records_ext scores a record exactly as the CPU arm's
_fit_one does. The N1 p on the block (for the BF-active classification) is the view's own N1:
the block view's N1 for "block", the ko view's N1 for "ko1".

Keys: base views only (ext_scope.check_base_key: world:<family>:<j>); refused before any work.
Never reads, fits or scores a real block.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np  # noqa: E402

import prep  # noqa: E402  (G7: the arm machinery; not modified)
import instrument as I  # noqa: E402
import ext_scope as XS  # noqa: E402

H = prep.H


def prepare_key_ext(key, mask):
    """Pool worker: the preparation of one base view for mask "block" or "ko1"."""
    XS.check_base_key(key)
    XS.check_mask(mask)
    K = prep.arm()
    bank = K.build_bank(key, prep._TERMS["t"], True)
    view = H.make_view(bank, K.MASKS["block" if mask == "block" else "ko"])
    if mask == "block":
        pv = prep.prepare_view(view)
        n1 = pv["n1"]
        O = np.concatenate([pv["O"][None], pv["Oi"]])       # grid 0: whole view; 1..: folds
        M = np.concatenate([pv["M"][None], pv["Mi"]])
        Y = pv["Y"]
        test = np.concatenate([np.zeros((1, 65, 65), bool), pv["test"]])
        n_folds = len(pv["folds"])
    else:
        n1 = H.fit_n1(view)                                  # train_fixed_lambda's fit_n1
        Mg, Y = H._grid(view)
        O = H._n1_logit_grid(n1)[None]
        M = Mg[None]
        test = np.zeros((1, 65, 65), bool)
        n_folds = 0
    A4 = np.empty((len(O), 65, 4))
    B4 = np.empty((len(O), 65, 4))
    for i in range(len(O)):
        A4[i], B4[i] = prep._svd_start4(O[i], Y, M[i])
    bc = K.BLOCK_CELLS
    y_block = bank.exists[bc[:, 0], bc[:, 1]].copy()
    block_content = {(int(s), int(t)): bank.content[(int(s), int(t))]
                     for s, t in bc.tolist() if bank.exists[s, t]}
    p_n1 = np.asarray(K._pred("N1").decode(n1, bc)["p_exist"], np.float64)
    return {"key": key, "mask": mask, "n1": n1, "O": O, "M": M.astype(bool),
            "Y": Y.astype(bool), "test": test, "A4": A4, "B4": B4, "n_folds": n_folds,
            "y_block": y_block, "block_content": block_content,
            "outside_density": prep.outside_density(bank), "p_n1": p_n1}


def decode_records_ext(task):
    """Pool worker (G4 / G6 for extension X): BF_r fits decoded through the harness's own decode
    and scored by harness.score as the CPU arm's _fit_one scores them, as records of the arm's
    store schema under the key "<bank>||<mask>||BF:<r>"; beside each, the sha256 of the raw
    float64 U, V, lambda and of the decoded p (V1's scheme)."""
    r, mask, items = task
    XS.check_mask(mask)
    K = prep.arm()
    P = K._pred(f"BF:{r}")
    out = []
    for key, data, y_block, block_content, od in items:
        rk = XS.record_key(key, mask, r)
        dec = P.decode(data, K.BLOCK_CELLS)
        p = np.asarray(dec["p_exist"], np.float64)
        sb = H.Bank(f"score.{key}", block_content)
        y = sb.exists[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]]
        assert np.array_equal(y, y_block)
        sc = H.score(dec, sb, K.BLOCK_CELLS)
        rec = {"p": p.tolist(), "y": y.tolist(), "lam": float(np.asarray(data["bf_lambda"])[0]),
               "score": {k: sc[k] for k in ("existence", "offset", "counts", "sign", "sign_n",
                                            "n_ne")},
               "outside_density": float(od)}
        hashes = {"U": I.array_sha256(data["bf_U"]), "V": I.array_sha256(data["bf_V"]),
                  "lambda": I.array_sha256(data["bf_lambda"]), "p": I.array_sha256(p)}
        out.append((rk, rec, hashes))
    return out
