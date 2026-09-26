"""T-G5 (the poisoned block) and T-G7 (two subprocess runs agree), seconds of GPU each.

T-G5: with the block cells of harness.REAL flipped in the main process and every prep worker, the
per-fit hashes of one world's base view and 5 shuffles are unchanged, and so is the degree-term
digest (V7 repeats it on 99 shuffles).
T-G7: two subprocess runs of one world's base view and 5 shuffles give equal hashes.
The runs are validation runs of the registered driver (run_registered.py) into pytest's tmp
folders, marked --allow-dirty and --stamp-unregistered while the tree is uncommitted and no stamp
is registered.
"""
import json
import os
import subprocess

import pytest

import instrument as I
from conftest import GI, needs_gpu

KEYS = "world:R:0,world:R:0|sh:0,world:R:0|sh:1,world:R:0|sh:2,world:R:0|sh:3,world:R:0|sh:4"


def _run(label, out, extra=()):
    env = dict(os.environ)
    for v in ("CUBLAS_WORKSPACE_CONFIG", "GPU_INSTRUMENT_FLAGS_OFF", "GPU_INSTRUMENT_DEVICE",
              "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
              "NUMEXPR_NUM_THREADS"):
        env.pop(v, None)
    args = [str(I.TORCH_PY), "run_registered.py", "--kind", "validation", "--label", label,
            "--keys", KEYS, "--workers", "6", "--allow-dirty", "--out", str(out)]
    if I.REGISTERED_STAMP is None:
        args.append("--stamp-unregistered")
    r = subprocess.run(args + list(extra), cwd=GI, capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-3000:]
    return (json.loads((out / "fit_hashes.json").read_text(encoding="utf-8")),
            json.loads((out / "manifest.json").read_text(encoding="utf-8")))


@pytest.fixture(scope="module")
def clean_run(tmp_path_factory):
    return _run("T-G5", tmp_path_factory.mktemp("tg5") / "clean")


@needs_gpu
def test_tg5_poisoned_block_changes_nothing(clean_run, tmp_path):
    h0, m0 = clean_run
    h1, m1 = _run("T-G5-poison", tmp_path / "poisoned", ["--poison-real-block"])
    assert m1["overrides"]["poison_real_block"]["removed"] + \
        m1["overrides"]["poison_real_block"]["added"] == 64
    assert m1["environment_prep_worker"]["arm"]["poisoned"] is not None
    assert len(h0) == 24 and h1 == h0
    assert m1["degree_terms_digest"] == m0["degree_terms_digest"]


@needs_gpu
def test_tg7_two_runs_equal(clean_run, tmp_path):
    h0, m0 = clean_run
    h1, m1 = _run("T-G7", tmp_path / "second")
    assert h1 == h0
    assert m1["composition"]["refusal_digest"] == m0["composition"]["refusal_digest"]


@needs_gpu
def test_poison_refused_outside_its_runs(tmp_path):
    env = dict(os.environ)
    env.pop("CUBLAS_WORKSPACE_CONFIG", None)
    r = subprocess.run([str(I.TORCH_PY), "run_registered.py", "--kind", "validation", "--label",
                        "V1", "--keys", "world:R:0", "--poison-real-block", "--allow-dirty",
                        "--stamp-unregistered", "--out", str(tmp_path / "x")], cwd=GI,
                       capture_output=True, text=True, env=env)
    assert r.returncode != 0 and "--poison-real-block outside V7" in (r.stdout + r.stderr)
    r = subprocess.run([str(I.TORCH_PY), "run_registered.py", "--kind", "arm", "--label", "x",
                        "--keys", "world:R:0", "--out", str(tmp_path / "y")], cwd=GI,
                       capture_output=True, text=True, env=env)
    assert r.returncode != 0 and "--expect-digest" in (r.stdout + r.stderr)
