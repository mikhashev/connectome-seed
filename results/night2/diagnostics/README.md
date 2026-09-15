# Night-2 diagnostics from saved checkpoints — commands, interpreter, outputs

**Date:** 2026-09-15 · **Run by:** CC (subagent), on Mike's word «делай диагностики» (DPC Research
chat 2026-09-15 06:22) · **Asked for by:** Ark and Zcode,
`docs/experiments/002-night2-seeds-1-and-2.md` §5a items 7 and 10,
`docs/next-session-plan.md` §3/§4.

Nothing here trains, commits, or writes into `connectome-seed-data`. The four runs'
directories were listed (path + size + mtime of all 396 files under
`results/flow/9991/{000,900,001,002}`) before the first command and after diagnostic 1 and
after diagnostic 2 — `diff` empty both times ("NO CHANGE to run dirs").
`flow/9991/002_killed_by_reboot` was not read or touched.

## Interpreter

```
C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/.venv/Scripts/python.exe
```
Python 3.10.20, torch 2.9.1+cu128, flyvis 1.2.0, numpy — GPU `NVIDIA RTX PRO 4500 Blackwell`
(reported by every run in its `META` line). `FLYVIS_ROOT_DIR` and `CUBLAS_WORKSPACE_CONFIG`
are set inside `diag1_eval_paths.py` itself, in the same place and the same way as
`night/run_individual.py:46-49`, so no environment variable has to be exported first.

Shorthands used below:

```
PY=".../63f3961a-.../scratchpad/flyvis-probe/.venv/Scripts/python.exe"
OUT="C:/Users/mikha/Documents/dpc-research/connectome-seed/results/night2/diagnostics"
ND="C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/03852100-01fd-45ef-82c3-e22ac607b0f7/scratchpad/diag/netdir"
```

`ND` is a throw-away datamate root in the session scratchpad. The solver that runs the
evaluation is built there with `datamate.set_root_context` (`diag1_eval_paths.py:119`), so the
only contact with `connectome-seed-data` is `torch.load` on the checkpoint files and `h5py`
reads of `chkpt_index.h5` / `chkpt_iter.h5`, both read-only. The solver is never asked to
checkpoint and `solver.test` is always called with `track_loss=False`, which is the only form
of the call that writes nothing (`flyvis/solver.py:543-552`).

## Commands, verbatim, in the order they were run

```bash
# snapshot of the run dirs before anything (repeated after diag1 and after diag2; diff empty)
cd /c/Users/mikha/Documents/dpc-research/connectome-seed-data/results/flow/9991 \
  && find 000 900 001 002 -type f -printf "%p %s %T@\n" | sort > before.txt

# diagnostic 1 (a) — last checkpoint of each of the four runs through the hook path
"$PY" "$OUT/diag1_eval_paths.py" --task paths  --out-dir "$OUT" --netdir-root "$ND"

# diagnostic 1 (b) — 5 evaluations in ONE process, then 3 in FRESH processes
"$PY" "$OUT/diag1_eval_paths.py" --task noise5 --out-dir "$OUT" --netdir-root "$ND"
"$PY" "$OUT/diag1_eval_paths.py" --task noise1 --rep 1 --out-dir "$OUT" --netdir-root "$ND"
"$PY" "$OUT/diag1_eval_paths.py" --task noise1 --rep 2 --out-dir "$OUT" --netdir-root "$ND"
"$PY" "$OUT/diag1_eval_paths.py" --task noise1 --rep 3 --out-dir "$OUT" --netdir-root "$ND"

# diagnostic 1 (c) — per-item (16 items) losses, four runs, at 250,008 and at 25,212
"$PY" "$OUT/diag1_eval_paths.py" --task items  --out-dir "$OUT" --netdir-root "$ND"

# diagnostic 1 (d) — hook path over all 72 checkpoints of seed 0 and seed 0' (144 evaluations)
"$PY" "$OUT/diag1_eval_paths.py" --task traj   --out-dir "$OUT" --netdir-root "$ND"

# diagnostic 2 — which parameters are trainable (printed from requires_grad, not assumed)
"$PY" "$OUT/diag2_weight_distance.py" --task requires-grad --out-dir "$OUT" --netdir-root "$ND"

# diagnostic 2 — weight-space distances (CPU only)
"$PY" "$OUT/diag2_weight_distance.py" --task all --out-dir "$OUT"
```

`--task paths` was run once before the `shutil.rmtree` guard was added to `build_solver`
(`diag1_eval_paths.py:112-118`); the guard only wipes the scratch datamate root between
processes and does not touch the measurement. Its numbers are in `diag1a_paths.json`.
`--task all` of diagnostic 2 was run twice: the second run added the iteration-0
per-group breakdowns; the distances themselves are unchanged (pure function of the files).

## Checkpoint → iteration mapping used (not guessed)

`flyvis/solver.py:453` stores `"iteration": self.iteration - 1` inside the checkpoint file and
`:463` writes the same value into `chkpt_iter.h5`, while `night/run_individual.py:498` records
`int(solver.iteration)` — which is what the committed `night_report_checkpoints.csv` and every
number quoted in `docs/experiments/00{1,2}-*.md` use. So

```
csv iteration  =  chkpt_iter.h5 value + 1  =  checkpoint-file "iteration" + 1
chkpt_00071    →  chkpt_iter.h5 250007     →  csv iteration 250008
chkpt_00000    →  chkpt_iter.h5     -1     →  csv iteration      0
chkpt_00008    →  chkpt_iter.h5  25211     →  csv iteration  25212
```

Both scripts build this table in `chkpt_table()` and select by the **csv** iteration.

## Output files

| file | what |
|---|---|
| `diag1_eval_paths.py` | diagnostic 1, all five sub-tasks |
| `diag2_weight_distance.py` | diagnostic 2 |
| `diag1a_paths.json` | (a) hook-path value vs stored checkpoint `val_loss`, four runs, chkpt 250,008 |
| `diag1b_noise_inprocess.json` | (b) 5 evaluations, one process |
| `diag1b_noise_proc1.json`, `_proc2.json`, `_proc3.json` | (b) 3 evaluations, fresh processes |
| `diag1c_per_item.json` | (c) 16 per-item losses × 4 runs × 2 checkpoints, plus the hook value and the per-item mean for each |
| `per_item_250008.csv`, `per_item_25212.csv` | (c) the same as a table, with the `seed0′ − seed0` column |
| `hook_path_trajectory_0_vs_0prime.csv` | (d) 72 rows: iteration, hook_val_0, hook_val_0prime, stored_ckpt_val_0, stored_ckpt_val_0prime |
| `diag1d_trajectory_summary.json` | (d) max \|hook − stored\| over the 144, and mean/min/max of (0′−0) over the 29 late checkpoints |
| `diag2_requires_grad.json` | the trainable key set, printed from `named_parameters()` / `named_buffers()` |
| `weight_distance_at_iterations.csv` | 6 pairs × 5 iterations, core / decoder / all, absolute and ÷ mean parameter norm |
| `diag2_group_breakdown_0_vs_0prime_250008.json` | per-group breakdown for (0,0′) at 250,008 |
| `diag2_group_breakdowns.json` | the same plus the iteration-0 controls (0,0′), (0,1), (0,2) |
| `weight_distance_trajectory.csv` | (0,0′) and (0,1) distances over all 72 checkpoints |
| `diag2_weight_distance.json` | everything from `--task all` in one file |

## What counted as "the hook path" and what did not

* `hook_eval()` (`diag1_eval_paths.py:150-172`, body 155-172) is `night/run_individual.py:531-546` copied
  verbatim — the no-op scheduler swap, the four-way RNG save/restore, `torch.no_grad()`, and
  `solver.test(dataloader=task.val_data, subdir="validation", track_loss=False)`. Only the
  wall-time / VRAM / state-assertion lines that follow it (`run_individual.py:547-577`) were
  dropped, because they record telemetry, not the value.
* `per_item_eval()` (`diag1_eval_paths.py:175-201`) is **not** the hook path: it is a copy of
  `flyvis/solver.py:474-556` with `track_loss` removed and the 16 per-item losses returned
  instead of only their mean. It is used only for (c); its mean is printed next to the hook
  value in the same run and agrees with it to < 7e-5 in all eight cases.
* `load_checkpoint()` sets `solver.iteration` from the file and calls the **real** scheduler at
  that iteration before the hook runs, which is what `flyvis`'s own checkpoint-time evaluation
  does (`solver.py:504`); the scheduled `dt` is asserted equal to the `dt` stored in the
  checkpoint. `dt` is constant 0.02 for the whole run (`config/scheduler/scheduler.yaml`
  `dt: start 0.02 stop 0.02`), so the only thing the scheduler changes is the learning rate,
  which `test()` does not use.
