# First rule's failure: predictions registered before rule #2

**Status: FINAL, ready to commit (pending CC's check).**

**History.**
- **v1** (written by CC, 09:29 UTC), consolidating predictions from Johnny and Ark's first pass
  (group chat, 09:21:28 / 09:24:40 UTC), was reviewed by the blind reader
  (`docs/plans/2026-09-23-blind-reader-report.md`). Verdict (report §B.2): **no item passed all
  four criteria** — (i) falsifier distinct from and not compatible with the confirming outcome,
  (ii) the compared readings predict different outcomes, (iii) cited numbers match the files,
  (iv) a run exists that measures it.
- **v2** rewrote the prediction sets. Johnny and Ark rewrote theirs in the group chat (messages
  [9] and [10] of the first round, 09:59 / 10:04 UTC) against the blind reader's checklist B.5,
  following CC's task in message [7] (09:53 UTC). The blind reader's own Part A predictions
  (written blind, before reading the draft) were kept as a third set.
- **v3** is the authors' fixes after the blind reader's round-2 review (report Part C,
  C.0–C.5), plus CC's own fixes from the same review. Round 2 findings: report `docs/plans/
  2026-09-23-blind-reader-report.md` Part C; authors' fixes: group chat messages [9] (Johnny,
  10:53:27 UTC) and [10] (Ark, 10:59:39 UTC) of the second round, following Mike's word at [8]
  (10:39:04 UTC, "@Ark @Johnny правьте свои пункты, @CC_windows ты свои").

  **Changed in v3** (so round 3 can review only these):
  - P-J2: ablated variant now fully defined (intercept, λ re-selection); CC-draft note added on
    what the variant removes.
  - P-J3: rewritten — `Δ ≤ 0`, expected range `[BF_r − 0.005, BF_r]` (was self-contradictory).
  - P-J5: rewritten, two-sided, conditioned on the offset field.
  - P-A1: rewritten — bounds fixed to remove the touching-boundary defect, "13.67/order of
    magnitude" dropped, `m(0.0) < +0.040` case stated as "no prediction."
  - P-A2: **withdrawn** by Ark (moved to §7, superseded appendix), replaced by a registration note
    on LOTO structure.
  - P-A4: rewritten — one refuting rule, a number instead of "≈ +0.025", a branch for
    offset-field-equals-N1, LOTO witness dropped.
  - P-A5: **withdrawn** by Ark (moved to §7, superseded appendix).
  - **P-A6 (new):** the verdict-facing half Ark split out of the old P-A4 — in-sample offset
    margin and P2's offset check.
  - §3b: P4 row rewritten (any margin above BF_r is a P4 pass for everyone); rank/starts row
    corrected (drops the reference to superseded v1 P-A2); form-defect-vs-content-fit row demoted
    to a note (its premise was wrong — degree is preserved under the shuffle).
  - §4b: split the k-sensitivity item into starts (7a) and the rule's own dimension parameter
    (7b); marked the offset-Jaccard-next-to-counts item as already satisfied; marked which runs
    are descriptive-only; noted the `--controls` re-run requirement (A20); left the spread-log
    assert's failure-mode open for Mike.
  - §4c (new): mandatory registration fields for rule #2 (declared r, timing cap, which fields the
    addition touches), and which branch of P-J4/P-J5/P-A4 applies to which answer.
  - §4(c) and §6 tagged `[informed by proposal / rule side]`.
  - P-B4 narrowed to "at rule #2's declared r, if r ≥ 8"; P-B6 narrowed on "at most a small
    addition" — both per the blind reader's own C.5 ask.
  - Summary counts (§3, end) updated for the round-2 fixes.
- **v4** comes after the blind reader's round 3 (report Part D) and Mike's word (11:33 UTC, "ок
  давай сделаем" to CC's proposal). **Changed in v4:**
  - P-J2 withdrawn, and the ablation run dropped from §4b;
  - P-J5: the zone overlap removed, and the offset-touched branch set to "no prediction" (CC, per
    D.1; Johnny to confirm);
  - P-A4: undetermined zone [0, +0.005) named;
  - P-B6: the "small addition" condition dropped (D.1);
  - §4c: the by-construction verdict facts added (no offset touch → rule #2 cannot pass C6; no
    existence touch → P4 ties), with a prediction/definitional table covering P4, P-J4, P-A4, P-A6
    and P-J5 (D.2).
- **v5 (final)** comes after the blind reader's round 4 (Part E, 11:51 UTC). **Changed in v5:**
  - §4c: the P4 "existence not touched" cell now states the bit-identical condition (P4's pass
    test, `harness.py:1028`, is a plain strict `>` with no τ) — tie holds only if rule #2's
    per-fold existence predictions are bit-identical to BF_r's; otherwise Δ is noise-level (~1e-12)
    and P4 is decided by noise, not by construction. The verdict-facts bullet on existence carries
    the same condition;
  - §4c table: P-J1 and P-B6 added to the existence-not-touched column as definitional (P-J1's
    margin is then BF_r's margin at the declared r: +0.04933 at r = 8, +0.04851 at r = 12, +0.03972
    at r = 4; P-B6 is BF's 10/10 fold wins);
  - P-J5's quantity cell: "or the Jaccard offset is printed next to this margin" removed, so the
    offset-touched branch reads only "no prediction";
  - P-J5: "Johnny to confirm" replaced with his confirmation, group chat 2026-09-23 11:36:53 UTC,
    plus his own caveat (the item assumes the addition carries no new per-node counts terms; if
    rule #2's registration says it does, the item is expected to fall, margin > +0.015);
  - a finding recorded (not fixed here, for the spec's owner, Zcode): spec A7 applies τ to
    superiority tests including P3 and P4, but `harness.py` applies τ only in P1/P2 (`cmp`) and
    uses a plain `>` at lines 1019 (P3) and 1028 (P4);
  - tidy: stale P-J2/ablation references removed (§4b item 4, its descriptive paragraph, §3b's
    note); "13.67×" and "small addition" removed from §3b; the garbled Δ = 0 sentence in §3b's P4
    row fixed; "acceptance A12" → "spec A12"; §4b item 2 narrowed to per-fold logits for paired P4
    resolution only (P-B2 dropped from it); §3 heading renamed "Predictions (final)" and the stale
    "for v3" wording in the task-process note (just above §1) generalized to every round; known
    values added to P-B3 and P-B4.

Per the original task ([7], 09:13:33 UTC): predictions first, then this file, then its logic is
read before commit, then rule #2 is written. No run and no rule #2 code before this file's commit.
Per message [7] (09:53:30 UTC), the same blind session re-checks this file's logic by the same
four criteria before any commit — each round, only against the items listed in that round's
"Changed in vN" list above.

---

## 1. Blindness record

**v1 record (kept).** Ark (message [10] of the first pass) read `rule_runs/first_rule_k12/RESULT.md`,
`result.json` (+ `spread_log_validation.json`), `HARNESS-CONTROLS.md`, `checks/n1_alone/RESULT.md`,
`harness_controls.json` (grep, four places); did not open the `2026-09-23-first-rule-*` plans or
`results/genome/c6/rules/`. Johnny (message [9] of the first pass) read the same result files plus
— by his own account — one forbidden file, `docs/plans/2026-09-23-first-rule-proposal.md`, §4.2–4.4
only, and quoted it into the group chat. Per the task instruction, every v1 Johnny item resting on
that reading was marked `[informed by proposal §4]`; those items are superseded below (§7).

**v2 additions, from the rewritten messages ([9], [10]):**

- **Ark's declaration ([10]).** For the rewrite he opened: the blind reader's report in full
  (including B.2 and B.5); `first_rule_k12/result.json` in full, via Python; `results/genome/c6/harness.py`
  lines 918–990, 1024–1069 and 1324–1330 (the exam's `dial_banks`, `loto`, `labels` assembly, and
  `dial_ratio` machinery); `2026-09-23-c6-amendment-acceptance.md`, only the window around A5 (found
  by grepping for `dial`). He did **not** open `results/genome/c6/rules/**` (including the first
  rule's `fit.py`/`decode.py`), `2026-09-23-first-rule-proposal.md`, `-search-criterion.md`, or
  `rule_runs/first_rule/`. One flagged exception: a search for the string `loto` in the proposal
  returned one line (line 502), a sentence stating that the proposal's leave-one-type-out split is
  descriptive; he read no further into that file on that hit. Recorded because he recorded it, not
  reproduced further.
- **Johnny's declaration ([9]).** His five rewritten items name no proposal arm ("§4.3", "§2.6")
  by that name; P-J1/P-J2/P-J3/P-J5 are stated against exam-record fields only. He flags one
  dependency he cannot resolve blind: **P-J4** assumes the addition in rule #2 does not touch
  offset sets; he states he does not know this from the proposal's mechanism (he has not read it)
  and can only ask Zcode. He marks P-J4 conditional on that answer, not resolved by this file.

**v3 addition.** For the round-2 fixes, Johnny read only the blind report's round-2 section (Part
C) and the group chat; he opened no new files. Ark's round-2 message ([10] of round two, 10:59:39
UTC) records the same reading: Part C in full, plus his own prior reading from round one. Neither
author reopened `results/genome/c6/rules/**`, the proposal, the search-criterion file, or the
rule-side file.

---

## 2. Verified facts

All checked against the allowed files. "Match" means the chat number equals the file's number to
the precision given.

| # | claim | chat value | file value | source | match |
|---|---|---|---|---|---|
| 1 | P1 existence, rule vs N1 (held-out) | 0.3670 / 0.3625 | rule 0.3670, N1 0.3625 | `first_rule_k12/RESULT.md` §P1 | yes |
| 2 | P2 existence in-sample, rule vs N1 | 0.2547 / 0.3354 | rule 0.2547427833618863, N1 (=D_k^N1 in-sample) 0.3353545725096699 | `first_rule_k12/result.json` `P2.insample_rule.existence`, `insample_n1.existence` | yes |
| 3 | Ark's per-fold existence margins (N1 − rule), folds 0–4 | +0.0427, +0.0203, −0.0043, −0.0243, −0.0408 | computed from `per_fold_rule`/`per_fold_N1` `existence`: +0.04272, +0.02030, −0.00431, −0.02426, −0.04085 | `result.json` `per_fold_rule`, `per_fold_N1` | yes |
| 3b | same, all 10 folds (not quoted verbatim in chat, computed here for the record) | — | fold5 +0.0103, fold6 −0.0470, fold7 +0.0480, fold8 −0.0573, fold9 +0.0073; mean of all 10 = −0.00451 | ibid. | mean matches RESULT.md P3 existence real margin −0.0045 |
| 4 | Ark's BF rank profile (real bank) r=1..16 | +0.0282, +0.0403, +0.0397, +0.0493, +0.0485 | r=1: 0.028150051052145946; r=3: 0.04034078611097054; r=4: 0.039723750076924115; r=8: 0.04933110015583628; r=16: 0.04851361152058485 | `harness_controls.json` (per-rank `P4.bf` blocks) | yes |
| 5 | "BF_12 threshold +0.0485" (this rule's own P4) | +0.0485 | rank 12, margin 0.0485130054821417 | `first_rule_k12/result.json` `P4.bf` | value matches to 4 decimals, **but see discrepancy note below** |
| 6 | k profile of BF_8 | +0.04927 / +0.04928 / +0.04933 at k=1/3/10 | 0.04926823262395004 / 0.04927961387835702 / 0.04933110015583628 | `harness_controls.json` `BF_8_real_bank_by_starts` | yes |
| 7 | rule loses to N0 in 10 of 10 folds (counts) | 10/10 | `did_not_run.folds_where_N0_beats_rule.counts` = 10 | `result.json` | yes |
| 8 | sign: rule = N1 = 0.9768, margin 0 on all 99 shuffles | 0.9768, margin 0, 99/99 | P1 sign rule 0.9768, N1 0.9768; P3 sign real_margin 0.0, shuffled_max 0.0, shuffled_mean 0.0, n_shuffled_ge_real 99 | `first_rule_k12/RESULT.md`, `result.json` `P3.sign` | yes |
| 9 | offset P3: real +0.0245, shuffled mean +0.0425, 97/99 ≥ real, p=0.98 | +0.0245 / +0.0425 / 97 / 0.98 | 0.024464970450011437 / 0.042538092256202656 / 97 / 0.98 | `result.json` `P3.offset` | yes |
| 10 | H18∩U18 = 14/18, p=1.1e-7, 75–78% of L's energy | 14/18, 1.1e-7, 75%/78% | overlap 14 of 18, p 1.1×10⁻⁷, energy 75% and 78% | `HARNESS-CONTROLS.md` "hub check" table | yes |

**Discrepancy note on #5.** The task brief and Johnny's/Ark's chat text both write "BF_12" for the
+0.0485 number. Verification shows two distinct fits land at +0.0485: (a) `first_rule_k12`'s own
P4 opponent, BF at **rank 12** (the rule's declared rank), margin **0.0485130054821417**; (b) a
separate, rule-independent BF at **rank 16** in `harness_controls.json`'s rank profile, margin
**0.04851361152058485**. These agree to four decimal places but are not the same fit and not
exactly the same number (differ at the 6th decimal). `harness_controls.json`'s "ranks that
occurred" list is 1, 3, 4, 8, 16 — it does not include 12. So "BF_12" is correct for
`first_rule_k12`'s own threshold, but Ark's rank-profile row of "+0.0485" at "r=16" is a different
object that happens to coincide numerically. Neither agent's number is wrong; the two objects
should not be treated as one measurement.

**Ark's claim that Johnny compared offset with the existence shuffled mean (−0.0643).** Checked.
Johnny's message [9] of round one, §4, writes the offset real margin +0.0245 "напротив −0.0643 у
shuffled mean". The value −0.0643 does not appear anywhere in the offset row of P3; it is the
**existence** row's shuffled mean (`P3.existence.shuffled_mean` = −0.06430553924056014, RESULT.md
P3 table). Offset's own shuffled mean is +0.0425. **Ark is right: Johnny's offset reasoning in his
Q4 rests on a misread** — he set the offset real margin against the wrong field's shuffled mean.
This does not by itself overturn Johnny's stated conclusion ("not on existence"), but the specific
number he offered as offset's comparison point is not offset's number.

No other discrepancies found among the checked numbers (rows 1–10). Below: verification of every
new number introduced in messages [9] and [10] of round one, checked against
`results/genome/c6/rule_runs/first_rule_k12/result.json` (`exam.loto`, `exam.dial`, `exam.P2`,
`exam.P4`) and `results/genome/c6/harness.py`.

| # | claim (message) | chat value | file value | match |
|---|---|---|---|---|
| 11 | `exam.loto` existence, rule / N1 | 0.75260 / 0.38582 | rule_mean 0.7525954661976462, n1_mean 0.38582034180687946 | yes |
| 12 | `exam.loto` offset, rule / N1 | 0.45210 / 0.45641 | rule_mean 0.45209674830115804, n1_mean 0.4564110212515322 | yes |
| 13 | `exam.loto` counts, rule / N1 | 1.06003 / 0.99387 | rule_mean 1.0600310620286142, n1_mean 0.9938748881787092 | yes |
| 14 | `exam.loto` sign, rule / N1 | 0.7676 / 0.7676 | rule_mean 0.7676004379784978, n1_mean 0.7676004379784978 (tie to reported precision) | yes |
| 15 | `exam.dial` means over 5 seeds, existence, f = 0/0.25/0.5/1.0 | −0.00451 / −0.04648 / −0.05772 / −0.06167 | computed from `exam.dial`: −0.0045104, −0.0464799, −0.0577219, −0.0616734 | yes |
| 16 | `exam.dial` means, offset, same f | +0.02446 / +0.03734 / +0.04137 / +0.03872 | +0.0244650, +0.0373436, +0.0413666, +0.0387244 | yes |
| 17 | `exam.dial` means, counts, same f | −0.06772 / −0.05747 / −0.04085 / −0.04220 | −0.0677187, −0.0574707, −0.0408525, −0.0421995 | yes |
| 18 | `exam.dial` means, sign, same f | 0.0 at all four | 0.0 at all five f values (incl. f = 0.75, not quoted in chat) | yes |
| 19 | `m(1.0) / m(0.0)` (existence dial ratio) | 13.67 | 13.673448882054943 | yes — but see the round-2 correction below (the ratio is undefined by the harness when `m(0.0) ≤ 0`) |
| 20 | acceptance A5 wording | "at most 0.25 × its margin at f = 0" | `2026-09-23-c6-amendment-acceptance.md:98`: "PR's held-out existence margin over N1 on PL1's dial at f = 1 (mean of 5 seeds) is at most **0.25 ×** its margin at f = 0" | yes, quoted correctly |
| 21 | `dial_ratio` applied only to PL1/PR | `harness.py:1329` | `dial_ratio(out["PL1/PR"])` at line 1329, inside the acceptance-criteria block (`harness.py:1300–1340`); no other call to `dial_ratio` found in that block | yes |
| 22 | loto / dial excluded from every verdict label | `harness.py:~1046–1058` | `labels` is built at lines 1046–1058 from `dnr`, `r1`, `r2`, `r3`, `r4` only; `lo` (loto, line 1045) and `dial_out` (line 1030–1044) are computed but never read when building `labels` | yes |
| 23 | P2 offset in-sample margin | −0.05926 | `exam.P2.insample_rule.offset` − `exam.P2.insample_n1.offset` = 0.4368102112282294 − 0.496066052957276 = **−0.05925584** | yes (rounds to −0.05926) |
| 24 | BF_3 margin | +0.04034 | `exam.P4.bf` at rank 3 is not in this run's own record (this run's `P4.bf.margin` is at rank 12); the +0.04034 figure is the v1-verified `harness_controls.json` rank-profile row (v1 §2 row 4), reconfirmed here, not a new number from [9]/[10] | yes, but sourced from `harness_controls.json`, not `result.json` |
| 25 | BF_12 margin | +0.04851 | `exam.P4.bf.margin` = 0.0485130054821417 at `exam.P4.bf.rank` = 12; also `exam.P4.threshold` = same value (BF is the binding threshold, not RP) | yes |

**Discrepancy notes.**

- None of rows 11–23 and 25 differ from the file at the reported precision.
- **Row 24 (BF_3 / BF_12) is not a discrepancy but a sourcing note, carried over from v1's
  discrepancy on this same pair of numbers:** BF_3 (+0.04034) and BF_12 (+0.04851) are cited
  together in [9] as if from one table; BF_3 is a rank-profile control value
  (`harness_controls.json`), BF_12 is this run's own P4 opponent (`result.json`). They are
  different fits at different ranks that are not interchangeable, though both are correctly
  quoted from their respective sources.
- **Ark's "two implementations, one number" claim (dial f = 1 existence, −0.06167, vs. P3 shuffled
  mean, −0.06431).** The two values differ by **0.0026**, as Ark states. Checked against
  `harness.py`: `shuffled_bank` (line 907, used by P3) and `dial_banks` at f = 1.0 (line 924, used
  by `exam.dial`) both call the same function, `rewire_and_permute(base, rng, f)`, with `f = 1.0`
  in both cases — so the destruction mechanism is identical. They are **not**, however, independent
  in the sense of two separate implementations: they are the *same* function called with different
  RNG seeds and different sample counts (P3 averages over 99 shuffled banks, seeds 0–98; the dial
  arm at f = 1.0 averages over only 5 seeds, `10000 + 100·fi + sd`). "Two implementations, one
  number" overstates it — it is one implementation, two seed sets, and the 0.0026 gap is within
  the spread expected from averaging 5 draws instead of 99 of the same random process, not evidence
  of a second, independently-arrived-at number. Recording as a **CC-draft note**, not a rewrite of
  Ark's text.

---

## 3. Predictions (final)

Authors' numbers are kept exactly as given; logical defects against criteria (i)–(iv) (per the
blind report's B.2/C.1 test) are flagged in the **CC-draft note** column, not silently fixed.
Items marked *(v2, unchanged)* were not touched in round two. Items marked *(v3, revised)* replace
the v2 text verbatim per the authors' round-2 messages.

### Johnny (P-J)

| id | claim | quantity (direction) | refuting outcome | undetermined zone | run/record field | new registration requirement | CC-draft note |
|---|---|---|---|---|---|---|---|
| P-J1 *(v2, unchanged)* | Rule #2, containing BF_r's logit, inherits BF's held-out existence margin over N1 | ≥ +0.040 (BF_3 +0.04034, BF_12 +0.04851) | < +0.030 | [0.030, 0.040) | `P4.rule_margin_existence` | none | Converges with A1-E (both ≥ +0.040) on different grounds (form defect vs. BF-by-construction); flagged by Johnny himself as convergence, not confirmation |
| P-J2 *(v4: withdrawn)* | — | — | — | — | — | — | **Withdrawn on Mike's word (group chat, 2026-09-23 11:33 UTC), on CC's recommendation.** The blind reader's round 3 (report D.1) found that the v3 ablation removes two measured components: N1's per-node effects, worth +0.0478 nats over N0, and BF_r's term, worth +0.040 to +0.049. So the +0.025 bar is cleared under either reading, and the item fails (ii). The ablation also doubles compute, and the question it asks (form defect vs overfit) is about the first rule, not rule #2. No ablation run is registered. The question stays open. See §7. |
| P-J3 *(v3, revised)* | Rule #2 fails P4: BF_r is already the best held-out estimate of the residual from training cells; the addition does not push the margin above it | Δ = margin(rule) − margin(BF_r) **≤ 0**; margin(rule) ∈ **[BF_r − 0.005, BF_r]**. A tie (Δ = 0, the addition penalised to zero) is a P4 **fail**, not a pass. | **P4 passes** — fold mean strictly above threshold at declared r (+0.0493 at r = 8, +0.0485 at r = 12) | none named beyond the expected range | P4 verdict of rule #2's exam | none | **Round-2 fix applied.** v2's "Δ < 0" contradicted its own expected range [BF_r − 0.005, BF_r + 0.005] (a margin of +0.003 satisfied the range but violated "< 0", and a tie satisfied "< 0"'s complement while still failing P4). Johnny's fix: Δ ≤ 0, range's upper bound moved to exactly BF_r. A margin below BF_r − 0.005 refutes the *quantity* (the addition actively hurts on held-out data) but not the *claim* — P4 still fails, same as Ark's P-A3. Converges with A3-P4/P-B5 on outcome; the three now differ only in their quantity bands (see §3b). |
| P-J4 *(v2, unchanged; condition now resolved structurally in §4c)* | If the addition does not touch offset sets, P3 offset ties on all 100 banks and fails; if it touches offset globally, the first rule's N0-like pattern repeats | pass requires held-out real-bank offset Jaccard ≥ 0.4831 (N1 0.42040 + shuffled-max margin 0.06267), effectively N_EB's 0.48417 | **P3 offset passes** at Jaccard ≤ 0.4842 (clears the shuffle without reaching N_EB) | none named | `P3.offset` of rule #2's exam | none | Which branch applies is settled by rule #2's registration field "which fields the addition touches" (§4c), not by asking Zcode separately — see §4c |
| P-J5 *(v5: zones fixed by CC per the reader's D.1; confirmed by Johnny in the group chat, 2026-09-23 11:36:53 UTC — the core claim, the band [−0.010, +0.005] and both refuting outcomes are his, and he accepts CC's branching. He adds one caveat of his own: the item assumes the addition carries no new per-node counts terms. If rule #2's registration says it does, the item is expected to fall, margin > +0.015.)* | Rule #2's counts field is a tie with N1, not new structure, because N1 already has per-node counts terms | held-out counts margin over N1 ∈ **[−0.010, +0.005]**, read against the registration's offset-field statement (§4c): the addition's offset sets = N1's | **two-sided:** margin **> +0.015** (counts structure beyond N1's per-node terms found); margin **< −0.010** (the addition actively hurts counts, as the first rule's −0.0677; "inherits N1's counts behaviour" is false) | (+0.005, +0.015] only; the lower edge is sharp at −0.010 | `P1` counts field of rule #2's exam, read with the offset condition from §4c | none beyond §4c's mandatory offset-field statement | **Round-2 fix applied.** v2 named only the upper falsifier; a margin below −0.01 was neither confirming nor refuting. Johnny's fix adds the lower bound and names it explicitly. The conditioning on the offset field (§4c) is what stops a counts-margin change that is really offset-set-driven (N_EB − N1 counts gap of 0.0785, see blind report B.2's P-J2 row) from being misread as counts structure.  **v4 (CC, per the reader's D.1):** the v3 undetermined zone [−0.015, −0.010) overlapped the lower refuting outcome (< −0.010). It is removed, so the lower edge is sharp. **Branches (§4c):** the item is a prediction only when the addition touches counts and does **not** touch offset sets. If it touches neither, the margin is exactly 0 by construction (definitional). If it touches offset sets, **no prediction**: the counts score moves with the offset field (a missing offset scores 0, spec A3), and no decision rule separating the two was registered. |

### Ark (P-A)

| id | claim | quantity (direction) | refuting outcome | undetermined zone | run/record field | new registration requirement | CC-draft note |
|---|---|---|---|---|---|---|---|
| P-A1 *(v3, revised)* | Acceptance A5's dial criterion applies to rule #2's own existence margin, and its margin disappears under destruction — it neither survives (which would make it ambient) nor inverts (which is what the first rule did) | m(1.0) ∈ **(−0.020, +0.020)**, right bound **strict**; **and** m(1.0)/m(0.0) ≤ 0.25 | (a) m(1.0) ≤ −0.030 (extrapolates against structure, as the first rule did: −0.0617); (b) m(1.0) ≥ +0.020 (margin lives in what destruction does not touch — ambient) | between the refuting bands and the confirming band | `exam.dial` of rule #2 (25 fits already run); `dial_ratio` machinery exists (`harness.py:1324`), **computable from the existing record, no harness change needed** | none | **Condition, stated:** requires `m(0.0) ≥ +0.040`; if `m(0.0) < +0.040` the item makes **no prediction** — `dial_ratio` returns `inf` when `m(0.0) ≤ 0` (`harness.py:1327`), and a ratio of two negative numbers has no reading under A5. **Record-only, not a verdict test** (confirmed against `harness.py`, C.0 of the blind report): `exam.dial` feeds no label and `dial_ratio` is currently applied only to `out["PL1/PR"]`, never to a rule. Constant 0.25 is A5's, registered for PR on PL1, where PR was **given** the true class vector; here the addition is not. Ark transfers the constant himself and flags it as his own choice, not a re-derivation. **Dropped in this round:** "13.67× / an order of magnitude" — meaningless once `m(0)` can be ≤ 0 (`dial_ratio` = inf), and the first rule's actual `m(0)` is −0.00451, i.e. already non-positive, so the "order of magnitude" reading never applied even to the first rule under this corrected understanding. |
| P-A3 *(v2, unchanged)* | P4 fails (fold-mean formulation) | rule margin − BF_r margin < +0.005, AND rule margin ≥ +0.040 | **P4 passes** — fold mean strictly above threshold at declared r (+0.04933 at r = 8, +0.04851 at r = 12); separately, a fall below +0.040 refutes the quantity but not the claim | none named beyond stated | `P4.rule_margin_existence`, `P4.bf.margin`, `P4.threshold` | none | Converges with P-J3 (now fixed) on outcome; the two differ only in their quantity bands (see §3b) |
| P-A4 *(v3, revised)* | Rule #2's offset advantage, **if it exists**, is ambient — it lives in what destruction leaves untouched, not in structure | **at offset field ≠ N1's:** m_off(1.0) − m_off(0.0) ≥ **+0.005** (first rule: +0.0245 → +0.0387, Δ = +0.0142; the +0.005 bar is deliberately set about 2.8× weaker than the first rule's own Δ, registered as such) | **one rule:** m_off(1.0) < m_off(0.0) — the margin does not grow with destruction, so no ambient signature; the offset margin is then either structure or noise | [0, +0.005), named by CC per the reader's D.1 | `dial` of rule #2's exam, offset field | none | **Round-2 fix applied.** v2 offered three witnesses and "any one failing refutes," which is not one falsifying rule (blind report C.1). Ark now states one rule, drops the LOTO witness (loto reduces to N1 on unseen types by construction, so it cannot witness anything about offset structure — same defect as old P-A2, see below), and gives a number instead of "≈ +0.025." **Branch at offset field = N1's** (registration field, §4c): the item **does not apply** — `m_off ≡ 0` by construction on every bank, and that is not a failure of P-A4, it is a different, verdict-facing question, now split out as **P-A6**. |
| **P-A6** *(new, split from v2's P-A4)* | In-sample offset margin ≤ 0 ⇒ P2 fails on offset for this family | in-sample offset margin (rule − N1) **≤ 0** (first rule: 0.43681 − 0.49607 = **−0.05926**) | in-sample offset margin **> 0** | none named | `P2.beats.n1_insample.offset` of rule #2's exam | none | Ark states this is a **verdict** prediction, not part of the ambient-signature claim — kept separate from P-A4 on purpose, per the blind report's C.1 note that P-A4 "presupposes... is a verdict prediction; say so." |

**Withdrawn this round (moved to §7):** P-A2 (LOTO existence ratio) and P-A5 (residual R² on BF),
both withdrawn by Ark. See §7 for his stated reasons and the registration note that replaces
P-A2's structural claim.

### Blind reader (P-B), from Part A of `docs/plans/2026-09-23-blind-reader-report.md`

| id | source | claim | quantity (direction) | refuting outcome | run/record field | CC-draft note |
|---|---|---|---|---|---|---|
| P-B1 | A1-E | P3's existence arm passes for rule #2 | real-bank existence margin over N1 ≥ +0.040; shuffled max ≤ +0.025; gap ≥ +0.015 | any of the 99 shuffled banks ≥ real margin (P3 existence fails); or gap < +0.015 with the arm still passing (quantity refuted, claim not) | `P3.existence` of rule #2's exam | Two independent refuting conditions named for quantity vs. claim, as B.2 requires |
| P-B2 | A1-O | P3's offset arm fails unless rule #2's offset field beats N_EB | needs real-bank held-out offset Jaccard ≈ 0.4204 + 0.0627 = 0.4831, essentially N_EB's 0.4842 | P3 offset passing while held-out mean offset Jaccard ≤ 0.4842 | `P3.offset` of rule #2's exam | Same falsifying condition as P-J4, stated independently; see §3b. **Caveat carried from Part C:** the 0.06267 bar is the first rule's (and N0-as-a-rule's) shuffled max, not rule #2's own — the bar is an estimate |
| P-B3 | A2-k | Starts do not move BF_r's (or rule #2's) held-out existence margin | \|margin(k=10) − margin(k=3)\| < 0.001 nats | difference ≥ 0.001 nats | new: BF_r and rule #2 run at k = 3 and k = 10 | Change-form prediction, not a level — satisfies B.5's checklist item 3 directly. **Registration requirement per §4b:** this second run is descriptive; only the registered k = 10 run's verdict counts. **Known value (BF half, at r = 8):** already measured, Δ = +0.00005 between k = 3 and k = 10 (§2 row 6) — well inside the < 0.001 band. Only the rule #2 half is still a prediction. |
| P-B4 | A2-r | Rank saturates near r ≈ 8; P4's threshold moves with declared rank, so rank does not help against P4 | BF_r's held-out existence margin on the real bank ∈ [+0.045, +0.052], **narrowed per the reader's C.5 to apply only at rule #2's declared r, if that r is ≥ 8** | BF_r's margin outside that range at rule #2's declared rank (r ≥ 8) | `harness_controls.json` rank profile / rule #2's own BF_r fit | Narrowing applied exactly as the reader's C.1/C.5 asked — the claim covered every r in 8…64 but only the declared r is measured. **Known values, already measured (BF fits are deterministic):** r = 8 → +0.04933, r = 12 → +0.04851, r = 16 → +0.04851 (§2 row 4, `harness_controls.json`). The item is a prediction only at a declared r that has not been run yet. |
| P-B5 | A3-P4 | Rule #2 fails P4 | rule margin − BF_r margin < +0.005 nats; in absolute terms margin stays below +0.054 at r = 12 | rule margin exceeds BF_r's by ≥ +0.005 nats (a pass by less refutes "fails P4" but not the quantity) | `P4.rule_margin_existence`, `P4.bf.margin` | **Correction note carried from the report's own B.3**: the reader's §A.3 rationale ("if the residual is rank-≤r bilinear, BF_r already extracts it") is corrected in B.3 — P4 is unreachable by construction only when **BF_r is already the best held-out estimator of the residual buildable from training cells**, not merely when the residual is low-rank (PL1/PR is the counterexample: rank ≤ 4 structure, PR clears BF_4 at +0.133 vs +0.074, because PR has the true classes for free). Part A's text is left as written in the report; this is the report's own correction of it, carried here rather than silently folded in |
| P-B6 | A3-P1 | If rule #2's existence logit contains N1 + BF_r (plus any addition), P1's existence arm passes. *(The v3 narrowing to a "small addition" is dropped per the reader's D.1: §4c has no size field. An addition that damages BF's fold wins is exactly what would refute this item.)* | ≥ 9 of 10 folds beating N1 on existence | ≤ 8 of 10 | `P1.existence.wins` of rule #2's exam | If existence is not touched, this is definitional (BF_r's fold wins, 10/10 at r = 8 and r = 12); see §4c |

---

## 3b. Agreements and disagreements across the three sets

| axis | agree | disagree | what separates the outcomes |
|---|---|---|---|
| Existence margin level ≥ +0.040 | P-J1, P-A3, P-B1 all predict ≥ +0.040 on the real bank | — | `P4.rule_margin_existence` or `P3.existence.real_margin` ≥ +0.040 |
| P4 outcome | P-J3 (fixed), P-A3, P-B5 all predict P4 fails | Quantitative width only: P-J3 "Δ ≤ 0, margin ∈ [BF_r − 0.005, BF_r]" vs. P-A3/P-B5 "rule − BF_r < +0.005" | **Any margin strictly above BF_r is a P4 pass, and refutes the *claim* of P-J3, P-A3 and P-B5 alike** — this is what "P4 passes" means for all three, not just for P-J3. A tie (Δ = 0, margin exactly at BF_r) satisfies all three items' quantities and fails P4 — it does not separate them. The only outcome that still separates P-J3 from P-A3/P-B5 is a rule margin in **[+0.040, BF_r − 0.005)**: it refutes P-J3's quantity (which requires margin ≥ BF_r − 0.005) while confirming P-A3's (which only requires margin ≥ +0.040 and rule − BF_r < +0.005). |
| P3 offset | P-J4 and P-B2 use the *same* numeric bar (Jaccard ≥ 0.4831–0.4842, essentially N_EB) and the same falsifier | Only in framing: P-J4 is conditional on whether the addition touches offset sets at all, now resolved structurally by §4c's mandatory registration field rather than by a separate question to Zcode; P-B2 is unconditional | The §4c registration field ("which fields the addition touches") resolves P-J4's condition directly; the Jaccard value itself resolves both |
| Counts / offset attribution | P-J5 (fixed: counts is a tie or a loss, not structure, read against the §4c offset-field statement) | vs. no counts claim in P-A or P-B v3 sets | `P1` counts margin with §4c's offset-field statement, or the offset Jaccard printed alongside |
| Rank/starts as a knob | P-B3 (starts, change-form) and P-B4 (BF's own rank profile, narrowed to the declared r) agree that starts barely move the margin and rank saturates near r ≈ 8 | — | Both are satisfied by the k = 3/10 run (P-B3, §4b item 7a) and the declared-r BF fit (P-B4) |
| P1 existence "where a pass could come from" | — | P-B6 predicts P1 existence *passes* (≥ 9/10 folds) if rule #2 is BF_r-plus-an-addition; the superseded v1 Johnny/Ark framing ("if it passes anywhere, it is offset or counts, not existence") is dropped in the v2/v3 rewrites — no current item now claims existence cannot pass P1 | `P1.existence.wins` of rule #2's exam settles it directly |

**Note, not a row (round-2 correction, replacing the v2 "form defect vs. content-fit" row).**
Ark's chat prose in round one argued from the dial/loto numbers that rule #2's existence margin is
"content-fit, not structure," because the margin deepens under destruction at f = 1 in the
first rule's own case, rather than shrinking. The blind reader's round-2 review (report C.2) found
the premise wrong: **degree is preserved under the shuffle** (spec A10), so a pure "missing
degree-term" form defect predicts **no change** in the margin under destruction, not a shrinking
one — degree-preserving rewiring does not touch what a form defect built on degree would be
sensitive to. The observed deepening is simply the recorded P3 existence pass (the rule does
relatively better on the real bank than on shuffled ones); whether to call that "structure" or
"content-fit" is a naming question these numbers do not settle on their own. **No item in v3 turns
this into a named-outcome disagreement** — doing so would need each side to name a rule #2 outcome,
which neither author has done. Recorded as a note, not a table row, per the reader's own C.2
finding.

---

## 4. Constraints for rule #2's registration

**`[informed by proposal / rule side]`** — the items below rest in part on content read from the
first rule's proposal or its rule-side mechanics, per the blindness record in §1 and the sourcing
noted inline.

**(a)** and **(c)** are kept verbatim from v1 (CC's corrections already applied there):

- **(a) P4's threshold (Ark).** P4's threshold is max(the random-projection threshold, BF_r's
  held-out existence margin over N1), with BF_r fitted at the rule's own declared rank r
  (`docs/plans/2026-09-23-c6-amendment-acceptance.md:115`). On the real bank BF_r's margin is
  +0.028 to +0.049 across r = 1–16, highest at r = 8 (§2 row 4, v1). In plain words: a rule passes
  P4 only if its mean held-out existence margin over N1 is strictly above that of a trained
  low-rank factorisation of its own rank. **Low rank alone does not make P4 unreachable.** On PL1,
  whose planted structure has rank ≤ 4, PR cleared BF_4 (+0.133 against +0.074,
  `harness_controls.json` `controls["PL1/PR"].P4`), because a sharper prior (discrete classes)
  beats a penalised continuous factorisation on finite data. PR was given its classes, so this
  does not show that a *learned* rule can do the same. P4 is unreachable by construction only if
  BF_r is already the best held-out estimator of the residual that any rule can build from the
  training cells and the admissible fields. A rule of the form "BF_r plus X" can clear P4 only if
  X adds held-out existence information that BF_r does not carry. If X is penalised to zero, the
  rule ties BF_r, and a tie fails (A7). Corrected on the blind reader's review (B.3); the first
  draft of this item was wrong.
- **(c) Correction: §2.6 does not vary starts.** The proposal's §2.6 is about the rule's own `k`,
  the dimension parameter in `first_rule_k12` that is also its declared rank r = 12
  (`GLOSSARY.md` §10; checked by CC against the proposal). It is **not** the number of starts,
  which is 10 or 3 (acceptance part 3 (c)). So the k = 8/16 sensitivity arm already varies the
  rule's complexity knob that Ark and Zcode asked for. The original text of this item follows,
  kept for the record. Its premise (that §2.6 varies starts) is wrong. Its point about starts
  stands on its own.
  **(Original.) §2.6 varies the wrong knob (Ark).** §2.6 as referenced varies starts k, but the
  profile in `harness_controls.json` shows starts barely move BF's margin (+0.00006 nats from k=1
  to k=10) while rank moves it 1.75× (r=1: +0.028 to r=8: +0.049). The knob that matters for
  "search-limited vs. family-limited" is rank, or the rule's own complexity parameter — not the
  number of starts.

---

## 4b. Registration requirements for rule #2's run

Collected from the v3 predictions (§3) and the blind report's B.5/C.5 checklists.

1. ~~Degree-term ablation as a separate registered run (P-J2).~~ **Dropped** on Mike's word (2026-09-23 11:33 UTC),
   together with P-J2 (§3, §7). No ablation run is part of rule #2's registration.
2. **Per-fold held-out logits for N1, BF_r and rule #2** (needed for a paired resolution of P4
   only, per Ark; per-fold BF_r and RP_r scores already suffice for the reader's own items):
   currently only mean BF margin is recorded (`harness.py:1043` region). **This is
   a harness change**, so `--controls` must be re-run with every existing verdict unchanged (A20)
   before it can be used.
3. **Per-type loto values, not only the 65-fold mean** (dropped as a prediction with P-A2's
   withdrawal, but kept as a useful diagnostic per Ark's structural note below): currently
   `exam.loto` records only `rule_mean`/`n1_mean` per field (verified rows 11–14, §2). **This is
   also a harness change**, requiring the same `--controls` re-run (A20).
4. **Offset Jaccard printed next to the counts margin — already satisfied, no change needed.**
   `per_fold_rule` already carries both the offset and the counts fields per fold, and
   `RESULT.md`'s P1 table already prints both. "Offset held fixed" (the other half of P-J5's
   condition) would be a **different predictor** — a separate variant run, not a record change.
5. **`dial_ratio` applied to rule #2, not only to PL1/PR** (P-A1): the current code applies it only
   to `out["PL1/PR"]` (`harness.py:1329`), and this is **computable from the existing `exam.dial`
   record with no harness change**. This changes what the **record** reports, not the verdict.
   **As a pass condition it would contradict spec §4.4/§5.3 and spec A12** ("descriptive...
   does not enter the decision"); it stays descriptive.
6. **The spread-log assert** (from chat [2], Zcode, blind-safe summary only — see §6): `assert
   lines_written == fits_attempted` at the end of the run, loud failure on mismatch. **Open
   question, not settled by any file read for this draft:** whether the assert runs *after* the
   record is written (a failure then flags a bad run without destroying its record) or *before*
   (a failure then turns a finished exam into a crashed run with no record at all), and whether
   such a failure should **void the verdict**. Left open as a decision for Mike.
7. **k-sensitivity, split into two registration items** (per the blind reader's round-2 review,
   report C.3 item 7 — v2's single item conflated two different knobs):
   - **(a) Starts, k = 3 vs. k = 10** (P-B3): a second full exam run at k = 3, compared to the
     registered k = 10 run.
   - **(b) The rule's own dimension parameter** (rank r), if wanted: changing it also changes the
     declared r and therefore BF_r's P4 threshold (+0.0493 at r = 8 vs. +0.0485 at r = 12, and
     other values from the BF rank profile — see §4c). Report, at each value tried: the rule's own
     margin, BF_r's margin at that r, and their difference.

   **Descriptive only.** The k = 3 run (7a) and any dimension-parameter
   runs (7b) are all **descriptive**: only the run registered under rule #2's declared r and k = 10
   produces a verdict. **Choosing among variants after seeing their results is not allowed** — that
   would be exactly the multiplicity the spec's registration-before-running structure exists to
   prevent (per the task's original instruction in §1: "predictions first, then this file... then
   rule #2 is written").

---

## 4c. Mandatory fields of rule #2's registration `[informed by proposal / rule side]`

Before rule #2's run, its registration must state:

1. **The declared rank r.** This fixes P4's threshold directly: **+0.04933 at r = 8**,
   **+0.04851 at r = 12**; at other r, read the corresponding value off the BF rank profile in
   `harness_controls.json` (§2 row 4: r = 1 → +0.02815, r = 3 → +0.04034, r = 4 → +0.03972).
   Every quantity in §3 that cites "+0.0493" or "+0.0485" is conditional on this field.
2. **The timing cap**, per acceptance part 3 (c) — fixes how many starts (10 or 3) the registered
   run itself uses, distinct from the k = 3 diagnostic run in §4b item 7a.
3. **Which fields the addition touches: existence / offset sets / counts / sign.** This is the
   field that resolves the conditional predictions below. State it as a checklist over the four
   fields, not a single yes/no, since an addition can touch some and not others.

**Verdict facts that follow from field 3 by construction (CC, on the blind reader's D.2; stated
before any run so that no confirmation in these branches is read as evidence):**

- **If the addition does not touch offset sets**, rule #2's offset field is N1's. Then P1 offset
  fails (every fold ties N1, 0 wins), P2 fails on offset (in-sample margin exactly 0, and a tie is
  not a win, A7), and P3 offset fails (a tie on all 100 banks). **Rule #2 cannot pass C6 in this
  branch, whatever its existence margin.**
- **If the addition does not touch existence**, rule #2's existence predictions are computed the
  same way BF_r's are. P4's pass test is a plain strict `>`, with no τ (`real_m["existence"] >
  thr`, `harness.py:1028`). So this branch is definitional only under a further condition: **if**
  rule #2's per-fold existence predictions are bit-identical to BF_r's, the margin ties the
  threshold exactly and P4 fails by definition, and P-J3, P-A3 and P-B5 would confirm trivially —
  not evidence. **Otherwise** (any non-identical computation path — different operation order,
  clipping, or the rule's own float32→float64 decode, `harness.py:277`) the difference is
  noise-level (about 1e-12), and that noise, not construction, decides P4 in either direction.
  "Fitted as the harness fits them" is not enough to guarantee bit-identity.
- **Without an offset touch, rule #2 cannot pass C6 in this branch, whatever its existence
  margin** (unconditional, per the first bullet). Without an existence touch, P4 is either a
  bit-identical tie (fail) or decided by float noise; neither confirms or refutes P-J3/P-A3/P-B5 as
  evidence about the addition. Rule #2's registration must say which case it is in.

**Branches selected by field 3.** Each cell is either a prediction, marked "prediction", or a
consequence of the definition, marked "definitional". A definitional cell is not evidence either
way.

| prediction | existence not touched | offset sets **not** touched | offset sets touched |
|---|---|---|---|
| P-J3, P-A3, P-B5 (P4) | definitional **only if** rule #2's per-fold existence predictions are bit-identical to BF_r's (tie, P4 fails, `harness.py:1028` plain `>`, no τ); otherwise Δ is noise-level (~1e-12) and P4 is decided by noise, not construction | (as the existence column decides) | (as the existence column decides) |
| P-J4 | — | definitional: tie on all 100 banks, P3 offset fails | prediction: the Jaccard bar (≥ 0.4831, essentially N_EB's 0.48417) |
| P-A4 | — | does not apply (`m_off ≡ 0` by construction) | prediction: m_off(1.0) − m_off(0.0) ≥ +0.005 |
| P-A6 | — | definitional: in-sample offset margin exactly 0, P2 fails on offset | prediction: in-sample offset margin ≤ τ (P2 fails on offset) vs > τ. It tests whether X's offset model contains N1's per-source mode |
| P-J5 | — | if counts are not touched either: definitional (margin exactly 0). If counts are touched: prediction, as stated | no prediction (the counts score moves with the offset field; no decision rule registered) |
| P-J1 | definitional: margin is BF_r's margin at the declared r (+0.04933 at r = 8, +0.04851 at r = 12, +0.03972 at r = 4) — settled by the declared r, not by the run | — | — |
| P-B6 | definitional: BF_r's fold wins, 10/10 at r = 8 and r = 12 | — | — |

**Registration note, not a prediction (Ark's LOTO structural finding).** If the addition X is zero
on a wholly unseen type, the LOTO existence ratio (rule_mean / n1_mean) for **any** BF-based rule
is exactly **1.00** by construction — because BF_r itself reduces exactly to N1 on leave-one-type-
out cells (`harness.py:666–695`: the SVD residual row for a fully held-out type is zero, so the
penalty gradient drives every start's factor for that type to zero, and N1's own per-type effect is
penalised to zero the same way). A LOTO ratio ≥ 1.3 is therefore a useful **red flag** that X is
overfitting by type, but the ratio's baseline of 1.00 is a fact about the rule's *form*, not about
the bank, so it is recorded here as a condition to check the registration against, not as a
falsifiable prediction (see P-A2's withdrawal, §7, for why it was pulled as a prediction).

---

## 5. Record defects to fix before rule #2's registration (Ark's five, v1, annotated by the blind reader's B.3)

Checked against `result.json`, `RESULT.md`, and `HARNESS-CONTROLS.md`.

1. **Wins denominator printed differently per field — holds.** `P1.existence` carries only
   `"wins": 5` (out of 10 folds, unstated), while `P1.offset` carries both `"wins_vs": {"N1": 5,
   "N0": 0, "N_EB": 1}` and a separate `"wins": 0`. The same word ("wins") names two different
   things in two adjacent fields of the same record; a reader (Johnny) read the offset field as
   "5/5" where the correct reading is "5 of 10 folds against N1." **Holds per B.3.**
2. **Sign arm without power counted as pass — annotated.** `P1.sign.pass` is `true`, but `P3.sign`
   shows the rule tied exactly with N1 (margin 0.0) on the real bank and on all 99 shuffled banks.
   **Blind reader's B.3 judgment: this is registered behaviour, not a record error** — a tie is not
   a loss under P1's non-inferiority rule (acceptance A7), so the pass label is doing what it is
   defined to do. The gap is a **reporting** gap (nothing flags that the field had no discriminating
   power), not a defect in the record itself. **Ark accepted this reading in [10]**: "дефект 2 —
   зарегистрированное поведение (A7: ничья не проигрыш), действительно не ошибка записи."
3. **"rule did not run" label shared by three objects — annotated, weaker than stated.** The label
   appears in `first_rule_k12`'s own verdict, in `HARNESS-CONTROLS.md`'s N2 criterion result, and
   implicitly in A6's failure list (PR-sh). **Blind reader's B.3 judgment: weaker than originally
   stated** — verdict labels are shared strings by design (spec §5.2), and three objects carrying
   one label is what a label is for; the real collision (a genuinely "did not run" case vs. a
   crashed run) is already handled elsewhere in `GLOSSARY.md`. **Ark accepted this in [10]**
   alongside defect 2.
4. **Verdict line joins five labels with no per-check mapping — holds.** `RESULT.md`'s verdict
   line reads "FAIL -- rule did not run; copy or marginal; below threshold for this family; family
   fits anything; ambient, not substantive structure" — five labels in one string, with no table in
   the record mapping each label to the specific check (P1/P2/P3/P4/N0) that produced it, beyond
   what a reader has to reconstruct from the separate P1–P4 tables above it.
5. **λ curve not recorded — holds.** `first_rule_k12/RESULT.md`'s P4 section records only the
   chosen λ per fold (3.0 in every fold). `HARNESS-CONTROLS.md`'s M5 criterion confirms a grid
   {1, 3, 10, 30, 100} was used by nested CV, but no file read for this task contains the margin at
   each λ on the grid — only the winning value.

Defects 1, 4 and 5 hold as stated; defect 2 is registered behaviour surfaced as a reporting gap,
not a record error; defect 3 is weaker than originally stated. Ark accepted both annotations in
message [10].

---

## 6. Zcode `[informed by proposal / rule side]`

Answered in chat [2] (09:36 UTC). Rule-side mechanics are in
`docs/plans/2026-09-23-first-rule-failure-rule-side.md`, marked "OFF LIMITS to blind reviewers"
and closed to this file's authors accordingly — not opened for this draft. Blind-safe summary,
from chat [2] only:

- Of the failure mechanisms named in advance (proposal §4), three fired: offset, counts, and P4
  (harder than "even odds"). The decisive failure, existence, was **not** in the named-risk list —
  it had been predicted to pass, and the proposal's stated "most likely outcome" (win existence,
  lose offset) did not occur.
- The proposal's random-label control and its starts-sensitivity check were never run in the first
  place. Carrying them into rule #2's registration means reformulating, not reusing verbatim: the
  random-label control needs family-independent framing with the arm's resolution (~0.02) named
  against the effect size sought (~0.005) so it registers as a resolution report, not a decisive
  arm; the starts-sensitivity check is nearly inert on its own (starts move the margin by +0.00006)
  and should only carry forward paired with the new family's own complexity knob, named, or stay
  descriptive.
- The missing spread-log line (one CV fit short of the expected count) is not being investigated
  before rule #2; instead, an assert (`lines_written == fits_attempted`) is added at the end of the
  run, with a loud failure on mismatch, placed where the first attempt already broke. **See §4b
  item 6: whether this assert runs before or after the record is written, and whether its failure
  voids the verdict, is not settled by any file read for this draft.**

---

## 7. Superseded items (not registered)

One line each, compressed, with the review verdict that superseded them.

### From v1 (superseded by the blind report's round-1 review, B.2)

| id | v1 claim (one line) | B.2 verdict |
|---|---|---|
| P-J1 (v1) | Held-out existence failure is mainly a form defect | fails (i), (ii), (iv) — falsifier and confirming outcome not complementary; random≈learned predicted by both readings; "§4.3" names the wrong arm |
| P-J2 (v1) | Counts structure is node-level, a per-rule motif too coarse | fails (ii) — N1 already has node-level counts terms; a tie "passes" |
| P-J3a (v1, `[informed]`) | Random-label margin ≈ learned margin (capacity, not structure) | fails (iv), (ii) weak — arm not identifiable from allowed files; resolution vs. effect size caveat applies |
| P-J3b (v1, `[informed]`) | Starts sensitivity (k=8/16) will not flip the sign | fails (i), (ii), (iv) — band includes values that both confirm and refute; level not change; k = 8/16 is not a starts value |
| P-J4 (v1, "P3" in Johnny's numbering) | Rule cannot clear BF_r's existence threshold; if it passes anywhere, it's offset or counts | fails (i) — P4 is a fold-mean test, falsifier stated per-fold; band inconsistent with BF_r's own level |
| P-A1 (v1) | Rule and BF_8 chase the same residual | fails (iv), (i)/(ii) weak — no per-fold BF scores in the record |
| P-A2 (v1) | Capacity is not the problem (complexity sweep) | fails (iv), (ii) conditional — "complexity sweep" not a registered arm; test only separates readings if it brackets r ≈ 8 |
| P-A3 (v1) | Per-source counts terms fix the counts arm | fails (i), (ii) — non-inferiority threshold is 0, not −0.02; N1 already has these terms |
| P-A4 (v1) | Power warning: §4.3/§2.6 resolution (~0.02) vs. effect sought (~0.005) | correctly recorded as a caveat, not a prediction — kept as constraint §4(b) |
| P-A5 (v1, random-label) | Random labels worse than learned, but only partially | fails (i), (iv); (ii) below resolution — unsigned quantity, arm not identifiable |
| P-A6 (v1, "P5") | §2.6 starts/rank arm empty at the starts axis | fails (i), (ii), (iv) — level not change; band inconsistent with BF-based rule's actual level |
| P-A7 (v1, "P6") | "BF plus something" will not clear BF_r's threshold | fails (i) — same P4 fold-mean defect as P-J4 |
| P-A8 (v1, "P7") | If rule #2 passes anywhere, it is on counts | fails (ii) — P1 counts non-inferiority means a tie "passes"; does not separate readings |

**Items that passed all four in v1: none**, confirmed by the blind report (B.2 summary): the
closest were P-J2 (failed only (ii)) and P-A7/P-J4 (failed only (i); fixed in v2 by restating the
falsifier as "P4 passes").

### From v2 (superseded by the blind report's round-2 review, Part C, and withdrawn by Ark himself)

| id | v2 claim (one line) | round-2 finding | Ark's stated withdrawal reason ([10]) |
|---|---|---|---|
| P-A2 (v2) | An addition built on BF does not close the leave-one-type-out (loto) existence gap: `loto.existence.rule_mean / n1_mean ≥ 1.5` | C.1: fails (ii) — BF_r reduces **exactly** to N1 on loto cells (`harness.py:666–695`), so the ratio is set by whether X is zero on unseen types, a fact about the rule's *form*, not the bank; the reader's own counter-prediction is ratio ≈ 1.00 for a BF-based rule whose addition vanishes on unseen types | "Читатель нашёл структурный факт: на LOTO-ячейках BF_r точно равен N1... для правила «BF + X» отношение LOTO равно 1.00 плюс то, что X делает на невиданном типе... Моя формулировка «банк противостоит обобщению типа» неверна, снимаю." Replaced by the registration note in §4c (structural fact, not a prediction). |
| P-A5 (v2) | The rule's residual over N1 lies in BF_r's direction: R² of (rule logit − N1 logit) on (BF_r logit − N1 logit) ≥ 0.70 | C.1: (ii) weak to failing — if rule #2 *contains* BF's term, (rule − N1) = BF-term + X, so R² is high by construction and measures the size of X relative to BF, not "same residual" as a fact about the bank; only separates readings if the bilinear part is fit independently of the harness's BF_r | "Читатель прав: ...R² высокий по построению... Различить версии он может только если билинейная часть правила фитится независимо от BF стенда. Снимаю. Требование пер-ячеечных логитов в регистрации остаётся, но для парного разрешения P4 и A1-O, не для этого R²." Per-cell logits kept as a registration requirement (§4b item 2), repurposed for P4/P-B2 pairing, not for this R². |

---

### From v3 (withdrawn after the blind reader's round 3, Part D)

| id | claim | why withdrawn |
|---|---|---|
| P-J2 (v3) | a degree-term ablation separates "form defect" from "overfit" | fails (ii): the ablation removes two components worth about +0.048 and +0.045 nats, so the +0.025 bar is cleared under either reading (report D.1). Withdrawn on Mike's word, 11:33 UTC |

## Files opened for this draft (v3)

- The group chat dump for both rounds (read whole; round-2 messages [7]–[10] used directly for
  this file's changes; round-1 messages [1]–[10] carried over from v2's own file list)
- `docs/plans/2026-09-23-blind-reader-report.md`, in full, including Part C (C.0–C.5)
- `docs/plans/2026-09-23-first-rule-failure-predictions.md` (this file's own prior version, v2)
- `results/genome/c6/rule_runs/first_rule_k12/result.json`, `RESULT.md` (carried from v2; not
  reopened for new numbers this round — no new numbers were introduced in round two)
- `results/genome/c6/checks/n1_alone/summary.json`, `RESULT.md` (listed to confirm no new numbers
  were needed from them this round; not re-read beyond the listing)
- `results/genome/c6/harness.py` (carried from v2's own citations; not reopened this round)
- `results/genome/c6/HARNESS-CONTROLS.md`, `harness_controls.json` (carried from v2)
- `docs/plans/2026-09-23-c6-amendment-acceptance.md` (carried from v2, A5 window)

No file under `results/genome/c6/rules/`, `results/genome/c6/rule_runs/first_rule/`, or either of
`2026-09-23-first-rule-proposal.md` / `2026-09-23-first-rule-search-criterion.md` /
`2026-09-23-first-rule-failure-rule-side.md` was opened, listed, or searched for this draft.
