# C6: the exam a regenerating rule must pass

This directory holds the exam of `docs/plans/2026-09-23-c6-control-specification.md`, with
Amendments 1 and 2. The acceptance criteria are in
`docs/plans/2026-09-23-c6-amendment-acceptance.md`. **No rule is registered, and none has been
run.**

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

Run (CPU, from the repository root):
`tools/.venv/Scripts/python.exe results/genome/c6/harness.py --controls`
