# Block B: the fit diagnostic of rule #2.1's block-only λ (plan, before the run)

Status: plan for review. Script: `results/genome/c6/checks/knockout_regrow_block_b_fit_diagnostic.py`;
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
5. **Selection** (141–142): `lam = max(l for l in LAMBDAS if ll[l] >= best - 1e-9)`: argmax, ties
   within 1e-9 go to the larger λ; then the final fit on all 40 cells at that λ (143–144).
   The per-λ totals are kept in `LAST_FIT["inner_ll"]` (398) but were not written by the run.

BF_1 (`harness.py` `fit_bf`, 710–731) is the same scheme with `bf_als` alone (no W), the same
folds, likelihood, clip and tie rule (728); `bf_als` reads `STARTS` = 10 (671).

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
  within 1e-9 of the best total (T has more than one member if and only if the tie rule acted);
- the same totals **without the one-cell fold**, and **without every single-class fold** (no
  present or no absent cell; in block B only the one-cell fold, which holds one present cell):
  a re-sum of the same numbers, stated as a sensitivity, not a refit.

Outputs: console, and `connectome-seed-data/knockout_regrow/blockB_fit_diagnostic_<UTC>_<head 12>/`
(`diagnostic.json`, `console.txt`, `SHA256SUMS.txt`); never the repository, the registered run's
folder or a reference folder (refused). It refuses a dirty tree and checks the pins and versions
(the registered script's `refuse_if_dirty`, `check_pins`). It reads block B's real cells: allowed
now, the registered run is done.

## 4. Reproduction check (before anything is read)

The refit must equal the registered run: rule #2.1 λ = 100 and `ceiling_block` = 0.7744360902255639;
BF_1 λ = 1 and 0.9649122807017544 (exact float equality); the 40 `p_exist` equal to the record
`real||block||<key>` of the run's `raw_fits_real.json.gz` (read-only, exact); the per-fold sums
equal `LAST_FIT["inner_ll"]` (exact) and give the fit's λ under the tie rule. **If any differs, the
run stops, writes `STOP.json` with the failures only, prints no per-fold table, and nothing is read.**

## 5. Reading, registered before the run (Ark's falsifier, 19:20 UTC)

For rule #2.1 only (BF_1 is printed for contrast, not read). T = the λ within 1e-9 of the best
all-fold total; the tie rule picks max T = 100. The rules apply in this order:

- **(a) tie rule:** λ = 1 is in T: the data do not separate λ = 1 from λ = 100; the tie rule chose.
- **(a) fold geometry:** without the single-class fold(s), the best λ (with its ties) is not
  inside T: λ = 100 wins only through the one-cell fold.
- **(b) data:** otherwise, if more than half of the two-class folds have their own choice (with
  its ties) inside T: "chosen by the data".
- **(c) carried by few folds:** otherwise: T wins the two-class sum, but in at most half of the
  two-class folds; the folds that carry it are named.

**Expected before the run (from fixtures, not a rule):** on the fixture world the per-fold values
of λ = 3, 10, 30, 100 agree within ~1e-13 and max |u·v| ≤ 1e-13 for each: above a threshold λ the
rank-1 term is zero (penalising |u|² + |v|² acts like a nuclear-norm penalty on u·v, whose
solution is u·v = 0 once λ exceeds, roughly, the largest singular value of the loss gradient at
u·v = 0), so those λ are one fit. If so on the real block, T is likely
{3, 10, 30, 100} or a tail of it, and "λ = 100" is the tie rule's name for "no interaction"; the
reading is then about λ = 1 against the zero interaction, which is what (a)–(c) test. The script
prints, for T, whether its λ give the same held-out value in every fold and the max |u·v|.

None of (a), (b), (c) changes the verdict (U, failed fit).

## 6. Runtime

Rule #2.1: 10 folds × 5 λ + 1 final = 51 `fit_uvw` = 153 `bf_als` calls × 10 starts × 25 sweeps;
BF_1: 51 `bf_als` × 10 starts. The registered run took 8.9 s and 2.9 s for these two fits
(`raw_fits_real.json.gz`, `secs`); the fixture test fits both at k = 10 in 3.6 s and 1.2 s. With
the import of the harness: **under one minute**, CPU, one process. It needs Mike's word to run.

## 7. Tests (fixtures only, no real bank)

The per-λ totals give the fit's λ under the tie rule, and equal rule #2.1's `inner_ll` bit for bit
(both predictors); recording does not change the fit (same `p_exist` as an unrecorded fit); a
changed total, value or stored `p` fails reproduction; the tie rule at 5e-10 and 2e-9; each reading
branch on hand-made tables; the output folder refusals; a dirty tree refused before the real bank
is read. `PYTHONUTF8=1 tools/.venv/Scripts/python.exe -m pytest -p no:cacheprovider -q
results/genome/c6/checks/test_knockout_regrow_block_b_fit_diagnostic.py`: 9 passed, ~3 s.

## 8. For reviewers

- A single-class fold cannot give −inf or NaN: p is clipped to [0.001, 0.999], so each cell adds
  between log 0.001 = −6.91 and log 0.999 = −0.001. The one-cell fold adds one such term per λ;
  its range across λ bounds how much it can move the totals (≤ 6.9 nats).
- The one-cell fold alone cannot make a tie in the totals: it can at most add the same value
  for several λ (e.g. if its p is clipped at 0.999 for all of them). A tie between λ comes from
  fits that are the same (the collapse above), and then it holds in every fold at once.
