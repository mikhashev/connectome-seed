---
**Status (revision 2.1, 2026-09-26 UTC): the reviewers' edits after the `--inspect-only` output.
Not re-reviewed, not committed, the build not run.** The inspect-only output
(`results/genome/c6/checks/male_cns_bank_builder_inspect_only.txt`, commit `2af21e5`) was
reviewed in the DPC Research chat on 2026-09-26 by Johnny (08:10 UTC), Zcode (08:11 UTC) and Ark
(08:19 UTC), all "yes, with edits", before the build (§13.4). The edits, who asked for each, and
where each lives are in §13.3. What revision 2.1 changes, in short: the left/right reading of §4
is restated in its measured form (the whole left lobe is not less complete; the deficit is
specific to R1–R6), with an expectation handed to the arm (§4, §12); the photoreceptor side is
named a transfer through `rootSide` (§1.2, §4); `R1-R6` / `R1-6` are named as two spellings of
one object (§3.1); an R7/R8 side control independent of `flywireType` is added (§4);
`assignedOlHex1/2` are shown to be column coordinates that cannot carry a side (§1.2, §4); the
codec is read from the record batch headers (§1.2, §6); and the instrument's edits (a–g of
§13.3) change the inspect header, the dirty-tree rule, the blindness test, three stop messages,
the environment field and the lobe-consistency print (§6, §9, §10, §11). **The type map, the
side rule, D1–D15 and the density target are unchanged.** New numbers in revision 2.1 are
annotation counts and IPC header fields only (a scratch script and the builder's own functions,
2026-09-26 UTC; no weight value was read). Revision 2's header follows.

**Status (revision 2, 2026-09-26 UTC): the reviewers' pass on revision 1. Not re-reviewed, not
committed, nothing built.** Revision 1 (commit `d6e3759`) was reviewed in the DPC Research chat on
2026-09-26 by Johnny (04:57 UTC), Ark (05:00 UTC) and Zcode (05:08 UTC), all "yes, with edits".
The eleven edits, who asked for each, and where each lives are in §13.2. What revision 2
changes, in short: the harness grid is an explicit obligation of the male arm (§7, §12); two
densities are named and the rationale of D1 is corrected (§5.2); the collapse of flyvis-65 onto
the placed grid is a decision (D15, §5.3); the c = 1 fact is corrected (§0, §5.5); the lobe
reading has two explanations (§4); the order map → T → threshold is fixed (§5.2); D2 says what
`w_min` changes; `rc_patterns` needs an attempt cap in the arm (§12); the sealed files' size is
not printed and their `w_min` is named (§9); the side parser and the birth-id sort are specified
(§3.2, §4); the file is renamed to its UTC day (D14 closed). **Revision 2 read no male CNS data.**
Its only new numbers are flyvis-65 counts on the placed grid under two collapses (§5.3). They were
computed from `offsets.csv` and `types.csv` with block A excluded by name before counting. The
line numbers it cites in `harness.py`, `flywire_bf_p3.py` and `knockout_regrow.py` were read at
commit `d6e3759`. Revision 1's header follows.

**Status (revision 1, drafted 2026-09-25 20:10–21:00 UTC; 2026-09-26 local, +07:00): draft for
review. Not reviewed, not committed, nothing built.** Drafted by a CC subagent on Mike's word in
the DPC Research chat, 2026-09-25 20:02 UTC: "do the male CNS builder". The seven points it must
fix were agreed in the chat at 19:58–20:01 UTC by Ark, Zcode and CC (as relayed in the drafting
brief; the chat is not in the repository). The design choices that need a vote are marked
**proposal** in the body and listed in §13. The body is written with the recommended option, so
the draft is complete as it stands.

**File date.** Revision 1 was named `2026-09-26-…`, the local day. The UTC clock read
2026-09-25 20:10 UTC when drafting began (`date -u`), so the
[glossary's date-time convention](../../GLOSSARY.md) dates it `2026-09-25-…`. **Revision 2
renames it** (`git mv`; the reviewers agreed, D14 closed). No other file of the repository named
the old path (checked with `grep` at the rename).

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
  `THE-MALE-CNS-BANK-NEEDS-A-REGISTERED-BUILDER-…`). **Revision 2 corrects what was seen (Zcode,
  2026-09-26 05:08 UTC, as relayed).** The perfect board with 4 mirror cells came from a
  **summed** threshold, a total of about 500–800 synapses per type pair, that was mislabelled
  "mean ≥ 1". **At an honest mean ≥ 1 (c = 1 in §5.1) the male block had 20–21 weak cross cells,
  with means of 1.0–2.2: not a perfect board.** Other definitions also gave 52–54 mirror cells.
  The committed files still carry the old label: the backlog says "total/n_tar >= 1 (about sum
  >= 850)", and knockout registration §8 says "at least 1, which is about a sum of 850 or more".
  This draft does not edit them. The correction rests on Zcode's word in the chat and is **not
  verified from any file** (§14).
- **Block A was inferable 64/64 at every threshold tried** (Zcode, preliminary graph; knockout
  registration §1.4, the inferability table: "64 / 64 at every pair threshold tried"; backlog
  entry: "block A inferable 64/64 in both lobes at every threshold Zcode tried"). So no threshold
  tried starves an endpoint of block A.
- **The people choosing D1 have seen block A at c = 1 and at a summed threshold.** The
  recommended rule (§5.2) is a function of outside-block cells and of flyvis-65 only, so its
  output does not depend on that knowledge. The choice *of the rule* is still made by people who
  have that knowledge, and this is recorded, not removed.
- Zcode's thresholds and definitions from the preliminary graph are **not written in any file
  this draft opened.** They are not reproduced here beyond the relayed words above.

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
`VCH_R`) and `somaSide` equal to that suffix. At revision 2, the following were **not checked**:
which of `somaSide`, `rootSide` and the `instance` suffix is filled for the 16 block types, for
R1–R6, R7, R8 and CT1; how many bodies each type has; whether `assignedOlHex1/2` is null for
T4/T5; the compression codec of either file; whether (`body_pre`, `body_post`) is unique; and
whether rows with `body_pre == body_post` exist. Uniqueness and autapses need the weight stream
(§6) and remain open.

**Settled by the inspect-only output (commit `2af21e5`) and revision 2.1 (annotations and IPC
headers only).**

- **Which column carries the side.** Every placed type except the photoreceptors takes its side
  from `somaSide` alone (the inspect table, §3.2). The photoreceptors take it from `rootSide`:
  R1–R6 `somaSide` 4 L / 9 R, `rootSide` 1,108 L / 2,256 R; R7 `somaSide` 1 / 1, `rootSide`
  607 / 691; R8 `somaSide` 14 / 0, `rootSide` 611 / 704. For all three the `instance` step
  assigns 0 / 0 and 0 bodies are unassigned. **So trust in the photoreceptor side is a transfer,
  not a measurement:** it rests on `rootSide` meaning the lobe for these cells as `somaSide`
  does for the others, and nothing in this file measures that. The lobe-consistency check (§4)
  is the first test of it; it needs the weight pass.
- **`assignedOlHex1/2` (revision 2.1; Ark proposed it as an independent lobe carrier).** Both are
  doubles that hold integers, 1–36 and 1–39. They are non-null for 23,720 bodies, all
  `superclass == ol_intrinsic`, in 15 types (L1, L2, L3, L5, C2, C3, T1, Mi1, Mi4, Mi9, Tm1, Tm2,
  Tm4, Tm9, Tm20; none of R1–R8, T4, T5 or CT1). Neither column has field metadata, and
  `SOURCE.md` says nothing about them. The pair (`assignedOlHex1`, `assignedOlHex2`) is one
  value per body per lobe (Mi1: 875 distinct pairs for 875 left bodies with a hex, 886 for 887
  right), and **the two lobes use the same coordinates**: all 879 pairs seen on the left also
  occur on the right (the right has 13 more). The best single threshold on either column
  predicts the side of a hex body with accuracy 0.5593, which is the share of right bodies among
  them (13,267 / 23,720). So these are **hex column coordinates within a lobe, not a side**, and
  they cannot carry the lobe. **No check is built on them.**
- **The compression codec (revision 2.1; Ark voted against deferring it).** Read from the
  flatbuffer headers only (§6): the weight file's 2,318 record batches are all `LZ4_FRAME`, and
  their header row lengths sum to 151,856,684, equal to the pandas metadata `stop`. The
  annotation file's 4 record batches are `LZ4_FRAME` too (211,577 rows).

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
- **The grid is fixed at 65 × 65 in the harness (revision 2; Johnny, Ark).** `NAMES` comes from
  `types.csv`, sorted by birth id, with `assert len(NAMES) == 65` (`harness.py:119-123`).
  `ALL_CELLS` is every `(s, t)` in `range(65)²` (`:154`). `Bank.exists` is a 65 × 65 array
  (`:163-166`). A bank on fewer types is therefore still a 65 × 65 bank whose unplaced rows and
  columns are empty. The cells an arm uses are restricted by replacing `H.ALL_CELLS`, as
  `flywire_bf_p3.py:74-76` (`restrict_to_30_grid`) does, leaving `FOLD`, `TYPE_FIELDS`,
  `PAIR_ID`, `NAMES` and `IDX` untouched. **This is an obligation of the male arm's registration,
  not of the builder** (§7, §12). No harness edit and no pin change are proposed here.
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

**What the two columns say about the photoreceptors (revision 2.1; Johnny, Zcode).**

- **`type = 'R1-R6'` and `flywireType = 'R1-6'` are two spellings of one object.** Both select
  3,377 bodies, and they are the same bodyIds (symmetric difference 0; checked in revision 2.1,
  and printed by `--inspect-only` from revision 2.1 on). The inspect line of commit `2af21e5`,
  "R1 … under flywireType [0, 0]; disagree 3377", is therefore a string artefact: it looks up
  `R1-R6` in `flywireType`, where the object is spelled `R1-6`. It is not an absence.
- **`flywireType` alone would cover R1–R6, R7 and R8.** `R1-6`, `R7` (1,300 bodies) and `R8`
  (1,329) are ready populations there, and they are the same bodies that `type` holds as
  `R1-R6`, as `R7d` + `R7p` + `R7y` + `R7_unclear` and as `R8d` + `R8p` + `R8y` + `R8_unclear` (§4).
  So, for the photoreceptors, the D3 mix of columns is redundant: it selects the same bodies as
  either column would. **The map is not changed** (same bodies); the redundancy is named. It
  does not extend to the whole map: under `flywireType`, four placed types carry another name
  (`Tm5Y` is `Tm5f`, 898 bodies; `TmY18` is `Tm27`, 1,367; `TmY13` is `TmY11`, 432; `Tm30` is
  `Tm31`, 124), and TmY9's `TmY9q` is `TmY9b` in `type` (515). `--inspect-only` prints these
  pairs from revision 2.1 on.
- **`R1-R6` is an aggregate label, and the status column marks it.** 1,983 of its 3,377 bodies
  (59 %) have a null `status`, and 1,982 of those carry `statusLabel = 'Out of scope'` (the
  other one has a null `statusLabel`). No other read type has a null status except **L4, with
  one body**: bodyId 136673, `somaSide` L, `instance` `L4_L`, `statusLabel` `Out of scope`.
  R7 and R8 have none (R7 has one `Anchor`; everything else is `Traced`). In the whole file,
  `statusLabel = 'Out of scope'` occurs only with a null status (4,585 bodies: 2,601 without a
  `type`, 1,982 `R1-R6`, one L4, one `Lai`). Under D7 (i) every mapped body counts whatever its
  status, so this changes no body count; it is recorded because it bears on the R1–R6 asymmetry
  (§4).

### 3.2 The map, 65 → placed types (proposal, D4)

| group | flyvis names | male CNS | placed at grid index | count |
|---|---|---|---|---|
| by name | the 49 names not listed below (the 16 block names among them) | same string in `type` | own index | 49 |
| renamed | Am | `Am1` in `type` | Am | 1 |
| one population, six flyvis types | R1, R2, R3, R4, R5, R6 | the R1–R6 type in `type`: `R1-R6` (read in the dry run of commit `2af21e5`; spelled `R1-6` in `flywireType`, §3.1) | **R1 only**; R2–R6 not placed | 1 placed (6 mapped) |
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
  1). **The index kept is the flyvis name whose birth id sorts first.** The birth id is the
  `birth_id` column of `types.csv`: the first 12 hex digits of sha256 of
  `cs-birth-v1|type|<name>` (`harness.id_hex`; the harness asserts the column equals it). The
  sort is ascending on the 12-character lowercase hex string, which for strings of equal length
  is the numeric order. So the population's index is also the lowest harness index among its
  names, since the harness indexes types in birth-id order (`harness.py:120`). This gives R1
  (`9654b247b494`; R2–R6 are `b075…`, `a935…`, `d54d…`, `bf13…`, `ef2d…`) and CT1(M10)
  (`63667a4a1a53`, before CT1(Lo1)'s `7c280b5b9f34`). The rule reads no data. The two CT1
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
breakdown of `status`. **From revision 2.1 also:** the value pairs on which the two columns
disagree (so that a second spelling shows as such, §3.1); the status per lobe of every type with
any status other than `Traced`; the whole file's status by side; the R7/R8 side control and the
`R1-R6` / `R1-6` body identity (§4, §3.1). These are annotation counts, not connectivity.

## 4. Left and right: two banks (proposal, D6; the within-animal null)

**Side of a body (in this order):** `somaSide` if it is `L` or `R`; otherwise `rootSide` if it is
`L` or `R`; otherwise the `_L` / `_R` suffix of `instance`; otherwise **unassigned**. `M`,
`unknown` and null do not assign. **The suffix parser (revision 2; Zcode):** the `instance`
string, unchanged (no strip, no case change), must end with exactly `_L` or `_R`, that is, match
the regular expression `_(L|R)\Z`; the side is the captured letter. Anything else is no suffix:
a null `instance`, a string ending in any other way (for example `_L_1`, `(L)` or a lowercase
`_l`), or a string equal to `_L` or `_R` alone. The fixture tests include each of these cases.
The first three rows of the file show the pattern (`DNp01(GF)_R`, `OCG01d_L`, `VCH_R`, §1.2).
Unassigned bodies are left out and counted per type. The fallback order exists because
optic-lobe sensory cells may have no `somaSide` (their somata lie outside the brain). **Checked
(inspect output, commit `2af21e5`; revision 2.1):** for R1–R8 it is so. R1–R6 takes its side
from `somaSide` for 4 L / 9 R bodies and from `rootSide` for 1,108 L / 2,256 R; R7 from
`somaSide` 1 / 1 and `rootSide` 607 / 691; R8 from `somaSide` 14 / 0 and `rootSide` 611 / 704.
No body of a placed type reaches the `instance` step, and none is unassigned. Every other placed
type takes its side from `somaSide` alone. **The photoreceptor side is therefore a transfer, not
a measurement** (§1.2): it trusts `rootSide` to mean the lobe. Across the whole file, the
`instance` step assigns a side to 16 L / 15 R `Traced` bodies, none of a placed type.

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
types, only their outside-block pairs enter the share. **Revision 2.1 (Ark):** beside each share
the build prints the inconsistencies themselves, per type, whether the check passes or stops:
the neuron-pair rows whose partner is in the other lobe, of all the type's rows, as source and
as target, and their weight. They are counted on the same outside-block rows as the share, so no
block-A pair enters them.

**No second lobe carrier is available in this file (revision 2.1).** Ark proposed
`assignedOlHex1` as an independent carrier of the lobe, to check the side rule. It is a hex
column coordinate within a lobe, and the two lobes use the same coordinates (§1.2), so it cannot
carry a side, and no check is built on it. The side rule is checked only by the lobe-consistency
check above.

**R7/R8 sides, independent of `flywireType` (revision 2.1; Ark).** The R7 and R8 roll-ups are
read from `flywireType` (§3.1). Their sides are recounted from the `type` variants: R7 =
`R7d` + `R7p` + `R7y` + `R7_unclear` (82 + 332 + 482 + 404), R8 = `R8d` + `R8p` + `R8y` +
`R8_unclear` (76 + 330 + 481 + 442). `R7R8_unclear` (85 bodies) was to be split by its
`flywireType`; all 85 have a null `flywireType`, so it enters neither. Result: the variant sets are
**the same bodies** as `flywireType = 'R7'` and `'R8'` (symmetric difference 0 for both), and give
the same sides, **R7 608 L / 692 R and R8 625 L / 704 R**. Johnny's R7/R8 numbers do not depend on
the column. `--inspect-only` prints this control from revision 2.1 on.

**Two banks.** Each lobe's bank is built from neuron pairs whose two bodies are both assigned to
that lobe. A pair across lobes enters neither bank. Its weight is counted per outside type pair and
printed as a diagnostic. **The same threshold `c*` is applied to both lobes** (D9, §5.2). So the
two banks share the animal, the pipeline and the cut. **They do not share a density:** `c*` is
set on the pooled lobes, so each lobe's outside density differs from T by whatever the two lobes
differ, by construction. Both densities are printed.

**Reading (handed to the arm's registration, D12; revised in revision 2, Johnny and Ark).** A
disagreement between the lobes, for example R in one and G in the other, is not averaging, since
neither bank averages over animals or columns. **It has two explanations that this builder cannot
separate:**

1. **Variation within the animal:** the two lobes of one fly are wired differently on block A;
2. **A difference of reconstruction between the lobes, in the types that differ (restated in
   revision 2.1 in its measured form; Johnny, Ark, Zcode).** Revision 2 wrote here that "the left
   lobe may be less completely reconstructed or typed" and that "this file's own counts point
   that way". **That general form is refuted by the same file** (§13.3, the refuted claim). The
   whole file's `status == Traced` bodies by side are **81,362 L / 82,738 R (1 : 1.02)** under
   `somaSide` then `rootSide`, and 81,378 L / 82,753 R under the full side rule of this section
   (the `instance` step adds 16 L / 15 R); either way, 1 : 1.02. The deficit is **specific to
   R1–R6**: 1,112 L / 2,265 R (1 : 2.04), of which `Traced` 501 / 893 and null status
   611 / 1,372. **R7 (608 / 692, 1 : 1.14) and R8 (625 / 704, 1 : 1.13), sided by the same rule
   through the same `rootSide` step, are nearly even**, and so is every other placed type (the
   inspect table). **The mechanism is not established.** The source statement stands: the male
   optic-lobe connectome that the male CNS extends is the right optic lobe
   ([where our bank comes from §5.2](../notes/2026-09-23-where-our-bank-comes-from.md), Nern et
   al. 2025). It does not explain why everything but R1–R6 is symmetric.

**Consequence, registered as an expectation and not as a defect (revision 2.1).** The placed
index R1 carries every R1–R6 body (§3.2, D4). Its left row and column hold about half the
bodies of the right (1,112 against 2,265). `x = W / n_tar` is a mean per target neuron, so the
body count alone does not fix `x`; but a lobe with half the reconstructed R1–R6 bodies can also
hold less of their synaptic weight, and under the shared cut `c*` the **left bank is expected to
be sparser in the R1 row and column.** So the lobe comparison in R1's row and column is **not a
clean within-animal null**. What the build supplies for it (all outside block A; R1–R6 is not a
block type): K_L and K_R, the present outside cells of each lobe at `c*`, and the present cells
in R1's row and column per lobe with the lobe's body count (printed beside `c*` and written to
the manifest as `population_rows_at_c_star`, revision 2.1; CT1(M10) is printed the same way).
They are diagnostics and decide nothing. **The first question put to the
build** is how much larger the R1-row asymmetry is than the 1 : 2.04 in bodies. `c*_L < c*_R`
among the §5.4 diagnostics would read as a consequence of this asymmetry. The rule that uses it
is the arm's (§12).

**The rule that separates them is the arm's to register, before its data.** What the builder
supplies for it, all outside block A: per lobe and per placed type, the body counts; per lobe, the
outside density at `c*`; the per-lobe matched cuts `c*_L` and `c*_R` (§5.4); and the cross-lobe
weight. Revision 1's proposal, "a male-CNS R needs both lobes", stays as one ingredient. It
settles when the male CNS reads R, but it does not say which explanation a disagreement has.

**Known asymmetries (recounted from the annotation file for revision 2.1; the counts of knockout
registration §8 are reproduced).** R1–R6 has 2,265 bodies on the right and 1,112 on the left.
CT1 and Am1 have n = 1 per lobe. The whole file and every other placed type are nearly even
(explanation 2 above). The male optic-lobe connectome that the male CNS extends is the
**right** optic lobe (Nern et al. 2025); that is a statement about the source, and it does not
explain why only R1–R6 is uneven. The per-type body counts per lobe are printed in the dry run.

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
altogether. Under D1's density rule, `c*` adapts to whatever `w_min` leaves, so the number of
present outside cells stays about K. **What `w_min` changes is the composition of the cells that
pass (revision 2; Ark).** A type pair whose weight is spread over many weight-1 neuron pairs loses
most of its `W` at `w_min` = 2. A type pair carried by fewer, stronger neuron pairs keeps its `W`.
So at the same density, a different `w_min` selects different cells. `w_min` = 2 and 3 are printed as diagnostics
(§5.4). The FlyWire builder used ≥ 2 as a starting choice (`SYNAPSE_THRESHOLD = 2`,
`flywire_bank_builder.py`). Whether flyvis's source volumes applied any per-pair cut was **not
checked**.

### 5.2 The rule for D1 (proposal): match flyvis-65's outside-block density, pooled over both lobes

**Order (revision 2; Ark).** The steps run in one order: **the type map is frozen (§3), then T
is computed from it (§5.3), then the threshold is chosen (below).** T depends on the placed grid
and on the collapse (D15), so a legal change of the map changes T. A legal change is one made by a
reviewed amendment of this registration. It moves the §5.3 table in the same amendment. The
"DENSITY TARGET DIFFERS" stop compares the run's T and K with the table **for the registered map
and collapse**. It catches a map that drifted without an amendment, not a map that was changed
legally.

Let Ω be the placed cells outside block A (2,961 cells on the 55-type grid, §3.2). **Block A's
mirror cells, the transposes (target → source) of its 64 cells, all lie in Ω** (Zcode). They are
64 positions, none of them in the block, since sources and targets are disjoint (checked for this
draft), and they are read like any other outside cell. Let **T** be the share of Ω that is
present in flyvis-65 after the collapse of D15 (existence under C6: at least one non-`dropped`
row, `harness.py`). Then:

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
It reads no block cell of either bank.

**What it matches (corrected in revision 2; Ark).** It matches **flyvis-65 on the same cells**:
the male bank's density on Ω equals flyvis-65's density on Ω, the property that sets how much a
rule can see there. **It does not match the density on which the knockout instrument's synthetic
limits were measured.** Two densities must be kept apart:

| density | cells | present | value |
|---|---|---|---|
| flyvis-65, full grid outside block A: the grid of the flyvis-65 run and of its synthetic worlds (knockout §1.3, §3.6) | 4,161 | 572 | **0.137467** |
| flyvis-65 on the placed Ω, restrict-only collapse (§5.3) | 2,961 | 497 | **0.167849** |

The second is **× 1.221** the first (0.167849 / 0.137467), because the ten unplaced types are
sparse in flyvis-65. Revision 1 said this rule "works at the density on which the synthetic
limits were measured". That was wrong, and it is withdrawn. **The full-grid alternative** (D1
option (b′)): take T = 0.137467 on Ω, which gives K = round(0.137467 × 5,922) = **814**, about
**407 per lobe** (814.08 unrounded). It matches the calibration density's number, but on
different cells. Neither option carries the synthetic limits over to the male bank. Whether they
must be re-derived on the male bank is D13, the arm's.

**Which grid the arm trains and scores on is the arm's to register (handed on; revision 2, Ark).**
The two options, with their consequences:

- **2,961 placed cells** outside the block, by replacing `H.ALL_CELLS` as the FlyWire arm did
  (§2). The training density per lobe is then the lobe's density on Ω, about T.
- **4,161 cells**, the full 65 × 65 grid without the block. Then **1,200 cells** (4,225 − 3,025)
  of the ten unplaced types are in training and always absent. The rule sees ten types with no
  input and no output, and the training density per lobe falls to about K / 2 / 4,161, for
  example 497 / 4,161 ≈ 0.119. Knockout check 2's count of 4,161 training cells would still pass,
  with a different meaning.

This builder recommends the first, as the FlyWire precedent, but the choice and its
consequences are the arm's.

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
| D4 recommended, **restrict-only collapse** (D15 (i)) | 55 | 2,961 | 497 | 0.167849 | 994 |
| D4 recommended, **pooled collapse** (D15 (ii), recommended) | **55** | **2,961** | **511** | **0.172577** | **1,022** |
| D4 recommended, full-grid density on Ω (D1 (b′)) | 55 | 2,961 | — | 0.137467 | 814 |

**The collapse of flyvis-65 onto the placed grid (D15; revision 2, Zcode).** flyvis-65 has 65
types. The male bank has 55. So T needs a rule for what an unplaced flyvis type contributes:

- **(i) restrict-only:** the cells of R2–R6, CT1(Lo1), Mi3, Mi11, Mi12 and Tm28 are dropped. R1's
  row is flyvis's R1 row alone. This gives 497.
- **(ii) pooled:** the index that carries a population in the male bank carries it in flyvis-65
  too. R1's cell `(R1, t)` is present if **any** of `(R1, t)` … `(R6, t)` is present (a logical
  OR), and likewise for columns, for `(R1, R1)` from any `(Ri, Rj)`, and for CT1(M10) from CT1(Lo1)
  or CT1(M10). Mi3, Mi11, Mi12 and Tm28 are dropped as in (i). This gives **511**.

**Verified for this draft** (scratch script, outside the repository, from `offsets.csv` and
`types.csv` under the pins of §1.1). The 64 block cells were excluded by name, after the
collapse and before any count was taken. The script held flyvis-65's set of present cells in
memory, block included, and printed no number about the block (flyvis-65's block A is public
anyway: the reviewed board of knockout §0). No collapsed cell falls in the block, since neither
R1–R6 nor CT1 is a block type (checked). **Zcode's 511 (T = 0.172577, K = 1,022) is reproduced
only when both populations are pooled.** Pooling R1–R6 alone gives 498 (T = 0.168186, K = 996). The pooled row above is
therefore "R1–R6 and CT1 pooled", the rule that matches D4 (one index per population, both
populations).

**Why (ii) is recommended.** The male index R1 holds every R1–R6 body, and CT1(M10) holds the one
CT1 cell with both compartments summed (§3.2, §8). The target should describe the same objects,
so flyvis-65's R1 index should also stand for all six. Under (i), flyvis's R1 row alone stands
against the male R1–R6 population.

**The builder prints T and K under both collapses** (and the full-grid (b′) value). It uses the
one D15 registers, and it stops with "DENSITY TARGET DIFFERS" if the T and K it recomputes for the
**registered map and collapse** differ from this table (the order of §5.2).

### 5.4 Diagnostics printed beside `c*` (decide nothing; outside block A only)

For each `w_min` ∈ {1, 2, 3} and each `c` in {`c*`; `c*` under the other collapse of D15;
`c*` at the full-grid density (b′); `c*_L` and `c*_R`, each lobe matched to T on its own; 0.5;
**1, the flyvis-style convention** (a pair needs at least one synapse per target
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
  number at all. **Corrected in revision 2 (Zcode):** revision 1 said c = 1 was the threshold
  under which the block is known to be a perfect board. It is not. At an honest c = 1 the male
  block had 20–21 weak cross cells (§0). The perfect board came from a summed threshold. **c = 1
  stays demoted for the same reason as before, because it was seen:** the block's content at c = 1
  is known to the people choosing, so choosing it now would be a choice made with knowledge of
  block A. That is lesson (a) of the lessons note, selection after the data. It is printed as a
  diagnostic. (The summed threshold that gave the perfect board is not an option here: it is not
  written in any file, and it was seen too.)
- **(b) Density match on the same cells, pooled (recommended),** with T from the collapse of D15.
- **(b′) Density match at the full-grid density** T = 0.137467 on Ω, K = 814 (§5.2): the
  calibration density's number, on different cells.
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
4. **Memory (what the cap is; revision 2.1, Ark):** the quantity is the **process's peak
   working set** as psutil reports it (`peak_wset`, Windows), or the current resident set size
   where the platform reports no peak. It is probed once before the stream and once after each
   record batch, and the maximum of the probes is recorded. Both measures count the pages of the
   memory-mapped weight file that the process has touched, not only its own allocations. The
   build **stops** when that maximum is above **4 GiB** ("MEMORY CAP", which names the measure
   and the batch). **The cap limits nothing:** it does not bound the batch size (set by the
   file's record batches), any allocation or the memory map. It is a guard against a repeat of
   the 18.1 GB read, detected at most one batch late, not a measured budget. A batch of 65,536
   rows is about 1.5 MB of `int64` data before any compression, and the accumulators are a few
   55 × 55 arrays. **Peak use was not measured**, and the machine's RAM was not read for this
   draft.
5. **Equality test (fixture):** on a synthetic feather written with small record batches, the
   chunked path and a whole-table `pandas` groupby must give identical `W` arrays (and, from
   revision 2.1, identical per-type counts of cross-lobe rows).
6. **The compression codec (revision 2.1; Ark voted against deferring it).** It is named without
   decoding any value: the builder reads the file footer (Arrow `Footer.fbs`: one Block per
   record batch, with its offset, metadata length and body length), then only the metadata
   bytes of each record batch message (`Message.fbs`: a `RecordBatch` header whose optional
   `compression` table holds the codec, `LZ4_FRAME` or `ZSTD`; absent means uncompressed). No
   message body is read. `--inspect-only` and the build both print the codec count over all
   batches, the sum of the batches' header row lengths against the pandas `stop`, and any
   footer/header body-length mismatch, and the manifest records them (`weight_file_header.
   ipc_headers`). A fixture test writes the same table under `lz4`, `zstd` and no compression
   and requires the three names. On the real files (revision 2.1, headers only): the weight file
   is `LZ4_FRAME` in all 2,318 batches, whose header lengths sum to 151,856,684; the annotation
   file is `LZ4_FRAME` in its 4 batches.

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
- **The grid (revision 2; Johnny raised it as blocking, Ark showed that it is not, with a
  residue).** The bank file names only placed types, but the harness it is loaded into is 65 × 65
  (§2): `NAMES` from `types.csv` with `assert len(NAMES) == 65` (`harness.py:119-123`),
  `ALL_CELLS` over `range(65)²` (`:154`), and `Bank.exists` a 65 × 65 array (`:163-166`). So the
  male bank loads as a 65 × 65 bank with ten empty rows and columns. **Obligation of the male arm's
  registration:** it restricts the cells it uses by replacing `H.ALL_CELLS`, as
  `results/genome/c6/checks/flywire_bf_p3.py:74-76` (`restrict_to_30_grid`) does, and it states
  which grid it trains and scores on (§5.2, the 2,961 / 4,161 choice). No harness edit and no pin
  change are needed for this. The harness structures that depend on the grid are listed as open
  in §12.

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
  **all 64 rows** (present or not), with `src, tar, W, n_tar, x, present`, so that the number of
  rows says nothing about presence. The bank file of §7 holds the outside cells only.
- **`w_min` of the sealed files (revision 2; Zcode):** `W`, `x` and `present` are computed at
  the registered `w_min` (D2, 1) and the registered `c*` only. No diagnostic `w_min` or `c`
  enters them. The cross-lobe weight of block type pairs (§6) is one further line, at the same
  `w_min`.
- **No size side channel (revision 2; Zcode).** A file's byte size could leak its content through
  the number of digits written. Every field of a sealed file is therefore written at a **fixed
  width**: integers zero-padded to 12 digits, `x` in `%.6e`, `present` as `0`/`1`. So the size is
  the same for every content. The size is **not printed**, and it is **not written** in any
  manifest, private or committed, or in `BUILD.md`. Only the sha256 is. (`SHA256SUMS.txt` holds
  hashes only.)
- Nothing the builder prints or writes, apart from the sealed files, is computed from a block
  row. The manifest names the sealed files with their sha256, and nothing else about them.
- The male-CNS arm's script is the first code allowed to read the sealed files, and it does so in
  its registered real run only.
- **If the rule is broken,** the break is recorded in that registration's error ledger, and the
  arm's verdict carries the note "block A of the male CNS was read before its registration was
  reviewed".

**The blindness test (fixture; a test that separates both worlds).** Two synthetic datasets that
are identical except for their block-A rows (a perfect board in one, a random pattern with the
same totals in the other) are built by the builder. Their stdout and their manifests must be
byte-identical, except for the sealed files' sha256. The sealed files themselves must differ, and
their byte sizes must be equal (the fixed width above). If any printed or written line depends on
a block row, the test fails. This is the builder's version of knockout machine check 6 ("BLOCK LEAKS INTO TRAINING").

**How the comparison is made (revision 2.1; Ark).** The fields allowed to differ are **declared**
as a named list in the test, and the test prints it. They are the hashes that must differ: the
weight file's sha256 (its block rows differ), the two sealed files' sha256, and the sha256 of the
two files that print those (the manifest, `BUILD.md`). Declared as: in stdout and `BUILD.md`, the
hash group of four line patterns (the weight file's pin line, the two sealed files' sha256 lines,
the manifest's sha256 line); in the manifest, the keys `inputs/janelia/<weight file>/sha256` and
`outputs/<sealed file>/sha256`; in `SHA256SUMS.txt`, the entries of the two sealed files, the
manifest and `BUILD.md`. The comparison is **line by line** for stdout and `BUILD.md`, **key by
key** for the manifest (flattened), and **entry by entry** for `SHA256SUMS.txt`. A line that
differs passes only if it matches one declared pattern in both worlds and is equal outside the
hash group; there is no global replacement of hash strings. **Positive controls:** (1) a number
computed from the block rows (the count of non-empty block cells), appended to
`pair_stats_outside.csv`, must fail the test; (2) the same number written into a non-masked key
of `bank.meta.json`, into a non-masked line of the report (stdout and `BUILD.md`), or into a
masked line outside its hash group, must each fail it.

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
unassigned); the lobe-consistency shares; the collapse (D15), with T and K under both collapses
and at the full-grid density; `w_min`, `c*`, the tie excess or shortfall; per-lobe outside
densities; the diagnostic table of §5.4; rows read, batches read, autapse rows dropped, duplicate
outside keys, cross-lobe weight of outside type pairs; peak memory and runtime; and each output
file's sha256 and, **except for the sealed files, its size** (the sealed files by sha256 only,
§9).

**Revision 2.1 (the reviewers of the inspect output).**

- **sha256 convention.** The builder's, the tests' and the registration's sha256 are
  LF-normalised, as the flyvis pins (§1.1) and `knockout_regrow.py` record theirs
  (`builder_sha256_lf`, `tests_sha256_lf`, `registration_sha256_lf`).
- **`builder_environment`** replaces the field `versions`, so that it cannot be taken for the
  instrument's environment (`tools/.venv`, python 3.10.20 / numpy 2.2.6). It holds the versions
  found, the four compared with the pins (python, numpy, pandas, pyarrow), psutil as reported
  and not compared, the `uv` command line, and a note that it is not the instrument's.
- **`machine_record.blas_at_run_time`** is the literal `not recorded (no BLAS path in the
  builder)`. The builder does integer sums and calls no BLAS routine, so it does not probe for
  one (no `threadpoolctl`). **No exception text is written into any field:** if
  `numpy.show_config` fails, `numpy_build` is the literal `not recorded
  (numpy.show_config(mode='dicts') failed)`.
- The lobe-consistency record per type adds the cross-lobe rows as source and as target, the
  rows of each, and the cross-lobe weight (§4); `population_rows_at_c_star` holds R1's and
  CT1(M10)'s present row and column cells per lobe (§4); `weight_file_header.ipc_headers` holds
  the codec (§6.6); `type_map.annotation_controls` holds the whole file's status by side, the
  R7/R8 control and the `R1-R6` / `R1-6` identity (§3.1, §4).

### 10.3 Modes

- **`--self-test`**: runs the fixture tests (§11) and reads no real data.
- **`--inspect-only`** (the dry run): checks the pins, reads the weight file's **schema and
  metadata only** (from revision 2.1 also the flatbuffer headers of its record batches, for the
  codec, §6.6), reads the annotations, applies the map and the side rule, runs the §3.3
  self-test, and prints the per-type counts. **It reads no weight column.** Its output is what the
  reviewers use to confirm the exact map strings (§3.2) before the build. A string that differs
  from the registered map sends the map back to review. It is not patched.
- **(no flag)**: the build. It refuses on a dirty tree under `results/genome/c6/` or
  `docs/plans/` unless `--allow-dirty` is given, and a build made with `--allow-dirty` is marked
  "NOT THE REGISTERED BUILD" in its manifest and `BUILD.md` (as `knockout_regrow.py` marks its runs).
  It refuses an existing output folder.
- **Both modes, from revision 2.1 (the reviewers of the inspect output).** The inspect output of
  commit `2af21e5` was run from a dirty tree, before the builder was committed. So
  **`--inspect-only` now refuses a dirty tree exactly as the build does**: it stops with
  "REFUSED" unless `--allow-dirty` is given, and a run with `--allow-dirty` on a dirty tree prints
  "NOT THE REGISTERED INSPECT-ONLY RUN". The header of both modes prints the git head, the
  tree's state, the **LF-normalised sha256 of the builder file and of this registration**, and
  the `builder_environment` (§10.4).

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

**Revision 2.1 (the reviewers of the inspect output).** "VERSIONS DIFFER" compares **only the
four pinned versions** (python, numpy, pandas, pyarrow) and says so; psutil is reported, not
compared (the inspect run of commit `2af21e5` found psutil 7.2.2). The header line and the
manifest field are named **`builder_environment`**, because this environment is not the
instrument's (`tools/.venv`: python 3.10.20, numpy 2.2.6), which the builder does not use.
"DENSITY TARGET DIFFERS" names the registered pair it compares, "the pooled collapse (D15) x the
placed 55-type grid, |Omega| = 2961", beside the run's own types and |Omega|. "MEMORY CAP" names
its measure (§6.4).

### 10.5 Order of work

1. This registration is reviewed by Ark, Johnny and Zcode, and Mike gives his word. The builder
   and tests are written against it, `--self-test` passes, and everything is committed.
2. `--inspect-only` on the real files (annotations and schema only). The reviewers confirm the map
   strings and read the per-lobe body counts. **Done once (commit `2af21e5`, from a dirty tree;
   votes §13.4).** After revision 2.1 and its instrument edits are committed, it is **rerun on
   the clean tree** (it now refuses a dirty one, §10.3), and its output replaces the committed
   one.
3. The build, on Mike's word. It writes the private outputs and prints `c*` and the outside-block
   diagnostics. The sealed files stay sealed.
4. The male-CNS arm's registration is drafted with the outside-block tables in hand (knockout
   §8: "Printed before its data"). After its review, the knockout registration is amended with the
   four pins, and the arm's script is the first to read the sealed files.

## 11. Tests (fixtures only; no real data)

1. **Blindness** (§9): two worlds differing only in block rows give identical prints and manifests
   except the sealed hashes, different sealed files, and equal sealed-file sizes.
1a. **Suffix parser** (§4): `X_L` and `X_R` assign; `X_L_1`, `X(L)`, `X_l`, `_L` alone and a null
   `instance` do not.
2. **Flip** (§4): a fixture where CT1's side label is opposite to its partners' passes with
   `FLIP = {CT1}` and stops without it. A fixture where it is not opposite stops with the flip.
3. **Zero matches:** a fixture with the canonical column renamed stops with "ZERO NAME MATCHES".
   A fixture with one placed type removed from one lobe stops with "TYPE WITH NO CELLS".
4. **Chunked equals whole** (§6.5).
5. **Density rule:** on a hand-made `x` table with known order, `c*`, the tie excess and the
   shortfall case come out as §5.2 states. T and K for the registered map and collapse equal
   §5.3 (497 / 994 restrict-only; 511 / 1,022 pooled), and a changed map moves them (the order of
   §5.2).
6. **Row count:** a fixture whose metadata `stop` differs from its rows stops with "ROW COUNT
   DIFFERS".
7. **One index per population:** R2–R6 and CT1(Lo1) never appear in the bank files, and R1 and
   CT1(M10) carry the pooled populations.

**Added or changed in revision 2.1** (`--self-test`: 22 of 22 in the registered environment):

- **1 (blindness)** compares against a declared, printed list of masked fields, line by line and
  key by key (§9). **1b:** positive control 1, a block-derived number in
  `pair_stats_outside.csv`, must fail. **1c:** positive control 2, the same number in a
  non-masked key of the manifest, in a non-masked report line, or in a masked line outside its
  hash group, must each fail.
- **2 (flip)** also requires the per-type inconsistency counts to be printed before the stop,
  with CT1(M10) marked below 0.5 (§4).
- **4 (chunked equals whole)** also compares the per-type cross-lobe row counts.
- **7** also compares R1's printed row and column counts with the bank files.
- **8. Inspect header and dirty tree** (§10.3): the header prints the LF sha256 of the builder
  and of the registration and the `builder_environment`; `--inspect-only` refuses a dirty tree,
  runs with `--allow-dirty` and says "NOT THE REGISTERED INSPECT-ONLY RUN", and says nothing of
  the kind on a clean tree.
- **9. Annotation controls** (§3.1, §4): the R7/R8 variant sets equal the `flywireType` roll-ups
  and `R1-R6` equals `R1-6` in the fixture; one body moved out of a variant set shows as a
  symmetric difference of 1.
- **10. Codec** (§6.6): the same table written with `lz4`, `zstd` and no compression is named
  `LZ4_FRAME`, `ZSTD` and `uncompressed`, with batch count and header row sum.
- **11. Stop messages** (§10.4, §6.4): "VERSIONS DIFFER" names the four compared pins and says
  psutil is not compared; "DENSITY TARGET DIFFERS" names the registered pair and the run's type
  count; "MEMORY CAP" names the peak working set and says it does not bound the batch size;
  `blas_at_run_time` is the literal.

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
- **The L/R reading (D12).** It has two explanations, variation within the animal and a
  difference of reconstruction between the lobes (§4). The rule that separates them is
  registered by the arm. **Revision 2.1:** the second explanation is not "the left lobe is less
  complete" (refuted in that form, §4, §13.3); it is specific to R1–R6 (1,112 L / 2,265 R,
  1 : 2.04), while R7, R8 and the whole file are nearly even.
- **The R1 row and column (obligation of the arm; revision 2.1, Johnny, Ark, Zcode).** R1 is
  one index carrying all R1–R6 bodies, and its left row and column have about half the bodies
  of the right. Under the shared cut `c*` the left bank is **expected** to be sparser in R1's row
  and column, so the lobe comparison there is not a clean within-animal null. This is registered
  as an expectation, not a defect. The arm's registration must say, before its data, how it
  treats R1's row and column in any lobe comparison (for example, whether a lobe difference
  confined to them counts). What it has for this: K_L and K_R, the per-lobe present counts in
  R1's row and column (`population_rows_at_c_star`), `c*_L` and `c*_R` (§5.4), and the first
  question put to the build, how much larger the R1-row asymmetry is than 1 : 2.04 in bodies.
  `c*_L < c*_R` would read as a consequence of the R1–R6 asymmetry.
- **The grid (obligation of the arm; revision 2, Johnny and Ark).** The arm restricts its cells
  by replacing `H.ALL_CELLS` (precedent: `results/genome/c6/checks/flywire_bf_p3.py:74-76`,
  `restrict_to_30_grid`), and it states whether it trains and scores on the 2,961 placed cells or
  on 4,161 with 1,200 always-absent cells (§5.2). On Windows, where workers are spawned, the
  FlyWire arm re-applied the restriction in each worker (`worker_init` there). **Open: which
  harness structures depend on the 65-type grid and what each does under a restricted
  `ALL_CELLS`.** No harness edit and no pin change are proposed. Read for this draft, not
  analysed:
  - `FOLD` (65 × 65, from `folds.csv`, `harness.py:149-153`): `cv_fold` (`:753-755`) holds out
    `FOLD == f` intersected with `ALL_CELLS`, and `inner_folds` (`:554-555`) reads `FOLD` on the
    view's cells. That gives the nested λ choice of `fit_bf` (`:710-728`). On a restricted grid the
    folds keep their cells, but their sizes and present counts change.
  - `PAIR_ID` (`:133`): used to check `folds.csv` at import (`:152`); unchanged.
  - `TYPE_FIELDS` (`:131`): 65 rows, handed to every rule in each view (`make_view`, `:180-186`),
    unplaced types included; their field codes are computed over all 65 types.
  - **Knockout check 8** (the harness identity, BF_1's full-bank margin 0.028150051052145946;
    `knockout_regrow.py:312-313`, `:2489`): it is defined on flyvis-65 on the full grid. It must
    run before `ALL_CELLS` is replaced, as the FlyWire arm's `machine_check` did ("wrapper on
    flyvis bank, unpatched grid").
  - Constants of the registered knockout script tied to flyvis-65: `N_TRAIN_CELLS, N_TRAIN_PRESENT
    = 4161, 572` (`knockout_regrow.py:192`, check 2), the 65 × 65 masks (`:178-189`), the
    synthetic-world draws over 65 × 65 (`:713-714`), and the pre-data tables' expected values
    (`ENDPOINTS_EXPECTED`, `MIRRORS_EXPECTED`, `:196-209`).
  - `shuffled_bank` → `rewire_and_permute` (`harness.py:871-883`) swaps only among the bank's
    present cells (`edges = sorted(bank.content)`), so its shuffles stay among placed types, but
    its rejection test reads the 65 × 65 `exists`.
- **`rc_patterns` needs an attempt cap in the arm's script (obligation of the arm; revision 2, Ark
  and Zcode).** In `knockout_regrow.py`, `rc_patterns` (`:596-624`) draws row-and-column-preserving
  patterns with `while (succ < RC_SWAPS).any():` (`:611`). It has **no attempt cap**, and it is
  written for an 8 × 8 block (`reshape(8, 8)` at `:607`, `rng.integers(8, …)` at `:612`), with
  `RC_SWAPS = 20 * 32` (`:244`). On flyvis-65 the block is the 32/32 board, and the loop ends. **On
  the male CNS the block's row and column counts are unknown and must stay unread** (§9). A block
  whose rows or columns are all present or all absent can admit few or no checkerboard swaps, and
  then the loop never ends. The arm's script must add an attempt cap with a stop message, on the
  harness's own pattern (`harness.py:881-883`: `cap = 100 * target`, and the loop runs `while …
  succ < target and att < cap`), that is, a cap of 100 × `RC_SWAPS` attempts per chain. **The
  registered block-A script is not edited.** The cap belongs to the arm's own script and
  registration. What the arm reports when the cap is hit is the arm's to register.
- **Types typed by connectivity.** If the male CNS's T4/T5 or Tm/Mi labels lean on connectivity,
  part of block A may be true by definition (candidates note, risk 2). This is not checked here.

## 13. Decisions for review (reviewers, then Mike)

Each item says what its options change and gives a recommendation. The body is written with the
recommendation.

| # | question | options (what each changes) | recommendation |
|---|---|---|---|
| **D1** | The pair threshold `c` on `x = W / n_tar` | (a) fixed `c = 1`: set without male data, but the block at c = 1 **was seen** (20–21 weak cross cells, not a perfect board; revision 2 corrects revision 1), so choosing it is a choice made with knowledge of block A. (b) **match flyvis-65's density on the same cells, Ω on the placed grid, pooled over both lobes** (§5.2): the output depends on outside cells only; T and K from the collapse of D15 (pooled: 511 / 2,961, T = 0.172577, K = 1,022; restrict-only: 497, 0.167849, 994); one cut for both lobes. It does **not** match the density the synthetic limits were calibrated on (0.137467 on 4,161 cells; × 1.22). (b′) the full-grid density 0.137467 on Ω: K = 814, about 407 per lobe; the calibration's number on different cells. (c) (b) per lobe: equal densities, but the within-animal null then compares two cuts. (d) degree-sequence match: closer to what N1 sees; needs a distance and a search of its own. (e) fixed synapse total: scales with lobe size and type counts; rejected. | **(b)** with the D15 collapse, with (a), (b′), (c), 0.5 and 2 printed beside it (§5.4) |
| **D2** | Minimum weight of a neuron pair, `w_min` | 1: keep everything the release keeps at confidence 0.5. 2 or 3: drops the 62 % of weight-1 edges (or more), the FlyWire builder's starting choice. Under D1 (b), `c*` adapts, so the number of present cells stays about K, but **the composition of the passing cells changes**: pairs spread over many weight-1 neuron pairs lose, pairs carried by few strong neuron pairs gain (revision 2, Ark). | **1**, with 2 and 3 printed |
| **D3** | The canonical name column | (i) **`type`, with a closed override table of three names** (R7, R8 roll-ups and TmY9q from `flywireType`): the animal's own typing, and the one the reviewed counts appear to use. (ii) `flywireType` everywhere: one column, no overrides, but labels carried over from a female FlyWire fly, 21,350 more nulls overall, and T4d counted 1,710 instead of 1,709. (iii) keep a body only where both columns agree: strictest, and it drops bodies for reasons no one has read. | **(i)** |
| **D4** | A population that flyvis splits into several types (R1–R6; CT1's two compartments) | (a) **one grid index per population** (R1; CT1(M10); the index is the birth-id-first name): 55 types; no duplicated rows. (b) the population at every flyvis index: 61 types, but six identical R rows and columns and two identical CT1 rows, which is structure flyvis-65 does not have. (c) split CT1 by region: needs a region-level download that is not in `connectome-seed-data/Janelia/`. | **(a)** |
| **D5** | TmY9 | (i) **map to `TmY9q`, flagged** (the review's map; outside block A). (ii) leave TmY9 out (54 types). | **(i)** |
| **D6** | Side and lobe | (i) **`somaSide` → `rootSide` → `instance` suffix; declared flip set {CT1}; the lobe-consistency check stops a wrong assignment** (§4). (ii) the lobe of every body from the majority side of its partners: automatic, but connectivity then assigns sides, and the flip is no longer a declared, checkable fact. | **(i)** |
| **D7** | Which bodies count | (i) **every body whose canonical value maps, whatever its `status`**; per-type status breakdown printed. (ii) `status == Traced` only: cleaner bodies, but it changes `n_tar` and so `x`, by amounts no one has read. | **(i)** |
| **D8** | Bank content | (i) **existence bank: one `(0, 0)` row per present pair, `n_syn = x`, sign +1** (§7). (ii) real offsets for types with `assignedOlHex1/2`, and pair rows for the rest: a mixed bank whose offset field means two things; T4/T5 have no hex (backlog). | **(i)** |
| **D9** | One cut for both lobes | (i) **one `c*` from the pooled lobes**: same cut, so a lobe difference is the animal's. (ii) `c*_ℓ` per lobe: equal densities, different cuts. | **(i)**, (ii) printed |
| **D10** | Block A sealed | (i) **a separate sealed file per lobe, 64 rows each, never read before the arm's review; blindness test** (§9). (ii) one bank file with a do-not-read rule: simpler, but any look at the bank shows the block. | **(i)** |
| **D11** | Where the banks live | (i) **outside the repository; the manifest and `BUILD.md` committed**, as for FlyWire. (ii) commit the outside bank files too (CC-BY allows it, per `SOURCE.md`): easier to reuse, but the committed tree would then hold per-pair male data, and the sealed files must stay outside anyway. | **(i)** |
| **D12** | The L/R reading (**handed to the arm's registration**) | (i) R on the male CNS needs R in both lobes. (ii) the right lobe primary (the side of FIB-19 and of the male optic lobe v1.1), the left lobe the null. **Revision 2 (Johnny, Ark):** a disagreement has two explanations, variation within the animal and incompleteness of the left lobe (R1–R6: 2,265 right, 1,112 left), and the pooled cut makes the lobe densities differ by construction (§4). The rule that separates the two explanations must be registered by the arm, before its data. **Revision 2.1 (Johnny, Ark, Zcode):** "incompleteness of the left lobe" is refuted in its general form (`Traced` L 81,362 / R 82,738, 1 : 1.02); the deficit is R1–R6-specific (1 : 2.04; R7 1 : 1.14, R8 1 : 1.13); the R1 row and column are an expected asymmetry the arm must treat (§4, §12). | **(i)** as one ingredient there; the separating rule is the arm's |
| **D13** | Synthetic worlds on the male bank (**handed to the arm's registration**) | knockout §8: "decided with the builder". It is a property of the instrument on this bank. | decide in the arm's registration |
| **D14** | File date | `2026-09-26-…` (the local day) vs `2026-09-25-…` (the UTC day of drafting, per GLOSSARY) | **Closed in revision 2:** renamed to `2026-09-25-…` with `git mv` (the reviewers agreed) |
| **D15** | **The collapse of flyvis-65 onto the placed grid** (new in revision 2, Zcode), which sets T and K | (i) restrict-only: unplaced types dropped, and R1 is flyvis's R1 alone; 497 of 2,961, T = 0.167849, K = 994. (ii) **pooled**: the index that carries a population carries it in flyvis-65 too, as a logical OR (R1 from R1–R6; CT1(M10) from both CT1 compartments); 511, T = 0.172577, K = 1,022. Pooling R1–R6 alone gives 498 (T = 0.168186, K = 996). All verified for this draft (§5.3). Both are printed, and the "DENSITY TARGET DIFFERS" stop is keyed to the registered one. | **(ii)**, R1–R6 and CT1 pooled, matching D4 |

### 13.1 Votes on revision 1 (DPC Research chat, 2026-09-26 UTC; as relayed by CC)

| reviewer | time (UTC) | vote |
|---|---|---|
| Johnny | 04:57 | yes, with edits |
| Ark | 05:00 | yes, with edits |
| Zcode | 05:08 | yes, with edits |

Revision 2 has not been voted on. **(Revision 2.1 note:** that stays true. Revision 2 applied the
edits these three votes asked for (§13.2, commit `8591491`); no separate vote on its text was
taken. The builder was written from it on Mike's word in the chat, 2026-09-26 07:39 UTC ("do 1").
The next votes are those on the builder's inspect-only output, §13.4.)

### 13.2 The edits of revision 2, who asked, and where each is applied

| # | edit | asked by | applied in |
|---|---|---|---|
| 1 | The harness grid is 65 × 65; the arm restricts `H.ALL_CELLS` as `flywire_bf_p3.py:74-76` does; an obligation of the arm; the grid-dependent harness structures listed as open; no harness edit, no pin change | Johnny (raised as blocking); Ark (not blocking, with a residue) | §2, §7, §12 |
| 2 | Two densities: 572 / 4,161 = 0.137467 (the synthetic limits' grid) vs 497 / 2,961 = 0.167849 on Ω (× 1.221); the rationale of §5.2 corrected to "matches flyvis-65 on the same cells"; the full-grid option (K = 814, about 407 per lobe) as D1 (b′); the 2,961 / 4,161 training grid handed to the arm with its consequence | Ark | §5.2, §5.3, §5.5, D1 |
| 3 | The collapse as a decision: restrict-only 497 vs pooled 511 (T = 0.172577, K = 1,022); T, K and the stop depend on the chosen collapse; both printed | Zcode | §5.3, §5.4, §10.2, §11, D15 |
| 4 | The c = 1 fact: the perfect board came from a summed threshold mislabelled "mean ≥ 1"; at an honest c = 1 the block had 20–21 weak cross cells; c = 1 stays demoted because it was seen; 64/64 inferable at every threshold tried added to §0 | Zcode | §0, §5.5, D1, §14 |
| 5 | Two explanations of a lobe disagreement (variation within the animal; incompleteness of the left lobe); the pooled cut makes the lobe densities differ by construction; the separating rule handed to the arm | Johnny, Ark | §4, §12, D12 |
| 6 | Order: map frozen → T → threshold, so the "DENSITY TARGET DIFFERS" stop does not fire on a legal map change | Ark | §5.2, §5.3 |
| 7 | D2: `w_min` changes the composition of the passing cells | Ark | §5.1, D2 |
| 8 | `rc_patterns` has no attempt cap and is written for 8 × 8; the arm's script adds a cap of 100 × target with a stop message (the pattern of `harness.py:881-883`); the registered block-A script is not edited | Ark, Zcode | §12 |
| 9 | Block A's mirror cells lie in Ω; the sealed files' size is not printed or written (fixed width); `w_min` of the sealed files named; the `instance`-suffix parser and the birth-id sort specified | Zcode | §5.2, §9, §10.2, §11, §4, §3.2 |
| 10 | Rename to `2026-09-25-…` with `git mv`; D14 closed | the reviewers | file name, header, D14 |
| 11 | This vote and edit table | CC's brief | §13.1, §13.2 |

**Where revision 2 differs from the brief.** Edit 3 relayed Zcode's pooled collapse as "R1 = OR
of R1–R6 presence". The count of 511 is reproduced only if CT1's two compartments are pooled too.
With R1–R6 alone the count is 498 (§5.3). Revision 2 registers the pooled collapse as both
populations, which is also what D4 places. For edit 2, Ark's alternative "K = 814, 407 per lobe"
is 0.137467 × 5,922 = 814.08, so about 407.04 per lobe (verified). For edit 8, the brief cited
`harness.py:883`; the cap is defined at `:881` and used at `:883`.

### 13.3 The edits of revision 2.1, who asked, and where each is applied

From the reviews of the inspect-only output (§13.4), as relayed in CC's brief. The type map, the
side rule, D1–D15 and the density target are not changed by any of them.

| # | edit | asked by | applied in |
|---|---|---|---|
| 1 | The left/right asymmetry in its measured form: whole-file `Traced` L 81,362 / R 82,738 (1 : 1.02), so "the left lobe is less complete" is refuted in its general form; the deficit is R1–R6-specific (1,112 / 2,265, 1 : 2.04; `Traced` 501 / 893, null 611 / 1,372), R7 608 / 692 (1 : 1.14) and R8 625 / 704 (1 : 1.13) nearly even; mechanism not established; the Nern et al. 2025 source statement kept, with what it does not explain. The R1 row and column as an expectation handed to the arm | Johnny, Ark, Zcode | §4, §12, D12 |
| 2 | Whether the side columns are filled for R1–R8: now checked, with the inspect numbers; the photoreceptor side is a transfer through `rootSide`, not a measurement | the reviewers | §1.2, §4 |
| 3 | `R1-R6` / `R1-6` are two spellings of the same 3,377 bodies; "under flywireType [0, 0]; disagree 3377" is a string artefact; `flywireType` alone would cover R1–R6, R7 and R8, so the D3 mix is redundant there (map unchanged); 59 % null status in R1–R6 as the mark of an aggregate label, and L4's one null body named | Johnny, Zcode | §3.1, §3.2, §3.3 |
| 4 | R7/R8 sides counted from the `type` variants, independent of `flywireType`: same bodies, 608 / 692 and 625 / 704; printed by `--inspect-only` | Ark | §4, builder `print_controls` |
| 5 | `assignedOlHex1` as an independent lobe carrier: it is a hex column coordinate shared by both lobes, so it cannot carry a side; no check built | Ark (proposal) | §1.2, §4 |
| 6 | The refuted claim recorded with its six fields (below); this registration has no error ledger of its own | the brief | §13.3 |
| a | `--inspect-only` prints the LF sha256 of the builder and of the registration and the git head, and refuses a dirty tree exactly as the build does | the reviewers | §10.3; builder `run` |
| b | `blas_at_run_time` is the literal `not recorded (no BLAS path in the builder)`; no exception text in any measurement field | the reviewers | §10.2; builder `machine_record` |
| c | The blindness test: a declared, printed list of masked fields; line-by-line and key-by-key comparison; a second positive control (a leak into the manifest or the report must fail) | the reviewers | §9, §11; tests |
| d | Stop messages name what they compare: "DENSITY TARGET DIFFERS" the registered pair; "VERSIONS DIFFER" the four compared pins; "MEMORY CAP" its measure (the process's peak working set, probed per batch; it bounds nothing) | the reviewers | §6.4, §10.4; builder |
| e | The builder's environment is the field `builder_environment`, named apart from the instrument's (python 3.10.20 / numpy 2.2.6) | the reviewers | §10.2, §10.4; builder |
| f | "LOBE ASSIGNMENT INCONSISTENT": per-type counts of the inconsistencies printed before a stop and on a pass; computed on outside-block pairs only | the reviewers | §4; builder `stream_weights`, `lobe_consistency` |
| g | The codec named without decoding a value, from the IPC flatbuffer headers; recorded in the inspect output and the manifest | Ark (against deferral) | §1.2, §6.6; builder `ipc_body_codecs` |
| 7 | This table and §13.4 | CC's brief | §13.3, §13.4 |

**Where revision 2.1 differs from the brief.** (i) The brief's whole-file `Traced` counts,
81,362 L / 82,738 R, are reproduced exactly with `somaSide` then `rootSide`. Under the full
registered side rule, which adds the `instance` step, they are 81,378 / 82,753 (991 unassigned).
The ratio is 1 : 1.02 either way; §4 gives both. (ii) The brief asked to split `R7R8_unclear` by
its `flywireType`; all 85 such bodies have a null `flywireType`, so they enter neither roll-up,
and the variant sets still equal the roll-ups. (iii) Every other number of the brief matched:
R1–R6 1,112 / 2,265, `Traced` 501 / 893, null 611 / 1,372; R7 608 / 692; R8 625 / 704; the side
steps of R1–R8; `R1-R6` and `R1-6` both 3,377 and the same bodies; 59 % null (1,983 / 3,377); L4
one null body. (iv) The expectation of edit 1 asks for "present counts in R1 rows per lobe"; the
build did not print them, so revision 2.1 adds that print (`population_rows_at_c_star`, §4).

**The refuted claim (error-ledger form; this registration has no ledger of its own).**

| field | entry |
|---|---|
| item | the reading of a lobe disagreement, explanation 2 (§4) |
| was | "the left lobe may be less completely reconstructed or typed. This file's own counts point that way: R1–R6 has 2,265 bodies on the right and 1,112 on the left"; and "So the left lobe may be less complete" |
| correct | the whole left lobe is not less complete: whole-file `Traced` L 81,362 / R 82,738 (1 : 1.02). The deficit is specific to R1–R6 (1 : 2.04); R7 (1 : 1.14) and R8 (1 : 1.13), sided through the same `rootSide` step, are nearly even. Mechanism not established |
| where it lived | `docs/plans/2026-09-25-male-cns-bank-builder-registration.md:302-305` and `:317` at revision 2 (commit `8591491`); echoed at `:736` (§12) and `:796` (D12) |
| what refuted it | the annotation file itself (pin §1.1): `status` by side over the whole file and the per-type side counts of the inspect output (`results/genome/c6/checks/male_cns_bank_builder_inspect_only.txt`, commit `2af21e5`), recounted for revision 2.1 |
| who caught | Johnny, DPC Research chat, 2026-09-26 08:10 UTC (Ark and Zcode asked for the same edit) |

### 13.4 Votes on the inspect-only output (DPC Research chat, 2026-09-26 UTC; as relayed by CC)

On `results/genome/c6/checks/male_cns_bank_builder_inspect_only.txt` (commit `2af21e5`), before
the build.

| reviewer | time (UTC) | vote |
|---|---|---|
| Johnny | 08:10 | yes, with edits |
| Zcode | 08:11 | yes, with edits |
| Ark | 08:19 | yes, with edits |

Revision 2.1 has not been voted on. The inspect-only run is to be repeated on the clean tree
after it is committed (§10.5).

## 14. Not verified at drafting

**Revision 2.1: what the list below no longer holds, and what it still does.** Settled since
revision 2: the side columns of R1–R8, CT1 and the 16 block types, and the exact map strings
(inspect output, commit `2af21e5`; §1.2, §4); the review's counts R7/R8 1,300 / 1,329, 931
`_unclear` (404 + 442 + 85), R1–R6 2,265 / 1,112, CT1 and Am1 n = 1 per lobe, and T4d 1,709 /
1,710 (the inspect table; recounted for revision 2.1 where §4 quotes them); the compression codec
and the sum of the batch lengths (§6.6; per-batch sizes are read but not printed). Still open:
key uniqueness and autapse rows (the weight stream); whether `rootSide` means the lobe for the
photoreceptors (the lobe-consistency check, in the build); the mechanism of the R1–R6
asymmetry (§4); CT1_L's 100 % and the backlog's counts; and the rest of the list.

- Which of `somaSide`, `rootSide` and the `instance` suffix carries the side for R1–R8, CT1 and
  the 16 block types; the exact strings of R1–R6, the R7/R8 roll-ups, `CT1`, `Am1` and `TmY9q`
  in their columns (§3.2). Settled by the dry run.
- That Am → Am1 is the backlog's 61st mapped type (§3.2; inferred from arithmetic).
- **Zcode's correction of the c = 1 fact** (revision 2, §0): that the perfect board came from a
  summed threshold of about 500–800 and that c = 1 gave 20–21 weak cross cells. It rests on his
  word in the chat of 2026-09-26 05:08 UTC, as relayed. The backlog and knockout registration §8
  still carry the older wording, and neither was edited.
- What each grid-dependent harness structure does under a restricted `ALL_CELLS` (§12). Listed,
  not analysed. The arm's registration owns it.
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
- Revision 2.1: `results/genome/c6/checks/male_cns_bank_builder_inspect_only.txt` (commit
  `2af21e5`); the annotation file's `status`, `statusLabel`, `somaSide`, `rootSide`, `instance`,
  `type`, `flywireType`, `superclass` and `assignedOlHex1/2` columns (scratch scripts outside the
  repository and the builder's own `print_controls`); the IPC footer and record batch headers
  of both files (`ipc_body_codecs`; no message body read); the Arrow format's `Footer.fbs` and
  `Message.fbs` (`Block`, `RecordBatch`, `BodyCompression`, `CompressionType`).
