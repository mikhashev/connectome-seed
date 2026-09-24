---
**Status:** registered, not yet run. Drafted by a CC subagent; branch logic checked and corrected by CC before commit (§6 rows and exhaustiveness, §6 consistency paragraph, §9 branch-A wording; worker function made picklable in the script). Written by CC (subagent), 2026-09-24 UTC, on
Mike's brief (step 2 of `docs/notes/2026-09-23-rule-2-1-c6-what-it-showed.md` §8: "The BF_1 P3
attribution run: proposed, not run."). This file must be committed before
`results/genome/c6/checks/bf1_p3.py` is run (same discipline as
`docs/plans/2026-09-23-n1-alone-check-registration.md`, its nearest precedent). **No P3(BF_1)
value of any kind exists anywhere at the time this file is written**, and this script's author did
not run the script beyond a real-bank-only smoke test that reproduces a value that is already
public (§10).
---

# Registration: P3 of BF_1 alone, "as a rule", on C6

## 0. Question and why it is asked now

Rule #2.1's existence term is `N1 + rank-1 bilinear term (BF_1-shaped) + field-group terms X`
(the rule's proposal, `docs/plans/2026-09-23-second-rule-proposal.md` §2.2). Its C6 record shows
P3 existence separating: real margin over N1 +0.033776, 0 of 99 shuffled banks doing as well
(`results/genome/c6/rule_runs/second_rule_v21_r1/result.json`, `exam.P3.existence`). The open
question (Johnny, in the outcome note's §4): **does that separation come from the rank-1 part
alone, or does it need X?**

The committed record holds only a *proxy* for this: the P3 existence row of the control
`"real/RP_r8 as a rule (seed 999)"` in `results/genome/c6/harness_controls.json`
(`n_shuffled_ge_real` 62, p = 0.63 — does not separate). But RP_r8 is **rank 8** and a **random**
projection, not the **trained rank-1** term inside rule #2.1. This run tests the trained object
directly: BF_1's own P3, on the same 99 shuffled banks.

## 1. Exactly what "BF_1" is

**Object:** `harness.bf_predictor(1)`, i.e. `Predictor("BF_r1_k{STARTS}", BF_FILES, lambda v:
fit_bf(v, 1), rank=1)` (`results/genome/c6/harness.py` lines 734–735). This is the identical
Python object the harness itself built for `exam.P4.bf` in rule #2.1's run — same function, same
`r = 1`, same global `STARTS`. It is not a separate reimplementation.

- **Program (charged decode):** `BF_FILES = [DEC / "n1_decode.py", DEC / "bf_decode.py"]`
  (harness.py line 532). `bf_decode.py` calls `n1_decode.decode` for everything (offsets, sign)
  and only overrides `p_exist` by adding a rank-1 bilinear term to N1's own existence logit:
  `z = n1_decode.logit(data, cells) + sum(bf_U[s] * bf_V[t])` (`decoders/bf_decode.py` lines
  8–13). **BF_1 changes only the existence field's prediction; its offsets and sign are byte-for-byte
  N1's**, because `fit_bf` starts from `n1 = fit_n1(view)` and only `.update()`s three new keys
  (`bf_U`, `bf_V`, `bf_lambda`) onto N1's own fitted dict (harness.py lines 710, 730). This
  answers item 3 below.
- **Fit (`fit_bf`, harness.py lines 710–731):** fits N1 first (Newton, deterministic, no RNG).
  Builds the observed grid `Y`/`M` from the training cells. For each of the rule's own 10 CV
  folds it does a **nested** choice of λ: for each of the 10 inner folds (`inner_folds`, from the
  fixed `FOLD` column of `folds.csv` — no RNG), it fits rank-1 ALS (`bf_als`) at every
  `λ ∈ BF_LAMBDAS = [1, 3, 10, 30, 100]` on the other 9 inner folds and scores held-out
  log-likelihood on the held-out inner fold; the λ with the best summed held-out log-likelihood
  wins (ties go to the larger λ). It then refits at that λ on the full training set.
- **Rank:** `r = 1`, fixed by the call `bf_predictor(1)`, not derived — this is the same `r = 1`
  that rule #2.1's `exam.P4.rank` recorded (A11's rank formula gave `r = 1` for the rule; BF_1 is
  requested at that same rank by construction of P4, harness.py line 1027 `bf_margin(r, bank)`
  with `r = rank_of(pred, full_data)` for the rule, which equals 1 here).
- **Starts (`bf_als`, harness.py lines 666–689):** `k = STARTS`. `STARTS = 10` is the harness
  module's default (line 539) and the value `--controls` and rule runs use unless overridden by
  `--starts 3`; rule #2.1's run used `--starts 10` (`ATTEMPTS.md`, timing decision), and
  `exam.P4.bf.margin` was computed at `stamp.starts_k = 10`
  (`second_rule_v21_r1/result.json`). Start 0 of the 10 is the SVD start of the residual
  `Y - sigmoid(O)`; starts 1–9 perturb it with fixed seeds `PCG64(30000 + j)`, `j = 1..9`
  (`PERTURB_SEED_BASE = 30000`, harness.py line 540); the best start by the **training**
  objective wins the fit (ties to the lower `j`). None of this is run-to-run random: the seeds
  are literal constants in the code, not derived from any external seed argument.
- **Seeds used, in total:** none are new. `PCG64(30000 + j)` for `j = 1..9` (BF's own internal
  restarts, fixed in the code) and the 99 shuffle seeds `0..98` (§2). **No seed from the reserved
  ranges (60000/61000/70000–70999/80000–80999) is touched.**
- **CV folds:** the same outer 10 folds as everywhere else in the exam (`FOLD` from
  `results/genome/c6/folds.csv`, `N_FOLDS = 10`), and the same inner 10 folds for λ's nested
  choice (`inner_folds`, the same `FOLD` column restricted to the training view).
- **Determinism:** every step above is either closed-form (N1's Newton fit), a fixed grid search
  with no RNG (λ), or ALS from fixed-seed starts. Given the same bank and `STARTS = 10`, `fit_bf`
  returns bit-identical output on every run. This is the basis for the tolerance in §5.

**This is the same BF_1 that produced `exam.P4.bf.margin = 0.028150051052145946`** in
`second_rule_v21_r1/result.json` (rank 1, `stamp.starts_k = 10`, `P4.bf.lambdas` all 1.0). §5's
machine check verifies this identity numerically before anything else is read.

## 2. Exactly which banks

The real bank (`harness.REAL`) and its 99 degree-preserving shuffles, built by
`harness.shuffled_bank(REAL, sd)` for `sd in range(99)` (`N_SHUFFLES = 99`, harness.py lines
907–921). These are **the same banks and the same seeds** P3 uses inside any C6 run
(`make_env`, harness.py lines 1224–1232, called from `rule_run`; `controls()` calls the same
`make_env` for the "as a rule" controls, e.g. `"real/RP_r8 as a rule (seed 999)"`). The seed set
does not depend on which predictor is scored — it depends only on the base bank (`REAL`) — so
BF_1 faces the byte-identical 99 banks rule #2.1 faced.

**No new randomness is needed anywhere in this run.** Seed discipline (60000 burned, 61000 ST0,
70000–70999 diagnostic, 80000–80999 reserved) is untouched; this run draws no seed from any of
those ranges and needs none, since both BF_1's fit and the shuffle banks are already fully pinned
by existing code paths.

## 3. Fields: existence yes; offset, counts, sign apply only trivially

- **Existence is the substantive field.** BF_1's decode overrides only `p_exist` (§1). Its
  existence margin over N1 is a real, non-trivial quantity — the same one already measured at
  +0.028150 in-sample-selected (held-out, mean over 10 folds) on the real bank.
- **Offset does not apply.** `bf_decode.decode` returns `out["offsets"]` and `out["sign"]`
  unchanged from `n1_decode.decode(data, ...)` (`decoders/bf_decode.py` line 9), and `fit_bf`
  never touches the offset-library or sign fields of the dict it inherits from `fit_n1`
  (harness.py lines 710–711, 730). So BF_1's offset/sign/counts scores on **any** bank are
  bit-identical to N1's own scores on that bank, by construction — not approximately equal, not
  usually equal, but the same floating-point values, because the decode function computes them
  from the same stored data with no BF-specific branch. Consequently BF_1's margin over N1 on
  offset, counts and sign is exactly 0.0 on every bank, real or shuffled, and BF_1's P3 on those
  three fields would read `n_shuffled_ge_real = 99`, `p = 1.00`, the same "by construction" row
  the registered "N1 as a rule" control already shows in `harness_controls.json`
  (`controls["real/N1 as a rule"].P3` — real margin 0 on every field, since N1 vs N1 is trivially
  a tie everywhere it is not existence). **These three fields are computed and reported for the
  record (so a reader can see the zero directly, not just take this paragraph's word for it), but
  they carry no reading and settle nothing.** Existence is the only field this registration reads.
- P4's tie band / threshold logic does not apply here: this run has no P4 arm of its own (BF_1 is
  not being compared to a threshold it would set against itself). Only P3 is run.

## 4. What is reported: three numbers, not a band

For the real bank and for each of the 99 shuffled banks, `existence_margin = margin(cv(BF_1,
bank), cv(N1, bank), "existence")`, using `harness.cv` and `harness.margin` unmodified (the exact
functions P3 uses inside `run_exam`, harness.py lines 744–750, 519–523). The summary reports, in
this order:

1. **`real_margin`** — BF_1's held-out existence margin over N1 on the real bank (must match
   `exam.P4.bf.margin`, §5).
2. **`shuffled_mean`** — mean of the 99 shuffled margins.
3. **`shuffled_max`** — max of the 99 shuffled margins.
4. **`n_shuffled_ge_real`** — count of shuffled margins ≥ `real_margin` (existence is
   lower-is-better as a raw score, but `margin` is already signed so larger = better regardless
   of field direction, matching harness.py's own convention; "≥" here means "at least as good a
   margin").
5. **`strictly_above_all`** — `all(real_margin - m > TAU for m in shuffled_margins)`, `TAU =
   1e-9`, the identical condition `r3["existence"]["strictly_above_all"]` uses (harness.py line
   1020).
6. **`p_one_sided = (1 + n_shuffled_ge_real) / (1 + 99)`**, the same formula `rule_run` uses for
   `P3_p_values` (harness.py lines 1634–1635).

No single number stands in for the other five; the script's summary and `RESULT.md` print all
six before any reading is stated.

## 5. Machine check, run and read before anything else

**Before any shuffled bank is scored**, the script fits BF_1 on the real bank only, computes
`real_margin`, and checks

```
abs(real_margin - 0.028150051052145946) <= 1e-9
```

against `exam.P4.bf.margin` of `results/genome/c6/rule_runs/second_rule_v21_r1/result.json`
(the value the script reads from that file at start, not a copied literal, so a future edit to
that record is caught). **Tolerance justification:** `fit_bf` is fully deterministic given the
bank and `STARTS` (§1); both this run and the recorded one use the real bank at `STARTS = 10`, so
the two numbers should be **bit-identical** in exact arithmetic. `post_run.py`'s own reproduction
checks (`results/genome/c6/rules/second_rule_v21/post_run.py` line 295,
`abs(bf_margin[1] - e["P4"]["bf"]["margin"]) <= EXACT` with `EXACT = 1e-12`) use the same
reasoning for the same object. This registration uses `1e-9` (`harness.TAU`, one order looser
than `post_run.py`'s `1e-12`) only to absorb machine-order-dependent floating-point summation
differences between a fresh process and the original run (different worker counts, different
NumPy BLAS call order in `np.linalg.svd`/`np.linalg.solve`); it is not a concession on identity of
the underlying computation.

**If the check fails, the script writes and prints that failure as the first line of its output,
including both numbers and the difference, and stops. It does not compute or print any shuffled-bank
number in that case.** A failing check means the "BF_1" reproduced here and the "BF_1" inside
`exam.P4.bf` are not the same object in practice, and that mismatch must be resolved (most likely
a `harness.py` change since the run, checked by the sha assert in §8) before any shuffle number is
worth reading.

## 6. Outcome branches, exhaustive and non-overlapping

Applied to **existence only** (§3). Uses the harness's own P3 criterion
(`strictly_above_all`, §4.5) as the formal branch condition, and Ark's "reading by distance"
(`gap = real_margin - shuffled_max`) as a second, plain-language reading of the same run. **The
formal branch governs the verdict; the distance reading is reported alongside it and is designed,
by the cut points below, never to contradict the formal branch** — see the consistency argument
after the table.

| branch | formal condition (harness's own P3 criterion, on existence) | distance reading | meaning | what the second brain (FlyWire) then tests |
|---|---|---|---|---|
| **A. BF_1 separates** | `n_shuffled_ge_real = 0` and `strictly_above_all` true | `gap` near BF_1's own real margin (≈ +0.027, i.e. `shuffled_max` near the rule's measured shuffle bound of +0.0008) | The rank-1 part **alone suffices** to separate: it finds structure the shuffle destroys. This run does **not** test whether X alone would also separate, so it does not say X contributes no separation; it says the rule's separation does not *need* X. | Is the **rank-1** structure (a low-dimensional per-type interaction) bank-specific — does it survive on a second, independently reconstructed brain? |
| **B. BF_1 does not separate** | `p_one_sided ≥ 0.05`, i.e. `n_shuffled_ge_real ≥ 4` (cut justified below) | `gap` near 0 or negative, i.e. `shuffled_max` close to or above `real_margin` | The rule's separation **needs X** — X alone, or X together with the rank-1 term; this run cannot tell those two apart. BF_1 alone is not distinguishable from a degree-preserving null on existence. | Is the **group structure** (the field-group terms X, not the rank-1 term alone) bank-specific? |
| **C. in between** | everything else: `1 ≤ n_shuffled_ge_real ≤ 3` (`p_one_sided` 0.02–0.04), or `n_shuffled_ge_real = 0` with `strictly_above_all` false (a tie within `TAU`) | `gap` small but not clearly near either end | Partial: the rank-1 part alone carries weak separation, short of the harness's own bar. Neither "rank-1 alone suffices" nor "rank-1 alone is ambient" is supported. | Both questions stay open; the second brain tests the rule's full existence term, and attributing between BF_1 and X needs a further, not-yet-registered run (e.g. X alone "as a rule"). |

Every possible result lands in exactly one row: A needs `n = 0` and strict; B needs `n ≥ 4`; C takes
`n` in 1–3 and the `n = 0`-but-tied case. The script's branch code (`bf1_p3.py`, `branch = ...`)
implements exactly this order: A first, then B by `p_one_sided ≥ 0.05`, else C.

**Caveat on what "BF_1" stands for.** BF_1 here is the rank-1 term fitted **on its own**, on top of
N1. Inside rule #2.1 the rank-1 term is fitted **jointly with X**, so it is not the same fitted
object. This run tests whether *a trained rank-1 term by itself* separates; it does not isolate
the rank-1 component as it sits inside the rule.

**Why the p = 0.05 cut for branch B, not p = 0.01 (P3's own pass bar).** P3's own pass bar
(`strictly_above_all`, `n_shuffled_ge_real = 0`, `p = 0.01`) is a **one-sided existence bar for
passing an exam**, calibrated to be strict because a false pass lets a rule through C6. This run
is not an exam pass/fail; it is a diagnostic read of *how much* separation survives. Using the
strict `p = 0.01` bar for "does not separate" would misclassify a middling result (e.g. 3 of 99
shuffles ≥ real, `p ≈ 0.04`) as "does not separate" when three-in-99 is still an unusual event
under the shuffle null. `p ≥ 0.05` is the conventional boundary for "not distinguishable from the
null at the usual significance level," and it leaves branch C to hold the genuinely ambiguous
region (`p` in about [0.02, 0.05)) honestly rather than forcing it into A or B.

**Formal branch and distance reading.** Both are read off the same 99 margins. A positive gap
(`shuffled_max < real_margin`) implies `n_shuffled_ge_real = 0`, so a large positive gap can only
occur in A. The two readings can still differ in *strength*: A can hold with a small gap (every
shuffle below the real margin, but the best one close to it), and B can hold with a gap that is
negative by only a little. **The formal branch governs the verdict.** The gap, `shuffled_mean` and
`shuffled_max` are printed next to it so a reader can see how strong the A or how weak the B is;
they do not move a result from one branch to another.

## 7. Can this test separate both worlds? (item 7)

**Neither branch is guaranteed by the numbers already on record.** The rule #2.1 outcome note
(§3) records that rule #1's own P3 existence gap (+0.039, from a rule that *failed* C6 overall)
was *larger* than rule #2.1's (+0.033), which shows the gap size alone does not track rule
quality — so no argument from "rule #2.1 passed, so its rank-1 part must separate" is safe.

Arguments both ways, from numbers already recorded:

- **Toward "BF_1 could separate" (branch A possible).** BF_1 beats N1 in **10 of 10 folds** on
  held-out existence (`exam.P4.bf.folds_beating_N1 = 10`, `second_rule_v21_r1/result.json`), and
  its held-out margin (+0.028150) is not small relative to the rule's own (+0.033776) — it is 83 %
  of it. A rank-1 term that wins every fold by a consistent margin is exactly the kind of stable,
  non-noise pattern a degree-preserving shuffle is built to destroy (the same logic the rule
  itself relied on for its own P3 pass). Branch A is not ruled out.
- **Toward "BF_1 might not separate" (branch B possible).** The nearest measured proxy for a
  low-rank term, `RP_r8 as a rule` (rank **8**, random, not trained), does *not* separate on
  existence: `shuffled_max = -0.0045` vs `real_margin = -0.0123` — its real margin is actually
  *negative* (RP_r8 is worse than N1 in-sample) and 62 of 99 shuffles do at least as well
  (`harness_controls.json`, `controls["real/RP_r8 as a rule (seed 999)"].P3.existence`). This is
  a poor proxy for BF_1 (§0) precisely because it is random and rank 8, not trained and rank 1 —
  but it does establish that "some rank-r additive term on the existence logit" is not
  automatically separating; separating requires the term to have actually **fit** something the
  shuffle destroys, and a random projection does not. Whether BF_1's *trained* fit crosses that
  line is exactly what is unknown.
- **A stronger argument that the test is not degenerate: BF_1's own shuffled fits are new
  computation.** `harness.precompute` (called by every C6 rule run) only fits BF predictors on
  the **real** bank (harness.py line 1583, `tasks += [("cv", f"BF:{r}", "real", f) ...]` — no
  loop over `env.shuffled` for BF). So **no BF_1-on-shuffled-bank fit exists anywhere in the
  repository before this run** — not in `second_rule_v21_r1`'s spread log, not in
  `harness_controls.json`. This is a genuine, unmeasured quantity, not a foregone conclusion
  dressed up as a question.
- **What would make the test degenerate, and why that is not the situation here.** The test would
  be degenerate only if BF_1's fit mechanically could not separate (e.g. if the shuffle preserved
  exactly the sufficient statistics BF_1's ALS fit depends on, the way N1's per-node marginals are
  preserved by the degree-preserving shuffle, `docs/notes/2026-09-23-rule-2-1-c6-what-it-showed.md`
  §3 fact 3 and `checks/n1_alone/RESULT.md`). BF_1's ALS fit uses the **pairwise (s, t) residual
  pattern** `Y - sigmoid(N1's own fit)`, not just per-node marginals — that residual pattern is
  exactly what a degree-preserving double-edge swap scrambles (it permutes which pairs are
  non-empty while holding each node's degree fixed), so there is no structural reason, analogous
  to N1's, why BF_1 *must* fail to separate. Conversely there is no structural reason it *must*
  separate either — unlike, say, a term that stores the observed values outright (the oracle
  control), which is *guaranteed* to separate on accuracy but shown, by
  `docs/notes/2026-09-23-rule-2-1-c6-what-it-showed.md` §4 ("Zcode's lesson from the oracle row"),
  *not* to separate on P3, because it is equally perfect on shuffled banks too. **Conclusion: this
  test is not degenerate. Both branches remain open given everything on record, and the run is
  informative whichever way it lands.**

## 8. Cost estimate, compute, outputs

- **Fits required:** `cv(BF_1, bank)` for 1 real + 99 shuffled banks = 100 banks × 10 outer folds
  = **1,000 outer-fold fits of BF_1**. Each such fit is `fit_bf(view, 1)`: one N1 fit (cheap,
  closed Newton) plus, for each of that fold's 10 *inner* folds, 5 λ values × rank-1 ALS with
  `STARTS = 10` restarts — i.e. roughly 500 ALS solves per outer fold, ~500,000 ALS solves in
  total across the run. `cv(N1, bank)` for the same 100 banks (1,000 more fits) is far cheaper
  (closed-form Newton, no ALS) and is already the cost `checks/n1_alone.py` measured at 24.3 s
  total for 100 banks — negligible next to BF_1's ALS cost.
- **Measured directly (smoke test, §10):** `cv(BF_1, REAL)` — 10 outer-fold fits, single process,
  no shuffles — took **17.0 s total (≈1.70 s per outer-fold fit)** on this machine
  (`bf1_p3.py --real-only`, `runtime_s = 17.02`). Scaling that to the full run (100 banks × 10
  outer folds = 1,000 outer-fold fits, §8's first bullet) gives **≈1,700 s (≈28 min) serial**, or
  roughly 3–5 minutes with 8–10 worker processes (`--workers`, `ProcessPoolExecutor` over the 99
  shuffled banks, each bank's own `cv` call still serial internally). This matches the DPC chat's
  informal "about 15 minutes" estimate to within the usual factor for worker count and shuffle
  construction overhead (each shuffled bank is also built fresh, a cheap but non-zero cost on top
  of the fits themselves). As a discarded upper-bound analogy: rule #2.1's own single fit at
  `k = 10` measured 6.665 s mean / 6.985 s max per fit
  (`rule_runs/second_rule_v21_r1/ATTEMPTS.md`) — the rule's fit is a *larger* computation than
  `fit_bf` alone (it also fits an offset library and field-group terms), so the direct measurement
  above is the number this estimate relies on, not that analogy.
- **CPU/GPU:** CPU only, matching every other harness arm (`OMP_NUM_THREADS` etc. pinned to 1 per
  the harness's own multiprocessing convention, harness.py lines 32–34); this repository's GPU-first
  rule applies to compute the codebase does on its own numeric kernels, and the harness's BLAS
  calls here are the existing, unmodified `fit_bf`/`bf_als` code path — no new kernel is written by
  this run.
- **Workers:** the script accepts `--workers N` and parallelises the 100 banks with a
  `ProcessPoolExecutor`, following `harness.rule_run`'s convention exactly (default `max(1,
  os.cpu_count() - 2)`, harness.py line 1726 and `checks/n1_alone.py`'s own single-process
  simplicity traded up to worker pool only if the smoke timing shows it is needed).
- **Where outputs go:** `results/genome/c6/checks/bf1_p3/` (`summary.json`, `per_shuffle.csv`,
  `RESULT.md`), script at `results/genome/c6/checks/bf1_p3.py`. **This deviates from the brief's
  suggested `rule_runs/bf1_p3/` + `rules/bf1_p3/run.py` layout**, because BF_1 is not a submitted
  "rule" in C6's sense (no new `PROGRAM_FILES`/`fit`/`NAME` is registered; it is the harness's own
  existing `bf_predictor(1)` object, scored on P3 alone) — it is a **diagnostic check**, exactly
  the shape of the existing precedent `results/genome/c6/checks/n1_alone.py` /
  `results/genome/c6/checks/n1_alone/`, which this script mirrors file-for-file (same output
  triple, same registration-before-script discipline, same git-head/hash stamping). A reader
  comparing the two directories should recognise the same convention.

## 9. What this run cannot show

- **It cannot show that the rank-1 structure, if it separates, is not itself an artifact of the
  bank being a column-averaged, two-fly-merged type-level template** (the same caveat rule #2.1's
  own record carries, `docs/notes/2026-09-23-rule-2-1-c6-what-it-showed.md` §6 interpretation
  line 1 — this run inherits it unchanged, since it uses the same `REAL` bank).
- **It cannot attribute X's contribution precisely**, even in branch A or C. Branch A says the
  rule's separation does not *need* X — but it does not say whether X alone would also separate,
  and it does not measure how much of the rule's
  +0.005626 margin over BF_1 (`second_rule_v21_r1/post_run.json`, `bf_line.rule_minus_bf.1`) is
  itself bank-specific versus ambient. A further, not-yet-registered run (X alone, or X's groups
  individually, "as a rule" against the same 99 shuffles) would be needed for that.
  - Note that the code path is already very close to available: `run_exam` can score **any**
    `Predictor`, so a hypothetical "X-only" run would follow the identical pattern this
    registration uses for BF_1 — but no such predictor exists yet, and none is built by this
    registration.
- **It is a single deterministic run, not a distribution over random rank-1 fits.** BF_1's ALS
  restarts are fixed-seed, not resampled; this run does not ask "how would a *typical* trained
  rank-1 term behave," only "how does *this* trained rank-1 term (the one already inside rule
  #2.1's P4) behave on the 99 already-fixed shuffles."
- **It says nothing about offset, counts or sign** beyond the by-construction zero of §3 — those
  fields are not where rule #2.1's separation question lives (P3's own pass condition already
  restricts itself to existence and offset, and offset is where rule #2.1 itself failed P3;
  BF_1 cannot be read on offset at all, §3).
- **The bank is still the FIB-25/FIB-19 type-level template**, not an individual fly's wiring
  (carried, unchanged, from every other C6 interpretation line).

## 10. Smoke test already run (real bank only; permitted, since the real-bank margin is already
public)

`tools/.venv/Scripts/python.exe results/genome/c6/checks/bf1_p3.py --real-only --allow-dirty
--out <scratch dir outside the repository>` was run once, on the uncommitted tree, writing only
to a temp directory outside the repository, never touching any shuffled bank (`--real-only` skips
all 99). Result: **exact** match — `this_run_existence_margin = 0.028150051052145946`,
`recorded_P4_bf_margin = 0.028150051052145946`, `difference = 0.0` (not merely within tolerance:
bit-identical, as §5's determinism argument predicted). Wall time **17.0 s** for the 10 outer-fold
fits (single process). This also incidentally confirmed §3's construction claim: the smoke test's
`real_margin` for offset, counts and sign all came out exactly `0.0`.

## 11. What the script must do, mechanically, before any value is computed or printed

1. Refuse to run if the working tree has uncommitted changes anywhere (`git status --porcelain`),
   mirroring `harness.rule_run`'s own refusal (harness.py lines 1623–1627) — this file's own
   commit must exist first.
2. Refuse to run if `harness.sha256_lf(harness.py)` does not equal
   `"6fc809527c69ee84aadebfc15c0ba755c189ddc93c80c05c0fa11d969a8d7297"`, the sha this
   registration was written against (also the sha recorded in `second_rule_v21_r1/result.json`'s
   `stamp.harness_sha256_lf` and in `harness_controls.json`). A different harness sha means BF_1's
   own code, the shuffle mechanism, or `margin`/`cv` may have changed since this registration was
   written, which must be resolved (a new registration, not a silent re-run) before any number is
   trusted.
3. Run the machine check of §5 first (real bank only) and stop, printing the failure, before
   touching any shuffled bank, if it fails.
4. Only if 1–3 all pass: compute the 99 shuffled margins, write `per_shuffle.csv` (existence
   margin per bank plus per-fold detail, matching `checks/n1_alone.py`'s CSV shape),
   `summary.json` (the six numbers of §4, the branch of §6, the git head and harness sha, runtime),
   and `RESULT.md` (a short table plus the branch reading, written for a reader who has not opened
   the registration).
5. The script is committed, but **not run**, by the author of this registration. Running it is a
   separate step, on Mike's word, after this file and the script are both reviewed.
