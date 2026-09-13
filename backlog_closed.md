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
