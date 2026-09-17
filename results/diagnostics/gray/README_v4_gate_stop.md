# Gray-stimulus control, v4: STOPPED AT A DOCUMENTED CEILING (16-item mean)

**Status: PREVIEW DIAGNOSTIC -- NOT A TEST.** Protocol:
`docs/briefs/2026-09-16-step1-gray-stimulus.md` **v4** (commit `f915d59`; Ark 20:23Z and Zcode
20:24Z accepted it). Launched on Mike's explicit word in the DPC Research chat,
2026-09-17 08:14:48Z: «@CC_windows «запускай шаг 1». **Run by:** a CC subagent (Opus),
2026-09-17 08:17-08:25Z. The earlier records are kept unchanged: `README_v2_gate_stop.md` and
`README_v31_gate_stop.md` (the v3.1 README, renamed in this directory, content unchanged).

> **The 48-cell sweep was NOT run.** The v4 **code gate passed** (§3). At `chkpt_00071` of run
> 000, the recorded copy-vs-original numbers breached one of the two documented ceilings of brief
> §6 v4. The copy with the identity transform (A) and one of the five original calls (B_1) differ
> on the 16-item mean by |mean(A) − mean(B_1)| = **`0.0001201629638671875`**, and the ceiling is
> 1e-4. The per-item ceiling (0.00146484375) held, and P0 passed at both checkpoints. The
> executor's instruction was to stop and report on a ceiling breach, so the run stopped there. The
> constant-output null, the main sweep, the fresh-process repeat and the readings were not run.
> After the stop, no GPU work of any kind was run.

Nothing was committed or pushed. No file outside this directory and the executor's scratchpad
was written. No training was run. No ablation hook was registered: `net._state_hooks == ()` was
asserted before and after the copy, after each of the five original calls, and after `hook_eval`.
Nothing is rounded: every number below is the `repr` string the script printed.

---

## 1. Files in this directory

| file | what | sha256 |
|---|---|---|
| `gray_stimulus.py` | the driver, updated to v4 (§2). **Uncommitted modification** of the committed v3.1 file (`939ee537…`) | `2c66e661a142823b743014602adbe756e9966d058de775e6dc5fa02c5b951422` |
| `gray_v4_main_gate_stop.log` | full stdout+stderr of the one `--task main` invocation, verbatim, including the code-gate diff and both CONTROL records with raw per-item vectors | `2a95313050923683d56332ce6c28901067a2355dfd5c11819e41570a9eb30883` |
| `README_v31_gate_stop.md` | the v3.1 run's README, renamed, content unchanged | `c4f65d3408a45c084061719c4225a5cd10969f4736facefb50475f1c0012dd77` |
| `README_v2_gate_stop.md` | the v2 run's README, unchanged | `5a65ed078b2205b826cf48c0515d86dc093e3a3f49c89ff2d52b7781a3d6b921` |
| `gray_control_v31_gate_stop.log` | the v3.1 log, unchanged | `bca46bae35420ab4e39b67dd8773b1e8349e1fbf92d2f43b9540483c02bd0de8` |
| `README.md` | this file | n/a |

The brief's §5 outputs (`gray_losses.csv`, `gray_controls.json`, `gray_repeat_controls.json`,
`gray_readings.json`) **do not exist**. `--task main` writes nothing when it stops before the sweep
(unchanged behaviour since v3.1). The code-gate diff that §6 v4 routes into `gray_controls.json`
is therefore recorded in the log and in §3 below. The script recorded its own sha256
(`2c66e661…`) in the log's META line (PID 48468, solver built 08:21:48Z).

Imported scripts, unchanged: `diag1_eval_paths.py` `bfb3ca5e…d13bd9f1`, `ablation.py`
`1545b53b…eff328`, `rowB.py` `195a89b5…7f4082`.

## 2. What changed in `gray_stimulus.py` (v3.1 `939ee537…` -> v4 `2c66e661…`)

- **New `code_gate()`** (brief §6 v4). It takes the source of `per_item_eval_transformed` and of
  `D.per_item_eval` with `inspect.getsourcelines` and computes a `difflib` unified diff, both over
  the whole function and over the body. The gate passes iff (1) the copy's executable body equals
  the original body with exactly the two declared substitutions applied, byte for byte, and
  exactly 2 body lines differ, and (2) `inspect.signature` differs only by the function name and
  the inserted `transform` parameter. The body is the statements after the docstring, located
  with `ast`. The declared substitutions sit at original file lines 188 (`for _, data` ->
  `for _i, data`) and 191 (`add_input(data["lum"])` -> `add_input(transform(data["lum"], _i))`).
  It runs first in `--task codegate` (new, CPU only), `--task control` and `--task main`, before
  the solver is built. On failure it stops.
- `copy_fidelity_control` no longer gates on the 10-pair floor. It records all B pairs and A vs
  each B_k, per item and on the 16-item mean, plus bitwise flags and the raw per-item vectors.
  It stops only on the documented ceilings: per-item |A−B_k| > 0.00146484375, or
  |mean(A) − mean(B_k)| > 1e-4, for any k. At iteration 0 these are the same ceilings, with
  bitwise equality recorded but not required. P0 is unchanged.
- `--task repeat` gates per cell on |Δ loss_16| ≤ 1e-4. It records the per-item deltas and the
  checkpoint's in-process spread next to the gate, without gating on them. The 3×-floor gate was
  removed.
- STATUS, brief and launch strings now say v4 / f915d59 / 08:14:48Z. The docstring lists the
  v4 changes.
- **Unchanged:** the conditions, the transforms, `per_item_eval_transformed`, the evaluator
  reuse, the sweep, the csv format, and the readings logic (§7 v3 = v4).
- **Exercised before launch (CPU, scratchpad, nothing written here):**
  - The code gate ran as `--task codegate` on the real copy and returned PASS.
  - It also ran on four mutants (`value=0.4` in the body; default `t_pre=0.3`; one extra body
    line; the rename alone without the transform). All four returned FAIL.
  - `task_repeat` ran on a synthetic 48-cell csv with the solver and sweep monkeypatched. A cell
    with a 2e-4 mean shift failed, a 5e-5 shift passed, and the gate reported 47/48.
  - `task_readings` ran on the same synthetic csv without error.

## 3. Code gate (brief §6 v4): **PASS**

Body diff, verbatim from the log:
```
--- diag1_eval_paths.py:per_item_eval body (lines 180-201)
+++ gray_stimulus.py:per_item_eval_transformed body (lines 218-239)
@@ -6,10 +6,10 @@
     losses = {t: [] for t in task.dataset.tasks}
     with torch.no_grad():
         with task.dataset.augmentation(False):
-            for _, data in enumerate(dataloader):
+            for _i, data in enumerate(dataloader):
                 n_samples, n_frames, _, _ = data["lum"].shape
                 solver.network.stimulus.zero(n_samples, n_frames)
-                solver.network.stimulus.add_input(data["lum"])
+                solver.network.stimulus.add_input(transform(data["lum"], _i))
                 activity = solver.network(solver.network.stimulus(), task.dataset.dt,
                                           state=initial_state)
                 for t in task.dataset.tasks:
```
The whole-function diff (in the log) also shows the def line, `per_item_eval(solver, t_pre=0.25)`
-> `per_item_eval_transformed(solver, transform, t_pre=0.25)`, and the two different docstrings
(3 lines each). Signature check: True. Body lines: 22 vs 22, 2 differing; both declared original
lines matched their declared text.

**Interpretation (stated as a deviation):** the brief says "the unified diff of the two function
bodies" and "only in the declared lines". The def line and the docstring cannot be identical in a
renamed copy that takes a `transform` argument. The executor therefore gated the executable body
byte for byte and the signature structurally. The docstrings are shown in the diff and are not
gated.

## 4. Copy/original numbers (recorded; ceilings gating), run 000

| checkpoint | iter | B pairs: max per-item / max on mean | A vs B_1..B_5 max per-item | mean(A) − mean(B_k), k=1..5 | bitwise A==B_k | ceilings |
|---|---|---|---|---|---|---|
| `chkpt_00000` | 0 | `0.0` / `0.0` (all 10 pairs bitwise) | `0.0` ×5 | `0.0` ×5 | all True | held |
| `chkpt_00071` | 250008 | `0.000732421875` (B1-B5) / **`0.000110626220703125`** (B1-B4) | `0.00048828125` / `0.00048828125` / `0.000244140625` / `0.000244140625` / `0.00048828125` | **`-0.0001201629638671875`** / `-1.049041748046875e-05` / `-1.9550323486328125e-05` / `-9.5367431640625e-06` / `-3.1948089599609375e-05` | all False | **per-item held; mean BREACHED (A−B_1)** |

At `chkpt_00071`:
- The five original means are `1148.8075399398804 / 1148.807430267334 / 1148.80743932724 /
  1148.8074293136597 / 1148.807451725006`, all 5 distinct. The copy mean is
  `1148.8074197769165`.
- The original-vs-original mean differences per pair are B1-B2 `0.00010967254638671875`,
  B1-B3 `0.00010061264038085938`, B1-B4 `0.000110626220703125`, B1-B5 `8.821487426757812e-05`,
  B2-B3 `9.059906005859375e-06`, B2-B4 `9.5367431640625e-07`, B2-B5 `2.1457672119140625e-05`,
  B3-B4 `1.0013580322265625e-05`, B3-B5 `1.239776611328125e-05`, B4-B5 `2.2411346435546875e-05`.
- The original-vs-original per-item max per pair is `0.00048828125` for 7 pairs,
  `0.000732421875` for B1-B5, `0.0003662109375` for B2-B5, and `0.000244140625` for B3-B4.
- The largest per-item value is `4764.62158203125`, in [4096, 8192), where the float32 ulp is
  4.8828125e-4.

Measured facts about the breach, stated without a verdict:
- The breach is on the mean, against one original call (B_1). A against the other four originals
  lies within 3.2e-05.
- **3 of the 10 original-vs-original pairs also exceed 1e-4 on the mean** (all involve B_1). The
  largest is `0.000110626220703125`. In this process the original evaluator's own in-process spread
  on the mean exceeds the ceiling the copy is held to.
- mean(A) lies `9.5e-06` below the lowest of the five original means, so it is outside their
  range.
- **Recorded for reviewers, not applied.** The brief's text is "|mean(A) − mean(B)| > 1e-4". The
  per-item clause is written with B_k. The executor applied the mean clause to each B_k, per the
  parallel with the per-item clause and the v4 header's "max |mean(A) − mean(B_k)|". Against the
  average of the five original means (`1148.807458114624`), mean(A) differs by
  `-3.8337707565005985e-05`. The script does not implement that reading, and it was not used to
  continue.
- For scale: C3 Part B (`results/diagnostics/c3/README.md`) measured the within-process E2
  (`D.per_item_eval`) 16-item-mean spread at 250008 as `8.106231689453125e-05` (run 003) and
  `0.0001087188720703125` (run 903).

## 5. P0 reproduction (brief §6): **PASS** at both checkpoints

| checkpoint | stored `val_loss` | copy mean | mean − stored | hook value | mean − hook |
|---|---|---|---|---|---|
| `chkpt_00000` | `1212.5555891990662` | `1212.5555891990662` | `0.0` | `1212.5555891990662` | `0.0` |
| `chkpt_00071` | `1148.8074851036072` | `1148.8074197769165` | `-6.532669067382812e-05` | `1148.8074426651` | `-2.288818359375e-05` |

No NaN or inf appeared: all per-item vectors of A and B_1..B_5 are finite (checked from the log).

## 6. Not computed
These were not computed because the run stopped before them: the constant-output null, the 48
cells, the fresh-process repeat and readings (i)/(ii)/(iii).

## 7. Run-dir integrity (brief §9.2)
All **594** files under `connectome-seed-data/results/flow/9991/{000,900,001,002,003,004}` were
listed with `find … -type f -printf "%p %s %T@\n" | sort`, files only. The before listing was taken
at 08:17:22Z, before any edit. The after listing was taken at 08:22:24Z. The `diff` is **empty
(0 bytes)**, and both listings hash to
`64d84e68e0bcd4bbeca6ac8664069e367094a267a184af695cc41863d83106f7`, the same hash as the v2 and
v3.1 runs. `find connectome-seed-data -newermt "2026-09-17 08:17 UTC" -type f` returns nothing.
The listings are in the executor's scratchpad (`…/03852100-…/scratchpad/gray_v4/v4_{before,after}.txt`,
`v4_listing.diff`). The scratch datamate root is `…/scratchpad/gray_v4/netdir_v4_main`.

## 8. Interpreter, command, timings, GPU
```
PY=".../63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/.venv/Scripts/python.exe"
cd C:/Users/mikha/Documents/dpc-research/connectome-seed
FLYVIS_ROOT_DIR=C:/Users/mikha/Documents/dpc-research/connectome-seed-data \
"$PY" -u results/diagnostics/gray/gray_stimulus.py --task main --out-dir results/diagnostics/gray \
      --netdir-root ".../03852100-01fd-45ef-82c3-e22ac607b0f7/scratchpad/gray_v4/netdir_v4_main"
```
Environment: Python 3.10, torch 2.9.1+cu128, flyvis 1.2.0, `cuda`, NVIDIA RTX PRO 4500 Blackwell.
Wall time was **35 s**, from 08:21:16Z to 08:21:51Z, exit code 3. About 32 s was the solver build;
the rest was 2 checkpoints × (1 copy + 5 original + 1 hook) evaluations.

GPU: before the run, `nvidia-smi` listed no python process; the only python processes on the machine
were the two dpc-messenger `run_service.py`, and no training wave was running. After the run it also
listed no python process (3046 MiB used by desktop apps, 0 % utilisation).

## 9. Deviations
1. The code gate covers the executable body and the signature. The docstring and the def-line
   text are not gated (§3).
2. At iteration 0 bitwise equality was recorded, not required, and the same ceilings were applied
   (C3 Part B: single `D.per_item_eval` calls at iteration 0 occasionally one float64 step of the
   mean off). In this run iteration 0 was bitwise anyway: A == all B_k, and all B pairs were equal.
3. The code-gate diff is in the log and this README, not in `gray_controls.json`. That file is
   written only after the sweep, and the run stopped before it.
4. The mean ceiling was applied per B_k. The alternative reading against the average of the B
   means is recorded in §4, not applied.
5. `--task codegate` was added, CPU only, and writes nothing.

## 10. What this cannot show
Nothing was measured about gray, zero or shuffled input. The only supported statements concern
the instrument:
- The copy's code differs from the original only in the declared lines.
- At iteration 0 the copy is bitwise faithful.
- At iteration 250,008 the copy's worst 16-item-mean deviation from a single original call
  (1.20e-04) exceeds the 1e-4 ceiling. In the same process, the original also deviates from
  itself by up to 1.11e-04.
- P0 holds.
- The run dirs were not modified.

Whether the mean ceiling, or the ≤ 1e-4 single-call fresh-process gate built on the same
quantity, needs restating is for Mike and the reviewers, not the executor.
