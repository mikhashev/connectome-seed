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

## Applied 2026-09-17

Authority: Mike, chat #247 «да», 2026-09-17 08:19:01Z. Reviewer pass: Ark 08:27:19Z (design green,
one addition — `boot_time_utc` — plus two checks), Zcode 08:28:59Z (green; default path byte-identical
by argv check, new fields only in json). Base hash reverified `4aafb2c481551e2b51a7ca65f02a04fd691c81d80a14a591b72688b8534e7d5d`,
`git apply` clean (no `--check` needed, applied directly, no reject).

**Ark's addition — `boot_time_utc`:** added inside `_machine_state()`, its own `try/except`, placed
right after the `uptime_s` try-block and before `hostname`. Computed only when `uptime_s` succeeded
(`isinstance(state.get("uptime_s"), (int, float))`); otherwise `{"error": "uptime_s unavailable"}`.
Value: `time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - uptime_s))` — no new import
(reuses the `time` module and the same ISO-string convention the file already uses for `finished_utc`),
matching "ISO format, computed only if uptime_s succeeded (else `{"error": ...}`), inside its own try."

**Ark's check (a) — call-site placement (line numbers post-patch):**
`rec["machine_state_start"] = _machine_state()` is at line 699, followed by `dump()` at line 700.
The training re-seed block — `random.seed(a.seed)` (703), `np.random.seed(a.seed)` (704),
`torch.manual_seed(a.seed)` (705) — and the training clock start —
`state["train_start"] = state["last_t"] = time.perf_counter()` (708) — all come strictly after.
**Confirmed: `machine_state_start` runs before both the reseed and the training clock.**
`rec["machine_state_end"] = _machine_state()` is at line 749, inside the existing `finally:` block,
after `end = time.perf_counter()` and `rec["total_train_wall_s"]` are already computed (line 727) —
i.e. strictly after `solver.train(...)` has returned or raised, on both the success and error path.

**Ark's check (b) — no `shell=True`:** four `subprocess.run` calls total in the file (line 141,
pre-existing `nvidia_smi_used_mib`; lines 160, 169, 196, the three new ones inside `_machine_state()`).
All four pass an argument list as the first positional arg (e.g. `["nvidia-smi", "--query-compute-apps=...", ...]`,
`["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", "..."]`) and none sets `shell=True`.
`grep -n "shell" tools/night/run_individual.py` returns exactly one line (197, the substring "shell"
inside the literal `"powershell.exe"`) — zero occurrences of the `shell=` keyword argument anywhere
in the file. **Confirmed: no `shell=True`, nvidia-smi's CSV output is read from `out.stdout`, not
shell-expanded.**

**Verification (CPU only, all via the flyvis-probe venv python unless noted):**
- `python -m py_compile tools/night/run_individual.py` — compiles clean, no output.
- `parse_args()` byte-identity check: loaded the pre-patch file (`git show HEAD:...` at commit
  `aebbe3a`, sha256 `dbe248a1edd437eb02b0cf18a82b34f2edbd8772e02472d3d73f9e7d869e441c`, confirmed
  equal to the recorded base `4aafb2c4...` via `git stash`/`sha256sum` before the patch was reapplied)
  and the post-patch file as two separately-named modules via `importlib.util.spec_from_file_location`,
  ran `parse_args()` on both with `sys.argv` set to night 4's recorded argv
  (`results/night4/rep_9991-903.slim.json` field `argv`: `--seed 3 --id 9991/903 --n-iters 250000
  --rungs 1000,5000,25000,250000 --tag rep --out-dir ... --no-determinism --progress-every 100
  --progress-file ...`). Result: `keys equal: True`, `values equal: True` — `vars(args)` dicts are
  identical. Confirms argv is unaffected by the patch, as designed (no new CLI argument).
- Standalone `_machine_state()` call, venv python
  `...\63f3961a-...\scratchpad\flyvis-probe\.venv\Scripts\python.exe`, via a scratch loader script
  under `...\03852100-...\scratchpad\ms_check\call_machine_state.py`. Output (abbreviated —
  `nvidia_smi_compute_processes` is a long per-process CSV list, elided here):
  ```
  nvidia_smi_memory_used_total_driver: "2984 MiB, 32623 MiB, 596.86"
  uptime_s: 205602.328
  boot_time_utc: "2026-09-14T23:31:17Z"
  hostname: "mike"
  other_python_processes: [4 lines, PID | CommandLine, each <=300 chars]
  ```
  All five fields returned real values, no `{"error": ...}` on this machine (nvidia-smi, PowerShell,
  and `GetTickCount64` all succeeded).
- `git diff --numstat -- tools/night/run_individual.py`: `65  0` — 65 insertions (55 from the reviewed
  patch + 10 for `boot_time_utc`), **0 deletions**.

**sha256 after patch (repo file):** `be007c744648ab15a59df222a1753d1ada95b2596afb5e0784784fe9fa6a0a93`.
Copied to the scratchpad night dir
(`...\63f3961a-...\scratchpad\flyvis-probe\night\run_individual.py`) — `sha256sum` on both paths
returns the same value, confirmed byte-identical.

No GPU work, no training run; all checks above ran on CPU / read-only system queries.
