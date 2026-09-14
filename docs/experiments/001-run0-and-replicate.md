# Experiment 001 — run 0 and its replicate

**Date:** 2026-09-14 · **Status:** run 0 and run 0′ complete, recorded below · **Substrate:** flyvis
1.2.0, connectome `fib25-fib19_v2.2.json`, extent 15, task `flow` on MPI-Sintel · **Written by:**
CC, from `docs/preregistration-cheap-vs-expensive.md` §3/§6/§7 and `results/night1/`.

**Observed** = read off a committed artefact, with its path. **Inferred** = a conclusion CC draws
from Observed numbers. **Reported** = someone else's statement, attributed.

## 1. Purpose

Run 0 (K = 1, Mike's decision 2026-09-13) is registered by
`docs/preregistration-cheap-vs-expensive.md` §6 to establish three things and no more: the price
of *expensive* on this card, one converged reference individual (seed 0, individual 1 of the
eventual N), and that the whole flow runs end to end on the GPU. Run 0 cannot speak to hypothesis
(a) or (b) — both need a second individual. Run 0′ is the §7 instrument-agreement control: seed 0
trained twice, non-deterministically, to measure the replicate difference the N runs' ranking will
have to rise above.

## 2. Setup

**Observed.** Model and task per pre-registration §2/§3 (unchanged). Seed mechanism: the run
script overrides `network.node_config.bias.seed=<seed>` (Hydra) and sets `random` / `numpy` /
`torch` seeds manually — stock flyvis seeds only the resting-potential initialisation (§2). Torch
determinism flags **off** (Mike, 2026-09-13 16:20 UTC), per the 3.77× cost measured the same day.
Tooling: `tools/night/run_individual.py` (the per-run hook, progress lines), `launch_wave.py`
(sequential, detached, replicate queued right after seed 0), `start_night.ps1` (dry-run, follow,
extent override) — at run time these lived in the session scratchpad, copied into this repository
as `tools/night/` in commit `08f34a0` (board:
[[THE-NIGHT-TOOLING-LIVES-IN-A-TEMPORARY-SCRATCHPAD]]). Launch: Mike's own PowerShell command,
production `llama-server` stopped first (board: [[THE-NIGHT-RUN-STARTS-ONLY-ON-MIKES-EXPLICIT-WORD]],
closed).

## 3. What ran

**Observed** (`results/night1/night_report.md`, `results/night1/wave_night1.json`).

| run | id | seed | started (UTC) | finished (UTC) | wall | iterations | exit | errors |
|---|---|---|---|---|---|---|---|---|
| run 0 | `9991/000` | 0 | 2026-09-13T18:40:31Z | 2026-09-13T22:40:56Z | 4:00:17 (14,417.6889 s) | 250,008 | ok | 0 |
| run 0′ | `9991/900` | 0 | 2026-09-13T22:40:59Z | 2026-09-14T02:39:51Z | 3:58:40 (14,319.9398 s) | 250,008 | ok | 0 |

Sequential, run 0′ launched automatically right after run 0 (`WAVE DONE 2/2 ok` at
2026-09-14T02:39:52Z, `wave_night1.json`). VRAM peak `torch.cuda.max_memory_allocated`
**1,426.0952 MiB**, identical for both runs. Artefacts: `results/night1/night_report.md`,
`night_report_checkpoints.csv`, `night1_9991-000.slim.json`, `rep_9991-900.slim.json`,
`wave_night1.json/.progress.log`; full (non-slim) per-run json/log/stdout live in
`connectome-seed-data/results/flow/9991/000/` and `.../900/` (h5 checkpoints, activity, loss).

## 4. Results

**Two-phase price** (`activity_penalty.stop_iter = 150000` removes the activity-penalty backward
pass after iteration 150,000): median 0.0644 s/iter over iterations 1–150,000, 0.0452 s/iter over
150,001–250,008 (run 0; run 0′ 0.0639 / 0.0451). 72 checkpoints each run. Source:
`results/night1/iter_wall_s_9991-000.csv.gz` / `iter_wall_s_9991-900.csv.gz` (per-iteration wall
times, committed derivatives of the full run jsons; recomputed medians match to printed
precision). Independent recomputation from `results/night1/wave_night1.progress.log` (Zcode,
100-iteration timestamps): 0.0653 / 0.0461 s/iter (run 0) — 1.5–2 % higher, because the log's
100-iteration stamps include hook/logging overhead.

**Rung table** (held-out loss, evaluation hook):

| iteration | run 0 | run 0′ | \|Δ\| | relative |
|---|---|---|---|---|
| 1,000 | 1208.9363 | 1208.9363 | 0.0000 | 0.0000 |
| 5,000 | 1207.7673 | 1207.7698 | 0.0025 | 0.0000 |
| 25,000 | 1191.7375 | 1192.0739 | 0.3365 | 2.8e-4 |
| 250,000 | 1146.1958 | 1158.9237 | 12.7279 | **1.1104 %** |

Replicate tolerance (§7, < 1 % at 250,000): **FAIL** at 1.1104 %; the three lower rungs are two to
four orders of magnitude below tolerance.

**Late-phase offset.** Over the 29 common checkpoints after iteration 150,000, run 0′ sits above
run 0 in **29 of 29**; mean (run 0′ − run 0) = **+12.64** (min 3.68, max 17.82); within-run
checkpoint standard deviation 6.02 (run 0) / 3.30 (run 0′). Divergence is visible from roughly
iteration 60,000; the two replicates settle on different plateaus, ≈ 1151.7 (run 0) vs ≈ 1164.3
(run 0′).

Late-phase replicate offset (29 checkpoints after 150,000): min +3.68, median +12.25, max +17.82,
mean +12.64; the pre-registered scalar for §7 is the hook value at 250,000 (12.7279). (Ark, chat
2026-09-14 05:12 UTC; recorded here, no rule changes.)

**Plateau facts (run 0).** Minimum held-out (checkpoint) loss **1141.0463 at iteration 219,612**;
relative change of held-out loss over the last 50,000 iterations (checkpoint near 200,000 → near
250,000, positive = rose) rose by **+0.11 %** (1147.5358 → 1148.8075); plateau: |change| < 0.2 %.

**Rung-vs-checkpoint jitter.** The evaluation-hook rung at iteration 250,000 (1146.1958) and the
checkpoint at iteration 250,008 (1148.8075) differ by **2.6117** over the 8 extra iterations;
training-loss standard deviation over the last 100 iterations ≈ 680 on a mean ≈ 1283, for scale —
the jitter is well inside iteration-to-iteration training noise. Source:
`results/night1/train_loss_last1000_9991-000.csv` (last-100 mean 1283.4386 / std 679.6031,
matches to printed precision).

Sources for this section: `results/night1/night_report.md`,
`results/night1/night_report_checkpoints.csv`, `results/night1/iter_wall_s_9991-000.csv.gz`,
`results/night1/iter_wall_s_9991-900.csv.gz`, `results/night1/train_loss_last1000_9991-000.csv`,
`results/night1/train_loss_last1000_9991-900.csv`, `results/night1/wave_night1.progress.log`.

## 5. Verdict against the pre-registration

The §7 replicate tolerance (< 1 % at the top rung) is **not met**: 1.1104 % ≥ 1 %. The three lower
rungs (1,000 / 5,000 / 25,000) are clean — |Δ| two to four orders of magnitude below the 250,000
figure. No rule in §3–§7 is changed by this record, per §7's own text: any change to the tolerance,
the ladder, or how the 250,000 rung is treated for (b) requires a new pre-registration written
*before* any N run, not an edit to this one after the result was seen.

§7's own escape clause applies: "a rung whose between-seed standard deviation does not exceed the
replicate difference is reported as *unmeasurable*, not as a failure of the surrogate." Whether the
250,000 rung is measurable for hypothesis (b) is therefore **not decided by this record alone** — it
depends on the between-seed standard deviation of held-out loss at 250,000 across the eventual N
individuals, which needs further seeds run to that iteration. The only between-seed spread
measured so far is at iteration 1,000, sd 0.52 across 3 seeds (the extent probe, 2026-09-13) — a
different population (1,000 iterations, not 250,000; the extent probe, not the N population) and
not a substitute.

## 6. What we learned that was not the goal

**Inferred.** The instrument floor of the expensive evaluation is ≈ 1.1 % relative, set by
trajectory divergence under non-deterministic training (determinism flags off, §7), not by
single-iteration jitter — the rung-vs-checkpoint gap over 8 iterations (§4) is two orders of
magnitude smaller than the seed-0 replicate gap over 250,000 iterations. Both day-time probes that
preceded run 0 (the GPU-price probe, the extent-5 probe) ran at most a few thousand iterations —
entirely inside phase 1 (before `activity_penalty.stop_iter = 150000`) — so neither measured the
phase-2 price or the late-phase divergence this record reports; the "≈ 4.40 h all-in" estimate in
pre-registration §3 was withdrawn there for the same reason.

## 7. Open decisions (Mike + reviewers)

1. **Instrument-floor route.** Proceed as registered — the top rung may come out *unmeasurable*
   for (b) rather than a surrogate failure — or write a new pre-registration for the expensive
   metric before the N runs (candidates: mean over plateau checkpoints, median of ≥ 2 replicates
   per seed).
2. **Floor N: 8 or 10** (`docs/preregistration-cheap-vs-expensive.md` §4, board:
   [[N-EQUALS-EIGHT-IS-BELOW-THE-FILES-OWN-MINIMUM]]) — unresolved before this record and
   unaffected by it.
3. **Top-k as a secondary hypothesis** (board:
   [[A-TRAINED-SURROGATE-IS-NOT-A-PREFIX-OF-THE-SAME-PROCESS]]) — unresolved before this record and
   unaffected by it.

## 8. Proposed next step (CC)

Run seeds 1 and 2 to 250,000 next night (tooling ready, `-NoReplicate`; see
`docs/next-session-plan.md`) to obtain the first between-seed distances at the plateau, compared
against the +12.64 / 1.11 % replicate offset above — the first direct input to the instrument-floor
decision in §7.
