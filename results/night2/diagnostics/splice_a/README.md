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
