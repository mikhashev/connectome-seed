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

### PRE-REGISTER-THE-CHEAP-VERSUS-EXPENSIVE-TEST: the test has a verified flow and no written reading, so a run today would produce a number nobody could interpret (HIGH, open, 2026-09-13 — Mike, 07:27 UTC: «всё ты делаешь, мы ревьювим»; the demand for numbers first is Johnny's, Ark's and Warren's, independently)

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


## BLOCKED ON DECISION


### HOW-MANY-FULL-RUNS-THE-TEST-IS-ALLOWED: K runs to convergence is the whole cost of Phase 2, and it is not a hardware question (HIGH, open, 2026-09-13 — asked by Ark, Johnny and Warren independently, 07:16–07:20 UTC)

- **Observed.** The GPU is local and the money is zero; the cost is K × 250,000 iterations,
  overnight. K bounds the statistic in the pre-registration, so it is needed *before* the
  file is final, not after.
- **First step.** Mike names K. Parent task [[PRE-REGISTER-THE-CHEAP-VERSUS-EXPENSIVE-TEST]].
- **Decided 2026-09-13 (Mike): K = 1 to begin with.** Run 0 only; N for the test follows from
  its measured cost by the rule in ADR-002 Q1. Entry stays open until N is set.
- **axis:** honesty


