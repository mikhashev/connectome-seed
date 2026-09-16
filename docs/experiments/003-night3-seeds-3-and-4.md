# Experiment 003 — night 3, seeds 3 and 4

**Date:** 2026-09-16 · **Status:** both waves complete, recorded below · **Substrate:** flyvis
1.2.0, connectome `fib25-fib19_v2.2.json`, extent 15, task `flow` on MPI-Sintel · **Written by:**
CC's subagent on Sonnet, 2026-09-16, from `docs/experiments/002-night2-seeds-1-and-2.md` (format),
`results/night3/`, and the raw night jsons; verified by CC.

**Observed** = read off a committed artefact, with its path. **Inferred** = a conclusion drawn
from Observed numbers. **Reported** = someone else's statement, attributed.

No ρ, no ranks, no verdict on (b)/(b2) is made in this record.

## 1. What ran

**Observed** (`results/night3/wave_night3.json`, `wave_night3.launcher.log`,
`night3_9991-003.slim.json`, `night3_9991-004.slim.json`).

| run | id | seed | tag | started (run json) | finished (run json) | total_train_wall_s | wall (launcher) | iterations | exit |
|---|---|---|---|---|---|---|---|---|---|
| seed 3 | `9991/003` | 3 | `night3` | 2026-09-15T20:35:26Z | 2026-09-16T00:35:37Z | 14399.5953 (3:59:59.5953) | 14415.1 s (launcher `2026-09-15T20:35:23Z`→`00:35:38Z`) | 250,008 | ok |
| seed 4 | `9991/004` | 4 | `night3` | 2026-09-16T00:35:40Z | 2026-09-16T04:40:22Z | 14671.0791 (4:04:31.0791) | 14684.5 s (launcher `2026-09-16T00:35:38Z`→`04:40:23Z`) | 250,008 | ok |

Both jobs ran in **one wave, start to end, no interruption**: `WAVE START tag=night3` at
`2026-09-15T20:35:23Z`, `WAVE DONE 2/2 ok` at `2026-09-16T04:40:23Z`. Unlike night 2 (seed 2's
first attempt killed mid-run by a Windows Update reboot, re-run as `night2b`), night 3 needed no
re-run: no `killed_*.partial.json`, only one wave-file triple
(`wave_night3.json`/`.launcher.log`/`.progress.log`). This is the **second same-wave pair**,
after (seed 0, seed 0′) in night 1 — seed 2 in night 2 ran solo in `night2b` and is no witness
to within-wave position, so (seed 3, seed 4) is the first pair since night 1 that can speak to
it at all (`docs/next-session-plan.md` §2a).

The run-json `started_utc`/`finished_utc` vs the launcher's own `launched_utc`/`exited_utc` carry
the same few-second gap already noted in nights 1–2 (set at different points in the process
lifecycle); this record uses the run json's own fields as primary, for consistency with 001/002.

Rebuild note: no reboot occurred in the machine's uptime record spanning this wave (last reboot
2026-09-15 06:31 local, well before `WAVE START` 20:35:23Z); VRAM held steady at 1426.1 MiB;
errors = 0 for both runs; 72 checkpoints each.

**Two-phase price** (median s/iter; phase 1 = iterations 1,000–150,000, phase 2 =
150,001–250,008), computed independently by `results/night3/extract_night3.py` from
`iter_wall_s_9991-003.csv.gz` / `iter_wall_s_9991-004.csv.gz` and cross-checked against
`tools/night/night_report.py`'s own `two_phase_price()` (pairwise `night_report_3v0.md` /
`night_report_4v0.md` / `night_report_4v3.md`) — identical to printed precision:

| run | phase1 median s/iter | phase2 median s/iter | overall median s/iter |
|---|---|---|---|
| seed 3 | 0.0642 | 0.0447 | 0.0612 |
| seed 4 | 0.0634 | 0.0462 | 0.0598 |
| (seed 0, for reference) | 0.0644 | 0.0452 | 0.0614 |

72 checkpoints each completed run, same cadence as nights 1–2 (`chkpt_every_epoch=300`, 12
iters/epoch ⇒ nominal 3,600-iteration spacing after the first two).

## 2. Rung table, n = 5 (seeds 0, 1, 2, 3, 4) beside n = 3, with the replicate and the 95 % χ² interval for σ

**Observed** (rung values from `night3_9991-003.slim.json` / `night3_9991-004.slim.json`
`rung_metrics`, reproduced by `night_report_3v0.md` / `night_report_4v0.md` /
`night_report_4v3.md`'s own rung tables and by `results/night3/extract_night3.py`'s independent
recomputation — all match to printed precision).

| iteration | seed 0 | seed 0′ | seed 1 | seed 2 | seed 3 | seed 4 | SD n=3 (0,1,2) | SD n=5 (0,1,2,3,4) | replicate \|0′−0\| | SD(n=5)/replicate |
|---|---|---|---|---|---|---|---|---|---|---|
| 1,000 | 1208.9363 | 1208.9363 | 1208.0556 | 1209.7639 | 1210.4139 | 1207.2574 | 0.8543 | 1.2698 | 0.0000 | undefined (÷0) |
| 5,000 | 1207.7673 | 1207.7698 | 1206.7832 | 1207.0115 | 1205.5457 | 1206.3897 | 0.5151 | 0.8173 | 0.0025 | 322.04 |
| 25,000 | 1191.7375 | 1192.0739 | 1190.2235 | 1204.3618 | 1192.5858 | 1208.6099 | 7.7627 | 8.3788 | 0.3365 | 24.90 |
| 250,000 | 1146.1958 | 1158.9237 | 1145.3572 | 1148.8000 | 1152.5066 | 1153.1134 | 1.7953 | 3.5426 | 12.7279 | 0.278 |

At 1,000 the replicate difference is 2.38e-5 (rounds to 0.0000 at printed precision), so the
ratio is reported as undefined rather than the very large finite number (≈53,259) it computes
to, matching the convention set in `docs/experiments/002-night2-seeds-1-and-2.md` §2. SD is the
sample standard deviation (`statistics.stdev`, ddof=1): 2 degrees of freedom at n=3, 4 degrees
of freedom at n=5.

**95 % χ² confidence interval for σ at n=5 (4 df)**, using the task's own quantiles
χ²₀.₉₇₅,₄ = 11.143 and χ²₀.₀₂₅,₄ = 0.4844 — interval = SD·√(4/11.143) … SD·√(4/0.4844)
(factors 0.5991 and 2.8736 respectively):

| iteration | SD (n=5) | 95 % CI for σ (n=5) | replicate \|0′−0\| | for reference: 95 % CI for σ (n=3, 2 df) |
|---|---|---|---|---|
| 1,000 | 1.2698 | [0.7608, 3.6489] | 0.0000 | [0.4449, 5.3720] |
| 5,000 | 0.8173 | [0.4897, 2.3486] | 0.0025 | [0.2682, 3.2385] |
| 25,000 | 8.3788 | [5.0201, 24.0774] | 0.3365 | [4.0421, 48.8080] |
| 250,000 | 3.5426 | [2.1225, 10.1801] | 12.7279 | [0.9347, 11.2857] |

(The n=3, 2-df interval uses χ²₀.₉₇₅,₂ = 7.378 and χ²₀.₀₂₅,₂ = 0.0506, as already computed in
`docs/experiments/002-night2-seeds-1-and-2.md` §5a item 3; reproduced here for the side-by-side,
not recomputed from new data.)

At n=5 the picture from n=3 holds in direction but narrows: at 250,000 the CI upper bound
(10.18) is now further below the replicate offset (12.73) than the n=3 upper bound was (11.29);
at 25,000 the CI lower bound (5.02) is still well above the replicate (0.34). Two new seeds did
not flip either inequality. This narrowing is a preview, not the registered application (§5).

## 3. Checkpoints

**Observed** (`results/night3/night_report_checkpoints.csv`, full float, built by
`extract_night3.py` from all six runs' `checkpoint_metrics`; 72 common checkpoint iterations
across seed 0, seed 0′, seed 1, seed 2, seed 3, seed 4).

**Late-phase offsets, 29 checkpoints after iteration 150,000** — mean / min / max, six-run table
extended from `docs/experiments/002-night2-seeds-1-and-2.md` §3, against the run-0/run-0′
replicate offset already on record (+12.6406 mean, min +3.6803, max +17.8153):

| diff | mean | min | max | positive / 29 |
|---|---|---|---|---|
| seed3 − seed0 | +8.9558 | −5.0278 | +23.1705 | 26/29 |
| seed4 − seed0 | +5.4463 | −11.9298 | +17.2501 | 23/29 |
| seed4 − seed3 | −3.5094 | −23.4329 | +11.5944 | 6/29 |

**Within-pair comparison, the two same-wave pairs.** (seed0′ − seed0) is positive at **29/29** of
the late checkpoints (mean +12.64, the twin offset already on record,
`docs/experiments/001-run0-and-replicate.md` §4 and `002` §5a item 9). (seed4 − seed3), the
second same-wave pair, is positive at only **6/29** (mean −3.51, min −23.43, max +11.59) — the
opposite regime: mostly negative, smaller in magnitude, and not one-sided. The two same-wave
pairs do not repeat each other's sign pattern; a within-wave position effect predicting a
positive second-job offset (Ark's night-4 design question, `docs/next-session-plan.md` §3) is
**not** what this pair shows on its own — (seed4 − seed3) is mostly negative. Both pairs and
both seed-vs-seed0 comparisons sit alongside each other; no ranking or mechanism is asserted
here.

**Plateau** (mean of the last 10 of the 72 common checkpoints) and **minimum checkpoint loss**
(over each seed's own full 72-checkpoint trajectory), all six seeds:

| seed | plateau (last-10 mean) | min checkpoint val_loss | at iteration |
|---|---|---|---|
| 0 | 1148.7081 | 1141.0463 | 219,612 |
| 0′ | 1162.7778 | 1156.0002 | 82,812 |
| 1 | 1142.1858 | 1139.7140 | 248,412 |
| 2 | 1146.8842 | 1137.8219 | 162,012 |
| 3 | 1154.4052 | 1150.9345 | 237,612 |
| 4 | 1154.4837 | 1150.0934 | 198,012 |

Seeds 3 and 4 have the two highest plateaus of the six (1154.41, 1154.48) and their minima
(1150.93, 1150.09) sit above every other seed's minimum except seed 0′'s (1156.00). Whether this
groups by individual, by night, or by wave position is not decided here — it is the same
question `docs/next-session-plan.md` §2a raises for the exploratory axes, deferred to §6 below.

## 4. C3 transients: seed 4's 25,000 value against its neighboring checkpoints, and seed 2's earlier case

**Observed** (`night3_9991-004.slim.json`, `night3_9991-003.slim.json` `checkpoint_metrics` and
`rung_metrics`; seed 2's figures from `night2b_9991-002.slim.json`, already recorded in
`docs/experiments/002-night2-seeds-1-and-2.md` §4).

Seed 4's three checkpoints bracketing the 25,000 rung (iterations 3,612 + k·3,600):

| iteration | checkpoint val_loss |
|---|---|
| 21,612 | 1206.3360 |
| 25,212 | 1203.2849 |
| 28,812 | 1200.1395 |

The rung's own evaluation-hook value at exactly iteration 25,000 is **1208.6099**
(`night3_9991-004.slim.json` → `rung_metrics`) — **above both** neighboring checkpoints
(1206.3360 and 1203.2849), by +2.27 and +5.33 respectively, and the checkpoint sequence itself
is monotonically decreasing (1206.34 → 1203.28 → 1200.14).

For comparison, seed 3's three checkpoints bracketing the same rung: 21,612 → 1201.7573;
25,212 → 1190.0517; 28,812 → 1184.5230; rung value 1192.5858 — **between** the two neighbors
(1201.76 and 1190.05, closer to the second), consistent with the decreasing checkpoint trend and
not a local spike.

Seed 2's earlier case (`002` §4, reproduced for the comparison): checkpoints 21,612 → 1205.1803,
25,212 → 1205.9782, 28,812 → 1200.7650 (rising then falling, not monotonic); rung value
1204.3618, **below both** neighbors by 0.8–1.6.

**What the three cases show.** Seed 4's rung-vs-checkpoint gap sits on the opposite side from
seed 2's: seed 2's C3 hook read *below* its checkpoint neighbors, seed 4's reads *above* both of
its neighbors, and seed 3's sits *between* its neighbors in line with a monotonic local trend.
Three individuals, three different relationships between the single-point rung hook and the
surrounding checkpoint trajectory at this rung — no shared sign, no shared mechanism read off
these six numbers. No single-iteration training-loss window was computed for seed 4 in this
session (the deeper 40-iteration/2,000-iteration characterization done for seed 2 in `002` §4
is not repeated here — it is not required by this record's scope).

## 5. §7 measurability clause, applied now as a preview at n = 5 (caveat: 4 degrees of freedom, still one shot)

**Reported / quoted**, not decided here. `docs/preregistration-cheap-vs-expensive.md` §7's
clause (quoted in `docs/experiments/001-run0-and-replicate.md` §5 and `002` §5): *"a rung whose
between-seed standard deviation does not exceed the replicate difference is reported as
unmeasurable, not as a failure of the surrogate."* §7 states the clause applies once, at the
registered N (8 or 10, still undecided — `docs/next-session-plan.md` §1.3). Applying it now, at
n=5 (4 degrees of freedom), is explicitly a preview, not the registered application — the same
status night 2's n=3 preview carried, one step further along the population and with one fewer
degree of freedom short of whatever N is finally registered.

The SD/replicate figures at n=5, repeated for this section's purpose:

| rung | SD (n=5) | replicate \|0′−0\| | SD(n=5)/replicate | 95 % CI for σ (n=5) |
|---|---|---|---|---|
| 1,000 | 1.2698 | 0.0000 | undefined | [0.7608, 3.6489] |
| 5,000 | 0.8173 | 0.0025 | 322.04 | [0.4897, 2.3486] |
| 25,000 | 8.3788 | 0.3365 | 24.90 | [5.0201, 24.0774] |
| 250,000 | 3.5426 | 12.7279 | 0.278 | [2.1225, 10.1801] |

`docs/next-session-plan.md` §3's branch wording, quoted verbatim (unchanged since night 2):

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

This record does not make that call, does not rank the two branches, and reports no ρ. The
reviewers' own reading that the two named (b) candidates do not survive measurement (plateau
SD/replicate 0.239 at n=3, `002` §5a item 7) is not re-evaluated at n=5 here.

## 6. Pre-registered night-3 readings (`docs/next-session-plan.md` §2a) — evaluated elsewhere

`docs/next-session-plan.md` §2a pre-registered, before launch, two readings for night 3 and named
two exploratory axes:

- The **registered reading**: whether seed 3 or seed 4 shows a single-type ablation dependence
  (protocol of `002` §5f, all 65 types, 16 items, clamp to 0, computed post hoc from checkpoint
  250,008) of the size seen in seed 2's R2 (+21,157, an order of magnitude above every other type
  in that run and above the largest twin per-type discrepancy, 2863 at T2a) — a repeat of that
  size would make R2 a repeated observation, not yet a test.
- The **positive reading**: a single-type excess exceeding 2863 (the twin discrepancy bound) in
  either seed 3 or seed 4.
- The **exploratory axes**, no verdict pre-committed: row-B activity on T5c/T5d; profile
  compression (sd, range); and — new with night 3 — within-pair vs between-pair closeness across
  the two same-wave pairs (0, 0′) and (3, 4), the first free separation of "individual" from
  "night"/"wave" available in this dataset (§3 above gives the raw within-pair sign/magnitude
  numbers for that separation; the ablation and row-B analyses are what apply the pre-registered
  reading to them).

These readings are evaluated in the ablation and row-B diagnostic records, not in this document:

- `results/night3/diagnostics/ablation/` (pointer — R2-sized single-type dependence check for
  seeds 3 and 4)
- `results/night3/diagnostics/rowB/` (pointer — row-B preview extended to n = 5–6, T5c/T5d and
  compression axes)

This record's §3 and §4 report only the loss-level (rung and checkpoint) numbers; the
cell-type-level reading of the pre-registered clause is not made here.

## 7. Provenance

- `results/night3/extract_night3.py` — this session's script; sha256
  `65c3cabfcad07cea765a3adec9a441b767f583765fae20b84c3775a175582692` (hardening item 9,
  `docs/tool-hardening-package.md`); builds the slim jsons, the two `iter_wall_s_*.csv.gz`, the
  two `train_loss_last1000_*.csv`, copies the wave json/launcher-log/progress-log triple, and
  builds the six-way `night_report_checkpoints.csv` (full float — hardening item 19; see
  `results/night3/README.md`). Its own equality assertion checks that both night-3 slim jsons
  carry exactly `results/night2/night2_9991-001.slim.json`'s key set.
- `tools/night/night_report.py` — run unmodified, three times (`--a`/`--b` pairwise, its only
  supported form), against the raw run jsons (the slim jsons drop `iter_wall_s`, which the
  two-phase price table needs): `night_report_3v0.md`, `night_report_4v0.md`,
  `night_report_4v3.md` (plus their own `night_report_checkpoints_3v0.csv` / `_4v0.csv` /
  `_4v3.csv`, `r4()`-formatted — see the README's item-19 note on which files are full float and
  which are not).
- Interpreter: system `python` via the `py` launcher (3.12.10 this session; the night-run venv,
  3.10.20, was not needed — both scripts use only the standard library).
- Inputs read (not modified): raw run jsons in the night scratchpad (`night1_9991-000.json`,
  `night3_9991-003.json`, `night3_9991-004.json`, and the three `wave_night3.*` files),
  `results/night1/night1_9991-000.slim.json`, `results/night1/rep_9991-900.slim.json`,
  `results/night2/night2_9991-001.slim.json`, `results/night2/night2b_9991-002.slim.json`.
- Written by: CC's subagent on Sonnet, 2026-09-16. Verified by: CC.
