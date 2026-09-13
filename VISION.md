# Vision — connectome-seed

**Date:** 2026-09-13
**Authors:** Mike Shevchenko (the idea, every decision), CC (this text), Ark / Johnny / Warren (review)
**Source:** the DPC Research group thread of 2026-09-13, saved verbatim under `chat/` (local only)
**Status:** living document. What is decided lives in `docs/decisions/`; what is being done lives in
`ROADMAP.md` and `backlog.md`; what is known lives in `literature.md`. This file says what we
are trying to find out and why, and nothing else.

---

## The goal in one paragraph

Grow a **lineage of artificial organisms from a real connectome** — not by emulating a fly and
calling it something larger, but by taking the *heritable grammar* out of the connectome (cell
types, excitatory/inhibitory balance, recurring motifs, sensorimotor loops), letting body and
nervous system develop together along a curriculum, and selecting on a multi-objective
fitness after each offspring has had a short period of plasticity. The artefact that matters is
the **evolutionary tree** — which module was inherited, where a line diverged, which skills
survived a change of body — not a single video of something walking. The original statement
of the idea is in [idea.md](idea.md), verbatim.

## The operating principle: the loop has a middle, and the middle is unproven

Every version of this idea has the same shape:

```
heritable material → development → a short, cheap adaptation ("youth") → evaluate → select → inherit
```

Two independent literatures, read at source on the day this folder was created, say the same
thing about the third step from different sides:

- **Evaluation.** On the smallest possible design space (a 3×3 voxel grid, 1,305,840 bodies),
  correctly ranking bodies required *more* controller training, not less; evolutionary
  algorithms *"regularly undervalue individuals with newly mutated bodies and eliminate
  promising morphologies"* — and the same paper shows co-optimising body and controller reaches
  solutions a fixed body cannot. (Mertan & Cheney, arXiv 2508.17464.)
- **Inheritance.** The one published codec that compresses a circuit into a genome by several
  orders of magnitude (322× at 94 % innate accuracy) does so with **gradients reaching the
  genome every generation** — its authors call that Lamarckian and biologically unrealistic,
  and call the gradient-free path *"slow and inefficient"*. (Shuvaev, Lachi, Koulakov, Zador,
  PNAS 2024.)

So the principle this project runs on is not "seed from a connectome" — that part is done by
others (flyvis; the whole-brain connectomic controller of a biomechanical fly). It is:

> **Before anything is grown, show that a cheap evaluation of an individual is consistent with
> an expensive one.** If it is not, the loop has no middle and nothing above it is worth
> building.

That is the condition in [docs/decisions/002](docs/decisions/002-file-under-condition.md). It is one
experiment, it is pre-registered before it runs, and both of its outcomes are results.

## What "expert", "module" and "seed" mean here

- A **module** is a typed sub-circuit — a set of cell types and their average connectivity —
  not a set of individual neurons. This is the level flyvis already works at (cell types with
  retinotopic tiling; the cell *count* is a lattice parameter, 45,669 at `extent=15`, 5,759 at
  `extent=5`). It is the right level for a grammar and the wrong level for within-type
  specificity, and the project says which of the two it is claiming at every step.
- A **seed** is a grammar extracted from a connectome, not the connectome. The connectome is
  the *product* of development; the genome is the *process*; inverting one product into a
  process is underdetermined, and the missing representation is the hole named by every reader
  of the idea, the author included.
- **Cheap** and **expensive** evaluation are numbers of training iterations, fixed in writing
  before a run, never chosen after seeing a result.

## What this is not

- Not a claim of "first": OpenWorm (2014), integrative C. elegans brain–body–environment
  simulators (2024), whole-fly-brain emulation on neuromorphic hardware (2025) and a
  connectome-as-controller fly (2026) all precede it.
- Not an answer to the storage-vs-addressing question of the sister track
  (`autoresearch-win-rtx`). This design keeps knowledge *outside* the weights; it is not
  evidence about whether a model reads knowledge from its own parameters.
- Not a project yet. A file under a condition, with the condition written down.

## How the team works on it

Mike decides. CC executes everything — code, runs, documents. Ark, Johnny and Warren review.
Every claim in this repository carries its status — **Observed** (a file or a run, with the
path), **Reported** (a colleague's observation, not re-checked by the writer), **Inferred**
(reasoning, with the check that would settle it named) — because on this track four design
conclusions reached by reading were refuted by running within a single day, three times by
different authors. A conclusion here without execution behind it waits for a probe rather
than a vote.
