# tools/night — the overnight run tooling

Copied into the repository 2026-09-14 from the session scratchpad
(`flyvis-probe/night/`), where it was built and exercised on 2026-09-13. Board:
[[THE-NIGHT-TOOLING-LIVES-IN-A-TEMPORARY-SCRATCHPAD]]. Scripts only — logs, per-run json/h5
outputs and the venv itself are not part of this commit.

## What each script does

- **`run_individual.py`** — one flyvis individual = one full training run to `--n-iters`
  (default 250,000), with held-out evaluation rungs. Composes the default `flow` config exactly
  as `flyvis train-single` does, then adds (without touching flyvis/datamate on disk): seed
  control (`network.node_config.bias.seed=<seed>` plus manual `random`/`numpy`/`torch` seeding
  for decoder init, data order and augmentation — stock flyvis seeds only the resting-potential
  init); optional determinism flags (`--no-determinism` to turn them off, as used for every run
  so far); a rung hook that runs `solver.test()` on the held-out split at exactly the requested
  iterations without disturbing the schedule; progress lines (`--progress-every`,
  `--progress-file`) with START/iteration/RUNG/CHECKPOINT/DONE markers; `--override` for Hydra
  config overrides (e.g. extent). Writes `<out-dir>/<tag>_<id>.json/.log/.stdout.log`.
- **`launch_wave.py`** — launches one or more `run_individual.py` processes and waits for them.
  Seed/id mapping: seed `s` → id `<ensemble>/<s:03d>`. `--replicate` adds run 0′: seed 0, id
  `<ensemble>/900`, tag `rep`, queued right after seed 0 when seed 0 is in `--seeds`.
  `--sequential` runs one at a time (used for every night so far — the card holds only one
  run at full speed, m = 1, board [[EIGHT-PROCESSES-SHARE-THE-CARD-NO-FASTER-THAN-ONE]]).
  `--detach` re-spawns itself as a detached Windows process so the runs survive the launching
  shell, writing `wave_<tag>.pid`, `wave_<tag>.progress.log` and `wave_<tag>.json` (rewritten
  after every launch/exit). `--dry` prints the exact command lines and starts nothing.
- **`start_night.ps1`** — the operator entry point (Windows PowerShell 5.1; no `&&`, no `??`, no
  ternary). Builds the `launch_wave.py` command line, prints it and the PID/log file paths, then
  either dry-runs (`-DryRun`), launches and follows the progress log, or just follows an
  existing wave (`-FollowOnly`). Parameters: `-Tag -Ensemble -Seeds -NIters -Rungs
  -ProgressEvery -Extent -FollowSeconds`, and `-NoReplicate` (added 2026-09-14) to omit
  `--replicate` — used for night 2, which runs two new seeds with no paired replicate.
- **`night_report.py`** — the morning report. Reads a `run_individual.py` json for run 0 (`--a`)
  and, if present, its replicate (`--b`); prints the two-phase price, the rung table, the
  replicate difference per rung, the full checkpoint trajectory (also written as a `.csv`
  alongside the report) and the per-run checkpoint-detail block (plateau, rung-vs-checkpoint
  jitter). Handles a missing or partial `--b` file.

## Environment recipe (verified on the live venv, 2026-09-14)

The venv lives at `<probe-root>/.venv` outside this repository (session scratchpad
`flyvis-probe/.venv` at record time) and is **not relocatable** — a `uv venv` bakes in absolute
paths. Re-create it from this recipe; this board entry
([[THE-NIGHT-TOOLING-LIVES-IN-A-TEMPORARY-SCRATCHPAD]]) stays open until that has been done
outside the scratchpad.

- **Python:** 3.10.20 (`python --version`, the live venv).
- **Package manager:** `uv` was used to create the venv and install packages.
- **torch:** `torch==2.9.1+cu128` from `https://download.pytorch.org/whl/cu128`
  (`import torch; torch.__version__` → `2.9.1+cu128`, `torch.version.cuda` → `12.8`).
- **torchvision:** `torchvision==0.24.1+cu128`, same index.
- **flyvis:** `flyvis==1.2.0` (`importlib.metadata.version("flyvis")`).
- **datamate:** `1.0.0` (`importlib.metadata.version("datamate")`) — flyvis's storage layer, a
  separate package under the same GitHub organisation; needs the Windows patch below.

Recipe, in order:

```powershell
uv venv .venv
.venv\Scripts\python.exe -m pip install torch==2.9.1+cu128 torchvision==0.24.1+cu128 `
    --index-url https://download.pytorch.org/whl/cu128
.venv\Scripts\python.exe -m pip install flyvis==1.2.0
# then apply the datamate patch below to <venv>\Lib\site-packages\datamate\io.py
```

### The datamate Windows patch

`datamate` unlinks an HDF5 file while an `h5py` handle on it is still open — allowed on Linux,
`WinError 32` on Windows. Board:
[[DATAMATE-UNLINKS-AN-OPEN-HDF5-FILE-AND-WINDOWS-REFUSES]] (upstream issue not yet filed).
Marker `windows-patch (CC, 2026-09-13)`, one occurrence in the live venv,
`<venv>\Lib\site-packages\datamate\io.py:169` (±12 lines, `_write_h5`):

```python
    val = np.asarray(val)
    try:
        f = h5.File(path, libver="latest", mode="w")
        if f["data"].dtype != val.dtype:
            raise ValueError()
        f["data"][...] = val
        f.swmr_mode = True
        assert f.swmr_mode
    except Exception:
        # windows-patch (CC, 2026-09-13): unlinking a file that still has an open
        # h5py handle is allowed on Linux and raises WinError 32 on Windows.
        try:
            f.close()
        except Exception:
            pass
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.is_dir():
            path.rmdir()
        elif path.exists():
            try:
                path.unlink()
            except FileNotFoundError:
```

The same close-before-unlink shape is needed in `_extend_h5`'s `_override_to_chunked` helper
(same file, the `f.close()` / `path.unlink()` pair immediately before the recursive
`_extend_h5(path, data)` call) — apply the same `try/except Exception: pass` around `f.close()`
there before `path.unlink()`.

### Environment variable

`FLYVIS_ROOT_DIR` must point at the data root before any run:

```powershell
$env:FLYVIS_ROOT_DIR = "C:/Users/mikha/Documents/dpc-research/connectome-seed-data"
```

(`start_night.ps1` sets this itself.) Outputs land under
`connectome-seed-data/results/flow/<ensemble>/<seed:03d>/` (or `/900/` for the replicate) — h5
checkpoints, activity, loss, per-iteration and per-checkpoint records; `datamate` NetworkDir
layout.

## Launch commands

**Night 1** (run 0 + replicate, 2026-09-13, Mike's own PowerShell command):

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\night\start_night.ps1 `
    -Tag night1 -Ensemble 9991 -Seeds 0
```

(`--replicate` is on by default; run 0′ — id `9991/900` — followed run 0 automatically.)

**Night 2** (seeds 1 and 2, no replicate, on Mike's word — see `docs/next-session-plan.md`):

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\night\start_night.ps1 `
    -Tag night2 -Ensemble 9991 -Seeds 1,2 -NoReplicate
```

Dry-run first (`-DryRun` added to either command) to confirm the exact command and the ids
before anything starts.

## Frozen requirements

`tools/night/requirements-frozen.txt` is a `uv pip freeze` of the live `tools/.venv`
taken 2026-09-20, after the venv itself was copied into the repo. It records exactly
what is installed, for comparison if the venv ever needs rebuilding — it is not a
`pip install -r` recipe, since torch needs the cu128 index above and datamate needs
the Windows patch above; neither survives a plain freeze/restore.
