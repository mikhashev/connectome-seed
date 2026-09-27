# Knock out and regrow, male CNS arm: block A in each optic lobe of one male

Registration `docs/plans/2026-09-26-knockout-regrow-male-cns-arm-registration.md`, revision 1.3; A `docs/plans/2026-09-24-knockout-regrow-registration.md` (amended, LF sha256 fc41505690365ff6d82fa618b00b482cc992bb36d708ed3b6fbbe6f54f96dbec). git_head=e07e347c2c0232dfd99de2584b5d4809837286d7, runtime=15364s. Seal record: intact.

Code (S30): lobe L: pre-run made by head a0e16b6, script 7a09f9fd (LF sha256 7a09f9fdfee38d93596fe0be9ffd4daab5b82cb287acdfa4a16bbdd4a3a281fc); this run by head e07e347, script 290ecb56 (LF sha256 290ecb565759def6d11e3b76811635ce033a6b008461427ecede4704245e8e32); different code: the reference is read by this script as registered only if the --from-raw check of section 3.3.1 (h) re-derived it byte for byte; lobe R: pre-run made by head a0e16b6, script 7a09f9fd (LF sha256 7a09f9fdfee38d93596fe0be9ffd4daab5b82cb287acdfa4a16bbdd4a3a281fc); this run by head e07e347, script 290ecb56 (LF sha256 290ecb565759def6d11e3b76811635ce033a6b008461427ecede4704245e8e32); different code: the reference is read by this script as registered only if the --from-raw check of section 3.3.1 (h) re-derived it byte for byte.

**Male reading: G in both lobes, each with its own limits (power of the male R not calibrated; this G does not by itself exclude averaging as the explanation of flyvis-65's G)**

The instrument on lobe L is weaker than A's (sections 5, 6, revision 1.3): per gamma, rule #2.1 seen (p_P <= 0.01) / read R, of the worlds at that gamma: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5 (A: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5); gamma*_P = 0.75 (A 0.6), gamma_R = 0.75; M worlds that read G at or above gamma_R: M0.85 seed 92184 (rule #2.1 AUC 0.5254, p_P 0.3695); M worlds that read W: M0.85 seed 92183 (rule #2.1 n_ge = 1 of 99). This G is stated against these limits.

The instrument on lobe R is weaker than A's (sections 5, 6, revision 1.3): per gamma, rule #2.1 seen (p_P <= 0.01) / read R, of the worlds at that gamma: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5 (A: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5); gamma*_P = 0.75 (A 0.6), gamma_R = 0.75; M worlds that read G at or above gamma_R: M0.85 seed 92184 (rule #2.1 AUC 0.5420, p_P 0.2872); M worlds that read W: none. This G is stated against these limits.

## Lobe L

**Verdict: male CNS, lobe L (existence bank at c* = 2.99436): G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5449 < 0.90)]. rule #2.1: AUC = 0.5020 (32/32), p_S = 0.63 (n_ge = 62 of 99, n_deg = 0), p_P = 0.4905; ceiling_full = 0.5449, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 1, BF_3 3, BF_4 3.**

The A section 4 row, verbatim (from the amended A):

> | **G: not detected at the R level above γ_R** | not R, not W; the primary **and every BF_r** have `p_P > 0.10`; and the primary's **`ceiling_block` >= 0.90** (the condition is revision 2's, unchanged; the cut is the gate cut, `GATE_CUT`, since revision 3.2) | **Revision 3.1 (Ark 09:32, Johnny 09:33, Zcode 09:34 UTC): "not detected at the R level above γ_R; leg P passes from γ\*_P".** The block carries no structure that this family regrows at the R level at a strength at or above γ_R, where a majority of the synthetic worlds read R. Leg P alone (of rule #2.1) already sees a majority from γ\*_P, and every predictor does from the family limit (§3.6). Revision 3's "not detected above γ\*" named leg P only. The label always prints **all three limits** with their brackets, **the per-γ fractions seen/n and R/n**, the transition band, and the instrument they come from: `BF_LAMBDAS` [1, 3, 10, 30, 100], ties within 1e-9 to the larger λ, `STARTS` = 10. The rule can express the block (`ceiling_block`), and by Johnny's count the information is there (64/64 inferable). **Not** "no grammar found" and **not** "no grammar exists": the instrument has no right to either claim (Ark 08:24, Johnny 08:27 UTC). A G reached through a selected λ = 100 reads "weaker than the detection limit", not "absent" (Zcode 08:22 UTC), and since revision 3.1 it can be read from the verdict line (below). The mechanism, "orthogonal" if the primary's `ceiling_full < 0.90` and "no information" otherwise, is printed beside the label as **a description only** (§2.4, decision (c)). **Revision 3.2 (A5):** the label names its gate variable ("gate: rule #2.1's ceiling_block = … >= 0.90"), and the mechanism description names whose `ceiling_full` it quotes ("rule #2.1's ceiling_full = …"); its cut, `MECHANISM_CUT` = 0.90, is borrowed from the gate and not calibrated (§2.4). A low `ceiling_full` with the gate passed gives G ("orthogonal"), not U. |

A's literal in the quoted row: "64/64 inferable" is A's count on flyvis-65; lobe L: 64/64 inferable at c* (check 4). The limits and the instrument on the label are lobe L's own (section 3.6).

The instrument on lobe L is weaker than A's (sections 5, 6, revision 1.3): per gamma, rule #2.1 seen (p_P <= 0.01) / read R, of the worlds at that gamma: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5 (A: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5); gamma*_P = 0.75 (A 0.6), gamma_R = 0.75; M worlds that read G at or above gamma_R: M0.85 seed 92184 (rule #2.1 AUC 0.5254, p_P 0.3695); M worlds that read W: M0.85 seed 92183 (rule #2.1 n_ge = 1 of 99). This G is stated against these limits.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5020 (32/32) | 0.001 | 0.8248 | +0.0507 | 0.500 | 0.5449 | 1.0000 | 0.04 | 0.00 | 62 / 99 | 0.63 | 0.4905 | 0.4332 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.5332 (32/32) | 0.000 | 0.8282 | +0.0473 | 0.500 | 0.5547 | 1.0000 | 0.61 | 0.07 | 8 / 99 | 0.09 | 0.3256 | 0.0015 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.4932 (32/32) | -0.018 | 0.9572 | -0.0817 | 0.500 | 0.5176 | 1.0000 | -0.39 | -0.01 | 99 / 99 | 1.00 | 0.5394 | 0.7011 | 1.0 / 3.0 / 1.0 |
| BF_3 | 0.4873 (32/32) | -0.067 | 0.8476 | +0.0280 | 0.500 | 0.9688 | 1.0000 | -0.03 | -0.03 | 99 / 99 | 1.00 | 0.5719 | 0.7731 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.5088 (32/32) | -0.011 | 0.8315 | +0.0441 | 0.500 | 0.9951 | 1.0000 | 0.02 | 0.02 | 1 / 99 | 0.02 | 0.4501 | 0.3778 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5000 (32/32) | 0.000 | 0.8756 | +0.0000 | 0.500 | 0.4844 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5098 | 0.5900 | None / None / None |

Smallest passing AUC on this block (own draws; not compared with the other lobe): 0.6719. Row-and-column null: complete.

Permuted-block ceiling_full of rule #2.1: 0.560, 0.641, 0.704, 0.680, 0.688, 0.809, 0.604, 0.720, 0.617, 0.773, 0.599, 0.663, 0.613, 0.619, 0.664, 0.719, 0.612, 0.564, 0.661, 0.720 (real block 0.5449).

Fixed lambda = 1 on the knockout view, diagnostic, decides nothing: rule #2.1 AUC 0.5293, p_P 0.3464; BF_1 AUC 0.5293, p_P 0.3441; BF_2 AUC 0.4932, p_P 0.5394; BF_3 AUC 0.4795, p_P 0.6114; BF_4 AUC 0.5088, p_P 0.4513.

Offset, counts and sign fields: meaningless on an existence bank (in summary.json).

Check 3 (printed): present 32/64; quadrants {'ON x T4': 16, 'OFF x T5': 16, 'ON x T5': 0, 'OFF x T4': 0}; row counts {'Mi1': 4, 'Tm3': 4, 'Mi4': 4, 'Mi9': 4, 'Tm1': 4, 'Tm2': 4, 'Tm4': 4, 'Tm9': 4}; column counts {'T4a': 4, 'T4b': 4, 'T4c': 4, 'T4d': 4, 'T5a': 4, 'T5b': 4, 'T5c': 4, 'T5d': 4}; y = x * w: True; balanced: True. Check 5 (printed): D(N1 logit) = 0.0000.

## Lobe R

**Verdict: male CNS, lobe R (existence bank at c* = 2.99436): G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5732 < 0.90)]. rule #2.1: AUC = 0.5127 (32/32), p_S = 0.21 (n_ge = 20 of 99, n_deg = 0), p_P = 0.4318; ceiling_full = 0.5732, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 3, BF_4 3.**

The A section 4 row, verbatim (from the amended A):

> | **G: not detected at the R level above γ_R** | not R, not W; the primary **and every BF_r** have `p_P > 0.10`; and the primary's **`ceiling_block` >= 0.90** (the condition is revision 2's, unchanged; the cut is the gate cut, `GATE_CUT`, since revision 3.2) | **Revision 3.1 (Ark 09:32, Johnny 09:33, Zcode 09:34 UTC): "not detected at the R level above γ_R; leg P passes from γ\*_P".** The block carries no structure that this family regrows at the R level at a strength at or above γ_R, where a majority of the synthetic worlds read R. Leg P alone (of rule #2.1) already sees a majority from γ\*_P, and every predictor does from the family limit (§3.6). Revision 3's "not detected above γ\*" named leg P only. The label always prints **all three limits** with their brackets, **the per-γ fractions seen/n and R/n**, the transition band, and the instrument they come from: `BF_LAMBDAS` [1, 3, 10, 30, 100], ties within 1e-9 to the larger λ, `STARTS` = 10. The rule can express the block (`ceiling_block`), and by Johnny's count the information is there (64/64 inferable). **Not** "no grammar found" and **not** "no grammar exists": the instrument has no right to either claim (Ark 08:24, Johnny 08:27 UTC). A G reached through a selected λ = 100 reads "weaker than the detection limit", not "absent" (Zcode 08:22 UTC), and since revision 3.1 it can be read from the verdict line (below). The mechanism, "orthogonal" if the primary's `ceiling_full < 0.90` and "no information" otherwise, is printed beside the label as **a description only** (§2.4, decision (c)). **Revision 3.2 (A5):** the label names its gate variable ("gate: rule #2.1's ceiling_block = … >= 0.90"), and the mechanism description names whose `ceiling_full` it quotes ("rule #2.1's ceiling_full = …"); its cut, `MECHANISM_CUT` = 0.90, is borrowed from the gate and not calibrated (§2.4). A low `ceiling_full` with the gate passed gives G ("orthogonal"), not U. |

A's literal in the quoted row: "64/64 inferable" is A's count on flyvis-65; lobe R: 64/64 inferable at c* (check 4). The limits and the instrument on the label are lobe R's own (section 3.6).

The instrument on lobe R is weaker than A's (sections 5, 6, revision 1.3): per gamma, rule #2.1 seen (p_P <= 0.01) / read R, of the worlds at that gamma: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5 (A: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5); gamma*_P = 0.75 (A 0.6), gamma_R = 0.75; M worlds that read G at or above gamma_R: M0.85 seed 92184 (rule #2.1 AUC 0.5420, p_P 0.2872); M worlds that read W: none. This G is stated against these limits.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5127 (32/32) | 0.011 | 0.8145 | +0.0595 | 0.500 | 0.5732 | 1.0000 | 0.17 | 0.03 | 20 / 99 | 0.21 | 0.4318 | 0.1018 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5127 (32/32) | 0.014 | 0.7897 | +0.0842 | 0.500 | 0.5762 | 1.0000 | 0.17 | 0.03 | 5 / 99 | 0.06 | 0.4314 | 0.1004 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.4951 (32/32) | -0.009 | 0.9682 | -0.0943 | 0.500 | 0.6094 | 1.0000 | -0.04 | -0.01 | 1 / 99 | 0.02 | 0.5309 | 0.6529 | 1.0 / 3.0 / 1.0 |
| BF_3 | 0.4922 (32/32) | -0.052 | 0.8358 | +0.0382 | 0.500 | 0.9541 | 1.0000 | -0.02 | -0.02 | 97 / 99 | 0.98 | 0.5442 | 0.6470 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.5654 (32/32) | 0.034 | 0.8215 | +0.0525 | 0.594 | 0.9990 | 1.0000 | 0.13 | 0.13 | 0 / 99 | 0.01 | 0.1858 | 0.0501 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4922 (32/32) | 0.000 | 0.8739 | +0.0000 | 0.438 | 0.4922 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5458 | 0.7432 | None / None / None |

Smallest passing AUC on this block (own draws; not compared with the other lobe): 0.6719. Row-and-column null: complete.

Permuted-block ceiling_full of rule #2.1: 0.529, 0.665, 0.688, 0.630, 0.699, 0.783, 0.628, 0.707, 0.593, 0.726, 0.627, 0.663, 0.603, 0.610, 0.634, 0.708, 0.598, 0.552, 0.675, 0.699 (real block 0.5732).

Fixed lambda = 1 on the knockout view, diagnostic, decides nothing: rule #2.1 AUC 0.5127, p_P 0.4318; BF_1 AUC 0.5127, p_P 0.4314; BF_2 AUC 0.4951, p_P 0.5309; BF_3 AUC 0.4902, p_P 0.5546; BF_4 AUC 0.5234, p_P 0.3698.

Offset, counts and sign fields: meaningless on an existence bank (in summary.json).

Check 3 (printed): present 32/64; quadrants {'ON x T4': 16, 'OFF x T5': 16, 'ON x T5': 0, 'OFF x T4': 0}; row counts {'Mi1': 4, 'Tm3': 4, 'Mi4': 4, 'Mi9': 4, 'Tm1': 4, 'Tm2': 4, 'Tm4': 4, 'Tm9': 4}; column counts {'T4a': 4, 'T4b': 4, 'T4c': 4, 'T4d': 4, 'T5a': 4, 'T5b': 4, 'T5c': 4, 'T5d': 4}; y = x * w: True; balanced: True. Check 5 (printed): D(N1 logit) = 0.0000.

## The lobe comparison (section 4.3)

Class S0: Block A is the same in both lobes at c*; the split comes from the instrument's response to the lobes' other differences (36 of 2,961 outside cells) or from the threshold of detection, not from block A. k = 0 (k* = 4), j = 0; direction L-only 0 against R-only 0 (outside: 3 against 33). Differing cells: none.

The two notions of split (S32): Split by reading (section 4.2, D3): no: G in both lobes, each with its own limits (power of the male R not calibrated; this G does not by itself exclude averaging as the explanation of flyvis-65's G). Block difference (section 4.3, by block): class S0, k = 0 of 64 cells differ. Two objects (revision 1.3): a split by reading is read as "the lobes' blocks differ" only if the section 4.3 class says so (S1, S2a, S2b); labels can differ at k = 0, and S2 may not fire when they differ. In the worlds (before unsealing): 5 of 25 dense-grid world pairs split by reading (seed 92142 U/R, seed 92161 U/G, seed 92164 U/R, seed 92172 R/U, seed 92183 W/R), 0 of 20 axis-family pairs; every world pair has k = 0 (the same board in both lobes).

## The joint reading with flyvis-65 (section 5)

flyvis-65 reads G; the male reading is G (A's D13 row: any other pair). Agreement: "not detected at the R level in the template or in either lobe of one animal, each against its own limits". The limits are not compared across banks as numbers (section 3.6). A G in the animal does not strengthen flyvis-65's G beyond its own limits. Power of the male R not calibrated; this G does not by itself exclude averaging as the explanation of flyvis-65's G.

within the animal, outside block A: the two lobes differ on 36 of 2,961 outside cells at c* (1.22 %; about 0.8 of 64 cells if spread evenly); 33 of the 36 are within a factor 2 of the cut.

Cross-lobe block weight, from the sealed files (printed after the verdicts): lobe L: # cross_lobe_block_weight_total=000000000000; lobe R: # cross_lobe_block_weight_total=000000000000.

## Pre-data tables (section 1.4)

Lobe L: inferable 64/64; mirrors [('T4a', 'Mi9'), ('T4b', 'Mi9'), ('T4c', 'Mi9')]; training present 496 of 2961; R1 and CT1(M10) rows and columns {'R1': (3, 1), 'CT1(M10)': (9, 31)}; endpoints {'Mi1': (22, 11), 'Tm3': (19, 10), 'Mi4': (17, 11), 'Mi9': (18, 13), 'Tm1': (17, 9), 'Tm2': (17, 7), 'Tm4': (16, 11), 'Tm9': (5, 5), 'T4a': (5, 9), 'T4b': (5, 8), 'T4c': (5, 9), 'T4d': (5, 8), 'T5a': (4, 7), 'T5b': (4, 8), 'T5c': (4, 8), 'T5d': (4, 9)}.

Lobe R: inferable 64/64; mirrors [('T4a', 'Mi9'), ('T4b', 'Mi9'), ('T4c', 'Mi9')]; training present 526 of 2961; R1 and CT1(M10) rows and columns {'R1': (3, 1), 'CT1(M10)': (9, 30)}; endpoints {'Mi1': (23, 11), 'Tm3': (21, 10), 'Mi4': (17, 11), 'Mi9': (20, 14), 'Tm1': (17, 9), 'Tm2': (18, 7), 'Tm4': (16, 12), 'Tm9': (5, 8), 'T4a': (6, 10), 'T4b': (5, 8), 'T4c': (5, 9), 'T4d': (5, 8), 'T5a': (4, 9), 'T5b': (4, 8), 'T5c': (4, 8), 'T5d': (4, 9)}.

Lobe agreement outside the block: both 493, L only 3, R only 33; near the cut in both lobes 33.

- FlyWire-30: 14 / 64 (provenance only (Johnny, review of 2026-09-24))
- male CNS v1.0, A's row: 64 / 64 at every pair threshold tried (Zcode, preliminary graph) (A section 1.4; a different object from this arm's row (clarification C1, section 11))
- male CNS v1.0, this arm: 64 / 64 at c* in each lobe (recomputed from the outside files at run start (check 4, section 1.4))

# Synthetic step, lobe L

## Two-world check, lobe L (section 3.6; A section 3.6)

| family | seed | label | G mechanism (description only) | rule AUC | ceiling_full | ceiling_block | n_ge / n_valid | p_S | p_P | n_deg | lambda ko | code |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R | 92100 | R | - | 1.0000 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| R | 92101 | R | - | 1.0000 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| R | 92102 | R | - | 1.0000 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| R | 92103 | R | - | 1.0000 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| R | 92104 | R | - | 0.9951 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| Nf | 92110 | G | no information (rule #2.1's ceiling_full = 0.9766 >= 0.90) | 0.5332 | 0.9766 | 1.0000 | 53 / 99 | 0.54 | 0.3196 | 0 | 100.0 | ok |
| Nf | 92111 | G | orthogonal (rule #2.1's ceiling_full = 0.4985 < 0.90) | 0.4941 | 0.4985 | 1.0000 | 51 / 99 | 0.52 | 0.5364 | 0 | 100.0 | ok |
| Nf | 92112 | G | orthogonal (rule #2.1's ceiling_full = 0.4980 < 0.90) | 0.5000 | 0.4980 | 1.0000 | 51 / 99 | 0.52 | 0.4988 | 0 | 100.0 | ok |
| Nf | 92113 | G | no information (rule #2.1's ceiling_full = 0.9941 >= 0.90) | 0.4795 | 0.9941 | 1.0000 | 56 / 99 | 0.57 | 0.6132 | 0 | 100.0 | ok |
| Nf | 92114 | G | no information (rule #2.1's ceiling_full = 0.9824 >= 0.90) | 0.5171 | 0.9824 | 1.0000 | 53 / 99 | 0.54 | 0.4131 | 0 | 100.0 | ok |
| No | 92120 | G | orthogonal (rule #2.1's ceiling_full = 0.4980 < 0.90) | 0.4854 | 0.4980 | 1.0000 | 95 / 99 | 0.96 | 0.5820 | 0 | 1.0 | ok |
| No | 92121 | G | orthogonal (rule #2.1's ceiling_full = 0.5273 < 0.90) | 0.5127 | 0.5273 | 1.0000 | 16 / 99 | 0.17 | 0.4396 | 0 | 1.0 | ok |
| No | 92122 | G | orthogonal (rule #2.1's ceiling_full = 0.5059 < 0.90) | 0.4980 | 0.5059 | 1.0000 | 93 / 99 | 0.94 | 0.5197 | 0 | 1.0 | ok |
| No | 92123 | G | orthogonal (rule #2.1's ceiling_full = 0.5059 < 0.90) | 0.5073 | 0.5059 | 1.0000 | 4 / 99 | 0.05 | 0.4634 | 0 | 1.0 | ok |
| No | 92124 | G | orthogonal (rule #2.1's ceiling_full = 0.5010 < 0.90) | 0.5010 | 0.5010 | 1.0000 | 90 / 99 | 0.91 | 0.4952 | 0 | 1.0 | ok |
| W | 92130 | W | - | 0.5205 | 0.5215 | 1.0000 | 41 / 99 | 0.42 | 0.3903 | 0 | 1.0 | ok |
| W | 92131 | W | - | 0.4980 | 0.5093 | 1.0000 | 11 / 99 | 0.12 | 0.5102 | 0 | 1.0 | ok |
| W | 92132 | W | - | 0.5146 | 0.5312 | 1.0000 | 3 / 99 | 0.04 | 0.4264 | 0 | 1.0 | ok |
| W | 92133 | W | - | 0.5215 | 0.5264 | 1.0000 | 47 / 99 | 0.48 | 0.3856 | 0 | 1.0 | ok |
| W | 92134 | W | - | 0.4795 | 0.4844 | 1.0000 | 99 / 99 | 1.00 | 0.6108 | 0 | 1.0 | ok |
| M0.5 | 92140 | G | no information (rule #2.1's ceiling_full = 0.9717 >= 0.90) | 0.5171 | 0.9717 | 1.0000 | 27 / 99 | 0.28 | 0.4162 | 0 | 100.0 | curve |
| M0.5 | 92141 | U | - | 0.6406 | 0.9990 | 1.0000 | 0 / 99 | 0.01 | 0.0276 | 0 | 3.0 | curve |
| M0.5 | 92142 | U | - | 0.6572 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0145 | 0 | 3.0 | curve |
| M0.5 | 92143 | G | no information (rule #2.1's ceiling_full = 1.0000 >= 0.90) | 0.5137 | 1.0000 | 1.0000 | 74 / 99 | 0.75 | 0.4309 | 0 | 100.0 | curve |
| M0.5 | 92144 | U | - | 0.6519 | 0.9844 | 1.0000 | 0 / 99 | 0.01 | 0.0192 | 0 | 3.0 | curve |
| M0.6 | 92160 | G | no information (rule #2.1's ceiling_full = 0.9980 >= 0.90) | 0.5674 | 0.9980 | 1.0000 | 0 / 99 | 0.01 | 0.1754 | 0 | 3.0 | curve |
| M0.6 | 92161 | U | - | 0.6436 | 0.9639 | 1.0000 | 0 / 99 | 0.01 | 0.0242 | 0 | 3.0 | curve |
| M0.6 | 92162 | R | - | 0.7402 | 0.9980 | 1.0000 | 0 / 99 | 0.01 | 0.0003 | 0 | 3.0 | curve |
| M0.6 | 92163 | U | - | 0.6572 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0142 | 0 | 3.0 | curve |
| M0.6 | 92164 | U | - | 0.6699 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0090 | 0 | 3.0 | curve |
| M0.75 | 92170 | R | - | 0.8203 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 3.0 | curve |
| M0.75 | 92171 | R | - | 0.6914 | 0.9551 | 1.0000 | 0 / 99 | 0.01 | 0.0036 | 0 | 3.0 | curve |
| M0.75 | 92172 | R | - | 0.7280 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0004 | 0 | 3.0 | curve |
| M0.75 | 92173 | U | - | 0.6802 | 0.9785 | 1.0000 | 0 / 99 | 0.01 | 0.0063 | 0 | 3.0 | curve |
| M0.75 | 92174 | R | - | 0.7178 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0014 | 0 | 3.0 | curve |
| M0.85 | 92180 | R | - | 0.8984 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |
| M0.85 | 92181 | R | - | 0.7461 | 0.9883 | 1.0000 | 0 / 99 | 0.01 | 0.0006 | 0 | 3.0 | curve |
| M0.85 | 92182 | R | - | 0.8193 | 0.9893 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |
| M0.85 | 92183 | W | - | 0.7017 | 0.9775 | 1.0000 | 1 / 99 | 0.02 | 0.0028 | 0 | 3.0 | curve |
| M0.85 | 92184 | G | no information (rule #2.1's ceiling_full = 0.9941 >= 0.90) | 0.5254 | 0.9941 | 1.0000 | 10 / 99 | 0.11 | 0.3695 | 0 | 3.0 | curve |
| M1.0 | 92150 | R | - | 0.9424 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |
| M1.0 | 92151 | R | - | 0.9697 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |
| M1.0 | 92152 | R | - | 0.8389 | 0.9980 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |
| M1.0 | 92153 | R | - | 0.9492 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |
| M1.0 | 92154 | R | - | 0.7920 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 3.0 | curve |

| family | requirement | labels read (R/W/G/U) | meet (min) | stop labels | result |
|---|---|---|---|---|---|
| R | each of 5 worlds reads R, on both D1 candidates | 5/0/0/0 | 5/5 (5) | 0 | no stop |
| Nf | never R or W (stop); at least 3 of 5 read G | 0/0/5/0 | 5/5 (3) | 0 | no stop |
| No | never R or W (stop); reads G; a U triggers the No contingency | 0/0/5/0 | 5/5 (0) | 0 | no stop |
| W | each of 5 worlds reads W, on both D1 candidates | 0/5/0/0 | 5/5 (5) | 0 | no stop |
| M0.5 | power curve: printed, no stop row; the three limits are taken from it | 0/0/2/3 | n/a (power curve) | 0 | no stop |
| M0.6 | power curve: printed, no stop row; the three limits are taken from it | 1/0/1/3 | n/a (power curve) | 0 | no stop |
| M0.75 | power curve: printed, no stop row; the three limits are taken from it | 4/0/0/1 | n/a (power curve) | 0 | no stop |
| M0.85 | power curve: printed, no stop row; the three limits are taken from it | 3/1/1/0 | n/a (power curve) | 0 | no stop |
| M1.0 | power curve: printed, no stop row; the three limits are taken from it | 5/0/0/0 | n/a (power curve) | 0 | no stop |

Pre-run table (section 7, revisions 3.2, 3.3): outcome 1: every deciding column equal; byte-identical (recorded, not gated); rows matched by family/j/seed/predictor: 0 missing now, 0 missing in the pre-run table, row order equal (a fact, not an outcome); mechanism_description differs on 0 rows (reported, not gated) (passed: True; byte-identical: True; pinned 506576312638005e5bd09876c9da0ffe9a8a753641a59a2b354c0c59bed25d91, recomputed 506576312638005e5bd09876c9da0ffe9a8a753641a59a2b354c0c59bed25d91).

Per-fit diagnostic against the lobe's pre-run raw fits (diagnostic, decides nothing): {'pinned': 28665, 'missing_now': 0, 'compared': 28665, 'fitted_this_pass': 28665, 'p_differ': 0, 'lambda_differ': 0, 'labels_differ': 0, 'score_differ': 0, 'outside_density_differ': 0, 'reused_from_ko_differ': 0, 'max_abs_dp': 0.0}; by kind {'pc': 900, 'block': 270, 'sh': 26730, 'ko': 270, 'full': 270, 'ko1': 225}.

Two-world check passed: True. No contingency triggered: False.

## Power curve and the three limits (section 3.6, revision 3.1)

| gamma | family | seen/n (rule #2.1 p_P <= 0.01) | R/n | seen/n BF_1, BF_2, BF_3, BF_4 | R/W/G/U | rule AUC | rule lambda ko |
|---|---|---|---|---|---|---|---|
| 0.0 | Nf (anchor) | 0/5 | 0/5 | 0/5, 0/5, 0/5, 0/5 | 0/0/5/0 | 0.533, 0.494, 0.500, 0.479, 0.517 | 100, 100, 100, 100, 100 |
| 0.5 | M0.5 | 0/5 | 0/5 | 2/5, 0/5, 0/5, 0/5 | 0/0/2/3 | 0.517, 0.641, 0.657, 0.514, 0.652 | 100, 3, 3, 100, 3 |
| 0.6 | M0.6 | 2/5 | 1/5 | 2/5, 1/5, 1/5, 1/5 | 1/0/1/3 | 0.567, 0.644, 0.740, 0.657, 0.670 | 3, 3, 3, 3, 3 |
| 0.75 | M0.75 | 5/5 | 4/5 | 4/5, 4/5, 3/5, 3/5 | 4/0/0/1 | 0.820, 0.691, 0.728, 0.680, 0.718 | 3, 3, 3, 3, 3 |
| 0.85 | M0.85 | 4/5 | 3/5 | 4/5, 4/5, 4/5, 4/5 | 3/1/1/0 | 0.898, 0.746, 0.819, 0.702, 0.525 | 1, 3, 1, 3, 3 |
| 1.0 | M1.0 | 5/5 | 5/5 | 5/5, 5/5, 5/5, 5/5 | 5/0/0/0 | 0.942, 0.970, 0.839, 0.949, 0.792 | 1, 1, 1, 1, 3 |
| 2.0 | R (anchor) | 5/5 | 5/5 | 5/5, 5/5, 5/5, 5/5 | 5/0/0/0 | 1.000, 1.000, 1.000, 1.000, 0.995 | 1, 1, 1, 1, 1 |

**The three limits** (in M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10):

- gamma*_P, the leg-P limit (rule #2.1 p_P <= 0.01 in a majority of the worlds): **0.75**, bracket (0.6, 0.75]; majority seen at every grid gamma above it: True.
- gamma_R (a majority of the worlds read R): **0.75**, bracket (0.6, 0.75]; majority R at every grid gamma above it: True.
- family limit (the largest leg-P limit: the maximum of each predictor's own leg-P limit): **0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4)**. Per predictor: rule #2.1 0.75, BF_1 0.75, BF_2 0.75, BF_3 0.75, BF_4 0.75. The limits use p_P <= 0.01 for every predictor and are not family-corrected, unlike the W gate (p_P <= 0.0125 = 0.05/4): a limit is a property of the instrument, not of a branch (revision 3.2).
- transition band [gamma*_P, gamma_R): empty: the two limits coincide (0 grid steps, 0 in gamma). Dense-grid worlds that read U: 0 inside the band, 6 below it, 1 above it. The band is the difference of two limits, each uncertain by about one grid step, so a one-step band is one of 0, 1 or 2 steps (revision 3.2).
- per gamma, seen/n and R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5.
- binomial note: with n = 5 worlds per gamma a limit has an error of about one grid step: a true detection probability of 0.2 or 0.4 gives '>= 3 of 5' with probability 0.06 or 0.32 (Johnny).
- M worlds that read G at or above gamma*_P: 1 (M0.85 92184); at or above gamma_R: 1 (M0.85 92184) (printed, no stop).
- grid complete: True.

**U rule:** threshold U read by 7 of 25 dense-grid worlds (7 threshold U, 0 failed fit, 0 ceiling_block not measured, 0 not readable): U stays; its frequency is printed. U is read as 'on the detection threshold; cannot be separated', the signature of the leg-P detection limit gamma*_P (revisions 3.1, 3.2), except a U whose reasons include rule #2.1's ceiling_block below 0.90, which reads 'failed fit: rule #2.1 cannot hold the block even when trained on it alone', and a U whose ceiling_block was not measured, which reads 'not measured: rule #2.1's ceiling_block was not measured; the G gate cannot be read' (revision 3.3). U across all 45 worlds: 7 (R 0/5, Nf 0/5, No 0/5, W 0/5, M0.5 3/5, M1.0 0/5, M0.6 3/5, M0.75 1/5, M0.85 0/5).

## Fixed lambda = 1 on the knockout view (section 3.5): diagnostic, decides nothing

Printed beside the limits, not on any verdict line. Where the selected lambda was 1 the selected fit is reused (path check: {'bank': 'world:W:0', 'identical': {'rule': True, 'BF:1': True, 'BF:2': True, 'BF:3': True, 'BF:4': True}, 'passed': True}).

| family | predictor | AUC at lambda 1 (per world) | mean | p_P <= 0.01 at lambda 1 | selected lambda | mean AUC selected | p_P <= 0.01 selected |
|---|---|---|---|---|---|---|---|
| R | rule #2.1 | 1.000, 1.000, 1.000, 1.000, 0.995 | 0.999 | 5/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.999 | 5/5 |
| R | BF_1 | 1.000, 1.000, 1.000, 1.000, 0.993 | 0.999 | 5/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.999 | 5/5 |
| R | BF_2 | 0.998, 1.000, 1.000, 0.977, 0.987 | 0.992 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.994 | 5/5 |
| R | BF_3 | 0.992, 0.987, 0.994, 0.943, 0.972 | 0.978 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.993 | 5/5 |
| R | BF_4 | 0.991, 0.984, 0.983, 0.971, 0.990 | 0.984 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.994 | 5/5 |
| Nf | rule #2.1 | 0.536, 0.500, 0.494, 0.499, 0.577 | 0.521 | 0/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.505 | 0/5 |
| Nf | BF_1 | 0.520, 0.482, 0.507, 0.488, 0.573 | 0.514 | 0/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.505 | 0/5 |
| Nf | BF_2 | 0.548, 0.475, 0.512, 0.509, 0.598 | 0.528 | 0/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.505 | 0/5 |
| Nf | BF_3 | 0.529, 0.556, 0.513, 0.479, 0.604 | 0.536 | 0/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.505 | 0/5 |
| Nf | BF_4 | 0.504, 0.429, 0.458, 0.479, 0.582 | 0.490 | 0/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.505 | 0/5 |
| No | rule #2.1 | 0.485, 0.513, 0.498, 0.507, 0.501 | 0.501 | 0/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.501 | 0/5 |
| No | BF_1 | 0.489, 0.511, 0.498, 0.510, 0.497 | 0.501 | 0/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.501 | 0/5 |
| No | BF_2 | 0.480, 0.502, 0.500, 0.530, 0.507 | 0.504 | 0/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.503 | 0/5 |
| No | BF_3 | 0.505, 0.497, 0.499, 0.516, 0.496 | 0.503 | 0/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.501 | 0/5 |
| No | BF_4 | 0.488, 0.520, 0.499, 0.488, 0.483 | 0.496 | 0/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.497 | 0/5 |
| W | rule #2.1 | 0.521, 0.498, 0.515, 0.521, 0.479 | 0.507 | 0/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.507 | 0/5 |
| W | BF_1 | 0.526, 0.490, 0.513, 0.521, 0.489 | 0.508 | 0/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.508 | 0/5 |
| W | BF_2 | 0.779, 0.798, 0.763, 0.723, 0.721 | 0.757 | 5/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.757 | 5/5 |
| W | BF_3 | 0.767, 0.816, 0.780, 0.690, 0.592 | 0.729 | 4/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.729 | 4/5 |
| W | BF_4 | 0.761, 0.825, 0.739, 0.681, 0.575 | 0.716 | 4/5 | 1.0, 3.0, 3.0, 3.0, 1.0 | 0.705 | 4/5 |
| M0.5 | rule #2.1 | 0.509, 0.775, 0.740, 0.688, 0.724 | 0.687 | 4/5 | 100.0, 3.0, 3.0, 100.0, 3.0 | 0.596 | 0/5 |
| M0.5 | BF_1 | 0.500, 0.768, 0.775, 0.679, 0.721 | 0.688 | 4/5 | 100.0, 3.0, 3.0, 100.0, 3.0 | 0.610 | 2/5 |
| M0.5 | BF_2 | 0.564, 0.751, 0.668, 0.375, 0.714 | 0.614 | 3/5 | 100.0, 100.0, 100.0, 100.0, 3.0 | 0.531 | 0/5 |
| M0.5 | BF_3 | 0.552, 0.597, 0.757, 0.390, 0.697 | 0.598 | 2/5 | 100.0, 100.0, 100.0, 100.0, 3.0 | 0.536 | 0/5 |
| M0.5 | BF_4 | 0.549, 0.558, 0.730, 0.441, 0.661 | 0.588 | 1/5 | 100.0, 100.0, 100.0, 100.0, 3.0 | 0.536 | 0/5 |
| M1.0 | rule #2.1 | 0.942, 0.970, 0.839, 0.949, 0.929 | 0.926 | 5/5 | 1.0, 1.0, 1.0, 1.0, 3.0 | 0.898 | 5/5 |
| M1.0 | BF_1 | 0.945, 0.973, 0.840, 0.948, 0.928 | 0.927 | 5/5 | 3.0, 1.0, 1.0, 3.0, 3.0 | 0.864 | 5/5 |
| M1.0 | BF_2 | 0.776, 0.929, 0.818, 0.923, 0.822 | 0.854 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.816 | 5/5 |
| M1.0 | BF_3 | 0.792, 0.885, 0.791, 0.924, 0.821 | 0.843 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.817 | 5/5 |
| M1.0 | BF_4 | 0.786, 0.922, 0.737, 0.926, 0.816 | 0.838 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.811 | 5/5 |
| M0.6 | rule #2.1 | 0.620, 0.709, 0.854, 0.774, 0.760 | 0.743 | 4/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.656 | 2/5 |
| M0.6 | BF_1 | 0.649, 0.714, 0.834, 0.771, 0.761 | 0.746 | 4/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.655 | 2/5 |
| M0.6 | BF_2 | 0.669, 0.588, 0.815, 0.734, 0.749 | 0.711 | 3/5 | 3.0, 3.0, 3.0, 3.0, 100.0 | 0.608 | 1/5 |
| M0.6 | BF_3 | 0.651, 0.562, 0.781, 0.760, 0.724 | 0.696 | 3/5 | 100.0, 3.0, 3.0, 3.0, 100.0 | 0.585 | 1/5 |
| M0.6 | BF_4 | 0.650, 0.522, 0.757, 0.729, 0.668 | 0.665 | 2/5 | 100.0, 3.0, 3.0, 3.0, 100.0 | 0.584 | 1/5 |
| M0.75 | rule #2.1 | 0.923, 0.746, 0.821, 0.770, 0.740 | 0.800 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.728 | 5/5 |
| M0.75 | BF_1 | 0.896, 0.735, 0.813, 0.749, 0.759 | 0.791 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.719 | 4/5 |
| M0.75 | BF_2 | 0.854, 0.738, 0.729, 0.662, 0.733 | 0.743 | 4/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.699 | 4/5 |
| M0.75 | BF_3 | 0.780, 0.695, 0.750, 0.611, 0.564 | 0.680 | 3/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.683 | 3/5 |
| M0.75 | BF_4 | 0.755, 0.690, 0.720, 0.633, 0.573 | 0.674 | 3/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.679 | 3/5 |
| M0.85 | rule #2.1 | 0.898, 0.809, 0.819, 0.785, 0.568 | 0.776 | 4/5 | 1.0, 3.0, 1.0, 3.0, 3.0 | 0.738 | 4/5 |
| M0.85 | BF_1 | 0.885, 0.827, 0.813, 0.763, 0.555 | 0.769 | 4/5 | 1.0, 3.0, 3.0, 3.0, 3.0 | 0.725 | 4/5 |
| M0.85 | BF_2 | 0.838, 0.822, 0.796, 0.731, 0.562 | 0.750 | 4/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.711 | 4/5 |
| M0.85 | BF_3 | 0.805, 0.820, 0.792, 0.769, 0.550 | 0.747 | 4/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.719 | 4/5 |
| M0.85 | BF_4 | 0.810, 0.790, 0.760, 0.725, 0.548 | 0.726 | 4/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.707 | 4/5 |

Fits: 0 re-read from saved fits, 28440 new world fits, fixed lambda: 46 reused, 174 fitted.

### World R, seed 92100: R: regrows

Outside density 0.2857; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 1.0000 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 1.0000 (32/32) | 3.626 | 0.2750 | +0.4960 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 1.0000 (32/32) | 3.229 | 0.2601 | +0.5109 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.9961 (32/32) | 2.400 | 0.3340 | +0.4369 | 0.969 | 1.0000 | 1.0000 | 0.99 | 0.99 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.9932 (32/32) | 2.303 | 0.3462 | +0.4247 | 0.969 | 1.0000 | 1.0000 | 0.99 | 0.99 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.9941 (32/32) | 2.315 | 0.3456 | +0.4253 | 0.969 | 1.0000 | 1.0000 | 0.99 | 0.99 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4932 (32/32) | 0.000 | 0.7709 | +0.0000 | 0.500 | 0.4932 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5420 | 0.6700 | None / None / None |

### World R, seed 92101: R: regrows

Outside density 0.2773; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 1.0000 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 1.0000 (32/32) | 3.402 | 0.2759 | +0.4824 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 1.0000 (32/32) | 2.982 | 0.2735 | +0.4847 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 1.0000 (32/32) | 2.208 | 0.3518 | +0.4064 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.9980 (32/32) | 2.175 | 0.3580 | +0.4002 | 0.969 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.9980 (32/32) | 2.204 | 0.3551 | +0.4032 | 0.969 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5352 (32/32) | 0.000 | 0.7583 | +0.0000 | 0.531 | 0.5293 | 0.5000 | 1.20 | n/a | 99 / 99 | 1.00 | 0.3113 | 0.0199 | None / None / None |

### World R, seed 92102: R: regrows

Outside density 0.2705; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 1.0000 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 1.0000 (32/32) | 2.918 | 0.3765 | +0.4433 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 1.0000 (32/32) | 2.597 | 0.3532 | +0.4667 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 1.0000 (32/32) | 1.972 | 0.4310 | +0.3888 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 1.0000 (32/32) | 1.957 | 0.4400 | +0.3798 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.9990 (32/32) | 1.942 | 0.4445 | +0.3754 | 0.969 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4883 (32/32) | 0.000 | 0.8198 | +0.0000 | 0.469 | 0.4883 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5698 | 0.7541 | None / None / None |

### World R, seed 92103: R: regrows

Outside density 0.2746; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 1.0000 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 1.0000 (32/32) | 3.369 | 0.2973 | +0.4801 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 1.0000 (32/32) | 2.909 | 0.2785 | +0.4989 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.9990 (32/32) | 2.228 | 0.3619 | +0.4155 | 0.969 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.9941 (32/32) | 2.080 | 0.3862 | +0.3912 | 0.969 | 1.0000 | 1.0000 | 0.99 | 0.99 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.9941 (32/32) | 2.039 | 0.3929 | +0.3845 | 0.969 | 1.0000 | 1.0000 | 0.99 | 0.99 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4951 (32/32) | 0.000 | 0.7774 | +0.0000 | 0.469 | 0.4971 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5298 | 0.6687 | None / None / None |

### World R, seed 92104: R: regrows

Outside density 0.2918; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.9951 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.9951 (32/32) | 3.135 | 0.3072 | +0.4599 | 0.969 | 1.0000 | 1.0000 | 0.99 | 0.99 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.9932 (32/32) | 2.864 | 0.2954 | +0.4717 | 0.969 | 1.0000 | 1.0000 | 0.99 | 0.99 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.9727 (32/32) | 2.146 | 0.3733 | +0.3937 | 0.969 | 1.0000 | 1.0000 | 0.95 | 0.95 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.9775 (32/32) | 2.164 | 0.3680 | +0.3991 | 0.969 | 1.0000 | 1.0000 | 0.96 | 0.96 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.9854 (32/32) | 2.272 | 0.3559 | +0.4111 | 0.969 | 1.0000 | 1.0000 | 0.97 | 0.97 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5117 (32/32) | 0.000 | 0.7670 | +0.0000 | 0.531 | 0.5107 | 0.5000 | 1.09 | n/a | 99 / 99 | 1.00 | 0.4406 | 0.2872 | None / None / None |

### World Nf, seed 92110: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1733; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 0.9766 >= 0.90)]. rule #2.1: AUC = 0.5332 (32/32), p_S = 0.54 (n_ge = 53 of 99, n_deg = 0), p_P = 0.3196; ceiling_full = 0.9766, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5332 (32/32) | 0.000 | 0.9198 | -0.0042 | 0.531 | 0.9766 | 1.0000 | 0.07 | 0.07 | 53 / 99 | 0.54 | 0.3196 | 0.0451 | 100.0 / 3.0 / 1.0 |
| BF_1 | 0.5312 (32/32) | 0.000 | 0.9156 | +0.0000 | 0.531 | 0.9893 | 1.0000 | 0.06 | 0.06 | 97 / 99 | 0.98 | 0.3321 | 0.0544 | 100.0 / 3.0 / 1.0 |
| BF_2 | 0.5312 (32/32) | 0.000 | 0.9156 | +0.0000 | 0.531 | 0.9941 | 1.0000 | 0.06 | 0.06 | 99 / 99 | 1.00 | 0.3321 | 0.0544 | 100.0 / 3.0 / 1.0 |
| BF_3 | 0.5312 (32/32) | 0.000 | 0.9156 | +0.0000 | 0.531 | 0.5283 | 1.0000 | 1.10 | 0.06 | 99 / 99 | 1.00 | 0.3321 | 0.0544 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.5312 (32/32) | 0.000 | 0.9156 | +0.0000 | 0.531 | 0.5283 | 1.0000 | 1.10 | 0.06 | 98 / 99 | 0.99 | 0.3321 | 0.0544 | 100.0 / 100.0 / 1.0 |
| N1 | 0.5312 (32/32) | 0.000 | 0.9156 | +0.0000 | 0.531 | 0.5283 | 0.5000 | 1.10 | n/a | 99 / 99 | 1.00 | 0.3321 | 0.0544 | None / None / None |

### World Nf, seed 92111: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1749; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.4985 < 0.90)]. rule #2.1: AUC = 0.4941 (32/32), p_S = 0.52 (n_ge = 51 of 99, n_deg = 0), p_P = 0.5364; ceiling_full = 0.4985, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4941 (32/32) | 0.000 | 0.8597 | +0.0027 | 0.500 | 0.4985 | 1.0000 | n/a | -0.01 | 51 / 99 | 0.52 | 0.5364 | 0.6153 | 100.0 / 100.0 / 1.0 |
| BF_1 | 0.4912 (32/32) | 0.000 | 0.8624 | +0.0000 | 0.500 | 0.4922 | 1.0000 | n/a | -0.02 | 97 / 99 | 0.98 | 0.5518 | 0.6704 | 100.0 / 100.0 / 1.0 |
| BF_2 | 0.4912 (32/32) | 0.000 | 0.8624 | +0.0000 | 0.500 | 0.4922 | 1.0000 | n/a | -0.02 | 99 / 99 | 1.00 | 0.5518 | 0.6704 | 100.0 / 100.0 / 1.0 |
| BF_3 | 0.4912 (32/32) | 0.000 | 0.8624 | +0.0000 | 0.500 | 0.4922 | 1.0000 | n/a | -0.02 | 98 / 99 | 0.99 | 0.5518 | 0.6704 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.4912 (32/32) | 0.000 | 0.8624 | +0.0000 | 0.500 | 0.4922 | 1.0000 | n/a | -0.02 | 99 / 99 | 1.00 | 0.5518 | 0.6704 | 100.0 / 100.0 / 1.0 |
| N1 | 0.4912 (32/32) | 0.000 | 0.8624 | +0.0000 | 0.500 | 0.4922 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5518 | 0.6704 | None / None / None |

### World Nf, seed 92112: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1736; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.4980 < 0.90)]. rule #2.1: AUC = 0.5000 (32/32), p_S = 0.52 (n_ge = 51 of 99, n_deg = 0), p_P = 0.4988; ceiling_full = 0.4980, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5000 (32/32) | 0.000 | 0.8736 | +0.0073 | 0.469 | 0.4980 | 1.0000 | n/a | 0.00 | 51 / 99 | 0.52 | 0.4988 | 0.5179 | 100.0 / 100.0 / 1.0 |
| BF_1 | 0.5029 (32/32) | 0.000 | 0.8809 | +0.0000 | 0.469 | 0.5029 | 1.0000 | 1.00 | 0.01 | 96 / 99 | 0.97 | 0.4862 | 0.4680 | 100.0 / 100.0 / 1.0 |
| BF_2 | 0.5029 (32/32) | 0.000 | 0.8809 | +0.0000 | 0.469 | 0.5029 | 1.0000 | 1.00 | 0.01 | 99 / 99 | 1.00 | 0.4862 | 0.4680 | 100.0 / 100.0 / 1.0 |
| BF_3 | 0.5029 (32/32) | 0.000 | 0.8809 | +0.0000 | 0.469 | 0.5029 | 1.0000 | 1.00 | 0.01 | 98 / 99 | 0.99 | 0.4862 | 0.4680 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.5029 (32/32) | 0.000 | 0.8809 | +0.0000 | 0.469 | 0.5029 | 1.0000 | 1.00 | 0.01 | 99 / 99 | 1.00 | 0.4862 | 0.4680 | 100.0 / 100.0 / 1.0 |
| N1 | 0.5029 (32/32) | 0.000 | 0.8809 | +0.0000 | 0.469 | 0.5029 | 0.5000 | 1.00 | n/a | 99 / 99 | 1.00 | 0.4862 | 0.4680 | None / None / None |

### World Nf, seed 92113: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1743; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 0.9941 >= 0.90)]. rule #2.1: AUC = 0.4795 (32/32), p_S = 0.57 (n_ge = 56 of 99, n_deg = 0), p_P = 0.6132; ceiling_full = 0.9941, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4795 (32/32) | 0.000 | 0.8822 | +0.0147 | 0.562 | 0.9941 | 1.0000 | -0.04 | -0.04 | 56 / 99 | 0.57 | 0.6132 | 0.9569 | 100.0 / 3.0 / 1.0 |
| BF_1 | 0.4824 (32/32) | 0.000 | 0.8969 | +0.0000 | 0.500 | 0.9912 | 1.0000 | -0.04 | -0.04 | 96 / 99 | 0.97 | 0.5998 | 0.9315 | 100.0 / 3.0 / 1.0 |
| BF_2 | 0.4824 (32/32) | 0.000 | 0.8969 | +0.0000 | 0.500 | 0.9932 | 1.0000 | -0.04 | -0.04 | 96 / 99 | 0.97 | 0.5998 | 0.9315 | 100.0 / 3.0 / 1.0 |
| BF_3 | 0.4824 (32/32) | 0.000 | 0.8969 | +0.0000 | 0.500 | 0.4785 | 1.0000 | n/a | -0.04 | 96 / 99 | 0.97 | 0.5998 | 0.9315 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.4824 (32/32) | 0.000 | 0.8969 | +0.0000 | 0.500 | 0.4785 | 1.0000 | n/a | -0.04 | 97 / 99 | 0.98 | 0.5998 | 0.9315 | 100.0 / 100.0 / 1.0 |
| N1 | 0.4824 (32/32) | 0.000 | 0.8969 | +0.0000 | 0.500 | 0.4785 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5998 | 0.9315 | None / None / None |

### World Nf, seed 92114: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1662; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 0.9824 >= 0.90)]. rule #2.1: AUC = 0.5171 (32/32), p_S = 0.54 (n_ge = 53 of 99, n_deg = 0), p_P = 0.4131; ceiling_full = 0.9824, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5171 (32/32) | 0.000 | 0.9170 | +0.0040 | 0.500 | 0.9824 | 1.0000 | 0.04 | 0.03 | 53 / 99 | 0.54 | 0.4131 | 0.2049 | 100.0 / 3.0 / 1.0 |
| BF_1 | 0.5186 (32/32) | 0.000 | 0.9210 | +0.0000 | 0.500 | 0.9824 | 1.0000 | 0.04 | 0.04 | 96 / 99 | 0.97 | 0.4065 | 0.1843 | 100.0 / 3.0 / 1.0 |
| BF_2 | 0.5186 (32/32) | 0.000 | 0.9210 | +0.0000 | 0.500 | 0.9814 | 1.0000 | 0.04 | 0.04 | 97 / 99 | 0.98 | 0.4065 | 0.1843 | 100.0 / 3.0 / 1.0 |
| BF_3 | 0.5186 (32/32) | 0.000 | 0.9210 | +0.0000 | 0.500 | 0.5117 | 1.0000 | 1.58 | 0.04 | 98 / 99 | 0.99 | 0.4065 | 0.1843 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.5186 (32/32) | 0.000 | 0.9210 | +0.0000 | 0.500 | 0.5117 | 1.0000 | 1.58 | 0.04 | 98 / 99 | 0.99 | 0.4065 | 0.1843 | 100.0 / 100.0 / 1.0 |
| N1 | 0.5186 (32/32) | 0.000 | 0.9210 | +0.0000 | 0.500 | 0.5117 | 0.5000 | 1.58 | n/a | 99 / 99 | 1.00 | 0.4065 | 0.1843 | None / None / None |

### World No, seed 92120: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.2955; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.4980 < 0.90)]. rule #2.1: AUC = 0.4854 (32/32), p_S = 0.96 (n_ge = 95 of 99, n_deg = 0), p_P = 0.5820; ceiling_full = 0.4980, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4854 (32/32) | -0.039 | 1.2832 | -0.4643 | 0.500 | 0.4980 | 1.0000 | n/a | -0.03 | 95 / 99 | 0.96 | 0.5820 | 0.5808 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.4893 (32/32) | -0.042 | 1.1091 | -0.2902 | 0.500 | 0.4971 | 1.0000 | n/a | -0.02 | 97 / 99 | 0.98 | 0.5626 | 0.5614 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.4990 (32/32) | -0.039 | 0.9785 | -0.1596 | 0.531 | 0.8574 | 1.0000 | -0.00 | -0.00 | 99 / 99 | 1.00 | 0.5090 | 0.5091 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5107 (32/32) | -0.034 | 0.9806 | -0.1618 | 0.531 | 0.9062 | 1.0000 | 0.03 | 0.02 | 0 / 99 | 0.01 | 0.4501 | 0.4442 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.5098 (32/32) | -0.037 | 0.9867 | -0.1679 | 0.531 | 0.9111 | 1.0000 | 0.02 | 0.02 | 0 / 99 | 0.01 | 0.4543 | 0.4488 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5039 (32/32) | 0.000 | 0.8188 | +0.0000 | 0.531 | 0.5039 | 0.5000 | 1.00 | n/a | 99 / 99 | 1.00 | 0.4810 | 0.4063 | None / None / None |

### World No, seed 92121: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.2837; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5273 < 0.90)]. rule #2.1: AUC = 0.5127 (32/32), p_S = 0.17 (n_ge = 16 of 99, n_deg = 0), p_P = 0.4396; ceiling_full = 0.5273, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5127 (32/32) | 0.042 | 1.1484 | -0.3261 | 0.500 | 0.5273 | 1.0000 | 0.46 | 0.03 | 16 / 99 | 0.17 | 0.4396 | 0.4318 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5107 (32/32) | 0.044 | 1.0331 | -0.2108 | 0.500 | 0.5137 | 1.0000 | 0.79 | 0.02 | 2 / 99 | 0.03 | 0.4478 | 0.4446 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.4941 (32/32) | -0.013 | 0.9427 | -0.1204 | 0.469 | 0.8867 | 1.0000 | -0.02 | -0.01 | 99 / 99 | 1.00 | 0.5352 | 0.5482 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.4854 (32/32) | -0.038 | 0.9484 | -0.1261 | 0.469 | 0.9131 | 1.0000 | -0.04 | -0.03 | 99 / 99 | 1.00 | 0.5842 | 0.6007 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.4941 (32/32) | -0.031 | 0.9320 | -0.1097 | 0.469 | 0.9297 | 1.0000 | -0.01 | -0.01 | 99 / 99 | 1.00 | 0.5360 | 0.5384 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5049 (32/32) | 0.000 | 0.8223 | +0.0000 | 0.438 | 0.5059 | 0.5000 | 0.83 | n/a | 99 / 99 | 1.00 | 0.4809 | 0.3679 | None / None / None |

### World No, seed 92122: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.2783; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5059 < 0.90)]. rule #2.1: AUC = 0.4980 (32/32), p_S = 0.94 (n_ge = 93 of 99, n_deg = 0), p_P = 0.5197; ceiling_full = 0.5059, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4980 (32/32) | -0.011 | 1.1996 | -0.4587 | 0.500 | 0.5059 | 1.0000 | -0.33 | -0.00 | 93 / 99 | 0.94 | 0.5197 | 0.5117 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.4980 (32/32) | -0.017 | 1.0637 | -0.3228 | 0.500 | 0.4990 | 1.0000 | n/a | -0.00 | 98 / 99 | 0.99 | 0.5199 | 0.5118 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.5029 (32/32) | -0.005 | 0.9301 | -0.1891 | 0.500 | 0.8838 | 1.0000 | 0.01 | 0.01 | 99 / 99 | 1.00 | 0.4936 | 0.4843 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5010 (32/32) | -0.014 | 0.9336 | -0.1927 | 0.500 | 0.9023 | 1.0000 | 0.00 | 0.00 | 99 / 99 | 1.00 | 0.5015 | 0.5004 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.4980 (32/32) | -0.014 | 0.9283 | -0.1873 | 0.500 | 0.9102 | 1.0000 | -0.00 | -0.00 | 99 / 99 | 1.00 | 0.5237 | 0.5171 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5127 (32/32) | 0.000 | 0.7409 | +0.0000 | 0.531 | 0.5127 | 0.5000 | 1.00 | n/a | 99 / 99 | 1.00 | 0.4300 | 0.0642 | None / None / None |

### World No, seed 92123: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.2918; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5059 < 0.90)]. rule #2.1: AUC = 0.5073 (32/32), p_S = 0.05 (n_ge = 4 of 99, n_deg = 0), p_P = 0.4634; ceiling_full = 0.5059, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5073 (32/32) | -0.010 | 1.1228 | -0.3238 | 0.500 | 0.5059 | 1.0000 | 1.25 | 0.01 | 4 / 99 | 0.05 | 0.4634 | 0.4655 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5098 (32/32) | -0.008 | 1.0232 | -0.2242 | 0.500 | 0.5059 | 1.0000 | 1.67 | 0.02 | 0 / 99 | 0.01 | 0.4521 | 0.4543 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.5107 (32/32) | 0.053 | 0.9025 | -0.1035 | 0.500 | 0.9707 | 1.0000 | 0.02 | 0.02 | 0 / 99 | 0.01 | 0.4497 | 0.4470 | 3.0 / 1.0 / 1.0 |
| BF_3 | 0.5098 (32/32) | 0.048 | 0.9061 | -0.1072 | 0.500 | 0.9121 | 1.0000 | 0.02 | 0.02 | 0 / 99 | 0.01 | 0.4504 | 0.4541 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.4912 (32/32) | 0.013 | 0.9153 | -0.1163 | 0.500 | 0.9346 | 1.0000 | -0.02 | -0.02 | 0 / 99 | 0.01 | 0.5556 | 0.5547 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4824 (32/32) | 0.000 | 0.7989 | +0.0000 | 0.469 | 0.4814 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5952 | 0.9381 | None / None / None |

### World No, seed 92124: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.2725; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5010 < 0.90)]. rule #2.1: AUC = 0.5010 (32/32), p_S = 0.91 (n_ge = 90 of 99, n_deg = 0), p_P = 0.4952; ceiling_full = 0.5010, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5010 (32/32) | 0.006 | 1.1473 | -0.3722 | 0.500 | 0.5010 | 1.0000 | 1.00 | 0.00 | 90 / 99 | 0.91 | 0.4952 | 0.4975 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.4971 (32/32) | 0.006 | 0.9987 | -0.2237 | 0.500 | 0.4932 | 1.0000 | n/a | -0.01 | 99 / 99 | 1.00 | 0.5164 | 0.5159 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.5088 (32/32) | 0.006 | 0.9117 | -0.1366 | 0.500 | 0.9209 | 1.0000 | 0.02 | 0.02 | 99 / 99 | 1.00 | 0.4539 | 0.4417 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.4990 (32/32) | -0.010 | 0.9217 | -0.1467 | 0.500 | 0.9316 | 1.0000 | -0.00 | -0.00 | 99 / 99 | 1.00 | 0.5075 | 0.5093 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.4941 (32/32) | -0.018 | 0.9270 | -0.1519 | 0.500 | 0.9326 | 1.0000 | -0.01 | -0.01 | 99 / 99 | 1.00 | 0.5344 | 0.5382 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5176 (32/32) | 0.000 | 0.7750 | +0.0000 | 0.500 | 0.5176 | 0.5000 | 1.00 | n/a | 99 / 99 | 1.00 | 0.3996 | 0.0963 | None / None / None |

### World W, seed 92130: W: rule weaker than the information available

Outside density 0.3310; block present 32.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.5205 (32/32), p_S = 0.42 (n_ge = 41 of 99, n_deg = 0), p_P = 0.3903; ceiling_full = 0.5215, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 1.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5205 (32/32) | 0.206 | 0.9265 | -0.2022 | 0.500 | 0.5215 | 1.0000 | 0.95 | 0.04 | 41 / 99 | 0.42 | 0.3903 | 0.4091 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5264 (32/32) | 0.183 | 0.8765 | -0.1522 | 0.500 | 0.5293 | 1.0000 | 0.90 | 0.05 | 3 / 99 | 0.04 | 0.3601 | 0.3782 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7793 (32/32) | 2.254 | 0.5748 | +0.1495 | 0.594 | 0.9717 | 1.0000 | 0.59 | 0.56 | 0 / 99 | 0.01 | 0.0001 | 0.0004 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.7666 (32/32) | 2.126 | 0.6535 | +0.0708 | 0.656 | 0.9785 | 1.0000 | 0.56 | 0.53 | 0 / 99 | 0.01 | 0.0001 | 0.0006 | 1.0 / 1.0 / 1.0 |
| BF_4 | 0.7607 (32/32) | 2.103 | 0.6759 | +0.0484 | 0.656 | 0.9854 | 1.0000 | 0.54 | 0.52 | 0 / 99 | 0.01 | 0.0001 | 0.0006 | 1.0 / 1.0 / 1.0 |
| N1 | 0.5176 (32/32) | 0.000 | 0.7243 | +0.0000 | 0.531 | 0.5166 | 0.5000 | 1.06 | n/a | 99 / 99 | 1.00 | 0.4139 | 0.0994 | None / None / None |

### World W, seed 92131: W: rule weaker than the information available

Outside density 0.3188; block present 32.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.4980 (32/32), p_S = 0.12 (n_ge = 11 of 99, n_deg = 0), p_P = 0.5102; ceiling_full = 0.5093, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4980 (32/32) | 0.009 | 1.0298 | -0.2683 | 0.500 | 0.5093 | 1.0000 | -0.21 | -0.00 | 11 / 99 | 0.12 | 0.5102 | 0.5186 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.4902 (32/32) | 0.014 | 0.9342 | -0.1728 | 0.500 | 0.4941 | 1.0000 | n/a | -0.02 | 2 / 99 | 0.03 | 0.5550 | 0.5642 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7979 (32/32) | 2.145 | 0.5661 | +0.1954 | 0.625 | 0.9893 | 1.0000 | 0.61 | 0.60 | 0 / 99 | 0.01 | 0.0001 | 0.0002 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.8164 (32/32) | 2.358 | 0.5783 | +0.1832 | 0.688 | 0.9980 | 1.0000 | 0.64 | 0.63 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_4 | 0.7695 (32/32) | 1.160 | 0.6413 | +0.1202 | 0.656 | 0.9736 | 1.0000 | 0.57 | 0.54 | 0 / 99 | 0.01 | 0.0002 | 0.0003 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4854 (32/32) | 0.000 | 0.7615 | +0.0000 | 0.469 | 0.4824 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5817 | 0.8561 | None / None / None |

### World W, seed 92132: W: rule weaker than the information available

Outside density 0.3300; block present 32.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.5146 (32/32), p_S = 0.04 (n_ge = 3 of 99, n_deg = 0), p_P = 0.4264; ceiling_full = 0.5312, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5146 (32/32) | 0.175 | 0.9735 | -0.2042 | 0.500 | 0.5312 | 1.0000 | 0.47 | 0.03 | 3 / 99 | 0.04 | 0.4264 | 0.4358 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5127 (32/32) | 0.175 | 0.9050 | -0.1357 | 0.500 | 0.5312 | 1.0000 | 0.41 | 0.03 | 0 / 99 | 0.01 | 0.4345 | 0.4458 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7627 (32/32) | 1.988 | 0.5803 | +0.1890 | 0.562 | 0.9854 | 1.0000 | 0.54 | 0.53 | 0 / 99 | 0.01 | 0.0004 | 0.0005 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.7803 (32/32) | 2.166 | 0.6075 | +0.1618 | 0.625 | 0.9961 | 1.0000 | 0.56 | 0.56 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_4 | 0.7393 (32/32) | 1.004 | 0.6655 | +0.1038 | 0.562 | 0.9736 | 1.0000 | 0.51 | 0.48 | 0 / 99 | 0.01 | 0.0008 | 0.0015 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5029 (32/32) | 0.000 | 0.7693 | +0.0000 | 0.531 | 0.5029 | 0.5000 | 1.00 | n/a | 99 / 99 | 1.00 | 0.4896 | 0.4282 | None / None / None |

### World W, seed 92133: W: rule weaker than the information available

Outside density 0.3164; block present 32.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.5215 (32/32), p_S = 0.48 (n_ge = 47 of 99, n_deg = 0), p_P = 0.3856; ceiling_full = 0.5264, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5215 (32/32) | 0.162 | 1.1243 | -0.3483 | 0.500 | 0.5264 | 1.0000 | 0.81 | 0.04 | 47 / 99 | 0.48 | 0.3856 | 0.3979 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5215 (32/32) | 0.211 | 1.0063 | -0.2303 | 0.500 | 0.5312 | 1.0000 | 0.69 | 0.04 | 98 / 99 | 0.99 | 0.3843 | 0.3990 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7227 (32/32) | 1.779 | 0.7202 | +0.0558 | 0.531 | 0.9336 | 1.0000 | 0.51 | 0.45 | 0 / 99 | 0.01 | 0.0017 | 0.0030 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.6904 (32/32) | 1.647 | 0.8262 | -0.0502 | 0.562 | 0.9951 | 1.0000 | 0.38 | 0.38 | 0 / 99 | 0.01 | 0.0045 | 0.0089 | 1.0 / 1.0 / 1.0 |
| BF_4 | 0.6797 (32/32) | 0.881 | 0.7349 | +0.0410 | 0.562 | 0.9541 | 1.0000 | 0.40 | 0.36 | 0 / 99 | 0.01 | 0.0071 | 0.0110 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5215 (32/32) | 0.000 | 0.7760 | +0.0000 | 0.531 | 0.5244 | 0.5000 | 0.88 | n/a | 99 / 99 | 1.00 | 0.3895 | 0.0346 | None / None / None |

### World W, seed 92134: W: rule weaker than the information available

Outside density 0.3178; block present 32.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.4795 (32/32), p_S = 1.00 (n_ge = 99 of 99, n_deg = 0), p_P = 0.6108; ceiling_full = 0.4844, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 1.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4795 (32/32) | -0.000 | 1.1983 | -0.4666 | 0.500 | 0.4844 | 1.0000 | n/a | -0.04 | 99 / 99 | 1.00 | 0.6108 | 0.6133 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.4893 (32/32) | 0.005 | 1.0859 | -0.3542 | 0.500 | 0.4814 | 1.0000 | n/a | -0.02 | 99 / 99 | 1.00 | 0.5601 | 0.5660 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7207 (32/32) | 1.357 | 0.8148 | -0.0831 | 0.500 | 0.8379 | 1.0000 | 0.65 | 0.44 | 0 / 99 | 0.01 | 0.0018 | 0.0034 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.5918 (32/32) | 0.923 | 0.9532 | -0.2215 | 0.500 | 0.8877 | 1.0000 | 0.24 | 0.18 | 0 / 99 | 0.01 | 0.1139 | 0.1358 | 1.0 / 1.0 / 1.0 |
| BF_4 | 0.5752 (32/32) | 0.823 | 1.0311 | -0.2994 | 0.500 | 0.9004 | 1.0000 | 0.19 | 0.15 | 0 / 99 | 0.01 | 0.1583 | 0.1851 | 1.0 / 3.0 / 1.0 |
| N1 | 0.5312 (32/32) | 0.000 | 0.7317 | +0.0000 | 0.531 | 0.5312 | 0.5000 | 1.00 | n/a | 99 / 99 | 1.00 | 0.3335 | 0.0265 | None / None / None |

### World M0.5, seed 92140: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1702; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 0.9717 >= 0.90)]. rule #2.1: AUC = 0.5171 (32/32), p_S = 0.28 (n_ge = 27 of 99, n_deg = 0), p_P = 0.4162; ceiling_full = 0.9717, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5171 (32/32) | 0.000 | 0.8203 | -0.0046 | 0.531 | 0.9717 | 1.0000 | 0.04 | 0.03 | 27 / 99 | 0.28 | 0.4162 | 0.1141 | 100.0 / 3.0 / 1.0 |
| BF_1 | 0.5107 (32/32) | 0.000 | 0.8158 | +0.0000 | 0.531 | 0.9834 | 1.0000 | 0.02 | 0.02 | 94 / 99 | 0.95 | 0.4505 | 0.2218 | 100.0 / 3.0 / 1.0 |
| BF_2 | 0.5107 (32/32) | 0.000 | 0.8158 | +0.0000 | 0.531 | 0.9941 | 1.0000 | 0.02 | 0.02 | 98 / 99 | 0.99 | 0.4505 | 0.2218 | 100.0 / 3.0 / 1.0 |
| BF_3 | 0.5107 (32/32) | 0.000 | 0.8158 | +0.0000 | 0.531 | 0.9961 | 1.0000 | 0.02 | 0.02 | 99 / 99 | 1.00 | 0.4505 | 0.2218 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.5107 (32/32) | 0.000 | 0.8158 | +0.0000 | 0.531 | 1.0000 | 1.0000 | 0.02 | 0.02 | 99 / 99 | 1.00 | 0.4505 | 0.2218 | 100.0 / 3.0 / 1.0 |
| N1 | 0.5107 (32/32) | 0.000 | 0.8158 | +0.0000 | 0.531 | 0.5078 | 0.5000 | 1.38 | n/a | 99 / 99 | 1.00 | 0.4505 | 0.2218 | None / None / None |

### World M0.5, seed 92141: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma))

Outside density 0.1847; block present 32.
Verdict line: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma)). rule #2.1: AUC = 0.6406 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0276; ceiling_full = 0.9990, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 100, BF_3 100, BF_4 100.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6406 (32/32) | 0.281 | 0.8563 | +0.0620 | 0.656 | 0.9990 | 1.0000 | 0.28 | 0.28 | 0 / 99 | 0.01 | 0.0276 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6592 (32/32) | 0.345 | 0.8392 | +0.0791 | 0.625 | 0.9990 | 1.0000 | 0.32 | 0.32 | 0 / 99 | 0.01 | 0.0150 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.4951 (32/32) | 0.000 | 0.9183 | +0.0000 | 0.500 | 0.9990 | 1.0000 | -0.01 | -0.01 | 98 / 99 | 0.99 | 0.5296 | 0.6249 | 100.0 / 3.0 / 1.0 |
| BF_3 | 0.4951 (32/32) | 0.000 | 0.9183 | +0.0000 | 0.500 | 0.9980 | 1.0000 | -0.01 | -0.01 | 99 / 99 | 1.00 | 0.5296 | 0.6249 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.4951 (32/32) | 0.000 | 0.9183 | +0.0000 | 0.500 | 0.9980 | 1.0000 | -0.01 | -0.01 | 99 / 99 | 1.00 | 0.5296 | 0.6249 | 100.0 / 3.0 / 1.0 |
| N1 | 0.4951 (32/32) | 0.000 | 0.9183 | +0.0000 | 0.500 | 0.4980 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5296 | 0.6249 | None / None / None |

### World M0.5, seed 92142: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma))

Outside density 0.1672; block present 32.
Verdict line: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma)). rule #2.1: AUC = 0.6572 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0145; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 100, BF_3 100, BF_4 100.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6572 (32/32) | 0.367 | 0.8891 | +0.0828 | 0.594 | 1.0000 | 1.0000 | 0.31 | 0.31 | 0 / 99 | 0.01 | 0.0145 | 0.0004 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6816 (32/32) | 0.394 | 0.8766 | +0.0953 | 0.656 | 1.0000 | 1.0000 | 0.36 | 0.36 | 0 / 99 | 0.01 | 0.0057 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.4941 (32/32) | 0.000 | 0.9719 | +0.0000 | 0.469 | 1.0000 | 1.0000 | -0.01 | -0.01 | 98 / 99 | 0.99 | 0.5365 | 0.6452 | 100.0 / 3.0 / 1.0 |
| BF_3 | 0.4941 (32/32) | 0.000 | 0.9719 | +0.0000 | 0.469 | 1.0000 | 1.0000 | -0.01 | -0.01 | 99 / 99 | 1.00 | 0.5365 | 0.6452 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.4941 (32/32) | 0.000 | 0.9719 | +0.0000 | 0.469 | 0.9990 | 1.0000 | -0.01 | -0.01 | 99 / 99 | 1.00 | 0.5365 | 0.6452 | 100.0 / 3.0 / 1.0 |
| N1 | 0.4941 (32/32) | 0.000 | 0.9719 | +0.0000 | 0.469 | 0.4941 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5365 | 0.6452 | None / None / None |

### World M0.5, seed 92143: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1766; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 1.0000 >= 0.90)]. rule #2.1: AUC = 0.5137 (32/32), p_S = 0.75 (n_ge = 74 of 99, n_deg = 0), p_P = 0.4309; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5137 (32/32) | 0.000 | 0.9753 | +0.0206 | 0.562 | 1.0000 | 1.0000 | 0.03 | 0.03 | 74 / 99 | 0.75 | 0.4309 | 0.0883 | 100.0 / 3.0 / 1.0 |
| BF_1 | 0.5225 (32/32) | 0.000 | 0.9959 | +0.0000 | 0.594 | 1.0000 | 1.0000 | 0.04 | 0.04 | 91 / 99 | 0.92 | 0.3827 | 0.0175 | 100.0 / 3.0 / 1.0 |
| BF_2 | 0.5225 (32/32) | 0.000 | 0.9959 | +0.0000 | 0.594 | 1.0000 | 1.0000 | 0.04 | 0.04 | 99 / 99 | 1.00 | 0.3827 | 0.0175 | 100.0 / 3.0 / 1.0 |
| BF_3 | 0.5225 (32/32) | 0.000 | 0.9959 | +0.0000 | 0.594 | 1.0000 | 1.0000 | 0.04 | 0.04 | 99 / 99 | 1.00 | 0.3827 | 0.0175 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.5225 (32/32) | 0.000 | 0.9959 | +0.0000 | 0.594 | 0.5156 | 1.0000 | 1.44 | 0.04 | 99 / 99 | 1.00 | 0.3827 | 0.0175 | 100.0 / 100.0 / 1.0 |
| N1 | 0.5225 (32/32) | 0.000 | 0.9959 | +0.0000 | 0.594 | 0.5156 | 0.5000 | 1.44 | n/a | 99 / 99 | 1.00 | 0.3827 | 0.0175 | None / None / None |

### World M0.5, seed 92144: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma))

Outside density 0.1770; block present 32.
Verdict line: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma)). rule #2.1: AUC = 0.6519 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0192; ceiling_full = 0.9844, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6519 (32/32) | 0.333 | 0.7608 | +0.0727 | 0.625 | 0.9844 | 1.0000 | 0.31 | 0.30 | 0 / 99 | 0.01 | 0.0192 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6758 (32/32) | 0.333 | 0.7617 | +0.0718 | 0.688 | 0.9873 | 1.0000 | 0.36 | 0.35 | 0 / 99 | 0.01 | 0.0077 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.6348 (32/32) | 0.323 | 0.7661 | +0.0673 | 0.594 | 0.9932 | 1.0000 | 0.27 | 0.27 | 0 / 99 | 0.01 | 0.0317 | 0.0015 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.6572 (32/32) | 0.372 | 0.7619 | +0.0716 | 0.594 | 0.9902 | 1.0000 | 0.32 | 0.31 | 0 / 99 | 0.01 | 0.0149 | 0.0007 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.6572 (32/32) | 0.370 | 0.7672 | +0.0663 | 0.625 | 0.9932 | 1.0000 | 0.32 | 0.31 | 0 / 99 | 0.01 | 0.0143 | 0.0014 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5166 (32/32) | 0.000 | 0.8334 | +0.0000 | 0.500 | 0.5166 | 0.5000 | 1.00 | n/a | 99 / 99 | 1.00 | 0.4091 | 0.2083 | None / None / None |

### World M1.0, seed 92150: R: regrows

Outside density 0.1912; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.9424 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.9424 (32/32) | 2.345 | 0.5028 | +0.3761 | 0.875 | 1.0000 | 1.0000 | 0.88 | 0.88 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.8555 (32/32) | 1.208 | 0.6285 | +0.2504 | 0.812 | 1.0000 | 1.0000 | 0.71 | 0.71 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 1.0 / 1.0 |
| BF_2 | 0.7939 (32/32) | 0.932 | 0.6868 | +0.1921 | 0.719 | 1.0000 | 1.0000 | 0.59 | 0.59 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7920 (32/32) | 0.927 | 0.6882 | +0.1907 | 0.750 | 1.0000 | 1.0000 | 0.58 | 0.58 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7969 (32/32) | 0.949 | 0.6858 | +0.1932 | 0.750 | 0.9990 | 1.0000 | 0.59 | 0.59 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5420 (32/32) | 0.000 | 0.8790 | +0.0000 | 0.562 | 0.5469 | 0.5000 | 0.90 | n/a | 99 / 99 | 1.00 | 0.2830 | 0.0097 | None / None / None |

### World M1.0, seed 92151: R: regrows

Outside density 0.2030; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.9697 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.9697 (32/32) | 2.247 | 0.4609 | +0.3895 | 0.938 | 1.0000 | 1.0000 | 0.94 | 0.94 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.9727 (32/32) | 2.078 | 0.4478 | +0.4026 | 0.938 | 1.0000 | 1.0000 | 0.95 | 0.95 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.8838 (32/32) | 1.134 | 0.5987 | +0.2517 | 0.812 | 0.9990 | 1.0000 | 0.77 | 0.77 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.8770 (32/32) | 1.120 | 0.6042 | +0.2462 | 0.812 | 1.0000 | 1.0000 | 0.75 | 0.75 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.8916 (32/32) | 1.140 | 0.5950 | +0.2555 | 0.844 | 1.0000 | 1.0000 | 0.78 | 0.78 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5273 (32/32) | 0.000 | 0.8504 | +0.0000 | 0.531 | 0.5098 | 0.5000 | 2.80 | n/a | 99 / 99 | 1.00 | 0.3582 | 0.0122 | None / None / None |

### World M1.0, seed 92152: R: regrows

Outside density 0.2020; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.8389 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 0.9980, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.8389 (32/32) | 1.623 | 0.5772 | +0.2845 | 0.750 | 0.9980 | 1.0000 | 0.68 | 0.68 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.8398 (32/32) | 1.553 | 0.5774 | +0.2844 | 0.781 | 0.9980 | 1.0000 | 0.68 | 0.68 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7598 (32/32) | 0.975 | 0.6658 | +0.1960 | 0.688 | 0.9873 | 1.0000 | 0.53 | 0.52 | 0 / 99 | 0.01 | 0.0004 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7559 (32/32) | 0.955 | 0.6724 | +0.1894 | 0.688 | 0.9961 | 1.0000 | 0.52 | 0.51 | 0 / 99 | 0.01 | 0.0004 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7148 (32/32) | 0.821 | 0.7078 | +0.1540 | 0.656 | 0.9951 | 1.0000 | 0.43 | 0.43 | 0 / 99 | 0.01 | 0.0009 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5371 (32/32) | 0.000 | 0.8618 | +0.0000 | 0.531 | 0.5303 | 0.5000 | 1.23 | n/a | 99 / 99 | 1.00 | 0.3056 | 0.0293 | None / None / None |

### World M1.0, seed 92153: R: regrows

Outside density 0.1888; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.9492 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.9492 (32/32) | 2.100 | 0.5015 | +0.3362 | 0.875 | 1.0000 | 1.0000 | 0.90 | 0.90 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.8779 (32/32) | 1.118 | 0.5948 | +0.2429 | 0.844 | 1.0000 | 1.0000 | 0.76 | 0.76 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.8711 (32/32) | 1.113 | 0.5882 | +0.2495 | 0.844 | 1.0000 | 1.0000 | 0.74 | 0.74 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.8799 (32/32) | 1.121 | 0.5904 | +0.2473 | 0.844 | 1.0000 | 1.0000 | 0.76 | 0.76 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.8877 (32/32) | 1.124 | 0.5918 | +0.2459 | 0.812 | 1.0000 | 1.0000 | 0.78 | 0.78 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4971 (32/32) | 0.000 | 0.8377 | +0.0000 | 0.531 | 0.5000 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5132 | 0.6415 | None / None / None |

### World M1.0, seed 92154: R: regrows

Outside density 0.1999; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.7920 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7920 (32/32) | 0.811 | 0.7227 | +0.1692 | 0.719 | 1.0000 | 1.0000 | 0.58 | 0.58 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 1.0 / 1.0 |
| BF_1 | 0.7744 (32/32) | 0.737 | 0.7225 | +0.1694 | 0.719 | 1.0000 | 1.0000 | 0.55 | 0.55 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.7705 (32/32) | 0.703 | 0.7323 | +0.1596 | 0.688 | 1.0000 | 1.0000 | 0.54 | 0.54 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7803 (32/32) | 0.760 | 0.7203 | +0.1716 | 0.656 | 1.0000 | 1.0000 | 0.56 | 0.56 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7627 (32/32) | 0.789 | 0.7206 | +0.1712 | 0.688 | 1.0000 | 1.0000 | 0.53 | 0.53 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4912 (32/32) | 0.000 | 0.8919 | +0.0000 | 0.438 | 0.4766 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5489 | 0.7176 | None / None / None |

### World M0.6, seed 92160: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1793; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 0.9980 >= 0.90)]. rule #2.1: AUC = 0.5674 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.1754; ceiling_full = 0.9980, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 100, BF_4 100; G reached through lambda = 100 on BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5674 (32/32) | 0.192 | 0.7864 | +0.0523 | 0.531 | 0.9980 | 1.0000 | 0.14 | 0.13 | 0 / 99 | 0.01 | 0.1754 | 0.0020 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.5742 (32/32) | 0.200 | 0.7916 | +0.0471 | 0.531 | 0.9990 | 1.0000 | 0.15 | 0.15 | 0 / 99 | 0.01 | 0.1546 | 0.0010 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.5889 (32/32) | 0.210 | 0.7855 | +0.0532 | 0.531 | 1.0000 | 1.0000 | 0.18 | 0.18 | 0 / 99 | 0.01 | 0.1134 | 0.0030 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.4785 (32/32) | 0.000 | 0.8387 | +0.0000 | 0.469 | 1.0000 | 1.0000 | -0.04 | -0.04 | 98 / 99 | 0.99 | 0.6197 | 0.9326 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.4785 (32/32) | 0.000 | 0.8387 | +0.0000 | 0.469 | 1.0000 | 1.0000 | -0.04 | -0.04 | 98 / 99 | 0.99 | 0.6197 | 0.9326 | 100.0 / 3.0 / 1.0 |
| N1 | 0.4785 (32/32) | 0.000 | 0.8387 | +0.0000 | 0.469 | 0.4844 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.6197 | 0.9326 | None / None / None |

### World M0.6, seed 92161: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma))

Outside density 0.1972; block present 32.
Verdict line: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma)). rule #2.1: AUC = 0.6436 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0242; ceiling_full = 0.9639, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6436 (32/32) | 0.302 | 0.7924 | +0.0974 | 0.625 | 0.9639 | 1.0000 | 0.31 | 0.29 | 0 / 99 | 0.01 | 0.0242 | 0.0002 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6426 (32/32) | 0.302 | 0.8018 | +0.0879 | 0.625 | 0.9619 | 1.0000 | 0.31 | 0.29 | 0 / 99 | 0.01 | 0.0247 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.5566 (32/32) | 0.129 | 0.8509 | +0.0389 | 0.594 | 0.9756 | 1.0000 | 0.12 | 0.11 | 0 / 99 | 0.01 | 0.2268 | 0.0951 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5420 (32/32) | 0.117 | 0.8603 | +0.0295 | 0.594 | 0.9727 | 1.0000 | 0.09 | 0.08 | 0 / 99 | 0.01 | 0.2863 | 0.1560 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.5381 (32/32) | 0.125 | 0.8603 | +0.0295 | 0.562 | 0.9834 | 1.0000 | 0.08 | 0.08 | 0 / 99 | 0.01 | 0.3100 | 0.1863 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5078 (32/32) | 0.000 | 0.8898 | +0.0000 | 0.500 | 0.5029 | 0.5000 | 2.67 | n/a | 99 / 99 | 1.00 | 0.4607 | 0.3538 | None / None / None |

### World M0.6, seed 92162: R: regrows

Outside density 0.1753; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.7402 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0003; ceiling_full = 0.9980, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7402 (32/32) | 0.581 | 0.7362 | +0.1231 | 0.719 | 0.9980 | 1.0000 | 0.48 | 0.48 | 0 / 99 | 0.01 | 0.0003 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7217 (32/32) | 0.560 | 0.7388 | +0.1204 | 0.656 | 0.9990 | 1.0000 | 0.44 | 0.44 | 0 / 99 | 0.01 | 0.0006 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.7422 (32/32) | 0.599 | 0.7314 | +0.1278 | 0.719 | 1.0000 | 1.0000 | 0.48 | 0.48 | 0 / 99 | 0.01 | 0.0003 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7295 (32/32) | 0.587 | 0.7383 | +0.1209 | 0.688 | 0.9980 | 1.0000 | 0.46 | 0.46 | 0 / 99 | 0.01 | 0.0008 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7314 (32/32) | 0.591 | 0.7369 | +0.1224 | 0.688 | 0.9990 | 1.0000 | 0.46 | 0.46 | 0 / 99 | 0.01 | 0.0007 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4707 (32/32) | 0.000 | 0.8592 | +0.0000 | 0.500 | 0.4639 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.6608 | 0.9541 | None / None / None |

### World M0.6, seed 92163: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma))

Outside density 0.1726; block present 32.
Verdict line: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma)). rule #2.1: AUC = 0.6572 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0142; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6572 (32/32) | 0.389 | 0.8106 | +0.0850 | 0.625 | 1.0000 | 1.0000 | 0.31 | 0.31 | 0 / 99 | 0.01 | 0.0142 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6689 (32/32) | 0.382 | 0.8070 | +0.0887 | 0.625 | 1.0000 | 1.0000 | 0.34 | 0.34 | 0 / 99 | 0.01 | 0.0099 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.6406 (32/32) | 0.341 | 0.8206 | +0.0750 | 0.625 | 1.0000 | 1.0000 | 0.28 | 0.28 | 0 / 99 | 0.01 | 0.0255 | 0.0002 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.6602 (32/32) | 0.380 | 0.8075 | +0.0881 | 0.625 | 1.0000 | 1.0000 | 0.32 | 0.32 | 0 / 99 | 0.01 | 0.0130 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.6592 (32/32) | 0.375 | 0.8100 | +0.0857 | 0.625 | 0.9990 | 1.0000 | 0.32 | 0.32 | 0 / 99 | 0.01 | 0.0130 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4863 (32/32) | 0.000 | 0.8957 | +0.0000 | 0.469 | 0.5020 | 0.5000 | -7.00 | n/a | 99 / 99 | 1.00 | 0.5753 | 0.8356 | None / None / None |

### World M0.6, seed 92164: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma))

Outside density 0.1841; block present 32.
Verdict line: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma)). rule #2.1: AUC = 0.6699 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0090; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 100, BF_3 100, BF_4 100.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6699 (32/32) | 0.314 | 0.7886 | +0.0740 | 0.562 | 1.0000 | 1.0000 | 0.34 | 0.34 | 0 / 99 | 0.01 | 0.0090 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6670 (32/32) | 0.296 | 0.7876 | +0.0751 | 0.562 | 1.0000 | 1.0000 | 0.33 | 0.33 | 0 / 99 | 0.01 | 0.0104 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.5127 (32/32) | 0.000 | 0.8626 | +0.0000 | 0.500 | 1.0000 | 1.0000 | 0.03 | 0.03 | 98 / 99 | 0.99 | 0.4340 | 0.2073 | 100.0 / 3.0 / 1.0 |
| BF_3 | 0.5127 (32/32) | 0.000 | 0.8626 | +0.0000 | 0.500 | 1.0000 | 1.0000 | 0.03 | 0.03 | 98 / 99 | 0.99 | 0.4340 | 0.2073 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.5127 (32/32) | 0.000 | 0.8626 | +0.0000 | 0.500 | 1.0000 | 1.0000 | 0.03 | 0.03 | 98 / 99 | 0.99 | 0.4340 | 0.2073 | 100.0 / 3.0 / 1.0 |
| N1 | 0.5127 (32/32) | 0.000 | 0.8626 | +0.0000 | 0.500 | 0.5098 | 0.5000 | 1.30 | n/a | 99 / 99 | 1.00 | 0.4340 | 0.2073 | None / None / None |

### World M0.75, seed 92170: R: regrows

Outside density 0.1861; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.8203 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.8203 (32/32) | 0.657 | 0.7928 | +0.1403 | 0.781 | 1.0000 | 1.0000 | 0.64 | 0.64 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.8057 (32/32) | 0.613 | 0.7922 | +0.1409 | 0.750 | 1.0000 | 1.0000 | 0.61 | 0.61 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.7656 (32/32) | 0.591 | 0.7986 | +0.1346 | 0.719 | 1.0000 | 1.0000 | 0.53 | 0.53 | 0 / 99 | 0.01 | 0.0004 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7568 (32/32) | 0.579 | 0.8088 | +0.1243 | 0.719 | 0.9990 | 1.0000 | 0.51 | 0.51 | 0 / 99 | 0.01 | 0.0004 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7471 (32/32) | 0.573 | 0.8121 | +0.1210 | 0.688 | 1.0000 | 1.0000 | 0.49 | 0.49 | 0 / 99 | 0.01 | 0.0004 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4844 (32/32) | 0.000 | 0.9331 | +0.0000 | 0.500 | 0.4824 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5902 | 0.7890 | None / None / None |

### World M0.75, seed 92171: R: regrows

Outside density 0.1864; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.6914 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0036; ceiling_full = 0.9551, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6914 (32/32) | 0.398 | 0.8178 | +0.0832 | 0.625 | 0.9551 | 1.0000 | 0.42 | 0.38 | 0 / 99 | 0.01 | 0.0036 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6943 (32/32) | 0.375 | 0.8231 | +0.0780 | 0.625 | 0.9492 | 1.0000 | 0.43 | 0.39 | 0 / 99 | 0.01 | 0.0032 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.6953 (32/32) | 0.389 | 0.8212 | +0.0799 | 0.625 | 0.9727 | 1.0000 | 0.41 | 0.39 | 0 / 99 | 0.01 | 0.0032 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.6797 (32/32) | 0.393 | 0.8182 | +0.0828 | 0.625 | 0.9727 | 1.0000 | 0.38 | 0.36 | 0 / 99 | 0.01 | 0.0059 | 0.0002 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.6787 (32/32) | 0.395 | 0.8174 | +0.0836 | 0.656 | 0.9922 | 1.0000 | 0.36 | 0.36 | 0 / 99 | 0.01 | 0.0062 | 0.0002 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5312 (32/32) | 0.000 | 0.9010 | +0.0000 | 0.469 | 0.5254 | 0.5000 | 1.23 | n/a | 99 / 99 | 1.00 | 0.3353 | 0.0586 | None / None / None |

### World M0.75, seed 92172: R: regrows

Outside density 0.1854; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.7280 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0004; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7280 (32/32) | 0.449 | 0.7457 | +0.1042 | 0.656 | 1.0000 | 1.0000 | 0.46 | 0.46 | 0 / 99 | 0.01 | 0.0004 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7217 (32/32) | 0.474 | 0.7396 | +0.1103 | 0.656 | 1.0000 | 1.0000 | 0.44 | 0.44 | 0 / 99 | 0.01 | 0.0006 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.7139 (32/32) | 0.454 | 0.7545 | +0.0954 | 0.656 | 1.0000 | 1.0000 | 0.43 | 0.43 | 0 / 99 | 0.01 | 0.0011 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7119 (32/32) | 0.492 | 0.7473 | +0.1026 | 0.688 | 1.0000 | 1.0000 | 0.42 | 0.42 | 0 / 99 | 0.01 | 0.0016 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7100 (32/32) | 0.483 | 0.7560 | +0.0939 | 0.719 | 1.0000 | 1.0000 | 0.42 | 0.42 | 0 / 99 | 0.01 | 0.0015 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4844 (32/32) | 0.000 | 0.8499 | +0.0000 | 0.500 | 0.4893 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5849 | 0.8608 | None / None / None |

### World M0.75, seed 92173: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma))

Outside density 0.1949; block present 32.
Verdict line: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma)). rule #2.1: AUC = 0.6802 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0063; ceiling_full = 0.9785, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6802 (32/32) | 0.333 | 0.7930 | +0.0780 | 0.688 | 0.9785 | 1.0000 | 0.38 | 0.36 | 0 / 99 | 0.01 | 0.0063 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6533 (32/32) | 0.302 | 0.7980 | +0.0730 | 0.625 | 0.9854 | 1.0000 | 0.32 | 0.31 | 0 / 99 | 0.01 | 0.0172 | 0.0002 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.6094 (32/32) | 0.206 | 0.8292 | +0.0418 | 0.594 | 0.9814 | 1.0000 | 0.23 | 0.22 | 0 / 99 | 0.01 | 0.0664 | 0.0122 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.6045 (32/32) | 0.201 | 0.8337 | +0.0373 | 0.625 | 0.9941 | 1.0000 | 0.21 | 0.21 | 0 / 99 | 0.01 | 0.0752 | 0.0201 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.6006 (32/32) | 0.199 | 0.8326 | +0.0384 | 0.594 | 0.9980 | 1.0000 | 0.20 | 0.20 | 0 / 99 | 0.01 | 0.0834 | 0.0274 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4766 (32/32) | 0.000 | 0.8710 | +0.0000 | 0.469 | 0.4766 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.6277 | 0.9219 | None / None / None |

### World M0.75, seed 92174: R: regrows

Outside density 0.1810; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.7178 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0014; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7178 (32/32) | 0.520 | 0.8030 | +0.0875 | 0.656 | 1.0000 | 1.0000 | 0.44 | 0.44 | 0 / 99 | 0.01 | 0.0014 | 0.0002 | 3.0 / 1.0 / 1.0 |
| BF_1 | 0.7197 (32/32) | 0.458 | 0.7986 | +0.0919 | 0.688 | 1.0000 | 1.0000 | 0.44 | 0.44 | 0 / 99 | 0.01 | 0.0012 | 0.0002 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.7129 (32/32) | 0.458 | 0.7990 | +0.0915 | 0.688 | 1.0000 | 1.0000 | 0.43 | 0.43 | 0 / 99 | 0.01 | 0.0017 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.6602 (32/32) | 0.306 | 0.8342 | +0.0563 | 0.625 | 1.0000 | 1.0000 | 0.32 | 0.32 | 0 / 99 | 0.01 | 0.0140 | 0.0029 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.6592 (32/32) | 0.318 | 0.8304 | +0.0601 | 0.625 | 1.0000 | 1.0000 | 0.32 | 0.32 | 0 / 99 | 0.01 | 0.0139 | 0.0037 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5254 (32/32) | 0.000 | 0.8905 | +0.0000 | 0.469 | 0.5117 | 0.5000 | 2.17 | n/a | 99 / 99 | 1.00 | 0.3600 | 0.0716 | None / None / None |

### World M0.85, seed 92180: R: regrows

Outside density 0.1803; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.8984 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.8984 (32/32) | 1.315 | 0.6717 | +0.2102 | 0.781 | 1.0000 | 1.0000 | 0.80 | 0.80 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.8848 (32/32) | 1.192 | 0.6442 | +0.2377 | 0.781 | 1.0000 | 1.0000 | 0.77 | 0.77 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7959 (32/32) | 0.759 | 0.7202 | +0.1617 | 0.750 | 0.9980 | 1.0000 | 0.59 | 0.59 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7861 (32/32) | 0.779 | 0.7191 | +0.1628 | 0.688 | 1.0000 | 1.0000 | 0.57 | 0.57 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7812 (32/32) | 0.767 | 0.7113 | +0.1706 | 0.719 | 1.0000 | 1.0000 | 0.56 | 0.56 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4951 (32/32) | 0.000 | 0.8819 | +0.0000 | 0.531 | 0.4980 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5322 | 0.6529 | None / None / None |

### World M0.85, seed 92181: R: regrows

Outside density 0.1912; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.7461 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0006; ceiling_full = 0.9883, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7461 (32/32) | 0.622 | 0.6888 | +0.1271 | 0.688 | 0.9883 | 1.0000 | 0.50 | 0.49 | 0 / 99 | 0.01 | 0.0006 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7520 (32/32) | 0.634 | 0.6774 | +0.1385 | 0.688 | 0.9902 | 1.0000 | 0.51 | 0.50 | 0 / 99 | 0.01 | 0.0005 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.7686 (32/32) | 0.721 | 0.6664 | +0.1496 | 0.750 | 0.9932 | 1.0000 | 0.54 | 0.54 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7773 (32/32) | 0.719 | 0.6657 | +0.1503 | 0.750 | 0.9922 | 1.0000 | 0.56 | 0.55 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7559 (32/32) | 0.669 | 0.6823 | +0.1337 | 0.781 | 0.9912 | 1.0000 | 0.52 | 0.51 | 0 / 99 | 0.01 | 0.0004 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5117 (32/32) | 0.000 | 0.8159 | +0.0000 | 0.531 | 0.5107 | 0.5000 | 1.09 | n/a | 99 / 99 | 1.00 | 0.4416 | 0.2616 | None / None / None |

### World M0.85, seed 92182: R: regrows

Outside density 0.1861; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.8193 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 0.9893, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.8193 (32/32) | 1.289 | 0.6850 | +0.2064 | 0.719 | 0.9893 | 1.0000 | 0.65 | 0.64 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.7354 (32/32) | 0.662 | 0.7461 | +0.1452 | 0.750 | 0.9902 | 1.0000 | 0.48 | 0.47 | 0 / 99 | 0.01 | 0.0008 | 0.0001 | 3.0 / 1.0 / 1.0 |
| BF_2 | 0.7451 (32/32) | 0.648 | 0.7434 | +0.1480 | 0.719 | 0.9980 | 1.0000 | 0.49 | 0.49 | 0 / 99 | 0.01 | 0.0004 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7510 (32/32) | 0.702 | 0.7381 | +0.1533 | 0.719 | 0.9980 | 1.0000 | 0.50 | 0.50 | 0 / 99 | 0.01 | 0.0004 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7441 (32/32) | 0.686 | 0.7441 | +0.1472 | 0.719 | 0.9980 | 1.0000 | 0.49 | 0.49 | 0 / 99 | 0.01 | 0.0006 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5156 (32/32) | 0.000 | 0.8914 | +0.0000 | 0.500 | 0.5107 | 0.5000 | 1.45 | n/a | 99 / 99 | 1.00 | 0.4256 | 0.1991 | None / None / None |

### World M0.85, seed 92183: W: rule weaker than the information available

Outside density 0.1864; block present 32.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.7017 (32/32), p_S = 0.02 (n_ge = 1 of 99, n_deg = 0), p_P = 0.0028; ceiling_full = 0.9775, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7017 (32/32) | 0.403 | 0.8567 | +0.0876 | 0.656 | 0.9775 | 1.0000 | 0.42 | 0.40 | 1 / 99 | 0.02 | 0.0028 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7090 (32/32) | 0.391 | 0.8542 | +0.0901 | 0.688 | 0.9756 | 1.0000 | 0.44 | 0.42 | 1 / 99 | 0.02 | 0.0017 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.7031 (32/32) | 0.391 | 0.8503 | +0.0940 | 0.656 | 0.9688 | 1.0000 | 0.43 | 0.41 | 0 / 99 | 0.01 | 0.0030 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7354 (32/32) | 0.417 | 0.8441 | +0.1002 | 0.656 | 0.9932 | 1.0000 | 0.48 | 0.47 | 0 / 99 | 0.01 | 0.0007 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7041 (32/32) | 0.370 | 0.8551 | +0.0892 | 0.625 | 1.0000 | 1.0000 | 0.41 | 0.41 | 0 / 99 | 0.01 | 0.0024 | 0.0002 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5098 (32/32) | 0.000 | 0.9442 | +0.0000 | 0.469 | 0.5078 | 0.5000 | 1.25 | n/a | 99 / 99 | 1.00 | 0.4447 | 0.3172 | None / None / None |

### World M0.85, seed 92184: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1787; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5; 0.85: 4/5, 3/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 0.9941 >= 0.90)]. rule #2.1: AUC = 0.5254 (32/32), p_S = 0.11 (n_ge = 10 of 99, n_deg = 0), p_P = 0.3695; ceiling_full = 0.9941, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5254 (32/32) | 0.088 | 0.8966 | +0.0061 | 0.500 | 0.9941 | 1.0000 | 0.05 | 0.05 | 10 / 99 | 0.11 | 0.3695 | 0.2853 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.5420 (32/32) | 0.109 | 0.8845 | +0.0182 | 0.531 | 0.9990 | 1.0000 | 0.08 | 0.08 | 2 / 99 | 0.03 | 0.2914 | 0.1795 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.5439 (32/32) | 0.119 | 0.8832 | +0.0195 | 0.531 | 0.9990 | 1.0000 | 0.09 | 0.09 | 0 / 99 | 0.01 | 0.2769 | 0.1821 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5449 (32/32) | 0.121 | 0.8827 | +0.0200 | 0.531 | 1.0000 | 1.0000 | 0.09 | 0.09 | 0 / 99 | 0.01 | 0.2708 | 0.2010 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.5488 (32/32) | 0.125 | 0.8800 | +0.0227 | 0.531 | 1.0000 | 1.0000 | 0.10 | 0.10 | 0 / 99 | 0.01 | 0.2552 | 0.1895 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5059 (32/32) | 0.000 | 0.9027 | +0.0000 | 0.500 | 0.5020 | 0.5000 | 3.00 | n/a | 99 / 99 | 1.00 | 0.4729 | 0.3600 | None / None / None |


# Synthetic step, lobe R

## Two-world check, lobe R (section 3.6; A section 3.6)

| family | seed | label | G mechanism (description only) | rule AUC | ceiling_full | ceiling_block | n_ge / n_valid | p_S | p_P | n_deg | lambda ko | code |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R | 92100 | R | - | 1.0000 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| R | 92101 | R | - | 1.0000 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| R | 92102 | R | - | 1.0000 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| R | 92103 | R | - | 1.0000 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| R | 92104 | R | - | 0.9990 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| Nf | 92110 | G | no information (rule #2.1's ceiling_full = 0.9854 >= 0.90) | 0.5366 | 0.9854 | 1.0000 | 64 / 99 | 0.65 | 0.3081 | 0 | 100.0 | ok |
| Nf | 92111 | G | orthogonal (rule #2.1's ceiling_full = 0.4927 < 0.90) | 0.4951 | 0.4927 | 1.0000 | 44 / 99 | 0.45 | 0.5323 | 0 | 100.0 | ok |
| Nf | 92112 | G | orthogonal (rule #2.1's ceiling_full = 0.4961 < 0.90) | 0.4990 | 0.4961 | 1.0000 | 45 / 99 | 0.46 | 0.5081 | 0 | 100.0 | ok |
| Nf | 92113 | G | no information (rule #2.1's ceiling_full = 0.9951 >= 0.90) | 0.4990 | 0.9951 | 1.0000 | 62 / 99 | 0.63 | 0.5043 | 0 | 100.0 | ok |
| Nf | 92114 | G | no information (rule #2.1's ceiling_full = 0.9814 >= 0.90) | 0.5103 | 0.9814 | 1.0000 | 13 / 99 | 0.14 | 0.4516 | 0 | 100.0 | ok |
| No | 92120 | G | orthogonal (rule #2.1's ceiling_full = 0.5010 < 0.90) | 0.4893 | 0.5010 | 1.0000 | 97 / 99 | 0.98 | 0.5612 | 0 | 1.0 | ok |
| No | 92121 | G | orthogonal (rule #2.1's ceiling_full = 0.5127 < 0.90) | 0.5117 | 0.5127 | 1.0000 | 4 / 99 | 0.05 | 0.4430 | 0 | 1.0 | ok |
| No | 92122 | G | orthogonal (rule #2.1's ceiling_full = 0.4995 < 0.90) | 0.5039 | 0.4995 | 1.0000 | 96 / 99 | 0.97 | 0.4869 | 0 | 1.0 | ok |
| No | 92123 | G | orthogonal (rule #2.1's ceiling_full = 0.5166 < 0.90) | 0.5117 | 0.5166 | 1.0000 | 1 / 99 | 0.02 | 0.4420 | 0 | 1.0 | ok |
| No | 92124 | G | orthogonal (rule #2.1's ceiling_full = 0.4922 < 0.90) | 0.4902 | 0.4922 | 1.0000 | 93 / 99 | 0.94 | 0.5535 | 0 | 1.0 | ok |
| W | 92130 | W | - | 0.5146 | 0.5195 | 1.0000 | 60 / 99 | 0.61 | 0.4191 | 0 | 1.0 | ok |
| W | 92131 | W | - | 0.5088 | 0.5068 | 1.0000 | 3 / 99 | 0.04 | 0.4516 | 0 | 1.0 | ok |
| W | 92132 | W | - | 0.5234 | 0.5322 | 1.0000 | 1 / 99 | 0.02 | 0.3797 | 0 | 1.0 | ok |
| W | 92133 | W | - | 0.5322 | 0.5430 | 1.0000 | 10 / 99 | 0.11 | 0.3323 | 0 | 1.0 | ok |
| W | 92134 | W | - | 0.4814 | 0.4834 | 1.0000 | 94 / 99 | 0.95 | 0.6009 | 0 | 1.0 | ok |
| M0.5 | 92140 | G | no information (rule #2.1's ceiling_full = 0.9814 >= 0.90) | 0.5210 | 0.9814 | 1.0000 | 23 / 99 | 0.24 | 0.3957 | 0 | 100.0 | curve |
| M0.5 | 92141 | U | - | 0.6343 | 0.9912 | 1.0000 | 0 / 99 | 0.01 | 0.0332 | 0 | 3.0 | curve |
| M0.5 | 92142 | R | - | 0.6719 | 0.9990 | 1.0000 | 0 / 99 | 0.01 | 0.0077 | 0 | 3.0 | curve |
| M0.5 | 92143 | G | no information (rule #2.1's ceiling_full = 1.0000 >= 0.90) | 0.5137 | 1.0000 | 1.0000 | 66 / 99 | 0.67 | 0.4253 | 0 | 100.0 | curve |
| M0.5 | 92144 | U | - | 0.6636 | 0.9805 | 1.0000 | 0 / 99 | 0.01 | 0.0117 | 0 | 3.0 | curve |
| M0.6 | 92160 | G | no information (rule #2.1's ceiling_full = 1.0000 >= 0.90) | 0.5820 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.1278 | 0 | 3.0 | curve |
| M0.6 | 92161 | G | no information (rule #2.1's ceiling_full = 0.9404 >= 0.90) | 0.5913 | 0.9404 | 1.0000 | 0 / 99 | 0.01 | 0.1066 | 0 | 3.0 | curve |
| M0.6 | 92162 | R | - | 0.7422 | 0.9951 | 1.0000 | 0 / 99 | 0.01 | 0.0003 | 0 | 3.0 | curve |
| M0.6 | 92163 | U | - | 0.6416 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0242 | 0 | 3.0 | curve |
| M0.6 | 92164 | R | - | 0.6758 | 0.9961 | 1.0000 | 0 / 99 | 0.01 | 0.0065 | 0 | 3.0 | curve |
| M0.75 | 92170 | R | - | 0.7578 | 0.9990 | 1.0000 | 0 / 99 | 0.01 | 0.0004 | 0 | 3.0 | curve |
| M0.75 | 92171 | R | - | 0.6685 | 0.9541 | 1.0000 | 0 / 99 | 0.01 | 0.0094 | 0 | 3.0 | curve |
| M0.75 | 92172 | U | - | 0.6895 | 0.9990 | 1.0000 | 0 / 99 | 0.01 | 0.0034 | 0 | 3.0 | curve |
| M0.75 | 92173 | U | - | 0.6807 | 0.9600 | 1.0000 | 0 / 99 | 0.01 | 0.0061 | 0 | 3.0 | curve |
| M0.75 | 92174 | R | - | 0.6963 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0032 | 0 | 3.0 | curve |
| M0.85 | 92180 | R | - | 0.9028 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |
| M0.85 | 92181 | R | - | 0.7715 | 0.9912 | 1.0000 | 0 / 99 | 0.01 | 0.0005 | 0 | 3.0 | curve |
| M0.85 | 92182 | R | - | 0.7314 | 0.9668 | 1.0000 | 0 / 99 | 0.01 | 0.0008 | 0 | 3.0 | curve |
| M0.85 | 92183 | R | - | 0.7246 | 0.9834 | 1.0000 | 0 / 99 | 0.01 | 0.0008 | 0 | 3.0 | curve |
| M0.85 | 92184 | G | no information (rule #2.1's ceiling_full = 0.9863 >= 0.90) | 0.5420 | 0.9863 | 1.0000 | 1 / 99 | 0.02 | 0.2872 | 0 | 3.0 | curve |
| M1.0 | 92150 | R | - | 0.9219 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |
| M1.0 | 92151 | R | - | 0.9453 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |
| M1.0 | 92152 | R | - | 0.8330 | 0.9873 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |
| M1.0 | 92153 | R | - | 0.9336 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |
| M1.0 | 92154 | R | - | 0.8896 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |

| family | requirement | labels read (R/W/G/U) | meet (min) | stop labels | result |
|---|---|---|---|---|---|
| R | each of 5 worlds reads R, on both D1 candidates | 5/0/0/0 | 5/5 (5) | 0 | no stop |
| Nf | never R or W (stop); at least 3 of 5 read G | 0/0/5/0 | 5/5 (3) | 0 | no stop |
| No | never R or W (stop); reads G; a U triggers the No contingency | 0/0/5/0 | 5/5 (0) | 0 | no stop |
| W | each of 5 worlds reads W, on both D1 candidates | 0/5/0/0 | 5/5 (5) | 0 | no stop |
| M0.5 | power curve: printed, no stop row; the three limits are taken from it | 1/0/2/2 | n/a (power curve) | 0 | no stop |
| M0.6 | power curve: printed, no stop row; the three limits are taken from it | 2/0/2/1 | n/a (power curve) | 0 | no stop |
| M0.75 | power curve: printed, no stop row; the three limits are taken from it | 3/0/0/2 | n/a (power curve) | 0 | no stop |
| M0.85 | power curve: printed, no stop row; the three limits are taken from it | 4/0/1/0 | n/a (power curve) | 0 | no stop |
| M1.0 | power curve: printed, no stop row; the three limits are taken from it | 5/0/0/0 | n/a (power curve) | 0 | no stop |

Pre-run table (section 7, revisions 3.2, 3.3): outcome 1: every deciding column equal; byte-identical (recorded, not gated); rows matched by family/j/seed/predictor: 0 missing now, 0 missing in the pre-run table, row order equal (a fact, not an outcome); mechanism_description differs on 0 rows (reported, not gated) (passed: True; byte-identical: True; pinned e8476a936356d3965aa5715d7f04a82c3587ff0795569db81071822fbca9cae0, recomputed e8476a936356d3965aa5715d7f04a82c3587ff0795569db81071822fbca9cae0).

Per-fit diagnostic against the lobe's pre-run raw fits (diagnostic, decides nothing): {'pinned': 28665, 'missing_now': 0, 'compared': 28665, 'fitted_this_pass': 28665, 'p_differ': 0, 'lambda_differ': 0, 'labels_differ': 0, 'score_differ': 0, 'outside_density_differ': 0, 'reused_from_ko_differ': 0, 'max_abs_dp': 0.0}; by kind {'pc': 900, 'block': 270, 'sh': 26730, 'ko': 270, 'full': 270, 'ko1': 225}.

Two-world check passed: True. No contingency triggered: False.

## Power curve and the three limits (section 3.6, revision 3.1)

| gamma | family | seen/n (rule #2.1 p_P <= 0.01) | R/n | seen/n BF_1, BF_2, BF_3, BF_4 | R/W/G/U | rule AUC | rule lambda ko |
|---|---|---|---|---|---|---|---|
| 0.0 | Nf (anchor) | 0/5 | 0/5 | 0/5, 0/5, 0/5, 0/5 | 0/0/5/0 | 0.537, 0.495, 0.499, 0.499, 0.510 | 100, 100, 100, 100, 100 |
| 0.5 | M0.5 | 1/5 | 1/5 | 1/5, 1/5, 0/5, 0/5 | 1/0/2/2 | 0.521, 0.634, 0.672, 0.514, 0.664 | 100, 3, 3, 100, 3 |
| 0.6 | M0.6 | 2/5 | 2/5 | 2/5, 1/5, 1/5, 1/5 | 2/0/2/1 | 0.582, 0.591, 0.742, 0.642, 0.676 | 3, 3, 3, 3, 3 |
| 0.75 | M0.75 | 5/5 | 3/5 | 3/5, 4/5, 3/5, 4/5 | 3/0/0/2 | 0.758, 0.668, 0.689, 0.681, 0.696 | 3, 3, 3, 3, 3 |
| 0.85 | M0.85 | 4/5 | 4/5 | 4/5, 4/5, 4/5, 4/5 | 4/0/1/0 | 0.903, 0.771, 0.731, 0.725, 0.542 | 1, 3, 3, 3, 3 |
| 1.0 | M1.0 | 5/5 | 5/5 | 5/5, 5/5, 5/5, 5/5 | 5/0/0/0 | 0.922, 0.945, 0.833, 0.934, 0.890 | 1, 1, 1, 1, 1 |
| 2.0 | R (anchor) | 5/5 | 5/5 | 5/5, 5/5, 5/5, 5/5 | 5/0/0/0 | 1.000, 1.000, 1.000, 1.000, 0.999 | 1, 1, 1, 1, 1 |

**The three limits** (in M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10):

- gamma*_P, the leg-P limit (rule #2.1 p_P <= 0.01 in a majority of the worlds): **0.75**, bracket (0.6, 0.75]; majority seen at every grid gamma above it: True.
- gamma_R (a majority of the worlds read R): **0.75**, bracket (0.6, 0.75]; majority R at every grid gamma above it: True.
- family limit (the largest leg-P limit: the maximum of each predictor's own leg-P limit): **0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4)**. Per predictor: rule #2.1 0.75, BF_1 0.75, BF_2 0.75, BF_3 0.75, BF_4 0.75. The limits use p_P <= 0.01 for every predictor and are not family-corrected, unlike the W gate (p_P <= 0.0125 = 0.05/4): a limit is a property of the instrument, not of a branch (revision 3.2).
- transition band [gamma*_P, gamma_R): empty: the two limits coincide (0 grid steps, 0 in gamma). Dense-grid worlds that read U: 0 inside the band, 3 below it, 2 above it. The band is the difference of two limits, each uncertain by about one grid step, so a one-step band is one of 0, 1 or 2 steps (revision 3.2).
- per gamma, seen/n and R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5.
- binomial note: with n = 5 worlds per gamma a limit has an error of about one grid step: a true detection probability of 0.2 or 0.4 gives '>= 3 of 5' with probability 0.06 or 0.32 (Johnny).
- M worlds that read G at or above gamma*_P: 1 (M0.85 92184); at or above gamma_R: 1 (M0.85 92184) (printed, no stop).
- grid complete: True.

**U rule:** threshold U read by 5 of 25 dense-grid worlds (5 threshold U, 0 failed fit, 0 ceiling_block not measured, 0 not readable): U stays; its frequency is printed. U is read as 'on the detection threshold; cannot be separated', the signature of the leg-P detection limit gamma*_P (revisions 3.1, 3.2), except a U whose reasons include rule #2.1's ceiling_block below 0.90, which reads 'failed fit: rule #2.1 cannot hold the block even when trained on it alone', and a U whose ceiling_block was not measured, which reads 'not measured: rule #2.1's ceiling_block was not measured; the G gate cannot be read' (revision 3.3). U across all 45 worlds: 5 (R 0/5, Nf 0/5, No 0/5, W 0/5, M0.5 2/5, M1.0 0/5, M0.6 1/5, M0.75 2/5, M0.85 0/5).

## Fixed lambda = 1 on the knockout view (section 3.5): diagnostic, decides nothing

Printed beside the limits, not on any verdict line. Where the selected lambda was 1 the selected fit is reused (path check: {'bank': 'world:W:0', 'identical': {'rule': True, 'BF:1': True, 'BF:2': True, 'BF:3': True, 'BF:4': True}, 'passed': True}).

| family | predictor | AUC at lambda 1 (per world) | mean | p_P <= 0.01 at lambda 1 | selected lambda | mean AUC selected | p_P <= 0.01 selected |
|---|---|---|---|---|---|---|---|
| R | rule #2.1 | 1.000, 1.000, 1.000, 1.000, 0.999 | 1.000 | 5/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 1.000 | 5/5 |
| R | BF_1 | 1.000, 1.000, 1.000, 1.000, 0.993 | 0.999 | 5/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.999 | 5/5 |
| R | BF_2 | 0.997, 1.000, 1.000, 0.992, 0.986 | 0.995 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.995 | 5/5 |
| R | BF_3 | 0.996, 0.998, 0.994, 0.979, 0.993 | 0.992 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.994 | 5/5 |
| R | BF_4 | 0.999, 0.984, 0.944, 0.993, 1.000 | 0.984 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.994 | 5/5 |
| Nf | rule #2.1 | 0.569, 0.513, 0.462, 0.500, 0.581 | 0.525 | 0/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.508 | 0/5 |
| Nf | BF_1 | 0.581, 0.502, 0.472, 0.499, 0.590 | 0.529 | 0/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.505 | 0/5 |
| Nf | BF_2 | 0.534, 0.452, 0.480, 0.538, 0.580 | 0.517 | 0/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.505 | 0/5 |
| Nf | BF_3 | 0.513, 0.354, 0.414, 0.494, 0.545 | 0.464 | 0/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.505 | 0/5 |
| Nf | BF_4 | 0.513, 0.401, 0.419, 0.456, 0.540 | 0.466 | 0/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.505 | 0/5 |
| No | rule #2.1 | 0.489, 0.512, 0.504, 0.512, 0.490 | 0.501 | 0/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.501 | 0/5 |
| No | BF_1 | 0.485, 0.506, 0.501, 0.516, 0.490 | 0.500 | 0/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.500 | 0/5 |
| No | BF_2 | 0.469, 0.519, 0.494, 0.544, 0.510 | 0.507 | 0/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.502 | 0/5 |
| No | BF_3 | 0.486, 0.497, 0.492, 0.524, 0.503 | 0.501 | 0/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.505 | 0/5 |
| No | BF_4 | 0.469, 0.502, 0.498, 0.535, 0.485 | 0.498 | 0/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.497 | 0/5 |
| W | rule #2.1 | 0.515, 0.509, 0.523, 0.532, 0.481 | 0.512 | 0/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.512 | 0/5 |
| W | BF_1 | 0.514, 0.510, 0.518, 0.532, 0.466 | 0.508 | 0/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.508 | 0/5 |
| W | BF_2 | 0.780, 0.802, 0.751, 0.722, 0.737 | 0.758 | 5/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.758 | 5/5 |
| W | BF_3 | 0.770, 0.819, 0.771, 0.696, 0.641 | 0.739 | 4/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.739 | 4/5 |
| W | BF_4 | 0.743, 0.805, 0.727, 0.721, 0.619 | 0.723 | 4/5 | 1.0, 3.0, 3.0, 3.0, 1.0 | 0.706 | 4/5 |
| M0.5 | rule #2.1 | 0.522, 0.743, 0.738, 0.678, 0.675 | 0.671 | 4/5 | 100.0, 3.0, 3.0, 100.0, 3.0 | 0.601 | 1/5 |
| M0.5 | BF_1 | 0.523, 0.760, 0.760, 0.671, 0.693 | 0.681 | 4/5 | 100.0, 3.0, 3.0, 100.0, 3.0 | 0.603 | 1/5 |
| M0.5 | BF_2 | 0.601, 0.560, 0.792, 0.519, 0.681 | 0.630 | 2/5 | 100.0, 3.0, 3.0, 100.0, 3.0 | 0.594 | 1/5 |
| M0.5 | BF_3 | 0.607, 0.534, 0.705, 0.478, 0.577 | 0.580 | 1/5 | 100.0, 3.0, 100.0, 100.0, 100.0 | 0.525 | 0/5 |
| M0.5 | BF_4 | 0.584, 0.464, 0.701, 0.459, 0.636 | 0.569 | 1/5 | 100.0, 3.0, 100.0, 100.0, 3.0 | 0.544 | 0/5 |
| M1.0 | rule #2.1 | 0.922, 0.945, 0.833, 0.934, 0.890 | 0.905 | 5/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.905 | 5/5 |
| M1.0 | BF_1 | 0.916, 0.955, 0.839, 0.932, 0.878 | 0.904 | 5/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.904 | 5/5 |
| M1.0 | BF_2 | 0.733, 0.942, 0.868, 0.929, 0.817 | 0.858 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.813 | 5/5 |
| M1.0 | BF_3 | 0.725, 0.950, 0.750, 0.938, 0.762 | 0.825 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.801 | 5/5 |
| M1.0 | BF_4 | 0.725, 0.904, 0.741, 0.943, 0.737 | 0.810 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.796 | 5/5 |
| M0.6 | rule #2.1 | 0.671, 0.675, 0.848, 0.748, 0.776 | 0.744 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.647 | 2/5 |
| M0.6 | BF_1 | 0.701, 0.661, 0.825, 0.740, 0.786 | 0.743 | 4/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.655 | 2/5 |
| M0.6 | BF_2 | 0.581, 0.643, 0.828, 0.703, 0.728 | 0.696 | 3/5 | 3.0, 3.0, 3.0, 3.0, 100.0 | 0.602 | 1/5 |
| M0.6 | BF_3 | 0.656, 0.614, 0.800, 0.646, 0.704 | 0.684 | 2/5 | 3.0, 100.0, 3.0, 3.0, 100.0 | 0.585 | 1/5 |
| M0.6 | BF_4 | 0.646, 0.610, 0.786, 0.608, 0.704 | 0.671 | 2/5 | 3.0, 3.0, 3.0, 3.0, 100.0 | 0.594 | 1/5 |
| M0.75 | rule #2.1 | 0.863, 0.732, 0.781, 0.717, 0.751 | 0.769 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.699 | 5/5 |
| M0.75 | BF_1 | 0.881, 0.721, 0.766, 0.724, 0.782 | 0.775 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.696 | 3/5 |
| M0.75 | BF_2 | 0.830, 0.718, 0.810, 0.653, 0.756 | 0.753 | 4/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.696 | 4/5 |
| M0.75 | BF_3 | 0.791, 0.668, 0.771, 0.597, 0.686 | 0.703 | 4/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.674 | 3/5 |
| M0.75 | BF_4 | 0.758, 0.662, 0.789, 0.598, 0.722 | 0.706 | 3/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.685 | 4/5 |
| M0.85 | rule #2.1 | 0.903, 0.838, 0.824, 0.765, 0.550 | 0.776 | 4/5 | 1.0, 3.0, 3.0, 3.0, 3.0 | 0.734 | 4/5 |
| M0.85 | BF_1 | 0.889, 0.854, 0.807, 0.768, 0.569 | 0.777 | 4/5 | 1.0, 3.0, 3.0, 3.0, 3.0 | 0.737 | 4/5 |
| M0.85 | BF_2 | 0.834, 0.821, 0.800, 0.739, 0.564 | 0.752 | 4/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.709 | 4/5 |
| M0.85 | BF_3 | 0.771, 0.805, 0.793, 0.713, 0.562 | 0.729 | 4/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.710 | 4/5 |
| M0.85 | BF_4 | 0.745, 0.822, 0.777, 0.639, 0.578 | 0.712 | 3/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.709 | 4/5 |

Fits: 0 re-read from saved fits, 28440 new world fits, fixed lambda: 49 reused, 171 fitted.

### World R, seed 92100: R: regrows

Outside density 0.2942; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 1.0000 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 1.0000 (32/32) | 3.303 | 0.2866 | +0.4796 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 1.0000 (32/32) | 2.991 | 0.2726 | +0.4936 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.9941 (32/32) | 2.231 | 0.3488 | +0.4174 | 0.969 | 1.0000 | 1.0000 | 0.99 | 0.99 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.9941 (32/32) | 2.266 | 0.3452 | +0.4210 | 0.969 | 1.0000 | 1.0000 | 0.99 | 0.99 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.9961 (32/32) | 2.258 | 0.3456 | +0.4206 | 0.969 | 1.0000 | 1.0000 | 0.99 | 0.99 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4961 (32/32) | 0.000 | 0.7662 | +0.0000 | 0.531 | 0.4961 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5231 | 0.5966 | None / None / None |

### World R, seed 92101: R: regrows

Outside density 0.2844; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 1.0000 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 1.0000 (32/32) | 3.227 | 0.2859 | +0.4726 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 1.0000 (32/32) | 2.949 | 0.2744 | +0.4841 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 1.0000 (32/32) | 2.202 | 0.3540 | +0.4045 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 1.0000 (32/32) | 2.212 | 0.3518 | +0.4067 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.9990 (32/32) | 2.197 | 0.3569 | +0.4016 | 0.969 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5273 (32/32) | 0.000 | 0.7585 | +0.0000 | 0.500 | 0.5215 | 0.5000 | 1.27 | n/a | 99 / 99 | 1.00 | 0.3490 | 0.0538 | None / None / None |

### World R, seed 92102: R: regrows

Outside density 0.2834; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 1.0000 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 1.0000 (32/32) | 2.866 | 0.3775 | +0.4377 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 1.0000 (32/32) | 2.515 | 0.3621 | +0.4531 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 1.0000 (32/32) | 1.947 | 0.4321 | +0.3832 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 1.0000 (32/32) | 1.960 | 0.4369 | +0.3783 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.9932 (32/32) | 1.925 | 0.4471 | +0.3681 | 0.938 | 1.0000 | 1.0000 | 0.99 | 0.99 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4893 (32/32) | 0.000 | 0.8152 | +0.0000 | 0.469 | 0.4893 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5676 | 0.7611 | None / None / None |

### World R, seed 92103: R: regrows

Outside density 0.2830; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 1.0000 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 1.0000 (32/32) | 3.387 | 0.2777 | +0.4882 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 1.0000 (32/32) | 2.984 | 0.2593 | +0.5067 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.9990 (32/32) | 2.289 | 0.3404 | +0.4256 | 0.969 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.9961 (32/32) | 2.253 | 0.3464 | +0.4196 | 0.969 | 1.0000 | 1.0000 | 0.99 | 0.99 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.9990 (32/32) | 2.298 | 0.3343 | +0.4317 | 0.969 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5020 (32/32) | 0.000 | 0.7659 | +0.0000 | 0.531 | 0.4990 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.4922 | 0.4473 | None / None / None |

### World R, seed 92104: R: regrows

Outside density 0.3012; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.9990 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.9990 (32/32) | 3.386 | 0.2818 | +0.4895 | 0.969 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.9932 (32/32) | 3.032 | 0.2835 | +0.4878 | 0.969 | 1.0000 | 1.0000 | 0.99 | 0.99 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.9824 (32/32) | 2.266 | 0.3620 | +0.4093 | 0.938 | 1.0000 | 1.0000 | 0.96 | 0.96 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.9805 (32/32) | 2.261 | 0.3624 | +0.4089 | 0.906 | 1.0000 | 1.0000 | 0.96 | 0.96 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.9834 (32/32) | 2.291 | 0.3592 | +0.4121 | 0.969 | 1.0000 | 1.0000 | 0.97 | 0.97 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5254 (32/32) | 0.000 | 0.7713 | +0.0000 | 0.500 | 0.5264 | 0.5000 | 0.96 | n/a | 99 / 99 | 1.00 | 0.3711 | 0.0921 | None / None / None |

### World Nf, seed 92110: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1810; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 0.9854 >= 0.90)]. rule #2.1: AUC = 0.5366 (32/32), p_S = 0.65 (n_ge = 64 of 99, n_deg = 0), p_P = 0.3081; ceiling_full = 0.9854, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5366 (32/32) | 0.000 | 0.8937 | +0.0020 | 0.562 | 0.9854 | 1.0000 | 0.08 | 0.07 | 64 / 99 | 0.65 | 0.3081 | 0.0302 | 100.0 / 3.0 / 1.0 |
| BF_1 | 0.5391 (32/32) | 0.000 | 0.8956 | +0.0000 | 0.562 | 0.9893 | 1.0000 | 0.08 | 0.08 | 98 / 99 | 0.99 | 0.2934 | 0.0217 | 100.0 / 3.0 / 1.0 |
| BF_2 | 0.5391 (32/32) | 0.000 | 0.8956 | +0.0000 | 0.562 | 0.5352 | 1.0000 | 1.11 | 0.08 | 99 / 99 | 1.00 | 0.2934 | 0.0217 | 100.0 / 100.0 / 1.0 |
| BF_3 | 0.5391 (32/32) | 0.000 | 0.8956 | +0.0000 | 0.562 | 0.5352 | 1.0000 | 1.11 | 0.08 | 99 / 99 | 1.00 | 0.2934 | 0.0217 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.5391 (32/32) | 0.000 | 0.8956 | +0.0000 | 0.562 | 0.5352 | 1.0000 | 1.11 | 0.08 | 99 / 99 | 1.00 | 0.2934 | 0.0217 | 100.0 / 100.0 / 1.0 |
| N1 | 0.5391 (32/32) | 0.000 | 0.8956 | +0.0000 | 0.562 | 0.5352 | 0.5000 | 1.11 | n/a | 99 / 99 | 1.00 | 0.2934 | 0.0217 | None / None / None |

### World Nf, seed 92111: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1837; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.4927 < 0.90)]. rule #2.1: AUC = 0.4951 (32/32), p_S = 0.45 (n_ge = 44 of 99, n_deg = 0), p_P = 0.5323; ceiling_full = 0.4927, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4951 (32/32) | 0.000 | 0.8649 | +0.0032 | 0.531 | 0.4927 | 1.0000 | n/a | -0.01 | 44 / 99 | 0.45 | 0.5323 | 0.6054 | 100.0 / 100.0 / 1.0 |
| BF_1 | 0.4961 (32/32) | 0.000 | 0.8681 | +0.0000 | 0.500 | 0.4951 | 1.0000 | n/a | -0.01 | 96 / 99 | 0.97 | 0.5262 | 0.5849 | 100.0 / 100.0 / 1.0 |
| BF_2 | 0.4961 (32/32) | 0.000 | 0.8681 | +0.0000 | 0.500 | 0.4951 | 1.0000 | n/a | -0.01 | 97 / 99 | 0.98 | 0.5262 | 0.5849 | 100.0 / 100.0 / 1.0 |
| BF_3 | 0.4961 (32/32) | 0.000 | 0.8681 | +0.0000 | 0.500 | 0.4951 | 1.0000 | n/a | -0.01 | 97 / 99 | 0.98 | 0.5262 | 0.5849 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.4961 (32/32) | 0.000 | 0.8681 | +0.0000 | 0.500 | 0.4951 | 1.0000 | n/a | -0.01 | 98 / 99 | 0.99 | 0.5262 | 0.5849 | 100.0 / 100.0 / 1.0 |
| N1 | 0.4961 (32/32) | 0.000 | 0.8681 | +0.0000 | 0.500 | 0.4951 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5262 | 0.5849 | None / None / None |

### World Nf, seed 92112: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1824; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.4961 < 0.90)]. rule #2.1: AUC = 0.4990 (32/32), p_S = 0.46 (n_ge = 45 of 99, n_deg = 0), p_P = 0.5081; ceiling_full = 0.4961, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4990 (32/32) | 0.000 | 0.8748 | +0.0035 | 0.469 | 0.4961 | 1.0000 | n/a | -0.00 | 45 / 99 | 0.46 | 0.5081 | 0.5330 | 100.0 / 100.0 / 1.0 |
| BF_1 | 0.4961 (32/32) | 0.000 | 0.8783 | +0.0000 | 0.469 | 0.5020 | 1.0000 | -2.00 | -0.01 | 96 / 99 | 0.97 | 0.5245 | 0.5976 | 100.0 / 100.0 / 1.0 |
| BF_2 | 0.4961 (32/32) | 0.000 | 0.8783 | +0.0000 | 0.469 | 0.5020 | 1.0000 | -2.00 | -0.01 | 98 / 99 | 0.99 | 0.5245 | 0.5976 | 100.0 / 100.0 / 1.0 |
| BF_3 | 0.4961 (32/32) | 0.000 | 0.8783 | +0.0000 | 0.469 | 0.5020 | 1.0000 | -2.00 | -0.01 | 99 / 99 | 1.00 | 0.5245 | 0.5976 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.4961 (32/32) | 0.000 | 0.8783 | +0.0000 | 0.469 | 1.0000 | 1.0000 | -0.01 | -0.01 | 99 / 99 | 1.00 | 0.5245 | 0.5976 | 100.0 / 3.0 / 1.0 |
| N1 | 0.4961 (32/32) | 0.000 | 0.8783 | +0.0000 | 0.469 | 0.5020 | 0.5000 | -2.00 | n/a | 99 / 99 | 1.00 | 0.5245 | 0.5976 | None / None / None |

### World Nf, seed 92113: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1841; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 0.9951 >= 0.90)]. rule #2.1: AUC = 0.4990 (32/32), p_S = 0.63 (n_ge = 62 of 99, n_deg = 0), p_P = 0.5043; ceiling_full = 0.9951, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4990 (32/32) | 0.000 | 0.8753 | -0.0081 | 0.531 | 0.9951 | 1.0000 | -0.00 | -0.00 | 62 / 99 | 0.63 | 0.5043 | 0.5377 | 100.0 / 3.0 / 1.0 |
| BF_1 | 0.4990 (32/32) | 0.000 | 0.8673 | +0.0000 | 0.531 | 1.0000 | 1.0000 | -0.00 | -0.00 | 93 / 99 | 0.94 | 0.5070 | 0.5438 | 100.0 / 3.0 / 1.0 |
| BF_2 | 0.4990 (32/32) | 0.000 | 0.8673 | +0.0000 | 0.531 | 0.4980 | 1.0000 | n/a | -0.00 | 97 / 99 | 0.98 | 0.5070 | 0.5438 | 100.0 / 100.0 / 1.0 |
| BF_3 | 0.4990 (32/32) | 0.000 | 0.8673 | +0.0000 | 0.531 | 0.4980 | 1.0000 | n/a | -0.00 | 99 / 99 | 1.00 | 0.5070 | 0.5438 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.4990 (32/32) | 0.000 | 0.8673 | +0.0000 | 0.531 | 0.4980 | 1.0000 | n/a | -0.00 | 98 / 99 | 0.99 | 0.5070 | 0.5438 | 100.0 / 100.0 / 1.0 |
| N1 | 0.4990 (32/32) | 0.000 | 0.8673 | +0.0000 | 0.531 | 0.4980 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5070 | 0.5438 | None / None / None |

### World Nf, seed 92114: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1746; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 0.9814 >= 0.90)]. rule #2.1: AUC = 0.5103 (32/32), p_S = 0.14 (n_ge = 13 of 99, n_deg = 0), p_P = 0.4516; ceiling_full = 0.9814, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5103 (32/32) | 0.000 | 0.8979 | +0.0079 | 0.469 | 0.9814 | 1.0000 | 0.02 | 0.02 | 13 / 99 | 0.14 | 0.4516 | 0.3127 | 100.0 / 3.0 / 1.0 |
| BF_1 | 0.4941 (32/32) | 0.000 | 0.9058 | +0.0000 | 0.406 | 0.9844 | 1.0000 | -0.01 | -0.01 | 96 / 99 | 0.97 | 0.5340 | 0.6073 | 100.0 / 3.0 / 1.0 |
| BF_2 | 0.4941 (32/32) | 0.000 | 0.9058 | +0.0000 | 0.406 | 0.9746 | 1.0000 | -0.01 | -0.01 | 99 / 99 | 1.00 | 0.5340 | 0.6073 | 100.0 / 3.0 / 1.0 |
| BF_3 | 0.4941 (32/32) | 0.000 | 0.9058 | +0.0000 | 0.406 | 0.4941 | 1.0000 | n/a | -0.01 | 99 / 99 | 1.00 | 0.5340 | 0.6073 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.4941 (32/32) | 0.000 | 0.9058 | +0.0000 | 0.406 | 0.4941 | 1.0000 | n/a | -0.01 | 99 / 99 | 1.00 | 0.5340 | 0.6073 | 100.0 / 100.0 / 1.0 |
| N1 | 0.4941 (32/32) | 0.000 | 0.9058 | +0.0000 | 0.406 | 0.4941 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5340 | 0.6073 | None / None / None |

### World No, seed 92120: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.3063; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5010 < 0.90)]. rule #2.1: AUC = 0.4893 (32/32), p_S = 0.98 (n_ge = 97 of 99, n_deg = 0), p_P = 0.5612; ceiling_full = 0.5010, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4893 (32/32) | -0.033 | 1.3039 | -0.4888 | 0.500 | 0.5010 | 1.0000 | -11.00 | -0.02 | 97 / 99 | 0.98 | 0.5612 | 0.5561 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.4854 (32/32) | -0.040 | 1.1378 | -0.3227 | 0.500 | 0.5039 | 1.0000 | -3.75 | -0.03 | 98 / 99 | 0.99 | 0.5841 | 0.5807 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.4834 (32/32) | -0.048 | 0.9949 | -0.1798 | 0.531 | 0.8027 | 1.0000 | -0.05 | -0.03 | 99 / 99 | 1.00 | 0.6001 | 0.5995 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.4951 (32/32) | -0.047 | 0.9942 | -0.1791 | 0.531 | 0.8877 | 1.0000 | -0.01 | -0.01 | 99 / 99 | 1.00 | 0.5366 | 0.5323 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.4902 (32/32) | -0.046 | 0.9923 | -0.1772 | 0.531 | 0.9023 | 1.0000 | -0.02 | -0.02 | 99 / 99 | 1.00 | 0.5615 | 0.5563 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5088 (32/32) | 0.000 | 0.8151 | +0.0000 | 0.562 | 0.5059 | 0.5000 | 1.50 | n/a | 99 / 99 | 1.00 | 0.4544 | 0.2828 | None / None / None |

### World No, seed 92121: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.2945; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5127 < 0.90)]. rule #2.1: AUC = 0.5117 (32/32), p_S = 0.05 (n_ge = 4 of 99, n_deg = 0), p_P = 0.4430; ceiling_full = 0.5127, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5117 (32/32) | 0.050 | 1.1600 | -0.3293 | 0.469 | 0.5127 | 1.0000 | 0.92 | 0.02 | 4 / 99 | 0.05 | 0.4430 | 0.4367 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5059 (32/32) | 0.033 | 1.0518 | -0.2212 | 0.469 | 0.5176 | 1.0000 | 0.33 | 0.01 | 2 / 99 | 0.03 | 0.4761 | 0.4722 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.5117 (32/32) | 0.035 | 0.9483 | -0.1176 | 0.500 | 0.8701 | 1.0000 | 0.03 | 0.02 | 0 / 99 | 0.01 | 0.4462 | 0.4289 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5000 (32/32) | 0.000 | 0.9593 | -0.1286 | 0.500 | 0.9004 | 1.0000 | 0.00 | 0.00 | 0 / 99 | 0.01 | 0.5061 | 0.5055 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.4961 (32/32) | -0.003 | 0.9577 | -0.1270 | 0.500 | 0.9248 | 1.0000 | -0.01 | -0.01 | 0 / 99 | 0.01 | 0.5264 | 0.5265 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4951 (32/32) | 0.000 | 0.8307 | +0.0000 | 0.469 | 0.4922 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5329 | 0.6235 | None / None / None |

### World No, seed 92122: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.2888; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.4995 < 0.90)]. rule #2.1: AUC = 0.5039 (32/32), p_S = 0.97 (n_ge = 96 of 99, n_deg = 0), p_P = 0.4869; ceiling_full = 0.4995, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5039 (32/32) | -0.009 | 1.1766 | -0.4308 | 0.500 | 0.4995 | 1.0000 | n/a | 0.01 | 96 / 99 | 0.97 | 0.4869 | 0.4810 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5010 (32/32) | -0.008 | 1.0411 | -0.2953 | 0.500 | 0.5059 | 1.0000 | 0.17 | 0.00 | 98 / 99 | 0.99 | 0.5046 | 0.4982 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.5078 (32/32) | 0.000 | 0.9284 | -0.1826 | 0.500 | 0.9141 | 1.0000 | 0.02 | 0.02 | 98 / 99 | 0.99 | 0.4688 | 0.4527 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5068 (32/32) | -0.002 | 0.9286 | -0.1828 | 0.500 | 0.9238 | 1.0000 | 0.02 | 0.01 | 99 / 99 | 1.00 | 0.4740 | 0.4634 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.5068 (32/32) | 0.001 | 0.9309 | -0.1851 | 0.500 | 0.9287 | 1.0000 | 0.02 | 0.01 | 99 / 99 | 1.00 | 0.4733 | 0.4653 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5293 (32/32) | 0.000 | 0.7458 | +0.0000 | 0.562 | 0.5293 | 0.5000 | 1.00 | n/a | 99 / 99 | 1.00 | 0.3447 | 0.0158 | None / None / None |

### World No, seed 92123: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.3016; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5166 < 0.90)]. rule #2.1: AUC = 0.5117 (32/32), p_S = 0.02 (n_ge = 1 of 99, n_deg = 0), p_P = 0.4420; ceiling_full = 0.5166, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5117 (32/32) | -0.015 | 1.0966 | -0.2929 | 0.500 | 0.5166 | 1.0000 | 0.71 | 0.02 | 1 / 99 | 0.02 | 0.4420 | 0.4413 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5156 (32/32) | -0.008 | 0.9937 | -0.1900 | 0.500 | 0.5156 | 1.0000 | 1.00 | 0.03 | 1 / 99 | 0.02 | 0.4229 | 0.4240 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.5137 (32/32) | 0.042 | 0.8941 | -0.0904 | 0.500 | 0.8682 | 1.0000 | 0.04 | 0.03 | 0 / 99 | 0.01 | 0.4309 | 0.4292 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5176 (32/32) | 0.050 | 0.8954 | -0.0917 | 0.469 | 0.9219 | 1.0000 | 0.04 | 0.04 | 0 / 99 | 0.01 | 0.4091 | 0.4121 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.5029 (32/32) | 0.069 | 0.8941 | -0.0905 | 0.500 | 0.9336 | 1.0000 | 0.01 | 0.01 | 0 / 99 | 0.01 | 0.4907 | 0.4858 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4834 (32/32) | 0.000 | 0.8037 | +0.0000 | 0.500 | 0.4824 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5955 | 0.9101 | None / None / None |

### World No, seed 92124: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.2874; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.4922 < 0.90)]. rule #2.1: AUC = 0.4902 (32/32), p_S = 0.94 (n_ge = 93 of 99, n_deg = 0), p_P = 0.5535; ceiling_full = 0.4922, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4902 (32/32) | 0.007 | 1.1513 | -0.3838 | 0.500 | 0.4922 | 1.0000 | n/a | -0.02 | 93 / 99 | 0.94 | 0.5535 | 0.5588 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.4902 (32/32) | 0.010 | 1.0292 | -0.2616 | 0.500 | 0.4922 | 1.0000 | n/a | -0.02 | 97 / 99 | 0.98 | 0.5511 | 0.5539 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.4941 (32/32) | 0.001 | 0.9273 | -0.1598 | 0.500 | 0.8857 | 1.0000 | -0.02 | -0.01 | 99 / 99 | 1.00 | 0.5370 | 0.5338 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5049 (32/32) | 0.010 | 0.9280 | -0.1605 | 0.500 | 0.8887 | 1.0000 | 0.01 | 0.01 | 99 / 99 | 1.00 | 0.4759 | 0.4747 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.4902 (32/32) | -0.013 | 0.9414 | -0.1738 | 0.500 | 0.9082 | 1.0000 | -0.02 | -0.02 | 99 / 99 | 1.00 | 0.5593 | 0.5590 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5127 (32/32) | 0.000 | 0.7675 | +0.0000 | 0.531 | 0.5117 | 0.5000 | 1.08 | n/a | 99 / 99 | 1.00 | 0.4301 | 0.2166 | None / None / None |

### World W, seed 92130: W: rule weaker than the information available

Outside density 0.3384; block present 32.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.5146 (32/32), p_S = 0.61 (n_ge = 60 of 99, n_deg = 0), p_P = 0.4191; ceiling_full = 0.5195, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 1.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5146 (32/32) | 0.164 | 0.9294 | -0.2081 | 0.500 | 0.5195 | 1.0000 | 0.75 | 0.03 | 60 / 99 | 0.61 | 0.4191 | 0.4343 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5137 (32/32) | 0.159 | 0.8770 | -0.1557 | 0.500 | 0.5273 | 1.0000 | 0.50 | 0.03 | 99 / 99 | 1.00 | 0.4262 | 0.4407 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7803 (32/32) | 2.234 | 0.5737 | +0.1476 | 0.625 | 0.9648 | 1.0000 | 0.60 | 0.56 | 0 / 99 | 0.01 | 0.0001 | 0.0004 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.7695 (32/32) | 2.147 | 0.6404 | +0.0809 | 0.625 | 0.9756 | 1.0000 | 0.57 | 0.54 | 0 / 99 | 0.01 | 0.0001 | 0.0004 | 1.0 / 1.0 / 1.0 |
| BF_4 | 0.7432 (32/32) | 2.037 | 0.7230 | -0.0017 | 0.594 | 0.9814 | 1.0000 | 0.51 | 0.49 | 0 / 99 | 0.01 | 0.0005 | 0.0011 | 1.0 / 1.0 / 1.0 |
| N1 | 0.5176 (32/32) | 0.000 | 0.7213 | +0.0000 | 0.531 | 0.5156 | 0.5000 | 1.12 | n/a | 99 / 99 | 1.00 | 0.4105 | 0.1126 | None / None / None |

### World W, seed 92131: W: rule weaker than the information available

Outside density 0.3222; block present 32.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.5088 (32/32), p_S = 0.04 (n_ge = 3 of 99, n_deg = 0), p_P = 0.4516; ceiling_full = 0.5068, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5088 (32/32) | 0.001 | 1.0351 | -0.2719 | 0.500 | 0.5068 | 1.0000 | 1.29 | 0.02 | 3 / 99 | 0.04 | 0.4516 | 0.4434 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5098 (32/32) | 0.006 | 0.9376 | -0.1744 | 0.500 | 0.5078 | 1.0000 | 1.25 | 0.02 | 0 / 99 | 0.01 | 0.4440 | 0.4399 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.8018 (32/32) | 2.120 | 0.5623 | +0.2009 | 0.656 | 0.9932 | 1.0000 | 0.61 | 0.60 | 0 / 99 | 0.01 | 0.0001 | 0.0002 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.8193 (32/32) | 2.292 | 0.5942 | +0.1691 | 0.688 | 1.0000 | 1.0000 | 0.64 | 0.64 | 0 / 99 | 0.01 | 0.0001 | 0.0002 | 1.0 / 1.0 / 1.0 |
| BF_4 | 0.7773 (32/32) | 1.156 | 0.6434 | +0.1199 | 0.656 | 0.9736 | 1.0000 | 0.59 | 0.55 | 0 / 99 | 0.01 | 0.0002 | 0.0002 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4736 (32/32) | 0.000 | 0.7632 | +0.0000 | 0.438 | 0.4736 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.6468 | 0.9889 | None / None / None |

### World W, seed 92132: W: rule weaker than the information available

Outside density 0.3381; block present 32.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.5234 (32/32), p_S = 0.02 (n_ge = 1 of 99, n_deg = 0), p_P = 0.3797; ceiling_full = 0.5322, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5234 (32/32) | 0.167 | 1.0006 | -0.2461 | 0.500 | 0.5322 | 1.0000 | 0.73 | 0.05 | 1 / 99 | 0.02 | 0.3797 | 0.3943 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5176 (32/32) | 0.186 | 0.9159 | -0.1614 | 0.500 | 0.5283 | 1.0000 | 0.62 | 0.04 | 0 / 99 | 0.01 | 0.4105 | 0.4229 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7510 (32/32) | 1.843 | 0.6112 | +0.1433 | 0.562 | 0.9688 | 1.0000 | 0.54 | 0.50 | 0 / 99 | 0.01 | 0.0005 | 0.0011 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.7705 (32/32) | 2.138 | 0.6252 | +0.1293 | 0.594 | 0.9961 | 1.0000 | 0.55 | 0.54 | 0 / 99 | 0.01 | 0.0002 | 0.0003 | 1.0 / 1.0 / 1.0 |
| BF_4 | 0.7119 (32/32) | 0.922 | 0.6794 | +0.0751 | 0.562 | 0.9658 | 1.0000 | 0.45 | 0.42 | 0 / 99 | 0.01 | 0.0019 | 0.0043 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5010 (32/32) | 0.000 | 0.7545 | +0.0000 | 0.500 | 0.5039 | 0.5000 | 0.25 | n/a | 99 / 99 | 1.00 | 0.4944 | 0.4858 | None / None / None |

### World W, seed 92133: W: rule weaker than the information available

Outside density 0.3252; block present 32.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.5322 (32/32), p_S = 0.11 (n_ge = 10 of 99, n_deg = 0), p_P = 0.3323; ceiling_full = 0.5430, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5322 (32/32) | 0.198 | 1.1408 | -0.3651 | 0.500 | 0.5430 | 1.0000 | 0.75 | 0.06 | 10 / 99 | 0.11 | 0.3323 | 0.3479 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5322 (32/32) | 0.232 | 1.0247 | -0.2489 | 0.500 | 0.5391 | 1.0000 | 0.82 | 0.06 | 0 / 99 | 0.01 | 0.3307 | 0.3471 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7217 (32/32) | 1.790 | 0.7444 | +0.0314 | 0.562 | 0.9316 | 1.0000 | 0.51 | 0.44 | 0 / 99 | 0.01 | 0.0018 | 0.0031 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.6963 (32/32) | 1.731 | 0.8275 | -0.0518 | 0.562 | 0.9834 | 1.0000 | 0.41 | 0.39 | 0 / 99 | 0.01 | 0.0035 | 0.0071 | 1.0 / 1.0 / 1.0 |
| BF_4 | 0.6807 (32/32) | 0.903 | 0.7377 | +0.0380 | 0.562 | 0.9414 | 1.0000 | 0.41 | 0.36 | 0 / 99 | 0.01 | 0.0071 | 0.0110 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5215 (32/32) | 0.000 | 0.7757 | +0.0000 | 0.531 | 0.5205 | 0.5000 | 1.05 | n/a | 99 / 99 | 1.00 | 0.3858 | 0.0385 | None / None / None |

### World W, seed 92134: W: rule weaker than the information available

Outside density 0.3256; block present 32.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.4814 (32/32), p_S = 0.95 (n_ge = 94 of 99, n_deg = 0), p_P = 0.6009; ceiling_full = 0.4834, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 1.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4814 (32/32) | 0.009 | 1.1936 | -0.4630 | 0.500 | 0.4834 | 1.0000 | n/a | -0.04 | 94 / 99 | 0.95 | 0.6009 | 0.6041 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.4658 (32/32) | 0.014 | 1.0824 | -0.3518 | 0.500 | 0.4775 | 1.0000 | n/a | -0.07 | 98 / 99 | 0.99 | 0.6809 | 0.6779 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7373 (32/32) | 1.496 | 0.7994 | -0.0688 | 0.500 | 0.8398 | 1.0000 | 0.70 | 0.47 | 0 / 99 | 0.01 | 0.0009 | 0.0019 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.6406 (32/32) | 1.152 | 0.9201 | -0.1895 | 0.531 | 0.8965 | 1.0000 | 0.35 | 0.28 | 0 / 99 | 0.01 | 0.0287 | 0.0431 | 1.0 / 1.0 / 1.0 |
| BF_4 | 0.6191 (32/32) | 1.109 | 1.0086 | -0.2780 | 0.531 | 0.9609 | 1.0000 | 0.26 | 0.24 | 0 / 99 | 0.01 | 0.0564 | 0.0747 | 1.0 / 1.0 / 1.0 |
| N1 | 0.5078 (32/32) | 0.000 | 0.7306 | +0.0000 | 0.500 | 0.5068 | 0.5000 | 1.14 | n/a | 99 / 99 | 1.00 | 0.4623 | 0.3162 | None / None / None |

### World M0.5, seed 92140: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1807; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 0.9814 >= 0.90)]. rule #2.1: AUC = 0.5210 (32/32), p_S = 0.24 (n_ge = 23 of 99, n_deg = 0), p_P = 0.3957; ceiling_full = 0.9814, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5210 (32/32) | 0.000 | 0.8066 | -0.0011 | 0.531 | 0.9814 | 1.0000 | 0.04 | 0.04 | 23 / 99 | 0.24 | 0.3957 | 0.0395 | 100.0 / 3.0 / 1.0 |
| BF_1 | 0.5117 (32/32) | 0.000 | 0.8056 | +0.0000 | 0.562 | 0.9893 | 1.0000 | 0.02 | 0.02 | 94 / 99 | 0.95 | 0.4478 | 0.1852 | 100.0 / 3.0 / 1.0 |
| BF_2 | 0.5117 (32/32) | 0.000 | 0.8056 | +0.0000 | 0.562 | 0.9980 | 1.0000 | 0.02 | 0.02 | 99 / 99 | 1.00 | 0.4478 | 0.1852 | 100.0 / 3.0 / 1.0 |
| BF_3 | 0.5117 (32/32) | 0.000 | 0.8056 | +0.0000 | 0.562 | 1.0000 | 1.0000 | 0.02 | 0.02 | 99 / 99 | 1.00 | 0.4478 | 0.1852 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.5117 (32/32) | 0.000 | 0.8056 | +0.0000 | 0.562 | 0.9990 | 1.0000 | 0.02 | 0.02 | 99 / 99 | 1.00 | 0.4478 | 0.1852 | 100.0 / 3.0 / 1.0 |
| N1 | 0.5117 (32/32) | 0.000 | 0.8056 | +0.0000 | 0.562 | 0.5166 | 0.5000 | 0.71 | n/a | 99 / 99 | 1.00 | 0.4478 | 0.1852 | None / None / None |

### World M0.5, seed 92141: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma))

Outside density 0.1996; block present 32.
Verdict line: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma)). rule #2.1: AUC = 0.6343 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0332; ceiling_full = 0.9912, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6343 (32/32) | 0.304 | 0.8327 | +0.0699 | 0.594 | 0.9912 | 1.0000 | 0.27 | 0.27 | 0 / 99 | 0.01 | 0.0332 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6602 (32/32) | 0.353 | 0.8232 | +0.0794 | 0.656 | 0.9951 | 1.0000 | 0.32 | 0.32 | 0 / 99 | 0.01 | 0.0134 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.5889 (32/32) | 0.150 | 0.8774 | +0.0253 | 0.562 | 0.9951 | 1.0000 | 0.18 | 0.18 | 0 / 99 | 0.01 | 0.1126 | 0.0187 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5771 (32/32) | 0.140 | 0.8827 | +0.0199 | 0.531 | 0.9980 | 1.0000 | 0.15 | 0.15 | 0 / 99 | 0.01 | 0.1465 | 0.0441 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.5615 (32/32) | 0.119 | 0.8918 | +0.0108 | 0.500 | 0.9980 | 1.0000 | 0.12 | 0.12 | 0 / 99 | 0.01 | 0.2031 | 0.0917 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5254 (32/32) | 0.000 | 0.9026 | +0.0000 | 0.562 | 0.5244 | 0.5000 | 1.04 | n/a | 99 / 99 | 1.00 | 0.3668 | 0.0815 | None / None / None |

### World M0.5, seed 92142: R: regrows

Outside density 0.1807; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.6719 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0077; ceiling_full = 0.9990, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 100, BF_4 100.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6719 (32/32) | 0.356 | 0.8551 | +0.0880 | 0.625 | 0.9990 | 1.0000 | 0.34 | 0.34 | 0 / 99 | 0.01 | 0.0077 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6709 (32/32) | 0.379 | 0.8546 | +0.0886 | 0.656 | 1.0000 | 1.0000 | 0.34 | 0.34 | 0 / 99 | 0.01 | 0.0079 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.7109 (32/32) | 0.497 | 0.8300 | +0.1132 | 0.656 | 1.0000 | 1.0000 | 0.42 | 0.42 | 0 / 99 | 0.01 | 0.0017 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.4902 (32/32) | 0.000 | 0.9432 | +0.0000 | 0.500 | 1.0000 | 1.0000 | -0.02 | -0.02 | 99 / 99 | 1.00 | 0.5619 | 0.7635 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.4902 (32/32) | 0.000 | 0.9432 | +0.0000 | 0.500 | 1.0000 | 1.0000 | -0.02 | -0.02 | 99 / 99 | 1.00 | 0.5619 | 0.7635 | 100.0 / 3.0 / 1.0 |
| N1 | 0.4902 (32/32) | 0.000 | 0.9432 | +0.0000 | 0.500 | 0.4941 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5619 | 0.7635 | None / None / None |

### World M0.5, seed 92143: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1874; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 1.0000 >= 0.90)]. rule #2.1: AUC = 0.5137 (32/32), p_S = 0.67 (n_ge = 66 of 99, n_deg = 0), p_P = 0.4253; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5137 (32/32) | 0.000 | 1.0010 | -0.0011 | 0.562 | 1.0000 | 1.0000 | 0.03 | 0.03 | 66 / 99 | 0.67 | 0.4253 | 0.0601 | 100.0 / 3.0 / 1.0 |
| BF_1 | 0.5186 (32/32) | 0.000 | 0.9999 | +0.0000 | 0.562 | 1.0000 | 1.0000 | 0.04 | 0.04 | 95 / 99 | 0.96 | 0.4021 | 0.0137 | 100.0 / 3.0 / 1.0 |
| BF_2 | 0.5186 (32/32) | 0.000 | 0.9999 | +0.0000 | 0.562 | 1.0000 | 1.0000 | 0.04 | 0.04 | 97 / 99 | 0.98 | 0.4021 | 0.0137 | 100.0 / 3.0 / 1.0 |
| BF_3 | 0.5186 (32/32) | 0.000 | 0.9999 | +0.0000 | 0.562 | 1.0000 | 1.0000 | 0.04 | 0.04 | 97 / 99 | 0.98 | 0.4021 | 0.0137 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.5186 (32/32) | 0.000 | 0.9999 | +0.0000 | 0.562 | 0.5078 | 1.0000 | 2.38 | 0.04 | 99 / 99 | 1.00 | 0.4021 | 0.0137 | 100.0 / 100.0 / 1.0 |
| N1 | 0.5186 (32/32) | 0.000 | 0.9999 | +0.0000 | 0.562 | 0.5078 | 0.5000 | 2.38 | n/a | 99 / 99 | 1.00 | 0.4021 | 0.0137 | None / None / None |

### World M0.5, seed 92144: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma))

Outside density 0.1861; block present 32.
Verdict line: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma)). rule #2.1: AUC = 0.6636 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0117; ceiling_full = 0.9805, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 100, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6636 (32/32) | 0.312 | 0.7459 | +0.0625 | 0.625 | 0.9805 | 1.0000 | 0.34 | 0.33 | 0 / 99 | 0.01 | 0.0117 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6523 (32/32) | 0.299 | 0.7448 | +0.0636 | 0.656 | 0.9873 | 1.0000 | 0.31 | 0.30 | 0 / 99 | 0.01 | 0.0183 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.6387 (32/32) | 0.311 | 0.7462 | +0.0622 | 0.594 | 0.9951 | 1.0000 | 0.28 | 0.28 | 0 / 99 | 0.01 | 0.0290 | 0.0014 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5293 (32/32) | 0.000 | 0.8084 | +0.0000 | 0.531 | 0.9932 | 1.0000 | 0.06 | 0.06 | 99 / 99 | 1.00 | 0.3476 | 0.0623 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.6357 (32/32) | 0.309 | 0.7546 | +0.0538 | 0.625 | 0.9941 | 1.0000 | 0.27 | 0.27 | 0 / 99 | 0.01 | 0.0305 | 0.0032 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5293 (32/32) | 0.000 | 0.8084 | +0.0000 | 0.531 | 0.5225 | 0.5000 | 1.30 | n/a | 99 / 99 | 1.00 | 0.3476 | 0.0623 | None / None / None |

### World M1.0, seed 92150: R: regrows

Outside density 0.2030; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.9219 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.9219 (32/32) | 1.996 | 0.5307 | +0.3366 | 0.875 | 1.0000 | 1.0000 | 0.84 | 0.84 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.9160 (32/32) | 1.878 | 0.5154 | +0.3518 | 0.875 | 1.0000 | 1.0000 | 0.83 | 0.83 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7783 (32/32) | 0.931 | 0.6848 | +0.1825 | 0.688 | 0.9971 | 1.0000 | 0.56 | 0.56 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7773 (32/32) | 0.917 | 0.6907 | +0.1766 | 0.750 | 0.9980 | 1.0000 | 0.56 | 0.55 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7734 (32/32) | 0.887 | 0.6986 | +0.1687 | 0.719 | 0.9990 | 1.0000 | 0.55 | 0.55 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5488 (32/32) | 0.000 | 0.8673 | +0.0000 | 0.500 | 0.5430 | 0.5000 | 1.14 | n/a | 99 / 99 | 1.00 | 0.2514 | 0.0038 | None / None / None |

### World M1.0, seed 92151: R: regrows

Outside density 0.2124; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.9453 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.9453 (32/32) | 2.149 | 0.4833 | +0.3686 | 0.875 | 1.0000 | 1.0000 | 0.89 | 0.89 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.9551 (32/32) | 1.960 | 0.4642 | +0.3877 | 0.906 | 1.0000 | 1.0000 | 0.91 | 0.91 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.8809 (32/32) | 1.146 | 0.5974 | +0.2545 | 0.781 | 1.0000 | 1.0000 | 0.76 | 0.76 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.8867 (32/32) | 1.190 | 0.5895 | +0.2624 | 0.844 | 1.0000 | 1.0000 | 0.77 | 0.77 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.8760 (32/32) | 1.167 | 0.5905 | +0.2615 | 0.781 | 1.0000 | 1.0000 | 0.75 | 0.75 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5127 (32/32) | 0.000 | 0.8519 | +0.0000 | 0.500 | 0.5127 | 0.5000 | 1.00 | n/a | 99 / 99 | 1.00 | 0.4300 | 0.1033 | None / None / None |

### World M1.0, seed 92152: R: regrows

Outside density 0.2145; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.8330 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 0.9873, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.8330 (32/32) | 1.680 | 0.5914 | +0.2775 | 0.750 | 0.9873 | 1.0000 | 0.68 | 0.67 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.8389 (32/32) | 1.612 | 0.5816 | +0.2872 | 0.781 | 0.9814 | 1.0000 | 0.70 | 0.68 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7773 (32/32) | 1.044 | 0.6597 | +0.2091 | 0.750 | 0.9805 | 1.0000 | 0.58 | 0.55 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7402 (32/32) | 0.904 | 0.6904 | +0.1784 | 0.656 | 0.9902 | 1.0000 | 0.49 | 0.48 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7266 (32/32) | 0.904 | 0.6948 | +0.1740 | 0.625 | 0.9941 | 1.0000 | 0.46 | 0.45 | 0 / 99 | 0.01 | 0.0006 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5273 (32/32) | 0.000 | 0.8688 | +0.0000 | 0.531 | 0.5264 | 0.5000 | 1.04 | n/a | 99 / 99 | 1.00 | 0.3539 | 0.0976 | None / None / None |

### World M1.0, seed 92153: R: regrows

Outside density 0.2013; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.9336 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.9336 (32/32) | 2.115 | 0.5050 | +0.3325 | 0.875 | 1.0000 | 1.0000 | 0.87 | 0.87 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.9316 (32/32) | 1.992 | 0.4822 | +0.3553 | 0.844 | 1.0000 | 1.0000 | 0.86 | 0.86 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.8721 (32/32) | 1.175 | 0.5844 | +0.2532 | 0.844 | 1.0000 | 1.0000 | 0.74 | 0.74 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.8750 (32/32) | 1.189 | 0.5813 | +0.2562 | 0.844 | 1.0000 | 1.0000 | 0.75 | 0.75 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.8955 (32/32) | 1.195 | 0.5797 | +0.2578 | 0.812 | 1.0000 | 1.0000 | 0.79 | 0.79 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5000 (32/32) | 0.000 | 0.8375 | +0.0000 | 0.531 | 0.4971 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5016 | 0.5121 | None / None / None |

### World M1.0, seed 92154: R: regrows

Outside density 0.2128; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.8896 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.8896 (32/32) | 1.328 | 0.6268 | +0.2568 | 0.750 | 1.0000 | 1.0000 | 0.78 | 0.78 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.8779 (32/32) | 1.152 | 0.6294 | +0.2542 | 0.750 | 1.0000 | 1.0000 | 0.76 | 0.76 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7559 (32/32) | 0.657 | 0.7366 | +0.1470 | 0.656 | 1.0000 | 1.0000 | 0.51 | 0.51 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7256 (32/32) | 0.611 | 0.7492 | +0.1345 | 0.656 | 1.0000 | 1.0000 | 0.45 | 0.45 | 0 / 99 | 0.01 | 0.0010 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7070 (32/32) | 0.600 | 0.7426 | +0.1410 | 0.625 | 1.0000 | 1.0000 | 0.41 | 0.41 | 0 / 99 | 0.01 | 0.0024 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4902 (32/32) | 0.000 | 0.8836 | +0.0000 | 0.469 | 0.4805 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5529 | 0.7733 | None / None / None |

### World M0.6, seed 92160: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1905; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 1.0000 >= 0.90)]. rule #2.1: AUC = 0.5820 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.1278; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5820 (32/32) | 0.286 | 0.7654 | +0.0788 | 0.500 | 1.0000 | 1.0000 | 0.16 | 0.16 | 0 / 99 | 0.01 | 0.1278 | 0.0002 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.5908 (32/32) | 0.267 | 0.7805 | +0.0637 | 0.500 | 1.0000 | 1.0000 | 0.18 | 0.18 | 0 / 99 | 0.01 | 0.1056 | 0.0004 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.5459 (32/32) | 0.174 | 0.8061 | +0.0381 | 0.500 | 1.0000 | 1.0000 | 0.09 | 0.09 | 1 / 99 | 0.02 | 0.2614 | 0.0927 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5615 (32/32) | 0.226 | 0.7890 | +0.0553 | 0.531 | 1.0000 | 1.0000 | 0.12 | 0.12 | 0 / 99 | 0.01 | 0.1973 | 0.0515 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.5576 (32/32) | 0.193 | 0.7944 | +0.0498 | 0.500 | 1.0000 | 1.0000 | 0.12 | 0.12 | 0 / 99 | 0.01 | 0.2123 | 0.0616 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4697 (32/32) | 0.000 | 0.8442 | +0.0000 | 0.438 | 0.4775 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.6636 | 0.9885 | None / None / None |

### World M0.6, seed 92161: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.2040; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 0.9404 >= 0.90)]. rule #2.1: AUC = 0.5913 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.1066; ceiling_full = 0.9404, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 100, BF_4 3; G reached through lambda = 100 on BF_3: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5913 (32/32) | 0.190 | 0.8183 | +0.0729 | 0.625 | 0.9404 | 1.0000 | 0.21 | 0.18 | 0 / 99 | 0.01 | 0.1066 | 0.0084 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.5869 (32/32) | 0.203 | 0.8213 | +0.0699 | 0.594 | 0.9482 | 1.0000 | 0.19 | 0.17 | 0 / 99 | 0.01 | 0.1212 | 0.0071 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.5537 (32/32) | 0.172 | 0.8321 | +0.0591 | 0.531 | 0.9736 | 1.0000 | 0.11 | 0.11 | 0 / 99 | 0.01 | 0.2393 | 0.0985 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5010 (32/32) | 0.000 | 0.8912 | +0.0000 | 0.531 | 0.9824 | 1.0000 | 0.00 | 0.00 | 99 / 99 | 1.00 | 0.4979 | 0.4804 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.5498 (32/32) | 0.185 | 0.8500 | +0.0413 | 0.531 | 0.9863 | 1.0000 | 0.10 | 0.10 | 0 / 99 | 0.01 | 0.2559 | 0.1125 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5010 (32/32) | 0.000 | 0.8912 | +0.0000 | 0.531 | 0.5029 | 0.5000 | 0.33 | n/a | 99 / 99 | 1.00 | 0.4979 | 0.4804 | None / None / None |

### World M0.6, seed 92162: R: regrows

Outside density 0.1834; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.7422 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0003; ceiling_full = 0.9951, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7422 (32/32) | 0.630 | 0.7210 | +0.1272 | 0.688 | 0.9951 | 1.0000 | 0.49 | 0.48 | 0 / 99 | 0.01 | 0.0003 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7646 (32/32) | 0.619 | 0.7157 | +0.1326 | 0.656 | 0.9990 | 1.0000 | 0.53 | 0.53 | 0 / 99 | 0.01 | 0.0003 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.7461 (32/32) | 0.637 | 0.7115 | +0.1367 | 0.656 | 0.9990 | 1.0000 | 0.49 | 0.49 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7373 (32/32) | 0.620 | 0.7205 | +0.1277 | 0.625 | 0.9990 | 1.0000 | 0.48 | 0.47 | 0 / 99 | 0.01 | 0.0006 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7422 (32/32) | 0.622 | 0.7205 | +0.1278 | 0.656 | 0.9990 | 1.0000 | 0.49 | 0.48 | 0 / 99 | 0.01 | 0.0005 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4785 (32/32) | 0.000 | 0.8482 | +0.0000 | 0.500 | 0.4814 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.6241 | 0.8747 | None / None / None |

### World M0.6, seed 92163: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma))

Outside density 0.1790; block present 32.
Verdict line: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma)). rule #2.1: AUC = 0.6416 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0242; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6416 (32/32) | 0.340 | 0.8420 | +0.0716 | 0.594 | 1.0000 | 1.0000 | 0.28 | 0.28 | 0 / 99 | 0.01 | 0.0242 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6465 (32/32) | 0.341 | 0.8342 | +0.0795 | 0.594 | 1.0000 | 1.0000 | 0.29 | 0.29 | 0 / 99 | 0.01 | 0.0207 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.6367 (32/32) | 0.351 | 0.8324 | +0.0812 | 0.594 | 1.0000 | 1.0000 | 0.27 | 0.27 | 0 / 99 | 0.01 | 0.0280 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5957 (32/32) | 0.258 | 0.8522 | +0.0615 | 0.531 | 1.0000 | 1.0000 | 0.19 | 0.19 | 0 / 99 | 0.01 | 0.0933 | 0.0016 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.5898 (32/32) | 0.247 | 0.8578 | +0.0558 | 0.531 | 1.0000 | 1.0000 | 0.18 | 0.18 | 0 / 99 | 0.01 | 0.1074 | 0.0022 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4805 (32/32) | 0.000 | 0.9136 | +0.0000 | 0.500 | 0.4844 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.6050 | 0.9221 | None / None / None |

### World M0.6, seed 92164: R: regrows

Outside density 0.1932; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.6758 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0065; ceiling_full = 0.9961, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 100, BF_3 100, BF_4 100.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6758 (32/32) | 0.320 | 0.7902 | +0.0737 | 0.594 | 0.9961 | 1.0000 | 0.35 | 0.35 | 0 / 99 | 0.01 | 0.0065 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6846 (32/32) | 0.321 | 0.7832 | +0.0807 | 0.625 | 0.9961 | 1.0000 | 0.37 | 0.37 | 0 / 99 | 0.01 | 0.0049 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.5283 (32/32) | 0.000 | 0.8639 | +0.0000 | 0.562 | 0.9971 | 1.0000 | 0.06 | 0.06 | 99 / 99 | 1.00 | 0.3552 | 0.0281 | 100.0 / 3.0 / 1.0 |
| BF_3 | 0.5283 (32/32) | 0.000 | 0.8639 | +0.0000 | 0.562 | 0.5225 | 1.0000 | 1.26 | 0.06 | 99 / 99 | 1.00 | 0.3552 | 0.0281 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.5283 (32/32) | 0.000 | 0.8639 | +0.0000 | 0.562 | 0.5225 | 1.0000 | 1.26 | 0.06 | 99 / 99 | 1.00 | 0.3552 | 0.0281 | 100.0 / 100.0 / 1.0 |
| N1 | 0.5283 (32/32) | 0.000 | 0.8639 | +0.0000 | 0.562 | 0.5225 | 0.5000 | 1.26 | n/a | 99 / 99 | 1.00 | 0.3552 | 0.0281 | None / None / None |

### World M0.75, seed 92170: R: regrows

Outside density 0.1979; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.7578 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0004; ceiling_full = 0.9990, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7578 (32/32) | 0.573 | 0.7888 | +0.1250 | 0.688 | 0.9990 | 1.0000 | 0.52 | 0.52 | 0 / 99 | 0.01 | 0.0004 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7637 (32/32) | 0.549 | 0.7854 | +0.1284 | 0.719 | 1.0000 | 1.0000 | 0.53 | 0.53 | 0 / 99 | 0.01 | 0.0003 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.7666 (32/32) | 0.561 | 0.7835 | +0.1303 | 0.750 | 0.9990 | 1.0000 | 0.53 | 0.53 | 0 / 99 | 0.01 | 0.0003 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7441 (32/32) | 0.540 | 0.7945 | +0.1193 | 0.719 | 0.9990 | 1.0000 | 0.49 | 0.49 | 0 / 99 | 0.01 | 0.0003 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7656 (32/32) | 0.555 | 0.7954 | +0.1184 | 0.719 | 0.9990 | 1.0000 | 0.53 | 0.53 | 0 / 99 | 0.01 | 0.0003 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4990 (32/32) | 0.000 | 0.9138 | +0.0000 | 0.500 | 0.4980 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5092 | 0.5257 | None / None / None |

### World M0.75, seed 92171: R: regrows

Outside density 0.1939; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.6685 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0094; ceiling_full = 0.9541, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6685 (32/32) | 0.394 | 0.8257 | +0.0839 | 0.594 | 0.9541 | 1.0000 | 0.37 | 0.34 | 0 / 99 | 0.01 | 0.0094 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6709 (32/32) | 0.379 | 0.8295 | +0.0801 | 0.656 | 0.9404 | 1.0000 | 0.39 | 0.34 | 0 / 99 | 0.01 | 0.0086 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.6855 (32/32) | 0.375 | 0.8307 | +0.0789 | 0.625 | 0.9580 | 1.0000 | 0.41 | 0.37 | 0 / 99 | 0.01 | 0.0041 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.6699 (32/32) | 0.358 | 0.8369 | +0.0728 | 0.625 | 0.9668 | 1.0000 | 0.36 | 0.34 | 0 / 99 | 0.01 | 0.0080 | 0.0002 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.6748 (32/32) | 0.365 | 0.8373 | +0.0724 | 0.625 | 0.9727 | 1.0000 | 0.37 | 0.35 | 0 / 99 | 0.01 | 0.0073 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5186 (32/32) | 0.000 | 0.9096 | +0.0000 | 0.469 | 0.5215 | 0.5000 | 0.86 | n/a | 99 / 99 | 1.00 | 0.4001 | 0.1804 | None / None / None |

### World M0.75, seed 92172: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma))

Outside density 0.1955; block present 32.
Verdict line: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma)). rule #2.1: AUC = 0.6895 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0034; ceiling_full = 0.9990, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6895 (32/32) | 0.505 | 0.7444 | +0.1026 | 0.656 | 0.9990 | 1.0000 | 0.38 | 0.38 | 0 / 99 | 0.01 | 0.0034 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6641 (32/32) | 0.484 | 0.7411 | +0.1058 | 0.625 | 1.0000 | 1.0000 | 0.33 | 0.33 | 0 / 99 | 0.01 | 0.0121 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.6855 (32/32) | 0.524 | 0.7333 | +0.1136 | 0.656 | 1.0000 | 1.0000 | 0.37 | 0.37 | 0 / 99 | 0.01 | 0.0046 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.6631 (32/32) | 0.504 | 0.7355 | +0.1114 | 0.594 | 1.0000 | 1.0000 | 0.33 | 0.33 | 0 / 99 | 0.01 | 0.0118 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.6992 (32/32) | 0.542 | 0.7277 | +0.1193 | 0.625 | 1.0000 | 1.0000 | 0.40 | 0.40 | 0 / 99 | 0.01 | 0.0030 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4648 (32/32) | 0.000 | 0.8470 | +0.0000 | 0.406 | 0.4736 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.6855 | 0.9988 | None / None / None |

### World M0.75, seed 92173: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma))

Outside density 0.2036; block present 32.
Verdict line: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma)). rule #2.1: AUC = 0.6807 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0061; ceiling_full = 0.9600, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6807 (32/32) | 0.337 | 0.7903 | +0.0716 | 0.656 | 0.9600 | 1.0000 | 0.39 | 0.36 | 0 / 99 | 0.01 | 0.0061 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6611 (32/32) | 0.310 | 0.7897 | +0.0722 | 0.594 | 0.9590 | 1.0000 | 0.35 | 0.32 | 0 / 99 | 0.01 | 0.0122 | 0.0002 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.6270 (32/32) | 0.217 | 0.8204 | +0.0415 | 0.562 | 0.9521 | 1.0000 | 0.28 | 0.25 | 0 / 99 | 0.01 | 0.0393 | 0.0057 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.6104 (32/32) | 0.191 | 0.8258 | +0.0361 | 0.625 | 0.9619 | 1.0000 | 0.24 | 0.22 | 0 / 99 | 0.01 | 0.0656 | 0.0148 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.6045 (32/32) | 0.186 | 0.8300 | +0.0319 | 0.625 | 0.9961 | 1.0000 | 0.21 | 0.21 | 0 / 99 | 0.01 | 0.0767 | 0.0264 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4814 (32/32) | 0.000 | 0.8619 | +0.0000 | 0.469 | 0.4834 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.6035 | 0.8357 | None / None / None |

### World M0.75, seed 92174: R: regrows

Outside density 0.1935; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.6963 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0032; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6963 (32/32) | 0.500 | 0.7980 | +0.0885 | 0.625 | 1.0000 | 1.0000 | 0.39 | 0.39 | 0 / 99 | 0.01 | 0.0032 | 0.0003 | 3.0 / 1.0 / 1.0 |
| BF_1 | 0.7217 (32/32) | 0.500 | 0.7875 | +0.0991 | 0.625 | 1.0000 | 1.0000 | 0.44 | 0.44 | 0 / 99 | 0.01 | 0.0009 | 0.0001 | 3.0 / 1.0 / 1.0 |
| BF_2 | 0.7168 (32/32) | 0.494 | 0.7897 | +0.0968 | 0.656 | 1.0000 | 1.0000 | 0.43 | 0.43 | 0 / 99 | 0.01 | 0.0014 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.6836 (32/32) | 0.402 | 0.8140 | +0.0725 | 0.656 | 1.0000 | 1.0000 | 0.37 | 0.37 | 0 / 99 | 0.01 | 0.0048 | 0.0006 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.6816 (32/32) | 0.400 | 0.8071 | +0.0795 | 0.656 | 1.0000 | 1.0000 | 0.36 | 0.36 | 0 / 99 | 0.01 | 0.0061 | 0.0006 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5273 (32/32) | 0.000 | 0.8866 | +0.0000 | 0.531 | 0.5059 | 0.5000 | 4.67 | n/a | 99 / 99 | 1.00 | 0.3486 | 0.0611 | None / None / None |

### World M0.85, seed 92180: R: regrows

Outside density 0.1905; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.9028 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.9028 (32/32) | 1.227 | 0.6320 | +0.2247 | 0.812 | 1.0000 | 1.0000 | 0.81 | 0.81 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.8887 (32/32) | 1.159 | 0.6198 | +0.2369 | 0.812 | 1.0000 | 1.0000 | 0.78 | 0.78 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7891 (32/32) | 0.747 | 0.6941 | +0.1626 | 0.719 | 1.0000 | 1.0000 | 0.58 | 0.58 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7793 (32/32) | 0.742 | 0.6939 | +0.1628 | 0.688 | 0.9961 | 1.0000 | 0.56 | 0.56 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7754 (32/32) | 0.724 | 0.7038 | +0.1529 | 0.656 | 0.9971 | 1.0000 | 0.55 | 0.55 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4980 (32/32) | 0.000 | 0.8567 | +0.0000 | 0.500 | 0.4932 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5168 | 0.5584 | None / None / None |

### World M0.85, seed 92181: R: regrows

Outside density 0.1996; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.7715 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0005; ceiling_full = 0.9912, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7715 (32/32) | 0.691 | 0.6603 | +0.1512 | 0.750 | 0.9912 | 1.0000 | 0.55 | 0.54 | 0 / 99 | 0.01 | 0.0005 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7764 (32/32) | 0.641 | 0.6675 | +0.1440 | 0.719 | 0.9922 | 1.0000 | 0.56 | 0.55 | 0 / 99 | 0.01 | 0.0003 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.7471 (32/32) | 0.592 | 0.6834 | +0.1281 | 0.688 | 0.9961 | 1.0000 | 0.50 | 0.49 | 0 / 99 | 0.01 | 0.0003 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7520 (32/32) | 0.633 | 0.6771 | +0.1344 | 0.719 | 0.9941 | 1.0000 | 0.51 | 0.50 | 0 / 99 | 0.01 | 0.0004 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7705 (32/32) | 0.636 | 0.6756 | +0.1359 | 0.750 | 0.9941 | 1.0000 | 0.55 | 0.54 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5117 (32/32) | 0.000 | 0.8115 | +0.0000 | 0.469 | 0.5166 | 0.5000 | 0.71 | n/a | 99 / 99 | 1.00 | 0.4478 | 0.2676 | None / None / None |

### World M0.85, seed 92182: R: regrows

Outside density 0.1925; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.7314 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0008; ceiling_full = 0.9668, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7314 (32/32) | 0.662 | 0.7489 | +0.1374 | 0.719 | 0.9668 | 1.0000 | 0.50 | 0.46 | 0 / 99 | 0.01 | 0.0008 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7334 (32/32) | 0.647 | 0.7451 | +0.1411 | 0.750 | 0.9678 | 1.0000 | 0.50 | 0.47 | 0 / 99 | 0.01 | 0.0007 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.7480 (32/32) | 0.641 | 0.7434 | +0.1429 | 0.750 | 0.9971 | 1.0000 | 0.50 | 0.50 | 0 / 99 | 0.01 | 0.0005 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7510 (32/32) | 0.716 | 0.7331 | +0.1532 | 0.750 | 0.9980 | 1.0000 | 0.50 | 0.50 | 0 / 99 | 0.01 | 0.0006 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7461 (32/32) | 0.704 | 0.7440 | +0.1422 | 0.719 | 0.9971 | 1.0000 | 0.50 | 0.49 | 0 / 99 | 0.01 | 0.0008 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5059 (32/32) | 0.000 | 0.8862 | +0.0000 | 0.500 | 0.4980 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.4774 | 0.3852 | None / None / None |

### World M0.85, seed 92183: R: regrows

Outside density 0.1989; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.7246 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0008; ceiling_full = 0.9834, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7246 (32/32) | 0.413 | 0.8232 | +0.0995 | 0.688 | 0.9834 | 1.0000 | 0.46 | 0.45 | 0 / 99 | 0.01 | 0.0008 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7197 (32/32) | 0.414 | 0.8294 | +0.0933 | 0.688 | 0.9814 | 1.0000 | 0.46 | 0.44 | 0 / 99 | 0.01 | 0.0008 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.7070 (32/32) | 0.418 | 0.8268 | +0.0959 | 0.625 | 0.9873 | 1.0000 | 0.42 | 0.41 | 0 / 99 | 0.01 | 0.0016 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7080 (32/32) | 0.414 | 0.8247 | +0.0979 | 0.656 | 0.9941 | 1.0000 | 0.42 | 0.42 | 0 / 99 | 0.01 | 0.0015 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.6777 (32/32) | 0.346 | 0.8423 | +0.0804 | 0.625 | 1.0000 | 1.0000 | 0.36 | 0.36 | 0 / 99 | 0.01 | 0.0061 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5078 (32/32) | 0.000 | 0.9226 | +0.0000 | 0.500 | 0.5068 | 0.5000 | 1.14 | n/a | 99 / 99 | 1.00 | 0.4598 | 0.3366 | None / None / None |

### World M0.85, seed 92184: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1928; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 2/5, 2/5; 0.75: 5/5, 3/5; 0.85: 4/5, 4/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 0.9863 >= 0.90)]. rule #2.1: AUC = 0.5420 (32/32), p_S = 0.02 (n_ge = 1 of 99, n_deg = 0), p_P = 0.2872; ceiling_full = 0.9863, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5420 (32/32) | 0.184 | 0.8650 | +0.0142 | 0.500 | 0.9863 | 1.0000 | 0.09 | 0.08 | 1 / 99 | 0.02 | 0.2872 | 0.1733 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.5664 (32/32) | 0.191 | 0.8477 | +0.0315 | 0.500 | 0.9961 | 1.0000 | 0.13 | 0.13 | 0 / 99 | 0.01 | 0.1863 | 0.0805 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.5547 (32/32) | 0.197 | 0.8466 | +0.0326 | 0.531 | 0.9961 | 1.0000 | 0.11 | 0.11 | 0 / 99 | 0.01 | 0.2321 | 0.1270 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5586 (32/32) | 0.204 | 0.8469 | +0.0323 | 0.562 | 0.9961 | 1.0000 | 0.12 | 0.12 | 0 / 99 | 0.01 | 0.2196 | 0.1305 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.5762 (32/32) | 0.224 | 0.8518 | +0.0274 | 0.562 | 0.9990 | 1.0000 | 0.15 | 0.15 | 0 / 99 | 0.01 | 0.1527 | 0.0554 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5020 (32/32) | 0.000 | 0.8792 | +0.0000 | 0.531 | 0.5029 | 0.5000 | 0.67 | n/a | 99 / 99 | 1.00 | 0.4941 | 0.4484 | None / None / None |

## The registered reading of this arm (section 4, quoted)

> ## 4. Reading rule
>
> ### 4.1 Per lobe: A §4, verbatim, with five stated differences
>
> A §4 applies **verbatim** to each lobe: the four branches in order, R and W on both D1 candidates,
> the cuts (`P_R` = 0.01, `P_W` = 0.0125, `P_G` = 0.10, `GATE_CUT` = 0.90, `MECHANISM_CUT` = 0.90),
> the U rule's naming (per lobe, on that lobe's dense grid), the verdict line's contents, λ on the
> verdict line, the No contingency (per lobe). No condition, cut or existing label string changes.
> Five differences (D12; the fifth added by revision 1.3, frozen before unsealing):
>
> 1. **A lobe prefix.** Each verdict line starts "male CNS, lobe ℓ (existence bank at c* = 2.99436):".
> 2. **A new U text** for a block on which leg P cannot pass (§3.2): "U: not readable: leg P cannot
>    reach p_P <= 0.01 on this block (n_present = k of 64)". It takes precedence over G, is never
>    renamed by the U rule and is not a threshold U. A lobe whose block has no AUC stops with "BLOCK
>    HAS NO AUC" and has no label (check 3).
> 3. **The quoted rows carry A's literals.** A's G row says "by Johnny's count the information is
>    there (64/64 inferable)", which holds on the male banks too (§1.4); its U row says "all 3
>    pre-run U worlds sit at γ = 0.6 = γ\*_P" and "by §2.4 this is a failure of the fit, since the
>    block is rank 1". The script prints, after each quoted row, one line naming which literals are
>    A's (the flyvis-65 pre-run U worlds; "the block is rank 1") and giving the lobe's own values.
>    The rows are quoted from the amended A, never from this file, which holds none of them
>    (script change S2, D12).
> 4. **"Failed fit" on a male block** keeps its text ("failed fit: rule #2.1 cannot hold the block
>    even when trained on it alone"), which states the measurement; it is read as "a failed fit or a
>    rank limit, not separated", since the male block is not known to be rank 1 (B's D9).
> 5. **A threshold U on the male banks (revision 1.3, frozen before unsealing; Ark, Zcode).** On
>    both male banks γ\*_P = γ_R = the family limit = 0.75, so the transition band [γ\*_P, γ_R) is
>    **empty by construction**, and every U world of the pre-run lies at or below the limit (lobe L
>    7: 3 at γ 0.5, 3 at 0.6, 1 at 0.75; lobe R 5: 2 at 0.5, 1 at 0.6, 2 at 0.75; none above;
>    §3.3.1 (d)). A's reading of U, "the signature of the leg-P detection limit γ\*_P" (A §4,
>    revisions 3.1, 3.2; A's three U worlds sat on γ\*_P = 0.6, inside a one-step band), does not
>    hold here. **On the male arm a threshold U reads "not detected at the R level: the two legs,
>    or the two D1 candidates, disagree", with no position on a threshold** (not "at the
>    threshold"). It is not read as "below the limit" either: it says only that R was not reached
>    and that the evidence is split; in the worlds that happened at γ from 0.5 up to the limit. The
>    label string stays A's ("U: on the detection threshold; cannot be separated", with the lobe's
>    limits); the script prints, after the quoted row and the A-literals line, one line with this
>    reading and the lobe's band, the γ of its U worlds and how many lie at and above the family
>    limit (S29). It applies to a threshold U only: a failed-fit U, a not-measured U, the "not
>    readable" U and a renamed U keep their own texts. If the registered run's synthetic step gave
>    a non-empty band (it cannot while it reproduces the references), the line says so and claims
>    nothing.
>
> **Leg S in every branch (revision 1.1, frozen before unsealing; Ark, Zcode).** "The primary passes
> leg S" means the count, `n_ge = 0` of the `99 − n_deg` shuffles with an AUC (A §4's own wording;
> `knockout_regrow.py:1067`), never `p_S <= 0.01`. `p_S` is printed beside it as information, with
> four decimals and a mark when `n_deg` >= 1 (§3.2, S28). This is not a further difference: A's rule
> is the count; the arm only prints `p_S` so that it cannot be misread as the deciding quantity.
>
> ### 4.2 The two lobes: one run, two labels, one male reading (proposals, D2, D3)
>
> **One invocation, both lobes (D2).** Both lobes' synthetic steps run and must pass before either
> sealed file is opened; then both blocks are unsealed and both real arms run, in one invocation from
> one committed head with one manifest (§7.4). So neither lobe's verdict is seen before the other's
> run is fixed. Each lobe gets its own label by §4.1.
>
> **The male reading (D3), from the two lobe labels:**
>
> | lobe L | lobe R | male reading |
> |---|---|---|
> | R | R | **R: regrows in both lobes of one animal** (builder D12 (i): an R on the male CNS needs R in both lobes) |
> | W | W | **W** in both lobes; the ranks that passed are printed per lobe |
> | G | G | **G** in both lobes, each with its own limits |
> | U | U | **U** in both lobes, each with its own U text |
> | any other pair | | **split: "lobe L reads X, lobe R reads Y"**, with the classification of §4.3. A split is not R, W or G on the male CNS. **Revision 1.3:** a split by reading, not a block difference; the two are printed apart (§4.3, "Two objects"; S32) |
> | a lobe with no AUC or "not readable" | | **one lobe only: "lobe ℓ reads X; lobe ℓ′ cannot be read (reason)"**. Not a male R even if X is R |
>
> **The male R is a conjunction of two A criteria (revision 1.1, frozen before unsealing; Johnny,
> Ark, Zcode).** A male R requires A's R in lobe L **and** A's R in lobe R. What that does, stated
> before data:
>
> - **Power: lower than a single-bank R, and not calibrated.** Both lobes must pass both legs on
>   both D1 candidates. The synthetic worlds measure each lobe's R on 32/32 boards (§3.6); no
>   registered quantity measures the joint R rate on the real blocks, whose shape is sealed.
> - **Null: not squared.** If the two lobes were independent tests, each with a false-R rate near
>   `P_R` = 0.01, a false "R in both" would be about 1e-4. They are not independent: both lobes use
>   one permutation matrix (seed 92000), one set of shuffle seeds and boards, and nearly the same
>   outside (493 of lobe R's 526 present outside cells are present in lobe L too; §1.4). The false
>   "R in both" rate therefore lies between `p_L · p_R` and `min(p_L, p_R)`, and with dependence this
>   strong it is nearer the upper end: **about 1 %, not 1e-4.** Neither end is calibrated; nothing in
>   this registration measures where between them it lies.
> - **So the male R is stricter in power and hardly stricter in null.** It is read as "R in each of
>   two strongly dependent readings of one animal", not as a replication.
> - **A split is the likely outcome for a marginal signal, and it is registered as such.** A block
>   near the detection limit can pass in one lobe and not in the other (one lobe R, the other U or
>   G). Such a split is informative: it is classified by §4.3 and printed with both lobe labels. It
>   gets **no male label**. That is a registered choice, made here before data, not a loss to be
>   repaired after it: no rule reads a split as a weak R, and no second criterion is added after
>   unsealing.
>
> ### 4.3 A split: the rule that separates its explanations (proposal, D4; builder D12, §12)
>
> The builder named two explanations of a lobe disagreement, variation within the animal and a
> difference of reconstruction between the lobes, and handed the separating rule to this arm, with
> the R1 row and column as a named obligation (builder §4, §12). **The build's facts change what can
> be separated:**
>
> - **The R1–R6 asymmetry cannot carry a split.** R1–R6 is not a block type, so it enters block A
>   only through training, through R1's row and column. At `c*` those are **the same 3 + 1 cells in
>   both lobes** (§1.4; `BUILD.md` line 185). The builder's registered expectation, a sparser R1 row
>   and column in lobe L, did not appear (§11). **Registered answer to builder §12's question:** no
>   lobe difference is confined to R1's row and column, because there is none there; if one appears
>   (a changed file), check 4 stops the run.
> - **No cross-lobe edge exists among the placed types** (0 of 2,332,880 rows), so the two lobe banks
>   share no neuron pair, and a lobe difference cannot be a mis-assigned side through connectivity.
> - **The block types are even in bodies** (R/L 0.987–1.020, §1.2). A reconstruction difference of
>   the block types in body counts is not seen; one in synapse counts is not measured here.
> - **The outside is not even in `x`:** at the shared cut the right lobe has 30 more present outside
>   cells (526 against 496), 33 R-only against 3 L-only, 33 of the 36 near the cut (§1.4). A lobe-wide
>   difference in `x` near the cut exists, of unknown mechanism (synapse detection, reconstruction of
>   synapses, or biology).
>
> **The classification of a split (registered before data; printed with every split and, as a
> diagnostic, when the lobes agree).** After unsealing, let `y_L`, `y_R` be the two blocks' present
> patterns, `k` the number of the 64 cells whose presence differs, and `k*` = **4**, the smallest `k`
> with a binomial tail `P(X >= k) <= 0.01` for `X ~ Binomial(64, 36 / 2,961)` (the outside
> disagreement rate of §1.4; tails 0.543, 0.183, 0.043, **0.0078** for k = 1..4; arithmetic, this
> draft):
>
> | class | condition | reading |
> |---|---|---|
> | **S0: same block** | `y_L = y_R` | "Block A is the same in both lobes at `c*`; the split comes from the instrument's response to the lobes' other differences (36 of 2,961 outside cells) or from the threshold of detection, not from block A." |
> | **S1: differs like the rest of the lobe** | `1 <= k < k*` | "Block A differs between the lobes in k of 64 cells, within the lobes' outside rate (36 / 2,961, expected about 0.8 of 64): not read as a difference specific to block A. Variation within the animal and a reconstruction difference are not separated." |
> | **S2a: differs more than the rest of the lobe, away from the cut** | `k >= k*`, and **every one** of the k differing block cells has `x` outside [0.5 `c*`, 2 `c*`] in both lobes | "Block A differs between the lobes more than the rest of the lobe does (k of 64; P(X >= k) = … under the outside rate), and no differing cell lies near the cut: a difference specific to block A. Its two explanations, variation within the animal and a difference of reconstruction or typing of the block types, are not separated by this test. The R1–R6 asymmetry is excluded as its carrier (R1 is not a block type, and R1's row and column are the same cells in both lobes at `c*`)." |
> | **S2b: differs more than the rest of the lobe, at the cut** | `k >= k*`, and **at least one** differing block cell does not meet S2a's condition (its `x` lies within [0.5 `c*`, 2 `c*`] in at least one lobe) | "Block A differs between the lobes in k of 64 cells (P(X >= k) = … under the outside rate), and j of them lie near the cut: block cells at the threshold; the same mechanism as 33 of the 36 differing outside cells; specificity to block A not established." |
>
> **S2 is conditional on `x` (revision 1.1, frozen before unsealing; Johnny, strengthened by Ark and
> Zcode).** Revision 1's S2 read every `k >= k*` as "a difference specific to block A". But 33 of the
> 36 outside cells that differ between the lobes lie near the cut in both lobes (§1.4): a lobe-wide
> difference in `x` near `c*` turns cells over one by one, and block cells near the cut would turn
> over by the same mechanism. So "specific to block A" is read only when no differing block cell is
> near the cut (S2a); otherwise S2b says the difference is at the threshold and its specificity is
> not established. The band [0.5 `c*`, 2 `c*`] is the one §1.4 used for the outside cells, fixed
> before unsealing. S2a requires every differing cell to lie outside the band in both lobes; S2b is
> its complement, so the two are exhaustive. **Which branch is expected (Ark):** the relayed
> description of §1.5 (20–21 weak cross cells with means 1.0–2.2 at c = 1, against `c*` = 2.994 and
> 0.5 `c*` = 1.497) puts weak block cells in or near the band, so if the lobes' blocks differ, S2b,
> the threshold branch, is the expected (modal) one. The relayed numbers are not verified (§10), and
> nothing is set from this expectation.
>
> Printed with the class: each differing cell by name with its presence in each lobe, whether each
> lobe's `x` lies within [0.5 `c*`, 2 `c*`] (and the count j of differing cells that fail S2a's
> condition), and the direction count (L-only against R-only) beside the outside's 3 against 33.
> **The binomial reference is descriptive**: block cells are not a random sample of outside cells
> (they are strong medulla-to-lobula-plate pathways, not a random draw of type pairs), and the class
> decides no label. It separates "a block-specific difference" (S2a) from "a lobe-wide one" (S0, S1)
> and from "a difference at the threshold" (S2b). It does not separate variation within the animal
> from reconstruction; nothing in one animal's two lobes can (§6).
>
> **Two objects called "split" (revision 1.3, frozen before unsealing; Ark, Zcode; Ark's class
> 154).** D3's split (§4.2) is **by reading**: the two lobe labels differ. The classes above are
> **by block**: `k` of the 64 cells differ in presence. They are different objects, and each can
> occur without the other:
>
> - **Labels can differ at k = 0.** It is measured now, on the worlds, where both lobes carry the
>   same board by seed (k = 0 in all 45 world pairs): **5 of the 25 dense-grid world pairs split
>   by reading** (seeds 92142 U/R, 92161 U/G, 92164 U/R, 92172 R/U, 92183 W/R; lobe L first),
>   **none of the 20 pairs of the axis families** (R, Nf, No, W) (§3.3.1 (d); verified on both
>   `synthetic_worlds.csv`). With identical blocks, the instrument alone splits one dense-grid pair
>   in five (5 of the 20 at γ 0.5–0.85, 0 of 5 at 1.0).
> - **S2 may never fire even when the labels disagree**, and an S1 or S2 block difference can
>   come with equal labels.
> - **After unsealing, a split by reading is not read as "the lobes' blocks differ"** unless the
>   class of this section says so (S1, S2a or S2b, with its own text); with S0 it reads "the same
>   block, read differently", as S0's text says.
>
> The script prints both, separately and each with its own name, after the male reading (S32):
> "Split by reading (section 4.2, D3): yes/no …. Block difference (section 4.3, by block): class …,
> k = … of 64 cells differ", followed by the worlds' reference counts computed from the registered
> run's own synthetic steps.

