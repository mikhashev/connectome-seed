# Next-session plan

**Date:** 2026-09-14 · **Written for:** Mike and the reviewers (Ark, Johnny, Warren, Zcode) ·
**Context:** run 0 and run 0′ are complete; the §7 replicate tolerance (< 1 % at 250,000) was
missed at 1.1104 %. Full record: `docs/experiments/001-run0-and-replicate.md`. Tooling record:
`tools/night/README.md`.

## 1. Decisions Mike must give before anything runs

1. **Instrument-floor route** — proceed as registered (top rung may come out *unmeasurable* for
   hypothesis (b), per §7's own clause) vs. write a new pre-registration for the expensive metric
   before any N run. **Note 2026-09-15:** numbers in, decision pending — night 2's three-seed
   rung SDs vs the run 0/run 0′ replicate offset are recorded in §2 below and on the board
   ([[THE-SPREAD-REPLICATE-RATIO-INVERTS-BETWEEN-C3-AND-THE-TOP-RUNG]]); the branch in §3 is now
   decidable, the call itself still waits on Mike + reviewers.
2. ~~**Night 2 = seeds 1 and 2, sequential, to 250,000, no replicate** — yes/no.~~ Decided
   2026-09-15, Mike «вноси…»/«запустил»; launched 2026-09-14T19:12:31Z, `wave_night2`.
3. **Floor N: 8 or 10** (`docs/preregistration-cheap-vs-expensive.md` §4,
   [[N-EQUALS-EIGHT-IS-BELOW-THE-FILES-OWN-MINIMUM]]).
4. ~~**Top-k as a secondary hypothesis** — enters the pre-registration or not
   ([[A-TRAINED-SURROGATE-IS-NOT-A-PREFIX-OF-THE-SAME-PROCESS]]).~~ Decided 2026-09-15,
   Mike «ок давай впишем»; form in §4/§5 of the pre-registration.
5. ~~Who fixes the PNAS line numbers in `research/analysis-cheap-step.md`.~~ Done in `dbeb878`
   (Ark's own correction applied by CC; verified lines 848–851 and 851–856).
6. **(a) outcome reading** — stands as the rule reads it / relabelled uninformative by the
   calibration / floor re-registered — Mike + reviewers. Numbers: `docs/experiments/002-night2-seeds-1-and-2.md`
   §5g, pre-registration §5 (a) 2026-09-15 note. Board:
   [[THE-COMPOSITION-MARGIN-OVER-ITS-FLOOR-IS-SMALLER-THAN-A-NULL-SHIFTS-MEDIAN-DELTA]].
7. **Population for the next pre-registration** — seed-only or wider variation (Zcode 07:05,
   Ark 07:36) — Mike.

**Ark's proposal, 2026-09-15 10:00 (for Mike, not a change):** the four BLOCKED ON DECISION
entries — N = 8/10 ([[N-EQUALS-EIGHT-IS-BELOW-THE-FILES-OWN-MINIMUM]]); the (a) outcome reading
([[THE-COMPOSITION-MARGIN-OVER-ITS-FLOOR-IS-SMALLER-THAN-A-NULL-SHIFTS-MEDIAN-DELTA]]); the
1.11 % replicate ([[THE-REPLICATE-DIFFERS-BY-ONE-POINT-ONE-PERCENT-AT-THE-TOP-RUNG]]); and the
C3/250k inversion ([[THE-SPREAD-REPLICATE-RATIO-INVERTS-BETWEEN-C3-AND-THE-TOP-RUNG]]) — are one
decision under four headings: what to do with an instrument that does not resolve individuals at
the top rung. Three outcomes: accept the limit (position paper), change the population (road C, a
new registration), or take (a) as an independent hypothesis. Merging them is Mike's call.

Nothing below runs before 1–4 are answered; night 2 specifically waits on Mike's explicit word
(the standing rule, board: [[THE-NIGHT-RUN-STARTS-ONLY-ON-MIKES-EXPLICIT-WORD]]).

## 2. Night 2 — on Mike's word

Seeds 1 and 2 to 250,000, sequential, **no replicate**, determinism off, extent 15. At run 0's
price (h_run 4:00:17 + wall between runs), ≈ 8.0 h total for two runs.

Command. Until the venv is re-created outside the scratchpad (per `tools/night/README.md`), night 2 runs from the same scratchpad copy as night 1 — the scripts in `tools/night/` are byte-identical to it. This is what Mike types, one line, `-DryRun` first:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\mikha\AppData\Local\Temp\claude\c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx\63f3961a-96ce-4048-8338-72c162ea66f8\scratchpad\flyvis-probe\night\start_night.ps1" -Tag night2 -Seeds 1,2 -NoReplicate
```

(`-DryRun` first to confirm the command and ids before launching; ids will be `9991/001` and
`9991/002` — ensemble 9991 already holds `000` and `900`, which is fine, the ids differ.)

**What the morning report compares.** Between-seed distances at every rung (1,000 / 5,000 /
25,000 / 250,000) and at the 72 common checkpoints: |seed1 − seed0|, |seed2 − seed0|,
|seed2 − seed1|, against the replicate offset already on record — **+12.64 mean (min 3.68, max
17.82) / 1.1104 % at 250,000** (`docs/experiments/001-run0-and-replicate.md` §4). Decision rule,
already registered (§7): a rung whose between-seed standard deviation does not exceed the
replicate difference is *unmeasurable*, not a failed surrogate.

**Result 2026-09-15.** Both waves complete. Seed 1 (`9991/001`) EXIT rc=0, 250,008 iterations,
14,532.9 s. Seed 2's first attempt (`9991/002`) was killed at iteration 12,700 by a Windows
Update planned restart (KB5129195, see
[[WINDOWS-UPDATE-RESTARTS-INSIDE-THE-NIGHT-WINDOW-BECAUSE-ACTIVE-HOURS-END-AT-0600]]); the
partial directory was renamed to `flow/9991/002_killed_by_reboot` and excluded under §7's
resume rule (an interrupted run is a failed run). Seed 2 was re-run from scratch as wave
`night2b` (`9991/002`): started 2026-09-15T01:13:46Z, EXIT rc=0, 250,008 iterations, 14,296.6 s,
done 05:12:18Z. Mike, chat 05:19Z: «прогон завершен». Full record:
`docs/experiments/002-night2-seeds-1-and-2.md`, `results/night2/`.

Rung SD (seeds 0/1/2, n=3) against the run 0/run 0′ replicate offset:

| rung | SD (n=3) | replicate \|0′−0\| | SD/replicate |
|---|---|---|---|
| 1,000 | 0.8543 | 0.0000 | — |
| 5,000 | 0.5151 | 0.0025 | — |
| 25,000 (C3) | 7.7627 | 0.3365 | ≈ 23 |
| 250,000 | 1.7953 | 12.7279 | ≈ 0.14 |

n=3 gives an SD with 2 degrees of freedom; §7's measurability clause is applied once at the
registered N. These are distances only — no ρ, no ranks, no verdict on (b)/(b2) yet. Board:
[[NIGHT-2-RUNS-SEEDS-1-AND-2-ON-MIKES-WORD]] (closed) and
[[THE-SPREAD-REPLICATE-RATIO-INVERTS-BETWEEN-C3-AND-THE-TOP-RUNG]].

## 2a. Night 3 — pre-registered reading, written before launch

**Pre-registered reading of night 3 (Ark 08:23, Zcode 08:24; recorded before the launch,
2026-09-15):** seeds 3 and 4 run the registered script unchanged. Their ablation profiles
(protocol of 002 §5f, all 65 types, 16 items, clamp to 0) are computed post hoc from the saved
checkpoint 250,008. Reading rule, fixed now: if neither seed 3 nor seed 4 shows a single-type
dependence of the size seen in seed 2 (R2: +21,157, i.e. an order of magnitude above every other
type in that run and above the largest twin per-type discrepancy, max_T |Δ_T(0) − Δ_T(0′)| =
2863 at T2a), then the R2 finding of seed 2 remains a single observation and is not interpreted
as a property of individuals. A single-type dependence in seed 3 or 4 of that size would make it
a repeated observation, not yet a test. Row B (activity profiles) for seeds 3 and 4 is a preview
at n = 5–6 (critical ρ 0.90–1.00), never read as a test.

**Positive reading (Ark 08:28):** if seed 3 OR seed 4 shows one type whose excess exceeds 2863
(the largest twin per-type discrepancy), the R2 finding becomes a repeated observation, still
not a test.

**Exploratory axes for night 3 (Ark 10:25):** the registered reading is R2 in the causal profile
only; row-B activity on T5c/T5d and profile compression (sd, range) are recorded as exploratory,
no verdict; night 3's (3, 4) is the second same-wave pair — within-pair vs between-pair closeness
across the two same-wave pairs is the first free separation of individual from night.

**Result 2026-09-16.** Both jobs ran in one wave, start to end, no reboot. Seed 3 (`9991/003`)
EXIT rc=0, 250,008 iterations, 14,415.1 s (launcher wall); seed 4 (`9991/004`) EXIT rc=0,
250,008 iterations, 14,684.5 s. `WAVE DONE 2/2 ok` 2026-09-16T04:40:23Z. Mike, chat 04:46Z:
«Ночной прогон завершен». Full record: `docs/experiments/003-night3-seeds-3-and-4.md`,
`results/night3/`.

Rung SD at n=5 (seeds 0, 1, 2, 3, 4) against the run 0/run 0′ replicate offset, with the 95 % χ²
interval for σ at n=5 (4 degrees of freedom, χ²₀.₉₇₅,₄ = 11.143, χ²₀.₀₂₅,₄ = 0.4844):

| rung | SD (n=3) | SD (n=5) | 95 % CI for σ (n=5) | replicate \|0′−0\| | SD(n=5)/replicate |
|---|---|---|---|---|---|
| 1,000 | 0.8543 | 1.2698 | [0.7608, 3.6489] | 0.0000 | undefined (÷0) |
| 5,000 | 0.5151 | 0.8173 | [0.4897, 2.3486] | 0.0025 | 322.04 |
| 25,000 (C3) | 7.7627 | 8.3788 | [5.0201, 24.0774] | 0.3365 | 24.90 |
| 250,000 | 1.7953 | 3.5426 | [2.1225, 10.1801] | 12.7279 | 0.278 |

n=5 gives an SD with 4 degrees of freedom; §7's measurability clause is still applied only as a
preview (registered N — 8 or 10 — still undecided, decision 3 above). Direction is unchanged
from n=3: at 250,000 the CI upper bound (10.18) is further below the replicate (12.73) than the
n=3 upper bound was (11.29); at 25,000 the CI lower bound (5.02) stays well above the replicate
(0.34). These are distances only — no ρ, no ranks, no verdict on (b)/(b2) yet.

The second same-wave pair (seed 4 − seed 3, mean −3.51, min −23.43, max +11.59) is positive at
only 6 of 29 late checkpoints, against (seed 0′ − seed 0)'s 29/29 — the two same-wave pairs do
not repeat each other's sign, so a within-wave position effect predicting a positive
second-job offset does not hold on this pair alone (`docs/experiments/003-night3-seeds-3-and-4.md`
§3). The pre-registered ablation reading (R2-sized single-type dependence in seed 3 or seed 4)
and the row-B preview extension are evaluated in `results/night3/diagnostics/{ablation,rowB}/`,
pointers only — not resolved in this plan or in `003`.

**Reading outcome 2026-09-16 (ablation):** clause (iii) positive for both seeds but
non-discriminating (5/6 runs exceed 2863); clause (ii) unsatisfiable as written (no run, including
seed 2, reaches 10×); clause (i) not met in size; R2 itself does not repeat (+147 / +42);
one-type dominance repeats (3.6× / 8.0×). Verdict for Mike and the reviewers; the reading rule's
defect is recorded in 003 §6.

**Reading outcome 2026-09-16 (row B, n = 6 preview):** row B for seeds 3/4 is done
(`docs/experiments/003-night3-seeds-3-and-4.md` §6b). The twin trap holds on 1 − ρ, margin 0.056
against the nearest foreign pair (1, 3) — same as the ablation channel — and fails on Euclidean
distance for both channels. The same-wave pair (3, 4) ranks 14 of 15 on both channels: no wave
effect. The row-B channel shows no single-type dominance (top/second ratio 1.0–1.4× for all six
runs), while the ablation channel does (2.8–8.0× for seeds 2/3/4); the T5c signature present in
seeds 0/1/2 is absent in seeds 3/4. All of the above is preview/exploratory, not a verdict.

## 3. Branches after night 2

**2026-09-15:** the branch below is now decidable with the numbers in the Result paragraph
above — SD/replicate ≈ 0.14 at 250,000 (spread far smaller than the replicate offset) against
≈ 23 at C3 (spread far larger). The numbers point at (b), but the call is Mike's + reviewers',
not made here.

- **(a) Top rung measurable** (between-seed sd at 250,000 exceeds the ~12.64 / 1.11 % replicate
  offset) → continue the population per the N rule (§4): nights 3–5, seeds 3 onward, to the
  chosen floor (8 or 10, decision 3 above).
- **(b) Not measurable** → a new pre-registration for the expensive metric is required before any
  further N run. Candidates to be reviewed, not decided here: the mean over the plateau
  checkpoints (run 0's plateau: 1141.0463 at iteration 219,612; rose by +0.11 % over the last
  50,000, |change| < 0.2 %); the
  median of ≥ 2 replicates per seed; both cost extra wall-clock and neither is registered yet.
  The lower rungs (1,000 / 5,000 / 25,000) are clean under either branch and do not need this
  decision.

**Reviewers 2026-09-15 (Ark 05:35, Zcode 05:44):** sequence proposed — (i) now, free, from the 72
saved checkpoints already on disk: re-evaluate one checkpoint several times and on a second
held-out split (evaluation noise vs trajectory noise), plus weight-space distance between seed 0
and seed 0′ at 250,000 (two basins vs steep landscape); (ii) night 3 = seeds 3 and 4 (critical
path of both branches); (iii) if (b) holds, night 4 = one replicate each of seeds 0 and 1
(distribution of the offset, seed-dependence, bimodality test). Both reviewers judge neither
candidate above viable as registered: plateau mean's own SD/replicate is 0.239 (still far below
1), and the median of ≥ 2 replicates is meaningless if the end state is bimodal. Rule both ask
written into the new pre-registration verbatim: the statistic is chosen by the diagnostics, not by
the table of ratios. Full detail: `docs/experiments/002-night2-seeds-1-and-2.md` §5a. Decision
Mike.

**Second pass 2026-09-15 (Ark 05:52, Zcode 05:55):** diagnostic 1 above is revised — run one saved
checkpoint through both reporting paths (hook vs checkpoint) first, since the two paths disagree by
0.7–2.6 at the top rung with no constant offset, before any evaluation-noise study. The honest
expected label for branch (b) at the top rung is "unanswerable by this instrument at the affordable
price" (r ≈ 40 replicates needed to separate σ_within from σ_between), not a failure of the
surrogate. Night 4, if reached, should place a replicate of seed 1 SECOND in a wave whose FIRST job
is a new seed, to separate a pair-random sign from a within-wave position effect — night 2's seed 2
(solo in `night2b`) is no witness to position. Full detail:
`docs/experiments/002-night2-seeds-1-and-2.md` §5a items 9–13.

**Diagnostics done 2026-09-15 — see 002 §5b; the sequence's step (i) is complete, steps (ii) night 3
and (iii) night 4 wait on Mike.**

**Third pass 2026-09-15 (Ark 06:47):** whatever statistic the new pre-registration adopts, it must
carry the item list and the aggregation rule explicitly, not the words "held-out loss" — §5c item 1
shows the top-rung seed order changes when 3 of the 16 held-out items are dropped. Pending. Full
detail: `docs/experiments/002-night2-seeds-1-and-2.md` §5c.

**Zcode 07:05 — remarks and proposals, Reported, decisions Mike:** (i) hypothesis (a) composition
is unblocked and is the cheapest item in the queue: A = seed 0 and B = seed 1 are trained with all
checkpoints; the T2 splice (k = 26) is a weight edit plus evaluation, minutes of GPU with the
evaluator built by the diagnostics; the instrument floor is now computable (3 × 12.7279 = 38.18,
3.33 %) and the 5 % bound 57.31, band non-empty; the mandatory A←A self-splice is nearly free; per
ADR-002 composition is the project's existence condition, so while (b) sits in instrument noise,
(a) is the load-bearing hypothesis and needs no night; caveat: the splice effect will also be
judged mostly by ambush_2/bandage_1, so a per-item report beside the aggregate is mandatory; Zcode
offers to run it his side (his submodels, Ark reviewing) on Mike's word. (ii) Connectivity as in §4
with the A↔A control. (iii) drop-k yes with the pre-stated consequence. (iv) Night 3 = seeds 3, 4 —
Zcode recommends giving the word (after pausing updates): checkpoints are metric-agnostic and
population-agnostic, any N needs them, they push the CI to n = 5, the GPU idles otherwise; night 4
as agreed (new seed first, replicate of seed 1 second). Strategic question (Zcode): the next
pre-registration must choose the population; seeds differ by 65 biases plus data order and
converge by 250,000 into a band below the instrument floor, so the population was nearly
homogeneous by construction — "should variation stay seed-only" stands above "how to fix the
expensive metric"; §8 of the current pre-registration fences structural variation, the next one
may choose anew; Mike's decision, all numbers now on the table.

**Three channels of variation (Ark 08:23) and the bias-only variant (Zcode 08:24):** the twins
(0, 0′) differ in neither the bias seed nor the data-order seed — they isolate run
non-determinism (12.73). Different seeds differ in both 65 biases and data order at once; no
measurement so far (loss, profile, ablation) separates 'bet on R2' from 'saw a different frame
order'. If individuality is carried by the data order, the 'genome = 65 numbers' frame and the
plan of bias mutations fall with it. Cheapest separation (Zcode): a bias-only variant — seed only
the bias (bias.seed = 1, 2) with the data-order seed fixed at 0; one night, two runs; profiles
post hoc. If bias-only individuals differ in profile, the 65-number genome holds and road C
narrows to bias mutations; if not, individuality rides on data order. This belongs in the
population decision (decision 7), before any N run.

**2×2 refinement (Ark 08:28):** bias-only alone cannot separate 'bias insufficient but
necessary' from 'individuality rides on data order' — a null result on bias-only is consistent
with either. The second arm, order-only (bias seed fixed, data-order seed varied), is required
to complete the 2×2; two runs each, one night of four or two nights. CC's finding: `run_individual.py`
takes a single `--seed` that feeds both `network.node_config.bias.seed` (`:282`, verified
against `:334-335`) and the global RNGs, seeded twice (`:208-210` before the network is built,
`:623-625` again before `solver.train` for the data-order / augmentation stream) — so separating
the two seeds needs a second script argument, which is a change to the registered flow, not a
night-script edit, and waits on a new registration.

**Diagnostics-2 done 2026-09-15 (Mike 07:43).** Four more diagnostics ran from the saved
checkpoints, on Mike's word «делай что можно до ночного прогона» — nothing trained, run dirs
verified unchanged. One line each, full detail `docs/experiments/002-night2-seeds-1-and-2.md`
§5d–§5g: **connectivity** — the 0↔0′ linear path carries a barrier of 96.6 (variant 2) against
an endpoint gap of 12.7, no better connected than the 0→1 control (115.2 at the same α) (§5d).
**drop-k** — the top-rung order (1<2<0) survives drop-one (0.8125) but is only modal at drop-3
(0.5054), and the twin sign degrades at C3 (§5e). **ablation** — the twin trap passes on both
pre-declared metrics in all three item subsets, margin only 4 % on Euclid and reversed by a
post-hoc Pearson; the supported claim is rank-order agreement, not agreement on the largest
effects (§5f). **(a) composition** — the registered T2 splice reads "composes predictably",
0.40 above its floor, while a null shift of the same norm moves the loss more on the median
draw (46.07 vs 38.58) (§5g).

**Night 4 revised (Ark 08:23, Zcode 08:24):** the replicate must run FIRST in the wave, not
second — in night 1 the replicate 0′ ran second, so position in the wave and pair identity are
confounded (n = 1). Night 4 = replicate of seed 3 (3′) as the first job, then a new seed (5) as
the second job. Readings fixed now: (3, 3′) ≈ 0 at matched position → the +12.73 'floor' is a
position effect of the second run, and the comparison of between-seed σ (1.80) with the twin
offset (12.73) was made across unlike conditions — to be revisited BEFORE the new
pre-registration; (3, 3′) ≈ +12.7 at matched position → the offset belongs to the re-run itself,
not the position, and §7 needs a new rule for what a replicate difference is. Position in the
wave becomes an explicit field in every run json (Zcode; it exists in the wave logs, to be
carried into the json).

**Each metric brings its own measured floor; inheritance is forbidden** (Ark 08:23, Zcode 08:24):
12.73 is a property of the loss; ρ, row B, the profile each need their own P0/P1 and floor.
Bought twice on 2026-09-15: the (a) floor built from two trainings' divergence; the ablation
floor nearly reused for ρ.

## 4. Side tasks (board entry names)

- Row B activity profiles (65 per-type means + within-type spread) from the 72 saved checkpoints of seeds 0, 0′, 1, 2, with P0 (cross-process reproducibility), P1, P2 and the twin trap, Spearman ρ pre-fixed as the measure, all 16 items — Ark's proposal `docs/proposals/mi-axis-per-cell-type-design.md`; preview, not a test. **Done 2026-09-15**, Mike's word 09:56 «делай ряд B»; run by CC; twin trap PASS (margin 0.1968 over the nearest foreign pair, floor 0.0); results in `results/night2/diagnostics/rowB/`, written up at `docs/experiments/002-night2-seeds-1-and-2.md` §5i; board [[ROW-B-CELL-TYPE-ACTIVITY-PROFILES-RUN-AS-A-PREVIEW-AT-N-EQUALS-FIVE-OR-SIX]] closed.
- **[[THE-NIGHT-TOOLING-LIVES-IN-A-TEMPORARY-SCRATCHPAD]]** — environment out of the scratchpad:
  recipe now in `tools/night/README.md` (this commit); remaining step is to re-create the venv
  from that recipe outside the scratchpad.
- **[[FLYVIS-RESUME-AND-RECOVER-ARE-BROKEN-IN-1-2-0]]** — upstream issue for flyvis (recover /
  resume, five defects found by execution).
- **[[DATAMATE-UNLINKS-AN-OPEN-HDF5-FILE-AND-WINDOWS-REFUSES]]** — upstream issue for datamate
  (the close-before-unlink Windows patch, `io.py`).
- **[[EIGHT-PROCESSES-SHARE-THE-CARD-NO-FASTER-THAN-ONE]]** — CUDA-graph prototype against run
  0's trajectory, after night 2 (not before — run 0 is the control); same entry also records
  extent 5 not adopted (1.46×, below the ≥ 3× bar that would have moved the night) — no further
  action on that sub-item.
- **[[THIRTEEN-LINKS-POINT-INTO-A-DIRECTORY-THAT-WILL-NOT-BE-PUSHED]]** — the 13 `chat/` links
  before the repo opens.
- ~~Diagnostics from saved checkpoints~~ — **Done 2026-09-15**, on Mike's word 06:22 «делай
  диагностики». Result: the two reporting paths agree to ≈1e-4 (the 0.7–2.6 top-rung gaps are 8
  iterations of weight movement, not two instruments); the twin (0,0′) weight-space gap at 250,008
  is 4.2372 = 0.52 of its own mean parameter norm, about three-quarters of the 0.59–0.78 spread
  between different-seed pairs; the loss gap is spread over 14 of 16 held-out items, not
  concentrated in one. Full detail: `docs/experiments/002-night2-seeds-1-and-2.md` §5b.
- ~~Linear mode connectivity, seed 0 ↔ 0′, (0,1) as control~~ — **Done 2026-09-15**, design Ark
  06:52 / Zcode 07:05, on Mike's word 07:43 «делай что можно до ночного прогона». Result: the
  main path (0→0′) carries a barrier of 96.6 (variant 2, primary) against an endpoint gap of
  12.7 — 7.6× — and is no better connected than the 0→1 control (115.2 at the same α); the
  self-path is flat to ≈1e-4 under both variants; the design's own resolution criterion is not
  met, so all barriers are lower bounds. Full detail:
  `docs/experiments/002-night2-seeds-1-and-2.md` §5d.
- ~~Ranking robustness to item composition~~ — **Done 2026-09-15**, Ark 06:47, on Mike's word
  07:43. Result: the pre-stated consequence occurred — the top-rung order (1<2<0) survives
  drop-one (0.8125) but is only modal, not universal, at drop-3 (0.5054, alternative 1<0<2 at
  152/560); the twin sign degrades at C3. Consequence stands: the new pre-registration must
  carry the item list and the aggregation rule. Full detail:
  `docs/experiments/002-night2-seeds-1-and-2.md` §5e.
- ~~Cell-type ablation profile~~ — **Done 2026-09-15**, unregistered diagnostic, Ark 07:39 /
  Zcode 07:43, on Mike's word 07:43. Result: the twin trap passes on both pre-declared metrics
  (Euclidean, Spearman) in all three item subsets, but the Euclidean margin over (0′,1) is only
  4 % and a post-hoc Pearson reverses it — the supported claim is agreement in rank order of
  type importance (ρ 0.72 vs 0.35–0.48), not in the largest effects. Full detail:
  `docs/experiments/002-night2-seeds-1-and-2.md` §5f.
- ~~Hypothesis (a) composition package~~ — **Done 2026-09-15**, Zcode's bundle 07:43 with Ark's
  null-shift calibration, on Mike's word 07:43. Result: the registered T2 splice (B = seed 1 →
  A = seed 0) gives Δ = +38.58 (3.366 % / 3.358 %), read by the registered rule as "composes
  predictably for this pair", 0.40 above the floor — but a null-shift calibration of the same
  norm moves the loss more on the median draw (46.07 vs 38.58), and the reverse splice explodes
  (+2029). Reading open for Mike + reviewers, board
  [[THE-COMPOSITION-MARGIN-OVER-ITS-FLOOR-IS-SMALLER-THAN-A-NULL-SHIFTS-MEDIAN-DELTA]]. Full
  detail: `docs/experiments/002-night2-seeds-1-and-2.md` §5g.
- ~~A←0′ and A←2 splices (achievable null from real individuals; Ark 08:23, Zcode 08:24)~~ —
  **Done 2026-09-15.** Result: A←0′ Δ +13.98 (1.2171 % / 1.4477 %, norm 0.2973), A←2 Δ +10.02
  (0.8722 % / 1.1020 %, norm 0.3463) — both below the floor 38.18 by 3–4× and shorter in norm
  than the registered A←B (Δ +38.58 / +41.19, norm 0.3819). Full detail: 002 §5g.
- ~~max_T |Δ_T(0) − Δ_T(0′)| = 2863 (T2a), computed by CC from `ablation_profiles.csv`~~ —
  **Done 2026-09-15.** Result: seed 2's R2 excess (+21,157.5) is 7.4× the largest twin per-type
  discrepancy over all 65 types (2863.0, T2a); every other comparator (mean, R2's own twin gap
  of 220.6) gives a larger ratio. Written into 002 §5f.
- ~~The reverse-splice `per_item_mean_minus_hook = 0.0` anomaly~~ — **Resolved 2026-09-15.**
  Two fresh-process re-runs (both path orders) show the two evaluation paths differ by ~5e-4,
  not 0.0 — a coincidence of two independent float64 means, not code-path reuse or float32
  saturation. The +2029.004 (+177.262 % of L_B) figure stands, reproduced across three
  processes to ±4e-4. Full detail: 002 §5g.
- ROADMAP: Ark 08:23: formulations after night 3, since night 3 decides which of the three
  outcomes is written into Phase 2 first; Zcode concurs.
- Tool-hardening package (Ark 08:42/08:45; CC) — nine items, see 002 §5h; **extended 2026-09-15
  (Zcode 09:04, Ark 08:54/09:36) with items 14–17**: a scaled null drawn in the non-negative
  orthant with a separate time-constant sign control; failed invariants set
  `exit = "state_check_failed"` (`run_individual.py:635`) and `night_report.py` prints the error
  strings, not just their count (`:149`); an idempotence control of the evaluator (evaluate twice,
  compare result and state); preflight in `start_night.ps1` for a pending reboot and free VRAM —
  all on Mike's word «чини инструменты». Night 3 runs the current script unchanged.
  Consolidated as `docs/tool-hardening-package.md` (19 items, 2026-09-15); execution on Mike's
  word.
- ~~Research-repo start checklist (Ark 08:50)~~ — **Done 2026-09-15**, Mike's word 09:56 «пиши
  чек-лист». File: `docs/CHECKLIST-research-repo.md` (14 rules with incident addresses, English,
  dense style); linked from `README.md`; board
  [[RESEARCH-REPO-START-CHECKLIST-WRITTEN-ON-MIKES-WORD]] (closed).

## 5. What not to do

- No change to any rule or tolerance in `docs/preregistration-cheap-vs-expensive.md` outside a
  new pre-registration written before it takes effect.
- No resume of an interrupted run (§7: an interrupted run is a failed run, re-run from the same
  seed; `resume_count > 0` excludes a run from N and from the replicate).
- No concurrent runs (m = 1 measured; aggregate throughput saturates at ≈ 17.5 it/s regardless of
  process count — [[EIGHT-PROCESSES-SHARE-THE-CARD-NO-FASTER-THAN-ONE]]).
- No GPU probes while a night run is on (production `llama-server` stays down for the duration,
  same as night 1).
- Do not read row B as a test at N < 8.
