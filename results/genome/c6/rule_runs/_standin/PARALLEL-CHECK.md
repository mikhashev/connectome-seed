# Stand-in check of the harness's rule path

**The stand-in** (`fit.py`) is the planted family PR with PL1's class vector, run on the real
bank. The controls already ran exactly this object as criterion N2. It is **not** a candidate
rule, and it exposes nothing new. Harness sha256 (LF-normalised): `c01cd9eb02481132a0d254ffe63e90a655e79979112d620207ce39c75bdfbd86`.

## 1. Parallel equals serial, byte for byte (k = 3 starts)

| run | workers | fits precomputed | precompute time | sha256 of `result.json` |
|---|---|---|---|---|
| parallel | 30 | 3,086 | 19 s | `9eca69f5b2b949929cf8b4452fa14b047cee65ef6fdbd2c75c1a21043605fc02` |
| serial | 1 | 3,086 | 69 s | `9eca69f5b2b949929cf8b4452fa14b047cee65ef6fdbd2c75c1a21043605fc02` |

The two `result.json` files are **byte-identical**. Every process runs with one BLAS thread.
The harness sets that before numpy is imported, and the workers inherit it.

## 2. Its verdict matches the controls' record (k = 10 starts)

`out/` holds the stand-in run at k = 10.

- **Verdict:** "FAIL -- rule did not run; copy or marginal; below threshold for this family;
  family fits anything; ambient, not substantive structure".
- **Against the controls' record** (`harness_controls.json` → `controls["real/PR"]`): the same
  verdict and labels, and 0 numeric differences beyond 1e-9 across every arm.
- It was run with `--allow-dirty-standin`, before this commit, and its stamp says so. That flag
  is refused for any rule outside `rule_runs/_standin/`.
