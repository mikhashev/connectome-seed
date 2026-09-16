# Brief — step 1: gray-stimulus control

**v2, 2026-09-16, after review by Ark and Zcode; v1 was posted at 06:23Z; a v1 sweep was run at
~06:30Z before the review arrived and its output was discarded unread (CC's protocol error,
recorded in chat); nothing from it is used.**

**Launch only on Mike's explicit «запускай» for this step in the DPC Research chat.**

Path aliases used below:
`FV` = `.../63f3961a-.../scratchpad/flyvis-probe/.venv/Lib/site-packages/flyvis` (flyvis 1.2.0)
`CS` = `C:\Users\mikha\Documents\dpc-research\connectome-seed`
`CSD` = `C:\Users\mikha\Documents\dpc-research\connectome-seed-data`

## 1. What is measured
12 networks = 6 runs `{000, 900, 001, 002, 003, 004}` x 2 checkpoints, x 4 input conditions,
on the same 16 held-out Sintel items, with the ablation scripts' evaluator and **no ablation
hook registered**. 48 evaluations, plus the fresh-process repeat (48 more).
- trained checkpoint = `chkpt_00071` (solver iteration 250,008) — `CS/results/night2/diagnostics/ablation/ablation.py:42`.
- iteration-0 checkpoint = **`chkpt_00000`**, checkpoint index 0, solver iteration 0 —
  `CS/results/night3/diagnostics/rowB/rowB.py:56-57` (`NAMED_CHKPTS = {0: 0, 8: 25212, 71: 250008}`)
  and `rowB.py:287-295` (`load_named`, which asserts the mapping at run time).
Conditions: **(a) gray** = every input element 0.5; **(b) zero** = every input element 0.0;
**(c) P0** = unmodified `data["lum"]`; **(d) shuffled frames** = the same item's `data["lum"]`
with the frame axis permuted by a fixed, per-item permutation whose seed is recorded in
`gray_controls.json` — content and per-frame image statistics preserved, temporal structure
destroyed (Zcode's version of Ark's "wrong video" condition; see §3, §7(iii)).

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
line-for-line copy of `per_item_eval` in which only the argument of line 191 changes, now three
transforms plus the identity case:
`lum` (condition c, unmodified) / `torch.full_like(lum, 0.5)` (condition a) /
`torch.zeros_like(lum)` (condition b) / `lum` with its frame axis permuted by a fixed,
per-item random permutation drawn once and recorded in `gray_controls.json` (condition d) — the
permutation is applied to the input `lum` tensor only; the target used by the decoder/loss is
unchanged.
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
real stimulus, not the resting state. Condition (d) shuffled is a fourth thing again: the same
content and the same per-frame image statistics as real input, with only the temporal ordering of
frames destroyed.

## 5. Outputs
New directory `CS/results/diagnostics/gray/` (nothing written anywhere else). Named by subject
(the gray-stimulus diagnostic), not by night — this directory hosts diagnostics over runs from
several nights (Ark; Zcode agrees).
- `gray_losses.csv` — first two lines `# PREVIEW DIAGNOSTIC -- NOT A TEST (...)` and
  `# script_sha256=<...>` (convention: `rowB.py:307-310`, `rowB_profiles_*.csv:1`); columns
  `run,label,checkpoint_iter,condition,loss_16` + 16 `loss_item_<short>` columns, `condition` now
  taking four values `gray|zero|real|shuffled`; every number written with `repr(float(x))` — full
  float, no rounding (`rowB.py:315-319`).
- `gray_controls.json` — `meta` with: `status`, `script_sha256` of the new script **and** of
  `diag1_eval_paths.py`, `ablation.py`, `rowB.py` (pattern: `ablation_night3.py:76-83`),
  `flyvis.__version__`, `torch.__version__`, python, `torch.cuda.get_device_name(0)`, `netdir`,
  `device`, `utc`, `val_items`, checkpoint names, the exact definition of each condition
  (including, for `shuffled`, the per-item frame-permutation seed), the seven invariants per
  evaluation, and `constant_output_null` (§6).

## 6. Controls
- **P0 reproduction.** Condition (c) must reproduce each checkpoint's stored `val_loss`
  (`diag1_eval_paths.py:147`) to <= 1e-4, and `per_item_mean - hook_eval()` to <= 1e-4. Prior
  observed values: -1.29e-05 and -5.91e-05 (`night3/.../ablation/README.md:117-120`).
- **Copy fidelity.** On one checkpoint, the new copy with the identity transform must return a
  per-item vector **exactly equal** to `D.per_item_eval(solver)`. If it does not, the copy is wrong
  and nothing else in the run is interpretable.
- **Fresh process.** Repeat all 48 cells in a second process; gate max |delta| <= 1e-4; record the
  actual spread rather than asserting it.
- **Iteration 0, gray vs real.** Expectation, stated in advance: a *difference*, but a small one.
  The stored iteration-0 losses are 1212.5556 / 1212.5556 / 1212.5530 / 1212.5592 / 1212.5497 /
  1212.5379 for seeds 0/0'/1/2/3/4 (`night2` and `night3` `rowB_eval_records.json`), i.e. the six
  untrained networks agree to ~0.02 on real input — consistent with a near-input-independent
  decoder output. The difference `L_untrained_gray(s) - L_untrained_real(s)` is recorded as a
  control number per seed, not used in the reading (Ark, Zcode) — the reading's reference is
  `L_untrained_gray(s)` itself, not `L_untrained_real(s)` (§7).
- **Constant-output null (Zcode).** Compute, from the targets alone, the loss a constant
  prediction would incur on the 16 items: the same `l2norm` used elsewhere in this evaluator,
  applied to `y_gt` against (i) its own per-item mean over frames and hexals, and (ii) zero — both
  are one line over the already-rendered targets. State both numbers; the executor must print (i),
  the per-item-mean version, as `constant_output_null` — it is the tighter, best-possible-constant
  comparator (comparator (ii), zero against `y_gt`, is weaker and purely illustrative, and is not
  itself `constant_output_null`). Record `constant_output_null` in `gray_controls.json`. Purpose:
  if `constant_output_null` is ≈ 1212, "gray ≈ 1212" is weak evidence by itself for any network,
  and conditions (b) zero and (d) shuffled carry the reading instead.

## 7. Pre-registered readings (verbatim)
(i) **Band, paired per seed, in units of the learned gain** (Zcode, building on Ark). Define
`gain_s = L_untrained_real(s) - L_trained_real(s)` (the loss improvement training bought, per
seed, on real input). Reading (i) holds for seed `s` if
`|L_trained_gray(s) - L_untrained_gray(s)| <= 0.1 * gain_s`
— "gray removes >= 90% of the learned gain." The reference is the **untrained** network on gray,
`L_untrained_gray(s)`, not the untrained network on real input. This replaces the earlier
"~1212 / agree the band with Ark" formulation; no fixed absolute number is pre-registered, only
the per-seed formula above.

(ii) **Seed 2, stated on both (a) and (b) explicitly** (Ark + Zcode):
- explosion on both (a) gray and (b) zero -> fragility to absence of drive is real;
- explosion only under the ablation's forced-zero state, i.e. neither (a) nor (b) explode -> the
  ablation deltas — **+21,158** (R2 single-type clamp-to-0, `delta_16` = +21157.5,
  `ablation_profiles.csv`, also pre-registered at `ablation_night3.py:64-65`) and **+30,626**
  (full R1-R8 clamp-to-0, seed-2 loss 31,774 minus the seed-2 trained baseline 1147.72, night-3
  record `docs/experiments/003-night3-seeds-3-and-4.md` §6c) — measure the dynamics' fragility to
  a zero clamp specifically, an instrument artefact, not a vision dependence, and the R2 ablation
  finding must be reworded accordingly.
(b) zero is the condition closest to the ablation (both silence the photoreceptor rows to a
constant, R1-R8); (a) gray is the third point (a non-zero, physiologically-meaningful constant).
Reference: seed 2's dominant single-type ablation is **R2, delta_16 = +21157.5**
(`night2/.../ablation/ablation_profiles.csv`; also pre-registered at `ablation_night3.py:64-65`).
Trained-checkpoint losses for the five other runs at 250,008: 1148.81, 1160.98, 1144.64, 1155.77,
1156.83; seed 2 is 1147.72.

(iii) **Reading for (d) shuffled frames**, fixed now, using the same per-seed gain band as (i):
- shuffled ~ real, i.e. within `0.1 * gain_s` of `L_trained_real(s)` -> the learned gain is not
  about motion;
- shuffled ~ gray, i.e. within `0.1 * gain_s` of `L_untrained_gray(s)` -> the learned gain is
  about temporal content;
- neither -> recorded as between.

## 8. Runtime — ESTIMATE
Measured reference points: night-2 ablation did 276 sixteen-item evaluations in 113.8 s wall,
0.18-0.34 s per evaluation (`night2/.../ablation/README.md:130-132`); night-3 recorded
`one_evaluation_wall_s` 0.492 (seed 3) and 0.179 (seed 4) (`ablation_controls.json`).
48 evaluations + 48 for the repeat + one solver build (~20-40 s, ESTIMATE) -> **~2-3 minutes
total, ESTIMATE**. No new rendering is needed: the Sintel rendering already exists under
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

## 10. Revision history
- **v1 -> v2** (Ark, review posted 06:24Z 2026-09-16): output directory renamed to
  `CS/results/diagnostics/gray/`, named by subject not by night (§5); reading (ii) split across
  conditions (a) and (b) explicitly, with (b) named as the condition closest to the ablation and
  (a) as the third point (§7); "wrong video" condition proposed, refined by Zcode into condition
  (d) (§1, §3, §7); paired per-seed band framing for reading (i) (§7).
- **v1 -> v2** (Zcode, review posted 06:27Z 2026-09-16): condition (d) specified precisely as
  frame-axis-permuted input with a fixed, recorded permutation seed, content and per-frame
  statistics preserved, temporal structure destroyed (§1, §3, §4); reading (i) and the new reading
  (iii) for (d) put in units of the learned gain `gain_s = L_untrained_real(s) - L_trained_real(s)`,
  band `0.1 * gain_s`, gray reference taken on the untrained network (§7); analytical
  constant-output null added, computed from the targets alone and recorded as
  `constant_output_null` (§6).
- **v1 -> v2** (CC, mechanical follow-through): 12 x 4 = 48 evaluations propagated through §1, §5,
  §6, §8; the iteration-0 gray-vs-real control sentence kept but restated as a recorded control
  number only, not used in the reading (§6); header and launch-rule lines added; v1's discarded
  sweep noted at the top.
