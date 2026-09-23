# Rule #2 gates: is the fault in the scales or in the weight?

**What this is.** A diagnosis of the two gates that failed in the single gate run (`gates.json`,
commit `e7e31fb`): **G-e+** (8 of 10 folds, 9 needed) and **G-o0** (−0.01996, band ±0.010). Mike
asked for it in the DPC Research group chat on 2026-09-23 at 16:41 UTC: why "the scales" (the gates
of the proposal's §2.5) do not work, and how to make them work.

**What this is not.** It is not a gate, not a fix and not a registration. Nothing in `fit.py`,
`decode.py`, `gate_banks.py`, `gates.py`, `harness.py` (sha256 `6fc80952…`) or the registered
proposal (`docs/plans/2026-09-23-second-rule-proposal.md`, commit `c3f996d`) was changed. The
gate verdict stands: **G-e+ and G-o0 FAILED, and under §2.5 the work stays stopped.** Any fix
below needs a new registration.

**Data touched.** Synthetic banks only: the registered gate banks GB1 and GB0 (seed 60000, already
seen by the gate run) and new draws of the same construction on **diagnostic seeds**. The real
bank, real folds and shuffled bank 0 were not used, and no score was computed on them.

**Scripts and records** (all in this directory):

| file | what it holds |
|---|---|
| `diagnosis.py` | Builds the banks and fits every model, fold by fold. Stages `registered`, `gb0`, `power` and `summary`. |
| `diagnosis_summary.py` | Aggregates. Every number below comes from `diagnosis_summary.json` unless another file is named. |
| `diagnosis_registered.json` | Seed 60000: per-fold scores of every model on GB1 and GB0, the fixed-λ sweep, the offset decomposition and the library-cap sweep. |
| `diagnosis_power_rows.json` | 3,000 rows: GB1-type banks, 100 diagnostic seeds × W* scaled by 1, 2 and 4 × 10 folds. |
| `diagnosis_gb0_rows.json` | 1,000 rows: GB0-type banks, 100 diagnostic seeds × 10 folds, with the library-cap sweep. |
| `diagnosis_summary.json` | All aggregates, including the reproduction check against `gates.json`. |
| `diagnosis_banks.json` | Every bank built (402), each with its seed, W* scale, non-empty count and a sha256 of its content. |

The three row files were written by `diagnosis.py` at sha256 `2fc86010…` (stamped in each), at
k = 10 starts, on harness `6fc80952…` and `fit.py` `d8dbb332…`. Reproduction: the diagnosis
re-fits the registered banks and matches `gates.json` exactly (largest difference 0.0 for the
rule, BF_1, N1 and N_EB, existence and offset; `reproduction_of_gates_json_max_abs_diff`).

Run from the repository root:
`tools/.venv/Scripts/python.exe results/genome/c6/rules/second_rule/diagnosis.py registered|gb0|power|summary`
(about 70 minutes on 30 processes in all).

## Seed discipline

| range | use |
|---|---|
| 60000 | The registered gate banks GB1 and GB0. Already seen by the gate run, and re-used here. |
| 61000 | ST0, the post-run self-test bank. Not used here. |
| **70000–70999** | **Diagnostic range.** Seeds **70000–70099** were used: each seed gives one GB0-type bank and three GB1-type banks (W* × 1, 2, 4), all from `gate_banks.draws(seed)`. |
| **80000–80999** | **Reserved for a future re-gate.** Nothing was generated, fitted or scored on it. `diagnosis.py` asserts that no seed in this range is built. |

The thresholds proposed below were calibrated on 70000–70099. A re-gate must therefore draw its
banks from the reserved range, which no calibration has seen.

## 0. The answer

| gate | fault | the numbers in one line |
|---|---|---|
| **G-e+** | **Scales.** The count "≥ 9 of 10 folds" is underpowered, and the registered GB1 was an unlucky draw. The weight is adequate. | On the registered GB1, the rule beats BF_1 on the fold mean by +0.00781 nats (paired t = 3.4), yet wins only 8 folds. On 100 fresh draws, the rule passes the 9-of-10 count 89 times, and a model that **knows the planted table W\* exactly** passes only 93 times. The registered GB1 is a 1st-percentile draw: only 1 % of draws show a rule advantage as small. |
| **G-o0** | **Weight.** The rule's 32-set, 800-bit offset library cannot hold what N_EB can choose from. The scales are fine. | On 100 fresh GB0 draws, the rule passes 10 times, with a mean of −0.0328. The library restriction costs −0.0291 and the side switch −0.0039. An N_EB-equivalent predictor never leaves the band (paired SD 0.00085, worst 0.0035). The registered −0.01996 is milder than typical. |

G-e0 and G-o+ passed, but neither shows that a threshold was calibrated (§3). **No threshold in §2.5
was set by a power or noise calculation.**

## 1. G-e+ (GB1: the rule beats BF_1 on held-out existence in ≥ 9 of 10 folds)

### 1.1 Per fold on the registered GB1 (`registered_GB1.per_fold`)

Existence is a held-out log-loss in nats (lower is better). Margin over N1 = N1 − model.
"Advantage" = BF_1 − model, so a positive value means the model beats BF_1 (a win needs > τ = 1e-9).

| fold | N1 | BF_1 | rule | rule margin over N1 | BF_1 margin over N1 | **rule − BF_1 advantage** | λ rule | λ BF_1 |
|---|---|---|---|---|---|---|---|---|
| 0 | 0.43717 | 0.41936 | 0.40829 | +0.02888 | +0.01782 | **+0.01106** | off (100) | 3 |
| 1 | 0.42306 | 0.41832 | 0.40520 | +0.01786 | +0.00474 | **+0.01312** | off (100) | 3 |
| 2 | 0.43702 | 0.42435 | 0.42502 | +0.01199 | +0.01267 | **−0.00068** | 3 | 3 |
| 3 | 0.45296 | 0.44062 | 0.42532 | +0.02764 | +0.01234 | **+0.01530** | off (100) | 3 |
| 4 | 0.46519 | 0.45391 | 0.43584 | +0.02935 | +0.01128 | **+0.01807** | off (100) | 3 |
| 5 | 0.45690 | 0.44821 | 0.44548 | +0.01142 | +0.00870 | **+0.00272** | 3 | 3 |
| 6 | 0.42665 | 0.40834 | 0.39695 | +0.02969 | +0.01831 | **+0.01138** | 3 | 3 |
| 7 | 0.47005 | 0.46295 | 0.45789 | +0.01216 | +0.00711 | **+0.00505** | 3 | 3 |
| 8 | 0.45712 | 0.45024 | 0.44378 | +0.01335 | +0.00688 | **+0.00647** | off (100) | 3 |
| 9 | 0.49559 | 0.48141 | 0.48584 | +0.00975 | +0.01417 | **−0.00442** | off (100) | 3 |
| **mean** | | | | **+0.01921** | **+0.01140** | **+0.00781** | | |

- **Per-fold SD of the advantage: 0.00722.** Paired t = 3.42 (`registered_GB1.models.rule`).
- On the fold mean the rule is clearly ahead of BF_1. It fails the gate on the fold count: 8
  wins, with two small losses.

### 1.2 Truth-knowing reference models ("oracles") on the registered GB1

The brief calls these oracles. They are **not** the glossary's oracle (the A14 control that returns
the true held-out cells). They are labelled O-… here to keep the two apart.

| model | what it knows / fits | folds beating BF_1 | mean advantage over BF_1 | per-fold SD | worst fold |
|---|---|---|---|---|---|
| rule (registered, quantised) | as gated | **8** | +0.00781 | 0.00722 | 9: −0.00442 |
| rule, float (μ = 1) | no quantisation | 8 | +0.00802 | 0.00713 | 9: −0.00449 |
| rule, float, **X_e by plain ML** (μ = 1e-6) | no penalty on W | 8 | +0.00781 | 0.00788 | 9: −0.00561 |
| **O-W\***: knows W\* exactly | c, a, b by N1's ridge with W\* as an offset; u, v by BF_1's algorithm (nested λ) | **9** | +0.00919 | 0.00844 | 9: −0.00753 |
| **O-ML-W**: knows c, a, b, u, v exactly | W by plain ML (μ = 1e-6) | 10 | +0.03715 | 0.01117 | 9: +0.02074 |
| O-true | the generating probabilities | 10 | +0.03873 | 0.01165 | 9: +0.01917 |

Source: `registered_GB1.models`.

- **The fair reference is O-W\*.** Like the rule and BF_1, it has to estimate the 260 per-type
  numbers from about 3,800 training cells, and it is given the planted group table for free. It
  passes the registered GB1 only by the minimum, 9 of 10, and loses fold 9 by more than the rule
  does.
- O-ML-W and O-true win every fold by about +0.037 to +0.039. That lead comes almost entirely from
  knowing the per-type terms, which no predictor can know. On GB0, where nothing is planted in W,
  O-true still beats BF_1 by +0.02346 (`registered_GB0.existence.models.oracle_true`). So these two
  bound what is possible, but they say nothing about X_e.
- **Plain ML changes nothing.** With no penalty on W the rule still wins 8 folds, with the same
  mean. The fixed μ = 1 is not what fails.

### 1.3 The λ = 100 fold, and the 0.00008 and 0.00068

**λ = 100 means "no bilinear term".** The fixed-λ sweep (`lambda_sweep_registered`) refits the
rule's float model and BF_1 at each λ of the grid {1, 3, 10, 30, 100}.

- **In all 20 registered folds (GB1 and GB0), at λ = 10, 30 and 100 the rank-1 term is exactly
  zero, for the rule and for BF_1.**
  - For the rule, the RMS of u·v is at most 2e-15.
  - For BF_1, the held-out loss at λ = 10 equals N1's to 2e-16.
  - Rank-1 ALS with this ridge has u = v = 0 as its solution there.
- So those three λ values are one model, "N1 (+ W) with no bilinear term". The nested scheme's
  "ties go to the larger λ" labels that model λ = 100.
- In practice the grid has three live choices: λ = 1, λ = 3 and "off".
- On GB1 the rule chose "off" in 6 of 10 folds (0, 1, 3, 4, 8, 9), and O-W\* in 5. BF_1 chose λ = 3
  in all 10.
- Over the diagnostic draws at W\* × 1, the rule chose "off" in 49.9 % of folds, and BF_1 in 3.7 %
  (`power_GB1_diagnostic.Wstar_x1.rule_lambda_share`, `BF1_lambda_share`).
- Reading: once W takes the group structure, the remaining rank-1 signal (planted u, v ~ N(0, 0.7²))
  often no longer pays for itself on the inner folds.

**Fold 9 is not lost by the λ choice.** Held-out loss in fold 9 at each fixed λ:

| λ | rule, float | BF_1 |
|---|---|---|
| 1 | 0.50094 | 0.47837 |
| 3 | 0.48606 | 0.48141 (BF_1's choice) |
| 10–100 ("off") | 0.48590 (the rule's choice) | 0.49559 (= N1) |

- At λ = 3 the rule would still lose fold 9, by 0.00465.
- O-W\*, which knows W\* exactly, also chooses "off" there and loses by 0.00753.
- O-true wins fold 9 by +0.01917.
- So fold 9 is lost by every model that has to estimate the per-type terms together with a group
  table. That is fold noise in the estimates, not a fault of the rule's λ choice.
- The README's sentence ("the rank-1 term shrinks towards zero") should be read as: the term is
  exactly zero, and λ = 3 would not have saved the fold.

**The two small numbers** (`small_numbers`) describe the same fold, fold 2 of GB1:

- **0.00008** (7.85e-5): the **unquantised float model's** held-out loss minus BF_1's
  (`gate_diagnostics.json`; README line 100). λ = 3.
- **0.00068** (6.76e-4): the **registered, quantised rule's** held-out loss minus BF_1's
  (`gates.json`). This is the number the gate judged. The 0.00060 between the two is the cost of
  quantisation, the coordinate-descent pass and c's refit in that fold.
- No committed file cites 0.00068 literally. By value, Ark's 0.00068 is this second number.
- In fold 2 even O-W\* wins by only +0.00248.

### 1.4 Power of "≥ 9 of 10 folds" (100 diagnostic draws per strength; `power_GB1_diagnostic`)

Pass rate = the share of the 100 banks on which the model beats BF_1 in ≥ 9 of 10 folds.

| W\* scale | rule (registered) | rule, float | rule, plain ML | **O-W\*** | O-ML-W | O-true | rule: mean advantage (5 %, 50 %, 95 %) | per-fold SD (rule) |
|---|---|---|---|---|---|---|---|---|
| **× 1 (registered)** | **0.89** | 0.93 | 0.80 | **0.93** | 1.00 | 1.00 | +0.0094, +0.0149, +0.0220 | 0.0088 |
| × 2 | 0.98 | 1.00 | 0.92 | 0.98 | 1.00 | 1.00 | +0.0135, +0.0198, +0.0290 | 0.0096 |
| × 4 | 1.00 | 1.00 | 0.95 | 0.99 | 1.00 | 1.00 | +0.0164, +0.0212, +0.0248 | 0.0084 |

- **At the registered strength, even a model that knows W\* exactly fails the gate on 7 of 100
  banks.** The rule fails on 11 of 100.
- Win counts of the rule at × 1: 7 wins on 1 bank, 8 wins on 10, 9 wins on 26, 10 wins on 63.
- A gate that turns away a perfect X_e 7 % of the time has no room for fold noise. The rule sits
  close to that ceiling: its mean advantage is 0.01508, against 0.01635 for O-W\*, about 92 %.
- **The registered GB1 is a tail draw** (`registered_GB1_within_diagnostic_x1`):
  - Only 1 % of the diagnostic banks give the rule a mean advantage as small as the registered
    +0.00781, and only 2 % do so for O-W\*.
  - 11 % give the rule ≤ 8 wins.
  - The rule's margin over N1 is +0.01921 on the registered bank, against a diagnostic mean of
    +0.02469 (SD 0.00534).
- **The fold count wastes information that the fold mean keeps.** Over the same draws:

| criterion | rule, W\* × 1 | O-W\*, W\* × 1 | rule on 100 GB0 draws (false pass) |
|---|---|---|---|
| ≥ 9 of 10 folds (registered) | 0.89 | 0.93 | 0.00 |
| ≥ 8 of 10 folds | 0.99 | 0.98 | 0.00 (at most 7 wins on the null) |
| paired t of the ten advantages > 2 | 1.00 | 1.00 | — |
| **fold-mean advantage > +0.002 (P4's form with the registered tie band)** | **1.00** (smallest bank mean +0.0075) | **1.00** | **0.00** (largest null mean +0.00058) |

Sources: `…Wstar_x1.models.*.pass_rate_*`, `GB0_diagnostic.G_e0.rule_pass_rate_*`.

- C6's own P4 compares the rule with BF_r on the **fold mean** (`harness.py` line 1031:
  margin − threshold > τ; the registration adds the +0.002 tie band). It never counts folds. So
  G-e+ is stricter than the exam arm it stands in front of.

### 1.5 Verdict on G-e+

**The fault is in the scales.**

- The count "9 of 10" fails a model that knows the planted table 7 % of the time at the registered
  strength.
- The registered bank sits in the 1st percentile of the planted effect's size.
- The rule carries about 92 % of the reference model's advantage, and on the registered bank it is
  ahead on the mean with t = 3.4.

A minor weight observation: the λ grid has only two live values, and the rule switches the
bilinear term off in half of the folds. Its measured cost is small: 0.0013 nats of mean advantage
against O-W\*, and 4 points of pass rate against the rule's own float model (quantisation).

## 2. G-o0 (GB0: the rule's mean held-out offset Jaccard minus N_EB's in [−0.010, +0.010])

### 2.1 The decomposition

Offset is a Jaccard, higher is better. For each fold:

- **(a) α choice:** N_EB's own choice rule (`harness.eb_choose`, unrestricted candidates) at the α
  the rule's source side chose, minus N_EB.
- **(b) library restriction:** the rule's source side with library-only candidates, minus (a)'s
  predictor.
- **(c) side switch:** the full rule, minus its source side alone.
- (a) + (b) + (c) = rule − N_EB exactly.

| | registered GB0 (seed 60000) | 100 diagnostic GB0 draws: mean (SD across banks) |
|---|---|---|
| **rule − N_EB** | **−0.01996** | **−0.0328** (0.0196); min −0.0812, max −0.0018 |
| (a) α choice | +0.00195 | +0.0003 (0.0009) |
| **(b) library restriction** | **−0.01866** | **−0.0291** (0.0182) |
| **(c) side switch** | **−0.00325** | **−0.0039** (0.0045) |
| held-out sets that are in the library | 86.6 % | 83.1 % |
| held-out cells that take the target side | 3.6 % | 2.5 % |
| G-o0 pass rate | fail | **0.10** |

Sources: `registered_GB0`, `GB0_diagnostic.G_o0`.

- **This confirms the earlier diagnostic's "about −0.019 and −0.003".** Precisely: −0.0187 from the
  library and −0.0032 from the switch, partly offset by +0.0019 from the α choice.
  `gate_diagnostics.json` had folded that α term into its "unrestricted" line (0.8595 against
  N_EB's 0.8575).
- The registered draw was milder than typical: 67 % of the draws do worse
  (`registered_GB0_within_diagnostic`).

### 2.2 The library cap: what size would work, and does DL still fit?

Each cap was re-run with `fit.fit_offsets`, with the caps patched inside the diagnosis process
only. "DL at fit" is the largest DL measured over all folds and draws. It uses the registered
layout: A and B move to a 6-bit array `AB__sym64` above 32 sets, and the decoder is taken at its
measured 494 bytes. The one-tenth limit is **9,481.2** bits. Today's worst case at the registered
caps is **8,527**.

| library cap (sets / bits / offsets) | G-o0 pass rate | rule − N_EB mean | worst draw | largest library seen (sets, offsets) | DL at fit (max) | registered GB0: rule − N_EB |
|---|---|---|---|---|---|---|
| **32 / 800 / 48 (registered)** | **0.10** | −0.0328 | −0.0812 | 32, 38 | 8,477 | −0.0200 |
| none / 1,000 / none | 0.42 | −0.0163 | −0.0617 | 50, 47 | 8,889 | −0.0035 |
| none / 1,200 / none | 0.74 | −0.0079 | −0.0391 | 56, 48 | 9,121 | +0.0013 |
| **none / 1,400 / none** | **0.90** | **−0.0037** | −0.0170 | **62, 49** | **9,352** | +0.0013 |
| none / 1,600 / none | 0.97 | −0.0023 | −0.0154 | 69, 50 | **9,628 (over)** | +0.0013 |
| 32 / none / none | 0.45 | −0.0117 | −0.0369 | 32, 50 (1,680 bits) | 9,417 | −0.0026 |
| none / none / none | 0.98 | −0.0012 | −0.0154 | 106, 62 | 12,353 (over) | −0.0001 |

Sources: `GB0_diagnostic.caps`, `registered_GB0.caps`.

- **On the registered GB0, about 1,000 bits would have passed.** At 1,000 bits the loss is
  −0.0035 with 34 sets. With 32 sets and no bit cap it is −0.0026, at 1,062 bits.
- **Passing reliably on fresh draws needs about 1,400 bits and about 64 sets**: 90 % of draws pass,
  with a mean of −0.0037. The set cap binds as well as the bit cap. With 32 sets and no bit cap,
  only 45 % pass.
- **DL still fits, but barely.** The worst case at caps of 64 sets, 1,400 bits and 64 offsets is
  **9,427** bits (`dl_worst_case_at_caps`). That is 900 more than today, and 54 bits under the
  limit, before the decoder grows to read the 6-bit index array. That growth was not measured.
  Seven more compressed bytes would break the limit. At 1,600 bits the worst case, 9,627, is over.
  With 32 sets and 1,400 bits the worst case is 9,127, but that library passes only about 45 %.
- **Even an unlimited library leaves the side switch.** Mean −0.0012, and 2 of 100 draws land
  outside the band (worst −0.0154).

### 2.3 Is ±0.010 a sensible band? (`GB0_diagnostic.N_EB_noise`)

- **N_EB's own level varies a lot between draws:** its 10-fold mean Jaccard is 0.8507, with an SD of
  **0.0131** across the 100 GB0 banks. But G-o0 is **paired**: the rule and N_EB are scored on the
  same bank and the same folds. So this spread does not enter the gate.
- **The paired noise is small.** An N_EB-equivalent predictor, which differs from N_EB only by an
  α chosen on other inner folds, shows:
  - rule-free difference from N_EB: mean +0.0003, **SD 0.00085** across banks;
  - largest |difference| 0.0035;
  - **inside ±0.010 on 100 of 100 banks**;
  - per-fold SD 0.0015.
- So ±0.010 is about **12 SD** of the noise the gate can see. The band is wide, not tight. A rule
  that did as well as N_EB would pass. The rule fails because its offset choices are worse: its
  per-fold SD against N_EB is 0.0172, and its mean is −0.033.

### 2.4 Verdict on G-o0

**The fault is in the weight.**

- The registered library (≤ 32 sets, ≤ 800 bits, ≤ 48 offsets) cannot hold the per-source offset
  sets that N_EB is free to choose. That costs −0.029 on average, and the side switch adds −0.004.
- The band is not the problem: an N_EB-equivalent predictor never leaves it.
- The proposal's §7 named the library cap as a risk ("the library cap alone can cost Jaccard on
  sources with unusual but consistent sets"). The gate measured it.
- **Caveat.** GB0's offset structure (each source copies one real cell's set in 80 % of its cells)
  was fixed by the registration. How much the library costs on the real bank is unknown. This
  diagnosis did not, and must not, measure it.

## 3. The gates that passed, and how the thresholds were chosen

**G-e0** (GB0: rule − BF_1 existence margin ≤ +0.002) passed at −0.00212.

- The criterion is one-sided, so a rule that is *worse* than BF_1 passes.
- On GB0 the registered rule is worse by −0.00212. Most of that is quantisation: the float model
  gives −0.00072 (`registered_GB0.G_e0_float_minus_BF1_margin`).
- Across 100 draws the pass rate is 100 %, with a mean of −0.0012 and a maximum of +0.0006. The
  registered −0.00212 is in the bottom 9 %.
- The gate does what it says, and X_e finds nothing where nothing is planted. But its threshold was
  never close to binding, so the pass says nothing about calibration.

**G-o+** (GB1: rule's offset Jaccard beats N_EB's in ≥ 9 of 10 folds) passed 10 of 10, at 0.6990
against 0.5722.

- The planted target effect is large: half the types are target-driven, and 80 % of their cells
  copy the target's set. The rule's mean Jaccard lead is +0.120 across the draws.
- Yet the same count criterion fails on **9 of 100** diagnostic draws at × 1: the fewest wins seen
  was 5 (`power_GB1_diagnostic.Wstar_x1.G_o_plus`).
- So the "9 of 10" count has the same weakness here. Its registered pass was helped by a strong
  planted effect.

**How the thresholds were set** (proposal §2.5 and §3):

- §2.5 lists the criteria and the planted values (W\*, the 0.5 target share, the 0.2 noise) with
  "fixed now", and gives **no reason for any threshold**.
- §3's last bullet covers all of the proposal's constants: they "come from the A5 arithmetic in §2.4
  or are stated conventions. None was tuned on data."
- By provenance:
  - "9 of 10" is C6 P1's fold-win count.
  - "+0.002" is the P4 tie band of §1.
  - "±0.010" has no stated source.
- **No power calculation, noise measurement or reference-model run was made before registration.**
  The thresholds are conventions and were not calibrated. The margins of the two passed gates are
  consistent with that: one could not fail for a weak rule, and the other passed on a large planted
  effect.

## 4. Conclusions

| gate | scales fault | weight fault |
|---|---|---|
| G-e+ | **Yes, main.** The count fails a W\*-knowing model 7 % of the time, and the registered bank is a 1st-percentile draw. | Minor. The rule reaches about 92 % of the reference advantage, and the λ grid often switches the bilinear term off. |
| G-o0 | **No.** Paired noise has SD 0.00085 against a ±0.010 band. | **Yes, main.** The library cap costs −0.029 and the side switch −0.004. |

## 5. Candidate fixes (none applied)

Every fix changes either §2.5 (the gates) or §2.3/§2.4 (the rule) of a **registered** proposal. So
every fix needs a **new registration**, and the re-gate must use banks from the reserved seed range
80000–80999.

**To the scales (gate definitions):**

| id | fix | measured effect (on the diagnostic draws) | DL cost | registration |
|---|---|---|---|---|
| S1 | **G-e+ judged as P4 judges it:** fold-mean advantage over BF_1 > +0.002 (the registered tie band) | rule passes 100/100 at × 1, O-W\* 100/100; false pass on 100 GB0 draws: 0 | 0 | new |
| S2 | G-e+ at ≥ 8 of 10 folds | rule 0.99, O-W\* 0.98; null 0/100, but the null reached 7 wins | 0 | new |
| S3 | keep 9 of 10, plant W\* × 2 | rule 0.98, O-W\* 0.98 | 0 | new. It tests a larger effect than the registered one, so it answers a weaker question. |
| S4 | the same change to G-o+ (fold mean, or ≥ 8 of 10) | the 9-of-10 count failed 9/100 draws at × 1 (not re-measured under S4) | 0 | new |
| S5 | G-o0 redefined as rule − its own source-side-only variant, so it measures only the side switch, which is what §2.5's sentence says it guards | the switch costs −0.0039 on average (SD 0.0045); not re-scored as a gate | 0 | new. **Not recommended alone:** the library cost would then appear at the exam's P1 offset against N_EB, where the author already expects a fail (S2-2). |
| — | widen G-o0's band to fit the rule | — | 0 | **Not recommended.** The band is already 12 paired-noise SDs wide. Widening it would hide a real loss. |

**To the weight (the rule):**

| id | fix | measured effect on G-o0 | DL cost (worst case at caps) | registration |
|---|---|---|---|---|
| W1 | library caps **64 sets / 1,400 bits / 64 offsets**; A and B become 6-bit symbols | pass 0.90, mean −0.0037, worst −0.0170 | **9,427** (+900; 54 bits under the limit, before the decoder's growth, which was not measured) | new |
| W2 | caps 64 / 1,200 / 64 | pass 0.74, mean −0.0079 | 9,227 (+700) | new |
| W3 | W1 paid for elsewhere, e.g. e and f as 2-bit levels (−130 bits) | not measured | about 9,297 | new |
| W4 | a stricter side switch (e.g. the target side only if f_t ≥ e_s + 2) | not measured. The switch's whole cost is −0.0039 today and −0.0012 with an unlimited library. G-o+'s gain may shrink. | 0 data bits; a few decoder bytes (not measured) | new |
| W5 | a finer λ grid for the bilinear term (e.g. 0.3 to 5), since λ ≥ 10 means "off" | not measured; the ceiling is O-W\*'s +0.0013 over the rule | 0 | new. It also changes BF_1-likeness, so G-bf would need rewording. |

**What I would recommend asking Mike to decide**, if a second registration is wanted:

- **S1 for G-e+.** It aligns the gate with P4, has full power here and has no false passes on the
  null.
- **W1 for G-o0.** It is the only measured option above 90 % that still fits DL.
- **Both need a fresh set of gate banks from 80000–80999.**
- **Before W1 is registered, its decoder must be written and its size measured.** At 54 bits of
  headroom, the decoder's growth decides whether W1 fits at all.
