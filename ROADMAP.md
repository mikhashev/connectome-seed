# Roadmap — connectome-seed

Phases are ordered by what blocks them, not by ambition. Each phase names the decision it
lands on (`docs/decisions/`) and the tasks it consists of (`backlog.md`). Dates are the writer's
local day; chat timestamps quoted anywhere in this repository are UTC (this machine is
UTC+07).

---

## Phase 0 — Record (DONE, 2026-09-13)

**Goal:** one idea and one day of examining it, saved so that it does not have to be re-derived.

- The idea verbatim (`idea.md`), the literature read at source with per-entry verification
  status (`literature.md`), the thread as it happened (`chat/`, local only), the one
  open-access PDF (`sources/`).
- Reviewed the same day by Johnny and Ark; corrections applied in place and named.
- Repository initialised with `chat/` ignored from the first commit — `8695d26`.

**Decisions:** [001 — publication shape](docs/decisions/001-publication-shape.md) (CC BY 4.0;
transcripts never enter history). [002 — file under a condition](docs/decisions/002-file-under-condition.md)
(the verdict, and the condition that would change it).

## Phase 1 — Pre-registration and the flow (IN PROGRESS)

**Goal:** be able to run the test *and* be able to read its result. Both, before the GPU.

**Flow, verified on this machine, CPU only (2026-09-13):** flyvis 1.2.0 installs on Windows;
its storage layer `datamate` fails on Windows by unlinking an HDF5 file that still has an
open handle (`io.py`, `_write_h5` / `_extend_h5`); a close-before-unlink patch holds —
`Network()` builds in 13.1 s; a full-node synthetic stimulus (5,768 photoreceptors, 20
frames) runs forward in 0.06 s and backward in 0.05 s with non-zero gradients. The dataset
(Sintel, ~5 GB: images + ground-truth flow) is on disk since `866b968` — 23/23 sequences, the
flow task builds and yields samples — and the price of a GPU iteration is measured (Phase 2,
item 1).

**Pre-registration, written before any run** — one file, with numbers:
1. what *cheap* is and what *expensive* is, in iterations (expensive: flyvis default
   `n_iters: 250000`, batch 4);
2. the number of individuals and seeds;
3. the statistic (rank correlation) and the threshold at which it is significant at that N;
4. the decision rule for each outcome;
5. the named prediction for composition — and the two hypotheses kept apart:
   **(a)** does a spliced module behave predictably, **(b)** does cheap evaluation agree with
   expensive. A result on one says nothing about the other.

**Draft:** [docs/preregistration-cheap-vs-expensive.md](docs/preregistration-cheap-vs-expensive.md) — in the repository since 2026-09-13, marked proposals await review; critical ρ values recomputed independently by CC (N=8: 0.6429, N=10: 0.5636).

A splice of two *identical* copies is a control that can only pass; the test splices two
*different* things (two ensemble members, or two cell types), with the prediction stated first.

**Exit:** the pre-registration file exists and has been reviewed (draft in repo, review open); the dataset is on disk — done 2026-09-13 (23/23 sequences, flow task builds and yields samples).

## Phase 2 — The test (IN PROGRESS — item 1 done 2026-09-13; long runs overnight)

**Goal:** the condition, measured.

1. **One training iteration on the GPU**, in a maintenance window with production down — this
   gives the price of *expensive* on this card. Nothing is scheduled from an estimate.
   **Done 2026-09-13** (Mike, 11:19 UTC: «карта свободна, можно делать прогоны»). Two runs of
   24 iterations of the stock `flow` config (batch 4, extent 15), `flyvis train-single` and the
   same config in-process with timing after `torch.cuda.synchronize()`, RTX PRO 4500 Blackwell,
   torch 2.9.1+cu128. Observed: **0.0619 s per training iteration** within an epoch (n = 22,
   min 0.0589, max 0.0694); checkpoint 0.73–0.90 s, post-epoch writes 0.30 s; peak VRAM
   **1,402 MiB** torch-allocated (1,512 MiB reserved), 4,568 MiB on the card over a 2,565 MiB
   desktop baseline; GPU utilization samples peaked at 42 % / 71 %; loss finite, 24/24. Cold
   solver init 28.4 s, warm 4.3 s. Inferred: 250,000 iterations = 15,475 s = **4.30 h**, ≈
   **4.6 h** all-in with ~70 checkpoints at `chkpt_every_epoch: 300`. Consequence for the
   pre-registration's N rule (N = floor(H_avail / h_run), ≥ 8): one ~10 h night holds **2
   sequential runs**; N = 8 is ~37 h ≈ 4 nights. Utilization ≤ 71 % and 1.5 GB per run suggest
   several runs could share the card — a hypothesis, **not measured** at that point. Logs in the
   scratchpad (`flyvis-probe/gpu_price_probe_instrumented.json` and siblings), outside the
   repository.
   **Concurrency, measured later the same day (m = 1, a gate for the N rule):** barrier-synchronised
   waves of 4 and 8 processes, 240 iterations each, `Compute Mode: Default` (time-sliced, no MPS
   on Windows). Observed: per process 0.2281 s/iter at k = 4 (3.69×) and 0.4502 s/iter at k = 8
   (7.27×); aggregate saturates at ≈ 17.5 it/s for any k (solo 16.2); card peak 10,116 / 17,542
   MiB, util peak 91 / 92 %. The hypothesis above is refuted: **m = 1**, the N rule reads
   N = floor(H_avail / h_run), a night holds two sequential runs, N = 8 needs four nights. Ark
   (chat, 15:45 UTC): «a gate for (b), not an optimisation». **Determinism flags**
   (`CUBLAS_WORKSPACE_CONFIG=:4096:8`, cudnn deterministic, `use_deterministic_algorithms(True,
   warn_only=True)`) cost 3.77×: 0.2335 s/iter ≈ 16.2 h per run against 0.0620 s without; losses
   differ at the 7th significant digit; decision pending Mike (pre-registration §7). Logs
   `flyvis-probe/gpu_concb_*`, `flyvis-probe/night/dry_9990-000.json`, `night/nodet_9990-010.json`
   in the scratchpad.
2. **K full runs to convergence**, overnight, per the pre-registration. K is Mike's number and
   is the real cost of this phase; the GPU is local and the money is zero. **Night plan (planned,
   not done):** run 0, then run 0′ (seed 0 twice, pre-registration §7), sequentially, ≈ 8.6–9.2 h
   together at the measured 4.3–4.6 h per run; launched on Mike's command.
3. The cheap evaluation of the same individuals, and the rank correlation between the two.

**Outcomes, both of them results:** cheap ranking *disagrees* with expensive → the 2508.17464
finding extended from a 3×3 voxel grid with a 1,417-parameter controller to a real optic-lobe
circuit on 65 cell types; cheap ranking *agrees* → the loop has a middle, and the idea in
`idea.md` becomes eligible to be a project.

## Phase 3 — The article (NOT STARTED)

Written for `Documents/articles`, in English. Its size is set by Phase 2: with a result, an
experimental paper about where cheap evaluation breaks in a developmental loop and one test of
it; without one, a position paper — two independent sources converging on the same unproven
step — and it is written as that, without claiming an experiment.

## Not on this roadmap, deliberately

- Growing anything. No body, no curriculum, no USPEX operators until Phase 2 has a number.
- Choosing the genome representation. Its absence is the *symptom* the condition tests for;
  three requirements (compression, composability, expressivity) pull apart, and the two
  candidate pieces that exist each pay for one with another — see `literature.md` §A1 and §F.
- Within-type specificity. flyvis discards it by construction; nothing in Phases 1–2 can
  speak to it, and the roadmap says so rather than letting a type-level result be read as more.

## Status — generated

The block below is written by `tools/backlog/build.py --roadmap` from `backlog.md` and
`docs/decisions/`; it is the only status in this file that is not typed by hand, so it is the only
one that can be trusted to be current.

<!-- generated by tools/backlog/build.py --roadmap · do not edit inside -->

| axis | decisions | board entries | awaiting observation |
|---|---|---|---|
| **collective** | — | 0 | 0 |
| **knowledge** | — | 0 | 0 |
| **network** | — | 0 | 0 |
| **honesty** | ADR-002 accepted | 3 | 0 |
| **reach** | ADR-001 accepted | 2 | 0 |

**Observation debt: 0 under an axis + 0 in entries that carry none = 0.** Work finished and never seen working; per axis it says which direction is running ahead of its evidence.


Rendered from `docs/decisions/*.md` front matter and `backlog.md`. Nothing here is written by hand; correct it at the source and re-run `uv run python tools/backlog/build.py --roadmap`.

<!-- /generated -->
