# Knock out and regrow: block B on flyvis-65

Registration `docs/plans/2026-09-25-knockout-regrow-block-b-registration.md`, revision 1.7.3 (a delta on `docs/plans/2026-09-24-knockout-regrow-registration.md`, pinned by its LF sha256 fc41505690365ff6d82fa618b00b482cc992bb36d708ed3b6fbbe6f54f96dbec). git_head=7a10d88ec95e65b809e629b3398ceaa193e6a2f8, runtime=8216s.

Block B is the second block tested on this bank, chosen after block A's verdict G; each block is read on its own, block A's G stands, and the cuts are not corrected for two blocks (B section 5, D11). Block B runs on the same averaged template as block A, so its label is no evidence for or against averaging (B section 0).

Code (S37): pre-run made by head 5f9cc51, script 2bb92b43 (LF sha256 2bb92b433565de50aea4db5e4235a3a964b0fa776a5e957c470af63fb27abe69); this run by head 7a10d88, script e650e47e (LF sha256 e650e47e5f6660500eca10fcb08f48ad68f41a25838892d3148fcc4616bb887b); different code by design (D10 (i): the revision after the pre-run wrote PRERUN_* into the reading script); the reference is checked by its pins and the column gate.

Earlier real-arm runs of this arm (S27): root read: C:\Users\mikha\Documents\dpc-research\connectome-seed-data\knockout_regrow, folders `flyvis65_blockB_*`; 0 found.

**Verdict: U: failed fit: rule #2.1 cannot hold the block even when trained on it alone. rule #2.1: AUC = 0.5063 (19/21), p_S = 0.69 (n_ge = 68 of 99, n_deg = 0), p_P = 0.4795; ceiling_full = 0.6316, ceiling_block = 0.7744; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 3, BF_4 3.**

The section 4 row of A, verbatim:

> | **U: on the detection threshold; cannot be separated** (revisions 2 and 3: "too noisy to decide"; renamed by the U rule of §3.6 if no dense-grid world reads U: **"insufficient evidence (uncalibrated)"**, never read as a finding) | anything else (the condition is unchanged) | The legs disagree; or the regrowth sits between `p_P` 0.01 and 0.10; or `ceiling_block` is below 0.90, which means that the rule cannot hold the block even when trained on it alone (by §2.4 this is a failure of the fit, since the block is rank 1), so its failure to regrow says nothing; or the two D1 candidates disagree on R/W. The report states which of these applied. **Revision 3.1 (Ark 09:32 UTC; Zcode agreeing; Johnny recording his falsifier as his own error): U is the signature of the threshold, not an independent state.** In the synthetic worlds it appears only in the transition band [γ\*_P, γ_R), between "not seen" and "seen at the R level" (§3.6). A U on the real block is read as "on the detection threshold; cannot be separated". It is printed with the band's width in grid steps and in γ. (A U whose only reason is `ceiling_block` below 0.90 is still a failed fit, as stated above.) **Revision 3.2 (Ark, V2): U is the signature of the detection limit γ\*_P, not of the band;** all 3 pre-run U worlds sit at γ = 0.6 = γ\*_P, and the band's width is uncertain by up to two grid steps (§3.6). The label prints γ\*_P beside the band. **Revision 3.2 (V4, A2): a U whose reasons include `ceiling_block` below 0.90 is a failed fit, whatever else is listed.** Its label text is "failed fit: rule #2.1 cannot hold the block even when trained on it alone", and the U rule's rename never applies to it. Every other U keeps the threshold reading, or the U rule's name. This branch never ran in the pre-run (`ceiling_block` = 1.0 in all 225 rule #2.1 and BF rows); a test injects the reasons and checks the text (`test_knockout_regrow_labels.py`). **Revision 3.3 (A4): a `ceiling_block` that was not measured is not a failed fit.** Its reason is "rule #2.1's ceiling_block was not measured, so the G gate of section 4 cannot be read" (not "n/a is below 0.90"), its label text is "not measured: rule #2.1's ceiling_block was not measured; the G gate cannot be read", and the U rule's rename never applies to it. A failed-fit reason, when also present, takes precedence. **Revision 3.3 (A3):** only a threshold U enters the U rule (§3.6). |

Block A's literals in the quoted row: "all 3 pre-run U worlds sit at γ = 0.6 = γ*_P" are block A's pre-run worlds; block B's worlds: 4 threshold U on the dense grid, gamma*_P = 0.75 (the U-rule paragraph); "the block is rank 1" is block A's board (A section 2.4); block B's real block is not known to be rank 1 (B section 2.4).

The failed fit is on block B read as: a failed fit or a rank limit, not separated (the real block is not known to be rank 1; B section 4, D9).

Beside this U: on block B, N1's additive score can order part of the block (B section 0), so the additive (degree) channel is a second possible source of this U: a rule that follows it can pass leg P and fail leg S (B section 4, D8).

N1's own p_P beside this U (decides nothing; B section 3.5): 0.4086

within-fly variation, not a cut: one FlyWire column differs from FlyWire-30 by a median of 34 extra and 27 missing pairs out of 900 cells (61 differing cells; about 2.7 of 40 cells if spread evenly; X_c = 0.54 shows it is not) (B section 2.4).

## Section 3.5 (flyvis-65, the real block B)

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5063 (19/21) | 0.006 | 0.8424 | -0.0615 | 0.474 | 0.6316 | 0.7744 | 0.05 | 0.02 | 68 / 99 | 0.69 | 0.4795 | 0.7088 | 1.0 / 1.0 / 100.0 |
| BF_1 | 0.5238 (19/21) | 0.077 | 0.8193 | -0.0384 | 0.474 | 0.6266 | 0.9649 | 0.19 | 0.05 | 1 / 99 | 0.02 | 0.4040 | 0.8546 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.5589 (19/21) | 0.077 | 0.8512 | -0.0703 | 0.526 | 0.6566 | 1.0000 | 0.38 | 0.12 | 0 / 99 | 0.01 | 0.2704 | 0.4216 | 1.0 / 3.0 / 1.0 |
| BF_3 | 0.5589 (19/21) | 0.156 | 0.7985 | -0.0176 | 0.526 | 0.7519 | 1.0000 | 0.23 | 0.12 | 0 / 99 | 0.01 | 0.2698 | 0.3969 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.5664 (19/21) | 0.144 | 0.8294 | -0.0485 | 0.526 | 0.7970 | 1.0000 | 0.22 | 0.13 | 0 / 99 | 0.01 | 0.2442 | 0.4765 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5226 (19/21) | 0.127 | 0.7809 | +0.0000 | 0.474 | 0.6353 | 0.7882 | 0.17 | 0.08 | 99 / 99 | 1.00 | 0.4086 | 0.4836 | None / None / None |

**Six strata, mean p_exist (B section 3.1):**

| predictor | L1 x ON | L1 x OFF | L2 x ON | L2 x OFF | L3-L5 x ON | L3-L5 x OFF |
|---|---|---|---|---|---|---|
| rule #2.1 | 0.121 | 0.126 | 0.208 | 0.264 | 0.320 | 0.353 |
| BF_1 | 0.131 | 0.117 | 0.260 | 0.229 | 0.339 | 0.308 |
| BF_2 | 0.132 | 0.116 | 0.264 | 0.229 | 0.346 | 0.299 |
| BF_3 | 0.129 | 0.135 | 0.258 | 0.281 | 0.346 | 0.328 |
| BF_4 | 0.121 | 0.119 | 0.235 | 0.227 | 0.328 | 0.272 |
| N1 | 0.136 | 0.123 | 0.278 | 0.257 | 0.353 | 0.331 |

**The 9 mirror partners, p_exist (B section 1.4)** and **AUC on the other 31 cells (not mirror partners):**

| predictor | L1->Mi1 | L1->Tm3 | L2->Mi4 | L2->Tm1 | L2->Tm2 | L3->Mi9 | L5->Mi1 | L5->Tm1 | L5->Tm2 | AUC on the other 31 cells (not mirror partners) |
|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.151 | 0.076 | 0.166 | 0.369 | 0.150 | 0.416 | 0.445 | 0.475 | 0.274 | 0.5570 |
| BF_1 | 0.153 | 0.077 | 0.253 | 0.290 | 0.165 | 0.392 | 0.431 | 0.385 | 0.263 | 0.5702 |
| BF_2 | 0.151 | 0.075 | 0.261 | 0.290 | 0.167 | 0.417 | 0.462 | 0.416 | 0.271 | 0.6009 |
| BF_3 | 0.140 | 0.084 | 0.226 | 0.342 | 0.228 | 0.389 | 0.439 | 0.445 | 0.306 | 0.6316 |
| BF_4 | 0.131 | 0.088 | 0.249 | 0.268 | 0.162 | 0.500 | 0.390 | 0.332 | 0.198 | 0.6140 |
| N1 | 0.131 | 0.087 | 0.313 | 0.293 | 0.232 | 0.385 | 0.364 | 0.387 | 0.315 | 0.5943 |

**Per-type AUC, the 13 block types (where a type's block cells hold both labels):**

| predictor | L1 | L2 | L3 | L4 | L5 | Mi1 | Tm3 | Mi4 | Mi9 | Tm1 | Tm2 | Tm4 | Tm9 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.42 | 0.67 | 0.50 | 0.44 | 0.33 | 0.00 | 0.67 | 0.50 | 0.67 | 0.50 | 0.33 | 0.50 | 0.67 |
| BF_1 | 0.42 | 0.75 | 0.44 | 0.38 | 0.53 | 0.00 | 0.67 | 0.50 | 0.67 | 0.25 | 0.33 | 0.33 | 0.83 |
| BF_2 | 0.42 | 0.75 | 0.44 | 0.38 | 0.47 | 0.00 | 0.33 | 0.50 | 0.67 | 0.50 | 0.33 | 0.67 | 1.00 |
| BF_3 | 0.33 | 0.67 | 0.62 | 0.50 | 0.33 | 0.00 | 0.33 | 0.50 | 0.50 | 0.50 | 0.83 | 0.83 | 0.67 |
| BF_4 | 0.25 | 0.58 | 0.56 | 0.25 | 0.87 | 0.00 | 0.17 | 0.50 | 0.67 | 0.50 | 0.33 | 0.83 | 1.00 |
| N1 | 0.25 | 0.88 | 0.47 | 0.44 | 0.47 | 0.12 | 0.42 | 0.58 | 0.58 | 0.25 | 0.58 | 0.58 | 0.75 |

**Permuted-block ceiling_full of rule #2.1 (20):** 0.763, 0.568, 0.644, 0.570, 0.619, 0.769, 0.618, 0.678, 0.658, 0.581, 0.617, 0.648, 0.697, 0.579, 0.799, 0.684, 0.748, 0.644, 0.585, 0.865 (real block 0.6316).

**Fixed lambda = 1 on the knockout view (diagnostic, decides nothing):**

| predictor | lambda | AUC | p_P | selected lambda | AUC at the selected lambda |
|---|---|---|---|---|---|
| rule #2.1 | 1 | 0.5063 | 0.4795 | 1 | 0.5063 |
| BF_1 | 1 | 0.5238 | 0.4040 | 1 | 0.5238 |
| BF_2 | 1 | 0.5589 | 0.2704 | 1 | 0.5589 |
| BF_3 | 1 | 0.5363 | 0.3501 | 3 | 0.5589 |
| BF_4 | 1 | 0.4486 | 0.7195 | 3 | 0.5664 |

**D(N1 logit), former check 5 (printed, decides nothing):** 0.126819.

**N1's own p_P beside this U (decides nothing; B section 3.5):** 0.4086.

The limits (block B's own, B section 3.6): gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10. Binomial note: with n = 5 worlds per gamma a limit has an error of about one grid step: a true detection probability of 0.2 or 0.4 gives '>= 3 of 5' with probability 0.06 or 0.32 (Johnny). Private and raw outputs: C:\Users\mikha\Documents\dpc-research\connectome-seed-data\knockout_regrow\flyvis65_blockB_20260928T143258Z_7a10d88ec95e.

## Pre-data table (section 1.4)

Endpoint table's sha256 aa0920288e6d38230c6a275c1690614120fdaf9104476264d42208ecf04f7705 (registered aa0920288e6d38230c6a275c1690614120fdaf9104476264d42208ecf04f7705).

| endpoint | kept (as in section 1.4) |
|---|---|
| L1 | [4, 14] |
| L2 | [10, 15] |
| L3 | [12, 13] |
| L4 | [14, 4] |
| L5 | [14, 11] |
| Mi1 | [13, 29] |
| Tm3 | [9, 22] |
| Mi4 | [15, 27] |
| Mi9 | [16, 25] |
| Tm1 | [14, 28] |
| Tm2 | [11, 22] |
| Tm4 | [12, 22] |
| Tm9 | [12, 13] |

Inferable block cells: 40 of 40. Mirror cells: [('Mi1', 'L1'), ('Mi1', 'L5'), ('Mi4', 'L2'), ('Mi9', 'L3'), ('Tm1', 'L2'), ('Tm1', 'L5'), ('Tm2', 'L2'), ('Tm2', 'L5'), ('Tm3', 'L1')]. Training present cells: 585 of 4185 (printed, not checked; D3).


## Two-world check (section 3.6, revision 3)

| family | seed | label | G mechanism (description only) | rule AUC | ceiling_full | ceiling_block | n_ge / n_valid | p_S | p_P | n_deg | lambda ko | code |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R | 91100 | R | - | 1.0000 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| R | 91101 | R | - | 1.0000 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| R | 91102 | R | - | 1.0000 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| R | 91103 | R | - | 1.0000 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| R | 91104 | R | - | 1.0000 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | ok |
| Nf | 91110 | G | orthogonal (rule #2.1's ceiling_full = 0.5038 < 0.90) | 0.5125 | 0.5038 | 1.0000 | 37 / 99 | 0.38 | 0.4457 | 0 | 100.0 | ok |
| Nf | 91111 | G | orthogonal (rule #2.1's ceiling_full = 0.5100 < 0.90) | 0.5062 | 0.5100 | 1.0000 | 58 / 99 | 0.59 | 0.4737 | 0 | 100.0 | ok |
| Nf | 91112 | G | orthogonal (rule #2.1's ceiling_full = 0.5250 < 0.90) | 0.5062 | 0.5250 | 1.0000 | 31 / 99 | 0.32 | 0.4796 | 0 | 100.0 | ok |
| Nf | 91113 | G | no information (rule #2.1's ceiling_full = 1.0000 >= 0.90) | 0.4988 | 1.0000 | 1.0000 | 41 / 99 | 0.42 | 0.5041 | 0 | 100.0 | ok |
| Nf | 91114 | G | orthogonal (rule #2.1's ceiling_full = 0.5500 < 0.90) | 0.5350 | 0.5500 | 1.0000 | 65 / 99 | 0.66 | 0.3594 | 0 | 100.0 | ok |
| No | 91120 | G | orthogonal (rule #2.1's ceiling_full = 0.4825 < 0.90) | 0.4850 | 0.4825 | 1.0000 | 66 / 99 | 0.67 | 0.5673 | 0 | 1.0 | ok |
| No | 91121 | G | orthogonal (rule #2.1's ceiling_full = 0.5000 < 0.90) | 0.5050 | 0.5000 | 1.0000 | 22 / 99 | 0.23 | 0.4836 | 0 | 1.0 | ok |
| No | 91122 | G | orthogonal (rule #2.1's ceiling_full = 0.5050 < 0.90) | 0.4725 | 0.5050 | 1.0000 | 86 / 99 | 0.87 | 0.6139 | 0 | 1.0 | ok |
| No | 91123 | G | orthogonal (rule #2.1's ceiling_full = 0.4838 < 0.90) | 0.4525 | 0.4838 | 1.0000 | 74 / 99 | 0.75 | 0.6926 | 0 | 1.0 | ok |
| No | 91124 | G | orthogonal (rule #2.1's ceiling_full = 0.5162 < 0.90) | 0.5100 | 0.5162 | 1.0000 | 4 / 99 | 0.05 | 0.4599 | 0 | 1.0 | ok |
| W | 91130 | W | - | 0.4888 | 0.5038 | 1.0000 | 93 / 99 | 0.94 | 0.5461 | 0 | 1.0 | ok |
| W | 91131 | W | - | 0.5150 | 0.5025 | 1.0000 | 19 / 99 | 0.20 | 0.4418 | 0 | 1.0 | ok |
| W | 91132 | W | - | 0.4925 | 0.5088 | 1.0000 | 94 / 99 | 0.95 | 0.5377 | 0 | 1.0 | ok |
| W | 91133 | W | - | 0.5450 | 0.5525 | 1.0000 | 7 / 99 | 0.08 | 0.3205 | 0 | 1.0 | ok |
| W | 91134 | W | - | 0.5425 | 0.5600 | 1.0000 | 0 / 99 | 0.01 | 0.3297 | 0 | 1.0 | ok |
| M0.5 | 91140 | U | - | 0.6300 | 0.9375 | 1.0000 | 0 / 99 | 0.01 | 0.0867 | 0 | 3.0 | curve |
| M0.5 | 91141 | U | - | 0.6212 | 0.9800 | 1.0000 | 0 / 99 | 0.01 | 0.0963 | 0 | 3.0 | curve |
| M0.5 | 91142 | G | no information (rule #2.1's ceiling_full = 0.9900 >= 0.90) | 0.4875 | 0.9900 | 1.0000 | 31 / 99 | 0.32 | 0.5522 | 0 | 100.0 | curve |
| M0.5 | 91143 | R | - | 0.7675 | 0.9925 | 1.0000 | 0 / 99 | 0.01 | 0.0015 | 0 | 3.0 | curve |
| M0.5 | 91144 | G | no information (rule #2.1's ceiling_full = 0.9975 >= 0.90) | 0.5112 | 0.9975 | 1.0000 | 47 / 99 | 0.48 | 0.4644 | 0 | 100.0 | curve |
| M0.6 | 91160 | W | - | 0.6800 | 0.9450 | 1.0000 | 0 / 99 | 0.01 | 0.0269 | 0 | 3.0 | curve |
| M0.6 | 91161 | U | - | 0.5837 | 0.9200 | 1.0000 | 1 / 99 | 0.02 | 0.1894 | 0 | 3.0 | curve |
| M0.6 | 91162 | U | - | 0.6450 | 0.9425 | 1.0000 | 0 / 99 | 0.01 | 0.0598 | 0 | 3.0 | curve |
| M0.6 | 91163 | R | - | 0.7325 | 0.9950 | 1.0000 | 0 / 99 | 0.01 | 0.0066 | 0 | 3.0 | curve |
| M0.6 | 91164 | G | orthogonal (rule #2.1's ceiling_full = 0.8575 < 0.90) | 0.5125 | 0.8575 | 1.0000 | 13 / 99 | 0.14 | 0.4453 | 0 | 3.0 | curve |
| M0.75 | 91170 | R | - | 0.8163 | 0.9850 | 1.0000 | 0 / 99 | 0.01 | 0.0006 | 0 | 3.0 | curve |
| M0.75 | 91171 | R | - | 0.9575 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 3.0 | curve |
| M0.75 | 91172 | R | - | 0.8925 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 3.0 | curve |
| M0.75 | 91173 | R | - | 0.7725 | 0.9925 | 1.0000 | 0 / 99 | 0.01 | 0.0007 | 0 | 3.0 | curve |
| M0.75 | 91174 | G | no information (rule #2.1's ceiling_full = 0.9875 >= 0.90) | 0.6188 | 0.9875 | 1.0000 | 1 / 99 | 0.02 | 0.1032 | 0 | 3.0 | curve |
| M0.85 | 91180 | R | - | 0.8375 | 0.9700 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 3.0 | curve |
| M0.85 | 91181 | R | - | 0.8300 | 0.9925 | 1.0000 | 0 / 99 | 0.01 | 0.0002 | 0 | 3.0 | curve |
| M0.85 | 91182 | R | - | 0.9575 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |
| M0.85 | 91183 | R | - | 0.8800 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 3.0 | curve |
| M0.85 | 91184 | R | - | 0.8625 | 0.9950 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 3.0 | curve |
| M1.0 | 91150 | R | - | 0.7675 | 0.9525 | 1.0000 | 0 / 99 | 0.01 | 0.0014 | 0 | 1.0 | curve |
| M1.0 | 91151 | R | - | 0.9475 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |
| M1.0 | 91152 | R | - | 0.9775 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |
| M1.0 | 91153 | R | - | 0.9525 | 0.9975 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |
| M1.0 | 91154 | R | - | 0.9975 | 1.0000 | 1.0000 | 0 / 99 | 0.01 | 0.0001 | 0 | 1.0 | curve |

| family | requirement | labels read (R/W/G/U) | meet (min) | stop labels | result |
|---|---|---|---|---|---|
| R | each of 5 worlds reads R, on both D1 candidates | 5/0/0/0 | 5/5 (5) | 0 | no stop |
| Nf | never R or W (stop); at least 3 of 5 read G | 0/0/5/0 | 5/5 (3) | 0 | no stop |
| No | never R or W (stop); reads G; a U triggers the No contingency | 0/0/5/0 | 5/5 (0) | 0 | no stop |
| W | each of 5 worlds reads W, on both D1 candidates | 0/5/0/0 | 5/5 (5) | 0 | no stop |
| M0.5 | power curve: printed, no stop row; the three limits are taken from it | 1/0/2/2 | n/a (power curve) | 0 | no stop |
| M0.6 | power curve: printed, no stop row; the three limits are taken from it | 1/1/1/2 | n/a (power curve) | 0 | no stop |
| M0.75 | power curve: printed, no stop row; the three limits are taken from it | 4/0/1/0 | n/a (power curve) | 0 | no stop |
| M0.85 | power curve: printed, no stop row; the three limits are taken from it | 5/0/0/0 | n/a (power curve) | 0 | no stop |
| M1.0 | power curve: printed, no stop row; the three limits are taken from it | 5/0/0/0 | n/a (power curve) | 0 | no stop |

Pre-run table (section 7, revisions 3.2, 3.3): outcome 1: every deciding column equal; byte-identical (recorded, not gated); rows matched by family/j/seed/predictor: 0 missing now, 0 missing in the pre-run table, row order equal (a fact, not an outcome); mechanism_description differs on 0 rows (reported, not gated) (passed: True; byte-identical: True; pinned 2187ce8983a840417f68aafe4f2678f139d77aecbc5a349cb1aa97a9b8740dcb, recomputed 2187ce8983a840417f68aafe4f2678f139d77aecbc5a349cb1aa97a9b8740dcb).

Per-fit diagnostic against the pre-run raw fits (diagnostic, decides nothing): {'pinned': 28665, 'missing_now': 0, 'compared': 28665, 'fitted_this_pass': 28665, 'p_differ': 0, 'lambda_differ': 0, 'labels_differ': 0, 'score_differ': 0, 'outside_density_differ': 0, 'reused_from_ko_differ': 0, 'max_abs_dp': 0.0}.

Two-world check passed: True. No contingency triggered: False.

## Power curve and the three limits (section 3.6, revision 3.1)

| gamma | family | seen/n (rule #2.1 p_P <= 0.01) | R/n | seen/n BF_1, BF_2, BF_3, BF_4 | R/W/G/U | rule AUC | rule lambda ko |
|---|---|---|---|---|---|---|---|
| 0.0 | Nf (anchor) | 0/5 | 0/5 | 0/5, 0/5, 0/5, 0/5 | 0/0/5/0 | 0.512, 0.506, 0.506, 0.499, 0.535 | 100, 100, 100, 100, 100 |
| 0.5 | M0.5 | 1/5 | 1/5 | 1/5, 0/5, 0/5, 0/5 | 1/0/2/2 | 0.630, 0.621, 0.487, 0.767, 0.511 | 3, 3, 100, 3, 100 |
| 0.6 | M0.6 | 1/5 | 1/5 | 1/5, 0/5, 0/5, 1/5 | 1/1/1/2 | 0.680, 0.584, 0.645, 0.733, 0.512 | 3, 3, 3, 3, 3 |
| 0.75 | M0.75 | 4/5 | 4/5 | 4/5, 4/5, 4/5, 4/5 | 4/0/1/0 | 0.816, 0.958, 0.892, 0.772, 0.619 | 3, 3, 3, 3, 3 |
| 0.85 | M0.85 | 5/5 | 5/5 | 5/5, 5/5, 5/5, 5/5 | 5/0/0/0 | 0.838, 0.830, 0.958, 0.880, 0.863 | 3, 3, 1, 3, 3 |
| 1.0 | M1.0 | 5/5 | 5/5 | 5/5, 5/5, 5/5, 5/5 | 5/0/0/0 | 0.767, 0.948, 0.978, 0.953, 0.998 | 1, 1, 1, 1, 1 |
| 2.0 | R (anchor) | 5/5 | 5/5 | 5/5, 5/5, 5/5, 5/5 | 5/0/0/0 | 1.000, 1.000, 1.000, 1.000, 1.000 | 1, 1, 1, 1, 1 |

**The three limits** (in M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10):

- gamma*_P, the leg-P limit (rule #2.1 p_P <= 0.01 in a majority of the worlds): **0.75**, bracket (0.6, 0.75]; majority seen at every grid gamma above it: True.
- gamma_R (a majority of the worlds read R): **0.75**, bracket (0.6, 0.75]; majority R at every grid gamma above it: True.
- family limit (the largest leg-P limit: the maximum of each predictor's own leg-P limit): **0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4)**. Per predictor: rule #2.1 0.75, BF_1 0.75, BF_2 0.75, BF_3 0.75, BF_4 0.75. The limits use p_P <= 0.01 for every predictor and are not family-corrected, unlike the W gate (p_P <= 0.0125 = 0.05/4): a limit is a property of the instrument, not of a branch (revision 3.2).
- transition band [gamma*_P, gamma_R): empty: the two limits coincide (0 grid steps, 0 in gamma). Dense-grid worlds that read U: 0 inside the band, 4 below it, 0 above it. The band is the difference of two limits, each uncertain by about one grid step, so a one-step band is one of 0, 1 or 2 steps (revision 3.2).
- per gamma, seen/n and R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5.
- binomial note: with n = 5 worlds per gamma a limit has an error of about one grid step: a true detection probability of 0.2 or 0.4 gives '>= 3 of 5' with probability 0.06 or 0.32 (Johnny).
- M worlds that read G at or above gamma*_P: 1 (M0.75 91174); at or above gamma_R: 1 (M0.75 91174) (printed, no stop).
- grid complete: True.

**U rule (block B's own U reading, B section 3.6; S32):** threshold U read by 4 of 25 dense-grid worlds (4 threshold U, 0 failed fit, 0 ceiling_block not measured, 0 not readable): U stays; its frequency is printed. Block B's threshold U worlds on the dense grid: 4 of 25 (by gamma: 0.5: 2, 0.6: 2); against block B's own gamma*_P = 0.75: 0 at it, 4 below it, 0 above it; they do not all lie at gamma*_P. Block A's reading of a threshold U as the signature of its leg-P limit is block A's and is not carried to block B beyond these positions. A U whose reasons include rule #2.1's ceiling_block below 0.90 reads 'failed fit: rule #2.1 cannot hold the block even when trained on it alone', and a U whose ceiling_block was not measured reads 'not measured: rule #2.1's ceiling_block was not measured; the G gate cannot be read'; neither is renamed. U across all 45 worlds: 4 (R 0 of 5, Nf 0 of 5, No 0 of 5, W 0 of 5, M0.5 2 of 5, M1.0 0 of 5, M0.6 2 of 5, M0.75 0 of 5, M0.85 0 of 5).

Not-readable U (S38; counted apart, never a threshold U): 0 of 25 dense-grid worlds; the real block: 0 of 1 (readable).

## Fixed lambda = 1 on the knockout view (section 3.5): diagnostic, decides nothing

Printed beside the limits, not on any verdict line. Where the selected lambda was 1 the selected fit is reused (path check: {'bank': None, 'passed': None, 'note': 'no bank selected lambda = 1 on all five'}).

| family | predictor | AUC at lambda 1 (per world) | mean | p_P <= 0.01 at lambda 1 | selected lambda | mean AUC selected | p_P <= 0.01 selected |
|---|---|---|---|---|---|---|---|
| R | rule #2.1 | 1.000, 1.000, 1.000, 1.000, 1.000 | 1.000 | 5/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 1.000 | 5/5 |
| R | BF_1 | 1.000, 1.000, 1.000, 1.000, 1.000 | 1.000 | 5/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 1.000 | 5/5 |
| R | BF_2 | 0.998, 1.000, 1.000, 1.000, 0.993 | 0.998 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.999 | 5/5 |
| R | BF_3 | 1.000, 0.990, 0.988, 1.000, 0.988 | 0.993 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.998 | 5/5 |
| R | BF_4 | 0.973, 0.980, 0.990, 1.000, 0.988 | 0.986 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.997 | 5/5 |
| Nf | rule #2.1 | 0.560, 0.501, 0.520, 0.797, 0.432 | 0.562 | 1/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.512 | 0/5 |
| Nf | BF_1 | 0.557, 0.490, 0.507, 0.738, 0.472 | 0.553 | 1/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.510 | 0/5 |
| Nf | BF_2 | 0.623, 0.517, 0.475, 0.760, 0.415 | 0.558 | 1/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.510 | 0/5 |
| Nf | BF_3 | 0.588, 0.487, 0.460, 0.738, 0.410 | 0.536 | 1/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.510 | 0/5 |
| Nf | BF_4 | 0.552, 0.490, 0.440, 0.642, 0.440 | 0.513 | 0/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.510 | 0/5 |
| No | rule #2.1 | 0.485, 0.505, 0.472, 0.453, 0.510 | 0.485 | 0/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.485 | 0/5 |
| No | BF_1 | 0.485, 0.480, 0.487, 0.445, 0.497 | 0.479 | 0/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.479 | 0/5 |
| No | BF_2 | 0.487, 0.515, 0.482, 0.422, 0.500 | 0.481 | 0/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.482 | 0/5 |
| No | BF_3 | 0.482, 0.500, 0.487, 0.448, 0.470 | 0.478 | 0/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.480 | 0/5 |
| No | BF_4 | 0.495, 0.487, 0.507, 0.422, 0.453 | 0.473 | 0/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.485 | 0/5 |
| W | rule #2.1 | 0.489, 0.515, 0.492, 0.545, 0.542 | 0.517 | 0/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.517 | 0/5 |
| W | BF_1 | 0.492, 0.505, 0.492, 0.542, 0.545 | 0.515 | 0/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.515 | 0/5 |
| W | BF_2 | 0.718, 0.810, 0.750, 0.745, 0.762 | 0.757 | 5/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.757 | 5/5 |
| W | BF_3 | 0.698, 0.785, 0.725, 0.723, 0.715 | 0.729 | 3/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.729 | 3/5 |
| W | BF_4 | 0.690, 0.745, 0.710, 0.723, 0.682 | 0.710 | 2/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.715 | 2/5 |
| M0.5 | rule #2.1 | 0.625, 0.695, 0.526, 0.874, 0.651 | 0.674 | 1/5 | 3.0, 3.0, 100.0, 3.0, 100.0 | 0.604 | 1/5 |
| M0.5 | BF_1 | 0.640, 0.698, 0.517, 0.875, 0.630 | 0.672 | 1/5 | 3.0, 3.0, 100.0, 3.0, 100.0 | 0.598 | 1/5 |
| M0.5 | BF_2 | 0.757, 0.767, 0.578, 0.767, 0.680 | 0.710 | 3/5 | 3.0, 100.0, 100.0, 100.0, 100.0 | 0.534 | 0/5 |
| M0.5 | BF_3 | 0.735, 0.630, 0.615, 0.757, 0.675 | 0.682 | 2/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.507 | 0/5 |
| M0.5 | BF_4 | 0.718, 0.730, 0.703, 0.720, 0.745 | 0.723 | 4/5 | 100.0, 100.0, 100.0, 100.0, 100.0 | 0.507 | 0/5 |
| M1.0 | rule #2.1 | 0.767, 0.948, 0.978, 0.953, 0.998 | 0.928 | 5/5 | 1.0, 1.0, 1.0, 1.0, 1.0 | 0.928 | 5/5 |
| M1.0 | BF_1 | 0.762, 0.943, 0.973, 0.948, 0.995 | 0.924 | 5/5 | 1.0, 1.0, 3.0, 1.0, 1.0 | 0.919 | 5/5 |
| M1.0 | BF_2 | 0.728, 0.930, 0.873, 0.858, 0.948 | 0.867 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.847 | 5/5 |
| M1.0 | BF_3 | 0.792, 0.935, 0.897, 0.833, 0.932 | 0.878 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.857 | 5/5 |
| M1.0 | BF_4 | 0.807, 0.917, 0.890, 0.868, 0.912 | 0.879 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.862 | 5/5 |
| M0.6 | rule #2.1 | 0.752, 0.662, 0.735, 0.815, 0.499 | 0.693 | 3/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.631 | 1/5 |
| M0.6 | BF_1 | 0.757, 0.642, 0.708, 0.860, 0.527 | 0.699 | 2/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.641 | 1/5 |
| M0.6 | BF_2 | 0.748, 0.685, 0.695, 0.715, 0.525 | 0.673 | 1/5 | 3.0, 3.0, 3.0, 3.0, 100.0 | 0.621 | 0/5 |
| M0.6 | BF_3 | 0.775, 0.660, 0.608, 0.217, 0.505 | 0.553 | 1/5 | 3.0, 100.0, 3.0, 3.0, 100.0 | 0.552 | 0/5 |
| M0.6 | BF_4 | 0.792, 0.542, 0.598, 0.225, 0.552 | 0.542 | 1/5 | 3.0, 100.0, 3.0, 100.0, 100.0 | 0.558 | 1/5 |
| M0.75 | rule #2.1 | 0.897, 0.990, 0.970, 0.873, 0.688 | 0.884 | 4/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.811 | 4/5 |
| M0.75 | BF_1 | 0.895, 0.983, 0.960, 0.855, 0.718 | 0.882 | 4/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.805 | 4/5 |
| M0.75 | BF_2 | 0.868, 0.988, 0.823, 0.775, 0.662 | 0.823 | 4/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.799 | 4/5 |
| M0.75 | BF_3 | 0.805, 0.905, 0.802, 0.780, 0.640 | 0.787 | 4/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.781 | 4/5 |
| M0.75 | BF_4 | 0.825, 0.863, 0.762, 0.677, 0.652 | 0.756 | 3/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.765 | 4/5 |
| M0.85 | rule #2.1 | 0.900, 0.882, 0.958, 0.920, 0.935 | 0.919 | 5/5 | 3.0, 3.0, 1.0, 3.0, 3.0 | 0.873 | 5/5 |
| M0.85 | BF_1 | 0.895, 0.887, 0.955, 0.927, 0.932 | 0.919 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.856 | 5/5 |
| M0.85 | BF_2 | 0.863, 0.818, 0.915, 0.870, 0.885 | 0.870 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.831 | 5/5 |
| M0.85 | BF_3 | 0.835, 0.830, 0.910, 0.777, 0.710 | 0.812 | 4/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.805 | 5/5 |
| M0.85 | BF_4 | 0.828, 0.850, 0.873, 0.745, 0.723 | 0.803 | 5/5 | 3.0, 3.0, 3.0, 3.0, 3.0 | 0.815 | 5/5 |

Fits: 0 re-read from saved fits, 28440 new world fits, fixed lambda: 50 reused, 175 fitted.

### World R, seed 91100: R: regrows

Outside density 0.2389; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 1.0000 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 1.0000 (20/20) | 3.809 | 0.2204 | +0.5052 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 1.0000 (20/20) | 3.476 | 0.2172 | +0.5085 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.9975 (20/20) | 2.686 | 0.2796 | +0.4461 | 0.950 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 1.0000 (20/20) | 2.707 | 0.2768 | +0.4488 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.9925 (20/20) | 2.578 | 0.2958 | +0.4298 | 0.950 | 1.0000 | 1.0000 | 0.99 | 0.99 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5138 (20/20) | 0.037 | 0.7257 | +0.0000 | 0.400 | 0.5150 | 0.7200 | 0.92 | 0.06 | 99 / 99 | 1.00 | 0.4457 | 0.6970 | None / None / None |

### World R, seed 91101: R: regrows

Outside density 0.2471; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 1.0000 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 1.0000 (20/20) | 4.222 | 0.1782 | +0.5493 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 1.0000 (20/20) | 3.790 | 0.1826 | +0.5450 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 1.0000 (20/20) | 2.999 | 0.2455 | +0.4820 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.9975 (20/20) | 2.954 | 0.2508 | +0.4767 | 0.950 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 1.0000 (20/20) | 3.015 | 0.2477 | +0.4798 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5288 (20/20) | 0.043 | 0.7275 | +0.0000 | 0.500 | 0.5513 | 0.7200 | 0.56 | 0.13 | 99 / 99 | 1.00 | 0.3887 | 0.5000 | None / None / None |

### World R, seed 91102: R: regrows

Outside density 0.2468; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 1.0000 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 1.0000 (20/20) | 3.457 | 0.2516 | +0.4948 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 1.0000 (20/20) | 3.047 | 0.2557 | +0.4907 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 1.0000 (20/20) | 2.407 | 0.3220 | +0.4243 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.9975 (20/20) | 2.378 | 0.3293 | +0.4171 | 0.950 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 1.0000 (20/20) | 2.452 | 0.3206 | +0.4258 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5150 (20/20) | 0.068 | 0.7464 | +0.0000 | 0.450 | 0.5238 | 0.7200 | 0.63 | 0.07 | 99 / 99 | 1.00 | 0.4320 | 0.9471 | None / None / None |

### World R, seed 91103: R: regrows

Outside density 0.2399; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 1.0000 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 1.0000 (20/20) | 3.846 | 0.2441 | +0.5251 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 1.0000 (20/20) | 3.191 | 0.2375 | +0.5317 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 1.0000 (20/20) | 2.541 | 0.3063 | +0.4629 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 1.0000 (20/20) | 2.549 | 0.3080 | +0.4612 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 1.0000 (20/20) | 2.736 | 0.2842 | +0.4850 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5300 (20/20) | -0.010 | 0.7692 | +0.0000 | 0.550 | 0.5513 | 0.7200 | 0.59 | 0.14 | 99 / 99 | 1.00 | 0.3847 | 0.0796 | None / None / None |

### World R, seed 91104: R: regrows

Outside density 0.2399; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 1.0000 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 1.0000 (20/20) | 3.691 | 0.2517 | +0.5237 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 1.0000 (20/20) | 3.272 | 0.2358 | +0.5397 | 1.000 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.9975 (20/20) | 2.516 | 0.3147 | +0.4607 | 0.950 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.9975 (20/20) | 2.511 | 0.3123 | +0.4632 | 0.950 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.9950 (20/20) | 2.369 | 0.3310 | +0.4444 | 0.950 | 1.0000 | 1.0000 | 0.99 | 0.99 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5000 (20/20) | -0.090 | 0.7754 | +0.0000 | 0.550 | 0.4963 | 0.7200 | n/a | 0.00 | 99 / 99 | 1.00 | 0.5077 | 0.0061 | None / None / None |

### World Nf, seed 91110: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1364; block present 20 of 40.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5038 < 0.90)]. rule #2.1: AUC = 0.5125 (20/20), p_S = 0.38 (n_ge = 37 of 99, n_deg = 0), p_P = 0.4457; ceiling_full = 0.5038, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5125 (20/20) | -0.075 | 0.9165 | +0.0058 | 0.600 | 0.5038 | 1.0000 | 3.33 | 0.02 | 37 / 99 | 0.38 | 0.4457 | 0.0006 | 100.0 / 100.0 / 1.0 |
| BF_1 | 0.5050 (20/20) | -0.060 | 0.9223 | +0.0000 | 0.550 | 0.4888 | 1.0000 | n/a | 0.01 | 97 / 99 | 0.98 | 0.4800 | 0.0014 | 100.0 / 100.0 / 1.0 |
| BF_2 | 0.5050 (20/20) | -0.060 | 0.9223 | +0.0000 | 0.550 | 0.4888 | 1.0000 | n/a | 0.01 | 99 / 99 | 1.00 | 0.4800 | 0.0014 | 100.0 / 100.0 / 1.0 |
| BF_3 | 0.5050 (20/20) | -0.060 | 0.9223 | +0.0000 | 0.550 | 0.4888 | 1.0000 | n/a | 0.01 | 99 / 99 | 1.00 | 0.4800 | 0.0014 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.5050 (20/20) | -0.060 | 0.9223 | +0.0000 | 0.550 | 0.4888 | 1.0000 | n/a | 0.01 | 99 / 99 | 1.00 | 0.4800 | 0.0014 | 100.0 / 100.0 / 1.0 |
| N1 | 0.5050 (20/20) | -0.060 | 0.9223 | +0.0000 | 0.550 | 0.4888 | 0.7200 | n/a | 0.02 | 99 / 99 | 1.00 | 0.4800 | 0.0014 | None / None / None |

### World Nf, seed 91111: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1391; block present 20 of 40.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5100 < 0.90)]. rule #2.1: AUC = 0.5062 (20/20), p_S = 0.59 (n_ge = 58 of 99, n_deg = 0), p_P = 0.4737; ceiling_full = 0.5100, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5062 (20/20) | 0.003 | 0.8477 | +0.0171 | 0.550 | 0.5100 | 1.0000 | 0.62 | 0.01 | 58 / 99 | 0.59 | 0.4737 | 0.3819 | 100.0 / 100.0 / 1.0 |
| BF_1 | 0.5112 (20/20) | 0.011 | 0.8649 | +0.0000 | 0.550 | 0.5150 | 1.0000 | 0.75 | 0.02 | 96 / 99 | 0.97 | 0.4529 | 0.3775 | 100.0 / 100.0 / 1.0 |
| BF_2 | 0.5112 (20/20) | 0.011 | 0.8649 | +0.0000 | 0.550 | 0.5150 | 1.0000 | 0.75 | 0.02 | 99 / 99 | 1.00 | 0.4529 | 0.3775 | 100.0 / 100.0 / 1.0 |
| BF_3 | 0.5112 (20/20) | 0.011 | 0.8649 | +0.0000 | 0.550 | 0.5150 | 1.0000 | 0.75 | 0.02 | 99 / 99 | 1.00 | 0.4529 | 0.3775 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.5112 (20/20) | 0.011 | 0.8649 | +0.0000 | 0.550 | 0.5150 | 1.0000 | 0.75 | 0.02 | 99 / 99 | 1.00 | 0.4529 | 0.3775 | 100.0 / 100.0 / 1.0 |
| N1 | 0.5112 (20/20) | 0.011 | 0.8649 | +0.0000 | 0.550 | 0.5150 | 0.7200 | 0.75 | 0.05 | 99 / 99 | 1.00 | 0.4529 | 0.3775 | None / None / None |

### World Nf, seed 91112: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1331; block present 20 of 40.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5250 < 0.90)]. rule #2.1: AUC = 0.5062 (20/20), p_S = 0.32 (n_ge = 31 of 99, n_deg = 0), p_P = 0.4796; ceiling_full = 0.5250, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5062 (20/20) | 0.003 | 0.8626 | +0.0058 | 0.450 | 0.5250 | 1.0000 | 0.25 | 0.01 | 31 / 99 | 0.32 | 0.4796 | 0.4511 | 100.0 / 100.0 / 1.0 |
| BF_1 | 0.5012 (20/20) | -0.020 | 0.8684 | +0.0000 | 0.500 | 0.5038 | 1.0000 | 0.33 | 0.00 | 98 / 99 | 0.99 | 0.4996 | 0.3077 | 100.0 / 100.0 / 1.0 |
| BF_2 | 0.5012 (20/20) | -0.020 | 0.8684 | +0.0000 | 0.500 | 0.5038 | 1.0000 | 0.33 | 0.00 | 99 / 99 | 1.00 | 0.4996 | 0.3077 | 100.0 / 100.0 / 1.0 |
| BF_3 | 0.5012 (20/20) | -0.020 | 0.8684 | +0.0000 | 0.500 | 0.5038 | 1.0000 | 0.33 | 0.00 | 99 / 99 | 1.00 | 0.4996 | 0.3077 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.5012 (20/20) | -0.020 | 0.8684 | +0.0000 | 0.500 | 0.5038 | 1.0000 | 0.33 | 0.00 | 98 / 99 | 0.99 | 0.4996 | 0.3077 | 100.0 / 100.0 / 1.0 |
| N1 | 0.5012 (20/20) | -0.020 | 0.8684 | +0.0000 | 0.500 | 0.5038 | 0.7200 | 0.33 | 0.01 | 99 / 99 | 1.00 | 0.4996 | 0.3077 | None / None / None |

### World Nf, seed 91113: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1443; block present 20 of 40.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 1.0000 >= 0.90)]. rule #2.1: AUC = 0.4988 (20/20), p_S = 0.42 (n_ge = 41 of 99, n_deg = 0), p_P = 0.5041; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4988 (20/20) | -0.032 | 0.8220 | -0.0040 | 0.550 | 1.0000 | 1.0000 | -0.00 | -0.00 | 41 / 99 | 0.42 | 0.5041 | 0.1311 | 100.0 / 3.0 / 1.0 |
| BF_1 | 0.4925 (20/20) | -0.016 | 0.8179 | +0.0000 | 0.500 | 1.0000 | 1.0000 | -0.02 | -0.02 | 94 / 99 | 0.95 | 0.5302 | 0.5092 | 100.0 / 3.0 / 1.0 |
| BF_2 | 0.4925 (20/20) | -0.016 | 0.8179 | +0.0000 | 0.500 | 0.4988 | 1.0000 | n/a | -0.02 | 98 / 99 | 0.99 | 0.5302 | 0.5092 | 100.0 / 100.0 / 1.0 |
| BF_3 | 0.4925 (20/20) | -0.016 | 0.8179 | +0.0000 | 0.500 | 0.4988 | 1.0000 | n/a | -0.02 | 98 / 99 | 0.99 | 0.5302 | 0.5092 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.4925 (20/20) | -0.016 | 0.8179 | +0.0000 | 0.500 | 0.4988 | 1.0000 | n/a | -0.02 | 99 / 99 | 1.00 | 0.5302 | 0.5092 | 100.0 / 100.0 / 1.0 |
| N1 | 0.4925 (20/20) | -0.016 | 0.8179 | +0.0000 | 0.500 | 0.4988 | 0.7200 | n/a | -0.03 | 99 / 99 | 1.00 | 0.5302 | 0.5092 | None / None / None |

### World Nf, seed 91114: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1302; block present 20 of 40.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5500 < 0.90)]. rule #2.1: AUC = 0.5350 (20/20), p_S = 0.66 (n_ge = 65 of 99, n_deg = 0), p_P = 0.3594; ceiling_full = 0.5500, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5350 (20/20) | 0.047 | 0.8520 | +0.0077 | 0.550 | 0.5500 | 1.0000 | 0.70 | 0.07 | 65 / 99 | 0.66 | 0.3594 | 0.1688 | 100.0 / 100.0 / 1.0 |
| BF_1 | 0.5400 (20/20) | 0.071 | 0.8598 | +0.0000 | 0.550 | 0.5675 | 1.0000 | 0.59 | 0.08 | 94 / 99 | 0.95 | 0.3419 | 0.1920 | 100.0 / 100.0 / 1.0 |
| BF_2 | 0.5400 (20/20) | 0.071 | 0.8598 | +0.0000 | 0.550 | 0.5675 | 1.0000 | 0.59 | 0.08 | 99 / 99 | 1.00 | 0.3419 | 0.1920 | 100.0 / 100.0 / 1.0 |
| BF_3 | 0.5400 (20/20) | 0.071 | 0.8598 | +0.0000 | 0.550 | 0.5675 | 1.0000 | 0.59 | 0.08 | 99 / 99 | 1.00 | 0.3419 | 0.1920 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.5400 (20/20) | 0.071 | 0.8598 | +0.0000 | 0.550 | 0.5675 | 1.0000 | 0.59 | 0.08 | 99 / 99 | 1.00 | 0.3419 | 0.1920 | 100.0 / 100.0 / 1.0 |
| N1 | 0.5400 (20/20) | 0.071 | 0.8598 | +0.0000 | 0.550 | 0.5675 | 0.7200 | 0.59 | 0.18 | 99 / 99 | 1.00 | 0.3419 | 0.1920 | None / None / None |

### World No, seed 91120: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.2413; block present 20 of 40.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.4825 < 0.90)]. rule #2.1: AUC = 0.4850 (20/20), p_S = 0.67 (n_ge = 66 of 99, n_deg = 0), p_P = 0.5673; ceiling_full = 0.4825, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4850 (20/20) | -0.076 | 1.1076 | -0.3407 | 0.500 | 0.4825 | 1.0000 | n/a | -0.03 | 66 / 99 | 0.67 | 0.5673 | 0.5040 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.4850 (20/20) | -0.076 | 1.0265 | -0.2596 | 0.500 | 0.4825 | 1.0000 | n/a | -0.03 | 98 / 99 | 0.99 | 0.5668 | 0.5047 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.5000 (20/20) | -0.025 | 0.9317 | -0.1648 | 0.500 | 0.7800 | 1.0000 | 0.00 | 0.00 | 0 / 99 | 0.01 | 0.5045 | 0.4084 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.4975 (20/20) | -0.003 | 0.9228 | -0.1558 | 0.500 | 0.8225 | 1.0000 | -0.01 | -0.01 | 0 / 99 | 0.01 | 0.5144 | 0.4643 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.4900 (20/20) | -0.027 | 0.9286 | -0.1616 | 0.500 | 0.8375 | 1.0000 | -0.03 | -0.02 | 99 / 99 | 1.00 | 0.5455 | 0.5157 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4900 (20/20) | -0.059 | 0.7669 | +0.0000 | 0.500 | 0.4938 | 0.6000 | n/a | -0.10 | 99 / 99 | 1.00 | 0.5419 | 0.0152 | None / None / None |

### World No, seed 91121: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.2478; block present 20 of 40.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5000 < 0.90)]. rule #2.1: AUC = 0.5050 (20/20), p_S = 0.23 (n_ge = 22 of 99, n_deg = 0), p_P = 0.4836; ceiling_full = 0.5000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5050 (20/20) | -0.069 | 1.1546 | -0.4135 | 0.500 | 0.5000 | 1.0000 | n/a | 0.01 | 22 / 99 | 0.23 | 0.4836 | 0.4617 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.4800 (20/20) | -0.065 | 1.0264 | -0.2853 | 0.500 | 0.4975 | 1.0000 | n/a | -0.04 | 98 / 99 | 0.99 | 0.5856 | 0.5813 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.4975 (20/20) | -0.077 | 0.9277 | -0.1866 | 0.500 | 0.5125 | 1.0000 | -0.20 | -0.01 | 0 / 99 | 0.01 | 0.5095 | 0.4950 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.4750 (20/20) | -0.097 | 0.8975 | -0.1564 | 0.500 | 0.8950 | 1.0000 | -0.06 | -0.05 | 99 / 99 | 1.00 | 0.5973 | 0.5812 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.4950 (20/20) | -0.102 | 0.9101 | -0.1690 | 0.500 | 0.9300 | 1.0000 | -0.01 | -0.01 | 0 / 99 | 0.01 | 0.5155 | 0.5033 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4875 (20/20) | -0.016 | 0.7411 | +0.0000 | 0.500 | 0.5038 | 0.6000 | -3.33 | -0.13 | 99 / 99 | 1.00 | 0.5528 | 0.5792 | None / None / None |

### World No, seed 91122: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.2485; block present 20 of 40.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5050 < 0.90)]. rule #2.1: AUC = 0.4725 (20/20), p_S = 0.87 (n_ge = 86 of 99, n_deg = 0), p_P = 0.6139; ceiling_full = 0.5050, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4725 (20/20) | -0.168 | 1.2013 | -0.4452 | 0.500 | 0.5050 | 1.0000 | -5.50 | -0.06 | 86 / 99 | 0.87 | 0.6139 | 0.5823 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.4875 (20/20) | -0.138 | 1.0923 | -0.3362 | 0.500 | 0.5150 | 1.0000 | -0.83 | -0.03 | 98 / 99 | 0.99 | 0.5495 | 0.5346 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.4900 (20/20) | -0.101 | 0.9760 | -0.2199 | 0.500 | 0.8225 | 1.0000 | -0.03 | -0.02 | 99 / 99 | 1.00 | 0.5443 | 0.5260 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5000 (20/20) | -0.072 | 0.9632 | -0.2071 | 0.500 | 0.8300 | 1.0000 | 0.00 | 0.00 | 0 / 99 | 0.01 | 0.4995 | 0.4947 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.5275 (20/20) | -0.029 | 0.9620 | -0.2059 | 0.500 | 0.8325 | 1.0000 | 0.08 | 0.05 | 0 / 99 | 0.01 | 0.3829 | 0.3900 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4950 (20/20) | -0.017 | 0.7561 | +0.0000 | 0.500 | 0.4963 | 0.6000 | n/a | -0.05 | 99 / 99 | 1.00 | 0.5304 | 0.4495 | None / None / None |

### World No, seed 91123: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.2530; block present 20 of 40.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.4838 < 0.90)]. rule #2.1: AUC = 0.4525 (20/20), p_S = 0.75 (n_ge = 74 of 99, n_deg = 0), p_P = 0.6926; ceiling_full = 0.4838, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4525 (20/20) | -0.226 | 1.2002 | -0.4451 | 0.500 | 0.4838 | 1.0000 | n/a | -0.09 | 74 / 99 | 0.75 | 0.6926 | 0.5921 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.4450 (20/20) | -0.192 | 1.0897 | -0.3346 | 0.500 | 0.4600 | 1.0000 | n/a | -0.11 | 99 / 99 | 1.00 | 0.7237 | 0.6249 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.4375 (20/20) | -0.206 | 0.9802 | -0.2250 | 0.500 | 0.4875 | 1.0000 | n/a | -0.12 | 99 / 99 | 1.00 | 0.7471 | 0.6775 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.4450 (20/20) | -0.240 | 0.9953 | -0.2402 | 0.500 | 0.7925 | 1.0000 | -0.19 | -0.11 | 99 / 99 | 1.00 | 0.7243 | 0.6559 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.4475 (20/20) | -0.255 | 1.0032 | -0.2481 | 0.500 | 0.8150 | 1.0000 | -0.17 | -0.10 | 99 / 99 | 1.00 | 0.7139 | 0.6793 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4700 (20/20) | -0.059 | 0.7551 | +0.0000 | 0.500 | 0.4763 | 0.6000 | n/a | -0.30 | 99 / 99 | 1.00 | 0.6360 | 0.4122 | None / None / None |

### World No, seed 91124: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.2719; block present 20 of 40.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.5162 < 0.90)]. rule #2.1: AUC = 0.5100 (20/20), p_S = 0.05 (n_ge = 4 of 99, n_deg = 0), p_P = 0.4599; ceiling_full = 0.5162, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5100 (20/20) | -0.007 | 1.2116 | -0.3116 | 0.500 | 0.5162 | 1.0000 | 0.62 | 0.02 | 4 / 99 | 0.05 | 0.4599 | 0.4472 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.4975 (20/20) | -0.093 | 1.1333 | -0.2333 | 0.500 | 0.5300 | 1.0000 | -0.08 | -0.01 | 0 / 99 | 0.01 | 0.5121 | 0.4763 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.4825 (20/20) | -0.092 | 1.0129 | -0.1130 | 0.500 | 0.5625 | 1.0000 | -0.28 | -0.04 | 99 / 99 | 1.00 | 0.5739 | 0.5217 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.4825 (20/20) | -0.101 | 1.0286 | -0.1287 | 0.500 | 0.7050 | 1.0000 | -0.09 | -0.04 | 99 / 99 | 1.00 | 0.5754 | 0.5115 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.4650 (20/20) | -0.132 | 1.0361 | -0.1361 | 0.500 | 0.7750 | 1.0000 | -0.13 | -0.07 | 99 / 99 | 1.00 | 0.6486 | 0.5940 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4875 (20/20) | -0.035 | 0.9000 | +0.0000 | 0.500 | 0.4875 | 0.6000 | n/a | -0.13 | 99 / 99 | 1.00 | 0.5603 | 0.6687 | None / None / None |

### World W, seed 91130: W: rule weaker than the information available

Outside density 0.3056; block present 20 of 40.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.4888 (20/20), p_S = 0.94 (n_ge = 93 of 99, n_deg = 0), p_P = 0.5461; ceiling_full = 0.5038, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4888 (20/20) | -0.036 | 1.1109 | -0.3906 | 0.500 | 0.5038 | 1.0000 | -3.00 | -0.02 | 93 / 99 | 0.94 | 0.5461 | 0.5307 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.4925 (20/20) | 0.005 | 1.0135 | -0.2932 | 0.500 | 0.4850 | 1.0000 | n/a | -0.02 | 99 / 99 | 1.00 | 0.5337 | 0.5276 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7175 (20/20) | 1.432 | 0.7530 | -0.0327 | 0.550 | 0.8325 | 1.0000 | 0.65 | 0.44 | 0 / 99 | 0.01 | 0.0088 | 0.0172 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.6975 (20/20) | 1.430 | 0.7945 | -0.0742 | 0.600 | 0.8925 | 1.0000 | 0.50 | 0.40 | 0 / 99 | 0.01 | 0.0166 | 0.0223 | 1.0 / 1.0 / 1.0 |
| BF_4 | 0.6775 (20/20) | 0.830 | 0.7402 | -0.0199 | 0.600 | 0.8425 | 1.0000 | 0.52 | 0.35 | 0 / 99 | 0.01 | 0.0295 | 0.0403 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5350 (20/20) | 0.053 | 0.7203 | +0.0000 | 0.550 | 0.5250 | 0.7200 | 1.40 | 0.16 | 99 / 99 | 1.00 | 0.3488 | 0.8443 | None / None / None |

### World W, seed 91131: W: rule weaker than the information available

Outside density 0.2996; block present 20 of 40.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.5150 (20/20), p_S = 0.20 (n_ge = 19 of 99, n_deg = 0), p_P = 0.4418; ceiling_full = 0.5025, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5150 (20/20) | -0.029 | 1.0680 | -0.3194 | 0.500 | 0.5025 | 1.0000 | 6.00 | 0.03 | 19 / 99 | 0.20 | 0.4418 | 0.4400 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5050 (20/20) | -0.032 | 1.0030 | -0.2544 | 0.500 | 0.5150 | 1.0000 | 0.33 | 0.01 | 1 / 99 | 0.02 | 0.4843 | 0.4777 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.8100 (20/20) | 2.639 | 0.6285 | +0.1202 | 0.750 | 0.9175 | 1.0000 | 0.74 | 0.62 | 0 / 99 | 0.01 | 0.0005 | 0.0023 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.7850 (20/20) | 2.642 | 0.6702 | +0.0784 | 0.750 | 0.9075 | 1.0000 | 0.70 | 0.57 | 0 / 99 | 0.01 | 0.0014 | 0.0055 | 1.0 / 3.0 / 1.0 |
| BF_4 | 0.7400 (20/20) | 1.391 | 0.6510 | +0.0976 | 0.700 | 0.9175 | 1.0000 | 0.57 | 0.48 | 0 / 99 | 0.01 | 0.0053 | 0.0155 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5025 (20/20) | 0.009 | 0.7487 | +0.0000 | 0.500 | 0.5000 | 0.7200 | n/a | 0.01 | 99 / 99 | 1.00 | 0.4954 | 0.5233 | None / None / None |

### World W, seed 91132: W: rule weaker than the information available

Outside density 0.2872; block present 20 of 40.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.4925 (20/20), p_S = 0.95 (n_ge = 94 of 99, n_deg = 0), p_P = 0.5377; ceiling_full = 0.5088, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4925 (20/20) | -0.026 | 1.0681 | -0.3438 | 0.500 | 0.5088 | 1.0000 | -0.86 | -0.02 | 94 / 99 | 0.95 | 0.5377 | 0.5688 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.4925 (20/20) | -0.005 | 0.9634 | -0.2390 | 0.500 | 0.5125 | 1.0000 | -0.60 | -0.02 | 99 / 99 | 1.00 | 0.5382 | 0.5762 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7500 (20/20) | 2.084 | 0.6180 | +0.1064 | 0.500 | 0.8925 | 1.0000 | 0.64 | 0.50 | 0 / 99 | 0.01 | 0.0036 | 0.0095 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.7250 (20/20) | 1.839 | 0.7037 | +0.0206 | 0.500 | 0.9450 | 1.0000 | 0.51 | 0.45 | 0 / 99 | 0.01 | 0.0085 | 0.0156 | 1.0 / 1.0 / 1.0 |
| BF_4 | 0.7250 (20/20) | 1.044 | 0.6881 | +0.0362 | 0.550 | 0.9475 | 1.0000 | 0.50 | 0.45 | 0 / 99 | 0.01 | 0.0081 | 0.0150 | 3.0 / 1.0 / 1.0 |
| N1 | 0.5212 (20/20) | 0.037 | 0.7243 | +0.0000 | 0.500 | 0.5225 | 0.7200 | 0.94 | 0.10 | 99 / 99 | 1.00 | 0.4140 | 0.6724 | None / None / None |

### World W, seed 91133: W: rule weaker than the information available

Outside density 0.2920; block present 20 of 40.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.5450 (20/20), p_S = 0.08 (n_ge = 7 of 99, n_deg = 0), p_P = 0.3205; ceiling_full = 0.5525, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5450 (20/20) | 0.131 | 1.0840 | -0.3487 | 0.500 | 0.5525 | 1.0000 | 0.86 | 0.09 | 7 / 99 | 0.08 | 0.3205 | 0.3345 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5425 (20/20) | 0.104 | 1.0009 | -0.2656 | 0.500 | 0.5525 | 1.0000 | 0.81 | 0.08 | 0 / 99 | 0.01 | 0.3279 | 0.3306 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7450 (20/20) | 1.998 | 0.7067 | +0.0286 | 0.500 | 0.8425 | 1.0000 | 0.72 | 0.49 | 0 / 99 | 0.01 | 0.0047 | 0.0150 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.7225 (20/20) | 1.752 | 0.8058 | -0.0705 | 0.500 | 0.8900 | 1.0000 | 0.57 | 0.45 | 0 / 99 | 0.01 | 0.0087 | 0.0195 | 1.0 / 1.0 / 1.0 |
| BF_4 | 0.7175 (20/20) | 1.053 | 0.7319 | +0.0034 | 0.500 | 0.9475 | 1.0000 | 0.49 | 0.44 | 0 / 99 | 0.01 | 0.0113 | 0.0229 | 3.0 / 1.0 / 1.0 |
| N1 | 0.5050 (20/20) | -0.007 | 0.7353 | +0.0000 | 0.500 | 0.5038 | 0.7200 | 1.33 | 0.02 | 99 / 99 | 1.00 | 0.4790 | 0.1956 | None / None / None |

### World W, seed 91134: W: rule weaker than the information available

Outside density 0.2941; block present 20 of 40.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.5425 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.3297; ceiling_full = 0.5600, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 1, BF_3 1, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5425 (20/20) | 0.253 | 0.9833 | -0.2575 | 0.500 | 0.5600 | 1.0000 | 0.71 | 0.08 | 0 / 99 | 0.01 | 0.3297 | 0.3544 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.5450 (20/20) | 0.280 | 0.9028 | -0.1769 | 0.500 | 0.5650 | 1.0000 | 0.69 | 0.09 | 0 / 99 | 0.01 | 0.3185 | 0.3265 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7625 (20/20) | 2.391 | 0.5949 | +0.1309 | 0.550 | 0.9025 | 1.0000 | 0.65 | 0.52 | 0 / 99 | 0.01 | 0.0027 | 0.0082 | 1.0 / 1.0 / 1.0 |
| BF_3 | 0.7150 (20/20) | 2.081 | 0.7377 | -0.0119 | 0.550 | 0.9375 | 1.0000 | 0.49 | 0.43 | 0 / 99 | 0.01 | 0.0103 | 0.0267 | 1.0 / 1.0 / 1.0 |
| BF_4 | 0.7125 (20/20) | 1.220 | 0.6731 | +0.0527 | 0.600 | 0.9325 | 1.0000 | 0.49 | 0.43 | 0 / 99 | 0.01 | 0.0104 | 0.0292 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4813 (20/20) | 0.000 | 0.7258 | +0.0000 | 0.450 | 0.4850 | 0.7200 | n/a | -0.09 | 99 / 99 | 1.00 | 0.5817 | 0.9193 | None / None / None |

### World M0.5, seed 91140: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma))

Outside density 0.1434; block present 20 of 40.
Verdict line: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma)). rule #2.1: AUC = 0.6300 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0867; ceiling_full = 0.9375, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 100, BF_4 100.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6300 (20/20) | 0.268 | 0.8529 | +0.0576 | 0.550 | 0.9375 | 1.0000 | 0.30 | 0.26 | 0 / 99 | 0.01 | 0.0867 | 0.0006 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6225 (20/20) | 0.254 | 0.8613 | +0.0492 | 0.550 | 0.9475 | 1.0000 | 0.27 | 0.25 | 0 / 99 | 0.01 | 0.1003 | 0.0012 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.6650 (20/20) | 0.466 | 0.8249 | +0.0855 | 0.600 | 0.9875 | 1.0000 | 0.34 | 0.33 | 0 / 99 | 0.01 | 0.0389 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.5300 (20/20) | 0.005 | 0.9105 | +0.0000 | 0.500 | 0.9925 | 1.0000 | 0.06 | 0.06 | 99 / 99 | 1.00 | 0.3823 | 0.1723 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.5300 (20/20) | 0.005 | 0.9105 | +0.0000 | 0.500 | 0.9900 | 1.0000 | 0.06 | 0.06 | 99 / 99 | 1.00 | 0.3823 | 0.1723 | 100.0 / 3.0 / 1.0 |
| N1 | 0.5300 (20/20) | 0.005 | 0.9105 | +0.0000 | 0.500 | 0.5413 | 0.7200 | 0.73 | 0.14 | 99 / 99 | 1.00 | 0.3823 | 0.1723 | None / None / None |

### World M0.5, seed 91141: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma))

Outside density 0.1520; block present 20 of 40.
Verdict line: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma)). rule #2.1: AUC = 0.6212 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0963; ceiling_full = 0.9800, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 100, BF_3 100, BF_4 100.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6212 (20/20) | 0.309 | 0.8040 | +0.0584 | 0.650 | 0.9800 | 1.0000 | 0.25 | 0.24 | 0 / 99 | 0.01 | 0.0963 | 0.0021 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6175 (20/20) | 0.320 | 0.7985 | +0.0639 | 0.650 | 0.9775 | 1.0000 | 0.25 | 0.24 | 0 / 99 | 0.01 | 0.1043 | 0.0016 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.5225 (20/20) | 0.036 | 0.8624 | +0.0000 | 0.600 | 0.5425 | 1.0000 | 0.53 | 0.04 | 99 / 99 | 1.00 | 0.4123 | 0.4369 | 100.0 / 100.0 / 1.0 |
| BF_3 | 0.5225 (20/20) | 0.036 | 0.8624 | +0.0000 | 0.600 | 0.5425 | 1.0000 | 0.53 | 0.04 | 99 / 99 | 1.00 | 0.4123 | 0.4369 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.5225 (20/20) | 0.036 | 0.8624 | +0.0000 | 0.600 | 0.5425 | 1.0000 | 0.53 | 0.04 | 99 / 99 | 1.00 | 0.4123 | 0.4369 | 100.0 / 100.0 / 1.0 |
| N1 | 0.5225 (20/20) | 0.036 | 0.8624 | +0.0000 | 0.600 | 0.5425 | 0.7200 | 0.53 | 0.10 | 99 / 99 | 1.00 | 0.4123 | 0.4369 | None / None / None |

### World M0.5, seed 91142: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1431; block present 20 of 40.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 0.9900 >= 0.90)]. rule #2.1: AUC = 0.4875 (20/20), p_S = 0.32 (n_ge = 31 of 99, n_deg = 0), p_P = 0.5522; ceiling_full = 0.9900, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.4875 (20/20) | 0.006 | 0.8611 | +0.0162 | 0.500 | 0.9900 | 1.0000 | -0.03 | -0.03 | 31 / 99 | 0.32 | 0.5522 | 0.7720 | 100.0 / 3.0 / 1.0 |
| BF_1 | 0.4800 (20/20) | -0.011 | 0.8774 | +0.0000 | 0.500 | 0.9900 | 1.0000 | -0.04 | -0.04 | 97 / 99 | 0.98 | 0.5851 | 0.7783 | 100.0 / 3.0 / 1.0 |
| BF_2 | 0.4800 (20/20) | -0.011 | 0.8774 | +0.0000 | 0.500 | 0.4975 | 1.0000 | n/a | -0.04 | 97 / 99 | 0.98 | 0.5851 | 0.7783 | 100.0 / 100.0 / 1.0 |
| BF_3 | 0.4800 (20/20) | -0.011 | 0.8774 | +0.0000 | 0.500 | 0.4975 | 1.0000 | n/a | -0.04 | 99 / 99 | 1.00 | 0.5851 | 0.7783 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.4800 (20/20) | -0.011 | 0.8774 | +0.0000 | 0.500 | 0.4975 | 1.0000 | n/a | -0.04 | 99 / 99 | 1.00 | 0.5851 | 0.7783 | 100.0 / 100.0 / 1.0 |
| N1 | 0.4800 (20/20) | -0.011 | 0.8774 | +0.0000 | 0.500 | 0.4975 | 0.7200 | n/a | -0.09 | 99 / 99 | 1.00 | 0.5851 | 0.7783 | None / None / None |

### World M0.5, seed 91143: R: regrows

Outside density 0.1479; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 0.7675 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0015; ceiling_full = 0.9925, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 100, BF_3 100, BF_4 100.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7675 (20/20) | 0.742 | 0.6969 | +0.1920 | 0.700 | 0.9925 | 1.0000 | 0.54 | 0.53 | 0 / 99 | 0.01 | 0.0015 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7550 (20/20) | 0.732 | 0.7106 | +0.1783 | 0.700 | 0.9925 | 1.0000 | 0.52 | 0.51 | 0 / 99 | 0.01 | 0.0028 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.4875 (20/20) | -0.071 | 0.8888 | +0.0000 | 0.500 | 0.9825 | 1.0000 | -0.03 | -0.03 | 98 / 99 | 0.99 | 0.5605 | 0.2197 | 100.0 / 3.0 / 1.0 |
| BF_3 | 0.4875 (20/20) | -0.071 | 0.8888 | +0.0000 | 0.500 | 0.9875 | 1.0000 | -0.03 | -0.03 | 99 / 99 | 1.00 | 0.5605 | 0.2197 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.4875 (20/20) | -0.071 | 0.8888 | +0.0000 | 0.500 | 0.9900 | 1.0000 | -0.03 | -0.03 | 99 / 99 | 1.00 | 0.5605 | 0.2197 | 100.0 / 3.0 / 1.0 |
| N1 | 0.4875 (20/20) | -0.071 | 0.8888 | +0.0000 | 0.500 | 0.4825 | 0.7200 | n/a | -0.06 | 99 / 99 | 1.00 | 0.5605 | 0.2197 | None / None / None |

### World M0.5, seed 91144: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1460; block present 20 of 40.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 0.9975 >= 0.90)]. rule #2.1: AUC = 0.5112 (20/20), p_S = 0.48 (n_ge = 47 of 99, n_deg = 0), p_P = 0.4644; ceiling_full = 0.9975, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 100, BF_1 100, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on rule #2.1, BF_1, BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5112 (20/20) | 0.036 | 0.8254 | +0.0008 | 0.500 | 0.9975 | 1.0000 | 0.02 | 0.02 | 47 / 99 | 0.48 | 0.4644 | 0.7270 | 100.0 / 3.0 / 1.0 |
| BF_1 | 0.5162 (20/20) | 0.029 | 0.8262 | +0.0000 | 0.500 | 0.9975 | 1.0000 | 0.03 | 0.03 | 95 / 99 | 0.96 | 0.4418 | 0.5285 | 100.0 / 3.0 / 1.0 |
| BF_2 | 0.5162 (20/20) | 0.029 | 0.8262 | +0.0000 | 0.500 | 0.5188 | 1.0000 | 0.87 | 0.03 | 98 / 99 | 0.99 | 0.4418 | 0.5285 | 100.0 / 100.0 / 1.0 |
| BF_3 | 0.5162 (20/20) | 0.029 | 0.8262 | +0.0000 | 0.500 | 0.5188 | 1.0000 | 0.87 | 0.03 | 99 / 99 | 1.00 | 0.4418 | 0.5285 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.5162 (20/20) | 0.029 | 0.8262 | +0.0000 | 0.500 | 0.5188 | 1.0000 | 0.87 | 0.03 | 99 / 99 | 1.00 | 0.4418 | 0.5285 | 100.0 / 100.0 / 1.0 |
| N1 | 0.5162 (20/20) | 0.029 | 0.8262 | +0.0000 | 0.500 | 0.5188 | 0.7200 | 0.87 | 0.07 | 99 / 99 | 1.00 | 0.4418 | 0.5285 | None / None / None |

### World M1.0, seed 91150: R: regrows

Outside density 0.1663; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 0.7675 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0014; ceiling_full = 0.9525, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7675 (20/20) | 0.875 | 0.7439 | +0.1642 | 0.700 | 0.9525 | 1.0000 | 0.59 | 0.53 | 0 / 99 | 0.01 | 0.0014 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.7625 (20/20) | 0.818 | 0.7277 | +0.1803 | 0.650 | 0.9450 | 1.0000 | 0.59 | 0.52 | 0 / 99 | 0.01 | 0.0018 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.7125 (20/20) | 0.708 | 0.7659 | +0.1422 | 0.600 | 0.9850 | 1.0000 | 0.44 | 0.43 | 0 / 99 | 0.01 | 0.0084 | 0.0004 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7200 (20/20) | 0.872 | 0.7585 | +0.1496 | 0.600 | 0.9850 | 1.0000 | 0.45 | 0.44 | 0 / 99 | 0.01 | 0.0079 | 0.0002 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7250 (20/20) | 0.890 | 0.7569 | +0.1512 | 0.650 | 0.9875 | 1.0000 | 0.46 | 0.45 | 0 / 99 | 0.01 | 0.0068 | 0.0003 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4850 (20/20) | 0.008 | 0.9081 | +0.0000 | 0.500 | 0.5025 | 0.7200 | -6.00 | -0.07 | 99 / 99 | 1.00 | 0.5590 | 0.7759 | None / None / None |

### World M1.0, seed 91151: R: regrows

Outside density 0.1670; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 0.9475 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.9475 (20/20) | 2.476 | 0.4679 | +0.4065 | 0.900 | 1.0000 | 1.0000 | 0.90 | 0.90 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.9425 (20/20) | 2.220 | 0.4666 | +0.4079 | 0.900 | 1.0000 | 1.0000 | 0.89 | 0.89 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.8700 (20/20) | 1.481 | 0.5714 | +0.3030 | 0.800 | 0.9975 | 1.0000 | 0.74 | 0.74 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.8775 (20/20) | 1.444 | 0.5787 | +0.2958 | 0.800 | 0.9975 | 1.0000 | 0.76 | 0.75 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.8825 (20/20) | 1.531 | 0.5688 | +0.3056 | 0.800 | 1.0000 | 1.0000 | 0.76 | 0.76 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4925 (20/20) | -0.030 | 0.8744 | +0.0000 | 0.500 | 0.4963 | 0.7200 | n/a | -0.03 | 99 / 99 | 1.00 | 0.5426 | 0.4546 | None / None / None |

### World M1.0, seed 91152: R: regrows

Outside density 0.1704; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 0.9775 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.9775 (20/20) | 2.114 | 0.4181 | +0.3584 | 0.900 | 1.0000 | 1.0000 | 0.96 | 0.96 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.9500 (20/20) | 1.347 | 0.5011 | +0.2754 | 0.900 | 0.9950 | 1.0000 | 0.91 | 0.90 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.8975 (20/20) | 1.125 | 0.5452 | +0.2313 | 0.800 | 1.0000 | 1.0000 | 0.79 | 0.79 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.9250 (20/20) | 1.205 | 0.5405 | +0.2360 | 0.850 | 1.0000 | 1.0000 | 0.85 | 0.85 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.9275 (20/20) | 1.223 | 0.5426 | +0.2338 | 0.850 | 1.0000 | 1.0000 | 0.85 | 0.85 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5150 (20/20) | 0.016 | 0.7765 | +0.0000 | 0.450 | 0.5225 | 0.7200 | 0.67 | 0.07 | 99 / 99 | 1.00 | 0.4368 | 0.5206 | None / None / None |

### World M1.0, seed 91153: R: regrows

Outside density 0.1730; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 0.9525 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 0.9975, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.9525 (20/20) | 2.183 | 0.4160 | +0.3843 | 0.900 | 0.9975 | 1.0000 | 0.91 | 0.91 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.9475 (20/20) | 1.973 | 0.4218 | +0.3786 | 0.900 | 1.0000 | 1.0000 | 0.90 | 0.90 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.8250 (20/20) | 1.166 | 0.5661 | +0.2343 | 0.750 | 0.9925 | 1.0000 | 0.66 | 0.65 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.8250 (20/20) | 1.135 | 0.5853 | +0.2151 | 0.750 | 0.9900 | 1.0000 | 0.66 | 0.65 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.8350 (20/20) | 1.106 | 0.5846 | +0.2158 | 0.750 | 1.0000 | 1.0000 | 0.67 | 0.67 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4938 (20/20) | -0.037 | 0.8004 | +0.0000 | 0.550 | 0.4950 | 0.7200 | n/a | -0.03 | 99 / 99 | 1.00 | 0.5304 | 0.0707 | None / None / None |

### World M1.0, seed 91154: R: regrows

Outside density 0.1711; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 0.9975 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 1, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.9975 (20/20) | 2.481 | 0.4373 | +0.4062 | 0.950 | 1.0000 | 1.0000 | 1.00 | 1.00 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.9950 (20/20) | 2.232 | 0.4443 | +0.3991 | 0.950 | 1.0000 | 1.0000 | 0.99 | 0.99 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_2 | 0.9325 (20/20) | 1.393 | 0.5727 | +0.2707 | 0.850 | 1.0000 | 1.0000 | 0.86 | 0.86 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.9350 (20/20) | 1.564 | 0.5532 | +0.2903 | 0.800 | 1.0000 | 1.0000 | 0.87 | 0.87 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.9375 (20/20) | 1.568 | 0.5616 | +0.2819 | 0.800 | 1.0000 | 1.0000 | 0.88 | 0.88 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5250 (20/20) | 0.057 | 0.8435 | +0.0000 | 0.500 | 0.5250 | 0.7200 | 1.00 | 0.11 | 99 / 99 | 1.00 | 0.3872 | 0.6255 | None / None / None |

### World M0.6, seed 91160: W: rule weaker than the information available

Outside density 0.1563; block present 20 of 40.
Verdict line: W: rule weaker than the information available. rule #2.1: AUC = 0.6800 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0269; ceiling_full = 0.9450, ceiling_block = 1.0000; R/W reading: rule #2.1 -> W, BF_1 -> W; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6800 (20/20) | 0.520 | 0.7629 | +0.1066 | 0.650 | 0.9450 | 1.0000 | 0.40 | 0.36 | 0 / 99 | 0.01 | 0.0269 | 0.0002 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7150 (20/20) | 0.489 | 0.7591 | +0.1104 | 0.650 | 0.9450 | 1.0000 | 0.48 | 0.43 | 0 / 99 | 0.01 | 0.0101 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.6675 (20/20) | 0.544 | 0.7588 | +0.1106 | 0.650 | 0.9850 | 1.0000 | 0.35 | 0.33 | 0 / 99 | 0.01 | 0.0359 | 0.0015 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7000 (20/20) | 0.677 | 0.7393 | +0.1301 | 0.650 | 0.9900 | 1.0000 | 0.41 | 0.40 | 0 / 99 | 0.01 | 0.0130 | 0.0010 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7125 (20/20) | 0.715 | 0.7385 | +0.1310 | 0.600 | 0.9950 | 1.0000 | 0.43 | 0.43 | 0 / 99 | 0.01 | 0.0094 | 0.0004 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5025 (20/20) | -0.001 | 0.8695 | +0.0000 | 0.550 | 0.5112 | 0.7200 | 0.22 | 0.01 | 99 / 99 | 1.00 | 0.5025 | 0.5134 | None / None / None |

### World M0.6, seed 91161: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma))

Outside density 0.1496; block present 20 of 40.
Verdict line: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma)). rule #2.1: AUC = 0.5837 (20/20), p_S = 0.02 (n_ge = 1 of 99, n_deg = 0), p_P = 0.1894; ceiling_full = 0.9200, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 100, BF_4 100.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5837 (20/20) | 0.203 | 0.8475 | +0.0811 | 0.550 | 0.9200 | 1.0000 | 0.20 | 0.17 | 1 / 99 | 0.02 | 0.1894 | 0.0245 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.5850 (20/20) | 0.216 | 0.8727 | +0.0560 | 0.550 | 0.9300 | 1.0000 | 0.20 | 0.17 | 0 / 99 | 0.01 | 0.1846 | 0.0105 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.6350 (20/20) | 0.275 | 0.8254 | +0.1032 | 0.550 | 0.9275 | 1.0000 | 0.32 | 0.27 | 0 / 99 | 0.01 | 0.0741 | 0.0025 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.4825 (20/20) | -0.025 | 0.9286 | +0.0000 | 0.550 | 0.9200 | 1.0000 | -0.04 | -0.04 | 99 / 99 | 1.00 | 0.5790 | 0.5866 | 100.0 / 3.0 / 1.0 |
| BF_4 | 0.4825 (20/20) | -0.025 | 0.9286 | +0.0000 | 0.550 | 0.5100 | 1.0000 | -1.75 | -0.04 | 99 / 99 | 1.00 | 0.5790 | 0.5866 | 100.0 / 100.0 / 1.0 |
| N1 | 0.4825 (20/20) | -0.025 | 0.9286 | +0.0000 | 0.550 | 0.5100 | 0.7200 | -1.75 | -0.08 | 99 / 99 | 1.00 | 0.5790 | 0.5866 | None / None / None |

### World M0.6, seed 91162: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma))

Outside density 0.1572; block present 20 of 40.
Verdict line: U: on the detection threshold; cannot be separated (at the leg-P detection limit gamma*_P = 0.75; transition band empty: the two limits coincide (0 grid steps, 0 in gamma)). rule #2.1: AUC = 0.6450 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0598; ceiling_full = 0.9425, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6450 (20/20) | 0.376 | 0.8244 | +0.0922 | 0.600 | 0.9425 | 1.0000 | 0.33 | 0.29 | 0 / 99 | 0.01 | 0.0598 | 0.0021 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6500 (20/20) | 0.363 | 0.8309 | +0.0856 | 0.600 | 0.9425 | 1.0000 | 0.34 | 0.30 | 0 / 99 | 0.01 | 0.0527 | 0.0022 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.6500 (20/20) | 0.361 | 0.8342 | +0.0823 | 0.600 | 0.9275 | 1.0000 | 0.35 | 0.30 | 0 / 99 | 0.01 | 0.0545 | 0.0021 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.6200 (20/20) | 0.363 | 0.8458 | +0.0707 | 0.600 | 0.9275 | 1.0000 | 0.28 | 0.24 | 0 / 99 | 0.01 | 0.1010 | 0.0057 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.6150 (20/20) | 0.357 | 0.8489 | +0.0676 | 0.600 | 0.9625 | 1.0000 | 0.25 | 0.23 | 0 / 99 | 0.01 | 0.1141 | 0.0059 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5125 (20/20) | -0.014 | 0.9166 | +0.0000 | 0.500 | 0.5225 | 0.7200 | 0.56 | 0.06 | 99 / 99 | 1.00 | 0.4568 | 0.2813 | None / None / None |

### World M0.6, seed 91163: R: regrows

Outside density 0.1553; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 0.7325 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0066; ceiling_full = 0.9950, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 100.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7325 (20/20) | 0.568 | 0.7413 | +0.1398 | 0.650 | 0.9950 | 1.0000 | 0.47 | 0.47 | 0 / 99 | 0.01 | 0.0066 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7250 (20/20) | 0.559 | 0.7401 | +0.1411 | 0.600 | 0.9950 | 1.0000 | 0.45 | 0.45 | 0 / 99 | 0.01 | 0.0086 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.6575 (20/20) | 0.389 | 0.7844 | +0.0967 | 0.550 | 1.0000 | 1.0000 | 0.31 | 0.31 | 0 / 99 | 0.01 | 0.0479 | 0.0026 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.4650 (20/20) | -0.102 | 0.9124 | -0.0313 | 0.450 | 1.0000 | 1.0000 | -0.07 | -0.07 | 99 / 99 | 1.00 | 0.6508 | 0.6474 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.4838 (20/20) | -0.005 | 0.8811 | +0.0000 | 0.500 | 1.0000 | 1.0000 | -0.03 | -0.03 | 99 / 99 | 1.00 | 0.5805 | 0.8166 | 100.0 / 3.0 / 1.0 |
| N1 | 0.4838 (20/20) | -0.005 | 0.8811 | +0.0000 | 0.500 | 0.5050 | 0.7200 | -3.25 | -0.07 | 99 / 99 | 1.00 | 0.5805 | 0.8166 | None / None / None |

### World M0.6, seed 91164: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1505; block present 20 of 40.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: orthogonal (rule #2.1's ceiling_full = 0.8575 < 0.90)]. rule #2.1: AUC = 0.5125 (20/20), p_S = 0.14 (n_ge = 13 of 99, n_deg = 0), p_P = 0.4453; ceiling_full = 0.8575, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 100, BF_3 100, BF_4 100; G reached through lambda = 100 on BF_2, BF_3, BF_4: there the interaction is shrunk to N1's additive prediction, so this G reads 'weaker than the detection limit', not 'absent'.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.5125 (20/20) | 0.010 | 0.9064 | +0.0178 | 0.450 | 0.8575 | 1.0000 | 0.03 | 0.02 | 13 / 99 | 0.14 | 0.4453 | 0.0154 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.5300 (20/20) | 0.038 | 0.9049 | +0.0193 | 0.550 | 0.8525 | 1.0000 | 0.09 | 0.06 | 2 / 99 | 0.03 | 0.3755 | 0.0087 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.4950 (20/20) | -0.056 | 0.9243 | +0.0000 | 0.500 | 0.4938 | 1.0000 | n/a | -0.01 | 99 / 99 | 1.00 | 0.5242 | 0.1587 | 100.0 / 100.0 / 1.0 |
| BF_3 | 0.4950 (20/20) | -0.056 | 0.9243 | +0.0000 | 0.500 | 0.4938 | 1.0000 | n/a | -0.01 | 99 / 99 | 1.00 | 0.5242 | 0.1587 | 100.0 / 100.0 / 1.0 |
| BF_4 | 0.4950 (20/20) | -0.056 | 0.9243 | +0.0000 | 0.500 | 0.4938 | 1.0000 | n/a | -0.01 | 99 / 99 | 1.00 | 0.5242 | 0.1587 | 100.0 / 100.0 / 1.0 |
| N1 | 0.4950 (20/20) | -0.056 | 0.9243 | +0.0000 | 0.500 | 0.4938 | 0.7200 | n/a | -0.02 | 99 / 99 | 1.00 | 0.5242 | 0.1587 | None / None / None |

### World M0.75, seed 91170: R: regrows

Outside density 0.1665; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 0.8163 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0006; ceiling_full = 0.9850, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.8163 (20/20) | 1.175 | 0.6217 | +0.2240 | 0.750 | 0.9850 | 1.0000 | 0.65 | 0.63 | 0 / 99 | 0.01 | 0.0006 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.8275 (20/20) | 1.193 | 0.6227 | +0.2230 | 0.750 | 0.9825 | 1.0000 | 0.68 | 0.66 | 0 / 99 | 0.01 | 0.0003 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.8250 (20/20) | 1.172 | 0.6281 | +0.2176 | 0.750 | 0.9875 | 1.0000 | 0.67 | 0.65 | 0 / 99 | 0.01 | 0.0004 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7975 (20/20) | 0.964 | 0.6709 | +0.1748 | 0.700 | 0.9800 | 1.0000 | 0.62 | 0.59 | 0 / 99 | 0.01 | 0.0007 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7975 (20/20) | 0.973 | 0.6668 | +0.1789 | 0.750 | 0.9800 | 1.0000 | 0.62 | 0.59 | 0 / 99 | 0.01 | 0.0007 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5138 (20/20) | 0.145 | 0.8457 | +0.0000 | 0.450 | 0.5275 | 0.7200 | 0.50 | 0.06 | 99 / 99 | 1.00 | 0.4340 | 0.9882 | None / None / None |

### World M0.75, seed 91171: R: regrows

Outside density 0.1572; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 0.9575 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.9575 (20/20) | 1.293 | 0.5393 | +0.2462 | 0.900 | 1.0000 | 1.0000 | 0.92 | 0.92 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.9375 (20/20) | 1.234 | 0.5369 | +0.2486 | 0.850 | 1.0000 | 1.0000 | 0.88 | 0.88 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.9525 (20/20) | 1.242 | 0.5301 | +0.2554 | 0.850 | 1.0000 | 1.0000 | 0.91 | 0.91 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.9300 (20/20) | 1.073 | 0.5611 | +0.2245 | 0.800 | 1.0000 | 1.0000 | 0.86 | 0.86 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.9175 (20/20) | 1.047 | 0.5721 | +0.2134 | 0.900 | 1.0000 | 1.0000 | 0.83 | 0.83 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5175 (20/20) | 0.052 | 0.7855 | +0.0000 | 0.450 | 0.5325 | 0.7200 | 0.54 | 0.08 | 99 / 99 | 1.00 | 0.4173 | 0.8618 | None / None / None |

### World M0.75, seed 91172: R: regrows

Outside density 0.1677; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 0.8925 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.8925 (20/20) | 1.176 | 0.5232 | +0.2321 | 0.850 | 1.0000 | 1.0000 | 0.78 | 0.78 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.8825 (20/20) | 1.121 | 0.5339 | +0.2213 | 0.800 | 0.9975 | 1.0000 | 0.77 | 0.76 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.8125 (20/20) | 1.003 | 0.5704 | +0.1849 | 0.750 | 0.9950 | 1.0000 | 0.63 | 0.62 | 0 / 99 | 0.01 | 0.0006 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.8025 (20/20) | 1.039 | 0.5714 | +0.1839 | 0.700 | 0.9900 | 1.0000 | 0.62 | 0.60 | 0 / 99 | 0.01 | 0.0007 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7775 (20/20) | 1.002 | 0.5806 | +0.1747 | 0.650 | 0.9900 | 1.0000 | 0.57 | 0.55 | 0 / 99 | 0.01 | 0.0014 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5375 (20/20) | 0.080 | 0.7553 | +0.0000 | 0.600 | 0.5425 | 0.7200 | 0.88 | 0.17 | 99 / 99 | 1.00 | 0.3379 | 0.5062 | None / None / None |

### World M0.75, seed 91173: R: regrows

Outside density 0.1503; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 0.7725 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0007; ceiling_full = 0.9925, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.7725 (20/20) | 0.692 | 0.7120 | +0.1299 | 0.750 | 0.9925 | 1.0000 | 0.55 | 0.54 | 0 / 99 | 0.01 | 0.0007 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.7700 (20/20) | 0.723 | 0.6968 | +0.1451 | 0.750 | 0.9775 | 1.0000 | 0.57 | 0.54 | 0 / 99 | 0.01 | 0.0010 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.8000 (20/20) | 0.727 | 0.6921 | +0.1498 | 0.700 | 0.9975 | 1.0000 | 0.60 | 0.60 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7725 (20/20) | 0.800 | 0.6832 | +0.1588 | 0.700 | 0.9900 | 1.0000 | 0.56 | 0.54 | 0 / 99 | 0.01 | 0.0005 | 0.0003 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7325 (20/20) | 0.697 | 0.7104 | +0.1315 | 0.650 | 0.9900 | 1.0000 | 0.47 | 0.47 | 0 / 99 | 0.01 | 0.0042 | 0.0043 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5162 (20/20) | 0.046 | 0.8419 | +0.0000 | 0.550 | 0.5337 | 0.7200 | 0.48 | 0.07 | 99 / 99 | 1.00 | 0.4337 | 0.5163 | None / None / None |

### World M0.75, seed 91174: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Outside density 0.1536; block present 20 of 40.
Verdict line: G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 1.0000 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10) [mechanism, description only: no information (rule #2.1's ceiling_full = 0.9875 >= 0.90)]. rule #2.1: AUC = 0.6188 (20/20), p_S = 0.02 (n_ge = 1 of 99, n_deg = 0), p_P = 0.1032; ceiling_full = 0.9875, ceiling_block = 1.0000; R/W reading: rule #2.1 -> -, BF_1 -> -; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.6188 (20/20) | 0.335 | 0.7792 | +0.0806 | 0.600 | 0.9875 | 1.0000 | 0.24 | 0.24 | 1 / 99 | 0.02 | 0.1032 | 0.0055 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.6075 (20/20) | 0.323 | 0.7736 | +0.0862 | 0.550 | 0.9900 | 1.0000 | 0.22 | 0.22 | 0 / 99 | 0.01 | 0.1289 | 0.0074 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.6075 (20/20) | 0.287 | 0.8072 | +0.0526 | 0.650 | 0.9975 | 1.0000 | 0.22 | 0.22 | 0 / 99 | 0.01 | 0.1302 | 0.0211 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.6025 (20/20) | 0.275 | 0.8152 | +0.0445 | 0.650 | 0.9875 | 1.0000 | 0.21 | 0.21 | 0 / 99 | 0.01 | 0.1419 | 0.0356 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.6025 (20/20) | 0.277 | 0.8115 | +0.0483 | 0.600 | 0.9925 | 1.0000 | 0.21 | 0.21 | 0 / 99 | 0.01 | 0.1430 | 0.0259 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4637 (20/20) | -0.049 | 0.8598 | +0.0000 | 0.500 | 0.4800 | 0.7200 | n/a | -0.16 | 99 / 99 | 1.00 | 0.6602 | 0.7802 | None / None / None |

### World M0.85, seed 91180: R: regrows

Outside density 0.1654; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 0.8375 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 0.9700, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.8375 (20/20) | 1.002 | 0.6344 | +0.2175 | 0.750 | 0.9700 | 1.0000 | 0.72 | 0.68 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.8325 (20/20) | 0.962 | 0.6432 | +0.2087 | 0.750 | 0.9750 | 1.0000 | 0.70 | 0.67 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.8075 (20/20) | 0.958 | 0.6530 | +0.1989 | 0.800 | 0.9725 | 1.0000 | 0.65 | 0.61 | 0 / 99 | 0.01 | 0.0003 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.8075 (20/20) | 0.971 | 0.6544 | +0.1975 | 0.750 | 0.9750 | 1.0000 | 0.65 | 0.61 | 0 / 99 | 0.01 | 0.0004 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.8200 (20/20) | 0.982 | 0.6500 | +0.2019 | 0.750 | 1.0000 | 1.0000 | 0.64 | 0.64 | 0 / 99 | 0.01 | 0.0003 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5038 (20/20) | -0.013 | 0.8519 | +0.0000 | 0.450 | 0.5000 | 0.7200 | n/a | 0.02 | 99 / 99 | 1.00 | 0.4939 | 0.3961 | None / None / None |

### World M0.85, seed 91181: R: regrows

Outside density 0.1711; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 0.8300 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0002; ceiling_full = 0.9925, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.8300 (20/20) | 1.025 | 0.6391 | +0.1991 | 0.750 | 0.9925 | 1.0000 | 0.67 | 0.66 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.8225 (20/20) | 1.000 | 0.6376 | +0.2006 | 0.750 | 0.9925 | 1.0000 | 0.65 | 0.65 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.8000 (20/20) | 1.007 | 0.6455 | +0.1927 | 0.700 | 0.9900 | 1.0000 | 0.61 | 0.60 | 0 / 99 | 0.01 | 0.0004 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.8150 (20/20) | 1.042 | 0.6443 | +0.1938 | 0.750 | 0.9775 | 1.0000 | 0.66 | 0.63 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.8500 (20/20) | 1.085 | 0.6416 | +0.1965 | 0.750 | 0.9950 | 1.0000 | 0.71 | 0.70 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5050 (20/20) | 0.046 | 0.8381 | +0.0000 | 0.450 | 0.5188 | 0.7200 | 0.27 | 0.02 | 99 / 99 | 1.00 | 0.4815 | 0.8735 | None / None / None |

### World M0.85, seed 91182: R: regrows

Outside density 0.1685; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 0.9575 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 1, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.9575 (20/20) | 1.466 | 0.5227 | +0.2680 | 0.900 | 1.0000 | 1.0000 | 0.92 | 0.92 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 1.0 / 1.0 / 1.0 |
| BF_1 | 0.8950 (20/20) | 0.940 | 0.5859 | +0.2048 | 0.800 | 1.0000 | 1.0000 | 0.79 | 0.79 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.8825 (20/20) | 0.945 | 0.5898 | +0.2009 | 0.750 | 0.9950 | 1.0000 | 0.77 | 0.76 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.8975 (20/20) | 1.017 | 0.5852 | +0.2055 | 0.750 | 0.9950 | 1.0000 | 0.80 | 0.79 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.9050 (20/20) | 1.054 | 0.5722 | +0.2186 | 0.800 | 0.9975 | 1.0000 | 0.81 | 0.81 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| N1 | 0.5262 (20/20) | 0.028 | 0.7908 | +0.0000 | 0.550 | 0.5375 | 0.7200 | 0.70 | 0.12 | 99 / 99 | 1.00 | 0.3929 | 0.2814 | None / None / None |

### World M0.85, seed 91183: R: regrows

Outside density 0.1639; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 0.8800 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 1.0000, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.8800 (20/20) | 1.208 | 0.5626 | +0.2616 | 0.750 | 1.0000 | 1.0000 | 0.76 | 0.76 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 1.0 / 1.0 |
| BF_1 | 0.8550 (20/20) | 1.095 | 0.5845 | +0.2397 | 0.800 | 1.0000 | 1.0000 | 0.71 | 0.71 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 1.0 / 1.0 |
| BF_2 | 0.8250 (20/20) | 1.140 | 0.5970 | +0.2273 | 0.750 | 0.9925 | 1.0000 | 0.66 | 0.65 | 0 / 99 | 0.01 | 0.0002 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7750 (20/20) | 1.014 | 0.6362 | +0.1880 | 0.700 | 0.9950 | 1.0000 | 0.56 | 0.55 | 0 / 99 | 0.01 | 0.0016 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7650 (20/20) | 0.974 | 0.6576 | +0.1666 | 0.700 | 0.9925 | 1.0000 | 0.54 | 0.53 | 0 / 99 | 0.01 | 0.0024 | 0.0004 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4738 (20/20) | -0.068 | 0.8242 | +0.0000 | 0.500 | 0.4825 | 0.7200 | n/a | -0.12 | 99 / 99 | 1.00 | 0.6161 | 0.4229 | None / None / None |

### World M0.85, seed 91184: R: regrows

Outside density 0.1515; block present 20 of 40.
Verdict line: R: regrows. rule #2.1: AUC = 0.8625 (20/20), p_S = 0.01 (n_ge = 0 of 99, n_deg = 0), p_P = 0.0001; ceiling_full = 0.9950, ceiling_block = 1.0000; R/W reading: rule #2.1 -> R, BF_1 -> R; lambda selected by each knockout fit (nested inner folds): rule #2.1 3, BF_1 3, BF_2 3, BF_3 3, BF_4 3.

| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | p_P row-col (diagnostic) | lambda ko/full/block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 0.8625 (20/20) | 1.143 | 0.5871 | +0.2438 | 0.850 | 0.9950 | 1.0000 | 0.73 | 0.73 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_1 | 0.8750 (20/20) | 1.108 | 0.5875 | +0.2433 | 0.850 | 1.0000 | 1.0000 | 0.75 | 0.75 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_2 | 0.8375 (20/20) | 1.027 | 0.6124 | +0.2185 | 0.750 | 1.0000 | 1.0000 | 0.68 | 0.68 | 0 / 99 | 0.01 | 0.0001 | 0.0001 | 3.0 / 3.0 / 1.0 |
| BF_3 | 0.7300 (20/20) | 0.820 | 0.6711 | +0.1598 | 0.650 | 0.9975 | 1.0000 | 0.46 | 0.46 | 0 / 99 | 0.01 | 0.0063 | 0.0007 | 3.0 / 3.0 / 1.0 |
| BF_4 | 0.7325 (20/20) | 0.810 | 0.6775 | +0.1534 | 0.650 | 0.9975 | 1.0000 | 0.47 | 0.47 | 0 / 99 | 0.01 | 0.0050 | 0.0006 | 3.0 / 3.0 / 1.0 |
| N1 | 0.4925 (20/20) | -0.011 | 0.8309 | +0.0000 | 0.550 | 0.4963 | 0.7200 | n/a | -0.03 | 99 / 99 | 1.00 | 0.5348 | 0.5476 | None / None / None |

## The registered reading (A section 4, quoted)

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

