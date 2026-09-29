"""Extension X (block mask and fixed lambda; draft, not registered): the comparator, VX1's hash
check and VX2's equivalence check (tools/.venv; no torch).

Plan: docs/plans/2026-09-29-gpu-instrument-extension-x-plan.md (draft for review).
The same scheme as V1 and V2 (registration sections 5 and 7), for the two new fits:
  * VX1, self-stability: three fresh runs of one (arm, mask) composition; every per-fit sha256
    of U, V, lambda and the decoded p equal across the three (hashes_equal).
  * VX2, equivalence against the arm's pinned CPU store (ext_scope.load_reference), per fit:
      E1 (exact): y equal; lambda equal (block: the chosen lambda, the CSV's lambda_block; ko1:
         1.0 on both sides); labels (p >= 0.5) equal on every block cell; AUC equal (the arm's
         auc: ceiling_block on a block record, auc_fixed_lambda1 on a ko1 record); on a ko1
         record also p_P_fixed_lambda1 equal (the arm's auc_null over its uniform permutations,
         TAU, N_PERM, as evaluate_bank computes it);
      E2-II: the flipped pairs of S(f) (ext_census.order_flips: present x absent on a block
         record, all pairs of the block on a ko1 record), each named; 0 required;
      E2-III: the at-risk list (smallest gap on S(f) below 2^-23), a list, not a gate;
      E3: not applicable, stated per run: no continuous column reads a block or ko1 record (A's
         and B's evaluate_bank read block records only through auc -> ceiling_block,
         regrown_share_block, and lam -> lambda_block; ko1 records only through auc and auc_null
         -> auc_fixed_lambda1, p_P_fixed_lambda1);
      diagnostics, never deciding: bit-equality of p, max |dp|, its cell, s(p) there;
         the fits not bit-equal per (rank, reused_from_ko) cell against denominators read from
         the reference before the GPU records are opened; the BF-active classification.
    Outcomes as section 5: 1 = E1 and E2-II hold; 2 = E1 holds and a pair flipped; 3 = E1 fails.
The reference census (ext_scope.reference_census) is printed with every report, each count with
its scope label.

Usage:
  tools/.venv/Scripts/python.exe ext_compare.py --arm B --mask block --runs <d1> <d2> <d3> \
      [--reference pinned|registered] [--json <path outside every reference folder>]
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

import instrument as I  # noqa: E402
import ext_scope as XS  # noqa: E402
import ext_census as XC  # noqa: E402

E3_STATEMENT = ("E3 not applicable: no continuous column reads a block or ko1 record (block -> "
                "ceiling_block = auc, regrown_share_block from exact AUCs, lambda_block; ko1 -> "
                "auc_fixed_lambda1, p_P_fixed_lambda1)")


def log(m=""):
    print(m, flush=True)


# ------------------------------------------------------------------------------------------
# VX1: the per-fit hashes of fresh runs.

def read_run(run_dir):
    run_dir = pathlib.Path(run_dir)
    ok, detail = I.check_sha256sums(run_dir)
    if not ok:
        raise SystemExit(f"REFUSED (X): {run_dir} does not verify against its SHA256SUMS.txt: "
                         f"{detail}")
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    planned = XS.planned(manifest["keys"], manifest["mask"], manifest["ranks"])
    return run_dir, manifest, planned


def hashes_equal(h1, h2):
    """V1's comparison of two runs' fit_hashes.json: every fit and field equal."""
    if sorted(h1) != sorted(h2):
        return {"compared": None, "differ": None, "keys_differ": True}
    differ = [k for k in h1 if h1[k] != h2[k]]
    by_field = {f: sum(1 for k in h1 if h1[k][f] != h2[k][f]) for f in ("U", "V", "lambda", "p")}
    return {"compared": len(h1), "differ": len(differ), "differing": sorted(differ),
            "differing_by_field": by_field, "keys_differ": False}


def self_stability(run_dirs):
    """VX1: the first run against each other run; all manifests of one composition."""
    runs = [read_run(d) for d in run_dirs]
    digests = {m["extension_digest"] for _, m, _ in runs}
    if len(digests) != 1:
        raise SystemExit(f"REFUSED (X): the runs have different extension digests {digests}")
    hs = [json.loads((d / "fit_hashes.json").read_text(encoding="utf-8")) for d, _, _ in runs]
    pairs = {f"run1_vs_run{i + 1}": hashes_equal(hs[0], hs[i]) for i in range(1, len(hs))}
    ok = all(v["differ"] == 0 for v in pairs.values())
    return {"passed": ok, "n_runs": len(runs), "extension_digest": digests.pop(),
            "stamps_equal": len({json.dumps(m["stamp"], sort_keys=True)
                                 for _, m, _ in runs}) == 1, **pairs}


# ------------------------------------------------------------------------------------------
# VX2: one run against the reference.

def p_P_fixed(p, y, K):
    """p_P_fixed_lambda1 as the arm's evaluate_bank computes it (uniform permutations only)."""
    y = np.asarray(y, bool)
    p = np.asarray(p, np.float64)
    Yu = y[K.uniform_perms()]
    a = K.auc(p, y)
    return (1 + int((K.auc_null(p, Yu) >= a - K.TAU).sum())) / (K.N_PERM + 1)


def compare_fit(rk, got, ref, K, p_n1_ref=None):
    bk, mk, pk = rk.split("||")
    y = np.asarray(ref["y"], bool)
    pr = np.asarray(ref["p"], np.float64)
    pg = np.asarray(got["p"], np.float64)
    a_ref, a_got = K.auc(pr, y), K.auc(pg, y)
    e1 = {"y_equal": bool(np.array_equal(y, np.asarray(got["y"], bool))),
          "lam_equal": float(got["lam"]) == float(ref["lam"]),
          "label_diffs": int(np.sum((pg >= 0.5) != (pr >= 0.5))),
          "auc_equal": a_got == a_ref}
    if mk == "ko1":
        e1["lam_is_fixed"] = float(got["lam"]) == XS.FIXED_LAMBDA == float(ref["lam"])
    bit = bool(np.array_equal(pg, pr))
    if mk == "ko1":
        e1["p_P_fixed_equal"] = True if bit else p_P_fixed(pg, y, K) == p_P_fixed(pr, y, K)
    e1["passed"] = all(v for k, v in e1.items() if k != "label_diffs") and e1["label_diffs"] == 0
    flips = [] if bit else XC.order_flips(pg, pr, y, bk, mk)
    c_ref = XC.census_fit(pr, y, bk, mk, p_n1=p_n1_ref)
    c_got = XC.census_fit(pg, y, bk, mk, p_n1=p_n1_ref)
    ent = {"key": rk, "mask": mk, "rank": int(pk.split(":")[1]), "lam_ref": float(ref["lam"]),
           "lam_got": float(got["lam"]), "reused_from_ko_ref": bool(ref.get("reused_from_ko")),
           "bit_equal": bit, "e1": e1, "n_flips": len(flips), "flips": flips,
           "auc_ref": a_ref, "auc_got": a_got, "census_ref": c_ref, "census_got": c_got,
           "at_risk": bool(c_ref["at_risk"] or c_got["at_risk"]),
           "other_fields_equal": bool(
               float(got["outside_density"]) == float(ref["outside_density"])
               and all(got["score"].get(k) == ref["score"].get(k) for k in
                       ("offset", "counts", "sign", "sign_n", "n_ne") if k in ref["score"]))}
    if not bit:
        dp = np.abs(pg - pr)
        i = int(np.argmax(dp))
        ent["diag"] = {"max_abs_dp": float(dp[i]), "cell": i, "p_ref_at_cell": float(pr[i]),
                       "s_p": float(np.spacing(np.float32(pr[i])))}
    return ent


def compare_records(got, ref, K, planned, ref_info=None, scope=""):
    """Every planned fit of `got` (a GPU run's records) against `ref` (the arm's CPU store)."""
    missing = [rk for rk in planned if rk not in ref]
    if missing:
        raise SystemExit(f"REFUSED (X): {len(missing)} planned fits have no reference record, "
                         f"e.g. {missing[:3]}")
    # Denominators and the BF-active classification from the reference alone, first.
    denom = Counter((int(rk.split(":")[-1]), bool(ref[rk].get("reused_from_ko")))
                    for rk in planned)
    act = {rk: (None if XS.n1_p_for(ref, rk) is None else not np.array_equal(
        np.asarray(ref[rk]["p"], np.float64), np.asarray(XS.n1_p_for(ref, rk), np.float64)))
        for rk in planned}
    if sorted(got) != sorted(planned):
        raise SystemExit("REFUSED (X): the GPU records do not match the planned keys")
    ents = [compare_fit(rk, got[rk], ref[rk], K, XS.n1_p_for(ref, rk)) for rk in planned]
    e1_fail = [e for e in ents if not e["e1"]["passed"]]
    flipped = [e for e in ents if e["n_flips"]]
    if e1_fail:
        outcome, text = 3, "REFUSED (outcome 3): E1 fails (lambda, label, AUC, y or p_P differs)"
    elif flipped:
        outcome, text = 2, f"REFUSED (outcome 2): E1 holds; {len(flipped)} fits with flipped pairs"
    else:
        outcome, text = 1, "EQUIVALENT (outcome 1): E1 and E2-II (0 flipped pairs) hold"
    nb = Counter((e["rank"], e["reused_from_ko_ref"]) for e in ents if not e["bit_equal"])
    return {"outcome": outcome, "outcome_text": text, "reference": ref_info, "n_fits": len(ents),
            "e3": E3_STATEMENT,
            "e1_failures": [{"key": e["key"], **e["e1"], "lam_ref": e["lam_ref"],
                             "lam_got": e["lam_got"], "auc_ref": e["auc_ref"],
                             "auc_got": e["auc_got"]} for e in e1_fail],
            "flipped_pairs": [{"key": e["key"], "flips": e["flips"]} for e in flipped],
            "n_flipped_pairs": sum(e["n_flips"] for e in ents),
            "at_risk": [{"key": e["key"], "gap_ref": e["census_ref"]["gap_S"],
                         "gap_got": e["census_got"]["gap_S"], "pair_ref": e["census_ref"]["pair_S"],
                         "auc_equal": e["e1"]["auc_equal"]} for e in ents if e["at_risk"]],
            "census_reference": XC.family_summary_scoped(
                [(e["key"], e["census_ref"]) for e in ents], f"reference: {scope}"),
            "census_gpu": XC.family_summary_scoped(
                [(e["key"], e["census_got"]) for e in ents], f"GPU run: {scope}"),
            "n_not_bit_equal": sum(not e["bit_equal"] for e in ents),
            "not_bit_equal_by_rank_and_reuse": [
                {"rank": k[0], "reused_from_ko_ref": k[1], "not_bit_equal": nb[k],
                 "denominator": v} for k, v in sorted(denom.items())],
            "differing_fits": [{"key": e["key"], **e["diag"], "lam": e["lam_ref"],
                                "bf_active": act[e["key"]]} for e in ents if not e["bit_equal"]],
            "bf_active": {"bf_active": sum(bool(v) for v in act.values()),
                          "p_equals_n1": sum(v is False for v in act.values()),
                          "no_n1": sum(v is None for v in act.values())},
            "records_other_fields_differ": [e["key"] for e in ents if not e["other_fields_equal"]],
            "per_fit": [{"key": e["key"], "bit_equal": e["bit_equal"], "e1": e["e1"]["passed"],
                         "n_flips": e["n_flips"], "at_risk": e["at_risk"]} for e in ents]}


def compare_run(run_dir, arm, which="pinned", ref=None, ref_info=None):
    run_dir, manifest, planned = read_run(run_dir)
    if manifest["arm"]["name"] != arm:
        raise SystemExit(f"REFUSED (X): run {run_dir} is arm {manifest['arm']['name']}, not {arm}")
    K = XS.arm_module(arm)
    if ref is None:
        ref, ref_info = XS.load_reference(arm, which)
    got = I.read_store(run_dir / manifest["files"]["records"])
    scope = (f"arm {arm} {manifest['mask']}-mask BF fits ({len(planned)} fits, "
             f"{len(manifest['keys'])} base views)")
    rep = compare_records(got, ref, K, planned, ref_info, scope)
    rep.update(gpu_run=str(run_dir), gpu_label=manifest.get("label"),
               gpu_head=manifest.get("git_head"), mask=manifest["mask"], arm=arm,
               reference_census=XS.reference_census(ref, manifest["mask"], manifest["keys"],
                                                    scope_arm=f"arm {arm}"))
    return rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=sorted(XS.ARMS), required=True)
    ap.add_argument("--mask", choices=XS.EXT_MASKS, required=True)
    ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--reference", choices=["pinned", "registered"], default="pinned")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    out = {"VX1": self_stability(a.runs) if len(a.runs) > 1 else None,
           "VX2": compare_run(a.runs[0], a.arm, a.reference)}
    if out["VX2"]["mask"] != a.mask:
        raise SystemExit(f"REFUSED (X): run mask {out['VX2']['mask']} is not {a.mask}")
    log(json.dumps({"VX1": out["VX1"], "VX2_outcome": out["VX2"]["outcome_text"],
                    "n_not_bit_equal": out["VX2"]["n_not_bit_equal"],
                    "n_flipped_pairs": out["VX2"]["n_flipped_pairs"],
                    "at_risk": len(out["VX2"]["at_risk"]), "e3": out["VX2"]["e3"]}, indent=1))
    if a.json:
        p = pathlib.Path(a.json)
        why = XS.ext_out_dir_refusal(p.parent)
        if why:
            raise SystemExit(why)
        I.write_json(p, out)
    ok = out["VX2"]["outcome"] == 1 and (out["VX1"] is None or out["VX1"]["passed"])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
