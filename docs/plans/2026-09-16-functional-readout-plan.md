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
