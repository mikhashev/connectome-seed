# Registration: the symmetric pair, block A at lambda = 100 and block B's verdict with the block lambda at 1

**Post-data registration. Not blind to:** block A's registered verdict (G, rule #2.1 AUC 0.5327 on
32/32, p_P 0.3288, `ceiling_block` 1.0000, `ceiling_full` 0.8442, lambda ko/full/block 1/1/1) and block B's
registered verdict (U, "failed fit: rule #2.1 cannot hold the block even when trained on it alone", AUC
0.5063 on 19/21, p_P 0.4795, `ceiling_block` 0.7744, `ceiling_full` 0.6316, lambda ko/full/block
1/1/100; BF_1..BF_4 p_P 0.4040, 0.2704, 0.2698, 0.2442); the `block_b_ceil1` measurement
(`results/genome/c6/checks/block_b_ceil1/`: control bit for bit at lambda 100, `cert` 132/133, `ceil_1`
0.9624 = 384/399, float 0.9599 = 383/399, branch (c) FF-sel on the real block); the 414-board lambda law
(`natural_fit_failure_replication/READING_NOTES.md` section 6: `lambda_c` takes only 1 and 100; the 247
boards at 100 carry |u.v| <= 1.31e-15) and the replication outcome RP1 (171 of 300 fresh certified
boards fail at lambda_c = 100); and the population numbers in Ark's 2026-09-30 14:23:57 UTC message
(on the 414 boards where the class holds the pattern: lambda forced to 1 passes 294 of 300 fresh, 98
of 99 seen, 15 of 15 worlds; the selected lambda passes 129, 46, 10; boards that pass at the selected
lambda and fail at lambda 1: 0 in all three sets; 62% of boards select lambda 100 and 92% of those
fail). **Revision 1, the prediction commit. Nothing is fitted or run by this file.**

## 0. The question, in plain words

Block A got the verdict G and block B got U, and for days the pair "A passes, B fails" has been read as
a difference between two blocks. `block_b_ceil1` showed that B's U depends on which lambda the fit
picked for the block-only ceiling (100 gives 0.7744, a forced 1 gives 0.9624). Two questions follow,
one for each block, so that both are answered by the same protocol at both lambdas:

1. **Would A also fail if its block-only fit were forced to lambda = 100?** (a new fit)
   - If A also falls below 0.90, the pair differs by the lambda that each fit happened to choose, not
     shown to differ by the block.
   - If A stays at or above 0.90, A survives the collapse and the population analogy is weaker than
     assumed.
2. **What label would B's own registered label function give if the block-only ceiling had been 0.9624
   (lambda = 1)?** (a reading, no fit) This is B's stored verdict with exactly one number replaced.

## 1. Objects

Definitions are those of `docs/plans/2026-09-29-failed-fit-branch-calibration-registration.md` ("the
calibration") and of `docs/plans/2026-09-30-block-b-ceil1-registration.md` ("the ceil_1 registration");
nothing is redefined here.

| object | definition | printed as |
|---|---|---|
| `cert_A` | the calibration's capacity search (`C.cert_search`, budget of the calibration rev 1.9 section 6, seeds 93300-93307) on A's real 64-cell pattern (32 present, 32 absent, 1024 pairs; a new pattern, no earlier `cert` searched it) | fraction, float, exact and `_tau` |
| `ceil_100_A` | rule #2.1's block-only fit on the real block A with `LAMBDAS = [100]` (S-C4b shortcut, `C.train_shortcut`), **quantised**, the registered object | exact and `_tau` |
| `ceil_100_A_float` | the same fit, float `fit_existence` output before quantisation | exact and `_tau` |
| `uv_max` | max over A's 64 block cells of \|(U V^T)\| of the lambda = 100 fit; **diagnostic, decides nothing** | float |
| Object 2, B | B's `read_label` and `label_text` (`knockout_regrow_block_b.py`) on B's stored verdict objects, `ceiling_block` of rule #2.1 := `ceil_1` (quantised, 384/399, from `block_b_ceil1/result.json`) | label text, deciding clause |
| Object 2, A | A's `read_label` and `label_text` (`knockout_regrow.py`) on A's stored verdict objects, `ceiling_block` of rule #2.1 := `ceil_100_A` | label text, deciding clause |

**Block A, read from the files, not assumed.** 64 cells (8 sources Mi1, Tm3, Mi4, Mi9, Tm1, Tm2, Tm4,
Tm9 x 8 targets T4a-d, T5a-d, row-major: `knockout_regrow.py:173-180`), **32 present and 32 absent, so
1024 pairs**: A's raw store `raw_fits_real.json.gz`, record `real||block||rule`, holds `y` with 32 present
of 64, and A's `summary.json` has `real.block_present` 32 and `RESULT.md` prints "AUC (32/32)".

**Wiring.** Bank: `H.REAL` (`knockout_regrow.py:757`, the bank of A's real arm; also block B's bank). Mask:
`KA.MASKS["block"]` (`:189`). Starts: `K._w_init(10, None, False)` (`knockout_regrow_block_b.py:1187`;
A's manifest records `starts` 10). Fits: `C.train_shortcut` (`failed_fit_calibration.py:495`) and
`C.float_p` (`:451`), the route of `block_b_ceil1.fit_at`. **Adaptation, stated because it is the one
place where A differs from B:** `C.train_shortcut`, `C.float_p` and `C.cert_search` read block B's
`K.MASKS`, `K.BLOCK_CELLS`, `K.N_SOURCES` and `K.N_TARGETS` at call time (`:495`, `:451`, `:393`), so the
script swaps those `K` names (and `K.BLOCK`, `K.N_BLOCK`) to A's for the length of one call with
`C.swapped_globals` (`:440`) and restores them; `fit.py`, the harness and the calibration are not edited.
The same rule #2.1 loads from the same `RULE_PATH`. AUC: `C.auc_counts` (`:209`).

## 2. Controls (must pass before any value is read)

1. **Fit control, A at lambda = 1.** The script first recomputes rule #2.1's block-only fit on A's real
   block at **lambda = 1** through the same route and must reproduce A's stored `ceiling_block` **bit for
   bit**: **1.0 = 1024/1024** (1024 wins, 0 ties of 1024 pairs; the store's `p` has two levels, minimum
   gap 0.75), **and** the exact and `_tau` readings must be equal, **and** the 64 `p` values must be
   bit-equal to the stored ones. An AUC of exactly 1.0 is reached by any perfect separator, so on A the
   value alone is a weak control; the `p` equality is therefore a stop condition here (unlike the
   ceil_1 registration, where it was printed only).
2. **Stored control (no fit).** Before any fit the script recomputes A's stored ceiling from the stored
   `p` and `y` (exact 1024/1024, 32/32, lambda 1) and refuses on any difference.
3. **Reading controls (no fit).** For each block, its label function on its own stored verdict objects
   with the **stored** `ceiling_block` must give the stored label letter and the stored `label_text`
   (B: U and the failed-fit text; A: G and its text), and the p_P rows of the primary and of BF_1..BF_4
   must be present in the stored objects. Otherwise `READING_CONTROL_FAILED` and no fit is run.
4. **Inputs.** The script prints and checks the LF sha256 of every input (section 7) and the raw store's
   sha256.
5. If control 1 fails: **STOP**, print `CONTROL_FAILED`, compute and print nothing else, write
   `stop_record.json`. A control that fails is a defect of the script or environment, not a finding, and
   is never answered by re-pinning.

## 3. Reading trees (fixed before any value)

### 3.1 Object 1 (A at lambda = 100); `cert_A` is read first

- **(a) `cert_A` < 0.90** => a rank limit of the class on block A, the first on a real bank; it
  **outranks** the lambda reading.
- **(d) DECODER SPLIT.** `ceil_100_A_float` < 0.90 <= `ceil_100_A` (quantised), or the reverse => the
  verdict is decided by the 5-bit decoder, not the fit; a separate outcome. In the script (d) is read
  after (a) and before (b)/(c).
- **(b) `cert_A` >= 0.90 and `ceil_100_A` < 0.90** => "A would fail at lambda = 100 as B did: the A/B
  pair differs by the lambda choice, not shown to differ by the block."
- **(c) `cert_A` >= 0.90 and `ceil_100_A` >= 0.90 and `ceil_100_A_float` >= 0.90** => "A survives the
  collapse; the population analogy is weaker than assumed."
- **Rider.** If `ceil_100_A` is within +-0.02 of 0.90, i.e. in [0.88, 0.92], the reading is "at the cut",
  not a side; (b) or (c) is printed with that qualifier.
- **Tie and ulp.** Every branch is read on the exact values. If the exact and the `_tau` readings of
  `ceil_100_A` fall on different sides of 0.90 the row is flagged `GATE_ULP_SPLIT` (calibration section
  6a): the branch follows the exact value, the `_tau` branch is printed beside it. The same for `cert_A`
  (`CERT_ULP_SPLIT`) and `ceil_100_A_float`.

### 3.2 Object 2 (a reading; its label is computed, but frozen here before)

**Is B at lambda = 1 a pure reading? Yes for the label; here is the evidence, file by file.**

- B's `RESULT.md` row for rule #2.1 has `lambda ko/full/block` = **1.0 / 1.0 / 100.0**: the knockout fit
  (AUC 0.5063, `n_ge` 68 of 99, `p_S` 0.69, `p_P` 0.4795) and the full-view fit (`ceiling_full` 0.6316)
  were selected at lambda = 1; only the block-only fit (`ceiling_block` 0.7744) was selected at 100. The
  same numbers are in B's `summary.json`, `real.rows.rule` (`lambda_ko` 1.0, `lambda_full` 1.0,
  `lambda_block` 100.0), and B's own "Fixed lambda = 1 on the knockout view" table shows rule #2.1 at
  lambda 1 with AUC 0.5063 and `p_P` 0.4795, the same values.
- **A correction of a chat statement, recorded here.** Ark's 14:23:57 message says B's other verdict
  objects were computed at lambda = 100: "У B остальные объекты вердикта (`p_P` 0.4795, тот AUC 0.5063,
  `n_ge`) посчитаны **при λ = 100**, то есть под тем же схлопнутым колларом." The stored row says
  otherwise for `p_P` and the AUC (lambda 1). **The one other stored input that used lambda = 100 is the
  set of the 99 leg-S shuffle fits behind `n_ge` and `p_S`:** each shuffle chose its own lambda by the
  nested folds, and for rule #2.1 that was 100 in 97 of 99 shuffles and 3 in two (the script prints this
  from the stored `per_shuffle`). This does not touch the label: `n_ge` enters only through
  `leg_S_passes`, which decides R together with `p_P` <= 0.01 (rule #2.1 has 0.4795), and the G row does
  not read leg S at all. `n_ge` and `p_S` are **not** recomputed at lambda 1 here (that would be a new
  set of 99 fits and is not part of this registration).
- B's label function is `read_label(rows, n_present, readable)` (`knockout_regrow_block_b.py:1599`), with
  the not-readable U of S38 before A's branches, and `label_text` (`:1666`); its inputs are all in B's
  `summary.json`: `real.rows` (p_P, `leg_S_passes`, `ceiling_block`, `ceiling_full` of the primary and
  BF_1..BF_4), `real.block_present` 19, `real.smallest_passing_auc` 0.7143 (not None, so readable),
  `synthetic.limits` and `synthetic.u_rule`. The BF_r p_P rows that the G condition "every BF_r has p_P >
  0.10" needs are stored (0.4040, 0.2704, 0.2698, 0.2442).
- **Expected label, from reading the label function and the stored numbers (not executed):** rule #2.1
  and BF_1 both read "-" (R needs `leg_S_passes` and p_P <= 0.01; W needs a BF_r with leg S and p_P <=
  0.0125, and BF_2..BF_4 have p_P 0.2704, 0.2698, 0.2442); every p_P is above 0.10 (smallest 0.2442,
  BF_4); the gate `ceiling_block` 0.9624 >= 0.90 passes; the block is readable. **Expected: G, decided by
  the G clause ("not R, not W; the primary and every BF_r have p_P > 0.10; the primary's
  `ceiling_block` >= 0.90")**, with the mechanism description "orthogonal (rule #2.1's `ceiling_full` =
  0.6316 < 0.90)" and B's own limits (gamma_R 0.75, leg P from 0.75, family limit 0.75, empty band).
- **What would falsify the expectation:** the printed label is not G, or a reading control of section 2
  fails. Either would mean that this reading of the label function or of the stored objects is wrong.
- **Object 2, A:** the same call on A's stored objects with `ceiling_block` := `ceil_100_A`. If
  `ceil_100_A` >= 0.90 the label is G; if below, U with the failed-fit text ("U: failed fit: rule #2.1
  cannot hold the block even when trained on it alone"); no other clause of A's stored objects changes
  (A's p_P are 0.3288, 0.3837, 0.4912, 0.5119, 0.5042).
- **The pair table** printed at the end: block x block lambda (A at 1 and B at 100 are the stored,
  registered values; A at 100 and B at 1 are this registration's), each with its `ceiling_block`, the gate
  result and the label: "both blocks, both lambdas, same protocol" on the gate clause.
- **Scope of the claim.** This reads the label function on the gate clause. It does not show that B's
  other legs would be unchanged under a lambda-1 protocol for the 99 shuffles (they are stored, not
  recomputed).

## 4. What it changes

No registered label is edited. The outcome adds a **dated reading line beside each block's verdict** in
the block's `READING_NOTES.md` (block B: `results/genome/c6/checks/knockout_regrow_block_b/READING_NOTES.md`;
block A's folder has no `READING_NOTES.md`, so the outcome commit creates one there and edits no file of
A's registered outputs), and feeds the collapsed-lambda declaration draft
(`docs/plans/2026-09-29-collapsed-lambda-verdict-class-registration.md`, section 1.4, the two real
blocks). Branch (b) with Object 2's B = G would put both real blocks in the class "gate depends on the
lambda the fit chose"; branch (c) would separate A from that class; (a) would be reported first and
separately.

## 5. Predictions (all: inference, not measurement)

**Quoted verbatim, in Russian, as posted in the DPC Research chat (the one allowed exception to
English: quoted chat text). An English one-line gloss follows each. All times are 2026-09-30 UTC.**
Every prediction below is **inference, not measurement**.

### 5.1 Ark, 14:23:57 UTC (the context line and the prediction)

> Если A при λ = 100 тоже падает, то «A прошёл, B упал» окончательно перестаёт быть фактом о блоках. Моё предсказание: **A при λ = 100 упадёт** (по популяции — 92 % падают), и это надо записать до счёта.

Gloss: if A also falls at lambda 100, "A passed, B failed" stops being a fact about the blocks; Ark
predicts A falls at lambda 100, by the population (92% of boards that select 100 fail), and asks that it
be recorded before the count. Inference from the 414-board population, not a measurement on A (`cert_A`
was never measured; A's membership in the population is presumed).

### 5.2 Zcode, 14:29:30 UTC, item 1 (A falls below 0.90, the caveat, the falsifier)

> 1. **Предсказание для A при λ = 100: упадёт ниже 0.90.** С явной оговоркой до счёта: измеренные 92% провалов относятся к доскам, которые **сами выбрали** 100; условная частота «выбравший λ = 1, вынужденный на 100» в популяции **не измерена** — у нас только синтетические z/z′ (обе 0.600). Прогон даст первую естественную точку на этот условный вопрос. Фальсификатор: A@100 ≥ 0.90 — тогда A выживает при коллапсе, и популяционная аналогия слабее, чем кажется.

Gloss: `ceil_100_A` < 0.90; the 92% is a rate among boards that chose 100 themselves, the conditional rate
for a board that chose 1 and is forced to 100 is not measured; falsifier `ceil_100_A` >= 0.90, which is
branch (c) of section 3.1.

### 5.3 Zcode, 14:29:30 UTC, item 2 (the scope question and the prediction for B)

> 2. **Вопрос области к «полному пути вердикта B при λ = 1»:** потолочная клауза и `p_P` (перестановки снимного `p` через `auc_null`) — минуты. Но «тот AUC 0.5063» и `n_ge` считаются на фите вида ko/full — если «полный путь» означает фиксированную λ и там, это уже не минуты, а заметная доля зарегистрированного прогона. Регистрация обязана назвать, **какие ноги переиспользуются, а какие считаются заново** — иначе «минуты» будут надеждой, а не обязательством. Если считаются только блок-клаузы — ожидаю, что B при λ = 1 читается G (AUC 0.96 против перестановочного нуля даёт p_P ≈ 0); это тоже записать до счёта.

Gloss: the registration must name which legs are reused and which are recomputed; if only the block
clauses are recomputed, Zcode expects B at lambda 1 to read G, with "AUC 0.96 against the permutation
null giving p_P ~ 0".

**Answer to the scope question (section 3.2):** nothing of B is recomputed; the knockout AUC 0.5063,
p_S, `n_ge`, p_P and the BF rows are reused from B's `summary.json`, and only `ceiling_block` is replaced.
**Note on the premise of "p_P ~ 0", which the label will not carry.** The registered p_P
(`docs/plans/2026-09-24-knockout-regrow-registration.md` section 3.2, "Leg P") is
`(1 + #{AUC_perm >= AUC_real - TAU}) / 10000` where `AUC_real` is the AUC of the **knockout prediction**
(a fit that never saw the block) against uniform permutations of the block's labels. For B that AUC is
0.5063 and the stored p_P is **0.4795**; that stays. Zcode's "0.96 against the permutation null" applies
the permutation test to the **block-only ceiling fit**, which was trained on the block's own labels; that
is a different object, it is not registered, it is close to 0 by construction, and this script does not
compute it. Two further points: the G clause requires every p_P > 0.10, so an expected label G with a
registered p_P ~ 0 would contradict itself; and Zcode's "reads G" is the expectation of section 3.2, but
its parenthesis describes an object that no registered row contains. The prediction is quoted as posted;
the label check of section 3.2 is the test of "reads G", and the stored p_P of 0.4795 is the registered
value that decides.

### 5.4 CC

CC, 2026-09-30, written into this file before the commit (not posted in the chat first):

- **Object 1:** `ceil_100_A` < 0.90, most likely in 0.50-0.70; branch (b). Reason: on the 414 boards
  every fit at lambda 100 carried |u.v| <= 1.31e-15, i.e. the interaction term is switched off and the
  block is left to the additive part; on block A the additive anchor N1 has `ceiling_block` 0.5000
  (A's `RESULT.md` N1 row), so with the interaction off there is little for the fit to hold A with.
  `cert_A` >= 0.90 (A's own lambda-1 fit reached 1024/1024, and that fit is a member of the class).
  No decoder split. Falsifier: `ceil_100_A` >= 0.90.
- **Object 2:** B reads G by the G clause, as stated in section 3.2.
- Inference, not measurement: the |u.v| collapse is measured on synthetic boards of B's shape, not on A.

## 6. Cost and consent

One process, CPU only, no GPU. **Estimate from block B's measurement**, where the whole `block_b_ceil1`
run (control fit, `cert` on 399 pairs, `ceil_1` and the 100-start diagnostic) took about a minute: here
two lambda-forced fits on A's block (a 64-cell block-only fit is small; the control at lambda 1 and
`ceil_100_A`), and one `cert` search on 1024 pairs (the calibration measured about 26.5 CPU-s for 399
pairs; expect the same order, perhaps two to three times that). **Expected seconds to a few minutes, well
under the 30-minute line.** Object 2 is JSON reads and two calls of the label functions; it costs
nothing.

**Consent.** The run needs the owner's yes, which is given for these two objects: DPC Research chat,
2026-09-30 15:54 UTC, Mike: "делай первые два" (the two measurements proposed by Ark: B's verdict at
lambda 1, A at lambda 100). The standing rule stays: no other run without his word (15:50:01 UTC:
"никакие прогоны не запускай без моего согласия").

## 7. Script, pins, order of commits, and the blind-review rule

- Script: `results/genome/c6/checks/symmetric_lambda_pair.py`; tests:
  `results/genome/c6/checks/test_symmetric_lambda_pair.py`; outputs (committed, refuse to overwrite):
  `results/genome/c6/checks/symmetric_lambda_pair/RESULT.md` and `result.json`.
- The script imports and does not copy: `block_b_ceil1.py`, `failed_fit_calibration.py`,
  `natural_fit_failure_replication.py`, `knockout_regrow_block_b.py` and `knockout_regrow.py`.
- `REGISTRATION_SHA256_LF_PINNED` and `PREDICTION_COMMIT_PINNED` are `None` in the script while this
  registration is under review, and the script refuses the real measurement (and `--dry-run` prints the
  refusal). It also refuses while `git status --porcelain` is not empty and if an output file exists.
- **New in this run's outputs:** `RESULT.md` and `result.json` record `git rev-parse HEAD` and the
  `git status --porcelain` text (which must be empty), beside the input hashes.
- Existing inputs pinned by LF sha256 in the script and checked in the gate: `knockout_regrow.py`
  `113c4526...9dc`, `block_b_ceil1.py` `e4b85ff1...391b`, A's `summary.json` `1337c577...a82c`, B's
  `summary.json` `a43e0319...f520`, `block_b_ceil1/result.json` `3c1e6d32...0249`; the block B, calibration
  and replication scripts as in the ceil_1 registration; A's raw store (raw sha256 `3c20e837...6006`).
- **Two-commit order.** (1) The **registration commit** (this file, final revision, with the CC slot
  filled) is the **prediction commit**: the predictions of section 5 and the trees of section 3 are frozen
  before any value exists. (2) The **script pin commit** sets `REGISTRATION_SHA256_LF_PINNED` (LF sha256
  of this file) and `PREDICTION_COMMIT_PINNED` (the commit of step 1). (3) The run, from that clean
  commit, on the owner's word.
- **No result goes into a commit subject before the owner's blind review.** The owner launches the blind
  review himself, in a separate session; until it is transcribed, the result files may be committed but
  no subject line, message or note states a value or a branch.
