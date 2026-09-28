# Block B: the fit diagnostic of rule #2.1's block-only λ (plan, before the run)

Status: plan, revision 1 (the reviewers' edits E1-E6, section 9). Script: `results/genome/c6/checks/knockout_regrow_block_b_fit_diagnostic.py`;
tests: `results/genome/c6/checks/test_knockout_regrow_block_b_fit_diagnostic.py` (fixtures only).
Step (ii) of Ark's order, agreed by Mike in the DPC Research chat on 2026-09-28 at 19:28 UTC.

## 1. The question, and what it does not decide

Block B's registered run (`results/genome/c6/checks/knockout_regrow_block_b/`, registration rev
1.7.3) read U, "failed fit": rule #2.1's `ceiling_block` = 0.7744 < 0.90. Its block-only fit chose
λ = 100, the top of the grid; the four BF block-only fits chose λ = 1. **Question:** was λ = 100
chosen by the data, or by the geometry of the inner folds (the one-cell fold) and the tie rule?

**It decides nothing about block B.** A §5 sends "the fit, not the block" to review; the label
stays U (failed fit) whatever this prints. The outcome feeds later registrations only: the
calibration of the failed-fit branch, and a gate that measures the interaction.

## 2. How the block-only fit chooses λ (read from the code at 29491de)

Found with the Orbit graph of this worktree (definitions of `harness.py`, `knockout_regrow_block_b.py`),
then read in full. **Rule #2.1 does not go through `harness.fit_bf`**; it has its own copy of the
scheme in `rules/second_rule_v21/fit.py`:

1. `knockout_regrow_block_b.py` `_fit_one` (1239–1265): `P.train(bank, MASKS["block"])` (1251),
   `MASKS["block"]` = the 40 cells (245); decode on the 40 cells (1254); `ceiling_block` = `auc` of
   that `p` (`evaluate_bank`, 1474). `_w_init` (1187) sets `H.STARTS = 10` (the registered `--starts 10`).
2. `harness.py` `Predictor.train` (293–301): `make_view(bank, mask)`, then `fit(view, starts=STARTS)`.
3. `fit.py` `fit` (362) → `fit_existence` (119–146). The inner folds are `harness.inner_folds`
   (554): the C6 fold ids (`folds.csv`) of the view's 40 cells, here 10 folds of 4, 4, 2, 4, 5, 3,
   2, 8, 1, 7 cells. For each fold f and each λ in `LAMBDAS` = {1, 3, 10, 30, 100} (57): N1 refitted
   on the other folds' cells (`subview`, `fit_n1`), then `fit_uvw` (97–112: 3 rounds of `bf_als` at
   rank 1 with penalty λ on u, v, then ridge on the 4 × 4 group term W with a fixed penalty MU = 1).
4. **The quantity maximised** (139–140): the inner held-out Bernoulli log-likelihood,
   Σ over the fold's held-out cells of log p (present) or log(1 − p) (absent), p = sigmoid of the
   logit clipped to [0.001, 0.999] (`H.CLIP`), **summed** (not averaged) over the 10 folds; a
   fold weighs by its cell count.
5. **Selection** (141–142): `lam = max(l for l in LAMBDAS if ll[l] >= best - LAMBDA_TIE)`,
   `LAMBDA_TIE = 1e-9` (68): argmax, ties within 1e-9 go to the larger λ; then the final fit on all 40 cells at that λ (143–144).
   The per-λ totals are kept in `LAST_FIT["inner_ll"]` (398) but were not written by the run.

BF_1 (`harness.py` `fit_bf`, 710–731) is the same scheme with `bf_als` alone (no W), the same
folds, likelihood, clip and tie rule (728); `bf_als` reads `STARTS` = 10 (671). Its tolerance is
a literal `1e-9` at 728, a second carrier that cannot be imported: the script reads it from the
source of `fit_bf` and stops at import unless it equals `fit.LAMBDA_TIE` (section 9, E6).

## 3. What is computed

On the real bank (`H.REAL`), block-only view, the same mask, folds, starts (k = 10) and seeds
(`PCG64(30000 + j)`, fixed in `bf_als`) as the registered run, for **rule #2.1** and, for
contrast, **BF_1**: one registered fit each, unchanged. The script does not reimplement the fit:
it wraps the one function that makes each inner fit (`fit_uvw`; `bf_als` for BF_1), keeps its
logit grid, and matches every call to its fold by the call's training mask (a mismatch stops).
From those grids, with the fit's own expression (item 4), it prints:

- per fold: cells, present, absent, the held-out log-likelihood for each of the 5 λ, the fold's own
  choice under the tie rule, the λ tied within 1e-9, clipped probabilities, max |u·v|;
- per λ: the total over all folds (summed in the fit's order), the selected λ, the set T of λ
  within `LAMBDA_TIE` of the best total (T has more than one member if and only if the tie rule
  acted), and the **margin m = total(λ = 100) − total(λ = 1)** in nats (section 5);
- the same totals, T and m **without the one-cell fold**, **without every single-class fold** (no
  present or no absent cell; in block B only the one-cell fold, which holds one present cell),
  and **without each fold in turn** (leave one fold out, E5), naming the folds whose removal
  changes the selected λ or the reading of m: re-sums of the same numbers, sensitivities, not
  refits;
- for **both** predictors (E4): T, the chosen λ, max |u·v| per λ over the inner fits and in the
  final fit, the **collapsed tail** (the λ whose inner fits have max |u·v| ≤ `UV_ZERO` = 1e-9 in
  every fold) and whether the chosen λ lies in it.

Outputs: console, and `connectome-seed-data/knockout_regrow/blockB_fit_diagnostic_<UTC>_<head 12>/`
(`diagnostic.json`, `console.txt`, `SHA256SUMS.txt`); never the repository, the registered run's
folder or a reference folder (refused). It refuses a dirty tree and checks the pins and versions
(the registered script's `refuse_if_dirty`, `check_pins`). It reads block B's real cells: allowed
now, the registered run is done.

**The outcome's carrier (Zcode).** After the run, the command, the UTC date, the output folder
and the key result (the reading's label, m, T, the folds that flip it, and the E4 sentence) go
into block B's `READING_NOTES.md` or into section 9 of the next revision of this plan, not only
into the chat.

## 4. Reproduction check (before anything is read)

The refit must equal the registered run: rule #2.1 λ = 100 and `ceiling_block` = 0.7744360902255639;
BF_1 λ = 1 and 0.9649122807017544 (exact float equality); the 40 `p_exist` equal to the record
`real||block||<key>` of the run's `raw_fits_real.json.gz` (read-only, exact); the per-fold sums
equal `LAST_FIT["inner_ll"]` (exact) and give the fit's λ under the tie rule. **If any differs, the
run stops, writes `STOP.json` with the failures only, prints no per-fold table, and nothing is read.**

Notes for whoever edits this gate later (Ark):

- The gate compares `P.decode(data, B.BLOCK_CELLS)["p_exist"]`, the decoded output of the stored
  model, so it also pins rule #2.1's **quantisation path** (5-bit symmetric symbols, `fit.py` 59,
  and section 2.3 of `fit.py` from line 149): a refit whose float fit matched but whose symbols
  differed would fail it. Do not weaken it to a comparison of float parameters.
- `recorded_block_fit` calls `B._w_init(starts, None, False)` (block B script 1187), which pops
  `SECOND_RULE_SPREAD_DIR` (1189): as in the registered run, no spread log is written (`fit.py`
  410–411 writes one only when that variable is set). The per-λ totals a spread log would carry
  are read from `LAST_FIT["inner_ll"]` (`fit.py` 398) instead.
- `recorded_block_fit` repeats the block-only part of `_fit_one` (1239–1265) rather than calling
  it. This is safe: it uses the registered carriers only (`B.MASKS["block"]`, `B.BLOCK_CELLS`,
  `B.auc`, `B._lambda_of`, `B._w_init`, `B._pred`), and the gate catches any divergence (λ,
  `ceiling_block`, the 40 `p_exist`).

## 5. Reading, registered before the run (Ark's falsifier, 19:20 UTC; revision 1)

**What the diagnostic can separate (E3, registered before the run).** The bottleneck is the λ
grid: it has no λ < 1, and its four upper λ are expected to be one model (u·v ≈ 0, below). So
the diagnostic can at most separate "an interaction at λ = 1" from "no interaction at any λ above
1". It says nothing about the absence of a rank term on the block: the weak-penalty regime
(λ < 1) is not tested. **The outcome is read about the grid, not about the block; a "no" does not
mean "no interaction".** Consequence for the later registration (iii): it must include λ < 1 or
a fixed λ, or it inherits the same floor.

**The decision number (E1).** The reading reads the margin in nats, not membership in T:
**m = total(λ = 100) − total(λ = 1)**, for rule #2.1. The script prints it as
`margin_top_over_low`, beside the two margins it already computed:

- `margin_tied_over_rest` = min over T − max over the λ outside T. By construction it exceeds
  `LAMBDA_TIE` whenever some λ is outside T (and is absent when T is the whole grid), so its sign
  carries no information. With a collapsed tail and λ = 1 outside T (T = {3, 10, 30, 100}) it
  equals m to within the tail's spread (~1e-13 on fixtures): **there `margin_tied_over_rest` and
  m are one number under two names**, and m is the one that stays defined when λ = 1 joins T.
- `margin_top_over_rest` = total(100) − the best other total. With a collapsed tail the best
  other is inside the tail, so this is the in-tail spread (~1e-13), **not** the decision number.

Each m is read as: **|m| ≤ `LAMBDA_TIE`**: "indifferent" (the data do not separate λ = 1 from
λ = 100); **m > `LAMBDA_TIE`**: "top preferred"; **m < −`LAMBDA_TIE`**: "lambda = 1 preferred".
The tolerance is `fit.LAMBDA_TIE` = 1e-9 nats, the fit's own; no larger practical threshold is
registered, and m is always printed with its size.

**The gate, as arithmetic.** If the all-fold selection is λ = 100 (the reproduction gate), then
total(100) ≥ best − `LAMBDA_TIE` ≥ total(1) − `LAMBDA_TIE`, so m ≥ −`LAMBDA_TIE`. The script
prints this check (`gate arithmetic: ...`); m < −`LAMBDA_TIE` would mean λ = 1 is chosen, i.e.
the gate must have failed.

**The rules**, for rule #2.1, in this order (the labels as the script prints them):

- **`not applicable`:** the all-fold selection is not λ = 100 (the gate has failed; nothing is
  read).
- **`gate arithmetic failed`:** m < −`LAMBDA_TIE` (cannot happen after the gate; printed if it
  does).
- **`(a) tie rule`:** |m| ≤ `LAMBDA_TIE`: the data are indifferent between λ = 1 and λ = 100; the
  tie rule chose. (E2) This reading is valid only together with the reproduction gate: if λ = 1
  were strictly best it would be in T trivially, and "λ = 1 ∈ T" alone would not say that the tie
  rule chose.
- **`(a) fold geometry`:** m > `LAMBDA_TIE`, but without the single-class fold(s) m ≤ `LAMBDA_TIE`
  (indifferent or λ = 1 preferred): the preference for λ = 100 is carried by the single-class
  fold(s).
- **`(b) data`:** otherwise, if more than half of the two-class folds have their own margin
  ll_f(100) − ll_f(1) > `LAMBDA_TIE`: "the data preferred lambda = 100". If λ = 100 lies in the
  collapsed tail this reads **"no interaction on the registered lambda grid"**; if not, "a weaker
  interaction (lambda = 100 is not in the collapsed tail), not none".
- **`(c) carried by few folds`:** otherwise: m > `LAMBDA_TIE` without the single-class folds,
  but in at most half of the two-class folds; the folds that carry it are named.

Every label is printed with T, the three margins, the collapsed tail and its spread, and the
**leave-one-fold-out** result (E5): for each fold f, the selected λ, T and m without f, and the
folds whose removal flips the selected λ or the reading of m. These are printed, not rules: they
name how many folds the outcome rests on. The console ends with "read about the registered
lambda grid (no lambda < 1), not about the block: a 'no' is not 'no interaction'".

**Both predictors (E4, a mechanical sentence registered now).** For rule #2.1 and BF_1 the
script prints T, the chosen λ, max |u·v| and whether the chosen λ lies in its collapsed tail. If
rule #2.1's chosen λ lies in its collapsed tail and BF_1's does not, then 0.7744 against 0.9649
compares two model classes (a fit with no rank-1 term against a rank-1 fit) as much as two
predictors. Otherwise the script says the two are not split by the tail.

**Expected before the run (from fixtures, not a rule):** on the fixture world the per-fold values
of λ = 3, 10, 30, 100 agree within ~1e-13 and max |u·v| ≤ 1e-13 for each, while λ = 1 has
max |u·v| ≈ 1.4 (both predictors): above a threshold λ the rank-1 term is zero (penalising
|u|² + |v|² acts like a nuclear-norm penalty on u·v, whose solution is u·v = 0 once λ exceeds,
roughly, the largest singular value of the loss gradient at u·v = 0), so those λ are one fit. If
so on the real block, T is likely {3, 10, 30, 100}, "λ = 100" is the tie rule's name for "no
interaction", and m is the contest of λ = 1 against the zero interaction.

None of the labels changes the verdict (U, failed fit).

## 6. Runtime

Rule #2.1: 10 folds × 5 λ + 1 final = 51 `fit_uvw` = 153 `bf_als` calls × 10 starts × 25 sweeps;
BF_1: 51 `bf_als` × 10 starts. The registered run took 8.9 s and 2.9 s for these two fits
(`raw_fits_real.json.gz`, `secs`); the fixture test fits both at k = 10 in 3.6 s and 1.2 s. With
the import of the harness: **under one minute**, CPU, one process. It needs Mike's word to run.

## 7. Tests (fixtures only, no real bank)

The per-λ totals give the fit's λ under the tie rule, and equal rule #2.1's `inner_ll` bit for bit
(both predictors); recording does not change the fit (same `p_exist` as an unrecorded fit); a
changed total, value or stored `p` fails reproduction; the tie rule at 5e-10 and 2e-9; each reading
branch on hand-made tables, read by the margin; a collapsed tail whose in-tail spread moves the
argmax from 100 to 3 when the single-class fold is dropped reads (b), not (a) fold geometry;
|m| ≤ `LAMBDA_TIE` reads indifferent; leave-one-fold-out names the one fold that carries
λ = 100; the collapsed tail and the E4 sentence on hand-made and fixture fits; `LAMBDA_TIE` is
`fit.py`'s, and harness.py's literal is read and equals it (a changed or missing literal is
caught); the console lines on the fixture fits; the output folder refusals; a dirty tree refused
before the real bank is read. `PYTHONUTF8=1 tools/.venv/Scripts/python.exe -m pytest -p
no:cacheprovider -q results/genome/c6/checks/test_knockout_regrow_block_b_fit_diagnostic.py`:
16 passed, ~3 s.

## 8. For reviewers

- A single-class fold cannot give −inf or NaN: p is clipped to [0.001, 0.999], so each cell adds
  between log 0.001 = −6.91 and log 0.999 = −0.001. The one-cell fold adds one such term per λ;
  its range across λ bounds how much it can move the totals (≤ 6.9 nats).
- The one-cell fold alone cannot make a tie in the totals: it can at most add the same value
  for several λ (e.g. if its p is clipped at 0.999 for all of them). A tie between λ comes from
  fits that are the same (the collapse above), and then it holds in every fold at once.

## 9. Revision 1 — the reviewers' edits

Review of 3fb444b in the DPC Research chat, 2026-09-28: Johnny 19:52 UTC "yes, no edits"; Ark
19:55 UTC "yes, with edits" (E1 and E3 required; E2, E4–E6 cheap); Zcode 19:56 UTC "yes, after E1
and E3" (joins Ark, accepts all). All are applied:

- **E1 (Ark, required):** the reading reads the margin m in nats, not membership in T (section
  5), for all folds, without the single-class folds, and for each leave-one-out set. Two
  corrections to the review's premises, from the code at 3fb444b: the old "(a) fold geometry"
  rule compared the *tie set* without the single-class fold with T, not the argmax, so it could
  fire (when λ = 1 wins without that fold); and `margin_top_over_rest` is not
  `margin_tied_over_rest` under a collapsed tail (it is the in-tail spread); m is. The margin
  rule is adopted anyway: it makes the decision a printed number, and it stays defined when
  λ = 1 is in T.
- **E2 (Ark):** "(a) tie rule" is valid only with the reproduction gate (section 5).
- **E3 (Ark, required):** the λ grid is the bottleneck; the outcome is read about the grid, not
  the block; registration (iii) must include λ < 1 or a fixed λ (section 5).
- **E4 (Ark):** T, the chosen λ, max |u·v| and the collapsed tail for both predictors, and the
  mechanical sentence on model classes (sections 3 and 5).
- **E5 (Ark, code):** leave-one-fold-out re-sums (`summarise`, key `leave_one_out`), with the
  folds that flip the choice or the reading named; tested on fixtures.
- **E6 (Ark, code):** the script uses `fit.LAMBDA_TIE` (loaded through `H.load_rule`, as the rule
  path loads `fit.py`) instead of its own `TIE`; harness.py 728's literal is read from
  `inspect.getsource(H.fit_bf)` and must equal it at import (section 2).
- **Ark's notes on section 4:** the gate pins the quantisation path; where the spread log went;
  why the copy of `_fit_one` is safe (section 4).
- **Zcode:** the outcome's carrier is `READING_NOTES.md` or the next revision's section 9, not
  only the chat (section 3).
- New constant, not in the review and open to it: `UV_ZERO` = 1e-9 (max |u·v| of a fit with no
  rank-1 term), used only to name the collapsed tail and to choose the (b) gloss and the E4
  sentence.
