"""The names engine v3 (gpu_bf3) takes from outside itself: DEVICE, DTYPE, H and _perturb_draws.

GPU instrument registration (docs/plans/2026-09-26-gpu-instrument-registration.md), G8 and D2:
the registered driver uses engine v3 only and asserts that gpu_bf (v1), gpu_bf2 (v2) and gpu_rule
are absent from sys.modules. At cdbde9e gpu_bf3.py:27 imported these four names from gpu_bf2,
which imports gpu_bf (gpu_bf2.py:26), so v3 could not be loaded without v1 and v2. This module
holds verbatim copies of the four definitions, so that gpu_bf3 imports neither:
  * DTYPE = torch.float64, as gpu_bf.py:32;
  * H, the harness module, imported read-only as gpu_bf.py:25-28 imports it (c6 and c6/checks on
    sys.path);
  * _perturb_draws and its cache, as gpu_bf2.py:28-37 (the PCG64(PERTURB_SEED_BASE + j) draws of
    harness.bf_als, in numpy);
  * DEVICE, as gpu_bf.py:31, with one addition: GPU_INSTRUMENT_DEVICE=cpu selects the torch CPU
    device (V5 (b) of the registration); any other value, or "cuda" with no CUDA device, refuses.
    gpu_bf.py:31 fell back to the CPU silently; a registered run must not.
The arithmetic of engine v3 is unchanged: the same values, the same draws, the same dtype.

Never reads, fits or scores the real block.
"""
import os
import pathlib
import sys

import numpy as np
import torch

HERE = pathlib.Path(__file__).resolve().parent
C6 = HERE.parent  # results/genome/c6
for _p in (str(C6), str(C6 / "checks")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import harness as H  # noqa: E402  (read-only import; not modified)

_DEVICE_NAME = os.environ.get("GPU_INSTRUMENT_DEVICE", "cuda")
if _DEVICE_NAME not in ("cuda", "cpu"):
    raise RuntimeError(f"REFUSED: GPU_INSTRUMENT_DEVICE={_DEVICE_NAME!r}; 'cuda' or 'cpu' only")
if _DEVICE_NAME == "cuda" and not torch.cuda.is_available():
    raise RuntimeError("REFUSED: no CUDA device, and the registered instrument never falls back "
                       "to the CPU (set GPU_INSTRUMENT_DEVICE=cpu only for V5 (b))")
DEVICE = torch.device(_DEVICE_NAME)
DTYPE = torch.float64

_DRAWS = {}


def _perturb_draws(r, j):
    if (r, j) not in _DRAWS:
        g = np.random.Generator(np.random.PCG64(H.PERTURB_SEED_BASE + j))
        zu = g.standard_normal((65, r))
        zv = g.standard_normal((65, r))
        _DRAWS[(r, j)] = (zu, zv)
    return _DRAWS[(r, j)]
