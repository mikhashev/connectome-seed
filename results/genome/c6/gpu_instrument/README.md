**Status (2026-09-25): not reviewed. A separate instrument; the registered knockout-and-regrow run does not use it.**

# GPU instrument for BF_r fits (knockout-and-regrow synthetic worlds)

**This is a separate instrument, not a rewrite of the registered CPU one.** Mike's rule: "GPU is
a separate instrument, not a rewrite of the CPU one." Nothing under `results/genome/c6/` outside
this directory was modified. This directory imports `harness.py` and `checks/knockout_regrow.py`
read-only, for data/world construction and for the N1 ridge fit (cheap, unbatched, called exactly
as the CPU instrument computes it, not reimplemented). It re-implements only the expensive part —
`harness.bf_als`'s ALS/Newton optimisation over `(fold x lambda x start)`, and, going further,
over many fits at once (many worlds and/or folds in one batch) — as PyTorch/CUDA tensor
computations. It has never read, fit or scored the real block, and it has never run
`knockout_regrow.py` as a script (its real and `--synthetic-only` arms live under
`if __name__ == "__main__":`, never imported). The only real-bank read anywhere in this directory
is `knockout_regrow.degree_terms()`, which fits N1 on the real bank's **knockout** view (block
cells excluded) — that is the synthetic worlds' own construction step, defined by the
registration (`docs/plans/2026-09-24-knockout-regrow-registration.md`, section 3.6), not a
real-arm computation.

Only the BF family (`harness.bf_als`/`fit_bf`, ranks 1-4) is ported. Rule #2.1
(`second_rule_v21`) is a different, non-ALS algorithm and is **not ported**; the registration's
own cost discussion (section 7) is specifically about `bf_als`'s numpy-dispatch overhead on many
small matrices, which is what batching addresses.

## Files

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

## Environment

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

## How to run

```
cd results/genome/c6/gpu_instrument
"c:/Users/mikha/Documents/dpc-research/autoresearch-win-rtx/.venv/Scripts/python.exe" validate_batched.py
```

This builds the 45 synthetic worlds (via `knockout_regrow.world_specs()`/`make_world()`, same
seeds as the CPU instrument), fits BF_1..BF_4 on the knockout arm with `gpu_fit_bf_many`, and
diffs against the CPU reference file. Writes `validation_batched_results.json`.

## Validation

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

## What went wrong on the way here (kept for whoever touches this next)

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

## What is not covered here

- Rule #2.1 — different algorithm, not ported.
- The real block — never read, per the task's hard limit.
- The full registered pipeline (shuffles, permutations, ceilings) — this instrument only
  reproduces the BF-family fit itself, on the knockout arm, on synthetic worlds.
- Shuffled-bank fits (the `|sh:` keys in `raw_fits.json.gz`) — not yet validated against this
  instrument.
