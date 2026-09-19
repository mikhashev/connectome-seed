# Row B — passive activity recording on the checkpoints of nights 4 and 5

**STATUS: UNREGISTERED DIAGNOSTIC. THIS IS A PREVIEW. NO NUMBER FROM IT READS AS A TEST.**
Not a test of hypothesis (b)/(b2) of `docs/preregistration-cheap-vs-expensive.md`, not a rung,
not an outcome of anything registered — today or later. Every output record carries
`"status": "unregistered_diagnostic"` and `"readable_as_verdict": false`, and the script
refuses to write a verdict field at all for the controls whose threshold does not yet exist.

**Asked for by:** Ark, DPC Research group chat 2026-09-20 19:13 local, as the field list
recorded in the backlog entry
`ROW-B-EXTRACTION-ON-NIGHTS-4-AND-5-NEEDS-THREE-SETTLED-POINTS-BEFORE-THE-FIRST-VALUE`.
**Design lineage:** `docs/proposals/mi-axis-per-cell-type-design.md` (Ark 2026-09-15 08:09 +
Addendum 08:13), §2–§3 (what row B is), §5 Addendum point 2 (which moment of the simulation is
read), Addendum point 3 (all 65 types primary). **Protocol precedents mirrored in layout and
convention:** `results/night2/diagnostics/rowB/README.md` §1–§8 and
`results/night2/diagnostics/ablation/README.md` §1–§8.

**This file was written and saved before `rowB.py` was run on any checkpoint.** At the time of
writing, `rowB.py` had been compiled (`python -m py_compile`), its `--help` printed, and its
`--dry-run` executed — that mode loads no checkpoint and runs no network. No activity value and
no loss value from any real run has been read or printed. Launch is Mike's word.

**ADR-003 (`docs/decisions/003-blind-authorship-after-the-numbers.md`) applies to this file.**
No result value appears anywhere below: no loss, no activity, no decimal that is a measurement.
Tolerances (`1e-3`, `1e-6`), axis sizes and file geometry are not measurements and do appear.

---

## 1. What is measured, and what the instrument is

For one **run** at one **checkpoint**, the network is run once over the registered held-out set
with a **read-only state hook** attached. The hook is called from `Network._state_api`
(`flyvis/network/network.py:430-433`) — the same site the ablation clamps at — at the end of
`_next_state` (`network.py:413`) and at the end of `_initial_state` (`network.py:375`). It
**reads** `state.nodes.activity`, detaches it, moves it to CPU, reduces it, and returns the
state object it was given. That the object was not written is **asserted inside the hook**
(`state.nodes.activity is x` after the read), which is why the service field
`activity_mutated: false` is a measurement of the code path and not a claim about it.

Nothing is trained. Nothing under `connectome-seed-data/results/flow/*` is written: the solver
lives in a scratch datamate root and the run directories are read with `torch.load` and `h5py`
only. `solver.checkpoint()` and `solver.test(track_loss=True)` — the only two calls that write
into a network directory — are never called.

**`activity.h5` is not this instrument.** For every run directory it touches, the first thing
the script prints is that file's h5py **shape and dtype**, and it never reads a value out of
it. The point is Ark's and is the reason the two are printed side by side: `activity.h5` holds
one scalar per training iteration (the mean over all nodes), which is a different object from
the 65-per-checkpoint axis built here. **Size is not an instrument.**

## 2. The two time axes, named separately

They are not the same axis and the field list's "65 × 72" hides that they are two:

| axis | what it indexes | length | where it comes from |
|---|---|---|---|
| **training axis** | saved checkpoints of one run | **72** | `chkpt_index.h5` / `chkpt_iter.h5` in the run directory |
| **simulation axis** | Euler steps within one held-out item | `n_frames` | resolved **at run time** from the recorded steps per item |

`n_frames` is **not** the `task.dataset.n_frames` of the run's `_meta.yaml` — that is the
pre-resampling frame count, and the config value is recorded beside the measured one so the two
can never be confused. The recorded per-step tensor is kept whole (`steps_by_type[item, type,
frame]`), so the choice of summary can be **checked** rather than replayed.

`chkpt_iter` is **read from `chkpt_iter.h5`**, never derived from the checkpoint index, and it
is cross-checked against the `"iteration"` stored inside the checkpoint file itself; a
disagreement is a refusal. The off-by-one is flyvis's and is carried verbatim from
`results/night2/diagnostics/diag1_eval_paths.py:62-77`: flyvis writes `chkpt_iter` as
`self.iteration - 1` (`flyvis/solver.py:463`) and stores `"iteration": self.iteration - 1`
inside the file (`solver.py:453`), while `tools/night/run_individual.py` records
`int(solver.iteration)` in the committed `night_report_checkpoints.csv`. So
`solver_iteration == chkpt_iter + 1`, and the first checkpoint's `chkpt_iter` is negative.

**`side_of_150k` is computed at write time**, from the `chkpt_iter` just read and the run's own
resolved `activity_penalty.stop_iter` — not from a constant written into the script, and not
from the checkpoint index. Because the two iteration conventions differ by one, **both**
readings are written (`side_by_chkpt_iter`, `side_by_solver_iteration`) together with
`conventions_agree`; the window in which they can disagree is exactly one iteration, and the
count of selected checkpoints that fall in it is printed by `--dry-run`.

## 3. The two reductions, named separately, and why both are recorded

This is observation (b) of the backlog entry. "65 numbers" is **two instruments under one
name**, and a file that records only one of them cannot later be asked which it recorded.

| reduction | nodes | frames | what it is the natural unit of |
|---|---|---|---|
| **all nodes of the type** | every node of type T (hundreds to thousands) | all | **row A's population** — the ablation silences all nodes of a type (`results/night2/diagnostics/ablation/ablation.py:90-98`, hook registered at `:106`) |
| **central cell, penalty window** | the **one** central cell of type T | from `n_frames // 4` onward | **the penalised quantity** — `activity[:, n_frames // 4 :, self.central_cells_index].mean(dim=1)` (`flyvis/solver.py:869-872`) |

Six matrices are written per (run, checkpoint), each `(n_items, n_types)`:

* `mean_by_type` — **primary**: all nodes of the type, all frames;
* `std_by_type` — the within-type spread, averaged over frames;
* `last_frame_by_type` — the secondary summary of the night-2 protocol;
* `central_cell_mean` — the central cell, all frames;
* `mean_by_type_skip_first_quarter` — all nodes, the penalty's frame window;
* `central_cell_mean_skip_first_quarter` — **exactly the penalised reduction**.

The middle two exist so that the difference between the reductions can be split into its two
causes — which nodes, and which frames — instead of being attributed to one of them.
`steps_by_type[item, type, frame]` and its central-cell counterpart are saved whole to an
`.h5`.

**A correction to the field list as handed over**, already recorded in the backlog entry and
repeated here because this file is the protocol: the ablation citation given was
`ablation.py:98-104` "in the flyvis package". There is no `ablation.py` under
`tools/.venv/Lib/site-packages/flyvis`. The file is a project script,
`results/night2/diagnostics/ablation/ablation.py`, and the silencing lines are `:90-98` and
`:106`.

## 4. Axis provenance

The type axis is taken from `net.connectome` and is the **same** axis as row A's:

* `type_labels` in `net.connectome.unique_cell_types` order — the order Ark's list names;
* asserted equal, at run time, to `list(dict.fromkeys(node_type_array(net)))`, which is the
  order `ablation.py:164` used for row A. The two are the same list; the assertion is what
  makes that a fact rather than a coincidence, and a mismatch is a refusal;
* `node_count_per_type`, from the same `nodes.type` array;
* `central_cell_index_per_type` from `net.connectome.central_cells_index`
  (`flyvis/connectome/connectome.py:262-264`: the nodes with `u == 0 and v == 0`), asserted
  aligned with the label order — the type at each central index must equal the label at the
  same position, or the penalty's 65-vector and ours would be two different orderings;
* `axis_sha256` over all four fields, and `axis_rowA_sha256` over the three fields row A's
  census records.

`axis_rowA_sha256` is fingerprinted against the census in
`results/night2/diagnostics/ablation/ablation_controls.json` (`meta.types`, `meta.type_counts`,
`meta.n_nodes`, `meta.n_types`), with
`results/night3/diagnostics/ablation/ablation_controls.json` as a second witness. **If the axis
differs from row A's in any label, count or node total, the script refuses: it prints the first
differing labels and exits non-zero (exit code 3).** It does not warn and continue. This is the
whole point of (c) in the backlog entry: an axis that drifts after the first value is read
cannot be repaired afterwards.

## 5. The three controls, reformulated for a passive recording

P1 and P2 of the ablation protocol do not transfer: there is no intervention to empty out and
none to make visible. They are restated, and the restatement is written here, before any value.

* **P0 — the evaluator reproduces the stored value.** The same evaluation with **no hook
  registered at all** must reproduce the `val_loss` stored inside the checkpoint file to
  **1e-3**. That is the tolerance `results/night2/diagnostics/ablation/README.md` §5 uses for
  P0, taken unchanged. The rung-hook path value
  (`diag1_eval_paths.hook_eval`, itself `run_individual.py`'s `eval_rung` body copied verbatim)
  is recorded beside it as P0's second reading.
* **P1′ — the recording hook does not change the loss.** The loss with the recorder registered
  must equal P0 **bitwise, or within 1e-6**. Recorded as pass/fail **plus the absolute
  difference**, plus: whether the per-item vectors are bitwise identical, the per-item maximum
  difference, that figure in float32 ULPs, and its own floor — the same state evaluated
  **twice with no hook at all**. The night-2 amendment of 2026-09-15T12:07Z applies: the
  criterion is on **the loss**, the aggregate the rung reports, and the per-item figures are
  recorded beside it for anyone who prefers the stricter reading.
* **P2′ — the instrument sees something.** Two statistics, no threshold yet:
  **(i)** the per-item vectors restricted to the input cell types (R1–R8, the only nodes the
  stimulus is injected into) must **differ between items** — if the recorder cannot tell two
  different stimuli apart at the photoreceptors, it is not reading the simulation;
  **(ii)** the 65-vector must **not be constant**.
  **Both thresholds are `null` and both verdicts are `null` with `verdict_status:
  "pending_floor"` until the floor of §6 exists.** A threshold for P2′ is derived from the
  floor and **never** from the data it judges. Writing one now, with the distribution of these
  statistics already on screen, is exactly the failure ADR-003 forbids.

**What a failure of the instrument is** (pre-declared, night-2 README §8, restated):
1. P1′ fails — the recording is not passive and nothing recorded describes the un-hooked run;
2. P2′ fails once its threshold exists — the instrument does not see the simulation;
3. the measure has to be changed after the result.
**A failure is a result**, not a reason to re-measure.

**Duplicate key = refusal.** Every keyed writer refuses a duplicate `(netdir, chkpt_index)`
instead of taking the latest value (`NoDupDict`, reused from night 2).

## 6. The floor, and where it may not come from

**The floor is measured for this metric at this state. It is NOT borrowed from the ablation,
and not from night 2's or night 3's row B.** ρ has its own scale, `mean_by_type` has another,
and `central_cell_mean_skip_first_quarter` a third; a floor measured on one of them is not a
floor on the others.

**Procedure.** One and the same `(run, checkpoint)` pair, evaluated in **three fresh
processes** — three separate OS processes, not three evaluations inside one, because the
quantity being bounded includes process-level non-determinism. Each process is marked with
`--floor-repeat N`, writes its own records under `_floor_procN` names, and touches nothing
else. `--floor-summarize` then reads the three and writes, for each of the two primary
quantities:

* **σ by type** — the sample standard deviation across the three processes, per cell type, and
  its maximum over the 65; and
* **σ of the metric** — the largest absolute pairwise difference between the three 65-vectors.

`--floor-summarize` runs no network and needs no GPU; it is arithmetic over files the script
itself wrote. The floor must exist before any P2′ threshold is written and before any distance
in §7 is read as a separation rather than as a number.

The night-2 caveat carries over and is restated here so that it is not discovered later: if a
floor comes out at exactly zero, "margin exceeds the floor" becomes trivially satisfiable, and
that is a property of the floor, not evidence about the individuals.

## 7. The twin trap

Pre-declared, and applied only once a floor exists. Measure: Spearman ρ over the 65 types,
distance `1 − ρ`, reused from `ablation.py` (`spearman`, `pearson`); Pearson is context only
and is **not** the measure — the two have already disagreed on this substrate, and choosing
between them after a result is choosing by outcome.

For each individual with a twin, three quantities are reported: **d(twin)**, **d(other)** for
every other pair, and the **nearest foreign pair taken as the minimum** over the foreign pairs
— not as `(0, 1)`. Taking the nearest foreign pair as the minimum is Ark's correction of
2026-09-15 08:13 (Addendum, point 2 of the verdict rule) and it makes the trap strictly harder
than the rule it replaced.

**Pass condition:** `d(twin)` is the minimum over all pairs **and** below the nearest foreign
pair by **more than the measured floor** of §6.

On the **16 / 13 / 10** item subsets: all 16 is the fixed composition; 13 (without the three
`ambush_2` items) and 10 (without `ambush_2` and `bandage_1`) are **context only**, per the
night-2 protocol §4 and the Zcode item-composition caveat.

**Who has a twin here.** The run list is taken from the committed
`results/night5/run_columns.csv`, keyed by **netdir**, never by label — that file's own header
says why: *the prime marks count marks, not order*. Night 4 contributes `9991/903` (seed 3,
replicate 2) and `9991/005` (seed 5, canonical, **no twin**); night 5 contributes `9992/000`
(seed 0, replicate 3) and `9992/003` (seed 3, replicate 3). Seed 3 therefore has **three** runs
across nights 3–5, so "the twin" is ambiguous for it and the record writes `twin_of` as a
**list** of the other runs of the same seed, with `twin_of_canonical` named separately.
`results/night4/wave_night4.json` — and `tools/night/wave_night5.json` when it is present; it
is gitignored by `.gitignore`'s `tools/night/*.json` rule — are read as **witnesses**, and a
seed disagreement between a wave record and `run_columns.csv` is a refusal.

## 8. The free falsifier

Ark's: print the **penalised quantity** per checkpoint and see whether the 150,000 boundary
binds. It is free — the activity is already recorded — and it is a falsifier because the
penalty is the one thing in the training loop that acts on exactly this axis.

Computed exactly as `flyvis/solver.py:868-883` computes it, on
`central_cell_mean_skip_first_quarter`:

```
pre_weight = (asymmetric_weighting(baseline − activity_mean, below_w, above_w) ** 2).mean()
weighted   = activity_penalty * pre_weight
```

with `asymmetric_weighting(x, γ, δ) = γ·relu(x) − δ·relu(−x)`
(`flyvis/utils/tensor_utils.py:443-461`). `baseline`, `below_w`, `above_w` and
`activity_penalty` are **read from the run's own resolved config**
(`_meta.yaml`, `config.penalizer.activity_penalty`) — none of them is written into the script,
and the script refuses if the run's `stop_iter` disagrees with the solver it built. Beside the
quantity: the counts of central cells **below** and **above** baseline, over all
(item, type) cells and per type.

**One difference from the training-time quantity, stated and not hidden.** In training the
tensor is the **training** batch's activity (batch size 4, augmentation on,
`flyvis/solver.py:350`). Here it is the **held-out** items, batch 1, augmentation off. The
reduction is identical; the stimulus population is not. The record says so in the field
`n_samples_in_training`.

## 9. Determinism, evaluation set, and what is reused

**Evaluation set:** the registered held-out split — 16 items, **batch 1**, augmentation off,
eval mode, all simulation time steps, `t_pre = 0.25`. The same forward as the rung hook and as
the ablation baseline. `n_items` and `item_names` are read from
`solver.task.val_seq_index` in registered order, not assumed.

**Determinism settings match evaluation, not training-from-scratch**, and they come from
`diag1_eval_paths.build_solver:90-93`, which reproduces `run_individual.py:284-286` under
`--no-determinism` — the flag every night wave ran under (`"no_determinism": true` in
`wave_night4.json` and `wave_night5.json`): `cudnn.deterministic = False`,
`cudnn.benchmark = False`, `torch.use_deterministic_algorithms` not set, seeds 0 for
`random` / `numpy` / `torch`. `CUBLAS_WORKSPACE_CONFIG=:4096:8` and `FLYVIS_ROOT_DIR` are set by
the script itself before torch and flyvis are imported, exactly as `ablation.py:22-25` and
`run_individual.py:46-49` do. Both are recorded in every output record.

**Reused verbatim, not re-implemented:**

| from | what |
|---|---|
| `results/night2/diagnostics/diag1_eval_paths.py` | `build_solver` (and with it the determinism settings), `load_checkpoint`, `per_item_eval`, `hook_eval`, `val_item_names` |
| `results/night2/diagnostics/ablation/ablation.py` | `node_type_array` (the type axis, taken exactly as row A takes it), `spearman`, `pearson`, `rankdata` |
| `results/night2/diagnostics/rowB/rowB.py` | `Recorder` (subclassed), `snapshot_state`, `invariants`, `NoDupDict`, `script_sha256` |

**Changed, each stated in the script's docstring as N1–N5:** the run list is keyed by netdir so
that ensemble 9992 is addressable at all (`diag1_eval_paths.chkpt_table` is hard-wired to 9991);
the hook detaches **and moves to CPU** before reducing; the central cell of each type is
recorded beside the all-nodes mean; the falsifier is added; P1/P2 become P1′/P2′ with null
thresholds.

**The seven `eval_rung` invariants** (`tools/night/run_individual.py:624-632`) are recorded
around **every** evaluation and a failure is a refusal, not a logged warning.

## 10. Per-record fields

**run group:** `netdir`, `run_id`, `run_label`, `seed`, `role`, `run_index_for_seed`, `night`,
`twin_of`, `twin_of_canonical`, `chkpt_index`, `chkpt_iter` (read from `chkpt_iter.h5`),
`solver_iteration`, `side_of_stop_iter` (both conventions), `checkpoint_sha256`,
`checkpoint_path`, `git_head`, `torch`, `flyvis`, `numpy`, `CUBLAS_WORKSPACE_CONFIG`,
`n_frames` (+ `n_frames_config`), `dt` (+ the checkpoint's own `dt`), `t_pre`, `n_items`,
`item_names` in registered order, `n_nodes`, `n_types`, `steps_steady_state`,
`n_state_hook_calls`, `eval_wall_s`.

**axis:** `type_labels`, `node_count_per_type`, `central_cell_index_per_type`, `n_nodes`,
`n_types`, `axis_sha256`, `axis_rowA_sha256`, and the row-A comparison — §4.

**values:** the six `(n_items, n_types)` matrices per item and their aggregates over items,
plus `steps_by_type[item, type, frame]` and `steps_central[item, type, frame]` — §3.

**falsifier:** §8. **controls:** §5. **service fields:** `status:
"unregistered_diagnostic"`, `readable_as_verdict: false`, `hook_kind: "record"`,
`activity_mutated: false`, `recording_detached: true`.

## 11. Files

| file | what |
|---|---|
| `rowB.py` | the script |
| `README.md` | this protocol |
| `rowB_dryrun.json` | what `--dry-run` resolved: paths, h5 shapes, checkpoint counts, the axis, the plan |
| `rowB_axis.json` | the axis and its comparison against row A's census |
| `rowB_records.json` | one entry per (run, checkpoint): run group, aggregates, falsifier, invariants |
| `rowB_controls.json` | P0 / P1′ / P2′ per (run, checkpoint) |
| `rowB_profiles_<run_label>_<chkpt_iter>.csv` | 65 rows per (run, checkpoint): aggregates + the per-item columns |
| `rowB_steps_<run_label>.h5` | `steps_by_type` and `steps_central`, saved whole, one group per checkpoint |
| `rowB_records_floor_proc<N>.json`, `rowB_floor.json` | the floor of §6 |

## 12. Launch — the exact commands

Interpreter and data root (the repository's own, `tools/.venv`, torch 2.9.1+cu128,
flyvis 1.2.0; `FLYVIS_ROOT_DIR` and `CUBLAS_WORKSPACE_CONFIG` are set by the script itself):

```
PY="C:/Users/mikha/Documents/dpc-research/connectome-seed/tools/.venv/Scripts/python.exe"
OUT="C:/Users/mikha/Documents/dpc-research/connectome-seed/results/night5/diagnostics/rowB"
ND="<a path containing 'scratchpad'>/rowB5/netdir"
```

`--netdir-root` must contain the string `scratchpad`; `build_solver` refuses otherwise
(`diag1_eval_paths.py:116`), and it wipes that directory before building the throw-away solver.

**Already run, before this file was saved — no checkpoint touched, no network run:**

```bash
"$PY" -m py_compile "$OUT/rowB.py"
"$PY" "$OUT/rowB.py" --help
"$PY" "$OUT/rowB.py" --night all --dry-run --out-dir "<scratch>"
```

**The measurement, on Mike's word — the three named checkpoints first** (iteration 0, the
checkpoint nearest C3, and the end state; indices 0, 8, 71 — verified present in all four runs
by `--dry-run`):

```bash
"$PY" "$OUT/rowB.py" --night all --chkpts 0,8,71 --out-dir "$OUT" --netdir-root "$ND"
```

**The floor — the same (run, checkpoint) pair in three fresh processes**, then the summary:

```bash
for r in 1 2 3; do \
  "$PY" "$OUT/rowB.py" --netdir 9992/003 --chkpts 71 --floor-repeat $r \
       --out-dir "$OUT" --netdir-root "$ND"; done
"$PY" "$OUT/rowB.py" --floor-summarize --out-dir "$OUT"
```

**The full training axis (all 72 checkpoints of all four runs) — a separate decision**, because
of its output size, see §13:

```bash
"$PY" "$OUT/rowB.py" --night all --chkpts all --out-dir "$OUT" --netdir-root "$ND"
```

A single run, or a single night, is `--netdir 9992/000` (repeatable) or `--night 4`.
`--netdir` and `--night` are mutually exclusive.

## 13. Cost, and where the estimate comes from

`--dry-run` resolves and prints the counts this estimate is built from: **288** (run,
checkpoint) pairs at `--chkpts all`, **12** at `--chkpts 0,8,71`, and **4 evaluations per
pair** (two with no hook — P0 and its own no-hook-vs-no-hook floor — one rung-hook path, one
with the recorder).

The per-evaluation cost is **already measured on this substrate, and it is cited rather than
reprinted here** — the figures live at their source and this file does not copy measured
decimals out of it (ADR-003):

* `results/night2/diagnostics/ablation/README.md`, section "Interpreter, commands, run time" —
  wall time and per-evaluation cost for 276 evaluations of the 16 held-out items, no hook;
* `results/night2/diagnostics/rowB/README.md` §9, the `traj` line — the same count of
  evaluations **with the row-B recorder attached**, plus the per-process startup cost.

Read against those two lines, `--chkpts 0,8,71` (**48 evaluations**) is on the order of a
minute of measurement inside one process, and `--chkpts all` (**1,152 evaluations**) is on the
order of ten minutes. **That is a lower bound for this script**, and the reason is stated
rather than absorbed: night 2's recorder reduced on the GPU, while this one moves each Euler
step's 45,669-value tensor to CPU inside the hook (N2, required by `recording_detached`) — one
synchronising copy per step, roughly 650 per evaluation. That cost has **not** been measured
and is not guessed at here. The first real run measures it: `eval_wall_s` is written per
(run, checkpoint), so it is measured once rather than estimated twice.

**Output size.** `--dry-run` prints `projected_steps_h5_bytes_uncompressed`. At `--chkpts all`
the per-step tensors are on the order of **200 MB uncompressed** across the four runs (gzip-4
is applied, so the files on disk are smaller). Whether that belongs in a repository whose
convention is to keep "the distilled `results/` tree" is a decision to take **before** the
launch, not after: `--chkpts 0,8,71` is under a tenth of it.

## 14. What this cannot show

Row B is **not causal**: it shows where individuals differ, not where the difference was made.
It does not replace row A; it asks whether row A can be made cheaper. It does not judge (b) —
a new readout after the data of nights 1–5 is a new document, not a re-reading of an old one.
It does not get around the floor: a difference smaller than the instrument's own wandering is
invisible here too. And the critical ρ at this N is 0.90–1.00
(`docs/proposals/mi-axis-per-cell-type-design.md` §6;
`docs/next-session-plan.md` §5: *"Do not read row B as a test at N < 8."*).

**This is a preview. No number from it reads as a test.**
