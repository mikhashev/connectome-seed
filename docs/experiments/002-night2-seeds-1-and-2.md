# Experiment 002 — night 2, seeds 1 and 2

**Date:** 2026-09-15 · **Status:** both waves complete, recorded below · **Substrate:** flyvis
1.2.0, connectome `fib25-fib19_v2.2.json`, extent 15, task `flow` on MPI-Sintel · **Written by:**
CC's subagent on Sonnet, 2026-09-15, from `docs/experiments/001-run0-and-replicate.md` (format),
`results/night2/`, and the raw night jsons; verified by CC.

**Observed** = read off a committed artefact, with its path. **Inferred** = a conclusion drawn
from Observed numbers. **Reported** = someone else's statement, attributed.

## 1. What ran

**Observed** (`results/night2/wave_night2.json`, `wave_night2.launcher.log`,
`wave_night2b.json`, `wave_night2b.launcher.log`, `night2_9991-001.slim.json`,
`night2b_9991-002.slim.json`, `killed_9991-002.partial.json`).

| run | id | seed | tag | started (run json) | finished (run json) | total_train_wall_s | wall (launcher) | iterations | exit |
|---|---|---|---|---|---|---|---|---|---|
| seed 1 | `9991/001` | 1 | `night2` | 2026-09-14T19:12:34Z | 2026-09-14T23:14:59Z | 14532.8769 (4:02:12.8769) | 14548.8979 s (launcher `2026-09-14T19:12:31Z`→`23:15:00Z`) | 250,008 | ok |
| seed 2, 1st attempt | `9991/002` | 2 | `night2` | 2026-09-14T23:15:02Z | — (killed) | n/a | n/a | last progress-log iteration 12,700 at `2026-09-14T23:29:04Z` | `training` (interrupted) |
| seed 2, re-run | `9991/002` | 2 | `night2b` | 2026-09-15T01:13:49Z | 2026-09-15T05:12:17Z | 14296.6488 (3:58:16.6488) | 14311.9681 s (launcher `2026-09-15T01:13:46Z`→`05:12:18Z`) | 250,008 | ok |

Note: run-json `started_utc`/`finished_utc` (set inside `run_individual.py`, after process/CUDA
setup) run a few seconds later/earlier than the wave launcher's own `launched_utc`/`exited_utc`
(set by `launch_wave.py` around the subprocess) — the same few-second gap is present in night 1's
own wave json (`9991/000`: launcher `18:40:30Z`→`22:40:57Z` vs run json `18:40:31Z`→`22:40:56Z`),
so this is not new to night 2. The main table above and `docs/experiments/001-...md` both use the
run json's own fields as primary, for consistency.

**The reboot.** Seed 2's first attempt (wave `night2`, id `9991/002`) was killed by a Windows
Update planned restart (KB5129195) — stated by the orchestrator and by `docs/next-session-plan.md`
§2 ("killed at iteration 12,700 ... at 23:29:19Z"). The last line this session can read directly is
`wave_night2.progress.log`'s final entry for that job: `2026-09-14T23:29:04Z night2 9991/002 iter
12700/250000 ... vram 1426MiB` (also the last line of `night2_9991-002.log` /
`.stdout.log`, timestamped `2026-09-15 01:29:04,533` local); no line for iteration 12,800 exists,
consistent with a kill between the two. The partial run's own json (`killed_9991-002.partial.json`
here, copied from `night2_9991-002.json`) shows `"exit": "training"`, `"final_iteration": null`,
2 rung entries (1,000: 1209.7631; 5,000: 1206.9981) and 5 checkpoint entries (through iteration
10,812 — the json is rewritten only at rung/checkpoint events per `tools/night/night_report.py`'s
own docstring, so it lags the progress log's 12,700 by one checkpoint interval). Mike renamed the
partial output directory to `flow/9991/002_killed_by_reboot`; under §7's resume rule ("an
interrupted run is a failed run", `docs/next-session-plan.md` §5) it is excluded from N and from
the replicate. Seed 2 was then re-run from scratch as wave `night2b` (fresh id `9991/002`, no
`resume_count`).

**Two-phase price** (median s/iter; phase 1 = iterations 1,000–150,000, phase 2 =
150,001–250,008), computed by `tools/night/night_report.py`'s own `two_phase_price()` (pairwise
runs `night_report_1v0.md`, `night_report_2v0.md`) and cross-checked by
`results/night2/extract_night2.py`'s independent copy of the same function against
`iter_wall_s_9991-001.csv.gz` / `iter_wall_s_9991-002.csv.gz` (identical to printed precision):

| run | phase1 median s/iter | phase2 median s/iter | overall median s/iter |
|---|---|---|---|
| seed 1 | 0.0647 | 0.0459 | 0.0622 |
| seed 2 | 0.0636 | 0.0454 | 0.0611 |
| (seed 0, for reference) | 0.0644 | 0.0452 | 0.0614 |

72 checkpoints each completed run (seed 1, seed 2-rerun), same cadence as night 1 (`chkpt_every_epoch=300`, 12 iters/epoch ⇒ nominal 3,600-iteration spacing after the first two).

## 2. Rung table

**Observed** (rung values: orchestrator-supplied, verified against `night2_9991-001.slim.json` /
`night2b_9991-002.slim.json` `rung_metrics` and reproduced by `night_report_1v0.md` /
`night_report_2v0.md` / `night_report_2v1.md`'s own rung tables — all match to printed precision).

| iteration | seed 0 | seed 0′ | seed 1 | seed 2 | \|1−0\| | \|2−0\| | \|2−1\| | SD(0,1,2), n=3 | replicate \|0′−0\| | SD/replicate |
|---|---|---|---|---|---|---|---|---|---|---|
| 1,000 | 1208.9363 | 1208.9363 | 1208.0556 | 1209.7639 | 0.8807 | 0.8276 | 1.7083 | 0.8543 | 0.0000 | undefined (÷0) |
| 5,000 | 1207.7673 | 1207.7698 | 1206.7832 | 1207.0115 | 0.9841 | 0.7558 | 0.2283 | 0.5151 | 0.0025 | 206.03 |
| 25,000 | 1191.7375 | 1192.0739 | 1190.2235 | 1204.3618 | 1.5140 | 12.6243 | 14.1383 | 7.7627 | 0.3365 | 23.08 |
| 250,000 | 1146.1958 | 1158.9237 | 1145.3572 | 1148.8000 | 0.8386 | 2.6042 | 3.4428 | 1.7953 | 12.7279 | 0.14 |

SD is the sample standard deviation over {seed0, seed1, seed2} (n=3, ddof=1, i.e. 2 degrees of
freedom) — computed in this session with Python's `statistics.stdev` and matching the
orchestrator-supplied values exactly. "SD/replicate" is that SD divided by the run-0/run-0′
replicate difference at the same rung (`docs/experiments/001-run0-and-replicate.md` §4); at
1,000 the replicate difference is 0.0000 so the ratio is undefined rather than a very large
finite number.

Two things move in opposite directions across rungs: at 25,000 the between-seed spread (7.76) is
**about 23× the replicate floor** (0.34); at 250,000 the between-seed spread (1.80) is **about
0.14× the replicate floor** (12.73) — the ordering inverts between the 25,000 and 250,000 rungs.
(`docs/next-session-plan.md` names this
`[[THE-SPREAD-REPLICATE-RATIO-INVERTS-BETWEEN-C3-AND-THE-TOP-RUNG]]`; the same numbers appear
there, §2.)

## 3. Checkpoints

**Observed** (`results/night2/night_report_checkpoints.csv`, built by `extract_night2.py` from
the four runs' `checkpoint_metrics`; 72 common checkpoint iterations across seed 0, seed 0′, seed
1, seed 2 — the same 72 iterations each run, since checkpoint cadence is set by
`chkpt_every_epoch`/epoch length, not by seed).

**29 checkpoints after iteration 150,000** — mean / min / max of the per-checkpoint differences,
against the run-0/run-0′ late-phase replicate offset already on record (+12.64 mean, min +3.68,
max +17.82; `docs/experiments/001-run0-and-replicate.md` §4):

| diff | mean | min | max |
|---|---|---|---|
| seed1 − seed0 | −5.3848 | −18.9212 | +9.5105 |
| seed2 − seed0 | −3.5593 | −21.6855 | +8.0023 |
| seed2 − seed1 | +1.8255 | −12.2667 | +10.4559 |

All three of these signed means sit inside the replicate's own min/max band (+3.68 to +17.82) only
at the top of their range or not at all — seed1−seed0 and seed2−seed0 are *negative* on average
(seeds 1 and 2 finishing the last third of training slightly below seed 0, not above it as run 0′
did), while seed2−seed1 is positive and smaller in magnitude than the replicate mean.

**Plateau** (mean of the last 10 of the 72 common checkpoints) and **minimum checkpoint loss**
(over each seed's own full 72-checkpoint trajectory) per seed:

| seed | plateau (last-10 mean) | min checkpoint val_loss | at iteration |
|---|---|---|---|
| 0 | 1148.7081 | 1141.0463 | 219,612 |
| 0′ | 1162.7778 | 1156.0002 | 82,812 |
| 1 | 1142.1858 | 1139.7140 | 248,412 |
| 2 | 1146.8842 | 1137.8219 | 162,012 |

(Seed 0's plateau/min figures match `docs/experiments/001-run0-and-replicate.md` §4 to printed
precision: 1141.0463 at 219,612.)

## 4. Seed 2's 25,000 rung — spike or trajectory?

**Observed** (`night2b_9991-002.json`'s `checkpoint_metrics` and `train_loss_per_iter`, read
directly this session — not committed in full, since the slim json drops `train_loss_per_iter`;
the checkpoint values below are also in `night2b_9991-002.slim.json`).

Seed 2's three checkpoints bracketing the 25,000 rung (iterations 3,612 + k·3,600):

| iteration | checkpoint val_loss |
|---|---|
| 21,612 | 1205.1803 |
| 25,212 | 1205.9782 |
| 28,812 | 1200.7650 |

The rung's own evaluation-hook value at exactly iteration 25,000 is **1204.3618**
(`night2b_9991-002.slim.json` → `rung_metrics`).

Single-iteration training loss (`train_loss_per_iter`) in the window iterations 24,981–25,020
(the 40 iterations straddling 25,000): mean 1343.3914, population std 665.9857 (computed this
session); the value at iteration 25,000 itself is 1038.1786. A wider window, iterations
24,000–26,000 (2,000 iterations): mean 1299.0257, std 642.5379.

What the checkpoints show: 1204.3618 (the rung) is below both neighboring checkpoints (1205.1803
and 1205.9782) by about 0.8–1.6, and the checkpoint sequence 1205.18 → 1205.98 → 1200.77 is not
monotonic either — it rises slightly from 21,612 to 25,212 before falling to 28,812. The
single-iteration training loss at iteration 25,000 (1038.1786) sits inside the surrounding
window's mean ± 1 std band (1343.39 ± 665.99, i.e. roughly 677–2009) — actually below the mean by
about 0.46 std, not an outlier by that measure. No further characterization beyond these numbers.

## 5. §7 measurability clause, applied now (caveat: n=3, one shot only)

**Reported / quoted**, not decided here. `docs/preregistration-cheap-vs-expensive.md` §7's clause
(quoted in `docs/experiments/001-run0-and-replicate.md` §5): *"a rung whose between-seed standard
deviation does not exceed the replicate difference is reported as unmeasurable, not as a failure
of the surrogate."* §7 also states the clause applies once, at the registered N (8 or 10, still
undecided — `docs/next-session-plan.md` §1.3) — applying it now, at n=3 (2 degrees of freedom),
is explicitly a preview, not the registered application.

The SD/replicate figures from §2 above, repeated for this section's purpose:

| rung | SD (n=3) | replicate \|0′−0\| | SD/replicate |
|---|---|---|---|
| 1,000 | 0.8543 | 0.0000 | undefined |
| 5,000 | 0.5151 | 0.0025 | 206.03 |
| 25,000 | 7.7627 | 0.3365 | 23.08 |
| 250,000 | 1.7953 | 12.7279 | 0.14 |

`docs/next-session-plan.md` §3's branch wording, quoted verbatim:

> **(a) Top rung measurable** (between-seed sd at 250,000 exceeds the ~12.64 / 1.11 % replicate
> offset) → continue the population per the N rule (§4): nights 3–5, seeds 3 onward, to the
> chosen floor (8 or 10, decision 3 above).
>
> **(b) Not measurable** → a new pre-registration for the expensive metric is required before any
> further N run. Candidates to be reviewed, not decided here: the mean over the plateau
> checkpoints (run 0's plateau: 1141.0463 at iteration 219,612; rose by +0.11% over the last
> 50,000, |change| < 0.2%); the median of ≥ 2 replicates per seed; both cost extra wall-clock and
> neither is registered yet. The lower rungs (1,000 / 5,000 / 25,000) are clean under either
> branch and do not need this decision.

`docs/next-session-plan.md` §1 already notes, in its own words, that "the branch in §3 is now
decidable, the call itself still waits on Mike + reviewers" — this record does not make that call,
does not rank the two branches, and reports no ρ.

## 5a. Reviewers' recomputation, 2026-09-15 (Ark 05:35, Zcode 05:44; verified by CC)

Every number in this section was recomputed by CC from `results/night2/night_report_checkpoints.csv`
and matches the reviewers' figures; marked "verified by CC" below per item.

**1. Four end-of-run statistics** (verified by CC, `statistics.stdev`, ddof=1):

| statistic | SD(0,1,2), n=3 | replicate \|0′−0\| | SD/replicate |
|---|---|---|---|
| rung hook @250,000 | 1.7953 | 12.7279 | 0.141 |
| plateau (mean of last 10 checkpoints) | 3.3651 | 14.0697 | 0.239 |
| checkpoint @250,008 | 2.1635 | 12.1748 | 0.178 |
| minimum checkpoint over the run | 1.6203 | 14.9539 | 0.108 |

Per-seed values (seed 0 / 0′ / 1 / 2), verified by CC:

| statistic | seed 0 | seed 0′ | seed 1 | seed 2 |
|---|---|---|---|---|
| plateau | 1148.7081 | 1162.7778 | 1142.1858 | 1146.8842 |
| ckpt @250,008 | 1148.8075 | 1160.9823 | 1144.6362 | 1147.7179 |
| minimum | 1141.0463 | 1156.0002 | 1139.7140 | 1137.8219 |

**2. Orderings.** Best → worst among seeds 0, 1, 2 under each statistic, verified by CC: rung@250,000:
1 → 0 → 2; ckpt@250,008: 1 → 2 → 0; plateau: 1 → 2 → 0; minimum: 2 → 1 → 0. Three distinct orders
of four. **Ark's reading, Reported:** the gaps between seeds (0.7–6.5) are of the order of the
within-run late-checkpoint SD (6.02 seed 0, 3.30 seed 0′, from the 001 record), so "rank at the top
rung is noise" is his inference, not a registered verdict.

**3. Zcode's 95 % χ² confidence intervals for σ at n = 3 (2 df)**, verified by CC by hand
(σ·√(2/χ²₀.₉₇₅,₂) … σ·√(2/χ²₀.₀₂₅,₂) with χ² quantiles 7.378 and 0.0506): at 250,000
σ ∈ [0.93, 11.28] against replicate 12.73 — the upper bound is below the replicate, but a single
wide seed would flip it; at C3 σ ∈ [4.04, 48.8] — even the lower bound is 12× the replicate floor
0.3365. The sentence "SD/replicate = 0.14" in §2/§5 above must be read with this interval.

**4. Ark's reading of the replicate, Reported and verified by CC on the csv:** seed 0 and seed 0′
are identical at iteration 0 to all printed digits (1212.5555891990662 both) and diverge
afterwards (iteration 12: 8.7e-5; 3,612: 0.015; 21,612: 0.68; 82,812: 12.46; then +10 to +17 to the
end, mean +12.64 over the 29 late checkpoints) — so |0′−0| is a twin-trajectory divergence that
grows with iteration, not a sample from a stationary noise distribution. Consequences he draws
(Reported, not adopted here): the small replicate at C3 reflects how little divergence has
accumulated by 25,000, not a better instrument; and the §7 denominator is one realisation (n = 1),
not an estimate of σ. Zcode concurs (Reported).

**5. Ark's tension argument, Reported verbatim in substance:** if run-to-run σ ≈ 12.73/1.128 ≈ 11.3,
three independent seeds landing with SD 1.80 is ≈ 4 % luck; if σ ≈ 1.8, then 12.73 is a ≈ 7σ event;
both cannot hold in one Gaussian model. He names a bimodal end-state distribution as the hypothesis
that explains both, explicitly not asserted from four points.

**6. Ark's replicate-cost estimate, Reported with his own caveat** (σ_rep from one pair, ±60 %,
order of magnitude): replicates per individual r > (σ_rep/σ_between)² — rung@250k ≈ 40 (≈ 53 nights
at N = 8), plateau ≈ 14 (≈ 19 nights), minimum ≈ 67 (≈ 89 nights).

**7. Reviewers' proposed sequence, Reported, decision Mike:**

(i) now, free, from the 72 saved checkpoints of each run (Zcode verified on disk: all 72 in
`flow/9991/{000,900,001,002}/chkpts/`, 5 for the killed run): re-evaluate one checkpoint several
times and on a second held-out split (evaluation noise vs trajectory noise); weight-space distance
between seed 0 and seed 0′ at 250,000 (two basins vs steep landscape); (ii) night 3 = seeds 3 and
4, on the critical path of both branches; (iii) if (b) holds, night 4 = one replicate each of seeds
0 and 1 (distribution of the offset, seed-dependence, bimodality test).

Both reviewers: the two candidates in the plan §3 (plateau mean; median of ≥ 2 replicates) do not
survive these four runs — plateau gives 0.239 against its own replicate 14.07; the median is
meaningless if the end state is bimodal. Rule both ask to be written into the new
pre-registration verbatim: the statistic is chosen by the diagnostics, not by the table of ratios.

**8. Two wording corrections from Ark, applied here as notes:** "clean" at the lower rungs means
"the replicate has not yet diverged", not "differences are stable" — seed 2's C3 gap of 12.6
closed to 2.6 by 250,000, so for that individual C3 measured a transient, not quality; and §7 as
written compares an SD (an estimate of σ) with |Δ| (one realisation) — an explicit distinction for
any new pre-registration. One from Zcode: the record's §1 says the killed run had 5 checkpoint
entries — keep; note that CC's chat message said 4, the record is right.

**Second pass (Ark 05:52, Zcode 05:55)**

9. Twin divergence is one-sided late in training (Ark; verified by CC): over the 72 night-1
checkpoints B−A (seed 0′ − seed 0) changes sign in 0…147,612 (43 points, range −3.04 at 140,412 to
+15.09 at 104,412) and is positive at all 29 checkpoints after 150,000 (min +3.68 at 165,612,
median +12.25, max +17.82 at 219,612). Ark's reading, Reported: a sign-symmetric chaotic divergence
would wander both ways; a one-sided shift that holds for 99,000 iterations is the difference
between two end states, so 12.7279 is a distance between two ends of one seed, not an instrument
resolution — substituting it as the §7 threshold compares two quantities of the same kind. Zcode's
refinement (verified by CC): positivity consolidates before `stop_iter` = 150,000, not at it —
thirds of the window 25,000–147,612 (35 checkpoints) give mean D = +1.58 → +7.02 → +8.22, 12 of the
last 13 checkpoints before 150,000 are positive, last negative at 140,412 (−3.04), divergence
saturates ≈ 80,000 (where run 0′'s minimum 82,812 sits). Both agree: no sign change in the last
99,000 iterations is a property of the process, not of the sample; "penalty switch-off fixes the
sign" and "sign consolidates as divergence saturates" are different mechanisms, and the second does
not implicate `stop_iter`.

10. Two reporting paths for nearly one state (Ark; verified by CC): hook @250,000 vs checkpoint
@250,008 — seed 0: 1146.1958 vs 1148.8075 (+2.61); seed 0′: 1158.9237 vs 1160.9823 (+2.06); seed 1:
1145.3572 vs 1144.6362 (−0.72); seed 2: 1148.8000 vs 1147.7179 (−1.08). Signs differ across runs (no
constant offset between paths); magnitudes 0.7–2.6 are the order of the whole between-seed spread
at the top rung (1.80), while 8 iterations ≈ 0.5 s of training and the late tail moves ±5 per 3,600
iterations without trend (expected ≈ 0.2 over 8). Reported, as a question not a conclusion: either
the two reporting paths disagree more than 8 iterations explain, or the within-run loss jumps
enough that a single number is not an estimate. Consequence both reviewers adopt: diagnostic 1
becomes "run ONE saved checkpoint through both reporting paths and ask whether they agree", before
any evaluation-noise study; until then hook and checkpoint are two instruments.

11. The C3 ratio 23 rests on one transient (Ark; verified by CC): σ(0,1,2) at 25,000 = 7.7627 is
made almost entirely by seed 2 (+12.62 at 25,000, +9.5 at 28,812), which closed the gap fully by
250,000; without it σ(0,1) = 1.0706 and the ratio to the replicate 0.3365 is 3.2, not 23. Ark
explicitly does NOT propose σ(0,1) as a statistic (that would be choice by outcome); the point is
that 23 says nothing about the instrument — both rung numbers describe descent phase, not
resolution. Zcode concurs and withdraws "robust" for C3: the CI lower bound 4.04 shows the spread
is not n = 3 luck but not what it is.

12. What follows (both, Reported): the plan's candidates are closed in substance — any within-run
scalar inherits the run's offset, so averaging checkpoints does not reduce it (plateau ratio 0.239
worse than the hook's 0.141); what is needed is a variance decomposition, r replicates per seed,
estimating σ_within and σ_between separately; at r ≈ 40 for the top rung that is out of reach, so
the honest expected label for (b) at the top rung is "unanswerable by this instrument at the
affordable price", to be written as such, not as a failure. Zcode: his k ≈ 25–40 and Ark's r are the
same arithmetic.

13. Night-4 design revised (Ark, Zcode agrees): the 0′ offset arose within one wave, so everything
shared by a wave (GPU state, power, temperature, resident llama-server) is excluded by
construction; what remains is "property of the pair (sign random pair to pair)" vs "position effect
(first run in a wave better than the second)". One run separates them: a replicate of seed 1 placed
SECOND in a wave whose FIRST job is a new seed — high → position; near seed 1 → pair-random. Night
2's seed 2 ran solo in `night2b`, so it is no witness to position.

## 5b. Diagnostics from saved checkpoints, 2026-09-15 (Mike's word 06:22 «делай диагностики»; run by CC's subagent on Opus; verified by CC)

**Observed**, from `results/night2/diagnostics/` (`diag1_eval_paths.py`, `diag2_weight_distance.py`,
their README, and the JSON/CSV outputs listed there) — the reviewers' sequence item (i) from §5a.7.

**(a) Two reporting paths agree.** Hook-path evaluation of checkpoint 250,008 vs flyvis's own
stored checkpoint `val_loss`, four runs (`diag1a_paths.json`):

| run | label | hook-path value | stored checkpoint `val_loss` | hook − stored |
|---|---|---|---|---|
| 000 | seed 0 | 1148.8074 | 1148.8075 | −1.0e-4 |
| 900 | seed 0′ | 1160.9824 | 1160.9823 | +4.9e-5 |
| 001 | seed 1 | 1144.6363 | 1144.6362 | +4.1e-5 |
| 002 | seed 2 | 1147.7179 | 1147.7179 | +4.0e-5 |

All four differences sit inside a 1.5e-4 band. Consequence: the 0.7–2.6 gaps between hook@250,000
and checkpoint@250,008 recorded in §5a item 10 are weight movement over 8 iterations, not two
instruments — this resolves that item the first way. Checkpoint-index mapping (not guessed):
`chkpt_iter.h5` stores iteration−1 (`flyvis/solver.py:453,463`) while the CSV stores
`solver.iteration` (`night/run_individual.py:498`), so `chkpt_00071` ↔ 250,008.

**(b) Evaluation noise.** Seed 0, checkpoint 250,008: 5 evaluations in one process spread 2.48e-5
(`diag1b_noise_inprocess.json`); 3 evaluations in fresh processes spread 3.77e-5
(`diag1b_noise_proc1/2/3.json`); across those 8 evaluations plus the stored checkpoint value, max
deviation 6.72e-5 (5.9e-8 relative to the ~1148.8 loss value) — float-level, not zero. The diag1a
hook-path run for this same checkpoint (task `paths`, row (a) above) read 1148.8074, 1.03e-4 below
the stored value — the same order as this noise floor, and already counted in (a), not a ninth
independent noise draw.

**(c) Per-item breakdown at 250,008** (16 held-out items × 4 runs, `per_item_250008.csv`):

| item | seed 0 | seed 0′ | seed 1 | seed 2 | seed0′ − seed0 |
|---|---|---|---|---|---|
| ambush_2_split_00 | 4048.8452 | 4068.6584 | 3935.1770 | 4112.5483 | +19.8132 |
| ambush_2_split_01 | 4363.8145 | 4381.7363 | 4312.6338 | 4363.9736 | +17.9219 |
| ambush_2_split_02 | 4764.6211 | 4782.3843 | 4714.0996 | 4701.6055 | +17.7632 |
| bamboo_1_split_00 | 93.3649 | 92.4739 | 105.0628 | 95.6211 | −0.8910 |
| bamboo_1_split_01 | 79.3864 | 82.7176 | 103.0105 | 79.4038 | +3.3312 |
| bamboo_1_split_02 | 104.8982 | 111.8489 | 123.5876 | 106.5946 | +6.9507 |
| bandage_1_split_00 | 687.7188 | 708.2150 | 692.6054 | 679.2449 | +20.4962 |
| bandage_1_split_01 | 690.9063 | 721.4998 | 706.9354 | 675.3077 | +30.5935 |
| bandage_1_split_02 | 546.3441 | 586.8903 | 559.3323 | 539.7303 | +40.5461 |
| cave_4_split_00 | 1181.2325 | 1184.1031 | 1190.2057 | 1183.8409 | +2.8706 |
| market_2_split_00 | 679.7902 | 669.8835 | 678.2033 | 663.8284 | −9.9067 |
| market_2_split_01 | 445.0692 | 450.3483 | 446.2205 | 459.8250 | +5.2791 |
| market_2_split_02 | 208.0599 | 219.4831 | 230.7196 | 222.8501 | +11.4232 |
| mountain_1_split_00 | 183.4995 | 184.9997 | 184.6738 | 166.6170 | +1.5002 |
| mountain_1_split_01 | 101.5424 | 115.1892 | 121.1735 | 107.9500 | +13.6468 |
| mountain_1_split_02 | 201.8258 | 215.2858 | 210.5390 | 204.5459 | +13.4601 |

Mean of the last column = +12.1749 — the checkpoint-path replicate already on record (§5a item 4,
+12.64 by the hook path over the 29 late checkpoints). 14 of 16 rows are positive. `bandage_1`'s
three rows sum to +91.64, 47 % of the total +194.80 across all 16; `ambush_2`'s three rows sum to
+55.50, 28 %. Loss scale ranges from ≈ 80–125 (`bamboo_1`) to ≈ 3,900–4,800 (`ambush_2`). At 25,212
(`per_item_25212.csv`) the same column is two-sided and small: mean +0.0756, min −2.9945
(`bandage_1_split_01`), max +4.9414 (`ambush_2_split_00`), 8 of 16 rows positive.

**(d) Same-evaluator trajectory**, all 72 checkpoints of seeds 0 and 0′ (`diag1d_trajectory_summary.json`,
`hook_path_trajectory_0_vs_0prime.csv`): max |hook − stored| over the 144 evaluations = 8.39e-5.
(0′ − 0) by the hook path, over the 29 checkpoints after iteration 150,000: mean +12.6406, min
+3.6803, max +17.8152 — the stored-path figures already in §5a item 9 reproduce under independent
re-evaluation.

**(e) Weight-space distances** (Euclidean, float64, `weight_distance_at_iterations.csv`;
trainable set verified by `requires_grad` in `diag2_requires_grad.json`: core 734 =
`nodes_bias` 65 + `nodes_time_const` 65 + `edges_syn_strength` 604; decoder 7,427; `edges_sign` /
`edges_syn_count` fixed; BatchNorm buffers excluded):

| pair | iter | d(core) | d(decoder) | d(all) | d(all)/mean‖·‖ |
|---|---|---|---|---|---|
| (0,0′) | 250,008 | 3.8340 | 1.8041 | 4.2372 | 0.5196 |
| (0,1) | 250,008 | 4.0554 | 3.7337 | 5.5124 | 0.6932 |
| (0,2) | 250,008 | 5.5598 | 3.1405 | 6.3855 | 0.7788 |
| (1,2) | 250,008 | 3.5274 | 3.9577 | 5.3014 | 0.6581 |
| (0′,1) | 250,008 | 2.8923 | 3.7155 | 4.7085 | 0.5877 |
| (0′,2) | 250,008 | 3.7421 | 3.2396 | 4.9496 | 0.5993 |
| (0,0′) | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| (0,1) | 0 | 0.5566 | 0.0000 | 0.5566 | 0.1126 |
| (0,2) | 0 | 0.5384 | 0.0000 | 0.5384 | 0.1084 |
| (1,2) | 0 | 0.6072 | 0.0000 | 0.6072 | 0.1225 |
| (0′,1) | 0 | 0.5566 | 0.0000 | 0.5566 | 0.1126 |
| (0′,2) | 0 | 0.5384 | 0.0000 | 0.5384 | 0.1084 |

(0,0′) is the positive control: 0 at iteration 0 in every group. Its trajectory across the five
saved-checkpoint sample points: 0 → 0.4203 (25,212) → 2.9690 (82,812) → 3.9929 (151,212) → 4.2372
(250,008). Group breakdown of (0,0′) at 250,008
(`diag2_group_breakdown_0_vs_0prime_250008.json`): `nodes_bias` 3.3377 (62.1 % of squared
distance), `edges_syn_strength` 1.7996 (18.0 %), `decoder` 1.8041 (18.1 %), `nodes_time_const`
0.5658 (1.8 %).

**(f) What the numbers show, stated without mechanism.** The twin pair (0,0′) ends 0.52 of its own
mean parameter norm apart — about three-quarters of the 0.59–0.78 range separating different-seed
pairs at the same iteration — with a loss gap (§5a item 4, +12.64 by the hook path, +12.1749 by the
per-item mean here) that the same evaluator reproduces to ≈1e-4 and that is spread over 14 of 16
held-out items, not concentrated in one. I.e., the replicate difference is a difference between two
end states of the weights, not evaluation noise. This is the reading Ark's §5a item 9 predicted; it
is recorded here as Observed. The mechanism — two basins vs a steep landscape — is not decided by
these numbers.

**(g)** An incidental Observed fact for §2 of the pre-registration: at iteration 0, seeds 0, 1 and 2
differ **only** in `nodes_bias` (distance 0.5384–0.6072 across the three pairs); `nodes_time_const`,
`edges_syn_strength` and the whole decoder are bit-identical across seeds at iteration 0
(`diag2_group_breakdowns.json`: `dist: 0.0`, `share_of_squared_distance: 1.0` on `nodes_bias` for
every iteration-0 pair). Mechanism not investigated.

**(h) Provenance.** Scripts and README in `results/night2/diagnostics/`; interpreter the night venv
(Python 3.10.20, torch 2.9.1+cu128, flyvis 1.2.0); run dirs verified unchanged by a before/after
listing of all 396 files under `results/flow/9991/{000,900,001,002}` (`diff` empty, both after
diagnostic 1 and after diagnostic 2); evaluator = a fresh solver built in a scratch datamate root
via `recover_network`/`recover_decoder`, `solver.test(track_loss=False)`
(`flyvis/solver.py:543-552`, the only form of the call that writes nothing); per-item losses from a
copy of `flyvis/solver.py:474-556` returning per-item values instead of only their mean, which
agrees with the hook value to < 7e-5 in all eight cases it was cross-checked against.

## 6. Provenance

- `results/night2/extract_night2.py` — this session's script; builds the slim jsons, the two
  `iter_wall_s_*.csv.gz`, the two `train_loss_last1000_*.csv`, copies the wave json/launcher-log/
  progress-log pairs, copies+renames the killed partial json, and builds the combined 4-way
  `night_report_checkpoints.csv`. No slimming script existed in `tools/night/` or the night
  scratchpad before this session (`grep -rl slim` on both returned nothing) — the night-1 slim
  jsons were the same two-key drop (`iter_wall_s`, `train_loss_per_iter`), verified this session
  by exact-equality diff against `results/night1/night1_9991-000.slim.json`.
- `tools/night/night_report.py` — run unmodified, three times (`--a`/`--b` pairwise, its only
  supported form): `night_report_1v0.md`, `night_report_2v0.md`, `night_report_2v1.md` (plus their
  own `night_report_checkpoints_1v0.csv` / `_2v0.csv` / `_2v1.csv`).
- `results/night2/night_report.md` — this session's hand-built combination of the three pairwise
  reports plus the 4-way checkpoint table (documents why it isn't itself a `night_report.py`
  invocation).
- Interpreter: system `python` (3.12.10 this session; the night-run venv, 3.10.20, was not needed
  — `night_report.py` and the extraction script use only the standard library).
- Inputs read (not modified): raw run jsons in the night scratchpad
  (`night1_9991-000.json`, `night2_9991-001.json`, `night2_9991-002.json`,
  `night2b_9991-002.json`, and the four `wave_*`/`*.progress.log`/`*.launcher.log` files),
  `results/night1/night1_9991-000.slim.json`, `results/night1/rep_9991-900.slim.json`.
- Written by: CC's subagent on Sonnet, 2026-09-15. Verified by: CC.
