# connectome-seed — a lineage of artificial organisms grown from a real connectome

**What this folder is.** The record of one idea and one day of examining it, saved on Mike's
word (DPC Research group, 2026-09-13 06:22 UTC: "save everything here, in a new folder" —
translated from Russian). It is a
**file under a condition, not a project** — that is the verdict of the three agent readers
(Johnny, Ark, CC), and the condition is stated below, precisely enough to be tested.

**Reviewed 2026-09-13** by Johnny ([chat/81](chat/81-johnny-063942.md)) and Ark
([chat/82](chat/82-ark-064101.md)); corrections applied in place on Mike's word
([chat/83](chat/83-mike-064218.md)). Every change carries the reviewer's name where it lands.

**Status:** the idea of 2026-09-13 as it was first written; this file has not been rewritten
since. What happened after it is not here — the pre-registration, the runs and their records
live in `docs/` and `results/`, and the current state of the condition is in
[ADR-002](docs/decisions/002-file-under-condition.md) § "Status of the condition". Which part of
the idea is being worked on now is stated in "The goal, in the owner's own words" below.

## State at 2026-09-20

*Dated block, kept short on purpose. The full account is in the two files it links; the only
status that is not typed by hand is the generated block at the bottom of
[ROADMAP.md](ROADMAP.md). No result value appears here — where a finding is numerical, the file
that carries the number is named.*

- **Goal and documents.** The goal is the five points of [idea.md](idea.md) plus the evolutionary
  tree, quoted by point number and no longer rebuilt from chat. The grammar track is the main
  line; measuring the fly is its instrument and is **paused, not cancelled** —
  [ADR-004](docs/decisions/004-grammar-is-the-main-line.md), accepted on the owner's word of
  2026-09-20, amended the same day at 10:15 UTC on the owner's word: "Pause the fly → grammar
  (point 1)".
- **The measurement track.** Ten runs on disk — six individuals, two of them run three times.
  Nothing beyond that is a test. This session established that evaluation non-repeatability is
  GPU operation order rather than the recording hook, that the same mechanism inside training is
  where the whole replicate gap is made, and that an individual shows in the rank *shape* of its
  65-type cell profile rather than in its magnitude or in held-out loss (declared and reported
  MIXED, with a reviewer's narrowing recorded beside it). Numbers live in
  `results/night5/diagnostics/rowB/`.
- **`activity_penalty.stop_iter` is left untouched** (owner's decision, 2026-09-20): the
  penalised quantity is smooth across its own 150,000 boundary in all ten runs and held-out loss
  shows no step there. The observation that survives is narrower — the cheap probe at 25,000 sits
  in an unsettled phase.
- **Night 6 is prepared and was not launched**
  ([brief](docs/briefs/2026-09-20-night6-deterministic-pairs.md)); a perturbation ladder is
  proposed in its place and is **not authorised**.
- **The grammar track** has its note delivered, its design placed with an amendment owed by its
  author, its label check done, and `literature.md` §I (digital evolution with inheritance, 24
  entries read at source) added. The extraction of the rule bank waits only on that amendment;
  the C6 control specification is not started and is blocked by nothing.
- **Session close:**
  [docs/retrospectives/2026-09-20-session-close.md](docs/retrospectives/2026-09-20-session-close.md)
  — what was done, decided, and by whom; what was not done; and the errors, including this
  session's own: the goal was first reconstructed from chat paraphrases and narrowed to point 1
  while `idea.md` sat in this directory.
- **Next session:**
  [docs/briefs/2026-09-20-next-session-handover.md](docs/briefs/2026-09-20-next-session-handover.md)
  — the state in one page, owners, what is blocked on what, the open decisions, and the reading
  order. Whoever starts must say which of the two jobs they are before reading anything.

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

## The goal, in the owner's own words

The goal is not a paraphrase and does not have to be reconstructed from discussion: it is in this
repository, verbatim and dated, as [idea.md](idea.md) (the record, Russian) and
[idea_en.md](idea_en.md) (translation). Mike Shevchenko, author, 2026-09-12 12:18. Restated by him
in one line as the project's description on 2026-09-19: **"to learn to make an elephant out of a
fly"** (translated from Russian). The two say the same thing: the idea opens with **"Not
'emulate a fly and call it an elephant', but grow a lineage of creatures from a real
connectome-seed"**, and the restatement promotes that distinction from a disclaimer to the goal.

It is five points, an artefact, and a named first step. All five are the goal; none of them is a
later addition.

1. **The seed is a heritable grammar, not all the weights** — neuron types, E/I balance, recurring
   graph motifs, sensory and motor circuits. "This is the first genome, not a cemented brain."
2. **Body and brain grow together** — the genome says which segments, joints and sensors the body
   has and how neuromodules are duplicated, connected and specialised. **Not a "fly → elephant"
   jump, but a curriculum:** fly → beetle → six-legged truck → small quadruped → heavy quadruped.
3. **USPEX operations, on a living graph** — heredity of working brain and body modules from two
   ancestors; softmutation where the controller is plastic rather than random axon-cutting;
   permutation of a module's role, type or sensory channel; random embryos and a diversity archive.
4. **A short "youth" before fitness is measured** — limited plasticity in several safe worlds, and
   only then the measurement: "we evaluate not the raw embryo, but what it stably settles into."
5. **Multi-objective fitness on a held-out set of arenas** — energy, stability, speed, recovery
   after a broken sensor or joint, novelty, transfer to unseen terrain; the arenas are held out
   "otherwise the winner is whoever found a hole in MuJoCo".

**The main artefact is not a single elephant video, but an evolutionary tree:** which mutation
appeared, which module was inherited from the fly, what grew, where a line broke, and which skills
survived the change of body.

**The first step is the author's own, and it is the one open now.** From the same message: *"the
most interesting next step, in my view, is formalising the representation of the genome (exactly
how the heritable grammar of modules and growth rules is written down). Almost everything else
depends on it."* That is point 1, and it is the track being worked on — see
[ROADMAP.md](ROADMAP.md) § "The grammar track". It is the first point, not the whole goal: points 2,
3 and 5 are designed for and not run, and nothing is grown until the condition below has a number.

**What the elephant means, operationally.** An elephant is not a bigger fly: more cells of the same
types is a lattice parameter, it does not add types, motifs or knobs, and the wiring is given to us
rather than produced. An elephant is a rule that *generates* the wiring — more cell types and
specific connections between them. Measured against that test, what we run on today holds a single
production over a lookup table that is not generative, and an individual is an initial condition on
wiring identical in every individual — not a genome in the generative sense
([docs/notes/2026-09-20-what-is-the-genome-here.md](docs/notes/2026-09-20-what-is-the-genome-here.md)).

**Why the measurement line below is not a detour.** Point 4 *is* the cheap-and-expensive pair: the
short youth is the cheap evaluation, the fitness measured after it is the expensive one. The idea's
own annotation says so — the short "youth" of point 4 is exactly the mechanism arXiv 2508.17464
measured as the source of mis-ranking. And the main artefact is a tree, so a selection instrument
that cannot tell one individual from another would grow a tree of noise. The grammar is the main
line, and measuring the fly is its instrument — confirmed by Mike, owner, 2026-09-20 09:27 UTC.
Later the same day the owner paused the measurement line (10:15 UTC: "Pause the fly → grammar
(point 1)"): no new night runs and no reading of it extends until it is resumed; the instruments
and records stand as they are. See
[ADR-004](docs/decisions/004-grammar-is-the-main-line.md).

**Two annotations the idea carries about itself**, recorded on 2026-09-13 and repeated here so this
section cannot be read without them: **"first" is not true** — OpenWorm since 2014, C. elegans
whole-body simulators, whole-fly-brain emulation on Loihi 2, and a connectome-as-controller fly in
2026 ([literature.md](literature.md)); and the point-4 note above. Neither kills the idea; both
change where it starts.

Owners of the open track: Ark — the design around S2 with label provenance; CC — the note "what is
the genome here" (delivered) and the extraction; Zcode — the C6 control specification
([docs/briefs/2026-09-19-genome-track-handover.md](docs/briefs/2026-09-19-genome-track-handover.md)).
The track needs no GPU and is not blocked by the nightly accrual.

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
CC executes everything, Ark, Johnny and Warren review. **Experiment record, added 2026-09-14:**
[docs/experiments/001-run0-and-replicate.md](docs/experiments/001-run0-and-replicate.md) (run 0
and its replicate, against the pre-registration); next session:
[docs/next-session-plan.md](docs/next-session-plan.md).

Start here for the rules this repository learned the hard way:
[docs/CHECKLIST-research-repo.md](docs/CHECKLIST-research-repo.md).

## Files

```
README.md          this
idea.md            the five points, verbatim (Russian, the record)
idea_en.md         English translation of idea.md, 2026-09-13 — not the record
literature.md      every source, what was verified how, numbers and quotes
chat/              the thread, one file per message, 67 → 84, UTC timestamps
                   (79–84 = the review round: Johnny 81, Ark 82, Mike's "finish it" 83,
                   translated from Russian)
sources/           shuvaev-2024-genomic-bottleneck-pnas.pdf (open-access, 7.5 MB)
```

**Clocks.** Chat timestamps are UTC; this machine is UTC+07. The thread ran 05:57–06:43 UTC
on 2026-09-13, which is 12:57–13:43 local.

**Not done, deliberately — as of 2026-09-13.** No repository initialised, no backlog entry, no
card in `autoresearch-win-rtx/docs/articles/` — those were Mike's calls and none had been given
that day. A repository and a board exist since; this paragraph is kept as the record of the day,
not as a statement about now.

## Licence

This repository is licensed under the Creative Commons Attribution 4.0 International License
(CC BY 4.0, [LICENSE](LICENSE)); attribution is required as "Mike Shevchenko, DPC Research —
https://github.com/mikhashev/". The PDF in `sources/` carries its own CC BY 4.0 attribution
to its authors (Shuvaev et al., PNAS 2024), stated on its first page.
