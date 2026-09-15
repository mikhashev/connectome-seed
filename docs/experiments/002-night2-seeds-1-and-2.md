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

## 5c. Third pass on the diagnostics (Ark 06:47; per-item decomposition)

1. Per-item pairwise, seed 1 vs seed 0 at 250,008 (verified by CC): seed 1 beats seed 0 on 4 of 16
   items (the three ambush_2 items and market_2_split_00) and loses on 12; the three ambush_2 items
   contribute −215.37 to the sum of (seed1 − seed0) (−13.46 on the 16-item mean), the other 13
   items +148.60 (+9.29); total −66.77 ≈ 16 × (1144.6362 − 1148.8075). Dropping the three ambush_2
   items, the order of the three seeds by the mean of the remaining 13 becomes 2 < 0 < 1 instead of
   1 < 2 < 0 (verified by CC: 13-item sums 5203.64 / 5352.27 / 5185.36 for seeds 0 / 1 / 2). Ark's
   reading, Reported: the quantity that ranks the individuals and the quantity that measures the
   instrument floor are the same handful of items (ambush_2 also carries 28.5 % of the twin gap);
   the "expensive ranking" at the top rung is ranking by who did better on the three darkest
   sequences, and the replicate says that number moves by ±12 between runs.

   CC's independent recompute of this item from `per_item_250008.csv` (full float precision,
   not the printed table): the 4-of-16 win/loss split, the four winning items, the ambush_2
   contribution (−215.3704, i.e. −215.37) and its 16-item-mean share (−13.4606, i.e. −13.46), and
   the three 13-item sums (5203.6383 / 5352.2694 / 5185.3598, i.e. 5203.64 / 5352.27 / 5185.36 and
   the resulting 2 < 0 < 1 order) all match exactly. Two sub-figures do not: CC gets the other-13
   sum as +148.6311 (+148.63, not +148.60) and the total as −66.7393 (−66.74, not −66.77); the
   aggregate cross-check 16 × (1144.6362 − 1148.8075) also gives −66.7408 (−66.74), agreeing with
   CC's direct sum rather than with the −66.77 above. Both values as given above (unchanged) and as
   recomputed are recorded; the discrepancy is ≈0.03–0.04, one order of magnitude below the −215.37
   ambush contribution, and does not change any ordering or sign in this item.

2. Relative view (verify from the CSV: per-item (seed0′ − seed0)/seed0 in %): Ark reports ambush_2
   items move 0.37–0.49 %, mountain_1_split_01 13.4 %, mountain_1_split_02 6.7 %, bamboo_1_split_02
   6.6 % — the twins diverge most in relative terms where the network solves well, and the absolute
   aggregate is dominated by items it does not solve (loss scales differ 60×, 79 vs 4,764). Ark's
   own caveat, Reported verbatim in substance: switching to a relative metric NOW would be a choice
   made after night-2 data exists; defensible only as a dated decision with a named reason
   (heteroscedasticity across items), never as pre-registered.

   CC's own recompute from `per_item_250008.csv`, (seed0′ − seed0)/seed0 × 100: ambush_2_split_00
   +0.4894 %, ambush_2_split_01 +0.4107 %, ambush_2_split_02 +0.3728 % (range 0.37–0.49 %, matches);
   mountain_1_split_01 +13.4395 % (matches 13.4 %); mountain_1_split_02 +6.6691 % (matches 6.7 %);
   bamboo_1_split_02 +6.6262 % (matches 6.6 %). All four match Ark's figures to the stated
   precision; no discrepancy found.

3. Weight-space, Ark's reframing (verified by CC from `weight_distance_at_iterations.csv` and
   `diag2_group_breakdowns.json`): relative within-group distance for the twins at 250,008 —
   nodes_bias 0.70, nodes_time_const 0.71, edges_syn_strength 0.77, decoder 0.29; for different-seed
   pairs the decoder is 0.62 (e.g. (0,1): 3.7337 / 6.0257). So the twin divergence is spread evenly
   over the core while pairs of different seeds differ mainly in the decoder — and the twins,
   closer in the decoder, are farther apart in loss (12.18 vs 2.16 between-seed by checkpoint,
   ratio 5.6). Ark: the "62 % of squared distance in nodes_bias" figure in §5b is a share of the
   square and is biased toward the large-norm group; the relative measure is the fairer one.
   Recorded as such; §5b's number stays as written.

   CC re-read `diag2_group_breakdowns.json` key `0_vs_0prime_250008` directly: `dist_over_mean_norm`
   is 0.6996 (nodes_bias), 0.7078 (nodes_time_const), 0.7746 (edges_syn_strength), 0.2938 (decoder)
   — matches 0.70 / 0.71 / 0.77 / 0.29 above. `weight_distance_at_iterations.csv` row `(0,1)` at
   250,008 gives `reln_decoder` 0.6196 with `d_decoder` 3.7337274807766705 /
   `meannorm_decoder` 6.025711254447206 (3.7337/6.0257 = 0.6196) — matches the 0.62 and the
   3.7337/6.0257 figures above exactly.

4. Limits Ark names (Reported): n = 3 seeds, n = 1 pair; between-seed differences per item up to
   177 that cancel in the aggregate — real cancellation vs a centring artefact of three seeds
   cannot be separated, which is why item 1 is built on pairwise counts; two basins vs steep
   landscape still open (distance, no curvature); one fly line, one rung, 16 items, one split; the
   seed's only channel at start is the 65 nodes_bias values out of 8,161 trainable — a measurement,
   not a fact about flyvis, mechanism unexamined.

5. Ark's two proposals, Reported, decision Mike: (i) linear mode connectivity between seed 0 and
   0′ — interpolate the weights between the two end states and evaluate the loss along the path
   (tens of evaluator runs, seconds of GPU), with (0,1) as control: loss rising mid-path → two
   basins; loss along the path not above the ends → one basin and 12.7 is an offset on a flat
   plateau. This is the direct answer to the registered "chaos or flat landscape" question, from
   files already on disk. (ii) Ranking robustness to item composition — drop-one and drop-random-k
   over the 16 items; if the order flips when 3 of 16 are removed, the new pre-registration must
   carry the item list and the aggregation rule, not the words "held-out loss". (iii) The rule
   again: do not change the metric because it gives a nicer ratio; a relative-per-item metric
   would "fix" the ratio, and that is exactly the temptation.

6. CC's answer to Ark's question (verified by CC, `torch.load` on `chkpt_00071` of all four runs):
   each checkpoint holds `network` (nodes_bias 65, nodes_time_const 65, edges_syn_strength 604
   trainable, plus the fixed edges_sign and edges_syn_count), `decoder/flow` (7,444 elements =
   7,427 trainable + 17 BatchNorm buffers: running_mean, running_var, num_batches_tracked), `optim`
   and `activity_optim` (Adam state), `iteration` (stored as iteration − 1), `dt`, `val_loss`.
   Interpolation over all 8,161 trainable parameters is therefore possible from disk; how to treat
   the BatchNorm buffers along the path (interpolate, or take one end's) must be decided and
   stated, since it affects the loss.

**Zcode 07:05 (verified by CC):** per-item decomposition recomputed and confirmed (4/16, −215.37,
+148.63, order 2 < 0 < 1 without ambush_2; twins 14/16, 47 % / 28 %); the CI and the per-item view
are complementary (the interval says σ is not sampling luck; the decomposition says what it is made
of); the seed also drives data order (run_individual.py:208-210, 623-625).

## 5d. Linear mode connectivity 0↔0′ (design Ark 06:52 / Zcode 07:05; run by CC's subagent on Opus; verified by CC)

**Design as run.** Variant 2 (primary): interpolate the 8,161 trainable weights linearly,
θ(α) = (1−α)θ_A + α·θ_B, and recompute the 17 BatchNorm buffers by a forward pass over the 51
training items (13 batches, `IndexSampler`, batch_size 4, drop_last False), augmentation off,
`momentum = None` (cumulative average, buffers reset first), `t_pre = 0.5` (the training value).
Variant 1: weights and the 17 BatchNorm buffers both interpolated linearly (a path in
stored-parameter space). Variant 3 (buffers from one end) was not run, per the design. Four
paths: self (0→0), main (0→0′), control (0→1), extra (0′→1, unregistered context). 21 points,
α = 0, 0.05, …, 1.0 on every path; the primary (main) path refined to a 0.025 step (41 points
total).

**Controls.** The self-path (0→0) is flat to ≈1e-4 under both variants (barrier 8.7e-5 variant
1, 6.0e-5 variant 2, largest inter-point change ≤1.2e-4). Variant-1 endpoints reproduce the
stored checkpoint `val_loss` to ≤7.9e-5 at every path's every endpoint. Variant-2 endpoints do
**not**: they land −3.3996 (seed 0), −1.5498 (seed 0′), −0.6592 (seed 1) below stored —
investigated before the grid was reported: the stored buffers are flyvis's own momentum-0.1 EMA
over 250,008 augmented training batches (effectively the last ~10 augmented batches), while the
recompute is the mean over one clean, unaugmented pass of all 51 training items — two different
estimators of the same statistic. Turning augmentation on for the recompute moves the offset to
−2.12/−0.58/−1.06 over three draws (spread 1.54, roughly two-thirds of −3.40). The offset is
identical at every α on a given path (the self-path proves it) and is therefore a constant of
the estimator, not entering the barrier (barrier = max along path − max(endpoints), within one
variant).

**Summary (path × variant):**

| path | variant | L(0) | L(1) | max | α at max | barrier |
|---|---|---|---|---|---|---|
| main (0→0′) | 2 | 1145.4078 | 1159.4325 | 1256.0185 | 0.10 | 96.5859 |
| main (0→0′) | 1 | 1148.8074 | 1160.9824 | 1535.0339 | 0.60 | 374.0515 |
| control (0→1) | 2 | 1145.4079 | 1143.9771 | 1260.6187 | 0.10 | 115.2108 |
| control (0→1) | 1 | 1148.8074 | 1144.6362 | 2936.7040 | 0.85 | 1787.8966 |
| extra (0′→1) | 2 | 1159.4325 | 1143.9770 | 1294.6970 | 0.05 | 135.2645 |
| extra (0′→1) | 1 | 1160.9824 | 1144.6362 | 1218.9421 | 0.05 | 57.9597 |
| self (0→0) | 2 | — | — | — | — | 6.0e-5 |
| self (0→0) | 1 | — | — | — | — | 8.7e-5 |

**Per-item barrier, main path, variant 2 (all 16 positive):** ambush_2 184.17 / 173.47 / 176.89;
bamboo_1 102.36 / 114.47 / 112.60; bandage_1 103.31 / 94.67 / 81.29; cave_4 47.12; market_2
139.03 / 97.26 / 70.50; mountain_1 93.46 / 91.95 / 89.98.

**Resolution caveat.** The design's own criterion — a resolution fine enough that a barrier of
order 12.7 cannot hide between points — is **not met**: the largest inter-point change is 63–82
on the main path (both variants) and 1,496.88 on the control path (variant 1, between α = 0.80
and 0.85), so a feature of size 12.7 can hide between points on all six non-self path×variant
combinations, and the reported barriers are lower bounds. Refining the primary path from 0.05 to
0.025 steps (41 points) left both barriers unchanged (96.5859 v2, 374.0515 v1, same α_max).

**Statement without mechanism.** The twins are not connected by a low-loss linear path: the
main-path barrier (96.6, variant 2) is 7.6× the endpoint difference itself (12.7), and the path
is not better connected than a different-seed pair — the control (0→1) carries a barrier of
115.2 at the same α. The self-path (≈1e-4 under both variants) shows that neither the
interpolation nor the BatchNorm recompute manufactures a barrier on its own. No mechanism
(basins vs. resolution) is decided by these numbers.

**Files:** `results/night2/diagnostics/connectivity/{connectivity.py, connectivity_profiles.csv,
connectivity_summary.json, README.md}`.

## 5e. Ranking robustness to item composition, drop-k (Ark 06:47; CC's subagent on Sonnet; verified by CC)

**Observed** (`results/night2/diagnostics/dropk/dropk_results.json`, `dropk_summary.md`).
Full-set order over the 16 held-out items: **1 < 2 < 0** at iteration 250,008 (the primary
rung's endpoint) and **1 < 0 < 2** at iteration 25,212 (C3 context) — the two rungs disagree even
before any item is dropped.

**Exhaustive drop-k, rung 250,008.** Fraction of subsets that reproduce the full-set order
exactly: k = 1 **0.8125** (13/16 subsets), k = 2 **0.6750** (81/120), k = 3 **0.5054**
(283/560); the most common alternative order at k = 3 is **1 < 0 < 2** (152 of 560 subsets).

**Scene-level drops (rung 250,008).** Dropping `ambush_2` entirely flips the order to
**2 < 0 < 1**; dropping `bandage_1` flips it to **1 < 0 < 2**; the other four scene drops
(`bamboo_1`, `cave_4`, `market_2`, `mountain_1`) leave the order unchanged at 1 < 2 < 0.

**Twin sign** (sign of seed0′ − seed0 over the remaining items, fraction positive over all
subsets of a given k): preserved in **100 %** of subsets for k = 1, 2 and 3 at rung 250,008; at
rung 25,212 it degrades to **0.875 / 0.700 / 0.643** for k = 1 / 2 / 3.

**Per-item pairwise wins** (16 items, no aggregation, rung 250,008): seed 1 beats seed 0 on
**4/16** items, seed 2 beats seed 0 on **6/16**, seed 1 beats seed 2 on **3/16**.

Ark's pre-stated consequence (`docs/experiments/002-night2-seeds-1-and-2.md` §5c item 5) has
occurred: the order survives drop-one but is only modal, not universal, at drop-3 (0.5054, just
over half). Consequence, as pre-registered: any new pre-registration for the expensive metric
must carry the item list and the aggregation rule explicitly, not the words "held-out loss".

**Files:** `results/night2/diagnostics/dropk/`.

**2026-09-15 — Basis note (Ark 08:45; CC):** drop-k and every per-item quantity in this record
are computed on checkpoint 250,008 by the per-item path; the registered rung statistic is the
training-time hook at iteration 250,000, which has no per-item decomposition and no saved state
(checkpoints are at 246,412 and 250,008). The two states order the seeds differently — hook
@250,000: 1 < 0 < 2; checkpoint @250,008: 1 < 2 < 0 — eight iterations apart. Consequence (Ark): a
new pre-registration that carries an item list and an aggregation rule adopts the per-item path on
a saved state as its instrument; it is not a refinement of the registered hook. On the same state
the two paths agree to 1e-5 (§5b).

## 5f. Cell-type ablation profiles (Ark 07:39, Zcode 07:43; unregistered diagnostic; CC's subagent on Opus; verified by CC)

**Status: unregistered diagnostic**, not a test of hypothesis (b)/(b2) and not a rung.

**The intervention**, fixed before any profile was run: `Network.register_state_hook`
(`flyvis/network/network.py:444-469`) masks `state.nodes.activity` to zero for one cell type at
every Euler step and at the initial state. Zero is the rectification point at both places
activity leaves the node — the synaptic current `weight * relu(source.activity)`
(`dynamics.py:214`) and the decoder's own rectification (`task/decoder.py:288`) — so
clamp-to-zero means "this cell type is silent" rather than "frozen at rest". Rule fixed before
running: clamp to 0.0, all 65 types, every integration step.

**Controls.** P0 (the evaluator reproduces the stored checkpoint `val_loss`): all four runs
inside **2.4e-5** of stored. P1 (ablating an empty set is a no-op): aggregate shift **≤2.9e-5**
across the four runs — passes as a no-op at the measurement's own precision, but is **not
bit-identical** (the masked path allocates a fresh contiguous tensor, changing which reduction
kernels run), recorded as measured rather than assumed. P2 (the instrument can see something):
silencing the 8 photoreceptor types R1–R8 costs **+58.4 / +47.0 / +64.9 / +30,626** for seeds
0 / 0′ / 1 / 2; silencing the 34 decoder-input types costs **+208.6 / +181.4 / +258.9 / +187.6**
— orders of magnitude above the noise floor on every run.

**Repeatability** (post-hoc, added after the profiles existed, `ablation_repeatability.json`):
all 260 single-type profiles recomputed in a fresh process repeat to **≤6.1e-4** per Δ_T,
Spearman **ρ = 1.0000** on every run — six to seven orders of magnitude below the smallest
between-run distance, so the between-run structure below is not measurement noise.

**The twin-trap distances** (Euclidean | 1−ρ, three item subsets):

| pair | 16 items | 13 items | 10 items |
|---|---|---|---|
| **(0, 0′)** | **4798.0 \| 0.285** | **5336.2 \| 0.297** | **5622.8 \| 0.317** |
| (0, 1) | 6059.4 \| 0.524 | 6888.9 \| 0.546 | 6951.7 \| 0.624 |
| (0, 2) | 22254.3 \| 0.647 | 23092.0 \| 0.605 | 22981.5 \| 0.584 |
| (1, 2) | 22627.2 \| 0.560 | 23606.1 \| 0.643 | 23558.0 \| 0.613 |
| (0′, 1) | 5006.7 \| 0.559 | 5880.7 \| 0.614 | 6048.5 \| 0.595 |
| (0′, 2) | 21632.8 \| 0.557 | 22379.7 \| 0.554 | 22202.0 \| 0.543 |

**Twin-trap verdict.** Passed on both pre-declared metrics (Euclidean and Spearman) in all three
item subsets — d(0,0′) is the smallest of the six pairs, every time. But the Euclidean margin
over (0′,1) is only 4 % (4798.0 vs 5006.7 on 16 items), and a post-hoc Pearson r (not
pre-declared) reverses it: (0′,1) r = 0.588 vs the twins' r = 0.351. The supported claim is
therefore the weaker one — **the rank order of the 65 types' importance is more similar between
twins than between different-seed pairs** (ρ 0.72 vs 0.35–0.48) — not that the twins agree on
their largest effects: seed 0's top type is Tm5c at +2,616.8, and the same type in seed 0′ is
+34.6.

**Sign agreement** (same sign of Δ_T across all four runs): 44 of 65 types on 16 items, 51 of 65
on 13 items, 43 of 65 on 10 items.

**R2 alone silenced:** +459 / +680 / **−1.0** / **+21,157** for seeds 0 / 0′ / 1 / 2 — seed 2's
end state collapses without photoreceptor type R2 while its un-ablated loss (1147.72) is
indistinguishable from the others.

**Mi4** is top-3 by |Δ_T| in all four runs.

**Twin per-type discrepancy (Ark 08:23, Zcode 08:24; computed by CC from
`ablation_profiles.csv`, `delta_16`):** max_T |Δ_T(0) − Δ_T(0′)| = **2863.0** (T2a), then Tm5c
**2582.2**, Mi4 **1943.0**, L5 **1616.3**, R8 **933.5**, T2 **505.9**. Seed 2's R2 excess
(**+21,157.5**; seeds 0 / 0′ / 1: **+459.2** / **+679.8** / **−1.0**) is **7.4×** the largest
twin discrepancy over all 65 types — a ratio against the most generous null available from
these data (the maximum over types); any other comparison (mean, or R2's own twin difference of
220.6) gives a larger ratio (Ark 08:28).

**Caveat.** One configuration, two twins, one comparison — no null distribution under which to
judge how surprising the twin margin is.

**Files:** `results/night2/diagnostics/ablation/`.

**2026-09-15 — Noise band for the sign claim (Ark 08:45; computed by CC from
`ablation_profiles.csv`, `delta_16`):** repeatability of a per-type Δ_T in a fresh process is
≤ 6.1e-4 (§5f), so the noise band is 2e-3. Types inside it: exactly one, Mi11, in all four runs
(Δ ≈ 0.000; the ablation does not touch it). Types with |Δ_T| < 1: 8 / 5 / 6 / 8 per run (seeds 0
/ 0′ / 1 / 2); < 10: 20 / 20 / 18 / 18. Of the 44 types whose sign agrees across all four runs, 19
have min |Δ_T| < 10 in at least one run (Am, C3, L3, L4, Mi10, Mi15, Mi9, R6, T1, T4a, …): the sign
agreement is not a coin flip at the noise level, but 19 of the 44 are small effects. Path noise
normalised to the loss (Ark): hook 0.022 ppm, per-item 0.52–0.85 ppm, ≈ 40×.

## 5g. Composition (a): registered splice T2 B→A with instrument control and null-shift calibration (Zcode 07:43 bundle, Ark's calibration; CC's subagent on Opus; verified by CC)

**Module identification** (`results/night2/diagnostics/splice_a/t2_module_indices.json`): cell
type T2 = type index 32; `nodes_bias[32]`, `nodes_time_const[32]`, and 24 `edges_syn_strength`
slots (flat indices listed in the file); the source-type set matches §2 of the pre-registration
exactly; **k = 26**. Ordering from `network.py:167,199` and `initialization.py:345-356,
496-515`.

**Reference.** L_A (unmodified seed 0, checkpoint 250,008) = **1148.807409** (stored checkpoint
`val_loss` 1148.807485). Self-splice A←A (the registered instrument control): Δ = **+1.38e-5** —
a no-op.

**Calibration** (Ark's null-shift, not part of the registered test; written
**2026-09-15T07:54:06Z**, before the registered splice was evaluated at **07:55:37Z**): r =
‖T2_B − T2_A‖ = **0.38185**. 20 isotropic random directions of the same norm r were drawn and
evaluated: **4 diverge** (two `inf`, one 5.29e18, one 3.41e11); the **16 finite** |Δ| values
range **10.70 … 69.55**, mean **44.44**, median **46.07**, and **10 of the 16** sit above the
floor 38.18 (14 of 20 counting the divergent draws as above-floor). The two real-direction
reference shifts: −v (A shifted away from B) gives Δ = **+61.60**; +2v gives Δ = **+53.49**. The
isotropic null in raw parameter space is not free of artefact: it sends 4–12 of the 24
synapse-strength slots negative on a given draw — values training's own clamp could never reach
— recorded as a property of this null, not corrected for.

**The registered splice, T2_A ← T2_B:** L = **1187.387355**, Δ = **+38.579946**, **3.3583 %** of
L_A (1148.8074), **3.3659 %** of **1146.1958** (§5(a)'s literal basis). Reading it on the basis
§5 names literally — 1146.1958, floor 38.18, 5 % bound 57.31 — **38.18 < 38.58 < 57.31**: the
registered rule reads **"composes predictably for this pair"**, margin **0.40** above the floor.
On the same-weights basis (L_A itself; floor 38.269, 5 % bound 57.440): same category, margin
**0.311**.

**Per-item Δ** (registered splice, vs the same-process A baseline): ambush_2 +28.73 / +55.88 /
+79.53; bamboo_1 −9.17 / −18.40 / −16.76; bandage_1 +106.42 / +118.25 / +114.31; cave_4 +17.88;
market_2 +46.79 / +31.56 / +11.94; mountain_1 −22.79 / +18.38 / +54.72; three items improve.

**Outside the registered test.** Reverse splice A→B (T2_B ← T2_A): L_B 1144.6362 →
**3173.6401**, Δ = **+2029.00** (**+177.3 %**) — the module does not compose the other
direction. B←B self-splice is a no-op (Δ ≈ 2.5e-5).

**Statement.** The registered category is recorded as the pre-registration's rule reads it —
"composes predictably for this pair" — but the calibration sitting beside it shows a
meaningless isotropic shift of the same norm moves the loss *more* on the median draw (46.07)
than the registered splice does (38.58), and the reverse direction explodes. Whether the (a)
outcome stands as read, is relabelled uninformative, or the floor itself needs re-registration
from the operation's own null is a decision for Mike and the reviewers, not made here.

**Files:** `results/night2/diagnostics/splice_a/`.

### Recheck of the reverse splice and the 0.0 (Ark 08:23/08:28, Zcode 08:24; run by CC's subagent on Opus; verified by CC)

The code finding: `stage_extra` (`splice_a.py:481-516`) computes nothing itself; every value
comes from `evaluate()` (`:169-182`), which runs `hook_eval` (`:172`) and `per_item_eval`
(`:174`) as two separate forward passes, with `per_item_mean` at `:179` taken over the second
pass; both paths use the same arithmetic (per-batch `.item()`, `np.mean`, float64). Fresh
re-runs in two processes, both orders: B←A hook **3173.6404418945312** / **3173.6400451660156**,
per-item mean **3173.639938354492** / **3173.6404724121094**, mean − hook **−5.04e-4** /
**+4.27e-4**; a third per-item pass in the same process changes **14 of 16** items by
**≤ 2.7e-3**; the float64 sum equals `math.fsum`, so the earlier 0.0 was a coincidence of two
independent means, not code-path reuse and not float32 saturation. Standing: **+2029.004 ± 4e-4**
across three processes (**+177.262 %** of L_B); the per-item decomposition stands within the
~1e-3 wobble. Ark's caveat recorded: the claim "loss is not a function of shift size" does not
rest on this number — it rests on the weight-space inversion (twins 0.52 at loss gap 12.7 vs
0.66–0.78 at 1.80) and the orthogonal-direction signature.

### Achievable null from real modules (Ark 08:23, Zcode 08:24; unregistered, no categories)

Same-process baseline L_A = **1148.8074293**. A←A (control): Δ **+7.68e-5**. A←0′ (twin's T2,
run 900): Δ **+13.9816**, **1.2171 %** of L_A / **1.4477 %** of 1146.1958, transplant norm
**0.2973**. A←2 (run 002): Δ **+10.0196**, **0.8722 %** / **1.1020 %**, norm **0.3463**. The
registered A←B, read the same two ways: Δ vs L_A **+38.5799** (**3.3583 %** of L_A); Δ vs
1146.1958 **+41.1916** (**3.5937 %** of 1146.1958) — these are the file's two distinct Δ
conventions (`extra3_achievable_null.json`'s footnote), stated exactly as it states them, not a
discrepancy. Both achievable transplants lie below the floor 38.18 by 3–4× and are shorter in
norm than the registered one.

Per-item columns for A←0′ and A←2 from `extra_per_item.csv` (16 values each, Δ vs the
same-process A baseline): ambush_2 A←0′ +0.04/+8.18/+21.93, A←2 +20.95/+5.28/+21.65; bamboo_1
A←0′ −8.49/−17.03/−16.61, A←2 +0.01/+2.12/+3.18; bandage_1 A←0′ +61.18/+67.78/+56.67, A←2
−11.30/−14.27/−11.99; cave_4 A←0′ +7.77, A←2 +6.23; market_2 A←0′ +13.49/+14.48/+1.05, A←2
+14.77/+8.74/+4.06; mountain_1 A←0′ −21.33/+1.41/+33.18, A←2 +53.78/+55.60/+1.52.

Three numbers side by side — isotropic null median 46.07 / real-module transplants 10–14 /
registered 38.58 — recorded without interpretation; the reading of (a)'s status remains decision
6. Note: an A←1 evaluation in the same process as the other three is running (Ark 08:28) and
will be appended as `extra4_same_process.json`.

**2026-09-15 — Reviewer's reading of the null (Ark 08:45, Reported):** the three achievable
transplants are not monotone in norm (0.297 → +13.98, 0.346 → +10.02, 0.382 → +38.58), so no
'effect from norm' model exists even among achievable transplants, and a population null cannot be
built from n = 3; the isotropic null is wrong not because it is high but because it samples a
region the trained network does not occupy; the (a) verdict therefore meets the same wall as (b): a
population is needed. Recorded, not adopted; decision 6 stands.

### Clamp censoring of the null calibration (Zcode 09:04; quantified by CC's subagent on Opus; verified by CC)

`Network.forward()` calls `self.clamp()` on every pass (`flyvis/network/network.py:527`); `clamp()`
applies `param.data.clamp_(0)` **in place** to every `non_negative`-configured, `requires_grad`
parameter (`:490-496`) — only `edges_syn_strength` carries `clamp_config = non_negative`;
`nodes_bias` and `nodes_time_const` are unclamped. The "training only" claim in
`splice_a.py:232-236` and the diagnostics README is **wrong**; verified directly (−0.5 written to a
synapse slot reads back 0.0 after one evaluation). So every calibration draw was evaluated
**censored at zero**. All 20 draws were regenerated bitwise-identical from seeds 0…19 (max abs diff
0.0); each drew 4–12 negative synapse slots (mean 7.9, median 8.0 of 24), 9 of 20 also a negative
(unclamped) `nodes_time_const`; pre-clamp norm 0.38185 for every draw; **post-clamp effective norm
min 0.2198, mean 0.2985, median 0.2964, max 0.3676** — 78.2 % of r survived on average. The two
real-direction reference shifts, recomputed the same way: −v 0.38185 → 0.32325 (84.7 % survived);
+2v 0.76371 → 0.58365 (76.4 %). None of the transplants actually written — registered splice A←B,
self-splice A←A, reverse splice B←A, and the achievable-null transplants A←0′/A←2 — carried a
negative value anywhere among their 26 slots (module minima: A 0.0 at T5d→T2, B 0.0 at T5b→T2, 0′
4.106e-05, 2 1.117e-05); **clamp was a no-op on every measured splice**, so the headline numbers of
this section stand unchanged. The four divergent draws (seeds 4, 9, 17, 18) are not distinguished
from the 16 kept by censoring (mean 7.0 vs 8.125 negative slots — divergent drew *fewer*),
post-clamp norm (0.3098 vs 0.2956), or time-constant sign (1 of 4 negative vs 8 of 16) — the
divergence is unlocalised by these data. Reading (Zcode, Reported): the null shifts were smaller
perturbations than declared and still moved the loss more than the transplant on the median draw,
so the calibration's conclusion survives and strengthens; Ark's "region the network does not
occupy" phrasing is corrected to "censored to an achievable region." Provenance note (Zcode):
`splice_a.py` on disk (mtime 2026-09-15T07:58:14Z) postdates the calibration (07:54:06Z) and the
splice (07:55:37Z) — a per-item stage was added afterward — so the byte-exact script that produced
the registered splice value is not on disk; night-1 derivative artefacts came from an uncommitted
interactive step, night-2's from a script with an equality check.

**Files:** `results/night2/diagnostics/splice_a/extra5_clamp_censoring.json`.

## 5h. Code audit of the diagnostics (Mike's question 08:40; Ark 08:42/08:45; CC's Explore agent on Sonnet; verified by CC)

(i) `hook_eval` (`diag1_eval_paths.py:151-173`) is a copy of the run-time hook path and reproduces
the stored val_loss to 1e-4 — the anchor of all four diagnostics; (ii) neither `hook_eval` nor
`per_item_eval` draws from any RNG during the loop (IndexSampler `flyvis/task/tasks.py:105,108`;
augmentation off disables `hex.py:320`; dropout off in eval); the RNG save/restore in `hook_eval`
(`:159-160, 168-171`) is defensive; the scheduler is no-op in `hook_eval` (`:161`) and real in
`per_item_eval` (`:182`, `solver.py:504`) and the paths agree to 1e-5, so the scheduler does not
affect the loss; the shared noise source is `cudnn.deterministic = False` (`:92-93`); (iii)
calibration and the registered splice use the same `evaluate()` (`splice_a.py:169-182`, called at
`:309, :319, :341` and `:425, :428`), functions imported from `diag1_eval_paths` (`:58-65`); (iv)
hard-coded constants in `splice_a.py:73-86` (`PREREG_SOURCES`, `K = 26`, `FLOOR_REL`,
`BASIS_PREREG`, `FLOOR_ABS_PREREG`, `BOUND_ABS_PREREG`, `STORED_LA`) are never checked against the
pre-registration document (cited only in a docstring, `:4`); the only live check is
`PREREG_SOURCES` against the source-type set computed from the network (`:127-141, :193-195`,
`assert len == K` at `:239`); the T2 index and the held-out list are computed live (`:135`;
`diag1_eval_paths.py:204-206`); (v) `run_individual.py:550-558` records seven post-evaluation
invariants (`lr_unchanged`, `pen_lr_unchanged`, `dt_unchanged`, `scheduler_iter_unchanged`,
`back_in_train_mode`, `was_in_train_mode_before`, `dataset_augment_restored`); none of the six
diagnostics scripts records any of them; what they do assert (table): diag1 — dt vs checkpoint,
checkpoint count, 0/0′ iteration alignment; splice_a — reproduction of the stored value to 1e-3
(assert), self-splice bitwise (recorded, not asserted); ablation — clamp = 0, hook state,
`_HOOK_SEEN` single-variable check (assert), P0/P1 (recorded, not asserted); connectivity — key
sets, dt (assert), self-path and (0,1) controls (recorded); diag2 — counts; dropk — no solver.
(vi) the isotropic null draw `u = rng.standard_normal(K); u /= ‖u‖; u *= r` is documented in the
code with the non-negativity caveat but registered nowhere, and it decides the (a) reading. (vii)
`evaluate()` computes both paths and never compares them; the bit-identical 0.0 was found by hand a
day later.

**Tool-hardening package, proposed (Ark 08:42/08:45, CC), on Mike's word, none of it recomputes
recorded numbers:** the seven invariants into `hook_eval` and every evaluation json;
`assert |hook − per_item_mean| < tol` with tol from the measured 0.85 ppm × loss × 3;
`--check-constants` reading §2/§5 from the document; module grouping recomputed from the
connectome beside `PREREG_SOURCES`; a per-slot scaled null beside the isotropic one; P0/P1/self-path
as asserts with thresholds in `ablation.py`/`connectivity.py`; the 250,008 basis note above. Also
Ark's seven-line research-repo start checklist with incident addresses, to be filed as
`docs/CHECKLIST-research-repo.md` on Mike's word.

### Bit-identity test on the reverse-splice state (Ark 08:54 ulp argument; run by CC's subagent on Opus; `extra6_bit_identity_test.json`)

Two fresh processes, hook and per-item interleaved 5+5 on the reverse-splice state (B = seed 1
with T2 from A = seed 0) and on baseline B, each preceded by a direct clamp probe. Process 1
(pid 42188): 9 of 10 values distinct on the reverse state, 9 of 10 on baseline; process 2
(pid 37260): 10 of 10 and 10 of 10. Spreads: reverse hook-path 1.98e-4 / 3.66e-4
(process 1/2), reverse per-item-path 2.75e-4 / 7.02e-4; baseline spreads correspondingly
smaller. Determinism flags identical across both processes (`cudnn.deterministic` False,
`cudnn.benchmark` False, `torch.are_deterministic_algorithms_enabled()` False,
`cudnn.allow_tf32` True, `matmul.allow_tf32` False, `float32_matmul_precision` "highest",
cuDNN 91002, CUDA 12.8, torch 2.9.1+cu128, one sm_12.0 device). **Conclusion: candidate (B)** —
within a process the two paths are not bit-deterministic. Correction to the ulp argument: values
lie on a lattice of step 2⁻¹⁶ = 1.52588e-05 on the reverse-splice state (2⁻²¹ = 4.768e-07 on
baseline), i.e. the resolution is set by float32 accumulation upstream, not the float64 ulp
(4.55e-13); the whole observed spread is only 25–46 lattice steps on the reverse state, so the
probability of an exact equality between two independent values is of order 1/40, not ~1e-9.
Exact equalities were directly observed: 2 of the 180 within-process unordered pairs (process 1:
one hook = one per-item mean on the reverse state at 3173.6402893066406; process 1: two per-item
repeats equal on baseline at 1144.636215209961), and pooling both processes, 4 of 190 pairs on the
reverse state (2.1 %, 3 of the 100 cross-process pairs) and 1 of 190 on baseline. The 07:56
equality is recorded as **a lattice coincidence with a measured rate ≈ 1–2 %, mechanism named**
(the coarse float32-derived lattice, not float64 rounding) — not as "chance float accumulation."

### Night-tooling audit (Mike 09:35; Zcode 09:36, Ark 09:36; verified by CC at the lines)

Zcode's eight confirmed properties: seeding with a bias-seed assert; the hook fires exactly at the
registered rungs (`solver_iteration_at_hook` = rung − 1); validation via `solver.test` with
augmentation off, batch 1, 16 items; waves run strictly sequentially via `pr.wait()`, no retries;
a refusal on an existing run directory, no resume used; checkpoints loaded strict in the
diagnostics; determinism left off by `start_night.ps1`, recorded honestly. His two notes: no
preflight for a pending reboot or free VRAM; `start_night.ps1` is the only safe entry point, since
bare `launch_wave.py` defaults to concurrent jobs.

Ark's two findings, verified by CC at the lines: (i) `run_individual.py:572` appends a failed
invariant set to `errors` and logs it, but `rec["exit"] = "ok"` is set unconditionally at `:635`
and the return code follows it (`return 0 if rec["exit"] == "ok" else 1` at `:673`) — **the
witness records but cannot veto**; `night_report.py:149` prints only `errors: {n}`, the count.
(ii) `night_report.py` writes checkpoint CSVs through `r4()` (`:60-64`, a fixed-4-decimal /
`"n/a"` formatter), so night-1's `results/night1/night_report_checkpoints.csv` (e.g.
`1212.5556`) is quantised at 1e-4 and any claim at 1e-5 is impossible from it; night-2's four-way
`results/night2/night_report_checkpoints.csv` was written by `extract_night2.py` with full floats
(`1212.5555891990662`) and is what this session's diagnostics used. (iii) The registered rung
hook fires at k = 250,000 while flyvis's checkpoint grid ends at 250,008 — two moments eight
iterations apart, neither declared in advance; this is the mechanism behind the hook-vs-checkpoint
gaps and order flips already noted in §5b/§5e — the training ran 8 iterations past the registered
250,000. (iv) None of the seven invariants checks that network parameters are unchanged by an
evaluation; harmless in the night run (clamp is idempotent there) but the class is unwitnessed —
an idempotence control (evaluate twice, compare result and state) is proposed as a universal
check.

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
