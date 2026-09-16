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

## Step 1 — gray stimulus (CC, minutes — estimate; brief reviewed by Zcode)

The six 250,008 checkpoints plus each run's iteration-0 checkpoint, same 16 items, same
evaluator, **no ablation**, input replaced by a constant gray (and separately by zero).

**Readings fixed before launch:**

- (i) gray ≈ 1212 for five runs → "learned = vision" closed from the second side.
- (ii) seed 2 under gray: ≈ 1212 → its explosion to 31,774 (under photoreceptor-silencing
  ablation, §6c above) was an artefact of forcing photoreceptor activity to zero, not a vision
  dependence; explosion under gray as well → the dependence is real.

**Controls:** iteration 0 under gray must give ≈ 1212; repeat in a fresh process, agreement
≤ 1e-4.

## Step 2 — tuning battery (CC, minutes per checkpoint — estimate; brief reviewed by Ark + Zcode)

Same seven networks per seed (250,008 and iteration 0): flashes → ON/OFF flash-response index per
type (65); moving edges → DSI and preferred direction per type; comparison with the built-in
literature table (polarity, DSI types, T4/T5 tuning curves from Maisak 2013) using flyvis's own
functions.

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
to chat; they launch after the first review by Ark/Zcode, or immediately on Mike's «старт».
"Minutes" are estimates from run volume, not measurements — the first thing reported after launch
is the actual time.
