---
**Status:** DRAFT registration, **revision 2.2**, not yet run, not yet committed. Drafted by a CC
subagent, 2026-09-24 UTC (18:20; 2026-09-25 local, +07:00), on ADR-005 decision 1 (Mike, chat
2026-09-24 17:53 UTC). Revised by a CC subagent on 2026-09-24 UTC after the reviews of Ark, Johnny
and Zcode (DPC Research chat, 18:26-18:35 UTC), again after CC's logic check (negative `Δ`), and
again after the second reviews of Ark, Zcode and Johnny (18:53-18:58 UTC); every change is listed
in §12. **Dated by its UTC
day**, as the [glossary's date-time convention](../../GLOSSARY.md) requires; the request named it
`2026-09-25-…`.
**No value of the column test exists anywhere at the time this file is written.** No per-column
table was built and no per-column existence set, agreement, containment, overlap or curve point was
computed. No synthetic world was run either: §3.8 specifies them for the script. What was read to
design it: the code of `flywire_bank_builder.py`, the headers and the *structure* of
`column_assignment.csv.gz` (which columns exist, which of the 30 types each column holds, §2.3),
the committed aggregate files `flywire_sensitivity/RESULT.md` and
`connectome-seed-data/FlyWire/derived/bank.meta.json` (counts only, including `neurons_per_type`),
and the flyvis 1.2.0 package (§8). No connectivity file was opened.
Every item that is a choice is listed in §10, "Decisions for Mike", with the reviewers' unanimous
recommendation. Until Mike answers them this file is a draft; the recommended option is written
into the body so the draft is complete as it stands.
---

# Registration: the column test on FlyWire (ADR-005 decision 1)

## 0. Question, name, and what it is not

**Name.** *The column test: a lower bound on how much agreement our processing produces.*

**Question.** The FlyWire-30 bank and flyvis-30 agree strongly: 159 of the 165 FlyWire-30 type
pairs lie inside flyvis-30, a containment of **96.4 %**
([ADR-005](../decisions/005-backward-before-forward.md), agreed point 3;
`results/genome/c6/checks/flywire_sensitivity/RESULT.md`). Both are averages. How does that
agreement depend on how many columns of the same fly are averaged? If it is about as high for one
un-averaged column as for the full average, averaging adds little. If it rises steeply with the
number of columns averaged, the averaging step is producing agreement that the raw units do not
have. If it *falls*, the averaging step is removing agreement that single columns have, and the
96.4 % understates it (§4, branch (c)).

**Why it is a lower bound (ADR-005 agreed point 4, Zcode).** Between reconstruction and bank our
processing has these steps: the **column mean** (on both sides: FlyWire-30 is our column mean,
flyvis-30 is the flyvis authors' column mean of each volume), the **pruning** of means below one
synapse (FlyWire side; it acts on the mean), the **max merge** of two volumes (flyvis only), and
**hand edits** (flyvis only). This test removes one step and a half from **one side only**: the
FlyWire column mean, and with it the mean-below-1 pruning, which acts on the mean and so cannot be
separated from it (§2.5). flyvis's own column mean, the max merge and the hand edits stay in
flyvis-30 untouched (Part A, §8, finds no way to remove either the merge or flyvis's averaging). So
the test can show *at least* this much order coming from our arithmetic; it cannot show *all* of
it (§6).
**Assumption, recorded, not shown:** "cannot overestimate" holds only if the steps the test leaves
in place do not *lower* agreement. A max merge adds pairs to flyvis-30 and cannot remove any, so it
can only raise containment of a FlyWire object inside flyvis-30; flyvis's column mean, if it acts
as ours does (§6), also points upward; the hand edits' direction is unknown
([where our bank comes from, §2.2](../notes/2026-09-23-where-our-bank-comes-from.md)).

**What it is not.** It is **not a proxy for the overlap between banks**, and it must not be
reported as one (ADR-005 agreed point 4, Johnny's objection). A column-to-column comparison is
within one fly and one pipeline; the bank-to-bank 96.4 % is between two flies (at least three),
two methods and two pipelines. The test says how much the FlyWire averaging step alone can move an
agreement number. It says nothing on its own about how similar two brains are.

**What it serves.** Question (ii), transfer between the two brains, is paused until this returns
(ADR-005 decision 2). The test passes ADR-005's admission rule because it closes one number (ii)
depends on: whether 96.4 % can be used as (ii)'s reference level as it stands, or must be
normalised against what averaging alone produces (§5).

## 1. Sources, licence, and what may be committed

Same sources as the FlyWire registration
([2026-09-24-flywire-bf-p3-registration.md §1](2026-09-24-flywire-bf-p3-registration.md)):

| File | Licence | Used for |
|---|---|---|
| `proofread_connections_783.feather` (Zenodo 10676866) | CC-BY-4.0 | neuron-to-neuron synapse counts |
| `column_assignment.csv.gz` (Codex, live file, downloaded 2026-09-23 UTC, sha256 `bdf4ce7f…f0f6`, 462,838 bytes) | **CC BY-NC 4.0, not for the repository** | type and hex column `(p, q)` per neuron |
| `derived/flywire_ol_right_30_offsets.csv` + `bank.meta.json` (our registered build, sha256 `25c5ff1d…42eb`) | inherits NC | the averaged FlyWire-30 bank, for the machine check (§3.6), the curve's anchor (§3.2) and statistic S3 |
| `results/genome/bank/offsets.csv` (committed) | flyvis json, as already committed | flyvis-30: rows with `provenance == "in_json"`, both ends among the 30 types (the same cut as `flywire_sensitivity.py`, 228 pairs) |

**Licence handling (fixed now).** Per-column tables encode column positions from the NC file, so:

- **Stay outside the repository**, under `connectome-seed-data/FlyWire/derived/column_test/`:
  the per-column offset rows, the per-column existence sets, the list of included columns, the
  sampled column lists of the curve, and any file keyed by column id or root id.
- **Committed:** the script, and aggregate statistics only: counts, quantiles, curve summaries,
  labels, the synthetic-world results, and the manifest with input hashes (§7). No row of the
  committed output may identify a column, a neuron or a per-column value.

## 2. The object: per-column type-pair tables

### 2.1 Types and neurons, identical to the bank

The same 30 types as the registered bank (FlyWire registration §2), and the same neurons: rows of
`column_assignment.csv.gz` with `hemisphere == "right"` and `type` among the 30, type taken from
that file, a root id with two right-hemisphere rows stops the run (builder §3a.1). The script
**imports** `FLYWIRE_NAME_OF`, `SYNAPSE_THRESHOLD` (2), `MEAN_PRUNE_BELOW` (1.0) and
`HEX_NEIGHBOURS` from `flywire_bank_builder.py` rather than copying them, and refuses unless that
file's sha256 equals `b109fd17d0d1cf88ddb94343f2b6234c68eeb7eeccab3a6d58af4ce3c20b0750`, the
`builder_sha256` recorded in `bank.meta.json` (checked equal at drafting).

Connections exactly as the bank: synapses summed over neuropil rows per (pre, post) root pair, both
ends among these neurons, kept at `>= SYNAPSE_THRESHOLD` synapses (builder lines 224-231).

### 2.2 What a column is

A **column** is one distinct `(p, q)` among the right-hemisphere rows of `column_assignment.csv.gz`
(the same key the builder uses, `pos[rid] = (p, q)`, builder line 212). Read at drafting (structure
only): 796 distinct `(p, q)`; `column_id` and `(p, q)` are one-to-one; **no column holds two
neurons of the same type** among the 30. So a column holds at most one neuron of each type, and the
number of type-`t` neurons `N_t` equals the number of columns holding type `t` (`bank.meta.json`,
`neurons_per_type`: from 654 for R8 to 796 for Mi1).

### 2.3 Which columns are included in the single-column statistics (the exclusion rule, fixed now)

Read at drafting, structure only (no connectivity): of the 796 right-hemisphere columns, **306**
hold a neuron of every one of the 30 types; **294** of those also have all six axial neighbours
`(±1, 0), (0, ±1), (1, −1), (−1, 1)` present among the 796 (the builder's own `HEX_NEIGHBOURS`
and interior definition, builder lines 194 and 235). Coverage is uneven: 612 columns hold at
least 28 types; the most often missing are R8 (142 columns) and R7 (137). These counts were
re-derived independently by Ark in review (796 / 306 / 294 / 612 / 142 / 137, and 0 columns with
a repeated type).

**Rule (recommended, D1):** a column is **included** iff it holds a neuron of all 30 types **and**
all six axial neighbours exist. That is 294 columns. Reason: (i) with all 30 target types present,
every column's existence set lives in the same 900-pair universe, so containments are comparable
across columns without a per-column universe; (ii) with all neighbours present, inputs at offset 1
(where 245 of the bank's 393 rows sit, `flywire_sensitivity/RESULT.md`) are not cut off by the
edge of the eye. Requiring the neighbours to be *complete* as well was considered and rejected: it
leaves 16 columns.

**Where the rule applies.** The inclusion rule governs the *single-column* statistics S1, S2, S3
and the primary S4 (§3.3-§3.5). It does **not** govern the per-column tables themselves (built for
all 796, §2.4), the machine check (§3.6), or the dose-response curve (§3.2), which draws its
samples from all 796 columns so that its last point is the bank itself.

**Stop rule:** if fewer than 100 columns are included, S1-S4 are not computed; the curve and its
reading (§3.2, §4) still are, since they do not depend on the inclusion rule.

**What the rule costs, stated now:** the 294 included columns are not a random sample. Columns
missing a type may be at the margin of the eye or in less completely proofread regions; S1-S4
describe the included columns only (§6).

### 2.4 The per-column table: target-anchored, the exact summand of the bank

`x_c` is defined for **every** column `c` of the 796, not only the included ones: the machine
check (§3.6) and the curve's anchor (§3.2) need all of them; the statistics then use subsets
(§2.3). For a column `c`, the type-`t` neuron `j` in `c` (if `c` holds one), and a type-`s` neuron
`i` at column `(p_c − du, q_c − dv)`, in any of the 796 columns:

```
x_c(s, t, du, dv) = syn(i -> j)   if that neuron pair is kept (>= 2 synapses), else 0
```

If `c` holds no type-`t` neuron, `x_c(·, t, ·, ·)` is 0 for every entry, and `c` contributes
nothing to type `t`'s denominator (§3.2).

**Why target-anchored.** The registered bank's value for `(s, t, du, dv)` is
`sum over j of type t of x(j) / N_t` (builder lines 253-263: the sum runs over post neurons and
divides by `N_t`, the number of column-assigned neurons of type `t`). Since each column holds at
most one type-`t` neuron, **the bank is exactly the mean over target columns of `x_c`**. The
per-column table is therefore the summand of the bank's average, with nothing else changed. A
source-anchored table would not have this identity. The machine check (§3.6) proves it.

**Offset support (recommended, D4): any offset.** The bank has no offset limit; its only filter is
the mean-below-1 pruning. The per-column table keeps every offset for the same reason. Rows by
`max(|du|, |dv|)` (0, 1, 2, 3 or more) are reported as aggregate counts so a reader can see how
much of the per-column existence rests on far offsets.

### 2.5 When a type pair exists in one column

**`(s, t)` exists in column `c`** iff `x_c(s, t, du, dv) > 0` for at least one `(du, dv)`, with the
self offset `s == t, (du, dv) == (0, 0)` excluded (the bank's autapse rule, builder line 265;
structurally empty here, since no column holds two same-type neurons). Call the set `E_c`.

This is the bank's own existence rule (FlyWire registration §3.6: "a type pair exists iff at least
one offset row survives") applied to one column. **The pruning step is applied and is a no-op**
at the column level: the "mean" over one target neuron is `x_c` itself, which is either 0 or at
least 2, so `mean < 1` removes nothing. This is not a design choice; it is what the bank's own
rule does to one column. It is also the heart of what the test measures: in the bank a row
survives only if the synapses at one offset, summed over all ~650-800 target neurons, reach `N_t`;
in one column a single kept neuron pair suffices.

**Consequence known before any data (structural, not a measurement):** every bank pair lies in
at least one column's set, taken over all 796 columns, because a surviving bank row has a positive
sum. The bank is therefore contained in the union of the per-column sets. Nothing forces it to be
contained in any one column's set, or any one column's set to be contained in the bank.

## 3. Statistics

Universe: the 900 ordered pairs of the 30 types. Three kinds of set are fixed before the run:
**F** = flyvis-30 (228 pairs), **B** = the registered FlyWire-30 bank (165 pairs), and `E_c` for
each column. For any set `A` in the universe, its **containment in F** is `C(A) = |A ∩ F| / |A|`
(undefined for an empty `A`; such cases are counted and printed, and left out of every quantile).

### 3.1 Reference numbers, already public (arithmetic on committed counts, not new measurements)

From `flywire_sensitivity/RESULT.md` (165 pairs in B, 228 in F, 69 of F missing from B, 6 of B
missing from F):

| name | value | from |
|---|---|---|
| `R_in` = containment of B in F, \|B∩F\|/\|B\| | **159/165 = 0.9636** (the 96.4 %) | ADR-005 point 3 |
| `R_cov` = coverage of F by B, \|B∩F\|/\|F\| | 159/228 = 0.6974 | same counts |
| `R_jac` = Jaccard of B and F | 159/234 = 0.6795 | same counts |
| chance level of `R_in` for a random set of any size in 900 | 228/900 = 0.2533 | hypergeometric mean |

### 3.2 The dose-response curve (primary)

**The average of a sample, with the builder's own rule.** For a set `K` of columns drawn from the
796, the **sample average** is built exactly as the builder builds the bank, restricted to `K`:

```
n_K(t)            = number of columns in K holding a type-t neuron   (as S4 does)
mean_K(s,t,du,dv) = sum over c in K of x_c(s, t, du, dv) / n_K(t)     (only where n_K(t) >= 1)
```

then the autapse row `s == t, (du, dv) == (0, 0)` is dropped, a row with `mean_K < 1` is dropped
(the pruning after division, `MEAN_PRUNE_BELOW` imported), and `(s, t)` exists in the sample
average iff at least one row survives. Call the resulting pair set `A_K`. A target type absent from
`K` (`n_K(t) = 0`) contributes no row. Two structural facts follow, without data:

- **`K` = all 796 columns reproduces the bank exactly** (`n_K(t) = N_t`), so `A_796 = B` and
  `C(A_796) = R_in = 159/165`. This is the §3.6 identity; the script asserts it a second time,
  on the curve's own code path, and stops if it fails ("CURVE ANCHOR FAILED").
- **`K` = one column gives `A_K = E_c`**, since the pruning is a no-op on one column (§2.5).

**The grid of `k`, and the samples.** `k = |K|` runs over **1, 2, 4, 8, 16, 32, 64, 128, 256,
512, 796** (11 values). Columns are indexed 0-795 in ascending `(p, q)` order.

- `k = 1`: every one of the 796 columns once (exhaustive; no seeds).
- `k = 2 … 512`: **50 samples** per `k`, sample `j` (0-49) drawn without replacement by
  `numpy.random.default_rng(1000 * k + j).choice(796, size=k, replace=False)`.
- `k = 796`: the single full set.

**Reported per `k`:** number of samples, number with empty `A_K`, and the 5th, 25th, 50th, 75th and
95th percentiles and the mean of `C(A_K)` and of `|A_K|` (`numpy.percentile`, default linear
interpolation, fixed now), and the same for the chance-corrected form `(C − 0.2533)/(1 − 0.2533)`.
The table and a plot of the median with the 5-95 band against `log2 k` are the curve.

**The primary statistic.**

```
Δ = C(A_796) − median over the 796 columns (non-empty E_c) of C(E_c)
  = R_in     − median_c C(E_c)
```

the rise of containment from one column to the full average. **`Δ` can be negative:** if single
columns carry sporadic pairs that lie inside F (for example among the 69 weak flyvis-only pairs),
those pairs raise a single column's containment and the averaging prunes them, so the median
single column can sit above `R_in`. It is read against the calibration of §3.8, never against a
threshold chosen by eye (§4). The intermediate points of the curve are
description: they show *where* the rise happens; they take no part in the label.

**`Δ` has no sampling error (Ark, Zcode; revision 2.2).** Both of its ends are exact: `k = 1` is
taken over all 796 columns, each once, and `k = 796` is the bank itself. No seed enters `Δ`, so the
verdict does not depend on seeds. Only the 50-sample intermediate points of the curve depend on
seeds, and they are description. (The synthetic worlds of §3.8 do depend on their seeds; they fix
the scale `Δ` is read on, not `Δ`.)

**Why the 796 and not the 294 as the curve's population (Zcode's anchor).** Only on the 796 does
the last point coincide with the registered bank by construction, so the curve ends at exactly the
number under question, 96.4 %, and its code path is checked against the bank. **Zcode's
falsifier:** if averaging the 294 included columns with the builder rule reproduced the bank, the
796 anchor would be unnecessary. The part of this that can be settled without connectivity: every
`N_t` is between 654 and 796 (`bank.meta.json`), while `n_K(t) = 294` for every type on the 294, so
the 294-average divides every row by a different number than the bank does; it can reproduce the
bank's 393 values only if the excluded 502 columns' sums happen to be in exactly the same
proportion, which only connectivity can decide. So the check is **left to the script**, which
prints, without any role in the verdict: whether the 294-average has the bank's 393 rows with
equal `n_syn` to `1e-12`, and, separately, its pair set's size, `|A_294 ∩ B|` and `C(A_294)`. The
796 anchor is kept either way: it costs nothing, and it is the only population on which the anchor
is guaranteed.

### 3.3 S1 (secondary: "the single column"): each included column inside flyvis-30

`C(E_c)` for each of the **294** included columns (§2.3). This is the single-column picture on a
common universe: the same flyvis-30, the same FlyWire fly, the same types, threshold and existence
rule, with **one thing changed**, the averaged bank B replaced by one un-averaged column holding
all 30 types. Reported: number of columns, min, 5th, 25th, 50th, 75th, 95th percentile, max, mean,
and `|E_c|` with the same summary. A column with `|E_c| = 0` is counted, printed, and left out.
Also printed: `Δ_294 = R_in − median over the 294 of C(E_c)`, located on the §3.8 calibration like
`Δ` and labelled by the same rule; **this label decides nothing** and is printed beside the primary
label so a reader sees whether columns missing some types move the reading.

**Density.** Under a density-matched null (a uniformly random set of the same size as `E_c`), the
expected `C(E_c)` is `|F|/900 = 0.2533` **whatever the size of `E_c`**. The chance level is therefore
the same for every column, every sample average and the bank's own `R_in`. So raw values are
compared with `R_in` directly; the chance-corrected form `(C − 0.2533)/(1 − 0.2533)` is a fixed
monotone transform of both sides and changes no reading. It is printed next to each quantile
(`R_in` becomes 0.9513).

### 3.4 S2 (secondary): single columns against each other, within the fly

For every unordered pair of included columns (294 columns give 43,071 pairs): Jaccard, and the
overlap coefficient `|E_c ∩ E_c'| / min(|E_c|, |E_c'|)`. Reported with the same quantiles. Each is
also printed chance-corrected against its own density-matched expectation (Jaccard and overlap of
two independent uniform sets of sizes `a`, `b` in 900; expected intersection `ab/900`), because
here, unlike S1, chance depends on the sizes. Printed next to them: `R_in` (overlap coefficient of
B and F, since B is the smaller) and `R_jac`.

### 3.5 S3 and S4 (secondary)

**S3, single columns against their own averaged bank:** `|E_c ∩ B| / |E_c|` (how much of one
column survives averaging) and `|E_c ∩ B| / |B|` (how much of the average one column already
holds), over the 294. Quantiles as above. No reference number: this is description of what the
column mean with its pruning removes and adds within one fly.

**S4, split-half averages (recommended, D6), on the same population as S1.** Twenty half-splits,
`numpy.random.default_rng(seed)` for seeds 0-19, each a permutation cut into two halves.

- **S4-294 (the one §5 uses):** splits of the **294 included columns** into halves of 147. Each half
  is averaged with the sample-average rule of §3.2 (`n_K(t) = 147` for every type).
- **S4-796 (printed beside it):** splits of all 796 columns into halves of 398, averaged the same
  way (`n_K(t)` varies by type).

Reported for each: overlap coefficient and Jaccard between the two halves, and `C` of each half
inside F, as quantiles over the 20 splits. S4-294 is the normaliser §5(b) names, so it is taken on
S1's population; S4-796 lets a reader compare with the curve at `k = 398`. Description only; it
takes no part in the verdict.

**Null considered and not used (D5):** a degree-preserving shuffle per column. It keeps each type's
in- and out-degree, which is the type-level order this test is about, so it would call most of
that order "chance". The density-matched null answers the question asked here, "is this agreement
more than two sets of this size would share", and is exact (no seeds).

### 3.6 Machine check (before any statistic is computed)

From the per-column tables over **all 796 columns**: `sum over c of x_c(s, t, du, dv) / N_t`,
pruned below 1, with the autapse rule, must reproduce the registered bank exactly: the same 393
rows, each `n_syn` equal to the bank's to `1e-12`, the same 165 pairs, and the offsets file's
sha256 `25c5ff1d8ac9dc29e663d1383754c48ef23efae12b65714c66103cd4384d42eb` must be the one read. If
it fails, the script stops and prints "MACHINE CHECK FAILED" and nothing else. Passing proves that
the per-column tables differ from the bank by the averaging step only.

### 3.7 The Q3/P95 label (secondary, non-monotonic, decides nothing)

The first draft read S1 by `Q3` and `P95` of the column distribution: (a) if `R_in <= Q3`, (b) if
`R_in > P95`, unclear between. Exactly: **(a) iff at least 25 % of columns have `C_c >= R_in`;
(b) iff at most 5 % of columns have `C_c >= R_in`.** Columns equal to B sit exactly at `R_in`
and count as `>=`, so they decide both borders.

Under thinning (every column is B with each pair dropped with probability `p`), a column has
`C_c >= R_in` when it loses at least one of the six non-F pairs of B, or loses nothing; the share
of such columns is `1 − (1 − p)^6 + (1 − p)^165`. Its minimum over `p` is **0.1496, at
`p` = 2.06 %**, so the share never falls to 5 % and **(b) is unreachable under thinning at any
`p`**. Ark's simulation (4000 repeats per rate; confirmed by Zcode and Johnny, 2026-09-24
18:53-18:58 UTC) gives the labels:

| `p` | Q3/P95 label under thinning |
|---|---|
| 0.05-0.5 % | (a) in 100 % of seeds |
| 1 % | on the edge: (a) 0.44, unclear 0.56 across seeds |
| 2 % | unclear in 100 % |
| 5 % | (a) in 83 % |
| 10 % | (a) in 100 % |

The borders lie near `p` ≈ 1.05 % and 4.7 %: the sequence is (a) → unclear → (a), with no (b). On
the uniform-extras worlds of §3.8 the rule gives (b) in 100 % of seeds at `r` = 5, 10, 20 and 40 %.
The rule's defects are therefore: (i) under thinning it can never say (b); (ii) it says "unclear"
where there is no effect at all (at `p` = 2 %, `Δ` = +0.0007). It is also **non-monotonic** in `p`
(two label changes). (An earlier table in review, with (b) at `p` = 0.2 %, is withdrawn; its
author corrected it.) The rule measures how often a column happens to lose FlyWire-specific pairs,
or none, not how well columns agree.

It is **kept as a secondary label only**, printed for S1 (on the 294) and S2, with the words
"secondary, non-monotonic in the thinning rate (§3.7); decides nothing". Its **switching points**
are printed from the thinning worlds of §3.8: the label of every thinning world, so a reader sees
at which `p` it changes.

### 3.8 Calibration and two-world check (synthetic, before the real curve; lesson b)

The reading of `Δ` (§4) is fixed by synthetic worlds that the script builds **before** it computes
any real curve point or S1-S4 value. The worlds use only B and F (bank-level sets the script
already holds) and no per-column data.

**The synthetic column and its average.** A synthetic world is **796** synthetic columns, each a
subset of the **full 900-cell grid** (every column holds all 30 types; see "type coverage" below).
A cell present in a column carries the value 2 (`SYNAPSE_THRESHOLD`, the smallest a kept neuron
pair can carry) at a single offset. A sample `K` of synthetic columns is averaged with the rule of
§3.2: the mean over `K` of the cell's value (the denominator is `|K|` for every type), pruned below
1; so a cell survives iff it is present in at least half of `K`. The curve of a world uses the
**same `k` grid and the same sample indices and seeds** as the real curve (§3.2), and its `Δ` is
computed the same way. Why the value 2: it is the most pruning-prone value a real entry can have.
`Δ` is insensitive to it in the ranges used, because `Δ` reads only the single column (where no
pruning acts) and the full average: at the full average, under thinning, B cells are present in at
least 90 % of columns and survive for any value ≥ 2; under extras, a non-B cell is present in at
most about 9 % of columns (below) and is pruned for any value below about 11. The intermediate
points of the synthetic curves do depend on the value (at `k = 2` one presence in two survives);
they are description only. **The value 2 is the definition, not an idealisation (Ark, revision
2.2):** every real entry is at least 2, and a non-bank cell has a per-type mean below 1, so it is
present in fewer than half the columns; a world of value-2 cells present in fewer than half the
columns is exactly that condition.

**Thinning worlds (should read flat).** Each column is B with each of its 165 pairs dropped
independently with probability `p` ∈ {0.05 %, 0.1 %, 0.2 %, 0.5 %, 1 %, 2 %, 5 %, 10 %}. Averaging
adds nothing here by construction: every column is a thinned copy of the average.

**Uniform-extras worlds (should rise).** Each column is B plus each of the 735 non-B cells added
independently with probability `q = r · 165 / 735`, so that a column carries on average `r` extra
pairs relative to `|B|`, for `r` ∈ {5 %, 10 %, 20 %, 40 %} (`q` = 1.12 %, 2.24 %, 4.49 %, 8.98 %).
Extras are uniform over the non-B cells, so a fraction 69/735 of them lands inside F (the cells of F
missing from B), as uniform noise would. Averaging with the mean≥1 pruning removes these sporadic
extras, so the curve rises. The world with `r = 0` is every column equal to B; its `Δ = 0` exactly
and needs no run.

**In-F extras worlds (should fall; revision 2.1, CC).** Each column is B plus each of the **69
cells of F \ B** (the flyvis-only pairs) added independently with probability `q_F`, and no other
cell. The 69 flyvis-only pairs are weak pairs, so sporadic pairs in a single FlyWire column may sit
exactly there rather than uniformly; such extras *raise* a single column's containment in F, and
averaging prunes them, so these worlds give `Δ < 0`. Rates: `q_F` ∈ {5 %, 10 %, 20 %, 30 %, 40 %},
that is `r_F = q_F · 69 / 165` ∈ {2.1 %, 4.2 %, 8.4 %, 12.5 %, 16.7 %} extra pairs relative to
`|B|`. **Why not the same `r` = 5-40 % as the uniform family:** with only 69 cells to draw from,
`r` = 40 % of `|B|` (66 pairs) would need `q_F` = 0.96, and any `r` above about 20.9 % needs
`q_F` ≥ 0.5. The extras would then be present in half the columns or more, would survive the
mean≥1 pruning (value 2, above), stop being sporadic, and turn `Δ` positive again. The cap
`q_F <= 0.40` keeps every in-F extra below half the columns at the full average by a wide margin
(sampling s.d. of the fraction over 796 columns about 0.017; the margin is 5.8σ, checked by the
reviewers, revision 2.2).

**Calibration.** Each family gets its own calibration worlds, on seeds used nowhere else
(`numpy.random.default_rng`; `i` is the index of the rate in its list, `j` a repeat):

- **Uniform extras:** one world per `r`, seed `250 + i`; its `Δ_cal(r)`. With `Δ_cal(0) = 0` these
  five points are the uniform calibration curve. The script requires `Δ_cal` strictly increasing in
  `r`, otherwise it stops ("CALIBRATION NOT MONOTONE"). **`k*`**, the equivalent extra-pair rate, is
  the linear interpolation of `r` against `Δ_cal(r)` on those five points, printed as "< 0 %" below
  0 and "> 40 %" above `Δ_cal(40 %)`. `k*` is defined on the uniform family only.
- **In-F extras:** one world per `q_F`, seed `400 + i`; its `Δ_calF(r_F)`. With `Δ_calF(0) = 0`
  these six points are the in-F calibration curve. The script requires `Δ_calF` strictly decreasing
  in `r_F`, otherwise it stops ("CALIBRATION NOT MONOTONE"). **`k*_F`** is the linear interpolation
  of `r_F` against `Δ_calF(r_F)` on those six points, printed as "> 16.7 %" below `Δ_calF(16.7 %)`.
  `k*_F` is defined on the in-F family only, and is printed only under label (c).
- **Thinning, the lower envelope `L`:** five calibration worlds per `p`, seeds `150 + 10 i + j`,
  `j` = 0-4 (40 worlds), and the eight thinning validation worlds of the two-world check below
  (one per `p`, seed `100 + i`). **`L` = the minimum of `Δ` over all 48 thinning worlds** (40 + 8;
  revision 2.2, Ark, accepted by Zcode), with nothing subtracted. `L` is the most negative rise
  that pure thinning, with no averaging effect, produced on these seeds. It is the floor below
  which a real `Δ` is read as (c) (§4). Since every thinning world enters `L`, **no thinning world
  can read (c), by construction.** Ark's measured band: `L` lies in about [−0.0014, 0];
  `P(L < −0.002) = 0` in 20,000 draws; the in-F worlds at `q_F` = 30 % and 40 % give
  `Δ` = −0.0041 and −0.0051, a two-to-three-fold margin below `L`.

**Seeds, all disjoint (revision 2.2).** World-generating seeds: thinning validation 100-107;
thinning calibration 150-154, 160-164, …, 220-224 (`150 + 10 i + j`, `i` = 0-7, `j` = 0-4);
uniform-extras calibration 250-253; uniform-extras validation 305, 310, 320, 330, 340; in-F
calibration 400-404; in-F validation 530, 540. The largest thinning calibration seed is 224, below
250, so no two of these ranges meet (revision 2.1 had the uniform calibration at 200-203, inside
the thinning range 200-204 at `i` = 5). Elsewhere: S4 splits use seeds 0-19 (§3.5), and the curve's
samples use `1000 k + j` (2000-2049 up to 512000-512049, §3.2), which every synthetic world reuses
on purpose so that its curve is sampled exactly as the real one. The script asserts that all
world-generating seeds are unique and distinct from 0-19 and from the curve's sample seeds, and
stops otherwise.

**Two-world check (independent seeds; accepted by CC).** Fresh worlds, built with seeds that no
calibration used, are read by the §4 rule exactly as the real data will be. (The eight thinning
validation worlds also enter `L`, above; so for them the check tests the upper side only.)

- every thinning world (one per `p`, seed `100 + i`) must read **(a)**, that is, not (b) and not
  unclear; (c) is impossible for them by construction (revision 2.2);
- uniform-extras worlds at `r` = 30 % and 40 % (seeds 330, 340) must read **(b)**;
- the uniform-extras world at `r` = 20 % (seed 320) must **not** read (a);
- the uniform-extras world at `r` = 10 % (seed 310) must read **unclear**;
- the uniform-extras world at `r` = 5 % (seed 305) must **not** read (b);
- in-F extras worlds at `q_F` = 30 % and 40 % (`r_F` = 12.5 %, 16.7 %; seeds 530, 540) must read
  **(c)**.

If any requirement fails, the script stops before it computes any real curve point or S1-S4 value:
the rule cannot see all three worlds and must be revised under a new draft. **Why not "the 20 %
world must read (b)":** a world built at exactly the (b) cut lands on either side of it by sampling
noise alone, about half the time each, so that requirement would stop a correct rule at random; the
requirement is therefore placed at 30 % and 40 %, clear of the cut, and the worlds that sit on a cut
(5 %, 20 %) are only required not to cross to the far label. **Why `L` is taken over all 48
thinning worlds (revision 2.2):** with `L` over the 40 calibration worlds only, a validation
thinning world could dip just below it and read (c); revision 2.1 therefore allowed "(a) or (c)".
Taking `L` over every thinning world removes that case, so the requirement is simply (a). **Why the
(c) requirement is at `q_F` = 30 % and 40 %** and not at the "30 % and 40 % of `|B|`" first asked for: those rates cannot
be built as sporadic in-F extras (above); 30 % and 40 % of the 69 cells are the two highest rates
that can, and the ones farthest below `L`. The in-F rate cap and this placement are **approved by
CC**.

**Type coverage: what the worlds do not reproduce.** Every synthetic column holds all 30 types and
lives in the full 900-cell grid, so in a synthetic sample `n_K(t) = |K|` for every type. Real
columns do not: 490 of the 796 lack at least one type, so a real single column has no pairs into its
missing target types, and real sample averages divide by `n_K(t) ≤ |K|`. The worlds are independent
columns; real columns are also spatially correlated. Neither difference is modelled. The first
enters the primary `Δ` through its `k = 1` median (taken over all 796); `Δ_294` (§3.3), whose
`k = 1` end uses only complete columns, is printed beside it so a reader can see its size. Each
world also has only one kind of departure from B; real columns may thin and add extras of both
kinds at once (§6, §3.9).

**Back-of-envelope, not a result.** From expected values only (no simulation):

- uniform extras: single-column containment about `(159 + 0.094 e)/(165 + e)` with `e = 1.65 r`
  extra pairs (`r` in %), which puts `Δ_cal` near +0.04, +0.08, +0.15 and +0.25 at `r` = 5, 10, 20,
  40 %;
- in-F extras: single-column containment `(159 + e)/(165 + e)` with `e ≈ 69 q_F`, which puts
  `Δ_calF` near −0.001, −0.002, −0.003, −0.004 and −0.005 at `q_F` = 5, 10, 20, 30, 40 %. The
  largest fall any in-F world can show is −0.011 (all 69 cells in every column, `228/234`), and
  that world is not sporadic;
- thinning: while more than half the columns lose no pair (`p` up to about 0.4 %), the median column
  equals B and `Δ = 0` exactly; above that, the median column has lost only pairs inside F and
  `Δ` is a small positive number (a few thousandths); at `p` = 10 % about 47 % of columns lose one of
  B's six non-F pairs and sit above `R_in`, so on some seeds the median crosses to just above
  `R_in` and `Δ` is slightly negative, of order −0.001. `L` is therefore expected at or a little
  below 0.

**Reviewers' check of these estimates (revision 2.2).** The reviewers' checks agree with Ark's
simulation: uniform extras give `Δ_cal` = +0.039, +0.079, +0.145 and +0.248 at `r` = 5, 10, 20,
40 %; in-F extras give `Δ_calF` from −0.0007 to −0.0051; `L` lies in about [−0.0014, 0] (above);
the ceiling `q_F <= 0.40` holds with a 5.8σ margin.

These numbers only show that the design is not empty; the script's values replace them. They also
show that **(c) reads effects of a few thousandths**: the whole in-F calibration spans about 0.005,
against about 0.25 for the uniform family (§6).

### 3.9 Where single columns' extra pairs lie (description; decides nothing; revision 2.1)

For each column with at least one pair outside B, the **in-F share of its extras**:

```
X_c = |E_c ∩ (F \ B)| / |E_c \ B|
```

the fraction of the column's non-B pairs that lie among the 69 flyvis-only pairs. Printed beside the
verdict as quantiles (as in §3.3) over the 796 columns and over the 294, with the number of
columns having no non-B pair, together with the quantiles of `|E_c \ B|` and of `|B \ E_c|` (extras
and losses per column). Reference points, printed verbatim: **uniform extras give 69/735 =
0.0939**, **in-F extras give 1**. This number shows which calibration family the real columns
resemble, and makes visible a mix in which the two kinds of extras cancel in `Δ` (§6). **It decides
nothing**; no label is read from it. The median of `X_c` over the 796 also enters the diagnostic
`k*_obs`, and the medians of `|E_c \ B|` and `|B \ E_c|` are printed on the verdict line (§4).

## 4. Reading rule (every branch named before data)

The label is read from the primary statistic `Δ` (§3.2), against two calibrations of §3.8: the
thinning lower envelope `L` (the minimum `Δ` over all 48 thinning worlds of §3.8, calibration and
validation, nothing subtracted) and the uniform-extras calibration, on which `Δ` is located as the equivalent
extra-pair rate `k*`. Under (c) its size is located on the in-F calibration as `k*_F`. The cut
points below are **fixed now, before any data**, and are not revised after the real curve is seen.
The four branches are exhaustive and exclusive: (c) is tested first, and (a), unclear and (b) are
read only when `Δ >= L`.

| label | condition | reading |
|---|---|---|
| **(c) averaging removes agreement** | `Δ < L` | Single FlyWire columns sit closer to flyvis-30 than the averaged bank does: the median column's containment is above anything pure thinning produced. The FlyWire column mean (with its pruning) removes pairs that flyvis-30 has, and the 96.4 % **understates** the agreement on the FlyWire side. The averaging is not what produces the overlap. The size is printed as `k*_F`, the in-F extra-pair rate that gives the same fall; no cut is read from it. |
| **(a) averaging adds little** | `Δ >= L` **and** `k* <= 5 %` (equivalently `L <= Δ <= Δ_cal(5 %)`) | Going from one column to the full average raises containment in flyvis-30 by no more than removing about one extra pair in twenty would, and does not lower it below what thinning alone gives. The 96.4 % is close to what one column already shows; the FlyWire column mean neither creates nor hides it. |
| **unclear** | `Δ >= L` and `5 % < k* < 20 %` | The rise is larger than a small amount of per-column noise would give, but not large enough to call the 96.4 % a product of averaging. |
| **(b) averaging manufactures agreement** | `Δ >= L` and `k* >= 20 %` (equivalently `Δ >= Δ_cal(20 %)`) | The rise from one column to the full average is as large as removing at least one extra pair in five from every column. The FlyWire column mean (with its pruning) lifts the agreement number well above what single columns show. |

**Why these cuts.** B itself disagrees with flyvis-30 on 6 of its 165 pairs, 3.6 %. At `k* <= 5 %`
the pairs averaging strips from a typical column are of the same order as that whole residual
disagreement, and every thinning world, where averaging adds nothing by construction, must fall in
this range (§3.8); so (a) is "indistinguishable, at this scale, from no averaging effect". At
`k* >= 20 %` averaging strips from a typical column more than five times the bank's whole
disagreement with flyvis-30: a single column then sits well below 96.4 % (about 0.82 by the
back-of-envelope of §3.8), and the 96.4 % is mostly the average's work. Between the two the effect
is real but of a size where "the average made it" and "the columns have it" both remain arguable,
and it is named as such rather than rounded to one side. A narrower unclear band (for example
5 %-10 %) was considered and not taken: at 10 % a single column's containment is still about 0.88,
which is not far enough below 0.96 to say that averaging *manufactures* the agreement.

**Why the (c) floor is `L` and not 0 (revision 2.1).** Without a branch for a negative `Δ`, a fall
would satisfy `k* <= 5 %` and be misread as (a). Pure thinning, where averaging does nothing, can
itself put the median column a little above `R_in` (§3.8, `p` = 10 %), so 0 would call a thinning
world (c). `L` is the most negative `Δ` that thinning produced on all 48 thinning worlds (§3.8),
and a real `Δ` below it is a fall that thinning did not reach; no thinning world can read (c), by
construction. `L` is taken as it is, with no margin subtracted: a margin would be a number chosen
by eye, and the two-world check (§3.8) already requires in-F worlds at 30-40 % to fall below it and
every thinning validation world to read (a). Measured by Ark: `L` lies in about [−0.0014, 0], and
the in-F worlds at `q_F` = 30 % and 40 % (`Δ` = −0.0041, −0.0051) sit two to three times further
below 0.

**Known consequence:** `L` is expected at or a little below 0 (§3.8), and the in-F calibration spans
only about 0.005, so (c) can be read from a fall of a few thousandths. `k*_F` is printed so that the
size of a (c) reading is never hidden behind its label. No minimum `k*_F` is required for (c)
(CC decision: no new cut). (c) is a direction label at a scale of thousandths; its practical
consequence equals (a)'s; what the test is built to detect is (b). **A marginal (c) with a small
`k*_F` is indistinguishable from a no-effect world crossing below `L` (about one run in fifty);
read its direction, not an effect** (Zcode, revision 2.2; about 1.5 % of no-effect worlds at
`p` = 10 % fall below zero).

**Why this rule and not the Q3/P95 rule.** `Δ` compares the median single column with the full
average, so dropping pairs (thinning) moves it by at most a few thousandths either way, whatever
`p`, while sporadic extra pairs move it in one direction only, more as there are more: upward when
they fall outside F, downward when they fall inside F; the reading is monotone in the effect it is
meant to see. The Q3/P95 label of the first draft is not (§3.7); it is printed as a secondary label
and decides nothing.

**Chance.** Every point of the curve has the same chance level, 0.2533 (§3.3), so the rule reads
the same on raw and chance-corrected values.

**What decides.** The verdict is the label of `Δ`. The label of `Δ_294` (§3.3, read by the same four
branches), the in-F share of extras (§3.9), the Q3/P95 labels of S1 and S2 (§3.7), and S2-S4 are
printed beside it and decide nothing. If the label of `Δ_294` differs from the verdict,
`RESULT.md` prints "the 796-column and 294-column readings disagree" beside the verdict. Whatever
the label, `RESULT.md` prints `Δ`, `L`, `k*` and `k*_F` as numbers next to it.

**Two prints on the verdict line (Ark, revision 2.2; no new cut, they decide nothing).**

- **Extras and losses.** The verdict line prints the median `|E_c \ B|` (extra pairs per column)
  and the median `|B \ E_c|` (bank pairs a column lacks), over the 796 columns, beside the label.
  The branch words ("strips", "removes") describe the case of extra pairs. To first order,
  ```
  Δ ≈ [(R_in − f_a) · a + (f_r − R_in) · r] / |B|
  ```
  with `a` the extra pairs of a column and `f_a` their in-F share, `r` the bank pairs it lacks
  (here a count, not the rate `r` of §3.8) and `f_r` their in-F share. Random loss contributes
  zero (`f_r = R_in`); loss of the six non-F pairs of B contributes negatively. A positive `Δ` can
  therefore also come from losses concentrated inside F: if the columns mostly lack bank pairs
  rather than carry extras, (b) can mean that averaging **restores missing pairs** rather than
  strips extras. The two medians show which case the columns are in.
- **`k*_obs`.** Printed next to `k*`: `k*_obs = Δ / (R_in − X)`, with `X` the median of `X_c`
  over the 796 columns (§3.9): the first-order extra-pair rate for the columns' own in-F share of
  extras. It is a diagnostic and decides nothing. Its measured bounds on the uniform-extras worlds:
  accurate at small `r` (`r` = 5 %: measured `Δ` +0.0392 against a first-order +0.0435), and it
  underestimates the rate at large `r` (`r` = 40 %: measured `Δ` +0.2481 against a first-order
  +0.3479). It is printed because `k*`
  rests on an assumption: that a real column's extra pairs fall in F like uniform noise,
  `f_a` = 69/735 = 0.094.

## 5. What each outcome means for question (ii)

| label | what (ii)'s registration must do |
|---|---|
| **(a)** | (ii) may use the 96.4 % as its reference level without normalising for the FlyWire column mean. It must still state that flyvis's own column mean, the max merge and the hand edits are unmeasured (Part A: none can be separated with what flyvis ships). |
| **(b)** | (ii) must normalise against averaging. Its registration names the normaliser before data: the S1 distribution (single included column inside flyvis-30) as the level expected with no averaging, and S4-294 (split-half of the same 294 columns inside flyvis-30) as the level averaging alone reaches within one fly; the curve (§3.2) is printed beside them. The 96.4 % is not to be read as between-brain agreement on its own. |
| **unclear** | (ii) must report the 96.4 % only beside the curve and the S1 quantiles, never alone. Whether (ii) resumes, and with which normaliser, returns to Mike. |
| **(c)** | (ii) may use the 96.4 % as its reference level without normalising for the FlyWire column mean, and must state that on the FlyWire side it is **conservative**: FlyWire averaging lowers agreement with flyvis-30, so it is not what produces the overlap. (ii) must print the S1 distribution beside the 96.4 % as the higher, single-column level, and `k*_F` with it. It must not claim that the 96.4 % understates between-brain agreement overall: flyvis's own column mean, the max merge and the hand edits remain unmeasured and may still inflate it from the flyvis side (§6). |

Under every label the result is a **lower bound** on the arithmetic's share (§0), on the FlyWire
side; under (c) that share is negative (the FlyWire arithmetic lowers the number). It is reported
under the name of §0, never as "the overlap between banks".

## 6. What the test cannot show (lesson b: can it see all the worlds?)

- **It can see all three worlds by construction check,** not by hope: §3.8 runs the rule on worlds
  where averaging adds nothing (thinning, eight rates), where it removes sporadic extras outside F
  (uniform extras) and where it removes sporadic extras inside F (in-F extras), with seeds
  independent of the calibration (the thinning validation worlds also enter `L`, so for them only
  the upper side is an independent check), and stops if the rule cannot tell them apart. That
  checks the rule, not the biology.
- **The verdict depends on the thresholds for `k*`, 5 % and 20 %** (Johnny, revision 2.2). They
  are fixed before data (§4) and are not revised after it. The script prints `k*` itself, so a
  reader can see how far it sits from each threshold. Johnny's falsifier: if `k*` lands far from
  both thresholds, this sensitivity does not bite.
- **Real sporadic pairs may be neither uniform nor all inside F.** The two extras families bracket
  the possibilities: uniform extras push `Δ` up, in-F extras push it down. A real mix can **cancel**:
  columns carrying both kinds can give `Δ ≈ 0` while averaging removes pairs in both directions. So
  a reading of (a) means "no *net* averaging effect on containment", **not** "no averaging effect".
  The in-F share of extras, `|E_c \ B|` and `|B \ E_c|` (§3.9) are printed beside the verdict so a
  cancelling mix is visible (for example, many extras per column with an in-F share well above
  0.094); they decide nothing.
- **(c) is read at a fine scale.** Because the flyvis-only cells are only 69, the whole in-F
  calibration spans about 0.005 of containment (§3.8), and the (c) floor `L` sits at or near 0. A
  (c) reading may therefore rest on a fall of a few thousandths; `k*_F`, `Δ` and `L` are printed
  with it so its size is never read from the label alone.
- **It bounds only the FlyWire side.** Three steps stay inside flyvis-30 unmeasured: **flyvis's own
  column averaging**, the **max merge** and the **hand edits**. Part A (§8) finds no per-volume and
  no per-column data in flyvis 1.2.0, so flyvis's averaging cannot be removed, just as the merge
  cannot. flyvis's averaging, if it acts as ours does, removes sporadic pairs and so raises
  agreement; the max merge can only add pairs to flyvis-30 and so can only raise containment of a
  FlyWire set inside it. Both unmeasured inflations point the same way as the one this test
  looks for on the FlyWire side, so if the test reads (a), (b) or unclear, the 96.4 % is an **upper
  bound on the unprocessed agreement from both sides**, and this test bounds the inflation **on the
  FlyWire side only**. If it reads (c), the FlyWire side points the other way, and the 96.4 % is an
  upper bound from the flyvis side only; the net direction is then unknown. The hand edits'
  direction is unknown in every case.
- **It cannot separate the column mean from the pruning below 1.** The pruning acts on the mean; at
  the column level it is a no-op (§2.5). The test measures the two together, as the bank applied
  them.
- **It cannot tell biology from reconstruction noise within a column.** A pair present in one
  column and absent from the bank may be a real idiosyncratic connection or a segmentation or
  synapse-detection error. Averaging removes both; the test counts both as "removed by averaging".
- **The synthetic worlds are simpler than the columns** (§3.8): independent columns, all 30 types,
  one value per present pair, extras uniform over non-B cells. The calibration fixes a scale for
  `Δ`; it does not claim the real columns are generated that way.
- **The single-column statistics do not speak for the excluded columns** (502 of 796), which may
  differ systematically (edge of the eye, proofreading completeness). The machine check and the
  curve use all 796; S1-S4 use 294 (S4-796 is printed beside S4-294).
- **It is within one fly.** Column-to-column agreement within FlyWire is not between-fly variation,
  and must not be read as such.
- **Offsets are not compared.** Existence only, as in question (i). A column and the bank may
  agree on a pair at different offsets.
- **The FlyWire typing caveat travels with it** (ADR-005 point 5): FlyWire's cell typing may lean
  on connectivity, which would raise within-fly agreement. Unverified.
- **Handedness does not matter here:** existence is invariant to a fixed relabelling of offsets
  (FlyWire registration §3.3).

## 7. Environment, script, outputs, cost

**Environment.** `tools/.venv` is not modified (its digest is pinned by night 6 gate 8). The script
reads the feather file and so runs as the builder does:

```
uv run --no-project --with pyarrow --with numpy --with pandas python \
    results/genome/c6/checks/flywire_column_test.py
```

**Script (design only; not written yet):** `results/genome/c6/checks/flywire_column_test.py`.
Order of work, each step refusing on failure:

1. Refuse on a dirty tree (this registration committed first) or a missing data root.
2. Check the builder's sha256 (§2.1), the column file's sha256 and size (§1), the bank offsets
   file's sha256 (§3.6); import the builder's constants.
3. Build `x_c` for all 796 columns (§2.4) into memory.
4. Machine check (§3.6).
5. Synthetic worlds (§3.8): the seed-uniqueness assertion, the three calibrations (uniform
   `Δ_cal`, in-F `Δ_calF`, and the thinning envelope `L` over all 48 thinning worlds), their
   monotonicity checks, then the two-world check on independent seeds. Stop on any failure. No
   real curve point or S1-S4 value exists yet.
6. The real curve (§3.2), its anchor check at `k = 796`, `Δ`, `L`, `k*`, `k*_F` and the verdict
   (§4), with the median `|E_c \ B|`, the median `|B \ E_c|` and `k*_obs` on the verdict line.
7. Column inclusion (§2.3); stop rule (< 100 columns) for S1-S4 only.
8. S1 with `Δ_294` and its label, the in-F share of extras (§3.9), S2, S3, S4-294 and S4-796, the
   Q3/P95 secondary labels (§3.7), Zcode's falsifier print (§3.2), the offset-bin counts (§2.4).
9. Write outputs; print wall-clock time.

**Outputs.**

- Committed, `results/genome/c6/checks/flywire_column_test/`: `RESULT.md` and `summary.json`
  holding the manifest (git head, script sha256, builder sha256, every input's sha256 and size,
  column-file download date), the included-column count and the counts the inclusion rule removed,
  the machine check's and the curve anchor's results, every synthetic world's curve summary, `Δ`,
  label and Q3/P95 label, the calibration points `Δ_cal(r)` and `Δ_calF(r_F)`, the thinning
  envelope `L` with the 48 `Δ` it is the minimum of, the real curve's per-`k` quantiles, `Δ`, `k*`,
  `k*_obs`, `k*_F` and the verdict, `Δ_294` and its label, the in-F share of extras (§3.9), every quantile of S1-S4 with its denominator
  (lesson g), the reference numbers of §3.1 **printed verbatim under their names** (lesson f), and
  the registered reading of §4 and §5 quoted, not paraphrased. Also a plot of the real curve with
  the calibration worlds' curves (aggregate only; no column identifiable).
- Not committed, `connectome-seed-data/FlyWire/derived/column_test/`: per-column offset rows,
  per-column existence sets, the included-column list, the sampled column lists, the S4 half-bank
  sets, and a manifest with their hashes.

**Cost.** Reading the feather file and grouping is the builder's cost (the build of 2026-09-24
was not timed separately; expect minutes, not hours, on this machine). Everything after that is
set arithmetic and sums of per-column rows:

- the real curve: 9 sampled values of `k` × 50 samples, plus 796 single columns and one full
  average; the sampled averages sum about 50 × (2 + 4 + … + 512) ≈ 51,000 column tables in all,
  which as a dense columns-by-rows array is one matrix product per `k`;
- the synthetic worlds: thinning 40 calibration + 8 validation, uniform extras 4 + 5, in-F extras
  5 + 2, so 64 worlds of 796 columns × 900 cells, each with the same curve (a boolean array; each
  `k` is one product of a 50 × 796 sample-indicator matrix with the 796 × 900 world);
- S1-S4: 294 columns, 43,071 column pairs, 2 × 20 splits.

Estimate: still under 10 minutes total, dominated by the feather read; single process, no GPU
needed (an estimate, not a measurement; the script prints the time actually taken).

## 8. Part A: does flyvis 1.2.0 expose FIB-25 and FIB-19 separately? (ADR-005 Q2)

**Verdict: NO.** flyvis 1.2.0 ships, and caches, only the merged template. **Confirmed by a second
reader (Zcode, 2026-09-24 18:35 UTC)**, from an independent reading of the package; **this
confirmation is final.** Evidence:

- **One connectome file.** The package's only connectome data file is
  `tools/.venv/Lib/site-packages/flyvis/connectome/fib25-fib19_v2.2.json`; the wheel's `RECORD`
  lists no other json, csv or h5 of connectivity (its only other data file is
  `flyvis/data/responses_norm.h5`, a response normaliser). The name `fib25-fib19` appears only as
  this one file name: in `config/network/connectome/connectome.yaml:2`,
  `connectome/connectome.py:156, 160`, `network/network.py:71`, `__init__.py:59` and the
  `_meta.yaml` of the compiled caches. No other string `fib19`, `fib25`, `FIB-19` or `FIB-25`
  occurs in the package or in `flyvis_cli`.
- **One estimate per offset in the json.** Its top-level keys are `nodes`, `edges`, `receptors`,
  `input_units`, `output_units`. Each of the 605 edges has exactly the fields `src`, `tar`,
  `offsets`, `alpha`, `alpha_fixed`, `alpha_references`, `time_constant`, `time_constant_fixed`,
  `lambda_mult`, `edge_type`, and `offsets` holds one `[[du, dv], n_syn]` per offset. The schema in
  the `ConnectomeFromAvgFilters` docstring (`connectome/connectome.py`, lines ~140-160) has one
  number per offset. There is no field for a second volume, and none for a single column.
- **`lambda_mult` is not a second estimate.** It is one float per edge (528 distinct values, 0.707
  to 134.4), stored as `n_syn_certainty` (`connectome.py:258, 431, 499`; docstring "Certainty of
  synapse count", `connectome.py:382`) and read by no other module. One scalar per edge cannot
  hold two per-offset estimates. How it was derived is not documented in the package; whether it
  reflects agreement between the volumes is **unknown**, and it is not used here.
- **The caches are compiled from the merged json.** Every `ConnectomeFromAvgFilters_000*` directory
  (in the package's `data/connectome/` and in `connectome-seed-data/connectome/` and `results/`)
  has `_meta.yaml` with `file: fib25-fib19_v2.2.json` and holds only compiled lattice edges
  (`du`, `dv`, `n_syn`, `n_syn_certainty`, `sign`, source and target index, type, `u`, `v`).
- **Downloads.** The package downloads Sintel, Moving MNIST (`utils/dataset_utils.py`) and, via
  `flyvis_cli/download_pretrained_models.py`, `results_pretrained_models.zip` and
  `results_umap_and_clustering.zip` (trained networks and clustering). None is a connectome source.
- **The paper's supplement.** No local copy exists: no `*MOESM*` or Lappalainen file in the
  repository or under `connectome-seed-data/` (the 2026-09-23 note read it online; nothing was
  saved). Equation 7 in that supplement describes the merge, not a released per-volume table.
  Nothing was downloaded for this reading.

**Consequence.** The two-number merge measurement of ADR-005 point 4 (overlap of one volume with
FlyWire against overlap of the merge with FlyWire) **cannot be made from flyvis 1.2.0**, so it is
not registered here. For the same reason flyvis's own column averaging cannot be undone: the
package holds only the averaged, merged estimate. The max merge and flyvis's averaging stay
unmeasured steps inside flyvis-30 (§0, §6). Getting per-volume estimates would need either the
flyvis authors' pre-merge tables (not public as far as this reading found; not checked outside the
package) or a rebuild from the FIB-25 and FIB-19 reconstructions with the authors' column
assignment, which is not public either. Both are outside the admission rule until a number asks
for them.

## 9. Lessons applied ([lessons note §3](../notes/2026-09-24-lessons-from-the-art-report.md))

| lesson | where here |
|---|---|
| a, selection after the data | one primary statistic (`Δ`), its calibration and its cuts fixed in §3.2, §3.8 and §4 before any column value exists |
| b, a null that cannot see the other world | §3.8 calibration (three families) and two-world check on independent seeds; §4 branch (c) for a negative `Δ`; §3.7 records why the first draft's rule failed it; §6 |
| c, a criterion written after the finding | a reading for (a), (b), (c) and unclear in §4 and §5 |
| e, read the object | the machine check (§3.6) rebuilds the whole bank from the per-column tables; the curve's anchor (§3.2) repeats it on the curve's code path |
| f, a number under its own name | §3.1's references and §4-§5's readings printed verbatim |
| g, denominators | every quantile printed with its number of columns, samples or column pairs |

## 10. Decisions for Mike

Each item: what the options change, and a recommendation. **D1-D6 carry the reviewers' unanimous
recommendation (Ark, Johnny, Zcode, DPC Research chat 2026-09-24 18:26-18:35 UTC); Mike may
override any of them.** The body above is written with the recommendation. In the second review
(18:53-18:58 UTC) all three reviewers accepted the `k*` thresholds 5 % and 20 % and D1-D6
unchanged.

1. **D1, which columns count for the single-column statistics.** Reviewers: **(i), 294**; Ark
   verified the counts 796 / 306 / 294 / 612 / 142 / 137 / 0. (i) complete and interior, 294
   columns: every column in the same 900-pair universe, inputs at offset 1 not cut by the edge.
   (ii) complete only, 306: 12 more columns, some at the edge, where offset-1 inputs can be missing
   and `E_c` shrinks for geometric reasons. (iii) all 796, each comparison restricted to the target
   types both sides hold: uses every column but makes the universe differ from column to column.
   (The curve uses all 796 whatever D1 says, §2.3.)
2. **D2, which statistic decides.** Reviewers: **the dose-response curve decides, S1 is kept as the
   single-column picture.** (i) the curve's `Δ` (§3.2): the full-average end is exactly the bank,
   the reading is monotone in the effect it looks for, and S1 is printed beside it. (ii) S1 alone,
   read by its quantiles: rejected in review because its rule is non-monotonic (§3.7). (iii) S2,
   column against column: closer to Ark's original wording but compares within one fly against a
   between-fly number.
3. **D3, the cuts.** Reviewers: **replace the Q3/P95 cuts by the curve rule; keep Q3/P95 as a
   secondary label.** (i) `k*` located on extras-world calibration, (a) at `k* <= 5 %`, (b) at
   `k* >= 20 %`, and (revision 2.1, CC's logic check, after the vote) (c) at `Δ < L`, with (a)
   also requiring `Δ >= L` (§4) [recommended]: a scale fixed by worlds with known answers, checked on
   independent seeds. (ii) Q3/P95 of the column distribution: non-monotonic (§3.7). (iii) No
   verdict, description only: safest against a bad cut, but then (ii)'s registration has no fixed
   rule. *Within D3, not voted on by the reviewers:* the two-world check requires (b) at 30 % and
   40 % and only "not (a)" at 20 %, because a world built on a cut crosses it at random (§3.8);
   **accepted by CC**. Branch (c), the in-F calibration, and the in-F rates capped at `q_F` = 40 %
   of the 69 cells (§3.8, **approved by CC**) are CC's and the reviser's; the reviewers have not
   seen them.
4. **D4, offset support.** Reviewers: **(i), any offset.** (i) any offset: the bank had no offset
   limit, so a limit here would be a second difference from the bank. (ii)
   `max(|du|, |dv|) <= 2`, the bank's observed range: removes far, possibly spurious per-column
   connections, but uses a bound read from the bank itself.
5. **D5, null.** Reviewers: **(i), density-matched.** (i) density-matched, exact. (ii) add a
   degree-preserving shuffle per column: it would count type-level order as chance, which is the
   order under test.
6. **D6, split-half S4.** Reviewers: **include, on S1's population (294), with S4-796 printed
   beside it.** (i) include, 20 seeded splits, description only: it is the normaliser branch (b)
   needs, and it costs seconds. (ii) leave out: branch (b) would then name its normaliser later,
   after this result is known.
7. **Order against the knockout registration** (ADR-005 Q3) is Mike's and is not decided here.

## 11. Not verified at drafting

- The feather file was not opened; its schema is taken from the FlyWire registration §3a.2.
- Whether `(p, q)` are true axial coordinates (assumed, as in the builder; the included-column
  count depends on it through the neighbour test).
- Why columns lack some of the 30 types (biology, assignment coverage, or proofreading).
- What `lambda_mult` in the flyvis json encodes.
- Whether the flyvis authors released per-volume tables anywhere outside the package.
- **Closed in revision 2.2: the switching points of the Q3/P95 label under thinning.** The earlier
  review table with (b) at `p` = 0.2 % is withdrawn by its author. Ark's simulation (4000 repeats
  per rate; confirmed by Zcode and Johnny) agrees with the reviser's back-of-envelope: (a) up to
  `p` = 0.5 %, on the edge at 1 %, unclear at 2 %, (a) again at 5-10 %, borders near 1.05 % and
  4.7 %, never (b), since the share of columns at or above `R_in` has minimum 0.1496 (§3.7). The
  label stays secondary; the script prints the actual labels.
- The back-of-envelope values of `Δ_cal`, `Δ_calF` and `L` in §3.8 are expected values, not
  medians of a run.
- **Closed in revision 2.2: whether the (c) floor `L` is robust.** `L` is now the minimum over all
  48 thinning worlds, so no validation thinning world can dip below it. Ark measured its band: `L`
  lies in about [−0.0014, 0], `P(L < −0.002) = 0` in 20,000 draws, and the in-F worlds at
  `q_F` = 30 % and 40 % (`Δ` = −0.0041, −0.0051) sit two to three times further below 0 (§3.8).

## 12. Changelog

**Revision 2 (2026-09-24 UTC): reviews by Ark, Johnny, Zcode** (DPC Research chat, 18:26-18:35
UTC; unanimous).

- §3.7, §4: the Q3/P95 rule is non-monotonic under thinning; demoted to a secondary label that
  decides nothing, printed with its switching points (Ark; confirmed by Johnny, Zcode).
- §3.2: the primary reading is a dose-response curve, containment in F of the average over `k`
  columns, `k` = 1 … 796 (Ark, Johnny).
- §3.2: the curve averages with the builder's own rule restricted to the sample (per-type
  denominator = type-`t` neurons in the sample, pruning after division) and samples from all 796
  columns, so `k = 796` is the bank exactly and is checked; 50 seeded samples per `k` (Zcode).
- §3.2: Zcode's falsifier (the 294-average reproducing the bank) recorded; the structural part
  (every `N_t` ≥ 654 ≠ 294) stated, the rest left to the script as a printed diagnostic (Zcode).
- §3.8, §4: the curve's reading is fixed before data by thinning worlds (`p` from 0.05 % to 10 %)
  and extras worlds (`r` = 5-40 %) on the full 900-cell grid; primary statistic `Δ`, read as the
  equivalent extra-pair rate `k*` with cuts at 5 % and 20 % (CC; low thinning rates Johnny).
- §3.8: the two-world check runs on seeds independent of the calibration and requires (b) at 30 %
  and 40 % rather than at 20 % (reviser, on CC's requirement; open in D3).
- §3.3: S1 kept as the secondary single-column picture on the 294, with `Δ_294` printed beside the
  verdict (Ark, Johnny).
- §3.5, §5: S4 taken on S1's population (294, halves of 147), S4-796 printed beside it; §5(b)
  names S4-294 (Ark, Zcode).
- §2.3, §2.4: `x_c` defined for all 796 columns; the inclusion rule governs only the single-column
  statistics (Ark, Zcode).
- §0, §5, §6: flyvis's own column averaging added to the unmeasured steps; both unmeasured
  inflations point the same way, so 96.4 % is an upper bound from both sides and the test bounds
  only the FlyWire side (Ark, Zcode).
- §8: Part A confirmed by a second reader (Zcode, 18:35 UTC).
- §10: the reviewers' votes on D1-D6 recorded as their unanimous recommendation, Mike may override
  (Ark, Johnny, Zcode).
- §7: script order, outputs and cost updated for the curve and the 17 synthetic worlds (reviser).

**Revision 2.1 (2026-09-24 UTC): negative-Δ branch (c) and in-F extras calibration (CC logic
check).**

- §3.2, §0: `Δ` can be negative (sporadic single-column pairs inside F \ B, pruned by averaging).
- §3.8: third calibration family, in-F extras (the 69 flyvis-only cells), `q_F` = 5-40 % of the 69
  cells (`r_F` = 2.1-16.7 % of `|B|`), with its own map `k*_F`; `k*` is defined on the uniform family
  only. Rates above `r` ≈ 20.9 % of `|B|` cannot be built as sporadic in-F extras (reviser).
- §3.8: thinning lower envelope `L` = minimum `Δ` over 40 thinning calibration worlds (5 seeds per
  `p`), nothing subtracted.
- §4: branch (c) "averaging removes agreement" at `Δ < L`; (a) now requires `Δ >= L` and
  `k* <= 5 %`, so a negative `Δ` is never read as (a).
- §3.8: two-world check adds in-F worlds at `q_F` = 30 % and 40 % that must read (c) on fresh seeds;
  thinning worlds must read (a). The revision-2 check (fresh seeds; (b) at 30/40 %, not (a) at
  20 %, unclear at 10 %, not (b) at 5 %) accepted by CC.
- §5: consequence of (c) for question (ii).
- §3.9, §6: in-F share of extras printed beside the verdict as description; a cancelling mix means
  `Δ ≈ 0` does not prove "no averaging effect"; (c) is read at a fine scale; the upper-bound
  statement of §6 is conditioned on the label.
- §7, §9, §10, §11: script order, outputs, cost (64 synthetic worlds), lessons, D3, open points.

**Revision 2.1, CC decisions (2026-09-24 UTC).**

- §3.8, §10: the in-F rate cap (`q_F` = 5-40 % of the 69 cells; (c) required at `q_F` = 30 % and
  40 %) approved by CC.
- §3.8: every thinning validation world must read (a) or (c) (not (b), not unclear), because (c) and
  (a) have the same consequence for question (ii); this removes the false stop of §11. In-F worlds
  at 30/40 % must still read (c); uniform worlds unchanged.
- §4: no minimum `k*_F` for (c) (no new cut); added: "(c) is a direction label at a scale of
  thousandths; its practical consequence equals (a)'s; what the test is built to detect is (b)."

**Revision 2.2 (2026-09-24 UTC): second reviews by Ark (18:53 UTC), Zcode (18:55 UTC) and Johnny
(18:58 UTC).** All three accept the `k*` thresholds 5 % and 20 % and D1-D6 unchanged.

- §3.7, §11: the reason for dropping the Q3/P95 rule rewritten on Ark's simulation (4000 repeats
  per rate): the exact rule, the share `1 − (1 − p)^6 + (1 − p)^165` with minimum 0.1496 at
  `p` = 2.06 %, labels (a) → unclear → (a) under thinning and never (b), (b) on every uniform-extras
  world; the defects are "never (b) under thinning" and "unclear with no effect". The earlier table
  with (b) at `p` = 0.2 % is withdrawn (Ark's self-correction, confirmed by Zcode and Johnny); the
  §11 item on it is closed. Q3/P95 stays a secondary label.
- §3.8: seed collision fixed. Thinning calibration `150 + 10 i + j` reaches 200-204 at `i` = 5,
  where the uniform-extras calibration sat (200-203); the uniform-extras calibration moves to
  `250 + i`. All world-generating seed ranges listed and disjoint; the script asserts that all
  seeds are unique (found by Ark; Zcode retracted his earlier "seeds do not overlap").
- §3.8, §4, §6, §7, §11: `L` is the minimum `Δ` over all 48 thinning worlds (40 calibration + 8
  validation), so no thinning world can read (c); the two-world check requires (a) of every
  thinning world instead of "(a) or (c)"; Ark's measured band for `L` recorded; the §11 item on
  `L`'s robustness closed (Ark, accepted by Zcode).
- §4: the marginal-(c) sentence, "A marginal (c) with a small `k*_F` is indistinguishable from a
  no-effect world crossing below `L` (about one run in fifty); read its direction, not an effect"
  (Zcode).
- §4, §3.9, §7: two prints on the verdict line, no new cuts: the medians of `|E_c \ B|` and
  `|B \ E_c|` with the first-order form of `Δ` (branch words describe extras; (b) can also mean
  averaging restores missing pairs), and `k*_obs = Δ / (R_in − X)` beside `k*` with its measured
  bounds (Ark).
- §3.2: `Δ` has no sampling error; the verdict does not depend on seeds (Ark, Zcode).
- §6: the verdict's dependence on the 5 %/20 % thresholds disclosed, with Johnny's falsifier
  (Johnny).
- §3.8: the reviewers' checks of the back-of-envelope estimates agree with Ark's simulation; the
  value 2 is the definition, not an idealisation (Ark).
- §8: Zcode's confirmation of Part A (18:35 UTC) marked final.
- §10: the second-review votes recorded.
