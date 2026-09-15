# Next-session plan

**Date:** 2026-09-14 · **Written for:** Mike and the reviewers (Ark, Johnny, Warren, Zcode) ·
**Context:** run 0 and run 0′ are complete; the §7 replicate tolerance (< 1 % at 250,000) was
missed at 1.1104 %. Full record: `docs/experiments/001-run0-and-replicate.md`. Tooling record:
`tools/night/README.md`.

## 1. Decisions Mike must give before anything runs

1. **Instrument-floor route** — proceed as registered (top rung may come out *unmeasurable* for
   hypothesis (b), per §7's own clause) vs. write a new pre-registration for the expensive metric
   before any N run. **Note 2026-09-15:** numbers in, decision pending — night 2's three-seed
   rung SDs vs the run 0/run 0′ replicate offset are recorded in §2 below and on the board
   ([[THE-SPREAD-REPLICATE-RATIO-INVERTS-BETWEEN-C3-AND-THE-TOP-RUNG]]); the branch in §3 is now
   decidable, the call itself still waits on Mike + reviewers.
2. ~~**Night 2 = seeds 1 and 2, sequential, to 250,000, no replicate** — yes/no.~~ Decided
   2026-09-15, Mike «вноси…»/«запустил»; launched 2026-09-14T19:12:31Z, `wave_night2`.
3. **Floor N: 8 or 10** (`docs/preregistration-cheap-vs-expensive.md` §4,
   [[N-EQUALS-EIGHT-IS-BELOW-THE-FILES-OWN-MINIMUM]]).
4. ~~**Top-k as a secondary hypothesis** — enters the pre-registration or not
   ([[A-TRAINED-SURROGATE-IS-NOT-A-PREFIX-OF-THE-SAME-PROCESS]]).~~ Decided 2026-09-15,
   Mike «ок давай впишем»; form in §4/§5 of the pre-registration.
5. ~~Who fixes the PNAS line numbers in `research/analysis-cheap-step.md`.~~ Done in `dbeb878`
   (Ark's own correction applied by CC; verified lines 848–851 and 851–856).

Nothing below runs before 1–4 are answered; night 2 specifically waits on Mike's explicit word
(the standing rule, board: [[THE-NIGHT-RUN-STARTS-ONLY-ON-MIKES-EXPLICIT-WORD]]).

## 2. Night 2 — on Mike's word

Seeds 1 and 2 to 250,000, sequential, **no replicate**, determinism off, extent 15. At run 0's
price (h_run 4:00:17 + wall between runs), ≈ 8.0 h total for two runs.

Command. Until the venv is re-created outside the scratchpad (per `tools/night/README.md`), night 2 runs from the same scratchpad copy as night 1 — the scripts in `tools/night/` are byte-identical to it. This is what Mike types, one line, `-DryRun` first:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\mikha\AppData\Local\Temp\claude\c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx\63f3961a-96ce-4048-8338-72c162ea66f8\scratchpad\flyvis-probe\night\start_night.ps1" -Tag night2 -Seeds 1,2 -NoReplicate
```

(`-DryRun` first to confirm the command and ids before launching; ids will be `9991/001` and
`9991/002` — ensemble 9991 already holds `000` and `900`, which is fine, the ids differ.)

**What the morning report compares.** Between-seed distances at every rung (1,000 / 5,000 /
25,000 / 250,000) and at the 72 common checkpoints: |seed1 − seed0|, |seed2 − seed0|,
|seed2 − seed1|, against the replicate offset already on record — **+12.64 mean (min 3.68, max
17.82) / 1.1104 % at 250,000** (`docs/experiments/001-run0-and-replicate.md` §4). Decision rule,
already registered (§7): a rung whose between-seed standard deviation does not exceed the
replicate difference is *unmeasurable*, not a failed surrogate.

**Result 2026-09-15.** Both waves complete. Seed 1 (`9991/001`) EXIT rc=0, 250,008 iterations,
14,532.9 s. Seed 2's first attempt (`9991/002`) was killed at iteration 12,700 by a Windows
Update planned restart (KB5129195, see
[[WINDOWS-UPDATE-RESTARTS-INSIDE-THE-NIGHT-WINDOW-BECAUSE-ACTIVE-HOURS-END-AT-0600]]); the
partial directory was renamed to `flow/9991/002_killed_by_reboot` and excluded under §7's
resume rule (an interrupted run is a failed run). Seed 2 was re-run from scratch as wave
`night2b` (`9991/002`): started 2026-09-15T01:13:46Z, EXIT rc=0, 250,008 iterations, 14,296.6 s,
done 05:12:18Z. Mike, chat 05:19Z: «прогон завершен». Full record:
`docs/experiments/002-night2-seeds-1-and-2.md`, `results/night2/`.

Rung SD (seeds 0/1/2, n=3) against the run 0/run 0′ replicate offset:

| rung | SD (n=3) | replicate \|0′−0\| | SD/replicate |
|---|---|---|---|
| 1,000 | 0.8543 | 0.0000 | — |
| 5,000 | 0.5151 | 0.0025 | — |
| 25,000 (C3) | 7.7627 | 0.3365 | ≈ 23 |
| 250,000 | 1.7953 | 12.7279 | ≈ 0.14 |

n=3 gives an SD with 2 degrees of freedom; §7's measurability clause is applied once at the
registered N. These are distances only — no ρ, no ranks, no verdict on (b)/(b2) yet. Board:
[[NIGHT-2-RUNS-SEEDS-1-AND-2-ON-MIKES-WORD]] (closed) and
[[THE-SPREAD-REPLICATE-RATIO-INVERTS-BETWEEN-C3-AND-THE-TOP-RUNG]].

## 3. Branches after night 2

**2026-09-15:** the branch below is now decidable with the numbers in the Result paragraph
above — SD/replicate ≈ 0.14 at 250,000 (spread far smaller than the replicate offset) against
≈ 23 at C3 (spread far larger). The numbers point at (b), but the call is Mike's + reviewers',
not made here.

- **(a) Top rung measurable** (between-seed sd at 250,000 exceeds the ~12.64 / 1.11 % replicate
  offset) → continue the population per the N rule (§4): nights 3–5, seeds 3 onward, to the
  chosen floor (8 or 10, decision 3 above).
- **(b) Not measurable** → a new pre-registration for the expensive metric is required before any
  further N run. Candidates to be reviewed, not decided here: the mean over the plateau
  checkpoints (run 0's plateau: 1141.0463 at iteration 219,612; rose by +0.11 % over the last
  50,000, |change| < 0.2 %); the
  median of ≥ 2 replicates per seed; both cost extra wall-clock and neither is registered yet.
  The lower rungs (1,000 / 5,000 / 25,000) are clean under either branch and do not need this
  decision.

**Reviewers 2026-09-15 (Ark 05:35, Zcode 05:44):** sequence proposed — (i) now, free, from the 72
saved checkpoints already on disk: re-evaluate one checkpoint several times and on a second
held-out split (evaluation noise vs trajectory noise), plus weight-space distance between seed 0
and seed 0′ at 250,000 (two basins vs steep landscape); (ii) night 3 = seeds 3 and 4 (critical
path of both branches); (iii) if (b) holds, night 4 = one replicate each of seeds 0 and 1
(distribution of the offset, seed-dependence, bimodality test). Both reviewers judge neither
candidate above viable as registered: plateau mean's own SD/replicate is 0.239 (still far below
1), and the median of ≥ 2 replicates is meaningless if the end state is bimodal. Rule both ask
written into the new pre-registration verbatim: the statistic is chosen by the diagnostics, not by
the table of ratios. Full detail: `docs/experiments/002-night2-seeds-1-and-2.md` §5a. Decision
Mike.

**Second pass 2026-09-15 (Ark 05:52, Zcode 05:55):** diagnostic 1 above is revised — run one saved
checkpoint through both reporting paths (hook vs checkpoint) first, since the two paths disagree by
0.7–2.6 at the top rung with no constant offset, before any evaluation-noise study. The honest
expected label for branch (b) at the top rung is "unanswerable by this instrument at the affordable
price" (r ≈ 40 replicates needed to separate σ_within from σ_between), not a failure of the
surrogate. Night 4, if reached, should place a replicate of seed 1 SECOND in a wave whose FIRST job
is a new seed, to separate a pair-random sign from a within-wave position effect — night 2's seed 2
(solo in `night2b`) is no witness to position. Full detail:
`docs/experiments/002-night2-seeds-1-and-2.md` §5a items 9–13.

## 4. Side tasks (board entry names)

- **[[THE-NIGHT-TOOLING-LIVES-IN-A-TEMPORARY-SCRATCHPAD]]** — environment out of the scratchpad:
  recipe now in `tools/night/README.md` (this commit); remaining step is to re-create the venv
  from that recipe outside the scratchpad.
- **[[FLYVIS-RESUME-AND-RECOVER-ARE-BROKEN-IN-1-2-0]]** — upstream issue for flyvis (recover /
  resume, five defects found by execution).
- **[[DATAMATE-UNLINKS-AN-OPEN-HDF5-FILE-AND-WINDOWS-REFUSES]]** — upstream issue for datamate
  (the close-before-unlink Windows patch, `io.py`).
- **[[EIGHT-PROCESSES-SHARE-THE-CARD-NO-FASTER-THAN-ONE]]** — CUDA-graph prototype against run
  0's trajectory, after night 2 (not before — run 0 is the control); same entry also records
  extent 5 not adopted (1.46×, below the ≥ 3× bar that would have moved the night) — no further
  action on that sub-item.
- **[[THIRTEEN-LINKS-POINT-INTO-A-DIRECTORY-THAT-WILL-NOT-BE-PUSHED]]** — the 13 `chat/` links
  before the repo opens.
- Diagnostics from saved checkpoints — starting with one saved checkpoint through both reporting
  paths (hook vs checkpoint; the two disagree by 0.7–2.6 at the top rung, second pass item 10),
  then evaluation-noise re-scoring and weight distance 0↔0′ — proposed by Ark, feasible per Zcode's
  disk check; on Mike's word.

## 5. What not to do

- No change to any rule or tolerance in `docs/preregistration-cheap-vs-expensive.md` outside a
  new pre-registration written before it takes effect.
- No resume of an interrupted run (§7: an interrupted run is a failed run, re-run from the same
  seed; `resume_count > 0` excludes a run from N and from the replicate).
- No concurrent runs (m = 1 measured; aggregate throughput saturates at ≈ 17.5 it/s regardless of
  process count — [[EIGHT-PROCESSES-SHARE-THE-CARD-NO-FASTER-THAN-ONE]]).
- No GPU probes while a night run is on (production `llama-server` stays down for the duration,
  same as night 1).
