---
**Status (revision 3.3, 2026-09-25 UTC): draft. Revision 3.3 has NOT been reviewed; no real-arm
run before its review, Zcode's vote and Mike's word.**

**Revision 3.3, 2026-09-25 UTC: the reviewers' pass on revision 3.2. Text and code only; no
fitting run.** It applies the review of revision 3.2 in the DPC Research chat, 2026-09-25
14:04–14:39 UTC (Ark and Johnny; both vote "yes, with edits"), Zcode's votes at 15:05 UTC and
CC's probes posted at 15:1x UTC. The procedure is Mike's word of 13:36 UTC: the subagent drafts,
CC checks, all three review. **Acceptance rule** (Ark and Johnny, 14:36–14:37 UTC): a new item
enters only if it (1) can destroy an artefact, (2) blocks the run, or (3) changes the text or the
coverage of a quoted verdict-line string. Drafted by a CC subagent. The votes and the items are in
§10, the changes and the error ledger in §12. What revision 3.3 changes:

- **The reproduction gate matches rows by key and splits outcome 3** (§3.3, §7). Rows are matched
  by (family, j, seed, predictor); missing rows, value differences and a change of row order are
  three separate outputs, and a change of order alone is not outcome 3. Outcome 3 is split into
  (a) identity or lattice columns and (b) continuous columns beyond `MACHINE_CHECK_TOL`. Its
  treatment names four layers (the fits, the leg-P null generator, the consumer, the machine) and
  the order in which they are read, and the self-test's outcomes are corrected: a self-identical
  rerun that still differs from the pinned table is a code difference **or** a machine
  difference, and the two cannot be told apart today. The null inputs are digested into the
  manifest. The 84 column-8 differences are checked to be exactly revision 3.2's rename.
- **The reference folder is protected** (§7): `--out` is refused at or inside the pinned
  pre-run folder, on any folder that holds a byte copy of it, and with `--arm`. "Recreating the
  reference" is written: never in place, and a red pin is never answered by re-pinning.
- **Three U texts** (§3.6, §4, §5): a threshold U, a failed fit, and a U whose `ceiling_block`
  was not measured; the U rule counts threshold U only.
- **The per-fit diagnostic** compares the five score fields too, and says so when a `--from-raw`
  pass compares the pinned store with itself (§3.3). **`--allow-dirty`** marks a real-arm run as
  not the registered run on its verdict line (§3.3, §7).
- **Reading rules, text only** (§3.2, §3.3, §3.6, §3.8): `smallest_passing_auc`; a pin is
  integrity, not reproducibility; the vocabulary of "present" and of λ; the γ_R input chain and
  `TAU`; what the gate covers; the provenance of the reference; the four reasons behind V1.
- **CC's probes** (§3.3, §11): a fresh refit of the three worlds that carry the γ_R bracket and
  the minus side of γ\*_P equals the pinned store on every field, shuffles and permuted-block
  ceilings included (2112 of 2112 fits).
- **An error ledger** (§12): every wrong wording caught in the review, with where it lives.

Revision 3.2 was reviewed at 14:04–14:39 UTC. Its status and its header follow, kept as written.

**Status (revision 3.2, 2026-09-25 UTC): draft. Revision 3.2 has NOT been reviewed; no real-arm
run before its review and Mike's word.**

**Revision 3.2, 2026-09-25 UTC: the reviewers' pass on revision 3.1. Text and code only; no
fitting run.** It applies the review of revision 3.1 in the DPC Research chat, 2026-09-25
12:06–13:13 UTC (Ark and Johnny; Zcode did not vote), on Mike's word at 13:36 UTC to assemble it
now: "Yes: the subagent applies the edits from Ark's list, CC checks and puts 3.2 to review for
all three; Zcode will read 3.2". Drafted by a CC subagent. The votes and the items are in §10,
the changes in §12. What revision 3.2 changes:

- **The reproduction gate compares the deciding columns, not the bytes** (§3.3, §7; Johnny
  blocked the byte-for-byte stop as written, Ark asked for changes). The fresh
  `synthetic_worlds.csv` is compared with the pinned one row by row: lattice columns exactly,
  continuous columns within `MACHINE_CHECK_TOL` = 1e-9, and `mechanism_description` (column 8)
  reported, not gated. Byte identity is recorded in the manifest as a fact. The three outcomes
  and their treatment are written before the run. The script checks every file listed in the
  pre-run `SHA256SUMS.txt`, and adds a per-fit diagnostic that decides nothing. The measured
  facts it rests on (CC, 2026-09-25) are in §3.3.
- **The U reason reaches the verdict line** (§4, §5). A U whose reasons include `ceiling_block`
  below the gate prints as a failed fit, and the U rule never renames it. This branch never ran
  in the pre-run, so a new test injects the reasons (a positive control, Johnny).
- **A `--from-raw` pass says that it re-read saved fits** and is not a reproduction (§7).
- **The manifest records the BLAS, the machine and the four thread variables** as found (§7).
- **One threshold on two variables is split** into a gate cut (`ceiling_block`) and a mechanism
  cut (`ceiling_full`), both 0.90, so nothing changes numerically (§2.4, §4). **This changes
  the text of column 8 of `synthetic_worlds.csv`:** the mechanism description now reads "rule
  #2.1's ceiling_full = …". The fresh table is therefore no longer byte-identical to the pinned
  one on the 84 rows that carry a mechanism description. Column 8 is outside the deciding set
  (§3.3). The `--from-raw` re-read of revision 3.2 (below, §3.3) found every deciding column
  equal, and differences in column 8 only, on 84 rows.
- **Reading rules, text only** (§3.1, §3.2, §3.6, §3.7, §7): the three limits of the pre-run
  table, the family limit included; what they rest on; λ; which p value defines them; what the
  CSV cannot show; `TAU`; the regrown share; the reasons of the three pre-run U worlds. **U is
  the signature of the detection limit γ\*_P, not of the band** (Ark).
- **Hygiene:** "weak leg" is replaced by "leg P" throughout, in the kept headers and in the
  records of revision 3.1 as well; sentences saying the files are "untracked" or "not
  committed" are marked "as of revision 3.1" (commit `8a514fa` committed them); the provenance
  of the fits (§3.7) and of the fitting runs (§7).
- **Readiness rule (Johnny 12:40 UTC, Ark accepted 12:45 UTC):** blocks A (the items that block
  the run or distort the verdict line) and B (the reading rules) must both be in the tree before
  the registered run starts, and C (hygiene) in the same commit (§10). Block D, the GPU, is not in
  this revision.

Revision 3.1 was reviewed at 12:06–13:13 UTC. Its status at session close and its header follow,
kept as written except for the vocabulary above.

**Status at session close (2026-09-25 09:41 UTC): committed as an unreviewed DRAFT on Mike's word
(Claude Code session, 2026-09-25, after the session close).
Revision 3.1 has NOT been reviewed. The next session starts with its review (handover
`docs/briefs/2026-09-25-next-session-handover.md` §2). No real-arm run is allowed before that review
and Mike's word.**

**Revision 3.1, 2026-09-25 UTC: the reviewers' pass on revision 3. Text and code only; nothing
was run** (Mike, DPC Research chat, 09:35 UTC: "run nothing"). It applies the requests of Ark
09:32, Johnny 09:33 and Zcode 09:34 UTC (§10, §12). What revision 3.1 changes: **three limits
instead of one**: γ\*_P (the leg-P limit), γ_R (the R level) and the family limit. **G is redefined
as "not detected at the R level above γ_R; leg P passes from γ\*_P"** (§3.6, §4). The
per-γ fractions seen/n and R/n are printed beside the limits, with Johnny's binomial note. **U is
the signature of the detection threshold**, and the report prints the width of the transition
band (§3.6, §4, §11). The λ selected by each knockout fit is printed on the verdict line (§4). λ
is recorded as a three-position knob (§6, §11). The files' mutability is recorded, and the
registered run must reproduce the pre-run table (§3.3, §7). The private and raw outputs are named
(§7). The instrument is the CPU harness; a GPU instrument would be a separate one (§7).
**The pre-run synthetic outputs** (revision 3's runs; SYNTHETIC.md, synthetic_only.json,
synthetic_worlds.csv, raw_fits.json.gz, rev2_full.log, SHA256SUMS.txt) are kept for
cross-checking in
`C:\Users\mikha\Documents\dpc-research\connectome-seed-data\knockout_regrow\synthetic_rev3_prerun\`
(§7). **Mutability, stated (Johnny 09:33 UTC):** this file and the script are both untracked
(as of revision 3.1; commit `8a514fa` committed them).
Revision 3's text was last saved at 09:25:54 UTC, 41 minutes after the script's last save at
08:44:21 UTC (file times, read before revision 3.1 edited both). The pre-run synthetic numbers
were produced before this final text. They are therefore **pre-run values**. The registered run
recomputes all of them from a clean committed tree (§3.3, §7). Revision 3's header follows
unchanged.

**Revision 3, 2026-09-25 UTC** (after the synthetic-only run of revision 2, D11: seen → corrected;
§12). It applies the reviewers' consensus of the DPC Research chat, 2026-09-25: Zcode 08:22,
Ark 08:24 and Johnny 08:27 UTC, summarised by CC at 08:28 UTC. Mike supported CC's two
summaries at 08:30 UTC ("ok делай"). **The real block is still not read, fitted or scored.**
The only new numbers are synthetic: the revision-2 run (30 worlds) and the dense-γ run of
revision 3 (15 new worlds, plus the fixed-λ diagnostic). Both are read in §3.6 and §12. What
revision 3 changes: M worlds become a power curve with no stop (§3.6). G is redefined as "not
detected above γ\*" (§4). The mechanism labels of G become description only (§2.4). Degenerate
shuffles are excluded from leg S (§3.2, D14). The λ switch is recorded as a measured property
of the instrument (§6, §11). The U rule (§3.6). The fixed λ = 1 diagnostic (§3.5). §7 is
corrected (D11 order, measured cost, outputs). Revision 2's header follows unchanged.

**Status (revision 2's header):** registration, **revision 2, draft for review**, not committed, not run. Revision 1 was
drafted by a CC subagent on 2026-09-24 at about 20:50 UTC (2026-09-25 03:50 local, +07:00), for
ADR-005 decision 3 ("knock out and regrow" is the next registration; Mike, DPC Research chat,
2026-09-24 17:53 UTC) and agreed point 6. Revision 2 applies the reviewers' consensus of the DPC
Research chat, 2026-09-24 (Ark 20:56, Johnny 20:58, Zcode 20:59 UTC; §12). Their votes are in
§10. **D11, the `--synthetic-only` run before commit, is pending Mike.** **Dated by its UTC day**,
as the [glossary's date-time convention](../../GLOSSARY.md) requires. The request named it
`2026-09-25-…`, which is the local day (§10, D12).
**No regrowth value exists anywhere at the time this file is written.** No rule, null or BF_r was
fitted on any bank, real or synthetic, and no synthetic world was drawn. The block's weights, offsets,
counts and signs were not read. The only numbers taken from the bank are **counts of names and of
presence outside the block** (§1.4). They were computed by one scratch script that dropped every
block cell before it read any presence, as the brief allowed. Also computed: one piece of algebra on
random numbers, with no bank involved (§2.3). Revision 2 adds algebra only (§2.4, §3.6), and no
bank number. The design choices that need a vote are marked
**proposal** in the body and listed in §10. The body is written with the recommended option, so
the draft is complete as it stands.
---

# Registration: knock out and regrow, block A on flyvis-65 (ADR-005 decision 3)

## 0. Question, name, and what it is not

**Name.** *Knock out and regrow: does a learnable rule that reads no type names regrow the ON/OFF
motion-input block it was not shown?*

**Question.** Remove from the bank every cell of block A: the 8 medulla inputs of the motion
pathways × the 8 direction-selective cells, 64 cells. Train the rule on everything else. Then ask
whether its predictions for the 64 cells tell the 32 present cells from the 32 absent ones better
than (i) the same rule on the same knockout in 99 degree-preserving shuffles of the bank, and
(ii) the same predictions scored against the block's own labels permuted within the block
(Zcode's second null). A rule that passes regrows structure that it was not shown and that the
bank's degrees do not carry. That is a claim of generation, not of fit. The standard is the
knockout and reversal experiments of [literature.md §28](../../literature.md) (Lenski et al.
2003), per ADR-005 agreed point 6.

**Why this block has a structure to regrow, not only a density.** On all three banks named in the
review, the block is a perfect board: ON × T4 (16 cells) and OFF × T5 (16 cells) are present, and
the 32 cross cells are absent (reviewed and recounted by name: Ark, Johnny, Zcode, 2026-09-24
20:22–20:39 UTC; [candidates note](../notes/2026-09-25-knockout-block-candidates.md), "Review and
decision"). Every one of the 16 types therefore has exactly 4 present cells out of 8 inside the
block. This fact is public and was not recounted for this draft. Two consequences follow before
any data:

- **No additive score can find the board.** For any score of the form `a_s + b_t`, the parity contrast
  `(ON×T4 + OFF×T5) − (ON×T5 + OFF×T4)`, summed or averaged, is identically zero (Ark's algebra on
  `fit_n1`, `harness.py:350-356`). So **the N1 leg decides nothing** on this block, in either
  direction. That is a statement about the contrast. N1's AUC is not pinned at 0.5 (§2.3).
- **The board is exactly rank 1** (§2.4). A rank-1 rule can therefore represent it, and a rule
  shown only the block can hold it.
- **Leakage through degrees cannot carry the board.** ADR-005 named degree leakage as the known
  risk. Inside the block every type has 4 of 8, so the block adds the same constant to every
  endpoint's degree. Even complete knowledge of total degrees says nothing about which block cells
  are present. And the knockout removes the block cells, so the rule sees outside degrees only.

**What the bank is (ADR-005 agreed point 2, stated as required).** The primary bank is
**flyvis-65**, the generation-zero bank (`results/genome/bank/offsets.csv`). It is a **synthetic
template of at least two flies**: flyvis's column-averaged estimates from the FIB-25 and FIB-19
volumes, fused by taking the larger of the two (Lappalainen et al. 2024, Supplementary Note 1,
eq. 7; [where our bank comes from, §1–§2](../notes/2026-09-23-where-our-bank-comes-from.md)). It is
not an animal. The node is not renamed (ADR-005 point 2). Mike chose flyvis-65 as the primary bank
at 2026-09-24 20:39 UTC.

**Column-test anchor (what "measured on the averaged representation" means here).** The result is
measured on flyvis's averaged representation, not on a single fly's wiring. The column test found
that averaging matters at this scale. One un-averaged FlyWire column has a median containment in
flyvis-30 of about **0.89**, against **0.964** for the averaged bank. That is **Δ = +0.073**,
about 7 points, with `k*` = 9.3 %, **verdict unclear**
(`results/genome/c6/checks/flywire_column_test/RESULT.md`). So the board's perfection may be
partly a product of averaging. A "regrows" reading on flyvis-65 is a reading about the template.
The animal control (§8) is what can carry it to one animal.

**What it is not.**

- It is **not a C6 exam.** It reuses C6's folds, predictors, shuffles and `margin`, but it has its
  own split (one block, not ten folds) and its own verdict. It changes no C6 verdict.
- It is **not question (ii)** (transfer between brains). (ii) stays paused until this is registered
  (Mike, 2026-09-24 20:13 UTC, option A).
- It is **not a claim that no grammar exists** when it fails. A failure is always relative to the
  registered rule and the BF family (§4). Since revision 3.1, G reads "not detected at the R
  level above γ_R; leg P passes from γ\*_P". It names the detection limits that the
  synthetic worlds measure for this instrument (§3.6).

**What it serves (ADR-005 admission rule).** It closes the number the forward path depends on most
directly: whether a rule fitted to the bank *generates* part of the fly it was not shown. That is
what a heritable grammar must do (ADR-005, Rationale).

## 1. The bank, the block, and exactly what is removed

### 1.1 Files and pins

| file | LF sha256 (read 2026-09-24 UTC) | used for |
|---|---|---|
| `results/genome/bank/offsets.csv` | `8c45e8508d8f6ae45e9ab3f9d95d58e4521894ccfa51954f6d77d41e550fa5f0` | flyvis-65, through `harness.REAL` |
| `results/genome/bank/types.csv` | `237a195a36f62ce182fee8486394c27d2beb9825bc029cb215c39c0fa323a477` | names, `type_fields` |
| `results/genome/c6/folds.csv` | `fb6f153b67fe1785a76c3823911e6fbb91cdda57ec952b36c40b4c95f1e213b8` | inner folds for λ (BF_r, rule #2.1) |
| `results/genome/c6/harness.py` | `6fc809527c69ee84aadebfc15c0ba755c189ddc93c80c05c0fa11d969a8d7297` | the harness as rule #2.1 and every P3 run used it |
| `results/genome/c6/rules/second_rule_v21/fit.py` | `92eb6ab1524bb22379b2d21184d10f493ff4c803a41918be8ee16f389a58d16c` | the primary rule's learner |
| `results/genome/c6/rules/second_rule_v21/decode.py` | `39a049013af18a1e89e534d9d378a5f59a772b894d7fab5b79f82f702723a15a` | the primary rule's decoder (pinned by its registration) |
| `results/genome/c6/decoders/bf_decode.py` | `6404210c5e78bbaaa14c6cddc6df7fc41ce958e6ff957c062cc956faad59c1de` | BF_r |
| `results/genome/c6/decoders/n1_decode.py` | `e9eb00e174fa3454046f8cc92439f2132f27697d5b7467bd3f22b64a37c8db96` | N1 |

The script refuses to run if any of these differs.

### 1.2 The block (fixed by decision; not reopened)

- **Sources (8):** Mi1, Tm3, Mi4, Mi9 (ON) and Tm1, Tm2, Tm4, Tm9 (OFF).
- **Targets (8):** T4a, T4b, T4c, T4d (ON edges) and T5a, T5b, T5c, T5d (OFF edges).
- **Cells:** all 64 ordered pairs (source, target). No self-pair lies in the block (sources and
  targets are disjoint).
- **Biology and sources:** the [candidates note §2A](../notes/2026-09-25-knockout-block-candidates.md)
  (Takemura et al. 2013, 2017; Shinomiya et al. 2019; Strother et al. 2017). The ON/OFF split of
  the eight inputs and the T4/T5 split of the eight targets are the **answer key**. They are used
  only to score and to print strata, never to train.

### 1.3 What is removed, entirely

**Removed from training:** for each of the 64 cells, **every row of `offsets.csv` with that (src, tar)**,
whatever its provenance (`in_json`, `hull_filled` or `dropped`), together with all of its fields
(`du`, `dv`, `n_syn`, `n_syn_json`, `sign`, `json_index`, `json_offset_order`), **and the cell's
existence label itself**, present or absent. In harness terms, the training mask is
`~BLOCK` over the 65 × 65 grid. `make_view` (`harness.py:180-186`) then gives the learner neither
the 64 cells nor their content. Nothing about them enters N1's existence fit, its per-source offset
sets, its count terms or its sign votes (`fit_n1`, lines 350-408), BF_r's grid `M` (`_grid`, lines
702-707), or rule #2.1's existence, offset library, counts and sign (its `fit` reads only the view).
The training set is **4,161 of 4,225 cells**. Of these, **572 are present**. The bank has 604
present cells under C6's existence rule (harness line 146), and 604 − 572 = 32, which agrees with
the reviewed count of 32 present block cells.

**Not removed (stated, so that a reader knows what the rule still sees):**

- the 16 types themselves, and every cell of their rows and columns outside the block (their other
  inputs and outputs, their self-loops, the cells among T4/T5 and among the eight inputs);
- the **mirror cells**, the transposes (target → source) of block cells, which lie outside the block
  (§1.4);
- the other known T4/T5 inputs that are among the 65 types: **C3, CT1(M10), CT1(Lo1), Mi10, TmY15**
  (and TmY4 into T5d). Their cells into T4/T5 stay in training. The block is the eight named
  inputs, not "every input of T4/T5". **CT1 is split by flyvis into two compartment types**;
- `view.type_fields` for all 65 types: `stride_u`, `stride_v`, `role` code and `layout` code
  (`harness.py:131-132`). **`types.csv` also has `n_out_entries` and `n_in_entries`, which count
  block entries. These columns are not in `type_fields` and no predictor here reads them;**
- the registry's birth ids for the 64 pairs. They are not read by any predictor.

**Existence under C6** is "at least one non-`dropped` row" (`harness.py:136-146`). The one pair in
the bank whose rows are all `dropped` is Lawf1 → Lawf1, outside the block (checked by name).

**The rule reads no type names (fixed by decision).** Every predictor here sees type *indices* and
`type_fields`, never names. `type_fields` are not names, but they are type annotations, so this is
checked, not assumed. On the block, **all 8 targets share one field group** (role `output`, layout
`output`, strides 1). The sources split into {Mi1, Mi4, Mi9} (`intermediate`) and {Tm1, Tm2, Tm3,
Tm4, Tm9} (`output`); that split agrees with ON/OFF on 7 of 8 sources, since Tm3 is ON. Rule #2.1's
field term is `W[G(s), G(t)]` (`second_rule_v21/fit.py`, `groups`, `group_design`). Because `G(t)`
is constant over the 8 targets, that term is a function of the source alone on the block. It is
therefore additive there, and by §0 it contributes exactly zero to the parity contrast. **The field
channel cannot carry the board.** (Values read from `types.csv` by name, §1.4.)

### 1.4 Printed before data: inferability, mirrors, what each endpoint keeps (computed now)

Computed by one scratch script (outside the repository, not committed) from the names in
`types.csv` and from presence in `offsets.csv` **after the 64 block cells were dropped**. No weight
was read. Presence means C6 existence, as in §1.3.

**What each endpoint keeps in training** (present cells outside the block, self-loops included):

| source | training targets | training sources | | target | training sources | training targets |
|---|---|---|---|---|---|---|
| Mi1 | 25 | 17 | | T4a | 8 | 9 |
| Tm3 | 18 | 12 | | T4b | 6 | 6 |
| Mi4 | 23 | 17 | | T4c | 8 | 7 |
| Mi9 | 21 | 19 | | T4d | 6 | 6 |
| Tm1 | 24 | 15 | | T5a | 4 | 7 |
| Tm2 | 18 | 13 | | T5b | 5 | 8 |
| Tm4 | 18 | 14 | | T5c | 4 | 7 |
| Tm9 | 9 | 14 | | T5d | 6 | 6 |

Each of the eight targets keeps its self-loop, which is counted above. Its other training sources
are C3, CT1(M10), Mi10 and TmY15 (T4), or CT1(Lo1) and TmY15 (T5), and the T4/T5 cells among
themselves. T5d also keeps TmY4.

**Johnny's inferability table on flyvis-65.** A block cell is *inferable* if its source has at
least 2 training targets and its target has at least 2 training sources.
**Result: 64 of 64 cells are inferable.** The thinnest endpoints are Tm9 (9 training targets) and
T5a and T5c (4 training sources each, 3 without the self-loop). **T5d is not a special case on
flyvis-65:** it keeps 6 training sources and 6 training targets. The note's "T5d leaves training
entirely" holds on FlyWire-30 only. So the T5d stratum of the candidates note is not needed here.
Per-type rows are still printed (§3.5).

| bank | inferable block cells | status here |
|---|---|---|
| **flyvis-65** | **64 / 64** | primary (computed for this draft) |
| FlyWire-30 | 14 / 64 | provenance only (Johnny, review of 2026-09-24) |
| male CNS v1.0 | 64 / 64 at every pair threshold tried (Zcode, preliminary graph, review 2026-09-24 20:59 UTC) | control arm; recomputed from the built bank and printed before its data (§8) |

**Mirror cells on flyvis-65.** A mirror cell is a present transpose (target → source) of a block
cell. **5 mirror cells are present:** (T4a, Mi9), (T4b, Mi9), (T4c, Mi9), (T5b, Tm2), (T5c, Tm2).
(On FlyWire-30 the count is 3 and on flyvis-30 it is 5; Ark, in review.) The run prints the rule's
predictions for their 5 block partners, (Mi9, T4a), (Mi9, T4b), (Mi9, T4c), (Tm2, T5b) and
(Tm2, T5c), on a line of their own, and the AUC on the other 59 cells beside the AUC on all 64
(§3.5). **None of the predictors here ties a type's source factor to its target factor.** BF_r's
`U` and `V` are separate, and rule #2.1 has one `(u, v)` pair plus the group-level `W`. So a mirror
cell (T4a, Mi9) enters `U[T4a]` and `V[Mi9]`, not `U[Mi9]·V[T4a]`, and it is not a direct channel.
The mirrors are printed so that a reader can check this.

The script recomputes all three tables at run time and stops if any differs from this section
("PRE-DATA TABLES DIFFER").

## 2. The predictors

### 2.1 The primary rule (proposal on the reading of "the registered C6 rule"; D1)

**Rule #2.1**, `second_rule_v21_r1`, **RANK = 1**. It is the only rule that has been registered for C6
and run on it: registration
[`2026-09-23-rule-2-1-registration.md`](2026-09-23-rule-2-1-registration.md) (committed
`15da501`); code `results/genome/c6/rules/second_rule_v21/`; C6 run
`rule_runs/second_rule_v21_r1/` at `k = 10` starts, `r = 1`. Its existence model is
`N1 + u·v + W[G(s), G(t)]` (the rule's proposal §2.2), and its rank was fixed by A11's arithmetic
(`RANK = 1`, `test_rank_is_registered_value`). On C6 it failed on offset but **passed existence on
P1, P3 and P4** (its outcome note, §1). Existence is the only field this registration reads, so
nothing in that failure bears on this test. It is run through its plug-in interface
(`harness.load_rule`) with `STARTS = 10`, unchanged.

The other reading, recorded under D1: "the registered rule and rank" as **BF_1**, the harness's
trained factorisation at the rule's P4 rank, registered for P3 in
[`2026-09-24-bf1-p3-registration.md`](2026-09-24-bf1-p3-registration.md) (`e3f17cb`). Either way
BF_1 is run (§2.2), so neither reading loses a number. What changes is which one the verdict is
read from.

### 2.2 The BF family, all ranks printed

`harness.bf_predictor(r)` for **r ∈ {1, 2, 3, 4}**, the family of the FlyWire registration
([`2026-09-24-flywire-bf-p3-registration.md`](2026-09-24-flywire-bf-p3-registration.md);
Bonferroni `0.05 / 4 = 0.0125`). Each one is fitted by `fit_bf` unchanged: N1 first, then λ from
`BF_LAMBDAS` by the nested inner folds of `folds.csv`, restricted to the training view, with ties
going to the larger λ, and `k = 10` starts. The λ chosen for each fit is printed. BF_r is a
learnable, name-free predictor. It serves as **the information-available probe** of §4 (branch W),
and every rank is printed whatever the verdict. (D6: whether to add r = 8, the rank of M4.)

### 2.3 N1: in the table, declared uninformative in both directions

`harness.N1` (`fit_n1`) on the same training mask. Its existence logit is `c + a_s + b_t`
(ridge, `LAMBDA = 1`).

- **The parity contrast is identically zero (Ark's algebra, fixed by decision).** Let the contrast
  be `D(z)` = mean of `z` over the 32 board cells minus mean over the 32 cross cells. Then
  `D(c + a_s + b_t) = 0` for every `a` and `b`, because every source row and every target column
  holds 4 board and 4 cross cells. So on the real block, "the rule beats N1 on `D`" is the same as
  "the rule has a non-additive part of the right sign". That is too weak to count as a leg: a
  vanishing interaction passes it. And "N1 is not beaten" cannot be read as smoothing either
  (Johnny's reading of its sign). **The N1 leg decides nothing.** N1's numbers are printed, and
  `|D(N1 logit)| < 1e-9` on the real block is a **machine check** (§3.4). It verifies that the board
  is balanced and that N1 is additive.
- **AUC is not pinned at 0.5 for an additive score (checked for this draft; algebra, no bank).**
  The zero holds for the linear contrast `D`, not for rank statistics. On the 8 × 8 board with the
  board cells present, 200,000 random additive scores `a_s + b_t` (normal `a` and `b` with a random
  scale; numpy `default_rng(0)`) gave an AUC from 0.400 to 0.599, with the 1st to 99th percentile
  at 0.469 to 0.531. A hill-climb found 0.629. Ark's independent draw (review, 2026-09-24 20:56
  UTC) gave 0.433 to 0.590, with the 1st to 99th percentile at 0.466 to 0.534. The two draws differ
  in their tails, as independent draws do, and agree on the point. **So the reading is "the N1 leg
  decides nothing", not "N1 sits at 0.5".** N1's AUC on the real block can lie anywhere in this
  band. This is why the shuffles leg subtracts N1's AUC on every bank (§3.2). (Ark retracted his
  earlier phrasing in the same review; revision 1's wording stands.)

### 2.4 The block is rank 1, and the two ceilings (revised in revision 2)

**The board is exactly rank 1 (Ark, review finding 5).** Write presence on the block in ±1 form:
`y_st = +1` if the cell is present and `−1` if it is absent. Let `x_s = +1` for the ON inputs (Mi1,
Tm3, Mi4, Mi9) and `−1` for the OFF inputs (Tm1, Tm2, Tm4, Tm9), and let `w_t = +1` for T4a–d and
`−1` for T5a–d. Then **`y_st = x_s · w_t` on all 64 cells**: ON × T4 and OFF × T5 give +1, and
the two cross quadrants give −1. The board is the outer product of one source vector and one
target vector. Three consequences follow before any data:

1. **The R world is realisable for a rank-1 rule.** The `u·v` term of rule #2.1, and BF_1's single
   factor, can represent the board exactly. The additive terms are constant on it, because every row
   and column holds 4 of 8 (§0). So "regrows" is within the primary's reach by construction, and a
   failure to regrow is not a failure of rank on the block itself.
2. **`ceiling_block` ≈ 1 in every world.** The real block is a board, and so is every block of
   §3.6 (by `z` or by `z'`), so each of them is rank 1. A rank-1 rule trained on the 64 cells alone
   can hold any of them. The expressivity gate for G (below) is therefore expected to pass
   everywhere. What it catches is a failure of the fit itself, such as a λ that shrinks the
   interaction to nothing or an optimiser that misses it. It does not catch a lack of rank.
3. **Permuted-block ceilings fall.** A uniform permutation of the block keeps 32/32 present but is
   almost never rank 1. Only 15,470 of the C(64, 32) ≈ 1.8 × 10^18 patterns with 32 present
   are rank 1 (algebra: a ±1 outer product has 32 present only if the source vector or the target
   vector is split 4/4). A rank-1 rule cannot hold a permuted block even in-sample, so its ceiling
   there should fall well below the real block's. **That fall carries information** (D9; Johnny,
   Ark finding 5). It shows that the real block's high ceiling comes from its rank-1 structure, not
   from a capacity to hold whatever the rule is shown.

**Two ceilings (Ark, review finding 1; Johnny showed that findings 1 and 3 are one defect).**
Revision 1 had one ceiling: the rule trained on the full bank and scored in-sample on the block.
That number mixes two questions. A block that contradicts its surroundings pulls it down even when
the rule could hold the block alone, so revision 1 would have read an orthogonal block as "the rule
cannot hold it" (U) (Ark, finding 3; the No world of §3.6). Revision 2 separates the two:

- **`ceiling_full`**: the rule is trained on the full bank (all 4,225 cells) and scored in-sample
  on the 64 block cells. One set of parameters must hold the block and its surroundings together, so
  **it measures whether the block is consistent with its surroundings.**
- **`ceiling_block`**: the rule is trained **only on the 64 block cells** (training mask = `BLOCK`,
  with λ chosen as in §2.2 by the nested inner folds of `folds.csv` restricted to those cells) and
  scored on them. **It measures pure expressivity.**

Both are computed for the primary and for each BF_r. **Both are printed on the verdict line**
(§4). Their roles:

- **The expressivity gate for G is `ceiling_block ≥ 0.90`** (§4). Below it, the rule cannot hold
  the block even when shown nothing else, and a failure to regrow says nothing (U). **Revision
  3.2:** the gate cut is a constant of its own (`GATE_CUT` = 0.90), and the G label names its
  gate variable, rule #2.1's `ceiling_block`. The gate never bound in the pre-run:
  `ceiling_block` = 1.0 in all 225 rule #2.1 and BF rows (N1's rows are 0.5 by construction). A
  U caused by it prints as a failed fit (§4). **Revision 3.3 (A4):** a `ceiling_block` that was
  not measured is not a failed fit and is not "below 0.90"; it has its own reason and its own U
  text (§4).
- **A low `ceiling_full` with a high `ceiling_block`** means that the block does not follow from its
  surroundings: the rule can express it but not together with the rest of the bank. Following
  Johnny, this is routed to **G**. Revision 2 labelled it by mechanism, so that one letter did not
  name two mechanisms:
  - **"orthogonal: block not implied by surroundings"** when `ceiling_full < 0.90`;
  - **"no information"** when `ceiling_full ≥ 0.90`: the block agrees with its surroundings
    when shown, but the surroundings do not carry it.

  **Revision 3 (decision (c), all three reviewers): the two mechanism labels are description
  only.** Both ceilings are reported, and the label is printed beside G as "mechanism,
  description only". No decision, requirement or consequence is read from it. The reason is
  measured. In the revision-2 run, 2 of the 5 Nf worlds, which carry no information by
  construction, read "orthogonal". Their full-bank fit had selected λ = 100, so `ceiling_full`
  fell to 0.51 and 0.55 (§3.6, "What the runs found"). `ceiling_full` therefore depends on the
  λ switch (§6), and it does not separate the two mechanisms.

  **Revision 3.2 (A5): one threshold on two variables, split.** Revision 3.1 used one constant,
  0.90, both to gate G on `ceiling_block` and to pick the mechanism word on `ceiling_full`. They
  are now two named constants, the gate cut (`GATE_CUT`) and the mechanism cut
  (`MECHANISM_CUT`), both 0.90, so nothing changes numerically. **The mechanism cut is borrowed
  from the gate and not calibrated:** in the pre-run table `ceiling_full` ranges from 0.457 to
  1.0 and is below 0.90 in 89 of its 270 rows. The description now says whose `ceiling_full`
  it quotes ("rule #2.1's ceiling_full = …"). It is a world-level text, repeated on all six rows
  of a world in `synthetic_worlds.csv`, so without the name the rows of BF_r and N1 seemed to
  quote their own column (§7).

Printed beside the ceilings, as within-fly variation and not as a cut: one FlyWire column
differs from FlyWire-30 by a median of **34 extra and 27 missing pairs** out of 900 cells (column
test, verdict line). Spread evenly, that is about 4 of 64 cells. The column test's `X_c` = 0.54
shows the noise is not spread evenly, so this is not a cut (candidates note §3.2).

**Ceilings on permuted blocks (proposal, D9; printed, decides nothing; `ceiling_full`).** The
primary rule is also trained on the full bank with the block replaced by 20 uniform within-block
permutations (seeds §3.7) and scored in-sample on each permuted block. That is **`ceiling_full`**
on each permuted block. By consequence 3 above, these ceilings are expected to fall, and the fall is
the reading: the real block is held because it is rank 1 and consistent with its surroundings. If
the rule held a permuted block about as well as the real one, its in-sample fit of the block would
be capacity, not structure. That is the "smoothing" reading of Zcode's null in the one arm where the
block is seen (§3.2 explains why the knockout arm cannot carry it).

## 3. Statistics (all proposals; D2–D5, D9, D10)

### 3.1 The metric on the block (proposal, D2)

For a predictor's `p_exist` on the 64 block cells and the bank's labels there:

- **Primary: AUC**, the Mann-Whitney probability that a present cell outranks an absent one, with
  ties counted as ½. The labels are balanced, 32 present and 32 absent. AUC is scale-free, so a
  heavy λ shrinkage does not hide a correct ordering, and 0.5 is chance whatever the predictor's
  calibration. The harness has no AUC. The script computes it in one function over the 64 cells,
  and the machine check tests that function on hand-made inputs (§3.4).
- **Printed beside it, deciding nothing:** the parity contrast `D` of the predictor's logit (N1's
  is 0 by §2.3, in floating point within `PARITY_TOL` = 1e-9 of 0, as check 5 registers it, not
  exactly 0.0; for the rule, `D` equals the parity contrast of its non-additive part); the
  harness's existence log-loss on the 64 cells and its margin over N1, the C6 convention (`score`,
  `margin`); precision at 32 (the share of present cells among the 32 highest `p_exist`, which
  equals accuracy on this balanced block); the mean `p_exist` of each quadrant (ON×T4, OFF×T5,
  ON×T5, OFF×T4); and the regrown share of each ceiling, `(AUC − 0.5) / (AUC_ceiling − 0.5)`,
  computed once against `ceiling_full` and once against `ceiling_block` (§2.4), and printed as
  "n/a" when that ceiling is `<= 0.5`. **Revision 3.2: despite its name, the regrown share is a
  ratio, not a share.** It can exceed 1 (a knockout AUC above the ceiling) and be negative (an
  AUC below 0.5). The CSV columns keep their names, `regrown_share_full` and
  `regrown_share_block`.

### 3.2 The legs

**Leg S, the 99 degree-preserving shuffles (fixed by decision; the statistic is a proposal, D3).**
For `sd` in 0..98, take `harness.shuffled_bank(REAL, sd)`: the same 99 banks every C6 P3 and every
BF P3 run used. Apply the **same 64-cell knockout by name**, fit the predictor and N1 on the
remaining 4,161 cells, and score both on the shuffled bank's own 64 block cells. The statistic on
each bank is the **AUC margin over N1**, `M = AUC(rule) − AUC(N1)`, matching P3's margin over N1
(`run_exam`, lines 1010-1022). A shuffle keeps degrees, so N1's AUC on a shuffled block can be well
above 0.5; subtracting it removes the degree channel on every bank alike.

- A shuffle whose block is all present or all absent has no AUC. Its number, `n_deg`, is always
  printed. **Revision 3 (D14 (ii), decision (d), all three reviewers): a degenerate shuffle is
  excluded from leg S**, and leg S counts against the `99 − n_deg` shuffles that have an AUC. A
  shuffle with no AUC on the block says nothing for or against the rule. Revision 2 counted it as
  ≥ real (D14 (i)), and then one degenerate shuffle made leg S unpassable for every predictor, and
  with it R and W (CC, 2026-09-24 21:10 UTC).
- `n_ge` = number of **non-degenerate** shuffles with `M_sd >= M_real − TAU` (`TAU = 1e-9`, the
  harness's tie band).
- **`TAU` is inert here (revision 3.2, text only).** An AUC on a block with 32 present and 32
  absent cells is a multiple of 1/2048 (it is (2·gt + eq)/2048), so for the AUCs of leg P and of
  its row-and-column variant, `x >= y − TAU` holds exactly when `x >= y`. In `n_ge` a shuffle's
  margin is scored on the shuffled block, whose present count need not be 32, so its AUCs are
  multiples of 1/(2 · n_present · n_absent). Two unequal margins then still differ by far more
  than 1e-9, and `TAU` can at most turn a floating-point rounding difference between two equal
  fractions into a tie. The tie band that matters is the λ tie in fitting (`LAMBDA_TIE`: held-out
  log-likelihoods within 1e-9 go to the larger λ, §6).
- **The γ_R input chain and `TAU`, stated once (revision 3.3, B4).** Leg S reaches γ_R through
  this chain: a shuffle's `present` (its block's present count) → degenerate when `present` is 0
  or 64, where `auc` returns no value (script, `auc`) → `n_deg` → `n_valid` = 99 − `n_deg` →
  `p_S`; a degenerate shuffle is excluded from `n_ge` (`evaluate_bank`). `n_ge` compares
  `M_real`, a difference of two AUCs on the 32/32 lattice (steps of 1/2048), with each shuffle's
  margin, a difference of two AUCs on that shuffle's own lattice (steps of 1/(2 · present ·
  absent)). **`TAU` is inert because the lattice gaps are far larger than `TAU` and the
  floating-point rounding is far smaller:** two unequal values on these lattices differ by at
  least 1/(2048 · 2 · present · absent) ≥ 1/2048² ≈ 2.4e-7, while rounding in double precision
  is of order 1e-16. The reading does not rest on the 1/2048 lattice alone. `TAU` is a tie
  policy, not the instrument's resolution (§12, error ledger).
- `p_S = (1 + n_ge) / (1 + 99 − n_deg)`. **Leg S passes** iff `n_ge = 0` and at least one shuffle
  has an AUC. With `n_deg = 0`, that is `p_S = 0.01`, as in revision 2.
- **Degenerate shuffles on the verdict line (Ark, review finding 4; kept in revision 3).** If
  `n_deg > 5`, the verdict line names `n_deg`, says that these shuffles are excluded, and gives the
  count that leg S uses, `99 − n_deg`, with the smallest `p_S` it allows, `1 / (100 − n_deg)`.
  Every world of both synthetic runs had `n_deg = 0` (§3.6), so the change alters no reading.
- Printed per shuffle: the block's present count, `AUC(rule)`, `AUC(N1)`, `M`, and the λ chosen
  (the FlyWire outcome note, §3, showed the λ record is where a near tie is read).

**Leg P, the permuted block (Zcode's null, fixed by decision).** The labels of the 64 block cells
are permuted uniformly within the block, which keeps 32 of 64 present and destroys the board. The
statistic is the predictor's AUC against the permuted labels.

- **What this leg is, stated plainly.** Training never sees the block (§1.3), so the regrown
  prediction is **byte-identical** whether the block holds the real or a permuted content. The
  script checks this (§3.4, leakage check). Leg P is therefore an exact label-permutation test of a
  fixed prediction. A rule "regrows the permuted block as well as the real one" only when its
  real-block AUC is within the permutation null. The `ceiling_full` on permuted blocks (§2.4) carries
  the other half of Zcode's worry, a rule that fits whatever it is shown.
- 9,999 permutations from one generator (seed §3.7). `p_P = (1 + #{AUC_perm >= AUC_real − TAU}) /
  10,000`. **Leg P passes** iff `p_P <= 0.01`. For 32/32 labels the null AUC has standard deviation
  `sqrt(65 / (12 · 32 · 32))` = 0.0727. So `p_P <= 0.01` needs an AUC of about 0.67 or more (both
  confirmed by Ark, review 2026-09-24 20:56 UTC). The script prints the exact smallest passing AUC
  from its own 9,999 draws.
- **`smallest_passing_auc` (revision 3.3, B1).** It is the lowest AUC on the k/1024 grid whose
  own null (the 9,999 draws) gives `p_P <= 0.01`. It depends on the block's labels `y` through
  `Yu = y[uniform_perms()]` (script, `evaluate_bank`), not only on their count, and on no fit, so
  it is γ-blind: the same at every γ from 0 to 2. It is a translation anchor between the AUC axis
  and `P_R`, not a γ limit. **Pre-run values: two numbers, split by the No family:** 0.666015625
  (682/1024) in 40 worlds and 0.6728515625 (689/1024) in the five No worlds (seeds 90120–90124),
  whose board follows `z'` instead of `z` (read from the pre-run `synthetic_only.json` and from
  the `--from-raw` re-read of revision 3.3). **Observation (Ark 15:22):** the pinned
  `synthetic_worlds.csv` has `board` = `z` in 40 worlds and `z'` in the 5 No worlds (checked on
  the pinned file), the same 40/5 split as `smallest_passing_auc`; the board is the carrier of the
  dependence on the layout `y`. This is an observation: its falsifier (recompute with board `z`
  at the same `y`) was not run.
- **Printed beside it (proposal, D4; decides nothing):** the same test under **row-and-column-preserving
  permutations** of the block. These are random 8 × 8 patterns with 4 present in every row and
  every column, drawn by 20 × 32 successful checkerboard swaps from the real pattern, 9,999 draws.
  They keep the block's within-block degrees, as the real board has them, and ask whether the rule
  found *this* board rather than any balanced one.

**Leg N1 (fixed by decision): printed, uninformative in both directions** (§2.3). No branch reads it.

### 3.3 Uniqueness and determinism

- **Run once.** The real arm is run once, at a committed head, with the tree clean under
  `results/genome/c6/` and `docs/plans/` (the refusal of `harness.rule_run`, reused).
  **`--allow-dirty` (revision 3.3, A7):** the option lets the real arm run on a dirty tree, which
  is useful for dry runs. **A real-arm run made with `--allow-dirty` is not the registered run**:
  its manifest records `not_the_registered_run`, its verdict line ends with "NOT THE REGISTERED
  RUN: made with --allow-dirty; this verdict cannot be cited as the registered result", and it
  cannot be cited as the registered result.
- **One manifest, from a clean committed tree, and the pre-run table reproduced (revision 3.1;
  Johnny 09:33, Zcode 09:34 UTC).** This file and the script were edited after the pre-run
  synthetic numbers were produced (header), so those numbers are pre-run values. The registered
  run recomputes everything, the synthetic step included, from a clean committed tree, in one run
  and one manifest. It refuses `--from-raw`. **It must reproduce the pre-run table**: with the
  same seeds and the same pinned environment (Zcode), its `synthetic_worlds.csv` must equal the
  pre-run file on the deciding columns (revision 3.2, below; revision 3.1 asked for byte
  identity). If it does not, the two-world check fails and the real arm does not run, just as
  when a stop row fails (§3.6).
- **The reproduction gate (revision 3.2; Johnny blocked the byte-for-byte stop as written, Ark
  asked for changes; V1 in §10).** *Why the gate changed.* The pinned `synthetic_worlds.csv` was
  written by a `--synthetic-only --from-raw` pass (its `SYNTHETIC.md` records "0 new world fits"
  and a runtime of 8 s), and the saved fits it read are mixed: 30 worlds were fitted by the
  revision-2 run (families R, Nf, No, W, M0.5, M1.0) and 15 by the revision-3 run (M0.6, M0.75,
  M0.85). The code of revisions 2 and 3 is not in git.
  *Why a byte-for-byte stop is not the gate: four reasons (revision 3.3, B7; V1 in §10).* (1) The
  fits are of mixed generation (revision 2 and revision 3, above). (2) The reference has no
  producer in git (the provenance below). (3) Byte identity is a fact of one machine: OpenBLAS
  chooses its kernel at run time (`DYNAMIC_ARCH`), and the kernel is not pinned. (4) gzip writes
  its mtime into the header of `raw_fits.json.gz`, so that file differs in bytes on every run;
  this is the only one of the four reasons that also applies to every future run.
  *Provenance of the reference (revision 3.3, B6).* Its producer exists only as a hash. The
  pinned `synthetic_only.json` manifest records revision "3", `script_sha256_lf` `508f4b17…`,
  `registration_sha256_lf` `4c88d602…`, `git_head` `ea60011` and `tree_dirty_under_c6_or_plans`
  true. At `ea60011` neither file was tracked, and no committed version of either file
  (`8a514fa`, `52eb381`) has those hashes. The report (`SYNTHETIC.md`) names no input, and the
  manifest's `from_raw` is a path in a Temp scratchpad. CC's probe P2 (below) established the
  input's identity by content.
  *Measured facts* (CC, 2026-09-25, this machine, `tools/.venv`, one process):
  (a) fresh fits by the revision-3.1 code of all 45 worlds × {N1, rule #2.1, BF_1–BF_4} on the
  knockout (`ko`) view equal the pinned `raw_fits.json.gz` bit for bit: 270 of 270, max |Δp| = 0,
  no λ and no label difference, in every family, M0.5 and M1.0 included. This covers 6 of the 637
  saved keys per world. The 99 shuffles (`|sh:`, 594 keys) and the 20 permuted-block ceilings
  (`|pc:`) were not recomputed. γ\*_P and the family limit rest on `p_P`, which uses the
  knockout fit's AUC (covered); γ_R also needs leg S, which counts the 99 shuffled fits (not
  covered; revision 3.3: covered for three worlds, fact (c)). (b) The revision-3.1 writer on the
  pinned fits (`--synthetic-only --from-raw`, 12 s; 13:40 UTC) reproduced the pinned CSV byte for
  byte (sha256 `7a2f0295…c8f1`). Revision 3.2 then changed
  the text of column 8 (§2.4): its own `--from-raw` re-read of the pinned fits (12 s, into a
  scratch directory) gives outcome 1 below, every deciding column equal, with column 8 differing
  on 84 rows and nothing else differing.
  *Measured facts added in revision 3.3* (CC's probes, posted 15:1x UTC; this machine,
  `tools/.venv`, the code of `52eb381`). (c) **P1, a fresh refit against the pinned
  `raw_fits.json.gz`**, in a 30-process pool, 581 s, every field compared (`p` on all 64 cells as
  exact lists, `lam`, `y`, and the whole `score` dict: existence, offset, counts, sign, `n_ne`):
  the base `ko` arm, all 45 worlds × 6 predictors, 270 of 270 equal; `|sh:`, all 99 shuffles × 6
  predictors for the worlds M0.6:0 and M0.75:0 (the γ_R bracket, revision-3 fits) and M0.5:0
  (the minus side of γ\*_P, revision-2 fits), 1782 of 1782 equal; `|pc:`, the 20 ceilings of the
  same 3 worlds, 60 of 60 equal. Total 2112 of 2112. Not recomputed: `|sh:` and `|pc:` of the
  other 42 worlds. (d) **P2, the input of the reference.** The file that the pinned manifest names
  as `from_raw` (…/scratchpad/knockout_synth/rev3/raw_fits.json.gz, in a CC scratchpad of
  2026-09-24/25) exists; compared with the pinned store as objects through `read_raw`, it has the
  same 28,665 keys, and 5 records differ, only in their `secs` field (`world:W:0`, `ko1`, rule
  #2.1 and BF_1–BF_4); `p`, `y`, `lam` and `score` are equal. The pinned `raw_fits.json.gz` is a
  byte copy of the reference pass's own output (…/rev3_final/raw_fits.json.gz, sha256
  `91035a…`). The revision-2 run's store (…/full/, 18,960 keys) equals the pinned store on every
  shared key. (e) **The `--from-raw` re-read of revision 3.3** (the drafting subagent, 13 s, into
  a scratch directory): outcome 1; rows matched by key, none missing on either side, row order
  equal; column 8 differs on 84 rows, and all 84 are exactly revision 3.2's rename; the recomputed
  CSV is byte-identical to revision 3.2's re-read (sha256 `32d62c71…95c1`).
  *The gate.* The fresh CSV is compared with the pinned CSV on the deciding columns, not by
  bytes. **Revision 3.3 (item ㉗): rows are matched by key**, (`family`, `j`, `seed`,
  `predictor`), not by position. Three outputs are kept apart: rows missing on either side (a
  duplicated key counts with them); key-matched rows whose values differ; and a change of row
  order, which is recorded as a fact and does not by itself give outcome 3.
  **Exact comparison** for the identity columns of a row (`family`, `j`, `seed`,
  `gamma_z`, `gamma_z1`, `board`, `predictor`) and for the lattice columns: `label`,
  `outside_density`, `auc`, `precision_at_32`, `ceiling_full`, `ceiling_block`, `M_real`,
  `n_ge`, `n_shuffles`, `n_deg`, `n_valid_shuffles`, `p_S`, `p_P`, `p_P_rowcol`, `lambda_ko`,
  `lambda_full`, `lambda_block`, `auc_other_59`, `auc_fixed_lambda1` and `p_P_fixed_lambda1`.
  Their values are exact dyadic or rational fractions with steps of at least 1e-4, so a tolerance
  adds nothing. (The per-γ counts seen/n and R/n are not columns; they are counts of `p_P` and
  `label`, which are compared.) **Within `MACHINE_CHECK_TOL` = 1e-9**, in each column's own
  units, for the continuous columns `D`, `logloss`, `logloss_margin_over_N1`,
  `regrown_share_full` and `regrown_share_block` (the last two are (AUC − 0.5)/(ceiling − 0.5), a
  ratio that is not on a lattice and amplifies a difference up to 512 times when the ceiling is
  near 0.5). The constant's name is reused from `bf1_p3.py`; `TAU` is not reused for it.
  **`mechanism_description` (column 8) is excluded from the deciding set**: it is a world-level
  text derived from rule #2.1's `ceiling_full` and repeated on all six rows of a world. It is
  compared after rule #2.1's `ceiling_full`, which is compared exactly, and its differences are
  reported, not gated. **Revision 3.3 (C5):** each column-8 difference is checked against
  revision 3.2's rename: the pinned text with "(ceiling_full X" rewritten as "(rule #2.1's
  ceiling_full = X" must equal the fresh text; the report counts the differences that are
  exactly the rename and prints those that are not. **Byte identity is recorded in the manifest
  as a fact** (`prerun_csv_byte_identical`), not used as the stop.
  *Outcomes and their treatment, written before the run (revision 3.3 replaces revision 3.2's
  treatment; items F1, ㉖, F10).* (1) Every deciding column equal: the gate passes. (2) Only
  continuous columns differ, within `MACHINE_CHECK_TOL`: the gate passes, and the report records
  which columns and the largest difference. (3) Otherwise the real arm does not run, and the
  table is not re-pinned. **Outcome 3 is split by what differed:** (a) identity or lattice (the
  header, a missing, duplicated or malformed row, or an identity or lattice column); (b)
  continuous (a continuous column beyond `MACHINE_CHECK_TOL`). The reason and the treatment
  branch on which part is non-empty. **The treatment names four layers and how each is told
  apart:** (i) *the fits*, told apart by the per-key diagnostic (`raw_fits_diagnostic`, below),
  by kind (`ko`, `full`, `block`, `ko1`, `sh`, `pc`) over all 637 keys per world, read in the
  treatment text; (ii) *the leg-P null generator* (`uniform_perms`, `rc_patterns`), told apart by
  the null-input digests (below); (iii) *the consumer* (`auc_null`, `avg_ranks`, `auc`,
  `parity_D`), which is what differs when the fits and the null inputs are equal and the null
  outputs are not; (iv) *the machine* (the BLAS kernel that `DYNAMIC_ARCH` chooses). **Order of
  reading:** the per-key diagnostic first; then the null-input digests; then the null outputs;
  the machine is what remains, and it cannot be separated today. Part (b) alone excludes layer
  (ii): the continuous columns are functions of the fits' `p` (`D`, the log-losses) or of lattice
  columns (the regrown shares), and the null enters only lattice columns (`p_P`, `p_P_rowcol`).
  **The cross-configuration self-test** (the synthetic step run once more with a different
  thread setting, into a new folder, and compared with the first run) has these outcomes:
  (1) self-identical and still different from the pinned table: a code difference **or** a
  machine difference; they cannot be told apart today, and both are named; (2) the rerun differs
  from itself: the gate itself is not self-consistent, and the run stops with that text.
  **Mechanism:** the four thread variables must be exported in the shell before launch, because
  the script's `setdefault` does not override a value already set; a naive rerun sets them to 1
  again and is identical. The code declares one BLAS thread per process, so varying the threads
  tests that claim, not the machine. (Revision 3.2 read the self-test as "self-identical and
  still different means an implementation difference; not self-identical means machine
  non-determinism". That reading was wrong: determinism within one version of the code is not
  invariance to the environment; §12, error ledger.) Either way the result goes to the chat. The
  script prints this treatment, branched on (a) and (b), on a failure (`repro_fail_treatment`);
  it does not run the self-test by itself. A red pin is never answered by re-pinning (§7,
  "Recreating the reference").
  *Null-input digests (revision 3.3, F10).* The manifest records, and the log prints, the sha256
  of the `uniform_perms()` matrix and of each `rc_patterns(y)` matrix, the latter as a dict keyed
  by the sha256 of the `y` bytes (the key of the `rc_patterns` cache), each over exactly the
  object that the null is computed from (`null_input_digests`). They are computed in the main
  process, where every null is computed; the pool workers compute no null (they use
  `uniform_perms` only for check 6's leak bank), so no per-worker digest is collected. None is
  needed for `perm_ceiling_perm`: its outputs are the `|pc:` fits, which are store keys, and
  `evaluate_bank` asserts their labels. The pinned reference records no digests, so they can be
  compared only between runs of this code.
  *Pins.* The script checks every file listed in the pre-run `SHA256SUMS.txt`, against the list
  and against the pins of §7, not only the CSV pin (Ark; Johnny noted that the list already
  names all five files). **Revision 3.3 (C6):** entries of the folder that are neither listed nor
  pinned, such as the `provenance/` subfolder of §7, are reported, not failed.
  **A pin is integrity, not reproducibility (revision 3.3, B2, item ㊱).** `raw_fits.json.gz`,
  and the real arm's `raw_fits_real.json.gz`, cannot be byte-reproduced by any run: gzip writes
  its mtime into header bytes 4–7 (Johnny's probe, 14:25 UTC: the same payload written 1.2 s
  apart gave different sha256). Reproducibility is claimed per file and per field, never for the
  `.gz` bytes. **`secs` is the second non-reproducible field** (revision 3.3, item 4): the gzip
  mtime is in the container, `secs` (the seconds a fit took) is inside every JSON record. The
  per-fit comparison excludes it by name.
  *Per-fit diagnostic (decides nothing).* The fresh run's fits are compared with the pinned
  `raw_fits.json.gz` key by key (`p_exist` on the 64 block cells, the selected λ, the labels),
  split by the worlds fitted by revision 2 (30) and by revision 3 (15), and by kind of fit.
  **Revision 3.3 (A8, item ㊲):** it also compares the `score` fields key by key (existence,
  offset, counts, sign, `n_ne`, and `sign_n` where both records hold it) and reports the
  differences per kind: three of the four C6 fields (offset, counts, sign) are not functions of
  `p` and enter no other channel. New raw records store `sign_n`, the integer, beside the older
  fields (C7). **Declared fields (revision 3.3, item ㊲; Ark 15:19, Johnny 15:19):** a store
  record has six fields, `p`, `y`, `lam`, `score`, `outside_density` and `secs`; 47 `ko1`
  records of the pinned store carry a seventh, `reused_from_ko`, the flag of a fixed-λ record
  copied from a knockout fit that selected λ = 1 (read from the pinned `raw_fits.json.gz`: 28,618
  records with six fields, 47 with seven). Compared exactly, key by key
  (`STORE_FIELDS_COMPARED`): `p`, `y`, `lam`, `score` (the `SCORE_FIELDS` that both records hold)
  and `outside_density`, which differs between a world's base bank and its shuffled banks, so it
  is compared only between records of the same key. Excluded by name (`STORE_FIELDS_EXCLUDED`):
  `secs`, a timing, and `reused_from_ko`, bookkeeping whose record's `p` is compared. The script
  asserts that every field it sees is declared in one of the two; the re-read of revision 3.3
  (second pass) passed that assert on all 28,665 pinned records. **Revision 3.3 (A6):** under `--from-raw` the diagnostic says what it compares;
  when the re-read store is the pinned one, it reads "re-read: compares the pinned store with
  itself; carries no information", apart from the fits that the pass itself made
  (`fitted_this_pass`).
  **What the gate covers (revision 3.3, B5, items ㉚ ㊶).** The gate compares the deciding columns
  of `synthetic_worlds.csv` only. It does not compare the synthetic summary values in
  `summary.json` (committed, and written only by the real arm in step 5): the synthetic
  `per_shuffle` records (the input of γ_R), the verdict lines, `smallest_passing_auc` and the
  permuted-block ceilings. The `per_shuffle.csv` in the committed outputs carries the **real**
  arm's shuffles: the same name as the synthetic `per_shuffle` in the JSON, a different object.
  The synthetic half of the registered run writes nothing to the repository by itself: its
  values reach the committed outputs only through step 5 of the real arm (`write_committed`), so
  a run that stops at the gate leaves as its trace the log and the private folder only. The
  per-key diagnostic covers all 637 fit keys per world (the
  `|sh:` and `|pc:` keys included) but not the null, which has no keys.
- **Determinism check (a stop).** The primary rule is fitted twice on the real knockout view.
  The two data dicts must hash byte-identically (the G-det test of rule #2.1, reused), else
  "NOT DETERMINISTIC" and stop. Every fit is deterministic given the bank: N1 is a Newton fit, λ is
  chosen on a fixed grid over fixed folds, and ALS starts come from `PCG64(30000 + j)`.
- **No seed enters the primary numbers.** `AUC_real`, both ceilings and every shuffle margin are
  deterministic. Only `p_P` depends on a seed, the permutation generator's. Its resolution is
  1/10,000, and it is fixed below.

### 3.4 Machine checks (before any block score is read)

Each stops the run with its own message:

1. **Pins** (§1.1): every sha256 equals the table. The rule loads through `harness.load_rule` with
   `RANK == 1`.
2. **Block and mask:** 64 cells, 8 distinct sources and 8 distinct targets, all 16 names in
   `harness.NAMES`. The training mask has 4,161 cells, and none of them is a block cell. The
   `ceiling_block` mask (§2.4) has exactly the 64 block cells.
3. **Board as reviewed:** in flyvis-65 the block has 32 present cells, ON × T4 = 16, OFF × T5 = 16,
   cross = 0. This is the reviewed, public count, re-read at run time; otherwise "BOARD DIFFERS FROM
   THE REVIEWED COUNT". Equivalently, `y_st = x_s · w_t` on all 64 cells (§2.4).
4. **Pre-data tables:** §1.4's three tables are recomputed and must match.
5. **N1 parity identity:** `|D(N1 logit)| < 1e-9` on the real block. `D` of N1 is registered
   as "within `PARITY_TOL` of 0", not as 0.0: four N1 rows of the pre-run table carry
   floating-point residues (seeds 90104: −5.55e-17, 90131: +2.78e-17, 90132: +5.55e-17, 90183:
   −1.11e-16; revision 3.2). Check 5 runs on the real arm only.
6. **Leakage check:** the primary rule is fitted on the knockout of the real bank and on the
   knockout of the real bank with its block replaced by permutation 0 of leg P. The two data dicts
   must be byte-identical ("BLOCK LEAKS INTO TRAINING").
7. **AUC function:** on hand-made inputs (a perfect ranking gives 1, its reverse 0, all ties 0.5,
   and one known mixed case) it returns the exact value.
8. **Harness identity (as in `bf1_p3`):** BF_1's full-bank C6 existence margin over N1 reproduces
   **0.028150051052145946** to 1e-9.
9. **Determinism** (§3.3).

### 3.5 What is printed per predictor (lessons f, g)

For the primary rule, BF_1–BF_4 and N1, on the real block: AUC with its 32/32 denominators, `D`,
the log-loss and its margin over N1, precision at 32, the four quadrant means, **`ceiling_full`
and `ceiling_block`** (§2.4), the regrown share of each, `p_S` with `n_ge` of `99 − n_deg` and `n_deg`,
`p_P` of 9,999, the row-and-column `p_P`, and the λ chosen (for the knockout fit and for each
ceiling). Also printed: the five mirror partners' `p_exist` with the AUC on the other 59 cells;
per-type rows (for each of the 16 types, the AUC over its 8 block cells, where it is defined, since
each type has 4 present and 4 absent); the §4 label read on each D1 candidate (rule #2.1 and BF_1)
and whether the two agree; and the 20 permuted-block `ceiling_full` values beside the real one.

**The fixed λ = 1 diagnostic (revision 3; Ark 08:24, with Johnny's condition 08:27 and CC's
summary 08:28, supported by Mike 08:30 UTC). Diagnostic, decides nothing.** For rule #2.1 and
each BF_r, one extra row: the knockout fit with λ fixed at 1, and its AUC and `p_P` on the block
(the same 9,999 permutations as leg P). It shows whether the unselected fit sees structure that
the nested λ choice sets to zero (§6, the λ switch). It is printed **beside the limits** (γ\* in
revision 3) and never on the
verdict line (Johnny's condition). No branch, requirement or consequence reads it. A reading
threshold on it may be added only after it has been calibrated on the same worlds and put to a
vote (CC's summary). How λ is fixed, without modifying any pinned file:

- **BF_r:** `harness.bf_als(O, Y, M, r, λ, starts)`, the harness function that takes λ. It is
  called exactly as the final fit of `fit_bf` calls it (`harness.py:729`): `O` is the logit grid of
  `fit_n1` on the knockout view, `M` and `Y` are that view's grid, and `starts = STARTS`.
- **Rule #2.1:** its `fit` has no λ argument. It reads its grid from the module global `LAMBDAS`
  (`second_rule_v21/fit.py:57`, lines 128–142). The script sets that global to `[1]` for this one
  fit and restores it afterwards. The nested choice then has one candidate, and every other step
  of the fit is unchanged.
- Where a knockout fit already selected λ = 1, that fit *is* the fixed-λ fit, and it is reused.
  This is checked once per run: on the first world whose five knockout fits all selected λ = 1,
  the five are refitted by the fixed-λ path, and each `p_exist` must equal the selected fit's
  exactly ("FIXED-LAMBDA PATH DIFFERS FROM THE SELECTED FIT" otherwise).

### 3.6 Two-world check (synthetic, before any real block score; lesson b; proposal, D8)

**Purpose.** To show, before data, that the reading rule of §4 *can* read each branch. It is run on
worlds whose answer is known by construction, read by exactly the same code and the same legs
(99 shuffles of each world, 9,999 permutations, both ceilings, the BF family) as the real bank.

**How a world is built.** A world is a 65-type bank on the harness grid, with the harness's
`TYPE_FIELDS` and `folds.csv` and the same 64 block positions. The rule sees positions only, as it
does on the real bank.

- **Latent polarity.** `z_i = +1` for the positions of Mi1, Tm3, Mi4, Mi9 and T4a–d, and `−1` for
  Tm1, Tm2, Tm4, Tm9 and T5a–d. The other 49 types get `z_i = ±1` with probability ½ each, from the
  world's seed.
- **Degree terms** (proposal): the N1 existence parameters `(c, a, b)` fitted on the **real knockout
  view**. They use outside-block cells only, which N1 fits in the run anyway, so each world's
  support per type resembles the real one; T5a and T5c stay thin, for example. (Alternative
  under D8: `a`, `b` ~ N(0, 1), `c = −2.2`, fully synthetic.)
- **Outside cells:** present iff `u_st < sigmoid(c + a_s + b_t + γ_z · z_s · z_t + γ_z1 · z1_s · z1_t)` (revision
  3.3: the two coefficients named γ_z and γ_z1, the CSV's `gamma_z` and `gamma_z1`, as in
  `make_world`; γ_z1 = 0 except in W; the column γ_out below is γ_z), with `u` one
  `(65, 65)` uniform draw from the world's generator.
- **Block cells, by family:**

| family | γ_out (γ_z) | block pattern | built so that | requirement (fresh seeds) | on failure |
|---|---|---|---|---|---|
| **R**, regrowable | 2.0 | board by `z` (present iff `z_s z_t = +1`), 16 + 16 | the outside carries `z`, and the block follows it | each of 5 worlds reads **R**, on both D1 candidates (§4) | stop |
| **Nf**, no information | 0 | board by `z` | the outside carries no polarity at all; the board exists only inside the block | **revision 3:** never **R** or **W**; **at least 3 of 5** read **G** | R or W on any world: stop. Fewer than 3 G: stop. A U: no stop by itself |
| **No**, orthogonal board | 2.0 | board by `z'`, where `z' = +1` on Mi1, Tm3, Tm1, Tm2, T4a, T4b, T5a, T5b and `−1` on the other 8 | the outside carries `z`, but the block follows a polarity orthogonal to it: `Σ z z'` = 0 over sources and over targets, so `D(z-pattern)` on the `z'` board is exactly 0 | **revision 3:** never **R** or **W**; reads **G** (its mechanism label is printed as a description) | R or W on any world: stop. U: no stop; the No contingency below |
| **W**, rank-2 information | `γ_z1 = 2.5` on a second polarity `z1` (random ±1 for the 49 others; on the 16 block types, `z1 = z'` above) plus `γ_z = 1.5` on `z` (revision 3.3 names them; revisions 2–3.2 wrote γ1 and γ2) | board by `z` | a rank-1 fit takes the dominant `z1` and misses `z`, while a rank-2 fit carries both | each of 5 worlds reads **W**, on both D1 candidates | stop |
| **M**, weak (the power curve) | **revision 3:** 0.5, 0.6, 0.75, 0.85, 1.0 (the dense grid) | board by `z` | real but weak information | **revision 3: none.** Every label is a true reading or a point of the power curve; the curve is printed and the three limits of revision 3.1 are taken from it | **no stop row** |

**The requirement rows as revised (revision 3, decisions (a) and (b)).** Revision 2 required every
M world to read "U or W: never G, never R", and it stopped the run otherwise. **That requirement
was wrong.** The structure of an M world is real, only weak. An M world that reads **R** or **W**
is read truly: the design found structure that exists. That is a point on the power curve, not a
defect. CC warned of this before the run (DPC Research chat, 2026-09-24 21:10 UTC, point 2), and the
run then stopped on it: M1.0 read R in 5 of 5 worlds (§3.6, "What the runs found"). Ark marks the
class of error: **a requirement written without asking whether it would stop a correct answer.**
Revision 3 therefore keeps no requirement that the design cannot pass by construction.

- **M worlds.** The only wrong reading an M world could give is a **false absence**: a claim that
  no structure is there. Since revision 3, G no longer claims absence. Under revision 3.1 it reads
  "not detected at the R level above γ_R; leg P passes from γ\*_P" (§4), and both limits
  are measured on these same worlds. So an M world that reads G below γ_R is read truly, and no
  label of an M world is a false absence. **The M rows have no stop.** They are printed as the
  power curve: per γ, the fractions seen/n and R/n and the label of each world. The numbers of M
  worlds **at or above γ\*_P** and **at or above γ_R** that read G are printed as the miss rates
  at the two limits. They decide nothing.
- **Nf worlds (γ = 0) must never read R or W.** That remains a stop: an R or W on a world
  with no information is a false positive. **At least 3 of 5** Nf worlds must read G (CC's proposal,
  2026-09-24 21:10 UTC, point 1). Revision 2 asked for all 5. If the interaction term is fitted
  noise, each of the five predictors' `p_P` is about uniform, and "all five above 0.10" then holds
  with probability about 0.9⁵ ≈ 0.59 per world, or about 0.07 for five worlds out of five. A
  requirement that sits on the threshold catches noise, as in the column test. In the
  08:22–08:28 UTC exchange no reviewer voted on this item by name. It was applied as part of the
  consensus that CC summarised and Mike supported (§12). **Revision 3.1: the reviewers confirmed
  it in their pass on revision 3** (Ark 09:32, Johnny 09:33, Zcode 09:34 UTC; §10). The
  revision-2 run met the old requirement anyway (5 of 5 read G), so the change alters no reading.
- **No worlds.** Under decision (c) the mechanism label is not read, so the requirement is
  "reads G", not "reads G (orthogonal)". R or W stays a stop, and U still triggers the No
  contingency. In the revision-2 run all 5 No worlds read G, with the description "orthogonal",
  so this change also alters no reading. **Revision 3.1: the reviewers confirmed "No reads G"**
  (Ark 09:32, Johnny 09:33, Zcode 09:34 UTC; §10).

**What each world should read under revision 2 (derived by algebra before the run; kept as
written; the measurements follow below, in "What the runs found").**

- **R.** The outside carries `z` at γ = 2.0 and the block follows `z`. Trained without the block,
  the rank-1 term takes `z`, and by §2.4 (consequence 1) `z_s z_t` is exactly the block's ±1
  labels. The primary and BF_1 should both pass legs S and P: **R**, agreed on both D1 candidates.
  Both ceilings ≈ 1.
- **Nf.** The outside has no interaction. The knockout fits' interaction terms are fitted noise or
  are shrunk away, so every AUC is near 0.5 and no predictor passes: not R, not W. `ceiling_block`
  ≈ 1 (§2.4, consequence 2), so the gate holds. `ceiling_full` should be high too, since the outside
  gives the rank-1 term nothing else to fit and the block is itself rank 1. Expected reading:
  **G (no information)**. Risk: if an interaction term is fitted noise, its `p_P` on the block is
  close to uniform, and all five predictors above 0.10 is then not assured (about 0.9^5 ≈ 0.59 per
  world if they were independent; BF ranks are nested, so they are not). If the term is shrunk to
  near zero, the prediction is nearly additive, its AUC stays inside the narrow additive band of
  §2.3, and `p_P` is far above 0.10. Which of the two happens is what D11 measures.
- **No.** The rank-1 term takes the outside's `z`. On the `z'` board, the score `z_s z_t` is
  **exactly** uninformative: the sources fall into the four (`z`, `z'`) classes (Mi1, Tm3), (Mi4,
  Mi9), (Tm1, Tm2), (Tm4, Tm9), the targets into (T4a, T4b), (T4c, T4d), (T5a, T5b), (T5c, T5d),
  and each score-label pair covers 16 cells, so the pure `z` score has AUC exactly 0.5. The additive
  terms move it only inside the band of §2.3. The outside has no second polarity, so no BF_r finds
  `z'`: not R, not W, every `p_P` expected well above 0.10. `ceiling_block` ≈ 1, and `ceiling_full`
  ≈ 0.5 for the primary, since its one rank-1 term is held by the outside's `z`. Expected reading:
  **G (orthogonal)**. Under revision 1's single ceiling this world would have read U (Ark,
  finding 3).
- **W.** The primary and BF_1 take the dominant `z1`, which equals `z'` on the block, so by the same
  algebra their knockout AUC is near 0.5 and neither reads R. BF_2 to BF_4 carry `z` too and should
  pass leg S and leg P at 0.0125. Expected reading: **W**, agreed on both D1 candidates. (The
  primary's `ceiling_full` is low and its `ceiling_block` ≈ 1, but W is tested before G.)
- **M (γ = 0.5, 1.0).** Weak `z` outside and a `z` board. Expected: at 0.5, a weak regrowth between
  the cuts, which is U; at 1.0, U, with a regrowth that may reach leg P. **Two risks, both stops:**
  at γ = 0.5 a world can read **G (no information)**, because `ceiling_block` ≈ 1 no longer blocks
  G and every `p_P` may exceed 0.10; at γ = 1.0 a world can read **R** if the primary passes both
  legs. Registering "never R" at γ = 1.0 registers that the primary's R threshold lies above γ =
  1.0.

**The γ breakpoint of revision 2 (Ark, finding 2).** Revision 2 printed, for γ in {0 (Nf), 0.5,
1.0, 2.0 (R)}, how many of the 5 worlds are **seen**: the primary passes leg P (`p_P <= 0.01`).
That grid gave the bracket (0.5, 1.0], half a unit of γ wide.

**γ\*, the detection limit (revision 3, decision (b), all three reviewers).** Revision 3 had one
limit, γ\*: the smallest grid γ at which a majority of the worlds are seen. **Revision 3.1
replaces it with three limits, below. Revision 3's γ\* is the first of them, γ\*_P.**

- **The dense grid.** γ ∈ {0.5, 0.6, 0.75, 0.85, 1.0}, with 5 worlds at each γ. M0.5 and M1.0
  reuse their revision-2 worlds and fits. M0.6, M0.75 and M0.85 are new families on fresh seeds
  (§3.7). Nf (γ = 0) and R (γ = 2.0) are printed on the same curve as anchors and enter no limit.
- **Seen.** A world is seen by a predictor when that predictor passes leg P (`p_P <= 0.01`). "Seen"
  without a predictor means seen by the primary, rule #2.1, as in revision 2.
- **Majority** means 3 or more of the 5 worlds at one γ.

**The three limits (revision 3.1; Ark 09:32, Johnny 09:33, Zcode 09:34 UTC).** Revision 3's one
γ\* named leg P only. A G stated against it claimed more than the instrument measured: at
γ\* = 0.6 only 2 of 5 worlds read R. Each limit is the smallest γ on the dense grid at which its
condition holds in a majority of the worlds. Its **bracket** is (the next grid γ below it, the
limit], with γ = 0 below 0.5. If no grid γ meets the condition, the limit is printed as "> 1.0
(not reached on the grid)".

| limit | condition, in a majority of the worlds at that γ | what it says |
|---|---|---|
| **γ\*_P, the leg-P limit** | rule #2.1 has `p_P <= 0.01` (revision 3's γ\*) | from here up, leg P alone sees the block |
| **γ_R, the R level** | the world reads **R** (§4: both legs, both D1 candidates) | from here up, the full reading rule regrows the block |
| **family limit** | computed per predictor: for each of rule #2.1 and BF_1–BF_4, the γ at which that predictor has `p_P <= 0.01`. The family limit is the **largest leg-P limit** of the five | from here up, every predictor of the family sees the block on leg P |

**Which p value defines the limits, and at what level (revision 3.2; V3 and B4 in §10).** All
three limits use `p_P <= 0.01`, for every predictor, the family limit included. The W gate of
§4 is family-corrected (`p_P <= 0.0125` = 0.05/4); the limits are not, because a limit is a
property of the instrument, not of a branch. `p_P` alone defines the limits. `p_P_rowcol` (the
row-and-column variant, §3.2) and `p_P_fixed_lambda1` (the fixed λ = 1 diagnostic, §3.5) are
diagnostics and are named as such where printed. On M0.6 they give 4 of 5 worlds seen, where
`p_P` gives 3 of 5. The family limit equals γ_R in the pre-run table (both 0.75), but not by
construction: R also needs leg S (`reading_on`), while a leg-P limit uses `p_P` only
(`detection_limits`). The limits are named "the smallest leg-P limit" (γ\*_P, rule #2.1's) and
"the largest leg-P limit" (the family limit), never "the weakest" or "the strongest predictor".

Printed beside the three limits, and never collapsed into them (Johnny 09:33 UTC): **at every γ of
the curve, the fraction seen/n and the fraction R/n**, and each predictor's seen/n. Also printed:
whether the majority holds at every grid γ above each limit; the number of M worlds that read G at
or above γ\*_P and at or above γ_R; the transition band (below); and the binomial note (next
item).

- **The binomial note (Johnny 09:33 UTC).** With n = 5 worlds per γ, a limit is uncertain by
  about one grid step. At a γ whose true detection probability is 0.2, "≥ 3 of 5" happens with
  probability about 0.06. At 0.4 it happens with probability about 0.32. (The exact binomial tails
  are 0.058 and 0.317. The script computes and prints them.) So a limit can land one grid step low,
  and by the same argument one step high. The bracket is the grid's resolution, not a confidence
  interval.
- **The transition band (revision 3.1; Ark 09:32 UTC).** The band is the set of grid γ in
  [γ\*_P, γ_R): leg P is seen by a majority there, but R is not read by a majority. The report
  prints its width in grid steps (the number of grid γ in the band) and in γ (γ_R − γ\*_P). It
  also prints how many dense-grid U worlds fall below, inside and above the band. If the two
  limits coincide, the band is empty, a sharp step. If γ_R is not reached, the band is open, and
  it is printed as a lower bound. **Revision 3.2 (Ark, V2):** the band is the difference of two
  limits, each uncertain by about one grid step at n = 5 (the binomial note), so a band of one
  grid step is one of 0, 1 or 2 steps.
- **The instrument.** The limits belong to the instrument, not to the fly. Each depends on three
  constants: the λ grid `BF_LAMBDAS` = [1, 3, 10, 30, 100] (`harness.py:535`); the tie rule, under
  which held-out log-likelihoods within 1e-9 of the best go to the **larger** λ
  (`harness.py:727-728`; rule #2.1 copies it, `LAMBDA_TIE = 1e-9`); and `STARTS` = 10. **Every
  printed G carries the three limits, their brackets, the per-γ fractions and these three
  constants** (Zcode 08:22 and Johnny 08:27 UTC, extended to the three limits by revision 3.1). A
  change to any constant moves the limits. A G stated without them would be a number under a name
  it no longer earns.
- **Units.** The limits are in the units of the M worlds: the coefficient of `z_s z_t` in the
  outside logit, on the degree terms of §3.6. They are not quantities of the real bank.

**The U rule (revision 3; CC's summary of 08:28, supported by Mike 08:30 UTC; written before the
dense grid was run).** U was **not visited** by any of the 30 worlds of the revision-2 run
(Zcode, 08:22 UTC). Johnny (08:27 UTC) showed why this is structural: the λ switch (§6) makes
the fit binary, and U is the remainder. He asked that U be removed or calibrated, not kept as a
"surprise". Zcode asked that it be kept and examined if the real run ever prints it. The rule
decides between the two by the dense grid itself:

- **If at least one world on the dense grid reads U**, U stays as "U: too noisy to decide", and
  its frequency across the worlds is printed.
- **If none does**, U is renamed **"insufficient evidence (uncalibrated)"** and is **never read as
  a finding**. The branch condition of §4 is unchanged. Only its name and its standing change.

This is Johnny's falsifier: "if an M world on the denser grid gives U even once, U is not
structurally unreachable". **Outcome:** 3 of 25 dense-grid worlds read U, all at γ = 0.6, so U
stays (see "What the runs found").

**Revision 3.3 (A3): the U rule counts threshold U only.** "Reads U" above means a threshold U.
A U whose reasons include `ceiling_block` below the gate (a failed fit) and a U whose
`ceiling_block` was not measured are counted apart (`n_u_failed`, `n_u_not_measured`, beside
`n_u_threshold`), and neither keeps nor renames U: a failed fit says nothing about the
threshold. In the pre-run table and in the re-read of revision 3.3 the 3 U worlds are all
threshold U (0 failed fit, 0 not measured).

**U is the signature of the threshold (revision 3.1; Ark 09:32 UTC, Zcode 09:34 UTC agreeing;
Johnny 09:33 UTC; narrowed in revision 3.2).** **Revision 3.2 (Ark, V2): U is the signature of
the detection limit γ\*_P, not of the band.** All 3 U worlds of the pre-run table sit at γ = 0.6
= γ\*_P, and the band's width is itself uncertain by up to two grid steps (above). The rest of
this paragraph is revision 3.1's reading. U is not an independent state of the block. It shows up in the transition
band, between "not seen" and "seen at the R level". All three U readings of the pre-run table were
at γ = 0.6. That is γ\*_P, the one grid γ in the band [γ\*_P, γ_R) = [0.6, 0.75) (pre-run
values). The U readings are worlds in which the legs or the D1 candidates split. They sit where
the seen fraction crosses one half (3 of 5 seen at γ = 0.6, 1 of 5 at 0.5). Johnny's falsifier fired against his own
structural reading, and he recorded that as his own error (09:33 UTC). **A U on the real block is
therefore read as "on the detection threshold; cannot be separated".** The report prints the
width of the transition band, in grid steps and in γ, and where each dense-grid U world falls
relative to it (§4, §11). The U rule above still applies. It sets the name if the registered run's
dense grid reads no U. **Revision 3.2 (V4, A2):** a U whose reasons include `ceiling_block` below
the gate is not a threshold reading but a failed fit; it prints as such, and the U rule never
renames it (§4). **Revision 3.3 (A4):** nor is a U whose `ceiling_block` was not measured; it
has its own text (§4).

**The No contingency (Ark, finding 3).** If, after the ceiling fix, any No world reads **U**, the
registration and the outcome note state: **"The design cannot tell an orthogonal board from
absence."** A U on the real block then does not exclude a block that contradicts its surroundings,
and a G on the real block is printed with its mechanism label but read only as G. The real arm still
runs, since this is a limit of reading, not a false positive.

**The labels statement (revision 2; superseded).** Revision 2 read the mechanism label of G only
if the synthetic check separated the two labels. The revision-2 run triggered it: 2 of 5 Nf
worlds read "orthogonal". Revision 3 makes the label a description in every case (§2.4, decision
(c)), so the statement has nothing left to switch.

- **Content** of a present cell (offsets, sign) is drawn by a seeded index from the real bank's
  **non-block** present cells, as `harness.planted_banks` draws it. No block content enters any
  world.
- **Printed per world:** outside density, the block's present count (32 by construction), and
  everything of §3.5.

**If a requirement marked "stop" fails (R, Nf, No, W), the real arm does not run.** The design is
then revised under a new draft. A No world reading U does not stop the run; it triggers the No
contingency above. The M rows never stop (revision 3).
**What the check can and cannot falsify** (as in the column test, §3.8): the R and Nf rows can
fail, since they test the reachability of "regrows" and of G by the whole pipeline, including
λ's nested choice, and the Nf row tests that no information is never read as R or W. The W row
tests whether the BF family can see information that the rank-1 primary cannot. The M rows do
not test; they measure the power curve and the three limits (revision 3.1). The No row tests that an orthogonal board is not
read as R or W. None of them tests biology.

**What the runs found (synthetic only; the real block was not read).** Two runs, both CPU with 30
workers and `--starts 10`. The revision-2 run: 30 worlds, 2026-09-24 21:32–22:58 UTC. Revision 3
added 15 worlds on the dense grid, 2026-09-25 08:39–09:23 UTC. The 30 revision-2 worlds were
re-read from their saved fits, not refitted. Every world had `ceiling_block` = 1.000 and
`n_deg` = 0.

| family (γ) | revision 2 requirement → result | revision 3 requirement | labels R/W/G/U | result |
|---|---|---|---|---|
| R (2.0) | each R → 5/5, met | unchanged | 5/0/0/0 | met |
| Nf (0) | each G → 5/5, met (3 "no information", 2 "orthogonal") | never R/W; ≥ 3 of 5 G | 0/0/5/0 | met |
| No (2.0) | each G (orthogonal) → 5/5, met | never R/W; G | 0/0/5/0 | met (all described "orthogonal") |
| W (γ_z = 1.5, γ_z1 = 2.5) | each W → 5/5, met | unchanged | 0/5/0/0 | met |
| M0.5 | U or W → **R 1, G 4: STOP** | power curve, no stop | 1/0/4/0 | curve |
| M0.6 (new) | — | power curve, no stop | 2/0/0/3 | curve |
| M0.75 (new) | — | power curve, no stop | 5/0/0/0 | curve |
| M0.85 (new) | — | power curve, no stop | 5/0/0/0 | curve |
| M1.0 | U or W → **R 5/5: STOP** | power curve, no stop | 5/0/0/0 | curve |

**The two-world check of revision 3 passes.** No row stops, and the No contingency is not
triggered.

**The power curve** (seen = rule #2.1 passes leg P; R = the world reads R; rule #2.1's knockout
AUC per world and its selected λ). **Pre-run values** (header, §3.3): the registered run
recomputes them and must reproduce them.

| γ | seen/n | R/n | R/W/G/U | rule AUC | selected λ |
|---|---|---|---|---|---|
| 0 (Nf, anchor) | 0/5 | 0/5 | 0/0/5/0 | 0.505, 0.536, 0.507, 0.502, 0.517 | 100 ×5 |
| 0.5 | 1/5 | 1/5 | 1/0/4/0 | 0.735, 0.500, 0.531, 0.528, 0.490 | 3, 100, 3, 100, 100 |
| 0.6 | 3/5 | 2/5 | 2/0/0/3 | 0.745, 0.565, 0.730, 0.673, 0.636 | 3 ×5 |
| 0.75 | 5/5 | 5/5 | 5/0/0/0 | 0.871, 0.876, 0.786, 0.725, 0.740 | 3 ×5 |
| 0.85 | 5/5 | 5/5 | 5/0/0/0 | 0.952, 0.776, 0.843, 0.840, 0.812 | 1, 3, 3, 3, 3 |
| 1.0 | 5/5 | 5/5 | 5/0/0/0 | 0.970, 0.954, 0.855, 0.974, 0.759 | 1, 1, 3, 1, 3 |
| 2.0 (R, anchor) | 5/5 | 5/5 | 5/0/0/0 | 1.000 ×5 | 1 ×5 |

**Revision 3 read one limit from this table: γ\* = 0.6, bracket (0.5, 0.6]**, in M-world units.
Instrument: `BF_LAMBDAS` [1, 3, 10, 30, 100], ties within 1e-9 to the larger λ, `STARTS` = 10. A
majority is seen at every grid γ ≥ 0.6. No M world at or above γ\* read G. The seen count at γ\*
is 3 of 5, the smallest majority.

**The three limits of revision 3.1, read from the same pre-run table. These are pre-run values;
the registered run recomputes them.**

- **γ\*_P = 0.6**, bracket (0.5, 0.6]: seen 3/5 at 0.6, 1/5 at 0.5 (revision 3's γ\*).
- **γ_R = 0.75**, bracket (0.6, 0.75]: R 2/5 at 0.6, 5/5 at 0.75.
- **Family limit: not in the pre-run table** (revision 3.1). The table printed no per-predictor
  seen counts for BF_1–BF_4, and revision 3.1 ran nothing. The registered run computes and
  prints it. **Revision 3.2: 0.75**, read from the pre-run `synthetic_worlds.csv` (Ark, V3):
  BF_2, BF_3 and BF_4 reach a majority only at 0.75, rule #2.1 and BF_1 at 0.6.
- **Transition band [0.6, 0.75)**: 1 grid step, 0.15 in γ. All 3 dense-grid U worlds lie inside
  it, at γ = 0.6.
- Instrument as above. No M world at or above γ_R read G.

**How to read the three limits (revision 3.2, text only; B1–B4 in §10).**

- **They are pre-run values of the synthetic step:** γ\*_P = 0.6, γ_R = 0.75 and the family
  limit = 0.75. They are values of the instrument on the M worlds, not an answer about the real
  block. The family limit equals γ_R here, but not by construction (see "Which p value defines
  the limits" above). **Revision 3.3 (B1):** beside them, `smallest_passing_auc` = 0.666015625
  (682/1024) in 40 worlds and 0.6728515625 (689/1024) in the five No worlds (§3.2). It is γ-blind
  and fits nothing: a translation anchor between the AUC axis and `P_R`, not a γ limit.
- **What they rest on.** The γ_R bracket (0.6, 0.75] rests entirely on worlds fitted by the
  revision-3 run (M0.6 and M0.75). The limits' exposure to the worlds fitted by the revision-2
  run is M0.5 only (5 worlds, the minus side of γ\*_P). M1.0 lies above all three limits and
  enters none of them: every limit is the smallest grid γ with a majority, so a grid point above
  it cannot move it.
- **λ.** The minus side (M0.5) is λ-robust: its four unseen worlds have `p_P_fixed_lambda1` =
  0.1171, 0.2516, 0.4709 and 0.6114, all above 0.01. The plus side (M0.6) holds on the minimal
  majority, 3 of 5 under the selected λ (2 R and 1 U), and 4 of 5 under λ = 1. The world that
  flips is 90164 (`p_P` 0.0308 under the selected λ, 0.0011 at λ = 1); the nearest miss is 3.1
  times the threshold under the selected λ. λ moves the margin, not the limit: γ\*_P is 0.6 both
  ways.
- **`p_P` defines the limits;** `p_P_rowcol` and `p_P_fixed_lambda1` are diagnostics (on M0.6
  they give 4 of 5, `p_P` gives 3 of 5).

**The U rule's outcome: U stays.** 3 of the 25 dense-grid worlds read U, all at γ = 0.6. Their
reasons, as the revision-3.1 writer logged them on 2026-09-25 (revision 3.2 corrects revision
3.1's summary of them): **90161**, the legs disagree for rule #2.1 (leg S `n_ge` = 0 of 99, leg P
`p_P` = 0.1888), and BF_2 has `p_P` = 0.0832 ≤ 0.10 without R or W; **90163**, the two D1
candidates disagree on R/W (rule #2.1 reads W, since its own leg S has `n_ge` = 1; BF_1 reads
R); **90164**, the legs disagree for
rule #2.1 (`n_ge` = 0, `p_P` = 0.0308), and rule #2.1 (`p_P` = 0.0308) and BF_1 (`p_P` =
0.0405) are ≤ 0.10 without R or W. None of them involves `ceiling_block`. U across all 45
worlds: 3. Johnny's falsifier fired, as he said it could (08:27 UTC). U is reachable, so it is
not renamed.

**The fixed λ = 1 diagnostic (decides nothing).** It is the mean knockout AUC of rule #2.1 at λ = 1
against the selected λ, with the count of worlds at `p_P <= 0.01`. R: 1.000 (5/5) against 1.000
(5/5). Nf: 0.550 (0/5) against 0.513 (0/5). No: 0.490 (0/5) against 0.490 (0/5). W: 0.516 (0/5)
against 0.516 (0/5), while BF_2–BF_4 are 5/5 in both. M0.5: 0.582 (1/5) against 0.557 (1/5).
M0.6: 0.753 (4/5) against 0.670 (3/5). M0.75: 0.903 (5/5) against 0.800 (5/5). M0.85: 0.910
(5/5) against 0.844 (5/5). M1.0: 0.941 (5/5) against 0.902 (5/5). At λ = 1, no Nf or No world
reaches `p_P <= 0.01` for any predictor. The per-predictor table is in the run's `SYNTHETIC.md`.
The fixed-λ path check passed: on world W j = 0, all five refits were identical to the selected
fits.

### 3.7 Seeds (all new; the script asserts that they are distinct)

| use | seed(s) | generator |
|---|---|---|
| leg P, uniform permutations (also permutation 0 of the leakage check) | 90000 | `numpy.random.default_rng(90000)`, 9,999 × `permutation(64)` in order |
| leg P, row-and-column-preserving permutations | 90001 | `default_rng(90001)` |
| ceiling on permuted blocks | 90010–90029 | `default_rng(90010 + j)`, `j = 0..19` |
| synthetic worlds (family index `i` in R, Nf, No, W, M0.5, M1.0 = 0..5, and, added in revision 3, M0.6, M0.75, M0.85 = 6..8; repeat `j` = 0..4) | 90100 + 10 i + j (90100–90154; revision 3 adds 90160–90184, fresh: no file of the repository used them, checked 2026-09-25) | `default_rng`: `z` for the 49 others, `z1`, `u`, content indices, in that order. **Provenance of the fits (revision 3.2):** the saved fits of the 30 worlds 90100–90154 were made by the revision-2 run, those of the 15 worlds 90160–90184 by the revision-3 run; fresh knockout fits of all 45 worlds by the revision-3.1 code equal them bit for bit (270 of 270, the knockout view only; §3.3) |
| shuffles of the real bank and of each world | 0..98 | `harness.shuffled_bank(base, sd)`, reused on purpose, as the column test reuses its curve seeds |
| BF / rule #2.1 ALS starts | `PCG64(30000 + j)` | fixed in the harness |

**Untouched:** 60000, 61000, 70000–70999 and 80000–80999 (rule #2.1's reserved ranges); 4242, 99
and 7 (planted); 1000–1019 (RP); 10000+ (dial); 20260923. The new range 90000–90999 meets none of
them.

### 3.8 Vocabulary (revision 3.3; C2, B3, item ㊴)

- **"Present in the block" has two carriers, on two banks.** `n_present`, `n_absent` and
  `block_present` count the block's present cells on the **base** bank of a world (or the real
  bank): 32 in all 45 worlds. `score["n_ne"]` in a raw record, and `present` in a `per_shuffle`
  record, count them on the bank that was fitted, which for a shuffle is the **shuffled** bank
  `sd`: it varies (16, for example). The definition is the same, `int(y.sum())` (harness `score`;
  script `evaluate_bank`); the banks differ.
- **λ.** `None`: the predictor has no λ axis (N1). **100** = `LAMBDA_MAX`: the interaction is
  shrunk to zero, and the prediction is N1's. Across the 23,850 fits that select λ, λ = 100 in
  22,125 (92.8 %), λ = 3 in 1,014 and λ = 1 in 711 (Johnny's count; the 936 records with λ = 1 in
  total include the 225 `ko1` fits at fixed λ = 1). **Ties** of the held-out log-likelihood
  within 1e-9 go to the **larger** λ (`harness.py:727-728`): a direction policy that the earlier
  revisions applied without naming it, named here.
- **`TAU`** is a tie policy, inert in every count of this registration (§3.2), not the
  instrument's resolution.

## 4. Reading rule (every branch named before data; proposal, D5)

Read on the primary rule unless a row says otherwise. The rows are tested **in order**, and the
first that holds is the verdict. U is the remainder, so the four branches are exhaustive and
exclusive.

**R/W agreement on both D1 candidates (proposal, marked for review; D1; Johnny).** The R and W rows
are evaluated twice: reading A with rule #2.1 as the primary, and reading B with BF_1 as the
primary (the other D1 reading, §2.1). In both readings the W row ranges over BF_1 to BF_4, so in
reading B it effectively asks for BF_2 to BF_4. **R stands only if both readings give R, and W
stands only if both give W.** If either reading gives R or W and the other does not give the same
letter, the label is **U**, and the report names both readings. If neither reading gives R or W,
the G and U rows are read on rule #2.1.

*Why this option and not a margin over a fit cost.* Johnny offered two ways to keep W from
being read when the passing BF_r and the failing primary differ by no more than fitting noise.
(a) W is read only if the passing BF_r's margin over the primary exceeds a fit cost, such as
the spread of the primary's AUC across folds or seeds. (b) R/W is printed on both D1 candidates,
and they must agree. This draft picks (b), for three reasons. First, it adds no new estimated
quantity and no new cut. Second, both objects are already fitted in every run, so it costs
nothing. Third, the harness defines no fit cost that suits a single held-out block: there is one
block, so there are no folds to spread over, and rule #2.1 is deterministic given the bank (§3.3).
The spread over its 10 ALS starts would likely be near zero for a rank-1 fit that converges to one
optimum, which would make (a) vacuous. What (b) does not do: it does not require a margin, so a
BF_r that passes by a hair over a primary that fails by a hair still reads W when BF_1 fails too.
Reviewers may prefer (a) with a quantity they name.

| branch | condition | reading |
|---|---|---|
| **R: regrows** | the primary passes leg S (`n_ge = 0` of the `99 − n_deg` shuffles with an AUC, §3.2) **and** leg P (`p_P <= 0.01`), **on both D1 candidates** | The rule, trained without the block, orders the block's cells better than it does in all 99 degree-preserving shuffles and better than 99 % of label permutations. It generates structure that it was not shown and that degrees do not carry, **on flyvis's averaged template**. |
| **W: rule weaker than the information available** | not R, and **some BF_r** (r = 1..4) passes leg S (`n_ge = 0`) and leg P at `p_P <= 0.0125` (0.05/4), **on both D1 candidates** | The bank outside the block implies the block for a learnable, name-free predictor, and the registered rule does not express it. That is a defect of the rule, not an absence of grammar. The rank that passed is named. |
| **G: not detected at the R level above γ_R** | not R, not W; the primary **and every BF_r** have `p_P > 0.10`; and the primary's **`ceiling_block` >= 0.90** (the condition is revision 2's, unchanged; the cut is the gate cut, `GATE_CUT`, since revision 3.2) | **Revision 3.1 (Ark 09:32, Johnny 09:33, Zcode 09:34 UTC): "not detected at the R level above γ_R; leg P passes from γ\*_P".** The block carries no structure that this family regrows at the R level at a strength at or above γ_R, where a majority of the synthetic worlds read R. Leg P alone (of rule #2.1) already sees a majority from γ\*_P, and every predictor does from the family limit (§3.6). Revision 3's "not detected above γ\*" named leg P only. The label always prints **all three limits** with their brackets, **the per-γ fractions seen/n and R/n**, the transition band, and the instrument they come from: `BF_LAMBDAS` [1, 3, 10, 30, 100], ties within 1e-9 to the larger λ, `STARTS` = 10. The rule can express the block (`ceiling_block`), and by Johnny's count the information is there (64/64 inferable). **Not** "no grammar found" and **not** "no grammar exists": the instrument has no right to either claim (Ark 08:24, Johnny 08:27 UTC). A G reached through a selected λ = 100 reads "weaker than the detection limit", not "absent" (Zcode 08:22 UTC), and since revision 3.1 it can be read from the verdict line (below). The mechanism, "orthogonal" if the primary's `ceiling_full < 0.90` and "no information" otherwise, is printed beside the label as **a description only** (§2.4, decision (c)). **Revision 3.2 (A5):** the label names its gate variable ("gate: rule #2.1's ceiling_block = … >= 0.90"), and the mechanism description names whose `ceiling_full` it quotes ("rule #2.1's ceiling_full = …"); its cut, `MECHANISM_CUT` = 0.90, is borrowed from the gate and not calibrated (§2.4). A low `ceiling_full` with the gate passed gives G ("orthogonal"), not U. |
| **U: on the detection threshold; cannot be separated** (revisions 2 and 3: "too noisy to decide"; renamed by the U rule of §3.6 if no dense-grid world reads U: **"insufficient evidence (uncalibrated)"**, never read as a finding) | anything else (the condition is unchanged) | The legs disagree; or the regrowth sits between `p_P` 0.01 and 0.10; or `ceiling_block` is below 0.90, which means that the rule cannot hold the block even when trained on it alone (by §2.4 this is a failure of the fit, since the block is rank 1), so its failure to regrow says nothing; or the two D1 candidates disagree on R/W. The report states which of these applied. **Revision 3.1 (Ark 09:32 UTC; Zcode agreeing; Johnny recording his falsifier as his own error): U is the signature of the threshold, not an independent state.** In the synthetic worlds it appears only in the transition band [γ\*_P, γ_R), between "not seen" and "seen at the R level" (§3.6). A U on the real block is read as "on the detection threshold; cannot be separated". It is printed with the band's width in grid steps and in γ. (A U whose only reason is `ceiling_block` below 0.90 is still a failed fit, as stated above.) **Revision 3.2 (Ark, V2): U is the signature of the detection limit γ\*_P, not of the band;** all 3 pre-run U worlds sit at γ = 0.6 = γ\*_P, and the band's width is uncertain by up to two grid steps (§3.6). The label prints γ\*_P beside the band. **Revision 3.2 (V4, A2): a U whose reasons include `ceiling_block` below 0.90 is a failed fit, whatever else is listed.** Its label text is "failed fit: rule #2.1 cannot hold the block even when trained on it alone", and the U rule's rename never applies to it. Every other U keeps the threshold reading, or the U rule's name. This branch never ran in the pre-run (`ceiling_block` = 1.0 in all 225 rule #2.1 and BF rows); a test injects the reasons and checks the text (`test_knockout_regrow_labels.py`). **Revision 3.3 (A4): a `ceiling_block` that was not measured is not a failed fit.** Its reason is "rule #2.1's ceiling_block was not measured, so the G gate of section 4 cannot be read" (not "n/a is below 0.90"), its label text is "not measured: rule #2.1's ceiling_block was not measured; the G gate cannot be read", and the U rule's rename never applies to it. A failed-fit reason, when also present, takes precedence. **Revision 3.3 (A3):** only a threshold U enters the U rule (§3.6). |

**The verdict line** prints: the label (G with γ_R, γ\*_P and the family limit, their brackets,
the per-γ fractions seen/n and R/n, the transition band and the instrument; U under the name the U
rule gives it, with γ\*_P and the band, or, when its reasons include `ceiling_block` below the
gate, as a failed fit (revision 3.2), or, when `ceiling_block` was not measured, as "not
measured" (revision 3.3)); for G, the mechanism, marked "description only"; the primary's
`AUC`, `p_S` (with `n_ge` of `99 − n_deg`) and `p_P`; **both ceilings, `ceiling_full` and
`ceiling_block`**; the R/W reading on each D1 candidate; **the λ selected by each knockout fit**
(rule #2.1 and BF_1–BF_4, each chosen by its nested inner folds; revision 3.1); and, if
`n_deg > 5`, the sentence "`n_deg` of 99 shuffles have no AUC on the block and are excluded from
leg S, which counts against `99 − n_deg` shuffles (smallest `p_S` …)" (§3.2). If the No
contingency of §3.6 was triggered, the verdict line quotes it. **The fixed λ = 1 diagnostic is not
on the verdict line** (§3.5, Johnny's condition). It is printed in the report beside the limits.
**Revision 3.3 (A7):** a real-arm run made with `--allow-dirty` ends its verdict line with "NOT
THE REGISTERED RUN: made with --allow-dirty; this verdict cannot be cited as the registered
result (sections 3.3, 7)." (§3.3).

**λ on the verdict line (revision 3.1; Zcode's request of 08:22 UTC, addition 1 (i); Ark 09:32
and Zcode 09:34 UTC vote yes).** The selected λ is already in each fit: `bf_lambda` for BF_r,
and the λ of rule #2.1's final fit for the primary. The verdict line prints it for all five
predictors. **If the label is G and any of them selected λ = 100**, the line adds: "G reached
through λ = 100 on …: there the interaction is shrunk to N1's additive prediction, so this G reads
'weaker than the detection limit', not 'absent'". So a G reached through λ = 100 can be read
from the verdict line alone. The λ values decide nothing. The label is set by §4's conditions
only.

**Why these cuts.** `p_S = 0.01` is the smallest a 99-shuffle leg can give, and it is the P3
standard. `p_P <= 0.01` puts the permutation leg on the same footing. The W level uses the FlyWire
registration's family correction. G asks for a *clear* failure, `p_P > 0.10`, of every predictor,
so that a near miss is read as U and not as G. The cut of 0.90 on `ceiling_block` means that the
rule, trained on the block alone, misorders at most one pair in ten. Below that, a regrowth failure
could be a failure to fit, so it is not read as G (D5). The same 0.90 on `ceiling_full` names the
mechanism of G as a description and decides nothing (revision 3). Since revision 3.2 the two are
separate named constants, the gate cut (`GATE_CUT`) and the mechanism cut (`MECHANISM_CUT`),
both 0.90; the mechanism cut is borrowed, not calibrated (§2.4). **What "too noisy" means on flyvis-65.** The template has no columns
(the column test, §8: flyvis 1.2.0 ships only the merged, averaged estimate). So the noise of this
test is the resolution of a 64-cell AUC, together with the rule's capacity, not within-fly
variation. The 34/27 is printed apart (§2.4).

**What decides.** The label. `AUC`, `p_S`, `p_P`, the two ceilings (beyond their roles above),
the mechanism description of G, the three limits, the per-γ fractions, the transition band, the
selected λ values, the regrown shares, every BF_r row,
the N1 row, the mirrors, the row-and-column `p_P`, the permuted-block ceilings, the per-type rows
and the fixed λ = 1 diagnostic are printed beside it (lesson f: registered rows verbatim, under
their names) and decide nothing.

## 5. What each outcome means for the forward path

| label | consequence |
|---|---|
| **R** | The first evidence of generation for this rule: an edge of the tree can be held to the knockout standard (ADR-005 decision 3). It holds for the averaged template only, until the male-CNS arm (§8) reads R too. Question (ii) may resume under its own registration (ADR-005 point 5). |
| **W** | The grammar line needs a better rule, not a different bank. The rank that passed is the lower bound on what the rule must represent. (ii) waits for a rule that passes. |
| **G: not detected at the R level above γ_R** | This family regrows no structure in the block at the R level at or above γ_R in M-world units. The leg-P limit γ\*_P and the family limit are printed beside it, with the instrument named on the label (revision 3.1). The forward path must not claim that the rule generates the optic lobe's motion circuit. It must not claim either that the block has no grammar: structure weaker than γ_R is not excluded, and the column test suggests that real structure may be weak. Whether any rule could detect it is not shown. The mechanism description ("orthogonal" or "no information") is printed and carries no consequence (revision 3). |
| **U: on the detection threshold; cannot be separated** (or, under the U rule, **"insufficient evidence (uncalibrated)"**) | Nothing is concluded beyond this: the block sits at the instrument's detection threshold, in the transition band, where this design cannot separate "seen" from "not seen" (revision 3.1). Whether to change the block, the family or the bank returns to Mike. If the U rule renamed U, the label is never read as a finding. If the No contingency was triggered (§3.6), U does not exclude an orthogonal block. **Revision 3.2:** the block sits at the detection limit γ\*_P (Ark, V2). **A U whose reasons include `ceiling_block` below 0.90 is a failed fit** ("failed fit: rule #2.1 cannot hold the block even when trained on it alone"; V4, A2): the rule could not hold the block even when trained on it alone, so nothing about the block is concluded, and the fit, not the block, returns to review. The U rule never renames it. A low `ceiling_full` with the gate passed is not this case: it gives G, with the description "orthogonal", not U. **Revision 3.3 (A4):** a U whose `ceiling_block` was not measured ("not measured: …") concludes nothing about the block either; the measurement, not the block, returns to review, and the U rule never renames it. |

## 6. What the test cannot show

- **One block, one pathway.** A pass says that the rule regrows *this* block. Other blocks (the
  candidates note's B and C) are not tested.
- **The template, not an animal** (§0, the column-test anchor). The board's perfection may partly be
  averaging. On FlyWire, one column holds 0.89 of its pairs inside flyvis-30 against 0.964 for the
  average. The male-CNS arm addresses this only as far as its own bank is un-averaged, which its
  builder decides (§8).
- **The answer key is textbook.** The block was chosen by an author who knew the answer (candidates
  note, risk 3). This is mitigated by fixing the rule, rank, legs and cuts before the run, and by
  the fact that no predictor reads names. It is not removed.
- **Mirror cells and the other T4/T5 inputs stay in training** (§1.3, §1.4). They are printed; no
  registered predictor uses mirrors directly.
- **Existence only decides** (proposal, D7). The harness's offset, count and sign fields are
  printed for the 32 present block cells. They decide nothing, and rule #2.1's offsets failed C6.
- **G is relative to the family and to its detection limits.** It cannot rule out a grammar that
  no BF_r of rank ≤ 4 and not rule #2.1 can express, nor one weaker than γ_R (revision 3.1;
  revision 3 said γ\*). Between γ\*_P and γ_R leg P alone sees a majority of worlds, and
  the full reading rule does not.
- **The λ switch: a measured property of the instrument (revision 3; Ark 08:24, Johnny 08:27,
  Zcode 08:22 UTC).** The nested choice of λ is not a slider but a switch. `fit_bf` selects the λ
  with the best inner held-out log-likelihood, and a tie within 1e-9 goes to the **larger** λ
  (`harness.py:727-728`; `BF_LAMBDAS` = [1, 3, 10, 30, 100], line 535; rule #2.1 copies both,
  `second_rule_v21/fit.py:57, 68, 142`). At λ = 100 the interaction term is shrunk to nothing, and
  the prediction is N1's. Johnny checked the lines in the code himself (08:27 UTC). **Measured in
  the synthetic runs** (the counts are in §3.6, "What the runs found"): across all 23,850 fits
  that select λ (rule #2.1 and BF_1–BF_4, on the knockout, full-bank, block-only, permuted-block
  and shuffled banks of all 45 worlds), the selected λ was 1, 3 or 100, and **never 10 or 30**.
  The consistent reading is that at λ ≥ 10 the interaction is shrunk to the same N1 prediction,
  so λ = 10, 30 and 100 tie and the tie goes to 100. λ = 100 is then "off": pure N1, `p_P`
  large, read G. **The switch has an intermediate state, measured by the dense grid of revision 3,
  which revised the reviewers' "on/off only" reading.** At γ = 0.6, every one of the 5 worlds
  selected λ = 3, and 3 of them read **U**. The interaction survived but was partly shrunk: the
  primary's mean knockout AUC was 0.670 at the selected λ = 3, and 0.753 at a fixed λ = 1. In
  the revision-2 run (γ ∈ {0, 0.5, 1.0, 2.0}) no world fell in this state, which is why U was
  not visited there. So the power curve is a steep step (1 of 5 seen at γ = 0.5, 3 of 5 at 0.6,
  5 of 5 from 0.75), not a pure switch.
  **Revision 3.1: λ is a three-position knob (Ark's measurement, 09:32 UTC).** Of the five
  registered values, λ took only three across the 23,850 fits: **1** (on: the interaction is
  fitted), **3** (partly shrunk: the state of γ = 0.6 and of the U readings), and **100** (off:
  pure N1). 10 and 30 never occur. This is recorded as a property of the instrument. The registered
  grid is not changed, since that would change the instrument (§3.6). **Ark's self-correction
  (09:32 UTC):** his earlier description, that the interaction "survives or zeroes", was too
  strong. The λ = 3 position is a real third state, in which the interaction survives only in
  part. **Link to P3 (Johnny, 08:27 UTC):** in BF_1's P3 run, 66 of the 99
  shuffled banks had a margin of exactly 0.0, 33 a negative one and none a positive one, and 943
  of 990 fold margins were exactly 0.0
  ([BF_1 P3 note §2](../notes/2026-09-24-bf1-p3-what-it-showed.md)). Johnny identifies this as the
  same switch. That note's one-fold diagnostic showed λ = 100 selected, with max |U Vᵀ| =
  6.1e−20, so BF_1 equals N1 and its margin over N1 is zero.
- **Low power at small effects.** With 64 cells, a leg P pass needs AUC ≳ 0.67. Below γ\*_P a
  weak regrowth mostly reads G (λ = 100 selected). In the transition band [γ\*_P, γ_R) it can
  read U (λ = 3, partly shrunk). The M worlds (§3.6) measure how weak an effect the design can
  see, as the three limits, and G is stated relative to them (revision 3.1). With 5 worlds per γ,
  each limit is uncertain by about one grid step (Johnny's binomial note, §3.6).
- **The limits come from the synthetic step, not from the real block** (revision 3.2). They are
  pre-run values until the registered run recomputes them, and the γ_R bracket rests on the
  worlds fitted by revision 3 only (§3.6).
- **The G gate is nearly automatic on this block.** The block is rank 1, so `ceiling_block` ≈ 1
  is expected in every world (§2.4). The gate catches a failed fit, not a lack of expressivity.
- **An orthogonal block may be indistinguishable from absence**, if the No worlds read U (§3.6,
  the No contingency).
- **Degenerate shuffles.** Since revision 3 (D14 (ii)) they are excluded from leg S, which then
  counts against `99 − n_deg`. Many of them coarsen `p_S`, and the verdict line names the count
  above 5 (§3.2).
- **U is calibrated only by the dense grid** (revision 3; Zcode 08:22, Johnny 08:27 UTC). No
  world of the revision-2 run read U. On the dense grid, 3 of 25 worlds read U, all at γ = 0.6,
  just at γ\*. So under the U rule, U **stays** "U: too noisy to decide", and its frequency is
  printed (§3.6). What it is calibrated against is thin: 3 worlds, at one γ, all in the λ = 3
  state. **Revision 3.1:** U is read as the signature of the threshold: "on the detection
  threshold; cannot be separated" (§3.6, §4). The reading rests on the same 3 worlds, all inside
  the one-step transition band of the pre-run table. **Revision 3.2 (Ark, V2):** all 3 sit at
  γ\*_P itself, so U is the signature of the detection limit γ\*_P, not of the band; the band is
  a difference of two limits and is uncertain by up to two grid steps. None of the 3 involves
  `ceiling_block` (§3.6).
- **Typing caveat for the control arm:** the male CNS typing may lean on connectivity, as may
  FlyWire's (ADR-005 point 5). Unverified.

## 7. Environment, script, run command, outputs, cost

**Environment.** `tools/.venv` (Python **3.10.20**, numpy **2.2.6**; read 2026-09-24 UTC), not
modified. The flyvis-65 arm reads no feather file, so it needs no `uv run`. The harness is
numpy-only and pinned, so **the run is on CPU**.

**The instrument is the pinned CPU numpy harness (revision 3.1; Mike, 09:34 UTC).** Every limit,
λ count and pre-run value in this file belongs to that instrument (§3.6). Mike: a GPU would be "a
separate instrument, not a rewrite of the CPU instrument that already exists". Ark measured why a
port does not pay here. `bf_als` at r = 4 takes 23.8 ms per call with `starts` = 1 and 183.8 ms
with `starts` = 10. That time is numpy dispatch overhead on small matrices, not arithmetic, so a
straight port would be slower. Batching the fits would be a rewrite. **A GPU instrument, if one is
ever built, is a separate instrument.** It is validated on its own, with its own registration and
its own synthetic worlds. It inherits none of this instrument's limits, and this registration does
not use it.

**Script (written after revision 2, revised with revisions 3, 3.1, 3.2 and 3.3; not committed as of
revision 3.1, and committed since by `8a514fa`):**
`results/genome/c6/checks/knockout_regrow.py`. It imports `harness` and loads rule #2.1 through
`harness.load_rule`, with no copies. **Its label test (revision 3.2):**
`results/genome/c6/checks/test_knockout_regrow_labels.py` calls `label_text` and `read_label`
with injected U reasons (the positive control of §4's failed-fit branch) and `csv_compare` on
hand-made tables; it fits nothing. **Revision 3.3** adds tests for the not-measured U text;
two probes in place of revision 3.2's equality pin, each moving one cut to 0.95 and requiring
that only the texts which print that cut move (expected strings built from the constants); the
U rule's count of threshold U; `csv_compare`'s key matching (a permuted copy of the rows gives
outcome 1 with the order recorded), missing rows, outcome-3 parts and column-8 rename check; and
the `--out` guard on a temporary folder with a monkeypatched `PRERUN_DIR` (never the real one):
14 tests. (`label_text` here is a function; `flywire_column_test.py`
has an unrelated dict `LABEL_TEXT`.) Order of work, each step refusing on failure:

1. **The real arm** refuses on a dirty tree under `results/genome/c6/` or `docs/plans/` (this
   registration and the script committed first). **`--synthetic-only` does not refuse** (revision 3,
   correcting revision 2, which said step 1 always refuses and so contradicted D11). It is run
   *before* commit by design (D11), so it records the tree state in its manifest
   (`tree_dirty_under_c6_or_plans`) instead. Both modes check the pins (§1.1).
2. Machine checks (§3.4). Checks 1, 2, 4 and 7 run in both modes. Checks 3, 5, 6, 8 and 9 read the
   real block or fit a rule on the real bank, so they run in the real arm only.
3. **Synthetic worlds and the two-world check** (§3.6): the requirement rows, the power curve and
   the three limits with the transition band (revision 3.1), the U rule, and the fixed λ = 1
   diagnostic with its path check (§3.5). **The pre-run reproduction (revision 3.1, revised in
   3.2):** `synthetic_worlds.csv` of this run must equal the pre-run file on the deciding columns
   (§3.3, below); byte identity is recorded, not gated. The per-fit diagnostic is computed beside
   it and decides nothing. The synthetic outputs are written to the run's private directory
   *before* the check is read, so a failure can be cross-checked. Stop on any failed requirement
   or failed reproduction (outcome 3 of §3.3). No real block score exists yet. **Revision 3.3
   (A2):** because the outputs are written before the outcome test, a failing run also writes;
   it is the `--out` guard below, not this order, that protects the reference. A run makes one
   write before the test, not two: `--arm` and `--synthetic-only` are mutually exclusive, and
   `--out` is refused with `--arm`.
4. The real arm: knockout fits (primary, BF_1–BF_4, N1), both ceilings (`ceiling_full` and
   `ceiling_block`), 99 shuffles × 6 predictors, leg P and its row-and-column variant, the
   permuted-block `ceiling_full` values, and the fixed λ = 1 knockout fits of the primary and each
   BF_r (diagnostic).
5. The verdict (§4), with the three limits and the U rule taken from step 3, then everything in
   §3.5; write the outputs.

**Run commands (pinned):**

```
tools/.venv/Scripts/python.exe results/genome/c6/checks/knockout_regrow.py --synthetic-only --starts 10 --workers 30
tools/.venv/Scripts/python.exe results/genome/c6/checks/knockout_regrow.py --arm flyvis65 --starts 10 --workers 30
```

`--synthetic-only` runs steps 1–3 and touches no real block cell. With `--out DIR` it writes its
outputs there. With `--from-raw FILE` it re-reads the saved fits of an earlier synthetic run and
fits only what those lack: new worlds and fixed-λ fits (revision 3). A world's fits are
deterministic given its seed, so a re-read world is the same world. (Revision 3.2: that sentence
states determinism within one version of the code. The equality across versions that it was used
for is now measured, with its limits: the knockout view only, on one machine; §3.3, fact (a).)
**A `--from-raw` pass is not a reproduction (revision 3.2):** it still compares its table with
the pre-run one and prints the outcome, but it reports that the table was re-read from saved
fits, and its result neither passes nor fails the gate. The real arm refuses
`--from-raw` and the smoke options, and it refits the synthetic step in full. `--starts 10` is the
`k` of rule #2.1's C6 run (`ATTEMPTS.md`). The manifest records the Python and numpy versions
actually used, and the run stops if they are not 3.10.20 and 2.2.6. **Since revision 3.2 the
manifest also records** (`machine_record`): the BLAS numpy was built with (`numpy.show_config`:
scipy-openblas, OpenBLAS 0.3.29, `DYNAMIC_ARCH`), the BLAS loaded at run time (`threadpoolctl`),
the machine and CPU identification, and the values of `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`,
`MKL_NUM_THREADS` and `NUMEXPR_NUM_THREADS`, both as found in the environment at start and as in
effect (the script's `setdefault` to 1 does not override a value already set). It also records
`prerun_csv_byte_identical`, `prerun_comparison_outcome` and `prerun_reread_from_saved_fits`.
**Since revision 3.3 the manifest also records** (B6, F10, A7): `tree_dirty_paths`, the lines of
`git status --porcelain` under `results/genome/c6/` and `docs/plans/`, not only the boolean;
`from_raw_record`, the `--from-raw` file with its sha256, whether it exists, and whether it is
the pinned store; `prerun_comparison_outcome_3_parts`; `null_input_digests` (§3.3); and
`not_the_registered_run`, set for a real-arm run with `--allow-dirty`. Under `--from-raw` the
per-fit diagnostic is marked for what it compares (§3.3).

**Outputs (committed; all aggregate):** `results/genome/c6/checks/knockout_regrow/` with
`RESULT.md` (the verdict line, the §4 row quoted verbatim, the §3.5 table, the pre-data tables of
§1.4, the two-world check table), `summary.json` (valid JSON, `null` for undefined), and
`per_shuffle.csv` and `synthetic_worlds.csv`. The flyvis bank is committed already, so nothing is
licence-restricted.

**What `synthetic_worlds.csv` cannot show (revision 3.2, text only).** It has one row per world
and predictor, 33 columns, and its format is unchanged from revision 3. It has no rows for the
shuffled fits (`|sh:`) or the permuted-block ceilings (`|pc:`), only their aggregates (`n_ge`,
`p_S`). It has no `n_present` or `n_absent` (they are printed on the verdict line, not written to
the CSV) and no U reasons (they are in `synthetic_only.json` and in the run's printed log). Column 8,
`mechanism_description`, is world-level: 84 rows carry text in the pre-run table, and in 70 of
them the quoted `ceiling_full` is rule #2.1's, not the row's own. **Revision 3.3 (C1):** column 8
is a world-level field derived from rule #2.1's row of that world and repeated on all six rows of
the world; the 84 rows are the 14 G worlds (5 Nf, 5 No, 4 M0.5) × 6. Since revision 3.2 the text
says so ("rule #2.1's ceiling_full = …"), which changed the text of those 84 rows and, with it,
the bytes of the file (§2.4, §3.3).

**Private outputs (revision 3; revision 2 did not name them).** `--synthetic-only --out DIR`
writes its files **outside the repository**, and they are not committed: `SYNTHETIC.md` (the
two-world check, the power curve and the limits, the U rule, the fixed-λ table, and every world's
§3.5 table), `synthetic_only.json` (the same in full, with the manifest), `synthetic_worlds.csv`,
`raw_fits.json.gz` (every fit's `p_exist` and labels on the 64 block positions of each world, the
input of `--from-raw`), and, since revision 3.1, `SHA256SUMS.txt`. They hold synthetic worlds
only, no real block cell, and nothing licence-restricted. The runs of 2026-09-24 and 2026-09-25
wrote them to CC's session scratchpad (`knockout_synth/full/` for revision 2;
`knockout_synth/rev3_old/` and `knockout_synth/rev3/` for revision 3).

**The pre-run outputs, kept for cross-checking (revision 3.1; Ark 09:32 and Zcode 09:34 UTC
require them before commit).** The outputs of revision 3's synthetic runs have been copied to

`C:\Users\mikha\Documents\dpc-research\connectome-seed-data\knockout_regrow\synthetic_rev3_prerun\`

that is, `connectome-seed-data/knockout_regrow/synthetic_rev3_prerun/`, beside the repository.
The folder holds `SYNTHETIC.md`, `synthetic_only.json`, `synthetic_worlds.csv`, `raw_fits.json.gz`,
`rev2_full.log` (the log of revision 2's full run) and `SHA256SUMS.txt`. The checksums are:

| file | sha256 (raw bytes, from `SHA256SUMS.txt`) |
|---|---|
| `SYNTHETIC.md` | `4526d2239c6bf378b161b7fb92bab2c022b0ac648a88fcda8fa02f86f9e58264` |
| `raw_fits.json.gz` | `91035af838446b86bda502fe8bf719910550bbad72c1cb12563800a984819e60` |
| `rev2_full.log` | `fa5606e37ebcb8e7b4aac69ba592638e3f77cfea9cbff58b639be2ee8ea960d0` |
| `synthetic_only.json` | `ea812dfd87238a4a23ca54e06faf5c1d93c7802a36ee28eff9857183236377dd` |
| `synthetic_worlds.csv` | `7a2f02953207f8aacb1cbd8c5e61e7731135d5a6f800a40b359cb0ff12f9c8f1` (pinned in the script as `PRERUN_WORLDS_CSV_SHA256`) |

`SYNTHETIC.md`'s header records revision 3, git head `ea60011` with both files untracked (as of
that run), and a runtime of 8 s. That runtime fits a `--from-raw` re-read of the saved fits, not a
fitting run; its line "0 new world fits" confirms it (§3.3).

**Every listed file is checked (revision 3.2; Ark).** The script pins all five checksums above
(`PRERUN_SHA256`) and, before comparing, reads every file listed in the folder's
`SHA256SUMS.txt`; each must match both the list and its pin, and the list must name exactly these
five files. A mismatch fails the reproduction gate (in a `--from-raw` pass it is reported only).
Since revision 3.3 (C6), entries of the folder that are neither listed nor pinned (the
`provenance/` subfolder below is expected there) are reported, not failed.

**Provenance records of the fitting runs (revision 3.2, to be added by CC).** The pinned table
was written by a re-read; the `SYNTHETIC.md` files of the two runs that fitted its worlds exist
only in CC's session scratchpad of 2026-09-24/25:
`…/f96abe4f-2e69-41dd-821c-62f19d58822d/scratchpad/knockout_synth/full/SYNTHETIC.md` (revision 2,
runtime 5122 s) and `…/knockout_synth/rev3/SYNTHETIC.md` (revision 3, runtime 2647 s, "19110
re-read, 9480 new world fits, fixed lambda 2 reused, 73 fitted"). They are to be copied, as
provenance records, to `connectome-seed-data/knockout_regrow/synthetic_rev3_prerun/provenance/`
with their own `SHA256SUMS.txt`. They are not copied into the pinned folder itself, whose five
files and checksums stay as above.

**The `--out` guard (revision 3.3, A2 and C4; items ㊷ ㊸).** Before revision 3.3 nothing guarded
`--out` (CC's probe P4: it was used as given when the synthetic outputs were written), and
`write_sha256sums` writes the sums over the folder's files (files only; subfolders are
ignored). So a `--synthetic-only --out` pointed at the reference would have overwritten it and
re-summed it. In step 1 of `main`, before any write or `mkdir`, the script now refuses
(`out_dir_refusal`): `--out` with `--arm` (the real arm writes to its own private directory and
ignored `--out` before); `--out` that resolves to `PRERUN_DIR` or to a path inside it; and a
folder that already holds a byte copy of the reference, that is, at least one file named like a
pinned file is present, and every such present file matches its `PRERUN_SHA256` pin. A folder in
which a present pinned-name file differs, or an empty or new folder, may be written. A missing
file is not a differing one. **Falsifier:** the content guard tells a byte copy of the reference
from a fresh run's folder only because `raw_fits.json.gz` is not byte-reproducible (gzip writes
its mtime, item ㊱, §3.3). If `write_raw` ever becomes deterministic (a fixed mtime), a fresh
run's folder could look like a copy of the reference, and the guard must be revisited.

**Recreating the reference (revision 3.3, A2, item ㊹).** The reference is never recreated in
place. A new reference is written to a new folder and compared with the old one; then
`PRERUN_DIR` and `PRERUN_SHA256` (and `PRERUN_WORLDS_CSV_SHA256` with them) are moved together,
in one registered, committed change that is reviewed before use. **A red pin is never answered by
re-pinning.**

**The registered run's private and raw outputs (revision 3.1).** The real arm writes them outside
the repository, to `connectome-seed-data/knockout_regrow/<run>/`, where `<run>` is
`<arm>_<UTC stamp>_<first 12 characters of the git head>`, for example
`flyvis65_20260926T100000Z_0123456789ab`. The script sets it (`PRIVATE_ROOT`,
`private_run_dir`). Written there: the synthetic step's `SYNTHETIC.md`, `synthetic_only.json`,
`synthetic_worlds.csv` and `raw_fits.json.gz`, all before the two-world check is read; then
`raw_fits_real.json.gz` (every real-arm fit's `p_exist` and labels on the 64 block cells:
knockout, ceilings, shuffles and permuted-block ceilings); and `SHA256SUMS.txt`. The manifest
names the directory (`private_outputs`). The flyvis bank is committed, so nothing there is
licence-restricted. They stay private because they are per-fit files, not aggregates.

**The reproduction requirement (revision 3.1; Johnny 09:33, Zcode 09:34 UTC; its gate revised
in revision 3.2, below and §3.3).** *This paragraph is as of revision 3.1; its byte-for-byte
requirement is replaced by revisions 3.2 and 3.3 below and in §3.3 (C3).* Revision 3's
numbers were produced while this file and the script were still being edited, and both are
untracked (header; as of revision 3.1, and committed since by `8a514fa`). The script's last save before revision 3.1 (08:44:21 UTC) falls inside the
fitting window of revision 3's added worlds (08:39–09:23 UTC). Whether that mattered is not known
from the files; the comparison below settles it. The registered run therefore recomputes everything from a clean committed
tree, the synthetic step included, in one run with one manifest (§3.3). With the same seeds and
the same pinned environment, its `synthetic_worlds.csv` **must reproduce the pre-run file byte for
byte**. The script first checks the pre-run file against its pinned sha256, then compares.
Every world, predictor and column is compared: labels, AUCs, `p_P`, `p_S`, both ceilings and the
selected λ. A missing pre-run file, a pre-run file that fails its checksum, or any difference
("PRE-RUN TABLE NOT REPRODUCED", with the first differing cells printed) fails the two-world check,
and the real arm does not run. A `--synthetic-only` run makes the same comparison when it is
complete (every family, 5 worlds, 99 shuffles, 20 permuted ceilings, `--starts 10`), and a smoke
run is marked "not comparable". The CSV writer is unchanged from revision 3, byte for byte, so
that the comparison is possible.

**Revision 3.2 replaces the byte comparison of the paragraph above** (Johnny blocked it as
written; Ark asked for changes; V1 in §10). The gate compares the deciding columns row by row,
with the three outcomes and their treatment of §3.3; a difference in the identity or lattice
columns, or in a continuous column beyond `MACHINE_CHECK_TOL`, prints "PRE-RUN TABLE NOT
REPRODUCED" with the first differing cells and fails the two-world check. Byte identity is
recorded in the manifest as a fact. The CSV format is unchanged (33 columns, the same writer);
only the text of column 8 changed (§2.4), so the fresh table is not byte-identical to the
pinned one, while its deciding columns are (the `--from-raw` re-read of revision 3.2, §3.3).
**Revision 3.3** matches the rows by key instead of by position, splits outcome 3 into its
parts (a) and (b), and rewrites the treatment (§3.3).

**The printed "mean seconds per knockout fit" (revision 3.3, item 4; Ark 15:20).** It averages,
per predictor, every record with mask `ko`: in each world the base knockout fit and the 99
shuffled-bank knockout fits, so 100 per world and 4,500 over the 45 worlds. Under `--from-raw`
these are the `secs` saved by the runs that made the fits. The script prints the population
beside the means (`mean_seconds_population`). It is a timing, not a claim about cost.

**Cost (measured; revision 3 replaces revision 2's estimate, which was about half the measured
cost).** CPU, 30 workers, `--starts 10`:

- **Revision 2's synthetic run:** 30 worlds, 18,960 fits (30 × (3 × 6 + 20 + 99 × 6)), **5,122 s,
  about 85 min** (2026-09-24, 21:32–22:58 UTC). Revision 2 had estimated about 1 hour.
- **Revision 3's added worlds:** 15 worlds (M0.6, M0.75, M0.85), 9,480 fits, plus the fixed-λ
  fits: **the 9,480 world fits in **2,634 s, about 44 min** (2026-09-25, 08:39–09:23 UTC), and the 73 new fixed-λ fits in 5 s**. Re-reading the 30 saved worlds and fitting their 100 missing fixed-λ fits
  took 18 s.
- **The registered real-arm command** refits the synthetic step in full: 45 worlds, 28,440 fits,
  about **2 h 10 min (about 3.65 fits per second)** at the measured rate. The real block itself is 6 × (3 + 99) + 20 = 632
  fits, plus up to 5 fixed-λ fits, **about 3 min** at the same rate. Permutations are scoring
  only, seconds.

## 8. The animal control: Janelia male CNS v1.0 (described; runs only after its builder is reviewed)

**Fixed by decision:** the animal control is the **Janelia male CNS v1.0** (Berg et al. 2026; one
male; CC-BY; `connectome-seed-data/Janelia/`, downloaded 2026-09-23 UTC). FlyWire-30 is kept as
provenance, with its 14/64 inferability.

- **It runs only after a separate step:** a bank builder for the male CNS, registered and
  reviewed on its own (type mapping, column assignment and averaging, threshold, handedness), in
  the way `flywire_bank_builder.py` was. **The male CNS bank and its builder are a separate
  registration.** **This registration will be amended, before that arm runs, to pin the built
  bank's sha256**, and nothing else in it changes.
- **What the review settled for the builder (recorded here, decided there).** Ark 20:48, Johnny
  20:50–20:53, Zcode 20:59 UTC, 2026-09-24:
  - **Type map accepted.** R1–R6 are one type. CT1 is mapped with the side flip: Zcode verified that
    CT1_L has 100 % of its weight with right-lobe partners. TmY9 is flagged. Johnny notes that
    `flywireType` gives TmY9q and ready R7/R8 roll-ups (1300/1329) that avoid 931 `_unclear`
    bodies. **The builder must declare one canonical name column**, because the two differ: T4d is
    1709 by `type` and 1710 by `flywireType`.
  - **The pair threshold is the builder's first open parameter.** The preliminary graph counted a
    pair when its total synapses divided by the number of target neurons in the lobe was at least
    1, which is about a sum of 850 or more. Under that definition the block is a perfect board with
    4 mirror cells. Zcode showed that under other definitions the board is not perfect: 20–21 weak
    cross cells with means of 1.0–2.2, and 52–54 mirror cells. **So the perfect board and the 4
    mirror cells depend on the threshold.** **64/64 inferability holds at every threshold Zcode
    tried.** For this arm, machine check 3 (§3.4) is therefore set by the builder's registered
    threshold, not by the flyvis-65 count.
  - **Reading the data.** Weights are read in chunks (a full read was killed at 18.1 GB). The
    builder's self-test stops on zero name matches. `#`-comment header lines are skipped.
  - **Within-animal null.** The left and right optic lobes of the one male are named as a
    within-animal null: the same block read per lobe, whose difference is variation inside one
    animal. Its use is decided with the builder.
  - **Recorded asymmetries.** R1–R6 is asymmetric between the lobes: 2265 right, 1112 left (as
    counted in review). CT1 and Am1 have n = 1 per lobe.
- **The same block by name.** All 16 names must map; the builder states the mapping. The same
  legs, cuts, seeds and branch rule apply. The male-CNS bank is embedded in the 65-type harness
  grid as the FlyWire arm was (`flywire_bf_p3.py`, `restrict_to_30_grid`): the harness's folds and
  `TYPE_FIELDS` stay, and cells outside the builder's type set are left out of training and scoring.
- **Printed before its data:** its inferability table, its mirror count, and what each endpoint
  keeps, as in §1.4, from names and outside-block presence only.
- **Its own two-world check** is not needed if the worlds of §3.6 are rebuilt on its degree terms.
  That is a proposal, decided with the builder.
- **Joint reading (proposal, D13):** R on both = "regrows in the template and in one animal"; R on
  flyvis-65 only = "regrows in the averaged template only; the animal does not show it", which
  bears on the column-test anchor; R on the male CNS only = a flag to re-examine both fits; any
  other pair = the flyvis-65 label stands alone, with the control's label printed beside it.

## 9. Lessons applied ([lessons note §3](../notes/2026-09-24-lessons-from-the-art-report.md))

| lesson | where here |
|---|---|
| a, selection after the data | the block, bank and rule are fixed by decision before data; the headline is the primary rule, and BF ranks are printed, not promoted (§2) |
| b, a null that cannot see the other world | §3.6: worlds where the block is regrowable, where it is not (two ways, told apart by the two ceilings of §2.4), where only a higher rank can see it, and where the information is weak, all read by the same code; §3.2 states what leg P can and cannot see |
| c, a criterion written after the finding | a reading for every branch in §4 and §5, including U and W |
| d, the evaluator is the system | reviewed by Ark, Johnny and Zcode before commit; the outcome note is reviewed before it is committed |
| e, read the object | §1.3 names every row removed and every channel left; machine checks 3–6 read the bank and the fitted objects |
| f, a number under its own name | §4's rows are printed verbatim; `p_S`, `p_P`, `ceiling_full` and `ceiling_block` appear under their names |
| g, denominators | 32/32, n of 99, n of 9,999, 64/64 inferable, 4,161 training cells |

## 10. Decisions for review (reviewers, then Mike)

Each item says what the options change, and gives a recommendation. The body is written with the
recommendation. **Votes** are those of the review in the DPC Research chat, 2026-09-24 (Ark
20:56, Johnny 20:58, Zcode 20:59 UTC). Zcode's lane was the control bank. He voted D11 and
deferred on the rest.

| # | question | options (what each changes) | recommendation | votes (2026-09-24) |
|---|---|---|---|---|
| **D1** | Which object is "the registered C6 rule and rank"? | (i) rule #2.1, r = 1: the only rule registered for and run on C6; reads `type_fields`, which are constant over the 8 targets (§1.3). (ii) BF_1: the harness's P4 opponent at that rank; simpler; registered for P3. Under (i) BF_1 is still printed; under (ii) rule #2.1 would be printed. **Addition (Johnny; revision 2, marked for review):** R and W are read on both candidates and must agree, else U (§4, which also gives the reason for choosing this over a margin above a fit cost). | (i), with the R/W agreement | Ark (i). Johnny (i) with the R/W addition. Zcode defers. |
| **D2** | Metric on the block | (i) AUC on 32/32: scale-free, reads directly as ordering. (ii) parity contrast `D` of logits: exactly 0 for N1 and isolates the non-additive part, but in logit units, so λ shrinkage scales it. (iii) log-loss margin over N1, the C6 convention: mixes calibration with ordering. | (i), with (ii) and (iii) printed | Ark (i). Johnny (i). Zcode defers. |
| **D3** | Leg S statistic | (i) AUC margin over N1 on each bank, as in P3; removes the degree channel that shuffles keep. (ii) raw AUC: simpler, but on shuffles N1 alone can score well above 0.5 through degree, which makes the leg test "better than degree" rather than "structure beyond degree". | (i) | Ark (i). Johnny (i). Zcode defers. |
| **D4** | Leg P permutation | (i) uniform within-block permutation, Zcode's null as agreed, primary; row-and-column-preserving printed. (ii) row-and-column-preserving as primary: stricter, since it asks for this board among balanced boards. | (i) | Ark (i). Johnny (i). Zcode defers. |
| **D5** | Branch cuts | leg S `n_ge = 0`; leg P `p_P <= 0.01`; W at 0.0125 over r = 1..4; G needs `p_P > 0.10` for every predictor and **`ceiling_block` ≥ 0.90**, with its mechanism named by `ceiling_full` (revision 2, §2.4, §4); U is the remainder. Lower cuts would make R easier and U rarer. | as written | Ark: as written with the ceiling fix. Johnny: the same. Zcode defers. **Revision 3:** the condition of G is unchanged; its name and reading are "not detected above γ\*", with the mechanism as a description only (decisions (b), (c); all three reviewers, 2026-09-25). **Revision 3.1:** the condition is still unchanged; the name and reading are "not detected at the R level above γ_R; leg P passes from γ\*_P", and U reads "on the detection threshold; cannot be separated" (Ark 09:32, Johnny 09:33, Zcode 09:34 UTC). |
| **D6** | BF ranks printed and used in W | (i) r = 1..4, the FlyWire family. (ii) also r = 8 (M4's rank): more capacity for W; the correction becomes 0.05/5 = 0.01. | (i) | Ark (i). Johnny (i). Zcode defers. |
| **D7** | Fields | (i) existence decides; offsets, counts and sign are printed for the 32 present cells. (ii) also require offsets: rule #2.1 failed offset on C6, so (ii) would test a known weakness. | (i) | Ark (i). Johnny (i). Zcode defers. |
| **D8** | Synthetic worlds | degree terms from N1 on the real knockout view (outside cells only) vs i.i.d. normal; γ values (R 2.0, W γ_z = 1.5 and γ_z1 = 2.5, M 0.5/1.0; axis names added in revision 3.3); the requirement rows, **now including M: U or W, never G, never R, a stop; and No: G (orthogonal), with its contingency** (§3.6). Changing γ after the synthetic-only run requires a new draft. | N1-based terms; γ as written; the M and No rows as in §3.6 | Ark: as written plus the M requirement. Johnny: the same (he raised M to a run condition). Zcode defers. **Revision 3** (the new draft that this row asks for): M is the power curve on the dense grid γ ∈ {0.5, 0.6, 0.75, 0.85, 1.0}, no stop; Nf never R or W (stop) and at least 3 of 5 G; No reads G, never R or W (decisions (a), (b); §3.6). |
| **D9** | Permuted-block ceilings | (i) 20 seeds, printed, decide nothing; **they are `ceiling_full`**, and their expected fall is information (§2.4). (ii) make them a gate for R: a stricter guard against smoothing, but a new cut. | (i) | Ark (i). Johnny (i), marked `ceiling_full`. Zcode defers. |
| **D10** | Seeds | the new range 90000–90154 as in §3.7; **revision 3 adds 90160–90184** for the dense γ grid | as written | Ark: as written. Johnny: as written. Zcode defers. |
| **D11** | Order | the `--synthetic-only` run (it fits rules on synthetic banks, which is regrowth on synthetic data) is made **before** this file is committed, as the column test's revision 2.3 was, so that the requirement rows are known to be reachable. It needs Mike's word. | run it, then commit | Ark yes. Johnny yes (he does not sign the G gate without it). Zcode yes. **Pending Mike.** **Mike: yes, 2026-09-24 21:04 UTC** ("ну ок запускай"). Run 21:32–22:58 UTC; it stopped on the M rows (§3.6, "What the runs found"). Revision 3's added worlds were run under the same approval. |
| **D12** | File date | `2026-09-24-…` (the UTC day, per GLOSSARY) vs `2026-09-25-…` (as requested, the local day) | 2026-09-24 | Ark: as written. Johnny: as written. Zcode defers. |
| **D13** | Joint reading with the male CNS | the table in §8 | as written | Ark: as written. Johnny: as written. Zcode defers. |
| **D14** | A shuffle whose block has no AUC | (i) counts as ≥ real (conservative). (ii) is dropped from the denominator (**adopted in revision 3**). **Note for review (revision 2):** under (i), one such shuffle makes leg S unpassable for every predictor, hence R and W; the verdict line names the count only above 5 (§3.2). | (i) | Ark (i). Johnny (i). Zcode defers. **Revision 3: (ii)**, decision (d), all three reviewers (Zcode 08:22, Ark 08:24, Johnny 08:27 UTC, 2026-09-25), on CC's point 3 of 21:10 UTC: excluded from leg S, which counts against 99 − n_deg; named on the verdict line above 5. |

**Revision 3: the decisions of 2026-09-25 and who voted for what.** DPC Research chat. CC set
out proposals (a)–(d) after the revision-2 run (2026-09-24 23:00 UTC). The three reviewers voted
(Zcode 08:22, Ark 08:24, Johnny 08:27 UTC). CC summarised the consensus and proposed how to settle
its two disagreements (08:28 UTC). Mike supported both settlements and said to proceed (08:30 UTC).

| item | what | Zcode 08:22 | Ark 08:24 | Johnny 08:27 | settled |
|---|---|---|---|---|---|
| (a) | M1.0 reading R is the correct reading, a point on the power curve, not a stop | yes | yes; the stop was a registration error that CC warned of at 21:10; marks the class "a requirement written without checking whether it stops a correct answer" | yes | all three |
| (b) | G with a detection limit, on a denser γ grid | yes, with the denser grid; the limit is relative to the instrument (BF family, nested λ, `BF_LAMBDAS`) | yes, and deeper: **redefine G** as "not detected above γ\*"; the instrument has no right to "no grammar found" | yes, and redefine G; γ\* rests on `BF_LAMBDAS`, the 1e-9 tie rule and `STARTS` = 10, and is printed with them | all three; G redefined; grid γ ∈ {0.5, 0.6, 0.75, 0.85, 1.0} (CC's summary) |
| (c) | mechanism labels of G as description only | yes | yes | yes | all three |
| (d) | degenerate shuffles excluded from leg S, counted against 99 − n_deg, named above 5 | yes | yes | yes | all three (D14 (ii)) |
| — | λ switch recorded as a measured property of the instrument | proposed (addition 1) | found it (`harness.py:727-728`) | checked it in the code himself; linked it to P3's 66/99 zero margins | all three |
| — | revision 3 with a date and a reason, and a journal of votes | asked for a journal of who voted what | asked for "revision 3 with date and reason", and gave the three reasons it is not fitting to the data (§12) | — | CC's summary |
| — | §7 text fixes (D11 order, cost, private outputs) | yes | — | — | CC's summary |
| — | fate of U | keep it; if the real run prints U, examine it separately | — | remove it or calibrate it; an uncalibrated remainder must not be read as "new" | **CC's settlement, supported by Mike 08:30:** the U rule of §3.6 |
| — | BF_r at fixed λ = 1 | — | proposed it | without a registered reading threshold it becomes this run's `k*_obs`; give it a threshold | **CC's settlement, supported by Mike 08:30:** printed as a diagnostic that decides nothing, beside γ\*, not on the verdict line; a threshold only after calibration on the worlds and a vote |
| — | Nf: never R or W (stop), at least 3 of 5 read G | not voted by name | not voted by name | not voted by name | CC's proposal of 2026-09-24 21:10 UTC (point 1), applied as part of the consensus that Mike supported; recorded here as not voted on by name |

Not adopted in revision 3, recorded: Zcode's addition 1 (i) asked for the λ chosen per fold to be
printed on the real verdict line. CC's summary did not carry it. The λ chosen for each fit is
printed in the §3.5 table and in `per_shuffle.csv`, not on the verdict line. **Adopted in
revision 3.1** (Ark 09:32 and Zcode 09:34 UTC vote yes; §4, "λ on the verdict line").

**Revision 3.1: the reviewers' pass on revision 3, 2026-09-25.** DPC Research chat, Ark 09:32,
Johnny 09:33 and Zcode 09:34 UTC. Mike, 09:34 UTC, on the GPU; Mike, 09:35 UTC: "run nothing".
Text and code only.

| item | what | Ark 09:32 | Johnny 09:33 | Zcode 09:34 | settled |
|---|---|---|---|---|---|
| 1 | three limits instead of one γ\*: γ\*_P (leg-P limit), γ_R (R level), family limit; G redefined as "not detected at the R level above γ_R; leg P passes from γ\*_P"; all three printed with the instrument | asked | asked | asked | all three (§3.6, §4, §5) |
| 2 | do not collapse the per-γ fraction: seen/n and R/n at every γ beside the limits; binomial note (n = 5: one grid step; p = 0.2 or 0.4 gives "≥ 3" with probability ≈ 0.06 or 0.32) | — | asked | — | Johnny's request, applied (§3.6) |
| 3 | U is the signature of the threshold, not an independent state; read "on the detection threshold; cannot be separated"; the width of the transition band printed | proposed | his falsifier fired against his structural reading; he recorded it as his own error | agrees | all three (§3.6, §4, §5, §6, §11) |
| 4 | λ selected per knockout fit on the verdict line; a G reached through λ = 100 readable there | yes | — | yes (his request of 08:22) | Ark and Zcode; confirms a point that the drafting subagent had left open (§4) |
| 5 | λ as a three-position knob (1, 3, 100 across 23,850 fits), a property of the instrument; his "survives or zeroes" was too strong | measured it; corrected himself | — | — | recorded (§6, §11) |
| 6 | mutability: both files untracked (as of revision 3.1; `8a514fa` committed them), the registration edited 41 min after the script; the registered run recomputes everything from a clean committed tree in one manifest and must reproduce the pre-run table (same seeds and environment) | — | raised it | same seeds and environment | recorded; the script stops on a failed reproduction (§3.3, §7) |
| 7 | the pre-run outputs kept for cross-checking before commit; the registered run's private and raw outputs named | required | — | required | §7, header |
| 8 | the GPU: a separate instrument, not a rewrite of the CPU one | measured `bf_als` (23.8 ms / 183.8 ms per call at 1 / 10 starts: dispatch overhead) | — | — | Mike 09:34 UTC (§7) |
| 9a | No reads G (drafted by the subagent) | confirmed | confirmed | confirmed | confirmed in the reviewers' pass (§3.6) |
| 9b | Nf: at least 3 of 5 read G (drafted by the subagent; not voted on by name at 08:22–08:28) | confirmed | confirmed | confirmed | confirmed in the reviewers' pass (§3.6) |
| 9c | λ on the verdict line (item 4, drafted as "not adopted") | yes | — | yes | adopted |

The table attributes each item as the request that asked for revision 3.1 attributes it. Where a
cell reads "—", this file records no statement by that reviewer on that item. For items 9a and
9b the request records that "the reviewers" confirmed them. It is recorded here as all three.

**Revision 3.2: the reviewers' pass on revision 3.1, 2026-09-25.** DPC Research chat,
12:06–13:13 UTC: Ark and Johnny; Zcode did not vote and will read revision 3.2. Mike, 13:36 UTC:
"Yes: the subagent applies the edits from Ark's list, CC checks and puts 3.2 to review for all
three; Zcode will read 3.2". Text and code only; no fitting run. **Readiness rule** (Johnny 12:40
UTC; Ark accepted at 12:45 UTC): blocks A and B must both be in the tree before the registered run
starts, and C goes in the same commit. Block D, the GPU, is outside this revision. The table
attributes each item as CC's work order for revision 3.2 attributes it; an item without a name
comes from the review as a whole.

*Votes on the four choices that the drafting subagent made in revision 3.1:*

| # | choice of revision 3.1 | votes | settled in revision 3.2 |
|---|---|---|---|
| V1 | the registered run stops unless it reproduces the pre-run table byte for byte | Ark: yes, with changes. Johnny: **no (block)**, as written | resolved by A1: the gate compares the deciding columns; byte identity is recorded, not gated (§3.3, §7) |
| V2 | the transition band [γ\*_P, γ_R) | yes, with fixes (the B items). Ark: the band is a difference of two limits, each ±1 grid step at n = 5, so a one-step band is one of 0, 1 or 2 steps; all 3 U worlds sit at γ = 0.6 = γ\*_P, so U is "the signature of the detection limit γ\*_P", not "of the band" | §3.6, §4, §5, §6 |
| V3 | `p_P <= 0.01` for every predictor, the family limit included | yes. The family limit is the maximum of the five leg-P limits, 0.75 (BF_2–BF_4 reach a majority only at 0.75; rule #2.1 and BF_1 at 0.6). State that the W gate is family-corrected (0.0125 = 0.05/4) while the limits are not, and why (a limit is a property of the instrument, not of a branch) | §3.6 |
| V4 | a U caused only by `ceiling_block` < 0.90 is a failed fit | yes in meaning, but **not implemented** in the code of revision 3.1 (the label text received no reasons) | A2 (§4, §5; `label_text`; the label test) |

*Items applied:*

| item | what | source | where |
|---|---|---|---|
| A1 | the reproduction gate on the deciding columns (lattice exact, continuous within `MACHINE_CHECK_TOL`, column 8 reported); three outcomes and their treatment written before the run, with the cross-configuration self-test; byte identity recorded; the measured facts (a) and (b); every file of the pre-run `SHA256SUMS.txt` checked; a per-fit diagnostic split by revision-2 and revision-3 worlds | V1 (Ark, Johnny); the pins: Ark N3, with Johnny's note that the list already names all five files | §3.3, §3.7, §7; `csv_compare`, `check_prerun_files`, `check_prerun_reproduced`, `raw_fits_diagnostic`, `PRERUN_SHA256`, `MACHINE_CHECK_TOL` |
| A2 | the U reasons reach the label text; a `ceiling_block` reason gives "failed fit", never renamed by the U rule; the CSV format unchanged; a positive control, since the branch never ran; §5 gets the same carve-out and names G for a low `ceiling_full` | V4; the positive control: Johnny 12:46:20, narrowed at 12:46:56 and 12:48:29 UTC | §4, §5; `label_text`, `ceiling_block_reason`, `verdict_line`, `run_synthetic`, `main`; `test_knockout_regrow_labels.py` |
| A3 | a `--from-raw` pass says that it re-read saved fits and is not a reproduction | — | §7; `check_prerun_reproduced`, `run_synthetic` |
| A4 | the manifest records the BLAS, the machine and the four thread variables as found | — | §7; `machine_record`, `THREAD_ENV_FOUND` |
| A5 | one threshold on two variables split into a gate cut and a mechanism cut (both 0.90); the G text names its gate variable and the mechanism text names rule #2.1's `ceiling_full`; the mechanism cut is borrowed, not calibrated; the gate cut never bound in the pre-run. It changes the text of column 8 of `synthetic_worlds.csv` | — | §2.4, §4, §7; `GATE_CUT`, `MECHANISM_CUT`, `mechanism_description`, `label_text` |
| B1–B4 | the three limits as pre-run values of the synthetic step (γ\*_P = 0.6, γ_R = 0.75, family limit = 0.75), not an answer about the real block; family = γ_R not by construction; what the limits rest on (the γ_R bracket on revision-3 worlds only; M0.5 the only revision-2 exposure; M1.0 enters none); λ robustness; `p_P` defines the limits, `p_P_rowcol` and `p_P_fixed_lambda1` are diagnostics | V2, V3 | §3.6, §6 |
| B5 | "a re-read world is the same world" states determinism within one version; the equality across versions is measured, with its limits | — | §7 |
| B6 | `D` of N1 registered as within `PARITY_TOL` of 0, not 0.0; four pre-run residues | — | §3.1, §3.4 |
| B7 | what the CSV cannot show | — | §7 |
| B8 | `TAU` is inert where it is applied to AUCs; the tie band that matters is λ's | — | §3.2; see §11 for a precision |
| B9 | the regrown share is a ratio, not a share; the column keeps its name | — | §3.1 |
| B10 | the U reasons of the three pre-run U worlds, from the revision-3.1 writer's log | — | §3.6 |
| C | "weak leg" → "leg P" throughout, and "the smallest/largest leg-P limit" (Ark N1, Johnny); "untracked"/"not committed" marked "as of revision 3.1" (Ark N2); the provenance of the fits (§3.7) and of the fitting runs (§7); the code comments on the pre-run outputs and on the limit keys; the name collision `LABEL_TEXT` / `label_text` noted once | Ark N1, N2; Johnny | header, §0, §3.6, §3.7, §4, §5, §6, §7, §10, §12 |

**Revision 3.3: the reviewers' pass on revision 3.2, 2026-09-25.** DPC Research chat,
14:04–14:39 UTC: Ark and Johnny, both "yes, with edits". Zcode voted at 15:05 UTC. CC posted
its probes at 15:1x UTC (§3.3, facts (c) and (d); §7, P4). Procedure, Mike 13:36 UTC: the
subagent drafts, CC checks, all three review. **Acceptance rule** (Ark and Johnny, 14:36–14:37
UTC): a new item enters only if it (1) can destroy an artefact, (2) blocks the run, or (3)
changes the text or the coverage of a quoted verdict-line string. **Readiness:** A and B in the
tree before the registered run starts; C in the same commit. The item codes in the "source"
column (F1, ㉖ and so on) are those of the review as CC's work order for revision 3.3 lists them;
the work order does not attribute each code to a reviewer, and this file does not either.

*Zcode's votes on V1–V4 (15:05 UTC). Zcode's binding vote is on the revision current at the
start of the run.*

| # | choice (§10, revision 3.2) | Zcode, 15:05 UTC |
|---|---|---|
| V1 | the registered run stops unless it reproduces the pre-run table byte for byte | **no**: the reference has no fresh provenance (`SYNTHETIC.md`, line 138); the code of revisions 2 and 3 is lost; byte identity is a fact of one machine, and the `DYNAMIC_ARCH` kernel is not pinned. Supports the column-wise gate on the registered discrete values, the per-fit comparison with `raw_fits.json.gz` as a diagnostic split 30/15, and byte identity as a recorded fact with the machine stamp |
| V2 | the transition band [γ\*_P, γ_R) | yes |
| V3 | `p_P <= 0.01` for every predictor, the family limit included | yes; the family limit is the maximum (0.75) |
| V4 | a U caused only by `ceiling_block` < 0.90 is a failed fit | yes, on two conditions: a committed regression test that exercises the new input through `ev` (it exists: `test_read_label_failed_fit_end_to_end`), and the third branch's text carried over from the dead branch (done in revision 3.2) |

*Items applied in revision 3.3:*

| item | what | source | where |
|---|---|---|---|
| A1 | `csv_compare` matches rows by key (family, j, seed, predictor); missing rows, value differences and row order are separate outputs, and a change of order alone is not outcome 3; outcome 3 split into (a) identity or lattice and (b) continuous beyond the tolerance; the treatment names four layers (fits, null generator, consumer, machine), how each is told apart and the order of reading; the self-test's two outcomes and its mechanism corrected; digests of the null inputs in the manifest | F1, ㉖, ㉗, F10 | §3.3, §7; `csv_compare`, `CSV_KEY_COLUMNS`, `outcome_3_reason`, `OUTCOME_3_PART_TEXT`, `PRERUN_OUTCOME_TEXT`, `repro_fail_treatment`, `REPRO_LAYERS`, `REPRO_BRANCH`, `REPRO_SELF_TEST`, `null_input_digests`, `check_prerun_reproduced`, `main` |
| A2 | the `--out` guard in step 1 (inside `PRERUN_DIR`; a byte copy of the reference; with `--arm`), with its falsifier; "Recreating the reference"; the outputs are written before the outcome test, so the guard, not the order, protects the reference; a test on a temporary folder | ㊷, ㊸, ㊹ | §7; `out_dir_refusal`, `main`; `test_out_guard_refusals` |
| A3 | the U rule counts threshold U only; failed-fit and not-measured U are counted apart | F2 | §3.6; `u_rule`, `u_kind` |
| A4 | a `ceiling_block` that was not measured has its own reason and U text, not the failed fit; test (ii) no longer pins the wrong behaviour | F3 | §2.4, §3.6, §4, §5; `ceiling_block_reason`, `CEILING_BLOCK_NOT_MEASURED`, `NOT_MEASURED_TEXT`, `label_text`; `test_ii_not_measured_is_not_a_failed_fit` |
| A5 | the equality pin `GATE_CUT == MECHANISM_CUT == 0.90` replaced by probes that move a cut to 0.95 and require the printed text to move (since the additions below, two probes, one cut each) | F4a | `test_probe_mechanism_cut_moves_only_the_mechanism_text`, `test_probe_gate_cut_moves_only_the_gate_texts` |
| A6 | under `--from-raw` the per-fit diagnostic is marked "re-read: compares the pinned store with itself; carries no information" (apart from the fits the pass made) | F5 | §3.3, §7; `raw_fits_diagnostic`, `run_synthetic` |
| A7 | `--allow-dirty` registered: a real-arm run made with it is not the registered run, and its verdict line and manifest say so | F7 | §3.3, §4, §7; `NOT_REGISTERED_TEXT`, `verdict_line`, `main` |
| A8 | the per-fit diagnostic compares the `score` fields key by key, per kind | ㊲ | §3.3; `raw_fits_diagnostic`, `SCORE_FIELDS` |
| B1 | the pre-run values of the synthetic step (γ\*_P = 0.6, γ_R = 0.75, family limit = 0.75; present in revision 3.2) and `smallest_passing_auc` (two values, split by No; γ-blind; a translation anchor, not a γ limit) | — | §3.2, §3.6; `smallest_passing_auc` docstring |
| B2 | a pin is integrity, not reproducibility (gzip mtime) | ㊱ | §3.3 |
| B3 | the carriers of "present in the block"; λ's values and counts; the tie direction named | ㊴ | §3.8 |
| B4 | the γ_R input chain; `TAU` inert because lattice gaps ≫ `TAU` and rounding ≪ `TAU` | ㊵ | §3.2 |
| B5 | what the gate covers and does not cover | ㉚, ㊶ | §3.3 |
| B6 | the provenance of the reference; the manifest records the dirty paths and the `--from-raw` file with its sha256 and existence | ㉝, ㉞, ㉜ | §3.3, §7; `main` |
| B7 | V1's four reasons (mixed fits; no producer; one machine; gzip mtime) | — | §3.3 |
| C1 | column 8 is a world-level field derived from rule #2.1's row | ㉔ | §7 |
| C2 | the vocabulary of B3 in one place | — | §3.8 |
| C3 | the revision-3.1 paragraph of §7 marked "as of revision 3.1; replaced" | — | §7, §11 |
| C4 | `--out` with `--arm` refused (done in A2) | — | §7; `out_dir_refusal` |
| C5 | the column-8 differences checked to be exactly revision 3.2's rename (84 of 84 in the re-read) | F6 | §3.3; `csv_compare`, `_mech_renamed_32` |
| C6 | `check_prerun_files` reports entries neither listed nor pinned, without failing | F9 (part) | §3.3, §7; `check_prerun_files` |
| C7 | new raw records store `sign_n` | ㊲′ | §3.3; `_w_group` |
| C8 | the error ledger | chat 14:37–14:38 UTC | §12 |

*Additions of 15:16–15:26 UTC, applied on top of commit `1d6bb9e`* (Ark 15:19 "a fix whose path
never ran is indistinguishable from none", Johnny 15:19):

| item | what | source | where |
|---|---|---|---|
| 1 | F4a as two cross-probes, each moving one cut: `MECHANISM_CUT` moves only the mechanism text; `GATE_CUT` moves only the `ceiling_block` reason and the G gate clause; expected strings built from the constants; no test asserts `GATE_CUT == MECHANISM_CUT` | Ark 15:19 §2 | `test_probe_mechanism_cut_moves_only_the_mechanism_text`, `test_probe_gate_cut_moves_only_the_gate_texts` |
| 2 | item ㉗'s control: a permuted copy of the reference rows gives outcome 1 with the order recorded (`test_csv_compare_by_key` had a two-row swap; a six-row permutation is added) | Ark, Johnny 15:19 | `test_csv_compare_by_key` |
| 3 | the store record's fields declared beside the CSV column classes: compared exactly `p`, `y`, `lam`, `score`, `outside_density`; excluded by name `secs` and `reused_from_ko`; an assert that every field seen is declared | Ark 15:19 §4, Johnny 15:19 §2 | §3.3; `STORE_FIELDS_COMPARED`, `STORE_FIELDS_EXCLUDED`, `raw_fits_diagnostic` |
| 4 | `secs`, the second non-reproducible field; the population of the printed mean seconds | Ark 15:20 | §3.3, §7; `mean_seconds_population`, `print_synthetic` |
| 5 | three rules never exercised in the pre-run, in one place | Johnny 15:20 | §11 |
| 6 | `board` (z 40, z' 5) as the carrier of the layout dependence of `smallest_passing_auc`; an observation, its falsifier not run | Ark 15:22 | §3.2 |
| 7 | the γ axes named γ_z and γ_z1 (CSV `gamma_z`, `gamma_z1`); values unchanged | Johnny 15:23, Ark 15:24 | §3.6, §10 (D8) |
| 8 | the ledger in six fields, with the rules for addresses, scope and pins; entries Johnny (8), Johnny (9), Ark (15) | Ark 15:25, Johnny 15:26 | §12 |

## 11. Not verified at drafting

**Revision 3: what the synthetic runs have since measured** (details in §3.6, "What the runs
found"; the real block is still unread).

- **Closed by D11.** R reads R, Nf reads G, No reads G and W reads W, each in 5 of 5 worlds. These
  were revision 2's expectations by algebra. The cost of §7 is now measured.
- **`ceiling_block`'s λ choice on 64 cells** (an open item of revision 2): `ceiling_block` = 1.000 for rule #2.1 and every BF_r in all 45 worlds (225 fits), and every block-only fit selected λ = 1. The block-only inner folds caused no failure.
- **The λ switch is a measured property of the instrument** (§6): across all 23,850 fits that select λ, the selected λ was 1, 3 or 100, never 10 or 30. The shuffled banks' knockout fits selected λ = 100 in 21,900 of 22,275 fits. The dense grid added an intermediate state (λ = 3, partly shrunk) that yields U near γ\*.
- **U was not visited** by any world of the revision-2 run (Zcode, 08:22 UTC). The dense grid's
  answer, and with it U's name, is in §3.6.

**Revision 3.1: recorded from the reviewers' pass (Ark 09:32, Johnny 09:33, Zcode 09:34 UTC); no
new number was computed.**

- **λ is a three-position knob, a property of the instrument** (Ark's measurement). Across 23,850
  fits λ took only 1, 3 and 100 of the five registered values (§6). Ark corrected his own earlier
  description: "survives or zeroes" was too strong, since at λ = 3 the interaction survives in
  part.
- **U is the signature of the threshold** (Ark; Zcode agrees; Johnny recorded that his falsifier
  fired against his own structural reading). All 3 U readings of the pre-run table lie at γ = 0.6,
  inside the transition band [γ\*_P, γ_R) = [0.6, 0.75): 1 grid step, 0.15 in γ (pre-run values).
  A real U is read "on the detection threshold; cannot be separated" (§3.6, §4).
- **Three limits from the pre-run table** (pre-run values; the registered run recomputes them):
  γ\*_P = 0.6 and γ_R = 0.75. The family limit was not in the pre-run table, and revision 3.1
  computed nothing.
- **Mutability** (Johnny). Both files are untracked (as of revision 3.1; `8a514fa` committed
  them), and the pre-run numbers precede the final text (header). The registered run recomputes everything from a clean committed tree and must
  reproduce the pre-run `synthetic_worlds.csv` byte for byte, or it stops (§3.3, §7). *(As of
  revision 3.1; the byte-for-byte requirement is replaced by the gate of revisions 3.2 and 3.3,
  §3.3.)*

**Revision 3.2: measured, and what it leaves open.**

- **Measured by CC (2026-09-25, this machine, `tools/.venv`, one process; §3.3):** fresh
  knockout fits of all 45 worlds × 6 predictors by the revision-3.1 code equal the pinned fits
  bit for bit (270 of 270), and the revision-3.1 writer on the pinned fits reproduced the pinned
  CSV byte for byte.
- **Measured for revision 3.2 (the drafting subagent, one `--synthetic-only --from-raw` re-read
  into a scratch directory, 12 s):** outcome 1 of the new gate, every deciding column equal; column
  8 differs on 84 rows, as A5 intends, and nothing else; the per-fit diagnostic found no
  difference (trivially, since a re-read uses the pinned fits). The label test passes (8 tests).
- **Not covered:** the 99 shuffles (`|sh:`, 594 keys per world) and the 20 permuted-block
  ceilings (`|pc:`) were not refitted, so leg S, and with it γ_R, rests on the saved fits until the
  registered run; the equality is measured on one machine only; the cross-configuration self-test
  of §3.3 is a written procedure, not run by the script.
- **`TAU` (a precision on B8).** It is exactly inert in `p_P` and `p_P_rowcol`, where both AUCs
  are on 32/32 labels. In `n_ge` the shuffled block's present count can differ from 32, so there
  it is inert only up to floating-point rounding between equal fractions (§3.2).
- **The G gate** never bound in the pre-run, and the failed-fit text is tested only on injected
  reasons (§4).

**Revision 3.3: measured, and what it leaves open.**

- **Measured by CC (probes posted 15:1x UTC; §3.3, facts (c) and (d)):** a fresh refit in a
  30-process pool (581 s) equals the pinned store on every field in 2112 of 2112 fits: the `ko`
  arm of all 45 worlds (270), the 99 shuffles (1782) and the 20 permuted-block ceilings (60) of
  M0.6:0, M0.75:0 and M0.5:0. The file named as the reference pass's `from_raw` holds the same
  28,665 keys as the pinned store and differs only in 5 `secs` fields; the pinned store is a byte
  copy of the reference pass's own output; the revision-2 run's store equals the pinned store on
  every shared key. The revision-3.1 writer reproduced the pinned CSV byte for byte (13:40 UTC).
  Before revision 3.3, `--out` had no guard (P4, §7).
- **Measured for revision 3.3 (the drafting subagent):** `python -m py_compile` on the script;
  the label test, 12 tests, all pass (14 after the additions of 15:16–15:26 UTC); and one `--synthetic-only --from-raw` re-read of the
  pinned `raw_fits.json.gz` into a scratch directory (13 s; its only fits are the five refits of
  the fixed-λ path check, and N1's degree terms on the real knockout view): outcome 1; rows
  matched by key, none missing, row order equal; column 8 differs on 84 rows, all 84 exactly
  revision 3.2's rename; the per-fit diagnostic, marked as a re-read of the pinned store, found no
  difference in `p`, λ, labels or score in the 28,665 keys; the U rule counts 3 threshold U, 0
  failed fit, 0 not measured; `smallest_passing_auc` 0.666015625 in 40 worlds and 0.6728515625 in
  the 5 No worlds. The `--out` refusal was tested on a throwaway copy of the pinned
  `synthetic_worlds.csv` in a scratch folder (refused, nothing written) and with `--arm`
  (refused before any check), besides the unit test; the pinned folder still matches its
  `SHA256SUMS.txt`.
- **Three rules never exercised in the pre-run (revision 3.3, item 5).** They are tested only
  on hand-made inputs, and no synthetic world reached them: (1) **the V4 failed-fit branch** of
  U (`ceiling_block` = 1.0 in 225 of the 225 fitted rule #2.1 and BF rows); (2) **`n_u_failed`**,
  which is 0 (and `n_u_not_measured` is 0); (3) **the D14 (ii) exclusion of degenerate
  shuffles**: `n_deg` = 0 and `n_valid_shuffles` = `n_shuffles` = 99 in all 270 rows of the
  pinned `synthetic_worlds.csv` (Johnny's count, 15:20 UTC, checked on the pinned file).
- **Not in this revision (open):** **F8**, the λ gap instrument (the loss gap between the best and
  the second λ of each fit), needs the per-λ losses, which live inside pinned fitting code; it
  stays open, since it cannot be obtained without modifying pinned files. **The rest of F9**: the
  "below" bucket of `transition_band`, and `label_text` branching on a prose prefix of a reason
  (open, block C). **The `|sh:` and `|pc:` fits of the other 42 worlds** were not recomputed
  (open). **The GPU instrument** is a separate document.

**Still not verified (revisions 3 and 3.1).**

- **The limits are in M-world units.** How a γ of the synthetic outside maps onto the real bank's
  structure is not known. The limits say what strength of rank-1 polarity this instrument detects
  in worlds built on the real degree terms. They do not say how strong the real block's polarity
  is.
- **The limits rest on 5 worlds per grid point.** "Majority" is 3 of 5, so a grid point can flip
  with one world. The bracket is the resolution of the grid, not a confidence interval. **Johnny's
  binomial note (revision 3.1):** with n = 5 a limit is uncertain by about one grid step. A γ
  whose true detection probability is 0.2 or 0.4 gives "≥ 3 of 5" with probability about 0.06 or
  0.32. So the one-step band of the pre-run table is within that resolution.
- **Whether the registered run reproduces the pre-run table.** Nothing was run for revision 3.1,
  so the byte comparison of §7 has not yet been made. The script's reproduction check was tested
  only on hand-made inputs. (Revision 3.2: partly measured, above; the gate now compares the
  deciding columns.)
- **The transition band's definition** ([γ\*_P, γ_R) on the grid) is drafted by the subagent from
  the reviewers' description ("between not seen and seen"). It was not voted on by name.
  (Revision 3.2: voted yes with fixes, V2 in §10; U is read at γ\*_P, not at the band.)
- **The fixed λ = 1 diagnostic has no calibrated reading.** It decides nothing (§3.5).

**Revision 2's list, kept:**

- The cost estimate of §7 (now replaced by a measurement).
- Whether rule #2.1's fit behaves on a view with 64 fewer cells exactly as on a C6 fold (it should:
  a C6 fold also removes about 422 cells by mask). The leakage check and determinism check cover
  the parts that matter.
- The male-CNS mapping of the 16 names is accepted in review (§8), but its canonical name column
  and pair threshold are open until the builder is registered. Also unverified: that flyvis's
  CT1(M10)/CT1(Lo1) split lies outside the block, and the male CNS's sex-specific differences in
  the optic lobe.
- **`ceiling_block`'s λ choice on 64 cells.** The inner folds of `folds.csv` restricted to the
  block hold only a few cells each. A fold with no present cell or no absent cell is possible, and
  how `fit_bf` and rule #2.1 behave there was not checked. D11 shows it. (Revision 3: measured,
  above.)
- **Whether every Nf world reads G.** If the knockout interaction is fitted noise, the five
  predictors' `p_P` values are close to uniform, and all five above 0.10 in all 5 worlds is not
  assured (§3.6). Whether the M worlds avoid G at γ = 0.5 and R at γ = 1.0 is likewise an
  expectation only. (Revision 3: Nf read G in 5 of 5. The M requirement was withdrawn as wrong,
  §3.6.)
- The Strother et al. 2017 page number (candidates note).

## 12. Changelog

**Revision 1 (2026-09-24 UTC, about 20:50): first draft, CC subagent.** Built on the fixed
decisions of the review of 2026-09-24 20:22–20:39 UTC and Mike's choice of flyvis-65
(20:39 UTC). Computed for this draft: the three pre-data tables of §1.4 (names and outside-block
presence only); the field groups of the 16 types (§1.3); the range of AUC for additive scores on
the board (§2.3, random numbers only). Proposals D1–D14 open.

**Revision 2 (2026-09-24 UTC, after 20:59): reviewers' consensus applied, CC subagent.** From the
DPC Research chat, 2026-09-24: Ark 20:56, Johnny 20:58, Zcode 20:59 UTC (and, for §8, Ark 20:48,
Johnny 20:50–20:53). Nothing was run, and no bank number was added.

- **Two ceilings** (Ark, finding 1; Johnny: findings 1 and 3 are one defect). `ceiling_full` (full
  bank, in-sample on the block: is the block consistent with its surroundings) and `ceiling_block`
  (the 64 cells only: pure expressivity). The G gate is `ceiling_block ≥ 0.90`. A low
  `ceiling_full` with a high `ceiling_block` is routed to G (Johnny), labelled "G (orthogonal: block
  not implied by surroundings)" against "G (no information)". Both are printed on the verdict line.
  D9's permuted-block ceilings are `ceiling_full`, and their fall carries information (Johnny; Ark,
  finding 5). §2.4, §3.1, §3.4, §3.5, §4, §5, §7, D5, D9.
- **The board is exactly rank 1** (Ark, finding 5): `y = x_s · w_t` in ±1 form, with its three
  consequences (R realisable for a rank-1 rule, `ceiling_block` ≈ 1 in every world, permuted
  ceilings fall). §0, §2.4, §3.4, §6.
- **M worlds** (Ark, finding 2; made a run condition by Johnny): γ = 0.5 and 1.0 must read U or W,
  never G and never R; a failure stops the run. The γ breakpoint between "seen" and "not seen" is
  printed. §3.6, §6, D8.
- **No row** (Ark, finding 3): the requirement is "reads G (orthogonal)". If No reads U, the
  registration states that the design cannot tell an orthogonal board from absence. §3.6, §5, §6.
- **Degenerate shuffles** (Ark, finding 4): above 5, the verdict line names the count and its cost,
  power for leg S of R and W. §3.2, §4, D14.
- **R/W separation** (Johnny): R and W are read on both D1 candidates and must agree, else U. It is
  chosen over a margin above a fit cost and marked for review, with the reason. §4, D1.
- **N1 wording** (Ark retracted his earlier phrasing; revision 1 was right): "the N1 leg decides
  nothing", not "N1 sits at 0.5"; Ark's independent range for additive AUCs is added, and his
  confirmation of 0.0727 and AUC ≳ 0.67. §0, §2.3, §3.2.
- **Expected readings** of R, Nf, No, W and M under the new rule, derived by algebra. §3.6.
- **Votes** of Ark, Johnny and Zcode on D1–D14; D11 pending Mike. §10.
- **Male CNS arm** (Zcode 20:59, Johnny 20:50–20:53, Ark 20:48): type map accepted (R1–R6 as one
  type, CT1 with the side flip, TmY9 flagged, `flywireType` roll-ups, one canonical name column);
  the pair threshold as the builder's first open parameter, with the perfect board and 4 mirror
  cells depending on it and 64/64 inferability at every threshold tried; chunked weight reads, the
  zero-match self-test, skipped `#` headers, the two lobes as a within-animal null, the R1–R6
  asymmetry, CT1 and Am1 at n = 1 per lobe; the builder is a separate registration. §1.4, §8, §11.

**Revision 3 (2026-09-25 UTC), after the synthetic-only run of revision 2 (D11): seen → corrected.
CC subagent.** What was seen: the revision-2 run (2026-09-24 21:32–22:58 UTC, 30 worlds) met the
R, Nf, No and W requirements, 5 of 5 each. It **stopped on the M rows**: M0.5 read R 1 and G 4,
and M1.0 read R 5 of 5. The nested λ choice acted as a switch, with ties going to λ = 100, which
is pure N1 (`harness.py:727-728`). No world read U. The consensus that corrects it (Zcode 08:22,
Ark 08:24, Johnny 08:27 UTC; CC's summary 08:28; Mike supported both settlements at 08:30 UTC)
is recorded vote by vote in §10.

**Why this is not fitting to the data** (Ark's three reasons, 08:24 UTC; Zcode agreed the
change is "a correction of the instrument after its own check"):

1. **It fixes a false stop.** The M requirement "never R" would have stopped a correct reading. The
   structure in an M world is real, and an R there is a true positive. It does not make R more
   likely on the real block.
2. **It weakens G rather than strengthening R.** G goes from "no grammar found" to "not detected
   above γ\*", a narrower claim carrying its instrument. No branch condition was loosened toward R
   or W. Leg S's exclusion of degenerate shuffles changes no world, since `n_deg` = 0 everywhere.
3. **It changes no real number.** The real block has not been read, fitted or scored. The rules,
   cuts, seeds of the real arm, legs and predictors are unchanged. Only the synthetic requirement
   rows, the naming and reading of G and U, and a printed diagnostic changed.

**Changes.**

- **(a) M worlds are a power curve, no stop** (all three). An M world may read R or W, which are
  true positives. The old requirement was wrong. CC warned of it before the run (2026-09-24 21:10
  UTC), and Ark marks the class of error. The only false reading an M world could give is a false
  absence, and under the redefined G there is none. §3.6, D8.
- **(b) G redefined: "not detected above γ\*"** (Ark and Johnny: redefine the branch; Zcode and
  Johnny: print it with its instrument). γ\* is the smallest γ on the dense grid {0.5, 0.6, 0.75,
  0.85, 1.0} (5 worlds each; M0.6, M0.75 and M0.85 new, seeds 90160–90184) at which a majority is
  seen. It is printed with its bracket and the instrument (`BF_LAMBDAS`, the 1e-9 tie rule,
  `STARTS`). Nf: never R or W (stop), at least 3 of 5 G (CC 21:10, point 1; not voted on by name,
  applied under the consensus). No: G, never R or W. §0, §3.6, §4, §5, D5, D8, D10.
- **(c) Mechanism labels of G are description only** (all three). The labels statement is
  superseded. §2.4, §3.6, §4, §5.
- **(d) Degenerate shuffles are excluded from leg S**, which counts against 99 − n_deg. They are
  named on the verdict line above 5 (all three). D14 → (ii). §3.2, §4, §6.
- **The λ switch as a measured property of the instrument**, with Johnny's link to P3 (66 of 99
  banks at margin exactly 0.0). §6, §11.
- **The U rule**, written before the dense grid was run (CC's settlement of Zcode's and Johnny's
  positions; Mike 08:30). Zcode's point is recorded: U was not visited in the first run. §3.6, §4,
  §5, §6.
- **The fixed λ = 1 diagnostic** (Ark; Johnny's condition; CC's settlement). It decides nothing,
  sits beside γ\*, and is not on the verdict line. §3.5, §4, §7.
- **§7 corrected** (Zcode: yes to CC's three text fixes). `--synthetic-only` records the tree state
  and does not refuse (D11). The cost is measured. The private outputs are named. §7, D11.

**Run under revision 3** (Mike's D11 approval of 2026-09-24 21:04 UTC; synthetic only). Only the
15 new worlds and the missing fixed-λ fits were fitted. The 30 revision-2 worlds were re-read from
their saved fits. That took 44 min for the new worlds, plus seconds for re-reading and the 173
fixed-λ fits. The result: **the two-world check passes**. **γ\* = 0.6, bracket (0.5, 0.6].**
**U stays**: 3 of 25 dense-grid worlds read U, all at γ = 0.6. The dense grid also revised the
"on/off only" reading of the λ switch: at γ = 0.6 all 5 worlds selected λ = 3, a partly shrunk
state (§6). Details are in §3.6, "What the runs found". No rule was adjusted after this run.

**Revision 3.1, 2026-09-25 UTC: the reviewers' pass on revision 3. Text and code only, no run.
CC subagent.** From the DPC Research chat: Ark 09:32, Johnny 09:33, Zcode 09:34 UTC; Mike 09:34
UTC (GPU) and 09:35 UTC ("run nothing"). **Nothing was run.** No script mode ran, `--synthetic-only`
and `--from-raw` included. Nothing was fitted, and no bank was read. The only checks were
`python -m py_compile` on the script and pure unit checks on hand-made inputs. Those checks took
the new functions from the script's source without importing the module, so they read no pin,
bank or harness. The only numbers added are read from revision 3's pre-run table (γ\*_P = 0.6,
γ_R = 0.75, the transition band), and they are marked pre-run. Votes, item by item, are in §10.

- **Three limits instead of one** (Ark, Johnny, Zcode): γ\*_P, the leg-P limit (revision 3's γ\*);
  γ_R, the R level; and the family limit, the largest leg-P limit over the predictors. **G
  redefined** as "not detected at the R level above γ_R; leg P passes from γ\*_P", printed
  with all three limits, their brackets and the instrument (`BF_LAMBDAS`, the 1e-9 tie rule,
  `STARTS`). Script: `grid_limit`, `family_limit`, `detection_limits` (replacing `gamma_star`),
  `limits_text`, `label_text`, `verdict_line`. §0, §3.6, §4, §5, §6.
- **The per-γ fractions are not collapsed** (Johnny): seen/n and R/n at every γ, and each
  predictor's seen/n, beside the limits; Johnny's binomial note (script: `binomial_note`, which
  computes the tails 0.058 and 0.317). §3.6, §6, §11.
- **U is the signature of the threshold** (Ark; Zcode agrees; Johnny recorded his falsifier's
  firing as his own error): read "on the detection threshold; cannot be separated". The report
  prints the width of the transition band [γ\*_P, γ_R) in grid steps and in γ, and where each U
  world lies (script: `transition_band`). The branch condition of U is unchanged. §3.6, §4, §5,
  §6, §11.
- **λ on the verdict line** (Zcode's request; Ark and Zcode vote yes): the λ selected by each
  knockout fit, and a G reached through λ = 100 named. §4, §10.
- **λ as a three-position knob** (Ark's measurement: 1, 3 and 100 across 23,850 fits), with Ark's
  self-correction ("survives or zeroes" was too strong). §6, §11.
- **Mutability and reproduction** (Johnny; Zcode: same seeds and environment). The registered
  run recomputes everything from a clean committed tree in one manifest. It must reproduce the
  pre-run `synthetic_worlds.csv` byte for byte, or the two-world check stops it. Script:
  `worlds_csv_bytes` (the revision-3 writer, byte for byte), `check_prerun_reproduced`,
  `csv_differences`, `PRERUN_WORLDS_CSV_SHA256`. Header, §3.3, §7, §11.
- **Raw outputs for cross-checking** (Ark and Zcode, before commit): the pre-run outputs in
  `connectome-seed-data/knockout_regrow/synthetic_rev3_prerun/`, with their checksums. The
  registered run writes its private and raw outputs to
  `connectome-seed-data/knockout_regrow/<arm>_<UTC stamp>_<head>/` (script: `PRIVATE_ROOT`,
  `private_run_dir`, `write_sha256sums`, `raw_fits_real.json.gz`). Header, §7.
- **The instrument is the pinned CPU numpy harness** (Mike 09:34 UTC; Ark's `bf_als` timing). A
  GPU instrument, if ever built, is separate and validated on its own. §7.
- **The three points the drafting subagent had decided are confirmed:** No reads G; Nf needs at
  least 3 of 5 G; λ goes on the verdict line. §3.6, §4, §10.

**Revision 3.2, 2026-09-25 UTC: the reviewers' pass on revision 3.1. Text and code only; no
fitting run. CC subagent.** From the DPC Research chat, 12:06–13:13 UTC (Ark and Johnny; Zcode
did not vote), on Mike's word at 13:36 UTC. **Revision 3.2 has NOT been reviewed; no real-arm
run before its review and Mike's word.** Runs made: `python -m py_compile` on the script; the new
label test (8 tests, all pass; it imports the script, which reads the pins and imports the
harness, and fits nothing); and one `--synthetic-only --from-raw` re-read of the pinned
`raw_fits.json.gz` into a scratch directory (12 s; its only fits are the ones this mode always
makes: N1's degree terms on the real knockout view, outside-block cells only, and the five
refits of the fixed-λ path check). No real block cell was read. Votes and items,
one by one, are in §10.

- **A1, the reproduction gate** (V1: Johnny's block, Ark's changes): the deciding columns row by
  row instead of the bytes; three outcomes written before the run; the cross-configuration
  self-test; byte identity recorded; every pre-run file checked; the per-fit diagnostic. The
  measured facts are recorded (CC). Script: `csv_compare`, `check_prerun_files`,
  `check_prerun_reproduced` (replacing `csv_differences` and the byte comparison),
  `raw_fits_diagnostic`, `PRERUN_SHA256`, `PRERUN_REV2_FAMILIES`, `PRERUN_REV3_FAMILIES`,
  `WORLDS_CSV_HEADER`, `CSV_EXACT_COLUMNS`, `CSV_CONTINUOUS_COLUMNS`, `CSV_REPORTED_COLUMNS`,
  `MACHINE_CHECK_TOL`, `REPRO_FAIL_TREATMENT`. §3.3, §3.7, §7, §11.
- **A2, the U reason on the verdict line** (V4; Johnny's positive control): `label_text` takes
  the reasons; a `ceiling_block` reason gives "failed fit", never renamed. Script: `label_text`,
  `ceiling_block_reason`, `FAILED_FIT_TEXT`, `CEILING_BLOCK_REASON`, and its callers
  `verdict_line`, `run_synthetic`, `main`. Test: `test_knockout_regrow_labels.py`. §3.6, §4, §5.
- **A3:** a `--from-raw` pass is reported as a re-read, not a reproduction, and neither passes
  nor fails the gate. Script: `check_prerun_reproduced`, `run_synthetic`. §7.
- **A4:** the manifest records the BLAS, the machine and the four thread variables as found.
  Script: `machine_record`, `THREAD_VARS`, `THREAD_ENV_FOUND`, `main`. §7.
- **A5:** `CEILING_CUT` split into `GATE_CUT` and `MECHANISM_CUT` (both 0.90); the G text names
  rule #2.1's `ceiling_block`; the mechanism text names rule #2.1's `ceiling_full`. **This
  changes the text of column 8 of `synthetic_worlds.csv` on the 84 rows that carry it, so the
  fresh table is no longer byte-identical to the pinned one; column 8 is outside the deciding
  set.** Script: `mechanism_description`, `read_label`, `label_text`. §2.4, §4, §7.
- **B1–B10, reading rules (text only):** the pre-run limits, the family limit included (0.75);
  what they rest on; λ; `p_P` defines the limits; within-version determinism; `D` of N1 within
  `PARITY_TOL`; what the CSV cannot show; `TAU`; the regrown share as a ratio; the U reasons of
  the three pre-run U worlds. U is the signature of γ\*_P, not of the band (V2); the W gate is
  family-corrected, the limits are not (V3). The script prints the diagnostics as diagnostics
  (`print_bank`, `md_bank_table`) and the two V2/V3 sentences beside the limits (`md_limits`).
  §3.1, §3.2, §3.4, §3.6, §6, §7, §11.
- **C, hygiene** (Ark N1, N2; Johnny): "weak leg" → "leg P" throughout (script: `limits_text`,
  `md_limits`, `transition_band`, `detection_limits`, whose keys `weak_leg` and
  `G_at_or_above_weak_leg` became `leg_P` and `G_at_or_above_leg_P`); "untracked" marked "as of
  revision 3.1"; the provenance of the fits and of the fitting runs; the comments on
  `PRERUN_DIR` and `LIMIT_KEYS`; the `LABEL_TEXT` / `label_text` collision noted.
  `REGISTRATION_REVISION` = "3.2". Header, §3.7, §7, §10.

**Revision 3.3, 2026-09-25 UTC: the reviewers' pass on revision 3.2. Text and code only; no
fitting run. CC subagent.** From the DPC Research chat, 14:04–14:39 UTC (Ark and Johnny, both
"yes, with edits"), Zcode's votes at 15:05 UTC and CC's probes at 15:1x UTC, on the procedure of
Mike's word at 13:36 UTC. **Revision 3.3 has NOT been reviewed; no real-arm run before its
review, Zcode's vote and Mike's word.** Runs made: `python -m py_compile` on the script; the
label test (12 tests, all pass; 14 after the additions of 15:16–15:26 UTC); one `--synthetic-only --from-raw` re-read of the pinned
`raw_fits.json.gz` into a scratch directory (13 s; no new world fit, the five refits of the
fixed-λ path check, N1's degree terms); and two refusals of `--out` (a throwaway copy of the
pinned CSV in a scratch folder; `--out` with `--arm`), each of which exited before any check or
write. No real block cell was read, and nothing under the pinned pre-run folder was written.
Votes and items, one by one, are in §10.

- **A1, the reproduction gate:** rows matched by key; missing rows, value differences and row
  order kept apart; outcome 3 split into (a) and (b); the treatment's four layers and order of
  reading; the self-test's outcomes and mechanism corrected; null-input digests. Script:
  `csv_compare`, `CSV_KEY_COLUMNS`, `outcome_3_reason`, `OUTCOME_3_PART_TEXT`,
  `PRERUN_OUTCOME_TEXT`, `repro_fail_treatment` (with `REPRO_LAYERS`, `REPRO_BRANCH`,
  `REPRO_SELF_TEST`; `REPRO_FAIL_TREATMENT` is kept as the two-part text),
  `null_input_digests`, `check_prerun_reproduced`, `main`. §3.3, §7, §10.
- **A2 and C4, the reference folder protected:** `out_dir_refusal` in step 1 of `main`, before
  any write; "Recreating the reference"; the note on the order of writes; the falsifier. Test:
  `test_out_guard_refusals`. §7.
- **A3 and A4, the U texts:** `u_kind`; `u_rule` counts `n_u_threshold`, `n_u_failed` and
  `n_u_not_measured`, and renames on threshold U only; `ceiling_block_reason(None)` returns
  `CEILING_BLOCK_NOT_MEASURED`, and `label_text` prints `NOT_MEASURED_TEXT`. Tests:
  `test_ii_not_measured_is_not_a_failed_fit`, `test_u_rule_counts_threshold_u_only`; test (ii)
  no longer pins "n/a is below 0.90" as a failed fit. §2.4, §3.6, §4, §5.
- **A5:** the equality pin replaced by a probe (the test). **A6, A8, C7:** `raw_fits_diagnostic`
  compares the score fields (`SCORE_FIELDS`), counts `fitted_this_pass` and is marked under a
  re-read; new raw records store `sign_n` (`_w_group`). **A7:** `NOT_REGISTERED_TEXT` on the
  verdict line and in the manifest. §3.3, §4, §7.
- **B1–B7, reading rules (text only):** `smallest_passing_auc`; a pin is integrity; the
  vocabulary (§3.8, new); the γ_R input chain and `TAU`; the gate's coverage; the provenance of
  the reference, with `tree_dirty_paths` and `from_raw_record` in the manifest; V1's four
  reasons. §3.2, §3.3, §3.6, §3.8, §7.
- **C1–C6, hygiene:** column 8 as a world-level field; the revision-3.1 byte-for-byte paragraphs
  marked "as of revision 3.1; replaced"; the column-8 rename check; unlisted entries of the
  pre-run folder reported (`check_prerun_files`). `git()` keeps the status column of the first
  porcelain line. `REGISTRATION_REVISION` = "3.3". Header, §3.3, §7, §11.
- **C8, the error ledger** (below).
- **The reviewers' additions of 15:16–15:26 UTC** (§10, on top of `1d6bb9e`): two cross-probes
  of the cuts; a six-row permuted-copy control of the key match; the declared store fields
  (`STORE_FIELDS_COMPARED`, `STORE_FIELDS_EXCLUDED`) with an assert in `raw_fits_diagnostic`,
  which now also compares `outside_density`; `secs` and the population of the mean seconds
  (`mean_seconds_population`); the three rules never exercised; `board` as the carrier of the
  layout dependence; the γ axes named γ_z and γ_z1; the ledger in six fields. Runs: py_compile;
  the label test, 14 tests, all pass; one more `--synthetic-only --from-raw` re-read of the
  pinned store into a scratch directory (13 s): outcome 1, 84 column-8 rows all the rename,
  `outside_density` and every other declared field equal in the 28,665 keys, and the
  declared-fields assert held; the recomputed CSV is byte-identical to the first re-read
  (sha256 `32d62c71…95c1`).

**Error ledger (revision 3.3, C8; six fields since the reviewers' additions of 15:16–15:26 UTC).**
One row per wrong wording caught in the review of revision 3.2 (DPC Research chat, 14:37–14:38
UTC, with additions at 15:16–15:26 UTC). **Where the body and the ledger disagree, the ledger's
"correct" is right.** Rules of the table:

- Both addresses, where the wrong wording lived and what refuted it, are artefacts: a file and
  line (with the commit), a key, or a pinned file. A session message or a tool call is not a
  place: a wording that lived only in the chat is written "chat only", and a refutation that
  rests only on a tool run is written "tool only".
- A "no such X" refutation names its scope.
- **A refutation that rests on a pinned file carries its support status**, written "under pin":
  refuted by that artefact as long as its pin (`PRERUN_SHA256` of the script, §7) holds. A
  re-pin would reopen it.
- "Where it lived" was checked by searching this file and the script; line numbers of the form
  ":981" are of the script at `52eb381`. Pinned CSV = the pre-run `synthetic_worlds.csv`;
  pinned JSON = the pre-run `synthetic_only.json`; pinned store = the pre-run
  `raw_fits.json.gz`; all three under `PRERUN_SHA256`.
- Split rule (Ark 15:25, Johnny 15:26 UTC): a row whose wrong wording lived in an A or B line of
  the body travels with that fix; the others may follow. In revision 3.3 every row goes in the
  same commit.

| item | was | correct | where the wrong wording lived | what refuted it | caught by |
|---|---|---|---|---|---|
| Ark (1) | the world that flips under λ = 1 is 90161 | 90164 (`p_P` 0.0308 → 0.0011) | chat only | pinned CSV, seed 90164, rule #2.1: `p_P` 0.0308, `p_P_fixed_lambda1` 0.0011 (under pin) | Ark |
| Ark (2) | `D` = 0.0 in 42 N1 rows, a residue in 3 | 41 + 4 (90132 was missed) | chat only | pinned CSV, N1 rows: `D` = 0.0 in 41, residues at 90104, 90131, 90132, 90183 (under pin) | Ark |
| Ark (3) | column 8 repeated 270 times | 84 (14 G worlds × 6) | chat only | pinned CSV, column 8 non-empty in 84 rows (Nf 30, No 30, M0.5 24) (under pin) | Ark |
| Ark (4) | `smallest_passing_auc` is one number per table | two, split by the No family | chat only | pinned JSON, `worlds[*].smallest_passing_auc`: 0.666015625 in 40, 0.6728515625 in 5 (under pin) | Ark |
| Ark (5) | V3: the family limit equals γ\*_P if rule #2.1 is the weakest | the family limit is the maximum, 0.75 | chat only | script `family_limit` (:1380, the maximum over the predictors' leg-P limits); pinned CSV, M0.6: BF_2 1/5, BF_3 1/5, BF_4 0/5 seen (under pin) | Ark |
| Ark (6) | ":979" | ":981" | chat only | script :981 (the `mechanism_description` line that prints `MECHANISM_CUT`) | Ark |
| Ark (7) | ":630-632 says M1.0 enters no limit" | it names Nf and R; the conclusion holds by structure | chat only | script :229-232 (`CURVE_ANCHORS`: Nf and R enter no limit); the conclusion for M1.0 by the definition of a limit (§3.6) | Ark |
| Ark (8) | the path `rules/second_rule_v21/harness.py` | `results/genome/c6/harness.py` | chat only | no `harness.py` in `results/genome/c6/rules/second_rule_v21/` (scope: that directory, working tree at `1d6bb9e`); `results/genome/c6/harness.py` is pinned in §1.1 | Ark |
| Ark (9) | "the λ confound is on the minus side" | on the plus side; λ moves the margin, not the limit | chat only | pinned CSV: the four unseen M0.5 worlds have `p_P_fixed_lambda1` > 0.01; 90164 (M0.6) flips (under pin) | Ark |
| Ark (10) | `ceiling_block` = 1.0 in 77 rows | N1's rows are 0.5 | chat only | pinned CSV: `ceiling_block` 0.5 in the 45 N1 rows, 1.0 in the other 225 (under pin) | Ark |
| Ark (11) | two writes before the outcome test | one (`--arm` and `--synthetic-only` are exclusive) | chat only | script :2007 (a mutually exclusive group) and :2104–2108 (one write per mode) | Ark |
| Ark (12) | "with A only, the run is possible" | A and B both before the start | chat only | this file at `52eb381`, header line 40 and §10 line 1468 (the readiness rule) | Ark |
| Ark (13) | "the self-test removes both cells" | determinism within a version is not invariance to the environment | chat only; the related reading lived in this file at `52eb381`, §3.3 line 578, and in the script, `REPRO_FAIL_TREATMENT` :1238–1239; both replaced by A1 (item ㉖) | script :53–58 (`setdefault` does not override a thread variable already set, so a naive rerun is identical) | Ark |
| Ark (14) | "`TAU` is the instrument's resolution" | a tie policy; inert in the counts by the lattice | chat only | `harness.py:66` (`TAU = 1e-9`, a tie band) and script :200; the lattice argument, §3.2 | Ark |
| Ark/Johnny ㊳ | "`score["n_ne"]` = 16 in the No worlds, so 'block present 32' overstates" | `n_present` = `n_absent` = `block_present` = 32 in all 45 worlds; `n_ne` = 16 belongs to shuffled-bank (`\|sh:`) and permuted-ceiling (`\|pc:`) keys, a different bank, not to the base block | a count of `score["n_ne"]` over the pinned store (a run; no artefact of its own) | pinned `synthetic_only.json`: fields `n_present`, `n_absent`, `block_present`, and No#0's verdict line "AUC = 0.4990 (32/32)" (under pin, `PRERUN_SHA256`) | Ark (artefact), Johnny (count) |
| Ark (15) | "the limits live on a slice of a two-dimensional space" | the M families are one-dimensional in `gamma_z` by construction | chat only | script `FAMILIES` (:239–241 at `1d6bb9e`: `gamma_z1` = 0.0 in every M family); pinned CSV, `gamma_z1` = 0.0 in all M rows (under pin) | Ark |
| Johnny (1) | "10 revision-2 fits" | 5 (M0.5) | chat only | pinned CSV, M0.5: 5 worlds (under pin); §3.7 (M0.5 is a revision-2 family) | Johnny |
| Johnny (2) | "the λ confound is on the minus side" | the plus side, world 90164 | chat only | as Ark (9) (under pin) | Johnny |
| Johnny (3) | BF_4 at γ = 0.6: 1–2 of 5 seen | 0 of 5 | chat only | pinned CSV, M0.6, BF_4: `p_P <= 0.01` in 0 of 5 (under pin) | Johnny |
| Johnny (4) | "fix ① is three lines" | it needs a fourth parameter | chat only | script `label_text` (:1049), whose fourth parameter is `reasons` (the drafter's reading of "fix ①"; not confirmed) | Johnny |
| Johnny (5) | "93 %" | 631 of 637 = 99.1 % not recomputed | chat only | pinned store: 28,665 keys = 45 worlds × 637 (under pin); fact (a) of §3.3 covered 6 per world | Johnny |
| Johnny (6) | ":883" | ":880" | chat only | script :880 (`Yu = y[uniform_perms()]`) | Johnny |
| Johnny (7) | two writes before the test | one | chat only | as Ark (11) | Johnny |
| Johnny (8) | "every store record has four fields" | six: `p`, `y`, `lam`, `score`, `outside_density`, `secs`; 47 `ko1` records carry a seventh, `reused_from_ko` | chat only | pinned store: 28,618 records with the six fields, 47 with the seven (under pin) | Johnny |
| Johnny (9) | "γ1 is not named in the registration" | it is named three times under other names, and the CSV column appears once | chat only | this file at `1d6bb9e`: line 841 ("γ1 = 2.5", "γ2 = 1.5"), line 1062 ("W (1.5 + 2.5)"), line 1647 ("W 2.5/1.5"); and line 656, the literal `gamma_z1` as a column of the gate (scope of the original search: the literal `gamma_z1`) | Johnny |
| CC (1) | "the reference is stale" (a GPU subagent's claim, not in the registration) | the reference reproduces bit for bit; the claim came from a wrong key and cell order | chat only | tool only (CC's probe P1, recorded in §3.3, fact (c)) | CC |
| CC (3) | "the GPU agrees with the live CPU to 3e-16" | 175 of 180; five BF_1 fits differ by 1.4e-9 to 3.8e-8 | chat only | `results/genome/c6/gpu_instrument/README.md` (untracked; it cites `run3.log`) | CC |

Johnny numbers his γ1 entry as his eighth in the chat, and the store-fields entry is also given
as his; the drafter did not have the chat and numbered the two sequentially, (8) and (9). CC's
entry (2) of the first list was withdrawn by CC, who could not confirm writing it; entries (1)
and (3) keep their numbers.
