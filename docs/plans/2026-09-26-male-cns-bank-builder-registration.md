---
**Status (revision 1, drafted 2026-09-25 20:10–21:00 UTC; 2026-09-26 local, +07:00): draft for
review. Not reviewed, not committed, nothing built.** Drafted by a CC subagent on Mike's word in
the DPC Research chat, 2026-09-25 20:02 UTC: "do the male CNS builder". The seven points it must
fix were agreed in the chat at 19:58–20:01 UTC by Ark, Zcode and CC (as relayed in the drafting
brief; the chat is not in the repository). The design choices that need a vote are marked
**proposal** in the body and listed in §13. The body is written with the recommended option, so
the draft is complete as it stands.

**File date.** The request named this file `2026-09-26-…`, which is the local day. The UTC clock
read 2026-09-25 20:10 UTC when drafting began (`date -u`), so the
[glossary's date-time convention](../../GLOSSARY.md) would date it `2026-09-25-…`. The name is
kept as requested and the question is D14 (§13), as it was D12 of the knockout registration.

**What was read from the male CNS data for this draft, and nothing else** (§1.2): the file list
and sizes; the sha256 of both files; the Arrow schema of both files; the pandas metadata of both
files (which carries the row counts); the first three rows of thirteen annotation columns; and the
value domains of five small annotation columns (`somaSide`, `rootSide`, `statusLabel`, `status`,
`superclass`). **No weight was read. No connectivity was computed. No type was counted.** The
only bank number computed is the flyvis-65 outside-block density on three candidate grids (§5.3),
from `offsets.csv` with the 64 block cells dropped before any presence was read.
---

# Registration: the male CNS bank builder (the animal control for knock out and regrow)

## 0. What this registers, and what it does not

**What it registers.** A **builder**: a script that turns the Janelia male CNS v1.0 flat
connectome into **two banks**, one per optic lobe, in the format the C6 harness loads. Each bank
lives on the harness's 65-type grid (4,225 cells) and uses the subset of types that the type map
places (§3). The banks are to serve as the **animal control** of the knock-out-and-regrow test,
[`2026-09-24-knockout-regrow-registration.md`](2026-09-24-knockout-regrow-registration.md) §8.

**What it does not register.**

- **Not the control arm.** Fitting, scoring and reading block A on these banks is the job of the
  male-CNS arm's own registration. That registration is separate and comes later (knockout
  registration §8: "The male CNS bank and its builder are a separate registration").
- **Not a verdict.** The builder fits nothing. It prints no number about the 64 cells of block A
  (§9).
- **Not a change to the knockout registration.** That registration is amended later, and only to
  pin the built banks' sha256 (its §8: "and nothing else in it changes").

**What is already known at drafting (stated, because a threshold is being chosen after it).**

- **The flyvis-65 arm has run.** Its registered verdict is **G**, "not detected at the R level
  above γ_R" (commit `1ed55ec`; the commit message and
  `docs/notes/2026-09-26-knockout-regrow-blind-review.md` §A). Under D13 of the knockout
  registration, "R on the male CNS only" is "a flag to re-examine both fits" (§8 there). **So
  the one male-CNS outcome that would change a reading is R.** A threshold that is looser or
  tighter on block A makes R easier or harder. This is why D1's rule reads no block cell (§5).
- **Block A of the male CNS has already been looked at,** in a preliminary graph (Zcode,
  2026-09-24 20:59 UTC; knockout registration §8; backlog entry
  `THE-MALE-CNS-BANK-NEEDS-A-REGISTERED-BUILDER-…`). Under the definition "total synapses / number
  of target neurons in the lobe ≥ 1" (about a sum of 850 or more), the block was a perfect board
  with 4 mirror cells. Under other definitions, 20–21 weak cross cells appeared, with means of
  1.0–2.2, and 52–54 mirror cells. **The people choosing D1 therefore know which threshold gives a
  perfect board.** The recommended rule (§5.2) is a function of outside-block cells and of
  flyvis-65 only, so its output does not depend on that knowledge. The choice *of the rule* is still
  made by people who have that knowledge, and this is recorded, not removed.
- Zcode's other definitions (the ones that gave 20–21 cross cells) are **not written in any file
  this draft opened.** They are not reproduced here.

## 1. Inputs and pins

### 1.1 Files

| file | bytes (observed) | sha256 (observed with `sha256sum`, 2026-09-25 ~20:15 UTC; equal to the folder's `SHA256SUMS.txt`) | used for |
|---|---|---|---|
| `connectome-seed-data/Janelia/body-annotations-male-cns-v1.0-minconf-0.5.feather` | 14,483,314 | `2177e246113e4cfbf1e7772ec37c6da1955ff22e8063d0b1f833101f99a9a3b2` | body → type, side |
| `connectome-seed-data/Janelia/connectome-weights-male-cns-v1.0-minconf-0.5.feather` | 1,051,241,946 | `e35da783d1c686b2b58b3b87cd6a403ae43bfcfba8bff28e08ef752c1a56afc1` | neuron-pair synapse counts |
| `results/genome/bank/offsets.csv` | — | `8c45e8508d8f6ae45e9ab3f9d95d58e4521894ccfa51954f6d77d41e550fa5f0` (LF; recomputed for this draft, equal to knockout registration §1.1) | flyvis-65 existence, for the density target (§5.3) |
| `results/genome/bank/types.csv` | — | `237a195a36f62ce182fee8486394c27d2beb9825bc029cb215c39c0fa323a477` (LF; as above) | flyvis-65 names and birth-id order |

`connectome-seed-data/Janelia/SOURCE.md` (read): "Male CNS v1.0 (Berg et al. 2026), flat
connectome files from `https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome/`
(see `https://male-cns.janelia.org/download/`), downloaded 2026-09-23 UTC by Mike. Licence:
CC-BY (Janelia project page)." The builder refuses if any sha256 above differs. The manifest
carries each input's name, size, sha256 and download date forward (the FlyWire precedent,
[`2026-09-24-flywire-bf-p3-registration.md`](2026-09-24-flywire-bf-p3-registration.md) §1,
"Manifest requirement"). The two flyvis CSVs start with one `# source=…` comment line. The builder
skips it as `harness.read_csv` does (`skiprows=1`), and it refuses if line 1 does not start with
`# source=flyvis`.

### 1.2 The schema, as observed (read-only; no weight read)

Read with pyarrow 25.0.1 through `pyarrow.ipc.open_file` on a memory map (scratch scripts outside
the repository).

**Weights file.** Three columns, `body_pre: int64`, `body_post: int64`, `weight: int64`.
**151,856,684 rows**: this is the `stop` of the pandas RangeIndex in the file's schema metadata,
not a count of rows read. It is stored in **2,318 record batches**. That is consistent with the
pandas default chunk of 65,536 rows (151,856,684 / 65,536 = 2,317.2), but the batch sizes of this
file were **not read**. There is no side, type, region (ROI) or confidence column. The confidence
cut is in the file name (`minconf-0.5`).

**Annotation file.** 211,577 rows in 4 record batches (65,536 × 3 + 14,969, read), 211,577
distinct `bodyId` (read). 36 columns: `assignedOlHex1`, `assignedOlHex2` (double), `bodyId`
(int64), `flywireType`, `group` (double), `instance`, `somaSide`, `statusLabel` (dictionary),
`superclass`, `type`, `vfbId`, `hemibrainType`, `itoleeHl`, `supertype`, `birthtime`,
`mancBodyid`, `mancGroup`, `mancType`, `subclass`, `synonyms`, `class`, `rootSide`,
`somaNeuromere`, `trumanHl`, `dimorphism`, `matchingNotes`, `entryNerve`, `mancSerial`,
`mcnsSerial`, `serialMotif`, `fruDsx`, `exitNerve`, `receptorType`, `somaLocation`,
`tosomaLocation`, `status`. Nulls: `type` 47,071 and `flywireType` 68,421.

**Value domains read (whole column; these are domains, not type counts):**

| column | values (count) |
|---|---|
| `somaSide` | `L` 75,215; `R` 75,119; `M` 392; null 60,851 |
| `rootSide` | `L` 7,802; `R` 9,723; `unknown` 414; null 193,638 |
| `status` | `Traced` 165,122; `Orphan` 15,925; `Glia` 11,864; `Unimportant` 10,751; null 5,472; `Assign` 1,832; `Anchor` 611 |
| `superclass` | 28 values, among them `ol_intrinsic` 89,403, `ol_sensory` 6,098, `visual_projection` 9,201, `visual_centrifugal` 563; null 44,877 |
| `statusLabel` | 20 values (`Reviewed` 54,066, `Roughly traced` 71,979, `Prelim Roughly traced` 36,387, …) |

The first three rows show `instance` values with a side suffix (`DNp01(GF)_R`, `OCG01d_L`,
`VCH_R`) and `somaSide` equal to that suffix. **Not checked:** which of `somaSide`, `rootSide` and
the `instance` suffix is filled for the 16 block types, for R1–R6, R7, R8 and CT1. Also not
checked: how many bodies each type has, whether `assignedOlHex1/2` is null for T4/T5, the
compression codec of either file, whether (`body_pre`, `body_post`) is unique, and whether rows
with `body_pre == body_post` exist. The builder settles each of these in its dry run (§10.3),
except uniqueness and autapses, which need the weight stream (§6).

## 2. What a bank file must contain (read from the harness and the FlyWire arm)

- The harness's bank is `Bank(name, content)`, where `content` maps a cell `(s, t)` of type
  indices to `{"offsets": {(du, dv): n_syn}, "hull": [...], "sign": ±1}`. **Existence is the
  presence of the key** (`harness.py`, `Bank.__post_init__`). Indices are the flyvis-65 names in
  birth-id order (`harness.NAMES`, `IDX`).
- The FlyWire arm's loader (`flywire_bf_p3.py`, `load_flywire_bank`) reads a CSV with columns
  `src, tar, du, dv, n_syn, sign`, with names in flyvis spelling, from the file named by
  `offsets_file` in a `bank.meta.json` beside it. It refuses a name outside its type set. It
  embeds the bank in the 65-type grid by setting `H.ALL_CELLS` to the placed types' cells
  (`restrict_to_30_grid`) and leaves `H.FOLD`, `H.TYPE_FIELDS`, `H.PAIR_ID`, `H.NAMES` and
  `H.IDX` untouched. The knockout registration §8 says the male-CNS bank is embedded "as the
  FlyWire arm was".
- **So the builder writes, per lobe, a CSV in that format, with names in flyvis spelling and only
  placed types, plus a manifest.** The loader of the male-CNS arm, which is not written here, reads
  it the same way.

## 3. The type map (proposals D3, D4, D5)

### 3.1 Canonical name column (proposal, D3)

**The canonical column is `type`.** A closed override table of three flyvis names reads
`flywireType` instead. Nothing else reads `flywireType`.

| flyvis name | male CNS column | male CNS value | why |
|---|---|---|---|
| R7 | `flywireType` | the R7 roll-up | `type` splits R7 into subtypes and leaves `_unclear` bodies; `flywireType` gives a ready roll-up (Johnny; knockout registration §8: "ready R7/R8 roll-ups (1300/1329) that avoid 931 `_unclear` bodies") |
| R8 | `flywireType` | the R8 roll-up | as R7 |
| TmY9 | `flywireType` | `TmY9q` | **flagged** (D5): FlyWire splits this type into `TmY9q` and `TmY9q__perp` ([where our bank comes from §5.2](../notes/2026-09-23-where-our-bank-comes-from.md)); the map takes `TmY9q` as the review did |

**Why `type` and not `flywireType`.** (i) It is the animal's own typing. `flywireType` is a label
carried over from the FlyWire female. For an animal control, the animal's own labels are the
natural reading. (ii) The reviewed counts ("49 by name"; backlog) are, by their wording, name
matches, and the special cases say "R7/R8 via flywireType", which implies the base column was
`type`. This choice reproduces the reviewed map. **Not verified by opening the data.** (iii) The
two columns differ on block types: T4d is 1,709 bodies by `type` and 1,710 by `flywireType`
(knockout registration §8). One column must win, and the override table must be closed so that
nobody picks per type after seeing counts.

**A body belongs to a flyvis type if its canonical value equals the mapped string exactly.** A
body matched by the override table is not also matched through `type`. The self-test stops if any
body is claimed by two flyvis types.

### 3.2 The map, 65 → placed types (proposal, D4)

| group | flyvis names | male CNS | placed at grid index | count |
|---|---|---|---|---|
| by name | the 49 names not listed below (the 16 block names among them) | same string in `type` | own index | 49 |
| renamed | Am | `Am1` in `type` | Am | 1 |
| one population, six flyvis types | R1, R2, R3, R4, R5, R6 | the R1–R6 type in `type` (exact string read in the dry run, §10.3) | **R1 only**; R2–R6 not placed | 1 placed (6 mapped) |
| override | R7, R8 | `flywireType` roll-ups | own index | 2 |
| one cell per lobe, two flyvis compartments | CT1(Lo1), CT1(M10) | `CT1` in `type`, with the side flip (§4) | **CT1(M10) only**; CT1(Lo1) not placed | 1 placed (2 mapped) |
| override, flagged | TmY9 | `TmY9q` in `flywireType` | own index | 1 |
| absent | Mi3, Mi11, Mi12, Tm28 | absent from every name column (backlog) | not placed | 0 |

**Placed: 55 types; grid 55 × 55 = 3,025 cells; outside block A 2,961.** Mapped: 61 of 65, as the
backlog says.

- **Arithmetic check, not a data check.** The 16 non-name cases above (R1–R6, R7, R8, the two CT1,
  TmY9, Am, and the four absent) leave 65 − 16 = 49 names, which equals the backlog's "49 by
  name". The backlog does not name its 61st mapped type. Am → Am1 is the case that makes 49 + 12
  = 61. That Am is that type is **inferred** from this arithmetic and from the
  [where-our-bank note §5.2](../notes/2026-09-23-where-our-bank-comes-from.md), which counted `Am`
  as `Am1` for the male optic lobe. **Not verified against the file.**
- **Why one index per population (D4).** R1–R6 is one type in the male CNS (the review accepted
  it; knockout registration §8). The flat files carry no region column (§1.2), so CT1's medulla
  and lobula compartments cannot be split. Placing one population at six (or two) indices would
  make six (or two) **identical** rows and columns. That is free structure outside the block that
  flyvis-65 does not have, since its R1–R6 rows differ (`types.csv`: `n_in_entries` 3, 3, 2, 2, 2,
  1). **The index kept is the flyvis name whose birth id sorts first**, which is R1 (`9654b247…`)
  and CT1(M10) (`63667a4a…` before CT1(Lo1)'s `7c280b5b…`). The rule reads no data. The two CT1
  indices have the same `type_fields` (`types.csv` rows 18–19: stride 1, 1, `intermediate`,
  `intermediate`), so the choice changes nothing a rule can see.
- **Unplaced names** (R2–R6, CT1(Lo1), Mi3, Mi11, Mi12, Tm28) are left out of training and scoring
  by the grid restriction, as the FlyWire arm left out 35 types.

### 3.3 Self-test of the map (runs in the dry run, before any weight is read)

The builder stops, each with its own message:

- **"ZERO NAME MATCHES"** if the canonical column matches none of the mapped strings, for
  example because the column name or the file is wrong (the backlog's first step);
- **"TYPE WITH NO CELLS"** if any placed type has 0 bodies in either lobe after the side rule
  (§4). This covers all 16 block names, which knockout registration §8 requires to map;
- **"BODY IN TWO TYPES"** if a body is claimed twice (§3.1);
- **"MAP STRING NOT FOUND"** if an exact string of the map (the R1–R6 string, `CT1`, `Am1`, the
  R7/R8 roll-ups, `TmY9q`) is absent from its column. The map is not repaired in place: a
  missing string returns the map to review.

Printed, deciding nothing: for each of the 61 mapped names, the body count per lobe under `type`
and under `flywireType`, the number of bodies on which the two columns disagree, and the per-type
breakdown of `status`. These are annotation counts, not connectivity.

## 4. Left and right: two banks (proposal, D6; the within-animal null)

**Side of a body (in this order):** `somaSide` if it is `L` or `R`; otherwise `rootSide` if it is
`L` or `R`; otherwise the `_L` / `_R` suffix of `instance`; otherwise **unassigned**. `M`,
`unknown` and null do not assign. Unassigned bodies are left out and counted per type. The
fallback order exists because optic-lobe sensory cells may have no `somaSide` (their somata lie
outside the brain). Whether that is so for R1–R8 in this file was **not checked** (§1.2).

**Lobe of a body = its side, except for the declared flip set `FLIP = {CT1}`,** whose lobe is the
opposite of its side label. Zcode verified that CT1_L has 100 % of its weight with right-lobe
partners (knockout registration §8). The flip is declared before data. It is not inferred.

**The lobe-consistency check (a check that can separate both worlds).** It runs during the weight
pass (§6), on neuron pairs of **outside-block type pairs only** (§9). For each placed type, it
computes the share of the type's synaptic weight, as source and as target, whose partner body is
assigned to the same lobe. The build stops with "LOBE ASSIGNMENT INCONSISTENT" if:

- any type not in `FLIP` has a same-lobe share below 0.5; or
- CT1 **after** the flip has a same-lobe share below 0.5.

If the flip were wrong, CT1's share would be near 0 (by Zcode's 100 %). If a side column meant
something other than the lobe for some type, that type's share would fall below 0.5. The shares are
printed for every type. CT1 is not a block type, so its check reads no block cell. For the 16 block
types, only their outside-block pairs enter the share.

**Two banks.** Each lobe's bank is built from neuron pairs whose two bodies are both assigned to
that lobe. A pair across lobes enters neither bank. Its weight is counted per outside type pair and
printed as a diagnostic. **The same threshold `c*` is applied to both lobes** (D9, §5.2). So the
two banks differ only by the lobe: same animal, same pipeline, same cut. **Reading (a proposal
handed to the arm's registration, D12):** if block A regrows (R) in one lobe and not in the other,
that difference is within-animal variation, not averaging. A male-CNS R would then need both lobes.

**Known asymmetries (knockout registration §8, as counted in review; not recounted here).** R1–R6
has 2,265 bodies on the right and 1,112 on the left. CT1 and Am1 have n = 1 per lobe. The male
optic-lobe connectome that the male CNS extends is the **right** optic lobe
([where our bank comes from §5.2](../notes/2026-09-23-where-our-bank-comes-from.md), Nern et al.
2025). So the left lobe may be less complete. The per-type body counts per lobe are printed in the
dry run.

## 5. The pair statistic and the pair threshold (D1, D2, D9)

### 5.1 The statistic

For lobe ℓ and placed types s, t:

- `W_ℓ(s, t)` = the sum of `weight` over rows with `body_pre` of type s in lobe ℓ, `body_post` of
  type t in lobe ℓ, `body_pre ≠ body_post`, and `weight ≥ w_min` (D2);
- `n_ℓ(t)` = the number of bodies of type t assigned to lobe ℓ (all of them, connected or not);
- `x_ℓ(s, t) = W_ℓ(s, t) / n_ℓ(t)`: **mean synapses per target neuron from source type s.**

**Why this statistic.** flyvis's `n_syn` for one offset is the mean over target neurons of the
synapses they receive from the source neuron at that offset
([where our bank comes from §2.2](../notes/2026-09-23-where-our-bank-comes-from.md)). Summed over
offsets, that is the mean over target neurons of the synapses received from type s. So `x` is the
offset-summed analogue of flyvis's `n_syn`, and it is also the statistic of the preliminary graph
(total / number of target neurons in the lobe). It is computed without offsets, because the male
CNS has no column assignment for T4/T5 (backlog).

**w_min (proposal, D2): 1.** The release is already cut at synapse confidence 0.5 (file name), and
62 % of edges carry weight 1 (backlog, Johnny). With `w_min` = 2 those edges would leave `W`
altogether. Under D1's density rule, `c*` adapts to whatever `w_min` leaves, so `w_min` changes
*which* cells pass at a given density, not how many. `w_min` = 2 and 3 are printed as diagnostics
(§5.4). The FlyWire builder used ≥ 2 as a starting choice (`SYNAPSE_THRESHOLD = 2`,
`flywire_bank_builder.py`). Whether flyvis's source volumes applied any per-pair cut was **not
checked**.

### 5.2 The rule for D1 (proposal): match flyvis-65's outside-block density, pooled over both lobes

Let Ω be the placed cells outside block A (2,961 cells on the 55-type grid, §3.2). Let **T** be
the share of Ω that is present in flyvis-65 (existence under C6: at least one non-`dropped` row,
`harness.py`). Then:

1. `K = round(T × 2 |Ω|)`, the number of present outside cells the two lobes should hold together
   at flyvis-65's density.
2. `c*` = the K-th largest value of the pooled multiset `{x_L(s, t), x_R(s, t) : (s, t) ∈ Ω}`.
3. **A cell of either lobe is present iff `x ≥ c*` and `x > 0`.** Ties at `c*` are all present,
   and the excess over K is printed. If fewer than K pooled outside cells have `x > 0`, `c*` is the
   smallest positive `x`, and the shortfall is printed ("density below target"). Neither case is a
   stop.
4. The same `c*` is applied to the 64 block cells of each lobe. **Those cells are thresholded
   inside the builder and written to the sealed file (§9). The builder never prints them, counts
   them or uses them in choosing `c*`.**

**What this rule reads:** flyvis-65 presence outside block A, and male-CNS `x` outside block A.
It reads no block cell of either bank. Because it matches **density**, the property that sets how
much a rule can see, the male arm's instrument works at the density on which the knockout
instrument's synthetic limits were measured (knockout registration §3.6, where the degree terms
come from flyvis-65). A male-CNS verdict that differs from flyvis-65's is then not a difference of
density by construction.

**What this rule does not do.** It does not make the two banks agree cell by cell. It does not
make degrees agree. And it cannot remove the knowledge described in §0: it only makes the output a
function that this knowledge cannot steer.

### 5.3 The target, computed now (flyvis-65 only; block dropped first)

Computed for this draft by a scratch script (outside the repository) from `offsets.csv` and
`types.csv` (pins §1.1). The 64 block cells were removed before any presence was read. The full-grid
row reproduces knockout registration §1.3 (572 present of 4,161).

| grid | types | outside cells `|Ω|` | flyvis-65 present in Ω | T | K (both lobes) |
|---|---|---|---|---|---|
| all 65 (reference only) | 65 | 4,161 | 572 | 0.137467 | — |
| D4 option (b): duplicated R1–R6 and CT1 | 61 | 3,657 | 545 | 0.149029 | 1,090 |
| **D4 recommended: one index per population** | **55** | **2,961** | **497** | **0.167849** | **994** |

The builder recomputes T and K at run time and stops ("DENSITY TARGET DIFFERS") if they differ from
this table for the registered grid.

### 5.4 Diagnostics printed beside `c*` (decide nothing; outside block A only)

For each `w_min` ∈ {1, 2, 3} and each `c` in {`c*`; `c*_L` and `c*_R`, each lobe matched to T on
its own; 0.5; **1, the flyvis-style convention** (a pair needs at least one synapse per target
neuron on average, which is flyvis's equation-8 cut applied to the pair's sum instead of per
offset); 2}, and for each lobe:

- present outside cells and density;
- Johnny's inferability of the 64 block cells: a source with ≥ 2 training targets and a target
  with ≥ 2 training sources, **from outside presence only**, as knockout registration §1.4 computes
  it;
- the count of mirror cells (present transposes of block cells; they lie outside the block);
- the smallest endpoint keep among the 16 block types;
- where `c = 1` falls in the pooled outside distribution (its rank of `2|Ω|`).

**Printed only after `c*` is fixed,** in the same run. They cannot move it: `c*` is computed in
step 2 of §5.2 before any diagnostic. Zcode's other preliminary definitions are not among them,
because they are not written in any file (§0).

### 5.5 Options considered for D1 (details in §13)

- **(a) A fixed convention, `c = 1` (total / n_tar ≥ 1).** It is simple and set with no male
  number at all. **But it is the threshold under which the block is already known to be a perfect
  board** (§0). Choosing it now would choose, with knowledge of block A, the value that makes the
  male board look like flyvis's. That is lesson (a) of the lessons note, selection after the data.
  It is printed as a diagnostic.
- **(b) Density match, pooled (recommended).**
- **(c) Density match per lobe.** Each lobe gets its own `c*_ℓ`, so the two banks have equal
  density. But then the within-animal null compares two different cuts. Printed as a diagnostic.
- **(d) Degree-distribution match** (for example, the smallest distance between the outside
  in-degree and out-degree sequences of flyvis-65 and the male bank). It is closer to what N1 sees,
  but it adds a distance and a search that need their own registration.
- **(e) A fixed synapse total (for example, W ≥ 5).** It scales with lobe size and with the
  number of neurons of each type, so it would treat R1–R6 (2,265 against 1,112) differently in
  the two lobes. Rejected.

## 6. Reading the weights in chunks

The full read was killed at 18.1 GB (backlog, Johnny). The builder never materialises the weights
table.

1. **Annotations first** (14.5 MB, read whole). They give a lookup from `bodyId` to (placed type
   index, lobe) for the placed bodies only: a sorted `int64` array of their body ids with parallel
   arrays of type index and lobe.
2. **Weights by record batch.** `pyarrow.ipc.open_file` on `pyarrow.memory_map` reads batches
   `0 … num_record_batches − 1` one at a time. For each batch, the builder takes the three columns
   as numpy arrays, maps both ends with `np.searchsorted` on the lookup, and keeps the rows with both
   ends placed. It drops `body_pre == body_post` and counts those. It routes each kept row by (type
   pair, lobe pair):
   - same lobe, **outside-block** type pair → the outside accumulators `W[w_min][ℓ][s, t]`, one per
     `w_min` ∈ {1, 2, 3}, with `np.add.at` on 55 × 55 arrays;
   - same lobe, **block** type pair → the block accumulators, which are written only to the sealed
     file (§9);
   - across lobes → a cross-lobe accumulator per outside type pair (diagnostic), and the
     lobe-consistency sums of §4. Cross-lobe rows of block type pairs enter no bank and no printed
     number; their total weight is written only into the sealed files (§9).
3. **Checks on the stream:** the rows read must sum to 151,856,684, the pandas metadata `stop`
   ("ROW COUNT DIFFERS"). The batches read must equal `num_record_batches`. Duplicate
   (`body_pre`, `body_post`) keys among kept **outside** rows are counted and printed (a sort of the
   kept rows, which are few). The build stops on any duplicate key among kept block rows, with a
   message that carries no number.
4. **Memory:** peak resident memory is recorded (psutil, in the builder's environment) and the
   build stops above a registered cap of **4 GiB** ("MEMORY CAP"). The cap is a guard against a
   repeat of the 18.1 GB read, not a measured budget. A batch of 65,536 rows is about 1.5 MB of
   `int64` data before any compression, and the accumulators are a few 55 × 55 arrays. **Peak use
   was not measured**, and the machine's RAM was not read for this draft.
5. **Equality test (fixture):** on a synthetic feather written with small record batches, the
   chunked path and a whole-table `pandas` groupby must give identical `W` arrays.

**No GPU.** The build fits nothing. It is one read of 1.05 GB with integer sums, bounded by
reading, not arithmetic. **Cost: not timed.**

## 7. What the male bank contains (proposal, D8)

**An existence bank.** For each present cell `(s, t)` of a lobe, one row
`src, tar, du=0, dv=0, n_syn=x_ℓ(s, t), sign=+1`.

- **Offsets:** there is no column assignment for T4/T5 (backlog), so no offset set is built. The
  `(0, 0)` row is a placeholder and not an autapse claim. The same-body rows were dropped in §6.
- **Sign:** a placeholder +1, as in the FlyWire builder (`PLACEHOLDER_SIGN = 1`). No EM volume
  measures sign.
- **Hull fill:** none.
- **What the arm can read from it:** existence only. The knockout test decides on existence
  (knockout registration D7). Its printed offsets, counts and sign would be **meaningless** on this
  bank, and the arm's registration must say so.
- **Not verified:** that `knockout_regrow.py`, rule #2.1's `fit` and the harness's `score` run on a
  bank whose every cell has the single offset `(0, 0)`. That is checked by the arm's registration,
  which owns the loader.

## 8. What changes between flyvis-65 and the male CNS bank (named)

| | flyvis-65 (primary) | male CNS bank (this builder) |
|---|---|---|
| animals | **at least two females**: FIB-25 (Canton-S) and FIB-19 (w1118 × Canton-S), plus a hand-built lamina model ([where our bank comes from §1](../notes/2026-09-23-where-our-bank-comes-from.md)) | **one male** (Berg et al. 2026); the same specimen as the male optic lobe v1.1 (ibid. §5.2) |
| merge across animals | per (s, t, offset), **the larger of the two estimates** (eq. 7) | **none**: one animal |
| averaging | **column-averaged** mean synapses per target neuron **per offset**, tiled on a hex lattice | **no column averaging, no offsets**: one mean per type pair over all target neurons of the lobe (`x`, §5.1). The per-target normalisation remains; the per-offset, per-column template does not |
| pruning | per offset, mean < 1 dropped (eq. 8); rows below 1 re-added by hand edits on T4/T5/TmY15 targets | per type pair, `x < c*` absent (§5.2); no hand edits |
| hull fill | yes (238 `hull_filled` rows, not scored) | none |
| lobes | one template (FIB-19 is a right eye) | **two banks, left and right** (§4) |
| scope | optic-lobe volumes, 65 model types | **whole CNS** release; restricted to 55 placed types; synapses counted wherever they lie (CT1's two compartments summed) |
| types | 65, CT1 split into two compartments, R1–R6 six types | 55 placed; R1–R6 one index; CT1 one index; Mi3, Mi11, Mi12, Tm28 absent; TmY9 → TmY9q flagged |
| typing | flyvis's (from the EM papers) | Janelia's `type` column; three overrides from `flywireType` (§3.1) |
| synapse detection | FIB-SEM, two volumes (8 and 10 nm) | the release at confidence ≥ 0.5; imaging method of the male CNS **not read** for this draft |
| content | existence, offsets, counts, sign | existence only (§7) |

**Reading, already fixed by the knockout registration (§8 and D13 there):** "R on the male CNS
only = a flag to re-examine both fits". (The drafting brief cited this as "§3.7/D13". In the
committed file it is §8, with its vote as D13 in §10. §3.7 there is the seed table.) Every row
above is a reason why the two banks can differ without any difference in grammar. A difference in
verdict measures all of them together
([where our bank comes from §5.3](../notes/2026-09-23-where-our-bank-comes-from.md), "A confound
no second bank removes").

## 9. Block A is sealed (proposal, D10)

**Rule.** The 64 block cells of each built bank are **not read** until the knockout male-CNS arm's
own registration has been reviewed and Mike has given his word. "Read" means: opened, printed,
loaded, counted, summarised, plotted or diffed, by a person or an agent. **The only permitted
operation is computing its sha256.**

**How the builder keeps it:**

- Per lobe, the block cells go to their own file, `male_cns_<lobe>_blockA.sealed.csv`. It holds
  **all 64 rows** (present or not), with `src, tar, W, n_tar, x, present`, so that the file's
  length says nothing about presence. The bank file of §7 holds the outside cells only.
- Nothing the builder prints or writes, apart from the sealed files, is computed from a block
  row. The manifest names the sealed files with their sha256 and byte size, and nothing else about
  them.
- The male-CNS arm's script is the first code allowed to read the sealed files, and it does so in
  its registered real run only.
- **If the rule is broken,** the break is recorded in that registration's error ledger, and the
  arm's verdict carries the note "block A of the male CNS was read before its registration was
  reviewed".

**The blindness test (fixture; a test that separates both worlds).** Two synthetic datasets that
are identical except for their block-A rows (a perfect board in one, a random pattern with the
same totals in the other) are built by the builder. Their stdout and their manifests must be
byte-identical, except for the sealed files' sha256 and byte size. The sealed files themselves must
differ. If any printed or written line depends on a block row, the test fails. This is the
builder's version of knockout machine check 6 ("BLOCK LEAKS INTO TRAINING").

## 10. Outputs, pins, environment and modes

### 10.1 Files

- **Builder:** `results/genome/c6/checks/male_cns_bank_builder.py`. **Tests:**
  `results/genome/c6/checks/test_male_cns_bank_builder.py`. Both are committed with this
  registration, after review.
- **Private outputs** (outside the repository; proposal D11), in
  `connectome-seed-data/Janelia/derived/male_cns_v1_<UTC stamp>_<first 12 characters of git head>/`:
  - `male_cns_R_outside.csv`, `male_cns_L_outside.csv`: the §7 format, outside cells only,
    present rows;
  - `male_cns_R_blockA.sealed.csv`, `male_cns_L_blockA.sealed.csv`: §9;
  - `pair_stats_outside.csv`: every outside cell of both lobes with `W` (for each `w_min`),
    `n_tar`, `x`, present at `c*`, and cross-lobe weight;
  - `bank.meta.json`: the manifest (§10.2);
  - `BUILD.md`: the printed report;
  - `SHA256SUMS.txt`: every file above.
- **Committed after the build** (on Mike's word): `results/genome/c6/checks/male_cns_bank/BUILD.md`
  and `bank.meta.json`, copies of the two private files. They hold aggregates, outside-block only,
  and hashes. The knockout registration is then amended to pin the four bank files' sha256 (its §8).

### 10.2 The manifest records

The registration path and its sha256; the git head and a dirty-tree listing; the builder's sha256;
each input's name, size, sha256 and download date (§1.1); the Python, numpy, pandas, pyarrow and
psutil versions actually used; the type map as applied, with the per-type per-lobe body counts
under both name columns; the side-rule counts per type (by `somaSide`, `rootSide`, `instance`,
unassigned); the lobe-consistency shares; T, K, `w_min`, `c*`, the tie excess or shortfall;
the diagnostic table of §5.4; rows read, batches read, autapse rows dropped, duplicate outside
keys, cross-lobe weight; peak memory and runtime; and each output file's sha256 (the sealed files
by hash and size only).

### 10.3 Modes

- **`--self-test`**: runs the fixture tests (§11) and reads no real data.
- **`--inspect-only`** (the dry run): checks the pins, reads the weight file's **schema and
  metadata only**, reads the annotations, applies the map and the side rule, runs the §3.3
  self-test, and prints the per-type counts. **It reads no weight column.** Its output is what the
  reviewers use to confirm the exact map strings (§3.2) before the build. A string that differs
  from the registered map sends the map back to review. It is not patched.
- **(no flag)**: the build. It refuses on a dirty tree under `results/genome/c6/` or
  `docs/plans/` unless `--allow-dirty` is given, and a build made with `--allow-dirty` is marked
  "NOT THE REGISTERED BUILD" in its manifest and `BUILD.md` (as `knockout_regrow.py` marks its runs).
  It refuses an existing output folder.

### 10.4 Environment

`pyarrow` must **not** be installed into `tools/.venv`, whose digest is pinned (FlyWire
registration §1, "Environment"). The builder runs in a throwaway `uv` environment, pinned to the
versions that `uv` resolved when this draft was written (observed 2026-09-25 UTC): Python 3.13.14,
numpy 2.5.3, pandas 3.0.6, pyarrow 25.0.1. psutil is to be added; its version is **not yet
pinned**.

```
uv run --no-project --python 3.13.14 --with pyarrow==25.0.1 --with numpy==2.5.3 --with pandas==3.0.6 --with psutil \
    python results/genome/c6/checks/male_cns_bank_builder.py [--self-test | --inspect-only] [--allow-dirty]
```

The builder stops if the versions it finds differ from the pins. It imports nothing from the
harness, because the harness refuses on changed pins and needs no pyarrow. It reads `types.csv` and
`offsets.csv` directly (§1.1).

### 10.5 Order of work

1. This registration is reviewed by Ark, Johnny and Zcode, and Mike gives his word. The builder
   and tests are written against it, `--self-test` passes, and everything is committed.
2. `--inspect-only` on the real files (annotations and schema only). The reviewers confirm the map
   strings and read the per-lobe body counts.
3. The build, on Mike's word. It writes the private outputs and prints `c*` and the outside-block
   diagnostics. The sealed files stay sealed.
4. The male-CNS arm's registration is drafted with the outside-block tables in hand (knockout
   §8: "Printed before its data"). After its review, the knockout registration is amended with the
   four pins, and the arm's script is the first to read the sealed files.

## 11. Tests (fixtures only; no real data)

1. **Blindness** (§9): two worlds differing only in block rows give identical prints and manifests
   except the sealed hashes, and different sealed files.
2. **Flip** (§4): a fixture where CT1's side label is opposite to its partners' passes with
   `FLIP = {CT1}` and stops without it. A fixture where it is not opposite stops with the flip.
3. **Zero matches:** a fixture with the canonical column renamed stops with "ZERO NAME MATCHES".
   A fixture with one placed type removed from one lobe stops with "TYPE WITH NO CELLS".
4. **Chunked equals whole** (§6.5).
5. **Density rule:** on a hand-made `x` table with known order, `c*`, the tie excess and the
   shortfall case come out as §5.2 states. T and K for the registered grid equal §5.3.
6. **Row count:** a fixture whose metadata `stop` differs from its rows stops with "ROW COUNT
   DIFFERS".
7. **One index per population:** R2–R6 and CT1(Lo1) never appear in the bank files, and R1 and
   CT1(M10) carry the pooled populations.

## 12. What this builder cannot show, and what it hands on

- **Whether block A is a board on the male CNS.** Knockout machine check 3 (32 present, 16 + 16,
  no cross) is the flyvis-65 count. For this arm it is set by the builder's threshold (knockout
  §8), so the arm's registration must decide what replaces it, **without reading the sealed files
  first**.
- **The 32/32 lattice.** Several knockout constants assume 32 present and 32 absent block cells
  (`smallest_passing_auc` by board, `TAU`'s inertness; knockout §3.2–§3.3). A male block with
  another count needs those re-derived in the arm's registration.
- **Its own synthetic worlds.** Knockout §8 proposes rebuilding the §3.6 worlds on the male bank's
  degree terms, "decided with the builder". **Handed on (D13):** it is the arm's decision, because
  it is a property of the instrument on this bank, not of the bank.
- **The L/R reading (D12)** is proposed in §4 and decided in the arm's registration.
- **Types typed by connectivity.** If the male CNS's T4/T5 or Tm/Mi labels lean on connectivity,
  part of block A may be true by definition (candidates note, risk 2). This is not checked here.

## 13. Decisions for review (reviewers, then Mike)

Each item says what its options change and gives a recommendation. The body is written with the
recommendation.

| # | question | options (what each changes) | recommendation |
|---|---|---|---|
| **D1** | The pair threshold `c` on `x = W / n_tar` | (a) fixed `c = 1`: set without male data, but it is the value already known to give a perfect male board, so choosing it is selection with knowledge of block A. (b) **match flyvis-65's outside-block density, pooled over both lobes** (§5.2): output depends on outside cells only; same density as the primary arm; one cut for both lobes. (c) the same, per lobe: equal densities, but the within-animal null then compares two cuts. (d) degree-sequence match: closer to what N1 sees; needs a distance and a search of its own. (e) fixed synapse total: scales with lobe size and type counts; rejected. | **(b)**, with (a), (c), 0.5 and 2 printed beside it (§5.4) |
| **D2** | Minimum weight of a neuron pair, `w_min` | 1: keep everything the release keeps at confidence 0.5. 2 or 3: drops the 62 % of weight-1 edges (or more), the FlyWire builder's starting choice. Under D1 (b), `c*` adapts, so this changes which cells pass, not how many. | **1**, with 2 and 3 printed |
| **D3** | The canonical name column | (i) **`type`, with a closed override table of three names** (R7, R8 roll-ups and TmY9q from `flywireType`): the animal's own typing, and the one the reviewed counts appear to use. (ii) `flywireType` everywhere: one column, no overrides, but labels carried over from a female FlyWire fly, 21,350 more nulls overall, and T4d counted 1,710 instead of 1,709. (iii) keep a body only where both columns agree: strictest, and it drops bodies for reasons no one has read. | **(i)** |
| **D4** | A population that flyvis splits into several types (R1–R6; CT1's two compartments) | (a) **one grid index per population** (R1; CT1(M10); the index is the birth-id-first name): 55 types; no duplicated rows. (b) the population at every flyvis index: 61 types, but six identical R rows and columns and two identical CT1 rows, which is structure flyvis-65 does not have. (c) split CT1 by region: needs a region-level download that is not in `connectome-seed-data/Janelia/`. | **(a)** |
| **D5** | TmY9 | (i) **map to `TmY9q`, flagged** (the review's map; outside block A). (ii) leave TmY9 out (54 types). | **(i)** |
| **D6** | Side and lobe | (i) **`somaSide` → `rootSide` → `instance` suffix; declared flip set {CT1}; the lobe-consistency check stops a wrong assignment** (§4). (ii) the lobe of every body from the majority side of its partners: automatic, but connectivity then assigns sides, and the flip is no longer a declared, checkable fact. | **(i)** |
| **D7** | Which bodies count | (i) **every body whose canonical value maps, whatever its `status`**; per-type status breakdown printed. (ii) `status == Traced` only: cleaner bodies, but it changes `n_tar` and so `x`, by amounts no one has read. | **(i)** |
| **D8** | Bank content | (i) **existence bank: one `(0, 0)` row per present pair, `n_syn = x`, sign +1** (§7). (ii) real offsets for types with `assignedOlHex1/2`, and pair rows for the rest: a mixed bank whose offset field means two things; T4/T5 have no hex (backlog). | **(i)** |
| **D9** | One cut for both lobes | (i) **one `c*` from the pooled lobes**: same cut, so a lobe difference is the animal's. (ii) `c*_ℓ` per lobe: equal densities, different cuts. | **(i)**, (ii) printed |
| **D10** | Block A sealed | (i) **a separate sealed file per lobe, 64 rows each, never read before the arm's review; blindness test** (§9). (ii) one bank file with a do-not-read rule: simpler, but any look at the bank shows the block. | **(i)** |
| **D11** | Where the banks live | (i) **outside the repository; the manifest and `BUILD.md` committed**, as for FlyWire. (ii) commit the outside bank files too (CC-BY allows it, per `SOURCE.md`): easier to reuse, but the committed tree would then hold per-pair male data, and the sealed files must stay outside anyway. | **(i)** |
| **D12** | The L/R reading (**handed to the arm's registration**) | (i) R on the male CNS needs R in both lobes; a disagreement reads "within-animal variation", not averaging. (ii) the right lobe primary (the side of FIB-19 and of the male optic lobe v1.1), the left lobe the null. | **(i)** as a proposal there |
| **D13** | Synthetic worlds on the male bank (**handed to the arm's registration**) | knockout §8: "decided with the builder". It is a property of the instrument on this bank. | decide in the arm's registration |
| **D14** | File date | `2026-09-26-…` (as requested; the local day) vs `2026-09-25-…` (the UTC day of drafting, per GLOSSARY) | rename to `2026-09-25-…` before commit, as knockout D12 did |

## 14. Not verified at drafting

- Which of `somaSide`, `rootSide` and the `instance` suffix carries the side for R1–R8, CT1 and
  the 16 block types; the exact strings of R1–R6, the R7/R8 roll-ups, `CT1`, `Am1` and `TmY9q`
  in their columns (§3.2). Settled by the dry run.
- That Am → Am1 is the backlog's 61st mapped type (§3.2; inferred from arithmetic).
- The backlog's counts (61 of 65, 49 by name, 62 % weight-1 edges, the 18.1 GB read), the
  review's counts (T4d 1,709 / 1,710; R7/R8 1,300 / 1,329; 931 `_unclear`; R1–R6 2,265 / 1,112;
  CT1 and Am1 n = 1 per lobe; CT1_L's 100 %) and Zcode's preliminary block views. All are quoted
  from the backlog or the knockout registration §8, not recounted.
- The weight file's batch sizes, compression codec, key uniqueness and autapse rows (§1.2).
- Peak memory and runtime of the build (§6).
- That the knockout script, rule #2.1 and the harness run on an existence bank with `(0, 0)`
  offsets only (§7).
- The imaging method and synapse-detection details of the male CNS release; the chat of
  2026-09-25 19:58–20:02 UTC, which is quoted as relayed in the drafting brief.

## 15. Sources

- Backlog entry `THE-MALE-CNS-BANK-NEEDS-A-REGISTERED-BUILDER-WITH-ITS-PAIR-THRESHOLD-FIXED-BEFORE-DATA`
  (`backlog.md`, line 28).
- [`2026-09-24-knockout-regrow-registration.md`](2026-09-24-knockout-regrow-registration.md),
  revision 3.4.1: §1 (bank, block, removal, pre-data tables), §3.4 (machine checks), §7, §8, §10
  (D13).
- [`docs/notes/2026-09-23-where-our-bank-comes-from.md`](../notes/2026-09-23-where-our-bank-comes-from.md)
  §1–§3, §5.
- [`docs/notes/2026-09-25-knockout-block-candidates.md`](../notes/2026-09-25-knockout-block-candidates.md).
- [`docs/decisions/005-backward-before-forward.md`](../decisions/005-backward-before-forward.md),
  with its amendment of 2026-09-24.
- [`GLOSSARY.md`](../../GLOSSARY.md) §1–§2.
- `results/genome/c6/harness.py` (bank loading, `Bank`, `make_view`, `fit_bf`);
  `results/genome/c6/checks/flywire_bank_builder.py`; `results/genome/c6/checks/flywire_bf_p3.py`
  (`restrict_to_30_grid`, `load_flywire_bank`); `results/genome/c6/checks/knockout_regrow.py`
  (`check_board`, `pre_data_tables`).
- [`2026-09-24-flywire-bf-p3-registration.md`](2026-09-24-flywire-bf-p3-registration.md) §1, §3b.
- Commit `1ed55ec` and `docs/notes/2026-09-26-knockout-regrow-blind-review.md` (the flyvis-65
  verdict, §0 only).
- `connectome-seed-data/Janelia/SOURCE.md`, `SHA256SUMS.txt`, and the two feather files' schemas
  and metadata (§1.2).
