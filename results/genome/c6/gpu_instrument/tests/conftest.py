"""Shared fixtures of the GPU instrument's tests (T-G1..T-G10 of the registration, section 10).

Run from the repository root with tools/.venv:
    tools/.venv/Scripts/python.exe -m pytest results/genome/c6/gpu_instrument/tests -q
The GPU tests (T-G1, T-G5, T-G6's subprocess part, T-G7) launch the torch venv
(instrument.TORCH_PY) as subprocesses; they are skipped if that interpreter or CUDA is absent.
Nothing here reads a real block or a sealed file: the fixtures are A's pinned synthetic store
(read-only, after check_prerun_files) and synthetic GPU runs.

One BLAS thread per process, set here before any test module imports numpy, as the instrument's
processes set it (prep, gpu_env, A's and the male script): a CPU fit made in the test process
(N1's degree terms, for one) differs in its last bits under another BLAS thread count.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import pathlib  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402

import pytest  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
GI = HERE.parent
if str(GI) not in sys.path:
    sys.path.insert(0, str(GI))

import instrument as I  # noqa: E402


@pytest.fixture(scope="session")
def K():
    import knockout_regrow
    return knockout_regrow


@pytest.fixture(scope="session")
def pinned(K):
    chk = K.check_prerun_files()
    assert chk["passed"], chk["reason"]
    return I.read_store(pathlib.Path(K.PRERUN_DIR) / "raw_fits.json.gz")


@pytest.fixture(scope="session")
def d1_keys(pinned):
    return [rk for rk in pinned if rk.split("||")[1] == "ko" and rk.split("||")[2].startswith("BF:")
            and "|pc:" not in rk]


def torch_available():
    if not I.TORCH_PY.is_file():
        return False
    r = subprocess.run([str(I.TORCH_PY), "-c", "import torch; print(torch.cuda.is_available())"],
                       capture_output=True, text=True)
    return r.returncode == 0 and r.stdout.strip() == "True"


needs_gpu = pytest.mark.skipif(not torch_available(), reason="torch venv or CUDA absent")


def run_torch(code, env=None, cwd=GI):
    import os
    e = dict(os.environ)
    for v in ("CUBLAS_WORKSPACE_CONFIG", "GPU_INSTRUMENT_FLAGS_OFF", "GPU_INSTRUMENT_DEVICE"):
        e.pop(v, None)
    e.update(env or {})
    return subprocess.run([str(I.TORCH_PY), "-c", code], capture_output=True, text=True,
                          cwd=cwd, env=e)
