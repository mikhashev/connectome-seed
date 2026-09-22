# Regularity of the type-pair table: the reading

**Written:** 2026-09-23 local time (2026-09-22 UTC), by CC (subagent), after `regularity.py`
ran. **Declaration:** `REGULARITY-DECLARATION.md`, sha256
`80e1b99c0c7a7d019978c395fa308d16c1e1b787ae6e7ecab41e0b6d8dfbabfe`, recorded 2026-09-22T19:53:03Z
before the script existed. **Numbers:** `regularity_results.json`. **Status:** descriptive. It
sets no threshold and gives no verdict on any encoding.

All numbers are on the compiled bank: 604 type pairs over a 65 × 65 grid, so 14.3 % of the grid
is filled. Every null had 2,000 draws (10,000 for sign). Where a result says "outside every
null draw", the empirical fraction is 1/2,001 (or 1/10,001), which is the smallest this
many draws can show.

## What the numbers say

### 1. Sign is almost a property of the source type, and every exception rests on one personal communication

- Knowing a pair's source type predicts its sign for **594 of 604 pairs (98.3 %)**. Shuffling
  the signs across pairs gives 66.1 % (95 % of draws between 64.4 and 68.1 %).
- The uncertainty left about the sign once the source is known is **0.057 bits**, against
  0.956 bits with no information. Under the shuffle it is 0.872 bits (0.841–0.899).
- The target type tells almost nothing: 68.5 % against the same 66 % null (1 % of shuffles do
  as well).
- **The 10 exceptions** are the minority-sign pairs of the four mixed types: R8 → Mi1, Mi4,
  Mi9, Mi15 (excitatory, where R8's other 5 are inhibitory); Am → L1, T1; C2 → L1, L2;
  C3 → L1, L2 (excitatory, where the rest are inhibitory). **All ten are `alpha_fixed` and all
  ten cite only `NernPC2018`, a personal communication.**

What this means for a rule: "one sign per cell type, plus a list of exceptions" describes the
sign column with 63 source-type signs and 10 exceptions, instead of 604 per-pair signs. The
exceptions are not spread randomly. They sit on one source of evidence.

### 2. Which pairs connect, and how strongly, has structure well beyond chance. It is not low-rank.

- **Spectrum of `L = ln(1 + synapse count)`.** The first component carries 29 % of the energy,
  against 14 % when all entries are shuffled. The top 5 carry 63 % (null 34 %). 90 % of the
  energy needs **18 components** (null 30–32) and 95 % needs **24** (null 37–39). The effective
  rank is **36.1** (null 49.1–50.8). The matrix has numerical rank 62 of 65.
- **Is it the pattern or the counts?** The declared D-S null keeps which pairs connect and
  shuffles only the counts among them. It still needs 22–24 components for 90 % (observed 18),
  with effective rank 40.5–42.8 (observed 36.1). So most of the concentration is in the
  *connection pattern*, and the counts add a smaller but consistent part on top of it.
- **The binary connection matrix `C` alone** needs 22 components for 90 % (null 31–32). Its
  effective rank is 39.8 (null 49.7–51.1).
- Every observed spectral value lies outside every null draw.

In plain words: a handful of shared factors explains a clearly larger share of the table than
chance would, but "a handful" does not reach 90 %. Getting there takes 18 of 65 dimensions. That
is structure a factorised rule could use, but it is not a table that collapses to a few numbers.

### 3. Spatial offset patterns repeat a lot as shapes and very little once counts are included

Per pair, the "pattern" is the set of `(du, dv)` column offsets it connects at.

| level | distinct patterns among 604 pairs | pairs sharing a pattern with another pair | patterns used only once |
|---|---|---|---|
| L1 shape, exact | 225 | 436 | 168 |
| L3 shape, up to the 12 hex symmetries | **144** | **504** | 100 |
| L2 shape + normalised counts (2 decimals) | 327 | 294 | 310 |
| L4 shape + counts, up to symmetry | 295 | 337 | 267 |

- **212 of 604 pairs (35 %) connect only within their own column**, at offset `(0, 0)`. Under
  the hex symmetries a further **56** are the same single nearest-neighbour offset in some
  direction. So 268 pairs (44 %) are "same column" or "one neighbour".
- About half of all pairs (286) have exactly one offset. The largest pattern has 33 offsets.
- Once the relative synapse counts are included, 310 pairs are unique. Most of the per-pair
  individuality is in the **counts across the kernel**, not in the kernel's shape.
- The raw json (605 entries, before hull filling) gives nearly the same numbers (L1 232, L3 152,
  L2 327). The hull fill does not create or destroy this structure.

### 4. The node order carries structure a sequential compressor can use. The gain is modest.

For the matrices `C`, `S`, `Q`, `K` and `N32`, under zlib and lzma, the table in flyvis node
order compresses to **6–9 % fewer bytes** for the four small-integer matrices (`C`, `S`, `Q`,
`K`), and 2–4 % fewer for the raw float counts `N32`, than the same table with rows and columns
permuted (the two permutation nulls agree to 0.1 %). Against the entry-shuffled table the saving
is **10–21 %** for the small-integer matrices (largest for sign) and 3–6 % for `N32`. The
percentages are against the null mean. Some examples:

| matrix | compressor | observed bytes | row/col permuted (95 % range) | entries shuffled (95 % range) |
|---|---|---|---|---|
| `C` connection | zlib | 427 | 456–481 | 476–497 |
| `S` sign | lzma | 544 | 580–604 | 676–700 |
| `Q` log-count bins | zlib | 730 | 761–792 | 800–826 |
| `N32` raw counts | lzma | 2,264 | 2,276–2,328 | 2,316–2,360 |

All observed sizes are below every null draw except `N32` under lzma, where 7 of 2,000
independent and 4 of 2,000 symmetric permutations were as small or smaller. The flyvis node
order groups types by name family (R, L, Lawf, Am, C, CT1, Mi, T, Tm, TmY), and that grouping
lines up with blocks in the table.

**Repeated rows.** R1–R6 have identical outgoing rows in `C` and `S`. Their incoming columns
split into pairs (R1 = R2, R4 = R5). Mi11 and Tm30 share an all-zero out-row: they are never a
source. Every other type's row and column is unique. So 59 distinct out-rows among 65 types, and
62 distinct in-columns.

## What the numbers do not say

- **They do not say an indirect encoding will beat a direct one here.** Clune et al. measured
  that crossover as performance on a task at controlled regularity levels. Nothing here is a
  task, and none of these measures is their `S`. The declaration forbids reading any of them as
  "regular enough".
- **"Beats the shuffle" is a low bar.** Almost any biological table beats an entry shuffle. The
  informative part is the *size*: 18 of 65 components for 90 %; 144 shapes for 604 pairs; a
  6–9 % compression gain from the order. The bare fact that each is outside its null is not the
  point.
- **The compressors are weak at this size.** At 4 KB the fixed overhead dominates. The
  zero-order entropy of `C`'s own 0/1 frequencies is about 313 bytes (arithmetic from the
  density, not a declared measure), and zlib does not reach it even on the real table (427).
  Compression sizes are therefore only comparable to each other. They are not estimates of
  description length.
- **The order effect partly measures the naming.** The families were named by anatomists who
  looked at morphology and connectivity. Part of what the node order "exposes" is knowledge
  already built into the names. A rule that starts from the 65 names inherits that knowledge; it
  does not discover it.
- **No stronger null was run.** A degree-preserving rewiring null would separate "a few types
  have many partners" from genuine block or factor structure. It was not declared, so it was not
  run. It is the obvious next measure.
- **Not measured: symmetry *between* types.** Whether T4a–d or T5a–d are rotated copies of one
  another as whole rows, which is the regularity a duplication-with-rotation operator would use,
  is not among the declared measures. L3 only shows that single pairs' *shapes* coincide under
  rotation.
- **The sign result is about the table, not about biology.** 98 % source-predictability says
  the json was written almost as "one sign per type". Whether real synapses obey that is not
  something this table can check. Its exceptions rest on an unpublished source.
- **The type list itself is not measured.** All of the above takes the 65 types as given. How
  many types there are, and which exist, is the part no measure here touches. It is also the
  part a growth grammar would most need to generate.
