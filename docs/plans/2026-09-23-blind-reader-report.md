# Blind reader report: predictions for rule #2, and a logic review of the draft

**Status:** working note by a blind reader. Not a registration and not committed by its author.
**Blindness:** the reader has not opened `docs/plans/2026-09-23-first-rule-proposal.md`,
`docs/plans/2026-09-23-first-rule-search-criterion.md`, anything under `results/genome/c6/rules/` or
`results/genome/c6/rule_runs/first_rule/`, or the group chat. Terms are those of `GLOSSARY.md`.

---

## Part A: the reader's own predictions (written before reading the draft)

**Written:** 2026-09-23 09:35 UTC (16:35 local, +07:00). Saved before
`docs/plans/2026-09-23-first-rule-failure-predictions.md` was opened.

**Sources used in Part A:** `GLOSSARY.md`; the C6 spec (§4.3, §5.1, A7, A9–A11, A19); acceptance
files 1–3; `results/genome/c6/HARNESS-CONTROLS.md`; `results/genome/c6/harness_controls.json`;
`results/genome/c6/rule_runs/first_rule_k12/RESULT.md` and `result.json`;
`results/genome/c6/checks/n1_alone/RESULT.md` and `summary.json`.

**What "rule #2 = BF_r plus an addition" is taken to mean here.** Its existence logit contains
N1 logit + U_s·V_t at rank r, fitted from training cells as BF_r is, plus some further term. The
reader does not know what the addition is, or which fields it touches. Where a prediction depends
on that, the prediction says so.

### A.0 Numbers the predictions rest on

| quantity | value | file and key |
|---|---|---|
| N1 held-out existence log-loss, real bank | 0.36248 | `harness_controls.json` `nulls_real_bank.N1.existence` |
| N1 held-out existence, 99 shuffled banks (min / mean / max) | 0.35938 / 0.36234 / 0.36564 | `checks/n1_alone/summary.json` `fields.existence` |
| N1 held-out offset Jaccard, real / shuffled max | 0.42040 / 0.42210 | same, `fields.offset` |
| N_EB held-out offset Jaccard, real | 0.48417 | `harness_controls.json` `nulls_real_bank.N_EB.offset` |
| BF_8 margin over N1 by starts k = 1, 3, 10 | +0.049268, +0.049280, +0.049331 | `harness_controls.json` `BF_8_real_bank_by_starts.{1,3,10}.margin` |
| BF_r margin over N1 by rank, real bank, k = 10 | r = 1: +0.02815; r = 3: +0.04034; r = 4: +0.03972; r = 8: +0.04933; r = 16: +0.04851 | `harness_controls.json` `controls["real/N0 as a rule" / "real/N1 as a rule" / "real/PR" / "real/RP_r8 as a rule (seed 999)" / "real/oracle"].P4.bf.margin` |
| BF_12 margin, real bank, k = 10 | +0.04851 | `first_rule_k12/result.json` `exam.P4.bf.margin` |
| RP_r threshold on the real bank, all ranks seen | −0.00475 to +0.00120 | `controls[*].P4.rp_threshold` for the real-bank controls; `result.json` `exam.P4.rp_threshold` = −0.00200 |
| first rule, P3 existence: real / shuffled max / shuffled mean | −0.00451 / −0.04355 / −0.06431 | `result.json` `exam.P3.existence` |
| first rule, P3 offset: real / shuffled max / shuffled mean | +0.02446 / +0.06267 / +0.04254 | `result.json` `exam.P3.offset` |
| N0 as a rule, P3 offset: real / shuffled max | +0.02613 / +0.06267 | `harness_controls.json` `controls["real/N0 as a rule"].P3.offset` |
| oracle, P3 existence: real / shuffled max / n ≥ real | +0.36148 / +0.36464 / 43 | `controls["real/oracle"].P3.existence` |
| cells moved by a shuffle, of 604 | 409 to 457 | `harness_controls.json` `control_d_shuffled_banks.cells_changed_min_max` |
| PL0: BF_4 margin, λ chosen | 0.000, λ = 100 in every fold | `controls["PL0/PR"].P4.bf` |

### A.1 The destroyed-structure arm

**Definition (spec §4.3, replaced in part by A9 and A10).** The arm builds 99 shuffled banks
(seeds 0–98): existence is rewired by 12,080 successful degree-preserving swaps, so every type
keeps its in- and out-degree, and the 604 four-field contents are then permuted without
replacement over the rewired non-empty cells. On each shuffled bank the held-out arm is re-run
with the same folds by cell position, for the rule and N1, and P3 holds on a field only if the
rule's real-bank margin over N1 (mean over folds) is strictly greater than its margin on all 99;
P3 needs this on existence and on offset set (§5.1), and a tie counts against the rule (A9).

Two facts from the numbers shape every prediction below:

- **N1's own score does not move under the shuffle on existence** (real 0.36248 inside the
  shuffled range 0.35938–0.36564, 56 of 99 at least as good). So on existence the arm compares the
  rule's own score on real vs shuffled banks. It is *not* passable by accuracy alone: the oracle
  fails it (real +0.36148, shuffled max +0.36464, 43 of 99 at least as high), because a perfect
  predictor's margin is just N1's loss, which the shuffle leaves in place. A rule passes only if it
  is **worse on shuffled banks than on the real one**, i.e. if what it learned is destroyed by the
  rewiring.
- **N1 is weaker on shuffled banks for offset sets** (real 0.42040, shuffled mean 0.40368), so a
  rule with a global, non-type offset prediction gets a *larger* margin on shuffled banks than on
  the real one. N0 as a rule shows it: real +0.02613, shuffled max +0.06267. The first rule shows
  the same pattern and the same shuffled max to every printed digit (0.06266951225736928), so its
  offset field behaved like N0's on the shuffled banks.

**Prediction A1-E (existence).**
- *Claim:* P3's existence arm passes for rule #2.
- *Quantity:* real-bank existence margin over N1 ≥ +0.040; shuffled max ≤ +0.025; so the gap
  (real − shuffled max) ≥ +0.015 nats.
- *Why:* the BF term's margin on the real bank is +0.040 to +0.049 at every rank ≥ 3. N1 is the
  maximum-entropy model for a given degree sequence, and the shuffled banks are degree-preserving
  random graphs, so the bilinear term should find little on them; where there is no low-rank
  structure the nested CV drives BF to λ = 100 and margin 0.000 (PL0). The residue it may find
  comes from the 147–195 cells a shuffle leaves in place (604 − 457 … 604 − 409), mostly at the
  hubs (hub check), which is why the bound is 0.025 and not 0.
- *Refuted by:* any of the 99 shuffled banks with existence margin ≥ the real one (P3 existence
  fails); or a gap below +0.015 with the arm still passing (quantity refuted, claim not).

**Prediction A1-O (offset set).**
- *Claim:* P3's offset arm fails for rule #2 **unless its offset field beats N_EB**. If the
  addition does not touch offset sets (offset = N1's), the margin is 0 on the real bank and on all
  99 (a tie on every bank) and the arm fails; that sub-case follows from the definition and is not
  a prediction. If the offset field is global or N0-like, it fails as the first rule's did.
- *Quantity:* to pass, the rule needs a real-bank offset margin over N1 above the shuffled max,
  which for every rule seen so far on the real bank is +0.06267. That is a real-bank held-out mean
  Jaccard of about 0.4204 + 0.0627 = 0.4831, essentially N_EB's 0.4842.
- *Refuted by:* P3 offset passing while the rule's held-out mean offset Jaccard on the real bank is
  ≤ 0.4842 (it clears the shuffle without reaching N_EB).

**Consequence.** Rule #2 "BF_r plus an addition" that is an existence-only addition gets the label
"family fits anything" from the offset field alone, whatever its existence margin. The verdict
cannot be read as a statement about existence structure unless the offset field is also modelled.

### A.2 Starts vs rank: which knob moves the held-out existence margin

| knob | range seen | margin range | change |
|---|---|---|---|
| starts k (BF_8) | 1 → 10 | +0.049268 → +0.049331 | **+0.00006 nats** |
| rank r (BF_r, k = 10) | 1 → 8 | +0.02815 → +0.04933 | **+0.021 nats** |
| rank r (BF_r, k = 10) | 8 → 12 → 16 | +0.04933 → +0.04851 → +0.04851 | −0.0008 nats (plateau) |

Rank moves the margin about 350 times more than starts do, and only up to r ≈ 8; beyond that the
margin is flat or slightly down (and not monotone below: r = 4 is below r = 3). λ = 3 is chosen in
every fold at every rank ≥ 3.

**Prediction A2-k.**
- *Claim:* the number of starts cannot move the held-out existence margin of BF_r or of a rule
  built on BF_r's SVD start.
- *Quantity:* |margin(k = 10) − margin(k = 3)| < 0.001 nats, for BF_r at rule #2's rank and for
  rule #2 itself if its existence part starts from the same SVD start.
- *Refuted by:* a difference ≥ 0.001 nats between k = 3 and k = 10 for either.

**Prediction A2-r.**
- *Claim:* rank is the only knob with an effect, and it saturates at r ≈ 8. Because P4's opponent
  is BF at the rule's own rank, choosing r does not help a rule against P4: the threshold moves with
  it.
- *Quantity:* for every r in 8…64, BF_r's held-out existence margin on the real bank lies in
  [+0.045, +0.052].
- *Refuted by:* BF_r's margin outside [+0.045, +0.052] at rule #2's rank, if that rank is ≥ 8.

### A.3 P4 for rule #2

**Threshold.** max(RP_r, BF_r). On the real bank RP_r is between −0.0048 and +0.0012 at every rank
seen, so the threshold is BF_r's margin: +0.0485 at r = 12, +0.049 at r = 8.

**Can any rule clear it?** Yes in principle: the oracle does on the real bank (+0.361 against
+0.0485), and PR does on PL1 (+0.133 against +0.074). But both were *given* what BF must learn:
the oracle the answer, PR its true class vector. A rule on the real bank learns its latent
structure from the same training cells BF uses.

**When it is unreachable by construction.** If every part of the existence residual after N1 that
is predictable from training cells (and the admissible per-type fields) is a rank-≤ r bilinear
term U_s·V_t, then penalised BF_r with nested λ already extracts it, and no learned rule can beat
it in expectation; a win would be fold noise. Rule #2 that *contains* BF_r is the sharp case: its
margin is BF_r's plus the addition's, and if the addition is penalised to zero it **ties** BF_r,
which A7 counts as a fail. The plateau at r ≥ 8 is consistent with that property (the bilinear
family has run out of things to find) but does not prove it. The addition can clear P4 only if the
residual has held-out-predictable structure that is **not** bilinear at rank r (for example
through the admissible fields stride, role and layout, which BF does not use, or a non-bilinear
interaction).

**Prediction A3-P4.**
- *Claim:* rule #2 fails P4.
- *Quantity:* its held-out existence margin over N1 minus BF_r's margin (same r, same k) is below
  +0.005 nats; in absolute terms its margin stays below +0.054 at r = 12.
- *Refuted by:* rule #2's margin exceeding BF_r's by ≥ +0.005 nats. (A pass by less than 0.005
  refutes the claim "fails P4" but not the quantity; the two are stated separately so that each has
  its own refuting outcome.)

**Prediction A3-P1 (a by-product, for completeness).**
- *Claim:* if rule #2's existence part is BF_r with at most a small addition, P1's existence arm
  passes: BF_8 beats N1 in 10 of 10 folds, BF_12 too.
- *Quantity:* ≥ 9 of 10 folds beating N1 on existence.
- *Refuted by:* ≤ 8 of 10.

### A.4 What Part A cannot do

- It does not know whether the addition touches offset sets, counts or sign, so A1-O is
  conditional on that.
- BF's margin on shuffled banks has never been computed (P3 is run for the rule only). A1-E's
  shuffled bound is a reasoned guess, not a measured one.
- The per-rank BF numbers come from different controls that happened to use those ranks; they are
  one BF fit per rank, not a sweep registered as such.

---

## Part B: logic review of the consolidated draft

**Written:** 2026-09-23, after Part A was saved (09:35 UTC). Part A above has not been edited
since. Reviewed file: `docs/plans/2026-09-23-first-rule-failure-predictions.md` (DRAFT, not
committed).

### B.0 A finding that comes before the item-by-item review: two arms share one name

In the allowed files, **"destroyed-structure arm" means the spec's §4.3**: 99 degree-preserving
shuffled banks, margins over N1 compared by P3 (`GLOSSARY.md` "arm"; spec §4.3, A9, A10). That arm
produces no "random-label" margin. The draft uses "§4.3 destroyed-structure arm" for a
**random-label arm** ("margin(random − N1) ≈ margin(learned − N1)", P-J1, P-J3a, P-A5, P-A4), and
"§2.6" for a **starts-sensitivity** arm. Neither object is defined in any file the reader may
open; they are presumably the first rule's proposal §4.3 and §2.6. So:

- every draft item that cites "§4.3" or "§2.6" names a run that the exam does not have, and the
  glossary term "destroyed-structure arm" points to a different run. Criterion (iv) fails for each
  of them as written, not because the run cannot exist but because the text does not identify it.
- **The draft makes no prediction about the exam's own destroyed-structure arm (P3) for rule #2.**
  Part A's A1-E and A1-O are about that arm.
- **"k = 8/16" is not a starts value the harness uses.** Starts are 10 or 3 (acceptance part 3
  (c)), and `GLOSSARY.md` §10 says the `k` in `first_rule_k12` "is a parameter of the first rule
  itself, not the number of starts (that run used 10 starts)". So P-J3b's "k = 8/16" is most likely
  the rule's own k, mislabelled as starts. If so, constraint §4(c) ("§2.6 varies the wrong knob")
  may be aimed at the wrong object: the rule's own k may be exactly the complexity knob Ark asks
  for. The reader cannot check this; the draft should say which k it means, by glossary sense.

**Recommendation:** rename the random-label arm and the §2.6 arm with new glossary terms before
commit, and cite them as "proposal §4.3" and "proposal §2.6", never as "the destroyed-structure
arm".

### B.1 Verified facts (draft §2): criterion (iii)

| # | verdict | file and key |
|---|---|---|
| 1 | matches | `first_rule_k12/RESULT.md` line 27 |
| 2 | matches | `result.json` `exam.P2.insample_rule.existence` = 0.25474, `exam.P2.insample_n1.existence` = 0.33535 (the draft's key path omits the `exam.` prefix) |
| 3, 3b | matches. Recomputed all ten fold margins (N1 − rule) from `exam.per_fold_N1` and `exam.per_fold_rule`: +0.04272, +0.02030, −0.00431, −0.02425, −0.04085, +0.01034, −0.04701, +0.04796, −0.05727, +0.00727; mean −0.004511 = `exam.P3.existence.real_margin` |
| 4 | matches: `harness_controls.json` `controls[...].P4.bf.margin` for real/N0 (r = 1), real/N1 (r = 3), real/PR (r = 4), real/RP_r8 (r = 8), real/oracle (r = 16) |
| 5 | matches, and the discrepancy note is correct (`result.json` `exam.P4.bf.margin` = 0.0485130; `controls["real/oracle"].P4.bf.margin` = 0.0485136). Small correction: "ranks that occurred: 1, 3, 4, 8 and 16" is a sentence in `HARNESS-CONTROLS.md` line 148, not a key of `harness_controls.json` |
| 6 | matches: `harness_controls.json` `BF_8_real_bank_by_starts` |
| 7 | matches: `result.json` `exam.did_not_run.folds_where_N0_beats_rule.counts` = 10 |
| 8 | matches: `result.json` `exam.P3.sign` |
| 9 | matches: `result.json` `exam.P3.offset`; `P3_p_values.offset.p_one_sided` = 0.98 |
| 10 | matches: `HARNESS-CONTROLS.md` lines 177–179 |
| Johnny's −0.0643 | the file value −0.0643 is the **existence** shuffled mean (`exam.P3.existence.shuffled_mean` = −0.064306); offset's is +0.042538. Johnny's message itself was not read (the chat is out of bounds) |

### B.2 Each prediction against (i)–(iv)

(i) the falsifier differs from the confirming outcome, and no outcome both confirms and refutes;
(ii) the two readings being compared predict different outcomes; (iii) cited numbers match the
files; (iv) a run exists that measures it.

| id | (i) | (ii) | (iii) | (iv) | verdict |
|---|---|---|---|---|---|
| **P-J1** | The confirming outcome ("again fails to separate held-out existence") and the falsifier (random ≈ learned within 0.01) are not complements: both can happen together. "Separate" is undefined (from N1 in P1, or from the shuffles in P3?). "≥ ~most folds" is not a number. The draft's own note is right: P-J1's falsifier is P-J3a's confirmation. | **Fails.** Random-label ≈ learned is what *both* readings predict: under "form defect" the form cannot use the labels, under "overfit" the learned labels are fitted noise. The outcome cannot choose between them. The test that would separate them is an ablation of the degree term (same family with and without an N1-logit offset), which no draft item registers. | "±0.01" has no file source (a chosen bound is fine, but say so). | **Fails.** "§4.3" names the spec's shuffled-bank arm, which has no random-label margin (B.0). And if rule #2 is "BF_r + X", it contains N1's logit, i.e. a degree term, so "a rule of the same family still without a degree term" will not be run unless registered as an ablation. | **fails (i), (ii), (iv)** |
| **P-J2** | Distinct outcomes, with a gap: 3–6 losses "with terms" neither confirms nor refutes. Acceptable if stated. | **Fails as written.** N1 already *has* node-level counts terms: m_o + α_s + β_t (spec A4). A rule that adds exactly those ties N1: 0 wins, 0 losses, which is neither the confirming "≥ 8/10 wins" nor the falsifier. Worse, the counts score depends on the **offset set**: a missing offset counts as predicted 0 (spec §4.1, A3). N_EB has N1's counts model and scores 0.9076 against N1's 0.9861 (`harness_controls.json` `nulls_real_bank.*.counts`), a 0.0785 difference produced by offset sets alone, larger than the first rule's −0.0677. So a counts change cannot be attributed to counts terms unless the offset field is held fixed. | no numbers cited | rule #2's P1 counts: measurable | **fails (ii)** |
| **P-J3a** `[informed]` | Distinct, with a gap (0.02–0.03 undetermined); the quantity is a mean while the falsifier is per-fold ("≥ 7/10 folds"). | Separable in principle (capacity → equal; structure → learned better), but P-A4's resolution caveat applies directly: a 0.02 band against a resolution of about 0.02. | thresholds only | **Fails**: arm not identifiable from the exam files (B.0). | **fails (iv)**; (ii) weak |
| **P-J3b** `[informed]` | **Fails.** The claim is "will not flip the sign", but the band [−0.02, +0.01] includes positive margins up to +0.01: a flip to +0.005 confirms the quantity and refutes the claim. | **Fails for rule #2.** The band is a *level*, not a *change*. A "BF_r + X" rule sits near BF_r's +0.040 to +0.049, so it lands above +0.02 at every k and "refutes" the prediction whether or not k has any effect. The band was fitted to the first rule's −0.0045, not to rule #2. | "k = 8/16" matches no registered starts value (10 or 3); see B.0 | "§2.6" not identifiable | **fails (i), (ii), (iv)** |
| **P-J4** | **Fails.** The claim is "cannot clear the threshold", but P4 is the **mean over folds**, strictly above the threshold (spec A11, A19). The falsifier is "≥ +0.05 in ≥ 8/10 folds". A mean of +0.049 passes P4 without triggering the falsifier, so a P4 pass would not refute a claim about P4. Per-fold margins spread by about ±0.05 (first rule: −0.057 to +0.048), so "≥ 0.05 in 8/10 folds" is almost unreachable for any rule. The second half ("if it passes anywhere, it is offset or counts") has no quantity and no falsifier. | The band [0.0, +0.03] is **below BF_r's own margin** (+0.040 at r = 3, +0.0485 at r = 12). For a rule that contains BF_r, landing there means X *damages* BF by ≥ 0.018; the band does not follow from the claim. | +0.0485 matches `result.json` `exam.P4.threshold` (r = 12). It is rule #2's threshold only if rule #2 declares r = 12; at r = 8 it is +0.0493. | P4 record: measurable (`P4.rule_margin_existence`, `P4.bf.margin`) | **fails (i)**; band inconsistent |
| **P-A1** | Mixed: "0/10 folds" and "gain < 0.005" are two quantities; the falsifier covers only the gain, with a gap at 0.005–0.01. The rule beating BF in 3/10 folds with gain < 0.01 is neither. | Weak: a "different residual" that is small or noisy also gives a gain < 0.005. "Same residual" is better tested directly, e.g. by the correlation of the rule's residual logit with BF's on held-out cells. | none cited | **Fails as written.** The record keeps only BF's mean margin, λ per fold and `folds_beating_N1` (`result.json` `exam.P4.bf`); there are no per-fold BF scores, so "rule beats BF_r in 0/10 folds" cannot be read off a run. "BF_r + rule's prediction" is not a harness predictor. The claim is about the *first* rule's residual but is measured on rule #2. | **fails (iv)**; (i), (ii) weak |
| **P-A2** | Gap 0.01–0.02; "moves by < 0.01" is unsigned while the falsifier is signed (+0.02). | Depends on where the rule starts: BF's own rank doubling 4 → 8 moved +0.0096 (`controls["real/PR"]` vs `controls["real/RP_r8 as a rule (seed 999)"]`), right at the 0.01 line, while 8 → 16 moved −0.0008. So below r ≈ 8 even the "capacity is not the problem" reading predicts about 0.01; above it, both readings predict about 0. The test separates only if the sweep brackets r ≈ 8. | none cited | "complexity sweep" is not a harness arm; it must be registered as a run | **fails (iv)**; (ii) conditional |
| **P-A3** | **Fails.** Claim: "per-source counts terms fix the counts arm". The quantity allows a margin of −0.02, but P1's counts arm needs the fold mean **not worse** than N1 (spec A8), i.e. margin ≥ 0. So a margin of −0.01 confirms the quantity while the counts arm still fails. A mean margin in [−0.02, 0) together with ≥ 8/10 wins is also hard to reach. | **Fails**, for P-J2's reasons: N1 already carries per-source (and per-target) counts terms, so adopting them ties N1; and the counts score moves with the offset field. | −0.0677 matches `result.json` `exam.P3.counts.real_margin` = −0.067719 | P1 counts: measurable | **fails (i), (ii)** |
| **P-A4** | Correctly recorded as a caveat without a falsifier. | — | "≈ 0.02" is not sourced. From the files: the first rule's P3 existence shuffled max − mean = 0.0208 (`exam.P3.existence`); the ten per-fold margins have SD ≈ 0.037, so the SE of a 10-fold mean ≈ 0.012. P4 compares two deterministic fits on the same folds, so a **paired** SE would be smaller; the harness does not record per-fold BF scores to compute it. | — | caveat, correctly not a prediction |
| **P-A5** | **Fails.** The claim is directional ("random will be worse than learned"), the quantity is unsigned (\|Δ\| ∈ [0.005, 0.04]): random *better* by 0.02 confirms the quantity and refutes the claim. Mean and per-fold are mixed again. | The lower edge 0.005 sits below the resolution Ark gives in P-A4 (≈ 0.02), so "within 0.005" and "0.005–0.02" cannot be told apart by this arm. | thresholds only | arm not identifiable (B.0) | **fails (i), (iv)**; (ii) below resolution |
| **P-A6** | **Fails.** "The arm will be empty at the starts axis" is a claim about *change*; the band [−0.02, +0.01] is a *level*. A swing from −0.02 to +0.01 (0.03, far from empty) confirms it. | **Fails for rule #2**, as P-J3b: a BF-based rule sits at about +0.045 and triggers "≥ +0.02 at any k" regardless of starts. | The note's numbers match: 0.049331 − 0.049268 = +0.000063 (`BF_8_real_bank_by_starts`; `HARNESS-CONTROLS.md` line 87); 0.04933 / 0.02815 = 1.75 | "§2.6" not identifiable | **fails (i), (ii), (iv)** |
| **P-A7** | **Fails**, same defect as P-J4: P4 is mean > threshold; the falsifier is "≥ +0.0500 in ≥ 8/10 folds". A mean of +0.0490 at r = 12 passes P4 and is inside neither the band nor the falsifier. The band [0.030, 0.048] also leaves 0.048–0.0485 unassigned. | Separable (a pass vs a fail of P4), once the falsifier is restated as "P4 passes". | +0.0485 matches `exam.P4.threshold` for r = 12 only | P4 record: measurable | **fails (i)** |
| **P-A8** | "Pass pattern on counts" is undefined: P3 does not decide on counts, so it can only mean P1's counts arm. The falsifier covers "passes existence while counts failed" but not "passes offset while counts failed", although the claim excludes offset too. | **Fails.** P1's counts arm is non-inferiority, and a tie is not a loss (A7). A rule that copies N1's counts ties N1 in every fold and "passes" counts, exactly as the first rule "passed" sign (0 losses, all ties, `exam.P1.sign`). So "passes on counts" does not separate "structure in counts" from "copied N1". | none cited | P1: measurable | **fails (ii)**; (i) incomplete |

**Items that pass all four:** none as written. The closest are P-J2 (fails only (ii)), P-A7
(fails only (i); restating the falsifier as "P4 passes" fixes it) and P-J4 (the same fix, plus
moving the band).

### B.3 Draft §4 constraints and §5 record defects

- **§4(a).** The numbers match (acceptance line 115, M4; ranks as in B.1 #4). **The
  by-construction statement is wrong as written.** "If everything beyond degree in the bank is
  low-rank, then no rule can clear P4" is contradicted in the allowed files: on PL1, whose planted
  structure is a 4 × 4 class-block pattern (rank ≤ 4), PR cleared BF_4, +0.133 against +0.074
  (`harness_controls.json` `controls["PL1/PR"].P4`). Low rank is not enough. What makes P4
  unreachable is that **BF_r is already the best held-out estimator of the residual that any rule
  can build from the training cells and the admissible fields**. A rule with a sharper prior
  (discrete classes instead of a penalised continuous factorisation) can beat BF on low-rank
  structure with finite data. PR had the true classes for free, so PL1 does not show that a
  *learned* rule can do it, but it does show that rank alone does not close P4. **The same
  correction applies to Part A's A.3**, which says that if the residual is rank-≤ r bilinear then
  "penalised BF_r … already extracts it". Part A is left as written; this is the reader's
  correction of it.
- **§4(b).** See P-A4: 0.02 is roughly what the files give for an unpaired spread; the paired
  resolution for P4 is not recorded.
- **§4(c).** The starts numbers are right. Whether §2.6 varies starts or the rule's own k cannot be
  checked from the allowed files (B.0).
- **§4(d).** Out of scope for a blind reader: it rests on a proposal quote.
- **§4(e).** Matches `RESULT.md` lines 73–84.
- **§5, defects 1, 4 and 5** hold against `result.json` (`exam.P1.existence.wins` vs
  `exam.P1.offset.wins_vs` / `wins`; the verdict line; `exam.P4.bf.lambdas` only). **Defect 2** is
  registered behaviour (A7: a tie is not a loss under non-inferiority), so it is a reporting gap,
  not a record error. **Defect 3** is weaker than stated: verdict labels are shared strings by
  design (spec §5.2); the real collision, "did not run" vs a crashed run, is already handled in
  `GLOSSARY.md`. Three objects carrying one label is what a label is for.

### B.4 The draft against Part A

| point | Part A | draft | agree? | what settles it |
|---|---|---|---|---|
| Starts as a knob | A2-k: \|Δmargin(k = 10 vs 3)\| < 0.001 | P-A6 note and §4(c): starts barely move BF (+0.00006) | **agree** on the fact; disagree on the test: the draft's bands (P-J3b, P-A6) measure a level, not a change | rule #2 run at k = 3 and k = 10: \|Δ\| of `P4.rule_margin_existence` and `P4.bf.margin` |
| Rank as a knob | A2-r: BF_r margin in [+0.045, +0.052] for r ≥ 8; plateau | §4(c): rank moves it 1.75× (r = 1 → 8) | **agree**; Part A adds that rank does not help against P4 because the threshold moves with it | BF_r margin at rule #2's declared r |
| Rule #2's existence margin level | A1-E: ≥ +0.040 (a BF-based rule inherits BF's margin) | P-J4: [0.0, +0.03]; P-A7: [+0.030, +0.048] | **disagree** with P-J4 clearly, partly with P-A7 | rule #2's `P4.rule_margin_existence`: ≥ 0.040 favours Part A; < 0.030 favours P-J4 |
| P4 outcome | A3-P4: fails; rule − BF_r < +0.005 | P-J4, P-A7: will not clear | **agree** on the outcome | P4 verdict, and rule − BF margin |
| P1 existence | A3-P1: passes (≥ 9/10 folds vs N1), as BF_8 and BF_12 beat N1 in 10/10 | P-J4, P-A8: "if it passes anywhere, not existence" | **disagree**, unless the draft means P4 by "existence" | rule #2's `P1.existence.wins` |
| The exam's destroyed-structure arm (P3) | A1-E: existence passes, gap ≥ 0.015; A1-O: offset fails unless the offset field beats N_EB (≈ 0.484 Jaccard) | no prediction (the draft's "§4.3" is a different arm) | **no overlap** | rule #2's `P3.existence` and `P3.offset` |
| Where a pass could come from | offset only by beating N_EB; counts can "pass" P1 by tying N1, which shows nothing | Ark: counts; Johnny: offset or counts | **disagree** with P-A8's reading of a counts pass | P1 counts wins *and* losses (not only the pass flag), with the offset field held fixed |
| When P4 is unreachable | A.3 as corrected in B.3: when BF_r is already the best held-out estimator from training cells, not merely when the residual is low-rank | §4(a): "if everything beyond degree is low-rank" | **disagree**; PL1 (PR +0.133 vs BF_4 +0.074) shows low rank alone is not enough | settled in the files for a rule given its classes; for a learned rule, only a rule that beats BF_r would show it |

### B.5 What the draft needs before commit

1. Rename the random-label arm and the §2.6 arm, and say which k (by glossary sense) §2.6 varies.
2. Restate every P4 falsifier as "P4 passes" (mean over folds, strict, against the threshold at
   rule #2's declared r), not as "≥ 0.05 in ≥ 8/10 folds" (P-J4, P-A7).
3. Replace the level bands of P-J3b and P-A6 with a change: \|margin(k₁) − margin(k₂)\| < ε.
4. Make directional claims directional in their quantities (P-A5, P-J3b).
5. For counts (P-J2, P-A3, P-A8): note that N1 already has node-level counts terms, that a tie
   "passes" P1 counts, and that the counts score moves with the offset field. Hold the offset
   field fixed, or report the Jaccard next to the counts margin.
6. Resolve P-J1 vs P-J3a. If P-J1 is kept, register a degree-term ablation as its test.
7. Add per-fold BF scores to the record if P-A1 or a paired resolution is wanted.
8. Correct §4(a)'s by-construction sentence (B.3).

### B.6 Files opened in this whole task

- `GLOSSARY.md`
- `docs/plans/2026-09-23-c6-control-specification.md`
- `docs/plans/2026-09-23-c6-amendment-acceptance.md`, `-2.md`, `-3.md`
- `results/genome/c6/HARNESS-CONTROLS.md`
- `results/genome/c6/harness_controls.json` (read with Python: keys and selected values)
- `results/genome/c6/rule_runs/first_rule_k12/RESULT.md`
- `results/genome/c6/rule_runs/first_rule_k12/result.json` (read with Python)
- `results/genome/c6/checks/n1_alone/RESULT.md`, `summary.json`
- `docs/plans/2026-09-23-first-rule-failure-predictions.md`, in Part B only, after Part A was saved
- this report (written)

Also a `wc -l` over the allowed files, and an `ls` of this report's path before it existed.
Nothing under `results/genome/c6/rules/` or `results/genome/c6/rule_runs/first_rule/`, neither of
the two forbidden plans, nothing under `C:/Users/mikha/.dpc/`, and none of their git history was
opened, listed or searched.

---

## Part C: review of DRAFT v2

**Written:** 2026-09-23 10:32 UTC (17:32 local, +07:00), by the same blind reader. Parts A and B
above are not edited. Reviewed file: `docs/plans/2026-09-23-first-rule-failure-predictions.md`,
DRAFT v2. Newly allowed this round: `results/genome/c6/harness.py`.

**Blindness note for this round.** DRAFT v2 itself now carries some rule-side content, and by
reading it I have seen that content:
- §4(c): "§2.6 is about the rule's own `k`, the dimension parameter … that is also its declared
  rank r = 12 … checked by CC against the proposal";
- §6: Zcode's summary of which of the proposal's §4 risks fired, and that existence "had been
  predicted to pass".

None of this is used below. §4(c) and §6 should carry the `[informed by proposal]` tag that v1
used, because blind reviewers read this file. `git status` printed the *path* of the new forbidden
file `docs/plans/2026-09-23-first-rule-failure-rule-side.md` (untracked); it was not opened.

### C.0 What `harness.py` shows (item 2 of the task, checked first because rows below use it)

| check | result | lines |
|---|---|---|
| `exam.dial` computed on every exam run | **Yes.** `run_exam` loops over `env.dial` unconditionally. `make_env` always builds the 25 dial banks, and the rule path's `precompute` always schedules their fits. The spec lets a rule drop the dial if it is expensive (§6, A13), but the code has no path for that. | 1030–1044; 1229; 1573, 1587 |
| `exam.loto` computed on every exam run | **Yes**, unconditionally: `lo = loto(pred, bank)`. | 1045; 983–987; 1586 |
| dial and loto enter no verdict label | **Yes.** `labels` is built only from `dnr`, `r1`, `r2`, `r3`, `r4`, and `verdict` only from `labels`. `dial_out` and `lo` are only written into the returned dict. | 1046–1059, 1066–1069 |
| A5's dial criterion applied only to PL1/PR | **Yes.** `dial_ratio` is defined inside `controls()` and called once, on `out["PL1/PR"]`. `rule_run` never calls it. | 1324–1329, 1367–1370; `A5_MAX_RATIO = 0.25` at 543 |
| `dial_ratio` with a margin ≤ 0 at f = 0 | returns **`inf`**, not m(1)/m(0) | 1327 |
| the dial at f = 0 | five copies of the real bank (seeds are not used), so its mean *is* the real held-out margin | 924–930 |
| the dial at f = 1 and P3's shuffles | the same function, `rewire_and_permute(base, rng, 1.0)`; seeds `PCG64(10400 + sd)` for the dial and `PCG64(seed)`, 0–98, for P3 | 871–901, 907–909, 924–933 |
| BF on a held-out type (loto) | when a type's whole row and column are held out, its row of the SVD residual is 0, so U₀ = 0 for it. Newton then has only the penalty gradient λU, which sends every start to 0. **BF's term is exactly 0 on every cell of the held-out type**, and N1's effect for that type is penalised to 0 as well. So on loto cells, **BF_r = N1** | 666–695, 647–657, 350–360 |

Re-checked from `result.json` (`exam.loto`, `exam.dial`): v2's rows 11–19 match. The five f = 1
existence margins are −0.0628, −0.0685, −0.0515, −0.0602, −0.0653 (SD ≈ 0.0066, so the SE of the
5-seed mean is ≈ 0.003).

**Are P-A1 and P-A2 predictions about the verdict?** No. Both are **record-only**: `exam.dial` and
`exam.loto` feed no label, and A5 is not applied to rules. That is acceptable in a registration,
on three conditions:
- (a) it says so in plain words;
- (b) it does not present them as tests of whether rule #2 passes;
- (c) any constant borrowed from elsewhere is registered anew here. P-A1's 0.25 is acceptance
  A5's constant, registered for PR on PL1, not for a candidate rule on the real bank.

Making either one a pass condition would contradict the spec (§4.4, §4.5, §5.3, A12: the dial and
leave-one-type-out are "descriptive" and do "not enter the decision"). It would need an appended,
monotone spec amendment, not a line in this file.

### C.1 Each v2 prediction against (i)–(iv)

| id | (i) refuting outcome possible and distinct | (ii) readings predict different outcomes | (iii) numbers vs files | (iv) run / field | verdict |
|---|---|---|---|---|---|
| **P-J1** (margin ≥ +0.040) | yes: < +0.030 refutes; [0.030, 0.040) is left undetermined, and says so | "the addition keeps BF's margin" vs "the addition damages it": different values | BF_3 +0.04034 = `harness_controls.json` `controls["real/N1 as a rule"].P4.bf.margin`; BF_12 +0.04851 = `result.json` `exam.P4.bf.margin` | `P4.rule_margin_existence` | **passes** |
| **P-J2** (degree ablation, Δ ≥ +0.025) | yes (< +0.010) | **Weak.** It measures whether the N1 term matters *for rule #2's family*; the readings ("form defect" vs "overfit") are about the *first* rule. A rank-r bilinear term can represent a_s + b_t in two of its dimensions, so dropping the N1 logit mostly costs rank and penalty, and neither reading gives a clear size for that. The ablated variant is undefined: is the intercept kept? is λ re-chosen? | 0.025 and 0.010 are the author's own constants, declared | two new runs; they must be registered, and it must be said that only the full rule's verdict counts | **passes (i), (iii); (ii) weak; (iv) conditional on registering the ablated variant exactly** |
| **P-J3** (fails P4; Δ < 0; expected [BF − 0.005, BF + 0.005]) | **Fails.** The quantity "Δ < 0" and the stated expected range [BF − 0.005, BF + 0.005] contradict each other: Δ = +0.003 is inside the expected range, violates "< 0", and is a P4 pass, which is the refuting outcome. And a tie (Δ = 0, the addition penalised to zero) fails P4, confirming the claim, while violating "< 0". | Readings differ once fixed | +0.0493 (r = 8) = `harness_controls.json` `BF_8_real_bank.margin`; +0.0485 (r = 12) = `exam.P4.threshold` | P4 record | **fails (i)**. Fix: Δ ≤ 0, expected range [BF − 0.005, BF] |
| **P-J4** (P3 offset; bar Jaccard ≥ 0.4831) | yes: a P3 offset pass at Jaccard ≤ 0.4842 | Only the non-trivial branch is a prediction; "no offset change → tie → fail" is by definition | 0.42040 = `summary.json` `fields.offset.real`; 0.06267 = `result.json` `exam.P3.offset.shuffled_max`; 0.48417 = `harness_controls.json` `nulls_real_bank.N_EB.offset`; 0.4204 + 0.0627 = 0.4831 correct. **Caveat:** 0.06267 is the first rule's (and N0-as-a-rule's) shuffled max. Rule #2's will be its own, so the bar is an estimate. Part A's A1-O has the same weakness. | `P3.offset` | **passes (i), (iii), (iv)**. The condition does not need Zcode: write both branches, since rule #2's registration will state whether the addition touches offset sets |
| **P-J5** (counts margin ∈ [−0.01, +0.005]) | **Incomplete.** A margin below −0.01 (the first rule's was −0.068) is neither confirming nor refuting, and is not listed as undetermined, although it contradicts "a tie" | **Fails.** The counts score moves with the offset field (a missing offset scores as 0, spec A3). If rule #2's offset field is not N1's, the counts margin shifts with no change to the counts model: N_EB has N1's counts model and a counts margin of +0.0785 over N1 (`harness_controls.json` `nulls_real_bank.N1.counts` 0.98614 − `N_EB.counts` 0.90761). That "refutes" P-J5 (> +0.015) for a reason that has nothing to do with counts. The accompanying requirement (§4b item 4) helps only if the refuting outcome is *conditioned* on it. | none cited. The CC note's "v1 §2 discrepancy on row 5 lineage" is a wrong citation: 0.0785 comes from this report's B.2 (P-J2 row) | P1 counts / `P3.counts.real_margin` | **fails (ii); (i) incomplete**. Fix: state it for the offset field equal to N1's, or refute on the counts margin *minus* the N_EB-style offset effect, and make < −0.01 a refuting outcome too |
| **P-A1** (dial: m(1) ∈ [−0.02, +0.02] and m(1)/m(0) ≤ 0.25, given m(0) ≥ 0.040) | Mostly yes. The bands touch at +0.020 (confirming ≤ +0.020, refuting (b) ≥ +0.020); make one strict. If m(0) < 0.040 the item says nothing, which is fine but should be stated as "no prediction" | yes: structure → small m(1); ambient → m(1) ≥ +0.02; the first rule's pattern → m(1) ≤ −0.03 | 13.67 = −0.06167 / −0.00451 is correct arithmetic, but the harness's `dial_ratio` returns **inf** when m(0) ≤ 0 (line 1327), and a ratio of two negatives has no reading under A5. "Failed by an order of magnitude" is not a statement A5 supports. | `exam.dial`: **computable from the existing record, no harness change needed** | **passes (ii), (iv); (i) fix the boundary; (iii) drop "13.67 / order of magnitude"; record-only (C.0)** |
| **P-A2** (loto existence ratio ≥ 1.5) | the refuting outcome (< 1.15) is possible | **Fails.** On loto cells, BF_r reduces **exactly** to N1 (C.0, last row). So for "N1 logit + BF term + X", the ratio is 1.000 plus whatever X does on a type it has never seen. The outcome is set by the rule's form (whether X is zero for unseen types, or uses stride/role/layout), not by anything about the bank. The first rule's 1.95 = 0.75260 / 0.38582 (`exam.loto.existence`, correct) shows only that that rule was overconfident on unseen types. **This reader's prediction is the opposite: ratio ≈ 1.00 for a BF-based rule whose addition vanishes on unseen types.** | 1.95 correct | `exam.loto` (record-only) | **fails (ii)** |
| **P-A3** (fails P4; Δ < +0.005 and margin ≥ +0.040) | yes: a P4 pass; claim and quantity have separate refuting outcomes, stated | yes ("BF_r is the best estimator" vs "X adds held-out information") | +0.04933 / +0.04851 correct (as P-J3) | P4 record | **passes** (same content as P-B5) |
| **P-A4** (offset advantage is ambient: three witnesses) | The refuting text names only witness 1 and then says "any one of the three failing refutes". Pick one. Witness 2's "f = 0 ≈ +0.025" is not a number: it is the first rule's value, copied. | Differ in principle (structural: in-sample > 0, m_off(1) < m_off(0), loto > N1). But the item **presupposes** that rule #2 *has* an offset advantage. If rule #2's offset field is N1's, every witness is 0 by construction and witness 2 (≥ +0.030) "refutes" it trivially. Conditional, like P-J4. **Unstated consequence:** witness 1 (in-sample offset margin ≤ 0) means P2 fails on offset (`P2.beats.n1_insample.offset` = false), so P-A4 *is* a verdict prediction ("below threshold for this family"); say so. | −0.05926 = `exam.P2.insample_rule.offset` − `insample_n1.offset`; +0.03872 / +0.02446 = `exam.dial` offset means; 0.45210 / 0.45641 = `exam.loto.offset`; all correct | `P2`, `dial`, `loto` | **fails (i) as written; (ii) conditional** |
| **P-A5** (R² ≥ 0.70 of the rule's residual logit on BF's) | yes (< 0.40) | **Weak to failing.** If rule #2 contains BF's term, (rule − N1) = BF-term + X, so R² is high by construction and measures only the size of X relative to the BF term. It says nothing about "the same residual" as a fact about the bank. It separates readings only if the rule's bilinear part is fitted independently of the harness's BF_r. | none | **needs per-cell held-out logits**, not per-fold means; "logit" must be defined before clipping (scores clip to [0.001, 0.999]). This is a harness change (C.4) | **(ii) weak; (iv) needs a harness change and a re-run of the controls** |
| **P-B1** (P3 existence passes; gap ≥ 0.015) | yes, two refuting outcomes | yes | ≥ 0.040 from the BF profile; 0.025 is a declared guess. New support: the first rule's dial at f = 1 averages −0.0617, the same process as P3 | `P3.existence` | **passes** |
| **P-B2** (P3 offset fails unless Jaccard > 0.4842) | yes; one-sided: above 0.4842 it predicts nothing, and should say so | the non-trivial branch only, as P-J4 | same caveat as P-J4: the 0.06267 bar is the first rule's shuffled max | `P3.offset` | **passes, with P-J4's caveat** |
| **P-B3** (starts: \|Δ(10 vs 3)\| < 0.001) | yes | "search-limited" vs not; the prior strongly favours "no change", which is still a prediction | BF_8 k = 3 vs 10: 0.049280 vs 0.049331 (`BF_8_real_bank_by_starts`) | **a second full exam run at k = 3**; the timing cap fixes k per run (acceptance part 3 (c)), so it must be registered as descriptive, with only the k = 10 run's verdict counting | **passes, (iv) conditional on registering the second run** |
| **P-B4** (BF_r ∈ [0.045, 0.052] for r in 8…64) | The claim covers every r in 8…64, but the refuting outcome checks only the declared r, and nothing at all if r < 8 | "saturation" vs growth: yes | correct | `P4.bf.margin` of rule #2. The `harness_controls.json` rank profile is past data, not a measurement of this prediction | **passes if narrowed to "at rule #2's declared r, if r ≥ 8"**; its "rank does not help against P4" half is a fact of the code, not a prediction |
| **P-B5** (fails P4; Δ < +0.005; < +0.054 at r = 12) | yes, separate refuting outcomes | yes, **with the B.3 correction** (P4 is unreachable only if BF_r is already the best estimator available from training cells) | correct | P4 record | **passes**; "< +0.054" applies only if r = 12 |
| **P-B6** (P1 existence ≥ 9/10) | yes (≤ 8/10) | "BF-based rule keeps BF's fold wins" vs "X damages them" | BF_8 10/10 = `harness_controls.json` `BF_8_real_bank.folds_beating_N1`; BF_12 10/10 = `result.json` `exam.P4.bf.folds_beating_N1` | `P1.existence.wins` | **passes**; drop "at most a small addition" (undefined) or define it |

**Summary.**
- **Pass all four:** P-J1, P-A3, P-B1, P-B5, P-B6.
- **Pass with a stated narrowing or condition:** P-J4, P-B2, P-B3, P-B4, and P-A1 (record-only).
- **Fail:** P-J3 (i), P-J5 (ii), P-A2 (ii), P-A4 (i), and P-J2 / P-A5 on (ii), weakly.

### C.2 §3b: agreements and disagreements

| §3b row | separating outcome named? | can it occur? | comment |
|---|---|---|---|
| existence level ≥ +0.040 | yes | yes | no disagreement, so nothing to separate |
| P4 width | named: a margin in [BF_r, BF_r + 0.005) | yes, but **mis-described** | Any margin strictly above BF_r is a **P4 pass**, which refutes the *claims* of P-J3, P-A3 *and* P-B5; only their quantities differ there. The outcome that separates P-J3 from P-A3/P-B5 *within* a P4 fail is **Δ = 0 exactly** (a tie, when X is penalised to zero). That can occur, and under the current "< 0" it refutes P-J3 alone. After the P-J3 fix (Δ ≤ 0), P-J3 and P-A3/P-B5 differ only on Δ ∈ (0, 0.005), where all three claims are refuted anyway, so the "disagreement" disappears. |
| P3 offset | yes (the Jaccard value) | yes | agreed bar; the condition is settled by rule #2's own registration, not by Zcode |
| counts / offset attribution | named | yes | there is no counterparty in v2, so this is not a disagreement |
| rank / starts | "the same sweep, varying rank and starts separately" | yes | **Error:** it cites "P-A2 (rule #2 complexity sweep, \|Δ\| < 0.01)". That is **v1** P-A2 (superseded, §7). v2 P-A2 is the loto item. So there is no v2 Ark item on this axis. Also, P-B3 is about starts only, and P-B4 is about the *opponent's* rank profile, not the rule's own dimension parameter. |
| P1 existence | yes | yes | no v2 disagreement left, as the row says |
| form defect vs content-fit | **no** | — | The CC note is right that it is not a table row. And its premise is wrong: under the destroyed-structure arm, degree is **preserved** (A10), so a pure "missing degree term" defect would hurt the rule equally on real and shuffled banks: the margin **would not change**. It would not "shrink". The observed deepening (−0.0045 → −0.0617) *is* the recorded P3 existence pass: the rule does relatively better on the real bank. Whether to call that "structure" or "content-fit" is a naming question these numbers cannot settle. To become a disagreement, each author must name a rule #2 outcome; for example, P-J2's ablation Δ vs P-A1's m(1). |

### C.3 §4b: registration requirements

| # | changes | conflicts with spec or acceptance? | comment |
|---|---|---|---|
| 1 ablation run | the **record** (a second run) | no, if it is stated that only the full rule's verdict counts. Submitting two variants and keeping the better one would be a multiplicity the spec does not allow for | define the ablated variant exactly (intercept, λ grid, starts); cost doubles (A13: 1,315 fits each) |
| 2 per-fold logits | the **record**, via a harness change | No direct conflict, but A20 requires the planted suite to be re-run "after every change to the exam", and every output is stamped with the harness sha256 (acceptance (c)). So: re-run `--controls` and show every verdict unchanged | must be **per-cell** held-out logits, defined before clipping, for P-A5's R² |
| 3 per-type loto | the **record**, via a harness change | same as 2 | useful, but see P-A2: for a BF-based rule the per-type values show only where X departs from N1 |
| 4 offset Jaccard next to counts | **neither**: already satisfied. `per_fold_rule` carries offset and counts per fold, and `RESULT.md`'s P1 table prints both | no | "offset held fixed" is a *different predictor*, i.e. another variant run like item 1, and must be registered as one |
| 5 `dial_ratio` for rule #2 | the **record** only; computable from the existing `exam.dial`, no harness change needed | **as a pass condition, yes**: it contradicts spec §4.4/§5.3 and A12 ("does not enter the decision") | say explicitly: descriptive. Note `dial_ratio` = inf for m(0) ≤ 0 |
| 6 spread-log assert | **neither**, if placed after the record is written; if it aborts before writing, it turns a finished exam into a crashed run with no record | no. If it goes in the harness, see item 2 (a harness change) | specify: record written first, then the assert; and whether a failure voids the verdict |
| 7 k-sensitivity "on the rule's own dimension parameter (P-B3/P-B4)" | the **record** (extra runs) | no | **Mislabelled.** P-B3 is *starts*; P-B4 is *BF's* rank. Split it: (a) starts, k = 3 vs 10 (P-B3); (b) the rule's own dimension parameter, if wanted. Changing (b) also changes the declared r, and so BF_r's threshold, so report the rule margin, the BF margin and their difference at each value |

**Missing requirements** (every prediction above depends on them):
- rule #2 must declare **r** before the run (A11); r = 8 and r = 12 give different thresholds;
- it must fix the **timing cap** (acceptance part 3 (c));
- it must state **whether the addition touches offset sets, counts or sign**, which resolves P-J4 and conditions P-A4 and P-J5.

### C.4 CC-draft notes

| note | agree? |
|---|---|
| §2, "two implementations, one number" | **Agree.** One function, `rewire_and_permute(…, 1.0)` (lines 907–909 and 924–933). The 0.0026 gap is about 1 SE of the 5-seed mean (per-seed SD 0.0066). |
| §2 row 24 (BF_3 vs BF_12 from different files) | agree |
| P-J1: converges with A1-E | agree |
| P-J2: threshold author-chosen | agree; add the (ii) weakness and the undefined ablation |
| P-J3: "a margin in [BF, BF + 0.005] refutes Johnny but not the blind reader" | **Disagree.** That margin is a P4 pass and refutes P-B5's claim too; only P-B5's quantity survives. And P-J3's own expected range includes it (C.1). |
| P-J4: explicitly conditional | agree; resolve it by branches, not by waiting for Zcode |
| P-J5: implements B.5.5 | **Partly.** Wrong citation (see C.1), and the refuting outcome is still not conditioned on the offset field. |
| P-A1: record-only | **Agree** (C.0); add that no harness change is needed and that 0.25 is borrowed from A5 |
| P-A3: converges with P-J3 | agree |
| P-A4: numbers verified | agree on the numbers; the logic defects are in C.1 |
| P-B1, P-B2, P-B3 notes | agree; P-B3 needs its second run registered |
| P-B5: B.3 correction carried | agree; it is carried accurately |
| P-B6: disagrees with superseded framing | agree |
| §3b last row: live, unturned disagreement | agree that it is not a row; disagree with its premise (C.2) |

### C.5 Is v2 ready to commit as a registration?

**No.** The minimum changes, most important first:

1. **Fix P-J3's internal contradiction**: Δ ≤ 0, expected range [BF − 0.005, BF]. Then correct
   §3b's P4 row and the P-J3 CC note, since a margin above BF is a P4 pass for everyone.
2. **Add the missing requirements**: rule #2's declared r, its timing cap, and which fields the
   addition touches. Without r, the cited thresholds (0.0485 / 0.0493) are not fixed. Without the
   field list, P-J4, P-A4 and P-J5 are undefined.
3. **Rework or drop P-A2**: BF reduces exactly to N1 on leave-one-type-out cells
   (`harness.py` 666–695), so the ratio is set by the rule's form, not the bank. And mark P-A1 and
   P-A2 as record-only, not verdict predictions.
4. **Condition P-J5 on the offset field** (or hold it fixed), and make a margin below −0.01 a
   refuting outcome.
5. **P-A4**: one refuting rule, not two; a number instead of "≈ +0.025"; a branch for "offset
   field = N1's"; and a statement that witness 1 implies a P2 fail.
6. **§4b**: split item 7 (starts vs the rule's own parameter); note that item 4 is already
   satisfied; state that items 1, 7 and P-B3's k = 3 run are descriptive and that only the
   registered run's verdict counts; items 2 and 3 are harness changes and need a `--controls`
   re-run (A20).
7. **§3b**: remove v1 P-A2 from the rank/starts row; either turn the form-defect vs content-fit
   row into two predictions with named outcomes, or drop it, and correct its premise (degree is
   preserved, so a form defect predicts no change).
8. **Tag §4(c) and §6 as informed by the proposal / rule side.**
9. Minor: drop "13.67 / order of magnitude" from P-A1; narrow P-B4 to the declared r; define or
   drop "small addition" in P-B6; make P-A1's +0.020 boundary strict.

Items 1–5 decide whether the predictions can be refuted cleanly. Items 6–9 are wording and
record-keeping.

### C.6 Files opened in this round

- `docs/plans/2026-09-23-first-rule-failure-predictions.md` (DRAFT v2), in full
- `results/genome/c6/harness.py`: a grep for definitions, dial, loto, labels and verdict; lines
  314–326, 350–375, 643–745, 870–1075, 1320–1332, 1365–1370, 1510–1520, 1560–1720; and the
  constants `DIAL_F`, `DIAL_SEEDS`, `A5_MAX_RATIO`, `SWAPS_PER_EDGE`
- `results/genome/c6/rule_runs/first_rule_k12/result.json` (with Python: `exam.loto`, `exam.dial`)
- this report (tail, then appended)
- `git status --short`, which printed the path, not the content, of the forbidden file
  `docs/plans/2026-09-23-first-rule-failure-rule-side.md`

Not opened: that rule-side file, anything under `results/genome/c6/rules/` or
`results/genome/c6/rule_runs/first_rule/`, the proposal, the search criterion, the group chat, or
their git history.

---

## Part D: review of DRAFT v3 (changed items only)

**Written:** 2026-09-23 11:12 UTC (18:12 local, +07:00), by the same blind reader. Parts A–C are
not edited. Scope: the "Changed in v3" list, the new §4c, and the rewritten §3b and §4b. Items that
passed in Part C and did not change are not re-reviewed.

### D.1 Changed predictions against (i)–(iv)

| id | (i) | (ii) | (iii) | (iv) | verdict |
|---|---|---|---|---|---|
| **P-J2** (ablation) | refuting outcome distinct (< +0.010) | **Fails.** The ablated variant removes **two** components: BF_r's bilinear term **and** N1's per-node effects ("global intercept + X, no per-node terms"). Both costs are already measured. N1's per-node effects are worth **+0.0478 nats** held-out over a global base rate (`harness_controls.json` `nulls_real_bank.N0.existence` − `N1.existence` = 0.41030 − 0.36248; also `controls["real/N0 as a rule"].P4.rule_margin_existence` = −0.04782). BF's term is worth +0.040 to +0.049 on top (`P4.bf.margin`). So unless X alone rebuilds both, the expected gap is about **+0.09 under either reading**, far above the +0.025 bar. The outcome measures how much of degree and bilinear structure X can rebuild, not "form defect vs overfit". The CC note's "which this file does not measure" is wrong: it is measured, as above. | 0.025 / 0.010 are author-chosen, declared | Two runs, descriptive (§4b). But "λ re-chosen … grid {1, 3, 10, 30, 100}" is BF's λ grid, and the ablated model has **no BF term**, so which penalty is re-chosen is undefined. | **fails (ii); (iv) underdefined**. Fix: remove **one** component (only N1's per-node effects, keeping BF_r + X + intercept; or only the bilinear term) and state what each reading predicts for that removal. Otherwise demote it to a descriptive run with no prediction. |
| **P-J3** | **Fixed.** The complement of Δ ≤ 0 is exactly "P4 passes" (on the real bank BF_r is the binding threshold, since RP_r ≤ +0.0012). A tie is a fail and satisfies Δ ≤ 0. A margin below BF_r − 0.005 refutes the quantity, not the claim; stated. | yes | +0.0493 / +0.0485 correct (Part C) | P4 record | **passes** |
| **P-J5** | **Fails.** The refuting outcome "margin < −0.010" and the undetermined zone "[−0.015, −0.010)" **overlap**: a margin of −0.012 is both. Presumably the lower refuting bound should be < −0.015, or the zone dropped. | **Still fails in one branch.** When the addition *does* touch offset sets, the item says only "read alongside the offset Jaccard". That gives no rule for when a counts shift counts as refuting, so the item has no refuting outcome in that branch. When it touches **neither** offset nor counts, the counts predictions are identical to N1's, the margin is exactly 0 by construction, and "confirms" trivially. That is a definition, not a prediction. | the 0.0785 citation is now correct (B.2) | P1 counts | **fails (i) and (ii)**. Fix: resolve the overlap; in the offset-touched branch either say "no prediction" or give a decision rule (e.g. "refute only if the counts margin is > +0.015 **and** the offset Jaccard is within ±0.005 of N1's"); mark the both-untouched branch as definitional. |
| **P-A1** | **Fixed.** (−0.020, +0.020) with a strict right bound, and refuting at ≤ −0.030 or ≥ +0.020: disjoint. m(0) < +0.040 → "no prediction", stated. With m(0) ≥ 0.040, `dial_ratio` is finite (`harness.py:1327`). | yes (structure → m(1) small; ambient → ≥ +0.020; inverted → ≤ −0.030) | −0.00451, −0.0617 correct; "13.67" dropped from the item | `exam.dial`, record-only, stated | **passes** |
| **P-A4** | One refuting rule now (m_off(1) < m_off(0)). **Unnamed gap:** 0 ≤ Δ < +0.005 neither confirms nor refutes, and the "undetermined zone" column says "none named". Name it. | **Passes.** Δ = [rule(1) − rule(0)] − [N1(1) − N1(0)]. N1's offset Jaccard drops under the shuffle (real 0.42040, shuffled mean 0.40368, `checks/n1_alone/summary.json` `fields.offset`), so a rule whose own offset sets do not depend on pair identity (global or N0-like) gains about +0.017 (the first rule +0.0143; N0 as a rule +0.0165, `controls["real/N0 as a rule"].P3.offset`). A rule with per-pair offset structure loses Jaccard under the shuffle *at least as fast as* N1, giving Δ ≤ 0. The readings differ. **Resolution is adequate:** the first rule's five f = 1 offset margins (0.0375, 0.0417, 0.0392, 0.0357, 0.0395) give a 5-seed SE ≈ 0.001, well below the 0.005 bar. | +0.0245 → +0.0387, Δ = +0.01426, 2.85× the bar: correct (`exam.dial`) | `exam.dial` offset; record-only; the offset = N1's branch "does not apply", correctly | **passes; name the [0, +0.005) zone** |
| **P-A6** (new) | The refuting outcome (> 0) is possible and distinct. Small mismatch: the record field is the boolean `P2.beats.n1_insample.offset`, which is true only for margin > τ = 1e-9 (`harness.py:516`, 855). State the item on the boolean, or on "margin ≤ τ". | **Weak, and definitional in one branch.** If the addition does not touch offset sets, the in-sample margin is **exactly 0**, so the item "confirms" by construction and P2 fails on offset by definition (a tie is not a win, A7). If it does, the outcome is set mostly by the rule's **form**: an offset model that contains N1's per-source mode as a special case and is fitted to training cells will almost always beat N1 in-sample (margin > 0); one that does not (global, N0-like, as the first rule's: −0.05926) will not. Name the two readings, and say that the item tests whether X's offset model contains N1's per-source mode. | −0.05926 correct (`exam.P2.insample_rule.offset` − `insample_n1.offset`) | `P2.beats.n1_insample.offset` | **passes (i), (iii), (iv); (ii) weak; definitional in the no-touch branch (see D.2)** |
| **P-B4** (narrowed) | now refuted only at the declared r if r ≥ 8; no prediction below 8, which is fine | yes | correct | `P4.bf.margin` of rule #2 (the `harness_controls.json` profile listed in the field column is past data, not the measurement) | **passes** |
| **P-B6** (narrowed) | **Broken condition.** It now applies "only when the addition is confirmed small by the §4c registration field on which fields the addition touches **and its size**". §4c has **no size field**, so the condition can never be checked, and the item may never apply. | — | correct | `P1.existence.wins` | **fails (iv) as narrowed.** My own fix: drop "at most a small addition". The item applies to any rule #2 whose existence logit contains N1 + BF_r; an addition that damages the fold wins is exactly what would refute it. |

### D.2 §4c: does each registration answer select exactly one branch?

Field 3 is a checklist over existence / offset sets / counts / sign. Sign: no prediction depends
on it.

| prediction | offset **not** touched | offset touched | gaps / overlaps |
|---|---|---|---|
| P-J4 | definitional (tie, P3 offset fails), stated | Jaccard bar | **exactly one branch each** ✓ |
| P-A4 | "does not apply", stated | growth rule | **exactly one** ✓ |
| P-A6 | table says "still applies … P-A6's own quantity … would show whether they differ in effect". **Wrong:** with offset = N1's, the in-sample margin is **0 by construction**, so this branch is definitional, not a prediction. | table cell is **"—" (blank)**, yet this is the only branch where P-A6 is a real prediction | **misassigned: one branch mislabelled, the other empty** |
| P-J5 | one row covers both counts touched and counts not touched; with **counts also untouched**, the margin is 0 by construction (definitional) | "read alongside the Jaccard", **no decision rule** | **gap** (no refuting outcome when offset is touched); **definitional sub-branch not marked** |
| P-J3, P-A3, P-B5 (P4) | — | — | **missing branch: existence.** If X does not touch existence, and rule #2's N1 and BF parts are fitted as the harness fits them, the rule's existence predictions are BF_r's, the margin **ties** the threshold, and P4 fails by definition. All three P4 items then "confirm" trivially. §4c must branch on existence too. |

**A registration-level fact §4c does not state.** If the addition does not touch offset sets,
rule #2's offset field is N1's. Then, by construction:
- **P1** offset fails: 0 wins vs N1, since every fold ties;
- **P2** fails on offset: the in-sample margin is 0, which is not a win;
- **P3** offset fails: a tie on all 100 banks.

So **rule #2 cannot pass C6** in that branch, whatever its existence margin. The registration
must say so in plain words before the run. Otherwise, confirmations of P-J4, P-A6 and parts of
P-J5 in that branch will read as evidence when they are definitions.

**LOTO registration note.** Correct, and correctly demoted to a note. Add one condition: the
"exactly 1.00" holds only if rule #2's N1 and BF parts are fitted as the harness fits them (ridge
per-type effects, SVD start from the probability-unit residual). Another fit may not send an unseen
type's factors to 0.

### D.3 Were C.2 and C.3 applied?

**§3b (C.2):**
- **P4 row: partly.** The main correction is in: any margin above BF_r is a P4 pass for all three
  sets. But the sentence about Δ = 0 is garbled (a tie satisfies both "≤ 0" and "< +0.005"). And
  the *remaining* quantity difference is not named: a margin in [+0.040, BF_r − 0.005) refutes
  P-J3's quantity and confirms P-A3's. That is the one outcome that still separates them, and it
  can occur.
- **Rank/starts row: applied.** v1 P-A2 is removed, and P-B4 is described as BF's rank.
- **Form-defect row: applied** (demoted to a note, premise corrected). Two small slips: the note
  says Ark argued "rule #2's existence margin" (it was the first rule's), and it repeats "13.67×",
  which v3 itself dropped as meaningless.
- **Counts row:** still in the table with no counterparty; harmless.

**§4b (C.3):**
- **Item 1: partly.** "Only the registered run's verdict counts" is stated. But the ablated
  variant removes two components and its λ is undefined (D.1).
- **Item 2: partly.** It is correctly flagged as a harness change needing a `--controls` re-run.
  But with P-A5 withdrawn, per-cell logits are no longer needed: a **paired P4 resolution needs
  per-fold BF_r (and RP_r) scores**, which are simpler. "Paired resolution of … P-B2" is
  confused: P-B2 is about offset Jaccard, which BF logits do not touch.
- **Item 3: applied.**
- **Item 4: applied.**
- **Item 5: applied.** One citation slip: "acceptance A12" should be **spec A12**.
- **Item 6:** left open for Mike. Acceptable in this file, but it must be decided in rule #2's own
  registration, before the run.
- **Item 7: applied** (split into 7a and 7b; descriptive; the no-choosing-among-variants rule
  stated).
- **Missing requirements: applied** as §4c, apart from the defects in D.2.

### D.4 C.5 checklist

| C.5 item | status |
|---|---|
| 1. Fix P-J3; correct §3b P4 row and the P-J3 note | **done** (the §3b sentence is garbled, and the remaining separating outcome is unnamed) |
| 2. Missing requirements (r, timing cap, fields touched) | **partly**: added as §4c, but the P-A6 and P-J5 branches are wrong or incomplete, there is no existence branch, and the "cannot pass if offset untouched" fact is missing |
| 3. Rework or drop P-A2; mark P-A1 and P-A2 record-only | **done** |
| 4. P-J5 conditioned on offset; margin < −0.01 refutes | **partly**: the lower bound is added but overlaps the undetermined zone; the offset-touched branch has no decision rule |
| 5. P-A4: one rule, a number, an offset = N1 branch, witness 1 → P2 | **done** (split into P-A6); name the [0, +0.005) zone |
| 6. §4b: split item 7, item 4 satisfied, descriptive runs, harness changes → controls re-run | **done** |
| 7. §3b: remove v1 P-A2; the form-defect row | **done** |
| 8. Tag §4(c) and §6 | **done** |
| 9. Minor fixes (13.67, P-B4, "small addition", P-A1 boundary) | **partly**: P-B6's narrowing points to a field §4c does not have; "13.67×" survives in the §3b note |

### D.5 Is v3 ready to commit as a registration?

**No.** Blocking only:

1. **P-J2 fails (ii).** The ablation removes two components worth about +0.048 and +0.045 nats,
   so the +0.025 bar is cleared under either reading. Remove one component, with each reading's
   predicted outcome stated, or demote it to a descriptive run. Define which λ is re-chosen.
2. **P-J5 fails (i) and (ii).** The refuting and undetermined ranges overlap at [−0.015, −0.010),
   and the offset-touched branch has no refuting rule.
3. **§4c branches.**
   - P-A6: definitional when offset is untouched; its real branch is blank.
   - P-J5: its both-untouched sub-branch is definitional, and it has no rule when offset is
     touched.
   - Add an **existence** branch: if X does not touch existence, P4 is a tie by definition.
   - P-B6's condition points to a size field §4c does not have; drop the condition.
4. **State the by-construction verdict.** If the addition does not touch offset sets, P1, P2 and
   P3 all fail on offset, and rule #2 cannot pass C6. The registration must say this before the
   run, so that confirmations in that branch are not counted as evidence.

Everything else in D.1–D.4 is wording.

### D.6 Files opened in this round

- `docs/plans/2026-09-23-first-rule-failure-predictions.md` (DRAFT v3), in full
- `results/genome/c6/harness.py`: grep for `def cmp` and `beats` / `n1_insample`; lines 511–517
- `results/genome/c6/rule_runs/first_rule_k12/result.json` (with Python: `exam.dial` offset at f = 1)
- `results/genome/c6/harness_controls.json` (with Python: `nulls_real_bank` existence,
  `controls["real/N0 as a rule"].P4`)
- this report (tail, then appended)

Not opened: `docs/plans/2026-09-23-first-rule-failure-rule-side.md`, anything under
`results/genome/c6/rules/` or `results/genome/c6/rule_runs/first_rule/`, the proposal, the search
criterion, the group chat, or their git history.

---

## Part E: review of DRAFT v4 (last round)

**Written:** 2026-09-23 11:51 UTC (18:51 local, +07:00), by the same blind reader. Parts A–D are
not edited. Scope: the "Changed in v4" list and the new §4c block (the verdict facts and the
prediction/definitional table).

### E.1 The four D.5 blockers

| D.5 blocker | status | reason |
|---|---|---|
| 1. P-J2 fails (ii) | **resolved** | Withdrawn, and the ablation run dropped. Stale references remain (§4b item 4 "registered like item 1 above"; §4b's descriptive paragraph "the ablation run (item 1)"; §3b note "P-J2's ablation Δ"). That is wording. |
| 2. P-J5 fails (i), (ii) | **partly resolved** | The overlap is gone (confirm [−0.010, +0.005], refute < −0.010 or > +0.015, zone (+0.005, +0.015] only), and the offset-touched branch is "no prediction". But the quantity cell still says "either the addition's offset sets = N1's, **or the Jaccard offset is printed next to this margin**", which reads as a prediction in the offset-touched branch and contradicts §4c. And the change is marked "Johnny to confirm": the item's author has not approved the text being registered in his name. |
| 3. §4c branches | **partly resolved** | P-A6 is fixed (definitional without an offset touch; a prediction on τ with one). P-J5's branches are fixed. The existence branch is added, and P-B6's size condition is dropped. Two gaps remain, both in the existence-not-touched column (E.2): the P4 "tie" needs a condition the text does not state, and P-J1 is missing although it is also fixed there. |
| 4. State the by-construction verdict | **resolved** | Stated, and correct: without an offset touch, P1, P2 and P3 all fail on offset (ties; `harness.py` 775–783, 855, 1019). The conclusion "only an addition that touches both existence and offset sets can pass" also holds, given the condition in E.2. |

### E.2 The §4c table

**Every "prediction" cell has a refuting outcome that can occur:**

| cell | refuting outcome | can it occur? |
|---|---|---|
| P-J4, offset touched | P3 offset passes with Jaccard ≤ 0.4842 | yes |
| P-A4, offset touched | m_off(1.0) < m_off(0.0) | yes: a rule with per-pair offset structure loses Jaccard under the shuffle at least as fast as N1 does (D.1) |
| P-A6, offset touched | in-sample offset margin > τ | yes, and it is likely if X's offset model contains N1's per-source mode |
| P-J5, counts touched and offset not touched | margin > +0.015 or < −0.010 | yes (the first rule's was −0.0677) |
| P4 items, existence touched | P4 passes | yes. The table has no explicit "existence touched" column; it is implied by the other columns. Wording only. |

**Is every "definitional" cell fixed by construction?**

| cell | fixed? | why |
|---|---|---|
| P-J4, offset not touched | **yes** | Identical predicted sets give an identical Jaccard, bit for bit, on every bank. The margin is exactly 0.0, and P3's `real_m > m` (line 1019) is false on all 99. |
| P-A6, offset not touched | **yes** | Identical sets give an in-sample margin of exactly 0, and `cmp` with τ gives no win (lines 516, 855). |
| P-J5, neither offset nor counts touched | **yes** | The counts predictions are N1's, so the margin is 0 up to float noise. P1 counts uses `cmp` with τ and `mean + TAU` (lines 784–790), so it is a tie either way. |
| P-A4, offset not touched: "does not apply" | yes | m_off ≡ 0 |
| **P4 items, existence not touched: "tie, P4 fails"** | **only under an unstated condition** | P4's pass test is `bool(real_m["existence"] > thr)` (`harness.py:1028`): a plain strict `>`, **with no τ**. P3's test at line 1019 is also a plain `>`. So "tie" holds only if rule #2's per-fold existence log-losses are **bit-identical** to BF_r's. "Fitted as the harness fits them" is not enough. The rule decodes through its own program (cast to float32 → float64, line 277), so any difference in operation order, clipping or dtype gives a Δ of about 1e-12. That tiny Δ then *decides* P4, in either direction, and the cell is not definitional. The condition must read: "if rule #2's existence predictions are bit-identical to BF_r's, P4 ties and fails; otherwise Δ is noise-level and P4 is decided by noise". |
| **missing definitional cells, existence not touched** | — | **P-J1**: the rule's margin is then BF_r's margin at the declared r, already known from the deterministic BF fits (+0.04933 at r = 8, +0.04851 at r = 12, +0.03972 at r = 4). So P-J1 is settled by the declared r, not by the run. **P-B6**: its own note says it is definitional there (BF's 10/10), but the table does not list it. |

**A finding about the exam** (reported, not a change to this file). Spec A7 says a tie within τ
is not a win "when superiority is tested (P1 on existence and offset set; P2; P3; P4)". The
harness applies τ in P1 and P2 (`cmp`) but **not** in P3 (line 1019) or P4 (line 1028), which use
a plain `>`. For every rule so far this made no difference, because the margins were far from
the thresholds. For a rule built on BF_r, it matters exactly at the point P-J3, P-A3 and P-B5 are
about. This is for the spec's owner of record (Zcode). Under the two-way freeze it is recorded as
a finding, not fixed here.

**A note on my own items.** The BF fits are deterministic (seeded starts, fixed folds). So:
- P-B4 at r ∈ {8, 12, 16} is **already measured**: +0.04933, +0.04851, +0.04851. It is a
  prediction only at a declared r that has not been run yet.
- The BF half of P-B3 at r = 8 is already measured (Δ = +0.00005 between k = 3 and k = 10). Only
  the rule half is still a prediction.

That does not block the commit, but these two should say so.

### E.3 Verdict

**No.** It is close. The commit is blocked by three short fixes and one approval:

1. **The P4 definitional cell.** Add the bit-identical condition (`harness.py:1028` uses a plain
   `>`, no τ). Without it, the "existence not touched → P4 fails" fact, and "only a rule touching
   both existence and offset can pass", are not true by construction.
2. **The existence-not-touched column.** Add P-J1 (and list P-B6) as definitional there, since
   their outcomes are fixed by the declared r.
3. **P-J5.** Delete "or the Jaccard offset is printed next to this margin" from the quantity cell,
   so that the offset-touched branch has only "no prediction".
4. **Johnny's approval** of the v4 text of P-J5, which is registered under his name.

Not blocking, and to be tidied when convenient:
- the stale references to P-J2 and the ablation (§4b items 1 and 4, the descriptive paragraph,
  the §3b note);
- "13.67×" and "small addition" in §3b;
- the garbled Δ = 0 sentence in §3b's P4 row;
- "acceptance A12" should read spec A12;
- §4b item 2's "logits … P-B2";
- "Predictions v3" as the §3 heading, and "for v3" in the history;
- the known values under P-B3 and P-B4 (E.2).

### E.4 Files opened in this round

- `docs/plans/2026-09-23-first-rule-failure-predictions.md` (DRAFT v4): the history lines 40–59 and
  §3 to §4c (lines 189–398); a grep for "Changed in v4" and the section headings
- `results/genome/c6/harness.py`: lines 273–312, 744–796, 840–868; a grep for lines 1019 and 1028
- this report (appended)

Not opened: `docs/plans/2026-09-23-first-rule-failure-rule-side.md`, anything under
`results/genome/c6/rules/` or `results/genome/c6/rule_runs/first_rule/`, the proposal, the search
criterion, the group chat, or their git history.
