"""Fixtures of extension X's tests (block mask and fixed lambda; draft, not registered).

Run from the repository root with tools/.venv, CPU only:
    tools/.venv/Scripts/python.exe -m pytest results/genome/c6/gpu_instrument/tests_ext -q
This folder is separate from tests/ on purpose: tests/conftest.py probes the torch venv for CUDA
at import (needs_gpu), and these tests must not touch the GPU at all. The one engine test runs
engine v3 on the torch CPU device (GPU_INSTRUMENT_DEVICE=cpu, CUDA_VISIBLE_DEVICES=-1) in a subprocess of tools/.venv;
the device is hidden. Run the suite itself with CUDA_VISIBLE_DEVICES=-1 as well. Fixtures: A's and B's pinned synthetic stores (read-only, after each arm's
check_prerun_files) and B's registered run's synthetic store (read-only, by its sha256). No real
block and no real-arm store is read.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import pathlib  # noqa: E402
import sys  # noqa: E402

import pytest  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
GI = HERE.parent
if str(GI) not in sys.path:
    sys.path.insert(0, str(GI))

import instrument as I  # noqa: E402  (puts c6 and c6/checks on sys.path)
import ext_scope as XS  # noqa: E402


@pytest.fixture(scope="session")
def ref_A():
    return XS.load_reference("A", "pinned")


@pytest.fixture(scope="session")
def ref_B():
    return XS.load_reference("B", "pinned")


@pytest.fixture(scope="session")
def ref_B_registered():
    return XS.load_reference("B", "registered")


@pytest.fixture(scope="session")
def K_A():
    return XS.arm_module("A")


@pytest.fixture(scope="session")
def K_B():
    return XS.arm_module("B")
