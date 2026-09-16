# Brief — step 1: gray-stimulus control

Path aliases used below:
`FV` = `.../63f3961a-.../scratchpad/flyvis-probe/.venv/Lib/site-packages/flyvis` (flyvis 1.2.0)
`CS` = `C:\Users\mikha\Documents\dpc-research\connectome-seed`
`CSD` = `C:\Users\mikha\Documents\dpc-research\connectome-seed-data`

## 1. What is measured
12 networks = 6 runs `{000, 900, 001, 002, 003, 004}` x 2 checkpoints, x 3 input conditions,
on the same 16 held-out Sintel items, with the ablation scripts' evaluator and **no ablation
hook registered**. 36 evaluations.
- trained checkpoint = `chkpt_00071` (solver iteration 250,008) — `CS/results/night2/diagnostics/ablation/ablation.py:42`.
- iteration-0 checkpoint = **`chkpt_00000`**, checkpoint index 0, solver iteration 0 —
  `CS/results/night3/diagnostics/rowB/rowB.py:56-57` (`NAMED_CHKPTS = {0: 0, 8: 25212, 71: 250008}`)
  and `rowB.py:287-295` (`load_named`, which asserts the mapping at run time).
Conditions: **(a) gray** = every input element 0.5; **(b) zero** = every input element 0.0;
**(c) P0** = unmodified `data["lum"]`.

## 2. Evaluator — reuse, do not re-implement
`CS/results/night2/diagnostics/diag1_eval_paths.py`: `build_solver` (:81), `chkpt_table` (:62),
`load_checkpoint` (:132), `hook_eval` (:151), `per_item_eval` (:176), `val_item_names` (:204).
Seven eval_rung invariants from `CS/results/night3/diagnostics/rowB/rowB.py:161-193`, wrapped as
in `ablation_night3.py:96-102`. The env vars must be set before importing torch/flyvis exactly as
`ablation_night3.py:30-33`.

## 3. Where the substitution happens
One line: `diag1_eval_paths.py:191`
```
solver.network.stimulus.add_input(data["lum"])
```
`data["lum"]` has shape `(n_samples, n_frames, 1, n_input_elements)` (`FV/network/stimulus.py:184`)
and `add_input` writes it into the photoreceptor rows of the buffer (`stimulus.py:206`,
`self.input_index` = R1..R8, `stimulus.py:128-131`).
Because `per_item_eval` hard-codes that expression, the executor writes a **new** script with a
line-for-line copy of `per_item_eval` in which only the argument of line 191 changes
(`lum -> torch.full_like(lum, 0.5)` / `torch.zeros_like(lum)` / `lum`).
**Do not edit `diag1_eval_paths.py`** — its sha256 is recorded inside already-committed outputs.
Everything else in the copy (including `t_pre=0.25`, `value=0.5` at `:183-184`, `augmentation(False)`
at `:187`, the decoder call at `:196`) stays byte-identical.

## 4. What "mid-gray" is, in flyvis units
Input luminance is in [0, 1]: `FV/datasets/sintel_utils.py:57`
`lum = np.float32(Image.open(path).convert("L")) / 255`.
0.5 is flyvis's own resting/background value, in four independent places:
- `FV/network/network.py:548-586` `steady_state(..., value: float = 0.5)`, docstring
  "Compute state after grey-scale stimulus"; `:580-581` `stimulus.zero(...)` then `add_pre_stim(value)`.
- `FV/network/network.py:619-623` fade-in ramps contrast about 0.5: `linspace(0,1)*(frames-0.5)+0.5`.
- `FV/datasets/moving_bar.py:194` `self.bg_intensity = 0.5`.
- `FV/datasets/flashes.py:57` `baseline = 2 * (dynamic_range.sum() / 2,)` -> 0.5 for `[0, 1]`.
Our own evaluator already uses it: `diag1_eval_paths.py:184` `value=0.5`.
**Gray is not "photoreceptors at zero."** Under gray the buffer carries 0.5 into R1-R8 and the
network sits at its own steady state; the ablation hook instead set `state.nodes.activity` to 0.0
(`ablation.py:63-84`). The two interventions are different, and that difference is the whole
content of reading (ii) below. Condition (b) all-zero is a third thing again: full-field black, a
real stimulus, not the resting state.

## 5. Outputs
New directory `CS/results/night4/diagnostics/gray/` (nothing written anywhere else).
- `gray_losses.csv` — first two lines `# PREVIEW DIAGNOSTIC -- NOT A TEST (...)` and
  `# script_sha256=<...>` (convention: `rowB.py:307-310`, `rowB_profiles_*.csv:1`); columns
  `run,label,checkpoint_iter,condition,loss_16` + 16 `loss_item_<short>` columns; every number
  written with `repr(float(x))` — full float, no rounding (`rowB.py:315-319`).
- `gray_controls.json` — `meta` with: `status`, `script_sha256` of the new script **and** of
  `diag1_eval_paths.py`, `ablation.py`, `rowB.py` (pattern: `ablation_night3.py:76-83`),
  `flyvis.__version__`, `torch.__version__`, python, `torch.cuda.get_device_name(0)`, `netdir`,
  `device`, `utc`, `val_items`, checkpoint names, the exact definition of each condition, and the
  seven invariants per evaluation.

## 6. Controls
- **P0 reproduction.** Condition (c) must reproduce each checkpoint's stored `val_loss`
  (`diag1_eval_paths.py:147`) to <= 1e-4, and `per_item_mean - hook_eval()` to <= 1e-4. Prior
  observed values: -1.29e-05 and -5.91e-05 (`night3/.../ablation/README.md:117-120`).
- **Copy fidelity.** On one checkpoint, the new copy with the identity transform must return a
  per-item vector **exactly equal** to `D.per_item_eval(solver)`. If it does not, the copy is wrong
  and nothing else in the run is interpretable.
- **Fresh process.** Repeat all 36 cells in a second process; gate max |delta| <= 1e-4; record the
  actual spread rather than asserting it.
- **Iteration 0, gray vs real.** Expectation, stated in advance: a *difference*, but a small one.
  The stored iteration-0 losses are 1212.5556 / 1212.5556 / 1212.5530 / 1212.5592 / 1212.5497 /
  1212.5379 for seeds 0/0'/1/2/3/4 (`night2` and `night3` `rowB_eval_records.json`), i.e. the six
  untrained networks agree to ~0.02 on real input — consistent with a near-input-independent
  decoder output. If gray and real agree at iteration 0 to within a few units, the "1212 plateau"
  is the constant-output plateau and it is a valid reference for reading (i). If they differ by
  >> 10, the plateau is not input-independent and reading (i) loses its reference — record it,
  do not reinterpret it on the spot.

## 7. Pre-registered readings (verbatim)
(i) gray ~ 1212 for five runs -> "learned = vision" closed from the second side.
(ii) seed 2 under gray: ~ 1212 -> its explosion under R1-R8 clamp-to-0 was an artefact of forcing
photoreceptor activity to zero, not a vision dependence; explosion -> the dependence is real.
Reference for (ii): seed 2's dominant single-type ablation is **R2, delta_16 = +21157.5**
(`night2/.../ablation/ablation_profiles.csv`; also pre-registered at `ablation_night3.py:64-65`).
Trained-checkpoint losses for the five other runs at 250,008: 1148.81, 1160.98, 1144.64, 1155.77,
1156.83; seed 2 is 1147.72.
No threshold is set here for "~". State the numbers; the reading is a comparison to 1212.55, and
the band should be agreed with Ark **before** the run, not after.

## 8. Runtime — ESTIMATE
Measured reference points: night-2 ablation did 276 sixteen-item evaluations in 113.8 s wall,
0.18-0.34 s per evaluation (`night2/.../ablation/README.md:130-132`); night-3 recorded
`one_evaluation_wall_s` 0.492 (seed 3) and 0.179 (seed 4) (`ablation_controls.json`).
36 evaluations + 36 for the repeat + one solver build (~20-40 s, ESTIMATE) -> **~2 minutes total,
ESTIMATE**. No new rendering is needed: the Sintel rendering already exists under
`CSD/renderings/RenderedSintel_0000`.

## 9. Do not
1. Do not train, do not call `solver.checkpoint()` or `solver.test(track_loss=True)` — those are
   the only two calls that write into a network dir (`diag1_eval_paths.py:6-11`).
2. Do not write anything under `CSD/results/flow/9991/**`. List all 594 files with size and mtime
   before and after and `diff` the listings, as `night3/.../ablation/README.md:107-111` does.
3. Do not edit `diag1_eval_paths.py`, `ablation.py`, `rowB.py`, or any file under
   `CS/results/night2/` or `CS/results/night3/`.
4. Do not register an ablation hook. Assert `net._state_hooks == ()` before and after every
   evaluation (`ablation.py:104, 111`).
5. Do not change `t_pre`, `value=0.5`, `dt`, batch size, augmentation, or the val item set.
6. Do not round any number in a csv or json; use `repr(float(x))`.
7. Do not commit, do not push, do not touch the `connectome-seed` working tree.
8. Do not label this a test. Header on every output: `PREVIEW DIAGNOSTIC -- NOT A TEST`.
9. If any of the seven invariants is False, stop and report — do not continue the sweep.
