# C6 harness controls: the exam run with no rule, after Amendment 2

**Written:** 2026-09-23, by CC (subagent), under option A (Mike, owner, 2026-09-23 21:01 UTC).
I built the harness and corrected it. I have not read the proposed rule (declaration:
`docs/plans/2026-09-23-c6-amendment-acceptance.md` §(e)).

**No rule was run.** None is registered, and the harness refuses `--rule`.

**What this run is checked against**, and the hashes of this run:

| | file | sha256 (LF-normalised) |
|---|---|---|
| harness | `results/genome/c6/harness.py` | `071d826a4a3894c6db77ff846f5019efa85a4cb278b18b9892916353f63f90f7` |
| acceptance criteria | `docs/plans/2026-09-23-c6-amendment-acceptance.md`, committed alone before the fix (`4332d17`) | `bd3697719aa96a2d6c39078d7d01823009746de50b694debecc0f0d450b43d3b` |
| acceptance criteria, part 2 | `docs/plans/2026-09-23-c6-amendment-acceptance-2.md`, committed before A6 was written (`c75139a`) | `4b6610e7ed30b6aaeccf6ea33008485fc3ec31a1869b93f74c78b7248f2e97f9` |
| acceptance criteria, part 3 | `docs/plans/2026-09-23-c6-amendment-acceptance-3.md`, committed before the code (`2e36a6d`) | `16432647ffc568c2a3cb77bc61459abe8df50902ca945badf97fc20be9e2ac9f` |
| specification | `docs/plans/2026-09-23-c6-control-specification.md`; Amendment 2 is A16–A24 | `5c58b02a53021f5a9d3ec5090e56dc183fb567568dfc1eda86e74ae8e28e7abd` |

`harness_controls.json` records the sha256 of the harness, the spec, the acceptance file, the
folds and every decoder.

**Run:** `tools/.venv/Scripts/python.exe results/genome/c6/harness.py --controls --starts 10`
(CPU, about 37 minutes). **Every verdict and margin below is at k = 10 starts per trained fit**
(acceptance, part 3). `harness_controls.json` records k next to every verdict and every P1, P2
and P4 margin.

**The previous version of this page** (commit `d443cf6`) reported three defects and one gap.
Amendment 2 addresses them:

| before | after |
|---|---|
| finding 1: the budget arm could not fail | A17, the armed D_k^N0 |
| finding 2: N1 was weaker than N0 on offset sets | A18, N_EB, and P1's offset arm must beat each of three nulls |
| finding 3: P4 had no bite | A19, the trained factorisation BF_r |
| no control showed the exam could be passed | A20, the planted-rule acceptance suite |

## Acceptance criteria, checked by code

Each row below was printed by the harness against the criterion's own text, as registered in
the acceptance file.

| id | criterion (short) | expected | got | result |
|---|---|---|---|---|
| R1 | N1 as a rule does not beat the armed table of its own size | P2 fails on "below threshold" **because of** the armed table | the armed table has k\*_armed = 25 cells at 18,052 bits. **N1 beats it on both fields.** Existence log-loss 0.335 against 0.399; offset Jaccard 0.496 against 0.471 | **FAIL** |
| R2 | N0 as a rule: within length, does not beat the armed table | "below threshold", not "not a bottleneck" | DL 3,113 bits, length OK; k\*_armed = 0; ties; labels as expected | PASS |
| R3 | k\*_armed at DL(bank)/10 ≥ 5 | ≥ 5 | **7** | PASS |
| A1 | the planted rule PR passes C6 on PL1 | PASS | PASS, with no label | PASS |
| A2 | N1 and N0 as rules fail on PL1 | both FAIL | both FAIL | PASS |
| A3 | the oracle on PL1 fails on size | "not a bottleneck" | FAIL: "not a bottleneck", "family fits anything" | PASS |
| A4 | a foreign genome of the same size fails on PL1 | FAIL | FAIL on every arm; DL 4,846 against PR's 4,904 | PASS |
| A5 | PR's dial margin at f = 1 ≤ 0.25 × its margin at f = 0 | ≤ 0.25 | 0.122 (0.1334 → 0.0163 nats) | PASS |
| N1 | PR on PL0 (no planted structure) fails | FAIL | FAIL | PASS |
| N2 | the PR family on the real fly bank fails | FAIL | FAIL, including "rule did not run" | PASS |
| N3 | the A14 controls on the real bank still fail | all FAIL | oracle, N1 as a rule, RP_r8: all FAIL | PASS |
| M1 | A5 and the one-tenth limit untouched | DL(bank) = 94,812 | 94,812 | PASS |
| M2 | P2 opponents only added | three opponents | D_k^N1 at k\*, D_k^N0 at k\*_armed, N1 in-sample | PASS |
| M3 | offset target stronger: N_EB mean Jaccard ≥ 0.4465 | ≥ 0.4465 | **0.4842** (N0 0.4465, N1 0.4204) | PASS |
| M4 | P4 replaced: BF_8's margin over N1 > 0 | > 0 | **+0.0493 nats**; beats N1 in 10 of 10 folds | PASS |
| M5 | frozen tuning values recorded | recorded | α per fold 8, 8, 8, 16, 16, 2, 8, 8, 8, 8 (in-sample 16); BF_8 λ = 3 in every fold | PASS |

**15 of 16 pass. R1 fails.** (Part 2 adds A6 and A6-D; both fail, see below.) Under the acceptance file §(f), a failed criterion is reported as a
failure of the amended exam and is **not re-tuned**.

The A14 checks were re-run: all eight hold (oracle; N1 as a rule; RP_r8 as a rule; 99 shuffled
banks, invariants exact).

## Search-budget parity (acceptance, part 3)

Each trained opponent (BF_r) now gets the rule's number of starts k: the SVD start, plus k − 1
seeded perturbations, with the best chosen on the training objective only.

**BF_8's held-out existence margin over N1 on the real bank:**

| k (starts) | margin (nats) | folds beating N1 | λ chosen |
|---|---|---|---|
| 1 | +0.04927 | 10 of 10 | 3 in every fold |
| 3 | +0.04928 | 10 of 10 | 3 in every fold |
| 10 | +0.04933 | 10 of 10 | 3 in every fold |

| id | criterion | got | result |
|---|---|---|---|
| S1 | k recorded, and printed next to every verdict and every P1, P2 and P4 margin | k = 10 on all 13 exam records | PASS |
| S2 | M4 holds at k = 10 | +0.04933 | PASS |
| S3 | M4 holds at k = 3 | +0.04928 | PASS |
| S4 | the best start is never worse than start 0 on the training objective | 5,980 fits, 0 violations | PASS |

The extra starts barely move BF: +0.00006 nats from k = 1 to k = 10. The SVD start already sits
at, or next to, the best optimum it finds. **Every verdict in this file is the same at k = 10 as
at k = 1.** The P4 thresholds moved only in the fourth decimal. For example, PR on PL1 still
passes: its margin is +0.1334 against a threshold of +0.0741.

## A6: a weak object that loses on the budget arm alone (acceptance, part 2)

| id | expected | got | result |
|---|---|---|---|
| A6 | PR-sh on PL1 passes P1, P3 and P4 and fails only with "below threshold for this family" | FAIL on every arm ("rule did not run", "copy or marginal", "below threshold", "family fits anything", "ambient"). DL 4,532 bits; k\*_armed = 0 | **FAIL** |
| A6-D | for some affordable k, the armed table D_k^N0 beats N1 in-sample on existence or offset set | **no**, on either bank. Real bank, k = 0…7: best armed existence 0.4071 against N1's 0.3354; best offset 0.4498 against 0.4961. PL1, k = 0…18: 0.4076 against 0.4052; 0.3633 against 0.8690 | **FAIL** |

**Both outcomes match the corrector's prior, which was registered before the run.**

- **A6-D is the decisive result.** Within the size limit, the armed table is worse than N1
  in-sample on both fields, at every k it can afford, on the real bank and on PL1. P2 requires
  every rule to beat N1 in-sample (A17).
- So **no object** can clear the N1 opponent and still lose to the armed table. The budget arm
  cannot be the sole reason a rule fails. This holds for any object, not only PR-sh.
- PR-sh itself also failed P1, P3 and P4. Its training cells were shuffled, so it learned
  nothing, and it is not a "working" object. That is a second, smaller reason why A6 fails,
  and A6-D makes it moot.
- As registered, the object was not bent: it was not padded, and neither the bank nor the
  storage format was changed.
- **The finding, in one line:** the budget arm has capacity (R2, R3) but, within the size
  limit, no bite. It is dominated by the N1 opponent. That is the fact of
  `docs/plans/2026-09-23-c6-amendment-acceptance-2.md` §2: honest storage of this matrix is a
  weak predictor at any length we can afford. The Clune threshold is defended by P1 and P2
  against N0, N1, N_EB and BF. The budget arm guards only against a partial download of the
  answer.

## What R1's failure means

Ark's test was: *a rule no better than N1 must lose to the table of its own size.* On this bank
it does not. Storing 25 of the heaviest cells verbatim, with N0 everywhere else, costs the same
18 kbits as N1, and it predicts worse than N1 on both fields.

- **What N1 is.** N1 is a good compression of the bank: two type-level effects and a
  per-source set beat 25 stored cells. That is not a hole a rule can use. A rule the size of N1
  is twice over P2's length limit, and P2 also requires every rule to beat N1 in-sample (A17).
  So an N1-level rule is still rejected, but by the length half and by the N1 opponent, **not
  by the armed table**.
- **What the arm can do.** The armed table rejects a rule on its own only below N1's size: R2,
  and R3's 7 cells at the limit.

## Findings about the amended exam

### 1. OPEN: below 7,721 bits, the armed table is N0

- D_k^N0 costs **6,928 bits of program** (n0 + store + dk0, charged once), plus 793 bits of N0
  data, before its first cell.
- So every rule smaller than 7,721 bits has k\*_armed = 0, and its armed opponent is plain N0.
  The planted rule (4,904 bits) met N0, not a table.
- The arm has cells only for rules between about 7.7 and 9.5 kbits (7 cells at the limit).
- This is Ark's point that the carrier program eats most of the budget, now measured. It is
  monotone: nothing got easier. But the "size-matched table" still has teeth only in a narrow
  band. Shrinking the charged program (for example, stripping the docstrings of the three
  decoders) would move the band; it would change the exam, so it is not done here.

### 2. P4 now bites

On the real bank BF_r beats N1 by 0.028–0.049 nats at every rank that occurred (1, 3, 4, 8
and 16). So P4 now asks a rule to beat N1 on existence by more than a trained factorisation of
its own rank does.

On PL1, BF_4 reached +0.074 and PR +0.133, so PR passed P4 with room. On PL0 the nested CV chose
λ = 100 and BF's margin was 0.000, which is the correct behaviour on a bank with no low-rank
structure.

### 3. The planted suite, in numbers

| | P1 | P2 | P3 (real margin vs the best of 99 shuffles) | P4 (rule vs threshold) | verdict |
|---|---|---|---|---|---|
| PR on PL1 (ρ = 1) | 10/10 on existence; 10/10 vs each offset null | DL 4,904 ≤ 13,383; beats all three opponents | existence 0.133 vs 0.021; offset 0.134 vs 0.095 | 0.133 > 0.074 | **PASS** |
| PR on PL0.5 (descriptive) | pass | pass | 0.041 vs 0.016; 0.213 vs 0.071 | 0.041 > −0.001 | PASS |
| PR on PL0 (ρ = 0) | offset 0 wins vs N0; "did not run" | fails vs D_k^N1 and N1 | fails | 0.013 > 0.000 | FAIL |
| PR, scrambled genome, on PL1 | offset 0 wins vs N1 | fails | fails | 0.017 < 0.074 | FAIL |

**Scope of A1 (Ark).** PL1 has 617 non-empty cells and DL(bank) = 133,827 bits, against the real
bank's 604 cells and 94,812 bits. So A1 speaks to the logic of the exam, not to the real bank's
budget.

So the exam accepts a small non-additive rule that is really there, at full and at half
strength. It rejects the same family when the structure is absent (PL0), when the genome is
wrong (scrambled), and when the rule is run on a bank it was not made for (the real fly, N2).

### 4. The hub check (report only; P3 unchanged, as registered)

| quantity | value |
|---|---|
| overlap of **H18** (top-18 types by leverage at rank k90) and **U18** (top-18 types by the fraction of their cells left unmoved by the 99 shuffles) | **14 of 18**; 5.0 expected by chance; hypergeometric p = 1.1 × 10⁻⁷ |
| Spearman correlation, leverage vs unmoved fraction | 0.81 (and 0.92 against total degree) |
| share of L's energy in cells touching U18, and touching H18 | 75 %, and 78 % |
| unmoved fraction per type | 0.04 to 0.49 |
| overlap types | C3, L2, L5, Mi1, Mi4, Mi9, T2, Tm1, Tm2, Tm3, Tm4, TmY14, TmY15, TmY4 |

**Naming.**

- **k90 = 18** is a *component count*: the singular components of L = ln(1 + N) that hold 90 %
  of its energy (`REGULARITY-READING.md` §2). It is not a set of types.
- **H18** and **U18** are *sets of types*. Their size, 18, was borrowed from k90 by convention.
- The harness's L equals `regularity.py`'s L exactly: 0 of 4,225 cells differ. `regularity.py`
  sums the compiled `n_syn` over the `in_json` and `hull_filled` rows, where every hull row has
  `n_syn = 1.0`. The harness adds 1.0 per hull row to the compiled `in_json` sum.
- No number in this section changed with the renaming.

Ark's hypothesis holds.

- **Existence.** Degree-preserving rewiring cannot move most of the cells of the high-degree
  types, and those types carry three quarters of the table's energy. So on existence, P3 compares
  the rule against shuffled banks that keep much of the hub structure in place.
- **Which way that cuts.** It makes P3's existence arm **conservative against the rule**. A rule
  that exploits hub existence keeps part of its margin on the shuffled banks, and must still beat
  all 99. So it is harder to pass, not easier. But it also means P3 separates "fits anything"
  from structure least well exactly at the hubs.
- **Offset set.** P3's offset-set arm is not affected, because contents are permuted over all
  cells, hubs included (A10).
- As registered, P3 is not changed. Any change is for the spec's owner.

## Harness choices made while implementing A17–A22

1. The dial's margins over the stored tables are in-sample (A17 folds in Convention 2).
2. The inner folds of the nested choices are the registered folds, restricted to the training
   cells.
3. BF_r is initialised by the SVD of the training residual in probability units, then
   refined by Newton. The registration does not fix the scale of the initialisation, and this
   is the one free implementation detail.
4. The planted banks use the same fold grid (by cell position), so their strata are not
   balanced, as for the shuffled banks (A10).

## What this does not show

- **Anything about the fly's wiring, or about any rule.** These are scores of nulls,
  degenerate predictors, and a synthetic generator.
- **Learnability.** PR is given its true class vector (its genome) and fits only the block
  parameters. That a rule of this family could *find* its classes is not tested.
