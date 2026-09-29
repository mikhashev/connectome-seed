---
**Status: DRAFT plan, revision 1.1, 2026-09-29 UTC: revision 1 (committed as `030b974`) with the
reviewers' edits applied. Nothing here has run on the GPU.** Warren (08:34:21), Ark (08:37:58),
Johnny (08:40:48) and Zcode (08:49:04 UTC) voted yes on `030b974` with edits (§X.11; the reviews
are cited as relayed by CC). Step 2 of the GPU plan Mike approved (DPC Research chat, 2026-09-29
08:08:12 UTC, "yes GPU plan", translated from Russian, as recorded in `backlog.md`): extend the GPU
instrument's validation to the block mask and to fixed-λ fits, bit-compared against saved CPU fits
by the scheme of V1 and V2. Called **extension X** below. Its code and CPU tests are written (§X.8;
46 tests pass on the CPU); its GPU runs (§X.5) wait for a committed head (with revision 1.5.1 of the
registration, `docs/plans/2026-09-29-gpu-instrument-revision-1.5-draft.md`) and llama-server
stopped on Mike's word. Drafted by a CC subagent; CC checks it; the reviewers review it; Mike gives
his word.

**What it is not.** Not a registration: when VX1, VX2, VX6 and VX7 pass, a revision of the
registration (1.6 or later) registers extension X, its composition identities and its census; until
then no arm uses it (D11). Extension X changes no registered file (`harness.py`, the arm scripts,
`gpu_bf3.py`, `prep.py`, `census.py` and the pinned stores are read only; `instrument.py`,
`gpu_stage.py` and `hybrid_arm.py` change in revision 1.5.1 of the registration, not here). Not a
port of rule #2.1 (§X.2). Not a validation of the failed-fit calibration's worlds (§X.4, §X.7).
---

# Extension X of the GPU instrument: the block mask and fixed λ (plan)

## X.1 Scope: the two fits

| mask | the CPU call it replaces | record key | its readers in `evaluate_bank` (A :1045, :1072, :1087; B :1474, :1504, :1519) |
|---|---|---|---|
| **block** | `P.train(bank, MASKS["block"])` = `harness.fit_bf(make_view(bank, BLOCK), r)`: N1 on the block view, λ by the nested scheme (10 inner folds × λ ∈ {1, 3, 10, 30, 100}, ties within 1e-9 to the larger), final `bf_als` at the chosen λ | `world:<f>:<j>\|\|block\|\|BF:<r>` | `ceiling_block` = `auc(p, y)`; `regrown_share_block` (a ratio of exact AUCs); `lambda_block` = `lam` |
| **ko1** | `train_fixed_lambda("BF:r", P, bank, 1.0)` (A `knockout_regrow.py:808`; B `knockout_regrow_block_b.py:1213–1237`): `fit_n1` on the ko view, `harness.bf_als(_n1_logit_grid(n1), Y, M, r, 1.0, starts=STARTS)`; no λ choice | `world:<f>:<j>\|\|ko1\|\|BF:<r>` | `auc_fixed_lambda1` = `auc(p, y)`; `p_P_fixed_lambda1` = `auc_null(p, Yu)` over the uniform permutations |

BF_1–BF_4, base views only (both records exist only on `world:<family>:<j>`): 45 × 4 = **180 fits
per mask per arm**. The GPU arithmetic is engine v3's own (`gpu_bf3.fit_bf_all` for block;
`gpu_bf3.solve_problems` on grid 0 at λ = 1 for ko1); no new arithmetic is written. Everything
else (bank, view, N1, grids, folds, held-out masks, SVD start, decode, score) is the CPU's own
call, as in D1 (a): T-X5 checks it bit for bit (§X.8).

**No continuous column reads either record** (the readers above are an AUC, a permutation p-value
on AUCs, a ratio of exact AUCs, and λ), so **E3 does not apply** to extension X; the comparator
prints that statement with every report instead of a bound.

## X.2 Rule #2.1's fixed-λ fit and its quantised decode: outside the GPU scope

Checked from the code:
- The registered instrument does not fit rule #2.1 at all: D1 (a) keeps it on the CPU, D13 (a)
  leaves its port unregistered, and the registered driver refuses to import `gpu_rule` (G8,
  `gpu_stage.FORBIDDEN_ENGINES`).
- The unregistered port (`gpu_rule.py`, engine v2) batches only the rank-1 `bf_als` calls inside
  `fit_existence`'s `fit_uvw` (`rules/second_rule_v21/fit.py:97–113`, `:119–146`). The ridge step
  on W, and everything after `fit_existence` — the quantisation `ExistQ` (`fit.py:172–265`: 5-bit
  symbols `to_sym`, float32 scales `sym_scale`), the coordinate descent, `refit_c`,
  `fit_offsets`, the counts and signs, and `decode.py` — run on the CPU even there
  (`prep.rule_post_key`, `prep.install_existence`).
- The fixed-λ rule fit sets the module global `LAMBDAS = [1.0]` for one fit
  (`train_fixed_lambda`, B `:1221–1228`; `fit.py:57`, `:128`, `:142`) and runs the whole rule,
  quantisation included, on the CPU.

So the `ko1‖rule`, `block‖rule` and `full‖rule` records stay CPU fits in any hybrid, and
extension X does not touch them. Porting them would be a D13 revision with its own validation; the
quantisation rounds float32-cast parameters to symbols, so a GPU difference can flip a symbol (M6:
3 of 45 rule base views differed on engine v2). Not proposed.

## X.3 References (read only)

| arm | store | pin | role |
|---|---|---|---|
| A (64 block cells) | `connectome-seed-data/knockout_regrow/synthetic_rev3_prerun/raw_fits.json.gz` | `91035af8...`, after A's `check_prerun_files` | reference (D4 (a)) |
| B (40 block cells) | `.../synthetic_blockB_prerun_20260927T211052Z_5f9cc51b9a24/raw_fits.json.gz` | `5d08f6e6...` (`knockout_regrow_block_b.PRERUN_SHA256`), after B's `check_prerun_files` | reference |
| B | `.../flyvis65_blockB_20260928T143258Z_7a10d88ec95e/raw_fits.json.gz` (B's registered run) | `55b240a7...` (its `SHA256SUMS.txt` line) | witness: a fresh CPU refit of all 28,665 synthetic keys, 0 `p`, λ, label or score differences against the pre-run (its `stdout.log` line 94); T-X4 confirms `p` and λ equal on all 360 block and ko1 BF records. VX2 against it must give the same report as against the pre-run |

`raw_fits_real.json.gz` beside B's registered store is never opened; no real block is fitted,
read or scored (`ext_scope.check_base_key` refuses every non-`world:` key, `prep.build_bank` is
called with `synthetic_only=True`). The output guard refuses all three folders
(`ext_scope.ext_out_dir_refusal`; revision 1.5.1 adds B's two folders to
`instrument.reference_dirs()` as well).

## X.4 The tie census of the references (T-X4; CPU reads, no fit)

Every count is of tied **pairs** on the named pair set; S(f) = present × absent on a block record
(its only reader is `auc`), all pairs of the block on a base `ko1` record (it feeds `auc_null`).

| scope | λ (all 180) | BF-active (p ≠ its view's N1 p) | copied from ko (`reused_from_ko`) | tied pairs on S(f) | smallest gap on S(f) (where) | at risk (< 2^-23) |
|---|---|---|---|---|---|---|
| A block, 180 fits | 1 | 180 | 0 | 0 | 0.7500 (`No:0`, BF_3) | 0 |
| B block, 180 fits | 1 | 180 | 0 | 0 | 0.6547 (`No:0`, BF_2) | 0 |
| A ko1, 180 fits | 1 (fixed) | 180 | 29 | 0 | 5.040e-7 (`M0.6:0`, BF_3) | 0 |
| B ko1, 180 fits | 1 (fixed) | 180 | 29 | 0 | 1.615e-6 (`Nf:1`, BF_2) | 0 |

What the census says about the block mask on these worlds: every block fit is **saturated**. A's
block BF `p` takes exactly 2 values per fit (one for the present cells, one for the absent ones:
about 0.875 and 0.125), B's takes 4; `ceiling_block` = AUC = 1.0 on all 180 fits of each arm; the
same-label ties (178,560 tied pairs in A, 33,840 in B, on all pairs) lie outside S(f). A flip of
S(f) needs a |Δp_i − Δp_j| of at least 0.65, and in A a label change needs a Δp of about 0.375
(from about 0.875 or 0.125 to 0.5). So on A's and B's worlds **the block comparison can refuse
only through λ, a label, the AUC or the bits**; E2-II cannot be exercised there.

**The block λ branch is not witnessed on A or B** (Ark): λ = 1 on all 180 block fits of each arm,
so the choice of any other λ on a block view has no CPU witness in either store.

The regime the failed-fit calibration cares about (`ceiling_block` < 0.90, where ties and
near-ties can sit on present × absent pairs) is in no saved CPU store. The ko1 fits are
informative: every fit is BF-active and tie-free, with a smallest gap of 5.0e-7 (A) and 1.6e-6
(B), about 8 and 27 times 2^-24.

## X.5 The runs (all on the GPU, synthetic worlds only; none made)

Driver `run_ext.py` (entry; imports `gpu_env` first) → `ext_gpu_stage.py`; comparator
`ext_compare.py` (tools/.venv). Private folders
`connectome-seed-data/gpu_instrument/<label>_<arm>_<mask>_<UTC>_<head 12>/`; committed aggregates in
`results/genome/c6/gpu_instrument/validation/VX*.json` after the runs.

| run | what | composition | passes if | refuses extension X if |
|---|---|---|---|---|
| VX0 | smoke | B, block and ko1, `--worlds R:0` | the driver completes; R1 (the registered stamp), R2, R3, G11, the preflight pass | an unavoidable `RuntimeError` under D6 |
| VX1 | self-stability (V1's scheme): three fresh runs | A and B × block and ko1: 4 compositions × 3 runs | every per-fit sha256 of U, V, λ and p equal across the three runs, and one composition identity, per composition | any hash differs: "NOT DETERMINISTIC" |
| VX7 | the poisoned block (T-G5's check on the block mask, the one mask that trains on block cells) | A and B, block, 45 base views, `--poison-real-block` | every per-fit hash and the degree-term digest equal to VX1 run 1 of the same arm and mask | any hash differs: a code path reads a real block cell |
| VX2 | equivalence (V2's scheme) | VX1 run 1 of each composition against its arm's pinned store (and B's also against B's registered store: an identical report required) | E1 (y, λ, labels, AUC; ko1: λ = 1 on both sides and `p_P_fixed_lambda1` equal) and E2-II (0 flipped pairs); E2-III list printed; E3's "not applicable" statement printed; diagnostics: bit-equality, max \|Δp\|, counts per (rank, `reused_from_ko`) cell against denominators read from the reference first; **a difference on a `reused_from_ko` record triggers the CPU path check of that record first** (Zcode's rider; `ext_compare.cpu_path_check`) | an E1 difference (outcome 3), a flipped pair (outcome 2), or a failed CPU path check |
| VX6 | negative control (**required**, Zcode): `--bf-tol 1e-5` in the GPU process | B, ko1 | the comparator's not-bit-equal set equals a direct byte comparison of the saved `p`, and its E1 failures are exactly the fits with a direct λ, label or AUC difference (`ext_compare.direct_recount`, `recount_agrees`) | the comparator misses or invents a difference; if no `p` moves, "uninformative" is recorded, not a pass |

**Order:** VX0; VX1 (12 runs); VX7 (compared with VX1 run 1); VX6; then VX2 and VX6's recount on
the CPU (seconds). The commands are in §X.9.

**The compositions (G18's binding, Zcode X.10.5).** Per (arm, mask): the arm's 45 base views in its
`world_specs()` order, ranks 1–4, starts 10. Each run records its **composition identity**
(`ext_scope.ext_composition_identity`): composition = the extension digest over the mask, the
ordered keys, starts, the ranks and, for ko1, λ = 1 (the arm is not hashed into it); world = the
degree-term digest; script = the arm module. VX1 refuses runs whose identities differ. `row_chunk`
40,000 is recorded, not in the identity (V4 (c)). With 45 banks every rank fits in one block (block:
2,250 inner problems; ko1: 45 problems), so no chunk boundary exists to move. The revision that
registers extension X registers the four identities VX1 measures.

## X.6 Why these criteria are V1's and V2's, and what they cannot see

- The per-fit hashes (VX1) and the comparison of decoded `p` (VX2) are the same functions as V1's
  and V2's (`instrument.array_sha256`; the census definitions of `census.py`, whose pair
  arithmetic `ext_census.py` carries over with the pair set built from the block's size, because
  B's block has 40 cells and `census.py` builds its all-pairs set from 64; T-X1).
- The block fits' λ choice is the one place the block mask can differ from the CPU on these worlds
  (§X.4). The block driver prints the near-tie count by rank (G15) so that a λ decided by less than
  1e-7 is visible; B's fit diagnostic (`READING_NOTES.md` §9) found that the λ grid does not
  separate λ = 1 from no interaction robustly on B's inner folds, so near-ties are expected.
- **The 29 ko1 copies per arm stay in VX2's 180** (Zcode). They are copies of the CPU ko fit at a
  selected λ of 1; the CPU's fresh fixed-λ fit equals them (A's and B's path checks), so a fresh GPU
  ko1 fit is compared with them as with the other 151, and they are counted as their own cell in the
  diagnostics. **Rider:** a difference on one of them is not read until the CPU path check of that
  record is re-run and passes (`cpu_path_check`: the arm's own `train_fixed_lambda` on the CPU,
  decoded, equal to the stored copy bit for bit); T-X7 runs it on B's first reused record.

## X.7 What a pass would license, and what not

A pass of VX1, VX2, VX6 and VX7 on both arms would let a revision register extension X: GPU BF block
and ko1 fits in a hybrid synthetic step of an arm that names them before its pre-run (D11). It would
**not** license:
- **any composition whose block fits carry ties on S(f)** (a property, not an arm name; Ark). A's
  and B's block fits carry none (§X.4), so VX2 on them cannot exercise E2-II on the block mask. A
  VX8-like cross-check, with the census repeated on the composition's own worlds (V8's pattern), is
  **mandatory** for every such composition, and it needs a CPU pre-run store of those worlds as its
  witness. The order is: **CPU pre-run → VX8 → GPU**;
- **the failed-fit calibration's block fits, in particular.** Its worlds are built to land below
  `ceiling_block` 0.90. The calibration stays on the CPU (as `backlog.md` records); its own CPU
  pre-run would serve as the VX8 witness, before the GPU could be named for it;
- **the block λ branch** (λ other than 1 on a block view): not witnessed on A or B (§X.4);
- **rule #2.1** (§X.2);
- **the hybrid's CPU side as it stands.** G13 (`hybrid_arm.check_gpu_stage`) plans only `ko` keys,
  and an arm's `complete_fixed_lambda` copies the ko record into ko1 where the selected λ is 1.
  Under a GPU ko1, the copy is of a GPU ko fit made in another batch than the GPU ko1 fits (V4:
  composition moves bits), so the arm's fixed-λ path check needs D9 (b)'s form for ko1 too. These
  are code items of the registering revision, not of this plan.

**For Mike (Johnny):** after extension X passes, the GPU instrument still does **not** cover the
failed-fit calibration automatically. The calibration would need its own CPU pre-run, then a VX8
cross-check on its worlds, and only then could it name the GPU.

## X.8 Code and tests (written; CPU tests run)

New files in `results/genome/c6/gpu_instrument/`, prefixed `ext_`, and a separate test folder.
Extension X modifies no existing file (the registered files that change belong to revision 1.5.1
of the registration, its R.12).

| file | what it does |
|---|---|
| `ext_census.py` | G16's census for a block of any size: the pair arithmetic of `census.py` carried over, with the pair set built from `len(y)`; `family_summary_scoped` returns the scope label as a field `scope` next to `families` (and the family names say which fits of that scope each family counts) |
| `ext_scope.py` | masks, base-key refusal, record keys, the extension digest and the composition identity (G18), the extended output guard, reference loading (A, B pinned, B registered), the reference census (CLI: `--arm A\|B`) |
| `ext_prep.py` | pool workers: `prepare_key_ext` (block: `prep.prepare_view` on the block view; ko1: grid 0 of the ko view) and `decode_records_ext` (decode, score, per-fit hashes) |
| `ext_engine.py` | `run_core`: GridStore, `fit_bf_all` (block) or `solve_problems` at λ = 1 (ko1), hand-off to the decode workers |
| `ext_gpu_stage.py`, `run_ext.py` | the validation driver (labels VX0, VX1, VX6, VX7; no arm runs): R1 (the registered stamp), R2, R3, R7, G8 (imports `gpu_stage`, which installs the engine refusal), extended G11, D10, the VRAM preflight, the composition identity, manifest, `SHA256SUMS.txt` |
| `ext_compare.py` | VX1's hash and identity comparison; VX2's comparator (E1 incl. `p_P_fixed_lambda1`, E2-II, E2-III, the E3 statement, diagnostics); the CPU path check on reused ko1 records (the rider); VX6's direct recount (`--vx6`) |
| `tests_ext/` | T-X1–T-X7 (below); a separate folder because `tests/conftest.py` probes CUDA at import |

| test | checks | result (2026-09-29, tools/.venv, CPU, `CUDA_VISIBLE_DEVICES=-1`) |
|---|---|---|
| T-X1 | `ext_census` equals `census.py` on A's 64-cell records (every base ko, ko1 and block record, D1's four at-risk fits, 2,000 random shuffles; flips on perturbed copies; family counts); on B's 40 cells `census.py` fails (IndexError) and `ext_census` counts 780 pairs | pass |
| T-X2 | base keys only; masks block and ko1 only; record keys; the output guard refuses A's and B's reference folders; the composition identity: its composition axis moves with mask, key order and set, starts, ranks, not with the arm; the arm is refused through the world and script axes, each alone; the registered digest recomputes to `a6a8a0df...` from A's key list (arm-blind) | pass |
| T-X3 | the comparator on A's and B's block and ko1 records: unmodified → outcome 1; one float64 step with no reorder → outcome 1, counted not bit-equal; λ changed, label flipped → outcome 3; a block present cell below an absent one → AUC fails, flips named; a ko1 same-label tie broken by one step → 1 flipped pair named, AUC unchanged, outcome 2 or 3 | pass |
| T-X4 | §X.4's census, number for number, with its scope labels; B's registered store equal to B's pinned store on all 360 block and ko1 BF records | pass |
| T-X5 | with ext_prep's arrays, the harness's own numpy `bf_als` reproduces the pinned record bit for bit through `decode_records_ext`: ko1 ranks 1 and 4, block rank 1 (fit_bf's λ choice re-executed from the prepared folds), A and B, `world:R:0` | pass |
| T-X6 | `run_core` on the torch CPU device (`GPU_INSTRUMENT_DEVICE=cpu`, `CUDA_VISIBLE_DEVICES=-1`, `gpu_env` first), B `world:R:0`, block rank 1 and ko1 ranks 1, 4, twice: equal hashes across the two runs; outcome 1 against B's pinned store (here also bit-equal, 3 of 3; not asserted) | pass |
| T-X7 | VX6's direct recount agrees with the comparator on unmodified records ("uninformative") and on a one-step move, a changed λ and a label flip; the CPU path check on B's first `reused_from_ko` ko1 record passes bit for bit | pass |

`tools/.venv/Scripts/python.exe -m pytest results/genome/c6/gpu_instrument/tests_ext -q`: **46
passed** (about 9 s). The existing suite `tests/` was run as well, with `CUDA_VISIBLE_DEVICES=-1`
so that its conftest's CUDA probe answers no: 130 passed, 16 GPU tests skipped (revision 1.5.1,
R.12).

## X.9 Cost, VRAM, the llama-server condition and the commands

**Time (estimates from measured analogues, not measured for extension X).** A block run has the
shape of V4a (45 base views, 10 folds × 5 λ, ranks 1–4): V4a took 37.4 s end to end, 26.8 s of
GPU, 6.5 s of prep. A ko1 run has no inner problems (45 problems per rank): a few seconds of GPU,
about 6 s of prep (the ko-view N1 dominates, as in V4a), plus about 3 s of setup. With process
start and the degree terms: **block about 40–60 s, ko1 about 15–25 s per run**. VX0 2 runs, VX1
12 runs, VX7 2 runs, VX6 1 run: about **12–15 min of wall time, about 3–4 min of GPU compute**;
VX2 and VX6's recount are CPU seconds. Allow a 30-minute window.

**VRAM.** V4a's torch peak was 4,479 MiB (45 banks, all inner problems in one block); a block run
is the same shape, so about 4.5 GB, plus the CUDA context (about 0.5 GB, outside torch's count);
ko1 well under 1 GB. The driver's preflight asks for the registered need at `row_chunk` 40,000,
**12,550 MiB free** (revision 1.5.1) before the upload, with no fallback.

**The llama-server condition.** On 2026-09-29, read by `nvidia-smi` while drafting, the GPU had
about 27.5–27.8 GB of 32.6 GB in use with `llama-server.exe` running (about 4.9 GB free). That is
below the preflight's 12,550 MiB. So **the runs need llama-server stopped**, which only Mike can
order, by his word typed in the session that runs them (not in the DPC chat); it is restarted
after the last run. Nothing in this plan stops or touches it.

**The commands** (from `results/genome/c6/gpu_instrument/`, a committed clean head; `T` is the
torch venv `../../../../../autoresearch-win-rtx/.venv/Scripts/python.exe`, `C` is
`../../../../tools/.venv/Scripts/python.exe`; `PYTHONUTF8=1` for every run):

```
# VX0 (smoke)
$T run_ext.py --label VX0 --arm B --mask block --worlds R:0
$T run_ext.py --label VX0 --arm B --mask ko1 --worlds R:0
# VX1: three fresh runs of each of the four compositions (12 runs)
for arm in A B; do for mask in block ko1; do for i in 1 2 3; do
  $T run_ext.py --label VX1 --arm $arm --mask $mask; done; done; done
# VX7: the poisoned block, per arm
$T run_ext.py --label VX7 --arm A --mask block --poison-real-block
$T run_ext.py --label VX7 --arm B --mask block --poison-real-block
# VX6: the negative control
$T run_ext.py --label VX6 --arm B --mask ko1 --bf-tol 1e-5
# CPU: VX1 and VX2 per composition; VX7 against VX1 run 1; VX6's recount
$C ext_compare.py --arm B --mask block --runs <VX1 r1> <VX1 r2> <VX1 r3> --json validation/VX2_B_block.json
$C ext_compare.py --arm B --mask block --runs <VX1 r1> --reference registered --json validation/VX2_B_block_registered.json
$C ext_compare.py --arm B --mask block --runs <VX1 r1> <VX7 B> --json validation/VX7_B_block.json
$C ext_compare.py --arm B --mask ko1 --runs <VX6 run> --vx6 --json validation/VX6_B_ko1.json
```

(and the same `ext_compare.py` lines for A block, A ko1, B ko1). Each driver run prints its
`RUN_DIR=`.

## X.10 Questions for the reviewers (revision 1; answered in §X.11)

1. **Ark:** on A's and B's worlds the block comparison cannot exercise E2-II (every block fit is
   saturated, §X.4). Is VX1 + VX2 + VX7 on these worlds enough to register the block engine for a
   future arm, with a VX8-like cross-check required on any arm whose block fits are not saturated
   (the failed-fit calibration first)?
2. **Zcode:** ko1 compares 29 fresh GPU fits per arm with records that are copies of the CPU ko
   fit (§X.6). Keep them in VX2's 180, or compare only the 151 the CPU fitted afresh?
3. **Johnny:** `ext_census` duplicates `census.py`'s definitions to lift the 64-cell limit, and
   T-X1 pins them equal on 64 cells. Accept the duplicate, or should `census.py` itself be
   generalised in the registering revision (a change to a registered file, re-tested by T-G9 and
   T-G10)?
4. **All:** VX6 is marked optional: the comparator is tested on fixtures (T-X3). Run it, and if so
   on ko1 (where a looser Newton stop can move `p`) or on block (where it can move only λ)?
5. **All:** the extension digest binds the arm and the mask (§X.5). Should the registering
   revision use the same binding for the `ko` composition (revision 1.5 draft, R.7 (1), G18)?
6. **Mike:** the GPU runs need llama-server stopped for about 30 minutes, on your word in the
   session that runs them. The code is uncommitted; the runs are made from a committed head after
   the reviewers' yes.

## X.11 Reviews of revision 1 (`030b974`; as relayed by CC) and the edits applied

| edit | asked by | applied in |
|---|---|---|
| a VX8-like cross-check is mandatory for any composition whose block fits carry ties on S(f), stated by property, not by arm | Ark | §X.7 |
| the calibration's own CPU pre-run is that witness: CPU pre-run → VX8 → GPU | Ark | §X.7 |
| the block λ branch is not witnessed on A or B (λ = 1 in all 180) | Ark | §X.4, §X.7 |
| a line for Mike: after X, the GPU does not cover the calibration automatically | Johnny | §X.7 |
| keep the 29 ko1 copies in the 180; rider: a difference in a reused cell gets the CPU path check first | Zcode | §X.5 (VX2), §X.6; `ext_compare.cpu_path_check`; T-X7 |
| run VX6, on ko1 (B) | Zcode | §X.5 (VX6 required), §X.9; `ext_compare.direct_recount`, `--vx6`; T-X7 |
| the same binding for `ko` and for X: the composition identity (an AND of composition, world, script; not a re-hash) | Zcode (X.10.5), Ark, Johnny | §X.5; `ext_scope.ext_composition_identity` (the arm removed from the extension digest); T-X2 |
| X.8 text: the scope is a field next to `families`; `ext_census` carries over the pair arithmetic of `census.py` | Zcode | §X.6, §X.8 |
| the VRAM need 12,550 MiB | Ark, Zcode (Warren: 12,526, recorded in revision 1.5.1) | §X.9 |
| "46 new tests pass"; the existing tests' status said plainly | Johnny | §X.8 |

Answers to §X.10: (1) yes, with the cross-check required by property (§X.7); (2) keep them, with
the rider; (3) the carried-over arithmetic stands, pinned by T-X1; (4) run VX6 on ko1 (B); (5) yes,
as the composition identity; (6) open: Mike's word.
