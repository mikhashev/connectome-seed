# Closed entries

## 2026-09-15 — closed by CC

### RUN-0-SHOWS-WHERE-THE-LOSS-PLATEAUS: run 0's rungs and checkpoints will show where held-out loss stops moving, and if that is far before 250,000 the expensive evaluation could be redefined cheaper — only by a new pre-registration written before the N runs (LOW, closed, 2026-09-14 — Ark, chat 2026-09-13; filed by CC)

**Closed:** S2026-09-13.1 · 2026-09-15 · disproved · docs/experiments/001-run0-and-replicate.md §4: minimum checkpoint loss 1141.0463 at iteration 219,612; held-out loss rose +0.11% (1147.5358 -> 1148.8075) over the last 50,000 iterations; docs/preregistration-cheap-vs-expensive.md §7 "Plateau facts"; the redefine-expensive-via-the-plateau reading judged not viable by reviewers, 002 §5a item 12 (docs/experiments/002-night2-seeds-1-and-2.md); a plateau is an interpretation of the tail, not a datum · closed by CC

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

### RESEARCH-REPO-START-CHECKLIST-WRITTEN-ON-MIKES-WORD: fourteen rules distilled from this session's incidents, so a new research repository starts by reading them rather than re-deriving the principles (LOW, closed, 2026-09-15 — Mike 09:56 «пиши чек-лист»; drafted by Ark 08:50/09:39/09:51, written by CC)

**Closed:** S2026-09-13.1 · 2026-09-15 · fixed · `docs/CHECKLIST-research-repo.md` written (14
rules with incident addresses, header carrying Mike's word and the authorship line, closing
links to `docs/tool-hardening-package.md` and `docs/preregistration-cheap-vs-expensive.md` §7);
linked from `README.md`; verified on disk by CC · commit: not yet committed this session (Mike's
instruction: do not commit) · closed by CC

- **Observed.** Ark proposed the checklist three times (08:50, 09:39, 09:51) as the rules
  emerged from the 002 §5h code audit and the tool-hardening package; Mike's word (DPC Research
  chat, 2026-09-15 09:56 UTC): «пиши чек-лист». The file carries the same 14 items in the same
  order as the rules Ark and Zcode named through the day, plus R1–R4 from
  `docs/tool-hardening-package.md`.
- **First step.** None — closed on completion; a future incident that adds a rule appends a
  15th item rather than reopening this entry.
- **axis:** honesty, reach

### NIGHT-2-RUNS-SEEDS-1-AND-2-ON-MIKES-WORD: seeds 1 and 2 trained to 250,000, sequential, no replicate, are the first between-seed distances against the run 0 / run 0′ replicate offset (HIGH, closed, 2026-09-14 — CC, from the experiment record and next-session plan)

**Closed:** S2026-09-13.1 · 2026-09-15 · fixed · seed 1 (9991/001) EXIT rc=0, 250,008 iterations, 14,532.9 s; seed 2 killed at iteration 12,700 by the KB5129195 restart, partial dir renamed to flow/9991/002_killed_by_reboot, excluded under §7's resume rule; re-run as wave night2b (9991/002), started 2026-09-15T01:13:46Z, EXIT rc=0, 250,008 iterations, 14,296.6 s, done 05:12:18Z; Mike, chat 05:19Z: «прогон завершен»; record docs/experiments/002-night2-seeds-1-and-2.md and results/night2/ · commit: (this commit) · closed by CC

- **Observed.** Tooling ready: `tools/night/start_night.ps1` takes `-NoReplicate` (this
  commit), dry-run quoted (ids `9991/001`, `9991/002`; ensemble 9991 already holds `000` and
  `900` — the ids differ, no collision). Command in `docs/next-session-plan.md` §2.
- **Observed 2026-09-15 (CC).** Mike's word given (DPC Research chat, 2026-09-15 18:32 local:
  «вноси да и напиши мне команду…», then «запустил»); launched. Launcher log: `WAVE START
  tag=night2` 2026-09-14T19:12:31Z, launcher PID 32124, mode sequential, detached, determinism
  off, 2 jobs. First run id 9991/001, seed 1, PID 16460, `--n-iters 250000 --rungs
  1000,5000,25000,250000 --no-determinism`; progress log at iteration 700: 0.066 s/iter, VRAM
  1426 MiB, ETA first run ≈ 23:46Z. Second run 9991/002, seed 2, follows sequentially.
  `flow/9991` now holds 000, 001, 900. The b2 amendment (`9c395d5`) and the review edits plus
  `rho_ci.py` (`21fa5ab`) were committed before the launch.
- **Observed 2026-09-15, later (CC).** Seed 1 (9991/001) completed: `EXIT rc=0
  final_iteration=250008 wall=14548.9s` at 23:15:00Z. Seed 2 (9991/002) started 23:15:00Z; last
  progress line iteration 12,700/250,000 at 23:29:04Z; killed at 23:29:19Z by a Windows Update
  planned restart (KB5129195) — see
  [[WINDOWS-UPDATE-RESTARTS-INSIDE-THE-NIGHT-WINDOW-BECAUSE-ACTIVE-HOURS-END-AT-0600]]. Under the
  registered §7 resume rule (an interrupted run is a failed run, re-run from the same seed, no
  resume) seed 2 is re-run from scratch. Pending Mike's decision: remove or rename
  `results/flow/9991/002` (`run_individual.py:301-308` refuses to start if it exists, and a new
  tag such as `night2b` keeps the partial `night2_9991-002.*` / `wave_night2.*` records intact),
  then `-Tag night2b -Seeds 2 -NoReplicate`.
- **First step.** Mike's word (the standing rule,
  [[THE-NIGHT-RUN-STARTS-ONLY-ON-MIKES-EXPLICIT-WORD]], closed), then launch by Mike; morning
  comparison against the replicate offset (+12.64 mean / 1.11 % at 250,000,
  `docs/experiments/001-run0-and-replicate.md` §4) per the decision rule already registered
  in `docs/preregistration-cheap-vs-expensive.md` §7.
- **axis:** collective
- **taken:** CC · 2026-09-15

### A-TRAINED-SURROGATE-IS-NOT-A-PREFIX-OF-THE-SAME-PROCESS: AlphaGenome Atlas shows a cheap evaluation that works, but it is a trained surrogate validated at the top of its ranking, while this project's cheap evaluation is a prefix of the expensive process, the kind 2508.17464 found not to rank (MEDIUM, closed, 2026-09-13 — Ark, 17:51 UTC, on Mike's link of 17:50 UTC; source read by CC 2026-09-14)

**Closed:** S2026-09-13.1 · 2026-09-15 · fixed · Mike decided yes 2026-09-15 18:05 local, DPC Research chat: «ок давай впишем»; the form is written into docs/preregistration-cheap-vs-expensive.md as secondary hypothesis (b2) — §1 bullet, §4 statistic X = |Top-k(C3) ∩ Top-k(250,000)| with exact hypergeometric tails for N = 8/10/12/16/20 and k = 2/3 from docs/prereg-scripts/topk_tail.py (8!-permutation self-check passed, Python 3.12.10), §5 decision rule and timing rule, §7 measurability paragraph, §8 exclusions, §9 provenance; k = 2 fixed, marked (proposed — fix in review) until seeds 1 and 2 start · commit: (this commit) · closed by CC

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

## 2026-09-13 — closed by CC

### HOW-MANY-FULL-RUNS-THE-TEST-IS-ALLOWED: K runs to convergence is the whole cost of Phase 2, and it is not a hardware question (HIGH, closed, 2026-09-13 — asked by Ark, Johnny and Warren independently, 07:16–07:20 UTC)

**Closed:** S2026-09-11.1 · 2026-09-13 · fixed · K = 1 decided by Mike 2026-09-13 (run 0 only); N is no longer a number to name but a rule in docs/preregistration-cheap-vs-expensive.md §4, N = floor(m · H_avail / h_run) − 1 with m = 1 measured (e797f02) and h_run from run 0; the floor 8 vs 10 remains Mike's choice as [[N-EQUALS-EIGHT-IS-BELOW-THE-FILES-OWN-MINIMUM]] · commit: (this commit) · closed by CC

- **Observed.** The GPU is local and the money is zero; the cost is K × 250,000 iterations,
  overnight. K bounds the statistic in the pre-registration, so it is needed *before* the
  file is final, not after.
- **First step.** Mike names K. Parent task [[PRE-REGISTER-THE-CHEAP-VERSUS-EXPENSIVE-TEST]].
- **Decided 2026-09-13 (Mike): K = 1 to begin with.** Run 0 only; N for the test follows from
  its measured cost by the rule in ADR-002 Q1. Entry stays open until N is set.
- **axis:** honesty

### IDEA-MD-IS-VERBATIM-RUSSIAN-IN-A-REPOSITORY-THAT-OPENS-IN-ENGLISH: the idea is 62 % Cyrillic by character because it is the author's text as written, and the public version must be English without ceasing to be the record (LOW, closed, 2026-09-13 — Mike, 06:46 UTC: «там всё на английском должно быть»)

**Closed:** S2026-09-11.1 · 2026-09-13 · fixed · commit 30dc626: idea_en.md is in the repository as a marked English translation beside idea.md, and idea.md stays verbatim as the record · closed by CC

- **Observed.** Measured 2026-09-13: README 0.5 % Cyrillic, `literature.md` 1.0 %,
  `idea.md` 62.4 %, `chat/` 70–95 %, whole folder 50.5 %.
- **First step.** Publish `idea.md` as a marked translation with the Russian original kept
  beside it — a translation labelled as one is not a retelling passed off as the source.
  Child of [[ADR-001]].
- **axis:** reach

### ONE-GPU-ITERATION-BEFORE-ANY-OVERNIGHT-RUN: the price of the expensive evaluation on this card is an estimate until one training iteration has been timed here (HIGH, closed, 2026-09-13 — Mike, 07:20 UTC: «сначала весь флоу проверить, а долгие прогоны ночью»)

**Closed:** S2026-09-11.1 · 2026-09-13 · fixed · measured 2026-09-13 on the RTX PRO 4500 Blackwell, torch 2.9.1+cu128: 0.0619 s per training iteration (n=22, min 0.0589, max 0.0694), peak VRAM 1,402 MiB allocated / 4,568 MiB on the card, loss finite 24/24, so 250,000 iterations = 4.30 h and about 4.6 h all-in with checkpoints; two runs per ~10 h night sequential, concurrency not measured; source scratchpad/flyvis-probe/gpu_price_probe_instrumented.json · closed by CC

- **Observed.** The flow runs on this machine on CPU: `Network()` builds in 13.1 s; a
  full-node synthetic stimulus (5,768 photoreceptors, 20 frames) runs forward in 0.06 s and
  backward in 0.05 s with non-zero gradients. No GPU iteration has run. The card is occupied
  by production (28,395 of 32,623 MiB at last check), so this needs a maintenance window.
  Warren's 10–50 ms per GPU iteration is Inferred by its author and is not adopted here.
- **First step.** In a window with production down: one iteration of the stock training loop
  on the GPU, its wall-clock and VRAM recorded. Only then is K × 250,000 iterations turned into
  a night. Blocked by [[PRE-REGISTER-THE-CHEAP-VERSUS-EXPENSIVE-TEST]]; was blocked by
  [[SINTEL-IS-THE-ONE-UNVERIFIED-LINK-IN-THE-FLOW]], closed 2026-09-13.
- **2026-09-13:** dataset on disk and the flow task builds and yields samples on CPU (see the closed Sintel entry). This entry is now blocked only by the pre-registration review and the maintenance window.
- **axis:** honesty

### PRE-LAUNCH-EDITS-TO-THE-PRE-REGISTRATION-BEFORE-RUN-0: two reviews asked for fifteen text edits before run 0, and any of them applied after the run would be indistinguishable from an edit made after looking (HIGH, closed, 2026-09-13 — Ark 15:45 UTC and Zcode 16:24 UTC, chat; the K1 lesson)

**Closed:** S2026-09-11.1 · 2026-09-13 · fixed · 24 exact replacements applied to docs/preregistration-cheap-vs-expensive.md on Mike's word 17:06 UTC; floor 8/10 left as Mike's choice in §4 · commit: (this commit) · closed by CC

- **Observed.** The fifteen: the N-rule off-by-one and the "four nights" prose; the H_avail
  horizon; floor 8 vs 10 (Mike chooses); C3 as the primary rung with Holm for C1/C2; the
  inconclusive band by permutation CI; the negative branch narrowed and the positive one
  sharpened; a two-sided (a) criterion with the self-splice as instrument control; σ instead
  of range in §7; the determinism sentence, false since Mike's 16:20 UTC decision; a resume
  rule; one h_run definition; the 4.6 h arithmetic; exact rows N = 12/16/20 and the two
  tails; the "independent re-run" line; the status line. Commit e797f02 applied the measured
  facts and left every semantic edit for Mike's word. A scratchpad draft of the edits was
  named (`prereg-edits-draft.md`); draft written 23:29 local and applied (CC,
  2026-09-13).
- **Inferred.** "Decided in advance" stays distinguishable from "decided after looking" only
  if the edits land in a commit that precedes run 0's first checkpoint.
- **First step.** Mike says which edits go in; CC applies them by exact replacement and
  commits before the launch word. Parent task [[PRE-REGISTER-THE-CHEAP-VERSUS-EXPENSIVE-TEST]].
  Blocks [[THE-NIGHT-RUN-STARTS-ONLY-ON-MIKES-EXPLICIT-WORD]].
- **axis:** honesty

### PRE-REGISTER-THE-CHEAP-VERSUS-EXPENSIVE-TEST: the test has a verified flow and no written reading, so a run today would produce a number nobody could interpret (HIGH, closed, 2026-09-13 — Mike, 07:27 UTC: «всё ты делаешь, мы ревьювим»; the demand for numbers first is Johnny's, Ark's and Warren's, independently)

**Closed:** S2026-09-11.1 · 2026-09-13 · fixed · docs/preregistration-cheap-vs-expensive.md written 2026-09-13, reviewed by Ark (15:45 UTC) and Zcode (16:24 UTC), the fifteen edits applied on Mike's word in 5175239; the two decisions still open live in their own entries — the floor 8 vs 10 ([[N-EQUALS-EIGHT-IS-BELOW-THE-FILES-OWN-MINIMUM]]) and top-k as a secondary hypothesis ([[A-TRAINED-SURROGATE-IS-NOT-A-PREFIX-OF-THE-SAME-PROCESS]]); Johnny and Warren have not reviewed, noted and not waited on · commit: (this commit) · closed by CC

- **Observed.** Three reviewers converged on the same missing file: what *cheap* and
  *expensive* are in iterations, the number of individuals and seeds, the statistic and its
  threshold, the decision rule per outcome, and a named prediction for composition. None of
  the five exists in writing. The only number already fixed is flyvis's default for
  *expensive*: `n_iters: 250000`, batch 4, lr 5e-5 → 5e-6.
- **Inferred.** Hypotheses (a) "a spliced module behaves predictably" and (b) "cheap agrees
  with expensive" must be registered separately with separate rules, or a month from now it
  will not be possible to say which one fell. A splice of two identical copies is a control
  that can only pass — the same shape as a zero-initialised adapter — so the splice joins two
  *different* members or types, and the prediction is written before the run.
- **First step.** One file in this repository with the five items as numbers; two of the
  numbers are not the writer's — K (Mike) and what is spliced (Ark's proposal, in review).
  Child of [[ADR-002]]. Blocks [[ONE-GPU-ITERATION-BEFORE-ANY-OVERNIGHT-RUN]].
- **2026-09-13:** draft in the repository (`docs/preregistration-cheap-vs-expensive.md`), scripts beside it; seven marked proposals open for review (source of variation; splice pair and cell type — Ark; ladder and prefix definition; held-out split and metric; N = 10 minimum and the N rule; the 5 % tolerance for (a); the 1 % replicate tolerance). Entry stays open until reviewed.
- **axis:** honesty

### RESUME-OF-AN-INTERRUPTED-RUN-IS-UNVALIDATED: the night plan kills run 0′ at a checkpoint and resumes it the next night, and nobody has checked what a resumed replicate restores or what §7 counts it as (HIGH, closed, 2026-09-13 — Zcode review 3.4, 16:24 UTC; filed by CC)

**Closed:** S2026-09-11.1 · 2026-09-13 · fixed · 48-iteration interrupt-and-resume test 2026-09-13: flyvis recover() fails as installed (resolve_checkpoints TypeError, datamate FileExistsError); replica restores no RNG/data order, penalty optimizer not recovered, counter off by one (48 → 59); resumed − uninterrupted at rungs 24/36/48 = −0.096/−0.141/−0.187 vs replicate noise ≤ 1.1e-4; rule registered in §7: interrupted run = failed run, re-run from the same seed, resume never used · commit: (this commit) · closed by CC

- **Observed.** The night plan is run 0 then run 0′, 8.6–9.2 h together at the measured
  4.3–4.6 h per run, inside an 8–9 h window — so run 0′ is interrupted at a checkpoint and
  resumed the following night. `docs/preregistration-cheap-vs-expensive.md` §7 has no rule
  for what a resumed replicate is, and what flyvis `resume=true` restores — optimizer state,
  scheduler, RNG, data order — has not been checked.
- **Inferred.** Until both are settled, a resumed run 0′ is not the replicate §7 describes,
  and the 1 % replicate tolerance would be measured against the wrong object.
- **Reported.** Zcode 3.4 (chat, 16:24 UTC).
- **First step.** A 48-iteration interrupt-and-resume test against an uninterrupted control,
  both with determinism off; compare the hook trajectories at rungs 24/36/48 against the
  replicate noise. Running now (CC subagent). The resume rule itself is one of the fifteen
  edits in [[PRE-LAUNCH-EDITS-TO-THE-PRE-REGISTRATION-BEFORE-RUN-0]].
- **axis:** honesty

### SINTEL-IS-THE-ONE-UNVERIFIED-LINK-IN-THE-FLOW: everything up to the dataset runs on this machine, and the dataset is five gigabytes of a third party's data under its own terms (HIGH, closed, 2026-09-13 — CC, 07:26 UTC, asked before pulling it)

**Closed:** S2026-09-11.1 · 2026-09-13 · fixed · archive 5,627,783,629 B = server size, CRC clean over 8,753 members; 23/23 sequences in training/final and training/flow; MultiTaskSintel(tasks=[flow]) builds (69 items) and yields lum (9,1,721) / flow (9,2,721); no licence file in the tree, README carries copyright 2012 Butler et al. and a cite request only; commit: (this commit) · closed by CC

- **Observed.** flyvis's flow task reads `training/final` (images, 1.7 GB) and
  `training/flow` (ground truth, 3.1 GB) from MPI-Sintel and downloads them itself via
  `download_sintel()`; the depth split is only needed for a depth task. Disk free: 516 GB.
  The dataset's README carries its own terms; they were not read.
- **First step.** Mike's word; then one call, and the flow is verified end to end.
- **axis:** honesty

### THE-ATTRIBUTION-STRING-FOR-CC-BY-IS-NOT-WRITTEN: the licence is chosen and the LICENSE file cannot be written without saying who the author is (MEDIUM, closed, 2026-09-13 — Mike, 06:55 UTC: «ок CC BY 4.0»)

**Closed:** S2026-09-11.1 · 2026-09-13 · fixed · LICENSE at repo root with the string; README ## Licence; commit: (this commit) · closed by CC

- **Observed.** README names Mike and three agents by role. CC BY 4.0 requires an
  attribution; the string is a decision, not a default.
- **First step.** Mike names it; the LICENSE file follows in the same pass as the links.
  Child of [[ADR-001]].
- **axis:** reach

### THE-SECOND-VOICE-IN-THE-IDEA-TRANSCRIPT-IS-GROK-AND-UNNAMED: the review pasted inside the idea's transcript is a model's output that the public documents cite without a source (MEDIUM, closed, 2026-09-13 — Mike, 06:53 UTC, on who the second voice is)

**Closed:** S2026-09-11.1 · 2026-09-13 · fixed · commit: (this commit); git grep for 'second voice' in tracked files returns only the ADR-001 decided line · closed by CC

- **Observed.** All three entries in the transcript are attributed to `Mike Shevchenko`; Mike
  stated he showed the idea to Grok. The name «Безногим» does not occur anywhere in this
  repository. README and `idea.md` say "the second voice".
- **Inferred.** It is Mike's own conversation with a model and his to publish; the standard
  that a quote carries its source (Johnny) is what is unmet. CC's recommendation: drop it from
  the public version — each of its points is either superseded by the reviews or wrong.
- **First step.** Mike: name it as *Grok, 2026-09-12, shown the idea by Mike*, or drop it.
  Child of [[ADR-001]].
- **axis:** reach

## 2026-09-14 — closed by CC

### THE-NIGHT-RUN-STARTS-ONLY-ON-MIKES-EXPLICIT-WORD: the launcher is ready and dry-printed, and nothing starts until Mike says so (HIGH, closed, 2026-09-13 — Mike, 16:22 UTC: «полный ночной прогон не запускаем пока я явно это не скажу»)

**Closed:** S2026-09-13.1 · 2026-09-14 · fixed · launched by Mike 18:40 UTC (run 0), sequential replicate run 0′ followed automatically; both runs exit ok, 0 errors, 250,008 iterations each; WAVE DONE 2/2 ok at 2026-09-14T02:39:52Z; results recorded in `results/night1/` · commit: (this commit) · closed by CC

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
- **Observed, 2026-09-14.** Run 0 (`9991/000`) started 2026-09-13T18:40:31Z, finished
  2026-09-13T22:40:56Z, 250,008 iterations, exit ok, 0 errors. Run 0′ (`9991/900`, the §7
  replicate) started 2026-09-13T22:40:59Z, finished 2026-09-14T02:39:51Z, 250,008
  iterations, exit ok, 0 errors. `wave_night1.json`: `"finished_utc": "2026-09-14T02:39:52Z"`;
  progress log: `WAVE DONE 2/2 ok`. Results and the pre-registration §3/§6/§7 record in
  `docs/preregistration-cheap-vs-expensive.md` and `results/night1/`.
- **First step.** The word. Then launch, and the PID and the first rung (1,000) reported to
  the chat. Was blocked by [[PRE-LAUNCH-EDITS-TO-THE-PRE-REGISTRATION-BEFORE-RUN-0]] and by
  [[RESUME-OF-AN-INTERRUPTED-RUN-IS-UNVALIDATED]], both closed 2026-09-13. Done — see Closed
  line above.
- **axis:** collective
