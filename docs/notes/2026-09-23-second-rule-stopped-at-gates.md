# Rule #2 stopped at its gates; no C6 run

**Written:** 2026-09-23 UTC, by CC, on Mike's choice of option A (DPC Research group chat,
16:26 UTC: "A, then B"), which Ark and Johnny also supported (16:28 and 16:31 UTC).

## What happened

- Rule #2 was registered in [`docs/plans/2026-09-23-second-rule-proposal.md`](../plans/2026-09-23-second-rule-proposal.md)
  (commit `c3f996d`). It was implemented at `dd4dc92`.
- Its seven gates on synthetic banks were run once (`e7e31fb`,
  `results/genome/c6/rules/second_rule/gates.json`). Two failed:
  - **G-e+:** on GB1 the rule beat BF_1 on existence in 8 of 10 folds, where 9 were needed;
  - **G-o0:** on GB0 the rule minus N_EB on offset sets was −0.01996, outside the ±0.010 band.
- The proposal's §2.5 says a failed gate stops the work. **Rule #2 is not run on C6.** No fit, score
  or held-out number exists for it on the real bank, and the harness has not been invoked with
  `--rule` for it.

## What this costs, recorded rather than hidden (Ark and Johnny)

The registered predictions ([`2026-09-23-first-rule-failure-predictions.md`](../plans/2026-09-23-first-rule-failure-predictions.md),
with the [addendum](2026-09-23-predictions-addendum-after-tau.md)) were written for rule #2's C6
run. **All of them stay unrun.** That includes P-J3, the one item that directly contradicted the
rule author's prior. A later rule is a new registration and needs new predictions. Items carry
over only where that registration says so explicitly.

## Why not run anyway

A failed positive control makes the exam unreadable. If the rule cannot find a signal planted on
purpose, its failure on the real bank cannot be told apart from the rule being unable to see. This
is the same precedent as rule #1's stalled search, which was fixed before its run.

## What comes next (B, not yet a plan)

Mike asked (16:41 UTC) to find out why the gates fail and how they can be made to work. A
diagnosis on synthetic banks only is running. For each failed gate it separates a fault of the
**gate** (miscalibrated or underpowered: even an oracle that knows the planted truth would fail it)
from a fault of the **rule** (too weak or too constrained). Its output goes to
`results/genome/c6/rules/second_rule/DIAGNOSIS.md`. It reserves a range of fresh synthetic seeds
for any future re-gate and does not look at them.

Johnny's condition on B (16:28 UTC): a new registration must name a fix for G-e+. Changing only the
offset library cap would leave G-e+ failing, and the registered 9/10 bar cannot be lowered after
the failure.
