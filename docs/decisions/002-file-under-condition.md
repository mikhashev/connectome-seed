---
adr: 002
title: "Treat connectome-seed as a file under a condition, and make the condition one pre-registered experiment"
status: accepted
date: 2026-09-13
deciders: [Mike]
consulted: [Johnny, Ark, Warren, CC]
informed: []
depends_on: []
related: [ADR-001]
supersedes: []
session: DPC Research group thread, 2026-09-13 05:57–07:31 UTC
axis: honesty
---

## Context and Problem Statement

The idea (`idea.md`): grow a lineage of artificial organisms from a heritable grammar
extracted from a real connectome, with USPEX-style operators on the living graph, a short
"youth" of plasticity before evaluation, and multi-objective selection. Four readers examined
it on the day it was posted. All four reached the same verdict from different directions, and
two of the thread's own claims did not survive checking. This ADR records the verdict, the
condition that would change it, and what the first experiment must look like for its result
to be readable.

## Decision Drivers

- **The author's own next step is the condition of the project's existence.** "Formalise the
  genome representation" is not a task; without composition under crossover and a notion of
  growth, the genome is a graph, not a grammar (Johnny).
- **Three requirements pull apart** — compression, composability, expressivity — and under
  them interfaces, no cheap validity oracle, pleiotropy (Ark).
- **Two independent literatures locate the weak step at the same place**, verified at
  source: correct ranking needs *more* controller optimisation, and cheap evaluation
  *"regularly undervalue[s] individuals with newly mutated bodies"* (Mertan & Cheney, arXiv
  2508.17464, §3.1, §4.2); the published circuit-to-genome codec works only with gradients
  reaching the genome each generation — *"a form of Lamarckian evolution … biologically
  unrealistic"* — and the gradient-free path is *"slow and inefficient"* (Shuvaev et al., PNAS
  2024, p. 9).
- **The thread's compute objection did not hold**: the estimate was two orders of magnitude
  off on its own inputs and counted neuron ODEs rather than body physics and the youth phase;
  on this machine the cost is a window, not a cluster (CC).
- **The USPEX analogy breaks where it thinks it is strongest**: DFT enthalpy is a physical
  quantity nobody chooses, fitness here is written by the author; DFT relaxation converges to
  something physical, "youth" minimises a training loss (Ark).

## Decision

**connectome-seed is a file under a condition, not a project.** The condition:

> **Show that a cheap evaluation of an individual is consistent with an expensive one.**

Not "when a genome representation exists" — its absence is the symptom. The condition is one
experiment on flyvis (Lappalainen et al., Nature 2024; the optic-lobe motion circuit at cell-type
level, code public), run **only after a written pre-registration** that fixes: what *cheap*
and *expensive* are in iterations; the number of individuals and seeds; the rank-correlation
statistic and its threshold at that N; the decision rule for each outcome; and the named
prediction for composition. Two hypotheses are registered **separately** — (a) a spliced
module behaves predictably, (b) cheap agrees with expensive — because a result on one says
nothing about the other. The splice joins two *different* things; two identical copies is a
control that can only pass.

**Order of execution (Mike, 07:20 UTC):** verify the whole flow first; long runs overnight.
**Roles (Mike, 07:27 UTC):** CC executes everything; Ark, Johnny and Warren review.

### Rationale

Both outcomes are results only if the numbers are fixed first. A negative extends 2508.17464
from a 3×3 voxel grid and a 1,417-parameter controller to a real circuit on 65 cell types; a
positive means the loop has a middle and the idea becomes eligible. Without pre-registration
either outcome can be read either way — the same failure this team already met once when a
kill criterion was quietly re-labelled as a ladder rung (`autoresearch-win-rtx`, K1).

## Considered Options

- **Start the project** — write the grammar, build the evolutionary loop. Rejected: the
  representation does not exist, and the weak step is documented in two fields.
- **Close the idea** — rejected: the same paper that measures the failure of cheap evaluation
  shows co-optimisation reaching morphology–controller pairs a fixed body cannot; the data
  (male CNS 2026, FlyWire, zebrafish with activity) are not the blocker; the tooling exists.
- **File under a condition, test the condition** — chosen.

## Consequences

- **Positive:** one cheap, bounded experiment with a pre-declared reading; either result is
  publishable at its honest size.
- **Negative:** nothing is grown until it runs; the idea's most attractive part (the tree) waits.
- **Neutral:** flyvis is built from FIB-25/FIB-19, not FlyWire — the same biological circuit,
  a different connectome release. Irrelevant to the composition test; relevant to the phrase
  "seed from FlyWire", which the idea uses and this repository does not.

## Confirmation

- [x] The pre-registration file exists with all five items as numbers, and was reviewed
      before the first GPU iteration. — `docs/preregistration-cheap-vs-expensive.md`,
      committed `8fd1d8a` on 2026-09-13, reviewed by Ark at 15:45 UTC and Zcode at 16:24 UTC
      the same day, pre-launch edits applied on Mike's word at 17:06, the file itself
      recording "run 0 not yet started". **One precision, since the box says "before the first
      GPU iteration":** the 24-iteration *cost probe* ran that morning at 11:19, before the
      review; the first *training* run began after it. Ticked on that reading — the probe
      measured the price of an iteration and tested no hypothesis — and the ambiguity is
      recorded rather than resolved silently (CC, 2026-09-19).
- [x] Hypotheses (a) and (b) have separate decision rules in that file. — its §1 is "Purpose
      and the two hypotheses, kept separate", §4 is the statistic and threshold for (b) alone,
      §5 is "Decision rules, both outcomes".
- [x] The first GPU iteration's cost is recorded before any overnight run is scheduled. —
      2026-09-13, **0.0619 s per training iteration** (n = 22, min 0.0589, max 0.0694), on
      Mike's word that the card was free; every night was scheduled after it (ROADMAP Phase 2
      item 1).

## Status of the condition — 2026-09-19, after five nights

**The condition is not met, it is not refuted, and it has been found to be underspecified.**
Recorded here because this ADR is what the project's existence hangs on, and because none of
the three statements below chooses a branch.

1. **The expensive side does not rank.** Ten runs exist — six individuals, two of them run
   three times. Pooled replicate SD **5.9316 on 4 df** against a between-individual SD of
   **5.2717 on 5 df**: ratio **0.889**, below one. Two runs of the same individual scatter at
   least as much as six different individuals do. Before night 5 this stood on one pair of
   runs; it now stands on four degrees of freedom and says the same thing
   ([experiment 005](../experiments/005-night5-third-runs-of-seed-0-and-seed-3.md)). The 95 %
   intervals overlap almost entirely, and the result is fragile to one run of the ten — a
   statement about n = 3 per individual, not a licence to drop that run.
2. **"Consistent with" was measured across two regularisation regimes.** `activity_penalty`
   acts on `nodes_bias` alone — the 65 cell-type biases, the only parameters a seed moves —
   for the first 150,000 of 250,000 iterations. The cheap probe sits at 25,000, inside that
   regime; the expensive rung at 250,000, outside it. "The cheap estimate is uninformative"
   and "the cheap estimate is informative about a differently-regularised system" are two
   different failures with the same symptom, and the design cannot separate them.
3. **One alternative endpoint was registered, read once, and closed.** Iterations to cross a
   fixed level — the form USPEX uses — returned **`TEST UNREADABLE`**: its own resolution
   floor removed 16 of 23 levels, all on the twin side
   ([results/diagnostics/reachability/](../../results/diagnostics/reachability/)). It will not
   be re-read, because every reviewer has seen the numbers and a corrected rule would be
   fitted to them. A v2 belongs on a substrate that does not exist yet, authored by someone
   who has not seen these — see [ADR-003](003-blind-authorship-after-the-numbers.md).

**What this ADR does not do here.** It does not reformulate the condition and does not choose
between abandoning the cheap side and changing the population. The next question is free and
comes first: the 72 checkpoints per run already on disk can say whether a probe placed *after*
150,000 predicts the final better than one at 25,000. If it does, the mismatch was where the
probe was put, and the substrate need not be touched at all.

## Open Questions

- **Q1 — decided 2026-09-13 (Mike): K = 1 to begin with.** Run 0 is one full run to
  convergence; it fixes the price of the expensive evaluation on this card and yields one
  converged reference individual. It cannot test hypothesis (b) — a rank correlation needs N
  individuals — so N for the test is set by rule from run 0's measured cost (as many full runs
  as fit one night, not below 8), in the pre-registration.
- **Q2:** What is spliced — two ensemble members, or two cell types. — pre-registration
- **Q3:** Whether a datamate fix goes upstream (`github.com/flyvis/datamate`, same
  organisation as flyvis) or stays a local patch. — CC, after the test

## Authors

- **Mike** — Decision, the order of execution, the roles
- **Johnny** — the "not a project" verdict; the demand for pre-registration with numbers
- **Ark** — the three-requirement diagnosis; the two-sided reading of both sources; the
  separation of (a) from (b); the identical-copies objection
- **Warren** — the same points from the cost side; the article scope
- **CC** — the compute correction, the literature read at source, the flow verified on this
  machine, this record

## References

- `literature.md` §D (2508.17464, full text) and §F (PNAS, p. 9) — the two grounds
- `ROADMAP.md` Phase 1–2 — where the condition is executed
- `chat/` (local) — the thread, 67 → 84
