"""G1 and G2 of the GPU instrument registration: imported FIRST by every registered GPU entry point.

docs/plans/2026-09-26-gpu-instrument-registration.md, revision 1.3: D6 (a), D7 (i), R1-R3.

On import, in this order:
  1. refuses if numpy or torch is already imported (the thread preamble and the cuBLAS workspace
     variable must precede them; T-G1);
  2. the thread preamble (R3): the four thread variables as found, then setdefault "1" (A's
     THREAD_ENV_FOUND form, knockout_regrow.py:84-90);
  3. CUBLAS_WORKSPACE_CONFIG=:4096:8 before torch is imported; a different value found refuses;
  4. imports torch and sets torch.use_deterministic_algorithms(True) (no warn_only), TF32 off for
     matmul and cuDNN, cudnn.deterministic = True, cudnn.benchmark = False;
  5. reads every setting back and refuses if any differs (R2).
The values set and read back are in SETTINGS. A RuntimeError raised later by a non-deterministic
operation stops the run (R2); nothing here catches it.

One exception, for V0's comparison run only: GPU_INSTRUMENT_FLAGS_OFF=1 skips 3 and 4 (the flag-free
state of the runs of section 2). The driver refuses it outside V0 (run_registered.py), and the
manifest records it.

environment_record() is G2's record (python, numpy with show_config and threadpoolctl, torch, CUDA,
cuDNN, the sha256 of the three bundled CUDA DLLs, GPU name, compute capability, total VRAM, driver
from nvidia-smi, torch threads, thread variables, the determinism settings); stamp() extracts the
fields of D7's stamp, which instrument.check_stamp compares with the registered one (R1).
"""
import os
import sys

_already = [m for m in ("numpy", "torch") if m in sys.modules]
if _already:
    raise RuntimeError(f"REFUSED (G1): {', '.join(_already)} imported before gpu_env; gpu_env "
                       "must be the first import of a registered GPU entry point (the thread "
                       "preamble and CUBLAS_WORKSPACE_CONFIG must precede numpy and torch)")

THREAD_VARS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")
THREAD_ENV_FOUND = {_v: os.environ.get(_v) for _v in THREAD_VARS}
for _v in THREAD_VARS:
    os.environ.setdefault(_v, "1")

CUBLAS_VAR = "CUBLAS_WORKSPACE_CONFIG"
CUBLAS_REQUIRED = ":4096:8"
CUBLAS_FOUND = os.environ.get(CUBLAS_VAR)
FLAGS_OFF = os.environ.get("GPU_INSTRUMENT_FLAGS_OFF", "") not in ("", "0")

if not FLAGS_OFF:
    if CUBLAS_FOUND is not None and CUBLAS_FOUND != CUBLAS_REQUIRED:
        raise RuntimeError(f"REFUSED (G1, D6): {CUBLAS_VAR}={CUBLAS_FOUND!r} found; the "
                           f"registered value is {CUBLAS_REQUIRED!r}")
    os.environ[CUBLAS_VAR] = CUBLAS_REQUIRED

import hashlib  # noqa: E402
import pathlib  # noqa: E402
import platform  # noqa: E402
import subprocess  # noqa: E402

import numpy as np  # noqa: E402
import torch  # noqa: E402

if not FLAGS_OFF:
    torch.use_deterministic_algorithms(True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def read_settings():
    """R2: the determinism settings as read back from torch and the environment."""
    return {"flags_off_for_V0_comparison": FLAGS_OFF,
            "CUBLAS_WORKSPACE_CONFIG": {"found": CUBLAS_FOUND,
                                        "in_effect": os.environ.get(CUBLAS_VAR)},
            "use_deterministic_algorithms": torch.are_deterministic_algorithms_enabled(),
            "deterministic_warn_only": torch.is_deterministic_algorithms_warn_only_enabled(),
            "cuda_matmul_allow_tf32": torch.backends.cuda.matmul.allow_tf32,
            "cudnn_allow_tf32": torch.backends.cudnn.allow_tf32,
            "cudnn_deterministic": torch.backends.cudnn.deterministic,
            "cudnn_benchmark": torch.backends.cudnn.benchmark,
            "float32_matmul_precision": torch.get_float32_matmul_precision(),
            "tf32_note": "TF32 does not touch float64: recorded, not relied on (D6 (a))"}


SETTINGS = read_settings()
if not FLAGS_OFF:
    _want = {"use_deterministic_algorithms": True, "deterministic_warn_only": False,
             "cuda_matmul_allow_tf32": False, "cudnn_allow_tf32": False,
             "cudnn_deterministic": True, "cudnn_benchmark": False}
    _bad = {k: SETTINGS[k] for k, v in _want.items() if SETTINGS[k] != v}
    if SETTINGS["CUBLAS_WORKSPACE_CONFIG"]["in_effect"] != CUBLAS_REQUIRED:
        _bad["CUBLAS_WORKSPACE_CONFIG"] = SETTINGS["CUBLAS_WORKSPACE_CONFIG"]
    if _bad:
        raise RuntimeError(f"REFUSED (R2): determinism settings read back wrong: {_bad}")


def thread_record():
    """R3: the four thread variables as found and in effect, and torch's thread count."""
    return {"thread_env": {v: {"found": THREAD_ENV_FOUND[v], "in_effect": os.environ.get(v)}
                           for v in THREAD_VARS},
            "torch_num_threads": torch.get_num_threads(),
            "torch_num_interop_threads": torch.get_num_interop_threads()}


def numpy_record():
    """numpy's build (show_config) and the BLAS loaded at run time (threadpoolctl), as A's
    machine_record; used in the main process and in one prep worker (G2)."""
    rec = {"numpy": np.__version__}
    try:
        cfg = np.show_config(mode="dicts")
        rec["numpy_build"] = {k: cfg.get("Build Dependencies", {}).get(k)
                              for k in ("blas", "lapack")}
    except Exception as e:                                  # recorded, never fatal
        rec["numpy_build"] = {"error": repr(e)}
    try:
        import threadpoolctl
        rec["blas_at_run_time"] = [{**i, "filepath": os.path.basename(i.get("filepath") or "")}
                                   for i in threadpoolctl.threadpool_info()]
    except Exception as e:
        rec["blas_at_run_time"] = {"error": repr(e)}
    return rec


def _dll_hashes():
    lib = pathlib.Path(torch.__file__).parent / "lib"
    out = {}
    for name in ("cublas64_12.dll", "cublasLt64_12.dll", "cusolver64_11.dll"):
        p = lib / name
        out[name] = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
    return out


def _driver_version():
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader",
                            "-i", "0"], capture_output=True, text=True, check=True, timeout=60)
        return r.stdout.strip().splitlines()[0].strip()
    except Exception as e:
        return f"unavailable: {e!r}"


def environment_record():
    """G2: the environment of this process."""
    cuda = torch.cuda.is_available()
    rec = {"python": platform.python_version(), **numpy_record(),
           "torch": torch.__version__, "cuda": torch.version.cuda,
           "cudnn": torch.backends.cudnn.version(), "dll_sha256": _dll_hashes(),
           "driver": _driver_version() if cuda else None,
           "gpu_name": torch.cuda.get_device_name(0) if cuda else None,
           "compute_capability": list(torch.cuda.get_device_capability(0)) if cuda else None,
           "total_vram_bytes": torch.cuda.get_device_properties(0).total_memory if cuda else None,
           "machine": {"machine": platform.machine(), "processor": platform.processor(),
                       "platform": platform.platform(), "cpu_count": os.cpu_count()},
           "determinism": read_settings(), **thread_record()}
    return rec


def stamp(rec=None):
    """D7's stamp: the fields instrument.STAMP_FIELDS of the environment record."""
    rec = environment_record() if rec is None else rec
    return {"python": rec["python"], "numpy": rec["numpy"], "torch": rec["torch"],
            "cuda": rec["cuda"], "dll_sha256": dict(rec["dll_sha256"]),
            "driver": rec["driver"], "gpu_name": rec["gpu_name"]}
