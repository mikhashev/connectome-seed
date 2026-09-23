# Handover — for the session that starts after 2026-09-23

**Written:** 2026-09-23 UTC, by CC, on Mike's word (DPC Research group, 2026-09-23 07:32 UTC:
"a retrospective in the chat and a plan for a new session; there is a lot of context here, we
continue in a new one", translated from Russian).
**Audience:** whoever opens this repository next, human or agent.

**This file carries no result value.** Where a finding is numerical, the file that holds the number
is named instead, as in [`2026-09-20-next-session-handover.md`](2026-09-20-next-session-handover.md),
which this file follows and does not replace. Terms are those of [`GLOSSARY.md`](../../GLOSSARY.md)
(committed at `4f69613`, 94 terms; if a term here is used differently there, the glossary wins).

---

## 1. Where the grammar track stands

The main line is grammar ([ADR-004](../decisions/004-grammar-is-the-main-line.md), accepted; the
measurement line is paused, not cancelled, by its 2026-09-20 amendment).

In order, all committed and pushed:

1. **Generation zero** — the bank of 65 types and 605 type-pair entries with content-derived birth
   ids: `results/genome/bank/` (README there).
2. **Regularity measured, descriptive only** — `results/genome/bank/REGULARITY-READING.md`.
3. **The C6 exam**, specified in `docs/plans/2026-09-23-c6-control-specification.md` and built with
   no rule in it: `results/genome/c6/`. The build found defects in the exam itself.
4. **The exam amended** (option A, Mike 2026-09-22 21:01 UTC) against acceptance criteria registered
   first: `docs/plans/2026-09-23-c6-amendment-acceptance.md`, `-2.md`, `-3.md`. One registered
   criterion (R1) fails and stands as recorded; A6 could not be built, as predicted in writing
   before it was run. Records: `results/genome/c6/HARNESS-CONTROLS.md`.
5. **The first rule** — proposal `docs/plans/2026-09-23-first-rule-proposal.md` (registered at
   `5a46886`); its search, as registered, stalled on planted tables, so it was fixed (option B, Mike
   2026-09-22 22:38 UTC) against a criterion committed first:
   `docs/plans/2026-09-23-first-rule-search-criterion.md`. Code and gate records:
   `results/genome/c6/rules/first_rule/`.
6. **The first rule's single C6 run: FAIL** (Mike's word 2026-09-23 06:58 UTC). Commit `8528061`
   carries the verdict verbatim in its subject. Record:
   `results/genome/c6/rule_runs/first_rule_k12/RESULT.md`. A first attempt crashed before any
   verdict on a missing log directory (`89683c6`).

## 2. Blindness — who has read what

- **Ark and Johnny have not opened the rule proposal or the rule code.** Their right to review the
  exam and its positive controls depends on that. Do not send them rule content.
- **Zcode opened the rule** (disclosed 2026-09-22 21:43 UTC); his reviews since are mechanical, and
  he is the reviewer for rule-side changes.
- The exam's corrector agent never opened the rule; the rule's implementer read it.
- The blind-author exclusion list for ADR-003 is regenerated after every commit that adds numbers:
  `docs/blind-author-exclusions.txt`.

## 3. The plan for the next session, in order

**0. The decisive, cheap check — before anything else.** Does N1 itself separate the real bank from
the 99 shuffled banks on existence? The run's P3 reports the rule's margin over N1, not N1 alone.
If N1 separates too, the structure the rule touched is marginal (degree), and a second rule of the
same family is pointless; if N1 does not, a non-marginal structure exists and the next rule should
model the residual after the marginal model. Write the per-shuffle values to a file (the run
committed only aggregates — a debt named by Zcode). CPU, minutes.

**1. Record the multiplicity caveat** on the run's single small P3 p-value (one of four fields, no
correction) in `RESULT.md`, before any second-rule family is chosen.

**2. The proposal's own pre-registered checks that were not run** (Zcode, 2026-09-23 07:38 UTC):
the random-label arm (§4.3) and the k = 8 / 16 sensitivity (§2.6). Either run them now as the
proposal registered them, or carry them into the second rule's registration. Do not drop them
silently.

**3. Failure analysis against the proposal's §4** — an explanation by someone who has seen the
numbers, so its conclusions are registered as **predictions** before the second rule is written
(Johnny, Ark).

**4. The second rule** — its family depends on step 0. Thresholds registered before its run. No new
run on these data without a new registration.

**5. Hygiene, public repository:**
- a table "verdict label → field and check" beside the verdict, because the joined label line reads
  as "everything is dead" and the spec label "rule did not run" (A11) is printed identically to the
  literal crash of the first attempt (Ark);
- `results/genome/c6/README.md` cites Ark at 2026-09-23 21:35 / 21:44 UTC; the messages were
  2026-09-22 (Ark); its "no rule is registered, and none has been run" is stale;
- `results/genome/c6/rules/first_rule/README.md` still says the run is not approved (Zcode);
- **a systematic date error, CC's:** the group's evening of 2026-09-22 UTC (about 20:40–23:59 UTC,
  which was already 2026-09-23 in local +07:00) is cited as "2026-09-23 HH:MM UTC" in the three
  acceptance files, the spec's amendment header and the C6 board entry, because CC's briefs to the
  agents carried the local date with UTC clock times. The acceptance files are hash-locked by the
  harness, so the fix is a dated erratum appended beside them (and an `append` on the board), never an
  edit of the locked bytes. Ark caught the first instance (the c6 README);
- the public chat summary called the rule's offset set "worse than all three"; it is worse than N0
  and N_EB and better than N1 in half the folds (Zcode). The record is correct; the summary was not.

**6. Older debts** (each has a board entry in `backlog.md`): the S2 design's description of the
Shuvaev decoder; bare local timestamps in the row-B records; the unreproducible PROFILES-READING §0
hash; the ~16 MB scratchpad remainder; broken `.exe` shims in the environment; ADR-004's open
confirmation boxes and its Q2 ("what is the elephant beyond grammar"), which waits on Mike.

## 4. Working conventions confirmed in this session

- The group chat: markdown only, sent as a file; **no @-tags** (Mike, 2026-09-23 07:32 UTC).
- The board is edited only through dpc-messenger `tools/backlog/build.py` verbs (Mike, 2026-09-22).
- Terms come from `GLOSSARY.md`; a new term is added there before it is used in a record (Mike, 2026-09-23 07:04 UTC).
- A registration is a commit before the value, never a hash printed beside it: the regularity
  declaration reproduces from git, the profiles seal does not.
- A positive control for every instrument, and the search is an instrument of its own.
