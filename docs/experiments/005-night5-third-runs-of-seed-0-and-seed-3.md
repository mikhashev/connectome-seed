# Experiment 005 — night 5, third runs of seed 0 and seed 3

**Ran:** 2026-09-18T21:06:36Z → 2026-09-19T04:59:37Z, both runs `exit: ok`.
**Composition:** `0″` = seed 0 as `9992/000`, then `3‴` = seed 3 as `9992/003`, tag
`night5`, ensemble 9992, 250,000 iterations each, `--no-determinism`, rungs
1000/5000/25000/250000.
**Brief:** `docs/briefs/2026-09-17-night5.md` (v4). **Launched by Mike** after the
pre-flight; CC did not start anything.
**Assembled by:** `results/night5/extract_night5.py`.

This is the first night whose raw artefacts were written **inside the repository** rather
than into a session scratchpad, and the first whose environment lived at `tools/.venv`.

---

## 1. What ran, and what the machine was doing

| | id | start UTC | finish UTC | exit | GPU in use at end |
|---|---|---|---|---|---|
| `0″` | 9992/000 | 2026-09-18T21:06:36Z | 2026-09-19T01:05:36Z | ok | 4,606 MiB |
| `3‴` | 9992/003 | 2026-09-19T01:05:40Z | 2026-09-19T04:59:37Z | ok | 4,607 MiB |

**No reboot, and this is the first night to prove it from the run's own record.**
`machine_state_start` / `machine_state_end` were added to `run_individual.py` on
2026-09-17 and had never been exercised by a run — that was its own backlog entry. All
four records carry `boot_time_utc = 2026-09-14T23:31:12Z`, and `uptime_s` increases
strictly within each run and across the pair (351,263.6 at the end of the first against
351,278.1 at the start of the second). **Both new runs therefore belong to boot session B**,
which is what the degrees-of-freedom arithmetic below depends on.

The card was free: 4,606 and 4,607 MiB in use at the end, inside the 3,720–4,805 MiB band
of nights 1–4. The `llama-server` that held 27.8 GiB earlier that day was stopped before
the launch.

## 2. The result at the top rung

Final aggregate `val_loss` at iteration 250,008, all ten runs
(`results/night5/night_report_checkpoints.csv`, which preserves night 4's nine columns and
all 72 rows byte-identically and adds two):

| run | session | val_loss |
|---|---|---|
| `1` | A | 1144.6362 |
| `0″` | **B** | **1147.4102** |
| `2` | B | 1147.7179 |
| `0` | A | 1148.8075 |
| `3` | B | 1155.7706 |
| `5` | B | 1156.3866 |
| `4` | B | 1156.8285 |
| `3‴` | **B** | **1158.8484** |
| `0′` | A | 1160.9823 |
| `3′` | B | 1163.3766 |

**Within each individual, now three runs each:**

- seed 0: 1147.4102, 1148.8075, 1160.9823 — range **13.5722**, SD(n=3) **7.4653**.
  Pairwise: **|0 − 0″| = 1.3973**, |0′ − 0| = 12.1749, |0′ − 0″| = 13.5722.
- seed 3: 1155.7706, 1158.8484, 1163.3766 — range **7.6059**, SD(n=3) **3.8259**.
  Pairwise: |3‴ − 3| = 3.0778, |3′ − 3‴| = 4.5281, |3′ − 3| = 7.6059.

**Between individuals**, the six canonical first runs: SD **5.2717** (5 df), range
12.1922. Taking an individual as the **mean** of its runs instead gives **5.7332** — a
different estimand, recorded beside it rather than in place of it.

**Pooled replicate SD: 5.9316 on 4 df** (95 % χ² CI **3.5538 … 17.0452**).
**Between-individual SD: 5.2717 on 5 df** (95 % CI **3.2907 … 12.9296**).
**Ratio between / replicate = 0.889.**

### What that does and does not say

**It does not clear the bar.** 0.889 is below 1: two runs of the same individual still
scatter at least as much as six different individuals do. The top rung does not rank
individuals, which is the same conclusion as before — reached now on 4 degrees of freedom
instead of a single pair, and without the normality assumption the earlier σ_rep of 10.26
needed (it divided a single absolute difference by 1.1284). **That is a methodological
upgrade, not a change of answer.**

**And the intervals overlap almost entirely.** 3.55–17.05 against 3.29–12.93. At 4 df the
point estimate carries very little resolution, and nothing here should be quoted without
its interval.

**The result rests on one run of the ten (Ark, 2026-09-19).** Seed 0's three runs are not
evenly spread: two nearly coincide and the third stands off. Dropping `0′` — which is
**not** proposed, since discarding the largest deviation is exactly what one may not do —
would give σ_rep = 3.175 and a ratio of 1.66, reversing the sign. That is a statement about
fragility at n = 3 per individual, where a single heavy point owns the variance, and it is
the reason the next step is more runs or a rank statistic rather than more χ² machinery.

### The seam answered, in the direction nobody expected

For two days the worry was that the 2026-09-14 boot seam would inflate the replicate
spread, and that `0″` — the run crossing it — would be the outlier. The measurement says
the opposite: **`0″` sits 1.3973 from its original, the smallest of seed 0's three
differences, and it is the cross-session one.** The outlier is `0′`, which never left
session A.

Correspondingly the two definitions of replicate noise barely differ: **5.9316 on 4 df**
including cross-session variation against **5.8705 on 3 df** within-session only.

**That measures one of the two questions, and an earlier draft of this paragraph answered
both from it (Ark, 2026-09-19; the numbers below recomputed here).** The two questions are
distinct: whether a cross-session pair adds to the **variance**, and whether the sessions
sit at different **levels**.

- **Variance: measured.** 5.9316 against 5.8705 — admitting the cross-session pair adds
  essentially nothing to the pooled spread.
- **Shift: not measured, and this substrate cannot measure it.** The only estimate available
  is one run in B against the mean of two in A. Its own standard error is
  σ·√(1 + ½) = 5.9316 × 1.2247 = **7.2648**, and the observed
  |0″ − mean(0, 0′)| = |1147.4102 − 1154.8949| = **7.4847** — that is **1.03 σ**. The data
  do not separate a shift of zero from a shift of fourteen. Nor is the small |0″ − 0| =
  1.3973 evidence of agreement: it is one realisation of a quantity whose standard
  deviation is σ√2 = **8.39**.

So the defensible statement is narrow: **the cross-session pair does not inflate the pooled
replicate variance.** Whether the sessions differ in level is open, and a v2 protocol should
not drop the eight cross-seam pairs *on this evidence* — nor keep them on the strength of a
shift estimate that carries one standard deviation of resolution. That is a decision for v2
to make explicitly, not one this night settles.

## 3. Gates

| gate | outcome |
|---|---|
| 1 — `uptime_s` strictly increases | **pass**, within each run and across the pair |
| 4 — the four `s/iter` sub-gates | **`3‴` passes all four. `0″` fails sub-gate 4c** (ratio 1.461 against the band [1.30, 1.45]); see below |
| 6 — `results/night5/` assembled | **done**, this commit |
| 7 — resolved config against nights 1–4 | **pass, both runs**: 162 of 162 invariant lines match; the four varying fields are `ensemble_and_network_id`, `network_name`, `description`, `seed` |
| 8 — environment identity | **pass**: 21,650 files, combined digest equal, nothing differing |
| 10 — degrees of freedom | both runs landed in session B, so the night delivered 2 df on seed 3 inside B and 1 within-session df on seed 0; pooled 4 df including cross-session, 3 df within-session |

### Gate 4, in full, because the failure is informative and the gate is partly at fault

**The instrument question, settled by measurement.** The brief's bands were taken from the
`s/iter` column of the progress log, which is a **rolling mean** of the last 100 iteration
times (`run_individual.py:679-680`). The run json's `iter_wall_s` array supports either
statistic, and the two disagree:

| | plateau | late | ratio |
|---|---|---|---|
| `0″`, log column (rolling mean) | 0.0653 | 0.0447 | 1.461 |
| `0″`, json **mean** | 0.0652 | 0.0447 | — |
| `0″`, json **median** | 0.0644 | **0.0439** | 1.467 |

**The log and the json agree to the fourth decimal once the same statistic is used.** The
0.0439 that appeared in review is the json's *median*; the bands are on a *mean*. So this
is not two instruments disagreeing but one comparison of a mean against a median, and under
the canonical instrument `0″`'s late level is 0.0447, **inside** its band. One sub-gate
fails, not two. (The repository's own `two_phase_price()` in `extract_night4.py` takes
medians of `iter_wall_s`, which is why both conventions are in circulation; they answer
different questions and neither is wrong.)

**What actually moved.** Both new runs are faster in the late phase than all eight earlier
runs — 0.0447 and 0.0448 against a previous minimum of 0.0457 — while their plateaus go in
opposite directions: `3‴` at 0.0630 is below all eight, `0″` at 0.0653 above all eight. The
phases are not coupled, and the ratio is their quotient, so it has a wider spread than
either band. `0″` happened to sit at both extremes at once.

**Three reasons the failure is not read here as voiding the pair** — the disposition is
the group's, not this record's:

1. **The gate fired in the direction it was not built for.** It exists to catch contention,
   and contention makes runs *slower*. Both of these were faster.
2. **The ratio is a derived quantity, not a third independent sentinel.** The two level
   bands alone permit ratios from 1.263 to 1.506, so a run can pass both levels and fail
   the ratio. Three sub-gates were taken from the same eight runs and then applied as if
   independent.
3. **Timing does not enter the science.** It was a proxy for "the same environment", and
   gate 7 answers that question directly: 162 of 162 invariant config lines match.

**And the honest reading of the bands themselves:** they were set from eight observations,
and the two new runs landed at the edges in *opposite* directions. The bands described a
sample, not a property — the same error as an SD taken over three seeds, one level down, on
the instrument instead of the science.

## 4. Provenance

- Raw: `tools/night/night5_9992-000.json`, `tools/night/night5_9992-003.json`,
  `tools/night/wave_night5.json`, `tools/night/wave_night5.progress.log` — written next to
  the launcher and gitignored by name; this record and `results/night5/` are what put the
  night into history.
- Assembly: `results/night5/extract_night5.py`. Its slim-json key check is narrowed rather
  than dropped: exactly `machine_state_start` and `machine_state_end` may be new against
  the night-4 reference, and a missing key still fails.
- **Run → column is an explicit mapping, `results/night5/run_columns.csv`, and must not be
  derived from a column name.** The first version of this file proposed a grammar —
  "`val_loss_seed<N>` followed by k `prime` tokens is the (k+1)-th run of seed N" — which is
  true of `val_loss_seed0primeprime` and **false** of `val_loss_seed3primeprimeprime`: three
  prime marks, but still the third run. The cause is our own notation, where `0″` and `3‴`
  both mean "third run" while carrying two marks and three; the names copied the marks, the
  rule spoke of the order, and they coincided for the first case only — a rule validated by
  its first instance and broken by its second (Ark, 2026-09-19). No number here was
  affected, because `extract_night5.py` maps runs to columns from a table and never from a
  name. But a v2 resolver built on the grammar would have given seed 3 a fourth run it does
  not have, a pooled df of 5 instead of 4, and one degree of freedom of claimed power for
  nothing. The eight night-4 names are unchanged, and the frozen v1 reading script is
  unaffected — it reads night 4's file by a pinned hash and never looks here.
- Independent checks of the same artefacts by Ark and Zcode are in the DPC Research group,
  2026-09-19.

## 5. What this record does not do

It does not reformulate ADR-002, does not choose between road A and road C, and does not
settle the disposition of gate 4. The (c)4 reading of 2026-09-18 returned `TEST UNREADABLE`
and licenses nothing by itself.

**And the "before" figure needs its estimator named, or the improvement is overstated.**
Measured on *the same* estimator that produces 0.889 — a pooled within-individual SD — the
ratio before this night was **0.734** (σ_rep = 7.1777 on 2 df, from the two twin pairs
alone). The figure **0.489** that has been quoted as the "before" comes from the
**range-based** σ_rep, |0′ − 0| divided by d₂ = 1.1284, which gives 10.7895; that estimator
was retired precisely because it assumes the difference is a draw from a normal. Quoting
0.49 → 0.889 compares two different estimators and makes the night look about three times
more decisive than it was.

So, stated properly: **on one estimator the ratio moved 0.734 → 0.889, and the degrees of
freedom moved 2 → 4.** The second is the real purchase; the first is still **below 1**, and
its 95 % interval overlaps the between-individual interval almost entirely.
