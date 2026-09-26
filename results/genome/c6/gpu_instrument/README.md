**Status (2026-09-26): not reviewed. A separate instrument; the registered knockout-and-regrow run does not use it.**

# GPU instrument for BF_r and rule #2.1 fits (knockout-and-regrow synthetic worlds)

**This is a separate instrument, not a rewrite of the registered CPU one.** Mike's rule: "GPU is
a separate instrument, not a rewrite of the CPU one." Nothing under `results/genome/c6/` outside
this directory was modified. This directory imports `harness.py`, `checks/knockout_regrow.py` and
(through `harness.load_rule`) `rules/second_rule_v21/fit.py` read-only. It uses them for bank and
world construction, the N1 ridge fits, `harness.ridge_logistic`, and the decoders. Those are
called exactly as the CPU instrument calls them, not reimplemented. The code here re-implements
only `harness.bf_als`'s ALS/Newton optimisation, as batched float64 PyTorch/CUDA computations
across many fits at once.

It has never read, fit or scored the real block. It has never run `knockout_regrow.py` as a
script: the real and `--synthetic-only` arms live under `if __name__ == "__main__":` and are
never imported. It has never opened `raw_fits_real.json.gz`. Every bank is built through
`knockout_regrow.build_bank(key, terms, synthetic_only=True)`, which refuses a `real` key, and
the workers here refuse one too. The only read of the real bank is
`knockout_regrow.degree_terms()`, which fits N1 on the real bank's **knockout** view, with block
cells excluded. That fit is the synthetic worlds' own construction step (registration section
3.6), not a real-arm computation.

Ported so far:

- the BF family (`harness.fit_bf`, ranks 1-4), on the worlds' knockout views and on their 99
  shuffled banks;
- rule #2.1's existence fit (`fit_existence` in `second_rule_v21/fit.py`), described below. The
  rest of rule #2.1's fit is not ported. It runs as the rule's own CPU code.

## Summary (2026-09-26)

The comparison is against the registered run's store of synthetic fits, through the harness's
own decode:
`connectome-seed-data/knockout_regrow/flyvis65_20260925T171656Z_74de0401a21f/raw_fits.json.gz`.

- **BF_1..BF_4 on all 45 worlds x 99 shuffled banks (17,820 fits):**
  - **17,820 / 17,820 are bit-equal in p.** Every λ matches, and so do every label and every AUC.
    This held in two independent runs (engines v2 and v3).
- **BF_1..BF_4 on the 45 worlds' own knockout views (180 fits):**
  - 175 / 180 are bit-equal.
  - The other 5 are BF_1 fits that differ by at most 5.6e-8 in p. Their λ, labels and AUC are
    identical.
  - These are the same five seeds that v1 flagged against a live `harness.fit_bf`.
- **Rule #2.1 with the GPU existence fit, 45 knockout views:**
  - 42 / 45 are bit-equal in p, and their four scores are identical.
  - The other 3 differ by at most 4.9e-8 in p (explained below).
- **Rule #2.1 on one world's 99 shuffles:** 99 / 99 are bit-equal, with the scores identical.
- **Rule #2.1 on all 45 worlds x 99 shuffles (4,455 fits):** 4,455 / 4,455 are bit-equal, with
  the four scores identical.
- **Wall time for all 45 worlds x 99 shuffles x BF_1..BF_4, plus the 45 base views (18,000
  fits):**
  - The GPU pipeline (v3), end to end: **2,362 s (39 min)**.
  - The registered CPU pool's equivalent for the same fits: about **5,313 s (89 min)**. That is
    about 2.2x slower than the GPU pipeline.
  - Wall time for one world's 99 shuffles x 4 ranks: 56 s on the GPU, about 119 s on the CPU
    pool.
- **Rule #2.1:** the GPU and the CPU pool are about equal.
  - One world's 99 shuffles: 41 s on the GPU, about 45 s on the CPU pool.
  - All 45 worlds' shuffles: 2,030 s on the GPU, about 1,986 s on the CPU pool.

## Files

- `prep.py`: CPU-side preparation, used in a process pool. It never imports torch.
  - `prepare_key` / `prepare_key_compact` build a synthetic bank with `knockout_regrow.build_bank`
    and take its knockout view. From the view they compute:
    - N1 on the view and on its 10 inner-fold training views (`harness.fit_n1`);
    - the logit grids, training grids and held-out masks.
    These are the same calls, in the same order, as `harness.fit_bf`.
  - `prepare_key_compact` also computes bf_als's SVD start, once per grid (see engine v3).
  - `decode_compare` decodes BF fits with the harness's own decode and compares them with the
    stored entries.
  - `rule_post_key` runs rule #2.1's own `fit()` with a precomputed existence fit, then decodes
    and scores the result as `knockout_regrow._w_group` does.
- `gpu_bf2.py` (engine v2): `bf_als_problems` solves many independent `bf_als` problems in one
  batch:
  - every batch row points at its problem's grid, so the grids are not repeated;
  - λ is set per row;
  - the Newton loop compacts its active set per row: only rows that have not met
    `_newton_rows`'s break are computed. v1 computed every row and froze the converged ones.
  - the Hessian is one batched matmul.
  `gpu_fit_bf_prepared` reproduces `fit_bf` over many prepared views.
- `gpu_bf3.py` (engine v3, the streamed pipeline):
  - all grids of all banks are uploaded to the GPU once;
  - the SVD starts come from the preparation step;
  - M, Y and the held-out masks are stored as bool;
  - the inner held-out log-likelihood is computed on the GPU, so ranks run back to back with no
    per-bank host loop.
- `gpu_rule.py`: rule #2.1's existence fit, batched (see below).
- `run_pipeline.py`: the v3 driver:
  1. prepare every bank first, in a pool of 24 workers;
  2. stream BF_1..BF_4 over all banks on the GPU;
  3. decode and compare in the same pool, overlapping the next rank's GPU work.
  It samples `nvidia-smi` every 500 ms and system RAM every second.
- `validate_shuffles.py`: the v2 driver. It works one world at a time, or on the base views with
  `--base`.
- `validate_rule.py`: validates the rule #2.1 port, on the base views (`--base`) or on the
  shuffles.
- Results:
  - `validation_pipeline_all45.json` (v3, 18,000 rows) and `pipeline_all45_nvsmi.csv` (its GPU
    samples);
  - `validation_shuffles_all45.json` (v2, 17,820 rows);
  - `validation_shuffles_base45.json`, `validation_shuffles_one_world_R0.json`,
    `validation_pipeline_one_world_R0.json`;
  - `validation_rule_base45.json`, `validation_rule_sh_R0.json`,
    `validation_rule_sh_all45.json`;
  - the logs `run6_shuffles_all45.log`, `run7_pipeline_all45.log` and `run8_rule_sh_all45.log`.
- v1 files (`gpu_bf.py`, `validate*.py` of 2026-09-25): unchanged, described in the last section.

## How to run

The environment is the same as for v1 (section "v1: Environment" below).

```
cd results/genome/c6/gpu_instrument
PY="c:/Users/mikha/Documents/dpc-research/autoresearch-win-rtx/.venv/Scripts/python.exe"
$PY run_pipeline.py --worlds all --n-sh 99 --base --workers 24 --tag all45      # BF, v3
$PY validate_shuffles.py --worlds all --n-sh 99 --workers 8 --tag all45         # BF, v2
$PY validate_rule.py --worlds all --base --workers 24 --tag base45              # rule #2.1
$PY validate_rule.py --worlds all --n-sh 99 --workers 24 --worlds-per-batch 1 --tag sh_all45
```

All scripts set one BLAS thread per process before numpy loads, as `knockout_regrow.py` does.
They also call `knockout_regrow._w_init(10, degree_terms(), True)`, as the registered run's
workers do, so `harness.STARTS = 10`.

## Validation against the registered store (2026-09-26)

**Reference.** The comparison uses
`flyvis65_20260925T171656Z_74de0401a21f/raw_fits.json.gz`, the registered run's 28,665
synthetic fits. It is read-only, and its real-arm file is never opened. The keys are
`world:<family>:<j>[|sh:<sd>]||ko||<predictor>`, with p in `BLOCK_CELLS` order.

**Method.** The GPU fit goes through `knockout_regrow._pred(pk).decode(data, BLOCK_CELLS)`, so the
float32 cast of the fitted parameters is applied as in the stored p. Before any compare, each
bank's stored y is checked against the y of the bank rebuilt here: 0 mismatches in every run
below.

**Columns.** "Bit-equal" means `np.array_equal(p_gpu, p_ref)` on all 64 cells. "Labels" counts
cells where `p >= 0.5` differs, out of 64 x fits. AUC is `knockout_regrow.auc`.

### BF_1..BF_4, shuffled banks: 45 worlds x 99 shuffles (`|sh:0..98`), knockout view

| run | fits | λ mismatches | p bit-equal | max &#124;Δp&#124; | max &#124;ΔAUC&#124; | labels |
|---|---|---|---|---|---|---|
| v2, `validate_shuffles.py`, one world per batch | 17,820 | 0 | **17,820** | 0 | 0 | 0 / 1,140,480 |
| v3, `run_pipeline.py`, all banks at once | 17,820 | 0 | **17,820** | 0 | 0 | 0 / 1,140,480 |

Per rank, both runs have 4,455 / 4,455 bit-equal and 0 λ mismatches.

**How much the λ check tests.** Most shuffled banks select λ = 100. The reference has 4,291,
4,416, 4,446 and 4,450 at λ = 100 for BF_1..BF_4. The remaining 164, 39, 9 and 5 select λ = 3.
So the final fit is often near N1. The λ choice itself depends on all 50 inner (fold x λ) fits of
every bank, and it matches on all 17,820.

**Near-ties.** v3 counts banks where some λ's inner log-likelihood lies within 1e-7 of the tie
threshold (best - 1e-9), where float64 noise could in principle flip the choice. There are about
1,600-1,700 such banks per rank, mostly λ = 30 vs λ = 100, where both fits collapse to about N1.
None of them flipped.

### BF_1..BF_4, the 45 worlds' own knockout views

| run | fits | λ mismatches | p bit-equal | max &#124;Δp&#124; | max &#124;ΔAUC&#124; | labels |
|---|---|---|---|---|---|---|
| v2 (`validate_shuffles.py --base`) | 180 | 0 | 177 | 5.5e-08 | 0 | 0 / 11,520 |
| v3 (in the all-45 pipeline run) | 180 | 0 | 175 | 5.6e-08 | 0 | 0 / 11,520 |

All differences are BF_1 fits. In v3 they are M1.0:0, M1.0:4, M0.75:0, M0.85:0 and M0.85:2,
seeds 90150, 90154, 90170, 90180 and 90182. These are exactly the five BF_1 fits that v1's
file-free check found differing from a live `harness.fit_bf`. v2 shows three of the five.

On these fits, float64 rounding differences in the GPU's summation order leave U, V a few 1e-8
away from the CPU's. This survives the float32 cast in decode. The cause is not traced further.
No shuffled bank shows it.

## Rule #2.1 (second_rule_v21): what is ported, and its validation

**What its fit does.** See `fit.py`: 95-147, 358-399.

1. `fit_existence` chooses λ by the nested inner-fold scheme of BF_r (10 folds x 5 λ). Inside
   every inner fit and in the final fit, it runs `fit_uvw`: ROUNDS = 3 rounds of two steps.
   - (i) `harness.bf_als` at rank 1, with offset O + W[G, G] and k = 10 starts;
   - (ii) the 16 entries of W, by `harness.ridge_logistic` on the group-pair indicators, with
     offset O + u·v and penalty MU.
2. Then come quantisation (`ExistQ`), coordinate descent over the symbols, the refit of c, the
   offset library with N_EB-style sides (`fit_offsets`), counts and signs.

**Cost.** Step (i) is about 3 x 51 `bf_als` calls per fit, which is three times BF_1's count.
It is the expensive part.

**It can be batched, and it is.** `gpu_rule.batched_fit_existence` handles each round like this:
- one GPU batch of every (view x fold x λ) problem's `bf_als` (`gpu_bf2.bf_als_problems`, rank 1);
- then the exact `harness.ridge_logistic` call per problem on the CPU (16 parameters, cheap);
- the inner log-likelihood and the λ rule with the same expressions as `fit_existence`.

**Everything after `fit_existence` is the rule's own code**, run unchanged in pool workers
(`prep.rule_post_key`). The mechanism:
- A worker loads the rule with `harness.load_rule`, as the registered workers do.
- `prep.install_existence` rebinds the name `fit_existence` in that process's module object to a
  function. The function returns the GPU result only for the exact view it was computed on:
  same cells, same exists, starts = 10, default rounds and `x_on`. Anything else raises.
- `fit.py` on disk is not touched.
- The rule's `fit()` then runs, is decoded by its `decode.py` through `Predictor.decode`, and is
  scored by `harness.score`.

| set | fits | λ mismatches | p bit-equal | four scores identical | max &#124;Δp&#124; | labels |
|---|---|---|---|---|---|---|
| 45 worlds, knockout view | 45 | 0 | 42 | 42 | 4.9e-08 | 0 / 2,880 |
| world R:0, 99 shuffles | 99 | 0 | 99 | 99 | 0 | 0 / 6,336 |
| all 45 worlds x 99 shuffles | 4,455 | 0 | **4,455** | 4,455 | 0 | 0 / 285,120 |

**The three base fits that differ** are M0.75:1, M0.85:3 and M0.75:3, all at λ = 3. Checked by
running the CPU `fit_existence` on the same views:
- λ is the same;
- the GPU's u differs from the CPU's by at most 3.2e-7;
- all quantised symbols (a, b, u, v, W) are identical;
- the float32 scale `s_uv` (and on M0.75:3 also `s_w`) differs by one float32 step. That moves p
  by about 5e-8.
- the offset, counts and sign scores are identical;
- existence (the log-loss score) differs in the 8th digit.

So these are rounding differences carried through the float32 scale, not different fits.

**Cost structure** for one world's 99 shuffles (`validation_rule_sh_R0.json`):

| stage | time |
|---|---|
| prep | 4.5 s |
| existence fit on the GPU (`bf_als`) | 25.2 s |
| ridge steps, CPU, in the GPU-driving process | 6.9 s |
| rest of the fit, 24 workers | 2.9 s |
| **total** | **41.1 s** |

The CPU pool's equivalent is about 45.5 s: 1,361 CPU-s over 29.9 workers. The rule port still
runs on engine v2, one world per batch. Moving it onto v3 (streaming, starts from the preparation
step) and the ridge steps into the pool is the obvious next step. It is not done.

## Timing (2026-09-26)

### The CPU reference

The registered run's log does not print seconds per fit. The store records `secs` for every fit,
measured inside a worker while all 30 workers ran. On this machine, an AMD Ryzen 9 9950X with
16 cores and 32 threads, the store's `secs` sum to 234,369 CPU-s over the 7,846 s synthetic stage
(log line 60). That is an effective parallelism of 29.9, so the pool was full throughout.

Below, "CPU pool equivalent" means the store's `secs` for the same fits divided by 29.9. It
estimates the wall time that part of the registered run occupied. It is not a separate measured
run. Mean seconds per fit on the shuffled banks: BF_1 4.47, BF_2 8.39, BF_3 10.25, BF_4 12.18,
rule #2.1 13.33, N1 0.04.

### BF_1..BF_4, same machine, same fits

| work | GPU path | wall | CPU pool equivalent |
|---|---|---|---|
| 1 world x 99 shuffles x 4 ranks (R:0) | v2 (8 prep workers) | 70 s (prep 7.4, GPU 60.8) | 119 s (3,562 CPU-s) |
| 1 world x 99 shuffles x 4 ranks (R:0) | v3 (24 prep workers) | **56 s** (prep 3.9, GPU 50.1, decode tail 0.02) | 119 s |
| 45 worlds x 99 shuffles x 4 ranks | v2, one world per batch | 2,879 s (prep 254, GPU 2,620) | 5,256 s (157,164 CPU-s) |
| 45 x 99 shuffles + 45 base views, x 4 ranks (18,000 fits) | **v3** | **2,362 s** | **5,313 s** (158,852 CPU-s) |
| 45 base views x 4 ranks | v2 | 28 s GPU (prep 2.3) | 56 s (1,688 CPU-s) |
| 45 base views x 4 ranks | v1 (2026-09-25) | 119 s GPU | 56 s |

### Rule #2.1, same machine, same fits

| work | GPU path | wall | CPU pool equivalent |
|---|---|---|---|
| 45 base views | `validate_rule.py --base`, 24 workers | 17.8 s | 19 s (566 CPU-s) |
| 1 world x 99 shuffles (R:0) | `validate_rule.py` | 41.1 s | 45.5 s (1,361 CPU-s) |
| 45 worlds x 99 shuffles | `validate_rule.py`, one world per batch | 2,030 s | 1,986 s (59,379 CPU-s) |

**v3's all-45 run, by phase:**

| phase | wall | GPU utilization (500 ms samples) |
|---|---|---|
| setup | 2.2 s | |
| prep of 4,500 banks, 24 workers | 138 s | 0 % |
| upload | 0.8 s | |
| GPU: BF_1 | 287 s | |
| GPU: BF_2 | 627 s | |
| GPU: BF_3 | 645 s | |
| GPU: BF_4 | 662 s | |
| GPU total | 2,221 s | mean 98.4 %, median 99 %, ≥ 90 % in 99.8 % of samples, < 20 % in 0.07 % |
| decode and compare left after the GPU finished | 0.2 s | |

The decode and compare overlapped the GPU entirely.

**v3's all-45 run, memory:**
- the prepared arrays are 2.2 GB;
- the system's used RAM peaked 6.1 GB above its level at start (the main process's peak working
  set was 5.4 GB);
- torch's peak VRAM allocation was 12.5 GB;
- `nvidia-smi` peaked at 18.2 GB used, which includes about 3 GB used by other processes.

**Before and after the pipeline change**, per world, for BF only:
- v2 (`validate_shuffles.py`) ran one world at a time: prep (5-8 s, GPU idle), then four ranks
  with a host loop between them, then decode and compare in the GPU-driving process. That is
  about 64 s per world, 58 s of it on the GPU.
- v3 prepares everything first. GPU work then comes to 49.4 s per world: 2,221 s / 45, which
  includes the 45 base views. The GPU is at about 98 % for the whole GPU phase.

The GPU phase is now compute-bound:
- Row chunks of 100,000 instead of 40,000 gave the same 49.5 s per world, at 26.5 GB VRAM.
- The remaining time is the float64 Newton/ALS arithmetic itself. float32 was not tried.

**The honest comparison.** For the BF family on the synthetic worlds, the GPU pipeline takes
39 min where the registered CPU pool took about 89 min, about 2.2x faster. It does this while
using one GPU and, for 2.3 min of preparation, 24 CPU workers. For rule #2.1, the GPU port and
the CPU pool are about equal.

The whole registered synthetic stage took 7,846 s. 67 % of its CPU-seconds went to BF on the
shuffles and 25 % to rule #2.1 on the shuffles. The GPU does not remove the need for the CPU
pool. It could take the BF share off it.

## What is not covered (2026-09-26)

- **The real block.** It is never read, per the hard limit.
- **The rest of the registered pipeline.** This covers the permuted-block ceilings (`|pc:`), the
  full/block ceilings, the fixed-λ diagnostic, N1 and the 9,999 permutations. They were not
  ported or timed here. The ceilings are `bf_als` fits on other masks and would batch the same
  way.
- **Rule #2.1 beyond its existence fit.** Quantisation, descent and the offset library run as
  the rule's own CPU code, by design.
- **float32.** Not attempted.
- **Review.** None of this has been reviewed.

# Engine v1 (2026-09-25), as written then

The statements in this section about what is not ported or not yet validated (rule #2.1, the
shuffled banks) are superseded by the sections above. The rest is unchanged.


## v1: Files

- `gpu_bf.py` — the instrument. `gpu_fit_bf(view, r)` reproduces one `harness.fit_bf` call
  (batched over `lambda x start` within that one fit; matches the CPU function to float64
  precision). `gpu_fit_bf_many(views, r)` is the actual point of the instrument: it fits BF_r on
  a whole list of views (e.g. all 45 synthetic worlds) in **two GPU calls total** — one batched
  call across every `(view x fold x lambda x start)` combination for the nested lambda choice,
  and one batched call (grouped by each view's chosen lambda) across every `(view x start)` for
  the final fit — instead of looping per world in Python.
- `validate.py` — validates `gpu_fit_bf` (single-fit batching) against the saved CPU reference,
  `connectome-seed-data/knockout_regrow/synthetic_rev3_prerun/raw_fits.json.gz`.
- `validate_vs_cpu.py` — validates `gpu_fit_bf` directly against `harness.fit_bf` called live, in
  the same process, on the same in-memory view (no reference file involved).
- `validate_batched.py` — validates `gpu_fit_bf_many` (cross-fit batching) against the same
  reference file, for all 45 worlds x BF_1..BF_4, and times the batched run. **This is the
  validation table below.**

## v1: Environment

Did not modify `tools/.venv` (pinned) and did not create a new venv. Used the existing
**`c:/Users/mikha/Documents/dpc-research/autoresearch-win-rtx/.venv`**, which already has:

- Python 3.10 (`cpython-3.10-windows-x86_64`, uv-managed)
- `torch==2.9.1+cu128`, CUDA available, tested on an RTX PRO 4500 (Blackwell)
- `numpy==2.2.6` — **the same version as `tools/.venv`**, which matters: the numpy-side code
  (SVD initialisation, the N1 ridge fit, `default_rng`/`PCG64` draws for world construction and
  ALS start perturbations) must reproduce the CPU harness bit-for-bit, and numpy version drift
  is a real risk for that.

All GPU tensor computation uses **float64** throughout (`DTYPE = torch.float64` in `gpu_bf.py`);
float32 was not attempted, since float64 was fast enough and the task's default is float64 unless
float32 is separately shown to match.

## v1: How to run

```
cd results/genome/c6/gpu_instrument
"c:/Users/mikha/Documents/dpc-research/autoresearch-win-rtx/.venv/Scripts/python.exe" validate_batched.py
```

This builds the 45 synthetic worlds (via `knockout_regrow.world_specs()`/`make_world()`, same
seeds as the CPU instrument), fits BF_1..BF_4 on the knockout arm with `gpu_fit_bf_many`, and
diffs against the CPU reference file. Writes `validation_batched_results.json`.

## v1: Validation

**Ground truth:** `connectome-seed-data/knockout_regrow/synthetic_rev3_prerun/raw_fits.json.gz`
(the CPU harness's saved knockout-arm ('ko') BF fits for the 45 synthetic worlds). This file
**does reproduce bit-exactly** on this machine — confirmed both by comparing it directly to a
fresh `harness.fit_bf` call, and by the GPU numbers below. (An earlier pass of this validation
wrongly concluded the file was stale; that was two bugs in the comparison script — a wrong key
(family index instead of within-family index) and a row-major vs `BLOCK_CELLS`-order mismatch on
the 64 block cells, both now fixed.) `validate_vs_cpu.py` gives an independent, file-free check
of the same claim: GPU vs a `harness.fit_bf` call made in the same process, same view, no
serialization involved — also exact.

### Cross-fit batched run: all 45 worlds x BF_1..BF_4, two GPU calls per rank

| family | n (worlds) | max &#124;ΔAUC&#124; | max &#124;Δp&#124; | label mismatches | λ mismatches |
|---|---|---|---|---|---|
| R     | 20 (5 worlds x 4 ranks) | 0 | 3.0e-08 | 0 / 1280 | 0 |
| Nf    | 20 | 0 | 1.0e-08 | 0 / 1280 | 0 |
| No    | 20 | 0 | 2.5e-08 | 0 / 1280 | 0 |
| W     | 20 | 0 | 7.9e-08 | 0 / 1280 | 0 |
| M0.5  | 20 | 0 | 1.2e-08 | 0 / 1280 | 0 |
| M0.6  | 20 | 0 | 1.7e-08 | 0 / 1280 | 0 |
| M0.75 | 20 | 0 | 2.6e-08 | 0 / 1280 | 0 |
| M0.85 | 20 | 0 | 4.4e-08 | 0 / 1280 | 0 |
| M1.0  | 20 | 0 | 6.0e-08 | 0 / 1280 | 0 |
| **all** | **180** | **0** | **7.9e-08** | **0 / 11520** | **0 / 180** |

Every one of the 180 (world, rank) fits selected the identical λ. The ~1e-8 in the max |Δp|
column is **not** GPU rounding: it comes from `p_exist_on_block_cells`, which evaluates the
logits from the float64 `bf_U`/`bf_V`, while the harness's `decode` first passes the fitted data
through `harness.cast` (a float32 round-trip) and the reference was written through `decode`.
Checked by CC, 2026-09-25: the GPU fits of `world:W:0` and `world:R:1`, BF_1 and BF_2, passed
through the harness's own `decode(data, BLOCK_CELLS)` match the reference with max |Δp| = **0**
(the accessor gives 1.8e-8 to 4.1e-8 on the same fits). The file-free `validate_vs_cpu.py` check
(GPU vs live `harness.fit_bf`, same accessor on both sides, `run3.log`, 180/180) agrees to 3e-16
on 175 fits. Five BF_1 fits differ by more, 1.4e-9 to 3.8e-8: M1.0 seeds 90150 and 90154, M0.75
seed 90170, M0.85 seeds 90180 and 90182. On those five, λ, AUC and labels are still identical.
So the GPU fit is **not** bit-identical to the CPU fit in every case: at float64 it can land a
few 1e-8 away. This has not been traced to its cause. Any comparison
against the reference should go through the harness's `decode`, not through this accessor.
Full row-level data: `validation_batched_results.json`.

### Timing

Batched (this instrument, `validate_batched.py`, `gpu_fit_bf_many`): **119.1 s** total for all 45
worlds x 4 ranks (BF_1: 18.5s, BF_2: 29.8s, BF_3: 33.3s, BF_4: 37.5s — 4 GPU dispatches for
fold-selection + 4 for the final fit, covering all 180 (world, rank) fits).

Unbatched, single-fit-at-a-time, same GPU, same process (`validate_vs_cpu.py`, `gpu_fit_bf`
called once per world per rank in a Python loop): about 1.1-2.4 s/fit when the GPU was otherwise
idle, growing to 6-21 s/fit under contention from the batched run executing concurrently. This is
the "batching within one fit only" version and is not the number to compare against — see next
line.

Unbatched **CPU** (`harness.fit_bf`, live, this machine, single-threaded, average over 67
completed (world, rank) pairs while contending for CPU cores with the concurrent GPU/numpy setup
work): **4.06 s/fit** average, projecting to roughly **12 minutes** for all 180 (world, rank)
combinations run serially on this machine. Against the cross-fit-batched GPU's 119 s, that is
roughly a **6x** wall-clock reduction for the same 180 fits, on one machine, with the CPU number
itself somewhat inflated by contention (an uncontended CPU number would likely be a bit faster,
and correspondingly the true speedup a bit lower than 6x as measured, but not qualitatively
different). **Against the parallel CPU harness the batched GPU is not yet faster:** the
registered CPU run uses 30 workers, and 180 fits at ~4 s each over 30 workers is about 25 s of
wall time, against the GPU's 119 s. The case for batching rests on the shuffled banks (the bulk of
the 28,665 fits), which are not yet batched or timed here. This is **not** the registration's ~85-minute/45-worlds figure, which covers the
*full* registered pipeline (99 shuffles, 9999 permutations, two ceilings, N1, rule #2.1, per
predictor) on 30 parallel workers — this instrument covers only the BF-family knockout-arm fits,
which are the part the registration's section 7 identifies as the batching-relevant cost
(`bf_als` at r=4: 23.8 ms/call at starts=1, 183.8 ms at starts=10, "mostly numpy dispatch on
small matrices").

## v1: What went wrong on the way here (kept for whoever touches this next)

1. **Iterating past Newton convergence is not safe to batch naively.** The first version of the
   batched Newton solver ran a fixed number of iterations per call instead of reproducing
   `harness._newton_rows`'s per-fit early-stop break. Rows with few training cells (e.g. T5a/T5c,
   4 training sources) give a near-singular per-row Hessian; iterating past convergence on those
   amplifies floating-point noise into a random walk to a different local optimum of the
   non-convex ALS objective, producing AUC differences up to 0.4 on some worlds even though the
   selected lambda still matched. Fixed by adding per-batch-item convergence masking (freeze an
   item once its max row-gradient norm < `BF_TOL`, exactly reproducing the CPU's `break`) — see
   `batched_newton_rows` in `gpu_bf.py`.
2. **The reference file is valid ground truth; an early check of it was wrong.** Comparing
   `gpu_fit_bf`'s output to `raw_fits.json.gz` using the wrong dictionary key (family index
   instead of within-family index `spec["j"]`) and the wrong cell ordering (row-major instead of
   `knockout_regrow.BLOCK_CELLS` order) produced large, spurious disagreements, including on
   `harness.fit_n1` alone (a deterministic fit with no randomness or ALS). This looked like
   evidence the file was stale; it was a bug in the comparison script, not the file. Both are
   fixed in `validate.py`; `p_exist_on_block_cells` in `gpu_bf.py` is the correctly-ordered
   accessor to use against this file.

## v1: What is not covered here

- Rule #2.1 — different algorithm, not ported.
- The real block — never read, per the task's hard limit.
- The full registered pipeline (shuffles, permutations, ceilings) — this instrument only
  reproduces the BF-family fit itself, on the knockout arm, on synthetic worlds.
- Shuffled-bank fits (the `|sh:` keys in `raw_fits.json.gz`) — not yet validated against this
  instrument.
