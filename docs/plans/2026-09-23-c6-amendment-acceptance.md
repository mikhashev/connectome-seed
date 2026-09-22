---
**Status:** REGISTRATION. It fixes what the amended C6 exam must be able to do, and what the
amendment may not do, **before** any change to the exam.

**Scope:** it changes no harness code and runs nothing new. Every number in it is a
pre-registered constant, or a value already published in
`results/genome/c6/HARNESS-CONTROLS.md` (commit `d443cf6`).

**Written by:** CC (subagent, the builder of the harness), 2026-09-23, under option A
(Mike, owner, 2026-09-23 21:01 UTC).

**Sources:** three reviews in the DPC Research chat, read in Russian and paraphrased here:

- Ark, genome track, 2026-09-23 20:43 UTC;
- Johnny, reviewer, 2026-09-23 20:53 UTC;
- Zcode, owner of record of C6, 2026-09-23 20:58 UTC.
---

# C6 amendment 2: acceptance criteria, registered before the fix

## 0. Why this file exists

The harness controls (`results/genome/c6/HARNESS-CONTROLS.md`) found that the exam has:

- a budget arm that cannot fail (finding 1);
- an offset-set null that is weaker than the floor (finding 2);
- a random-projection arm (P4) with no bite (finding 3);
- no control showing that the exam can be passed at all.

The three reviewers agreed on option A. The corrector is the agent who built the harness and
has **not** read the proposed rule. Ark added the condition that the fix itself be checked:

> "a fix to the exam needs a control of its own, otherwise we move the hole instead of closing
> it"

(Ark, 20:43 UTC, translated). So this file states what the amended exam must be able to do, and
what the amendment may not do. It is committed on its own, before the amendment. The amendment
is then judged against this file, by code.

## (a) What the amended exam must be able to do

Each criterion has an id. The harness must print, for each id, the criterion's text, the
expected outcome, the outcome it got, and PASS or FAIL.

### Reject: a stored table beats a rule that is no better than N1

| id | criterion | expected |
|---|---|---|
| **R1** | "N1 submitted as a rule", on the real bank, **does not beat** the armed table D_k^N0 (A17 below) at its own description length, in-sample, on at least one of existence and offset set. | P2 fails for it with the label "below threshold for this family" |
| **R2** | "N0 submitted as a rule", on the real bank, is within the length limit, and **does not beat** the armed table at its own length. | P2 fails for it with the label "below threshold for this family", and **not** with "not a bottleneck" |
| **R3** | The arm is not empty at the size limit. At a budget of DL(bank) / 10 = 9,481.2 bits, the armed table stores k\*_armed ≥ **5** cells. Zcode expects about 7–10. | k\*_armed ≥ 5 |

### Accept: a planted, small, non-additive rule of known size and known strength

**The planted generator (PL).** Everything below is fixed now, before it is run.
Randomness is numpy `Generator(PCG64(4242))`, consumed in the order listed.

1. **Classes.** A permutation π of the 65 type indices (the harness's birth-id order). Type
   π[j] gets class j mod 4. That is K = 4 classes of sizes 17, 16, 16 and 16.
2. **Existence.**
   - The pattern Δ[a, b] is +1 if b = (a + 1) mod 4, else −1. This is a cycle between classes.
     It is **non-additive**: no x_a + y_b equals it.
   - At strength ρ: p[a, b] = d + ρ · (p_Δ − d), where p_Δ = 0.45 if Δ = +1 and 0.04 if
     Δ = −1, and d = 0.1425 (the density both patterns share).
   - Each of the 4,225 cells exists independently with p[class(s), class(t)].
3. **Templates.**
   - For each of the 16 class pairs, one real non-empty cell is drawn without replacement from
     the fly bank's 604, in the harness's (s, t) index order.
   - The template's offset set is that cell's `in_json` offset set.
   - Its count at **every** offset is expm1(μ_ab), where μ_ab is that cell's mean `log1p(n_syn)`.
   - A sign σ[a] is drawn per source class: +1 with probability 0.62, else −1.
4. **Content.** For each existing cell, one uniform draw u.
   - If u < ρ, the cell takes its class pair's template (offsets, counts, and sign σ[class(s)]).
   - Otherwise it takes the content (`in_json` offsets, counts, sign) of a uniformly drawn real
     non-empty cell, drawn with replacement.
   - No hull rows.
5. Strengths **ρ = 1 (PL1)** and **ρ = 0 (PL0)**, from the same seed and the same draws.
   ρ = 0.5 is run as well, descriptively.

**The planted rule (PR).** Its genome is the class vector: 65 symbols of an alphabet of 4. The
learner fits everything else from the **training cells only**, per class pair (a, b):

- the existence rate;
- the most frequent offset set, with A4's tie rule; if the class pair has no training cell,
  the set is empty;
- μ, the mean `log1p(n_syn)` over its training rows, predicted at every offset of its set;
- per source class, the majority sign, a tie giving +1.

Its decode program is its own charged file. It declares RANK = 4. Everything is charged under
A5; its DL is its "known size".

| id | criterion | expected |
|---|---|---|
| **A1** | PR on PL1 **passes C6**: P1, P2, P3 and P4 as amended, and not "did not run". | PASS verdict |
| **A2** | N1 as a rule, and N0 as a rule, on PL1 **fail** C6. | both FAIL |
| **A3** | The oracle on PL1 **fails on size**. | FAIL, with the label "not a bottleneck" |
| **A4** | A **foreign genome of the same size** loses. PR with its class vector permuted by `PCG64(99)` has exactly PR's length, and on PL1 it **fails** C6. P2 already requires the same-size stored table to lose to PR in A1. | FAIL |
| **A5** | **The margin vanishes when structure is destroyed.** PR's held-out existence margin over N1 on PL1's dial at f = 1 (mean of 5 seeds) is at most **0.25 ×** its margin at f = 0. P3 passing in A1 covers the 99 shuffles. | ratio ≤ 0.25 |

### Not trivial: the exam still says no

| id | criterion | expected |
|---|---|---|
| **N1** | PR on **PL0** (strength 0, the same seed) **fails** C6. | FAIL |
| **N2** | The PR family on the **real fly bank** (PL1's class vector, block parameters refitted) **fails** C6. | FAIL |
| **N3** | On the real bank, the registered A14 controls still do not pass: oracle, N1 as a rule, RP_r8 as a rule. | all three FAIL |

## (b) Monotonicity: what the amendment may not do (Zcode)

| id | criterion | checked by code as |
|---|---|---|
| **M1** | The A5 bit table and the one-tenth constant are untouched. | The harness's A5 functions and the constant 10 are unchanged, and DL(bank) on the real bank is still **94,812** bits |
| **M2** | P2 opponents are only **added**. The old D_k^N1 at k\* stays. The armed D_k^N0 at k\*_armed, and N1 in-sample, are added. | P2 requires all three wins |
| **M3** | The offset-set target only gets **stronger**. P1's offset arm must beat **each** of N1 (as registered), N0 and the new empirical-Bayes null N_EB in ≥ 9 of 10 folds. **Control number, registered now:** N_EB's mean held-out Jaccard on the real bank ≥ **0.4465**, which is N0's published value. Zcode measured 0.4875, but with α tuned on the same folds. | N_EB's mean ≥ 0.4465 |
| **M4** | P4 is **replaced**, not deleted. The opponent is a trained bilinear factorisation BF_r of the same rank r (A11's rank rule). The P4 threshold becomes max(the old RP threshold, BF_r's margin), so it can only rise. **Control number, registered now:** BF_8's mean held-out existence margin over N1 on the real bank must be **> 0**, so that it provably beats N1. Zcode's one-pass SVD residual gave +0.016 nats. | BF_8 margin > 0 |
| **M5** | Smoothing and penalty are **frozen by rules stated here, before any tuning** (below). The values chosen are recorded. They are not re-chosen after any rule is seen. | recorded in the output |

**Freezing rules, registered now.**

- **α of N_EB.** Choose from the grid {0.5, 1, 2, 4, 8, 16, 32, 64, 128} by **nested**
  cross-validation.
  - Inside each outer fold's training cells, each of the 9 training folds is held out in turn.
  - The chosen α maximises the mean inner held-out Jaccard over non-empty cells. A tie goes to
    the larger α.
  - The outer held-out fold never enters the choice.
  - For in-sample use, α is chosen by the same rule over all 10 folds.
- **λ of BF_r.** Choose from {1, 3, 10, 30, 100} by the same nested scheme. The criterion is
  the inner held-out existence log-likelihood; a tie goes to the larger λ.
- **N_EB, exactly.** Over the training non-empty cells:
  - g(S) is the frequency of offset set S.
  - For source s, with c_s(S) the count of S among its training cells and n_s the number of
    those cells: p_s(S) = (c_s(S) + α·g(S)) / (n_s + α).
  - Its predicted set is the observed training set A that maximises Σ_S p_s(S)·J(A, S), with
    A4's tie rule.
  - Its other fields are N1's.
- **BF_r, exactly.**
  - The model: logit = N1 logit + U_s·V_t, with U and V of size 65 × r. It minimises the
    training log-loss + (λ/2)(‖U‖² + ‖V‖²).
  - Initialisation: U and V are the rank-r SVD factors of the training residual (y − p_N1,
    0 off the training cells), each scaled by √σ.
  - It then runs 25 alternating sweeps. Each half-sweep is a batched Newton solve per row, until
    the largest gradient norm is below 1e-6, or for 20 iterations.

## (c) Re-runs

After the amendment, the four A14 controls (oracle, N1 as a rule, RP_r8 as a rule, the 99
shuffled banks) are re-run on the real bank, together with every criterion in (a). They go in
the same commit as the amendment. Every output carries the harness's sha256.

## (d) Two-way freeze (Ark)

- The exam is not edited to fit the rule.
- The rule is not edited to fit the amended exam.
- If the amended exam requires something the proposed rule does not express, that is a
  **finding**, reported as one. It is not a reason to change either side.

## (e) What the corrector has read (Ark: attested by declaration, because git cannot)

**Opened, in this whole task:**

- `docs/plans/2026-09-23-c6-control-specification.md`;
- `docs/plans/2026-09-23-grammar-track-next-steps.md`;
- in `results/genome/bank/`:
  - `README.md`, `REGISTRY.md`, `REGULARITY-READING.md`, `bank.meta.json` and
    `extract_bank.py`, all in full;
  - heads and parts of `birth_ids.csv`, `types.csv`, `type_pairs.csv` and `offsets.csv`;
  - lines of `regularity.py` (grep, and lines 55–84);
  - the structure of `regularity_results.json`;
  - grep lines of `REGULARITY-DECLARATION.md`;
- `literature.md`: the section headings, lines 400–440, 540–607, 677–721 and 1155–1206
  (§I.1 in part, §I.3 entry 18, and "What this changes for us");
- grep output lines from `ROADMAP.md`, `docs/plans/2026-09-20-genome-design-around-s2.md`,
  `tools/contamination_scan.py`, and **four lines from night-experiment files**
  (`docs/briefs/2026-09-16-step2-tuning-battery.md`,
  `docs/briefs/2026-09-17-c3-jitter-and-evaluator-floor.md`,
  `docs/experiments/002-…`, `003-…`, `004-…`). These were matches for "198" in a search for the
  old birth id. **Two of those lines carry night-3 and night-4 loss values.** I did not use
  them. They are declared here because they were seen;
- everything under `results/genome/c6/`, which I wrote;
- the chat dump holding the three reviews above, plus the two earlier CC and Zcode messages in
  the same dump. None of it states the rule's content.

**Not opened:** `docs/plans/2026-09-23-first-rule-proposal.md`. I did not read, grep, diff or
`git show` it, or anything that quotes it. Two `ls docs/plans/` listings, made while another
agent was writing it, showed no such file. My repository-wide greps for "birth" and "198" ran
before it was committed, and no line of it appeared in their output. I know of it only its path
and that it proposes a rule.

## (f) Stop condition

- If any fix cannot be made without breaking a criterion in (b), the corrector **stops and
  reports**, and does not commit that fix. Option B, a blind fresh session, is the fallback.
- A criterion in (a) that fails after the fix is reported as a failure of the amended exam.
  It is not re-tuned.

## (g) Report-only checks, defined now

- **README line.** The exam scores offset sets exactly, with no canonicalisation under the
  lattice's symmetries: 225 exact sets, and 327 when counts are included. The regularity
  measure canonicalises them, to 144 shapes.
- **The hub check (Ark).**
  - Hub set H: the 18 types with the largest leverage in the top-18 SVD subspace of L = ln(1 +
    total compiled synapses per pair), as built by `regularity.py`. The leverage of type i is
    ½·Σ_{k≤18}(U[i,k]² + V[i,k]²).
  - Set U: the 18 types whose non-empty cells (as source or as target) most often stay in place
    across the 99 shuffled banks, measured as the mean fraction unmoved.
  - Reported: |H ∩ U| against the hypergeometric expectation 18·18/65 ≈ 5.0, with its
    one-sided p; the Spearman correlation of leverage with the unmoved fraction; and the share
    of L's energy in cells whose source or target is in U.
  - **This does not change P3.** It says where P3 is weakest.
