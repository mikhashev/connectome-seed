"""G9: the equivalence comparator, E1, E2 and E3 of section 5 (tools/.venv; no torch).

docs/plans/2026-09-26-gpu-instrument-registration.md, revision 1.4 (e2fab47), sections 5 and 7
(V2, V8); Ark's review of revision 1.3 (chat 12:09 UTC), points 1 and 2, is part of revision 1.4.

It compares a GPU stage's BF ko records (a run folder written by run_registered.py) with a CPU
reference store: by default A's pinned pre-run store, read after check_prerun_files (imported
read-only from A's script) has verified the pinned folder; for V8 another store named by path
and sha256. Per fit (record key "world:<f>:<j>[|sh:<sd>]||ko||BF:<r>"):
  * E1 (= E2-I): y equal (the GPU y must equal the reference y), lambda equal, the labels
    (p >= 0.5) equal on the 64 cells, AUC (knockout_regrow.auc) equal;
  * E2-II: the flipped pairs of S(f) (census.order_flips), each named; 0 required;
  * E2-III: the at-risk list (smallest gap on S(f) < 2^-23 on either side), each entry with its
    pair, whether its AUC equals the reference's and, on a base view, whether p_P and p_P_rowcol
    equal the reference's; a difference there is refused by E1, never by E2-III;
  * E3 on each base-view fit whose p is not bit-equal: the bound on D (2 delta / q_min) and on
    logloss (delta / m_min) from the reference p and the fit's own delta = max |dp|, printed with
    the tighter form and the count of cells where logit_of clips; the fit's own D and logloss
    (score existence) must move by no more than their bounds, and not at all where p is
    bit-equal; a change at a clipped cell is not covered and fails;
  * diagnostics, never deciding: max |dp|, its cell, s(p) of the reference p there, the ratio;
    the counts of non-bit-equal fits per (rank x lambda x view) cell against denominators read
    from the reference store's lambda BEFORE the GPU records are opened (on A: 37, 164, 4,299,
    13,500 in M18's four groups).
Ark, point 1: the BF-active classification, computed from the reference store alone with no fit:
a fit is BF-active if its p differs from the p of its own view's N1 record (on A: every fit at
lambda < 100, and three at lambda = 100, world:W:4|sh:84 BF:2-BF:4; 359 of 18,000).
Ark, point 2: every census count carries its per-fit denominator (census.family_summary).

Outcomes (section 5): 1 = E1, E2-II and E3 hold; 2 = E1 holds, a flipped pair or E3 fails:
refused; 3 = E1 fails anywhere: refused.

The arm (V8): the AUC, D, logit and leg-P functions of E1, E3 and the at-risk outputs are the arm's
own. By default A's (knockout_regrow); V8 passes the male adapter (male_arm), whose auc, parity_D,
logit_of, auc_null, TAU and N_PERM are the male script's and whose null_patterns(y) gives the male
leg P's own permutations (default_rng(92000)) and row-and-column patterns (default_rng(92001)). The
pair sets are those of section 5 for every arm: per (column, fit), S(f) = present x absent on a
shuffle, all 2,016 on a base view's ko fit (census.census_set_of); the male arm's columns read the
same sets (auc_other_61, per_type_auc and precision_at_n_present are subsets or boundaries of the
present x absent pairs; p_P and p_P_rowcol rank a base view over all 64 cells).

Usage:
  tools/.venv/Scripts/python.exe gpu_equivalence.py --gpu <run dir> [--json <report path>]
  tools/.venv/Scripts/python.exe gpu_equivalence.py --gpu <run dir> --reference <store> \
      --reference-sha256 <hex>
"""
import argparse
import json
import pathlib
import sys
from collections import Counter

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import instrument as I  # noqa: E402  (puts c6 and c6/checks on sys.path)
import census as C  # noqa: E402
import knockout_regrow as K  # noqa: E402  (read-only import; its arms live under __main__)
import harness as H  # noqa: E402

LOGIT_CLIP = (1e-300, 1 - 1e-16)          # knockout_regrow.logit_of (:1010-1012)


def log(m=""):
    print(m, flush=True)


# ------------------------------------------------------------------------------------------
# The reference.

def load_reference(path=None, sha256=None):
    """A's pinned store after check_prerun_files (D4 (a)), or a named store with its sha256."""
    if path is None:
        chk = K.check_prerun_files()
        if not chk["passed"]:
            raise SystemExit(f"REFUSED (G9, D4): the pinned pre-run folder does not verify: "
                             f"{chk['reason']}")
        path = pathlib.Path(K.PRERUN_DIR) / "raw_fits.json.gz"
        sha256 = K.PRERUN_SHA256["raw_fits.json.gz"]
        info = {"path": str(path), "pinned": True, "check_prerun_files": chk["reason"]}
    else:
        path = pathlib.Path(path)
        if not path.is_file():
            raise SystemExit(f"REFUSED (G9): reference store {path} not found")
        if sha256 is None:
            raise SystemExit("REFUSED (G9): a reference other than the pinned store needs its "
                             "sha256 (--reference-sha256)")
        info = {"path": str(path), "pinned": False}
    got = I.sha256_file(path)
    if got != sha256:
        raise SystemExit(f"REFUSED (G9): reference {path} sha256 {got}, expected {sha256}")
    info["sha256"] = got
    return I.read_store(path), info


def cell_group(r, lam, base):
    """M18's four groups: rank 1 lambda in {1, 3} base; rank 1 lambda in {1, 3} shuffle; rank 1
    lambda = 100; ranks 2-4 (any lambda)."""
    if r != 1:
        return "ranks 2-4, any lambda"
    if lam == 100:
        return "rank 1, lambda 100"
    return f"rank 1, lambda {{1, 3}}, {'base' if base else 'shuffle'}"


def denominators(ref, planned):
    """Diagnostic denominators from the reference store's lambda, for the planned record keys,
    read before the GPU records are opened: per (rank x lambda x view) cell and per M18 group."""
    cells, groups = Counter(), Counter()
    for rk in planned:
        bk, _, pk = I.split_record_key(rk)
        r, lam, base = int(pk.split(":")[1]), float(ref[rk]["lam"]), I.is_base_view(bk)
        cells[(r, lam, "base" if base else "shuffle")] += 1
        groups[cell_group(r, lam, base)] += 1
    return cells, groups


def bf_active(ref, planned):
    """Ark, point 1: per planned fit, True if its reference p differs from its view's N1 p
    (None if the reference has no N1 record for the view)."""
    out = {}
    for rk in planned:
        bk, mk, _ = I.split_record_key(rk)
        n1 = ref.get(f"{bk}||{mk}||N1")
        out[rk] = None if n1 is None else not np.array_equal(
            np.asarray(ref[rk]["p"], np.float64), np.asarray(n1["p"], np.float64))
    return out


def bf_active_summary(ref, planned, act):
    tab = Counter()
    for rk in planned:
        bk, _, pk = I.split_record_key(rk)
        tab[(pk, float(ref[rk]["lam"]), "base" if I.is_base_view(bk) else "shuffle",
             act[rk])] += 1
    exceptions = [rk for rk in planned if act[rk] and float(ref[rk]["lam"]) == 100.0]
    below = [rk for rk in planned if float(ref[rk]["lam"]) < 100.0]
    return {"n_fits": len(planned), "bf_active": sum(bool(v) for v in act.values()),
            "p_equals_n1": sum(v is False for v in act.values()),
            "no_n1_record": sum(v is None for v in act.values()),
            "lambda_below_100": len(below),
            "lambda_below_100_all_active": all(act[rk] for rk in below),
            "active_at_lambda_100": exceptions,
            "table": [{"predictor": k[0], "lambda": k[1], "view": k[2], "bf_active": k[3],
                       "fits": v} for k, v in sorted(tab.items(), key=str)]}


# ------------------------------------------------------------------------------------------
# E3.

def e3_bounds(p_ref, y, delta):
    """Section 5, E3, for one fit whose p is not bit-equal: delta = its own max |dp|; p_ref the
    reference p. D: 2 delta / q_min, q_min over the non-clipped cells of min over the endpoints
    p +- delta of p(1 - p); cells whose interval reaches logit_of's clip are left out and counted.
    The tighter form delta * (mean_present 1/(p(1-p)) + mean_absent 1/(p(1-p))) is a diagnostic.
    logloss: delta / m_min, m_min over the endpoints after harness.CLIP (p~ on a present cell,
    1 - p~ on an absent one); a cell whose whole interval lies beyond one end of CLIP contributes
    nothing."""
    p = np.asarray(p_ref, np.float64)
    y = np.asarray(y, bool)
    lo, hi = p - delta, p + delta
    clipped = (lo <= LOGIT_CLIP[0]) | (hi >= LOGIT_CLIP[1])
    qm = np.minimum(lo * (1 - lo), hi * (1 - hi))[~clipped]
    q_min = float(qm.min()) if qm.size else None
    with np.errstate(divide="ignore"):
        inv = 1.0 / (p * (1 - p))
    tighter = (float(delta * (inv[y].mean() + inv[~y].mean()))
               if y.any() and (~y).any() else None)
    c_lo, c_hi = H.CLIP
    contributes = ~((hi <= c_lo) | (lo >= c_hi))
    lo_c, hi_c = np.clip(lo, c_lo, c_hi), np.clip(hi, c_lo, c_hi)
    m = np.where(y, np.minimum(lo_c, hi_c), np.minimum(1 - lo_c, 1 - hi_c))
    m_min = float(m[contributes].min()) if contributes.any() else None
    return {"delta": float(delta), "q_min": q_min,
            "D_bound": (2 * delta / q_min) if q_min else None, "D_tighter_diagnostic": tighter,
            "cells_clipped_by_logit_of": int(clipped.sum()),
            "clipped_cells": [int(i) for i in np.flatnonzero(clipped)],
            "m_min": m_min, "logloss_bound": (delta / m_min) if m_min else 0.0}


def e3_check(bounds, D_ref, D_got, ll_ref, ll_got, dp=None):
    """E3 on one fit (or one CSV row): |dD| <= D_bound and |d logloss| <= logloss_bound
    (logloss_margin_over_N1 moves by exactly -d logloss, N1 being a CPU fit). bounds None means
    the fit is bit-equal: every value must be exact. dp (per-cell |dp|): a nonzero dp at a cell
    clipped by logit_of is not covered and fails."""
    if bounds is None:
        ok = (D_ref == D_got) and (ll_ref == ll_got)
        return {"passed": bool(ok), "exact_required": True, "dD": None if D_ref is None or
                D_got is None else abs(D_got - D_ref), "dlogloss": abs(ll_got - ll_ref)}
    res = {"exact_required": False}
    if D_ref is None or D_got is None:
        okD = D_ref is None and D_got is None
        res["dD"] = None
    else:
        dD = abs(D_got - D_ref)
        res["dD"] = dD
        okD = bounds["D_bound"] is not None and dD <= bounds["D_bound"]
    if dp is not None and bounds["clipped_cells"]:
        moved = [i for i in bounds["clipped_cells"] if dp[i] != 0]
        res["clipped_cells_moved"] = moved
        okD = okD and not moved
    dll = abs(ll_got - ll_ref)
    res["dlogloss"] = dll
    okL = dll <= bounds["logloss_bound"]
    res.update(D_within=bool(okD), logloss_within=bool(okL), passed=bool(okD and okL))
    return res


def D_of(p, y, arm=None):
    arm = arm_of(arm)
    return arm.parity_D(arm.logit_of(p), y)


# ------------------------------------------------------------------------------------------
# Per fit.

_NULLS = {}


def arm_of(arm):
    """The arm whose functions the comparator uses: A's (knockout_regrow) unless given."""
    return K if arm is None else arm


def null_inputs(y, arm=None):
    """(Yu, Yrc) of a base view's labels, as the arm's evaluate_bank builds them (cached per arm
    and y). Yrc is None where the arm's row-and-column null has no patterns (the male S13)."""
    arm = arm_of(arm)
    y = np.asarray(y, bool)
    key = (getattr(arm, "__name__", repr(arm)), y.tobytes())
    if key not in _NULLS:
        if hasattr(arm, "null_patterns"):
            _NULLS[key] = arm.null_patterns(y)
        else:
            _NULLS[key] = (y[arm.uniform_perms()], arm.rc_patterns(y))
    return _NULLS[key]


def p_P_pair(p, y, arm=None):
    """p_P and p_P_rowcol of a base-view fit, as the arm's evaluate_bank computes them."""
    arm = arm_of(arm)
    y = np.asarray(y, bool)
    Yu, Yrc = null_inputs(y, arm)
    p = np.asarray(p, np.float64)
    a = arm.auc(p, y)
    return ((1 + int((arm.auc_null(p, Yu) >= a - arm.TAU).sum())) / (arm.N_PERM + 1),
            None if Yrc is None else
            (1 + int((arm.auc_null(p, Yrc) >= a - arm.TAU).sum())) / (arm.N_PERM + 1))


def compare_fit(rk, got, ref, p_n1_ref=None, e3_base_only=True, arm=None):
    """Every quantity of section 5 for one fit (the arm's AUC, D and leg P)."""
    arm = arm_of(arm)
    bk, mk, pk = I.split_record_key(rk)
    base = I.is_base_view(bk)
    y = np.asarray(ref["y"], bool)
    yg = np.asarray(got["y"], bool)
    pr = np.asarray(ref["p"], np.float64)
    pg = np.asarray(got["p"], np.float64)
    a_ref, a_got = arm.auc(pr, y), arm.auc(pg, y)
    e1 = {"y_equal": bool(np.array_equal(y, yg)),
          "lam_equal": float(got["lam"]) == float(ref["lam"]),
          "label_diffs": int(np.sum((pg >= 0.5) != (pr >= 0.5))),
          "auc_equal": a_got == a_ref}
    e1["passed"] = bool(e1["y_equal"] and e1["lam_equal"] and e1["label_diffs"] == 0
                        and e1["auc_equal"])
    bit = bool(np.array_equal(pg, pr))
    flips = [] if bit else C.order_flips(pg, pr, y, bk, mk)
    cen_ref = C.census_fit(pr, y, bk, mk, p_n1=p_n1_ref)
    cen_got = C.census_fit(pg, y, bk, mk, p_n1=p_n1_ref)
    ent = {"key": rk, "rank": int(pk.split(":")[1]), "lam_ref": float(ref["lam"]),
           "lam_got": float(got["lam"]), "view": "base" if base else "shuffle",
           "bit_equal": bit, "e1": e1, "n_flips": len(flips), "flips": flips,
           "auc_ref": a_ref, "auc_got": a_got,
           "census_ref": cen_ref, "census_got": cen_got,
           "at_risk": bool(cen_ref["at_risk"] or cen_got["at_risk"]),
           # G4 fidelity (reported): the record fields other than p, lam and score existence
           "other_fields_equal": bool(
               float(got["outside_density"]) == float(ref["outside_density"])
               and all(got["score"].get(k) == ref["score"].get(k) for k in
                       ("offset", "counts", "sign", "sign_n", "n_ne") if k in ref["score"])),
           "at_risk_side": [s for s, c in (("reference", cen_ref), ("gpu", cen_got))
                            if c["at_risk"]]}
    if ent["at_risk"]:
        ar = {"auc_equal": a_got == a_ref}
        if base:
            pp_ref, pp_got = p_P_pair(pr, y, arm), p_P_pair(pg, y, arm)
            ar.update(p_P_equal=pp_ref[0] == pp_got[0], p_P_rowcol_equal=pp_ref[1] == pp_got[1],
                      p_P_ref=pp_ref, p_P_got=pp_got)
        ent["at_risk_outputs"] = ar
    if not bit:
        dp = np.abs(pg - pr)
        i = int(np.argmax(dp))
        s = float(np.spacing(np.float32(pr[i])))
        ent["diag"] = {"max_abs_dp": float(dp[i]), "cell": i, "p_ref_at_cell": float(pr[i]),
                       "s_p": s, "ratio_to_s_p": float(dp[i] / s)}
    if base or not e3_base_only:
        bounds = None if bit else e3_bounds(pr, y, float(np.max(np.abs(pg - pr))))
        ent["e3_bounds"] = bounds
        ent["e3"] = e3_check(bounds, D_of(pr, y, arm), D_of(pg, y, arm),
                             float(ref["score"]["existence"]), float(got["score"]["existence"]),
                             dp=None if bit else np.abs(pg - pr))
    return ent


def compact(ent):
    """The per-fit summary that V6's brute-force recount is compared with."""
    return {"key": ent["key"], "y_equal": ent["e1"]["y_equal"],
            "lam_equal": ent["e1"]["lam_equal"], "label_diffs": ent["e1"]["label_diffs"],
            "auc_equal": ent["e1"]["auc_equal"], "bit_equal": ent["bit_equal"],
            "max_abs_dp": ent.get("diag", {}).get("max_abs_dp", 0.0),
            "n_flips": ent["n_flips"], "at_risk": ent["at_risk"]}


# ------------------------------------------------------------------------------------------
# A run folder against the reference.

def read_gpu_run(run_dir):
    run_dir = pathlib.Path(run_dir)
    ok, detail = I.check_sha256sums(run_dir)
    if not ok:
        raise SystemExit(f"REFUSED (G9): {run_dir} does not verify against its SHA256SUMS.txt: "
                         f"{detail}")
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    for k in manifest["keys"]:
        I.check_key(k)
    ranks = manifest["composition"]["ranks"]
    planned = [I.bf_record_key(k, r) for r in ranks for k in manifest["keys"]]
    return run_dir, manifest, planned


def compare_run(run_dir, ref=None, ref_info=None, only=None, arm=None):
    """V2 / V8: every planned fit of a GPU run against the reference. only: a set of record
    keys to restrict to (V6: the BF-active subset). arm: the arm module whose AUC, D and leg P
    the comparison uses (None: A's; V8: the male adapter). Returns the report."""
    run_dir, manifest, planned = read_gpu_run(run_dir)
    if ref is None:
        ref, ref_info = load_reference()
    missing = [rk for rk in planned if rk not in ref]
    if missing:
        raise SystemExit(f"REFUSED (G9): {len(missing)} planned fits have no reference record, "
                         f"e.g. {missing[:3]}")
    # Denominators and the BF-active classification from the reference alone, before the GPU
    # records are opened.
    cells, groups = denominators(ref, planned)
    act = bf_active(ref, planned)
    act_sum = bf_active_summary(ref, planned, act)
    got = I.read_store(run_dir / manifest["files"]["records"])
    if sorted(got) != sorted(planned):
        raise SystemExit("REFUSED (G9): the GPU records do not match the manifest's planned keys")
    for rk in got:
        bk, mk, pk = I.split_record_key(rk)
        I.check_key(bk)
        if mk != "ko" or pk not in K.BF_KEYS:
            raise SystemExit(f"REFUSED (G9, D1 (a)): record {rk} is not a BF ko record")
    use = [rk for rk in planned if only is None or rk in only]
    ents = []
    for rk in use:
        bk, mk, _ = I.split_record_key(rk)
        n1 = ref.get(f"{bk}||{mk}||N1")
        ents.append(compare_fit(rk, got[rk], ref[rk], None if n1 is None else n1["p"], arm=arm))
    rep = summarise(ents, cells, groups, act, act_sum, manifest, ref_info, run_dir)
    rep["arm"] = getattr(arm_of(arm), "__name__", repr(arm))
    return rep


def summarise(ents, cells, groups, act, act_sum, manifest, ref_info, run_dir):
    e1_fail = [e for e in ents if not e["e1"]["passed"]]
    flipped = [e for e in ents if e["n_flips"]]
    e3_fail = [e for e in ents if "e3" in e and not e["e3"]["passed"]]
    differ = [e for e in ents if not e["bit_equal"]]
    risk = [e for e in ents if e["at_risk"]]
    if e1_fail:
        outcome = 3
        text = ("REFUSED (outcome 3): E1 fails (a lambda, label, AUC or y differs; an at-risk "
                "fit's included): the instrument changed a deciding output")
    elif flipped or e3_fail:
        outcome = 2
        text = (f"REFUSED (outcome 2): E1 holds; {len(flipped)} fits with flipped pairs (E2-II), "
                f"{len(e3_fail)} fits beyond E3")
    else:
        outcome = 1
        text = ("EQUIVALENT (outcome 1): E1, E2-II (0 flipped pairs) and E3 hold on the compared "
                "fits")
    nb_cells, nb_groups = Counter(), Counter()
    for e in differ:
        base = e["view"] == "base"
        nb_cells[(e["rank"], e["lam_ref"], e["view"])] += 1
        nb_groups[cell_group(e["rank"], e["lam_ref"], base)] += 1
    fam_ref = C.family_summary([(e["key"], e["census_ref"]) for e in ents])
    fam_got = C.family_summary([(e["key"], e["census_got"]) for e in ents])
    differing_with_ties = sum(1 for e in differ if e["census_ref"]["tied_S"] > 0)
    at_risk_n1 = sum(1 for e in risk if e["census_ref"]["p_equals_n1"] is False)
    rep = {"outcome": outcome, "outcome_text": text,
           "reference": ref_info, "gpu_run": str(run_dir), "gpu_label": manifest.get("label"),
           "gpu_head": manifest.get("git_head"), "n_fits": len(ents),
           "e1_failures": [{"key": e["key"], **e["e1"], "auc_ref": e["auc_ref"],
                            "auc_got": e["auc_got"], "lam_ref": e["lam_ref"],
                            "lam_got": e["lam_got"]} for e in e1_fail],
           "flipped_pairs": [{"key": e["key"], "flips": e["flips"]} for e in flipped],
           "n_flipped_pairs": sum(e["n_flips"] for e in ents),
           "e3_failures": [{"key": e["key"], "e3": e["e3"], "bounds": e["e3_bounds"]}
                           for e in e3_fail],
           "at_risk": [{"key": e["key"], "side": e["at_risk_side"],
                        "pair_ref": e["census_ref"]["pair_S"], "gap_ref": e["census_ref"]["gap_S"],
                        "pair_got": e["census_got"]["pair_S"], "gap_got": e["census_got"]["gap_S"],
                        "p_equals_n1_ref": e["census_ref"]["p_equals_n1"],
                        **e.get("at_risk_outputs", {})} for e in risk],
           "census_by_family_reference": fam_ref, "census_by_family_gpu": fam_got,
           "differing_fits": [{"key": e["key"], **e["diag"], "lam": e["lam_ref"],
                               "e3_bounds": e.get("e3_bounds"), "e3": e.get("e3"),
                               "tied_pairs_S_ref": e["census_ref"]["tied_S"],
                               "bf_active": act.get(e["key"])} for e in differ],
           "n_not_bit_equal": len(differ),
           "records_other_fields_differ": [e["key"] for e in ents if not e["other_fields_equal"]],
           "differing_fits_that_carry_ties": differing_with_ties,
           "at_risk_fits_whose_p_differs_from_n1": at_risk_n1,
           "not_bit_equal_by_cell": [{"rank": k[0], "lambda": k[1], "view": k[2],
                                      "not_bit_equal": nb_cells[k], "denominator": v}
                                     for k, v in sorted(cells.items())],
           "not_bit_equal_by_M18_group": {g: {"not_bit_equal": nb_groups[g], "denominator": v}
                                          for g, v in groups.items()},
           "bf_active": act_sum,
           "per_fit": [compact(e) for e in ents]}
    return rep


def print_bf_active(a):
    """The BF-active classification (Ark point 1), from bf_active_summary."""
    log(f"Ark point 1, BF-active classification (reference store alone, no fit): "
        f"{a['bf_active']} of {a['n_fits']} fits have p different from their view's N1 p; "
        f"{a['p_equals_n1']} equal; lambda < 100: {a['lambda_below_100']} fits, all BF-active: "
        f"{a['lambda_below_100_all_active']}; BF-active at lambda = 100: {a['active_at_lambda_100']}")
    for row in a["table"]:
        log(f"  {row['predictor']} lambda {row['lambda']:g} {row['view']:8s} "
            f"BF-active={row['bf_active']}: {row['fits']}")


def print_report(rep):
    log(f"reference: {rep['reference']}")
    log(f"GPU run: {rep['gpu_run']} (label {rep['gpu_label']}, head {rep['gpu_head']})"
        + (f"; arm functions: {rep['arm']}" if rep.get("arm") else ""))
    print_bf_active(rep["bf_active"])
    log(f"E1: {len(rep['e1_failures'])} fits fail")
    for e in rep["e1_failures"][:50]:
        log(f"  E1 FAIL {e}")
    log(f"E2-II: {rep['n_flipped_pairs']} flipped pairs in {len(rep['flipped_pairs'])} fits")
    for f in rep["flipped_pairs"][:50]:
        for x in f["flips"]:
            log(f"  FLIP {f['key']} cells {x['cells']} labels {x['labels']} p_ref {x['p_ref']} "
                f"p_gpu {x['p_got']} states {x['state_ref']} -> {x['state_got']}")
    log(f"E2-III at-risk list (smallest gap on S(f) < 2^-23; not a gate): {len(rep['at_risk'])}")
    for e in rep["at_risk"]:
        log(f"  AT RISK {e}")
    log("census by column family (tied pairs; per-fit denominators summed; Ark point 2):")
    for side in ("reference", "gpu"):
        for fam, v in rep[f"census_by_family_{side}"].items():
            log(f"  {side:9s} {fam}: {v}")
    log(f"E3: {len(rep['e3_failures'])} fits beyond their bounds")
    for e in rep["e3_failures"]:
        log(f"  E3 FAIL {e}")
    log(f"diagnostics: {rep['n_not_bit_equal']} fits not bit-equal "
        f"({rep['differing_fits_that_carry_ties']} carry ties on S(f) in the reference; "
        f"at-risk fits whose p differs from N1: {rep['at_risk_fits_whose_p_differs_from_n1']})")
    for d in rep["differing_fits"]:
        b = d.get("e3_bounds") or {}
        log(f"  {d['key']} lambda {d['lam']:g}: max|dp| {d['max_abs_dp']:.4g} at cell {d['cell']} "
            f"(p_ref {d['p_ref_at_cell']:.6g}, s(p) {d['s_p']:.3g}, ratio {d['ratio_to_s_p']:.3g})"
            + (f"; E3 D bound {b.get('D_bound'):.3g} (tighter {b.get('D_tighter_diagnostic'):.3g}),"
               f" logloss bound {b.get('logloss_bound'):.3g}, clipped cells "
               f"{b.get('cells_clipped_by_logit_of')}" if b else "")
            + f"; BF-active {d['bf_active']}")
    log("not bit-equal per (rank x lambda x view) cell, denominators from the reference lambda:")
    for c in rep["not_bit_equal_by_cell"]:
        log(f"  BF_{c['rank']} lambda {c['lambda']:g} {c['view']}: {c['not_bit_equal']} / "
            f"{c['denominator']}")
    for g, v in rep["not_bit_equal_by_M18_group"].items():
        log(f"  {g}: {v['not_bit_equal']} / {v['denominator']}")
    log(f"G4 record fidelity (outside_density, score offset/counts/sign/sign_n/n_ne; reported): "
        f"{len(rep['records_other_fields_differ'])} records differ from the reference")
    log(rep["outcome_text"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gpu", required=True)
    ap.add_argument("--reference", default=None)
    ap.add_argument("--reference-sha256", default=None)
    ap.add_argument("--only-bf-active", action="store_true")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    ref, info = load_reference(a.reference, a.reference_sha256)
    only = None
    if a.only_bf_active:
        _, manifest, planned = read_gpu_run(a.gpu)
        act = bf_active(ref, planned)
        only = {rk for rk, v in act.items() if v}
    rep = compare_run(a.gpu, ref, info, only=only)
    print_report(rep)
    if a.json:
        out = pathlib.Path(a.json)
        refusal = I.out_dir_refusal(out.parent)
        if refusal:
            raise SystemExit(refusal)
        I.write_json(out, rep)
        log(f"wrote {out}")
    sys.exit(0 if rep["outcome"] == 1 else 1)


if __name__ == "__main__":
    main()
