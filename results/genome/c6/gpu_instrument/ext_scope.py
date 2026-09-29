"""Extension X (block mask and fixed lambda; draft, not registered): scope, keys, references and
the reference census. torch-free; runs in tools/.venv.

Plan: docs/plans/2026-09-29-gpu-instrument-extension-x-plan.md (draft for review).
The registered instrument (revision 1.4, D1 (a)) fits BF_1..BF_4 on the ko mask only
(prep.prepare_key_compact refuses any other mask). Extension X would add two BF fits of the
knockout-and-regrow synthetic step, each validated by the V1 scheme (per-fit sha256 of U, V,
lambda and the decoded p, three fresh runs) and the V2 scheme (E1, E2-II, E2-III against a pinned
CPU store):
  * "block": BF_r trained on the block mask (MASKS["block"]: the block cells only), lambda chosen
    by fit_bf's nested scheme; the record the CPU writes as "<bank>||block||BF:<r>". It feeds
    ceiling_block, regrown_share_block and lambda_block (evaluate_bank).
  * "ko1": BF_r on the ko mask at the fixed lambda FIXED_LAMBDA = 1 (train_fixed_lambda: fit_n1 on
    the view, harness.bf_als at lambda 1, k = STARTS; no lambda choice); the record
    "<bank>||ko1||BF:<r>". It feeds auc_fixed_lambda1 and p_P_fixed_lambda1.
Both exist only on base views (world:<family>:<j>, never a shuffle, never |pc:, never real).
Rule #2.1's fixed-lambda fit (fit.LAMBDAS set to [1]) and its quantised decode are NOT in the
scope: the rule is CPU in the registered instrument (D1 (a), D13 (a)), its only port
(gpu_rule.py, engine v2) is unregistered and refused by the registered driver (G8), and even that
port leaves the quantisation (ExistQ, descend, refit_c), the offset library and decode.py on the
CPU (gpu_rule.py docstring; prep.rule_post_key).

References (read only; never written; G11 extended by EXT_REFERENCE_DIRS):
  * A: the pinned pre-run store synthetic_rev3_prerun/raw_fits.json.gz, after A's
    check_prerun_files (D4 (a)); 64 block cells.
  * B: the pinned block B pre-run store synthetic_blockB_prerun_20260927T211052Z_5f9cc51b9a24/
    raw_fits.json.gz, after block B's check_prerun_files; 40 block cells.
  * B's registered run's synthetic store flyvis65_blockB_20260928T143258Z_7a10d88ec95e/
    raw_fits.json.gz (its SHA256SUMS.txt line): a fresh CPU refit of every synthetic key, equal to
    the pre-run on p, lambda, labels and score (its stdout.log line 94); a witness that the
    reference reproduces, not a second reference. raw_fits_real.json.gz beside it is never opened.
"""
import json
import pathlib
import re
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
C6 = HERE.parent
for _p in (str(HERE), str(C6), str(C6 / "checks")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import instrument as I  # noqa: E402
import ext_census as XC  # noqa: E402

EXT_MASKS = ("block", "ko1")
RANKS = (1, 2, 3, 4)
FIXED_LAMBDA = 1.0                 # A and B: FIXED_LAMBDA = 1.0 (knockout_regrow.py:235, B :288)
BASE_KEY_RE = re.compile(r"^world:[A-Za-z][A-Za-z0-9.]*:[0-9]+$")

PRIVATE = I.ROOT.parent / "connectome-seed-data" / "knockout_regrow"
B_REGISTERED_DIR = PRIVATE / "flyvis65_blockB_20260928T143258Z_7a10d88ec95e"
B_REGISTERED_STORE_SHA256 = "55b240a7c0144a2d73860f10f78be84e7738977df547c70ad7c84fda50438fbc"
# G11 for extension X: B's pinned pre-run folder and B's registered run folder, besides
# instrument.reference_dirs() (which names A's and the male arm's folders only).
EXT_REFERENCE_DIRS = (PRIVATE / "synthetic_blockB_prerun_20260927T211052Z_5f9cc51b9a24",
                      B_REGISTERED_DIR)
ARMS = {"A": "knockout_regrow", "B": "knockout_regrow_block_b"}


def check_base_key(key):
    """Extension X accepts base views only: world:<family>:<j> (no |sh:, |pc:, |leak, real)."""
    I.check_key(key)
    if not BASE_KEY_RE.match(key):
        raise ValueError(f"REFUSED (X-R6): key {key!r}; block-mask and fixed-lambda records exist "
                         "only on base views world:<family>:<j>")
    return key


def check_mask(mask):
    if mask not in EXT_MASKS:
        raise ValueError(f"REFUSED (X): mask {mask!r}; extension X fits {EXT_MASKS} only (the ko "
                         "mask is the registered instrument's, D1 (a))")
    return mask


def record_key(bank_key, mask, r):
    return f"{check_base_key(bank_key)}||{check_mask(mask)}||BF:{int(r)}"


def planned(keys, mask, ranks=RANKS):
    """The planned record keys: for each rank in rank order, the keys in order (as gpu_stage)."""
    return [record_key(k, mask, r) for r in ranks for k in keys]


def ext_composition_digest(arm_module_name, mask, keys, starts, ranks):
    """The refusal digest of an extension-X run: sha256 over the arm module's name, the mask, the
    ordered key list, starts, the rank order and (ko1) the fixed lambda. Unlike
    instrument.composition_digest (keys, starts, ranks only), it binds the arm and the mask: the
    key strings world:<family>:<j> are the same in A, B and the male arm, and V1 and V8 (both
    lobes) carry the same registered digest a6a8a0df... for three different sets of banks."""
    import hashlib
    keys = [check_base_key(k) for k in keys]
    check_mask(mask)
    obj = {"extension": "X", "arm": str(arm_module_name), "mask": mask, "keys": keys,
           "starts": int(starts), "ranks": [int(r) for r in ranks],
           "fixed_lambda": FIXED_LAMBDA if mask == "ko1" else None}
    return hashlib.sha256(I._canon(obj).encode()).hexdigest()


def ext_out_dir_refusal(out):
    """G11 for extension X: instrument.out_dir_refusal, plus B's two folders."""
    why = I.out_dir_refusal(out)
    if why:
        return why
    target = pathlib.Path(out).resolve()
    for ref in EXT_REFERENCE_DIRS:
        ref = ref.resolve()
        if target == ref or target.is_relative_to(ref):
            return f"REFUSED (X-G11): {target} is a reference folder or inside one ({ref})"
    return None


def arm_module(arm):
    import importlib
    if arm not in ARMS:
        raise ValueError(f"REFUSED (X): arm {arm!r}; one of {sorted(ARMS)}")
    return importlib.import_module(ARMS[arm])


def load_reference(arm, which="pinned"):
    """(store, info): the arm's pinned pre-run store after its own check_prerun_files; or, for B
    with which="registered", B's registered run's synthetic store against its SHA256SUMS line."""
    K = arm_module(arm)
    if which == "pinned":
        chk = K.check_prerun_files()
        if not chk["passed"]:
            raise SystemExit(f"REFUSED (X, D4): {arm}'s pinned pre-run folder does not verify: "
                             f"{chk['reason']}")
        path = pathlib.Path(K.PRERUN_DIR) / "raw_fits.json.gz"
        want = K.PRERUN_SHA256["raw_fits.json.gz"]
    elif which == "registered" and arm == "B":
        path = B_REGISTERED_DIR / "raw_fits.json.gz"
        want = B_REGISTERED_STORE_SHA256
    else:
        raise ValueError(f"REFUSED (X): reference {which!r} for arm {arm!r}")
    got = I.sha256_file(path)
    if got != want:
        raise SystemExit(f"REFUSED (X): {path} sha256 {got}, expected {want}")
    return I.read_store(path), {"arm": arm, "which": which, "path": str(path), "sha256": got}


def base_keys_of(ref):
    """The base views of a store, in the arm's world_specs order is not needed: sorted by the
    order the store's ko N1 base records appear under world_specs is the driver's business; here
    the set, sorted."""
    return sorted({rk.split("||")[0] for rk in ref
                   if BASE_KEY_RE.match(rk.split("||")[0]) and rk.split("||")[1] == "ko"})


def n1_p_for(ref, rk):
    """The N1 p a fit is compared with for the BF-active classification: block -> the block
    view's N1 (block||N1); ko1 -> the ko view's N1 (ko||N1), whose logit grid is the fixed-lambda
    fit's offset."""
    bk, mk, _ = rk.split("||")
    n1 = ref.get(f"{bk}||{'block' if mk == 'block' else 'ko'}||N1")
    return None if n1 is None else n1["p"]


def reference_census(ref, mask, keys=None, scope_arm=""):
    """The census of the reference's records of one mask (every BF fit of that mask on the base
    views), with the BF-active split, lambda counts, reused_from_ko counts and the at-risk list.
    Reads the store only; makes no fit."""
    keys = base_keys_of(ref) if keys is None else keys
    pl = planned(keys, mask)
    entries, lam, act, reused = [], {}, {"bf_active": 0, "p_equals_n1": 0, "no_n1": 0}, 0
    for rk in pl:
        rec = ref[rk]
        bk, mk, _ = rk.split("||")
        pn1 = n1_p_for(ref, rk)
        c = XC.census_fit(rec["p"], rec["y"], bk, mk, p_n1=pn1)
        entries.append((rk, c))
        pk = rk.split("||")[2]
        lam.setdefault(pk, {})
        lam[pk][str(float(rec["lam"]))] = lam[pk].get(str(float(rec["lam"])), 0) + 1
        if c["p_equals_n1"] is None:
            act["no_n1"] += 1
        elif c["p_equals_n1"]:
            act["p_equals_n1"] += 1
        else:
            act["bf_active"] += 1
        reused += bool(rec.get("reused_from_ko", False))
    scope = (f"{scope_arm} {mask}-mask BF_1-BF_4 fits of the {len(keys)} base views "
             f"({len(pl)} fits)").strip()
    return {"mask": mask, "scope": scope, "n_fits": len(pl), "lambda_by_rank": lam,
            "bf_active": act, "reused_from_ko": reused,
            "census": XC.family_summary_scoped(entries, scope),
            "at_risk": XC.at_risk_list(entries),
            "n_cells": int(len(ref[pl[0]]["y"])) if pl else None}


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Extension X: the reference census (CPU, read-only)")
    ap.add_argument("--arm", choices=sorted(ARMS), required=True)
    ap.add_argument("--which", choices=["pinned", "registered"], default="pinned")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    ref, info = load_reference(a.arm, a.which)
    out = {"reference": info,
           "masks": {m: reference_census(ref, m, scope_arm=f"arm {a.arm}") for m in EXT_MASKS}}
    txt = json.dumps(I.json_safe(out), indent=1)
    if a.json:
        p = pathlib.Path(a.json)
        why = ext_out_dir_refusal(p.parent)
        if why:
            raise SystemExit(why)
        p.write_text(txt, encoding="utf-8", newline="\n")
    print(txt)


if __name__ == "__main__":
    main()
