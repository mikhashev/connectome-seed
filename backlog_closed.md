# Closed entries

## 2026-09-13 — closed by CC

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
