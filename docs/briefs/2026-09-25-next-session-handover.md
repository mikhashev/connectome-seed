# Handover — for the session that starts after 2026-09-25

**Written:** 2026-09-25 UTC, by CC, on Mike's word (DPC Research group, 2026-09-25 09:40 UTC:
"let's do the retrospective and close the session; in the new session we do option A", translated
from Russian). **Audience:** whoever opens this repository next, human or agent.

**This file carries no result value.** Where a finding is numerical, the file that holds it is
named. It follows [`2026-09-24-next-session-handover.md`](2026-09-24-next-session-handover.md);
the retrospective of this session is
[`docs/retrospectives/2026-09-25-session-close.md`](../retrospectives/2026-09-25-session-close.md).

---

## 1. Where things stand

- **ADR-005 (backward before forward)** is amended: decision 1 is done, Q1–Q3 are answered, and
  the knockout bank is chosen. See [ADR-005](../decisions/005-backward-before-forward.md),
  § Amendment 2026-09-24.
- **The column test is done.** It ran once. The result is
  [`results/genome/c6/checks/flywire_column_test/RESULT.md`](../../results/genome/c6/checks/flywire_column_test/RESULT.md),
  commit `9705ef1`, with its label and every number. Question (ii) stays **paused** until
  "knock out and regrow" is registered (Mike, 2026-09-24 20:13 UTC).
- **Knock out and regrow** is where the session stopped:
  - **Block A** is chosen: the ON/OFF inputs × T4/T5, 64 cells. See
    [`docs/notes/2026-09-25-knockout-block-candidates.md`](../notes/2026-09-25-knockout-block-candidates.md).
  - **Primary bank:** flyvis-65.
  - **Animal control:** Janelia male CNS v1.0. Its bank needs its own registered builder.
  - **Registration:** [`docs/plans/2026-09-24-knockout-regrow-registration.md`](../plans/2026-09-24-knockout-regrow-registration.md),
    **revision 3.1**. The reviewers have read revision 3 (Ark, Johnny, Zcode, 2026-09-25
    09:32–09:34 UTC); revision 3.1 applies their pass and **has not been reviewed yet**.
  - **Script:** [`results/genome/c6/checks/knockout_regrow.py`](../../results/genome/c6/checks/knockout_regrow.py),
    revision 3.1.
  - Both files are committed as an **unreviewed draft** (on Mike's word after the
    session close). The registration's header says so.
  - The pre-run synthetic outputs (45 worlds) are in
    `connectome-seed-data/knockout_regrow/synthetic_rev3_prerun/`, with `SHA256SUMS.txt`.
    Revision 3.1 requires the registered run to reproduce that table.
  - **Nothing has been run on the real block.** Mike, 2026-09-25 09:35 UTC: "don't launch any runs
    for now".

## 2. The next session: option A (Mike, 2026-09-25 09:40 UTC)

Option A as posted in the chat at 09:39 UTC:

1. **The reviewers read revision 3.1.** Ark, Johnny and Zcode check the three limits (γ\*_P, γ_R,
   family), the per-γ fractions, U as the threshold's signature, λ on the verdict line, and the
   reproduction stop. Four points are the subagent's own choices and need a vote:
   - the reproduction is a byte-for-byte stop on `synthetic_worlds.csv`;
   - the transition band is defined as [γ\*_P, γ_R);
   - every predictor's limit uses p_P ≤ 0.01;
   - a U caused only by `ceiling_block` < 0.90 is a failed fit.

   CC's own concern: a byte-for-byte stop can fail for benign reasons (float formatting, BLAS
   threading). Comparing labels and counts exactly, and numbers within a tolerance, may be the
   safer reading. Put it to the vote.
2. **The real run happens on the CPU**, with the registered instrument and on Mike's word only.
   It uses one manifest from a clean committed tree, recomputes the synthetic worlds (about 2 h
   10 min on 30 workers) and then runs the real block (about 3 min).
3. **In parallel, a GPU instrument.** A separate instrument that batches the thousands of
   same-shaped fits (shuffles × predictors × starts) into one tensor. It is validated against the
   CPU instrument on the saved 45 worlds (`raw_fits.json.gz` is the reference). Later work runs on
   it: the male-CNS control and the next registrations. Two constraints:
   - it is **not** a rewrite of the registered CPU instrument (Mike, 09:34 UTC);
   - VRAM is mostly held by `llama-server` (Ark's reading: 28.6 of 32.6 GB), so freeing it is
     Mike's call.
4. **The male-CNS builder registration.** Its first open parameter is the pair threshold. The
   specification points are in the backlog entry
   `THE-MALE-CNS-BANK-NEEDS-A-REGISTERED-BUILDER-WITH-ITS-PAIR-THRESHOLD-FIXED-BEFORE-DATA`.

## 3. How this work has been run (keep it)

Everything in the 2026-09-24 handover § 3 still holds. Added this session:

- **Synthetic worlds before commit** (the D11 practice). In one day they caught four design
  defects before any data:
  - the column test's non-monotone Q3/P95 rule;
  - its single-draw anchors;
  - a stop row that forbade a correct reading;
  - a G branch that could not separate "absent" from "weaker than the instrument".
- **Every requirement row is checked for "can the design pass this by construction?"** before
  it is written. A 5-of-5 requirement at a noisy cut fails by chance.
- **Raw outputs go to `connectome-seed-data/`** with `SHA256SUMS.txt` before review, so that the
  reviewers can check machine against prose.
- **Chat:** no @-tags except when a review is needed (Mike, 2026-09-24 20:59 UTC). Every message
  is markdown and is sent from the per-tag outbox.
- **Ask for GPU before an instrument is ordered.** This session's knockout script was ordered on
  the CPU harness without asking; Mike's question at 09:29 UTC exposed it.

## 4. Open items, not blocking

- The column-test registration still has two text items for a revision 2.4: the S2 "overlap" is
  intersection over the smaller set (Johnny), and Ark's text additions.
- Hemibrain (`connectome-seed-data/Hemibrain/`) is an unpacked archive only and is not in any
  plan (Johnny; Zcode: its optic lobe is incomplete).
- The 2026-09-24 handover § 4 items are unchanged.
