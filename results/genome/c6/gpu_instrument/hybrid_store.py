"""G10: the hybrid-store builder for V3 (tools/.venv; no torch).

docs/plans/2026-09-26-gpu-instrument-registration.md, revision 1.3, V3: "a hybrid store: V1's BF
ko records beside the pinned store's other records". From a GPU stage's run folder and A's pinned
pre-run store (read after check_prerun_files), it writes into a scratch folder (refused at or in
a reference folder, G11) a raw_fits.json.gz in A's format in which:
  * every BF_r ko record the GPU run holds (base views and shuffles) replaces the pinned record;
  * every ko1 record of the pinned store that is a copy of its ko fit (reused_from_ko set, A's
    complete_fixed_lambda) is replaced by a copy of the GPU ko record with reused_from_ko True,
    as a hybrid run would make it (the census scope of section 5: "the ko1 records copied from
    them");
  * every other record (N1, rule #2.1, the ceilings, the |pc: fits, the fitted ko1 records) is
    the pinned CPU record, unchanged.
A's script then re-reads it unmodified: --synthetic-only --from-raw <hybrid> --out <scratch>.

Usage:
  tools/.venv/Scripts/python.exe hybrid_store.py --gpu <run dir> --out <scratch dir>
"""
import argparse
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import instrument as I  # noqa: E402
import gpu_equivalence as G  # noqa: E402
import knockout_regrow as K  # noqa: E402  (read-only)


def build_hybrid(gpu_run_dir, out_dir, ref=None, ref_info=None):
    out_dir = pathlib.Path(out_dir)
    refusal = I.out_dir_refusal(out_dir)
    if refusal:
        raise SystemExit(refusal)
    if out_dir.exists() and any(out_dir.iterdir()):
        raise SystemExit(f"REFUSED (G10): {out_dir} exists and is not empty")
    run_dir, manifest, planned = G.read_gpu_run(gpu_run_dir)
    if ref is None:
        ref, ref_info = G.load_reference()
    gpu = I.read_store(run_dir / manifest["files"]["records"])
    if sorted(gpu) != sorted(planned):
        raise SystemExit("REFUSED (G10): the GPU records do not match the manifest's keys")
    hyb = dict(ref)
    replaced_ko, replaced_ko1, kept_ko1_fitted = 0, 0, 0
    for rk, rec in gpu.items():
        if rk not in ref:
            raise SystemExit(f"REFUSED (G10): {rk} is not in the reference store")
        hyb[rk] = rec
        replaced_ko += 1
        bk, _, pk = I.split_record_key(rk)
        if I.is_base_view(bk):
            k1 = f"{bk}||ko1||{pk}"
            if k1 in ref:
                if ref[k1].get("reused_from_ko", False):
                    hyb[k1] = {**rec, "reused_from_ko": True}
                    replaced_ko1 += 1
                else:
                    kept_ko1_fitted += 1
    out_dir.mkdir(parents=True, exist_ok=True)
    I.write_json_gz(out_dir / "raw_fits.json.gz", hyb)
    prov = {"built_by": "hybrid_store.py (G10)", "gpu_run": str(run_dir),
            "gpu_label": manifest.get("label"), "gpu_head": manifest.get("git_head"),
            "reference": ref_info, "records": len(hyb), "gpu_ko_records": replaced_ko,
            "ko1_copies_replaced_by_gpu_ko": replaced_ko1,
            "ko1_fitted_records_kept_cpu": kept_ko1_fitted,
            "raw_fits_sha256": I.sha256_file(out_dir / "raw_fits.json.gz")}
    I.write_json(out_dir / "hybrid_provenance.json", prov)
    I.write_sha256sums(out_dir)
    return prov


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gpu", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    prov = build_hybrid(a.gpu, a.out)
    print(json.dumps(prov, indent=1), flush=True)


if __name__ == "__main__":
    main()
