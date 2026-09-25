# Knock out and regrow: block A on flyvis-65

Registration `docs/plans/2026-09-24-knockout-regrow-registration.md`, revision 3.4.1. git_head=74de0401a21f33db22def152fd72fdf0d490ffb4, runtime=8070s.

**Verdict: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.8442 < 0.90)]. rule #2.1: AUC = 0.5327 (32/32), p_S = 0.70 (n_ge = 69 of 99, n_deg = 0), p_P = 0.3288; ceiling_full = 0.8442, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 3, BF_4 3.**

The section 4 row, verbatim:

> | **G: not detected at the R level above γ_R** | not R, not W; the primary **and every BF_r** have `p_P > 0.10`; and the primary's **`ceiling_block` >= 0.90** (the condition is revision 2's, unchanged; the cut is the gate cut, `GATE_CUT`, since revision 3.2) | **Revision 3.1 (Ark 09:32, Johnny 09:33, Zcode 09:34 UTC): "not detected at the R level above γ_R; leg P passes from γ\*_P".** The block carries no structure that this family regrows at the R level at a strength at or above γ_R, where a majority of the synthetic worlds read R. Leg P alone (of rule #2.1) already sees a majority from γ\*_P, and every predictor does from the family limit (§3.6). Revision 3's "not detected above γ\*" named leg P only. The label always prints **all three limits** with their brackets, **the per-γ fractions seen/n and R/n**, the transition band, and the instrument they come from: `BF_LAMBDAS` [1, 3, 10, 30, 100], ties within 1e-9 to the larger λ, `STARTS` = 10. The rule can express the block (`ceiling_block`), and by Johnny's count the information is there (64/64 inferable). **Not** "no grammar found" and **not** "no grammar exists": the instrument has no right to either claim (Ark 08:24, Johnny 08:27 UTC). A G reached through a selected λ = 100 reads "weaker than the detection limit", not "absent" (Zcode 08:22 UTC), and since revision 3.1 it can be read from the verdict line (below). The mechanism, "orthogonal" if the primary's `ceiling_full < 0.90` and "no information" otherwise, is printed beside the label as **a description only** (§2.4, decision (c)). **Revision 3.2 (A5):** the label names its gate variable ("gate: rule #2.1's ceiling_block = … >= 0.90"), and the mechanism description names whose `ceiling_full` it quotes ("rule #2.1's ceiling_full = …"); its cut, `MECHANISM_CUT` = 0.90, is borrowed from the gate and not calibrated (§2.4). A low `ceiling_full` with the gate passed gives G ("orthogonal"), not U. |

within-fly variation, not a cut: one FlyWire column differs from FlyWire-30 by a median of 34 extra and 27 missing pairs out of 900 cells (about 4 of 64 cells if spread evenly; X_c = 0.54 shows it is not) (section 2.4).

## Section 3.5 (flyvis-65, the real block)

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5327 | 0.065 | 0.7403 | +0.0697 | 0.500 | 0.8442 | 1.0000 | 0.10 | 0.07 | 69 / 99 | 0.70 | 0.3288 | 0.0409 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5215 | 0.060 | 0.7193 | +0.0906 | 0.500 | 0.7646 | 1.0000 | 0.08 | 0.04 | 99 / 99 | 1.00 | 0.3837 | 0.1367 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.5029 | 0.134 | 0.9678 | -0.1579 | 0.469 | 0.9111 | 1.0000 | 0.01 | 0.01 | 99 / 99 | 1.00 | 0.4912 | 0.4386 | 1.0 / 3.0 / 1.0 |
| BF_3 | 0.5000 | -0.035 | 0.7541 | +0.0559 | 0.469 | 0.9951 | 1.0000 | 0.00 | 0.00 | 99 / 99 | 1.00 | 0.5119 | 0.5092 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.5010 | -0.042 | 0.7690 | +0.0410 | 0.500 | 1.0000 | 1.0000 | 0.00 | 0.00 | 98 / 99 | 0.99 | 0.5042 | 0.4885 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5352 | 0.000 | 0.8099 | +0.0000 | 0.531 | 0.5215 | 0.5000 | 1.64 | n/a | 99 / 99 | 1.00 | 0.3221 | 0.0161 | None / None / None |

Permuted-block ceiling_full of rule #2.1: 0.789, 0.645, 0.783, 0.798, 0.591, 0.699, 0.811, 0.752, 0.712, 0.713, 0.700, 0.651, 0.625, 0.652, 0.742, 0.745, 0.638, 0.704, 0.685, 0.762 (real block 0.8442).

Per-type AUC, mirrors, quadrant means and the D7 fields are in summary.json.

The limits: gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10. Binomial note: with n = 5 worlds per gamma a limit has an error of about one grid step: a true detection probability of 0.2 or 0.4 gives '>= 3 of 5' with probability 0.06 or 0.32 (Johnny). Private and raw outputs: C:\Users\mikha\Documents\dpc-research\connectome-seed-data\knockout_regrow\flyvis65_20260925T171656Z_74de0401a21f.

Fixed lambda = 1 on the knockout view, diagnostic, decides nothing: rule #2.1 AUC 0.5327, p_P 0.3288; BF_1 AUC 0.5215, p_P 0.3837; BF_2 AUC 0.5029, p_P 0.4912; BF_3 AUC 0.4844, p_P 0.5915; BF_4 AUC 0.4805, p_P 0.6135.

## Pre-data tables (section 1.4)

| endpoint | kept (as in section 1.4) |
|---|---|
| Mi1 | (25, 17) |
| Tm3 | (18, 12) |
| Mi4 | (23, 17) |
| Mi9 | (21, 19) |
| Tm1 | (24, 15) |
| Tm2 | (18, 13) |
| Tm4 | (18, 14) |
| Tm9 | (9, 14) |
| T4a | (8, 9) |
| T4b | (6, 6) |
| T4c | (8, 7) |
| T4d | (6, 6) |
| T5a | (4, 7) |
| T5b | (5, 8) |
| T5c | (4, 7) |
| T5d | (6, 6) |

Inferable block cells: 64 / 64. Mirror cells: [('T4a', 'Mi9'), ('T4b', 'Mi9'), ('T4c', 'Mi9'), ('T5b', 'Tm2'), ('T5c', 'Tm2')]. Training present cells: 572 of 4161.

- FlyWire-30: 14 / 64 (provenance only (Johnny, review of 2026-09-24))
- male CNS v1.0: 64 / 64 at every pair threshold tried (Zcode, preliminary graph) (control arm; recomputed from the built bank and printed before its data (section 8))

## Two-world check (section 3.6, revision 3)

| family | seed | label | G mechanism (description only) | rule AUC | ceiling_full | ceiling_block | n_ge / n_valid | p_S | p_P | n_deg | lambda ko | code |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R | 90100 | R | - | 1.0000 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| R | 90101 | R | - | 1.0000 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| R | 90102 | R | - | 1.0000 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| R | 90103 | R | - | 1.0000 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| R | 90104 | R | - | 1.0000 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| Nf | 90110 | G | orthogonal (rule #2.1's ceiling_full = 0.5088 < 0.90) | 0.5049 | 0.5088 | 1.0000 | 58 / 99 | 0.59 | 0.4779 | 0 | 100.0 | ok |
| Nf | 90111 | G | orthogonal (rule #2.1's ceiling_full = 0.5513 < 0.90) | 0.5361 | 0.5513 | 1.0000 | 85 / 99 | 0.86 | 0.3093 | 0 | 100.0 | ok |
| Nf | 90112 | G | no information (rule #2.1's ceiling_full = 0.9561 >= 0.90) | 0.5068 | 0.9561 | 1.0000 | 31 / 99 | 0.32 | 0.4636 | 0 | 100.0 | ok |
| Nf | 90113 | G | no information (rule #2.1's ceiling_full = 1.0000 >= 0.90) | 0.5020 | 1.0000 | 1.0000 | 44 / 99 | 0.45 | 0.4915 | 0 | 100.0 | ok |
| Nf | 90114 | G | no information (rule #2.1's ceiling_full = 0.9355 >= 0.90) | 0.5166 | 0.9355 | 1.0000 | 68 / 99 | 0.69 | 0.4156 | 0 | 100.0 | ok |
| No | 90120 | G | orthogonal (rule #2.1's ceiling_full = 0.4883 < 0.90) | 0.4990 | 0.4883 | 1.0000 | 83 / 99 | 0.84 | 0.5082 | 0 | 1.0 | ok |
| No | 90121 | G | orthogonal (rule #2.1's ceiling_full = 0.4966 < 0.90) | 0.4961 | 0.4966 | 1.0000 | 53 / 99 | 0.54 | 0.5220 | 0 | 1.0 | ok |
| No | 90122 | G | orthogonal (rule #2.1's ceiling_full = 0.5020 < 0.90) | 0.4980 | 0.5020 | 1.0000 | 24 / 99 | 0.25 | 0.5141 | 0 | 1.0 | ok |
| No | 90123 | G | orthogonal (rule #2.1's ceiling_full = 0.4902 < 0.90) | 0.4756 | 0.4902 | 1.0000 | 3 / 99 | 0.04 | 0.6290 | 0 | 1.0 | ok |
| No | 90124 | G | orthogonal (rule #2.1's ceiling_full = 0.4751 < 0.90) | 0.4805 | 0.4751 | 1.0000 | 95 / 99 | 0.96 | 0.6047 | 0 | 1.0 | ok |
| W | 90130 | W | - | 0.5034 | 0.5176 | 1.0000 | 49 / 99 | 0.50 | 0.4939 | 0 | 1.0 | ok |
| W | 90131 | W | - | 0.5312 | 0.5342 | 1.0000 | 98 / 99 | 0.99 | 0.3426 | 0 | 1.0 | ok |
| W | 90132 | W | - | 0.5225 | 0.5244 | 1.0000 | 2 / 99 | 0.03 | 0.3845 | 0 | 1.0 | ok |
| W | 90133 | W | - | 0.5190 | 0.5273 | 1.0000 | 2 / 99 | 0.03 | 0.4029 | 0 | 1.0 | ok |
| W | 90134 | W | - | 0.5029 | 0.5156 | 1.0000 | 48 / 99 | 0.49 | 0.4853 | 0 | 1.0 | ok |
| M0.5 | 90140 | R | - | 0.7354 | 0.9883 | 1.0000 | 0 / 99 | 0.01 | 0.0004 | 0 | 3.0 | curve |
| M0.5 | 90141 | G | no information (rule #2.1's ceiling_full = 1.0000 >= 0.90) | 0.5005 | 1.0000 | 1.0000 | 49 / 99 | 0.50 | 0.4998 | 0 | 100.0 | curve |
| M0.5 | 90142 | G | no information (rule #2.1's ceiling_full = 0.9893 >= 0.90) | 0.5308 | 0.9893 | 1.0000 | 0 / 99 | 0.01 | 0.3425 | 0 | 3.0 | curve |
| M0.5 | 90143 | G | orthogonal (rule #2.1's ceiling_full = 0.5327 < 0.90) | 0.5283 | 0.5327 | 1.0000 | 44 / 99 | 0.45 | 0.3590 | 0 | 100.0 | curve |
| M0.5 | 90144 | G | no information (rule #2.1's ceiling_full = 0.9990 >= 0.90) | 0.4902 | 0.9990 | 1.0000 | 43 / 99 | 0.44 | 0.5525 | 0 | 100.0 | curve |
| M0.6 | 90160 | R | - | 0.7451 | 0.9971 | 1.0000 | 0 / 99 | 0.01 | 0.0002 | 0 | 3.0 | curve |
| M0.6 | 90161 | U | - | 0.5654 | 0.9717 | 1.0000 | 0 / 99 | 0.01 | 0.1888 | 0 | 3.0 | curve |
| M0.6 | 90162 | R | - | 0.7300 | 0.9980 | 1.0000 | 0 / 99 | 0.01 | 0.0008 | 0 | 3.0 | curve |
| M0.6 | 90163 | U | - | 0.6729 | 1.0000 | 1.0000 | 1 / 99 | 0.02 | 0.0082 | 0 | 3.0 | curve |
| M0.6 | 90164 | U | - | 0.6357 | 0.9824 | 1.0000 | 0 / 99 | 0.01 | 0.0308 | 0 | 3.0 | curve |
| M0.75 | 90170 | R | - | 0.8711 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 3.0 | curve |
| M0.75 | 90171 | R | - | 0.8760 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 3.0 | curve |
| M0.75 | 90172 | R | - | 0.7861 | 0.9971 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 3.0 | curve |
| M0.75 | 90173 | R | - | 0.7246 | 0.9941 | 1.0000 | 0 / 99 | 0.01 | 0.0010 | 0 | 3.0 | curve |
| M0.75 | 90174 | R | - | 0.7402 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0003 | 0 | 3.0 | curve |
| M0.85 | 90180 | R | - | 0.9517 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |
| M0.85 | 90181 | R | - | 0.7764 | 0.9873 | 1.0000 | 0 / 99 | 0.01 | 0.0002 | 0 | 3.0 | curve |
| M0.85 | 90182 | R | - | 0.8428 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 3.0 | curve |
| M0.85 | 90183 | R | - | 0.8398 | 0.9990 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 3.0 | curve |
| M0.85 | 90184 | R | - | 0.8115 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 3.0 | curve |
| M1.0 | 90150 | R | - | 0.9697 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |
| M1.0 | 90151 | R | - | 0.9541 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |
| M1.0 | 90152 | R | - | 0.8555 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 3.0 | curve |
| M1.0 | 90153 | R | - | 0.9736 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |
| M1.0 | 90154 | R | - | 0.7588 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 3.0 | curve |

| family | requirement | labels read (R/W/G/U) | meet (min) | stop labels | result |
|---|---|---|---|---|---|
| R | each of 5 worlds reads R, on both D1 candidates | 5/0/0/0 | 5/5 (5) | 0 | no stop |
| Nf | never R or W (stop); at least 3 of 5 read G | 0/0/5/0 | 5/5 (3) | 0 | no stop |
| No | never R or W (stop); reads G; a U triggers the No contingency | 0/0/5/0 | 5/5 (0) | 0 | no stop |
| W | each of 5 worlds reads W, on both D1 candidates | 0/5/0/0 | 5/5 (5) | 0 | no stop |
| M0.5 | power curve: printed, no stop row; the three limits are taken from it | 1/0/4/0 | n/a (power curve) | 0 | no stop |
| M0.6 | power curve: printed, no stop row; the three limits are taken from it | 2/0/0/3 | n/a (power curve) | 0 | no stop |
| M0.75 | power curve: printed, no stop row; the three limits are taken from it | 5/0/0/0 | n/a (power curve) | 0 | no stop |
| M0.85 | power curve: printed, no stop row; the three limits are taken from it | 5/0/0/0 | n/a (power curve) | 0 | no stop |
| M1.0 | power curve: printed, no stop row; the three limits are taken from it | 5/0/0/0 | n/a (power curve) | 0 | no stop |

Pre-run table (section 7, revisions 3.2, 3.3): outcome 1: every deciding column equal; not byte-identical (recorded, not gated); rows matched by family/j/seed/predictor: 0 missing now, 0 missing in the pre-run table, row order equal (a fact, not an outcome); mechanism_description differs on 84 rows (reported, not gated), of which 84 are exactly revision 3.2's rename and 0 are not (passed: True; byte-identical: False; pinned 7a2f02953207f8aacb1cbd8c5e61e7731135d5a6f800a40b359cb0ff12f9c8f1, recomputed 32d62c717d20eb2fafeb465c2ee8fcf8e3880d7a327646bdccc8753714f895c1).

Per-fit diagnostic against the pre-run raw fits (diagnostic, decides nothing): revision_2_worlds: {'pinned': 19110, 'missing_now': 0, 'compared': 19110, 'fitted_this_pass': 19110, 'p_differ': 0, 'lambda_differ': 0, 'labels_differ': 0, 'score_differ': 0, 'outside_density_differ': 0, 'reused_from_ko_differ': 0, 'max_abs_dp': 0.0}, revision_3_worlds: {'pinned': 9555, 'missing_now': 0, 'compared': 9555, 'fitted_this_pass': 9555, 'p_differ': 0, 'lambda_differ': 0, 'labels_differ': 0, 'score_differ': 0, 'outside_density_differ': 0, 'reused_from_ko_differ': 0, 'max_abs_dp': 0.0}.

Two-world check passed: True. No contingency triggered: False.

## Power curve and the three limits (section 3.6, revision 3.1)

| gamma | family | seen/n (rule #2.1 p_P <= 0.01) | R/n | seen/n BF_1, BF_2, BF_3, BF_4 | R/W/G/U | rule AUC | rule lambda ko |
|---|---|---|---|---|---|---|---|
| 0.0 | Nf (anchor) | 0/5 | 0/5 | 0/5, 0/5, 0/5, 0/5 | 0/0/5/0 | 0.505, 0.536, 0.507, 0.502, 0.517 | 100, 100, 100, 100, 100 |
| 0.5 | M0.5 | 1/5 | 1/5 | 1/5, 0/5, 0/5, 0/5 | 1/0/4/0 | 0.735, 0.500, 0.531, 0.528, 0.490 | 3, 100, 3, 100, 100 |
| 0.6 | M0.6 | 3/5 | 2/5 | 3/5, 1/5, 1/5, 0/5 | 2/0/0/3 | 0.745, 0.565, 0.730, 0.673, 0.636 | 3, 3, 3, 3, 3 |
| 0.75 | M0.75 | 5/5 | 5/5 | 5/5, 5/5, 5/5, 5/5 | 5/0/0/0 | 0.871, 0.876, 0.786, 0.725, 0.740 | 3, 3, 3, 3, 3 |
| 0.85 | M0.85 | 5/5 | 5/5 | 5/5, 5/5, 5/5, 5/5 | 5/0/0/0 | 0.952, 0.776, 0.843, 0.840, 0.812 | 1, 3, 3, 3, 3 |
| 1.0 | M1.0 | 5/5 | 5/5 | 5/5, 5/5, 5/5, 5/5 | 5/0/0/0 | 0.970, 0.954, 0.855, 0.974, 0.759 | 1, 1, 3, 1, 3 |
| 2.0 | R (anchor) | 5/5 | 5/5 | 5/5, 5/5, 5/5, 5/5 | 5/0/0/0 | 1.000, 1.000, 1.000, 1.000, 1.000 | 1, 1, 1, 1, 1 |

**The three limits** (in M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10):

- gamma*_P, the leg-P limit (rule #2.1 p_P <= 0.01 in a majority of the worlds): **0.6**, bracket (0.5, 0.6]; majority seen at every grid gamma above it: True.
- gamma_R (a majority of the worlds read R): **0.75**, bracket (0.6, 0.75]; majority R at every grid gamma above it: True.
- family limit (the largest leg-P limit: the maximum of each predictor's own leg-P limit): **0.75 (set by BF_2, BF_3, BF_4)**. Per predictor: rule #2.1 0.6, BF_1 0.6, BF_2 0.75, BF_3 0.75, BF_4 0.75. The limits use p_P <= 0.01 for every predictor and are not family-corrected, unlike the W gate (p_P <= 0.0125 = 0.05/4): a limit is a property of the instrument, not of a branch (revision 3.2).
- transition band [gamma*_P, gamma_R): [0.6, 0.75): 1 grid step(s), 0.15 in gamma. Dense-grid worlds that read U: 3 inside the band, 0 below it, 0 above it. The band is the difference of two limits, each uncertain by about one grid step, so a one-step band is one of 0, 1 or 2 steps (revision 3.2).
- per gamma, seen/n and R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5.
- binomial note: with n = 5 worlds per gamma a limit has an error of about one grid step: a true detection probability of 0.2 or 0.4 gives '>= 3 of 5' with probability 0.06 or 0.32 (Johnny).
- M worlds that read G at or above gamma*_P: 0; at or above gamma_R: 0 (printed, no stop).
- grid complete: True.

**U rule:** threshold U read by 3 of 25 dense-grid worlds (3 threshold U, 0 failed fit, 0 ceiling_block not measured): U stays; its frequency is printed. U is read as 'on the detection threshold; cannot be separated', the signature of the leg-P detection limit gamma*_P (revisions 3.1, 3.2), except a U whose reasons include rule #2.1's ceiling_block below 0.90, which reads 'failed fit: rule #2.1 cannot hold the block even when trained on it alone', and a U whose ceiling_block was not measured, which reads 'not measured: rule #2.1's ceiling_block was not measured; the G gate cannot be read' (revision 3.3). U across all 45 worlds: 3 (R 0/5, Nf 0/5, No 0/5, W 0/5, M0.5 0/5, M1.0 0/5, M0.6 3/5, M0.75 0/5, M0.85 0/5).

## Fixed lambda = 1 on the knockout view (section 3.5): diagnostic, decides nothing

Printed beside the limits, not on any verdict line. Where the selected lambda was 1 the selected fit is reused (path check: {'bank': 'world:W:0', 'identical': {'rule': True, 'BF:1': True, 'BF:2': True, 'BF:3': True, 'BF:4': True}, 'passed': True}).

| family | predictor | AUC at lambda 1 (per world) | mean | p_P <= 0.01 at lambda 1 | selected lambda | mean AUC selected | p_P <= 0.01 selected |
|---|---|---|---|---|---|---|---|
| R | rule #2.1 | 1.000, 1.000, 1.000, 1.000, 1.000 | 1.000 | 5/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 1.000 | 5/5 |
| R | BF_1 | 1.000, 1.000, 1.000, 1.000, 1.000 | 1.000 | 5/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 1.000 | 5/5 |
| R | BF_2 | 1.000, 1.000, 0.994, 1.000, 0.986 | 0.996 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.998 | 5/5 |
| R | BF_3 | 1.000, 1.000, 0.975, 0.999, 0.985 | 0.992 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.998 | 5/5 |
| R | BF_4 | 0.932, 0.986, 0.966, 0.994, 0.978 | 0.971 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.996 | 5/5 |
| Nf | rule #2.1 | 0.508, 0.515, 0.593, 0.623, 0.510 | 0.550 | 0/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.513 | 0/5 |
| Nf | BF_1 | 0.503, 0.511, 0.600, 0.635, 0.502 | 0.550 | 0/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.517 | 0/5 |
| Nf | BF_2 | 0.484, 0.492, 0.589, 0.646, 0.492 | 0.541 | 0/5 | 100.0, 100.0, 3.0, 100.0, 100.0 | 0.528 | 0/5 |
| Nf | BF_3 | 0.494, 0.483, 0.586, 0.567, 0.517 | 0.529 | 0/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.517 | 0/5 |
| Nf | BF_4 | 0.474, 0.475, 0.564, 0.433, 0.537 | 0.496 | 0/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.517 | 0/5 |
| No | rule #2.1 | 0.499, 0.496, 0.498, 0.476, 0.480 | 0.490 | 0/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.490 | 0/5 |
| No | BF_1 | 0.499, 0.500, 0.506, 0.478, 0.487 | 0.494 | 0/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.494 | 0/5 |
| No | BF_2 | 0.481, 0.505, 0.481, 0.503, 0.492 | 0.493 | 0/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.487 | 0/5 |
| No | BF_3 | 0.484, 0.502, 0.451, 0.473, 0.489 | 0.480 | 0/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.485 | 0/5 |
| No | BF_4 | 0.481, 0.521, 0.482, 0.481, 0.499 | 0.493 | 0/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.494 | 0/5 |
| W | rule #2.1 | 0.503, 0.531, 0.522, 0.519, 0.503 | 0.516 | 0/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.516 | 0/5 |
| W | BF_1 | 0.516, 0.535, 0.521, 0.519, 0.515 | 0.521 | 0/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.521 | 0/5 |
| W | BF_2 | 0.745, 0.729, 0.733, 0.755, 0.753 | 0.743 | 5/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.743 | 5/5 |
| W | BF_3 | 0.685, 0.695, 0.704, 0.751, 0.758 | 0.719 | 5/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.719 | 5/5 |
| W | BF_4 | 0.689, 0.678, 0.682, 0.750, 0.765 | 0.713 | 5/5 | 1.0, 1.0, 1.0, 1.0, 3.0 | 0.705 | 5/5 |
| M0.5 | rule #2.1 | 0.786, 0.586, 0.550, 0.507, 0.480 | 0.582 | 1/5 | 3.0, 100.0, 3.0, 100.0, 100.0 | 0.557 | 1/5 |
| M0.5 | BF_1 | 0.810, 0.611, 0.542, 0.485, 0.448 | 0.579 | 1/5 | 3.0, 100.0, 3.0, 100.0, 100.0 | 0.556 | 1/5 |
| M0.5 | BF_2 | 0.810, 0.592, 0.516, 0.464, 0.504 | 0.577 | 1/5 | 100.0, 100.0, 100.0, 100.0, 3.0 | 0.503 | 0/5 |
| M0.5 | BF_3 | 0.739, 0.585, 0.507, 0.442, 0.574 | 0.570 | 1/5 | 100.0, 3.0, 100.0, 100.0, 3.0 | 0.528 | 0/5 |
| M0.5 | BF_4 | 0.732, 0.581, 0.610, 0.465, 0.598 | 0.597 | 1/5 | 100.0, 3.0, 100.0, 3.0, 100.0 | 0.507 | 0/5 |
| M1.0 | rule #2.1 | 0.970, 0.954, 0.944, 0.974, 0.864 | 0.941 | 5/5 | 1.0, 1.0, 3.0, 1.0, 3.0 | 0.902 | 5/5 |
| M1.0 | BF_1 | 0.969, 0.973, 0.939, 0.970, 0.853 | 0.941 | 5/5 | 1.0, 1.0, 3.0, 1.0, 3.0 | 0.905 | 5/5 |
| M1.0 | BF_2 | 0.907, 0.970, 0.882, 0.952, 0.858 | 0.914 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.865 | 5/5 |
| M1.0 | BF_3 | 0.831, 0.896, 0.856, 0.911, 0.727 | 0.844 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.839 | 5/5 |
| M1.0 | BF_4 | 0.803, 0.822, 0.847, 0.865, 0.692 | 0.806 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.829 | 5/5 |
| M0.6 | rule #2.1 | 0.821, 0.595, 0.847, 0.780, 0.722 | 0.753 | 4/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.670 | 3/5 |
| M0.6 | BF_1 | 0.819, 0.626, 0.861, 0.802, 0.691 | 0.760 | 4/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.677 | 3/5 |
| M0.6 | BF_2 | 0.772, 0.616, 0.663, 0.604, 0.621 | 0.655 | 1/5 | 3.0, 3.0, 3.0, 100.0, 100.0 | 0.591 | 1/5 |
| M0.6 | BF_3 | 0.736, 0.559, 0.640, 0.625, 0.616 | 0.635 | 1/5 | 3.0, 100.0, 3.0, 100.0, 100.0 | 0.574 | 1/5 |
| M0.6 | BF_4 | 0.712, 0.580, 0.623, 0.629, 0.610 | 0.631 | 1/5 | 100.0, 100.0, 3.0, 100.0, 100.0 | 0.536 | 0/5 |
| M0.75 | rule #2.1 | 0.951, 0.969, 0.901, 0.819, 0.874 | 0.903 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.800 | 5/5 |
| M0.75 | BF_1 | 0.960, 0.971, 0.898, 0.837, 0.883 | 0.910 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.799 | 5/5 |
| M0.75 | BF_2 | 0.917, 0.955, 0.731, 0.880, 0.881 | 0.873 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.787 | 5/5 |
| M0.75 | BF_3 | 0.859, 0.950, 0.750, 0.894, 0.804 | 0.851 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.773 | 5/5 |
| M0.75 | BF_4 | 0.755, 0.892, 0.718, 0.895, 0.791 | 0.810 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.762 | 5/5 |
| M0.85 | rule #2.1 | 0.952, 0.848, 0.915, 0.928, 0.908 | 0.910 | 5/5 | 1.0, 3.0, 3.0, 3.0, 3.0 | 0.844 | 5/5 |
| M0.85 | BF_1 | 0.951, 0.858, 0.922, 0.914, 0.908 | 0.911 | 5/5 | 1.0, 3.0, 3.0, 3.0, 3.0 | 0.844 | 5/5 |
| M0.85 | BF_2 | 0.900, 0.759, 0.889, 0.862, 0.888 | 0.860 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.811 | 5/5 |
| M0.85 | BF_3 | 0.849, 0.750, 0.811, 0.870, 0.793 | 0.814 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.791 | 5/5 |
| M0.85 | BF_4 | 0.776, 0.709, 0.745, 0.822, 0.805 | 0.771 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.777 | 5/5 |

Fits: 0 re-read from saved fits, 28440 new world fits, fixed lambda: 47 reused, 173 fitted.

### World R, seed 90100: R: regrows

Outside density 0.2401; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 1.0000 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 1.0000 | 3.356 | 0.2739 | +0.4835 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 1.0000 | 2.919 | 0.2688 | +0.4886 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 1.0000 | 2.288 | 0.3375 | +0.4199 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 1.0000 | 2.300 | 0.3371 | +0.4203 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 1.0000 | 2.440 | 0.3210 | +0.4364 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5459 | 0.000 | 0.7574 | +0.0000 | 0.625 | 0.5488 | 0.5000 | 0.94 | n/a | 99 / 99 | 1.00 | 0.2645 | 0.0007 | None / None / None |

### World R, seed 90101: R: regrows

Outside density 0.2367; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 1.0000 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 1.0000 | 3.665 | 0.2436 | +0.5151 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 1.0000 | 3.247 | 0.2282 | +0.5304 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 1.0000 | 2.527 | 0.3007 | +0.4579 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 1.0000 | 2.489 | 0.3048 | +0.4538 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 1.0000 | 2.411 | 0.3136 | +0.4451 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5107 | 0.000 | 0.7587 | +0.0000 | 0.500 | 0.5088 | 0.5000 | 1.22 | n/a | 99 / 99 | 1.00 | 0.4484 | 0.1248 | None / None / None |

### World R, seed 90102: R: regrows

Outside density 0.2447; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 1.0000 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 1.0000 | 3.308 | 0.2913 | +0.4811 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 1.0000 | 2.973 | 0.2800 | +0.4924 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.9912 | 2.224 | 0.3616 | +0.4109 | 0.938 | 1.0000 | 1.0000 | 0.98 | 0.98 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.9893 | 2.236 | 0.3590 | +0.4135 | 0.906 | 1.0000 | 1.0000 | 0.98 | 0.98 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.9824 | 2.157 | 0.3740 | +0.3984 | 0.906 | 1.0000 | 1.0000 | 0.96 | 0.96 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5352 | 0.000 | 0.7724 | +0.0000 | 0.531 | 0.5391 | 0.5000 | 0.90 | n/a | 99 / 99 | 1.00 | 0.3170 | 0.0432 | None / None / None |

### World R, seed 90103: R: regrows

Outside density 0.2420; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 1.0000 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 1.0000 | 3.994 | 0.1976 | +0.5299 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 1.0000 | 3.525 | 0.1934 | +0.5341 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 1.0000 | 2.488 | 0.2912 | +0.4363 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 1.0000 | 2.447 | 0.2968 | +0.4307 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.9990 | 2.492 | 0.2925 | +0.4350 | 0.969 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4980 | 0.000 | 0.7275 | +0.0000 | 0.500 | 0.5020 | 0.5000 | -1.00 | n/a | 99 / 99 | 1.00 | 0.5186 | 0.5704 | None / None / None |

### World R, seed 90104: R: regrows

Outside density 0.2531; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 1.0000 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 1.0000 | 3.204 | 0.2460 | +0.4763 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 1.0000 | 2.831 | 0.2438 | +0.4785 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 1.0000 | 2.381 | 0.2970 | +0.4253 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 1.0000 | 2.395 | 0.2984 | +0.4239 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 1.0000 | 2.412 | 0.3012 | +0.4211 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5078 | -0.000 | 0.7223 | +0.0000 | 0.531 | 0.5098 | 0.5000 | 0.80 | n/a | 99 / 99 | 1.00 | 0.4518 | 0.3303 | None / None / None |

### World Nf, seed 90110: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1425; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5088 < 0.90)]. rule #2.1: AUC = 0.5049 (32/32), p_S = 0.59 (n_ge = 58 of 99, n_deg = 0), p_P = 0.4779; ceiling_full = 0.5088, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5049 | 0.000 | 0.8132 | +0.0010 | 0.531 | 0.5088 | 1.0000 | 0.56 | 0.01 | 58 / 99 | 0.59 | 0.4779 | 0.3719 | 100.0 / 100.0 / 1.0 |
| BF_1 | 0.5078 | 0.000 | 0.8142 | +0.0000 | 0.500 | 0.5068 | 1.0000 | 1.14 | 0.02 | 97 / 99 | 0.98 | 0.4626 | 0.3004 | 100.0 / 100.0 / 1.0 |
| BF_2 | 0.5078 | 0.000 | 0.8142 | +0.0000 | 0.500 | 0.5068 | 1.0000 | 1.14 | 0.02 | 98 / 99 | 0.99 | 0.4626 | 0.3004 | 100.0 / 100.0 / 1.0 |
| BF_3 | 0.5078 | 0.000 | 0.8142 | +0.0000 | 0.500 | 0.5068 | 1.0000 | 1.14 | 0.02 | 99 / 99 | 1.00 | 0.4626 | 0.3004 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.5078 | 0.000 | 0.8142 | +0.0000 | 0.500 | 0.5068 | 1.0000 | 1.14 | 0.02 | 99 / 99 | 1.00 | 0.4626 | 0.3004 | 100.0 / 100.0 / 1.0 |
| N1 | 0.5078 | 0.000 | 0.8142 | +0.0000 | 0.500 | 0.5068 | 0.5000 | 1.14 | n/a | 99 / 99 | 1.00 | 0.4626 | 0.3004 | None / None / None |

### World Nf, seed 90111: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1341; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5513 < 0.90)]. rule #2.1: AUC = 0.5361 (32/32), p_S = 0.86 (n_ge = 85 of 99, n_deg = 0), p_P = 0.3093; ceiling_full = 0.5513, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5361 | 0.000 | 0.7973 | +0.0049 | 0.562 | 0.5513 | 1.0000 | 0.70 | 0.07 | 85 / 99 | 0.86 | 0.3093 | 0.0207 | 100.0 / 100.0 / 1.0 |
| BF_1 | 0.5488 | 0.000 | 0.8022 | +0.0000 | 0.562 | 0.5566 | 1.0000 | 0.86 | 0.10 | 95 / 99 | 0.96 | 0.2504 | 0.0025 | 100.0 / 100.0 / 1.0 |
| BF_2 | 0.5488 | 0.000 | 0.8022 | +0.0000 | 0.562 | 0.5566 | 1.0000 | 0.86 | 0.10 | 98 / 99 | 0.99 | 0.2504 | 0.0025 | 100.0 / 100.0 / 1.0 |
| BF_3 | 0.5488 | 0.000 | 0.8022 | +0.0000 | 0.562 | 0.5566 | 1.0000 | 0.86 | 0.10 | 99 / 99 | 1.00 | 0.2504 | 0.0025 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.5488 | 0.000 | 0.8022 | +0.0000 | 0.562 | 0.5566 | 1.0000 | 0.86 | 0.10 | 99 / 99 | 1.00 | 0.2504 | 0.0025 | 100.0 / 100.0 / 1.0 |
| N1 | 0.5488 | 0.000 | 0.8022 | +0.0000 | 0.562 | 0.5566 | 0.5000 | 0.86 | n/a | 99 / 99 | 1.00 | 0.2504 | 0.0025 | None / None / None |

### World Nf, seed 90112: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1242; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 0.9561 >= 0.90)]. rule #2.1: AUC = 0.5068 (32/32), p_S = 0.32 (n_ge = 31 of 99, n_deg = 0), p_P = 0.4636; ceiling_full = 0.9561, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 3, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5068 | 0.000 | 0.9766 | +0.0035 | 0.562 | 0.9561 | 1.0000 | 0.01 | 0.01 | 31 / 99 | 0.32 | 0.4636 | 0.3011 | 100.0 / 3.0 / 1.0 |
| BF_1 | 0.5039 | 0.000 | 0.9800 | +0.0000 | 0.531 | 0.9551 | 1.0000 | 0.01 | 0.01 | 98 / 99 | 0.99 | 0.4816 | 0.3787 | 100.0 / 3.0 / 1.0 |
| BF_2 | 0.5557 | 0.154 | 0.9331 | +0.0470 | 0.562 | 0.9385 | 1.0000 | 0.13 | 0.11 | 0 / 99 | 0.01 | 0.2252 | 0.0576 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5039 | 0.000 | 0.9800 | +0.0000 | 0.531 | 0.9580 | 1.0000 | 0.01 | 0.01 | 99 / 99 | 1.00 | 0.4816 | 0.3787 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.5039 | 0.000 | 0.9800 | +0.0000 | 0.531 | 0.9736 | 1.0000 | 0.01 | 0.01 | 99 / 99 | 1.00 | 0.4816 | 0.3787 | 100.0 / 3.0 / 1.0 |
| N1 | 0.5039 | 0.000 | 0.9800 | +0.0000 | 0.531 | 0.4922 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.4816 | 0.3787 | None / None / None |

### World Nf, seed 90113: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1391; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 1.0000 >= 0.90)]. rule #2.1: AUC = 0.5020 (32/32), p_S = 0.45 (n_ge = 44 of 99, n_deg = 0), p_P = 0.4915; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5020 | 0.000 | 0.8994 | +0.0019 | 0.562 | 1.0000 | 1.0000 | 0.00 | 0.00 | 44 / 99 | 0.45 | 0.4915 | 0.4418 | 100.0 / 3.0 / 1.0 |
| BF_1 | 0.5029 | 0.000 | 0.9013 | +0.0000 | 0.562 | 1.0000 | 1.0000 | 0.01 | 0.01 | 97 / 99 | 0.98 | 0.4863 | 0.4121 | 100.0 / 3.0 / 1.0 |
| BF_2 | 0.5029 | 0.000 | 0.9013 | +0.0000 | 0.562 | 1.0000 | 1.0000 | 0.01 | 0.01 | 99 / 99 | 1.00 | 0.4863 | 0.4121 | 100.0 / 3.0 / 1.0 |
| BF_3 | 0.5029 | 0.000 | 0.9013 | +0.0000 | 0.562 | 1.0000 | 1.0000 | 0.01 | 0.01 | 99 / 99 | 1.00 | 0.4863 | 0.4121 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.5029 | 0.000 | 0.9013 | +0.0000 | 0.562 | 1.0000 | 1.0000 | 0.01 | 0.01 | 99 / 99 | 1.00 | 0.4863 | 0.4121 | 100.0 / 3.0 / 1.0 |
| N1 | 0.5029 | 0.000 | 0.9013 | +0.0000 | 0.562 | 0.4980 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.4863 | 0.4121 | None / None / None |

### World Nf, seed 90114: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1423; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 0.9355 >= 0.90)]. rule #2.1: AUC = 0.5166 (32/32), p_S = 0.69 (n_ge = 68 of 99, n_deg = 0), p_P = 0.4156; ceiling_full = 0.9355, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5166 | 0.000 | 0.9058 | +0.0110 | 0.531 | 0.9355 | 1.0000 | 0.04 | 0.03 | 68 / 99 | 0.69 | 0.4156 | 0.1724 | 100.0 / 3.0 / 1.0 |
| BF_1 | 0.5225 | 0.000 | 0.9168 | +0.0000 | 0.531 | 0.9346 | 1.0000 | 0.05 | 0.04 | 97 / 99 | 0.98 | 0.3860 | 0.1084 | 100.0 / 3.0 / 1.0 |
| BF_2 | 0.5225 | 0.000 | 0.9168 | +0.0000 | 0.531 | 0.5176 | 1.0000 | 1.28 | 0.04 | 98 / 99 | 0.99 | 0.3860 | 0.1084 | 100.0 / 100.0 / 1.0 |
| BF_3 | 0.5225 | 0.000 | 0.9168 | +0.0000 | 0.531 | 0.5176 | 1.0000 | 1.28 | 0.04 | 97 / 99 | 0.98 | 0.3860 | 0.1084 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.5225 | 0.000 | 0.9168 | +0.0000 | 0.531 | 0.5176 | 1.0000 | 1.28 | 0.04 | 98 / 99 | 0.99 | 0.3860 | 0.1084 | 100.0 / 100.0 / 1.0 |
| N1 | 0.5225 | 0.000 | 0.9168 | +0.0000 | 0.531 | 0.5176 | 0.5000 | 1.28 | n/a | 99 / 99 | 1.00 | 0.3860 | 0.1084 | None / None / None |

### World No, seed 90120: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.2372; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.4883 < 0.90)]. rule #2.1: AUC = 0.4990 (32/32), p_S = 0.84 (n_ge = 83 of 99, n_deg = 0), p_P = 0.5082; ceiling_full = 0.4883, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4990 | 0.020 | 1.1422 | -0.4224 | 0.500 | 0.4883 | 1.0000 | n/a | -0.00 | 83 / 99 | 0.84 | 0.5082 | 0.5028 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.4990 | 0.014 | 1.0441 | -0.3243 | 0.500 | 0.5010 | 1.0000 | -1.00 | -0.00 | 99 / 99 | 1.00 | 0.5100 | 0.5041 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.4834 | 0.003 | 0.9244 | -0.2047 | 0.500 | 0.9541 | 1.0000 | -0.04 | -0.03 | 99 / 99 | 1.00 | 0.5895 | 0.5867 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.4795 | -0.018 | 0.9300 | -0.2102 | 0.500 | 0.9561 | 1.0000 | -0.04 | -0.04 | 99 / 99 | 1.00 | 0.6107 | 0.6049 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.5127 | 0.007 | 0.9280 | -0.2082 | 0.500 | 0.9580 | 1.0000 | 0.03 | 0.03 | 0 / 99 | 0.01 | 0.4351 | 0.4354 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5068 | 0.000 | 0.7198 | +0.0000 | 0.500 | 0.5068 | 0.5000 | 1.00 | n/a | 99 / 99 | 1.00 | 0.4661 | 0.3621 | None / None / None |

### World No, seed 90121: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.2427; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.4966 < 0.90)]. rule #2.1: AUC = 0.4961 (32/32), p_S = 0.54 (n_ge = 53 of 99, n_deg = 0), p_P = 0.5220; ceiling_full = 0.4966, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4961 | -0.000 | 1.1067 | -0.3620 | 0.500 | 0.4966 | 1.0000 | n/a | -0.01 | 53 / 99 | 0.54 | 0.5220 | 0.5278 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5000 | -0.001 | 1.0018 | -0.2570 | 0.500 | 0.4961 | 1.0000 | n/a | 0.00 | 2 / 99 | 0.03 | 0.5028 | 0.5059 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.5010 | -0.000 | 0.9092 | -0.1645 | 0.500 | 0.8838 | 1.0000 | 0.00 | 0.00 | 0 / 99 | 0.01 | 0.4959 | 0.5011 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5010 | 0.003 | 0.9031 | -0.1584 | 0.500 | 0.9004 | 1.0000 | 0.00 | 0.00 | 0 / 99 | 0.01 | 0.4968 | 0.5062 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.5127 | 0.024 | 0.8887 | -0.1440 | 0.531 | 0.9258 | 1.0000 | 0.03 | 0.03 | 0 / 99 | 0.01 | 0.4315 | 0.4391 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4961 | 0.000 | 0.7447 | +0.0000 | 0.500 | 0.4912 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5134 | 0.6260 | None / None / None |

### World No, seed 90122: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.2499; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5020 < 0.90)]. rule #2.1: AUC = 0.4980 (32/32), p_S = 0.25 (n_ge = 24 of 99, n_deg = 0), p_P = 0.5141; ceiling_full = 0.5020, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4980 | -0.136 | 1.2449 | -0.5135 | 0.500 | 0.5020 | 1.0000 | -1.00 | -0.00 | 24 / 99 | 0.25 | 0.5141 | 0.5191 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5059 | -0.143 | 1.1439 | -0.4126 | 0.500 | 0.5098 | 1.0000 | 0.60 | 0.01 | 0 / 99 | 0.01 | 0.4717 | 0.4799 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.4756 | -0.103 | 0.9791 | -0.2478 | 0.500 | 0.8379 | 1.0000 | -0.07 | -0.05 | 99 / 99 | 1.00 | 0.6371 | 0.6238 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.4688 | -0.147 | 0.9786 | -0.2473 | 0.531 | 0.9023 | 1.0000 | -0.08 | -0.06 | 99 / 99 | 1.00 | 0.6736 | 0.6548 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.4697 | -0.105 | 0.9681 | -0.2367 | 0.531 | 0.9336 | 1.0000 | -0.07 | -0.06 | 99 / 99 | 1.00 | 0.6669 | 0.6504 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4863 | 0.000 | 0.7314 | +0.0000 | 0.500 | 0.4893 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5752 | 0.7862 | None / None / None |

### World No, seed 90123: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.2406; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.4902 < 0.90)]. rule #2.1: AUC = 0.4756 (32/32), p_S = 0.04 (n_ge = 3 of 99, n_deg = 0), p_P = 0.6290; ceiling_full = 0.4902, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4756 | 0.005 | 1.0539 | -0.2959 | 0.500 | 0.4902 | 1.0000 | n/a | -0.05 | 3 / 99 | 0.04 | 0.6290 | 0.6386 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.4775 | 0.002 | 0.9543 | -0.1964 | 0.500 | 0.4854 | 1.0000 | n/a | -0.04 | 1 / 99 | 0.02 | 0.6198 | 0.6325 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.4961 | 0.000 | 0.8904 | -0.1325 | 0.500 | 0.9023 | 1.0000 | -0.01 | -0.01 | 0 / 99 | 0.01 | 0.5226 | 0.5258 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.4775 | -0.074 | 0.9118 | -0.1539 | 0.500 | 0.9229 | 1.0000 | -0.05 | -0.04 | 0 / 99 | 0.01 | 0.6196 | 0.6236 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.4717 | -0.092 | 0.9168 | -0.1588 | 0.500 | 0.9307 | 1.0000 | -0.07 | -0.06 | 0 / 99 | 0.01 | 0.6538 | 0.6527 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4561 | 0.000 | 0.7579 | +0.0000 | 0.438 | 0.4570 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.7240 | 0.9997 | None / None / None |

### World No, seed 90124: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.2372; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.4751 < 0.90)]. rule #2.1: AUC = 0.4805 (32/32), p_S = 0.96 (n_ge = 95 of 99, n_deg = 0), p_P = 0.6047; ceiling_full = 0.4751, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4805 | -0.003 | 1.0779 | -0.3460 | 0.500 | 0.4751 | 1.0000 | n/a | -0.04 | 95 / 99 | 0.96 | 0.6047 | 0.6065 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.4873 | -0.011 | 0.9928 | -0.2610 | 0.500 | 0.4844 | 1.0000 | n/a | -0.03 | 99 / 99 | 1.00 | 0.5696 | 0.5733 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.4795 | -0.039 | 0.9016 | -0.1697 | 0.500 | 0.8506 | 1.0000 | -0.06 | -0.04 | 98 / 99 | 0.99 | 0.6133 | 0.6139 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.4990 | 0.000 | 0.9007 | -0.1689 | 0.531 | 0.8584 | 1.0000 | -0.00 | -0.00 | 99 / 99 | 1.00 | 0.5100 | 0.5104 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.5039 | -0.011 | 0.9049 | -0.1731 | 0.500 | 0.9209 | 1.0000 | 0.01 | 0.01 | 99 / 99 | 1.00 | 0.4796 | 0.4819 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5049 | 0.000 | 0.7319 | +0.0000 | 0.500 | 0.5000 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.4743 | 0.3593 | None / None / None |

### World W, seed 90130: W: rule weaker than the information available

Outside density 0.2879; block present 32.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.5034 (32/32), p_S = 0.50 (n_ge = 49 of 99, n_deg = 0), p_P = 0.4939; ceiling_full = 0.5176, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 1.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5034 | 0.090 | 1.1342 | -0.4116 | 0.500 | 0.5176 | 1.0000 | 0.19 | 0.01 | 49 / 99 | 0.50 | 0.4939 | 0.4847 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5156 | 0.147 | 1.0328 | -0.3101 | 0.500 | 0.5146 | 1.0000 | 1.07 | 0.03 | 0 / 99 | 0.01 | 0.4296 | 0.4225 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7451 | 2.124 | 0.7614 | -0.0387 | 0.500 | 0.8887 | 1.0000 | 0.63 | 0.49 | 0 / 99 | 0.01 | 0.0004 | 0.0018 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.6846 | 1.732 | 0.9117 | -0.1890 | 0.500 | 0.9414 | 1.0000 | 0.42 | 0.37 | 0 / 99 | 0.01 | 0.0046 | 0.0123 | 1.0 / 1.0 / 1.0 |
| BF_4 | 0.6895 | 1.935 | 0.9131 | -0.1905 | 0.531 | 0.9893 | 1.0000 | 0.39 | 0.38 | 0 / 99 | 0.01 | 0.0028 | 0.0089 | 1.0 / 1.0 / 1.0 |
| N1 | 0.5020 | 0.000 | 0.7226 | +0.0000 | 0.469 | 0.5020 | 0.5000 | 1.00 | n/a | 99 / 99 | 1.00 | 0.4875 | 0.4632 | None / None / None |

### World W, seed 90131: W: rule weaker than the information available

Outside density 0.2930; block present 32.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.5312 (32/32), p_S = 0.99 (n_ge = 98 of 99, n_deg = 0), p_P = 0.3426; ceiling_full = 0.5342, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 1.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5312 | 0.108 | 1.0712 | -0.3604 | 0.500 | 0.5342 | 1.0000 | 0.91 | 0.06 | 98 / 99 | 0.99 | 0.3426 | 0.3459 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5352 | 0.153 | 1.0046 | -0.2938 | 0.500 | 0.5332 | 1.0000 | 1.06 | 0.07 | 99 / 99 | 1.00 | 0.3187 | 0.3280 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7295 | 1.902 | 0.7475 | -0.0368 | 0.531 | 0.8662 | 1.0000 | 0.63 | 0.46 | 0 / 99 | 0.01 | 0.0007 | 0.0025 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.6953 | 1.778 | 0.8322 | -0.1214 | 0.562 | 0.9277 | 1.0000 | 0.46 | 0.39 | 0 / 99 | 0.01 | 0.0036 | 0.0081 | 1.0 / 1.0 / 1.0 |
| BF_4 | 0.6777 | 1.724 | 0.8931 | -0.1824 | 0.531 | 0.9854 | 1.0000 | 0.37 | 0.36 | 0 / 99 | 0.01 | 0.0069 | 0.0150 | 1.0 / 1.0 / 1.0 |
| N1 | 0.5674 | 0.000 | 0.7107 | +0.0000 | 0.562 | 0.5645 | 0.5000 | 1.05 | n/a | 99 / 99 | 1.00 | 0.1763 | 0.0001 | None / None / None |

### World W, seed 90132: W: rule weaker than the information available

Outside density 0.2918; block present 32.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.5225 (32/32), p_S = 0.03 (n_ge = 2 of 99, n_deg = 0), p_P = 0.3845; ceiling_full = 0.5244, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 1.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5225 | 0.202 | 1.1530 | -0.4358 | 0.500 | 0.5244 | 1.0000 | 0.92 | 0.04 | 2 / 99 | 0.03 | 0.3845 | 0.3970 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5205 | 0.249 | 1.0397 | -0.3224 | 0.500 | 0.5215 | 1.0000 | 0.95 | 0.04 | 0 / 99 | 0.01 | 0.3965 | 0.4065 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7334 | 1.805 | 0.8134 | -0.0962 | 0.500 | 0.8604 | 1.0000 | 0.65 | 0.47 | 0 / 99 | 0.01 | 0.0007 | 0.0023 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.7041 | 1.562 | 0.8842 | -0.1670 | 0.500 | 0.9443 | 1.0000 | 0.46 | 0.41 | 0 / 99 | 0.01 | 0.0025 | 0.0074 | 1.0 / 1.0 / 1.0 |
| BF_4 | 0.6816 | 1.564 | 0.8925 | -0.1753 | 0.500 | 0.9814 | 1.0000 | 0.38 | 0.36 | 0 / 99 | 0.01 | 0.0054 | 0.0138 | 1.0 / 1.0 / 1.0 |
| N1 | 0.5000 | 0.000 | 0.7173 | +0.0000 | 0.500 | 0.4980 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5055 | 0.5126 | None / None / None |

### World W, seed 90133: W: rule weaker than the information available

Outside density 0.2867; block present 32.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.5190 (32/32), p_S = 0.03 (n_ge = 2 of 99, n_deg = 0), p_P = 0.4029; ceiling_full = 0.5273, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 1.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5190 | 0.079 | 1.0300 | -0.3035 | 0.500 | 0.5273 | 1.0000 | 0.70 | 0.04 | 2 / 99 | 0.03 | 0.4029 | 0.4069 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5186 | 0.095 | 0.9497 | -0.2232 | 0.500 | 0.5234 | 1.0000 | 0.79 | 0.04 | 0 / 99 | 0.01 | 0.4082 | 0.4116 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7549 | 2.546 | 0.5645 | +0.1619 | 0.562 | 0.9893 | 1.0000 | 0.52 | 0.51 | 0 / 99 | 0.01 | 0.0004 | 0.0010 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.7510 | 2.236 | 0.6544 | +0.0721 | 0.562 | 0.9990 | 1.0000 | 0.50 | 0.50 | 0 / 99 | 0.01 | 0.0004 | 0.0015 | 1.0 / 1.0 / 1.0 |
| BF_4 | 0.7500 | 2.544 | 0.6818 | +0.0447 | 0.594 | 0.9990 | 1.0000 | 0.50 | 0.50 | 0 / 99 | 0.01 | 0.0003 | 0.0019 | 1.0 / 1.0 / 1.0 |
| N1 | 0.4766 | 0.000 | 0.7265 | +0.0000 | 0.438 | 0.4766 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.6269 | 0.9534 | None / None / None |

### World W, seed 90134: W: rule weaker than the information available

Outside density 0.2975; block present 32.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.5029 (32/32), p_S = 0.49 (n_ge = 48 of 99, n_deg = 0), p_P = 0.4853; ceiling_full = 0.5156, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5029 | 0.162 | 1.0722 | -0.3299 | 0.500 | 0.5156 | 1.0000 | 0.19 | 0.01 | 48 / 99 | 0.49 | 0.4853 | 0.4849 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5146 | 0.214 | 0.9826 | -0.2402 | 0.500 | 0.5361 | 1.0000 | 0.41 | 0.03 | 0 / 99 | 0.01 | 0.4223 | 0.4268 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7529 | 2.457 | 0.6171 | +0.1252 | 0.562 | 0.9746 | 1.0000 | 0.53 | 0.51 | 0 / 99 | 0.01 | 0.0003 | 0.0010 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.7578 | 2.299 | 0.6734 | +0.0689 | 0.625 | 0.9863 | 1.0000 | 0.53 | 0.52 | 0 / 99 | 0.01 | 0.0003 | 0.0006 | 1.0 / 1.0 / 1.0 |
| BF_4 | 0.7285 | 1.229 | 0.6693 | +0.0730 | 0.562 | 0.9502 | 1.0000 | 0.51 | 0.46 | 0 / 99 | 0.01 | 0.0009 | 0.0027 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5020 | 0.000 | 0.7423 | +0.0000 | 0.531 | 0.4961 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.4912 | 0.4586 | None / None / None |

### World M0.5, seed 90140: R: regrows

Outside density 0.1516; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.7354 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0004; ceiling_full = 0.9883, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 100, BF_3 100, BF_4 100.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7354 | 0.572 | 0.6883 | +0.1227 | 0.656 | 0.9883 | 1.0000 | 0.48 | 0.47 | 0 / 99 | 0.01 | 0.0004 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7363 | 0.575 | 0.6836 | +0.1273 | 0.656 | 0.9922 | 1.0000 | 0.48 | 0.47 | 0 / 99 | 0.01 | 0.0004 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.4932 | 0.000 | 0.8110 | +0.0000 | 0.500 | 0.9961 | 1.0000 | -0.01 | -0.01 | 98 / 99 | 0.99 | 0.5468 | 0.6888 | 100.0 / 3.0 / 1.0 |
| BF_3 | 0.4932 | 0.000 | 0.8110 | +0.0000 | 0.500 | 0.9941 | 1.0000 | -0.01 | -0.01 | 99 / 99 | 1.00 | 0.5468 | 0.6888 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.4932 | 0.000 | 0.8110 | +0.0000 | 0.500 | 0.9971 | 1.0000 | -0.01 | -0.01 | 99 / 99 | 1.00 | 0.5468 | 0.6888 | 100.0 / 3.0 / 1.0 |
| N1 | 0.4932 | 0.000 | 0.8110 | +0.0000 | 0.500 | 0.4951 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5468 | 0.6888 | None / None / None |

### World M0.5, seed 90141: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1370; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 1.0000 >= 0.90)]. rule #2.1: AUC = 0.5005 (32/32), p_S = 0.50 (n_ge = 49 of 99, n_deg = 0), p_P = 0.4998; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 3, BF_4 3; G reached through lambda = 100 on rule #2.1, BF_1, BF_2: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5005 | 0.000 | 0.8697 | +0.0122 | 0.500 | 1.0000 | 1.0000 | 0.00 | 0.00 | 49 / 99 | 0.50 | 0.4998 | 0.4766 | 100.0 / 3.0 / 1.0 |
| BF_1 | 0.4990 | 0.000 | 0.8819 | +0.0000 | 0.500 | 1.0000 | 1.0000 | -0.00 | -0.00 | 93 / 99 | 0.94 | 0.5115 | 0.5552 | 100.0 / 3.0 / 1.0 |
| BF_2 | 0.4990 | 0.000 | 0.8819 | +0.0000 | 0.500 | 1.0000 | 1.0000 | -0.00 | -0.00 | 99 / 99 | 1.00 | 0.5115 | 0.5552 | 100.0 / 3.0 / 1.0 |
| BF_3 | 0.5664 | 0.198 | 0.8563 | +0.0256 | 0.562 | 1.0000 | 1.0000 | 0.13 | 0.13 | 0 / 99 | 0.01 | 0.1818 | 0.0231 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.5635 | 0.200 | 0.8568 | +0.0250 | 0.531 | 1.0000 | 1.0000 | 0.13 | 0.13 | 0 / 99 | 0.01 | 0.1935 | 0.0308 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4990 | 0.000 | 0.8819 | +0.0000 | 0.500 | 0.4961 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5115 | 0.5552 | None / None / None |

### World M0.5, seed 90142: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1420; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 0.9893 >= 0.90)]. rule #2.1: AUC = 0.5308 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.3425; ceiling_full = 0.9893, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5308 | 0.113 | 0.8817 | +0.0236 | 0.562 | 0.9893 | 1.0000 | 0.06 | 0.06 | 0 / 99 | 0.01 | 0.3425 | 0.1306 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.5283 | 0.111 | 0.8828 | +0.0226 | 0.562 | 0.9902 | 1.0000 | 0.06 | 0.06 | 1 / 99 | 0.02 | 0.3560 | 0.1491 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.4990 | 0.000 | 0.9053 | +0.0000 | 0.500 | 0.9961 | 1.0000 | -0.00 | -0.00 | 97 / 99 | 0.98 | 0.5140 | 0.5302 | 100.0 / 3.0 / 1.0 |
| BF_3 | 0.4990 | 0.000 | 0.9053 | +0.0000 | 0.500 | 0.9951 | 1.0000 | -0.00 | -0.00 | 98 / 99 | 0.99 | 0.5140 | 0.5302 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.4990 | 0.000 | 0.9053 | +0.0000 | 0.500 | 0.9951 | 1.0000 | -0.00 | -0.00 | 98 / 99 | 0.99 | 0.5140 | 0.5302 | 100.0 / 3.0 / 1.0 |
| N1 | 0.4990 | 0.000 | 0.9053 | +0.0000 | 0.500 | 0.5146 | 0.5000 | -0.07 | n/a | 99 / 99 | 1.00 | 0.5140 | 0.5302 | None / None / None |

### World M0.5, seed 90143: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1533; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5327 < 0.90)]. rule #2.1: AUC = 0.5283 (32/32), p_S = 0.45 (n_ge = 44 of 99, n_deg = 0), p_P = 0.3590; ceiling_full = 0.5327, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 3; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5283 | 0.000 | 0.7785 | +0.0131 | 0.531 | 0.5327 | 1.0000 | 0.87 | 0.06 | 44 / 99 | 0.45 | 0.3590 | 0.0466 | 100.0 / 100.0 / 1.0 |
| BF_1 | 0.5264 | 0.000 | 0.7916 | +0.0000 | 0.531 | 0.5371 | 1.0000 | 0.71 | 0.05 | 97 / 99 | 0.98 | 0.3699 | 0.0709 | 100.0 / 100.0 / 1.0 |
| BF_2 | 0.5264 | 0.000 | 0.7916 | +0.0000 | 0.531 | 0.5371 | 1.0000 | 0.71 | 0.05 | 99 / 99 | 1.00 | 0.3699 | 0.0709 | 100.0 / 100.0 / 1.0 |
| BF_3 | 0.5264 | 0.000 | 0.7916 | +0.0000 | 0.531 | 0.5371 | 1.0000 | 0.71 | 0.05 | 99 / 99 | 1.00 | 0.3699 | 0.0709 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.4893 | -0.094 | 0.8402 | -0.0486 | 0.594 | 0.9688 | 1.0000 | -0.02 | -0.02 | 99 / 99 | 1.00 | 0.5732 | 0.5923 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5264 | 0.000 | 0.7916 | +0.0000 | 0.531 | 0.5371 | 0.5000 | 0.71 | n/a | 99 / 99 | 1.00 | 0.3699 | 0.0709 | None / None / None |

### World M0.5, seed 90144: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1507; block present 32.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.6 (bracket (0.5, 0.6]); family limit = 0.75 (set by BF_2, BF_3, BF_4); transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma; per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 3/5, 2/5; 0.75: 5/5, 5/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 0.9990 >= 0.90)]. rule #2.1: AUC = 0.4902 (32/32), p_S = 0.44 (n_ge = 43 of 99, n_deg = 0), p_P = 0.5525; ceiling_full = 0.9990, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 3, BF_3 3, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4902 | 0.000 | 0.8582 | -0.0005 | 0.469 | 0.9990 | 1.0000 | -0.02 | -0.02 | 43 / 99 | 0.44 | 0.5525 | 0.7962 | 100.0 / 3.0 / 1.0 |
| BF_1 | 0.4902 | 0.000 | 0.8577 | +0.0000 | 0.500 | 0.9980 | 1.0000 | -0.02 | -0.02 | 97 / 99 | 0.98 | 0.5518 | 0.8017 | 100.0 / 3.0 / 1.0 |
| BF_2 | 0.4980 | 0.008 | 0.8807 | -0.0230 | 0.469 | 0.9971 | 1.0000 | -0.00 | -0.00 | 0 / 99 | 0.01 | 0.5223 | 0.5271 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5537 | 0.128 | 0.8575 | +0.0003 | 0.594 | 0.9980 | 1.0000 | 0.11 | 0.11 | 0 / 99 | 0.01 | 0.2380 | 0.0990 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.4902 | 0.000 | 0.8577 | +0.0000 | 0.500 | 0.9922 | 1.0000 | -0.02 | -0.02 | 98 / 99 | 0.99 | 0.5518 | 0.8017 | 100.0 / 3.0 / 1.0 |
| N1 | 0.4902 | 0.000 | 0.8577 | +0.0000 | 0.500 | 0.4922 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5518 | 0.8017 | None / None / None |

### World M1.0, seed 90150: R: regrows

Outside density 0.1687; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.9697 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.9697 | 1.791 | 0.4941 | +0.3303 | 0.938 | 1.0000 | 1.0000 | 0.94 | 0.94 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.9688 | 1.547 | 0.5082 | +0.3162 | 0.938 | 1.0000 | 1.0000 | 0.94 | 0.94 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.8877 | 1.012 | 0.6066 | +0.2178 | 0.812 | 0.9990 | 1.0000 | 0.78 | 0.78 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.8535 | 0.984 | 0.6209 | +0.2035 | 0.750 | 1.0000 | 1.0000 | 0.71 | 0.71 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.8564 | 0.982 | 0.6248 | +0.1996 | 0.750 | 0.9990 | 1.0000 | 0.71 | 0.71 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5078 | 0.000 | 0.8244 | +0.0000 | 0.562 | 0.5039 | 0.5000 | 2.00 | n/a | 99 / 99 | 1.00 | 0.4656 | 0.3585 | None / None / None |

### World M1.0, seed 90151: R: regrows

Outside density 0.1716; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.9541 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.9541 | 1.749 | 0.4975 | +0.3006 | 0.875 | 1.0000 | 1.0000 | 0.91 | 0.91 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.9727 | 1.585 | 0.4825 | +0.3156 | 0.875 | 1.0000 | 1.0000 | 0.95 | 0.95 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.9307 | 1.076 | 0.5668 | +0.2313 | 0.875 | 1.0000 | 1.0000 | 0.86 | 0.86 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.8984 | 1.086 | 0.5727 | +0.2254 | 0.812 | 1.0000 | 1.0000 | 0.80 | 0.80 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.8779 | 1.022 | 0.5922 | +0.2059 | 0.812 | 1.0000 | 1.0000 | 0.76 | 0.76 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5059 | 0.000 | 0.7981 | +0.0000 | 0.469 | 0.5029 | 0.5000 | 2.00 | n/a | 99 / 99 | 1.00 | 0.4717 | 0.3377 | None / None / None |

### World M1.0, seed 90152: R: regrows

Outside density 0.1634; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.8555 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.8555 | 1.015 | 0.6171 | +0.2161 | 0.781 | 1.0000 | 1.0000 | 0.71 | 0.71 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 1.0 / 1.0 |
| BF_1 | 0.8525 | 1.067 | 0.6090 | +0.2243 | 0.812 | 0.9980 | 1.0000 | 0.71 | 0.71 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.8242 | 1.030 | 0.6200 | +0.2133 | 0.750 | 0.9990 | 1.0000 | 0.65 | 0.65 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7979 | 1.050 | 0.6297 | +0.2036 | 0.719 | 0.9990 | 1.0000 | 0.60 | 0.60 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7998 | 1.094 | 0.6293 | +0.2040 | 0.719 | 1.0000 | 1.0000 | 0.60 | 0.60 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5068 | 0.000 | 0.8333 | +0.0000 | 0.469 | 0.5068 | 0.5000 | 1.00 | n/a | 99 / 99 | 1.00 | 0.4498 | 0.3558 | None / None / None |

### World M1.0, seed 90153: R: regrows

Outside density 0.1682; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.9736 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.9736 | 1.842 | 0.4644 | +0.3138 | 0.875 | 1.0000 | 1.0000 | 0.95 | 0.95 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.9697 | 1.747 | 0.4512 | +0.3270 | 0.875 | 1.0000 | 1.0000 | 0.94 | 0.94 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.9121 | 1.200 | 0.5367 | +0.2415 | 0.875 | 1.0000 | 1.0000 | 0.82 | 0.82 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.9092 | 1.220 | 0.5356 | +0.2426 | 0.844 | 1.0000 | 1.0000 | 0.82 | 0.82 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.8867 | 1.186 | 0.5451 | +0.2331 | 0.812 | 1.0000 | 1.0000 | 0.77 | 0.77 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5137 | 0.000 | 0.7782 | +0.0000 | 0.500 | 0.5146 | 0.5000 | 0.93 | n/a | 99 / 99 | 1.00 | 0.4243 | 0.2458 | None / None / None |

### World M1.0, seed 90154: R: regrows

Outside density 0.1673; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.7588 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7588 | 0.788 | 0.6147 | +0.1705 | 0.688 | 1.0000 | 1.0000 | 0.52 | 0.52 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 1.0 / 1.0 |
| BF_1 | 0.7598 | 0.760 | 0.6199 | +0.1652 | 0.719 | 0.9980 | 1.0000 | 0.52 | 0.52 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.7695 | 0.793 | 0.6171 | +0.1681 | 0.656 | 0.9990 | 1.0000 | 0.54 | 0.54 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7363 | 0.835 | 0.6326 | +0.1525 | 0.656 | 0.9873 | 1.0000 | 0.48 | 0.47 | 0 / 99 | 0.01 | 0.0004 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7217 | 0.760 | 0.6510 | +0.1342 | 0.656 | 0.9883 | 1.0000 | 0.45 | 0.44 | 0 / 99 | 0.01 | 0.0006 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5049 | 0.000 | 0.7851 | +0.0000 | 0.500 | 0.5068 | 0.5000 | 0.71 | n/a | 99 / 99 | 1.00 | 0.4806 | 0.3139 | None / None / None |

### World M0.6, seed 90160: R: regrows

Outside density 0.1399; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.7451 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0002; ceiling_full = 0.9971, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 100.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7451 | 0.589 | 0.6499 | +0.1415 | 0.656 | 0.9971 | 1.0000 | 0.49 | 0.49 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7334 | 0.558 | 0.6676 | +0.1238 | 0.656 | 0.9971 | 1.0000 | 0.47 | 0.47 | 0 / 99 | 0.01 | 0.0005 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.7256 | 0.570 | 0.6700 | +0.1214 | 0.625 | 0.9932 | 1.0000 | 0.46 | 0.45 | 0 / 99 | 0.01 | 0.0006 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.6982 | 0.492 | 0.6872 | +0.1042 | 0.625 | 0.9971 | 1.0000 | 0.40 | 0.40 | 0 / 99 | 0.01 | 0.0031 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.5068 | 0.000 | 0.7914 | +0.0000 | 0.500 | 0.9980 | 1.0000 | 0.01 | 0.01 | 99 / 99 | 1.00 | 0.4692 | 0.2742 | 100.0 / 3.0 / 1.0 |
| N1 | 0.5068 | 0.000 | 0.7914 | +0.0000 | 0.500 | 0.5020 | 0.5000 | 3.50 | n/a | 99 / 99 | 1.00 | 0.4692 | 0.2742 | None / None / None |

### World M0.6, seed 90161: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.6; transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma)

Outside density 0.1483; block present 32.
Verdict line: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.6; transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma). rule #2.1: AUC = 0.5654 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.1888; ceiling_full = 0.9717, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 100, BF_4 100.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5654 | 0.241 | 0.8621 | +0.0355 | 0.500 | 0.9717 | 1.0000 | 0.14 | 0.13 | 0 / 99 | 0.01 | 0.1888 | 0.0107 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.5918 | 0.229 | 0.8519 | +0.0457 | 0.594 | 0.9805 | 1.0000 | 0.19 | 0.18 | 0 / 99 | 0.01 | 0.1072 | 0.0014 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.6025 | 0.226 | 0.8554 | +0.0422 | 0.594 | 1.0000 | 1.0000 | 0.21 | 0.21 | 0 / 99 | 0.01 | 0.0832 | 0.0024 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5322 | 0.000 | 0.8976 | +0.0000 | 0.500 | 0.9990 | 1.0000 | 0.06 | 0.06 | 99 / 99 | 1.00 | 0.3292 | 0.0259 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.5322 | 0.000 | 0.8976 | +0.0000 | 0.500 | 0.9990 | 1.0000 | 0.06 | 0.06 | 99 / 99 | 1.00 | 0.3292 | 0.0259 | 100.0 / 3.0 / 1.0 |
| N1 | 0.5322 | 0.000 | 0.8976 | +0.0000 | 0.500 | 0.5234 | 0.5000 | 1.38 | n/a | 99 / 99 | 1.00 | 0.3292 | 0.0259 | None / None / None |

### World M0.6, seed 90162: R: regrows

Outside density 0.1459; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.7300 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0008; ceiling_full = 0.9980, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7300 | 0.583 | 0.7064 | +0.1332 | 0.688 | 0.9980 | 1.0000 | 0.46 | 0.46 | 0 / 99 | 0.01 | 0.0008 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7568 | 0.614 | 0.7039 | +0.1357 | 0.656 | 1.0000 | 1.0000 | 0.51 | 0.51 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.5879 | 0.238 | 0.7971 | +0.0425 | 0.531 | 0.9990 | 1.0000 | 0.18 | 0.18 | 0 / 99 | 0.01 | 0.1148 | 0.0275 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.6016 | 0.276 | 0.7945 | +0.0451 | 0.594 | 0.9980 | 1.0000 | 0.20 | 0.20 | 0 / 99 | 0.01 | 0.0811 | 0.0175 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.6016 | 0.269 | 0.7999 | +0.0397 | 0.594 | 0.9990 | 1.0000 | 0.20 | 0.20 | 0 / 99 | 0.01 | 0.0816 | 0.0209 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5098 | 0.000 | 0.8396 | +0.0000 | 0.500 | 0.5195 | 0.5000 | 0.50 | n/a | 99 / 99 | 1.00 | 0.4497 | 0.2994 | None / None / None |

### World M0.6, seed 90163: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.6; transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma)

Outside density 0.1516; block present 32.
Verdict line: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.6; transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma). rule #2.1: AUC = 0.6729 (32/32), p_S = 0.02 (n_ge = 1 of 99, n_deg = 0), p_P = 0.0082; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 100, BF_3 100, BF_4 100.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6729 | 0.437 | 0.7539 | +0.0880 | 0.656 | 1.0000 | 1.0000 | 0.35 | 0.35 | 1 / 99 | 0.02 | 0.0082 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6787 | 0.438 | 0.7472 | +0.0948 | 0.656 | 1.0000 | 1.0000 | 0.36 | 0.36 | 0 / 99 | 0.01 | 0.0070 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.5146 | 0.000 | 0.8419 | +0.0000 | 0.562 | 1.0000 | 1.0000 | 0.03 | 0.03 | 98 / 99 | 0.99 | 0.4239 | 0.1341 | 100.0 / 3.0 / 1.0 |
| BF_3 | 0.5146 | 0.000 | 0.8419 | +0.0000 | 0.562 | 0.9990 | 1.0000 | 0.03 | 0.03 | 98 / 99 | 0.99 | 0.4239 | 0.1341 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.5146 | 0.000 | 0.8419 | +0.0000 | 0.562 | 1.0000 | 1.0000 | 0.03 | 0.03 | 99 / 99 | 1.00 | 0.4239 | 0.1341 | 100.0 / 3.0 / 1.0 |
| N1 | 0.5146 | 0.000 | 0.8419 | +0.0000 | 0.562 | 0.5146 | 0.5000 | 1.00 | n/a | 99 / 99 | 1.00 | 0.4239 | 0.1341 | None / None / None |

### World M0.6, seed 90164: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.6; transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma)

Outside density 0.1370; block present 32.
Verdict line: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.6; transition band [0.6, 0.75): 1 grid step(s), 0.15 in gamma). rule #2.1: AUC = 0.6357 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0308; ceiling_full = 0.9824, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 100, BF_3 100, BF_4 100.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6357 | 0.361 | 0.7864 | +0.0843 | 0.594 | 0.9824 | 1.0000 | 0.28 | 0.27 | 0 / 99 | 0.01 | 0.0308 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6260 | 0.332 | 0.8020 | +0.0687 | 0.594 | 0.9834 | 1.0000 | 0.26 | 0.25 | 0 / 99 | 0.01 | 0.0405 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.5225 | 0.000 | 0.8707 | +0.0000 | 0.500 | 0.9844 | 1.0000 | 0.05 | 0.04 | 99 / 99 | 1.00 | 0.3924 | 0.0662 | 100.0 / 3.0 / 1.0 |
| BF_3 | 0.5225 | 0.000 | 0.8707 | +0.0000 | 0.500 | 0.9922 | 1.0000 | 0.05 | 0.04 | 99 / 99 | 1.00 | 0.3924 | 0.0662 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.5225 | 0.000 | 0.8707 | +0.0000 | 0.500 | 0.9893 | 1.0000 | 0.05 | 0.04 | 99 / 99 | 1.00 | 0.3924 | 0.0662 | 100.0 / 3.0 / 1.0 |
| N1 | 0.5225 | 0.000 | 0.8707 | +0.0000 | 0.500 | 0.5244 | 0.5000 | 0.92 | n/a | 99 / 99 | 1.00 | 0.3924 | 0.0662 | None / None / None |

### World M0.75, seed 90170: R: regrows

Outside density 0.1579; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.8711 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.8711 | 1.019 | 0.6566 | +0.2194 | 0.844 | 1.0000 | 1.0000 | 0.74 | 0.74 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.8691 | 1.049 | 0.6502 | +0.2258 | 0.844 | 1.0000 | 1.0000 | 0.74 | 0.74 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.8672 | 1.073 | 0.6411 | +0.2349 | 0.750 | 1.0000 | 1.0000 | 0.73 | 0.73 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.8330 | 0.943 | 0.6673 | +0.2087 | 0.750 | 1.0000 | 1.0000 | 0.67 | 0.67 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.8105 | 0.914 | 0.6787 | +0.1974 | 0.750 | 1.0000 | 1.0000 | 0.62 | 0.62 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4941 | 0.000 | 0.8760 | +0.0000 | 0.438 | 0.5059 | 0.5000 | -1.00 | n/a | 99 / 99 | 1.00 | 0.5313 | 0.6495 | None / None / None |

### World M0.75, seed 90171: R: regrows

Outside density 0.1591; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.8760 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.8760 | 0.986 | 0.5744 | +0.2150 | 0.781 | 1.0000 | 1.0000 | 0.75 | 0.75 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.8760 | 0.934 | 0.5833 | +0.2061 | 0.781 | 1.0000 | 1.0000 | 0.75 | 0.75 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.8770 | 0.984 | 0.5778 | +0.2116 | 0.781 | 1.0000 | 1.0000 | 0.75 | 0.75 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.8760 | 0.990 | 0.5778 | +0.2116 | 0.781 | 1.0000 | 1.0000 | 0.75 | 0.75 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.8457 | 0.889 | 0.6003 | +0.1892 | 0.750 | 1.0000 | 1.0000 | 0.69 | 0.69 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4863 | 0.000 | 0.7894 | +0.0000 | 0.469 | 0.4883 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5766 | 0.8042 | None / None / None |

### World M0.75, seed 90172: R: regrows

Outside density 0.1536; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.7861 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 0.9971, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7861 | 0.887 | 0.6394 | +0.1879 | 0.719 | 0.9971 | 1.0000 | 0.58 | 0.57 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7861 | 0.836 | 0.6520 | +0.1754 | 0.719 | 0.9961 | 1.0000 | 0.58 | 0.57 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.6885 | 0.526 | 0.7187 | +0.1087 | 0.594 | 0.9990 | 1.0000 | 0.38 | 0.38 | 0 / 99 | 0.01 | 0.0036 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.6982 | 0.553 | 0.7068 | +0.1205 | 0.625 | 0.9951 | 1.0000 | 0.40 | 0.40 | 0 / 99 | 0.01 | 0.0023 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.6738 | 0.504 | 0.7255 | +0.1019 | 0.625 | 0.9980 | 1.0000 | 0.35 | 0.35 | 0 / 99 | 0.01 | 0.0080 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4951 | 0.000 | 0.8273 | +0.0000 | 0.500 | 0.4961 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5353 | 0.6415 | None / None / None |

### World M0.75, seed 90173: R: regrows

Outside density 0.1617; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.7246 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0010; ceiling_full = 0.9941, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7246 | 0.658 | 0.6834 | +0.1406 | 0.688 | 0.9941 | 1.0000 | 0.45 | 0.45 | 0 / 99 | 0.01 | 0.0010 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7256 | 0.658 | 0.6845 | +0.1394 | 0.688 | 0.9990 | 1.0000 | 0.45 | 0.45 | 0 / 99 | 0.01 | 0.0014 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.7656 | 0.794 | 0.6546 | +0.1693 | 0.688 | 1.0000 | 1.0000 | 0.53 | 0.53 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7705 | 0.783 | 0.6526 | +0.1713 | 0.719 | 1.0000 | 1.0000 | 0.54 | 0.54 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7842 | 0.762 | 0.6581 | +0.1658 | 0.719 | 1.0000 | 1.0000 | 0.57 | 0.57 | 0 / 99 | 0.01 | 0.0003 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5127 | 0.000 | 0.8239 | +0.0000 | 0.531 | 0.5068 | 0.5000 | 1.86 | n/a | 99 / 99 | 1.00 | 0.4330 | 0.2071 | None / None / None |

### World M0.75, seed 90174: R: regrows

Outside density 0.1553; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.7402 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0003; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7402 | 0.982 | 0.6151 | +0.1884 | 0.656 | 1.0000 | 1.0000 | 0.48 | 0.48 | 0 / 99 | 0.01 | 0.0003 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7363 | 0.947 | 0.6142 | +0.1892 | 0.656 | 1.0000 | 1.0000 | 0.47 | 0.47 | 0 / 99 | 0.01 | 0.0004 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.7393 | 0.890 | 0.6239 | +0.1795 | 0.656 | 1.0000 | 1.0000 | 0.48 | 0.48 | 0 / 99 | 0.01 | 0.0006 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.6885 | 0.781 | 0.6603 | +0.1432 | 0.656 | 0.9990 | 1.0000 | 0.38 | 0.38 | 0 / 99 | 0.01 | 0.0046 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.6934 | 0.784 | 0.6622 | +0.1413 | 0.625 | 1.0000 | 1.0000 | 0.39 | 0.39 | 0 / 99 | 0.01 | 0.0037 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4902 | 0.000 | 0.8035 | +0.0000 | 0.500 | 0.4922 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5529 | 0.8175 | None / None / None |

### World M0.85, seed 90180: R: regrows

Outside density 0.1497; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.9517 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.9517 | 1.723 | 0.5499 | +0.2964 | 0.906 | 1.0000 | 1.0000 | 0.90 | 0.90 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.9512 | 1.501 | 0.5440 | +0.3022 | 0.875 | 1.0000 | 1.0000 | 0.90 | 0.90 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.8633 | 0.931 | 0.6471 | +0.1991 | 0.875 | 0.9990 | 1.0000 | 0.73 | 0.73 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.8477 | 0.947 | 0.6454 | +0.2009 | 0.844 | 0.9990 | 1.0000 | 0.70 | 0.70 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.8545 | 0.957 | 0.6473 | +0.1990 | 0.812 | 1.0000 | 1.0000 | 0.71 | 0.71 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5244 | 0.000 | 0.8463 | +0.0000 | 0.500 | 0.5244 | 0.5000 | 1.00 | n/a | 99 / 99 | 1.00 | 0.3623 | 0.1043 | None / None / None |

### World M0.85, seed 90181: R: regrows

Outside density 0.1608; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.7764 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0002; ceiling_full = 0.9873, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7764 | 0.652 | 0.7353 | +0.1276 | 0.688 | 0.9873 | 1.0000 | 0.57 | 0.55 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7861 | 0.637 | 0.7200 | +0.1428 | 0.688 | 0.9961 | 1.0000 | 0.58 | 0.57 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.7393 | 0.527 | 0.7531 | +0.1097 | 0.656 | 0.9990 | 1.0000 | 0.48 | 0.48 | 0 / 99 | 0.01 | 0.0004 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7227 | 0.545 | 0.7522 | +0.1107 | 0.656 | 0.9990 | 1.0000 | 0.45 | 0.45 | 0 / 99 | 0.01 | 0.0009 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.6924 | 0.502 | 0.7674 | +0.0955 | 0.656 | 0.9980 | 1.0000 | 0.39 | 0.38 | 0 / 99 | 0.01 | 0.0037 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4922 | 0.000 | 0.8628 | +0.0000 | 0.500 | 0.4980 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5421 | 0.7597 | None / None / None |

### World M0.85, seed 90182: R: regrows

Outside density 0.1555; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.8428 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.8428 | 1.144 | 0.5680 | +0.2359 | 0.750 | 1.0000 | 1.0000 | 0.69 | 0.69 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.8438 | 1.107 | 0.5746 | +0.2293 | 0.750 | 1.0000 | 1.0000 | 0.69 | 0.69 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.8154 | 1.044 | 0.5903 | +0.2136 | 0.719 | 1.0000 | 1.0000 | 0.63 | 0.63 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7910 | 0.992 | 0.6057 | +0.1982 | 0.688 | 1.0000 | 1.0000 | 0.58 | 0.58 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7480 | 0.872 | 0.6366 | +0.1673 | 0.656 | 1.0000 | 1.0000 | 0.50 | 0.50 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5059 | 0.000 | 0.8039 | +0.0000 | 0.500 | 0.5039 | 0.5000 | 1.50 | n/a | 99 / 99 | 1.00 | 0.4703 | 0.2435 | None / None / None |

### World M0.85, seed 90183: R: regrows

Outside density 0.1497; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.8398 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 0.9990, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.8398 | 0.983 | 0.6312 | +0.2015 | 0.781 | 0.9990 | 1.0000 | 0.68 | 0.68 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.8330 | 0.943 | 0.6295 | +0.2032 | 0.781 | 0.9990 | 1.0000 | 0.67 | 0.67 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.8242 | 0.914 | 0.6356 | +0.1972 | 0.719 | 1.0000 | 1.0000 | 0.65 | 0.65 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.8115 | 0.904 | 0.6410 | +0.1917 | 0.750 | 0.9980 | 1.0000 | 0.63 | 0.62 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.8066 | 0.908 | 0.6520 | +0.1808 | 0.781 | 0.9941 | 1.0000 | 0.62 | 0.61 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4902 | -0.000 | 0.8328 | +0.0000 | 0.531 | 0.4951 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.5559 | 0.7249 | None / None / None |

### World M0.85, seed 90184: R: regrows

Outside density 0.1641; block present 32.
Verdict line: R: regrows. rule #2.1: AUC = 0.8115 (32/32), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.8115 | 0.891 | 0.6379 | +0.2039 | 0.781 | 1.0000 | 1.0000 | 0.62 | 0.62 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.8057 | 0.887 | 0.6458 | +0.1960 | 0.781 | 0.9990 | 1.0000 | 0.61 | 0.61 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.8145 | 0.938 | 0.6408 | +0.2010 | 0.781 | 0.9980 | 1.0000 | 0.63 | 0.63 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7812 | 0.928 | 0.6504 | +0.1914 | 0.719 | 0.9971 | 1.0000 | 0.57 | 0.56 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7822 | 0.918 | 0.6527 | +0.1891 | 0.719 | 0.9980 | 1.0000 | 0.57 | 0.56 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5049 | 0.000 | 0.8418 | +0.0000 | 0.469 | 0.5000 | 0.5000 | n/a | n/a | 99 / 99 | 1.00 | 0.4799 | 0.3807 | None / None / None |

## The registered reading (section 4, quoted)

> ## 4. Reading rule (every branch named before data; proposal, D5)
>
> Read on the primary rule unless a row says otherwise. The rows are tested **in order**, and the
> first that holds is the verdict. U is the remainder, so the four branches are exhaustive and
> exclusive.
>
> **R/W agreement on both D1 candidates (proposal, marked for review; D1; Johnny).** The R and W rows
> are evaluated twice: reading A with rule #2.1 as the primary, and reading B with BF_1 as the
> primary (the other D1 reading, §2.1). In both readings the W row ranges over BF_1 to BF_4, so in
> reading B it effectively asks for BF_2 to BF_4. **R stands only if both readings give R, and W
> stands only if both give W.** If either reading gives R or W and the other does not give the same
> letter, the label is **U**, and the report names both readings. If neither reading gives R or W,
> the G and U rows are read on rule #2.1.
>
> *Why this option and not a margin over a fit cost.* Johnny offered two ways to keep W from
> being read when the passing BF_r and the failing primary differ by no more than fitting noise.
> (a) W is read only if the passing BF_r's margin over the primary exceeds a fit cost, such as
> the spread of the primary's AUC across folds or seeds. (b) R/W is printed on both D1 candidates,
> and they must agree. This draft picks (b), for three reasons. First, it adds no new estimated
> quantity and no new cut. Second, both objects are already fitted in every run, so it costs
> nothing. Third, the harness defines no fit cost that suits a single held-out block: there is one
> block, so there are no folds to spread over, and rule #2.1 is deterministic given the bank (§3.3).
> The spread over its 10 ALS starts would likely be near zero for a rank-1 fit that converges to one
> optimum, which would make (a) vacuous. What (b) does not do: it does not require a margin, so a
> BF_r that passes by a hair over a primary that fails by a hair still reads W when BF_1 fails too.
> Reviewers may prefer (a) with a quantity they name.
>
> | branch | condition | reading |
> |---|---|---|
> | **R: regrows** | the primary passes leg S (`n_ge = 0` of the `99 − n_deg` shuffles with an AUC, §3.2) **and** leg P (`p_P <= 0.01`), **on both D1 candidates** | The rule, trained without the block, orders the block's cells better than it does in all 99 degree-preserving shuffles and better than 99 % of label permutations. It generates structure that it was not shown and that degrees do not carry, **on flyvis's averaged template**. |
> | **W: rule weaker than the information available** | not R, and **some BF_r** (r = 1..4) passes leg S (`n_ge = 0`) and leg P at `p_P <= 0.0125` (0.05/4), **on both D1 candidates** | The bank outside the block implies the block for a learnable, name-free predictor, and the registered rule does not express it. That is a defect of the rule, not an absence of grammar. The rank that passed is named. |
> | **G: not detected at the R level above γ_R** | not R, not W; the primary **and every BF_r** have `p_P > 0.10`; and the primary's **`ceiling_block` >= 0.90** (the condition is revision 2's, unchanged; the cut is the gate cut, `GATE_CUT`, since revision 3.2) | **Revision 3.1 (Ark 09:32, Johnny 09:33, Zcode 09:34 UTC): "not detected at the R level above γ_R; leg P passes from γ\*_P".** The block carries no structure that this family regrows at the R level at a strength at or above γ_R, where a majority of the synthetic worlds read R. Leg P alone (of rule #2.1) already sees a majority from γ\*_P, and every predictor does from the family limit (§3.6). Revision 3's "not detected above γ\*" named leg P only. The label always prints **all three limits** with their brackets, **the per-γ fractions seen/n and R/n**, the transition band, and the instrument they come from: `BF_LAMBDAS` [1, 3, 10, 30, 100], ties within 1e-9 to the larger λ, `STARTS` = 10. The rule can express the block (`ceiling_block`), and by Johnny's count the information is there (64/64 inferable). **Not** "no grammar found" and **not** "no grammar exists": the instrument has no right to either claim (Ark 08:24, Johnny 08:27 UTC). A G reached through a selected λ = 100 reads "weaker than the detection limit", not "absent" (Zcode 08:22 UTC), and since revision 3.1 it can be read from the verdict line (below). The mechanism, "orthogonal" if the primary's `ceiling_full < 0.90` and "no information" otherwise, is printed beside the label as **a description only** (§2.4, decision (c)). **Revision 3.2 (A5):** the label names its gate variable ("gate: rule #2.1's ceiling_block = … >= 0.90"), and the mechanism description names whose `ceiling_full` it quotes ("rule #2.1's ceiling_full = …"); its cut, `MECHANISM_CUT` = 0.90, is borrowed from the gate and not calibrated (§2.4). A low `ceiling_full` with the gate passed gives G ("orthogonal"), not U. |
> | **U: on the detection threshold; cannot be separated** (revisions 2 and 3: "too noisy to decide"; renamed by the U rule of §3.6 if no dense-grid world reads U: **"insufficient evidence (uncalibrated)"**, never read as a finding) | anything else (the condition is unchanged) | The legs disagree; or the regrowth sits between `p_P` 0.01 and 0.10; or `ceiling_block` is below 0.90, which means that the rule cannot hold the block even when trained on it alone (by §2.4 this is a failure of the fit, since the block is rank 1), so its failure to regrow says nothing; or the two D1 candidates disagree on R/W. The report states which of these applied. **Revision 3.1 (Ark 09:32 UTC; Zcode agreeing; Johnny recording his falsifier as his own error): U is the signature of the threshold, not an independent state.** In the synthetic worlds it appears only in the transition band [γ\*_P, γ_R), between "not seen" and "seen at the R level" (§3.6). A U on the real block is read as "on the detection threshold; cannot be separated". It is printed with the band's width in grid steps and in γ. (A U whose only reason is `ceiling_block` below 0.90 is still a failed fit, as stated above.) **Revision 3.2 (Ark, V2): U is the signature of the detection limit γ\*_P, not of the band;** all 3 pre-run U worlds sit at γ = 0.6 = γ\*_P, and the band's width is uncertain by up to two grid steps (§3.6). The label prints γ\*_P beside the band. **Revision 3.2 (V4, A2): a U whose reasons include `ceiling_block` below 0.90 is a failed fit, whatever else is listed.** Its label text is "failed fit: rule #2.1 cannot hold the block even when trained on it alone", and the U rule's rename never applies to it. Every other U keeps the threshold reading, or the U rule's name. This branch never ran in the pre-run (`ceiling_block` = 1.0 in all 225 rule #2.1 and BF rows); a test injects the reasons and checks the text (`test_knockout_regrow_labels.py`). **Revision 3.3 (A4): a `ceiling_block` that was not measured is not a failed fit.** Its reason is "rule #2.1's ceiling_block was not measured, so the G gate of section 4 cannot be read" (not "n/a is below 0.90"), its label text is "not measured: rule #2.1's ceiling_block was not measured; the G gate cannot be read", and the U rule's rename never applies to it. A failed-fit reason, when also present, takes precedence. **Revision 3.3 (A3):** only a threshold U enters the U rule (§3.6). |
>
> **The verdict line** prints: the label (G with γ_R, γ\*_P and the family limit, their brackets,
> the per-γ fractions seen/n and R/n, the transition band and the instrument; U under the name the U
> rule gives it, with γ\*_P and the band, or, when its reasons include `ceiling_block` below the
> gate, as a failed fit (revision 3.2), or, when `ceiling_block` was not measured, as "not
> measured" (revision 3.3)); for G, the mechanism, marked "description only"; the primary's
> `AUC`, `p_S` (with `n_ge` of `99 − n_deg`) and `p_P`; **both ceilings, `ceiling_full` and
> `ceiling_block`**; the R/W reading on each D1 candidate; **the λ selected by each knockout fit**
> (rule #2.1 and BF_1–BF_4, each chosen by its nested inner folds; revision 3.1); and, if
> `n_deg > 5`, the sentence "`n_deg` of 99 shuffles have no AUC on the block and are excluded from
> leg S, which counts against `99 − n_deg` shuffles (smallest `p_S` …)" (§3.2). If the No
> contingency of §3.6 was triggered, the verdict line quotes it. **The fixed λ = 1 diagnostic is not
> on the verdict line** (§3.5, Johnny's condition). It is printed in the report beside the limits.
> **Revision 3.3 (A7):** a real-arm run made with `--allow-dirty` ends its verdict line with "NOT
> THE REGISTERED RUN: made with --allow-dirty; this verdict cannot be cited as the registered
> result (sections 3.3, 7)." (§3.3).
>
> **λ on the verdict line (revision 3.1; Zcode's request of 08:22 UTC, addition 1 (i); Ark 09:32
> and Zcode 09:34 UTC vote yes).** The selected λ is already in each fit: `bf_lambda` for BF_r,
> and the λ of rule #2.1's final fit for the primary. The verdict line prints it for all five
> predictors. **If the label is G and any of them selected λ = 100**, the line adds: "G reached
> through λ = 100 on …: there the interaction is shrunk to N1's additive prediction, so this G reads
> 'weaker than the detection limit', not 'absent'". So a G reached through λ = 100 can be read
> from the verdict line alone. The λ values decide nothing. The label is set by §4's conditions
> only.
>
> **Why these cuts.** `p_S = 0.01` is the smallest a 99-shuffle leg can give, and it is the P3
> standard. `p_P <= 0.01` puts the permutation leg on the same footing. The W level uses the FlyWire
> registration's family correction. G asks for a *clear* failure, `p_P > 0.10`, of every predictor,
> so that a near miss is read as U and not as G. The cut of 0.90 on `ceiling_block` means that the
> rule, trained on the block alone, misorders at most one pair in ten. Below that, a regrowth failure
> could be a failure to fit, so it is not read as G (D5). The same 0.90 on `ceiling_full` names the
> mechanism of G as a description and decides nothing (revision 3). Since revision 3.2 the two are
> separate named constants, the gate cut (`GATE_CUT`) and the mechanism cut (`MECHANISM_CUT`),
> both 0.90; the mechanism cut is borrowed, not calibrated (§2.4). **What "too noisy" means on flyvis-65.** The template has no columns
> (the column test, §8: flyvis 1.2.0 ships only the merged, averaged estimate). So the noise of this
> test is the resolution of a 64-cell AUC, together with the rule's capacity, not within-fly
> variation. The 34/27 is printed apart (§2.4).
>
> **What decides.** The label. `AUC`, `p_S`, `p_P`, the two ceilings (beyond their roles above),
> the mechanism description of G, the three limits, the per-γ fractions, the transition band, the
> selected λ values, the regrown shares, every BF_r row,
> the N1 row, the mirrors, the row-and-column `p_P`, the permuted-block ceilings, the per-type rows
> and the fixed λ = 1 diagnostic are printed beside it (lesson f: registered rows verbatim, under
> their names) and decide nothing.

