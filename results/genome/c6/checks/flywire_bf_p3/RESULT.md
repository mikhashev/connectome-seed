# BF_r on FlyWire-30 and flyvis-30: P3 against each bank's own 99 shuffles

Registration: `docs/plans/2026-09-24-flywire-bf-p3-registration.md`. Machine check (unpatched wrapper, flyvis full bank): True (difference 0.00e+00).

**Headline, r = 1:** FlyWire-30 A: BF_r separates; flyvis-30 C: in between. **Joint reading:** FlyWire-30 separates, flyvis-30 does not: an unexpected direction -- read as a flag to re-examine both fits before drawing a substantive conclusion. **Label (registration section 3b):** support difference real, reading stands.

| arm | r | real margin | shuffled mean | shuffled max | n >= real | p | p < 0.0125 | gap | real folds at lambda=100 | shuffle folds at lambda=100 | branch | negative reading |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| flywire30 | 1 | +0.03431 | -0.00116 | +0.00412 | 0 | 0.01 | True | +0.03019 | 0.00 | 0.67 | A: BF_r separates | - |
| flywire30 | 2 | +0.01413 | -0.00075 | +0.00540 | 0 | 0.01 | True | +0.00873 | 0.00 | 0.67 | A: BF_r separates | - |
| flywire30 | 3 | +0.01137 | -0.00075 | +0.00465 | 0 | 0.01 | True | +0.00672 | 0.00 | 0.67 | A: BF_r separates | - |
| flywire30 | 4 | +0.00810 | -0.00076 | +0.00464 | 0 | 0.01 | True | +0.00346 | 0.00 | 0.67 | A: BF_r separates | - |
| flyvis30 | 1 | +0.00928 | -0.00062 | +0.00930 | 1 | 0.02 | False | -0.00001 | 0.00 | 0.72 | C: in between | - |
| flyvis30 | 2 | +0.01796 | -0.00107 | +0.00925 | 0 | 0.01 | True | +0.00871 | 0.00 | 0.72 | A: BF_r separates | - |
| flyvis30 | 3 | +0.02143 | -0.00130 | +0.00751 | 0 | 0.01 | True | +0.01392 | 0.00 | 0.70 | A: BF_r separates | - |
| flyvis30 | 4 | +0.02794 | -0.00116 | +0.00693 | 0 | 0.01 | True | +0.02101 | 0.00 | 0.70 | A: BF_r separates | - |

**Also (registration section 5a, printed, not a branch):** the full-65 flyvis BF_1 was 'A: BF_1 separates', but flyvis-30 is not A at r = 1: the separating structure does not live in the 30 column-assigned types alone; some of the 35 dropped types carry it.

## Joint reading per rank

| r | FlyWire-30 | flyvis-30 | reading |
|---|---|---|---|
| 1 | A: BF_r separates | C: in between | FlyWire-30 separates, flyvis-30 does not: an unexpected direction -- read as a flag to re-examine both fits before drawing a substantive conclusion. |
| 2 | A: BF_r separates | A: BF_r separates | both banks separate: the pattern is present in the second brain. |
| 3 | A: BF_r separates | A: BF_r separates | both banks separate: the pattern is present in the second brain. |
| 4 | A: BF_r separates | A: BF_r separates | both banks separate: the pattern is present in the second brain. |

flyvis30 is its own run (30 of 65 types, its own fold subset, its own shuffles), not a repeat or a subset of the full-65 BF_1 result in results/genome/c6/checks/bf1_p3/summary.json (real margin 0.028150051052145946).

git_head=d12415a967ca062db8873a606af3e196e9998248, runtime=2028.9s.
