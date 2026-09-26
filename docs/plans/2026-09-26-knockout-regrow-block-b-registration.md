---
**Status: DRAFT, not reviewed, not committed.** Drafted 2026-09-26 UTC by a CC subagent on Mike's
word (DPC Research chat, 2026-09-25 20:02 UTC, as relayed by CC; the chat is not in the
repository): a second block on flyvis-65. Nothing was fitted, regrown or scored for block B. No
cell of block B was read from the bank (§1.5, read declaration).

**What this file is.** A delta on block A's registration,
[`2026-09-24-knockout-regrow-registration.md`](2026-09-24-knockout-regrow-registration.md),
**revision 3.4.1** (commit `74db080`; the registered run of block A used it at head `74de040`;
cited below as "A §n"). **Everything of revision 3.4.1 applies to block B unchanged unless a
section below says otherwise.** Every gate and every reading rule of revision 3.4.1 is kept. What
changes is the block, what follows from its shape, the synthetic worlds built on it, the values
registered from those worlds, the seeds, and the script constants.

**Order of work proposed (D10).** (1) This draft is reviewed. (2) The block-B script is written
and committed with this draft marked as a draft. (3) The `--synthetic-only` pre-run of block B is
made from that committed head, on Mike's word, and becomes block B's pinned reference. (4) A
revision of this file registers the values read from that reference (§3.3) and is reviewed.
(5) The registered run.

**Order of drafting, recorded.** §1.2 (the choice rule, the options and the chosen block) was
written into this file before any table of §1.4 was computed. §1.4's tables were then computed by
one scratch script from names and from presence outside block B only (§1.4, §1.5). After the
tables, §1.2 was edited for wording, for factual qualifications (B-full's targets on the 65
grid; candidate C's size there, not counted), and to make its tie-break explicit (the
larger of the two options that pass, which was already the recommendation, and the admission of
a restriction of a candidate by its own biology text, which is what B-motion already was). The
chosen block did not change.
---

# Registration: knock out and regrow, block B on flyvis-65 (a delta on block A's registration)

## 0. Question, name, and what it is not (delta on A §0)

**Name.** *Knock out and regrow, block B: does a learnable rule that reads no type names regrow
the lamina's input to the eight motion-pathway inputs, which it was not shown?*

**Question.** A §0 with the block replaced: remove every cell of block B (L1–L5 × the eight
medulla inputs of block A's pathway, 40 cells, §1.2), train on everything else, and ask whether
the predictions for the 40 cells separate the present cells from the absent ones better than the
same rule on the same knockout in the 99 degree-preserving shuffles (leg S) and better than the
block's labels permuted within the block (leg P). The standard is ADR-005 agreed point 6, as for
block A.

**What does not transfer from A §0, and why.** Block A was known before its registration to be a
perfect board (16 + 16 present, no cross cells; counted three times in review). Three statements
of A §0 rest on that board, and none of them can be made for block B before data:

- **"No additive score can find the board"** (A §0, §2.3). It needs every row and every column of
  the block to hold the same share of present cells. A 5 × 8 block cannot: a row has 8 cells and
  a column 5, so a common share f needs 8f and 5f both integers, which only f = 0 or 1 allow
  (algebra, this draft). **So N1's additive score can order part of block B,** and the N1 leg,
  which decides nothing in A either, is no longer "uninformative in both directions" by algebra
  (§2.3 below).
- **"Leakage through degrees cannot carry the board"** (A §0). It rested on 4 of 8 in every row
  and column. For block B it is not known before data, and by the line above it cannot hold
  exactly. Leg S subtracts N1's AUC on every bank (A §3.2), so R still needs structure beyond the
  degrees; leg P does not subtract it (§4 below, D8).
- **"The board is exactly rank 1"** (A §2.4). Block B's pattern is not known, and the note's own
  biology (L3 → Mi9, an ON input, and L3 → Tm9, an OFF input) is not a ±1 outer product with the
  targets' ON/OFF split. So the G gate `ceiling_block >= 0.90` is not "nearly automatic" on block
  B, and a `ceiling_block` below it can be a rank limit of the rule, not only a failed fit (§2.4,
  D9).

**What the bank is.** Unchanged (A §0): flyvis-65, the generation-zero bank, a synthetic template
of at least two flies, not an animal. The column-test anchor is unchanged.

**What it is not.** Unchanged (A §0), and in addition: **it is not a second try at block A.**
Block A's verdict G stands as registered. Block B is read on its own (§5, D11).

## 1. The bank, the block, and exactly what is removed

### 1.1 Files and pins

Unchanged: the eight pins of A §1.1 (`offsets.csv`, `types.csv`, `folds.csv`, `harness.py`, rule
#2.1's `fit.py` and `decode.py`, `bf_decode.py`, `n1_decode.py`). The scratch script of §1.4 read
`offsets.csv`, `types.csv` and `harness.py` at the pinned hashes (`8c45e850…`, `237a195a…`,
`6fc80952…`; LF sha256, 2026-09-26). The block-B script records this file's own LF sha256 in its
manifest, as A's does (§7).

### 1.2 Block B: the choice rule, written before any table was computed

**The criteria (block A's, unchanged).** Block A was kept for four reasons (candidates note §5)
under two conditions (candidates note §1, "What a block is"; ADR-005 agreed point 6):

- **K1, structure, not only density:** the block holds present and absent cells, and the absent
  ones are biologically meaningful, so a rule is scored on discrimination and the permuted-block
  null destroys exactly the structure claimed.
- **K2, no copy of itself:** symmetric siblings (directions, ON/OFF halves) are removed together,
  so no sibling left in training can regrow the block by copying.
- **K3, endpoints stay visible:** no type loses (almost) all of its row or column. Otherwise N1
  and BF_r cannot place it, and "no information" and "no grammar" are read from the same failure.
- **K4, documented and large enough:** described in several EM volumes, with enough present cells
  to be measured.
- **Conditions:** a block is a set of cells fixed by a rule on type names, chosen on biological
  grounds before its content is read; all four fields of every cell in it are removed; the rule
  under test reads no type names.

**The rule for B, written before data.** Block B is taken from the candidates note's list (§2:
A, B, C), or from a restriction of one of them by a name rule taken from that candidate's own
biology text, and judged by K1–K4 on the name rule alone. No presence, weight, offset or sign of
any cell of any candidate block was read to choose it. Of the options that pass K1–K4 by name,
the largest is taken (K4). Once chosen, the §1.4-type tables (what each
endpoint keeps, inferability, mirrors) are computed from presence **outside** block B, as §1.4
of block A's registration did; they do not reopen the choice, and a failure of K3 there goes to
review (D1), not to an automatic switch.

**The options, on the 65-type grid.** The candidates note counted its candidates on a 30-type grid
(note §1). Its name rules are translated to the 65 types of `types.csv`: the photoreceptors are
R1–R8 (the eight `input`/`retina` types), the lamina monopolar cells L1–L5.

| option | name rule | cells | K1 structure | K2 copy | K3 endpoints visible (by the rule's shape) | K4 | what choosing it changes |
|---|---|---|---|---|---|---|---|
| **B-full** (candidate B as written) | src ∈ {L1–L5} × tar ∉ {L1–L5, R1–R8} | 5 × 52 = 260 | yes (note §2B) | yes | **no**: the L rows keep only L→L and L→R cells; the note's own risk ("almost a whole-row knockout ... 'no grammar' and 'no information' would be read from the same failure") | yes | a block where a G cannot be told from "no information"; its targets also take in 29 types that the 30-type rule never had to consider (52 against 23; Lawf1, Lawf2 and Am among them), so the note's rule does not fix it on the 65 grid |
| **B-motion** (candidate B restricted; recommended) | src ∈ {L1, L2, L3, L4, L5} × tar ∈ {Mi1, Tm3, Mi4, Mi9, Tm1, Tm2, Tm4, Tm9} (block A's eight sources) | 5 × 8 = 40 | yes: "L1 feeds the ON side (Mi1, Tm3), L2 the OFF side (Tm1, Tm2, Tm4), and L3 feeds Mi9, Tm9 and Tm20" (note §2B) | yes: both polarities and all five L types are removed together | **yes by shape**: each L row keeps its cells into the other 44 non-L, non-R types; each target column keeps its cells from the other 60 types | same sources as candidate B (Meinertzhagen & O'Neil 1991; Takemura et al. 2013, 2015) | the stage upstream of block A: the lamina's input to the eight motion inputs. **It is not one of the note's three rules verbatim**: it restricts candidate B's targets to the targets named in candidate B's own biology paragraph and in block A's source list (D1) |
| **B-L123** | src ∈ {L1, L2, L3} × the same eight | 3 × 8 = 24 | yes | yes | yes by shape | smaller: only the L types whose targets the note states | fewer cells, lower power (a leg-P pass needs a higher AUC on 24 cells than on 40) |
| **C** (candidate C as written) | src ∈ {R7, R8} × tar ∉ {R1–R8} | 2 × 57 = 114 | partly (note §2C) | yes | **no**: the R7 and R8 rows keep only cells into R1–R8 | **no on the 30 grid**: "too small and too noisy" (4 FlyWire-30 pairs, 7 flyvis-30 pairs; note §2). On the 65 grid its targets include Tm5a, Tm5b, Tm5c and Tm5Y (flyvis's Tm5 types; the note names Tm5 as an R7 partner "not among the 30"; the identification is this draft's); its size there was not counted | a near whole-row block, as B-full |
| **defer** | a new candidates note on the 65-type grid | — | — | — | — | — | a new selection round, reviewed before any registration; costs a session |

**Chosen (recommendation; D1): B-motion**, 40 cells, `{L1–L5} × {Mi1, Tm3, Mi4, Mi9, Tm1, Tm2,
Tm4, Tm9}`. Two options pass K1–K4 by their name rule, B-motion and B-L123, and B-motion is the
larger (40 cells against 24). It keeps candidate B's
biology and sources and removes candidate B's own named risk (K3) by restricting the targets to
the ones that biology names. It is the input stage of block A's pathway, so it asks the same
question one synapse upstream.

**What the choice does not rest on.** Block A's run printed rule #2.1's `ceiling_full` = 0.8442
("orthogonal", as a description only; `RESULT.md` line 5). **That value is not a reason for
choosing block B, and this test does not try to find a block with a higher `ceiling_full`.** The
mechanism label of G is a description from which no decision is read (block A's registration §2.4,
decision (c)), and a block chosen to move it would be selection after the data (lesson a). Nor
does the choice rest on block A's verdict G: B-motion restricts candidate B, which was written
(note committed `10b704e`) before block A's registration, and it is judged by the criteria written
then. It is still chosen after block A's result was known; §1.5 says what that does and does not
compromise.

**The answer key (used only to score and to print strata, never to train).** From the note §2B:
L1 → Mi1, Tm3 (ON); L2 → Tm1, Tm2, Tm4 (OFF); L3 → Mi9, Tm9. The targets' ON/OFF split is block
A's (§1.2 there): ON = {Mi1, Tm3, Mi4, Mi9}, OFF = {Tm1, Tm2, Tm4, Tm9}. **Not stated in any
file opened for this draft:** the targets of L4 and L5 inside the block, and whether L1 → OFF and
L2 → ON are absent (the note's "L1 feeds the ON side, L2 the OFF side" implies it; the implication
is this draft's). The key is textbook, so risk 3 of the note (the author knows the answer) applies
as it did to block A.

### 1.3 What is removed, entirely (delta on A §1.3)

**Removed from training:** for each of the 40 cells, every row of `offsets.csv` with that
(src, tar), whatever its provenance (`in_json`, `hull_filled`, `dropped`), with all its fields,
and the cell's existence label, present or absent. The training mask is `~BLOCK_B`. **Training
cells: 4,225 − 40 = 4,185.** The training present count is **not** computed before data: the
bank's 604 present cells are public (A §1.3), so 604 minus that count is block B's present count
(D3). The script prints it at run start.

**Not removed (stated, so that a reader knows what the rule still sees):**

- **Block A's 64 cells.** They were the knockout in A and are ordinary training cells here, with
  their board (ON inputs → T4, OFF inputs → T5). That board states the eight targets' ON/OFF
  polarity **in their source role**. Block B asks about them **in their target role**. None of
  the registered predictors ties a type's source factor to its target factor (A §1.4: BF_r's `U`
  and `V` are separate; rule #2.1 has one `(u, v)` pair and the group-level `W`), so block A's
  board is not a direct channel into block B. A rule that tied the two roles would have one.
- The 13 types and every other cell of their rows and columns: the L rows' outputs to the other
  44 non-L, non-R types, L → L and L → R cells, the L columns (their inputs, including R1–R6),
  and the eight targets' other inputs, among them the R8 inputs of Mi1, Mi4 and Mi9 that the
  note names (note §2C).
- The **mirror cells** (§1.4): the transposes, target → source, which lie outside the block.
- `view.type_fields` for all 65 types, and the registry's birth ids (read by no predictor).

**Existence under C6**, unchanged (A §1.3). Lawf1 → Lawf1, the one all-`dropped` pair, is
outside block B (checked by name).

**The rule reads no type names; the field channel on block B.** The five sources share one field
group: `stride` (1, 1), role `intermediate`, layout `intermediate` (`types.csv`; the scratch
script's `type_fields` gives [1, 1, 1, 0] for each). So rule #2.1's field term `W[G(s), G(t)]`
is a function of the target alone on block B, that is, an additive target term. The targets split
into `intermediate` {Mi1, Mi4, Mi9} and `output` {Tm1, Tm2, Tm3, Tm4, Tm9} (A §1.3), which agrees
with ON/OFF on 7 of 8. **An additive term cannot carry an interaction, but on block B an additive
term can order part of the block** (§0), so the field channel is one more additive channel beside
N1's, not a zero one as on block A.

### 1.4 Printed before data: inferability, mirrors, what each endpoint keeps (computed now)

Computed on 2026-09-26 by one scratch script (outside the repository, in the drafting agent's
session scratchpad, not committed), after §1.2 was written: names from `types.csv`, presence as
`harness.REAL.exists & ~BLOCK_B`, one expression, so no cell of block B was read. Presence means
C6 existence, as in A §1.3. Self-loops are counted, as in A. **Not computed:** anything inside
the block, and the training present total (§1.3).

- **Johnny's inferability (a source with ≥ 2 training targets and a target with ≥ 2 training
  sources): 40 of 40 block cells are inferable.** Every source keeps at least 4 training targets;
  every target keeps at least 9 training sources.
- **What each endpoint keeps: not printed here (D2).** For the eight targets, A §1.4 printed their
  training sources outside block A, which is their full in-degree, since block A does not touch
  their columns. The same count outside block B is that in-degree minus their L inputs inside
  block B. **The difference of the two published tables would be block B's column counts,** a
  count of block B's content. The table is therefore registered by its hash: the UTF-8 bytes of
  `json.dumps({"endpoints": keep}, sort_keys=True, separators=(",", ":"))`, where `keep` maps each
  source to [training targets, training sources] and each target to [training sources, training
  targets], have sha256
  **`aa0920288e6d38230c6a275c1690614120fdaf9104476264d42208ecf04f7705`**. The script recomputes the
  table, prints it at run start (before any fit on the real bank) and stops on a different hash
  ("PRE-DATA TABLES DIFFER"). A consistency check of the scratch script against A's published
  table, on block A's cells only: each of the eight targets' training-target counts equals A
  §1.4's count plus 4, block A's four present cells per source back in training.
- **Mirror cells on flyvis-65: 9 are present**, of 40 (block A: 5 of 64): (Mi1, L1), (Mi1, L5),
  (Mi4, L2), (Mi9, L3), (Tm1, L2), (Tm1, L5), (Tm2, L2), (Tm2, L5), (Tm3, L1). The run prints the
  predictions for their 9 block partners on a line of their own, and the AUC on the other 31
  cells beside the AUC on all 40 (A §3.5). Five of the nine partners are cells that the note's key
  names as present (L1 → Mi1, L1 → Tm3, L2 → Tm1, L2 → Tm2, L3 → Mi9); whether they are present
  in the bank was not read. As in A, no registered predictor ties a type's source factor to its
  target factor, so a mirror is not a direct channel; a rule that tied them could read much of
  the key from the mirrors.
- **The other banks' rows of A §1.4** (FlyWire-30 14 / 64; male CNS 64 / 64) are block A's and are
  not printed for block B. They were not computed for block B.

### 1.5 Prior exposure of block B's cells, and the read declaration

The request calls this "contamination". In this repository that word is ADR-003's term (a value
seen by a blind author; GLOSSARY §8), so this file says **prior exposure**.

**What happened to block B's 40 cells before this file.**

1. **They were training cells of every block-A fit.** Block A's knockout mask was `~BLOCK_A`
   (A §1.3), which holds all 40: the knockout fits, the 99 shuffled banks (in which they were
   shuffled) and the fixed-λ fits of block A's real arm, and the one real-bank fit of A's
   synthetic step (N1's degree terms, item 2). They were also in the full bank of the real arm's
   `ceiling_full` fits and permuted-block ceilings; `ceiling_block` trained on block A's 64 cells
   only.
2. **They entered block A's synthetic worlds through the degree terms.** A's worlds use N1's
   `(c, a, b)` fitted on the real knockout view of block A (A §3.6; script `degree_terms`), which
   holds block B's cells. The content (offsets, sign) of block B's present cells was also in A's
   content pool (`NONBLOCK_CELLS`, the present cells outside block A) and could be copied into
   random outside cells of A's worlds. Existence at block B's positions in A's worlds was drawn
   from the world's logit, not copied.
3. **They were never scored as a knockout target.** Every stored fit of block A holds `p_exist` on
   block A's 64 positions only (script `_w_group`: `decode(data, BLOCK_CELLS)`,
   `score(dec, bank, BLOCK_CELLS)`; A §7, "raw_fits.json.gz … on the 64 block positions").
4. **They were scored inside aggregates.** C6's held-out unit is the cell and its 10 folds cover
   all 4,225 cells (GLOSSARY §5, "held-out unit", "fold"), so block B's cells, like block A's, were
   held out once in every C6 run of rule #2.1 and BF_r and entered fold-level scores. Block A's
   check 8 (BF_1's full-bank C6 existence margin over N1, through the harness's `cv` folds) scored
   them the same way. Whether any C6 diagnostic printed per-cell predictions for L → medulla cells
   was not searched (§11).
5. **Their content is public.** `offsets.csv` is committed. The candidates note printed counts for
   candidate B on the 30-type grid (28 FlyWire-30 pairs and 32 flyvis-30 pairs in its 115 cells,
   note §2). Those 115 cells contain block B's 40, and flyvis-30 is flyvis-65 restricted to the
   30 types (note §1), so 32 is an upper bound on block B's present count, not the count (if the
   note's "pair" is C6 existence; not checked). No file opened for this draft gives the count.
   §1.4 says how A §1.4 and a full endpoint table would give its column counts.

**What this compromises.**

- **The block is chosen after block A's verdict.** That is selection after data at the level of
  which block to test (lesson a). It is mitigated, not removed: the candidate list and the
  criteria predate block A's run, and `ceiling_full` = 0.8442 is named in §1.2 as not a reason.
- **The answer is textbook and the bank is public** (risk 3, as for block A).
- **Block A's synthetic limits cannot be reused:** A's worlds were built on block A's board and on
  degree terms that include block B's cells. Block B's limits come from new worlds (§3.6).
- **What was learnt about the instrument on this bank** (for example the λ that block A's
  knockout fits selected: 1, 1, 1, 3, 3; `RESULT.md` line 5) was learnt with block B's cells in
  training. It describes a neighbouring view, not block B's answer, and no cut is set from it.

**What this does not compromise.**

- **No fit is carried over.** Every fit of block B's run is made from scratch on block B's own
  training view with the pinned learners and the harness's fixed starts (A §3.3: every fit is
  deterministic given the bank). What block A's fits learnt from block B's cells is an input of
  no block-B fit.
- **Block B's worlds are rebuilt on block B's knockout view** (§3.6), so block B's content enters
  none of them: their degree terms are fitted with block B masked, and their content pool is the
  present cells outside block B.
- **No prediction on a block-B cell was scored as a knockout target or read out per cell** (items
  3 and 4), so no cut, rank, rule or λ grid was tuned on block B. Every gate and reading rule is revision 3.4.1's, fixed before block B
  was chosen.
- Leg S's 99 shuffled banks are the same banks as in A, reused by design (A §3.2, §3.7); leg P
  and every world get new seeds (§3.7).

**Read declaration (the drafting agent).** Opened: the candidates note; A's registration §0–§11
(§12 located by heading only); `GLOSSARY.md`; ADR-005; the blind review note; block A's
`RESULT.md` lines 1–259; the script `knockout_regrow.py` (constants, checks, worlds, evaluation,
the committed-output writer); the first columns of `types.csv`; seed contexts found by grep. Not
opened: `offsets.csv` as text, `type_pairs.csv`, `summary.json`, the regularity reading, anything
under `chat/`. **Two incidental exposures, stated:** (1) listing the names of `types.csv` also
showed its `n_out_entries` column, a whole-bank degree total per type; with an endpoint table it
bounds an L row's count inside the block; no such difference is written here. (2) While
cross-checking the scratch table against A §1.4, the agent saw that the subtraction gives block
B's column counts and saw the result for one target before stopping. That value is not written in
this file, and the choice (§1.2) was on disk before it.
## 2. The predictors (delta on A §2)

- **§2.1 and §2.2 unchanged:** rule #2.1 (`RANK = 1`, `STARTS = 10`) is the primary, with R/W read
  on both D1 candidates (rule #2.1 and BF_1); BF_1–BF_4 are printed, each with its nested λ.
- **§2.3, N1: changed in its reading, not in its role.** On a 5 × 8 block the parity identity
  `D(c + a_s + b_t) = 0` for every `a`, `b` cannot hold (§0). N1's AUC on block B is therefore not
  confined to the additive band of A §2.3, which was drawn on block A's balanced board. N1 still
  enters no branch; it is printed, and leg S subtracts its AUC on every bank. Check 5 changes
  accordingly (§3.4, D6).
- **§2.4, the two ceilings: definitions unchanged** (`ceiling_full` on the full bank,
  `ceiling_block` on the 40 cells alone with λ by the nested inner folds restricted to them;
  `GATE_CUT` = `MECHANISM_CUT` = 0.90). **Changed:** A's consequences 1–3 (the R world is
  realisable, `ceiling_block` ≈ 1, permuted-block ceilings fall) rest on the block being rank 1.
  They hold for block B's synthetic boards, which are planted rank 1 (§3.6), and are **not known**
  for the real block B. On the real block, a `ceiling_block` below 0.90 can be a rank limit of
  rule #2.1 (its logit is `c + a_s + b_t + u_s v_t + W[G(s), G(t)]`), not only a failed fit (D9).
  The 20 permuted-block ceilings are printed as in A, with no expected fall. The within-fly note
  scales to the block: 61 differing cells of 900, spread evenly, put about 2.7 in 40 cells
  (arithmetic, this draft; A: about 4 in 64); it stays a note, not a cut.

## 3. Statistics (delta on A §3)

### 3.1 The metric

AUC, unchanged. Block B's labels need not be balanced, so the denominators are `n_present` /
`n_absent` (the verdict line already prints them). Printed beside it, deciding nothing, as in A,
with three adaptations (D7): **precision at `n_present`** (the share of present cells among the
`n_present` highest `p_exist`; it is not accuracy when the labels are unbalanced) in place of
precision at 32; **six strata means** in place of A's four quadrants: L1 × ON, L1 × OFF, L2 × ON,
L2 × OFF, {L3, L4, L5} × ON, {L3, L4, L5} × OFF (ON and OFF are the targets' split, §1.2); the
AUC on the 31 cells that are not mirror partners, in place of "the other 59".

### 3.2 The legs

- **Leg S: unchanged** (the same 99 `harness.shuffled_bank(REAL, sd)` banks, the knockout of block
  B by name, the AUC margin over N1, `n_ge = 0` of the `99 − n_deg` shuffles with an AUC, A's D14 (ii),
  `n_deg` named above 5). A shuffled 40-cell block is all present or all absent more easily than a
  64-cell one if it is sparse; `n_deg` is printed.
- **Leg P: unchanged in form:** 9,999 uniform permutations of the 40 labels from one generator
  (seed 91000, §3.7), `p_P = (1 + #{AUC_perm >= AUC_real − TAU}) / 10,000`, passing at `<= 0.01`.
  The AUC needed moves with the counts: the null's standard deviation is
  `sqrt((n_p + n_a + 1) / (12 n_p n_a))`; at 20/20 (the synthetic boards) it is 0.0924, so a pass
  needs an AUC of about 0.72 (normal approximation, this draft; the same formula gives A's 0.0727
  and about 0.67 at 32/32). The script prints the exact value.
- **`smallest_passing_auc`:** unchanged in definition, on the grid `k / (n_p n_a)` (A: `k/1024`);
  two new registered values, one per synthetic board (§3.3, §3.6).
- **Row-and-column variant (printed, decides nothing):** 5 × 8 patterns with the block's row and
  column counts, 640 successful checkerboard swaps per draw as in A, seed 91001. **New guard
  (D7):** a pattern with no checkerboard 2 × 2 (a nested pattern) admits no swap, and A's loop
  (`rc_patterns`, `while (succ < RC_SWAPS).any()`) would never end. If the block's pattern has no
  checkerboard, the variant prints "n/a: the row-and-column null has one pattern".
- **`TAU` stays inert:** every AUC here is a multiple of `1/(2 n_p n_a)` with `2 n_p n_a <= 800`,
  so two unequal margins differ by at least `1/800²` ≈ 1.6e-6, far above 1e-9 (arithmetic, this
  draft).
- **Leg N1:** printed, decides nothing, as in A; on block B it is not "uninformative by algebra"
  (§2).

### 3.3 Uniqueness, determinism and the reproduction gate (delta on A §3.3)

- **Unchanged:** run once from a clean committed tree; `--allow-dirty` makes a run that is not the
  registered run, with A's text; the determinism check; no seed enters the primary numbers except
  `p_P`'s; the gate on the deciding columns, rows matched by key, outcomes 1–3 with parts (a) and
  (b), the four layers and their order of reading, the self-test's two outcomes, the null-input
  digests, the per-fit diagnostic (deciding nothing), the store's declared fields, "a pin is
  integrity, not reproducibility".
- **New reference.** The gate compares with **block B's own pinned pre-run reference**, a new
  folder (proposed `connectome-seed-data/knockout_regrow/synthetic_blockB_prerun/`) with its own
  `PRERUN_DIR`, `PRERUN_SHA256` and `PRERUN_WORLDS_CSV_SHA256`. **Block A's reference is not
  touched and not re-pinned;** A §7's "Recreating the reference" governs A's folder, and block B's
  is a new reference, not a re-pin of A's. Under D10 (i) block B's reference is made by one
  fitting run from a committed head, so two of A's four reasons against a byte gate (mixed fits;
  no producer in git) do not arise; the other two (the `DYNAMIC_ARCH` kernel; the gzip mtime)
  still do, so the column gate is kept. The per-fit diagnostic's split into revision-2 and
  revision-3 worlds does not apply (one run); it is split by kind of fit only.
- **Registered values, recomputed from block B's worlds and read from block B's reference (one
  address, as revision 3.4.1 item B):** `smallest_passing_auc` for board `z_B` and for board
  `z'_B` (from its `synthetic_only.json`), and the `ko1` count, copied and fitted (from its
  `raw_fits.json.gz`). **Their values do not exist yet.** The revision of this file that follows
  the pre-run states them, verified on the pinned files, as A §3.3 did.

### 3.4 Machine checks (delta on A §3.4)

| check | block B |
|---|---|
| 1 pins | unchanged |
| 2 block and mask | 40 cells, 5 distinct sources, 8 distinct targets, all 13 names in `harness.NAMES`, sources and targets disjoint; training mask 4,185 cells, none in the block; `ceiling_block` mask = the 40. **Added:** all 64 cells of block A are in the training mask |
| 3 board as reviewed | **no reviewed count exists** (D3). Replaced by: the block's present count and its six strata counts are printed at run start, before any fit on the real bank; the run stops only if the block has no AUC (0 or 40 present: "BLOCK HAS NO AUC") |
| 4 pre-data tables | the endpoint table's sha256 (§1.4), 40 / 40 inferable and the 9 mirrors must match, else "PRE-DATA TABLES DIFFER"; the training present count is printed, not checked (D3) |
| 5 N1 parity identity | **cannot pass on any non-degenerate 5 × 8 block** (§0); `D(N1 logit)` is printed, no stop (D6) |
| 6 leakage | unchanged: block B's knockout of the real bank against the same with its block replaced by permutation 0 of block B's leg P |
| 7 AUC function | unchanged, plus one hand case with unbalanced labels on 40 cells (A's rank-sum path is checked on four hand cases and one random 32/32 case) |
| 8 harness identity | unchanged (0.028150051052145946 to 1e-9) |
| 9 determinism | unchanged, on block B's knockout view |

### 3.5 What is printed

As A §3.5, with the adaptations of §3.1 (strata, precision at `n_present`, the other 31 cells),
the 9 mirror partners, per-type rows for the 13 types (where a type's block cells hold both
labels), the 20 permuted-block `ceiling_full`, the fixed λ = 1 diagnostic, and two additions
printed beside the verdict and never on it: `D(N1 logit)` (former check 5) and N1's own `p_P`
next to any U (D8).

### 3.6 Synthetic worlds (delta on A §3.6)

**Kept unchanged:** the nine families (R, Nf, No, W, M0.5, M0.6, M0.75, M0.85, M1.0) with the same
γ values (`gamma_z`, `gamma_z1`), 5 worlds each, 45 worlds; the requirement rows and their stops
(R each R; Nf never R or W, at least 3 of 5 G; No never R or W, reads G, U triggers the No
contingency; W each W; the M rows a power curve with no stop); the three limits (γ\*_P, γ_R, the
family limit), their brackets, the transition band, the binomial note, the U rule (threshold U
only); the fixed λ = 1 diagnostic with its path check; 99 shuffles and 20 permuted-block ceilings
per world; the rule that a failed stop row stops the real arm.

**Changed:**

- **Block positions:** block B's 40 cells.
- **Latent polarity on the 13 block types (D4):** targets as in A (`z` = +1 on Mi1, Tm3, Mi4, Mi9;
  −1 on Tm1, Tm2, Tm4, Tm9); sources L1 +1 and L2 −1 (the note's ON and OFF sides), and **L3 +1,
  L4 −1, L5 +1, fixed by rule, not by biology**: the worlds calibrate the instrument on a planted
  rank-1 board of block B's shape, not the biology of L3–L5. The other 52 types (T4a–d and T5a–d
  among them now) draw `z` from the world's seed, as the 49 others did in A.
- **Board `z_B`:** present iff `z_s z_t = +1`. Each L row then holds 4 of 8, so **every world's
  block has 20 present of 40**. `make_world`'s assertion becomes 20 (A: 32).
- **Board `z'_B` (No; and `z1` on the block types in W) (D5):** on the targets, A's `z'` (+1 on
  Mi1, Tm3, Tm1, Tm2; −1 on Mi4, Mi9, Tm4, Tm9), which is exactly orthogonal to `z` over the eight
  targets, with each of the four (`z`, `z'`) classes holding 2 targets; on the sources,
  `z'` = (+1, +1, −1, −1, +1) for L1–L5, so `Σ z z'` = +1 over the five sources (0 is impossible
  with five). Board `z'_B` also holds 20 of 40.
- **Why the No world's pure `z` score still has AUC exactly 0.5** (algebra, this draft; it
  replaces A's "`Σ z z'` = 0 over sources and over targets", which cannot hold with five sources).
  In any row s, the score `z_s z_t` is +1 on the 4 targets with `z_t = z_s` and −1 on the other 4.
  Within each group of 4, `z'_t` = +1 on exactly 2, because each (`z`, `z'`) class of the targets
  holds 2. So under board `z'_B` each score group holds 2 present and 2 absent in every row, 10
  and 10 over the block, and AUC = P(+ on the present, − on the absent) + ½ P(tie) = ¼ + ¼ = ½.
  Only the targets' orthogonality is needed. (Checked numerically on the two boards above: 20 and
  20 present, AUC 0.5 exactly; no bank involved.) The script's assertion changes to: exact
  orthogonality and class sizes of 2 over the targets; `|Σ z z'|` = 1 over the sources.
- **W:** `z1` = `z'_B` on the block types, `γ_z1` = 2.5, `γ_z` = 1.5, as in A. A rank-1 fit that
  takes `z1` scores the `z_B` board at AUC 0.5 exactly by the same algebra.
- **Degree terms:** N1's `(c, a, b)` on the real bank's knockout view of **block B** (outside block
  B only; block A's cells included). **Content pool:** the real bank's present cells outside block
  B.
- **Limits:** recomputed from block B's worlds, and block B's G label prints block B's limits.
  **Block A's limits (γ\*_P = 0.6, γ_R = 0.75, family 0.75) are not block B's.** They are in
  M-world units on block A's degree terms and board; block B's worlds have other degree terms and a
  40-cell board, so block B's limits are measured afresh and are not compared with A's as numbers.
- **The expectations of A §3.6** (R reads R, Nf reads G, No reads G, W reads W) carry over by the
  same algebra on block B's planted boards. They are expectations until block B's pre-run measures
  them.

### 3.7 Seeds (all new; the script asserts that they are distinct)

| use | seed(s) | generator |
|---|---|---|
| leg P, uniform permutations (also permutation 0 of the leakage check) | 91000 | `default_rng(91000)`, 9,999 × `permutation(40)` in order |
| leg P, row-and-column-preserving | 91001 | `default_rng(91001)` |
| ceiling on permuted blocks | 91010–91029 | `default_rng(91010 + j)`, `j` = 0..19 |
| synthetic worlds (family index `i` in A's order R, Nf, No, W, M0.5, M1.0, M0.6, M0.75, M0.85 = 0..8; repeat `j` = 0..4) | 91100 + 10 i + j (91100–91184) | `default_rng`, draws in A's order |
| shuffles of the real bank and of each world | 0..98 | `harness.shuffled_bank(base, sd)`, reused on purpose, as in A |
| BF / rule #2.1 ALS starts | `PCG64(30000 + j)` | fixed in the harness |

**Untouched:** A §3.7's list (60000, 61000, 70000–70999, 80000–80999, 4242, 99, 7, 1000–1019,
the dial seeds, 20260923) **and block A's own seeds** (90000, 90001, 90010–90029, 90100–90154,
90160–90184). **Checked 2026-09-26:** a grep of the repository's `.py`, `.md` and `.json` files for
91000–91999 found no seed: the hits are the cuDNN version string 91002 in night records and digits
inside floating-point values (`diagnosis_power_rows.json` and a `spread` file of rule #2.1's C6
run, contexts printed). The script asserts that the new seeds are distinct, lie in
91000–91999, and meet none of the untouched, reused or block-A seeds.

### 3.8 Vocabulary (additions)

- **Block B** means the 40 cells of §1.2. **Candidate B** means the note's 115-cell rule on the
  30-type grid. The candidates note also uses a bare "B" for the FlyWire-30 bank (note §1); this
  file always writes "FlyWire-30".
- **Prior exposure**, not "contamination" (§1.5).
- **Present in the block:** A §3.8's two carriers, with 20 in every synthetic world and the real
  count unknown before the run.

## 4. Reading rule (unchanged)

A §4 applies **verbatim**: the four branches in order, R and W read on both D1 candidates, the
cuts (`P_R` = 0.01, `P_W` = 0.0125, `P_G` = 0.10, `GATE_CUT` = 0.90, `MECHANISM_CUT` = 0.90), the
U rule's naming, the verdict line's contents, λ on the verdict line. No condition, cut or label
string changes. Three readings that differ on block B, stated so that nobody reads A's glosses
into B's verdict:

- **The quoted rows carry block A's literals.** The G row says "by Johnny's count the information
  is there (64/64 inferable)"; the U row says "all 3 pre-run U worlds sit at γ = 0.6 = γ\*_P" and
  "by §2.4 this is a failure of the fit, since the block is rank 1". For block B the counts are
  40 / 40 (§1.4) and block B's own limits and U worlds (§3.6), printed on its verdict line. The
  script prints a line after the quoted row saying which literals are block A's (D9).
- **"Failed fit" on block B** (D9): the label text "failed fit: rule #2.1 cannot hold the block
  even when trained on it alone" is kept verbatim; it states the measurement. On block B it is
  read as "a failed fit or a rank limit, not separated", since the real block is not known to be
  rank 1 (§2).
- **U and the degree channel** (D8): on block B, N1's additive score can order part of the block
  (§0). A rule that follows it can pass leg P and fail leg S, which reads U, not R. U's label and
  text are kept; the report prints N1's own `p_P` beside any U, and the outcome note names the
  additive channel as a second possible source of U on this block.

## 5. What each outcome means (delta on A §5)

A §5 applies, with "the block" meaning block B. **Joint reading with block A (D11):** each block is
read on its own. Block A's G stands as registered. An R on block B would read "the rule regrows
the lamina's input to the eight motion-pathway inputs, on flyvis's averaged template"; it changes
nothing in block A's G, and neither block alone licenses "the rule regrows the motion pathway".
The cuts are not corrected for two blocks (that would change the gates). `RESULT.md`'s header
states that block B is the second block tested on this bank, chosen after block A's G.

## 6. What the test cannot show (delta on A §6)

A §6 applies, and in addition:

- **No parity or degree argument protects block B** (§0): N1 and the field term can order part of
  it; leg S is the leg that removes that channel.
- **The G gate is not automatic** (§2): a `ceiling_block` below 0.90 can be a rank limit.
- **Less power:** 40 cells; a leg-P pass needs an AUC of about 0.72 at 20/20 against about 0.67 at
  32/32 in A (§3.2). The thinnest source keeps 4 training targets (§1.4).
- **Prior exposure** (§1.5): the block is chosen after block A's verdict, and its cells trained
  every block-A fit.
- **Mirrors:** 9 of 40 partners, and five of them are cells the key names (§1.4); a rule that tied
  source and target factors could read them; no registered predictor does.
- **The male-CNS arm** (A §8) is not part of this registration (§8).

## 7. Environment, script, run command, outputs, cost (delta on A §7)

**Environment and instrument: unchanged.** `tools/.venv` (Python 3.10.20, numpy 2.2.6), CPU, the
pinned numpy harness. The GPU instrument of commit `74de040` (its subject: "separate, unreviewed")
is not used: A §7 says a GPU instrument "inherits none of this instrument's limits" and needs its
own registration (D12).

**Script changes needed (listed; none is made by this draft):**

| # | where (A's script) | change |
|---|---|---|
| S1 | the file | a new script, `results/genome/c6/checks/knockout_regrow_block_b.py`, a copy of A's with the changes below; A's script stays byte-unchanged (D13); a new label test beside A's |
| S2 | `REGISTRATION`, `REGISTRATION_REVISION`, the manifest | this file and its revision; **plus A's registration path, pinned by its LF sha256 at `74db080`**, because §4 is quoted from it (`quote_row`, `quote_section`) and this file does not restate it |
| S3 | the block (lines 173–189) | `SOURCES` = L1–L5, `TARGETS` = the eight; the answer-key sets; `N_BLOCK` = 40; `BLOCK`, `MASKS`; A's `X_SIGN`, `W_SIGN`, `BOARD` removed |
| S4 | `QUADRANTS` | the six strata of §3.1 |
| S5 | `N_TRAIN_CELLS`, `N_TRAIN_PRESENT` | 4,185; no registered present count (printed) |
| S6 | `ENDPOINTS_EXPECTED`, `INFERABLE_EXPECTED`, `MIRRORS_EXPECTED`, `MIRROR_IDX`, `INFERABILITY_PROVENANCE` | the endpoint table's sha256 and its canonical form (§1.4); 40; the 9 mirrors; the FlyWire-30 and male-CNS rows removed |
| S7 | `check_block_and_mask` | 40 / 5 / 8 / 4,185, and block A's 64 cells in the training mask |
| S8 | `check_board` | replaced by the print and the "BLOCK HAS NO AUC" stop (§3.4) |
| S9 | `check_n1_parity` | a printed value, no stop (D6) |
| S10 | `check_auc_function` | one unbalanced 40-cell case |
| S11 | `uniform_perms`, `perm_ceiling_perm` | `permutation(40)`; seeds 91000, 91010 + j |
| S12 | `rc_patterns` | reshape to (5, 8); row and column indices drawn on their own ranges (A draws all four from `integers(8)`); the no-checkerboard guard (D7) |
| S13 | `SEED_*`, `assert_seeds_unique`, `reserved_seeds` | 91000, 91001, 91010, 91100; range 91000–91999; block A's seeds added to the reserved set |
| S14 | worlds: `Z_PLUS`, `ZPRIME_PLUS`, the two assertions, `OTHERS`, `NONBLOCK_CELLS`, `degree_terms`, `make_world` | §3.6 (D4, D5): the polarity of the 13 types; target-only exact orthogonality; 52 others; content pool and degree terms outside block B; assertion 20 |
| S15 | `precision_at_32`, `auc_other_59`, the CSV header, the printed and Markdown tables ("/64", "(32/32)", "other 59", "P@32") | precision at `n_present`; the other 31; block B's own CSV column names (its reference is written by this script, so no compatibility with A's CSV is needed) |
| S16 | `smallest_passing_auc` | docstring (`k/(n_p n_a)`); the logic already uses `N_BLOCK` and the count |
| S17 | `PRERUN_DIR`, `PRERUN_SHA256`, `PRERUN_WORLDS_CSV_SHA256`, `PRERUN_REV2_FAMILIES`, `PRERUN_REV3_FAMILIES`, `_mech_renamed_32` | block B's reference, set in the revision after the pre-run (D10); the revision-2/3 split and revision 3.2's rename check are A's history and not needed |
| S18 | `out_dir_refusal` | refuses `--out` at or in **both** A's and block B's reference folders and on byte copies of either |
| S19 | `write_committed`, `OUT` | `results/genome/c6/checks/knockout_regrow_block_b/`; the title; the line after the quoted §4 row naming A's literals (§4, D9); the header line of §5 |
| S20 | `--arm`, `private_run_dir` | an arm name that keeps block B's private folders apart, for example `flyvis65_blockB` |
| S21 | `WITHIN_FLY_NOTE`, the `TAU` comment | "about 2.7 of 40 cells"; the lattice text made generic |
| S22 | tests | copies of A's 17 label tests adapted to block B's reference, plus: the rc guard; 20/20 on both boards and the exact 0.5 of the No algebra; check 5 as a print; the seed assertion |

**Run commands (to be pinned in the revision after the pre-run):** as A's, with the new script and
arm name, `--starts 10 --workers 30`.

**Outputs:** committed aggregates in `results/genome/c6/checks/knockout_regrow_block_b/`
(`RESULT.md`, `summary.json`, `per_shuffle.csv`, `synthetic_worlds.csv`); private and raw outputs
in `connectome-seed-data/knockout_regrow/<arm>_<UTC stamp>_<head 12>/`; block B's reference in its
own folder (§3.3).

**Cost (estimated from A's measurements):** a fit runs on the 65 × 65 view whatever the block's
size, so the per-fit rate should be A's (assumed; §11). The pre-run is 45 worlds × (3 × 6 + 20 +
99 × 6) = 28,440 fits, about 2 h 10 min at A's measured 3.65 fits per second (A §7); block A's
registered run took 8,070 s in all (`RESULT.md` line 3). The registered run refits the synthetic
step, so the two runs together take about 4.5 h of CPU wall time.

## 8. The animal control

Not part of this registration. A §8's male-CNS arm has not been built. If it is ever run on block
B, its builder must also map L1–L5, and this file is amended to pin the built bank, as A §8 says
for block A.

## 9. Lessons applied (delta on A §9)

| lesson | where here |
|---|---|
| a, selection after the data | the choice after block A's verdict is named (§1.5); `ceiling_full` is named as not a reason (§1.2); the candidates and criteria predate block A's run |
| b, a null that cannot see the other world | block B's own worlds (§3.6) |
| c, a criterion written after the finding | none: every gate and reading rule is revision 3.4.1's (§4) |
| e, read the object | §1.3 names every row removed and every channel left, block A's board included |
| g, denominators | 40 cells, `n_present`/`n_absent`, 4,185 training cells, 40 / 40 inferable, 9 mirrors |

## 10. Decisions for review (reviewers, then Mike)

The body is written with the recommendation of each row.

| # | question | options (what each changes) | recommendation |
|---|---|---|---|
| **D1** | Which block B | **B-motion** (L1–L5 × block A's eight sources, 40 cells): passes K1–K4 by its name rule; it is candidate B restricted by candidate B's own biology, **not one of the note's rules verbatim**. **B-L123** (24 cells): only the L types whose targets the note states; less power. **B-full** (260 cells) and **C** (114): fail K3 by shape, so a failure cannot be read as "no grammar". **Defer:** a new candidates note on the 65-type grid; a session of selection and review | B-motion |
| **D2** | How much of §1.4 is printed before data | (i) the full endpoint table, as A §1.4: with A §1.4 it gives block B's column counts by subtraction. (ii) inferability, minima, mirrors and the table's sha256; the script prints the table at run start and checks the hash. (iii) nothing before data: K3 unverified until the run | (ii) |
| **D3** | Block B's own pattern before the run | (i) counted by name after this choice is committed, three times, as block A's board was, and registered; check 3 then compares with it; §0's open questions (degree channel, rank) are settled before data, and the authors see the answer. (ii) unread until the run: check 3 prints the counts and stops only on "no AUC"; the training present count is printed, not checked | (ii) |
| **D4** | Worlds' polarity on L3–L5 | (i) fixed L3 +1, L4 −1, L5 +1: one layout per board, so the one-value-per-board check of `smallest_passing_auc` can hold. (ii) drawn per world: the layout varies by world, so that check fails by construction and would have to be registered per world (a gate change). (iii) all +1: columns 4 of 5 against 1 of 5 | (i) |
| **D5** | `z'_B` and the No assertion | (i) A's `z'` on the targets (exact orthogonality, classes of 2), `z'` = (+1, +1, −1, −1, +1) on L1–L5, the assertion relaxed to the targets, with §3.6's algebra. (ii) make the sources orthogonal too, which needs an even number of sources, so it changes the block of D1 | (i) |
| **D6** | Check 5 (N1 parity identity) | (i) a printed value, no stop. (ii) kept as a stop: it fails on every non-degenerate 5 × 8 block (§0), so the real arm could never run | (i) |
| **D7** | Printed-only adaptations | strata for quadrants; precision at `n_present`; the other 31 cells; the row-and-column null on 5 × 8 with 640 swaps and a guard for a pattern with no checkerboard (without it the swap loop never ends). All decide nothing | as written |
| **D8** | U and the degree channel | (i) U's label and text unchanged; N1's own `p_P` printed beside U; the outcome note names the additive channel. (ii) a new U reason, "N1 alone passes leg P", on the verdict line: changes a verdict-line string, so it needs its own review and a test | (i) |
| **D9** | A's literals in the quoted §4 rows; "failed fit" | (i) quote A's rows verbatim, then a printed line naming A's literals (64/64; the pre-run U worlds; "the block is rank 1"); "failed fit" read on block B as "fit failure or rank limit, not separated". (ii) restate §4 in this file with block B's literals: a new text of a reading rule, reviewed as such | (i) |
| **D10** | Order of work | (i) commit the script and this draft; the pre-run from that committed head on Mike's word; a revision registering the values read from the pinned reference; review; the registered run. Block B's reference then has a producer in git. (ii) A's D11 order (pre-run before commit): repeats the provenance gap of A §3.3 | (i) |
| **D11** | Joint reading with block A | (i) each block alone, A's G stands, no correction, `RESULT.md` names block B as the second block tried after A's G. (ii) a correction over two blocks (for example `P_R` = 0.005): changes revision 3.4.1's gates | (i) |
| **D12** | Instrument | (i) the pinned CPU harness, as A: the same instrument, about 4.5 h of wall time. (ii) the GPU instrument of `74de040`: separate and unreviewed; by A §7 it needs its own registration and synthetic worlds | (i) |
| **D13** | Script form | (i) a new file, a copy of A's, reviewed as a diff against it; A's file untouched. (ii) a `--block` flag in A's file: the file that A's run and blind review cite changes (A stays reproducible from `74de040`). (iii) import A's module and override its constants: fragile, since `BLOCK`, `MASKS`, `MIRROR_IDX`, `Z_BLOCK`, `ZPRIME` and `NONBLOCK_CELLS` are computed at import | (i) |
| **D14** | Seeds | as §3.7 | as written |

## 11. Not verified at drafting

- **Biology:** the targets of L4 and L5 inside the block; that L1 → OFF and L2 → ON are absent
  (inferred in §1.2, not stated in any file opened); the note's sources were not opened, and
  `literature.md` has no entry on the lamina (a grep for "lamina", L1–L3 and the authors found
  none).
- **The algebra of this draft,** for review: that no non-degenerate 5 × 8 block is balanced in
  rows and columns (§0); the exact 0.5 of the No world with target-only orthogonality (§3.6); the
  normal approximation of the leg-P pass at 20/20 (§3.2); the `TAU` bound (§3.2).
- **`ceiling_block`'s nested λ on 40 cells:** the inner folds restricted to the block hold about 4
  cells each; a fold with no present or no absent cell is possible. On block A's 64 cells no
  failure occurred (A §11); on 40 cells it is not measured until the pre-run.
- **Cost:** the assumption that a block-B fit costs what a block-A fit did.
- **Per-cell exposure in C6:** whether any C6 diagnostic printed per-cell predictions for
  L → medulla cells (§1.5, item 4) was not searched.
- **Block B's present count** is unknown. If it is small, power is low and degenerate shuffles are
  more likely; if it is 0 or 40, the run stops (§3.4).
- **GLOSSARY:** it has no entry for block A, block B or knockout; its rules of use ask for a term
  to be added before use. Not added here (this draft modifies no existing file).
- **The male-CNS mapping of L1–L5** (§8).
