# C6: the exam a regenerating rule must pass

This directory holds the exam of `docs/plans/2026-09-23-c6-control-specification.md`, with
Amendments 1 and 2. The acceptance criteria are in
`docs/plans/2026-09-23-c6-amendment-acceptance.md`. **Three rules have been registered; two of them have run.**
Rule #1 (`first_rule_k12`) failed. Rule #2 stopped at its gates and never reached this harness
(`docs/notes/2026-09-23-second-rule-stopped-at-gates.md`). Rule #2.1 passed gates and ran once:
verdict FAIL, on the offset field only — existence passed P1, P3 and P4
(`docs/notes/2026-09-23-rule-2-1-c6-what-it-showed.md`). See
`results/genome/c6/rule_runs/first_rule_k12/RESULT.md` for the rule #1 record.

| file | what it is |
|---|---|
| `make_folds.py`, `folds.csv`, `folds.meta.json` | the 10 folds over the 65 × 65 grid, committed before any rule (A2) |
| `harness.py` | the exam, its nulls and opponents, the planted-rule acceptance suite, and the plug-in interface for a rule (in its docstring) |
| `decoders/*.py` | the charged decode programs of the built-in predictors (A5) |
| `harness_controls.json` | every score of every control and acceptance run, with the sha256 of the harness, spec, acceptance file, folds and decoders |
| `HARNESS-CONTROLS.md` | what the controls showed, and whether the exam behaves as designed |

**Offset sets are scored exactly, not up to symmetry (A21).**

- The exam compares offset sets as exact sets of `(du, dv)` offsets, with no canonicalisation
  under the 12 symmetries of the hex lattice. On the compiled bank that is 225 distinct exact
  sets, and 327 once counts are included.
- The regularity measure (`results/genome/bank/REGULARITY-READING.md` §3) canonicalises, to 144
  shapes.
- So the two artefacts measure different objects. A rule that gets a shape right only up to
  rotation scores as wrong here.

**What the budget arm is for** (Ark, genome track, 2026-09-23 21:35 and 21:44 UTC, translated
from Russian):

> "The Clune threshold here is defended by P1/P2 against N0/N1/N_EB/BF. The budget arm defends
> something else: the rule must not be a partial download of the answer. In the 7.7–9.5 kbit
> band the verdict rests on N1 and the shuffle, not on storage."

R1's recorded failure and that narrow band are one fact: honest storage of this matrix is a weak
predictor at any length we can afford. Its home is
`docs/plans/2026-09-23-c6-amendment-acceptance-2.md` §2.

**Three different "18"s.**

- **k90 = 18** is a *component count*: the singular components of L = ln(1 + N) that hold 90 %
  of its energy.
- **H18** is a *set of types*: the top 18 types by leverage at rank k90.
- **U18** is a *set of types*: the top 18 types by the fraction of their cells left unmoved by
  the shuffles.
- The set size 18 in H18 and U18 was borrowed from k90.
- The harness's L equals `regularity.py`'s L exactly: 0 of 4,225 cells differ.

Run (CPU, from the repository root):
`tools/.venv/Scripts/python.exe results/genome/c6/harness.py --controls`
