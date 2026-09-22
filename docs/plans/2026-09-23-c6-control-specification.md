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

---

## Amendment — 2026-09-23, before any harness or rule

**Written by:** CC (subagent), 2026-09-23, on Mike's word ("build the C6 exam without a rule, so
the exam itself can be checked", paraphrased from Russian). **Why:** two reviews of the text
above, both in the DPC Research chat on 2026-09-23 and both translated from Russian:

- **Ark, 20:10 UTC.** Birth ids must be derivable from the entity, not from the order it was
  listed in. Name `k` explicitly. A random projection of the same rank is a falsifier.
- **Zcode, 20:19 UTC.** Three holes to close before the harness: (1) the description-length
  accounting can be gamed; (2) the folds file does not exist yet; (3) the statistics at the
  decision points are thin.

**State when this was written.** No harness, no rule, no C6 score and no folds file existed.
`results/genome/bank/REGULARITY-READING.md` **had been published**, and its numbers were known to
the author of this amendment. Only one constant below comes from it: the 18-component mark in
A6, which Ark named. That clause only **adds** a comparison and relaxes nothing, so it cannot make
a pass easier. Every other number below is a convention chosen for a stated reason, or
arithmetic on the grid's structural counts (65 types, 4,225 cells, 604 non-empty, 2,117
json-matched rows).

**How to read it.** The text above is not edited. Each item names the passage it changes and
says whether it **replaces** it, **clarifies** it (the original was ambiguous; this fixes one
reading), or **adds** to it. Where an item and the original disagree, the item governs. Every
number in this amendment is a pre-registered constant, not a result.

### A1. Identifiers: content-derived birth ids, and what "opaque" can and cannot mean — *replaces* §2 input 3 and every "birth id" in §3–§4

- Birth ids are now **derived from names** (`results/genome/bank/REGISTRY.md` § Revision v1). A
  type's id is the first 12 hex digits of sha256(`cs-birth-v1|type|<name>`). A pair's id is the
  first 12 hex digits of sha256(`cs-birth-v1|pair|<src>-><tar>`). The pair function is defined
  on all 4,225 cells, so an empty cell also has an id. The old integer ids survive only as
  `display_no`, and C6 never uses them.
- **The ids are not secret.** The 65 names are public, so anyone can hash them and invert the
  mapping. No deterministic public relabelling can hide the names from code that wants them. So
  opacity is enforced by **what the harness hands to a rule and by review**, not by cryptography.
  - The harness gives a rule each type as an **integer index 0–64**, ordered by the type's birth
    id (hex string order). It passes no names and no birth ids.
  - It also passes the admissible per-type fields of §2: `stride_u`, `stride_v`, `role` and
    `layout`.
  - A rule's source must not contain a type name, a birth id, or a hash of either. The reviewer
    checks the charged source for this (A5). If a rule is found to break it, it is scored under
    §2's "with names" branch and cannot pass.

### A2. The folds — *clarifies* §4.1 "Folds"

- **Strata.** *Non-empty* means the 604 pairs present in the compiled bank. *Empty* means the
  other 3,621 cells, including `Lawf1 → Lawf1`, which is flagged in the file.
- **Key.** For each cell, key = sha256 of the UTF-8 string `"C6-v1:" + pair_birth_id`, as hex.
  The original text hashed `src_birth_id + ":" + tar_birth_id`. A1 replaces those integer ids,
  and a pair id is already a function of the two names, so the key uses the pair id.
- **Assignment.** Within each stratum, sort cells by key (hex string, ascending), and set
  fold = rank mod 10, with ranks counted from 0. This is how "taken mod 10 within each stratum's
  sorted order" is read here. It gives exact balance: 61 non-empty cells in folds 0–3 and 60 in
  folds 4–9; 363 empty cells in fold 0 and 362 in folds 1–9.
- **Files.** The generator is `results/genome/c6/make_folds.py`. It writes `folds.csv` and
  `folds.meta.json`, which record the sha256 of this specification and of the generator. It
  refuses to overwrite an existing `folds.csv` that differs from what it would write. The folds
  file is committed before any harness or rule code exists (Zcode, hole 2).

### A3. Fields and what each score reads — *clarifies* §2 and the §4.1 score table

- **Existence** of a cell is true iff the cell is one of the 604 compiled pairs.
- **Offset set** of a non-empty cell is the set of its `in_json` offsets. `hull_filled` rows are
  excluded, as §2's strata already require. Jaccard between two empty sets is 1. A cell whose
  true set is empty cannot occur among the 604.
- **Counts** are scored on held-out `in_json` rows only. Each row's target is `log1p(n_syn)`,
  with `n_syn` the compiled value. The prediction is `log1p` of the predictor's count for that
  offset in that cell, or 0 if the predictor gives none. Extra predicted offsets do not enter
  the count score; the Jaccard score already charges them.
- **Sign** is the pair's `alpha`, scored as the fraction of held-out non-empty cells with the
  correct sign.
- Logarithms in log-loss are natural.

### A4. The nulls, fitted exactly — *clarifies* §3

All nulls are fitted on the training folds only.

- **N0.**
  - Existence: the training base rate.
  - Offset set: the most frequent `in_json` offset set among training non-empty cells.
  - Counts: for each offset in that set, the median `log1p(n_syn)` of training `in_json` rows
    at that offset.
  - Sign: the training majority; a tie gives +1.
  - **Ties for the most frequent set** go to the smaller set, then to the lexicographically
    smaller sorted list of `(du, dv)`. This tie rule is used everywhere below.
- **N1.**
  - *Existence:* logit p = c + a_s + b_t, fitted by maximum likelihood with an L2 penalty
    ½·λ·(Σa² + Σb²), λ = 1. The intercept is not penalised. The fit stops when the gradient norm
    falls below 1e-8. Why a penalty: a type with no training partners, such as the two types that
    are never a source, would otherwise get an effect of −∞. λ = 1 is the standard weak choice.
    It amounts to a unit-normal prior on each log-odds effect.
  - *Offset set:* the source type's most frequent `in_json` offset set among its training
    non-empty cells. If it has none, N0's set.
  - *Counts:* for each offset o of the predicted set, `log1p` prediction = m_o + α_s + β_t.
    - m_o is the mean over training `in_json` rows at offset o, or the mean of all training rows
      if o is unseen.
    - α_s is the mean of (value − m_o) over the source's training rows.
    - β_t is the mean of (value − m_o − α_s) over the target's training rows.
    - A missing effect is 0.
    - This is how "source mean × target mean on the log scale, per offset" is read here: two
      additive effects on the log scale, with an offset-specific base.
  - *Sign:* the source type's majority sign over its training non-empty cells. A tie, or no
    pair, gives N0's sign.
- **Clipping.** Every predictor's existence probability is clipped to [0.001, 0.999] before
  scoring. This covers N0, N1, D_k, RP_r, the controls and the rule. The original clipped only
  hard outputs. Clipping everyone the same way stops any predictor from winning or losing
  through one infinite log-loss term (Zcode, hole 3).

### A5. Description length: what is charged, and what the shared decoder is — *replaces* the accounting paragraph of §4.2 (Zcode, hole 1)

**Every predictor is scored as a pair (program, data).** This covers the rule, N1, D_k, the
stored bank and every control.

- The **program** is the source file of the predictor's `decode` module. It turns `data` into
  predictions for any list of cells, given only the admissible per-type fields of A1.
- The **data** is a dictionary of named numpy arrays.
- The **learner** that produced the data from the training cells is **not** charged. It is not
  part of the description; only what it outputs is.

**The uncharged decoder is the same for everyone.** It is CPython 3.10, its standard library,
numpy (the version pinned in the harness record), and the harness's scoring code. That is all.
So "the same uncharged decoder for the rule and for D_k" means one interpreter, not one program:
*both* D_k's decode module and the rule's are charged, by the same formula.

- A decode module may import only the standard library and numpy. Any other import leaves its
  length undefined, and the run is reported OPEN.
- The decode module must be a pure function of `data`, the per-type fields and the list of
  cells. The harness reloads the module before decoding and hands it deep copies. Anything the
  module keeps elsewhere, such as a module-level cache filled by the learner, is a defect of the
  rule.

**Bits charged:**

| item | bits |
|---|---|
| program | 8 × the byte length of the UTF-8 source file compressed with lzma, raw LZMA2 format, preset 9 \| EXTREME. Comments count; an author who wants them free can remove them. |
| real number | 32. The harness casts every float array to float32 **before** decoding, so the charged precision is the precision actually used. |
| integer | Elias-gamma length of zigzag(x) + 1, where zigzag maps 0, −1, 1, −2, … to 0, 1, 2, 3, …. The code is universal, so no range has to be declared. |
| symbol from an alphabet of size m | ⌈log₂ m⌉, where m is either a literal in the charged program or a charged integer in the data. m = 1 costs 0. |
| boolean | 1 |
| array shape | the integer code, once per dimension |
| array name | 8 per character |
| anything else (strings, objects, pickles) | not allowed: the run is OPEN |

**The three predictors that are pure storage** use one storage format, so they are comparable:

- **Stored cell** (D_k's stored cells, and the bank).
  - The cell address is a symbol from 4,225 cells: 13 bits.
  - The sign is 1 bit.
  - The number of `in_json` offsets is charged with the integer code.
  - For each offset: du and dv with the integer code, and `n_syn` as a real (32 bits).
- **How `n_syn` is charged** (Zcode's "integer n_syn"). In this bank `n_syn` is real-valued: it
  is an average over filters, and most json-matched values are not whole numbers. Stored
  verbatim it is a real, at 32 bits. A predictor that chooses to output whole-number counts
  may store them with the integer code. It is then scored on what it outputs, rounding error
  included.
- **The bank's own length**, DL(bank), is the length of the predictor S_all. Its program is a
  decode module that reads stored cells. Its data is all 604 non-empty cells in the stored-cell
  format, and every unstored cell is empty. The hull-filled rows are not stored: they are
  regrown by the decoder the transition uses, and C6 does not score them.
- **Do the N1 tables count in D_k's length? Yes.** D_k is N1 plus k stored cells, and it is a
  complete predictor. Its length is: its decode program + N1's data fitted on the full bank + the
  k stored cells. The same holds for any rule that uses N1 or N0 inside itself: it pays for them
  as data and as program.
- N1's data under this accounting:
  - existence: 131 reals;
  - offset sets: one stored offset set per source type, in the stored-cell offset format without
    counts, plus 1 bit per type for "falls back to N0";
  - counts: one real per distinct training offset for m_o, plus 130 reals for α and β;
  - sign: 65 symbols from {−1, +1, fall back}, 2 bits each;
  - N0's own data, for the fallbacks.

### A6. `k` named explicitly, and the 18-component mark — *replaces* the D_k definition's "k is set so that…" in §3 (Ark)

- **The order of cells.** D_k's stored cells are taken in decreasing order of total `in_json`
  `n_syn`. Ties go to the smaller pair birth id (hex string order).
- **DL(D_k)** = L(D_k's decode program) + L(N1 data, full-bank fit) + the sum of the first k
  stored-cell costs.
- **k\*(rule)** = the largest k in 0…604 with DL(D_k) ≤ DL(rule).
  - If even D_0 (N1 alone) is longer than the rule, k\* = 0. The rule is then compared with
    D_0, and the record says so.
  - k\*, DL(rule), DL(D_k\*) and DL(bank) are written into every C6 record as numbers. "The
    size-matched table" is never left implicit.
- **The 18-component mark.** M18 = 18 × (65 + 65) × 32 = **74,880 bits**. That is the parameter
  cost, under A5, of a rank-18 factorisation of the 65 × 65 log-count table: 18 is the number
  of components that carries 90 % of that table's energy (`REGULARITY-READING.md` §2, the one
  number this amendment takes from a published result). Ark's clause, as registered:
  - **A rule with DL(rule) < M18 must beat D_k\* in-sample on existence and on offset set.**
    P2 already requires this of every rule. The clause makes it explicit that being "small by
    the regularity reading's own yardstick" is not a pass by itself.
  - The harness also reports k18 = the largest k with DL(D_k) ≤ M18, and D_k18's scores, as a
    fixed reference point on the size axis. k18 is reported, not decided on.
- **In-sample "beats"** in P2 uses the tolerance and tie rule of A7, on all 4,225 cells (for
  existence) or all non-empty cells (for offset set), with both predictors fitted on the full
  bank.

### A7. What "beats" means: ties and tolerance — *adds* to §5 (Zcode, hole 3)

- **A win.** In a fold, a predictor beats another on a field iff its score is better by more
  than τ.
  - τ = 1e-9, absolute, for existence log-loss, offset-set Jaccard and count MAE.
  - For sign, the two predictors' numbers of correct cells are compared as integers, with no
    tolerance.
- **Why τ is tiny, not a practical margin.** τ only makes identical predictions count as ties
  despite floating-point noise. Whether a margin is large enough to matter is judged by P2 (is
  it smaller than a table) and by P3 and P4 (is it structure). A per-fold effect-size threshold
  would be a third, arbitrary judge of the same thing.
- **Ties.** A tie is **not a win** when superiority is tested (P1 on existence and offset set;
  P2; P3; P4). It is **not a loss** when non-inferiority is tested (P1 on counts and sign; the
  "rule did not run" check).

### A8. P1, stricter on counts and sign — *replaces* the second half of §5.1 P1 (Zcode, hole 3)

- Existence and offset set are unchanged: at least 9 of 10 fold wins on each. Each is a
  one-sided sign test at p = 11/1024 ≈ 0.011.
- **Counts and sign, new:** the rule is worse than N1 (by more than τ) in **at most 2 of 10
  folds** on each field, **and** its mean score over the 10 folds is not worse than N1's.
- **Why 2 of 10.** The original allowed 5 of 10, which is what a rule that loses to N1 half the
  time would show. Take a rule that really is worse than N1 at least half the time. The chance
  that it shows at most 2 worse folds out of 10 is (1 + 10 + 45)/1024 = 56/1024 ≈ 0.055.
  So "at most 2 of 10" is a one-sided non-inferiority sign test at about the 5 % level, the
  mirror image of the 9-of-10 superiority test. "At most 1 of 10" would be the 1 % test. It is
  not chosen: on sign, where N1 is nearly always right, a rule could lose one fold by a single
  cell through bad luck.

### A9. P3 with 99 shuffled banks — *replaces* "20 shuffled banks" in §4.3 and P3's "rank 1 of 21" (Zcode, hole 3)

- **The multiple-testing question.** P3 is applied to two fields, and **both** must hold for a
  pass. When a verdict needs every one of several tests to succeed (an intersection-union test,
  Berger 1982), the chance of a false pass is at most the largest single-test level, not their
  sum. So the original's 1/21 was not inflated by the two fields.
- **Why it is still changed.** 1/21 ≈ 0.048 sits right at 5 %. And the §5.2 fail labels are
  read field by field, which is a per-field claim that does need a correction. So:
  - **99 shuffled banks**, with seeds 0–98, replace the 20.
  - P3 holds on a field iff the real-bank margin (mean over folds) is **strictly greater than**
    the margin on all 99. That is rank 1 of 100, a Monte Carlo p ≤ 0.01 per field.
  - Bonferroni over all four fields gives 4 × 0.01 = 0.04 < 0.05, so even a claim made about any
    single field keeps family-wise error under 5 %.
  - 99 (B + 1 = 100) is the conventional Monte Carlo test size (Davison & Hinkley 1997, ch. 4).
- **Ties.** A tie with a shuffled bank counts against the rule.
- **Cost.** 990 rule fits instead of 200 (see A13).

### A10. The shuffle, exactly — *clarifies* §4.3 (Zcode, hole 3: "with or without replacement")

- **Existence: degree-preserving rewiring.** Start from the 65 × 65 binary table of non-empty
  cells. Repeatedly pick two non-empty cells (s₁, t₁) and (s₂, t₂) uniformly. If (s₁, t₂) and
  (s₂, t₁) are both empty and distinct, move the two entries there. Stop after 20 × 604 = 12,080
  **successful** swaps.
  - Self-pairs (s, s) are ordinary cells.
  - Every type keeps its out-degree and in-degree exactly.
  - 20 swaps per edge is a common mixing length for this Markov chain. The count is fixed here,
    not tuned.
- **Content: without replacement.** The 604 four-field contents are the `in_json` offsets with
  their counts, the hull rows and the sign. They are permuted uniformly at random over the 604
  non-empty cells of the rewired table.
  - **Why without replacement.** It keeps the multiset of contents exactly, not just in
    expectation, so the only thing destroyed is which pair gets which content. Drawing with
    replacement would duplicate some contents and lose others, and change the value
    distributions by chance. That is a second, unintended source of variation.
- **Randomness.** numpy `Generator(PCG64(seed))`, one seed per shuffled bank, shared by the
  rewiring and then the permutation, in that order.
- The same folds are used by cell position, as §4.3 says.

### A11. The random-projection arm — *adds* §4.6 and P4 (Ark: "ambient, not substantive structure")

**The question.** Does the rule's margin need *its* structure, or would any rank-r structure
with the same number of fitted numbers do as well?

- **The rank r of a rule.** The rule declares r, the dimension of its per-type latent
  representation. A rule without one gets r = max(1, round(n_real / 130)), where n_real is the
  number of reals in its full-bank data. So RP_r fits about as many reals as the rule stores.
  r is capped at 64.
- **The predictor RP_r, seed j** (existence field):
  - logit p(s, t) = N1 logit(s, t) + Σᵢ G[s, i] · B[t, i], for i = 1…r.
  - G is 65 × r with iid entries N(0, 1/r), drawn from `Generator(PCG64(1000 + j))`, and it
    stays fixed: this is the random projection.
  - B is fitted on the training cells by L2-penalised logistic regression (λ = 1, as N1), with
    the N1 logit held fixed as an offset.
  - The transposed variant puts G on the target side and fits the source side.
  - RP's margin for seed j is the better of the two variants: N1's log-loss minus RP's, as a
    mean over the 10 folds. Taking the better variant is conservative against the rule.
- **P4 — the margin is not ambient.** The rule's existence margin over N1 (mean over folds) is
  strictly greater than the largest RP_r margin over seeds j = 0…19.
  - This is a threshold, "beat the best of 20 random controls", not a p-value.
  - Failure label: **"ambient, not substantive structure"**.
- **Why existence only.** Rank is defined for a matrix field. Existence is the 65 × 65 matrix
  on which the regularity reading measured concentration. An offset set is a set per cell, and
  a "random projection" of it would be a construction invented here, not Ark's control. P3's
  shuffle already guards the offset set. RP_r's counts are reported descriptively (same
  construction on the per-row residuals of N1's counts, least squares, same λ), and do not
  decide anything.
- **§5.1 therefore reads "all four hold"**: P1, P2, P3, P4.

### A12. The regularity dial, exactly — *clarifies* §4.4

For each f and seed:

- choose round(f × 604) non-empty cells uniformly at random;
- rewire only among them: swaps as in A10, using only chosen cells, for 20 × (number chosen)
  successful swaps, or until 100 × that many attempts have been made; the number achieved is
  reported;
- permute their contents among themselves, without replacement.

Seeds are 10000 + 100·(f index) + seed. The dial still does not enter the decision.

### A13. Cost, revised — *replaces* the per-rule count in §6

Per candidate rule: 10 (primary) + 99 × 10 (shuffled) + 25 × 10 (dial) + 65 (secondary) =
**1,315 rule fits**.

- P1–P4 need **1,000** of them. The 20 × 2 × 10 = 400 RP_r fits are cheap logistic fits and
  are not counted as rule fits.
- If one rule fit is expensive, the dial is still the first thing dropped.
- **P3 is not reduced below 99 banks.** If 99 is unaffordable for some rule, that rule's P3 is
  reported OPEN, not run at 20.
- Still CPU only.

### A14. The exam checks itself first — *adds* §4.7

Before any rule is scored, the harness runs controls with **no rule in it**. What each must show
is registered here, before the harness exists:

| control | what it is | must show |
|---|---|---|
| (a) oracle | returns the true held-out cells | P1 won on all four fields in every fold. Its data holds the whole table, so DL ≥ DL(bank) and it **fails P2 on length** ("not a bottleneck"). An oracle that passes C6 is a defect of the exam. |
| (b) N1 submitted as a rule | the N1 predictor | P1 on existence and offset set: **0 wins** (every fold a tie). P1 on counts and sign: no loss. It must not pass. |
| (c) RP_r as a rule | r = 8, seed 999, outside P4's seeds | Must not pass C6. Whatever P1 shows is reported. |
| (d) shuffled banks | the 99 banks of A10 | Each keeps every type's in- and out-degree exactly, has exactly 604 non-empty cells, and holds the same multiset of contents. N1's existence score on them is reported next to the real bank's. |

Any control that does not behave as registered is reported as a **defect of the exam**, in
plain words, before any rule is run.

### A15. Constants registered by this amendment

| constant | value | item |
|---|---|---|
| birth-id rule version, id length | `cs-birth-v1`, 12 hex digits | A1 |
| fold key prefix, number of folds | `C6-v1:`, 10 | A2 |
| N1 penalty λ, convergence | 1, gradient norm < 1e-8 | A4 |
| existence clip | [0.001, 0.999], all predictors | A4 |
| real, program, cell address | 32 bits; 8 × lzma-raw preset 9 \| EXTREME bytes; 13 bits | A5 |
| tie tolerance τ | 1e-9 absolute; exact for sign counts | A7 |
| P1 existence and offset set | ≥ 9 of 10 wins each | §5.1, unchanged |
| P1 counts and sign | ≤ 2 of 10 losses each, and a fold mean not worse | A8 |
| shuffled banks for P3 | 99, seeds 0–98, strict rank 1 of 100 | A9 |
| rewiring length | 20 × 604 successful swaps | A10 |
| RP seeds, rank rule, cap | 20 (projection seeds 1000–1019), r declared or round(n_real / 130), ≤ 64 | A11 |
| M18 | 74,880 bits | A6 |
| P2 length limit | DL(rule) ≤ DL(bank) / 10 | §5.1, unchanged |
| dial | f ∈ {0, 0.25, 0.5, 0.75, 1}, 5 seeds each | §4.4, unchanged |

---

## Amendment 2 — 2026-09-23: registration of acceptance criteria, before the fix

**Written by:** CC (subagent), 2026-09-23, under option A (Mike, owner, 2026-09-23 21:01 UTC).
**Why:** the harness controls found three defects in the exam (`results/genome/c6/HARNESS-CONTROLS.md`
§ "Findings about the exam"). The reviewers asked that what the fixed exam must be able to do be
registered **before** the fix (Ark, genome track, 2026-09-23 20:43 UTC; Johnny, reviewer,
2026-09-23 20:53 UTC; Zcode, owner of record of C6, 2026-09-23 20:58 UTC).

### A16. Acceptance criteria are registered in a separate file — *adds*

`docs/plans/2026-09-23-c6-amendment-acceptance.md`, sha256 (LF-normalised)
`bd3697719aa96a2d6c39078d7d01823009746de50b694debecc0f0d450b43d3b`. The amendment that follows
(A17 onwards) is judged against it by code, criterion by criterion. It is committed alone, before
any change to the exam. The text above this section, up to and including A15, is unchanged. Its
first 41,349 bytes (LF-normalised) still hash to the value recorded in
`results/genome/c6/folds.meta.json`, and every amendment only appends.

### Amendment 2, continued — 2026-09-23: the fix (A17–A22)

**Written by:** CC (subagent, the builder of the harness), who has not read the proposed rule
(declaration: `docs/plans/2026-09-23-c6-amendment-acceptance.md` §(e)). **Judged against:** the
acceptance criteria of A16, by code. The results are in `results/genome/c6/harness_controls.json`
and `HARNESS-CONTROLS.md`. As above, every number here is a registered constant, not a result.

**Monotonicity (acceptance §(b)).**

- A5's bit table, the one-tenth constant and every threshold of A1–A15 are unchanged.
- The items below only add opponents, or raise thresholds.

#### A17. The budget arm, armed — *adds* an opponent to §5.1 P2 (hole 1; Zcode's fix, Ark's principle)

- **D_k^N0.** It stores the first k cells in A6's order, verbatim in A5's storage format, and
  answers N0 everywhere else.
  - Its program is `decoders/n0_decode.py` + `decoders/store_decode.py` +
    `decoders/dk0_decode.py`, compressed together and charged once. Its data is N0's data plus
    the k stored cells.
  - **One basis, one charge:** each predictor pays for its own basis once, and for nothing it
    does not use. D_k^N0 carries no N1.
- **k\*_armed(rule)** = the largest k in 0…604 with DL(D_k^N0) ≤ DL(rule). It is written into
  every record next to k\*.
- **P2, amended.** A rule passes P2 iff:
  - DL(rule) ≤ DL(bank) / 10 (unchanged); **and**
  - in-sample, it beats each of the following on existence and on offset set (A7's tie rule):
    **D_k^N1 at k\*** (the A6 opponent, kept), **D_k^N0 at k\*_armed** (new), and **N1** (new).
- The label for failing any of the three is "below threshold for this family".
- **Convention 2 is folded in here.** The budget arm is defined **in-sample** only: P2, and the
  dial's margin over the stored table (§5.3). A held-out D_k is not defined, because its stored
  cells come from training folds only, so on held-out cells it equals its fallback.
  - The dial reports the in-sample margin over both D_k^N1 at k\* and D_k^N0 at k\*_armed, next
    to the held-out margin over N1.
  - The finding that the old arm could not fail (k\* = 0) and this convention were one defect.
    A17 closes both (Ark, genome track, 2026-09-23 20:43 UTC).
- **Acceptance test of the arm:** R1–R3 of the acceptance file. A rule no better than N1 must
  lose to the table of its own size.

#### A18. The offset-set target, strengthened — *adds* opponents to §5.1 P1 (hole 2)

- **N_EB.** A smoothed, per-source, empirical-Bayes distribution over offset sets, shrunk
  toward the global one. It predicts the observed set with the highest expected Jaccard. Its
  other fields are N1's.
  - The definition, and the nested choice of α from {0.5, 1, 2, 4, 8, 16, 32, 64, 128} (ties to
    the larger α), are those registered in the acceptance file §(b). They are not re-stated here
    so that there is only one text. The α chosen in each fold is recorded.
  - Program: `decoders/n1_decode.py`. N_EB is N1's data with the per-source sets replaced.
- **P1's offset arm, amended.** The rule must beat **each** of N1 (as before), N0 and N_EB, in
  at least 9 of 10 folds each.
  - This keeps the old test and adds two, so it cannot become easier.
  - It also closes the "N1 weaker than N0" finding without re-defining N1.
- **Registered control number:** N_EB's mean held-out Jaccard on the real bank ≥ 0.4465 (M3).

#### A19. P4, replaced by a trained factorisation — *replaces* A11's threshold by a larger one (hole 3)

- **BF_r.** Existence logit = N1 logit + U_s·V_t, with U and V of size 65 × r, where r is A11's
  rank of the rule.
  - Fitted by penalised likelihood, from an SVD initialisation, with 25 alternating Newton
    sweeps and λ chosen by nested CV from {1, 3, 10, 30, 100} (ties to the larger λ). The
    definition is exactly that of the acceptance file §(b).
  - Program: `decoders/n1_decode.py` + `decoders/bf_decode.py`.
- **P4, amended.** The rule's existence margin over N1 (mean over folds) must be strictly
  greater than **max(the A11 random-projection threshold, BF_r's margin)**.
  - A11's random projection is still computed, so the threshold can only rise.
  - Failure label: unchanged, "ambient, not substantive structure".
- **Registered control number:** BF_8's mean held-out existence margin over N1 on the real bank
  > 0 (M4).

#### A20. The planted-rule acceptance suite — *adds* §4.8 (Ark, Johnny)

The generator (PL, seed 4242, K = 4, a cycle pattern, strengths ρ ∈ {1, 0.5, 0}), the planted
rule (PR), the scrambled genome (seed 99), and criteria R1–R3, A1–A5, N1–N3 and M1–M5 are those
of the acceptance file. The harness runs them after every change to the exam and prints PASS or
FAIL for each one against the criterion's text. A failed criterion is a failure of the exam, and
is reported as such.

#### A21. What "offset set" means — *clarifies* A3

- The exam scores offset sets **exactly**: two sets are equal only if they hold the same
  `(du, dv)` offsets. There is no canonicalisation under the 12 symmetries of the hex lattice.
- On the compiled bank that is 225 distinct exact sets, and 327 once counts are included. The
  regularity measure (`results/genome/bank/REGULARITY-READING.md` §3) canonicalises, to 144
  shapes.
- So the exam tests a harder object than the one the regularity reading called compressible. A
  rule that reproduces a shape only up to rotation is scored as wrong on this field (Ark,
  2026-09-23 20:43 UTC; Johnny, 2026-09-23 20:53 UTC; Zcode, 2026-09-23 20:58 UTC).

#### A22. Conventions registered, and a report-only check — *adds*

- **Now registered as part of the exam,** from HARNESS-CONTROLS.md § "Harness conventions":
  - A predicted count below 0 is read as 0 before `log1p`.
  - Types are given to a rule as indices 0–64 in birth-id order.
  - The decode import check is static.
- **The harness refuses to run** if the first 41,349 bytes of this file (its fold-time text)
  or the acceptance file change. Amendments may only append.
- **The hub check** (acceptance file §(g)) is computed and reported. It **does not change P3**.
  The acceptance file registered it as report-only.

#### A23. Acceptance, part 2, registered before the A6 object — *adds*

`docs/plans/2026-09-23-c6-amendment-acceptance-2.md`, sha256 (LF-normalised)
`4b6610e7ed30b6aaeccf6ea33008485fc3ec31a1869b93f74c78b7248f2e97f9`.

It registers the following:

- **The weak object A6** (PR-sh). It must pass P1, P3 and P4 and lose on the budget arm alone.
- **A6-D.** A check of whether any object can do that within the size limit.
- **The role of the budget arm.** Ark (genome track, 2026-09-23 21:35 and 21:44 UTC) states
  it. R1 and the narrow band are one fact.
- **The naming** of k90 (a component count) as distinct from H18 and U18 (sets of types).
- **The scope of A1.**

The harness refuses to run if this file changes. The amendment of A17–A22 was accepted (Ark, content review, 2026-09-23
21:35 and 21:44 UTC; Zcode, owner of record of C6, mechanical check, 2026-09-23 21:43 UTC).
