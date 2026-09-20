# Plan after the USPEX reading — the endpoint before N

**Date:** 2026-09-17 (UTC; 2026-09-18 local, UTC+7) · **Written for:** Mike and the reviewers
(Ark, Zcode) · **Written by:** CC on Mike's word "do it, and write a new plan" — translated from Russian —
(2026-09-17,
12:20 UTC) · **Context:** the USPEX review
`research/uspex/2026-09-17-uspex-analogue-to-adr-002.md` and the two errors it exposed.

This file records an order of work and the state of the evidence. **It decides nothing:** every
launch still waits on Mike's word, and the endpoint below is not registered by this file.

## 1. Why the plan changed — and what did not change it

The reading of Oganov did not change the plan. Two of our own errors did, and the reading is what
exposed them.

- **A population substitution.** `SD = 1.7953` at the 250,000 hook is the sample sd over seeds
  **{0, 1, 2}, n = 3** — the column is headed `SD(0,1,2) n=3`
  (`docs/experiments/002-night2-seeds-1-and-2.md:71`). The six-individual figure at the same rung
  was already on record: **5.1425**
  (`docs/experiments/004-night4-replicate-3prime-and-seed-5.md:81`). The smaller of the two had
  been carried into a cost estimate, and it is 2.86× smaller.
- **A class error in the endpoint.** Our (b) test asks for the **order of final states**. USPEX's
  own statistic asks **how many steps it takes to reach a target fixed outside the run**
  (generations and structures to `E = 90.912`). Run-to-run scatter moves the second and destroys
  the first. This is not an instrument that is too weak; it is the wrong class of quantity.

What the USPEX reading contributed is exactly two things: the language for the second error, and
the architectural reading of ADR-002 — their cheap side proposes and filters, their expensive side
issues the verdict, and their cheap side carries an explicit out-of-distribution exit ("should
either be rejected, or calculated at the ab initio level and then used for re-training the MLF").
It does **not** licence our condition; it warns against its shape.

## 2. What is established, and what may not be cited

**Established without any model** — this is the statement to quote:

> The two replicate gaps at the 250,000 hook, **12.7279**
> (`docs/experiments/001-run0-and-replicate.md:68`, table "run 0 against run 0′") and
> **10.4309** (`004:91`, table "the second replicate pair"), are larger than the sd across all
> six individuals at the same rung, **SD(n=6) = 5.1425**, and each of them takes up most of the
> **range** of
> the six individuals themselves — 1145.3572 (seed 1) to 1159.1158 (seed 5), a range of
> **13.7586**: 92.5 % and 75.8 % of it (`004:81`, the eight-run table at iteration 250,000).

**Two different quantities are called "spread" in this project, and they differ by a factor of
2.7 — so this file names both.** `results/night4/README.md:130` uses "spread of the six
individuals" for the **standard deviation**, `SD(n=6) = 5.1425`. The sentence above uses the
**range**, `range(6) = 13.7586` at the hook and `12.1922` on the checkpoint curve. Only one of them
belongs in any given comparison, and under one word the wrong one reaches the gate. Named apart on
Ark's point, 2026-09-17.

**The range in that sentence counts individuals only, on purpose.** Taking the maximum over all
eight stored runs gives 1145.3572 to 1162.9375 = 17.5803, but 1162.9375 is replicate 3′, not an
individual — putting a replicate inside the population a replicate gap is compared against
inflates that population, and always in the one direction that makes the gap look like it fits.
An earlier revision of this file quoted 17.5803; the correction is Ark's, 2026-09-17, recomputed
by CC from the same table.

No ratio and no model are needed for it.

**May not be cited: any nights figure.** Under §(c)1a of the review the moment estimate of the
between-individual variance is negative — 5.1425² = 26.4 against a within-individual variance of
≈105–127 — so the signal/noise model that every price comes out of is contradicted by the data.
"~53 nights", "~16 nights" and "~5 nights" are all products of that model. **N is not
"expensive"; N is currently not estimable.**

**Two further corrections now on record:**

- **Two of the six held-out scenes flip the seed order**, not one, and the "three tasks" were three
  splits of one scene: `drop sequence_02_ambush_2 (3 items) -> 2 < 0 < 1 [FLIP]` and
  `drop sequence_09_bandage_1 (3 items) -> 1 < 0 < 2 [FLIP]`
  (`results/night2/diagnostics/dropk/dropk_summary.md`); `bamboo_1` and `cave_4` do not flip.
- **An individual is more than 65 numbers.** The 65 differing `nodes_bias` values of 8,161 are
  measured, but the run script seeds `random`, `numpy` and `torch` from the seed, so data order and
  augmentation differ per individual as well (`docs/preregistration-cheap-vs-expensive.md`,
  clarification of 2026-09-15). Individuals differ by more than 65 numbers, and twins with
  identical inputs still diverge by 10–13 — which supports the saturating-divergence reading, not
  "the seed sets very little".

## 3. Order of work

Recommended by Ark, CC and Zcode, converged independently in the 2026-09-17 thread. Each launch
waits on Mike's word.

1. **Pre-register the reachability endpoint** — "iterations to cross a fixed aggregate `val_loss`
   level". Zcode drafts; Ark and CC review **before any data is touched**. §4 lists what the
   registration must fix.
2. **Read it.** Minutes of CPU, no GPU: the substrate is already on disk — 72 aggregate `val_loss`
   checkpoints per run × 8 runs, two replicate pairs.
3. **Gate.** If the twin difference in crossing time is not smaller than the between-individual
   difference across the whole registered grid, the ranking-class endpoint is dead on this
   substrate and road **A** is the honest reading. If it is smaller, the endpoint is readable at
   N = 8 and road **C** is not needed to rescue it.
4. **Only then the N floor** (8 or 10). §2's "N is not currently estimable" is about a different
   quantity than this one: what is unestimable is the **replicate budget** r — how many repeats
   per individual a ranking endpoint would need — because the variance model it comes from is
   contradicted by the data. The **number of individuals** for reading (b) is a registered choice
   between 8 and 10 and remains Mike's, once the class of the endpoint is settled.
5. **If nights are bought, the first night is a third replicate pair, not a seventh individual.**
   Every statement about reliability — σ_rep, the ρ ceiling, and the question of whether the
   signal/noise model applies at all — is unestimable on two pairs; §(c)1a's negative variance
   estimate is itself a consequence of σ_rep resting on two observations. A third pair yields a
   **first** estimate, not a good one — at three pairs the sd of σ_rep is still of order ±50 %
   (Ark, 2026-09-17). One night buys that third pair: the measured throughput is **2 runs per night** — night 1 = seed 0 and replicate 0′,
   night 2 = seeds 1 and 2, night 3 = seeds 3 and 4 in one wave, night 4 = replicate 3′ and seed 5
   (`docs/experiments/001`–`004`). A seventh individual buys nothing until the class of the
   endpoint is settled.
6. **Independent of the gate** — these three do not wait on it: the R2 rewording in
   `docs/experiments/002` and `003`, if it is wanted at all (the verdict is already recorded in
   `results/diagnostics/gray/README.md` §8 and `ROADMAP.md` § "Diagnostics while N accrues — the
   functional-readout track", step 1); the "type ablation versus
   input removal" control for Mi4 and CT1(Lo1), which has never been set; and step 2, the tuning
   battery, whose brief is ready and whose prerequisite closed with `32759e2`.

## 4. What the registration must carry

(a)–(c) are Zcode's and Ark's; (d)–(g) are CC's additions from the same thread.

- **(a) The threshold grid as a rule, not a list** — e.g. every level crossed by all eight runs, at
  a fixed step. A grid chosen after looking at the curves manufactures a stable threshold by
  selection.
- **(b) The acceptance criterion in one sentence**, fixed before reading, with no post-hoc choice
  of a favourable threshold.
- **(c) The instrument's resolution, measured rather than assumed.** The checkpoint grid is **not
  uniform**: iterations 0, 12, then 3,600 apart, with a final step of 1,596 to 250,008 — 72 points
  in total (`results/night4/night_report_checkpoints.csv`). Crossing time is quantised by that
  grid.
- **(d) A disqualification clause on the resolution.** If the twin difference in crossing time is
  ≲ one grid step, the test is **unreadable**, not weak — we would be measuring the checkpoint
  interval. Recording this before the computation is what stops it from becoming an explanation
  after it. The precedent is on record: replicate 0′ came in at 1.1104 % against a 1 % tolerance
  (`docs/experiments/001-run0-and-replicate.md:68`), and the discussion of the instrument's floor
  started afterwards.
- **(e) A positive control.** The criterion in (b) only tests discrimination, and a statistic that
  discriminates *nothing* passes it the same way. The control is already on disk: the endpoint must
  separate each trained run from **its own iteration-0 state**, where the untrained level is
  1212.5556 and the learned gain within the same field is 63.7481 for seed 0 — five times the
  largest twin gap (`results/night4/night_report_checkpoints.csv`, iterations 0 and 250,008). If
  the endpoint cannot see a 60-unit difference, it is dead regardless of what it says about twins.
  This is the control the retired L3 probe failed: four cells agreed neatly while the instrument
  could not pass its own positive control.
- **(f) The field, named.** The test runs on the **checkpoint curve**, a different field from the
  250,000 hook, and its twin gaps are its own: at iteration 250,008 the curve gives
  `0′ − 0 = 12.1749` and `3′ − 3 = 7.6059`, against the hook's 12.7279 and 10.4309 (same file,
  recomputed by CC 2026-09-17 UTC). Every comparison in the criterion must be computed in the
  field the test uses; carrying the hook's numbers into a curve-based criterion is the same
  population error as §1, one level down.
  **And the range it is compared against must count individuals only.** In this field at
  iteration 250,008 `range(8) = 18.7403`, but `range(6)` — the six individuals — is
  **12.1922** — 1144.6362 (seed 1) to 1156.8285 (seed 4), and the maximum is seed 4, not the last
  column. The criterion compares against 12.1922. Read that way the twin gap is not comfortably
  inside the population: `0′ − 0` = 12.1749 is **99.86 %** of it, a difference of 0.017 against a
  read noise larger than that, and `3′ − 3` is 62.4 %. This is a stronger statement than §2's,
  and it sits in exactly the field the gate will read. Correction and recomputation: Ark,
  2026-09-17, re-verified by CC from `results/night4/night_report_checkpoints.csv`.
- **(g) The inherited fragility, stated.** The aggregate is the same 16 items over 6 scenes, two of
  which flip the order (§2), and crossing time inherits it. Not a blocker. If the test fails there
  is a second free branch: recompute the aggregate under alternative item weightings from the
  per-item tables already on disk — again no GPU, again with its own registration.

**(h)–(k) were raised in review by Ark on 2026-09-17, after this file was first committed.**
CC recommends all four and has re-verified the measurements behind (h) and (j); none of them is
accepted by Mike yet, and they are written here so that whoever drafts the registration reads
them in the place where they belong.

- **(h) "Iterations to cross" is undefined on a non-monotone curve, and the data already hold a
  counterexample.** Seed 5 reads 1188.8464 at iteration 86,412 and **1306.4735** at 90,012 — a
  spike 117 loss units above the whole field — and at 25,212 it reads 1213.5255, which is above
  its own untrained start of 1212.5467 (`results/night4/night_report_checkpoints.csv`; recomputed
  by CC 2026-09-17 UTC). Any level above roughly 1188 therefore needs a stated rule: first
  downward crossing, last crossing, or first level below which the curve stays. Without it the
  statistic depends on a convention chosen after the curves have been seen — which is the very
  failure (a) and (b) exist to prevent.
- **(i) The comparator in the gate is not size-matched, and the mismatch biases it towards
  passing.** Two (or with a third night, three) replicate pairs against **15** between-individual
  differences among six individuals: comparing maxima lets the larger family win by chance alone.
  A gate that can only pass is the same class of instrument as the retired L3 probe. The
  registration needs a named null — a permutation or sign test, or a comparison of distributions
  — not max against max.
- **(j) The positive control in (e) tests gross functioning, not resolution.** 63.7481 loss units
  is about five times the effect being measured (≈12), so the endpoint can pass (e) and still be
  blind at the scale that matters. The cheap addition: state the resolution **in loss units** —
  how much loss one 3,600-iteration grid step spans near the threshold — computed from the same
  file.
- **(k) Process, not statistics.** The registration is drafted by Zcode and would likely be read
  by Zcode. Given that this session's error class is "choice made after the look", the reading
  should be a script **committed before it is run**, run once, with its output recorded verbatim,
  and preferably executed by someone other than the author of the criterion.

## 5. What ADR-002 needs afterwards — not decided here

The condition as written ("show that a cheap evaluation of an individual is consistent with an
expensive one") is a **ranking** requirement, and the instrument does not carry it. Two candidate
forms, to be chosen after step 3 and written in the same commit as the verdict, so the repository
never holds two inconsistent statements:

- if the reachability endpoint survives — restate the condition around reachability;
- if it does not — restate it in the transferable form the USPEX practice actually supports: the
  cheap side may reject and may order provisionally, and every promoted individual is re-evaluated
  expensively before it is called better.

## 6. What stays in force

- **ADR-002 stands.** Its condition is not met, and the USPEX reading does not annul it.
- **(b) is read once, at the final N** — but N is chosen after step 3, not before.
- **The §7 replicate tolerance is still failed** (1.1104 % against < 1 %), and the rule has never
  been applied once at a registered N.
- **External blind review remains a mandatory gate.** This thread is its justification: three
  instruments, two errors inside one number, both found before a decision was taken on it.
- **The R2 finding stands reworded** as fragility to a zero clamp, not as vision dependence.
- **Measurement rules R1–R4 and checklist items 15–17** are unchanged.

## 7. Decisions waiting on Mike

1. The word to send the (c)4 registration to review, and then the word to read the data.
2. `N = 8` or `10` — after step 3.
3. Whether night 5 is the third replicate pair (§3 item 5 recommends it) or something else.
4. Whether the R2 text in `002`/`003` is edited at all, or left standing with the override one layer
   above it, as this repository's convention has it.
5. Whether ADR-002's condition is restated (§5), and in which of the two forms.
6. Road **C** — changing the population — is **covered by no document**: not by the review, not by
   this plan. It needs its own input, and nobody has computed one.

## 8. Boundaries of this file

- The order in §3 is a recommendation, not a decision. Mike approved writing it down.
- **No number here is new.** Each is cited to a committed record, and the ones CC recomputed — the
  two sds, the range, the twin gaps in the curve field, the learned gain, the grid step — are
  arithmetic over committed values, not new measurements.
- σ_rep rests on **two** replicate pairs, ±60 % by its author's own caveat. Everything in §2 that
  depends on it is direction, not magnitude.
- The reliability-ceiling argument (CC, 2026-09-17) is recorded in `backlog.md` as an unreviewed
  reading and is deliberately **not** used in this plan's reasoning: with a negative variance
  estimate no version of that model yields a number, and the qualitative form — the observation
  exceeds the instrument — is what §2 states instead.
- The version of the superseded local manual — USPEX **9.4.4 (25 June 2017)** rather than a
  damaged copy of 10.6 — was Zcode's recovery from the file's raw objects and has since been
  **independently reproduced** (Zcode, 2026-09-17, by a blind second pass with its own script and
  no answer supplied in its prompt): the title page carries `Version 9.4.4, June 25, 2017.`
  (object 356) and the running header `USPEX 9.4.4` appears in all 35 recoverable header objects,
  while that manual's own contents put §4.12 at printed page 54 — past the truncation. The script,
  its extracted fragments and a result file live at
  `sources/local/uspex/uspex-manual-truncated-recovery/`, which is **outside git history** under
  the same `.gitignore` rule as the PDFs, so the check is re-runnable on this machine and not from
  a fresh clone — moving the script itself into the tree would fix that and is worth one line of
  decision. CC's byte-level check, which found no `trailer`, no `/Info` and no readable XMP, is
  consistent with the recovery and independently confirms only that ordinary metadata does not
  survive in that file.
