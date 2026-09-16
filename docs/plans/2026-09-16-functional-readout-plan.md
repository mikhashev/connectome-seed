# Functional readout plan — 2026-09-16

**Date:** 2026-09-16 · **Written for:** Mike and the reviewers (Ark, Zcode) · **Context:** the
night-3 ablation record (`docs/experiments/003-night3-seeds-3-and-4.md` §6, §6c) and the checklist
addition (`docs/CHECKLIST-research-repo.md` rule 16). Translated from this session's chat plan,
faithfully, with the numbers and readings kept as stated there; cost estimates are marked as
estimates, not measurements.

## Roles

- **Mike** — the words «старт» / «пиши команду» and the decisions.
- **CC** — briefs, execution by subagents, verification of raw outputs, records, commits.
- **Ark and Zcode** — review every brief BEFORE launch and recompute from raw files AFTER.
  Ark additionally: provenance of the `groundtruth_utils` fields and the genome design rewritten
  around S2. Zcode additionally: the C6 control specification and the reading of the
  gray-stimulus control.

## Step 0 — records (CC, text, today)

Override the machine verdict in 003 §6 and the ablation README; checklist rule 16; the "scale 60"
paragraph in 003. (This step is what this commit carries.)

## Step 1 — gray stimulus (CC, minutes — estimate; brief v2 reviewed by Ark and Zcode)

The six 250,008 checkpoints plus each run's iteration-0 checkpoint, same 16 items, same
evaluator, **no ablation**, four input conditions: (a) constant gray 0.5, (b) constant zero 0.0,
(c) unmodified real input (P0), (d) the same item's input with the frame axis permuted
(shuffled — fixed permutation seed recorded in the json, content and per-frame image statistics
preserved, temporal structure destroyed). Output: `results/diagnostics/gray/` (named by subject,
not by night — this directory hosts diagnostics over runs from several nights).

**Readings fixed before launch (brief v2):**

- (i) **paired, per seed, in units of the learned gain**: `gain_s = L_untrained_real(s) -
  L_trained_real(s)`; holds for seed `s` if `|L_trained_gray(s) - L_untrained_gray(s)| ≤
  0.1 · gain_s` ("gray removes ≥ 90% of the learned gain"); the reference is the untrained
  network on gray, not on real input.
- (ii) seed 2 stated on both (a) gray and (b) zero explicitly: explosion on both → fragility to
  absence of drive is real; explosion only under the ablation's forced-zero state (neither (a)
  nor (b) explode) → the ablation deltas measure fragility to a zero clamp specifically, an
  instrument artefact, and the R2 finding (explosion to 31,774 under photoreceptor-silencing
  ablation, §6c above) must be reworded; (b) is the condition closest to the ablation, (a) is the
  third point.
- (iii) reading for (d) shuffled, same band as (i): shuffled ≈ real → the learned gain is not
  about motion; shuffled ≈ gray → the learned gain is about temporal content; between → recorded
  as between.

**Controls:** the iteration-0 gray-vs-real difference is recorded as a control number only, not
used in the reading; an analytical constant-output null is computed from the targets alone;
repeat in a fresh process, agreement ≤ 1e-4.

## Step 2 — tuning battery (CC, minutes per checkpoint — estimate; brief v2 reviewed by Ark + Zcode)

Same seven networks per seed (250,008 and iteration 0): flashes → ON/OFF flash-response index per
type (65); moving edges → DSI and preferred direction per type; comparison with the built-in
literature table (polarity, DSI types, T4/T5 tuning curves from Maisak 2013) using flyvis's own
functions. Output: `results/diagnostics/tuning/` (named by subject, not by night). **dt decision
(Ark, Zcode concurring): primary dt = 0.02** (the networks' own training regime; the Euler step
enters the kinetics — the rate divides by `max(time_const, dt)` in `dynamics.py`, so a different
dt changes the effective kinetics, not only the resolution); **secondary dt = 1/200** (flyvis's
own regime, for comparability); the difference between the two is a third quantity: tuning that
holds at both dt → robust, tuning that holds only at 1/200 → an artefact of the step, a result
about the substrate.

**Readings declared before data:**

- (a) **Twin trap in tuning space** — (0, 0′) minimum of 15 by rank, with the 1/15 floor as a
  sanity check.
- (b) **Is the dominant type functional** — deviation of the dominant type's tuning (R2 in
  seed 2, Mi4 in seed 3, CT1 in seed 4) from the same type in the five other runs, ranked among
  65 types, outcomes ≤ 3 / ≥ 30 / between as in Ark's design.
- (c) How many of the 65 types hold the literature polarity and direction in each fly, and the
  spread of that count across flies.
- (d) Iteration 0 as the null: what tuning connectivity alone gives without training.

All diagnostics, not tests.

## Step 3 — genome (Ark writes the design around S2 with label provenance)

Ark writes the design around S2 with label provenance; CC writes the two-page "what is the genome
here" with source addresses after the design; Zcode writes the C6 control specification. CC
extracts the label array and the rule bank as soon as Ark hands over the field list.

**Boundary (Ark, 2026-09-16 19:51Z, recorded on his request):** C6/S2 fit the *compiled* rule bank
(the h5 edge table: 2,355 rows `(source_type, target_type, du, dv) → n_syn, sign`, identical at
extent 5 and 15); the transition json → compiled bank is **not verified and not licensed** by
either test. Measured 2026-09-16 (CC, read-only): the json carries 605 `(src, tar)` entries with
2,140 offset rows; 2,117 of those keys match the bank one-to-one, 238 bank rows are added by the
convex-hull fill (`n_syn_fill = 1`, all n_syn = 1.0), and 23 json rows have no bank counterpart
(all self-projections of the `stride [3, 2]` types Lawf1/Lawf2 whose offset is not on the type's own
stride lattice, dropped by the `KeyError` suppression at `connectome.py:497-498`). On the 2,117
matched keys the bank is an **identity copy of the json up to a float32 cast**: max |n_syn_bank −
n_synapses_json| = 6.5e-6, and `n_syn_certainty` = `lambda_mult` to 4.4e-6 (`connectome.py:403-432,
473-499, 248, 258`; no scaling, averaging or rounding exists in the code). CC's chat figure of
2026-09-16 19:49Z, "only 807 of 2,117 keys carry the same n_syn", was an artefact of comparing a
float64 json value with the float32 bank at a 1e-9 tolerance and is withdrawn (corrected in chat
the same evening). So the json → bank transition is deterministic and, apart from the hull fill and
the stride-dropping, value-preserving; it is still not exercised by C6/S2 themselves, so a success
of S2 licenses "predict the bank from the bank" plus this documented transition, not more. The pair count is 605 in the json and 604 instantiated: `Lawf1 → Lawf1`
with its single offset `[1, 0]` never lands on a Lawf1 cell under that type's `stride [3, 2]`
(mechanism inferred from the layout pattern, not executed).

## Step 4 — night 4 (Mike launches; independent of steps 1–3)

Replicate 3′ first in the wave, new seed 5 second, `-NoReplicate`, Windows Update paused until
2026-10-20.

## Order and start

Step 0 starts now on Mike's «давайте пробовать». Briefs for steps 1 and 2 follow and are posted
to chat for review by Ark/Zcode before launch. "Minutes" are estimates from run volume, not
measurements — the first thing reported after launch is the actual time.

**Rule (Mike, 06:3xZ): nothing launches without Mike's explicit «запускай» in the chat; plan
approval is not a launch word. On 2026-09-16 CC launched step 1 before the reviews arrived; the
output was discarded unread and step 1 is re-run from brief v2 only on Mike's word.**

2026-09-16 20:03Z: step 1 (v2) launched on Mike's word and stopped at the copy-fidelity gate
(evaluator floor, not a copy defect); brief amended to v3; re-launch on Mike's word.

## After night 4 (proposed, each on Mike's word)

(a) **Jitter at C3** (CC, proposed 2026-09-16 05:38Z; Ark 19:58Z: only after night 4): re-run one
seed to 26,000 iterations with the validation hook every 100 iterations to see the trajectory
jitter at C3 directly; requires an optional flag in `run_individual.py` whose default path is
byte-identical to the current one, shown by diff before any run.

(b) **Evaluator floor by path, state and repeat type** (Ark 20:09Z, 20:11Z; Zcode 20:14Z): three
readings at checkpoints 0 / 25,212 / 250,008 of one seed × both evaluation paths (state-hook path
used by ablation/rowB; `per_item_eval` → `solver.test` path used by diag1/splice/gray) ×
within-process and between-process repeats. Known so far: `per_item_eval` within process at
250,008 = 8.6e-05 on the 16-item mean (0.0 at iteration 0); state-hook path between three fresh
processes at 250,008 = 8e-08 (`rowB_controls.json`); the state-hook path was never repeated
within one process. Answers both "does the floor grow with training" and "is the floor a
property of the checkpoint, the path, or the process". Rule to carry into the next registration
(Ark 20:11Z): the two paths differ in the nature of their repeat, and a floor measured on one
path must not be substituted into a rule for the other.
