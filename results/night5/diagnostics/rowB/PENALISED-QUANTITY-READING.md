# Row B free falsifier — the penalised quantity across `stop_iter = 150,000`

> **OFF LIMITS TO A BLIND v2 AUTHOR.** This file contains result values. Under
> `docs/decisions/003-blind-authorship-after-the-numbers.md` (ADR-003), anyone who must author
> a criterion that has not yet been written must not read this file, and must not read
> `results/night5/diagnostics/rowB/penalised_quantity_by_checkpoint.csv`,
> `results/night5/diagnostics/rowB/penalised_quantity.svg` / `.png`, or
> `results/night5/diagnostics/rowB/rowB_records.json`. The protocol
> (`results/night5/diagnostics/rowB/README.md`) and the script (`rowB.py`) stay readable: they
> hold no values.

**Status:** unregistered diagnostic. `status: "unregistered_diagnostic"`,
`readable_as_verdict: false` (`rowB_records.json`, top level, and in every one of the 720
records). **No number below reads as a test.**

**Read once, by CC on Mike's word given 2026-09-20 in the DPC Research chat.**
**Date:** 2026-09-20.
**Scope of this reading:** one quantity and nothing else — the activity penalty's own
pre-weight quantity (`falsifier_penalized_quantity.pre_weight`) and the counts of central cells
below / above baseline. The activity **profiles** (`mean_by_type`, `central_cell_mean`,
`std_by_type`, `last_frame_by_type`, the `_skip_first_quarter` matrices, the per-step `.h5`)
were **not** opened, not summarised and not plotted, and no individual's profile was compared
with another's. That reading has not been approved.

---

**Which column the prose quotes (Johnny, 2026-09-20).** `penalised_quantity_by_checkpoint.csv`
has two value columns, `pre_weight` and `weighted`. Verified numerically (a few rows of the csv)
and from the code (`rowB.py:940`, `flyvis/solver.py:868-883`): `weighted = activity_penalty ×
pre_weight`, with `activity_penalty = 0.1` read from every run's own resolved config and
identical across all 720 records (§2 above). E.g. `9991/000`, checkpoint 0:
`pre_weight = 19.692142334800554`, `weighted = 1.9692142334800555` —
`19.692142334800554 × 0.1 = 1.9692142334800554`, matching to float rounding. The two columns
are the same quantity on two scales; the branch of the reading rule (§1, §4) is identical on
either, since a constant positive multiplier changes no ratio and no sign. **Every number quoted
in this file's prose (§2–§8) is the `pre_weight` column.** `weighted` is `pre_weight` times the
configured penalty weight and is not separately discussed below.

---

## 1. The rule, as it was written before the values

The rule is quoted here from the repository, verbatim, and is applied as written.

**`backlog.md`, entry `ROW-B-EXTRACTION-ON-NIGHTS-4-AND-5-NEEDS-THREE-SETTLED-POINTS-BEFORE-THE-FIRST-VALUE`:**

> **Inferred.** Ark's free falsifier — print the penalised quantity per checkpoint to test
> whether the 150,000 boundary binds — is cheap and should run before the first row-B value is
> read.

**`results/night5/diagnostics/rowB/README.md` §8, "The free falsifier":**

> Ark's: print the **penalised quantity** per checkpoint and see whether the 150,000 boundary
> binds. It is free — the activity is already recorded — and it is a falsifier because the
> penalty is the one thing in the training loop that acts on exactly this axis.

**A discrepancy, stated and not resolved in this file.** The reading was commissioned with a
fuller branch rule, attributed to Ark in the group chat:

> "if the penalty was binding, after 150k the quantity DRIFTS away from baseline; if the
> trajectory is SMOOTH through the boundary, the penalty was not binding, and the backlog card
> about the cheap and the dear estimate living in different regularisation regimes weakens."

**At reading time, the repository's two statements of the rule did not contain the DRIFT /
SMOOTH / AMBIGUOUS branches.** They said what to print and what it was for ("whether the
150,000 boundary binds"); they did not say how the printed trajectory is read into a branch.
The instruction for this session was to quote the repo's wording and apply the repo's. The
repo's wording is applied — it fixes the question ("does the boundary bind?") and the quantity
— and the chat's branches were used **only as the labels this reading was asked to assign**,
marked as such wherever they appear below. Where a run's behaviour is not covered by either
branch as worded, it is reported as **ambiguous under the rule as written**, and **no threshold
is invented to resolve it.**

**Since recorded in the repository.** The three-branch wording (DRIFT / SMOOTH / AMBIGUOUS), as
Ark wrote it down on 2026-09-20 21:43 local — after this reading, to record the rule as it was
applied — now lives in `results/night5/diagnostics/rowB/README.md`, "How the quantity is read
across the 150,000 boundary (rule)" (under §8). That section carries the honest provenance line
and both the Russian original and an English rendering. This paragraph's observation stands
unchanged: at the time this file was written, the repo held only the question and the quantity,
not the branches.

---

## 2. Observed — what was read, and from where

**Source:** `results/night5/diagnostics/rowB/rowB_records.json`, 720 records = 10 runs × 72
checkpoints, produced 2026-09-20. Field read per record:
`falsifier_penalized_quantity.pre_weight`, `.n_central_below_baseline`,
`.n_central_above_baseline`, `.n_central_at_baseline`, `.n_cells_total`, together with
`run.chkpt_iter`, `run.side_of_stop_iter` and the run-identity block.

**Tidy extract written:** `results/night5/diagnostics/rowB/penalised_quantity_by_checkpoint.csv`
(720 rows).

**The quantity.** `rowB.py:837-879` recomputes `flyvis/solver.py:868-883`:

```
pre_weight = (asymmetric_weighting(baseline − central_cell_mean_skip_first_quarter,
                                   below_w, above_w) ** 2).mean()
weighted   = activity_penalty * pre_weight
```

**Constants, read from each run's own resolved `_meta.yaml`** (`constants_source` in every
record), and **identical across all ten runs and all 720 records** (checked, not assumed):
`activity_baseline = 5.0`, `below_baseline_penalty_weight = 1.0`,
`above_baseline_penalty_weight = 0.1`, `activity_penalty = 0.1`, `stop_iter = 150000`.
`weighted = 0.1 × pre_weight` exactly, so only `pre_weight` is tabulated.

**Direction convention.** Larger `pre_weight` = central cells further from the baseline of 5.0;
smaller = closer. The penalty, while active, pushes this number **down**. "Drifts away from
baseline" therefore means `pre_weight` **rises**.

**Run identity.** Ten runs, six individuals (`N` block of `rowB_records.json`):
seed 0 = `9991/000` with replicates `9991/900` (seed 0′) and `9992/000` (seed 0″);
seed 3 = `9991/003` with replicates `9991/903` (seed 3′) and `9992/003` (seed 3‴);
seeds 1, 2, 4, 5 = `9991/001`, `9991/002`, `9991/004`, `9991/005`, one run each.

**Path.** `reduction_path: "gpu"`, `deterministic: false`,
`determinism_mode: "as the nights ran: --no-determinism"`, `activity_mutated: false`,
`floor_k: 1`, `git_head: effaff28c07c1e0c6462d7bfd3c2dbf993e2e000`.

### 2a. The checkpoint grid, and how sharply the boundary can be located

All ten runs share one `chkpt_iter` grid (checked: identical tuple for all ten). 72
checkpoints; the only spacings present are **12** (checkpoint 0 → 1, iters −1 → 11), **3600**
(everywhere in between) and **1596** (the last step, 248,411 → 250,007).

Around the boundary the spacing is **3600**:

| | `chkpt_index` | `chkpt_iter` |
|---|---|---|
| last checkpoint with the penalty still active | 42 | **147,611** |
| `stop_iter` | — | **150,000** |
| first checkpoint with the penalty off | 43 | **151,211** |

So the boundary sits **2,389 iterations after** the last "before" checkpoint and **1,211
iterations before** the first "after" checkpoint. **A step at 150,000 can be localised no more
sharply than to a 3,600-iteration window**, and anything that happens inside that window is
seen only as the single 42→43 difference.

Both iteration conventions agree on the side of every one of the 720 records
(`conventions_agree: true`, 720/720; zero records where `side_by_chkpt_iter` and
`side_by_solver_iteration` differ). 43 checkpoints before, 29 at or after.

---

## 3. Observed — the shape per run

`lastB` = value at `chkpt_iter` 147,611. `firstA` = value at 151,211. `jump` = `firstA − lastB`.
`med|Δ|` = median absolute checkpoint-to-checkpoint change **within the local window** — the
last 10 checkpoints before (115,211…147,611) and the first 10 at or after (151,211…183,611) —
i.e. the run's own typical step size next to the boundary, not over the whole run. `slope`
= ordinary least squares on those same two 10-checkpoint windows, in units of `pre_weight` per
10,000 iterations. `end` = the value at the final checkpoint, `chkpt_iter` 250,007.

| run | netdir | replicate | lastB (147,611) | firstA (151,211) | jump | med\|Δ\| before | med\|Δ\| after | slope/10k before | slope/10k after | end (250,007) |
|---|---|---|---|---|---|---|---|---|---|---|
| seed 0 | 9991/000 | no | 16.2480 | 16.2369 | −0.0111 | 0.0691 | 0.0892 | +0.0013 | −0.0987 | 16.1900 |
| seed 0′ | 9991/900 | yes | 16.8358 | 16.8617 | +0.0259 | 0.0923 | 0.1214 | −0.2437 | −0.1253 | 16.3465 |
| seed 0″ | 9992/000 | yes | 17.6588 | 17.6591 | +0.0003 | 0.3717 | 0.2716 | −0.6190 | −0.1331 | 17.3493 |
| seed 1 | 9991/001 | no | 20.8258 | 20.8445 | +0.0187 | 0.1394 | 0.0760 | +0.1425 | +0.1148 | 21.6184 |
| seed 2 | 9991/002 | no | 16.6147 | 16.6264 | +0.0117 | 0.0739 | 0.0686 | −0.2344 | −0.0182 | 16.3885 |
| seed 3 | 9991/003 | no | 17.5685 | 17.5356 | −0.0329 | 0.0611 | 0.0707 | +0.0121 | +0.0079 | 17.6297 |
| seed 3′ | 9991/903 | yes | 18.7477 | 18.5818 | −0.1659 | 0.0908 | 0.0742 | +0.1262 | +0.0641 | 19.0626 |
| seed 3‴ | 9992/003 | yes | 19.7798 | 19.8675 | +0.0876 | 0.1350 | 0.5934 | +0.0485 | **+7.8295** | **56.7047** |
| seed 4 | 9991/004 | no | 16.6665 | 16.8204 | +0.1539 | 0.1402 | 0.0324 | +0.3284 | +0.0358 | 16.7745 |
| seed 5 | 9991/005 | no | 19.8161 | 19.7800 | −0.0361 | 0.0769 | 0.0984 | −0.8260 | −0.2121 | 18.7549 |

Two further columns, because a 10-checkpoint window is short: the value range the run occupies
**after** 150,000, against the range it occupied **before** 150,000 (checkpoint 0, the
untrained state at `chkpt_iter = −1`, is excluded from the "before" range — all ten runs start
at 19.69–19.76 there, which is the initialisation, not training), and the total movement from
`firstA` to `end`.

| run | before-150k range (excl. init) | after-150k range | `end − firstA` | as % of `firstA` |
|---|---|---|---|---|
| seed 0 | 15.628 – 41.715 | 15.854 – 16.281 | −0.0469 | −0.3 % |
| seed 0′ | 16.818 – 58.627 | 16.314 – 17.002 | −0.5152 | −3.1 % |
| seed 0″ | 16.618 – 129.772 | 17.073 – 18.121 | −0.3098 | −1.8 % |
| seed 1 | 18.348 – 41.932 | 20.844 – 21.631 | +0.7739 | +3.7 % |
| seed 2 | 16.615 – 49.951 | 16.235 – 16.743 | −0.2378 | −1.4 % |
| seed 3 | 16.808 – 45.695 | 17.368 – 17.649 | +0.0940 | +0.5 % |
| seed 3′ | 18.322 – 62.218 | 18.582 – 19.093 | +0.4808 | +2.6 % |
| seed 3‴ | 18.667 – 65.608 | 19.813 – 60.639 | **+36.8372** | **+185 %** |
| seed 4 | 15.648 – 21.924 | 16.775 – 17.107 | −0.0459 | −0.3 % |
| seed 5 | 19.736 – 109.023 | 18.727 – 19.780 | −1.0251 | −5.2 % |

**The jump at the boundary itself (corrected 2026-09-21 — Zcode; see the corrections section,
§10, item (i)).** In **eight of ten** runs `|jump|` is **strictly smaller than the run's own
median step in the ten checkpoints before the boundary** (ratio < 1): 0.00 (seed 0″), 0.13
(seed 1), 0.16 (seed 0, seed 2), 0.28 (seed 0′), 0.47 (seed 5), 0.54 (seed 3), 0.65 (seed 3‴).
The other two both exceed their own local step: seed 4 at **1.10** and seed 3′ at **1.83** —
`jump` −0.1659 against a local median step of 0.0908 for seed 3′, i.e. about twice a typical
step and **in the direction of the baseline**, not away from it. **No run shows a
discontinuity at 42→43 that stands out against its own neighbouring steps** — that reading does
not depend on whether the count of ratios below 1 is eight or nine.

**Counts of central cells below / above baseline** (16 items × 65 types = 1040 cells per
checkpoint; `n_central_at_baseline` is 0 in every one of the 720 records):

| run | 147,611 below/above | 151,211 below/above | 250,007 below/above |
|---|---|---|---|
| seed 0 | 930 / 110 | 933 / 107 | 931 / 109 |
| seed 0′ | 829 / 211 | 837 / 203 | 846 / 194 |
| seed 0″ | 780 / 260 | 775 / 265 | 793 / 247 |
| seed 1 | 969 / 71 | 979 / 61 | 978 / 62 |
| seed 2 | 914 / 126 | 905 / 135 | 881 / 159 |
| seed 3 | 926 / 114 | 921 / 119 | 962 / 78 |
| seed 3′ | 989 / 51 | 978 / 62 | 999 / 41 |
| seed 3‴ | 998 / 42 | 992 / 48 | 870 / 170 |
| seed 4 | 907 / 133 | 904 / 136 | 857 / 183 |
| seed 5 | 1020 / 20 | 1018 / 22 | 959 / 81 |

Across the boundary the counts move by **3 to 11 cells out of 1040** (0.3 %–1.1 %) in every
run. The majority of central cells sit **below** baseline at every checkpoint of every run
(minimum over all 720 records: 661 of 1040). At checkpoint 0 (the untrained state) all ten runs
read 1040 below / 0 above.

### 3a. The one run that moves — and where it moves

Seed 3‴ (`9992/003`) is the only run whose post-boundary trajectory leaves its neighbourhood.
Its per-checkpoint values after the boundary:

| `chkpt_iter` | 151,211 | 154,811 | 158,411 | 162,011 | **165,611** | 169,211 | 172,811 | … | 250,007 |
|---|---|---|---|---|---|---|---|---|---|
| `pre_weight` | 19.8675 | 19.8993 | 19.8128 | 19.8967 | **28.4100** | 32.7216 | 37.6307 | … | 56.7047 |

**The rise does not begin at the boundary.** Four checkpoints — 14,400 iterations — pass at
19.81–19.90, flat, before the jump between 162,011 and 165,611. That jump is **~15,600
iterations after `stop_iter`**, and eight checkpoint grid steps away from it. Its own
`jump` at 42→43 is +0.0876, 0.65 of its local median step.

Two further facts about this run, stated because they bear on how much weight the excursion can
carry: its post-150k maximum (60.639, at 241,211) is **below its own pre-150k maximum** (65.608,
at 25,211); and it had a larger and faster excursion **while the penalty was active**, running
19.4 → 65.6 → 18.7 between iterations 7,211 and 39,611.

### 3b. Three runs that leave their pre-boundary band downwards

Seed 0′, seed 2 and seed 5 spend most of the post-boundary side **below** the lowest value they
reached before it: 26 of 29, 27 of 29 and 28 of 29 post-boundary checkpoints respectively fall
under their own pre-150k minimum (16.818, 16.615, 19.736). First such checkpoint: 158,411
(seed 0′), 154,811 (seed 2), 154,811 (seed 5). The movement is **towards** the baseline —
`end − firstA` = −0.52, −0.24, −1.03. The other seven runs stay inside their own pre-150k
range at every post-boundary checkpoint (0 of 29 outside).

---

## 4. The branch each run falls under

Branch labels as the commissioning wording states them: **DRIFT** = "after 150k the quantity
drifts away from baseline" (→ the penalty was binding); **SMOOTH** = "the trajectory is smooth
through the boundary" (→ the penalty was not binding). Recall §1: these branches are **not** in
the repository's wording of the rule.

| run | branch, applied as written | why |
|---|---|---|
| seed 0 | **SMOOTH** | jump −0.011 = 0.16 of its own local step; end −0.3 % from `firstA`; never leaves its pre-150k range |
| seed 0′ | **SMOOTH at the boundary; AMBIGUOUS thereafter** | jump +0.026 = 0.28 of a local step, but the run then settles 26/29 checkpoints below its pre-150k floor, moving **towards** baseline — a direction the rule's DRIFT branch does not describe |
| seed 0″ | **SMOOTH** | jump +0.0003, the smallest of the ten; end −1.8 %; stays in range |
| seed 1 | **SMOOTH at the boundary; AMBIGUOUS thereafter** | jump +0.019 = 0.13 of a local step, but it is the only run with a sustained positive slope on both sides (+0.14 / +0.11 per 10k) and +3.7 % from `firstA` to `end` — a slow rise that **crosses the boundary unchanged**, so it is movement, but not movement *caused at* 150,000 |
| seed 2 | **SMOOTH at the boundary; AMBIGUOUS thereafter** | as seed 0′: jump 0.16 of a local step, then 27/29 below the pre-150k floor, towards baseline |
| seed 3 | **SMOOTH** | jump −0.033; slopes +0.012 / +0.008 per 10k, essentially flat on both sides; +0.5 % to the end |
| seed 3′ | **AMBIGUOUS at the boundary** | the only run whose jump (−0.166) exceeds its own local step (×1.83) — but it is **negative**, i.e. towards baseline, which is neither the rule's DRIFT (away) nor cleanly SMOOTH. ×1.83 against ×1.10 for the next-largest is a difference of degree, and the rule as written gives no threshold to call it a step |
| seed 3‴ | **AMBIGUOUS — DRIFT in magnitude, not in place** | +185 % from `firstA` to `end` is the only movement in the ten that the word "drifts away" plainly fits. But it starts four checkpoints (≈15,600 iterations) after the boundary, after a flat stretch; its own boundary jump is 0.65 of a local step; and its post-150k maximum stays under its pre-150k maximum. **The rule as written does not say how long after the boundary a rise may begin and still count as the boundary's doing.** Not resolved here |
| seed 4 | **SMOOTH** | jump +0.154 = 1.10 of its own local step, the second-largest ratio, but the slope flattens after the boundary (+0.33 → +0.04 per 10k) and the run ends −0.3 % from `firstA`, inside its pre-150k range |
| seed 5 | **SMOOTH at the boundary; AMBIGUOUS thereafter** | jump −0.036 = 0.47 of a local step, then 28/29 checkpoints below its pre-150k floor, towards baseline; steepest pre-boundary slope of the ten (−0.83 per 10k) flattening to −0.21 |

**Count.** Under the rule as written: **SMOOTH through the boundary — 10 of 10 at the boundary
itself** (no run shows a step at 42→43 that stands out from its own neighbouring steps; the
closest, seed 3′, is 1.83 local steps and points the wrong way for DRIFT). **DRIFT away from
baseline after the boundary — 0 of 10 cleanly; 1 of 10 (seed 3‴) in magnitude but displaced
≈15,600 iterations from the boundary, which the rule does not adjudicate.**

---

## 5. Inferred

**The 150,000 boundary does not bind, in the sense the falsifier was set up to test.** Turning
the activity penalty off at `stop_iter` leaves no mark on its own pre-weight quantity at the
scale this grid can see: in all ten runs the change across the boundary is smaller than — or, in
two cases, of the same order as — the run's ordinary checkpoint-to-checkpoint wandering in the
same region, and in **eight of ten** (corrected 2026-09-21, §10 (i)) it is a strict fraction of
it. Over the whole remaining 100,000 iterations the quantity moves by −5.2 % to +3.7 % of its
boundary value in nine runs, with **no common direction** (four up, six down) — which is what a
quantity that was not being held does, and not what a released constraint does.

**Under the commissioning wording this is the SMOOTH branch, so the backlog card about the
cheap and the dear estimate living in different regularisation regimes weakens.** That is the
most this reading supports, and it is weakened, not closed: this is an unregistered diagnostic
(`readable_as_verdict: false`), the branch labels are not in the repository's own statement of
the rule (§1), and one run (seed 3‴) is left explicitly unresolved.

**What is *not* inferred.** That the penalty did nothing during training. Every run's largest
excursions in this quantity happen **early, while the penalty is active** (pre-150k maxima 21.9
to 129.8, against post-150k maxima 16.3 to 60.6). Seven of the ten runs sit below their own
initialisation value (19.69–19.76 at `chkpt_iter = −1`) by the last pre-boundary checkpoint;
three do not (seed 1 at 20.83, seed 5 at 19.82, seed 3‴ at 19.78). This reading says the
**boundary at 150,000** does not bind; it says nothing about whether the penalty shaped the
first 150,000 iterations, and the instrument here cannot separate "the penalty stopped mattering
well before 150,000" from "the penalty never mattered".

---

## 6. Replicates versus individuals — descriptive only

**No test, no p-value, no ranking.** N = 6 individuals (`rowB_records.json`, `N` block:
`"N_is_counted_in": "individuals; replicate runs of the same seed do NOT enter N"`), and
`README.md` §14 is explicit: *"Do not read row B as a test at N < 8."* What follows is a
description of ten numbers.

Final-checkpoint `pre_weight`:

* individual 0, three runs: 16.1900 / 16.3465 / 17.3493 — **spread 1.159**
* individual 3, three runs: 17.6297 / 19.0626 / 56.7047 — **spread 39.075**
* the six individuals, one canonical run each: 16.1900 / 21.6184 / 16.3885 / 17.6297 / 16.7745 /
  18.7549 — **spread 5.428**, sample SD 2.055

Mean over the 29 post-boundary checkpoints gives the same picture: individual 0 spreads 1.317,
individual 3 spreads 25.588, the six individuals spread 5.285.

**Descriptively: replicates of individual 0 agree with each other more closely than different
individuals do; replicates of individual 3 do not — one of its three runs (seed 3‴) is further
from its own twins than any two individuals are from each other.** With one of two replicate
sets behaving each way, **this reading supports no statement about whether the quantity is an
individual-level property.** It is recorded because it was asked for and because the asymmetry
is the kind of thing a later, registered reading would need to have known in advance.

---

## 7. Caveats carried

1. **Different sample from training's.** The quantity here is computed on the **16 held-out
   items, batch 1, augmentation off**; in training the same reduction ran on **augmented
   training batches of 4** (`flyvis/solver.py:350`; `README.md` §8; the record's own field
   `n_samples_in_training`). The reduction is identical; the stimulus population is not. A
   level difference between this quantity and training's is expected and is not evidence of
   anything.
2. **The frame window.** Row B reproduces the penalty's reduction on `n_frames = 40` recorded
   steps, dropping the first `40 // 4 = 10` — i.e. **steps 10…39 of 40** (`rowB.py:809`,
   `flyvis/solver.py:869-872`; `n_frames: 40`, `n_frames_config: 19` in every record). That the
   *evaluation* window is steps 10–39 of 40 is verified from the code and the records. That
   **training** built its activity tensor on the same step count is **not** verified — it is the
   open backlog entry `THE-SIMULATION-AXIS-AT-EVALUATION-IS-FORTY-STEPS-PER-ITEM-NOT-NINETEEN`,
   whose first step is precisely to check this. Until it is checked, "exactly the penalised
   quantity" is a claim about the formula and the reduction, not about the window's equality
   with training's.
3. **Non-deterministic mode, and an instrument floor.** `deterministic: false`,
   `determinism_mode: "as the nights ran: --no-determinism"` — the nights' own setting
   (`results/night2/diagnostics/diag1_eval_paths.py:90-93`, `tools/night/start_night.ps1:68`).
   Two identical evaluations of one state are not required to agree; the floor on activity
   means is of order **1e-7**. Every difference tabulated here is 1e-2 or larger, so the floor
   does not explain any of them — but it is the reason no digit past the fourth decimal should
   be read as stable, and the reason P1′ fails 628/720 in this run's controls
   (`rowB_controls.json`; tolerance 1e-6, unattainable on this path by construction — `README.md`
   §15 E.3). P0 passes **720/720**; `activity_mutated: false` in all 720 records.
4. **Unregistered.** `status: "unregistered_diagnostic"`, `readable_as_verdict: false`. This
   file is a reading of a preview, not a result of a test.
5. **Grid resolution.** The checkpoint spacing at the boundary is **3,600 iterations** (last
   before: 147,611; first after: 151,211; `stop_iter` 2,389 / 1,211 iterations from them). **A
   step confined to a window narrower than 3,600 iterations would appear here as exactly one
   difference and could not be distinguished in shape from a single noisy checkpoint.** The
   claim "smooth through the boundary" is therefore a claim at 3,600-iteration resolution and no
   finer.
6. **GPU reduction path.** `reduction_path: "gpu"` in all 720 records. The superseded
   three-checkpoint CPU-path outputs of 2026-09-20 in this directory were **not** read and
   nothing here is pooled with them (`README.md` §10, §15 A7).
7. **What was not read.** No activity profile of any kind, and no comparison between
   individuals' profiles. Only `pre_weight` and the below/above counts.

---

## 8. What this does and does not license for `stop_iter`

**It licenses, at most, one statement:** that at 3,600-iteration resolution, on this sample and
this path, **the activity penalty's own pre-weight quantity shows no response to the penalty
being switched off at 150,000** — i.e. the 150,000 boundary does not appear to bind. That
statement carries the branch consequence the commissioning wording names: the backlog card
about the cheap and the dear estimate living in different regularisation regimes **weakens**.

**It does not license changing `stop_iter`.** A different `stop_iter` is a **new series of
training runs**, and gate 7 refuses it on the strength of this file. Nothing here is a
pre-registered test, nothing here was powered to detect the effect it failed to find, and
"no visible response" at this resolution is not "no effect".

**It is not evidence about ranking individuals.** N = 6 individuals; `README.md` §14: *"Do not
read row B as a test at N < 8"*, and *"Six is more individuals, not a test."* The per-run
values in §3 differ between runs; that difference is **not** read here as a property of the
individuals, and §6 shows why it cannot be — one of the two replicate sets disagrees with
itself more than the individuals disagree with each other.

**It does not settle seed 3‴.** The one run that moves does so ≈15,600 iterations past the
boundary, after four flat checkpoints, and stays under its own pre-boundary maximum. Whether
that counts as the boundary's doing is not decidable under the rule as written, and **no
threshold was invented here to decide it.** If someone wants it decided, the criterion must be
written by an author who has not read this file (ADR-003).

---

## 9. Files

| file | what |
|---|---|
| `results/night5/diagnostics/rowB/penalised_quantity_by_checkpoint.csv` | the tidy extract, 720 rows, one per (run, checkpoint) — **holds values** |
| `results/night5/diagnostics/rowB/penalised_quantity.svg`, `.png` | all ten runs, `pre_weight` vs `chkpt_iter`, one hue per individual, replicates dashed, vertical line at 150,000 — **holds values** |
| `results/night5/diagnostics/rowB/PENALISED-QUANTITY-READING.md` | this file — **holds values** |
| `results/night5/diagnostics/rowB/rowB_records.json` | the source, 720 records — **holds values** |
| `results/night5/diagnostics/rowB/README.md` | the protocol, §8 the falsifier — no values |
| `results/night5/diagnostics/rowB/rowB.py` | the script, `penalised_quantity` at `:837` — no values |
| `backlog.md`, `ROW-B-EXTRACTION-…-BEFORE-THE-FIRST-VALUE` | the rule's other statement — no values |
| `docs/decisions/003-blind-authorship-after-the-numbers.md` | why the first four rows are off limits to a blind v2 author |

---

## 10. Corrections after review (Zcode, 2026-09-21 local)

Three corrections. The original wording is kept visible below, alongside the fix, rather than
deleted; the sentences in §3 and §5 themselves are also corrected in place, each pointing back
here.

**(i) "9 of 10 runs' boundary jump is smaller than the run's own typical step" — corrected to
8.** Original wording (§3, before this correction): *"In nine of ten runs `|jump|` is smaller
than the run's own median step in the ten checkpoints before the boundary: ratios 0.00 (seed
0″), 0.13 (seed 1), 0.16 (seed 0, seed 2), 0.28 (seed 0′), 0.47 (seed 5), 0.54 (seed 3), 0.65
(seed 3‴), 1.10 (seed 4). The tenth, seed 3′, is 1.83…"* The file's own printed list already
contradicts its own count: `1.10` (seed 4) is **greater than 1**, i.e. `|jump|` there is
**larger**, not smaller, than the local median step — so the list itself has only **eight**
ratios below 1 (0.00, 0.13, 0.16, 0.16, 0.28, 0.47, 0.54, 0.65), and two runs exceed their own
local step (seed 4 at 1.10, seed 3′ at 1.83). Recomputed independently from
`penalised_quantity_by_checkpoint.csv`, using the **local window** the file itself defines in
§3 (the ten checkpoints immediately before the boundary, ratios of `|jump|` to the median of
their nine consecutive absolute differences): the same eight ratios and the same two exceptions
are reproduced exactly. **"Nine" holds only on a wider window** — e.g. the median absolute
step taken over the **whole run** (all 71 consecutive differences) instead of the local
ten-checkpoint one — under which seed 4's own step size grows (its run has larger early
excursions) enough to bring its ratio under 1 in some window choices; but that is not the window
§3 defines and uses for the other nine ratios, and mixing windows inside one count is not done
here. **By the file's own stated metric and window, the count is eight, not nine.** §3 above is
corrected in place.

**(ii) "the 150,000 boundary is the smallest of the nine 25,000 boundaries" — true for the
median of `|Δ|`, not for the absolute value of the signed median.** This claim, as stated in
`backlog.md` (`THE-CHEAP-AND-THE-DEAR-ESTIMATE-ARE-TAKEN-UNDER-DIFFERENT-REGULARISATION…`, the
bullet with **2.2332**), already names its metric correctly — **"median `|Δ|`"** — and is
confirmed correct here, recomputed independently from
`results/night5/night_report_checkpoints.csv`:

| metric | value at 150,000 | rank among the nine (1 = smallest) |
|---|---|---|
| median of `\|Δ\|` (Δ = signed change per run at the boundary) | **2.2332** | **1st (smallest)** |
| absolute value of the **signed** median of Δ | **2.2332** (same number here — median Δ at 150,000 happens to be all-positive-sign-consistent) | **4th** |

Full recomputation, both metrics, all nine boundaries (`night_report_checkpoints.csv`,
checkpoint immediately before / at-or-after each boundary):

| boundary | median \|Δ\| | rank | \|signed median Δ\| | rank |
|---|---|---|---|---|
| 25,000 | 8.4490 | 9th | 8.4490 | 9th |
| 50,000 | 3.9945 | 3rd | 1.1549 | 2nd |
| 75,000 | 6.7998 | 8th | 4.3258 | 5th |
| 100,000 | 5.2875 | 4th | 0.6399 | **1st** |
| 125,000 | 5.6189 | 5th | 5.6189 | 7th |
| **150,000** | **2.2332** | **1st** | **2.2332** | **4th** |
| 175,000 | 6.0928 | 6th | 4.5618 | 6th |
| 200,000 | 6.1443 | 7th | 6.1443 | 8th |
| 225,000 | 3.1230 | 2nd | 1.6858 | 3rd |

`tools/atlas/verdicts.json` was checked and does **not** repeat this specific ranking claim (it
states only that no boundary jump stands out, without the "smallest of the nine" figure), so no
edit was needed there. `backlog.md`'s bullet is left as written — it already names "median
`|Δ|`" — no edit was needed there either.

**(iii) "floor k=5" does not apply across all 720 pairs of the full run.** `README.md` §12(4)'s
launch command for the full 72-checkpoint × 10-run run reads `--floor-k 5`, and §6a says "the
owner will run `K = 5`" — but the **actual** full run whose records this file reads used
`floor_k: 1` (this file, §2, "Path": *"`floor_k: 1`"*), i.e. the no-hook floor was taken **once
per pair (K=1)**, not five times. `K = 5` was run for the **three-checkpoint** scope (30 pairs,
`three_checkpoint_gpu_path/`) and for the **three-process floor** of §6 (the single pair
`9992/003` @ checkpoint 71, three fresh processes) — both confirmed from `backlog.md`'s
2026-09-20 CC entry under `ROW-B-EXTRACTION-…`. Inside the full 720-pair run, the floor was
taken once per pair. `README.md` §12(4)'s command is corrected to note this; no sentence in
`backlog.md` claims k=5 for the 720-pair run (it correctly scopes "K = 5" to the three-checkpoint
run only), so no backlog edit was needed for this item.
