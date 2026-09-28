# Blind review: knock out and regrow, block B on flyvis-65 (registered run of 2026-09-28)

**Written:** 2026-09-28 18:57 UTC (2026-09-29 01:57 local, +07:00), by an external blind reviewer: a
fresh Claude Code session (model `claude-fable-5-1`) that was given the review brief and nothing
else about this run. **Not committed.** The review was read-only: no tracked file and no file of
the run was changed, the registered script was not rerun, and no fit was made (section 0.4 lists
the side effects).

**Conclusion: the verdict follows.** The label U, in its failed-fit form and with the registered
text, is what B §4 and A §4 give for the run's stored values, and every number the run printed is
the number its outputs hold; on block B that text is read "a failed fit or a rank limit, not
separated" (B §4), and nothing about the block is concluded from it (A §5).

**Names used below.** "B" is block B's registration,
`docs/plans/2026-09-25-knockout-regrow-block-b-registration.md` (revision 1.7.3). "A" is block A's,
`docs/plans/2026-09-24-knockout-regrow-registration.md` (revision 3.4.1 with Amendment 1). "B:922"
means line 922 of B. "The script" is `results/genome/c6/checks/knockout_regrow_block_b.py`. "The
committed folder" is `results/genome/c6/checks/knockout_regrow_block_b/`. "The private folder" is
`connectome-seed-data/knockout_regrow/flyvis65_blockB_20260928T143258Z_7a10d88ec95e/`. "The
reference" is
`connectome-seed-data/knockout_regrow/synthetic_blockB_prerun_20260927T211052Z_5f9cc51b9a24/`. "The
console copy" is
`connectome-seed-data/knockout_regrow/flyvis65_blockB_registered_20260928T143257Z.stdout.log`.
`summary.json` and `RESULT.md` are the committed folder's; `verdict.json`, `synthetic_only.json`,
`stdout.log` and the two `raw_fits` files are the private folder's unless the reference is named.
Every time is UTC; file times were read in local time (+07:00) and converted.

## Findings in short

1. **The label is U, and it is U by one conjunct.** Neither D1 reading gives R or W. The first two
   conjuncts of the G row hold. The third, the primary's `ceiling_block >= 0.90`, fails at 0.7744
   (309 of 399 pairs). (A.3, A.4)
2. **The gate is read on the primary alone, as registered.** `ceiling_block` is below 0.90 in 2 of
   the 6 rows (rule #2.1 and N1), that is, in 1 of the 5 fitted predictors. BF_1 has 0.9649, and
   BF_2 to BF_4 have 1.0. No sentence in the sections read gives these values a part in the label.
   (A.5)
3. **"Failed fit" is the registered name of the branch. The registration does not make it a finding
   about the cause.** The justification inside the quoted A row is block A's. What B supports is
   the reading "a failed fit or a rank limit, not separated", with A §5's "nothing about the block
   is concluded". The run prints that reading beside the verdict, not on it, so a citation of the
   verdict line alone drops it. (A.6, A.7, D.2)
4. **What the run holds about that fit** (it decides nothing): the primary's block-only fit
   selected λ = 100, and its stored prediction on the 40 cells is an additive score with no
   interaction left. So the gate variable did not measure a rank-1 interaction on block B. In the
   45 synthetic worlds, of the run and of the reference, no row of rule #2.1 or BF_1 to BF_4 had a
   `ceiling_block` below 1.0, and no block-only fit selected a λ other than 1: the branch was met
   for the first time on the real block. A reading that used these facts to choose between "failed
   fit" and "rank limit" would be written after the data. (A.8)
5. **Every number recomputed from the raw fits equals the stored one**, bit for bit, by code that
   imports nothing from the script. (B)
6. **Every printed number equals the stored one.** The four committed files and the private
   `SYNTHETIC.md` are reproduced byte for byte from the stored JSON by the script's own writers. (C)
7. **The gates passed in the registered order, and the reproduction gate passed with outcome 1.**
   The run's synthetic fits equal the reference's in all 28,665 records. The three checksum lists
   verify. (E)
8. **One caveat on the committed checksum list.** Two of its four entries are sums of bytes with
   CRLF line ends, and git holds these two files with LF. A checkout that does not convert line ends
   will not verify them. (E.7)
9. **Three smaller remarks.** The additive-channel note is printed under its registered condition
   (any U), but the mechanism it names did not occur in this run (D.4). `summary.json` holds two
   run times under one name (C.5). The subject of commit `ce48577` cites the label without its
   reading (D.2).

## 0. Blindness declaration, and what was read

### 0.1 Opened

"By eye" means read line by line. "By script" means loaded and compared by a scratch script, without
reading the content line by line.

| # | file | part | how |
|---|---|---|---|
| 1 | `GLOSSARY.md` | lines 1–201 (all) | by eye |
| 2 | B | lines 173–1228 (§0 to §8) | by eye |
| 3 | A | lines 173–1773 (§0 to §9), 1965–2092 (§11), 2497–2540 (§13, Amendment 1) | by eye |
| 4 | the script | lines 1–3719 (all), at HEAD | by eye; imported read-only by four scratch scripts |
| 5 | `results/genome/c6/rules/second_rule_v21/fit.py` | lines 77–151; the lines of its constants and function heads (a search) | by eye |
| 6 | `results/genome/bank/offsets.csv` | its comment line, header and first row by eye; all 2,378 rows by script | both |
| 7 | `RESULT.md` | lines 1–279 by eye; all 971 lines by script | both |
| 8 | `summary.json`, `per_shuffle.csv`, committed `synthetic_worlds.csv` | the keys and columns named in A to E | by script |
| 9 | the committed folder's `SHA256SUMS.txt` | all | by eye |
| 10 | `verdict.json`, `REAL_ARM_STARTED.json`, the private folder's `SHA256SUMS.txt` | all | by eye |
| 11 | `raw_fits_real.json.gz`, `raw_fits.json.gz`, `synthetic_only.json`, private `synthetic_worlds.csv` | all records | by script |
| 12 | `SYNTHETIC.md` (private) | compared with a regenerated copy; hashed | by script only |
| 13 | `stdout.log` (private) | lines 1464–1532 by eye; the lines that match a list of stage markers, by search (E.1); all 1,532 lines by `diff` | both |
| 14 | the console copy | lines 1–16 by eye; all 1,532 lines by `diff` | both |
| 15 | the reference | `SHA256SUMS.txt` by eye; `synthetic_only.json`, `raw_fits.json.gz`, `synthetic_worlds.csv` by script; `SYNTHETIC.md` and `stdout.log` hashed only | both |
| 16 | git | `git log -4` (four commit subjects); `git show --stat ce48577`; `git diff --stat 7a10d88 ce48577`; `git diff 5f9cc51 7a10d88` on the script (its changed lines); `git diff --stat 5f9cc51 7a10d88`; `git ls-files --eol`; `git status`; LF hashes of blobs | commands |
| 17 | the Orbit code graph | its manifest; the definitions of the script; the callers of 45 of its functions | queries |

The brief's statement about the commits was checked: HEAD is `ce48577ceb9dcb9463e1e5d3adbdd56ca283a67d`,
its parent is `7a10d88ec95e65b809e629b3398ceaa193e6a2f8`, and `git diff --stat 7a10d88 ce48577`
lists five files, all in the committed folder. The LF sha256 of the script is `e650e47e…bb887b`, of
B `bd290d26…83a61f` and of A `fc415056…96dbec`, each the same at `7a10d88`, at `ce48577` and in the
working tree.

### 0.2 Not opened

Nothing under `chat/`, `docs/briefs/` or `docs/retrospectives/`; not `backlog.md`,
`backlog_closed.md` or `ROADMAP.md`; no file of `docs/notes/`, and no file name of that folder was
shown to me (one command counted the names equal to this report's name, and printed 0); B lines
1–172 and 1229–1962; A lines 1–172, 1774–1964 and 2093–2496. Searches of the two registrations
were made by a script that prints matches inside the allowed line ranges only (`grep_allowed.py`).

### 0.3 Unintended exposure

1. **The verdict and the reviewers' votes, from commit subjects.** The session's starting context
   carried the last five commit subjects. One is "Block B on flyvis-65: registered run outputs
   (verdict U, failed fit: ceiling_block 0.7744 < 0.90)". Four say that revisions 1.7 to 1.7.3 of B
   were answered "yes" by three reviewers (Johnny, Ark, Zcode), with the times. The brief gave the
   verdict too. No commit subject says what anyone expected of the run.
2. **The operator's assistant memory.** Its index (19 one-line notes on how to work in this
   repository) was loaded into the session automatically. I opened two notes, on delegating work and
   on language. None of the 19 lines states an expectation about block B.
3. **Headings of forbidden sections.** A search for headings of levels 1 and 2 in B and in A showed
   the titles of B §9, §10, §11 and of A §10, §12. No line of their text was shown.
4. **Counts of matches outside the allowed ranges.** `grep_allowed.py` prints how many matches lie
   outside the ranges, as numbers only (for example "failed fit": 3 in B, 8 in A).
5. **Names of files, not their content.** A listing of the data folder for names that hold "lockB"
   showed `blockB_reread_diagnostic_20260928T072433Z_62228ad0f3e6.console.log`, which I did not open.
   `git status --ignored` showed the names of git-ignored entries, among them `chat/` and
   `backlog.html`.
6. **What the allowed sections themselves carry.** B §0 to §8 and A §0 to §9, §11 name reviewers,
   times and votes on single items, state block A's verdict G and its `ceiling_full` = 0.8442
   (B:292), and say that the male CNS arm was run. This is reading the brief allows; it is listed so
   that the reader can weigh it.
7. **The second reader** (A.9) was a subagent of this session. Its working files lay in the same
   scratch folder as mine, where two of my JSON dumps hold the printed label. Its report declares no
   reading of them. I did not read its transcript.

### 0.4 Instruments and side effects

- **Python:** `tools/.venv` (Python 3.10.20, numpy 2.2.6), every call with `PYTHONUTF8=1`.
- **Scratch scripts:** 18 of mine and 1 of the second reader, in the session's scratch folder,
  outside the repository (appendix). Four of mine import the script read-only. `main()` was never
  called.
- **The citations of this report were checked by a script:** for 170 cited places (lines of A, B,
  the script, `fit.py`, `RESULT.md` and `stdout.log`), the quoted words occur inside the cited lines,
  170 of 170 (`verify_citations.py`).
- **Regeneration into scratch:** `regenerate_outputs.py` points the script's output folder (`OUT`)
  at the scratch folder before it calls `write_committed`. After it ran, `git status` was clean and
  the sha256 of the committed `RESULT.md` and `summary.json` were unchanged.
- **No byte-code cache was written into the repository:** no `.pyc` under `results/genome/c6/` has a
  modification time inside the review's window. The cache of the script is dated 2026-09-28
  07:41:10, before the run.
- **A hook of the session** runs after every shell command and reports re-indexing the code graph.
  During the review the git-ignored file `atlas.html` in the repository root changed (modification
  time 2026-09-28 18:44:40 at the time of the check). No command of mine wrote it, and it is not a
  file of the run.
- **Orbit:** the manifest names this repository at commit `ce48577…`, which is HEAD, so no re-index
  was asked for. Callers were read from the graph and confirmed by grep (appendix).

## A. The label

### A.1 The values used, and where they sit

All keys are of `summary.json` (sha256 `a43e0319…92f520`) unless a file is named. Floats are as
stored. Fractions in brackets are my exact recomputation (section B).

**The block.**

| value | stored | key |
|---|---|---|
| present and absent cells | 19 and 21 of 40 | `real.block_present`; `real.rows.rule.n_present`, `.n_absent`; `checks.3_block_print.present`, `.absent` |
| the six strata | 2 of 4, 0 of 4, 3 of 4, 3 of 4, 7 of 12, 4 of 12 | `checks.3_block_print.strata` |
| `smallest_passing_auc` | 0.7142857142857143 (285/399) | `real.smallest_passing_auc` |
| shuffles with no AUC on the block | 0 of 99 | `real.n_deg` |

**The six rows** (`real.rows.<key>`, fields `auc`, `n_ge`, `n_valid_shuffles`, `leg_S_passes`,
`p_P`, `ceiling_full`, `ceiling_block`, `lambda_ko`, `lambda_full`, `lambda_block`).

| row (key) | AUC | `n_ge` of `n_valid` | leg S | `p_P` | `ceiling_full` | `ceiling_block` | λ ko / full / block |
|---|---|---|---|---|---|---|---|
| rule #2.1 (`rule`), the primary | 0.506265664160401 (202/399) | 68 of 99 | fails | 0.4795 | 0.631578947368421 | 0.7744360902255639 (309/399) | 1 / 1 / 100 |
| BF_1 (`BF:1`) | 0.5238095238095238 (209/399) | 1 of 99 | fails | 0.4040 | 0.6265664160401002 | 0.9649122807017544 (385/399) | 1 / 1 / 1 |
| BF_2 (`BF:2`) | 0.5588972431077694 (223/399) | 0 of 99 | passes | 0.2704 | 0.656641604010025 | 1.0 | 1 / 3 / 1 |
| BF_3 (`BF:3`) | 0.5588972431077694 (223/399) | 0 of 99 | passes | 0.2698 | 0.7518796992481203 | 1.0 | 3 / 3 / 1 |
| BF_4 (`BF:4`) | 0.5664160401002506 (226/399) | 0 of 99 | passes | 0.2442 | 0.7969924812030075 | 1.0 | 3 / 3 / 1 |
| N1 (`N1`) | 0.5225563909774437 (208.5/399) | 99 of 99 | fails | 0.4086 | 0.6353383458646616 | 0.7882205513784462 (314.5/399) | none |

**The synthetic step** (`synthetic_only.json`, sha256 `13ebb423…6cf596`; `summary.json` holds the
same object under `synthetic`, section C.4).

| value | stored | key |
|---|---|---|
| two-world check | passed `true`, stop `false`, No contingency `false` | `two_world_check.passed`, `.stop`, `.no_contingency` |
| γ\*_P, the leg-P limit | 0.75, bracket (0.6, 0.75] | `limits.leg_P.gamma`, `.bracket_text` |
| γ_R | 0.75, bracket (0.6, 0.75] | `limits.R.gamma`, `.bracket_text` |
| family limit | 0.75, set by all five predictors | `limits.family.gamma`, `.by` |
| transition band | empty, 0 grid steps | `limits.band.text` |
| seen by rule #2.1, per γ | γ 0 (Nf): 0 of 5; 0.5: 1 of 5; 0.6: 1 of 5; 0.75: 4 of 5; 0.85: 5 of 5; 1.0: 5 of 5; 2.0 (R): 5 of 5 | `limits.rows[*].seen`, `.n` |
| read R, per γ | the same seven counts: 0, 1, 1, 4, 5, 5, 5 of 5 | `limits.rows[*].R` |
| U rule | 4 threshold U of 25 dense-grid worlds (2 of 5 at γ 0.5, 2 of 5 at γ 0.6); not renamed | `u_rule.n_u_threshold`, `.dense_grid_worlds`, `.frequency_by_family`, `.renamed` |

**The printed label** (`verdict.json`, sha256 `fa5aaf48…97c950`): `label` = "U"; `label_text` =
"U: failed fit: rule #2.1 cannot hold the block even when trained on it alone".

No limit enters a condition of this label. The limits are printed with a G and with a threshold U
(A:1327, A:1328, A:1330–1334). They are listed here because the brief asks for them, and because
the two-world check must pass before the real arm runs (A:1158).

### A.2 Is the block readable

Yes.

- `real.smallest_passing_auc` is 0.7142857142857143, not `None`. B's condition is the object
  "`smallest_passing_auc is None`" (B:575–578).
- It lies on the grid k / (n_p · n_a) of the block's own counts: 19 × 21 = 399, and the stored value
  times 399 is 285.0. My recomputation gives k = 285: the tie-free prediction has `p_P` = 0.0103 at
  284/399 and 0.0094 at 285/399 (`recompute_independent.py`).
- n_p equals check 3's present count: 19 in `real.rows.rule.n_present`, in `real.block_present` and
  in `checks.3_block_print.present`.
- Check 3's strata counts add up to it: 2 + 0 + 3 + 3 + 7 + 4 = 19, of 4 + 4 + 4 + 4 + 12 + 12 = 40.
- The same 19 cells are in the bank file: read from `results/genome/bank/offsets.csv` without the
  harness (a pair is present when it has a row that is not `dropped`), the block has 19 present
  cells, the same six strata counts, and the same 40 labels as the store (`bank_checks.py`). The
  bank has 604 present pairs, 585 of them outside the block; `checks.4_pre_data_tables.training_present`
  is 585.

### A.3 The branches, in the registered order

**Step 0, B's "not readable" U.** "on the real block, `smallest_passing_auc is None` … reads a U of
its own kind, 'not readable', which takes precedence over every other branch" (B:575–577). The value
is not `None` (A.2). **It does not fire.**

**Step 1, R.** "the primary passes leg S (`n_ge = 0` of the `99 − n_deg` shuffles with an AUC, §3.2)
**and** leg P (`p_P <= 0.01`), **on both D1 candidates**" (A:1325).

- With rule #2.1 as the primary: `n_ge` = 68 of 99, leg S fails; `p_P` = 0.4795, leg P fails.
- With BF_1 as the primary: `n_ge` = 1 of 99, leg S fails; `p_P` = 0.4040, leg P fails.

**Not R** in either reading.

**Step 2, W.** "not R, and **some BF_r** (r = 1..4) passes leg S (`n_ge = 0`) and leg P at
`p_P <= 0.0125`" (A:1326); "In both readings the W row ranges over BF_1 to BF_4" (A:1304).

- BF_1: leg S fails (`n_ge` = 1).
- BF_2, BF_3, BF_4: leg S passes (`n_ge` = 0 of 99), leg P fails (`p_P` = 0.2704, 0.2698, 0.2442).

No rank passes both legs. **Not W** in either reading.

**The D1 rule.** Both readings give neither letter, so "If neither reading gives R or W, the G and U
rows are read on rule #2.1" (A:1307–1308). The stored readings agree: `real.reading_A_rule.letter`
and `real.reading_B_BF1.letter` are both "-".

**Step 3, G.** Not G (A.4).

**Step 4, U.** "anything else" (A:1328). Of the reasons that row names:

| reason in A:1328 | applies | values |
|---|---|---|
| "The legs disagree" | no | for the primary both legs fail |
| "the regrowth sits between `p_P` 0.01 and 0.10" | no | the smallest `p_P` of the five is 0.2442 |
| "`ceiling_block` is below 0.90" | **yes** | 0.7744360902255639 |
| "the two D1 candidates disagree on R/W" | no | both read "-" |

The stored list has this one reason: `real.U_reasons` = ["rule #2.1's ceiling_block = 0.7744 is below
0.90: the rule cannot hold the block even when trained on it alone"].

**The text of the label.** "a U whose reasons include `ceiling_block` below 0.90 is a failed fit,
whatever else is listed. Its label text is 'failed fit: rule #2.1 cannot hold the block even when
trained on it alone', and the U rule's rename never applies to it" (A:1328). B keeps it: "the label
text … is kept verbatim" (B:922–923).

**So the label is U, printed as a failed fit. It equals the printed label.**

The script reads the same way. `read_label` (script lines 1599–1642) takes the two readings from
`reading_on` (1542–1550), tests the gate on `rows["rule"]` only (line 1620), and puts the
not-readable reason first when `readable` is false (1636–1638). `u_kind` (1582–1596) gives
"failed_fit" when a reason starts with "rule #2.1's ceiling_block = ", and `label_text` (1666–1696)
prints `FAILED_FIT_TEXT` (line 369) for it. The cuts are `GATE_CUT` = 0.90, `P_R` = 0.01, `P_W` =
0.0125 and `P_G` = 0.10 (lines 273–277). The script's readers, applied by me to the stored fits,
give the stored label and text (B.2).

### A.4 The G row, conjunct by conjunct

The row is A:1327: "not R, not W; the primary **and every BF_r** have `p_P > 0.10`; and the
primary's **`ceiling_block` >= 0.90**".

| conjunct | read on | values | holds |
|---|---|---|---|
| not R, not W | both D1 readings | A.3 | **yes** |
| `p_P > 0.10` | rule #2.1 and BF_1 to BF_4 | 0.4795, 0.4040, 0.2704, 0.2698, 0.2442 | **yes** |
| `ceiling_block >= 0.90` | rule #2.1 alone | 0.7744360902255639; 309 of 399 pairs in half-pair units, where the cut needs 359.1 | **no** |

The label is U and not G because of the third conjunct only.

### A.5 Primary or family

**The registered text reads the gate from the primary, rule #2.1, alone.**

- The G row says "the primary's `ceiling_block`" (A:1327), and the same row says "the primary and
  every BF_r" where it means the family.
- "the G label names its gate variable, rule #2.1's `ceiling_block`" (A:458–459).
- "If neither reading gives R or W, the G and U rows are read on rule #2.1" (A:1307–1308).
- The label text names rule #2.1 (A:1328), and B names the rule when it states the alternative: "a
  `ceiling_block` below 0.90 can be a rank limit of rule #2.1" (B:534–535).

So the printed text, "rule #2.1 cannot hold the block", is about the primary, and **the printed
verdict follows the text as registered.**

**All six rows** (`real.rows.<key>.ceiling_block`, `.lambda_block`; the same values are in the
console block "== flyvis-65, the real block B (section 3.5) ==", `stdout.log` lines 1497–1503, and
in `RESULT.md` lines 31–36).

| row | `ceiling_block` | pairs of 399, in half-pair units | below 0.90 | λ of the block-only fit |
|---|---|---|---|---|
| rule #2.1 | 0.7744360902255639 | 309 | **yes** | 100 |
| BF_1 | 0.9649122807017544 | 385 | no | 1 |
| BF_2 | 1.0 | 399 | no | 1 |
| BF_3 | 1.0 | 399 | no | 1 |
| BF_4 | 1.0 | 399 | no | 1 |
| N1 | 0.7882205513784462 | 314.5 | **yes** | none (N1 has no λ) |

`ceiling_block` is below 0.90 in **2 of 6 rows**. Among the five fitted predictors (rule #2.1 and
BF_1 to BF_4) it is below 0.90 in **1 of 5**, the primary. The block-only predictions of BF_2, BF_3
and BF_4 agree within 8.7e-8 in `p`, so their three values of 1.0 are one solution found three
times (`bf_same.py`).

**Does anything in the sections read decide how the other values bear on the label?** No. The
sentences that speak of them print them or deny them a part:

- "Both are computed for the primary and for each BF_r" (A:453).
- "What decides. The label. … the two ceilings (beyond their roles above) … every BF_r row, the N1
  row … are printed beside it … and decide nothing" (A:1368–1373).
- "The λ values decide nothing. The label is set by §4's conditions only" (A:1352–1353).
- N1 "enters no branch" (B:526–527).

Searched: B lines 173–1228 and A lines 173–1773, 1965–2092, 2497–2540, for "rank limit", "failed
fit", "lambda_block", "block-only", "block only", "trained on it alone", "only on the 64" and "on the
40 cells alone" (`grep_allowed.py`), and read in full. No rule was found that uses BF_r's
`ceiling_block` or any `lambda_block`.

Had the gate been read on BF_1, the label would be G: 0.9649 is above the cut, and the other
conjuncts hold. The registration excludes that reading, so this is a remark on how narrowly the
label is set, not a second label.

### A.6 How this U is read, and how the run reads it

**What the registrations say.**

- "A U whose reasons include `ceiling_block` below 0.90 is a failed fit …: the rule could not hold
  the block even when trained on it alone, so nothing about the block is concluded, and the fit, not
  the block, returns to review. The U rule never renames it" (A:1382). B §5: "A §5 applies, with
  'the block' meaning block B" (B:933).
- "On block B it is read as 'a failed fit or a rank limit, not separated', since the real block is
  not known to be rank 1" (B:923–925). The same in B:199–203, B:531–535 and B:951.
- "the report prints N1's own `p_P` beside any U, and the outcome note names the additive channel as
  a second possible source of U on this block" (B:928–929).
- It is not G: below the cut "a regrowth failure could be a failure to fit, so it is not read as G"
  (A:1358–1360).

**What the run prints.** The four conditional lines are in `verdict.json` (`conditional_lines`), in
`stdout.log` lines 1523–1526 and in `RESULT.md` lines 17, 19, 21 and 23:

1. the line that names block A's literals (D.3);
2. "The failed fit is on block B read as: a failed fit or a rank limit, not separated (the real
   block is not known to be rank 1; B section 4, D9).";
3. the additive-channel note (D.4);
4. "N1's own p_P beside this U (decides nothing; B section 3.5): 0.4086".

**So the U is read as B §4 and B §5 say,** with the two readings B adds. One sentence of the
registration has no carrier of its own in the run's outputs: A §5's "nothing about the block is
concluded, and the fit, not the block, returns to review" (D.5).

### A.7 Does the printed label say more than block B's registration allows

**The label string does not. A reading of it as a finding would.**

- The string is registered for block B word for word, as the name of the branch and of the
  measurement: "it states the measurement" (B:923). The measurement is that the primary's
  `ceiling_block` is 0.7744, below 0.90.
- The argument that makes "failed fit" a cause is block A's: "by §2.4 this is a failure of the fit,
  since the block is rank 1" (A:1328). B does not accept it for block B. It lists "The board is
  exactly rank 1" among the statements that do not transfer (B:185–187, B:199–203), it says that A's
  consequences "are **not known** for the real block B" (B:531–534), and it lists the sentence among
  block A's literals (B:917–921).
- So "the verdict follows" means this: the letter U follows, its kind follows (a U whose reasons
  include the primary's `ceiling_block` below the gate), and its registered text follows. It does
  not mean that the run found the fit, and not the rule's form, to be the cause.
- **What B's registration supports is the reading "a failed fit or a rank limit, not separated".**
  The label as printed is supported as a text, and only together with that reading.

### A.8 What the run holds about the fit (none of it decides anything)

Under A §4 these facts decide nothing (A:1368–1373, A:1352–1353), and no sentence in the sections
read lets them separate a failed fit from a rank limit. A reading that did so now would be a
reading written after the data. They are listed because A §5 sends "the fit, not the block" to
review, and this is what the run holds about that fit.

1. **The primary's block-only fit selected λ = 100.** `real.rows.rule.lambda_block` = 100.0;
   `RESULT.md` line 31, "1.0 / 1.0 / 100.0"; `stdout.log` line 1498; `raw_fits_real.json.gz`, record
   `real||block||rule`, field `lam`. The four BF block-only fits selected λ = 1.
2. **Its stored prediction on the 40 cells is an additive score.** Write the logits of `p` as a
   5 × 8 table and take away the row means and the column means. What is left, the part that no row
   effect plus column effect can carry, has a largest absolute value of 5.0e-16 for rule #2.1. For
   N1, which is additive by construction, it is 2.9e-16; for BF_1 it is 2.09, and for BF_2 to BF_4
   1.81 (`interaction_exact.py`, records `real||block||<key>`, field `p`). So 0.7744 is the AUC of
   an additive score. The rank-1 term `u_s v_t` adds nothing to it.
3. **It is not N1's prediction.** The two differ by at most 0.040 in `p`, and their logits differ by
   an additive table. Rule #2.1 keeps its field term at every λ: `W` has its own fixed penalty,
   `MU = 1` (`second_rule_v21/fit.py` lines 56 and 97–112), and on block B `W[G(s), G(t)]` is a
   function of the target alone (B:339–346). A's vocabulary line, "**100** = `LAMBDA_MAX`: the
   interaction is shrunk to zero, and the prediction is N1's" (A:1287–1288), holds for BF_1 in this
   run and not for rule #2.1. On the 99 shuffled banks BF_1 selected λ = 100 on 97, and its margin
   over N1 is exactly 0 on all 97 of them. Rule #2.1 selected λ = 100 on 97, and its margin is
   exactly 0 on 5 of those 97 (`per_shuffle.csv`, columns `lam_rule`, `M_rule`, `lam_BF:1`,
   `M_BF:1`; `final_checks.py`).
4. **The gate variable therefore did not measure a rank-1 interaction on block B.** The run measured
   one once, with BF_1: trained on the block alone at λ = 1 it orders 385 of 399 pairs, 0.9649. BF_1
   is another learner than rule #2.1, so this is BF_1's value and not the rule's.
5. **The block is not rank 1 in the sense of A §2.4.** A writes block A's board as an outer product
   `y_st = x_s · w_t` of two ±1 vectors (A:416–421). The ±1 table of block B's 40 labels has five
   non-zero singular values (4.64, 3.33, 2.00, 1.46, 1.12) and is not such a product
   (`bank_checks.py`, from `offsets.csv`). Its rows hold 2, 6, 4, 4 and 3 present cells (L1 to L5),
   its columns 4, 3, 2, 3, 1, 2, 2 and 2 (Mi1, Tm3, Mi4, Mi9, Tm1, Tm2, Tm4, Tm9). B wrote before
   the data that the block "is not known to be rank 1". The run printed the counts, not the pattern;
   the pattern is in the bank, and it is not rank 1.
6. **No synthetic world met this branch.** In the run's 45 worlds and in the reference's,
   `ceiling_block` is 1.0 in all 225 rows of rule #2.1 and BF_1 to BF_4 (`synthetic_worlds.csv`,
   column `ceiling_block`), and all 225 block-only fits selected λ = 1 (`raw_fits.json.gz`, records
   `world:<family>:<j>||block||<key>`, field `lam`). `u_rule.n_u_failed` is 0. A says the same of
   its own pre-run (A:1328, A:2039–2044). The two-world check shows that the reading rule can read
   R, W, G and a threshold U. It does not show what a `ceiling_block` below the gate looks like in a
   world whose answer is known.
7. **The inner folds that choose λ for a block-only fit are small.** The 40 cells fall into the ten
   folds of `folds.csv` as 4, 4, 2, 4, 5, 3, 2, 8, 1 and 7 cells. One fold holds a single cell, a
   present one, so it has no absent cell (`block_only_fits.py`, `harness.inner_folds` on the
   block-only view). A named this as not verified (A:2082–2085) and then measured it on block A's
   worlds only (A:1972). Why λ = 100 was selected is not in the outputs (last section, item 3).

### A.9 A second derivation

After my own derivation I gave the task to a second reader: a subagent of this session on another
model (the agent tool's `opus` setting). It had the same blindness list. It was also forbidden to
read the script, `RESULT.md`, any log, `verdict.json` and the keys of `summary.json` that hold the
printed answer, and it was not told my result.

**Its result equals mine in every step:** not readable, no; R, no on both candidates; W, no; G fails
on "the primary's `ceiling_block` >= 0.90" alone, read on rule #2.1; U as a failed fit, with the
same text and the same lines of A and B; 2 of 6 rows below 0.90; no sentence that gives the other
rows or any `lambda_block` a part. It named five points that it found open in the text. None changes
the label.

1. "The legs disagree" names no predictor; read on the family it would add a reason, since BF_2 to
   BF_4 pass leg S and fail leg P. (My reading: A:1298 sets the primary as the default.)
2. A gate read on BF_1 would give G (A.5).
3. The D8 note prints although its mechanism is not this U's reason (D.4).
4. λ = 100 matches A's own example of a failed fit (A:430–431), and the text gives it no part. It
   could not explain why 0.7744 is not N1's 0.7882. A.8 item 3 explains it.
5. A:1442's "nearly automatic" gate is set aside by B:199–203 and B:951.

**How far it counts.** The second reader declared that its starting context held the subject of
commit `ce48577`, with the verdict in it. It was not blind to the printed label, as I was not. It
confirms that the registered text leads to this label. It is not an independent guess of the
outcome.

## B. Recomputation from the raw fits

**Input.** `raw_fits_real.json.gz` (sha256 `2461d921…e398c6`), 637 records: 18 base fits (6
predictors × the masks `ko`, `full`, `block`), 5 fixed-λ fits, 20 permuted-block ceilings and 594
fits on the 99 shuffled banks. A record holds `p` and `y` on the 40 cells, `lam`, `score`,
`outside_density` and `secs`.

### B.1 By own code

`recompute_independent.py` imports nothing from the script.

- **AUC:** the count of (present, absent) pairs with the present cell ranked higher, ties as one
  half, in exact fractions.
- **Leg S:** for each of the 99 shuffled banks, M = AUC(predictor) − AUC(N1) on that bank's own
  block labels; `n_ge` counts the shuffles with M >= M_real. The count with `TAU` = 1e-9 and the
  count in exact fractions are equal for all six rows.
- **Leg P:** `default_rng(91000)`, 9,999 × `permutation(40)` in order, labels `y[perm]` (B:565–566);
  the AUC of the fixed prediction against each, by a matrix of pair comparisons, which is another
  route than the script's rank sums. The sha256 of my permutation matrix is `1e8b3561…b9ec00`, the
  value in `manifest.null_input_digests.uniform_perms.sha256`.
- **`p_S`** = (1 + `n_ge`) / (1 + 99 − `n_deg`); **`p_P`** = (1 + count) / 10,000.

| row | AUC | M_real | `n_ge` of 99 | `p_S` | permutations with AUC >= the real one | `p_P` | `ceiling_full` | `ceiling_block` |
|---|---|---|---|---|---|---|---|---|
| rule #2.1 | 202/399 | −13/798 | 68 | 0.69 | 4,794 of 9,999 | 0.4795 | 12/19 | 103/133 |
| BF_1 | 11/21 | 1/798 | 1 | 0.02 | 4,039 of 9,999 | 0.4040 | 250/399 | 55/57 |
| BF_2 | 223/399 | 29/798 | 0 | 0.01 | 2,703 of 9,999 | 0.2704 | 262/399 | 1 |
| BF_3 | 223/399 | 29/798 | 0 | 0.01 | 2,697 of 9,999 | 0.2698 | 100/133 | 1 |
| BF_4 | 226/399 | 5/114 | 0 | 0.01 | 2,441 of 9,999 | 0.2442 | 106/133 | 1 |
| N1 | 139/266 | 0 | 99 | 1.00 | 4,085 of 9,999 | 0.4086 | 169/266 | 629/798 |

**Compared with `summary.json`, by float equality and with no tolerance:** 13 values per row (`auc`,
`M_real`, `n_ge`, `n_valid_shuffles`, `n_deg`, `p_S`, `p_P`, `ceiling_full`, `ceiling_block`, the
three λ as one triple, `n_present`, `n_absent`, `leg_S_passes`), 78 in all. **0 differ.** `M_real`
is equal bit for bit in all 6 rows.

Also equal:

- `smallest_passing_auc`: 285/399 (A.2).
- the per-shuffle table: 99 rows × 21 columns = 2,079 cells in `real.per_shuffle`, 0 differ; the same
  2,079 cells in `per_shuffle.csv`, 0 differ. Its header has 21 names, all different (S33).
- the 20 permuted-block ceilings (`real.perm_ceilings_full_rule`), with the labels of each record
  equal to `y[default_rng(91010 + j).permutation(40)]`.
- the 5 fixed-λ rows (`real.fixed_lambda`): AUC, `p_P` and the reuse flag. 3 of 5 are copies of the
  knockout fit (rule #2.1, BF_1, BF_2), 2 of 5 were fitted (BF_3, BF_4), as the log says ("2 fits",
  `stdout.log` line 1491).
- the existence log-loss: the mean binary cross-entropy of `p` against `y`, in nats, equals
  `score.existence` of all 6 knockout records, with a difference of 0.

### B.2 By the script's own readers

`recompute_with_script.py` imports the script and calls `read_raw`, `evaluate_bank("real", …)`,
`label_text`, `verdict_line`, `quote_row`, `a_literals_line` and `conditional_lines` on the stored
fits, with the limits and the U rule of `synthetic_only.json`.

- The object it builds **equals `summary.json`'s `real` as a whole**: 23 keys, 0 differ. This covers
  the columns I did not write code for: `D`, `precision_at_n_present`, `strata_mean_p`,
  `mirror_partners_p`, `auc_other_31`, `per_type_auc`, `p_P_rowcol` and the regrown shares.
- The six fields of `verdict.json` equal the rebuilt values and `summary.json`'s.
- The LF sha256 of the file that was imported is `e650e47e…bb887b`, the script's at `7a10d88`.

### B.3 Two facts of the recomputation that are not in the printed tables

- **Rule #2.1 on the 99 shuffled banks:** M > 0 on 47, M = 0 on 5, M < 0 on 47; the largest is
  +0.0867. The real M is −0.0163 (−13/798), so `n_ge` = 68.
- **The permuted-block ceilings do not fall below the real block's:** 12 of the 20 are at or above
  the real block's `ceiling_full` of 0.6316 (smallest 0.568, largest 0.865, mean 0.667). B
  registered them "with no expected fall" (B:536), so nothing is read from this.

## C. Printed against stored

### C.1 The verdict line

`RESULT.md` line 11 is the only line that starts with "**Verdict: ". Its text equals
`real.verdict_line` of `summary.json` and `verdict_line` of `verdict.json`, character for character.
The same line is in `stdout.log` at 1519 and 1530.

| printed | stored, formatted as the line formats it | equal |
|---|---|---|
| AUC = 0.5063 (19/21) | `real.rows.rule.auc`, `.n_present`, `.n_absent` | yes |
| p_S = 0.69 (n_ge = 68 of 99, n_deg = 0) | `.p_S`, `.n_ge`, `.n_valid_shuffles`, `.n_deg` | yes |
| p_P = 0.4795 | `.p_P` | yes |
| ceiling_full = 0.6316, ceiling_block = 0.7744 | `.ceiling_full`, `.ceiling_block` | yes |
| R/W reading: rule #2.1 -> -, BF_1 -> - | `real.reading_A_rule.letter`, `real.reading_B_BF1.letter` | yes |
| λ: rule #2.1 1, BF_1 1, BF_2 1, BF_3 3, BF_4 3 | `real.rows.<key>.lambda_ko` of the five | yes |

The line holds what A:1330–1341 asks of a failed-fit U: the label, the primary's AUC with its
denominators, `p_S` with `n_ge` of 99 − `n_deg`, `p_P`, both ceilings, the R/W reading on each D1
candidate, and the λ of each knockout fit. With `n_deg` = 0, `p_S` is printed with two decimals and
no mark (S36).

### C.2 The real-block table

`RESULT.md` lines 29–36: 6 rows × 15 cells = 90 cells. Each equals the stored value with the
decimals of its column. **0 differ** (`result_md_checks.py`). The console table, `stdout.log` lines
1497–1503, holds the same values (by eye).

### C.3 The other quantities of B §3.5

All equal to `summary.json` (`result_md_checks.py`):

- the six strata means, 6 rows (`RESULT.md` lines 40–47);
- the 9 mirror partners and the AUC on the other 31 cells, 6 rows (51–58);
- the per-type AUC of the 13 types, 6 rows (62–69);
- the 20 permuted-block ceilings (71);
- the fixed λ = 1 table, 5 rows (75–81);
- D(N1 logit) = 0.126819 (83), stored `checks.5_n1_parity.D_N1_logit` = 0.12681934999344058;
- N1's own `p_P` = 0.4086 (23 and 85), stored `real.rows.N1.p_P`.

### C.4 Whole files

`regenerate_outputs.py` loads `summary.json` and calls the script's `write_committed` with the
output folder pointed at scratch.

- `RESULT.md`, `summary.json`, `per_shuffle.csv` and `synthetic_worlds.csv` come out **byte for byte
  equal** to the files of the committed folder, 4 of 4. So `RESULT.md` holds nothing that
  `summary.json` and A's text do not give.
- `SYNTHETIC.md`, rebuilt from `synthetic_only.json`, equals the private file.
- `synthetic_only.json` without its `manifest`, `checks` and `seeds` equals `summary.json`'s
  `synthetic` as a whole.
- The section of A quoted at the end of `RESULT.md` (lines 893–970) equals A lines 1296–1373, 78
  lines, with the quote mark in front (`quoted_section.py`).

### C.5 Two small remarks

- **Two run times under one name.** `summary.json` holds `manifest.runtime_s` = 8027.44 and
  `runtime_s` = 8216.19. The first is set at the end of the synthetic step (script line 3658) and is
  not set again. `RESULT.md` line 3 and the log's last line print the second, 8216 s, which is the
  whole run.
- **`RESULT.md` line 109 prints the mirror cells as Python tuples**, `summary.json` holds them as
  lists. The content is equal.

## D. Reading

### D.1 Nothing in `RESULT.md` reads the label as more than U

Searched: `RESULT.md` lines 1–260, its own text before the 45 per-world sections, for "no grammar",
"no structure", "regrows", "does not regrow", "absent", "intact", "weaker", "stronger", "not
detected", "motion pathway" and "lamina", without regard to case. **None occurs.** "averag" occurs
once, in line 5, which says that the label "is no evidence for or against averaging", as B:218–219
requires. After line 260, "regrows", "weaker" and "absent" occur only in the sections of the 45
synthetic worlds (their labels and verdict lines, where a G reached through λ = 100 carries A's
registered sentence "'weaker than the detection limit', not 'absent'") and in the quoted section of
A; "no grammar" occurs only in the quoted section of A (`final_checks.py`).

The header says what B §5 asks: block B is "the second block tested on this bank, chosen after
block A's verdict G" (line 5; B:937–938). No line compares block B's instrument with block A's
(B:963–965). The line on earlier runs prints the scope searched and "0 found", and not "intact"
(line 9; S27).

### D.2 The words of the label

The verdict line carries A's words "failed fit" and "cannot hold the block". B's reading, "a failed
fit or a rank limit, not separated", is on line 19, four lines below. That is where B puts it:
beside the verdict, under its condition (S30, B:1129), and not on the verdict line.

A reader who has the verdict line alone has a stronger statement than B allows. The subject of
commit `ce48577` is such a citation: "verdict U, failed fit: ceiling_block 0.7744 < 0.90". It gives
the label and the measurement, which is right as far as it goes, and leaves out the reading.

### D.3 Is the quoted row kept apart from block B's values

**Yes, as B §4 requires.** The quoted row (line 15) is a line of A word for word (A:1328). The next
text, line 17, names the two literals that B:917–921 lists for the U row, and gives block B's own
values:

- "all 3 pre-run U worlds sit at γ = 0.6 = γ\*_P" is named as block A's; block B's worlds are given
  as "4 threshold U on the dense grid, gamma\*_P = 0.75". Both numbers equal `u_rule.n_u_threshold`
  and `limits.leg_P.gamma`.
- "the block is rank 1" is named as block A's board; "block B's real block is not known to be rank
  1".

Nothing stands between the quoted row and that line. B's third literal, "64/64 inferable", is in
the G row and does not occur here.

The quoted row holds two more statements about block A's pre-run that line 17 does not name. B does
not list them, so the script does what B registers; they are noted for the reader.

- "In the synthetic worlds it appears only in the transition band". For block B the band is empty
  and the 4 threshold U lie below γ\*_P. The U-rule paragraph says so (line 203): "they do not all
  lie at gamma\*_P", and block A's reading "is not carried to block B beyond these positions" (S32).
- "This branch never ran in the pre-run (`ceiling_block` = 1.0 in all 225 rule #2.1 and BF rows); a
  test injects the reasons and checks the text (`test_knockout_regrow_labels.py`)". The count holds
  for block B's pre-run too (A.8 item 6). The test file named is block A's.

### D.4 The conditional texts (S30)

**Each is printed under its registered condition.**

In this run all four conditions hold, so the run itself cannot show the other case. I called
`conditional_lines` on made-up outcomes (`regenerate_outputs.py`):

| outcome | lines printed |
|---|---|
| R, W | none |
| G | the A-literals line |
| threshold U | the A-literals line, the additive-channel note, N1's `p_P` |
| failed-fit U | the same three and the failed-fit reading |
| not-measured U, not-readable U | the A-literals line, the additive-channel note, N1's `p_P` |

This is S30's list (B:1129). In `RESULT.md` and in `stdout.log` each of the four texts occurs once,
and N1's `p_P` a second time in the §3.5 lines (`RESULT.md` line 85).

**One remark on the additive-channel note.** Its condition is "a U". The mechanism it names is "a
rule that follows it can pass leg P and fail leg S" (B:926–928). In this run that did not happen:
the primary fails both legs (`p_P` = 0.4795, `n_ge` = 68 of 99), N1's own AUC is 0.5226 with `p_P` =
0.4086, and the U's one reason is the gate. The note says "possible", and the line beside it lets
the reader see N1's `p_P`, so nothing false is printed. A reader should not take the note as a
description of this U.

### D.5 Is it clear that this U concludes nothing about the block

**It is clear that the label is U and not G, and that no sentence says "no grammar".** What the U
means is carried by two texts: the quoted row ("so its failure to regrow says nothing", in block A's
words) and line 19.

`RESULT.md` has no sentence of its own that says what is and is not concluded. A §5's sentence is
not printed, and neither registration asks for it: A:1563–1565 lists what `RESULT.md` holds, and
`quote_section` quotes §4 only (script line 3258).

The table that follows the verdict shows AUCs of 0.51 to 0.57 and `p_P` of 0.24 to 0.48, with the
first two conjuncts of G holding (A.4). A reader can take that for a G in all but name. The
registration forbids that reading (A:1358–1360). An outcome note that cites this run would need A
§5's sentence beside the label.

## E. Gates, order and reproduction

### E.1 Did the gate pass before the folder existed and before check 3 printed the block

**Yes, by the code that ran and by the times of the files. The log cannot show it, by design.**

**The code.** `arm_gate` is called in one place, line 3486 of `main` (Orbit: caller `main`; grep for
`arm_gate(` in the script: the definition at 3399 and the call at 3486). It runs check 1
(`check_pins`), check 2 (`check_block_and_mask`), check 7 (`check_auc_function`), the seeds
(`assert_seeds_unique`) and the provenance (`prerun_provenance`), lines 3412–3429. Each leaves the
run on a failure. Only after it returns come `private_run_dir` (3488), `mkdir` (3489), the marker
(3490–3492), `tee_to` (3523) and `_run` (3526). `real_bank()` and `check_block_print` are in `_run`
(3572, 3576). `_run` takes the gate's results and does not run these checks again in the arm (3554,
3569, 3586, 3588, 3594).

**The log.** `_run` logs the gate's results "at their places" (script lines 3551–3552), so the log
has check 1, the earlier runs, check 2, check 3, check 4, the §1.4 table, check 7, the seeds and the
provenance as lines 1 to 10. That is B §7's order of printing, not the order of execution.

**The times.**

| time | event | source |
|---|---|---|
| 07:33:45 | commit `7a10d88`, the head of the run | git |
| 14:32:57.662 | the console copy is created | its creation time; its name says 143257Z |
| 14:32:58.237 | the private folder, `REAL_ARM_STARTED.json` and `stdout.log` are created | their creation times; the marker's `started_utc` 14:32:58Z; the folder's name |
| 16:46:45.770 to 16:46:48.893 | `synthetic_only.json`, `synthetic_worlds.csv`, `raw_fits.json.gz`, `SYNTHETIC.md` | modification times; the gzip header of `raw_fits.json.gz` says 16:46:45 |
| between | "Two-world check passed: True"; then the real arm, 632 fits in 181 s | `stdout.log` lines 1382, 1468–1490 |
| 16:49:54.347, .349 | `raw_fits_real.json.gz`, `verdict.json` | modification times; gzip header 16:49:54 |
| 16:49:54.517 to .530 | `summary.json`, `per_shuffle.csv`, `RESULT.md`, committed `synthetic_worlds.csv`; the last line of the log | modification times |
| 16:49:54.586, .603 | `SHA256SUMS.txt`, private and then committed | modification times |
| 16:50:38 | commit `ce48577`, the outputs | git |

- The folder was made 0.575 s after the console file. On this machine the interpreter's start, the
  import of the script, the steps before the gate and the five checks take 0.47 to 0.49 s together,
  in three timings (`gate_timing.py`). So there was time for the gate before the folder.
- The search of S27 ran before the folder was made: it found 0 folders, and the same search now
  finds this run's folder.
- 14:32:58 plus the 8,216 s of the log's last line is 16:49:54.

### E.2 The machine checks

| check | result | address |
|---|---|---|
| 1 pins | passed; Python 3.10.20, numpy 2.2.6, rule #2.1 rank 1, A's LF sha256 equal to the pin | `checks.1_pins`; log line 2 |
| 2 block and mask | passed; 40 cells, 5 sources, 8 targets, 4,185 training cells, 64 cells of block A in training | `checks.2_block_and_mask`; log line 4 |
| 3 block print | 19 of 40 present; the block has an AUC | `checks.3_block_print`; log line 5 |
| 4 pre-data tables | **passed**; the table's sha256 equals the registered `aa092028…f7705`, 40 of 40 inferable, the 9 mirrors of B:408–409 | `checks.4_pre_data_tables`; log line 6 |
| 5 N1 parity | printed, no stop: D = 0.126819 | `checks.5_n1_parity`; log line 12 |
| 6 leakage | **passed**; the two hashes are equal, `6027013a…267d705` | `checks.6_leakage`; log line 40 |
| 7 AUC function | passed; five hand cases, both routes | `checks.7_auc_function`; log line 8 |
| 8 harness identity | **passed**; BF_1's margin 0.028150051052145946, difference 0.0 | `checks.8_harness_identity`; log lines 18–40 |
| 9 determinism | **passed**; two fits, one hash | `checks.9_determinism`; log line 40 |
| seeds | 67 new seeds, all different, in 91000–91999, none reserved | `seeds`; log line 9 |

Checked by own means: the eight pinned files have the pinned LF sha256 at `7a10d88` and in the
working tree, 8 of 8. The §1.4 table rebuilt from `offsets.csv` equals the printed one, its
canonical form has the registered sha256, and the 9 mirror cells are the registered ones
(`bank_checks.py`).

### E.3 The two-world check

**It passed, with no stop recorded, before the real block was scored.**

- `two_world_check.passed` is `true`, `.stop` is `false` and `.no_contingency` is `false`, in
  `synthetic_only.json`, which was written at 16:46:45.770, before the real arm's fits.
- The rows: R 5 of 5 read R; Nf 5 of 5 read G; No 5 of 5 read G; W 5 of 5 read W; no family stops
  (`two_world_check.rows[*].labels`, `.stops`). The M rows are the power curve and have no stop.
- In the log, "Two-world check passed: True" is line 1382, the real arm starts at line 1468, and the
  real block is printed from line 1495.
- My recount from `synthetic_worlds.csv` gives the same: a leg-P limit of 0.75 for each of the five
  predictors, γ_R = 0.75, `n_deg` = 0 and 99 valid shuffles in all 270 rows (`reference_checks.py`).
- Before any fit, `smallest_passing_auc` equalled the registered value in 45 of 45 worlds: 0.7125
  (285/400) on board `z`, 40 worlds, and 0.7175 (287/400) on board `z'`, 5 worlds (log lines 41–42;
  `smallest_passing_auc_check`). My own code gives the same two values.
- The `ko1` count is 225 records, 50 copied and 175 fitted, equal to the reference's store (log line
  92; `fits.ko1_count`). I counted the same in both stores.

Checks 6, 8 and 9 fit on the real bank before the synthetic step, and check 3 prints the block's
count at the start. A §3.4 and B §3.4 register that. None of them scores the 40 cells as a knockout
target. Check 8 scores every cell of the bank once inside its ten-fold margin, the block's cells
among them, as B says of block A's check 8 (B:441–445).

### E.4 The console copy against the private log

**They agree on every line.** Both have 1,532 lines. With the carriage returns taken out of the
console copy (1,532 of them; it has CRLF line ends, the log LF), `diff` finds no difference. The
console copy holds no line that the log lacks. If both streams were redirected into it, as
B:1159–1166 registers, nothing was written to the error stream (last section, item 8). Neither
holds "Traceback", "Error", "Warning", "REFUSED", "SMOKE", "DIFFERS", "FAILED", "STOP", "NOT THE
REGISTERED RUN" or "NOT A REFERENCE", searched in these spellings, capitals kept.

### E.5 A clean committed tree

**Yes, as far as the run's own record and the hashes can show.**

- `manifest.git_head` = `7a10d88ec95e65b809e629b3398ceaa193e6a2f8`;
  `manifest.tree_dirty_under_c6_or_plans` = `false`; `.tree_dirty_paths` = []; `.allow_dirty` =
  `false`; `.not_the_registered_run` = `null`. The marker holds the same head.
- `manifest.script_sha256_lf` = `e650e47e…bb887b` and `manifest.registration_sha256_lf` =
  `bd290d26…83a61f`, the LF sha256 of the two files at `7a10d88` (0.1).
- `manifest.command_environment.argv` is the registered command, `--arm flyvis65_blockB --starts 10
  --workers 30` (B:1155), and `PYTHONUTF8` is "1". `log_output_errors` is 0.
- The run was made from the main checkout: the log's line 1531 names the committed folder inside
  `connectome-seed/` (B:1175–1192).

The refusal covers `results/genome/c6/` and `docs/plans/` only, by registration (A:614–615).

### E.6 The reproduction gate

**It passed: outcome 1.**

- "pre-run table (section 7): outcome 1: every deciding column equal; byte-identical (recorded, not
  gated); rows matched by family/j/seed/predictor: 0 missing now, 0 missing in the pre-run table, row
  order equal …" (log line 93; `two_world_check.prerun_reproduction`: `outcome` 1, `passed` `true`,
  270 rows on each side, 0 exact differences, 0 continuous differences).
- The per-fit diagnostic: 28,665 records compared, 0 differ in `p`, λ, labels, scores, outside
  density or the reuse flag; the largest difference in `p` is 0.0 (log line 94;
  `raw_fits_diagnostic.total`).
- **By own means:** the run's `synthetic_worlds.csv` and the reference's have one sha256,
  `2187ce89…8740dcb`. The two `raw_fits.json.gz` stores have the same 28,665 keys, and no record
  differs in any field but `secs` (`reference_checks.py`). The two stores come from two fitting runs:
  `fits.saved_reread` is 0 and `fits.fitted_main` is 28,440 in both.
- **The provenance (S37):** the reference's manifest names head `5f9cc51b…0e4cacf` and script
  `2bb92b43…27abe69`, the registered values. It records a clean tree, no `not_a_reference`, `--starts
  10`, no `--from-raw`. The LF sha256 of the script at `5f9cc51` is that value, and of B at `5f9cc51`
  it is `3bb1bc34…de357e`, the value B:671–672 gives.
- **The five pins** in the script (lines 129–134) equal the five lines of the reference's
  `SHA256SUMS.txt`.
- **Between the two heads** the script changed only in its revision strings, the `PRERUN_*`
  constants, one docstring, and `arm_gate` with its wiring into `main` and `_run` (`git diff 5f9cc51
  7a10d88`). No line of `evaluate_bank`, `read_label`, `u_kind`, `label_text`, `verdict_line`,
  `smallest_passing_auc`, `conditional_lines`, the fitting functions or the world generator changed.
  The code that read the 45 worlds of the reference is the code that read the real block.

### E.7 The checksum lists

Verified with `sha256sum -c`, and each list compared with the files of its folder.

| folder | entries | verify | files that the list does not name |
|---|---|---|---|
| the private folder | 8 | 8 of 8, `stdout.log` among them | none |
| the committed folder, in this working tree | 4 | 4 of 4 | none |
| the reference | 5 | 5 of 5 | none |

The sha256 of the three lists are `4b35f753…4dbe658` (private), `a149efb4…6bd6a16` (committed) and
`696d1d38…9f00207` (reference). The console copy is pinned nowhere; its sha256 is
`a6d88f4d…cfc0b4a`.

**The caveat.** Two entries of the committed list are sums of bytes that git does not hold.

- `per_shuffle.csv` and `synthetic_worlds.csv` are written with CRLF line ends (Python's `csv`
  module). This checkout has `core.autocrlf = true`, and no git attribute applies to the two files
  (`git check-attr -a`; the repository root has no `.gitattributes`), so git stores them with LF:
  `git ls-files --eol` gives `i/lf w/crlf` for both.
- The blobs at `ce48577` have sha256 `75601f42…0aa22e55` and `f9e22bd0…2abb30bf`. The list gives
  `28ffdb42…c321206a2` and `2187ce89…8740dcb`. Those are the sums of the working-tree bytes, and of
  the blobs with LF turned back into CRLF (checked).
- `RESULT.md`, `summary.json` and `SHA256SUMS.txt` are LF in both places.

So a checkout that converts line ends as this one does verifies 4 of 4, and a checkout that does not
(Linux, or `core.autocrlf = false`) verifies 2 of 4, with nothing changed. S29 asks that the sums
verify for the files the run wrote, and they do. It does not speak of git's conversion.

### E.8 One run

At its start the run found no earlier real-arm folder: "root read: …\knockout_regrow, folders
`flyvis65_blockB_*`; 0 found" (log line 3; `manifest.earlier_real_arm_runs`). Now the folder
`connectome-seed-data/knockout_regrow/` holds one folder named `flyvis65_blockB_*`, this run's. It
holds no `stop_record.json`, and it has its sums, so the run completed (S29, S39). Searched: that
folder on this machine, for names that hold "lockB".

## What could not be checked, and why

1. **The forbidden sections.** B lines 1–172 and §9 to §11, and A lines 1–172, §10 and §12, were not
   read. B's decisions D1 to D13 are cited all through the sections read, and their text is in B
   §10. Where the sections read say what a decision means at the place of use, I used that: D8 and
   D9 in B §4, D3 in B §1.3 and §3.4. If B §10 words one of them otherwise, this review cannot
   know it.
2. **The order of the gate** is read from the code and from the times of the files (E.1). No output
   of the run records when the gate ran.
3. **Why the primary's block-only fit selected λ = 100.** A store record holds `p`, `y`, `lam`,
   `score`, `outside_density` and `secs`. It does not hold the inner held-out log-likelihoods of the
   five λ. They could be had only by fitting again, and no fit was made in this review.
4. **Whether the stored `p` are what the fits give.** Nothing was refitted. For the synthetic step
   two fitting runs agree in all 28,665 records. For the real arm the run's own evidence is check 9,
   two fits of the primary on the knockout view with one hash. The other real-arm fits were made
   once.
5. **The machine.** One machine, one BLAS kernel. No second machine and no second thread setting was
   tried (A:735–746).
6. **The script's tests** were not run. Whether each test named in B §7 fails under its mutation
   was not checked.
7. **The requirements S23 to S40** were not checked one by one. Checked: S25 (by the times of the
   files), S27, S29, S30, S31 (every quantity of B §3.5 has its table or line), S32, S33, S36, S37
   (the header line of `RESULT.md` and the manifest) and S38 (the count line, `RESULT.md` line 205).
8. **The command as typed.** The manifest records `argv` and `PYTHONUTF8`. That both streams were
   redirected with `2>&1` (B:1159–1166) cannot be seen from the files. The console copy holds no
   line that the log lacks. That fits a redirect of both streams in a run that wrote nothing to the
   error stream, and it fits as well a redirect of the output stream alone.
9. **"On Mike's word"** (B:1153–1154) is recorded in the chat only, which is forbidden.
10. **Other machines and folders.** The search for other real-arm runs covered one folder on this
    machine (E.8).
11. **The second reader's blindness** rests on its own declaration (0.3 item 7, A.9).

## Appendix: queries, searches and scratch scripts

**Orbit** (repository `C:\Users\mikha\Documents\dpc-research\connectome-seed`, project
5719256599771620764, indexed at `ce48577…`):

- `SELECT * FROM _orbit_manifest`
- `SELECT name, definition_type, start_line, end_line FROM gl_definition WHERE project_id = … AND
  file_path = 'results/genome/c6/checks/knockout_regrow_block_b.py' ORDER BY start_line`
- `SELECT tgt.name AS callee, src.name AS caller, src.file_path, src.start_line FROM gl_edge e JOIN
  gl_definition tgt ON e.target_id = tgt.id JOIN gl_definition src ON e.source_id = src.id WHERE
  e.relationship_kind = 'CALLS' AND tgt.file_path = '…/knockout_regrow_block_b.py' AND tgt.name IN
  (…45 names…)`

**Grep, to confirm** (ripgrep, on the script):

- `\b(arm_gate|check_block_print|private_run_dir|real_bank|tee_to|write_sha256sums|find_earlier_runs|check_registered_constants|refuse_if_dirty|out_dir_refusal)\(|REAL_ARM_MARKER`
- `\b(evaluate_bank|read_label|u_kind|label_text|verdict_line|smallest_passing_auc|conditional_lines|reading_on|a_literals_line|ceiling_block_reason|quote_row|write_verdict_json|write_committed)\(`
- `knockout_regrow_block_b` in `*.py` of the repository, as ripgrep walks it: 2 files, the script (4
  lines) and `test_knockout_regrow_block_b.py` (8 lines). No other Python file names the module.

The graph and grep agree on every caller but one. The graph has no edge from `u_positions` to
`u_kind`; grep finds the call at script line 2771, inside a generator expression.

**Callers of the functions the brief names,** inside the script:

| function | called by |
|---|---|
| `evaluate_bank` | `run_synthetic` (2626), `_run` (3686) |
| `read_label` | `evaluate_bank` (1536) |
| `u_kind` | `label_text` (1685), `conditional_lines` (1788), `u_rule` (2370), `u_positions` (2771) |
| `label_text` | `verdict_line` (1725), `run_synthetic` (2636), `_run` (3687) |
| `verdict_line` | `run_synthetic` (2638), `_run` (3689) |
| `smallest_passing_auc` | `board_smallest_passing_auc` (1381), `check_smallest_passing_auc` (1425), `evaluate_bank` (1527) |
| `conditional_lines` | `_run` (3695) |
| `arm_gate` | `main` (3486) |

The test file calls them too.

**Scratch scripts** (the session's scratch folder, outside the repository; sha256, first 12 digits):

| script | what it does | sha256 |
|---|---|---|
| `explore1.py` to `explore4.py` | print the stored values named in A.1 and E | `feb8c60b1dca`, `50db80c03a8b`, `2c74a1105e65`, `498830f3dfa1` |
| `recompute_independent.py` | B.1 | `031df37d7aee` |
| `recompute_with_script.py` | B.2; the labels of the store against the harness's bank | `c85cf7a06084` |
| `result_md_checks.py` | C.1 to C.3, D.1 | `eb7008cd2076` |
| `regenerate_outputs.py` | C.4, D.4 | `746fb71bb614` |
| `quoted_section.py` | C.4, C.5 | `12428e79deb5` |
| `reference_checks.py` | E.3, E.6, A.8 item 6 | `d515e7c3009e` |
| `bank_checks.py` | A.2, A.8 item 5, E.2 | `03d33ebfda43` |
| `block_only_fits.py`, `interaction_exact.py`, `bf_same.py` | A.5, A.8 | `a81d97a376c0`, `dfb8cd3fb1e2`, `6be3f8fbf94c` |
| `gate_timing.py` | E.1 | `99b5cc295d1f` |
| `grep_allowed.py` | searches of A and B inside the allowed ranges | `1bd57b75c139` |
| `final_checks.py` | single sentences of A.5, A.8, D.1 and E.4 | `4488cd15d8af` |
| `verify_citations.py` | 170 citations of this report against their sources | `7d5cad553f65` |
| `extract_allowed.py` | the second reader's; prints the allowed keys of `summary.json` | `7d61100818ca` |
