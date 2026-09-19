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

A pre-registered test was executed once on 2026-09-18 and the instrument reported that it
could not read: its own resolution floor removed most of the grid, and every dropped level
went on the twin side. *(The verdict string and the counts are deliberately not repeated here.
This document is required reading for the very author who must not see them — see the
sanitisation note at the end of Consequences.)* Within an hour the
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
- **The protection is the exclusion list, not the absence of the data.** This decision was
  argued while night 5 had not run, on the ground that contamination needs both a rule and its
  data, so fixing the rule while the data is absent is clean by construction. **That ground
  expired before this ADR was written** (amended 2026-09-19, Zcode): night 5 finished at
  04:59:37Z and its ten curves — the substrate v2 will read — have been on disk since. The
  argument remains true of *this* v2 only in the weaker form that the rule is fixed before the
  data is read. So the working protection is now the list below, and it must cover the
  substrate itself.
- **Blindness is required to the VALUES, not to the rule** (Ark and Zcode, 2026-09-19; this
  is the load-bearing clause and the earlier wording was wider than its mechanism). The
  repairs the v1 reading exposed — that a resolution floor belongs to the *difference* being
  compared and not to one of its terms, that a lower anchor needs an offset — are supplied to
  the author **as requirements**, because the first is derivable from dimensions and the
  second is not derivable at all. What then protects against fitting is not ignorance of the
  problem but that **no constant is free**: where a number is needed it is derived, and a rule
  with nothing adjustable cannot be tuned toward an answer. The empirical support is this
  project's own history — v1 carried exactly three hand-set constants marked "registered
  choice — fix in review", and the entire authorship dispute was about them; once v2 made the
  anchors computed, the question of who wrote the rule lost most of its force.
- **The exclusion list is GENERATED, not maintained.** `docs/blind-author-exclusions.txt`,
  produced by `tools/contamination_scan.py` against a values file kept **outside** this
  repository, so the literals never enter it and only paths — which are not values — come back
  in. **The first version of this list was written by hand and named five paths; the scan
  found 52 of 288 tracked files**, including `VISION.md`, `ROADMAP.md`, ADR-002, the v1
  registration (which is a data sheet for eight of the ten curves: it carries every curve
  minimum and every iteration-12 value by name), §4 of experiment 005, and **this ADR itself**.
  A list wrong by 47 entries on its first day is a recollection, not a list — and none of the
  three people able to check it would have noticed by reading, because all three had already
  seen the numbers. Regenerate it before any blind session begins.
- **Whole directories are excluded regardless of the scan**, because they *are* the values or
  are untracked: `results/diagnostics/reachability/`, `results/night5/`,
  `tools/night/night5_*`, the repository history for 2026-09-18 and 2026-09-19 (`git log` and
  `git show` — the commit messages carry the verdict and the ratios in plain text), and the
  DPC Research group thread from 2026-09-18 onward.
- **What the author may have, and needs:** the substrate's *structural* shape — 72 checkpoints
  by 10 runs, the iteration grid, which run is which individual and which boot session —
  supplied by the handover as a description, never by opening the file. The same line §11 of
  the v1 registration drew between structure and values.
- **This Decision section is the authoritative copy of the rule; the handover is the working
  copy for a session, and `docs/blind-author-exclusions.txt` is the authoritative list of
  paths.** Named because three places referred to the list differently and a later edit would
  otherwise diverge (Ark, 2026-09-19).
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
- **Blind author, with the contaminated material excluded by path.** Chosen. It was argued as
  "on a substrate that does not yet exist"; by the time the decision was written the substrate
  did exist, which moves the whole weight of the option onto the exclusion list and is why
  that list is exhaustive above rather than illustrative.

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
- [ ] The excluded material is listed by path in `docs/blind-author-exclusions.txt`,
      **regenerated by `tools/contamination_scan.py` immediately before the blind session
      starts**, not described in prose and not carried forward from a previous run. (This box
      previously said "in the handover", while the rule lives in Decision and the list in the
      generated file — three places, no named authority. Corrected 2026-09-19 on Ark's point.)
- [ ] v2 contains no constant chosen by hand: every number in it is derived from a rule stated
      before the data exists.
- [ ] The review of v2 by anyone who saw v1's numbers is recorded as a logic review, and says
      so.

## Open Questions

- **Q1:** Whether a reviewer who has seen the numbers can usefully check a *derived* constant's
  derivation without checking the constant. Provisionally yes — the derivation is an argument,
  not a value — but it has not been tested.
- **Q2 — partly answered 2026-09-19, and the answer is uncomfortable.** The contaminated
  numbers are **committed**, in the files and in the commit messages themselves, so `git log`
  alone leaks the verdict, the ratio and the SDs. The history is therefore on the exclusion
  list above. What remains open is that **nothing enforces any of it**: the list is a sentence
  in a brief, and every future author inherits the contamination rather than a clean slate.
  The only structural answers are an author outside this repository or a substrate this
  repository has never recorded — neither of which is available today, and both of which cost
  more than the discipline does.

## Authors

- **Ark** — the finding that the floor sat on the wrong quantity, and the first statement that
  the same substrate may not be re-read
- **Zcode** — the argument that a rule fixed before the data exists is stronger than one fixed
  before the data is read, and the proposal of a brief with no numbers in it
- **CC** — the self-exclusion from authorship of v2, the exclusion list by path, and this
  record
- **Mike** — the decision

## References

> **For the blind author: read §Decision and §Consequences of this file and nothing else in
> it.** The references below are the provenance of the decision, and several of them are
> addresses of the very material the decision excludes — a pointer is not a value, but a
> pointer in the document you are required to read is an invitation rather than a risk (Ark,
> 2026-09-19). The Context section above is worse: it states both the diagnosis and the
> repair, which is deliberate — you are meant to receive the repairs as requirements — but it
> also quotes the shape of the result, so it is not neutral reading either.

- `docs/preregistration-reachability-endpoint.md` (v7) — the registration that produced the
  unreadable verdict, including its §11 rules on what voids a reading
- `results/diagnostics/reachability/` — the one reading, stdout verbatim and JSON
- `docs/experiments/005-night5-third-runs-of-seed-0-and-seed-3.md` §2–3 — excluded material
- `docs/briefs/2026-09-19-genome-track-handover.md` §6 — the first exclusion list in use
