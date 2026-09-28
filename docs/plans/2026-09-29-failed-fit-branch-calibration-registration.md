---
**Status: draft rev 1.3, text only, not reviewed.** Revision 1.3 (2026-09-29 UTC, CC subagent)
carries CC's **rerun** of the capacity survey into the text. CC replaced the survey folder
`docs/prereg-scripts/2026-09-29-capacity-survey/`: the rerun is at its top level, and the first run
is kept in `prev/` because rev 1.2 cited it. The rerun counts pairs exactly in float64 (a win is
d > 0, a tie is d == 0), stores every best member, and rechecks each with `Fraction`: 1,052 members,
0 mismatches, confirmed by CC's independent run of `verify_members.py`.

What changes in revision 1.3:
- **Every survey number now comes from the rerun** (`survey_log_v2.txt`): §0, §2a, §5b, §6, §8,
  §10, §11, §12, §15 and §16.
  - The 5 × 8 floor is 377/400 = 0.9425; it was 376.
  - **8 × 8 is corrected**: the minimum is 892/1,024 = 0.8711. Rev 1.2's "0.8662 (887)" came from
    the first run's float32 count and is withdrawn.
  - 10 × 10 has 3 boards ≤ 0.85 (it was 2).
  - The 13 × 13 minimum is 5,728/7,098 = 0.8070, the Paley board.
  - **The 13 × 13 claim "all 12 boards ≤ 0.85 are circulant" is now supported by the log**, which
    lists them with a circulant check.
- **Board F's 378/400 now has a carrier**: `auc_search_out.txt` and `auc_search_members.json`.
- **`cert` in §6** is defined by the rerun's method: exact counting, the member stored, the
  `Fraction` recheck.
- **§16** records which of rev 1.2's five survey findings remain: only the `flat_board` naming, now
  also in the README, plus one new remark.

Nothing was fitted or run by the drafting agent. It read the new files and checked two claims
against `survey_boards.csv` (README).

**Revision 1.2's status, as it stood:** "draft rev 1.2, text only, not reviewed." Revision 1.2 (2026-09-29 UTC, CC subagent)
applies CC's check of 2026-09-29: **RLF is invalid.** A numeric search of the free class
`a_s + b_t + u_s v_t` found a member at 378/400 = 0.945 on board F, which CC recomputed. CC's
capacity survey, 571 boards of 5 × 8 with 4 present per row, found **no board with a best-found
capacity below 0.94** (first run; the rerun's floor is 0.9425, rev 1.3). So no rank-limit world below the gate can be built on block B's shape by any
design known to this file. The survey is carried in the repository at
`docs/prereg-scripts/2026-09-29-capacity-survey/` (four files copied unchanged, with a README). It is
a design computation on constructed boards, not a value of any registered run.

What changes in revision 1.2:
- RLF is withdrawn (§4, §5).
- The absence of a rank-limit witness on 5 × 8 is declared **before values** (§2a, outcome C6 in §7).
- A **capacity search certificate** joins the separator (§6). It is sound in one direction only.
- "Fit failure" is defined against the actual fitter, with four sub-kinds read from source (§3):
  FF-sel, FF-struct, FF-quant and FF-opt. FF-quant is new: rule #2.1's decoder quantises its terms
  to 5-bit symbols.
- The rank-limit side becomes three options for Mike, with a recommendation (§5b).
- §6, §7, §8 ((v) re-derived without a rank-limit family), §9, §10, §11, §12, §13, §14, §15 and §16
  follow.
- Seed index 3 (RL2 in rev 1, RLF in rev 1.1) and index 4 (RLH) stay unused.

Nothing was fitted or run by the drafting agent. The survey's numbers are CC's; this revision read
the four files and records what it found wrong in them (README; §16).

**Revision 1.1's status, as it stood:** "draft rev 1.1, text only, not reviewed." It fixed CC's
first check: RL2 was not a rank-limit world (a hand-built member at 368/400 = 0.92). It withdrew RL2
and RLH (every RLH board has a member at 340/400 = 0.85) and introduced RLF, whose hand-built members
reached 320/400 and 326/400. The arithmetic is kept in §5a.

**Revision 1's status, as it stood:** "draft rev 1, text only, not reviewed." It was drafted
2026-09-29 UTC by a CC subagent for the backlog entry
`THE-FAILED-FIT-BRANCH-HAS-NO-SYNTHETIC-WITNESS-AND-THE-GATE-DOES-NOT-MEASURE-THE-INTERACTION`
(`backlog.md` line 22).

**Scope of every revision:**
- Nothing was fitted or run by the drafting agent. No bank was built. The real flyvis-65 bank,
  block B's private folder and the pre-run folders were not read.
- Every number not cited to a file is one of three kinds: arithmetic done in a draft (marked
  "arithmetic, this draft"), CC's survey (cited to its folder), or marked **to be fixed before
  values**.
- No gate, cut, grid, seed, block, reading rule or label string of A or B changes by this file.
  What it proposes to change is listed in §8, §13 and §14 and applies only to arms registered
  after it.
---

# Registration: calibrating the failed-fit branch with synthetic worlds of known cause

"A" is `docs/plans/2026-09-24-knockout-regrow-registration.md`; "B" is
`docs/plans/2026-09-25-knockout-regrow-block-b-registration.md` (rev 1.7.3); "RN" is
`results/genome/c6/checks/knockout_regrow_block_b/READING_NOTES.md`; "DIAG" is
`docs/plans/2026-09-28-block-b-fit-diagnostic.md`; "the B script" is
`results/genome/c6/checks/knockout_regrow_block_b.py`; "fit.py" is
`results/genome/c6/rules/second_rule_v21/fit.py`; "SURVEY" is
`docs/prereg-scripts/2026-09-29-capacity-survey/`; "A:1382" is a line of A.

## 0. Purpose, name, and the two sentences that must come first

**Name.** *The failed-fit branch: a synthetic witness of known cause, and whether the reading can
tell a failed fit from a rank limit.*

**Purpose.**
- **The branch.** A §4 sends a `ceiling_block` below `GATE_CUT` = 0.90 to U, "failed fit: rule #2.1
  cannot hold the block even when trained on it alone" (A:1328, revision 3.2 (V4, A2); B script
  line 369). A §5 reads it as "the fit, not the block, returns to review" (A:1382).
- **No synthetic world has ever met it.** `ceiling_block` = 1.0 and `lambda_block` = 1 in all 225
  rule #2.1 and BF rows, in block A's pre-run and in block B's run and reference alike (A:459–460;
  RN §3a). Block B then met the branch on the real block (0.7744; RN §1).
- **What this file does.** It builds worlds whose cause is known by construction, lands them below
  the gate, and so gives the branch its first witness (item i).
- **What it carries.** The primary-versus-family rule (item v; RN §8 item 5) is carried here because
  this file brings the witness. Item (iii), a gate on the interaction, is a separate section (§13)
  that Mike can drop without touching §§1–12.

**First sentence (before any value).** **The registered reading cannot separate a failed fit from a
rank limit.**
- Both causes produce the same object: one number, rule #2.1's `ceiling_block`, below 0.90.
- Both produce the same label text: `FAILED_FIT_TEXT` (B script line 369), chosen by `u_kind`
  (lines 1582–1596) from the reason `ceiling_block_reason` (lines 1564–1573).
- B already said so for block B: "a failed fit or a rank limit, not separated" (B:922–925; D9 at
  B:1257).
- So the registered label can be calibrated only for **reachability**. Separation needs a further
  measured object: §6 registers two, the capacity search certificate and the fixed-λ ceiling.

**Second sentence (revision 1.2, before any value).** **On block B's shape (5 × 8, 4 present per
row), no rank-limit world below the gate is known.**
- No tested board has a best-found class capacity below 377/400 = 0.9425 (§2a; SURVEY, the rerun).
- So this file witnesses the failed-fit branch **on the fit-failure side only** on this shape
  (outcome C6, declared now, §7).
- The rank side is handled per block by the certificate (§6) and, if Mike chooses, on another shape
  (§5b).

## 1. What is and is not claimed

**Claimed, if the run meets its predictions:**
- The failed-fit branch is reachable by the registered code on synthetic worlds whose cause is a
  fit failure of known sub-kind (§3). It is not reached on the reference boards (§10).
- For each world that meets the branch, the capacity certificate and `ceil_1` name the side (fit,
  not class) and, where they can, the sub-kind (§6). Counts are stated with their denominators
  (B §3.9).
- Under each option of the primary-versus-family rule (§8), what each family reads, measured.

**Not claimed:**
- **Nothing about block B.** Its label (U, failed fit) stands as registered (RN §1; B §5). No outcome
  of this file re-reads block B, and §8's rule, if adopted, applies to later arms only.
- **Nothing about any real block's rank.** Item iv (RN §8 item 4) is not this file's question.
- **No proof that a rank-limit board of block B's shape does not exist.** The survey gives lower
  bounds on 571 boards of one row count (§2a). Boards with unequal rows (block B's real block had
  2, 6, 4, 4, 3) were not surveyed.
- **Nothing about biology.**
- **Not a claim that the fit diagnostic's reading (c) is general** (RN §9). §13 uses it as a motive
  only.

## 2. Why every synthetic world so far met the gate (read from the code)

1. **The block is planted as an exact ±1 outer product.** `make_world` sets the block cells to
   `np.outer(zb, zb) > 0` (B script line 1125; A's `knockout_regrow.py` line 720). This is rank 1
   (A:416–421), and A §2.4 consequence 2 predicted `ceiling_block` ≈ 1 (A:427–431).
2. **The block-only fit sees only the block.**
   - `MASKS["block"]` = `BLOCK` (B script line 245).
   - The ceiling fit is `P.train(bank, MASKS["block"])` inside `_fit_one` (lines 1239–1266, via
     `plan_bank`, line 1309), scored at line 1474.
   - The outside cells do not enter it.
3. **So the block-only fit is a function of the board alone.**
   - The inner folds are fixed per cell (`harness.inner_folds`, `harness.py:554–555`, from
     `folds.csv`).
   - The ALS starts are fixed (`PCG64(30000 + j)`, `harness.py:666–697`).
   - Existence is fitted from labels only (fit.py:119–147; `fit_bf`, `harness.py:710–733`).
   - Block B's worlds use two boards (`FAMILIES`, B script lines 322–324). **By the code path, the
     225 rows are 2 boards × 5 predictors = 10 distinct block-only problems, repeated.**
   - This is *to be confirmed before values* on the stored `p` vectors of the pinned reference
     (read-only).
   - Consequence for this file: a family whose board is the same in every world gives one gate
     measurement, not five (§4).
4. **The gate is read only after R and W are excluded.** In `read_label` (B script lines 1599–1631),
   `gate` is computed only in the `else` branch (line 1620), and the failed-fit reason is appended
   only there (line 1626). So every witness world needs an outside that carries no block structure.

## 2a. The design finding (revision 1.2): class capacity on block B's shape

- **What was searched** (rev 1.3: the rerun, SURVEY top level; the first run is in `prev/` and is
  superseded).
  - The class is the free class `a_s + b_t + u_s v_t` (no penalty, no offset, no quantisation).
  - The search is Adam on an annealed sigmoid surrogate of AUC.
  - Stage 1 runs every board at 100 starts; stage 2 reruns the 10 lowest 5 times at 500 starts; a
    deep pass runs 2 seeds at 1,200 steps (`survey.py`, `run_survey.py`).
  - Counting is **exact** in float64 (win d > 0, tie d == 0). Every best member is stored
    (`members_*.json`) and recounted with `Fraction`, with 0 mismatches over 1,052 members.
- **Results on 5 × 8 with 4 present per row** (SURVEY `survey_log_v2.txt`):

  | board set | boards | lowest best-found capacity |
  |---|---|---|
  | random | 300 | 0.945 |
  | all 21 Walsh–Hadamard 5-sets | 21 | 0.9425 |
  | Walsh–Hadamard rows and complements | 150 | 0.9425 |
  | boards with always- and never-present columns | 100 | 0.9775 |
  | **all** | **571** | **0.9425 (377/400)** |

  The median is 0.985. No board fell below 0.90, and no 5 × 8 board is flagged unstable (rerun
  spread above 2 of 400).
- **Board F** (rev 1.1's RLF) has a member at 378/400 = 0.945 (`auc_search_out.txt`: surrogate
  seed 2; `Fraction` recount 378; member in `auc_search_members.json`). The RL2 control reaches
  400/400. The discrete search reaches 350.5 on F.
- **Every value is a lower bound**, since a found member is a witness. It cannot show that a board
  is below 0.90. Rev 1.3: the counts are exact for the stored members, so the float32 caveat of
  rev 1.2 no longer applies.
- **Larger shapes, about half present per row** (for §5b only):

  | shape | lowest best-found | boards < 0.90 | boards ≤ 0.85 | flagged unstable (largest spread) |
  |---|---|---|---|---|
  | 8 × 8 | 892/1,024 = 0.8711 (#163, circulant) | 22 of 220 | 0 | 3 boards (7 of 1,024) |
  | 10 × 10 | 2,115/2,500 = 0.846 (#138, circulant) | 17 of 160 | 3, all circulant | 6 boards (25 of 2,500) |
  | 13 × 13 | 5,728/7,098 = 0.8070 (#100, the Paley board) | 61 of 101 | 12, all circulant | 9 boards (104 of 7,098) |

  - On 13 × 13 the log lists the 12 boards ≤ 0.85 with a circulant check, and none is
    non-circulant.
  - The lowest non-circulant board is 0.8629 on 13 × 13, 0.8896 on 10 × 10 and 0.8926 on 8 × 8.
    The 13 × 13 value is the log's `rand` group minimum; all three were checked against
    `survey_boards.csv` (SURVEY README).
- **Consequence.** On 5 × 8 with 4 per row, every board tried has class capacity ≥ 0.9425, far above
  the gate. So a `ceiling_block` below 0.90 on such a board would have a fitter cause, not a class
  cause. That is why the rank side is not witnessed here (C6), and why the certificate of §6, run on
  a given block, can exclude a rank limit for that block without any synthetic rank-limit world.

## 3. The causes, defined against the actual fitter

**The class.** Rule #2.1's existence logit is `c + a_s + b_t + u_s v_t + W[G(s), G(t)]` (A §2.1; fit.py
`fit_uvw`, 97–112, and `logit_grid`, 115–116).
- **On block B's 13 types, W is a column effect.** L1–L5 are `stride_u` 1 with role "intermediate".
  Mi1, Mi4 and Mi9 are "intermediate"; Tm1, Tm2, Tm3, Tm4 and Tm9 are "output"
  (`results/genome/bank/types.csv`). `groups` sets G = role code when `stride_u` ≤ 1 (fit.py:82–88).
- **So on this shape, rule #2.1's class equals the free class of §2a**: additive terms plus one rank-1
  term, with the column effect absorbed into b.
- **BF_1's class (`fit_bf`) is not the same object.** It is N1's fixed additive offset plus `U V^T`,
  with the additive part not free.

**The fitter, as the registered path runs it** (the block-only fit is `P.train` then `P.decode`;
B script lines 1239–1266):

1. **N1 first, alone.**
   - `fit_existence` calls `H.fit_n1(view)` (fit.py:124; `harness.py:350–399`).
   - That is `ridge_logistic` (`harness.py:314–323`) on the design [intercept | 65 source indicators
     | 65 target indicators] (`harness.py:352–356`).
   - The penalty vector is 1 except the intercept (`pen[0] = 0`, line 358), and λ = `LAMBDA` = 1
     (`harness.py:67`). The gradient is `Xᵀ(p − y) + λ·pen·w`: log-loss + ½(|a|² + |b|²), c free.
   - It is fitted on the view's cells only. Types outside the block get a = b = 0 from the penalty.
   - **These a, b, c are never refitted jointly with u·v.** The logit grid O built from them
     (`_n1_logit_grid`, `harness.py:697–699`) is a fixed offset from here on.
2. **λ by the nested inner folds.**
   - Each inner fold refits N1 on its subview, then runs step 3 for every λ in `LAMBDAS` =
     [1, 3, 10, 30, 100] (fit.py:57, 128–140).
   - It chooses by inner held-out log-likelihood, with ties within `LAMBDA_TIE` = 1e-9 going to the
     larger λ (fit.py:68, 141–142).
3. **`fit_uvw` at the chosen λ** (fit.py:97–112).
   - Start with W = 0, then `ROUNDS` = 3 rounds (fit.py:55) of two steps.
   - (i) `bf_als` at rank 1 with offset O + W[G, G] (fit.py:108). Its objective is log-loss +
     ½λ(|u|² + |v|²) (`_bf_objective`, `harness.py:660–663`). It runs 25 row-Newton sweeps
     (`BF_SWEEPS`, `harness.py:536`) from 10 starts and keeps the best penalised training objective
     (`harness.py:666–697`).
   - (ii) W by `ridge_logistic` on the 16 group-pair indicators, with offset O + u·v, penalty 1 and
     λ = `MU` = 1, no intercept (fit.py:109–111; `MU`, fit.py:56).
   - O itself is not touched.
4. **Quantisation** (`ExistQ`, fit.py:172–265; called from `fit`, fit.py:362–368).
   - u and v are rebalanced so that max|u| = max|v|.
   - a and b share one scale over all 65 types; u and v share one scale; W has its own.
   - Each is rounded to a 5-bit symmetric symbol: 32 levels, value = scale·(q − 16)/16, scale =
     max|x|·16/15 (`SYM`, fit.py:59; `sym_scale`/`to_sym`, fit.py:150–160).
   - One coordinate-descent pass (q ± 1) on the penalised objective follows (`descend`,
     fit.py:230–247). The objective is ½|a|² + ½|b|² + ½λ(|u|² + |v|²) + ½`MU`|W|², per the
     `ExistQ` docstring.
   - Then c is refitted in float32 (`refit_c`, fit.py:249–265).
5. **Decode.** `decode.py` line 13 rebuilds `z = c + a[s] + b[t] + u[s]v[t] + W[g[s], g[t]]` from the
   symbols. **BF_r is not quantised:** `bf_decode.py` adds `U_s·V_t` to N1's logit after the
   harness's float32 cast (`cast`, `harness.py:273–278`).

**Definitions**, for a block pattern y and rule #2.1:
- **`cap(y)`:** the supremum of in-sample AUC over the free class of §2a. It is a property of the
  class and the pattern.
- **`cert(y)`:** the capacity search certificate (§6): the best AUC found for an explicit member,
  rechecked in float64. It proves `cap(y) ≥ cert(y)`.
- **`ceil_λ(y)`:** the in-sample AUC of the **registered path** (steps 1, 3, 4, 5) with the grid set to
  the single value λ (no nested choice). **`ceil_1`** is the one at λ = 1, the grid's floor.
- **`ceiling_block(y)`:** the registered object (steps 1–5).

**The causes** (only when `ceiling_block` < 0.90):

| cause | definition | built here? |
|---|---|---|
| **Rank limit (RL)** | `cap(y) < 0.90`: no member of the class passes the gate | no (§2a, §5b) |
| **FF-sel** | `ceil_1 ≥ 0.90`: the registered path passes at the grid's floor, and the nested choice picked a λ whose fit does not (block B's pattern by RN §9: λ = 100, the rank term collapsed) | yes: FC forced, FN natural |
| **FF-struct** | `cap ≥ 0.90`, but the fitter's optimum passes at no λ of the grid. The fixed N1 ridge (½ penalty on a and b, fitted before u·v and never refitted), the penalty on u·v and W, the log-loss objective and the rank-1 alternation keep it below the gate even at λ = 1 before quantisation | not constructed |
| **FF-quant** | the float fit at λ passes, the 5-bit quantised model (steps 4–5) does not. Rule #2.1 only | not constructed |
| **FF-opt** | the fitter's own penalised objective has a better optimum that passes, which the registered starts miss | not constructed (Q-J2) |

**What `ceil_1` can and cannot tell apart.**
- It separates **FF-sel** (`ceil_1` ≥ 0.90) from the other three (`ceil_1` < 0.90).
- It cannot separate FF-struct, FF-quant and FF-opt from one another, and on its own it cannot
  separate any of them from RL.
- `cert` ≥ 0.90 separates all four FF kinds from RL.
- Two printed diagnostics narrow the rest, as lower bounds only (§6):
  - `ceil_1_float`, the AUC of step 3's float output at λ = 1 before step 4, separates FF-quant from
    FF-struct/FF-opt.
  - `ceil_1_starts100`, step 3 at λ = 1 with 100 starts, can show FF-opt; it cannot prove FF-struct.
- **Whether FF-quant is a "fit failure" at all is a question of what the rule is** (Q-A5). The
  quantised representation is the registered rule's own decoder. A limit it imposes is a limit of the
  rule's representation, not of the optimiser, though not a rank limit either.

## 4. The world families (revision 1.2: fit-failure side only)

**Common to all worlds:**
- The harness grid, block B's 40 cells, `TYPE_FIELDS`, `folds.csv`, N1's degree terms on block B's
  knockout view (`degree_terms`, B script lines 1097–1102) and the content pool of B §3.6.
- 99 shuffles, 9,999 permutations, both ceilings and the BF family, **read by the registered code**
  (B script lines 1441–1631).
- **Outside: γ_z = γ_z1 = 0** (the Nf outside), so R and W are not expected (§2, fact 4).

**Board per world.** Each natural family varies its board across worlds (§2, fact 3), so its 5
worlds give 5 gate measurements.
- This departs from B's D4 (i) (B:1252).
- `smallest_passing_auc` is computed per world (B script line 1523). The one-value-per-board check
  is not registered for these families (S-C5).

| family | cause | block pattern | present | varies per world by | certificate | worlds |
|---|---|---|---|---|---|---|
| **FC** (control) | FF-sel, forced | the z board of B §3.6 | 20 / 40 | nothing | the planted score, AUC 1 (exact) | 5 (one board) |
| **FN1** | FF-sel expected, natural | z board, 1 present and 1 absent cell swapped | 20 / 40 | which cells (seeded) | planted score, 380/400 = 0.95 (exact) | 5 |
| **FN2** | as FN1 | z board, 2 + 2 cells swapped | 20 / 40 | which cells (seeded) | planted score, 360/400 = 0.90 (exact) | 5 |

**Withdrawn** (arithmetic in §5a):

| family | revision | reason |
|---|---|---|
| RL2 | 1.1 | a member at 368/400 = 0.92 |
| RLH | 1.1 | every board has a member at 340/400 = 0.85 |
| RLF | 1.2 | a member at 378/400 = 0.945, found by search (§2a) |

**The swap rule of FN1/FN2 (to be fixed before values).** Swaps keep 20 / 40 present, drawn uniformly
by the world's seed. Whether a swap may touch the single-cell inner fold is open (Q-J1).

**Why FC is a control, not a world.**
- FC's block-only fit of rule #2.1 runs with the grid set to `[100]`, by the module-global swap of
  `train_fixed_lambda` (B script lines 1213–1236, which sets `fit.LAMBDAS`, fit.py:57).
- It is not read by exactly the same code as the real bank (A:932–934).
- So it witnesses the branch's mechanics, not the instrument on a world.

**Seeds (proposed; to be checked before values).**
- The range is 93000–93999. World `j` of family index `i` gets `93100 + 10 i + j`, with FC, FN1,
  FN2 = 0, 1, 2. **Indices 3 and 4 stay unused** (rev 1 RL2/RLH, rev 1.1 RLF).
- The permuted-board reference (§10) takes 93010–93108.
- `git grep -n -E '\b93[0-9]{3}\b' -- '*.py'` found no use (2026-09-29). The script asserts
  disjointness from A's, B's and the male arm's seeds (B script lines 1031–1063).
- The survey's own seeds (2026, 11, 100–104, 0–2; SURVEY README) are not seeds of this registration.

## 5. Certificates fixed before any fit

- **FF families:** the AUC of the planted score `z_s z_t` on the world's labels, exact arithmetic.
  - With k present and k absent cells swapped on a 20 / 20 board, AUC = ((20 − k)² + (20 − k)k)/400.
  - FC: 1. FN1 (k = 1): 0.95. FN2 (k = 2): 0.90.
  - The planted score is a member of the class, so `cap` ≥ this value, and a world that meets the
    branch has a fitter cause by construction.
  - **FN2 sits exactly at the cut** (Q-A2).
- **Additive-only AUC of each board:** printed per world, **to be fixed before values** by an exact
  computation over additive scores.
  - For orientation: a column-only score on the z board has AUC 0.60 (arithmetic, rev 1).
  - That is not the maximum.

### 5a. The withdrawn rank-limit boards, with their arithmetic (kept from revisions 1.1 and 1.2)

All counts are out of the 20 × 20 = 400 present × absent pairs, with a tie worth ½.

- **R(m)** (one direction; m rows perfect; a = b = 0): 16m² + 8m(20 − 4m) + ½(20 − 4m)².
  - m = 1 gives 272 (0.68).
  - m = 2 gives 328 (0.82).
  - m = 3 gives 368 (0.92).
- **RL2** (3 rows on ±z, 2 on ±z′): R(3) = 368/400 = 0.92 > 0.90 (CC's check, rev 1.1).
- **RLH** (five distinct Walsh–Hadamard rows):
  - Take one row perfect, plus a column term equal to the column sum S′ of the other four rows.
  - S′ has one of three profiles, giving 336, 340 or 328 in all.
  - The parity and sum-of-squares of the Hadamard column sums (Σ S² = 40, S odd) leave at most one
    row off the 340 profile.
  - So every RLH board has a member at 340/400 = 0.85.
- **RLF** (board F: rows {0,1,4,5}, {2,3,4,6}, {0,2,5,7}, {0,1,3,6}, {1,2,3,7}):
  - The hand-built members reached 320/400 and 326/400 (rev 1.1).
  - The search found 378/400 = 0.945 (rev 1.2; §2a). Withdrawn.
- **The rev 1.1 lesson.** A rank-limit family needs a lower-bound check before any upper bound is
  sought. A hand check is not enough: the search raised F from 0.815 to 0.945.

### 5b. The rank-limit side: options for Mike and the reviewers (not chosen)

| option | what it does | what it changes | what it cannot do |
|---|---|---|---|
| **(a)** 5 × 8, fit-failure side only | FC + FN on block B's shape. The rank side of a failed fit is closed **per block** by the certificate (§6): `cert ≥ 0.90` excludes a rank limit for that block | nothing beyond §§4–14 | it gives the branch no rank-limit witness; C6 stands |
| **(b)** a synthetic-only rank-limit family on a larger block shape (for example 13 × 13 circulant boards: 12 of 101 boards ≤ 0.85 best-found, all circulant; the lowest non-circulant board is 0.8629) | worlds whose class capacity is plausibly below the gate | **a different block:** a new mask of 169 cells on 26 types; the fixed folds of `folds.csv` restricted to those cells (a different fold composition, perhaps new single-class folds); N1 fitted on a different view; other leg-P arithmetic and `smallest_passing_auc` grid; a new seed set. **W is not a column effect in general:** if the 26 types span several field groups, rule #2.1's class adds `W[G(s), G(t)]` interactions that the survey's class lacks, so the survey does not bound it unless the types are chosen with one group on one side. **The RL membership still rests on best-found values**, which moved by up to 104 of 7,098 between reruns (9 of the 13 × 13 boards flagged unstable), and no upper bound is proved | **it does not calibrate block B's shape:** the gate's behaviour on a 169-cell block with other folds says nothing about how a 40-cell block fails |
| **(c)** both | (a) now; (b) as its own registration | as (a), then as (b) | as each |

**Recommendation: (a).**
- The question the branch leaves open on block B's shape is "fit or class?". On this shape the
  class side is excluded by certificate on every board tried. The certificate answers the question
  for any given block directly, which a synthetic rank-limit world on another shape could not.
- (b) would witness the rank side of a different instrument configuration, with a membership that
  is not proved.
- Take (b) up only when a block of that size is proposed for a knockout, as part of that block's
  own registration (Q-M5).

## 6. The separator and the predictions (written before values)

**The separator.** It is printed for every world and every predictor, beside the registered
objects. It decides nothing about the label.

1. **`cert`, the capacity search certificate (revision 1.2; method as the rerun, rev 1.3).**
   - The survey's search (`survey.py`, `best_auc`, SURVEY top level) runs on the block's pattern,
     **before any fit**. Its budget is to be fixed before values; the rerun's staging (100, then
     5 × 500 starts, then 2 deep seeds at 1,200 steps) is the proposal.
   - Pairs are counted **exactly** in float64 on the float64-cast member: a win is d > 0 and a tie
     is d == 0, with no tolerance.
   - The best member is **stored**, recounted with `Fraction` (`frac_count`), and recounted once
     more by the registered `auc` (B script lines 791–801: exact comparison, ties counted ½). All
     three counts must agree, or the certificate is void.
   - `cert` is the agreed count.
   - **`cert` ≥ 0.90 proves the class holds the block**: the stored member is the witness.
   - `cert` < 0.90 proves nothing.
   - The rerun spread is printed beside it. In the survey, no 5 × 8 board was flagged unstable;
     spreads reached 7 of 1,024 on 8 × 8, 25 of 2,500 on 10 × 10 and 104 of 7,098 on 13 × 13.
   - For FC and FN, the certificate of §5 is exact, and `cert` is printed as a cross-check.
2. **`ceil_1`**, the fitter-side measurement (§3).
3. **`ceil_1_float` and `ceil_1_starts100`**, diagnostics (§3).

| registered `ceiling_block` | `cert` | `ceil_1` | `ceil_1_float` | reads |
|---|---|---|---|---|
| ≥ 0.90 | any | any | any | gate passed |
| < 0.90 | ≥ 0.90 | ≥ 0.90 | any | **fit failure, FF-sel** |
| < 0.90 | ≥ 0.90 | < 0.90 | ≥ 0.90 | **fit failure, FF-quant** |
| < 0.90 | ≥ 0.90 | < 0.90 | < 0.90 | **fit failure, FF-struct or FF-opt, not separated** (`ceil_1_starts100` ≥ 0.90 names FF-opt) |
| < 0.90 | < 0.90 | any | any | **not separated: rank limit or fit** (no witness either way) |

**Direction of soundness.** A "fit failure" row is sound: a stored member passes the gate. The last
row is not a rank-limit reading.

**Predictions.**

| family | registered label | `ceiling_block` (rule #2.1) | `cert` | `ceil_1` | reads | stop if |
|---|---|---|---|---|---|---|
| FC | U, failed fit, in 5 of 5 | additive-only value of the z board (< 0.90), all 5 equal | 1 (exact) | 1.0 (as block B's pre-run `lambda_block` 1 fits, RN §3a) | FF-sel | any world not failed fit; `ceiling_block` ≥ 0.90 (the forcing did not act); `ceil_1` < 0.90 (the planted board failing at λ = 1 would contradict the pre-run) |
| FN1 | not predicted: failed fit if the nested choice collapses, else G or threshold U | < 0.90 if collapsed | ≥ 0.95 (exact) | ≥ 0.90 expected | FF-sel where the branch is met, else the row the separator gives | none (a count, §7) |
| FN2 | as FN1 | as FN1 | ≥ 0.90 (exact) | ≥ 0.90 expected, at the cut | as FN1 | none |

- **Stops on R and W.** An R or W on any world is a stop, as on B's Nf (`REQUIREMENTS`, B script
  lines 353–363).
- **No threshold U when the gate fails.** A failed-fit reason takes precedence (`u_kind`,
  lines 1582–1596).

## 7. The witness test, and the calibration's outcome labels

**The witness test (revision 1.2).** The design can separate "fit" from "class" on a world that meets
the branch if the separator reads a **fit-failure** row wherever the construction says fit. The
certificate guarantees this for FC and FN: an exact member passes the gate. So the fit side of the
test is decidable in every world.

The informative part is **the sub-kind**:
- FC must read FF-sel (its cause is the forced selection).
- An FN world that meets the branch reads FF-sel, or reveals FF-struct/quant/opt on a board the
  class holds.

The class side of the test has no world on this shape (C6).

| family | decidable? |
|---|---|
| FC | yes (exact certificate; `ceil_1` measured) |
| FN1 | yes, where the branch is met; whether it is met is a count |
| FN2 | yes, at the cut (Q-A2) |
| rank-limit families | none on 5 × 8 (§2a, §5a); option (b) of §5b would need its own test |

**Outcome labels (every one named before values; revision 1.2 renumbers them):**

| label | condition | what it licenses |
|---|---|---|
| **C1: fit side witnessed, natural and forced** | FC reads FF-sel in 5 of 5, and at least one FN world meets the branch and reads a fit-failure row | a later registration may print `cert` and `ceil_1` beside a failed fit and name the side (and the sub-kind where the table names one); the label text changes only by a reviewed revision (S-C7) |
| **C2: fit side witnessed, forced only** | FC as in C1; no FN world meets the branch | as C1 for FC's mechanics; a natural FF-sel is not shown at these parameters |
| **C3: sub-kind not identified** | some world meets the branch with `cert` ≥ 0.90 and `ceil_1` < 0.90, and neither diagnostic names the sub-kind | the side (fit) is named; the sub-kind stays "FF-struct or FF-opt, not separated" |
| **C5: branch not reached / stop** | a stop row of §6 fires | a design error; the run stops |
| **C6 (declared before values, for block B's shape): no rank-limit witness** | stands from §2a, whatever the run gives | the failed-fit branch is witnessed on the fit side only on 5 × 8. For a given 5 × 8 block, `cert` ≥ 0.90 closes the rank side; `cert` < 0.90 leaves "a failed fit or a rank limit, not separated" (B's D9). No proof that no rank-limit board of this shape exists |

(Rev 1.1's C1–C4 assumed a rank-limit family and are withdrawn. C4 has no successor, because no
world can break the fit side of the test when every FF certificate is exact.)

## 8. (v) Primary versus family (carried because this file brings the witness)

**What it is (RN §8 item 5; RN §2).**
- The G row reads the gate on rule #2.1 alone (A:1327; A:458–459; `read_label`, B script line 1620).
- Read on BF_1, block B's label would have been G (RN §2).
- Ark's condition: change this rule only in a registration that brings a witness, justified by the
  narrowness known before the run.

**Options:**

| option | gate for G | on a later block |
|---|---|---|
| **(v-a)** primary (as registered) | rule #2.1's `ceiling_block` ≥ 0.90 | unchanged |
| **(v-b)** both D1 candidates | rule #2.1 and BF_1 each ≥ 0.90; disagreement gives U with a new reason (mirrors A:1302–1308) | stricter; a new label string |
| **(v-c)** family, any member | max over rule #2.1 and BF_1–BF_4 ≥ 0.90 | looser; matches G's family wording (A:1327) |
| **(v-d)** family, every member | every member ≥ 0.90 | strictest |

**(v) re-derived without a rank-limit family on 5 × 8 (revision 1.2).**
- **BF_4 holds every 5 × 8 pattern** (algebra, rev 1.1).
  - Choose U (5 × 4) with column space w^⊥, w free of zeros, and ±sign(w) outside the board's at
    most 8 column patterns.
  - Every other orthant is then reachable, so a large common scale over N1's fixed offset gives
    AUC 1.
  - So on this shape (v-c) passes whenever BF_4's nested choice does not collapse, whatever the
    board. **(v-c) reads selection, not capacity.**
- **Rule #2.1's class holds every surveyed 5 × 8 board at ≥ 0.9425** (§2a).
  - So on this shape the options differ only through the **fitters' selection and structure**
    (FF-sel, FF-struct, FF-quant, FF-opt of rule #2.1 against BF_1–BF_4's own fits).
  - They do not differ through capacity.
- **The witness is FC.** Its rule #2.1 fit is forced into the tail and its BF fits are not.

  | family | (v-a) | (v-b) | (v-c) | (v-d) |
  |---|---|---|---|---|
  | FC | ff | U, "the D1 candidates disagree on the gate" (BF_1 holds the z board at λ = 1: pre-run `ceiling_block` 1, RN §3a) | G | ff |
  | FN1, FN2 | as their registered label | depends on BF_1's own selection | G wherever some member passes | ff wherever any member fails |

  ("ff" = U, failed fit.) FC separates {(v-a), (v-d)} from (v-b) and from (v-c).
- **What no family here separates.**
  - (v-a) from (v-d): that needs a BF_r to fail where rule #2.1 passes (Q-W1).
  - Any option by capacity (C6).
- This file does not choose. Whatever is chosen applies to later arms; block B is not re-read.

## 9. Thresholds

| name | value | status |
|---|---|---|
| `GATE_CUT` | 0.90 | registered (A:458–459; B script line 273); unchanged |
| `P_R`, `P_W`, `P_G`, `MECHANISM_CUT` | 0.01, 0.0125, 0.10, 0.90 | registered (B script lines 273–277); unchanged |
| λ grid, tie | [1, 3, 10, 30, 100]; 1e-9 to the larger λ | registered (`harness.py:535`, `:727–728`; fit.py:57, 68, 142); unchanged |
| `STARTS` | 10 | registered; unchanged |
| `LAMBDA_CAP` | 1 | proposed (the grid's floor; B script line 288) |
| certificate and capacity cut | 0.90 | proposed, borrowed from `GATE_CUT`, not calibrated |
| certificate budget (K, steps, reruns) | K and steps to be fixed; at least 5 reruns; the recheck by the registered `auc` in float64 | **to be fixed before values** |
| starts for `ceil_1_starts100` | 100 | proposed |
| swaps in FN1 / FN2 | 1 + 1, 2 + 2 | proposed; FN2 at the cut (Q-A2) |
| worlds per family | 5 | proposed |
| `RL_MARGIN_CUT` | — | **withdrawn** with the rank-limit families (rev 1.2) |

## 10. The null and the references

- **Gate-passing reference (reused, not rerun).** Block B's pinned reference: the z and z′ boards
  with `ceiling_block` 1.0 (RN §3a), read-only. §2's "2 boards" applies.
- **Permuted-board reference (new, printed, decides nothing).**
  - 99 uniform permutations of the z board's 40 labels (seeds 93010–93108), block-only fits only.
  - Printed per board: `ceiling_block`, `ceil_1`, `ceil_1_float` and `cert` for rule #2.1, and
    `ceiling_block` for BF_1–BF_4.
  - It is the one place where the separator meets patterns that are not rank 1. It shows how often
    the registered path fails on boards the class holds, since the survey puts every 4-per-row
    5 × 8 board at ≥ 0.9425. Permuted boards need not have 4 per row, so the survey does not cover
    them, and their `cert` is measured.
  - A permuted board is never a world of this registration.
- **Not a reference.** Block B's real table (RN §3b) is post-data (Q-M3).

## 11. Compute and instrument

- **Certificates.** At survey scale the 5 × 8 stage took 169 s for 571 boards: 94 s at 100 starts,
  38 s of refinement, 37 s of deep pass, and the `Fraction` recheck under 1 s (SURVEY
  `survey_log_v2.txt`). For 15 worlds and 99 permuted boards at the registered budget, the estimate
  is **to be fixed before values** (minutes).
- **Block-only fits** (the gate, `ceil_1`, `ceil_1_float`, `ceil_1_starts100`, the permuted boards):
  seconds each; minutes in all.
- **Full reading of the 15 worlds** (FC, FN1, FN2).
  - A's synthetic step took 85 min for 45 worlds on 30 CPU workers (`backlog.md`, the GPU entry).
  - Scaled, 15 worlds take about 28 min (arithmetic, this draft). This is **to be fixed before
    values** from a timing of one world of block B's shape.
- **GPU: not used.**
  - The GPU instrument is validated only for BF_1–BF_4 on the `ko` mask (GPU registration D1 (a),
    line 263).
  - Block-only fits, fixed-λ fits and rule #2.1 are outside that scope (D1 (b)–(d)).
  - D11 (line 273) requires the hybrid to be named before a pre-run.
  - The survey's search is a separate numpy computation, not the GPU instrument.
  - **Recommendation: CPU for every number.**

## 12. What would change a reading

- **FC failing its own predictions.** An FC world with `ceil_1` < 0.90 contradicts the pre-run's
  λ = 1 fits of the z board: a stop (C5), and the registered path is examined before anything is
  read. An FC world with `ceiling_block` ≥ 0.90 means the forcing did not act (C5).
- **A board below the survey's floor.** A 5 × 8 board with 4 per row and `cert` < 0.9425 at the
  registered budget would move §2a's floor. A board with a proved `cap` < 0.90 would withdraw C6's
  "no rank-limit witness known" for this shape.
- **The float32 caveat** (rev 1.2) is resolved by the rerun (rev 1.3): its counts are exact and its
  members stored. A new `verify_members.py` mismatch would void the affected values.
- **The "2 boards" claim not confirmed** (§2): the sentence is corrected; the per-world board
  variation stays.
- **Rule #2.1 at λ = 1 on block B's own labels** is not part of this file and is not computed under
  it (§16).

## 13. Separate section, optional: (iii) a gate that measures the interaction

**Take or drop as a whole; §§0–12 do not depend on it.**

**Motive (RN §9; DIAG §5).**
- On block B's inner folds the registered grid did not separate λ = 1 from "no interaction" robustly.
- λ = 100 was preferred by m = +0.435 nat, of which 0.39 came from the one-cell fold.
- Fewer than half of the two-class folds preferred λ = 100, and removing fold 9 alone reversed the
  choice.
- For rule #2.1, λ ≥ 3 collapsed the rank term, so its grid was in effect {1, off}.
- The registered gate is therefore read on the additive part whenever the choice collapses
  (RN §3a).
- Zcode's point (RN §8 item 2): gate on the interaction.

| option | the object | what it needs |
|---|---|---|
| **(iii-a)** fixed λ | `ceiling_block` at λ = `LAMBDA_GATE`, no nested choice | a value (1, or below 1, to be fixed); a new label reason |
| **(iii-b)** interaction share | AUC of the fitted `u_s v_t` term alone, or the full score's AUC minus its additive part's | a definition invariant to the additive terms; an uncalibrated cut |
| **(iii-c)** nested choice, repaired | the grid extended below 1, and label-stratified inner folds for the block-only fit (every fold holds both classes) | a new fold object, not `folds.csv` (whose `stratum` column encodes the real bank's presence, `make_folds.py:89`) |

**AD, the additive board.** Present iff `a_s + b_t` > threshold (20 of 40), built so that the
additive terms alone reach AUC 1 with u·v = 0. The registered gate passes it; (iii-b) should fail it.
FC and FN are the witness that (iii-a) and (iii-c) pass boards the class holds where the registered
choice collapsed.

| family | registered gate | (iii-a) λ = 1 | (iii-b) | (iii-c) |
|---|---|---|---|---|
| FC | fails | passes | passes | passes if the repaired choice keeps λ ≤ 1 (measured) |
| FN1, FN2 | fails where collapsed | passes if `ceil_1` ≥ 0.90 | passes if the interaction survives the swaps | measured |
| AD | passes | passes | **fails** | passes |

A gate of (iii) would bring new label strings, reviewed with an injection test, and would apply to
later arms only. Under (iii-a) the FF-sel sub-kind disappears by construction; FF-struct, FF-quant
and FF-opt remain (§3).

## 14. Script changes needed (listed; none is made by this draft)

| # | change |
|---|---|
| S-C1 | a new script, a copy of the B script (A's and B's files byte-unchanged), with `FAMILIES` = FC, FN1, FN2 and the Nf outside |
| S-C2 | the FN board builder (seeded swaps); `make_world`'s assertion of 20 present kept |
| S-C3 | the forced-grid block-only fit for FC: `train_fixed_lambda`'s global swap on `MASKS["block"]` (today hard-wired to `MASKS["ko"]`, B script lines 1225, 1231) |
| S-C4 | `ceil_1` on the block mask for rule #2.1 and BF_1–BF_4 |
| S-C4a | `ceil_1_float`: the AUC of `fit_existence`'s float output at λ = 1 (fit.py:119–147, before `ExistQ`), computed by calling it on the block view; `ceil_1_starts100`: the same with `starts` = 100 |
| S-C5 | `smallest_passing_auc` per world |
| S-C6 | `cert`: the survey's `best_auc` at the registered budget, the best member rechecked in float64 by the registered `auc` (B script lines 791–801), its parameters stored, the rerun spread printed; the exact certificates of §5 printed beside it. The search code is copied from SURVEY with its hash, not imported from the scratchpad |
| S-C7 | the separator's reading printed beside the label; **the label text unchanged** |
| S-C8 | the permuted-board reference |
| S-C9 | (§8) the four gate options computed and printed per world; only the registered one sets the label |
| S-C10 | (§13, if taken) AD and the (iii) objects |
| S-C11 | seeds of §4 asserted disjoint; callers read from the Orbit graph and confirmed by grep at the script's review (B §3.9) |

## 15. Open questions

**For the reviewers.**
- **Q-A1 (Ark; rev 1.2 replaces the old Q-A1 and Q-A4; rev 1.3 narrowed).** Is the survey adequate
  as §2a's ground? Rev 1.3's rerun settles the counting (exact, members stored and rechecked) and
  F's carrier. What remains open:
  - Should boards with unequal rows, like block B's real 2, 6, 4, 4, 3, be surveyed before C6 is
    stated? The survey has one row count (4 per row).
  - Is the search budget enough, given the instability on the larger shapes?
- **Q-A2 (Ark).** FN2 sits exactly at the cut. Keep it, or use k = 1 only?
- **Q-A3 (Ark).** Confirm §2's "10 block-only problems" on the stored `p` vectors.
- **Q-A5 (Ark, Johnny; rev 1.2).** Is FF-quant a fit failure, or a limit of the rule's registered
  representation? The 5-bit symbols are part of rule #2.1's decoder and its description length; BF_r
  has none.
- **Q-J1 (Johnny).** Should FN swaps target the single-cell inner fold, or be drawn uniformly?
- **Q-J2 (Johnny).** Should FF-struct or FF-opt get a constructed control, for example a start budget
  of 1, or N1's ridge refitted jointly (a changed fitter, like FC's forced grid)?
- **Q-W1 (Warren).** Are "5 of 5" requirements for FC right at one board? Is a family needed where a
  BF_r fails and rule #2.1 passes, to separate (v-a) from (v-d)?
- **Q-Z1 (Zcode).** (iii): which option; for (iii-a), which λ; for (iii-c), which split.
- **Q-Z2 (Zcode).** Confirm that `ceil_1` and `cert` are free of the single-class-fold problem: neither
  has a nested choice.

**For Mike (each with what it affects; recommendation last).**
- **Q-M1: which items.** (i) + (v) only, or with (iii). *Recommendation: (i) + (v) first.*
- **Q-M2: instrument.** *Recommendation: CPU* (§11).
- **Q-M3: block B's own table as a world.** *Recommendation: no* (post-data).
- **Q-M4: (v).** *Recommendation: choose after the values.*
- **Q-M5: the rank-limit side (§5b).** (a) 5 × 8 fit side only, with the certificate closing the rank
  side per block; (b) a synthetic rank-limit family on a larger shape; (c) both. *Recommendation:
  (a).* The certificate answers "fit or class?" for any given 5 × 8 block. (b) calibrates a different
  mask, folds and N1 view, with unproved membership, and does not calibrate block B's shape.

## 16. Not verified at drafting; findings about the survey; one post-data observation

**Not verified:**
- §2's "2 boards" (code path only).
- Every value marked "to be fixed before values".
- The GPU registration's line numbers as read on 2026-09-29.

**Findings about the survey.** Rev 1.2 raised five problems about the first run; rev 1.3 checked
them against the rerun, reading all of SURVEY's top-level files.

1. **Board F's 0.945 had no printout.** **Resolved:** `auc_search_out.txt` prints the search and the
   `Fraction` recount (378), and `auc_search_members.json` stores the member.
2. **float32 counts.** **Resolved:** the search dynamics are still float32, but every count is exact
   float64 on the stored member (`survey.py` `best_auc`, "wins d>0, ties d==0"). Every member is
   recounted with `Fraction`, and the logged mismatch lists are empty.
3. **The 8 × 8 minimum.** **Superseded:** rev 1.2's "0.8662 (887/1,024), not 0.873" read the first
   run's float32 count of an unprinted board. The rerun's exact minimum is 892/1,024 = 0.8711
   (#163). Rev 1.2's correction is withdrawn.
4. **"All 12 on 13 × 13 are circulant".** **Resolved:** the rerun log lists the 12 with
   `is_circulant`, and none is non-circulant.
5. **Naming.** **Remains:** `flat_board` / group `flat` builds 1–2 always-present and 1–2
   never-present columns. It is not the "flat columns" of rev 1.1's F. This is recorded in the
   README (remark 5).
6. **Line endings (rev 1.2's sixth remark).** **Resolved** by `.gitattributes` (`* -text`).
   `auc_search.py` and `run_survey.py` have CRLF line ends and the rest LF, all stored as written.
7. **New (rev 1.3).** `auc_search_out.txt` line 11 is a numpy overflow warning (from `exp` in the
   logistic-loss gradient; harmless to the counts) that prints the local scratchpad path. It is
   recorded in the README (remark 6).

**A post-data observation, deciding nothing (narrowed in rev 1.2).**
- By §3 and §2a, the free class holds block B's real labels at ≥ 0.9649. BF_1's float fit (`RESULT.md`
  line 32) is a member of that class on this shape. So **a rank limit of the class is excluded for
  block B**.
- Rev 1.1 went further and said the failed fit is "of the FF-sel kind or the optimiser". That was too
  narrow: FF-struct and **FF-quant** are also open.
  - Rule #2.1's registered decoder is quantised (§3, step 4) and BF_1's is not.
  - So BF_1's 0.9649 does not show that the rule's registered path at λ = 1 would pass.
- RN §9 (the choice collapsed to λ = 100) points to FF-sel, but no fit of rule #2.1 at λ = 1 on the
  real block was made, and none is made under this file.
- This does not change block B's label or B's D9 text. It bears on RN §7's first bullet and on RN §9's
  E4 ("two model classes as much as two predictors"): the two ceilings also differ by quantisation.
