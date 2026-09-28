# How to read this folder (added after the run; the outputs are left as the run wrote them)

This file was written after the registered run, beside its frozen outputs. It is **not** in this
folder's `SHA256SUMS.txt`, and it changes nothing in `RESULT.md`, `summary.json`, the two CSVs or
the sums. It records the reading that the outputs do not carry, the post-data observations that
decide nothing, two findings about the artifact, and what stays open. Sources: the blind review
`docs/notes/2026-09-28-knockout-regrow-block-b-blind-review.md` (commit 804f87a, conclusion "the
verdict follows"), and the reviewers' notes in the DPC Research chat, 2026-09-28 (Zcode 19:08,
Johnny 19:18, Ark 19:20 UTC). "A" is `docs/plans/2026-09-24-knockout-regrow-registration.md`,
"B" is `docs/plans/2026-09-25-knockout-regrow-block-b-registration.md` (rev 1.7.3), "A:1328" is a
line of A, "the private folder" is
`connectome-seed-data/knockout_regrow/flyvis65_blockB_20260928T143258Z_7a10d88ec95e/`.

## 1. The reading (the carrier `RESULT.md` lacks; review D.5)

- **The label is U, in its failed-fit form**: "U: failed fit: rule #2.1 cannot hold the block even
  when trained on it alone" (`RESULT.md` line 11; `verdict.json` `label_text`; `stdout.log` line 1519).
- **Nothing about block B is concluded from it; the fit, not the block, returns to review.** This is
  A §5's sentence for any U whose reasons include `ceiling_block` below 0.90 (A:1382), applied to
  block B by B §5 (B:933). No output of the run prints it (review D.5).
- **On block B it is read "a failed fit or a rank limit, not separated"** (B §4, B:922–925; D9,
  B:1257), since the real block is not known to be rank 1. The run prints this beside the verdict,
  not on it (`RESULT.md` line 19; `stdout.log` line 1524).
- **The block is readable, and this was checked, not assumed** (Ark and Zcode, 19:34–19:36 UTC):
  `real.smallest_passing_auc` = 0.7142857142857143 = 285/399 on the grid k/(19·21), not `None`, so
  B's "not readable" U (S38, B:575–578), which would take precedence over every branch, did not
  fire (review A.2). The label below is read on a readable block.
- **It is not G, and it is not "no grammar". Below the gate "a regrowth failure could be a failure
  to fit, so it is not read as G" (A:1358–1360). The table under the verdict (AUC 0.51–0.57, `p_P`
  0.24–0.48; `RESULT.md` lines 31–35) is not a G in all but name (review D.5).
- **A citation of the verdict line alone drops this reading** (review D.2). The subject of commit
  ce48577 ("verdict U, failed fit: ceiling_block 0.7744 < 0.90") is such a citation.

## 2. Why U and not G

The G row (A:1327) has three conjuncts (review A.4):

| conjunct | read on | values | holds |
|---|---|---|---|
| not R, not W | both D1 readings | rule #2.1 -> -, BF_1 -> - (`RESULT.md` line 11) | yes |
| `p_P > 0.10` | rule #2.1 and BF_1–BF_4 | 0.4795, 0.4040, 0.2704, 0.2698, 0.2442 (lines 31–35) | yes |
| `ceiling_block >= 0.90` | rule #2.1 alone | 0.7744 = 309 of 399 pairs (`real.rows.rule.ceiling_block`) | **no** |

The registered text reads the gate on the primary alone (A:1327, A:458–459, A:1307–1308; review
A.5). The run's one reason is that conjunct: "rule #2.1's ceiling_block = 0.7744 is below 0.90"
(`stdout.log` line 1520).

**A remark about the rule, not the run (Ark).** Read on BF_1 (`ceiling_block` 0.9649, 385 of 399
pairs) the label would be G (review A.5). The registration excludes that reading, and how narrowly
the label is set was already in A §4's text before the run.

## 3. Post-data observations that decide nothing (review A.8)

None of these enters the label (A:1352–1353, A:1368–1373), and none separates "failed fit" from
"rank limit": a reading that used them to choose would be written after the data.

**3a. Made by the run (seen only after the data).**

| observation | value | address |
|---|---|---|
| λ of rule #2.1's block-only fit | 100 (the grid edge); the four BF block-only fits chose 1 | `real.rows.rule.lambda_block`; `RESULT.md` line 31 "1.0 / 1.0 / 100.0"; `raw_fits_real.json.gz` record `real\|\|block\|\|rule`, field `lam` |
| its **logit** on the 40 cells, as a 5 × 8 table minus row and column means: largest residual | ~5e-16 (additive) | same record, field `p` |
| the same residual for the others (logit) | BF_1 2.09, BF_2–BF_4 1.81, N1 ~3e-16 (additive by construction) | records `real\|\|block\|\|<key>` |
| the same residual in `p`-space for rule #2.1 (Zcode) | ~3e-2, from the sigmoid, not from an interaction | same record |
| distance from N1's prediction | at most 0.040 in `p` (rule #2.1 keeps its field term, review A.8 item 3) | records `…\|\|rule`, `…\|\|N1` |
| inner folds of the block-only fit | 4, 4, 2, 4, 5, 3, 2, 8, 1, 7 cells (sum 40); present by fold 1, 2, 1, 3, 2, 2, 1, 3, 1, 3 (sum 19); the one-cell fold holds a present cell and no absent one | `results/genome/c6/folds.csv`; review A.8 item 7 |
| synthetic worlds meeting this branch | none: `ceiling_block` 1.0 and `lambda_block` 1 in all 225 rows of rule #2.1 and BF_1–BF_4 (the run's and the reference's) | `synthetic_worlds.csv`; review A.8 item 6 |

So 0.7744 is the AUC of an additive score: the `u_s · v_t` term adds nothing to it, and it is not
N1's prediction either (N1's own `ceiling_block` is 0.7882, `RESULT.md` line 36). **Why λ = 100
was selected is not in the outputs:** the stored records hold no inner held-out likelihoods, and
only a refit would give them (review, "What could not be checked", item 3).

**3b. Computable before the run, but not registered as an input (Ark).** The ±1 table of block B's
40 labels (sources L1–L5 × targets Mi1, Tm3, Mi4, Mi9, Tm1, Tm2, Tm4, Tm9, from
`results/genome/bank/offsets.csv`) has five non-zero singular values, 4.6373, 3.3333, 2.0000,
1.4567, 1.1235 (review A.8 item 5: 4.64, 3.33, 2.00, 1.46, 1.12). It is not rank 1 in A §2.4's
sense (`y_st = x_s · w_t`, A:416–421). Present cells by source 2, 6, 4, 4, 3; by target 4, 3, 2,
3, 1, 2, 2, 2 (each margin sums to 19, one count two ways; Zcode) (19 of 40: `stdout.log` line 1496, "block present 19 of 40"; `RESULT.md` line 31,
"(19/21)"). The table's cells equal the labels stored with the block-only fits (`raw_fits_real.json.gz`,
records `real||block||<key>`, field `y`). This fact is
kept out of the reading **because it was not a registered input**, not because it came late; B
said before the data only that the block "is not known to be rank 1" (B:531–535).

## 4. Two findings about the artifact (Ark 19:20 UTC, checked)

- **(a) The address "(B section 2.4)".** `RESULT.md` lines 17 and 25 and `summary.json`
  `real.a_literals_line` (and `real.conditional_lines[0]`) cite "(B section 2.4)". B has no
  numbered subsection 2.4: its §2 (B:520–539) is a list of deltas on A §2, and its third item is
  headed "§2.4, the two ceilings" (B:529), which B itself cites as "§2.4" (B:202). The two texts
  cited are in that item ("not known for the real block B", B:531–535; the within-fly note,
  B:537–539). The string comes from the script (`knockout_regrow_block_b.py` lines 290, 294,
  1770–1771). A reader looking for a section 2.4 in B finds none; the unambiguous address is B §2,
  the item on the two ceilings (B:529–539), with §4 and D9 (B:922–925, B:1257). The frozen artifact
  is not edited. Because the script prints the string, correcting prose does not stop it from
  returning: a fix is an edit of the script, with its own revision and head (Ark, Zcode).
- **(b) The commit subject.** Commit ce48577's subject cites the label and its measurement without
  the reading of section 1 (review D.2).

## 5. The checksum caveat and its fix (review E.7; commit c42f184)

`per_shuffle.csv` and `synthetic_worlds.csv` were written with CRLF (Python's `csv`) and summed on
those bytes; git at ce48577 stored them as LF. Commit c42f184 adds this folder's `.gitattributes`
(`*.csv -text`), so git now stores them as written. The sums were not regenerated:
`SHA256SUMS.txt` describes the bytes the run wrote. This folder therefore holds two files that the
run did not write and the sums do not name: `.gitattributes` and this `READING_NOTES.md`.

| file | sha256 of the stored bytes at ce48577 | at c42f184 | CR bytes at c42f184 |
|---|---|---|---|
| `per_shuffle.csv` | 75601f42…0aa22e55 (LF) | 28ffdb42…c321206a2 | 100 |
| `synthetic_worlds.csv` | f9e22bd0…2abb30bf (LF) | 2187ce89…8740dcb | 271 |

(Checked with `git show <commit>:<path> | sha256sum` and a count of `\r`.) **Zcode's note:** the
reference pin `PRERUN_SHA256["synthetic_worlds.csv"]` = 2187ce89… is also a sum of CRLF bytes
(`RESULT.md` pre-run table line, "pinned … recomputed 2187ce89…"). The reference lives outside git,
so the pin stays valid; an LF rebuild would not match it, by design.

## 6. Two small remarks (review C.5, D.4)

- `summary.json` holds two run times: `manifest.runtime_s` = 8027.44 (set at the end of the
  synthetic step and not updated) and `runtime_s` = 8216.19 (the whole run; `RESULT.md` line 3,
  `stdout.log` last line "wall-clock 8216s").
- The D8 additive-channel note (`RESULT.md` line 21) is printed under its registered condition,
  any U (S30, B:1129). Its mechanism, a rule that passes leg P and fails leg S (B:926–928), did not
  occur here: rule #2.1 fails both legs (`n_ge` = 68 of 99, `p_P` = 0.4795), and the U's one reason
  is the gate. It is not a description of this U.

## 7. What this run does not show

- Whether the fit or the rule's rank caused `ceiling_block` = 0.7744 (B:922–925; section 3).
- Anything about a grammar in block B, for or against (A:1382; B §5).
- Anything about averaging (`RESULT.md` line 5), or about block A's G, which stands (B §5, D11).
- What a `ceiling_block` below the gate looks like in a world whose answer is known: no synthetic
  world met this branch (section 3a).

## 8. Open for Mike (listed, not chosen)

Two kinds of question, kept apart (Ark: a gate that measures the interaction and the block's rank
are different objects).

**About the gate and the fit:**

1. **Calibrate the failed-fit branch** with synthetic worlds of known cause (Ark), so that a
   `ceiling_block` below 0.90 has a reference.
2. **A gate that measures the interaction** rather than the additive part (Zcode): a fixed λ, a
   residual after N1, or larger folds.
3. **A diagnostic refit of rule #2.1's block-only fit** that prints the five inner λ values by fold
   (Ark): A §5 sends the fit to review, and one number decides whether λ = 100 was chosen by the
   one-cell fold. It is a fit, so it needs its own word.

**About the block and the rule:**

4. **The rank question** (Ark): no longer testable on block B, since its rank is now known
   (section 3b); it needs constructed worlds or another block.
5. **Primary versus family** (Ark): change the rule that reads the gate on rule #2.1 alone only in
   the registration that brings a witness for the branch, justified by the narrowness known before
   the run, not by "BF_1 would give G".

Record: `docs/notes/2026-09-28-knockout-regrow-block-b-blind-review.md`; commits ce48577, 804f87a,
c42f184.

## 9. The fit diagnostic (ii): why rule #2.1's block-only fit chose λ = 100 (run 2026-09-28 20:08 UTC)

Plan `docs/plans/2026-09-28-block-b-fit-diagnostic.md` (revision 1, commit 3be7824; reviewed by Johnny,
Ark and Zcode, 19:52–19:56 UTC; run on Mike's word, DPC Research chat 20:00 UTC). Script
`results/genome/c6/checks/knockout_regrow_block_b_fit_diagnostic.py` at 3be7824, run from the worktree
`cs-blockb-diag` beside the data folder, clean tree:
`PYTHONUTF8=1 tools/.venv/Scripts/python.exe results/genome/c6/checks/knockout_regrow_block_b_fit_diagnostic.py > ../connectome-seed-data/knockout_regrow/blockB_fit_diagnostic_20260928T200841Z.console.log 2>&1`
(exit 0, 5 s). Outputs: `connectome-seed-data/knockout_regrow/blockB_fit_diagnostic_20260928T200841Z_3be78249595c/`
(`diagnostic.json`, `console.txt`, `SHA256SUMS.txt`); console copy sha256 `d025867a…bf5df8`.

- **Reproduction passed** for both refits: rule #2.1 λ 100, `ceiling_block` 0.7744360902255639; BF_1 λ 1,
  0.9649122807017544 (and the 40 `p_exist` and the per-fold sums, as the plan requires).
- **Rule #2.1, per λ total held-out log-likelihood (nats):** λ 1 −32.3258; λ 3, 10, 30, 100 −31.8911
  (one fit: the collapsed tail, max |u·v| at the chosen λ 2.6e-19). m = total(100) − total(1) = **+0.435**.
  Without the one-cell fold 8 (1 present, 0 absent): m = **+0.042**. Two-class folds preferring the tail:
  **4 of 9** (0, 1, 5, 9); folds 2, 3, 4, 6, 7 prefer λ = 1. Leaving out **fold 9 alone flips the choice to
  λ = 1** (m −0.999).
- **Registered reading (plan §5): "(c) carried by few folds"** — λ = 100 is preferred by 0.435 nats in all,
  of which 0.39 come from the one-cell fold, and by fewer than half of the two-class folds; one fold's
  removal reverses it. Read about the registered λ grid (no λ < 1), not about the block: this is not "no
  interaction".
- **BF_1, same folds:** λ 1 preferred by m = −0.044 (−0.300 without fold 8); the same four two-class folds
  prefer the tail, and leaving out any one of folds 2, 3, 4, 6, 7 flips its choice to the tail. Its chosen λ
  = 1 is outside the collapsed tail (max |u·v| 1.8).
- **E4:** rule #2.1 chose a λ in its collapsed tail and BF_1 did not, so 0.7744 against 0.9649 compares a
  fit with no rank-1 term against a rank-1 fit — two model classes as much as two predictors.
- **What this changes:** nothing about the label (U, failed fit). For the next registrations: on block B's
  inner folds the grid does not separate λ = 1 from "no interaction" robustly for either predictor (margins
  well under one nat once the single-class fold is out, decided by one or two folds); a gate that measures
  the interaction (iii) needs λ < 1 or a fixed λ, and folds without single-class members.
