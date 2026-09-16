# Gray-stimulus control, v3.1: STOPPED AT THE STEP-1 GATE AGAIN

**Status: PREVIEW DIAGNOSTIC -- NOT A TEST.** Protocol:
`docs/briefs/2026-09-16-step1-gray-stimulus.md` **v3.1** (commit `54823c4`). Launched on Mike's
explicit word in the DPC Research chat, 2026-09-16 20:14:03Z: «@CC_windows запускай шаг 1»
(reviewers Ark 20:09Z/20:11Z and Zcode 20:14Z raised no objections to v3/v3.1). **Run by:** CC's
subagent (Opus), 2026-09-16 20:15-20:25Z. The v2 run's record is kept unchanged as
`README_v2_gate_stop.md`, renamed within this directory.

> **The 48-cell sweep was NOT run.** At `chkpt_00071` of run 000 the v3.1 copy-fidelity control
> fails: the copy with the identity transform (A) deviates from one of five calls of the original
> `D.per_item_eval` (B_1) by a max per-item **0.000732421875**. The **floor**, the max per-item
> deviation over all 10 pairs among B_1..B_5, is **0.00048828125**. The brief's rule
> (§6, v3.1) is pass iff max_k max per-item |A−B_k| ≤ floor, so this is a **FAIL**.
> `chkpt_00000` passes bitwise. P0 passes at both checkpoints. The executor's instruction was:
> if any gate fails, stop and report. The run stopped there: no constant-output null, no main
> sweep, no fresh-process repeat, no readings. After the stop, no GPU work of any kind was run
> (no floor re-measurement, no diagnosis run).

Nothing was committed or pushed. No file outside this directory and the executor's scratchpad
was written. No training was run. No ablation hook was registered: `net._state_hooks == ()` was
asserted before and after the copy, after each of the five original calls, and after `hook_eval`.
Nothing is rounded: the numbers below are the `repr` strings the script printed.

---

## 1. Files in this directory

| file | what | sha256 |
|---|---|---|
| `gray_stimulus.py` | the driver, updated to v3.1 (§2). **Uncommitted modification** of the committed file | `939ee5371529f684551e47be4591612d07bc2a62d8bc06d4555a0b10c6404d73` |
| `gray_control_v31_gate_stop.log` | full stdout+stderr of the one `--task control` invocation, verbatim | `bca46bae35420ab4e39b67dd8773b1e8349e1fbf92d2f43b9540483c02bd0de8` |
| `README_v2_gate_stop.md` | the v2 run's README, renamed, content unchanged | `5a65ed078b2205b826cf48c0515d86dc093e3a3f49c89ff2d52b7781a3d6b921` |
| `README.md` | this file | n/a |

The brief's §5 outputs (`gray_losses.csv`, `gray_controls.json`, `gray_repeat_controls.json`, and
the readings json) **do not exist**, because `--task control` writes nothing and the run stopped
after it.

Unchanged, imported scripts (hashes match `README_v2_gate_stop.md` §2 and the night-3 ablation
README): `diag1_eval_paths.py` `bfb3ca5e…d13bd9f1`, `ablation.py` `1545b53b…eff328`, `rowB.py`
(night2 = night3) `195a89b5…7f4082`, `ablation_night3.py` `c20013b4…fac156a`.

## 2. What changed in `gray_stimulus.py` (v2 `94840b02…` -> v3.1 `939ee537…`)

- New `copy_fidelity_control(solver, run, ci)`, used by `--task control` and `--task main`. It
  computes A (the copy, identity transform), then B_1..B_5 (five calls of the original
  `D.per_item_eval` on the same loaded checkpoint), then `hook_eval`. The floor is max per-item
  |B_j−B_k| over all 10 pairs; the script also records the floor on the 16-item mean. A is
  compared with each B_k and the worst pair is reported. Pass iff worst ≤ floor. At iteration 0
  the floor must be 0.0 and A must equal every B_k bitwise. P0 is unchanged (≤ 1e-4 against the
  stored value and the hook).
- `--task main` stops with nothing written if its own control fails.
- `--task repeat`: the gate is applied per checkpoint. It passes iff max |Δ loss_16| ≤ 3 × the
  in-process floor on the 16-item mean from `gray_controls.json`; ≤ 1e-4 is reported separately,
  and results are recorded per cell and per checkpoint.
- `--task readings`: reading (ii) is `excess_cond = L_trained,cond − L_untrained_gray` for gray
  and zero, classed as ≥ 10·gain_s explodes / ≤ 0.1·gain_s returns / else between. It is
  computed for all six seeds; seed 2 is the pre-registered one. The previous executor's
  provisional 3062.6 threshold is **removed**. Reading (iii) is void when
  |L_trained_real − L_untrained_gray| ≤ 0.2·gain_s; otherwise the exclusive branches apply.
- STATUS/brief/launch strings now say v3.1 and 20:14:03Z. The module docstring lists these
  changes.
- **Unchanged:** the four conditions, the transform line, `per_item_eval_transformed`, the
  evaluator reuse, the sweep, the csv format, and `--task floor` (unused this run).
- Pre-run check of the readings logic only: `--task readings` was run on a hand-made synthetic
  csv in the scratchpad. It needs no GPU; its output stayed in the scratchpad, and its branches
  matched hand calculation. The repeat-gate code has **not** been exercised: it never ran.

## 3. Controls: the numbers (`--task control`, PID 29812, solver built 2026-09-16T20:19:51Z)

### 3a. Copy fidelity (brief §6 v3.1), run 000

| checkpoint | iter | floor: max per-item over 10 pairs | floor on 16-item mean | A vs B_1..B_5 max per-item | worst | pass |
|---|---|---|---|---|---|---|
| `chkpt_00000` | 0 | `0.0` | `0.0` | `0.0` ×5, all bitwise equal | `0.0` | **yes** (bitwise) |
| `chkpt_00071` | 250008 | `0.00048828125` | `8.869171142578125e-05` | `0.000732421875` / `0.000244140625` / `0.00048828125` / `0.00048828125` / `0.00048828125` | **A−B_1 `0.000732421875`** | **NO** |

At `chkpt_00071`:
- Per-pair floor, max per-item: `0.00048828125` for 8 pairs, `0.000244140625` for B1-B5 and
  B2-B5.
- The five original means: `1148.8074097633362 / 1148.8074278831482 / 1148.8074984550476 /
  1148.8074779510498 / 1148.8074097633362`. That is 4 distinct values; B_1 and B_5 are equal.
- Copy mean: `1148.807454586029`.
- mean(A) − mean(B_k): `4.482269287109375e-05 / 2.6702880859375e-05 / -4.38690185546875e-05 /
  -2.3365020751953125e-05 / 4.482269287109375e-05`.

Measured facts, stated without a verdict (the brief's gate is per-item, and it fails):
- The copy's mean lies inside the range of the five original means, and its largest |mean
  difference| (4.48e-05) is below the floor on the 16-item mean (8.87e-05).
- Every per-item difference printed here is an integer multiple of `0.000244140625`. The failing
  value is 3 of those steps, against a floor of 2.
- In the v2 run (`README_v2_gate_stop.md` §3b, a different process), the original-vs-original
  maximum over five calls was `0.0009765625`, 4 steps.
- The v2 figures and this run's figures are two measurements of the same quantity in two
  processes, and they differ by a factor of 2.

### 3b. P0 reproduction (brief §6)

| checkpoint | stored `val_loss` | copy mean | mean − stored | hook value | mean − hook | ≤ 1e-4 |
|---|---|---|---|---|---|---|
| `chkpt_00000` | `1212.5555891990662` | `1212.5555891990662` | `0.0` | `1212.5555891990662` | `0.0` | **yes** |
| `chkpt_00071` | `1148.8074851036072` | `1148.807454586029` | `-3.0517578125e-05` | `1148.8074479103088` | `6.67572021484375e-06` | **yes** |

### 3c. Not computed (the run stopped before these)
The constant-output null, the 48 cells, the fresh-process gate, and readings (i)/(ii)/(iii).

## 4. The four input conditions, as implemented (unchanged from v2; never applied)

| condition | brief | transform applied to `data["lum"]` at the argument of `diag1_eval_paths.py:191` |
|---|---|---|
| `real` | (c) | `lum`, the identity |
| `gray` | (a) | `torch.full_like(lum, 0.5)` |
| `zero` | (b) | `torch.zeros_like(lum)` |
| `shuffled` | (d) | `lum[:, perm]`: the frame axis is permuted; **the target is not permuted** |

Permutation: `SHUFFLE_SEED = 20260916`,
`perm = numpy.random.default_rng([SHUFFLE_SEED, item_index]).permutation(n_frames)`, where
`item_index` is the dataloader index 0..15. The loop-variable rename `_` -> `_i` is allowed by
brief §9.10.

## 5. Run-dir integrity (brief §9.2)

All **594** files under `connectome-seed-data/results/flow/9991/{000,900,001,002,003,004}` were
listed (`find … -printf "%p %s %T@\n" | sort`). The before listing was taken at
2026-09-16T20:15:46Z, before any edit or run; the after listing was taken after the control
invocation. `diff` is **empty (0 bytes): NO CHANGE to the run dirs.** Both listings hash to
`64d84e68e0bcd4bbeca6ac8664069e367094a267a184af695cc41863d83106f7`, the same hash as the v2 run's
listings. `find connectome-seed-data -newermt "2026-09-16 20:15 UTC"` returns nothing. The
listings are in the executor's scratchpad (`…/03852100-…/scratchpad/gray/v31_{before,after}.txt`,
`v31_listing.diff`). The scratch datamate root is `…/scratchpad/gray/netdir_v31_control`.

## 6. Interpreter, command, timings, GPU

```
PY=".../63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/.venv/Scripts/python.exe"
cd C:/Users/mikha/Documents/dpc-research/connectome-seed
"$PY" results/diagnostics/gray/gray_stimulus.py --task control --out-dir results/diagnostics/gray \
      --netdir-root ".../03852100-01fd-45ef-82c3-e22ac607b0f7/scratchpad/gray/netdir_v31_control"
```
`FLYVIS_ROOT_DIR=C:/Users/mikha/Documents/dpc-research/connectome-seed-data` and
`CUBLAS_WORKSPACE_CONFIG` are set inside the script. Environment: Python 3.10.20, torch
2.9.1+cu128, flyvis 1.2.0, device `cuda`, GPU `NVIDIA RTX PRO 4500 Blackwell`, `dt` 0.02, batch
size 1, 16 held-out items.

Wall time: started 20:19:18Z, log last written 20:19:53Z, so **~35 s** (about 33 s solver build,
the rest 2 checkpoints × 7 evaluations).

GPU: before the run, `nvidia-smi` listed no python process. After the run it also listed none.
The unnamed entries are `dwm.exe` (2524) and `Taskmgr.exe` (8052). The `python.exe` PIDs
7492/43004 are the dpc-messenger `run_service.py` and are not on the compute list. Mike's
`llama-server.exe` (PID 45360, ~28.7 GiB) was not touched.

## 7. What this cannot show

Nothing was measured about gray, zero or shuffled input. The only supported statements concern
the instrument:
- The copy is bitwise faithful at iteration 0.
- At iteration 250,008 its worst per-item deviation from five original calls exceeds that
  process's 10-pair floor by one quantisation step.
- The evaluator reproduces both stored values to ≤ 3.06e-05.
- The run dirs were not modified.

Whether the copy-fidelity rule needs another restatement is for Mike and the reviewers, not the
executor. Possible directions include a floor taken from more calls, the floor on the 16-item
mean, or the maximum over copy-vs-copy as well.
