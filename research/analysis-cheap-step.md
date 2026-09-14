<!-- imported from Ark's sandbox C:/Users/mikha/.dpc/agents/agent_001/research/analysis-cheap-step.md, sha256 007dbf5976a272cd9c5be639a1d9dafaf46504cfd8d30684ac289c4d9d0b83b4, mtime 2026-09-13 18:02:00 UTC, imported by CC on Mike's word 2026-09-13 18:09 UTC; content unchanged below -->
<!-- line references to S2 corrected to 848–852 on 2026-09-14 (Ark's own correction, chat 2026-09-13 18:25 UTC; verified by CC) -->


# The cheap step in the middle of the loop

**Status:** analysis, not a plan. Nothing here has been run.
**Author:** Ark (agent_001), 2026-09-13.
**For:** `connectome-seed` — read together with `preregistration-cheap-vs-expensive.md`.
**Purpose:** record why the *cheap estimate of an individual* is the unproven step, and how far that claim
extends — so that a month from now the sources are quoted on both halves, not one.

---

## Sources

| # | Source | How far read | Copy |
|---|---|---|---|
| S1 | Mertan & Cheney, *Evolutionary Brain-Body Co-Optimization Fails to Select for Morphological Potential*, arXiv 2508.17464 (v2, 2026-08) | full HTML, §1–8 | `2508.17464_full.md` |
| S2 | Shuvaev, Lachi, Koulakov, Zador, *Encoding innate ability through a genomic bottleneck*, PNAS 2024 | full text, pp. 1–12 | `pnas_genomic_bottleneck_full.md` |
| S3 | DeepMind, *AlphaGenome Atlas* (blog + PDF) — cited only for the taxonomy in §4 | blog + PDF, pp. 1–2 line-by-line; rest paged | `alphagenome-atlas_full.md`, `alphagenome-atlas-notes.md` |

Line numbers below refer to the local copies. Labels: **Observed** = read in the source at the cited place;
**Inferred** = my reading, not the authors'. Where a figure is quoted from the earlier full read of the same
file and was *not* re-verified in the final pass, it is marked **[not re-checked]** — see §7.

---

## 1. The one formulation both sources arrive at

> **The expensive step is where the result is born. The cheap step in the middle of the loop is unproven.**

S1 (Observed). §6 — the paper's own summary of its finding (local copy line 190):

> *"it is not possible to rank high-performing individuals early in evolution (as it requires more controller
> optimization to estimate their fitness well, as shown in Fig. 1)"*

And the contribution bullet, line 30:

> *"ranking high-performing individuals correctly requires extensive controller training and hypothesize that
> this need, combined with fragile co-adaptation, hinders the optimization of morphologies in evolutionary
> brain-body co-optimization by creating dynamics leading to first-mover advantage."*

S2 (Observed). Local copy lines 851–856:

> *"The feedback in our algorithm that guides the gradient from each generation—the fact that the trained
> weight matrix in the kth generation is used to modify the genome in the (k + 1)st generation—can be viewed
> as a form of Lamarckian evolution, and is, as such, biologically unrealistic."*

and lines 848–851:

> *"…of optimization that does not exploit a gradient, is in general a relatively slow and inefficient
> algorithm, successful because it operates on massive numbers of individuals in parallel over [hundreds of
> millions of years]."*

Two different objects — a controller for a voxel body, a weight matrix for a network — one shape of loop:
**individual → estimate → edit the inherited material.** In both, the cheap version of *estimate* is what
the loop is betting on, and in neither is it shown to work.

---

## 2. The number that makes it concrete

S1 mapped the morphology-fitness landscape **exhaustively** (Observed, lines 15 and 72):

- design space: 3×3 voxel grid, at most 9 voxels, **1,305,840 distinct viable morphologies** (Evogym);
- landscape built with **300 generations of AFPO** (line 72); population 20 per algorithm
  **[not re-checked — read in the earlier pass, Table 1]**;
- the controller is a small MLP, on the order of a thousand parameters **[not re-checked]**.

Arithmetic (mine, **Inferred** — not stated in the paper):

```
1,305,840 morphologies × 300 generations × population 20  ≈  7.8 × 10⁹ evaluations
```

This was funded by NSF 2239691 / 2218063 and the Vermont Advanced Computing Center (Observed, §8) — and it
*still* was not enough for the top of the range, so a second pass was bolted on: **10,000 further
generations** over the same morphologies (Observed, §4.1 line 125; 94,201 morphologies updated there
**[not re-checked]**).

Why this matters more than anything else in the two papers: **the idea proposes to make cheap exactly the
operation that is measured here to be expensive — and measured in the smallest possible space.** Billions of
evaluations for a 3×3 grid.

Downstream outcome in the same space (Observed, line 32): search at times *"stagnates at points in the
morphology-fitness landscape that are not even a local maximum"*, and the algorithms *"consistently undervalue
the fitness of offspring with newly mutated bodies"*. Rates per algorithm (17/100 AFPO, 22/100 MAP-Elites,
13/100 MIP; 38/100 MAP-Elites runs stagnating) **[not re-checked]**.

**Inferred:** scaling 7.8×10⁹ upward is not linear. In S1 the cheap side was a small controller. In the
connectome-seed idea the cheap side is training a plastic controller over a developed nervous system —
orders of magnitude more expensive per individual. That is where "a short youth" stops being short.

---

## 3. The second half of each source, which must travel with the first

Both papers have a positive side. Quoting only the objection is the error we keep catching in ourselves.

**S1 is not only negative.** Observed, abstract and §5 (line 176):

> *"co-optimizing morphology and control creates useful goal-switching, yielding morphology-controller pairs
> whose performance cannot be reached by optimizing the controller alone for a fixed morphology"*

> *"Fig. 9 shows that in two out of five cases, control-only treatment is unlikely to achieve the same level
> of performance as co-op treatment."*

So co-optimization **does** reach what fixed morphology cannot — and the authors themselves call the
comparison unfair (3 algorithms × 100 runs × double budget against 10 runs; Observed, line 184).

**S2 is positive, and paid for with a gradient.** Their 322-fold compression holds because the gradient
reaches the genome **every generation** — that is the mechanism, not a side note. And they supply the
counterweight themselves (Observed, lines 1667–1679): the *net* effect is *"similar to Darwinian evolution"*,
the trait becomes *"genetically assimilated"* — the Baldwin effect. Quote both halves or neither.

**Boundaries of the linking (Inferred):** S1 is 2D voxels, one controller, locomotion. S2 is supervised/RL
benchmarks, not organism development. What they share is the **form of the loop**, not the object.

---

## 4. Three kinds of "cheap estimate" — and which one we are testing

Kept separate because conflating them is easy and costly.

| kind | mechanism | cost structure | evidence |
|---|---|---|---|
| **1. Prefix of the same process** | stop early (1k / 5k / 25k of 250k) | nothing extra; the surrogate *is* the expensive thing, truncated | S1 — shown **not** to rank correctly |
| **2. Learned surrogate** | train a model on expensive measurements, then predict | pay once for the training set, predict forever | S3 AlphaGenome — **works** |
| **3. Mechanistic reduction** | replace the expensive simulator with a cheaper correct model | pay once for the reduction | not used in this track (listed for completeness) |

**Our preregistration tests kind 1.** AlphaGenome's success licenses kind 2 — not kind 1. This distinction
is the difference between "someone solved this" and "someone solved a different version of this".

S3 is also the largest recent instance of the *argument* being identical to ours (Observed, blog):

> *"With roughly 9 billion possible single-letter mutations in the human genome, testing each one in the lab
> is practically impossible."*

Expensive measurement unavailable → cheap substitute. Same move. Three conditions make it work there and are
absent here (Inferred): a surrogate trained on **real measured labels**, a **finite small** space
(3 alternatives × ~3×10⁹ positions), and **one fixed input** (the human genome). And S3 has **no loop** — no
population, no selection, no inheritance; enumeration replaces evolution. It is a catalogue of effects, not
a developmental loop.

One usable idea from S3 (Inferred, **proposed — not registered**): they rank everything cheaply and verify
only the **top** experimentally (*"used AlphaGenome Atlas to identify and experimentally verify key
variants"*; one DNM1 variant was confirmed). That suggests splitting hypothesis (b):

- **b1 — agreement of the full ranking** (what the preregistration currently specifies);
- **b2 — hit in the top-k**, a weaker claim, closer to what AlphaGenome actually relies on.

S1 does not kill b2 — it never tested it. Decision belongs to Mike, and to *before* the N-night, not after.

---

## 5. The structural weakness that is ours alone

S3's expensive side is an **external** measurement — a lab experiment. S1's is a longer simulator run, but
its population is generated by the same simulator, so at least the ranking procedure differs.

Ours is neither: our "expensive" estimate is **the same simulator, run longer**. There is no independent
arbiter anywhere in the loop (Inferred). That is a weakness of the whole track, not only of this test, and it
should be named in the article rather than found by a reviewer.

---

## 6. What this implies for the test and the article

The test as specified (cheap prefix vs expensive full run, Spearman agreement over N individuals) is a
**direct extension of S1 to a richer substrate** — 65 cell types, ~1.5M synapses, a real optic-lobe circuit,
against a 3×3 voxel grid. Both outcomes are publishable **provided the preregistration holds**:

- **Negative** — the finding generalises beyond toy spaces: the assumption much of developmental
  neuroevolution is built on does not hold where the loop actually runs.
- **Positive** — a cheap estimate *is* viable on a biological substrate, which licenses a class of
  experiments currently out of budget reach.

The one-line claim for the article, and it is **not** about a fly:

> In both fields, correct estimation of an individual in the middle of a developmental loop costs so much more
> than a cheap one that the cheap one ranks it wrongly — and in neither field has a surrogate been shown to
> agree with the expensive estimate.

Second line, ours:

> In the smallest possible space (a 3×3 grid) the price of correct ranking has been measured — on the order of
> 10⁹ evaluations on an HPC allocation — and the top of the range still could not be ranked.

**Article boundaries to state:** S1 is 2D voxels, one controller, locomotion; S2 is supervised/RL benchmarks,
not development; the link between them is the form of the loop, not the object (Inferred).

---

## 7. Verification log for this file

**Re-verified in the final pass** (pattern searched in the local copies, line numbers as reported):
S1 lines 15, 30, 32, 72, 125, 176, 184, 190; S2 lines 848–851, 851–856, 1667–1679, 1779–1781.

**Quoted from the earlier full read of the same file, not re-checked in the final pass** (marked in place):
S1 population size 20; controller parameter count; 94,201 morphologies in the §4.1 update; per-algorithm
success rates and the 38/100 figure. These are the numbers to confirm before they enter the article.

**Not verified at all:** the 500-simulation-step evaluation budget (stated in an earlier message, not
located in the copy on disk — treat as unconfirmed); any figure from S3 beyond the blog and the first two
pages of the PDF.

**Explicitly not claimed by this file:**
- that the connectome-seed *idea* is disproven — it is not; the loop's middle step is untested, which is a
  different statement;
- that prefix estimation cannot work at *any* scale — only that it has been measured not to work in the one
  place anyone measured it, and that nobody has shown it working;
- that S3's three conditions are the only relevant ones — they are the three visible from the blog and the
  first two pages of the PDF.

**Open:** (1) whether (b) splits into b1/b2 — Mike, before the N-night; (2) whether this file is published
inside the repo or kept as a working note; (3) PDF provenance for S3 (release / snapshot) — the blog copy on
disk is undated.
