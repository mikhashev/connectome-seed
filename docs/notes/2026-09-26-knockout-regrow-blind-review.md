# Blind review: knockout-and-regrow, block A on flyvis-65 (registered run of 2026-09-25)

**Written:** 2026-09-26 UTC, by an external blind reviewer (Claude Code session, brief pasted by
Mike). **Not to be committed** (the brief's instruction). Read-only: nothing in the repository or
in the private folders was modified, and the registered script was not rerun.

**Conclusion (one line): the verdict follows.** The printed verdict G, with every number on the
verdict line and in the §3.5 table, follows from the registered §4 conditions applied to the
run's own `summary.json`, and every deciding number was reproduced exactly from the run's private
raw fits by an independent implementation.

**Scope.** Registration `docs/plans/2026-09-24-knockout-regrow-registration.md`, revision 3.4.1,
§0–§9 and §11 only (§10 and §12 not opened). Script `results/genome/c6/checks/knockout_regrow.py`
(2,666 lines, the version committed at the run's head; see E.2). Committed outputs
`results/genome/c6/checks/knockout_regrow/`. Private outputs
`connectome-seed-data/knockout_regrow/flyvis65_20260925T171656Z_74de0401a21f/`.

---

## A. Label: §4 applied by hand to `summary.json`

All values below are quoted from `summary.json` at the JSON paths given (`$` = file root), at
full stored precision. `RESULT.md` was not used for this section.

| predictor | path under `$.real.rows` | `n_ge` | `leg_S_passes` | `p_P` | `ceiling_block` | `ceiling_full` |
|---|---|---|---|---|---|---|
| rule #2.1 | `.rule` | 69 | false | 0.3288 | 1.0 | 0.84423828125 |
| BF_1 | `.["BF:1"]` | 99 | false | 0.3837 | 1.0 | 0.7646484375 |
| BF_2 | `.["BF:2"]` | 99 | false | 0.4912 | 1.0 | 0.9111328125 |
| BF_3 | `.["BF:3"]` | 99 | false | 0.5119 | 1.0 | 0.9951171875 |
| BF_4 | `.["BF:4"]` | 98 | false | 0.5042 | 1.0 | 1.0 |

(`n_deg` = 0 and `n_valid_shuffles` = 99 in every row, same paths; `$.real.n_deg` = 0.)

The §4 rows in order (registration lines 1296–1328; the branch conditions are the table rows at
lines 1325–1328):

1. **R** (line 1325): needs the primary to pass leg S (`n_ge = 0` of the 99 − `n_deg` shuffles,
   §3.2 line 565) **and** leg P (`p_P <= 0.01`), on both D1 candidates. Reading A (rule #2.1):
   `n_ge` = 69 ≠ 0 and `p_P` = 0.3288 > 0.01 — fails. Reading B (BF_1): `n_ge` = 99, `p_P` =
   0.3837 — fails. **Not R.**
2. **W** (line 1326): needs some BF_r (r = 1..4) with `n_ge = 0` and `p_P <= 0.0125`, on both
   readings. The four BF rows have `n_ge` = 99, 99, 99, 98 (none 0) and `p_P` ≥ 0.3837 (all >
   0.0125). **Not W.** Both readings therefore give "-"
   (`$.real.reading_A_rule.letter` = `-`, `$.real.reading_B_BF1.letter` = `-`), and by the §4
   preamble (lines 1302–1308) G and U are read on rule #2.1.
3. **G** (line 1327): needs (i) not R, not W — holds; (ii) the primary **and every BF_r** with
   `p_P > 0.10` — 0.3288, 0.3837, 0.4912, 0.5119, 0.5042, all > 0.10 — holds; (iii) the
   primary's `ceiling_block >= 0.90` (`GATE_CUT`) — `$.real.rows.rule.ceiling_block` = 1.0 —
   holds. **G follows.** Rows are tested in order and the first that holds is the verdict
   (line 1298), so the label is **G**, which equals the printed verdict
   (`$.real.label` = `"G"`; RESULT.md line 5).

Ancillary parts of the label, also checked from `summary.json`:

- **Mechanism description** (§2.4, lines 464–489; §4 line 1327): rule #2.1's `ceiling_full` =
  0.84423828125 < `MECHANISM_CUT` = 0.90 → "orthogonal", printed as **description only**.
  `$.real.mechanism_description` = `"orthogonal (rule #2.1's ceiling_full = 0.8442 < 0.90)"` and
  the verdict line marks it "[mechanism, description only: …]". Correct.
- **The three limits printed on the G label** (§3.6 lines 1045–1067; §4 line 1327 requires them).
  Recounted by me from `$.synthetic.worlds[*].rows[*].p_P` and `[*].label`: seen/n by rule #2.1 at
  γ = 0.5, 0.6, 0.75, 0.85, 1.0 is 1/5, 3/5, 5/5, 5/5, 5/5 and R/n is 1/5, 2/5, 5/5, 5/5, 5/5,
  giving γ\*_P = 0.6 (bracket (0.5, 0.6]), γ_R = 0.75 (bracket (0.6, 0.75]), per-predictor leg-P
  limits {rule 0.6, BF_1 0.6, BF_2 0.75, BF_3 0.75, BF_4 0.75}, family limit 0.75 set by BF_2,
  BF_3, BF_4, transition band [0.6, 0.75) = 1 grid step = 0.15 in γ, and 3 U worlds all inside
  the band. All equal the stored `$.synthetic.limits` and the printed label. `M worlds that read
  G at or above γ*_P / γ_R`: both empty (`$.synthetic.limits.G_at_or_above_leg_P`, `.G_at_or_above_R` = []).
- **U rule** (§3.6 lines 1100–1121): `$.synthetic.u_rule` = 3 threshold U of 25 dense-grid
  worlds (0 failed fit, 0 not measured), `renamed` = false → U stays, as the report prints.
- **λ on the verdict line** (§4 lines 1346–1353): selected knockout λ are 1, 1, 1, 3, 3
  (`$.real.rows.*.lambda_ko`). None is 100, so the "G reached through λ = 100" sentence is
  correctly absent from the real verdict line.
- **No contingency** (§3.6 lines 1141–1145): no No world read U
  (`$.synthetic.two_world_check.rows[2]`, labels G ×5), `$.synthetic.two_world_check.no_contingency`
  = false; the verdict line correctly carries no contingency sentence.
- **n_deg sentence** (§3.2 lines 567–570): `n_deg` = 0 ≤ 5, so no sentence. Correct.

The script's reading functions implement these §4 conditions literally: `reading_on`
(knockout_regrow.py:1105–1113), `read_label` (:1151–1185), `label_text` (:1208–1233),
`verdict_line` (:1240–1273); `P_R` = 0.01, `P_W` = 0.0125, `P_G` = 0.10, `GATE_CUT` =
`MECHANISM_CUT` = 0.90 (:222–226).

## B. Recompute from the private raw fits

Method: independent implementation in a scratch script; nothing imported from the repository.
AUC by explicit pairwise Mann-Whitney with ties ½ (registration §3.1), and a separate averaged-
rank path for the permutation null; both cross-checked against each other. The leg-P null drawn
by me as `numpy.random.default_rng(90000)`, 9,999 × `permutation(64)` in order (§3.7 table,
line 1268). `TAU` = 1e-9 (§3.2). Inputs: `raw_fits_real.json.gz` (637 records = 6 predictors ×
(ko, full, block) + 99 shuffles × 6 + 20 permuted-block ceilings + 5 ko1), after verifying every
file in the folder against its `SHA256SUMS.txt` (all match; no unlisted files).

The block labels `y` in the raw records equal the reviewed board (ON × T4 and OFF × T5 present,
32 of 64; reconstructed by me from §1.2 names in the registered SOURCES × TARGETS row-major
order, script :171–184), and are identical across all base ko/full/block records.

Results (mine vs `$.real.rows.*`; "exact" means Python float equality):

| quantity | rule #2.1 | BF_1 | match |
|---|---|---|---|
| block AUC | 0.53271484375 | 0.521484375 | exact |
| AUC(N1) | 0.53515625 | — | exact |
| `M_real` | −0.00244140625 | −0.013671875 | exact |
| `n_ge` (of 99, `n_deg` = 0) | 69 | 99 | exact |
| `p_S` | 0.70 | 1.00 | exact |
| `p_P` (count ≥ AUC − TAU) | 0.3288 (3,287 of 9,999) | 0.3837 (3,836) | exact |
| `ceiling_full` | 0.84423828125 | 0.7646484375 | exact |
| `ceiling_block` | 1.0 | 1.0 | exact |

Also recomputed, all exact: AUC, `M_real`, `n_ge`, `p_S`, `p_P` for BF_2 (0.5029296875, −0.0322265625,
99, 1.0, 0.4912), BF_3 (0.5, −0.03515625, 99, 1.0, 0.5119) and BF_4 (0.5009765625, −0.0341796875,
98, 0.99, 0.5042); BF_4's single shuffle strictly below its margin is sd = 18 (M = −0.03480…),
consistent with `n_ge` = 98. `per_shuffle.csv` (committed, 99 rows) equals my recomputation from
the raw fits on `present` and all six predictors' AUC and λ, 0 mismatches.

Beyond the brief, the same machinery re-derived **all 45 synthetic worlds** from the private
`raw_fits.json.gz` (28,665 records): per world and predictor the AUC, `p_P`, `n_ge`, both
ceilings, then my own §4 reading with the D1 agreement rule. Every world's label and every
compared number equals `$.synthetic.worlds` (R: RRRRR, Nf: GGGGG, No: GGGGG, W: WWWWW, M0.5:
RGGGG, M0.6: RURUU, M0.75: RRRRR, M0.85: RRRRR, M1.0: RRRRR), and my limits from those labels are
γ\*_P = 0.6, γ_R = 0.75, family = 0.75 (BF_2–4), 3 dense-grid U all at γ = 0.6 — identical to the
stored and printed limits. `smallest_passing_auc` re-derived by me from the k/1024 grid over a
tie-free prediction's permutation null: 0.666015625 for board `z` (world R:0 and the real block)
and 0.6728515625 for board `z'` (world No:0), equal to the registered values of §3.3 (lines
829–846) and to `$.real.smallest_passing_auc`.

`p_P` was therefore feasible and recomputed; the null of §3.2 (uniform label permutations, one
generator, seed 90000) reproduces the stored values exactly, which also confirms that the stored
`p_P` used the registered generator.

## C. Printed vs stored

Exact string or byte comparisons (scratch scripts; "equal" = byte/string identity):

- **Verdict line**: RESULT.md line 5 (`**Verdict: …**`) equals `$.real.verdict_line`. Equal.
- **§3.5 table**: the six rows (RESULT.md lines 17–22) rebuilt from `$.real.rows` with the
  script's own format strings (`md_bank_table`, knockout_regrow.py:2382–2396) — all 6 equal,
  including every rounding (e.g. 0.53271484375 → 0.5327; share (full) 0.0950… → 0.10; N1's
  share (block) `n/a`).
- **Permuted-block ceilings line** (RESULT.md line 24): equals the 20 values of
  `$.real.perm_ceilings_full_rule` at 3 decimals plus the real `ceiling_full`. Equal.
- **Fixed-λ line** (RESULT.md line 30): equals `$.real.fixed_lambda` (BF_3 0.484375 → 0.4844,
  p_P 0.5915; BF_4 0.48046875 → 0.4805, p_P 0.6135). Equal.
- **The §4 row quoted verbatim** (RESULT.md line 9): equals the registration's G row (line 1327)
  with the `> ` prefix. Equal. The quoted §4 section at the file's tail equals the registration's
  §4 (`## 4. Reading rule` … before `## 5.`), line for line.
- **The limits line** (RESULT.md line 28): equals the text rebuilt from `$.synthetic.limits`
  (limits_text, :1198–1205) plus the binomial note and the private-outputs path from
  `$.manifest.private_outputs`.
- **synthetic_worlds.csv** (committed, 270 rows): equals `$.synthetic.worlds` on family, j, seed,
  board, label, auc, p_P, p_S, n_ge, n_deg, both ceilings and lambda_ko for every row (0
  mismatches), and is byte-identical to the private copy in the run folder; sha256
  `32d62c717d20eb2fafeb465c2ee8fcf8e3880d7a327646bdccc8753714f895c1`, the value printed in
  RESULT.md line 120 and matching the truncation `32d62c71…95c1` in §3.3 (line 680).
- **per_shuffle.csv**: equals `$.real.per_shuffle` on every compared column (section B above; the
  committed CSV carries the real arm's shuffles, as §3.3 line 822 states).

## D. Reading: nothing stated beyond §4–§6

- The verdict and label text are exactly the registered G text: "not detected at the R level
  above gamma_R", with the gate variable named, all three limits with brackets, the per-γ
  fractions, the transition band and the instrument constants — as §4 line 1327 requires. The
  mechanism is inside "[mechanism, description only: …]" and no sentence of RESULT.md reads a
  decision or consequence from it.
- A scan of RESULT.md outside the quoted registration text for overclaiming ("no grammar",
  "absent/absence", "proves", "rules out", "no structure", "conclusive", …): every hit is inside
  registered guard text — the quoted §4 row itself, and the λ = 100 sentence on synthetic
  Nf/M0.5/No world verdict lines ("… this G reads 'weaker than the detection limit', not
  'absent'"), which §4 (lines 1346–1353) requires there. The real block's verdict line contains
  neither word (no knockout fit selected λ = 100).
- The mirrors, per-type AUCs, quadrant means and D7 offset/count/sign fields are deferred to
  summary.json (RESULT.md line 26) and decide nothing, as §4 "What decides" (lines 1368–1373)
  requires. The fixed-λ diagnostic is printed apart from the verdict line (RESULT.md lines 30,
  151–201), per Johnny's condition (§3.5 lines 908–915).
- RESULT.md line 3 states the registration and revision 3.4.1 and the git head; no claim of
  animal-level generality appears anywhere (the within-fly note, line 11, is the registered §2.4
  text).

## E. Gates and the committed tree

1. **Recorded gate results** (all in `summary.json`):
   - Pins §1.1: `$.checks.1_pins.passed` = true; the eight hashes recorded equal the
     registration's table (lines 243–253).
   - Machine checks §3.4: `$.checks.2_block_and_mask/.3_board/.4_pre_data_tables/.5_n1_parity/
     .6_leakage/.7_auc_function/.8_harness_identity/.9_determinism` — all `passed: true`. Check 5:
     `D_N1_logit` = 0.0 (< 1e-9). Check 8: BF_1 margin 0.028150051052145946, difference 0.0.
     Check 3: quadrants 16/16/0/0, `y_equals_x_times_w` = true.
   - Pre-run reference verified before any fit (revision 3.4.1):
     `$.synthetic.two_world_check.prerun_reproduction.prerun_files.passed` = true ("every listed
     file matches its listed and pinned sha256"), unlisted = [].
   - `smallest_passing_auc` checked scalar (§3.3 lines 829–862):
     `$.synthetic.smallest_passing_auc_check.passed` = true, 45 of 45 worlds, registered values
     derived from the pinned `synthetic_only.json` (z 0.666015625, z' 0.6728515625).
   - ko1 count control (§3.3 lines 801–816): `$.synthetic.fits.ko1_count` — counted 225/47/178 ==
     registered 225/47/178 (5 fitted by the path check on world:W:0), `passed` = true. RESULT.md's
     "47 reused, 173 fitted" (line 203) is the completion step's own counter; 173 + 5 path-check
     fits = 178, consistent.
   - Reproduction gate (§3.3, §7): `prerun_reproduction.passed` = true, outcome 1 ("every
     deciding column equal"), rows matched by key, 0 missing either side, order equal;
     `byte_identical` = false recorded as a fact; mechanism_description differs on 84 rows, 84
     exactly revision 3.2's rename, 0 unexplained. Manifest:
     `$.manifest.prerun_comparison_outcome` = 1, `prerun_csv_byte_identical` = false.
   - Two-world check §3.6: `$.synthetic.two_world_check.passed` = true, `stop` = false; stop rows
     met (R 5/5 R, Nf 5 G ≥ 3 and no R/W, No 5 G, W 5/5 W), M rows "curve"; `no_contingency` =
     false. The per-fit diagnostic (decides nothing) compared all 28,665 pinned records with this
     run's fits: 0 differences, `max_abs_dp` = 0.0 (`$.synthetic.raw_fits_diagnostic`).
   - Fixed-λ path check: `$.synthetic.fixed_lambda_path_check.passed` = true (world:W:0, all five
     identical).
   The script's control flow stops before the real arm on any of these failing
   (knockout_regrow.py:1948–2016 for the step-3 stops, :2632–2636 for the two-world stop; the
   real arm starts at :2639), and the script that ran is the committed one (point 2), so the
   recorded passes are the gates that gated.
2. **Clean committed tree.** `$.manifest.git_head` =
   `74de0401a21f33db22def152fd72fdf0d490ffb4`; `tree_dirty_under_c6_or_plans` = false,
   `tree_dirty_paths` = [], `allow_dirty` = false, `not_the_registered_run` = null, `mode` =
   "flyvis65", `smoke` = false, `starts` = 10, `from_raw` = null, `device` = "CPU", python
   3.10.20, numpy 2.2.6 (as §7 requires). Verified independently against git: the commit exists
   (committed 2026-09-25 16:54:54 UTC, before the run stamp 17:16:56Z in the private folder
   name); all eight §1.1 pins match `git show 74de040…:<file>` (LF-normalised sha256); the
   manifest's `registration_sha256_lf` (409184de…) and `script_sha256_lf` (113c4526…) equal the
   committed blobs of the registration and the script at that head; the working-tree copies I
   reviewed equal those blobs. The private folder name's hash suffix equals the head's first 12
   characters. The verdict line carries no "--allow-dirty" suffix, correctly.
3. **Private outputs.** All six files match the folder's `SHA256SUMS.txt`; the manifest inside
   the private `synthetic_only.json` is identical to `$.manifest` of the committed
   `summary.json` (same git head, same gate outcomes). Runtime: manifest 7,872 s (recorded at
   the end of step 3), RESULT.md header 8,070 s (whole run) — two registered fields, not a
   discrepancy.
4. **Observations, not gate failures:**
   - **There is no log file.** The registered private outputs (§7 lines 1657–1666) do not
     include one, and none exists in the run folder; the brief's "log" therefore has no file to
     check. Gate evidence above comes from the manifest and the recorded check objects. The
     stdout log of the run was not preserved.
   - `$.manifest.machine_record.blas_runtime` = null: §7 (revision 3.2, lines 1549–1553) says
     the manifest records "the BLAS loaded at run time (threadpoolctl)"; the key exists but
     holds null (threadpoolctl presumably absent). The build-time BLAS and thread variables are
     recorded.
   - **The committed outputs are not yet committed**: `git status --porcelain` shows
     `?? results/genome/c6/checks/knockout_regrow/`, and `git log`/`git ls-files` for that path
     are empty. The files exist only in the working tree as of this review.
   - The head commit (74de040, "GPU instrument for BF_r fits: separate, unreviewed…") adds a GPU
     tool that this registration does not use (§7: the instrument is the pinned CPU harness);
     the manifest records `device: CPU` and the pins cover the instrument files.
   - The `provenance/` subfolder that §7 (revision 3.2, lines 1623–1631) says is to be added to
     the pre-run reference folder is absent (the folder holds exactly the five pinned files plus
     `SHA256SUMS.txt`, all matching their pins today).

## What I could not check, and why

- **The fits themselves.** Read-only mandate: no refit of the 28,440 synthetic and 637 real-arm
  fits. My recomputation starts from the stored `p_exist`/`y`/`lam` per fit. That the synthetic
  fits equal the pinned pre-run store rests on the run's own per-fit diagnostic (0 differences
  over 28,665 records) and on the reproduction gate (outcome 1), not on my recomputation.
- **Non-deciding printed quantities** not recomputed: `D`, log-loss and its margin, precision at
  32, quadrant means, regrown shares, `p_P_rowcol` (the row-and-column generator), per-type
  AUCs, mirror `p_exist`, `auc_other_59`, and the D7 offset/count/sign fields. All decide
  nothing under §4 "What decides"; their printed copies equal `summary.json` (section C covers
  every §3.5 table cell as a string).
- **The gates' execution order** is established from the committed script's control flow plus
  the recorded outcomes, not from a preserved log (none exists; E.4).
- **`$.checks` completeness beyond pass flags**: I did not re-derive check 4's three §1.4 tables
  from `offsets.csv` myself; the printed tables (RESULT.md lines 32–56) equal the registration's
  §1.4 (lines 314–353) by inspection, and check 4 recomputes them by construction.
- **Blindness notes.** Not opened: anything under `chat/`, `docs/briefs/`, `docs/retrospectives/`,
  `backlog.md`, `backlog_closed.md`, `ROADMAP.md`, and §10/§12 of the registration (section
  boundaries located by heading grep: §10 at line 1774, §11 at 1965, §12 at 2093; I read 1–1773
  and 1965–2092). The registration's pre-§0 status header (lines 1–169) is outside the named
  exclusions and was read; it, like §0–§9, names reviewers and vote times, which the exclusion
  list does not forbid. Commit subjects (from `git log --oneline` of the two registered files)
  were seen; one names a reviewer's table. `GLOSSARY.md` was read as instructed.
