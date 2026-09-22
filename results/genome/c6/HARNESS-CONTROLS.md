# C6 harness controls: the exam run with no rule, after Amendment 2

**Written:** 2026-09-23, by CC (subagent), under option A (Mike, owner, 2026-09-23 21:01 UTC).
I built the harness and corrected it. I have not read the proposed rule (declaration:
`docs/plans/2026-09-23-c6-amendment-acceptance.md` §(e)).

**No rule was run.** None is registered, and the harness refuses `--rule`.

**What this run is checked against**, and the hashes of this run:

| | file | sha256 (LF-normalised) |
|---|---|---|
| harness | `results/genome/c6/harness.py` | `6a1ca2fa077b336e401c25e4b83ed7ed2c756c64590b444925636f7676d7dc1c` |
| acceptance criteria | `docs/plans/2026-09-23-c6-amendment-acceptance.md`, committed alone before the fix (`4332d17`) | `bd3697719aa96a2d6c39078d7d01823009746de50b694debecc0f0d450b43d3b` |
| specification | `docs/plans/2026-09-23-c6-control-specification.md`; Amendment 2 is A16–A22 | `ec4130d0362a4de968c2e854472c78065c0b752dfc397b499a4f0d58d2261e9f` |

`harness_controls.json` records the sha256 of the harness, the spec, the acceptance file, the
folds and every decoder.

**Run:** `tools/.venv/Scripts/python.exe results/genome/c6/harness.py --controls` (CPU, about
10 minutes).

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

**15 of 16 pass. R1 fails.** Under the acceptance file §(f), a failed criterion is reported as a
failure of the amended exam and is **not re-tuned**.

The A14 checks were re-run: all eight hold (oracle; N1 as a rule; RP_r8 as a rule; 99 shuffled
banks, invariants exact).

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

So the exam accepts a small non-additive rule that is really there, at full and at half
strength. It rejects the same family when the structure is absent (PL0), when the genome is
wrong (scrambled), and when the rule is run on a bank it was not made for (the real fly, N2).

### 4. The hub check (report only; P3 unchanged, as registered)

| quantity | value |
|---|---|
| overlap of H (the 18 types with the most leverage in the top 18 SVD components of L) and U (the 18 types whose cells the shuffle most often leaves in place) | **14 of 18**; 5.0 expected by chance; hypergeometric p = 1.1 × 10⁻⁷ |
| Spearman correlation, leverage vs unmoved fraction | 0.81 (and 0.92 against total degree) |
| share of L's energy in cells touching U, and touching H | 75 %, and 78 % |
| unmoved fraction per type | 0.04 to 0.49 |
| overlap types | C3, L2, L5, Mi1, Mi4, Mi9, T2, Tm1, Tm2, Tm3, Tm4, TmY14, TmY15, TmY4 |

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
