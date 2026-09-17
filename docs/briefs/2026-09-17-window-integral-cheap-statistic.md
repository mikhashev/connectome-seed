# Window-integral cheap statistic — pre-launch brief

**v1.1.** **Launch confirmed by Mike in the chat, 2026-09-17 08:19:01Z («#247 да», answering
CC's 08:18:06Z question); reviewer pass by Ark 08:27:19Z and Zcode 08:28:59Z on this brief,
both green with additions (folded in below, §8); launch after that pass.**

**Status:** v1.0 was DRAFT, text only — no analysis script run, no number computed, no GPU
used. v1.1 folds in the reviewers' additions, still before any number is computed. Question:
Ark 07:36Z / Zcode 07:43Z, DPC Research chat. Written from the run jsons and repository
records only (§1 lists exactly what was read).

## 1. Why C3 (hook at 25,000) is in question

Run 703 (`results/diagnostics/c3/partA/jitter_9991-703.json`, dense hook reads, 20k–26k
step 100/25) sits on a steep descent at 25,000: plateau ≈1204–1208 until ~17,000, descent
from ~18–20k, slope ≈ −0.0033/iteration in 24–26k (reading (a), `readings.json`), local
read-noise residual sd ≈ 1.8–2.2 around the fitted trend (readings (a)/(a′)). A point value
at a fixed iteration ranks runs partly by *phase of descent*, not only by where the descent
has settled. Candidate fix: replace the point with a mean over a window spanning the
descent (e.g. 20k–30k), before this is proposed for registration.

## 2. What is on record (read, not computed)

Full runs to iteration 250,008 (`checkpoint_metrics` every 3,600 iterations: 0, 12, 3612,
7212, …; `rung_metrics` = hook value at exactly 1,000 / 5,000 / 25,000 / 250,000): seed 0
(`night1_9991-000.json`), seed 0′ replicate (`rep_9991-900.json`), seed 1
(`night2_9991-001.json`), seed 2 (`night2b_9991-002.json` — the completed re-run; the
earlier `night2_9991-002.json` is the run killed at iteration 12,700 by a Windows Update
restart and is excluded from N under the resume rule, §7 of the pre-registration), seed 3
(`night3_9991-003.json`), seed 4 (`night3_9991-004.json`), seed 3′ replicate
(`rep_9991-903.json`), seed 5 (`night4_9991-005.json`) — **8 full runs**: individuals
0–5 (n = 6, the registered (b) population) plus replicates 0′ and 3′ (not individuals,
§7's instrument-noise pair). `train_loss_per_iter` (per-iteration training loss on
augmented batches, sd ≈ 680/batch, mean ≈ 1283 near the end) exists for all 8.

One partial/diagnostic run: 703 (`jitter_9991-703.json`), seed 3, same schedule and
scheduler as the full runs, dense hooks 20k–26k plus a coarser 1k-step grid to 26,000,
checkpoints at 0, 12, 3612, …, 21612, 25212 — **stops at iteration 26,000, so it has no
28,812 checkpoint and no 250,000 hook.** It is treated here as a third throw of seed 3
(with 003, 903) only for the within-seed comparison in §5, never as an individual of N.

## 3. Data limits — state plainly before choosing a statistic

- The checkpoint grid inside a 20k–30k window gives only **21,612 / 25,212 / 28,812** —
  3 points per run — not a dense window mean. "Window mean on stored checkpoints" is a
  2–3-point mean, not an integral.
- 703 lacks 28,812, so any window statistic built from checkpoints and including 703 is a
  **2-point mean for 703** against a 3-point mean for the other 7 runs, unless the window
  is narrowed to what 703 has (≤25,212) or 703 is excluded from that statistic.
- Checkpoint validation loss and the evaluation-hook value are the same quantity (bit-equal
  at iteration 12 in the dry run, §6 of the pre-registration) but sampled on **different
  iteration grids** — the hook is read at exactly 25,000, checkpoints land at 25,212 etc.
  A checkpoint-window statistic is therefore not directly the same measurement as the
  registered C3 point value; the two differ by construction, not only by averaging.
- No replicate-difference floor exists yet for any window statistic. §7 of the
  pre-registration gives the replicate floor only for the *hook* at 25,000 (0.3365) and at
  250,000 (12.7279), from run 0/0′ and (per the c3 diagnostic) run 703 vs 003/903 at
  25,000. A window mean would need its own floor, not this one inherited (checklist rule 8,
  R1: floor per metric, no inheritance).
- Intermediate-iteration GPU re-evaluation of stored checkpoints does not exist: only the
  iterations actually checkpointed (every 3,600) have a stored network state to evaluate.
  There is no way to get, e.g., a value at 22,000 from the stored checkpoints without a new
  dense run like 703.

## 4. Options for reviewers

**(A) Checkpoint-window mean, stored data only.** Mean of the 3 checkpoints in 20k–30k
(21612/25212/28812), or the 5 checkpoints in 18012–32412, computed per run. For the 7 runs
that reach 28,812 this is a genuine, if coarse, multi-point mean; 703 is either excluded
from this statistic or included using only its own available checkpoints (a narrower,
non-matching window) — report both ways if 703 is included at all, never silently pick one.
**(v1.1, Ark 08:27:19Z): (A) is not interpretable without (C) — for every run, report where
the window (20k–30k or 18012–32412) lies relative to that run's own descent-onset estimate
(§4(C)). A and C are read together: a window mean is a different number depending on whether
it sits before, straddling, or after the run's own onset, and (C) is what says which.**

**(B) Train-loss window mean.** `train_loss_per_iter` averaged over the same window, for
all 8 runs including 703 (dense per-iteration, no gap). This is **train loss on augmented
batches, not held-out loss** — a different quantity from C3 and from (A), with its own much
larger per-batch sd (≈680). Usable, if at all, only as a **descent-onset marker** (where the
train curve bends), not as a substitute ranking statistic for (b) — do not present a
train-loss window mean as commensurate with the registered held-out metric.

**(C) Descent-onset estimate.** The iteration at which the checkpoint or hook series first
crosses a fixed level (e.g. 1,200), estimated from the available points (dense for 703,
sparse — 21612/25212/28812 — for the other 7). This is a **separate quantity** (a location,
not a loss value) and is presented as a candidate diagnostic alongside the window mean, not
as a replacement for either C3 or the window statistic.

**(D) Dense GPU re-evaluation.** Not possible from stored checkpoints for iterations that
were never checkpointed. A dense re-run (like 703, but for other seeds) is a **separate
launch**, out of scope for this brief and not proposed here.

## 5. Pre-registered comparison, before any number is computed

- **Statistics to compute (CPU, from stored json only):** (A) the checkpoint-window mean at
  two window widths (20k–30k, 3 pts; 18012–32412, 5 pts) for the 7 runs with a 28,812
  checkpoint, and separately for 703 on its own available window; (B) train-loss window mean
  over the matching iteration range, all 8 runs, reported but not compared to (A)/C3 on the
  same axis; (C) descent-onset iteration at level 1,200, all 8 (703 dense, others by
  linear interpolation between checkpoints).
- **Within-seed vs between-individual spread:** sd of the within-seed set for seed 0
  ({000, 900}, n = 2) and for seed 3 ({003, 903, 703}, n = 3), each compared descriptively
  to sd of the n = 6 individuals (seeds 0–5) at the same statistic. **n = 2 and n = 3 are
  too small for any test; this comparison is descriptive only**, reported as numbers and a
  direction (smaller/larger than the point-value spreads), never as a pass/fail gate
  (checklist rule 17b: no single-run threshold; rule 17d: state whether "a correct surrogate
  fails this comparison" is even answerable at these n — if it is not, say so instead of
  computing a verdict).
- **(v1.1, Ark 08:27:19Z) Shifted-window rank stability — a direct test of the mechanism.**
  Three checkpoint-grid windows, each 3 points, each shifted by one checkpoint interval
  (3,600 iterations) from the last: **W1 = {18,012, 21,612, 25,212}**,
  **W2 = {21,612, 25,212, 28,812}** (identical to §4(A)'s narrow 20k–30k window),
  **W3 = {25,212, 28,812, 32,412}**. Computed for the n = 6 individuals (seeds 0–5); 703 has
  all three points of W1, only {21,612, 25,212} of W2 (2-point mean, reported as such), and
  only {25,212} of W3 (a single point, not a mean — reported, not silently dropped, never
  averaged as if it were three). For each pair of the three windows, report the rank order of
  the six individuals under each window and the Spearman ρ between the two rankings
  (descriptive, n = 6, no critical value — same rule as §5's ρ below). Stability is read from
  the three pairwise ρ values and from eyeballing whether the same individuals swap ranks,
  not from a single number.
- **(v1.1, Ark 08:27:19Z) Run 703 calibrates the coarse grid.** Estimate 703's descent-onset
  (§4(C), level 1,200 crossing, linear interpolation) twice: once from its dense hook reads
  (`rung_metrics`, 139 points, 1,000–26,000) and once from the checkpoint-grid-like subsample
  of its reads — 703's own `checkpoint_metrics` (0, 12, 3,612, 7,212, 10,812, 14,412, 18,012,
  21,612, 25,212), the same grid the seven full runs are read on. Report the difference
  between the two onset estimates. **If they disagree by more than one checkpoint interval
  (3,600 iterations), mark §4(C)'s onset estimate on the seven full runs as unreliable** — it
  is read from the same coarse grid 703's subsample uses, with no dense reads to check it.
- **Ranking agreement with the top rung:** Spearman ρ between the window statistic and the
  hook at 250,000, over seeds 0–5 (n = 6), reported as a descriptive number with no critical
  value applied — **this is not the registered (b) test** (§4 of the pre-registration; that
  test is defined at C3, with its own N rule, critical values and Holm correction, and is
  not re-run here at a different N or a different statistic). Do not present this ρ with a
  p-value, a "reject/fail to reject" label, or any language implying a test was performed.
  **(v1.1, Zcode 08:28:59Z): at n = 6 neither this ρ nor the difference between two such ρ
  values (e.g. window ρ vs point ρ, or the pairwise ρ of §5's shifted-window comparison) has
  resolution — the pre-registration's own table (§4) gives the critical ρ at n = 6 as 0.829,
  and no correlation coefficient below that is distinguishable from chance at this N. Wherever
  this brief or its outputs say a ρ is "not lower" than another, that sentence means "did not
  visibly fail" — a description of the number seen, not a claim of statistical resolution.
  Say this plainly next to every ρ comparison, not once and then dropped.**
- **Promotion criterion, fixed now:** the window statistic becomes a *candidate for the next
  registration* only if, on this same recorded data, (i) its within-seed spread (both the
  n=2 and n=3 sets) is reduced relative to the point-value's within-seed spread at the same
  seeds, **and** (ii) its ρ with the 250,000 hook (n=6, descriptive) is not lower than the
  point value's ρ with the same target. Either condition failing, or condition (i) holding
  only for one of the two within-seed sets, means **not a candidate as proposed** — report
  which condition failed and by how much, not a single verdict word. No threshold here is a
  single-run number: both comparisons pool the existing n=2/n=3/n=6 sets, and the margin
  between window and point statistic is reported alongside the spread itself, not as a bare
  pass/fail. **(v1.1, Ark 08:27:19Z): "reduced" is fixed as a named factor before any number
  is seen — condition (i) counts as satisfied only if sd(window) ≤ 0.5 × sd(point at 25,000),
  and this must hold for BOTH the seed-0 pair ({000, 900}, n = 2) and the seed-3 trio
  ({003, 903, 703}, n = 3) independently. "Visibly smaller" is retired; report the ratio for
  each of the two sets and whether each clears 0.5, not an impression.**

## 6. Cost and do-not

**Cost:** CPU seconds reading and parsing existing json (largest file ≈8.7 MB); no GPU, no
new training, no new checkpoint.

**Do not:** no GPU; no writes to `connectome-seed-data`; no change to
`docs/preregistration-cheap-vs-expensive.md`; no ρ reported as a test, a p-value, or a
reject/accept decision; no numeric gate built from a single run (checklist rule 17); no
promotion of the window statistic to a registered rung without a separate pre-registration
step, written before any of its numbers are seen twice.

## 7. Next step, named but not run here

**(v1.1, Zcode 08:28:59Z):** the onset-aligned window — a window shifted to sit relative to
each run's own descent-onset estimate (§4(C)), rather than at the same fixed iterations for
every run — is named here as the next step after this brief's computation, not computed in
it. It is conditional: it is only worth building **if §4(C)'s onset estimate is marked
reliable** by the 703 calibration in §5 (the dense-vs-checkpoint-subsample onset difference
at or under one checkpoint interval). If §5 marks C unreliable on the seven full runs, the
onset-aligned window has no reliable onset to align to and stays unbuilt pending a denser
read.

## 8. Revision history

- **v1.0, 2026-09-17, CC.** Initial draft, written from run jsons and repository records
  only; no analysis script run, no number computed. Reviewed by Ark (07:36Z question,
  08:27:19Z pass with additions) and Zcode (07:43Z question, 08:28:59Z pass with additions).
- **v1.1, 2026-09-17, CC.** Folds in the reviewers' additions before any number is computed:
  Ark (08:27:19Z) — §4(A) read together with §4(C); the shifted-window rank-stability test
  (§5, exact windows W1/W2/W3) as a direct test of the mechanism; run 703's dense-vs-subsample
  onset calibration and its unreliable-mark rule (§5); the "visibly smaller" criterion
  replaced by the named factor sd(window) ≤ 0.5 × sd(point) on both within-seed sets (§5).
  Zcode (08:28:59Z) — the onset-aligned window named as the conditional next step (§7); the
  n = 6 resolution statement for ρ and for differences between two ρ values (§5).
