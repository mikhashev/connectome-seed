# Literature — what exists, verified how

Searched 2026-09-13 on Mike's word («поищите работу — может кто уже решил этот вопрос; может
есть что-то похожее из решённых проблем из других областей — кодеки, материаловедение»).
Every entry says **how far it was read**. Quotes are verbatim from the source named; nothing
below is from a retelling. Where a source refused the fetch (paywall, cookie wall, rate
limit) that is written down rather than papered over.

Reviewed 2026-09-13 by Johnny ([chat/81](chat/81-johnny-063942.md)) and Ark
([chat/82](chat/82-ark-064101.md)); their corrections are applied in place and each is
marked with the reviewer's name where it lands. Applied on Mike's word
([chat/83](chat/83-mike-064218.md)).

Read status: **full text** = text extracted and read · **abstract** = abstract page read ·
**paywalled** = not read; cited only through an open copy or not cited for detail.

---

## A. The question itself, in three other fields

### 1. Codecs — the genome *is* a codec, and this has been done numerically
**Shuvaev S., Lachi D., Koulakov A., Zador A. — "Encoding innate ability through a genomic
bottleneck", PNAS, received 2024-05-17, accepted 2024-08-04.** Open-access PDF saved to
[sources/](sources/shuvaev-2024-genomic-bottleneck-pnas.pdf). **Full text.**

The framing, verbatim: *"we formulate the problem of innate behavioral capacity in the context
of artificial neural networks in terms of lossy compression of the weight matrix."* Mechanism:
*"The input to the genomic network ('g-network') is a pair of neurons (pre- and postsynaptic)
specified by binary strings … The output of the g-network is the expected strength of the
connection between these neurons."* — i.e. a decoder; the phenotype's weights are generated,
not stored.

Numbers, verbatim:
- *"the g-network was able to achieve **322-fold** compression while maintaining innate
  performance almost equal to that of the fully trained network"* (MNIST, 94 % on init);
  *"a good innate performance of 79% correct could even be achieved using the GN5, a network
  with **1,038-fold** compression."*
- CIFAR-10: *"GN50, a network with **92-fold** compression, achieved initial performance of
  76%."*
- Transfer CIFAR-10 → SVHN: *"the performance of g-network mediated transfer was
  indistinguishable from the standard approach … even though in this case the number of
  transferred parameters was **92 times fewer**."*
- Another task: *"compressed the p-network **492-fold** … innate performance … remained
  excellent up to about **3,500-fold** compression."*

The result that cuts against the idea's point 4 — **p. 4, Fig. 3E** (located by Ark, 2026-09-13;
re-verified here in the PDF): *"To our surprise, genomic compression did not affect the
learning trajectory; the only speedup was due to the higher initial performance, as though the
p-network was 'hot-started' by the g-network."* And the paper's own qualifier one sentence
later: *"Thus genomic compression, at least under these conditions, did not affect the learning
rate."* And one that cuts for it: *"solutions obtained
from p-networks initialized by g-networks did not appear to engage in reward hacking."*

**Why it matters here — narrowed after review (Ark, 2026-09-13):** what is closed is the
**storage half** of requirement 1 — *ids → weights, 322×* — not a grammar that *grows*. The
paper calls its decompression *"a process analogous to neural development"* (p. 9): an
analogy, not morphogenesis — no growth, no body, no differentiation in time.

And keying the g-network on **cell type** instead of neuron id, which the first version of this
file proposed as "the typed grammar the thread asked for", **pays in resolution**: the input
is *"log₂ N binary tags to specify each neuron uniquely"* and the genome size *"scales as
H log N"* (p. 9). Replace the unique tag by a type and every neuron of a type becomes
interchangeable — the generated connectome is a **type → type block model**, and within-type
specificity (the very thing the male/female FlyWire comparison exists to see) is gone. To keep
both, the label has to be (type + developmental coordinate), and then the grammar owes an
account of where the coordinate comes from. The original problem returns. See §F for the
second, larger collision.

### 2. Materials / chemistry — validity by construction
**Krenn M., Häse F., Nigam A., Friederich P., Aspuru-Guzik A. — "Self-Referencing Embedded
Strings (SELFIES): A 100% robust molecular string representation", Machine Learning: Science
and Technology, 2020; arXiv 1905.13741.** **Abstract.** Code: aspuru-guzik-group/selfies.

Verbatim: *"the standard strings molecular representation SMILES shows substantial weaknesses …
large fractions of strings do not correspond to valid molecules. Here, we solve this problem at
a fundamental level … Every SELFIES string corresponds to a valid molecule, and SELFIES can
represent every molecule."*

**Why it matters here:** Johnny's objection 1 and Ark's requirement 5 — "any graph is valid,
there is no cheap oracle" — is the exact problem chemistry had with SMILES under mutation, and
it was solved by moving validity **into the decoder**, not into the fitness function. USPEX
itself (Oganov) is the other materials-science piece and was already in the idea.

### 3. Robotics — encodings compared, none dominates
**Miras K. — "Constrained by Design: Influence of Genetic Encodings on Evolved Traits of
Robots", Frontiers in Robotics and AI, 2021 (PMC8239187).** **Abstract + findings.**

CPPN vs L-system on the same robots: CPPN robots *"often have a 'spider' shape and are
relatively slow, but present very coordinated and stable gaits"*; L-system robots *"often have
a 'snake' shape and are much faster, but present exceedingly uncoordinated and unstable
gaits."* No encoding wins; each imposes its own bias.

**Why it matters here:** Ark's diagnosis — compression, composability, expressivity pull apart
— confirmed on real evolved robots, not argued.

---

## B. Already done on the fly

### 4. The seed circuit, built and public
**Lappalainen J. et al. — "Connectome-constrained networks predict neural activity across the
fly visual system", Nature 634, 1132–1140 (2024); bioRxiv 2023.03.11.532232.** Nature full text
**paywalled**; bioRxiv **abstract** read; code TuragaLab/flyvis (readme read).

Abstract, verbatim: *"We can now measure the connectivity of every neuron in a neural circuit,
but we are still blind to other biological details, including the dynamical characteristics of
each neuron."* The model wires **64 cell types** of the optic-lobe motion pathways from
connectome data, optimises the unknown single-neuron and synapse parameters on a
motion-detection task, and its predictions *"agreed with experimental measurements of neural
activity across 24 studies."* Direction selectivity and ON/OFF channels are predicted. The
names T4/T5 are not in the abstract; what the abstract does say is *"64 cell types in the
**motion pathways** of the fruit fly optic lobe"*, and T4/T5 are the direction-selective
cells of exactly that pathway — so the link holds **at circuit level** (Ark, 2026-09-13),
while the names themselves remain from the Nature summary.

**Why it matters here:** this is the circuit Ark proposed as the one-run falsifier (write T4/T5
into the grammar, splice two copies, check the behaviour is predictable). It is already
written, already task-optimised, already on GitHub. The falsifier starts from here.

### 5. Connectome as the controller of a body
**Jin Z., Zhu Y., Zhang C., Sui Y. — "Whole-Brain Connectomic Graph Model Enables Whole-Body
Locomotion Control in Fruit Fly", arXiv 2602.17997, v1 2026-02-20, final 2026-06-14.**
**Abstract.**

Verbatim: *"we introduce the Fly-connectomic Graph Model, which directly instantiates the
whole-brain connectome of an adult Drosophila as a graph-structured neural controller for
movements of a simulated biomechanical fruit fly via deep reinforcement learning."* Which
connectome release and the neuron count are **not in the abstract**.

**Why it matters here:** the idea's "fly → body" is not a hypothesis to test; it is the
starting point someone else already reached.

### 6. A codec over FlyWire subgraphs
**Li Y., Liu X., Chen G. — "Unveiling and Steering Connectome Organization with Interpretable
Latent Variables", arXiv 2505.13011, 2025-05.** **Abstract.**

Verbatim: *"combines subgraph extraction from the Drosophila connectome, FlyWire, with a
generative model to derive interpretable low-dimensional representations of neural circuitry
… the ability to manipulate these latent codes to controllably generate connectome subgraphs
with predefined properties."*

---

## C. The two 2026 papers on requirement 2 and on "youth"

### 7. Modules through a bottleneck
**Hamidi M., Khajehabdollahi S., Wu C. M., Giannakakis E. — "Distilling a Modular Reservoir
Through a Genomic Bottleneck", arXiv 2606.28380, 2026-06-20.** **Abstract.**

Verbatim: *"we use hypernetworks to learn a compressed generative process that generates the
connectivity of a modular reservoir"*; the emerging connectivity *"already equips the organism
with functional modules upon birth"*; the networks *"solve difficult temporal tasks with
minimal training and without concessions to robustness."*

**Why it matters here:** modules and a bottleneck in one representation — requirement 2
(composability), first approximation. Whether the modules are *cuttable and re-attachable*
between two genomes is not claimed in the abstract.

### 8. Youth as a heritable parameter
**Medvid S., Valenia A., Glybovets M. — "Activity-Dependent Plasticity in
Morphogenetically-Grown Recurrent Networks", arXiv 2604.03386, v1 2026-04-03, rev
2026-06-15.** **Abstract.**

Verbatim: *"We characterise Hebbian and anti-Hebbian plasticity across **50,000**
morphogenetically grown recurrent controllers (5M+ configurations on CartPole and Acrobot),
then test whether co-evolutionary experiments — where plasticity parameters are encoded in the
genome and evolved alongside the developmental architecture — recover these patterns."*
Findings: anti-Hebbian beats Hebbian for competent networks (Cohen's d 0.53–0.64); *"regret …
reaches 52–100%"*; *"plasticity's role shifts from fine-tuning to genuine adaptation under
non-stationarity."*

**Why it matters here:** the idea's "youth" as a fixed step becomes an evolved parameter — the
strengthening the idea's own reviewer suggested — and the regret number says a fixed youth
setting loses most of what an adaptive one gains.

---

## D. The counterexample both critics cited — read at source, and it is two-sided

**Mertan A., Cheney N. — "Evolutionary Brain-Body Co-Optimization Consistently Fails to Select
for Morphological Potential", arXiv 2508.17464, v1 2025-08-24, v2 2026-08-12.** Abstract and
**full HTML text** read.

Note the title: the thread quoted it as "…to Select Near-Optimal Solutions"; that is not the
title.

Against the idea — verbatim, with section: *"it requires more controller optimization to
estimate their fitness well"* (§3.1); *"algorithms are likely to undervalue new individuals
with newly mutated morphologies due to significant negative transfer"* (§4.2);
*"morphologies that are selected in an uninformed way early in evolution accrue more controller
optimization"* (§6, the first-mover dynamic). Their exhaustive map trained a controller for
each of **1,305,840** morphologies with *"300 generations of age-fitness Pareto optimization
with a population size of 20"* (§3, Table 1) — that is the **landscape-construction** budget.
The co-optimisation experiments themselves run **10,000 generations** (§4.1; Johnny,
2026-09-13, read at source). **Inferred, not the paper's claim:** that 300 × 20 is "the number a
short youth has to match" is this team's reading of what correct ranking cost them; the paper
states the budget, not the threshold.

For the idea — verbatim, from the same abstract: *"co-optimizing morphology and control
creates useful goal-switching, yielding morphology-controller pairs whose performance cannot
be reached by optimizing the controller alone for a fixed morphology."*

The paper attacks *cheap evaluation*, not *co-growth of body and brain*. Only the first half
had entered the thread.

---

## E. Prior "connectome-seeded organisms" — the "first" claim
Named in the thread and not re-verified here beyond their existence: OpenWorm (C. elegans, 302
neurons, since 2014); integrative brain–body–environment C. elegans simulators (Nature
Computational Science, 2024-12); whole-fly-brain emulation on Intel Loihi 2 (arXiv 2508.16792);
and entry 5 above. "First honest connectome-seeded artificial organism" does not survive
these.

---

## F. The Lamarckian coupling — where the PNAS codec and a USPEX loop part ways

Found by Ark (2026-09-13, [chat/82](chat/82-ark-064101.md)); every quote below re-verified
in the PDF, **p. 9**, and the sentences on both sides of his quote are included because the
paper argues with itself here and only the whole passage is honest.

Verbatim: *"For the reasons of efficiency, we have used gradients to optimize both the inner and
outer loops. Evolution, which can be viewed as a form of optimization that does not exploit a
gradient, is in general a relatively slow and inefficient algorithm, successful because it
operates on massive numbers of individuals in parallel over hundreds of millions of years. The
feedback in our algorithm that guides the gradient from each generation—the fact that the
trained weight matrix in the kth generation is used to modify the genome in the (k + 1)st
generation—can be viewed as a form of Lamarckian evolution, and is, as such, biologically
unrealistic. The net effect of our approach, however, is similar to Darwinian evolution. Our
algorithm can also be seen as an implementation of the Baldwin effect."* (p. 10 adds that the
outer loop *"repeated these iterations 500 times"*.)

What this does to the synthesis proposed in [chat/77](chat/77-cc-061918.md) — three things,
in order of weight:

1. **The 322× was demonstrated where the inner loop is differentiable and backpropagation
   reaches the genome.** An evolutionary search over morphologies has no gradient; that is a
   different regime, and the compression numbers are not reproduced in it. The paper says so
   itself by calling the gradient-free path "slow and inefficient".
2. **A Lamarckian genome edit is not a mutation.** The idea's main artefact is the lineage —
   which mutation appeared, which module was inherited. A genome rewritten from the trained
   phenotype each generation has no annotatable mutation. At the exact point where the codec is
   successful, the codec and the tree stand on opposite sides of the paper's own distinction.
3. **The paper's own net-effect claim is the honest counterweight** — "similar to Darwinian
   evolution", "an implementation of the Baldwin effect". So the collision is with the
   *mechanism* the idea specifies (heredity of modules, soft mutation), not with the *outcome*
   the idea wants. That is a narrower objection than "the codec cannot be used", and it says
   where the work is: a genome update that is Darwinian in mechanism, not only in net effect.

**Net for the condition:** it stands, and now has a second, independent ground. The PNAS
result is not for a gradient-free loop; the 2508.17464 result says cheap evaluation misranks.
Both say the same thing from different sides: **the cheap step in the middle of the loop is the
unproven step.**

## What was NOT verified, and where fetches failed
- PNAS page returned 403; PubMed pages returned a cookie wall for both papers; bioRxiv
  rate-limited (429) the flyvis full text once; Nature redirected to a login. The PNAS paper
  was read from the lab's open PDF (saved); flyvis from the bioRxiv abstract page and the repo
  readme.
- Neuron counts and the connectome release behind entry 5 are not in its abstract.
- No paper below was read for its methods beyond what is quoted. Entries 6–8 are abstracts.

## G. Dataset — MPI-Sintel (rights, read at source)

**Observed** (files read 2026-09-13). On disk, outside the repository by design, at
`connectome-seed-data/SintelDataSet`: archive `MPI-Sintel-complete.zip`, 5,627,783,629 bytes
(= server Content-Length), `zipfile.testzip()` clean over all 8,753 members; extracted
`training/final` 23 sequences / 1,064 files, `training/flow` 23 / 1,041 (`.flo`),
`training/clean` 23 / 1,064, `test/final` and `test/clean` 12 sequences each. flyvis resolves
it (`download_sintel()` → "Found Sintel at"); `MultiTaskSintel(tasks=["flow"], n_frames=4)`
yields 69 items, sample 0 `lum (9, 1, 721)`, `flow (9, 2, 721)`, float32. CPU only.

**Rights.** No LICENSE or COPYING file exists anywhere in the extracted tree. `README.txt`
line 3: *"Copyright (c) 2012 Daniel Butler, Jonas Wulff, Garrett Stanley, Michael Black,
Max-Planck Institute for Intelligent Systems, Tuebingen"*; line 155: *"If you use this work,
please cite:"* followed by the bibtex entry `Butler:ECCV:2012` ("A naturalistic open source
movie for optical flow evaluation", ECCV 2012, LNCS 7577, pp. 611–625). The words "license",
"licence", "terms" and "permission" do not occur in `README.txt`. The website's terms
(sintel.is.tue.mpg.de) were **not** read.

**Consequence.** The data never enter this repository — not the archive, not a frame, not a
`.flo` file; the data root is ignored and sits beside the repository, not inside it. Any
article that uses the flow task cites Butler et al. 2012.

---

## H. The second kind of cheap evaluation (read at source, 2026-09-14)

**AlphaGenome Atlas team (Google DeepMind, with Exeter, Broad, Boston Children's, Stowers, MSK) —
"AlphaGenome Atlas: in silico mutagenesis of the entire human genome improves prioritization and
interpretation of non-coding variants"**, preprint PDF at Mike's link
(<https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/alphagenome-atlas.pdf>,
83 pages, 14,647,436 bytes), and the DeepMind blog post of the same name, **"AlphaGenome Atlas:
A predictive map of every possible DNA letter change in the human genome"**, dated
*"September 8, 2026"*, byline *"AlphaGenome Atlas team"*
(<https://deepmind.google/blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/>).
Brought in by Mike (DPC Research chat, 2026-09-13 17:50 UTC). **Full text** of both, read at
source by CC's subagent 2026-09-14: the PDF fetched with curl and its text extracted with pypdf
(263,411 characters); the blog fetched with curl and grepped. The PDF carries **no date line of
its own**; the date above is the blog's. Lead authors (PDF, first line): *"Jun Cheng, Kyle R.
Taylor, Lauren Nicolaisen, Joshua Pan, Clare Bycroft, Matteo Perino, Tom Ward, Gareth Hawkes,
Laura E. Covill, Melanie Weilert, Raina W. Thomas, Natasha Latysheva"*; the supervising-author
line ends with *"Pushmeet Kohli, Žiga Avsec"*.

**The sentence Ark quoted is on the blog, not in the PDF** — the words "practically impossible"
do not occur in the PDF text. Blog, verbatim: *"With roughly 9 billion possible single-letter
mutations in the human genome, testing each one in the lab is practically impossible."*
Confirmed word for word.

Numbers, verbatim:
- PDF §2: *"we calculated the difference between reference and alternate allele predictions for
  all **~9 billion** SNVs in hg38 using AlphaGenome"*; *"We also scored **>100 million** indels
  observed in major biobanks (gnomAD, UK Biobank, All of Us)"*.
- Size — blog only: *"AlphaGenome Atlas is a massive **1-petabyte** dataset, more than 30 times
  larger than the AlphaFold Database."* No TB/PB figure is in the PDF text.
- AVI — PDF abstract: *"These predictions were then used to derive a unified and interpretable
  AlphaGenome Variant Impact (AVI) score"*; blog: *"The AVI combines the strengths of AlphaGenome
  and AlphaMissense … condensing both models' predictions into a single number. Now, researchers
  can rapidly rank variants and interpret their molecular effects at the same time."*
- The source's own top-K metric — PDF, Fig. 3A legend: *"AVI and CADD v1.7 were evaluated on
  **112** likely pathogenic variants from solved cases, ranked against intra-patient background
  variants. Curves plot the cumulative recall (y-axis) of causal variants captured within the
  top K prioritized candidates (x-axis)."* Panel labels (fig. S9A): *"Top 10: 36.2% vs 27.6%
  Top 50: 74.3% vs 61.0% Top 100: 86.7% vs 78.1%"* (AVI vs CADD v1.7).

Validation at the top of the ranking, verbatim:
- Blog (Ark's quote, confirmed): *"Our trusted external collaborators have already used
  AlphaGenome Atlas to identify and **experimentally verify** key variants in unsolved rare
  disease research and find rare variants associated with common traits."*
- Blog, DNM1: *"the team discovered a variant affecting a gene called DNM1, which is strongly
  linked to epileptic encephalopathy. Crucially, the AlphaGenome predictions underlying the AVI
  score showed exactly how the variant functioned: it created an incorrect splice site … that led
  to an abnormal extension of the resulting protein. Experimental screens validated the research
  prediction"*.
- PDF, the same case: *"For a proband with epileptic encephalopathy (Fig. 3B), the **top ranked**
  variant by AVI was a heterozygous noncoding VUS in intron 10 of DNM1 (chr9:128225994:G>A …)"*;
  *"We then performed high-throughput experiments in which the 265 nucleotides upstream of exon
  10a were mutagenized and assayed in a minigene reporter assay across 5 cell lines … We
  identified 12 intronic variants that led to in-frame exon extensions, including all three of
  the likely pathogenic variants we and others have reported"*; *"Together, this evidence was
  sufficient to recommend Likely Pathogenic classification of chr9:128225994:G>A."*
- PDF, motif maps: *"For three TFs, we experimentally validated the mapped motif instances by
  performing high-resolution ChIP-nexus binding experiments"*.

Predictions versus validation — the source's own words:
- PDF, Discussion: *"Atlas and AVI are research tools that predict molecular effects, and
  therefore can only act as part of the evidence chain leading to clinical diagnoses, and are
  not sufficient evidence on their own."* Data Availability: *"AlphaGenome Atlas and AVI
  predictions are provided for research purposes only. Not for use in diagnostic procedures for
  medical decision-making."*
- Blog: *"AlphaGenome has not been validated for, and is not approved for, any clinical use."*

Not found in the fetched text: a date line in the PDF; a dataset-size figure in the PDF; the
"practically impossible" sentence in the PDF (blog only, as above).

**The distinction — Reported: Ark, DPC Research chat 2026-09-13 17:51 UTC** (the analysis is
his; this file records it). There are two kinds of "cheap evaluation", and they are not the
same claim:

- **(i) A trained surrogate.** A model fitted once on a large corpus of expensive measurements,
  then predicting cheaply. AlphaGenome's kind. Validated not over the whole population but at
  the **top of its ranking**, by an external experiment — the DNM1 case above, as the source
  states it.
- **(ii) A prefix of the same process.** Nothing is trained; the expensive procedure is stopped
  early (here 1k / 5k / 25k iterations instead of 250k). This project's pre-registration's kind
  — and the kind arXiv 2508.17464 (§D) measured and found **not to rank**.

AlphaGenome's success is evidence for (i). It does not license (ii). Three conditions it had
that this project lacks (Ark's reading, Reported): a surrogate trained on real measurements
(here there are no fitness measurements — only the simulator, so a surrogate would have to be
trained on N expensive runs of that same simulator, deferring the saving); a finite,
enumerable space (3 alternatives × 3 billion positions, so "compute everything instead of
searching" is feasible; genomes and morphologies are unbounded); one fixed genome (individuals
here are unbounded and do not lie ready). And a fourth, structural (Ark, same message): their
expensive check is external and independent of the model; ours is the same simulator run
longer — **no independent arbiter exists anywhere in the programme**, not only in the test.

**What it changes here — proposed, not registered.** 2508.17464 tested whether a cheap ranking
agrees with the expensive ranking over the whole population (rank correlation). DeepMind never
tested that and did not need to; what was checked, and held, is whether the cheap score **finds
the top**. That is a second, weaker hypothesis for (b): *does the cheap evaluation find the
top-k of the expensive ranking?* — distinct from rank correlation, and 2508.17464 did not test
it. Whether it enters `docs/preregistration-cheap-vs-expensive.md` as a secondary hypothesis
is **Mike's decision**; nothing in that file changes with this entry. What the source *does*
show, as a fact about method (Observed above, inference ours): a top-K recall curve against an
independent truth is what a "finds the top" test looks like when it is done.

**What it gives us:** the largest current example of the "expensive is unreachable → cheap
proxy" move, done in a way that works; a named reason it works; and a second hypothesis
shape for (b) that the existing counterexample leaves untouched.

**What it does not give us:** a licence for a prefix-of-the-process proxy; a reason to build
an "atlas" of morphologies (§D's 1,305,840-morphology map was that, and the top still did not
rank); or an arbiter — the top of our ranking has nothing external to be checked against.
