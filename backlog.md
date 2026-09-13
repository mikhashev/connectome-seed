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

### A-TRAINED-SURROGATE-IS-NOT-A-PREFIX-OF-THE-SAME-PROCESS: AlphaGenome Atlas shows a cheap evaluation that works, but it is a trained surrogate validated at the top of its ranking, while this project's cheap evaluation is a prefix of the expensive process, the kind 2508.17464 found not to rank (MEDIUM, open, 2026-09-13 — Ark, 17:51 UTC, on Mike's link of 17:50 UTC; source read by CC 2026-09-14)

- **Observed.** Source read at source 2026-09-14 (`literature.md` §H): the blog says
  *"testing each one in the lab is practically impossible"* and that collaborators
  *"experimentally verify key variants"*; the PDF says the DNM1 variant was *"the top ranked
  variant by AVI"* and a minigene assay across 5 cell lines confirmed it. What was validated is
  the top of a trained model's ranking against an external experiment, not agreement over a
  population.
- **Reported.** Ark, 17:51 UTC: two kinds of cheap evaluation — a trained surrogate
  (AlphaGenome's; works) versus a prefix of the same process (ours; what 2508.17464 measured
  and found not to rank). Three conditions they had and we lack: a surrogate trained on real
  measurements, a finite enumerable space, one fixed genome. Their success does not license
  our kind.
- **Inferred.** Hypothesis (b) as registered asks for rank agreement over the whole
  population; a weaker, untested-by-2508.17464 form is "does the cheap evaluation find the
  top-k of the expensive ranking?". Proposed, not registered.
- **First step.** Mike decides whether "finds the top-k" enters the pre-registration as a
  secondary hypothesis before the N runs; run 0 is unaffected. Parent task
  [[PRE-REGISTER-THE-CHEAP-VERSUS-EXPENSIVE-TEST]], closed 2026-09-13.
- **axis:** knowledge

### THE-NIGHT-TOOLING-LIVES-IN-A-TEMPORARY-SCRATCHPAD: the runner, the launcher and the patched environment sit in a session temp directory that nothing in the repository points at, and the venv cannot be moved (HIGH, open, 2026-09-14 — CC, on finishing the night tooling; instructions sent 2026-09-13 17:55 UTC)

- **Observed.** `flyvis-probe/night/run_individual.py`, `launch_wave.py`, `start_night.ps1`
  and the environment `flyvis-probe/.venv` (torch 2.9.1+cu128, flyvis 1.2.0, datamate with
  the close-before-unlink patch) are all under `AppData/Local/Temp/claude/…/scratchpad/`;
  the repository holds none of them; a uv venv is not relocatable.
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

- **Observed.** Nothing yet: run 0 has not started. The hook records held-out loss at
  1,000 / 5,000 / 25,000 / 250,000 (§3) and the checkpoint cadence adds ≈ 70 points.
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


## BLOCKED ON DECISION


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

### THE-NIGHT-RUN-STARTS-ONLY-ON-MIKES-EXPLICIT-WORD: the launcher is ready and dry-printed, and nothing starts until Mike says so (HIGH, open, 2026-09-13 — Mike, 16:22 UTC: «полный ночной прогон не запускаем пока я явно это не скажу»)

- **Observed.** Launcher `flyvis-probe/night/launch_wave.py` in the scratchpad (8,643 B,
  2026-09-13); command `launch_wave.py --tag night1 --ensemble 9991 --seeds 0 --replicate
  --sequential --detach --no-determinism`, dry-printed; ensemble 9991 unused; determinism
  off decided by Mike at 16:20 UTC.
- **Observed, 17:07 UTC.** Mike asks for console progress logging so he can launch from
  PowerShell himself and watch; being added to the launcher.
- **Observed, 2026-09-13 late.** Extent 5 measured and rejected — 1.46×, not the ≥ 3× that
  would have moved the night ([[EIGHT-PROCESSES-SHARE-THE-CARD-NO-FASTER-THAN-ONE]]); the
  night stays on extent 15. Tooling final: `night/run_individual.py` (rung hook, progress
  lines, `--override`), `night/launch_wave.py` (`--sequential --detach`, replicate right
  after seed 0), `night/start_night.ps1` (`-DryRun`, `-FollowOnly`, `-Extent`), all
  exercised on 24–48-iteration runs; launch instructions sent to Mike 17:55 UTC; the launch
  is Mike's own PowerShell command. Everything sits in the session scratchpad —
  [[THE-NIGHT-TOOLING-LIVES-IN-A-TEMPORARY-SCRATCHPAD]].
- **First step.** The word. Then launch, and the PID and the first rung (1,000) reported to
  the chat. Was blocked by [[PRE-LAUNCH-EDITS-TO-THE-PRE-REGISTRATION-BEFORE-RUN-0]] and by
  [[RESUME-OF-AN-INTERRUPTED-RUN-IS-UNVALIDATED]], both closed 2026-09-13.
- **axis:** collective
