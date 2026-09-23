# C6 harness: τ now applies in P3 and P4, as spec A7 already said

**Written:** 2026-09-23, by CC (subagent), on Mike's approval (DPC Research group chat,
2026-09-23 13:26 UTC).
**What this is:** a record of a code change to `results/genome/c6/harness.py`. It aligns the
code with spec A7. **It is not a new rule and not an amendment:** the spec, the acceptance files
and the registered constants are unchanged.

## What was wrong

Spec A7 (`docs/plans/2026-09-23-c6-control-specification.md`) says:

> A tie is **not a win** when superiority is tested (P1 on existence and offset set; P2; P3;
> P4).

and a win means being better by more than τ = 1e-9. The harness applied τ in P1 and P2 (`cmp`,
and P1's `mean + TAU`), but P3 and P4 used a plain `>`:

| test | before | after |
|---|---|---|
| P3, "strictly above all 99 shuffles", per field | `real_m[f] > m` | `real_m[f] - m > TAU` |
| P4, "above the threshold" | `real_m["existence"] > thr` | `real_m["existence"] - thr > TAU` |

`TAU` is the registered constant (A15), the same one `cmp` uses. The report-only count
`n_shuffled_ge_real` is unchanged.

**Effect.** The change is monotone: it can only turn a pass into a fail, and only when a margin
is within 1e-9 of the shuffled margin or of the threshold, that is, at floating-point noise.

## Who found it and who ruled

- **Found** by the blind reader: `docs/plans/2026-09-23-blind-reader-report.md`, Part E (a
  finding about the exam; P4's `harness.py:1028` and P3's line 1019 used a plain `>`). Also
  recorded in `docs/plans/2026-09-23-first-rule-failure-predictions.md` (v5 change list).
- **Ruled** by Zcode, the spec's owner (group chat, 2026-09-23 13:17 UTC): align the code to A7.

## Hashes and line numbers

- Harness sha256 (LF-normalised) before: `c01cd9eb02481132a0d254ffe63e90a655e79979112d620207ce39c75bdfbd86`
  (the version the rule runs under `rule_runs/` record). After:
  `6fc809527c69ee84aadebfc15c0ba755c189ddc93c80c05c0fa11d969a8d7297`.
- The change adds three lines. Line numbers of `harness.py` cited in earlier records (for
  example "1019" and "1028") refer to the version those records stamp; from line 1019 on they are
  now shifted.
- No earlier record is rewritten. The controls were re-run on the new harness (A20); the result
  is in `results/genome/c6/HARNESS-CONTROLS.md`, section "Re-run after the τ alignment".
