---
**Status: DRAFT, revision 1.2, 2026-09-26 UTC (`date -u` read 11:32 UTC when the edits began;
revision 1 was begun at 10:26 UTC and committed as `fedeec5`; revision 1.1 was committed as
`345acf2`).** Revision 1.1 applied the reviewers' edits of 10:52–10:54 UTC. Revision 1.2 applies
the decision of 11:15–11:25 UTC (Ark, Zcode: options (a)/(b)/(c) for E2a rejected; E2 replaced by
a tie census, §5), recorded in §15 with its own votes and edits tables. Johnny is out (Mike, 11:00
UTC); the two votes stand, and Johnny reads revision 1.2 in a new session. **Not committed; Mike's
word is not given. Nothing was fitted for it: no GPU run of the instrument, no CPU fit. The only
runs made while drafting are listed in §12 (a 20-second environment probe on random tensors, and
read-only counts and checksums over the pinned and the flyvis-65 run's synthetic stores, the
pinned `synthetic_worlds.csv` and the instrument's JSON dumps).** Drafted by a CC
subagent; CC checks it, the reviewers (Ark, Johnny, Zcode) review it, and Mike gives his word. The
design choices are marked **proposal** in the body and listed in §4 (D1–D13), each with its
options, what each option changes, and a recommendation. The body is written with the
recommended option, so the draft is complete as it stands.

**Why this file exists.** Mike, DPC Research chat, 2026-09-26 09:13 UTC: "of course we review the
GPU instrument for the ~×2.3 speed-up on BF", and at 09:13:41: "what's the point of not using the
GPU to speed up without loss of quality if we can". Block A's registration requires it: a GPU
instrument "is a separate instrument. It is validated on its own, with its own registration and
its own synthetic worlds. It inherits none of this instrument's limits, and this registration
does not use it" (A §7, `docs/plans/2026-09-24-knockout-regrow-registration.md` lines 1473–1476
at `74db080`). The reviewers, 09:14–09:18 UTC (chat, as relayed to the drafter): an arm's pre-run
must be made by the same instrument as its run, so the male arm stays on the CPU; the GPU is a
separate registration; a GPU run of the male worlds may serve as an unregistered cross-check
during that arm's pre-run. Ark: the saving is about 35–40 % per arm until rule #2.1, the
ceilings, λ and the permutations are ported, and the base-view differences must be fixed or
explained before any registration.

**Hard limit, kept by every step of this file.** The GPU instrument never reads, fits or scores a
real block: not block A or block B of flyvis-65, not the male CNS sealed files
(`male_cns_L_blockA.sealed.csv`, `male_cns_R_blockA.sealed.csv`), and never
`raw_fits_real.json.gz`. It fits synthetic worlds and the shuffled banks of synthetic worlds only
(§1.4 states the one contact with the real bank's outside cells, and the harness import).
---

# Registration: the GPU instrument for the knockout-and-regrow synthetic step

## 0. What this is, and what it is not

**What it is.** The registration of a second instrument for the synthetic step of the
knockout-and-regrow arms: a batched float64 PyTorch/CUDA re-implementation of the BF_r fits
(`harness.fit_bf`, ranks 1–4), used beside the pinned CPU harness in a **hybrid** synthetic step
(D1, D8). It registers, before any validation run: what the GPU replaces and what stays on the
CPU; the criterion by which it counts as equivalent to the CPU instrument; the reproduction gate
of a GPU run; the validation runs, their cost and the results that refuse the instrument; which
arms may use it; and the code changes it needs.

**What it is not.** It is not a change to the registered CPU instrument: `harness.py`,
`checks/knockout_regrow.py`, the pinned files of A §1.1 and the pinned pre-run folder
`connectome-seed-data/knockout_regrow/synthetic_rev3_prerun/` are read only. It changes nothing in
block A's verdict (G, made on the CPU at head `74de040`; `results/genome/c6/checks/knockout_regrow/RESULT.md`).
It does not move the male CNS arm or block B onto the GPU (§8). It does not register the
unreviewed engines v1 and v2 or the rule #2.1 port (D2, D13).

**Vocabulary.** *Engine v1/v2/v3*: the three GPU fitters in
`results/genome/c6/gpu_instrument/` (`gpu_bf.py`, `gpu_bf2.py`, `gpu_bf3.py`). *Base view*: a
world's own knockout (`ko`) view, key `world:<family>:<j>`. *Shuffle*: key
`world:<family>:<j>|sh:<sd>`. *Bit-equal*: `np.array_equal` of the 64 decoded `p` values, through
the harness's own decode. *Batch composition*: the ordered list of banks given to the GPU, with
`row_chunk`, `starts`, the rank order and the chunk boundaries that follow from them (§3.3).
*Hybrid synthetic step*: BF_1–BF_4 on the `ko` mask of every synthetic base view and shuffle on
the GPU (engine v3); every other fit on the pinned CPU harness.

## 1. The instrument as it stands (commits `74de040`, `cdbde9e`; unreviewed)

### 1.1 Files

All paths under `results/genome/c6/gpu_instrument/`; line numbers at `cdbde9e`, which is also the
current head for this directory.

| file | what it is | registered use (proposal) |
|---|---|---|
| `gpu_bf.py` | engine v1: `gpu_fit_bf`, `gpu_fit_bf_many`; defines `DEVICE`, `DTYPE = torch.float64` (:31–32) | none; kept as history |
| `gpu_bf2.py` | engine v2: `bf_als_problems` (:105–144) with per-row active-set compaction (:57–86); `choose_lambda`, `inner_ll` on the host (:147–158) | none (D2) |
| `gpu_bf3.py` | engine v3, the streamed pipeline: `GridStore` (all grids resident on the GPU), `newton_rows_v3` (:78–106), `_heldout_ll` on the GPU (:117–122), `solve_problems` (:125–171), `fit_bf_all` (:174–195) | **the engine** (D2) |
| `gpu_rule.py` | rule #2.1's existence fit, batched on engine v2 (:65–97) | none (D13) |
| `prep.py` | CPU preparation in a pool (N1 fits, grids, held-out masks, SVD starts; `prepare_key_compact` :146–161), `decode_compare` (:164–184), the rule's post-existence CPU part (:107–130). Refuses a key whose base is `real` (:64, :112, :147) | yes, after G7 |
| `run_pipeline.py` | the v3 driver; keys = 45 worlds × 99 shuffles, then the 45 base views appended (:112–114) | yes, after G1–G6 |
| `validate*.py` | v1 and v2 validation drivers | none |
| `README.md`, `run*.log`, `validation_*.json`, `pipeline_*_nvsmi.csv` | the record of the measurements (§2) | cited |

`.gitignore` excludes the two full per-fit dumps (`validation_pipeline_all45.json`,
`validation_shuffles_all45.json`, "~6 MB each"); they exist in the working directory and were read
for this draft. They hold, per fit, λ, AUC, max |Δp| and `p_bit_equal`, but **not the fitted p**.

### 1.2 What the GPU computes and what it takes from the CPU harness

- **From the harness, unchanged (CPU, in the prep pool):** bank construction
  (`knockout_regrow.build_bank(key, terms, True)`), the knockout view, N1 on the view and on its
  ten inner-fold training views (`harness.fit_n1`), the logit and training grids, the held-out
  masks, the SVD start of `bf_als` (`prep._svd_start4`, :140–143), and the decode
  (`Predictor.decode`, which casts every float array to float32 and back, `harness.py:273–277`,
  `:303–305`).
- **Re-implemented on the GPU, in float64:** the Newton row updates and ALS sweeps of
  `harness.bf_als` (`harness.py:647–697`), the penalised objective that picks the best of the ten
  starts, **the inner held-out log-likelihood of each (fold, λ) problem** (`gpu_bf3.py:117–122`),
  and, on the host, its sum over folds and the tie rule of `fit_bf` (`gpu_bf3.py:174–195`). The
  README's "re-implements only `harness.bf_als`'s ALS/Newton optimisation" omits the λ choice
  (§11, row G-(1)).
- **Where the arithmetic differs from the harness (read from the code):** the sigmoid
  (`torch.sigmoid`, `gpu_bf3.py:91`, against `1 / (1 + exp(-z))`, `harness.py:643–644`); the
  Hessian contraction (a batched matmul of W with the outer products of V, `gpu_bf3.py:102–103`,
  against `np.einsum("st,tk,tl->skl", …)`, `harness.py:655`); the row solve
  (`torch.linalg.solve` on a batch, `gpu_bf3.py:104`, against `np.linalg.solve`,
  `harness.py:656`); the held-out sum (`torch.sum` over the 65 × 65 masked grid, `gpu_bf3.py:122`,
  against `np.sum` over the boolean-indexed cells, `harness.py:726`). All of it is float64 (`DTYPE`,
  `gpu_bf.py:32`); M, Y and the masks are bool and enter through `torch.where`, which is exact.
  So the float64 U, V of the GPU are not expected to equal the CPU's bit for bit; what is
  compared is `p` after decode's float32 cast (§3).

### 1.3 Environment used by the measurements

`c:/Users/mikha/Documents/dpc-research/autoresearch-win-rtx/.venv` (a venv of another project,
not modified): Python 3.10.20, numpy 2.2.6, torch 2.9.1+cu128 (CUDA 12.8, cuDNN 91002), psutil
7.2.2; GPU NVIDIA RTX PRO 4500 Blackwell (compute capability 12.0, 32,623 MiB), driver 596.86.
The CUDA libraries are the DLLs bundled in `torch/lib` (`cublas64_12.dll`, `cublasLt64_12.dll`,
`cusolver64_11.dll`), which carry no pip version. `tools/.venv` has the same Python and numpy
(3.10.20, 2.2.6). All read at drafting (§12, run P1); none of it is recorded by any GPU script,
which records only `gpu_name` (`run_pipeline.py:186`).

### 1.4 Contact with the real bank

- **The degree terms.** Every driver calls `knockout_regrow.degree_terms()`
  (`knockout_regrow.py:694–698` at `74db080`): N1 fitted on the real bank's **knockout** view,
  4,161 outside-block cells, no block cell. This is the one real-bank fit that A's
  `--synthetic-only` makes (A §3.6, D8; the flyvis-65 run's log, line 8: "4161 outside-block
  cells; no block cell read"). The worlds' content pool is the 572 non-block present cells
  (`NONBLOCK_CELLS`, `knockout_regrow.py:691`).
- **The harness import.** Importing `harness` builds `REAL` from the committed flyvis-65 bank at
  module level (`harness.py:136`, `:169`), block cells included, as in every harness process. No
  code path of the instrument indexes a block cell of `REAL`; §7 registers a test that would
  detect one (T-G5).
- **The refusals.** `prep.py` refuses a key whose base is `real` (:64, :112, :147), and
  `build_bank` refuses one under `synthetic_only=True` (`knockout_regrow.py:749–757`). The v1
  scripts build worlds with `make_world` directly (`validate.py:50`, `validate_batched.py:43`),
  outside that refusal; they build only world specs.
- **The stores read.** The v2/v3 drivers read the flyvis-65 run's synthetic store
  (`connectome-seed-data/knockout_regrow/flyvis65_20260925T171656Z_74de0401a21f/raw_fits.json.gz`,
  `run_pipeline.py` `REF`); `raw_fits_real.json.gz` beside it is never opened. The male arm's
  sealed files are not read by any file of the instrument (it has no male code).

## 2. What has been measured, with sources

Every number below was read from the named file by the drafter. "Verified" means the drafter
recomputed it from the file; "as recorded" means it was read, not recomputed.

| # | claim | value | source | status |
|---|---|---|---|---|
| M1 | BF_1–BF_4, 45 worlds × 99 shuffles, v2 (one world per batch) | 17,820 / 17,820 bit-equal; 0 λ, 0 label, 0 AUC differences | `run6_shuffles_all45.log:47–55` | as recorded |
| M2 | the same, v3 (all 4,500 banks in one store) | 17,820 / 17,820 (the 18,000 of the run minus the 180 base fits) | `run7_pipeline_all45.log:7–11`, `:63–92`; `validation_pipeline_all45.json` rows | verified (rows) |
| M3 | base views, v3 | 175 / 180 bit-equal; the 5 others are BF_1: M1.0:0 (λ 1), M1.0:4 (λ 3), M0.75:0 (λ 3), M0.85:0 (λ 1), M0.85:2 (λ 3); max \|Δp\| 5.632e-8; 0 λ, label, AUC differences | `run7_pipeline_all45.log:11`, `:94–98` | verified (rows) |
| M4 | base views, v2 (45 views in one batch) | 177 / 180; the 3 others: M1.0:4 (5.54e-8), M0.75:0 (1.63e-8), M0.85:0 (2.94e-8) | `validation_shuffles_base45.json` summary and rows | verified (rows) |
| M5 | v1 against a live `harness.fit_bf`, same process, float64 accessor (not decode) | 175 fits within 3e-16; 5 BF_1 fits (seeds 90150, 90154, 90170, 90180, 90182) differ by 1.4e-9 to 3.8e-8; λ, AUC, labels identical | `run3.log:101`, `:117`, `:141`, `:161`, `:169`, `:182–188` | as recorded |
| M6 | rule #2.1 with the GPU existence fit (engine v2), base views | 42 / 45 bit-equal, four scores identical on the 42; M0.75:1, M0.75:3, M0.85:3 differ by ≤ 4.89e-8, all at λ 3 | `validation_rule_base45.json` summary and rows | verified (rows) |
| M7 | rule #2.1, 45 worlds × 99 shuffles | 4,455 / 4,455 bit-equal, scores identical | `run8_rule_sh_all45.log:46–58` | as recorded |
| M8 | "8 differences on base fits" | 5 BF_1 (v3) + 3 rule #2.1 (v2) = 8; max 5.632e-8 | M3, M6 | verified |
| M9 | v3 wall time, 18,000 BF fits (45 × (99 + 1) × 4) | end to end 2,362.3 s (39.4 min): setup 2.2, prep 137.8 (24 workers), upload 0.8, GPU 2,221.1 (BF_1 286.8, BF_2 627.1, BF_3 645.4, BF_4 661.7), decode tail 0.2 | `run7_pipeline_all45.log:1–4`, `:21–34` | as recorded |
| M10 | v3 resources | prepared arrays 2,209 MiB; torch peak 12,526 MiB; `nvidia-smi` peak 18,176 MiB (other processes included); GPU utilisation mean 98.4 % in the GPU phase; **in the prep phase (137.8 s) the GPU is idle**: 271 samples, mean utilisation 0.0037 % (one 1 % sample), median 0 %, all below 20 % | `run7_pipeline_all45.log:37–57`; `validation_pipeline_all45.json` summary `gpu_util.prep`; `pipeline_all45_nvsmi.csv` (`util` in percent) | as recorded; prep idle verified (summary) |
| M11 | the CPU pool's equivalent for the same 18,000 fits | 158,852 CPU-s ÷ 29.87 = 5,318 s (88.6 min; the README divides by 29.9 and gets 5,313 s); an **estimate** from the store's per-fit `secs`, not a separate run | store `secs` (§12, run P3); `run7_pipeline_all45.log:36`; README:241–249 | verified |
| M12 | the flyvis-65 run's synthetic stage | 7,846 s; 234,369 CPU-s in the store; effective parallelism 29.87 | flyvis-65 stdout log line 60; store (§12, P3) | verified |
| M13 | shares of the stage's CPU-s | BF_1–BF_4 on `ko` (base + shuffles) 67.8 %; rule #2.1 in all masks 31.0 % (shuffles 25.3 %, permuted-block ceilings 4.9 %); BF ceilings, BF fixed λ and N1 together 1.2 % | store (§12, P3) | verified |
| M14 | rule #2.1 port, all shuffles | 2,030.5 s wall on the GPU path (of which GPU `bf_als` 1,141.9 s, CPU ridge steps in the GPU process 529.6 s, prep 156.6 s, the rule's remaining CPU fit 110.5 s) against 59,379 CPU-s ÷ 29.9 = 1,986 s | `run8_rule_sh_all45.log:1–45` (summed), `:56–58` | verified (sums) |
| M15 | λ of the shuffled banks | λ = 100 in 4,291 / 4,416 / 4,446 / 4,450 of 4,455 (BF_1–BF_4); near-ties (a λ within 1e-7 of the tie threshold) in 1,586 / 1,665 / 1,689 / 1,678 of 4,500 banks; none flipped. **The near-tie counts are one arm's (A's 45 worlds, the v3 composition)**: each GPU run of an arm recounts and prints its own by rank (G15); they are never transferred to another arm | store (§12, P3); `run7_pipeline_all45.log:1–4`; `validation_pipeline_all45.json` summary `near_ties_by_rank` | verified (λ); as recorded (near-ties; the inner log-likelihoods are not saved, so they cannot be recounted from a file) |
| M16 | the flyvis-65 run's synthetic fits equal the pinned pre-run store | 19,110 + 9,555 = 28,665 compared; 0 differences in p, λ, labels, score | flyvis-65 stdout log line 94 | as recorded |
| M17 | ceilings, fixed λ, N1, permutations | not ported, not timed | README:313–319 | as recorded |
| M18 | the 18,000 v3 fits by (rank × λ × view), λ read from the reference | rank 1, λ ∈ {1, 3}, base view: **37 fits, 5 not bit-equal**; rank 1, λ ∈ {1, 3}, shuffle: 164, 0; rank 1, λ = 100 (base 8, shuffles 4,291): 4,299, 0; ranks 2–4, any λ: 13,500, 0. No other λ occurs at rank 1. The v2 set (M4) is a subset of the v3 set. E1's fields on all 18,000: 0 λ, 0 label (of 1,152,000), max AUC difference 0.0 | `validation_pipeline_all45.json` rows (`lam_ref`, `p_bit_equal`); the same four denominators from the pinned pre-run store's `lam` (§12, P6) | verified (rows; Ark's breakdown, 10:52 UTC, reproduced exactly) |
| M19 | the lattice of `synthetic_worlds.csv` (revision 1.2) | smallest gap between distinct values over the 270 rows, per column: 1/2048 (4.883e-4) for `auc`, `M_real`, `ceiling_full`, `auc_fixed_lambda1`; 1e-4 for `p_P`, `p_P_rowcol`, `p_P_fixed_lambda1`; `outside_density` 1/4161, `regrown_share_block` 1/1024, `precision_at_32` 1/32, `p_S` 1e-2; `auc_other_59` 1.60e-5 **between rows**, but each row lies on its own lattice 1/(2ab), a + b = 59, a ∈ {27, 28, 29}, a step of at least 5.7e-4 (it is in `CSV_EXACT_COLUMNS`); continuous: `D` 2.78e-17, `logloss` 8.7e-6, `logloss_margin_over_N1` 5.5e-5, `regrown_share_full` 3.9e-6 | pinned `synthetic_worlds.csv` (§12, P7) | verified (Ark's table, 11:15 UTC, reproduced; `auc_other_59` reclassified, `logloss_margin_over_N1` added) |
| M20 | the tie census of the pinned pre-run store (revision 1.2; pairs = present × absent by the record's own `y`, §5 E2-II) | all 28,665 records: 27,123 with at least one exact tie, 782,376 exact ties; **1 record with smallest gap < 2^-24**, `world:M0.85:0\|sh:10\|\|ko\|\|rule` (1.836e-8, no tie; a rule shuffle, CPU in D1 scope); next smallest 9.08e-8 (`world:M0.85:2\|sh:79\|\|ko\|\|BF:1`–`BF:4` and `…\|\|N1`); 438 records with smallest gap < 1e-5, of which 32 are tie-free (31 in [2^-24, 1e-5) plus the one below). **D1 scope (the 18,000 `ko` BF fits):** 17,604 fits with a tie, 423,777 ties; smallest gap 9.08e-8; **0 at risk**; 333 with smallest gap < 1e-5. M3's five: 0 ties each; smallest gaps 6.31e-5 (M1.0:0), 1.06e-3 (M1.0:4), 9.46e-5 (M0.75:0), 1.26e-4 (M0.85:0), 2.97e-4 (M0.85:2). `block‖N1`: 45 of 45 with p constant (1,024 ties of 1,024 pairs, AUC 0.5); `full‖N1`, `ko‖N1` not constant (`world:R:0\|\|full\|\|N1`: 10 ties, 35 distinct values). Shuffles hold 10 to 41 present cells, so 540 to 1,024 pairs | pinned `raw_fits.json.gz` (§12, P7) | verified (Ark's census, 11:15 UTC, and Zcode's 438, 11:25 UTC, reproduced; one label corrected, §15) |

The two logs of the registered CPU run are
`connectome-seed-data/knockout_regrow/flyvis65_20260925T171656Z_74de0401a21f.stdout.log`
("the flyvis-65 run's log") and its private folder. The pinned pre-run folder passed
`sha256sum -c SHA256SUMS.txt`, five of five, at drafting (§12, P4).

**On "×2.3".** End to end, 5,318 / 2,362 = 2.25; GPU phase alone, 5,318 / 2,221 = 2.39; the README
says "about 2.2x" (README:54, :305) and the male arm's D13 says "about 2.3 times" (its line 977 at
`a6761e2`). All four describe the BF part only. For a whole synthetic pass the hybrid saves about
38 %, not a factor 2.3 (§9; the male arm's revision 1.1 says the same, its lines 820–825).

## 3. The base-view differences, and why a GPU fit depends on its batch

### 3.1 What the files show

1. **Float64 throughout; the float32 cast absorbs almost every difference.** In v1's live
   comparison the float64 accessor differs from the CPU by 1.1e-16 to 2.2e-16 on 175 fits
   (`run3.log`, e.g. lines 1–4), so the GPU's U, V are not bit-equal to the CPU's on *any* fit;
   decode's float32 round trip (`harness.py:273–277`) maps them to the same float32 parameters on
   17,995 of 18,000 v3 fits (M2, M3). Bit-equality of `p` is therefore a property of the cast, not
   of the float64 arithmetic.
2. **The differing fits are rank 1 at small λ.** All 5 BF differences are BF_1 at λ 1 or 3 (M3);
   the 3 rule #2.1 differences are rule fits (rank 1 by `RANK == 1`) at λ 3 (M6). On those fits the
   float64 difference is 1.4e-9 to 3.8e-8 before the cast (M5), large enough to cross a float32
   rounding boundary. That these fits have a flat objective is Zcode's reading (chat 09:32 UTC); no
   file measures the curvature.
3. **The rule's three.** The README records a check by the CPU `fit_existence` on the same views:
   same λ, u within 3.2e-7, all quantised symbols equal, one float32 step in `s_uv` (and `s_w` on
   M0.75:3), offset, counts and signs equal (README:211–219). No log or JSON of that check exists
   in the directory ("tool only").
4. **Which fits differ depends on the batch.** v2 with the 45 base views in one batch misses 3
   (M4); v3 with all 4,500 banks misses 5 (M3). The two engines give different `p` on **at least
   3** of the 180 base fits: M1.0:0 and M0.85:2 (bit-equal to the CPU in v2, not in v3) and M1.0:4
   (not bit-equal in either, with max |Δp| 5.54e-8 in v2 and 3.16e-8 in v3, so the two `p` differ).
   M0.75:0 and M0.85:0 have the same max |Δp| in both and cannot be told apart, because neither
   run saved the per-fit `p` (§11, row G-(4)). The v2 set is a subset of the v3 set (M18). No
   direct v2↔v3 comparison of `p` was made; "at least 3" is inferred from the two comparisons
   with the CPU, not measured between the engines.

### 3.2 Zcode's probe (`C:\Users\mikha\AppData\Local\Temp\gpu_probe\`, read at drafting)

- **Self-stability.** `probe_once.py` runs engine v2 (`gpu_fit_bf_prepared`) on the three base
  views M1.0:0, M0.85:2, M0.75:0, ranks 1 and 4, and writes the sha256 of the raw float64 bytes of
  `bf_U`, `bf_V`, `bf_lambda` (18 hashes). **Three** runs are in the folder: `run1.txt` and
  `run2.txt` (`chunk=25000`) and `run3.txt` (`chunk=2000`); all three give the same 18 hashes. The
  chunk change does not change the batch here: 3 views × 10 folds × 5 λ = 150 inner problems fit in
  one chunk at both sizes (`row_chunk // starts` = 2,500 or 200; `gpu_bf2.py:111`). All three ran
  with `det=False` (line 1 of each file): deterministic algorithms were **off**.
- **What the self-stability result covers (A3, Ark 10:52 UTC).** It was measured with the flags
  off, on engine v2, on three views. D6 turns the flags on, so **the 18 matching hashes do not
  carry over** to the registered configuration: V1 measures self-stability again under D6 on
  engine v3, and also compares the set of differing base fits under D6 with the flag-free state
  (M3's five, v3). Chunk size: run1 (`chunk=25000`) and run3 (`chunk=2000`) agree on 18 of 18
  hashes; as noted above, no chunk boundary moved between them.
- **Batch sensitivity.** `run4_all45batch.txt` holds the same three views fitted inside a 45-view
  batch: the BF_1 `bf_U` and `bf_V` hashes of all three differ from `run1.txt` (lines 1–9 against
  `run1.txt:2–10`); the BF_4 hashes and every λ are equal. So batch composition is sensitive. The
  script that produced `run4` is not in the folder (`probe_once.py` fixes the three worlds, :32),
  and the file has no header line (no stamp, no `det`, no script name, no chunk), so its producer
  cannot be checked. **It is recorded as historical evidence without provenance**; V4 (d)
  re-shoots it with a header, and until then no registered choice rests on it alone.
- **Root cause (Zcode, chat 09:32).** Not float32; float64 reduction order (cuBLAS / cuSOLVER
  against numpy's BLAS / LAPACK, `torch.sigmoid`, the held-out sum), quantised by the float32 cast
  on both sides. The code supports the list of places where the order or the formula differs
  (§1.2); which of them moves the five fits is not measured. "Δp = one float32 ulp (5.63e-8 ≈
  2^-24)" is not exact: 5.63e-8 is the observed maximum; 2^-24 = 5.96e-8 is the float32 spacing
  for p ≥ 0.5 (smaller at smaller p); `p` is stored as float64 (§11, row G-(5)).
- **Economics (Zcode).** A hybrid pass about 38 % faster, 4,870 s against 7,846 s. The drafter's
  arithmetic gives 4,890 s (§9); the two agree within 0.5 %.

### 3.3 What follows

A GPU fit is a function of **(its bank, the code, the software and hardware stack, the batch
composition)**, not of its bank alone. The CPU fits are functions of the bank and the code, run in
any order on any worker. Three consequences are registered here: the batch composition (the
ordered key list, `starts`, the rank order) is part of the instrument and is fixed, while
`row_chunk` is recorded (D5, §6); equivalence to the CPU is claimed on the deciding outputs, not
on the bits of every `p` (D3, §5); and the explanation of the differences is tested, not only
stated (V5, §7).

## 4. Decisions for review (reviewers, then Mike)

Each row says what each option changes. The body follows the recommendation.

| # | question | options (what each changes) | recommendation |
|---|---|---|---|
| **D1** | Scope: what the GPU replaces | **(a) BF_1–BF_4 on the `ko` mask of every synthetic base view and shuffle** (the 18,000 validated fits, 67.8 % of the stage's CPU-s, M13); everything else on the CPU. (b) (a) plus the BF ceilings (`full`, `block`), BF at fixed λ = 1 and N1: +1.2 % of CPU-s, needs porting and a validation of its own. (c) (a) plus rule #2.1: its port runs on engine v2 and is not faster (M14), so it would mix engines for no gain. (d) everything: the permuted-block ceilings and the rest of rule #2.1 are not ported; permutations are scoring only (seconds, A §7 line 1713–1714) and gain nothing | **(a)** |
| **D2** | Engine | **(a) v3 only, end to end, for every registered BF fit.** (b) v2: slower (2,879 s against 2,362 s for the shuffles, M1, M9). (c) v2 for the rule and v3 for BF: two engines whose `p` differ on at least 3 of 180 base fits (§3.1, item 4) | **(a)**; v1, v2 and the rule port stay in the directory as unregistered history, and the registered driver refuses to import them (G8) |
| **D3** | Equivalence criterion against the CPU | (a) **bit-equal `p` through decode on every fit**: already fails (5 of 180 base fits, M3). **(b) E1 + E2 + E3 of §5 (revision 1.2)**: every deciding output exact (λ, labels, AUCs, every exact column of `synthetic_worlds.csv`, every verdict and label string; E1 = E2-I); a **tie census** of every fit, printed by every run, with **0 flipped pairs** required against the reference (E2-II); every **at-risk** fit (smallest gap < 2^-24) with an identical AUC (E2-III); the continuous CSV columns within a bound propagated per differing fit from its own max \|Δp\| (E3). Δp and the per-p float32 bound are printed diagnostics, not criteria: a p-scale bound measures in the wrong place, since decode casts the logit's parameters, not p (§5). This is Ark's and Zcode's decision of 11:15–11:25 UTC, which rejected revision 1.1's E2a (a per-cell bound \|Δp\| ≤ s(p)) and the three ways of keeping it. (c) exact deciding outputs only, no census: a drift of the instrument that reorders two cells without yet moving an AUC would go unseen. **What (b) does not see:** a drift that moves no pair's order and no exact output; it is printed (Δp), not refused, and between an arm's pre-run and its run R5 still requires bit-equality | **(b)** |
| **D4** | Reference of the validation | **(a) A's pinned pre-run store** `synthetic_rev3_prerun/raw_fits.json.gz` (under `PRERUN_SHA256`, A §7), read after `check_prerun_files`. (b) the flyvis-65 run's synthetic store, which the v2/v3 runs used: equal to (a) on every compared field (M16) but not pinned by A's script | **(a)**; the earlier runs' use of (b) is equivalent by M16 |
| **D5** | The batch composition | **(a) part of the instrument**: the ordered key list, `starts` and the rank order (composition and order) are written to the manifest with a digest, the **refusal digest**; a registered GPU run uses the composition of its pre-run, and a run whose refusal digest differs is refused. **`row_chunk` and the chunk boundaries that follow from it are recorded values, not part of the refusal digest** (Ark, A3): chunk size moved no hash in the probe (run1 against run3, 18 of 18), while batch composition did (run1 against run4). Because no chunk boundary moved between run1 and run3 (§3.2), V4 (c) tests a chunk change that moves every boundary at full scale; if any hash changes there, `row_chunk` returns to the refusal digest in the revision that registers V1–V5's results. An out-of-memory error stops the run (never an automatic smaller chunk). (b) make every fit independent of its batch (no active-set compaction, fixed padded batch shapes): unknown cost, and not shown to remove the dependence, since cuBLAS may still pick its kernel by batch size. (c) ignore it: a rerun with another chunk or another bank list could change 5-odd base fits without anyone knowing why | **(a)**; (b) is future work, a revision of its own |
| **D6** | Determinism settings | **(a) on and measured**: `CUBLAS_WORKSPACE_CONFIG=:4096:8` set before torch is imported (the value found is recorded, and a different value refuses), `torch.use_deterministic_algorithms(True)` with no `warn_only`, TF32 off for matmul and cuDNN, `cudnn.deterministic = True`, `cudnn.benchmark = False`. TF32 does not touch float64, so that setting is recorded, not relied on. Every validation run is made with (a), since (a) may change the bits relative to the flag-free runs of §2; the probe's 18 matching hashes (flags off, engine v2) do not carry over, and V1 compares the set of differing base fits under (a) with the flag-free state (M3). (b) off, relying on the probe's 3 of 3 stable runs, which were all made with the flags off | **(a)** |
| **D7** | Python environment | **(i) `autoresearch-win-rtx/.venv` with a stamp check at start**: Python 3.10.20, numpy 2.2.6, torch 2.9.1+cu128, CUDA 12.8, the sha256 of the three bundled CUDA DLLs, the driver version and the GPU name must equal the registered stamp, else the run refuses. **The registered stamp is the one measured in V1** and written into the revision that registers V1's results; it travels as a registered value, and every later run (an arm's GPU pre-run and its registered run included) must equal that registered stamp, not merely be equal between its own pre-run and run (Ark, D7). Cheap; but the venv belongs to another project, which may upgrade it and block a planned run. (ii) a dedicated venv for this repository, created from a committed lock file: safe from the other project; costs a download of about 3 GB and a check that its numpy build equals `tools/.venv`'s | **(i)** now, with the refusal; (ii) before a second arm names the instrument |
| **D8** | How a hybrid synthetic step runs | (I1) the arm's script imports the GPU engine and runs in the torch venv: one process, but the CPU part leaves `tools/.venv`, the environment A §7 registers. **(I2) two stages from one committed head**: the GPU stage writes a store of BF `ko` records and a manifest; the arm's script, in `tools/.venv`, checks that manifest (same head, file hashes, key set, composition digest, stack stamp, degree-term digest), takes those records, and fits everything else on the CPU | **(I2)** |
| **D9** | A's fixed-λ path check under the hybrid | A's check refits the five knockout fits of the first bank whose five selected λ = 1 on the CPU and requires `p` exactly equal to the selected fit's (`knockout_regrow.py:1812–1830`). Under the hybrid the selected BF fits are GPU fits. (a) keep exact: passes on A's worlds (the bank is `world:W:0`, flyvis-65 log line 68, not among M3's five), but on another arm's worlds the bank may be a sensitive one, and the check would stop the synthetic step for a difference that D3 tolerates. **(b) BF exact on λ, labels and AUC, with 0 flipped pairs between the CPU refit and the selected GPU fit (E2-II's definition, §5), the refit's \|Δp\| printed; rule #2.1 exact as now** (it stays on the CPU). (Revision 1.1 read "`p` within E2a"; E2a is withdrawn in revision 1.2.) (c) refit on the GPU in the identical final-stage batch: exact, but only a determinism test, not a test of the fixed-λ path | **(b)** |
| **D10** | The degree terms | **(a) computed by the GPU stage as A's `--synthetic-only` computes them** (§1.4), with their digest in the manifest; the CPU stage computes its own, and the two digests must be equal (G13); a poisoned-block test (T-G5) shows that no block cell enters. (b) passed in from the CPU stage by file: one computation, but the GPU stage then depends on an unpinned intermediate file | **(a)** |
| **D11** | Which arms may use it | **Only an arm whose registration names the hybrid instrument before its pre-run, so that pre-run and registered run are made by the same instrument and the same batch composition.** Block A: never (its verdict is made). Male CNS arm: stays on the CPU (its D13 (i)); a GPU run of its worlds is an unregistered cross-check (V8). Block B: stays on the CPU (its D12 (i)) unless its registration is revised before its pre-run, after this validation passes. Future arms: may name it | as stated |
| **D12** | Go or wait | **(a) validate the BF-only hybrid now** (§7, about 2 h 50 min of GPU): it saves about 49 min per synthetic pass of a flyvis-65-sized arm (§9). (b) wait until rule #2.1 is faster on the GPU: the saving would grow toward about 65 %, but no port exists that is faster (M14). (c) drop it | **(a)** |
| **D13** | The rule #2.1 port | **(a) unregistered**; a port onto engine v3, with the ridge steps in the pool, is a later revision with its own validation. (b) register it on v2 now: not faster (M14) and a second engine (D2) | **(a)** |

## 5. The equivalence criterion (D3 (b))

Evaluated once, on A's 45 worlds, against A's pinned pre-run store (D4), with the registered batch
composition (§6) and the determinism settings (D6). All three parts must hold.

**E1, exact (the deciding outputs); E2-I of the decision of 11:15–11:25 UTC, unchanged.**
- λ equal on every one of the 18,000 BF fits (4 ranks × 45 worlds × (99 shuffles + 1 base view)).
- Labels (`p >= 0.5`) equal on every one of the 1,152,000 cells; AUC (`knockout_regrow.auc`)
  equal on every fit.
- Through A's own writer on a hybrid store (V3): every **exact** column of
  `synthetic_worlds.csv` (`CSV_EXACT_COLUMNS`, `knockout_regrow.py:2264–2268` at `74db080`: the
  identity and lattice columns, AUCs, `p_S`, `p_P`, `n_ge`, the λ columns and the rest) equal to
  the pinned CSV, rows matched by key; `mechanism_description` equal as a string; every world's
  printed verdict line and label equal as strings to those of an A `--from-raw` pass over the
  pinned store itself; the `ko1` count equal (47 copied, 178 fitted).

**E2, the tie census (revision 1.2; replaces revision 1.1's E2a and E2b).** Decided by Ark (11:15
UTC) and Zcode (11:25 UTC), who rejected E2a (a per-cell bound |Δp| ≤ s(p)) and the three ways
of keeping it (§15). E1 and E3 stay as in revision 1.1.

*Why a census.* A GPU `p` enters the deciding outputs through the **order** of the 64 cells'
values, not through their size. Within a row, every exact column of `synthetic_worlds.csv` sits
on a lattice whose step is at least 1e-4 (M19; `auc_other_59` on a per-row lattice of at least
5.7e-4), while the observed Δp is at most 5.63e-8 (M3). A difference that small moves an exact
column only by changing the order of two cells. The paths, read from `evaluate_bank`
(`knockout_regrow.py:1015–1100` at `74db080`, unchanged at the current head):
- **Present × absent pairs, by the record's own `y`.** `auc` = (gt + 0.5·eq) / (n_pos·n_neg)
  (`:501–510`): one tie turned into an order moves it by 0.5 / (n_pos·n_neg), which is 4.88e-4 at
  32 / 32, exactly one step of its 1/2048 lattice; an opposite order moves it by two steps. From
  `auc` follow `M_real`, `n_ge` (against `m_real − TAU` on the shuffles, `:1049`), `p_S` and the
  `regrown_share` ratios. `auc_other_59` and the per-type AUCs use subsets of the same pairs
  (`:1053–1055`, `:1075`); `precision_at_32` (`:909–912`) changes only when a present and an
  absent cell trade places across the 32nd rank (ties broken in block cell order).
  `auc_fixed_lambda1` and `p_P_fixed_lambda1` read the selected `ko` fit's `p` where the `ko1`
  record is a copy of it (`reused_from_ko`, `:1845`). A shuffle's `p` enters only through
  `auc(p, y_sd)` (`:1025–1034`).
- **Any pair of the 64 cells, on a base view (drafter's addition; not in the decision, for the
  reviewers).** `p_P` and `p_P_rowcol` rank the base view's `p` over all 64 cells (`auc_null`,
  `avg_ranks`, `:513–536`) and score the ranks against permuted labels (`Yu`, `Yrc`,
  `:1022–1023`). Under a permutation, two cells with the same label in `y` take different labels,
  so a same-label pair that changes order moves that permutation's null AUC by one step, and
  through `null >= a − TAU` it can move the count behind `p_P`. Ark's "the only path is a flipped
  tie in `auc`" (11:15 UTC) holds for the shuffles, not for a base view's `p_P`; the census
  therefore takes all pairs on a base view.

*Definitions.*
- **Census pair set S(f).** On a shuffle: the present × absent pairs by the record's own `y` (the
  64 booleans of `bank.exists` in block cell order, `knockout_regrow.py:860`; present and absent
  cells are interleaved, so "the first 32 against the last 32" is not this set and gives other
  numbers, Zcode, 11:25 UTC). There are n_pos·n_neg of them: 1,024 at 32 / 32, 540 to 1,024 on
  A's shuffles, which hold 10 to 41 present cells (M20). On a base view: all 2,016 unordered pairs
  of the 64 cells, with the 1,024 present × absent pairs printed as their own sub-count. `y` is
  read from the reference record; the GPU record's `y` (G4, from the same bank) must equal it,
  else E1 fails.
- **Order state** of a pair (i, j) under p: sign(p_i − p_j) ∈ {−1, 0, +1}, compared exactly on the
  decoded float64 `p` (no tolerance).
- **Exact tie:** a pair of S(f) with p_i = p_j. **Smallest gap:** min |p_i − p_j| over the pairs
  of S(f) with p_i ≠ p_j (reported as "none" if p is constant on S(f), as on `block‖N1`).
- **Flipped pair** (the decision's "flipped tie"), defined only between a GPU fit and its CPU
  reference: a pair of S(f) whose order state under the GPU `p` differs from its order state under
  the reference `p`, that is, **tied on one side and ordered on the other (0 against ±1), or
  ordered oppositely (+1 against −1)**. A pair tied on both sides, or ordered the same way on both
  sides, is not flipped, whatever the |Δp| of its cells. The count is over pairs, so two flips never
  cancel in it, although their effects on `auc` can.

*The criterion.*
- **E2-I, exact:** E1 as it stands (λ, labels, AUC, the exact columns, the strings).
- **E2-II, the census, printed by every GPU run (G16):** per fit, the number of exact ties (with
  the present × absent sub-count on a base view), the smallest gap, and, where a reference
  exists, the number of flipped pairs. **Required: 0 flipped pairs on every fit**; otherwise each
  flipped pair is named (fit key, the two block cells, both sides' `p` and order states) and the
  instrument is refused. Against A's pinned store (V2) and against the male CPU pre-run store
  (V8), all three numbers are printed. **In an arm run with no CPU reference** (the GPU stage of a
  hybrid pre-run or registered run), the census prints ties, gaps and the at-risk list; it
  cannot say whether any pair flipped, since a flip is a comparison with a CPU fit that the arm
  does not make. Flips are measurable only against a reference (V2, V8). Between an arm's GPU
  pre-run and its GPU run, R5's bit-equality implies 0 flips between the two.
- **E2-III, at risk:** a fit is **at risk** if its smallest gap is below **2^-24 = 5.96e-8**, the
  float32 spacing on [0.5, 1), used as the universal bound (not the observed maximum, 5.63e-8).
  Every at-risk fit is named in the print, and **an at-risk fit must have an identical AUC** (on
  a base view also identical `p_P` and `p_P_rowcol`, by the drafter's addition above); if one
  differs, the instrument is refused. Against a reference E2-III is contained in E1, which already
  requires every AUC to be identical; what it adds is the named list, so that a pass on an
  at-risk fit is recorded as a case exercised, and a threshold against which another arm's census
  is read. On A, D1's scope holds **0 at-risk fits** (smallest gap 9.08e-8, M20). The store's one
  at-risk record, `world:M0.85:0|sh:10||ko||rule` (1.836e-8, tie-free), is a rule #2.1 shuffle: it
  was bit-equal in the unregistered rule port's run (M7, engine v2), so an at-risk fit has held
  once, but on the rule port, not on the registered engine or in its scope (D1, D13).
- **Printed beside E2-III, not a criterion (drafter's addition, for the reviewers):** the fits
  whose smallest gap lies in [2^-24, 2^-23). Two cells moving in opposite directions by up to
  2^-24 each close a gap of up to 2^-23 = 1.19e-7, and one float32 step of p is not a bound on Δp
  (below). On A: 4 fits of D1's scope, `world:M0.85:2|sh:79||ko||BF:1`–`BF:4` (9.08e-8 each, the
  same pair as that shuffle's N1), all bit-equal (M2).
- **Diagnostics, printed, never deciding (revision 1.1's E2a and E2b):** each fit's max |Δp|, the
  cell where it occurs, that cell's reference p, s(p) = `np.spacing(np.float32(p))` and the ratio
  |Δp| / s(p); the number of fits not bit-equal per (rank × λ × view) cell, against denominators
  fixed from the reference store's λ before the GPU stage starts (on A, 37, 164, 4,299 and 13,500;
  §12, P6; never the GPU run's own λ). A cell whose count rises against V1's is reported in the
  chat.

*Why Δp and the per-p bound are diagnostics (revision 1.1's analysis, kept as the reason).* Decode
casts the *parameters* (the N1 terms, U, V) to float32, not p; p is a float64 sigmoid of a float64
sum (`harness.py:273–277`, `decoders/bf_decode.py:10–12`). One float32 step of the logit z_i moves
p by about p(1 − p)·s(z_i), and on M3's five fits this exceeds s(p_i) at 16 to 33 of the 64 cells
(those far from p = 0.5, where |z| is above about 1): there a per-p bound is tighter than one cast
step of the logit, and it would refuse a difference of the same origin as M3's. Conversely, the
largest observed difference (M0.85:2, 5.63e-8) is larger than p(1 − p)·s(z_i) at every cell of
that fit (at most 2.27e-8): it is not one step of z at any cell but the sum of steps of several
parameters. A p-scale bound therefore measures in the wrong place: its size is set by where the
cast happens (on the logit's parameters), while the outputs consume the order of the cells.
Revision 1.1 also found that E2a could not be decided on M3's five from the files (no per-cell GPU
`p` was saved). The census can be read from the reference alone: a pair flips only if
|Δp_i − Δp_j| reaches its gap.

*The census on A (M20; CPU reads of the pinned store, §12, P7).*

| fit | λ | max \|Δp\| (v3) | exact ties (all pairs / present × absent) | smallest gap, present × absent | smallest gap, all 2,016 pairs | all-pairs gap ÷ (2 · max \|Δp\|) |
|---|---|---|---|---|---|---|
| M1.0:0 BF_1 | 1 | 2.333e-8 | 0 / 0 | 6.31e-5 | 6.31e-5 | 1,353 |
| M1.0:4 BF_1 | 3 | 3.156e-8 | 0 / 0 | 1.06e-3 | 8.15e-5 | 1,291 |
| M0.75:0 BF_1 | 3 | 1.631e-8 | 0 / 0 | 9.46e-5 | 2.01e-5 | 615 |
| M0.85:0 BF_1 | 1 | 2.937e-8 | 0 / 0 | 1.26e-4 | 7.02e-5 | 1,196 |
| M0.85:2 BF_1 | 3 | 5.632e-8 | 0 / 0 | 2.97e-4 | 1.22e-4 | 1,085 |

On each of the five, |Δp_i − Δp_j| ≤ 2 · max |Δp| is more than 600 times smaller than the smallest
gap, so no pair can flip: their AUC, `p_P` and `p_P_rowcol` provably cannot move. The other 17,995
fits of D1's scope are bit-equal (M2, M3) and cannot flip either. So **0 flipped pairs in 18,000
fits on A**, derived from the files, not counted from saved GPU `p` (none was saved; V2 counts
them). **Every tie of D1's scope on A (423,777 in 17,604 fits, M20) sits on a bit-equal fit**: on
A no tie was ever exposed to a nonzero Δp.

*Why the census must be repeated on another bank (Ark, 11:15 UTC).* Tie structure depends on the
bank (density, boards, degenerate shuffles): on A, `block‖N1` is constant on all 45 worlds (1,024
ties of 1,024 pairs, AUC exactly 0.5, which no flip can move), while `full‖N1` and `ko‖N1` carry
ties without being constant (M20); "1,024 / 1,024" is a property of A's block bank only. **0
flips in 18,000 is a fact about A.** Ark's candidate mechanism for it, that both members of a tied
pair go through the same reduction and move together, is **unverified**: on A no tied pair sat on
a fit that differed. V8 repeats the census on the male arm's worlds during that arm's pre-run,
before it unseals; it separates "by construction" from "luck" only if some male fit that differs
from its CPU reference carries ties, and V8 prints how many do (if none, the question stays open
and is said to be open). The census costs seconds: at most 2,016 pairs per fit, no fit made.

*Scope: the census applies to the fits the GPU produces.* Under D1 (a) these are the 18,000 `ko`
BF fits (base views and shuffles), and the `ko1` records copied from them. The ceilings (`full‖*`,
`block‖*`, and the `|pc:` family, `full‖rule`), the `ko1` fits the CPU makes, N1 and rule #2.1 are
fits of the pinned CPU harness in the hybrid as well; their `p` is the CPU's by construction, no
pair of theirs can flip, and **the census is not applied to them in this instrument**.
`ceiling_full` enters the mechanism, but in D1 (a) it is a CPU AUC over a CPU fit. If a later
revision ports the ceilings (D1 (b)), the census applies to them, with the present × absent pairs
of each record's own `y` (a `|pc:` record's `y` is the permuted `y`, `:1082–1083`), and that
revision registers it. For scale only: the `|pc:` family holds 7,828 ties in 502 of its 900 fits
on A, smallest gap 2.04e-7 (M20 counts; §12, P7).

**E3, the continuous columns, within a bound propagated per differing fit (Ark's A2).** A's gate
compares `D`, `logloss`, `logloss_margin_over_N1`, `regrown_share_full`, `regrown_share_block`
within `MACHINE_CHECK_TOL` = 1e-9 (`knockout_regrow.py:319`, `:2269–2270`). That tolerance was set
for two CPU runs and **cannot be E3**: on the differing rows it would give outcome 3(b) of A's
gate. At p = 0.5, a Δp of 5.6e-8 on one cell already moves `D` by 5.6e-8 / (0.25 × 32) ≈ 7e-9.
For each fit whose `p` is not bit-equal, with δ = that fit's own max_i |Δp_i| (observed) and p_i the
reference `p`, the bound is computed and **printed per differing fit, not as a constant** (derived
from the code at `74db080`, unchanged at the current head):

- **`D`** = `parity_D(logit_of(p), y)`: the mean of logit(p) over the present block cells minus the
  mean over the absent ones (`knockout_regrow.py:478–483`, `:1010–1012`, `:1059`). By the mean
  value theorem each cell's logit moves by at most δ / min over [p_i − δ, p_i + δ] of p(1 − p), and
  p(1 − p) is concave, so that minimum is at an endpoint. Each of the two means moves by at most the
  largest cell change, and they can move in opposite directions, so
  **|ΔD| ≤ 2δ / q_min**, with q_min = min_i min_{s = ±1} (p_i + sδ)(1 − p_i − sδ).
  The factor 2 comes from `D` being a difference of two means. The tighter form
  δ · (mean_{present} 1/(p_i(1 − p_i)) + mean_{absent} 1/(p_i(1 − p_i))) is printed beside it as a
  diagnostic.
- **Where `logit_of` clips** (p ≤ 1e-300 or p ≥ 1 − 1e-16, `knockout_regrow.py:1011`) the
  propagation is switched off, not computed: those cells are left out of q_min, and a change of `D`
  that such a cell causes is not covered and fails E3. The pinned store has no such cell among the
  11,520 cells of the 180 base BF fits (§12, P6).
- **`logloss`** = `harness.score`'s `existence`, one mean over the 64 cells of
  −[y log p̃ + (1 − y) log(1 − p̃)], p̃ = clip(p, 0.001, 0.999) (`harness.py:65`, `:490–494`). One
  mean, so no factor 2: **|Δlogloss| ≤ δ / m_min**, with m_min = min_i of p̃ (present) or 1 − p̃
  (absent), taken over the endpoints p_i ± δ after the clip (so m_min ≥ 0.001 and the bound is
  always finite; a cell whose whole interval lies beyond one end of `CLIP` contributes nothing).
- **`logloss_margin_over_N1`** = ll_N1 − logloss (`knockout_regrow.py:1060`): the same bound, since
  N1 is a CPU fit and identical.
- **`regrown_share_full`, `regrown_share_block`** = (AUC − 0.5) / (ceiling − 0.5)
  (`knockout_regrow.py:915–921`): the AUC is exact by E1 and the ceilings are CPU fits, so they must
  be exact.
- A bit-equal fit's row must be exact in all five columns.

What the bounds would be on the five fits of the flag-free v3 run (pinned `p`, each fit's own δ;
V3 prints its own from V1's δ):

| fit | δ | q_min | **`D` bound 2δ/q_min** | tighter form (diagnostic) | m_min | **`logloss` bound δ/m_min** |
|---|---|---|---|---|---|---|
| M1.0:0 BF_1 | 2.333e-8 | 0.0311 | 1.50e-6 | 3.13e-7 | 0.0901 | 2.59e-7 |
| M0.85:0 BF_1 | 2.937e-8 | 0.0296 | 1.99e-6 | 4.28e-7 | 0.147 | 2.00e-7 |
| M0.75:0 BF_1 | 1.631e-8 | 0.0617 | 5.29e-7 | 2.16e-7 | 0.134 | 1.22e-7 |
| M0.85:2 BF_1 | 5.632e-8 | 0.0616 | 1.83e-6 | 6.52e-7 | 0.171 | 3.30e-7 |
| M1.0:4 BF_1 | 3.156e-8 | 0.1145 | 5.51e-7 | 3.25e-7 | 0.152 | 2.08e-7 |

**Reconciliation with revision 1's E3 numbers.** Revision 1 gave 6.2e-7 to 8.7e-7 for `D` and
1.1e-7 to 1.4e-7 for `logloss` on the five rows (at most 4.3e-6 and 4.9e-7 over the 180 base BF
rows). They reproduce (6.18e-7 to 8.74e-7; 1.14e-7 to 1.38e-7; 4.29e-6 and 4.88e-7): they are the
tighter form with δ = 6e-8 on every cell, a valid first-order bound on `D`, and they were not
wrong. Ark's per-fit numbers also reproduce exactly (min p 0.032, 0.031, 0.066, 0.066, 0.132;
largest d(logit)/dp 32.1, 33.8, 16.2, 16.2, 8.7; |ΔD| 1.81e-6, 1.90e-6, 9.13e-7, 9.14e-7, 4.92e-7
for M1.0:0, M0.85:0, M0.75:0, M0.85:2, M1.0:4): they are the global δ = 5.632e-8 times
max_i 1/(p_i(1 − p_i)), which bounds the largest single-cell logit change, not `D`. The formula as
relayed ("max|Δp| / min_i p_i(1 − p_i)") lacks the factor 2: on M1.0:4 its 4.92e-7 is below the
tighter form at the same δ (5.80e-7), so it is not a bound on `D` there. The registered formula is
therefore Ark's with the factor 2 and the endpoint minimum. No ledger row: revision 1's numbers
stand, and the formula as relayed lived in the drafting brief, not in an artefact (the same case
as the note under §11).

**Prediction, written before V3:** A's gate with its 1e-9 tolerance would report outcome 3(b) on
the differing BF_1 rows (five in the flag-free v3 run); E3 is the comparison that decides for this
instrument.

**Outcomes (revision 1.2).** (1) E1, E2-II (0 flipped pairs), E2-III and E3 hold: the instrument
is equivalent on A's worlds, and the result, with the census (ties, gaps, the at-risk list), the
set of differing fits and the diagnostics, is committed. (2) E1 holds, and E2-II finds a flipped
pair or E3 does not hold: refused; the reviewers decide whether a revision is needed. (3) E1 fails
anywhere, an at-risk fit's AUC included (E2-III): refused; the instrument changed a deciding
output. The diagnostics (Δp, s(p), the counts per cell) never decide an outcome.

## 6. The reproduction gate of a GPU run (the analogue of A §3.3)

A GPU run registered for an arm (the GPU stage of a hybrid pre-run or registered run) must pass
every item before its records are used; each item is a stop.

- **R1, environment stamp** (D7): the registered stamp, the one measured in V1 and written into
  the revision that registers V1's results, equals the run's, field by field; equality between a
  run and its own pre-run is not enough. The manifest records it (G2).
- **R2, determinism settings** (D6): set before torch is imported and read back after
  (`torch.are_deterministic_algorithms_enabled()` is True, the workspace variable in effect is
  `:4096:8`); a `RuntimeError` from a non-deterministic operation stops the run.
- **R3, thread preamble and record:** the four thread variables set before numpy loads in the main
  process and in every prep worker, as found and as in effect (A's `THREAD_ENV_FOUND` form,
  `knockout_regrow.py:84–90`); `torch.get_num_threads()` recorded.
- **R4, batch composition** (D5): the refusal digest (the ordered key list, `starts`, the rank
  order) equals the registered one; `row_chunk` and every chunk boundary are recorded in the
  manifest beside it, not refused on (unless V4 (c) returns `row_chunk` to the digest); a
  `row_chunk` other than the pre-run's that moves any bit is still caught by R5. Free VRAM is
  checked before the upload against the registered need (the measured torch peak, 12.5 GB at `row_chunk` 40,000,
  M10); too little VRAM stops the run with no fallback. (The session handover of 2026-09-25 notes
  that `llama-server` can hold most of the 32.6 GB; freeing it is Mike's call.)
- **R5, pre-run reproduced:** the registered run's GPU records equal the arm's GPU pre-run's
  **bit for bit** (per-fit sha256 of the raw U, V, λ and of the decoded `p`, G6). The hybrid CSV
  then goes through the arm's own gate unchanged (A §3.3), whose 1e-9 tolerance applies, since both
  sides are made by the same instrument.
- **R6, the refusals:** no key whose base is not `world:` (so `real`, `real|sh:`, `real|pc:` and
  `real|leak` are refused at every entry), no `|pc:` or `|leak` key (D1 (a)), no write at or in a
  pinned reference folder or a byte copy of one (A's `out_dir_refusal` logic, G11).
- **R7, one head:** the GPU stage and the CPU stage record the same git head and a clean tree under
  `results/genome/c6/` and `docs/plans/`; the CPU stage refuses records whose manifest names
  another head (G13).
- **Printed, not a stop (revision 1.2): the census of E2-II** (G16): per fit, exact ties, the
  smallest gap and the at-risk list (E2-III), and the fits with smallest gap in [2^-24, 2^-23).
  An arm's GPU run has no CPU reference, so it prints no flip count (§5, E2-II); R5 makes its
  census equal to its pre-run's.

The instrument itself is accepted only after **V1**: three full independent runs of the registered
composition, made in fresh processes, with every per-fit hash equal across the three (§7).

## 7. The validation plan

All runs on synthetic worlds only, into private folders under
`connectome-seed-data/gpu_instrument/<tag>_<UTC stamp>_<head 12>/`, each with its manifest and
`SHA256SUMS.txt`; committed aggregates in `results/genome/c6/gpu_instrument/validation/`. The
per-fit `p` and hashes are saved this time (the earlier runs did not, §3.1). GPU times are
estimated from §2; none of these runs was made for this draft. Every run below needs G1–G11 and
G16 (the census, revision 1.2) first, and V3 needs G10.

| run | what | on which worlds | GPU time (estimate) | passes if | refuses the instrument if |
|---|---|---|---|---|---|
| V0 | smoke: settings on, one world | R:0 base + 99 shuffles, BF_1–BF_4 | about 1 min (56 s, M9's one-world figure, `validation_pipeline_one_world_R0.json`) | R1–R4 pass; the hashes with the settings on are compared with a run with them off, and the overhead is recorded | the settings raise an error that cannot be avoided (then D6 (a) cannot be met) |
| V1 | self-stability: three full independent runs of the registered composition | A's 45 worlds, 99 shuffles + base, BF_1–BF_4 (18,000 fits) | about 3 × 40 min = 2 h (plus 3 × 2.3 min of 24 CPU workers) | all 18,000 × 3 per-fit hashes equal. Also reported (A3): the set of base fits that differ from the CPU under D6 against the flag-free set (M3's five), and the environment stamp, which becomes the registered stamp of D7 | any hash differs: "NOT DETERMINISTIC" |
| V2 | equivalence, E1 and E2 | V1's first run against A's pinned pre-run store | none (CPU, minutes; the census seconds) | E1, E2-II and E2-III of §5 (revision 1.2): 0 flipped pairs over every fit's census pair set; every at-risk fit named, with an identical AUC (on A none is expected, M20). Printed: the census of all 18,000 fits (ties, gaps, the at-risk list, the [2^-24, 2^-23) list) and the diagnostics (each differing fit's max \|Δp\|, its cell, s(p); the counts per cell against 37 / 164 / 4,299 / 13,500) | any λ, label or AUC difference; one flipped pair (named); an at-risk fit whose AUC differs |
| V3 | A's gate on a hybrid store, E1 and E3 | a hybrid store: V1's BF `ko` records beside the pinned store's other records; A's script, unmodified, `--synthetic-only --from-raw <hybrid> --out <scratch>`, and the same pass over the pinned store for the reference strings | none (CPU, about 15 s each, plus the path check's five CPU refits) | E1 (CSV exact columns, strings, `ko1` count); E3; the path check passes under D9 (b) | an exact column or a string differs; E3 exceeded |
| V4 | batch sensitivity, a statement, not a gate | (a) the 45 base views as one batch; (b) one world per batch for M1.0:0, M0.85:2, M0.75:0; (c) **required since revision 1.1**: all 45 worlds, the registered key list, at `row_chunk` 100,000, which moves every chunk boundary (D5 rests on it); (d) the probe's `run4` re-shot with a header line (stamp, `det`, script name and hash, `row_chunk`): M1.0:0, M0.85:2, M0.75:0 inside the 45-view batch, under D6 | (a) about 30 s; (b) about 3 min; (c) about 37 min at 26.5 GB (README:301); (d) about 30 s | the report: how many per-fit hashes change against V1, and E1–E3 against the CPU for each composition; for (c), whether `row_chunk` moves any hash | E1 fails under a composition: not a refusal of the registered composition, but it is reported, and D5 (a) is then the only safe option; (c) moves a hash: `row_chunk` returns to the refusal digest (D5) |
| V5 | the explanation of the base differences (Ark's condition) | (a) CPU only: `harness.fit_bf` on the 180 base views with `OPENBLAS_NUM_THREADS=4` exported before launch (another BLAS reduction order), compared with the pinned store; (b) engine v3 on `torch` CPU device, float64, on M3's five fits and five bit-equal controls | (a) none (CPU, a few minutes); (b) none (CPU, minutes) | written before the run: if the fits that move in (a) are mainly the rank-1, small-λ base fits (M3's five or a set overlapping them) while most of the rest stay bit-equal, the differences are a property of those fits under any change of reduction order, and the Δp that E2's diagnostics print is explained (revision 1.1 read "the tolerance of E2a") | (a) moves none of M3's five and (b) reproduces them: the differences come from the GPU code, not from the fits; the instrument then waits for a fix, whatever the census says |
| V6 | negative control: the comparator can separate | engine v3 with `BF_TOL` 1e-5 (instead of 1e-6), R:0 base + 99 shuffles | about 1 min | the comparator flags the run (E1, a flipped pair of E2-II, or E3); its Δp diagnostic is printed beside. Since revision 1.2 no criterion bounds Δp, so V6 now tests whether the census and E1 see a changed stopping rule; whether `BF_TOL` 1e-5 reorders any pair on R:0 is not known before the run | the comparator passes a run made with a changed stopping rule: it cannot separate, and it is refused |
| V7 | the poisoned-block test (T-G5) | R:0 base + 99 shuffles, with the block cells of `harness.REAL` flipped in the GPU process and in every prep worker | about 1 min | every per-fit hash equal to the unpoisoned run | any hash changes: a code path reads a real block cell |
| V8 | cross-check on the male worlds, **unregistered** | the male arm's 45 worlds per lobe, BF `ko`, base + 99 shuffles; needs that arm's script (its S1, S4, S5, S14) and its CPU pre-run store | about 40 min per lobe if A's rate holds on the placed grid (not measured), 80 min for both | E1, E2 and E3 against the male CPU pre-run store, reported in the chat as a cross-check. **Revision 1.2 (Ark): the census is repeated on the male worlds, during that arm's pre-run and before it unseals**, since tie structure depends on the bank and 0 flips in 18,000 is a fact about A (§5): ties, gaps, the at-risk list, the flips counted against the male CPU store, and how many of the fits that differ carry ties (which is what separates "by construction" from "luck") | nothing for the male arm, which stays on the CPU (its D13 (iii)). For this instrument: a flipped pair, or an at-risk fit whose AUC differs, refuses it for every arm that would name it (E2-II, E2-III); a statement about the GPU instrument, not an input to a male gate |

**Totals.** V0–V7: about **2 h 50 min of GPU time** with V4 (c), now required (2 h 10 min without
it), mostly V1; CPU minutes. V8: about 80 min more, after the male pre-run's store exists and
before the male arm unseals. Revision 1.2 changes no run's cost: the census reads the saved `p`
(G5) in seconds and makes no fit, so the totals and the break-even of §9 stand. The GPU runs use 24 CPU
workers for about 2.3 min each and one CPU core for the rest, so they can run while the CPU pool
does other work; the other work would then be slower, not different.

**Order.** G1–G11, G16 and their tests; V0; V6 and V7 (cheap, and they decide whether the comparator
and the refusals work); V1; V2; V3; V5; V4. V8 when the male store exists, before the male arm
unseals. The results go to a revision of this file, which registers the refusal digest, the stamp
measured in V1 (D7), the set of differing base fits with the counts per cell and A's census (ties,
gaps, at-risk list, 0 flips expected), and whether `row_chunk` stays out of the digest
(V4 (c)), and is reviewed before any arm names the instrument.

## 8. Use by registered arms

- **The rule (D11):** an arm may use the hybrid instrument only if its registration names it
  before its pre-run, and its pre-run and its registered run are both made on it, with the same
  composition (the arm's own 45 worlds and their shuffles, in a registered order), the same stamp
  and the same head rules. The arm's limits (γ\*_P, γ_R, the family limit) and its
  `smallest_passing_auc` values are then measured by the hybrid instrument, as A §7 requires for a
  new instrument. The real arm (the real bank's 632 fits, A §7 line 1712–1713) stays on the CPU:
  it touches a real block, and it takes about 3 minutes.
- **Block A:** its verdict (G) is made on the CPU; this instrument never re-reads it. A's worlds
  are the validation set only.
- **The male CNS arm:** stays on the CPU: its D13 keeps (i) and allows (iii), the unregistered
  cross-check (revision 1.1, `a6761e2`, §7.1 lines 809–830 and D13 line 977; all three reviewers).
  Moving it would need its registration revised before its pre-run, and it would lose time: the
  validation (about 2 h 50 min of GPU plus a review) is longer than the saving on one lobe's pass
  (about 49 min). V8 is that cross-check; by the male D13 (iii) its output is an input to no gate,
  reference or registered value. The GPU
  never reads the sealed files: V8 fits synthetic worlds whose degree terms and content come from
  the lobe's outside file (the male draft's S14), not from a sealed file.
- **Block B:** stays on the CPU by its D12 (i)
  (`docs/plans/2026-09-25-knockout-regrow-block-b-registration.md` lines 566–569 and 645, at
  `8591491`). Its pre-run has not been made. If this validation passes before B's pre-run, B's
  registration may be revised to name the hybrid instrument; B would then need the arm adapter
  (G7) for its script and its own composition.
- **Future arms** of this test name the instrument in their registration, with a composition of
  their own worlds.

## 9. Economics, per phase (stated honestly)

Figures for a flyvis-65-sized arm (45 worlds, 99 shuffles, 20 permuted-block ceilings), from the
flyvis-65 run's store and the v3 log (M9–M14).

| phase | CPU only (registered today) | hybrid (D1 (a), run one after the other) | saving |
|---|---|---|---|
| synthetic step, one pass | 7,846 s (130.8 min, measured) | CPU remainder 75,518 CPU-s ÷ 29.9 ≈ 2,526 s, plus GPU BF 2,362 s ≈ **4,890 s (81.5 min)** | ≈ 2,960 s, **≈ 49 min, −38 %** (Zcode: 4,870 s) |
| one arm: pre-run + registered run | ≈ 4 h 22 min | ≈ 2 h 43 min | ≈ 1 h 39 min |
| the real arm | ≈ 3 min | the same (CPU) | 0 |
| the validation of this file (once) | — | ≈ 2 h 50 min of GPU, CPU nearly free | a cost |
| porting BF ceilings, BF fixed λ, N1 (D1 (b)) | — | — | ≤ 1.2 % of CPU-s, ≈ 1.5 min per pass |
| rule #2.1 (31.0 % of CPU-s) | — | the v2 port: 2,030 s against 1,986 s | none today |

**What is not claimed.** (1) Running the GPU stage at the same time as the CPU remainder would
bring a pass toward max(2,526, 2,362) s plus contention, about 2,700 s (−65 %): arithmetic only,
not measured; the GPU stage's 24 prep workers and the CPU pool would compete for the 32 threads.
(2) The "89 min" of the CPU side is the store's `secs` divided by the pool's parallelism (M11), not
a measured run of the BF fits alone. (3) The rate on another bank (the male placed grid) is assumed.
(4) The hybrid's GPU stage begins with its CPU prep (137.8 s on 24 workers, M9), during which the
GPU is idle (mean utilisation 0.0037 %, median 0 %, M10): the 2,362 s include it. Overlapping the
prep with the GPU work is not measured and not claimed.

**Break-even.** The validation costs about as much GPU time as 1.7 arms save (2 h 50 min against
1 h 39 min per arm); the larger cost is
the review. The instrument pays from the second arm that names it, and it saves nothing for the
male arm, which stays on the CPU. Mike's "without loss of quality" is registered as E1 (every
deciding output exact); the `p` values themselves may differ on a few fits, with no pair of cells reordered (E2-II) and
the continuous columns within E3.

## 10. Code changes required (none made by this draft)

All in `results/genome/c6/gpu_instrument/` or in an arm's new script; `harness.py`,
`checks/knockout_regrow.py` and the pinned files stay byte-unchanged.

| # | change |
|---|---|
| G1 | `gpu_env.py`, imported first by every registered GPU entry point: the thread preamble (four variables, found and in effect), `CUBLAS_WORKSPACE_CONFIG=:4096:8` before torch is imported (a different value found refuses), then `torch.use_deterministic_algorithms(True)`, TF32 off, `cudnn.deterministic = True`, `cudnn.benchmark = False`; asserts read back (R2, R3) |
| G2 | the environment record in the manifest (the stamp of V1 is the registered stamp, D7): Python, numpy (`show_config`, `threadpoolctl`) in the main process and in one prep worker, torch, `torch.version.cuda`, cuDNN, the sha256 of `cublas64_12.dll`, `cublasLt64_12.dll`, `cusolver64_11.dll` in `torch/lib`, GPU name, compute capability, total VRAM, driver (`nvidia-smi`), the determinism settings, git head, `tree_dirty_paths`, the LF sha256 of every instrument file and of A's pinned files; the stamp check of D7 (i) (R1) |
| G3 | the batch manifest: the refusal digest of the ordered key list, `starts` and the rank order, with refusal on a digest other than the registered one; `row_chunk` and every chunk boundary recorded beside it, outside the digest (D5); VRAM preflight; no automatic chunk fallback (R4) |
| G4 | per-fit records in A's store schema (`p`, `y`, `lam`, `score` from `harness.score`, `outside_density`; `secs` = the rank's GPU wall time divided by the banks, labelled "apportioned" in the manifest), so that A's writer and gate read them unchanged; no new record field (A's script asserts the declared fields) |
| G5 | the private output folder and `SHA256SUMS.txt`; per-fit decoded `p` saved |
| G6 | per-fit sha256 of the raw float64 U, V, λ and of the decoded `p` (the probe's method), in a sidecar file named in the manifest |
| G7 | the arm adapter: `prep` takes the arm's module (and lobe) instead of importing `knockout_regrow` directly, applies that arm's grid restriction in every worker (the male draft's S5), and accepts only keys `world:<family>:<j>` and `world:<family>:<j>\|sh:<sd>` (R6) |
| G8 | the registered driver uses `gpu_bf3` only and asserts that `gpu_bf`, `gpu_bf2` and `gpu_rule` are absent from `sys.modules` (D2) |
| G9 | `gpu_equivalence.py`: E1, E2 and E3 of §5 (revision 1.2), reading A's pinned pre-run store after `check_prerun_files` (imported read-only from A's script). E2-II: each fit's census pair set S(f) from the reference `y` (present × absent on a shuffle, all 2,016 pairs on a base view), the GPU `y` asserted equal; the order state of every pair on both sides, compared exactly; the flipped pairs counted and each named. E2-III: the at-risk list (smallest gap < 2^-24) with each at-risk fit's AUC (and, on a base view, `p_P`, `p_P_rowcol`) compared. Printed beside: the [2^-24, 2^-23) list; the diagnostics (max \|Δp\|, its cell, s(p) of the pinned `p`, the ratio; the counts per (rank × λ × view) cell against denominators from the pinned store's λ, read before the GPU records are opened). E3's bounds per differing fit from the pinned `p` and that fit's own max \|Δp\|, printed with the tighter form and the count of cells where `logit_of` clips. The census itself is the function of G16 |
| G10 | the hybrid-store builder for V3 (writes to a scratch folder, never into a reference folder) |
| G11 | the output guard: no write at or in `PRERUN_DIR`, the arm references, or a byte copy of one (A's `out_dir_refusal` rule, reimplemented here, since A's script is not modified) |
| G12 | in the arm's new script (not A's): the fixed-λ path check of D9 (b) for BF records made by the GPU (λ, labels, AUC exact; 0 flipped pairs by the census function of G16) |
| G13 | in the arm's new script: the GPU-stage import of D8 (I2): same head, clean tree, file hashes, key set equal to the planned BF `ko` keys, composition digest, stamp, degree-term digest equal to its own (R7) |
| G14 | README corrections for the ledger rows of §11; `validate_vs_cpu.py`'s docstring corrected (row G-(6)) |
| G15 | every GPU run prints and writes to its manifest its own near-tie counts by rank (`fit_bf_all`'s `near_tie`, `gpu_bf3.py:193`); a count from another arm or another run is never carried over (M15) |
| G16 | **(revision 1.2)** one census function (`census.py`), used by G9 and by every GPU run (V0–V8 and an arm's GPU stage): per fit, from its own decoded `p` and `y`, the exact ties on S(f) (with the present × absent sub-count on a base view), the smallest gap, the at-risk list (< 2^-24) and the [2^-24, 2^-23) list, printed and written to the manifest; with no reference, no flip count is printed (§5, E2-II). Like G15, a census from another arm or run is never carried over |

**Tests (fixtures, CPU, or seconds of GPU; no real block, no sealed file).**
- **T-G1:** in a subprocess, importing `gpu_env` then torch gives deterministic mode on and the
  workspace variable in effect; importing torch first makes `gpu_env` refuse.
- **T-G2:** every entry point refuses `real`, `real|sh:0`, `real|pc:0`, `real|leak`,
  `world:R:0|pc:0` and a malformed key.
- **T-G3:** the refusal digest changes when the key order, the key set, `starts` or the rank order
  changes, and not when `row_chunk` changes (which is recorded); a digest mismatch refuses.
- **T-G4 (the comparator separates both worlds; revision 1.2):** on the pinned records, an
  injected Δp of 1.01 × s(p) on one cell that reorders no pair of S(f) passes E2 and is printed as
  a diagnostic (Δp is not a criterion); a λ changed on one fit fails E1; a label flipped fails E1;
  a `D` moved just beyond its E3 bound fails E3 and one moved just within it passes; the
  denominators of the counts per cell read from the pinned store are 37, 164, 4,299 and 13,500;
  the unmodified records pass all three.
- **T-G9 (an injected flip is caught; revision 1.2):** (i) in a D1-scope shuffle with an exact
  tie, one member of a tied present × absent pair is moved by one float64 step (`np.nextafter`)
  in the GPU copy: E2-II counts as many flipped pairs as that cell had ties in S(f), names each,
  and refuses; (ii) in a tie-free fit, the `p` of a present and an absent cell adjacent in order
  are exchanged: an opposite order is counted and named; (iii) in one of the 9 base views of D1's
  scope whose ties are all same-label pairs (M20 data, §12, P7), one member of such a tie is moved
  by one float64 step: the AUC is unchanged, and E2-II still counts and names the flip (the
  all-pairs set of a base view); (iv) a move that changes no order state gives 0 flips and passes.
  The census function run over the whole pinned store reproduces M20: 27,123 records with a tie,
  782,376 ties, 1 record below 2^-24 (`world:M0.85:0|sh:10||ko||rule`), 438 below 1e-5 of which
  32 tie-free; in D1's scope 0 at risk.
- **T-G10 (an at-risk fit with a changed AUC is refused; revision 1.2):** from a pinned D1-scope
  fit, a reference copy is made at risk by setting a present cell to an absent cell's `p` plus
  3e-8 (smallest gap 3e-8 < 2^-24); a GPU copy equal to it passes and lists the fit as at risk; a
  GPU copy with that present cell at the absent cell's `p` minus 3e-8 changes the AUC by
  1 / (n_pos·n_neg) and is refused, with E2-III's message naming the fit (E1 and E2-II also fire);
  a reference copy with smallest gap 6.0e-8 is not listed as at risk and is listed in the
  [2^-24, 2^-23) band.
- **T-G5 (poisoned block):** with the block cells of `harness.REAL` flipped in the main process and
  every worker, the per-fit hashes of one world's base view and 5 shuffles are unchanged (seconds
  of GPU; V7 repeats it on 99 shuffles).
- **T-G6:** the stamp check refuses a mocked torch version and a mocked DLL hash.
- **T-G7:** two subprocess runs of one world's base view and 5 shuffles give equal hashes (seconds
  of GPU).
- **T-G8:** the arm's path check (G12) passes a BF record with λ, labels and AUC equal and no
  flipped pair (its \|Δp\| printed), and fails one with a flipped pair or with another λ; rule
  #2.1 stays exact (revision 1.2; revision 1.1 tested "within E2a").

## 11. Error ledger (A §12 form; A's working rules apply)

Line numbers carry their commit; README and code lines are at `cdbde9e`. "Where the body and the
ledger disagree, the ledger's 'correct' is right" (A §12).

| item | was | correct | where the wrong wording lived | what refuted it | caught by |
|---|---|---|---|---|---|
| G-(1) | "The code here re-implements only `harness.bf_als`'s ALS/Newton optimisation" | it also re-implements `fit_bf`'s λ choice: the inner held-out log-likelihood (on the GPU in v3), its sum over folds and the tie rule (on the host in v2 and v3), and in the rule port `fit_existence`'s λ choice | `README.md:10–12` | `gpu_bf3.py:117–122` (`_heldout_ll`), `:174–195` (`fit_bf_all`); `gpu_bf2.py:147–158` (`choose_lambda`, `inner_ll`); `gpu_rule.py:65–97` | this draft |
| G-(2) | "All scripts set one BLAS thread per process before numpy loads" | the v2/v3 drivers and `prep` do (`run_pipeline.py:25–26`, `validate_shuffles.py:18–19`, `validate_rule.py:16–17`, `prep.py:16–17`); the v1 scripts import numpy with no preamble (`validate.py:15`, `validate_vs_cpu.py:22`, `validate_batched.py:14`), and `harness.py`'s `setdefault` (:33–34) runs after numpy is loaded, too late for OpenBLAS | `README.md:122` | the files and lines named (scope: the eight `.py` files of the directory) | this draft |
| G-(4) | "v2 and v3 disagree on 2 of 180 base fits" | **≥ 3; no direct comparison was made.** The "2" was a set difference (v3's five minus v2's three, the v2 set being a subset of the v3 set, M18), not a v2↔v3 comparison of `p`. The at-least-3 are M1.0:0 and M0.85:2 (bit-equal in v2, not in v3) and M1.0:4 (not bit-equal in either; max \|Δp\| 5.54e-8 in v2, 3.16e-8 in v3, so the two `p` differ); M0.75:0 and M0.85:0 cannot be told apart without the per-fit `p`, which neither run saved | chat only (Zcode's; he accepts it as his, 10:54 UTC) | `validation_shuffles_base45.json` (row `world:M1.0:4\|\|ko\|\|BF:1`, 5.540526e-08); `run7_pipeline_all45.log:95` (3.156e-08) | this draft |
| G-(5) | "Δp = one float32 ulp (5.63e-8 ≈ 2^-24)" | **5.63e-8 is the observed maximum; 2^-24 = 5.96e-8 is the ulp bound (the float32 spacing) at p ≥ 0.5, smaller at smaller p (§5: revision 1.1's E2a; since revision 1.2 a printed diagnostic, and 2^-24 the at-risk threshold of E2-III); `p` is stored as float64**, computed from float32-cast parameters (`harness.py:273–277`, `decoders/bf_decode.py:10–12`). The observed 5.63e-8 is larger than one float32 step of the logit at any cell of its fit (§5, drafter's caution) | chat only (Zcode's; he accepts it as his, 10:54 UTC) | `run7_pipeline_all45.log:11` (5.6323528e-08); arithmetic | this draft |
| G-(6) | the pre-run store is "stale"; "`harness.fit_n1` … already disagrees with that file's stored N1 predictions" | the store reproduces bit for bit; the claim came from a wrong key and cell order (A §12, row CC (1)) | `validate_vs_cpu.py:1–13` at `74de040` and `cdbde9e`, never corrected | A §3.3, facts (a) and (c) (A lines 650–669 at `74db080`); `README.md:377–385` | this draft |
| G-(7) | "Every bank is built through `knockout_regrow.build_bank(key, terms, synthetic_only=True)`" | true of the v2/v3 code; the v1 scripts call `make_world` directly, outside `build_bank`'s refusal (they build world specs only) | `README.md:16–17` | `validate.py:50`, `validate_batched.py:43`, `validate_vs_cpu.py:54` | this draft |
| G-(8) | "All 45 worlds' shuffles: 2,030 s on the GPU" (rule #2.1) | 2,030 s is the wall time of the GPU path; the GPU `bf_als` is 1,142 s of it, the ridge steps on the CPU in the GPU process 530 s, prep 157 s, the rest of the rule's fit 110 s | `README.md:59` | `run8_rule_sh_all45.log:1–45` (per-world stage times, summed) | this draft |

**Clarification notes (not ledger rows).** A's rule for the table requires both addresses to be
artefacts, or "chat only" for a wording that lived only in the chat; "a session message or a tool
call is not a place" (A §12, lines 2392–2395 at `74db080`). Following A's precedent of recording
such cases beside the ledger rather than in it (A §12, line 2379), three cases are recorded here:

- **Former row G-(3) (revision 1), moved here in revision 1.1.** Revision 1's row read the wrong
  wording "the GPU scripts have no thread preamble — add" as Zcode's (chat, 09:32 UTC). Zcode's
  chat line was "preamble + a record of the actual environment (the GPU scripts have no record of
  the environment — add)": the claim was about the environment record, and it is correct. The
  v2/v3 drivers and `prep` have the preamble (`run_pipeline.py:25–26`, `prep.py:16–17`, row
  G-(2)); no GPU script records the environment in effect (they record `gpu_name`, `workers` and
  `row_chunk` only, `run_pipeline.py:184–186`, `validate_shuffles.py:130–133`). The "no preamble"
  reading came from CC's relay in the drafting brief, not from Zcode's text; the brief is a session
  message, not an artefact, so the case is not a ledger row. Zcode's point stands as G1–G2.
- **E3's formula as relayed (revision 1.1).** The drafting brief for revision 1.1 relayed E3 as
  |ΔD| ≤ max|Δp| / min_i p_i(1 − p_i). `D` is a difference of two means, so the bound needs a
  factor 2 (§5, E3, reconciliation); the registered formula carries it. The wording lived in the
  brief, a session message, so it is recorded here and not as a row.
- **Ark's census number, clarified by Zcode (revision 1.2; chat only).** Ark's census (11:15 UTC)
  gave 31 records with a small smallest gap; Zcode (11:25 UTC) gave **438 records with smallest
  gap < 1e-5**. Both reproduce (M20): 438 is every record whose smallest gap is below 1e-5; 31 is
  the narrow set, **tie-free records with smallest gap in [5.96e-8, 1e-5)** (32 tie-free records
  below 1e-5, the 31 plus the one below 2^-24). Neither number was wrong under its own definition,
  and neither entered an artefact before this revision, so it is a clarification, not a ledger
  row; §5 and M20 state the narrow definition beside each number.

## 12. Runs made while drafting, and what was not verified

**Runs made (all read-only on the repository and the data folders; outputs in the drafter's
scratchpad only).**
- **P1, environment probe** (the torch venv, about 20 s): versions of §1.3; with
  `CUBLAS_WORKSPACE_CONFIG=:4096:8` and `torch.use_deterministic_algorithms(True)`,
  `torch.linalg.solve` on float64 batches of shape (3000, 65, r, r) for r = 1 and 4, index
  assignment `U[idx] = …`, boolean gather, `torch.where`, batched matmul and `amax` ran without
  error, on random tensors. This is not a run of the engine: an operation of the engine not in
  this list may still raise (V0 decides). "Tool only".
- **P2, reads** of every file in `gpu_instrument/` and in the probe folder.
- **P3, counts over the flyvis-65 run's synthetic store** (`tools/.venv`, read-only): M11–M13,
  M15.
- **P4,** `sha256sum -c SHA256SUMS.txt` in the pinned pre-run folder: five of five OK.
- **P5, E3's bounds** from the pinned pre-run store's `p` (read-only).
- **P6, revision 1.1 (CPU reads only, `tools/.venv`, 11:04–11:30 UTC; no fit, no GPU):** the
  (rank × λ × view) breakdown of the 18,000 rows of `validation_pipeline_all45.json` and the same
  four denominators from the pinned store's `lam` (M18); the v2 set as a subset of the v3 set
  (`validation_shuffles_base45.json`); E1's fields over the 18,000 rows; the probe's `run1`,
  `run3`, `run4` hashes; E2a's float32 spacing check and E3's per-fit bounds on the pinned `p`
  (§5), with the count of cells where `logit_of` or `CLIP` clips (0 of 11,520 on the 180 base BF
  fits for both); `gpu_util.prep` from the summary; the pinned store's sha256 against its
  `SHA256SUMS.txt` line (equal).
- **P7, revision 1.2 (CPU reads only, `tools/.venv`, 11:32 UTC onward; no fit, no GPU):** the
  smallest gap between distinct values of every numeric column of the pinned
  `synthetic_worlds.csv` over its 270 rows, and the per-row lattice of `auc_other_59` (M19); the
  census of all 28,665 records of the pinned `raw_fits.json.gz` (exact ties and smallest gap per
  record, over the present × absent pairs by the record's own `y`, over all 2,016 pairs, and, to
  check Zcode's remark, over "the first 32 against the last 32"), by family, over D1's scope and
  on M3's five (M20, §5); the lines of `knockout_regrow.py` at `74db080` through which `p` reaches
  the exact columns (§5). Outputs in the drafter's scratchpad only.

**Not verified.**
- That the determinism settings leave the engine's bits unchanged, or its speed (V0).
- Which of the places of §1.2 moves M3's five fits; the "flat objective" reading (V5).
- The rule #2.1 check of README:211–219 (no artefact).
- How `run4_all45batch.txt` was produced (no script, no header line); it is historical evidence
  without provenance until V4 (d) re-shoots it.
- Whether `row_chunk` moves any hash at full scale (V4 (c)); run1 against run3 moved no chunk
  boundary.
- Which cell carries each of the five fits' largest |Δp| (since revision 1.2 a diagnostic, not a
  criterion; V2 prints it). Whether they can flip a pair is decided from the reference (§5, M20:
  they cannot).
- The near-tie counts of M15 (the inner log-likelihoods are not saved).
- **0 flipped pairs on A** is derived (bit-equal fits, and the five's gaps against their Δp, §5),
  not counted: no per-cell GPU `p` was saved. V2 counts it.
- Ark's candidate mechanism for why no tie flipped on A (both members of a pair go through the
  same reduction); on A no tie sat on a differing fit, so the files cannot test it (V8 may).
- That a same-label flip on a base view moves `p_P` or `p_P_rowcol` on some fit: read from the
  code (`auc_null`, §5), not produced on a fit; T-G9 (iii) checks only that the census sees it.
- The chat messages of 11:00–11:25 UTC (Mike, Ark, Zcode): quoted as relayed in the drafting
  brief for revision 1.2.
- Whether V4's other compositions keep E1.
- The GPU rate on the male placed grid and on block B's worlds.
- The chat messages of 09:13–09:32 UTC: quoted as relayed in the drafting brief; the chat is not in
  the repository.
- The male arm's registration was committed as revision 1.1 (`a6761e2`) while this draft was being
  written; its §7.1 and D13 were read at that commit, the rest at `f82d442`.

## 13. Sources

- A: `docs/plans/2026-09-24-knockout-regrow-registration.md` at `74db080` (§3.3 lines 612–869, §7
  lines 1462–1714, §12 ledger rules 2369–2418).
- The male CNS arm: `docs/plans/2026-09-26-knockout-regrow-male-cns-arm-registration.md` at
  `a6761e2`, revision 1.1 (§7.1 lines 809–830; D13 line 977); S1, S5, S14 of its §7.2.
- Block B: `docs/plans/2026-09-25-knockout-regrow-block-b-registration.md` at `8591491` (§7 lines
  566–569; D12 line 645).
- `results/genome/c6/harness.py` (pinned) and `results/genome/c6/checks/knockout_regrow.py` at
  `74db080`.
- `results/genome/c6/gpu_instrument/` at `cdbde9e`, including the two ignored dumps in the working
  directory.
- `connectome-seed-data/knockout_regrow/flyvis65_20260925T171656Z_74de0401a21f.stdout.log`, its
  folder's `raw_fits.json.gz`, and `synthetic_rev3_prerun/`.
- `C:\Users\mikha\AppData\Local\Temp\gpu_probe\` (`probe_once.py`, `run1.txt`–`run3.txt`,
  `run4_all45batch.txt`, `a.txt`, `b.txt`).
- `docs/briefs/2026-09-25-next-session-handover.md` (the VRAM note).

## 14. Changelog

- **Revision 1, 2026-09-26 UTC:** first draft, by a CC subagent, on the brief relayed by CC after
  Mike's words of 09:13 UTC and the reviewers' notes of 09:14–09:32 UTC.
- **Revision 1.1, 2026-09-26 UTC (edits begun 11:04 UTC):** the reviewers' edits of 10:52–10:54
  UTC (§15): E2 split into E2a (a per-cell float32-spacing bound) and E2b (a diagnostic count per
  (rank × λ × view) cell, denominators from the reference store); E3 propagated per differing fit
  with the factor 2 of a difference of two means; A3 on what the probe's self-stability covers,
  `row_chunk` recorded outside the refusal digest and V4 (c) made required, V4 (d) added; D7's
  stamp registered from V1; ledger rows G-(4), G-(5) rewritten and G-(3) moved to a clarification
  note; near-ties per arm (G15); the prep phase's idle GPU in §9; M18 added. By a CC subagent.
- **Revision 1.2, 2026-09-26 UTC (edits begun 11:32 UTC):** the decision of 11:15–11:25 UTC
  (§15, review of revision 1.1): E2a and E2b withdrawn; E2 is the tie census (E2-I = E1, E2-II the
  census with 0 flipped pairs, E2-III the at-risk fits), Δp and s(p) printed diagnostics; the
  census pair set, the flipped-pair definition, the scope (GPU-made fits only) and what a run
  with no reference can state (§5); M19 (the CSV lattice) and M20 (the census of A) added; D3, D9
  (b), §6, V2, V5, V6, V8, Totals, Order, §9, G9, G12, G16, T-G4, T-G8, T-G9, T-G10 updated; §11
  clarification of Ark's census number; §12 P7. No run's cost changes. By a CC subagent.

## 15. Reviews (DPC Research chat, 2026-09-26 UTC)

### 15.1 Review of revision 1 (10:52–10:54 UTC)

Revision 1.2 withdrew E2a and E2b (§15.2); the rows below record revision 1.1 as it was made.

**Votes.**

| reviewer | time (UTC) | vote | what it rests on |
|---|---|---|---|
| Ark | 10:52 | yes, with edits | A1, A2, A3, the D7 stamp, the C items (below). Ark reproduced from the files: v3 175 / 180 base fits bit-equal, the 5 others all `…||ko||BF:1` (M1.0:0 λ 1, M1.0:4 λ 3, M0.75:0 λ 3, M0.85:0 λ 1, M0.85:2 λ 3), max \|Δp\| 5.6323528063728645e-08; v2 177 / 180 (M1.0:4 5.5405e-8, M0.75:0 1.6313e-8, M0.85:0 2.9370e-8), a subset of the v3 set; E1 on all 18,000: 0 λ, 0 label differences, max AUC difference 0.0; shuffles 17,820 / 17,820 |
| Zcode | 10:54 | yes, with edits | accepts A1–A3 and the D9 form; accepts ledger G-(4) and G-(5) as his own errors, with the forms now in §11; on G-(3), his chat line was about the environment record (§11, clarification notes) |
| Johnny | — | **no vote** | his session hit its context limit at 10:49 UTC |
| Mike | — | not given | **Mike decides whether to wait for a third vote** |

Every number of Ark's reproduction was recomputed from the same files at drafting (§12, P6) and
agrees, to the digits given.

**Edits.** "Differs" says where this revision departs from the edit as it was relayed to the
drafter, and why.

| edit | asked by | applied in | differs |
|---|---|---|---|
| **A1**: E2 is not a count and not a rate; E2a, the universal per-cell criterion; E2b, a diagnostic count per (rank × λ × view) cell with fixed denominators | Ark; Zcode agrees | M18 (§2); D3 (§4); §5 E2, E2a check table, drafter's caution, Outcomes; D9 (b); V2, V5, V6 (§7); §9; G9, T-G4, T-G8 (§10) | The breakdown reproduces exactly (37 / 5, 164 / 0, 4,299 / 0, 13,500 / 0). Revision 1's "0 of 17,820 shuffles, refuse on one" was a count too and is dropped: a shuffle within E2a passes and is counted. E2a cannot be decided on the five observed fits from the files (no per-cell GPU `p`); §5 gives the cells where each could pass. The drafter adds a caution: s(p) is tighter than one float32 step of the logit at 16–33 of 64 cells per fit, and 5.63e-8 is more than one such step at any cell of M0.85:2 |
| **E2b's denominator source** | Ark (A1) | §5 E2b | From the λ of the reference store the comparison reads (A's pinned store: 37, 164, 4,299, 13,500), fixed and hashed before the GPU stage; never the GPU run's own λ. In a hybrid arm with no CPU BF store there is no E2 at all (R5 judges it); with a CPU store of its worlds (V8), that store is the source |
| **A2**: E3 not A's `MACHINE_CHECK_TOL`; a per-fit propagated bound, printed per differing fit; clipped cells switched off | Ark; Zcode agrees | §5 E3 (formula, clip rule, logloss analogue, per-fit table, reconciliation); G9 | **Factor 2 added**: `D` is a mean over present cells minus a mean over absent ones, so \|ΔD\| ≤ 2δ / q_min, with q_min taken at the endpoints p_i ± δ to make the bound exact rather than first-order. Ark's per-fit numbers reproduce exactly, but his form bounds the largest single-cell logit change, not `D` (on M1.0:4 it is below the tighter bound at the same δ). logloss: \|Δ\| ≤ δ / m_min, no factor 2 (one mean). Revision 1's numbers (6.2e-7 to 8.7e-7) reproduce and were not wrong, so no ledger row; the formula as relayed is a clarification note (§11) |
| **A3**: the probe's self-stability was measured with the flags off; V1 compares the differing set under D6 with the flag-free state; chunk size recorded, not in the refusal digest; composition and order stay in it; `run4` without provenance until V4 re-shoots it with a header | Ark; Zcode agrees | §3.2; §3.3; D5, D6 (§4); R4 (§6); V1, V4 (c), V4 (d), Totals, Order (§7); G3, T-G3 (§10); §12 | `row_chunk` is outside the refusal digest as asked, but **run1 against run3 moved no chunk boundary** (150 inner problems fit in one chunk at both sizes, §3.2), while run4, a larger batch, did move hashes. So V4 (c), a full-scale run at another `row_chunk`, is made **required** (+37 min of GPU: totals 2 h 50 min, break-even 1.7 arms), and `row_chunk` returns to the digest if it moves a hash. R5 still catches a `row_chunk` change between an arm's pre-run and its run |
| **D7**: V1's stamp is the registered stamp; a later run must equal it, not merely its own pre-run | Ark; Zcode agrees | D7 (§4); R1 (§6); V1, Order (§7); G2 (§10) | none |
| **G-(3)** | Zcode (his chat line); CC's brief | §11, clarification notes (the row is removed from the table) | Moved to a note, as the brief allowed: A's rule requires artefact addresses or "chat only", and the wrong wording lived in CC's brief, a session message |
| **G-(4)**: "≥ 3; no direct comparison was made" | Zcode (accepts as his) | §11 row G-(4); §3.1 item 4 | none |
| **G-(5)**: 5.63e-8 observed maximum; 2^-24 the ulp bound at p ≥ 0.5, smaller at smaller p; p stored as float64 | Zcode (accepts as his) | §11 row G-(5); §3.2 root cause | Adds a pointer to §5's finding that 5.63e-8 is more than one step of the logit at any cell |
| **C**: near-ties are one arm's count; recount and print per arm, never transfer | Ark | M15 (§2); G15 (§10); §12 | The counts cannot be recounted from a file (the inner log-likelihoods are not saved); G15 makes every run print its own |
| **C**: in §9, prep leaves the GPU idle for about 138 s at the start of the hybrid | Ark | M10 (§2); §9, "What is not claimed" (4) | **The measured utilisation is 0.0037 %, not 0.37 %**: `util` is in percent (`pipeline_all45_nvsmi.csv`), and the prep window's 271 samples hold one sample of 1 % (mean 0.00369, median 0) |
| **C**: Ark confirms 158,851.5 CPU-s ÷ 29.87 = 5,319 s; end_to_end_wall 2,362.3 s; ×2.25 | Ark | no change (M9, M11) | Ark's labels M15 / M16 are the draft's M11 and M9. 158,851.5 ÷ 29.87 = 5,318.1 (5,317.9 with the unrounded 29.871), so **5,318 s, as M11 has it, not 5,319**; 2,362.3 s and ×2.25 agree |
| **D9 form** | Zcode accepts | D9 (b) now names E2a | none |

### 15.2 Review of revision 1.1 (11:00–11:25 UTC)

**Votes.**

| reviewer | time (UTC) | vote | what it rests on |
|---|---|---|---|
| Ark | 11:15 | **rejects options (a), (b) and (c) for E2a; E2 replaced by a tie census** | his measurements (scripts in his sandbox, `gpu_e2_check.py`, `gpu_e2_census.py`): the CSV lattice (M19), the census of the pinned store (M20), M3's five tie-free with gaps ≥ 6.31e-5, `block‖N1` constant; the census to be repeated on the male worlds (V8); acknowledges that his "0.37 %" and "5,319 ✓" are corrected in revision 1.1 (below) |
| Zcode | 11:25 | **the same** | the census defined by the record's own `y` (interleaved, not "first 32 / last 32"); 438 records with smallest gap < 1e-5, not 31 (§11, clarification); next smallest gap after the at-risk record 9.08e-8 |
| Johnny | — | **out** | Mike, 11:00 UTC: Johnny is out. The two votes stand; Johnny reads revision 1.2 in a new session |
| Mike | — | not given | the registration still needs his word |

The options (a), (b) and (c) for E2a are cited as relayed in the drafting brief; their wording
is not in the repository. Every number of Ark's and Zcode's messages was recomputed from the
pinned files at drafting (§12, P7); the matches and the one mismatch are in the edits table.

**Edits.** "Differs" says where this revision departs from the decision as it was relayed to the
drafter, and why.

| edit | asked by | applied in | differs |
|---|---|---|---|
| **E2 replaced by the tie census**: E2-I (= E1), E2-II (census, 0 flipped pairs required, each flip named), E2-III (at risk below 2^-24, identical AUC required); E1 and E3 (factor 2) kept | Ark, Zcode | D3 (§4); §5 E1 heading, E2, Outcomes; D9 (b); V2, V5, V6 (§7); §9 | **Drafter's additions, for the reviewers:** (1) on a base view the pair set is all 2,016 pairs, not only present × absent: `p_P` and `p_P_rowcol` rank p over all 64 cells against permuted labels (`auc_null`, `knockout_regrow.py:513–536`), so a same-label pair that changes order can move them; E2-III on a base view also requires identical `p_P`, `p_P_rowcol`. On A this adds nothing at risk (smallest all-pairs gap of a D1 base view 1.59e-6). (2) The fits with smallest gap in [2^-24, 2^-23) are printed, not judged: two cells moving oppositely by up to 2^-24 each close 2^-23 (4 D1 fits on A, all bit-equal). (3) Against a reference E2-III is contained in E1; its role is the named list. (4) The store's one at-risk record held on the rule port (engine v2, M7), not on the registered engine; D1's scope has 0 at-risk fits |
| **The flipped-tie definition** | the decision (to be defined) | §5, E2-II | Named "flipped pair": a pair tied on one side and ordered on the other, or ordered oppositely, compared exactly on the decoded float64 `p`; the count is over pairs, so flips never cancel in it |
| **What the census says with no CPU reference** | the decision | §5 E2-II; §6 (printed line); G16 | ties, gaps and the at-risk list only; flips need a reference (V2, V8); R5 makes an arm's run's census equal to its pre-run's |
| **The census repeated on the male worlds (V8), during that arm's pre-run, before unsealing; the mechanism unverified** | Ark | §5; V8, Totals, Order (§7); §12 | V8 separates "by construction" from "luck" only if a male fit that differs from its CPU reference carries ties; on A no differing fit had a tie (every one of the 423,777 ties of D1's scope sits on a bit-equal fit), so V8 prints that count. V8 decides nothing for the male arm; a flip or an at-risk AUC difference there refuses this instrument, a statement about the GPU instrument, not an input to a male gate (the male D13 (iii)) |
| **Ceilings** | the decision (state it) | §5, scope | The census is not applied to the ceilings (`full‖*`, `block‖*`, `\|pc:`) in D1 (a): they are CPU fits in the hybrid too and cannot flip. It applies if a revision ports them (D1 (b)) |
| **Item 1, the lattice** | Ark | M19 (§2); §5 | Every number reproduces. Two additions: `auc_other_59` is in `CSV_EXACT_COLUMNS` and each row sits on its own lattice 1/(2ab), a + b = 59 (step ≥ 5.7e-4); its 1.6e-5 is a gap between rows of different lattices, not "continuous". `logloss_margin_over_N1` (5.5e-5, continuous) was missing from the list. "The only path is a flipped tie in `auc`" holds for the shuffles, not for a base view's `p_P` (row above) |
| **Items 2–4, 6, the census** | Ark; Zcode (438, 9.08e-8) | M20 (§2); §5 | Every number reproduces (5 × 0 ties; gaps 6.31e-5, 1.06e-3, 9.46e-5, 1.26e-4, 2.97e-4; 27,123; 782,376; one record at 1.836e-8, tie-free; next 9.08e-8; 438; 31 + 1; `block‖N1` 45 × 1,024 / 1,024; `world:R:0\|\|full\|\|N1` 10 ties, 35 values). **One mismatch:** "the `\|pc:` family (full‖rule) carries 46,080 ties over 270 fits" — 46,080 over 270 fits is the block-mask family (`block‖BF` 180 + `block‖N1` 45 + `block‖rule` 45), all of it from `block‖N1`. The `\|pc:` family holds 7,828 ties in 502 of its 900 fits (smallest gap 2.04e-7). Also: the pairs per fit are n_pos·n_neg, 1,024 only at 32 / 32 (A's shuffles: 540 to 1,024) |
| **Item 5, the census by the record's own `y`** | Zcode | §5 definitions | Confirmed: "first 32 / last 32" gives 18,162 records with a tie, 592,591 ties, none below 2^-24 and 421 below 1e-5 |
| **438 against 31** | Zcode | §11, clarification note | Both reproduce under their definitions; recorded with the narrow definition, not as a ledger row |
| **Ark's acknowledgement (11:15 UTC)** of the "0.37 %" and "5,319 ✓" corrections | Ark | no change (§15.1, rows C; M10, M11) | none: 0.0037 % and 5,318 s stand as revision 1.1 has them |
| **Tests** | the decision | T-G4 (rewritten), T-G8, T-G9 (an injected flip is caught), T-G10 (an at-risk fit with a changed AUC is refused); G9, G12, G16 (§10) | T-G9 (iii) adds a same-label flip on a base view (the drafter's addition above) |
| **§9 totals** | the decision (if a run changes) | §7 Totals | No run changes: the census reads saved `p` in seconds and makes no fit; 2 h 50 min, V8 80 min and the break-even stand |
