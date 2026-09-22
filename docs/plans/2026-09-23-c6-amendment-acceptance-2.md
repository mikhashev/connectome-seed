---
**Status:** REGISTRATION. This file adds items the review of Amendment 2 requires before any rule
is run. It is committed **before** the A6 object below is written or run. It does not edit the
first acceptance file (`docs/plans/2026-09-23-c6-amendment-acceptance.md`), which the harness
locks by hash.

**Written by:** CC (subagent, the builder and corrector of the harness), 2026-09-23.

**Sources:**
- Ark, genome track, review of the amendment's content, 2026-09-23 21:35 and 21:44 UTC;
- Zcode, owner of record of C6, mechanical check, 2026-09-23 21:43 UTC.

These are relayed by the coordinator and paraphrased or translated from Russian. The amendment
itself (commit `dd34f9d`) is accepted.
---

# C6 amendment 2: acceptance, part 2

## 1. A6: a working weak object that loses on the budget arm alone

**What Ark asks for** (translated from Russian): *"One working weak object that passes P1/P3/P4
and loses specifically on the budget arm, with the recorded branch label. Without it, the arm has
shown capacity but not bite."*

**The object, PR-sh.** It is the planted rule's family, with PL1's true class vector, but its
class-pair parameters are trained on **shuffled training cells**. This is Ark's first
suggestion, built only from machinery already in the harness.

- **Learner.** Take the fold's training cells in the view's order.
  1. With `Generator(PCG64(7))`, used afresh for every fit: permute the existence labels among
     the training cells (`permutation(n_train)`).
  2. Then permute the training non-empty contents (offsets, counts, sign), in sorted
     `(s, t)` order, over the new non-empty cells in sorted order
     (`permutation(n_nonempty)`).
  3. Then fit PR's block parameters (`fit_planted`, PL1's class vector) on the shuffled cells.
- **Program:** `decoders/planted_decode.py`, the same program as PR. RANK = 4.
- **Bank:** PL1 (seed 4242, ρ = 1).
- **Size:** whatever its full-bank fit charges under A5. PR's data shapes predict about 4.8–5.0
  kbits. At that size k\*_armed = 0 on PL1, so its armed opponent is D_0^N0, which is N0 plus
  the armed program.

| id | criterion | expected (Ark's requirement) |
|---|---|---|
| **A6** | PR-sh on PL1 passes P1, P3 and P4 and is within P2's length limit. In-sample it beats D_k^N1 at k\* and N1, and does **not** beat D_k^N0 at k\*_armed on at least one of existence and offset set. It is not "did not run". | verdict FAIL with exactly one label: **"below threshold for this family"** |
| **A6-D** | **Whether any object can do this at all.** On the real bank and on PL1, for some k in 0…k\*_armed(DL(bank) / 10), D_k^N0 beats N1 in-sample on existence or on offset set. P2 requires every rule to beat N1 in-sample (A17). If the armed table is worse than N1 on both fields at every affordable k, then no object that clears the N1 opponent can lose to the armed table. A6 is then impossible for *any* object, not just PR-sh. | yes, for at least one k on at least one bank |

**The corrector's prior, registered before the run.** I expect **both A6 and A6-D to fail**. The
arithmetic uses only numbers already published in `HARNESS-CONTROLS.md` (commit `dd34f9d`):

- **Existence, real bank.** N1 in-sample 0.335; N0 in-sample 0.410. Each stored cell improves
  the armed table by at most (−ln 0.146 − 0.001) / 4225 ≈ 0.00045. So 7 cells cannot close a
  gap of 0.075.
- **Offset set, real bank.** N1 in-sample 0.496; N0 0.447. Seven cells add at most 7/604 ≈
  0.012.
- **PL1.** Existence: N1 0.405, the armed table at k = 0 0.416. Offset set: N1 0.869, the armed
  table at k = 0 0.353. PL1's size limit is 13,383 bits.

**If this prior holds**, the finding is: *within the size limit, the budget arm is dominated by
the N1 opponent, and it can never be the sole reason a rule fails.* The object is **not** bent to
produce the label. That includes padding it past 7,721 bits, choosing another bank, or changing
the storage format.

## 2. What the budget arm is for (the arm-role line)

In Ark's words (translated from Russian): **"The Clune threshold here is defended by P1/P2
against N0/N1/N_EB/BF. The budget arm defends something else: the rule must not be a partial
download of the answer. In the 7.7–9.5 kbit band the verdict rests on N1 and the shuffle, not on
storage."**

**R1 and the narrow band are one fact.** HARNESS-CONTROLS.md reported two things:

- R1's failure: at N1's own size, 25 stored cells do not beat N1.
- The band: below 7,721 bits the armed table is N0, and at the limit it holds 7 cells.

They are the same fact: **honest storage of this matrix is a weak predictor at any length we can
afford.** They have one home, here. **R1's recorded FAIL stands.** It is not re-scored or
re-worded.

## 3. Naming: three different "18"s

- **k90** is a **count**: the number of singular components of L = ln(1 + N) that hold 90 % of
  its energy. Its value is 18 (`results/genome/bank/REGULARITY-READING.md` §2). It is not a set
  of types.
- **H18** is a **set of types**: the top 18 types by leverage in the rank-k90 SVD subspace of L.
- **U18** is a **set of types**: the top 18 types by the fraction of their cells left unmoved by
  the 99 shuffles.
- **The set size 18 in H18 and U18 was borrowed from k90.** It is a convention, not something
  measured about the sets.
- **Is the harness's L the same as regularity.py's L? Yes, exactly.**
  - `regularity.py` sums the compiled `n_syn` per pair over `in_json` and `hull_filled` rows,
    and every hull row has `n_syn = 1.0`.
  - The harness sums the compiled `in_json` counts and adds 1.0 per hull row.
  - Recomputed on all 4,225 cells: 0 cells differ, and the maximum absolute difference is 0.0.
- No number changes.

## 4. What A1 speaks to

PL1 has **617** non-empty cells and DL(bank) = **133,827** bits, against the real bank's 604
cells and 94,812 bits. So A1 (the planted rule passes) speaks to the **logic of the exam**, not to
the real bank's budget.

## 5. Procedure and freeze

- The harness refuses to run if this file changes (A23).
- A6 and A6-D are run in the commit after this one. They are printed PASS or FAIL against the
  text above.
- The two-way freeze of the first acceptance file §(d) applies.

**Declaration, continuing the first file's §(e).** Since that declaration I have opened only files
I wrote or am amending:

- the spec, both acceptance files, and `results/genome/c6/*`;
- lines 55–84 of `results/genome/bank/regularity.py`, and the structure of
  `regularity_results.json`;
- `results/genome/bank/offsets.csv`, for the L check.

The reviews of 21:35, 21:43 and 21:44 UTC reached me only through the coordinator's summary.
**The rule proposal (`docs/plans/2026-09-23-first-rule-proposal.md`, commit `5a46886`) has still
not been opened, grepped, diffed or shown.** No rule has been run.
