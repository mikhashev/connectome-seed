# Row B — per-cell-type activity profiles from the saved checkpoints

**STATUS: PREVIEW DIAGNOSTIC, NOT A TEST.** n = 4 individuals. The critical ρ at N = 4–5 is
0.90–1.00 (`docs/proposals/mi-axis-per-cell-type-design.md` §6), so **no number in this
directory may be read as a test** of hypothesis (b)/(b2) or of anything else, today or later.
A registered reading needs N ≥ 8. This label is repeated in every output json
(`"status": "PREVIEW DIAGNOSTIC -- NOT A TEST (n=4, critical rho 0.90-1.00)"`).

Design: `docs/proposals/mi-axis-per-cell-type-design.md` (Ark, 2026-09-15 08:09, with the
Addendum of 08:13). Mike's word "do row B" (translated from Russian), DPC Research chat
2026-09-15 09:56.
Everything in **§1–§8 below was written and saved before `rowB.py` was run for the first
time**; §9 onwards (commands, timings, results pointers) was appended after.

## 1. What is measured

Row B for one run at one checkpoint = for each of the 65 cell types

- **mean activity over that type's nodes**, and
- **within-type spread** (std over that type's nodes),

recorded **at every simulation time step** (row C-in-time, saved whole — Addendum point 2),
and summarised as

- **primary: the mean over the whole simulation window**,
- **secondary: the value at the last step**.

Activity = `state.nodes.activity` **as seen by the state hook** — the same quantity the
ablation clamps (`flyvis/network/network.py:430-433`, `_state_api`, called at the end of
`_next_state:413` and of `_initial_state:375`). It is read **without being modified**: the
hook returns the state unchanged.

**Primary profile = all 65 types** (secondary, 57 without R1–R8, printed beside it), fixed in
the Addendum point 3 before this run.

## 2. Evaluation set and forward path

The registered 16 held-out items, **augmentation off, batch 1, eval mode, all simulation time
steps** — the same forward as the rung hook / ablation baseline. The evaluator is **reused
verbatim** from `../diag1_eval_paths.py` (`build_solver`, `chkpt_table`, `load_checkpoint`,
`per_item_eval`, `val_item_names`) and the ablation hook from `../ablation/ablation.py`
(`ablate_hook`, `make_mask`, `spearman`, `pearson`); the solver is built in a scratch datamate
root, the run dirs are read with `torch.load` only. Nothing is trained, no checkpoint or run
dir is written.

Purity of the recording hook, asserted at run time:

- `assert net._state_hooks == ()` before registering (and after clearing);
- **the loss** with the recording hook must agree with the loss without it to **1e-4**
  (bit-identity is additionally recorded, measured not assumed);
- the **seven `eval_rung` invariants** (`tools/night/run_individual.py:550-558`) are recorded
  around every evaluation: `lr_unchanged`, `pen_lr_unchanged`, `dt_unchanged`,
  `scheduler_iter_unchanged`, `back_in_train_mode`, `was_in_train_mode_before`,
  `dataset_augment_restored`.

**Amendment, 2026-09-15 12:07, written at the moment it was made and before any B value was
looked at (only losses had been printed).** The first implementation applied the 1e-4
tolerance to the **per-item** losses and aborted: the max per-item difference was
`0.00048828125` = **exactly one float32 ULP at a ≈ 4,800 loss** (`ambush_2`), i.e. the last
representable bit of the largest item, on a path whose own noise is 0.52–0.85 ppm
(002 §5f, ≈ 4e-3 at that magnitude). The criterion is therefore applied, as §2 says in words,
to **the loss** — the 16-item value the rung hook reports; and beside it are recorded, measured
not assumed: the per-item max difference, the same quantity **in float32 ULPs**, and its own
floor, the same state evaluated **twice with no hook at all**
(`per_item_max_abs_diff_nohook_vs_nohook_FLOOR`). The change is written here rather than
applied silently; the per-item figures are in `rowB_eval_records.json` for anyone who prefers
the stricter reading.

## 3. Rows

- **Row B per item:** the 65 × 16 matrix (primary summary), plus the aggregate over the 16
  items, at iteration **0** (`chkpt_00000`), **25,212** (`chkpt_00008`, the checkpoint nearest
  C3) and **250,008** (`chkpt_00071`).
- **Row C:** row B at **all 72 checkpoints** of each run (65 × 72 per run, aggregate over
  items). Per-item is kept only at 0 / 25,212 / 250,008, to keep the size down.
- **Row C-in-time:** the per-time-step 65-vector is saved whole for the three named
  checkpoints (`rowB_timeseries.npz`), so that the choice of summary can be checked rather
  than replayed.

## 4. Measure, fixed before the first look

- **Carrier measure: Spearman ρ over the 65 types** (Addendum point 2 of §5 / point 2 of the
  verdict rule). Pearson is printed beside it as context only — it is **not** the measure.
- **Distance between individuals: 1 − ρ.**
- **Item composition: all 16**, per item beside it; 13 (without `ambush_2`) and 10 (without
  `bandage_1`) as **context only**.
- **Summary: mean over the whole simulation window** (primary); last step secondary.

## 5. Controls — run and written before any comparison

- **P0, graduated ladder at iteration 0** (Addendum point 1):
  | pair | input | what B must show |
  |---|---|---|
  | (0, 0′) at iter 0 | the same weights, the same data order | **bitwise identical, or identical at noise level** |
  | (0, 1), (0, 2) at iter 0 | difference is exactly the 65 `nodes_bias` | **small but not zero** |
  | (0, 1) at 250,008 | real different individuals | full difference |
- **Reproducibility floor:** the same checkpoint (seed 0, 250,008) evaluated in **3 fresh
  processes**. The floor for ρ is the **spread of Spearman ρ between those three profiles**
  (reported as max(1 − ρ) over the three process pairs), together with the **max per-type
  |ΔB|**. The floor is measured for this metric at this state; it is **not** inherited from
  the ablation (rule R1 / hardening item 13).
- **P2 sanity:** silencing R1–R8 with the ablation hook (reused from `../ablation/ablation.py`)
  must change B of downstream types. Reported: the **top-10 changed types**. If B does not
  move, the instrument does not see an intervention.

## 6. Twin trap — pre-declared

Measure: Spearman ρ over the 65 types; distance 1 − ρ; on the 16-item aggregate.

**Pass condition:** `d(0,0′)` is the **minimum of the six pairs** **and** below the **nearest
foreign pair** by more than the **measured floor** of §5.

All six pairs are reported on 16 items and per item; 13 and 10 items as context only.

## 7. B ↔ A (row A = the causal ablation profile `Δ_T`, `delta_16`, from
`../ablation/ablation_profiles.csv`)

- **(i) primary, within individual:** Spearman ρ between B (primary summary at 250,008) and
  `Δ_T` of the **same** run, 65 types.
- **(ii) preview only, between individuals:** agreement of the two 4 × 4 distance matrices —
  Spearman over the 6 pairwise distances.

## 8. Failure of the instrument — pre-declared

1. `d(0,0′)` is not below the nearest foreign pair by more than the floor;
2. P2 does not move B;
3. the measure has to be changed after the result.

**A failure is a result**, not a reason to re-measure.

**Duplicate key = refusal.** Every reader in `rowB.py` refuses a duplicate key instead of
taking the latest value (hardening item 12).

## 9. Provenance (appended after the run)

**Interpreter:** `C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/.venv/Scripts/python.exe`
— Python 3.10.20, torch 2.9.1+cu128, flyvis 1.2.0, CUDA device as recorded in each json's
`meta.gpu`.

**Data root:** `FLYVIS_ROOT_DIR=C:/Users/mikha/Documents/dpc-research/connectome-seed-data`
(set by the script itself, `rowB.py:29-32`, exactly as `ablation.py:22-26`).

**`rowB.py` sha256:** `195a89b555bedf3a0ff00a4c4e0542eafa6370243fbf9ed954f5fe8fbf7f4082`
(hardening item 9; the same value is written into every output json as `script_sha256`, and
into the header comment of every csv).

**Commands, verbatim** (`$OUT` = this directory, `$S` =
`C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/03852100-01fd-45ef-82c3-e22ac607b0f7/scratchpad/rowB`;
run from `$OUT`):

```
$PY rowB.py --task profiles --out-dir "$OUT" --scratch-dir "$S"
for r in 1 2 3; do $PY rowB.py --task repro --rep $r --out-dir "$OUT" --scratch-dir "$S"; done
$PY rowB.py --task p2   --out-dir "$OUT" --scratch-dir "$S"
$PY rowB.py --task traj --out-dir "$OUT" --scratch-dir "$S"
$PY rowB.py --task analyze --out-dir "$OUT" --scratch-dir "$S"
```

**Run time:** `profiles` 8.9 s of measurement (36 evaluations: 12 with the recording hook, 24
without, for the purity check and its floor) inside a ~38 s process; each `repro` process ~30 s
(one evaluation); `p2` 8 evaluations; `traj` 91.0 s of measurement (288 evaluations = 4 runs ×
72 checkpoints); `analyze` needs no GPU. One 16-item evaluation ≈ 0.2–0.3 s.

**Simulation geometry observed:** 13 steps of grey steady state (computed once per evaluation,
phase 0, not part of any summary) and **40 simulation steps per item**, 16 items, batch 1,
dt = 0.02 — 653 state-hook calls per evaluation.

**Intermediate files** (three reproducibility processes, P2, row-C meta) are in `$S`, not here;
this directory holds only the outputs listed in §10.

**Run dirs unchanged:** a `find`-listing of all **396 files** under
`connectome-seed-data/results/flow/9991/{000,900,001,002}` with name + size + mtime, taken
before the first run and after the last, `diff` **empty**.

## 10. Files

| file | what |
|---|---|
| `rowB.py` | the script (5 tasks: `profiles`, `repro`, `p2`, `traj`, `analyze`) |
| `rowB_profiles_250008.csv` | row B at iteration 250,008, 4 runs × 65 types, aggregate + 16 per-item columns |
| `rowB_profiles_25212.csv` | the same at iteration 25,212 (the checkpoint nearest C3) |
| `rowB_profiles_iter0.csv` | the same at iteration 0 (the P0 ladder) |
| `rowC_trajectory.csv` | row C: 4 runs × 72 checkpoints × 65 types (aggregate over the 16 items) |
| `rowB_timeseries.npz` | row C-in-time: the per-simulation-step 65-vector for every item at the three named checkpoints, saved whole (§3) |
| `rowB_eval_records.json` | per evaluation: purity, the per-item floor, the seven invariants, step counts |
| `rowB_controls.json` | P0 ladder, the measured floor, P2 |
| `rowB_distances.json` | the six pairs, 16/13/10 items, per item, the twin-trap verdict |
| `rowB_vs_rowA.json` | B ↔ A (i) within individual, (ii) between individuals (preview) |
| `rowB_preview.json` | 25,212 → 250,008 |

Every one of them carries the PREVIEW-DIAGNOSTIC label and the script sha256.
