# Row B — night 3 (seeds 3 and 4), and the six-run analysis

**STATUS: PREVIEW DIAGNOSTIC, NOT A TEST.** n = 6 individuals. The critical ρ at N = 4–6 is
0.90–1.00 (`docs/proposals/mi-axis-per-cell-type-design.md` §6) and
`docs/next-session-plan.md` §5 says plainly: *"Do not read row B as a test at N < 8."*
**No number in this directory may be read as a test** of hypothesis (b)/(b2) or of anything
else, today or later. The label is repeated in every output json and in every csv header
(`"status": "PREVIEW DIAGNOSTIC -- NOT A TEST (n=6, critical rho 0.90-1.00; N>=8 rule)"`).

Protocol: **exactly** `results/night2/diagnostics/rowB/README.md` §1–§8, including its dated
amendment of 2026-09-15T12:07Z on the purity tolerance. That file is the specification; this
one records only what is *different*, what was run, and what came out. **§1–§5 below were
written and saved before `rowB3.py` was run for the first time**; §6 onward was appended after.

## 1. What is different from night 2, and nothing else is

The measurement is night 2's `rowB.py`, copied **byte-identically** into this directory
(`cmp` clean, sha256 `195a89b555bedf3a0ff00a4c4e0542eafa6370243fbf9ed954f5fe8fbf7f4082` —
the same value the night-2 README §9 records) and **imported as a module** by `rowB3.py`.
`rowB.task_profiles`, `rowB.task_p2` and `rowB.task_traj` are called unchanged.

Three deliberate differences, each stated in `rowB3.py`'s docstring before the first run:

| | what | why |
|---|---|---|
| **D1** | `rowB.RUNS` = `{"003": "seed3", "004": "seed4"}` | night 3's two runs instead of night 1/2's four |
| **D2** | `rowB.STATUS` says n = 6, not n = 4 | it is a label written into every output; "n=4" in a night-3 file would be false |
| **D3** | `task_repro3` = `rowB.task_repro` with the run identifier as a variable (seed **3** @ 250,008, not seed 0) | a floor is measured, never inherited — README §5, rule R1 / hardening item 13 |

D3 is the only hand-written measurement code in this directory. Its literal diff against
`rowB.task_repro` is printed by `rowB3.py --task diff` and reproduced in §6 below: the run id,
the output filename and the added `driver` stamp; nothing else.

`rowB.task_analyze` is **not** called — it hard-codes the four night-2 labels and six pairs.
`rowB3.task_analyze` replaces it and is analysis only, no GPU, no new evaluation.

**The first four individuals are not recomputed.** Their profiles are read from
`results/night2/diagnostics/rowB/rowB_profiles_{250008,25212,iter0}.csv` and cited; the
six-run tables are built by merging those four label-blocks with this directory's two, with
the cell-type order and the held-out item order asserted equal between the two nights
(`rowB3.py`, `load_six`).

## 2. What is measured for seeds 3 and 4 (night-2 protocol, unchanged)

Row B at **250,008** (`chkpt_00071`), **25,212** (`chkpt_00008`, the checkpoint nearest C3)
and **iteration 0** (`chkpt_00000`) — per item (65 × 16) and aggregate; primary = the mean over
the whole simulation window, secondary = the last step; within-type std beside both. Row C =
the same at all **72** checkpoints of each run, aggregate over items. Row C-in-time saved
whole for the three named checkpoints. `chkpt_index` → iteration is asserted at run time
against `chkpt_index.h5`/`chkpt_iter.h5` (`rowB.load_named`, `rowB.py:287-295`); verified
before the run for both runs: `chkpt_00000` → 0, `chkpt_00008` → 25,212, `chkpt_00071` →
250,008, 72 checkpoints each.

Controls, all four, for the **new** seeds:

- **hook purity** — the 16-item loss with and without the recorder, tolerance 1e-4 (night-2
  README §2 as amended 2026-09-15T12:07Z), with the per-item max difference, that figure in
  float32 ULPs, and its own no-hook-vs-no-hook floor recorded beside it;
- **the seven `eval_rung` invariants** (`tools/night/run_individual.py:550-558`) recorded and
  asserted around **every** evaluation (hardening item 1);
- **P0, graduated ladder at iteration 0**, now over **all 15 pairs** including the nine new
  ones — at iteration 0 two runs differ by exactly their 65 `nodes_bias`, so every cross-seed
  pair must be small but not zero, and the twins exactly zero;
- **the floor for the new seeds** — seed 3 @ 250,008 in **3 fresh processes**: the spread of
  Spearman ρ between the three profiles and the max per-type |ΔB|;
- **P2** — silencing R1–R8 with the ablation hook must move B of downstream types.

Script sha256 of **both** files is written into every json (hardening item 9).

## 3. The six-run analysis — the questions, fixed before the numbers

Measure unchanged: **Spearman ρ over the 65 types, distance 1 − ρ, on the 16-item aggregate**;
13 (without `ambush_2`) and 10 (without `bandage_1`) as **context only**.

- **(a)** all **15** pairwise distances; the twin trap restated at n = 6 — is (0, 0′) still the
  minimum, what is the nearest foreign pair, is it the minimum in 16/16 items.
- **(b)** the same-wave pair (3, 4) against every cross-wave pair. **Wave membership**, read
  from the launcher records, not assumed: seed 0 and seed 0′ = wave `night1`
  (`results/night1/wave_night1.json`, jobs `9991/000`, `9991/900`); seed 1 = wave `night2`;
  seed 2 = wave `night2b` (its first attempt was killed by a Windows Update restart and re-run
  solo, `docs/next-session-plan.md` §2), so **(1, 2) is a cross-wave pair**; seeds 3 and 4 =
  wave `night3`, sequential, seed 3 first (`results/night3/wave_night3.json`). Two same-wave
  pairs exist for the first time: (0, 0′) same wave **and** same seed, (3, 4) same wave and
  **different** seeds; the other 13 pairs are different seeds and different waves. Numbers
  only, no verdict — the design's own note (002 §5i second pass item 5).
- **(c)** exploratory axis 1, named before the launch (`docs/next-session-plan.md` §2a,
  Ark 10:25): activity on T5c/T5d and T2, against the measured twin amplitude band 1.75×.
- **(d)** exploratory axis 2, same source: profile compression (sd, min, max, range).
- **(e)** B ↔ A within individual, which needs night 3's ablation profiles
  (`results/night3/diagnostics/ablation/ablation_profiles.csv`, another agent's output).
  If the file does not exist when this runs, the B side is written and the A side is recorded
  **pending** — not estimated, not skipped silently.
- **(f)** the 25,212 → 250,008 preview at n = 6.
- **(g)** seed 2's self-consistency 0.36 in the six-run context.

Exploratory means exploratory: **(c), (d), (f), (g) carry no verdict and no threshold.**
Adding a reading for them now would be choice after data (002 §5i second pass item 7).

## 4. What would be a failure of the instrument (pre-declared, night-2 README §8)

1. the twin pair is not the minimum, or not below the nearest foreign pair by more than the
   measured floor; 2. P2 does not move B; 3. the measure has to be changed after the result.
**A failure is a result**, not a reason to re-measure. Duplicate key = refusal
(`rowB.NoDupDict`, hardening item 12) — it also guards the four-plus-two label merge.

## 5. What is not touched

Nothing is trained. Nothing under `connectome-seed-data/results/flow/9991/*` is written: the
solver lives in a scratch datamate root and the checkpoints are read with `torch.load` only.
Nothing outside this directory is written except the three intermediate jsons in the session
scratchpad. A `find`-listing of every file under `connectome-seed-data/results/flow/9991`
(name + size + mtime) is taken before the first run and after the last, and `diff`ed (§6).

---

## 6. Provenance (appended after the run)

**Interpreter:**
`C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/.venv/Scripts/python.exe`
— the same venv as night 2's row B; versions as recorded in each json's `meta`.

**Data root:** `FLYVIS_ROOT_DIR=C:/Users/mikha/Documents/dpc-research/connectome-seed-data`,
set by `rowB.py:29-32` (unchanged) and by `rowB3.py:42-45` before torch/flyvis are imported.

**sha256 (hardening item 9), both written into every json:**

- `rowB.py` `195a89b555bedf3a0ff00a4c4e0542eafa6370243fbf9ed954f5fe8fbf7f4082` — byte-identical
  to `results/night2/diagnostics/rowB/rowB.py`, verified with `cmp`.
- `rowB3.py` `f5ab3e5f80f3b8b59d72f76c06c3853b87a3a77066bf59281054f97fa9c9684a` — also in the
  `rowB3.py_sha256` field of every json, and in `SHA256.txt` beside every other file here.

**Commands, verbatim** (`$OUT` = this directory, `$S` = the session scratchpad
`.../03852100-.../scratchpad/rowB3`):

```
$PY rowB3.py --task profiles --out-dir "$OUT" --scratch-dir "$S"
for r in 1 2 3; do $PY rowB3.py --task repro --rep $r --out-dir "$OUT" --scratch-dir "$S"; done
$PY rowB3.py --task p2   --out-dir "$OUT" --scratch-dir "$S"
$PY rowB3.py --task traj --out-dir "$OUT" --scratch-dir "$S"
$PY rowB3.py --task analyze --out-dir "$OUT" --scratch-dir "$S"
```

**D3, the literal diff** (`rowB3.py --task diff`) — the run id, the output filename, the print
label and the added `driver` stamp; the measurement lines are identical:

```
-    solver_it, info = load_named(solver, "000", 71)
+    run, label, ci = "003", "seed3", 71
+    solver_it, info = rb.load_named(solver, run, ci)
-           "run": "000", "label": "seed0", "solver_iteration": solver_it,
+           "run": run, "label": label, "solver_iteration": solver_it,
-    (Path(scratch) / f"rowB_repro_proc{a.rep}.json")...
+    (Path(scratch) / f"rowB3_repro_proc{a.rep}.json")...
```

**Run dirs unchanged:** a `find`-listing of all **625** files under
`connectome-seed-data/results/flow/9991` (all seven run directories, name + size + mtime),
taken before the first run and after the last — `diff` empty. Recorded in §8.

## 7. Files

| file | what |
|---|---|
| `rowB.py` | night 2's measurement, byte-identical copy |
| `rowB3.py` | the driver: D1–D3 and the six-run analysis |
| `rowB_profiles_250008.csv` | row B at 250,008, seeds 3 and 4, 65 types, aggregate + 16 per-item columns |
| `rowB_profiles_25212.csv` | the same at 25,212 |
| `rowB_profiles_iter0.csv` | the same at iteration 0 |
| `rowC_trajectory.csv` | row C: 2 runs × 72 checkpoints × 65 types, aggregate over the 16 items |
| `rowB_timeseries.npz` | row C-in-time, saved whole, for the three named checkpoints |
| `rowB_eval_records.json` | per evaluation: purity, the per-item floor, the seven invariants, step counts |
| `rowB_controls.json` | the P0 ladder over all 15 pairs at iteration 0, the seed-3 floor, P2, the purity summary, the invariant count |
| `rowB_distances.json` | the 15 pairs (16/13/10 items, per item), the twin trap at n = 6, the same-wave comparison |
| `rowB_exploratory.json` | axis 1 (T5c/T5d/T2) and axis 2 (compression) |
| `rowB_preview.json` | 25,212 → 250,008 at n = 6, and seed 2's 0.36 in context |
| `rowB_vs_rowA.json` | B ↔ A: the B side, and the A side or its pending status |
| `SHA256.txt` | sha256 of every file in this directory |

Every json carries the PREVIEW-DIAGNOSTIC label and both script sha256s.

## 8. Results (appended after the run; every figure is in the jsons named beside it)

**PREVIEW DIAGNOSTIC, n = 6 — not a test.** Nothing below is a verdict.

**Controls for the new seeds** (`rowB_controls.json`). Hook purity: the 16-item loss with and
without the recorder agrees to **0.0 / 0.0** (iteration 0), **3.05e-5 / 3.34e-6** (25,212),
**3.15e-5 / 2.48e-5** (250,008) for seeds 3 / 4, tolerance 1e-4 — pass on all six. Per-item max
difference **≤ 0.000488 = 1.0 float32 ULP**, against a no-hook-vs-no-hook floor of 0.000488 /
0.000244 at 250,008 — the amendment case of night-2 README §2, recorded, not silently passed.
Geometry as night 2: 13 grey steady-state steps, 40 steps × 16 items, 653 hook calls per
evaluation. Seven `eval_rung` invariants: **163 evaluations**, all seven true on every one
(19 recorded individually, 144 asserted inside `rowB.task_traj`), one distinct invariant tuple.
**P0 ladder at iteration 0, all 15 pairs:** twins **0.000000** (max |ΔB| 1.40e-10); the nine new
cross-seed pairs **0.1192–0.2112** with max |ΔB| **0.154–0.274** — small but not zero, as the
65-bias-only difference requires; (0, x) equals (0′, x) to the digit for every x, as it must.
**Floor, seed 3 @ 250,008, three fresh processes:** ρ = 1.0000 on all three pairs → rank floor
**0.0**; max per-type |ΔB| **1.35e-8** (night 2's seed-0 figure was 8.25e-8). The night-2 caveat
carries over: a rank floor of exactly 0 makes "margin exceeds the floor" trivially satisfiable.
**P2:** seed 3 loss +58.04, B moves on 64/65 types, max |ΔB| 16.73 (Tm3 −16.73, Mi1 −15.37,
Lawf2 −7.99); seed 4 loss +79.26, 64/65, max |ΔB| 34.11 (Mi4 +34.11, Tm3 +16.28, T2a +13.97).
The instrument sees the intervention on both new individuals.

**The 15 pairs** (`rowB_distances.json`) and the twin trap at n = 6: d(0, 0′) = **0.3487** is
still the **minimum of 15**; the nearest foreign pair is no longer (0, 2) 0.5455 but **(1, 3)
0.4043**, so the margin falls from 0.1968 to **0.0556**. The twin pair is the minimum in
**16/16 items** individually (nearest foreign per item: (1, 3) in 15 of 16), and on both
secondary readings (last step 0.3622 vs 0.4231; 57 types without R1–R8 0.2765 vs 0.4232).

**Same wave vs different wave** — the first comparison with two same-wave pairs: (0, 0′) same
wave and same seed **0.3487** (rank 1 of 15); **(3, 4) same wave, different seeds, 0.8565 —
rank 14 of 15**, above 12 of the 13 cross-wave pairs and above the cross-wave median 0.5990 and
mean 0.6365 (min 0.4043, max 0.8647, sd 0.1456). Numbers only.

**Exploratory axis 1** (`rowB_exploratory.json`), mean_window: T5c 41.62 / −0.04 / 12.31 / 11.14
/ **2.19 / 0.35**; T5d 40.65 / 19.97 / −0.81 / −0.13 / **0.38 / 0.10**; T2 12.94 / 16.80 / 2.66 /
−0.21 / **0.85 / 3.80** (seeds 0 / 0′ / 1 / 2 / **3** / **4**).

**Exploratory axis 2**, population sd of the 65 values: 7.32 / 5.18 / 2.42 / 2.70 / **2.20** /
**5.76**; range 43.53 / 24.68 / 21.12 / 11.89 / **13.71** / **34.57**; profile maximum at T5c /
Tm4 / T5c / T5c / **T3 10.79** / **Tm3 33.03**. Seed 3 is the most compressed of all six; seed 4
is the second least. Within-pair sd ratio for (3, 4) = **2.62** (twin reference 1.41).

**B ↔ A** (`rowB_vs_rowA.json`): the night-3 ablation profiles existed when this ran, so the
A side is complete. ρ(B, Δ_T) within individual = **+0.549** (seed 3) and **+0.573** (seed 4),
beside night 2's +0.389 / +0.481 / +0.563 / +0.653.

**Preview 25k → 250k at n = 6** (`rowB_preview.json`): within-run ρ(B@25,212, B@250,008) =
**0.695** (seed 3) and **0.377** (seed 4), beside 0.581 / 0.675 / 0.790 / 0.358. Spearman
between the 15 between-run distances at 25,212 and at 250,008 = **0.825** (night 2: 0.60 over 6
distances); the twin pair is the minimum of 15 already at 25,212 (0.1246).

**Seed 2's 0.36 in context:** the six self-consistencies rank seed 2 (0.358) first from the
bottom and **seed 4 (0.377) second**, then seed 0 (0.581), seed 0′ (0.675), **seed 3 (0.695)**,
seed 1 (0.790). Seed 2 is no longer alone at the bottom; the open question of 002 §5i second
pass item 4 is not answered here.

**One number in the night-2 write-up does not survive recomputation** (`rowB_exploratory.json`,
`twin_amplitude_band_recomputed`): 002 §5i second pass item 3 gives the twin amplitude band as
"T5c 41.6 vs 23.8 (1.75×)". Read back from
`night2/diagnostics/rowB/rowB_profiles_250008.csv`, seed 0's T5c is 41.6183 but seed 0′'s T5c
is **−0.0365**; **23.8381 is seed 0′'s Tm4**, that profile's maximum. 1.7459 is the ratio of the
two profiles' maxima, which sit on different types — the number is right for what it measures,
the type label on it is not. Measured per type, the twin band is max |ΔB| = **41.65** (median
0.73), larger than (3, 4)'s **28.80** (median 1.13). Consequence, stated not decided: a
per-type threshold of "1.75×" is more permissive than the twin data support. The conclusion the
figure was written to carry — amplitude floats between twins, rank does not — is unchanged and
strengthened. Restating the rule is Mike's and the reviewers' call.

**Run dirs unchanged:** 625 files under `connectome-seed-data/results/flow/9991` (all seven run
directories), name + size + mtime, before and after — `diff` empty. Nothing outside this
directory was written; `git status` in `connectome-seed` shows only this new directory.
Run time: `profiles` 4.1 s of measurement, each `repro` ~30 s of process, `p2` 4 evaluations,
`traj` 47.8 s (144 evaluations), `analyze` no GPU. Another agent's ablation ran on the same GPU
concurrently.
