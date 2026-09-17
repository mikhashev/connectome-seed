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

## Phase 1 — Pre-registration and the flow (DONE, 2026-09-15)

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

**Exit — DONE 2026-09-15.** The pre-registration file exists with all five registered items as
numbers and was reviewed before the first GPU iteration: Ark (2026-09-13 15:45 UTC) and Zcode
(2026-09-13 16:24 UTC); pre-launch edits applied on Mike's word 17:06 UTC the same day, before
run 0 launched (18:40:31Z). The (b2) top-k amendment (§1/§4/§5 of the pre-registration) was
reviewed under its own timing rule — committed before any `wave_night2.*` file or result for
9991/001 or 9991/002 existed — by Ark and Zcode (2026-09-15 18:21/18:24 local) and applied on
Mike's word «вноси» 18:32 local 2026-09-15, before seeds 1 and 2 started
(`docs/preregistration-cheap-vs-expensive.md` §9). Dataset on disk since 2026-09-13 (23/23
sequences, flow task builds and yields samples). **One loose end, not blocking the exit:** the
review of `rho_ci.py`'s construction (Zcode, 2026-09-15 18:45 local — construction accepted,
its numbers reproduced independently) ends "Applied on Mike's word [to be filled at commit]" in
the pre-registration's own §9 — that confirmation line is still unfilled in the source file.

## Phase 2 — The test (IN PROGRESS — item 1 done 2026-09-13; nights 1–4 done, n = 6 individuals trained, N not yet reached)

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
   N = floor(H_avail / h_run), a night holds two sequential runs, N = 8 means nine runs, five
   nights at two per night (floor 8 vs 10 is Mike's open choice, §4). Ark
   (chat, 15:45 UTC): «a gate for (b), not an optimisation». **Determinism flags**
   (`CUBLAS_WORKSPACE_CONFIG=:4096:8`, cudnn deterministic, `use_deterministic_algorithms(True,
   warn_only=True)`) cost 3.77×: 0.2335 s/iter ≈ 16.2 h per run against 0.0620 s without; losses
   differ at the 7th significant digit; decision pending Mike (pre-registration §7). Logs
   `flyvis-probe/gpu_concb_*`, `flyvis-probe/night/dry_9990-000.json`, `night/nodet_9990-010.json`
   in the scratchpad.
2. **K full runs to convergence**, overnight, per the pre-registration. K is Mike's number and
   is the real cost of this phase; the GPU is local and the money is zero. Resume is not used —
   an interrupted run is a failed run (§7, measured 2026-09-13; the killed night-2 attempt below
   is the one case of this rule firing).

   **Nights 1–4 done, individuals seeds 0–5 (n = 6) trained to 250,000, plus two §7
   instrument-noise replicate pairs (0′ = id `9991/900`, 3′ = id `9991/903` — replicates, not
   additional individuals of N):**

   - **Night 1 (2026-09-13/14):** run 0 (seed 0, `9991/000`) and its replicate run 0′
     (`9991/900`), sequential. h_run = 4.00 h. §7 replicate tolerance (< 1 % at 250,000)
     **not met**: 1.1104 % (\|Δ\| 12.7279). Record:
     [docs/experiments/001-run0-and-replicate.md](docs/experiments/001-run0-and-replicate.md).
   - **Night 2 (2026-09-14/15):** seeds 1 and 2. Seed 2's first attempt (`9991/002`, wave
     `night2`) was killed at iteration 12,700 by a Windows Update planned restart (KB5129195)
     and excluded under the resume rule; re-run from scratch as wave `night2b` (same id
     `9991/002`), completed. Record:
     [docs/experiments/002-night2-seeds-1-and-2.md](docs/experiments/002-night2-seeds-1-and-2.md).
   - **Night 3 (2026-09-15/16):** seeds 3 and 4, one wave, no interruption. Record:
     [docs/experiments/003-night3-seeds-3-and-4.md](docs/experiments/003-night3-seeds-3-and-4.md).
   - **Night 4 (2026-09-16/17):** replicate 3′ (id `9991/903`, seed 3, ran FIRST in the wave —
     position-matched against night 3's seed 3, which also ran first) and seed 5 (`9991/005`),
     one wave, no interruption. Record:
     [docs/experiments/004-night4-replicate-3prime-and-seed-5.md](docs/experiments/004-night4-replicate-3prime-and-seed-5.md).

   **Observed, n = 6 individuals + 2 replicate pairs** (record 004 §2/§4): replicate difference
   at the 250,000 hook — 0′ vs 0: **12.7279**; 3′ vs 3: **10.4309**. Between-individual sample sd
   at 250,000 over seeds {0,1,2,3,4,5} (n = 6, 5 degrees of freedom): **5.1425**, 95 % χ²
   interval **[3.210, 12.613]**. The night-4 pre-registered reading (three explanations named
   before the data: position, universal divergence, seed-dependence) **rules out a within-wave
   position effect** — \|3′ − 3\| is large (+10.4309), not near zero as a position effect would
   predict; it does not separate universal divergence from a seed-dependent magnitude.

   **The §7 measurability rule** ("a rung whose between-seed standard deviation does not exceed
   the replicate difference is unmeasurable, not a failure of the surrogate") **is applied once,
   at the registered N, and has not been applied.** Every SD / χ² figure recorded through night 4
   (n = 3, 5, 6 so far) is an explicit preview, one degree of freedom short of whatever N is
   finally registered.

   **N remains undecided** (§4's floor — 8 or 10, Mike's open choice —
   [[N-EQUALS-EIGHT-IS-BELOW-THE-FILES-OWN-MINIMUM]]); at floor 8, two more individuals are
   needed (seeds 6, 7); at floor 10, four more (seeds 6–9).

   Next session: [docs/next-session-plan.md](docs/next-session-plan.md).
3. The cheap evaluation of the same individuals, and the rank correlation between the two. The
   cheap statistic is the C3 hook (25,000 iterations, §3 of the pre-registration), recorded in
   every run above; ρ, and the b2 top-k statistic, are each computed once, at N — neither has
   been computed yet.

   **Observed complications, no rule changed by either:**
   - **(i) C3 sits on a steep descent whose onset varies between runs.** A dense-hook diagnostic
     run (id `9991/703`, a third throw of seed 3,
     [results/diagnostics/c3/](results/diagnostics/c3/README.md)) reads the hook every 100 (and
     every 25) iterations across 20,000–26,000: local slope ≈ −0.0027 to −0.0033/iteration,
     residual sd around the fitted trend **≈ 1.8–2.2**, flat across lags 25–100. Against that:
     the registered C3 replicate difference from the one pair on record before night 4 was
     **0.3365** (0/0′, §7 of the pre-registration); the second replicate pair (3/3′, night 4)
     gives **5.18** at the exact hook (rounds from 5.1847, ≈15× larger) and the opposite sign at
     the neighbouring checkpoint (25,212: −2.9157) — the §4/§7 b2 measurability threshold
     (0.3365) rests on a single replicate pair and is not stable across replicates of the same
     seed (`docs/experiments/004-night4-replicate-3prime-and-seed-5.md` §4, "The C3 finding").
   - **(ii) A window-integral statistic is under review as a candidate for the next
     registration** — [docs/briefs/2026-09-17-window-integral-cheap-statistic.md](docs/briefs/2026-09-17-window-integral-cheap-statistic.md)
     (draft, text only, Mike's launch word not yet given). No number here is computed and no
     rule is changed by either complication; both are Observed, feeding a possible future
     registration, not this one.

**Scale (proposal only, no rule change).** The loss learned by training is ≈ 60 loss units on an
untrained held-out level of ≈ 1,212
([docs/experiments/003-night3-seeds-3-and-4.md](docs/experiments/003-night3-seeds-3-and-4.md) §6c)
— so percentages of the raw loss (e.g. §7's 1.11 % tolerance figure at the top rung) are
percentages of an untrained background, not of the learned signal. On the learned-gain scale the
twin replicate difference is ≈ 21 % of the gain and the n = 5 between-seed σ is ≈ 6 % of it (003
§6c); proposed only for the next registration — §7's tolerance and its recorded FAIL stand
exactly as written.

**Outcomes, both of them results:** cheap ranking *disagrees* with expensive → the 2508.17464
finding extended from a 3×3 voxel grid with a 1,417-parameter controller to a real optic-lobe
circuit on 65 cell types; cheap ranking *agrees* → the loop has a middle, and the idea in
`idea.md` becomes eligible to be a project.

**Unmeasurable — a third status, not a result about the surrogate.** The pre-registration's own
rule (§7): "a rung whose between-seed standard deviation does not exceed the replicate
difference is reported as unmeasurable, not as a failure of the surrogate"; the same shape
applies to the b2 top-k boundary (§4/§5: if the k-th/(k+1)-th gap fails to clear the replicate
floor on either side, that boundary is "unmeasurable … neither a positive nor a negative b2"). A
rung or boundary found unmeasurable carries no verdict on the surrogate at this budget, and it is
the case that routes to Phase 3's position-paper path below, the same as a run with no ranking
result.

**Exit:** N individuals complete (§4's floor — 8 or 10, Mike's choice, not yet made) and the
registered rules — ρ and its critical value at C3, the b2 top-k statistic, the §7 measurability
clause — applied once, at that N, not before. **Proposed addition, awaiting Mike's word, not
part of the Exit above** (Ark, chat 2026-09-17 08:18Z): "and the verdict does not depend on which
replicate is used as the floor."

### Diagnostics while N accrues — the functional-readout track

Plan: [docs/plans/2026-09-16-functional-readout-plan.md](docs/plans/2026-09-16-functional-readout-plan.md).
None of this is (a), (b) or b2; it runs alongside the nightly N accrual on saved checkpoints and
one dense diagnostic run, and none of it changes a pre-registration rule.

- **Step 0 — records.** Done 2026-09-16 (the plan's own commit: override of the ablation
  machine-verdict in 003 §6, checklist rule 16, the "scale 60" paragraph).
- **C3 measurement** (jitter and evaluator-floor by path). Done 2026-09-17 —
  [results/diagnostics/c3/](results/diagnostics/c3/README.md); see Phase 2 item 3(i) above.
- **Step 1 — gray stimulus.** Three gate stops on the copy-fidelity control, none of them the
  48-cell sweep running yet: v2 ("exactly equal" was unsatisfiable at `chkpt_00071` because the
  evaluator itself does not reproduce itself bitwise there); v3.1 (failed by one quantisation
  step over a 10-pair floor — checklist rule 17); v4 (code gate passed, but the recorded
  copy-vs-original 16-item-mean difference, 0.00012016…, breached the documented 1e-4 ceiling —
  the per-item ceiling held). Relaunched each time on Mike's word; latest stop 2026-09-17 08:25Z.
  [results/diagnostics/gray/README.md](results/diagnostics/gray/README.md) (v4, current) and its
  v2/v3.1 predecessors kept beside it in the same directory. **Status: stopped, not running** —
  the sweep has not executed under any brief version yet.
- **Step 2 — tuning battery.** Brief ready
  ([docs/briefs/2026-09-16-step2-tuning-battery.md](docs/briefs/2026-09-16-step2-tuning-battery.md)),
  waits on step 1.
- **Step 3 — genome.** Not started; design and boundary in the plan above (§ Step 3): Ark writes
  the design around S2 with label provenance, CC the two-page "what is the genome here" note,
  Zcode the C6 control specification.

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
  The substrate already carries a graph-level description: flyvis compiles 45,669 cells (extent
  15) from a rule bank of 2,355 `(source_type, target_type, du, dv)` rows, expanded from 605
  type-pair entries in `fib25-fib19_v2.2.json` (604 instantiate — one, `Lawf1 → Lawf1`, never
  lands on a lattice cell under its own stride). The bank equals the json up to a float32 cast
  on the 2,117 matched keys, plus 238 convex-hull fill rows and 23 dropped off-lattice
  self-offsets (Lawf1/Lawf2, `stride [3, 2]`); identical at extent 5 and extent 15
  (`docs/plans/2026-09-16-functional-readout-plan.md` Step 3 boundary paragraph). What is still
  absent is a rule that generates cell *types*, not the compiled connectivity among them;
  choosing a genome representation for growth stays off this roadmap.
- Within-type specificity. flyvis discards it by construction; nothing in Phases 1–2 can
  speak to it, and the roadmap says so rather than letting a type-level result be read as more.

## Maintenance (proposal, awaiting Mike's word)

Ark, chat 2026-09-17 08:18Z: a plan change that changes a phase's state should carry its
ROADMAP line in the same commit. Recorded as a proposal, not yet adopted as a rule.

## Status — generated

The block below is written by `tools/backlog/build.py --roadmap` from `backlog.md` and
`docs/decisions/`; it is the only status in this file that is not typed by hand, so it is the only
one that can be trusted to be current.

<!-- generated by tools/backlog/build.py --roadmap · do not edit inside -->

| axis | decisions | board entries | awaiting observation |
|---|---|---|---|
| **collective** | — | 2 | 0 |
| **knowledge** | — | 5 | 0 |
| **network** | — | 0 | 0 |
| **honesty** | ADR-002 accepted | 7 | 0 |
| **reach** | ADR-001 accepted | 2 | 0 |

**Observation debt: 0 under an axis + 0 in entries that carry none = 0.** Work finished and never seen working; per axis it says which direction is running ahead of its evidence.


Rendered from `docs/decisions/*.md` front matter and `backlog.md`. Nothing here is written by hand; correct it at the source and re-run `uv run python tools/backlog/build.py --roadmap`.

<!-- /generated -->
