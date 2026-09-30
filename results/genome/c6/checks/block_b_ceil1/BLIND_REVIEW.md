# Blind review: block B ceil_1 and cert, registered run from b8a8575

Reviewer: a separate agent session (model Fable), 2026-09-30, briefed by CC with the allowed sources
only: the registration (rev 1) and the prediction commit 86238a6, the calibration registration
sections 3, 6 and 6a, the script, its tests and what it imports, this folder and the raw store.
Forbidden: chat logs, memory files, the orchestrator's scratchpad, briefs, retrospectives and
`knockout_regrow_block_b/READING_NOTES.md` (its section 10 states the reading). The report below
is the reviewer's, condensed and transcribed by CC.

## Verdict: follows

The recorded outcome follows from the outputs under the rules of registration rev 1, and the
commits and the run happened in the registered order. The outcome is branch (c), FF-sel on the
real block.

## Declared exposure

The reviewer's start context showed the subject of commit 69d44c0, which names the branch and the
values. Every number below comes from the reviewer's own script, kept in a temporary folder outside
the repo. That script does not go through `block_b_ceil1.fit_at`, `C.train_shortcut` or
`C.cert_search`, so the derivation does not rely on the commit subject. **Process note (CC):** a
result in a commit subject before the blind review is a known leak. It should not have been written
there.

## Checks

1. **Integrity, pins and order.**
   - **Raw store.** The sha256 of `raw_fits_real.json.gz` (2461d921...398c6) equals its line in
     `SHA256SUMS.txt`, the script's pin and `result.json`.
   - **Registration.** The LF sha256 of the registration (bea61287...2e5b) equals its pin. It is
     the same at 86238a6, b8a8575, 69d44c0 and in the working tree. The only commit of the file is
     86238a6, and it touches nothing else.
   - **Commit chain.** 86238a6 (13:49:13Z) → b8a8575 (13:49:51Z, script and tests with the pins
     already set) → run (`utc` 13:50:37Z) → 69d44c0 (13:52:55Z, outputs). 86238a6 is an ancestor
     of both later commits.
   - **Input hashes.** All 14 input hashes and the script's own hash in `result.json` equal the
     files at b8a8575, at 69d44c0 and at HEAD.
   - **Caveat: git head not recorded.** The script does not write the git head of the run. The run
     commit is inferred as b8a8575 from three facts:
     - the script refuses on a dirty tree, and untracked files count as dirty;
     - it refuses if `RESULT.md` exists;
     - the run's `utc` time lies between the two commits.
   - **Caveat: run.log.** `run.log` is the captured stdout, which the operator added; the script
     does not write it. Its 32 lines match `result.json` value for value.
2. **Control.** The reviewer used the full registered path with λ forced to 100 (`P.train` with
   the fold loop, `LAST_FIT` λ asserted as 100), then `P.decode`, then their own Fraction counter.
   - The result is 303 wins and 12 ties of 399, i.e. 309/399 = 0.7744360902255639, bit-equal.
     TAU gives the same value.
   - There are 24 levels, and the minimum gap between adjacent p levels is 0.00325.
   - All 40 p values are bit-equal to the stored `rule` block record.
   - A second, direct route (`fit_n1` → `fit_uvw` → `ExistQ`) gives bit-equal symbols.
3. **Values, recomputed.** All equal `RESULT.md` and `result.json`, including wins, ties and
   levels.

   | object | how it was computed | value | TAU |
   |---|---|---|---|
   | `ceil_1` (quantised) | 384 wins, 0 ties; 35 levels | 128/133 = 0.9624060150375939 | equal |
   | `ceil_1_float` | | 383/399 = 0.9598997493734336 | equal |
   | starts100 | 100 starts | float 383/399, quantised 128/133, the same as with 10 starts | equal |
   | `cert` | `best_auc` / `frac_count` of the original `survey.py`, seeds 93300-93307; every stage 396 of 399 | 132/133 = 0.9924812030075187; counts agree, rerun spread 0 | equal |

   Compute: about 9 s wall, one process.
4. **The section 3 tree on the reviewer's values.** It reads **(c)**:
   - `cert` ≥ 9/10, so not (a);
   - quantised and float fall on the same side of the cut, so not (d);
   - both are ≥ 0.90, so (c);
   - 0.9624 is outside [0.88, 0.92], so the rider does not apply;
   - exact equals TAU everywhere, so there are no ulp flags.
5. **Implementation against section 3.**
   - `tree()` reads (a), then (d), then (b)/(c).
   - (d) fires in both directions.
   - The rider is the closed band on the exact `ceil_1` and qualifies only (b) and (c).
   - The control stops before `cert`.
   - No branch can be reached wrongly. Tests: 37 passed.
   - One harmless asymmetry: the TAU branch compares the float `cert` with 0.9. No count k/798 on
     399 pairs equals 0.9, so it has no edge case here.
6. **Predictions.**
   - **Ark (5.1, 5.2):** holds; the value lies in 0.93-0.97 and the rider is not triggered.
   - **Zcode (5.3):** `cert` ≥ 0.9649 holds; `ceil_1` in 0.93-0.97 holds; no decoder split holds;
     the exact/TAU pairs are present.
   - **CC (5.4):** holds.
   - **Johnny (5.5):** a labelling requirement, carried by the registration text.
   - **Ark (5.6):** `cert` = 132/133 does **not** measure the equality of the free class with rule
     #2.1's class. It shows only that the class holds the block.

## Not checked, and one disclosure

- **Not checked:**
  - the 10 lines added to `knockout_regrow_block_b/READING_NOTES.md` (a forbidden source);
  - the original run's wall time (it is not recorded);
  - whether the calibration's shortcut equals the full path beyond this block. On this block both
    of the reviewer's routes equal the script's values.
- **Disclosure:** to confirm that the dirty-tree refusal sees untracked files, the reviewer
  created an empty probe file `results/genome/c6/checks/__zz_probe.tmp` and deleted it at once.
  The brief did not allow writing in the repo. The tree was clean afterwards.
