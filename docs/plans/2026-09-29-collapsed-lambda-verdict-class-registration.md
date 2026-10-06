# Registration: verdicts read at a collapsed interaction (a declared structural class)

**Status: rev 2, text only, reviewed in chat: follows (Ark 18:45:51, Zcode 18:52:53, DPC Research
chat 2026-10-06 UTC; Warren 18:46:55 and Johnny 18:55:49 in support). The review's citation and
wording fixes are applied in this text (§12 records the answers). Mike's decisions on Q7, Q8 and
Q10 are pending.**

**Revision note.**
- **Rev 2, 2026-10-06 UTC.** It replaces rev 1 (commit `1e9fc9a`, 2026-09-29), in place.
- **Why.** Rev 1 was written before the symmetric lambda pair (prediction commit `e7d973f`, run
  outputs `f8e11db`, owner's blind review `bc833d2`, 2026-09-30) and before block B's `ceil_1`
  check (2026-09-30). Both changed what is known about the two real blocks. Rev 1 also defined the
  class by two conditions at once (λ_c = 100 and a small |u·v|), and a review (DPC Research chat,
  2026-09-29 16:15 UTC, as recorded in `GLOSSARY.md:244`) asked for λ_c = 100 alone to define it.
- **What changed against rev 1.**
  1. **The definition.** The class is now defined by λ_c = 100 alone. |u·v| ≤ `UV_FLOOR` is its
     consequence, kept as a check on the declaration (§1), not as a second condition.
  2. **Three regimes.** A table with both real blocks and the natural boards is new (§3).
  3. **Block A is no longer "outside, not measured".** Block A was measured at λ = 100 by the pair:
     it falls to the all-ties floor 0.5 (§3, §5). Rev 1's remark that A's shape differs from the
     λ law's shape is dropped: the pair measured A directly.
  4. **Block B's sub-kind is now named.** `ceil_1` and `cert` were measured on the real block (FF-sel).
     Rev 1's "sub-kind not named" (old Q5) and old Q8 are superseded.
  5. **Block B's label at λ = 1.** With only the block-only ceiling replaced by its λ = 1 value, B's
     own reading rule gives G (§5). This is a reading, not a verdict (§8).
  6. **Population figure, stated with its denominator** (§4).
  7. **The verdict mixes λ across clauses** (§6). New.
  8. **A "Not shown" section** (§8). New.
  9. **Open questions** updated (§12).
- **Kept from rev 1.** The λ law and the gap on the 414 boards (§2), the reading-line texts, the
  floor proposal, the carrier for future scripts, the post-hoc status, the recount.
- **This revision edits no registered label.** It only adds reading lines (§0, §7).

**Post-data.** Every number below was already on file before this draft was written. The class is
declared post hoc from the (iii-b) diagnostic, the replication's run and the symmetric pair. The
pair itself was registered before its run and blind-reviewed; the class declaration is not. This
file is not blind to any of them. A future run can only confirm the class on fresh boards (§10).

Abbreviations (paths from the repository root):
- "CAL" is `docs/plans/2026-09-29-failed-fit-branch-calibration-registration.md`.
- "RNR" is `results/genome/c6/checks/natural_fit_failure_replication/READING_NOTES.md`.
- "REP" is `results/genome/c6/checks/natural_fit_failure_replication/REPLICATION.md`.
- "DIAGCSV" is `docs/prereg-scripts/2026-09-29-iiib-diagnostic/iiib_diag_boards.csv`, which has a
  header on line 1 and one board per line on lines 2–415. "DIAGREADME" is the README beside it.
- "A-RES" is `results/genome/c6/checks/knockout_regrow/RESULT.md`. "A-RN" is
  `results/genome/c6/checks/knockout_regrow/READING_NOTES.md`.
- "B-RES" is `results/genome/c6/checks/knockout_regrow_block_b/RESULT.md`. "B-RN" is
  `results/genome/c6/checks/knockout_regrow_block_b/READING_NOTES.md`.
- "PAIR" is `results/genome/c6/checks/symmetric_lambda_pair/RESULT.md`. "PAIR-BR" is
  `results/genome/c6/checks/symmetric_lambda_pair/BLIND_REVIEW_raw.md` (the owner's blind review,
  verbatim).
- "B1" is `results/genome/c6/checks/block_b_ceil1/RESULT.md`.
- "GLOSS" is `GLOSSARY.md`. Terms used below and defined there: gate (GLOSS:191), `ceiling_block`
  (GLOSS:45), `ceil_1` (GLOSS:47), N1 (GLOSS:49), λ_c (GLOSS:241), FF-sel and the other failed-fit
  sub-kinds (GLOSS:46), tie (GLOSS:154), verdict labels (GLOSS:156), "read at a collapsed
  interaction" (GLOSS:244).
- "DIAG" is `docs/plans/2026-09-28-block-b-fit-diagnostic.md`. "DIAGJSON" is
  `connectome-seed-data/knockout_regrow/blockB_fit_diagnostic_20260928T200841Z_3be78249595c/diagnostic.json`.
  It lives outside the repository. Its sha256 `4ece4795…fb8d34` equals the one in its `SHA256SUMS.txt`.

## 0. What this is, and what it is not

- **The origin.** Mike chose "1 then 2" on 2026-09-29 (RNR:65–74). Option 1: (iii-b) stays a
  diagnostic. Option 2, this file: declare the structural class in text.
- **It edits no label.** No registered label, verdict line, outcome label or prediction is changed.
  The class **only adds a reading line** beside a registered label (§7), as the project already does
  in reading notes (B-RN §1, B-RN §10–§11, A-RN §1).
- **No new computation.** No fit, no script, no run. Every number is taken from a file already
  committed or pinned (§13).
- **No threshold on a continuous measure.** The class is keyed to the chosen λ_c, which takes two
  values on every board on file. The |u·v| floor is a check on the declaration (§1.2), not a
  calibrated cut on a score. (iii-b)'s interaction share, which needed such a cut (CAL:1199, 1219),
  stays a diagnostic.

## 1. The declaration

### 1.1 The class

A **block verdict** is **read at a collapsed interaction** when one thing holds: the block-only fit
that set `ceiling_block` was taken at **λ_c = 100**, chosen by the nested folds or forced.

Plain words. Rule #2.1's fit has two parts: an additive part (a source effect and a target effect,
which cost nothing to keep) and an interaction part, the product u·v, shrunk by the knob λ. At
λ = 100 the interaction part is shrunk to zero. The verdict then reads only the additive part. That
is why the class is named by λ_c and not by the block.

Such a verdict carries this reading line, verbatim:

> **"read at a collapsed interaction: not evidence about the rule's interaction structure"**

Under the class, the sub-kind is read as follows:
- **G → "additive-only pass (the board 41 class)."**
  - The gate was passed by the additive terms alone.
  - This is (iii)'s claim, measured: CAL:1179–1184 for board 41; CAL:1202–1204 for AD, the
    constructed board.
  - The label stays G. The line says that the G is no evidence that the rule's interaction term
    holds the block.
  - "Additive-only" means the additive terms of the collapsed fit, not N1 alone. The collapsed fit
    can pass with N1 below the cut: fresh:161 has N1 0.892500 and a gate value of 0.901250
    (DIAGCSV:163), the gap carried by the additive residual (§2.1; Johnny, chat 18:55:49 UTC).
- **U → "FF-sel" if `ceil_1` ≥ 0.90**, by CAL §6's separator (CAL:890, with CAL:502 for the
  definition).
  - CAL §6 also needs `cert` ≥ 0.90. `cert` is ≥ 0.9725 on all 300 fresh boards, ≥ 0.975 on the 99
    seen boards and 1.0 on the 5 FC worlds (§13).
  - On those boards the FF-sel reading therefore rests on `ceil_1` alone.
  - A U with `ceil_1` < 0.90 keeps its separator row: FF-quant, or FF-struct or FF-opt, not
    separated. The class line is printed beside it all the same.
  - The label stays U.

### 1.2 The consequence, u·v = 0, and the floor that checks it

**Two scales.** "dc" below is the double-centred object of DIAGCSV (§2, notation); "raw" is the
fitter's max |u_s v_t| (DIAG, DIAGJSON). For a rank-1 term the dc entries are bounded by
4 · raw, so a dc value can sit up to 4 times above the raw one; the two are not compared against
one number without saying so.

On every board on file at λ_c = 100 the interaction part is numerically zero (§2.1): dc |u·v| runs
from 2.26e-17 to 1.311e-15. On every board at λ_c = 1 dc |u·v| is at least 1.079. So "u·v = 0"
follows from "λ_c = 100" on this record. It does not define the class.

The check, `UV_FLOOR`:
- Any floor in the open interval (1.311e-15, 1.079) separates all 414 boards identically.
- **Proposal: `UV_FLOOR` = 1e-9, in the dc scale.** It is not a new number: it is DIAG's `UV_ZERO`
  = 1e-9, registered for exactly this purpose, the "collapsed tail" (DIAG:66–67; DIAGJSON:2451). It
  sits 6 orders of magnitude above the largest collapsed dc value and 9 below the smallest live one.
- Inner fits collapse less deeply than the final fits. On block B, rule #2.1's inner fits at λ = 3
  reach a raw 2.36e-13 (DIAGJSON, `tails.rule.uv_max_folds` at 3.0); in the dc scale that is at most
  4 · 2.362e-13 ≈ 9.4e-13. Either way it is above the dc 1.311e-15 seen on DIAGCSV and below 1e-9. A
  floor set at the largest observed collapsed value would misread such a fit as live.
- **Use.** A board with λ_c = 100 and |u·v| above `UV_FLOOR`, or λ_c = 1 and |u·v| at or below it, is
  printed under `COLLAPSE_LAW_BROKEN` (§10, §11). It does not change the class; it sends the
  declaration back to review.

The alternative, a floor at 1.311e-15 itself, is listed as Q2 (§12) and not recommended.

### 1.3 Why λ_c = 100 and not "any collapsed λ"

- On the record no board's block-only fit chose λ_c = 3, 10 or 30 (§2.1). (Other fits did choose
  λ = 3: see §6.) So the class is declared only where it was observed.
- A future board at λ_c ∈ {3, 10, 30} with |u·v| ≤ `UV_FLOOR` is **outside** this declaration as
  written. The script prints its flag (§11), and Q3 (§12) asks whether to widen the class.

## 2. The facts on the 414 boards, recounted

All counts are over the 414 boards of DIAGCSV: 300 fresh, 99 seen (permuted) and 15 calibration
worlds. The script's own run checked its recomputed AUCs against the carriers in 1842 of 1842
comparisons (DIAGREADME:42–43). The fresh rows also agree with the replication's `boards.csv`:
`lambda_c`, `ceiling_block` and `ceil_1` match on 300 of 300 (§13).

**Notation.**
- The registered gate object is `ceiling_block`, the quantised AUC at λ_c (column `full_quant_lc`).
- `ceil_1` is the same AUC at λ = 1 (column `full_quant_l1`).
- **"|u·v|"** is DIAGCSV's `R3_float_lc_maxabs`: the largest absolute entry of the double-centred
  float block logit at λ_c.
  - Its definition is `iiib_diag.py:105`, with the centring at `iiib_diag.py:84`.
  - On block B's shape this equals max |(u_s − ū)(v_t − v̄)| (DIAGREADME:32–41).
  - It is the u·v term with its additive gauge removed. It is not the fitter's raw
    max |u_s v_t|, which the records do not store (DIAGREADME:49).

### 2.1 The λ law

**λ_c takes only the values 1 and 100 on all 414 boards.** No board chose λ = 3, 10 or 30. (This
count is rev 1's; the pair adds no board to it, because block A's λ = 100 is forced, not chosen.)

| λ_c | boards (fresh / seen / worlds) | \|u·v\| range | R3 under TAU | registered verdict |
|---|---|---|---|---|
| 100 | **247** (186 / 56 / 5) | 2.26e-17 to **1.311e-15** (max: perm:76, DIAGCSV:378) | **0.500000 on all 247**, for both the float and the quantised fit (`R3_float_lc_tau`, `R3_quant_lc_tau`) | **229 U, 18 G** |
| 1 | **167** (114 / 43 / 10) | **1.079** (min: fresh:113, DIAGCSV:115) to 2.403 | (live, not 0.5) | **167 G**, 0 U. The smallest `ceiling_block` is 0.915 |

(RNR:68–70 gives the same totals: 247 boards, |u·v| ≤ 1.31e-15, 229 U and 18 G; 167 boards,
|u·v| ≥ 1.079, all pass.)

**Row λ_c = 100, in more detail.**
- **The 5 worlds are FC's.** They were forced to λ = 100 by construction (CAL:958), not chosen by
  the nested folds (DIAGCSV:401–405, `grid` = `100.0`). The other 242 chose λ = 100 through the
  registered nested choice.
- **The split of U and G:**
  - 229 U = 171 fresh + 53 seen + 5 worlds;
  - 18 G = 15 fresh + 3 seen (perm:15, perm:49 and perm:76, at DIAGCSV:317, 351 and 378).
- **The fresh counts match REP.**
  - 171 failures among 186 at λ_c = 100 (REP:18).
  - The 15 passes at λ = 100 (REP:17; the rows at REP:455–473).
  - The seen counts are the 53 of 99 of RNR:31–32 and the 3 passes of 46 that chose λ = 100
    (RNR:10–11).
- **N1 on the 18 G.**
  - The 15 fresh G have N1 recorded. For them, **N1 ≥ 0.8925**. The minimum is fresh:161, with N1
    0.892500 and a gate value of 0.901250 (DIAGCSV:163; REP:467).
  - Two of them, fresh:76 and fresh:97, have N1 exactly 0.900000 and a gate value of 0.900000
    (REP:462, 464).
  - **N1 is missing for the 3 seen G, and for every seen board.** The seen boards carry no
    `block||N1` record (DIAGREADME:27–28). DIAGCSV's `n1` is empty on all 99 seen rows.
- **The additive part decides.**
  - On the 186 fresh boards at λ_c = 100, `ceiling_block` − N1 lies in **[−0.025, +0.0125]**.
  - On the 15 fresh G it lies in [−0.00875, +0.01125] (REP:459–473, column `gap`).
  - On the 5 FC worlds it is 0 under TAU: both are 0.60 under TAU (CAL:362, 366–367). DIAGCSV's
    `n1` on those five rows (DIAGCSV:401–405) is the exact value, 0.720000; the difference is the
    ulp split of CAL:354–369.
  - So at λ_c = 100 the gate reads N1's additive order to within about one or two pairs in a hundred.
- **N1 on the 176 U with N1 recorded.** One has N1 ≥ 0.90: fresh:266, with N1 0.900000 and a gate
  value of 0.898750 (DIAGCSV:268). It is one of the three `DECODER_SPLIT_AT_LC` boards (RNR:42–44).

**Row λ_c = 1.** All 167 boards carry |u·v| ≥ 1.079 and all 167 are G.

**The gap.** The largest collapsed value, 1.311e-15, and the smallest live value, 1.079, differ by a
factor of 8.2e14: log10 = 14.9, or 15 orders of magnitude. No board falls between them.

### 2.2 (iii-a), a property of the class

- **On 414 of 414 boards, 0 boards pass the gate at the chosen λ_c and fail it at λ = 1.**
  - The counting rule: `full_quant_lc` ≥ 0.90 and `full_quant_l1` < 0.90, over DIAGCSV:2–415.
  - At λ_c = 1 this is trivial, since the two columns are equal on all 167 such boards.
  - It has content on the 247 boards at λ_c = 100. There, the 18 that pass at λ_c = 100 all pass at
    λ = 1 too, with `ceil_1` ≥ 0.96. The smallest is fresh:145 at 0.960000 (REP:466).
- **λ = 1 passes 407 of 414 boards (98.3 %).**
  - The 7 that fail at λ = 1 are fresh:40, 146, 151, 179, 222 and 229, and perm:89.
  - All 7 are U at λ_c = 100.
- This is recorded as a property of the class, not a gate (RNR:58–61). (iii-a) as a gate stays
  withdrawn.

### 2.3 The verdict follows the λ choice

- On this record, λ_c alone predicts |u·v|: collapsed at 100, live at 1.
- At λ_c = 1 every board passes.
- At λ_c = 100 the verdict is whatever the additive part gives (§2.1). This is Johnny's reading,
  "at λ = 100 the additive part decides" (RNR:70–71, DPC Research chat 16:10:00 UTC).
- The mechanism is the one DIAG expected before its run and DIAGJSON confirmed on block B
  (`tails.rule.collapsed_tail` = 3, 10, 30, 100): λ ≥ 3 collapses the rank-1 term for rule #2.1, so
  the grid is in effect {1, off} (DIAG:168–171; CAL:1191).

## 3. Three regimes, all measured

The gate reads `ceiling_block` at λ_c. When λ_c = 100 the interaction part is off, so
`ceiling_block` is whatever the additive part reaches. Three regimes follow, depending on how much
order the additive part holds.

| regime | what the additive part holds | `ceiling_block` at λ_c = 100 | gate (cut 0.90) | the cases | carrier |
|---|---|---|---|---|---|
| **1. Additive part null** | nothing: every source and every target has 4 of 8 cells present, so the additive fit is flat | **0.5000**, the all-ties floor: 0 wins, 1024 ties, 1 level; \|u·v\| 3.289e-19 | fails: **U** when read by A's own rule | **block A**, with its block-only fit forced to λ = 100 | PAIR:21–24, 48, 55; PAIR-BR:29–30, 33; A-RN:15–18 |
| **2. Additive part moderate** | some order, below the cut | **0.7744**; raw \|u·v\| 2.697e-19 | fails: **U**, the registered label | **block B**, block-only fit chosen at λ = 100 | PAIR:56–57; B1:17; B-RES:31; DIAGJSON:1078 |
| **3. Additive part alone at or above the cut** | the whole pass | **≥ 0.90** (15 fresh G: N1 ≥ 0.8925, two at exactly 0.9000; gate − N1 within [−0.00875, +0.01125]) | passes: **G**, not about the interaction | the **board 41 class**: **18 natural instances** (15 fresh + 3 seen) | §2.1; REP:17, 459–473; RNR:51–53 |

Notes on the table.
- **Regime 1 is forced by arithmetic, not by a weak fit.** The reviewer's explanation (PAIR-BR:33):
  A's marginals are balanced, so the additive fit returns zero; with the interaction switched off at
  λ = 100 nothing is left, and 0.5 is the value of a fit that ties every pair. It is the all-ties
  floor, not a partially failing fit. A's own pattern is exactly a rank-1 board (ON × T4 union
  OFF × T5), so one explicit member certifies it (`cert_A` = 1/1 = 1.000000 over 1024 pairs,
  PAIR:20; the reviewer's own count 1024/1024, PAIR-BR:31, 33).
- **In regime 1 the 0.5 is not a measurement of any additive-part AUC.** No file read for this draft
  prints N1's own AUC on block A. The statement "the additive part is null" rests on the reviewer's
  derivation (PAIR-BR:33; A-RN:16–17) and on the fit's printed flat output (1 level), not on a
  separate N1 score.
- **Regime 3 is shown for the 15 fresh boards only.** For the 3 seen G the N1 value is not on
  record (§2.1), so "additive part alone" is a reading for them, not a measured one. Also, N1 on the
  fresh G reaches 0.8925 to 0.9000 at the lowest, so "at or above the cut" means "at or within about
  one pair in a hundred of it" (§2.1).
- **The three regimes have one cause.** The gate sees the additive part only, because the λ choice
  switched the interaction part off.
- **The two blocks differ by their additive part and by the λ choice, not shown to differ by the
  block.** On the gate clause the pair finds branch (b): "A would fail at lambda = 100 as B did: the
  A/B pair differs by the lambda choice, not shown to differ by the block" (PAIR:11).

## 4. The population figure

**Statement, with its denominators.** Over the 300 fresh certified permuted boards of the
replication:
- **171 of 300 (0.570) fail the gate** at their registered block-only fit (REP:13; RNR:7–8).
- **186 of 300 (62.0 %) chose λ_c = 100**, so they are in the class (REP:18; the 62.0 % is RNR:33).
- **All 171 failures are in the class** (171 of 171, REP:18, P5 (ii)).
- **Among the 186 in the class, 171 fail (92 %; arithmetic on REP:18) and 15 pass**, the 15 being
  regime 3 (REP:17).
- **FF-sel among the 186: 165** (REP:18).

So "57 %" is the failure rate over **all 300 fresh boards**, not over the boards the class holds.
The backlog entry `THE-COLLAPSED-LAMBDA-VERDICT-CLASS-IS-NOT-DECLARED-AROUND-LAMBDA-C-100` words it
"U on 57% of boards the class holds"; that wording moves the denominator. Over the boards the class
holds, the U share is 171 of 186. The 57 % is also a share of failures that are all in the class,
not the share of the class that fails. (§12 Q10 asks whether to correct the backlog wording.)

Over all 414 boards on file, 247 are in the class (59.7 %; arithmetic on §2.1).

**The seen set gives the same picture.** 56 of 99 seen boards are at λ_c = 100 (56.6 %, RNR:33);
53 of 99 fail (0.5354, RNR:31–32). Ark's reading is that the fresh set is indistinguishable from
the seen set in the share choosing λ = 100 (62.0 % against 56.6 %, z = 0.95; RNR:33–34).

**What the figure does not say.** It is a rate on one family of generated boards (the replication's
permuted boards), not a rate on nature. The replication's own wording is "collapse near 57 %"
(RNR:49–50), with a label that flips with the criterion chosen (RNR §2).

## 5. The two real blocks

### 5.1 Both blocks, at both λ (the gate clause)

| block | block-only λ | `ceiling_block` | gate ≥ 0.90 | label by the block's own rule | carrier |
|---|---|---|---|---|---|
| A (flyvis-65) | **1** (registered, chosen) | **1.0000** | passes | **G** (registered) | A-RES:5, 17; PAIR:19, 54 |
| A | **100** (forced by the pair) | **0.5000** | fails | **U**, "failed fit" (a reading, not a registered label) | PAIR:21, 48, 55 |
| B (flyvis-65) | **1** (`ceil_1`, measured on the real block) | **0.9624** | passes | **G** (by B's own `read_label`, only this input replaced) | B1:18–20 (value); PAIR:34–38, 56; PAIR-BR:35; B-RN:220–221 |
| B | **100** (registered, chosen) | **0.7744** | fails | **U**, "failed fit" (registered) | B-RES:11, 31; PAIR:57 |

**Plain reading.** At λ = 1 both blocks pass the gate. At λ = 100 both fail it. The gate reads the
λ, not the block (PAIR:11, PAIR:50–57; B-RN:221–223). At λ = 1 the two blocks still differ in
number, not in label: A reaches 1.0000, B reaches 0.9624 (PAIR:54, 56).

The registered labels (A: G; B: U) are **not edited**. The A/λ = 100 row and the B/λ = 1 row are
readings produced by the pair's registered route (PAIR:30–57).

### 5.2 Block B

- **Its λ = 100 was chosen by a fragile margin** (B-RN §9, B-RN:174–182).
  - m = +0.435 nat in all, of which 0.39 comes from the one-cell fold 8. Without that fold,
    m = +0.042.
  - Only 4 of the 9 two-class folds prefer λ = 100.
  - Leaving out fold 9 alone flips the choice to λ = 1 (m = −0.999).
  - The registered reading is "(c) carried by few folds".
- **Its u·v at the chosen λ is collapsed.** The diagnostic's refit reproduced `ceiling_block`
  0.7744360902255639 (B-RN:172). Its final-fit raw max |u_s v_t| is **2.697e-19** (DIAGJSON:1078,
  `tables.rule.final_uv_max`; DIAGJSON:2427). B-RN:175 quotes 2.6e-19, the inner-fold value at
  λ = 100: 2.628e-19, `tails.rule.uv_max_folds`. This is the raw term, not the double-centred one; for
  a rank-1 term the double-centred entries are bounded by 4 · max |u_s v_t| ≈ 1.1e-18, below every
  floor proposed in §1.2.
- **Its failed-fit sub-kind is now named: FF-sel on the real block.** `cert` = 132/133 = 0.992481,
  `ceil_1` = 0.962406 (float 0.959900), branch (c), no flag (B1:7–9, 17–21). The reading is that the U
  came from the λ choice and that the word "cannot" in B's label is wider than the measurement
  (B1:9; B-RN:205–209).

### 5.3 Block A

- **The registered fit was at λ = 1, so A's registered G is outside the class.** The class says
  nothing about A's G. A has 32 present and 32 absent cells, on 8 sources by 8 targets, with 4 of 8
  present on every source and every target (A-RES:15; PAIR-BR:33; PAIR:19 gives 1024 pairs).
- **A forced to λ = 100:** max |u·v| = 3.289e-19 (PAIR:24), `ceil_100_A` = 0.5000 with all 1024 pairs
  tied and 1 level (PAIR:21–22), `cert_A` = 1/1 = 1.000000 over 1024 pairs (PAIR:20; 1024/1024 in
  the reviewer's count, PAIR-BR:31).
- **The control** reproduced A's registered `ceiling_block` 1.0 at λ = 1 with all 64 p bit-equal
  to the store (PAIR:28).
- A's u·v at its *registered* fit (λ = 1) is not recorded in any file read here.

## 6. The verdict mixes λ across clauses

A block verdict is made from several fits. They do not all sit at the same λ. For block B, the
selected λ per predictor (knockout / full / block) is (PAIR:61–68):

| predictor | knockout | full | block-only |
|---|---|---|---|
| rule #2.1 | 1 | 1 | **100** |
| BF_1 | 1 | 1 | 1 |
| BF_2 | 1 | 3 | 1 |
| BF_3 | **3** | 3 | 1 |
| BF_4 | **3** | 3 | 1 |
| N1 | none | none | none |

And for the 99 leg-S shuffle fits (PAIR:70), the count by selected λ is:
- rule #2.1: 97 at λ = 100, 2 at λ = 3;
- BF_1: 97 at 100, 2 at 3;
- BF_2: 99 at 100;
- BF_3: 99 at 100;
- BF_4: 98 at 100, 1 at 3.

What this means, clause by clause:
- **The gate clause** reads rule #2.1's block-only fit, the only one of its three fits that chose
  λ = 100. This is the clause the class concerns.
- **The knockout legs** for the rule and for BF_1 and BF_2 are at λ = 1. For BF_3 and BF_4 they are at
  **λ = 3**, so the BF_3/BF_4 p_P values come from λ = 3 fits (PAIR-BR:37; B-RN:223–224).
- **Leg S** rests on shuffle fits that mostly chose λ = 100 (PAIR:70; PAIR-BR:37).
- **The G clause** reads the stored D1 readings and the p_P values. On B none of them is near its
  limit: every p_P > 0.10, the smallest being BF_4 at 0.2442 (PAIR:38), and a W reading needs
  p_P ≤ 0.0125 (PAIR-BR:37). The reviewer's wording is that neither the λ = 3 knockout fits nor the
  λ = 100 shuffle fits "decides here" (PAIR-BR:37). So the G at λ = 1 does not depend on them, but it
  does read them.

**What this limits.** "B's whole verdict at λ = 1" is not shown by the pair. It shows one clause
(the gate clause) at λ = 1 and takes the others as stored (§8).

## 7. How the line reads on past registered results (no label changes)

**No registered label, verdict line, outcome label or prediction changes.** The reading line is
printed beside a label, as CAL does for the FF-quant line (CAL:541–545) and as B-RN §1 does for
"not separated" (B-RN:21–22). Nothing below re-reads a block.

| result | at λ_c = 100? | \|u·v\| recorded? | registered label (unchanged) | reading line under this class |
|---|---|---|---|---|
| **Block B**, B-RES:11, 31 | yes, chosen (B-RES:31) | raw 2.697e-19 (DIAGJSON:1078); not in the per-board carrier form | **U: failed fit**; read "a failed fit or a rank limit, not separated" (B-RN:21–22) | **"read at a collapsed interaction: not evidence about the rule's interaction structure."** Sub-kind: **FF-sel** (`cert` 0.992481, `ceil_1` 0.9624; B1:17–19). B-RN §10–§11 already carry the `ceil_1` reading and the λ = 1 reading |
| **Block A**, A-RES:5, 17 | **no**: λ_c = 1.0 (A-RES:17) | no (registered fit); 3.289e-19 at the forced λ = 100 (PAIR:24) | **G** | **outside the class as registered.** The class says nothing about A's G. A-RN §1 already carries the forced-λ = 100 reading (U at 0.5000) beside it |
| **Male CNS arm**, `results/genome/c6/checks/knockout_regrow_male_cns/RESULT.md`:27, 58 | no: λ_c = 1.0 on lobes L and R | no | G, G | outside the class |
| **Calibration FC worlds** (CAL:958; DIAGCSV:401–405) | yes, forced | yes (DIAGCSV) | U, FF-sel | in the class: "read at a collapsed interaction"; FF-sel (`ceil_1` = 1.000000) |
| **Replication** (REP:13, 18, 455–473) | 186 of 300 fresh | yes (DIAGCSV) | 171 U, 15 G at λ_c = 100 | all 186 in the class. 15 G → additive-only pass; of the 171 U, 165 read FF-sel (REP:18), 1 FF-quant at λ = 1 (fresh:40), 5 FF-struct or FF-opt, not separated |
| **Calibration seen boards** (the 99 permuted) | 56 of 99 | yes (DIAGCSV) | 53 U, 3 G at λ_c = 100 | all 56 in the class. 3 G → additive-only pass; 52 of the 53 U read FF-sel; perm:89 (`ceil_1` 0.895000, DIAGCSV:391) keeps its row |
| **M8 board 41** (CAL:1179–1183) | yes, forced | no: not on file (Q6) | not a label: a survey measurement | the class's type case by name, as a motive (Q6) |

**In total, over the 247 boards of DIAGCSV at λ_c = 100:**
- 18 G read as additive-only passes;
- of the 229 U, 222 read FF-sel (`ceil_1` ≥ 0.90), and 7 keep their separator row.

**Where the lines go.** Block B's `READING_NOTES.md` (§10–§11 already carry the λ = 1 reading, and
would take one line naming the class), the calibration's `CALIBRATION.md` reading notes (FC), and
the replication's `READING_NOTES.md`. In block B's notes the class line goes beside §10 **together
with a one-line scope correction** to B-RN:207–208, which says p_P, the knockout AUC and n_ge were
computed at λ = 100; they come from the λ = 1 knockout and full fits of the rule (B-RES §3.5, PAIR:63),
as B-RN:223–224 already says (Ark and Zcode, chat 2026-10-06 UTC). `GLOSSARY.md:244` is restated
at adoption: one defining condition (λ_c = 100), and its pointer moved from §2 to §1. The touch is a line beside the label, only in reading notes,
and only if this declaration is adopted (Q7). The frozen outputs are not edited (RNR:3).

## 8. Not shown

This declaration does not show, and does not claim to show:
1. **How the fitter behaves on block A, and why its fold selection goes as it does.**
   - A's λ = 100 value was forced by the pair. The fold-selection mechanism on block A (what the
     nested folds would choose at λ = 100 versus 1, and by what margin) was not run. A's registered
     choice was λ = 1, and the reason for it is not shown here.
   - The pair gives the value 0.5 at a forced λ = 100. It does not give the fitter's inner behaviour
     on A's folds.
2. **Block B's full verdict at λ = 1.**
   - The pair read the **gate clause** at λ = 1 (B1 and PAIR:34–40). The other pieces of B's verdict
     are the stored ones: the knockout legs, the full fits, leg S's 99 shuffle fits, and the p_P
     values, at the λ values of §6.
   - Of these, the knockout legs for the rule, BF_1 and BF_2 were already at λ = 1. BF_3 and BF_4
     knockouts were at λ = 3. Leg S mostly sat at λ = 100.
   - A full verdict at a fixed λ = 1 (knockout, full and shuffle legs refit) would take more than 30
     minutes and needs Mike's yes first (backlog item
     `BLOCK-B-FULL-VERDICT-AT-FIXED-LAMBDA-1-IS-A-LONG-RUN-THAT-WAITS-ON-MIKES-YES`; Q8 below).
3. **That A and B differ or do not differ by the block.** The pair shows they differ by the λ choice
   on the gate clause; it does not show they do not differ by the block (PAIR:11).
4. **That the 18 natural instances are all additive alone.** N1 is recorded only on the 15 fresh
   ones (§3).
5. **The rate in nature.** The population figure is a rate on the replication's generated boards
   (§4).

## 9. What this does NOT claim

- **Nothing about why the fitter picks λ = 100 on block B.**
  - The open question is the fragile fold margin: 0.39 of the 0.435 nat comes from the one-cell
    fold, and fold 9 alone flips the choice (B-RN:174–182).
  - The class describes what a verdict read at λ = 100 can mean. It does not explain the choice.
- **Nothing about block B's rule, block, or rank.**
  - "Not evidence about the rule's interaction structure" is not "no interaction".
  - B-RN:180–182 already says the λ = 100 choice is "not 'no interaction'".
- **Nothing about whether block A's pattern is held by the rule.** A's pattern is a rank-1 board that
  one explicit member certifies (PAIR-BR:33); A's registered G at λ = 1 stands as registered.
- **No claim that λ_c = 1 fits are evidence of interaction.**
  - The class names what a collapsed verdict is not.
  - It does not certify the live ones. On every λ_c = 1 board, `ceil_1` ≥ 0.90 is also reached by
    fits whose additive part might carry most of the order. That is (iii-b)'s question, which stays
    a diagnostic.
- **No new gate, no new label string, no change to the U rule or the separator.**
  - (iii-a) as a gate stays withdrawn (RNR:58–61).
  - (iii-b) stays a diagnostic (RNR:67).
  - (iii-c) is not taken (CAL:1220–1221).
- **Nothing about biology.**

## 10. Post-hoc status, and what a future run can do

- **The class is declared after the data.** The λ law, the gap, and the "additive part decides"
  reading were all read off DIAGCSV and REP after the runs (DIAGREADME:3–6; RNR:62–63). The pair was
  registered before its run; its use here is post hoc.
- **A future run can only confirm it, on fresh boards.** The confirmation is structural:
  - every board at λ_c = 100 has |u·v| ≤ `UV_FLOOR`, and every board at λ_c = 1 has |u·v| above it;
  - no board takes λ_c ∈ {3, 10, 30}, or, if one does, it is printed and counted.

  A board that breaks either statement is printed under the flag `COLLAPSE_LAW_BROKEN` and counted.
  That board's reading line is withheld and the class is returned to review. The board's label is
  unaffected.
- **No confirmation run is registered here.** The carrier of §11 lets the next registered knockout or
  calibration run confirm the class at no extra fit cost.

## 11. The carrier needed in future scripts (a script item; no script is changed by this draft)

For the **next knockout or calibration script**, per board or block and per predictor where a
block-only fit is made:

| # | item |
|---|---|
| S-L1 | print `lambda_c` of the block-only fit (read as CAL's `_lambda_of`, B script lines 1205–1210), and whether it was chosen or forced |
| S-L2 | print **`uv_max_raw`**: max \|u_s v_t\| of the float fit at λ_c, read from `fit_uvw`'s U, V before `ExistQ`, as DIAG does (`final_uv_max`) |
| S-L3 | print **`uv_max_dc`**: max \|double-centred float block logit\| at λ_c, the object of DIAGCSV (`iiib_diag.py:84`, 105), so that later boards compare with the 414 on file |
| S-L4 | print the flag **`COLLAPSED_AT_LC`** = (λ_c = 100), and the reading line of §1.1 beside the label when it is set. **The label text is unchanged** (as CAL S-C7, CAL:1239) |
| S-L5 | print `COLLAPSE_LAW_BROKEN` when a board's λ_c and its `uv_max_dc` disagree with §1.2 (λ_c = 100 with `uv_max_dc` > `UV_FLOOR`, or λ_c = 1 with `uv_max_dc` ≤ `UV_FLOOR`), and count it in the outcome |
| S-L6 | record N1's `block` `p` on **every** board, including permuted ones, so the additive-only reading can be checked where it is currently missing (the seen boards, §2.1) |
| S-L7 | a label-injection test: the flag set or unset leaves the label string byte-identical, in each of the three regimes of §3 (0.5, 0.7744, ≥ 0.90) (Ark, chat 18:45:51 UTC) |
| S-L8 | print each clause's selected λ (knockout, full, block-only, and the shuffle fits' count per λ), as the pair's `lambda_provenance` does (PAIR:59–70), so the mixed-λ note of §6 is on every verdict |

`UV_FLOOR` is to be a named constant in the script, equal to DIAG's `UV_ZERO` if Q2 is answered as
recommended. The script comments that the floor is justified in the dc scale (S-L3), that a raw
value (S-L2) can sit up to 4 times below the dc one for a rank-1 term, and that only the dc value
is compared with the floor. In rev 1 the flag was keyed on both λ_c and |u·v|; here it is keyed on λ_c, and |u·v|
feeds only S-L5.

## 12. Open questions

**Q1 (Ark). Is the object right?** "|u·v|" in the carrier is the double-centred logit (DIAGCSV),
while DIAG's is the raw max |u_s v_t|.
- **Recommendation:** print both (S-L2, S-L3), and use the double-centred one in the S-L5 check. It
  is invariant to the additive gauge (DIAGREADME:40–41, 49) and is what the 414 boards carry.

**Q2 (Warren). Where is the floor?** The choices are 1e-9 (DIAG's `UV_ZERO`) or 1.311e-15 (the
largest collapsed value on file). The floor now only checks the declaration (§1.2).
- **Recommendation:** 1e-9. It is an existing registered constant, it sits deep in the empty gap,
  and it tolerates inner-fit collapse at 2.4e-13 (§1.2).
- The floor at 1.311e-15 would be fitted to the maximum of the data, and the next board could break
  it by rounding alone, and the check would then raise false alarms.

**Q3 (Zcode). Should the class cover any collapsed λ_c, not only 100?**
- **Recommendation:** not now. Declare it where it was observed (λ_c = 100).
- Print the flag for λ_c ∈ {3, 10, 30} too, and widen the class by a later text-only revision if a
  board ever lands there.

**Q4 (Johnny). Should the G reading line say "additive-only pass" or "additive-dominated pass"?**
- On the 15 fresh G, `ceiling_block` − N1 ranges from −0.00875 to +0.01125, so the collapsed fit is
  not identical to N1: quantisation and the W column effect enter (DIAGREADME:86–87).
- **Recommendation:** "additive-only", since the interaction part is zero to 1e-15. The gap to N1 is
  additive too (c, a, b, W's column effect). Print the gap beside it. For the 3 seen G, where N1 is
  not on record, say "additive-only by the class; N1 not recorded".

**Q6 (Zcode). Board 41: is its |u·v| on file?** (Numbering follows rev 1; Q5 and Q8 of rev 1 are
resolved or replaced, below.)
- **Answered at review: no.** SURVEY `m8_profile_boards.csv`, the carrier CAL:1183 names, has only
  cert, N1, q100, f100, q1 and f1 columns (Ark 18:45:51, Zcode 18:52:53 UTC; CC re-read the header).
  Board 41 stays the motive, as CAL:1179–1183 name it.
- **Margin, noted at review.** On board 41 the float fit at λ = 100 does not pass the gate:
  f100 = 0.899749 (359/399), quantised q100 = 0.904762 (361/399), N1 = 0.909774 (363/399)
  (`m8_profile_boards.csv`, board 41). The type case sits one cell from the cut. While the class is
  a reading line this does not matter; if it is ever read as a boundary, the margin is to be printed.

**Q7 (Mike). Should the reading line be added to past results' reading notes once this is
adopted?** The results affected are block B, FC and the replication.
- **What each option affects:**
  - **(a) Add it** to B-RN, the calibration's reading notes and RNR, as a line beside each label.
    It touches three reading-notes files and no frozen output or label.
  - **(b) Future runs only.** The past results keep their current text, and the class is read only
    from this file.
- **Recommendation:** (a). It is a reading line, which the project already adds beside labels after
  the fact (B-RN §1, §10–§11; RNR §§1–6; A-RN §1). A reader of block B's U should see that it was read
  at a collapsed interaction.

**Q8 (Mike). Should B's full verdict at a fixed λ = 1 be run (knockout, full and shuffle legs)?**
It takes more than 30 minutes and needs Mike's yes first. It replaces rev 1's Q8 (measure B's
`ceil_1` and `cert`), which is done.
- **What each option affects:**
  - **(a) Run it.** Then the declaration can say what B's whole verdict is at λ = 1, and §6 and §8
    item 2 close. It costs a long run.
  - **(b) Do not run it.** The declaration stands with §8 item 2 stated as not shown; B's label at
    λ = 1 stays a gate-clause reading.
- **Recommendation:** (b) for now. The declaration does not need it: it says what a λ = 100 verdict
  is, not what B's verdict at λ = 1 would be. Ask again only if a reviewer needs the whole verdict.

**Q9 (all reviewers). Is "text only" enough, or does the class need an injection test before
adoption?**
- **Recommendation:** text now. The test (S-L7) comes with the next script that prints the flag, as
  CAL's label tests did.

**Q10 (CC, Mike). Should the backlog entry's "U on 57% of boards the class holds" be corrected?**
The carriers give 171 of 300 fresh boards fail (57 %), 186 of 300 in the class, and 171 of 186 of
those fail (§4). The correction goes through the backlog tool only.
- **What each option affects:** (a) correct the wording, so the denominator is right; (b) leave it,
  and the entry keeps a figure that reads as a share of the class.
- **Recommendation:** (a).

**Answers at review (DPC Research chat, 2026-10-06 UTC).**
- **Q1:** print both; the dc value goes into the S-L5 check; the script comments the scale (§11)
  (Ark).
- **Q2:** 1e-9 (Ark, Zcode).
- **Q3:** do not widen now (Zcode).
- **Q6:** answered above.
- **Q9:** text now; S-L7 extended to the three regimes of §3 (Ark, Zcode).
- **Q7, Q8, Q10:** reviewers vote (a), (b), (a) (Ark, Warren, Zcode, Johnny). **Mike decides.**

**Superseded rev 1 questions.** Rev 1's Q5 (how B's line reads without `ceil_1`) and Q8 (measure
B's `ceil_1` and `cert`) are closed by B1 (§5.2). Rev 1's Q1–Q4, Q6, Q7 and Q9 are kept above under
their old numbers.

## 13. How the numbers were recounted

Rev 1's recount was done read-only, with Python and `PYTHONUTF8=1`, on:
- DIAGCSV;
- `results/genome/c6/checks/natural_fit_failure_replication/boards.csv`;
- `results/genome/c6/checks/failed_fit_calibration/permuted_reference.csv` and `worlds.csv`;
- DIAGJSON.

The recount (carried over from rev 1; the totals agree with RNR:68–70 and REP:13–18):
- **Groups** (`group`): 300 / 99 / 15.
- **λ_c** (`lambda_c`): only 1 and 100. There are 247 boards at λ_c = 100 (186 / 56 / 5) and 167 at
  λ_c = 1 (114 / 43 / 10).
- **|u·v|** (`R3_float_lc_maxabs`):
  - at λ_c = 100 it runs from 2.255e-17 to 1.311e-15;
  - at λ_c = 1 it runs from 1.079 to 2.403.
- **R3 under TAU** (`R3_float_lc_tau` and `R3_quant_lc_tau`): 0.500000 on all 247 collapsed boards.
- **Verdicts** (gate = `full_quant_lc` ≥ 0.90):
  - at λ_c = 100: 229 U and 18 G;
  - at λ_c = 1: 167 G, with a minimum of 0.915.
- **(iii-a):** 0 boards have `full_quant_lc` ≥ 0.90 and `full_quant_l1` < 0.90. `full_quant_l1`
  ≥ 0.90 on 407 of 414.
- **N1 on the 15 fresh G:** minimum 0.8925 (fresh:161). `n1` is empty on all 99 seen rows.
- **U at λ_c = 100 with `ceil_1` ≥ 0.90:** 222 of 229.
- **Cross-check** against the replication's `boards.csv`: `lambda_c`, `ceiling_block` and `ceil_1`
  agree with DIAGCSV on 300 of 300 fresh boards, to 5e-7.
- **The replication's `separator_reading` at λ_c = 100:**
  - 164 "fit failure, FF-sel";
  - 1 "FF-sel; and FF-quant at λ_c";
  - 1 "FF-quant (at λ = 1)";
  - 5 "FF-struct or FF-opt, not separated";
  - 15 "gate passed".
- **`cert`:**
  - at least 0.9725 on the 300 fresh boards (`boards.csv`, `cert`);
  - at least 0.975 on the 99 seen boards (`permuted_reference.csv`);
  - 1.0 on the 15 worlds (`worlds.csv`).
- **Block B** (DIAGJSON):
  - `tables.rule.final_uv_max` = 2.697359681714383e-19;
  - `tails.rule.uv_max_folds`: 1.827 at λ = 1, 2.36e-13 at λ = 3, 2.63e-19 at λ = 100;
  - `uv_zero` = 1e-09.

Added in rev 2 (read from the carriers, not recomputed): block A and B values of §3, §5 and §6 from
PAIR, PAIR-BR and B1; the population figures of §4 from REP:13–18 and RNR:7–8, 31–35. The only
arithmetic is 171/186 = 0.919, 15/186 = 0.081 and 247/414 = 0.597, which is marked as such where used.
The DIAGCSV-derived counts of §2 and §7 (seen-set, 7 U without FF-sel, 222 of 229) were not
re-read by the drafter of rev 2. At review Ark and Zcode each recounted them independently from
DIAGCSV, `boards.csv`, `permuted_reference.csv`, `worlds.csv` and DIAGJSON, and found no difference
(chat 18:45:51 and 18:52:53 UTC).
