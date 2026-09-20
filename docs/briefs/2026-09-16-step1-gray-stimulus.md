# Brief — step 1: gray-stimulus control

**v2, 2026-09-16, after review by Ark and Zcode; v1 was posted at 06:23Z; a v1 sweep was run at
~06:30Z before the review arrived and its output was discarded unread (CC's protocol error,
recorded in chat); nothing from it is used.**

**v3 (2026-09-16 evening, after the gate stop).** v2 was launched on Mike's word at 19:52Z
(actually 19:50:18Z per the run record) and stopped at §6's copy-fidelity gate: the identity-
transform copy passes bitwise at `chkpt_00000` but cannot pass "exactly equal" at `chkpt_00071`,
because `D.per_item_eval` itself does not reproduce itself in the same process at that checkpoint
(five repeat calls on the same loaded checkpoint give five distinct 16-item means, spread
8.58e-05, per-item spread 0.0009765625; source: `cudnn.deterministic=False` in `build_solver`,
`diag1_eval_paths.py:90-93`, matching the night runs' `--no-determinism`). The copy's deviation
from the original equals the original's own repeat floor exactly. P0 passed at both checkpoints.
Nothing else ran. §6 and §7 below are revised to state the evaluator's own measured floor as the
bar, in place of exact equality and an unstated "explodes" threshold; v2's text is kept and the
diffs are itemised in the revision history (§10). **Launch of v3 requires Mike's explicit
"go ahead" (translated from Russian) in the chat again; the v2 launch word was consumed by the
run that stopped at the
gate.**

**v4, 2026-09-17, after the second gate stop.** v3.1 was launched on Mike's word and stopped a
second time at §6's copy-fidelity gate, now failing on a numeric comparison rather than exact
equality: the copy's worst per-item deviation (0.000732421875) exceeded the 10-pair floor
(0.00048828125) by one quantisation step (step 0.000244140625) — records
`results/diagnostics/gray/README.md` and `README_v2_gate_stop.md`, commits `4e54965`, `8f0208f`.
On the 16-item mean the copy lay inside the originals' own range (max |mean(A) − mean(B_k)|
4.48e-05 vs a floor on the mean of 8.87e-05); the per-item floor itself varied 2x between processes
(0.0009765625 measured in the v2 process). CC proposed v4; Ark (20:23Z) and Zcode (20:24Z)
accepted with additions. §6's copy-fidelity control is replaced by a **code gate** — a diff of the
copied function against its source, not a number (Ark: the diff replaces the numeric gate in that
role) — and the numeric comparisons between copy and original become recorded quantities with a
documented ceiling, never a comparison against another run's extremum; see checklist rule 17. See
revised §6 and the v3.1 -> v4 entry in §10. **Launch of v4 requires Mike's explicit "run step
1" (translated from Russian) in the chat again, naming the step; the v3.1 launch word was consumed by the run that stopped
at the gate a second time; not while a training wave runs.**

**v5, 2026-09-17, after the third gate stop.** v4 was launched on Mike's word (08:14:48Z) and
stopped a third time at §6: the code-diff gate passed and P0 passed, but the stop applied the
copy-fidelity 1e-4 mean ceiling to a single original call (|mean(A) − mean(B_1)| = 1.20e-04) while
the original's own five calls differ up to 1.11e-04 on the mean in one process (commit `b7c2879`;
`results/diagnostics/gray/README.md`, `gray_v4_main_gate_stop.log`). CC proposed v5 in chat
08:25:52Z; Ark (08:27:19Z) and Zcode (08:28:59Z) accepted, Ark with two additions. The numeric
comparison between copy and original (§6) is redefined from a single original call to the mean of
five copy calls vs the mean of five original calls, same checkpoint, same process, ceiling raised
to **1e-2**, with the ceiling and its derivation printed next to every number (Ark). P0 (§6) is
likewise redefined on the mean of five calls against the stored `val_loss`, ceiling **1e-3**. The
fresh-process repeat (§6) is likewise redefined on the mean of five calls per cell, ceiling
**1e-2**. §6 gains an explicit Stops enumeration; §8 gains a cost note reflecting the five-call
design. See revised §6, §8 and the v4 -> v5 entry in §10. **Launch requires Mike's new "run step
1" (translated from Russian) in the chat; the 08:14:48Z word was used by the v4 run.**

**Launch only on Mike's explicit "run step 1" (translated from Russian) for this step in the DPC Research chat; not
while a training wave runs.**

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
- `gray_repeat_controls.json` **(v3, named here so it is not a surprise; gate updated in v4)** —
  the fresh-process repeat pass (§6): per checkpoint, the in-process floor (max |B-C|, per-item
  and on the 16-item mean, from two repeat calls of the original `D.per_item_eval`); per cell, the
  second-process 16-item-mean delta against the first process, recorded per-item as well but
  gating only on the 16-item mean; and, per cell, whether it passes <= 1e-4.

## 6. Controls
- **P0 reproduction (v5, revised at the third gate stop).** Condition (c) must reproduce each
  checkpoint's stored `val_loss` (`diag1_eval_paths.py:147`): the gating quantity is the mean of
  five calls of condition (c) against the stored `val_loss`, ceiling **1e-3** (the largest value
  on record on this path is 7e-05). `per_item_mean - hook_eval()` is **recorded, not gating** (v5.1, CC): C3 Part B measured the
  same-weights hook − `per_item_eval` difference at up to 1.435e-4 (903@250008), so a 1e-4 gate on it
  would be a fourth false stop; its sanity bound is the P0 ceiling, 1e-3, on the mean of five calls. Prior observed values: -1.29e-05 and -5.91e-05 (`night3/.../ablation/README.md:117-120`).
- **Copy fidelity — code gate (v4, unchanged in v5).** (Ark: the diff replaces the numeric gate in
  that role.) The copied `per_item_eval` must differ from `diag1_eval_paths.py`'s `per_item_eval`
  only in the declared lines: the transform on the `add_input` argument (diag1 line 191, §3) and
  the loop-variable rename `_` -> `_i` (line 188, §9.10). The executor prints the unified diff of
  the two function bodies into `gray_controls.json` and the README; any other difference -> stop.
  This gate passed on every run to date, including the v4 run that stopped on the numeric
  comparison below (v5 header note).
  **Numeric comparison (v5, revised at the third gate stop) — mean of five vs mean of five.** On
  each checkpoint, five original calls B_1..B_5 and five copy calls A_1..A_5, all in the same
  process; the gating quantity is |mean(A_1..A_5) − mean(B_1..B_5)| on the 16-item mean, ceiling
  **1e-2**. Print the ceiling and its derivation next to every number (Ark): ≈ 50x above all
  measured noise on this comparison to date (≤ 2.0e-4 between processes, C3 Part B
  `results/diagnostics/c3/README.md`), and ≈ 500x below the narrowest pre-registered reading band
  (`0.1 * gain_s` ≈ 5–6, §7). The ceiling is a **sanity bound, not a precision bound** (Ark): it
  catches a wrong copy — wrong checkpoint, data, or index — whose error is in units, not a subtle
  numeric drift. Per-item deviations for all pairs among B_1..B_5 and for each A_i against each
  B_k, and the pairwise floor among B_1..B_5 itself (max over all 10 pairs, per-item and on the
  16-item mean), are recorded per checkpoint in `gray_controls.json` but do not gate. At iteration 0 bitwise equality is **recorded, not required** (v5.1, CC): C3 Part B saw single
  calls at iteration 0 one float64 step off (1212.5497364997864); the ceilings above apply there too.
  **Note (Zcode) — the quantisation step.** Per-item losses are float32; the unit in the last place
  (ulp) of a float32 value in [2048, 4096) is 2⁻¹² = 2.44140625e-4, and in [4096, 8192) it is
  2⁻¹¹ = 4.8828125e-4; the largest per-item losses (ambush_2 splits ≈ 4049–4765) set the lattice,
  so per-item differences are multiples of these steps. The grid is a property of the largest
  per-item values, not of the mean.
- **Fresh process (v5, revised at the third gate stop).** Repeat all 48 cells in a second process.
  Each cell's value is the mean of five copy (A) calls, matching the numeric-comparison definition
  above. Gate on that per-cell mean: |delta| between the two processes ≤ **1e-2** per cell.
  Per-item repeat differences between the two processes stay **recorded, not gating** — state next
  to the gate the measured in-process spread of that checkpoint (8.6e-05 at `chkpt_00071`, from
  five repeat calls of the original `D.per_item_eval` in one process — see Copy fidelity above).
  Rationale: the evaluator runs with `cudnn.deterministic=False` by the night runs' own
  configuration (`build_solver`, `diag1_eval_paths.py:90-93`); changing that would change the
  evaluator.
- **Stops (v5).** crash; NaN/inf; code-diff failure (Copy fidelity above); any of the three
  ceilings above (numeric-comparison ceiling 1e-2, P0 ceiling 1e-3, fresh-process ceiling 1e-2); a
  run-dir file change (§9.2). One line (Ark): in stops 1–3 (the v2, v3.1, and v4 gate stops) the
  decisive gate — the code diff — passed whenever it ran, and P0 passed; the stops cost no data.
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

**Operationalisation of "explodes" (v3, pre-registered at the gate stop).** For a trained network
under condition `cond` in `{gray, zero}`, define
`excess_cond(s) = L_trained,cond(s) - L_untrained_gray(s)` — the excess of the trained network's
loss under that condition over its own (same-seed) untrained-on-gray loss. Then, in units of
`gain_s` (§7(i)): `excess_cond(s) >= 10 * gain_s` -> "explodes"; `excess_cond(s) <= 0.1 * gain_s`
-> "returns"; otherwise -> "between". Ablation reference point, for scale: seed 2, R1–R8 full
clamp (night-3), excess `+30,626` ≈ 500 × `gain_s` — two orders of magnitude above the "explodes"
threshold.

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

(iii) **Reading for (d) shuffled frames**, fixed now, using the same per-seed gain band as (i)
(**v3: branches made exclusive at the gate stop**). Shuffled is read against the **nearer** of the
two references, `L_trained_real(s)` and `L_untrained_gray(s)`:
- "not about motion" if shuffled is within `0.1 * gain_s` of `L_trained_real(s)` **and** farther
  than `0.1 * gain_s` from `L_untrained_gray(s)`;
- "about temporal content" if the reverse: within `0.1 * gain_s` of `L_untrained_gray(s)` **and**
  farther than `0.1 * gain_s` from `L_trained_real(s)`;
- "between" otherwise — including the case where the two references themselves lie within
  `0.2 * gain_s` of each other, in which case both branches can be satisfied at once and the
  reading is **void for that seed**, recorded as void rather than assigned to either branch.

## 8. Runtime — ESTIMATE
Measured reference points: night-2 ablation did 276 sixteen-item evaluations in 113.8 s wall,
0.18-0.34 s per evaluation (`night2/.../ablation/README.md:130-132`); night-3 recorded
`one_evaluation_wall_s` 0.492 (seed 3) and 0.179 (seed 4) (`ablation_controls.json`).
**Cost note (v5, revised at the third gate stop):** 48 cells × 5 calls + repeat ≈ 1–2 min of
evaluation plus solver builds (estimate). No new rendering is needed: the Sintel rendering already
exists under `CSD/renderings/RenderedSintel_0000`.

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
10. **(v3, added at the gate stop)** Exception to §3's "only the argument of line 191 changes":
    the loop-variable rename `_` -> `_i` in the copied `per_item_eval` (now
    `per_item_eval_transformed`) is allowed — the executor needed it to index the per-item frame
    permutation of condition (d) (shuffled). It must be declared in the script's docstring; it
    already is (`gray_stimulus.py`, module docstring and `per_item_eval_transformed`'s own
    docstring).

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
- **v2 -> v3** (2026-09-16 evening, after the gate stop; source: the executor's run at 19:50:18Z
  and `results/diagnostics/gray/README.md` §3, §7): copy-fidelity control (§6) restated against
  the evaluator's own in-process repeat floor instead of exact equality, since
  `cudnn.deterministic=False` (`diag1_eval_paths.py:90-93`) makes `D.per_item_eval` itself
  non-reproducible in-process at `chkpt_00071` (spread 8.58e-05 on the 16-item mean, 0.0009765625
  per-item) while iteration 0 stays bitwise; fresh-process gate (§6) restated as <= 3x that floor,
  with the existing 1e-4 target kept and reported separately; reading (ii) (§7) given a
  pre-registered numeric "explodes"/"returns"/"between" operationalisation in units of `gain_s`,
  referenced against the R1-R8 clamp excess (+30,626 ~ 500 x `gain_s`), replacing the executor's
  provisional trained-real-baseline threshold; reading (iii) (§7) branches made mutually exclusive
  by nearest-reference, with the overlap case (references within 0.2 x `gain_s`) recorded as void
  rather than double-satisfied; §5 gains `gray_repeat_controls.json`; §9 gains an explicit
  exception for the `_` -> `_i` loop-variable rename already declared in `gray_stimulus.py`'s
  docstrings; header gains the v3 note and a fresh launch-word requirement. v2's text is otherwise
  unchanged.
- **v3 -> v3.1** (2026-09-16 20:09Z, Ark): the copy-fidelity floor is the maximum over all 10
  pairs of five calls of the original evaluator, not one pair; no other change. Reviewer pass on
  v3: Ark 20:09Z, no objections to the four v3 edits. Launch still requires Mike's "go ahead"
  (translated from Russian).
- **v3.1 -> v4** (2026-09-17, after the second gate stop; source: DPC Research chat 20:23–20:29Z;
  records `results/diagnostics/gray/README.md` and `README_v2_gate_stop.md`, commits `4e54965`,
  `8f0208f`): v3.1 was launched and stopped a second time at §6's copy-fidelity gate — the copy's
  worst per-item deviation (0.000732421875) exceeded the 10-pair floor (0.00048828125) by one
  quantisation step (0.000244140625), while on the 16-item mean the copy lay inside the originals'
  own range (max |mean(A) − mean(B_k)| 4.48e-05 vs floor 8.87e-05) and the per-item floor itself
  varied 2x between processes (0.0009765625 in the v2 process). Copy fidelity (§6) is replaced by
  a **code gate** (Ark: the diff replaces the numeric gate in that role): the executor prints the
  unified diff of the copied `per_item_eval` against `diag1_eval_paths.py`'s `per_item_eval` into
  `gray_controls.json` and the README, gating on any difference beyond the two declared lines
  (the `add_input` transform, line 191, and the `_` -> `_i` rename, line 188). Numeric comparisons
  between copy and original are now recorded, not gating, with a documented ceiling: per-item
  |A−B_k| > 1.5 x 0.0009765625 = 0.00146484375, or 16-item-mean |mean(A) − mean(B)| > 1e-4;
  iteration 0 stays bitwise. Zcode's account of the quantisation step added as a note in §6 (per-
  item float32 ulp 2.44140625e-4 in [2048,4096), 4.8828125e-4 in [4096,8192), set by the largest
  per-item losses, e.g. ambush_2 ≈ 4049–4765, so the grid is a property of the largest values, not
  the mean). Fresh-process repeat (§6) gate simplified to the 16-item mean alone (≤ 1e-4 per cell);
  per-item repeat differences between the two processes recorded, not gating. Header gains the v4
  note and a fresh launch-word requirement naming the step, "run step 1" (translated from
  Russian), and excluding launch
  while a training wave runs. New checklist rule 17 (`docs/CHECKLIST-research-repo.md`) records the
  general defect. Ark 20:23Z, Zcode 20:24Z, both accepted with additions.
- **v4 -> v5** (2026-09-17, after the third gate stop; source: DPC Research chat 08:25:52–08:28:59Z;
  records `results/diagnostics/gray/README.md`, `gray_v4_main_gate_stop.log`, commit `b7c2879`):
  v4 was launched (08:14:48Z) and stopped a third time — the code-diff gate passed and P0 passed,
  but the stop applied the copy-fidelity 1e-4 mean ceiling to a single original call
  (|mean(A) − mean(B_1)| = 1.20e-04) while the original's own five calls differ up to 1.11e-04 on
  the mean in one process. CC proposed v5 in chat 08:25:52Z; Ark (08:27:19Z) and Zcode (08:28:59Z)
  accepted, Ark with two additions. Copy fidelity's numeric comparison (§6) is redefined from a
  single original call to the mean of five copy calls vs the mean of five original calls, same
  checkpoint, same process, ceiling **1e-2**, stated with its derivation next to every number
  (Ark): ≈ 50x above all measured noise (≤ 2.0e-4 between processes, C3 Part B
  `results/diagnostics/c3/README.md`) and ≈ 500x below the narrowest pre-registered reading band
  (`0.1 * gain_s` ≈ 5-6, §7); the ceiling is stated explicitly as a sanity bound, not a precision
  bound (Ark) — it catches a wrong copy (wrong checkpoint, data, or index), an error in units, not
  a subtle drift. Per-item numbers stay recorded, not gating. P0 reproduction (§6) is likewise
  redefined on the mean of five calls against the stored `val_loss`, ceiling **1e-3** (the largest
  value on record on this path is 7e-05). Fresh-process repeat (§6) is likewise redefined on the
  mean of five calls per cell, gate |delta| <= **1e-2** per cell between processes. §6 gains an
  explicit Stops enumeration (crash, NaN/inf, code-diff failure, the three ceilings above, a
  run-dir file change) with Ark's note that in the first three gate stops the decisive gate (the
  code diff) passed whenever it ran, and P0 passed, so those stops cost no data. §8 gains a cost
  note: 48 cells x 5 calls + repeat ~= 1-2 min of evaluation plus solver builds (estimate). Header
  gains the v5 note and a fresh launch-word requirement; the 08:14:48Z word was used by the v4
  run.
- **v5 -> v5.1** (2026-09-17, CC, before any launch): two remaining single-call gates removed —
  `per_item_mean − hook_eval()` becomes recorded (measured up to 1.435e-4 on the same weights, C3
  Part B) with the 1e-3 P0 ceiling as its sanity bound; iteration-0 bitwise equality becomes recorded
  (one-float64-step deviations measured in C3 Part B). No other change. Launch still requires Mike's
  new "run step 1" (translated from Russian).
