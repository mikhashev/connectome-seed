# Brief — machine state in the run json

**Date:** 2026-09-17. Not applied. Patch: `docs/briefs/2026-09-17-run_individual-machine-state.patch`,
a unified diff against `tools/night/run_individual.py` at commit `a8a800813448ec2979a717a380a58955a17fea6a`
(sha256 `4aafb2c481551e2b51a7ca65f02a04fd691c81d80a14a591b72688b8534e7d5d`, matches the file on disk —
verified with `sha256sum`); `git apply --check` against the current file passes. `git diff --numstat`:
55 lines added, 0 deleted, one file. Origin: Ark and Zcode, chat 2026-09-17 — record fields in each
run json, at start and end, that could separate run groups.

## What it adds

One new function, `_machine_state()`, and two call sites. All five fields go through their own
`try/except`, so a missing tool degrades that one field to `{"error": repr(e)}` and never raises out
of the function — the run cannot fail because a system query failed:

- `nvidia_smi_compute_processes` — `nvidia-smi --query-compute-apps=pid,process_name,used_memory
  --format=csv,noheader` (pid, name, used memory per compute process).
- `nvidia_smi_memory_used_total_driver` — `nvidia-smi --query-gpu=memory.used,memory.total,driver_version
  --format=csv,noheader` (total memory used + driver version in one call).
- `uptime_s` — `ctypes.windll.kernel32.GetTickCount64() / 1000.0` (no subprocess needed on Windows).
- `hostname` — `socket.gethostname()`.
- `other_python_processes` — PowerShell `Get-CimInstance Win32_Process | Where-Object { $_.Name -match
  'python' } | ForEach-Object { "$($_.ProcessId) | $($_.CommandLine)" }`, each line truncated to 300
  chars. This is the same query family (`Get-CimInstance Win32_Process`, PowerShell) the C3 executor
  used for `results/diagnostics/c3/machine_state.json`'s `python_processes` field, which prints
  `PID | CommandLine` lines the same way.

Every external call carries `timeout=10` (subprocess) and is read-only (no `-Confirm`, no writes, no
`taskkill`). Two new json keys only: `machine_state_start`, `machine_state_end` — no existing key is
renamed, reordered, or changed in type.

## Where, and why the training path is unchanged

`_machine_state()` is a pure function: it takes no arguments derived from training state and returns
a dict; nothing it touches is read by training code. The two call sites:

1. `rec["machine_state_start"] = _machine_state()` — inserted right after `solver.penalty.__class__ =
   PenaltyHooked` and *before* the `# ---- train ----` block's re-seeding (`random.seed`, `np.random.seed`,
   `torch.manual_seed`) and before `state["train_start"] = time.perf_counter()`. It runs, then a `dump()`
   (already an existing, idempotent pattern used elsewhere in the file), then the reseed happens exactly
   as before — so even though the call spends wall time on subprocesses, that time is spent *before* the
   seed is (re-)set and *before* the training clock starts, so RNG state at training start and every
   reported wall-clock figure (`total_train_wall_s`, `iter_wall_s`, …) are unaffected.
2. `rec["machine_state_end"] = _machine_state()` — inserted inside the existing `finally:` block, after
   `end = time.perf_counter()` and `rec["total_train_wall_s"]` are already computed from that captured
   `end`, and after the `train_loss_per_iter` read, immediately before `rec["finished_utc"]` and the
   final `dump()`. Training (`solver.train(...)`) has already returned or raised by this point, so the
   call is strictly after training ends, on both the success and the error path (the `finally:` block
   runs either way) — matching the requirement to record it "at start and at end" of each run.

argv is unaffected: no new CLI argument is added, so `parse_args()` output on any recorded argv (e.g.
night 4's `rep_9991-903.slim.json`) is byte-identical before and after this patch — unlike the
`--stop-after-iter` patch (`docs/briefs/2026-09-17-c3-run_individual.patch`, commit `a8a8008`), which
did add one key (`stop_after_iter: None`) and whose argv-diff check is the model this brief follows.

## What changes about the output

The run json is **not** byte-identical to before: two new top-level keys, `machine_state_start` and
`machine_state_end`, each a dict of the five fields above (or `{"error": ...}` per field on failure).
No existing key's value changes; the two extra `dump()`-triggering writes do not change cadence.

**CC review 2026-09-17:** `GetTickCount64` needs `restype = ctypes.c_uint64`; with ctypes' default `c_int` the 64-bit millisecond count is truncated and wraps after ~24.8 days of uptime. Fixed in the committed patch (+3 lines instead of +1); the base-file hash and `git apply --check` were re-verified.
