# Handover — for the session that starts after 2026-09-24

**Written:** 2026-09-24 UTC, by CC, on Mike's word (DPC Research group, 2026-09-24 10:04 UTC:
"do 3, and we will do 1 in a new session", translated from Russian). Item 1 is question (ii) below.
**Audience:** whoever opens this repository next, human or agent.

**This file carries no result value.** Where a finding is numerical, the file that holds it is
named. It follows [`2026-09-23-next-session-handover.md`](2026-09-23-next-session-handover.md) and
does not replace it.

---

## 1. What was done on 2026-09-23 and 2026-09-24, in order

All committed and pushed; each step was registered before it was run, and each registration was
reviewed by Ark, Johnny and Zcode in the DPC Research group before the run.

1. **Rule #2.1 on C6: one run, verdict FAIL on the offset field only.** Outcome note:
   [`docs/notes/2026-09-23-rule-2-1-c6-what-it-showed.md`](../notes/2026-09-23-rule-2-1-c6-what-it-showed.md).
2. **BF_1 alone on P3** (is the separation carried by the rank-1 term?): branch A. Registration
   [`docs/plans/2026-09-24-bf1-p3-registration.md`](../plans/2026-09-24-bf1-p3-registration.md);
   outcome [`docs/notes/2026-09-24-bf1-p3-what-it-showed.md`](../notes/2026-09-24-bf1-p3-what-it-showed.md).
3. **The second brain (FlyWire right optic lobe), question (i) "is the structure there?".** A
   30-type bank built from FlyWire v783 by a registered procedure, run against its own shuffles,
   with flyvis restricted to the same 30 types as the control arm. Registration
   [`docs/plans/2026-09-24-flywire-bf-p3-registration.md`](../plans/2026-09-24-flywire-bf-p3-registration.md)
   (§3a the build as implemented, §3b bank sensitivity); results `results/genome/c6/checks/flywire_bf_p3/`
   and `flywire_sensitivity/`; outcome and review
   [`docs/notes/2026-09-24-flywire-p3-what-it-showed.md`](../notes/2026-09-24-flywire-p3-what-it-showed.md).
   Read that note's §1 and §3 before anything else: the headline row is a registered flag, and the
   note says why.
4. **Status documents brought up to date** for an external reviewer: `README.md`,
   `results/genome/c6/README.md`, the grammar-track next-steps table, the S2 design's order of work.

## 2. The next task: question (ii), transfer

Mike's choice (10:04 UTC): in a new session. Question: is the structure found in one brain the
**same** structure in the other? Points already raised in the chat that a registration must settle
before any value exists:

- **Direction and object.** Fit BF_r on one 30-type bank, score it on the other, on the pairs the
  two banks share. Which direction, or both, and which ranks.
- **Its own null** (Ark): a fit on a *shuffled* source bank, scored on the same target. Without it,
  "transfer worked" means nothing.
- **Headline rank.** In question (i) the registered headline, r = 1, fell exactly where the two
  arms' rank profiles crossed (outcome note §4). Choose and justify the headline with that in mind.
- **Lambda readings for every branch.** Question (i)'s registration gave lambda readings for
  branch B only, and the flag came out as a C (outcome note §3). Write readings for A, B and C.
- **Known differences between the banks,** measured before any BF value: support (FlyWire has no
  offsets beyond 2), density, the flyvis hand edits on T4 targets (registration §3b of question (i)).
  Johnny reads the opposite rank profiles as evidence against "the same structure"; that reading
  is recorded, not tested.

## 3. How this work has been run (keep it)

- **Registration before build, build before run, run once.** Every choice fixed in writing first;
  changes after review are amendments committed before the step they govern.
- **CC checks the logic of every registration a subagent drafts before it is committed**, and the
  reviewers read the committed text. This caught, before any value: an arm cut from the wrong bank,
  workers that would have scored the wrong bank, an inverted guard, wrong repository paths, and a
  builder with no build in it.
- **`tools/.venv` is pinned** (digest `94f7f483…`, night 6 gate 8). Anything that needs another
  package, such as `pyarrow` for the FlyWire feather file, runs in a throwaway environment:
  `uv run --no-project --with pyarrow --with numpy --with pandas python …`.
- **Data outside the repository.** `connectome-seed-data/FlyWire/` (see its `SOURCE.md`). The column
  file is CC BY-NC, so the built banks stay in `connectome-seed-data/FlyWire/derived/`; only code,
  manifests with hashes, and aggregate results are committed.
- After every commit, regenerate `docs/blind-author-exclusions.txt` with
  `tools/contamination_scan.py` and commit it if it changed.

## 4. Open items, not blocking

- The external-review prompt drafted by Ark in the chat needs three edits agreed there: add the
  bank-origin note to the reading route, drop the unverified "NeurIPS 2025" reference, add the
  `bf1_p3.py` quick check.
- `results/genome/c6/rules/second_rule/post_run.py` line 54 still has `ROOT = C6.parents[1]`
  (rule #2 never ran on C6, so it never mattered).
- Twenty tracked lines mention `chat/` by name; none is a link (Ark's recount).
