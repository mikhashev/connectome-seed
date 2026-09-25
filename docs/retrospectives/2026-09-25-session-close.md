# Retrospective — session of 2026-09-24 18:00 UTC → 2026-09-25 09:41 UTC

**Written by:** CC, on Mike's word (DPC Research group, 2026-09-25 09:40 UTC: "let's do the
retrospective and close the session", translated from Russian). **Audience:** Mike and the
reviewers (Ark, Johnny, Zcode).

**This file carries no result value.** Where a finding is numerical, the file that holds it is
named. Structural counts, dates, commit hashes and instrument timings are written plainly.

---

## 1. What the session produced

- **The column test, from registration to result.**
  - Registration revision 2.2 (`f568691`), then 2.3 with the script (`b3f41ed`).
  - It went through three review rounds (Ark, Johnny, Zcode).
  - It ran once. Aggregates only are committed (`9705ef1`); the per-column files stay in
    `connectome-seed-data` (CC BY-NC).
  - Zcode checked RESULT.md against `summary.json`. A CC subagent recomputed the §3.9 descriptors
    independently, without the test's code. Both checks agreed.
- **ADR-005 amended** (`fb3c32e`). Decision 1 is done and Q1–Q3 are answered. Question (ii) stays
  paused (Mike, 20:13 UTC).
- **Knock out and regrow.**
  - Block A chosen by name before data, with the checkerboard counted independently by three
    reviewers (`10b704e`).
  - The bank decided: flyvis-65 primary, male CNS as the animal control, FlyWire-30 as provenance
    (Mike, 20:39 UTC).
  - The registration reached revision 3.1 and the script was written.
  - Synthetic runs:
    - an 85-minute run of revision 2, which stopped on the M worlds;
    - a 44-minute dense-grid run of revision 3, which passed.

    Outputs are in `connectome-seed-data/knockout_regrow/synthetic_rev3_prerun/`.
  - No real block cell was read.
- **The male CNS was surveyed** by names and presence (type map, block inferability). The
  reviewers corrected the map: R7/R8 and TmY9 come from `flywireType`. The builder specification
  is recorded as a backlog entry.
- **Board and roadmap were kept current** through `build.py`:
  - the column-test entry closed;
  - the knockout entry appended at each milestone;
  - the male-CNS builder entry added;
  - the ADR-005 paragraph added to the roadmap.

## 2. What went well

- **Synthetic worlds before data caught four defects** before any real value existed:
  - the column test's non-monotone reading rule, where Ark's own table was wrong and he withdrew
    it;
  - its single-draw calibration anchors;
  - the knockout's M-world stop, which forbade a correct reading;
  - a G branch that could not tell absence from weakness, because λ selection acts as a switch
    (read from `harness.py:727-728` by Johnny).
- **Self-corrections were recorded as such:**
  - Ark on the Q3/P95 table and on "λ survives or zeroes";
  - Johnny on "U is unreachable", where his falsifier fired against him;
  - Zcode on "seeds do not overlap";
  - CC on the male-CNS threshold wording and the R7/R8 and TmY9 guesses.
- **Machine-against-prose checks** became routine: raw outputs go to a shared path with checksums
  before review.

## 3. What went wrong, and what changes

- **The knockout script was ordered on the CPU harness without asking about GPU.** Mike asked at
  09:29 UTC. The saving is large only with a batched GPU instrument, and that is a separate
  instrument (Mike, 09:34). **Change:** ask about GPU before any instrument is ordered. The next
  session builds the GPU instrument in parallel (option A).
- **Requirement rows were written that the design could not pass**: "all 5 Nf worlds read G",
  "M never reads R", and a D14 rule that lost leg S at the first degenerate shuffle. CC flagged
  them at 21:10 UTC, before the run. **Change:** every requirement row is checked for "can this
  pass by construction?" before it is written.
- **Wording that did not say how a number was computed.**
  - "Mean ≥ 1" on the male CNS: the divisor was not stated (Zcode).
  - γ\* was named as a detection limit but computed on the weak leg (Johnny).

  This is the same class as the rest of the day. **Change:** every threshold is written with its
  formula.
- **A question from Mike went unanswered** (#173, the GPU question). It was answered only after
  he asked again. **Change:** answer the owner's direct question first, before summarising the
  reviewers.
- **The registration and the script were edited out of order** (the text 41 minutes after the
  script; Johnny). **Change:** the registered run starts from a clean committed tree in one
  manifest, and revision 3.1 requires it.

## 4. Commits

`f568691`, `941ab83`, `b3f41ed`, `9705ef1`, `1a26939`, `3c5c037`, `10b704e`, `0f14304`, `fb3c32e`,
`2be6fe1`, `ea60011`. The session-close commit adds this file and the handover. The knockout
registration and its script stay untracked until revision 3.1 is reviewed.

## 5. Handover

[`docs/briefs/2026-09-25-next-session-handover.md`](../briefs/2026-09-25-next-session-handover.md).
