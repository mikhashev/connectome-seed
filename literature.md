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
