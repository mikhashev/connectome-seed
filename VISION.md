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
The five points, the artefact and the author's own named first step are there verbatim and are the
goal; this paragraph is a summary of them and not a substitute (Mike Shevchenko, author,
2026-09-12 12:18). Restated by him as the project's description on 2026-09-19 —
**"to learn to make an elephant out of a fly"** (translated from Russian) — which is the
idea's own opening distinction ("not 'emulate a fly and call it an elephant'") promoted from a
disclaimer to the goal.

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

### The two lines, and why both exist — 2026-09-19

The condition above is not a rival of the idea's point 1; it is the idea's point 4 turned into a
test. Point 4 says each offspring gets a short "youth" of limited plasticity and *only then* is
fitness measured — that is the cheap evaluation and the expensive one, named by the author before
any of this was built. The idea's own annotation records that this is precisely the mechanism
arXiv 2508.17464 measured as the source of mis-ranking (`idea.md`, closing note, 2026-09-13). And
the main artefact is a tree (point 5's selection, point 2's lineage): a tree selected by an
instrument that cannot tell two individuals apart is a tree of noise. So the measurement is what
makes a grammar's result readable, not a detour from it.

**Which is the main line.** *Ark, reviewer, DPC Research group, 2026-09-19 11:11 UTC:* "if the goal
is the elephant, then the grammar is the main line and measuring the fly is instrumentation." That
is Ark's reading, and CC's record of the same day agrees with it. **The owner confirmed it** —
*Mike, owner, 2026-09-20 09:27 UTC:* the grammar is the main line and the measurement runs as its
instrument. The narrower fact that preceded the confirmation: on 2026-09-19 Mike chose the grammar
track as the one to run next (*Mike, owner, DPC Research group, 2026-09-19 14:45 UTC*), the track
that needs no GPU and is not blocked by the nightly accrual; the blind-authored second registration
of the reachability endpoint is deferred, not cancelled
([ADR-003](docs/decisions/003-blind-authorship-after-the-numbers.md)). **Later the same day, at
10:15 UTC, the owner paused the measurement line** — "Pause the fly → grammar (point 1)" — so the
two no longer run together: the grammar track continues, the measurement line is paused, not
cancelled, until the owner resumes it.

**The order lifts nothing.** Nothing is grown until Phase 2 has a number (`ROADMAP.md`, "Not on this
roadmap, deliberately"): the grammar of point 1 is *designed* now, and points 2, 3 and 5 — body and
brain growing together, the USPEX operators, the multi-objective fitness on held-out arenas — are
designed for and not run. The reason is the one this file already gives from the other side: an
elephant cannot be designed by a team that cannot yet weigh a fly.

*(The decision is recorded as
[ADR-004](docs/decisions/004-grammar-is-the-main-line.md); this paragraph is a summary and not the
decision record.)*

### What the condition looks like after five nights (2026-09-19)

Two things were learned that change how the condition must be read. Neither settles it.

**The expensive side is not a fixed reference.** Ten runs now exist — six individuals, two of
them run three times. The spread between two runs of *the same* individual is at least as large
as the spread between six *different* ones: pooled replicate SD **5.93** on 4 degrees of freedom
against a between-individual SD of **5.27**, a ratio of **0.889**, which is below one
([experiment 005](docs/experiments/005-night5-third-runs-of-seed-0-and-seed-3.md)). Before
night 5 that comparison stood on a single pair of runs; it now stands on four degrees of freedom
and says the same thing. So "consistent with an expensive one" presumes an expensive evaluation
that ranks — and on the final loss, it does not.

**And the question was underspecified.** flyvis applies an activity penalty to the 65 cell-type
biases — the only parameters a seed moves — for the first 150,000 of 250,000 iterations, and then
never again. The cheap probe sits at 25,000, **inside** that regime; the expensive rung at
250,000, **outside** it. So "does the cheap estimate agree with the expensive one" was being
measured as "does it agree with one taken under different regularisation". Two different failures
wear the same symptom, and the design as it stands cannot tell them apart.

**One alternative was tried and closed honestly.** A reachability endpoint — iterations to cross
a fixed loss level, the form USPEX uses — was pre-registered and read **once**. It returned
`TEST UNREADABLE`: its own resolution floor removed 16 of 23 levels, all on the twin side. Not a
pass, not a failure; the instrument reported that it could not read. It is closed in that form
and will not be re-read, because a rule chosen after the numbers are visible is a rule fitted to
them.

**What this does not say.** It does not say the project is refuted, and it does not choose a
branch. It says the condition is harder than it was written, that the cheap and the expensive
side must first be defined in one regime, and that the next question — whether a probe placed
*after* 150,000 predicts the final better than one at 25,000 — costs nothing, because the
checkpoints are already on disk.

### And what it looks like one day later (2026-09-20)

The section above stands; three things beneath it moved, and one of them removes a reason the
section gave. Numbers are not restated here — each item names the file that carries them.

**The second half of "the question was underspecified" has weakened, and the owner has decided
what follows from that.** The penalised quantity itself was read once, across its own boundary,
with the rule's branches written before the first value:
`results/night5/diagnostics/rowB/PENALISED-QUANTITY-READING.md`. It is smooth through 150,000 in
all ten runs, and held-out loss shows no step there either — so by the time the penalty is
dropped it was no longer holding the network, and "the cheap and the dear estimate live in two
regimes" is not the sharp contrast it was written as. What survives is narrower and is still
open as its own question: at 25,000, where the cheap probe sits, the penalised quantity is
markedly higher and more variable in most runs, so **the cheap probe is taken while the system is
still unsettled**. On that reading **`activity_penalty.stop_iter` is left untouched** — Mike,
owner, 2026-09-20. (A "loss step at 150,100" claimed in the thread was seconds per iteration, not
loss: the two timing sub-gates of `docs/briefs/2026-09-17-night5.md` §4.4, which exist precisely
because dropping the penalty optimiser changes the per-iteration cost and not the network.)

**The expensive side's non-ranking now has a mechanism, and it is ours rather than the
individuals'.** Replicates of one seed are copies of one config to the last field: identical at
iteration 0, apart by under one float32 step at iteration 12, and apart by the whole replicate
gap at the end. The same GPU operation order that makes a single evaluation non-repeatable —
driven to exactly zero when deterministic algorithms are switched on, in every pair of the full
row B run, with the registered control never amended
(`results/night5/diagnostics/rowB/README.md`) — runs uncontrolled for 250,000 training
iterations. Determinism on the training path was measured for the first time this session: about
3.33× slower, no operator refusing, and the same seed twice bitwise identical over 2,000
iterations (`docs/briefs/2026-09-20-night6-deterministic-pairs.md`). So the replicate spread the
section above reports is a property of how we train, not a property of an individual — which
makes the condition harder again, not easier, because switching determinism on would drive that
spread toward zero and ratify the method instead of testing it (Ark's trap, named before the
measurement).

**And an individual does show somewhere — in a shape, not in a level.** Row B's 65-type profiles
were read once, the reading rule hashed before any value was opened
(`results/night5/diagnostics/rowB/PROFILES-READING.md`). Before training, replicates of one seed
are identical, so the whole replicate gap is made inside training; at the end, replicates
resemble each other by the rank **shape** of the profile and not by its **magnitude**, and not by
held-out loss. The declared answer was MIXED and is reported as MIXED. Two readings of it are
kept side by side and neither is chosen: *Ark, reviewer, 2026-09-20 09:45 UTC (translated from
Russian)* — count by margin rather than by wins, one "win" is a tie at printed precision, the
shape result rests on one individual of two when each pair is judged against the nearest foreign
run, pairs within an individual are not independent so the denominator is individuals, and the
rank order of types at the start is set by the connectome rather than by the seed; and a later
descriptive recomputation by CC over the last 29 checkpoints — post hoc, description only, never
a verdict — in which loss and magnitude put replicates as far apart as different individuals
while shape puts different individuals about twice as far apart as replicates, for both
individuals that have replicates.

**What this does not say.** It does not choose a branch and it does not settle the condition. It
says that the instrument's own contribution to the spread is now identified and measurable, that
the regime argument is weaker than it was written, and that if an individual is to be *defined*
at all, shape is the candidate the data point at. The proposed next step — a perturbation ladder
under deterministic training, to measure how fast the system forgets its initial condition — is
**not authorised**; the night that was authorised was not launched, because under determinism the
replicate spread is undefined rather than zero and there would be nothing to compare against.
Session record: [docs/retrospectives/2026-09-20-session-close.md](docs/retrospectives/2026-09-20-session-close.md).

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
- A **grammar** — point 1 of the idea, and the thing the restated goal asks us to learn to write —
  is a rule that *produces* the wiring table: which cell types exist, which pairs connect, at which
  offsets, with which signs. By that test the substrate we run on holds exactly one production —
  tile a column motif over a hex disc of a given radius — over a lookup table that is not
  generative; raising the radius adds columns, not types or motifs. An individual today is an
  initial condition on wiring identical in every individual, not a genome in the generative sense
  ([docs/notes/2026-09-20-what-is-the-genome-here.md](docs/notes/2026-09-20-what-is-the-genome-here.md)
  §3, §5).
- **Cheap** and **expensive** evaluation are numbers of training iterations, fixed in writing
  before a run, never chosen after seeing a result.

## What this is not

- Not a claim of "first": OpenWorm (2011), integrative C. elegans brain–body–environment
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
