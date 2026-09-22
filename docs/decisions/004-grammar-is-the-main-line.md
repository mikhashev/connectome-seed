---
adr: 004
title: "The grammar track is the main line, and measuring the fly is instrumentation for it"
status: accepted
date: 2026-09-20
deciders: [Mike]
consulted: [Ark, CC, Zcode, Johnny]
informed: []
depends_on: [ADR-002]
related: [ADR-002, ADR-003]
supersedes: []
session: DPC Research group thread, 2026-09-17 → 2026-09-20
axis: knowledge
---

## Context and Problem Statement

The project's goal is stated in the group description in the owner's words: **"to learn to
make an elephant out of a fly"**. The long form was written by the owner on 2026-09-12 and is
committed in the repository as `idea.md` (English; the Russian original of 2026-09-12 is in
git history at `2488ecb`, and the English rendering is dated 2026-09-13). It has five points and names its own principal artifact: **not a video of an
elephant, but an evolutionary tree** — which mutation appeared, which module was inherited from
the fly, what grew, where the lineage broke, which skills survived the change of body.

Between 2026-09-17 and 2026-09-20 the work was almost entirely on a different object: nights
1–5, the reachability endpoint, the per-cell-type readout, the instrument's floor, `stop_iter`.
That work was sound and it was necessary — a number that cannot be read is not a number — but
by 2026-09-20 three things had drifted apart:

1. **The three top-level documents no longer describe the project.** `README.md` still says
   "idea, not started. No code, no runs, no repository". `ROADMAP.md` carries the grammar only
   as a sub-branch ("Step 3 — genome", status "Not started") inside the diagnostics section,
   and one of its lines — "Choosing the genome representation … stays off this roadmap" — reads
   as a prohibition on precisely the work now planned. `VISION.md` names the inherited grammar
   but presents cheap-versus-expensive as the project's single principle.
2. **The primary source had stopped being read.** A survey on 2026-09-20 found that no
   participant in the thread had cited `idea.md` at all: the goal had been reconstructed from
   paraphrases by two agents, and in that reconstruction it had narrowed to the first of its
   five points. The owner's own text, dated and committed, was passed over in favour of a
   summary of it.
3. **The measurement line's purpose had been lost.** No document answered why the fly must be
   measured at all — and the answer was already in the repository: point 4 of `idea.md`
   ("local relaxation = the descendant's life") *is* the cheap/expensive pair, and the closing
   annotation of `idea.md` records that the literature has measured that very mechanism as a source of
   mis-ranking.

## Decision Drivers

- **The grammar needs no GPU and is not blocked by the nights.** `ROADMAP.md` says so in as
  many words; it has been true since 2026-09-16 and has been rediscovered as a fresh idea more
  than once.
- **The repository is the source of truth for its own goal.** A goal held in a chat paraphrase
  cannot be audited, dated, or checked for drift — and the drift above happened while the
  primary source sat in the repository root.
- **A restated goal must fit on one page and be quotable.** If it does not, the next session
  reconstructs it again, from whoever happens to be talking.
- **The two lines are not independent.** The measurement line does not merely accompany the
  grammar: what the grammar must produce is constrained by what an instrument can distinguish.
  Measuring the fly is how one learns what an elephant has to be.

## Decision

**The goal of this project is the five points of `idea.md`, and its artifact is the
evolutionary tree. The grammar track (Path I) is the main line. Measuring the fly is
instrumentation for it — not a gate on designing the grammar, and not a distraction from it.**

Concretely:

1. **The grammar track starts now**, in parallel with the measurement line, and is not blocked
   by the number the nights are accruing. Growing anything remains blocked until Phase 2 has a
   number — *designing* is not growing, and the prohibition is narrowed to the former.
2. **The goal is quoted from `idea.md`, never restated from chat.** Every document that states
   it carries all five points — the inherited grammar; the body-and-brain curriculum (fly →
   beetle → six-legged truck → small quadruped → heavy quadruped); the USPEX operators on a
   living graph; the descendant's "youth" before measurement; the multi-objective fitness with
   a closed arena set — and the artifact: a tree, not a video.
3. **The grammar is named as the first step, not the whole goal.** The owner's own words: it is
   the next step he named, and "almost everything else depends on it" — which is not the same
   as saying the goal is the grammar.
4. **The status of the measurement line is: parallel, with the grammar as the main line.**
   *(No source settled this sentence until the owner did: Mike, 2026-09-20 09:27 UTC — see Open Questions, Q1.)*
5. **Project state lives in one place — `ROADMAP.md`.** The plan stays the home of design; the
   handover brief stays the home of the reading list. A status repeated in three documents
   diverges in three ways.

### Rationale

The alternative — letting the documents keep describing a version of the project that no longer
exists — is not neutral. `README.md` currently asserts that there is no code and no runs, in a
repository with five nights of runs and a committed note on the genome; that is not a stale
sentence, it is a false one, and the first outsider to read it is misled. The second
alternative — keeping the goal in the thread and in review messages — is what produced the
narrowing to point 1 and the loss of point 4: a paraphrase of a paraphrase is not a
specification.

## Amendment — 2026-09-20 10:15 UTC: the measurement line is paused

Decision point 4 above said *parallel*. Later the same morning the owner narrowed it: "Pause the fly → grammar (point 1)" (Mike, owner, DPC Research group, 2026-09-20 10:15 UTC, translated from Russian). The measurement line — nights, held-out loss, the ADR-002 condition, the perturbation ladder — is **paused, not cancelled**: no new night is run and no reading of it is extended until the owner resumes it. Work goes to point 1 of `idea.md`, the representation of the genome. The instruments and records of the measurement line stay as they are; its open board entries stay open and are marked as paused, not closed. Everything else in this record stands.

## Consequences

- **Positive:** the road to the goal stops depending on any agent's memory of the chat; a
  newcomer can read the goal, its source, its date and its author in-tree; the measurement line
  acquires a stated purpose instead of an implicit one.
- **Negative:** three documents must be edited together, and an edited line shifts every
  line-number reference below it. `graph.json` and `atlas.html` are derived from these files
  and must be rebuilt alongside the commit (they are ignored by git); the quarantine scan must be re-run, because one of
  the three files is not currently on the exclusion list.
- **Neutral:** the blind registration (Path II) is deferred, not cancelled; this ADR does not
  change its scope.

## Confirmation

- [ ] `README.md`, `VISION.md`, `ROADMAP.md` each state the goal with all five points and cite
      `idea.md` with author and date.
- [ ] The goal statement in the repository and `idea.md` agree sentence by sentence; no claim
      about the goal is traceable only to the chat.
- [ ] `ROADMAP.md` has a section for the grammar track with named owners, outside the
      diagnostics section.
- [ ] The line that reads as a prohibition distinguishes *growing* from *designing* in as many
      words.
- [ ] No line-number reference below the edited region is stale; `graph.json` no longer carries
      a pre-edit position for the generated block.
- [ ] `contamination_scan.py --required` passes; `README.md` is not newly excluded.

## Scope

- `README.md` — status line; a section "The goal, in the owner's own words"
- `VISION.md` — the goal paragraph; which line is primary as of 2026-09-19
- `ROADMAP.md` — the grammar track moved out of the diagnostics section; the prohibition line
  narrowed
- `graph.json`, `graph.html`, `atlas.html` — regenerated at the same time; all three are ignored by git, so they never appear in the commit
- `docs/briefs/2026-09-19-genome-track-handover.md` — unchanged (its reading list is not state)

## Open Questions

- **Q1 — ANSWERED (Mike, 2026-09-20 09:27 UTC: "yes", translated from Russian).** Does the owner confirm the reading —
  grammar as the main line, the measurement line parallel to it? No source settles this; every
  document that encodes the reading is citing an agent, not the owner. — Mike
- **Q2:** What exactly is "the elephant" beyond the grammar? The five-point reading is
  unopposed and unconfirmed; alternative readings have never been put in writing. — Mike
- **Q3:** The grammar track's three pieces — the design around S2 with label provenance, the
  note on what a genome is here, the C6 control specification — are **all three assigned**
  (`ROADMAP.md`, `docs/briefs/2026-09-19-genome-track-handover.md`). **One is delivered** (CC's
  note, committed in `effaff2`); **two are unwritten**: this design (Ark) and the C6
  specification (Zcode). — Ark

## Authors

- **Mike** — Decision; the goal text (`idea.md`, 2026-09-12)
- **Ark** — Draft; the finding that the goal's primary source had never been cited, and that
  the goal had narrowed to point 1 of 5 in every paraphrase of it
- **CC** — The survey of the three documents against the goal, and the patch
- **Zcode, Johnny** — Review

## References

- `docs/decisions/001-publication-shape.md` — the convention this ADR follows (quote carries
  its source; plain attribution into chat)
- `docs/decisions/003-blind-authorship-after-the-numbers.md` — the deferred registration
- `idea.md` (2026-09-12; English translation of 2026-09-13; the Russian original is in git
  history at `2488ecb`) — the primary source
- `docs/notes/2026-09-20-what-is-the-genome-here.md` — what the substrate supplies today
