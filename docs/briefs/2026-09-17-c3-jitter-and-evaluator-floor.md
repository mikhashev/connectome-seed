# Brief — C3 measurement: trajectory jitter at 25,000 and the evaluator floor by path

**v1, 2026-09-17. Launch word given by Mike 06:16:45Z; launch only after the reviewer pass by Ark and
Zcode on this brief is in the chat.** Nothing in this brief has run on the GPU. Written by CC's
subagent; the patch is `docs/briefs/2026-09-17-c3-run_individual.patch`, **not applied**.
Aliases: `CS` = `connectome-seed`, `CSD` = `connectome-seed-data`, `FP` = the night venv root
`.../63f3961a-.../scratchpad/flyvis-probe`, `D` = `results/night2/diagnostics/diag1_eval_paths.py`,
`ABL` = `results/night2/diagnostics/ablation/ablation.py`, `RB` = `results/night2/diagnostics/rowB/rowB.py`.

## 0. Why, and the point this measurement exists to settle
"Checkpoint − hook" at C3 (seed 3: 1190.0516934 − 1192.5858383 = −2.5341; 3′: −0.2651; at the top
rung 3.2641 / 0.4391; `night3_9991-003.slim.json`, `rep_9991-903.slim.json`) was read (Ark) as a
path difference that is a property of the run. **It is not a same-state path difference.** The hook
reads the weights after 25,000 completed iterations; checkpoint 8 reads them after 25,212 (the
checkpoint fires only at an epoch end, 12 iterations/epoch, every 300 epochs; flyvis `solver.py`
train loop). At 250,000 vs 250,008 the gap is 8 iterations. The quantity mixes **trajectory
movement over 212 (or 8) steps** with **evaluation path**. This brief separates them: Part B reads
both paths on the *same* stored weights; Part A measures how much the hook value moves over
100-iteration steps around C3, and reads both paths on the same weights inside the training process.

## 1. On record already (Observed, with sources) — and two corrections
- Same-state path difference, hook path minus `per_item_eval` mean, on six runs
  (`night2/diagnostics/diag1c_per_item.json`; `night3/diagnostics/ablation/ablation_controls.json`):
  at 25,212 for 0/0′/1/2 ≤ 1.01e-05 in absolute value; at 250,008 for 0/0′/1/2/3/4 ≤ 6.2e-05. Not yet
  measured at 25,212 for 003/903 by the hook path. That is 4–5 orders below 2.53.
- Arithmetic on recorded checkpoints, context only: seed 3's checkpoint slope 21,612→25,212 is
  −0.003252/iteration, i.e. −0.689 over 212 iterations (3′: −0.861). A linear trend alone does not
  give −2.53 for seed 3 nor −0.27 for 3′; this is the question Part A answers, not an answer.
- Evaluator floors: `per_item_eval` five calls, one process, 250,008: 8.6–8.9e-05 on the 16-item
  mean (0.0 at iteration 0); hook path five calls, seed 0, 250,008: spread 2.48e-05
  (`diag1b_noise_inprocess.json`).
- **Correction (name vs number).** The "8e-08 between three processes on the state-hook path"
  (`docs/plans/2026-09-16-functional-readout-plan.md` "After night 4" (b)) is `floor_max_abs_deltaB`:
  the per-type **activity-profile** difference of row B (night 2 seed 0: 8.25e-08; night 3 seed 3:
  1.35e-08, `night3/diagnostics/rowB/rowB_controls.json`), **not a loss floor.** The 16-item loss
  of those same three processes spreads 2.29e-05 (seed 3, 250,008: 1155.7706489562988 …
  1155.7706718444824) and 3.29e-05 (night 2, seed 0). Do not carry 8e-08 into any loss rule.
- **Correction (paths).** In the code there are two evaluators, not "per_item_eval→solver.test vs
  state-hook". `ABL.eval_items(solver, None)` *is* `D.per_item_eval` (no hook registered); rowB's
  `eval_rowB` is `D.per_item_eval` plus a read-only recorder hook. The distinct second path is
  `D.hook_eval` = the rung hook (`run_individual.py:531-546`: flyvis `solver.test(track_loss=False)`
  with a no-op scheduler), which produced every night hook value. Part B therefore reads three
  callables (§2), so the "state hook registered" variant is measured, not assumed equal.

## 2. Part B — evaluator floor by path × state × repeat (read-only, runs first)
New script `CS/results/diagnostics/c3/c3_evaluator_floor.py`, committed before it runs (rule 12);
imports `D`, `ABL`, `RB` exactly as `night3/diagnostics/ablation/ablation_night3.py:35-53`; env vars
as `:30-33`; writes the sha256 of itself and of `D`, `ABL`, `RB` into every output.
- **Evaluators.** E1 = `D.hook_eval(solver)` (rung-hook path; returns the 16-item mean only — no
  per-item output exists on this path). E2 = `D.per_item_eval(solver)["flow"]` (copy of flyvis
  `test`, scheduler applied; the P0 path). E3 = `ABL.eval_items(solver, ABL.make_mask(types_arr,
  set(), device))` (E2 with the ablation state hook registered, all-ones mask = no clamp; ablation P1).
- **States.** Runs 003 and 903; checkpoint indices 0, 8, 71, loaded with `RB.load_named` (asserts
  0→0, 8→25,212, 71→250,008). Checkpoints read with `torch.load` only.
- **Repeats.** Three processes P1, P2, P3, run one after another, each with its own fresh netdir root
  `<session scratchpad>/c3_netdir_proc{p}` (`D.build_solver` asserts "scratchpad" in the path and
  **deletes** that root, `D:116-119` — never point it at anything else). In each process, for each
  (run, checkpoint): load once, then five rounds of E1, E2, E3 interleaved (15 calls). Every call
  wrapped in `RB.snapshot_state` / `RB.invariants`, asserted all seven True.
- **Recorded (all `repr(float)`, no rounding):** every 16-item mean; every per-item vector (E2, E3);
  stored `val_loss`; for each cell (run, checkpoint, evaluator): within-process all 10 pairs per
  process (30), cross-process pairs (75), max |Δ| on the mean and, for E2/E3, max per-item |Δ| and
  the same in float32 ulps of the largest per-item value (`rowB.py:365-367`); same-state path
  differences E1−E2, E1−E3, E2−E3 over all 25 call pairs per process; stored − E1 and stored − E2
  per call. Outputs `CS/results/diagnostics/c3/partB/`: `c3B_proc{1,2,3}.json`,
  `c3B_floor.json`, `c3B_means.csv` (header `# PREVIEW DIAGNOSTIC -- NOT A TEST` + `# script_sha256=`).
- **Gate (only these):** crash; NaN/inf in any value; an invariant False; **P0**: in P1, for each
  (run, checkpoint), |mean of the five E2 16-item means − stored `val_loss`| ≤ 1e-4. Single-call P0
  values are recorded, not gated. Rule 17(d): on record, single-call |P0| reached 7.68e-05 (seed 2,
  250,008, `diag1c`) against an in-process E2 spread up to 8.9e-05, so a single-call 1e-4 gate could
  stop a correct implementation; the five-call mean narrows that, but the probability cannot be
  stated from the records — reviewers decide whether 1e-4 on the five-call mean is acceptable.
- **B′ (optional, after Part A):** the same script on run 703's checkpoints 7 (21,612) and 8
  (25,212), P1 only — offline E1/E2/E3 on the weights Part A reads in-process (§5 d).

## 3. Part A — trajectory jitter at C3 (one re-run; a second optional)
- **Code:** one optional flag, `--stop-after-iter K` (§4). **`--n-iters` must stay 250000**: the lr
  schedule is `stepwise` over `stop_iter = task.n_iters` (flyvis `solver.py:995`, `:1147`; recorded
  `lr_net_at_iter` 25,000 = 4.5e-05) and the epoch count is `ceil((n_iters − iteration)/12)`;
  `--n-iters 26000` would compress the schedule tenfold and be a different training run.
- **Id and outputs.** `launch_wave.py` maps seeds to `<ENS>/<s:03d>` and replicates to `<ENS>/9<s:02d>`
  (`:95`, `:108`); it cannot produce 7xx, so run 703 is started by calling `run_individual.py` directly,
  not via `start_night.ps1`. `CSD/results/flow/9991/` holds `000 001 002 002_killed_by_reboot 003 004
  005 900 903` — 700/703 are free, and `run_individual.py:301-308` refuses if the dir exists. flyvis
  writes the new network dir `CSD/results/flow/9991/703` (checkpoints 0–8); the run json/log/progress
  go to `--out-dir CS/results/diagnostics/c3/partA/` (stem `jitter_9991-703`), not to a night dir.
- **Rungs (65):** `1000,5000,20000,20100,20200,20300,20400,20500,20600,20700,20800,20900,21000,21100,21200,21300,21400,21500,21600,21612,21700,21800,21900,22000,22100,22200,22300,22400,22500,22600,22700,22800,22900,23000,23100,23200,23300,23400,23500,23600,23700,23800,23900,24000,24100,24200,24300,24400,24500,24600,24700,24800,24900,25000,25100,25200,25212,25300,25400,25500,25600,25700,25800,25900,26000`
  = {1,000, 5,000} ∪ {20,000…26,000 step 100} (61) ∪ {21,612, 25,212}. No window flag is needed:
  `--rungs` already takes any list (`run_individual.py:156, 579, 596`). 21,612 and 25,212 are the
  completed-iteration counts of checkpoints 7 and 8: the hook there fires after the last parameter
  update of that epoch (penalty step, flyvis `solver.py:812-827`) and before the epoch-end
  `scheduler` + `checkpoint()`, which change lr only (dt is constant 0.02) — **the same weights, both
  paths, one process, no state files.** (Claimed from code order; the §5 d number is its check.)
  *Reviewer choice:* pre-window reads every 1,000 (1,000…19,000, +17 hooks) as first proposed, or
  only 1,000 and 5,000 as above — the default keeps the hook schedule before 20,000 identical to
  nights 3–4; the hook restores all RNG states, but under `--no-determinism` that equivalence cannot
  be shown by a number.
- **A0 smoke (GPU, ~1 min, ESTIMATE):** the `_StopAfterIter` path through flyvis's train loop is
  **not exercised** (only the refusal path was, on CPU). `--seed 3 --id 9983/000 --tag c3smoke
  --n-iters 250000 --rungs 24 --stop-after-iter 24 --no-determinism --out-dir <scratchpad>/c3smoke`
  (ensemble 9983 is unused). Expect `exit` "ok", `stopped_after_iter` 24, `final_iteration` 23, one
  rung, checkpoints at 0 and 12, `errors` []. Anything else → stop, no A1.
- **A1 (seed 3):** `FP\.venv\Scripts\python.exe CS\tools\night\run_individual.py --seed 3 --id
  9991/703 --n-iters 250000 --rungs <the 65 above> --tag jitter --out-dir
  CS\results\diagnostics\c3\partA --no-determinism --progress-every 100 --stop-after-iter 26000`,
  run on the committed patched file (sha256 written to `partA/SHA256.txt` before launch).
- **A2 (optional, seed 0):** identical with `--seed 0 --id 9991/700`; its pre-condition value is
  1212.5555891990662 (night 1, 000 and 900). Reviewers decide A2 on cost (§7).

## 4. The code change and how byte-identity of the default path is shown
Patch: 20 lines added, **0 deleted** (`git diff --numstat`). Added: (i) one `add_argument`
(`--stop-after-iter`, default None); (ii) `class _StopAfterIter(Exception)`; (iii) a refusal block
in `main()` guarded by `a.stop_after_iter is not None` (K must be in `--rungs`, 0 < K < n_iters, no
`--resume`; prints, returns 2, touches nothing); (iv) in `on_iteration_end`, after the rung block,
`if a.stop_after_iter is not None and k == a.stop_after_iter: raise _StopAfterIter(k)`; (v) an
`except _StopAfterIter` clause before `except BaseException` setting `exit` "ok" and
`stopped_after_iter` — reachable only through (iv). No existing line is edited.
Verification, done by the brief author on CPU (no GPU, no training): `git apply --check` against
`tools/night/run_individual.py` (sha256 `5ccd38b89a5962439a9fc0cb8d7b762d254e67b80aeffbb58f0bf4224eb55a4a`, identical to `FP/night/run_individual.py`)
passes; `parse_args()` of the original and patched file on night 4's recorded argv
(`rep_9991-903.slim.json`) gives 12 equal keys plus `stop_after_iter: None`; the refusal path with
K ∉ rungs printed the refusal, rc 2, no out-dir created. Required before A0: reviewers read the diff;
the executor applies it, re-runs the argv check, commits, records sha256.

## 5. Pre-registered readings (descriptive, not tests; fixed before the run)
Let v(k) = `rung_metrics[k].val_loss` of run 703; c(i) = `checkpoint_metrics` val_loss at iteration i.
Script `CS/results/diagnostics/c3/c3_jitter_reading.py`, committed before A1, CPU only.
- **(a) Amplitude.** OLS line of v on k over the 61 grid reads (20,000…26,000 step 100; 21,612 and
  25,212 not in the fit). Report slope, residual sd (ddof = 2), max |residual| and its k; each also
  ÷ 0.3365 (registered C3 replicate, pre-registration §4/§7) and ÷ 56.7791 (seed 3's learned gain,
  checkpoint 0 − checkpoint 250,008, `004` §3; A2 uses seed 0's 63.7481).
- **(b) Band.** B = [min, max] of v over the 11 grid reads 24,500…25,500. For night 3's
  v(25,000) = 1192.585838317871 and night 4's 1187.4011011123657: inside B (yes/no), distance to the
  nearer edge, and (value − fitted line at 25,000) ÷ residual sd. (A2: 1191.737461090088 /
  1192.0739254951477.)
- **(c) Autocorrelation.** Lag-1 Pearson correlation of the (a) residuals over the 60 consecutive
  pairs — independent jitter vs slow wander. No threshold.
- **(d) Same state, in process.** c(21,612) − v(21,612) and c(25,212) − v(25,212); and run 703's own
  c(25,212) − v(25,000) split into movement v(25,212) − v(25,000) plus path c(25,212) − v(25,212).
- **(e) Recorded only:** v(1,000), v(5,000), c at 0…25,212 beside 003 and 903; whether c(12) equals
  003's/903's bitwise (before any hook — where divergence begins).

## 6. Controls and stop conditions
- **Part A pre-condition (not a gate on jitter):** c(0) of run 703 == 1212.549735546112 bitwise
  (`repr` equality, as 003 and 903). The json is dumped at every checkpoint: read it when
  `CHECKPOINT 0` appears (progress prints 4 decimals only); on mismatch stop the process, identified
  by CommandLine, and report.
- **Run-dir listing:** before and after each part, list every file under `CSD/results/flow/9991/`
  with size and mtime; diff. B: no change at all. A0/A1/A2: no change to any pre-existing entry; the
  only additions are under `9991/703` (`9991/700`); A0's under `9983/000`. Any other change → stop.
- **Invariants:** `run_individual.py` records a failed check in `errors` but does not stop
  (`:571-573`); per rule R4 any False at any rung voids the run — reported, not read.
- `errors` [] and `nondeterministic_ops` recorded; `argv` diffed against `night3_9991-003.json`
  (expected differences: `--id`, `--tag`, `--rungs`, `--out-dir`, `--progress-file` absent,
  `--stop-after-iter`); `connectome_sha256` and `versions` equal to nights 3–4.
- GPU exclusive: `nvidia-smi --query-compute-apps=pid,process_name --format=csv` shows no compute
  process before each part; nothing starts while a training wave or any other GPU job runs.
- **Stop and report** on: crash, NaN/inf, P0 failure, pre-condition mismatch, invariant False,
  listing change, A0 not as expected. Nothing is re-run silently.

## 7. Order and cost (ESTIMATES from logs, labelled)
1. **Part B:** 3 processes × (build ~20–40 s, ESTIMATE, not measured on this path) + 3 × 90 calls
   × 0.18–0.49 s (night-3 ablation `one_evaluation_wall_s` 0.179/0.492; hook `hook_wall_s` 0.25–0.27)
   → **~2–4 min**.
2. **A0 smoke:** ~1 min (startup + 24 iterations + 2 checkpoints).
3. **A1:** nights 3/4 reached the 25,000 hook at `wall_s_since_start` 1647.5 s (003) / 1681.0 s (903);
   ×26/25 → 1713–1748 s, + 61 extra hooks × ~0.26 s ≈ 16 s, + startup → **~29–31 min per re-run.**
   (Phase-1 median is 0.0642–0.0644 s/iter, `004` §1; the overall 0.061 median includes the faster
   phase after 150,000 and underestimates the first 26,000.) Every-1,000 option: +~5 s.
4. **A2 (optional):** another ~29–31 min (seed 0 reached 25,000 at 1660.3 s).
5. **B′ (optional):** ~1 min. Total without options ≈ 35 min; with both ≈ 66 min.

## 8. Do not
1. Do not edit `run_individual.py` beyond applying this patch verbatim; do not touch
   `launch_wave.py`, `start_night.ps1`, `D`, `ABL`, `RB`, or anything under `results/night*/`.
2. Do not change `--no-determinism`, `--n-iters 250000`, extent (15, no override), schedule, or the
   nights' rungs; do not resume.
3. Do not write into any existing run dir; never call `solver.checkpoint()` or
   `solver.test(track_loss=True)` in Part B; `D.build_solver` roots only under the scratchpad.
4. Do not round anything in csv/json (`repr(float(x))`); header `PREVIEW DIAGNOSTIC -- NOT A TEST`.
5. Not a test: no verdict text, no threshold on (a)–(e); nothing here changes the registered 0.3365
   or 12.7279 — whether they should be re-derived is Mike's and the reviewers' decision.
6. Do not launch any part before the Ark and Zcode pass on this brief is in the chat.

## 9. Where the code does not match the design as first proposed
- `--val-every-window` is unnecessary (`--rungs` suffices); the needed change is a clean stop, because
  `--n-iters 26000` changes the lr schedule. The stop path is untested until A0.
- E1 (hook path) has no per-item losses; per-item floors exist for E2/E3 only.
- "State-hook path" and `per_item_eval` are the same function; 8e-08 is not a loss floor (§1).
- Saving solver state at every window read is not needed: checkpoints 7/8 coincide with rungs.
