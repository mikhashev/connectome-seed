---
**Status: ACCEPTED (not merged), revision 1.6 of the GPU instrument registration, 2026-10-06 UTC. Text only: no fit and no GPU call
was made for it; the instrument's CPU tests ran once before the commit, on Mike's word (S.7).** It registers extension X (the block
mask and the fixed-lambda `ko1` fit) on the strength of the validation runs VX0, VX1, VX2, VX6 and VX7
of 2026-09-29 (committed in `29548f1`), and it carries the three stale texts that
`backlog.md` (entry `THE-GPU-INSTRUMENT-REVISION-REGISTERING-EXTENSION-X-STILL-CARRIES-THREE-STALE-HASHED-TEXTS`)
says only this revision may fix. **Reviewed in the DPC Research chat: follows** (Ark 2026-10-06
19:16:26 UTC, Q1 with two corrections to S.4; Warren 19:16:55, Q4; Johnny 19:18:36, Q3; Zcode
2026-10-07 05:36:24 UTC, Q2). The corrections are applied in S.2, S.4, S.5 and S.9. **Mike's word:
yes to the revision and to the tests (Claude Code session, 2026-10-07).** The tests ran on CPU before
the commit (S.7). The merge (S.10 Q6) is not decided; the draft files stay separate until it is. The reviewers' votes on the VX results ("four yes",
handover section 2) are not in a repository carrier; they are cited from the handover.
---

# GPU instrument registration, revision 1.6 (draft): extension X registered, three stale texts fixed

## S.0 What this revision is, and what it is not

**Form.** Like revision 1.5/1.5.1 (`docs/plans/2026-09-29-gpu-instrument-revision-1.5-draft.md`,
"Why a separate file"), this is a separate dated file in `docs/plans/`, written as sections that can
be merged into the registration unchanged. The registration
(`docs/plans/2026-09-26-gpu-instrument-registration.md`) is the text under which V0-V8 and VX0-VX7
ran; its text is hashed (`instrument.REGISTRATION_TEXTS`, `instrument.py:44-51`) and every run record
names it. So this revision does **not** edit it. The registration stays at revision 1.4
(LF sha256 `0f5be2fc...`, `e2fab47` with section 15.5 from `a0e16b6`); the VX manifests record exactly
that (`revision "1.4"`, e.g. `VX1_A_block_20260929T134726Z_5d65baf16803/manifest.json`,
`registration_text`). Revision 1.5.1 is likewise still a draft file. The status header of the
registration and its table `REGISTRATION_TEXTS` change **only when 1.4 + 1.5.1 + 1.6 are merged in one
step** (S.8); this draft adds no row to the table, because a row needs the merged text's hash, which
does not exist yet.

**It registers** (S.2-S.5): extension X's scope (the block mask and the fixed-lambda `ko1` fit, BF_1-BF_4,
base views only, arms A and B), its four composition identities, what VX0-VX7 showed with the carrier of
each number, and the envelope of the fits that differ from the CPU.

**It does not register**: any use by an arm (D11 stands: an arm names the instrument before its
pre-run; `ext_gpu_stage.py` refuses arm runs altogether); rule #2.1 (extension X plan section X.2);
any composition whose block or ko1 fits carry a pair on S(f) with a gap below 2^-23 (S.4); a block
fit at a lambda other than 1 (S.4); the hybrid's
CPU side for `ko1` (S.4); a code check of the four identities (S.2). It changes no gate, E1, E2, E3 or
D1-D13.

## S.1 Extension X: what it is

Source: `docs/plans/2026-09-29-gpu-instrument-extension-x-plan.md`, revision 1.1, sections X.1, X.2.

| mask | the CPU fit it replaces | record key | read by |
|---|---|---|---|
| block | `harness.fit_bf` on the block view: N1, lambda by the nested scheme, final `bf_als` | `world:<f>:<j>\|\|block\|\|BF:<r>` | `ceiling_block` (an AUC), `regrown_share_block` (a ratio of exact AUCs), `lambda_block` |
| ko1 | `train_fixed_lambda("BF:r", ..., 1.0)`: N1 on the ko view, `bf_als` at lambda = 1, no lambda choice | `world:<f>:<j>\|\|ko1\|\|BF:<r>` | `auc_fixed_lambda1`, `p_P_fixed_lambda1` (a permutation p-value on AUCs) |

BF_1-BF_4, base views only: 45 x 4 = 180 fits per mask per arm. Arms: A (`knockout_regrow`, 64 block
cells) and B (`knockout_regrow_block_b`, 40 block cells). GPU arithmetic is engine v3's own; no new
arithmetic. **E3 does not apply**: no continuous column reads either record (X.1; every VX2 report
prints the statement, e.g. `VX2_A_block.json:50`).

References: A's pinned store (`91035af8...`) and B's pinned pre-run store (`5d08f6e6...`), plus B's
registered run's store (`55b240a7...`) as a witness (the `reference` blocks, e.g. `VX2_A_block.json:43-48`;
`VX2_B_block_registered.json`).

## S.2 The four composition identities (G18 form: composition, world, script, compared as an AND)

Measured by VX1's three runs per composition (all equal across the runs, `passed: true`) and recorded
in each report's `VX1.composition_identity`. The arm is not hashed into the composition axis
(`ext_scope.ext_composition_digest`); it enters through the world and script axes.

| mask | arm | composition (extension digest) | world (degree-term digest) | script |
|---|---|---|---|---|
| block | A | `abce449f49a6983187d6a9e3ac588844eeba4d61de797aabda19125d0c709979` | `d48adfbd3c27c90e16c699041c5f1e3d99be21838857b2816278e9dbcc5d9d6b` | `knockout_regrow`, no lobe |
| block | B | `abce449f49a6983187d6a9e3ac588844eeba4d61de797aabda19125d0c709979` | `8533c590708e9cbde508cbf4983db370895ad0dc37fac5b490f98bdf2066298a` | `knockout_regrow_block_b`, no lobe |
| ko1 | A | `9444344eb1ff9b3376018be4e7e6d720658cddc8bb345d32b09932caef9710b1` | `d48adfbd3c27c90e16c699041c5f1e3d99be21838857b2816278e9dbcc5d9d6b` | `knockout_regrow`, no lobe |
| ko1 | B | `9444344eb1ff9b3376018be4e7e6d720658cddc8bb345d32b09932caef9710b1` | `8533c590708e9cbde508cbf4983db370895ad0dc37fac5b490f98bdf2066298a` | `knockout_regrow_block_b`, no lobe |

Carriers: `validation/VX2_A_block.json:5-12`, `VX2_B_block.json:5-12`, `VX2_A_ko1.json:5-12`,
`VX2_B_ko1.json:5-12` (identity block at lines 5-13). The A world digest equals the one registered for the
`ko` composition (`instrument.py`, `REGISTERED_COMPOSITION_IDENTITIES["A"]`, revision 1.5.1).
**Stated gap:** no code compares an extension X run with these four values. The driver refuses
arm runs (`run_ext.py` is a shim on `ext_gpu_stage.main()`; the refusal is `ext_gpu_stage.py:61-74`,
validation labels only; the G19 registry is `instrument.py:213`, `:219-243`), and VX1 compares a run's identity only with its sibling runs (`ext_compare.self_stability`).
A registered value without a check is a record, not a refusal; the check (a table in `ext_scope.py` and
a comparison in `ext_gpu_stage.py`) is a code item that belongs to the revision that lets an arm name
extension X, not to this one (S.7).

## S.3 What the validation showed, with carriers

All runs: GPU, from head `5d65baf168032eca67f337e10080fc87436de5a5`, clean tree, 2026-09-29
13:47-13:50 UTC, llama-server stopped on Mike's word (commit message of `29548f1`; manifests
`not_from_a_committed_head: false`, e.g. `VX1_A_block_20260929T134726Z_5d65baf16803/manifest.json:21`).
Registered stamp and registered VRAM need 12,550 MiB in every manifest (`vram.registered_need_mib`).
The files the runs hashed (`file_sha256_lf` in the manifests) are byte-identical at `HEAD` to the
committed ones before this revision's three edits (S.6).

| run | composition | verdict | carrier |
|---|---|---|---|
| VX0 smoke | B block, B ko1, `--worlds R:0` | both completed, rc 0 (R1, R2, R3, G11, preflight passed) | commit message `29548f1`; private folders `VX0_B_block_20260929T134717Z_5d65baf16803`, `VX0_B_ko1_20260929T134722Z_5d65baf16803`. No committed aggregate; the manifests are outside the repository |
| VX1 self-stability | A, B x block, ko1; three runs each | PASS in all four: every per-fit hash of U, V, lambda and p equal across the three runs (differ 0 in run1-vs-run2 and run1-vs-run3), one identity, stamps equal | `VX2_A_block.json:2-39`, `VX2_B_block.json:2-39`, `VX2_A_ko1.json:2-39`, `VX2_B_ko1.json:2-39` (`passed: true` at :3, `n_runs: 3` at :4, `differ: 0` at :17 and :29) |
| VX2 equivalence | each composition, run 1 against the arm's pinned store | outcome 1 EQUIVALENT in all four: E1 0 failures, 0 flipped pairs, no at-risk pair, 180 fits each | `VX2_A_block.json:41-54`, `VX2_B_block.json:41-54`, `VX2_A_ko1.json:41-54`, `VX2_B_ko1.json:41-54` |
| VX2 against B's registered store | B block | the same report as against the pre-run: outcome 1, 5 of 180 not bit-equal, the same five keys | `VX2_B_block_registered.json:4-17`, `:84`, `:111-150` |
| VX7 poisoned real block | A block, B block | PASS: run with `--poison-real-block` equal to VX1 run 1 on every per-fit hash (differ 0) and on the identity (same world digest) | `VX7_A_block.json:2-27`, `VX7_B_block.json:2-27` |
| VX6 negative control | B ko1, `--bf-tol 1e-5` | PASS by the plan's rule (X.5): the comparator's not-bit-equal set (167 of 180) equals the direct recount's (167), no E1 difference on either side, not "uninformative". The outcome was 1 (EQUIVALENT): no lambda, label or AUC moved, and none was required to | `VX6_B_ko1.json:4-17`, `:84` (167), `:3020-3028` (`direct_recount`: `agrees: true`, 167 and 167, `uninformative: false`); 19 CPU path checks on reused records all passed (`:2923-3019`) |

**Not-bit-equal fits against the CPU (diagnostic, decides nothing; E1 and E2-II hold):**

| composition | not bit-equal / 180 | which | max abs dp | carrier |
|---|---|---|---|---|
| A block | 5 | `world:No:0`..`No:4`, `block\|\|BF:4` (rank 4, lambda 1) | 2.914e-9 | `VX2_A_block.json:121-163` |
| B block | 5 | `world:No:0`..`No:4`, `block\|\|BF:4` | 1.775e-8 | `VX2_B_block.json:121-163`; the same five against B's registered store, `VX2_B_block_registered.json:84-150` |
| A ko1 | 3 | `world:M0.75:0` (9.833e-8), `M0.85:0` (2.937e-8), `M0.85:1` (1.840e-8), each `ko1\|\|BF:1` (rank 1, lambda 1 fixed) | 9.833e-8 | `VX2_A_ko1.json:121-200` (rank-and-reuse cells at :122-171; one of the three is a `reused_from_ko` record, `world:M0.85:0`; its CPU path check passed with max abs dp 0.0, `:1472-1478`) |
| B ko1 | 1 | `world:M0.85:1`, `ko1\|\|BF:1` | 2.948e-9 | `VX2_B_ko1.json:121-175` |

**Ties and gaps (reference and GPU censuses equal, number for number):** no tied pair on S(f) in any
of the four compositions. Smallest gap on S(f): A block 0.7500 (`No:0`, BF_3), B block 0.6547 (`No:0`,
BF_2), A ko1 5.040e-7 (`M0.6:0`, BF_3), B ko1 1.615e-6 (`Nf:1`, BF_2); 0 fits below 2^-23.
Carriers: `VX2_A_block.json:56-120`, `VX2_B_block.json:56-120` (gap 0.6547 at :64), `VX2_A_ko1.json:56-120`,
`VX2_B_ko1.json:56-120`; the same numbers are X.4's table (T-X4).

## S.4 What is not validated, and what a pass does not license

1. **The tie and near-tie regime (VX8).** Every block fit on A's and B's worlds is saturated: no tie
   on S(f), smallest gap 0.65 or more (S.3). E2-II cannot be exercised on the block mask there. **No
   VX8 was run** (the plan's order CPU pre-run -> VX8 -> GPU, X.7). So extension X is registered
   **only** for compositions whose **block or ko1** fits carry **no pair on S(f) with a gap below
   2^-23** (`BAND`, `census.py:28`; the at-risk flag, `census.py:89`; the count `fits_gap_below_band`,
   `census.py:132`). A tie is the case gap = 0 and is included. Any other composition needs a
   VX8-like cross-check on its own CPU pre-run store before it may name the GPU. The property decides,
   not the arm's name (Ark, X.7).
   - **Why ko1 is named too.** E2-II runs on ko1 as well, with S(f) = all pairs. There the margin is
     thin: A ko1's smallest gap is 5.040e-7 (`VX2_A_ko1.json:115-116`, `world:M0.6:0||ko1||BF:3`)
     against an observed max |dp| of 9.833e-8, a ratio of 5.1. On block the ratio is about 3.7e7
     (0.6547 against 1.775e-8). So on ko1 a gap below the band is the first thing to give way.
   - The narrower wording ("block fits", "ties") came from X.11; Ark corrected his own item at review
     (chat 2026-10-06 19:16:26 UTC).
2. **A block fit at a lambda other than 1.** On all 180 block fits of each arm both sides chose
   lambda = 1: `reference_census.lambda_by_rank` = 45 at "1.0" for each of BF_1-BF_4
   (`VX2_A_block.json:1483-1496`, `VX2_B_block.json:1483`; ko1 carries the same field,
   `VX2_A_ko1.json:1497`, `VX2_B_ko1.json:1465`), pinned by `tests_ext/test_x4_reference_census.py:33`.
   - **What is validated:** the lambda choice. E1 compares lambda, and the GPU chose what the CPU
     chose on every block fit.
   - **What is not:** a block fit at another lambda. The CPU store holds the fit at the chosen lambda
     only, so a block fit at lambda = 100 (the collapsed-lambda class: A at 100 reads 0.5000, B 0.7744)
     would be compared with a CPU fit at that lambda for the first time.
3. **Rule #2.1** (`ko1||rule`, `block||rule`, `full||rule`): CPU in every hybrid, untouched (X.2).
4. **The hybrid's CPU side for `ko1`.** G13 plans `ko` keys only and an arm copies the ko record into ko1
   where the selected lambda is 1 (X.7, last bullet). The GPU ko1 fit is made in another batch than the
   GPU ko fit, so the arm's fixed-lambda path check needs D9 (b)'s form for ko1. Code items of the
   revision that lets an arm name extension X.
5. **Any run on the real block.** None: VX7 shows the poisoned real block moves no hash; no real block
   was fitted, read or scored.
6. **The explanation of the differing fits.** Open, as V5 left it for `ko` (revision 1.5.1, R.4a). VX6
   shows only that the comparator sees a changed stopping rule.
7. **The identity check is a condition on the arm revision.** When a revision lets an arm name
   extension X, the comparison of a run with the four identities of S.2 must be a **refusal** (as G13
   is, `hybrid_arm.py:60-63`), not a log line (Johnny, chat 19:18:36 UTC).

## S.5 The envelope of the fits that differ (a known open object, same form as R.4a)

Under D6 the GPU differs from the CPU on 14 of 720 extension X fits (5 + 5 + 3 + 1): on block, only
rank 4, lambda 1, the five `No` worlds of each arm, max abs dp 2.914e-9 (A) and 1.775e-8 (B); on ko1,
only rank 1 at the fixed lambda 1, 3 fits on A (max 9.833e-8) and 1 on B (2.948e-9). None carries a tie
or an at-risk pair on its census pair set; E1 and E2-II hold (S.3). **A's `world:M0.75:0||ko1||BF:1`,
at 9.833e-8, is 82.5 % of 2^-23 (1.192e-7) and above the largest dp of any `ko` fit (5.632e-8, R.4a).**
It stays below the threshold; it is the nearest approach in X and is recorded as such. No lower
trigger is set for ko1 (Zcode, chat 2026-10-07 05:36:24 UTC): 2^-23 is the registered E2-III band, and
the S.4 item 1 bound handles the thin ko1 margin up front.

**Escalation triggers for extension X (proposed; the reviewers decide).** Any one is reported in the
chat and stops use of extension X for the arm concerned: (1) a differing fit outside S.5's cells (block:
rank other than 4 or any lambda other than 1; ko1: rank other than 1); (2) max abs dp above 2^-23 on any
fit; (3) a differing fit that carries a tie or an at-risk pair on its census pair set; (4) a count per
(rank x reused) cell above VX2's; (5) a reused-record difference whose CPU path check fails. None has
fired in VX1, VX2, VX6 (the control moves p by up to 1.09e-6 on purpose; VX6 is excluded), VX7.

**Why (2) and (3) are enough (Zcode).** A pair on a differing fit can flip only if dp exceeds its
gap. If some gap is below the band, the fit is at risk and (3) fires. If every gap is at or above the
band, then dp < band ≤ gap for any fit that (2) lets through, so no flip is possible.

## S.6 The three stale texts, fixed in this revision

All three edits are text only (a help string, a docstring, prose). Hashes (LF sha256), before as
recorded in the VX manifests, after as computed at drafting:

| # | file | what was stale | the fix | hash before -> after |
|---|---|---|---|---|
| 1 | `ext_compare.py:291-292` | the VX6 help text said the outcome "is expected to be a refusal". VX6 on B ko1 read outcome 1 and passed by the plan's rule (S.3); the plan (X.5) never required a refusal: it requires the comparator to equal the direct recount | "...passes if the comparator equals the direct recount; its outcome is not prescribed (B ko1 read outcome 1)" | `f4e585e7...ee37cf` -> `4327d134...ee475` |
| 2 | `ext_gpu_stage.py:23` | the docstring says the preflight needs "12,526 MiB at 40,000". The code asks `instrument.REGISTERED_VRAM_NEED_MIB[40000]` = 12,550 (`instrument.py:250`), and every VX manifest records `registered_need_mib` 12,550. 12,550 is V1's torch peak under D6: 12550.08 MiB in each of V1's three runs (`connectome-seed-data/gpu_instrument/V1_run_*/manifest.json`, `vram.torch_peak_alloc_mib`); 12,526 is M10's flag-free peak (registration M10) | "12,550 MiB at 40,000" | `2bb391ed...a97c` -> `9af3b95b...7560` |
| 3 | `README.md` (535 lines before and after, so the line citations README:54, :211, :241, :301, :313 of the registration and `instrument.py:248` keep their targets) | line 1 "Status (2026-09-26): not reviewed"; lines 2-6 "Registration" pointer; line 344 "None of this has been reviewed" (written in 2026-09-26, kept as history and dated); line 346 heading "not yet validated"; line 351 "Nothing here has been through V1-V8"; line 358 "`REGISTERED_STAMP` is `None` until V1's stamp is registered"; lines 383-385 "Until the revision that registers V1's results, the stamp is not registered ... an arm run refuses" | the status line says validated, reviewed as the revision files record, no registered arm names it, revision 1.6 (draft) registers extension X; the pointer lists revisions 1.5.1 and 1.6 as drafts not merged and names `run_ext.py`; the others say V0-V8 ran, V1's stamp is registered in code since `8faea07` (G17), `--stamp-unregistered` is refused, an arm run refuses every arm module (G19), and the V0-V8 manifests that say "STAMP NOT YET REGISTERED" are not edited | `6727c2d4...1cd` -> `24e680c8...700` |

Full hashes: ext_compare.py `f4e585e7d61e9a02a6e1ad15844f839bd2b142027acb92682b3ea71c37ee37cf` ->
`4327d134885cb3dfc4709a7d32f6c50c0dc5ea3eb9c9019e089dbf217c0ee475`; ext_gpu_stage.py
`2bb391ed9806f41c8faa9a3e9f74b2feadfb09b12a9011db268f4b96cba2a97c` ->
`9af3b95be49ed3073c0e7d2bc71ff1ae41b9aa8ffb95da17055e24a453ae7560`; README.md
`6727c2d4efb3af384fa2ee8701139c088826f3b273bda8a9c9eff018eedcf1cd` ->
`24e680c874160c3a76751592860e15d3ac64f440c6987e3154a55ce1cc552700`. (Any further edit of these files
changes the "after" value; re-hash before filing.)

**What these hashes mean.** `instrument.instrument_file_hashes()` (`instrument.py:340-349`) records the LF
sha256 of every `.py` file of the directory and of `README.md` in every run manifest
(`gpu_stage.py:258`, `ext_gpu_stage.py:123`). Nothing pins them to a table. The one comparison is
`hybrid_arm.check_gpu_stage` (G13, `hybrid_arm.py:60-63`): a GPU stage consumed by an arm's CPU stage must
carry file hashes equal to the CPU stage's current files. So the three edits (a) leave the VX manifests as
historical records of the files they hashed, (b) mean that any run that follows is made from a head
that contains the edits, which it records, and (c) make a GPU stage made before this revision's commit
unusable by an arm after it (none exists: no arm names the instrument). The edit of an executable
file is limited to one argparse `help=` string (it changes `--help` output only) and a module docstring.
**Disclosure:** the validated code of extension X is the code hashed in the VX manifests; the code at
the committed head of this revision differs from it by those two strings. No executable statement
changed; the `ext_*` and instrument tests do not read either string (grep, S.7).

**Residue not touched.** The docstrings of `ext_compare.py`, `ext_census.py`, `ext_engine.py`,
`ext_prep.py`, `ext_scope.py`, `ext_gpu_stage.py` (lines 1-4) and `run_ext.py` (line 1) still say "draft,
not registered", and `ext_gpu_stage.py:130` and `:206` write "draft, unregistered" into the run log and
the manifest. They are true until this revision is accepted and stale after. Editing them changes
runtime strings recorded in manifests, so it belongs to the merge step (S.8), with tests.

## S.7 Code changes and tests

**Code changes in this revision:** the two strings of S.6 (1 and 2). No other `.py` change; no row is
added to `instrument.REGISTRATION_TEXTS` (S.0). The README is not code.
**Tests that would confirm the change (not run; this draft ran nothing):**

- `tools/.venv/Scripts/python.exe -m pytest results/genome/c6/gpu_instrument/tests_ext -q`, with
  `PYTHONUTF8=1` and `CUDA_VISIBLE_DEVICES=-1`: 46 passed in about 9 s on 2026-09-29 (extension X plan
  X.8). It imports `ext_compare` (T-X3, T-X7) and so checks that the edited module still imports.
- `tools/.venv/Scripts/python.exe -m pytest results/genome/c6/gpu_instrument/tests -q`, the same
  environment: 130 passed, 16 skipped (the `needs_gpu` tests) in 27 s together with `tests_ext`: 176
  passed, 16 skipped (revision 1.5.1, R.12). Needed only because every file hash changes; no test
  there reads `ext_*.py` or the README text (grep of `tests/` and `tests_ext/` for `README`, the help
  string and `12,526`: no match).
- **Run on Mike's word, 2026-10-07, on the working tree of this revision**, `PYTHONUTF8=1`,
  `CUDA_VISIBLE_DEVICES=-1`, one pytest call per folder (the two folders each have a `conftest.py`, and
  one call over both fails at collection on the name clash): `tests_ext` 46 passed in 12.0 s; `tests`
  130 passed, 16 skipped in 17.4 s. The same counts as R.12.
- No GPU run is needed: nothing executable changed. `python ext_compare.py --help` (a CPU call of
  seconds) would show the new help text.

## S.8 Merging, and the table

When 1.5.1 and 1.6 are accepted, the merge into the registration is one step: a new status header, the
new rows, a changelog line, section 15.6/15.7 for the reviews. The new text's LF sha256 is then added to
`instrument.REGISTRATION_TEXTS` as the row `("1.6", "<merge commit>", note)`, which is a code change
with its own test (T-G11's `REGISTRATION_TEXTS` test reads `a0e16b6`'s text and the table's rows). The
commit that holds the row and the text cannot contain its own hash, so the row names the commit
that adds it, as the 1.4 row does. Until then the instrument labels a run "1.4" (the VX manifests
did), which is correct for the text it hashes.

## S.9 Ledger rows (A section 12 form) and changelog line

| item | was | correct | where the wrong wording lived | what refuted it | caught by |
|---|---|---|---|---|---|
| G-(12) | VX6's outcome "is expected to be a refusal" | the plan requires the comparator to equal the direct recount; VX6 read outcome 1 and passed, `uninformative: false` | `ext_compare.py:291-292` (help string), at `5d65baf` and before | `VX6_B_ko1.json:4`, `:3020-3028`; commit message of `29548f1` ("the driver's help text expected a refusal; none was due") | CC, 2026-09-29; this draft |
| G-(13) | the VRAM preflight need "12,526 MiB at 40,000" | 12,550 MiB (V1's peak under D6) | `ext_gpu_stage.py:23` (docstring) | `instrument.py:250`; manifests `vram.registered_need_mib`; V1 manifests `torch_peak_alloc_mib` 12550.08 | CC, 2026-09-30 (backlog); this draft |
| G-(14) | README status "not reviewed"; "V1-V8 not run"; "REGISTERED_STAMP is None" | S.6 row 3 | `README.md:1`, `:344`, `:346`, `:351`, `:358`, `:383-385` | the registration's revisions and reviews; `instrument.py:262-269`, `:286-288`; `validation/` | CC, 2026-09-30 (backlog); this draft |

**Changelog (section 14), proposed line.** Revision 1.6, 2026-10-06 UTC: extension X registered (block mask
and fixed-lambda ko1, arms A and B, base views; VX0-VX7 of `29548f1`), its four composition identities,
its envelope and escalation triggers; not registered: the tie and near-tie regime below 2^-23 on block or ko1 (VX8), a block fit at a lambda other than 1, rule
#2.1, any use by an arm; three stale texts fixed (ledger rows G-(12)-G-(14)). By a CC subagent.

## S.10 Questions for the reviewers

1. **Ark:** are S.4 items 1 and 2 the right limits? Item 1 says extension X is registered only for
   compositions whose block fits carry no tie on S(f), and any other needs its own VX8-like cross-check.
2. **Zcode:** S.5 gives X its own envelope and triggers. Is A ko1's `M0.75:0` at 9.833e-8 (82.5 % of 2^-23)
   a reason to register a lower trigger than 2^-23 for ko1, or is a recorded nearest approach enough?
3. **Johnny:** S.2 registers four identities as values with no code check (the driver refuses arm runs).
   Accept, or should the check ship in this revision (a code change with tests)?
4. **Warren:** S.6 edits two executable-file strings and a README after the validation. Is the
   disclosure in S.6 enough, or should the VX runs be repeated (a GPU run, on Mike's word)?
5. **All:** the residue of S.6 ("draft, not registered" in docstrings and in two run-log strings) is left
   for the merge step. Agree, or fix them here?
6. **Mike:** (a) your word on the revision; (b) merge 1.4 + 1.5.1 + 1.6 into the registration in one
   commit (S.8), or keep the draft files until an arm needs the instrument.
