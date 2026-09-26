"""G7, the arm adapter for the male CNS arm: V8 only, an unregistered cross-check.

GPU instrument registration docs/plans/2026-09-26-gpu-instrument-registration.md, revision 1.4,
section 7 (V8) and D11; the male arm's registration
docs/plans/2026-09-26-knockout-regrow-male-cns-arm-registration.md, revision 1.1, D13 (iii): the GPU
instrument may run the male worlds as a second, unregistered cross-check; its output is an input to
no gate, reference or registered value of the male arm, which stays on the CPU (its D13 (i)).

The male script (results/genome/c6/checks/knockout_regrow_male_cns.py, imported read-only as M; the
file is not modified) does not have A's interface, which prep and gpu_stage drive: it has
degree_terms(bank) (the lobe's bank as an argument), build_bank(key, ctx) (the worker's context
M._W), _w_init(starts, terms, synthetic_only, lobe, restrict, real_block), one bank per lobe,
restrict_to_placed_grid() and no set_lobe. prep.set_arm maps the arm name
"knockout_regrow_male_cns" to this module, which gives A's interface by calling the male script's
own functions, in the order its own --synthetic-only run calls them, and nothing else:

  set_lobe(lobe)            the lobe (L or R), and the seal guard below
  restrict_to_placed_grid() M.restrict_to_placed_grid() (S5: H.ALL_CELLS = the 3,025 placed cells)
  degree_terms()            as the male main (run_synthetic_only after common_checks): the
                            restriction, then M.degree_terms(M.load_male_bank(lobe)): N1 on the
                            lobe's knockout view on the placed grid, outside-block cells only, from
                            the lobe's pin-checked outside file (S14)
  _w_init(starts, terms, synthetic_only)
                            M._w_init(starts, terms, True, lobe, True, None): exactly the
                            initializer of the male pre-run's synthetic pool (run_synthetic:
                            init_args = (starts, terms, True, lobe, True, None)); it restricts the
                            grid and loads the lobe's outside bank and content pool in this process
  build_bank(key, terms, synthetic_only)
                            M.build_bank(key, M._W), the male _w_group's own call, after R6's key
                            check and a check that this process's M._W is the lobe's synthetic pool
                            on the placed grid, initialised with these terms
  outside_density(bank)     the male _fit_one's expression, bank.exists[~BLOCK & PLACED_GRID].mean()
                            (S6, S14: the 2,961 placed outside cells)
  null_patterns(y)          leg P's null inputs as the male evaluate_bank builds them, for the
                            comparator's p_P and p_P_rowcol (E2-III on a base view)
  worker_state()            what a prep worker records about this process (G2)
Every other name (MASKS, BLOCK, BLOCK_CELLS, BLOCK_NAMES, world_specs, _pred, auc, parity_D,
logit_of, auc_null, TAU, N_PERM, BF_KEYS, H, ...) is the male module's own (module __getattr__).

The seal. Nothing here calls open_sealed, verify_sealed_pins, parse_sealed, sealed_path or
real_bank, and no key that reaches M.build_bank can be "real" (I.check_key, R6), nor can a context
with a real block (M._W["real_block"] is None, M._W["syn"] is True, both checked). In addition,
set_lobe makes the seal unreachable in this process: M._UNSEAL["allowed"] = False (open_sealed
refuses) and M.SEALED_DIR points at a folder that does not exist (verify_sealed_pins, which does
not look at _UNSEAL, would fail to read rather than hash a file of the build folder). The module
object is changed in this process only; the male script on disk is not.
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
C6 = HERE.parent
for _p in (str(HERE), str(C6), str(C6 / "checks")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np  # noqa: E402

import instrument as I  # noqa: E402  (torch-free)
import knockout_regrow_male_cns as M  # noqa: E402  (read-only import; its runs live under __main__)

H = M.H
ARM_NAME = "knockout_regrow_male_cns"
ADAPTER = "male_arm"
# A folder that does not exist, so that no sealed-file path of this process names the build folder.
NO_SEALED_DIR = pathlib.Path(I.DATA_ROOT) / "male_arm_adapter_has_no_sealed_files"
_STATE = {"lobe": None}


def __getattr__(name):
    """Every name this adapter does not define is the male module's own."""
    try:
        return getattr(M, name)
    except AttributeError:
        raise AttributeError(f"module {__name__!r} (the male adapter) and the male script have no "
                             f"attribute {name!r}") from None


def seal_guard():
    """Make the seal unreachable in this process (see the module docstring)."""
    M._UNSEAL["allowed"] = False
    M.SEALED_DIR = NO_SEALED_DIR
    assert not NO_SEALED_DIR.exists(), NO_SEALED_DIR


def set_lobe(lobe):
    if lobe not in M.LOBES:
        raise RuntimeError(f"REFUSED (G7): lobe {lobe!r}; the male arm's lobes are {M.LOBES}")
    seal_guard()
    _STATE["lobe"] = lobe


def lobe():
    if _STATE["lobe"] is None:
        raise RuntimeError("REFUSED (G7): the male adapter has no lobe; prep.set_arm("
                           "'knockout_regrow_male_cns', lobe) selects it")
    return _STATE["lobe"]


def restrict_to_placed_grid():
    M.restrict_to_placed_grid()


def degree_terms():
    """N1's (c, a, b) on the lobe's knockout view on the placed grid, as the male main computes
    them (restriction first, then the lobe's outside bank, pin-checked)."""
    lb = lobe()
    M.restrict_to_placed_grid()
    return M.degree_terms(M.load_male_bank(lb))


def _w_init(starts, terms, synthetic_only):
    if synthetic_only is not True:
        raise RuntimeError("REFUSED (G7): the male adapter runs a synthetic pool only")
    seal_guard()
    M._w_init(starts, terms, True, lobe(), True, None)


def _check_pool(terms):
    W = M._W
    why = []
    if W.get("lobe") != _STATE["lobe"] or W.get("lobe") is None:
        why.append(f"the pool's lobe is {W.get('lobe')!r}, the adapter's {_STATE['lobe']!r}")
    if W.get("syn") is not True or W.get("real_block") is not None:
        why.append("the pool is not a synthetic pool (syn True, no real block)")
    if W.get("restrict") is not True or len(H.ALL_CELLS) != M.N_PLACED_CELLS:
        why.append(f"the grid is not restricted (len(H.ALL_CELLS) = {len(H.ALL_CELLS)})")
    if W.get("terms") is None or I.degree_terms_digest(terms) != I.degree_terms_digest(W["terms"]):
        why.append("the degree terms given differ from the terms the pool was initialised with")
    if M._UNSEAL["allowed"] or pathlib.Path(M.SEALED_DIR) != NO_SEALED_DIR:
        why.append("the seal guard is not in place")
    if why:
        raise RuntimeError("REFUSED (G7): " + "; ".join(why) + " (call _w_init first)")


def build_bank(key, terms, synthetic_only):
    """The bank of a world key (R6: world:<family>:<j>[|sh:<sd>]) as the male pool builds it."""
    I.check_key(key)
    if synthetic_only is not True:
        raise RuntimeError("REFUSED (G7): the male adapter builds synthetic banks only")
    _check_pool(terms)
    return M.build_bank(key, M._W)


def outside_density(bank):
    """S6, S14: as M._fit_one records it, over the 2,961 placed outside cells."""
    return float(bank.exists[~M.BLOCK & M.PLACED_GRID].mean())


def null_patterns(y):
    """(Yu, Yrc) of the male evaluate_bank: y[uniform_perms()] (default_rng(92000)) and
    rc_patterns(y, mode)["patterns"] (default_rng(92001), with the attempt cap). The comparator
    calls it with mode "real", whose patterns are the synthetic mode's; the two modes differ only
    when a chain hits the attempt cap (synthetic: the process exits; real: no patterns, and
    p_P_rowcol is None), which the male pre-run would already have stopped on."""
    y = np.asarray(y, bool)
    rc = M.rc_patterns(y, "real")
    return y[M.uniform_perms()], rc["patterns"]


def worker_state():
    """G2: the male pool of this process."""
    W = M._W
    return {"adapter": ADAPTER, "arm": ARM_NAME, "lobe": _STATE["lobe"],
            "pool_lobe": W.get("lobe"), "synthetic_only": W.get("syn"),
            "real_block_is_none": W.get("real_block") is None, "restrict": W.get("restrict"),
            "n_all_cells": int(len(H.ALL_CELLS)), "starts": H.STARTS,
            "content_pool_rows": None if W.get("pool") is None else len(W["pool"]),
            "unseal_allowed": bool(M._UNSEAL["allowed"]), "sealed_dir": str(M.SEALED_DIR),
            "sealed_dir_exists": pathlib.Path(M.SEALED_DIR).exists(),
            "male_script_sha256_lf": I.sha256_lf(M.__file__)}
