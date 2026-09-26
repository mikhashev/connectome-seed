"""CPU-side preparation for the GPU instrument, runnable in a small process pool.

For one bank key (synthetic worlds only: "world:<family>:<j>" with an optional "|sh:<sd>"), this
builds the bank exactly as the CPU instrument does (the arm module's build_bank with
synthetic_only=True, which refuses any "real" key), takes its knockout view, and computes every
input that fit_bf (and rule #2.1's fit_existence) derives from the view before the ALS starts:
N1 on the whole view and on each inner-fold training subview (harness.fit_n1, the exact CPU call),
the N1 logit grids (harness._n1_logit_grid), the training grids (harness._grid) and the held-out
masks. These are the same calls, in the same order, as harness.fit_bf; nothing is reimplemented.

This module imports numpy, harness and the arm module only (no torch), so pool workers start
fast. It sets one BLAS thread per process before numpy loads, as knockout_regrow does.

G7 of the GPU instrument registration (docs/plans/2026-09-26-gpu-instrument-registration.md,
revision 1.4), the arm adapter: the arm's module (and lobe) is given to the worker initializer
(init_arm_worker) instead of being imported here directly. Block A's script, knockout_regrow, is
the default arm, loaded on first use, so the unregistered v2 drivers (validate_shuffles.py,
validate_rule.py) and run_pipeline.py keep working. An arm module is driven through A's interface:
set_lobe(lobe), degree_terms(), build_bank(key, terms, synthetic_only), _w_init(starts, terms,
synthetic_only), MASKS, BLOCK, BLOCK_CELLS, _pred. An arm whose script has another interface is
reached through an adapter module named in ARM_ADAPTERS; the male CNS arm's script
(knockout_regrow_male_cns) is reached through male_arm.py (V8 only), which calls the male script's
own functions as its own synthetic pool does. For an arm module other than A's:
  * set_lobe(lobe) is called if a lobe is given (a module without it refuses a lobe; the male
    adapter refuses no lobe);
  * the module's _w_init(10, terms, True) runs in every worker, as the registered run's workers
    (the male adapter: the male _w_init with the lobe, the restriction and no real block);
  * restrict_to_placed_grid() is called as well if the module defines it (idempotent), so the
    restriction holds in every worker whatever _w_init does;
  * outside_density(bank), if the module defines it (the male S6/S14: the placed outside cells),
    replaces A's bank.exists[~BLOCK].mean();
  * worker_state(), if the module defines it, is recorded by worker_record (G2).
The registered path (prepare_key_compact, decode_records) accepts only the keys of R6
(instrument.check_key): world:<family>:<j> and world:<family>:<j>|sh:<sd>.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import importlib  # noqa: E402
import pathlib  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402

import numpy as np  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
C6 = HERE.parent
for _p in (str(HERE), str(C6), str(C6 / "checks")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import harness as H          # noqa: E402  (read-only import)
import instrument as I       # noqa: E402  (torch-free: key refusals, hashes)

_TERMS = {}
_ARM = {"mod": None, "name": None, "lobe": None, "adapter": None, "poisoned": False,
        "worker_init": None}
DEFAULT_ARM = "knockout_regrow"
# G7: arm scripts whose interface is not A's, and the adapter module that gives them A's. The male
# CNS arm needs a lobe; its adapter is used by V8 only (gpu_stage.refusals).
ARM_ADAPTERS = {"knockout_regrow_male_cns": "male_arm"}
ARMS_NEEDING_A_LOBE = ("knockout_regrow_male_cns",)


def set_arm(name=DEFAULT_ARM, lobe=None):
    """G7: load the arm module by name (read-only import; through its adapter if ARM_ADAPTERS
    names one) and select its lobe."""
    adapter = ARM_ADAPTERS.get(name)
    if name in ARMS_NEEDING_A_LOBE and lobe is None:
        raise RuntimeError(f"REFUSED (G7): arm {name} needs a lobe (--lobe)")
    mod = importlib.import_module(adapter or name)
    if lobe is not None:
        if not hasattr(mod, "set_lobe"):
            raise RuntimeError(f"REFUSED (G7): arm module {name} has no set_lobe(); the adapter "
                               "cannot select a lobe")
        mod.set_lobe(lobe)
    _ARM.update(mod=mod, name=name, lobe=lobe, adapter=adapter)
    return mod


def arm():
    if _ARM["mod"] is None:
        set_arm(DEFAULT_ARM, None)
    return _ARM["mod"]


def restrict_grid(mod):
    """The arm's grid restriction (the male draft's S5), if it has one; A's arm has none."""
    if hasattr(mod, "restrict_to_placed_grid"):
        mod.restrict_to_placed_grid()
        return True
    return False


def poison_real_block():
    """T-G5 / V7 (validation only): flip the 64 block cells of harness.REAL in this process.
    A present block cell loses its content; an absent one gains a dummy content. Any code path
    that read a block cell of REAL would change its result (or fail)."""
    K = arm()
    content = H.REAL.content                     # the same dict as H.REAL_CONTENT
    flipped = {"removed": 0, "added": 0}
    for s, t in K.BLOCK_CELLS.tolist():
        k = (int(s), int(t))
        if k in content:
            del content[k]
            H.REAL.exists[k] = False
            flipped["removed"] += 1
        else:
            content[k] = {"offsets": {(0, 0): 1.0}, "hull": [], "sign": 1}
            H.REAL.exists[k] = True
            flipped["added"] += 1
    _ARM["poisoned"] = True
    return flipped


def outside_density(bank):
    K = arm()
    if hasattr(K, "outside_density"):
        return float(K.outside_density(bank))
    return float(bank.exists[~K.BLOCK].mean())


def init_worker(terms):
    _TERMS["t"] = terms


def init_arm_worker(arm_name, lobe, terms, poison=False):
    """G7: the registered GPU stage's pool initializer: the arm module (and lobe), its worker
    init as the registered run's workers (_w_init(10, terms, True): harness.STARTS = 10, rule #2.1
    loaded through harness.load_rule), its grid restriction, and (V7 / T-G5 only) the poison."""
    mod = set_arm(arm_name, lobe)
    _TERMS["t"] = terms
    mod._w_init(10, terms, True)
    restricted = restrict_grid(mod)
    flipped = poison_real_block() if poison else None
    _ARM["worker_init"] = {"arm": arm_name, "lobe": lobe, "adapter": _ARM["adapter"],
                           "grid_restricted": restricted,
                           "n_all_cells": int(len(H.ALL_CELLS)), "starts": H.STARTS,
                           "poisoned": flipped,
                           "arm_state": (mod.worker_state() if hasattr(mod, "worker_state")
                                         else None)}


def worker_record(_=None):
    """G2: the environment of one prep worker (numpy, BLAS, thread variables, the arm)."""
    rec = {"python": sys.version.split()[0], "numpy": np.__version__, "pid": os.getpid(),
           "thread_env_in_effect": {v: os.environ.get(v) for v in
                                    ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                                     "NUMEXPR_NUM_THREADS")},
           "arm": dict(_ARM["worker_init"] or {}),
           "degree_terms_digest": (I.degree_terms_digest(_TERMS["t"]) if "t" in _TERMS
                                   else None)}
    try:
        cfg = np.show_config(mode="dicts")
        rec["numpy_build"] = {k: cfg.get("Build Dependencies", {}).get(k)
                              for k in ("blas", "lapack")}
    except Exception as e:
        rec["numpy_build"] = {"error": repr(e)}
    try:
        import threadpoolctl
        rec["blas_at_run_time"] = [{**i, "filepath": os.path.basename(i.get("filepath") or "")}
                                   for i in threadpoolctl.threadpool_info()]
    except Exception as e:
        rec["blas_at_run_time"] = {"error": repr(e)}
    return rec


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
    K = arm()
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
# Unregistered (D13); kept for validate_rule.py.

def init_rule_worker(terms):
    """As the registered run's workers: knockout_regrow._w_init(10, terms, True) sets
    harness.STARTS = 10 and loads rule #2.1 through harness.load_rule into this process."""
    _TERMS["t"] = terms
    arm()._w_init(10, terms, True)


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
    K = arm()
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
# Compact preparation for the streamed pipeline (gpu_bf3). Same calls as prepare_view; in
# addition the SVD start of harness.bf_als is computed here, once per grid: bf_als's E, u, sv,
# vt depend on (O, Y, M) only, not on r or lambda, so the rank-r start U0 = u[:, :r] * sqrt(sv[:r])
# is, element for element, the first r columns of the rank-4 one. Grids are stored as bool where
# they are 0/1 (M, Y, test) to save memory.

def _svd_start4(O, Y, M):
    E = np.where(M > 0, Y - H._sig(O), 0.0)
    u, sv, vt = np.linalg.svd(E)
    return u[:, :4] * np.sqrt(sv[:4]), vt[:4].T * np.sqrt(sv[:4])


def prepare_key_compact(key, mask="ko"):
    """The registered GPU stage's preparation of one bank (R6: world and world|sh keys only).
    Besides the grids and starts, it returns what the record of A's store schema needs from the
    bank (G4): the block labels, the content of the present block cells (all harness.score reads
    of a bank: exists and content on the 64 block cells), outside_density as A's _w_group
    computes it, and the N1 p on the block (the at-risk list's "p equals its view's N1 p")."""
    I.check_key(key)
    if mask != "ko":
        raise ValueError(f"REFUSED (D1 (a)): mask {mask!r}; the GPU fits the ko mask only")
    K = arm()
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
    bc = K.BLOCK_CELLS
    y_block = bank.exists[bc[:, 0], bc[:, 1]].copy()
    block_content = {(int(s), int(t)): bank.content[(int(s), int(t))]
                     for s, t in bc.tolist() if bank.exists[s, t]}
    p_n1 = np.asarray(K._pred("N1").decode(pv["n1"], bc)["p_exist"], np.float64)
    return {"key": key, "n1": pv["n1"], "O": O, "M": M.astype(bool), "Y": pv["Y"].astype(bool),
            "test": test, "A4": A4, "B4": B4, "n_folds": len(pv["folds"]),
            "y_block": y_block, "block_content": block_content,
            "outside_density": outside_density(bank), "p_n1": p_n1}


def decode_records(task):
    """G4 / G6, pool worker: BF_r fits of the GPU decoded through the harness's own decode
    (Predictor.decode: the float32 cast of every float array), scored by harness.score exactly
    as A's _w_group scores a ko fit, as records of A's store schema (p, y, lam, score,
    outside_density; secs is filled by the driver). Beside each record, outside it: the sha256
    of the raw float64 U, V, lambda and of the decoded p (G6). The score reads only the 64 block
    cells of the bank, rebuilt here from their labels and content (a Bank whose other cells are
    absent gives the same y and the same score)."""
    r, items = task
    K = arm()
    P = K._pred(f"BF:{r}")
    out = []
    for key, data, y_block, block_content, od in items:
        I.check_key(key)
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
        out.append((I.bf_record_key(key, r), rec, hashes))
    return out


def decode_compare(task):
    """Pool worker (unregistered run_pipeline.py): decode BF_r fits through the harness's own
    decode and compare with the stored reference entries (passed in; the worker never opens a
    store)."""
    K = arm()
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
