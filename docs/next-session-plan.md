# Next-session plan

**Date:** 2026-09-14 · **Written for:** Mike and the reviewers (Ark, Johnny, Warren, Zcode) ·
**Context:** run 0 and run 0′ are complete; the §7 replicate tolerance (< 1 % at 250,000) was
missed at 1.1104 %. Full record: `docs/experiments/001-run0-and-replicate.md`. Tooling record:
`tools/night/README.md`.

## 1. Decisions Mike must give before anything runs

1. **Instrument-floor route** — proceed as registered (top rung may come out *unmeasurable* for
   hypothesis (b), per §7's own clause) vs. write a new pre-registration for the expensive metric
   before any N run.
2. **Night 2 = seeds 1 and 2, sequential, to 250,000, no replicate** — yes/no.
3. **Floor N: 8 or 10** (`docs/preregistration-cheap-vs-expensive.md` §4,
   [[N-EQUALS-EIGHT-IS-BELOW-THE-FILES-OWN-MINIMUM]]).
4. **Top-k as a secondary hypothesis** — enters the pre-registration or not
   ([[A-TRAINED-SURROGATE-IS-NOT-A-PREFIX-OF-THE-SAME-PROCESS]]).
5. **Who fixes the PNAS line numbers in `research/analysis-cheap-step.md` (848–852).**

Nothing below runs before 1–4 are answered; night 2 specifically waits on Mike's explicit word
(the standing rule, board: [[THE-NIGHT-RUN-STARTS-ONLY-ON-MIKES-EXPLICIT-WORD]]).

## 2. Night 2 — on Mike's word

Seeds 1 and 2 to 250,000, sequential, **no replicate**, determinism off, extent 15. At run 0's
price (h_run 4:00:17 + wall between runs), ≈ 8.0 h total for two runs.

Command (from `tools/night/`, the venv re-created per `tools/night/README.md`):

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\night\start_night.ps1 `
    -Tag night2 -Ensemble 9991 -Seeds 1,2 -NoReplicate
```

(`-DryRun` first to confirm the command and ids before launching; ids will be `9991/001` and
`9991/002` — ensemble 9991 already holds `000` and `900`, which is fine, the ids differ.)

**What the morning report compares.** Between-seed distances at every rung (1,000 / 5,000 /
25,000 / 250,000) and at the 72 common checkpoints: |seed1 − seed0|, |seed2 − seed0|,
|seed2 − seed1|, against the replicate offset already on record — **+12.64 mean (min 3.68, max
17.82) / 1.1104 % at 250,000** (`docs/experiments/001-run0-and-replicate.md` §4). Decision rule,
already registered (§7): a rung whose between-seed standard deviation does not exceed the
replicate difference is *unmeasurable*, not a failed surrogate.

## 3. Branches after night 2

- **(a) Top rung measurable** (between-seed sd at 250,000 exceeds the ~12.64 / 1.11 % replicate
  offset) → continue the population per the N rule (§4): nights 3–5, seeds 3 onward, to the
  chosen floor (8 or 10, decision 3 above).
- **(b) Not measurable** → a new pre-registration for the expensive metric is required before any
  further N run. Candidates to be reviewed, not decided here: the mean over the plateau
  checkpoints (run 0's plateau: 1141.0463 at iteration 219,612, −0.11 % over the last 50,000); the
  median of ≥ 2 replicates per seed; both cost extra wall-clock and neither is registered yet.
  The lower rungs (1,000 / 5,000 / 25,000) are clean under either branch and do not need this
  decision.

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

## 5. What not to do

- No change to any rule or tolerance in `docs/preregistration-cheap-vs-expensive.md` outside a
  new pre-registration written before it takes effect.
- No resume of an interrupted run (§7: an interrupted run is a failed run, re-run from the same
  seed; `resume_count > 0` excludes a run from N and from the replicate).
- No concurrent runs (m = 1 measured; aggregate throughput saturates at ≈ 17.5 it/s regardless of
  process count — [[EIGHT-PROCESSES-SHARE-THE-CARD-NO-FASTER-THAN-ONE]]).
- No GPU probes while a night run is on (production `llama-server` stays down for the duration,
  same as night 1).
