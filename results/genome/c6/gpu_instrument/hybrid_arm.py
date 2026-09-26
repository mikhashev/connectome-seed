"""G12 and G13: what an arm's new script (not A's) calls to use the hybrid instrument (tools/.venv).

docs/plans/2026-09-26-gpu-instrument-registration.md, revision 1.3: D8 (I2), D9 (b), D10 (a), R1,
R4, R7; section 10, G12 and G13. No arm script names the hybrid instrument yet (D11); these are
the functions such a script imports, tested on fixtures (T-G8) and used by V3's path check.

  * check_gpu_stage (G13, D8 (I2)): the CPU stage's import of a GPU stage's run folder. It refuses
    unless the folder verifies against its SHA256SUMS.txt; the manifest names the CPU stage's own
    head and a clean tree, and the CPU stage's own tree is clean (R7); every instrument file's LF
    sha256 in the manifest equals the file at this head; the key set equals the planned BF ko
    keys; the composition digest equals the expected (registered) one and recomputes from the
    manifest's keys; the stamp equals the registered stamp (R1); the degree-term digest equals
    the CPU stage's own (D10). It returns the BF ko records.
  * path_check_bf / fixed_lambda_path_check_hybrid (G12, D9 (b)): A's fixed-lambda path check
    for GPU-made BF records: the CPU refit at lambda = 1 against the selected GPU fit, exact on
    lambda, labels and AUC, with 0 flipped pairs on S(f) (census.order_flips), its |dp| printed;
    rule #2.1 stays on the CPU and stays exact.
"""
import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import instrument as I  # noqa: E402
import census as C  # noqa: E402


class GpuStageRefused(Exception):
    pass


def check_gpu_stage(run_dir, planned_keys, expected_digest, own_terms, registered_stamp=None,
                    own_head=None, own_dirty=None, require_clean=True, file_hashes=None):
    """G13. planned_keys: the arm's planned bank keys (world and world|sh). Returns
    (records, report). Raises GpuStageRefused with every reason found."""
    run_dir = pathlib.Path(run_dir)
    why = []
    ok, detail = I.check_sha256sums(run_dir)
    if not ok:
        raise GpuStageRefused(f"REFUSED (G13): {run_dir} does not verify: {detail}")
    m = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    own_head = I.git_head() if own_head is None else own_head
    own_dirty = I.tree_dirty_paths() if own_dirty is None else own_dirty
    if m.get("kind") != "arm":
        why.append(f"the GPU stage is a {m.get('kind')!r} run, not an arm run")
    if m.get("git_head") != own_head:
        why.append(f"head {m.get('git_head')} differs from this stage's {own_head} (R7)")
    if m.get("not_from_a_committed_head") or m.get("tree_dirty_paths"):
        why.append("the GPU stage ran from a dirty tree (R7)")
    if require_clean and own_dirty:
        why.append(f"this stage's tree is dirty: {own_dirty} (R7)")
    fh = I.instrument_file_hashes() if file_hashes is None else file_hashes
    diff = {f: (m.get("file_sha256_lf", {}).get(f), h) for f, h in fh.items()
            if m.get("file_sha256_lf", {}).get(f) != h}
    if diff:
        why.append(f"instrument file hashes differ from this head: {sorted(diff)}")
    try:
        for k in m.get("keys", []):
            I.check_key(k)
    except ValueError as e:
        why.append(str(e))
    planned = list(planned_keys)
    for k in planned:
        I.check_key(k)
    if sorted(m.get("keys", [])) != sorted(planned):
        why.append("the GPU stage's key set differs from the planned BF ko keys")
    comp = m.get("composition", {})
    try:
        recomputed = I.composition_digest(m.get("keys", []), comp.get("starts"),
                                          comp.get("ranks", []))
    except (ValueError, TypeError) as e:
        recomputed = f"not recomputable: {e}"
    if recomputed != comp.get("refusal_digest"):
        why.append("the manifest's composition digest does not recompute from its keys")
    if expected_digest is None or comp.get("refusal_digest") != expected_digest:
        why.append(f"composition digest {comp.get('refusal_digest')} differs from the expected "
                   f"{expected_digest} (R4)")
    if comp.get("ranks") != [1, 2, 3, 4]:
        why.append(f"ranks {comp.get('ranks')}; the hybrid needs BF_1..BF_4")
    try:
        I.check_stamp(m.get("stamp", {}), registered=registered_stamp)
    except ValueError as e:
        why.append(str(e))
    if m.get("degree_terms_digest") != I.degree_terms_digest(own_terms):
        why.append("the degree-term digest differs from this stage's own (D10)")
    ov = m.get("overrides", {})
    if ov.get("flags_off") or ov.get("bf_tol") or ov.get("poison_real_block") or \
            ov.get("device", "cuda") != "cuda":
        why.append(f"the GPU stage ran with an override: {ov}")
    if why:
        raise GpuStageRefused("REFUSED (G13): " + "; ".join(why))
    recs = I.read_store(run_dir / m["files"]["records"])
    want = sorted(I.bf_record_key(k, r) for r in (1, 2, 3, 4) for k in planned)
    if sorted(recs) != want:
        raise GpuStageRefused("REFUSED (G13): the records are not the planned BF ko records")
    return recs, {"run_dir": str(run_dir), "head": own_head, "digest": comp.get("refusal_digest"),
                  "records": len(recs), "passed": True}


def check_prerun_reproduced(prerun_dir, run_dir):
    """R5: the registered run's GPU records equal the arm's GPU pre-run's bit for bit: every
    per-fit sha256 of the raw U, V, lambda and of the decoded p (G6) equal, over the same keys,
    and the same composition digest. Raises GpuStageRefused on any difference."""
    out = {}
    for name, d in (("prerun", prerun_dir), ("run", run_dir)):
        d = pathlib.Path(d)
        ok, detail = I.check_sha256sums(d)
        if not ok:
            raise GpuStageRefused(f"REFUSED (R5): {name} folder {d} does not verify: {detail}")
        m = json.loads((d / "manifest.json").read_text(encoding="utf-8"))
        h = json.loads((d / m["files"]["hashes"]).read_text(encoding="utf-8"))
        out[name] = (m, h)
    (mp, hp), (mr, hr) = out["prerun"], out["run"]
    if mp["composition"]["refusal_digest"] != mr["composition"]["refusal_digest"]:
        raise GpuStageRefused("REFUSED (R5): the run's composition differs from its pre-run's")
    if sorted(hp) != sorted(hr):
        raise GpuStageRefused("REFUSED (R5): the run's fits differ from its pre-run's key set")
    diff = [k for k in hp if hp[k] != hr[k]]
    if diff:
        raise GpuStageRefused(f"REFUSED (R5): {len(diff)} fits differ from the pre-run bit for "
                              f"bit, e.g. {diff[:5]}")
    return {"fits": len(hp), "passed": True}


def _auc(p, y):
    import knockout_regrow as K
    return K.auc(p, y)


def path_check_bf(cpu_rec, gpu_rec, bank_key, mask="ko"):
    """G12 / D9 (b) for one BF record: the CPU refit at fixed lambda (cpu_rec) against the
    selected GPU fit (gpu_rec). Exact on lambda, labels and AUC; 0 flipped pairs on S(f) of the
    selected fit's view; |dp| printed."""
    y = np.asarray(cpu_rec["y"], bool)
    pc = np.asarray(cpu_rec["p"], np.float64)
    pg = np.asarray(gpu_rec["p"], np.float64)
    flips = C.order_flips(pg, pc, y, bank_key, mask)
    res = {"lam_equal": float(cpu_rec["lam"]) == float(gpu_rec["lam"]),
           "y_equal": bool(np.array_equal(y, np.asarray(gpu_rec["y"], bool))),
           "label_diffs": int(np.sum((pc >= 0.5) != (pg >= 0.5))),
           "auc_equal": _auc(pc, y) == _auc(pg, y),
           "n_flips": len(flips), "flips": flips,
           "max_abs_dp": float(np.max(np.abs(pc - pg))),
           "bit_equal": bool(np.array_equal(pc, pg))}
    res["passed"] = bool(res["lam_equal"] and res["y_equal"] and res["label_diffs"] == 0
                         and res["auc_equal"] and res["n_flips"] == 0)
    return res


def path_check_rule(cpu_rec, rec):
    """Rule #2.1 stays on the CPU and stays exact (A's check)."""
    same = [float(x) for x in cpu_rec["p"]] == [float(x) for x in rec["p"]]
    return {"exact": same, "passed": same}


def fixed_lambda_path_check_hybrid(F, base_keys, refit, fixed_lambda=1.0):
    """G12: A's fixed_lambda_path_check (knockout_regrow.py:1812-1830) with D9 (b) for the BF
    records. F: {(bank, mask, pk): record}; refit(bank, pk) -> the CPU record of the fixed-lambda
    fit (A's train_fixed_lambda path). On the first bank whose five ko fits (rule #2.1, BF_1..BF_4)
    all selected lambda = 1, the five are refitted; BF: D9 (b); rule: exact."""
    ks = ("rule", "BF:1", "BF:2", "BF:3", "BF:4")
    for bk in base_keys:
        if all(float(F[(bk, "ko", pk)]["lam"]) == fixed_lambda for pk in ks):
            per = {}
            for pk in ks:
                cpu = refit(bk, pk)
                per[pk] = (path_check_rule(cpu, F[(bk, "ko", pk)]) if pk == "rule"
                           else path_check_bf(cpu, F[(bk, "ko", pk)], bk, "ko"))
            return {"bank": bk, "per_predictor": per,
                    "passed": all(v["passed"] for v in per.values()),
                    "rule": "D9 (b): BF exact on lambda, labels, AUC, 0 flipped pairs; rule #2.1 "
                            "exact"}
    return {"bank": None, "passed": None, "note": "no bank selected lambda = 1 on all five"}
