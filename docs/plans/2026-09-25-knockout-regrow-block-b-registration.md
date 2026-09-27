---
**Status: revision 1.6.1: revision 1.6 reviewed, all three reviewers yes (Zcode 18:26, Johnny
18:27, Ark 18:30/18:32 UTC), with the small edits below.** Revision 1.6 and the block-B script at
`8bb5aee` (branch `block-b-script`) were reviewed in the DPC Research chat on 2026-09-27 (Zcode
18:26 UTC, Johnny 18:27 UTC, Ark 18:30 and 18:32 UTC; §10, "Revision 1.6.1"). Revision 1.6.1
applies Ark's small, non-blocking edits, asked for in the same commit; it was drafted 2026-09-28
UTC by a CC subagent on the same word of Mike's (2026-09-27 14:31 UTC, "continue what we were
doing"). Nothing was fitted or run on the real bank and no cell of block B was read for revision
1.6.1; the script's tests ran on fixtures only.

**Revision 1.6's status, as it stood (committed in `8bb5aee`):**
"**Status: revision 1.6: DRAFT, the reviewers' pass on 1.5 (`b810ecb`) applied; not
re-reviewed.** Revision 1.5 and the block-B script at `b810ecb` (branch `block-b-script`) were
reviewed in the DPC Research chat on 2026-09-27 (Johnny 17:54 UTC, Ark 17:58 and 18:00 UTC, Zcode
18:05 UTC; §10, "Revision 1.6"). Revision 1.6 was drafted 2026-09-28 UTC by a CC subagent on the
same word of Mike's (2026-09-27 14:31 UTC, "continue what we were doing"); its changes, each with
its reviewer, are in §10 ("Revision 1.6"). Nothing was fitted or run on the real bank and no cell
of block B was read for revision 1.6; the script's tests ran on fixtures only."

**Revision 1.5's status, as it stood (committed in `b810ecb`):**
"**Status: revision 1.5: DRAFT, the reviewers' pass on the script (`1a765f5`) applied; not
re-reviewed.** The block-B script and its tests, written on revision 1.4.1 (branch
`block-b-script`, commit `1a765f5`), were reviewed in the DPC Research chat on 2026-09-27
(Johnny 16:45 UTC, Ark 16:48 and 16:52 UTC, Zcode 17:01 UTC; §10, "Revision 1.5"). Revision 1.5
was drafted 2026-09-28 UTC by a CC subagent on the same word of Mike's (2026-09-27 14:31 UTC,
"continue what we were doing"); its changes, each with its reviewer, are in §10 ("Revision 1.5").
Nothing was fitted or run on the real bank and no cell of block B was read for revision 1.5; the
script's tests ran on fixtures only."

**Revision 1.4.1's status and history, as they stood (committed in `3e5f2da`):**
"**Status: revision 1.4.1: revision 1.4 reviewed, all three reviewers "yes" (Ark, Johnny, Zcode,
16:01–16:05 UTC), with the one factual correction in §6 that the vote required (§10, "Revision
1.4.1"). Revision 1.4 was: DRAFT, the reviewers' pass on revision 1.3 applied; committed in
`68c0171`.**" Revision 1.3 was reviewed in the DPC Research chat on 2026-09-27 (Ark 15:36 UTC, "yes,
with edits", and 15:39 on Johnny's M6 fix; Johnny 15:41, "yes, with one factual fix"; Zcode 15:46,
"yes, with edits"). Revision 1.4 was drafted 2026-09-27 UTC by a CC subagent on the same word of
Mike's (14:31 UTC, "continue what we were doing"); every change is text only, and each, with its
reviewer, is in §10 ("Revision 1.4"). Nothing was fitted, run or read from the bank for revision
1.4.

**Revision 1.3's status and history, as they stood (committed in `6b195bc`):**
"**Status: revision 1.3: DRAFT, the reviewers' pass on revision 1.2 applied; not re-reviewed, not
committed.**" Revision 1.2 was reviewed in the DPC Research chat on 2026-09-27 (Ark 14:48 UTC, with
a follow-up at 14:59; Johnny 14:56; Zcode 15:11; all "yes, with edits"). Revision 1.3 was drafted
2026-09-27 UTC by a CC subagent on the same word of Mike's (14:31 UTC, "continue what we were
doing"); its changes, each with its reviewer, are in §10 ("Revision 1.3"). Nothing was fitted,
run or read from block B's cells for revision 1.3; the one computation (the endpoint table's hash,
§1.4) read presence outside block B only.

**Revision 1.2's status, as it stood (committed in `9b86839`):** "revision 1.2: DRAFT, A's pins
after Amendment 1, S1–S22 re-checked against the male CNS arm's script, the male arm's script
debts registered as S23–S35; not reviewed, not committed." Revision 1.2 was drafted 2026-09-27 UTC by a CC subagent, after Mike's word in the
DPC Research chat (2026-09-27 14:31 UTC, "continue what we were doing", as relayed by CC: start
Q1, block B on flyvis-65, with a registration revision first); its changes and their sources
are in §10 ("Revision 1.2"). Nothing was fitted, run or read from the bank for revision 1.2.

**The history before revision 1.2, as it stood.** Revision 1.1 (DRAFT, the reviewers' pass on
revision 1 applied; not re-reviewed) was committed in `8591491` together with the male CNS
builder's revision 2. Revision 1 was drafted 2026-09-25 UTC (after Mike's word; the scratch scripts
of §1.4 are stamped 20:12 and 20:14 UTC) by a CC subagent on Mike's word (DPC Research chat,
2026-09-25 20:02 UTC, as relayed by CC; the chat is not in the repository): a second block on
flyvis-65. It was committed as a draft in `d6e3759` (2026-09-26 04:50 UTC) under the name
`2026-09-26-…`, and renamed to its UTC day by `git mv` in revision 1.1 (D15). Revision 1 was
reviewed in the DPC Research chat on 2026-09-26: Johnny 04:57, Ark 05:00, Zcode 05:08 UTC, all
"yes, with edits"; the votes and the edits are in §10 ("Revision 1.1"). Nothing was fitted,
regrown or scored for block B. No cell of block B was read from the bank (§1.5, read declaration).

**What this file is.** A delta on block A's registration,
[`2026-09-24-knockout-regrow-registration.md`](2026-09-24-knockout-regrow-registration.md),
**revision 3.4.1 with its Amendment 1** (revision 3.4.1: commit `74db080`; the registered run of
block A used it at head `74de040`; Amendment 1: commit `6fff1e4`; cited below as "A §n").
**Revision 1.2: which text of A this file pins.** A's file as it now stands (revision 3.4.1 plus
Amendment 1, A §13), LF sha256
**`fc41505690365ff6d82fa618b00b482cc992bb36d708ed3b6fbbe6f54f96dbec`**, is the file block B's
script quotes and checks (S2). The text under which block A's flyvis-65 verdict was made is
revision 3.4.1 alone, LF sha256 `409184dead0a8f9b971bd4b480043725d4a0d1a3c53c20c35734a944a63facd6`,
recovered with `git show 74db080:docs/plans/2026-09-24-knockout-regrow-registration.md`; that is
history and is not re-pinned. Both hashes were recomputed for revision 1.2 from the blobs at
`6fff1e4` and `74db080` (LF bytes; §10, "Revision 1.2").

**What Amendment 1 changed, and what it changes for block B (revision 1.2).** Amendment 1 is
append-only: 45 added lines (one blank line and 44 of text; A goes from 2,495 to 2,540 lines)
after A's line 2,495, one new section "## 13. Amendment 1" (`git show
6fff1e4`). It (1) pins the male CNS bank's four files, (2) cancels A §8's sentence "The same legs,
cuts, seeds and branch rule apply" **as it concerns seeds, for the male CNS arm only** (its seeds
are 92000–92999), (3) names the text of the flyvis-65 verdict (above), and (4) says nothing else
changes. **For block B:** (1) and (2) concern the male arm, not block B; block B's seeds were
already its own (§3.7), and the male arm's seeds now join block B's reserved set (§3.7, S13).
(3) is the pointer above. The one consequence for block B is that **A's LF sha256 changed**, so
S2's pin changes from `409184de…` to `fc415056…`. **A's lines 1–2,495 are byte-identical at
`74db080` and `6fff1e4`** (checked for revision 1.2), so every A line number cited anywhere stays
true, `quote_section("## 4. Reading rule", "## 5. What each outcome means")` returns the same
text, and `quote_row` returns the same line for each label (R 1325, W 1326, G 1327, U 1328; the
amendment holds no line starting with any of the four keys; checked by script on both blobs,
revision 1.2). **Everything of A applies to block B unchanged unless a section below says
otherwise.** Every gate and every reading rule of revision 3.4.1 is kept (Amendment 1 changed
none). What
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
chosen block did not change. **Revision 1.1 correction (Zcode):** "its own biology text" is too
strong for B-motion's targets: candidate B's paragraph names 7 of the 8 (§1.2); the carrier of
the target set is block A's source list.
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

**It is not a test of averaging (revision 1.2).** Block B runs on flyvis-65, the same averaged
template as block A, so no outcome of block B can separate "the rule reads a grammar" from "the
bank is an average of flies" (ADR-005's question (ii)). The male CNS arm's joint reading carries
the caution that the male G "does not by itself exclude averaging as the explanation of
flyvis-65's G" (male arm registration §5; `SEAL_BROKEN_NOTE.md`), and block B does not address
it. **Question (ii) stays paused** (Mike, DPC Research chat, 2026-09-27 14:31 UTC, as relayed by
CC and recorded in `backlog.md` by commit `bbfa91b`; retrospective
`docs/retrospectives/2026-09-27-session-close.md` §5). No sentence of block B's
`RESULT.md` may read its label as evidence for or against averaging.

## 1. The bank, the block, and exactly what is removed

### 1.1 Files and pins

Unchanged: the eight pins of A §1.1 (`offsets.csv`, `types.csv`, `folds.csv`, `harness.py`, rule
#2.1's `fit.py` and `decode.py`, `bf_decode.py`, `n1_decode.py`). The scratch script of §1.4 read
`offsets.csv`, `types.csv` and `harness.py` at the pinned hashes (`8c45e850…`, `237a195a…`,
`6fc80952…`; LF sha256, 2026-09-25 UTC). The block-B script records this file's own LF sha256 in its
manifest, as A's does (§7). **Revision 1.2:** it also checks A's registration against its LF
sha256 after Amendment 1, `fc415056…` (header; S2). **Revision 1.3 (Ark, Zcode; open point 7 of
1.2):** these eight pins are **not extended** to a male bank. A male arm on block B, if one is
ever run, is registered in a file of its own (§8); revision 1.1's rule that this file would be
amended to pin the built male bank is withdrawn by the reviewers' vote on revision 1.2.

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

**Revision 1.1 (Johnny; Zcode on the target set): what this rule is, stated plainly.** The rule
above was written in this draft, after block A's verdict G was known, not in the candidates
note. Its second clause ("a restriction of one of them") admits an option that no line of the note
contains, and B-motion is exactly such an option: **a narrowing invented in this draft.** Its
target set is **carried by block A's source list** (A §1.2), not by candidate B's paragraph, which
names 7 of the 8 (Mi1, Tm3, Tm1, Tm2, Tm4, Mi9, Tm9) and also Tm20, which B-motion leaves out; Mi4
is not in that paragraph (note, lines 81–83, checked for revision 1.1). So the selection after the
data happens **at the level of the block choice itself**, not only through block B's cells having
been in training (§1.5).

**The options, on the 65-type grid.** The candidates note counted its candidates on a 30-type grid
(note §1). Its name rules are translated to the 65 types of `types.csv`: the photoreceptors are
R1–R8 (the eight `input`/`retina` types), the lamina monopolar cells L1–L5.

| option | name rule | cells | K1 structure | K2 copy | K3 endpoints visible (by the rule's shape) | K4 | what choosing it changes |
|---|---|---|---|---|---|---|---|
| **B-full** (candidate B as written) | src ∈ {L1–L5} × tar ∉ {L1–L5, R1–R8} | 5 × 52 = 260 | yes (note §2B) | yes | **no**: the L rows keep only L→L and L→R cells; the note's own risk ("almost a whole-row knockout ... 'no grammar' and 'no information' would be read from the same failure") | yes | a block where a G cannot be told from "no information"; its targets also take in 29 types that the 30-type rule never had to consider (52 against 23; Lawf1, Lawf2 and Am among them), so the note's rule does not fix it on the 65 grid |
| **B-motion** (candidate B restricted; recommended) | src ∈ {L1, L2, L3, L4, L5} × tar ∈ {Mi1, Tm3, Mi4, Mi9, Tm1, Tm2, Tm4, Tm9} (block A's eight sources) | 5 × 8 = 40 | yes: "L1 feeds the ON side (Mi1, Tm3), L2 the OFF side (Tm1, Tm2, Tm4), and L3 feeds Mi9, Tm9 and Tm20" (note §2B) | yes: both polarities and all five L types are removed together | **yes by shape**: each L row keeps its cells into the other 44 non-L, non-R types; each target column keeps its cells from the other 60 types | same sources as candidate B (Meinertzhagen & O'Neil 1991; Takemura et al. 2013, 2015) | the stage upstream of block A: the lamina's input to the eight motion inputs. **It is not one of the note's three rules**: it is a narrowing invented in this draft. Its target set is carried by block A's source list; candidate B's paragraph names 7 of the 8 (not Mi4) and also Tm20, which is left out (revision 1.1, Zcode; D1) |
| **B-L123** | src ∈ {L1, L2, L3} × the same eight | 3 × 8 = 24 | yes | yes | yes by shape | smaller: only the L types whose targets the note states | fewer cells, lower power (a leg-P pass needs a higher AUC on 24 cells than on 40) |
| **C** (candidate C as written) | src ∈ {R7, R8} × tar ∉ {R1–R8} | 2 × 57 = 114 | partly (note §2C) | yes | **no**: the R7 and R8 rows keep only cells into R1–R8 | **no on the 30 grid**: "too small and too noisy" (4 FlyWire-30 pairs, 7 flyvis-30 pairs; note §2). On the 65 grid its targets include Tm5a, Tm5b, Tm5c and Tm5Y (flyvis's Tm5 types; the note names Tm5 as an R7 partner "not among the 30"; the identification is this draft's); its size there was not counted | a near whole-row block, as B-full |
| **defer** | a new candidates note on the 65-type grid | — | — | — | — | — | a new selection round, reviewed before any registration; costs a session |

**Chosen (recommendation; D1): B-motion**, 40 cells, `{L1–L5} × {Mi1, Tm3, Mi4, Mi9, Tm1, Tm2,
Tm4, Tm9}`. Two options pass K1–K4 by their name rule, B-motion and B-L123, and B-motion is the
larger (40 cells against 24). It keeps candidate B's sources (the L types) and literature, and
removes candidate B's own named risk (K3) by restricting the targets to block A's eight sources,
7 of which candidate B's biology names (revision 1.1: revision 1 said "the ones that biology
names"). It is the input stage of block A's pathway, so it asks the same question one synapse
upstream.

**What the choice does not rest on.** Block A's run printed rule #2.1's `ceiling_full` = 0.8442
("orthogonal", as a description only; `RESULT.md` line 5). **That value is not a reason for
choosing block B, and this test does not try to find a block with a higher `ceiling_full`.** The
mechanism label of G is a description from which no decision is read (block A's registration §2.4,
decision (c)), and a block chosen to move it would be selection after the data (lesson a). Nor
does the choice rest on block A's verdict G: B-motion restricts candidate B, which was written
(note committed `10b704e`) before block A's registration, and it is judged by the criteria written
then. **But it is chosen after block A's G, and the narrowing itself is new** (revision 1.1,
Johnny): the candidates and the criteria predate block A's result; the choice among them, and
the option chosen, do not. §1.5 says what that does and does not compromise.

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
(D3). The script prints it at run start, **in the real arm only** (revision 1.5; §1.4 names the
two routes by which a print in `--synthetic-only` would give block B's content).

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

Computed on 2026-09-25 (about 20:12 UTC) by one scratch script (outside the repository, in the drafting agent's
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
  ("PRE-DATA TABLES DIFFER"). **Revision 1.5 (all three reviewers of the script): the table and
  the training present count (§1.3) are printed in the real arm only (D3 (ii)).** In
  `--synthetic-only` (the pre-run) the script checks the hash, the inferable count and the
  mirrors and prints only those. A print in `--synthetic-only` would give block B's content
  before the registered run by two routes: (1) 604 minus the training present count is block B's
  present count; (2) the table's per-name [out, in] pairs, together with the public whole-bank
  degrees (A §1.4), give presence inside the block per name (`check_pre_data_tables`). A consistency check of the scratch script against A's published
  table, on block A's cells only: each of the eight targets' training-target counts equals A
  §1.4's count plus 4, block A's four present cells per source back in training.
- **The canonical form, exactly (revision 1.3; Ark M1, settled with Zcode).** Recovered from the
  scratch script that computed the hash, `blockb_hash.py` (written 2026-09-25 20:14:26 UTC by the
  revision-1 drafting agent; the file is still in that agent's session scratchpad, raw sha256
  `263426b26e45691a627482473cbb893bd7d1530f32d5c421cec220a72abdb633`, and its source is in that
  agent's transcript, `tasks/a49d69f4558f37fce.output`, line 139; neither is in the repository).
  With `SOURCES = ("L1", "L2", "L3", "L4", "L5")`, `TARGETS = ("Mi1", "Tm3", "Mi4", "Mi9", "Tm1",
  "Tm2", "Tm4", "Tm9")`, `BLOCK` the 65 × 65 boolean mask of the 40 cells by `harness.IDX`, and
  `ex = harness.REAL.exists & ~BLOCK`:
  - **keys:** the 13 type names as Python `str` (`"L1"` … `"L5"`, then the eight targets); no
    other key. The outer dict has the one key `"endpoints"`.
  - **values:** a `list` of two Python `int` (not numpy integers, not names): for a source `s`,
    `[int(ex[IDX[s], :].sum()), int(ex[:, IDX[s]].sum())]` (training targets, training sources);
    for a target `t`, `[int(ex[:, IDX[t]].sum()), int(ex[IDX[t], :].sum())]` (training sources,
    training targets). Self-loops are counted (the sums include the diagonal).
  - **serialisation:** `json.dumps({"endpoints": keep}, sort_keys=True, separators=(",", ":"))`
    with the defaults otherwise (`ensure_ascii=True`; the text is ASCII); `sort_keys` sorts every
    dict level, here the outer dict and `keep`, so the order is `L1, L2, L3, L4, L5, Mi1, Mi4,
    Mi9, Tm1, Tm2, Tm3, Tm4, Tm9`; the lists keep their order. The hash is
    `sha256(canon.encode("utf-8"))`, no trailing newline.
  - **one element, in form only:** `"L1":[<int>,<int>]` (the values are not written here, D2).
  - **Recomputed for revision 1.3** (2026-09-27 UTC, `PYTHONUTF8=1`, `tools/.venv`, with the
    inputs at their pins `8c45e850…`, `237a195a…`, `6fc80952…`): a copy of that script's
    computation, printing only the hash, its match and the types above (no count), gave
    `aa0920288e6d…f7705`, equal to the registered value. **What the script touches:** importing
    the harness loads the whole bank into memory, block B included; every count is taken from
    `ex`, in which block B is masked in the same expression, so no value of a block-B cell is
    computed or printed. The earlier scratch script of §1.4 (`blockb_predata.py`, 20:12:45 UTC,
    raw sha256 `251bdb78…`) builds `keep` the same way with tuples, which `json.dumps` writes as
    the same arrays; it printed the table's values to that agent's transcript, and it was not run
    and its output was not read for revision 1.3.
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
   **Revision 1.3 (Ark M7, settled with Zcode): the caveat stays as written.** Zcode's grep of the
   candidates note, repeated for revision 1.3 on `docs/notes/2026-09-25-knockout-block-candidates.md`:
   "pair" is the note's count unit of bank cells ("FlyWire-30 bank (165 pairs)", "flyvis-30 …
   (228 pairs)", lines 16–18; "pairs of B (out of 165) and of flyvis-30 (out of 228)", lines
   37–38; the counts come from `type_pairs.csv`, line 136), and the string "C6" does not occur in
   the note (0 matches). So the note does not say that its "pair" is C6 existence, and "upper
   bound 32" keeps its condition. **Open, not done here:** checking the note's flyvis-30 pairs
   against flyvis-65's C6-present cells would need the bank's cells, block B's among them, which
   D3 (ii) abstains from before the registered run (§11).

**Block B's content cannot be kept blind (revision 1.1, Johnny).** Because `offsets.csv` is
committed and the note has already printed an upper bound of 32 for a superset of the block,
nobody can be blind to block B's content; anyone can count it. What this file can do is **choose
not to count it** before the run (D3 (ii)): no author of this registration counts the block's
cells or writes a count of them, and the reading rules are fixed before anyone does. That is a
declared abstention, checked only by the read declarations of the people involved, not an
enforced blindness. **Revision 1.5:** the script does not print either count route of §1.4 (the
endpoint table, the training present count) outside the real arm, so the pre-run's outputs do not
carry them.

**What this compromises.**

- **The block is chosen after block A's verdict G, and B-motion is a narrowing invented in this
  draft, not a line of the candidates note** (revision 1.1, Johnny; §1.2). That is selection after
  data **at the level of the block choice** (lesson a), and it is a second exposure, separate
  from items 1–5 (block B's cells in training and in public files). It is mitigated, not removed:
  the candidate list and the criteria predate block A's run, the reading rules and cuts are
  revision 3.4.1's, and `ceiling_full` = 0.8442 is named in §1.2 as not a reason. What is not
  mitigated: the narrowing and the choice among the options were made by an author who knew
  block A's result.
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
showed its `n_out_entries` column, a whole-bank degree total per type. **Revision 1.1
(Zcode):** that column needs no endpoint table to say something about block B. On its own it is an
upper bound on each L row's count inside the block (a type has at most one compiled pair per json
entry, GLOSSARY §2, "json entry"), and with counts already public (the note's bound of 32 on the
30-type grid, item 5; A §1.4) it bounds the block's content further. Revision 1 said "with an
endpoint table it bounds", which understated it. No such bound is computed or written here. (2) While
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
AUC on the 31 cells that are not mirror partners, in place of "the other 59". **Revision 1.3 (Ark
M6, withdrawn as an edit; this half line kept; its parenthesis rewritten in revision 1.4, Ark
15:39, Zcode, on Johnny's diagnosis):** {L3, L4, L5}: the note names no ON/OFF side for them (it
names no targets for L4 and L5; for L3 it names three — Mi9, Tm9 and Tm20 — of which the block
keeps two, Mi9 and Tm9, one ON and one OFF by the key, §1.2; the reviewers' wording "names no
targets" is narrowed here for L3); not a polarity claim (the
strata are source type × the targets' ON/OFF split of the key,
§1.2, not the L3–L5 polarities fixed for the worlds by D4).

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
- **A block on which leg P cannot pass: the "not readable" U (revision 1.3; Johnny edit 1, Ark,
  Zcode; open point 3 of 1.2).** Ported from the male CNS arm **by its object, not by a count**:
  on the real block, `smallest_passing_auc is None` (no AUC on the grid reaches `p_P <= 0.01`)
  reads a U of its own kind, "not readable", which **takes precedence over every other branch (R,
  W and G alike), is never renamed by the U rule, and is not a threshold U** (S38). No threshold
  on `n_present` is registered for it; the object `smallest_passing_auc is None` is the condition.
  The 0 / 40 stop of §3.4 check 3 stays as it is (a block with no AUC has no label at all). Male
  sources: `knockout_regrow_male_cns.py` lines 407–411 (the comment and `NOT_READABLE_REASON`)
  and line 1627 (`read_label(rows, n_present=int(y.sum()), readable=spa is not None)`, in
  `evaluate_bank`); the male registration's S16 (line 1308) and D8 (line 1474). A's script has no
  such rule: its `evaluate_bank` calls `read_label(rows)` (`knockout_regrow.py` line 1099).
- **Row-and-column variant (printed, decides nothing):** 5 × 8 patterns with the block's row and
  column counts, 640 successful checkerboard swaps per draw as in A, seed 91001. **New guards
  (D7; revision 1.1, Ark and Zcode).** A's loop (`rc_patterns`, `while (succ < RC_SWAPS).any()`)
  has no attempt limit, so a chain that cannot reach 640 swaps never ends. (1) **An attempt cap
  with a stop**, on the pattern of the harness's own rewiring (`harness.py:881–883`:
  `cap = 100 * target`, `while … succ < target and att < cap`): each chain may make at most
  100 × 640 = 64,000 attempts; if any chain reaches the cap before its 640 swaps, the script stops
  with "ROW-AND-COLUMN NULL: ATTEMPT CAP REACHED (chain …, successes …, attempts …)". The harness
  records `successful_swaps` and `attempts` and goes on (`shuffled_bank`, lines 905–916); the
  stop here is block B's own rule. (2) **Before the loop**, a pattern with no checkerboard 2 × 2 (a
  nested pattern) admits no swap at all; its row-and-column null has exactly one pattern, and the
  variant prints "n/a: the row-and-column null has one pattern" instead of entering the loop.
  (3) **Revision 1.3 (Ark, Zcode; open point 2 of 1.2): the stop leaves a file.** D7's stop is
  kept; before it exits, the script writes a stop record as a file (`stop_record.json`) in the
  run's own folder, with the chain, `succ`, `att`, the arm and the head, so that from outside a
  stopped run is told from a run that never started by a file, not by a log line (S39).
  **A's code would not even reach the loop on block B:** `reshape(8, 8)` of 40 labels raises
  `ValueError` ("cannot reshape array of size 40 into shape (8,8)"), and with the reshape fixed to
  (5, 8) but the indices still drawn by `integers(8)`, the first row index above 4 raises
  `IndexError` (both checked on numpy 2.2.6, `tools/.venv`, no bank involved; S12).
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
- **What a pin covers (revision 1.3; Ark M3, settled with Zcode; S17).** Each of block B's
  reference pins is the sha256 of a file's **raw bytes**, `.gz` included, read with
  `read_bytes()` as A's `check_prerun_files` (`knockout_regrow.py` lines 1512–1540, the hash at
  line 1530) and the male one (`knockout_regrow_male_cns.py` lines 2074–2106, the hash at line
  2096) do: it is integrity. It is not reproducibility: `raw_fits.json.gz` cannot be
  byte-reproduced, because gzip writes its mtime into the header (A §3.3, lines 763–769, "A pin
  is integrity, not reproducibility"; reason (4) of the four, lines 636–641). What a rerun must
  reproduce is carried by the column gate of this section, not by the pins. **A red pin is never
  answered by re-pinning** (A §7, "Recreating the reference", lines 1648–1655; A's summary, lines
  47–49): a new reference goes to a new folder, and `PRERUN_DIR` and the pins move together in one
  reviewed, committed change.
- **Two consequences of the byte-copy guard as S18 words it (revision 1.4; Ark, Zcode; checked
  against the male `out_dir_refusal`, `knockout_regrow_male_cns.py` lines 2944–2974: the rule in
  its docstring, lines 2947–2952, the content guard, lines 2964–2973).** (a) A folder in which no
  pinned-name file is present (empty, or holding the reference's files under other names) is not
  refused as a copy: the guard compares only the pinned-name files that are present, and with none
  present there is nothing to compare (`if present and all(...)`, line 2970). Only the path guard
  (at or inside a reference folder) applies to it. (b) The rule rests on the `.gz` bytes not being
  reproducible: a fresh run in a folder that holds the old content does not match every pin (its
  `raw_fits.json.gz` carries a new gzip mtime), so it is not refused; if the pinned set ever became
  fully byte-reproducible, a fresh run into such a folder would be refused as a copy (the male
  docstring's falsifier, lines 2950–2952). Both are stated, not changed: S18's rule stands.
- **New reference.** The gate compares with **block B's own pinned pre-run reference**, a new
  folder (proposed `connectome-seed-data/knockout_regrow/synthetic_blockB_prerun/`) with its own
  `PRERUN_DIR`, `PRERUN_SHA256` and `PRERUN_WORLDS_CSV_SHA256`. **The sequence (revision 1.5;
  Zcode's answer to Ark):** the pre-run's `--out` is a new stamped folder; `PRERUN_DIR` and the
  pins move to it in the revision after the pre-run (D10 (i), step (4) of the order of work in
  the header); the path the constant names now is never written into, since S18's path guard
  refuses `--out` at or inside it unconditionally, pins or none (`protected_references` and the
  path guard of `out_dir_refusal` in block B's script). **Block A's reference is not
  touched and not re-pinned;** A §7's "Recreating the reference" governs A's folder, and block B's
  is a new reference, not a re-pin of A's. Under D10 (i) block B's reference is made by one
  fitting run from a committed head, so two of A's four reasons against a byte gate (mixed fits;
  no producer in git) do not arise; the other two (the `DYNAMIC_ARCH` kernel; the gzip mtime)
  still do, so the column gate is kept. The per-fit diagnostic's split into revision-2 and
  revision-3 worlds does not apply (one run); it is split by kind of fit only.
- **The reference is made by fitting, never by a re-read (revision 1.6, A4; Ark 17:58 and 18:00,
  Zcode 18:05, Johnny 17:54).** Block B's reference is made by one fresh fitting
  `--synthetic-only` run from a committed head (S17, D10 (i)). A `--synthetic-only --from-raw`
  run with `--out` is refused before any folder is made ("REFUSED: block B's reference is made by
  one fresh fitting run (S17, D10 (i)); an --out folder can be a reference, and a re-read is not
  one. Run --from-raw without --out."); without `--out` it writes nothing and is a diagnostic, as
  the male §3.3.1 (h) check is registered (no `--out`). **The rule is decided by the object read,
  not by the writer's hash:** S37's `PRERUN_SCRIPT_SHA256_LF` is the LF sha256 of the script file
  (`"script_sha256_lf": sha256_lf(Path(__file__))`, line 3480 at `b810ecb`), the same with or
  without `--from-raw`. What a re-read lacks is a tie between the loaded store and block B. Four
  readings of the script at `b810ecb`: (1) the store's key is `"||".join(k)` in `write_raw` (line
  3008) and `k.split("||")` in `read_raw` (line 3013): the bank key (a world or `real`), the mask
  kind and the predictor, **no block name**; the masks come from the script's constants
  (`MASKS`, line 232), not from the store; (2) `read_raw(a.from_raw)` goes straight into
  `run_synthetic` (line 3506) with no check of whose store it is; (3) `evaluate_bank` takes each
  world's labels from the store (`base["N1"]["y"]`, line 1433) and checks them only against the
  other fits of the same store (line 1436): **under `--from-raw` the block's labels come from the
  store, and the only cross-check is the fits' agreement with each other**; (4) the one link,
  `from_raw_record["is_the_pinned_store"]` (lines 3472–3473), was recorded and decided nothing,
  and with no pins it was vacuously true (`None == None`); besides, `not_a_reference` (line 3382)
  was tied only to the dirty tree, and `prerun_provenance` read only `git_head` and
  `script_sha256_lf` from the reference's manifest (lines 2060–2062). **D10 (i) is about
  provenance, not method** (Johnny): it asks that block B's reference have a producer in git, one
  fitting run from a committed head; a re-read's producer is whatever wrote the store it reads.
  **The asymmetry with A is a gain:** A's reference table was itself a re-read of A's own store
  (A §3.3, line 632: its `SYNTHETIC.md` records "0 new world fits"), so a later re-read of A's
  store checks a re-read against a re-read; block B's reference is built by fitting from scratch,
  so a later `--from-raw` re-read of block B's pinned store checks the re-read path against a
  fitted reference, which is strictly stronger. **With the reproduction gate (㉜):** this rule
  and `check_prerun_reproduced(..., reread=True)` are one rule seen from two sides: a re-read is
  compared with the pinned table only when its store is block B's own pinned `raw_fits.json.gz`
  (`is_the_pinned_store`, revision 1.6: a condition, False when the pins or the file are absent);
  a re-read of any other store is not compared and records no outcome; `passed` stays `None` for
  every re-read (A revision 3.2: a re-read is not a reproduction). On the reader's side, a
  reference whose manifest carries `not_a_reference` is refused (S37, revision 1.6).
- **What being a reference needs, and three readings of the code (revision 1.6.1; Ark 18:30 and
  18:32; S40, S37, S17).** Being block B's reference needs **the registered form** (no smoke
  option, `--starts 10`) **and a clean committed tree**: `main` sets `not_a_reference` when the
  tree is dirty **or** the run is not in the registered form (`if (dirty or not comparable)`,
  line 3457 of 1.6.1; 1.6 had `dirty and comparable`), with its actual cause
  (`not_a_reference_text`: an `--allow-dirty` run carries `NOT_A_REFERENCE_TEXT`, a run not in
  the registered form `NOT_A_REFERENCE_FORM_TEXT`, which names the uncommitted tree as well when
  there is one). For a comparable run the mark equals `dirty`, so the pre-run is unchanged; a
  clean-tree `--synthetic-only --out` run with a smoke option or `--starts 3` is now marked, and
  the reader refuses it (S37). (1) The manifest's `from_raw_record` is `None` unless `--from-raw`
  is given (`a.from_raw_record = None`, then set under `if a.from_raw:`, lines 3544–3547 of
  1.6.1), so in a fresh run `pinned_store` is False by construction and the re-read branches of
  `check_prerun_reproduced` and `check_ko1_count` are never taken. (2) `prerun_provenance` is
  called only under `reference_mode()` (lines 3529–3530 of 1.6.1), that is, **not in the
  pre-run, by design**: in the pre-run there is no reference to read, this run makes it (D10
  (i)). This is not an omission and is not to be "fixed" later. (3) `--arm --from-raw` is
  **refused, not marked**: `main` exits with "REFUSED: the real arm runs as registered: --starts
  10, no smoke option, no --from-raw (sections 3.3, 7)" before any check, fit or folder (line
  3385 of 1.6, line 3414 of 1.6.1).
- **Registered values, recomputed from block B's worlds and read from block B's reference (one
  address, as revision 3.4.1 item B):** `smallest_passing_auc` for board `z_B` and for board
  `z'_B` (from its `synthetic_only.json`), and the `ko1` count, copied and fitted (from its
  `raw_fits.json.gz`). **Their values do not exist yet.** The revision of this file that follows
  the pre-run states them, verified on the pinned files, as A §3.3 did.

### 3.4 Machine checks (delta on A §3.4)

| check | block B |
|---|---|
| 1 pins | unchanged |
| 2 block and mask | 40 cells, 5 distinct sources, 8 distinct targets, all 13 names in `harness.NAMES`, sources and targets disjoint; training mask 4,185 cells, none in the block; `ceiling_block` mask = the 40. **Added:** all 64 cells of block A are in the training mask. **Revision 1.3 (Ark M2, no new check):** since the training mask is `~BLOCK_B`, this addition is exactly `BLOCK_A ∩ BLOCK_B = ∅` |
| 3 board as reviewed | **no reviewed count exists** (D3). Replaced by: the block's present count and its six strata counts are printed at run start, before any fit on the real bank; the run stops only if the block has no AUC (0 or 40 present: "BLOCK HAS NO AUC"). **Revision 1.3:** unchanged; a block that has an AUC but on which leg P cannot pass reads the "not readable" U (§3.2, S38), not a stop |
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

**Revision 1.4 (Zcode, Ark): where the "not readable" U is counted apart (the carrier of S38's
"counted apart").** When it fires, it is printed on the verdict line and counted on its own line in
`RESULT.md`'s U-rule paragraph, separately from the threshold U worlds (S32 governs that
paragraph's text, not this count); wherever §3.5 or §3.6 counts U kinds, it has its own place and
is never added into the threshold U count.

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
90160–90184). **Checked 2026-09-25 UTC:** a grep of the repository's `.py`, `.md` and `.json` files for
91000–91999 found no seed: the hits are the cuDNN version string 91002 in night records and digits
inside floating-point values (`diagnosis_power_rows.json` and a `spread` file of rule #2.1's C6
run, contexts printed). The script asserts that the new seeds are distinct, lie in
91000–91999, and meet none of the untouched, reused or block-A seeds.

**Revision 1.2: the male CNS arm's seeds join the untouched list.** The male arm, registered and
run after revision 1.1, uses 92000, 92001, 92010–92029 and 92100–92184 in the range 92000–92999
(male arm registration §3.7; `knockout_regrow_male_cns.py` lines 345–349 at `01d2d05`, unchanged
to HEAD), and its script already reserves block B's seeds (`B_SEEDS`, line 353: 91000, 91001,
91010–91029, 91100–91184, the values of this section). The two ranges are disjoint, so no seed of
this section changes; block B's reserved set adds the male seeds (S13). **Re-checked 2026-09-27
UTC:** `git grep -n -E '\b91[0-9]{3}\b' -- '*.py'` finds one line, the male script's `B_SEEDS`
(block B's own seeds, reserved there), and no other use.

### 3.8 Vocabulary (additions)

- **Block B** means the 40 cells of §1.2. **Candidate B** means the note's 115-cell rule on the
  30-type grid. The candidates note also uses a bare "B" for the FlyWire-30 bank (note §1); this
  file always writes "FlyWire-30".
- **Prior exposure**, not "contamination" (§1.5).
- **Present in the block:** A §3.8's two carriers, with 20 in every synthetic world and the real
  count unknown before the run.

### 3.9 Rules of counting and record (revision 1.2; retrospective 2026-09-27 §4)

The retrospective's rules (`docs/retrospectives/2026-09-27-session-close.md` §4, lines 155–166)
that bear on a registration, bound on this file, its later revisions, block B's script and its
outputs. They add requirements; they relax none.

- **A counted claim states its scope and its denominator** ("k of n", and what n counts). A count
  carried from one scope to another is recounted in the new scope first; it is not carried.
  (Source: the male ledger's "one world of five" carried from seen/n to R/n without a recount,
  retro §3, lines 138–140.) In the script this is S34.
- **Every census number carries its scope label** (every fit / `ko`–`ko1` / D1) **and the band it
  was counted at.** Block B runs on the CPU harness (D12 (i)) and registers no census; the rule
  binds any tie or at-risk count that a later revision or a review of block B writes. (Source:
  Ark's at-risk counts at 2·2^-23 against the registered 2^-23, retro §3, lines 141–143.)
- **"Not recomputed" is read from the run log**, not assumed from the code path. Any statement in
  block B's `RESULT.md`, its later revisions or its reviews that a fit or a value was reused, not
  refitted, cites the log line or the stored field (`reused_from_ko`) that shows it. (Source:
  revision 3.4's "`reused_from_ko` is derived from `lam`" claim, retro §3, lines 121–123.)
- **Callers are read from the Orbit code graph and confirmed by grep** when block B's script is
  written and reviewed (retro §4, line 165); an absence is confirmed by grep, not by the graph.
  **Revision 1.3 (Johnny's note, in Zcode's form):** the callers check is done at the script's
  review, and the grep command it ran goes into the review artifact.

## 4. Reading rule (delta: one U kind precedes the four branches)

A §4 applies **verbatim**: the four branches in order, R and W read on both D1 candidates, the
cuts (`P_R` = 0.01, `P_W` = 0.0125, `P_G` = 0.10, `GATE_CUT` = 0.90, `MECHANISM_CUT` = 0.90), the
U rule's naming, the verdict line's contents, λ on the verdict line. No condition, cut or label
string changes. (Revision 1.2: A §4 is quoted from A's file as it now stands, pinned by
`fc415056…`; §4 is A's lines 1296–1374, byte-identical to revision 3.4.1's, since Amendment 1
only appends after line 2,495; see the header.) **Revision 1.3 qualifies "no condition … or label
string changes":** one U kind is added before A's four branches, the "not readable" U of §3.2
(S38), on the reviewers' vote on revision 1.2 (Johnny edit 1, Ark, Zcode). A's branches, cuts and
label strings are otherwise quoted and applied as they stand; the new U text is block B's own,
reviewed as part of this file, and tested by S38. Three readings that differ on block B, stated
so that nobody reads A's glosses into B's verdict:

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

**A fifth outcome (revision 1.4; Ark M8, Zcode):** a block whose `smallest_passing_auc` is `None`
reads the "not readable" U (§3.2, S38), not G, and says nothing about a grammar, because at
`n_p` = 1 the floor of `p_P` is 0.0245 < `P_G` = 0.10, so by the letter of A §4 a G would be
reachable without the precedence.

## 6. What the test cannot show (delta on A §6)

A §6 applies, and in addition:

- **No parity or degree argument protects block B** (§0): N1 and the field term can order part of
  it; leg S is the leg that removes that channel.
- **The G gate is not automatic** (§2): a `ceiling_block` below 0.90 can be a rank limit.
- **Less power:** 40 cells; a leg-P pass needs an AUC of about 0.72 at 20/20 against about 0.67 at
  32/32 in A (§3.2). The thinnest source keeps 4 training targets (§1.4). **Revision 1.2 (scope of
  this statement):** it is arithmetic on the leg-P null at the two block sizes (normal
  approximation, §3.2), not a measurement of the instrument. How often block B's instrument sees
  a planted board is measured only by block B's own worlds (§3.6), 5 per γ, and **is not compared
  with A's curves or limits as numbers**: the Q2 note
  (`docs/notes/2026-09-27-knockout-regrow-power-curves-A-vs-male.md` §0, §6) found that per-γ
  counts at 5 worlds per γ on different draws of worlds cannot separate "a weaker instrument"
  from "a different draw" (a one-grid-step shift is missed about 38 % of the time by the pooled
  exact test, Q2 §3.3), and the male arm's claim "instrument weaker" was narrowed for that reason
  (male arm registration §11, the row after the Q2 note, lines 1854–1864 at HEAD `bbfa91b`). No
  line of block B's script or `RESULT.md` says block B's instrument is weaker or stronger than
  A's; the per-γ counts it prints beside its limits are the reading, stated with their
  denominators (5 worlds per γ).
- **Few present cells (revision 1.3; Johnny edit 1, Ark, Zcode).** The leg-P bar moves with the
  count: the fewer present (or absent) cells the block holds, the higher the AUC a pass needs, and
  at the extreme no AUC passes (§3.2, the "not readable" U, S38). **A reviewer's unregistered
  probe, deciding nothing:** Ark's `b_spa_probe.py` (Ark's review sandbox, outside this repository), a run of `smallest_passing_auc` with block B's leg-P
  parameters (N = 40, seed 91000, `N_PERM` = 9,999; no bank involved), relayed by CC, gave None
  at `n_p` = 1, 0.9605 at 2, 0.9009 at 3, 0.8542 at 4, 0.7990 at 6, 0.7467 at 10 and 0.7150 at 20,
  and a floor of `p_P` = 0.0245 at `n_p` = 1. By that probe the one hole below the middle is
  `n_p` = 1. **Revision 1.3 wrote, as arithmetic, not probed:** "the uniform permutation null of
  the AUC depends on `n_p` and `n_a` symmetrically (with one absent cell there are again only 40
  arrangements), so `n_p` = 39 is the same hole." **Revision 1.4 (Ark, Zcode): now probed, by a
  reviewer's unregistered probe deciding nothing.** Ark's `b_spa_probe2.py` (Ark's review sandbox, outside this
  repository; on the pinned numpy 2.2.6; N = 40, seed 91000; no bank involved), relayed by CC: `n_p` = 1 → None
  (floor of `p_P` 0.0245); `n_p` = 39 → None (floor 0.0237); `n_p` = 2 and `n_p` = 38 →
  0.9605263157894737 both (denominator 76). The symmetry is exact in the verdict and near in the
  floor. **Revision 1.4.1 (Ark 16:01/16:03, Zcode 16:05):** the earlier probe table (the values above)
  was reproduced by the second script on the same interpreter and the same numpy
  (`connectome-seed/tools/.venv`, 2.2.6); no other numpy version was used in this review. Neither hole is a registered threshold: the rule reads the object
  (`smallest_passing_auc is None`), whatever the count.
- **The bar against the count and the layout (revision 1.4; Ark M9, Zcode; the same probe status:
  unregistered, deciding nothing, relayed by CC).** The bar rises as present cells fall **in
  trend, not monotonically**: `n_p` = 15 → 0.72267, 16 → 0.72396, 17 → 0.71867. At one count it
  depends on **which** cells are present (the layout), because the null is one fixed set of
  permutations (seed 91000) applied to that layout: `n_p` = 8 → 0.7695 / 0.7734 / 0.7617;
  `n_p` = 16 → 0.7266 / 0.7161; `n_p` = 20 → 0.7175 / 0.7125; `n_p` = 2 → 0.9605 in all four
  layouts probed. **What this supports:** D4 (i)'s stated reason, that one layout per board is
  what lets the one-value-per-board check of `smallest_passing_auc` hold, and that under D4 (ii)
  (the L3–L5 polarities drawn per world, so the layout varies by world) that check would fail by
  construction. The probe is independent support for that reason only; it does not bear on the
  biology of L3–L5, which D4 does not claim, and it changes no registered value (the per-board
  values are read from block B's reference, §3.3).
- **Prior exposure** (§1.5): the block is chosen after block A's verdict, and its cells trained
  every block-A fit.
- **Mirrors, a named risk (revision 1.1, Johnny).** 9 of block B's 40 cells have a present mirror
  (block A: 5 of 64), and five of the nine partners are cells that the answer key names as present
  (§1.4). The registered predictors do not tie a type's source factor to its target factor
  (BF_r's `U` and `V` are separate; rule #2.1 has one `(u, v)` pair and the group-level `W`;
  A §1.4), so the mirrors are **not a direct channel** for them. They would be one for any rule
  that tied the two roles, and a regrowth by such a rule on block B would have to be read against
  the mirrors first. The 9 partners are printed on their own line, with the AUC on the other 31.
- **The male-CNS arm** (A §8) is not part of this registration (§8). **Revision 1.2:** it has
  since been registered and run on block A only (§8), and it does not bear on block B's reading.

## 7. Environment, script, run command, outputs, cost (delta on A §7)

**Environment and instrument: unchanged.** `tools/.venv` (Python 3.10.20, numpy 2.2.6), CPU, the
pinned numpy harness. The GPU instrument of commit `74de040` (its subject: "separate, unreviewed")
is not used: A §7 says a GPU instrument "inherits none of this instrument's limits" and needs its
own registration (D12). **Revision 1.2, a fact since revision 1.1, not a change of D12:** the GPU
instrument now has its own registration (`docs/plans/2026-09-26-gpu-instrument-registration.md`,
revisions 1–1.4) and validation (V0–V8, commits `e50bf74`, `1ad6155`, `0c7a67b`); no registered
arm reads it, and D12 (i) stands as written unless the reviewers reopen it.

**The command's environment (revision 1.2; male arm ledger, lines 1726–1733 at HEAD):** every
run of block B's script whose output is redirected is made with `PYTHONUTF8=1` (retrospective §4),
and the manifest records it (S28). S23 and S24 make the code independent of that setting; the
setting stays, as a second guard.

**Script changes needed (listed; none is made by this draft):**

| # | where (A's script) | change |
|---|---|---|
| S1 | the file | a new script, `results/genome/c6/checks/knockout_regrow_block_b.py`, a copy of A's with the changes below; A's script stays byte-unchanged (D13); a new label test beside A's |
| S2 | `REGISTRATION`, `REGISTRATION_REVISION`, the manifest | this file and its revision; **plus A's registration path, pinned by its LF sha256**, because §4 is quoted from it (`quote_row`, `quote_section`) and this file does not restate it. **Revision 1.1 said "at `74db080`" (`409184de…`); revision 1.2 pins A after Amendment 1: `A_REGISTRATION_SHA256_LF_AMENDED` = `fc41505690365ff6d82fa618b00b482cc992bb36d708ed3b6fbbe6f54f96dbec`** (the value and the constant's name are the male arm's, `knockout_regrow_male_cns.py` lines 74–75 at `01d2d05`), checked at run start and recorded in the manifest; `409184de…` is kept as a second, informational constant naming the text of A's verdict (as the male script's `A_REGISTRATION_SHA256_LF_FLYVIS65`, lines 78–79). `quote_row` and `quote_section` read A's file by path, never this file (this file has no row that starts with a label key; male S2's reasoning). **Revision 1.3 (Ark, Zcode; open point 1 of 1.2):** the pin stays on A after Amendment 1 (`fc415056…`); if A ever gets an Amendment 2, block B's run stops on the pin mismatch, and that stop is read as "A changed", not as a defect of the environment |
| S3 | the block (lines 173–189) | `SOURCES` = L1–L5, `TARGETS` = the eight; the answer-key sets; `N_BLOCK` = 40; `BLOCK`, `MASKS`; A's `X_SIGN`, `W_SIGN`, `BOARD` removed |
| S4 | `QUADRANTS` | the six strata of §3.1 |
| S5 | `N_TRAIN_CELLS`, `N_TRAIN_PRESENT` | 4,185; no registered present count (printed) |
| S6 | `ENDPOINTS_EXPECTED`, `INFERABLE_EXPECTED`, `MIRRORS_EXPECTED`, `MIRROR_IDX`, `INFERABILITY_PROVENANCE` | the endpoint table's sha256 and its canonical form (§1.4); 40; the 9 mirrors; the FlyWire-30 and male-CNS rows removed |
| S7 | `check_block_and_mask` | 40 / 5 / 8 / 4,185, and block A's 64 cells in the training mask |
| S8 | `check_board` | replaced by the print and the "BLOCK HAS NO AUC" stop (§3.4) |
| S9 | `check_n1_parity` | a printed value, no stop (D6) |
| S10 | `check_auc_function` | one unbalanced 40-cell case |
| S11 | `uniform_perms`, `perm_ceiling_perm` | `permutation(40)`; seeds 91000, 91010 + j |
| S12 | `rc_patterns` | reshape to (5, 8) (A's `reshape(8, 8)` raises `ValueError` on 40 labels); row and column indices drawn on their own ranges (A draws all four from `integers(8)`, which raises `IndexError` on a 5-row pattern); an attempt cap of 100 × 640 per chain with a stop message, on the pattern of `harness.py:881–883`; the no-checkerboard pre-check printing "n/a" (D7; revision 1.1, Ark and Zcode). **Revision 1.3:** the stop writes its stop record first (§3.2 (3), S39) |
| S13 | `SEED_*`, `assert_seeds_unique`, `reserved_seeds` | 91000, 91001, 91010, 91100; range 91000–91999; block A's seeds added to the reserved set; **revision 1.2: and the male arm's (92000, 92001, 92010–92029, 92100–92184; §3.7)** |
| S14 | worlds: `Z_PLUS`, `ZPRIME_PLUS`, the two assertions, `OTHERS`, `NONBLOCK_CELLS`, `degree_terms`, `make_world` | §3.6 (D4, D5): the polarity of the 13 types; target-only exact orthogonality; 52 others; content pool and degree terms outside block B; assertion 20 |
| S15 | `precision_at_32`, `auc_other_59`, the CSV header, the printed and Markdown tables ("/64", "(32/32)", "other 59", "P@32") | precision at `n_present`; the other 31; block B's own CSV column names (its reference is written by this script, so no compatibility with A's CSV is needed) |
| S16 | `smallest_passing_auc` | docstring (`k/(n_p n_a)`); the logic already uses `N_BLOCK` and the count. (Block B's S16 keeps this meaning; the male arm's S16 "not readable" rule is ported as S38, revision 1.3) |
| S17 | `PRERUN_DIR`, `PRERUN_SHA256`, `PRERUN_WORLDS_CSV_SHA256`, `PRERUN_REV2_FAMILIES`, `PRERUN_REV3_FAMILIES`, `_mech_renamed_32` | block B's reference, set in the revision after the pre-run (D10); the revision-2/3 split and revision 3.2's rename check are A's history and not needed. **Revision 1.3 (Ark M3, settled with Zcode): what each pin covers.** `PRERUN_SHA256` pins the **raw bytes** of every file of block B's reference, `raw_fits.json.gz` included, read by `check_prerun_files` with `read_bytes()` as A's (lines 1512–1540) and the male one (lines 2074–2106) do; `PRERUN_WORLDS_CSV_SHA256` is the worlds table's entry of that dict. The pins are integrity only: the `.gz` bytes are not reproducible (A §3.3, lines 763–769), so what a rerun must reproduce is checked by the column gate of §3.3, not by a pin. Re-pinning in answer to a red pin is forbidden (A §7, "Recreating the reference", lines 1648–1655). **Revision 1.5 (Ark, Zcode; ㊱):** `write_raw` writes `raw_fits.json.gz` with gzip's mtime in its header; the pinned bytes are integrity, the column gate is reproducibility, and a rerun's own `.gz` is expected to differ in bytes and is never compared with a pinned file (`write_raw` is unchanged). **Revision 1.6 (A4; Ark 17:58 and 18:00, Zcode 18:05, Johnny 17:54): the reference is made by fitting, decided by its object.** `--synthetic-only --from-raw` with `--out` is refused before any folder is made; without `--out` it is a diagnostic. The raw store's key carries no block name and a loaded store is not checked against block B (the four readings, with their lines, are in §3.3, "The reference is made by fitting, never by a re-read"); `is_the_pinned_store` is False when the pins or the file are absent, and gates the re-read comparison of §3.3's gate (㉜). Tests `test_S17_from_raw_with_out_refused_without_out_a_diagnostic` and `test_S17_is_the_pinned_store_is_a_condition`; each fails under its mutation (run for revision 1.6). **Revision 1.6.1 (Ark 18:30 and 18:32).** *Where a re-read's comparison outcome is visible:* `manifest["prerun_comparison_outcome"]` (beside it `prerun_comparison_outcome_3_parts` and `prerun_reread_from_saved_fits`), and in `synthetic_only.json` at `two_world_check.prerun_reproduction.comparison` (present only when a comparison was made; `outcome` beside it); for a re-read of a store that is not the pinned one both are empty (`None`, no `comparison`). *The ko1 count follows its twin:* `check_ko1_count` takes `pinned_store` as `check_prerun_reproduced` does; under `--from-raw` of a store other than block B's pinned one the count is not compared with the registered value and records no equality (`equal` None); `passed` is `None` for every re-read, as before, so no gate changes. Test `test_S17_ko1_count_reread_compared_only_for_the_pinned_store`. *`--arm --from-raw` is refused, not marked* (line 3385 of 1.6; §3.3, "What being a reference needs") |
| S18 | `out_dir_refusal` | refuses `--out` at or in **both** A's and block B's reference folders and on byte copies of either; **revision 1.2: and the two male references** (`synthetic_malecns_L_prerun/`, `synthetic_malecns_R_prerun/` under `connectome-seed-data/knockout_regrow/`, with their pins), as the male script's `protected_references` already lists A's, B's and both male folders. **Revision 1.3 (Ark M5, settled with Zcode), the wording:** A's reference and both male references are guarded by their path and recognised as byte copies by their pins together (a folder is a copy when at least one pinned-name file is present and every present pinned-name file equals its pin; A §7, lines 1637–1643; male `out_dir_refusal`, lines 2944–2974). Block B's own folder is guarded **by its path only** until the pre-run (its pins do not exist; the male script writes `B_PRERUN_SHA256 = None`, line 139); its pins are added in the revision after the pre-run, and from then on it is recognised by them as the others are |
| S19 | `write_committed`, `OUT` | `results/genome/c6/checks/knockout_regrow_block_b/`; the title; the line after the quoted §4 row naming A's literals (§4, D9); the header line of §5 |
| S20 | `--arm`, `private_run_dir` | an arm name that keeps block B's private folders apart, for example `flyvis65_blockB` |
| S21 | `WITHIN_FLY_NOTE`, the `TAU` comment | "about 2.7 of 40 cells"; the lattice text made generic |
| S22 | tests | copies of A's 17 label tests adapted to block B's reference, plus: the rc guard; 20/20 on both boards and the exact 0.5 of the No algebra; check 5 as a print; the seed assertion |

**The plan of the port: S1–S22 against the male CNS arm's script (revision 1.3; Ark, Zcode; open
points 5 and 6 of 1.2).** Revision 1.2 titled this table "S1–S22 re-checked against the male CNS
arm's script as it ran"; revision 1.3 keeps its content and reads it as **the plan of the port**:
each row states "male line → block B requirement". **D13 is kept:** block B's script is a copy of
A's, and the diff that is reviewed is against A's script; a row below says which male form is
ported into that copy, never that block B's file is the male file. **Numbering (revision 1.3;
Zcode, Ark):** male S-numbers are never reused in block B; block B's S16, S28 and S30 keep their
block-B meanings; every port from the male script is marked "(the male arm's SNN)". Revision
1.2's paragraph, as it stood: the male arm's
script (`results/genome/c6/checks/knockout_regrow_male_cns.py`, written in `ee380a1`, last changed
in `01d2d05`, LF sha256 `290ecb565759def6d11e3b76811635ce033a6b008461427ecede4704245e8e32` at
`01d2d05`, `e07e347` and HEAD; the script of both registered runs) is also a copy of A's script,
and it already solves several of the changes planned here, **for a 64-cell 8 × 8 block**. Line
numbers are of that file at `01d2d05` (unchanged to HEAD; revision 1.3: still unchanged at
`9b86839`, same LF sha256). "Solved" means a form block B's script
may port; the diff that is reviewed stays against A's script (D13 (i)); porting is not a change
of any value of this file.

| # | 1.2's status (solved by the male script?) | port: male line → block B requirement |
|---|---|---|
| S1 | form only | male S1 (a copy of A's) → block B's S1: its own copy of A's file and its own label test, still to be written |
| S2 | **yes** (the constant) | lines 74–80 (`A_REGISTRATION_SHA256_LF_AMENDED`, `A_REGISTRATION_SHA256_LF_FLYVIS65`; 1.2 wrote "70–80", the comment above them starts at 70) and `check_registered_constants` (line 567) → block B's S2: the same amended value, checked at run start |
| S3 | no | none → block-specific (L1–L5 × the eight) |
| S4 | no | none (the male arm keeps A's four quadrants) → block B's six strata, new |
| S5 | no | none → 4,185, block B's |
| S6 | no | none (the male tables are per lobe, male S8) → block B's table registered by its hash (§1.4) |
| S7 | form only | `check_block_and_mask` adapted to 2,961 / 3,025 / 64 (male S7) → block B's counts 40 / 5 / 8 / 4,185, plus block A's 64 in training |
| S8 | **yes, in form** | `check_block_print` (line 734), which prints the block after unsealing and stops on `NO_AUC_TEXT` = "BLOCK HAS NO AUC" → block B prints at run start (no seal), with 0 / 40 as the stop |
| S9 | **yes** | `check_n1_parity` (line 863), a printed value with the balance, "decides nothing", no stop → block B's S9 as it is |
| S10 | **yes, in form** | `check_auc_function` (line 912), one unbalanced 64-cell hand case (16 of 64) → block B's 40-cell case |
| S11 | form only | `uniform_perms` (line 960), `permutation(N_BLOCK)` → with `N_BLOCK` = 40 the same code draws `permutation(40)`; block B's seeds |
| S12 | **partly** | the no-checkerboard pre-check and the cap of 100 × 640 attempts per chain in `_rc_chains` / `rc_patterns` (lines 992–1047, `RC_CAP_FACTOR` line 340) → block B's pre-check and cap. **Not ported, block B's own:** the (5, 8) reshape and per-axis index ranges (the male code has `reshape(8, 8)` and `integers(8)`, `_rc_chains` lines 995 and 1008). **Not ported, a difference kept:** on a real block the male script prints "n/a (attempt cap reached: …)" and goes on (male D9 (i)); block B keeps D7's stop, and revision 1.3 adds the stop record (§3.2 (3), S39) |
| S13 | **partly** | `reserved_seeds` (line 1072), which reserves A's and B's seeds → block B reserves A's and the male arm's (S13) |
| S14 | **partly** (revision 1.5, Zcode: 1.3–1.4.1 said "no") | `board_y` (lines 1121–1125), the block labels of a world's board, ported by name (block B's script marks it `# port: male board_y (lines 1121-1125) -> S14`) → block B's worlds (§3.6) are otherwise block B's own |
| S15 | **yes, in form** | `precision_at_n_present` (line 1418); the generic "other N" AUC; the arm's own CSV column names → block B's S15 |
| S16 | **yes** (docstring) | `smallest_passing_auc` (line 1438), grid `k/(n_p n_a)` → block B's S16 (the docstring). The male "not readable" U (male S16, D8), which 1.2 left open, is ported by revision 1.3 as **S38 (the male arm's S16, its not-readable part)** |
| S17 | **yes** | A's revision-2/3 split and `_mech_renamed_32` not carried (male lines 95–96) → block B's S17, with what each pin covers (revision 1.3, M3) |
| S18 | **yes, in form** | `protected_references` / `out_dir_refusal` (lines 2936–2974; 1.2 wrote 2975, the blank line after), which refuse A's, B's (path only, `B_PRERUN_SHA256 = None`, line 139) and both male folders → block B's list, the same four, with B's pins once they exist (revision 1.3 wording, M5) |
| S19 | **partly** | `a_literals_line` (line 3223), the line after the quoted §4 row naming A's literals; `write_committed` in the male form → block B's S19; the debts S31–S33 change it |
| S20 | **yes** | `private_run_dir(arm, head)` (line 2930), keyed on the arm name → block B's arm name |
| S21 | **yes, in form** | the lattice text made generic (male S24; the `TAU` comment, lines 321–327) → block B's S21; the within-fly note is block B's ("about 2.7 of 40 cells"). **Revision 1.5 (Zcode):** the script now marks the port (`# port: male TAU comment, the lattice text made generic (lines 321-327; the male arm's S24) -> S21`) |
| S22 | form only | male T1, copies of A's 17 label tests (male §7.3) → block B's S22; the requirements S23–S39 add their own tests |

**Not planned by S1–S22, solved by the male script (revision 1.2's paragraph, as it stood):**
"open for block B (§10, "Revision 1.2", open points): male S28 (`p_S` printed with four decimals
and "[leg S decided by the count …]" when `n_deg` >= 1) and male S30 (`PRERUN_GIT_HEAD`,
`PRERUN_SCRIPT_SHA256_LF`, `prerun_provenance`: the head and script that made the pinned
reference, checked before any fit, "PRE-RUN PROVENANCE DIFFERS"). Under D10 (i) block B's
reference is made by one script and read by a later one (the revision after the pre-run sets
`PRERUN_*` in the script, so its hash changes), the case male S30 and male §3.3.1 (h) were
written for." **Revision 1.3 (Ark, Zcode; open point 4 of 1.2):** both are now requirements,
S36 (the male arm's S28) and S37 (the male arm's S30), below.

**Revision 1.2: the male arm's script debts, registered as requirements S23–S35.** Sources: the
retrospective `docs/retrospectives/2026-09-27-session-close.md` §5 ("Debts for block B's script",
lines 181–194) and §3 (lines 104–153); the male arm registration §11 (lines 1714–1733, the cp1252
break; 1784–1805, the blind review's findings; 1807–1845, the reviewers' reclassification,
commit `86d7288`; 1877–1879, the filter debt; 1881–1887, the debts) at HEAD `bbfa91b`;
`results/genome/c6/checks/knockout_regrow_male_cns/SEAL_BROKEN_NOTE.md`, `READING_NOTES.md`,
`RESULT.md`; the blind review `docs/notes/2026-09-27-knockout-regrow-male-cns-blind-review.md`
(§0 line 11, §C line 93, §D line 105, §E lines 111 and 115, "Not checked" line 184). Each row
names a test that fails if the requirement is not met. **No test here reads block B's cells of
the real bank:** every end-to-end test runs on a fixture bank or on a synthetic world, since a
run of the real arm on flyvis-65 would count block B, which D3 (ii) abstains from before the
registered run. **Revision 1.3** extends S25 and S27 in place and appends S36–S39: three ports
from the male script (S36, S37, S38, each marked with its male number) and one requirement of
block B's own (S39, the stop record). By the numbering rule above, no male S-number is reused. **Revision 1.5** appends S40, the port
of the male script's dirty-tree refusal of `--synthetic-only` (a form of the male code, which has
no S-number for it).

| # | requirement | what it pays (source) | test that fails if it is not paid |
|---|---|---|---|
| S23 | **UTF-8 at the top.** Before any other statement that can print, the script calls `sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")` and the same for `sys.stderr` (and the same for the tee's file handles, which are opened with `encoding="utf-8"`) | run 1 of the male arm stopped on `UnicodeEncodeError: 'charmap' codec can't encode character 'γ'` after unsealing (male ledger lines 1714–1733; retro §3, lines 104–112) | a subprocess runs the script's import and a print of A's quoted G row (it holds γ) with `PYTHONUTF8=0` and `PYTHONIOENCODING=cp1252:strict`, stdout redirected to a file: exit 0, and the file decodes as UTF-8 and contains γ |
| S24 | **`log()` cannot kill a run.** `log` writes to the tee's file first, then to the console inside a guard that catches `UnicodeError` and `OSError`, writes the line with `backslashreplace` instead, and counts the event (`log_output_errors` in the manifest); it never raises | male `log` (line 464) calls `print`, and `_Tee.write` (line 444) writes to the stream before the file, so a console error killed the run and lost the line (male ledger line 1731) | a unit test gives `log` a stream whose `write` raises `UnicodeEncodeError`: `log("γ")` returns, the tee file holds "γ", and the counter is 1 |
| S25 | **Real fits and verdict lines on disk before any print.** In the real arm, the raw fits (`raw_fits_real.json.gz`) and a `verdict.json` (the label, the verdict line, the quoted row, the A-literals line) are written and flushed to the private folder **before** the first print of the real block's table or verdict | male `_finish_real_arm` prints the real table (line 3902) before `write_raw` (line 3908); run 1's real fits were held in memory and lost (male ledger lines 1722–1724; retro §3) | a test on a fixture bank patches `log` to raise on its first call after the real fits: both files exist, and `verdict.json`'s line equals the one the unpatched run prints. **Revision 1.3 (Ark M4, settled with Zcode): extended to the synthetic step, in both modes** (`--synthetic-only` and the registered run): the synthetic step's fits and outputs are written to disk before the first print of its tables. Male fact: `print_synthetic` (line 3764) comes before `write_synthetic_outputs` (line 3776) in `run_synthetic_only`, and in the real arm's synthetic step `print_synthetic` (line 3845) comes before `write_synthetic_outputs` (lines 3846–3848). Added test: in each mode, on a fixture world set, `print_synthetic` (or `log`) is patched to raise on its first call after the synthetic fits; the synthetic outputs (`raw_fits.json.gz`, `synthetic_only.json`, `synthetic_worlds.csv`) exist and hold every world. Under the male order this test fails (nothing is written) |
| S26 | **An ASCII end-to-end rehearsal.** A test runs the end of the real-arm path (the table, the quoted §4 row, the A-literals line, the verdict line, `write_committed`, the sums) on a fixture bank in a subprocess with `PYTHONUTF8=0`, `PYTHONIOENCODING=ascii:strict` and stdout redirected to a file | "the tests never ran the end of the real arm under a strict encoding" (retro §3, lines 105–107) | the rehearsal exits 0; `RESULT.md` exists and contains A's quoted G row with γ in UTF-8; `SHA256SUMS.txt` verifies (S29). Under this setting A's and the male `log` (a bare `print` to the console first) raise on γ, as the male run 1 did |
| S27 | **The run's record of prior real-arm runs is read at run time.** There is no seal in block B (its content is public, §1.5), so the male `SEAL_RECORD` constant is **not** carried. Instead the script writes a marker file in the private folder when it starts the real arm; at start it lists every earlier folder of block B's arm under `connectome-seed-data/knockout_regrow/` holding that marker, prints them with the scope searched ("searched: <root>, folders `<arm>_*`; N found"), and records the list in the manifest. `RESULT.md` prints that line; it never prints "intact" or any status the run cannot measure. **Revision 1.3 (Ark, Zcode; closes open point 7 of 1.2 and Johnny's edit 2): three outcomes, each printed with the scope searched:** (a) "root does not exist: <root>"; (b) "root exists and cannot be read: <root> (<error>)"; (c) "root read: <root>, folders `<arm>_*`; N found" (N = 0 included). (a) and (b) are not written as "0 found". This is S34's rule applied to the search: a search that matched nothing because it could not look must not look like a measurement of zero. **S27 runs in the real arm only** (revision 1.6; Ark, Zcode): `find_earlier_runs` is called under `--arm` only (line 3365 at `b810ecb`), and `--synthetic-only` sets `earlier = None` (line 3383 at `b810ecb`) and searches nothing | male `RESULT.md` line 3 "Seal record: intact." from a constant (`SEAL_RECORD`, line 183) after run 1 had unsealed; "a claim the writer cannot measure", class fix in block B (male ledger lines 1784–1791, 1810–1814; retro §3, lines 146–149) | a fixture private root with one earlier folder holding the marker: the printed line names it; with none: "0 found" and the scope; a grep test finds no string `"intact"` in the script's output text constants. **Revision 1.3:** a missing root prints outcome (a) and a root the process cannot list (patched `iterdir` raising `PermissionError`) prints outcome (b); in neither case does the line or the manifest hold "0 found" |
| S28 | **The command's environment in the manifest.** The manifest records `sys.argv`, `sys.stdout.encoding`, `sys.stderr.encoding`, and the values found of `PYTHONUTF8`, `PYTHONIOENCODING`, `PYTHONHASHSEED` and the four BLAS thread variables (found before `setdefault` and in effect) | the male manifest records only the thread variables (line 532); `PYTHONUTF8=1` of run 2 is not verifiable from the outputs (blind review line 184; male ledger lines 1800–1801, 1842–1843) | a test sets `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` in a subprocess, builds the manifest: both appear with those values; unset, they appear as `null` |
| S29 | **`SHA256SUMS.txt` written last.** In every folder the script writes, the sums are written after the last log line, after the tee is closed; nothing is written to that folder afterwards, and the sums cover `stdout.log` | male `write_sha256sums(private)` (line 3940) runs before `write_committed` and the "wrote …" and "wall-clock" lines, so the `stdout.log` entry does not verify (blind review line 93; male ledger lines 1797–1799, 1819–1821) | after the rehearsal (S26), every entry of every `SHA256SUMS.txt` the run wrote verifies, `stdout.log` included. **Revision 1.4:** a run stopped before the end writes no sums, which S39 uses as a second sign of the stop. **Revision 1.5 (OPEN 3, decided on the reviewers' votes; OPEN 4, Ark, Zcode).** (a) *The literal reading is kept:* the committed folder `OUT` (`results/genome/c6/checks/knockout_regrow_block_b/`) gets its own `SHA256SUMS.txt`, written last as the private folder's is. This is a **delta from A** (A's committed folder had none). `.gitignore` does not cover the file, so it is committed with the registered run's artifacts. **Revision 1.6 (Ark, Zcode; ㊹):** the sums in `OUT` cover the committed folder's files and are **not** a reference pin: they are never compared with `PRERUN_SHA256` (`check_prerun_files` reads only `PRERUN_DIR/SHA256SUMS.txt`; `OUT` is not among `protected_references`). (b) *The general form:* **the folder of any run that did not complete has no `SHA256SUMS.txt`**: a failed two-world check, check 4 ("PRE-DATA TABLES DIFFER"), a block with no AUC (check 3), a provenance failure (S37) and the attempt cap (S39) alike. One sign, not special cases: `main` writes the sums only after `_run` has returned, and every stop is a `sys.exit` inside `_run` or before any folder is made (checked for revision 1.5 in the code; no exit path writes sums first) |
| S30 | **A conditional diagnostic sentence carries its condition.** Every registered text printed as a diagnostic either prints only when its condition holds or states the condition in its own words. Block B has no lobe comparison, so the male S0 sentence has no copy here; the class applies to block B's own conditional texts: the line naming A's literals (§4, D9), the D8 outcome note ("a second possible source of U on this block": printed beside a U only), N1's `p_P` beside a U, the "failed fit or rank limit" reading (beside a failed fit only) | the male S0 text "the split comes from the instrument's response …" was printed where no split by reading occurred; block B's writer "carries the condition in the sentence" (male ledger lines 1834–1837) | a table-driven test of each conditional text over the four labels on fixture outcomes: printed only under its condition, or its text contains the condition's clause |
| S31 | **§3.5's columns in `RESULT.md`.** Every quantity §3.5 says is printed (the six strata means, precision at `n_present`, the 9 mirror partners' `p_exist`, the AUC on the other 31, the per-type rows for the 13 types, the 20 permuted-block `ceiling_full`, the fixed λ = 1 diagnostic, `D(N1 logit)`, N1's `p_P` beside any U) has a column or a line in `RESULT.md`, not only in the log and `summary.json` | male `RESULT.md` has no column for §3.5's mirror, other-61 and quadrant values; "§3.5's statement is wider than the artifact" (blind review line 115; male ledger lines 1803–1804, 1825–1828) | on the rehearsal's `RESULT.md`, a list of the §3.5 items, each mapped to its header string, is found; the values equal `summary.json`'s |
| S32 | **The synthetic U-rule paragraph follows block B's own U reading.** The "U rule" paragraph of `RESULT.md` prints the γ of block B's own U worlds against block B's own limits, computed from block B's synthetic step, and says whether they lie in A's position ("at γ\*_P") or not; it does not print A's reading of a threshold U as block B's | male `RESULT.md` lines 194 and 974 print A's reading of a threshold U, which the male §4.1 (5) says does not hold there (male ledger lines 1801–1803, 1822–1825; `knockout_regrow_male_cns.py` line 2835) | a fixture synthetic step whose U worlds lie below γ\*_P: the paragraph states that and does not contain A's literal "sit at γ = 0.6 = γ\*_P" as a description of block B |
| S33 | **No duplicate `auc_N1` column.** `per_shuffle.csv`'s header has unique names | male `write_per_shuffle_csv` (line 2985) writes `auc_N1` explicitly and again from `PRED_KEYS` (which ends with `"N1"`, line 307) (blind review line 105; male ledger line 1805) | the rehearsal's `per_shuffle.csv` header: `len(set(cols)) == len(cols)` |
| S34 | **Every filter states its denominator.** Every count the script prints or writes over a filtered set is written "k of n", n the number of rows the filter matched; a filter that matches no row stops with "FILTER MATCHED NOTHING: <key>" instead of returning 0. The same rule binds counts written into this file's later revisions (§3.9). **Revision 1.3:** S27's search of earlier runs is an instance of this rule (its three outcomes) | a filter on `BF:1` against the CSVs' `BF_1` returned 0 and looked like a measurement (Ark, 2026-09-27 14:01 UTC; male ledger lines 1877–1879) | a unit test counts over a fixture table with the key `BF:1` where rows say `BF_1`: it raises; with the right key it returns "k of n" with n equal to the matched rows |
| S35 | **Fenced drafts inside a registration are marked.** Any fenced block in this file or its later revisions that holds registration text (a draft of an amendment, a section) is introduced by the line "**Fenced draft, not a section.**", and a heading inside a fence is never counted as this file's heading | the male arm's blind reviewer read Appendix A's fenced "## 13. Amendment 1" as a section of the registration (blind review line 11; male ledger lines 1843–1845) | a test reads this registration, finds every fence opening (```` ``` ```` or `~~~`) and asserts the marker line within the two lines before it; a fixture with an unmarked fence makes the checker fail (this file has no fence at revision 1.2, so the fixture case is what shows the test can fail) |
| S36 | **(the male arm's S28) The `p_S` mark (revision 1.3; Ark, Zcode; open point 4 of 1.2).** When `n_deg` >= 1, `p_S` is printed with four decimals followed by the mark "[leg S decided by the count: n_ge = {n_ge} of {n_valid}]", everywhere it is printed (the verdict line, the bank print, the synthetic table, the `RESULT.md` bank table); when `n_deg` = 0 it is printed as A prints it (two decimals, no mark). No decision reads `p_S`: leg S stays `n_valid >= 1 and n_ge == 0` (§3.2) | male `P_S_MARK` (line 421) and `p_s_text` (lines 1788–1796); male registration S28 (line 1324); A printed `p_S` without saying that the count decides, which on a bank with degenerate shuffles reads as a p-value near the cut | as male T12 (`test_T12_p_S_print`, `test_knockout_regrow_male_cns.py` line 984), on block B's fixture: with one degenerate shuffle the verdict line and the `RESULT.md` bank table hold "p_S = 0.0101 [leg S decided by the count: n_ge = 0 of 98]"; with none, "p_S = 0.01" and no "[leg S"; A's printing fails the first assertion |
| S37 | **(the male arm's S30) Pre-run provenance, checked before any fit (revision 1.3; Ark, Zcode; open point 4 of 1.2).** The revision after the pre-run registers `PRERUN_GIT_HEAD` and `PRERUN_SCRIPT_SHA256_LF` beside block B's pins. **`PRERUN_SCRIPT_SHA256_LF` is the LF sha256 of the script that wrote the reference** (read from the reference's `synthetic_only.json` manifest after `check_prerun_files` passes); **the reading script's own hash is intentionally different**, because under D10 (i) that revision writes `PRERUN_*` into the script, so the script that reads the reference is not the one that wrote it. Before any fit (in the registered run and in any `--synthetic-only` run that reads the reference), `prerun_provenance` compares the reference's manifest with the two registered values and stops with "PRE-RUN PROVENANCE DIFFERS" on a mismatch; both codes (the reference's and this run's) are printed, recorded in the manifest and in `RESULT.md`'s header ("pre-run made by …; this run by …"). A difference between the writing script's hash and the reading script's hash is not a mismatch. **Revision 1.6 (A4; Ark 18:00):** a reference whose manifest carries a non-null `not_a_reference` (an `--allow-dirty` run, S40) is refused by `prerun_provenance` (passed False, so the run stops with "PRE-RUN PROVENANCE DIFFERS" before any fit), whatever its pins and head: an `--allow-dirty` folder can never be pinned and pass. Test `test_S37_reader_refuses_a_not_a_reference_folder` (its files verify, the reader refuses; it fails with the refusal removed). **Revision 1.6.1 (Ark 18:32):** since `not_a_reference` is set for every run not in the registered form as well (S40, revision 1.6.1), the reader refuses such a folder too: being a reference needs the registered form and a clean committed tree. `test_S40_non_registered_form_is_not_a_reference`: a clean-tree smoke folder pinned by its own sums verifies and is refused | male `PRERUN_GIT_HEAD`, `PRERUN_SCRIPT_SHA256_LF` (lines 118–127), `prerun_provenance` (lines 2109–2137), its stops (lines 3753, 3836); male registration S30 (line 1321) and §3.3.1 (h) (line 799) | as male T14 (`test_T14_S30_prerun_provenance`, line 1166), on a temporary reference: a manifest naming the registered head and script passes although the running script's hash differs; a manifest naming another script stops with "PRE-RUN PROVENANCE DIFFERS" before the first fit (a patched fit function that raises is never called) |
| S38 | **(the male arm's S16, its not-readable part) The "not readable" U (revision 1.3; Johnny edit 1, Ark, Zcode; open point 3 of 1.2).** On the real block, `smallest_passing_auc is None` gives a U of its own kind, "not readable", with block B's own text ("not readable: leg P cannot reach p_P <= 0.01 on this block (n_present = {k} of 40)"; the male text says "of 64"). It takes precedence over R, W and G alike, is never renamed by the U rule, is not a threshold U, and is counted apart wherever U kinds are counted. The condition is the object `smallest_passing_auc is None`; no threshold on `n_present` is written anywhere (§3.2). The 0 / 40 stop of check 3 stays | male `NOT_READABLE_REASON` (lines 407–411), `read_label(..., readable=spa is not None)` (line 1627), `u_kind` (line 1672), `read_label` (lines 1688–1730); male registration S16 (line 1308), D8 (line 1474); A's `evaluate_bank` calls `read_label(rows)` with no such argument (`knockout_regrow.py` line 1099) | as male T8 (`test_T8_not_readable_and_no_auc`, line 789), on 40 cells: with `n_p` = 1 and rows that would read R (and again W, and G), the label is U, its first reason starts with "not readable", `u_kind` is `not_readable`, and the U rule's rename leaves it unchanged; with `n_p` = 2 and the same rows, the ordinary branch is read. With A's `read_label(rows)` the first case reads R, so the test fails. **Revision 1.4 (Zcode): the literal.** The test asserts the reason's text equals block B's literal, "not readable: leg P cannot reach p_P <= 0.01 on this block (n_present = 1 of 40)", so that a verbatim copy of the male `NOT_READABLE_REASON` (lines 410–411, "(n_present = {k} of 64)") fails; where S38 says "counted apart", the carrier is §3.5 (revision 1.4) |
| S39 | **The attempt-cap stop leaves a record (revision 1.3; Ark, Zcode; open point 2 of 1.2).** When a row-and-column chain reaches the cap of 100 × 640 attempts (D7, S12), the script, before it exits, writes `stop_record.json` into the run's own folder (the real arm's private folder; the `--out` folder in `--synthetic-only`), flushed and closed, holding the stop message, the chain index, `succ`, `att`, the arm and the git head, and then stops with the message of §3.2. A run that never started has no such file; a stopped run has it | D7's stop was only a log line, so from outside a stopped run could not be told from a run that never started (Ark, Zcode, review of 1.2) | a fixture 5 × 8 pattern that admits a swap in only one position and a cap lowered by patching `RC_CAP_FACTOR`: the process exits non-zero, `stop_record.json` exists in the run folder and its `chain`, `succ`, `att`, `arm` and `head` equal the values printed in the stop message; a version that only logs fails the existence assertion. **Revision 1.4 (Ark, Zcode): a stopped run writes no sums and never becomes a reference.** Since `SHA256SUMS.txt` is written last (S29), a stopped run's folder has no `SHA256SUMS.txt`; that absence is a second sign of the stop, independent of `stop_record.json`, and a stopped `--synthetic-only` (pre-run) folder never becomes block B's reference. Added to the test: after the stop, the run folder holds no `SHA256SUMS.txt`. **Revision 1.5 (OPEN 2, kept):** seen from outside, a `--synthetic-only` run is in one of three states: no folder (legitimate without `--out`: such a run writes nothing, A §7, and its stop message says "none (the run has no folder)"); a folder with `stop_record.json` and no sums (stopped); a folder with sums (completed). **Revision 1.6 (Ark, Zcode):** these states say whether a run **completed**; whether a folder may be a reference is its manifest's `not_a_reference`, and one does not follow from the other: an `--allow-dirty` run completes and has sums, but is not a reference (S40). That is a fourth state: a folder with sums whose manifest carries `not_a_reference`; the reader refuses it (S37, revision 1.6). **Revision 1.6.1 (Ark 18:32):** being a reference needs the registered form (no smoke option, `--starts 10`) and a clean committed tree; the fourth state is reached by an `--allow-dirty` run and by any `--synthetic-only --out` run not in the registered form, clean tree or not (S40, revision 1.6.1) |
| S40 | **(revision 1.5; Ark, Zcode; OPEN 5) A full `--synthetic-only` run refuses a dirty tree unless `--allow-dirty`.** A comparable `--synthetic-only` run (`--starts 10`, no smoke option) on a tree with uncommitted changes under `results/genome/c6/` or `docs/plans/` stops with "REFUSED" before its folder is made; with `--allow-dirty` it runs and is marked "NOT A REFERENCE" in the log, the manifest (`not_a_reference`) and `SYNTHETIC.md`. **A tightening relative to A:** A's `--synthetic-only` recorded the tree state; B refuses. It serves D10 (i): block B's reference is made from a committed head | the port of the male script's dirty-tree refusal (`knockout_regrow_male_cns.py`, `run_synthetic_only`, lines 3721–3727 at `01d2d05`; a form of the male code, not a male S-number); before revision 1.5 the port was in block B's script as an open item | `test_S40_dirty_tree_refused_unless_allow_dirty`: on a fixture with a dirty tree the run exits with "REFUSED" and no folder; with `--allow-dirty` the three carriers hold the mark; a clean tree carries none. Removing the refusal, or the mark, makes the test fail (both mutations run for revision 1.5). **Revision 1.6.1 (Ark 18:32): the mark covers the form as well.** `not_a_reference` is set when the tree is dirty **or** the run is not comparable (`dirty or not comparable`; 1.6 had `dirty and comparable`), with its actual cause (`NOT_A_REFERENCE_TEXT` for an `--allow-dirty` run, `NOT_A_REFERENCE_FORM_TEXT` for a smoke option or `--starts != 10`, naming the uncommitted tree too when there is one); for a comparable run it equals `dirty`, so the pre-run is unchanged. Being a reference needs the registered form and a clean committed tree. `test_S40_non_registered_form_is_not_a_reference`: on a clean tree a smoke run with `--out` carries the mark in its manifest and `SYNTHETIC.md`, and the S37 reader refuses it; `--starts 3` and a dirty smoke run carry it too. With the token reverted the test fails (mutation run for revision 1.6.1) |

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

Not part of this registration. **Revision 1.1 said:** "A §8's male-CNS arm has not been built."
**Revision 1.2, the state since then:** the male CNS bank was built (`5860619`), A §8's promise to
pin it was kept by A's Amendment 1 (`6fff1e4`), and the male CNS arm was registered
(`docs/plans/2026-09-26-knockout-regrow-male-cns-arm-registration.md`, revision 1.3) and run on
**block A** (run 2 at head `e07e347`; outputs in `results/genome/c6/checks/knockout_regrow_male_cns/`,
to be read with `SEAL_BROKEN_NOTE.md` and `READING_NOTES.md` there). Its verdicts are in that
folder and are not restated here. It did not touch block B. Revision 1.1's rule stands: if a
male arm is ever run on block B, its builder must also map L1–L5, and this file is amended to pin
the built bank. (The male arm on block A was registered as a file of its own beside A's
amendment; whether a male arm on block B would follow that form is not decided here, §10
"Revision 1.2", open points.) Whether the built male bank places L1–L5 was not checked for this
revision (§11).

**Revision 1.3 (Ark, Zcode; open point 7 of 1.2): a male arm on block B is a separate registration
file, not an amendment of this file.** The part of revision 1.1's rule quoted above that says
"this file is amended to pin the built bank" is withdrawn on the reviewers' vote; §1.1's eight
pins are not extended. That the builder must map L1–L5 remains a condition of any such arm, and
belongs to that registration.

## 9. Lessons applied (delta on A §9)

| lesson | where here |
|---|---|
| a, selection after the data | the choice after block A's verdict is named (§1.5); `ceiling_full` is named as not a reason (§1.2); the candidates and criteria predate block A's run |
| b, a null that cannot see the other world | block B's own worlds (§3.6) |
| c, a criterion written after the finding | none: every gate and reading rule is revision 3.4.1's (§4) |
| e, read the object | §1.3 names every row removed and every channel left, block A's board included |
| g, denominators | 40 cells, `n_present`/`n_absent`, 4,185 training cells, 40 / 40 inferable, 9 mirrors |
| retro 2026-09-27 §4 (revision 1.2): scope and denominator; census scope and band; "not recomputed" from the log; callers from the graph | §3.9; S34 |
| retro 2026-09-27 §3 (revision 1.2): the cp1252 crash after unsealing; outputs that claim what the writer cannot measure; sums before the last log line | S23–S29 (§7) |
| male ledger, after the Q2 note (revision 1.2): "instrument weaker" not separated from the draw | §6, "Less power" |
| review of revision 1.2 (revision 1.3): a stop and an empty search must be told from "nothing happened"; a rule ported by its object, not by a count | S27, S34, S38, S39 |

## 10. Decisions for review (reviewers, then Mike)

The body is written with the recommendation of each row.

| # | question | options (what each changes) | recommendation |
|---|---|---|---|
| **D1** | Which block B | **B-motion** (L1–L5 × block A's eight sources, 40 cells): passes K1–K4 by its name rule; it is candidate B restricted by candidate B's own biology, **not one of the note's rules verbatim**. **B-L123** (24 cells): only the L types whose targets the note states; less power. **B-full** (260 cells) and **C** (114): fail K3 by shape, so a failure cannot be read as "no grammar". **Defer:** a new candidates note on the 65-type grid; a session of selection and review | B-motion |
| **D2** | How much of §1.4 is printed before data | (i) the full endpoint table, as A §1.4: with A §1.4 it gives block B's column counts by subtraction. (ii) inferability, minima, mirrors and the table's sha256; the script prints the table at run start and checks the hash. (iii) nothing before data: K3 unverified until the run | (ii) |
| **D3** | Block B's own pattern before the run | (i) counted by name after this choice is committed, three times, as block A's board was, and registered; check 3 then compares with it; §0's open questions (degree channel, rank) are settled before data, and the authors see the answer. (ii) **a choice not to count it before the run** (revision 1.1, Johnny: not blindness, which is not achievable, since `offsets.csv` is committed and the note printed an upper bound of 32; §1.5): check 3 prints the counts and stops only on "no AUC"; the training present count is printed, not checked; the abstention is declared, not enforced | (ii) |
| **D4** | Worlds' polarity on L3–L5 | (i) fixed L3 +1, L4 −1, L5 +1: one layout per board, so the one-value-per-board check of `smallest_passing_auc` can hold. (ii) drawn per world: the layout varies by world, so that check fails by construction and would have to be registered per world (a gate change). (iii) all +1: columns 4 of 5 against 1 of 5 | (i) |
| **D5** | `z'_B` and the No assertion | (i) A's `z'` on the targets (exact orthogonality, classes of 2), `z'` = (+1, +1, −1, −1, +1) on L1–L5, the assertion relaxed to the targets, with §3.6's algebra. (ii) make the sources orthogonal too, which needs an even number of sources, so it changes the block of D1 | (i) |
| **D6** | Check 5 (N1 parity identity) | (i) a printed value, no stop. (ii) kept as a stop: it fails on every non-degenerate 5 × 8 block (§0), so the real arm could never run | (i) |
| **D7** | Printed-only adaptations | strata for quadrants; precision at `n_present`; the other 31 cells; the row-and-column null on 5 × 8 with 640 swaps, an attempt cap of 100 × 640 per chain that stops the run with a message (the harness's pattern, `harness.py:881–883`; revision 1.1, Ark and Zcode), and a pre-check that prints "n/a" for a pattern with no checkerboard. **Revision 1.3 (Ark, Zcode):** the stop is kept and writes a stop record file first (S39). Without a cap A's swap loop has no end; without S12 it would fail earlier, on the reshape. The cap stops the whole run although the variant decides nothing: the alternative is to print "n/a (cap reached)" and go on, which keeps the run but reports a truncated null | as written (stop) |
| **D8** | U and the degree channel | (i) U's label and text unchanged; N1's own `p_P` printed beside U; the outcome note names the additive channel. (ii) a new U reason, "N1 alone passes leg P", on the verdict line: changes a verdict-line string, so it needs its own review and a test | (i) |
| **D9** | A's literals in the quoted §4 rows; "failed fit" | (i) quote A's rows verbatim, then a printed line naming A's literals (64/64; the pre-run U worlds; "the block is rank 1"); "failed fit" read on block B as "fit failure or rank limit, not separated". (ii) restate §4 in this file with block B's literals: a new text of a reading rule, reviewed as such | (i) |
| **D10** | Order of work | (i) commit the script and this draft; the pre-run from that committed head on Mike's word; a revision registering the values read from the pinned reference; review; the registered run. Block B's reference then has a producer in git. (ii) A's D11 order (pre-run before commit): repeats the provenance gap of A §3.3 | (i) |
| **D11** | Joint reading with block A | (i) each block alone, A's G stands, no correction, `RESULT.md` names block B as the second block tried after A's G. (ii) a correction over two blocks (for example `P_R` = 0.005): changes revision 3.4.1's gates | (i) |
| **D12** | Instrument | (i) the pinned CPU harness, as A: the same instrument, about 4.5 h of wall time. (ii) the GPU instrument of `74de040`: separate and unreviewed; by A §7 it needs its own registration and synthetic worlds | (i) |
| **D13** | Script form | (i) a new file, a copy of A's, reviewed as a diff against it; A's file untouched. (ii) a `--block` flag in A's file: the file that A's run and blind review cite changes (A stays reproducible from `74de040`). (iii) import A's module and override its constants: fragile, since `BLOCK`, `MASKS`, `MIRROR_IDX`, `Z_BLOCK`, `ZPRIME` and `NONBLOCK_CELLS` are computed at import | (i) |
| **D14** | Seeds | as §3.7 | as written |
| **D15** | File date (revision 1.1) | `2026-09-26-…` (the name of revision 1, commit `d6e3759`; the local day at +07:00) vs `2026-09-25-…` (the UTC day of drafting, per the GLOSSARY's date-time convention: the §1.4 scratch scripts are stamped 2026-09-25 20:12 and 20:14 UTC) | `2026-09-25-…`, renamed with `git mv` in revision 1.1; as the knockout registration's D12 decided the same question and as the male-CNS builder draft's D14 does (that draft is renamed to `2026-09-25-…` in the same working tree). No other file of the repository referred to the old name (grep, revision 1.1) |

### Revision 1.1: the reviewers' pass on revision 1 (2026-09-26)

Revision 1 (commit `d6e3759`) was reviewed in the DPC Research chat on 2026-09-26. The votes and
the edits are as CC's message to the drafting agent relays them; the chat is not in the
repository. Zcode also recomputed, independently: the endpoint table's sha256 (exact match), 40 /
40 inferable, the minima 4 and 9, the 9 mirrors, the option sizes 260 and 114, both algebras of
this draft (the 5 × 8 balance and the No world's exact 0.5), and the seeds.

| reviewer | time (UTC) | vote |
|---|---|---|
| Johnny | 04:57 | yes, with edits |
| Ark | 05:00 | yes, with edits |
| Zcode | 05:08 | yes, with edits |

| # | edit | asked by | applied in revision 1.1 |
|---|---|---|---|
| 1 | D3 and §1.5: "unread before the run" is a choice not to count, not achievable blindness (`offsets.csv` is committed; the note printed an upper bound of 32) | Johnny | yes: §1.5 ("Block B's content cannot be kept blind"), D3 (ii) |
| 2 | Selection after data at the level of the block choice: the block is chosen after block A's G, and B-motion is a narrowing invented in this draft, not a line of the note; stated besides "B's cells were in training" | Johnny | yes: §1.2 (a paragraph under the rule; "What the choice does not rest on"), §1.5 ("What this compromises") |
| 3 | The eight targets' provenance: candidate B's paragraph names 7 of the 8 (it has Tm20 and not Mi4); the carrier of the set is block A's source list | Zcode | yes: §1.2 (the rule's paragraph, the option table, "Chosen"), the header's drafting record; checked against the note, lines 81–83 |
| 4 | Mirrors as a named risk in §6: 9 / 40 against 5 / 64, five partners named present by the key, no direct channel for the registered predictors | Johnny | yes: §6 |
| 5 | `n_out_entries`: the column itself, with public counts, already bounds the in-block row count; the endpoint table is not needed for that | Zcode | yes: §1.5, read declaration |
| 6 | `rc_patterns`: an attempt cap with a stop message, on the pattern of `harness.py:883` (cap = 100 × target), not only a no-checkerboard check; A's `reshape(8, 8)` / `integers(8)` fail on 5 × 8 before any hang | Ark, Zcode | yes: §3.2, D7, S12. The error at the reshape is `ValueError`; `IndexError` comes from `integers(8)` once the reshape is fixed (both checked on numpy 2.2.6). The cap line is `harness.py:881`, the loop condition line 883 |
| 7 | Date: rename to `2026-09-25-…` with `git mv`, recorded as a D item | reviewers (as relayed) | yes: D15, header; the in-file dates of revision 1 ("2026-09-26" in §1.1, §1.4, §3.7) corrected to the UTC day |
| 8 | This table of votes and edits | CC's request, from the review | yes |

### Revision 1.2: A's pins after Amendment 1, the male arm's script, and its debts (2026-09-27)

Drafted 2026-09-27 UTC by a CC subagent after Mike's word (DPC Research chat, 14:31 UTC, as
relayed by CC). Not reviewed, not committed. Nothing was fitted, run or read from the bank. No
gate, cut, reading rule, block, grid, seed of block B or D-row recommendation changed; every
change below adds a pin, a requirement, a statement of scope or a fact dated after revision 1.1.

| # | change | where | source |
|---|---|---|---|
| 1 | Header: status "revision 1.2: DRAFT … not reviewed, not committed"; the history of 1.1 kept, with its commit `8591491` named | header | `git log --follow` of this file (`d6e3759`, `8591491`) |
| 2 | A pinned as revision 3.4.1 **with Amendment 1**, LF sha256 `fc415056…`; `409184de…` kept as the text of A's verdict; what Amendment 1 changed and that it changes only S2's pin for block B; A's lines 1–2,495 byte-identical; `quote_row` / `quote_section` unchanged (R 1325, W 1326, G 1327, U 1328) | header ("What this file is", "What Amendment 1 changed"); §4 | `git show 6fff1e4`; `git show 01d2d05` (`knockout_regrow_male_cns.py` lines 74–75); male arm registration §9.3 (lines 1520–1570) and D11 (line 1477), which name block B's S2 and header as "to be updated by a revision of B"; recomputed (the hash table below) |
| 3 | S2: the pinned value `fc415056…` and the constant names | §7, S2 | as item 2 |
| 4 | "What it is not": block B does not test averaging; question (ii) stays paused | §0 | retro §5 (lines 170–177, 199–200); `backlog.md` via `bbfa91b`; male arm §5 caution |
| 5 | Seeds: the male arm's seeds (92000–92999) join the untouched list and the reserved set; no block-B seed changes; the 91xxx grep repeated | §3.7; S13 | `knockout_regrow_male_cns.py` lines 345–353 at `01d2d05`; A §13 item 2 |
| 6 | S18: the two male reference folders added to the refusal list | §7, S18 | `knockout_regrow_male_cns.py` lines 97–98, 2936–2941 |
| 7 | S1–S22 re-checked against the male script: which are solved in form, which are not (S12's reshape and indices), one difference (the cap on a real block), and two male items not planned here (male S28, S30) | §7, table after S22 | `knockout_regrow_male_cns.py` at `01d2d05` (LF `290ecb56…`); male arm registration §7.2 (lines 1289–1324), D9 (line 1475), D8 (line 1474) |
| 8 | The 13 debts registered as S23–S35, each with a test that can fail | §7 | retro §5 lines 181–194; male ledger lines 1714–1733, 1784–1887 (`e07e347`, `86d7288`, `46365e7`); the blind review note; `SEAL_BROKEN_NOTE.md`, `READING_NOTES.md` |
| 9 | §3.9, the retro's rules of counting and record | §3.9; §9 | retro §4 lines 155–166 |
| 10 | "Less power" scoped as leg-P arithmetic, not an instrument measurement; no comparison of block B's curves or limits with A's as numbers | §6 | Q2 note §0, §3.3, §6; male ledger lines 1854–1864 (`46365e7`) |
| 11 | §6's and §8's male-arm statements brought up to date (built, amended, run on block A; not on block B); §7: the GPU instrument now registered and validated (D12 unchanged); the command's environment | §6, §7, §8 | retro §1 (lines 24–63); commits `5860619`, `6fff1e4`, `e07e347`, `0286ae1`, `e50bf74`, `1ad6155`, `0c7a67b` |
| 12 | §9 lessons: three rows | §9 | as items 8–10 |
| 13 | §11: two items | §11 | this revision |

**Hashes written in revision 1.2 and how each was recomputed** (Git Bash, 2026-09-27 UTC; LF
bytes: each blob piped through `tr -d '\r'`, which gave the same value as the raw blob in every
case, since the blobs are stored with LF):

| value | object | command |
|---|---|---|
| `fc41505690365ff6d82fa618b00b482cc992bb36d708ed3b6fbbe6f54f96dbec` | A's registration at `6fff1e4` (and at HEAD `bbfa91b`, and the working tree) | `git show 6fff1e4:docs/plans/2026-09-24-knockout-regrow-registration.md \| tr -d '\r' \| sha256sum` |
| `409184dead0a8f9b971bd4b480043725d4a0d1a3c53c20c35734a944a63facd6` | A's registration at `74db080` | `git show 74db080:docs/plans/2026-09-24-knockout-regrow-registration.md \| tr -d '\r' \| sha256sum` |
| `290ecb565759def6d11e3b76811635ce033a6b008461427ecede4704245e8e32` | the male arm's script at `01d2d05`, `e07e347` and HEAD | `git show <commit>:results/genome/c6/checks/knockout_regrow_male_cns.py \| tr -d '\r' \| sha256sum` (at `8531c6d` the same command gives `1b952ca6…`, at `ee380a1` `745f19a7…`) |

The byte identity of A's first 2,495 lines and the `quote_row` line numbers were checked by a
scratch script (`PYTHONUTF8=1`, `tools/.venv`) on the two blobs; it is not committed.

**Open points for the reviewers (not decided by this revision).**

1. **Which text S2 checks.** The male arm's D11 (line 1477) and §9.3 offered block B two ways:
   pin the amended hash, or read A from git at `74db080`. Revision 1.2 writes the first (as the
   male script does); the quoted text is the same either way (item 2).
2. **The attempt cap on the real block.** Block B's D7 recommends a stop; the male arm chose
   "n/a (attempt cap reached: …)" and goes on (male D9 (i), line 1475), because a stop on the real block
   would come after the seal was broken. Block B has no seal, so the male reason does not carry
   over, but the two arms now differ. D7 is kept as written.
3. **A block on which leg P cannot pass.** With few present cells (for example 1 of 40, where the
   permutation null gives `p_P` >= 1/40 > 0.01), `smallest_passing_auc` is `None`. The male arm
   registered a "not readable" U for this (male S16, D8); block B's revision 1.1 stops only at 0
   or 40 present (§3.4, check 3). Whether block B adds a rule is a choice of the reading, not made
   here.
4. **Male S28 and S30** (the `p_S` mark when `n_deg` >= 1; the pre-run's provenance and the
   `--from-raw` check). Under D10 (i) block B's reference is read by a later script than the one
   that made it, the case male S30 and §3.3.1 (h) cover. Not added as requirements here.
5. **The base of block B's script** (D13 (i): a copy of A's, reviewed as a diff against it). The
   male script already carries many of S1–S22 and none of S23–S35. Whether block B is written from
   A's file with the male solutions ported, or from the male file, changes what the diff shows;
   D13 is kept as written.
6. **A male arm on block B** (§8): revision 1.1's rule (amend this file) is kept; the male arm on
   block A used a registration of its own.
7. **S27's form.** The retro's wording is "the seal record read at run time"; block B has no
   sealed file, so S27 records earlier real-arm runs of block B found at run time, with the scope
   searched. Whether that is the record the reviewers meant is for them.

**Revision 1.3: points 1–7 are answered by the reviewers' pass below** (items 1–8 of its table).
The points are kept as revision 1.2 wrote them.

### Revision 1.3: the reviewers' pass on revision 1.2 (2026-09-27)

Revision 1.2 (commit `9b86839`) was reviewed in the DPC Research chat on 2026-09-27. The votes and
the edits are as CC's message to the drafting agent relays them, with the consensus settled
between Ark and Zcode on Ark's M1–M7; the chat is not in the repository. Mike's word covering the
work: 14:31 UTC ("continue what we were doing"). Drafted by a CC subagent; not re-reviewed, not
committed. Nothing was fitted or run; no cell of block B was read (the one computation, §1.4's
hash, read presence outside block B only). No gate, cut, grid, seed, block or D-row
recommendation changed. What changed in the reading: one U kind (S38) is added before A's
branches (§4, the qualification written there); D7's stop is kept and now leaves a file (S39).

| reviewer | time (UTC) | vote |
|---|---|---|
| Ark | 14:48 (follow-up 14:59) | yes, with edits |
| Johnny | 14:56 | yes, with edits |
| Zcode | 15:11 | yes, with edits |

| # | edit | asked by | applied in revision 1.3 (where; sources checked) |
|---|---|---|---|
| 1 | Open point 1: S2 stays pinned to A after Amendment 1 (`fc415056…`); an Amendment 2 of A stops the run on the pin, read as "A changed", not as an environment defect | Ark, Zcode | S2 (one sentence) |
| 2 | Open point 2: D7's stop kept; a stopped run writes a stop record as a file before exit (chain, `succ`, `att`, arm, head), with a test that can fail | Ark, Zcode | §3.2 (3); S12; S39 (new) |
| 3 | Open point 3: the male "not readable" U ported by its object (`smallest_passing_auc is None`), not by a count; precedence over R, W and G; never renamed; not a threshold U; no threshold on the count; the 0 / 40 stop unchanged; the leg-P bar moving with the count stated, with Ark's probe quoted as unregistered | Johnny (edit 1), Ark, Zcode | §3.2; §3.4 check 3; §4 (qualification); §6 ("Few present cells"); S16 (note); S38 (new). Male script lines 407–411 and 1627, male registration lines 1308 (S16) and 1474 (D8), A's script line 1099: each opened and checked for revision 1.3 |
| 4 | Open point 4: male S28 and S30 added as S36 and S37, each with a test that can fail; `PRERUN_SCRIPT_SHA256_LF` is the hash of the script that wrote the reference, the reading script's hash differs by design (D10 (i)) | Ark, Zcode | S36, S37 (new); the port-plan paragraph. Male lines 118–127, 421, 1788–1796, 2109–2137, 3753, 3836; male registration lines 1321, 1324, 799; male tests T12 (line 984) and T14 S30 (line 1166): checked |
| 5 | Numbering: male S-numbers never reused; B's S16, S28, S30 keep their meanings; every port marked "(the male arm's SNN)"; the not-readable rule on a free number with its male source in words | Zcode, Ark | the port-plan paragraph; S16; S36–S38 |
| 6 | Open points 5 and 6 (D13): D13 kept; the table "S1–S22 re-checked against the male CNS arm's script" renamed and read as the plan of the port, each row "male line → B requirement" | Ark, Zcode | §7, "The plan of the port" (content of 1.2's table kept; two of its line ranges corrected: 70–80 → 74–80, 2936–2975 → 2936–2974) |
| 7 | Open point 6: a male arm on block B is a separate registration file; §1.1's eight pins not extended; revision 1.1's rule changed on the reviewers' vote | Ark, Zcode | §1.1; §8 (1.1's rule quoted, the amendment clause withdrawn) |
| 8 | Open point 7 and Johnny's edit 2: S27's three outcomes (root missing / root unreadable / root read, N found including 0), each with the scope searched; linked to S34 | Ark, Zcode, Johnny (edit 2) | S27 (requirement and test); S34 |
| 9 | M1: the exact canonical form of §1.4's table (key and value types, `sort_keys` on nested dicts, one element); recovered from the scratch script, not invented; the hash recomputed without reading block B's cells | Ark (M1), Zcode | §1.4, "The canonical form, exactly". The script `blockb_hash.py` (20:14:26 UTC 2026-09-25) was found in the revision-1 agent's scratchpad and transcript; the computation reads presence outside block B only; recomputed hash equals `aa092028…` |
| 10 | M2: one sentence, check 2's block-A clause is exactly `BLOCK_A ∩ BLOCK_B = ∅`; no new check | Ark (M2), Zcode | §3.4, check 2 |
| 11 | M3: S17 names what each pin covers (raw bytes, `.gz` included, `read_bytes()`); the column gate because `.gz` bytes are not reproducible; re-pinning forbidden | Ark (M3), Zcode | §3.3 (a bullet); S17. A's `check_prerun_files` lines 1512–1540 (hash at 1530), male lines 2074–2106 (hash at 2096); A's registration lines 636–641, 763–769, 1648–1655, 47–49: checked |
| 12 | M4: S25 extended to the synthetic step in both modes | Ark (M4), Zcode | S25. Male lines 3764 and 3776 (`run_synthetic_only`), 3845 and 3846–3848 (real arm): checked |
| 13 | M5: S18's wording (A's and both male references by path and pins; B's folder by path only until the pre-run, `B_PRERUN_SHA256 = None`) | Ark (M5), Zcode | S18. Male lines 139, 2936–2974; A's registration lines 1637–1643: checked |
| 14 | M6 (withdrawn): half a line in §3.1 that {L3, L4, L5} makes no polarity claim | Ark (M6), Zcode | §3.1. The strata were checked to be source type × the targets' ON/OFF split of the key (§1.2), not D4's L3–L5 polarities. The reviewers' words "the note names no targets for them" are narrowed for L3: the note names Mi9 and Tm9 (and Tm20) for L3 (§1.2); for L4 and L5 it names none |
| 15 | M7: the "upper bound 32" / "pair" caveat stays; Zcode's grep recorded; the check against flyvis-65's present cells not done (it needs the bank) and listed as open | Ark (M7), Zcode | §1.5 item 5; §11. The grep was repeated: "pair" is a count unit of bank cells (lines 16–18, 37–38, 136); "C6" has 0 matches |
| 16 | Johnny's §3.9 note: the callers check is done at the script's review, and the grep command goes into the review artifact | Johnny, in Zcode's form | §3.9 |
| 17 | This section and the header | CC's request | header; §10 |

**Computations for revision 1.3** (2026-09-27 UTC, `PYTHONUTF8=1`, `tools/.venv`): the §1.4 hash
only (above; the script printed the hash, its match and the types, no count). The three inputs'
LF sha256 were re-read and match their pins. Nothing else was run.

### Revision 1.4: the reviewers' pass on revision 1.3 (2026-09-27)

Revision 1.3 (commit `6b195bc`) was reviewed in the DPC Research chat on 2026-09-27. The votes and
the edits are as CC's message to the drafting agent relays them; the chat is not in the
repository. Mike's word covering the work: 14:31 UTC ("continue what we were doing"). Drafted by
a CC subagent; not re-reviewed, not committed. Every change is text only. Nothing was fitted or
run and the bank was not read; the probes quoted in §6 are Ark's, unregistered, and were not
rerun for this revision. No gate, cut, grid, seed, block or D-row recommendation changed.

| reviewer | time (UTC) | vote |
|---|---|---|
| Ark | 15:36 (and 15:39, on Johnny's M6 fix) | yes, with edits |
| Johnny | 15:41 | yes, with one factual fix |
| Zcode | 15:46 | yes, with edits |

| # | change | where | asked by (time, UTC) | checked against |
|---|---|---|---|---|
| 1 | The L3 parenthesis: the defect was the carrier, not the count. It now names both sets (the note's three targets for L3, Mi9, Tm9 and Tm20; the block's two, Mi9 and Tm9) and gives the ON/OFF split to the key | §3.1 | Ark (15:39), Zcode; Johnny's diagnosis (15:41) | the candidates note, lines 81–82 ("L3 feeds Mi9, Tm9 and Tm20"); §1.2's key (ON = {Mi1, Tm3, Mi4, Mi9}, OFF = {Tm1, Tm2, Tm4, Tm9}) |
| 2 | §4's heading: "(unchanged)" → "(delta: one U kind precedes the four branches)" | §4 | Ark (15:36), Zcode (15:46) | revision 1.3's qualification in §4's first paragraph |
| 3 | A fifth outcome: `smallest_passing_auc` `None` reads the not-readable U, not G, and says nothing about a grammar; the reason (floor 0.0245 < `P_G` = 0.10 at `n_p` = 1) | §5 | Ark (M8, 15:36), Zcode (15:46) | §6's probe value; A §4's `P_G` as quoted in §4 |
| 4 | Two consequences of the byte-copy guard: no refusal where no pinned-name file is present; the rule rests on the `.gz` bytes not being reproducible | §3.3 (a bullet) | Ark (15:36), Zcode (15:46) | male `out_dir_refusal`, lines 2944–2974 (docstring 2947–2952, guard 2964–2973, the condition at 2970), opened and read |
| 5 | A stopped run writes no sums and never becomes a reference: the missing `SHA256SUMS.txt` as a second, independent sign of the stop; added to S39's test; S29 cross-referenced | S39; S29 | Ark (15:36), Zcode (15:46) | S29's own rule (sums written last) |
| 6 | `n_p` = 39: "arithmetic, not probed" → probed, by Ark's `b_spa_probe2.py` (unregistered, deciding nothing): 1 and 39 → None (floors 0.0245, 0.0237); 2 and 38 → 0.9605263157894737 (denominator 76); the earlier table reproduced on numpy 2.2.6 | §6, "Few present cells" | Ark (15:36), Zcode (15:46) | the values as relayed by CC; not rerun |
| 7 | M9: the bar rises in trend, not monotonically (15, 16, 17), and depends on the layout at one count (8, 16, 20; 2 the same in four layouts); named as independent support for D4 (i)'s stated reason (one layout per board lets the one-value-per-board check hold; under (ii) it fails by construction) | §6 (a bullet) | Ark (M9, 15:36), Zcode (15:46) | D4's text (§10) read first; the probe fits its stated reason and nothing wider |
| 8 | The carrier of S38's "counted apart": printed on the verdict line, counted on its own line in the U-rule paragraph (S32 is about that paragraph's text, not the count), its own place wherever §3.5 or §3.6 counts U kinds | §3.5; S38 (a pointer) | Zcode (15:46), Ark (15:36) | S32's and S38's texts |
| 9 | S38's literal: block B's text says "of 40"; the test checks that literal, so a verbatim copy of the male "of 64" fails | S38 (test) | Zcode (15:46) | male `NOT_READABLE_REASON`, lines 410–411 ("(n_present = {k} of 64)"), opened |
| 10 | Header status 1.4; 1.3's status and history kept as they stood (`6b195bc`); this section | header; §10 | CC's request | — |

**Not applied: Johnny's literal fix.** Johnny's fix (15:41) was to change "two" to "three" in the
L3 parenthesis. Applied literally, it would make the sentence false: three targets cannot be "one
ON and one OFF", and Tm20 is not in the block and has no side in the key (§1.2). Item 1 above is
Ark's form (15:39) of the same fix, which Zcode joined. **Tm20's ON/OFF side is named in no file
opened for this revision** (the candidates note names it only as an L3 target, lines 81–82; §1.2's
key does not contain it).

**A record of CC's chat message (Zcode).** CC's chat message of 15:32 UTC said "three line ranges
were wrong in 1.2"; this file records two (§7, the plan of the port, and item 6 of "Revision 1.3":
70–80 → 74–80; 2936–2975 → 2936–2974). The file is the carrier; the chat message's count is not.

### Revision 1.4.1: one factual correction in §6 (2026-09-27)

Revision 1.4 (commit `68c0171`) was reviewed in the DPC Research chat: Ark 16:01 UTC and 16:03 UTC
("yes" on all nine items, with one correction), Johnny 16:02 UTC ("yes, no edits"; his check covered
§6's probe values, not the version sentence), Zcode 16:05 UTC ("yes", the correction required).
Applied by CC; text only; nothing run, the bank not read.

| item | was | correct | where the wrong text lived | refuted by | caught by |
|---|---|---|---|---|---|
| §6, the probes' numpy | "was also reproduced on numpy 2.2.6, not only on 2.4.6" | both tables were made on one interpreter, `connectome-seed/tools/.venv`, numpy 2.2.6; no other version was used | §6 (revision 1.4); its source was Ark's chat message of 15:36 UTC ("not 2.4.6, as in #13"), relayed by CC | `tools/.venv/Scripts/python.exe -c "import numpy; print(numpy.__version__)"` → 2.2.6, and Ark's tool log of the session | Ark (16:01) |
| §6, the probes' carriers | the first table was "Ark's sandbox run", with no script named; the second said "sandbox" without whose | `b_spa_probe.py` and `b_spa_probe2.py`, in Ark's review sandbox, outside this repository (Zcode checked both exist) | §6 | — | Ark (16:01, 16:03), Zcode (16:05) |

Revision 1.4.1 carries the review of 1.4 and this correction only; the header's status says so.

### Revision 1.5: the reviewers' pass on the script (2026-09-28)

The block-B script and its tests at `1a765f5` (branch `block-b-script`, on revision 1.4.1) were
reviewed in the DPC Research chat on 2026-09-27. The votes and the edits are as CC's message to
the drafting agent relays them; the chat is not in the repository. Mike's word covering the work:
2026-09-27 14:31 UTC. Drafted by a CC subagent; not re-reviewed. Zcode also ran the 59 tests of
`1a765f5` independently: 59 passed, 37.47 s. Nothing was fitted or run on the real bank, no cell
of block B was read, and no gate, cut, grid, seed, block or D-row recommendation changed. The
script changes are code comments, the port markers, the revision constant and two tests (S38
extended, S40 new); no computation changed.

| reviewer | time (UTC) | vote |
|---|---|---|
| Johnny | 16:45 | yes, with the OPEN items resolved |
| Ark | 16:48 and 16:52 | yes, with edits |
| Zcode | 17:01 | yes, with edits |

| # | change | where | reviewer (time, UTC) | checked against |
|---|---|---|---|---|
| 1 | S40 registered: a full `--synthetic-only` run refuses a dirty tree unless `--allow-dirty`, which marks it NOT A REFERENCE (log, manifest, `SYNTHETIC.md`); named a tightening relative to A; the script's marker `-> D10 (i)` changed to `-> S40`; a new test that can fail | §7 (S40; the paragraph before the S23–S40 table); script `main`; test `test_S40_dirty_tree_refused_unless_allow_dirty` | Ark (16:48), Zcode (17:01); OPEN 5 | male `run_synthetic_only`, lines 3716–3727 (the refusal 3723–3726, the mark 3727) at HEAD, opened; A's `refuse_if_dirty` (`knockout_regrow.py` lines 386–393) is called by the real arm only. No test of the refusal existed at `1a765f5` (grep for `allow-dirty` in the test file: 0); the new test fails with the refusal removed and with the mark removed (both run) |
| 2 | The §1.4 table and the training present count are printed in the real arm only; both leak routes named (604 minus the training present count; the per-name [out, in] pairs with A §1.4's whole-bank degrees) | §1.3, §1.4, §1.5; script `check_pre_data_tables` (comment) | Johnny (16:45), Ark (16:48), Zcode (17:01); OPEN 1 | `check_pre_data_tables` returns the table and the count only with `real_arm` true; `_run` prints them only under `a.arm` |
| 3 | The three outside states of a `--synthetic-only` run: no folder / `stop_record.json` and no sums / sums | S39; script `write_stop_record` (comment) | Johnny, Ark, Zcode; OPEN 2 | `write_stop_record` returns `None` without a folder and the stop message says "none (the run has no folder)" |
| 4 | `SHA256SUMS.txt` is written in the committed `OUT` too (the literal reading of S29); a delta from A; `.gitignore` does not cover it | S29 (a); script `main` (comment) | decided by CC on the votes: Zcode's vote (keep the literal reading), Ark accepted either if chosen explicitly (16:48, 16:52); OPEN 3 | `git check-ignore -v results/genome/c6/checks/knockout_regrow_block_b/SHA256SUMS.txt`: not ignored (exit 1) |
| 5 | The general form: the folder of any run that did not complete has no `SHA256SUMS.txt` (two-world check, check 4, check 3, S37, S39) | S29 (b); script `_run` (comment) | Ark (16:48), Zcode (17:01); OPEN 4 | every `sys.exit` of the script read: each is inside `_run` (or its callees) or before any folder is made; `main` calls `write_sha256sums` only after `_run` returns (`completed = True`). No exit path writes sums first; no code change was needed |
| 6 | The `PRERUN_DIR` sequence: the pre-run's `--out` is a new stamped folder; `PRERUN_DIR` and the pins move to it in the revision after the pre-run; the path the constant names now is never written into | §3.3 ("New reference") | Zcode (17:01), in answer to Ark (16:48) | "D10 (iv)" as relayed names no item: D10 has options (i) and (ii); the step is (4) of the order of work under D10 (i) (the header). `protected_references` (block B's script, lines 2912–2921 at `1a765f5`) lists `("B", PRERUN_DIR, PRERUN_SHA256)`; the path guard of `out_dir_refusal` (lines 2939–2943 at `1a765f5`) refuses at or inside every listed folder whatever its pins |
| 7 | `write_raw` writes a `.gz` with its mtime; pinned bytes are integrity, the column gate is reproducibility; a rerun's `.gz` is never compared with a pinned file | S17 | Ark (16:48), Zcode (17:01); ㊱ | `write_raw` calls `gzip.open(path, "wt", …)` with no `mtime` argument, so the header carries the time of writing; `write_raw` unchanged |
| 8 | The disclosure of a subagent's grep of `types.csv` during script construction (Ark's wording) | §11 | Ark (16:48); Johnny, Zcode agree | the wording as relayed |
| 9 | The plan of the port: S21's port marker added in the script (the male `TAU` comment, lines 321–327, male S24); S14's row corrected from "no" to "partly" (`board_y`, male lines 1121–1125) | §7, the plan of the port; script (the `TAU` comment) | Zcode (17:01) | male lines 321–327 opened: block B's `TAU` comment follows their generic form ("with n_p present of …", "the same lattice argument holds for it"), which A's comment (`knockout_regrow.py` lines 228–233) does not have; male `board_y` lines 1121–1125 opened |
| 10 | Script: `has_auc` means "AUC defined" (0 < n < 40), not "leg P can pass"; n = 1 and 39 pass check 3 and are read by S38 | script `block_print`, `check_block_print` (docstring, comment) | Ark (A1) | — |
| 11 | Script: the `# OPEN:` markers replaced by pointers to the registration items, the decisions' text kept | script (five places) | Ark (A2) | `grep "OPEN:"` in the script: 0 |
| 12 | Test: `test_S38_not_readable` extended: `n_p` = 39 gives the not-readable U with "(n_present = 39 of 40)", `n_p` = 1 and 39 pass check 3, `n_p` = 2 carries no not-readable text | test file | Ark (A3) | only the `None` of Ark's unregistered probe is relied on (the test asserts `smallest_passing_auc` is `None` at 1 and 39, as before), not its floor values |
| 13 | Header status 1.5; 1.4.1's status and history quoted as they stood (`3e5f2da`); `REGISTRATION_REVISION` = "1.5" in the script and its test; this section | header; §10; script; test | CC's request | — |

**A4: applied in revision 1.6** (§10, "Revision 1.6"; §3.3, "The reference is made by fitting,
never by a re-read"; S17, S37). The paragraph that stood here in revision 1.5 ("Not applied:
A4 …", committed in `b810ecb`) gave a wrong reason, S37's single writer hash; revision 1.6's
journal row records it. Its facts about A and the male arm stand and are used in §3.3: A's pinned
reference table was written by a `--synthetic-only --from-raw` pass (A §3.3, revision 3.2, line
632: "0 new world fits"; A §7, line 1614), and the male registration registers a
`--synthetic-only --from-raw` check after the merge without `--out` (male §3.3.1 (h), line 799;
D15 (i), line 1481).

### Revision 1.6: the reviewers' pass on revision 1.5 (2026-09-28)

Revision 1.5 and the script and tests at `b810ecb` (branch `block-b-script`) were reviewed in the
DPC Research chat on 2026-09-27. The votes and the edits are as CC's message to the drafting agent
relays them; the chat is not in the repository. Mike's word covering the work: 2026-09-27 14:31
UTC. Drafted by a CC subagent; not re-reviewed. Zcode ran the 60 tests of `b810ecb`
independently: 60 passed, 38.07 s. Nothing was fitted or run on the real bank, no cell of block B
was read, and no gate, cut, grid, seed, block or D-row recommendation changed. The script gains
three carriers of A4 (a refusal, a condition, a reader's refusal), comments and the revision
constant; no registered number's computation changed. The test file gains three tests.

| reviewer | time (UTC) | vote |
|---|---|---|
| Johnny | 17:54 | yes, with the A4 resolution named |
| Ark | 17:58 and 18:00 | yes (A4 decided by the object); yes, with one code edit (A4 needs a carrier in code; a refusal preferred) |
| Zcode | 18:05 | yes (ran the 60 tests: 60 passed, 38.07 s); A4 in Ark's form, with the refusal |

| # | change | where | reviewer (time, UTC) | checked against |
|---|---|---|---|---|
| 1 | Maker side: `--synthetic-only --from-raw` with `--out` is refused before any folder is made ("REFUSED: block B's reference is made by one fresh fitting run (S17, D10 (i)); an --out folder can be a reference, and a re-read is not one. Run --from-raw without --out."); without `--out` it stays a diagnostic | script `main` (next to S40's refusal), `FROM_RAW_OUT_REFUSED_TEXT`, the `--from-raw` help; §3.3; S17 | Ark (17:58, 18:00), Zcode (18:05); Johnny's reasoning (17:54) | the refusal (line 3417 of 1.6) precedes `folder.mkdir` (line 3429 of 1.6) and does not depend on the tree state; `test_S17_from_raw_with_out_refused_without_out_a_diagnostic`: on a clean fixture tree the run exits with the text and no folder; a `--from-raw` run without `--out` completes, re-reads the saved fits and writes no folder. With the refusal removed the test fails (mutation M1) |
| 2 | `is_the_pinned_store` from record to condition: False when the pins or the file are absent; it gates the re-read comparison: `check_prerun_reproduced(..., reread=True)` compares with the pinned table only for block B's own pinned store, and a re-read of another store records no outcome; `passed` stays `None` for every re-read; the per-fit diagnostic's note reads the same condition | script `is_the_pinned_store` (new), `check_prerun_reproduced` (parameter `pinned_store`), `run_synthetic`, `_run`; §3.3; S17 | Ark (18:00), Zcode (18:05) | at `b810ecb` the record (lines 3472–3473) compared `sha256` with `(PRERUN_SHA256 or {}).get(...)`: `None == None` with no pins and no file; nothing read it. The gate's place is the re-read branch of `check_prerun_reproduced` (item ㉜); a re-read never stops the run, as before. `test_S17_is_the_pinned_store_is_a_condition` fails with the old vacuous comparison (M2) and with the gate removed (M3) |
| 3 | Reader side: `prerun_provenance` refuses a reference whose manifest carries a non-null `not_a_reference` | script `prerun_provenance`; S37 | Ark (18:00) | at `b810ecb` it read only `git_head` and `script_sha256_lf` (lines 2060–2062). `test_S37_reader_refuses_a_not_a_reference_folder`: a fixture reference made with `--allow-dirty` and pinned by its own sums verifies (`check_prerun_files` passes) and is refused; the real arm stops with "PRE-RUN PROVENANCE DIFFERS" before any fit. With the refusal removed the test fails (M4) |
| 4 | The reason by the object: the key carries no block; four readings with lines; "under `--from-raw` the block's labels come from the store, and the only cross-check is the fits' agreement with each other"; D10 (i) is about provenance, not method; the asymmetry A↔B as a gain; the rule joined with `reread=True` in the reproduction gate (㉜) | §3.3 ("The reference is made by fitting, never by a re-read"); S17 | Ark (17:58, the readings), Zcode (18:05, verified them), Johnny (17:54, provenance, not method) | each line opened by the drafting agent at `b810ecb`: 3008, 3013 (`write_raw`, `read_raw`), 232 (`MASKS`), 3506, 1433 and 1436 (`evaluate_bank`), 3472–3473, 3382, 2060–2062, 3480 (`script_sha256_lf` of `Path(__file__)`); A's registration line 632 |
| 5 | OPEN 2's three outside states say whether a run completed; being a reference is the manifest's `not_a_reference`; the fourth state (sums and `not_a_reference`) | S39 | Ark, Zcode | `test_S40_dirty_tree_refused_unless_allow_dirty`: an `--allow-dirty` folder has `SHA256SUMS.txt` and `not_a_reference` set |
| 6 | The sums in `OUT` are not a reference pin; never compared with `PRERUN_SHA256` | S29 (a); script `main` (comment) | Ark, Zcode; ㊹ | `check_prerun_files` reads only `PRERUN_DIR/SHA256SUMS.txt`; `protected_references` (line 2919 at `b810ecb`) lists A's, block B's and the male references, not `OUT` |
| 7 | "S27 runs in the real arm only" | S27; script `main` (comment) | Ark, Zcode | `find_earlier_runs` is called under `a.arm` only (line 3365 at `b810ecb`); the `--synthetic-only` branch sets `earlier = None` (line 3383 at `b810ecb`) |
| 8 | The name "D10 (iv)" (Revision 1.5, row 6) was Zcode's (17:01), passed on by CC in its relay, and caught at CC's stop condition by the agent drafting 1.5; Zcode acknowledged it (18:05). Row 6's text stands; it did not say whose the name was | this section | Zcode (18:05) | Revision 1.5, row 6: "'D10 (iv)' as relayed names no item" |
| 9 | Header status 1.6; 1.5's status quoted as it stood (`b810ecb`); 1.5's "Not applied: A4" replaced by a pointer; `REGISTRATION_REVISION` = "1.6" in the script and its test; this section | header; §10; script; test | CC's request | — |

| item | was | correct | where the wrong text lived | refuted by | caught by |
|---|---|---|---|---|---|
| A4, why a re-read cannot make block B's reference | reference made by one fresh pass; S37's single writer hash stays exact | S37's writer hash hashes the script file and is the same under `--from-raw`; the key carries no block, the loaded store is unchecked, the labels come from the store; the rule is decided by the object, with carriers in code (rows 1–3) | §10, Revision 1.5, "Not applied: A4" (`b810ecb`); CC's chat message of 17:42 UTC and Zcode's wording of 17:01 UTC | the four readings at `b810ecb`: lines 3008 and 3013; 3506; 1433 (with 1436); 3472–3473 (with 3382 and 2060–2062); and line 3480, `sha256_lf(Path(__file__))` | Ark (17:58) |

### Revision 1.6.1: revision 1.6 reviewed; Ark's small edits (2026-09-28)

Revision 1.6 and the script and tests at `8bb5aee` (branch `block-b-script`) were reviewed in the
DPC Research chat on 2026-09-27. The votes and the edits are as CC's message to the drafting agent
relays them; the chat is not in the repository. Mike's word covering the work: 2026-09-27 14:31
UTC. Drafted by a CC subagent. Zcode ran the 63 tests of `8bb5aee` independently: 63 passed,
43.55 s. All three votes are yes; Ark asked for small, non-blocking edits in the same commit, and
this revision applies them. Nothing was fitted or run on the real bank, no cell of block B was
read, and no gate, cut, grid, seed, block or D-row recommendation changed. The script's pre-run
is unchanged (for a comparable run the new mark equals the old one); no registered number's
computation changed. The test file gains two tests and an extension.

| reviewer | time (UTC) | vote |
|---|---|---|
| Zcode | 18:26 | yes (ran the 63 tests: 63 passed, 43.55 s); confirms both readings |
| Johnny | 18:27 | yes, no edits |
| Ark | 18:30 and 18:32 | yes, with small non-blocking edits in the same commit (rows 1–3) and two questions (answered below) |

| # | change | where | reviewer (time, UTC) | checked against |
|---|---|---|---|---|
| 1 | One token: `not_a_reference = … if (dirty and comparable) else None` became `… if (dirty or not comparable) else None`; the mark names its actual cause (`not_a_reference_text`; new `NOT_A_REFERENCE_FORM_TEXT` for a run not in the registered form; `NOT_A_REFERENCE_TEXT` unchanged for an `--allow-dirty` run); `SYNTHETIC.md` prints the manifest's mark, not the constant. Being a reference needs the registered form and a clean committed tree | script `main` (line 3457 of 1.6.1), `not_a_reference_text`, `NOT_A_REFERENCE_FORM_TEXT`, `write_synthetic_outputs`; §3.3 (new bullet); S37; S39; S40 | Ark (18:32) | for a comparable run `dirty or not comparable` equals `dirty`, so the pre-run's mark is as in 1.6 (`test_S40_dirty_tree_refused_unless_allow_dirty` passes unchanged, also under the reverted token). `test_S40_non_registered_form_is_not_a_reference`: a clean-tree `--smoke-shuffles 1 --out` run carries `NOT_A_REFERENCE_FORM_TEXT` in its manifest and `SYNTHETIC.md`; pinned by its own sums it verifies and `prerun_provenance` refuses it; `--starts 3` and a dirty smoke run are marked too. With the token reverted the test fails, the other passes; the script was restored byte for byte (sha256 compared) |
| 2 | `check_ko1_count` takes `pinned_store`, as its twin `check_prerun_reproduced` does: under `--from-raw` of a store that is not block B's pinned one the count is not compared with the registered value (`equal` None, status "informative, not compared"); for the pinned store it is compared (`equal` recorded); `passed` stays `None` for every re-read, so no registered gate changed | script `check_ko1_count` (lines 2452–2481 of 1.6.1), `run_synthetic` (`pinned_store` read once, passed to both twins); S17; §3.3 | Ark (18:32) | at `8bb5aee` the call (lines 2581–2582) passed `reread` but not `pinned_store`, and the comparison `got == registered` was recorded for any re-read store; the re-read branch set `passed` None already, so the gate is untouched. Test `test_A16_ko1_count_control` extended (unit), `test_S17_ko1_count_reread_compared_only_for_the_pinned_store` (end to end on a fixture reference: the pinned store compares, equal True; the same fits re-gzipped with another mtime are not compared, equal None). The test fails with the argument removed from the call (M2) and with the rule removed from `check_ko1_count` (M3); restored byte for byte |
| 3 | Phrases: `from_raw_record` exists only under `--from-raw` and `pinned_store` is False by construction in a fresh run; where a re-read's comparison outcome is visible (`manifest["prerun_comparison_outcome"]`, `two_world_check.prerun_reproduction.comparison` in `synthetic_only.json`); `prerun_provenance` is called only under `reference_mode()`, not in the pre-run, by design | §3.3 (new bullet); S17 | Ark (18:30, 18:32) | both names opened in the code: `manifest["prerun_comparison_outcome"] = rp["outcome"]` (line 3588 of 1.6.1), `rp = syn["two_world_check"]["prerun_reproduction"]`; `two_world_check` returns `"prerun_reproduction": repro` (line 1810) and `check_prerun_reproduced` stores `comparison=cmp` (line 2136) only when it compares; `synthetic_only.json` is `{"manifest": manifest, **syn}`. `prerun_provenance` has one caller, under `if reference_mode():` (lines 3529–3530 of 1.6.1) |
| 4 | Header status 1.6.1; 1.6's status quoted as it stood (`8bb5aee`); `REGISTRATION_REVISION` = "1.6.1" in the script and its test; this section | header; §10; script; test | CC's request | — |

**Ark's two questions, answered (checked by CC, and by the drafting agent in the code):**

- *`--arm --from-raw`: refused or marked?* **Refused.** `main` exits before any check, fit or
  folder: `if a.arm and (smoke or a.from_raw or a.starts != 10): sys.exit("REFUSED: the real arm
  runs as registered: --starts 10, no smoke option, no --from-raw (sections 3.3, 7)")` (line 3385
  of 1.6; line 3350 of 1.5; line 3414 of 1.6.1). Stated in §3.3 and S17.
- *A latent crash in 1.5: `PRERUN_SHA256["raw_fits.json.gz"]` subscripted on `None` (line 2592
  at `b810ecb`)?* **Not reachable; checked, not a fixed defect, so no journal row.** The
  subscript sits inside `if comparable and repro.get("prerun_files", {}).get("passed"):` (line
  2586 at `b810ecb`). In the pre-run (`PRERUN_SHA256` None) `check_prerun_reproduced` returns at
  `if not reference_mode():` (line 2092 at `b810ecb`) before it sets `prerun_files`, so the
  guard reads `{}` and is false; and `check_prerun_files` itself returns `passed` False when the
  pins are `None` (`if not pins:`, line 2017 at `b810ecb`). In reference mode `PRERUN_SHA256` is
  a dict. Revision 1.6 replaced the subscript with `is_the_pinned_store`, which uses `.get`.


## 11. Not verified at drafting

- **Revision 1.5, a disclosure (Ark's wording; Johnny and Zcode agree).** During script
  construction, one subagent ran a grep of `types.csv` by L1–L5 and saw their rows, including the
  bank-wide `n_out_entries` column (the column §1.5's abstention names). No block-B count was
  derived from it and nothing was recorded. This did not happen during a fit or a run.

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
  more likely; if it is 0 or 40, the run stops (§3.4). **Revision 1.3:** if leg P cannot pass on
  it (`smallest_passing_auc is None`), it reads the "not readable" U (§3.2, S38); Ark's probe of
  where that happens (§6) is unregistered.
- **Revision 1.3: the note's "pair" against flyvis-65's C6 existence** (§1.5 item 5, M7): not
  checked; it needs the bank's cells, block B's among them, and D3 (ii) abstains before the run.
- **Revision 1.3: S36–S39 and the extensions of S25 and S27** are, like S23–S35, requirements on
  a script that does not exist; their tests are described, not written, and that each can fail
  was reasoned from the male script's code and tests at `01d2d05`, not run.
- **Revision 1.3: the stop record's folder in `--synthetic-only`** (S39): the reviewers asked for
  a file "in the private folder"; in `--synthetic-only` the run's folder is `--out`, and S39
  writes it there. That reading is this draft's.
- **GLOSSARY:** it has no entry for block A, block B or knockout; its rules of use ask for a term
  to be added before use. Not added here (this draft modifies no existing file).
- **The male-CNS mapping of L1–L5** (§8). Revision 1.2: whether the built male bank
  (`5860619`) places L1–L5 was not checked.
- **Revision 1.2: S23–S35 are requirements on a script that does not exist.** Their tests are
  described, not written; that each test can fail was reasoned from the male script's code at
  `01d2d05`, not run.
