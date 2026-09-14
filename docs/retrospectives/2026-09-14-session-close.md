# Retrospective — session S2026-09-13.1 (2026-09-13 05:57 UTC → 2026-09-14 05:54 UTC)

**Written by:** CC, on Mike's word (DPC Research chat, 2026-09-14 05:53 UTC: «Давайте ретроспективу оба»). Ark writes his own. **Audience:** Mike and the reviewers. Every claim below is Observed unless marked.

## What the session produced

- **A repository from an idea in one day.** 19 commits from `8695d26` (git init, 2026-09-13 14:22 local) to `7120fc8` (2026-09-14 12:30 local); 39 tracked files; private GitHub, CC BY 4.0. Board: 10 open, 10 closed, validated `0 refusals · 0 warnings` at every commit that touched it.
- **A pre-registration reviewed twice before anything ran** (Ark 15:45 UTC, Zcode 16:24 UTC), fifteen edits applied on Mike's word before run 0; its critical ρ table reproduced by four implementations.
- **The first scientific runs of the track.** Run 0 (seed 0) and run 0′ (seed 0 again), 250,008 iterations each, both `exit ok`, h_run 4:00:17 and 3:58:40, launched by Mike from PowerShell at 18:40 UTC, finished 02:39 UTC. Records: `docs/experiments/001-run0-and-replicate.md`, `results/night1/`.
- **The result the night was registered to give: the instrument floor.** Replicate difference 0.0000 / 0.0025 / 0.3365 / 12.73 at 1,000 / 5,000 / 25,000 / 250,000; at the top rung 1.11 % ≥ the pre-registered 1 % tolerance → §7 FAIL, recorded as such. The offset is one-sided (29/29 checkpoints after 150,000), two plateaus ≈ 1152 and ≈ 1164. Lower rungs clean by four orders of magnitude against the seed spread measured at 1,000.
- **Five measurements that each killed a reading**: concurrent processes (aggregate saturates at ≈ 17.5 it/s for k = 1/4/8; m = 1); batching (batch 16 = 3.46× the time of batch 4); extent 5 (1.46× faster, not 3.7×); the 4.4 h estimate (phase-1 probes missed `activity_penalty.stop_iter = 150000`; true h_run 4.0 h); resume (flyvis `recover()` broken; a resumed run departs ~1000× the replicate noise). Every one of them was reached by reading first and refuted by a 24–1,008-iteration run within the hour.

## What worked

1. **Pre-registration before the run.** The tolerance written at 07:55 UTC caught at 02:39 UTC what would otherwise have been read as "the seed converged". The void conditions prevented any retuning after the fact; the record says FAIL and the rules are unchanged.
2. **Execution over reading.** Ten of the day's conclusions were checked by a cheap run; five fell. None of the five would have fallen to a second reading.
3. **Three reviewers with different optics.** Ark (design, the composition test, the floor as a distribution), Zcode (source checks on flyvis, the resume test that proved decisive, the provenance corrections), and Mike's own questions («а почему прибор ломается?», «что важнее — точность или повторяемость?») that forced the SNR framing.
4. **Delegation.** ~20 subagents executed the mechanical and the measured work; the main thread kept the chat, the decisions and the verification by tool output and commit hash.

## CC's errors this session, counted

1. "The GPU idles 55 %, so concurrent processes help" — refuted by the barrier-synchronised wave.
2. "Launch-bound, so batching amortises ~N×" — refuted by the batch-size proxy. Both readings were posted to the chat as Inferred before the measurement; both were wrong in the same direction (optimistic about a speed-up).
3. "≈ 4.4 h per run" — every day-time probe measured only the phase with the activity penalty on; the two-phase schedule was in `solver.py:653` all along.
4. Sign error in the record: "loss dropped −0.11 % over the last 50,000" — it rose by +0.11 % (Zcode).
5. Two numbers in the committed record were not reproducible from committed files (phase medians, train-loss std) — the arrays had been stripped from the slim jsons (Zcode). Fixed in `dbeb878`.
6. "dpc-messenger untouched" claimed from the tree state while the tool's `close` verb had in fact snapshotted the home board (mechanism vs tree).
7. All subagents ran on Fable 5.1 until Mike asked; one died on the session limit (429). Rule since: every `Agent` call names a model, `sonnet` by default.
8. Twice piped the chat re-poll through `head`, against the standing rule; corrected by re-polling in full before sending.
9. The next-session plan cited a night-2 command from a venv that does not exist yet; fixed in `110d17e`.

Pattern: errors 1–3 are one class — extrapolating from a probe that did not cover the regime the claim was about (schedule phases, contexts, lattice). Errors 4–5 are provenance: a number in a record without a committed file behind it. The reviewers caught 4–6; execution caught 1–3; Mike caught 7; the rule caught 8.

## What the reviewers changed

Ark: the (a)/(b) separation, the identical-copies objection, the two-sided (a) criterion, the extent-5 proposal (measured, rejected), the SNR framing, the floor as a distribution (min +3.68 / median +12.25 / max +17.82). Zcode: the flyvis source checks, the resume test (3.4), off-by-one prose, H_avail horizon, floor 8 vs 10, the exact ρ rows, two provenance fixes, the retraction of his own 150k-shock hypothesis by data. Both retracted a claim of their own during the session; so did CC.

## Open at close (all wait on Mike's word)

- Instrument-floor route: proceed as registered (top rung may come out unmeasurable) vs new pre-registration of the expensive metric before the N runs.
- Night 2 = seeds 1 and 2, no replicate — yes/no (command ready, `-DryRun` first).
- Floor N 8 or 10 (after night 2, per Zcode).
- Top-k as a secondary hypothesis, form fixed before night 2 if yes.
- Housekeeping: venv out of the scratchpad (recipe in `tools/night/README.md`); upstream issues for datamate and flyvis; CUDA-graph prototype after night 2; 13 `chat/` links before the repo opens.

Plan: `docs/next-session-plan.md`.
