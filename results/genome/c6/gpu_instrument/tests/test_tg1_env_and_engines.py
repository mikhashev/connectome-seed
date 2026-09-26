"""T-G1 (G1, R2): in a subprocess, importing gpu_env then torch gives deterministic mode on and the
workspace variable in effect; importing torch first makes gpu_env refuse; a different
CUBLAS_WORKSPACE_CONFIG found refuses. Also G8 (D2): the registered driver's modules refuse to load
engines v1, v2 and the rule port, and engine v3 no longer imports them."""
from conftest import needs_gpu, run_torch


@needs_gpu
def test_gpu_env_first_sets_deterministic_mode():
    r = run_torch("import os, gpu_env, torch; "
                  "print(torch.are_deterministic_algorithms_enabled(), "
                  "torch.is_deterministic_algorithms_warn_only_enabled(), "
                  "os.environ['CUBLAS_WORKSPACE_CONFIG'], "
                  "torch.backends.cudnn.deterministic, torch.backends.cudnn.benchmark, "
                  "torch.backends.cuda.matmul.allow_tf32)")
    assert r.returncode == 0, r.stderr
    assert r.stdout.split() == ["True", "False", ":4096:8", "True", "False", "False"]


@needs_gpu
def test_torch_first_refuses():
    r = run_torch("import torch; import gpu_env")
    assert r.returncode != 0
    assert "REFUSED (G1)" in r.stderr


@needs_gpu
def test_numpy_first_refuses():
    r = run_torch("import numpy; import gpu_env")
    assert r.returncode != 0 and "REFUSED (G1)" in r.stderr


@needs_gpu
def test_other_workspace_value_refuses():
    r = run_torch("import gpu_env", env={"CUBLAS_WORKSPACE_CONFIG": ":16:8"})
    assert r.returncode != 0 and "REFUSED (G1, D6)" in r.stderr


@needs_gpu
def test_registered_value_found_is_accepted():
    r = run_torch("import os, gpu_env; print(gpu_env.SETTINGS['CUBLAS_WORKSPACE_CONFIG'])",
                  env={"CUBLAS_WORKSPACE_CONFIG": ":4096:8"})
    assert r.returncode == 0, r.stderr
    assert "':4096:8'" in r.stdout


@needs_gpu
def test_gpu_stage_refuses_without_gpu_env():
    r = run_torch("import gpu_stage")
    assert r.returncode != 0 and "REFUSED (G1)" in r.stderr


@needs_gpu
def test_g8_v3_only():
    r = run_torch("import sys, gpu_env, gpu_stage\n"
                  "assert all(m not in sys.modules for m in ('gpu_bf', 'gpu_bf2', 'gpu_rule'))\n"
                  "for m in ('gpu_bf', 'gpu_bf2', 'gpu_rule'):\n"
                  "    try:\n"
                  "        __import__(m)\n"
                  "    except ImportError as e:\n"
                  "        assert 'REFUSED (G8' in str(e)\n"
                  "    else:\n"
                  "        raise SystemExit('imported ' + m)\n"
                  "print('ok')")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "ok"


def test_g8_engine_v3_source_does_not_import_v1_v2():
    import pathlib
    src = (pathlib.Path(__file__).resolve().parents[1] / "gpu_bf3.py").read_text(encoding="utf-8")
    assert "from gpu_bf2" not in src and "import gpu_bf2" not in src
    assert "from gpu_common import DEVICE, DTYPE, H, _perturb_draws" in src
