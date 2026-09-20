# Row B — passive activity recording on the complete runs of nights 1–5

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

**Amended 2026-09-20, after the first three-checkpoint run and the review it drew.** The
amendments are §15, each dated, each saying what prompted it, and every one of them was
written **before** the run it governs. The registered **P1′ tolerance of `1e-6` is not
amended**: it stands exactly as registered, and the FAIL verdicts the first run produced under
it stand as results. §§1–14 below are the protocol as amended; where a section changed, §15
says which decision changed it.

**Amended again, 2026-09-20, after Ark's reading of `rowB_floor_det.json` (confirmed by CC)** —
four fixes to `--floor-summarize` and to the run's own provenance block, none touching what was
measured (§6, §6a, §9, §10, §16). **Outputs already on disk from before this second amendment
— every `rowB_records*.json`, `rowB_controls*.json`, `.h5` and `.csv` file the earlier `rowB.py`
wrote, and the `rowB_floor[_det].json` files copied into
`floor_summaries_before_sigma_guard/` — were written by that earlier script revision and carry
its own `script_sha256`, not this file's.** Only `rowB_floor.json` and `rowB_floor_det.json`
themselves were regenerated, by `--floor-summarize` alone (no GPU work, no checkpoint touched),
from the unchanged `rowB_records_floor_proc*[_det].json` files that the earlier revision wrote.

**ADR-003 (`docs/decisions/003-blind-authorship-after-the-numbers.md`) applies to this file.**
No result value appears anywhere below: no loss, no activity, no decimal that is a measurement.
Tolerances (`1e-3`, `1e-6`), axis sizes and file geometry are not measurements and do appear.

---

## 1. What is measured, and what the instrument is

For one **run** at one **checkpoint**, the network is run once over the registered held-out set
with a **read-only state hook** attached. The hook is called from `Network._state_api`
(`flyvis/network/network.py:430-433`) — the same site the ablation clamps at — at the end of
`_next_state` (`network.py:413`) and at the end of `_initial_state` (`network.py:375`). It
**reads** `state.nodes.activity`, detaches it, reduces it **on the GPU** — only the reduced
per-type vector (65) and the central-cell vector (65) are moved to CPU — and returns the
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
  must equal P0 **bitwise, or within 1e-6**. The night-2 amendment of 2026-09-15T12:07Z
  applies: the criterion is on **the loss**, the aggregate the rung reports, and the per-item
  figures are recorded beside it for anyone who prefers the stricter reading.

  **The two levels are named separately everywhere** (§15 A2/E). They are different
  statistics and neither substitutes for the other:

  | level | field | has a criterion | has a floor |
  |---|---|---|---|
  | **loss** (the per-item mean — the level `pass` is taken at) | `abs_diff` | **yes, the registered 1e-6** | `abs_diff_loss_nohook_vs_nohook` |
  | **per item** (the maximum over the 16 items) | `per_item_max_abs_diff` | no | `per_item_max_abs_diff_nohook_vs_nohook_FLOOR` |

  A ULP figure is written at **both** levels and they are **not the same number of ULPs**;
  `ulps_level` says which one a field is. Both floors come from the same K repeats (§6).
  `pass` is `abs_diff <= 1e-6` (or bitwise equality) and **nothing else**: the floor
  comparison is the separate, explicitly **unregistered** field
  `descriptive_hook_diff_le_max_floor` (`registered: false`,
  `replaces_the_verdict: false`), which describes and does not judge.
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

  **Amended 2026-09-20 (Ark / CC).** `numpy`'s `ddof=1` sample standard deviation of three
  **bitwise-identical** float64 rows is not always exactly `0.0` — it can come out at the order
  of `1e-15`, a rounding residue of the mean subtraction, not a measured spread. `sigma_by_type`
  and `max_sigma_by_type` are now guarded: where the range (max − min) across the three
  processes is exactly `0` for a type, σ for that type is written as exactly `0.0`.

`--floor-summarize` runs no network and needs no GPU; it is arithmetic over files the script
itself wrote. It refuses if the three processes do not share **one** reduction path and **one**
determinism mode. The floor must exist before any P2′ threshold is written and before any
distance in §7 is read as a separation rather than as a number.

### 6a. The within-process floor of P1′ — `--floor-k` (amendment A3, 2026-09-20)

The across-process floor above bounds the **profiles**. P1′ needs a floor on **the loss**, in
the same process, and until this amendment it had a sample of size **one**: two no-hook
evaluations, one difference. One difference is not a bound.

`--floor-k K` evaluates the same state with **no hook** `K + 1` times and records **all K**
differences against the first — at **both** levels of §5 — together with their maxima and
whether all `K + 1` were bitwise identical. Default `K = 1`, which reproduces the earlier
two-evaluation behaviour exactly; the owner will run `K = 5`. Cost is `K + 3` evaluations per
(run, checkpoint) instead of 4. **At `K = 1` the floor is still a sample of size one and the
record says so in `caveat_at_k_1`.**

**Amended 2026-09-20 (Ark / CC).** Inside one process, `floor_k` names `K` — a real setting of
that process. In `rowB_floor[_det].json` (the **across-process** floor of the first part of this
section, not this within-process one) `floor_k` used to be `--floor-summarize`'s own unused
default and named nothing about the three processes it summarized. It is now
`floor_k_inside_each_process`, read from the three `--floor-repeat` record files' own `floor_k`
and **refused (exit 3)** if they disagree; the old, meaningless top-level `floor_k` is dropped
from the summary.

### 6b. The P2′ multiplier, declared before the floor exists (amendment A6, 2026-09-20)

**Threshold for P2′ = 10 × the measured floor of §6**, taken on the **same reduction path** and
in the **same determinism mode** as the statistic it judges. That is a **computation, not a
judgement**: the multiplier `10` and the rule's text are constants in `rowB.py`
(`P2_FLOOR_MULTIPLIER`, `P2_THRESHOLD_RULE`), written down **today, before any floor for this
metric has been measured**, and `--floor-summarize` only multiplies and records which floor it
multiplied. Both P2′ statistics read off `mean_by_type` and so take the `mean_by_type` floor; a
threshold for the penalised reduction is written beside them from the central-cell floor,
because that quantity has its own scale.

**Stated honestly, because it is the weak point of this declaration:** the P2′ statistics of
the three-checkpoint run of 2026-09-20 were **already visible to reviewers before this
multiplier was declared**. The multiplier is therefore not declared behind a blind. It is a
round number, chosen for being round and not tuned to those statistics, and this paragraph
exists so that nobody has to reconstruct that fact later. A multiplier chosen after seeing the
data is weaker evidence than one chosen before, and that is a property of this threshold, not
of the individuals.

The thresholds are written into `rowB_floor[_det].json`. **The controls files keep the nulls
they were written with**; nothing already on disk is edited after the fact.

The night-2 caveat carries over and is restated here so that it is not discovered later: if a
floor comes out at exactly zero, "margin exceeds the floor" becomes trivially satisfiable, and
that is a property of the floor, not evidence about the individuals.

**Amended 2026-09-20 (Ark's reading of `rowB_floor_det.json`, confirmed by CC).** In
**deterministic** mode the floor is **exactly zero**: three fresh-process repeats of the same
state, forward and reduction both under `torch.use_deterministic_algorithms(True)`, recompute
bit for bit, so the criterion of this section **degenerates to exact equality** — a failure
there means **a bit changed somewhere in the stack**, not that an effect is small. Reading a
zero deterministic floor as "any nonzero difference is huge relative to the floor" is the
mistake this paragraph forecloses. **The mode is part of the threshold, not only this section's
header**: `--floor-summarize` now writes `reduction_path` and `deterministic` **inside each
threshold object** of `p2prime_thresholds`, on the same line as the number, because a threshold
copied out of this file without its mode is not the threshold that was declared.

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
says why: *the prime marks count marks, not order*. The scope is the **ten complete runs** of
nights 1–5 (`--night all10`, amendment A1): `9991/000`, `9991/900`, `9991/001`, `9991/002`,
`9991/003`, `9991/903`, `9991/004`, `9991/005`, `9992/000`, `9992/003`.

**Ten runs are six individuals, and N is counted in individuals.** Seeds 0 and 3 have three
runs each; seeds 1, 2, 4 and 5 have one each. So **N_individuals = 6** and
**n_replicate_runs = 4**, and a replicate **does not enter N** — it is the same individual
measured again, which is what makes it a floor and not a data point. Every record carries
`individual`, `replicate_of`, `is_individual_representative` and
`n_runs_of_this_individual`; `--dry-run` prints the `N` block and the per-individual run lists,
so the count can be read off the plan rather than recomputed from labels. Seed 3 has **three**
runs, so "the twin" is ambiguous for it and the record writes `twin_of` as a **list** of the
other runs of the same seed, with `twin_of_canonical` named separately.

**Two refusals guard the scope** (exit 3, before any checkpoint is opened): a run whose
`chkpts` directory does not hold exactly **72** checkpoints is not a tenth of this scope and is
refused, not silently shortened; and a run label that does not name exactly one directory on
disk is refused. `9991/002_killed_by_reboot` sits beside `9991/002` in the flow tree and holds
a partial run — it is **never** picked, resolution is by exact directory-name equality against
the csv, and `--dry-run` lists it as a **rejected candidate** with its checkpoint count so that
what was passed over is visible rather than assumed.
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

**Which scale the falsifier's own two written fields are on (Johnny, 2026-09-20).** The record
and the tidy csv carry both `pre_weight` (the quantity above) and `weighted = activity_penalty ×
pre_weight`; every number quoted in `PENALISED-QUANTITY-READING.md`'s prose is `pre_weight`, and
the two columns differ by exactly the configured `activity_penalty` (`0.1`, identical across all
ten runs) — see that file's own note near its top.

### How the quantity is read across the 150,000 boundary (rule)

**Provenance.** Stated by Ark in the group chat before the first value was read (2026-09-20,
message on the field list, 19:13 local: drift vs smooth); the three-branch wording below was
written down by Ark on 2026-09-20 21:43 local, AFTER the reading, to record the rule as it was
applied — the AMBIGUOUS branch names cases the reading had already met. It is recorded here so
the next reading does not re-derive it.

> **Правило чтения величины штрафа через границу 150 000** (сформулировано до первого значения).
> Величина, которую штраф минимизировал, читается на каждом чекпойнте; смотрим, как она ведёт
> себя на самой границе и за ней.
>
> - **DRIFT** — после границы величина смещается от baseline, и смещение имеет общее направление
>   у большинства прогонов, заметно большее, чем на соседних границах: штраф держал состояние,
>   его снятие видно.
> - **SMOOTH** — изменение на границе не выделяется среди соседних границ (у нас соседние дают от
>   −0,70 % до +0,53 %, граница +0,19 %), общего направления нет: к моменту снятия штраф
>   состояние не держал.
> - **AMBIGUOUS** — случай не сводится ни к одной форме (смещение начинается не на границе, а
>   позже; или величина идёт *к* baseline, чего правило не описывает) — правило не применяется,
>   случай остаётся открытым и записывается явно.

**English rendering (translation, not a second original).**

> **Rule for reading the penalty quantity across the 150,000 boundary** (formulated before the
> first value). The quantity the penalty minimised is read at every checkpoint; we look at how
> it behaves right at the boundary and past it.
>
> - **DRIFT** — after the boundary the quantity shifts away from baseline, the shift has a
>   common direction across most runs, and it is noticeably larger than at neighbouring
>   boundaries: the penalty was holding the state, and its removal is visible.
> - **SMOOTH** — the change at the boundary does not stand out among neighbouring boundaries (our
>   neighbours give from −0.70% to +0.53%, the boundary gives +0.19%), and there is no common
>   direction: by the time the penalty was lifted, it was no longer holding the state.
> - **AMBIGUOUS** — the case does not reduce to either form (the shift begins not at the
>   boundary but later; or the quantity moves *toward* baseline, which the rule does not
>   describe) — the rule does not apply, the case stays open and is written down explicitly.

**Honest note beside it.** The percentages inside the SMOOTH bullet (−0.70% to +0.53%, boundary
+0.19%) are **held-out LOSS** changes across the 25,000-iteration learning-rate boundaries
(`results/night5/night_report_checkpoints.csv`), not changes of the penalised quantity itself —
a different instrument, quoted here only because it is the figure Ark's own text cites.

**Run 9992/003 (seed 3, third replicate, seed 3‴), stated before its profiles are opened
(Johnny, 2026-09-20).** `penalised_quantity_by_checkpoint.csv` and `run_notes.json` both carry a
`reading_rule_branch`/`reading_rule_note` pair per run, copied — not recomputed — from
`PENALISED-QUANTITY-READING.md` §4. Under that reading, `9992/003` is the one run whose
post-boundary trajectory leaves its neighbourhood on the **central-cell activity axis** (§8's
falsifier; `PENALISED-QUANTITY-READING.md` §3a), but it is **not** an outlier on **held-out
loss** (`results/night5/night_report_checkpoints.csv`) — on that axis it is, if anything, the
calmest of its three seed-3 replicates. Whoever next opens the activity **profiles**
(`mean_by_type`, `central_cell_mean`, the per-step `.h5`) must not silently pool `9992/003` with
its replicates as "a twin like the others", and must not silently drop it either — **both
choices must be stated, before the profiles are opened**, not discovered afterward.

**The question the profiles will be read for — AUTHORISED by Mike 2026-09-20 09:27 UTC; read once
— see PROFILES-READING.md (recorded 2026-09-20,
before the repository's own reading of the profiles; wording Ark's, group chat 21:43 local):**
«различает ли ряд B индивидов; где на этой оси лежит `3‴` после границы» — does row B tell
individuals apart, and where does `3‴` lie on this axis after the boundary. N is counted in
individuals (6), replicates do not enter N, and this remains a preview: no number from it reads
as a test. The reading waits on Mike's word and on the stated handling of `9992/003` above.
Honest note: on 2026-09-20 Ark compared the two modes' profiles in his own sandbox to size the
mode difference (at most ~1e-6 against a between-run range of tens), so the *scale* of the
between-run range was seen by one reviewer before this line existed; which run resembles which
was not read by anyone.

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

**Amended 2026-09-20 (Ark / CC): instrument labels.** Every record's and controls file's
provenance block now carries `gpu_instrument.cuda_runtime_version` (`torch.version.cuda`) and
`gpu_instrument.driver_version` (read via `torch.cuda` where it exposes one, else parsed from
`nvidia-smi --query-gpu=driver_version --format=csv,noheader`; `"unavailable"` if neither
works — this never fails the run). Reason: the `--deterministic` promise "recomputes to the
bit" (§15 A4, below) holds only **for the same driver/library stack**; a run on a moved stack is
not the same instrument even with identical flags, and until this amendment nothing recorded
which stack a run was on.

**`instrument_stack.json` (2026-09-20, Zcode).** No existing artefact of the 2026-09-20 runs
carries a driver version — `gpu_instrument_labels()` exists in `rowB.py` (`:254`) but
`driver_version` was added to it only after those runs were produced. `results/night5/
diagnostics/rowB/instrument_stack.json` records the driver/CUDA/cuDNN/torch/flyvis/numpy/python
versions, GPU name and OS build of this machine, read the same day. **It is a same-day witness
of the stack, not run provenance**: it does not prove the driver was unchanged for the whole
duration of the 2026-09-20 runs, only that it read this on the same machine the same day.

**This mirroring is the reason the 1e-6 was unattainable, and that is a finding** (§15 E).
Because evaluation runs under the nights' `--no-determinism`
(`results/night2/diagnostics/diag1_eval_paths.py:90-93`; `tools/night/start_night.ps1:68`),
two identical evaluations of one state are **not required to agree bit for bit**, and on
trained checkpoints they do not. An **absolute** tolerance of `1e-6` on the loss is therefore
unreachable **by construction** on this path — not because the hook is active, but because the
path itself does not repeat. **The tolerance is unchanged**; what changes is that this README
now says what it was measuring.

**`--deterministic` — a second, separate instrument** (amendment A4). It sets
`torch.use_deterministic_algorithms(True)`, `cudnn.deterministic = True`,
`cudnn.benchmark = False` **before any CUDA work**, and re-applies the two cudnn flags after
`build_solver`, which deliberately sets them to the `--no-determinism` values; **both**
applications are recorded, so the record shows the order and not just a final state.
`torch.use_deterministic_algorithms` is called **nowhere** in flyvis or in these scripts — only
at `tools/night/run_individual.py:295`, in the `else` branch that `--no-determinism` never
takes — so this flag introduces a code path the nights never ran. Accordingly:

* every record, the controls file and the `.h5` attributes carry `deterministic: true/false`;
* **every output is written under a `_det` name**, so the two instruments can never be mixed
  inside one file. A deterministic result is not comparable with a `--no-determinism` one and
  the file names make that structural rather than remembered;
* **training flags are not touched**, here or anywhere in this script;
* if PyTorch raises *"does not have a deterministic implementation"*, the script catches it at
  top level, writes `rowB_nondeterministic_op_det.json` naming **the operator** and the
  innermost flyvis/project frame (`file:line`), and exits **4** — a code of its own, distinct
  from the refusals' 3. **That outcome is a finding, not a crash:** it names an operator in
  this forward that has no deterministic CUDA implementation.

**The recording hook's own reduction is a likely candidate.** It uses `index_add_`, which is on
PyTorch's nondeterministic list on CUDA. If that is the operator that refuses, `--reduce-on
cpu` moves the detached activity to the host before the reduction, so the **forward** can be
tested deterministically with the reduction off the GPU (§15 A5). Default is `gpu`, per the
owner's GPU-first instruction; `reduction_device` and `reduction_path` record which ran.

**Reused verbatim, not re-implemented:**

| from | what |
|---|---|
| `results/night2/diagnostics/diag1_eval_paths.py` | `build_solver` (and with it the determinism settings), `load_checkpoint`, `per_item_eval`, `hook_eval`, `val_item_names` |
| `results/night2/diagnostics/ablation/ablation.py` | `node_type_array` (the type axis, taken exactly as row A takes it), `spearman`, `pearson`, `rankdata` |
| `results/night2/diagnostics/rowB/rowB.py` | `Recorder` (subclassed), `snapshot_state`, `invariants`, `NoDupDict`, `script_sha256` |

**Changed, each stated in the script's docstring as N1–N5 (before the first run) and A1–A6
(2026-09-20, §15):** the run list is keyed by netdir so
that ensemble 9992 is addressable at all (`diag1_eval_paths.chkpt_table` is hard-wired to 9991);
the hook detaches before reducing and reduces **on the GPU**; the central cell of each type is
recorded beside the all-nodes mean; the falsifier is added; P1/P2 become P1′/P2′ with null
thresholds.

**The seven `eval_rung` invariants** (`tools/night/run_individual.py:624-632`) are recorded
around **every** evaluation and a failure is a refusal, not a logged warning.

## 10. Per-record fields

**run group:** `netdir`, `run_id`, `run_label`, `seed`, `role`, `run_index_for_seed`, `night`,
`individual`, `individual_label`, `replicate_of`, `is_individual_representative`,
`n_runs_of_this_individual`,
`twin_of`, `twin_of_canonical`, `chkpt_index`, `chkpt_iter` (read from `chkpt_iter.h5`),
`solver_iteration`, `side_of_stop_iter` (both conventions), `checkpoint_sha256`,
`checkpoint_path`, `git_head`, `torch`, `flyvis`, `numpy`, `CUBLAS_WORKSPACE_CONFIG`,
`n_frames` (+ `n_frames_config`), `dt` (+ the checkpoint's own `dt`), `t_pre`, `n_items`,
`item_names` in registered order, `n_nodes`, `n_types`, `steps_steady_state`,
`n_state_hook_calls`, `eval_wall_s`.

**axis:** `type_labels`, `node_count_per_type`, `central_cell_index_per_type`, `n_nodes`,
`n_types`, `axis_sha256`, `axis_rowA_sha256`, and the row-A comparison — §4.

**Amended 2026-09-20:** the `env` block also carries `gpu_instrument.cuda_runtime_version` and
`gpu_instrument.driver_version` (§9).

**values:** the six `(n_items, n_types)` matrices per item and their aggregates over items,
plus `steps_by_type[item, type, frame]` and `steps_central[item, type, frame]` — §3.

**falsifier:** §8. **controls:** §5. **service fields:** `status:
"unregistered_diagnostic"`, `readable_as_verdict: false`, `hook_kind: "record"`,
`activity_mutated: false`, `recording_detached: true` (detached inside the hook; reduced on
the GPU; only the reduced per-type vectors (65) and the central-cell vector (65) are moved to
CPU), `reduction_device`, `reduction_path` (`"gpu"` / `"cpu"`), `deterministic`,
`determinism_mode`, `floor_k`.

**Where the reduction runs, and which files came from where.** The per-type `index_add_` is
float64 on the activity's own device; a GPU sum accumulates in a different order than the CPU
sum, so the two can differ in the last bits, which is accepted for this instrument.
`reduction_path` is written into every record, into the `.h5` attributes and into the csv
header, so no file is ever silent about which path produced it.

**The three-checkpoint outputs of 2026-09-20 in this directory were produced on the CPU path.
They are SUPERSEDED, not mixed.** They are not comparable, value by value, with anything
produced on the GPU path, and nothing downstream may pool the two. They are kept because a
superseded measurement is a record of what the instrument did that day; they are not an input
to any later reading.

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
| `rowB_records_floor_proc<N>.json`, `rowB_floor.json` | the floor of §6, and the P2′ thresholds of §6b |
| `rowB_nondeterministic_op_det.json` | §9/§15 A4: the operator that refused, its frame, and exit 4 |

**Under `--deterministic` every one of these names takes a `_det` suffix**
(`rowB_records_det.json`, `rowB_steps_<run_label>_det.h5`, …). Two instruments, two sets of
files, no file holding both.

### 11a. Raw outputs stay out of git (Zcode, 2026-09-20/21)

**Principle.** Raw per-checkpoint outputs live outside git; instruments, protocols, controls
and summaries live inside it. This repository draws that same line elsewhere for other raw
streams — the distinction between the committed `results/` tree and the gitignored raw wave
output (`.gitignore`'s own comment, above, on `tools/night/*.json`/`*.log`) is the same shape of
rule applied to a different raw stream. (Checked, 2026-09-20/21: no `ADR-009` or similarly
numbered decision document names this convention explicitly anywhere under `docs/decisions/` —
only three ADRs exist there, 001–003 — so this paragraph states the principle as practiced in
this repository's own `.gitignore`, not as a numbered decision on record; if the convention is
meant to be an ADR, it has not been written yet.)

**Where they are on disk and how large.** The per-checkpoint activity-profile csvs
(`rowB_profiles_*.csv`, `rowB_floor_profiles_*.csv`) and the per-run step h5 files
(`rowB_steps_*.h5`, `rowB_floor_steps_*.h5`) — including their copies inside
`three_checkpoint_gpu_path/`, `superseded_cpu_path_first_run/` and `floor_summaries_before_sigma_guard/`
— total **about 824 MB** across the ten runs, on disk in this directory, gitignored by the
patterns added to `.gitignore` on 2026-09-20/21 (scoped to `results/night5/diagnostics/rowB/`
only, so nights 2 and 3's already-tracked, differently-scoped files of similar names are
untouched).

**They regenerate bit-for-bit.** The deterministic run (`--deterministic`, §9 amendment A4)
recomputes to the bit from the committed `rowB.py`, given the same checkpoints on disk and the
same driver/library stack recorded in `instrument_stack.json` (§9) — that same-day witness file
is why "the same stack" is a checkable claim and not an assumption. The normal (`--no-determinism`)
path does not repeat bit-for-bit between two calls (§9, §15 E.3) and so is not itself a
regeneration guarantee; the deterministic path is.

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
"$PY" "$OUT/rowB.py" --night all10 --chkpts 0,8,71 --dry-run --out-dir "<scratch>"
"$PY" "$OUT/rowB.py" --night all10 --chkpts all   --dry-run --out-dir "<scratch>"
```

**(1) The measurement, on Mike's word — the three named checkpoints, ten runs, GPU path**
(iteration 0, the checkpoint nearest C3, and the end state; indices 0, 8, 71 — verified present
in all ten runs by `--dry-run`), with the floor at `K = 5`:

```bash
"$PY" "$OUT/rowB.py" --night all10 --chkpts 0,8,71 --floor-k 5 \
     --out-dir "$OUT" --netdir-root "$ND"
```

**(2) The same, deterministic** — a *separate* instrument, writing `_det` names; exit 4 means
an operator refused and is a finding (§9). If it is `index_add_`, add `--reduce-on cpu`:

```bash
"$PY" "$OUT/rowB.py" --night all10 --chkpts 0,8,71 --floor-k 5 --deterministic \
     --out-dir "$OUT" --netdir-root "$ND"
"$PY" "$OUT/rowB.py" --night all10 --chkpts 0,8,71 --floor-k 5 --deterministic \
     --reduce-on cpu --out-dir "$OUT" --netdir-root "$ND"     # only if exit 4 named index_add_
```

**(3) The floor — the same (run, checkpoint) pair in three fresh processes**, then the summary,
which also writes the P2′ thresholds from the rule of §6b:

```bash
for r in 1 2 3; do \
  "$PY" "$OUT/rowB.py" --netdir 9992/003 --chkpts 71 --floor-repeat $r --floor-k 5 \
       --out-dir "$OUT" --netdir-root "$ND"; done
"$PY" "$OUT/rowB.py" --floor-summarize --out-dir "$OUT"
```

**(4) The full training axis — all 72 checkpoints of all ten runs, 720 pairs — a separate
decision**, because of its output size, see §13:

```bash
"$PY" "$OUT/rowB.py" --night all10 --chkpts all --floor-k 5 \
     --out-dir "$OUT" --netdir-root "$ND"
```

**Corrected note (Zcode, 2026-09-21).** This command shows `--floor-k 5` as an option, but the
full run actually launched (720 pairs, whose `rowB_records.json` `PENALISED-QUANTITY-READING.md`
reads) used the **default, `floor_k: 1`** — the no-hook floor was taken **once per pair**, not
five times, across all 720 pairs. `K = 5` was run only for the three-checkpoint scope (30 pairs)
and for the three-process floor of §6 (one pair, three processes). "Floor k=5" does **not**
describe the full 720-pair run.

A single run, a single night, or nights 4–5 only, is `--netdir 9992/000` (repeatable),
`--night 4`, or `--night all`. `--netdir` and `--night` are mutually exclusive.

## 13. Cost, and where the estimate comes from

`--dry-run` resolves and prints the counts this estimate is built from. For the **ten-run**
scope (`--night all10`), `K + 3` evaluations per (run, checkpoint) — `K + 1` with no hook (P0
and its floor), one rung-hook path, one with the recorder:

| selection | pairs | evaluations at `--floor-k 1` | at `--floor-k 5` |
|---|---|---|---|
| `--chkpts 0,8,71` | **30** | **120** | **240** |
| `--chkpts all` | **720** | **2,880** | **5,760** |

(For the earlier four-run scope, `--night all`: 12 and 288 pairs, 48 and 1,152 evaluations at
`K = 1`.)

The per-evaluation cost is **already measured on this substrate, and it is cited rather than
reprinted here** — the figures live at their source and this file does not copy measured
decimals out of it (ADR-003):

* `results/night2/diagnostics/ablation/README.md`, section "Interpreter, commands, run time" —
  wall time and per-evaluation cost for 276 evaluations of the 16 held-out items, no hook;
* `results/night2/diagnostics/rowB/README.md` §9, the `traj` line — the same count of
  evaluations **with the row-B recorder attached**, plus the per-process startup cost.

Read against those two lines, the ten-run `--chkpts 0,8,71 --floor-k 5` (**240 evaluations**)
is on the order of a few minutes of measurement inside one process, and `--chkpts all
--floor-k 5` (**5,760 evaluations**) on the order of two hours, plus one process startup. The
`--reduce-on cpu` path is slower than either and is a diagnostic, not a production path.
This script reduces on the GPU exactly as night 2's recorder does, and
moves only the two reduced 65-vectors per Euler step to the host, in `_flush` rather than in
the hook, so no per-step synchronising copy of the 45,669-value tensor is paid. `eval_wall_s`
is written per (run, checkpoint), so the cost is measured rather than estimated. The
three-checkpoint run of **2026-09-20** in this directory predates that change and did move
each step's tensor to CPU inside the hook; its `eval_wall_s` is the cost of that older path.

**Output size.** `--dry-run` prints `projected_steps_h5_bytes_uncompressed`. At `--chkpts all`
the per-step tensors are on the order of **500 MB uncompressed** across the ten runs (gzip-4
is applied, so the files on disk are smaller). Whether that belongs in a repository whose
convention is to keep "the distilled `results/` tree" is a decision to take **before** the
launch, not after: `--chkpts 0,8,71` is about a twenty-fourth of it. Running both instruments
(with and without `--deterministic`) doubles it.

## 14. What this cannot show

Row B is **not causal**: it shows where individuals differ, not where the difference was made.
It does not replace row A; it asks whether row A can be made cheaper. It does not judge (b) —
a new readout after the data of nights 1–5 is a new document, not a re-reading of an old one.
It does not get around the floor: a difference smaller than the instrument's own wandering is
invisible here too.

**And the N. For the ten-run scope, `N_individuals = 6`** — ten runs, six seeds; the four
replicate runs **do not enter N**, because a replicate is the same individual measured again
and is a floor, not a data point. The critical ρ **at that N** is the design document's to
give, and this file does not quote a figure it has not derived: see
`docs/proposals/mi-axis-per-cell-type-design.md` §6 for the table of critical ρ against N. Ten
runs raise N from 4 to **6**; they do not raise it to the 8 that
`docs/next-session-plan.md` §5 sets as the floor for reading row B as a test at all
(*"Do not read row B as a test at N < 8."*). **Six is more individuals, not a test.**

**This is a preview. No number from it reads as a test.**

---

## 15. Amendments of 2026-09-20, after the first three-checkpoint run

Each amendment below was written **after** the first three-checkpoint run of this script and
**before** the run it governs. Each says what prompted it. **None of them touches the
registered P1′ tolerance**: `1e-6` stands, and the FAIL verdicts it produced stand as results.
**No result value appears in this section** (ADR-003); tolerances, counts, multipliers and
levels are not measurements.

### A1 — scope: the ten complete runs, N counted in individuals

**Prompted by:** the owner ("10"). Nights 4 and 5 are four runs; the substrate has **ten**
complete runs across nights 1–5. A preview taken on four of them is a preview of the nights,
not of the substrate. `--night all10` resolves all ten from the committed
`results/night5/run_columns.csv`, keyed by netdir; **72 checkpoints or refuse**, and a label
that does not name exactly one directory is a refusal (§7). **N is counted in individuals:
`N_individuals = 6`, four replicate runs, and replicates do not enter N** (§7, §14).

### A2 — the floor at the judged level

**Prompted by:** Johnny, confirmed by Ark and Zcode. P1′ is registered **on the loss** (§5),
but the no-hook-vs-no-hook floor was recorded only for the **per-item maximum**: the judged
level had a criterion and no floor, the unjudged level had a floor and no criterion.
`abs_diff_loss_nohook_vs_nohook` is now recorded beside `abs_diff`, **at the level the verdict
is taken at**, and §5 names the two levels separately in a table.

### A3 — the floor is no longer a sample of size one

**Prompted by:** Ark. Two evaluations give one difference; one difference is not a bound.
`--floor-k K` (§6a), all K differences recorded at both levels, their maxima beside them, and
the with-hook difference compared against the maximum of the K in
`descriptive_hook_diff_le_max_floor` — **`registered: false`, and it does not replace, soften
or override the P1′ pass/fail.**

### A4 — deterministic diagnostic mode

**Prompted by:** Ark; Zcode verified that `torch.use_deterministic_algorithms` is called
nowhere in flyvis or in these scripts, only at `tools/night/run_individual.py:295` in the
`else` branch `--no-determinism` never takes. `--deterministic`, its `_det` file names, the
`deterministic` field in every record / controls file / `.h5` attribute, and **exit 4 with a
named operator as a finding** — all of §9. **Training flags are not touched.**

### A5 — `--reduce-on cpu|gpu`

**Prompted by:** the same, one step further. The recording hook reduces with `index_add_`,
which is on PyTorch's nondeterministic list on CUDA, so it is a likely operator to refuse under
A4. `--reduce-on cpu` moves the detached activity off the GPU before reducing, so the forward
can be tested deterministically. Default `gpu`, per the owner's GPU-first instruction.

### A6 — the P2′ multiplier, declared before the floor

**Prompted by:** Ark. §6b: threshold = **10 × the measured floor**, same path, same mode;
a computation, not a judgement; declared today, before any floor for this metric exists —
**with the honest caveat, in §6b, that the first run's P2′ statistics were already visible to
reviewers before the multiplier was declared.**

### A7 — path labelling

Every record, `.h5` attribute set and csv header carries `reduction_path`. **The
three-checkpoint outputs of 2026-09-20 in this directory were produced on the CPU path and are
superseded, not mixed** (§10).

### E — what the first run showed about the *instrument*

Not about the individuals. No value is quoted; these are statements about the measuring device.

1. **P0 passed 12 of 12** within its registered `1e-3` — the evaluator reproduces the value
   stored in the checkpoint. But the difference was **exactly zero in some pairs and not in
   all of them**: the evaluator agrees with the stored value to within its tolerance, and does
   not always reproduce it bit for bit.
2. **"2 ULP" was a per-item figure and was read as if it were the verdict's.** The per-item
   maximum difference and the loss-level difference are **different statistics**, and the
   loss-level difference is a **larger** number of ULPs than the per-item one. The two levels
   are now named separately in every field, every table and every sentence (§5, A2); a ULP
   figure without its level is not a quantity.
3. **The `1e-6` was unattainable on trained checkpoints by construction**, and that is a
   finding about the path, not about the hook. Evaluation mirrors the nights'
   `--no-determinism` (`results/night2/diagnostics/diag1_eval_paths.py:90-93`;
   `tools/night/start_night.ps1:68`), so two identical evaluations of one state are not
   required to agree, and non-repeatability is **expected** on this path. An absolute
   tolerance of `1e-6` on the loss therefore cannot be met by an instrument that is bounded by
   a floor larger than it. **The tolerance is unchanged and the FAIL verdicts stand.** A3
   measures that floor instead of assuming it; A4 provides the path on which repeatability is
   a reasonable thing to ask for. Changing the tolerance after the result is the one move
   §5's third failure mode forbids, and it is not made here.

---

## 16. Addendum of 2026-09-20 — what the runs showed about the *instrument*

Same rule as §15 E: statements about the measuring device, not about the individuals. No loss
value and no activity value appears below.

**Deterministic mode, three checkpoints, then the full 720 pairs.** `--night all10 --chkpts
0,8,71 --deterministic`: **P0 720/720** within its registered tolerance; **P1′ 720/720 as
registered** — under `torch.use_deterministic_algorithms(True)` the loss with the recorder
registered reproduces the no-hook reading to the tolerance in every pair. The hook-vs-no-hook
floor and the no-hook-vs-no-hook floor were **exactly zero at both levels** (loss and per-item)
in every pair; **no operator refused determinism** anywhere in the forward or in the recording
hook's own reduction (no exit-4 finding was written). The full deterministic run of all 72
checkpoints × 10 runs (720 pairs) was **about 2.9× slower per run than normal mode**, measured
as script wall time: **2145 s** deterministic against **747 s** normal mode.

**Normal mode, the full 720 pairs (the run `PENALISED-QUANTITY-READING.md` reads).**
`--night all10 --chkpts all` under `--no-determinism` (the nights' own path, §9): **P0
720/720**; **P1′ 92 pass / 628 fail** against the registered `1e-6` on the loss. This is
**explained by GPU operation order** (§9, §15 A4/E.3): the nights' evaluation path does not set
`torch.use_deterministic_algorithms`, so two identical evaluations of one state are not required
to agree bit for bit, and on trained checkpoints they measurably do not. **The tolerance is not
amended by this addendum or by any other in this file** — it stands at `1e-6`, and the FAIL
verdicts this run produced under it stand as results, exactly as §15 already states for the
first, smaller run.

**Which run is the record.** Per Ark (DPC Research group chat, 2026-09-20): **if the
deterministic full run completes cleanly, it becomes the official record**, because it
recomputes to the bit and so is the instrument least confounded by the path's own
non-repeatability; the deterministic 720/720 P0 and P1′ readings above satisfy that condition.
**The two modes are never mixed in one table** — every file name, service field and this section
keep them apart (§9, §10, §15 A4/A7). **The `stop_iter` reading of 2026-09-20
(`PENALISED-QUANTITY-READING.md`) was taken on the NORMAL-mode run** (`deterministic: false`,
`rowB_records.json`, not `rowB_records_det.json`) and that file says so in its own §2 ("Path").
It is not superseded by the deterministic run existing — it is a reading of a different
instrument's output, and this section exists so that which instrument produced which reading is
never left to be inferred from context.
