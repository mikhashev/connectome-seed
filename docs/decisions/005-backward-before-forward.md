---
adr: 005
title: "Go backward before forward: close the numbers the forward path depends on, starting with the fly"
status: accepted
date: 2026-09-24
deciders: [Mike]
consulted: [Ark, Johnny, Zcode, CC]
informed: []
depends_on: [ADR-004]
related: [ADR-002, ADR-003, ADR-004]
supersedes: []
session: DPC Research group thread, 2026-09-24 17:40–17:53 UTC
axis: honesty
---

## Context and Problem Statement

The project's goal is to make an elephant out of a fly (`idea.md`; ADR-004). By 2026-09-24 the
forward path had reached question (i) on the second brain: a 30-type bank built from FlyWire's right
optic lobe separates from its own shuffles
([outcome note](../notes/2026-09-24-flywire-p3-what-it-showed.md)). The handover named question (ii),
transfer between the two brains, as the next task
([handover §2](../briefs/2026-09-24-next-session-handover.md)).

At 17:40 UTC Mike asked the group a different question (translated from Russian): *what if we move
from what we have not forward but backward: from the fly first, not toward the elephant.* Ark, Johnny,
Zcode and CC discussed it from 17:40 to 17:51 UTC. Mike decided at 17:53 UTC.

What made the question worth asking is what the root of the tree actually is. The **generation-zero
bank** ([GLOSSARY.md:46](../../GLOSSARY.md), [:74](../../GLOSSARY.md)) is the root of the evolutionary
tree. It was not taken from one animal. flyvis built it from two FIB-SEM volumes, FIB-25 and FIB-19,
which are at least two female flies. Each volume's local reconstructions were averaged over columns
into one mean synapse count per type pair and offset. The two volumes' estimates were then fused by
taking **the larger of the two** (Lappalainen et al. 2024, Supplementary Note 1, equation 7)
([where our bank comes from, §1–§2](../notes/2026-09-23-where-our-bank-comes-from.md)). So the root is
a template made by arithmetic. Any agreement between it and another brain is agreement with that
arithmetic as well as with biology.

**Source.** The chat is not in the repository. Every statement below that is attributed to a person
comes from the DPC Research group thread of 2026-09-24, between 17:40 and 17:53 UTC. All times are UTC.

## Decision Drivers

- **The root of the tree is synthetic (Ark).** The generation-zero bank is flyvis's max-merged,
  column-averaged template of at least two flies. It is not an animal.
- **Averaging may manufacture agreement (Ark).** 159 of the 165 FlyWire-30 pairs lie inside
  flyvis-30, a containment of 96.4 %. That is agreement between two averages. How much of it is
  biology and how much is our own arithmetic is unknown. A transfer test run now would inherit that unknown.
- **Question (i)'s rank profiles point the other way.** The two arms' margins run in opposite
  directions across ranks ([outcome note §4](../notes/2026-09-24-flywire-p3-what-it-showed.md)).
  Johnny reads this as evidence against "the same structure".
- **Backward work has a known way of going wrong.** Measuring without a rule is why the measurement
  line was paused ([ADR-004](004-grammar-is-the-main-line.md), amendment of 2026-09-20 10:15 UTC).
  A backward step has to justify itself by the forward number it closes.
- **The tree's edges need knockout and reversal to count as findings.** Lenski et al. 2003
  ([literature.md §28](../../literature.md)) made the drawn line of descent evidence by removing
  elements and undoing steps. The same standard applies to a rule that claims to generate the bank.

## Decision

**Before going forward toward the elephant, go backward toward the fly, but only where doing so closes
a number the forward path depends on.** Mike answered yes to each of three decisions (17:53 UTC):

1. **The column test on FlyWire, plus a reading of whether flyvis exposes the FIB-25 and FIB-19
   estimates separately (before the max merge): YES.**
2. **Question (ii), transfer between the two brains: PAUSED: YES.** It is paused until the column
   test returns, not cancelled.
3. **"Knock out and regrow" is the next registration: YES.**

### Points all four agents agreed

Recorded as agreed, each with who raised it.

1. **Admission rule (Ark).** Backward work is allowed only where it closes a number the forward path
   depends on. Anything else is measurement without a rule, which is why the measurement line was
   paused (ADR-004).
2. **The tree's root is synthetic (Ark).** The generation-zero bank is flyvis's max-merged,
   column-averaged template of at least two flies, not an animal. The next registration says this in
   so many words. The node is **not renamed** until a first result exists (Ark, Johnny, CC).
3. **Averaging may manufacture agreement (Ark).** The 96.4 % containment (159 of 165 FlyWire-30 pairs
   inside flyvis-30) is agreement between two averages. How much is biology and how much is our
   arithmetic is unknown. For that reason question (ii) is paused until the column test.
4. **The column test, named honestly (Ark's proposal; Johnny's objection; Zcode's reconciliation).**
   Per-column type-pair tables within one FlyWire fly give a **lower bound** on how much order our
   processing produces: column averaging is one of four steps (column mean, max merge, pruning below
   one synapse, hand edits), so the test can underestimate the arithmetic's contribution but not
   overestimate it (Zcode). It is **not** a proxy for the overlap between banks, and it is not to
   be reported as one. It is paired with the **separate-volumes reading (Zcode)**: if flyvis exposes
   the FIB-25 and FIB-19 estimates before merging, then overlap(one volume vs FlyWire) against
   overlap(merged vs FlyWire) measures the merge's contribution directly.
5. **When question (ii) returns (all four).** Its registration carries all of the following:
   - **Two arms.** The main arm has the source term fitted without the held-out fold, so it must
     generalise. A secondary "ceiling" arm uses the full source. The difference between the two
     measures the trivial overlap channel (Johnny's power objection, Zcode's arms).
   - **Cell-stratified scoring:** shared cells, target-only cells, source-only cells.
   - **Null 2c as the primary null for "the same":** one consistent type permutation applied to both
     axes of the source factors.
   - **Headline-rank rule r = 2,** stated as "the lowest rank at which both sources were A in (i)",
     with Ark's falsifier. All four ranks are printed.
   - **Question (i)'s opposite rank profiles recorded in advance** as measured evidence against "the
     same structure".
   - **λ chosen only by the source's own cross-validation.**
   - **Existence-only scope,** stated.
   - **The FlyWire typing caveat** travels with it: FlyWire's cell typing may lean on connectivity.
     This is unverified.
6. **Knock out and regrow (CC; second null from Zcode).** Remove a block of the bank, chosen before
   any data is seen and on biological grounds (for example a whole pathway). Train on the rest. Test
   whether the rule regrows the block better than N1 and better than shuffles. **Second null:** regrow
   the block with its pairs permuted. If the permuted block regrows just as well, the rule is
   smoothing, not generating. **Known risk:** indirect leakage through degrees. The registration must
   state exactly what is removed, entirely. **Standard:** the knockout and reversal experiments of
   literature.md §28.
7. **The backward ladder (Zcode, Johnny, Ark).**
   - **Larva** (Winding et al. 2023) comes after the column test.
   - **Fly embryo:** Zcode's search found no public full connectome, so it is recorded as a vision,
     not a step.
   - **C. elegans** (Cook et al. 2019; Witvliet et al. 2021, eight individuals from L1 to adult, not
     averaged) gets a separate ADR when a number demands its first rung.
   - **Johnny's view is recorded:** other species are a new project.
   - None of these three sources is read at source in `literature.md` yet; they are cited as named in
     the chat.

### Rationale

Transfer between two averaged banks cannot be read while the averaging itself may be what agrees.
The column test and the separate-volumes reading are the cheapest way to split "the brains agree" from
"our pipelines agree". Each closes one number that question (ii) depends on, so both pass the
admission rule. "Knock out and regrow" goes forward and backward at once. It asks whether a rule
generates part of the fly it was not shown, which is what a heritable grammar must do. It also meets
the standard the tree artefact will be held to anyway. The ladder beyond the fly is written down so
it is not rediscovered, and it stays closed until a number asks for it. That keeps the backward
direction from turning into the measurement line again.

## Considered Options

- **Go on to question (ii) now** (the handover's plan). Rejected for now: a positive result could be
  produced by the averaging itself, and the registration could not separate the two.
- **Go backward without a rule:** read the larva, C. elegans, the embryo, as far as the data reach.
  Rejected. It is the failure ADR-004 paused.
- **Backward under the admission rule, with (ii) paused and knockout next.** Chosen.

## Amendment — 2026-09-24 18:23–21:00 UTC: decision 1 done; Q1, Q2 and Q3 answered; the knockout bank chosen

Recorded on the owner's word "record the consensus" (Mike, DPC Research group, 2026-09-24 20:59 UTC,
translated from Russian). Everything else in this record stands.

- **Decision 1 is done.**
  - **Part A, the separate-volumes reading (Q2): NO.** flyvis 1.2.0 ships only the merged
    `fib25-fib19_v2.2.json`. The max merge cannot be measured from flyvis (CC, 18:23 UTC;
    confirmed by Zcode, 18:35 UTC).
  - **The column test** was registered (`f568691`, revision 2.2; `b3f41ed`, revision 2.3, with the
    script) after three review rounds by Ark, Johnny and Zcode. It was run once, and the result is
    `9705ef1`, `results/genome/c6/checks/flywire_column_test/RESULT.md`.
  - **Verdict: unclear.** Δ = +0.073 and k* = 9.3 %, between the registered cuts of 5 % and 20 %.
    A single FlyWire column holds a median 0.890 of its type pairs inside flyvis-30, against
    0.964 for the averaged bank, and averaging adds about 7 points.
  - The extra pairs of a single column lie inside flyvis far more often than uniform noise would
    (median X_c 0.54 against 0.094). So real columns resemble neither calibration family.
  - The machine-written numbers were checked against the prose by Zcode (about 620 values, 0
    differences). 34 / 27 / 0.54 were recomputed independently by a CC subagent without the
    test's code.
- **Question (ii) stays paused** until "knock out and regrow" is registered. This was option A of
  two (Mike, 20:13 UTC). When (ii) resumes, the 96.4 % is printed only beside the curve, the
  single-column quantiles and X_c, with a self-consistency baseline (Johnny).
- **Q3, the order:** the column test first, then the knockout registration. This is settled by
  the sequence above.
- **Q1, the block: block A**, `{Mi1, Tm3, Mi4, Mi9, Tm1, Tm2, Tm4, Tm9} × {T4a–d, T5a–d}`, 64
  cells. Chosen by name before any weight was read
  (`docs/notes/2026-09-25-knockout-block-candidates.md`, `10b704e`).
  - The board is the perfect ON×T4 / OFF×T5 checkerboard in FlyWire-30, flyvis-30 and flyvis-65:
    16 + 16 present, no cross cells. This was counted three times, by Ark, Johnny and Zcode.
  - The rule reads no type names (Johnny, Zcode; a name channel proposed by Ark was declined).
- **The bank (Mike, 20:39 UTC): flyvis-65 is the primary bank.**
  - The Janelia male CNS v1.0 (one male, CC-BY) replaces FlyWire-30 as the animal control. Its
    bank needs its own reviewed builder.
  - FlyWire-30 is kept as provenance. On it only 14 of 64 block cells are inferable (Johnny):
    T4d and T5a–d touch nothing outside the block except their self-loops.
  - On flyvis-65 and on the male CNS all 64 cells are inferable. On the male CNS this holds at
    every pair threshold tried (Zcode). Whether the male CNS board is perfect depends on the
    threshold; that threshold is the builder's first open parameter (Zcode, 20:59 UTC).
- **The knockout registration** is drafted, `docs/plans/2026-09-24-knockout-regrow-registration.md`.
  It is in review with Ark, Johnny and Zcode. Running its synthetic worlds before commit (its D11)
  waits for the owner's word.

## Consequences

- **Positive:** the next transfer result, whichever way it falls, can be told apart from an artefact
  of averaging. The next registration tests generation rather than fit.
- **Negative:** question (ii) waits. The handover's §2 is no longer the next task.
- **Neutral:** the generation-zero node keeps its name and its birth ids. Only the description of what
  it is changes, and that change goes into the next registration's text.

## Confirmation

- [x] The column-test registration calls itself a measurement of the order averaging removes, and
      does not call itself a proxy for between-bank overlap (`f568691`, §0).
- [x] The separate-volumes reading states whether flyvis 1.2.0 exposes FIB-25 and FIB-19 estimates
      separately, with the file or code location as evidence either way (NO; column-test
      registration §8, Part A).
- [ ] The knockout registration names the removed block before any data is seen, gives a biological
      reason for it, states everything removed with it, and carries the permuted-block null.
- [ ] The next registration states that the generation-zero bank is a synthetic template of at least
      two flies.
- [ ] When question (ii) is registered, it carries every item of agreed point 5.

## Open Questions

- **Q1:** Which block is knocked out: which pathway, and how is it fixed before data? CC, in the
  registration. **Answered 2026-09-24: block A, by name, before data (Amendment).**
- **Q2:** Does flyvis 1.2.0 ship the per-volume estimates at all, or only the merged json? CC, the
  reading of decision 1. **Answered 2026-09-24: only the merged json (Amendment).**
- **Q3:** Once the column test and the knockout registration exist, what is the order between them?
  Mike. **Answered 2026-09-24: the column test first; it has run (Amendment).**

## Authors

- **Mike:** the question (17:40 UTC); the three decisions (17:53 UTC)
- **Ark:** the admission rule; the synthetic root; averaging may manufacture agreement; the column
  test; cell-stratified scoring
- **Johnny:** the objection that the column test is not a proxy for overlap; the power objection
  behind the two arms; the view that other species are a new project
- **Zcode:** the separate-volumes reading; the two arms; the second null for knockout; the embryo search;
  the λ rule (source cross-validation only); the existence-only scope; the 2c scheme (one consistent
  permutation on both axes); "lower bound"
- **CC:** knock out and regrow; this record; the amendment of 2026-09-24

## References

- [ADR-004](004-grammar-is-the-main-line.md): the grammar as the main line; the measurement line paused
- [GLOSSARY.md](../../GLOSSARY.md) lines 46 and 74: generation-zero bank; generation zero
- [docs/notes/2026-09-23-where-our-bank-comes-from.md](../notes/2026-09-23-where-our-bank-comes-from.md)
  §1–§2: two volumes, column averaging, the max merge
- [docs/notes/2026-09-24-flywire-p3-what-it-showed.md](../notes/2026-09-24-flywire-p3-what-it-showed.md)
  §4: opposite rank profiles; the headline at the crossing point
- [docs/briefs/2026-09-24-next-session-handover.md](../briefs/2026-09-24-next-session-handover.md)
  §2: question (ii) as it stood before this decision
- [literature.md](../../literature.md) §28: Lenski et al. 2003, knockout and reversal
- DPC Research group thread, 2026-09-24 17:40–17:53 UTC (not in the repository)
