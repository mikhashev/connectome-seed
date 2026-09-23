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

### Run 1 (the single run): completed, not a crash

- Started 2026-09-23 19:44:52 UTC (shell clock), at commit `e243a41` on a clean tree
  (`tree_dirty_under_c6_or_plans: False` in the stamp). Ended 19:54:38 UTC. Harness wall time
  585.1 s with 30 workers (precompute: 3,086 independent fits in 573 s). Exit code 0.
- The command above, exactly, with `SECOND_RULE_SPREAD_DIR` set as shown. 1,341 spread files written.
- No crash, no exception from `harness.py` or from the rule's code. This run is the verdict;
  no other run of rule #2.1 on C6 is made (registration §4 and §9).
- Verdict line, verbatim: **C6 verdict for second_rule_v21_r1 (k = 10 starts, r = 1): FAIL -- copy
  or marginal; below threshold for this family; family fits anything**
- The record (`result.json`, `run_info.json`, `RESULT.md`, `spread/`) is committed as the harness
  wrote it, before `post_run.py` runs.

## Post-run (`rules/second_rule_v21/post_run.py`; not a C6 run, no verdict)

- First execution, 2026-09-23 19:55:49 UTC at `6baff38`: the spread-log check ran, then every
  refit worker failed to load the rule (FileNotFoundError on `results/results/genome/...`), because
  the script's `ROOT` was `results/`, not the repository root. Nothing it wrote was kept or
  committed. Fixed in `fb24d17` (one line, no computation changed; self-test passes).
- Second execution, 19:56:58–19:57:49 UTC at `fb24d17`: completed; every reproduction check holds.
  Its outputs are committed as written.
