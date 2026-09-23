# Rule #2.1 C6 run: attempts file

The run's attempts file (reading [R17] of `rules/second_rule/README.md`, carried to rule #2.1):
first the timing-cap decision, then every run and every crashed run. The harness does not write
or overwrite this file.

## Timing cap (rule #2 proposal §1; unchanged by the rule #2.1 registration §1.3)

Measured 2026-09-23, 19:44:21–19:44:29 UTC, at commit `fbdb3e9`, **before any real-bank fit** of
rule #2.1. Script: `rules/second_rule_v21/timing.py 30`; record: `rules/second_rule_v21/timing_k10.json`.

- **What was timed:** the rule's fits of folds 0–9 of **shuffled bank 0** at k = 10, ten at once,
  one per process. No decode and no score of any kind.
- `fit.py` LF sha256 `92eb6ab1…` (the registered learner); `harness.py` LF sha256 `6fc80952…`.
- Machine: 32 logical CPUs. The run's worker count: **30**.

| quantity | value |
|---|---|
| mean seconds per fit | 6.665 |
| largest seconds per fit | 6.985 |
| wall time of the ten fits | 7.62 s |
| rule fits in the run | 1,341 |
| projection | 6.665 s × 1,341 / 30 = **0.083 hours** (about 5 minutes) |
| cap | 12 hours |

**Decision: k = 10 starts for every fit of the run** (projection ≤ 12 hours). This agrees with
Mike's "10 стартов" (DPC Research group chat, 2026-09-23 19:41 UTC); the registered rule decides it.

## Runs

Mike's word for the single C6 run: "запускаем 1 и 2" (DPC Research group chat, 2026-09-23
19:41 UTC). Planned command, from the repository root, on a clean tree:

    SECOND_RULE_SPREAD_DIR=results/genome/c6/rule_runs/second_rule_v21_r1/spread \
      tools/.venv/Scripts/python.exe results/genome/c6/harness.py \
      --rule results/genome/c6/rules/second_rule_v21/fit.py --starts 10 --workers 30

Output directory: the harness's default, `rule_runs/second_rule_v21_r1/`.

No run has been made at the time of this commit.
