---
project: connectome-seed
entry_level: h3
status_machine: v1
language_cutoff: 2026-09-13
---

# connectome-seed Backlog

> Mike decides. CC executes. Ark, Johnny and Warren review.
> Direction lives in `VISION.md`, the order of work in `ROADMAP.md`, the decisions in
> `docs/decisions/`. Format and validator: dpc-messenger `docs/BACKLOG_FORMAT.md`; check and rebuild
> the views from the dpc-messenger checkout with the path given explicitly and `--out` set to
> this directory. The `axis:` vocabulary (collective / knowledge / network / honesty / reach)
> is dpc-messenger's, adopted as-is because the checker is shared.

## OPEN



### THE-INSTRUMENTS-WERE-AUDITED-THE-DAY-THEY-WERE-BUILT-AND-NINETEEN-FIXES-WAIT-ON-MIKES-WORD: the code audit of the diagnostics found witnesses that cannot veto, constants never checked against the pre-registration and an undocumented null-draw rule, and nineteen fixes with falsifiers wait on Mike's word to fix the tools (HIGH, open, 2026-09-15 — Ark 08:42/08:45/09:39/09:51, Zcode 09:04, CC; consolidated `docs/tool-hardening-package.md`; Mike's word «чини инструменты»)

- **Observed.** `docs/tool-hardening-package.md` (19 items): tier A, before the first analysis
  of night 3 — items 1, 2, 15, 16 (the seven `eval_rung` invariants into every evaluation json;
  a lattice-derived hook/per-item tolerance; a failed invariant sets `exit =
  "state_check_failed"` instead of staying `"ok"`; an idempotence control of the evaluator);
  tier B, before the new pre-registration — items 3a/3b (`--check-constants` against the
  pre-registration; no numbers in identifier names), 4–14 (connectome-checked module grouping,
  a scaled null beside the isotropic one, P0/P1/self-path as asserts, noise-band and state
  labels on every output, script-hash provenance, one evaluation entry point, the null-draw
  rule registered before any draw, duplicate-key refusal, per-metric-per-state floors, a paired
  re-draw for clamp censoring), 17 (preflight for a pending reboot / free VRAM), 19 (a
  provenance field for any quantity that crossed more than one formatter); tier C, before night
  3 — nothing, night 3 runs the current script unchanged. Source: 002 §5h code audit (Mike's
  question 08:40; Ark 08:42/08:45; CC's Explore agent on Sonnet; verified by CC), extended
  09:04–09:51 with items 14–19 and rules R1–R4. Item numbering: item 18 (the base-rate check)
  was folded into rule R2 when rules were separated from fixes; the gap is deliberate.
- **Inferred.** None of the 19 items recomputes a recorded number — only item 14's null
  calibration is re-run once, a second line beside the first; every falsifier is stated as a
  concrete test that fails today and must pass after the fix.
- **First step.** Mike's word «чини инструменты», then tier A (items 1 and 15 are tested
  together by one test; item 16 needs a purpose-built fixture); items 5 and 13 are
  design-first, not one-line changes. See
  [[THE-COMPOSITION-MARGIN-OVER-ITS-FLOOR-IS-SMALLER-THAN-A-NULL-SHIFTS-MEDIAN-DELTA]] (the (a)
  reading items 5/11 answer) and
  [[WINDOWS-UPDATE-RESTARTS-INSIDE-THE-NIGHT-WINDOW-BECAUSE-ACTIVE-HOURS-END-AT-0600]] (item
  17).
- **axis:** honesty

### DATAMATE-UNLINKS-AN-OPEN-HDF5-FILE-AND-WINDOWS-REFUSES: flyvis does not build its connectome on Windows because its storage layer deletes a file while an h5py handle is still open (MEDIUM, open, 2026-09-13 — found by CC while verifying the flow)

- **Observed.** `datamate/io.py`, `_write_h5`: `h5.File(path, mode="w")` is opened, the
  `except` branch runs while that handle is live, and `path.unlink()` raises `WinError 32`.
  The same shape sits in `_extend_h5`. `HDF5_USE_FILE_LOCKING=FALSE` changes nothing — it is
  not a locking problem. A close-before-unlink patch in both functions makes `Network()` build.
  `datamate` is a separate package (v1.0.0) under the same GitHub organisation as flyvis
  (`github.com/flyvis/datamate`) — Ark's point that it is a third-party dependency stands, and
  so does the consequence that a local patch breaks on upgrade.
- **First step.** Keep the patch in the scratch environment for the test; open an upstream
  issue or PR at `flyvis/datamate` with the two-line fix so the next install does not need it.
  Not before the test — the patch is not on the critical path once it holds.
- **axis:** honesty, reach

### THIRTEEN-LINKS-POINT-INTO-A-DIRECTORY-THAT-WILL-NOT-BE-PUSHED: README, literature and idea link into chat/, which is ignored from history, so every one of them resolves to nothing on GitHub (MEDIUM, open, 2026-09-13 — consequence of Mike's «chat/ в gitignore», 06:50 UTC)

- **Observed.** Counted before the first commit: README 8 distinct links, `literature.md` 4,
  `idea.md` 1. All of the form `chat/NN-name-hhmmss.md`. `chat/` is excluded by `.gitignore`
  from `8695d26`.
- **First step.** Replace each with a plain attribution — name, role, date, UTC — which is what
  the README already carries in prose; the information survives, the link does not. Mechanical;
  done in the same pass as the LICENSE and the translation. Child of [[ADR-001]].
- **axis:** reach

### EIGHT-PROCESSES-SHARE-THE-CARD-NO-FASTER-THAN-ONE: aggregate throughput saturates near 17.5 it/s whatever the process count, so only fewer kernel launches per iteration can shorten a night (MEDIUM, open, 2026-09-13 — CC, from the concurrency measurement committed in e797f02)

- **Observed.** Per process 0.0619 / 0.228 / 0.450 s/iter at k = 1 / 4 / 8; aggregate
  ≈ 17.5 it/s at every k; `Compute Mode: Default`, no MPS on Windows (sources: scratchpad
  `flyvis-probe/gpu_concb_*`, via `gpu_concb_analyze.py`; pre-registration §4, m = 1 fixed).
  3,104 kernel launches per iteration and GPU busy 45 % single-process — CC, 2026-09-13,
  not yet in a committed log.
- **Observed, batching proxy (2026-09-13).** Batch 4 / 8 / 16 in one process → 0.0654 /
  0.1215 / 0.2261 s/iter, 240 iterations each (`flyvis-probe/gpu_batch_9987_000..002.json`):
  3.46× the time for 4× the samples, a 16 % per-sample gain and no more. Batch 24 and 32 fail
  before the first iteration on flyvis's 16-sequence validation split (`RuntimeError: size of
  tensor a (32) must match … (16)`; `gpu_batch_9987_003/004.json`, `iteration_after: 0`).
  flyvis trains ensembles one process per member (`compute_cloud_utils.py:427-449`); no
  `vmap` / `functional_call` anywhere in the package. From both sides — processes and batch —
  the card's ceiling is ≈ 65–70 stimulus-samples/s.
- **Observed, extent 5 (2026-09-13).** `extent_probe/ext5_9986-*.json` against
  `ext15_9985-*.json`, 1,008 iterations × 4 runs per extent: extent 5 = 5,759 nodes /
  171,471 edges and still 734 free parameters (65 types, 604 pairs, none missing);
  0.0443 vs 0.0648 s/iter → 1.46× (3.08 h vs 4.50 h per run); GPU util 18–25 % at extent 5
  against 62–71 % at extent 15 — a fixed ≈ 40 ms per iteration (the 40-step Python loop,
  ~3,100 launches) that does not shrink with the lattice. Seeds spread on both extents at
  1,000 iterations (sd 0.29 / 0.52) against a replicate difference of 1–2e-5 (determinism
  off). Decision (CC's recommendation, sent 17:50 UTC; the ≥ 3× condition not met): the night
  stays on extent 15, extent 5 not adopted.
- **Inferred.** The one lever left is the fixed ≈ 40 ms: CUDA graphs or `torch.compile`
  around the simulation loop — up to ~1.6× at extent 15, ~3× at extent 5. Not before run 0:
  the change needs a control, and run 0 is that control.
- **First step.** After run 0, a 1,000-iteration CUDA-graph prototype compared to run 0's
  hook trajectory. See also [[HOW-MANY-FULL-RUNS-THE-TEST-IS-ALLOWED]], closed 2026-09-13 —
  this measurement is what bounds N per night.
- **axis:** knowledge


### THE-NIGHT-TOOLING-LIVES-IN-A-TEMPORARY-SCRATCHPAD: the runner, the launcher and the patched environment sit in a session temp directory that nothing in the repository points at, and the venv cannot be moved (HIGH, open, 2026-09-14 — CC, on finishing the night tooling; instructions sent 2026-09-13 17:55 UTC)

- **Observed.** `flyvis-probe/night/run_individual.py`, `launch_wave.py`, `start_night.ps1`
  and the environment `flyvis-probe/.venv` (torch 2.9.1+cu128, flyvis 1.2.0, datamate with
  the close-before-unlink patch) are all under `AppData/Local/Temp/claude/…/scratchpad/`;
  the repository holds none of them; a uv venv is not relocatable.
- **Observed 2026-09-14.** Scripts copied to `tools/night/` in commit (this commit); the
  venv recipe still to be documented.
- **Observed 2026-09-14 (this commit).** Scripts and recipe now in `tools/night/`:
  `run_individual.py`, `launch_wave.py`, `start_night.ps1` (with the new `-NoReplicate`
  switch), `night_report.py`, and `tools/night/README.md` (python/torch/flyvis/datamate
  versions, the datamate Windows patch extracted from the live venv's `io.py`,
  `FLYVIS_ROOT_DIR`, both launch commands). Remaining: re-create the venv outside the
  scratchpad from that recipe.
- **Inferred.** The night can run from there once. The next night cannot if the scratchpad
  is gone, and the datamate patch goes with it —
  [[DATAMATE-UNLINKS-AN-OPEN-HDF5-FILE-AND-WINDOWS-REFUSES]].
- **First step.** After the night, on Mike's word: copy `night/` into the repository as
  `tools/night/` (scripts only, no logs); write the venv recipe beside them (uv venv, torch
  2.9.1+cu128, flyvis 1.2.0, the datamate patch); re-create the environment outside the
  scratchpad and re-patch it; one 24-iteration dry run from the new location.
- **2026-09-15, CC:** Night 3 (2026-09-15) again runs from the scratchpad copy (.../63f3961a-.../scratchpad/flyvis-probe/, per docs/next-session-plan.md §2); venv and scripts verified present and byte-identical to tools/night/ for the three executed files (run_individual.py, launch_wave.py, start_night.ps1); the migration per tools/night/README.md is scheduled after night 3, not before -- a pause costs more than the risk tonight (Ark 10:00); the two open entries about the night killing itself (this one and [[WINDOWS-UPDATE-RESTARTS-INSIDE-THE-NIGHT-WINDOW-BECAUSE-ACTIVE-HOURS-END-AT-0600]]) are both live tonight.
- **2026-09-17 UTC (2026-09-18 local), CC:** Still unmigrated. Night 3 and night 4 both ran off the same scratchpad copy: `results/night3/README.md:51` and `results/night4/README.md:61` each set `RAW` to `.../63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/night`. The C3 diagnostic (2026-09-17) ran the same way: `results/diagnostics/c3/README.md:39` and `:97` write its netdir roots and A0-smoke output under `<scratchpad>`. The machine-state patch (commit `4f1b30c`, 2026-09-17) was verified against the scratchpad copy too -- its commit message: "the patched file's sha256 matches between the repo and the scratchpad night dir." The venv has still not been re-created outside the scratchpad.
- **2026-09-18, CC — "a uv venv is not relocatable" is half true, and the half that matters here is false.** The venv was copied to `tools/.venv` and hashed against the original: 21,650 files each with `__pycache__` excluded, combined sha256 `94f7f483e8410e54887c98b20d520872823f1ba5ad9fa1c12d6b95359da7e318` on both sides, zero differing and zero present on one side only. From the new path `python.exe` runs, `import flyvis, datamate, torch` succeeds, `torch.cuda.is_available()` is `True`, and `start_night.ps1 -DryRun` reaches the launcher — so the night path, which invokes `python.exe <script>` and never a console entry point, is unaffected by the move. What genuinely does not relocate is the `Scripts\*.exe` layer: `flyvis.exe` carries the literal string `...\63f3961a-...\scratchpad\flyvis-probe\.venv\Scripts\python.exe` inside the binary, and it ran during the check **only because that path still exists**. The 2026-09-14 claim was written without a measurement behind it and was too strong; the accurate form is that the entry-point executables are not relocatable and the interpreter is. There is also no `pip` in this venv at all — uv creates it without one — so "re-create and re-patch from the recipe" was never going to be a `pip install` either way.
- **Residual risk, named because the copy does not remove it.** Once the scratchpad is deleted, every `Scripts\*.exe` in the copy becomes a broken stub pointing at a directory that no longer exists. Nothing in the night path calls them, so no night breaks; a person who types `flyvis …` gets a failure whose message names a temp directory and explains nothing. Either re-create the venv from `tools/night/README.md` at leisure, or leave the stubs and know why they fail. See [[THE-ONLY-RUNNABLE-ENVIRONMENT-LIVES-IN-A-SCRATCHPAD-OF-A-SESSION-THAT-HAS-ENDED]] for the move itself.
- **axis:** collective

### FLYVIS-RESUME-AND-RECOVER-ARE-BROKEN-IN-1-2-0: five defects found by execution in the installed flyvis stand between anyone and a resumed run, and none of them is reported upstream (MEDIUM, open, 2026-09-14 — CC, from the interrupt-and-resume test of 2026-09-13)

- **Observed.** `night/resA_9989-000.json` and `night/resA_9989-000.resume2.stdout.log`
  (scratchpad): (1) `solver.recover()` cannot run — `resolve_checkpoints` signature
  `TypeError` at `solver.py:598`; (2) datamate refuses to re-open a NetworkDir
  (`FileExistsError` on `delete_if_exists`); (3) the checkpoint stores `iteration − 1`, so a
  48-iteration budget ran to 59; (4) no RNG or data-order state is saved — the first 12
  post-resume losses correlate 1.0000 with epoch 0's; (5) a penalty optimizer key mismatch
  (`activity_optim` vs `penalty_optims`) leaves it unrecovered. A sixth is already on the
  board: [[DATAMATE-UNLINKS-AN-OPEN-HDF5-FILE-AND-WINDOWS-REFUSES]].
- **Inferred.** The consequence for this test is registered: §7 counts an interrupted run
  as failed ([[RESUME-OF-AN-INTERRUPTED-RUN-IS-UNVALIDATED]], closed 2026-09-13). Upstream
  fixes would not change that rule; they change what the next user of flyvis 1.2.0 inherits.
- **First step.** On Mike's word, an upstream issue at `flyvis/flyvis` with the
  48-iteration minimal reproduction; until then the §7 rule stands.
- **axis:** knowledge


### WINDOWS-UPDATE-RESTARTS-INSIDE-THE-NIGHT-WINDOW-BECAUSE-ACTIVE-HOURS-END-AT-0600: a planned Windows Update restart killed seed 2 mid-run because active hours end at 06:00 while the night window runs to 11:30, and the launcher has no preflight for a pending reboot (HIGH, open, 2026-09-15 — CC, from the KB5129195 restart during night 2)

- **Observed.** System event log: "2026-09 Security Update (KB5129195)" (build 26200.9457)
  download started 02:33 local 2026-09-15, "Installation Started" 03:10:53 local, three planned
  restarts at 06:29:19 / 06:30:20 / 06:31:05 local (23:29Z–23:31Z 2026-09-14), two logged as
  User32 1074 "TrustedInstaller.exe … on behalf of NT AUTHORITY\SYSTEM … Operating System:
  Upgrade (Planned) 0x80020003", "Installation Successful" 06:33:45 local; no Kernel-Power 41 /
  6008 / 1001 — not a crash or power loss. Active hours on this machine are 12:00–06:00 local
  (`HKLM\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings`), so 06:29 was the first minute Windows
  was allowed to restart. Edition: Windows 11 Home (EditionID Core) — no gpedit, no
  WindowsUpdate policy keys exist.
- **Inferred.** The night window (02:00–11:30 local, per the tooling) runs five and a half
  hours past the end of active hours (06:00 local); nothing in `start_night.ps1` checks for a
  pending reboot or otherwise defends the run against an automatic restart. Follow-up to
  [[NIGHT-2-RUNS-SEEDS-1-AND-2-ON-MIKES-WORD]] — this restart is what killed its seed 2 run at
  iteration 12,700.
- **First step.** Mike chooses the protection: pause updates before each night, shift active
  hours to cover 02:00–11:30, or a policy value if one is documented for Home (the orchestrator
  is checking Microsoft's documentation now). Then `start_night.ps1` gets a preflight that
  refuses to launch when `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto
  Update\RebootRequired` or `…\Component Based Servicing\RebootPending` exists.
- **Observed, 2026-09-15 (CC).** The preflight fix is now item 17 of
  `docs/tool-hardening-package.md` (tier B, before the new pre-registration): refuse to launch
  on a pending reboot or insufficient free VRAM, falsifier — create the `RebootRequired` key in
  a test hive → `start_night.ps1` must refuse; today it launches. Execution waits on Mike's word
  «чини инструменты» —
  [[THE-INSTRUMENTS-WERE-AUDITED-THE-DAY-THEY-WERE-BUILT-AND-NINETEEN-FIXES-WAIT-ON-MIKES-WORD]].
- **axis:** collective

### THE-TUNING-BATTERY-CHECKS-WHETHER-THE-DOMINANT-ABLATION-TYPE-IS-FUNCTIONAL: flash and moving-edge tuning per cell type, compared against Maisak 2013, will show whether seed 2's R2, seed 3's Mi4 and seed 4's CT1 differ in tuning from the same type in the other five runs (HIGH, open, 2026-09-16 — CC, docs/plans/2026-09-16-functional-readout-plan.md step 2)

- **Observed.** `docs/experiments/003-night3-seeds-3-and-4.md` §6 item 2: each of the six runs
  has one cell type that dominates its own ablation profile (Tm5c / Mi4 / TmY15 / R2 / Mi4 /
  CT1(Lo1) for seeds 0/0′/1/2/3/4), and the dominant type differs run to run — "the type that
  blows up is different in every run that has one" (ablation README §5).
- **Inferred.** Whether the dominant type is doing anything *functionally* distinctive (its
  ON/OFF flash-response index or DSI/preferred direction, against the same type in the other
  five runs and against the literature) is a separate question from whether it dominates the
  ablation loss, and is untested.
- **First step.** CC's subagent computes, per seed at 250,008 and at iteration 0: flash-response
  index and DSI/preferred direction per type (65), using flyvis's own functions; brief reviewed
  by Ark and Zcode before launch, readings (a)–(d) of the plan fixed before data (twin trap in
  tuning space; dominant-type deviation ranked among 65, outcomes ≤3 / ≥30 / between;
  literature-polarity count per fly; iteration-0 as the null). All diagnostics, not tests.
- **2026-09-17 UTC (2026-09-18 local), CC:** Unblocked. Step 1 (gray stimulus) closed 2026-09-17, commit `32759e2` —
  see [[THE-GRAY-STIMULUS-CONTROL-TESTS-LEARNED-EQUALS-VISION-FROM-THE-SECOND-SIDE]] in
  `backlog_closed.md` — so this step's own prerequisite ("waits on step 1",
  `docs/briefs/2026-09-16-step2-tuning-battery.md`) is satisfied. The brief is ready; the launch
  itself still waits on the owner's word.
- **axis:** knowledge

### THE-GENOME-DESIGN-AROUND-S2-NEEDS-LABEL-PROVENANCE-BEFORE-EXTRACTION: Ark's design around S2 and CC's two-page "what is the genome here" note are the prerequisite for extracting the label array and rule bank (HIGH, open, 2026-09-16 — CC, docs/plans/2026-09-16-functional-readout-plan.md step 3)

- **Observed.** No design for the genome track exists yet beyond the plan's naming of it; the
  plan assigns provenance of the `groundtruth_utils` fields and the design rewrite around S2 to
  Ark, and a two-page "what is the genome here" note with source addresses to CC, written after
  Ark's design lands. Zcode owns the C6 control specification for the same track.
- **Inferred.** CC cannot extract the label array or the rule bank before Ark hands over the
  field list — the step is ordered, not parallel with its own prerequisite.
- **First step.** Ark writes the design around S2 with label provenance; CC extracts the label
  array and rule bank as soon as the field list is handed over, then writes the two-page note.
- **axis:** knowledge

### THE-LEARNED-GAIN-IS-SIXTY-LOSS-UNITS-ON-AN-UNTRAINED-LEVEL-OF-TWELVE-HUNDRED: rescaling the replicate difference and the between-seed sigma onto the learned-gain axis gives 21% and 6% respectively, a candidate basis for the next registration (HIGH, open, 2026-09-16 — CC, docs/experiments/003-night3-seeds-3-and-4.md §6c)

- **Observed.** `docs/experiments/003-night3-seeds-3-and-4.md` §6c: untrained held-out loss
  ≈1212.55 across six seeds, checkpoint-250,008 loss 1144.64–1160.98 → a learned gain of ≈60
  loss units. On that scale the twin replicate difference (12.73) is 21% and the between-seed σ
  at n=5 (3.54) is 6%.
- **Inferred.** This is a proposal for how a future pre-registration might state its tolerance
  (as a fraction of the learned gain rather than of the raw loss), not a re-reading of the
  existing one — §7's tolerance and its FAIL stand exactly as written and are not revisited by
  this observation.
- **First step.** Mike + reviewers decide, at the next pre-registration, whether a
  learned-gain-relative tolerance replaces or supplements the current raw-loss one.
- **axis:** honesty

### MACHINE-STATE-WAS-ADDED-TO-THE-RUN-JSON-BUT-NEVER-EXERCISED-BY-A-RUN: a machine-state snapshot field landed in the night runner on 2026-09-17, after night 4 had already finished, and no run or diagnostic since has taken that code path (MEDIUM, open, 2026-09-17 — CC, from commit 4f1b30c and a grep of the four completed nights)

- **Observed.** Commit `4f1b30c` (2026-09-17T08:38:54Z UTC) adds two call sites to
  `tools/night/run_individual.py`: `rec["machine_state_start"] = _machine_state()` at line 699,
  before the training reseed and the wall-clock start, and `rec["machine_state_end"] =
  _machine_state()` at line 749, inside the existing `finally:` block.
- **Observed.** No json under `results/night1`, `results/night2`, `results/night3` or
  `results/night4` contains the string `machine_state` — all four completed nights predate the
  patch.
- **Observed.** Step 1 (gray stimulus, commit `32759e2`, same day) ran through
  `results/diagnostics/gray/gray_stimulus.py`, which imports `diag1_eval_paths`, `ablation` and
  `rowB` (`gray_stimulus.py:127-129`) and does not import `run_individual` — step 1 never took
  the patched code path either.
- **Observed.** `4f1b30c` landed 2026-09-17T08:38:54Z (UTC); night 4's last commit `f3b02e2` was
  2026-09-17T05:56:41Z (UTC) — the patch landed after night 4 had already finished and been
  recorded, not before it.
- **Observed.** `results/diagnostics/c3/machine_state.json` is a separate artefact — the C3
  diagnostic's own 5-record machine-state log (`results/diagnostics/c3/README.md:27`: "5 records:
  start, after B, before A1, after A1/before B′, end"), written by that diagnostic's own harness,
  not by the `rec["machine_state_start"/"_end"]` field this entry is about.
- **Inferred.** The commit's own verification (git apply, py_compile, parse_args byte-identity, a
  standalone `_machine_state()` call) checks the patch statically; none of it exercises the field
  inside an actual training run. The field's first real exercise is whatever night run comes next.
- **First step.** The next night run will be the first to carry `machine_state_start` and
  `machine_state_end` in its json; check their presence and shape then.
- **axis:** honesty

### THE-POINT-STATISTICS-RHO-PREVIEW-AT-N-EQUALS-SIX-MUST-NOT-BE-CITED-AS-THE-TEST: the 0.8857 rank correlation between the C3 point statistic and the 250,000 hook at n=6 is a preview of the registered (b) test taken before N is chosen and rests on one pair, and any citation of it must carry that label (MEDIUM, open, 2026-09-17 — CC, from commit a7233dc and Ark/Zcode's confirmation)

- **Observed.** Commit `a7233dc` records Ark's (chat 2026-09-17 08:51:11Z) and Zcode's
  (08:52:47Z) confirmed reading of the ρ = 0.8857 point-statistic value reported in
  `results/diagnostics/window/README.md` §4: "a preview of the registered (b) test at n=6, before
  N is chosen, not a test and not a decision by itself — the registered test is read once at the
  final N with that N's own critical value" (`results/diagnostics/window/README.md:164-166`).
- **Observed.** The value rests on one pair: swapping the ranks of seeds 4 and 5 drops it to
  ρ = 0.714, below the n=6 critical value 0.829 (`results/diagnostics/window/README.md:167-171`).
- **Observed.** The label sits at the source — boxed directly under the ρ table in §4 of
  `results/diagnostics/window/README.md` (lines 164-171) — and is not restated anywhere else in
  that file or in `ROADMAP.md`.
- **Inferred.** The registered (b)/b2 test is defined at C3 with its own N rule and Holm
  correction (`docs/preregistration-cheap-vs-expensive.md`), and is read once, at the final N —
  it is not re-run at n=6. Any future citation of 0.8857 (or the 0.714 swap) outside its labelled
  source must carry the same preview caveat, not be presented as an interim reading of (b) or b2.
- **First step.** None scheduled; this entry is a standing caution against citing the number
  bare. It closes only when superseded by the registered N reading itself, or folded verbatim
  into a future registration's own text.
- **axis:** honesty

### A-REACHABILITY-ENDPOINT-IS-PROPOSED-AND-NOT-REGISTERED-WHILE-ITS-SUBSTRATE-ALREADY-SITS-ON-DISK: iterations-to-cross a fixed aggregate val_loss level is proposed as the endpoint class that survives run-to-run scatter, the 72-checkpoint curves of all eight runs are already stored, and nothing about it is pre-registered (HIGH, open, 2026-09-17 — CC, from the 2026-09-17 USPEX review thread; drafting assigned to Zcode)

- **Observed.** The USPEX statistic our own (b) test was compared against counts **steps to a target fixed outside the run** (generations and structures to `E = 90.912`), not the order of final states — `research/uspex/2026-09-17-uspex-analogue-to-adr-002.md` §(b)1, §(c)4. Run-to-run scatter moves a time-to-target and destroys an order of finals.
- **Observed.** The substrate is already stored, so the test costs no GPU and no night: 72 aggregate `val_loss` checkpoints per run for all eight runs, on a grid that is **not uniform** — iterations 0, 12, then 3,600 apart, with a final step of 1,596 to 250,008 (`results/night4/night_report_checkpoints.csv`).
- **Observed.** The curve is a **different field** from the 250,000 hook and its replicate gaps are its own: at 250,008 the curve gives `0′ − 0 = 12.1749` and `3′ − 3 = 7.6059` against the hook's 12.7279 and 10.4309, with a trained spread of 18.7403 (same file; recomputed by CC 2026-09-17 UTC from the stored values).
- **Observed.** A positive control exists in the same table: the untrained level is 1212.5556 and the learned gain within the curve field is 63.7481 for seed 0 — about five times the largest replicate gap.
- **Inferred.** Because §(c)1a leaves the cost of N unestimable (the moment estimate of the between-individual variance is negative), this free test is the only step that can settle the **class** of the endpoint before any night is bought. It is a recommendation of the review thread, **not a decision**: no rule changes until it is registered and read.
- **First step.** Zcode drafts the registration in the repository's style — threshold grid stated as a rule, acceptance criterion in one sentence, the measured resolution, a disqualification clause for the case where the replicate difference is ≲ one grid step, the positive control above, the field named, and the inherited item-weighting fragility — per `docs/plans/2026-09-17-endpoint-before-n.md` §4; Ark and CC review it **before any data is touched**.
- **axis:** knowledge

## IN PROGRESS

### THE-ONLY-RUNNABLE-ENVIRONMENT-LIVES-IN-A-SCRATCHPAD-OF-A-SESSION-THAT-HAS-ENDED: every night since 2026-09-13 ran from a venv under a temporary per-session directory whose owning session is gone, and the repository's own copy of the launcher cannot start a night at all (HIGH, in progress, 2026-09-17 — Mike «Переезд — надо сделать обязательно, заведи таску HIGH в новой сесси с него начнем потом»; raised by Ark, confirmed by CC)

- **Observed.** All nine job records across the five wave files name one interpreter and one script copy, under `%LOCALAPPDATA%\Temp\claude\c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx\63f3961a-96ce-4048-8338-72c162ea66f8\scratchpadlyvis-probe\` (Ark, 2026-09-17, from `results/night{1,2,3,4}/wave_*.json`). That session id is **not** the session running today, so the directory has no owner: nothing refreshes it, and any cleanup of stale per-session scratchpads takes the project's only venv with it (CC, 2026-09-17).
- **Observed.** The copy has not drifted: `run_individual.py`, `launch_wave.py` and `start_night.ps1` are byte-identical between `tools/night/` and that scratchpad (sha256 `be007c74…`, `ad206bd8…`, `117379c8…`; CC, 2026-09-17). The risk is disappearance, not divergence.
- **Observed.** The repository copy cannot launch a night as it stands. `start_night.ps1:46` derives the interpreter as `Split-Path -Parent $PSScriptRoot` + `.venv\Scripts\python.exe` — from `tools/night/` that is `tools/.venv`, which does not exist — and `:56` throws `venv python not found: $py`. `launch_wave.py:35` has the same broken default but `:77` accepts `--python`, so that one file is usable when the interpreter is passed explicitly: the default is broken, not the capability (CC, 2026-09-17).
- **Inferred.** A migration that moves only the venv and leaves the launcher deriving its interpreter from the script's parent directory exchanges one orphaned directory for another. The move and a launcher that runs from the repository are one task, not two (Ark, 2026-09-17).
- **Done, 2026-09-18 (CC).** The environment was copied out of the ended session's scratchpad into `tools/.venv` — 25,221 files, 4.85 GiB, robocopy reporting 0 failures — and answers from its new path: `python 3.10.20`, `torch 2.9.1+cu128` with `torch.cuda.is_available() == True`, `flyvis 1.2.0`. No launcher change was needed after all: `start_night.ps1:43-46` derives the interpreter as the script's parent plus `.venv\Scripts\python.exe`, which from the committed `tools/night/` is exactly `tools/.venv`, so putting the venv at that path makes the existing derivation correct instead of broken. Ark's "the move and a launcher that runs from the repository are one task" holds, and the cheaper half of it turned out to be a copy to the right place rather than a new `--python` argument.
- **Done, 2026-09-18 (CC).** `tools\night\start_night.ps1 -DryRun -Tag night5 -Ensemble 9992 -Seeds "3,0" -NoReplicate`, run **from the repository**, reaches the launcher and prints its two jobs (`9992/003` seed 3 first, `9992/000` seed 0 second, both tag `night5`) and `[dry] 2 commands; mode=sequential; detach=True; nothing started`. This is the first time the committed copy has been shown to start a night; before it, it threw at `:56` before reaching the launcher.
- **Observed, 2026-09-18 (CC).** The move changes where a night's raw output lands: `--out-dir` is the launcher's own directory and `start_night.ps1` never overrides it, so night 5 onward writes its per-run json/log/stdout triples and the wave's pid/progress/launcher files **into `tools/night/` inside the repository**, where nights 1-4 wrote into the scratchpad. Ignore rules were added for exactly those names (`tools/night/*.json`, `tools/night/*.log`, `tools/night/wave_*.pid`) and verified with `git check-ignore` against the seven filenames night 5 will write, because a wave in flight would otherwise leave the tree dirty — the state a pre-registration's own guard refuses to run in. Nothing of that shape has ever been in history; the committed trace stays the distilled `results/night*/`.
- **Observed, 2026-09-18 (CC).** A copy is an assumption until it is hashed, so both trees were hashed file by file (sha256, `__pycache__` excluded) and compared by a combined digest over the sorted (path, hash) pairs. **Result: identical** — 21,650 files on each side with `__pycache__` excluded, combined digest `94f7f483e8410e54887c98b20d520872823f1ba5ad9fa1c12d6b95359da7e318` on both, zero files differing and zero present in one tree only. The requirement now lives as a gate in `docs/briefs/2026-09-17-night5.md` §4 gate 8: if the digests ever disagree, night 5's curves are not comparable to nights 1-4's.
- **Still open.** Ark's acceptance condition is unmet by construction: it requires a **full run's** `json_iter_wall_median_all_s` to land inside **[0.0598, 0.0622]**, which no dry run can supply. The entry stays open until a night has run from `tools/.venv` and its timing gates are read (night 5's §4 gate 4 is the instrument). Also unresolved: the scratchpad copy is still the only place nights 1-4's raw artefacts exist, and deleting it is a separate decision from moving the environment.
- **First step.** Give the environment a home outside `Temp` and outside any session-scoped path; make `start_night.ps1` accept an explicit interpreter path (or resolve one that exists in the repository layout); then re-verify with `-DryRun` from the repository copy, and accept the move only if a full run's `json_iter_wall_median_all_s` stays inside **[0.0598, 0.0622]** — the band of all eight runs on record, spread 4.10 % across four days and one restart (Ark, 2026-09-17). Mike's word: start the next session with this.
- **axis:** collective



## BLOCKED ON DECISION


### THE-SPREAD-REPLICATE-RATIO-INVERTS-BETWEEN-C3-AND-THE-TOP-RUNG: the between-seed spread at 250,000 is smaller than the replicate offset while at rung C3 it is larger, so the plan's §3 branch is decidable and waits on Mike + reviewers (HIGH, open, 2026-09-15 — CC, from the night 2 rung SDs and the §7 replicate comparison, 2026-09-15)

- **Observed.** Held-out loss at rungs, seed 0/1/2 (docs/experiments/002-night2-seeds-1-and-2.md, results/night2/): 1,000: 1208.9363/1208.0556/1209.7639; 5,000: 1207.7673/1206.7832/1207.0115; 25,000 (C3): 1191.7375/1190.2235/1204.3618; 250,000: 1146.1958/1145.3572/1148.8000. Sample SD over seeds {0,1,2} (n=3): 0.8543/0.5151/7.7627/1.7953 respectively. Replicate |0′−0| (night 1, docs/experiments/001-run0-and-replicate.md §4): 0.0000/0.0025/0.3365/12.7279. Ratio SD/replicate ≈23 at 25,000 (C3, the primary rung), ≈0.14 at 250,000 — the between-seed spread at 250,000 (1.7953) is about seven times smaller than the replicate difference (12.7279), while at C3 it is about 23 times larger (7.7627 vs 0.3365).
- **Inferred.** n=3 gives an SD with 2 degrees of freedom; the §7 measurability clause is applied once at the registered N, so this is a distance, not a verdict — no rho, no ranks, no call on hypothesis (b)/(b2) yet. What it does settle is the branch itself: docs/next-session-plan.md §3's (a) top rung measurable / (b) not measurable is now decidable with these numbers. See [[NIGHT-2-RUNS-SEEDS-1-AND-2-ON-MIKES-WORD]] (closed) and [[THE-REPLICATE-DIFFERS-BY-ONE-POINT-ONE-PERCENT-AT-THE-TOP-RUNG]].
- **Observed, 2026-09-15 (diagnostics, docs/experiments/002-night2-seeds-1-and-2.md §5b):** the hook-path and stored-checkpoint reporting paths agree to ≈1e-4 at checkpoint 250,008 across all four runs, so the 0.7-2.6 top-rung gap between the two paths (§5a item 10) is weight movement over 8 iterations, not two instruments; evaluation noise on one checkpoint is float-level (max deviation 6.72e-5 across 8 re-evaluations plus the stored value). The run-0/run-0' twin weight-space distance at 250,008 is 4.2372, 0.52 of its own mean parameter norm and about three-quarters of the 0.59-0.78 range separating different-seed pairs at the same iteration; the +12.1749 per-item-mean loss gap between the twins is spread over 14 of 16 held-out items (bandage_1's three items carry 47%, ambush_2's three carry 28%), not concentrated in one outlier item.
- **Observed, 2026-09-17 (C3 diagnostic, results/diagnostics/c3/README.md):** the §4/§7 b2
  measurability threshold at C3 was set from a single replicate pair (0/0′, |Δ| 0.3365 at
  25,000). The second replicate pair does not reproduce it: |3′ − 3| at the 25,000 hook is
  5.1847, ≈ 15× larger (5.1847 / 0.3365 = 15.41), and the neighbouring checkpoint at 25,212 gives
  3′ − 3 = −2.9157 — opposite in sign to the registered +0.3365, and the same sign as
  the 25,000 reading, not a flip between the two checkpoints
  (`docs/experiments/004-night4-replicate-3prime-and-seed-5.md` §4, "The C3 finding"). A third
  throw of seed 3 (run 703) reads close to the replicate and far from the original at the C3 hook:
  (703,3) = −4.7582573890686035, (703,3′) = 0.4264798164367676
  (`results/diagnostics/c3/README.md` §7 reading (f)). So the C3/top-rung inversion this entry
  records is itself measured from a threshold — 0.3365 — that is not stable across replicates of
  the same seed; see `ROADMAP.md:154-160`.
- **First step:** Mike + reviewers read docs/experiments/002-night2-seeds-1-and-2.md and choose branch (a) (continue to the floor N, nights 3-5) or (b) (a new pre-registration for the expensive metric before any further N run) per docs/next-session-plan.md §3.
- **axis:** honesty
- **filed:** CC · 2026-09-15

### THE-COMPOSITION-MARGIN-OVER-ITS-FLOOR-IS-SMALLER-THAN-A-NULL-SHIFTS-MEDIAN-DELTA: the registered (a) splice reads "composes predictably" by a 0.40 margin over a floor borrowed from the replicate difference, while a null shift of the same norm moves the loss further and the reverse splice explodes (HIGH, open, 2026-09-15 — CC, from the splice_a diagnostic and Ark's null-shift calibration, 2026-09-15)

- **Observed.** Registered splice T2_A ← T2_B (B = seed 1, A = seed 0, checkpoint 250,008; docs/experiments/002-night2-seeds-1-and-2.md §5g, results/night2/diagnostics/splice_a/): Δ = +38.579946, 3.3583 % of L_A (1148.8074), 3.3659 % of the pre-registration's literal basis 1146.1958. By docs/preregistration-cheap-vs-expensive.md §5 (a)'s rule (floor 38.18, 5 % bound 57.31 on that basis): 38.18 < 38.58 < 57.31 → "composes predictably for this pair", margin 0.40. Self-splice A←A (the mandatory instrument control) is a no-op, +1.4e-5. A null-shift calibration written before the splice (Ark, chat 07:33) drew 20 isotropic random 26-vectors of the same norm as B−A (r = 0.38185): 4 diverge, the 16 finite |Δ| range 10.70-69.55, mean 44.44, median 46.07 — above the registered splice's own 38.58 — and 10 of 16 sit above the floor 38.18. The reverse splice (A→B) gives Δ = +2029.00 (+177.3 %), outside the registered test.
- **Reported.** Ark's calibration (chat 2026-09-15 07:33) and Zcode's bundling it with the splice run (07:43) were both proposed before the registered splice was evaluated; run order verified by the timestamps inside `splice_a/calibration.json` (07:54:06Z) and `splice_a/splice_result.json` (07:55:37Z).
- **Inferred.** The registered category is recorded as the pre-registration's rule reads it, but the margin above the floor (0.40) is smaller than what a directionless shift of the same size does to the loss on the median draw (46.07) — the floor (3× the replicate difference) was not measured from this operation's own null and may not be the right instrument for it.
- **First step.** Mike + reviewers decide the reading: stands as the rule reads it / relabelled uninformative by the calibration / the floor is re-registered from the operation's own null distribution — a floor measured from the operation's own null needs its own registration, not a retrofit onto this one. See [[THE-SPREAD-REPLICATE-RATIO-INVERTS-BETWEEN-C3-AND-THE-TOP-RUNG]].
- **axis:** honesty
- **filed:** CC · 2026-09-15

### N-EQUALS-EIGHT-IS-BELOW-THE-FILES-OWN-MINIMUM: §4 calls N = 10 the minimum at which the test is meaningful and in the same section lets N fall to 8, where power at a true rho of 0.5 is about a third (MEDIUM, open, 2026-09-13 — Zcode 3.3 and Ark 6, chat; filed by CC)

- **Observed.** `docs/preregistration-cheap-vs-expensive.md` §4: "N = 10 is the minimum at
  which the test is meaningful" and, in the rule, "N is never below 8". With m = 1 measured
  (commit e797f02) the rule yields N = 8 at four nights. Power at true ρ = 0.5: ≈ 32 % at
  N = 8, ≈ 41 % at N = 10 (figures as reported; not recomputed here).
- **Inferred.** At N = 8 the honest registered outcome is `inconclusive — underpowered`
  unless agreement is near-perfect; a floor of 10 costs 11 runs including run 0′, six nights
  at two per night.
- **Reported.** Zcode 3.3, Ark 6.
- **First step.** Mike chooses: floor 10 (11 runs incl. run 0′, six nights) or floor 8 with
  `inconclusive — underpowered` registered as the expected outcome. Parent task
  [[HOW-MANY-FULL-RUNS-THE-TEST-IS-ALLOWED]], closed 2026-09-13; one of the fifteen in
  [[PRE-LAUNCH-EDITS-TO-THE-PRE-REGISTRATION-BEFORE-RUN-0]], closed 2026-09-13.
- **axis:** honesty

### THE-REPLICATE-DIFFERS-BY-ONE-POINT-ONE-PERCENT-AT-THE-TOP-RUNG: seed 0 trained twice (run 0, run 0′) lands 1.11 % apart in held-out loss at iteration 250,000, past this file's own 1 % replicate tolerance (HIGH, open, 2026-09-14 — CC, from run 0 / run 0′ per §7)

- **Observed.** Rung table (run 0 / run 0′ held-out loss): 1,000 → 1208.9363 / 1208.9363
  (|Δ| 0.0000); 5,000 → 1207.7673 / 1207.7698 (0.0025); 25,000 → 1191.7375 / 1192.0739
  (0.3365, rel 2.8e-4); **250,000 → 1146.1958 / 1158.9237 (|Δ| 12.7279, rel 1.1104 % →
  FAIL, §7 tolerance is < 1 %)**. Over the 29 common checkpoints after iteration 150,000,
  run 0′ is above run 0 in 29 of 29; mean (run 0′ − run 0) = +12.64 (min 3.68, max 17.82);
  within-run checkpoint standard deviation 6.02 (run 0) / 3.30 (run 0′); the two replicates
  settle on different plateaus, ≈ 1151.7 vs ≈ 1164.3; divergence visible from roughly
  iteration 60,000. Run 0's own minimum held-out loss is 1141.0463 at iteration 219,612;
  held-out loss rose by +0.11 % (1147.5358 → 1148.8075) over the last 50,000 iterations
  (plateau: |change| < 0.2 %). Full tables:
  `results/night1/night_report.md`, `results/night1/night_report_checkpoints.csv`.
- **Inferred.** The instrument floor of the expensive evaluation is ≈ 1.1 % relative, set
  by trajectory divergence under non-deterministic training (determinism flags off, §7),
  not by single-iteration jitter. Per §7 as written, a rung whose between-seed standard
  deviation does not exceed the replicate difference is reported as *unmeasurable*, not as
  a failure of the surrogate — whether the 250,000 rung is measurable for hypothesis (b)
  depends on the between-seed spread at that iteration, unknown until further seeds run
  there (at iteration 1,000 it was 0.52 across 3 seeds, extent probe — a different
  population, not the N population).
- **First step.** Mike + reviewers decide: proceed as registered (the top rung may come out
  *unmeasurable* rather than a surrogate failure) or write a new pre-registration for the
  expensive metric before the N runs. **Proposed (CC), decision Mike + reviewers:** run
  seeds 1 and 2 to 250,000 next night (≈ 4 h each) to get the first between-seed distances
  at the plateau against the 12.64 mean replicate offset above.
- **Experiment record:** `docs/experiments/001-run0-and-replicate.md`; plan:
  `docs/next-session-plan.md`.
- **2026-09-15, CC:** Night 2 gives the top-rung between-seed distances: seed 0/1/2 held-out loss at 250,000 = 1146.1958/1145.3572/1148.8000, sample SD (n=3) = 1.7953, against the replicate |0′−0| of 12.7279 (1.11 %) above — SD/replicate ≈ 0.14, about seven times smaller than the replicate offset. At rung C3 (25,000) the same comparison inverts: SD 7.7627 vs replicate 0.3365, ≈23× larger. n=3 (2 degrees of freedom); no verdict on (b)/(b2) here — see [[THE-SPREAD-REPLICATE-RATIO-INVERTS-BETWEEN-C3-AND-THE-TOP-RUNG]] and docs/experiments/002-night2-seeds-1-and-2.md.
- **2026-09-15, CC (four more diagnostics, docs/experiments/002-night2-seeds-1-and-2.md §5d/§5f):** connectivity — the linear path between run 0 and run 0′ at 250,008 carries a barrier of 96.6 (variant 2) against their 12.7 endpoint gap, and is no better connected than the 0→1 control (115.2 at the same α); the self-path is flat to ≈1e-4, and the design's own resolution criterion is not met, so all barriers are lower bounds. ablation (unregistered) — the twin trap passes on both pre-declared metrics (Euclidean, Spearman) in all three item subsets, but the Euclidean margin over the (0′,1) different-seed pair is only 4 % and a post-hoc Pearson reverses it; the supported claim is that the twins agree in rank order of cell-type importance (ρ 0.72 vs 0.35–0.48 for different seeds), not in their largest single effects (seed 0's top type Tm5c +2,616.8 is +34.6 in seed 0′).
- **2026-09-15, CC:** Ark 10:00: the entry title states half the fact -- after night 2 the statement is "three different individuals sit closer to each other (SD 1.80) than one individual to its own replicate (12.73), seven times", and after the diagnostics "the two ends of one seed sit in different basins (barrier 96.6) like different seeds do"; the title is not rewritten (no backfilling per the format) -- the current statement lives in docs/experiments/002-night2-seeds-1-and-2.md §2/§5d and in [[THE-SPREAD-REPLICATE-RATIO-INVERTS-BETWEEN-C3-AND-THE-TOP-RUNG]].
- **2026-09-17 UTC (2026-09-18 local), CC (night 4 adds a second replicate pair; recomputed by CC from the
  committed values, arithmetic on numbers already in the repo, not a new measurement):**
  - **The second replicate pair.** 3′ − 3 = +10.4309 at 250,000, 0.905 % of seed 3
    (`docs/experiments/004-night4-replicate-3prime-and-seed-5.md:91`) — the same order of
    magnitude as the first pair's +12.7279 (1.11 %).
  - **The population fact.** σ = 1.7953 at the 250,000 hook is the sample sd over seeds {0,1,2}
    only, n=3 (`docs/experiments/002-night2-seeds-1-and-2.md:71`), while the sd over all six seeds
    {0..5} at the same rung is 5.1425 (`docs/experiments/004-night4-replicate-3prime-and-seed-5.md:81`)
    — a factor of 2.86 (5.1425 / 1.7953).
  - **The consequence for the replicate-cost estimate.** With r > (σ_rep/σ_between)², σ_rep from
    the single first pair (12.7279 / 1.128 = 11.28) and the n=3 σ (1.7953) gives r = (11.28 /
    1.7953)² = 39.5 ≈ 40, matching the figure already on record at
    `docs/experiments/002-night2-seeds-1-and-2.md:234-236` (≈ 53 nights at N = 8). Using instead
    the n=6 σ (5.1425) with both replicate pairs — σ_rep = mean(|12.7279|, |10.4309|) / 1.128 =
    11.5794 / 1.128 = 10.27 — gives r = (10.27 / 5.1425)² = 4.0, ≈ 5.3 nights in the same
    conversion (4.0 × 53/40). The cost estimate swings from ≈ 53 nights to ≈ 5 depending on which
    seed population supplies the denominator.
  - **The variance comparison.** Within-individual variance ≈ 105–127 (σ_rep 10.27² = 105.5 to
    11.28² = 127.2) sits above the between-seed variance at n=6, 5.1425² = 26.4 — the observed
    between-seed spread is smaller than the twin noise. The record's own 95 % χ² CI for σ(n=6) at
    250,000 is [3.2100, 12.6126]
    (`docs/experiments/004-night4-replicate-3prime-and-seed-5.md:105`).
  - **A units defect in the line above, found in review and corrected here** (Ark, 2026-09-17 UTC;
    verified by CC at source the same day). An earlier version of this note put that interval next
    to the twin gap 12.7279 and reported its upper bound as sitting "just below" it. Those are two
    kinds of quantity: on the left an interval for a **standard deviation**, on the right the
    **difference of two runs**. Brought to common units under the normal-difference convention
    σ = |Δ|/1.128379 — which is an **assumption, not a measurement** — the twin difference is
    σ_rep = 11.28, and then the n=6 interval [3.2100, 12.6126] **contains** it while the n=5
    interval [2.1225, 10.1801] does not. So the direction does not survive the change of units:
    with five individuals the spread is distinguishable from the replicate, with six it is not.
    The same comparison stands in `docs/next-session-plan.md` §2a and carries the same defect;
    an override is recorded there rather than a rewrite of the record.
  - **The source record's own wording**, kept for the trail
    (`docs/experiments/004-night4-replicate-3prime-and-seed-5.md:113-114`: "the CI upper bound
    (12.61) now sits just below the run-0/0′ replicate offset (12.73)").
  - **CC's reading, 2026-09-17 UTC (2026-09-18 local), not reviewed:** if the top rung's test-retest reliability is
    indistinguishable from zero, any cheap-vs-expensive correlation is bounded above by that
    reliability, so the ρ preview cannot be read as a statement about individuals until the top
    rung shows reliability above zero.
- **axis:** honesty
