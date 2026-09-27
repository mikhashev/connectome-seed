# Retrospective — session of 2026-09-25 09:41 UTC → 2026-09-27 ~14:10 UTC

**Written by:** CC (drafted by a CC subagent), on Mike's word (DPC Research group, 2026-09-27
13:51 UTC, as relayed by CC: "fix the current progress in the documentation where needed and in
the backlog, do a retro, and close the session; we continue in a new one"). **Audience:** Mike and
the reviewers (Ark, Johnny, Zcode).

**This file carries no result value.** A verdict is named, together with the file that holds it.
Every number behind a verdict stays in that file. Structural counts, dates, commit hashes and
instrument timings are written plainly. Times are UTC.

---

## 1. What the session produced

- **Knock out and regrow, block A on flyvis-65: registered, run, and blind-reviewed.**
  - Registration revisions 3.1 → 3.4.1 (`8a514fa`, `52eb381`, `1d6bb9e`, `e6bba28`, `cde61d4`,
    `ea8fe27`, `74db080`), reviewed by Ark, Johnny and Zcode.
  - The registered run: head `74de040`, 2026-09-25 17:16–19:31 UTC, on the CPU. **Verdict G.**
    The file is `results/genome/c6/checks/knockout_regrow/RESULT.md`.
  - A blind review in a separate session found that the verdict follows
    (`docs/notes/2026-09-26-knockout-regrow-blind-review.md`). Outputs and review were committed
    together in `1ed55ec`.
- **The GPU instrument: from a prototype to a registered and validated instrument.** It is a
  separate instrument, and no registered arm reads it.
  - Early versions:
    - v1 for BF_r (`74de040`);
    - v2/v3 for the shuffled banks and rule #2.1, bit-equal through the harness's decode on the
      45 synthetic worlds (`cdbde9e`, unreviewed).
  - Registration `docs/plans/2026-09-26-gpu-instrument-registration.md`, revisions 1 → 1.4
    (`fedeec5`, `345acf2`, `5983385`, `ec5cbc0`, `e2fab47`). The E2 criterion became a tie census
    (Ark, Zcode).
  - Code G1–G16 with tests T-G1–T-G10 (`a0e16b6`).
  - Validation:
    - V0–V7 PASS or statements (`e50bf74`);
    - the V8 male CNS adapter (`1ad6155`);
    - V8 on lobes L and R: CROSS-CHECK EQUIVALENT (`0c7a67b`).
- **The male CNS bank builder and the bank.**
  - Builder registration drafted (`d6e3759`), then revision 2 (`8591491`).
  - Builder and fixture tests (`bdd250c`). The `--inspect-only` output went to review
    (`2af21e5`).
  - Revision 2.1 (`476cf9b`), with the inspect-only output from the clean tree (`e0a3cd7`).
  - The bank was built on 2026-09-26 on Mike's word (`5860619`). `bank.meta.json` is pinned by its
    LF sha256 (`c8f0ea5`).
- **The male CNS arm, end to end.**
  - Registration `docs/plans/2026-09-26-knockout-regrow-male-cns-arm-registration.md`, revisions
    1 → 1.3 (`f82d442`, `a6761e2`, `af11d31`, `70e759e`).
  - Script and tests (`ee380a1`).
  - Pre-run of both lobes, 2026-09-26 13:12–17:37 UTC, from `a0e16b6`.
  - Amendment 1 to block A's registration (`6fff1e4`). A's amended hash was set in `01d2d05`.
  - Registered run 1 (head `01d2d05`) broke the seal after unsealing. It crashed on a cp1252
    stdout error at 2026-09-26 23:25 UTC. The break is recorded in `e07e347` and in
    `SEAL_BROKEN_NOTE.md`.
  - Registered run 2 (`e07e347`, `PYTHONUTF8=1`), 2026-09-27 07:16–11:32 UTC. The result:
    - **G in both lobes; male reading G;**
    - **S0** (k = 0);
    - **joint reading with flyvis-65's G: agreement**, with the registered caution.

    The result is in `results/genome/c6/checks/knockout_regrow_male_cns/RESULT.md` (`0286ae1`).
    Read it together with `SEAL_BROKEN_NOTE.md` and `READING_NOTES.md` in the same folder.
  - The blind review of run 2 found that the verdicts follow (`63b0366`,
    `docs/notes/2026-09-27-knockout-regrow-male-cns-blind-review.md`). The reviewers then
    reclassified its findings (`86d7288`).
- **The Q2 note** (`0914962`, `docs/notes/2026-09-27-knockout-regrow-power-curves-A-vs-male.md`).
  It is a diagnostic with no fitting. It found that the male power curves and A's cannot be
  separated from a different draw of worlds. The claim "instrument weaker" was therefore narrowed
  in the arm's ledger (`46365e7`).
- **Block B on flyvis-65.** The registration was drafted and revised to 1.1 (`d6e3759`,
  `8591491`). Nothing has been built or run.
- **Backlog, through `build.py` at the close:**
  - GPU entry: progress appended.
  - Male CNS builder entry: closed as fixed.
  - Knockout entry: block A, the male arm and the next steps appended.
  - Block B: a new entry, with the script debts.

## 2. What went well

- **Reviewers recomputed from files instead of from prose.** Some examples:
  - Johnny's count of the degenerate shuffles on the pinned `synthetic_worlds.csv` (A §11);
  - Ark's census recount;
  - Zcode on `RESULT.md:3` and the header lines.

  Both blind reviews recomputed every deciding number from the private raw fits.
- **The tie census replaced a p-tolerance** as the GPU equivalence criterion E2 (Ark, Zcode;
  GPU registration revision 1.2). A tolerance says how far apart two values may be. The census
  says which pairs of values could swap order, which is what a label depends on.
- **The blind review caught record defects that no gate checks.** Examples:
  - on flyvis-65: the run's stdout log kept outside the run folder, and the pre-run reference's
    provenance records not yet added;
  - on the male arm:
    - "Seal record: intact";
    - `SHA256SUMS.txt` written before the last log lines;
    - `PYTHONUTF8` missing from the manifest;
    - `RESULT.md` missing the §3.5 columns that the registration promises.
- **V8 on lobe R ran the first live E2-III test in D1.** A BF-active fit in D1 was at risk under
  the registered band. Its GPU pair equals the reference bit for bit, so the test passed
  (`0c7a67b`).
- **Deterministic reruns were byte-identical.** Run 2 equals run 1 fit by fit on the synthetic
  step (28,665 keys per lobe, 0 fields differ). Lobe L's printed table and verdict line are
  identical. Block A's reproduction gate refitted the pinned store bit for bit.

## 3. What went wrong, and what it cost

- **The cp1252 stdout crash, after unsealing.**
  - Root cause: stdout was redirected to a file. Python on Windows then used cp1252, and A's
    quoted row carries a γ. The tests never ran the end of the real arm under a strict encoding.
  - Cost:
    - the seal was broken after review;
    - lobe L's verdict line and both block prints were seen before any output was written;
    - the real fits held in memory were lost;
    - a rerun of about 4 h 16 min;
    - a decision round on §7.4 (4) (below).
- **CC named the wrong script hash in `e07e347`'s note and message:** `1b952ca6…` against the
  true `290ecb56…`.
  - Cost: a ledger row. It also showed that the §3.3.1 (h) check had run with a script that
    differs from the registered one by one constant, which had to be clarified.
- **Two earlier CC errors, both recorded in A's ledger:**
  - "The reference is stale." This was a GPU subagent's claim, relayed by CC, and it came from a
    wrong key and cell order. It also survives in `validate_vs_cpu.py`'s docstring (GPU
    registration, row G-(6)).
  - "`reused_from_ko` is derived from `lam`; comparison redundant." This was revision 3.4's
    text. It cost a revision (3.4.1), which made the comparison required and the count a
    registered control.
- **The first pre-run was refused on a CRLF checkout.**
  - A Windows checkout writes the committed `bank.meta.json` with CRLF line endings, so its raw
    hash did not match the pin.
  - Cost: a refused start and a fix commit (`c8f0ea5`, pin by the LF sha256).
- **The worktree and a dirty tree got in each other's way.** GPU validation wrote into the
  repository while the pre-run requires a clean tree.
  - Cost: the two could not share the main worktree. Solved by running the pre-run from a
    separate worktree (`cs-prerun`, at `a0e16b6`).
- **A registered rule could not be kept as written.**
  - §7.4 (4) asks for a second run "from the same head" that carries S26's note. That note is a
    constant in the script, so setting it needs a new head.
  - Cost: run 2 waited from the first naming (chat, 2026-09-26 23:35 UTC) to Mike's word
    (2026-09-27 07:14 UTC).
    Option (a) was chosen: the note lives beside the outputs, not on the verdict line.
- **Ark's and Zcode's "one world of five" was carried to R/n without a recount.**
  - The count was taken on seen/n. On R/n the difference is larger.
  - Cost: the ledger entry was narrowed a second time, after the Q2 note.
- **Ark's at-risk counts used a band of 2·2^-23, not the registered 2^-23.**
  - Cost: a recount in arm revision 1.3 at both bands and three scopes. Ark's A count is
    reproduced by none of the three scopes.
- **CC did not tag the reviewers on the blind review's result until Mike asked.**
  - Cost: the review waited for the reviewers. (From CC's account; not checked against a file.)
- **Outputs made claims their writer cannot measure.**
  - `RESULT.md` and `summary.json` print "Seal record: intact" from a constant. A script cannot
    detect a seal broken by an earlier run.
  - Cost: a ledger row. The class fix is deferred to block B.
- **"Instrument weaker" was written into a registration before it was measured against the
  draw.**
  - Cost: a diagnostic note (Q2), a ledger narrowing, and a `RESULT.md` that is read with a
    correction beside it.

## 4. Lessons and rules adopted

- **Every redirected run gets `PYTHONUTF8=1`.** The script debts below make the code independent
  of this setting.
- **A counted claim states its scope and its denominator.** A count carried from one scope to
  another is recounted first.
- **"Not recomputed" is read from the run log**, not assumed from the code path.
- **Every census number carries its scope label** (every fit / `ko`-`ko1` / D1) and the band it
  was counted at.
- **Results, blind reviews and "what next" go to the reviewers with a tag.**
- **Callers come from the Orbit graph**, confirmed by grep. Worktrees are reindexed.
- **Long runs go in a separate clean worktree** whenever other jobs write into the repository.

## 5. Open items

- **Next.** This is the consensus of Ark and Zcode (2026-09-27 14:01–14:04 UTC). The order is for
  Mike to confirm.
  1. **Q1, block B on flyvis-65.** First comes a registration revision that carries:
     - A's pins after Amendment 1;
     - the script changes S1–S22;
     - the debts below.

     Block B does not test averaging, because it uses the same bank.
  2. **Check whether a bank-free unit for the limits can be computed.** It would re-express the
     pinned worlds, with no fit (Q2 note §7, item 4).
  3. **Q3, a weight bank, is deferred** for lack of power at 5 worlds per γ.
- **Debts for block B's script:**
  - UTF-8 reconfigured at the top of the script;
  - `log()` cannot kill a run;
  - real fits and verdict lines written to disk before any print;
  - an ASCII end-to-end rehearsal test;
  - the seal record read at run time;
  - the command's environment variables in the manifest;
  - `SHA256SUMS.txt` written last;
  - the S0 sentence carries its condition;
  - §3.5's columns in `RESULT.md`;
  - the synthetic U-rule paragraph follows each arm's own U reading;
  - no duplicate `auc_N1` column;
  - every filter states its denominator;
  - fenced drafts inside a registration are marked.
- **The GPU instrument.** Two things are pending:
  - a registration revision that carries the V1 stamp and the composition digest;
  - scope labels on every census number.
- **Johnny left the session** (context limit). He reads the committed revisions in a new session.
- **Question (ii)** stays paused under ADR-005. The joint reading's caution says the male G does
  not by itself exclude averaging, and block B does not test it.
- **Backlog:** `BLOCK-B-ON-FLYVIS-65-WAITS-ON-A-REGISTRATION-REVISION-THAT-CARRIES-THE-MALE-ARMS-DEBTS`,
  `KNOCK-OUT-AND-REGROW-TESTS-WHETHER-THE-RULE-GENERATES-A-BLOCK-IT-WAS-NOT-SHOWN`, and
  `A-BATCHED-GPU-INSTRUMENT-CAN-RUN-THE-C6-FITS-IN-MINUTES-BUT-IS-A-SEPARATE-INSTRUMENT`.

## 6. Commits

`8a514fa`, `52eb381`, `1d6bb9e`, `e6bba28`, `cde61d4`, `ea8fe27`, `74db080`, `74de040`, `1ed55ec`,
`d6e3759`, `8591491`, `cdbde9e`, `bdd250c`, `2af21e5`, `476cf9b`, `e0a3cd7`, `5860619`, `f82d442`,
`a6761e2`, `fedeec5`, `345acf2`, `5983385`, `ec5cbc0`, `e2fab47`, `ee380a1`, `c8f0ea5`, `a0e16b6`,
`1ad6155`, `e50bf74`, `af11d31`, `0c7a67b`, `70e759e`, `8531c6d` (merge), `6fff1e4`, `01d2d05`,
`e07e347`, `0286ae1`, `63b0366`, `86d7288`, `0914962`, `46365e7`. The session-close commit adds
this file and the backlog and roadmap updates.
