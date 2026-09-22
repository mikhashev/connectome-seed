---
**Status:** REGISTRATION. It is committed **before** any change to the first rule's search
procedure, and before any fit of the planted or shuffled tables named below.
**Written by:** CC (subagent, implementer of the first rule's fitting code), 2026-09-23.
**Decision:** Mike, owner, 2026-09-23 22:38 UTC (group chat): option B, fix the rule's search
procedure before any real run, against a criterion registered first.
**The criterion's shape:** Ark, genome track, 2026-09-23 22:29 UTC. Ark stays blind to the rule's
content, and this file was not sent to him.
**Reviewer of the fix:** Zcode.
**Rule:** `docs/plans/2026-09-23-first-rule-proposal.md`, registered at commit `5a46886`. Its code
is in `results/genome/c6/rules/first_rule/` (commit `05c1a8d`).
---

# The first rule's search procedure: the criterion a fix must meet

## Why a fix is needed

The rule's stage 1 (proposal §2.4) is a greedy search. It starts from random labels and no rules.

- **What was observed.** On shuffled bank 0 (used for timing only), 8 of 10 restarts stopped
  after the first sweep with **no rule at all**. On synthetic planted tables, most restarts did
  the same.
- **Why.** A rule on random Bernoulli(0.25) labels rarely earns its 25 bits. Until some rule
  exists, no label flip can lower J. So the first sweep "changes nothing", and the restart ends.
- **What that means.** The search as registered can stop before it has looked. This file fixes,
  before any change is made, what a repaired search must show.

## 1. What may change, and what is frozen

- **May change: the search procedure of proposal §2.4 only.** That means the initialisation, the
  order of moves, the stopping rule and the restarts.
- **Frozen:**
  - the model (§2.1–§2.2) and the decoder, `decode.py`, 555 lzma bytes, byte-identical;
  - the objective J, including the clipped p;
  - the quantisation grids;
  - the caps (k = 12 labels, R_max = 40, M_max = 16, O_max = 64);
  - the 25-bit rule cost;
  - stages 2–4;
  - the C6 description-length accounting.
- **The old procedure stays callable.** It becomes `SEARCH = "v1"`. The fix is `SEARCH = "v2"`,
  and it is declared in an appendix to the proposal, dated, before the gates are run.
- **Restarts.** The number of restarts k stays a parameter. The gates are run at k = 10.

## 2. Seeds (none of them in the exam's own null)

C6's P3 uses `harness.shuffled_bank(REAL, i)` for i = 0…98. Shuffled bank 0 was used for timing.
None of those banks is used in any check below.

| use | tables | seeds |
|---|---|---|
| **Development** of v2: looked at freely while designing the fix | planted | 3000–3009 |
| | shuffled | `harness.shuffled_bank(REAL, s)`, s = 1100–1109 |
| **Gates**: run once, on the final v2, after it is committed | planted | 2000–2019 (N = 20) |
| | shuffled | `harness.shuffled_bank(REAL, s)`, s = 1000–1019 (M = 20) |

- The v1 measurement (§6) uses the gate seeds.
- Timing uses shuffled bank 0, as proposal §2.4 registers. Timing is not a falsification check.
- **Held-out split for every table with seed s:** training cells are those with `FOLD != s mod
  10`, and the held-out cells are those with `FOLD == s mod 10`. FOLD is the harness's
  `folds.csv`, read by cell position.

## 3. The planted class: generator PG1

**What it is.** Each table is drawn from the rule's own model family, under the rule's caps, on 65
type indices (no names, no real content). The target is a realistic density: the real bank has
604 of 4,225 non-empty cells, which is 0.143.

**The draw.** Seed s uses one `numpy.random.Generator(PCG64(s))`. Each attempt draws, in this
order:

1. **Expression.** E = `rng.random((65, 12)) < 0.12`.
2. **Rules.**
   - 12 rules on the ordered label pairs x = sorted(`rng.choice(144, 12, replace=False)`), with
     (i, j) = (x // 12, x % 12).
   - ρ levels are `rng.integers(11, 16, 12)`.
3. **Motif library, 12 motifs.**
   - Motif 0 is {(0, 0)}.
   - Then repeat until there are 12 distinct shapes: n = `rng.integers(2, 7)`; picks =
     `rng.choice(18, n − 1, replace=False) + 1`, indexing D2. D2 is the radius-2 hex disc,
     listed as (0, 0) first, then (u, v) for u = −2…2 and v = −2…2 with
     max(|u|, |v|, |u + v|) ≤ 2, in that loop order. The shape is `canon({(0,0)} ∪ picks)` and
     is added only if new.
   - π levels: `rng.integers(8, 16, len(shape))` per motif, in library order.
4. **Per rule.** Motif `rng.integers(12, size=12)`, orientation `rng.integers(12, size=12)`, and
   w level `rng.integers(12, 26, 12)`.
5. **Count gains.**
   - a = clip(round(`rng.normal(8, 1.5, 65)`), 0, 15), then b drawn the same way.
   - w_0 = `rng.integers(8, 20)`.
   - The ε level is 9 (ε = 2^−5.5 ≈ 0.022).
6. **Sign.** `rng.random(65) < 0.6`, where True means +1.
7. **Existence.** u = `rng.random((65, 65))`. Cell (s, t) is non-empty iff u < p(s, t), the
   noisy-OR of §2.2, unclipped.
8. **Content.** z = `rng.normal(0, 0.3, (65, 65, 6))`.
   - A non-empty cell gets the offsets and counts that `decode.py` gives the planted genome.
   - The k-th decoded offset's count is multiplied by exp(z[s, t, k]).
   - Sign is σ_s. There are no hull rows.
9. **Acceptance.** The attempt is kept iff all of these hold:
   - the density is in [0.12, 0.17];
   - every label is expressed by at least one type;
   - no two label columns are equal;
   - the planted genome's data length (`harness.data_bits` of its packed arrays, rules in (i, j)
     order) is in **[2,200, 3,600] bits**, which is a total DL of 6,640–8,040 bits with the
     4,440-bit decoder.

   Otherwise the next attempt continues on the same generator, for at most 1,000 attempts.

**Why this band.**

- A realistic fit, with about 12 rules and a full 16-motif library, has about 3,100 data bits.
- A fit at the caps has 3,600–3,800.
- The proposal (§2.5) bounds the data at about 4,070.
- PG1 genomes come out at about 2,500–2,700 data bits: 12 rules and 12 motifs.

**The planted genome's J** is `fit.total_J` of the planted E, rules, ρ levels and ε level, on the
table's training cells.

## 4. The positive gate

**"Finds".** A fit with SEARCH v2 at k = 10, using the full `fit.fit` (stages 1–4), finds the
planted rule of a table iff **both** hold:

- **(F1)** its best restart's training J ≤ J_planted + **0.01 × J_planted**;
- **(F2)** on the table's held-out cells, its existence log-loss is lower than N1's by more than
  τ = 1e-9. Both are decoded through `harness.Predictor(...).decode` and scored with
  `harness.score`, and N1 is `harness.fit_n1` on the same training view.

**Gate:** the fit finds the planted rule on **at least 15 of the 20** planted gate tables.

## 5. The negative gate

**"False find".** On a shuffled gate bank, the v2 fit at k = 10 has a held-out existence
log-loss lower than N1's by more than τ.

**Gate:** false finds on **at most 1 of the 20** shuffled gate banks.

**Why existence only.** The fix changes stage 1, and stage 1 fits existence only. On a shuffled
bank the offset contents are permuted independently of the pair. There, a motif pooled over many
cells can beat N1's per-source modal set for reasons that have nothing to do with the search. N1 is
known to be weaker than N0 on offsets (HARNESS-CONTROLS). So offset set, counts and sign are
**reported** for both gates, and decide nothing.

## 6. The old procedure, kept as a measurement

On the same 20 planted and 20 shuffled gate tables, SEARCH v1 at k = 10 is run and recorded on a
separate line:

- **stall rate:** the fraction of the 200 restarts that end with zero rules, and the number of
  tables whose best restart has zero rules;
- **find rate:** the number of planted tables on which v1 "finds" (F1 and F2);
- **false-find rate:** the number of shuffled tables on which v1 beats N1 on existence.

Read as: *how much regularity the greedy search needs before it starts.* **It is a measurement,
never a verdict.**

## 7. Two-way freeze

- **If no fix passes both gates, that is the finding.** It is reported as such. The gates are not
  loosened, the seeds are not changed, and the planted class is not redrawn.
- **If v2 passes, v2 becomes the procedure** for every fit of the C6 run, primary included. The
  timing rule of proposal §2.4 (10 restarts, or 3 if 1,315 fits exceed 48 hours) is re-measured
  for v2 on shuffled bank 0. The choice stays Mike's.
- **Whatever the gates show**, nothing here touches the real bank or a real fold. The rule's C6
  run still needs Mike's separate approval.
