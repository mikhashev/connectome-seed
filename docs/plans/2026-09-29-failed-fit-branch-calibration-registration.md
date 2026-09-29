---
**Status: draft rev 1.5, text only, not reviewed.** Revision 1.5 (2026-09-29 UTC, CC subagent)
applies **Johnny's second review** (DPC Research chat, 2026-09-29 05:41:19 UTC). He wrote it on rev
1.3, so each point was checked against rev 1.4:
- **§7:** a plain statement of what this run witnesses (FF-sel only), so that no reader over-claims
  (the V4 defect class). New.
- **§3:** the claim C6 and `cert` rest on is weakened from "equals" to **inclusion** of the free class
  in rule #2.1's class. The column-effect claim is marked as read from the code, and C6 does not
  depend on it. New.
- **§16:** the BF_1 citation (`RESULT.md` line 32: `ceiling_block` 0.9649, λ block 1.0; BF_r a
  float32 cast, not quantised) is recorded as checked by CC. New.
- **S-C11:** the seed assert takes this registration's own ranges as literals. New.
- **§15:** Q-J1's trade-off becomes Mike's **M6**, with Johnny's recommendation: uniform. New.
- **§8:** Johnny asked for the BF_4 claim to be marked "not verified". Rev 1.4 already added the
  carrier, so it now reads "verified by construction", with the capacity-not-fit caveat kept.
  Updated.

Nothing was run. No bank was read.

**Revision 1.4's status, as it stood:** "draft rev 1.4, text only, not reviewed." Revision 1.4 (2026-09-29 UTC, CC subagent)
applies the reviews of rev 1.3 (`1b6b6ad`). All four reviewers said "yes, with edits" in the DPC
Research chat on 2026-09-29. Nothing ran on any bank. Two design checks on constructed boards were
added to SURVEY: `bf4_check.py` and `fc_anchor.py`, with their outputs.

**Ark (05:29:40 UTC):**
- **Q-A3 confirmed** from the pinned `raw_fits.json.gz`: 2 boards (40 worlds z, 5 No worlds z′),
  `lam` 1.0 and `ceiling_block` 1.0 in all 225 rows (§2). One discrepancy is left open: N1's 0.72 on
  z (Q-A6).
- **Q-A1 in its hard form:** `cert` is the load-bearing instrument; the 0.9425 floor is refused
  outside 4-per-row boards (§1, §6). The planted members are the search's positive control (§5).
- **One line in §6:** `cert` bounds the class, not the fit.
- **Q-A2:** FN2 kept as the ladder's rung. The certificate depends only on k (§4). The `cert` cut is
  named "borrowed, not calibrated" (§9).
- **A5:** `ceil_1_float` is mandatory, and the pair (`ceil_λc_float`, `ceiling_block`) is added at the
  chosen λ (§3, §6, S-C4a).
- **A1:** FC's number is computed and registered before values: **0.600000** for the fit at λ = 100 on
  board z (§4, §5). The stop is split into two branches (§6, §12).
- **A2:** the exact reproduction `ceil_1` = 1.0 is registered (§4, §6).
- **A3:** `cert` ≥ the planted value is an assert (§5, §6, S-C6).
- **A4:** the seed collision is fixed. The permuted reference moves to 93200–93298, and `cert` gets
  93300–93307 (§4).
- **(iii-a) = `ceil_1`** (§13).

**Zcode (05:35:21 UTC):**
- Q-Z2 confirmed by code, with line citations (§6).
- The single-λ shortcut (S-C4b).
- No prediction drawn from RN §9's 1.83 (§6).
- Caveat 4 on `ceil_λc_float` (§3).
- The Q-Z1 recommendation (§13).
- The seed list completed (§4).

**Johnny (05:35:45 UTC):**
- Uniform swaps (Q-J1); no constructed control (Q-J2).
- The FF-quant reading line holding both views (§3).
- The FN rows in one form (§6, with one wording question, Q-J3).
- The BF_4 claim given a carrier with hashes: SURVEY `bf4_capacity.md`, `bf4_check.py` and
  `bf4_check_out.txt`. **0 failures on 824 boards**, including unequal row profiles (§8).

**Warren (05:23 and 05:36:49 UTC):**
- FC is 1 gate measurement × 5 external draws (§4, §6, §7).
- No (v-a)/(v-d) family in this run (§1, §8).

**§15:** every reviewer question is marked answered. Mike's M1–M5 stay open, with the reviewers'
positions under M1.

**Revision 1.3's status, as it stood:** "draft rev 1.3, text only, not reviewed." Revision 1.3 (2026-09-29 UTC, CC subagent)
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
- **Nothing that separates (v-a) from (v-d)** (rev 1.4; Warren, 05:36:49 UTC). No family here has a
  BF_r failing where rule #2.1 passes. Such a family would be an optional, separate, small
  registration later (§8).
- **No transfer of the 0.9425 floor to other row profiles** (rev 1.4; Ark, 05:29:40 UTC). The floor
  of §2a holds only for 4-per-row boards. **A future arm that cites it for a board with any other
  row profile is refused**; block B's real rows are 2, 6, 4, 4, 3. For a given block, the
  load-bearing instrument is `cert` (§6), computed on that block.

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
   - **Confirmed (rev 1.4; Ark's recount from the pinned pre-run `raw_fits.json.gz`, DPC Research
     chat 2026-09-29 05:29:40 UTC).** On the block mask, every predictor has exactly 2 distinct `p`
     and 2 distinct `y`.
     - The split is 40 / 5: the 40 worlds of M0.5, M0.6, M0.75, M0.85, M1.0, Nf, R and W are board z,
       and the 5 No worlds are board z′.
     - `lam` is 1.0 in all 225 rows.
     - The pinned `ceiling_block` is 1.0 for rule #2.1 and BF_1–BF_4 on both boards.
     - The outside density varies from 0.130 to 0.306 across worlds while the block `p` does not
       move.
     - Ark gives N1's block values as 0.72 (z) and 0.60 (z′). **One discrepancy, not resolved
       here:** `fc_anchor.py` (SURVEY) fits N1 on a constructed block-only view of each board and
       gets 0.600000 on both (240 of 400 pairs). Boards z and z′ are the same pattern up to a
       relabelling of rows and columns, and N1's ridge treats every type alike, so N1's AUC should
       be equal on the two. Q-A6 asks Ark which object his 0.72 is. Nothing in this file depends
       on N1's block value.
     - This meets Johnny's objection 1.
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
- **What C6 and `cert` rest on: inclusion, not equality** (rev 1.5; Johnny, 05:41:19 UTC).
  - The free class of §2a, `a_s + b_t + u_s v_t`, is **included** in rule #2.1's class on any block:
    set W = 0, and c is absorbed into a.
  - So `cap(rule #2.1) ≥ cap(free)`. A free-class member at ≥ 0.90 is a witness that rule #2.1's class
    holds the block. That is all that `cert`'s soundness (§6) and C6 (§7) need.
- **Equality on this shape is read from the code and is not relied on.** The column-effect item above
  was read from `types.csv` and `groups()`. Given it, the two classes coincide on block B's shape
  (W's column effect is absorbed into b). **C6 does not depend on it.** On a block where W is not a
  column effect, rule #2.1's class is larger, and `cert` remains a valid lower bound.
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
- **Mandatory printed fields** (rev 1.4; Ark, A5, 05:29:40 UTC). Two float/quantised pairs, so that
  FF-quant is seen at the λ that actually decided:
  - at λ = 1: `ceil_1_float` (the AUC of step 3's float output, before step 4) beside `ceil_1`;
  - at the chosen λ_c: `ceil_λc_float` (the same float AUC at the λ that `_lambda_of` reads from
    `LAST_FIT`, B script lines 1205–1210) beside `ceiling_block`, the quantised value at λ_c.

  **Why both.** The normal failure is a chosen λ_c ≠ 1: on block B it was λ = 100. **Zcode's caveat 4
  (05:35:21 UTC):** `ceil_λc_float` inherits the nested choice by design, so the one-class-fold
  confirmation of §6 does not carry over to it.
- **Still a diagnostic:** `ceil_1_starts100` (step 3 at λ = 1 with 100 starts) can show FF-opt but
  cannot prove FF-struct. It is a lower bound only.
- **What `fc_anchor.py` found on the z board at λ = 100** (SURVEY): the float fit gives 0.555, the
  quantised path 0.600. At the collapsed λ, quantisation *raised* the AUC. So the float/quantised pair
  can move in either direction.
- **FF-quant, the reading line** (rev 1.4; Johnny 05:35:45 and Ark 05:29:40 UTC, both views
  recorded): *"FF-quant: fit side (the class holds the block); the registered quantised
  representation cannot express the float fit."*
  - Johnny calls it a limit of the quantised representation. Ark calls it a fit-side cause.
  - They agree that the label does not change and that the sub-kind is printed.

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
| **FC** (control) | FF-sel, forced | the z board of B §3.6 | 20 / 40 | nothing | the planted score, AUC 1 (exact) | 5 worlds, but **1 gate measurement × 5 external draws** (the outside and the legs vary; the block-only fit does not) |
| **FN1** | FF-sel expected, natural | z board, 1 present and 1 absent cell swapped | 20 / 40 | which cells (seeded) | planted score, 380/400 = 0.95 (exact) | 5 |
| **FN2** | as FN1 | z board, 2 + 2 cells swapped | 20 / 40 | which cells (seeded) | planted score, 360/400 = 0.90 (exact) | 5 |

**Withdrawn** (arithmetic in §5a):

| family | revision | reason |
|---|---|---|
| RL2 | 1.1 | a member at 368/400 = 0.92 |
| RLH | 1.1 | every board has a member at 340/400 = 0.85 |
| RLF | 1.2 | a member at 378/400 = 0.945, found by search (§2a) |

**FC's worlds are not 5 confirmations** (rev 1.4; Warren, 05:23 and 05:36:49 UTC). The block-only
fit depends on the board alone (§2, fact 3), so FC's 5 worlds are 1 gate measurement repeated under
5 external draws. **The gate's robustness is measured by FN1 and FN2**, whose boards vary per world.

**The swap rule of FN1/FN2** (rev 1.4; Q-J1 answered by Johnny, 05:35:45 UTC): **uniform swaps.**
- Swaps keep 20 / 40 present. The swapped cells are drawn uniformly from the present and the absent
  cells of the z board by the world's seed, with no steering toward any inner fold.
- **The certificate depends only on k, not on which cells were swapped** (Ark, 05:29:40 UTC): it is
  ((20 − k)² + (20 − k)k)/400 for any choice of cells (§5). So the swap rule affects the fit only,
  never the certificate.

**The ladder** (rev 1.4; Q-A2 answered by Ark): FC 1.0 → FN1 0.95 → FN2 0.90. FN2 is kept as the rung
at the cut: the inclusiveness case of "≥ 0.90".

**The number FC stands on** (rev 1.4; Ark, A1; computed before values; SURVEY `fc_anchor.py`,
`fc_anchor_out.txt`):
- **The object.** It is rule #2.1's registered block-only path (train + decode) on board z with the
  grid forced to [100]: the fit at λ = 100. It is **not** "additive-only": u·v is not exactly 0 there
  (max |u·v| on the block 1.4e-20), and the W term and the quantisation also act.
- **Value: 0.600000**, which is 240 of 400 pairs (162 wins, 156 ties). The float fit before
  quantisation gives 0.555 (222 of 400).
- **Ark's anchors, for comparison.** His a_s + b_t search found nothing above 0.71 on z. N1's block
  value is 0.600 on the constructed view (see §2 for the discrepancy with Ark's 0.72).
- **The margin.** 0.600 is 120 pairs below the gate (0.90 = 360 of 400). FC's stop (b) of §6 is
  therefore not expected to fire.

**Reproduction registered** (rev 1.4; Ark, A2):
- FC's `ceil_1` on board z must equal 1.0 exactly, which is also the pinned block `ceiling_block` of
  rule #2.1 on board z (Ark's recount, §2).
- `fc_anchor.py` reproduces both on the constructed view: grid [1] gives 1.000000; the registered grid
  gives λ 1 and 1.000000.

**Why FC is a control, not a world.**
- FC's block-only fit of rule #2.1 runs with the grid set to `[100]`, by the module-global swap of
  `train_fixed_lambda` (B script lines 1213–1236, which sets `fit.LAMBDAS`, fit.py:57).
- It is not read by exactly the same code as the real bank (A:932–934).
- So it witnesses the branch's mechanics, not the instrument on a world.

**Seeds (proposed; rev 1.4 fixes a collision found by Ark, A4, 05:29:40 UTC).** Rev 1.3's permuted
reference, 93010–93108, overlapped the worlds 93100–93104.

| use | seeds |
|---|---|
| worlds: family index `i` (FC, FN1, FN2 = 0, 1, 2), world `j` = 0..4 | `93100 + 10 i + j`: 93100–93104, 93110–93114, 93120–93124. **Indices 3 and 4 stay unused** (93130–93134, 93140–93144; rev 1 RL2/RLH, rev 1.1 RLF) |
| permuted-board reference (§10), 99 permutations | **93200–93298** (moved in rev 1.4) |
| `cert` search on each block pattern: stage 1, the 5 refinement reruns, the 2 deep reruns | **93300; 93301–93305; 93306–93307** (new in rev 1.4) |

- **The survey's seeds cannot be reused for `cert`.** The survey used 11, 100–104 and 200–201. Seed
  11 lies inside the harness shuffle seeds 0–98, which B's seed assertion reserves
  (`reserved_seeds`, B script lines 1031–1043).
- **Disjointness (checked 2026-09-29).**
  - The ranges are disjoint from one another.
  - They are disjoint from A's seeds (90000–90184; A §3.7), B's (91000–91184; B §3.7) and the male
    arm's (92000–92184; B script `MALE_SEEDS`, line 317).
  - They are disjoint from A's untouched list (60000, 61000, 70000–70999, 80000–80999, 4242, 99, 7,
    1000–1019, the dial seeds 10000–10404, 20260923; B §3.7; `reserved_seeds`), the shuffle seeds 0–98, and `PCG64(30000 + j)`.
  - `git grep -n -E '\b93[0-9]{3}\b' -- '*.py'` found no use. The new script asserts all of this, as
    B's `assert_seeds_unique` does (B script lines 1050–1063).
- **Seeds of the design computations, not of this registration** (SURVEY README):
  - survey boards `default_rng(2026)`;
  - search stage 1 seed 11, refinement 100–104, deep pass 200–201;
  - `auc_search.py` surrogate starts, seeds 0–2 (logistic 0–1; the discrete search `default_rng(0)`);
  - `bf4_check.py` `default_rng(20260929)`.

## 5. Certificates fixed before any fit

- **FF families:** the AUC of the planted score `z_s z_t` on the world's labels, exact arithmetic.
  - With k present and k absent cells swapped on a 20 / 20 board, AUC = ((20 − k)² + (20 − k)k)/400.
  - FC: 1. FN1 (k = 1): 0.95. FN2 (k = 2): 0.90.
  - The planted score is a member of the class, so `cap` ≥ this value, and a world that meets the
    branch has a fitter cause by construction.
  - The value depends only on k, not on which cells were swapped (§4).
  - **FN2 sits exactly at the cut and is kept** as the ladder's inclusiveness rung (Q-A2, answered).
- **The fit at λ = 100 on each board** (rev 1.4 renames rev 1.3's "additive-only AUC"; Ark, A1): the
  registered path with the grid forced to [100]. It is printed per world. **For FC's board z it is
  registered now: 0.600000** (§4; SURVEY `fc_anchor.py`).
- **The planted members are the search's positive control** (rev 1.4; Ark, 05:29:40 UTC).
  - On every FC and FN board, `cert` must reach at least the planted value (1.0, 0.95, 0.90).
  - **This is an assert, not a cross-check** (A3). If `cert` falls below the planted value, the
    search budget is too small, and the run stops before any fit.

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
   - **`cert` bounds the class's capacity, not the fit** (rev 1.4; Ark, 05:29:40 UTC). The registered
     fit's AUC is at most `cap`, so `cert` ≥ 0.90 proves "the class can", not "the fit got there".
   - **`cert` is the load-bearing instrument**, computed per block (Ark). §2a's floor is not a
     substitute for it outside 4-per-row boards (§1).
   - The rerun spread is printed beside it. In the survey, no 5 × 8 board was flagged unstable;
     spreads reached 7 of 1,024 on 8 × 8, 25 of 2,500 on 10 × 10 and 104 of 7,098 on 13 × 13.
   - **For FC and FN, `cert` ≥ the planted value of §5 is asserted** (A3). A failure stops the run.
2. **`ceil_1`**, the fitter-side measurement (§3).
3. **Mandatory:** `ceil_1_float`, and the pair (`ceil_λc_float`, `ceiling_block`) at the chosen λ_c
   (§3). **Diagnostic:** `ceil_1_starts100`.

**Q-Z2, confirmed by code** (rev 1.4; Zcode, 05:35:21 UTC). Neither `ceil_1` nor `cert` can be moved
by a one-class inner fold.
- **`ceil_1`.** With `LAMBDAS` = [1], `fit_existence` still runs its fold loop (fit.py:129–140), but
  the choice at fit.py:141–142 ranges over one λ and returns it whatever the fold likelihoods are.
  The final fit (fit.py:143–144) uses every cell of the view. The inner folds therefore touch
  `inner_ll` only.
- **`cert`.** `best_auc` (SURVEY `survey.py` lines 9–52) has no folds at all.
- **Zcode's shortcut** makes this structural (§14, S-C4b).

| registered `ceiling_block` | `cert` | `ceil_1` | `ceil_1_float` | `ceil_λc_float` | reads |
|---|---|---|---|---|---|
| ≥ 0.90 | any | any | any | any | gate passed |
| < 0.90 | ≥ 0.90 | ≥ 0.90 | any | ≥ 0.90 | **fit failure, FF-sel; and FF-quant at λ_c** (the float fit at λ_c passed, the quantised one did not) |
| < 0.90 | ≥ 0.90 | ≥ 0.90 | any | < 0.90 | **fit failure, FF-sel** |
| < 0.90 | ≥ 0.90 | < 0.90 | ≥ 0.90 | any | **fit failure, FF-quant** (at λ = 1) |
| < 0.90 | ≥ 0.90 | < 0.90 | < 0.90 | any | **fit failure, FF-struct or FF-opt, not separated** (`ceil_1_starts100` ≥ 0.90 names FF-opt) |
| < 0.90 | < 0.90 | any | any | any | **not separated: rank limit or fit** (no witness either way) |

Every FF-quant row is printed with Johnny's and Ark's reading line (§3).

**Direction of soundness.** A "fit failure" row is sound: a stored member passes the gate. The last
row is not a rank-limit reading.

**Predictions.**

| family | registered label | `ceiling_block` (rule #2.1) | `cert` | `ceil_1` | reads | stop if |
|---|---|---|---|---|---|---|
| FC | U, failed fit, in 5 of 5 (**1 gate measurement × 5 external draws**; Warren) | **0.600000** in all 5 (the fit at λ = 100 on board z, registered in §4) | ≥ 1 (asserted) | **exactly 1.0** (reproduction, A2: = the pinned block `ceiling_block` of rule #2.1 on board z) | FF-sel | any world that does not read failed fit. **`ceiling_block` ≠ 0.600000, in two branches** (A1): (a) `LAST_FIT["lambda"]` ≠ 100, **the forcing did not act**, a script defect; (b) the forcing acted and the value is ≥ 0.90, **FC is not a witness**. `ceil_1` ≠ 1.0 (the reproduction failed) |
| FN1 | **G if the nested choice does not collapse; U, failed fit if it collapses** (`ceiling_block` < 0.90), read FF-sel when `ceil_1` ≥ 0.90, else by the separator's row | < 0.90 if collapsed | ≥ 0.95 (asserted) | ≥ 0.90 expected | FF-sel where the branch is met, else the row the separator gives | none (a count, §7) |
| FN2 | the same form as FN1 (Johnny, 05:35:45 UTC) | as FN1 | ≥ 0.90 (asserted) | ≥ 0.90 expected, at the cut | as FN1 | none |

- **A prediction not made** (rev 1.4; Zcode, 05:35:21 UTC). RN §9's "max |u·v| 1.83 at λ = 1" on
  block B came from fold-complement refits (inner fits). It is **not** a prediction of any world's
  `ceil_1`, and is not used as one.
- **Johnny's wording, as relayed.** It read FN2 as "U, failed fit (FF-sel) if it collapses and
  ceil_1 < 0.90". By §3, FF-sel means `ceil_1` ≥ 0.90. The row above keeps his form (G if no
  collapse, U failed fit if collapse) and reads the sub-kind by the separator. To be confirmed with
  Johnny (§15).

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

**Witnessed by this run** (rev 1.5; Johnny, 05:41:19 UTC; stated so that no reader over-claims, the
V4 defect class):
- **FF-sel only.** FC forces it. FN shows it if the nested choice collapses.
- **FF-struct, FF-opt and FF-quant are not witnessed.** No world is built to produce them. When they
  occur, the separator names them as **residuals**, not as witnessed causes.

| family | decidable? |
|---|---|
| FC | yes (exact certificate, asserted; `ceil_1` measured). **One gate measurement**, not five (Warren) |
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
- **BF_4 can reach AUC 1 on every 5 × 8 pattern: verified by construction** (rev 1.5; Johnny,
  05:41:19 UTC, had asked for "not verified", written before the carrier existed).
  - **Carrier:** SURVEY `bf4_capacity.md`, with the argument written out, and `bf4_check.py` with its
    output `bf4_check_out.txt` (hashes in the README).
  - **The check:** 824 boards, 0 failures, exact counting.
  - **The check covers capacity, not the fit.**
  - **The class, as fitted.** BF_r is N1's fixed additive offset O plus `U Vᵀ` at rank r
    (`fit_bf`, `harness.py:710–733`; `bf_decode.py`).
  - **The construction.** Choose U (5 × 4) spanning w⊥, with w ∈ {±1}^5 and ±w outside the board's
    at most 8 column patterns. Every column pattern then has an exact rational preimage in w⊥, with
    margin δ > 0. Scaling by K > range(O)/(2δ) puts every present cell above every absent one, for
    any additive O.
  - **The offset contributes nothing needed and prevents nothing.**
  - **The check.** 824 boards × 2 offsets gave 0 failures, with exact `Fraction` counting. The boards
    are the 571 survey boards, 50 with block B's real row profile 2, 6, 4, 4, 3, 200 with random
    unequal rows, and 3 edge cases.
  - This is capacity, not the fit: BF_4's penalised fit at the nested λ can still collapse.
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
  - (v-a) from (v-d): that needs a BF_r to fail where rule #2.1 passes. **This run has no such
    family** (Warren, 05:36:49 UTC). It would be an optional, separate, small registration later
    (§1).
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
| `cert` cut | 0.90 | **borrowed, not calibrated** (rev 1.4 names it so; Ark, 05:29:40 UTC): borrowed from `GATE_CUT`, as `MECHANISM_CUT` was (A:483–484) |
| `cert` budget (K, steps, reruns) | proposed as the rerun's staging (100 starts × 500 steps; the 5 × 500-start reruns; 2 deep seeds at 1,200 steps); exact counting, the `Fraction` recheck and the recheck by the registered `auc` | **to be fixed before values**. The positive control is FC/FN's assert (§5) |
| starts for `ceil_1_starts100` | 100 | proposed |
| swaps in FN1 / FN2 | 1 + 1, 2 + 2, uniform | proposed; FN2 kept at the cut (Q-A2, answered) |
| worlds per family | 5 | proposed (FC: 1 gate measurement × 5 draws) |
| FC's registered value | 0.600000 (240 of 400) | computed before values (§4; SURVEY `fc_anchor_out.txt`) |
| `RL_MARGIN_CUT` | — | **withdrawn** with the rank-limit families (rev 1.2) |

## 10. The null and the references

- **Gate-passing reference (reused, not rerun).** Block B's pinned reference: the z and z′ boards
  with `ceiling_block` 1.0 (RN §3a), read-only. By Ark's recount it is 2 block-only problems (§2).
- **Permuted-board reference (new, printed, decides nothing).**
  - 99 uniform permutations of the z board's 40 labels (seeds 93200–93298, moved in rev 1.4), block-only fits only.
  - Printed per board: `ceiling_block`, `ceil_1`, `ceil_1_float`, `ceil_λc_float` and `cert` for rule #2.1, and
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
- **Block-only fits** (the gate, `ceil_1`, `ceil_1_float`, `ceil_λc_float`, `ceil_1_starts100`, the
  permuted boards): seconds each; minutes in all. `fc_anchor.py` ran its three grids on two boards in
  seconds.
- **Design checks before values** (rev 1.4): `bf4_check.py` (824 boards) and `fc_anchor.py`, both
  seconds on the CPU, outputs in SURVEY.
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

- **FC failing its own predictions** (rev 1.4, the two branches of A1). An FC world with
  `ceil_1` ≠ 1.0 fails the registered reproduction (A2): a stop (C5), and the registered path is
  examined before anything is read. An FC world with `ceiling_block` ≠ 0.600000 is a stop too. In
  branch (a), `LAST_FIT["lambda"]` ≠ 100: the forcing did not act (a script defect). In branch (b),
  the forcing acted and the value is ≥ 0.90: FC is not a witness.
- **A board below the survey's floor.** A 5 × 8 board with 4 per row and `cert` < 0.9425 at the
  registered budget would move §2a's floor. A board with a proved `cap` < 0.90 would withdraw C6's
  "no rank-limit witness known" for this shape.
- **The float32 caveat** (rev 1.2) is resolved by the rerun (rev 1.3): its counts are exact and its
  members stored. A new `verify_members.py` mismatch would void the affected values.
- **The "2 boards" claim**: confirmed by Ark's recount (§2). The N1 discrepancy (0.72 against
  `fc_anchor.py`'s 0.600) is open (Q-A6) and bears on no reading here.
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
| **(iii-a)** fixed λ | `ceiling_block` at λ = `LAMBDA_GATE`, no nested choice. **At λ = 1 it is exactly `ceil_1`** (Ark, 05:29:40 UTC), so run (i) collects its material at no extra cost | a value; a new label reason |
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

**Zcode's recommendation (Q-Z1, 05:35:21 UTC), recorded.** The recommendation is Zcode's. The one-line reasons are the drafting agent's summary, to be checked against Zcode's message.
- **(iii-a) at λ = 1.** It is exactly `ceil_1`, free of the one-class-fold problem by code (§6), and
  already measured by (i).
- **Not λ < 1.** Below the grid's floor the penalty weakens toward the unpenalised class, so the
  gate would drift toward `cap` and stop measuring the registered fitter.
- **(iii-b) as a diagnostic only.** The interaction share needs a cut that nothing calibrates.
- **Not (iii-c).** A label-stratified fold object is a new instrument, with its own registration and
  review burden, and it repairs a nested choice that (iii-a) removes.

A gate of (iii) would bring new label strings, reviewed with an injection test, and would apply to
later arms only. Under (iii-a) the FF-sel sub-kind disappears by construction; FF-struct, FF-quant
and FF-opt remain (§3).

## 14. Script changes needed (listed; none is made by this draft)

| # | change |
|---|---|
| S-C1 | a new script, a copy of the B script (A's and B's files byte-unchanged), with `FAMILIES` = FC, FN1, FN2 and the Nf outside |
| S-C2 | the FN board builder (seeded swaps); `make_world`'s assertion of 20 present kept |
| S-C3 | the forced-grid block-only fit for FC: `train_fixed_lambda`'s global swap on `MASKS["block"]` (today hard-wired to `MASKS["ko"]`, B script lines 1225, 1231); the stop of §6 in its two branches, (a) `LAST_FIT["lambda"]` ≠ 100 and (b) value ≥ 0.90; the reproduction asserts `ceiling_block` = 0.600000 and `ceil_1` = 1.0 on board z |
| S-C4 | `ceil_1` on the block mask for rule #2.1 and BF_1–BF_4 |
| S-C4a | **mandatory:** `ceil_1_float`, the AUC of `fit_existence`'s float output at λ = 1 (fit.py:119–147, before `ExistQ`), computed by calling it on the block view, as `fc_anchor.py` does; `ceil_λc_float` at the chosen λ_c read by `_lambda_of` (B script lines 1205–1210). **Diagnostic:** `ceil_1_starts100`, the same at λ = 1 with `starts` = 100 |
| S-C4b | **Zcode's shortcut** (05:35:21 UTC): when `len(LAMBDAS) == 1`, the new script skips the fold loop. It calls `H.fit_n1` and `fit_uvw` at the one λ directly (fit.py:124, 143–144) and then the registered quantisation and decode. fit.py stays unchanged, and a test asserts that the result equals the full path's, bit for bit, on board z and on an FN board. "No nested choice" is then structural |
| S-C5 | `smallest_passing_auc` per world |
| S-C6 | `cert`: the survey's `best_auc` at the registered budget, the best member counted exactly, rechecked with `Fraction` and by the registered `auc` (B script lines 791–801), its parameters stored, the rerun spread printed; **`cert` ≥ the planted value asserted on every FC and FN board** (A3); seeds 93300–93307. The search code is copied from SURVEY with its hash, not imported from the scratchpad |
| S-C7 | the separator's reading printed beside the label; **the label text unchanged** |
| S-C8 | the permuted-board reference (seeds 93200–93298) |
| S-C9 | (§8) the four gate options computed and printed per world; only the registered one sets the label |
| S-C10 | (§13, if taken) AD and the (iii) objects |
| S-C11 | seeds of §4 asserted disjoint. **The assert takes this registration's own ranges as literals** (rev 1.5; Johnny, 05:41:19 UTC), since they are in no `.py` file yet and a grep-based check would miss them: worlds 93100–93104, 93110–93114, 93120–93124; the permuted reference 93200–93298; the `cert` seeds 93300–93307. It checks them against one another and against `reserved_seeds` (B script lines 1031–1043: A's, the male arm's, the untouched list, the shuffles and the ALS starts) and B's own seeds. Callers are read from the Orbit graph and confirmed by grep at the script's review (B §3.9) |

## 15. Open questions

**Answered in the reviews of rev 1.3** (DPC Research chat, 2026-09-29 UTC). Each is kept with its
answer.
- **Q-A1 (Ark, 05:29:40).** Answered in its hard form: `cert` is the load-bearing instrument, per
  block. The 0.9425 floor holds for 4-per-row boards only, and citing it for another row profile is
  refused (§1, §6). The search budget's positive control is FC/FN's planted members, asserted (§5).
- **Q-A2 (Ark).** Keep FN2 as the ladder's rung at the cut, the inclusiveness case (§4, §5).
- **Q-A3 (Ark).** Confirmed from the pinned `raw_fits.json.gz`: 2 boards, 40/5, `lam` 1.0 in 225
  rows, `ceiling_block` 1.0 (§2).
- **Q-A5 (Ark, Johnny).** The label does not change. The sub-kind is printed with the reading line
  that holds both views (§3). `ceil_1_float` and the pair at λ_c are mandatory (§3, §6).
- **Q-J1 (Johnny, 05:35:45).** Uniform swaps (§4). The trade-off is Mike's (M6, rev 1.5).
- **Q-J2 (Johnny).** No constructed control for FF-struct or FF-opt; the separator is enough.
- **Q-W1 (Warren, 05:23, 05:36:49).** FC is 1 gate measurement × 5 external draws; FN1/FN2 measure
  the gate's robustness (§4, §6). There is no (v-a)/(v-d) family in this run; it is an optional,
  separate registration (§1, §8).
- **Q-Z1 (Zcode, 05:35:21).** (iii-a) at λ = 1; not λ < 1; (iii-b) as a diagnostic only; not (iii-c)
  (§13).
- **Q-Z2 (Zcode).** Confirmed by code for `ceil_1` and `cert` (§6), made structural by S-C4b. It does
  not extend to `ceil_λc_float` (Zcode's caveat 4, §3).

**Two small items raised by this revision** (not reopening the answers above):
- **Q-A6 (Ark).** Which object is "N1 gives 0.72 (z)"? `fc_anchor.py` gets 0.600 on both boards,
  and the boards are isomorphic (§2). Nothing depends on it.
- **Q-J3 (Johnny).** Confirm the FN rows' wording in §6. FF-sel is `ceil_1` ≥ 0.90, so "FF-sel …
  and ceil_1 < 0.90" was read as "failed fit if it collapses, sub-kind by the separator".

**For Mike (each with what it affects; recommendation last).**
- **Q-M1: which items.** (i) + (v) only, or with (iii). *Recommendation: (i) + (v) first.*
  - **Zcode and Ark** note that (iii-a)'s data comes free with (i): at λ = 1 it is `ceil_1`, which
    (i) prints anyway.
  - **Johnny** votes (i) + (v) without (iii).
  - Either way, run (i) collects the material. The choice is only whether a gate of (iii) is
    registered for later arms.
- **Q-M2: instrument.** *Recommendation: CPU* (§11).
- **Q-M3: block B's own table as a world.** *Recommendation: no* (post-data).
- **Q-M4: (v).** *Recommendation: choose after the values.*
- **Q-M5: the rank-limit side (§5b).** (a) 5 × 8 fit side only, with the certificate closing the rank
  side per block; (b) a synthetic rank-limit family on a larger shape; (c) both. *Recommendation:
  (a).* The certificate answers "fit or class?" for any given 5 × 8 block. (b) calibrates a different
  mask, folds and N1 view, with unproved membership, and does not calibrate block B's shape.
- **Q-M6: FN's swap rule** (rev 1.5; Johnny, 05:41:19 UTC: this choice is Mike's).
  - **Uniform swaps** (§4, as registered): FN may never reach the branch, which leaves the forced FC
    as the only witness (C2).
  - **Swaps aimed at the single-cell inner fold:** more likely to give a natural witness, but that
    witness would be confounded with block B, since it copies one post-data finding (RN §9).
  - The certificate is the same either way; it depends only on k (§4).
  - *Johnny's recommendation: uniform.*

## 16. Not verified at drafting; findings about the survey; one post-data observation

**Not verified by this drafting agent:**
- §2's "2 boards" rests on Ark's recount of the pinned `raw_fits.json.gz`. This agent did not read
  the pinned pre-run folder.
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
  line 32) is a member of that class on this shape.
  - **Checked by CC** (rev 1.5, on Johnny's point, 05:41:19 UTC): `RESULT.md` line 32 is the BF_1 row,
    with `ceiling_block` 0.9649 and λ block 1.0.
  - BF_r is not quantised: its decode is a float32 cast (`bf_decode.py`; `harness.py:273–278`).
  - The citation holds. So **a rank limit of the class is excluded for
  block B**.
- Rev 1.1 went further and said the failed fit is "of the FF-sel kind or the optimiser". That was too
  narrow: FF-struct and **FF-quant** are also open.
  - Rule #2.1's registered decoder is quantised (§3, step 4) and BF_1's is not.
  - So BF_1's 0.9649 does not show that the rule's registered path at λ = 1 would pass.
- RN §9 (the choice collapsed to λ = 100) points to FF-sel, but no fit of rule #2.1 at λ = 1 on the
  real block was made, and none is made under this file.
- This does not change block B's label or B's D9 text. It bears on RN §7's first bullet and on RN §9's
  E4 ("two model classes as much as two predictors"): the two ceilings also differ by quantisation.
