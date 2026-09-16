# Gray-stimulus control — STOPPED AT THE STEP-1 GATE

**Status: PREVIEW DIAGNOSTIC — NOT A TEST.** Protocol:
`docs/briefs/2026-09-16-step1-gray-stimulus.md` (v2, 2026-09-16, after review by Ark and Zcode),
written and saved before this script was run. Launched on Mike's explicit word in the DPC
Research chat, 2026-09-16 19:50:18Z. **Run by:** CC's subagent (Opus), 2026-09-16/17.

> **The 48-cell sweep was NOT run.** The brief's §6 **copy-fidelity** control — *"the new copy
> with the identity transform must return a per-item vector **exactly equal** to
> `D.per_item_eval(solver)`"* — **passes exactly at `chkpt_00000` and does not pass at
> `chkpt_00071`**, and the executor's instruction for step 1 was: if either step-1 control
> fails, stop and report. It was stopped. §3 below shows *why* it does not pass at
> `chkpt_00071`, measured rather than argued: at that checkpoint `D.per_item_eval` **does not
> reproduce itself** in the same process either. Five consecutive calls of the **original**
> function on the **same** loaded checkpoint give **five distinct** 16-item means, spread
> 8.58e-05, per-item spread 9.77e-04 — the same spread the copy shows against it. The control as
> written is therefore unsatisfiable at `chkpt_00071` by a property of the evaluator, not of the
> copy. Whether the control should be restated against its own measured floor (as
> `rowB.py` already does with `PURITY_TOL` and `nohook_vs_nohook_FLOOR`) is a brief amendment for
> Mike and the reviewers, **not** a decision the executor took.

Nothing was committed, nothing was pushed, no existing file was edited, nothing outside this
directory and the executor's scratchpad was written, no training was run, no ablation hook was
registered (`net._state_hooks == ()` asserted before and after every evaluation), no number here
is rounded (`repr(float(x))` throughout the script; the tables below quote those reprs).

---

## 1. What exists in this directory

| file | what |
|---|---|
| `gray_stimulus.py` | the driver. Imports the evaluator from `../../night2/diagnostics/diag1_eval_paths.py` and the seven `eval_rung` invariants from `../../night2/diagnostics/rowB/rowB.py`; nothing of the evaluation path is re-implemented. Five sub-commands: `control`, `floor`, `main`, `repeat`, `readings`. **`main`, `repeat` and `readings` have never been run.** |
| `README.md` | this file |

`gray_losses.csv`, `gray_controls.json`, `gray_losses_repeat.csv` and `gray_readings.json` — the
brief's §5 outputs — **do not exist**, because the sweep did not run.

## 2. sha256 of every script involved

| file | sha256 |
|---|---|
| `results/diagnostics/gray/gray_stimulus.py` | `94840b02d914326b76d25387fb30161e49543195cd26fd08ad38327e7e1c26b7` |
| `results/night2/diagnostics/diag1_eval_paths.py` (unchanged, imported) | `bfb3ca5eb1d20b3084d09cac57e333efae2a34b7ec4b503d60602275d13bd9f1` |
| `results/night2/diagnostics/ablation/ablation.py` (unchanged, imported) | `1545b53b14b64758f0cc5630a8be8a635ff1e3cf0a1083aec375d251b0eff328` |
| `results/night2/diagnostics/rowB/rowB.py` (unchanged, imported) | `195a89b555bedf3a0ff00a4c4e0542eafa6370243fbf9ed954f5fe8fbf7f4082` |
| `results/night3/diagnostics/rowB/rowB.py` (**byte-identical** to the night-2 copy, `diff` empty) | `195a89b555bedf3a0ff00a4c4e0542eafa6370243fbf9ed954f5fe8fbf7f4082` |
| `results/night3/diagnostics/ablation/ablation_night3.py` (not imported; hashed for provenance) | `c20013b4ab0826af6d89cccd653d1cfa601915017fbbd04156fe1628ffac156a` |

The first four match the table in `../../night3/diagnostics/ablation/README.md` §1 exactly, so
the evaluator used here is the same bytes that produced the night-2 and night-3 numbers. The
brief §2 cites `results/night3/.../rowB.py`; that file and the night-2 one are byte-identical
(`diff` empty, same sha256), so `gray_stimulus.py` imports the night-2 path — the path
`ablation_night3.py:39` uses — and records both hashes.

**All numbers below were produced by `gray_stimulus.py` at the sha256 above.** An earlier
invocation of `--task control` at an earlier hash (before `--task floor` was added) produced the
same verdict and the same pass/fail pattern; `--task control` was re-run at the final hash so
that everything recorded here comes from one file.

## 3. Controls — the numbers

### 3a. Copy fidelity (brief §6) and P0 reproduction (brief §6), run 000

`--task control`, one process, PID 27740, 2026-09-16T20:03:08Z. A = the copy with the identity
transform, B = `D.per_item_eval(solver)`, C = `D.per_item_eval(solver)` a second time (the
evaluator's own repeat floor, measured beside the control rather than assumed).

| checkpoint | iter | A == B bitwise | max abs per-item A−B | max abs per-item B−C (floor) | mean(A) − mean(B) |
|---|---|---|---|---|---|
| `chkpt_00000` | 0 | **true** | `0.0` | `0.0` | `0.0` |
| `chkpt_00071` | 250008 | **false** | `0.000244140625` | `0.00018310546875` | `-1.811981201171875e-05` |

| checkpoint | stored `val_loss` | copy per-item mean | mean − stored | rung-hook value | mean − hook | P0 ≤ 1e-4 |
|---|---|---|---|---|---|---|
| `chkpt_00000` | `1212.5555891990662` | `1212.5555891990662` | `0.0` | `1212.5555891990662` | `0.0` | **yes** |
| `chkpt_00071` | `1148.8074851036072` | `1148.8074460029602` | `-3.910064697265625e-05` | `1148.807451248169` | `-5.245208740234375e-06` | **yes** |

**P0 passes at both checkpoints**, well inside the brief's 1e-4 and consistent with the prior
observed values quoted in the brief (−1.29e-05, −5.91e-05). **Copy fidelity passes at
`chkpt_00000` and fails at `chkpt_00071`.**

### 3b. Why it fails — the evaluator's own repeat floor (`--task floor`)

Added after the gate did not pass, to separate "the copy is wrong" from "the evaluator is not
bitwise reproducible". Five repeats of the **original** `D.per_item_eval` and five of the copy,
**interleaved**, on the same loaded checkpoint, one process, PID 42368, 2026-09-16T20:01:46Z.

| checkpoint | orig-vs-orig max abs per-item | copy-vs-copy | copy-vs-orig | distinct orig means (of 5) | distinct copy means (of 5) | bitwise-equal copy/orig pairs (of 25) |
|---|---|---|---|---|---|---|
| `chkpt_00000` | `0.0` | `0.0` | `0.0` | 1 | 1 | **25** |
| `chkpt_00071` | `0.0009765625` | `0.000732421875` | `0.0009765625` | **5** | **5** | **0** |

At `chkpt_00071` the five **original** means are
`1148.8074479103088 / 1148.8074703216553 / 1148.8074045181274 / 1148.8073935508728 /
1148.8073844909668` — spread `8.58306884765625e-05`; the copy's own five means have spread
`8.487701416015625e-05`; mean-of-means copy − original = `-6.580352874152595e-06`, i.e. **13×
smaller than the original's own spread**. The copy-vs-original maximum per-item difference is
**exactly** the original-vs-original maximum, `0.0009765625`.

At `chkpt_00000` everything is bitwise identical: 25 of 25 cross pairs equal, one distinct mean.

This is not new to this directory. `../../night3/diagnostics/rowB/rowB_controls.json` already
records `per_item_max_abs_diff_nohook_vs_nohook_FLOOR` = `0.0` at iteration 0 and
`nohook_vs_nohook_abs_diff_of_the_16_item_loss` = `3.2901763916015625e-05` (seed 3) /
`1.430511474609375e-05` (seed 4) at iteration 250,008 — the same effect, measured there and
tolerated there with a 1e-4 tolerance. The source is the night runs' own configuration:
`build_solver` sets `cudnn.deterministic = False` and `cudnn.benchmark = False`
(`diag1_eval_paths.py:90-93`), matching `night/run_individual.py:211-218` under `--no-determinism`.
Changing that would change the evaluator, which the brief forbids.

### 3c. Constant-output null (brief §6) — NOT computed

It is step 2 of the execution order, after the step-1 gate. The gate stopped first.
`constant_output_null()` is implemented in `gray_stimulus.py` and has never been executed.

## 4. The four input conditions, as implemented

Substitution site: the argument of `diag1_eval_paths.py:191`
`solver.network.stimulus.add_input(data["lum"])`, inside a line-for-line copy of
`per_item_eval` (`diag1_eval_paths.py:176-201`). `t_pre=0.25`, `value=0.5` (:183-184),
`augmentation(False)` (:187), the decoder call (:196) and the loss call (:198) are byte-identical
in the copy.

| condition | brief | transform applied to `data["lum"]` |
|---|---|---|
| `real` | (c) | `lum` — the identity |
| `gray` | (a) | `torch.full_like(lum, 0.5)` |
| `zero` | (b) | `torch.zeros_like(lum)` |
| `shuffled` | (d) | `lum[:, perm]` — frame axis (dim 1) permuted; the **target is not permuted** |

**Permutation seed and derivation, fixed before any run:** `SHUFFLE_SEED = 20260916`;
`perm = numpy.random.default_rng([SHUFFLE_SEED, item_index]).permutation(n_frames)`, where
`item_index` is the dataloader enumeration index 0..15 and `n_frames` is that item's own frame
count. Derived from `(SHUFFLE_SEED, item_index)` alone — not from a global RNG stream — so the
same permutation is drawn in every process, for every run and every checkpoint. **No permutation
was ever applied: the sweep did not run.**

**Deviation from the brief, recorded:** the brief §3 says the copy changes *"only the argument of
line 191"*. The copy also renames the throw-away loop variable on `:188` from `_` to `_i`, which
is what indexes the per-item permutation of condition (d). That is the only other textual
difference; it is stated in the script's module docstring and in `per_item_eval_transformed`'s
own docstring.

## 5. Run-dir integrity (brief §10.2)

All **594** files under `connectome-seed-data/results/flow/9991/{000,900,001,002,003,004}` listed
with size and mtime before anything was run and again after the last invocation:

```bash
cd /c/Users/mikha/Documents/dpc-research/connectome-seed-data/results/flow/9991 \
  && find 000 900 001 002 003 004 -type f -printf "%p %s %T@\n" | sort > before.txt   # then after.txt
diff before.txt after.txt
```

`diff` **empty — NO CHANGE to run dirs.** Both listings hash to
`64d84e68e0bcd4bbeca6ac8664069e367094a267a184af695cc41863d83106f7`. Nothing under
`connectome-seed-data` was written.

Side effects outside this directory: importing `diag1_eval_paths`, `ablation` and `rowB`
refreshed the three existing `__pycache__/*.pyc` files under `results/night2/diagnostics/`
(gitignored, `.gitignore:8`); **no `.py` file was touched**, and `git status` shows no
modification under `results/night2/` or `results/night3/`. The scratch datamate roots live under
the executor's scratchpad (`.../03852100-.../scratchpad/gray/netdir_*`), as `build_solver`'s own
assertion requires (`diag1_eval_paths.py:116`).

## 6. Interpreter, commands, timings

```
PY="C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/.venv/Scripts/python.exe"
OUT="C:/Users/mikha/Documents/dpc-research/connectome-seed/results/diagnostics/gray"
ND="C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/03852100-01fd-45ef-82c3-e22ac607b0f7/scratchpad/gray"

cd "C:/Users/mikha/Documents/dpc-research/connectome-seed"
"$PY" "$OUT/gray_stimulus.py" --task floor   --out-dir "$OUT" --netdir-root "$ND/netdir_floor"
"$PY" "$OUT/gray_stimulus.py" --task control --out-dir "$OUT" --netdir-root "$ND/netdir_control2"
```

Working directory `connectome-seed`; `FLYVIS_ROOT_DIR` and `CUBLAS_WORKSPACE_CONFIG` are set
inside `gray_stimulus.py:44-48` the same way as `ablation_night3.py:30-33`, so nothing has to be
exported first.

Python 3.10.20, torch 2.9.1+cu128, flyvis 1.2.0, device `cuda`, GPU
`NVIDIA RTX PRO 4500 Blackwell`, `dt` 0.02, batch size 1, 16 held-out items.

| invocation | wall | what it did |
|---|---|---|
| `--task control` (first, earlier hash) | 41.3 s | 2 checkpoints × (copy + 2 originals + 1 rung hook) = 8 evaluations, + solver build |
| `--task floor` | 36.4 s | 2 checkpoints × 10 evaluations = 20 evaluations, + solver build |
| `--task control` (final hash) | 34.8 s | 8 evaluations, + solver build |

36 evaluations in total, none of them part of the 48-cell sweep. Solver build dominates: the
evaluations themselves ran in roughly 0.2–0.5 s each, consistent with the brief §8 reference
points. **No other python process was on the GPU** at any point (checked with `nvidia-smi` before
the first invocation and after the last); a non-python `llama-server.exe` held ~28.9 GiB of the
card's 32.6 GiB throughout, which is recorded because it is a plausible contributor to the
kernel-selection nondeterminism of §3b but was **not** isolated as its cause.

## 7. What a v3 of the brief has to settle before the sweep is worth running

1. **The copy-fidelity control's tolerance.** As written ("exactly equal") it is satisfiable only
   at `chkpt_00000`. The measured alternative is already in this repo's vocabulary: require
   `max|A − B|` to be **at or below the evaluator's own repeat floor `max|B − C|`, measured in
   the same process on the same checkpoint** — which is what §3b reports, and which the copy
   passes (`0.0009765625` against `0.0009765625`; mean offset 13× below the original's own
   spread).
2. **The fresh-process gate of §6** (`max |delta| ≤ 1e-4` over the 48 cells) is *not* in question:
   the in-process spread measured here is 8.6e-05 on the 16-item mean, inside that gate but not
   far inside it, so the gate will be close-run at `chkpt_00071` and comfortable at `chkpt_00000`.
   This is a measurement, not a prediction of the outcome.
3. **Reading (ii) has no numeric threshold.** §7(ii) branches on "explosion on both (a) and (b)"
   vs "neither (a) nor (b) explode" but pre-registers no number for "explodes"; it pre-registers
   only the two reference magnitudes +21,157.5 and +30,626. `gray_stimulus.py`'s `--task readings`
   currently operationalises "explodes" as *excess over the seed-2 trained-real baseline ≥ 3062.6*
   (one tenth of the R1–R8 clamp excess) and labels that, in the output json, as the **executor's**
   operationalisation and not the brief's, recording the raw excesses so any other threshold can
   be applied. That choice should be made by the brief, not by the script.
4. **Reading (iii)'s three branches are not mutually exclusive.** "within `0.1·gain_s` of
   `L_trained_real(s)`" and "within `0.1·gain_s` of `L_untrained_gray(s)`" can both hold when the
   two references are within `0.2·gain_s` of each other. The script records that case explicitly
   rather than silently picking the first branch.
5. **An output file the brief does not name.** `--task repeat` writes the fresh-process comparison
   (max |delta| per cell) to `gray_repeat_controls.json`, because `gray_controls.json` is already
   closed by the first process. Named here so it is not a surprise.

## 8. What this cannot show

Nothing was measured about gray, zero or shuffled input. The only statements this directory
supports are about the instrument: the copy of `per_item_eval` is bitwise faithful at iteration 0
and indistinguishable from the original at its own repeat floor at iteration 250,008; the
evaluator reproduces both stored checkpoint values to ≤ 3.91e-05; and the six run directories were
not modified.
