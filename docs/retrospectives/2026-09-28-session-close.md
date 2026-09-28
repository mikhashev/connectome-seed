# Retrospective — session of 2026-09-27 14:27 UTC → 2026-09-28 ~20:15 UTC

**Written by:** CC (drafted by a CC subagent), on Mike's word (DPC Research chat, 2026-09-28
20:00 UTC, as relayed by CC: "run, then a retrospective here in the chat, then close the session
and continue in a new one"). **Audience:** Mike and the reviewers (Ark, Johnny, Zcode).

**This file carries no result value.** A verdict is named, together with the file that holds it.
Every number behind a verdict stays in that file. Structural counts, dates, commit hashes and
instrument timings are written plainly. Times are UTC. The chat is not in the repository; a chat
time below is cited as relayed by CC.

---

## 1. What the session produced

- **Block B's registration, revisions 1.2 → 1.7.3.** The file is
  `docs/plans/2026-09-25-knockout-regrow-block-b-registration.md`; its §10 holds every revision's
  votes, edits and journal rows. Ark, Johnny and Zcode reviewed each round.
  - 1.2 (`9b86839`): A's pins after Amendment 1, S1–S22 re-checked against the male script, the
    male arm's 13 debts as S23–S35.
  - 1.3 (`6b195bc`), 1.4 (`68c0171`), 1.4.1 (`3e5f2da`): the reviewers' passes; the not-readable U
    (S38), the stop record (S39), male S28/S30 ported as S36/S37.
  - 1.5 (`b810ecb`), 1.6 (`8bb5aee`), 1.6.1 (`5f9cc51`): the reviewers' passes on the script; S40
    (a dirty tree is not a reference); A4 (a re-read never makes the reference) with three carriers
    in code.
  - 1.7 (`bb398a2`): the pre-run's values pinned. 1.7.1 (`891d144`): the reviewers' edits.
  - 1.7.2 (`62228ad`): the gate order (`arm_gate` before the folder, the marker and the show).
  - 1.7.3 (`404f098`, `7a10d88`): the reviewers' notes on 1.7.2, the console redirect for a refusal
    before the folder, the one-time re-read's outcome.
- **Block B's script and tests** (`results/genome/c6/checks/knockout_regrow_block_b.py`,
  `test_knockout_regrow_block_b.py`): first committed at `1a765f5` (S1–S39), then revised with each
  registration revision; S1–S40, 68 tests at 1.7.2 and 1.7.3 (all passed, no skips).
- **The pre-run**, 2026-09-27 21:10–23:23 UTC, from `5f9cc51` (revision 1.6.1), on Mike's word
  (about 21:10 UTC, as relayed by CC). Reference
  `synthetic_blockB_prerun_20260927T211052Z_5f9cc51b9a24`. The two-world check passed; the
  limits γ\*_P and γ_R are both 0.75 on block B's worlds (registration §10, revision 1.7).
- **The one-time diagnostic re-read** of the pinned store, 2026-09-28 07:24:33 UTC, from `62228ad`
  in the worktree `cs-blockb-pins`: outcome 1, byte-identical, 7 s. Not a registered step; its
  console file is its only record (registration §10, revision 1.7.3).
- **The registered run**, 2026-09-28 14:32:58–16:49:54 UTC, from `7a10d88` (revision 1.7.3),
  8216 s. **Verdict: U, failed fit.** The file is
  `results/genome/c6/checks/knockout_regrow_block_b/RESULT.md`; outputs committed in `ce48577`.
  Read it with `READING_NOTES.md` in the same folder: on block B the failed fit is read "a failed
  fit or a rank limit, not separated", and nothing about the block is concluded from it.
- **The blind review** by an external session (Fable, a fresh Claude Code session given only the
  brief): **"the verdict follows"** (`804f87a`,
  `docs/notes/2026-09-28-knockout-regrow-block-b-blind-review.md`).
- **The committed sums fixed** (`c42f184`): the two CSVs are stored as the run wrote them (CRLF),
  through a folder-scoped `.gitattributes`, so `SHA256SUMS.txt` verifies on any checkout.
- **`READING_NOTES.md`** beside the frozen outputs (`a2c8738`, `29491de`, `c37b846`): the reading
  `RESULT.md` lacks, the post-data observations that decide nothing, two findings about the
  artifact, the open questions, and §9, the fit diagnostic.
- **The fit diagnostic** of rule #2.1's block-only λ (step (ii) of Ark's order, agreed by Mike
  19:28 UTC): plan, script and fixture tests (`3fb444b`), revision 1 with the reviewers' edits
  E1–E6 (`3be7824`; Johnny, Ark, Zcode 19:52–19:56 UTC), run 20:08 UTC on Mike's word (20:00 UTC),
  5 s. Its registered reading: **"(c) carried by few folds"** (`READING_NOTES.md` §9;
  `docs/plans/2026-09-28-block-b-fit-diagnostic.md`). It changes nothing about the label.
- **Question (ii)'s pause kept** on Mike's word (2026-09-27 14:31 UTC); the resume condition is an
  R label, not a registration (`bbfa91b`).

## 2. What went well

- **The failed-fit precedence held block B away from G.** The rule that a U whose reasons include
  a low `ceiling_block` is a failed fit, never renamed and never read as G, was in A §4 before
  block B's run. The run met exactly that branch, and the label was read as the text says
  (`READING_NOTES.md` §1–§2).
- **The reproduction gate and the re-read agreed with the reference.** The run's gate passed with
  outcome 1; the per-fit diagnostic compared 28,665 keys with 0 differences. The re-read before
  the run had already shown the pinned store read back byte-identical.
- **Reviewers recomputed from files.** Examples: Zcode's independent test runs at every script
  revision; Ark's line-number check of Johnny's step table from `git show 891d144`; Ark and Zcode
  checking that the real block is readable (not the S38 U) before reading the label.
- **The blind review gave a second derivation and file-time evidence.** It derived the label a
  second time from the registered text (review A.9), recomputed every deciding number with code
  that imports nothing from the script (B.1), and showed from file creation times that the gate ran
  before the folder existed (E.1), which the log cannot show by design.
- **The gate reorder (1.7.2) was found before the run.** CC found it while checking Ark's P2: at
  1.7.1 a bad pin or a missing reference would have stopped the run after block B was printed and
  the marker written.
- **The fit diagnostic reads a margin, not a set membership** (edit E1, before the run). Sets built
  by construction (for example "the folds that prefer λ = 100") would have decided by how they were
  built; the margin, with and without the single-class fold, and leave-one-fold-out, did not.

## 3. What went wrong, and what it cost

- **"A name without a carrier": many errors, several of them CC's.** Each was caught by a reviewer
  or by the drafting agent and cost a journal row or a correction round.
  - CC's chat message (2026-09-27 15:32 UTC) said "three line ranges were wrong in 1.2"; the file
    records two (Zcode; registration §10, revision 1.4).
  - "D10 (iv)" named no item (D10 has options (i) and (ii)). It was Zcode's name (17:01 UTC),
    passed on by CC unchecked, and caught by the drafting agent (revision 1.6, row 8).
  - CC gave a wrong reason for A4 (S37's single writer hash, committed in `b810ecb`); the real
    reason is the object: the store's key carries no block and the labels come from the store (Ark
    17:58 UTC; revision 1.6's journal row). Cost: a revision.
  - A4's rule had no carrier in code until 1.6: it stood as prose only (Ark 18:00 UTC). Cost: three
    code carriers and three tests.
  - "numpy 2.4.6": no such version was used; both probe tables were made on numpy 2.2.6 (Ark's
    own correction; revision 1.4.1).
  - Johnny's literal fix to the L3 parenthesis would have given Tm20 an ON/OFF side that no file
    names; Ark's form was applied instead (revision 1.4, "Not applied").
  - "B §2.4" was called nonexistent, by Ark and then by CC after checking the headings only. It
    exists, as the delta item headed "§2.4, the two ceilings" in B §2 (B:529). The script's printed
    address "(B section 2.4)" is still ambiguous for a reader (`READING_NOTES.md` §4 (a)).
  - CC's message of `c42f184` calls sha256 values of the stored files "blobs".
  - The subject of `ce48577` cites the verdict line and its measurement without the reading
    (review D.2; `READING_NOTES.md` §4 (b)).
- **The real arm's gate order.** Until 1.7.2 a bad pin, a corrupt or missing reference, or A's
  changed registration would have stopped the run after block B was printed and the marker
  written. Cost: revision 1.7.2, one new test with two inputs and a mutation check; it did not
  reach a run.
- **A refusal inside `arm_gate` left nothing on disk** until 1.7.3 (no folder, no marker, the log
  buffer never written). Cost: the registered command gained a console redirect, the only carrier
  of such a refusal (Ark 07:23 UTC, required).
- **The committed sums were sums of CRLF bytes while git stored LF.** The csv module wrote CRLF;
  CC's decision on OPEN 3 (revision 1.5) put `SHA256SUMS.txt` in the committed folder too; without
  a `.gitattributes` git normalised the two CSVs. Found by the blind review (E.7). Cost: a fix
  commit (`c42f184`) and two unsummed files in the folder (`.gitattributes`, `READING_NOTES.md`).
- **CC let the Orbit rule lapse.** After the first few briefs CC stopped writing the Orbit line
  into subagent briefs, did not query Orbit itself, and did not index a new worktree, until Mike
  asked (DPC Research chat, 2026-09-28 07:10 UTC, as relayed by CC). Revision 1.7.3's T1 and the
  blind review's E.1 then used the graph.
- **CC asked the agents to "object before merge" without tagging them.** Agents reply only when
  tagged (Mike, DPC Research chat, 2026-09-28 06:39 UTC, as relayed by CC). Cost: the question had
  to be asked again, with tags.
- **The DPC backend was down for part of the pre-run report** (as relayed by CC; no file records
  it). Cost: a delayed report.
- **A previous CC session ended in the middle of a subagent's work** on the diagnostic's edits
  E1–E6; it was resumed and finished in `3be7824` (as relayed by CC).

## 4. Lessons and rules adopted

- **Check the text under a heading, not only the heading.** A section can exist as an item inside
  another section.
- **A rule needs a carrier in code, with a test that fails without it**, not only prose in the
  registration.
- **Ask the agents with tags.** An untagged question is not a question to them.
- **Every code brief carries the Orbit line**, and every new worktree is indexed; CC queries Orbit
  itself for callers before relying on grep.
- **The pinned bytes are the writer's bytes.** A sum pins what the script wrote (CRLF from the csv
  module); git must store those bytes, or the sum is compared with different bytes.
- **A refusal before the folder exists needs the console redirect**; the redirect is part of the
  registered command.
- **Read decisions by margins, not by set membership, when the sets are built by construction.**
- **A commit subject or a citation of a verdict carries its reading**, not the verdict line alone.

## 5. Open items

Listed for Mike, not chosen (`READING_NOTES.md` §8–§9):

- **(i) Calibrate the failed-fit branch** with synthetic worlds of known cause, so that a
  `ceiling_block` below the gate has a reference (Ark). No synthetic world met the branch.
- **(iii) A gate that measures the interaction**, not the additive part (Zcode). After the fit
  diagnostic: it needs λ < 1 or a fixed λ, and inner folds without single-class members.
- **(iv) The rank question** is no longer testable on block B, since its rank is now known; it
  needs constructed worlds or another block (Ark).
- **(v) Primary versus family:** change the rule that reads the gate on rule #2.1 alone only in the
  registration that brings a witness for the branch (Ark).
- **The script's address "(B section 2.4)"** is fixed only by a script revision with its own head;
  the frozen outputs are not edited.
- **A test on the stored bytes of committed sums** (Zcode): that `SHA256SUMS.txt` verifies against
  the blobs git holds.
- **ADR-002** stays unresolved.
- **Question (ii)** stays paused (resume on an R label on some block, or a way to separate brain
  agreement from averaging agreement).
- **Ark's proposal:** move the main line to animal banks and build FlyWire with the male builder's
  construction (no offsets). It needs a registration.
- **Backlog:** the block B entry is closed as fixed (registered run done, verdict U, blind review);
  the knockout entry carries this session's progress; a new entry,
  `THE-FAILED-FIT-BRANCH-HAS-NO-SYNTHETIC-WITNESS-AND-THE-GATE-DOES-NOT-MEASURE-THE-INTERACTION`,
  holds items (i) and (iii).

## 6. Commits

`bbfa91b`, `9b86839`, `6b195bc`, `68c0171`, `3e5f2da`, `1a765f5`, `b810ecb`, `8bb5aee`, `5f9cc51`,
`bb398a2`, `891d144`, `62228ad`, `404f098`, `7a10d88`, `ce48577`, `804f87a`, `c42f184`, `a2c8738`,
`29491de`, `3fb444b`, `3be7824`, `c37b846`. The session-close commit adds this file and the backlog
and roadmap updates.
