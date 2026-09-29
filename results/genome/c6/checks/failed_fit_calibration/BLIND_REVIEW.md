# Blind review: failed-fit branch calibration, registered run from 255a03d

Reviewer: a separate agent session (model Fable), 2026-09-29, briefed by CC with the allowed
sources only: the registration rev 1.9, this folder and the data folder, the script and what it
imports. Forbidden: the scratchpad, chat logs, memory files, commit messages beyond the start
context, retrospectives. The report below is the reviewer's, transcribed by CC.

## Verdict

**The recorded outcome follows.** Outcome "C2, C6" derives exactly from the outputs under
registration rev 1.9's own rules (sections 6, 6a, 7). No stop row and no flag row could have fired
on these outputs. Two registered "printed per world" diagnostics are absent or under-reported
(listed under "Not licensed / missing"); neither enters any label, stop, flag or outcome rule.

## Checks and evidence

1. **Integrity and pins.** `sha256sum -c`: repo copy 7 OK (raw_fits.json.gz absent, as expected);
   data copy 8 OK. Registration LF sha256 `7aa53ec9...` equals the pin in stdout.log:1 and the
   manifest. Script, B script and survey.py LF hashes at HEAD equal the manifest; `git diff --stat
   255a03d HEAD` on the script, B script, harness.py, fit.py, survey.py and the registration is
   empty. Manifest: not_registered null, fixture false, tree_dirty_paths empty, git_head 255a03d.
   No stop_record.json. Seeds checks all true; cert budget equals section 6.
2. **Recomputation from calibration.json and worlds.csv** (own code, section 6 table on exact
   values, cert = Fraction): all 15 worlds match on separator row, sub-kinds, branch_met, flags,
   FC stops and A3. FC: ceiling_block 162 wins, 156 ties = 0.600000 exactly (tau identical),
   lambda 100 on all 5; ceil_1 = 1.0 exactly (A2); ceil_lambda_c_float 0.48 exact / 0.60 TAU
   (ulp_sensitive, reproduces section 3/4); N1 on board z 0.72 exact / 0.60 TAU (section 2, Q-A6).
   A3: cert 1/1 >= planted 1, 19/20, 9/10 on every board. Stops (a), (b), (c), the ceil_1 stop,
   "FC does not read failed fit", script-defect (block_fit_reproduced true on all 15), R/W: none
   fired; `stops = []`. Flags GATE_/CEIL_1_/CERT_ULP_SPLIT: none.
3. **Recount from raw p and y** (raw_fits.json.gz): every recorded value matches on all 15 worlds,
   including BF_1-BF_4 against bf_block.csv. FC's 5 worlds share one board; the 10 FN boards are
   distinct; FN1 differs from z in exactly 2 cells, FN2 in exactly 4. All 99 permuted boards
   recounted, 0 mismatches; 110 distinct patterns = 110 cert entries.
4. **cert:** independent Fraction recount of all 110 stored members: 0 mismatches; counts_agree
   true, ulp_sensitive false on all 110; world boards 1/1; permuted minimum 39/40 = 0.975.
5. **Registered label path:** `auc` (B:791-800) exact, ties 1/2; `evaluate_bank` ceiling_block is
   the registered object; `read_label` gate >= 0.90 -> `u_kind` failed_fit -> `FAILED_FIT_TEXT`;
   FN: p_P > 0.10 and gate >= 0.90 -> G. FC's forced fit is `K._fit_one` with LAMBDAS = [100] on
   the block mask (S-C3).
6. **Code spot-checks:** `separator_reading` is row for row the section 6 table; FC stop branches,
   ceil_1 stop, not-failed-fit stop, script-defect stop and section 6a flags present;
   `outcome_labels` implements section 7 as registered; `cert_search` staging and Fraction
   certificate as registered; `assert_final_fit` present.
7. **Permuted reference "printed, decides nothing":** `outcome_labels` receives only the 15 worlds.
   Recomputed: 53 of 99 ceiling_block < 0.90, 99 of 99 cert >= 0.90; lambda_c = 100 on 56 boards,
   1 on 43.

## Derivation

FC: 5 of 5 read U, failed fit, sub-kind FF-sel. FN: 0 of 10 meet the branch, so C1 fails and C2
holds. C3: no. C5: no stop. C6: declared, stands. **Outcome = C2, C6** = recorded. Section 6
predictions for FC and FN all met; section 8's gate-option table for FC reproduced.

## Not licensed / missing (none affects the outcome)

1. Section 5, "the fit at lambda = 100 on each board ... is printed per world": for the 10 FN
   worlds no forced-lambda = 100 fit exists. Sections 14 and 14a never ask for it, so the script
   followed section 14, but section 5's sentence is unmet for FN. Diagnostic only.
2. Sections 6/6a: CEIL_1_ULP_SPLIT and CERT_ULP_SPLIT are to be "printed and counted like
   GATE_ULP_SPLIT"; only `gate_ulp_split_count` is reported. The per-world flags column is empty,
   so the counts are visibly 0, but not reported under their own names.
3. Cosmetic: `manifest.cert_budget.status` still says "proposed"; `ceil_lambda_c_float`'s
   ulp_sensitive flag and `ceil_1_starts100_quantised` appear only in calibration.json.
4. `manifest.ko1`: 0 reused, 75 fitted; decides nothing here.

## Exposure declaration (the reviewer's)

Before opening any allowed file, the session context showed the memory index (topic titles only)
and the last five commit subjects (naming the run's commit, its source commit 255a03d, the pinned
LF sha256 and rev 1.9's content). No memory file, scratchpad, chat log, .dpc or retrospective was
opened; no file was written. harness.py and fit.py were not opened. Not checked: the numerical
correctness of the fitter and of the survey's search, cross-machine reproducibility, the cited
fit.py/harness.py line numbers. The run was not re-executed.
