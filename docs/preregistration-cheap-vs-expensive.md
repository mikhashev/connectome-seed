# Pre-registration — does a cheap evaluation of a flyvis individual agree with an expensive one?

**Date:** 2026-09-13 · **Status:** DRAFT; reviewed by Ark 2026-09-13 15:45 UTC (seven points, all accepted by CC, edits pending Mike's word); 24–48-iteration probes have run, run 0 not yet · **Substrate:** flyvis 1.2.0 (Lappalainen et al., Nature 2024)

Every number below carries its origin. **[FIXED]** = verified on this machine or in the flyvis defaults on 2026-09-13, not to be altered. **(proposed — fix in review)** = a choice made in this draft that the reviewers (Johnny, Ark, Warren) confirm or replace *before* the first GPU iteration. Once run 0 starts, nothing in §3–§5 changes; see §7.

---

## 1. Purpose and the two hypotheses, kept separate

Two independent sources place the unproven step of an evolutionary loop at the same point: cheap evaluation mis-ranks newly mutated individuals (Mertan & Cheney, arXiv 2508.17464, §3.1/§4.2, 1,305,840 bodies), and the one published circuit-to-genome codec works only with gradients reaching the genome (Shuvaev et al., PNAS 2024, p. 9). This experiment measures that step on a real connectome-constrained circuit. Both outcomes are results *because* the numbers are fixed here first.

- **(a) Composition.** A module spliced from one individual into another behaves predictably — the host's behaviour changes by less than a stated tolerance (§5).
- **(b) Evaluation.** A cheap evaluation ranks N individuals the same way an expensive one does (§3–§5).

A result on (a) says nothing about (b), and the reverse. Each has its own decision rule (§5) and its own invalidation conditions (§7). They share the trained individuals and nothing else.

## 2. Individuals

**Model** [FIXED]: flyvis 1.2.0, default connectome `fib25-fib19_v2.2.json`, `extent=15` → 45,669 nodes, 1,513,231 edges, 65 unique cell types; trainable parameters: network core 734 free (2,959 fixed) + decoder 7,427. The node count is a lattice parameter (`extent=5` gives 5,759 nodes), not a biological count. The connectome source is FIB-25 / FIB-19 (Janelia), not FlyWire.

**Task** [FIXED]: optic-flow estimation on MPI-Sintel, flyvis default task `flow`; images `training/final`, ground truth `training/flow`.

**One individual** = one flyvis network of the configuration above, trained from one random seed on the task, with the default expensive schedule (§3). The seed sets parameter initialisation and data order. This is the flyvis notion of an ensemble member.

*Observed 2026-09-13 (CC's subagent, flyvis 1.2.0 source in the run venv; verified by CC):* the previous sentence is true only under the run script's override. In stock flyvis `ensemble_and_network_id` sets no seed; the only seeded initialisation is the resting potential (`config/network/node_config/bias/bias.yaml: seed: 0`; `network/initialization.py:159-164`, a local `torch.Generator`). Data order and augmentation draw from unseeded global RNGs (`task/tasks.py:91` — `SubsetRandomSampler` without a generator; `datasets/augmentation/hex.py:103-104, 205-206, 320` — `np.random` / `torch.randn_like`). The run script (`night/run_individual.py`, scratchpad) therefore overrides `network.node_config.bias.seed=<seed>` and sets the `random`, `numpy` and `torch` manual seeds, and its json asserts the bias seed (`bias_seed_in_network_config: 0`, `hydra_overrides` includes `network.node_config.bias.seed=0` in `night/dry_9990-000.json`).

**Source of variation across the N individuals** (proposed — fix in review): different random seeds only, seeds `0 … N−1`, same connectome, same task, same schedule. No perturbation of the connectome and no spliced individuals enter the population used for (b). Reason: (b) needs individuals whose expensive ranking is well defined; a spliced individual would import the outcome of (a) into the population for (b), which is the entanglement §1 forbids.

**Splice for (a)** (to be fixed in review — Ark's proposal): the module is one cell type's free parameters (its node parameters and the synapse parameters of its incoming edges) copied from individual B into individual A, all else in A unchanged. Which cell type, and which pair (A, B): Ark fixes. **Forbidden control:** A spliced with a copy of itself, or two identical copies of any member — a control that can only pass. B must be a *different* ensemble member (different seed) or the module must be a *different* cell type than the one it replaces.

**Fixed 2026-09-13 (Ark, chat 15:45 UTC; k computed by CC):** the module is the cell type with the largest share of free parameters — its node parameters plus the parameters of its incoming edges, grouped by target type; the pair is **A = seed 0, B = seed 1**. Measured (`param_share_by_type.py` → `param_share_by_type.json` / `.md`, scratchpad; the grouping is flyvis's own: `network/initialization.py:345-356` nodes by `type`, `:496-515` edges by `(source_type, target_type)`): the 734 free core parameters are 65 `nodes_bias` + 65 `nodes_time_const` + 604 `edges_syn_strength` (one per (source_type, target_type) pair); `edges_sign` (604) and `edges_syn_count` (2,355) are fixed. Module sizes over the 65 types sum to 734 (asserted in the script). Largest: **T2, k = 26 of 734 = 3.54 %** — 2 node parameters + 24 incoming edge types (C2, C3, L4, L5, Mi1, Mi13, Mi2, Mi3, Mi9, T2 self, T3, T5b, T5d, Tm1, Tm16, Tm2, Tm3, Tm4, TmY13, TmY15, TmY18, TmY3, TmY4, TmY5a). Next: Mi9 21, TmY15 20, TmY4 20, Mi1 19, Mi4 19. Median k = 12, minimum 3 (Mi11, R6, R7, R8, Tm30). The (a) criterion in §5 is unchanged in this revision; Ark's proposed rewording waits for Mike's word.

## 3. Definitions of cheap and expensive, in iterations

**Expensive** [FIXED] = flyvis default full training: `n_iters = 250000`, batch size 4, learning rate 5e-5 decaying to 5e-6 (scheduler), checkpoint every 300 epochs. **Wall-clock per iteration on this card** [FIXED]: **0.0619 s** per training iteration within an epoch (mean, n = 22, min 0.0589 s, max 0.0694 s), hence 250,000 iterations = 15,475 s = **4.30 h**, and ≈ **4.6 h** all-in with ~70 checkpoints (0.73–0.90 s each) at `chkpt_every_epoch: 300` plus per-epoch overhead (0.010–0.016 s steady state, 0.30 s post-epoch h5 writes); peak VRAM 1,402 MiB torch-allocated, 1,512 MiB reserved, 4,568 MiB on the card over a 2,565 MiB desktop baseline. Provenance: measured 2026-09-13 11:26–11:28 UTC on the NVIDIA RTX PRO 4500 Blackwell (compute capability 12.0, 32 GB), torch 2.9.1+cu128, flyvis 1.2.0, Windows, default `flow` config (batch 4, extent 15); two runs of 24 iterations (2 epochs × 12 batches), `flyvis train-single` and the same config in-process with timing after `torch.cuda.synchronize()`; per-iteration times are consecutive `iter_end` deltas in `scratchpad/flyvis-probe/gpu_price_probe_instrumented.json` (scratchpad, outside this repository). This is the Phase 2 step-1 probe, not run 0; run 0 records its own figure per §6. The CPU figures already measured (`Network()` 13.1 s; forward 0.06 s / backward 0.05 s for 20 frames, synthetic full-node stimulus) are not a training iteration and are not used for any estimate here.

**Cheap ladder** (proposed — fix in review), chosen now, three rungs as fractions of expensive:

| rung | fraction | iterations |
|---|---|---|
| C1 | 0.4 % | 1,000 |
| C2 | 2 % | 5,000 |
| C3 | 10 % | 25,000 |

The ladder does not change after any result is seen (§7). A rung is added or moved only in review, before run 0.

**Cheap is a prefix of expensive** (proposed — fix in review): the cheap evaluation of individual *i* at rung C*k* is the held-out metric of the *same* training run at iteration C*k*, with the expensive schedule (the learning-rate scheduler is set for 250,000 iterations and is not compressed). So N expensive runs yield all rungs at no extra cost. A standalone short run with its own compressed schedule is a *different* cheap evaluation and is not tested here (§8).

**Ranking metric at every budget** (proposed — fix in review): the task loss used by flyvis for `flow` (its default `flow` loss, unchanged), computed on the **held-out Sintel split** — the validation split flyvis's default task config defines over Sintel *sequences*. The list of held-out sequence names is printed from the task config and pasted into this file before run 0. If the default config defines no held-out split, 20 % of sequences (by sequence, never by frame, drawn with seed 0) are held out and the same list is used for all N. The metric is recorded at exactly iterations 1,000 / 5,000 / 25,000 / 250,000 by an evaluation hook in the training loop, not by the nearest checkpoint — the 300-epoch checkpoint cadence need not coincide with the rungs.

**Held-out split, printed 2026-09-13 [FIXED]** (flyvis default `original_split: true`, `datasets/sintel_utils.py:249-276`, indices 37 and 38 removed at `:290-291`; the list below is the `split` field of the dry run `night/dry_9990-000.json`, scratchpad). Held-out scenes (6): ambush_2, bamboo_1, bandage_1, cave_4, market_2, mountain_1 → 16 items, batch size 1, `IndexSampler`. Training scenes (17): alley_1, alley_2, ambush_4, ambush_5, ambush_6, ambush_7, bamboo_2, bandage_2, cave_2, market_5, market_6, shaman_2, shaman_3, sleeping_1, sleeping_2, temple_2, temple_3 → 51 items, batch size 4, 12 batches per epoch. Intersection: empty, by scene and by item. Two items are in neither list — `sequence_12_cave_4_split_01`, `sequence_12_cave_4_split_02` — excluded by flyvis. The 20 %-with-seed-0 fallback above is therefore not used. Augmentation: the training context enables jitter / rotate / flip / noise / gamma (`solver.py:271, 294`), validation runs under `augmentation(False)` (`solver.py:514`); the flags measured in the dry run agree (`augmentation` field of the same json: train `jitter/rotate/flip/noise/gamma_correct: True`, val all `False`). Checkpoint cadence: observed in the 48-iteration dry run at iterations 0, 12 and 48 (the last) — i.e. iteration 0, the end of the first epoch, and the end; inferred for a full run, every 3,600 iterations thereafter (`chkpt_every_epoch: 300` × 12 batches). The evaluation hook's held-out loss equals flyvis's own checkpoint validation loss bit-for-bit (dry run, iteration 12: 1212.257435798645 from both).

## 4. Statistic and threshold for (b)

**Statistic:** Spearman rank correlation ρ between the cheap ranking (held-out loss at rung C*k*, ascending) and the expensive ranking (held-out loss at 250,000, ascending) over the N individuals, one ρ per rung. Ties are not expected with a continuous loss; if a tie occurs it is broken by the midrank convention and noted.

**Test:** one-sided, H1: ρ > 0, α = 0.05. Critical values computed on 2026-09-13 for this draft, not quoted from a table:

| N | critical ρ (reject if ρ ≥) | exact tail P(ρ ≥ crit) | method |
|---|---|---|---|
| 8 | 0.6429 | 0.0481 | exact, all 8! = 40,320 permutations |
| 10 | 0.5636 | 0.0481 | exact, all 10! = 3,628,800 permutations |
| 12 | 0.5035 | 0.0495 | Monte Carlo, 2 × 10⁶ random permutations, two seeds agree to 4 decimals |
| 16 | 0.4294 | 0.0494 | Monte Carlo, as above |
| 20 | 0.3805 | 0.0496 | Monte Carlo, as above |

Method: for N ≤ 10 the full permutation distribution of Σd² under H0 (uniform random ranking) was enumerated and the critical ρ taken as the smallest value with P(ρ_perm ≥ ρ) ≤ 0.05; for N > 10 the same rule over 2 × 10⁶ uniformly random permutations (numpy 2.5.2 under Python 3.12.10, `C:/Users/mikha/AppData/Local/Programs/Python/Python312/python.exe`, no scipy — the t cross-check below is the scipy-free one; seeds 0 and 1, identical to 4 decimals). Re-run independently by CC on 2026-09-13 with that same interpreter: all five rows reproduced, N = 8 → 0.6429 and N = 10 → 0.5636 exactly. Cross-check: the t-approximation t = ρ√((N−2)/(1−ρ²)) with the t quantile obtained by numerical integration gives 0.6215 / 0.5494 / 0.4973 / 0.4259 / 0.3783 — a few thousandths *below* the exact values, as expected for small N; the exact/permutation column is the one that binds. Script: `crit_rho.py` and `crit_rho_check.py` in `docs/prereg-scripts/` ([crit_rho.py](prereg-scripts/crit_rho.py), [crit_rho_check.py](prereg-scripts/crit_rho_check.py)).

**Pre-registered N** (proposed — fix in review): **N = 10** is the minimum at which the test is meaningful — at N = 10 a perfect-minus-one-swap ranking (ρ = 0.988) passes and a coin-flip ranking passes 4.8 % of the time; below 8 the critical ρ exceeds 0.64 and only near-perfect agreement can be detected. The final N is set by run 0, as a rule, not a number:

> N = floor( H_avail / h_run ), where h_run is the measured wall-clock of run 0 to 250,000 iterations (§6) and H_avail is the GPU-hours Mike allocates to overnight maintenance windows; if run 0's VRAM peak allows m concurrent runs on 32 GB with per-run throughput measured to be ≥ 80 % of solo, N = floor( m · H_avail / h_run ). N is never below 8. If the rule yields N < 8, the experiment does not run at that budget and the shortfall is reported as the result of Phase 2 step 1.

**m, measured 2026-09-13 [FIXED]** (CC's subagents, verified by CC; `gpu_concb_9996_*.json` for k = 4, `gpu_concb_9995_*.json` for k = 8, `gpu_concb_nvsmi.log`, analysed by `gpu_concb_analyze.py`, all in the scratchpad): barrier-synchronised waves of k identical processes, 240 iterations each, RTX PRO 4500 Blackwell in `Compute Mode: Default` (time-sliced; no MPS on Windows). Within-epoch s/iter in the window where all k processes train: k = 1 → 0.0619 s (16.2 it/s); k = 4 → 0.2281 s per process (3.69×), aggregate 17.5 it/s, card peak 10,116 MiB, util peak 91 %; k = 8 → 0.4502 s per process (7.27×), aggregate 17.8 it/s, card peak 17,542 MiB, util peak 92 %. Aggregate throughput saturates at ≈ 17.5 it/s for any k, so per-run throughput at k ≥ 2 is far below the 80 % of solo the rule requires: **m = 1**. Inferred: with H_avail = 8–9 h per night and h_run ≈ 4.3–4.6 h, a night holds two sequential runs; N = 8 needs four nights. Reported: Ark (chat, 15:45 UTC) named this measurement "a gate for (b), not an optimisation".

The chosen N is written into this file, with the arithmetic, before any run after run 0 is started. The critical ρ for that N is read from the table above (or computed by the same script if N is not in the table) and written next to it.

## 5. Decision rules, both outcomes

**(b) Evaluation.** For each rung C*k* compute ρ_k and compare with the critical value for the registered N.

- If some rung reaches critical: **"A cheap surrogate exists at that budget."** Report the *smallest* such rung and all three ρ values with their exact tail probabilities. Rungs above the smallest passing one are reported, not used to relabel the result.
- If no rung reaches critical: **"No cheap surrogate at ≤ 10 % of expensive on this substrate."** This extends 2508.17464 from a 3×3 voxel grid and a 1,417-parameter controller to a connectome-constrained circuit on 65 cell types with 734 free core parameters. All three ρ values are reported; a ρ that is large but below critical is reported as below critical.
- Not reported as a result: any ρ from a rung not in §3, any ρ over a subset of the N individuals, any second metric.

**(a) Composition.** Named prediction (proposed — fix in review): after splicing the chosen module from B into A (§2), A's held-out task loss (§3 metric, same held-out split, no retraining after the splice) changes by **less than 5 % relative** to A's own held-out loss at 250,000 iterations. The 5 % is fixed now. Interpretation: within tolerance → "the type-level module composes predictably for this pair"; outside tolerance → "it does not; the module's meaning depends on its host". Either way the statement is about *one* pair and *one* cell type and is reported at that size; it is neither a statement about (b) nor about within-type specificity (§8). If Ark's proposal names a different observable than task loss (e.g. a cell-type response to a fixed stimulus set), the observable and its tolerance replace this paragraph in review, before run 0.

## 6. What run 0 (K = 1) is and is not

Decision (Mike, 2026-09-13): **K = 1 to begin with** — one full run to 250,000 iterations before anything else is scheduled.

Run 0 **can** establish: the price of expensive on this card; one converged reference individual (seed 0), which is also individual 1 of the N; and that the whole flow — Sintel on disk, the `datamate` close-before-unlink patch, training, evaluation hook, checkpointing — runs end to end on the GPU.

Run 0 **cannot** establish anything about hypothesis (b): with N = 1 no ranking and no rank correlation exists, and no rung of the ladder can be scored. It cannot establish (a) either, since a splice needs a second, different individual.

Recorded from run 0, all of them, before the N rule (§4) is applied:

- wall-clock per iteration (median over iterations 1,000–2,000, after warm-up) and total wall-clock to 250,000;
- VRAM peak (`torch.cuda.max_memory_allocated` and the driver's view);
- held-out loss at 1,000 / 5,000 / 25,000 / 250,000 (the evaluation hook working is itself a flow check);
- the checkpoint cadence actually observed (iterations per epoch on this Sintel split, hence iterations between checkpoints);
- the flyvis version, connectome file hash, the task config as resolved, the held-out sequence list, the seed, and the git commit of the local patch.

Run 0 starts only in a maintenance window with production down (ROADMAP Phase 2, step 1).

## 7. Controls, and what would invalidate the run

**Instrument agreement, first.** Before the N runs: seed 0 trained twice with the same config (run 0 and run 0′). Expectation: **not bit-exact on GPU** — non-deterministic kernels and reduction order; torch determinism flags are set where flyvis permits and the residual is measured. The tolerance that replaces bit-exactness (proposed — fix in review): |loss₀ − loss₀′| / loss₀ at 250,000 must be **< 1 %**, and — the condition that matters for (b) — the replicate difference at every rung must be **smaller than the range of held-out losses across the N individuals at that rung**. If the between-seed range at a rung does not exceed the replicate difference, ranks at that rung are instrument noise and that rung is reported as *unmeasurable*, not as a failure of the surrogate. Run 0′ counts against the budget in §4.

**Determinism flags, cost measured 2026-09-13** (`night/dry_9990-000.json` flags on vs `night/nodet_9990-010.json` flags off, scratchpad; 48 iterations each, seed 0, same config): with `CUBLAS_WORKSPACE_CONFIG=:4096:8`, `cudnn.deterministic=True`, `cudnn.benchmark=False`, `torch.use_deterministic_algorithms(True, warn_only=True)`, no op warns (`nondeterministic_ops: {}`), but the median per-iteration time is **0.2335 s — 3.77× the 0.0619 s of §3** → ≈ 16.2 h per 250,000-iteration run; without the flags 0.0620 s. Held-out losses differ between the two modes at the 7th significant digit (iteration 12: 1212.257435798645 with flags, 1212.2575216293335 without). **Decision pending (Mike).** CC recommends flags off for run 0 / run 0′: this section already measures the replicate residual, and the night window holds two runs only without the flags.

**Data leakage.** Held-out and training are disjoint *by sequence*; the intersection of the two sequence-name lists is printed and must be empty; augmentations (flips, rotations, whatever flyvis's `flow` task applies) are confirmed to apply to the training split only. A non-empty intersection voids every metric.

**Void conditions.** The run is void, and is reported as void, if after any result is seen: the cheap ladder is changed; N is changed; the ranking metric or held-out split is changed; the (a) tolerance or observable is changed; individuals are dropped. A failed run (crash, NaN) is re-run from the same seed and the failure is logged; it is not replaced by a different seed.

## 8. What this experiment does NOT test

- **Within-type specificity.** flyvis pools neurons by cell type with retinotopic tiling; specificity within a type is discarded by construction, and no result here speaks to it.
- **Bodies, curricula, USPEX operators, growth, a genome representation.** None of these exist in this experiment.
- **Whether a trained individual is "good".** Only whether the cheap and expensive evaluations *agree in rank*; absolute loss values are recorded but carry no decision.
- **Standalone short training** with its own compressed schedule as the cheap evaluation (§3). A negative here says the *prefix* of expensive does not rank; it does not say that no cheap procedure could.
- **Generalisation beyond this substrate**: one connectome release, one task, one loss, one card.

## 9. Provenance

- **Date:** 2026-09-13.
- **Decisions:** Mike — the condition (ADR-002), K = 1, order of execution (flow first, long runs overnight), roles.
- **Design:** Ark — the composition test (a), the separation of (a) from (b), the identical-copies objection, the second ground for the condition (PNAS p. 9). Reviewers' five-item demand (Johnny, Ark, Warren): cheap/expensive in iterations; number of individuals and seeds; statistic and threshold at that N; decision rule per outcome; named prediction for composition.
- **Sources:** `README.md`, `VISION.md`, `ROADMAP.md`, `literature.md` §D and §F, `docs/decisions/002-file-under-condition.md` of `connectome-seed`, read 2026-09-13.
- **This draft:** written by CC's subagent to the scratchpad; placed in the repository on 2026-09-13 for review, with its scripts beside it in `docs/prereg-scripts/`. It becomes the pre-registration only after review and only in the version committed before run 0.
- **Open for review, with the marks above:** source of variation (§2); the splice — pair and cell type (§2, Ark); ladder rungs and prefix definition (§3); held-out split and metric (§3); N = 10 minimum and the N rule (§4); the 5 % tolerance and the (a) observable (§5); the 1 % replicate tolerance (§7).
