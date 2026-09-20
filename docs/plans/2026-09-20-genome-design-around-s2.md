# Design around S2 — what the genome track predicts, and which labels may judge it

**Author:** Ark (agent_001), 2026-09-20
**Status:** design. Nothing here has been run. Repo is read-only to me — CC places this file.
**For:** `connectome-seed`, card `THE-GENOME-DESIGN-AROUND-S2-NEEDS-LABEL-PROVENANCE-BEFORE-EXTRACTION`
(HIGH, open, 2026-09-16), `docs/plans/2026-09-16-functional-readout-plan.md` step 3.
**Suggested path:** `docs/plans/2026-09-20-genome-design-around-s2.md`.

**What this document is.** The extraction CC is waiting on has two halves — the **rule bank**
and the **label array**. The bank is a table and its boundary is already written down. The
label array is a judgement call: some of its columns may not be labels at all. This document
handed the field list with a provenance class per field, and specifies the one check that has
to run before any of those fields is used as an external yardstick.

**What it is not.** It is not the design of a generative rule for cell types — that is the
elephant, it is a larger piece, and it is not licensed by anything below. It is the readout
design around S2.

---

## Sources

| # | Source | How far I read it |
|---|---|---|
| A | `docs/briefs/2026-09-16-step2-tuning-battery.md` §8 | lines 89–103, read directly |
| B | `docs/plans/2026-09-16-functional-readout-plan.md` step 3 and its boundary block | lines 78–104, read directly |
| C | `backlog.md` card `THE-GENOME-DESIGN-AROUND-S2-…` | lines 205–213, read directly |
| D | `research/analysis-cheap-step.md` §Sources and §1 | lines 1–60 and §Sources, read directly |
| E | `docs/notes/2026-09-20-what-is-the-genome-here.md` | **not read by me** — quoted from `ROADMAP.md` and CC's report |
| F | flyvis `groundtruth_utils.py` | **not opened by me** — everything about its fields is quoted from A §8 |

E and F are named because they are the two places below where I am relaying rather than
verifying. F matters most: the whole field inventory in §3 is A's, and A's inventory is a
survey, not a source reading. §6 makes closing that gap the first step.

---

## 1. What S2 is, and what is borrowed from it

**S2** = Shuvaev, Lachi, Koulakov, Zador, *Encoding innate ability through a genomic
bottleneck*, PNAS 2024. Local copy `pnas_genomic_bottleneck_full.md`; my reading of it is in
`research/analysis-cheap-step.md`.

**The shape that is borrowed.** An inherited object — their word is *genome* — is much smaller
than the network it produces, and the evolutionary loop edits **the inherited object**, not the
network. The network is a readout. That is exactly the shape our track is missing: today the
substrate is a compiled table (2,355 bank rows) plus **one** generative rule (replicate the
column motif over a hex disk of radius *n*; identical at extent 5 and 15). Everything else — 65
type names, which pairs connect, the offsets, the counts, the signs — is a lookup, not a rule.

**What is not borrowed.**

- **Their decoder.** Their genome maps to a weight matrix through a fixed random projection.
  We have no reason to copy that, and the choice is downstream of this document.
- **Their loop is Lamarckian, in their own words** (local copy lines 851–856: the trained weight
  matrix modifies the genome in the next generation — *"biologically unrealistic"*). Their
  cheap step is therefore **paid for with a gradient**. Ours is not, and this asymmetry is not
  decoration: it is the difference between a cheap step that is cheap and one that is merely
  smaller.
- **Their claim of innate ability.** It rests on benchmarks we do not share.

**Why S2 is the right anchor anyway.** Because it is the literature instance of the exact
question this track asks — *can the inherited object, rather than the compiled network, carry
the structure?* — and because the same paper is the one that taught us, separately, that the
cheap step in the middle of a loop is where the unproven bet sits.

---

## 2. What the track predicts, from what

**One sentence: the compiled rule bank is predicted from the compiled rule bank.**

This sounds circular, and it is meant to. The claim under test is **not** "we predict biology".
It is the narrow, checkable one: **a rule small enough to be called a genome regenerates the
bank, and the regeneration is not a copy of the table.** If that cannot be shown, nothing
larger should be built on it.

**What the object is, exactly** (from B's boundary block, quoted, not re-measured by me):

- the compiled bank is the h5 edge table — 2,355 rows of
  `(source_type, target_type, du, dv) → n_syn, sign`, identical at extent 5 and 15;
- the source json carries 605 `(src, tar)` entries with 2,140 offset rows; **2,117** of those
  keys match the bank one-to-one; **238** bank rows are added by the convex-hull fill
  (`n_syn_fill = 1`); **23** json rows have no bank counterpart (self-projections of the
  `stride [3, 2]` types, dropped by the `KeyError` suppression at `connectome.py:497-498`);
- on the 2,117 matched keys the bank is an **identity copy of the json up to a float32 cast**
  (max |Δn_syn| = 6.5e-6);
- the pair count is **605 in the json and 604 instantiated** — `Lawf1 → Lawf1` never lands on a
  Lawf1 cell under that type's `stride [3, 2]` (mechanism inferred from the layout pattern,
  not executed).

**What this licenses, in B's own words:** a success of S2 licenses *"predict the bank from the
bank"* plus this documented transition — **not more**. The transition json → bank is
deterministic and value-preserving apart from the hull fill and the stride-dropping, and it is
**not exercised by C6/S2 themselves**. A design that quietly used the transition as its target
would be testing the one step nobody has licensed.

---

## 3. The label array — field list for extraction

**Shape:** one row per cell type, 65 rows, on the **same type axis as row A and row B** (taken
from `net.connectome.nodes.type[:]`, the same function the ablation uses). An axis taken from a
different source makes "does the label array agree with the readout" unanswerable by
construction.

**Instrument note before the inventory.** A §8 makes a **negative** claim — *"no source stated
at all for"* twelve fields. A negative claim needs its instrument named as much as a positive
one: which patterns were searched for (`Fig`, `et al`, `from`, a citation-shaped comment), in
what forms. Until that is stated, "no source stated" is a survey result, not a finding.

**Four provenance classes.** The disposition differs per class, and the class travels **with
each column** into the extracted file.

### Class A — sourced

| field | source, as quoted in A §8 |
|---|---|
| `L5` (`:29`) | `# Drews 2020, Matulis 2020` |
| `tuning_curves`, incl. T4a–d / T5a–d (`:514`) | `# from Maisak et al. 2013 Fig. 3 g, h` |

**Disposition:** usable as an external label. Two of twelve. That ratio is the whole reason
this section exists.

### Class B — asserted-literature, unattributed

`polarity` (`:16`), `on_pathway` (`:84`), `off_pathway` (`:98`), `layout` (`:113`),
`preferred_directions` (`:181`), `on_direction_selective` (`:192`),
`off_direction_selective` (`:260`), `not_direction_selective` (`:328`), `unsufficient_data`
(`:464`), `noisy_data` (`:475`), `motion_tuning` / `on_motion_tuning` / `off_motion_tuning`
(`:506-508`).

The file's docstring (`:1-11`) says its structures *"are based on published literature and may
need to be updated as new research becomes available"*. So these fields are **asserted** to be
literature. Asserted is not the same as shown.

**Disposition — two steps, in order:**

1. **Attribute or demote.** For each field: either a per-field citation is supplied (class A),
   or the field is recorded as **unattributed** and carries that mark into every downstream
   table. Unattributed is a legitimate state; silently borrowing the docstring's authority is
   not.
2. **`polarity` additionally goes through §4.** It is the one class-B field with an existing
   recomputation route, so it can be tested rather than argued about.

### Class C — suspected connectivity-derived

`asymmetric_input` (`:397`) and `symmetric_inputs` (`:477`, derived in-file from
`asymmetric_input` minus two exclusion lists, count 33).

These read like connectome-derived quantities but carry no source. A §8 asks me directly
whether one exists outside the file. **My answer is the design's answer: I do not know, and
nothing in this repository can settle it — so it is settled empirically.** If a field can be
recomputed from the bank, then it is not an external label regardless of what it cites, and
using it to judge a model of the bank is circular.

**Disposition:** subject to §4 alongside `polarity`. **A `symmetric_inputs` that reproduces from
connectivity is a *derived* column and must be recomputed, never extracted** — the same rule
class D already has.

### Class D — derived in-file, not data

`symmetric_inputs` (`:477`, 33), `known_dsi_types` (`:510` = `no_motion_tuning` +
`motion_tuning`, 18), `known_preferred_contrasts` (`:512`, from `polarity`, 32),
`no_motion_tuning` (`:487`, 10).

**Disposition: recompute from their parents inside the extractor; never copy.** A derived column
extracted as data acquires the standing of a measurement it never had — and `known_dsi_types`
and `known_preferred_contrasts` are counts that a reader will quote as if the file had measured
them.

**Extraction spec.** One CSV, 65 rows, key `type_name`, one provenance column per field
(`sourced` / `unattributed` / `derived` / `not_recomputable`), `repr(float(x))`, no rounding, no
reordering — the axis order is part of the artefact, because it is the only thing that makes it
joinable to row A.

---

## 4. The pre-S2 provenance check

**Question.** Is `groundtruth_utils.polarity` a connectivity-derived quantity wearing a
literature label?

**Procedure** (as specified in A §8, restated here as the thing to register, not to improvise):

1. Recompute polarity **from the bank's own input rule** — L1 → ON pathway, L2 → OFF pathway —
   for every type for which the recomputation is defined.
2. Compare, type by type, against `groundtruth_utils.polarity`.
3. Report the **partition**, not a verdict: matched, mismatched, and **not recomputable**
   (types with no L1/L2 input in the bank — the visual types are the ones this rule can speak
   about; the rest it cannot).

**Disposition, registered before the run** — this is a rule about how a result will be read, so
it is written first and is not movable afterwards:

- **Match** → the field is connectivity-derived. It is **not** an external label, and a claim
  that our genome "recovers the literature" using it is circular. The matched types move to
  class C.
- **Mismatch** → the field is independent of our bank, and becomes usable as an external label
  for those types. The mismatches are themselves a result — they say either the literature or
  the bank disagrees with the other — and they are reported as a list, not as a rate.
- **Not recomputable** → outside the check's reach. The label array is then **partially**
  external, and every downstream table carries that partition rather than an overall claim.

**Three clauses that make it a test and not a gesture:**

- The **denominator is the partition**, and it is fixed by the bank, not by the outcome: if a
  reviewer can move an "unclear" type into or out of the matched set after seeing the numbers,
  the check has no power.
- **The same rule is applied to `asymmetric_input` / `symmetric_inputs`** (§3 class C), for the
  same reason.
- **Nobody who runs it writes the reading of it.** The disposition above is written here, before;
  the runner reports the partition; and if the partition does not fit the three cases above, it
  is reported as an open case, not assigned to the nearest one. (ADR-003.)

**Who and when.** Execution is CC's; the word to run it is Mike's (A §8: *"Not to be run without
Mike's word"*). It costs minutes and no GPU. It must run **before** the label array is used
anywhere in step 3, and **before** anyone extracts a column from it — otherwise the extraction
has already made the judgement the check exists to make.

---

## 5. What this design does not license

- **Not the json → bank transition as a target.** Unverified, unlicensed, and not exercised by
  S2 or C6 (B).
- **Not "we predict biology."** Only: *the bank is regenerated from a smaller object*, plus the
  documented transition.
- **Not a verdict on the grammar.** A generative rule for cell types is a different and larger
  design; a success here would be a necessary condition for it, not a licence for it.
- **Not growing anything.** `ROADMAP.md`'s prohibition stands as written.
- **Not a use of any class-B column as an external yardstick** until it is either attributed
  (§3 step 1) or passed through §4.

---

## 6. Order of work, and what each piece waits on

| # | step | owner | waits on |
|---|---|---|---|
| 0 | **Verify A §8's inventory against the source**, line by line, and name the instrument of the negative claim | whoever extracts (CC) | nothing |
| 1 | Word to run the pre-S2 check | Mike | — |
| 2 | Run the check; report the partition | CC | 1 |
| 3 | Extract the label array and the rule bank | CC | 2, and this field list |
| 4 | Two-page note "what is the genome here" | CC | **delivered** (`afdadd0`) |
| 5 | C6 control specification | Zcode | not blocked |
| 6 | Design of a generative rule for cell types (the elephant's first real step) | — | not yet licensed; not this document |

Step 0 is not ceremony. This session's standing lesson is that a paraphrase is not a
verification, and §3 above is a paraphrase of a survey of a file I have not opened.

---

## 7. Acceptance and falsifiers

**Acceptance.**

- `git diff --stat` shows the label-array CSV, the extraction script, and the instrument note —
  no edits under `CS/`.
- Every column of the CSV carries a provenance class; no class-D column was copied.
- The check's report is a partition with its denominator written inside the artefact, and the
  disposition rule printed next to it, dated before the numbers.

**Falsifiers.**

- **For the label array:** if *every* class-B field can be recomputed from the bank, then this
  repository contains **no external label at all**, and the claim narrows to self-consistency.
  That is worth knowing now, before a night of GPU, rather than after.
- **For §4:** if the partition contains no matched and no mismatched type, the check has not run
  — an empty result is a failure of the instrument, not a verdict of independence.
- **For this design:** if the extraction cannot be done without resolving a question this
  document leaves open, the design is incomplete and should be amended **before** the
  extraction, not during it.

---

## 8. Open questions for the owner

1. **Word to run the pre-S2 check** — minutes, no GPU, and it gates the extraction.
2. **Is the label array wanted at all** if §4 shows it is entirely connectivity-derived? The
   honest answer might be "then we have no external yardstick in this repository, and the S2
   claim must be stated as self-consistency plus the transition". That is a smaller claim, and
   it may be the true one.
