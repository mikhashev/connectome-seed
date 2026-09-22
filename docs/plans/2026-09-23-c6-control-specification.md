---
**Status:** SPECIFICATION — written before any rule exists and before any regularity number has
been read. Registers the control; runs nothing.
**Owner of record:** Zcode (`docs/plans/2026-09-16-functional-readout-plan.md` § Roles and
§ "Step 3 — genome"; `ROADMAP.md`; ADR-004 Q3).
**Written by:** CC, 2026-09-23, on Mike's word. The owner told CC to do all of the grammar step's
first pieces himself, including the two nominally owned by Zcode and Ark (Mike, owner,
2026-09-23; paraphrased from Russian, not quoted). **Zcode has not reviewed this text.** It stands
as CC's draft of Zcode's piece until Zcode confirms or amends it.
**No measured results.** Every number below is either a structural integer of the compiled
connectome (already on record in `docs/notes/2026-09-20-what-is-the-genome-here.md` §2 and the
plan's Step-3 boundary block) or a constant chosen here, before data. No loss, activity,
regularity or fit value from any run appears in this file
(`docs/decisions/003-blind-authorship-after-the-numbers.md`).
---

# C6 — the control a regenerating rule must pass

## 0. Where the name comes from, and what this file adds

The repository names C6 in five places and defines it in none. What is fixed in writing is its
**object and its boundary** (Ark, 2026-09-16 19:51 UTC, recorded in
`docs/plans/2026-09-16-functional-readout-plan.md` § "Step 3 — genome"): *C6/S2 fit the compiled
rule bank*, and *the transition json → compiled bank is not verified and not licensed by either
test*. The S2 design (`docs/plans/2026-09-20-genome-design-around-s2.md` §2) states the claim C6
has to guard: **"a rule small enough to be called a genome regenerates the bank, and the
regeneration is not a copy of the table."** The genome note (§6 q.3) leaves the held-out unit
open and warns that C6 "must be specified against the same unit or it controls nothing".

This file turns that into a procedure: what C6 controls against, on which unit, with which
pass/fail rule, at what cost, and what a pass does not license.

## 1. What C6 controls against

A candidate rule can appear to "regenerate the bank" for three reasons that are not the reason we
want. C6 has one arm per reason.

| # | the way a rule can look good without being a genome | the arm that catches it |
|---|---|---|
| 1 | **It is a copy.** It memorised the table, so it reproduces what it was shown and nothing else. | **Held-out arm** (§4.1): score only on type pairs the rule never saw. |
| 2 | **It is a cheap marginal.** Its held-out success comes from facts any trivial model has — how often a type sends edges, how often it receives them, a source type's usual sign. | **Null ladder** (§3): the rule must beat the type-marginal null, not just chance. |
| 3 | **It is not smaller.** It regenerates the table, but its own description is as long as the table's, or a direct encoding of the same length does as well. | **Budget arm** (§4.2): description length, and a size-matched direct encoding. |
| 4 | **Its family fits anything.** Its margin over the null comes from the flexibility of the rule family, not from structure in the fly's wiring. | **Destroyed-structure arm** (§4.3): the same fit on banks whose pair structure has been shuffled. |

Arm 3 is where Clune et al. 2011 must show up (`literature.md` §I.1 entry 13): *"FT-NEAT
outcompetes HyperNEAT when problem regularity is low"*, and the indirect encoding's advantage is
statistically indistinguishable from zero below a regularity threshold. A genome is an indirect
encoding. If the fly's type-pair table is below the threshold for a given rule family, the honest
outcome is that the size-matched direct encoding wins arm 3, and **C6 must be able to return that
outcome** — a control that no plausible rule could fail is not a control. Arm 4 borrows Clune's
instrument directly: a regularity *dial*, built by destroying structure by known fractions (§4.4).

## 2. The object, and what a predictor may see

**Object.** The compiled bank, as the boundary requires: 604 instantiated ordered type pairs,
2,355 rows `(source_type, target_type, du, dv) → n_syn`, one `sign` per pair, at extent 15
(identical at extent 5). The extraction producing it is in progress at `results/genome/bank/`;
C6 reads that extraction and nothing else.

**The target is the full 65 × 65 ordered type-pair table** — 4,225 cells, of which 604 are
non-empty. Each cell carries four fields:

| field | what the rule must produce for a cell |
|---|---|
| **existence** | does the pair connect at all |
| **offset set** | the set of `(du, dv)` offsets present |
| **counts** | `n_syn` per offset |
| **sign** | the pair's ±1 |

Empty cells are targets too. A rule that only fills in cells it is told exist has skipped the
first thing a grammar must decide; that is where most of the table's entropy sits (Ark,
2026-09-20, §5 of the amendment to the S2 design).

**Strata inside the bank** (flags carried by the extraction, per the genome note §6 field list):

- **json-matched rows (2,117):** scored.
- **hull-filled rows (238):** reported, **not scored** for the pass decision. They are produced by
  the convex-hull fill with `n_syn_fill = 1` — a constant set by the json → bank transition, which
  C6 does not license. Scoring them would reward every predictor equally for a step nobody has
  verified, and dilute the contrast between rule and null.
- **`Lawf1 → Lawf1`:** present in the json, absent from the bank (never lands under `stride [3, 2]`).
  Under the bank as object it is an **empty cell**, flagged, and reported separately.
- **the 23 dropped json rows:** not in the bank, not targets.

**Admissible inputs to any predictor, rule or null:**

1. the training-fold cells, all four fields;
2. per-type fields that are part of the bank: `pattern` kind and stride, `layout` role (the labels
   check found `layout` wholly bank-derived, `results/diagnostics/labels/partition.json`);
3. **the 65 types as opaque birth ids**, not as names (`results/genome/bank/`, birth ids, in
   progress).

**Inadmissible:**

- anything from `flyvis.utils.groundtruth_utils` — those are external labels, not the bank;
- `alpha_fixed`, `alpha_references` — provenance of the sign column, and so leakage into the sign
  field (genome note §6 q.2, settled here as *inadmissible*);
- **the strings of the type names.** "T4a", "T4b", "T4c", "T4d" share a stem because anatomists
  already saw the regularity; a rule that parses names imports that human judgement. A rule that
  wants name-derived features must declare them as an extra input, and is then **scored twice** —
  with and without — and the pass decision uses the run without.

## 3. The null ladder

Every null is fitted on the training folds only, with the same folds as the rule.

- **N0 — global marginal.** Existence at the training base rate; offset set = the most frequent
  offset set among training pairs; counts = the median count per offset in training; sign = the
  majority sign in training.
- **N1 — type-marginal (the null that matters).** Existence from an additive source-effect +
  target-effect model (logistic, fitted on training cells); offset set = the source type's most
  frequent offset set in training, falling back to N0 when the source has no training pair;
  counts = source mean × target mean on the log scale, per offset; sign = the source type's
  majority sign in training, falling back to N0. N1 is a direct encoding of *type-level* facts
  with 2 × 65 existence parameters plus per-type tables — cheap, and exactly what a rule must add
  something to.
- **D_k — size-matched direct encoding (budget arm only).** Stores `k` cells of the table verbatim
  (the `k` cells with the largest total `n_syn`, ties broken by birth id) and answers N1 for every
  other cell; `k` is set so that the description length of D_k equals the rule's (§4.2).

N0 is a sanity floor — a rule that does not beat N0 has not run. **The pass decision is against N1
and D_k.**

## 4. The procedure

### 4.1 Held-out arm — the unit is the ordered type pair

**Decision: the held-out unit is the ordered type pair `(source_type, target_type)` — a whole
cell of the 65 × 65 table, with all its offsets, counts and sign, and including empty cells.**

Why not the others:

- **Not the row (offset).** Splitting by row leaks the pair's remaining offsets: offsets of one
  pair are contiguous on the hex lattice and share the pair's sign and scale, so a held-out row is
  predicted from its own pair's other rows. That measures interpolation inside a pair, which even
  a lookup table with smoothing does, not the regularity *between* pairs that a genome would have
  to express. (The genome note, §6 q.3, names the leak.)
- **Not the cell type.** Holding out a type removes all 129 of its cells at once (65 outgoing,
  65 incoming, the self-pair counted once). Under opaque birth ids a new type carries no information except `pattern` and `layout`, so
  every predictor fails and the arm has no power to separate a rule from a null. It asks a
  different question — can a rule place a type it has never seen — which is point 1's later
  question (adding a cell type by mutation), not this one. It is run as a **secondary,
  descriptive** split (§4.5) and does not enter the decision.
- **The type pair** is the smallest unit with no within-unit leak, and the unit a genome would
  vary: a mutation adds, removes or rewires a pair. Leakage *across* pairs through shared source or
  target types is not a leak here — it is precisely the regularity the rule is supposed to find,
  and N1 already credits the part of it that is only marginal.

**Folds.** 10 folds over the 4,225 cells, stratified so each fold holds one tenth of the non-empty
cells and one tenth of the empty ones. Assignment is by a keyed hash of the pair's two birth ids
(sha256 of `"C6-v1:" + src_birth_id + ":" + tar_birth_id`, taken mod 10 within each stratum's
sorted order). The fold file is generated once, hashed, and committed **before any rule is fitted
or any regularity figure is read**; it is never regenerated for a new rule.

**Per fold**, fit the rule and N1 on the other nine folds, predict the held-out fold, and score:

| field | score (pre-stated) | scored on |
|---|---|---|
| existence | mean log-loss; hard outputs clipped to [0.001, 0.999] | all held-out cells |
| offset set | mean Jaccard of predicted vs true offset sets | held-out non-empty cells |
| counts | mean absolute error of `log1p(n_syn)`, a missing offset counting as predicted 0 | held-out json-matched rows |
| sign | fraction correct | held-out non-empty cells |

The four scores are **reported separately and never summed** into one number.

### 4.2 Budget arm — is the rule smaller, and does a direct table of its size do as well

Description length, one fixed accounting for every predictor: **32 bits per real-valued
parameter; ⌈log2 m⌉ bits per discrete symbol drawn from an alphabet of size m; the fixed decoder
(the program that turns a rule into a table) is not charged**, and must therefore be the same
decoder for the rule and for D_k. The bank's own description length is computed with the same
accounting.

In-sample (all folds pooled), compare the rule with D_k at equal description length on the four
fields of §4.1.

### 4.3 Destroyed-structure arm — does the margin survive shuffling

Build **20 shuffled banks**, each with a fixed recorded seed:

- existence: a degree-preserving rewiring of the 65 × 65 table (each type keeps its out-degree and
  in-degree in pairs);
- offset sets, counts and sign: each non-empty cell of the shuffled table receives the four-field
  content of a **uniformly drawn non-empty original cell**, so the value distributions are kept
  and the pair-to-content assignment is destroyed.

On each shuffled bank, re-run §4.1 with the same folds (by cell position), for the rule and N1,
and compute the **margin** = rule minus N1 per field (signed so that larger is better).

### 4.4 The regularity dial (Clune's instrument, descriptive)

Repeat §4.3 with only a fraction `f` of non-empty cells shuffled, `f ∈ {0, 0.25, 0.5, 0.75, 1}`,
5 seeds per `f`. Report the rule's margin over N1 and over D_k as a function of `f`. This is the
Clune et al. design transplanted: regularity as a knob with a number on it. It is descriptive and
**does not enter the pass decision** (§5); its registered reading is in §5.3.

### 4.5 Secondary split — leave one cell type out (descriptive)

65 folds, each holding out every cell with that type as source or target. Scored as §4.1, rule and
N1. Descriptive only; it does not enter the decision.

## 5. Pass and fail, stated before any rule or number exists

### 5.1 A rule passes C6 if and only if all three hold

- **P1 — generalises beyond marginals.** On the primary split, the rule beats N1 on **existence**
  and on **offset set** in **at least 9 of 10 folds each** (one-sided sign test, p ≈ 0.011 per
  field); and on **counts** and **sign** it is **not worse than N1 in more than 5 of 10 folds**.
- **P2 — is a genome, not a restatement.** Its description length is **at most one tenth** of the
  bank's under §4.2's accounting, **and** at that length it beats D_k in-sample on existence and
  offset set.
- **P3 — the margin is structure.** For existence and offset set, the rule's margin over N1 on the
  real bank (mean over folds) **exceeds its margin on every one of the 20 shuffled banks** (rank
  1 of 21, one-sided p ≈ 0.048).

### 5.2 Everything else is a fail, and is named by the arm that failed

- P1 fails → **"copy or marginal"**: the rule does not generalise beyond type marginals.
- P2 fails on length → **"not a bottleneck"**; fails against D_k → **"below threshold for this
  family"** — Clune's result, reproduced on the fly. This is a legitimate and informative outcome.
- P3 fails → **"family fits anything"**: the margin over N1 is flexibility, not structure.
- If N0 beats the rule on any field in more than 5 folds, the run is reported as **"rule did not
  run"**, not as a fail of the grammar.
- A fold where N1 cannot be fitted is reported as open, not dropped; the denominator stays 10.

Nobody who runs C6 writes its reading beyond these labels (ADR-003). A result that does not fit
the labels is reported as **OPEN**, not assigned to the nearest one.

### 5.3 How the regularity dial is to be read (registered now)

If the rule's margin over D_k at `f = 0` (the real bank) is **no larger than its margin at
`f = 0.5`**, the real bank is recorded as behaving, for this rule family, like a half-shuffled
one — below the family's regularity threshold — whatever P1–P3 say. The crossing point, if any,
is reported as a value of `f`, not as a verdict.

### 5.4 Relation to the regularity measurement

The regularity measurement being produced alongside the extraction
(`results/genome/bank/REGULARITY-READING.md`, **forthcoming; not read when this was written**)
estimates how regular the type-pair table is. C6 does not depend on its numbers and must not be
tuned after reading them: every constant above (10 folds, 9 of 10, one tenth, 20 shuffles, the
dial fractions) is fixed here, dated 2026-09-23, before that file exists. The two are meant to be
read together afterwards: the regularity reading predicts which regime C6 will operate in, and C6
is the test of that prediction for a particular rule. A low regularity reading followed by a C6
pass, or a high one followed by a "below threshold" fail, is itself worth reporting — it would mean
the regularity measure and the rule family disagree about what "regular" is.

## 6. Cost

- **The nulls, the fold file, the shuffled banks, the dial:** CPU only, seconds to minutes; a
  4,225-cell table and closed-form or logistic fits. **No GPU.**
- **Per candidate rule:** 10 (primary) + 20 × 10 (shuffled) + 25 × 10 (dial) + 65 (secondary)
  = **525 fits**. The rule's fitting cost is the rule's, not C6's; if one fit is expensive, the
  dial (250 fits) is the first thing dropped, and the drop is reported. P1–P3 need 210 fits and
  are not reduced.
- **Nothing in C6 trains a network or reads a checkpoint.** The measurement line stays paused
  (ADR-004 amendment) and C6 does not touch it.

## 7. What a pass does NOT license

- **Not "we predict biology."** Only: *the compiled bank is regenerated, on held-out type pairs,
  from a smaller object, beyond what type marginals give* (S2 design §2, §5).
- **Not the json → bank transition.** Hull-filled rows are unscored; the transition stays
  unlicensed (plan § "Step 3 — genome", boundary block).
- **Not a working fly.** A regenerated bank that is close field by field can still behave
  differently once compiled and trained. That is a functional test, it needs a GPU, and it waits on
  the measurement line being resumed.
- **Not heredity or composability (idea.md point 3).** C6 says nothing about whether modules of the
  rule can be inherited, grafted or crossed; that needs birth ids and a crossover test of its own.
- **Not growth, and not the elephant.** `ROADMAP.md`'s prohibition on growing anything stands.
- **Not a ranking of two passing rules** beyond the four per-field scores; picking between rules is
  a separate decision.
- **Not a statement about any other connectome.** A pass is about this bank.

## 8. Sources

- `docs/plans/2026-09-16-functional-readout-plan.md` — § Roles; § "Step 3 — genome" and its
  boundary block (Ark, 2026-09-16 19:51 UTC).
- `docs/plans/2026-09-20-genome-design-around-s2.md` — §2 the claim, §5 the licence, §6 the order
  of work, and its amendment of 2026-09-23.
- `docs/notes/2026-09-20-what-is-the-genome-here.md` — §2 structural counts; §6 q.1–q.3.
- `results/diagnostics/labels/README.md`, `partition.json` — `layout` is bank-derived; sign
  provenance.
- `literature.md` §I.1 — entry 12 (HyperNEAT), entry 13 (Clune et al. 2011, the regularity dial and
  the threshold); §"What this changes for us" item 4.
- `results/genome/bank/` — the extraction, birth ids and `REGULARITY-READING.md`, in progress by
  another agent; cited as forthcoming.
