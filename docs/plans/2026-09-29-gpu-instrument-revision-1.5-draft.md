---
**Status: DRAFT, revision 1.5 of the GPU instrument registration, 2026-09-29 UTC. Text only: no
run was made for it, no code was changed for it.** It carries what §7 ("Order") of
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

# GPU instrument registration, revision 1.5 (draft): V1's stamp, the composition digest, A's census with scope labels

## R.0 What revision 1.5 changes, and what it does not

It **registers values** that V0–V8 measured: the environment stamp (D7), the refusal digest of
A's composition (D5), `row_chunk` outside the digest (V4 (c)), the differing base fits and their
counts per cell, and A's census per column family, each number with its scope. It **corrects**
the status header (stale since `e2fab47`), the revision label of the V0–V7 records, and §9's
economics (V1 measured a slower GPU pass than M9). It **names three gaps** found while drafting
(R.7) and proposes their fixes as code items G17–G19, not made here.

It does not change E1, E2, E3, R1–R7, D1–D13 or any refusal; it does not register extension X
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

The interpreter is `autoresearch-win-rtx/.venv` (D7 (i)). Checked on 2026-09-29 by a read-only
`nvidia-smi` query while drafting: the driver is still 596.86. Code item **G17** (not made here):
`instrument.REGISTERED_STAMP` takes this dict, after which `--stamp-unregistered` is refused
(`instrument.check_stamp` already refuses it once a stamp is registered). T-G6 and T-G5/T-G7 pass
`--stamp-unregistered` only while `REGISTERED_STAMP is None`, so they follow without an edit.

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
upload, and 31,312 MiB were free in every V run, so nothing turned on it. Code item **G17** writes
`REGISTERED_COMPOSITION_DIGESTS["A-45-worlds-99-shuffles"] = "a6a8a0df..."` and proposes the need
at 40,000 as 12,550 MiB (V1's measured peak under D6).

**The digest does not bind the arm (a gap; R.7 (1)).** V8's two runs (the male arm, lobes L and R)
carry the same refusal digest `a6a8a0df...` and the same `keys_sha256` as V1: the key strings
`world:<family>:<j>[|sh:<sd>]` are the same in every arm, and the digest covers only the strings.
What tells the three compositions apart is the arm module, the lobe and the degree-term digest
(A `d48adfbd...`, male L `03ede4ed...`, male R `ca2aac16...`), all in the manifests. The hybrid's
CPU stage refuses a GPU store made for another arm through D10 (G13 compares the degree-term
digest with its own, `hybrid_arm.check_gpu_stage`), so no wrong store can enter an arm; but R4
alone does not refuse it. Revision 1.5 registers the digest **together with** its arm: "A's
composition" is the triple (refusal digest `a6a8a0df...`, arm module `knockout_regrow`, degree-term
digest `d48adfbd...`), and an arm's registration names its own triple.

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
| V5 | STATEMENT, neither refused nor explained | (a) CPU with 4 BLAS threads: 0 base fits moved, M3's five included; (b) engine v3 on the torch CPU device: 3 of M3's five differ from the CPU harness, 1 equals V1's GPU `p`, 5 of 5 controls equal both. So the five are not "a property of the fits under any change of reduction order" (V5's prediction), and not reproduced as a pure GPU effect either; §7's refusal condition ("(a) moves none and (b) reproduces them") is not met, since (b) did not reproduce them. The explanation of the base differences stays open |
| V6 | PASS (the comparator equals the brute-force recount on all 359 BF-active fits) | with `BF_TOL` 1e-5, 321 of 359 fits not bit-equal; the comparator refused it (outcome 3: 2 E1 failures, AUC of `world:W:4\|sh:84` BF_2 and BF_4, and 10 flipped pairs): the gates bite on a real change |
| V7 | PASS | 400 of 400 hashes and the degree-term digest equal with the real block poisoned |
| V8 L, R | CROSS-CHECK EQUIVALENT (outcome 1) | R.5 |

## R.7 Findings while drafting (proposed code items; none made)

1. **The refusal digest is arm-blind** (R.3). **G18:** an arm run's R4 compares the registered
   triple (refusal digest, arm module and lobe, degree-term digest), not the digest alone.
2. **The GPU stage does not refuse an arm module it has no adapter for.** `gpu_stage.refusals`
   restricts only modules listed in `prep.ARM_ADAPTERS` (the male arm). `--kind arm
   --arm-module knockout_regrow_block_b` passes `refusals()` (block B's module has A's interface,
   so `prep.set_arm` loads it directly); only the stamp (R1) and `--expect-digest` (R4, arm-blind)
   stand in the way, and D11 is enforced by procedure. **G19:** `refusals()` accepts in an arm run
   only the arm modules a revision registers (today none), and in a validation run only A's module
   and the male adapter under their labels; extension X's own driver is separate
   (`ext_gpu_stage.py`) and refuses arm runs altogether.
3. **G11 does not name block B's folders.** `instrument.reference_dirs()` lists A's pinned folder,
   the flyvis-65 run's folder and the male arm's folders; block B's pinned pre-run folder
   (`synthetic_blockB_prerun_20260927T211052Z_5f9cc51b9a24`) and B's registered run folder
   (`flyvis65_blockB_20260928T143258Z_7a10d88ec95e`) are not refused as output folders. Extension X's
   guard (`ext_scope.ext_out_dir_refusal`) adds them; G19 adds them to `reference_dirs()`.
4. **The V0–V7 records name revision 1.3.** Their `registration` field reads "revision 1.3
   (`ec5cbc0`)" with an `applied_ahead` note, while head `a0e16b6` carried revision 1.4's text
   (committed `e2fab47`) and §15.5: `instrument.REGISTRATION_REVISION` was still "1.3" at
   `a0e16b6` and was updated in `1ad6155`, before V8. The runs were made under revision 1.4's text;
   the label is stale, the records are not wrong otherwise. Ledger row G-(10) below.

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
| G-(10) | "registration ... revision 1.3 (ec5cbc0)" in the V0–V7 records | revision 1.4 (`e2fab47`, with §15.5 added in `a0e16b6`) was the text at the runs' head `a0e16b6` | `validation/V0.json`–`V7.json`, field `registration`; `instrument.py:34–35` at `a0e16b6` | `git show a0e16b6:docs/plans/2026-09-26-gpu-instrument-registration.md` (header "revision 1.4"); `1ad6155` (the constant updated) | this draft |

**Changelog (§14), proposed line.** Revision 1.5, 2026-09-29 UTC: V1's stamp registered (D7); A's
refusal digest `a6a8a0df...` registered with its arm and degree-term digest (D5, R4); `row_chunk`
stays outside the digest (V4 (c)); the differing base fits (M3's five) and the counts per cell;
A's census with a scope label on every number, and the JSON labels mapped; V0–V8 outcomes
recorded; §9 corrected under D6; the status header brought up to date; G17–G19 proposed; ledger
row G-(10). By a CC subagent.

## R.10 Questions for the reviewers

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
