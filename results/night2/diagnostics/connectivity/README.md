# Linear mode connectivity between saved flyvis end states — commands, interpreter, outputs

**Date:** 2026-09-15 · **Run by:** CC (subagent), on Mike's word (DPC Research chat 2026-09-15
07:43 «do now what can be done before tonight's run») · **Design fixed by:** Ark 06:52 and
Zcode 07:05, written in `docs/next-session-plan.md` §4 (bullet "Linear mode connectivity",
sub-bullet "Design"); background `docs/experiments/002-night2-seeds-1-and-2.md` §5b and §5c
items 5–6.

Nothing here trains, commits, or writes into `connectome-seed-data`. The four runs'
directories were listed (path + size + mtime of all 396 files under
`results/flow/9991/{000,900,001,002}`) before the first command and after the last —
`diff` empty ("NO CHANGE to run dirs"). `flow/9991/002_killed_by_reboot` was not read or
touched. Checkpoints are read with `torch.load` only.

## Interpreter

```
C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/.venv/Scripts/python.exe
```
Python 3.10.20, torch 2.9.1+cu128, flyvis 1.2.0, GPU `NVIDIA RTX PRO 4500 Blackwell`
(`META` line of every run; also `run_meta_*.json`). `FLYVIS_ROOT_DIR` and
`CUBLAS_WORKSPACE_CONFIG` are set inside `connectivity.py:29-33`, the same way and in the
same place as `night/run_individual.py:46-49` and `diag1_eval_paths.py:30-33`, so no
environment variable has to be exported first.

Shorthands used below:

```
PY=".../63f3961a-.../scratchpad/flyvis-probe/.venv/Scripts/python.exe"
OUT="C:/Users/mikha/Documents/dpc-research/connectome-seed/results/night2/diagnostics/connectivity"
ND="C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/03852100-01fd-45ef-82c3-e22ac607b0f7/scratchpad/conn/netdir"
```

## Commands, verbatim, in the order they were run

```bash
# snapshot of the run dirs before anything (repeated after the last command; diff empty)
cd /c/Users/mikha/Documents/dpc-research/connectome-seed-data/results/flow/9991 \
  && find 000 900 001 002 -type f -printf "%p %s %T@\n" | sort > .../conn/before.txt

# smoke test of the two controls, to a SCRATCH out-dir (not this directory)
"$PY" "$OUT/connectivity.py" --task run --out-dir ".../conn/smoke" --netdir-root "$ND" \
  --paths self_0_to_0 --alphas 0,0.5,1 --variants 1,2

# investigation of the variant-2 endpoint offset (scratch script, NOT in this directory:
#   .../conn/investigate_bn.py; see "Variant 2 endpoint offset" below)
"$PY" ".../conn/investigate_bn.py" ".../conn"

# main grid: 4 paths x 2 variants x 21 alphas (0, 0.05, ..., 1.0) = 168 points, 107.8 s
"$PY" "$OUT/connectivity.py" --task run --out-dir "$OUT" --netdir-root "$ND" \
  --paths main_0_to_0prime,control_0_to_1,self_0_to_0,extra_0prime_to_1 --variants 1,2

# refinement, primary path: the 20 half-way points 0.025, 0.075, ..., 0.975 (includes the
# mandated 0.5 +/- 0.025), 40 points, 32.7 s
"$PY" "$OUT/connectivity.py" --task run --out-dir "$OUT" --netdir-root "$ND" \
  --paths main_0_to_0prime --variants 1,2 \
  --alphas 0.025,0.075,0.125,0.175,0.225,0.275,0.325,0.375,0.425,0.475,0.525,0.575,0.625,0.675,0.725,0.775,0.825,0.875,0.925,0.975

# refinement, other three paths: the mandated 0.5 +/- 0.025 only, 12 points, 6.5 s
"$PY" "$OUT/connectivity.py" --task run --out-dir "$OUT" --netdir-root "$ND" \
  --paths control_0_to_1,self_0_to_0,extra_0prime_to_1 --variants 1,2 --alphas 0.475,0.525

# csv + json
"$PY" "$OUT/connectivity.py" --task summarize --out-dir "$OUT"

# snapshot after
cd /c/Users/mikha/Documents/dpc-research/connectome-seed-data/results/flow/9991 \
  && find 000 900 001 002 -type f -printf "%p %s %T@\n" | sort > .../conn/after.txt \
  && diff .../conn/before.txt .../conn/after.txt
```

**Run time:** 107.8 + 32.7 + 6.5 = **147.0 s of measurement** for 220 evaluated points
(each point = one BatchNorm recompute for variant 2, one `hook_eval`, one `per_item_eval`),
plus ~25 s of solver/dataset construction per process. Per point: variant 1 0.35–0.95 s,
variant 2 0.55–1.30 s.

## What was interpolated

Endpoints are `results/flow/9991/{000,900,001,002}/chkpts/chkpt_00071` = solver iteration
250,008 (`chkpt_iter.h5` stores 250,007, `flyvis/solver.py:453,463` vs
`night/run_individual.py:498` — the mapping used by `chkpt_table()` in both diagnostic
scripts). `000` = seed 0, `900` = seed 0′, `001` = seed 1, `002` = seed 2.

θ(α) = (1−α)·θ_A + α·θ_B over the **8,161 trainable parameters**, computed in float64 and
cast back to float32 (`connectivity.py:112-123`). Key sets are asserted against the
checkpoint, not assumed (`connectivity.py:96-108`):

* core trainable 734 = `nodes_bias` 65 + `nodes_time_const` 65 + `edges_syn_strength` 604
* decoder trainable 7,427 = `base.0.weight` 6800 + `base.0.bias` 8 + `base.1.weight` 8 +
  `base.1.bias` 8 + `decoder.0.weight` 600 + `decoder.0.bias` 3
* core fixed 2,959 (`edges_sign`, `edges_syn_count`) — **asserted bit-identical between the
  two endpoints** and copied through (`connectivity.py:137-139`)
* the 17 BatchNorm buffers `base.1.running_mean` 8 / `running_var` 8 /
  `num_batches_tracked` 1 — interpolated in **variant 1** (the integer
  `num_batches_tracked` in float64, rounded to nearest), recomputed in **variant 2**

At α = 0 and α = 1 the interpolated trainable tensors are asserted bit-equal to the
endpoint's own (`connectivity.py:146-155`).

**Variant 3 (buffers from one end) was not run**, per the design.

## The BatchNorm recompute (variant 2) — the choices made

`connectivity.py:180-249`. Four things the design left to be decided; each is stated here
with the file:line it was decided against.

1. **Sampler and number of batches.** flyvis's own training loader is
   `DataLoader(dataset, batch_size=4, sampler=SubsetRandomSampler(train_seq_index),
   drop_last=True)` (`flyvis/task/tasks.py:85-90`): a random order that drops 3 of the 51
   training items per epoch and draws from an unseeded global RNG. A random, partial pass
   would make the recompute stochastic and put noise into the self-path control, so the
   recompute uses **`IndexSampler(train_seq_index)`** — the sampler flyvis itself uses for
   the validation loader (`flyvis/task/tasks.py:104-107`) — with **batch_size 4,
   drop_last=False**: **13 batches** (12 of 4 items + 1 of 3), **all 51 training items
   exactly once**, fixed order. Training split = the 17 scenes / 51 items of
   `docs/preregistration-cheap-vs-expensive.md` §3 ("Held-out split, printed 2026-09-13").
   Printed by the script as
   `BN_LOADER {"n_train_items": 51, "batch_size": 4, "n_batches": 13,
   "sampler": "IndexSampler", "drop_last": false}`.
2. **Augmentation OFF** (`dataset.augmentation(False)`). flyvis trains under
   `augmentation(True)` (`flyvis/solver.py:294`), and those augmentations draw from
   **unseeded global RNGs** (`flyvis/datasets/augmentation/hex.py:103-104, 205-206, 320,
   386`). Measured cost of the alternative: three augmentation-ON recomputes of the same
   seed-0 end state gave −2.1205 / −0.5839 / −1.0570 against the stored `val_loss`, a
   spread of **1.54 between draws** — noise of the same order as the quantities being
   compared, and it would destroy the self-path control.
3. **`momentum = None`** (cumulative average over batches), reset first with
   `bn.reset_running_stats()`, as the design specifies. Control: the same 13-batch pass
   with flyvis's default `momentum = 0.1` gives **+18.12** against stored, because a
   13-step EMA from the reset values (0, 1) has not left its initialisation. Because
   momentum None weights **batches**, not items, the 3-item last batch counts like a
   4-item batch; this is deterministic and identical at every α, so it is a property of
   the estimator, not a per-point artefact.
4. **`t_pre = 0.5` for the steady state** — the TRAINING value
   (`config.get("t_pre_train", 0.5)`, `flyvis/solver.py:300`), not `test()`'s 0.25
   (`flyvis/solver.py:479`), because this forward pass is the training-side one. Control:
   the same pass at t_pre = 0.25 gives −5.7526 against stored, further away than −3.3996.
   The final 3-item batch needs its own steady state (flyvis builds one per batch size,
   `flyvis/network/network.py:548-586`), so two are computed per point.

During the recompute the modules are in **train** mode (`solver._train()`) under
`torch.no_grad()`; the evaluation afterwards runs in eval mode through the hook path.

## Variant 2 endpoint offset — investigated before the grid was reported

The design requires the endpoints to reproduce the stored checkpoint `val_loss` to ≲ 1e-3,
"if it exceeds 0.5 on the aggregate, say so and investigate the recompute before
proceeding". Variant 1 reproduces to ≤ 7e-5 (table below). **Variant 2 does not**: it lands
−3.3996 (seed 0), −1.5498 (seed 0′), −0.6592 (seed 1) below the stored values. Investigated
with the scratch script `.../conn/investigate_bn.py`; findings:

* The stored buffers carry `num_batches_tracked = 250008`, i.e. they are flyvis's default
  **EMA with momentum 0.1 over 250,008 augmented training batches** — effectively the last
  ~10 augmented batches of 4 sequences. The recompute is the **mean over a clean full pass
  of all 51 training items**. These are two different estimators of the same statistic; a
  gap is expected, not a defect.
* The recomputed values are close to the stored ones in the buffers themselves. Seed 0,
  `running_mean` recomputed `[-0.595, -0.542, 0.021, 0.207, -0.923, -0.506, -0.815,
  -0.626]` vs stored `[-0.607, -0.578, -0.003, 0.154, -0.887, -0.519, -0.749, -0.626]`;
  `running_var` recomputed `[0.143, 0.163, 0.205, 0.110, 0.291, 0.154, 0.236, 0.182]` vs
  stored `[0.160, 0.188, 0.184, 0.124, 0.280, 0.162, 0.231, 0.200]`.
* Turning augmentation on moves the offset to −2.12 / −0.58 / −1.06 over three draws (mean
  ≈ −1.25, spread 1.54), i.e. roughly two thirds of the −3.40 is the augmentation
  difference and the rest is full-pass-average vs short-EMA. Neither is a broken recompute.

**Decision, stated rather than hidden:** the design's own definition of the barrier is
`max along the path − max(endpoints)` **within one variant**, and the recompute is applied
identically at every α (the self-path proves it: flat to 1.2e-4). The offset is therefore a
constant of the estimator and does not enter the barrier. The grid was run as designed, with
the offset reported. No parameter of the recompute was tuned to shrink it.

## Resolution — the design's own criterion is NOT met, stated plainly

The design asks for a resolution "so a barrier of order 12.7 on the aggregate cannot hide
between points", and for the largest inter-point change to be stated. Largest |Δ loss|
between adjacent grid points, after refinement:

| path | variant | n points | max \|inter-point change\| |
|---|---|---|---|
| main (0 → 0′) | 1 | 41 | 82.34 |
| main (0 → 0′) | 2 | 41 | 63.21 |
| control (0 → 1) | 1 | 23 | **1496.88** (between α = 0.80 and 0.85) |
| control (0 → 1) | 2 | 23 | 76.96 |
| self (0 → 0) | 1 | 23 | 0.00009 |
| self (0 → 0) | 2 | 23 | 0.00012 |
| extra (0′ → 1) | 1 | 23 | 57.96 |
| extra (0′ → 1) | 2 | 23 | 135.26 |

Every non-self path moves by far more than 12.7 between adjacent points, so **a feature of
size 12.7 can hide between points on all six of them**. The reported maxima and barriers are
therefore **lower bounds**: refining a grid can only raise `max`, never lower it. On the
primary path the 0.05 grid was halved to 0.025 (41 points) and the barrier was **unchanged**
— 96.5859 on variant 2 (max still at α = 0.1) and 374.0515 on variant 1 (max still at
α = 0.6), recomputed on the 21-point subset and on all 41 points. The extra 20 points found
no higher point, but the step sizes above show that is not proof there is none.

## Output files

| file | what |
|---|---|
| `connectivity.py` | the script, both sub-commands |
| `rows.jsonl` | one line per evaluated point, as written (220 lines) |
| `connectivity_profiles.csv` | path, run_a, run_b, variant, α, aggregate (hook path), aggregate (per-item mean), their difference, bn_batches, wall_s, and the 16 per-item losses |
| `connectivity_summary.json` | per path × variant: endpoint losses, stored endpoint `val_loss`, endpoint reproduction errors, max / α_max / min / α_min, max(endpoints), barrier, largest inter-point change (signed and absolute), range, the 16 per-item barriers, and the whole (α, loss) profile |
| `run_meta_*.json` | interpreter / GPU / netdir / argv / BN-loader description / wall time, one per invocation |

The CSV carries two aggregates per row: `aggregate_hook` (**the reported one** — the rung
hook of `night/run_individual.py:531-546`, reused verbatim through
`diag1_eval_paths.hook_eval`) and `aggregate_per_item_mean` (the mean of the 16 per-item
losses from `diag1_eval_paths.per_item_eval`, a copy of `flyvis/solver.py:474-556`). They
are two separate evaluations; their difference is ≤ 1.4e-3 over all 220 rows and is in the
CSV column `hook_minus_per_item_mean`. Adding the second aggregate column is an addition to
the design's CSV spec, not a substitution.

## Evaluator — reused, not re-implemented

`connectivity.py:45-52` imports `build_solver`, `chkpt_table`, `hook_eval`,
`per_item_eval`, `val_item_names` from `../diag1_eval_paths.py`. So: fresh solver in a
scratch datamate root via `datamate.set_root_context`, `recover_network` /
`recover_decoder`, `solver.test(dataloader=task.val_data, subdir="validation",
track_loss=False)` — the only form of the call that writes nothing
(`flyvis/solver.py:543-552`) — the no-op scheduler swap and the four-way RNG save/restore,
and the per-item copy of `flyvis/solver.py:474-556`. The solver's iteration is set to
250,008 and the real scheduler applied at that iteration before every evaluation
(`connectivity.py:158-168`), as `diag1_eval_paths.load_checkpoint` does. Hook path verified
equal to the stored `val_loss` to ≤ 8e-5 at every variant-1 endpoint of every path (eight
endpoint evaluations; largest deviation −7.87e-5).
