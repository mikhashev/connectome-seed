---
**Status:** NOTE, descriptive. It registers nothing and decides nothing. Written by CC (subagent),
2026-09-23 UTC (evening; 2026-09-24 local, +07:00), on Mike's word in the DPC Research group chat
(2026-09-23 18:30 UTC, as relayed by CC). **Read and write only:** no run, no fit and no registration
was made for it.
**Method.** Every claim is marked by how it is known. **Observed**: the author read the file, the
code or the paper text (full text from PubMed Central, eLife or the publisher's supplement,
downloaded this session). **Snippet**: known only from an abstract, a search result or a page
summarised by a fetch tool. **Inferred**: the author's conclusion from observed items. Counts from
the json were recomputed this session with the venv's Python. No loss, activity or checkpoint value
appears here.
**Date note.** The chat times cited here (18:00–18:30 UTC) fall on 2026-09-23 UTC. At the time of
writing the UTC clock read 2026-09-23 18:47 (**Observed**, `date -u`), so they cannot be on
2026-09-24 UTC. The request named this file `2026-09-24-…`; it is dated by its UTC day, as the
[glossary's date-time convention](../../GLOSSARY.md) requires.
---

# Where our bank comes from

**Short answer.** The bank `flyvis/connectome/fib25-fib19_v2.2.json` is **not** the hemibrain. It
was assembled by the flyvis authors (Lappalainen et al., Nature 2024) from two Janelia FIB-SEM
optic-lobe volumes, **FIB-25** (Takemura et al. 2015) and **FIB-19** (Shinomiya et al. 2019). These
are **two different female flies**. The lamina part comes from an earlier hand-built model. The
local reconstructions were turned into **column-averaged, type-level mean synapse counts per
offset**, merged across the two volumes, pruned, edited by hand in a few places, and tiled over a
hexagonal lattice. So the bank is a **consensus template of one circuit**. It is not the wiring of
one animal, and it holds no per-neuron weights.

## 1. Which datasets

### 1.1 What flyvis says it used

**Observed**, Lappalainen et al. 2024, Methods, "Construction of spatially invariant connectome
from local reconstructions" (PMC11525180):

> "The original data stem from focused ion beam scanning electron microscopy datasets from the
> FlyEM project at Janelia Research Campus. The FIB-25 dataset volume comprises seven medulla
> columns and the FIB-19 dataset volume comprises the entire optic lobe and, in particular,
> detailed connectivity information for inputs to both the T4 and T5 pathways. The data available
> to us consisted of 1,801 neurons, 702 neurons from FIB-25 and 1,099 neurons from FIB-19."

**Observed**, Supplementary Note 2 (the publisher's supplementary PDF, `41586_2024_7939_MOESM1_ESM.pdf`):

> "Since neither FIB-19 nor FIB-25 contain the connections of the ommatidia or first neuropile,
> the lamina [89, 90], we reused and refined the existing hand-crafted model from our previous
> work [91], which is based on data from Rivera-Alba et al. [92] and Tuthill et al. [93, 94]."

Here [91] is Tschopp, Reiser & Turaga 2018 (arXiv 1806.04793), [92] is Rivera-Alba et al. 2011
(Curr. Biol.), and [93, 94] are Tuthill et al. 2013 and 2014 (Neuron). **Observed**, the
supplement's reference list.

### 1.2 The two volumes

| | **FIB-25** | **FIB-19** |
|---|---|---|
| Paper | Takemura S. et al., "Synaptic circuits and their variations within different columns in the visual system of *Drosophila*", *PNAS* 112:13711–13716, **2015** (PMC4640747). The same volume is analysed further in Takemura et al., *eLife* 6:e24394, **2017**. | Shinomiya K. et al., "Comparisons between the ON- and OFF-edge motion pathways in the *Drosophila* brain", *eLife* 8:e40025, **2019**. |
| Region | **Seven medulla columns**, "a central 'Home' column and its six immediate neighbors" (2015). The volume holds no lobula: the 2019 paper says these seven-column reports "failed to identify the lobula". | Methods: "a stack of 8 nm voxel cubes covering the central part of the medulla, lobula, and lobula plate, together with the second optic chiasm". The abstract says "a single EM dataset covering the entire optic lobe". It contains no lamina (Lappalainen, Supplementary Note 2). |
| Volume | "a 40 × 40 × 80-μm volume at an isotropic resolution of 10 nm per pixel" (2015) | "153 μm x 85 μm x 180 μm" |
| Imaging | FIB-SEM, Zeiss NVision, 10 nm isotropic | FIB-SEM, Zeiss NVision, 8 nm voxels |
| Flies | **One**: "The seven columns analyzed in this study are all from a single WT fly" (2015) | **One**: "the right eye and optic lobe of a 6-day post-eclosion female fruit fly" |
| Strain | "an adult Canton-S WT fly, between 5 and 6 d posteclosion" (2015) | "a cross between homozygous w1118 and CS wild type" |
| Sex | **Not stated** in the 2015 main text (its SI was not read). **Stated as female** in Takemura et al. 2017 for the same seven-column volume: "The heads of wild-type Canton-S female flies between 5 and 6 days post-eclosion were fixed…", and "These seven columns have been partially analysed elsewhere (Takemura et al., 2015)". | **Female**, stated |
| Data | "ID code FIB-25", Janelia FlyEM data release (2015) | "fib19-grayscale", `http://emdata.janelia.org/optic-lobe/` (2019 data citation) |

Everything in the table is **Observed** in the named paper. That the 2015 and 2017 papers describe
the same animal is **Inferred**, from the identical volume size, the identical seven columns and
the 2017 sentence quoted above.

**A discrepancy, recorded rather than resolved.** Lappalainen's Methods say FIB-19 "comprises the
entire optic lobe". Shinomiya's own Methods say "the central part of the medulla, lobula, and
lobula plate", and Lappalainen's Supplementary Note 2 says FIB-19 lacks the lamina. **Observed**,
all three texts.

**So, in plain numbers.** The bank rests on **at least two flies**, both female. One was Canton-S;
the other was w1118 × Canton-S. The lamina part rests on other sources. The flyvis authors had
**1,801 neurons** from the two volumes. The hemibrain has about 25,000 neurons. **Observed.** The
sex and number of flies behind the lamina model (Rivera-Alba 2011, Tuthill 2013/2014) were
**not checked**.

## 2. How flyvis turned them into the 65-type, 605-entry, hex-lattice template

### 2.1 Column positions and fusion of the two volumes

**Observed**, Lappalainen Supplementary Note 1:

- Only about 830 of the 1,801 neurons had hand-annotated columns. An expectation-maximisation
  algorithm placed the rest. It used "synaptic connection statistics, projected synapse
  center-of-mass clusters and existing column annotations".
- The two volumes were evaluated separately. Then, for each source type *s*, target type *t* and
  offset *(y, x)*, the fused value takes **the larger of the two estimates**:
  "μ_{s,t,(y,x)} = max(μ^{FIB-19}, μ^{FIB-25})" (their equation 7).
- Pruning: "We imposed the following additional filter on our estimated model parameters, to
  remove both autapses and spurious connections with less than one synapse on average." Their
  equation 8 conditions on `s = t ∧ (y, x) = (0, 0)` and on `μ < 1`; its right-hand side did not
  survive text extraction, and "set to zero" is **Inferred** from the sentence. Also: "The
  resulting mean synapse counts μ_{s,t,(y,x)} form the convolutional filters for our simulation."

### 2.2 Averaging over columns: what `n_syn` is

**Observed**, Lappalainen Fig. 1e legend: the values "represent the average number of synapses
projecting from presynaptic Mi9 cells in columns with indicated offset onto the postsynaptic
dendrite of T4d cells". Main text: "By this assumption of translation invariance due to periodic
tiling, the synapse count between each pair of neurons was the same across all pairs of neurons
with the same presynaptic and postsynaptic cell type and relative location in retinotopic space."

So each json offset row `[[du, dv], n_syn]` holds **one mean**, taken over reconstructed
postsynaptic neurons of the target type, of the synapses they receive from the source-type neuron
at that offset. **Inferred** from the legend and equation 7. This is why most values are not
integers.

**Zcode's count, verified.** Of the **2,140** offset rows in the json, **1,645** have a
non-integer `n_syn`; the other 495 are integer-valued. **Observed**, recomputed this session. (By
Python type there are 1,649 floats and 491 ints; four of the floats have integer values.) By
entry: 313 of the 605 json entries have only non-integer rows, 145 only integer rows and 147
mixed. Values run from 0.0447 to 144.09. **Observed.**

**The rows below 1 come from later hand edits.** Equation 8 prunes means below 1, yet
**200 rows** in the json are below 1. They sit in **20 entries**, all targeting TmY15 or a T4/T5
subtype (TmY15 75 rows; T4a–d 67; T5a–d 58). **Observed.** Supplementary Note 2, "Additional
proofreading", describes two edits after the pipeline. **Observed:**

> "…did not fully capture the asymmetry reported in [90] of the T5 anatomical receptive field of
> Tm9, which we then substituted by a Gaussian at the reported offset column scaled by the
> reported number of input synapses. For few T4 and T5 inputs the number of input synapses
> reported in the literature[90] slightly deviated from our reconstruction. To get a better
> initialization of our filter scale we scaled them to closely match the number of input synapses
> reported[90]."

That these edits produced the sub-1 rows is **Inferred**; the note does not say which entries
were rescaled. There are no self-offset rows at (0, 0) in the json (0 found, **Observed**), which
agrees with the autapse rule.

### 2.3 The offsets (du, dv) and the lattice

- **Offsets.** Each json entry lists `[[du, dv], n_syn]` rows: 2,140 rows over 605 entries, 1 to
  26 per entry, with no |du| or |dv| above 6. **Observed**
  (`docs/notes/2026-09-20-what-is-the-genome-here.md` §2, reproduced this session).
- **Tiling.** `add_conv_edges` (`flyvis/connectome/connectome.py:473-499`) connects every source
  node at `(u, v)` to the target node at `(u + du, v + dv)`, giving every edge instance the entry's
  one `n_syn`. A missing target is skipped silently (`with suppress(KeyError)`). **Observed.**
- **Extent.** `add_strided_nodes` (`connectome.py:326-343`) fills a hexagonal disc of radius
  `extent` (15 by default, `config/network/connectome/connectome.yaml`). That gives 721 nodes per
  stride-[1, 1] type and 123 per Lawf type: 63 × 721 + 2 × 123 = **45,669** nodes. **Observed**
  (code and arithmetic). Lappalainen: "2D hexagonal arrays 31 columns across". The Lawf strides
  are inferred, not measured: "we modeled them with an inferred spatial stride … resulting in 123
  cell of each type in our model" (Supplementary Note 2). **Observed.** A real eye has about 800
  columns: Matsliah et al. 2024 put "the true number of columns in this optic lobe" at the top of
  a 720–800 range. **Observed.** So the extent is a lattice parameter, not a count of columns in
  a fly.
- **CT1.** One cell per optic lobe, modelled as two types: "we modelled CT1 as two anatomically
  separate cell types CT1(Lo1) and CT1(M10)" (Supplementary Note 2). **Observed.** Hence
  Lappalainen's "64 cell types" in the text and the 65 in the json ("counting CT1 twice for the
  compartments in the medulla and lobula", Methods). **Observed.**

### 2.4 `n_syn_fill`: the hull fill

`add_edges` (`connectome.py:403-432`) calls `fill_hull` for every entry with **three or more**
offset rows. Every lattice point inside the convex hull of the reported offsets that is not already
listed is added with `n_syn = n_syn_fill`, which is **1** by default (`connectome.py:435-470`).
**Observed.** In the compiled bank this adds 238 rows (`hull_filled`), all of which land
(`results/genome/bank/README.md`). **Observed.** Lappalainen, Supplementary Note 2: "the convex hull
of the filters is filled with ones to remove spatial discontinuities. Although these are considered
mostly false positives from the connectome reconstruction [97], this allowed for weak autapses in
our hexagonal model that did not affect the tuning predictions." Reference [97] is Scheffer et al.
2020, the hemibrain paper. **Observed.** **That citation is the only place the hemibrain appears in
the provenance of this bank that this note found.**

### 2.5 `n_syn` inside the network

`SynapseCount` (`flyvis/network/initialization.py:422`) groups compiled
edges by `(source_type, target_type, du, dv)` and takes their mean `n_syn`. That returns the json
value, because every instance of a row carries the same number. It is fixed:
`requires_grad: false` in `config/network/edge_config/syn_count/syn_count.yaml`.
`SynapseCountScaling` sets each pair's initial trainable strength to `0.01 / ⟨n_syn⟩`, the mean
over the pair's offsets (their equation: α = ρ / ⟨N⟩). **Observed.** The 604 trainable scalars are
**one per compiled type pair**, shared by every edge instance of that pair
(`docs/notes/2026-09-20-what-is-the-genome-here.md` §1). **Observed.**

The edge field `lambda_mult` is read and stored as `n_syn_certainty` (`connectome.py:431`,
`:499`). No other module of flyvis 1.2.0 reads it. **Observed** (grep over the package).

### 2.6 The sign source

- **The paper.** "Synaptic signs for most cell types were predicted on the basis of known
  expression of neurotransmitter markers (primarily the cell-type-specific transcriptomics data
  from ref. 30). For a minority of cell types included in the model, no experimental data on
  transmitter phenotypes were available. For these neurons, we used guesses of plausible
  transmitter phenotypes." Ref. 30 is Davis et al. 2020, *eLife* 9:e50901. Histamine, GABA and
  glutamate were treated as hyperpolarising and acetylcholine as depolarising. R8 outputs were
  split by whether the target expresses `ort`. **Observed**, Methods.
- **The json.** `alpha` is +1 on 377 entries and −1 on 228. `alpha_fixed` is true on **272**
  entries, and every one of them carries `alpha_references`. The keys cited are `NernPC2018` (286
  slots), `ReiserPC2017` (82), `Hardie1989` (40), `Karuppudurai2014` (12) and `Lin2016` (12).
  **Observed**, recomputed. Most of these are personal communications; the counts are in
  `results/genome/bank/README.md` § "Warning: most sign citations are personal communications".
  **No json entry cites Davis et al. 2020 by key.** **Observed.** How the paper's transcriptomic
  rule maps onto the json's per-entry references is not stated in either place.
- The sign is **per compiled type pair** and fixed during training (`edges_sign`,
  `docs/notes/2026-09-20-what-is-the-genome-here.md` §1). It was not measured in either EM
  volume. **Observed.**

## 3. What the bank therefore is, and is not

**It is** a type-level, column-averaged, translation-invariant template of one optic-lobe circuit:
the motion pathways from photoreceptors through lamina and medulla to lobula and lobula plate. It
covers 65 model types and 605 json entries, each a set of mean synapse counts per hex offset with
one sign. It was built from two female flies' partial reconstructions, merged by taking the maximum
estimate, pruned, edited by hand for Tm9 → T5 and some T4/T5 inputs, and completed with a
hand-built lamina model. **Inferred** from §1–§2.

**It is not:**

- **the hemibrain.** The hemibrain "covers most of the right hemisphere of the brain, except the
  optic lobe (OL)…" and "Neurons that arborize only in the optic lobe are not classified, except
  for several intrinsic neurons in the lobula"
  (Scheffer et al. 2020, *eLife* 9:e57443). **Observed.** Its only role in this bank's provenance
  is the citation in §2.4.
- **one individual.** There are at least two flies, plus literature components. **Observed**
  (§1).
- **raw per-neuron weights.** No row is a synapse count between two identified neurons. Each is a
  mean over neurons and columns, and the model then copies it to every column. **Observed**
  (§2.2–§2.3).

**What "individual variability" can and cannot mean for this bank.** The glossary's
**individual** is a trained flyvis network, not a fly ([GLOSSARY.md](../../GLOSSARY.md), row
"individual").

- **Between trained individuals.** The bank is identical in every one of them. They differ in the
  65 seeded `nodes_bias` values and in data order
  (`docs/notes/2026-09-20-what-is-the-genome-here.md` §3). **Observed.**
- **Between flies.** This bank cannot express it. There is one value per (pair, offset), and the
  two flies are fused by a maximum, not kept apart. **Inferred.** Measuring it needs a second bank
  built the same way from another fly (§5).
- **Between columns of one fly.** The averaging removed it. It was measured for FIB-25's seven
  columns and 20 "modular" types in Takemura et al. 2015 ("comparing the circuits common to all
  seven columns to assess variation in their connection strengths", Datasets S1–S2). **Observed**
  (main text; the datasets were not opened). That is the only per-column variability tied to this
  bank's sources.
- **Between neurons.** It is absent. No per-neuron weight exists in the bank or among the trained
  parameters, which are 604 per-pair scalars. **Observed.**

## 4. Corrections to claims in the group chat, 2026-09-23 UTC

The wording below is as relayed by CC. The author did not read the chat, and the language of the
originals was not checked. Zcode retracted items 3 and 4 at 18:28 UTC (as relayed).

| # | Who, when (UTC) | Claim | Correction |
|---|---|---|---|
| 1 | Ark, 18:00 | "a subset of the hemibrain (Scheffer 2020), one female, ~25,000 neurons" | The bank is built from FIB-25 and FIB-19 (Takemura et al. 2015; Shinomiya et al. 2019), not the hemibrain, which excludes the optic lobe (§1, §3). It rests on at least two female flies, not one. The flyvis authors had 1,801 neurons from the two volumes; about 25,000 is the hemibrain's count (§1.2). |
| 2 | Ark, 18:06 | "we fitted the noisiest part, individual weights" | The bank holds column-averaged mean counts per (type pair, offset), not per-neuron weights (§2.2). What is fitted is 604 per-pair scalars plus 65 biases and 65 time constants; the counts themselves are fixed (§2.5). |
| 3 | Zcode, 18:17 | "bank = one female (hemibrain)" | As item 1: not the hemibrain, and not one fly. Both source flies are female (§1.2). |
| 4 | Zcode, 18:17, plan (b) | "train on hemibrain, test on FlyWire" | The hemibrain leaves optic-lobe-only neurons untyped, apart from several lobula intrinsic types, and holds only "small pieces" of the medulla (§3, §5.1), so it cannot supply this circuit. Candidates that do cover the 65 types' circuit are in §5. |

## 5. A second bank from another fly?

**Question** (Mike, as relayed). Can we get a second, independent bank of the **same 65 types**,
the same optic-lobe columnar circuit from another fly, to use beside or instead of the 99
**shuffled banks**?

### 5.1 The two links Mike gave

- `https://elifesciences.org/articles/57443` is **the hemibrain**: Scheffer L.K. et al., "A
  connectome and analysis of the adult *Drosophila* central brain", *eLife* 2020. One female
  ("a 5-day-old female of wild-type Canton S strain G1 x w1118"), FIB-SEM, "except the optic lobe
  (OL)". It notes that "more than half of the lobula (LO) and small pieces of the lobula plate
  (LOP) and medulla (ME) are within the dataset", but optic-lobe-only neurons are not typed, "except for several intrinsic neurons in the lobula".
  **Observed.** It **does not cover** the columnar types of our bank.
- `https://www.nature.com/articles/s41586-024-07558-y` is **FlyWire**: Dorkenwald S. et al.,
  "Neuronal wiring diagram of an adult brain", *Nature* 634 (2024), PMC11446842. It covers
  "139,255 neurons reconstructed from an adult female *Drosophila melanogaster*", whole brain,
  serial-section TEM (the FAFB volume of Zheng et al.), with "All neurons in the central brain and
  both optic lobes … segmented and proofread". **Observed.** It **covers** the circuit. Its
  optic-lobe typing is Matsliah et al. 2024 (§5.2). The paper itself says: "In previous studies, an
  absence of information across columns has necessitated treating each column as identical in
  simulations of the optic lobe", citing Lappalainen et al. 2024. **Observed.**

### 5.2 Candidate second brains

"1:1 names" counts how many of our 65 json type names appear **with the same spelling as one
type** in the dataset's published type list. **Observed** by a script over our json and the
lists: `left_vs_right_types_*.csv` in `github.com/murthylab/visual-system-parts-list` (FlyWire
v783), and `Nern-et-al_SuppTable01_Cell-types-and-counts.xlsx` in
`github.com/reiserlab/male-drosophila-visual-system-connectome-code` (optic-lobe v1.1). `Am` was
counted as matching `Am1`. A same name does not prove the same type definition; that is
**Inferred** only. "Entries" counts the json entries whose source and target both match.

| Dataset | Sex, flies, method | Region | Per-column assignment | 1:1 names (of 65) | Licence; access |
|---|---|---|---|---|---|
| **Hemibrain v1.2.1** (Scheffer 2020) | female, 1, FIB-SEM | central brain; optic lobe mostly absent | none for optic-lobe types | not applicable: optic-lobe-only neurons untyped, except several lobula intrinsic types | "without restriction, with only the requirement to cite the source" (paper); neuPrint. **Observed** |
| **FlyWire FAFB v783**, right optic lobe (Dorkenwald 2024; Matsliah 2024, *Nature*, PMC11446827) | female, 1, ssTEM | whole brain, both optic lobes, lamina included | **Yes:** "23,452 'columnar' neurons of 31 distinct types … divided into 796 'columns'"; 22,578 assigned (Codex Visual Columns Challenge page). Codex "maps a number of cell types to locations in the hexagonal lattice of columns and ommatidia" (Matsliah). **Observed.** Which 31 types: not checked. | **48**; entries **452/605**, 1,800/2,140 rows, 0.80 of the json's total `n_syn` | Connectivity deposit Zenodo 10676866: **CC-BY-4.0** (**Observed**, Zenodo API); Codex downloads need Google sign-in (**Observed**, Codex page); parts-list repository Apache-2.0 (**Observed**, GitHub API) |
| **FlyWire FAFB v783**, left optic lobe | the **same fly** as the row above | as above | not checked | typing "completed" and "match[es] the right optic lobe" (Matsliah, **Observed**); names not recounted | as above |
| **Male optic lobe, optic-lobe:v1.1** (Nern et al., *Nature* 2025, PMC12119369) | **male**, 1, FIB-SEM ("males from a cross between Canton S strain G1 × w1118") | right optic lobe; lamina "incomplete" with worse completion metrics | **Yes:** hex coordinates (`hex1_id`, `hex2_id`) for **15 types** (L1, L2, L3, L5, Mi1, Mi4, Mi9, C2, C3, Tm1, Tm2, Tm4, Tm9, Tm20, T1) at 920 rows (892 distinct coordinates; 821 rows with all 15), in `params/ME_columnar-cells_location.xlsx`; T4 mapped to Mi1 for lobula-plate columns; column ROIs in neuPrint. **Observed** | **50**; entries **483/605**, 1,916/2,140 rows, 0.83 of total `n_syn` | Cell Type Explorer deposit Zenodo 10891950: CC-BY-4.0 (**Observed**); neuPrint `optic-lobe:v1.1` (**Observed**, Data availability); dataset licence **Inferred** CC-BY from the male CNS page (same specimen); code repository GPL-3.0 (**Observed**) |
| **Male CNS v1.0** (Berg et al., *Cell* 2026) | male, 1: **the same specimen** as optic-lobe:v1.1 ("extends the recent optic lobe connectome from the same specimen") | whole CNS, both optic lobes | not checked | not checked | "The FlyEM Male CNS dataset is licensed under CC-BY"; neuPrint `male-cns:v1.0` (**Observed**, Janelia project page) |
| **BANC v888** (Bates et al., *Nature* 2026) | female, 1, GridTape serial-section TEM | CNS; optic lobes: "the medulla, lobula and lobula plate", but "It lacks the lamina", so R1–R6 and lamina connections are missing | none found in the paper text | not counted. Optic-lobe types: 21.3 % of right and 63.8 % of left proofread optic-lobe neurons "lacked a human-verified cell type" before an alignment step. **Observed** | CC BY 4.0 (repository badge), Harvard Dataverse 10.7910/DVN/7WTH1N; latest reconstruction access "restricted to authorized users". **Observed** |

**Our 15 to 17 names without a one-to-one match.** **Observed**, same script.

- **Both datasets:** R1–R6 (six types here, one type `R1-6` / `R1-R6` there); `CT1(Lo1)` and
  `CT1(M10)` (one cell `CT1` there, so the compartments need a split by neuropil); `Mi3`, `Mi11`,
  `Mi12` and `Tm28` (absent from both lists, and not mentioned in either paper's text); `TmY9`
  (split in two there: `TmY9a`/`TmY9b` in Nern, `TmY9q`/`TmY9q__perp` in FlyWire).
- **Male optic lobe only:** R7 and R8 (each split into `d`, `p` and `y` subtypes).
- **FlyWire only:** `Tm5Y` (FlyWire splits Tm5 into `Tm5a`–`Tm5f`, and which of them corresponds
  was not checked), `Tm30`, `TmY13` and `TmY18` (absent from the FlyWire list).

**Not second flies:** FIB-25 and FIB-19 themselves. Takemura 2015's seven-column per-column counts
give within-fly variation (§3), not a second animal.

### 5.3 What building a bank in our format would take

These are **Inferred** steps. **Nothing here was started.**

1. **A neuron table with type and column.** Our format needs every neuron of a matched type at a
   hex position `(u, v)`. FlyWire's assignment covers 31 columnar types; Nern's covers 15 types
   directly, plus T4 through Mi1 and the lobula through Tm types. The other matched types
   (multi-column Tm/TmY types, Mi2, Mi10, Lawf1/2 with stride [3, 2], and the single cells Am1 and
   CT1) need a rule. Nern already uses a "home column (the column with the largest synapse count)"
   (**Observed**, Extended Data Fig. 6 legend); flyvis used a probabilistic EM (§2.1). The rule
   chosen changes the offsets.
2. **Axis alignment.** Map the dataset's `(p, q)` / `(hex1, hex2)` onto flyvis's axial `(u, v)`
   with the right orientation and handedness. The FlyWire paper notes its "image and dataset are
   mirror inverted relative to the native fly brain" (**Observed**). The flyvis axis convention
   relative to the eye was not checked.
3. **Neuron-to-neuron synapse counts.** These are available (FlyWire
   `proofread_connections_783.feather`; neuPrint for optic-lobe v1.1). **Observed** (file listing;
   Data availability).
4. **Averaging to our definition.** For each (source type, target type, du, dv), compute the mean
   over target neurons of synapses received from the source neuron at that offset (§2.2). Choose
   whether to average over the whole eye or a central patch like FIB-25's seven columns, since edge
   columns are incomplete. Then drop means below 1 and self rows at (0, 0) (§2.1), and leave the
   hull fill to flyvis at compile time.
5. **Signs.** No EM dataset measures sign. Either copy our json's per-pair `alpha`, or derive signs
   from the dataset's neurotransmitter predictions. Record which.
6. **Unmatched types.** Merge, split or drop the 15–17 names above, and record each decision.
7. **Write the json in the flyvis schema and compile it** with `ConnectomeFromAvgFilters`. Comparing
   it with our bank is then possible only on the matched subset (483 or 452 of 605 entries).

**A confound no second bank removes.** A new bank would differ from ours by fly, sex (Nern: male),
imaging and synapse detection (Takemura 2015 found "about 1.5-fold as many T-bars" with FIB-SEM as
with ssTEM), typing, column-assignment rule, and flyvis's hand edits (§2.2), which would not be
repeated. A difference between the two banks therefore measures **all of these together**, not
between-fly variation alone. **Inferred.** Some pairings hold part of this fixed:

- FlyWire right versus FlyWire left optic lobe: same fly, same method; this isolates the
  hemisphere.
- FlyWire versus male optic lobe: two flies, two sexes, two methods.
- Either of them versus our bank: adds the flyvis pipeline and hand edits.

### 5.4 Verdict and rough effort

- **Feasible, but not as "the same 65 types".** A bank from **FlyWire's right optic lobe** or the
  **male optic lobe** can be built for about **48–50 of our 65 types**, covering about
  **75–80 % of json entries and 80–83 % of the total `n_syn`**. The lamina inputs (R1–R6 as six
  types) and the CT1 compartments do not carry over one to one, and four of our types are absent
  from both catalogues. **Inferred** from §5.2.
- **Best first candidate: FlyWire right optic lobe** (**Inferred**). It is female like our sources,
  has a column assignment for 31 columnar types, has the lamina, and its connectivity is on Zenodo
  under CC-BY-4.0 without sign-in; the column file needs a Codex sign-in. The male optic lobe is the
  better independent-method check but adds sex as a difference and has a weak lamina.
- **Beside the 99 shuffled banks, not instead of them** (**Inferred**). A shuffled bank asks
  whether a rule finds structure that a random rewiring with the same marginals lacks. A second-fly
  bank asks whether what a rule finds survives a change of fly and pipeline. These are different
  questions, and neither answers the other.
- **Rough effort** (**Inferred**; no step was timed):
  - data access: half a day, plus Mike's Google sign-in for Codex or a neuPrint token;
  - column assignment for the types that lack one: 2–4 days;
  - averaging, pruning and writing the json: 1 day;
  - checks (compile, compare structure on the matched subset): 1–2 days.
  - That is **about 1–1.5 weeks for one dataset** and about 2–3 weeks for both. Any use as a
    control needs its own registration first.

## 6. Not verified

- The sex of the FIB-25 fly in Takemura 2015 itself (its SI was not read); the attribution to
  female rests on Takemura 2017 describing the same volume.
- The sex and number of flies behind the lamina model (Rivera-Alba 2011; Tuthill 2013, 2014;
  Tschopp 2018).
- Which json entries the flyvis authors rescaled or replaced (the supplement names Tm9 → T5 and
  "few T4 and T5 inputs" only).
- How the paper's transcriptomic sign rule maps onto the json's per-entry references.
- The licence text of the neuPrint `optic-lobe:v1.1` dataset itself, and the list of FlyWire's 31
  column-assigned types.
- Column assignment and optic-lobe typing in the male CNS left optic lobe and in BANC.
- Whether `Mi3`, `Mi11`, `Mi12`, `Tm28`, `Tm5Y` (FlyWire), `Tm30`, `TmY13` and `TmY18` (FlyWire)
  exist under other names in those datasets.
- The chat wording in §4, which was relayed, not read.

## Sources

- Lappalainen J.K. et al., *Nature* 634 (2024), doi 10.1038/s41586-024-07939-3; PMC11525180;
  supplementary information `41586_2024_7939_MOESM1_ESM.pdf` (Supplementary Notes 1–2).
- Takemura S. et al., *PNAS* 112:13711 (2015), PMC4640747.
- Takemura S. et al., *eLife* 6:e24394 (2017).
- Shinomiya K. et al., *eLife* 8:e40025 (2019).
- Scheffer L.K. et al., *eLife* 9:e57443 (2020).
- Dorkenwald S. et al., *Nature* 634 (2024), doi 10.1038/s41586-024-07558-y; PMC11446842.
- Matsliah A. et al., *Nature* (2024), doi 10.1038/s41586-024-07981-1; PMC11446827;
  `github.com/murthylab/visual-system-parts-list`.
- Nern A. et al., *Nature* (2025), doi 10.1038/s41586-025-08746-0; PMC12119369;
  `github.com/reiserlab/male-drosophila-visual-system-connectome-code` (`params/`).
- Janelia FlyEM, Male CNS Connectome project page (`janelia.org/project-team/flyem/male-cns-connectome`).
- Bates A.S. et al., *Nature* (2026), doi 10.1038/s41586-026-10735-w; PMC13518251;
  `github.com/htem/BANC-project`.
- Codex (`codex.flywire.ai`), Visual Columns Challenge page; Zenodo records 10676866 and 10891950.
- flyvis 1.2.0 in `tools/.venv/Lib/site-packages/flyvis/`: `connectome/connectome.py`,
  `connectome/fib25-fib19_v2.2.json`, `network/initialization.py`, `config/network/`.
