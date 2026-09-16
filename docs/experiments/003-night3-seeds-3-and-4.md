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

**Ablation profiles of seeds 3 and 4 and the pre-registered reading (2026-09-16; protocol of 002
§5f, `ablation.py` imported not copied; run by CC's subagent on Opus; verified by CC)**

> **Override of the machine verdict (2026-09-16, on Mike's word «давайте пробовать», reviewers
> Ark 05:27Z and Zcode 05:27Z concurring).** `ablation_reading.json`'s own `verdict` field reads
> `"positive_reading_triggered": true` and text *"POSITIVE: a single-type dependence exceeding
> 2863 appears in seed 3 or seed 4 -> the R2 finding becomes a REPEATED OBSERVATION, still not a
> test."* **That printed text is not this record's reading.** `docs/next-session-plan.md` §2a's
> rule was written with two different size definitions for the same clause — "of the size seen
> in seed 2, +21,157" in the sentence before, "exceeds 2863" (the twin discrepancy bound) in the
> operational clause the script (`ablation_night3.py:466-476`) actually evaluated. The script
> executed the operational clause literally and only that clause, which measures single-type
> *dominance* (a ratio against the second-largest type in the same run), not a repeat of R2's
> +21,157.5. It is not a repeat: Δ_R2 is +146.9 (seed 3) and +41.8 (seed 4) against +21,157.5
> (seed 2) — half an order of magnitude short, not "the size seen in seed 2". The threshold 2863
> is also met by 5 of the 6 runs on record (item 2 below), so it does not discriminate a repeat
> from the background rate. **The outcome under the registered rule is therefore undetermined by
> defect of the rule, not positive** — this is recorded as a pre-registration defect (the rule's
> two clauses disagree with each other and the script could only execute one of them), not as a
> positive outcome, and not as a re-reading of what the script printed. `ablation_reading.json`
> itself is left unchanged, as the artefact of what the script printed under the rule as written
> — see checklist rule 16, `docs/CHECKLIST-research-repo.md`.

1. Controls: stored val_loss 1155.7706 / 1156.8285 (seeds 3 / 4); P0 −1.3e-5 / −5.9e-5; P1 +1.3e-5
   / +6.4e-5 (max item 4.9e-4, not bit-identical, within the noise floor); P2 R1–R8 +58.04 /
   +79.26; P2 the 34 decoder-input types +409.92 (+35.5 %) / +388.15 (+33.6 %) — exploratory note:
   twice the +16–23 % span of every night-2 run. 204 evaluations, seven invariants asserted;
   repeatability seed 3 fresh process max |ΔΔ_T| 2.9e-4 (Tm3), ρ = 1.0000; run dirs unchanged (594
   files); night-2 profiles re-read from the committed CSV, the 13/10-item columns recomputed from
   the per-item columns (max deviation 9e-13).
2. The pre-registered reading, clause by clause (the rule in plan §2a was written with three
   clauses: (i) "a single-type dependence of the size seen in seed 2" (R2 +21,157); (ii) "an order
   of magnitude above every other type in that run"; (iii) "above the largest twin per-type
   discrepancy 2863"): table of top type / second type / ratio / > 2863 for all six runs — seed 0
   Tm5c 2616.8 / Mi4 1323.5 / 1.98× / no; seed 0′ Mi4 3266.6 / T2a 3171.9 / 1.03× / yes; seed 1
   TmY15 3959.5 / T2a 3651.0 / 1.08× / yes; seed 2 R2 21,157.5 / Mi4 7475.9 / 2.83× / yes; seed 3
   Mi4 4827.5 / L5 1346.1 / 3.59× / yes; seed 4 CT1(Lo1) 10,460.9 / Tm5b 1314.1 / 7.96× / yes.
   Clause (iii): positive for both seeds as written — but the threshold does not discriminate: 5 of
   6 runs exceed it, including 0′ and 1 whose top/second ratio is ≈ 1. Clause (ii): satisfied by no
   run, including the reference run seed 2 (2.83×, not 10×) — the clause was unsatisfiable as
   written; what does repeat is one-type dominance: top/second 1.0–2.0× for seeds 0 / 0′ / 1 and
   2.8× / 3.6× / 8.0× for seeds 2 / 3 / 4, seed 4's shape sharper than seed 2's. Clause (i): 10,461
   is half of 21,157 and 4,828 a quarter — not "the same size". Δ_R2 across six runs: +459.2 /
   +679.8 / −1.0 / +21,157.5 / +146.9 / +41.8 — R2 itself does not repeat and is not in the top 10
   of seeds 3 or 4; the class (one type carries a disproportionate share) repeats, the type does
   not. Statement: the reading rule was written ambiguously and one clause was unsatisfiable — a
   defect of the pre-registered reading, CC's, recorded as such; all three clause outcomes are
   recorded side by side; the verdict is the reviewers' and Mike's, not made here.
3. Twin trap on 15 pairs (1−ρ, 16 items, ranked): (0,0′) 0.2847 · (1,3) 0.4558 · (0,3) 0.4653 ·
   (0′,3) 0.5181 · (0,1) 0.5238 · (0′,2) 0.5571 · (0′,1) 0.5594 · (1,2) 0.5598 · (2,3) 0.6072 ·
   (0,2) 0.6466 · (2,4) 0.6744 · (0,4) 0.7047 · (1,4) 0.7177 · (3,4) 0.9017 · (0′,4) 0.9117. On
   1−ρ the twins remain the global minimum in all three item subsets (0.2847 / 0.2968 / 0.3168),
   nearest foreign pair now (1,3) 0.4558; on Euclidean the twin trap FAILS: (0′,3) 3545 and (0,3)
   4705 undercut the twins' 4798 (and in the 13/10-item subsets). Same-wave pair (3,4): 1−ρ 0.9017,
   rank 14 of 15 (Euclidean 11,679, rank 8); cross-wave 1−ρ spans 0.456–0.912, median 0.560 — the
   two runs of one night are nearly the farthest pair; no wave clustering on this instrument. Sign
   agreement 6/6: 39 of 65 (16 items), 41 (13), 37 (10); noise band |Δ_T| < 2e-3: Mi11 only in
   seeds 3 and 4 (Mi11 and Mi12 for seed 4 on 13 items).

## 6b. Row B (observational profile), seeds 3 and 4 — preview, n = 6, not a test

**Reported / recomputed from committed artefacts**, not run in this session
(`results/night3/diagnostics/rowB/`; run by CC's subagent on Opus; verified by CC).

1. Artefacts: `rowB3.py` (this directory's driver) and `rowB.py` (a byte-identical copy of
   night 2's `rowB.py`, imported as a module — the three deliberate differences from night 2 are
   stated in `rowB3.py`'s own docstring). Seeds 0–2's profiles are not recomputed here; they are
   read from `results/night2/diagnostics/rowB/rowB_profiles_250008.csv`. `SHA256.txt` lists the
   hash of every file in the directory. Outputs: `rowB_profiles_{iter0,25212,250008}.csv`,
   `rowB_distances.json`, `rowB_exploratory.json`, `rowB_preview.json`, `rowB_vs_rowA.json`,
   `rowB_controls.json`, `rowB_eval_records.json`, `rowC_trajectory.csv`, `README.md`.
2. Controls: hook purity 0…3e-5 against a tolerance of 1e-4; seven `eval_rung` invariants
   asserted on 163 evaluations; P0 ladder at iteration 0 over all 15 pairs — twins **0.000000**,
   the nine new cross-seed pairs **0.119–0.211**; floor for seed 3 across three fresh processes,
   ρ = **1.0000**, max |ΔB| **1.4e-8**; P2 (silencing R1–R8) moves B on **64 of 65** types in both
   seeds.
3. The 15 pairwise distances (1 − ρ, Spearman over the 16-item aggregate, 65 types) at 250,008,
   ascending: (0, 0′) 0.3487 · (1, 3) 0.4043 · (2, 3) 0.4752 · (0, 3) 0.4969 · (0, 2) 0.5455 ·
   (0, 1) 0.5689 · (1, 2) 0.5759 · (0′, 3) 0.5990 · (0′, 1) 0.6350 · (0, 4) 0.7313 · (1, 4) 0.7478
   · (2, 4) 0.8085 · (0′, 2) 0.8212 · (3, 4) 0.8565 · (0′, 4) 0.8647.
4. **Twin trap**: (0, 0′) is the minimum of the 15, in 16/16 items and on both secondary
   readings. The nearest foreign pair moves from (0, 2) (night 2) to **(1, 3) 0.4043**; the
   margin falls from 0.197 to **0.056**. On Euclidean distance the twin trap fails — as it does
   for the ablation (row-A) profile, §6 item 3 above.
5. **Same-wave pair (3, 4)**: 0.8565, rank 14 of 15, above 12 of the 13 cross-wave pairs
   (cross-wave median 0.599). The same answer as the ablation channel: no wave effect on this
   instrument.
6. **Exploratory axes** (numbers, no verdict), order seeds 0 / 0′ / 1 / 2 / 3 / 4:
   - T5c mean activity: 41.62 / −0.04 / 12.31 / 11.14 / 2.19 / 0.35; T5d: 40.65 / 19.97 / −0.81 /
     −0.13 / 0.38 / 0.10. T5c was the top type of the row-B profile for seeds 0, 1 and 2; for
     seeds 3 and 4 the top types are T3 and Tm3.
   - Profile sd: 7.32 / 5.18 / 2.42 / 2.70 / 2.20 / 5.76; range: 43.5 / 24.7 / 21.1 / 11.9 / 13.7
     / 34.6. Seed 3 is the most compressed of the six, seed 4 the second-widest. The same-wave
     pair straddles the "night 1 / night 2" compression split named in `002` §5i second pass
     item 5, so a per-night compression confound is not supported by these two points.
   - Top/second ratio by |mean| at 250,008 (requested by Ark for the channel comparison): seed 0
     T5c/T5d 1.02×; 0′ Tm4/T5d 1.19×; 1 T5c/C3 1.40×; 2 T5c/Tm2 1.04×; 3 T3/T2a 1.12×; 4
     Tm3/T2a 1.33× — all six in 1.0–1.4×. The ablation channel (§6 item 2 above) gives 1.98 /
     1.03 / 1.08 / 2.83 / 3.59 / 7.96×. The "one dominant type" form exists only in the causal
     (ablation) channel; the observational row-B channel does not show it for any run.
   - B ↔ A within-individual Spearman: seeds 3/4 = **+0.549 / +0.573** (night-2 runs: 0.389 /
     0.481 / 0.563 / 0.653).
   - Preview 25,212 → 250,008 at n = 6: Spearman between the 15 distances at the two checkpoints
     = **0.825** (was 0.60 over six pairs at n = 4); within-run self-consistency (25,212 vs
     250,008 profile ρ): seed 2 0.358, seed 4 0.377, seed 0 0.581, 0′ 0.675, seed 3 0.695, seed 1
     0.790.
7. **Twin amplitude band per type**: max |ΔB| between seed 0 and seed 0′ = **41.65** (median
   0.73), larger than the (3, 4) pair's **28.80**. See the correction to `002` §5i second pass
   item 3 recorded in `002` itself.
8. **Verdict**: none. This is a preview diagnostic, not the pre-registered (b)/(b2) test, which
   runs once at the registered N.

## 6c. The scale of the loss: learned gain vs untrained level (observation, 2026-09-16)

**Observed** (slim jsons' `checkpoint_metrics` at iteration 0, all six seeds;
`results/night3/diagnostics/ablation/ablation_controls.json` P2a for R1–R8 silenced;
`results/night2/diagnostics/per_item_250008.csv`, seed 0's per-item column). No rule change; this
is a reading of scale, not a new registration.

| quantity | seed 0 | seed 0′ | seed 1 | seed 2 | seed 3 | seed 4 |
|---|---|---|---|---|---|---|
| held-out loss, iteration 0 | 1212.56 | 1212.56 | 1212.55 | 1212.56 | 1212.55 | 1212.54 |
| checkpoint 250,008 | 1148.81 | 1160.98 | 1144.64 | 1147.72 | 1155.77 | 1156.83 |
| R1–R8 silenced (P2a) | 1207.24 | 1208.01 | 1209.50 | 31,773.93 | 1213.82 | 1236.09 |
| fraction of learned gain removed by blinding | 0.917 | 0.912 | 0.955 | 472.3 | 1.022 | 1.423 |

Held-out loss at iteration 0 is identical to two decimals across all six seeds — the untrained
level does not depend on seed. Per-item scale (seed 0, checkpoint 250,008,
`per_item_250008.csv`): min `bamboo_1_split_01` = 79.39, max `ambush_2_split_02` = 4,764.62; the
three `ambush_2` splits (4,049 / 4,364 / 4,765) dominate the 16-item mean. The training loss is
flyvis's `l2norm` — per-sample L2 norm over (frames, flow channels, hexals), averaged over the
batch (`flyvis/task/objectives.py:10-22`) — not a per-pixel error, which is why individual items
sit at such different scales.

**Reading (observation, no rule change).** The learned gain is ≈ 60 loss units on an untrained
level of ≈ 1,212. Silencing all photoreceptors removes essentially the whole learned gain in five
of six runs (fraction 0.91–1.42, i.e. the silenced loss returns to at or above the untrained
level) — **the earlier chat reading, "five of six runs barely depend on input," is withdrawn by
its authors, Ark and Zcode, 06:03–06:04Z.** Seed 2 is a different phenomenon: it does not return
to the untrained level, it explodes to 31,773.93, more than an order of magnitude above it — 26×
the untrained level, not a return to it.

**Consequence, stated as a proposal for the next registration only — not decided here.** On the
learned-gain scale, the twin replicate difference (12.73, `002` §5a item 9 / `001` §4) is **21 %**
of the ≈ 60-unit gain, and the between-seed σ at n = 5 (3.54, §2 above) is **6 %** of it. §7's
tolerance and its FAIL (`docs/preregistration-cheap-vs-expensive.md` §7; the 1.11 % / 12.73 result
recorded in `001` §4 and reproduced in §2 above) stand exactly as written — this observation
proposes a possible next-registration reframing of scale, it does not revisit the registered
percentage or its outcome.

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
