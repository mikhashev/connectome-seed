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
