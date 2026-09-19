---
adr: 003
title: "A criterion written after its numbers are visible must be authored by someone who has not seen them"
status: accepted
date: 2026-09-19
deciders: [Mike]
consulted: [Ark, Zcode, CC]
informed: []
depends_on: [ADR-002]
related: [ADR-002]
supersedes: []
session: DPC Research group thread, 2026-09-18 → 2026-09-19
axis: honesty
---

## Context and Problem Statement

A pre-registered test was executed once on 2026-09-18 and returned `TEST UNREADABLE`: its own
resolution floor removed 16 of 23 grid levels, every one on the twin side. Within an hour the
reason was clear and, on the face of it, structural — the floor had been placed on the twin
gap, one of the two quantities being compared, rather than on the **margin** between them.
Closeness of the twins raises resolution; the rule read it as absence of information and
discarded exactly the levels where the signal was strongest.

The dimensional argument for the repair does not depend on any observed value, and its
direction is **against** the project's interest: with the floor on the margin, the verdict
becomes FAIL rather than the ACCEPT everyone wanted. Both facts were offered, sincerely, as
grounds for re-reading the same substrate with the corrected rule.

They are not sufficient, and the reason is the problem this ADR settles. The argument is
structural but the *finding* came from the data: sixteen levels left on the twin side, seen
first and reasoned about afterwards. The order of events cannot be repaired by the quality of
the reasoning. And the second repair — how far to offset the lower anchor — has no
argument-from-dimensions at all: any offset is chosen knowing which levels it removes.

## Decision Drivers

- **A rule chosen after the numbers are visible is fitted to them**, whatever the author
  intends, and the author is the last person able to judge whether it is.
- **The usual remedy is a disinterested signatory, and there was none.** All three reviewers
  had read the committed JSON. It is in the repository, so anyone who takes the question up
  inherits the same contamination by reading the history.
- **"The correction hurts us" is evidence of good faith, not of validity.** It was raised and
  is recorded; it does not change what was seen before what.
- **The cost of the honest path turned out to be zero.** The corrected rule needs a substrate
  that does not exist yet; the next night produces one. Nothing is delayed by refusing to
  re-read.

## Decision

**A criterion, threshold or resolution floor devised after its own numbers have been seen may
not be authored, and may not be signed off, by anyone who has seen them. It must be written on
a substrate that does not yet exist, by an author excluded from the contaminated material by
name, and reviewed by the others for internal consistency only — never for whether a threshold
is "reasonable".**

Concretely, for the reachability endpoint:

- **v1 is closed as unreadable and will not be re-read.** The verdict stands as the instrument
  reported it.
- **v2 is written before the data it will judge exists.** Contamination requires both a rule
  and its data; fixing the rule while the data is absent is clean by construction, and
  strictly cleaner than fixing it before merely *reading* existing data.
- **The author of v2 is a session that has not read** `results/diagnostics/reachability/`, the
  group thread from 2026-09-18 onward, or §2–3 of experiment 005. The exclusion list is
  written down, not remembered.
- **Those who have seen the numbers may review logic and may not review thresholds.** Whether
  a verdict follows from its premises is checkable by anyone; whether a bar is set at the
  right place is a judgement that silently consults what one has seen.
- **The fewer free constants a rule has, the smaller this problem is.** Where a number is
  needed it is *derived* — a multiple of the checkpoint step, a count of degrees of freedom —
  not chosen. A rule with no adjustable constants cannot be tuned, and then the question of
  who wrote it loses half its force.

## Considered Options

- **Re-read the same substrate with the corrected floor.** Rejected: the correction was found
  in the data, and a second repair (the anchor offset) has no data-free justification at all.
- **Have a contaminated author write v2 and disclose the contamination.** Rejected: disclosure
  records the problem without removing it, and the reviewers able to catch a fitted threshold
  are the same people who saw the numbers.
- **Wait for an outside executor.** Rejected as unnecessary — a fresh session with a written
  exclusion list is available immediately and costs nothing.
- **Blind author on a substrate that does not yet exist.** Chosen.

## Consequences

- The next session splits in two, and they may not be the same session: one may read
  everything (the genome track); one may not (the v2 author). Whoever starts says which they
  are before reading anything.
- Handover briefs must carry an explicit *do-not-read* list, not a general instruction to be
  careful. `docs/briefs/2026-09-19-genome-track-handover.md` carries the first one.
- The cost of this discipline is an artefact that cannot be improved in place. That is the
  intended cost: a one-shot reading that can be re-run under a better rule is not a one-shot
  reading.
- It applies to any future instrument, not only to this endpoint — including the tuning
  battery and any genome-side readout.

## Confirmation

- [ ] v2 exists, and its own header names the session that wrote it and states that the
      session had not read the excluded material.
- [ ] The excluded material is listed by path in the handover, not described in prose.
- [ ] v2 contains no constant chosen by hand: every number in it is derived from a rule stated
      before the data exists.
- [ ] The review of v2 by anyone who saw v1's numbers is recorded as a logic review, and says
      so.

## Open Questions

- **Q1:** Whether a reviewer who has seen the numbers can usefully check a *derived* constant's
  derivation without checking the constant. Provisionally yes — the derivation is an argument,
  not a value — but it has not been tested.
- **Q2:** How this interacts with the repository's own history. The contaminated numbers are
  committed, so every future author inherits the exclusion list rather than a clean slate. No
  mechanism enforces it beyond the handover saying so.

## Authors

- **Ark** — the finding that the floor sat on the wrong quantity, and the first statement that
  the same substrate may not be re-read
- **Zcode** — the argument that a rule fixed before the data exists is stronger than one fixed
  before the data is read, and the proposal of a brief with no numbers in it
- **CC** — the self-exclusion from authorship of v2, the exclusion list by path, and this
  record
- **Mike** — the decision

## References

- `docs/preregistration-reachability-endpoint.md` (v7) — the registration that produced the
  unreadable verdict, including its §11 rules on what voids a reading
- `results/diagnostics/reachability/` — the one reading, stdout verbatim and JSON
- `docs/experiments/005-night5-third-runs-of-seed-0-and-seed-3.md` §2–3 — excluded material
- `docs/briefs/2026-09-19-genome-track-handover.md` §6 — the first exclusion list in use
