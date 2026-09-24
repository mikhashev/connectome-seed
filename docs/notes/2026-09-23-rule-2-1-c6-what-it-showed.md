# Rule #2.1 on C6: what the run showed and what it did not

**Written:** 2026-09-23 UTC, by CC (subagent), on Mike's word in the DPC Research group chat
(20:29 UTC, "давай 1": write this outcome note). **No new run of any kind was made for this note.**
Every number is quoted from a committed file, or computed by arithmetic on one (said where so).

**Short names for the sources used below.**

| name | path |
|---|---|
| `RESULT` | `results/genome/c6/rule_runs/second_rule_v21_r1/RESULT.md` |
| `R` | `results/genome/c6/rule_runs/second_rule_v21_r1/result.json` (keys under `exam.` unless shown) |
| `PR` | `results/genome/c6/rule_runs/second_rule_v21_r1/post_run.json` |
| `ATT` | `results/genome/c6/rule_runs/second_rule_v21_r1/ATTEMPTS.md` |
| `HC` | `results/genome/c6/harness_controls.json` |
| `N1A` | `results/genome/c6/checks/n1_alone/summary.json` (and its `RESULT.md`) |
| `REG` | `docs/plans/2026-09-23-rule-2-1-registration.md` |
| `PROP` | `docs/plans/2026-09-23-second-rule-proposal.md` (governs where `REG` is silent) |
| `PRED` | `docs/plans/2026-09-23-first-rule-failure-predictions.md` |
| `ADD` | `docs/notes/2026-09-23-predictions-addendum-after-tau.md` |
| `H` | `results/genome/c6/harness.py`, LF sha256 `6fc80952…` (the run's `R` `stamp.harness_sha256_lf`, and `HC` `harness_sha256_lf`) |

## 1. The verdict, and where each label comes from

Verbatim (`R` `verdict_line`; `RESULT` line 3):

> **C6 verdict for second_rule_v21_r1 (k = 10 starts, r = 1): FAIL -- copy or marginal; below
> threshold for this family; family fits anything**

`H` builds the labels at lines 1049–1061, one label per failed check. Each row below was checked
in the code and against the record.

| label | check | field that failed it | record | `H` lines |
|---|---|---|---|---|
| copy or marginal | P1 (`r1["pass"]` is false) | **offset**. P1 offset needs ≥ 9 of 10 fold wins against each of N1, N0 and N_EB. It got 9, 8 and 3. Existence (10 wins), counts (0 losses) and sign (0 losses) pass. | `R` `P1.offset.wins_vs` = {N1: 9, N0: 8, N_EB: 3}, `P1.offset.pass` false; `P1.existence.pass`, `P1.counts.pass`, `P1.sign.pass` true | 780–783 (offset pass), 792 (P1 pass = all four fields), 1052–1053 (label) |
| below threshold for this family | P2 (`r2["all_opponents_beaten"]` is false) | **offset**. In-sample, the rule loses on offset to D_k^N1 at k\* and to N1: 0.4762 vs 0.4961. At k\* = 0, D_k^N1 is N1 itself. On existence it beats all three opponents. | `R` `P2.beats` = {dk_star: {existence true, offset **false**}, dk_armed: {true, true}, n1_insample: {existence true, offset **false**}}; `P2.insample_rule.offset` 0.47622, `P2.insample_n1.offset` 0.49607; `P2.k_star` 0 | 853–857 (beats), 1056–1057 (label) |
| family fits anything | P3 (`r3["pass"]` is false) | **offset**. 24 of 99 shuffled banks have an offset margin at least as large as the real one. Existence passes (0 of 99). | `R` `P3.offset.n_shuffled_ge_real` 24, `strictly_above_all` false; `P3.existence.strictly_above_all` true | 1016–1022, 1058–1059 (label) |

**P3's pass uses only existence and offset.** Line 1022 reads
`r3["pass"] = r3["existence"]["strictly_above_all"] and r3["offset"]["strictly_above_all"]`.
Sign and counts are computed and recorded (lines 1016–1021) but never read there. So the sign row
of P3 (margin 0, 99 of 99 shuffles ≥ real) plays no part in "family fits anything".

**All three labels come from offset.** Existence passes P1, P2 and P3 here. The three labels that
did not fire, and why:

- **"rule did not run"** (line 1050): N0 beats the rule in at most 2 folds on any field (`R` `did_not_run.folds_where_N0_beats_rule`: offset 2, all others 0). The limit is `DNR_MAX` = 5 (line 79).
- **"not a bottleneck"** (line 1054): DL(rule) 9,217 bits ≤ DL(bank)/10 = 9,481.2 (`R` `P2.length_ok` true; line 856).
- **"ambient, not substantive structure"** (line 1060): P4 passes (`R` `P4.pass` true; line 1031).

## 2. The arms

All at k = 10 starts and r = 1 (`R` `stamp.starts_k`, `stamp.rank_r`). Scores are held-out means
over 10 folds unless marked in-sample.

### P1 (`RESULT` §P1; `R` `per_fold_*` and `P1`)

| field | rule | N1 | N0 | N_EB | fold record | pass |
|---|---|---|---|---|---|---|
| existence (lower is better) | 0.3287 | 0.3625 | 0.4103 | 0.3625 | wins vs N1: 10 | true |
| offset (higher is better) | 0.4685 | 0.4204 | 0.4465 | 0.4842 | wins vs N1 9, N0 8, N_EB 3 | **false** |
| counts (lower is better) | 0.9204 | 0.9861 | 1.0157 | 0.9076 | losses 0, mean not worse | true |
| sign (higher is better) | 0.9768 | 0.9768 | 0.6225 | 0.9768 | losses 0, mean not worse | true (a tie: the rule's sign is N1's by construction, `RESULT` interpretation line 3) |

### P2 (`R` `P2`)

- DL(rule) **9,217 bits**, of which the program is 3,904. DL(bank) is 94,812, so the limit is 9,481.2. Length ok: true.
- k\* = 0 and k\*_armed = 6.
- In-sample existence: rule 0.2779 against D_k^N1 = N1 at 0.3354 and D_k^N0 at 0.4075. The rule beats all three.
- In-sample offset: rule 0.4762 against D_k^N1 = N1 at 0.4961 (loses) and D_k^N0 at 0.4482 (beats).

### P3 (`R` `P3`; p-values from `R` `P3_p_values`, computed as (1 + n)/(99 + 1), `H` lines 1634–1635)

| field | real margin over N1 | shuffled mean | shuffled max | shuffled ≥ real | one-sided p |
|---|---|---|---|---|---|
| existence | +0.0338 | −0.0007 | +0.0008 | **0** | 0.01 |
| offset | +0.0481 | +0.0421 | +0.0622 | 24 | 0.25 |
| counts | +0.0657 | +0.0104 | +0.0243 | 0 | 0.01 |
| sign | 0.0000 | 0.0000 | 0.0000 | 99 | 1.00 |

The shuffle invariants hold (`R` `shuffle_invariants_hold` true). Counts also clear all 99
shuffles, but counts do not enter P3's pass (line 1022).

### P4, the Δ, the tie band and the paired SE

- Rule's existence margin over N1: **+0.033776** (`R` `P4.rule_margin_existence`).
- Random-projection threshold: +0.0010 (`R` `P4.rp_threshold` 0.001005; argmax seed 1009, side 1, `PR` `rp_threshold_argmax`).
- BF_1 margin: **+0.028150**, with λ = 1.0 in all 10 folds. BF_1 beats N1 in 10 of 10 folds (`R` `P4.bf.margin`, `P4.bf.lambdas`, `P4.bf.folds_beating_N1`).
- Threshold: +0.028150 (BF_1 binds). Harness pass: **true** (`R` `P4.threshold`, `P4.pass`).
- **Δ = rule − BF_1 = +0.005626** (`PR` `p4_tie_band.delta`).
- **Tie band** (registered, `PROP` §4.1): Δ > +0.002 counts as a pass. Reading: **"passed (Delta > +0.002)"** (`PR` `p4_tie_band.reading`).
- **S2-8 paired read:** the paired SE of the ten per-fold Δ's is **0.00156** (`PR` `s2_8.paired_se` 0.0015622). The bar is max(+0.005, 2 × SE = 0.00312), which is **+0.005** (`PR` `s2_8.bar`). Δ ≥ bar, so the zone is **"a real amount"** (`PR` `s2_8.zone`).
- 9 of the 10 per-fold Δ's are positive. The only negative one is fold 3, at −0.00496 (`PR` `s2_8.per_fold_delta`; counted here).

### The mandatory BF_1..BF_4 line (`PR` `bf_line`; `RESULT` post-run block)

| r | BF_r margin over N1 | rule − BF_r | role |
|---|---|---|---|
| 1 | +0.02815 | **+0.00563** | the decision |
| 2 | +0.02823 | +0.00555 | context only |
| 3 | +0.04034 | **−0.00656** | context only |
| 4 | +0.03972 | **−0.00595** | context only |

Reproduction checks in `PR` `checks` (bf1_matches_record, rp_max_matches_record,
loto_means_match_record, bf3_reproduces_controls, bf4_reproduces_controls): **all true**.

**BF_2's provenance.** Unlike BF_1, BF_3 and BF_4, which are reproduced against pre-existing
records (`checks` above), BF_2 is trained at run time by the post-run script itself, as
registered: `results/genome/c6/rules/second_rule_v21/post_run.py` builds `BF_RANKS` and calls
`H.bf_predictor(r)` (`harness.py` lines 734–735) under cross-validation for each rank in
`BF_RANKS`, including r = 2 (`post_run.py` lines 161, 283–284). `REG` registers this BF sweep
(`docs/plans/2026-09-23-rule-2-1-registration.md` line 454: rule tested "against BF_2, BF_3 and
BF_4 (context)").

### Spread-log check (`PR` `spread_log`; also `spread_log_validation.json`)

The check found 1,341 per-fit files for 1,341 rule fits. All 1,341 parse as JSON, no temporary
files were left, and no per-bank count mismatches were found. `file_count_equals_fit_count` and
`spread_log_reliable` are both true.

### Leave-one-type-out (descriptive; `R` `loto`)

| field | rule mean | N1 mean |
|---|---|---|
| existence | 0.3819 | 0.3858 |
| offset | 0.5005 | 0.4564 |
| counts | 0.8775 | 0.9939 |
| sign | 0.7676 | 0.7676 |

The existence ratio rule/N1 is **0.990** (computed here from the two means).

## 3. The main finding: three facts added together

This is Johnny's framing from the chat (20:12 UTC). No single fact carries it alone.

**Correction (Ark, review, 2026-09-23 20:46 UTC): P3 existence passing "for the first time" is
wrong.** Rule #1 also had P3 existence 0 of 99 shuffles ≥ real, `strictly_above_all` true
(`results/genome/c6/rule_runs/first_rule_k12/result.json` `exam.P3.existence`). What is new for
rule #2.1 is P1 existence at 10 of 10 folds (rule #1: 5 of 10) and passing P4 (rule #1 did not).

| field (`exam/P3/existence/*`, `exam/P4/*`) | rule #1 (`first_rule_k12/result.json`) | rule #2.1 (`R` = `second_rule_v21_r1/result.json`) |
|---|---|---|
| P1 existence | 5/10, **FAIL** | 10/10, **PASS** |
| P3 real_margin | −0.00451 | +0.03378 |
| P3 shuffled_mean | −0.06431 | −0.00068 |
| P3 shuffled_max | −0.04355 | +0.00082 |
| P3 n_shuffled_ge_real | 0 | 0 |
| P3 gap (real − shuffled_max) | +0.03904 | +0.03296 |
| P4 | **FAIL** (rule margin −0.00451 vs threshold = bf margin +0.04851, bf rank 12) | **PASS** (bf margin +0.02815, bf rank 1) |

**Consequence.** The count "0 of 99" does not say which mechanism produced it. Rule #1's gap came
from the rule degrading on shuffled banks while its own real margin was already negative; rule
#2.1's gap came from improving on the real bank while staying near zero on shuffles. So the P3 gap
by itself is not a measure of rule quality — the failed rule #1 has the larger gap of the two.

1. **P1 existence: 10 of 10 fold wins over N1** (`R` `P1.existence.wins` = 10). On held-out cells of the real bank, the rule predicts existence better than N1 in every fold.
2. **P3 existence: 0 of 99 shuffled banks do at least as well as the real one.** The real margin is +0.0338. The shuffled maximum is +0.0008 and the shuffled mean is −0.0007 (`R` `P3.existence`). The margin exists on the real bank and vanishes on degree-preserving shuffles.
3. **Step 0: N1 alone does not separate real from shuffled on existence.** Real 0.36248; shuffled min, mean and max 0.35938, 0.36234 and 0.36564. 56 of 99 shuffles are as good or better, p = **0.57** (`N1A` `fields.existence`). N1's scoring code is unchanged between that check's harness (`c01cd9eb…`) and this run's. `git diff ae89705 HEAD -- results/genome/c6/harness.py` touches only the τ lines of P3 and P4. N1's real existence score is 0.3625 in both.

**Sum:** the gap between real and shuffled comes from what the rule adds on top of N1, not from N1.
It depends on pair structure that the shuffle destroys while keeping every node's degree and the bag
of contents (`N1A` `RESULT.md`, "Shuffle mechanism"). Fact 3 can only locate the gap. By
construction, it cannot say on its own whether structure beyond degree exists (`N1A` `RESULT.md`,
Ark's limitation, 09:02 UTC).

### The dial (Ark, 20:15 UTC)

Held-out margin over N1. Each cell is the mean over 5 seeds, with the [min, max] over those seeds
in brackets. Means are computed here from `R` `dial[*].heldout_margin_over_N1`.

| f (fraction shuffled) | existence | offset | counts |
|---|---|---|---|
| 0 | +0.0338 [+0.0338, +0.0338] | +0.0481 [+0.0481, +0.0481] | +0.0657 [+0.0657, +0.0657] |
| 0.25 | +0.0056 [+0.0022, +0.0090] | +0.0435 [+0.0397, +0.0527] | +0.0399 [+0.0349, +0.0440] |
| 0.5 | +0.0013 [−0.0010, +0.0028] | +0.0424 [+0.0367, +0.0501] | +0.0227 [+0.0177, +0.0301] |
| 0.75 | −0.0002 [−0.0028, +0.0015] | +0.0376 [+0.0304, +0.0484] | +0.0061 [+0.0043, +0.0093] |
| 1 | −0.0008 [−0.0018, +0.0003] | +0.0362 [+0.0309, +0.0398] | +0.0072 [−0.0005, +0.0109] |

What the dial shows:

- **Existence** loses about 83 % of its margin once a quarter of the cells is shuffled, and reaches zero by f = 0.75.
- **Offset** keeps about three quarters of its margin (+0.0362 of +0.0481) under full shuffling. This is the same fact P3 offset records (shuffled mean +0.0421, 24 of 99 ≥ real). Most of the offset margin survives what the shuffle keeps.
- **Counts** fall steadily to near zero.

**Correction: two views of one instrument, not two independent instruments.**

- **f = 1 and P3 use the same function.** The dial at f = 1 and P3's shuffled banks both call `rewire_and_permute(base, rng, 1.0)` (`H` lines 909 and 932), on different seeds. P3 uses seeds 0–98 with `PCG64(seed)` (lines 908, 1227). The dial uses `PCG64(10000 + 100·fi + sd)`, which is seeds 10400–10404 at f = 1 (line 931). So the dial at f = 1 agreeing with P3 is expected. Existence: −0.0008 (dial) vs −0.0007 (P3 mean). Offset: +0.0362 vs +0.0421. Counts: +0.0072 vs +0.0104. The agreement is five more draws of the same random process, not a second instrument. The same note was made for the first rule (`PRED` §2, "two implementations, one number").
- **f = 0 is the real bank.** At f = 0, `dial_banks` copies the base content unchanged (lines 928–929). So m(0) equals the real margin by construction: +0.033776150658201 on all five seeds, the same float as `R` `P3.existence.real_margin`. m(0) is not a measurement of anything new.

## 4. Attribution: the rank-1 part or the group addition? (Johnny's open question)

The rule's existence term is N1 plus a rank-1 bilinear term plus field groups (`PROP` title and
§2.2). The run cannot say which of the last two parts carries the separation. The committed record
holds only a **proxy**: the P3 existence rows of the five real-bank controls in `HC` (Zcode, 20:23 UTC).

| control (`HC` `controls["real/…"]`) | what it is | existence margin over N1 | shuffled max | shuffled ≥ real | implied one-sided p |
|---|---|---|---|---|---|
| RP_r8 as a rule (seed 999) | N1 plus a **random** rank-8 projection (`H` 445–448, 1278–1279) | −0.0123 | −0.0045 | 62 | 0.63 |
| PR | the planted-class predictor, using the four classes planted in the synthetic banks PL1, PL05 and PL0 (`H` 1086–1088, 1280–1281) | −0.0476 | −0.0448 | 28 | 0.29 |
| N1 as a rule | N1 itself | 0 | 0 | 99 | 1.00 |
| N0 as a rule | N0 | −0.0478 | −0.0448 | 33 | 0.34 |
| oracle | stores the bank's full content (`H` 441–442) | +0.3615 | +0.3646 | 43 | 0.44 |
| *for comparison: rule #2.1* | | *+0.0338* | *+0.0008* | *0* | *0.01* |

(Every value in the table is from `HC` `controls["real/<name>"].P3.existence`: `real_margin`,
`shuffled_max` and `n_shuffled_ge_real`. The p column is computed here as (1 + n)/(99 + 1), the
same formula `R` `P3_p_values` uses (`H` lines 1634–1635), restored per Zcode's review request.)

**What the pre-registration of the BF_1 P3 run must carry.** This run is proposed but **not
approved or run yet** (§8). The reviewers ask that its pre-registration state, in
advance:

- **Three numbers, not one band** (Ark): `real_margin`, `shuffled_mean` and `shuffled_max`, not a
  single pass/fail band.
- **A machine check** (Ark): P3(BF_1).real_margin must equal `exam/P4/bf/margin` = **+0.028150**
  from the rule #2.1 record (`R` `P4.bf.margin`). If it does not, the "BF_1" of the new run and the
  BF_1 inside P4 are different objects, and that mismatch is reported before any reading.
- **Reading by distance** (Ark): BF_1 does not separate if its shuffled_max lands near its own real
  margin (+0.028, gap ≈ 0). It separates if shuffled_max lands near the rule's measured shuffle
  bound (+0.0008, gap ≈ +0.027).
- **Each outcome paired with what the second brain (FlyWire) then tests** (Johnny): if BF_1
  separates, the rank-1 part is itself bank-specific and X adds only margin level — the second
  brain tests "is the rank-1 structure bank-specific?". If BF_1 does not separate, X (the group
  terms) carries the separation — the second brain tests "is the group structure bank-specific?".

**Zcode's lesson from the oracle row.** The oracle is as accurate as any predictor can be: its
existence margin over N1 is +0.36. Yet 43 of 99 shuffles match or beat it, because it is equally
perfect on every shuffled bank. **Separation is a signature of using structure the shuffle
destroys, not of accuracy.**

**This is a proxy, not an answer.** None of the five controls separates on existence, and only
rule #2.1 does. RP_r8 is the nearest stand-in for a low-rank term, and it does not separate. But
RP_r8 is **rank 8** and a **random** projection. It is not the **trained** BF_1 inside the rule,
and BF_1 by itself beats N1 in 10 of 10 folds (`R` `P4.bf.folds_beating_N1`). So the proxy cannot
rule out that the rank-1 part alone would separate.

**The direct test is proposed, not run.** It is P3 of BF_1 itself: BF_1 on the 99 shuffled
banks, the same seeds. The chat estimate is about 15 minutes. Before it runs, it needs a short
pre-registration that states what each outcome means:

- BF_1 separates with a gap like the rule's;
- BF_1 separates with a smaller gap;
- BF_1 does not separate.

It also needs the band that decides "like the rule's".

## 5. What the run does not show

- **P4 is passed only against BF_1.** The rule beats BF_1 by +0.00563 and BF_2 by +0.00555. It **loses** to BF_3 by −0.00656 (BF_3 +0.04034) and to BF_4 by −0.00595 (BF_4 +0.03972) (`PR` `bf_line`). BF_8's margin is +0.04933 (`HC` `controls["real/RP_r8 as a rule (seed 999)"].P4.bf.margin`), 0.0156 above the rule. r = 1 is the **lowest** of the known BF reference points (`ADD` §3). The rule's author disclosed this before the run: "A reader should weigh a P4 pass at r = 1 with that in mind" (`PROP` §3). So the pass does not mean "beats the best factorisation".
- **The family was chosen after the regularity numbers were read.** Rule #2's author had read rule #1's real-bank results and the whole-bank regularity numbers before choosing the family (`PROP` §3; `RESULT` interpretation line 4). The caveat travels with this result.
- **p = 0.01 is a floor, not an estimate.** With 99 shuffles and none at or above the real margin, p = (1 + 0)/(99 + 1) = 0.01 is the smallest value the test can print. A Bonferroni correction over P3's four fields gives 4 × 0.01 = **0.04**.
- **The bank is a template, not one fly.** It is flyvis's FIB-25/FIB-19 type-level template, column-averaged, and it merges two female flies by taking the larger of the two estimates (their equation 7) (`docs/notes/2026-09-23-where-our-bank-comes-from.md` §2.1–§2.2, §3; `RESULT` interpretation line 1). **Column averaging is not between-fly stability.** It removes variation between columns inside one reconstruction and says nothing about what carries over between individuals (same note §3; `RESULT` interpretation line 2). The finding answers "is a type-level template compressible?", not "is an individual brain compressible?".
- **The post-run script crashed once; the verdict was not touched.**
  - `rules/second_rule_v21/post_run.py` first ran at 19:55:49 UTC at `6baff38`. It set `ROOT` to `results/` instead of the repository root, so every refit worker failed with a FileNotFoundError on `results/results/genome/...` (`ATT` "Post-run").
  - Nothing it wrote was kept. The fix is `fb24d17` (one line: `ROOT = C6.parents[2]`), and the second execution completed at 19:57:49 UTC.
  - The verdict was written earlier, by the harness, and committed first (`6baff38`). The post-run script changes no verdict (`PR` `what`).
  - **The same bug is still in rule #2's script:** `results/genome/c6/rules/second_rule/post_run.py` line 54 reads `ROOT = C6.parents[1]`. Rule #2 never ran on C6, so it never mattered. `fb24d17` left it untouched on purpose. Anyone reusing that script inherits the crash.

## 6. Registered predictions: mechanical outcomes

These are the items that `REG` §7 carries over, judged on the branches in `PROP` §4.4. "Silent"
means the item registered no reading for this case. "Not applicable" means its branch does not
apply.

### Registered items (`PRED` §3, with `ADD` §4)

| item | registered claim / quantity | outcome | number |
|---|---|---|---|
| P-J1 | inherits BF's margin; ≥ +0.040, refuted < +0.030 | **silent**: registered silent on quantity at r = 1 (`ADD` §4) | margin +0.0338. Johnny's live reading (not registered), "≈ BF_1 within ±0.002", i.e. [0.026, 0.030], does not hold: the margin is 0.0056 above BF_1. By his own words, anything outside that band is the addition's effect. |
| P-J3 | P4 fails; Δ ≤ 0 | **refuted** | Δ = +0.00563; harness P4 pass true |
| P-J4 | P3 offset passes only at Jaccard ≥ 0.4831; refuted by a pass at ≤ 0.4842 | **confirmed** (the refuting outcome did not occur) | P3 offset fails; held-out Jaccard 0.4685 |
| P-J5 | counts tie | **not applicable** (no prediction when offset sets are touched) | counts margin +0.0657, recorded only |
| P-A1 | dial: m(1.0) ∈ (−0.020, +0.020) and m(1.0)/m(0.0) ≤ 0.25; only if m(0.0) ≥ +0.040 | **silent**: the guard did not open, since m(0.0) = +0.0338 < +0.040 | The data match the item's content: m(1.0) = −0.0008 and the ratio is −0.023. **Ark declines to claim it**, and it is not counted. |
| P-A3 | P4 fails (quantity empty at r = 1, `ADD` §4) | **refuted** (claim) | P4 pass; Δ = +0.00563 |
| P-A4 | offset margin grows under destruction: m_off(1.0) − m_off(0.0) ≥ +0.005; refuted if m_off(1.0) < m_off(0.0) | **refuted** | +0.0362 − 0.0481 = **−0.0119** (the rule's author expected this refutation) |
| P-A6 | in-sample offset margin ≤ τ | **confirmed** | 0.4762 − 0.4961 = **−0.0199** (`R` `P2.beats.n1_insample.offset` false) |
| P-B1 | P3 existence passes; margin ≥ +0.040; shuffled max ≤ +0.025; gap ≥ +0.015 | **confirmed on its named refuting outcomes**. Neither "any shuffle ≥ real" nor "gap < +0.015 with the arm passing" occurred. **Its stated margin of ≥ +0.040 was not met.** | 0 of 99; margin +0.0338; shuffled max +0.0008; gap +0.0330 |
| P-B2 | P3 offset fails unless Jaccard > 0.4842 | **confirmed** | P3 offset fails; Jaccard 0.4685 |
| P-B3 | \|margin(k = 10) − margin(k = 3)\| < 0.001 | **silent**: not measured, because the k = 3 descriptive run (`PROP` §5.3) was not made | — |
| P-B4 | BF_r ∈ [0.045, 0.052] at r ≥ 8 | **not applicable** (r = 1) | — |
| P-B5 | P4 fails; rule − BF_r < +0.005 | **refuted** (claim and quantity) | rule − BF_1 = +0.00563 ≥ +0.005 |
| P-B6 | ≥ 9 of 10 existence wins vs N1 | **confirmed** | 10 of 10 |
| LOTO note | registration note, not a prediction; does not hold by construction here (`PROP` §4.4) | **not applicable**. The author's descriptive expectation (ratio < 1.00 and below 1.3) holds. | ratio 0.990 |

### The author's items (`PROP` §4.2, carried by `REG` §7)

| item | claim / quantity | outcome | number | author's probability |
|---|---|---|---|---|
| S2-1 | P1 existence passes | **confirmed** | 10 wins | 0.85 |
| S2-2 | P1 offset fails on N_EB; wins vs N1 ≥ 9, vs N0 ≥ 9; Jaccard ∈ [0.475, 0.505] | **claim confirmed, quantity refuted** | 3 wins vs N_EB. But 8 wins vs N0 (not ≥ 9), and the Jaccard is 0.4685, below the band. | 0.75 |
| S2-3 | P1 counts passes; margin ∈ [+0.030, +0.100] | **confirmed** | 0 losses; margin +0.0657 | 0.75 |
| S2-4 | sign tie | **definitional**, not a prediction | 0.9768 = 0.9768 | — |
| S2-5 | P2 in-sample offset margin > τ | **refuted** | −0.0199 | 0.75 |
| S2-6 | P3 existence passes; gap ≥ +0.010 | **confirmed** | 0 of 99; gap +0.0330 | 0.8 |
| S2-7 | P3 offset fails | **confirmed** | 24 of 99 | 0.6 |
| S2-8 | X adds held-out existence information beyond BF_1: Δ ≥ max(+0.005, 2 × paired SE) | **confirmed ("a real amount")** | Δ +0.00563; bar +0.005; SE 0.00156 | Δ > 0: 0.5; Δ > +0.002: 0.4; at or above the bar: 0.3 |
| S2-9 | whole exam fails | **confirmed** | FAIL | 0.95 |

**All three "P4 fails" items were refuted:** P-J3 (Johnny), P-A3 (Ark) and P-B5 (the blind reader).
The rule's author put about 0.5 on Δ > 0 (`PROP` §4.2 S2-8; `ADD` §4, "about 0.5 that the margin
lands above BF_1"). That was the best-calibrated prior on this outcome, which is one outcome, not a
calibration record. The same author's refuted items are S2-5 and the quantity half of S2-2.

## 7. Corrections made in the chat

- **"Family fits anything = offset + sign" (Johnny) is wrong.** P3's pass reads only existence and offset (`H` line 1022), and existence passed, so the label comes from offset alone.
- **"Two independent instruments" is overstated (Ark, withdrawn).** The dial at f = 1 and P3 run the same shuffle function on different seeds (§3 above). Ark confirmed this in code: `shuffled_bank` (`H` lines 907–909) and `dial_banks` (`H` lines 924–932) both call `rewire_and_permute`; at frac = 1.0 all edges are chosen, and the target swap count is `SWAPS_PER_EDGE * len(E)` with `SWAPS_PER_EDGE` = 20 (`H` line 70) — the same procedure, only the seeds differ.
- **The BF_4 figure.** Rule − BF_4 = −0.0059476 (`PR` `bf_line.rule_minus_bf.4`). That is −0.00595 at five decimals. The chat's −0.0060 rounds the already-rounded −0.00595; the value at four decimals is −0.0059.
- **Zcode's own mix-up (Zcode, requested for the record).** In the chat Zcode wrote that P-B1 "stayed silent by its +0.040 guard." That was P-A1 (Ark's item, silent because m(0.0) = +0.0338 < the +0.040 guard — see §6 table). P-B1 is a different item: it is **confirmed by its refuters** (neither named refuting outcome occurred); only its secondary +0.040 magnitude was not reached (§6 table).

## 8. Next steps, as agreed

The chat reached consensus at 20:26 UTC. **Mike has chosen only step 1 so far** (this note).

1. **This note.** Done here.
2. **The BF_1 P3 attribution run: proposed, not run.** It runs P3 of the trained BF_1 on the same 99 shuffled banks and needs a short pre-registration first (§4).
3. **The second brain (FlyWire), after that, with its own registration.** The data are downloaded and checked **outside the repository**. That was stated in the chat and is not verifiable from this repository.
4. **Offset: postponed.** All three labels come from offset. The exam is asymmetric there: N_EB computes its offset sets for free, as a null fitted on the training folds, while the rule pays bits in its DL to store its own. Whether that asymmetry is fair is a separate question about the exam, not about rule #2.1.

## Files opened for this note

`RESULT.md`, `result.json`, `post_run.json`, `ATTEMPTS.md`, `run_info.json` and
`spread_log_validation.json` of `second_rule_v21_r1`; `harness_controls.json`;
`checks/n1_alone/RESULT.md` and `summary.json`; `harness.py` (lines 60–80, 441–457, 745–1073,
1215–1300, 1322–1336 and 1628–1640); `REG` (header, §2.2–§2.3 and §7); `PRED` (in full); `ADD`
(in full); `PROP` §3–§4.4; `docs/notes/2026-09-23-where-our-bank-comes-from.md` (headings and
§1–§2.2); `rules/second_rule/post_run.py` lines 50–56; `git show fb24d17`; `git diff ae89705 HEAD
-- results/genome/c6/harness.py`; `GLOSSARY.md` (§6–§7 rows).

## Changes after review

- Johnny, 2026-09-23 20:45 UTC: paired each BF_1-P3 outcome (separates / does not separate) with
  what the second brain (FlyWire) would then test (§4).
- Ark, 2026-09-23 20:46 UTC: reworded §3's "for the first time" claim — P3 existence also passed
  for rule #1; what is new for rule #2.1 is P1 at 10/10 and passing P4 — and added the rule #1 vs
  rule #2.1 side-by-side table with its consequence paragraph (§3); added the pre-registration
  requirements for the BF_1 P3 run — three numbers, the machine check against `P4.bf.margin`, and
  reading by distance (§4); withdrew "two independent instruments" with the `shuffled_bank` /
  `dial_banks` code citation (§7).
- Zcode, 2026-09-24 05:50 UTC: restored the implied one-sided p column on the attribution table
  (§4); asked for the record that Zcode's own chat statement conflated P-B1 with P-A1 (§7); asked
  for BF_2's provenance (§2); corrected the rule #2 `post_run.py` bug line from 55 to 54 (§5).
