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

---

## I. Digital evolution with inheritance — the half this file did not have

Searched 2026-09-20 on Mike's word (literature pass authorised 09:27 UTC). Everything above
was built from the **connectome** side. Nothing above mentions Tierra, Avida, von Neumann,
open-ended evolution, quality-diversity, NEAT, CPPNs, L-systems, or noisy-fitness theory —
i.e. nothing above bears on points 2–5 of [idea.md](idea.md) or on the evolutionary tree. This
section is that half. Same rules as §A–§H: every entry says **how far it was read**, quotes are
verbatim from the source named, and a fetch that failed is written down.

Leads came from Zcode (DPC Research chat, 2026-09-20) as arXiv ids and one-line claims. They
were treated as **leads to verify**, not as facts. Where his note and the source disagree, both
are given — see §I.9; one id of his is wrong and one date correction of his is right.

Local copies of everything read beyond an abstract are in
`sources/local/2026-09-20-digital-evolution/` with a `PROVENANCE.md` giving each URL and the
extraction command. That directory is gitignored: none of these has a confirmed redistribution
licence, so nothing here enters the repository.

Read status, as above: **full text** = text extracted and read · **abstract** = abstract page
read · plus, new here, **full text, §§ named** = the PDF was extracted and specific sections
were read, not the whole paper.

### I.1 Genome representation — how "a rule that generates wiring" has been written down before

This is point 1 and Mike's own named next step («формализация представления генома»). Six
entries; they are the ones Ark's track should read before proposing a rule.

#### 9. The original: one graph encodes body and brain, and it is read as growth instructions
**Sims K. — "Evolving Virtual Creatures", Computer Graphics (SIGGRAPH '94 Proceedings), July
1994, pp. 15–22.** PDF from the author's site. **Full text.**

What was done: a genetic algorithm over directed graphs; each graph is decoded into a
three-dimensional articulated body *and* its controller, and the creatures are evaluated in a
physical simulation for swimming, walking, jumping and following.

The representation, verbatim: *"A genetic language is presented that uses nodes and connections
as its primitive elements to represent directed graphs, which are used to describe both the
morphology and the neural circuitry of these creatures."* And, on growth: *"The genetic
representation of this morphology is a directed graph of nodes and connections. Each graph
contains the developmental instructions for growing a creature, and provides a way of reusing
instructions to make similar or recursive components within the creature."* The brain is the
same kind of object: *"The genotype descriptions of virtual brains and the actual phenotype
brains are both directed graphs of nodes and connections."*

Two mating operators, verbatim — this is point 3's «склеиваем рабочие модули двух предков»,
written down in 1994: *"The first is a crossover operation … The nodes of two parents are each
aligned in a row as they are stored, and the nodes of the first parent are copied to make the
child, but one or more crossover points determine when the copying source should switch to the
other parent."* And: *"A second mating method grafts two genotypes together by connecting a
node of one parent to a node of another. The first parent is copied, and one of its connections
is chosen at random and adjusted to point to a random node in the second parent. Newly
unconnected nodes of the first parent are removed and the newly connected node of the second
parent and any of its descendants are appended to the new graph."* Operator mix, verbatim:
*"40% asexual, 30% crossovers, and 30% grafting."*

What was measured, and the instrument: fitness is distance/velocity in a dynamics simulation
(*"The fitness tests each include a dynamics simulation"*); population 300, 50–100 generations,
run on a 32-processor CM-5, *"might take around three hours"*.

**What it says to our points — (i) a worked technique, and (ii) a failure mode in the same
paper.** The technique: the idea's "grammar that grows body and brain together" and its
heredity operator both already exist in this exact form, and grafting — attach a subtree of
parent 2 where parent 1 had a connection — is a cleaner statement of "glue working modules"
than crossover on a linear genome. The failure mode, verbatim: *"A population of interbreeding
creatures often converges toward homogeneity, but each separately run evolution can produce
completely different locomotion strategies."* That is the simulator cockroach of point 3, named
by the founding paper, and Sims's own answer was to run many separate evolutions rather than
to maintain diversity inside one.

#### 10. L-systems: the same job done by rewrite rules, and what that buys
**Hornby G. S., Pollack J. B. — "Evolving L-systems to generate virtual creatures", Computers &
Graphics 25 (2001) 1041–1048.** Course copy (UCL). **Full text.**

What was done: parametric 0L-systems (*"an ordered quadruplet, G = (V, S, ω, P)"*) are evolved;
the string a grammar produces is a sequence of turtle-style construction commands, and *"The
creature constructor module follows the string of construction commands, building the creature
piece by piece."*

The claim against direct encodings, verbatim: *"the most recent work in this area has produced
ungainly creatures with less than 50 components. The asymmetries of these creatures is a result
of using a direct encoding, an explicit encoding with a one-to-one mapping from genotypic
encoding to creature-part. As direct encodings have no re-use, symmetries and regularities do
not occur, except by chance."* And the result: *"Creatures evolved by this system have hundreds
of parts."* Setup: population 100, up to 500 generations, *"10-20 production rules, 2-4
condition-successor pairs and 1-3 parameters for production rules."*

One measurement detail that belongs to §I.5, not here — their fitness is already resampled:
*"As this joint noise affects how the creature moves, three evaluation trials are made, each
using different random noise, with the lowest score assigned as the creature's fitness."*

**What it says to our points — (i) a worked technique.** This is the closest published thing to
«наследуемая грамматика»: rules, parameters, re-use, and a decoder that turns a derived string
into a body. The reason to read it before writing our own rule is its constraint list —
conditions restricted to comparisons of a parameter against a constant, parameters restricted to
one arithmetic operation — which is how they kept an arbitrary grammar decodable. Compare with
SELFIES (§A.2): validity lives in the decoder, not in the fitness function.

#### 11. CPPNs: development without time or local interaction
**Stanley K. O. — "Compositional Pattern Producing Networks: A Novel Abstraction of
Development", Genetic Programming and Evolvable Machines, Springer, 2007** (author preprint;
its title page reads *"To appear in: Genetic Programming and Evolvable Machines Special Issue on
Developmental Systems"*, so the volume and pages are **not on the copy read** and are not
asserted here). **Full text.**

The move, verbatim: *"Unlike currently accepted abstractions such as iterative rewrite systems
and cellular growth simulations, CPPNs map to the phenotype without local interaction, that is,
each individual component of the phenotype is determined independently of every other
component."* The argument that this is allowed: *"any morphology, when viewed as a distribution
of particles in space, is possible to represent as a function without the notion of time. A
developmental chronology is only one way of producing a particular constellation of particles."*
And what replaces growth: *"In this way, composition replaces interaction."*

What was measured, and how: not a benchmark. The evidence is interactive evolution of 2-D images
by a human chooser, assessed against a named list of motifs — *"Symmetry, reuse, reuse with
variation, preservation of regularities, and elaboration of existing regularities all are
demonstrated and capitalized on by CPPN-NEAT."* So the instrument is a human eye against a
checklist of regularities, and the paper says so.

**What it says to our points — (i) a worked technique, with a warning.** It is the cheapest
possible answer to "how is a growth rule written down": as a composed function of coordinates,
queried per element. For a connectome seed the appeal is direct — a neuron's position in a
developmental coordinate frame becomes the query, which is exactly the *"(type + developmental
coordinate)"* label §A.1 says the genomic-bottleneck codec would need. The warning is that
CPPNs deliberately throw away temporal unfolding, so nothing in a CPPN expresses "this module
duplicates, then specialises" — point 2's core verb. Regularity yes; a developmental *history*
no.

#### 12. HyperNEAT: a CPPN that outputs connectivity, at any resolution
**Stanley K. O., D'Ambrosio D. B., Gauci J. — "A Hypercube-Based Indirect Encoding for Evolving
Large-Scale Neural Networks", Artificial Life 15(2), MIT Press, 2009** (author preprint, header
*"Accepted to appear in Artificial Life journal 15(2)"*). **Full text.**

Mechanism, verbatim: *"HyperNEAT employs an indirect encoding called connective Compositional
Pattern Producing Networks (connective CPPNs) that can produce connectivity patterns with
symmetries and repeating motifs by interpreting spatial patterns generated within a hypercube as
connectivity patterns in a lower-dimensional space."* The property that matters to us,
verbatim: *"connective CPPNs can represent the same connectivity pattern at any resolution,
allowing ANNs to scale to new numbers of inputs and outputs without further evolution"*; and in
§3.5, *"There is no upper bound on substrate resolution, that is, a connectivity concept is
infinite in resolution."*

What was measured, and how: visual discrimination on an 11×11 substrate (*"a total of 14,641
potential connection strengths"*), then the *same evolved CPPN re-queried* at 33×33 and 55×55 —
*"the weights of over one million and nine million connections, respectively"* — with no further
evolution; 20 runs, 300 generations, against a direct-encoding control (P-NEAT). Result,
verbatim: *"The results show that HyperNEAT generalizes significantly better than P-NEAT
(p < 0.01) and scales almost perfectly."*

**What it says to our points — (i) a worked technique, and the closest prior art to point 1.**
"The seed is not all the weights but a rule" is exactly a connective CPPN: a generator queried on
a (source, target) pair to return a weight. Note the relation to §A.1: the PNAS g-network is the
same shape — pre/post pair in, weight out — but trained by gradient; HyperNEAT is the same shape
*evolved*, which is the regime §F says the PNAS compression numbers do not cover. If Ark's track
wants a gradient-free genome that generates wiring, this is the existing baseline to beat, not a
gap.

#### 13. The price of an indirect encoding, measured across a regularity dial
**Clune J., Stanley K. O., Pennock R. T., Ofria C. — "On the Performance of Indirect Encoding
Across the Continuum of Regularity", IEEE Transactions on Evolutionary Computation 15(3),
346–367, June 2011; DOI 10.1109/TEVC.2010.2104157.** Author copy. **Full text.**

What was done, and the instrument — this is the part worth copying: they built problems with a
*tunable* regularity. In the "target weights" problem, *"some randomly chosen subset of the
target weight values, S, are assigned Q, a single randomly-chosen value"*; S runs 0, 10, 20 …
100 %, eleven treatments, ten runs each, 1000 generations, population 1000. So "regularity" is
not an adjective here, it is a knob with a number on it.

Results, verbatim: *"FT-NEAT outcompetes HyperNEAT when problem regularity is low."* … *"As
problem regularity increases, HyperNEAT's performance rises to, and then surpasses, that of
FT-NEAT, demonstrating that HyperNEAT can exploit problem regularity."* … *"FT-NEAT is blind to
problem regularity."* The threshold, verbatim: *"the performance of HyperNEAT is statistically
indistinguishable below a certain regularity threshold (p > 0.051 comparing the final
performance of the S = 0% treatment to treatments with S ≤ 30%)"*; and on the bit-mirroring
problem, *"HyperNEAT's performance advantage is statistically significant only once that type of
regularity is above 50%"*. The fix they propose, verbatim from the abstract: *"a new algorithm
called HybrID that hybridizes indirect and direct encodings, which matched HyperNEAT's
performance on regular problems yet outperformed it on problems with some irregularity."*

**What it says to our points — (ii) a documented failure mode, and the sharpest single result
for point 1.** An indirect encoding is not free: below a measurable regularity threshold it
*loses* to evolving the weights directly. A connectome seed is a bet that the fly's wiring is
regular enough for a rule to pay. That bet is now a measurable quantity rather than a belief —
and this paper shows how to measure it: build the same task at several regularity levels and
watch where the indirect encoding crosses the direct one. It also says the eventual answer is
probably HybrID-shaped: a rule that generates the wiring, plus a refinement stage that breaks the
rule where it must. That matters for the tree — if the refinement is per-individual and not
heritable, the tree records the rule and not the refinement, and the artefact has to say so.

#### 14. Neural developmental programs: growth by local message passing
**Najarro E., Sudhakaran S., Risi S. — "Towards Self-Assembling Artificial Neural Networks
through Neural Developmental Programs", arXiv 2307.08197, submitted 2023-07-17.** **Abstract.**

Verbatim: *"The growth process is guided by another neural network, which we call a Neural
Developmental Program (NDP) and which operates through local communication alone."* And: *"we
take initial steps toward neural networks that grow through a developmental process that mirrors
key properties of embryonic development in biological organisms."* The abstract names the axis of
the study — *"the role of neural growth on different machine learning benchmarks and different
optimization methods (evolutionary training, online RL, offline RL, and supervised learning)"* —
but **no numbers are in the abstract**, and the paper itself was not read.

**What it says to our points — (i) a technique, and the missing half of entry 11.** This is the
branch Stanley's CPPN paper deliberately gave up — local interaction and unfolding over time —
put back, with the growth rule itself a network. That is what point 2's «модули дублируются,
соединяются, специализируются» needs a formalism for. Not verified beyond the abstract; read
before adopting.

### I.2 Body and brain together, and curricula (point 2)

#### 15. Premature morphological convergence, with a number on it
**Cheney N., Bongard J., SunSpiral V., Lipson H. — "Scalable Co-Optimization of Morphology and
Control in Embodied Machines", arXiv 1706.06133, v1 2017-06-19, v2 2017-12-12.** **Full text,
§§ abstract, I, III–V.**

The hypothesis, verbatim: *"most evolutionary changes to morphology tend to adversely impact
sensorimotor control, leading to an overall decrease in behavioral performance."* The technique,
verbatim: *"morphological innovation protection, which temporarily reduces selection pressure on
recently morphologically-changed individuals, thus enabling evolution some time to 'readapt' to
the new morphology with subsequent control policy mutations."*

What was measured, and how: a (μ, λ) evolution strategy, *"μ = 25 parents and λ = 25 mutants for
a population size of 50"*, 5000 generations, 30 runs per treatment; *"Crossover was not
considered in this work"*; a mutation touches morphology or controller but *"not both"*, and five
morphology:controller mutation ratios (1:99 … 99:1) were tried, of which *"none showed a
significant effect on resolving the premature convergence and resulting fitness in preliminary
trials without innovation protection."* The failure mode, quantified: without protection, *"gross
morphological changes tend to be absent after generation 50 (just 1% into the full 5000
generations)."*

**What it says to our points — (ii) the failure mode point 2 walks into.** The idea's curriculum
(fly → beetle → six-legged truck → quadruped) assumes the body keeps changing. This says that in
a plain evolutionary loop it stops changing almost immediately, and that tuning how often the
body is mutated does not fix it; what fixes it is a protected period for the newly changed body.
Note the relation to §D's 2508.17464, same first author: §D says cheap evaluation *misranks* new
morphologies; this says the cure is to *not select on them yet*. The two are the same finding
from opposite ends, and "youth" (point 4) is on the hook for both.

#### 16. POET: generate the environments as well as the solutions
**Wang R., Lehman J., Clune J., Stanley K. O. — "Paired Open-Ended Trailblazer (POET): Endlessly
Generating Increasingly Complex and Diverse Learning Environments and Their Solutions", arXiv
1901.01753, v1 2019-01-07, v3 2019-02-21; comments field "28 pages, 9 figures".** **Abstract.**

Verbatim: *"it pairs the generation of environmental challenges and the optimization of agents to
solve those challenges"*; *"critically, allows these stepping-stone solutions to transfer between
problems if better, catalyzing innovation"*; and the claim: *"POET produces a diverse range of
sophisticated behaviors that solve a wide range of environmental challenges, many of which cannot
be solved by direct optimization alone, or even through a direct-path curriculum-building control
algorithm introduced to highlight the critical role of open-endedness in solving ambitious
challenges."*

**What it says to our points — (i) a technique, and (iii) something that undercuts the idea's
curriculum.** The idea fixes the curriculum in advance and in order. POET's control condition is
precisely "a direct-path curriculum-building control algorithm", and the abstract says it loses.
If that holds, a hand-written fly → beetle → quadruped ladder is the weaker design, and the
environments should be generated and kept in an archive alongside the creatures. The transfer
step is also something the tree must be able to record: a solution that moves between
environments is an edge that is not a parent-child edge.

#### 17. OMNI-EPIC: the environments written as code by a model
**Faldor M., Zhang J., Cully A., Clune J. — "OMNI-EPIC: Open-endedness via Models of human
Notions of Interestingness with Environments Programmed in Code", arXiv 2405.15568, v1
2024-05-24, v3 2025-02-14.** **Abstract.**

Verbatim: *"OMNI-EPIC leverages foundation models to autonomously generate code specifying the
next learnable (i.e., not too easy or difficult for the agent's current skill set) and
interesting (e.g., worthwhile and novel) tasks"*; it *"generates both environments (e.g., an
obstacle course) and reward functions (e.g., progress through the obstacle course quickly without
touching red objects)"*. The abstract reports no quantitative result — it says *"We showcase the
explosive creativity of OMNI-EPIC"* — and the paper was not read.

**What it says to our points — (i), weakly.** It is the current form of point 5's «отдельный
закрытый набор арен»: arenas as generated code rather than a fixed list. Also a caution — if a
model writes the reward function, the evaluator itself becomes part of the search space. See
§I.6.

### I.3 Variation operators on structured graphs (point 3)

#### 18. NEAT: why crossing two networks normally destroys them, and the fix
**Stanley K. O., Miikkulainen R. — "Evolving Neural Networks through Augmenting Topologies",
Evolutionary Computation 10(2), 99–127, MIT Press, 2002.** PDF marked *"This article is provided
courtesy of The MIT Press."* **Full text.**

The problem, verbatim: *"Competing conventions means having more than one way to express a
solution to a weight optimization problem with a neural network. When genomes representing the
same solution do not have the same encoding, crossover is likely to produce damaged offspring."*
And why it is worse for graphs: *"An even more difficult form of competing conventions is present
in TWEANNs, because TWEANN networks can represent similar solutions using entirely different
topologies, or even genomes of different sizes."*

The fix, verbatim: *"The main insight in NEAT is that the historical origin of two genes is
direct evidence of homology if the genes share the same origin. Thus, NEAT performs artificial
synapsis based on historical markings, allowing it to add new structure without losing track of
which gene is which over the course of a simulation."* Mechanically: *"Whenever a new gene
appears (through structural mutation), a global innovation number is incremented and assigned to
that gene … innovation numbers are never changed."* At crossover: *"genes are randomly chosen
from either parent at matching genes, whereas all excess or disjoint genes are always included
from the more fit parent."* And the second use of the same bookkeeping: *"Thus, innovations in
NEAT are protected in their own species."*

What was measured, and how: double pole balancing, averages over 20–120 runs, counting
evaluations to a solution, plus a component ablation (Table 3, "double pole balancing with
velocities", averages excluding failures): Full NEAT **3,600** evaluations, 0 % failures;
Nonmating NEAT **5,557**, 0 %; Initial Random NEAT **23,033**, 5 %; Nonspeciated NEAT **25,600**,
25 %; No-Growth NEAT **30,239**, 80 %. Verbatim on the crossover ablation: *"It took on average
5,557 evaluations to find a solution without mating, compared to 3,600 with mating enabled. The
difference is statistically significant (p = 0.001). Thus, it is clear that mating does
contribute when it is done right."* And on the harder benchmark: *"NEAT takes 25 times fewer
evaluations than Gruau's original benchmark."*

**What it says to our points — (i) a worked technique, and the one point 3 needs most.**
«Склеиваем рабочие модули мозга и тела двух предков» is crossover on graphs, and this paper says
plainly that doing it without a homology record damages offspring. The lesson transfers exactly:
every module, rule or connection in our genome needs a **birth id that is never reused and never
renumbered**, and inheritance is defined by matching those ids. That one decision is also what
makes the evolutionary tree computable — the tree and the crossover operator want the same data
structure. Read the ablation honestly, though: mating is worth about 1.5× here, while growth from
minimal structure is worth about 8×. Crossover is not the big lever; the bookkeeping that makes
it legal is.

### I.4 Diversity maintenance (points 3 and 5)

#### 19. Novelty search: the objective is the problem
**Lehman J., Stanley K. O. — "Abandoning Objectives: Evolution through the Search for Novelty
Alone", Evolutionary Computation 19(2), 189–223, MIT Press, 2011.** Author preprint.
**Full text.**

The mechanism, verbatim: *"The novelty of a newly generated individual is computed with respect
to the behaviors of an archive of past individuals whose behaviors were highly novel when they
originated."* The metric: *"A simple measure of sparseness at a point is the average distance to
the k-nearest neighbors of that point, where k is a fixed parameter that is determined
experimentally."* Entry rule: *"If novelty is sufficiently high at the location of a new
individual, i.e. above some minimal threshold ρmin, then the individual is entered into the
permanent archive."*

What was measured, and how: maze navigation, 40 runs per method, counting evaluations and success
rate. Medium maze, verbatim: *"Novelty search took on average 18,274 evaluations (sd = 20,447) to
reach a solution, while fitness-based NEAT was three times slower, taking 56,334 evaluations (sd
= 48,705), averaged over 40 runs."* Hard maze, verbatim: *"fitness-based NEAT was only successful
in three out of 40 runs, while NEAT with random selection fared marginally better, succeeding in
four out of 40 runs … However, novelty search was able to solve the same map in 39 out of 40
runs."* A size effect worth noting: solutions found by fitness had *"66.74 connections, sd =
56.7"*, *"almost three times greater (p < 0.05; Student's t-test) than those evolved by NEAT with
novelty search (24.6 connections, sd = 4.59)."*

**What it says to our points — (i) a technique, and (iii) a challenge to point 5.** The archive
in point 3 («random embryos и diversity archive») is this, and it is not decoration: on the
deceptive map the objective-driven run is no better than random selection. The challenge is
sharper than it looks. Point 5 lists «новизна стратегии» as *one objective among six*. This
paper's result is that novelty works when it **replaces** the objective, and their own control
shows the weaker version is weaker: when behaviour was characterised by the fitness measure
itself, *"The maze was solved in only 11 out of 40 runs."*

#### 20. MAP-Elites: an archive with axes the designer chooses
**Mouret J.-B., Clune J. — "Illuminating search spaces by mapping elites", arXiv 1504.04909,
submitted 2015-04-20; the arXiv comments field reads "Early draft".** **Abstract.**

Verbatim: *"It creates a map of high-performing solutions at each point in a space defined by
dimensions of variation that a user gets to choose."* And: *"Interestingly, because MAP-Elites
explores more of the search space, it also tends to find a better overall solution than
state-of-the-art search algorithms."* Domains named in the abstract: *"producing modular neural
networks to designing simulated and real soft robots"*. No numbers are in the abstract; the paper
was not read, and its own comments field calls it a draft.

**What it says to our points — (i) a technique, and also a shape for the tree.** MAP-Elites gives
an archive whose cells are *named by the designer* — limb count, mass, gait frequency, fraction
of fly-inherited modules. That is a better fit for the idea's artefact than a plain novelty
archive: the map is readable by a person, and "which body plans were ever occupied, and by whose
descendants" is exactly a question the tree is supposed to answer. Read the paper before quoting
any number from it.

### I.5 Selection under noisy or cheap evaluation (point 4)

§D and §H already carry this project's own case: 2508.17464 measured that cheap evaluation does
not rank, and §H separates a trained surrogate from a prefix of the same process. What was
missing is the older literature that named the problem and its standard cures. Three entries;
they connect to §D rather than repeat it.

#### 21. The survey that names the cures — and says the choice between them is unsettled
**Jin Y., Branke J. — "Evolutionary Optimization in Uncertain Environments — A Survey", IEEE
Transactions on Evolutionary Computation 9(3), 303–317, 2005.** Honda Research Institute author
copy (title page: *"To appear in IEEE Transactions on Evolutionary Computation, 2005"*).
**Full text, §§ I, III.A–III.B.**

The taxonomy, verbatim: *"uncertainties in evolutionary computation can be divided into the
following four categories. First, the fitness function is noisy. Second, the design variables
and/or the environmental parameters may change after optimization … Third, the fitness function
is approximated, which means that the fitness function suffers from approximation errors. Fourth,
the optimum of the problem to be solved changes over time."*

The cures, verbatim. Implicit averaging: *"Because promising areas of the search space are
sampled repeatedly by the EA, and there are usually many similar solutions in the population,
when the population is large, the influence of noise in evaluating an individual is very likely
to be compensated by that of a similar individual … a simple approach to reducing the influence
of noise on optimization is to use a large population size."* Explicit averaging is §III.A,
re-sampling. And the honest part, verbatim: *"A natural question is whether explicit averaging in
the form of re-sampling or implicit averaging in the form of a larger population size would be
more effective, given that the total number of fitness evaluations per generation is fixed.
Conflicting conclusions have been reported in different investigations."*

**What it says to our points — (ii), and a correction of framing.** The measured problem behind
point 4 — replicate runs of one configuration diverging as much as different individuals — is
category 1, plain noisy fitness: a 2005-vintage problem with named remedies (re-sampling, larger
population, surrogate models), not a novel obstacle. The correction is that "just average more
runs" is **not** the settled answer. Under a fixed evaluation budget the literature disagrees
about whether to spend it on repeats or on population size, so which one this project picks is a
registrable design decision with a falsifier, not a default.

#### 22. How little noise it takes to break selection — a proof, not an anecdote
**Sudholt D. — "Analysing the Robustness of Evolutionary Algorithms to Noise: Refined Runtime
Bounds and an Example Where Noise is Beneficial", arXiv 1812.00966, v1 2018-12-03.**
**Full text, abstract + §1.**

The classic result, as this paper states it, verbatim: Droste *"proved that, when p = O((log
n)/n) the (1+1) EA can still optimise OneMax efficiently. But when p = ω((log n)/n) the expected
optimisation time becomes superpolynomial."* This paper's own result, verbatim: *"We close this
gap by showing that the expected optimisation time is Θ(n²) · exp(Θ(min{pn², n})) for all p ≤
1/2 … Hence the (1+1) EA on LeadingOnes is much more sensitive to noise than previously
thought."* The mitigation, verbatim: *"We also show that offspring populations of size λ ≥ 3.42
log n can effectively deal with much higher noise than known before."* And against a lazy
reading: *"we present an example of a rugged landscape where prior noise can help to escape from
local optima by blurring the landscape."*

**What it says to our points — (ii), the result class named in the brief, now with a citation.**
The threshold behaviour is the point: below a noise level the algorithm works, above it the
expected time blows up exponentially, and the threshold is *low*. This is the theory-side
statement of §D's empirical one. It also names the one cheap lever that is provably right here —
**offspring population size**, logarithmic in problem size — and it forbids a blanket "noise is
always bad" sentence in our record.

#### 23. Successive halving: spend the budget on the survivors
**Li L., Jamieson K., DeSalvo G., Rostamizadeh A., Talwalkar A. — "Hyperband: A Novel
Bandit-Based Approach to Hyperparameter Optimization", arXiv 1603.06560, v1 2016-03-21, v4
2018-06-18; journal reference on the arXiv record: Journal of Machine Learning Research 18 (2018)
1–52.** **Abstract.**

Verbatim: *"we focus on speeding up random search through adaptive resource allocation and
early-stopping. We formulate hyperparameter optimization as a pure-exploration non-stochastic
infinite-armed bandit problem where a predefined resource like iterations, data samples, or
features is allocated to randomly sampled configurations."* Claimed result: *"Hyperband can
provide over an order-of-magnitude speedup over our competitor set on a variety of deep-learning
and kernel-based learning problems."*

**What it says to our points — (i) a technique that changes the shape of the question.** The
cheap evaluation in this project is a prefix of the expensive one (§H's category ii). Hyperband is
the standard way to use such a prefix *without* requiring it to rank: it does not claim the short
run ranks, only that it can eliminate a fraction, and it re-invests the saved budget in the
survivors at longer horizons. That reframes the registered question from "does the cheap score
rank?" to "at what horizon can the bottom fraction be discarded without losing the eventual
winner?" — nearer to §H's "does it find the top?" than to rank correlation. Read at the abstract
only; the description above is the abstract's, not the algorithm as implemented.

### I.6 Reward hacking and evaluator exploits (point 5's held-out arenas)

#### 24. The canonical collection of evolution breaking its own fitness function
**Lehman J., Clune J., Misevic D., Adami C., Altenberg L., … Stanley K. O. (51 authors) — "The
Surprising Creativity of Digital Evolution: A Collection of Anecdotes from the Evolutionary
Computation and Artificial Life Research Communities", arXiv 1803.03453, v1 2018-03-09, v4
2019-11-21.** **Abstract.**

Verbatim: *"many researchers in the field of digital evolution have observed their evolving
algorithms and organisms subverting their intentions, exposing unrecognized bugs in their code,
producing unexpected adaptations, or exhibiting outcomes uncannily convergent with ones in
nature."* And the paper's own status, verbatim: *"This paper is the crowd-sourced product of
researchers in the fields of artificial life and evolutionary computation who have provided
first-hand accounts of such cases. It thus serves as a written, fact-checked collection of
scientifically important and even entertaining stories."* The individual anecdotes were **not
read**, so none is quoted here — including whichever ones the idea's phrase «нашёл дыру в MuJoCo»
is reaching for.

**What it says to our points — (ii), and it is the reference point 5 should cite.** The held-out
arena set is the right instinct and this is its evidence base. Worth noting who wrote it: Cheney
(§D and entry 15), Stanley (entries 11, 12, 18, 19), Sims (entry 9), Lenski and Ofria (entry 28)
are all in the author list — the people who documented the failure are the people who built the
encodings.

#### 25. An evaluator that is a peer-review process, and what actually happened
**Yamada Y., Lange R. T., Lu C., Hu S., Lu C., Foerster J., Clune J., Ha D. — "The AI
Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search", arXiv
2504.08066, v1 2025-04-10.** **Abstract** (the arXiv listing showed **no withdrawal notice** as
of 2026-09-20); plus the authors' own account, **Sakana AI, "The AI Scientist Generates its First
Peer-Reviewed Scientific Publication", page dated 2025-03-12**, **read in full**.

From the arXiv abstract, verbatim: *"an end-to-end agentic system capable of producing the first
entirely AI generated peer-review-accepted workshop paper"*, using *"a novel progressive agentic
tree-search methodology managed by a dedicated experiment manager agent."*

From the Sakana page — the numbers Zcode's one-liner compresses. Three papers were submitted to
an ICLR workshop; one passed review with *"Rating: 6: Marginally above acceptance threshold,
Rating: 7: Good paper, accept, Rating: 6: Marginally above acceptance threshold"*, the other two
*"did not meet the bar for acceptance."* On blindness, verbatim: *"The reviewers were informed
about the possibility and likelihood that papers they are reviewing might be AI generated (3 out
of 43 papers) but not if the papers assigned to them were actually AI generated or not."* On
withdrawal, verbatim: *"Even if papers by The AI Scientist were accepted, we would withdraw them
before they were actually published."*

**What it says to our points — (iii) and (ii).** (iii): the honest reading is that the venue was
a workshop, the reviewers were pre-warned that some papers were AI-generated, and the authors
withdrew the paper themselves — so "passed blind review" is true only with all three
qualifications attached, and our own record should carry them. (ii): the transferable fact is the
shape — when the evaluator is a judgement rather than a measurement, whatever is being optimised
will find the judgement's tolerances. Point 5's held-out arenas are a defence only if the
held-out set is never used to steer.

#### 26. A system whose fitness is a benchmark, which edits itself, and which grows a tree
**Zhang J., Hu S., Lu C., Lange R., Clune J. — "Darwin Godel Machine: Open-Ended Evolution of
Self-Improving Agents", arXiv 2505.22954, v1 2025-05-29, v2 2025-09-26, v3 2026-03-12; code
linked from the arXiv record.** **Abstract.**

Verbatim: *"a self-improving system that iteratively modifies its own code (thereby also
improving its ability to modify its own codebase) and empirically validates each change using
coding benchmarks"*; *"the DGM maintains an archive of generated coding agents. It grows the
archive by sampling an agent from it and using a foundation model to create a new, interesting,
version of the sampled agent. This open-ended exploration forms a growing tree of diverse,
high-quality agents and allows the parallel exploration of many different paths through the
search space."* Numbers, verbatim: *"increasing performance on SWE-bench from 20.0% to 50.0%, and
on Polyglot from 14.2% to 30.7%"*, with *"All experiments were done with safety precautions
(e.g., sandboxing, human oversight)."*

**What it says to our points — (i), and it is the nearest living relative of the idea's
architecture.** Archive + mutation by a generator + empirical validation + *"a growing tree"* is
point 3, point 4 and the artefact, running today, in a domain where evaluation is cheap and
objective. Zcode's author list checks out exactly. Note what makes it work and what we lack: its
evaluator is an external benchmark with a ground truth, which §H says this programme has nowhere.
The abstract describes no reward-hacking episode; Zcode's brief asked for a "DGM evaluator
episode" and **nothing read here supports one** — see §I.9.

#### 27. AlphaEvolve: evolution where the evaluator is a checkable program
**Novikov A., Vũ N., Eisenberger M., Dupont E., Huang P.-S., Wagner A. Z., Shirobokov S.,
Kozlovskii B., Ruiz F. J. R., Mehrabian A., Kumar M. P., See A., Chaudhuri S., Holland G., Davies
A., Nowozin S., Kohli P., Balog M. — "AlphaEvolve: A coding agent for scientific and algorithmic
discovery", arXiv 2506.13131, v1 2025-06-16.** **Abstract.**

Verbatim: *"an evolutionary coding agent that substantially enhances capabilities of
state-of-the-art LLMs"*; *"Using an evolutionary approach, continuously receiving feedback from
one or more evaluators, AlphaEvolve iteratively improves the algorithm"*; the headline: *"a
search algorithm that found a procedure to multiply two 4×4 complex-valued matrices using 48
scalar multiplications; offering the first improvement, after 56 years, over Strassen's algorithm
in this setting"*, and *"novel, provably correct algorithms"*. Zcode's id checks out.

**What it says to our points — (i), and more usefully (iii) about why it works.** The clause that
matters here is *"provably correct"*: AlphaEvolve's fitness is a program whose output can be
verified independently of the search. That is precisely the property §H says is missing in this
programme (*"no independent arbiter exists anywhere in the programme"*). So AlphaEvolve is not
evidence that "LLM-driven evolution works" in our setting; it is evidence that evolution works
**when the evaluator is exact**. Written that way it is honest; written the other way it is
encouragement we have not earned.

### I.7 Phylogeny as the artefact (the idea's main artefact)

#### 28. The paper that traced where a complex feature came from, mutation by mutation
**Lenski R. E., Ofria C., Pennock R. T., Adami C. — "The evolutionary origin of complex
features", Nature 423, 139–144 (2003).** Course copy of the published article. **Full text.**

What was done, and the instrument — this is the method the tree artefact should copy. Avida
digital organisms (*"a genome is a circular sequence of instructions"*, 26 possible instructions,
asexual reproduction by binary fission, mutation on copy) were rewarded for logic functions; the
study followed the **line of descent** of a population that evolved EQU. Verbatim: *"We also
identified every mutation that fell along the line of descent in this population, and
characterized the phenotypic changes associated with each step. The EQU function first appeared
at step 111 (update 27,450). There were 103 single mutations, six double mutations, and two
triple mutations among these steps. Forty-five of the steps increased overall fitness, 48 were
neutral and 18 were deleterious relative to the immediate parent."*

Two results make the method worth copying. First, a knockout analysis of what the feature
actually depended on, verbatim: *"The genome of the first EQU-performing organism had 60
instructions; eliminating any of 35 of them destroyed that function."* Second, a *reversal
experiment* on a single ancestral step, verbatim: *"we reversed this one-step-prior mutation in
the genotype that first expressed EQU. This reversal eliminated the EQU function. Therefore, a
mutation that was highly deleterious when it appeared was highly beneficial in combination with a
subsequent mutation."* Across replicates, verbatim: *"The case-study population was one of 50
that evolved under identical conditions, 23 of which acquired EQU. The phylogenetic depth at
which EQU first appeared ranged from 51 to 721 steps."*

**What it says to our points — (i), and it is the standard the artefact must meet.** The idea
wants a tree that says «какая мутация появилась, какой модуль унаследован от мухи, где линия
сломалась». This paper shows such a claim is only as good as two operations the drawn tree cannot
perform: **knockout** (remove the element — does the skill die?) and **reversal** (undo the
ancestral step — does the skill still arise?). A tree is a hypothesis; those two experiments turn
an edge into a finding. It also warns about replicate count: 50 populations, 23 reached the
feature, depth 51–721 — a single lineage picture proves nothing about inevitability.

#### 29. Tierra: the first lineage bookkeeping, and the criterion for naming a genotype
**Ray T. S. — "An Approach to the Synthesis of Life", in Artificial Life II, SFI Studies in the
Sciences of Complexity vol. XI (Farmer, Langton, Rasmussen & Taylor, eds), Redwood City, CA:
Addison-Wesley, 1991, pp. 371–408.** Read from the **author's own LaTeX source** (`tierra.tex`,
his site), not from a typeset copy; the citation line above is the one in that file. **Full text
of the source, §§ introduction, genebank manager, results.**

The bookkeeping, verbatim: *"Mutations result in the appearance of new genotypes, which are
watched by an automated genebank manager. In one implementation of the manager, when new
genotypes replicate twice, producing a genetically identical offspring at least once, they are
given a unique name and saved to disk."* The naming scheme, verbatim: *"Each genotype name
contains two parts, a number and a three letter code. The number represents the number of
instructions in the genome … Thus the ancestor is named 80aaa, and the first mutant of size 80 is
named 80aab. The first parasite of size 45 is named 45aaa."* And what makes the tree
reconstructible, verbatim: *"The genebanker saves some additional information with each genome:
the genotype name of its immediate ancestor which makes possible the reconstruction of the entire
phylogeny; the time and date of origin."*

An emergence worth recording, verbatim: *"Genetic parasites evolve which are sloppy replicators,
and have the effect of moving pieces of code around between creatures, causing rather massive
rearrangements of the genomes."* Recombination appeared without being implemented.

**What it says to our points — (i), with one design decision handed over ready-made.** Two
things. First, the **entry criterion**: a genotype is recorded only after it has replicated twice
with at least one identical offspring — the tree records *lineages*, not every mutant ever
generated. That is the rule that keeps a phylogeny finite and meaningful, and the idea's tree
needs one like it. Second, the minimal per-node record — name, immediate ancestor, time of origin
— is all the reconstruction requires; everything else is decoration.

#### 30. Tooling: phylogeny tracking as a library, not a script
**Dolson E., Rodriguez-Papa S., Moreno M. A. — "Phylotrack: C++ and Python libraries for in
silico phylogenetic tracking", arXiv 2405.09389, v1 2024-05-15, v2 2024-07-16.** **Abstract.**
Only one fragment came back verbatim from the abstract page — that such systems replicate
*"heredity, variation, and differential reproductive success"* — so what follows is the
abstract's content in the fetch's words, not the authors'.

Content: two components — Phylotracklib (C++, header-only, under the Empirical project umbrella)
and Phylotrackpy (a Python interface via Pybind11); both give an API for attaching phylogenetic
tracking to a digital-evolution system and a stand-alone interface for phylogenetic topology
metrics; explicit pruning and abstraction features to bound memory; design aimed at populations
in the tens of thousands.

**What it says to our points — (i), and it removes a job from the roadmap.** If the tree is the
project's main artefact, the tree needs a format, metrics and a memory bound, and a library for
exactly that exists, in Python. Two honest caveats: read at the abstract only; and a companion
line of work on ALife data standards (Lalejini, Dolson et al., ALIFE 2019) appeared in the search
listing but **was not opened**, so nothing about a standard format is asserted here.

### I.8 Self-replication — framing, not core

#### 31. The description read twice: interpreted as instructions, copied as data
**von Neumann J. — Theory of Self-Reproducing Automata, ed. A. W. Burks, University of Illinois
Press, 1966.** **Not read.** What was read instead: **Burks A. W., "Von Neumann's Self-Reproducing
Automata", report 08226-11-T, University of Michigan, June 1969**, PDF. **Full text, §§ on the
kinematic system and self-reproduction.** Everything below is Burks's exposition, not von
Neumann's own words.

Verbatim (Burks): *"A finite kinematic automaton can be completely described by listing its parts
and their connections, and this description Φ(M) can be stored on the tape. A (finite)
constructing automaton can then be designed which will interpret this description and carry out
the construction."* And the second, different reading of the same tape, verbatim: *"The
constructing machine M next makes a tape for the new machine, copies its own tape contents
(namely, Φ(M)) on this new tape, and attaches the tape to the newly constructed machine."*

**What it says to our points — (i) framing, with one sharp consequence for point 1.** The
description is used twice and differently: *interpreted* to build the body, and *copied
uninterpreted* to be inherited. A genome that is only interpreted has no heredity; a genome that
is only copied has no phenotype. The «наследуемая грамматика» must survive both readings — which
is a concrete, cheap test for any proposed representation: can it be copied bit-for-bit by a
process that does not understand it, and separately decoded by one that does?

#### 32. RepliBench: the same question asked of today's models
**Black S., Cooper Stickland A., Pencharz J., Sourbut O., Schmatz M., Bailey J., Matthews O.,
Millwood B., Remedios A., Cooney A. (UK AI Security Institute) — "RepliBench: Evaluating the
Autonomous Replication Capabilities of Language Model Agents", arXiv 2504.18565, v1 2025-04-21,
v2 2025-05-05.** **Abstract.**

Verbatim: *"RepliBench is derived from a decomposition of these capabilities covering four core
domains: obtaining resources, exfiltrating model weights, replicating onto compute, and
persisting on this compute for long periods. We create 20 novel task families consisting of 86
individual tasks. We benchmark 5 frontier models, and find they do not currently pose a credible
threat of self-replication, but succeed on many components and are improving rapidly."* And:
*"the best model we evaluated (Claude 3.7 Sonnet) has a >50% pass@10 score on 15/20 task
families, and a >50% pass@10 score for 9/20 families on the hardest variants."*

**What it says to our points — framing only.** It is the modern instance of entry 31's question,
and it is here because the brief asked for it. Two of the figures in the brief need correcting:
**five** frontier models, not seven, and **four** domains; and "released 2025-04-22" is the AISI
blog's date, not the arXiv v1 date (2025-04-21). See §I.9.

### I.9 Leads checked against their sources

Zcode's list, item by item, with what the source says.

- **AlphaEvolve arXiv 2506.13131** — correct (entry 27).
- **AI Scientist v2 arXiv 2504.08066** — correct, and the fuller story is entry 25. His summary
  ("accepted at an ICLR 2025 workshop through blind review, then withdrawn by Sakana who
  disclosed authorship") is right in outline; the source adds that reviewers were told in advance
  that 3 of 43 papers were AI-generated, which weakens "blind".
- **POET arXiv 1901.01753** — correct (entry 16). **Omni-EPIC arXiv 2405.15568** — correct
  (entry 17).
- **Darwin Gödel Machine arXiv 2505.22954 (Zhang, Hu, Lu, Lange, Clune)** — correct, author list
  exact (entry 26). But the brief also asked for "the DGM evaluator episode" as a reward-hacking
  case, and **nothing read here supports that**: the abstract describes safety precautions, not
  an exploit. Marked **not verified — lead only**.
- **RepliBench** — id is **2504.18565** (the brief gave none). Corrections: five models, not
  seven; four domains, 20 task families, 86 tasks; arXiv v1 2025-04-21, the 2025-04-22 date being
  the AISI blog's. "None passed end to end" is consistent with *"do not currently pose a credible
  threat of self-replication"*, but the paper does not use that phrasing, and the per-family
  pass@10 figures quoted in entry 32 show partial success is the actual result.
- **Xenobots kinematic self-replication — Kriegman, Blackiston, Levin, Bongard, PNAS 2021** —
  confirmed as **"Kinematic self-replication in reconfigurable organisms", PNAS 118(49)
  e2112672118, published 2021-11-29**, authors exactly as given. `pnas.org` returned 403; read
  instead at the PMC record of the same DOI (PMC8670470), **significance statement only**.
  Verbatim from it: *"Here we show that clusters of cells, if freed from a developing organism,
  can similarly find and combine loose cells into clusters that look and move like they do, and
  that this ability does not have to be specifically evolved or introduced by genetic
  manipulation."* The brief's parenthetical about anthrobots refers to a **different** paper and
  was **not checked**.
- **BAAIWorm (Zhao et al., 2024)** — the work exists, but under a different title and venue than
  the brief implies: **"An integrative data-driven model simulating C. elegans brain, body and
  environment interactions", Nature Computational Science, 2024**. **Not fetched** — this comes
  from the search listing only, so author list, volume and pages are **not verified**. Marked
  **lead only**. Note it is plausibly the same work §E already records as "integrative
  brain–body–environment C. elegans simulators (Nature Computational Science, 2024-12)".
- **FlyGM arXiv 2602.17997** — the id is correct and the paper is **already in this file as entry
  5**. Abstract re-read 2026-09-20: v1 2026-02-20, v2 2026-03-08, v3 2026-06-14; authors Jin Z.,
  Zhu Y., Zhang C., Sui Y. The claim that **synapse signs are assigned rather than measured** is
  **not in the abstract** and is **not verified here**; the abstract still gives neither the
  connectome release nor a neuron count, exactly as entry 5 says. The v3 abstract does add a
  claim entry 5 does not carry: *"We achieve stable performance across diverse locomotion tasks,
  as well as better sample efficiency compared to both graph and non-graph baselines."*
- **Fly brain on Loihi 2, "arXiv 2508.16453"** — **the id in the brief is wrong.** 2508.16453 is
  *"Anti-establishment sentiment on TikTok: Implications for understanding influence(rs) and
  expertise on social media"* (Xu T., Hasell A., Tomkins S.; accepted at ICWSM-2026), an
  unrelated paper — fetched and read to be sure. The Loihi work is **arXiv 2508.16792**, the id
  **already in §E of this file**: *"Neuromorphic Simulation of Drosophila Melanogaster Brain
  Connectome on Loihi 2"*, Wang F., Theilman B. H., Rothganger F., Severa W., Vineyard C. M.,
  Aimone J. B., submitted 2025-08-22. Abstract read; verbatim: *"we implement the whole-brain
  connectome of the adult Drosophila melanogaster (fruit fly) from the FlyWire Consortium
  containing 140K neurons and 50M synapses on the Intel Loihi 2 neuromorphic platform"*, fitted
  *"onto 12 Loihi 2 chips"*. §E is right; the lead was wrong.
- **OpenWorm "since 2011" against this repository's "since 2014"** — **Zcode is right, and both
  [idea_en.md](idea_en.md) and §E of this file are wrong.** The project's own history page
  (docs.openworm.org/fullhistory) records the idea as a tweet of **2010-01-01** — *"new year's
  resolution: simulate the whole C. elegans brain (302 neurons)!"* — and the naming in **early
  January 2011**: *"Stephen proposes the name 'OpenWorm' and the name sticks."* Neither
  `idea_en.md` nor §E is edited: `idea_en.md` is the record of what was said, and §A–§H are not
  rewritten by this pass. The correction lives here and should be carried wherever the date is
  next used.

#### Whether anything already *is* "a connectome-seeded lineage with inheritance"

Searched 2026-09-20 for prior work that evolves a lineage from a real connectome seed.
**Nothing peer-reviewed was found.** The search surfaced only public code repositories — hobby or
unreviewed projects — whose descriptions match the idea closely; **none was opened, none is cited
here, and their existence is not evidence of anything.** They are mentioned only so the next
person does not assume the search missed them. Two honest limits: one search engine, English
queries, one day; and an absent result is not an absent work.

What §E already establishes stands, and this section sharpens it. Connectome-*instantiated*
controllers exist (entry 5, FlyGM). Connectome-*constrained* trained models exist (entry 4,
flyvis). Whole-connectome *emulation* exists (2508.16792). Body-and-brain evolution with
inheritance exists and is 32 years old (entry 9, Sims). What was not found is the
**conjunction**: a heritable genome *derived from a measured connectome*, varied and selected
over generations, with the lineage recorded. The claim to novelty should be written as that
conjunction and nothing wider — in the spirit of the idea's own note that "first" is not true.

### What this changes for us

1. **Ark's genome track has a required reading list, not a blank page.** Before proposing a rule:
   Sims's directed graph (9), Hornby & Pollack's constrained L-system (10), CPPNs (11), HyperNEAT
   (12). HyperNEAT in particular is the existing baseline for "a rule that generates wiring,
   evolved rather than trained" — the gradient-free regime §F says the PNAS codec does not cover.
2. **Any proposed rule must survive von Neumann's two readings (31):** copyable bit-for-bit
   without interpretation, and separately decodable into a phenotype. One line, and it kills
   representations early.
3. **Every heritable element needs a birth id that is never reused or renumbered (18).** NEAT's
   historical markings are the difference between "glue two ancestors' modules" working and
   producing damaged offspring — and the same ids are what make the tree computable. Cheapest
   decision on this list, and it has to be made before a genome is written.
4. **The indirect encoding is a bet with a measurable threshold (13).** Below a regularity level
   an indirect encoding loses to direct weights, and the seed's regularity is a measurable
   property of the fly's wiring, not an assumption; Clune et al. show how to measure it. They also
   show the likely endgame is HybrID-shaped — rule plus refinement — and if the refinement is not
   heritable then the tree records the rule only, which the artefact's design must state.
5. **Design against premature morphological convergence (15).** Without protection, gross body
   change stopped after 1 % of the run, and retuning the morphology mutation rate did not fix it.
   Point 2 needs morphological innovation protection or an equivalent — the same mechanism §D's
   mis-ranking result asks for from the other side.
6. **Design against a hand-written curriculum (16).** POET's own control condition *is* a
   direct-path curriculum builder, and it loses. Treat fly → beetle → quadruped as a baseline to
   beat, not as the plan.
7. **The diversity archive is load-bearing, and probably cannot be one objective among six
   (19, 20).** Novelty beat the objective 39/40 against 3/40 on the deceptive maze, and the
   weighted-in variant was much weaker (11/40). MAP-Elites is the better archive shape here
   because its cells are named by the designer — limb count, fraction of fly-inherited modules —
   which is also a readable axis for the artefact.
8. **The noisy-selection problem is 2005-vintage, has named cures, and has no default (21, 22,
   23).** Re-sampling against larger population is explicitly unsettled under a fixed budget, so
   our choice is a registrable decision with a falsifier. Sudholt gives the one provable lever
   (offspring population ~log n) and the threshold shape. Hyperband reframes the registered
   question usefully: not "does the cheap score rank?" but "at what horizon can the bottom
   fraction be discarded without losing the winner?" — which is nearer §H's "does it find the
   top?".
9. **The tree artefact should borrow three specific things.** Tierra's entry criterion — a
   genotype is recorded only after it replicates twice with at least one identical offspring (29)
   — and its minimal node record (name, immediate ancestor, time of origin). Lenski et al.'s two
   experiments (28), knockout and ancestral reversal, without which an edge in the tree is a
   drawing and not a finding. And Phylotrack (30), so format, metrics and memory bound are not
   re-invented here.
10. **State the novelty as a conjunction, and say plainly what our evaluator cannot do.** Nothing
    peer-reviewed was found that is a connectome-seeded lineage with inheritance, but every
    conjunct exists separately and one of them is from 1994 (9). On the evaluator: AlphaEvolve
    works because its fitness is *provably correct* (27) and the DGM because its fitness is an
    external benchmark (26). §H's point — that this programme has no independent arbiter anywhere
    — is exactly why those successes do not transfer, and it should be written that way rather
    than cited as encouragement.

### §I — what was NOT verified, and where fetches failed

- `pnas.org` returned 403 (Xenobots); read at PMC8670470 instead, **significance statement only**.
- `direct.mit.edu` returned 403, so **Cheney N., Bongard J., SunSpiral V., Lipson H. — "On the
  Difficulty of Co-Optimizing Morphology and Control in Evolved Virtual Creatures", Proceedings
  of the Artificial Life Conference (ALIFE) 2016, MIT Press, pp. 226–233** was **not read at
  source**. It is the paper that first analysed premature morphological convergence; entry 15 is
  the follow-up by the same authors and carries every quote used here. Marked **not verified —
  lead only**; do not cite its findings until it is opened.
- `api.semanticscholar.org` returned 429.
- `eplex.cs.ucf.edu` now 302-redirects to an unrelated domain which 404s; entries 11, 12 and 19
  were read from Wayback copies of the author preprints. Journal volume/page lines are given only
  where the preprint itself carries them.
- Entries 14, 16, 17, 20, 23, 24, 26, 27, 30 and 32 are **abstracts only**. No number from any of
  them beyond what is quoted above should be used.
- Nature (entry 28) was read from a course copy of the published article, not from nature.com.
- **BAAIWorm** was not fetched at all — search listing only — and is marked lead only.
- Nothing in this section carries a result value from this repository's own experiments.
  `literature.md` is not on `docs/blind-author-exclusions.txt` (checked 2026-09-20, 86 lines,
  68 files) and this section keeps it that way.
