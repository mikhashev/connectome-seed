# Experiment 004 — night 4, replicate 3′ and seed 5

**Date:** 2026-09-17 · **Status:** both jobs complete, recorded below · **Substrate:** flyvis
1.2.0, connectome `fib25-fib19_v2.2.json`, extent 15, task `flow` on MPI-Sintel · **Written by:**
CC's subagent on Sonnet, 2026-09-17, from `docs/experiments/003-night3-seeds-3-and-4.md` (format),
`results/night4/`, and the raw night jsons; verified by CC.

**Observed** = read off a committed artefact, with its path. **Inferred** = a conclusion drawn
from Observed numbers. **Reported** = someone else's statement, attributed.

No ρ, no ranks, no verdict on (b)/(b2) is made in this record.

## 1. What ran

**Observed** (`results/night4/wave_night4.json`, `wave_night4.launcher.log`,
`rep_9991-903.slim.json`, `night4_9991-005.slim.json`).

| run | id | seed | tag | started (run json) | finished (run json) | total_train_wall_s | wall (launcher) | iterations | exit |
|---|---|---|---|---|---|---|---|---|---|
| replicate 3′ | `9991/903` | 3 | `rep` | 2026-09-16T20:27:30Z | 2026-09-17T00:27:45Z | 14435.3311 (4:00:35.3311) | 14444.2 s (launcher `2026-09-16T20:27:29Z`→`00:28:13Z`) | 250,008 | ok |
| seed 5 | `9991/005` | 5 | `night4` | 2026-09-17T00:28:14Z | 2026-09-17T04:28:34Z | 14460.3758 (4:01:00.3758) | 14474.1 s (launcher `2026-09-17T00:28:13Z`→`04:29:27Z`) | 250,008 | ok |

Both jobs ran in **one wave, start to end, no interruption**: `WAVE START tag=night4` at
`2026-09-16T20:27:29Z`, `WAVE DONE 2/2 ok` at `2026-09-17T04:29:27Z`. Like night 3, night 4
needed no re-run: no `killed_*.partial.json`, only one wave-file triple
(`wave_night4.json`/`.launcher.log`/`.progress.log`). Wall figures above are the launcher's own
`wall_s` field, consistent with how night 1–3's "wall (launcher)" column was reported
(`results/night4/README.md` notes the small, expected gap against each run's own
`total_train_wall_s`).

**Launch and pre-registered reading.** Night 4 was launched as
`tools/night/start_night.ps1 -Tag night4 -Seeds 5 -ReplicateOf 3 -NoReplicate` (launcher commit
`3f4af81`, `--replicate-of` added for this wave), running replicate 3′ (seed 3, id `9991/903`,
tag `rep`) FIRST and seed 5 (id `9991/005`) SECOND, sequential, `--no-determinism`, 250,000
iterations, rungs 1,000/5,000/25,000/250,000 — the reading itself was pre-registered before
launch (`docs/next-session-plan.md` §2a, Ark 19:58Z/Zcode 20:14Z, recorded 2026-09-16, committed
`874cc32`) and is applied in §4 below.

**argv comparison.** `rep_9991-903.json`'s `argv` differs from `night3_9991-003.json`'s only in
`--id` (`9991/903` vs `9991/003`), `--tag` (`rep` vs `night3`) and `--progress-file`
(`wave_night4.progress.log` vs `wave_night3.progress.log`); `--seed 3`, `--n-iters 250000`,
`--rungs 1000,5000,25000,250000`, `--out-dir`, `--no-determinism` and `--progress-every 100` are
byte-identical. `connectome_sha256`
(`bfbb0766251ff09e22723d0ebbf7b14793e70b3ae8ad0eea64eac9d28223351a`) and `versions` (`flyvis
1.2.0`, `torch 2.9.1+cu128`, `numpy 2.2.6`, `python 3.10.20`, `cuda 12.8`, `cudnn 91002`, `gpu
NVIDIA RTX PRO 4500 Blackwell`) are identical across `night3_9991-003.json`, `rep_9991-903.json`
and `night4_9991-005.json` — `run_individual.py` is unchanged since night 3, same connectome
file, same environment.

Rebuild note: 72 checkpoints each; `errors: []` for both runs.

**Two-phase price** (median s/iter; phase 1 = iterations 1,000–150,000, phase 2 =
150,001–250,008), computed independently by `results/night4/extract_night4.py` from
`iter_wall_s_9991-903.csv.gz` / `iter_wall_s_9991-005.csv.gz` and cross-checked against
`tools/night/night_report.py`'s own `two_phase_price()` (pairwise `night_report_3primev3.md` /
`night_report_5v0.md` / `night_report_3primev0prime.md`) — identical to printed precision:

| run | phase1 median s/iter | phase2 median s/iter | overall median s/iter |
|---|---|---|---|
| replicate 3′ | 0.0644 | 0.0454 | 0.0607 |
| seed 5 | 0.0640 | 0.0457 | 0.0609 |
| (seed 3, for reference) | 0.0642 | 0.0447 | 0.0612 |
| (seed 0, for reference) | 0.0644 | 0.0452 | 0.0614 |

72 checkpoints each completed run, same cadence as nights 1–3 (`chkpt_every_epoch=300`, 12
iters/epoch ⇒ nominal 3,600-iteration spacing after the first two).

## 2. Rung table, n = 6 (individuals 0, 1, 2, 3, 4, 5) beside n = 5, with the two replicate pairs and the 95 % χ² interval for σ

**Observed** (rung values from `rep_9991-903.slim.json` / `night4_9991-005.slim.json`
`rung_metrics`, reproduced by `night_report_3primev3.md` / `night_report_5v0.md` /
`night_report_3primev0prime.md`'s own rung tables and by
`results/night4/extract_night4.py`'s independent recomputation — all match to printed
precision).

| iteration | seed 0 | seed 0′ | seed 1 | seed 2 | seed 3 | seed 4 | seed 5 | replicate 3′ | SD n=5 (0,1,2,3,4) | SD n=6 (0,1,2,3,4,5) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1,000 | 1208.9363 | 1208.9363 | 1208.0556 | 1209.7639 | 1210.4139 | 1207.2574 | 1207.3300 | 1210.4302 | 1.2698 | 1.3012 |
| 5,000 | 1207.7673 | 1207.7698 | 1206.7832 | 1207.0115 | 1205.5457 | 1206.3897 | 1208.2387 | 1205.5182 | 0.8173 | 0.9639 |
| 25,000 | 1191.7375 | 1192.0739 | 1190.2235 | 1204.3618 | 1192.5858 | 1208.6099 | 1204.7794 | 1187.4011 | 8.3788 | 8.0614 |
| 250,000 | 1146.1958 | 1158.9237 | 1145.3572 | 1148.8000 | 1152.5066 | 1153.1134 | 1159.1158 | 1162.9375 | 3.5426 | 5.1425 |

**The two replicate pairs, side by side** (this wave adds the second one — night 1's (0, 0′) and
night 4's own (3, 3′)):

| iteration | seed 3 | replicate 3′ | 3′ − 3 | seed 0 | replicate 0′ | 0′ − 0 |
|---|---|---|---|---|---|---|
| 1,000 | 1210.4139 | 1210.4302 | +0.0163 (rounds to +0.016) | 1208.9363 | 1208.9363 | 0.0000 |
| 5,000 | 1205.5457 | 1205.5182 | −0.0276 (rounds to −0.028) | 1207.7673 | 1207.7698 | +0.0025 |
| 25,000 | 1192.5858 | 1187.4011 | −5.1847 (rounds to −5.185) | 1191.7375 | 1192.0739 | +0.3365 |
| 250,000 | 1152.5066 | 1162.9375 | +10.4309 (rounds to +10.431; 0.905 % of seed 3) | 1146.1958 | 1158.9237 | +12.7279 |

SD is the sample standard deviation (`statistics.stdev`, ddof=1): 4 degrees of freedom at n=5, 5
degrees of freedom at n=6.

**95 % χ² confidence interval for σ at n=6 (5 df)**, using the quantiles χ²₀.₉₇₅,₅ = 12.8325 and
χ²₀.₀₂₅,₅ = 0.8312 (`scipy.stats.chi2.ppf(0.975, 5)` / `.ppf(0.025, 5)`) — interval =
SD·√(5/12.8325) … SD·√(5/0.8312):

| iteration | SD (n=6) | 95 % CI for σ (n=6) | replicate \|0′−0\| | for reference: 95 % CI for σ (n=5, 4 df) |
|---|---|---|---|---|
| 1,000 | 1.3012 | [0.8122, 3.1913] | 0.0000 | [0.7608, 3.6489] |
| 5,000 | 0.9639 | [0.6017, 2.3642] | 0.0025 | [0.4897, 2.3486] |
| 25,000 | 8.0614 | [5.0320, 19.7717] | 0.3365 | [5.0201, 24.0774] |
| 250,000 | 5.1425 | [3.2100, 12.6126] | 12.7279 | [2.1225, 10.1801] |

(The n=5, 4-df interval uses χ²₀.₉₇₅,₄ = 11.143 and χ²₀.₀₂₅,₄ = 0.4844, already computed in
`docs/experiments/003-night3-seeds-3-and-4.md` §2; reproduced here for the side-by-side, not
recomputed from new data.)

At n=6 the picture from n=5 mostly holds in direction, with one change of note: at 250,000 the CI
now widens on both ends (n=5: [2.12, 10.18] → n=6: [3.21, 12.61]) because seed 5 (1159.1158) sits
close to the top of the range, pulling SD up from 3.5426 to 5.1425 — the CI upper bound (12.61) now
sits just below the run-0/0′ replicate offset (12.73), narrower than at n=5 but on the same side;
at 25,000 the CI lower bound (5.03) is still well above the replicate offset (0.34). This
narrowing/widening is a preview, not the registered application (§5).

## 3. Checkpoints

**Observed** (`results/night4/night_report_checkpoints.csv`, full float, built by
`extract_night4.py` from all eight runs' `checkpoint_metrics`; 72 common checkpoint iterations
across seed 0, seed 0′, seed 1, seed 2, seed 3, seed 4, replicate 3′, seed 5).

**Checkpoint at final_iteration 250,008** (the two replicate pairs):

| pair | earlier | replicate | diff |
|---|---|---|---|
| 3′ − 3 | 3: 1155.7706 | 3′: 1163.3766 | +7.6059 (rounds to +7.606) |
| 0′ − 0 | 0: 1148.8075 | 0′: 1160.9823 | +12.1749 |

**Late-phase offsets, 29 checkpoints after iteration 150,000** — mean / min / max / median, for
the three pairs the task named ((3′ vs 3), (5 vs 0), (3′ vs 0′)), against the (0′ − 0) reference
already on record:

| diff | mean | min | max | median | positive / 29 |
|---|---|---|---|---|---|
| 3′ − 3 | +7.0032 | −3.5566 | +12.4983 | +7.9409 | 27/29 |
| 5 − 0 | +5.4146 | −10.6298 | +19.7061 | +4.9026 | 21/29 |
| 3′ − 0′ | +3.3183 | −4.9640 | +11.6755 | +3.2181 | 21/29 |
| 0′ − 0 (reference) | +12.6406 | +3.6803 | +17.8153 | +12.2470 | 29/29 |

**Selected checkpoint differences, 3′ − 3** (iterations named in the task brief):

| iteration | 3′ | 3 | diff |
|---|---|---|---|
| 25,212 | 1187.1360 | 1190.0517 | −2.9157 (rounds to −2.916) |
| 72,012 | 1174.2891 | 1178.1888 | −3.8997 (rounds to −3.900) |
| 79,212 | 1186.6132 | 1174.6413 | +11.9719 (rounds to +11.972) |
| 151,212 | 1176.7531 | 1165.2208 | +11.5324 (rounds to +11.532) |
| 180,012 | 1168.1160 | 1166.3808 | +1.7352 (rounds to +1.735) |

**Learned gain** (checkpoint 0 − checkpoint 250,008), the three runs the task brief names:

| run | checkpoint 0 | checkpoint 250,008 | learned gain |
|---|---|---|---|
| seed 3 | 1212.5497 | 1155.7706 | 56.7791 (rounds to 56.779) |
| replicate 3′ | 1212.5497 | 1163.3766 | 49.1732 (rounds to 49.173) |
| seed 5 | 1212.5467 | 1156.3866 | 56.1601 (rounds to 56.160) |

`results/night4/extract_night4.py` prints the same quantity for all eight runs (seed 0: 63.7481;
0′: 51.5732; 1: 67.9168; 2: 64.8414; 4: 55.7095) — carried in the script's own stdout, not
repeated as a table here since the task brief's three-run comparison is what this record needs;
the full eight-run set is available by re-running the script.

**Plateau** (mean of the last 10 of the 72 common checkpoints) and **minimum checkpoint loss**
(over each run's own full 72-checkpoint trajectory), all eight runs:

| run | plateau (last-10 mean) | min checkpoint val_loss | at iteration |
|---|---|---|---|
| 0 | 1148.7081 | 1141.0463 | 219,612 |
| 0′ | 1162.7778 | 1156.0002 | 82,812 |
| 1 | 1142.1858 | 1139.7140 | 248,412 |
| 2 | 1146.8842 | 1137.8219 | 162,012 |
| 3 | 1154.4052 | 1150.9345 | 237,612 |
| 4 | 1154.4837 | 1150.0934 | 198,012 |
| 3′ | 1163.9078 | 1161.6192 | 248,412 |
| 5 | 1151.4077 | 1143.1055 | 223,212 |

Replicate 3′ has the highest plateau of the eight runs on record (1163.91), just above 0′
(1162.78); its minimum (1161.62) is likewise the highest minimum on record. Seed 5's plateau
(1151.41) and minimum (1143.11) sit in the middle of the pack, closer to seeds 0/2 than to
3/4/3′. Whether this groups by individual, replicate-vs-original, or wave is not decided here.

## 4. The pre-registered night-4 reading, applied as written

**Reported / quoted**, then applied to the numbers above — `docs/next-session-plan.md` §2a's
"Pre-registered reading of night 4" (Ark 19:58Z, Zcode 20:14Z, recorded 2026-09-16 before launch,
committed `874cc32`).

**Position correction, already recorded in the plan and reproduced here.** Seed 3 ran FIRST in
night 3 (`wave_night3.json`: `9991/003` launched 20:35:23Z, `9991/004` at 00:35:38Z); replicate
3′ (`9991/903`) also ran FIRST in night 4 (`wave_night4.json`: launched 20:27:29Z, `9991/005` at
00:28:13Z). So (3, 3′) is a replicate pair at the **same** wave position (first vs first) — the
same shape as (0, 0′), which was also first-and-only in its own wave.

**Three explanations named before the data, and what each predicts for |3′ − 3| at 250,000**
(Ark 19:58Z): **P — position effect** (the second job in a wave ends worse): predicts ≈ 0,
because 3 and 3′ occupy the *same* position; **U — replicate divergence is universal**: predicts
≈ +12.7 (the (0, 0′) figure); **S — the offset depends on the seed** (seed 0's trajectory
diverges under non-determinism, seed 3's may not, or by a different amount): predicts anything.

**Result applied.** |3′ − 3| at 250,000 = +10.4309 (§2 above) — large, not near zero. **This
rules out P**: with position held constant between the two runs, a position effect predicts ≈ 0,
and the observed offset is neither small nor of a different sign than (0, 0′)'s — it is
comparable in size. **U predicted ≈ +12.7; observed is +10.4** — close in the same direction, not
exact. **S is not excluded** by this result: a value near +12.7 that is somewhat smaller is
consistent with either U (with sampling noise) or S (a seed-dependent magnitude that happens to
be close to seed 0's). This record does not choose between U and S; only P is ruled out by the
constant-position design.

**Recorded as an observation, no verdict** (n = 2 replicate pairs on record): in both pairs, the
replicate ends worse than its original at the 250,000 hook (+12.7279 for 0′ − 0, +10.4309 for
3′ − 3), and the sign is one-sided in the late-checkpoint tail in both cases (29/29 positive for
0′ − 0, 27/29 positive for 3′ − 3, §3 above). Two pairs is not enough to establish a rate; this is
stated as what is on record, not as a rule or a prediction for a third pair.

**The C3 finding.** The registered C3 (25,000) replicate difference on record before this wave
was **0.3365** (§7 of the pre-registration, pair 0/0′; also `docs/experiments/002-night2-*.md`
§5a and `003` §2). The second replicate pair does **not** reproduce it: |3′ − 3| at the 25,000
hook = **5.1847** (rounds to 5.18), **≈15× larger** (5.1847 / 0.3365 = 15.41); the neighbouring
checkpoint at 25,212 gives 3′ − 3 = **−2.9157** (rounds to −2.92), also far from 0.3365 and of
the opposite sign from the hook value. **The `docs/preregistration-cheap-vs-expensive.md` §4/§7
b2 "cheap-side" measurability threshold (0.3365 at C3) rests on a single replicate pair** — this
second pair shows the threshold is not stable across replicates of even the same seed. Stated as
an observation: the rule itself (§4's b2 clause, "the top-k set of a ranking exists only if the
gap … exceeds … 0.3365 on the cheap side") is **not changed** by this record; whether it should
be re-derived from two pairs instead of one is a decision for Mike and the reviewers, not made
here.

**Seed 5 at C3.** Seed 5's C3 (25,000) hook value is **1204.7794** — closer to seeds 2
(1204.3618) and 4 (1208.6099) than to seeds 0/0′/1/3/3′, which cluster at 1187.4–1192.6 (§2
table). Seed 5 "lags" (reads a higher, less-trained loss) at C3 the same way seeds 2 and 4 do;
whether this is a property of individuals, of the population getting less homogeneous as it
grows, or something else is not decided here — it is recorded as the same pattern already
visible in night 3 (`003` §3's plateau observation: "seeds 3 and 4 have the two highest
plateaus… whether this groups by individual, by night, or by wave position is not decided
there").

**§7 measurability clause: applied once, at the registered N, not here.** §7's rule ("a rung
whose between-seed standard deviation does not exceed the replicate difference is reported as
unmeasurable, not as a failure of the surrogate") and its b2 companion in §4 are, by the
pre-registration's own timing rule, applied a single time once all N individuals are collected —
N (8 or 10) is still undecided (`docs/next-session-plan.md` §1 decision 3). This record computes
the n=6 SD and CI (§2 above) as the same kind of preview night 2 and night 3 already carried
(one preview further along the population, one fewer degree of freedom short of whatever N is
finally registered); it is not the registered application, and no ρ is computed here — none of
the pre-registration's ρ-based (b)/(b2) statistics is run in this record.

## 5. Provenance

- `results/night4/extract_night4.py` — this session's script; sha256
  `480e3855d2468701a298ae128cf33771a0b08214fab30e77db8c1189e87d61d0` (hardening item 9,
  `docs/tool-hardening-package.md`); builds the slim jsons, the two `iter_wall_s_*.csv.gz`, the
  two `train_loss_last1000_*.csv`, copies the wave json/launcher-log/progress-log triple, and
  builds the eight-way `night_report_checkpoints.csv` (full float — hardening item 19; see
  `results/night4/README.md`). Its own equality assertion checks that both night-4 slim jsons
  carry exactly `results/night2/night2_9991-001.slim.json`'s key set.
- `tools/night/night_report.py` — run unmodified, three times (`--a`/`--b` pairwise, its only
  supported form), against the raw run jsons (the slim jsons drop `iter_wall_s`, which the
  two-phase price table needs): `night_report_3primev3.md`, `night_report_5v0.md`,
  `night_report_3primev0prime.md` (plus their own
  `night_report_checkpoints_{3primev3,5v0,3primev0prime}.csv`, `r4()`-formatted — see the
  README's item-19 note on which files are full float and which are not).
- Interpreter: system `python` via the `py` launcher (3.12.10 this session; the night-run venv,
  3.10.20, was not needed — both scripts use only the standard library).
- Inputs read (not modified): raw run jsons in the night scratchpad (`night1_9991-000.json`,
  `rep_9991-900.json`, `night3_9991-003.json`, `rep_9991-903.json`, `night4_9991-005.json`, and
  the three `wave_night4.*` files), `results/night1/night1_9991-000.slim.json`,
  `results/night1/rep_9991-900.slim.json`, `results/night2/night2_9991-001.slim.json`,
  `results/night2/night2b_9991-002.slim.json`, `results/night3/night3_9991-003.slim.json`,
  `results/night3/night3_9991-004.slim.json`.
- Written by: CC's subagent on Sonnet, 2026-09-17. Verified by: CC.
