# Closed entries

## 2026-09-13 — closed by CC

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
