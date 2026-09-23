---
**Status:** PROPOSAL, revised after Zcode's review (group chat, 2026-09-23 13:17 UTC). Mike approved
going ahead at 13:26 UTC. **Not registered.** It becomes a registration only when it is committed,
before any code for it exists and before it meets any data it is judged on. No rule code has been
written, no fit has been made and nothing has been run for it.
**Changed after Zcode's review:**
- §1: r is computed, not declared, and its arithmetic is written out.
- §1, §4, §5.2, §8: the margins against BF_1–BF_4 must be printed.
- §1, §4.2, §7, §8: a registered P4 tie band of ±0.002.
- §1, §4.1, §6: P3 and P4 now use τ, as spec A7 requires.
- §6, §9: the A20 re-run is handled.
- §9: Q1–Q3 are closed.
**Written by:** CC (subagent), 2026-09-23 12:12 UTC, on CC's brief (handover step 4,
`docs/briefs/2026-09-23-next-session-handover.md` §3).
**Judged by:** the C6 specification as amended (A1–A24), `docs/plans/2026-09-23-c6-control-specification.md`,
and the three acceptance files; if C6 is amended again, **C6 governs**.
**Registered predictions it answers to:** `docs/plans/2026-09-23-first-rule-failure-predictions.md`
(FINAL, commits `b8ca3dd` and `32a4ae9`). That file is not edited here. §4 below says which of its
branches applies.
**Blindness.** §1–§7 carry rule content. Ark, Johnny and the blind reader are blind to rule content
and must read **only §8** (the blind-safe summary) and §9. Zcode reviews the rest.
**No new measured results.** Every number below is either quoted from a committed record (the file
is named each time), a structural count of the admissible per-type fields, or arithmetic on the A5
bit table.
---

# The second rule: N1 + a rank-1 bilinear term + field groups and target-side offset sets

## 0. Summary, in plain words

The second rule predicts each cell of the type-pair table from four stored ingredients:

1. **N1's own per-type terms**, stored on a coarse quantisation step so that they fit in the budget.
2. **One trained bilinear term** u_s·v_t on the existence logit, fitted the way BF_r is fitted, at
   rank 1. This is all the rank the one-tenth limit leaves room for (§2.4).
3. **The addition X, in two parts**, each using information that N1, BF_r and N_EB do not use:
   - **X_e (existence):** a 4 × 4 table of logit shifts indexed by the source's and the target's
     **field group**. A field group is what the admissible per-type fields (`stride_u`, `stride_v`,
     `role`, `layout`) actually distinguish: four groups of 8, 21, 34 and 2 types (§2.1). BF_r
     never reads these fields. Because the fields are known for a type the rule has never seen,
     X_e is the one part of the existence model that still speaks on leave-one-type-out cells.
   - **X_o (offset sets):** every type gets **two** smoothed offset sets, one from its outgoing
     cells (as N_EB does for sources) and one from its **incoming** cells, which N_EB ignores. A
     cell takes the target's set when the target's incoming sets are more concentrated than the
     source's outgoing ones, and the source's set otherwise.
4. **N1's counts model** (offset base plus source and target effects) and **N1's sign**, the
   latter reproduced bit for bit.

**What I expect, written now:** P1 existence, P2 and P3 existence pass. P4 at rank 1 is close to
even odds. **The likeliest failure is the offset set**: I expect the rule not to beat N_EB in 9 of 10
folds (P1, "copy or marginal") and P3 offset to fail more often than not ("family fits anything").
My probability that the rule passes C6 as a whole is **at most 5 %**. §7 gives the reasons.

## 1. Mandatory registration fields (predictions file §4c)

| field | value |
|---|---|
| **rank r (computed, not declared; Zcode's ruling, 2026-09-23 13:17 UTC)** | **r = 1**, by A11's rule applied to the fitted interaction numbers of the existence logit. **Arithmetic:** the bilinear term has 65 + 65 = 130 fitted numbers (u_s, v_t). X_e is a term on a **fixed partition**: 4 × 4 = 16 fitted numbers and **no per-type coordinates**, since the field groups are given, not fitted. So r = round((130 + 16) / 130) = round(1.123) = **1**. The rule file sets `RANK = 1` so that the harness uses this value. **The registration carries its own arithmetic and does not rely on the fallback in the harness's `rank_of`.** That fallback counts only the float arrays in the data (float32 after the cast). This rule stores almost everything as integer symbols, so the fallback would count 6 floats and also return r = 1, but by a degenerate count that says nothing about the rule. **Why the arithmetic is written down:** at r = 4 the P4 threshold would be BF_4's +0.03972, not BF_1's +0.02815, and my P4 prior would drop from 0.5 to 0.15 (§4.3). |
| **BF margins printed with the verdict (mandatory)** | Directly under the harness's verdict line, the run's record must print the rule's mean existence margin over N1 minus BF_r's margin for **BF_1 (the decision)** and for **BF_2, BF_3 and BF_4 (context only)**, all at the run's k. BF_1's value is the record's own `P4.bf.margin`. BF_2 is fitted by the post-run script (§6) with the harness's `bf_predictor(2)`. BF_3 and BF_4 are refitted the same way; at k = 10 they must reproduce +0.04034 and +0.03972. The line is part of the record, not a reading, and it cannot be dropped. |
| **P4 tie band (registered before the run; Zcode's ruling)** | Δ = rule margin − P4 threshold. **A Δ within ±0.002 is read as a tie, not a pass.** The reasons are quantisation (about 0.001 nats, §2.4) and fold noise. For this registration, P4 counts as passed only if **Δ > +0.002**. If the harness prints P4 as passed with 0 < Δ ≤ +0.002, the record states under the verdict line that this registration reads it as a tie. The harness's verdict string itself is printed verbatim and is not altered. |
| **resulting P4 threshold** | max(RP_1 threshold, BF_1 margin). On the real bank at k = 10 BF_1's margin over N1 is **+0.02815** (0.028150051052145946; `harness_controls.json`, `controls["real/N0 as a rule"].P4.bf.margin`, quoted in the predictions file §2 row 4 and §4c). RP_r thresholds on the real bank lie between −0.00475 and +0.00120 at every rank seen (blind reader report, Part A.0), so BF_1 binds. The threshold printed by the run itself governs. If the timing cap forces k = 3, BF_1 is refitted at k = 3 and that value governs (not yet measured; starts moved BF_8 by +0.00006 between k = 1 and 10). |
| **timing cap** | **k = 10 starts**, unless the projected wall time is over 12 hours. Projection: time the rule's fits of folds 0–9 of **shuffled bank 0** at k = 10, and scale their mean to the 1,341 rule fits the harness makes (1,250 cross-validation, 65 leave-one-type-out, 26 in-sample) at the run's worker count. If over 12 hours, **k = 3 for every fit of the run**. The measurement and the decision are written to the run's attempts file before any real-bank fit (acceptance part 3 (c)). No score is computed on shuffled bank 0 for this. Expected: k = 10. |
| **fields X touches** | **existence: yes** (X_e; the N1 and bilinear parts are also re-quantised, so no cell's existence prediction is bit-identical to BF_1's). **offset sets: yes** (X_o). **counts: yes**, but only through two things: the counts are scored on X_o's offset sets, and N1's counts terms are stored on a quantisation step. **No new per-node counts term** is added; the counts model is N1's (m_o + α_s + β_t). **sign: no.** The learner stores N1's per-source majority sign with N1's fallback already resolved, so the decoded sign is identical to N1's on every cell of every bank. |

**By-construction facts that follow (predictions file §4c), stated so that none is read as evidence:**

- Sign: P1 sign ties N1 in every fold (0 losses, mean equal); P3 sign margin is exactly 0 on all 100
  banks. Definitional.
- P2 length: the caps in §2.4 bound DL(rule) at **9,375 bits**, under the one-tenth limit of
  9,481.2 bits, once the decode program passes its size gate (§2.5). Definitional after the gate.
- Existence and offset sets are both touched, so neither by-construction fail of §4c applies: the
  rule can in principle pass C6, and P4 is not a bit-identical tie.
- **τ in P3 and P4.** A separate change, being committed with a `--controls` re-run before this
  rule runs, aligns `harness.py` with spec A7. P3 and P4 now require the margin to exceed its
  comparison by **more than τ = 1e-9**, not a plain `>` (the finding recorded in the predictions
  file's v5 history). So a float-noise difference can no longer decide P3 or P4. What remains is
  the noise of quantisation and folds, at about 1e-3, which the ±0.002 tie band above covers.

## 2. Family and mechanism

### 2.1 What the admissible per-type fields contain (a structural count, not a fit)

The harness hands a rule `type_fields` = (`stride_u`, `stride_v`, role code, layout code) per type
(spec A1; `harness.py` lines 131–132). Counted from `results/genome/bank/types.csv` (these four
columns only):

| stride (u, v) | role | layout | types |
|---|---|---|---|
| (1, 1) | input | retina | 8 |
| (1, 1) | intermediate | intermediate | 21 |
| (1, 1) | output | output | 34 |
| (3, 2) | intermediate | intermediate | 2 |

- **`role` and `layout` are the same partition** on all 65 types. Both are built from the json's
  `input_units` and `output_units` lists (`results/genome/bank/README.md` lines 42–44, 93–97).
- `stride_u` and `stride_v` separate only the two `stride [3, 2]` types (Lawf1 and Lawf2).
- So the admissible fields carry exactly one variable with four values: the **field group** G(t)
  (new glossary term). The rule computes it in its decode program as G = 3 if `stride_u` > 1,
  else the role code (0 input, 1 intermediate, 2 output). It never reads a name or a birth id.

This is a finding about the exam's inputs, not about the rule: **everything a predictor may know
about a type it has never seen is two bits.**

### 2.2 The model (the decode program computes this)

For a cell (s, t):

- **Existence.** logit = c + a_s + b_t + u_s·v_t + W[G(s), G(t)], then p = σ(logit). c, a, b are
  N1's existence terms. u, v are the rank-1 bilinear term. W is X_e, a 4 × 4 table.
- **Offset set.** A library of at most 32 exact offset sets is stored. Each type has a source-side
  index A_s and a target-side index B_t into the library, and two concentration levels e_s
  (source side) and f_t (target side), each 0–7. The cell's set is library[B_t] if f_t > e_s, and
  library[A_s] otherwise. A tie goes to the source side, which is N_EB's side.
- **Counts.** For each offset o of the cell's set: n̂ = expm1(m_o + α_s + β_t). These are N1's
  counts terms (spec A4). m_o is stored for every offset that occurs in the library.
- **Sign.** The stored ±1 of the source type, which equals N1's prediction (§1).

### 2.3 The learner (not charged; training cells only; deterministic)

**Existence.**

1. c, a, b: N1's existence fit exactly as the harness does it (ridge logistic, λ = 1, intercept
   unpenalised; `harness.py` `fit_n1`). O = c + a_s + b_t.
2. For a given penalty λ, fit (u, v, W) in **3 alternating rounds**, starting from W = 0:
   - (i) u, v: the harness's BF algorithm at rank 1 (`bf_als`), with offset O + W[G(s), G(t)]:
     SVD start of the probability-unit residual, the run's k starts with the registered
     perturbation seeds (acceptance part 3 (a)), 25 alternating Newton sweeps, the best start by
     the penalised training objective.
   - (ii) W: ridge logistic on the 16 group-pair indicators, offset O + u_s·v_t, penalty
     μ = 1 on all 16 entries (the same unit-normal prior as N1's λ = 1), no intercept. μ is fixed
     now and never tuned.
   - Round 1 step (i) runs with W = 0, so it is exactly the harness's BF_1 fit at that λ.
3. λ is chosen from {1, 3, 10, 30, 100} by the harness's nested scheme for BF_r (inner folds;
   inner held-out log-likelihood; ties to the larger λ), with steps 1–2 inside every inner fit.
4. The final fit uses the chosen λ on the whole training view.

**Quantisation of the existence terms.** a and b share one scale, u and v share one scale (after
rescaling u by κ and v by 1/κ so that max|u| = max|v|), W has its own. Each value is stored as a
5-bit symbol q with value scale · (q − 16) / 16; the scale is max|x| · 16/15 so both ends are
representable, and zero is exact. Then one pass of coordinate descent: in the order a, b, u, v, W,
each symbol tries q ± 1 and keeps the move if the penalised training objective falls by more than
1e-9. Then c is refitted as a float by Newton on the training log-loss, everything else fixed.

**Offset sets.**

1. **Library.** Take the training non-empty cells' exact offset sets in decreasing order of
   frequency (A4's tie rule). Add a set if, after adding it, the library holds at most 32 sets,
   the library's own A5 cost is at most 800 bits, and the library contains at most 48 distinct
   offsets. Otherwise skip it and go on. The scan is deterministic.
2. **Source side, A_s.** N_EB's formula (acceptance file §(b)): p_s(S) = (c_s(S) + α·g(S)) /
   (n_s + α) over **all** observed training sets S, where c_s counts the source's outgoing training
   cells. The chosen set is the **library** set A that maximises Σ_S p_s(S)·J(A, S), with A4's
   tie rule. α is chosen by N_EB's nested scheme from its grid, with the same candidate
   restriction.
3. **Target side, B_t.** The same, with c_t counting the target's **incoming** training cells, and
   its own α chosen by the same nested scheme.
4. **Concentration levels.** e_s = the maximised expected Jaccard of A_s under p_s; f_t = the same
   for B_t under p_t. Each is stored as min(7, ⌊8 · value⌋). A type with no training non-empty
   cell on a side gets level 0 on that side.

**Counts.** N1's counts terms as the harness computes them (`fit_n1`): m_o, α_s, β_t. m_o is kept
for the library's offsets only (each occurs in training by construction). α and β share one scale
on the same 5-bit symmetric step as above; m_o is stored as a 5-bit symbol on [0, max m].

**Sign.** N1's per-source majority over training non-empty cells; a tie or no cell gives N0's
training majority (a tie there gives +1). Stored as one boolean per type.

**Determinism.** Every step is seeded or deterministic, so the same training view always gives the
same data, byte for byte (gate G-det, §2.5). The post-run scripts of §5 and §6 rely on this.

### 2.4 Description length under A5

**The family does not fit the budget unquantised.** N1 as a rule alone costs about 18 kbits
(`HARNESS-CONTROLS.md` R1 row: its armed table of equal length is 18,052 bits), about twice the
one-tenth limit, and a BF term costs 130 · r · 32 bits more. So "N1 + BF_r + X" is admissible only
with every per-type number on a quantisation step, and only at r = 1: each extra rank costs at
least 130 × 5 = 650 bits, and the table below has 106 bits to spare.

**Data arrays** (names chosen short, since A5 charges 8 bits per character):

| array | contents | A5 cost, worst case | expected |
|---|---|---|---|
| `Q__sym32` | one flat vector of 5-bit symbols: a, b, u, v, α, β, A, B (8 × 65 = 520), W (16), m (n_m ≤ 48) | 584 × 5 + 64 (name) + 24 (shape) = **3,008** | n_m ≈ 30: 2,918 |
| `c` | 6 float32: c, and the scales of (a, b), (u, v), (α, β), W, m | 192 + 8 + 10 = **210** | 210 |
| `L` | the library, integers: for each set its length, then its du's, then its dv's | **≤ 800** by the cap | about 600 |
| `e__sym8` | e (65) and f (65), 3-bit symbols | 390 + 56 + 20 = **466** | 466 |
| `s` | sign, 65 booleans | 65 + 8 + 18 = **91** | 91 |
| **data total** | | **4,575** | about 4,285 |
| decode program | capped at **600 bytes** after lzma (§2.5) | **4,800** | about 4,500 |
| **DL(rule)** | | **9,375** ≤ 9,481.2 | about 8,800 |

- Every array shape is fixed before data, except the library and n_m, which are capped. So the
  worst case is known now, and P2's length half cannot fail once the decode program passes its
  size gate.
- For comparison: rule #1's charged program was 4,440 bits (`first_rule_k12/RESULT.md` P2 line).
- **k\*** will be 0 (D_0^N1 is N1, about 18 kbits, longer than the rule), so P2's D_k^N1 opponent is
  N1 in-sample. **k\*_armed** will be small but not 0, since the rule is longer than 7,721 bits
  (`HARNESS-CONTROLS.md` finding 1): the armed table holds a few cells.

**The quantisation cost, estimated before data.** With 5-bit symbols over a range of about ±4 on
a and b, each logit term carries a uniform error of about ±0.13, a logit variance of about 0.015
in total. Its expected cost in held-out log-loss is about ½ · E[p(1 − p)] · 0.015 ≈ 0.001 nats,
before the coordinate-descent pass reduces it. That is small against the effects in §4, but it is
paid against an opponent (BF_1) that stores 32-bit floats and pays nothing for them.

### 2.5 Gates before the real run (the learner is an instrument of its own)

Each gate runs on synthetic banks or on shuffled bank 0, never on the real bank. A failed gate
**stops the work**. The rule is then not run, and any fix goes through a new registration, as for
rule #1's search (option B).

**Two gate banks, GB1 and GB0** (new glossary term). Both use the real 65 types and their real
admissible fields, the harness's folds by cell position, and numpy `Generator(PCG64(60000))`,
consumed in this order:

1. a_s, b_t ~ N(0, 1) (65 + 65); u_s, v_t ~ N(0, 0.7²) (65 + 65);
2. per type, a source template and a target template: two indices drawn uniformly, with
   replacement, from the real bank's 604 non-empty cells in sorted (s, t) order; the template is
   that cell's `in_json` offsets and counts;
3. per type, a target flag π_t ~ Bernoulli(0.5);
4. per source type, a sign: +1 with probability 0.62, else −1;
5. per cell, u₁ ~ U(0, 1) for existence, u₂ ~ U(0, 1) for noise, and one uniform index into the
   604 real non-empty cells.

- **GB1 (signal).** logit = −2.0 + a_s + b_t + u_s·v_t + W*[G(s), G(t)], with W* fixed now:
  rows = source group, columns = target group, both in the order (input, intermediate, output,
  stride-3):
  `[[−1.5, +2.0, −1.0, 0.0], [0.0, +1.0, +0.5, 0.0], [−1.0, 0.0, +1.0, 0.0], [0.0, +1.5, 0.0, −1.0]]`.
  A cell exists if u₁ < σ(logit). Its offset set and counts are the target's template if π_t = 1,
  else the source's template; with probability 0.2 (u₂ < 0.2) they are replaced by the content of
  the drawn real cell. Its sign is the source's.
- **GB0 (null).** The same draws with W* = 0 and π_t = 0 for every type.

| id | criterion | expected |
|---|---|---|
| **G-e+** | On GB1, the rule's held-out existence score beats BF_1's (A7's τ) in ≥ 9 of 10 folds. | pass |
| **G-e0** | On GB0, the rule's mean held-out existence margin over N1 minus BF_1's is ≤ +0.002 nats. X_e must find nothing where nothing is planted. | pass |
| **G-o+** | On GB1, the rule's held-out offset Jaccard beats N_EB's in ≥ 9 of 10 folds. | pass |
| **G-o0** | On GB0, the rule's mean held-out offset Jaccard minus N_EB's lies in [−0.010, +0.010]. The side choice must not damage a bank where only sources matter. | pass |
| **G-bf** | With X switched off (W ≡ 0, one round) and no quantisation, the learner's (u, v) and existence predictions equal the harness's BF_1 on shuffled bank 0, all 10 folds, to 1e-9. | pass |
| **G-size** | The decode program compresses to ≤ 600 bytes under A5's lzma rule, measured on the file alone. It imports only numpy and the standard library. | pass |
| **G-det** | Two fits of the same training view give byte-identical data (GB1, fold 0). | pass |

G-size is checked first, before any fit. If the decode program cannot be written within 600 bytes,
this proposal comes back for re-registration; it is not squeezed after any score exists.

## 3. How this family was chosen, and what I had read (contamination caveat)

Rule #1's family was chosen after reading whole-bank regularity numbers (its proposal §4.5). The
same kind of caveat applies here, in a different form, and it travels with any result.

**What was chosen for me.** The skeleton "N1 + BF_r + X, with X touching existence and offset sets"
was set by CC's brief. That brief follows from the registered predictions' §4c (by construction,
no other skeleton containing BF_r can pass C6) and from the handover's step 0. Both rest on
**held-out exam numbers**: the BF rank profile, N_EB's offset score, and the first rule's full
record. So the skeleton was chosen after seeing held-out numbers of the real bank. I did not open
the step-0 check itself (`results/genome/c6/checks/n1_alone/`).

**What I chose, and what I had read when I chose it.**

- Before choosing X, I had read the handover; the registered predictions (which quote the BF
  profile at r = 1, 3, 4, 8, 12, 16; N1's, N0's and N_EB's held-out scores; the first rule's P1–P4,
  dial and leave-one-type-out means); the blind reader report (Parts A and C–E); the spec and the
  three acceptance files; `HARNESS-CONTROLS.md` (N_EB 0.4842; BF_8 by starts; the A6-D in-sample
  numbers; the hub check); `harness.py` in full; rule #1's proposal (which quotes whole-bank
  regularity numbers: 594 of 604 signs predicted by the source, 212 of 604 pairs `(0,0)` only, 144
  shapes, 225 exact sets, k90 = 18, the 59 and 62 distinct rows and columns); rule #1's
  `RESULT.md`; Zcode's rule-side notes; four columns of `types.csv` (the field counts of §2.1);
  `results/genome/bank/README.md` lines 36–105; three grep lines of
  `results/diagnostics/labels/partition.json`; the `program_bits` block of
  `harness_controls.json` (lines 19–28); rule #1's `fit.py` interface lines and `README.md`.
- **X_e** (field groups) was chosen because BF_r does not read the fields and the reader's Part A.3
  names them as the one admissible source BF lacks. I have **not seen any number relating field
  groups to existence** on any bank.
- **X_o** (target side) was chosen because N_EB, the strongest offset null, reads only the source,
  and rule #1's source-free offset field lost to it. I have **not seen any target-side offset
  statistic** on any bank.
- **r = 1** was forced by the budget (§2.4). **It is also the lowest P4 threshold in the known
  profile** (+0.02815, against +0.03972 to +0.04933 at r = 3–16), and I knew that when I wrote it
  down. A reader should weigh a P4 pass at r = 1 with that in mind. §5 reports the rule's margin
  beside BF_2, BF_3 and BF_4 so that nobody reads a pass at r = 1 as "beats the best
  factorisation".
- All caps, bit widths and constants (32 sets, 800 bits, 48 offsets, 5 and 3 bits, μ = 1, 3
  rounds, 12 hours) come from the A5 arithmetic in §2.4 or are stated conventions. None was tuned
  on data.

**What I did not open:** `REGULARITY-READING.md`; `result.json` of any run; `harness_controls.json`
beyond the `program_bits` block; `checks/n1_alone/`; `offsets.csv`, `type_pairs.csv` and the other
columns of `types.csv`; the first-rule search criterion; rule #1's `decode.py` source, gates and
spread log. **Nothing was run** except `git log`, `date`, a sha256 of `harness.py`, and `awk`
counts of four `types.csv` columns.

## 4. Thresholds, predictions and branches

### 4.1 The exam's thresholds (C6 as registered; nothing is changed)

P1: ≥ 9 of 10 fold wins on existence vs N1, and on offset vs **each** of N1, N0 and N_EB; counts
and sign ≤ 2 losses of 10 vs N1 with a fold mean not worse. P2: DL ≤ 9,481.2 bits, and in-sample
beats D_k^N1 at k\* (= N1), D_k^N0 at k\*_armed, and N1, on existence and offset. P3: existence and
offset margins over N1 above all 99 shuffled banks by more than τ = 1e-9. P4: existence margin over
N1 above **+0.02815** (r = 1, k = 10) by more than τ. Both τ conditions come from the harness change
that aligns P3 and P4 with spec A7, committed before this run (§1). **This registration adds the
P4 tie band:** P4 counts as passed only if Δ = margin − threshold > +0.002 (§1). **Only the
registered run's verdict counts.**

### 4.2 The author's own predictions (additional to the registered ones)

Each has a claim, a quantity, a refuting outcome and my probability. P = C6 arm.

| id | arm | claim | quantity | refuting outcome | undetermined | my probability |
|---|---|---|---|---|---|---|
| **S2-1** | P1 existence | passes | ≥ 9 of 10 fold wins vs N1 | ≤ 8 wins | — | 0.85 |
| **S2-2** | P1 offset | **fails, on N_EB** | wins vs N1 ≥ 9 and vs N0 ≥ 9, but vs N_EB ≤ 8; held-out mean Jaccard ∈ [0.475, 0.505] | ≥ 9 wins vs N_EB (claim refuted); Jaccard outside the band (quantity refuted) | — | fail vs N_EB: 0.75 |
| **S2-3** | P1 counts | passes | ≤ 2 losses vs N1, mean not worse; mean counts margin over N1 ∈ [+0.030, +0.100] (lower MAE) | > 2 losses or mean worse (claim); margin outside the band (quantity) | — | 0.75 |
| **S2-4** | P1 sign | tie | — | — | — | **definitional** (§1), not a prediction |
| **S2-5** | P2 | in-sample beats N1 on existence and on offset set | in-sample offset margin over N1 > τ | offset margin ≤ τ (P2 fails on offset) | — | 0.75 |
| **S2-6** | P3 existence | passes | real margin − shuffled max ≥ +0.010 nats | any shuffled margin ≥ real (claim); gap < +0.010 with the arm passing (quantity) | — | 0.8 |
| **S2-7** | P3 offset | **fails** | real offset margin over N1 ≤ its shuffled max | P3 offset passes | — | fail: 0.6 |
| **S2-8** | P4 | **X adds held-out existence information beyond BF_1** | a **real amount**: Δ = rule margin − BF_1 margin ≥ max(+0.005, 2 × the paired standard error of the ten per-fold Δ's). The bar always lies above the tie band. | Δ ≤ +0.002: a P4 fail or, for \|Δ\| ≤ 0.002, a registered tie. Either refutes the claim. | +0.002 < Δ < the bar: P4 passed under the tie band, but not a real amount by this item | Δ > 0: 0.5; Δ > +0.002 (clears the tie band): 0.4; Δ at or above the bar: 0.3 |
| **S2-9** | whole exam | fails | verdict FAIL | verdict PASS | — | 0.95 |

Notes:

- **S2-8 is the item the family exists for.** Its bar is the "real amount" the brief asks for. The
  paired standard error needs BF_1's per-fold scores. §6 gets them without a harness change.
- **Three zones, fixed before the run:**
  - Δ ≤ +0.002: fail, or a tie. The tie band covers quantisation and fold noise.
  - +0.002 < Δ < the real-amount bar: a P4 pass under this registration, but not a real amount.
  - Δ at or above the bar: a real amount.
- **The registered predictions P-J3, P-A3 and P-B5 are unchanged.** Their claims are about the
  harness's P4 verdict as registered. The tie-band reading is printed beside that verdict (§1),
  and both are reported.
- **P1 offset against N1 and N0 is expected to pass** (S2-2). The claim is only that N_EB is not
  beaten in 9 folds. The 0.475–0.505 band sits on both sides of N_EB's 0.4842.
- S2-6 rests on the reader's A.1 point: on existence P3 passes only if the rule is worse on the
  shuffled banks than on the real one. Degree-preserving rewiring destroys field-group blocks and
  most low-rank structure except at the hubs.

### 4.3 Why the rank arithmetic matters (Zcode ruled r = 1; §1)

Under a different rank count, r = 4, the P4 threshold would be BF_4's **+0.03972**
(`harness_controls.json`, `controls["real/PR"].P4.bf.margin`, predictions file §4c), and my
probability of Δ > 0 would fall from 0.5 to 0.15. Zcode ruled on 2026-09-23 at 13:17 UTC that r is
computed by A11's rule, which gives r = 1 (§1). The r = 4 case is not a branch of this registration.
It is printed only as context, as the BF_4 row of the mandatory BF_1–BF_4 line.

### 4.4 The registered predictions: which branch applies

Field choices (§1): existence touched, offset sets touched, counts touched (no new per-node counts
term), sign not touched.

| registered item | branch that applies | what I expect |
|---|---|---|
| **P-J1** (margin ≥ +0.040) | prediction (existence touched) | **Not confirmed.** Its band was set on BF_r at r ≥ 3. At r = 1 the rule's bilinear part is BF_1-like (+0.02815). I expect a margin in [+0.025, +0.040): P-J1 undetermined if ≥ +0.030, refuted below. |
| **P-J3** (P4 fails; Δ ≤ 0; margin ∈ [BF_r − 0.005, BF_r]) | prediction, judged on the harness's P4 verdict as registered | At r = 1 the band is [+0.02315, +0.02815]. I give it about 0.5 (S2-8). A Δ in (0, +0.002] refutes P-J3 on the harness verdict, while this registration's tie band reads it as a tie. Both readings are printed (§4.2). |
| **P-J4** (P3 offset needs Jaccard ≥ 0.4831) | prediction (offset touched) | Agree. If P3 offset passes, I expect the Jaccard to exceed 0.4842. |
| **P-J5** (counts tie) | **no prediction** (offset touched) | Johnny's caveat does not apply: no new per-node counts term. My own counts item is S2-3. |
| **P-A1** (dial ratio; needs m(0.0) ≥ +0.040) | existence touched, but the condition is expected to fail | I expect m(0.0) < +0.040, so **no prediction**. If m(0.0) ≥ +0.040, the item applies as registered. Record-only either way. |
| **P-A3** (P4 fails; rule − BF_r < +0.005 **and** margin ≥ +0.040) | prediction | **Finding: at r = 1 its quantity is empty.** Margin ≥ +0.040 means rule − BF_1 ≥ +0.0118, which contradicts rule − BF_1 < +0.005. No outcome can confirm the quantity; only the claim (P4 fails) is testable. It is not edited here. |
| **P-A4** (offset margin grows under destruction by ≥ +0.005) | prediction (offset touched) | **Refuted, I expect**: m_off(1.0) < m_off(0.0). Both of X_o's sides are per-type, and the shuffle destroys them. On shuffled cells the rule falls back toward the global smoothed set, as N_EB does. |
| **P-A6** (in-sample offset margin ≤ τ) | prediction (offset touched) | **Refuted, I expect** (S2-5). The source side maximises expected Jaccard over the source's own training sets, which contains N1's modal-set choice as a candidate when that set is in the library. |
| **P-B1** (P3 existence passes; margin ≥ +0.040; gap ≥ +0.015) | prediction | Claim confirmed, quantity refuted: I expect P3 existence to pass (S2-6) with a real margin below +0.040. |
| **P-B2** (P3 offset fails unless Jaccard > 0.4842) | prediction | Agree (S2-7). |
| **P-B3** (starts: \|Δ(k = 10 vs 3)\| < 0.001) | prediction; its rule half needs the k = 3 descriptive run (§5.3) | Agree. |
| **P-B4** (BF_r ∈ [0.045, 0.052] at r ≥ 8) | **does not apply** (r = 1) | — |
| **P-B5** (P4 fails; rule − BF_r < +0.005) | prediction | About 0.7 for the quantity, 0.5 for the claim (S2-8). |
| **P-B6** (≥ 9 of 10 existence wins vs N1) | prediction (existence touched) | Agree (S2-1). |
| **LOTO registration note** (ratio 1.00 for a BF rule whose addition vanishes on unseen types) | **does not hold by construction here**: X_e does not vanish on an unseen type, since its field group is known. | Descriptive expectation: leave-one-type-out existence rule_mean / n1_mean < 1.00, and below Ark's 1.3 red flag. |

## 5. Transferred checks, reworded

All of these are **descriptive**. They run **after** the registered run's record is written and
committed, through scripts that import the harness (like `checks/n1_alone.py`), not through
`--rule`. None of them produces a verdict. **Choosing among variants after seeing their results is
not allowed**: only the registered run's verdict counts.

### 5.1 The randomised-inputs arm: a resolution report, not a verdict arm

Rule #1's random-label arm (its proposal §4.3) asked whether the latent variables carried structure
or only capacity. X has no fitted latent variables. What it reads per type is the field group
(X_e) and the target-side offset information (X_o). The reworded arm randomises exactly those:

- **Randomisation:** a permutation of the 65 types, from `Generator(PCG64(50000 + j))`, j = 0–4. It
  is applied to the field-group vector (so group sizes 8, 21, 34 and 2 are kept) and, with the same
  permutation, to the target-side pair (B_t, f_t). Everything else is refitted as registered.
- **Split:** the primary 10 folds of the real bank only (10 fits per seed, 50 in all).
- **Reported:** per seed and per fold, the existence log-loss and offset Jaccard of the registered
  rule and of the randomised rule; the paired difference (registered − randomised), its mean and
  its standard deviation over folds.
- **Resolution, named before the run:** the arm resolves a mean difference only if it exceeds
  2 × SD / √10 of the paired per-fold differences. The effect it looks for is X's own size, which I
  expect to be about +0.005 nats on existence and +0.005 to +0.010 in Jaccard. Zcode estimated
  rule #1's arm at a resolution of about 0.02 against an effect of about 0.005. **If the
  resolution printed is coarser than the effect sought, the arm is recorded as "unresolved", not
  as evidence either way.**

### 5.2 Sensitivity on the rule's own dimension parameter (not starts)

The rule's complexity knob is the rank of its bilinear term, r_b. The registered run has r_b = 1.
Descriptively, r_b ∈ {0, 2} are run on the primary split with everything else unchanged:

- r_b = 0: N1 + X only. This is X's margin with no bilinear term.
- r_b = 2: over the one-tenth limit by about 650 bits (§2.4). Its DL is reported, and its P1
  numbers are still read.

At each r_b ∈ {0, 1, 2} the report gives: the rule's mean existence margin over N1; BF's margin at
the matching rank (BF_1 for r_b = 0 and 1, BF_2 for r_b = 2, fitted by the harness's own
`bf_predictor` at the run's k); and their difference, mean and paired SD. The sweep itself is
descriptive.

**Mandatory, not optional (Zcode's ruling):** the registered run's record prints, directly under
its verdict line, the rule's margin minus BF_1's (the decision) and minus BF_2's, BF_3's and BF_4's
(context), as fixed in §1. That line does not wait for the sweep. It is written by the post-run
script from the record and the deterministic BF refits (§6), and the record is not complete
without it.

### 5.3 Starts, k = 3 (for P-B3)

The rule and BF_1, primary split, at k = 3, compared with the registered k = 10 run: the change in
each one's mean existence margin. Descriptive.

## 6. Harness changes: none needed

| wanted | how, without a harness change | needed for the verdict? |
|---|---|---|
| **Per-fold BF_1 and RP_1 scores**, for the paired read of S2-8 and P4 | BF and RP fits are seeded and deterministic. A post-run script recomputes `cv(bf_predictor(1), REAL)` and the RP_1 fits at the run's k, and pairs them with the record's `per_fold_rule`. **Check:** the script's mean BF_1 margin must equal the record's `P4.bf.margin` to 1e-12. If it does not, the paired read is void and is reported as such. | Not for the harness's P4 verdict (the fold mean, above the threshold by more than τ). **Yes for the record:** the mandatory BF_1–BF_4 line and the paired read of the tie band and of S2-8 need it. |
| **Per-type leave-one-type-out values** | The same way: the rule is deterministic (G-det), so a script recomputes `loto_fold` for the rule and N1 and writes all 65 rows. | No. Descriptive (spec §4.5). |
| **The spread-log check** | Rule-side, not in the harness. The learner writes **one file per fit** (named by the bank name and a sha256 of the training mask) into a directory it creates itself. Rule #1 appended from 30 worker processes to one shared file (`fit.py` line 602); lost or interleaved appends are a plausible cause of its missing line, though that was not investigated. After the harness has written and the run has been committed, a script counts the files against the 1,341 fits expected and writes `spread_log_validation.json`. | No. **Recommendation for Mike (predictions file §4b item 6):** the record is written first and the check after. A mismatch marks the spread log unreliable and **does not void the verdict**, since no verdict number derives from it. |

- So rule #2 needs **no harness change of its own**, and no `--controls` re-run is required on its
  account (A20).
- **The τ change is separate from this rule.** It aligns P3 and P4 with spec A7 (a margin must
  exceed its comparison by more than τ = 1e-9). It is committed with its own `--controls` re-run
  before rule #2's run. Rule #2 runs on that harness, and its record stamps that harness's sha256.
- **A20: handled.** The `--controls` re-run owed since commit `958a976`, which added the rule path
  after the last controls run (recorded sha256 `071d826a…`), is **done**: commits `1789aeb` (τ in
  P3/P4) and `8046fa1` (controls on harness sha256 `6fc80952…`). Every value in
  `harness_controls.json` is identical to the previous run except the harness sha and the run time,
  so every verdict is unchanged. Rule #2 runs on harness `6fc80952…`.
- If Zcode prefers these outputs inside the harness record (per-fold BF/RP, per-type LOTO, and the
  assert placed after the record is written), that is a harness change: `--controls` must be re-run
  with every verdict unchanged (A20) before rule #2's run. This is optional.

## 7. Honest risks

**The likeliest failure: the offset set.** N_EB is a strong null (0.4842 against N1's 0.4204).
X_o adds target-side evidence through a coarse switch (two 3-bit levels, ties to the source) and
restricts every choice to a 32-set library, which N_EB does not. The library cap alone can cost
Jaccard on sources with unusual but consistent sets. Beating N_EB in 9 of 10 folds needs a
consistent gain, not an average one. On the shuffled banks the rule's offset field falls back
toward the global smoothed set, which is at least as good as N0's modal set. So its shuffled max
is probably at or above the +0.06267 every rule so far has shown, and P3 offset needs a real
Jaccard above about 0.485–0.49. I expect "copy or marginal" and "family fits anything" from the
offset field, whatever existence does.

**P4: my prior is 0.5 for Δ > 0, 0.4 for clearing the ±0.002 tie band, and 0.3 for a real
amount (S2-8).** The tie band exists because quantisation alone costs about 0.001 nats and fold
noise adds to it. So a harness P4 pass by less than 0.002 is not read as a pass. For the pass:
- X_e reads the one input BF_1 cannot learn from data: a type's group is known exactly, even for
  a type with few training cells.
- The four groups are anatomical stages (retina, lamina-like intermediates, output units, and the
  two stride-3 types). Wiring between stages is not additive in source and target, so a 4 × 4 table
  plausibly carries existence information beyond one bilinear direction.

Against it:
- The first bilinear direction BF_1 learns may already *be* that stage contrast. Then X_e adds
  little.
- Quantisation costs about 0.001 nats against an opponent that stores 32-bit floats for free.
- The four groups are coarse (two bits per type). The 2-type stride-3 group is almost per-type,
  so its penalised entries do little.

**Rank accounting (ruled: r = 1, by A11's arithmetic in §1).** Had X_e been counted toward r, the
threshold would have been +0.03972 and P4 unlikely (0.15). The arithmetic is written into the
registration so that this choice is visible.

**Size.** The decode program must fit in 600 compressed bytes, and rule #1's needed 555 for a
simpler output path. If G-size fails, the proposal returns before any fit.

**Honesty of the rank-1 choice.** It is forced by the budget and also the lowest known threshold
(§3). A P4 pass at r = 1 says "beats a trained factorisation with the same number of fitted
interaction numbers". It does not say "beats BF_3 or BF_4". The mandatory BF_1–BF_4 line (§1, §5.2)
prints all four beside the verdict.

**Search.** The bilinear part is BF's own algorithm, and the other parts are closed-form or convex
ridge fits, so the search risk that stalled rule #1 is small. G-bf and G-det check it.

## 8. Blind-safe summary (for Ark, Johnny and the blind reader)

This section gives only the registration fields, the thresholds and the arms touched. It gives no
mechanism, no latent variables and no fitting details.

- **Rank, computed by A11's rule (not declared; Zcode's ruling, 2026-09-23 13:17 UTC):**
  r = round((130 + 16) / 130) = 1.
  - 130 is the number of fitted per-type numbers in the rule's interaction terms.
  - 16 is the number of fitted numbers in a term on a fixed partition, which has no per-type
    coordinates.
  - The registration carries this arithmetic itself and does not rely on the harness's fallback
    rank count. That fallback would also give 1, but by a degenerate count.
  - At r = 4 the threshold would be +0.03972, and the author's P4 prior would drop from 0.5 to 0.15.
- **P4 threshold:** +0.02815 at k = 10 (BF_1's margin over N1 from the existing rank profile). The
  run's own printed threshold governs.
- **P4 tie band (registered before the run):** a margin within ±0.002 of the threshold is read as
  a tie, not a pass, because quantisation (about 0.001) and fold noise sit at that scale. P4
  counts as passed for this registration only if the margin exceeds the threshold by more than
  0.002. A "real amount" is at least max(0.005, 2 × the paired standard error).
- **Mandatory printing:** under the verdict line, the record prints the margin against BF_1 (the
  decision) and against BF_2, BF_3 and BF_4 (context).
- **τ:** P3 and P4 now require a margin to exceed its comparison by more than τ = 1e-9. This is a
  separate harness change that aligns them with spec A7, committed (`1789aeb`) with a `--controls` re-run
  before this run.
- **Timing cap:** 10 starts, unless the projected wall time measured on shuffled bank 0 exceeds 12
  hours; then 3 for the whole run. Decided and recorded before any real-bank fit.
- **Fields touched:** existence yes; offset sets yes; counts yes (scored on changed offset sets,
  with no new per-node counts term); **sign no** (identical to N1's on every cell).
- **By construction:** P1 sign ties N1 and P3 sign is 0 on all 100 banks. Neither of §4c's
  by-construction fails applies. DL is capped at 9,375 bits, under the one-tenth limit.
- **Registered-prediction branches** (predictions file §4c): P-J4, P-A4, P-A6 and P-B2 are
  predictions (offset touched). P-J5 is "no prediction". P-J1, P-J3, P-A3, P-B1, P-B5 and P-B6 are
  predictions (existence touched). P-B4 does not apply (r < 8). P-A1 makes no prediction unless
  the real margin reaches +0.040.
- **Finding for the predictions' authors:** at r = 1, P-A3's quantity (margin ≥ +0.040 **and**
  rule − BF_r < +0.005) is empty, because BF_1 is +0.02815. Only its claim (P4 fails) can be
  tested. The file is registered and is not edited; this is recorded here.
- **The author's expectations by arm:**
  - P1 existence: pass.
  - P1 offset: fail against N_EB.
  - P1 counts: pass.
  - P2: pass.
  - P3 existence: pass.
  - P3 offset: fail.
  - P4: about even odds of a margin above BF_1's, and 0.4 of clearing the tie band.
  - Whole exam: FAIL expected (probability of a pass ≤ 5 %).
- **Descriptive only, after the run** (no verdict): a randomised-inputs resolution report, a
  sensitivity sweep on the rule's own complexity parameter (with BF's margin at each value), a
  k = 3 starts comparison, per-fold opponent scores and per-type leave-one-type-out values. **No
  harness change of its own** is needed. The spread-log check runs after the record is written and
  does not void the verdict. The A20 `--controls` re-run is done (`8046fa1`, every verdict unchanged).
- **A finding about the exam's inputs** (structural, blind-safe): the admissible per-type fields
  collapse to four groups of 8, 21, 34 and 2 types, and `role` equals `layout` on every type.

## 9. Questions before registration

1. **Rank: closed.** Zcode ruled (2026-09-23 13:17 UTC) that r is computed by A11's rule:
   r = round((130 + 16) / 130) = 1 (§1). The printing of BF_1–BF_4 is mandatory.
2. **The spread-log check: before or after the record, and does it void the verdict? (Mike;
   predictions file §4b item 6.)**
   - *Affects:* whether a logging fault can erase a finished exam.
   - *Recommendation:* after the record, and it does not void the verdict (§6). Still open unless
     Mike has answered it.
3. **The A20 `--controls` re-run: done** (`8046fa1`, every verdict unchanged). The separate τ change to P3 and P4
   is committed with its own controls re-run before rule #2's run.
4. **Register this proposal? (Mike approved going ahead, 2026-09-23 13:26 UTC.)**
   - *Affects:* once it is committed, none of its constants may change after any number is seen.
   - *Recommendation:* commit it once the τ change and the controls re-run are committed. The run is
     informative even if it fails:
     - it measures whether the only per-type facts the exam admits carry held-out existence
       information beyond a rank-1 factorisation;
     - it measures whether target-side evidence moves the offset set beyond N_EB.

## Files opened for this proposal

- `docs/briefs/2026-09-23-next-session-handover.md`
- `docs/plans/2026-09-23-first-rule-failure-predictions.md`
- `docs/plans/2026-09-23-blind-reader-report.md` (Parts A–E)
- `docs/plans/2026-09-23-c6-control-specification.md`
- `docs/plans/2026-09-23-c6-amendment-acceptance.md`, `-2.md`, `-3.md`
- `results/genome/c6/HARNESS-CONTROLS.md`
- `results/genome/c6/harness.py` (in full); `results/genome/c6/decoders/n1_decode.py`,
  `bf_decode.py`; byte sizes of the decoders
- `results/genome/c6/harness_controls.json`: the `program_bits` block only (lines 19–28), and a
  grep for its `harness_sha256_lf` line
- `docs/plans/2026-09-23-first-rule-proposal.md`
- `docs/plans/2026-09-23-first-rule-failure-rule-side.md`
- `results/genome/c6/rule_runs/first_rule_k12/RESULT.md`
- `results/genome/c6/rules/first_rule/README.md` (first 40 lines); grep lines of `fit.py`
  (interface and spread log); byte sizes of `decode.py` and `fit.py`
- `GLOSSARY.md`
- `results/genome/bank/types.csv`: the header and the four admissible field columns (by `awk`)
- `results/genome/bank/README.md`, lines 36–105, and a grep for role and layout
- `results/diagnostics/labels/README.md` and `partition.json`: grep lines for `layout`
- `git log` of `harness.py` and `harness_controls.json`; `git show --stat` of `958a976`
