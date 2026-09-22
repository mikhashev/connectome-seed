# Regularity of the type-pair table: declaration, written before the measurement

**Written:** 2026-09-23 local time (2026-09-22 UTC), by CC (subagent), on the grammar step's first pieces ("you do it all",
Mike, owner). **Status:** declaration. It is saved and hashed **before** `regularity.py` is
written or run; the hash and the UTC time are in `REGULARITY-DECLARATION.sha256.json`, and
`regularity.py` refuses to run if this file no longer matches that hash.

## What this is, and what it is not

This is a **descriptive** measurement of how much structure the fly's type-pair table has. It
answers a question that `literature.md` §I entry 13 (Clune, Stanley, Pennock, Ofria 2011) makes
central and that nobody has measured here: an indirect encoding (a rule that generates the
wiring) only pays when the thing it generates is regular enough, and below some regularity it
loses to writing the table down directly. At the level of the **rule**, the regularity is
already known to be maximal: the compiled bank is identical at extent 5 and extent 15, and the
node `pattern` production takes two values. At the level of the **type-pair table** (which pairs
connect, with which sign, at which offsets, with how many synapses) it is unmeasured, and that
is where all the entropy is.

**This declaration sets no threshold and no verdict.** Every measure below is reported as an
observed value next to the distribution of the same value under a declared null. No number
below is compared to a cut-off, and no outcome is labelled "regular enough" or "not regular
enough". Clune et al.'s regularity knob `S` belongs to synthetic problems they built; it has no
direct counterpart in a fixed biological table, and none of the measures below is presented as
an estimate of it.

**What was already known to the author before writing this** (so it is not mistaken for a
prediction): the table has 605 json entries and 604 compiled pairs; 2,355 compiled offset rows;
four source types (Am, C2, C3, R8) carry both signs across their outgoing entries
(`results/diagnostics/labels/partition.json`); the 65 types are in flyvis node order, which
groups them by family name (R, L, Lawf, Am, C, CT1, Mi, T, Tm, TmY). No compression ratio,
singular value, pattern count or conditional entropy had been computed by the author.

## The object

The **compiled bank** (604 type pairs, 2,355 `(source_type, target_type, du, dv)` rows, read
from `offsets.csv` rows flagged `in_json` or `hull_filled`), because that is the object the S2
design fits (`docs/plans/2026-09-20-genome-design-around-s2.md` §2). Where a measure is also
reported on the raw json (605 entries, 2,140 offset rows), it is said so beside it.

Types are indexed in connectome node order (the axis `types.csv` records). Rows are the source
type, columns the target type. Five 65 × 65 matrices:

| name | entry for pair (s, t) | 0 when no pair | serialised as |
|---|---|---|---|
| `C` | 1 if the pair exists | 0 | uint8 |
| `S` | its sign, +1 or −1 | 0 | int8 |
| `Q` | `round(2 · log2(1 + N))`, N = total n_syn of the pair summed over its compiled offset rows (half-octave bins) | 0 | uint8 |
| `K` | number of compiled offset rows of the pair | 0 | uint8 |
| `N32` | N itself | 0 | float32 |

and `L = ln(1 + N)` as float64 for the spectrum. All serialisations are row-major (C order).
The bin width of `Q` is a choice; it is fixed here and not varied after the numbers are seen.

## The measures

**(a) Compressibility.** Each of `C`, `S`, `Q`, `K`, `N32` is compressed with `zlib` (level 9)
and `lzma` (xz, preset 9). Reported: compressed bytes and the ratio compressed / raw bytes.
Three nulls, 2,000 draws each:

- **P-indep** — rows and columns permuted by two independent random permutations. Keeps the
  multiset of rows and of columns; destroys the node order. Tests whether the node order exposes
  structure a sequential compressor can use.
- **P-sym** — one random permutation applied to rows and columns alike (a relabelling of the
  types). Keeps the graph exactly; destroys only the order.
- **E-shuffle** — all 4,225 entries shuffled. Keeps only the histogram of values; destroys every
  row, column and block structure.

Per matrix, compressor and null: observed size; null mean, standard deviation, minimum, 2.5 %,
50 %, 97.5 % percentiles; the empirical fraction `(k + 1) / (n + 1)` of null draws whose size is
≤ the observed; and `z = (observed − mean) / sd`.

**(a′) Repeated rows and columns.** Number of distinct rows and distinct columns of `C`, `S` and
`Q`, and the groups of types that share an identical out-row or in-column in `C` and in `S`.
No null (a count).

**(b) Offset patterns.** For each pair, its pattern is its set of `(du, dv)` offsets, with and
without counts. Four levels:

- **L1** — the support set, exact;
- **L2** — the support set with each offset's n_syn divided by the pair's total, rounded to
  2 decimals;
- **L3** — the support set up to the 12 symmetries of the hexagonal lattice (6 rotations ×
  reflection; in axial coordinates rotation is `(u, v) → (u + v, −u)` and reflection
  `(u, v) → (v, u)`), canonical form the lexicographically smallest sorted tuple of the 12;
- **L4** — L2 up to the same 12 symmetries.

Reported for the compiled bank (604 pairs) and for the raw json offsets (605 entries): number of
distinct patterns; number of pairs whose pattern is shared with at least one other pair; number
of singleton patterns; the ten largest groups with their size and pattern; the distribution of
support size; the number of pairs whose support is `{(0, 0)}` alone. **No null** — this is a
count; the reference point is the number of pairs itself (every pair distinct).

**(c) Sign from source type.** Over the 604 compiled pairs: `H(sign)` in bits; `H(sign | source
type)` and `H(sign | target type)` (pair-weighted); the accuracy of predicting each pair's sign
by its source type's majority sign, and by its target type's; the list of mixed-sign source
types with the targets of their minority-sign pairs and those pairs' `alpha_fixed` and
references. Null: the 604 signs permuted across pairs (totals kept), 10,000 draws, giving the
distribution of `H(sign | source)`, `H(sign | target)` and both majority accuracies.

**(d) Low-rank structure.** Singular values of `L` and of `C` (all 65 reported). Per matrix:
fraction of `Σσ²` in the top 1, 2, 3, 5, 10 components; `k90` and `k95` (fewest components
reaching 90 % and 95 % of `Σσ²`); effective rank `exp(H(p))` with `p = σ / Σσ`; stable rank
`Σσ² / σ₁²`. **Row and column permutation is not used as a null here**: permuting rows and
columns multiplies by permutation matrices and leaves the singular values exactly unchanged, so
that null would be identical to the observation by construction. Two nulls instead, 2,000 draws
each:

- **D-E** — all 4,225 entries shuffled (for `L` and `C`);
- **D-S** — for `L` only: the non-zero values permuted among the observed non-zero positions.
  Keeps which pairs connect; destroys which pair has which count. Separates structure in the
  connection pattern from structure in the counts.

## Fixed in advance

- Random generator `numpy.random.default_rng(20260923)`, one stream, draws in the order the
  measures are listed above.
- 2,000 null draws per (a) and (d) cell, 10,000 for (c). Not changed after the numbers are seen.
- Nothing here is dropped after the run. A measure that turns out uninformative is reported as
  uninformative, with the reason.

## Who writes the reading

The runner (CC) writes `REGULARITY-READING.md`: what the numbers say about whether the table
has structure a compact rule could exploit, and what they do not say. The reading may describe;
it may not introduce a threshold, and it may not call the table "regular enough" for any
encoding.
