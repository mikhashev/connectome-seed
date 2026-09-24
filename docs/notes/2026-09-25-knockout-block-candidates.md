# Knock out and regrow: which block, fixed before data

**Written:** 2026-09-25 by CC (subagent), for ADR-005 open question **Q1** ("Which block is knocked
out: which pathway, and how is it fixed before data?"). **Status:** proposal. It is not the
registration. Nothing was fitted, regrown or scored. No weight, synapse count or offset of any bank
was read. The only numbers taken from the banks are **counts of type pairs that a name rule
selects**, as allowed (§4 says exactly what was counted, and in what order).

## 1. What is being chosen

ADR-005, decision 3 and agreed point 6: remove a block of the bank, "chosen before any data is seen
and on biological grounds", train on the rest, and test whether a rule regrows the block better than
N1, better than the 99 degree-preserving shuffles, and better than the **permuted block** (Zcode's
second null). The registration "must state exactly what is removed, entirely".

The bank here is the 30-type grid (30 × 30 = 900 type-pair cells, self-pairs included). **B** is the
FlyWire-30 bank (165 pairs). **flyvis-30** is the generation-zero bank restricted to the same 30
types (228 pairs), which is a synthetic template of at least two flies, not an animal (ADR-005,
agreed point 2). The 30 types are R7, R8, L1–L5, C2, C3, Mi1, Mi4, Mi9, Tm1, Tm2, Tm3, Tm4, Tm9, Tm20,
T1, T2, T2a, T3, T4a–d and T5a–d.

**What a block is.** A block is a set of **cells** defined by a rule on type names. It holds both the
pairs present and the pairs absent. All four fields of every cell in it are removed: existence,
offsets, counts and sign. A block that holds only present pairs cannot be scored on discrimination:
a rule that just predicts "dense here" would win.

**Why a block must leave its endpoints visible.** N1 is a ridge logistic regression with one
source term and one target term per type (`harness.py`, `fit_n1`). A BF_r rule adds a rank-r
per-type term on top of N1's residual. If a block removes every entry of a type, neither can place
that type, and failure is guaranteed by construction. That is "no information", not "no grammar".
The other side of this is the **degree leakage** that ADR-005 names: whatever of a type's row and
column stays in training tells N1 its degree. The registration must print, for every endpoint type,
how many of its entries stay in training.

## 2. Three candidates

Counts are cells selected in the 900-cell grid, and pairs of B (out of 165) and of flyvis-30 (out of
228) among them.

| | block (name rule) | cells | B pairs | share of B | flyvis-30 pairs |
|---|---|---|---|---|---|
| **A** | motion-input rectangle: src ∈ {Mi1, Tm3, Mi4, Mi9, Tm1, Tm2, Tm4, Tm9} × tar ∈ {T4a–d, T5a–d} | 64 | 32 | 19.4 % | 32 |
| **B** | lamina outputs: src ∈ {L1–L5} × tar ∉ {L1–L5, R7, R8} | 115 | 28 | 17.0 % | 32 |
| **C** | colour path, R7/R8 outputs: src ∈ {R7, R8} × tar ∉ {R7, R8} | 56 | 4 | 2.4 % | 7 |

### A. ON and OFF motion inputs to T4 and T5, all four directions

- **Removes:** all 64 cells of the 8 × 8 rectangle: the four ON-pathway medulla inputs and the four
  OFF-pathway inputs, against all eight direction-selective cells. Nothing else.
- **Biology:** T4 (ON edges) takes its main columnar input from Mi1, Tm3, Mi4 and Mi9. T5 (OFF edges)
  takes its main input from Tm1, Tm2, Tm4 and Tm9. The two input sets barely overlap. So the block
  has a structure to regrow, and a clear place where the answer is "absent": the ON × T5 and
  OFF × T4 cells. Of the 64 cells, 32 are present in each bank. The two 16-cell rectangles (ON × T4,
  OFF × T5) are each fully present, so the 32 cross cells are absent in both banks. This is the
  textbook segregation, now also counted.
- **Sources:** Takemura et al. 2013, *Nature* 500:175 (Mi1 and Tm3 onto T4); Takemura et al. 2017,
  *eLife* 6:e24394 (the full T4 input set, including Mi4 and Mi9); Shinomiya et al. 2019, *eLife*
  8:e40025 (T5 inputs Tm1, Tm2, Tm4, Tm9, compared with T4); Strother et al. 2017, *Neuron* 94:168
  (the functional roles of the T4 inputs). I am confident of the first three. Of the Strother
  citation I am sure of the paper but not of the page number.
- **Why all four directions together:** T4a–d and T5a–d are four copies that differ by the layer
  of the lobula plate they project to. Knock out T4d alone while T4a–c stay, and a rule can regrow
  it by copying a sibling. The same holds for the mirror: knock out ON alone, and OFF stays as a
  template. Removing both halves and all directions leaves no copy of the block in training. (A
  single-direction slice, every cell touching T4d or T5d, is 116 cells and 9 B pairs. It is kept
  out. At most it could serve as a positive control that a copy is regrown.)
- **Risk 1: thin endpoints.** Outside the block, T4a–d and T5a–c keep only 1–4 pairs each in B (inputs plus outputs: T4a 4, T4b 3, T4c 2, T4d 1, T5a–c 1 each, and for T4d and T5a–c the one pair is the self-loop; corrected after review by Ark, Johnny and Zcode),
  and **T5d keeps none**, so T5d leaves training entirely. The eight input types keep 1–12 outputs
  each outside the block. The registration scores T5d's 8 cells as their own stratum.
- **Risk 2: FlyWire typing.** The T4/T5 subtype labels and the Tm/Mi labels in FlyWire may lean on
  connectivity (ADR-005, agreed point 5; unverified). Part of the block's content could then be
  true by definition.
- **Risk 3: the author knows the answer.** This segregation is textbook. The rule must be fixed
  and committed before the block is removed: an existing rule (BF_r at the registered rank) or a new
  rule written without reference to this block.

### B. Lamina outputs, L1–L5 into the medulla and lobula

- **Removes:** every cell from a lamina monopolar cell to a non-lamina, non-photoreceptor type
  (5 × 23 = 115 cells). L→L cells and every cell into L1–L5 stay.
- **Biology:** the split into ON and OFF begins here. L1 feeds the ON side (Mi1, Tm3), L2 the OFF
  side (Tm1, Tm2, Tm4), and L3 feeds Mi9, Tm9 and Tm20. The lamina is the input stage of both motion
  pathways.
- **Sources:** Meinertzhagen & O'Neil 1991, *J Comp Neurol* 305:232 (lamina synapses); Takemura
  et al. 2013 (above); Takemura et al. 2015, *PNAS* 112:13711 (the medulla's seven-column
  circuits and how they vary across columns).
- **Risk:** this is almost a whole-row knockout. The block holds 28 of the 33 B pairs whose source
  is an L type. What stays in training are the L columns, and these are thin because R1–R6 are not
  among the 30 types. A factor rule that does not tie a type's inputs to its outputs has nothing to
  place the L rows with. So "no grammar" and "no information" would be read from the same failure.

### C. The colour path: R7/R8 outputs

- **Removes:** every cell from R7 or R8 to a non-photoreceptor type (2 × 28 = 56 cells).
- **Biology:** R7 and R8 bypass the lamina and end in the medulla, on the colour path (Tm20, Mi1,
  Mi4 and Mi9 from R8; Tm5 and Dm8 from R7, but those two types are not among the 30).
- **Sources:** Takemura, Lu & Meinertzhagen 2008, *J Comp Neurol* (medulla input terminals; I am
  unsure of the volume and page); Gao et al. 2008, *Neuron* (Tm5, Tm20, Dm8 and spectral preference);
  Karuppudurai et al. 2014, *Neuron* (one of the bank's own sign citations).
- **Risk: too small and too noisy.** 4 B pairs, 2.4 % of the bank. R7 and R8 are the two types
  missing from the most FlyWire columns (137 and 142 of 796; column test, §2.3). A block of 4
  positives cannot beat within-fly noise, so the verdict would be "unclear" by design.

## 3. The three anchors the reviewers agreed

1. **The held-out block is measured on B's representation**, the averaged 165-pair bank, and not on
   a single fly's wiring. The target for each removed cell is its value in B.
2. **The noise scale.** One FlyWire column differs from B by a median of **34 extra and 27 missing
   pairs** (column test, verdict line). A median of **0.54** of a column's extra pairs fall in
   flyvis-30 (`X_c`, §3.9), and a single column's containment in flyvis-30 is 0.89 against the
   bank's 0.96. A regrown block must be judged against this within-fly noise. The registration
   needs a noise ceiling for the block: each column's E_c restricted to the block's cells, scored
   against B with the same metric. Its median over the 796 columns is fixed as a procedure now and
   computed only in the run. Spread evenly, 61 differing cells out of 900 would put about 4 in a
   64-cell block. The 0.54 already shows that the noise is not spread evenly, so this estimate is
   not a cut. The registration then has three branches:
   - the rule beats N1, the shuffles and the permuted block: the rule **regrows** the block;
   - the rule does not beat N1, and the noise ceiling is itself close to N1: the block is **too
     noisy to decide**, meaning the rule is weaker than within-fly noise, or the noise is all there
     is;
   - the rule does not beat N1, and the noise ceiling is well above N1: **no grammar** for this
     block.

   The cuts between these branches are registered before data.
3. **The permuted block** (Zcode): the block's cell contents are randomly permuted within the block,
   so the count stays 32 of 64 and the ON/OFF segregation is destroyed. Its result is **expected near
   the in-F calibration Δ of −0.003 to −0.005** (column test, §3.8, `q_F` = 30–40 %). If the rule
   regrows the permuted block as well as the real one, the rule is smoothing, not generating
   (ADR-005, agreed point 6).

## 4. What was counted, and in what order

Candidate A was chosen, and the other two named, from the literature above. The table in §2 was
counted after that. The counts came from the (src, tar) names of B's offsets file (outside the
repository, `connectome-seed-data/FlyWire/derived/flywire_ol_right_30_offsets.csv`) and from the
names in `results/genome/bank/type_pairs.csv`. No `n_syn` column was read. Two more counts were taken
for A's risk: each endpoint type's number of B pairs outside the block, and the same for R7, R8 and
L1–L5. These are also counts of name-rule selections. They revealed that A's content is fully
segregated and that T5d has no entries outside A. Neither changed the recommendation.

## 5. Recommendation: A, the motion-input rectangle

- **It has a structure to regrow, not only a density.** Half its cells are present and half absent,
  and the absent half is biologically meaningful. So a rule can be scored on discrimination, and
  the permuted-block null can destroy exactly the structure being claimed.
- **It leaves no copy of itself.** All directions and both polarities are removed, so neither
  direction symmetry nor ON/OFF mirroring can regrow it trivially.
- **Its endpoints stay visible,** except T5d, which is named and scored separately. So a failure
  can be read as "no grammar", which B cannot offer.
- **It is the best-documented block in the fly optic lobe,** from several independent EM volumes
  (FIB-19 and FIB-25 via Takemura 2013, 2015 and 2017 and Shinomiya 2019, and now FlyWire). It is
  large enough (32 B pairs, 19.4 %) to be measured against within-fly noise, which C is not.

What the registration still has to fix: the metric and the three branch cuts of §3; whether the
primary bank is B or flyvis-30 (the name rule gives 32 of 64 in both); how T5d's stratum is
reported; and which rule is run. Other known T4/T5 inputs are outside the block by definition: C3
is among the 30 and its cells into T4/T5 stay in training; CT1 and TmY15 are not among the 30. The
registration says so.

## Review and decision (2026-09-24 20:22-20:39 UTC, DPC Research chat)

- Reviewed by Ark, Johnny and Zcode; all counts above were recomputed three times from the bank
  files by name. The board is perfect (16 + 16, no cross cells) in FlyWire-30, flyvis-30 and
  flyvis-65 (Zcode).
- **Block A is kept.** The rule is learnable and reads no type names: names are the answer key,
  so a rule that reads them makes the test circular (Johnny, Zcode; Ark's proposal of a name
  channel was declined).
- **The N1 leg is uninformative on this block, in both directions:** for any additive score
  `a_s + b_t` the parity contrast (ON×T4 + OFF×T5) − (ON×T5 + OFF×T4) is identically zero (Ark's
  algebra, `harness.py:350-356`; Johnny's reading of its sign). The 99 shuffles and the permuted
  block are the legs that separate.
- **Mirror cells:** the transposes (T4a,Mi9), (T4b,Mi9), (T4c,Mi9) stay in training on B (five on
  flyvis-30); they are counted on the chosen bank and printed on their own line (Ark).
- **Ceiling:** the rule trained on the full bank and scored on the block; the column numbers 34/27
  are printed apart, as within-fly variation (Ark, Johnny, Zcode).
- **Inferability before data:** on FlyWire-30 only 14 of 64 block cells are inferable (a source
  with at least 2 training targets and a target with at least 2 training sources), against 64 of
  64 on flyvis (Johnny). The chosen bank's inferability table is printed before data.
- **Mike's decision, 20:39 UTC: flyvis-65 is the primary bank.** The Janelia male CNS v1.0 (one
  male, CC-BY; `connectome-seed-data/Janelia/`) replaces FlyWire-30 as the animal control; its
  bank needs its own reviewed builder. FlyWire-30 is kept as provenance.

