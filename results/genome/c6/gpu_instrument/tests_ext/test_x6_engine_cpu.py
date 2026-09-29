"""T-X6: ext_engine.run_core runs end to end on the torch CPU device (GPU_INSTRUMENT_DEVICE=cpu,
CUDA_VISIBLE_DEVICES empty, gpu_env imported first), on arm B's world:R:0: block at rank 1, ko1
at ranks 1 and 4, twice each. Planned keys, lambda, per-fit hashes equal across the two runs, and
the comparator's outcome 1 against B's pinned store are asserted; bit-equality of p is printed,
not asserted. A test of the plumbing, not a validation: VX1 and VX2 run on the GPU.
"""
import json
import os
import subprocess
import sys

import ext_compare as XK
import ext_scope as XS
from conftest import GI

SCRIPT = r"""
import gpu_env
import json
import prep, ext_prep as XP, ext_engine as XE, ext_scope as XS
name = XS.ARMS["B"]
K = prep.set_arm(name, None)
prep.init_arm_worker(name, None, K.degree_terms())
out = {}
for mask, ranks in (("block", (1,)), ("ko1", (1, 4))):
    runs = []
    for rep in range(2):
        preps = [XP.prepare_key_ext("world:R:0", mask)]
        res, info = XE.run_core(["world:R:0"], preps, mask, ranks, 10, 40000,
                                lambda t: XP.decode_records_ext(t), log=lambda m: None)
        runs.append({rk: {"rec": rec, "h": h} for _, (rk, rec, h) in res})
    out[mask] = {"runs": runs, "per": info["per"], "n_folds": info["n_folds"]}
print("JSON=" + json.dumps(out))
"""


def _run():
    env = dict(os.environ)
    for v in ("CUBLAS_WORKSPACE_CONFIG", "GPU_INSTRUMENT_FLAGS_OFF", "OMP_NUM_THREADS",
              "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        env.pop(v, None)
    env.update(GPU_INSTRUMENT_DEVICE="cpu", CUDA_VISIBLE_DEVICES="", PYTHONUTF8="1")
    r = subprocess.run([sys.executable, "-c", SCRIPT], cwd=GI, capture_output=True, text=True,
                       env=env, timeout=1800)
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-3000:]
    line = [ln for ln in r.stdout.splitlines() if ln.startswith("JSON=")][0]
    return json.loads(line[5:])


def test_x6_engine_on_torch_cpu(ref_B, K_B):
    out = _run()
    ref = ref_B[0]
    assert (out["block"]["per"], out["block"]["n_folds"]) == (11, 10)
    assert (out["ko1"]["per"], out["ko1"]["n_folds"]) == (1, 0)
    for mask, ranks in (("block", (1,)), ("ko1", (1, 4))):
        a, b = out[mask]["runs"]
        planned = XS.planned(["world:R:0"], mask, ranks)
        assert sorted(a) == sorted(planned) == sorted(b)
        assert all(a[k]["h"] == b[k]["h"] for k in planned)
        got = {k: a[k]["rec"] for k in planned}
        if mask == "ko1":
            assert all(got[k]["lam"] == 1.0 for k in planned)
        rep = XK.compare_records(got, ref, K_B, planned, scope=f"T-X6 {mask}")
        print(f"{mask}: outcome {rep['outcome']}; not bit-equal {rep['n_not_bit_equal']} of "
              f"{rep['n_fits']}; {[d['max_abs_dp'] for d in rep['differing_fits']]}")
        assert rep["outcome"] == 1, rep["outcome_text"]
