# Hypothesis (a) — the COMPOSITION package: T2 spliced from B (seed 1) into A (seed 0)

**Date:** 2026-09-15 · **Run by:** CC's subagent on Opus, on Mike's word (DPC Research chat
07:43 local, «do now what can be done before tonight's run»), package as bundled by Zcode
(07:43) with Ark's null-shift calibration (07:33) · **Repo HEAD at launch:** `0485e8f`
(working tree clean except untracked diagnostics directories).

**Registered test:** `docs/preregistration-cheap-vs-expensive.md` §2 (the module = cell type
T2's free parameters, k = 26; pair A = seed 0, B = seed 1; mandatory instrument control
A←A first) and §5 (a) (the criterion, its floor and its 5 % bound). The order of operations
below is part of the record: every file was written to disk before the next stage ran, and
each file carries its own UTC timestamp in `meta.utc`.

Nothing here trains, commits, or writes into `connectome-seed-data`. The two run directories
were listed (path + size + mtime of all 198 files under `results/flow/9991/{000,001}`) before
the first command and after the last; `diff` empty — **NO CHANGE to run dirs**.

## Interpreter

```
C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/.venv/Scripts/python.exe
```

Python 3.10.20, torch 2.9.1+cu128, flyvis 1.2.0, GPU `NVIDIA RTX PRO 4500 Blackwell`
(reported by every stage in its `META` line and in each JSON's `meta`). `FLYVIS_ROOT_DIR`
and `CUBLAS_WORKSPACE_CONFIG` are set by `diag1_eval_paths.py` at import, in the same place
and the same way as `night/run_individual.py:46-49`, so no environment variable has to be
exported first.

## What is reused, and from where

`splice_a.py` imports the evaluator and the parameter loading from
`results/night2/diagnostics/diag1_eval_paths.py` rather than re-implementing them:
`build_solver` (solver in a throw-away datamate root), `chkpt_table` (checkpoint → csv
iteration, stored + 1), `load_checkpoint` (`recover_network` / `recover_decoder` + the real
scheduler at that iteration), `hook_eval` (**the rung hook**, `night/run_individual.py:531-546`
verbatim — the registered evaluator), `per_item_eval` (the 16 per-item losses; *not* the hook
path), `val_item_names`. Checkpoints: `results/flow/9991/000/chkpts/chkpt_00071` (A) and
`.../001/chkpts/chkpt_00071` (B), both csv iteration **250,008** (`chkpt_iter.h5` 250,007 + 1).

The module is spliced at the level of the **raw** registered parameters — `nodes_bias`,
`nodes_time_const`, `edges_syn_strength` — i.e. exactly the tensors the checkpoint stores and
the 734 free core parameters of §2. `Network.clamp()` (`flyvis/network/network.py:480-507`),
which enforces the `non_negative` clamp on `edges_syn_strength` and the symmetry masks, is
called in **training only**; `solver.test()` does not call it, so no evaluation in this
package clamps. There are no symmetry masks on any group (all zero-length,
`t2_module_indices.json`).

## Commands, verbatim, in the order they were run

```bash
PY=".../63f3961a-.../scratchpad/flyvis-probe/.venv/Scripts/python.exe"
OUT="C:/Users/mikha/Documents/dpc-research/connectome-seed/results/night2/diagnostics/splice_a"
ND="C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/03852100-01fd-45ef-82c3-e22ac607b0f7/scratchpad/splice/netdir"

# snapshot of the two run dirs before anything (repeated after the last stage; diff empty)
cd /c/Users/mikha/Documents/dpc-research/connectome-seed-data/results/flow/9991 \
  && find 000 001 -type f -printf "%p %s %T@\n" | sort > .../scratchpad/splice/before.txt

# step 1 — identify the 26 T2 parameters, check the source-type set against prereg Sec 2
"$PY" "$OUT/splice_a.py" --stage indices      --netdir-root "$ND"   # 07:50:52Z

# step 2 — reference: A unchanged -> L_A
"$PY" "$OUT/splice_a.py" --stage reference    --netdir-root "$ND"   # 07:51:54Z

# step 3 — registered instrument control: self-splice A<-A
"$PY" "$OUT/splice_a.py" --stage self         --netdir-root "$ND"   # 07:53:00Z

# step 4 — Ark's null-shift calibration (NOT registered), written before step 5 runs
"$PY" "$OUT/splice_a.py" --stage calib        --netdir-root "$ND"   # 07:54:06Z
"$PY" "$OUT/splice_a.py" --stage calibsummary                        # 07:54:56Z

# step 5 — THE REGISTERED SPLICE: T2_A <- T2_B
"$PY" "$OUT/splice_a.py" --stage splice       --netdir-root "$ND"   # 07:55:37Z

# step 6 — extra context, NOT part of the registered test: B<-A and B<-B
"$PY" "$OUT/splice_a.py" --stage extra        --netdir-root "$ND"   # 07:56:36Z

# step 7 — assemble the per-item table from the files already written
"$PY" "$OUT/splice_a.py" --stage percsv

# snapshot after
cd /c/Users/mikha/Documents/dpc-research/connectome-seed-data/results/flow/9991 \
  && find 000 001 -type f -printf "%p %s %T@\n" | sort > .../scratchpad/splice/after.txt
diff before.txt after.txt   # empty
```

`--stage calibsummary` was added and run **after `--stage calib` and before `--stage splice`**
(07:54:56Z < 07:55:37Z, both recorded in the files), because four of the twenty draws diverged
(two `inf`, two > 1e11) and `inf` poisons the mean/median/max of the 20-value summary. It adds
the field `summary_abs_delta_finite_subset` to `calibration.json` and changes nothing already
written there; its exclusion rule is stated in the field itself. `calibration.json`'s mtime is
therefore later than its `meta.utc`.

`ND` is a throw-away datamate root in the session scratchpad; the solver that runs every
evaluation is built there with `datamate.set_root_context` (`diag1_eval_paths.py:119`), so the
only contact with `connectome-seed-data` is `torch.load` on the two checkpoint files and
`h5py` reads of `chkpt_index.h5` / `chkpt_iter.h5`, all read-only. `solver.test` is always
called with `track_loss=False` (`flyvis/solver.py:543-552`, the only form that writes nothing).

## Output files

| file | what |
|---|---|
| `splice_a.py` | the whole package, one stage per sub-command |
| `t2_module_indices.json` | step 1 — the 26 (key, flat index) slots, the type ordering and its source, the source-type set check against prereg §2, symmetry/clamp config |
| `reference.json` | step 2 — L_A aggregate + 16 per-item, vs the stored checkpoint `val_loss` |
| `self_splice.json` | step 3 — the registered instrument control A←A |
| `calibration.json` | step 4 — 20 random-direction draws at ‖u‖ = ‖v‖, the two real-direction reference shifts (−v, +2v), both summaries |
| `splice_result.json` | step 5 — the registered splice, Δ on both bases with both categories |
| `extra_unregistered.json` | step 6 — B←A and B←B; **not** an (a) outcome |
| `per_item.csv` | step 7 — 16 rows + an `AGGREGATE_hook` row, every column beside its aggregate. The `calib_*` columns are over all 20 draws and carry `inf` where a draw diverged; the `calib16_*` columns are over the 16 kept draws of `summary_abs_delta_finite_subset`. Both are printed; neither is a registered quantity. |

## Definitions fixed in the code, so the record is unambiguous

* **The module vector** is the 26 values in the fixed order: `nodes_bias[32]`,
  `nodes_time_const[32]`, then the 24 `edges_syn_strength` entries in ascending flat index
  (`t2_module_indices.json` → `module`). The same order is used for v, for every u, and for
  every write.
* **Δ** is reported on two bases, as the brief asks: against `1146.1958` — the number §5 (a)
  names literally, the hook value at iteration 250,000 of run 0 — with §5 (a)'s own absolute
  bounds 38.18 / 57.31; and against **L_A**, the loss of the very weights being spliced
  (checkpoint 250,008), with the same *relative* bounds 3.3313 % / 5 % converted on L_A.
  There is no saved checkpoint at exactly iteration 250,000; `chkpt_00071` = 250,008 is the
  only place the weights exist, and its loss is 1148.8075, 2.61 above the 250,000 hook value
  (prereg §7, "8 extra iterations").
* Each evaluation stage also evaluates unmodified A in the same process first
  (`baseline_same_process`), so Δ is available both against the registered L_A and against a
  baseline that carries the same process's evaluation noise. The two differ by 1.7e-5 on the
  registered splice.

---

## Addendum, 2026-09-15 (second session) — the 0.0 anomaly and the achievable-null splices

Run by CC's subagent on Opus, same interpreter, same GPU, repo HEAD `66f1189` at launch.
Driver: `<session scratchpad>/splice2/splice2.py` (three stages, three fresh processes) and
`<session scratchpad>/splice2/merge.py` (assembly only, no evaluation); both import
`splice_a.py` / `diag1_eval_paths.py` rather than re-implementing anything. Nothing here is
a registered (a) outcome, and no category is assigned to any number below. The four run
directories `results/flow/9991/{000,900,001,002}` (396 files) were listed before the first
command and after the last; `diff` empty — **NO CHANGE to run dirs**. New files:
`extra2_reverse_recheck.json`, `extra3_achievable_null.json`, `extra_per_item.csv`.

### 1 — why `per_item_mean_minus_hook` was exactly 0.0 for B←A

**The two numbers are two independent evaluations; nothing is reused.** `stage_extra`
(`splice_a.py:481-516`) computes no loss of its own: every value it writes comes from
`evaluate()` (`splice_a.py:169-182`), called at `:489` (baseline B), `:493` (B←B) and `:497`
(B←A). Inside `evaluate()`, `hook_eval(solver)` runs at `:172` and
`per_item_eval(solver)["flow"]` at `:174` — two separate forward passes over the same 16
validation items; `"hook"` is `:177`, `"per_item_mean"` is `np.mean(per)` at `:179` over the
*second* pass's values, and the printed difference is `np.mean(per) - hook` at `:180`. No
tensor, list or scalar crosses between the paths.

The two paths also use **identical arithmetic**: `hook_eval` (`diag1_eval_paths.py:151-173`)
calls `solver.test(track_loss=False)`, and `MultiTaskSolver.test` (`flyvis/solver.py:473-556`)
collects one `.item()` per batch into a tuple (`:531-536`), averages with `np.mean` (`:542`),
divides the single-task sum by 1 (`:547-548`) and returns it (`:556`); `per_item_eval`
(`diag1_eval_paths.py:176-202`) is the same loop returning the same 16 values. So the only
possible source of a difference is the per-item losses themselves, which are not reproducible
between forward passes (`cudnn.deterministic = False`, `diag1_eval_paths.py:92-93`).

Re-run in two fresh processes, both paths computed separately, in both orders:

| | fresh run 1 (hook first) | fresh run 2 (per-item first) | 2026-09-15 07:56 |
|---|---|---|---|
| baseline B, hook | 1144.636218547821 | 1144.63622713089 | 1144.636239528656 |
| B←A hook path | 3173.6404418945312 | 3173.6400451660156 | 3173.6400756835938 |
| B←A per-item mean | 3173.639938354492 | 3173.6404724121094 | 3173.6400756835938 |
| `mean − hook` | **−0.0005035400390625** | **+0.00042724609375** | 0.0 |
| third pass (per-item again) | 3173.6400756835938 | 3173.640365600586 | — |
| Δ vs same-process L_B | +2029.0042233467102 | +2029.0038180351257 | +2029.0038361549377 |
| Δ as % of same-process L_B | 177.26192745507132 | 177.2618907162291 | 177.2618903792921 |

The difference is ~5e-4 in both fresh runs, i.e. the earlier 0.0 was a **collision of two
independently computed float64 means, not a code-path reuse and not a float32 saturation
effect**. The float32/float64 check confirms the accumulation is not the cause: for fresh run
1 the 16 values sum to 50778.239013671875 in float64, exactly equal to `math.fsum` (the
float64 sum is exact), while a float32 accumulation gives 50778.23828125 — a different number
(mean 3173.639892578125 vs 3173.639938354492), so accumulation order would matter if either
path used float32, and neither does. The direct evidence is the third pass: re-running the
per-item path a second time inside the same process changes 14 of the 16 item losses (max
|Δ| 2.44e-3 in run 1, 2.69e-3 in run 2), which is the ~5e-4 scale of the aggregate.

**The +2029 (+177 %) figure stands.** Three independent processes give B←A hook values
3173.6404418945312 / 3173.6400451660156 / 3173.6400756835938 (spread 3.97e-4) and deltas
+2029.0042233467102 / +2029.0038180351257 / +2029.0038361549377 (spread 4.05e-4), i.e.
**+2029.004 (+177.262 % of L_B)** on any of the three.

### 2 — achievable-null splices into A (unregistered; no category assigned)

One process, `--stage null`: A = seed 0 at checkpoint 250,008 loaded fresh before each write,
the same 26 T2 slots as `t2_module_indices.json`, aggregate by the hook path, 16 per-item
losses beside it. Same-process baseline L_A = 1148.8074293136597 (`reference.json` L_A =
1148.807409286499). Δ below is against `reference.json` L_A.

| splice | L | Δ vs L_A | \|Δ\|/L_A % | Δ vs 1146.1958 | \|Δ\|/1146.1958 % | ‖T2_X − T2_A‖ |
|---|---|---|---|---|---|---|
| A←A (control) | 1148.8074860572815 | +7.677078247070312e-05 | 6.68e-06 | +2.6116860572815312 | 0.22785688599465564 | 0.0 |
| A←0′ (run 900) | 1162.789032459259 | +13.98162317276001 | 1.2170554489584735 | +16.59323245925907 | 1.4476787002062885 | 0.2973379965419648 |
| A←2 (run 002) | 1158.8270206451416 | +10.019611358642578 | 0.8721750293084857 | +12.631220645141639 | 1.1020124698713465 | 0.34632670460554055 |
| A←B (registered, 07:55) | 1187.3873553276062 | +38.57994604110718 | 3.3582 | +41.1915553276062 | 3.5937 | 0.38185439431963675 |

Reference marks, as numbers: the §5 (a) floor 38.18 and 5 % bound 57.31 on the literal basis
1146.1958; the same relative bounds on L_A are 38.26907241815186 and 57.44037046432496. Both
new aggregates (13.98 and 10.02) sit below both floors; both transplant norms (0.2973, 0.3463)
sit below the registered pair's 0.38185439431963675. The A←A control moved the aggregate by
+5.67e-05 against its own same-process baseline (per-item |Δ| ≤ 5.1e-4) and the module read
back bitwise unchanged.

Per-item columns for all of the above are in `extra_per_item.csv` (16 rows + an
`AGGREGATE_hook` row): `L_A_same_process`, `A_from_A`(+delta), `A_from_0prime`(+delta),
`A_from_2`(+delta), and the two reverse-splice re-runs `L_B_recheck_run{1,2}`,
`B_from_A_recheck_run{1,2}`(+delta). The original `per_item.csv` is unchanged.

*Footnote on the last row's two percentages:* here `Δ vs 1146.1958` is `L − 1146.1958`
(41.1915553276062 for A←B, hence 3.5937 %), whereas `splice_result.json`'s
`abs_delta_over_1146.1958_percent` = 3.365912354687321 expresses the *same* Δ vs L_A
(38.57994604110718) over the 1146.1958 basis. Both appear in the record; they are two
different quantities, not a discrepancy. The A←0′ / A←2 rows use the `L − 1146.1958` form in
that column, as do their `delta_vs_1146.1958` fields in `extra3_achievable_null.json`.

## Addendum 2, 2026-09-15 — all four T2→A transplants in ONE process

Ark's review request (08:28): put the four transplants into A in one process so they are
comparable without cross-process spread. Driver: `<session scratchpad>/splice3/extra4.py`,
same interpreter and GPU, imports `splice_a.py` / `diag1_eval_paths.py` rather than
re-implementing anything. Repo HEAD unchanged from the addendum-1 session. The four run
directories `results/flow/9991/{000,900,001,002}` (396 files) were listed before the first
command and after the last; `diff` empty — **NO CHANGE to run dirs**. New file:
`extra4_same_process.json`. Not a registered (a) outcome; no category assigned.

Order, one process, checkpoint A (250,008) loaded once: baseline A (hook + per-item),
A←A, A←0′, A←2, A←1, baseline A again (drift check). Between every transplant, A's module
is written back to the live values captured right after the checkpoint load and the
restoration is asserted bitwise (`module_restored_bitwise: true` on all four blocks;
`module_bitwise_A_after_all_transplants: true`).

| transplant | ‖T2_X − T2_A‖ | L | Δ vs same-process baseline | \|Δ\|/baseline % |
|---|---|---|---|---|
| A←A (control) | 0.0 | 1148.8074069023132 | −4.38690185546875e-05 | 4.0e-06 |
| A←0′ (run 900) | 0.2973379965419648 | 1162.7890062332153 | +13.981555461883545 | 1.217050 |
| A←2 (run 002) | 0.34632670460554055 | 1158.8270211219788 | +10.019570350646973 | 0.872171 |
| A←1 (run 001, registered) | 0.38185439431963675 | 1187.3873572349548 | +38.57990646362305 | 3.358257 |

Baselines: first (before any transplant) 1148.8074507713318; second (after all four, drift
check) 1148.8074789047241. Difference (second − first) = +2.8133392333984375e-05, i.e.
2.4e-06 % of the first — the same ~1e-3-scale evaluation noise seen throughout this package,
not module drift (the module reads back bitwise-A after the last restore).

A←1 in this process reproduces the earlier registered splice (`splice_result.json`,
`delta_vs_reference_L_A` = 38.57994604110718, cross-process) to within 3.96e-5, i.e. well
inside the known ~1e-3 wobble. The A←0′ and A←2 aggregates and norms match
`extra3_achievable_null.json` (cross-process: +13.981603145599365 / 0.2973379965419648 and
+10.019591331481934 / 0.34632670460554055) to within the same noise floor. Ranking by both
norm and effect size is identical in-process and cross-process: A←A < A←2 < A←0′ < A←1.

## Addendum 3, 2026-09-15 — the clamp censoring, and the bit-identical 0.0

Run by CC's subagent on Opus, same interpreter and GPU, repo HEAD `e2997e4` at launch,
following the reviewers' code audit of this directory (Zcode 09:04, Ark 08:54). Drivers:
`<session scratchpad>/splice4/extra5_clamp.py` (arithmetic on the files already here — no
model, no evaluation, no re-draw) and `<session scratchpad>/splice4/extra6_bitid.py` (two
fresh processes), assembled by `merge6.py`; both import `splice_a.py` /
`diag1_eval_paths.py` rather than re-implementing anything. The four run directories
`results/flow/9991/{000,900,001,002}` (396 files) were listed before the first command and
after the last; `diff` empty — **NO CHANGE to run dirs**. No commit. New files:
`extra5_clamp_censoring.json`, `extra6_bit_identity_test.json`.

### 0 — correction to this README and to `splice_a.py`

The "What is reused" section above and `splice_a.py:232-236` state that `Network.clamp()`
is *called in training only* and that *no evaluation in this package clamps*. **That is
false.** `Network.forward()` calls `self.clamp()` on every pass
(`flyvis/network/network.py:527`), and `clamp()` does `param.data.clamp_(0)` **in place**
for every parameter whose `clamp_config` is `non_negative` and whose `requires_grad` is
True (`:490-496`). Directly checked at the end of both processes of §2 below:
`edges_syn_strength.requires_grad` is `True`, and −0.5 written into T2 synapse slot 2
reads back as exactly `0.0` after a single `hook_eval` (`clamp_probe` in
`extra6_bit_identity_test.json`). So every state evaluated in this package was evaluated
**censored at zero**, and the in-memory module was mutated. `clamp_config` is
`non_negative` for `edges_syn_strength` only; `nodes_bias` and `nodes_time_const` are
`null` — **the 2 node slots are not clamped**. All symmetry masks are zero-length, so the
symmetry half of `clamp()` is a no-op here.

### 1 — how much of each calibration draw survived the clamp (`extra5_clamp_censoring.json`)

Arithmetic only. Each draw's `u` was regenerated exactly as `stage_calib` does
(`np.random.default_rng(seed).standard_normal(26)`, then `/‖u‖ · r` with
`r = 0.38185439431963675`) and compared with the stored `draws[i].u`:
**all 20 bitwise identical** (max abs diff
0.0), and the recomputed negative-slot
counts equal the `n_syn_strength_slots_negative` already recorded in `calibration.json`
(True). Every vector is rounded to
float32 before the test, because that is what the parameter tensor holds.

`pre` = ‖written − T2_A‖ (should be r); `post` = ‖clamp(written) − T2_A‖, the shift the
network was actually evaluated at. `neg` = how many of the **24** synapse slots went
negative; `node<0` = how many of the **2** unclamped node slots went negative.

| seed | neg /24 | node<0 /2 | pre-clamp ‖·‖ | post-clamp ‖·‖ | post/pre | recorded \|Δ\| |
|---|---|---|---|---|---|---|
| 0 | 8 | 0 | 0.381854 | 0.270410 | 0.7081 | 35.28 |
| 1 | 9 | 0 | 0.381854 | 0.219776 | 0.5755 | 69.19 |
| 2 | 7 | 1 | 0.381854 | 0.287341 | 0.7525 | 45.93 |
| 3 | 7 | 1 | 0.381854 | 0.347698 | 0.9106 | 34.27 |
| 4 *(divergent)* | 8 | 0 | 0.381854 | 0.275237 | 0.7208 | inf |
| 5 | 9 | 1 | 0.381854 | 0.330452 | 0.8654 | 31.63 |
| 6 | 8 | 0 | 0.381854 | 0.297229 | 0.7784 | 57.03 |
| 7 | 12 | 0 | 0.381854 | 0.234120 | 0.6131 | 67.45 |
| 8 | 8 | 1 | 0.381854 | 0.309696 | 0.8110 | 10.7 |
| 9 *(divergent)* | 6 | 0 | 0.381854 | 0.335024 | 0.8774 | 5.29e+18 |
| 10 | 10 | 1 | 0.381854 | 0.249035 | 0.6522 | 38.34 |
| 11 | 9 | 0 | 0.381854 | 0.284892 | 0.7461 | 55.64 |
| 12 | 8 | 0 | 0.381854 | 0.298447 | 0.7816 | 69.55 |
| 13 | 4 | 1 | 0.381854 | 0.364562 | 0.9547 | 10.98 |
| 14 | 8 | 1 | 0.381854 | 0.295560 | 0.7740 | 22.9 |
| 15 | 7 | 1 | 0.381854 | 0.337452 | 0.8837 | 46.62 |
| 16 | 7 | 0 | 0.381854 | 0.287733 | 0.7535 | 46.21 |
| 17 *(divergent)* | 8 | 0 | 0.381854 | 0.261264 | 0.6842 | 3.413e+11 |
| 18 *(divergent)* | 6 | 1 | 0.381854 | 0.367602 | 0.9627 | inf |
| 19 | 9 | 0 | 0.381854 | 0.315703 | 0.8268 | 69.3 |

All 20 draws had at least one negative synapse slot (4–12, mean 7.9, median 8.0 of 24); 9 of 20 also had a negative `nodes_time_const` (not clamped, so evaluated as written).
Pre-clamp norms equal r to 1e-6 (True).
**Post-clamp effective norms: min 0.219776, mean 0.298462, max 0.367602** (median 0.296395, sd 0.040907). **Zcode's reported 0.22–0.37, mean 0.30 is CONFIRMED** to 2 dp. On average only 78.2 % of the intended r survived, i.e. the null distribution was drawn at a smaller and seed-dependent shift than the registered
transplant it was meant to calibrate.

Reference shifts (same arithmetic):

| shift | neg /24 | node<0 /2 | pre-clamp ‖·‖ | post-clamp ‖·‖ | post/pre | recorded Δ |
|---|---|---|---|---|---|---|
| minus_v | 9 | 0 | 0.381854 | 0.323247 | 0.8465 | 61.600959 |
| plus_2v | 10 | 0 | 0.763709 | 0.583651 | 0.7642 | 53.486861 |

### 1b — the transplants were not censored

Minimum value over the 26 slots of every module that was actually transplanted (all
values float32-exact, read from the files already written):

| module | source field | min over 26 | min over the 24 syn slots | n negative | clamp a no-op |
|---|---|---|---|---|---|
| T2_A (seed 0, the host) | `calibration.json:T2_module_A` | 0.0 | 0.0 | 0 | True |
| T2_B written into A (registered splice) | `splice_result.json:T2_module_B_written` | 0.0 | 0.0 | 0 | True |
| T2_A written into A (self-splice A<-A) | `splice_result.json:T2_module_A_before` | 0.0 | 0.0 | 0 | True |
| T2_A written into B (reverse splice B<-A) | `calibration.json:T2_module_A (= what stage_extra wrote)` | 0.0 | 0.0 | 0 | True |
| T2_B (seed 1, host of the reverse splice) | `calibration.json:T2_module_B` | 0.0 | 0.0 | 0 | True |
| extra3 T2_modules/000 | `extra3_achievable_null.json:T2_modules/000` | 0.0 | 0.0 | 0 | True |
| extra3 T2_modules/900 | `extra3_achievable_null.json:T2_modules/900` | 4.106387132196687e-05 | 4.106387132196687e-05 | 0 | True |
| extra3 T2_modules/001 | `extra3_achievable_null.json:T2_modules/001` | 0.0 | 0.0 | 0 | True |
| extra3 T2_modules/002 | `extra3_achievable_null.json:T2_modules/002` | 1.1173940038133878e-05 | 1.1173940038133878e-05 | 0 | True |
| extra4 T2_modules_source/000 | `extra4_same_process.json:T2_modules_source/000` | 0.0 | 0.0 | 0 | True |
| extra4 T2_modules_source/900 | `extra4_same_process.json:T2_modules_source/900` | 4.106387132196687e-05 | 4.106387132196687e-05 | 0 | True |
| extra4 T2_modules_source/001 | `extra4_same_process.json:T2_modules_source/001` | 0.0 | 0.0 | 0 | True |
| extra4 T2_modules_source/002 | `extra4_same_process.json:T2_modules_source/002` | 1.1173940038133878e-05 | 1.1173940038133878e-05 | 0 | True |
| extra4 T2_module_A_live | `extra4_same_process.json:T2_module_A_live` | 0.0 | 0.0 | 0 | True |

**No transplanted value was negative in any module** — registered splice A←B, self-splice
A←A, reverse splice B←A, and the achievable-null transplants A←0′ and A←2 — so `clamp()`
was a **no-op** for all of them (`transplants_clamp_was_a_noop_everywhere`: True). Trained modules sit on or above zero by
construction: run 000's `T5d->T2` and run 001's `T5b->T2` are exactly 0.0 (clamped during
training), the smallest positive minima being 4.11e-05 (run 900, `TmY15->T2`) and 1.12e-05
(run 002, `Mi13->T2`). The censoring therefore affects **only** the null calibration, not
any measured splice.

### 1c — the four divergent draws (seeds 4, 9, 17, 18)

Numbers only; nothing distinctive found. Negative synapse slots: divergent mean 7.0 (range 6–8) vs kept 8.125 (4–12) — divergent draws were censored
*less*, not more. Post-clamp effective norm: divergent mean 0.309782 vs kept 0.295632. `nodes_bias` after the shift (baseline A 0.513320): divergent 0.45998–0.59219 vs kept 0.38579–0.64727. `nodes_time_const` (baseline A 0.019670): divergent -0.06636–0.04391 vs kept -0.17135–0.13489. One of the four divergent
draws (seed 18) had a negative time constant, against 8 of the 16 kept. No separation on
any of these four quantities.

### 2 — the bit-identical 0.0 (`extra6_bit_identity_test.json`)

Two fresh processes; in each, `hook_eval` and `per_item_eval` interleaved h,p,h,p,… five
of each on the reverse-splice state (B = seed 1 with T2 from A = seed 0), then the same
5+5 on the baseline-B control after a fresh checkpoint reload. All values with all digits:

**process_1** (pid 42188, 2026-09-15T09:32:23Z):

| i | path | reverse splice B←A | baseline B (control) |
|---|---|---|---|
| 0 | hook | 3173.6403045654297 | 1144.6362190246582 |
| 1 | per_item_mean | 3173.64013671875 | 1144.636218547821 |
| 2 | hook | 3173.640350341797 | 1144.636221408844 |
| 3 | per_item_mean | 3173.6402893066406 | 1144.636215209961 |
| 4 | hook | 3173.6401977539062 | 1144.6362223625183 |
| 5 | per_item_mean | 3173.6400146484375 | 1144.6362013816833 |
| 6 | hook | 3173.640151977539 | 1144.6362824440002 |
| 7 | per_item_mean | 3173.640167236328 | 1144.6362390518188 |
| 8 | hook | 3173.6402893066406 | 1144.6362385749817 |
| 9 | per_item_mean | 3173.640090942383 | 1144.636215209961 |

distinct bit patterns of the 10: reverse **9/10**, baseline **9/10**; identical unordered pairs of the 45: reverse 1, baseline 1; hook-path spread 0.000198364 / 6.34193e-05; per-item-path spread 0.000274658 / 3.76701e-05.

**process_2** (pid 37260, 2026-09-15T09:33:08Z):

| i | path | reverse splice B←A | baseline B (control) |
|---|---|---|---|
| 0 | hook | 3173.6403198242188 | 1144.636284828186 |
| 1 | per_item_mean | 3173.640151977539 | 1144.6361989974976 |
| 2 | hook | 3173.6402587890625 | 1144.636254787445 |
| 3 | per_item_mean | 3173.6404418945312 | 1144.6362433433533 |
| 4 | hook | 3173.6399688720703 | 1144.6362524032593 |
| 5 | per_item_mean | 3173.6400299072266 | 1144.6362438201904 |
| 6 | hook | 3173.640335083008 | 1144.636263370514 |
| 7 | per_item_mean | 3173.6397399902344 | 1144.636260509491 |
| 8 | hook | 3173.64013671875 | 1144.6362552642822 |
| 9 | per_item_mean | 3173.640167236328 | 1144.6361894607544 |

distinct bit patterns of the 10: reverse **10/10**, baseline **10/10**; identical unordered pairs of the 45: reverse 0, baseline 0; hook-path spread 0.000366211 / 3.24249e-05; per-item-path spread 0.000701904 / 7.10487e-05.

Both processes reported identical flags and device: `cudnn.deterministic` False, `cudnn.benchmark` False, `torch.are_deterministic_algorithms_enabled()` False, `cudnn.allow_tf32` True, `matmul.allow_tf32` False, `float32_matmul_precision` 'highest', cuDNN 91002, CUDA 12.8, torch 2.9.1+cu128, `CUBLAS_WORKSPACE_CONFIG` :4096:8, NVIDIA RTX PRO 4500 Blackwell sm_12.0 (82 SMs, 34207236096 bytes), 1 device (`determinism_flags_both_processes_identical`: True). Because `cudnn.benchmark` is False,
cuDNN does not autotune and cannot pick a different algorithm per process on that account;
anything beyond what is listed (cuBLAS heuristic state, kernel cache, allocator layout) is
not observable from here and is not asserted.

**Conclusion: the data support Ark's candidate (B).** Within one process the same state
re-evaluated by the same path is not bit-reproducible — 5 hook repeats gave 5 distinct bit
patterns in both processes and on both states, and 9/10, 9/10, 10/10, 10/10 of the ten
values per block were distinct — so the 07:56 equality is **not** the expected behaviour of
a deterministic pair of paths and is recorded here as **unexplained**, not as a
coincidence, and no mechanism is asserted for it.

One number the ulp argument gets wrong, recorded as a measured rate and not as an
explanation: the values do not live at the float64 ulp (4.55e-13). They lie on a coarse
lattice — step 1.52587890625e-05 (2**-16) on the reverse-splice state, whose whole observed spread is only 25–46 steps wide, and step 4.76837158203125e-07 (2**-21) on the baseline state (138–149 steps). Exact equalities were directly observed: 2 of the 180 within-process unordered pairs
(process 1, reverse state, one hook == one per-item mean at 3173.6402893066406; process 1, baseline, two per-item repeats at 1144.636215209961), and pooling both processes 4/190 pairs on the reverse state (2.1 %, of which 3 of the 100 cross-process pairs) and 1/190 on the baseline state.

