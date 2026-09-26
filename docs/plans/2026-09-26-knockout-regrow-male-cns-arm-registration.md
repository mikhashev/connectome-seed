---
**Status: DRAFT, revision 1, 2026-09-26 UTC (`date -u` read 08:52 UTC when drafting began).
Not reviewed, not committed. No script written, nothing fitted, no sealed file opened.** Drafted
by a CC subagent for review by Ark, Johnny and Zcode, then Mike. The design choices that need a
vote are marked **proposal** in the body and listed in §9 (D1–D16), each with its options, what
each option changes, and a recommendation. The body is written with the recommended option, so
the draft is complete as it stands.

**What this file is.** The registration of the **male CNS arm** of knock out and regrow: the
animal control that block A's registration names in its §8,
[`2026-09-24-knockout-regrow-registration.md`](2026-09-24-knockout-regrow-registration.md),
**revision 3.4.1** (commit `74db080`; LF sha256 `409184de…3facd6`, the value the flyvis-65 run's
manifest recorded; cited below as "A §n"). It is a **delta on A**: everything of A revision 3.4.1
applies to this arm unchanged unless a section below says otherwise. Every gate and every reading
rule of A is kept. What changes is the bank (two banks, one per optic lobe of one male), the grid,
what follows from a block whose content is sealed, the synthetic worlds built on the male banks,
the values registered from those worlds, the seeds and the script constants. Its form follows
block B's registration,
[`2026-09-25-knockout-regrow-block-b-registration.md`](2026-09-25-knockout-regrow-block-b-registration.md),
revision 1.1 ("B §n"). The banks are the output of the male CNS builder,
[`2026-09-25-male-cns-bank-builder-registration.md`](2026-09-25-male-cns-bank-builder-registration.md),
revision 2.1 ("the builder", "builder §n"), built at head `e0a3cd7` and committed in `5860619`
(`results/genome/c6/checks/male_cns_bank/BUILD.md` and `bank.meta.json`). The builder hands this
arm a list of obligations (builder §12, D12, D13); §9 settles each of them and names where.

**Order of work proposed (D15).** (1) This draft is reviewed, and Mike gives his word. (2) The
arm's script (a new file, D14) and its tests are written against it and committed with this file,
marked as a draft. (3) The `--synthetic-only` pre-run of both lobes is made from that committed
head, on Mike's word; it reads no sealed file, and its outputs become the arm's two pinned
references. (4) A revision of this file registers the values read from those references (§3.3)
and is reviewed; in the same step A is amended with the four bank pins (D11). (5) The registered
run, on Mike's word. It is the first and only code that opens the sealed files (§7.4).

**The seal, at drafting: intact.** No person or agent involved in this draft has opened, printed,
loaded, counted, summarised, plotted or diffed `male_cns_L_blockA.sealed.csv` or
`male_cns_R_blockA.sealed.csv`. Their sha256 values are quoted from `bank.meta.json` and
`SHA256SUMS.txt` only. The drafting agent listed the build folder's file names (no sizes) and did
not open either file. The prior exposure of block A of the male CNS through other channels is
declared in §1.5.
---

# Registration: knock out and regrow, the male CNS arm (the animal control of block A)

## 0. Question, name, and what it is not

**Name.** *Knock out and regrow, male CNS arm: does the same learnable rule, reading no type
names, regrow block A in each optic lobe of one male fly, where it was not shown?*

**Question.** A §0 with the bank replaced. For each lobe ℓ ∈ {L, R} of the Janelia male CNS v1.0
(Berg et al. 2026; one male), take the bank that the builder produced at its registered cut: an
existence bank on the 55 placed types, with a cell present iff `x_ℓ(s, t) = W_ℓ(s, t) / n_ℓ(t) ≥
c*` (builder §5). Remove every cell of block A (the same 64 cells by name: Mi1, Tm3, Mi4, Mi9, Tm1,
Tm2, Tm4, Tm9 × T4a–d, T5a–d). Train on the rest of the lobe's bank. Ask whether the predictions
for the 64 cells separate the present cells from the absent ones better than the same rule on the
same knockout in 99 degree-preserving shuffles of that lobe's bank (leg S) and better than the
block's own labels permuted within the block (leg P). The standard is ADR-005 agreed point 6, as for
block A.

**What an animal control is for here.** Block A on flyvis-65 read **G**, "not detected at the R
level above γ_R" (commit `1ed55ec`; `results/genome/c6/checks/knockout_regrow/RESULT.md` line 5;
the blind review, `docs/notes/2026-09-26-knockout-regrow-blind-review.md` §A, "the verdict
follows"). flyvis-65 is a template of at least two flies, averaged over columns and merged by
taking the larger estimate (A §0). The male bank is one animal, not averaged over columns or
animals, cut at one threshold (builder §8, the table of what differs). The arm asks whether the
flyvis-65 reading holds in one animal. §5 registers, before data, how each male outcome is read
against flyvis-65's G.

**What is known at drafting, stated because this design is written after it.**

- **flyvis-65's verdict is G** (above). A §8's joint reading table (A D13) was written and voted
  before that verdict; the male-specific readings of §4.2, §4.3 and §5 of this file are written
  after it.
- **The build's outside-block facts** (all outside block A; `BUILD.md`, `bank.meta.json`):
  - The cut: `c*` = **2.99436** (2.994356659142212), K = 1,022 pooled present outside cells, `w_min`
    = 1, tie excess 0, shortfall 0 (`BUILD.md` line 181; `bank.meta.json` lines 3734–3742).
  - Lobe L: **496** of 2,961 outside cells present, density **0.167511**; lobe R: **526**,
    **0.177643** (`BUILD.md` lines 182–183; `bank.meta.json` lines 3743–3750). The flyvis-65
    density on the same 2,961 cells under the registered pooled collapse is 0.172577 (`BUILD.md`
    line 17); the density on which A's synthetic limits were measured is 0.137467, on 4,161 cells
    of the 65-type grid (builder §5.2). Ark's point: 0.1675 and 0.1776 are ×1.22 and ×1.29 of it.
  - Per-lobe matched cuts, diagnostics only: `c*_L` = 2.69453, `c*_R` = 3.39337 (`BUILD.md` lines
    195, 198).
  - **R1's row and column at `c*`: lobe L 3 / 1 (1,112 bodies), lobe R 3 / 1 (2,265 bodies)**
    (`BUILD.md` line 185; `bank.meta.json` `population_rows_at_c_star`, from line 3751). **The
    R1-row asymmetry that the builder registered as an expectation (builder §4, §12) did not
    appear.** This draft checked the outside files (§1.4): R1's 3 row cells and 1 column cell are
    the same cells in both lobes. CT1(M10): L 9 / 31, R 9 / 30 (`BUILD.md` line 184).
  - **Cross-lobe outside rows: 0 of 2,332,880** kept outside rows; cross-lobe weight of outside
    type pairs 0; duplicate outside keys 0 (`BUILD.md` line 121; `bank.meta.json` lines 4466–4476).
    The lobe-consistency check therefore passed with every placed type at share 1.0000
    (`BUILD.md` lines 124–179), trivially: no neuron pair of these types crosses the midline, so
    connectivity cannot test the side rule on these types (the check could not have failed except
    by a side label that contradicts the lobe of every partner).
  - Inferable **64 / 64** at `c*` in both lobes; **3** mirror cells in each lobe; smallest endpoint
    keep T5a 4 (`BUILD.md` lines 189–190). Also printed by the builder: inferable 56 / 64 in lobe L
    at the (b′) cut for `w_min` = 2 and 3 (`BUILD.md` lines 210, 227; §11, ledger row M(1)).
  - All 16 block names map by name (`type` column), with 808–1,037 bodies per type per lobe and
    a right/left body ratio between 0.98 and 1.02 for every block type (`BUILD.md` lines 30–84;
    §1.2).
- **Block A of the male CNS was seen before this arm, through the preliminary graph** (§1.5).

**What does not transfer from A §0, and why.** Three statements of A §0 rest on flyvis-65's block
being a perfect board (16 + 16 present, no cross cell), counted three times in review. On the
male banks the block is sealed, so none of them can be made before data:

- **"No additive score can find the board."** It needs every row and every column of the block to
  hold the same share of present cells. An 8 × 8 block can satisfy that (a balanced pattern), but
  whether the male blocks do is unknown. **So N1's additive score may order part of the male
  block,** and check 5 becomes a print (§3.4, D8).
- **"Leakage through degrees cannot carry the board."** It rested on 4 of 8 in every row and
  column. Unknown here. Leg S subtracts N1's AUC on every bank (A §3.2), so R still needs structure
  beyond the degrees.
- **"The board is exactly rank 1"** (A §2.4). Unknown here. A `ceiling_block` below 0.90 can then
  be a rank limit of rule #2.1, not only a failed fit (§2, as B's D9).

**What it is not.**

- **Not a second verdict on flyvis-65.** flyvis-65's G stands as registered. §5 says what each
  male outcome adds to it.
- **Not a test of the builder.** The banks are the builder's registered output; this arm reads
  them as they are, at `c*`. The builder's diagnostic cuts are not tested here (§6).
- **Not a C6 exam, not question (ii)**, as A §0.

## 1. The banks, the block, and exactly what is removed

### 1.1 Files and pins

**Unchanged:** the eight pins of A §1.1 (`offsets.csv`, `types.csv`, `folds.csv`, `harness.py`,
rule #2.1's `fit.py` and `decode.py`, `bf_decode.py`, `n1_decode.py`). flyvis-65 is still read,
for machine check 8 only (§3.4).

**Added (the male banks).** The build folder is
`connectome-seed-data/Janelia/derived/male_cns_v1_20260926T084555Z_e0a3cd744c39/` (outside the
repository, builder D11 (i)). sha256 over raw bytes, from the committed `bank.meta.json` (lines
4480–4498) and `SHA256SUMS.txt`, and for the three outside files recomputed by this draft
(`sha256sum`, 2026-09-26 UTC, equal):

| file | sha256 | read by |
|---|---|---|
| `male_cns_L_outside.csv` | `16c5752a241b2e61d4caeaa23bc4b9b9385011c2bfa6a2db504195199bfe9fb0` | every mode |
| `male_cns_R_outside.csv` | `27a9079b656d1aeb1943702e173d2fa3009f7d8257a78f9e8b5c0f3712b4cf36` | every mode |
| `pair_stats_outside.csv` | `dd71e686c50c127fa9b3bf9f05f957adbd1340d579c839361d16c6c0f0db421f` | check 4 (lobe agreement), §4.3 |
| `male_cns_L_blockA.sealed.csv` | `eb611f6805484c4f54c22f072a2ca74219a97b3265c6bfb8a4639e45108e8b8e` | the registered real run only (§7.4) |
| `male_cns_R_blockA.sealed.csv` | `c53a44670b784f7af1c8c3973ba440961b24bff08b039a0cf4c73bd32414da84` | the registered real run only (§7.4) |
| `bank.meta.json` (private and committed copies, byte-equal) | `5ff4af9df5b6ca8e6bfb8282bb27a3b00697a4123b1885118a6d11057ab32d8b` | every mode (`c_star`, the placed list) |

The script refuses if any differs. The sealed files' hashes are checked **before** they are
opened, in the real run only; no other mode computes more than that hash (§7.4). **Where the pins
live (D11):** in this file and the arm's script; A is amended, append-only, with the four bank
pins, as A §8 and builder §10.5 step 4 promise.

### 1.2 The block (unchanged; its mapping on the male bank)

The same 64 cells by name (A §1.2); the same answer key (ON/OFF of the eight sources, T4/T5 of the
eight targets), used only to score and to print strata. **All 16 names map by name** through the
`type` column, and each has bodies in both lobes (the builder's "TYPE WITH NO CELLS" passed;
`BUILD.md` line 101):

| type | L | R | | type | L | R |
|---|---|---|---|---|---|---|
| Mi1 | 886 | 887 | | T4a | 835 | 849 |
| Tm3 | 1,017 | 1,037 | | T4b | 844 | 846 |
| Mi4 | 883 | 889 | | T4c | 895 | 883 |
| Mi9 | 886 | 889 | | T4d | 850 | 859 |
| Tm1 | 887 | 890 | | T5a | 826 | 838 |
| Tm2 | 883 | 883 | | T5b | 863 | 852 |
| Tm4 | 837 | 833 | | T5c | 862 | 858 |
| Tm9 | 884 | 887 | | T5d | 812 | 808 |

(Bodies per lobe after the side rule, `BUILD.md` lines 30–84. R/L between 0.987 (T4c) and 1.020
(Tm3); every block type takes its side from `somaSide` alone.)

### 1.3 What is removed, entirely; the grid (proposal, D1)

**Removed from training, per lobe:** the 64 block cells, every field and the existence label
(A §1.3). On the male bank a cell's content is one row `(0, 0)` with `n_syn = x` and sign +1
(builder §7); the removal takes that row and the label.

**The grid (D1): the placed grid.** The arm trains and scores on the 55 placed types only, by
replacing `H.ALL_CELLS` with the 55 × 55 = 3,025 placed cells, as the FlyWire arm did
(`restrict_to_30_grid`, `results/genome/c6/checks/flywire_bf_p3.py:73-75` at `c55d3e3`; the
assignment is line 75). **Training cells per lobe: 3,025 − 64 = 2,961. Training present: 496 (L),
526 (R)** (`BUILD.md` lines 182–183). A §8 already fixed this ("cells outside the builder's type
set are left out of training and scoring"); the builder handed the choice on with the 4,161-cell
alternative (builder §5.2), which D1 records.

**What depends on the grid, and what the arm does with each** (harness lines at `1789aeb`, the
pinned `harness.py`, sha `6fc80952…`, unchanged since; script lines of `knockout_regrow.py` at
`74db080`; no harness edit and no pin change):

| structure | where | under the restricted `ALL_CELLS` | the arm |
|---|---|---|---|
| `ALL_CELLS` | `harness.py:154` | replaced by the 3,025 placed cells | `restrict_to_placed_grid()` in the main process after check 8, and in every worker's initializer (Windows spawns workers; the FlyWire arm re-applied it in `worker_init`, `flywire_bf_p3.py:116-125`); each fit asserts `len(H.ALL_CELLS) == 3025` (as `flywire_bf_p3.py:175-177`) (S5) |
| `make_view` | `harness.py:180-186` | reads `ALL_CELLS` at call time, so the `~BLOCK` mask gives 2,961 training cells, the full mask 3,025, the block mask 64 | unchanged; check 2 counts these (S7) |
| `FOLD`, `inner_folds`, `cv_fold` | `harness.py:149-153`, `:554-555`, `:753-755` | `FOLD` (65 × 65 from `folds.csv`) is untouched; each placed cell keeps its fold. Per fold the 2,961 cells split 292, 301, 286, 293, 290, 300, 274, 304, 307, 314 (65-grid: 414–419), and the present outside cells 43–56 (L) and 47–64 (R) (§1.4). The nested λ choice (`fit_bf`, `:710-728`; rule #2.1, `fit.py:119-142`) runs on these folds. `cv_fold` is used by check 8 only, on the full grid | unchanged; every fold holds present and absent cells in both lobes (checked, §1.4) |
| `PAIR_ID` | `harness.py:133`, `:152` | used to check `folds.csv` at import | unchanged |
| `TYPE_FIELDS` | `harness.py:131-132` | 65 rows, computed over all 65 flyvis types, handed to every fit (`make_view`) | unchanged (FlyWire precedent). R1 carries flyvis R1's fields and CT1(M10) flyvis CT1(M10)'s; the ten unplaced types' rows have no cells |
| `NAMES`, `IDX` | `harness.py:119-123` | 65 names in birth-id order | unchanged |
| `Bank.exists` | `harness.py:163-166` | 65 × 65; unplaced rows and columns empty | the male loader writes placed cells only, and refuses any other name (S4) |
| `REAL`, `REAL_CONTENT` | `harness.py:135-146`, `:169` | flyvis-65 | used only by check 8. Every other use of `H.REAL` in the script (`pre_data_tables` via `main` :2556, `degree_terms` :694-698, `NONBLOCK_CELLS` :691, `build_bank("real")` :754-757, `check_board` :2554, `machine_checks_real` :2466-2472) takes the lobe's male bank (S6) |
| `fit_n1` | `harness.py:350-408` | 131 features (intercept, 65 source, 65 target indicators); the unplaced types have no rows, so the ridge (`LAMBDA` = 1) holds their `a`, `b` at 0 | unchanged; their terms touch no placed cell |
| `bf_als`, `_grid`, `_n1_logit_grid` | `harness.py:666-707` | 65 × 65 arrays; unplaced rows of `M` are 0, so their factors are held at 0 by the ridge; the SVD start and the `PCG64(30000 + j)` perturbations are drawn over 65 rows as before | unchanged |
| `shuffled_bank`, `rewire_and_permute` | `harness.py:871-921` | swaps among the bank's present cells, whose endpoints are placed, so every shuffle stays on the placed grid; `canon_content` needs a `"hull"` key | the loader writes `"hull": []` (S4) |
| `score` | `harness.py:490-508` | per cell; offset, counts and sign are computed on the `(0, 0)` placeholder | printed, marked meaningless (§2, D5) |
| check 8 | `knockout_regrow.py:2464-2490`, constant `:313` | defined on flyvis-65 on the full 65 grid | runs first, on flyvis-65, before any restriction, in a pool whose initializer does not restrict (the FlyWire arm: "wrapper on flyvis bank, unpatched grid", `flywire_bf_p3.py:157-167`) (S6) |
| constants for the 65 grid and flyvis-65 | `knockout_regrow.py:189-209`, `:427-428`, `:681`, `:691`, `:701-728`, `:866` | `N_TRAIN_CELLS, N_TRAIN_PRESENT = 4161, 572`; `MASKS["full"].sum() == 65 * 65`; `OTHERS` (49 types); the content pool (572 flyvis cells); the worlds' 65 × 65 draws; `outside_density = bank.exists[~BLOCK].mean()` over 4,161 cells | per lobe 2,961 / 496 or 526; `OTHERS` = the 39 placed non-block types; worlds with every unplaced cell absent; `outside_density` over the 2,961 placed outside cells (S7, S14) |
| constants written for a 32/32 block | `knockout_regrow.py:228-233` (`TAU` comment), `:244` (`RC_SWAPS = 20 * 32`), `:435-445` (`check_board`), `:539-561` (check 7's random 32/32 case), `:909-912` (`precision_at_32`), `:924-937` (`smallest_passing_auc` docstring, "k/1024"), `:1039`, `:1075` (`auc_other_59`), `:2383` ("AUC (32/32)", "P@32"), `:237-239` (`WITHIN_FLY_NOTE`, "about 4 of 64") | the male block's count is sealed | §3 and S9–S16, S24. `RC_SWAPS` stays 640 (a constant of the null generator); `make_world`'s assertion of 32 (`:727`) stays, since every world's block is a 32/32 board |
| `rc_patterns` | `knockout_regrow.py:596-624` | `reshape(8, 8)` (`:607`) and `integers(8)` (`:612`) fit block A on any bank; the loop `while (succ < RC_SWAPS).any()` (`:611`) has no attempt cap | an attempt cap of 100 × 640 per chain on the harness's pattern (`harness.py:881-883`), with its own treatment on the real block (§3.2, D9, S13) |

**Not removed (stated, so that a reader knows what the rule still sees):** the 16 types and every
other cell of their rows and columns among placed types; the three mirror cells (§1.4); the other
T4/T5 inputs among the placed types (C3, CT1(M10), Mi10, TmY15, TmY4; CT1(Lo1) is not placed, and
CT1's two compartments are summed in CT1(M10), builder §3.2); `TYPE_FIELDS` for all 65 types.
**Also not in training, unlike flyvis-65:** the ten unplaced types (Mi3, Mi11, Mi12, Tm28 absent
from the male CNS; R2–R6 and CT1(Lo1) pooled into R1 and CT1(M10); `BUILD.md` line 15).

**The field channel.** Unchanged from A §1.3: the eight targets share one field group, so rule
#2.1's field term is a function of the source alone on the block, an additive term. On flyvis-65
its parity contrast was zero because the board is balanced; on the male block that depends on the
sealed pattern (§0).

### 1.4 Printed before data: what each endpoint keeps, inferability, mirrors, lobe agreement

Computed on 2026-09-26 UTC by one scratch script (in the drafting agent's session scratchpad, not
committed) from `pair_stats_outside.csv` and the two `*_outside.csv` files only, after checking
that they hold **no row of a block-A cell** (0 of 5,922 rows of `pair_stats_outside.csv`; 0 in
each outside bank) and that each outside bank equals the `present = 1` rows of
`pair_stats_outside.csv` for its lobe. Presence is the builder's (`x ≥ c*`). Self-loops are
counted, as in A §1.4. No block cell was read: the files hold none.

**What each endpoint keeps in training** (present outside cells; sources: training targets,
training sources; targets: training sources, training targets):

| source | L | R | | target | L | R |
|---|---|---|---|---|---|---|
| Mi1 | 22, 11 | 23, 11 | | T4a | 5, 9 | 6, 10 |
| Tm3 | 19, 10 | 21, 10 | | T4b | 5, 8 | 5, 8 |
| Mi4 | 17, 11 | 17, 11 | | T4c | 5, 9 | 5, 9 |
| Mi9 | 18, 13 | 20, 14 | | T4d | 5, 8 | 5, 8 |
| Tm1 | 17, 9 | 17, 9 | | T5a | 4, 7 | 4, 9 |
| Tm2 | 17, 7 | 18, 7 | | T5b | 4, 8 | 4, 8 |
| Tm4 | 16, 11 | 16, 12 | | T5c | 4, 8 | 4, 8 |
| Tm9 | 5, 5 | 5, 8 | | T5d | 4, 9 | 4, 9 |

Unlike block B (B §1.4, D2), this table can be printed whole: its difference from a full-degree
table would give the block's row and column counts, and no full-degree table of the male banks
exists outside the sealed files.

- **Johnny's inferability: 64 / 64 in each lobe** (a source with ≥ 2 training targets and a
  target with ≥ 2 training sources). The thinnest endpoints are T5a–T5d (4 training sources each)
  and Tm9 (5 training targets). Equal to `BUILD.md` lines 189–190.
- **Mirror cells: 3 in each lobe, the same three:** (T4a, Mi9), (T4b, Mi9), (T4c, Mi9). Their
  block partners are (Mi9, T4a), (Mi9, T4b), (Mi9, T4c). flyvis-65 had these three and (T5b, Tm2),
  (T5c, Tm2) (A §1.4). The AUC on the other **61** cells is printed beside the AUC on all 64.
- **Rows and columns outside the block:** Lawf2 and T1 have no present outside cell as a source in
  either lobe (empty rows); Tm30 has one in lobe L. R1, R7 and R8 have one present cell as a target
  in each lobe. Every type has at least one present cell as a target. 28 self-loops are present in
  each lobe.
- **R1's row and column: the same cells in both lobes** (3 row cells, 1 column cell), so no lobe
  difference outside the block lies in them.
- **Lobe agreement outside the block** (the within-animal reference of §4.3): of the 2,961
  outside cells, **493 are present in both lobes, 3 in L only and 33 in R only** (36 differ,
  1.22 %). The 3 L-only cells: (Tm5a, CT1(M10)), (Tm5c, Am), (TmY5a, CT1(M10)). The 33 R-only
  cells: (C2, Mi2), (C3, Tm16), (C3, Tm9), (L3, TmY18), (L4, L3), (L4, Mi14), (L4, Tm9), (L5, Tm20),
  (Lawf1, L3), (Mi1, Mi14), (Mi10, T4a), (Mi13, Mi9), (Mi13, Tm9), (Mi15, Mi14), (Mi9, T2),
  (Mi9, T2a), (T4a, Mi13), (T5a, TmY15), (T5a, TmY18), (Tm16, TmY15), (Tm2, T2a), (Tm20, T2a),
  (Tm20, TmY3), (Tm3, Mi10), (Tm3, Tm4), (Tm30, Tm5b), (Tm5Y, CT1(M10)), (Tm5Y, Mi10), (Tm5a,
  Tm30), (TmY13, T2), (TmY14, C3), (TmY9, Lawf2), (TmY9, Mi13). In 33 of the 36, both lobes' `x`
  lie within [0.5 `c*`, 2 `c*`]; across the 36, `x_L / x_R` ranges from 0.1 to 5.5. So the lobes'
  outside difference is mostly a difference near the cut, and it is directional (R > L), which is
  also why `c*_L` < `c*_R` (§11, expectations table). 74 (L) and 65 (R) outside cells have `x` in
  [0.8 `c*`, 1.25 `c*`).
- **Folds** (from `folds.csv` and the outside files): present outside cells per fold 51, 46, 47,
  43, 47, 51, 56, 52, 47, 56 (L) and 53, 48, 48, 47, 49, 55, 57, 55, 50, 64 (R); the 64 block cells
  fall 8, 4, 7, 6, 8, 4, 7, 8, 6, 6 into folds 0–9, as on flyvis-65 (bank-independent).

**The script recomputes these tables at run start, in every mode, from the outside files only,
and stops with "PRE-DATA TABLES DIFFER" if any differs from this section** (check 4, §3.4). The
male row of A's inferability table ("64 / 64 at every pair threshold tried (Zcode, preliminary
graph)") is replaced, for this arm, by "64 / 64 at `c*` in each lobe" (ledger row M(1), §11).

### 1.5 Prior exposure of male block A, and the read declaration

This repository says **prior exposure**, not "contamination" (B §1.5).

1. **The preliminary graph.** Block A of the male CNS was looked at before any registration, in
   Zcode's preliminary graph (A §8; builder §0). What the committed files record of it, as relayed
   and not verified from any file: under a summed threshold the block was a perfect board with 4
   mirror cells; **at an honest mean ≥ 1 (c = 1) it had 20–21 weak cross cells with means of
   1.0–2.2**, and 52–54 mirror cells under other definitions (builder §0, Zcode 2026-09-26 05:08
   UTC as relayed). Zcode's definitions (lobes, `n_tar`, `w_min`) are not written in any file.
2. **So the authors of this draft know a relayed description of block A at a cut below `c*`.**
   `c*` = 2.994 lies above the relayed means of the weak cross cells. A reader can form an
   expectation of the male block at `c*` from committed text. This file writes no such
   expectation and sets nothing from it: machine check 3 prints the block instead of comparing it
   with a count (§3.4, D8), no cut, rank, λ grid or seed is chosen with reference to it, and every
   gate and reading rule is A's, fixed before the male bank was built.
3. **flyvis-65's G is known** (§0), and so is the flyvis-65 block (public). The lobe-disagreement
   rule (§4.3) and the male readings against G (§5) are written after that verdict. They name
   their inputs, and none of them is the male block.
4. **The build's aggregates** (inferable, mirrors, smallest endpoint keep, at `c*` and at the
   diagnostic cuts) are outside-block numbers (builder §9) and are known.
5. **What no one has seen:** the male block at `c*` in either lobe. The sealed files have not been
   read (header).

**Read declaration (the drafting agent).** Opened in full: A (revision 3.4.1, all sections); the
builder (revision 2.1); B (revision 1.1); `BUILD.md`; `bank.meta.json` (the committed copy, key by
key); `knockout_regrow.py`; the relevant parts of `harness.py` (lines 1–260, 290–780, 850–930);
`flywire_bf_p3.py` lines 1–180; rule #2.1's `fit.py` lines 265–414 and a grep of the rest;
`RESULT.md` lines 1–120 of the flyvis-65 run; the blind review note; `idea.md`. Read from the
build folder: the file names (a listing without sizes); `pair_stats_outside.csv`,
`male_cns_L_outside.csv`, `male_cns_R_outside.csv` (the whole files, by a scratch script, for §1.4);
the committed `SHA256SUMS.txt` (hashes only). Read from git: `git show --stat cdbde9e` (the GPU
instrument's commit message, D13) and the last commit of each cited file. A grep of the
repository's `.py`, `.md` and `.json` files for 92000–92999 (§3.7). **Not opened:** either sealed
file, `summary.json` of the flyvis-65 run beyond what the blind review quotes, anything under
`chat/`.

## 2. The predictors (delta on A §2)

- **Unchanged:** rule #2.1 (`RANK = 1`, `STARTS = 10`) is the primary, with R/W read on both D1
  candidates (rule #2.1 and BF_1); BF_1–BF_4 with their nested λ; N1, printed, deciding nothing.
- **N1:** as B §2, its AUC is not confined to A's additive band unless the male block is
  balanced (§0); it enters no branch, and leg S subtracts it on every bank.
- **The two ceilings: definitions unchanged.** A's consequences 1–3 (the R world realisable,
  `ceiling_block` ≈ 1, permuted-block ceilings fall) hold for the synthetic boards, which are rank
  1, and are **not known** for the male blocks. On a male block, a `ceiling_block` below 0.90 can
  be a rank limit of rule #2.1 (its logit is `c + a_s + b_t + u_s v_t + W[G(s), G(t)]`), not only a
  failed fit (as B's D9; §4.1). The 20 permuted-block ceilings are printed, with no expected fall.
- **The existence bank (proposal, D5; builder §7, §12).** Every present cell of a male bank has
  exactly one offset, `(0, 0)`, with `n_syn = x` and sign +1. What each registered code path does
  with it, read from the code:
  - `make_view` (`harness.py:180-186`) copies `offsets` and `sign`; `hull` is not read.
  - N1 (`fit_n1`, `harness.py:350-408`): the existence fit reads `view.exists` only; the offset
    sets are all `{(0, 0)}`; the count terms fit `log1p(x)`; every source's sign vote is +1.
  - BF_r (`fit_bf`, `:710-731`): existence only, on N1's logit.
  - Rule #2.1 (`fit.py:315-356`, `:362-412`): its existence part (N1 + `u·v` + `W`) reads existence
    only; its offset library is built from one distinct set, so the library holds one set and
    both side choices return it; `m` holds one value.
  - `score` (`harness.py:490-508`): existence log-loss as usual; offset (Jaccard on `{(0, 0)}`),
    counts and sign are computed on placeholders.
  So **nothing in the existence path reads an offset, a count or a sign**, and the offset, count
  and sign fields are **meaningless on this bank**: the arm prints them under that label (S25).
  **Not verified by running:** that rule #2.1's offset branch, `eb_tables` and `data_bits` run
  without error on one distinct set. Two things check it before the sealed files are opened: a
  fixture test that trains, decodes and scores all six predictors on a synthetic world with male
  existence content (§7.3, test T5), and the pre-run itself, whose worlds carry only male
  existence content (§3.6). A failure there stops the arm before any real block score.
- The loader writes `"hull": []` (the harness's `canon_content`, `harness.py:903-904`, reads the
  key in every shuffle's invariant) and refuses any name outside the 55 placed types (S4).

## 3. Statistics (delta on A §3)

### 3.1 The metric

AUC, unchanged. The male block's labels need not be balanced, so the denominators are `n_present`
/ `n_absent`, which the verdict line already prints (`knockout_regrow.py:1251`). Printed beside
it, deciding nothing, as in A, with three adaptations (D8): **precision at `n_present`** in place
of precision at 32; A's **four quadrant means** (ON × T4, OFF × T5, ON × T5, OFF × T4), unchanged,
since the answer key is the same; the **AUC on the other 61 cells** (not the three mirror partners)
in place of "the other 59". The block's present pattern is printed after unsealing (§3.4, check 3).

### 3.2 The legs

- **Leg S: unchanged in form.** For each lobe, `harness.shuffled_bank(bank_ℓ, sd)` for `sd` in
  0..98, where `bank_ℓ` is the lobe's full male bank (outside cells and, in the real run, the
  present block cells). The same knockout by name, the AUC margin over N1, `n_ge = 0` of the
  `99 − n_deg` shuffles with an AUC (A's D14 (ii)), `n_deg` named above 5. A shuffle keeps the
  lobe's degrees, block included, and stays on the placed grid (§1.3). If the male block is
  sparse, a shuffled block is all absent more often; `n_deg` is printed.
- **Leg P: unchanged in form:** 9,999 uniform permutations of the 64 labels from one generator
  (seed 92000, §3.7), `p_P = (1 + #{AUC_perm >= AUC_real − TAU}) / 10,000`, passing at `<= 0.01`.
  The AUC needed moves with the counts. The null's standard deviation is
  `sqrt((n_p + n_a + 1) / (12 n_p n_a))`: 0.0727 at 32/32, 0.0785 at 20/44, 0.0840 at 16/48, 0.1002
  at 10/54 (arithmetic, this draft). The script prints the exact value.
- **`smallest_passing_auc`:** unchanged in definition, on the grid `k / (n_p n_a)` (A: `k / 1024`).
  Its registered values for boards `z` and `z'` are read from the arm's own pre-run references
  (§3.3). **When no AUC on the grid gives `p_P <= 0.01`** (for example `n_present` = 1 or 63: a
  single present cell ranked first still leaves about 1 in 64 permutations tied or above, `p_P` ≈
  0.016), leg P cannot pass on that block, so R and W are unreachable by construction. **That lobe
  reads U with its own text, "not readable: leg P cannot reach p_P <= 0.01 on this block
  (n_present = k of 64)"**, never renamed by the U rule and not counted as a threshold U (D8).
- **`TAU` stays inert:** every AUC is a multiple of `1 / (2 n_p n_a)` with `n_p n_a <= 1,024`, so
  two unequal values on these lattices differ by at least `1 / (4 · 1,024²)` ≈ 2.4e-7 ≫ 1e-9 (as A
  §3.2).
- **Row-and-column variant (printed, decides nothing; D9).** 8 × 8 patterns with the block's row
  and column counts, 640 successful checkerboard swaps per chain from the block's own pattern,
  seed 92001. `reshape(8, 8)` and `integers(8)` are right for block A on any bank (unlike B's 5 × 8,
  B §3.2). **New guards (builder §12; Ark, Zcode):**
  1. **Before the loop:** a pattern with no 2 × 2 checkerboard admits no swap; its row-and-column
     null has one pattern, and the variant prints "n/a: the row-and-column null has one pattern".
  2. **An attempt cap** on the harness's pattern (`harness.py:881-883`: `cap = 100 * target`, loop
     `while … succ < target and att < cap`): each chain may make at most 100 × 640 = 64,000
     attempts. A chain finishes under the cap only if at least 1 % of its attempts succeed. On the
     32/32 board, 1,024 of the 4,096 ordered attempts are checkerboards (25 %); a sparse or nearly
     nested real block can fall below 1 % although it is swappable.
  3. **What a cap hit does (D9):** in a synthetic world (every block is a 32/32 board) it is a
     malfunction and **stops the synthetic step** ("ROW-AND-COLUMN NULL: ATTEMPT CAP REACHED
     (chain …, successes …, attempts …)"). **On a real male block it does not stop:** the variant
     prints "n/a (attempt cap reached: chain …, successes …, attempts …)" and the run goes on. The
     variant decides nothing, and the real run is made once, after the seal is broken (§7.4); a
     stop there would forfeit the registered run for a diagnostic.
- **Leg N1:** printed, decides nothing; on the male block it is not "uninformative by algebra"
  (§0).

### 3.3 Uniqueness, determinism and the reproduction gate (delta on A §3.3)

- **Unchanged:** the determinism check; no seed enters the primary numbers except `p_P`'s; the
  reproduction gate on the deciding columns, rows matched by key, outcomes 1–3 with parts (a) and
  (b), the four layers and their order of reading, the self-test's two outcomes, the null-input
  digests, the per-fit diagnostic (deciding nothing), the store's declared fields, "a pin is
  integrity, not reproducibility", "a red pin is never answered by re-pinning".
- **Changed: run once, and never dirty.** The real arm runs once, at a committed head, with the
  tree clean. **`--allow-dirty` is refused with the male arm** (D10): A lets a dirty real-arm run
  go on, marked "NOT THE REGISTERED RUN", but any run of the real arm opens the sealed files, and
  the builder allows that "in its registered real run only" (builder §9). A dry run of the real
  arm does not exist; the real arm's code paths are exercised before the seal is broken on
  synthetic banks (§7.3).
- **New references, one per lobe (B §3.3's reasoning).** The gate compares with the arm's own
  pinned pre-run references, two new folders (proposed
  `connectome-seed-data/knockout_regrow/synthetic_malecns_L_prerun/` and `…_R_prerun/`), each with
  its own `PRERUN_DIR`, `PRERUN_SHA256` and `PRERUN_WORLDS_CSV_SHA256`. A's and B's references are
  not touched. Each is made by one fitting run from a committed head (D15), so two of A's four
  reasons against a byte gate (mixed fits; no producer in git) do not arise; the other two (the
  `DYNAMIC_ARCH` kernel; the gzip mtime) do, so the column gate is kept. The per-fit diagnostic is
  split by kind of fit only.
- **Registered values, read from each lobe's reference (one address, A revision 3.4.1 item B):**
  `smallest_passing_auc` for boards `z` and `z'`, and the `ko1` count (copied and fitted). **Their
  values do not exist yet.** The revision of this file that follows the pre-run states them,
  verified on the pinned files. Because both lobes use the same leg-P seed and the same boards
  (§3.6, §3.7), **the two lobes' `smallest_passing_auc` values must be equal board by board**; the
  script asserts it.
- **Both lobes' gates pass before either sealed file is opened** (§4.2, §7.4). A failed stop row or
  a failed reproduction in either lobe stops the arm with both blocks sealed.

### 3.4 Machine checks (delta on A §3.4)

Per lobe unless marked. Checks 1, 2, 4, 7 and 10 run in every mode; checks 6 and 9 run in the real
arm before the seal is broken; check 3, check 5, check 6′ and check 11 run after it.

| check | male CNS arm |
|---|---|
| 1 pins | A's eight pins; the six male files of §1.1 (the sealed files by hash only, and only in the real arm before opening; §7.4); Python 3.10.20 and numpy 2.2.6; rule #2.1 with `RANK == 1` |
| 2 block and mask | 64 cells, 8 sources, 8 targets, all 16 names in the placed set; on the placed grid the knockout view has 2,961 cells, none in the block; the full view 3,025; the block view 64 |
| 3 board | **no reviewed count exists** (A §8: "set by the builder's registered threshold"; §1.5). Replaced by a print, after unsealing: the block's present count, the four quadrant counts, the row and column counts, whether `y_st = x_s · w_t` (flyvis's board), and whether the block is balanced (4 of 8 in every row and column). It stops that lobe only if the block has no AUC (0 or 64 present: "BLOCK HAS NO AUC") (D8) |
| 4 pre-data tables | §1.4's endpoint table, 64 / 64 inferable, the three mirrors, the training present count (496 / 526), R1's and CT1(M10)'s row and column cells, and the lobe agreement (493 / 3 / 33) must match, else "PRE-DATA TABLES DIFFER". From the outside files only |
| 5 N1 parity identity | `D(N1 logit)` printed with the balance of check 3; no stop (it is 0 only on a balanced block) (D8) |
| 6 leakage | **before unsealing:** the knockout fit of rule #2.1 on the lobe's bank with its block filled two ways (all absent; the board `z`) must give byte-identical data dicts. **6′, after unsealing:** the same fit on the real lobe bank must give the same hash ("BLOCK LEAKS INTO TRAINING") |
| 7 AUC function | A's hand cases, plus one unbalanced 64-cell case |
| 8 harness identity (once) | unchanged: BF_1's full-bank C6 existence margin on flyvis-65 reproduces 0.028150051052145946 to 1e-9, **run before any grid restriction**, in a pool that does not restrict (§1.3) |
| 9 determinism | before unsealing, the knockout fit twice on the lobe's knockout view (block excluded by the mask) |
| 10 grid (new) | `len(H.ALL_CELLS) == 3025` in the main process after the restriction and in every fit in every worker; the lobe's bank has no cell outside the placed set |
| 11 sealed file (new, after unsealing) | the file's sha256 equals its pin before it is opened; 64 rows; the names are exactly the 64 block cells; `present == (x >= c* and x > 0)` on every row, with `c*` from `bank.meta.json`; else "SEALED FILE INCONSISTENT", which stops the arm (§7.4) |

### 3.5 What is printed

As A §3.5 per lobe, with the adaptations of §3.1 (precision at `n_present`, the other 61 cells),
the three mirror partners, per-type rows for the 16 types (where a type's cells hold both labels),
the 20 permuted-block `ceiling_full`, the fixed λ = 1 diagnostic, and, beside the verdict and never
on it: `D(N1 logit)` (former check 5), N1's own `p_P` beside any U (as B's D8), the block pattern
of check 3, the lobe comparison of §4.3, and the offset, count and sign fields under the label
"meaningless on an existence bank". **The within-fly note** (A's `WITHIN_FLY_NOTE`, about FlyWire)
is replaced by the within-animal note: "within the animal, outside block A: the two lobes differ on
36 of 2,961 outside cells at `c*` (1.22 %; about 0.8 of 64 cells if spread evenly); 33 of the 36
are within a factor 2 of the cut".

### 3.6 Synthetic worlds (proposal, D6; builder D13)

**Why A's limits do not transfer.** A's limits (γ\*_P = 0.6, γ_R = 0.75, family limit 0.75) and
its `smallest_passing_auc` values belong to A's instrument on A's worlds: N1's degree terms fitted
on flyvis-65's knockout view, the 65-type grid, outside density 0.1375, and flyvis content with
real offsets (A §3.6, "The instrument", "Units"). The male banks differ in all four: degree terms,
the 55-type grid, density 0.1675 / 0.1776 (×1.22 / ×1.29 of A's), and existence-only content. A
limit in "M-world units" is a coefficient of `z_s z_t` on top of those degree terms, so it moves
with them. The recommendation is to rebuild the worlds on each lobe (D6 (b)).

**Kept unchanged:** the nine families (R, Nf, No, W, M0.5, M0.6, M0.75, M0.85, M1.0) with the same
γ values (`gamma_z`, `gamma_z1`), 5 worlds each, 45 worlds per lobe; the boards `z` and `z'` on
the 16 block types, by name (A's `Z_PLUS`, `ZPRIME_PLUS`, and both orthogonality assertions,
`knockout_regrow.py:261-262`, `:689-690`); the requirement rows and their stops (R each R; Nf never
R or W, at least 3 of 5 G; No never R or W, reads G, a U triggers the No contingency; W each W; the
M rows a power curve with no stop); the three limits, their brackets, the transition band, the
binomial note, the U rule (threshold U only); the fixed λ = 1 diagnostic with its path check; 99
shuffles and 20 permuted-block ceilings per world; the rule that a failed stop row stops the real
arm.

**Changed (per lobe):**

- **The grid:** each world lives on the placed grid. Every cell with an unplaced endpoint is
  absent (`make_world` sets them absent and asserts it), so no shuffle of a world can move an edge
  onto an unplaced cell (S14).
- **The other types:** `OTHERS` = the 39 placed types outside the 16 block types (A: 49); `z` and
  `z1` are drawn for them in ascending harness index, as in A.
- **Degree terms:** N1's `(c, a, b)` fitted on the lobe's knockout view on the placed grid (the
  outside bank only; no sealed file). At γ = 0 a world's outside density is then near the lobe's.
- **Content pool:** the lobe's present outside cells (496 or 526 existence rows); a world is an
  existence bank like the real one, so the pre-run exercises the existence path of every predictor
  (§2).
- **`outside_density`:** the mean over the 2,961 placed outside cells.
- **Limits:** each lobe's G label prints that lobe's limits. They are not compared with A's or with
  each other as numbers (as B §3.6); both are printed.
- **The expectations of A §3.6** (R reads R, Nf reads G, No reads G, W reads W) carry over by the
  same algebra on the same boards. They are expectations until the pre-run measures them. On a
  denser bank the M worlds may be seen at lower γ; a limit reached at γ = 0.5 prints the bracket
  (0, 0.5] (`grid_limit`, `knockout_regrow.py:1656-1675`), and that is read as the grid's
  resolution.
- **What the worlds cannot match:** every world's block is a 32/32 board. The male block's count
  and shape are sealed, so the limits are measured on boards whatever the real block turns out to
  be (§6).

**Cost (A §7's measured rate, 3.65 fits per second on 30 CPU workers; assumed to hold on the placed
grid, where every array is still 65 × 65):** one lobe's synthetic step is 45 × (3 × 6 + 20 + 99 × 6)
= 28,440 fits, about **2 h 10 min**; both lobes about **4 h 20 min**. The pre-run and the registered
run's refit together: about **8 h 40 min** of CPU wall time, plus the real blocks (§7.5).

### 3.7 Seeds (proposal, D7; all new; the script asserts that they are distinct)

| use | seed(s) | generator |
|---|---|---|
| leg P, uniform permutations | 92000 | `default_rng(92000)`, 9,999 × `permutation(64)` in order |
| leg P, row-and-column-preserving | 92001 | `default_rng(92001)` |
| ceiling on permuted blocks | 92010–92029 | `default_rng(92010 + j)`, `j` = 0..19 |
| synthetic worlds (family index `i` in A's order R, Nf, No, W, M0.5, M1.0, M0.6, M0.75, M0.85 = 0..8; repeat `j` = 0..4) | 92100 + 10 i + j (92100–92184) | `default_rng`, draws in A's order, over the 39 placed others |
| shuffles of each lobe's bank and of each world | 0..98 | `harness.shuffled_bank(base, sd)`, reused on purpose, as in A |
| BF / rule #2.1 ALS starts | `PCG64(30000 + j)` | fixed in the harness |

**The same seeds serve both lobes** (common random numbers): the two lobes' worlds differ only by
their degree terms and content pools, and their leg-P nulls are the same permutations, so a
difference between the lobes cannot come from a draw. **A §8 says "the same legs, cuts, seeds and
branch rule apply"**; this table replaces A's seeds with new ones (D7 records the choice and its
reason). **Untouched:** A §3.7's list (60000, 61000, 70000–70999, 80000–80999, 4242, 99, 7,
1000–1019, the dial seeds, 20260923), A's own seeds (90000, 90001, 90010–90029, 90100–90154,
90160–90184) and B's (91000, 91001, 91010–91029, 91100–91184). **Checked 2026-09-26 UTC:** a grep
of the repository's `.py`, `.md` and `.json` files for 92000–92999 found no seed: the hits are
digits inside floating-point values (`results/genome/c6/rules/second_rule/diagnosis_power_rows.json`)
and two neuron-pair row counts in `BUILD.md` (92745 and 92100, lines 159 and 168) and their copies
in `bank.meta.json`. The script asserts that the new seeds are distinct, lie in 92000–92999, and
meet none of the untouched, reused, block-A or block-B seeds.

### 3.8 Vocabulary (additions)

- **Lobe** L or R: the builder's lobe (side, with the CT1 flip; builder §4). **A lobe's bank** =
  its outside bank plus, in the real run only, its present block cells.
- **Sealed**, **unsealing:** the builder §9 rule; unsealing is the first opening of a sealed file,
  in the registered real run (§7.4).
- **Split:** the two lobes read different letters (§4.2).
- **Present in the block:** A §3.8's two carriers, with 32 in every synthetic world and the real
  count unknown before the run.

## 4. Reading rule

### 4.1 Per lobe: A §4, verbatim, with four stated differences

A §4 applies **verbatim** to each lobe: the four branches in order, R and W on both D1 candidates,
the cuts (`P_R` = 0.01, `P_W` = 0.0125, `P_G` = 0.10, `GATE_CUT` = 0.90, `MECHANISM_CUT` = 0.90),
the U rule's naming (per lobe, on that lobe's dense grid), the verdict line's contents, λ on the
verdict line, the No contingency (per lobe). No condition, cut or existing label string changes.
Four differences (D12):

1. **A lobe prefix.** Each verdict line starts "male CNS, lobe ℓ (existence bank at c* = 2.99436):".
2. **A new U text** for a block on which leg P cannot pass (§3.2): "U: not readable: leg P cannot
   reach p_P <= 0.01 on this block (n_present = k of 64)". It takes precedence over G, is never
   renamed by the U rule and is not a threshold U. A lobe whose block has no AUC stops with "BLOCK
   HAS NO AUC" and has no label (check 3).
3. **The quoted rows carry A's literals.** A's G row says "by Johnny's count the information is
   there (64/64 inferable)", which holds on the male banks too (§1.4); its U row says "all 3
   pre-run U worlds sit at γ = 0.6 = γ\*_P" and "by §2.4 this is a failure of the fit, since the
   block is rank 1". The script prints, after each quoted row, one line naming which literals are
   A's (the flyvis-65 pre-run U worlds; "the block is rank 1") and giving the lobe's own values.
4. **"Failed fit" on a male block** keeps its text ("failed fit: rule #2.1 cannot hold the block
   even when trained on it alone"), which states the measurement; it is read as "a failed fit or a
   rank limit, not separated", since the male block is not known to be rank 1 (B's D9).

### 4.2 The two lobes: one run, two labels, one male reading (proposals, D2, D3)

**One invocation, both lobes (D2).** Both lobes' synthetic steps run and must pass before either
sealed file is opened; then both blocks are unsealed and both real arms run, in one invocation from
one committed head with one manifest (§7.4). So neither lobe's verdict is seen before the other's
run is fixed. Each lobe gets its own label by §4.1.

**The male reading (D3), from the two lobe labels:**

| lobe L | lobe R | male reading |
|---|---|---|
| R | R | **R: regrows in both lobes of one animal** (builder D12 (i): an R on the male CNS needs R in both lobes) |
| W | W | **W** in both lobes; the ranks that passed are printed per lobe |
| G | G | **G** in both lobes, each with its own limits |
| U | U | **U** in both lobes, each with its own U text |
| any other pair | | **split: "lobe L reads X, lobe R reads Y"**, with the classification of §4.3. A split is not R, W or G on the male CNS |
| a lobe with no AUC or "not readable" | | **one lobe only: "lobe ℓ reads X; lobe ℓ′ cannot be read (reason)"**. Not a male R even if X is R |

### 4.3 A split: the rule that separates its explanations (proposal, D4; builder D12, §12)

The builder named two explanations of a lobe disagreement, variation within the animal and a
difference of reconstruction between the lobes, and handed the separating rule to this arm, with
the R1 row and column as a named obligation (builder §4, §12). **The build's facts change what can
be separated:**

- **The R1–R6 asymmetry cannot carry a split.** R1–R6 is not a block type, so it enters block A
  only through training, through R1's row and column. At `c*` those are **the same 3 + 1 cells in
  both lobes** (§1.4; `BUILD.md` line 185). The builder's registered expectation, a sparser R1 row
  and column in lobe L, did not appear (§11). **Registered answer to builder §12's question:** no
  lobe difference is confined to R1's row and column, because there is none there; if one appears
  (a changed file), check 4 stops the run.
- **No cross-lobe edge exists among the placed types** (0 of 2,332,880 rows), so the two lobe banks
  share no neuron pair, and a lobe difference cannot be a mis-assigned side through connectivity.
- **The block types are even in bodies** (R/L 0.987–1.020, §1.2). A reconstruction difference of
  the block types in body counts is not seen; one in synapse counts is not measured here.
- **The outside is not even in `x`:** at the shared cut the right lobe has 30 more present outside
  cells (526 against 496), 33 R-only against 3 L-only, 33 of the 36 near the cut (§1.4). A lobe-wide
  difference in `x` near the cut exists, of unknown mechanism (synapse detection, reconstruction of
  synapses, or biology).

**The classification of a split (registered before data; printed with every split and, as a
diagnostic, when the lobes agree).** After unsealing, let `y_L`, `y_R` be the two blocks' present
patterns, `k` the number of the 64 cells whose presence differs, and `k*` = **4**, the smallest `k`
with a binomial tail `P(X >= k) <= 0.01` for `X ~ Binomial(64, 36 / 2,961)` (the outside
disagreement rate of §1.4; tails 0.543, 0.183, 0.043, **0.0078** for k = 1..4; arithmetic, this
draft):

| class | condition | reading |
|---|---|---|
| **S0: same block** | `y_L = y_R` | "Block A is the same in both lobes at `c*`; the split comes from the instrument's response to the lobes' other differences (36 of 2,961 outside cells) or from the threshold of detection, not from block A." |
| **S1: differs like the rest of the lobe** | `1 <= k < k*` | "Block A differs between the lobes in k of 64 cells, within the lobes' outside rate (36 / 2,961, expected about 0.8 of 64): not read as a difference specific to block A. Variation within the animal and a reconstruction difference are not separated." |
| **S2: differs more than the rest of the lobe** | `k >= k*` | "Block A differs between the lobes more than the rest of the lobe does (k of 64; P(X >= k) = … under the outside rate): a difference specific to block A. Its two explanations, variation within the animal and a difference of reconstruction or typing of the block types, are not separated by this test. The R1–R6 asymmetry is excluded as its carrier (R1 is not a block type, and R1's row and column are the same cells in both lobes at `c*`)." |

Printed with the class: each differing cell by name with its presence in each lobe, whether both
lobes' `x` lie within [0.5 `c*`, 2 `c*`], and the direction count (L-only against R-only) beside the
outside's 3 against 33. **The binomial reference is descriptive**: block cells are not a random
sample of outside cells (they are strong medulla-to-lobula-plate pathways, not a random draw of
type pairs), and the class decides no label. It separates "a block-specific difference" from "a
lobe-wide one". It does not separate variation within the animal from reconstruction; nothing in
one animal's two lobes can (§6).

## 5. What each outcome means, and the joint reading with flyvis-65 (delta on A §5, §8)

**A's D13 table stands** (A §8, voted "as written" by Ark and Johnny on 2026-09-24): R on both =
"regrows in the template and in one animal"; R on flyvis-65 only = "regrows in the averaged
template only; the animal does not show it"; R on the male CNS only = "a flag to re-examine both
fits"; any other pair = "the flyvis-65 label stands alone, with the control's label printed
beside". "R on the male CNS" means the male reading R of §4.2 (both lobes).

**flyvis-65 read G, so the joint readings reachable now are these (proposal, D16; each follows
A's D13 and adds its reading):**

| male reading | A's D13 row | reading (registered before data) |
|---|---|---|
| **R** (both lobes) | R on the male CNS only: a flag | **Neither verdict is overturned.** flyvis-65's G stands. The male R reads: "regrows in both lobes of one animal, on an existence bank at one cut; the template does not show it at the R level." The flag is a registered list of what must be examined, **under a new registration, not by a rerun**: (i) the averaging of flyvis-65 (per offset, merged over two flies, column-averaged) against one animal's type-pair means (builder §8), the column-test anchor of A §0 in the other direction; (ii) the threshold: the male block is cut at `c*`, chosen on outside cells, and flyvis's by eq. 8 per offset; (iii) the prior exposure of §1.5; (iv) typing by connectivity in the male CNS (A §6). No consequence for the forward path is drawn from a male R alone |
| **W** (both lobes) | any other pair | flyvis-65's G stands alone. Printed beside it: "in both lobes of one animal the outside implies block A for a BF_r while rule #2.1 misses; on the template no BF_r passed". It bears on A's column-test anchor (averaging may hide information the animal carries) and on the rule (W); it changes no registered label |
| **G** (both lobes) | any other pair | Agreement: "not detected at the R level in the template or in either lobe of one animal, each against its own limits". The limits are not compared across banks as numbers (§3.6). A G in the animal does not strengthen flyvis-65's G beyond its own limits; it removes "an artefact of averaging" as the only explanation of flyvis-65's G |
| **U**, split, one lobe only | any other pair | flyvis-65's G stands alone; the male reading, its lobe labels and, for a split, its class (§4.3) are printed beside it |

**Per lobe**, A §5's table applies to each lobe's label, with "the block" meaning that lobe's
block and "on flyvis's averaged template" replaced by "in lobe ℓ of one male, on an existence bank
at `c*`".

## 6. What the test cannot show (delta on A §6)

A §6 applies, except its male-CNS item, which this arm replaces, and in addition:

- **One animal.** Two lobes of one male are not two animals. A split's class separates a
  block-specific difference from a lobe-wide one; it cannot separate variation within the animal
  from a reconstruction or typing difference (§4.3). A second male, or a female, is not in this
  registration.
- **One cut.** The verdict is at `c*` = 2.994 (`w_min` = 1). The builder printed the outside at
  other cuts (`BUILD.md` lines 188–238); the block at those cuts is not scored.
- **An existence bank.** No offsets, counts or sign exist on it (builder §7, D8); those fields are
  meaningless here. The within-type averaging to one mean per type pair is itself an averaging
  (over the target neurons of a lobe), though not over columns or animals.
- **Boards in the worlds, an unknown block in reality.** The limits are measured on 32/32 rank-1
  boards (§3.6). If the male block has another count or shape, its G is still stated against those
  limits, in M-world units, on the lobe's degree terms.
- **The G gate is not automatic,** since the male block is not known to be rank 1 (§2).
- **No parity or degree argument protects the male block** (§0).
- **The side of the photoreceptors is a transfer** through `rootSide` (builder §1.2); R1, R7 and R8
  are training endpoints only. The lobe-consistency check passed trivially (§0) and did not test
  it.
- **The unplaced types** (Mi3, Mi11, Mi12, Tm28 absent; R1–R6 and CT1 pooled) make the male
  training view differ from flyvis-65's in ways that no gate reads (builder §8).
- **Prior exposure** (§1.5): the male block was seen at other cuts before this design, and this
  design is written after flyvis-65's G.
- **Typing by connectivity** (A §6; candidates note, risk 2): if the male CNS's T4/T5 or Tm/Mi
  labels lean on connectivity, part of block A may be true by definition. Unverified.

## 7. Environment, script, tests, the unseal protocol, run commands, outputs, cost

### 7.1 Environment and instrument (proposal, D13)

Unchanged: `tools/.venv` (Python 3.10.20, numpy 2.2.6), CPU, the pinned numpy harness, 30 workers,
`--starts 10`. The arm reads CSV files, so it needs no pyarrow and no `uv` environment. **The GPU
instrument is not used.** It is a separate instrument (A §7), unreviewed; its commit `cdbde9e`
reports BF_1–BF_4 on the 45 worlds in 39 min against about 89 min on the CPU pool, rule #2.1 not yet
faster than the pool, and base-view fits not all bit-equal (BF 175 / 180, rule #2.1 42 / 45; the
rest within 6e-8). It would need its own registration and synthetic worlds (A §7), and it would
shorten only the BF part of the wall time (four of the six predictors; rule #2.1 is not faster).

### 7.2 Script changes (listed; none is made by this draft; D14)

| # | where (A's script, lines at `74db080`) | change |
|---|---|---|
| S1 | the file | a new script, `results/genome/c6/checks/knockout_regrow_male_cns.py`, a copy of A's with the changes below, reviewed as a diff against it; A's script stays byte-unchanged; a new label test beside A's |
| S2 | `REGISTRATION`, `REGISTRATION_REVISION`, the manifest (:109-110, :2583-2601) | this file and its revision; A's registration path pinned by its LF sha256 **after** the D11 amendment, because §4 is quoted from it (`quote_row` :2373-2379, `quote_section` :2367-2370); the builder's registration and `bank.meta.json` recorded |
| S3 | `PINS` (:139-156) | the six male files of §1.1, beside A's eight; the sealed files' hashes kept apart (`SEALED_SHA256`) and checked only in `open_sealed` (S21) |
| S4 | new: the loader | `load_male_bank(lobe)` reads `male_cns_<lobe>_outside.csv` (`src, tar, du, dv, n_syn, sign`), builds `{"offsets": {(0, 0): n_syn}, "hull": [], "sign": 1}` per present cell, refuses a name outside the 55 placed types, a block-A cell ("BLOCK ROW IN OUTSIDE FILE"), an offset other than `(0, 0)` or a sign other than +1, as `load_flywire_bank` does (`flywire_bf_p3.py:85-98`) |
| S5 | new: the grid | `restrict_to_placed_grid()` replaces `H.ALL_CELLS` with the 3,025 placed cells (`flywire_bf_p3.py:73-75`); called in `main` after check 8 and in `_w_init` (:782-786) for every worker; `_w_group` (:834) asserts `len(H.ALL_CELLS) == 3025` |
| S6 | every `H.REAL` (:691, :694-698, :754-757, :2466-2472, :2554, :2556) | the lobe's male bank; check 8 stays on flyvis-65's `H.REAL` on the full grid, run before S5, in its own pool with an initializer that does not restrict |
| S7 | `N_TRAIN_CELLS, N_TRAIN_PRESENT` (:192), `check_block_and_mask` (:418-432) | 2,961 per lobe; 496 (L), 526 (R); the view counts 2,961 / 3,025 / 64 on the placed grid; all 16 names in the placed set |
| S8 | `ENDPOINTS_EXPECTED`, `INFERABLE_EXPECTED`, `MIRRORS_EXPECTED`, `MIRROR_IDX`, `INFERABILITY_PROVENANCE` (:196-209), `check_pre_data_tables` (:466-475) | per lobe, §1.4; three mirrors; the male row "64 / 64 at c* in each lobe"; added: R1's and CT1(M10)'s row and column cells, and the lobe agreement 493 / 3 / 33, computed from `pair_stats_outside.csv` |
| S9 | `check_board` (:435-445) | the print of check 3 after unsealing, and the "BLOCK HAS NO AUC" stop per lobe (D8) |
| S10 | `check_n1_parity` (:492-498) | a printed value with the balance, no stop (D8) |
| S11 | `check_auc_function` (:539-561) | one unbalanced 64-cell hand case |
| S12 | `SEED_*` (:248-251), `assert_seeds_unique` (:665-675), `reserved_seeds` (:649-656) | 92000, 92001, 92010, 92100; range 92000–92999; A's and B's seeds in the reserved set |
| S13 | `rc_patterns` (:596-624) | the no-checkerboard pre-check ("n/a: the row-and-column null has one pattern"); an attempt cap of 100 × 640 per chain (`harness.py:881-883`); a cap hit stops a synthetic step and prints "n/a (attempt cap reached: …)" on a real block (D9); `RC_SWAPS` stays 640 |
| S14 | worlds: `OTHERS` (:681), `NONBLOCK_CELLS` (:691), `degree_terms` (:694-698), `make_world` (:701-728), `outside_density` in `_w_group` (:866) | the 39 placed others; the lobe's outside content pool; N1 on the lobe's knockout view on the placed grid; every unplaced cell absent, asserted; the density over the 2,961 placed outside cells |
| S15 | `precision_at_32` (:909-912), `auc_other_59` (:1039, :1075), the CSV header (:2251-2257), `print_bank` (:2069-), `md_bank_table` (:2382-2396) | precision at `n_present`; the other 61; the arm's own CSV column names (its references are written by this script); "AUC (n_p/n_a)" |
| S16 | `smallest_passing_auc` (:924-937), `read_label` (:1151-1185), `label_text` (:1208-1233), `u_kind` (:1139-1148), `u_rule` (:1784-) | the docstring (`k / (n_p n_a)`); `None` gives the "not readable" U of §3.2, a U kind of its own, never renamed, not a threshold U |
| S17 | `PRERUN_DIR`, `PRERUN_SHA256`, `PRERUN_WORLDS_CSV_SHA256`, `PRERUN_REV2_FAMILIES`, `PRERUN_REV3_FAMILIES`, `_mech_renamed_32` (:124-136, :1336-1338) | one reference per lobe, set in the revision after the pre-run (D15); A's revision-2/3 split and revision 3.2's rename check are A's history and not needed |
| S18 | `out_dir_refusal` (:2307-2333) | refuses `--out` at or in A's reference, B's (once it exists) and both male references, and on byte copies of any of them |
| S19 | `write_committed`, `OUT` (:111, :2425-2459) | `results/genome/c6/checks/knockout_regrow_male_cns/`; a title naming the arm; the male reading first, then each lobe's verdict line, the quoted §4 row and the line naming A's literals (§4.1); the joint reading with flyvis-65 (§5); per-lobe `per_shuffle_<lobe>.csv` and `synthetic_worlds_<lobe>.csv` |
| S20 | `main`, `--arm` (:2498-2533) | `--arm malecns` runs both lobes (§4.2); `--synthetic-only --lobe L|R` for the pre-run; `private_run_dir` gives `malecns_<UTC stamp>_<head 12>`; **`--allow-dirty` refused with `--arm malecns`** (D10) |
| S21 | new: the unseal step | `open_sealed(lobe)`, called only from the real-arm path after both lobes' synthetic steps and checks 1, 2, 4, 6, 7, 8, 9, 10 have passed: checks the sha256 first, then parses the fixed-width file, runs check 11, returns the present block cells with `n_syn = x`; prints the file's cross-lobe block-weight line after the verdicts (§7.4) |
| S22 | `machine_checks_real` (:2464-2495) | checks 6 and 9 before unsealing on the two synthetic block fillings; check 6′ after unsealing against the pre-unseal hash |
| S23 | new: the lobe comparison | `lobe_split_class(y_L, y_R, x_L, x_R)` (§4.3, with `k*` computed from 36 / 2,961 and checked equal to 4) and `male_reading(label_L, label_R)` (§4.2); the joint reading with flyvis-65 (§5) as a table lookup, no computation |
| S24 | `WITHIN_FLY_NOTE` (:237-239), the `TAU` comment (:228-233) | the within-animal note of §3.5; the lattice text made generic |
| S25 | `print_bank`, `md_bank_table`, `summary.json` (the D7 fields, :1077) | the offset, count and sign fields printed under "meaningless on an existence bank" |
| S26 | `SEAL_RECORD`, new | a constant, "intact" in this revision; if a registered amendment records a break of the seal before review, the verdict lines end with the builder's note "block A of the male CNS was read before its registration was reviewed" (builder §9) |
| S27 | tests | §7.3 |

### 7.3 Tests (fixtures and synthetic banks only; no sealed file)

- **T1:** copies of A's 17 label tests, adapted to the arm's references and texts (as B's S22).
- **T2, the grid:** after `restrict_to_placed_grid()`, the three views count 2,961 / 3,025 / 64;
  a worker started by the pool reports 3,025; the loader refuses an unplaced name and a block row.
- **T3, the seal:** a spy on `open_sealed` records **zero calls** in `--synthetic-only`, in every
  other test and in the pre-unseal part of the real-arm path run against fixture files; with
  fixture sealed files of the builder's fixed-width format, `open_sealed` refuses a wrong hash
  before reading a byte, and check 11 refuses a row whose `present` contradicts `x` and `c*`.
- **T4, the leak (check 6):** on a synthetic lobe bank, the knockout fit's data dict is
  byte-identical under the two block fillings and under a random third.
- **T5, the existence bank:** one world with male existence content (fixture content pool): N1,
  rule #2.1 and BF_1–BF_4 train, decode and score on the `ko`, `full` and `block` masks at
  `--starts 3`; the existence log-loss is finite; the offset, count and sign fields exist and are
  labelled meaningless.
- **T6, the worlds:** every unplaced cell is absent; 39 others; 32/32 on both boards; the No
  algebra's exact 0.5 on board `z'` holds on the placed grid.
- **T7, `rc_patterns`:** the 32/32 board completes; a fixture pattern with no checkerboard prints
  "n/a: the row-and-column null has one pattern"; a fixture pattern with a success rate below 1 %
  reaches the cap and stops in a synthetic step, prints "n/a (attempt cap reached: …)" in the real
  path.
- **T8, readability:** `n_present` = 1 and 63 give `smallest_passing_auc = None` and the "not
  readable" U; 0 and 64 give "BLOCK HAS NO AUC".
- **T9, the lobe rules:** `male_reading` on all 16 letter pairs and the one-lobe cases;
  `lobe_split_class` on hand-made `y_L`, `y_R` (S0, S1 with k = 3, S2 with k = 4); `k*` = 4.
- **T10, seeds and refusals:** the seed assertion; `--allow-dirty` with `--arm malecns` refused;
  `out_dir_refusal` on all four reference folders (monkeypatched to temporary folders, never the
  real ones, as A's `test_out_guard_refusals`).
- **T11, check 3 and 5 as prints:** a fixture block that is not a board prints its counts and does
  not stop; `D(N1 logit)` is printed.

### 7.4 The unseal protocol (proposal, D10)

1. The sealed files are opened **only** by `open_sealed`, **only** in `--arm malecns`, **only**
   after: the tree is clean and committed (no `--allow-dirty`); checks 1, 2, 4, 7, 8 and 10 have
   passed; both lobes' synthetic steps have passed their stop rows and their reproduction gates;
   checks 6 and 9 have passed on both lobes before unsealing.
2. `open_sealed` checks the file's sha256 against its pin before reading it. A mismatch stops the
   arm with the seal intact ("SEALED FILE PIN DIFFERS").
3. Both lobes are unsealed, then both real arms run, then the male reading, then the outputs.
4. **A failure after unsealing** (check 11, check 6′, an exception) stops the arm. The seal is then
   broken without a verdict. The log and the private outputs are kept, the break is recorded in
   §11's ledger, and a second run from the same head is made only on Mike's word, with the first
   run's log committed beside its outputs. The verdict of a second run carries the note of S26.
5. The real arm writes its private outputs, including both lobes' block patterns and `x` values
   (per-cell male data), to `connectome-seed-data/knockout_regrow/malecns_<stamp>_<head>/`. The
   committed outputs hold aggregates: counts, the quadrant counts, and, for a split, the differing
   cells by name with their presence (§4.3), consistent with the builder's D11 (i).
6. The stdout log of the registered run is kept in the private folder (the blind review of the
   flyvis-65 run found none, its §E.4).

### 7.5 Run commands, outputs, cost

**Commands (to be pinned in the revision after the pre-run):**

```
tools/.venv/Scripts/python.exe results/genome/c6/checks/knockout_regrow_male_cns.py --synthetic-only --lobe L --starts 10 --workers 30 --out <new folder>
tools/.venv/Scripts/python.exe results/genome/c6/checks/knockout_regrow_male_cns.py --synthetic-only --lobe R --starts 10 --workers 30 --out <new folder>
tools/.venv/Scripts/python.exe results/genome/c6/checks/knockout_regrow_male_cns.py --arm malecns --starts 10 --workers 30
```

**Outputs:** committed aggregates in `results/genome/c6/checks/knockout_regrow_male_cns/`
(`RESULT.md`, `summary.json`, `per_shuffle_L.csv`, `per_shuffle_R.csv`, `synthetic_worlds_L.csv`,
`synthetic_worlds_R.csv`); private and raw outputs as §7.4; the two references in their own folders
(§3.3). Male CNS data is CC-BY (builder §1.1).

**Cost (A §7's rate):** pre-run about 4 h 20 min (both lobes); registered run about 4 h 20 min for
the two synthetic steps plus, per lobe, 6 × (3 + 99) + 20 = 632 real-arm fits, 5 fixed-λ fits and
the checks' 4 rule fits, and 20 C6 folds once for check 8: about 8 min. **Total about 8 h 50 min of
CPU wall time on 30 workers.** The rate on the placed grid is assumed, not measured (§10).

## 8. Lessons applied (delta on A §9)

| lesson | where here |
|---|---|
| a, selection after the data | the prior exposure is declared (§1.5); check 3 prints instead of comparing; every gate is A's |
| b, a null that cannot see the other world | worlds rebuilt on each lobe's outside (§3.6) |
| c, a criterion written after the finding | the male readings of §4.2, §4.3 and §5 are written after flyvis-65's G and before the male block is seen; each names its inputs |
| e, read the object | §1.3's table of every grid-dependent structure, with its line; §2's walk of the existence path |
| g, denominators | 2,961 training cells, 496 / 526 present, `n_present` / `n_absent`, 64 / 64 inferable, 3 mirrors, 36 / 2,961 lobe disagreement |

## 9. Decisions for review (reviewers, then Mike)

The body is written with the recommendation of each row.

| # | question | options (what each changes) | recommendation |
|---|---|---|---|
| **D1** | Which grid the arm trains and scores on (builder §5.2, §12) | **(i) the placed grid**: `H.ALL_CELLS` = 3,025 placed cells; 2,961 training cells per lobe, density 0.1675 / 0.1776, about flyvis-65's on the same cells (0.1726); A §8 already says "cells outside the builder's type set are left out of training and scoring"; the FlyWire precedent. (ii) the 65 grid: 4,161 training cells, of which **1,200 always absent** (the ten unplaced types): the rule sees ten types with no input or output, N1 spends 20 terms on them, every inner fold gains about 120 certain absences, and the training density falls to about 0.119 / 0.126, far from every calibration density; check 2's count of 4,161 would pass with another meaning | **(i)** |
| **D2** | How the two lobes are run | **(i) one invocation, both lobes; both synthetic gates pass before either sealed file is opened; one label per lobe** (§4.2): no lobe's verdict is seen before the other's run is fixed. (ii) two invocations, one per lobe: restartable, but the second lobe's run is made knowing the first's verdict. (iii) the right lobe primary and the left the null (builder D12 (ii)): halves the cost, but the left block, sealed like the right, would then be read as a null with no registered test of its own. (iv) a pooled statistic over both lobes (for example a mean AUC): a new statistic and new cuts, which need their own calibration | **(i)** |
| **D3** | The male reading from the two lobe labels | **(i) the table of §4.2**: a male R needs R in both lobes (builder D12 (i)); a common letter is the male letter; any other pair is a split with its class; one readable lobe is "one lobe only", never a male R. (ii) a male R if either lobe reads R: easier R, and a split would then be read as a positive | **(i)** |
| **D4** | The rule that separates the explanations of a split (builder D12, §12) | **(i) the classification of §4.3**: S0 same block; S1 differs within the lobes' outside rate; S2 differs beyond it (`k* = 4` from 36 / 2,961); R1–R6 excluded as a carrier by the build's facts; within-animal variation and reconstruction named as not separable. (ii) print the lobe difference, classify nothing: no registered reading of a split. (iii) read every split as within-animal variation: claims what one animal cannot show | **(i)** |
| **D5** | The existence bank (builder §7, §12) | **(i) run the registered predictors and harness unchanged on one `(0, 0)` offset per present cell; the offset, count and sign fields printed as meaningless; the existence path checked by T5 and by the pre-run** (§2). (ii) put a synthetic offset structure into the male bank: content that the animal does not have | **(i)** |
| **D6** | Synthetic worlds and limits (builder D13; Ark's ×1.22 point) | (a) **transfer A's limits and `smallest_passing_auc`** (γ\*_P 0.6, γ_R 0.75, family 0.75): no pre-run, 0 h; but they were measured on flyvis-65's degree terms, the 65 grid, density 0.137 and content with offsets, so a male G would carry limits of another instrument-bank pair. **(b) rebuild A's 45 worlds on each lobe** (degree terms, grid, content pool and density of the lobe; §3.6): about 2 h 10 min per lobe per pass, **4 h 20 min for the pre-run and 4 h 20 min again in the registered run**. (c) one world set on one lobe's outside, used for both lobes: half the cost; the lobes' outsides share 493 of 526 present cells, so the other lobe's limits would likely be close, but they would be assumed, not measured | **(b)** |
| **D7** | Seeds | (i) **A's seeds, as A §8 says** ("the same legs, cuts, seeds and branch rule apply"): the leg-P null would be flyvis-65's permutations, and the boards' `smallest_passing_auc` would reproduce A's registered values; but the worlds are different objects on another grid, so sharing A's world seeds buys no comparability and makes their CSV keys collide with A's reference. **(ii) a new range, 92000–92999, shared by both lobes** (§3.7): disjoint from A and B; common random numbers between the lobes. (iii) new seeds per lobe: a lobe difference could then come from a draw. (iv) A's leg-P seeds (90000, 90001) and new world and ceiling seeds: comparability of `p_P` with flyvis-65, at the cost of a mixed rule | **(ii)** |
| **D8** | Checks 3 and 5, the metric, and the unreadable block | **(i) check 3 prints the block after unsealing and stops only on no AUC; check 5 prints; precision at `n_present`, the other 61 cells; a block on which leg P cannot pass (`smallest_passing_auc` = None) reads the new U text "not readable"** (§3.2, §4.1). (ii) keep check 3 as a comparison with a count: there is no reviewed count, and writing one now would be selection with the knowledge of §1.5. (iii) no new U text: such a block could then read G, a vacuous G, since leg P could not have passed | **(i)** |
| **D9** | The row-and-column variant's attempt cap (builder §12) | **(i) a cap of 100 × 640 attempts per chain; a hit stops a synthetic step (a malfunction on a 32/32 board) and prints "n/a (attempt cap reached: …)" on a real block, which goes on**; the no-checkerboard pre-check prints "n/a". (ii) a hit stops everywhere, as B's D7: on the real block the stop would come after the seal is broken, forfeiting the run for a diagnostic that decides nothing; a sparse real block can hit the cap although swappable (§3.2). (iii) no cap: a real block with no reachable swap would never end | **(i)** |
| **D10** | The unseal protocol (builder §9) | **(i) §7.4: the sealed files are opened only by the registered real run, after every gate that does not need them; `--allow-dirty` refused with the male arm; a failure after unsealing is recorded, and a second run only on Mike's word.** (ii) A's rule, a dirty real-arm run allowed and marked "not the registered run": such a run opens the sealed files, which builder §9 allows only in the registered run | **(i)** |
| **D11** | Where the bank pins live (A §8; builder §10.5 step 4) | **(i) amend A, append-only, with the four bank pins, as both documents promise, and pin them in the arm's script too.** A's LF sha256 then changes from `409184de…`: the flyvis-65 run's manifest keeps the old value as the text it ran under; **block B's S2, which pins A "by its LF sha256 at `74db080`", must pin the amended hash or read A from git at `74db080`** (B is not yet implemented). (ii) pin only here and leave A unedited, recording here that A §8's promise is discharged here: A's text would keep a promise that A itself never shows fulfilled | **(i)**, with B's S2 note |
| **D12** | Verdict-line strings | **(i) A's rows quoted verbatim, then the four differences of §4.1** (lobe prefix; the "not readable" U; a line naming A's literals; "failed fit" read as fit failure or rank limit). (ii) restate §4 with the male's literals: a new text of a reading rule, reviewed as such | **(i)** |
| **D13** | Instrument | **(i) the pinned CPU harness, as A and B**: about 8 h 50 min of wall time in all. (ii) the GPU instrument of `cdbde9e`: separate and unreviewed, BF about 2.3 times faster, rule #2.1 not faster, base views not all bit-equal; by A §7 it needs its own registration and synthetic worlds | **(i)** |
| **D14** | Script form | **(i) a new file, a copy of A's, reviewed as a diff; A's untouched** (as B's D13 (i)). (ii) a `--arm malecns` inside A's file: the file that A's run and its blind review cite would change. (iii) import A's module and override its constants: `BLOCK`, `MASKS`, `MIRROR_IDX`, `NONBLOCK_CELLS`, `OTHERS` and the world arrays are computed at import (B's D13) | **(i)** |
| **D15** | Order of work | **(i) the header's order**: the script and this draft committed; the pre-run of both lobes from that committed head on Mike's word; a revision registering the values read from the pinned references, reviewed; A amended (D11); the registered run on Mike's word. Each reference has a producer in git. (ii) A's D11 order (pre-run before commit): repeats the provenance gap of A §3.3 | **(i)** |
| **D16** | The joint reading with flyvis-65's G | **(i) A's D13 table as voted, and the readings of §5** for male R (a flag with a registered list, examined under a new registration, overturning neither verdict), W, G, U and split. (ii) A's D13 table alone, with no reading written before data for the cases it leaves as "any other pair" | **(i)** |

## 10. Not verified at drafting

- **That rule #2.1's offset path, `eb_tables` and `data_bits` run on one distinct offset set** (§2).
  Read from the code, not run; T5 and the pre-run check it.
- **The fit rate on the placed grid** (§3.6, §7.5): assumed equal to A's measured 3.65 fits per
  second.
- **The male worlds' behaviour:** that R reads R, Nf reads G, No reads G and W reads W on the male
  degree terms and existence content, and where the limits fall. Expectations until the pre-run.
- **That the lobe-consistency check tested the side rule:** it could not fail on these types
  (§0); the photoreceptor side remains a transfer (builder §1.2).
- **The mechanism of the lobes' outside difference** in `x` (33 R-only against 3 L-only cells at
  the shared cut; `c*_L` < `c*_R`): not established.
- **The prior exposure's content** (§1.5): Zcode's preliminary graph and its definitions are in no
  file; the relayed description is quoted from the builder, not verified.
- **The binomial reference of §4.3** treats block cells as exchangeable with outside cells; they
  are not (strong pathway cells). It is registered as descriptive.
- **Typing by connectivity** in the male CNS (A §6): unchecked.
- **GLOSSARY:** no entry for "lobe", "sealed" or "split"; its rules of use ask for a term to be added
  before use. Not added here (this draft modifies no existing file).

## 11. Error ledger (working rules inherited from A §12)

**Working rules (A §12, revision 3.4, item 4).** A claim that an object is present or absent
requires a census of all the names the artefact declares for it. A claim about a column or a field
requires a census of that column. A partial or null result is a statement about the pattern and
the scope searched, not about the object. **A cited line carries its revision explicitly**: in this
file, `knockout_regrow.py` lines are of `74db080`, `harness.py` of `1789aeb` (the pinned file),
`flywire_bf_p3.py` of `c55d3e3`, rule #2.1's `fit.py` of `6ffce66`, `BUILD.md` and
`bank.meta.json` of `5860619`.

**Ledger** (six fields, A §12's form; the rows found while drafting):

| item | was | correct | where the wrong wording lived | what refuted it | caught by |
|---|---|---|---|---|---|
| M(1) | "male CNS v1.0: 64 / 64 at every pair threshold tried (Zcode, preliminary graph)" | at the registered cut, 64 / 64 in each lobe; among the builder's printed cuts, lobe L is 56 / 64 at the (b′) cut for `w_min` = 2 and 3. Zcode's own thresholds are in no file, so the claim cannot be checked against them; as written it reads as general | A §1.4 (the inferability table) at `74db080`; `knockout_regrow.py:205-208` (`INFERABILITY_PROVENANCE`) at `74db080`; printed in `knockout_regrow/RESULT.md` line 56; builder §0 ("64/64 at every threshold tried") | `BUILD.md` lines 189–190 (64 / 64 at `c*`), 210 and 227 (56 / 64, lobe L) at `5860619` | this draft |
| M(2) | `restrict_to_30_grid` at `flywire_bf_p3.py:74-76` (and ":74" in the drafting brief) | the function is lines 73–75 (definition 73, docstring 74, the assignment of `H.ALL_CELLS` 75) at `c55d3e3`, the file's last change, which precedes the commit (`d6e3759`) at which the builder read it | builder §2, §7, §12, §13.2 row 1 (`:74-76`) at `476cf9b` | `flywire_bf_p3.py` at `c55d3e3`, lines 73–75 | this draft |

**Registered expectations and what the build showed** (not wrong wordings; recorded so that no one
reads them as met):

| expectation (where registered) | what the build showed | source |
|---|---|---|
| "under the shared cut `c*` the left bank is expected to be sparser in R1's row and column" (builder §4, §12, revision 2.1) | not borne out: 3 / 1 in both lobes, the same cells | `BUILD.md` line 185; §1.4 |
| "`c*_L < c*_R` among the §5.4 diagnostics would read as a consequence of this asymmetry" (builder §4, §12) | `c*_L` = 2.69453 < `c*_R` = 3.39337 did occur, but R1's row and column are equal between the lobes, so the gap is not carried by R1–R6; it is lobe-wide (33 R-only against 3 L-only outside cells at `c*`) | `BUILD.md` lines 195, 198; §1.4 |
| "the first question put to the build: how much larger the R1-row asymmetry is than 1 : 2.04 in bodies" (builder §4) | answered: at `c*` there is no R1-row asymmetry in presence (1 : 1 against 1 : 2.04 in bodies) | `BUILD.md` line 185 |

**The seal record:** intact at revision 1 (header). A break before review is recorded here, and S26
carries it to the verdict lines.

## 12. Changelog

**Revision 1 (2026-09-26 UTC): first draft, CC subagent.** Built on A revision 3.4.1, the builder
revision 2.1 and its build (`5860619`), and B revision 1.1 as the template. Computed for this
draft, from the outside files only (after checking they hold no block row): the per-lobe endpoint
tables, inferability, mirrors, R1's and CT1(M10)'s rows, the lobe agreement (493 / 3 / 33 with the
36 cells and their `x` relative to `c*`), the fold composition on the placed grid; from arithmetic
only: the null standard deviations, the binomial tails and `k*` = 4. No sealed file opened; nothing
fitted. Proposals D1–D16 open.

## 13. Sources

- [`2026-09-24-knockout-regrow-registration.md`](2026-09-24-knockout-regrow-registration.md),
  revision 3.4.1: §0–§8, §10 (D13), §12.
- [`2026-09-25-male-cns-bank-builder-registration.md`](2026-09-25-male-cns-bank-builder-registration.md),
  revision 2.1: §0, §2, §4, §5, §7, §8, §9, §10.5, §12, §13.
- [`2026-09-25-knockout-regrow-block-b-registration.md`](2026-09-25-knockout-regrow-block-b-registration.md),
  revision 1.1: the form of a second-arm registration, §3.2 (the `rc_patterns` guards), §7 (the
  script-change table), D9, D10, D13.
- `results/genome/c6/checks/male_cns_bank/BUILD.md`, `bank.meta.json`, `SHA256SUMS.txt` (commit
  `5860619`); the build folder's `pair_stats_outside.csv`, `male_cns_L_outside.csv`,
  `male_cns_R_outside.csv`.
- `results/genome/c6/checks/knockout_regrow.py` (`74db080`), `results/genome/c6/harness.py`
  (`1789aeb`, pinned), `results/genome/c6/checks/flywire_bf_p3.py` (`c55d3e3`),
  `results/genome/c6/rules/second_rule_v21/fit.py` (`6ffce66`), `results/genome/c6/folds.csv`.
- `results/genome/c6/checks/knockout_regrow/RESULT.md` (the flyvis-65 verdict, `1ed55ec`);
  `docs/notes/2026-09-26-knockout-regrow-blind-review.md`.
- Commit `cdbde9e` (the GPU instrument's message only).
- `idea.md` (the project goal; context).
