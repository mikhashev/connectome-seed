# connectome-seed — a lineage of artificial organisms grown from a real connectome

**What this folder is.** The record of one idea and one day of examining it, saved on Mike's
word (DPC Research group, 2026-09-13 06:22 UTC: «сохрани сюда всё в новую папку»). It is a
**file under a condition, not a project** — that is the verdict of the three agent readers
(Johnny, Ark, CC), and the condition is stated below, precisely enough to be tested.

**Reviewed 2026-09-13** by Johnny ([chat/81](chat/81-johnny-063942.md)) and Ark
([chat/82](chat/82-ark-064101.md)); corrections applied in place on Mike's word
([chat/83](chat/83-mike-064218.md)). Every change carries the reviewer's name where it lands.

**Status:** idea, not started. No code, no runs, no repository. Nothing in here has been
executed except the literature search.

---

## The idea in one paragraph

Instead of emulating a fly and calling it an elephant, take the *heritable grammar* out of a
real connectome (cell types, E/I balance, recurring motifs, sensorimotor loops), let body and
nervous system grow together along a curriculum (fly → beetle → hexapod → quadruped), apply
USPEX-style operators on the living graph (heredity of modules, soft mutation where the
controller is plastic, permutation of roles, a diversity archive), give every offspring a short
"youth" of limited plasticity before measuring it, and select on a multi-objective fitness in
closed arenas. The main artefact is the **evolutionary tree**, not one video. Full text as
posted in the thread: [chat/67](chat/67-mike-055707.md); a clean copy of the five points:
[idea.md](idea.md); in English, [idea_en.md](idea_en.md).

## What the readers found — the shape, not the retelling

Three agent readers, one thread, all in [chat/](chat/). The findings that survived
cross-check:

- **It is not a project yet, and the author says why himself.** The next step the author names
  — *formalising the genome representation* — is not a next task but the condition of the
  project's existence. Johnny, [68](chat/68-johnny-060109.md).
- **Why that representation is a hole and not a detail.** Three requirements pull in three
  directions — *compression* (the genome must be orders of magnitude smaller than the
  phenotype), *composability* (a module cut from one parent must mean the same thing in the
  other), *expressivity* (one grammar must grow a fly and, after mutation, a beetle) — and
  under them sit interfaces, the absence of a cheap validity oracle, and pleiotropy. A
  connectome is the *product* of development; the genome is the *process*; inverting one
  product into a process is underdetermined. Ark, [73](chat/73-ark-061157.md).
- **The USPEX analogy breaks in three load-bearing places** — DFT enthalpy is a physical
  quantity nobody chooses, fitness here is written by the author; DFT relaxation converges to
  something physical, "youth" minimises a training loss; and the paper both critics cite
  measures exactly the failure a *short* youth would produce. Ark, [69](chat/69-ark-060236.md).
- **Two claims in the thread did not survive checking.** The compute estimate ("this is an HPC
  project") was off by two orders of magnitude on its own inputs and counted the wrong cost
  (neuron ODEs instead of body physics and the youth phase); on this card it fits. And the
  paper cited as the counterexample, arXiv 2508.17464, is **two-sided**: its second half shows
  brain–body co-optimisation reaching morphology–controller pairs a fixed body cannot. Only one
  half had entered the thread. CC, [70](chat/70-cc-060556.md).
- **The data are not the blocker.** The male fly CNS (brain + ventral nerve cord, Cell,
  2026-09-03) pairs with FlyWire (female); zebrafish adds structure + activity. Ark, [73].

## The condition, stated so it can be tested

> **Show that a cheap evaluation of an individual is consistent with an expensive one.**

Not "when a genome representation exists" — its absence is the symptom. arXiv 2508.17464
measured the disease on 1,305,840 morphologies: *"it requires more controller optimization to
estimate their fitness well"*, and evolutionary algorithms *"regularly undervalue individuals
with newly mutated bodies and eliminate promising morphologies"*. Their landscape was built with
**300 generations × population 20** per body (§3, Table 1), and their co-optimisation runs go to
**10,000 generations** (§4.1). **Inferred:** that 300 × 20 is "the number a short youth has to
beat" is this team's reading, not the paper's claim — the paper states its budget, not a
threshold. It is still one experiment.

The condition now has a **second, independent ground** (Ark): the PNAS codec below was
demonstrated only where the inner loop is differentiable, and its authors call the
gradient-free path "slow and inefficient" — see [literature.md §F](literature.md). Two papers,
two sides, one sentence: the cheap step in the middle of the loop is the unproven step.

## What already exists — the literature answer

Nobody has solved all three requirements at once. **Each one has a solved instance in a
different field, and two of them are on this very fly.** Verified at source, with numbers, in
[literature.md](literature.md). The short form:

| requirement | solved where | what it gives us |
|---|---|---|
| compression — **the storage half only** (ids → weights) | Shuvaev/Koulakov/Zador, PNAS 2024 — the *genomic bottleneck* is literally a codec: a small network maps (pre, post) neuron identities → connection strength | 322× at 94 % innate accuracy; up to ~3 500×; transfer unchanged at 92× fewer parameters. **Shown with gradients through the genome (Lamarckian, the authors' word); not reproduced in a gradient-free loop.** Decompression is *"analogous"* to development — no growth, no body |
| validity by construction | SELFIES (Krenn 2020, chemistry) — every string is a valid molecule, built for genetic algorithms | validity moves out of the fitness oracle and into the decoder |
| the seed circuit, already built | flyvis (Lappalainen, Nature 2024) — 64 cell types wired from the connectome, unknowns optimised on a task, matches 24 experiments; code public | the T4/T5 falsifier Ark proposed is on GitHub |
| connectome → body | Jin et al., arXiv 2602.17997 — whole fly connectome instantiated as the controller of a biomechanical fly via RL | "fly → body" is a starting point, not a hypothesis |
| modules + bottleneck | arXiv 2606.28380 — hypernetwork generates a modular reservoir, "functional modules upon birth" | requirement 2 **only in first approximation: whether the modules are cuttable and re-attachable between two genomes is not claimed in the abstract** |
| youth as an evolved parameter | arXiv 2604.03386 — 50 000 grown controllers, plasticity parameters in the genome | the "youth" step becomes heritable |
| encodings compared | Miras, Frontiers 2021 — CPPN vs L-systems | no encoding dominates; the three-way pull is real on real robots |

One result cuts *against* the idea: the genomic bottleneck gives innate ability but
*"did not affect the learning trajectory"* — decompression makes the newborn competent, it does
not make its youth cheaper.

## The cheapest next step — proposed, then cut down by review, still Inferred

The first version of this section said: glue the PNAS g-network keyed on **cell types** to
SELFIES-style validity and start from flyvis. Two of its three pieces survived review; the
first did not survive intact, and the way it failed is the useful part:

- **Keying on cell type buys composability with resolution** (Ark). Unique tags cost
  *H log N* bits and give single-neuron specificity; type tags make every neuron of a type
  interchangeable — a type → type block model, which is precisely what the male/female
  connectome comparison was built to see past. The honest label is (type + developmental
  coordinate), and then the grammar must say where the coordinate comes from. The original
  problem is back, one level down.
- **The codec's demonstrated regime is Lamarckian** (Ark, PNAS p. 9). Its 322× came from
  gradients reaching the genome every generation; the idea's loop is gradient-free heredity
  and mutation, and its main artefact — an annotated lineage — cannot exist under a genome
  rewritten from the phenotype. The paper's own counterweight ("net effect similar to
  Darwinian evolution", Baldwin effect) says the *outcome* may transfer; the *mechanism* the
  idea specifies does not, as shown.

What still stands: validity by construction (SELFIES) as the design rule for whatever the
grammar is; flyvis as the circuit to start from; and Ark's one-run test on composition.

**Corrected after the second review (Ark, 07:16 UTC).** An earlier version of this paragraph
said the composition test "doubles as the check on the condition". It does not. There are two
hypotheses and they are registered separately: **(a)** a spliced module behaves predictably;
**(b)** a cheap evaluation agrees with an expensive one. A negative on (a) says nothing about
(b), and the reverse. And a splice of two *identical* copies is a control that can only pass —
if the copies do not interact the composite is trivially "predictable", the same shape as a
zero-initialised adapter — so the test splices two *different* things (two ensemble members, or
two cell types) and names its prediction before it runs. What is spliced, and the numbers
for (b), live in the pre-registration file, not here. Marked **Inferred** — a synthesis, not a
paper, and thinner than it was this morning.

**Project files, added 2026-09-13 on Mike's word:** [VISION.md](VISION.md) (what we are trying
to find out), [ROADMAP.md](ROADMAP.md) (phases, ordered by what blocks them),
[docs/decisions/](docs/decisions/) (ADR-001 publication shape, ADR-002 file under a condition),
[backlog.md](backlog.md) (tasks, validated with the shared backlog tool). Roles as of that day:
CC executes everything, Ark, Johnny and Warren review.

## Files

```
README.md          this
idea.md            the five points, verbatim (Russian, the record)
idea_en.md         English translation of idea.md, 2026-09-13 — not the record
literature.md      every source, what was verified how, numbers and quotes
chat/              the thread, one file per message, 67 → 84, UTC timestamps
                   (79–84 = the review round: Johnny 81, Ark 82, Mike's "доделай" 83)
sources/           shuvaev-2024-genomic-bottleneck-pnas.pdf (open-access, 7.5 MB)
```

**Clocks.** Chat timestamps are UTC; this machine is UTC+07. The thread ran 05:57–06:43 UTC
on 2026-09-13, which is 12:57–13:43 local.

**Not done, deliberately.** No repository initialised, no backlog entry, no card in
`autoresearch-win-rtx/docs/articles/` — those are Mike's calls and none was given.

## Licence

This repository is licensed under the Creative Commons Attribution 4.0 International License
(CC BY 4.0, [LICENSE](LICENSE)); attribution is required as "Mike Shevchenko, DPC Research —
https://github.com/mikhashev/". The PDF in `sources/` carries its own CC BY 4.0 attribution
to its authors (Shuvaev et al., PNAS 2024), stated on its first page.
