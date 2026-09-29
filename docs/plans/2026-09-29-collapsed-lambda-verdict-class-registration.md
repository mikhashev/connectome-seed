# Registration: verdicts read at a collapsed interaction (a declared structural class)

**Status: draft rev 1, text only, not reviewed.**

**Post-data.** Every number below was already on file before this draft was written. The class is
declared post hoc from the (iii-b) diagnostic and the replication's run. This file is not blind to
them. A future run can only confirm the class on fresh boards (§5).

Abbreviations (paths from the repository root):
- "CAL" is `docs/plans/2026-09-29-failed-fit-branch-calibration-registration.md`.
- "RNR" is `results/genome/c6/checks/natural_fit_failure_replication/READING_NOTES.md`.
- "REP" is `results/genome/c6/checks/natural_fit_failure_replication/REPLICATION.md`.
- "DIAGCSV" is `docs/prereg-scripts/2026-09-29-iiib-diagnostic/iiib_diag_boards.csv`, which has a
  header on line 1 and one board per line on lines 2–415. "DIAGREADME" is the README beside it.
- "A-RES" is `results/genome/c6/checks/knockout_regrow/RESULT.md`. "B-RES" is
  `results/genome/c6/checks/knockout_regrow_block_b/RESULT.md`. "B-RN" is
  `results/genome/c6/checks/knockout_regrow_block_b/READING_NOTES.md`.
- "DIAG" is `docs/plans/2026-09-28-block-b-fit-diagnostic.md`. "DIAGJSON" is
  `connectome-seed-data/knockout_regrow/blockB_fit_diagnostic_20260928T200841Z_3be78249595c/diagnostic.json`.
  It lives outside the repository. Its sha256 `4ece4795…fb8d34` equals the one in its `SHA256SUMS.txt`.

## 0. What this is, and what it is not

- **The origin.** Mike chose "1 then 2" on 2026-09-29 (RNR:65–74). Option 1: (iii-b) stays a
  diagnostic. Option 2, this file: declare the structural class in text.
- **No new computation.** No fit, no script, no run. The numbers were recounted read-only from files
  already committed or pinned (§8).
- **No threshold on a continuous measure.** The class is keyed to two things:
  - the chosen λ_c, which takes two values on every board on file;
  - a numerical floor on |u·v| that sits in an empty gap of about 15 orders of magnitude (§2.2).

  Neither is a calibrated cut on a score. (iii-b)'s interaction share, which needed such a cut
  (CAL:1199, 1219), stays a diagnostic.
- **No label changes.** The class adds a **reading line** printed beside a registered label. It
  never replaces the label (§3).

## 1. The facts, recounted

All counts are over the 414 boards of DIAGCSV: 300 fresh, 99 seen (permuted) and 15 calibration
worlds. The script's own run checked its recomputed AUCs against the carriers in 1842 of 1842
comparisons (DIAGREADME:42–43). The fresh rows also agree with the replication's `boards.csv`:
`lambda_c`, `ceiling_block` and `ceil_1` match on 300 of 300 (§8).

**Notation.**
- The registered gate object is `ceiling_block`. It is the quantised AUC at λ_c, column
  `full_quant_lc` of DIAGCSV.
- `ceil_1` is the same AUC at λ = 1, column `full_quant_l1`.
- **"|u·v|"** is DIAGCSV's `R3_float_lc_maxabs`: the largest absolute entry of the double-centred
  float block logit at λ_c.
  - Its definition is `iiib_diag.py:105`, with the centring at `iiib_diag.py:84`.
  - On block B's shape this equals max |(u_s − ū)(v_t − v̄)| (DIAGREADME:32–41).
  - It is the u·v term with its additive gauge removed. It is not the fitter's raw
    max |u_s v_t|, which the records do not store (DIAGREADME:49).

### 1.1 (iii-a), a property of the class

- **On 414 of 414 boards, 0 boards pass the gate at the chosen λ_c and fail it at λ = 1.**
  - The counting rule: `full_quant_lc` ≥ 0.90 and `full_quant_l1` < 0.90, over DIAGCSV:2–415.
  - At λ_c = 1 this is trivial, since the two columns are equal on all 167 such boards.
  - It has content on the 247 boards at λ_c = 100. There, the 18 that pass at λ_c = 100 all pass at
    λ = 1 too, with `ceil_1` ≥ 0.96. The smallest is fresh:145 at 0.960000 (REP:466).
- **λ = 1 passes 407 of 414 boards (98.3 %).**
  - The 7 that fail at λ = 1 are fresh:40, 146, 151, 179, 222 and 229, and perm:89.
  - All 7 are U at λ_c = 100 (§1.2).
- This is recorded as a property of the class, not a gate (RNR:58–61). (iii-a) as a gate stays
  withdrawn.

### 1.2 The λ law

**λ_c takes only the values 1 and 100 on all 414 boards.** No board chose λ = 3, 10 or 30.

| λ_c | boards (fresh / seen / worlds) | \|u·v\| range | R3 under TAU | registered verdict |
|---|---|---|---|---|
| 100 | **247** (186 / 56 / 5) | 2.26e-17 to **1.311e-15** (max: perm:76, DIAGCSV:378) | **0.500000 on all 247**, for both the float and the quantised fit (`R3_float_lc_tau`, `R3_quant_lc_tau`) | **229 U, 18 G** |
| 1 | **167** (114 / 43 / 10) | **1.079** (min: fresh:113, DIAGCSV:115) to 2.403 | (live, not 0.5) | **167 G**, 0 U. The smallest `ceiling_block` is 0.915 |

**Row λ_c = 100, in more detail.**
- **The 5 worlds are FC's.** They were forced to λ = 100 by construction (CAL:958), not chosen by
  the nested folds (DIAGCSV:401–405, `grid` = `100.0`). The other 242 chose λ = 100 through the
  registered nested choice.
- **The split of U and G:**
  - 229 U = 171 fresh + 53 seen + 5 worlds;
  - 18 G = 15 fresh + 3 seen (perm:15, perm:49 and perm:76, at DIAGCSV:317, 351 and 378).
- **The fresh counts match REP.**
  - 171 failures among 186 at λ_c = 100 (REP:18).
  - The 15 passes at λ = 100 (REP:455–473).
  - The seen counts are the 53 of 99 of RNR:31–32.
- **N1 on the 18 G.**
  - The 15 fresh G have N1 recorded. For them, **N1 ≥ 0.8925**. The minimum is fresh:161, with N1
    0.892500 and a gate value of 0.901250 (DIAGCSV:163; REP:467).
  - Two of them, fresh:76 and fresh:97, have N1 exactly 0.900000 and a gate value of 0.900000
    (REP:462, 464).
  - **N1 is missing for the 3 seen G, and for every seen board.** The seen boards carry no `block||N1`
    record (DIAGREADME:27–28). DIAGCSV's `n1` is empty on all 99 seen rows.
- **The additive part decides.**
  - On the 186 fresh boards at λ_c = 100, `ceiling_block` − N1 lies in **[−0.025, +0.0125]**.
  - On the 15 fresh G it lies in [−0.00875, +0.01125] (REP:459–473, column `gap`).
  - On the 5 FC worlds it is 0 under TAU: both are 0.600000 (DIAGCSV:401–405; the ulp split of
    CAL:354–369).
  - So at λ_c = 100 the gate reads N1's additive order to within about one or two pairs in a hundred.
- **N1 on the 176 U with N1 recorded.** One has N1 ≥ 0.90: fresh:266, with N1 0.900000 and a gate
  value of 0.898750 (DIAGCSV:268). It is one of the three `DECODER_SPLIT_AT_LC` boards (RNR:42–44).

**Row λ_c = 1.** All 167 boards carry |u·v| ≥ 1.079 and all 167 are G.

**The gap.** The largest collapsed value, 1.311e-15, and the smallest live value, 1.079, differ by a
factor of 8.2e14: log10 = 14.9, or 15 orders of magnitude. No board falls between them.

### 1.3 The verdict follows the λ choice

- On this record, λ_c alone predicts |u·v|: collapsed at 100, live at 1.
- At λ_c = 1 every board passes.
- At λ_c = 100 the verdict is whatever N1's additive order gives (§1.2). This is Johnny's reading,
  "at λ = 100 the additive part decides" (RNR:71, DPC Research chat 16:10:00 UTC).
- The mechanism is the one DIAG expected before its run and DIAGJSON confirmed on block B (`tails.rule.collapsed_tail` = 3, 10, 30, 100): λ ≥ 3 collapses the rank-1 term for rule #2.1, so the grid is in effect
  {1, off} (DIAG:168–171; CAL:1191).

### 1.4 The two real blocks

| block | block-only λ_c | `ceiling_block` | registered label | source |
|---|---|---|---|---|
| A (flyvis-65) | **1.0** | **1.0000** | G: not detected at the R level above γ_R | A-RES:17 (column "lambda ko/full/block" = 1.0 / 1.0 / 1.0); A-RES:5 |
| B (flyvis-65) | **100.0** | **0.7744** | U: failed fit | B-RES:31 (1.0 / 1.0 / 100.0); B-RES:11 |

**Block B's λ = 100 was chosen by a fragile margin** (B-RN §9, B-RN:174–182).
- m = +0.435 nat in all, of which 0.39 comes from the one-cell fold 8. Without that fold,
  m = +0.042.
- Only 4 of the 9 two-class folds prefer λ = 100.
- Leaving out fold 9 alone flips the choice to λ = 1 (m = −0.999).
- The registered reading is "(c) carried by few folds".

**Block B's u·v at the chosen λ is collapsed.**
- The diagnostic's refit of the registered block-only fit reproduced `ceiling_block`
  0.7744360902255639 (B-RN:172).
- Its final-fit max |u_s v_t| is **2.697e-19** (DIAGJSON:1078, `tables.rule.final_uv_max`;
  DIAGJSON:2427).
- B-RN:175 quotes 2.6e-19, which is the inner-fold value at λ = 100: 2.628e-19,
  `tails.rule.uv_max_folds`.
- This is the raw term, not the double-centred one. For a rank-1 term the double-centred entries are
  bounded by 4 · max |u_s v_t| ≈ 1.1e-18. That is below every floor proposed in §2.2.

**Block A's u·v is not recorded.** No file read for this draft gives |u·v| for block A's block-only
fit.

## 2. The declaration

### 2.1 The class

A **block verdict** is **read at a collapsed interaction** when both of these hold:
1. the block-only fit that set `ceiling_block` was taken at **λ_c = 100**, chosen or forced;
2. its **|u·v|**, recorded per board (§6), is **≤ `UV_FLOOR`** (§2.2).

Such a verdict carries this reading line, verbatim:

> **"read at a collapsed interaction: not evidence about the rule's interaction structure"**

Under the class, the sub-kind is read as follows:
- **G → "additive-only pass (the board 41 class)."**
  - The gate was passed by the additive terms alone, with u·v = 0.
  - This is (iii)'s claim, measured: CAL:1179–1184 for board 41; CAL:1202–1204 for AD, the
    constructed board.
  - The label stays G. The line says that the G is no evidence that the rule's interaction term
    holds the block.
- **U → "FF-sel" if `ceil_1` ≥ 0.90**, by CAL §6's separator (CAL:890, with CAL:502 for the
  definition).
  - CAL §6 also needs `cert` ≥ 0.90. `cert` is ≥ 0.9725 on all 300 fresh boards, ≥ 0.975 on the 99
    seen boards and 1.0 on the 5 FC worlds (§8).
  - On those boards the FF-sel reading therefore rests on `ceil_1` alone.
  - A U with `ceil_1` < 0.90 keeps its separator row: FF-quant, or FF-struct or FF-opt, not
    separated. The class line is printed beside it all the same.
  - The label stays U.

### 2.2 The floor, `UV_FLOOR`

What the data fix:
- Every collapsed value on file is ≤ 1.311e-15 (perm:76, DIAGCSV:378).
- Every live value is ≥ 1.079 (fresh:113, DIAGCSV:115).
- Any floor in the open interval (1.311e-15, 1.079) classifies all 414 boards identically.

**Proposal: `UV_FLOOR` = 1e-9.** The reasons:
- **It is not a new number.** It is DIAG's `UV_ZERO` = 1e-9, registered for exactly this purpose:
  the "collapsed tail" (DIAG:65–66; DIAGJSON:2451).
- **It keeps 6 orders of margin above the largest collapsed value and 9 below the smallest live
  one.**
- **Inner fits collapse less deeply than the final fits.**
  - On block B, rule #2.1's inner fits at λ = 3 reach 2.36e-13 (DIAGJSON, `tails.rule.uv_max_folds`
    at 3.0).
  - That is already above the 1.311e-15 seen on DIAGCSV.
  - A floor set at the largest observed collapsed value would misread such a fit as live.

The alternative, a floor at 1.311e-15 itself, is listed as Q2 (§7) and not recommended.

### 2.3 Why λ_c = 100 and not "any collapsed λ"

- On the record no board chose λ = 3, 10 or 30 (§1.2). So the class is declared only where it was
  observed.
- A future board at λ_c ∈ {3, 10, 30} with |u·v| ≤ `UV_FLOOR` is **outside** this declaration as
  written. The script prints its flag (§6), and Q3 (§7) asks whether to widen the class.

## 3. How this reads on past registered results (no label changes)

**No registered label, verdict line, outcome label or prediction changes.** The reading line is
printed beside a label, as CAL does for the FF-quant line (CAL:541–545) and as B-RN §1 does for
"not separated" (B-RN:21–22). Nothing below re-reads a block.

| result | at λ_c = 100? | \|u·v\| recorded? | registered label (unchanged) | reading line under this class |
|---|---|---|---|---|
| **Block B**, B-RES:11, 31 | yes, chosen (B-RES:31) | raw 2.697e-19 (DIAGJSON:1078); not in the per-board carrier form | **U: failed fit**; read "a failed fit or a rank limit, not separated" (B-RN:21–22) | **"read at a collapsed interaction: not evidence about the rule's interaction structure."** The FF-sel sub-kind is **not named**: `ceil_1` and `cert` were not measured on the real block in any file read here. The "not separated" line stands beside it |
| **Block A**, A-RES:5, 17 | **no**: λ_c = 1.0 (A-RES:17) | no | **G** | **outside the class.** The class says nothing about block A's G. Also: A's block has 32 present and 32 absent cells (A-RES:15), not the 5 × 8 shape of the λ law, so §1.2 does not transfer to it |
| **Male CNS arm**, `results/genome/c6/checks/knockout_regrow_male_cns/RESULT.md`:27, 58 | no: λ_c = 1.0 on lobes L and R | no | G, G | outside the class |
| **Calibration FC worlds** (CAL:958; DIAGCSV:401–405) | yes, forced | yes (DIAGCSV) | U, FF-sel | in the class: "read at a collapsed interaction"; FF-sel (`ceil_1` = 1.000000) |
| **Replication** (REP:13, 18, 455–473) | 186 of 300 fresh | yes (DIAGCSV) | 171 U, 15 G at λ_c = 100 | all 186 in the class. 15 G → additive-only pass; of the 171 U, 165 read FF-sel (REP:18), 1 FF-quant at λ = 1 (fresh:40), 5 FF-struct or FF-opt, not separated |
| **Calibration seen boards** (the 99 permuted) | 56 of 99 | yes (DIAGCSV) | 53 U, 3 G at λ_c = 100 | all 56 in the class. 3 G → additive-only pass; 52 of the 53 U read FF-sel; perm:89 (`ceil_1` 0.895000, DIAGCSV:391) keeps its row |
| **M8 board 41** (CAL:1179–1184) | yes, forced | not in any file read here | not a label: a survey measurement | the class's type case by name. Whether its \|u·v\| is on file is open (Q6) |

**In total, over the 247 boards of DIAGCSV at λ_c = 100:**
- 18 G read as additive-only passes;
- of the 229 U, 222 read FF-sel (`ceil_1` ≥ 0.90), and 7 keep their separator row.

**Which past results the reading line touches.** Block B's `RESULT.md` and `READING_NOTES.md`;
the calibration's `CALIBRATION.md` (FC); the replication's `REPLICATION.md`. The touch is a line
beside the label, to be added only in reading notes, and only if this registration is adopted. The
frozen outputs are not edited (RNR:3).

**Block A is not touched.**

## 4. What this does NOT claim

- **Nothing about why the fitter picks λ = 100 on block B.**
  - The open question is the fragile fold margin: 0.39 of the 0.435 nat comes from the one-cell
    fold, and fold 9 alone flips the choice (B-RN:174–182).
  - The class describes what a verdict read at λ = 100 can mean. It does not explain the choice.
- **Nothing about block B's rule, block, or rank.**
  - "Not evidence about the rule's interaction structure" is not "no interaction".
  - B-RN:180–182 already says the λ = 100 choice is "not 'no interaction'".
- **Nothing about block A.** A was read at λ = 1 (§3).
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

## 5. Post-hoc status, and what a future run can do

- **The class is declared after the data.** The λ law, the gap, and the "additive part decides"
  reading were all read off DIAGCSV and REP after the runs (DIAGREADME:3–6; RNR:62–63).
- **A future run can only confirm it, on fresh boards.** The confirmation is structural:
  - every board at λ_c = 100 has |u·v| ≤ `UV_FLOOR`, and every board at λ_c = 1 has |u·v| above it;
  - no board takes λ_c ∈ {3, 10, 30}, or, if one does, it is printed and counted.

  A board that breaks either statement is printed under the flag `COLLAPSE_LAW_BROKEN` and counted.
  That board's reading line is withheld and the class is returned to review. The board's label is
  unaffected.
- **No confirmation run is registered here.** The carrier of §6 lets the next registered knockout or
  calibration run confirm the class at no extra fit cost.

## 6. The carrier needed in future scripts (a script item; no script is changed by this draft)

For the **next knockout or calibration script**, per board or block and per predictor where a
block-only fit is made:

| # | item |
|---|---|
| S-L1 | print `lambda_c` of the block-only fit (read as CAL's `_lambda_of`, B script lines 1205–1210), and whether it was chosen or forced |
| S-L2 | print **`uv_max_raw`**: max \|u_s v_t\| of the float fit at λ_c, read from `fit_uvw`'s U, V before `ExistQ`, as DIAG does (`final_uv_max`) |
| S-L3 | print **`uv_max_dc`**: max \|double-centred float block logit\| at λ_c, the object of DIAGCSV (`iiib_diag.py:84`, 105), so that later boards compare with the 414 on file |
| S-L4 | print the flag **`COLLAPSED_AT_LC`** = (λ_c = 100) and (`uv_max_dc` ≤ `UV_FLOOR`), and the reading line of §2.1 beside the label when it is set. **The label text is unchanged** (as CAL S-C7, CAL:1239) |
| S-L5 | print `COLLAPSE_LAW_BROKEN` when a board's λ_c and its collapse disagree with §5, and count it in the outcome |
| S-L6 | record N1's `block` `p` on **every** board, including permuted ones, so the additive-only reading can be checked where it is currently missing (the seen boards, §1.2) |
| S-L7 | a label-injection test: the flag set or unset leaves the label string byte-identical |

`UV_FLOOR` is to be a named constant in the script, equal to DIAG's `UV_ZERO` if Q2 is answered as
recommended.

## 7. Open questions

**Q1 (Ark). Is the object right?** "|u·v|" in the carrier is the double-centred logit (DIAGCSV),
while DIAG's is the raw max |u_s v_t|.
- **Recommendation:** print both (S-L2, S-L3), and key the flag on the double-centred one. It is
  invariant to the additive gauge (DIAGREADME:40–41, 49) and is what the 414 boards carry.

**Q2 (Warren). Where is the floor?** The choices are 1e-9 (DIAG's `UV_ZERO`) or 1.311e-15 (the
largest collapsed value on file).
- **Recommendation:** 1e-9. It is an existing registered constant, it sits deep in the empty gap,
  and it tolerates inner-fit collapse at 2.4e-13 (§2.2).
- The floor at 1.311e-15 would be fitted to the maximum of the data, and the next board could break
  it by rounding alone.

**Q3 (Zcode). Should the class cover any collapsed λ_c, not only 100?**
- **Recommendation:** not now. Declare it where it was observed (λ_c = 100).
- Print the flag for λ_c ∈ {3, 10, 30} too, and widen the class by a later text-only revision if a
  board ever lands there.

**Q4 (Johnny). Should the G reading line say "additive-only pass" or "additive-dominated pass"?**
- On the 15 fresh G, `ceiling_block` − N1 ranges from −0.00875 to +0.01125, so the collapsed fit is
  not identical to N1: quantisation and the W column effect enter (DIAGREADME:86–87).
- **Recommendation:** "additive-only", since u·v = 0 to 1e-15. The gap to N1 is additive too
  (c, a, b, W's column effect). Print the gap beside it.

**Q5 (Ark, Johnny). How does block B's line read without `ceil_1`?**
- **Recommendation:** print the class line alone. Say "sub-kind not named: `ceil_1` and `cert` not
  measured on the real block". Do not infer FF-sel from the 222 of 229 on the permuted boards.
- Whether to measure block B's `ceil_1` and `cert` read-only is a separate item for Mike (Q7).

**Q6 (Zcode). Board 41: is its |u·v| on file?** It is named as the type case, but no file read here
records its |u·v|.
- **Recommendation:** check SURVEY `m8_profile_boards.csv` at review. If it is absent, name board 41
  as the motive only, as CAL:1184 already does.

**Q7 (Mike). Should the reading line be added to past results' reading notes once this is
adopted?** The results affected are block B, FC and the replication.
- **What each option affects:**
  - **(a) Add it** to B-RN, the calibration's reading notes and RNR, as a line beside each label.
    It touches three reading-notes files and no frozen output or label.
  - **(b) Future runs only.** The past results keep their current text, and the class is read only
    from this file.
- **Recommendation:** (a). It is a reading line, which the project already adds beside labels after
  the fact (B-RN §1, RNR §§1–6). A reader of block B's U should see that it was read at a collapsed
  interaction.

**Q8 (Mike). Should block B's `ceil_1` and `cert` be measured?** It would be a read-only
re-evaluation on the pinned bank, which is a separate registration, not this one.
- **What it affects:** it would let block B's line name a sub-kind: FF-sel if `ceil_1` ≥ 0.90.
- **Recommendation:** list it in the backlog. Do not run it under this file.

**Q9 (all reviewers). Is "text only" enough, or does the class need an injection test before
adoption?**
- **Recommendation:** text now. The test (S-L7) comes with the next script that prints the flag, as
  CAL's label tests did.

## 8. How the numbers were recounted

Everything was read-only, with Python and `PYTHONUTF8=1`, on:
- DIAGCSV;
- `results/genome/c6/checks/natural_fit_failure_replication/boards.csv`;
- `results/genome/c6/checks/failed_fit_calibration/permuted_reference.csv` and `worlds.csv`;
- DIAGJSON.

The recount:
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
