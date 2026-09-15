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

### RUN-0-SHOWS-WHERE-THE-LOSS-PLATEAUS: run 0's rungs and checkpoints will show where held-out loss stops moving, and if that is far before 250,000 the expensive evaluation could be redefined cheaper — only by a new pre-registration written before the N runs (LOW, open, 2026-09-14 — Ark, chat 2026-09-13; filed by CC)

- **Observed 2026-09-14 (run 0).** Plateau reached: minimum held-out (checkpoint) loss
  1141.0463 at iteration 219,612; held-out loss rose by +0.11 % (1147.5358 → 1148.8075) over
  the last 50,000 iterations (checkpoint near 200,000 → checkpoint near 250,000); plateau:
  |change| < 0.2 %. Rung-vs-checkpoint jitter: the
  evaluation-hook rung at iteration 250,000 (1146.1958) and the checkpoint at iteration
  250,008 (1148.8075) differ by 2.61 over the 8 extra iterations. Full trajectory in
  `results/night1/night_report.md` and `results/night1/night_report_checkpoints.csv`.
- **Reported.** Ark: a free lever — run 0's plateau could redefine "expensive" together with
  the ladder.
- **Inferred.** The redefinition is a change to §3 after seeing run 0 — allowed for the
  population only if registered anew *before* the N runs, and not available at all once (b)
  has been seen.
- **First step.** After run 0, plot held-out loss against iteration from the rung and
  checkpoint metrics; if a plateau sits far before 250,000, propose a new pre-registration
  to Mike before any N run starts. Parent task
  [[PRE-REGISTER-THE-CHEAP-VERSUS-EXPENSIVE-TEST]], closed 2026-09-13.
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



## IN PROGRESS

### ROW-B-CELL-TYPE-ACTIVITY-PROFILES-RUN-AS-A-PREVIEW-AT-N-EQUALS-FIVE-OR-SIX: row B (65 per-type activity profiles across P0/P1/P2 and the twin trap) runs from the 72 saved checkpoints of seeds 0, 0′, 1, 2 as a preview diagnostic, never read as a test until N ≥ 8 (MEDIUM, in-progress, 2026-09-15 — Mike 09:56 «делай ряд B»; protocol `docs/proposals/mi-axis-per-cell-type-design.md`; taken by CC)

- **Observed.** Mike's word (DPC Research chat, 2026-09-15 09:56 UTC: «делай ряд B»). Protocol:
  `docs/proposals/mi-axis-per-cell-type-design.md` — 65 per-type means + within-type spread, P0
  (cross-process reproducibility), P1, P2, the twin trap, Spearman ρ pre-fixed as the measure,
  all 16 held-out items. Source: the 72 saved checkpoints of seeds 0, 0′, 1, 2 (`results/night1/`,
  `results/night2/`).
- **Inferred.** At n = 5–6 seeds the critical ρ is 0.90–1.00
  (`docs/next-session-plan.md` §5: "Do not read row B as a test at N < 8"); this run is a
  preview and cannot be read as a hypothesis test.
- **First step.** CC runs the protocol against the 72 checkpoints; results to
  `results/night2/diagnostics/rowB/`.
- **axis:** knowledge
- **taken:** CC · 2026-09-15

## BLOCKED ON DECISION


### THE-SPREAD-REPLICATE-RATIO-INVERTS-BETWEEN-C3-AND-THE-TOP-RUNG: the between-seed spread at 250,000 is smaller than the replicate offset while at rung C3 it is larger, so the plan's §3 branch is decidable and waits on Mike + reviewers (HIGH, open, 2026-09-15 — CC, from the night 2 rung SDs and the §7 replicate comparison, 2026-09-15)

- **Observed.** Held-out loss at rungs, seed 0/1/2 (docs/experiments/002-night2-seeds-1-and-2.md, results/night2/): 1,000: 1208.9363/1208.0556/1209.7639; 5,000: 1207.7673/1206.7832/1207.0115; 25,000 (C3): 1191.7375/1190.2235/1204.3618; 250,000: 1146.1958/1145.3572/1148.8000. Sample SD over seeds {0,1,2} (n=3): 0.8543/0.5151/7.7627/1.7953 respectively. Replicate |0′−0| (night 1, docs/experiments/001-run0-and-replicate.md §4): 0.0000/0.0025/0.3365/12.7279. Ratio SD/replicate ≈23 at 25,000 (C3, the primary rung), ≈0.14 at 250,000 — the between-seed spread at 250,000 (1.7953) is about seven times smaller than the replicate difference (12.7279), while at C3 it is about 23 times larger (7.7627 vs 0.3365).
- **Inferred.** n=3 gives an SD with 2 degrees of freedom; the §7 measurability clause is applied once at the registered N, so this is a distance, not a verdict — no rho, no ranks, no call on hypothesis (b)/(b2) yet. What it does settle is the branch itself: docs/next-session-plan.md §3's (a) top rung measurable / (b) not measurable is now decidable with these numbers. See [[NIGHT-2-RUNS-SEEDS-1-AND-2-ON-MIKES-WORD]] (closed) and [[THE-REPLICATE-DIFFERS-BY-ONE-POINT-ONE-PERCENT-AT-THE-TOP-RUNG]].
- **Observed, 2026-09-15 (diagnostics, docs/experiments/002-night2-seeds-1-and-2.md §5b):** the hook-path and stored-checkpoint reporting paths agree to ≈1e-4 at checkpoint 250,008 across all four runs, so the 0.7-2.6 top-rung gap between the two paths (§5a item 10) is weight movement over 8 iterations, not two instruments; evaluation noise on one checkpoint is float-level (max deviation 6.72e-5 across 8 re-evaluations plus the stored value). The run-0/run-0' twin weight-space distance at 250,008 is 4.2372, 0.52 of its own mean parameter norm and about three-quarters of the 0.59-0.78 range separating different-seed pairs at the same iteration; the +12.1749 per-item-mean loss gap between the twins is spread over 14 of 16 held-out items (bandage_1's three items carry 47%, ambush_2's three carry 28%), not concentrated in one outlier item.
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
- **axis:** honesty
