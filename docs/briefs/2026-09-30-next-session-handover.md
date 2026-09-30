# Handover — for the session that starts after 2026-09-30

**Written:** 2026-09-30 UTC, by CC, on Mike's word (DPC Research group, 2026-09-30 16:53 UTC:
"update the documentation and the tasks; write the plan for the next session here; I suggest we
continue in a new one", translated from Russian). **Audience:** whoever opens this repository
next, human or agent.

**This file carries no result value.** Where a finding is numerical, the file that holds it is
named. It follows [`2026-09-25-next-session-handover.md`](2026-09-25-next-session-handover.md). The
tasks live in [`backlog.md`](../../backlog.md), which is edited only through the shared backlog tool.

---

## 1. Standing rules set by the owner in this session

- **No run of any length starts without Mike's yes.** This applies to seconds-long fits and
  recomputations too, and to runs by subagents. Give the time and resources estimate with the
  question. (2026-09-30 15:50 UTC; replaces the earlier 30-minute line.)
- **Mike launches every blind review himself, in a separate Claude Code session.** CC writes the
  brief and keeps it outside the repo and outside its own scratch folder. CC does not spawn the
  reviewer. (2026-09-30 15:54 UTC.)
- **No result goes into a commit subject, a branch name or a run-folder name before the blind
  review.** (Ark and Zcode, 2026-09-30 15:47–15:49 UTC; it was broken once, in 69d44c0.)
- **Run scripts record `git rev-parse HEAD` and an empty `git status --porcelain`** in their
  outputs, as `symmetric_lambda_pair.py` does.
- **A blind review is stored verbatim** (`BLIND_REVIEW_raw.md`). A condensation by CC is marked as
  one.
- **Windows:** set `PYTHONUTF8=1` for every Python run. Use `tools/.venv/Scripts/python.exe`.

## 2. What was done (2026-09-29 → 2026-09-30)

| work | carrier | review |
|---|---|---|
| Failed-fit branch calibration | [CALIBRATION.md](../../results/genome/c6/checks/failed_fit_calibration/CALIBRATION.md) | blind review in the folder |
| GPU extension X validation | `results/genome/c6/gpu_instrument/validation/` | reviewers' four yes; the revision text is not written yet |
| Natural fit-failure replication | [REPLICATION.md](../../results/genome/c6/checks/natural_fit_failure_replication/REPLICATION.md), [READING_NOTES](../../results/genome/c6/checks/natural_fit_failure_replication/READING_NOTES.md) | blind review in the folder |
| (iii-b) diagnostic, closed as a diagnostic | [`docs/prereg-scripts/2026-09-29-iiib-diagnostic/`](../prereg-scripts/2026-09-29-iiib-diagnostic/) | — |
| Rule #2.1 on the real block B at a fixed λ = 1 | [block_b_ceil1/RESULT.md](../../results/genome/c6/checks/block_b_ceil1/RESULT.md) | independent recomputation, **not blind** ([BLIND_REVIEW.md](../../results/genome/c6/checks/block_b_ceil1/BLIND_REVIEW.md)) |
| The symmetric λ pair (A at λ 100; B's label with the block λ at 1) | [symmetric_lambda_pair/RESULT.md](../../results/genome/c6/checks/symmetric_lambda_pair/RESULT.md) | owner's blind review: follows ([BLIND_REVIEW_raw.md](../../results/genome/c6/checks/symmetric_lambda_pair/BLIND_REVIEW_raw.md)) |
| README to one screen; GLOSSARY "Read these first" and section 11; origin moved | [README.md](../../README.md), [GLOSSARY.md](../../GLOSSARY.md), [origin](../history/2026-09-13-origin.md) | Ark, Warren, Zcode |

The reading lines beside the two blocks' verdicts are in
[block A notes](../../results/genome/c6/checks/knockout_regrow/READING_NOTES.md) §1 and
[block B notes](../../results/genome/c6/checks/knockout_regrow_block_b/READING_NOTES.md) §10–§11.
No registered label was edited.

## 3. What it means, in plain words

- **The gate reads the λ, not the block.** Both blocks pass when their block-only fit is at λ = 1.
  Both fail when it is at λ = 100. At λ = 100 the interaction term is switched off, and the gate
  sees only the additive part.
- **Three regimes, all measured:**
  - Additive part null: the all-ties floor. Block A: its marginals are balanced, so its fall at
    λ = 100 is forced by arithmetic.
  - Additive part moderate: a fail. Block B.
  - Additive part alone at or above the cut: a pass that is not about the interaction. The
    board-41 class, with 18 natural instances.
- **Not shown:**
  - how the fitter behaves on A, and the fold-selection mechanism on A;
  - B's full verdict at λ = 1. The knockout legs were already at λ = 1. Leg S rests on shuffle
    fits that mostly chose 100. BF_3/BF_4's p_P come from λ = 3 fits. The G clause reads none of
    them.
- **At λ = 1 the blocks still differ in number, not in label.** Block A reaches the maximum; block
  B is close to the cut. See the carriers.

## 4. Plan for the next session, in order

1. **Collapsed-λ verdict class declaration (text, no run).** Rewrite the draft
   [`docs/plans/2026-09-29-collapsed-lambda-verdict-class-registration.md`](../plans/2026-09-29-collapsed-lambda-verdict-class-registration.md)
   (rev 1, `1e9fc9a`). It must:
   - define the class by λ_c = 100, with u·v = 0 as its consequence;
   - carry the three-regime table with both real blocks;
   - carry the population figure from the replication notes;
   - state that the verdict mixes λ across clauses;
   - state the "not shown" items of section 3.

   Review in chat, then commit. It changes no label; it adds reading lines.
2. **GPU instrument revision registering extension X (text).** It covers:
   - the VX6 help text (`ext_compare.py:291-292`);
   - the prose drift in `ext_gpu_stage.py:23` (12,526 → 12,550);
   - the stale "Status (2026-09-26): not reviewed" line in `gpu_instrument/README.md`. That README
     is hashed by `instrument.py`, so the line changes only through the revision.
3. **Process hygiene (small code change, with tests).** Run scripts capture their own stdout into
   the output folder. `run.log` is currently captured outside and copied in: it has CRLF endings,
   it is not gitignored, and inside the repo it would trip the porcelain check.
4. **Decision for Mike, only if the declaration needs it:** B's full verdict at a fixed λ = 1, with
   the knockout, full and shuffle legs. It takes more than 30 minutes.

## 5. How to start

- Read the DPC Research chat with `--last 10` or more, never less.
- Read this file, then the backlog entries it names.
- Send chat messages from the per-tag outbox with `--as CC_windows`, as markdown.
- Use Orbit for the call graph. Pass every standing rule of section 1 to every subagent.
