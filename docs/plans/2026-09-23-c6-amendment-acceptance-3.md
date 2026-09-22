---
**Status:** REGISTRATION. It is committed **before** any code change it describes. It does not
edit the first two acceptance files, which the harness locks by hash.

**Written by:** CC (subagent, the builder and corrector of the harness), 2026-09-23.

**Source:** Ark, genome track, 2026-09-23 21:48 UTC, relayed by the coordinator and paraphrased:
*search is free in description length, so an opponent given less search than the rule is a
weaker opponent.*
---

# C6 amendment 2: acceptance, part 3 — search-budget parity

## The problem

- BF_r, the trained opponent of P4 (A19), is fitted from one deterministic start, the SVD start,
  with no restarts.
- A candidate rule may be fitted with k restarts: 10, or 3 if a timing cap fires.
- The number of starts is not charged in A5, so the rule gets search the opponent does not.

## (a) Every trained opponent gets the same number of starts k as the rule under test

**Start 0 is the SVD start.** It is registered from now on (item (d)).

**Starts j = 1 … k − 1 perturb start 0.**

- U_j = U_0 + ε·G_U,j and V_j = V_0 + ε·G_V,j.
- G_U,j and G_V,j are 65 × r arrays of iid N(0, 1). They are drawn in that order from numpy
  `Generator(PCG64(30000 + j))`.
- The scale is ε = max(0.5 · RMS(all entries of U_0 and V_0), 0.05).
- The seeds are the same in every fit, so every fit is deterministic.

**Each start is refined** exactly as in A19: 25 alternating sweeps of batched per-row Newton,
until the largest gradient norm is below 1e-6, or for 20 iterations.

**The best start is chosen on the training loss only.** That loss is the penalised training
objective the fit minimises: the sum of log-loss over the training cells, plus (λ/2)(‖U‖² + ‖V‖²).
A tie goes to the lower j. No held-out cell enters the choice.

**Where it applies.** It applies to every BF_r fit: the inner fits of λ's nested choice, and the
final fit.

**Monotonicity.** Start 0 is always among the candidates, and the choice minimises the training
objective. So the chosen fit's training objective is never worse than at k = 1. The opponent can
only be as strong or stronger in what it optimises. Its held-out margin is not guaranteed to rise.
It is reported at each k, and it is not used to pick k.

## (b) k is a harness parameter, and it is printed everywhere

- `harness.py --starts K` sets k. The default is 10.
- k is recorded, and printed next to every verdict and every P1, P2 and P4 margin, in the log,
  in `harness_controls.json` and in `HARNESS-CONTROLS.md`.
- If a rule's `fit` accepts a `starts` argument, the harness passes the same k to it.

## (c) The timing cap is decided once, before any arm runs

- The choice of 10 or 3 restarts is made once, before any arm runs. It is fixed for the whole
  run, and it applies to every fit of every arm, including the 99 P3 shuffles, the dial and the
  leave-one-type-out split, and to BF's k as well.
- **The criterion that decides it belongs to the rule's registration.** I have not read that
  registration. The harness takes the outcome as the input `--starts`, before any arm runs, and
  never changes it during a run.

## (d) The SVD start's scale is registered from now on

HARNESS-CONTROLS.md flagged one unregistered implementation detail: the scale of BF_r's
initialisation. It is registered now, as implemented since commit `dd34f9d`:

- the residual is taken in **probability units**: E = y − σ(N1 logit) on the training cells,
  and 0 elsewhere;
- with E = u·diag(s)·vᵀ its SVD, U_0 = u[:, :r]·√s[:r] and V_0 = v[:, :r]·√s[:r];
- no further rescaling.

## Criteria (checked by code)

| id | criterion | expected |
|---|---|---|
| **S1** | The run's k is recorded, and printed next to every verdict and every P1, P2 and P4 margin. | yes |
| **S2** | M4 still holds at k = 10: BF_8's mean held-out existence margin over N1 on the real bank is > 0. | > 0 |
| **S3** | M4 still holds at k = 3 (run if affordable). | > 0 |
| **S4** | With multiple starts, BF_8's training objective is never worse than at k = 1, in every fit. | yes (by construction; checked) |

BF_8's margins on the real bank are reported at k = 1, 3 and 10.

**Declaration.** The rule proposal (commit `5a46886`) has still not been opened. No rule has been
run.
