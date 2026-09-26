---
**Status: DRAFT, revision 1.3, 2026-09-27 UTC. No sealed file opened.** Revision 1.2 was
reviewed in the DPC Research chat on 2026-09-26 UTC by Ark (18:10, "yes, with edits") and Zcode
(18:13, "yes", with edits) (§9.4). Revision 1.3 applies those edits (§9.5). **Three reading
rules are frozen before unsealing:** on the male banks a threshold U reads "not detected at the R
level", with no position on a threshold, because the transition band is empty (§4.1 (5), §6);
the instrument's weakness on the male banks is named with its numbers beside every male G (§5,
§6); "split" names two objects, a split by reading (§4.2) and a block difference (§4.3), and one
is never read as the other (§4.3). Also: the z / z′ order (§3.3.1 (c)); `n_deg` inert, with its
cause (§3.3.1 (d)); the `ko1` wording (§3.3.1 (a)); the link copy ← original (§3.3.1 (b), D17);
the pre-run and the registered run are made by different code, both recorded (S30), and the
`--from-raw` check after the merge is registered and was run (§3.3.1 (h)); a clarification of the
GPU census counts (§7.1, chat-only); the form of the amendment to A decided (Appendix A). Script
changes S29–S32 and test T14 (§7.2, §7.3). No gate, cut, seed, world or option of D1–D17
changes. Step 4 (A amended, its hash set in the script) and step 5 (the registered run, on Mike's
word) are next; before step 5, the check of §3.3.1 (h) is repeated at the merged head. Drafted by
a CC subagent; CC checks it.

**Status of revision 1.2, as written then: DRAFT, revision 1.2, 2026-09-27 UTC, for review (D15
step 3). Not voted on. No sealed file opened.** Revision 1.2 registers the values read from the two pinned pre-run references
(§3.3.1) and sets the script's placeholders for them (S17); it decides where the references live
(D17, new) and drafts the amendment to A (Appendix A; A itself is not edited). It changes no gate,
cut, reading rule, seed, world or option of D1–D16. **Where the order of work stands:** step 1,
revision 1.1 committed (`a6761e2`), Mike's word recorded in the GPU instrument's registration
(`docs/plans/2026-09-26-gpu-instrument-registration.md` lines 12–13 at `e50bf74`: "Mike gave his
word to run the GPU validation, §7, and the male arm", ~12:15 UTC); step 2, the script and tests
committed (`ee380a1`, `c8f0ea5`); step 3, the `--synthetic-only` pre-run of both lobes from the
committed head `a0e16b6`, tree clean, exit 0 (§3.3.1), and this revision; step 4 (A amended, the
amended hash set in the script) and step 5 (the registered run, on Mike's word) are next. **The
pre-run stops nothing:** every stop row and both two-world checks passed in both lobes. **It
surprised in four places** (§3.3.1 (d)): the leg-P limit γ\*_P is 0.75 in both lobes, not A's 0.6;
one M world at γ = 0.85 reads G in each lobe (A: none at or above γ_R); one M world reads W in
lobe L (A: none); the U worlds lie below or at the limits, not in a transition band (the band is
empty). Drafted by a CC subagent; CC checks it, the reviewers review it.

**Status of revision 1.1, as written then: DRAFT, revision 1.1, 2026-09-26 UTC. Revision 1.1 has
not been voted on and is not committed. No script written, nothing fitted, no sealed file
opened.** Revision 1 (commit
`f82d442`; `date -u` read 08:52 UTC when its drafting began) was reviewed in the DPC Research chat
by Johnny (09:14 UTC), Ark (09:18) and Zcode (09:32), all "yes, with edits" (§9.1). Revision 1.1
applies those edits (§9.2): three reading rules frozen before unsealing (the male R as a
conjunction, §4.2; the split class S2 conditional on `x`, §4.3; leg S decided by the count,
§3.2), and the edits to D7, D8, D11, D12, D13, §1.5, §3.3, §3.6, §3.7, §7.5 and the ledger. It
also specifies the content of the amendment to A (§9.3), which is made in a later step. Drafted
by a CC subagent; Mike's word is still needed. The design choices are marked **proposal** in the
body and listed in §9 (D1–D16), each with its options, what each option changes, and a
recommendation. The body is written with the recommended option (as relayed, no vote asked for
another option; D7 (ii), D11 (i) and D13 (i) were kept explicitly), so the draft is complete as it
stands.

**What this file is.** The registration of the **male CNS arm** of knock out and regrow: the
animal control that block A's registration names in its §8,
[`2026-09-24-knockout-regrow-registration.md`](2026-09-24-knockout-regrow-registration.md),
**revision 3.4.1** (commit `74db080`; LF sha256 `409184de…3facd6`, the value the flyvis-65 run's
manifest recorded; cited below as "A §n"; after the amendment of §9.3 this citation is updated to
the amended hash, and `409184de…` stays the text the flyvis-65 verdict was made under). It is a
**delta on A**: everything of A revision 3.4.1
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
and is reviewed; in the same step A is amended as §9.3 specifies (D11). (5) The registered
run, on Mike's word. It is the first and only code that opens the sealed files (§7.4).

**The seal, at drafting: intact.** No person or agent involved in this draft has opened, printed,
loaded, counted, summarised, plotted or diffed `male_cns_L_blockA.sealed.csv` or
`male_cns_R_blockA.sealed.csv`. Their sha256 values are quoted from `bank.meta.json` and
`SHA256SUMS.txt` only. The drafting agent listed the build folder's file names (no sizes) and did
not open either file. The prior exposure of block A of the male CNS through other channels is
declared in §1.5. **At revision 1.2: intact.** The pre-run read the outside files only (§3.3.1
(a)); the revision 1.2 agent did not open, hash, count, size or list either sealed file, and read
their names and hashes only from this file and the script. **At revision 1.3: intact.** The
revision 1.3 agent read the reference folders and the pre-run folders (synthetic worlds only)
and did not open, hash, count, size or list either sealed file.
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
    at the (b′) cut for `w_min` = 2 and 3 (`BUILD.md` lines 210, 227; §11, clarification C1).
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
pins, as A §8 and builder §10.5 step 4 promise, together with the cancellation of A's seeds for
this arm and the way to recover A's text as it stood at the flyvis-65 verdict (§9.3).

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
graph)") is, for this arm, "64 / 64 at `c*` in each lobe": a different object, not a correction of
A's row (clarification C1, §11).

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
   **One consequence is named, because it bears on readability (revision 1.1; Johnny, Zcode):**
   the relayed weak cells (means 1.0–2.2) lie below `c*`, so at `c*` the block may be sparse,
   with `n_present` well below 32. A sparse block raises the chance of the "not readable" U of
   §3.2 (`smallest_passing_auc` = None) and of degenerate shuffles in leg S (§3.2). This is a named
   risk, not an expectation that sets anything: no gate, cut or branch moves with it, and the
   relayed numbers are not verified (§10).
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

**Read declaration, revision 1.1 (a second CC subagent).** Read in addition: this file whole; A
§3.2, §4, §5, §8 and its end; `knockout_regrow.py` (`74db080`) lines 300–313, 770–790, 920–940,
1010–1080, 1240–1260, 1810–1876, 2075–2090, 2155–2165, 2280–2292, 2340–2400, 2420–2435; the
builder's §10.1, §10.5 and §13; the `n_deg` and `degenerate` columns of A's pinned pre-run
`synthetic_worlds.csv` (`connectome-seed-data/knockout_regrow/synthetic_rev3_prerun/`) and of the
flyvis-65 run's committed `synthetic_worlds.csv` and `per_shuffle.csv`; greps of the repository
(§3.7, §9.3, §11). **Not opened:** either sealed file (neither read, counted nor sized), anything
under `chat/`. The reviewers' messages are known from CC's brief only.

**Read declaration, revision 1.2 (a third CC subagent).** Read: this file whole; the arm's script
(its constants, `placeholders_unset`, `check_registered_constants`, `check_pins`,
`smallest_passing_auc` and its derivation, `reference_mode`, `check_prerun_files`,
`check_prerun_reproduced`, `ko1_count` and its control, `run_synthetic`, `out_dir_refusal`,
`quote_row`, `quote_section`, `open_sealed`, `run_synthetic_only`, `run_real_arm`, `main`) and its
tests; A §3.6 (the limits, lines 1195–1240), §7 (the reference, lines 1590–1665), §8 (lines
1735–1760) and its last lines; the GPU instrument's `instrument.py` lines 280–300 and
`validation.py` lines 680–760 (how V8 reads the male pre-run folders); from both pre-run folders,
`SHA256SUMS.txt`, `SYNTHETIC.md` (head), `synthetic_only.json` (every key, by script),
`synthetic_worlds.csv` (header and row count), `raw_fits.json.gz` (by the script's `read_raw`, for
counts only), and both stdout logs (whole); A's pinned `synthetic_rev3_prerun/SYNTHETIC.md` and
`synthetic_only.json` (for A's values, as history). **Not opened:** either sealed file (not read,
hashed, counted, sized or listed), anything under `chat/`, the main worktree (where V8 runs). The
GPU V8 lobe L result is known from CC's brief only (§7.1).

**Read declaration, revision 1.3 (a fourth CC subagent, in the worktree `cs-v8`).** Read: this
file whole; the arm's script and tests (whole where changed); A §8 (lines 1716–1760) and the
heading list of A; the GPU instrument's `census.py` whole and `validation.py` lines 660–830. From
both reference folders: `synthetic_worlds.csv` (every row, by script), `synthetic_only.json`
(the manifest, `fits`, `limits`, `u_rule`, the worlds' labels and U reasons), `raw_fits.json.gz`
(every record, by script: the shuffled blocks' present counts, the `ko1` provenance, the census
of §7.1); `sha256sum` of the five files of each reference and of each pre-run folder. From A's
pinned `synthetic_rev3_prerun/`: `synthetic_worlds.csv` (rule #2.1 rows: the power curve) and
`raw_fits.json.gz` (the `ko1` provenance and the census, by script). **Not opened:** either sealed
file (not read, hashed, counted, sized or listed), the Janelia build folder beyond the pinned
outside files that the script's check 1 hashes, anything under `chat/`, the main worktree. The
reviews of revision 1.2 are known from CC's brief only.

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
- **Leg S is decided by the count; `p_S` is informative (revision 1.1, frozen before unsealing;
  Ark, Zcode).** A's script decides leg S by `n_valid >= 1 and n_ge == 0`
  (`knockout_regrow.py:1067`) and computes `p_S = (1 + n_ge) / (1 + n_valid)` (`:1068`), which it
  prints with two decimals (`:.2f` at `:1252`, the verdict line; also `:2083`, `:2162`, `:2393`).
  With `n_deg` = 1 a passing leg S has `p_S` = 1 / 99 = 0.0101, which prints "0.01" and looks
  equal to `P_R` = 0.01, while the gate decided by the count; with `n_deg` = 2, 1 / 98 = 0.0102.
  The count and a "`p_S` <= 0.01" reading coincide only when `n_deg` = 0. That held in all 270 rows
  of A's pinned pre-run and of the flyvis-65 run's synthetic step (checked, column `n_deg`), by
  chance, not by construction; A's `N_DEG_SENTENCE` (`:310-311`) prints the smallest `p_S` with
  three decimals only when `n_deg` > 5. **For this arm: the count decides leg S** (A's rule,
  unchanged); `p_S` is printed as information and never compared with a cut; **when `n_deg` >= 1,
  `p_S` is printed with four decimals and a mark** naming the count as the deciding quantity (S28).
  A sparse male block makes `n_deg` >= 1 more likely (§1.5).
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
  **Linked to §1.5 (revision 1.1; Johnny, Zcode):** the relayed weak cells of the male block lie
  below `c*`, so the block at `c*` may be sparse (`n_present` well below 32), and the chance of this
  "not readable" U is higher than a 32/32 board would suggest. It is a named risk, not a
  prediction: nothing is set from it.
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
     stop there would forfeit the registered run for a diagnostic. **The asymmetry with check 3
     is deliberate (revision 1.1, Johnny; D8):** a block with no AUC is fatal for that lobe,
     because there is no verdict to print; an `rc_patterns` cap hit is a diagnostic, and the
     verdict stands.
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
  verified on the pinned files. **In the synthetic worlds**, both lobes use the same leg-P seed and
  the same boards (§3.6, §3.7), and `smallest_passing_auc` depends only on the block's labels and
  the permutations (`knockout_regrow.py:924-937`), so **the two lobes' values must be equal board
  by board**; the script asserts it. **This does not extend to the real blocks (revision 1.1,
  Ark):** each lobe's real block has its own labels, so its `smallest_passing_auc` is a new value,
  computed once, with no registered value to compare it with; the two lobes' real values are
  printed, not asserted equal.
- **Both lobes' gates pass before either sealed file is opened** (§4.2, §7.4). A failed stop row or
  a failed reproduction in either lobe stops the arm with both blocks sealed.

### 3.3.1 The pinned references and the values read from them (revision 1.2; D15 step 3)

Every value below was read from the two reference folders or their stdout logs by this revision's
agent, with the source named. "The pre-run folder" is
`connectome-seed-data/knockout_regrow/malecns_prerun_<lobe>_20260926T131249Z/`; "the reference" is
its byte copy `connectome-seed-data/knockout_regrow/synthetic_malecns_<lobe>_prerun/` (D17);
"the log" is `malecns_prerun_<lobe>_20260926T131249Z.stdout.log` beside the pre-run folder;
"the manifest" is the `manifest` key of the reference's `synthetic_only.json`.

**(a) The pre-run, as it ran.**

| | lobe L | lobe R | source |
|---|---|---|---|
| mode and arguments | `--synthetic-only`, lobes `["L"]`, starts 10, workers 30, 5 worlds per family, 99 shuffles, 20 permuted-block ceilings, all nine families, smoke false, `from_raw` null | the same, lobes `["R"]` | manifest keys `mode`, `lobes`, `starts`, `workers`, `worlds_per_family`, `shuffles`, `perm_ceilings`, `families`, `smoke`, `from_raw` |
| head | `a0e16b696389fb796a9f3b95c308358b52dd9dc8` | the same | manifest `git_head` |
| tree | clean: `tree_dirty_under_c6_or_plans` false, `tree_dirty_paths` [], `allow_dirty` false, `not_a_reference` null | the same | manifest |
| texts it ran under | this file, revision 1.1, LF sha256 `1560e40c85fac44dea278aa49fc36f92e10a1f4d003fb306aefc148eb4f2b693`; the script, LF sha256 `7a09f9fdfee38d93596fe0be9ffd4daab5b82cb287acdfa4a16bbdd4a3a281fc`; A recorded as `409184de…3facd6` | the same | manifest `registration_sha256_lf`, `script_sha256_lf`, `a_registration_sha256_lf`; both recomputed by this revision from `git show a0e16b6:<path>` (LF): equal |
| pre-run mode | `reference_mode` false: made the reference, checked none | the same | manifest; log line 9 ("PRE-RUN MODE (lobe L) …") |
| exit and runtime | exit 0; 8,001 s (2 h 13 min) | exit 0; 7,890 s (2 h 11 min 30 s) | the log's last line; CC's brief (exit codes); manifest `runtime_s` 7,996.3 / 7,886.0 (taken before the outputs were written) |
| world fits | 28,440 in 7,981 s (3.56 fits per second) | 28,440 in 7,873 s (3.61 fits per second) | the log, `[synthetic worlds] 5490 groups, 28440 fits` and `… done in 7981s` / `7873s` |
| fixed λ = 1 (`ko1`) | path check on `world:W:0`: 5 fits, identical for rule #2.1 and BF_1–BF_4; **main pass: 46 copied, 174 fitted** (220); with the 5 path-check fits the store holds **46 copied and 179 fitted** (225; row (c)) | the same path check; **main pass: 49 copied, 171 fitted** (220); in the store **49 copied, 176 fitted** (225) | the log ("fixed-lambda path check", "Fits: …"); `synthetic_only.json` `fits.fixed_lambda` (main pass) and `fits.ko1_count.counted` (store). **Revision 1.3 (Zcode):** the two pairs are one count at two scopes. The 5 path-check fits are the `ko1` records of `world:W:0`, refitted by the fixed-λ path and unflagged, so they count as fitted in the store and not in the main pass: verified on `raw_fits.json.gz`, 51 (L) and 54 (R) base `ko` fits of rule #2.1 and BF_r selected λ = 1, 5 of them `world:W:0`'s, and 46 / 49 `ko1` records carry `reused_from_ko`. **As in A:** 52 base fits at λ = 1, 5 of them `world:W:0`'s, 47 flagged; 173 + 5 = 178 fitted |
| records in the store | 28,665 = 45 × 637: `ko` 270, `full` 270, `block` 270, `ko1` 225, shuffles 26,730, permuted-block ceilings 900 | the same counts | `raw_fits.json.gz`, read with the script's `read_raw` |
| machine | AMD64 Family 26 Model 68, 32 logical CPUs, Windows 10.0.26200; Python 3.10.20, numpy 2.2.6 (scipy-openblas 0.3.29); the four BLAS thread variables 1 (none set before launch) | the same | manifest `machine_record`; the log's "machine record" line |
| mean seconds per knockout fit | rule #2.1 13.5, BF_1 4.5, BF_2 8.6, BF_3 10.5, BF_4 12.5, N1 0.03 | 13.3, 4.5, 8.5, 10.3, 12.3, 0.03 | `synthetic_only.json` `mean_seconds_per_knockout_fit` |
| the log | 1,721 lines, sha256 `b5e2343d3223680d4ce2c8f46bf7c74d4f94b3b0aaabdb51427efeed8f5c7f3c` | 1,717 lines, sha256 `ef42ba024bef630dce8049c98ca70dc439ede2bf716da470bfe3b0e95b2670b5` | computed by this revision; provenance, not pinned by the script |

**No sealed file was touched.** Both logs end with the script's line, quoted: "--synthetic-only
(lobe L): stopped before any real block; no sealed file was touched. 8001s" (log L, line 1,721)
and "--synthetic-only (lobe R): stopped before any real block; no sealed file was touched. 7890s"
(log R, line 1,717); the manifest records `sealed_files_touched` false and `seal_record`
"intact". **That line is printed unconditionally at the end of every `--synthetic-only` run, so
it is not evidence by itself.** The evidence is the code path: the only reader of a sealed file,
`open_sealed`, raises unless `_UNSEAL["allowed"]` is set, which only `_run_real_arm` sets (script
line 3687 at revision 1.2), after both lobes' synthetic steps; `verify_sealed_pins`, the only
hasher, is called only there; neither log contains the word "UNSEALING"; and test T3 records zero
calls of either in `--synthetic-only`.

**(b) Where the references live (D17), and their verification.** The pre-run wrote to the
pre-run folders (its `--out`; manifest `private_outputs`). Its five files were copied byte for
byte to the folders §3.3 proposed, `synthetic_malecns_L_prerun/` and `synthetic_malecns_R_prerun/`,
which are the script's `PRERUN_DIR` (unchanged since revision 1.1) and which each reference's own
manifest names as `prerun_dir`. Checked on 2026-09-27 UTC: `sha256sum -c SHA256SUMS.txt` in each
original and each copy, all four listed files OK; `cmp` of all five files between original and
copy, equal; `SHA256SUMS.txt` itself: L `d28ead5e5b65d106b0a14901f1053cdcabfa07efce2b1e7034bf63ae2deec64f`,
R `5495bedf642d33a41ba71001f5492aa9f2c24c294f0b723f0f172dc89ed24521`, equal in original and copy.
The pre-run folders were not modified; the copies hold exactly the five files (no stdout log, no
other entry), so `check_prerun_files` reports nothing unlisted.

**The link copy ← original (revision 1.3, D17; Ark, Zcode).** `synthetic_malecns_<lobe>_prerun/`
is a byte copy of `malecns_prerun_<lobe>_20260926T131249Z/`: **all five sha256 equal** in each
lobe. Recomputed on 2026-09-27 UTC by this revision, in `connectome-seed-data/knockout_regrow/`:

```
for l in L R; do for f in SHA256SUMS.txt SYNTHETIC.md raw_fits.json.gz synthetic_only.json synthetic_worlds.csv; do
  sha256sum malecns_prerun_${l}_20260926T131249Z/$f synthetic_malecns_${l}_prerun/$f; done
  (cd synthetic_malecns_${l}_prerun && sha256sum -c SHA256SUMS.txt); done
```

Every pair equal (the four listed values are row (c)'s pins; `SHA256SUMS.txt` itself L
`d28ead5e…deec64f`, R `5495bedf…ed24521`), and `sha256sum -c` OK on all four listed files in
each copy. The link is recorded here only: the copies hold no note of it, since a file added to a
pinned folder would be an unlisted entry of `check_prerun_files` (reported, not failed) and would
break T13's "nothing unlisted"; the originals are not written either.

**(c) The registered values (the script's S17 constants, and what the registered run reads from
the references).**

| value | lobe L | lobe R | source |
|---|---|---|---|
| `PRERUN_DIR` | `connectome-seed-data/knockout_regrow/synthetic_malecns_L_prerun` | `…/synthetic_malecns_R_prerun` | D17; script constant, unchanged |
| `PRERUN_SHA256["SYNTHETIC.md"]` | `97797a5120eab60bdf7c5ea94aaeb5835430f54a3af9c2e27c12b0d81741363f` | `6f4b94b1c9096b45a8532395a2e45f47b5484663431d66532548d68db4753e84` | the folder's `SHA256SUMS.txt`, recomputed (raw bytes) |
| `PRERUN_SHA256["raw_fits.json.gz"]` | `e0e1114d9c7fc6bcb316a131aaea572b426ef46e6f1c4f8786fdb63d2783dad2` | `183b9376315dd98bb421015fb721d941cddf2dd1949f96be82055d1f4c5acade` | the same |
| `PRERUN_SHA256["synthetic_only.json"]` | `9498de82d33444ff98e090b2cff895d2ab760f433fbf41d22e12e9b67b61f649` | `8acf217d77fbe21d29561f47cc33373769e74f3cc50150def97eca4f6b49f219` | the same |
| `PRERUN_SHA256["synthetic_worlds.csv"]` = `PRERUN_WORLDS_CSV_SHA256` | `506576312638005e5bd09876c9da0ffe9a8a753641a59a2b354c0c59bed25d91` | `e8476a936356d3965aa5715d7f04a82c3587ff0795569db81071822fbca9cae0` | the same; also the log's "pre-run table (section 7): … recomputed sha256" line |
| `smallest_passing_auc`, board `z` (40 worlds: every family but No) | **0.671875** (688 / 1024) | **0.671875** | `synthetic_only.json` `worlds[*].smallest_passing_auc` by `board` (`derive_smallest_passing_auc`); the log's "smallest_passing_auc registered values" line |
| `smallest_passing_auc`, board `z'` (5 worlds: No) | **0.669921875** (686 / 1024) | **0.669921875** | the same |
| `ko1` count (registered control) | 225 records: 46 copied from `ko`, 179 fitted (5 of them by the path check on `world:W:0`; main pass 174, row (a)) | 225: 49 copied, 176 fitted (5 by the path check; main pass 171) | `registered_ko1_count` on `raw_fits.json.gz`; `synthetic_only.json` `fits.ko1_count.counted`; the log's "ko1 records" line |
| code that made the reference (S30, revision 1.3) | head `a0e16b6` (`a0e16b696389fb796a9f3b95c308358b52dd9dc8`), script LF sha256 `7a09f9fdfee38d93596fe0be9ffd4daab5b82cb287acdfa4a16bbdd4a3a281fc` | the same | the manifest's `git_head` and `script_sha256_lf`; the script's `PRERUN_GIT_HEAD` and `PRERUN_SCRIPT_SHA256_LF` |

**L = R board by board, as §3.3 asserts for the worlds:** both lobes give 0.671875 for `z` and
0.669921875 for `z'`, and so does `board_smallest_passing_auc()`, which computes them from the
boards' labels and `uniform_perms()` alone. The registered run asserts the equality before
unsealing. They differ from A's registered values (0.666015625 for `z`, 0.6728515625 for `z'`,
A §3.2) because the leg-P seed differs (92000 against 90000; D7 (ii)): expected, not a surprise.
**The order is reversed (revision 1.3; Ark, Zcode):** on A, z < z′ (0.666015625 < 0.6728515625);
on the male banks, z > z′ (0.671875 > 0.669921875). A value is compared with its own board's
value in its own arm, never across arms by board name.
**The null-input digests** (equal in both lobes; the log's "null-input digests" line; manifest
`null_input_digests`): `uniform_perms` sha256 `d1377913384e3409576620a8ae9e531e8a630c751a6b0942378f2e986db0ee3d`
(int64, 9,999 × 64, seed 92000, computed in the main process); `rc_patterns` (seed 92001), one per
block label vector: labels `50af3eb1…f3f1d` → `df9482806b01c353f35448557221e060f53e94637fe68971e667a6ca57da5f21`,
labels `fc09a87e…fcd92a9` → `8e03d585828147801125c4eb43a4739ee5d294d75c267ca325d28158632c0dcf` (bool,
9,999 × 64). **The degree terms** (N1 on the lobe's knockout view, 2,961 placed outside cells; the
log's line 8; full arrays in manifest `degree_terms`): lobe L `c` = −1.8711, `a` in [−1.775,
+1.544], `b` in [−1.422, +2.064]; lobe R `c` = −1.7909, `a` in [−1.816, +1.545], `b` in [−1.479,
+1.915].

**(d) Pre-run values: the limits, the gates, the power curve.** These are values of the synthetic
step. The registered run refits both lobes and recomputes them; its reproduction gate compares its
worlds table with the reference's on the deciding columns (outcome 1 or 2 passes, 3 stops), so a
reproduced run prints these same values. Sources: each log's "Two-world check", "Power curve and
the three limits" and "U rule" sections, and `synthetic_only.json` keys `two_world_check`,
`limits`, `u_rule`.

| quantity | lobe L | lobe R | A's pre-run (history; A §3.6, lines 1195–1240 at `74db080`) |
|---|---|---|---|
| stop row R (each of 5 reads R, both D1 candidates) | 5/5 R, no stop | 5/5 R, no stop | 5/5 R |
| stop row Nf (never R or W; ≥ 3 of 5 G) | 5/5 G, no stop | 5/5 G, no stop | 5/5 G |
| stop row No (never R or W; reads G; a U triggers the contingency) | 5/5 G, no stop; contingency not triggered | 5/5 G; not triggered | 5/5 G |
| stop row W (each of 5 reads W, both D1 candidates) | 5/5 W, no stop | 5/5 W, no stop | 5/5 W |
| two-world check | passed | passed | passed |
| `smallest_passing_auc` check before the fits | 45 of 45 worlds equal | 45 of 45 | 45 of 45 (A's values) |
| **γ\*_P** (leg-P limit, rule #2.1 `p_P` <= 0.01 in a majority) | **0.75**, bracket (0.6, 0.75] | **0.75**, bracket (0.6, 0.75] | **0.6**, bracket (0.5, 0.6] |
| **γ_R** (a majority reads R) | **0.75**, bracket (0.6, 0.75] | **0.75**, bracket (0.6, 0.75] | 0.75, bracket (0.6, 0.75] |
| **family limit** (largest per-predictor leg-P limit) | **0.75**, set by all five (rule #2.1, BF_1–BF_4 each 0.75) | **0.75**, the same | 0.75 (rule #2.1 and BF_1 0.6; BF_2–BF_4 0.75) |
| transition band [γ\*_P, γ_R) | empty (0 grid steps) | empty | [0.6, 0.75), one step |
| majority seen / R at every grid γ above the limit | true / true | true / true | true / true |
| grid complete | true | true | true |
| rule #2.1 seen / R per γ (revision 1.3: in each pair, the first number is the worlds at that γ whose rule #2.1 `p_P` <= 0.01, "seen"; the second, the worlds whose label is R; of 5; verified on each `synthetic_worlds.csv`, rule #2.1 rows): 0.5 | 0/5, 0/5 | 1/5, 1/5 | 1/5, 1/5 |
| 0.6 | 2/5, 1/5 | 2/5, 2/5 | 3/5, 2/5 |
| 0.75 | 5/5, 4/5 | 5/5, 3/5 | 5/5, 5/5 |
| 0.85 | 4/5, 3/5 | 4/5, 4/5 | 5/5, 5/5 |
| 1.0 | 5/5, 5/5 | 5/5, 5/5 | 5/5, 5/5 |
| labels R/W/G/U: M0.5, M0.6, M0.75, M0.85, M1.0 | 0/0/2/3, 1/0/1/3, 4/0/0/1, 3/1/1/0, 5/0/0/0 | 1/0/2/2, 2/0/2/1, 3/0/0/2, 4/0/1/0, 5/0/0/0 | 1/0/4/0, 2/0/0/3, 5/0/0/0, 5/0/0/0, 5/0/0/0 |
| U worlds (all threshold U; none failed fit, not measured or not readable) | 7 of 45: 3 at 0.5, 3 at 0.6, 1 at 0.75; 6 below the (empty) band, 1 above | 5 of 45: 2 at 0.5, 1 at 0.6, 2 at 0.75; 3 below, 2 above | 3 of 45, all at 0.6, all inside the band |
| U rule | U stays (7 of 25 dense-grid worlds) | U stays (5 of 25) | U stays (3 of 25) |
| M worlds reading G at or above γ\*_P / γ_R | 1 / 1 (M0.85, seed 92184) | 1 / 1 (M0.85, seed 92184) | none |
| `n_deg` | 0 in all 270 rows | 0 in all 270 rows | 0 in all 270 rows |
| **why `n_deg` is 0 (revision 1.3, Ark)** | **inert because no shuffle gives present ∈ {0, 64}**: the 26,730 shuffled-bank records hold 9 to 37 present block cells (the 17,820 BF `ko` shuffle fits the same) | 12 to 36 | not recounted |
| `ceiling_block` of rule #2.1 and BF_1–BF_4 | 1.0 in all 225 rows | 1.0 in all 225 rows | 1.0 in all 225 rows |
| `rc_patterns` (the attempt cap, D9) | complete in all 45 worlds; at most 4,614 attempts per chain against the cap of 64,000 | the same | no cap in A |
| Nf worlds' outside density (the lobe's: 0.1675 / 0.1776) | 0.1724 (0.1662–0.1749) | 0.1812 (0.1746–0.1841) | 0.1365 (A's bank 0.1375) |

**The joint R on the worlds (a count made by this revision from the two tables; it decides
nothing and enters no gate).** The lobes share their world seeds (§3.7), so each M world has a
pair of labels. Both lobes read R in 0 of 5 pairs at γ = 0.5, 1 of 5 at 0.6, 3 of 5 at 0.75, 3 of
5 at 0.85 and 5 of 5 at 1.0. The pairs whose labels differ: 5 of the 20 at γ 0.5–0.85 (seeds
92142 U/R, 92161 U/G, 92164 U/R, 92172 R/U, 92183 W/R; lobe L first); none among the 25 others.
This is the first measurement of what §4.2 said was not measured: on 32/32 boards near the limit,
one pair in four splits, and the male R's majority is reached at γ = 0.75 with 3 of 5, against 4
and 3 of 5 per lobe. **Revision 1.3 (verified on the two CSVs and the stores):** the five pairs
are seeds 92142 (M0.5, U/R), 92161 (M0.6, U/G), 92164 (M0.6, U/R), 92172 (M0.75, R/U) and 92183
(M0.85, W/R), 5 of the 25 dense-grid pairs; none of the 20 pairs of the axis families (R, Nf,
No, W). **Every one of the 45 world pairs has the same block in both lobes** (the same board by
seed; the base `ko` records' labels are equal in all 45), so all five splits are **splits by
reading at k = 0**: the lobes' labels differ while their blocks are identical (§4.3, "two
objects").

**Surprises, stated plainly (compared with §3.6, §10 and A's pre-run as history):**

1. **γ\*_P = 0.75 in both lobes, not 0.6.** §3.6 said "on a denser bank the M worlds may be seen
   at lower γ"; the opposite happened: at γ = 0.6 rule #2.1 is seen in 2 of 5 worlds in each lobe
   (A: 3 of 5), so the leg-P limit moves up one grid step and meets γ_R. By the binomial note (a
   limit is uncertain by about one grid step with 5 worlds) this is within noise for each lobe,
   and the two lobes are not two independent observations (common seeds). The family limit stays
   0.75, but it is now set by rule #2.1 and BF_1 too (A: BF_2–BF_4 only).
2. **The transition band is empty, and the U worlds lie below it or at it** (L: 6 below, 1 at
   0.75; R: 3 below, 2 at 0.75). A's reading of U (A §4, revisions 3.1 and 3.2: "the signature of
   the leg-P detection limit γ\*_P", "all 3 pre-run U worlds sit at γ = 0.6 = γ\*_P") rests on A's
   pre-run; on the male instrument U worlds sit at γ = 0.5–0.75, up to two grid steps below
   γ\*_P. The quoted row keeps A's literals; the line after it names them and gives the lobe's
   own values (§4.1, difference 3). No reading rule changes (frozen); the reviewers may want the
   U row's printed band to be read with this in mind. **Revision 1.3 (Ark, Zcode): a reading rule
   is frozen from this, before unsealing** (§4.1 (5), §6; S29): on the male arm a threshold U
   reads "not detected at the R level", with no position on a threshold. The U reasons, read from
   each `synthetic_only.json`: in all 12 U worlds rule #2.1 passes leg S (`n_ge` = 0 of 99); in 5
   the legs disagree (leg P `p_P` 0.0117–0.0332) and in 7 the two D1 candidates disagree, one of
   them reading R (L 92142, 92144, 92163: BF_1 R; L 92164, 92173, R 92172, 92173: rule #2.1 R).
3. **One M world above both limits reads G in each lobe:** M0.85, seed 92184 (rule #2.1 AUC
   0.5254, `p_P` 0.3695, `n_ge` 10 in lobe L; AUC 0.5420, `p_P` 0.2872, `n_ge` 1 in lobe R;
   `ceiling_block` 1.0, so the G gate passes). A's pre-run had no G at or above γ_R. The G label
   reads "not detected at the R level above γ_R"; on the male instrument 1 of the 10 worlds at γ
   0.85 and 1.0 was missed in each lobe (the same seed: one draw of `z` seen through two lobes).
   Printed by the script (`G_at_or_above_leg_P`, `G_at_or_above_R`); no stop row reads it.
4. **One M world reads W in lobe L:** M0.85, seed 92183: rule #2.1 AUC 0.7017, `p_P` 0.0028, but
   leg S fails by one shuffle (`n_ge` = 1 of 99); BF_2–BF_4 pass both legs (`n_ge` 0, `p_P` 0.0030,
   0.0007, 0.0024), so both D1 candidates read W. In an M world the block is realisable by rule
   #2.1 (§2), so this W misreads the world. A's pre-run had no W in its M families. Lobe R reads
   the same seed R.
5. **Power per γ is lower than A's above the limit:** R in 4/5 and 3/5 worlds at γ = 0.75 (A 5/5),
   3/5 and 4/5 at 0.85 (A 5/5). The stop families (R, Nf, No, W) read exactly as in A.
6. **Not surprises:** the stop rows, both two-world checks and every requirement passed in both
   lobes; `smallest_passing_auc` equal in both lobes; `n_deg` = 0 and `ceiling_block` = 1.0
   everywhere, as in A; the Nf worlds' density near the lobe's, as §3.6 expected; the `ko1`
   count inside §3.6's upper bound of 225 (A: 47 / 178); the fit rate (3.56 and 3.61 fits per
   second on the world fits, against the assumed 3.65; §10) and the runtime (§3.6 predicted about
   2 h 11 min per lobe; measured 2 h 13 min and 2 h 11 min). The existence path of every
   predictor (§2, §10 first item) ran 28,665 fits per lobe without error.

**(e) Does the pre-run stop the registered run? No.** No stop row failed, both two-world checks
passed, the No contingency was not triggered, and the lobes' `smallest_passing_auc` are equal by
board. The registered run stops before unsealing only if its own synthetic step fails: a refit
that does not reproduce the reference (outcome 3), a different `ko1` count, a failed stop row, a
`smallest_passing_auc` mismatch, or a pin that differs. Until A is amended it refuses at once
(below).

**(f) The reproduction check from the reference's own store** (2026-09-27 UTC, this revision's
agent; A's `--from-raw` analogue; `--synthetic-only --lobe L|R --starts 10 --workers 5
--allow-dirty --from-raw <the reference>/raw_fits.json.gz`, no `--out`, run with the script of
this revision, LF sha256 `42b83ddc3ab80df13572fdbf5bb9a3fd0d4859358f5415bc1ac8fc0e9373468b`, from
the uncommitted tree that became this revision's commit; `--allow-dirty` marks such a run NOT A
REFERENCE, and it writes nothing). Both lobes, about 9 s each, exit 0:

- reference mode (the pins of (c)); `check_prerun_files` passed (every listed file equal to its
  listed and pinned sha256); `smallest_passing_auc` derived from the pinned `synthetic_only.json`,
  one value per board ({z: 40, z': 5} worlds), and 45 of 45 worlds equal to it with `Yu` generated
  fresh, the only check of this pass that could stop it;
- **the worlds table re-derived from the store is byte-identical to the pinned one** (outcome 1,
  every deciding column equal; recomputed sha256 = the pin in each lobe; 0 rows missing either
  way; `mechanism_description` equal on every row);
- the fixed-λ path check refitted 5 fits per lobe fresh on `world:W:0`: identical to the stored
  ones for rule #2.1 and BF_1–BF_4;
- the per-fit diagnostic: 28,665 keys compared, `p`, λ, labels, scores and `reused_from_ko` equal
  on all (it compares the store with itself, so it carries no information beyond the 5 fresh
  fits); the `ko1` count read from the store equals the registered one; the limits, the U rule and
  the degree-term line printed as in the pre-run; the null-input digests equal the pre-run's.

This shows that the reference is self-consistent and that the script of this revision reads it as
registered. It is not a reproduction by refitting; that is the registered run's gate.

**(g) What the script does at revision 1.2.** `PRERUN_SHA256` and `PRERUN_WORLDS_CSV_SHA256` are
set for both lobes, so `reference_mode` is true for both: a `--synthetic-only` run verifies the
reference's files before any fit, reads the registered values from it, stops a fresh comparable
run whose `ko1` count or worlds table (outcome 3) differs, and compares its fits key by key.
**`A_REGISTRATION_SHA256_LF_AMENDED` stays `None` until A's amendment is committed** (D15 step 4).
While it is `None`, `--arm malecns` refuses at its first step, before any file is read:
`check_registered_constants` exits "REFUSED: --arm malecns needs the values that the revision
after the pre-run registers (D15 (i), sections 3.3, 9.3); still placeholders:
A_REGISTRATION_SHA256_LF_AMENDED (A's LF sha256 after the amendment of section 9.3)". Once set,
`check_pins(real_arm=True)` also refuses unless A's current LF sha256 equals it. Every other mode
records A's hash and goes on. Test T13 (§7.3) checks all of this on the real references. **A
consequence outside this arm:** the GPU instrument's V8 refuses a male store made by another
version of this script (`validation.py` `check_male_store`: "the store was made by the male
script …, this head's is …"); the pre-run stores were made by `7a09f9fd…`, and this revision's
script is `42b83ddc…`, so V8 cannot be rerun at a head that contains this revision without a
change on its side. V8 decides nothing for this arm (D13 (iii)). **Revision 1.3 (S30):** a
`--synthetic-only` run in reference mode and the registered run read each reference's manifest
(after `check_prerun_files`) and stop with "PRE-RUN PROVENANCE DIFFERS" unless it names head
`a0e16b6` and script `7a09f9fd…` (`PRERUN_GIT_HEAD`, `PRERUN_SCRIPT_SHA256_LF`); both print, and
the registered run records in its manifest (`prerun_provenance`) and in `RESULT.md`, "lobe ℓ:
pre-run made by head a0e16b6, script 7a09f9fd (LF sha256 …); this run by head <head>, script
<sha> (LF sha256 …)", with "different code" when the two scripts differ.

**(h) The `--from-raw` check after the merge (revision 1.3, registered; Zcode's proposal, Ark).**
The pre-run was made by the script at `a0e16b6` (LF `7a09f9fd…`); the registered run will be made
by the script after this branch is merged (another hash; S30). **Registered:** after the merge
and before the registered run, a `--synthetic-only --lobe L|R --starts 10 --workers 5
--from-raw <reference>/raw_fits.json.gz` pass (no `--out`; it writes nothing) is run with the
merged script against each pinned store, from the merged head with the tree clean. **It must
re-derive each lobe's worlds table byte for byte** (outcome 1, byte-identical, recomputed sha256
equal to `PRERUN_WORLDS_CSV_SHA256`), with the `smallest_passing_auc` check 45 of 45, the `ko1`
count equal to the registered one and the fixed-λ path check identical. **If it does in both
lobes, re-running the pre-run is not needed**: the new code reads the old references as
registered, and the registered run's own refit is still gated by the reproduction gate (outcome
1 or 2). **If it does not in either lobe, the registered run does not start**; the difference is
reported, and what follows is decided in a new revision. Its log is kept beside the registered
run's (§7.4 (6)).

**Run by this revision (2026-09-27 UTC), with this revision's final script** (LF sha256
`1b952ca6aca7c5026061a5db21e27aef2176ecd255e8c19f4b658437495af7a9`), from the uncommitted tree
at `af11d31` that became this revision's commit (`--allow-dirty`, so marked NOT A REFERENCE; it
writes nothing): **both lobes re-derive their worlds table byte for byte** (outcome 1,
byte-identical; recomputed sha256 L `50657631…c59bed25d91`, R `e8476a93…c9cae0` = the pins; 0 rows
missing either way; `mechanism_description` equal on every row); `smallest_passing_auc` 45 of
45; `ko1` 225 (46 / 179 L, 49 / 176 R), equal to the registered count; the fixed-λ path check
identical for all five predictors on `world:W:0`; the per-fit diagnostic 28,665 compared, 0
differing (the store against itself, plus 5 fresh fits); S30's line printed "different code"
(`7a09f9fd` against `1b952ca6`); exit 0 in 8 s (L) and 9 s (R). The check is repeated at the
merged head (the merge changes no byte of the script, but the head changes).

### 3.4 Machine checks (delta on A §3.4)

Per lobe unless marked. Checks 1, 2, 4, 7 and 10 run in every mode; checks 6 and 9 run in the real
arm before the seal is broken; check 3, check 5, check 6′ and check 11 run after it.

| check | male CNS arm |
|---|---|
| 1 pins | A's eight pins; the six male files of §1.1 (the sealed files by hash only, and only in the real arm before opening; §7.4); Python 3.10.20 and numpy 2.2.6; rule #2.1 with `RANK == 1` |
| 2 block and mask | 64 cells, 8 sources, 8 targets, all 16 names in the placed set; on the placed grid the knockout view has 2,961 cells, none in the block; the full view 3,025; the block view 64 |
| 3 board | **no reviewed count exists** (A §8: "set by the builder's registered threshold"; §1.5). Replaced by a print, after unsealing: the block's present count, the four quadrant counts, the row and column counts, whether `y_st = x_s · w_t` (flyvis's board), and whether the block is balanced (4 of 8 in every row and column). It stops that lobe only if the block has no AUC (0 or 64 present: "BLOCK HAS NO AUC"): fatal, since there is no verdict to print, unlike an `rc_patterns` cap hit, a diagnostic after which the verdict stands (D8) |
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
grid, where every array is still 65 × 65):** one lobe's synthetic step is 45 × (3 × 6 + 20 + 99 × 6
+ 5) = 28,665 fits, about **2 h 11 min**; both lobes about **4 h 22 min**. The pre-run and the
registered run's refit together: about **8 h 44 min** of CPU wall time, plus the real blocks
(§7.5). **The + 5 (revision 1.1, Zcode):** the `ko1` fits, the knockout at fixed λ = 1 of rule
#2.1 and BF_1–BF_4 on every world (the diagnostic of A §3.5; `complete_fixed_lambda`,
`knockout_regrow.py:1833-1853`): 225 per lobe, about + 0.8 %. Revision 1 left them out; A's
script counts 637 keys per world (`:1462`). The 225 is an upper bound: a `ko1` record whose ko fit
already selected λ = 1 is copied, not fitted (A's pinned store: 225 records, 47 copied, 178
fitted, `:1870-1871`).

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
reason), and the amendment to A cancels that sentence as it concerns seeds, with the address of
this section (§9.3). **What is given up (revision 1.1, Johnny):** the male leg-P null is not
flyvis-65's 9,999 permutations, so a male `p_P` is not directly comparable with flyvis-65's `p_P`
draw for draw; the two are compared only as two tests of the same rule, each against its own
null. **Untouched:** A §3.7's list (60000, 61000, 70000–70999, 80000–80999, 4242, 99, 7,
1000–1019, the dial seeds, 20260923), A's own seeds (90000, 90001, 90010–90029, 90100–90154,
90160–90184) and B's (91000, 91001, 91010–91029, 91100–91184). **Checked 2026-09-26 UTC:** a grep
of the repository's `.py`, `.md` and `.json` files for 92000–92999 found no seed. **Revision 1.1
(Zcode): revision 1 named two hits, but the list was not exhaustive.** Recounted over the tracked
files at revision 1's tree (`f82d442`, before this revision's edits; `git grep -E '92[0-9]{3}'`): **96,233 occurrences of a digit string 92000–92999 on 92,083
lines in 904 files** (4 `.py`, 21 `.md`, 879 `.json`), almost all inside longer numbers:
floating-point values, sha256 strings and counts. Bounded as a whole decimal number (no digit, hex
letter or decimal point on either side), the only hits outside this file are the two neuron-pair
row counts in `BUILD.md` (92745 and 92100, lines 159 and 168) and their copies in
`bank.meta.json` (lines 3479, 3587). None of the four `.py` files' hits is a seed (two sha256
strings in `knockout_regrow.py:130`, `:155`; floating-point values in two `post_run.py` and
`night3/diagnostics/rowB/rowB3.py`). **The conclusion "no seed in the range" stands**; the census
is by pattern, and a seed written as an expression (for example `92_000` or `90000 + 2000`) would
not be found by it. The script asserts that the new seeds are distinct, lie in 92000–92999, and
meet none of the untouched, reused, block-A or block-B seeds.

### 3.8 Vocabulary (additions)

- **Lobe** L or R: the builder's lobe (side, with the CT1 flip; builder §4). **A lobe's bank** =
  its outside bank plus, in the real run only, its present block cells.
- **Sealed**, **unsealing:** the builder §9 rule; unsealing is the first opening of a sealed file,
  in the registered real run (§7.4).
- **Split:** the two lobes read different letters (§4.2). **Revision 1.3:** this is the **split
  by reading**. The **block difference** is another object: `k`, the number of the 64 cells whose
  presence differs between the lobes' blocks, with the class S0/S1/S2a/S2b of §4.3. The two are
  printed apart (S32), and one is never read as the other (§4.3, "Two objects").
- **Present in the block:** A §3.8's two carriers, with 32 in every synthetic world and the real
  count unknown before the run.

## 4. Reading rule

### 4.1 Per lobe: A §4, verbatim, with five stated differences

A §4 applies **verbatim** to each lobe: the four branches in order, R and W on both D1 candidates,
the cuts (`P_R` = 0.01, `P_W` = 0.0125, `P_G` = 0.10, `GATE_CUT` = 0.90, `MECHANISM_CUT` = 0.90),
the U rule's naming (per lobe, on that lobe's dense grid), the verdict line's contents, λ on the
verdict line, the No contingency (per lobe). No condition, cut or existing label string changes.
Five differences (D12; the fifth added by revision 1.3, frozen before unsealing):

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
   The rows are quoted from the amended A, never from this file, which holds none of them
   (script change S2, D12).
4. **"Failed fit" on a male block** keeps its text ("failed fit: rule #2.1 cannot hold the block
   even when trained on it alone"), which states the measurement; it is read as "a failed fit or a
   rank limit, not separated", since the male block is not known to be rank 1 (B's D9).
5. **A threshold U on the male banks (revision 1.3, frozen before unsealing; Ark, Zcode).** On
   both male banks γ\*_P = γ_R = the family limit = 0.75, so the transition band [γ\*_P, γ_R) is
   **empty by construction**, and every U world of the pre-run lies at or below the limit (lobe L
   7: 3 at γ 0.5, 3 at 0.6, 1 at 0.75; lobe R 5: 2 at 0.5, 1 at 0.6, 2 at 0.75; none above;
   §3.3.1 (d)). A's reading of U, "the signature of the leg-P detection limit γ\*_P" (A §4,
   revisions 3.1, 3.2; A's three U worlds sat on γ\*_P = 0.6, inside a one-step band), does not
   hold here. **On the male arm a threshold U reads "not detected at the R level: the two legs,
   or the two D1 candidates, disagree", with no position on a threshold** (not "at the
   threshold"). It is not read as "below the limit" either: it says only that R was not reached
   and that the evidence is split; in the worlds that happened at γ from 0.5 up to the limit. The
   label string stays A's ("U: on the detection threshold; cannot be separated", with the lobe's
   limits); the script prints, after the quoted row and the A-literals line, one line with this
   reading and the lobe's band, the γ of its U worlds and how many lie at and above the family
   limit (S29). It applies to a threshold U only: a failed-fit U, a not-measured U, the "not
   readable" U and a renamed U keep their own texts. If the registered run's synthetic step gave
   a non-empty band (it cannot while it reproduces the references), the line says so and claims
   nothing.

**Leg S in every branch (revision 1.1, frozen before unsealing; Ark, Zcode).** "The primary passes
leg S" means the count, `n_ge = 0` of the `99 − n_deg` shuffles with an AUC (A §4's own wording;
`knockout_regrow.py:1067`), never `p_S <= 0.01`. `p_S` is printed beside it as information, with
four decimals and a mark when `n_deg` >= 1 (§3.2, S28). This is not a further difference: A's rule
is the count; the arm only prints `p_S` so that it cannot be misread as the deciding quantity.

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
| any other pair | | **split: "lobe L reads X, lobe R reads Y"**, with the classification of §4.3. A split is not R, W or G on the male CNS. **Revision 1.3:** a split by reading, not a block difference; the two are printed apart (§4.3, "Two objects"; S32) |
| a lobe with no AUC or "not readable" | | **one lobe only: "lobe ℓ reads X; lobe ℓ′ cannot be read (reason)"**. Not a male R even if X is R |

**The male R is a conjunction of two A criteria (revision 1.1, frozen before unsealing; Johnny,
Ark, Zcode).** A male R requires A's R in lobe L **and** A's R in lobe R. What that does, stated
before data:

- **Power: lower than a single-bank R, and not calibrated.** Both lobes must pass both legs on
  both D1 candidates. The synthetic worlds measure each lobe's R on 32/32 boards (§3.6); no
  registered quantity measures the joint R rate on the real blocks, whose shape is sealed.
- **Null: not squared.** If the two lobes were independent tests, each with a false-R rate near
  `P_R` = 0.01, a false "R in both" would be about 1e-4. They are not independent: both lobes use
  one permutation matrix (seed 92000), one set of shuffle seeds and boards, and nearly the same
  outside (493 of lobe R's 526 present outside cells are present in lobe L too; §1.4). The false
  "R in both" rate therefore lies between `p_L · p_R` and `min(p_L, p_R)`, and with dependence this
  strong it is nearer the upper end: **about 1 %, not 1e-4.** Neither end is calibrated; nothing in
  this registration measures where between them it lies.
- **So the male R is stricter in power and hardly stricter in null.** It is read as "R in each of
  two strongly dependent readings of one animal", not as a replication.
- **A split is the likely outcome for a marginal signal, and it is registered as such.** A block
  near the detection limit can pass in one lobe and not in the other (one lobe R, the other U or
  G). Such a split is informative: it is classified by §4.3 and printed with both lobe labels. It
  gets **no male label**. That is a registered choice, made here before data, not a loss to be
  repaired after it: no rule reads a split as a weak R, and no second criterion is added after
  unsealing.

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
| **S2a: differs more than the rest of the lobe, away from the cut** | `k >= k*`, and **every one** of the k differing block cells has `x` outside [0.5 `c*`, 2 `c*`] in both lobes | "Block A differs between the lobes more than the rest of the lobe does (k of 64; P(X >= k) = … under the outside rate), and no differing cell lies near the cut: a difference specific to block A. Its two explanations, variation within the animal and a difference of reconstruction or typing of the block types, are not separated by this test. The R1–R6 asymmetry is excluded as its carrier (R1 is not a block type, and R1's row and column are the same cells in both lobes at `c*`)." |
| **S2b: differs more than the rest of the lobe, at the cut** | `k >= k*`, and **at least one** differing block cell does not meet S2a's condition (its `x` lies within [0.5 `c*`, 2 `c*`] in at least one lobe) | "Block A differs between the lobes in k of 64 cells (P(X >= k) = … under the outside rate), and j of them lie near the cut: block cells at the threshold; the same mechanism as 33 of the 36 differing outside cells; specificity to block A not established." |

**S2 is conditional on `x` (revision 1.1, frozen before unsealing; Johnny, strengthened by Ark and
Zcode).** Revision 1's S2 read every `k >= k*` as "a difference specific to block A". But 33 of the
36 outside cells that differ between the lobes lie near the cut in both lobes (§1.4): a lobe-wide
difference in `x` near `c*` turns cells over one by one, and block cells near the cut would turn
over by the same mechanism. So "specific to block A" is read only when no differing block cell is
near the cut (S2a); otherwise S2b says the difference is at the threshold and its specificity is
not established. The band [0.5 `c*`, 2 `c*`] is the one §1.4 used for the outside cells, fixed
before unsealing. S2a requires every differing cell to lie outside the band in both lobes; S2b is
its complement, so the two are exhaustive. **Which branch is expected (Ark):** the relayed
description of §1.5 (20–21 weak cross cells with means 1.0–2.2 at c = 1, against `c*` = 2.994 and
0.5 `c*` = 1.497) puts weak block cells in or near the band, so if the lobes' blocks differ, S2b,
the threshold branch, is the expected (modal) one. The relayed numbers are not verified (§10), and
nothing is set from this expectation.

Printed with the class: each differing cell by name with its presence in each lobe, whether each
lobe's `x` lies within [0.5 `c*`, 2 `c*`] (and the count j of differing cells that fail S2a's
condition), and the direction count (L-only against R-only) beside the outside's 3 against 33.
**The binomial reference is descriptive**: block cells are not a random sample of outside cells
(they are strong medulla-to-lobula-plate pathways, not a random draw of type pairs), and the class
decides no label. It separates "a block-specific difference" (S2a) from "a lobe-wide one" (S0, S1)
and from "a difference at the threshold" (S2b). It does not separate variation within the animal
from reconstruction; nothing in one animal's two lobes can (§6).

**Two objects called "split" (revision 1.3, frozen before unsealing; Ark, Zcode; Ark's class
154).** D3's split (§4.2) is **by reading**: the two lobe labels differ. The classes above are
**by block**: `k` of the 64 cells differ in presence. They are different objects, and each can
occur without the other:

- **Labels can differ at k = 0.** It is measured now, on the worlds, where both lobes carry the
  same board by seed (k = 0 in all 45 world pairs): **5 of the 25 dense-grid world pairs split
  by reading** (seeds 92142 U/R, 92161 U/G, 92164 U/R, 92172 R/U, 92183 W/R; lobe L first),
  **none of the 20 pairs of the axis families** (R, Nf, No, W) (§3.3.1 (d); verified on both
  `synthetic_worlds.csv`). With identical blocks, the instrument alone splits one dense-grid pair
  in five (5 of the 20 at γ 0.5–0.85, 0 of 5 at 1.0).
- **S2 may never fire even when the labels disagree**, and an S1 or S2 block difference can
  come with equal labels.
- **After unsealing, a split by reading is not read as "the lobes' blocks differ"** unless the
  class of this section says so (S1, S2a or S2b, with its own text); with S0 it reads "the same
  block, read differently", as S0's text says.

The script prints both, separately and each with its own name, after the male reading (S32):
"Split by reading (section 4.2, D3): yes/no …. Block difference (section 4.3, by block): class …,
k = … of 64 cells differ", followed by the worlds' reference counts computed from the registered
run's own synthetic steps.

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
| **G** (both lobes) | any other pair | Agreement: "not detected at the R level in the template or in either lobe of one animal, each against its own limits". The limits are not compared across banks as numbers (§3.6). A G in the animal does not strengthen flyvis-65's G beyond its own limits. **Revision 1.1 (Johnny, Ark, Zcode):** agreement removes "an artefact of averaging" as the only explanation of flyvis-65's G **only at a power not below A's**, and that is not measured: the male R is a conjunction of two lobes, with lower and uncalibrated power (§4.2), and each lobe's limits are measured on its own instrument-bank pair. **A male G is weaker than it reads**: it is printed with the sentence "power of the male R not calibrated; this G does not by itself exclude averaging as the explanation of flyvis-65's G" |
| **U**, split, one lobe only | any other pair | flyvis-65's G stands alone; the male reading, its lobe labels and, for a split, its class (§4.3) are printed beside it |

**Per lobe**, A §5's table applies to each lobe's label, with "the block" meaning that lobe's
block and "on flyvis's averaged template" replaced by "in lobe ℓ of one male, on an existence bank
at `c*`".

**The instrument is weaker on the male banks, named with its numbers beside any male G
(revision 1.3, frozen before unsealing; Ark, Zcode).** A G on the male arm, in a lobe or as the
male reading, is stated against an instrument that the pre-run measured to be weaker than A's
(§3.3.1 (d); verified on both `synthetic_worlds.csv`, rule #2.1 rows):

| γ | lobe L: seen, R | lobe R: seen, R | A: seen, R |
|---|---|---|---|
| 0.5 | 0/5, 0/5 | 1/5, 1/5 | 1/5, 1/5 |
| 0.6 | 2/5, 1/5 | 2/5, 2/5 | 3/5, 2/5 |
| 0.75 | 5/5, 4/5 | 5/5, 3/5 | 5/5, 5/5 |
| 0.85 | 4/5, 3/5 | 4/5, 4/5 | 5/5, 5/5 |
| 1.0 | 5/5, 5/5 | 5/5, 5/5 | 5/5, 5/5 |

In each pair the first number is the worlds at that γ in which rule #2.1 is **seen** (`p_P` <=
0.01), the second the worlds whose label is **R**, of 5. So rule #2.1 is seen at γ 0.6 in 2 of 5
worlds in each lobe (A 3 of 5), which moves γ\*_P to 0.75 (A 0.6); above the limit, R is read in
4/5 and 3/5 worlds at γ 0.75 and 0.85 in lobe L and 3/5 and 4/5 in lobe R (A 5/5 and 5/5).
**One M world above γ_R reads G in both lobes:** M0.85, seed 92184 (rule #2.1 AUC 0.5254, `p_P`
0.3695 in lobe L; AUC 0.5420, `p_P` 0.2872 in lobe R). **One M world above the limit reads W in
lobe L:** M0.85, seed 92183 (rule #2.1 `n_ge` = 1 of 99; lobe R reads it R). A has neither. The
script prints this beside every G of a lobe and beside a male G, computed from that lobe's
synthetic step in the registered run (S31): "The instrument on lobe ℓ is weaker than A's …: per
gamma, rule #2.1 seen (p_P <= 0.01) / read R, of the worlds at that gamma: … (A: …); gamma\*_P = …
(A 0.6), gamma_R = …; M worlds that read G at or above gamma_R: …; M worlds that read W: …. This
G is stated against these limits." It adds to the male G sentence of the G row above; it changes
no label.

## 6. What the test cannot show (delta on A §6)

A §6 applies, except its male-CNS item, which this arm replaces, and in addition:

- **One animal.** Two lobes of one male are not two animals. A split's class separates a
  block-specific difference from a lobe-wide one; it cannot separate variation within the animal
  from a reconstruction or typing difference (§4.3). A second male, or a female, is not in this
  registration.
- **A signal in one lobe is not read as R (a named cost; revision 1.1, Johnny, Ark, Zcode).** The
  male R needs R in both lobes (§4.2). A block that regrows at the R level in one lobe only is a
  split, classified by §4.3, with no male label. For a marginal signal that is the likely outcome.
  The conjunction lowers the power of the male R, and its power is not calibrated; its false-R rate
  is not squared (the lobes share one permutation matrix, one set of boards and nearly the same
  outside), so it lies between `p_L · p_R` and `min(p_L, p_R)`, about 1 %, not 1e-4, and neither
  end is calibrated. Stricter in power, hardly stricter in null.
- **One cut.** The verdict is at `c*` = 2.994 (`w_min` = 1). The builder printed the outside at
  other cuts (`BUILD.md` lines 188–238); the block at those cuts is not scored.
- **An existence bank.** No offsets, counts or sign exist on it (builder §7, D8); those fields are
  meaningless here. The within-type averaging to one mean per type pair is itself an averaging
  (over the target neurons of a lobe), though not over columns or animals.
- **Boards in the worlds, an unknown block in reality.** The limits are measured on 32/32 rank-1
  boards (§3.6). If the male block has another count or shape, its G is still stated against those
  limits, in M-world units, on the lobe's degree terms.
- **The G gate is not automatic,** since the male block is not known to be rank 1 (§2).
- **A weaker instrument (revision 1.3; Ark, Zcode).** On the male banks rule #2.1 is seen at
  γ 0.6 in 2 of 5 worlds per lobe (A 3 of 5), R is read in 4/5 and 3/5 (L) and 3/5 and 4/5 (R)
  worlds at γ 0.75 and 0.85 (A 5/5), one world at γ 0.85 (seed 92184) reads G in both lobes and
  one (seed 92183) reads W in lobe L (§5, the table). A male G is stated against this instrument,
  and the script says so beside it (S31).
- **A U has no position on a threshold (revision 1.3; Ark, Zcode).** On the male banks the
  transition band is empty and the U worlds lie at γ 0.5–0.75, at or below the limit; a threshold
  U reads "not detected at the R level: the two legs, or the two D1 candidates, disagree", not
  "at the detection limit γ\*_P" (§4.1 (5); S29).
- **A split by reading is not a block difference (revision 1.3; Ark, Zcode).** With identical
  blocks (k = 0) the lobes' labels differed in 5 of 25 dense-grid world pairs; a split by reading
  says nothing about the blocks unless §4.3's class says so (§4.3, "Two objects"; S32).
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

**Revision 1.1 (D13; Johnny, Ark, Zcode).** All three reviewers keep the CPU instrument (i) for
this arm: the pinned pre-run must be made by the same instrument as the registered run, and the
GPU instrument has no registration yet. **Its economics, as Ark and Zcode gave them (relayed, not
recomputed here, except 1 − 4,870 / 7,846 = 37.9 %):** the hybrid saves about 38 % of a pass
(4,870 s against 7,846 s), not a factor 2.3; rule #2.1 is not faster on GPU; the ceilings, the
fixed-λ diagnostic and the permutations are not ported. **Option (iii) (Johnny, Ark):** during the
pre-run, the GPU instrument may run the male worlds as a second, unregistered cross-check. It
decides nothing, its output is an input to no gate, reference or registered value, and it is
reported apart from the pinned references. **The GPU instrument gets its own registration, on a
separate track** (Mike's word, DPC Research chat, 09:13 UTC: "review the GPU instrument"); nothing
in this arm waits for it.

**Revision 1.2, a chat-only note (relayed by CC; read from no file by this revision; decides
nothing for this arm, D13 (iii)).** The GPU cross-check V8 on lobe L, against the lobe's CPU
pre-run store: **EQUIVALENT (outcome 1)**; E1 0; flipped pairs 0; at-risk 0; 8 fits not
bit-equal; the male lobe L BF-active count 557 of 18,000 (3.1 %). V8 on lobe R was running when
this revision was written. Its output is an input to no gate, reference or registered value of
this arm (§3.3.1). See §3.3.1 (g) for why V8 cannot be rerun at a head containing this revision
without a change on the GPU instrument's side.

**Revision 1.3, a chat-only clarification for the GPU track (decides nothing for this arm, D13
(iii)).** Ark reported at-risk counts A 12, L 1, R 11 "at threshold 2·2^-23 = 2.384e-7". The
GPU instrument's registered band (its registration, revision 1.4, E2-III; `census.py` `BAND`) is
**2^-23 = 1.192e-7**. Recounted by this revision on both male stores (`raw_fits.json.gz` of each
reference) with the registered definition, through `census.census_fit` itself: the census pair
set S(f) is the present × absent pairs by the fit's own labels (the auc columns) on every record,
and all 2,016 pairs only on a base view's `ko`/`ko1` record (the auc_null columns); a fit is at
risk when the smallest gap between **distinct** values of `p` on S(f) is below the band; exact
ties are not gaps and are counted apart, as tied pairs.

| scope (fits per store) | lobe L: < 2^-23 / < 2·2^-23 | lobe R: < 2^-23 / < 2·2^-23 | tied pairs on S(f), L / R |
|---|---|---|---|
| every fit (28,665) | 1 / 2 | 3 / 11 | 846,270 in 26,966 fits / 814,576 in 27,067 fits |
| `ko` and `ko1` records, base views and shuffles (27,225) | 0 / 1 | 3 / 11 | 788,910 / 758,387 |
| D1 subset: BF_1–BF_4 `ko`, base views and shuffles (18,000; V8's composition) | **0 / 1** | **1 / 8** | 475,457 / 456,929 |

**The D1 subsets by name.** Lobe L, at 2·2^-23 only: `world:M1.0:4 ko BF:4` (a base view, all
pairs; gap 1.97e-7; two absent cells). Lobe R, at 2^-23: `world:M0.5:0|sh:98 ko BF:1` (gap
1.06e-7); at 2·2^-23 also `world:R:1|sh:29 ko BF:1`, `BF:2`, `BF:3`, `BF:4` (gap 1.33e-7 each, the
same pair), `world:R:2|sh:37 ko BF:1` (2.20e-7), `world:R:4|sh:12 ko BF:1` (1.78e-7) and
`world:M1.0:0|sh:67 ko BF:1` (2.23e-7): 8. The fits outside D1 that make up the rest: L, a
permuted-block ceiling of rule #2.1 (`full`, below both bands); R, one rule #2.1 `ko` shuffle
and the base `ko1` record of BF_4 (all pairs), both below both bands, and at 2·2^-23 also one N1
`ko` shuffle (3 + 8 = 11). **Ark's L 1 and R 11 are the counts at 2·2^-23 on the `ko`/`ko1`
scope** (both reproduced exactly; R's also on every fit); at the registered band they are L 0 and
R 3 (D1: 0 and 1). A's store, the same definition, as a cross-reference: 6 / 14 (every fit),
6 / 13 (`ko`/`ko1`), 4 / 8 (D1); Ark's A 12 is not reproduced by any of these three scopes. This
belongs to the GPU track; nothing in this arm reads it.

### 7.2 Script changes (listed; none is made by this draft; D14)

| # | where (A's script, lines at `74db080`) | change |
|---|---|---|
| S1 | the file | a new script, `results/genome/c6/checks/knockout_regrow_male_cns.py`, a copy of A's with the changes below, reviewed as a diff against it; A's script stays byte-unchanged; a new label test beside A's |
| S2 | `REGISTRATION`, `REGISTRATION_REVISION`, the manifest (:109-110, :2583-2601) | this file and its revision; A's registration path pinned by its LF sha256 **after** the D11 amendment, because §4 is quoted from it (`quote_row` :2373-2379, `quote_section` :2367-2370); the builder's registration and `bank.meta.json` recorded. **`quote_row` reads from the amended A, never from this file (revision 1.1; Johnny, Zcode).** It returns the first line that starts with the label's key (`next(...)`, :2379). In A the U and G keys already match two rows each, §4's and §5's (A lines 1328 and 1382 for U, 1327 and 1381 for G; R and W one each, 1325 and 1326); the quote is §4's only because §4 comes first. This file has **zero** such rows (§4.2's table starts "\| R \| R \|"), so quoting from it would raise `StopIteration`. The amendment to A is appended after A's last line (§9.3), below both tables, so it cannot capture the first match even if it held such a line |
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
| S17 | `PRERUN_DIR`, `PRERUN_SHA256`, `PRERUN_WORLDS_CSV_SHA256`, `PRERUN_REV2_FAMILIES`, `PRERUN_REV3_FAMILIES`, `_mech_renamed_32` (:124-136, :1336-1338) | one reference per lobe, set in the revision after the pre-run (D15); A's revision-2/3 split and revision 3.2's rename check are A's history and not needed. **Revision 1.2: set** (§3.3.1 (c)); `PRERUN_DIR` unchanged (D17) |
| S18 | `out_dir_refusal` (:2307-2333) | refuses `--out` at or in A's reference, B's (once it exists) and both male references, and on byte copies of any of them |
| S19 | `write_committed`, `OUT` (:111, :2425-2459) | `results/genome/c6/checks/knockout_regrow_male_cns/`; a title naming the arm; the male reading first, then each lobe's verdict line, the quoted §4 row and the line naming A's literals (§4.1); the joint reading with flyvis-65 (§5); per-lobe `per_shuffle_<lobe>.csv` and `synthetic_worlds_<lobe>.csv` |
| S20 | `main`, `--arm` (:2498-2533) | `--arm malecns` runs both lobes (§4.2); `--synthetic-only --lobe L|R` for the pre-run; `private_run_dir` gives `malecns_<UTC stamp>_<head 12>`; **`--allow-dirty` refused with `--arm malecns`** (D10) |
| S21 | new: the unseal step | `open_sealed(lobe)`, called only from the real-arm path after both lobes' synthetic steps and checks 1, 2, 4, 6, 7, 8, 9, 10 have passed: checks the sha256 first, then parses the fixed-width file, runs check 11, returns the present block cells with `n_syn = x`; prints the file's cross-lobe block-weight line after the verdicts (§7.4) |
| S22 | `machine_checks_real` (:2464-2495) | checks 6 and 9 before unsealing on the two synthetic block fillings; check 6′ after unsealing against the pre-unseal hash |
| S23 | new: the lobe comparison | `lobe_split_class(y_L, y_R, x_L, x_R)` (§4.3, with `k*` computed from 36 / 2,961 and checked equal to 4; S2 split into S2a and S2b by the band [0.5 `c*`, 2 `c*`] on each differing cell's `x` in both lobes, revision 1.1) and `male_reading(label_L, label_R)` (§4.2); the joint reading with flyvis-65 (§5) as a table lookup, no computation |
| S24 | `WITHIN_FLY_NOTE` (:237-239), the `TAU` comment (:228-233) | the within-animal note of §3.5; the lattice text made generic |
| S25 | `print_bank`, `md_bank_table`, `summary.json` (the D7 fields, :1077) | the offset, count and sign fields printed under "meaningless on an existence bank" |
| S26 | `SEAL_RECORD`, new | a constant, "intact" in this revision; if a registered amendment records a break of the seal before review, the verdict lines end with the builder's note "block A of the male CNS was read before its registration was reviewed" (builder §9) |
| S27 | tests | §7.3 |
| S29 | new (revision 1.3; Ark, Zcode): `male_u_reading_line`, called in `real_arm_lobe`, printed in `_finish_real_arm` and `RESULT.md` after the A-literals line | with a lobe's **threshold** U only: the male U reading of §4.1 (5), with the lobe's band, the γ of its dense-grid U worlds and how many lie at and above the family limit, computed from the lobe's synthetic step; if the band is not empty, a line saying so that claims nothing; `None` for R, W, G and for a failed-fit, not-measured, not-readable or renamed U. No label string changes |
| S30 | new (revision 1.3; Ark, Zcode): `PRERUN_GIT_HEAD`, `PRERUN_SCRIPT_SHA256_LF`, `prerun_provenance`; `run_synthetic_only` (reference mode) and `_run_real_arm` | the head and script that made each reference (`a0e16b6`, `7a09f9fd…`, read from each reference's manifest after `check_prerun_files`); a mismatch stops with "PRE-RUN PROVENANCE DIFFERS" before any fit; both codes printed and recorded in the manifest (`prerun_provenance`) and in `RESULT.md`'s header ("pre-run made by …; this run by …"). The `--from-raw` check after the merge (§3.3.1 (h)) is a procedure, not code |
| S31 | new (revision 1.3; Ark, Zcode): `A_CURVE_TEXT`, `male_g_instrument_line`, called in `real_arm_lobe` (a lobe G) and `_finish_real_arm` (a male G, both lobes) | the instrument's numbers of §5 beside every G: the power curve (seen, R) per γ against A's, γ\*_P against A's 0.6, γ_R, the M worlds that read G at or above γ_R with rule #2.1's AUC and `p_P`, and the M worlds that read W with `n_ge`; computed from the lobe's synthetic step |
| S32 | new (revision 1.3; Ark, Zcode): `split_notions`, called in `_finish_real_arm`; `summary.json` `split_notions`; `RESULT.md`'s lobe comparison | the split by reading and the block difference printed apart, each with its own name, the rule that one is not read as the other, and the worlds' reference: world pairs whose labels differ on the dense grid and on the axis families, with each pair's `k` (0: the same board) |
| S28 | the `p_S` prints: the verdict line (:1252), `print_bank` (:2083), `md_check_and_curve` (:2162, the synthetic table), `md_bank_table` (:2393); `N_DEG_SENTENCE` (:310-311) (revision 1.1; Ark, Zcode) | when `n_deg` >= 1, `p_S` is printed with four decimals and the mark "[leg S decided by the count: n_ge = 0 of n_valid]" (or "n_ge = k of n_valid" when it fails); when `n_deg` = 0, as A; no decision reads `p_S` (leg S stays `n_valid >= 1 and n_ge == 0`, :1067) |

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
  `lobe_split_class` on hand-made `y_L`, `y_R` (S0, S1 with k = 3, S2a with k = 4 and every
  differing cell's `x` outside [0.5 `c*`, 2 `c*`] in both lobes, S2b with k = 4 and one cell
  inside the band in one lobe only); `k*` = 4.
- **T12, the `p_S` print (S28):** a fixture evaluation with `n_deg` = 1 and `n_ge` = 0 passes leg
  S and prints `p_S = 0.0101` with the mark; with `n_deg` = 0 the line is A's.
- **T10, seeds and refusals:** the seed assertion; `--allow-dirty` with `--arm malecns` refused;
  `out_dir_refusal` on all four reference folders (monkeypatched to temporary folders, never the
  real ones, as A's `test_out_guard_refusals`).
- **T11, check 3 and 5 as prints:** a fixture block that is not a board prints its counts and does
  not stop; `D(N1 logit)` is printed.
- **T13, the registered references (revision 1.2):** for each lobe, on the real reference folders
  (synthetic worlds only; the seal guard records zero sealed-file calls): `reference_mode` is
  true; `check_prerun_files` passes with nothing unlisted and exactly the four files; the worlds
  CSV pin is the listed one; `smallest_passing_auc` derives as {z: 0.671875, z': 0.669921875}
  from 40 and 5 worlds and equals `board_smallest_passing_auc()`; the `ko1` count read from the
  store is §3.3.1's; the manifest records head `a0e16b6`, a clean tree, no `--allow-dirty`, no
  sealed file touched, a full non-smoke run in pre-run mode; `--out` is refused at the reference
  and at the pre-run folder it was copied from; the only placeholder left is A's amended hash, and
  `check_registered_constants` refuses on it. T3's `--synthetic-only` test now sets lobe L's pins
  to `None` for its duration, so that it keeps testing pre-run mode on fixture fits.
- **T14, revision 1.3 (S29–S32):** S29 on fixture worlds shaped like lobe L's pre-run (empty
  band; the line gives "0.5: 3, 0.6: 3, 0.75: 1", "1 at it, 0 above it" and the frozen reading)
  and on A's shape (a one-step band: the line claims nothing); no line for a failed-fit, not
  readable or renamed U, or for a G; and on both registered references (L 3/3/1, R 2/1/2). S31 on
  fixtures and on both references: lobe L's curve "0.5: 0/5, 0/5; 0.6: 2/5, 1/5; 0.75: 5/5, 4/5;
  0.85: 4/5, 3/5; 1.0: 5/5, 5/5", seed 92184 with AUC 0.5254 and `p_P` 0.3695, seed 92183 W with
  `n_ge` = 1 of 99; lobe R's curve, 92184 with 0.5420 and 0.2872, no W. S32 on fixtures (a split by
  reading with class S0, k = 0) and on both references ("5 of 25 dense-grid world pairs … 0 of 20
  axis-family pairs; every world pair has k = 0"). S30 on both references (head `a0e16b6`, script
  `7a09f9fd…`, "different code"; a wrong constant fails). T3's real-arm flow also checks that the
  manifest carries both lobes' provenance and that `RESULT.md` prints S30's and S32's lines; its
  fixture references set `PRERUN_GIT_HEAD` and `PRERUN_SCRIPT_SHA256_LF` to the head and script
  that made them.

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

**Revision 1.2: the pre-run as run.** The two `--synthetic-only` commands above, each with `--out
../connectome-seed-data/knockout_regrow/malecns_prerun_<lobe>_20260926T131249Z` (the manifest's
arguments and `private_outputs`, §3.3.1 (a)), from `a0e16b6` with the tree clean. The registered
run is the third command, unchanged, from the committed head that carries A's amended hash (D15
steps 4 and 5).

**Revision 1.3: the check before the registered run** (§3.3.1 (h)), from the merged head with
the tree clean, both lobes, before the third command:

```
tools/.venv/Scripts/python.exe results/genome/c6/checks/knockout_regrow_male_cns.py --synthetic-only --lobe L --starts 10 --workers 5 --from-raw ../connectome-seed-data/knockout_regrow/synthetic_malecns_L_prerun/raw_fits.json.gz
tools/.venv/Scripts/python.exe results/genome/c6/checks/knockout_regrow_male_cns.py --synthetic-only --lobe R --starts 10 --workers 5 --from-raw ../connectome-seed-data/knockout_regrow/synthetic_malecns_R_prerun/raw_fits.json.gz
```

Each must print "outcome 1: every deciding column equal; byte-identical" with the recomputed
sha256 equal to the lobe's pin, else the registered run does not start.

**Outputs:** committed aggregates in `results/genome/c6/checks/knockout_regrow_male_cns/`
(`RESULT.md`, `summary.json`, `per_shuffle_L.csv`, `per_shuffle_R.csv`, `synthetic_worlds_L.csv`,
`synthetic_worlds_R.csv`); private and raw outputs as §7.4; the two references in their own folders
(§3.3). Male CNS data is CC-BY (builder §1.1). **What `per_shuffle_L.csv` and `per_shuffle_R.csv`
carry (revision 1.1, Johnny; read from A's code):** the **real arm's** leg S, not the synthetic
worlds'. A's `write_committed` calls `write_per_shuffle_csv(real, …)` (`knockout_regrow.py:2429`)
on the real bank's evaluation; each of its 99 rows (`evaluate_bank`, :1024-1034; writer :2344-2352)
holds `sd`, `present` (the present count of the shuffled bank's 64 block cells), `degenerate`,
`auc_N1`, and for each of the six predictors its AUC on the shuffled block, its margin `M` over N1
and the λ selected. Per lobe, the rows are that lobe's real-bank shuffles. They are aggregates (no
per-cell male data); the `present` column is a count on shuffled banks that contain the real
block, written only after unsealing. The synthetic worlds' shuffles are summarised in
`synthetic_worlds_<lobe>.csv` (`n_ge`, `n_deg`, `n_valid_shuffles`, `p_S` per world and predictor)
and are not written per shuffle.

**Cost (A §7's rate):** pre-run about 4 h 22 min (both lobes, with the `ko1` fits, §3.6);
registered run about 4 h 22 min for the two synthetic steps plus, per lobe, 6 × (3 + 99) + 20 = 632
real-arm fits, 5 fixed-λ fits and the checks' 4 rule fits, and 20 C6 folds once for check 8:
about 8 min. **Total about 8 h 52 min of CPU wall time on 30 workers.** The rate on the placed grid is assumed, not measured (§10).

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
| **D4** | The rule that separates the explanations of a split (builder D12, §12) | **(i) the classification of §4.3**: S0 same block; S1 differs within the lobes' outside rate; S2 differs beyond it (`k* = 4` from 36 / 2,961), read as specific to block A only if no differing cell lies near the cut (S2a), else as a difference at the threshold (S2b; revision 1.1); R1–R6 excluded as a carrier by the build's facts; within-animal variation and reconstruction named as not separable. (ii) print the lobe difference, classify nothing: no registered reading of a split. (iii) read every split as within-animal variation: claims what one animal cannot show | **(i)** |
| **D5** | The existence bank (builder §7, §12) | **(i) run the registered predictors and harness unchanged on one `(0, 0)` offset per present cell; the offset, count and sign fields printed as meaningless; the existence path checked by T5 and by the pre-run** (§2). (ii) put a synthetic offset structure into the male bank: content that the animal does not have | **(i)** |
| **D6** | Synthetic worlds and limits (builder D13; Ark's ×1.22 point) | (a) **transfer A's limits and `smallest_passing_auc`** (γ\*_P 0.6, γ_R 0.75, family 0.75): no pre-run, 0 h; but they were measured on flyvis-65's degree terms, the 65 grid, density 0.137 and content with offsets, so a male G would carry limits of another instrument-bank pair. **(b) rebuild A's 45 worlds on each lobe** (degree terms, grid, content pool and density of the lobe; §3.6): about 2 h 11 min per lobe per pass, **4 h 22 min for the pre-run and 4 h 22 min again in the registered run** (with the `ko1` fits, §3.6). (c) one world set on one lobe's outside, used for both lobes: half the cost; the lobes' outsides share 493 of 526 present cells, so the other lobe's limits would likely be close, but they would be assumed, not measured | **(b)** |
| **D7** | Seeds | (i) **A's seeds, as A §8 says** ("the same legs, cuts, seeds and branch rule apply"): the leg-P null would be flyvis-65's permutations, and the boards' `smallest_passing_auc` would reproduce A's registered values; but the worlds are different objects on another grid, so sharing A's world seeds buys no comparability and makes their CSV keys collide with A's reference. **(ii) a new range, 92000–92999, shared by both lobes** (§3.7): disjoint from A and B; common random numbers between the lobes. (iii) new seeds per lobe: a lobe difference could then come from a draw. (iv) A's leg-P seeds (90000, 90001) and new world and ceiling seeds: comparability of `p_P` with flyvis-65, at the cost of a mixed rule. **Revision 1.1 (Johnny; Ark, Zcode):** under (ii) the **direct comparability of the male `p_P` with flyvis-65's is given up**, stated as the price of (ii); and A §8's sentence "the same legs, cuts, seeds and branch rule apply" is cancelled, as it concerns seeds, by the amendment to A, with the address of §3.7 (§9.3) | **(ii)**, kept |
| **D8** | Checks 3 and 5, the metric, and the unreadable block | **(i) check 3 prints the block after unsealing and stops only on no AUC; check 5 prints; precision at `n_present`, the other 61 cells; a block on which leg P cannot pass (`smallest_passing_auc` = None) reads the new U text "not readable"** (§3.2, §4.1). (ii) keep check 3 as a comparison with a count: there is no reviewed count, and writing one now would be selection with the knowledge of §1.5. (iii) no new U text: such a block could then read G, a vacuous G, since leg P could not have passed. **The asymmetry with D9, named (revision 1.1, Johnny):** no AUC is fatal for the lobe, because there is no verdict to print; an `rc_patterns` cap hit on a real block is a diagnostic, and the verdict stands | **(i)** |
| **D9** | The row-and-column variant's attempt cap (builder §12) | **(i) a cap of 100 × 640 attempts per chain; a hit stops a synthetic step (a malfunction on a 32/32 board) and prints "n/a (attempt cap reached: …)" on a real block, which goes on**; the no-checkerboard pre-check prints "n/a". (ii) a hit stops everywhere, as B's D7: on the real block the stop would come after the seal is broken, forfeiting the run for a diagnostic that decides nothing; a sparse real block can hit the cap although swappable (§3.2). (iii) no cap: a real block with no reachable swap would never end | **(i)** |
| **D10** | The unseal protocol (builder §9) | **(i) §7.4: the sealed files are opened only by the registered real run, after every gate that does not need them; `--allow-dirty` refused with the male arm; a failure after unsealing is recorded, and a second run only on Mike's word.** (ii) A's rule, a dirty real-arm run allowed and marked "not the registered run": such a run opens the sealed files, which builder §9 allows only in the registered run | **(i)** |
| **D11** | Where the bank pins live (A §8; builder §10.5 step 4) | **(i) amend A, append-only, with the four bank pins, as both documents promise, and pin them in the arm's script too.** A's LF sha256 then changes from `409184de…`: the flyvis-65 run's manifest keeps the old value as the text it ran under; **block B's S2, which pins A "by its LF sha256 at `74db080`", must pin the amended hash or read A from git at `74db080`** (B is not yet implemented). (ii) pin only here and leave A unedited, recording here that A §8's promise is discharged here: A's text would keep a promise that A itself never shows fulfilled. **Revision 1.1 (Johnny, Ark, Zcode):** the amendment's content is specified in §9.3: the four bank pins; the cancellation of A's seeds for this arm (D7); and the line `git show 74db080:docs/plans/2026-09-24-knockout-regrow-registration.md` as the way to recover the text under which the flyvis-65 verdict was made (Johnny). Every place that cites A by its LF hash or "at `74db080`" is listed there, with which is updated and which stays history (Ark), checked by grep | **(i)**, kept, with §9.3 |
| **D12** | Verdict-line strings | **(i) A's rows quoted verbatim, then the four differences of §4.1** (lobe prefix; the "not readable" U; a line naming A's literals; "failed fit" read as fit failure or rank limit); **revision 1.3 adds a fifth**, the male reading of a threshold U with an empty band (§4.1 (5), S29), printed as a line of its own; no label string changes. (ii) restate §4 with the male's literals: a new text of a reading rule, reviewed as such. **Revision 1.1 (Johnny, Zcode):** the rows are quoted from the **amended A**, not from this file. `quote_row` takes the first line starting with the key (`knockout_regrow.py:2373-2379`); in A the U and G keys already match two rows each (§4's and §5's; A lines 1327–1328 and 1381–1382), and the quote is §4's only because §4 comes first. This file has zero such rows, so quoting from it would raise `StopIteration`. The amendment is appended after A's last line, below both tables, so it cannot capture the first match (S2) | **(i)** |
| **D13** | Instrument | **(i) the pinned CPU harness, as A and B**: about 8 h 52 min of wall time in all (revision 1.1, with the `ko1` fits). (ii) the GPU instrument of `cdbde9e`: separate and unreviewed, BF about 2.3 times faster, rule #2.1 not faster, base views not all bit-equal; by A §7 it needs its own registration and synthetic worlds. **(iii) (revision 1.1; Johnny, Ark):** (i), and the GPU instrument may run the male worlds during the pre-run as a second, **unregistered** cross-check: it decides nothing, and its output is an input to no gate, reference or registered value. **Revision 1.1 (all three reviewers):** (i) is kept, because the pinned pre-run must be made by the same instrument as the registered run, and the GPU instrument has no registration yet; it gets its own registration on a separate track (Mike, 09:13 UTC: "review the GPU instrument"). Ark's and Zcode's economics: the hybrid saves about 38 % of a pass (4,870 s against 7,846 s), not ×2.3; rule #2.1 is not faster on GPU; the ceilings, fixed λ and the permutations are not ported (§7.1) | **(i)**, kept; (iii) allowed |
| **D14** | Script form | **(i) a new file, a copy of A's, reviewed as a diff; A's untouched** (as B's D13 (i)). (ii) a `--arm malecns` inside A's file: the file that A's run and its blind review cite would change. (iii) import A's module and override its constants: `BLOCK`, `MASKS`, `MIRROR_IDX`, `NONBLOCK_CELLS`, `OTHERS` and the world arrays are computed at import (B's D13) | **(i)** |
| **D15** | Order of work | **(i) the header's order**: the script and this draft committed; the pre-run of both lobes from that committed head on Mike's word; a revision registering the values read from the pinned references, reviewed; A amended (D11); the registered run on Mike's word. Each reference has a producer in git. **Revision 1.3:** between the merge (with A's amended hash) and the registered run, the `--from-raw` check of §3.3.1 (h) in both lobes; if either lobe's worlds table is not re-derived byte for byte, the registered run does not start. (ii) A's D11 order (pre-run before commit): repeats the provenance gap of A §3.3 | **(i)** |
| **D16** | The joint reading with flyvis-65's G | **(i) A's D13 table as voted, and the readings of §5** for male R (a flag with a registered list, examined under a new registration, overturning neither verdict), W, G, U and split. (ii) A's D13 table alone, with no reading written before data for the cases it leaves as "any other pair" | **(i)** |
| **D17** (revision 1.2) | Where the pinned references live. The pre-run wrote to `malecns_prerun_<lobe>_20260926T131249Z/`; the script refuses `--out` at the proposed `synthetic_malecns_<lobe>_prerun/` (S18), so the pre-run could not write there. §3.3 proposes those names; the script's `PRERUN_DIR` already holds them, its comment says the reference "is moved to PRERUN_DIR[lobe] in that reviewed change", and each reference's manifest records them as `prerun_dir`; A copied its outputs to its reference folder (A §7, "have been copied to") | **(i) copy the five files byte for byte to `synthetic_malecns_<lobe>_prerun/`, leave the pre-run folders untouched, `PRERUN_DIR` unchanged:** follows §3.3, A's precedent and the script's constant; the pre-run folders stay where the stdout logs name them and where the GPU instrument's V8 reads them (`instrument.py` `MALE_PRERUN_STORES`); the originals then hold a byte copy of a pinned reference, so `--out` there is refused by the content guard (S18), and the copies by the path guard; the cost is a second copy of about 8.9 MB per lobe. (ii) point `PRERUN_DIR` at the pre-run folders: no copy, but the manifest's `prerun_dir` would name a folder that does not hold the reference, and the path guard would then protect the V8 input folders as the references (harmless, but two roles in one folder). (iii) move (rename) the folders, as the script's comment says: one copy, but the stdout logs and V8's `MALE_PRERUN_STORES` would name folders that no longer exist, and V8 on lobe R, whose input is lobe R's pre-run folder, was running when this revision was written | **(i)**, done (§3.3.1 (b)). **Revision 1.3 (Ark, Zcode):** the link copy ← original recorded here with its verification command (all five sha256 equal; §3.3.1 (b)); no file is added to either folder |

### 9.1 Votes on revision 1 (DPC Research chat, 2026-09-26 UTC; as relayed by CC)

| reviewer | time (UTC) | vote |
|---|---|---|
| Johnny | 09:14 | yes, with edits |
| Ark | 09:18 | yes, with edits |
| Zcode | 09:32 | yes, with edits |

Revision 1.1 has not been voted on. Mike's word is not yet given (header).

### 9.2 The edits of revision 1.1, who asked, and where each is applied

Items 1–3 are reading rules, **frozen before unsealing**: they are fixed in this revision, before
either sealed file is opened, and no later revision changes them after the seal is broken. Items
4–15 are the other edits. None changes an option of D1–D16.

| # | edit | asked by | applied in | where this revision differs from CC's brief |
|---|---|---|---|---|
| 1 | The male R is a conjunction of two A criteria: power lower than a single-bank R and not calibrated; the null not squared (one permutation matrix, one set of boards, 493 of 526 present outside cells shared), between `p_L · p_R` and `min(p_L, p_R)`, about 1 %, not 1e-4; "stricter in power, hardly stricter in null"; the G reading weaker than it reads; "a signal in one lobe is not read as R" a named cost; a split named before data as the likely outcome of a marginal signal, informative, with no male label | Johnny, Ark, Zcode | §4.2 (after the table), §5 (G row), §6 (first new bullet) | §5's G row also prints a sentence with the G ("power of the male R not calibrated; …"), so that the weakening is on the output, not only in this file |
| 2 | S2 conditional on `x`: "specific to block A" only if every differing block cell lies outside [0.5 `c*`, 2 `c*`] in both lobes; otherwise "block cells at the threshold; the same mechanism as 33 of the 36 differing outside cells; specificity not established"; Ark's note that the threshold branch is the expected one given §1.5, with the relayed numbers unverified | Johnny; strengthened by Ark and Zcode | §4.3 (S2a, S2b and the note after the table), D4, S23, T9 | the brief's "at least one lies inside" is written as the exact complement of S2a (a cell whose `x` is within the band in **at least one** lobe), so that S2a and S2b are exhaustive; the classes are named S2a and S2b |
| 3 | Leg S: the count decides (`:1067`), `p_S` (`:1068`) is informative; `:.2f` at `:1252` prints 1 / 99 as "0.01"; they coincide only when `n_deg` = 0 (all 270 rows of A's pre-run, by chance); with `n_deg` >= 1, `p_S` printed with more digits and a mark (S28); a sparse block makes `n_deg` >= 1 more likely | Ark, Zcode | §3.2 (new bullet), §4.1 (paragraph after the four differences), S28, T12 | verified: `n_deg` = 0 in all 270 rows of A's pinned pre-run `synthetic_worlds.csv` and of the flyvis-65 run's committed one; the same `:.2f` print is also at `:2083`, `:2162`, `:2393`, all in S28; the digits are fixed at four |
| 4 | D7: the direct comparability of `p_P` with flyvis-65 is given up; the amendment to A cancels A §8's "the same legs, cuts, seeds and branch rule apply" as it concerns seeds, with an address | Johnny; Ark, Zcode | §3.7, D7, §9.3 | the address is A §8, lines 1749–1750 at `74db080`, bullet "The same block by name" |
| 5 | D11: the amendment adds the four bank pins, the seed cancellation, and `git show 74db080:docs/plans/2026-09-24-knockout-regrow-registration.md` as the way to recover the text of the flyvis-65 verdict; every place that cites A by its LF hash or "at `74db080`" listed, updated or history, verified by grep | Johnny; Ark | §9.3, D11, §1.1, header | the grep found three places beyond the brief's four: block B's header (line 14), the blind review note (line 220) and the private run folder's `synthetic_only.json`; all listed in §9.3. The builder speaks of "the four pins" without naming the files; read here as the two outside and the two sealed files |
| 6 | D8: the asymmetry named ("no AUC: fatal, no verdict to print; `rc_patterns` cap: a diagnostic, the verdict stands") | Johnny | D8, §3.2 (guard 3), §3.4 (check 3) | none |
| 7 | §1.5 linked to §3.2: the weak block cells imply a possibly sparse block (`n_present` well below 32), so a higher chance of the "not readable" U | Johnny, Zcode | §1.5 (point 2), §3.2 (`smallest_passing_auc`) | stated as a named risk that sets nothing, in keeping with §1.5's rule that nothing is set from the prior exposure; also linked to `n_deg` (item 3) |
| 8 | M(1) is not an error and not a narrowing but a different object; replaced by the three-part form; moved out of the error ledger | the reviewers (as relayed) | §11 (clarification C1), §0, §1.4 | A's row, as written, is about the male CNS at the thresholds of Zcode's preliminary graph (A §1.4 at `74db080`); the brief's form calls them "every flyvis-65 pair threshold tried on the 65 grid", which no file records. C1 quotes A's row as written and gives the brief's description as the reviewers' |
| 9 | M(2) stays (`flywire_bf_p3.py:73-75`); the builder registration still carries `:74-76` in four places, listed, not edited | Zcode | §11 (M(2)) | verified by grep: lines 214, 705, 976, 1056 of the builder registration at `476cf9b`, as Zcode said |
| 10 | `quote_row`: in A the U and G keys match two rows each; this file has zero such rows (quoting from it would raise `StopIteration`); rows are quoted from the amended A, whose append-only amendment lies after its last line | Johnny, Zcode | S2, D12, §4.1 (difference 3) | verified: `:2373-2379`; A lines 1327 / 1381 (G), 1328 / 1382 (U), 1325 (R), 1326 (W); zero lines of this file start with any of the four keys |
| 11 | §3.3: equal `smallest_passing_auc` in L and R by board holds for the synthetic worlds; not for the real blocks, where the value is new | Ark | §3.3 | none |
| 12 | §7.5: what `per_shuffle_L.csv` / `per_shuffle_R.csv` carry | Johnny | §7.5 | read from the code: the real arm's 99 shuffles per lobe, columns listed |
| 13 | §3.7: the grep inventory is not exhaustive; the conclusion stands, with the count | Zcode | §3.7 | the count: 96,233 occurrences on 92,083 lines in 904 tracked `.py`, `.md` and `.json` files |
| 14 | §3.6: the 5 `ko1` fits per world (+225 per lobe, about +0.8 %) named in the cost formula | Zcode | §3.6, §7.5, D6, D13 | 225 is an upper bound: a `ko1` record whose ko fit selected λ = 1 is copied (A's pinned store: 47 copied, 178 fitted); the totals become 2 h 11 min per lobe per pass and about 8 h 52 min in all |
| 15 | D13: CPU (i) kept; option (iii), the GPU instrument as an unregistered cross-check during the pre-run; the GPU instrument's own registration on a separate track (Mike, 09:13 UTC); Ark's and Zcode's economics | Johnny, Ark, Zcode (Mike's word for the separate track) | D13, §7.1 | the economics are relayed; only 1 − 4,870 / 7,846 = 37.9 % was recomputed |
| 16 | This table, §9.1 and §9.3 | CC's brief | §9.1–§9.3, §12 | none |

### 9.3 The amendment to A: its content (specified here; made in step 4 of the header's order)

This revision does not edit A. It fixes what the amendment will contain, so that the reviewers
vote on it with this file.

1. **Where:** appended after A's last line, as a new section; nothing above it changes. It lies
   below A's §4 and §5 tables, so `quote_row` still returns §4's rows (S2, D12). **Its form
   (revision 1.3, decided by CC):** a new section, "## 13. Amendment 1" (Zcode's position: A's
   §12 holds the changelog and the error ledger, whose rows have their own six-field format and
   should not carry a normative change; the new section carries both addresses, A §8 lines
   1725–1726 (the promise to pin) and 1749–1750 (the seeds), and the pins). **The single pointer
   line Ark asked for is the first line inside §13 itself**, so no line above the amendment
   changes and item 5 ("nothing else") holds. Ark's alternative, a subsection §12.x, is recorded
   and not taken, for Zcode's reason (Appendix A).
2. **The four bank pins** (A §8: "amended, before that arm runs, to pin the built bank's sha256";
   builder §10.1, §10.5 step 4): the sha256 values of `male_cns_L_outside.csv`,
   `male_cns_R_outside.csv`, `male_cns_L_blockA.sealed.csv` and `male_cns_R_blockA.sealed.csv`,
   as in §1.1, with the build folder's name.
3. **The seeds, cancelled for the male arm (D7):** "A §8's sentence 'The same legs, cuts, seeds and
   branch rule apply' (A lines 1749–1750 at `74db080`, bullet 'The same block by name') no longer
   applies to seeds for the male CNS arm. Its seeds are those of
   `docs/plans/2026-09-26-knockout-regrow-male-cns-arm-registration.md` §3.7. Legs, cuts and the
   branch rule apply as written."
4. **The text of the flyvis-65 verdict:** "The flyvis-65 verdict (commit `1ed55ec`) was made under
   revision 3.4.1, LF sha256 `409184de…3facd6`. That text is recovered with
   `git show 74db080:docs/plans/2026-09-24-knockout-regrow-registration.md`."
5. **Nothing else** (A §8: "nothing else in it changes").

**Every place that cites A by its LF hash (`409184de…`) or "at `74db080`"** (found by
`git grep -n 409184de` and `git grep -n 74db080` over the tracked files, and `grep -rl 409184de`
over `connectome-seed-data/knockout_regrow/`, 2026-09-26 UTC):

| place | what it cites | after the amendment |
|---|---|---|
| this file, header ("What this file is", lines 18–21 of revision 1.1; line 12 of revision 1) | A revision 3.4.1, commit `74db080`, LF `409184de…` | **updated** in the revision that follows the amendment (step 4): the amended hash is cited; `409184de…` stays named as the text of the flyvis-65 verdict |
| this file, S2 (§7.2) | A "pinned by its LF sha256 after the D11 amendment" | **updated**: the arm's script pins the amended hash |
| this file, D11 (§9) | `409184de…` as the value before the amendment | history, unchanged |
| this file, §1.3, §7.2, §11 (clarification C1 and the working rules) and §13 | A §1.4 and `knockout_regrow.py` lines "at `74db080`" | history, unchanged: they name where a wording lived, or the script's lines (A's script is not amended) |
| block B's S2 (`2026-09-25-knockout-regrow-block-b-registration.md` line 576) | A "pinned by its LF sha256 at `74db080`" | **to be updated** by a revision of B (not by this file): pin the amended hash, or read A from git at `74db080`; B is not yet implemented |
| block B's header (same file, line 14) | A revision 3.4.1, commit `74db080` | history: a citation by commit, true as written; B's next revision says which text it quotes |
| the flyvis-65 run manifest: `results/genome/c6/checks/knockout_regrow/summary.json` line 5 (`registration_sha256_lf`), and the private run folder's `synthetic_only.json` (`connectome-seed-data/knockout_regrow/flyvis65_20260925T171656Z_74de0401a21f/`) | `409184de…` | **history, untouched**: the text the run was made under |
| the blind review note (`docs/notes/2026-09-26-knockout-regrow-blind-review.md` line 220) | `409184de…`, as verified against the run's manifest | history, untouched |

No `.py` file in the repository contains either string: A's script reads its registration by path
and records its hash at run time, so a rerun of A's script after the amendment would record the
amended hash (A's script is not rerun by this arm).

**The list at revision 1.2** (the same greps repeated on 2026-09-27 UTC at `e50bf74` plus this
revision's tree; `git grep -c 74db080`: block B 2, the GPU instrument's registration 11, this file
20, the arm's script 3, its tests 1). Places added since revision 1.1, each with what happens to
it; the rows above stand:

| place | what it cites | after the amendment |
|---|---|---|
| the arm's script, `A_REGISTRATION_SHA256_LF_FLYVIS65` (line 77) and its docstring and comments (lines 5–9, 74–75) | `409184de…` as the text of the flyvis-65 verdict; A's script's lines "at `74db080`" | history, unchanged. **Revision 1.1's sentence "No `.py` file … contains either string" no longer holds** since `ee380a1`: this constant contains the full hash, as history |
| the arm's script, `A_REGISTRATION_SHA256_LF_AMENDED` | `None` (placeholder) | **updated** in step 4 to the amended LF sha256 (S2) |
| the arm's tests (line 724 at revision 1.1) | A's script's `rc_patterns` lines at `74db080` | history, unchanged (A's script is not amended) |
| the GPU instrument's registration (`docs/plans/2026-09-26-gpu-instrument-registration.md` lines 30, 132, 287, 303, 547, 911, 918, 957, 1007, 1076, 1083 at `e50bf74`) | A's text (lines 30, 918, 1076: A §7 lines 1473–1476, A §12 lines 2392–2395, A §3.3 and §7) and A's script's lines at `74db080` | history, unchanged: the amendment is appended after A's last line, so every line number above it stays true |
| the arm's two pre-run references and their stdout logs (`synthetic_only.json` manifest `a_registration_sha256_lf`, and the logs' check 1 line), in both the pre-run folders and the copies | `409184de…`, recorded (pre-run mode) | **history, untouched**: the pinned references are never edited; the registered run records the amended hash in its own manifest |

### 9.4 Votes on revision 1.2 (DPC Research chat, 2026-09-26 UTC; as relayed by CC)

| reviewer | time (UTC) | vote |
|---|---|---|
| Ark | 18:10 | yes, with edits |
| Zcode | 18:13 | yes, with edits |

No other vote on revision 1.2 is relayed. Revision 1.3 has not been voted on.

### 9.5 The edits of revision 1.3, who asked, and where each is applied

Items 1–3 are reading rules, **frozen before unsealing**: fixed in this revision, before either
sealed file is opened; no later revision changes them after the seal is broken. None changes a
gate, cut, seed, world or option of D1–D17. Every number was verified on the files named in the
"applied in" column's sections.

| # | edit | asked by | applied in | where this revision differs from CC's brief |
|---|---|---|---|---|
| 1 | U with an empty band: γ\*_P = γ_R = family limit = 0.75, the band empty by construction, the U worlds at or below the limit (L 7: 3 at 0.5, 3 at 0.6, 1 at 0.75; R 5: 2, 1, 2); A's "signature of γ\*_P" does not hold; on the male arm a U is not "at the threshold" | Ark, Zcode | §4.1 (5), §6, §3.3.1 (d) surprise 2; S29; T14 | The brief's wording "U reads 'signal not detected'" is written as **"not detected at the R level: the two legs, or the two D1 candidates, disagree"**: in all 12 U worlds rule #2.1 passes leg S (`n_ge` = 0), 5 have the legs disagreeing and 7 have one D1 candidate reading R, so "signal not detected" would say more than the worlds show. It applies to a threshold U only; the label string stays A's |
| 2 | The instrument is weaker on the male banks, named with its numbers beside any male G: seen at γ 0.6 in 2/5 (A 3/5); the power curves; M0.85 seed 92184 G in both lobes (AUC 0.525/0.542, `p_P` 0.3695/0.2872); seed 92183 W in L (`n_ge` = 1 of 99), R in R | Ark, Zcode | §5 (new paragraph and table), §6; S31; T14 | Verified: in each pair the first number is the worlds whose rule #2.1 `p_P` <= 0.01 ("seen"), the second the worlds labelled R, of 5; A's 3/5 at 0.6 read from A's pinned CSV. The line is printed beside a lobe's G and beside a male G, computed from the registered run's own synthetic step rather than typed as constants |
| 3 | Split: two objects (by reading, D3; by block, §4.3); labels can differ at k = 0; measured now: 5 of 25 dense-grid pairs, none on the axis families; S2 may never fire when labels differ; after unsealing a split is not read as "the blocks differ" unless §4.3's class says so; printed apart | Ark, Zcode (Ark's class 154) | §4.3 ("Two objects"), §3.8, §4.2 table, §6, §3.3.1 (d); S32; T14 | Verified: the five seeds and letters as in the brief (92142 U/R, 92161 U/G, 92164 U/R, 92172 R/U, 92183 W/R), 0 of 20 axis pairs. Added: every one of the 45 world pairs has the same block in both lobes (base labels equal), so all five are splits by reading **at k = 0** |
| 4 | z / z′ order: on A z < z′, on the male banks z > z′ | Ark, Zcode | §3.3.1 (c), after the L = R paragraph | none |
| 5 | `n_deg` inert, signed by its cause | Ark | §3.3.1 (d), new row | `n_deg` = 0 in all 540 rows verified. **The present counts differ from the brief's "19…33":** the shuffled blocks hold 9–37 (L) and 12–36 (R) present cells over all 26,730 shuffle records per lobe (the 17,820 BF `ko` shuffle fits the same); the cause stands (never 0 or 64) |
| 6 | `ko1` wording: "main pass: 46 copied, 174 fitted" (220); the full 179 / 176 include the 5 path-check fits on `world:W:0`, as in A | Zcode | §3.3.1 (a), (c) | Verified on the stores: 51 (L) and 54 (R) base fits at λ = 1, 5 of them `world:W:0`'s (unflagged `ko1`), 46 / 49 flagged; A: 52, 5, 47, 173 + 5 = 178 |
| 7 | D17: the link copy ← original, all five sha256 equal, with the command | Ark, Zcode | §3.3.1 (b), D17 | Recorded in this file only; no file added to either folder (`check_prerun_files` would report it as unlisted and T13 requires none) |
| 8 | The pre-run and the registered run are made by different code: `PRERUN_SCRIPT_SHA256_LF`, both codes recorded and printed; Zcode's `--from-raw` check after the merge registered; run now | Ark, Zcode (the check: Zcode) | S30 (`PRERUN_GIT_HEAD`, `PRERUN_SCRIPT_SHA256_LF`, `prerun_provenance`); §3.3.1 (c) row, (g), (h); §7.5; D15; T14 | Also a `PRERUN_GIT_HEAD` constant, and a mismatch of either stops the run. The check run by this revision re-derived both worlds tables byte for byte (§3.3.1 (h)) |
| 9 | Ark's census numbers (A 12, L 1, R 11 at 2·2^-23): recount at the registered 2^-23 and at 2·2^-23, with the D1 subsets | CC (a caution on Ark's numbers) | §7.1, a chat-only clarification | L 0 / 1 and R 3 / 11 on the `ko`/`ko1` scope (Ark's L 1 and R 11 reproduced at 2·2^-23); D1: L 0 / 1, R 1 / 8, named; A's 12 not reproduced by any of three scopes (6 / 14, 6 / 13, 4 / 8). Decides nothing for the arm |
| 10 | The form of the amendment to A | Ark (§12.x, a pointer line), Zcode (a new §13); decided by CC | §9.3 item 1, Appendix A | none: "## 13. Amendment 1" kept; Ark's pointer line is the first line inside §13; Ark's alternative recorded |
| 11 | The votes and this table | CC's brief | §9.4, §9.5, header, §12 | none |

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
- **Revision 1.1 additions.** The reviewers' messages are known from CC's brief, not read in the
  chat. The GPU economics of §7.1 (4,870 s, 7,846 s, "not ported") are relayed, not recomputed.
  The false "R in both" rate of §4.2 is bounded by argument, not measured. The expectation that
  S2b is the modal split class (§4.3) rests on the relayed description of §1.5, which is not
  verified. The rate of `ko1` fits that are copied rather than fitted on the male worlds is
  unknown until the pre-run (§3.6).
- **Revision 1.2: what the pre-run settled, and what stays open.** Settled by the pre-run
  (§3.3.1): the existence path of every predictor runs (28,665 fits per lobe, no error; the first
  item above); the fit rate on the placed grid (3.56 and 3.61 fits per second on the world fits;
  the second item); the male worlds' behaviour (R reads R, Nf and No read G, W reads W in both
  lobes; the limits are γ\*_P = γ_R = family limit = 0.75; the third item, with the surprises of
  §3.3.1 (d)); the `ko1` rate (46 and 49 of 225 copied). **Still open:** that the registered
  run's refit reproduces the references (its gate; the `--from-raw` check of §3.3.1 (f) shows
  only that each reference is consistent with its own store); the joint R on the real blocks (the
  worlds' pair count of §3.3.1 (d) is on 32/32 boards); the V8 result on lobe R and everything
  about V8 beyond CC's relay (§7.1); every other item above.
- **Revision 1.3.** The reviews of revision 1.2 are known from CC's brief, not read in the chat.
  Not reproduced: the "19…33" present counts relayed with edit 5 (the stores give 9–37 and
  12–36; §9.5) and Ark's A count of 12 at-risk fits (§7.1); where those numbers came from is not
  known here. The `--from-raw` check of §3.3.1 (h) was run on the uncommitted tree that became
  this revision's commit; it is repeated at the merged head before the registered run. The GPU
  instrument's tests were not run by this revision (its `male_arm.py` imports the arm's script,
  whose changes S29–S32 are additions that no function of `male_arm.py` calls; checked with the
  code graph and grep).

## 11. Error ledger (working rules inherited from A §12)

**Working rules (A §12, revision 3.4, item 4).** A claim that an object is present or absent
requires a census of all the names the artefact declares for it. A claim about a column or a field
requires a census of that column. A partial or null result is a statement about the pattern and
the scope searched, not about the object. **A cited line carries its revision explicitly**: in this
file, `knockout_regrow.py` lines are of `74db080`, `harness.py` of `1789aeb` (the pinned file),
`flywire_bf_p3.py` of `c55d3e3`, rule #2.1's `fit.py` of `6ffce66`, `BUILD.md` and
`bank.meta.json` of `5860619`.

**Ledger** (six fields, A §12's form; the rows found while drafting). **Revision 1.1:** revision
1's row M(1) is not a wrong wording, so it does not fit the ledger's definition (a wording that
was wrong, with its refutation); it moves to the clarifications below as C1 (the reviewers: "not
an error and not a narrowing: a different object").

| item | was | correct | where the wrong wording lived | what refuted it | caught by |
|---|---|---|---|---|---|
| M(2) | `restrict_to_30_grid` at `flywire_bf_p3.py:74-76` (and ":74" in the drafting brief) | the function is lines 73–75 (definition 73, docstring 74, the assignment of `H.ALL_CELLS` 75) at `c55d3e3`, the file's last change, which precedes the commit (`d6e3759`) at which the builder read it | builder §2, §7, §12, §13.2 row 1 (`:74-76`) at `476cf9b`: **still there, in four places** (revision 1.1, Zcode; `git grep -n "74-76"`): lines 214 (§2), 705 (§7), 976 (§12) and 1056 (§13.2, edit 1). Not edited here; the builder's next revision corrects them | `flywire_bf_p3.py` at `c55d3e3`, lines 73–75 | this draft |

**Clarifications (not errors; revision 1.1).**

| item | clarification |
|---|---|
| C1 (revision 1's ledger row M(1)) | Three objects, none a correction of another. **A's row:** "male CNS v1.0: 64 / 64 at every pair threshold tried (Zcode, preliminary graph)" (A §1.4 at `74db080`; `knockout_regrow.py:205-208`; `knockout_regrow/RESULT.md` line 56; builder §0), which the reviewers describe as 64 / 64 at every flyvis-65 pair threshold tried on the 65 grid; the thresholds are in no file. **This arm:** 64 / 64 at `c*` in each lobe (`BUILD.md` lines 189–190). **The (b′) diagnostic, at another cut and on this bank:** 56 / 64 in lobe L at `w_min` 2 and 3 (`BUILD.md` lines 210, 227). Revision 1 called A's row a wording that "reads as general"; it is a statement about other thresholds, and it stays in A as written |
| C2 (revision 1.3, Zcode) | Revision 1.2's §3.3.1 (a) gave the `ko1` split as "46 records copied from the `ko` fit, 174 fitted" and row (c) as "46 copied, 179 fitted". Both were true, at two scopes: the main pass (220 records) and the store (225, with the 5 path-check fits of `world:W:0`, fitted and unflagged). Not a wrong number, so not a ledger row; (a) now names both scopes |

**Registered expectations and what the build showed** (not wrong wordings; recorded so that no one
reads them as met):

| expectation (where registered) | what the build showed | source |
|---|---|---|
| "under the shared cut `c*` the left bank is expected to be sparser in R1's row and column" (builder §4, §12, revision 2.1) | not borne out: 3 / 1 in both lobes, the same cells | `BUILD.md` line 185; §1.4 |
| "`c*_L < c*_R` among the §5.4 diagnostics would read as a consequence of this asymmetry" (builder §4, §12) | `c*_L` = 2.69453 < `c*_R` = 3.39337 did occur, but R1's row and column are equal between the lobes, so the gap is not carried by R1–R6; it is lobe-wide (33 R-only against 3 L-only outside cells at `c*`) | `BUILD.md` lines 195, 198; §1.4 |
| "the first question put to the build: how much larger the R1-row asymmetry is than 1 : 2.04 in bodies" (builder §4) | answered: at `c*` there is no R1-row asymmetry in presence (1 : 1 against 1 : 2.04 in bodies) | `BUILD.md` line 185 |
| "On a denser bank the M worlds may be seen at lower γ" (§3.6, revision 1) | not borne out: γ\*_P = 0.75 in both lobes against A's 0.6 (seen 2 of 5 at γ = 0.6 in each lobe, A 3 of 5); within one grid step, the binomial note's resolution (revision 1.2) | §3.3.1 (d) |
| "The expectations of A §3.6 (R reads R, Nf reads G, No reads G, W reads W) carry over" (§3.6) | met in both lobes: every stop row passed, labels as A's in the four stop families | §3.3.1 (d) |
| A's U reading, written on A's pre-run: U worlds in the band, at γ\*_P (A §4, revisions 3.1, 3.2; quoted by this arm as A's literals, §4.1) | on the male worlds the band is empty and the U worlds lie at γ 0.5–0.75, below or at the limits (L 7, R 5) | §3.3.1 (d) **Revision 1.3:** a reading rule is frozen from it, §4.1 (5) |
| "At γ = 0 a world's outside density is then near the lobe's" (§3.6) | met: Nf worlds 0.1724 (L; lobe 0.1675) and 0.1812 (R; lobe 0.1776) | §3.3.1 (d) |
| cost: about 2 h 11 min per lobe per pass (§3.6) | 2 h 13 min (L) and 2 h 11 min (R) | §3.3.1 (a) |

**The seal record:** intact at revision 1, at revision 1.1, at revision 1.2 and at revision 1.3 (header). A break
before review is recorded here, and S26 carries it to the verdict lines.

## 12. Changelog

**Revision 1 (2026-09-26 UTC): first draft, CC subagent.** Built on A revision 3.4.1, the builder
revision 2.1 and its build (`5860619`), and B revision 1.1 as the template. Computed for this
draft, from the outside files only (after checking they hold no block row): the per-lobe endpoint
tables, inferability, mirrors, R1's and CT1(M10)'s rows, the lobe agreement (493 / 3 / 33 with the
36 cells and their `x` relative to `c*`), the fold composition on the placed grid; from arithmetic
only: the null standard deviations, the binomial tails and `k*` = 4. No sealed file opened; nothing
fitted. Proposals D1–D16 open.

**Revision 1.1 (2026-09-26 UTC): the reviewers' edits, CC subagent.** Votes of Johnny (09:14),
Ark (09:18) and Zcode (09:32 UTC), all "yes, with edits" (§9.1); the edits and who asked are in
§9.2. Reading rules frozen before unsealing: the male R as a conjunction (§4.2, §5, §6); split class
S2 split into S2a and S2b by `x` (§4.3); leg S decided by the count, `p_S` printed with four
decimals and a mark when `n_deg` >= 1 (§3.2, §4.1, S28). Also: D7 (comparability of `p_P` given
up), D8 (the asymmetry with D9), D11 and §9.3 (the amendment's content and the list of places that
cite A by hash or commit), D12 and S2 (`quote_row` reads the amended A), D13 and §7.1 (option (iii),
the separate track, the economics), §1.5 and §3.2 (a possibly sparse block), §3.3 (equal
`smallest_passing_auc` in the worlds only), §3.6, §7.5, D6 (the `ko1` fits; about 8 h 52 min in
all), §3.7 (the grep count), §7.5 (what the per-shuffle files carry), §11 (M(1) moved to C1; M(2)'s
four builder lines). Checked for this revision: `n_deg` in A's pre-run and run CSVs; the script
lines cited; the greps of §3.7, §9.3 and §11. No sealed file opened; nothing fitted; A, the
builder registration and B not edited.

**Revision 1.2 (2026-09-27 UTC): the values read from the pinned references (D15 step 3), CC
subagent.** New: §3.3.1 (the pre-run as it ran, where the references live, the registered values
with their sources, the pre-run values against A's, the surprises, whether the pre-run stops the
registered run, the `--from-raw` check, what the script does now); D17 (where the references
live: byte copies in the proposed folders); §7.1 (a chat-only note on V8 lobe L); §7.3 (T13);
§7.5 (the pre-run as run); §9.3 (the list of citers brought to revision 1.2); §10 (what the
pre-run settled); §11 (the expectations met or not, the seal record); Appendix A (the draft of
the amendment to A). Done outside this file: the two reference folders copied (§3.3.1 (b)); in
the script, `PRERUN_SHA256` and `PRERUN_WORLDS_CSV_SHA256` set for both lobes, `REGISTRATION_REVISION`
= "1.2", `A_REGISTRATION_SHA256_LF_AMENDED` left `None`; in the tests, T13 added and T3's
`--synthetic-only` test held in pre-run mode; 39 tests pass (38 of revision 1.1 and T13). Run by
this revision: two `--from-raw` passes (about 9 s each, 5 fits each, §3.3.1 (f)) and the tests.
No gate, cut, reading rule, seed, world or option of D1–D16 changes. No sealed file opened; A, the
builder registration and B not edited.

**Revision 1.3 (2026-09-27 UTC): the reviewers' edits on revision 1.2, CC subagent.** Votes of Ark
(18:10) and Zcode (18:13 UTC), "yes, with edits" (§9.4); the edits, who asked and where each is
applied in §9.5. Reading rules frozen before unsealing: a threshold U on the male banks, with an
empty band, reads "not detected at the R level", with no position on a threshold (§4.1 (5), §6;
S29); the instrument's weakness named with its numbers beside every male G (§5, §6; S31); the two
objects called "split", printed apart, one never read as the other (§4.3, §3.8, §4.2, §6; S32).
Also: §3.3.1 (a) the `ko1` scopes, (b) the link copy ← original with its command, (c) the z / z′
order and the code that made the references, (d) the meaning of the curve's pairs, `n_deg` with
its cause and the world pairs at k = 0, (g) and (h) the pre-run's and this run's code (S30) and
the `--from-raw` check after the merge, registered and run; §7.1 a chat-only clarification of the
GPU census counts; §7.2 S29–S32; §7.3 T14; §7.5 the check's commands; D12, D15, D17; §9.3 item 1
and Appendix A (the amendment's form decided; Ark's pointer line inside §13); §10, §11 (C2, the U
expectation row, the seal record). In the script: `REGISTRATION_REVISION` = "1.3", S29–S32; in
the tests: T14 (7 tests) and two assertions in T3's real-arm flow; 46 tests pass. Run by this
revision: the two `--from-raw` passes (§3.3.1 (h)), the census and the checks of §9.5 by scratch
scripts (not committed), the tests. No gate, cut, seed, world or option of D1–D17 changes. No
sealed file opened; A, the builder registration and B not edited; no file added to or changed in
the reference or pre-run folders.

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
- Revision 1.1: A's pinned pre-run `connectome-seed-data/knockout_regrow/synthetic_rev3_prerun/synthetic_worlds.csv`
  and the flyvis-65 run's committed `synthetic_worlds.csv` and `per_shuffle.csv` (the `n_deg` and
  `degenerate` columns only); CC's brief relaying the three reviews and Mike's 09:13 UTC word.
- Revision 1.2: the two pre-run folders `connectome-seed-data/knockout_regrow/malecns_prerun_L_20260926T131249Z/`
  and `…_R_…/`, their stdout logs, and their copies `synthetic_malecns_L_prerun/` and
  `synthetic_malecns_R_prerun/`; A's pinned pre-run `synthetic_rev3_prerun/` (`SYNTHETIC.md`,
  `synthetic_only.json`); `docs/plans/2026-09-26-gpu-instrument-registration.md` (header, at
  `e50bf74`); `results/genome/c6/gpu_instrument/instrument.py` and `validation.py` (how V8 reads
  the male stores); CC's brief (the pre-run's exit codes, the V8 lobe L relay).
- Revision 1.3: both references' `synthetic_worlds.csv`, `synthetic_only.json` and
  `raw_fits.json.gz`, and the five files of each pre-run folder (sha256 only); A's pinned
  `synthetic_rev3_prerun/synthetic_worlds.csv` and `raw_fits.json.gz`;
  `results/genome/c6/gpu_instrument/census.py` (the census definition, used as is) and
  `validation.py` (V8's composition); A §8 at `74db080` (lines 1725–1726, 1749–1750); CC's brief
  (the two reviews of revision 1.2 and CC's decision on the amendment's form).
- `idea.md` (the project goal; context).

## Appendix A. Draft of the amendment to A (revisions 1.2, 1.3; to be made in D15 step 4)

The text below is a **draft** for the reviewers. It is appended, as one new section, after A's
last line (`- \`REGISTRATION_REVISION\` = "3.4.1". Header line, §10, §12.`, line 2,495 at
`74db080`), after one blank line; nothing above it changes, so every line number of A cited
anywhere stays true, and `quote_row` still returns A §4's rows (no line of the amendment starts
with "| **R: regrows**", "| **W: rule weaker", "| **U: on the detection threshold" or "| **G: not
detected at the R level above γ_R**"; S2, D12). A's header and `REGISTRATION_REVISION` line are not
edited (A §8: "nothing else in it changes"; §9.3 item 5). After it is committed, step 4 also sets
`A_REGISTRATION_SHA256_LF_AMENDED` in the arm's script to A's new LF sha256, updates this file's
header citation (§9.3 table, first two rows), and records the commit here.

~~~markdown
## 13. Amendment 1 (append-only): the male CNS arm's bank pins and seeds

**Pointer.** This section amends §8 of revision 3.4.1 at two addresses: the promise to pin the
built bank (§8, lines 1725–1726) and the sentence on seeds (§8, lines 1749–1750, bullet "The same
block by name"); no line above this section is changed.

**What this section is.** The amendment that §8 promises ("This registration will be amended,
before that arm runs, to pin the built bank's sha256, and nothing else in it changes"; §8,
lines 1725–1726) and that the builder's registration names
(`docs/plans/2026-09-25-male-cns-bank-builder-registration.md`, revision 2.1, §10.1 and §10.5
step 4). Its content was fixed by the male CNS arm's registration,
`docs/plans/2026-09-26-knockout-regrow-male-cns-arm-registration.md`, §9.3 (revision 1.1, D11
(i)), and reviewed with it. It is appended after this file's last line; no line above it is
changed.

**1. The four bank pins** (sha256 over raw bytes; the build folder
`connectome-seed-data/Janelia/derived/male_cns_v1_20260926T084555Z_e0a3cd744c39/`, outside the
repository, built at head `e0a3cd7`, committed in `5860619` with
`results/genome/c6/checks/male_cns_bank/BUILD.md` and `bank.meta.json`):

| file | sha256 |
|---|---|
| `male_cns_L_outside.csv` | `16c5752a241b2e61d4caeaa23bc4b9b9385011c2bfa6a2db504195199bfe9fb0` |
| `male_cns_R_outside.csv` | `27a9079b656d1aeb1943702e173d2fa3009f7d8257a78f9e8b5c0f3712b4cf36` |
| `male_cns_L_blockA.sealed.csv` | `eb611f6805484c4f54c22f072a2ca74219a97b3265c6bfb8a4639e45108e8b8e` |
| `male_cns_R_blockA.sealed.csv` | `c53a44670b784f7af1c8c3973ba440961b24bff08b039a0cf4c73bd32414da84` |

The two sealed files' values are quoted from `bank.meta.json` and the build's `SHA256SUMS.txt`;
they are checked against these pins before they are opened, in the male arm's registered run
only. The male arm pins the same four values, and two more files, in its §1.1 and its script.

**2. The seeds, cancelled for the male arm.** §8's sentence "The same legs, cuts, seeds and
branch rule apply" (lines 1749–1750 at `74db080`, bullet "The same block by name") no longer
applies to seeds for the male CNS arm. Its seeds are those of
`docs/plans/2026-09-26-knockout-regrow-male-cns-arm-registration.md` §3.7 (92000–92999). Legs,
cuts and the branch rule apply as written.

**3. The text of the flyvis-65 verdict.** The flyvis-65 verdict (commit `1ed55ec`) was made under
revision 3.4.1, LF sha256 `409184dead0a8f9b971bd4b480043725d4a0d1a3c53c20c35734a944a63facd6`.
That text is recovered with
`git show 74db080:docs/plans/2026-09-24-knockout-regrow-registration.md`.

**4. Nothing else changes** (§8). Every place that cites this file by its LF hash or "at
`74db080`" is listed, with what happens to it, in the male arm's registration §9.3.
~~~

**Notes for the reviewers on the draft.**

- **Its heading number (revision 1.3: decided by CC).** A's last section is "## 12. Changelog";
  the draft names itself "## 13." **Kept: a new section, "## 13. Amendment 1"** (Zcode's
  position): A's §12 holds the changelog and the error ledger, whose rows have their own
  six-field format and should not carry a normative change; a new section keeps A's §12 as it was
  at the verdict and carries both addresses (§8 lines 1725–1726 and 1749–1750) and the pins.
  **Ark's alternative, a subsection §12.x, is recorded and not taken**, for that reason.
- **A's status header is not touched,** so after the amendment A's header still reads "revision
  3.4.1" while its text has an appended section. **Revision 1.3:** the single pointer line Ark
  asked for is placed as **the first line inside §13 itself** ("**Pointer.** This section amends
  §8 …"), not in A's header, so no line above the amendment changes and §9.3 item 5 ("nothing
  else") holds. It starts with none of `quote_row`'s four keys.
- **Its LF sha256 cannot be computed before the text is final;** step 4 computes it after the
  commit and sets it in the script (the registered run refuses until then, §3.3.1 (g)).
- **Block B** pins A "by its LF sha256 at `74db080`" (B's S2, line 576); the amendment changes
  that hash, so B's next revision chooses the amended hash or `git show 74db080:…` (§9.3 table).
