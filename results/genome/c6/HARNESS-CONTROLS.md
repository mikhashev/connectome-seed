# C6 harness controls: the exam run with no rule

**Written:** 2026-09-23, by CC (subagent), on Mike's word ("build the C6 exam without a rule, so
the exam itself can be checked", paraphrased from Russian).

**Status:** a check of the exam itself. **No rule was run.** A rule proposal exists elsewhere in
`docs/plans/`; it was not read, and it is not registered.

**Run:** `tools/.venv/Scripts/python.exe results/genome/c6/harness.py --controls` (CPU, about
2 minutes). All numbers below are in `harness_controls.json`, which also records the sha256 of
the spec, the folds, the harness and each decoder.

**Specification:** `docs/plans/2026-09-23-c6-control-specification.md` with its Amendment (A1–A15),
at the hash in `folds.meta.json`. The harness refuses to run if the spec or `folds.csv` changes.

## Files

| file | what it is |
|---|---|
| `harness.py` | the exam: loading, nulls N0 and N1, D_k, S_all (the stored bank), the random-projection arm, the shuffled banks and the dial, the leave-one-type-out split, description length, P1–P4, the labels, and the plug-in interface for a rule (in its docstring) |
| `decoders/*.py` | the **charged** decode programs of the built-in predictors: `n1_decode`, `n0_decode`, `store_decode`, `dk_decode` (= n1 + store + itself), `rp_decode` (= n1 + itself) |
| `harness_controls.json` | every per-fold score and every arm, for each control |

## What each registered control (A14) had to show, and what it showed

| control | registered expectation | observed | as designed? |
|---|---|---|---|
| (a) oracle | wins P1 on all four fields in every fold; DL ≥ DL(bank); fails P2 on length; does not pass C6 | 10/10 wins on each of the four fields, no ties. DL = 94,812 bits = DL(bank), against a limit of 9,481. **FAIL**: "not a bottleneck", "family fits anything" | **yes** |
| (b) N1 as a rule | 0 wins on existence and offset set; no losses on counts and sign; does not pass | 0 and 0 wins, every fold a tie; 0 and 0 losses. **FAIL**: "copy or marginal" and others | **yes** |
| (c) RP_r8, seed 999, as a rule | does not pass | P1 failed: 1 of 10 wins on existence, and it is *worse* than N1 on existence and counts. **FAIL** on every label | **yes** |
| (d) 99 shuffled banks | every bank keeps each type's in- and out-degree, has 604 non-empty cells, and holds the same multiset of contents | all hold, on all 99 banks; 12,080 successful swaps each | **yes** |

**Every registered expectation held. No control behaved against its registration.**

Some of what the controls show is a **property of the exam** rather than a failure of a control.
Several of these properties should be decided on before any rule is run. They are listed next.

## Findings about the exam: read before any rule is run

### 1. DEFECT: at the one-tenth limit, D_k collapses to N1

- N1 itself costs **18,089 bits**: 4,896 for its program and about 13,200 for its data. That is
  already about **twice the P2 length limit** (DL(bank) / 10 = 9,481 bits).
- D_k contains N1 (A5), so D_0 is at least that large. Any rule short enough to pass P2's length
  half therefore has **k\* = 0**.
- So its "size-matched direct encoding" is N1, not a table of the rule's size. P2's second half
  reduces to "beat N1 in-sample", which P1 already asks on held-out cells.
- **The budget arm cannot return Clune's "below threshold" outcome for any rule that passes on
  length.** That is the outcome §1 says C6 must be able to return.
- This follows from A5 ("the N1 tables count in D_k's length"), combined with the one-tenth
  limit. I made that A5 choice; the spec's own numbers were already in place.
- A fix needs a decision. One option: a size-matched table **without** N1, that stores k cells
  and answers N0 or "empty" elsewhere. At about 9.4 kbits that stores on the order of a few dozen
  cells. The harness is not changed until the spec is.

### 2. DEFECT: N1 is weaker than N0 on offset set

- Mean held-out Jaccard: **N0 0.447, N1 0.420**. N0 beats N1 on offset set in 5 of 10 folds.
- The "did not run" check fires above 5, so N1 as a rule sits exactly at the edge of being
  labelled "rule did not run".
- Consequence: P1's offset-set arm is easier than intended. A rule can "beat N1" on offset set by
  doing what the global null does. The source type's most frequent set (A4) is a worse guess
  than the most frequent set overall.
- The registered null is implemented as written. Whether N1's offset-set part should fall back
  to, or be compared against, max(N0, N1) is for the spec's owner.

### 3. WEAK ARM: the random-projection falsifier (P4) has little bite at these settings

- At every rank tried (3, 8 and 16), RP_r does **worse** than N1 on existence. The best of the 20
  seeds has a margin of −0.003 to −0.005 nats.
- So P4 as registered reduces to "the rule's existence margin over N1 is above about −0.004".
  Any rule that passes P1 on existence also passes P4.
- The cause is that a random side plus a fitted side, with λ = 1, overfits more than it finds.
- As a falsifier of "ambient structure" it is currently weak. It is not wrong. Strengthening it
  means changing A11 (for example, choosing λ by inner cross-validation), which is a spec
  decision.

### 4. As designed: P3 fails a memoriser

- The oracle's margin over N1 is N1's own loss, whatever bank it is given. On existence, 43 of
  the 99 shuffled banks give it a margin at least as large as the real one; on offset set, 97 do.
- A predictor that succeeds on *any* table, whether real or shuffled, is exactly what P3 exists
  to catch ("family fits anything"), and it catches it.
- Related: N1's existence log-loss on the real bank (0.362) sits inside the shuffled range
  (0.359–0.366), as degree-preserving rewiring should give. On offset set, N1's real Jaccard
  (0.420) is near the top of the shuffled range (0.383–0.422), so the real bank is slightly
  *easier* for N1 there. That makes P3 on offset set harder for a rule, not easier.

### 5. As designed: P4 does not catch the oracle

The oracle passes P4 (margin 0.361, far above RP). P4 is not meant to catch memorisation; P2 and
P3 do, and did.

### 6. Rewiring leaves about a quarter to a third of the pairs in place

After 12,080 successful swaps, 409–457 of the 604 non-empty cells have moved. The rest stay,
mostly around high-degree types, where few swaps are legal. That is a property of
degree-preserving nulls, not a bug. It is reported so that "shuffled" is not read as "fully
random".

## Harness conventions not written in the spec (to be registered or rejected)

1. **Negative predicted counts are read as 0** before `log1p` (a count cannot be negative).
   - N1's additive log model predicted a value below zero once in 769 held-out offset
     predictions on the real bank. Every true value is positive, so clipping can only reduce
     that error.
2. **The dial's "margin over D_k" (§5.3) is taken in-sample.**
   - Held out, D_k equals N1 on every held-out cell by construction: stored cells come from
     training folds only. A held-out margin over D_k would just repeat the margin over N1.
   - The harness reports both: the held-out margin over N1, and the in-sample margin over
     D_k\*, with k\* fixed from the real bank.
3. **Type indices given to a rule** are 0–64 in birth-id order.
   - `role` and `layout` are passed as integer codes, in the sorted order of their strings.
4. **Import check.** A decode program may import the standard library, numpy, and its own
   listed files. The check is static (Python's `ast` parser). It will not catch dynamic
   imports; review of the charged source remains the backstop (A1, A5).
5. **The full-bank N1 fit** used for D_k and k\* is the same N1 learner, run on all 4,225 cells.

## Description lengths (bits, A5)

| | program | total |
|---|---|---|
| S_all (the bank) | 4,336 | **94,812** |
| P2 limit (one tenth) | | 9,481 |
| M18 (A6) | | 74,880 → k18 = 209 cells |
| N1 | 4,896 | 18,089 (k\* = 0) |
| RP_r8 | 8,256 | 55,053 (k\* = 117) |
| D_k program | 8,296 | |

## What this does not show

- **Power.** No control shows that a small, good rule *can* pass. The oracle passes P1 but
  cannot be small. With finding 1, a rule that passes P2 on length meets no real size-matched
  opponent. A planted-structure control (a synthetic bank with a known small generator) would
  test power. It was not registered, so it was not run.
- **Anything about the fly's wiring, or about any rule.** These are scores of nulls and of
  deliberately degenerate predictors.
