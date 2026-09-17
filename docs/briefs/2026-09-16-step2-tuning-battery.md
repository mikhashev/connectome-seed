# Brief — step 2: tuning battery (flashes + moving edges vs. the literature table)

**v2, 2026-09-16, after review by Ark and Zcode; v1 was posted at 06:23Z; no v1 sweep was run for
step 2 (only step 1's v1 sweep was launched and discarded — see brief 1's header).**

**Launch only on Mike's explicit «запускай» for this step in the DPC Research chat.**

Aliases: `FV` = `.../63f3961a-.../scratchpad/flyvis-probe/.venv/Lib/site-packages/flyvis` (1.2.0); `CS` = `...\dpc-research\connectome-seed`; `CSD` = `...\dpc-research\connectome-seed-data`.

## 0. Network set — one correction
The request says "seven networks per seed". What exists is **12**: 6 runs x {`chkpt_00071` = iteration 250,008, `chkpt_00000` = iteration 0} (`rowB.py:56-57`, `:287-295`). I read "65 x 7 x 6" as **65 cell types x 7 per-type quantities x 6 runs**, one such table per checkpoint. Ark to confirm.

## 1. The wrapper API does NOT support our checkpoints — plainly
`flash_responses` / `moving_edge_responses` / `moving_bar_responses` all funnel into `generic_responses` (`FV/analysis/stimulus_responses.py:111-256`), which requires a `flyvis.NetworkView` (`:123` isinstance) and uses `.memory` `:147`, `.connectome` `:212`, `.dir.config` `:253`, `.name` `:247`.
`NetworkView.__init__` (`FV/network/network_view.py:85-122`) needs a flyvis `NetworkDir` with `dir.config.network`, resolvable `chkpts`, a best-checkpoint validation-loss file — **and it creates a joblib `Memory` at `self.dir.path/"__cache__"` (`:109-114`), i.e. it writes inside the run directory.** The whole wrapper layer is unusable for us. Do not fake a NetworkView.

## 2. The minimal adapter that IS supported
`Network.stimulus_response(stim_dataset, dt, indices=None, t_pre=1.0, t_fade_in=0.0, grad=False, default_stim_key="lum", batch_size=1)` is a plain `Network` method with no NetworkView in it (`FV/network/network.py:712-799`). So:
1. `solver = D.build_solver(scratch_root)`; `D.load_checkpoint(solver, <chkpt>)` — the ablation path (`CS/results/night2/diagnostics/diag1_eval_paths.py:81`, `:132`).
2. `net = solver.network`; iterate `net.stimulus_response(ds, dt=..., t_pre=1.0, t_fade_in=0.0, batch_size=4)`.
3. Build the `xr.Dataset` ourselves, copying `stimulus_responses.py:58-108` (batch concat, `np.take(responses, cell_index, axis=-1)`) and `:204-254` (coords `frame/channel/hex_pixel/neuron`; `time = arange(n)*dt - t_pre`; `cell_type/u/v` from `net.connectome.nodes`; `attrs['config'] = ds.config.to_dict()`). All analysis functions read only from that Dataset.
   - `cell_index = net.connectome.central_cells_index[:]` (`stimulus_responses.py:56`) -> 65 central cells, one per type; type strings via `ablation.py:87-89`.
   - `import flyvis.utils` first: it registers the `.custom` accessor at import (`FV/utils/__init__.py:40-47`, called at `:60`), needed by `correlation_to_known_tuning_curves` and `angular_tuning`.

## 3. Datasets — flyvis defaults, kept as-is
**Flashes** (`FV/datasets/flashes.py:162-171`), config from `stimulus_responses.py:270-277`: `boxfilter=dict(extent=15, kernel_size=13)` (= our training extent), `dynamic_range=[0,1]`, `t_stim=1`, `t_pre=1.0`, `dt=1/200`, `radius=[-1,6]`, `alternations=(0,1,0)` -> 4 samples (`flashes.py:186-191`), n_frames = 3/dt = 600.
**MovingEdge** (`FV/datasets/moving_bar.py:662-695`), config from `stimulus_responses.py:300-310`: `offsets=(-10,11)`, `intensities=[0,1]`, `speeds=(2.4,4.8,9.7,13,19,25)`, `height=80`, `post_pad_mode="continue"`, `dt=1/200`, `t_pre=1.0`, `t_post=1.0`, `device=flyvis.device`; `angles=[0,30..330]` (`:676`), `widths` forced to `[80]` (`:680`) -> **144 samples**. `t_stim = len(offsets)*led_width/(speed*omm_width)` (`:198-200`; `led_width=radians(2.25)` `:161`, `omm_width=radians(5.8)` `:158`) -> slowest speed 3.39 s, n_frames = (1+3.39+1)/dt ~= **1079**.
**MovingBar** (432 samples, widths [1,2,4]): OMIT in pass 1 — 3x cost, and flyvis's own ensemble view uses the *edge* set for DSI (`FV/network/ensemble_view.py:269-270`) and flashes with `radius=6` for FRI (`:237-238`).

**Three silent traps.**
- `MovingBar.dt` setter (`moving_bar.py:249-262`) **refuses** a dt different from the construction dt and only logs a warning, while `stimulus_response` assigns `stim_dataset.dt = dt` (`network.py:744`). Construct with the intended dt; `assert ds.dt == dt` afterwards.
- `Flashes.dt` is a plain attribute (`flashes.py:159, 193`): assigning it does **not** re-render, it only shifts the time axis. Same rule.
- **dt decision (Ark, Zcode concurring): primary dt = 0.02**, the networks' own training regime
  (`rowB_eval_records.json:184`, asserted at `diag1_eval_paths.py:146`); **secondary dt = 1/200**,
  flyvis's own regime, kept for comparability with flyvis's published numbers. This is not only a
  resolution choice: the Euler step enters the kinetics themselves — the rate term divides by
  `max(time_const, dt)` (Zcode: `FV/network/dynamics.py:207-209`), so a different dt changes the
  network's effective time constants, not merely how finely the trajectory is sampled. The
  difference between the two dt runs is therefore declared a **third quantity**, not noise: tuning
  that holds at both dt -> robust; tuning that holds only at dt = 1/200 -> an artefact of the step,
  a result about the substrate (flyvis's own simulation regime), not about the trained network.
  Both dt values require their own dataset construction, per the two traps above; `simulate` warns
  only above 1/50 (`network.py:673-679`), so neither 0.02 nor 1/200 trips that warning.

**Rendering writes into `CSD/renderings` unless redirected.** `RenderedFlashes` / `RenderedOffsets` are `@root(renderings_dir)` Directories (`flashes.py:25`, `moving_bar.py:30`), `renderings_dir = FLYVIS_ROOT_DIR/renderings` (`FV/__init__.py:57`) = `CSD/renderings`. `@root` defaults to `precedence=2` — "overrides global but not context settings" (`datamate/context.py:69-73`, logic `:121-127`). So wrap **only the dataset constructors** in `datamate.set_root_context(<scratchpad>/renderings)` (`context.py:143-160`); the solver build must see the real root (connectome, SintelDataSet, results).

**NaN padding is expected.** `MovingBar._resample` pads to `t_stim_max` with NaN (`moving_bar.py:340-346`), so faster speeds feed NaN after their stimulus ends and the state goes NaN for the rest of that sample. `peak_responses` masks it (`moving_bar_responses.py:64-71`, `.where(masks, other=0)`). Do not repair it; record the NaN frame fraction per sample.

## 4. Analysis calls — exact signatures
- `flash_responses.flash_response_index(dataset, radius=6, on_intensity=1.0, off_intensity=0.0, nonnegative=True)` — `:25-31`; asserts `alternations == (0,1,0)` at `:50`.
- `flash_responses.fri_correlation_to_known(fris)` — `:91-115`; uses only `polarity != 0` types.
- `moving_bar_responses.peak_responses(dataset, norm=None, from_degree=None, to_degree=None)` — `:41`.
- `moving_bar_responses.direction_selectivity_index(dataset, average=True)` — `:155-194`.
- `moving_bar_responses.preferred_direction(dataset, average=True)` — `:515-552` (radians).
- `moving_bar_responses.angular_tuning(peak_responses(ds), cell_type=<str>, intensity=<0|1>)` — `:637`.
- `moving_bar_responses.dsi_correlation_to_known(dsis)` — `:395-439`; asserts `sizes['intensity'] == 2`.
- `moving_bar_responses.correlation_to_known_tuning_curves(dataset, absmax=False)` — `:442-481`; T4a-d/T5a-d only; ground truth via `get_known_tuning_curves(cell_types, angles)` `:484-512`.
- `moving_bar_responses.angular_distance_to_known(pds)` — `:555-572`; T4 at intensity 1, T5 at 0.
The last two are **not called anywhere inside flyvis**, so the source does not say whether the edge or the bar dataset is intended. Both satisfy the required dims (edge has one width -> trivial argmax).

## 5. Outputs
`CS/results/diagnostics/tuning/`, brief-1 conventions (`PREVIEW DIAGNOSTIC -- NOT A TEST` header
line, `# script_sha256=`, every number via `repr(float(x))` — `rowB.py:307-319`). Named by
subject, not by night (Ark; Zcode agrees) — this directory hosts diagnostics over runs from
several nights.
- `tuning_per_type.csv` — `run,label,checkpoint_iter,cell_type` + FRI, DSI_on, DSI_off,
  `PD_on_cos`, `PD_on_sin`, `PD_off_cos`, `PD_off_sin` (PD encoded circularly as (cos, sin), never
  the raw angle — Ark; Zcode agrees), and the 12-angle tuning vector per intensity (24 cols).
  65 x 12 = 780 rows. The raw `PD_on`/`PD_off` radians returned by `preferred_direction`
  (`moving_bar_responses.py:515-552`) are computed as an intermediate but not stored as a column;
  only their cosine and sine are.
- `tuning_literature.json` — per network: `fri_correlation_to_known`, `dsi_correlation_to_known`, `correlation_to_known_tuning_curves` (8), `angular_distance_to_known` (8).
- `tuning_controls.json` — meta as in brief 1 (sha256 of this script + `diag1_eval_paths.py`, `ablation.py`, `rowB.py`; flyvis/torch/python/GPU/utc) + `ds.config.to_dict()` verbatim for both datasets, both dt values (0.02 and 1/200), n_samples, n_frames, NaN fractions, per-network wall time.

## 6. Controls
- **P0:** same network twice in one process -> per-type vectors bitwise identical (these datasets draw no RNG; `stimulus_response` sets none). Report max |delta|.
- **P0-bis:** fresh process; record the spread. No gate pre-set.
- **Iteration-0 baseline:** the whole battery on `chkpt_00000` of every run.
- **What the literature-comparison functions return for an untrained vs a trained net: TO BE MEASURED.** The flyvis source states no range and nothing has been run. Do not put a number from the paper into the pre-registration.
- **Controls follow checklist rule 17 (added 2026-09-17).** Any copy of flyvis code (should one be
  needed here) is gated by a code diff, not by a number; numeric reproducibility of tuning
  quantities (P0, P0-bis above) is recorded, with stops only on documented ceilings derived from
  ≥ 2 processes; no control compares one realisation with an extremum of another.

## 7. Pre-registered readings (verbatim, with mechanics)
(a) **twin trap in tuning space** — (0, 0') minimum of 15 pairwise distances by rank correlation across the concatenated per-type tuning vector, with the 1/15 floor as a sanity check. Mechanics: one vector per network = 65 types x [FRI, DSI_on, DSI_off, cos PD_on, sin PD_on, cos PD_off, sin PD_off, 24 tuning values] — PD encoded circularly, never the raw angle (Ark; Zcode agrees); distance = 1 - Spearman rho (`ablation.py` `spearman`, reused at `rowB.py:325`).
(b) **dominant type functional?** — deviation of the dominant type's tuning (**R2** in seed 2, **Mi4** in seed 3, **CT1(Lo1)** in seed 4 — named exactly, not "CT1"; there are two CT1 types) from the same type in the five other runs, ranked among 65 types, outcomes <= 3 / >= 30 / between. Exact names and sizes from `ablation_profiles.csv`: seed 2 **R2** +21157.5, seed 3 **Mi4** +4827.5, seed 4 **CT1(Lo1)** +10460.9.
(c) **count of the 65 types holding the literature polarity and direction per fly and its spread across flies.** *Not attainable as written:* only **32 of the 65** types have a non-zero `polarity` entry (`FV/utils/groundtruth_utils.py:16-82`; the other 33 are 0 = unknown) and only **8** have a `preferred_directions` entry (`:181-190`). The counts are out of 32 and out of 8. These counts are **descriptive only** (Ark); the carrying quantities for reading (c) are `fri_correlation_to_known`, `dsi_correlation_to_known`, `correlation_to_known_tuning_curves`, and `angular_distance_to_known`.
(d) **iteration 0 as null.**

## 8. Provenance question for Ark — `groundtruth_utils` fields
Docstring `:1-11`: "All data structures are based on published literature and may need to be updated as new research becomes available." **The file contains exactly two citations**, quoted in full: `"L5": 1,  # Drews 2020, Matulis 2020` (`:29`) and `# from Maisak et al. 2013 Fig. 3 g, h` (`:514`, covering `tuning_curves`, T4a-d/T5a-d). Other comments are definitions, not sources: `# 1 is ON, 0 is unknown, -1 is OFF` (`:15`), `# no motion tuning in T4 and T5 inputs` (`:486`).
**No source stated at all** for: `polarity` as a whole (`:16`), `on_pathway` (`:84`), `off_pathway` (`:98`), `layout` (`:113`), `preferred_directions` (`:181`), `on_direction_selective` (`:192`), `off_direction_selective` (`:260`), `not_direction_selective` (`:328`), `asymmetric_input` (`:397`), `unsufficient_data` (`:464`), `noisy_data` (`:475`), `motion_tuning`/`on_`/`off_` (`:506-508`).
**Derived in-file, not data:** `symmetric_inputs` (`:477`, from `asymmetric_input` minus the two exclusion lists, 33), `known_dsi_types` (`:510` = `no_motion_tuning + motion_tuning`, 18), `known_preferred_contrasts` (`:512`, from `polarity`, 32), `no_motion_tuning` (`:487`, 10, with three L-types commented out at `:488-490`, `:496-498`).
No field anywhere is described as derived from connectivity. Question for Ark: `asymmetric_input` / `symmetric_inputs` read like connectome-derived quantities but carry no source — is there one outside the file?

**Mandatory pre-S2 provenance check (Ark) — for the genome step, not for this battery.** Before
`polarity` is used as an external label anywhere in step 3 (genome): recompute polarity from the
input rule of the connectome itself (L1 -> ON, L2 -> OFF pathway) and compare it with
`groundtruth_utils.polarity`. If it matches, the field is connectivity-derived, not an independent
literature label, and is not usable as an external label for S2. **Not to be run without Mike's
word.**

## 9. Runtime and memory — ESTIMATE
Memory: `forward` stacks the whole run (`network.py:546`), so ~`batch x n_frames x 45669 x 4 B` for the activity plus the same for the stimulus buffer. MovingEdge at batch 4 x 1079 frames ~= 0.79 GiB each -> ~1.6-2.5 GiB peak; batch_size 4 (the flyvis default) is comfortable on 32 GiB.
Time: our 16-item eval at dt=0.02 takes 0.18-0.49 s (`night2/.../ablation/README.md:130-132`; `night3/.../ablation_controls.json` `one_evaluation_wall_s`), but those items are ~19 Euler steps. MovingEdge is 36 batches x 1079 sequential steps ~= 38.8k steps per network; Flashes is 1 batch x 600. **ESTIMATE 3-8 min per network for edges, < 10 s for flashes -> 12 networks ~= 45-100 min**, plus a one-off `RenderedOffsets` render (144 angle x width x intensity, ESTIMATE 1-5 min). This estimate is now doubled by the two-dt decision (primary 0.02 + secondary 1/200) unless the two dt runs share a render. All of these are estimates with no measurement behind them: measure the first network's real wall time and report it before continuing with the other eleven.

## 10. Do not
1. No `NetworkView`, `flash_responses()`, `moving_edge_responses()`, `moving_bar_responses()` or `Ensemble` — each writes `__cache__` into a network directory.
2. Nothing written under `CSD/results/flow/9991/**`; diff the 594-file listing (size + mtime) before and after, as `night3/.../ablation/README.md:107-111` does.
3. No `RenderedFlashes`/`RenderedOffsets` in `CSD/renderings` — `set_root_context` around the dataset constructors only.
4. No training; never call `solver.checkpoint()` or `solver.test(track_loss=True)`.
5. No edits under `CS/results/night2/`, `CS/results/night3/`, or anywhere in `CS`.
6. No change to any flyvis dataset default. If one must change, stop and ask.
7. Do not drop, interpolate or zero the NaN padding outside `peak_responses`' own masking.
8. Do not quote a literature-correlation "expected range" that was not measured in this run.
9. No rounding in outputs; `repr(float(x))`.
10. Do not commit or push. Do not call this a test.

## 11. Revision history
- **v1 -> v2** (Ark, review posted 06:24Z 2026-09-16): output directory renamed to
  `CS/results/diagnostics/tuning/`, named by subject not by night (§5); PD encoded circularly as
  (cos, sin), never the raw angle, propagated into `tuning_per_type.csv` and reading (a)'s vector
  (§5, §7(a)); dominant-type names in reading (b) stated exactly, `CT1(Lo1)` at first mention
  (§7(b)); reading (c)'s 32-of and 8-of counts marked descriptive only, with the four
  correlation/distance functions named as the carrying quantities (§7(c)); mandatory pre-S2
  provenance check specified for the genome step (§8); dt = 0.02 primary / 1/200 secondary
  decided, concurring with Zcode.
- **v1 -> v2** (Zcode, review posted 06:27Z 2026-09-16): dt decision grounded mechanically — the
  Euler step enters the kinetics via `max(time_const, dt)` in `FV/network/dynamics.py:207-209`, so
  dt is not only a resolution choice; primary dt = 0.02 (training regime), secondary dt = 1/200
  (flyvis regime), and the primary/secondary discrepancy declared a third, reportable quantity
  rather than noise (§3); PD-circularity agreed (§5, §7(a)).
- **v1 -> v2** (CC, mechanical follow-through): header and launch-rule lines added, matching
  brief 1; runtime estimate note added for the two-dt cost (§9); no v1 sweep was run for step 2,
  so no discard note is needed.
- **v2, addendum** (2026-09-17, CC): §6 gains a note that controls follow checklist rule 17,
  added after step 1's copy-fidelity gate stopped twice falsely (exact equality, then one
  quantisation step over a 10-pair floor; Ark 20:23Z, Zcode 20:24Z) — any copy of flyvis code is
  gated by a code diff, numeric reproducibility is recorded with stops only on documented
  ceilings derived from ≥ 2 processes, and no control compares one realisation with an extremum
  of another. No other change.
- **Pre-launch gate audit, 2026-09-17 UTC (2026-09-18 local), CC — recorded, nothing in the
  readings changed by it.** Run on Mike's word to do the plan's item D
  (`docs/plans/2026-09-17-endpoint-before-n.md` §3 item 6), because checklist rule 17 requires the
  gates to be checked before a launch word is sought, not after it. Four findings, in the order
  that matters:
  1. **§6's controls pass rule 17.** P0 reports `max |delta|` with no threshold (`:76`), P0-bis
     states "No gate pre-set" (`:77`), and the v2 addendum routes code identity to a diff and any
     ceiling to ≥ 2 processes (`:80-83`). This is the lesson of step 1's three false stops,
     applied. Nothing to fix here.
  2. **Reading (b)'s bins carry no derivation.** The outcomes `≤ 3 / ≥ 30 / between` (`:87`) come
     from `docs/plans/2026-09-16-functional-readout-plan.md:71` — "as in Ark's design" — and
     neither file states what the two numbers prove, over how many realisations they were set,
     what margin they carry, or the probability that a correct implementation lands in the wrong
     bin. Rule 17(a)/(b)/(d) asks for exactly those. The gap is sharper than usual here because
     this brief itself records that the underlying quantity's own reproducibility is unmeasured:
     "*What the literature-comparison functions return for an untrained vs a trained net: TO BE
     MEASURED. The flyvis source states no range and nothing has been run*" (`:79`). A rank-bin
     boundary set before the instrument's noise on that quantity is known is a number without a
     floor under it. **This is the reading's author's call, not the auditor's** — either a stated
     derivation or an explicit deferral (bins reported descriptively, decided after P0/P0-bis
     measure the tuning quantity's own spread). No bin is changed here.
  3. **Reading (b)'s premise for seed 2 has been overtaken by step 1.** The dominant type is
     selected by ablation-delta magnitude, and seed 2's entry is `R2 +21157.5` (`:87`). Step 1
     concluded that this delta measures "the dynamics' fragility to a zero clamp specifically, an
     instrument artefact, not a vision dependence"
     (`results/diagnostics/gray/README.md:204-208`, commit `32759e2`; summarised in
     `ROADMAP.md`). So for seed 2 the selector is known to be contaminated: the type was chosen by
     a number that is now attributed to the apparatus. Recorded as an override above the reading,
     per checklist rule 16's convention, and not edited into `:87`.
  4. **Reading (b) is not independent of the Mi4/CT1 control, and that is an ordering fact.**
     The same reading names `Mi4` (seed 3, +4827.5) and `CT1(Lo1)` (seed 4, +10460.9) as dominant
     types by the same selector. Whether that dominance is a property of the flies or of the
     forced-zero clamp is precisely what the control owed for those two types asks
     (`docs/plans/2026-09-17-endpoint-before-n.md` §3 item 6; brief drafted 2026-09-17). If that
     control finds the same artefact, reading (b) is measuring the tuning of types selected by an
     instrument effect for all three seeds, not one. That makes reading (b) **downstream of the
     control**, where the plan currently lists the two as independent. Stated here as a
     consequence for the order of work; the plan's own wording is the plan's to change.

  Also noted: this addendum's own v2 entry (2026-09-17, CC) carries no dated reviewer pass from
  Ark or Zcode, unlike every earlier revision in this file and unlike the sibling diagnostics
  (`results/diagnostics/c3/README.md:6`, `results/diagnostics/gray/README.md:9`). The standing
  rule is that every brief is reviewed before launch; that pass is owed on the addendum and on
  this note.
