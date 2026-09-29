---
**Status: DRAFT, revision 1.5.1 of the GPU instrument registration, 2026-09-29 UTC: revision 1.5
(committed as `030b974`) with the reviewers' edits applied.** Warren (08:34:21), Ark (08:37:58),
Johnny (08:40:48) and Zcode (08:49:04 UTC) voted yes on `030b974` with edits (R.11; the reviews are
cited as relayed by CC, the chat is not in the repository). Revision 1.5.1 is no longer text only:
Ark's condition (Zcode agreeing) puts G19 in the same revision that registers the stamp, so G17,
G18, G19 and G-(10)'s fix are made in the working tree, uncommitted (R.12), with their tests; the
one run made for it is V5 (c), CPU only, 3 s (R.4a). No GPU run was made. It carries what §7 ("Order") of
`docs/plans/2026-09-26-gpu-instrument-registration.md` requires of "a revision of this file, which
registers the refusal digest, the stamp measured in V1 (D7), the set of differing base fits with
the counts per cell and A's census (ties, gaps, at-risk list, 0 flips expected, each per column
family), and whether `row_chunk` stays out of the digest (V4 (c))". It also carries the item the
backlog entry A-BATCHED-GPU-INSTRUMENT-... lists as pending: every census number with its scope
label.

**Why a separate file.** The registration is the registered text under which V0–V8 ran (its
revision 1.4 at `e2fab47`, with §15.5 added in `a0e16b6`); the validation records name it by
revision and commit. The brief for this draft forbids editing a registered file. So revision 1.5 is
drafted here, written as sections that can be merged into the registration unchanged (a new status
header, new rows M21–M27 of §2, a new §7.2, new ledger rows, a changelog line, and §15.6 for the
reviews), once the reviewers and Mike accept it. Until then the registration stays at revision 1.4
and nothing in this file changes a gate.

**Plan approved by Mike** (DPC Research chat, 2026-09-29 08:08:12 UTC, "yes GPU plan", translated from Russian, as
recorded in `backlog.md`): (1) this revision, reviewed; (2) validation extended to the block mask
and to fixed-λ fits (a separate plan: `docs/plans/2026-09-29-gpu-instrument-extension-x-plan.md`);
(3) the next registered knockout registration runs on the GPU, with the instrument named before its
pre-run. Drafted by a CC subagent; CC checks it; the reviewers (Ark, Johnny, Zcode) review it;
Mike gives his word.

**Sources read for this draft** (read-only): the registration at `HEAD` (`0e16c9e`; the file is
unchanged since `a0e16b6`), `results/genome/c6/gpu_instrument/validation/V0.json`–`V8_R.json` and
`table.json` (committed in `e50bf74` and `0c7a67b`), the run manifests under
`connectome-seed-data/gpu_instrument/` (V1's three runs, V4c, V8 L and R), `instrument.py`,
`gpu_stage.py`, `hybrid_arm.py`, `census.py`, `gpu_equivalence.py` at `HEAD`.
---

# GPU instrument registration, revision 1.5.1 (draft): V1's stamp, the composition identity, A's census with scope labels, G17–G19

## R.0 What revision 1.5 changes, and what it does not

It **registers values** that V0–V8 measured: the environment stamp (D7), the refusal digest of
A's composition (D5), `row_chunk` outside the digest (V4 (c)), the differing base fits and their
counts per cell, and A's census per column family, each number with its scope. It **corrects**
the status header (stale since `e2fab47`), the revision label of the V0–V7 records, and §9's
economics (V1 measured a slower GPU pass than M9). It **closes three gaps** found while drafting
(R.7) with code items G17–G19 (revision 1.5.1: made, R.12), registers **the composition identity**
(R.3, G18), and registers **the envelope of the five differing fits** as a known open object with
escalation triggers (R.4a).

It does not change E1, E2, E3 or D1–D13. It tightens two refusals: R4 compares the composition
identity instead of the digest alone (G18), and the driver refuses every arm module outside a
closed registry (G19); it does not register extension X
(the block mask and fixed λ), which has its own plan; it does not let any arm use the instrument
(D11 stands: an arm names it before its pre-run).

## R.1 The status header (replaces lines 1–22 of revision 1.4)

Revision 1.4's header still reads "DRAFT", "Not committed", "Zcode's review of revision 1.3 ...
pending" and "nothing has been fitted for this file yet". Each is now false: revision 1.4 was
committed as `e2fab47`; Zcode confirmed revisions 1.3 and 1.4 at 12:56 UTC (§15.5, added in
`a0e16b6`); V0–V7 ran at head `a0e16b6` (13:13–16:44 UTC) and V8 at head `e50bf74` (16:46–18:19 UTC),
all on 2026-09-26. Proposed header:

> **Status: revision 1.5, 2026-09-29 UTC. Revision 1.4 (`e2fab47`) was reviewed by Ark (12:09
> UTC) and Zcode (12:56 UTC) and carried Mike's word (~12:15 UTC); V0–V7 ran at `a0e16b6`, V8 at
> `e50bf74`; their aggregates are in `results/genome/c6/gpu_instrument/validation/` (`e50bf74`,
> `0c7a67b`). Revision 1.5 registers V1's stamp, A's composition digest and A's census (§7.2).
> No arm names the instrument yet (D11).**

## R.2 The registered environment stamp (D7, R1)

Measured by V1 in each of its three runs and equal across them (`V1.json`,
`details.stamps_equal_across_runs = true`); the same stamp was recorded by V0, V4 and V8. It
becomes the registered stamp: every later GPU run (an arm's pre-run and registered run included)
must equal it field by field (R1), not only its own pre-run.

| field | registered value |
|---|---|
| python | 3.10.20 |
| numpy | 2.2.6 |
| torch | 2.9.1+cu128 |
| cuda | 12.8 |
| `cublas64_12.dll` sha256 | `9513540e4ec4c51ee9e7304138c2cc255c29a8c181f9e80c38efa25738becd99` |
| `cublasLt64_12.dll` sha256 | `b199d1ff892a81b7fd3d57ba1781549609b41500b36008fef326038393ad46c7` |
| `cusolver64_11.dll` sha256 | `3d4f7a66b5f352db56d4bb5962bb453a42d5feb2d831779f4a0bebc9971c36fb` |
| driver | 596.86 |
| gpu_name | NVIDIA RTX PRO 4500 Blackwell |

The interpreter is `autoresearch-win-rtx/.venv` (D7 (i)). **Two witnesses** (revision 1.5.1,
Ark's edit): (1) V1, 2026-09-26, the three runs equal; (2) Ark's field-by-field reading on
2026-09-29 (chat 08:37:58 UTC): driver 596.86, the three DLL hashes, python 3.10.20, numpy 2.2.6,
torch 2.9.1+cu128, all equal to the table. (The drafter's `nvidia-smi` query of the same day also
read driver 596.86.) **G17 (made, R.12):** `instrument.REGISTERED_STAMP` holds this dict; since it
is registered, `--stamp-unregistered` is refused (`check_stamp`, unchanged) and a different field
refuses (R1). T-G6's placeholder assertion `REGISTERED_STAMP is None` is replaced by a test that
the registered stamp is V1's, read from `V1.json`.

## R.3 The registered refusal digest of A's composition (D5, R4) and `row_chunk` (V4 (c))

| item | value (source: the three V1 manifests, V4c's manifest) |
|---|---|
| refusal digest | `a6a8a0dfd445f0dcc69fe29602af50b074e4534418082d37757c4580fdd72e8e` |
| covers | the ordered key list, `starts`, the rank order (D5 (a)) |
| ordered key list | 4,500 keys: every world's 99 shuffles in A's `world_specs()` order, then the 45 base views; `keys_sha256` `1d0f24a79036b9473898b7d9ee8a95d6a3f4ffb0796044d8a2f1e9258dab1165` |
| starts | 10 |
| ranks | 1, 2, 3, 4 |
| `row_chunk` (recorded, not in the digest) | 40,000: 4,000 problems per block; per rank 225,000 inner (bank, fold, λ) problems in 57 blocks, then 4,500 final problems in 2 |
| V4 (c): `row_chunk` 100,000 | 0 of 18,000 per-fit hashes differ from V1 run 1 (`V4.json`); E outcome 1 |

**`row_chunk` stays out of the refusal digest** (D5's condition "if any hash changes there,
`row_chunk` returns to the refusal digest" did not occur). R5 still catches any `row_chunk` change
between an arm's GPU pre-run and its run. V4c's torch peak at `row_chunk` 100,000 was 24,300 MiB
(its manifest), below the registered 26.5 GB need (README:301, `REGISTERED_VRAM_NEED_MIB`), which
stays as it is (conservative). At 40,000 the three V1 runs peaked at 12,550 MiB each, 24 MiB above
the registered 12,526 MiB (M10, flag-free); the need is a preflight on free memory before the
upload, and 31,312 MiB were free in every V run, so nothing turned on it. **The registered need
at `row_chunk` 40,000 becomes 12,550 MiB**, V1's measured torch peak under D6 (Ark, Zcode: the
need is the peak of the registered configuration, not of the flag-free one; lesson 157). Warren
preferred to keep 12,526 MiB (M10); his view is recorded. The 24 MiB between the two decide nothing
while llama-server is stopped (31,312 MiB free), and both refuse beside it (about 4,900 MiB free
on 2026-09-29). **G17 (made):** `REGISTERED_COMPOSITION_DIGESTS["A"] = "a6a8a0df..."`,
`REGISTERED_VRAM_NEED_MIB[40000] = 12550`.

**The digest does not bind the arm (a gap; R.7 (1)).** V8's two runs (the male arm, lobes L and R)
carry the same refusal digest `a6a8a0df...` and the same `keys_sha256` as V1: the key strings
`world:<family>:<j>[|sh:<sd>]` are the same in every arm, and the digest covers only the strings.
What tells the three compositions apart is the arm module, the lobe and the degree-term digest
(A `d48adfbd...`, male L `03ede4ed...`, male R `ca2aac16...`), all in the manifests. The hybrid's
CPU stage refuses a GPU store made for another arm through D10 (G13 compares the degree-term
digest with its own, `hybrid_arm.check_gpu_stage`), so no wrong store can enter an arm; but R4
alone does not refuse it.

**The composition identity (G18; revision 1.5.1, as Ark, Zcode and Johnny preferred).** One named
object that R4 compares **as a whole**: an AND of three values, not a re-hash of them (a recomputed
digest would be a value no run has witnessed). Its three axes:

| axis | what it binds | value for A (V1's manifests) |
|---|---|---|
| **composition** | the keys: the refusal digest of D5 (ordered keys, starts, ranks) | `a6a8a0dfd445f0dcc69fe29602af50b074e4534418082d37757c4580fdd72e8e` |
| **world** | what the banks are built from: the degree-term digest (D10) | `d48adfbd3c27c90e16c699041c5f1e3d99be21838857b2816278e9dbcc5d9d6b` |
| **script** | the arm module and its lobe | `knockout_regrow`, no lobe |

The identity rests on the content: the world axis is the digest of the degree terms every bank is
built from, so a bank set of another arm cannot pass it; the module name is a label, compared as a
string beside it. Registered: `REGISTERED_COMPOSITION_IDENTITIES["A"]` (V1's triple; V8's lobes
share its composition axis and differ on world and script, T-G11). An arm run names the identity
it expects (`--expect-identity`; an arm run with `--expect-digest` alone is refused as arm-blind);
the driver compares the run's identity with it after the degree terms are computed, and the CPU
stage (G13) compares the GPU stage's identity with the arm's when given (`check_gpu_stage(...,
expected_identity=)`). The same binding applies to the `ko` composition here and to extension X's
compositions (its plan, §X.5; Zcode X.10.5).

## R.4 The differing base fits under D6 and the counts per cell (V1, V2)

V1 (three runs, every per-fit hash of U, V, λ and p equal, 18,000 × 3) and V2 (V1 run 1 against
A's pinned store, `sha256 91035af8...`, after `check_prerun_files`): **outcome 1** (E1 0 failures,
E2-II 0 flipped pairs, E3 0 failures). The base fits whose `p` differs from the CPU under D6 are
M3's five, the same set as the flag-free v3 run (`V1.json`, `same_as_M3 = true`):
`world:M0.75:0`, `M0.85:0`, `M0.85:2`, `M1.0:0`, `M1.0:4`, each `||ko||BF:1`.

| cell (scope: D1, the 18,000 `ko` BF fits of A) | not bit-equal / denominator (from the pinned λ) |
|---|---|
| rank 1, λ ∈ {1, 3}, base view | 5 / 37 (λ 1: 2 / 19; λ 3: 3 / 18) |
| rank 1, λ ∈ {1, 3}, shuffle | 0 / 164 |
| rank 1, λ = 100 | 0 / 4,299 |
| ranks 2–4, any λ | 0 / 13,500 |

None of the five carries a tie on its census pair set (`differing_fits_that_carry_ties = 0`).
Their E3 checks passed (V3: the five rows of `synthetic_worlds.csv`, `D` and `logloss` within
their per-fit bounds; e.g. `M0.75:0` BF_1: |ΔD| 3.05e-8 against the bound 5.29e-7).

## R.4a The envelope of the five: a known open object (Zcode (a), (b))

**Registered as open, not explained.** Under D6 the GPU differs from the CPU on exactly five fits
of A's D1: `world:M1.0:0`, `M1.0:4`, `M0.75:0`, `M0.85:0`, `M0.85:2`, each `||ko||BF:1`, base view.
**Their envelope**: every one is rank 1, λ ∈ {1, 3}, base view; max |Δp| 1.631e-8 to 5.632e-8;
0 ties and 0 at-risk pairs on their census pair sets (smallest all-pairs gap 2.01e-5, more than
600 times 2 · max |Δp|, §5); E1 and E3 hold; the set is the same flag-free and under D6. V8 found
the same pattern on the male worlds (8 and 3 fits, all rank 1, base, λ ∈ {1, 3}, none carrying
ties).

**V5 (c) (revision 1.5.1; CPU, float64, 3 s; `v5c_cpu_recount.py`; report
`connectome-seed-data/gpu_instrument/V5c_20260929T085955Z_10e806cdd755/v5c.json`).** The five and
five controls (`world:R:0`–`R:4` BF_1, V5 (b)'s) refitted with the harness's own calls at their
pinned λ: all ten reproduce the pinned `p` bit for bit at the registered stop (`BF_TOL` 1e-6).
Tightening the Newton stop to 1e-8, 1e-10 and 1e-12 moves the five's float64 BF logit term by up to
6.9e-8 to 1.4e-7 and their decoded `p` by 2.3e-8 to 5.4e-8 (5 of 5 at 1e-10): the size of the
GPU–CPU differences (1.6e-8 to 5.6e-8). `M1.0:0` at 1e-10 lands on V1's GPU `p` bit for bit; the
other four match the GPU at no stop tried. On the controls the same tightening moves the term by
at most 2.3e-9, and the decoded `p` of 1 of 5 (`R:1`, 1.65e-8, a fit the GPU matches bit for bit
at the registered stop). The float32 cast margins of U and V do not separate the groups (the
controls' smallest margin is 1.3e-4 float32 steps, the five's 2.3e-3). **Reading (a statement,
non-blocking):** the registered stop does not fix the five's decoded `p` to better than about
5e-8, and the GPU's answers lie inside that stopping envelope. Which arithmetic difference picks
the GPU's point stays open, as V5 left it.

**Escalation triggers** (any one is reported in the chat and stops the use of the instrument for
the arm concerned until the reviewers decide): (1) a differing fit outside the envelope's cell
(rank ≥ 2, λ = 100, or a shuffle) in any run with a CPU reference; (2) max |Δp| above 2^-23 =
1.19e-7 on any fit; (3) a differing fit that carries a tie or an at-risk pair on its census pair
set; (4) a count per (rank × λ × view) cell above V1's (already §5's rule); (5) an E3 check that
uses more than half its bound. None has fired in V1, V2, V4 or V8.

## R.5 A's census, every number with its scope (V2; M20 restated)

**The scope labels.** Each census number below carries one of five scopes. The JSON outputs of
`census.family_summary` use two labels that do not name a scope, so they are mapped here:

| scope label (this revision) | what it counts | JSON label it replaces |
|---|---|---|
| **store** | every record of A's pinned store, 28,665 (all masks, predictors, views, `\|pc:`) | none (M20's "all 28,665") |
| **D1** | the 18,000 `ko` BF_1–BF_4 fits, base views and shuffles: what the GPU makes | "auc (pa pairs, every fit)" and "S(f)" in V2 (their "every fit" is every fit of the compared set, which in V2 is D1) |
| **D1 base ko** | the 180 base-view `ko` BF fits of D1 | "auc_null (all pairs, base ko/ko1)" in V2 and V8: **no `ko1` record was ever in a GPU run** (D1 (a)), so the "/ko1" in that label counted nothing |
| **base ko, six predictors** | the 270 base-view `ko` fits of all six predictors (CPU fits outside D1 included) | none (§5's "for comparison") |
| **V6 subset** | the 359 BF-active D1 fits V6 drew | the same two JSON labels in `V6.json` |

The same mapping holds for V8 per lobe (scope **male D1**, 18,000 per lobe; **male D1 base ko**,
180). Extension X's census (`ext_census.family_summary_scoped`) writes the scope into every family
name, so new records need no mapping.

**A's census in scope D1 (V2, reference and GPU sides equal, number for number):**

| family (pair set) | scope | fits | fits with a tie | tied pairs | pairs (per-fit denominators summed) | smallest gap (where) | at risk (< 2^-23) |
|---|---|---|---|---|---|---|---|
| `auc` (present × absent, own `y`) | D1 | 18,000 | 17,604 | 423,777 | 17,439,428 | 9.079e-8 (`M0.85:2\|sh:79`, BF_1) | 4 |
| `auc_null` (all 2,016) | D1 base ko | 180 | 41 | 1,538 | 362,880 | 1.586e-6 (`M1.0:3`, BF_1) | 0 |
| S(f) | D1 | 18,000 | 17,613 | 424,535 | 17,617,988 | 9.079e-8 | 4 |

**Flipped pairs: 0 in scope D1** (counted by V2 on saved `p`, where revision 1.4 had derived it).
**At-risk list (E2-III), scope D1:** `world:M0.85:2|sh:79||ko||BF:1`–`BF:4`, gap 9.079e-8 on
cells 50 (present) and 59 (absent), `p` equal to the view's N1 `p` on both sides, AUC equal.
**BF-active, scope D1:** 359 (33 at λ 1, 323 at λ 3, 3 at λ 100: `world:W:4|sh:84`, BF_2–BF_4).

**Store-wide and other scopes (M20, unchanged numbers, labels added):** store, present × absent:
27,123 records with a tie, 782,376 tied pairs; store, all pairs: 27,563, 1,851,770; store, at
risk on each record's own census pair set: 6; base ko, six predictors, all pairs: 114 fits,
4,370 tied pairs, smallest gap 1.702e-7; `|pc:` (900, present × absent): 502 fits, 7,828 tied
pairs.

**The male worlds (V8, a cross-check; decides nothing for the male arm):**

| lobe | scope | S(f): fits with a tie / tied pairs / smallest gap | at risk | not bit-equal (all rank 1, base, λ ∈ {1, 3}) | differing fits with ties | BF-active |
|---|---|---|---|---|---|---|
| L | male D1 | 17,420 / 475,457 / 1.968e-7 | 0 | 8 of 38 | 0 | 557 |
| R | male D1 | 17,478 / 456,929 / 1.063e-7 | 1 | 3 of 38 | 0 | 503 |

Lobe R's at-risk fit `world:M0.5:0|sh:98||ko||BF:1` (gap 1.063e-7, cells `Tm9->T4a` present and
`Tm4->T4a` absent) is BF-active (its `p` is not its N1's) and its GPU pair equals the reference bit
for bit: the first case of E2-III exercised on a BF-made pair. Zcode's synthesis of §15.5 ("E2-III
cannot be exercised inside D1 on A's worlds") stands for A; V8 R supplies the live case.

## R.6 The other validation results (for the record; each a PASS or a statement)

| run | outcome | what it shows |
|---|---|---|
| V0 | PASS | R1–R4 with the settings on; no `RuntimeError`; 0 of 400 hashes differ between settings on and off; GPU time ×1.07 |
| V3 | PASS | A's own gate on the hybrid store: every exact column and string equal; E3 on the five rows; the D9 (b) path check on `world:W:0`; `ko1` 47 copied / 178 fitted |
| V4 | STATEMENT | batch composition moves hashes (V4a: 12 of 180; V4d: 9 of 90; V4b: 1 of 4 in each of three single-world runs), E outcome 1 under every composition; `row_chunk` moves none (V4c) |
| V5 | STATEMENT, neither refused nor explained; (c) added in revision 1.5.1 (R.4a) | (a) CPU with 4 BLAS threads: 0 base fits moved, M3's five included; (b) engine v3 on the torch CPU device: 3 of M3's five differ from the CPU harness, 1 equals V1's GPU `p`, 5 of 5 controls equal both. So the five are not "a property of the fits under any change of reduction order" (V5's prediction), and not reproduced as a pure GPU effect either; §7's refusal condition ("(a) moves none and (b) reproduces them") is not met, since (b) did not reproduce them. The explanation of the base differences stays open |
| V6 | PASS (the comparator equals the brute-force recount on all 359 BF-active fits) | with `BF_TOL` 1e-5, 321 of 359 fits not bit-equal; the comparator refused it (outcome 3: 2 E1 failures, AUC of `world:W:4\|sh:84` BF_2 and BF_4, and 10 flipped pairs): the gates bite on a real change |
| V7 | PASS | 400 of 400 hashes and the degree-term digest equal with the real block poisoned |
| V8 L, R | CROSS-CHECK EQUIVALENT (outcome 1) | R.5 |

## R.7 Findings while drafting (revision 1.5.1: the code items made, R.12)

1. **The refusal digest is arm-blind** (R.3). **G18 (made):** R4 compares the composition
   identity (composition, world, script) as a whole.
2. **The GPU stage does not refuse an arm module it has no adapter for.** `gpu_stage.refusals`
   restricts only modules listed in `prep.ARM_ADAPTERS` (the male arm). `--kind arm
   --arm-module knockout_regrow_block_b` passes `refusals()` (block B's module has A's interface,
   so `prep.set_arm` loads it directly); only the stamp (R1) and `--expect-digest` (R4, arm-blind)
   stand in the way, and D11 is enforced by procedure. `gpu_stage.py`'s module header (:26–29 at
   `HEAD`) already described a closed set; the code enforced only the male adapter (:166–204).
   **Ark's condition (Zcode agreeing): G19 goes in the same revision that registers the stamp.**
   Today an arm run is refused only because R1 fails (no stamp); once G17 registers the stamp that
   refusal is gone, and without G19 a window would open that does not exist today. **G19 (made):**
   `instrument.arm_module_refusal`, called by `refusals()`, refuses in an arm run every module not
   in `REGISTERED_ARM_MODULES` (registered: none), and in a validation run every module not in
   `VALIDATION_ARM_MODULES` (A's script under every label; the male arm's only as V8 and smoke,
   with a lobe). Extension X's driver is separate (`ext_gpu_stage.py`) and refuses arm runs
   altogether. Ledger row G-(11).
3. **G11 does not name block B's folders.** `instrument.reference_dirs()` lists A's pinned folder,
   the flyvis-65 run's folder and the male arm's folders; block B's pinned pre-run folder
   (`synthetic_blockB_prerun_20260927T211052Z_5f9cc51b9a24`) and B's registered run folder
   (`flyvis65_blockB_20260928T143258Z_7a10d88ec95e`) are not refused as output folders. Extension X's
   guard (`ext_scope.ext_out_dir_refusal`) adds them; revision 1.5.1 adds them to
   `reference_dirs()` (`instrument.BLOCK_B_REFERENCE_DIRS`).
4. **The V0–V7 records name revision 1.3.** Their `registration` field reads "revision 1.3
   (`ec5cbc0`)" with an `applied_ahead` note, while head `a0e16b6` carried revision 1.4's text
   (committed `e2fab47`) and §15.5: `instrument.REGISTRATION_REVISION` was still "1.3" at
   `a0e16b6` and was updated in `1ad6155`, before V8. The records wrote the hand-set constant, not
   the text: the label followed an edit of `instrument.py`, not the registration. **Fix (made, Ark's
   edit):** the label is derived from the text's content hash (`instrument.REGISTRATION_TEXTS`, the
   LF sha256 of each committed revision mapped to its revision, commit and note;
   `registration_text_record()`); a text not in the table is labelled UNKNOWN, and manifests and
   validation rows record the hash. The V0–V7 records are **not edited**. Ledger row G-(10).

## R.8 Economics under D6 (§9, corrected)

§9 used M9, the flag-free v3 run (2,362 s end to end, GPU 2,221 s). Under D6 the full composition
measured, end to end: V1 2,888 / 2,841 / 2,858 s (GPU 2,441 / 2,388 / 2,399 s; prep 430–440 s);
V8 L 2,697 s (GPU 2,360 s; prep 319 s); V8 R 2,424 s (GPU 2,323 s; prep 93 s). The GPU phase is
5–10 % slower than M9 (V0's ×1.07); the prep phase varies 93–440 s with the machine's load (M9:
138 s). A hybrid pass is therefore about 2,526 + (2,424 to 2,888) ≈ 4,950–5,410 s, a saving of
about 2,430–2,900 s (**41–48 min, −31 % to −37 %**) against 7,846 s, not revision 1.4's 49 min
(−38 %). The break-even moves from 1.7 arms to about 1.8–2.1 arms (2 h 50 min of validation against 82–96 min saved per arm, two passes each); the
instrument still pays from the second arm that names it.

## R.9 Ledger row (A §12 form) and changelog line

| item | was | correct | where the wrong wording lived | what refuted it | caught by |
|---|---|---|---|---|---|
| G-(10) | "registration ... revision 1.3 (ec5cbc0)" in the V0–V7 records | revision 1.4 (`e2fab47`, with §15.5 added in `a0e16b6`; LF sha256 `0f5be2fc...`) was the text at the runs' head `a0e16b6`; the records wrote a hand-set constant, not the text; the fix derives the label from the text's hash, and the records stay as written | `validation/V0.json`–`V7.json`, field `registration`; `instrument.py:34–35` at `a0e16b6` | `git show a0e16b6:docs/plans/2026-09-26-gpu-instrument-registration.md` (header "revision 1.4"); `1ad6155` (the constant hand-edited); T-G11 | this draft; Ark (the fix) |
| G-(11) | "`--arm-module knockout_regrow_male_cns` ... refused in an arm run and under any other validation label" (`gpu_stage.py` header :26–29), read as the whole rule for arm modules | the code refused only the male adapter; any other module with A's interface (block B's script) passed `refusals()` in an arm run, held back only by R1 (no stamp) and an arm-blind R4 | `gpu_stage.py:166–204` at `HEAD` | reading the code; T-G11's driver test (block B's script refused since G19) | this draft (R.7 (2)); Ark (the condition on G19) |

**Changelog (§14), proposed lines.** Revision 1.5, 2026-09-29 UTC (`030b974`): V1's stamp
registered (D7); A's refusal digest `a6a8a0df...` registered (D5); `row_chunk` stays outside the
digest (V4 (c)); the differing base fits (M3's five) and the counts per cell; A's census with a
scope label on every number, and the JSON labels mapped; V0–V8 outcomes recorded; §9 corrected
under D6; the status header brought up to date; G17–G19 proposed; ledger row G-(10). By a CC
subagent. Revision 1.5.1, 2026-09-29 UTC: the reviews of Warren, Ark, Johnny and Zcode applied
(R.11): G17, G18 (the composition identity), G19 (the arm-module registry, in the same revision as
the stamp) and G-(10)'s fix made in code with tests (R.12); the VRAM need 12,550 MiB; the stamp's
two witnesses; the envelope of the five registered as a known open object with escalation
triggers, and V5 (c) run (R.4a); ledger rows G-(10) (rewritten) and G-(11). By a CC subagent.

## R.10 Questions for the reviewers (revision 1.5; answered in R.11)

1. **Ark:** is the triple (refusal digest, arm module and lobe, degree-term digest) the right
   binding for R4, or should the arm and the degree-term digest enter the digest itself (which
   would change the value V1 measured, so V1's digest would be recomputed, not re-measured)?
2. **Zcode:** V5 found neither outcome §7 wrote down. Is "a statement, the explanation open" the
   right record, or does V5 (b)'s split (3 of 5 differ on the torch CPU device, 1 equals the GPU)
   call for a V5 (c) before an arm names the instrument?
3. **Johnny (reads revision 1.4 for the first time):** the scope table of R.5 maps the JSON
   labels without renaming them in `census.py` (a registered file). Enough, or should G16's labels
   be renamed in code (a code change with its own tests)?
4. **All:** the registered VRAM need at `row_chunk` 40,000: keep 12,526 MiB (M10, flag-free) or
   take V1's 12,550 MiB (D6)? The preflight decides nothing while llama-server is stopped (31,312
   MiB free), but refuses beside it (about 4,900 MiB free on 2026-09-29).
5. **All:** G19 would refuse `--kind arm` for every arm module until a revision registers one.
   Is that the wanted default for step (3) of Mike's plan (the next knockout registration on the
   GPU), which would then register its own module and triple before its pre-run?
6. **Mike:** revision 1.5 changes no gate and registers measured values only. It needs the
   reviewers' yes and your word before it is merged into the registration and committed.

## R.11 Reviews of revision 1.5 (`030b974`; DPC Research chat, 2026-09-29 UTC, as relayed by CC)

| reviewer | time (UTC) | vote | edits |
|---|---|---|---|
| Warren | 08:34:21 | yes, with edits | keep the VRAM need at 12,526 MiB (not adopted; recorded, R.3) |
| Ark | 08:37:58 | yes, with a condition and edits | G19 and `REGISTERED_ARM_MODULES` in the same revision as the stamp; the triple as one object compared as a whole; VRAM 12,550 MiB; the stamp re-read field by field (second witness); G-(10) fixed by deriving the label from the content hash, old records not edited; scope lines in the X plan |
| Johnny | 08:40:48 | yes, with edits | the identity as an AND, not a re-hash; list the registered code files that change and add a ledger row; run the existing `tests/` suite if CUDA is not needed at collection, else say so; the X plan's line for Mike on the calibration |
| Zcode | 08:49:04 | yes, with edits | agrees with Ark's condition; the identity, also for `ko` (X.10.5); VRAM 12,550 MiB; the envelope of the five as a known open object with escalation triggers; V5 (c) as a cheap non-blocking float64 CPU recount; in the X plan: keep the 29 ko1 copies (rider: a difference in a reused cell gets the CPU path check first), run VX6 on ko1 (B), two text fixes in X.8 |

Answers to R.10: (1) the triple as one named object, the composition identity, compared as an AND
(R.3); (2) V5 stays a statement, and V5 (c) is added (R.4a); (3) the mapping of R.5 is kept, and
new code carries the scope as a field (`ext_census`); (4) 12,550 MiB, Warren's 12,526 recorded;
(5) yes: G19 refuses every arm module until a revision registers one; (6) open: Mike's word.

## R.12 Code of revision 1.5.1 (working tree, uncommitted)

**Registered code files that change** (each is in the manifests' `file_sha256_lf`, so the next
run's manifest records new hashes):

| file | change |
|---|---|
| `results/genome/c6/gpu_instrument/instrument.py` | G17: `REGISTERED_STAMP` (V1's), `REGISTERED_COMPOSITION_DIGESTS["A"]`, `REGISTERED_VRAM_NEED_MIB[40000] = 12550`; G18: `IDENTITY_AXES`, `REGISTERED_COMPOSITION_IDENTITIES["A"]`, `composition_identity`, `check_composition_identity`; G19: `REGISTERED_ARM_MODULES` (empty), `VALIDATION_ARM_MODULES`, `arm_module_refusal`; G-(10): `REGISTRATION_TEXTS`, `registration_text_record`, and `REGISTRATION_REVISION` / `_COMMIT` / `_NOTE` derived from the text's hash; R.7 (3): `BLOCK_B_REFERENCE_DIRS` in `reference_dirs()`; the module docstring |
| `results/genome/c6/gpu_instrument/gpu_stage.py` | G19: `refusals()` calls `arm_module_refusal` in place of the male-only check; an arm run needs `--expect-identity` (G18); the identity is computed after the degree terms and checked; the manifest records `composition_identity`, its check and `registration_text`; `MALE_ARM_LABELS` read from the registry; the module docstring |
| `results/genome/c6/gpu_instrument/hybrid_arm.py` | G18 in G13: `check_gpu_stage(..., expected_identity=None)` compares the GPU stage's identity when given |
| `results/genome/c6/gpu_instrument/validation.py` | the validation row records `registration_text_sha256_lf` |
| `results/genome/c6/gpu_instrument/tests/test_tg6_stamp.py` | the placeholder `REGISTERED_STAMP is None` replaced by `test_registered_stamp_is_v1s`; the unregistered mode tested with `use_module_default=False` |

**New files:** `tests/test_tg11_registry.py` (T-G11: G19's registries; the driver refusing block
B's script in an arm run; G18 on V1's and V8's manifests and in G13; G-(10)'s derived label and the
V0–V7 fact; the VRAM need; B's folders in `reference_dirs()`); `v5c_cpu_recount.py` (V5 (c)).
Extension X's files are listed in its plan.

**Tests** (tools/.venv, `PYTHONUTF8=1`, `CUDA_VISIBLE_DEVICES=-1`, 2026-09-29):
`pytest results/genome/c6/gpu_instrument/tests_ext results/genome/c6/gpu_instrument/tests`:
**176 passed, 16 skipped** (46 in `tests_ext/`, 130 in `tests/`, 27 s). The 16 skipped are the `needs_gpu` tests (T-G1, T-G2's driver cases, T-G5, T-G6's
real-stamp case, T-G7, V8's two driver tests). `tests/conftest.py` does ask CUDA at collection
(`torch.cuda.is_available()` in a torch-venv subprocess); with `CUDA_VISIBLE_DEVICES=-1` it
answers no and the GPU tests skip. A first attempt with the variable set empty did not hide the
device from that probe: the GPU tests started and failed at `torch.cuda.get_device_name`
("Invalid device id") before any allocation (GPU memory 27,800 MiB before, 27,757 MiB after;
llama-server untouched); its results are not used. The GPU tests were not re-run.
