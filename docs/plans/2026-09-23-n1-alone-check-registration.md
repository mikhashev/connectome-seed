# Registration: does N1 alone separate the real bank from the 99 shuffled banks?

**Written:** 2026-09-23, by CC (subagent), under the C6 blindness rule for this check. I did not
open `results/genome/c6/rules/`, `results/genome/c6/rule_runs/first_rule/spread.jsonl`, or
`docs/plans/2026-09-23-first-rule-proposal.md` / `...-search-criterion.md`. This check needs only
the exam side of the harness; it does not involve the rule.

## Question

`first_rule_k12`'s P3 (`results/genome/c6/rule_runs/first_rule_k12/RESULT.md` §P3) reports the
rule's *margin over N1* (`rule_score - N1_score`, signed so larger = better) on the real bank
against 99 shuffled banks, and gets existence p = 0.01 (real margin -0.0045, strictly above all
99 shuffled margins, which range up to -0.0436). That is a statement about the margin, not about
N1 by itself. The handover
(`docs/briefs/2026-09-23-next-session-handover.md` §3 step 0) asks the prior question: **does N1
alone (not a margin, its own held-out score) separate the real bank from the 99 shuffled banks on
existence?**

- If yes (real N1 score strictly better than all 99 shuffled N1 scores): the structure N1 already
  captures is itself non-marginal/non-ambient, so the rule's small margin over N1 is being
  measured against a null that is already doing real work — inconclusive as to whether a *second*
  rule of the same family would find anything new beyond what N1 finds.
- If no (real N1 score is not better than all 99 shuffled N1 scores, i.e. p > 0.01, in particular
  if real falls inside or below the shuffled spread): the structure the existing rule touched
  (i.e. what N1 already models) is itself marginal/ambient by this test. In that case a second
  rule of the same family — built to beat N1 the way the first one was — is pointless, because
  the target it would be beating (N1) is not distinguishable from a degree/marginal baseline in
  the first place; the next rule should instead model the residual after a marginal (N1) model,
  not try to out-score N1 on the raw field again.

## Exact quantity

Per field `f` in `("existence", "offset", "counts", "sign")`, but **existence is the field the
decision rule below is stated on** (offset/counts/sign are reported descriptively only, as P3
already restricts its own pass condition to existence and offset):

- `real_N1[f]` = `harness.cv(N1, REAL)` — N1's held-out score for field `f`, mean over the same
  10 folds (`N_FOLDS = 10`, `FOLD` from `folds.csv`) used everywhere else in the exam. No
  reimplementation: this calls `harness.cv` directly.
- For each shuffle seed `sd` in `range(99)` (the same `N_SHUFFLES = 99`, the same
  `harness.shuffled_bank(REAL, sd)` used to build `env.shuffled` for P3):
  `shuffled_N1[sd][f]` = mean over the same 10 folds of `harness.cv(N1, shuffled_bank)[f]`.
- Score direction is `harness.LOWER_IS_BETTER[f]`: `True` for existence and counts (log-loss /
  count error, lower is better), `False` for offset and sign (Jaccard / sign accuracy, higher is
  better). This is a **raw score**, not a margin: no N1 subtraction, no `rule` predictor involved
  at all. (Contrast with P3's `margin(rule_scores, null_scores, f)`, which is
  `rule[f] - N1[f]` signed so larger is better regardless of field direction — that quantity is
  not computed here.)

## Decision rule (same convention as P3)

For existence, define "at least as good as real" using the field's direction: a shuffled value
counts if `shuffled_N1[sd]["existence"] <= real_N1["existence"]` (lower is better, so "as good or
better" means "as low or lower").

`n_ge = count of shuffles at least as good as real`
`p_one_sided = (1 + n_ge) / (1 + 99)` — identical formula to
`results/genome/c6/harness.py`'s `rule_run` (`p3 = {..., p_one_sided=(1 + n_shuffled_ge_real) /
(N_SHUFFLES + 1)}`).

**"N1 separates the real bank from the 99 shuffled banks on existence" iff `n_ge == 0`, i.e.
`p_one_sided == 0.01`** (real strictly better than every one of the 99 shuffles) — the same
"strictly above/below all 99" bar P3 uses for its own pass condition.

- **If N1 separates** (p = 0.01): branch "yes" above — the structure N1 captures is itself
  non-marginal; a second rule of the same family should not be ruled out on this ground alone.
- **If N1 does not separate** (p > 0.01): branch "no" above — the structure is marginal/ambient
  by this test; a second rule of the same family chasing a margin over N1 is pointless, and the
  next rule should model what's left after a marginal (degree) baseline, not try to beat N1 on
  existence directly.

Offset, counts and sign get the same table entries (real value; shuffled min/mean/max; `n_ge`;
`p_one_sided`) computed the same way, reported **descriptively only** — they do not feed the
verdict above, which the handover states specifically for existence.

## Prediction, and why this is close to being decidable before running anything

`results/genome/c6/harness_controls.json` (`control_d_shuffled_banks`, from the harness's own
`--controls` run, `results/genome/c6/HARNESS-CONTROLS.md`) already computed the aggregate form of
exactly this quantity, as part of an unrelated invariant check (control (d), shuffle invariants),
using the same `cv(N1, ...)` calls, the same real bank, and the same 99
`shuffled_bank(REAL, sd)` banks:

- `N1_existence_logloss_real = 0.36248`
- `N1_existence_logloss_shuffled_min_mean_max = [0.35938, 0.36234, 0.36564]`

The real value (0.36248) is **not** the minimum of the combined set — the shuffled minimum
(0.35938) is lower (better, since existence is lower-is-better) than the real value, and the real
value sits close to the shuffled mean (0.36234), inside the shuffled range. So on the aggregate
statistic alone, at least one shuffle already beats real, meaning `n_ge >= 1` and
`p_one_sided > 0.01`.

**Prediction: N1 does not separate the real bank from the 99 shuffled banks on existence** (branch
"no"). The mechanism: `fit_n1`'s existence arm is a ridge-logistic regression on per-source-node
and per-target-node one-hot indicators only (`X[:, 1+s]`, `X[:, 66+t]`, `results/genome/c6/
harness.py:353-359`) — i.e., it is a per-node-identity (hence closely tied to per-node in/out
degree) model. `shuffled_bank` preserves `out_degrees_kept` and `in_degrees_kept` **exactly** for
every one of the 99 shuffles (verified invariant, `control_d_shuffled_banks.invariants_all_hold =
True`). This is not "identical by construction" in the strict sense — the shuffle preserves exact
row/column sums of the full 65x65 existence matrix, not the per-fold train/held-out split of
those sums, and the regression is ridge-penalized, not an exact marginal fit — so real and
shuffled N1 scores are expected to be close but not bit-identical. The prediction above, and the
aggregate numbers it is based on, will be checked exactly per-seed by
`results/genome/c6/checks/n1_alone.py`, run only after this file is committed.

## Offset, counts, sign: what the same aggregate control already shows

- offset: `N1_offset_jaccard_real = 0.4204`; `shuffled_min_mean_max = [0.3825, 0.4037, 0.4221]`.
  Higher is better for offset, and real (0.4204) is *above* the shuffled max (0.4221)... real is
  actually below the shuffled max (0.4221 > 0.4204), so real is not the best either — real sits
  above the shuffled mean but below the shuffled max, so at least one shuffle is expected to be at
  least as good. This will also be computed exactly, but is reported descriptively only per the
  decision rule above (the verdict is stated for existence only).
- counts, sign: no equivalent aggregate is precomputed for these two fields in
  `harness_controls.json`; they will be computed fresh by the script, descriptively only.

## Commit discipline

This file is committed alone, before `results/genome/c6/checks/n1_alone.py` is written or run,
per the same registration-before-computation discipline the rest of C6 uses.
