# Power curves of block A and the male CNS arm: a weaker instrument, or a different draw? (Q2)

**Written:** 2026-09-27 UTC by a CC subagent, for CC to review. **This is a diagnostic note,
written outside any registration. It decides nothing, changes no label and amends no
registration.** Nothing was fitted and nothing ran on the GPU. No sealed file was opened. Every
number below was read from committed or pinned files, or computed from them by the exact tests
named in §3 and §4. The scratch scripts are in the session scratchpad and not in the repository.

**The question (Q2; Ark and Zcode, DPC Research chat, 2026-09-27 13:24–13:28 UTC).** The male
arm's registered caution (arm §5, G row, and revision 1.3's "instrument weaker" line) calls the
instrument on the male banks weaker than A's, citing γ\*_P = 0.75 against A's 0.6. Ark and Zcode
object on three points:

- the deficit is one world of five per γ;
- that lies within the ±1 grid step that the binomial note assigns to a limit at n = 5;
- the two curves come from different draws of worlds.

Q2 asks what the per-γ power curves can and cannot separate.

## 0. Answer in brief

1. **The counts do not separate "weaker instrument" from "different draw".** No test on seen/n
   or R/n reaches p ≤ 0.05 two-sided, per γ or pooled over γ, for A against either lobe (§3). The
   difference that moves γ\*_P is 3/5 against 2/5 at γ = 0.6. Its Fisher p is 1.0.
2. **The tests have almost no power at n = 5.** At one γ, a one-sided Fisher test at 0.05
   rejects only 5/5 v ≤ 1/5 or 4/5 v 0/5. Suppose the male curve sat a full grid step to the
   right of A's. Pooled over the five γ, the stratified exact test would then miss that shift
   about 38 % of the time (§3.3).
3. **The per-world AUCs carry weak evidence of a difference at γ 0.75–0.85, but the evidence is
   not established.**
   - At those γ the male worlds give lower rule #2.1 and BF_1 AUCs than A's worlds. At γ = 0.5
     they give higher ones (§4). Stratified exact rank tests give two-sided p between 0.045 and
     0.19.
   - The tests are uncorrected, several were run, and the test set was chosen after the data
     were seen.
   - L and R share their world seeds, so lobe R does not replicate lobe L. It is one draw seen
     through two banks.
4. **Even a real bank effect could not be called "the instrument" rather than "the units of
   γ".**
   - Leg P turns seen/unseen at nearly the same AUC on all three banks: about 0.67.
   - What differs is the AUC that a given γ produces on a bank. That depends on the world
     generator's degree terms, its grid (49 against 39 other types), its density and its content
     (§5).
   - The male arm's own §3.6 says that limits in M-world units "are not compared with A's or
     with each other as numbers".
5. **No existing file pairs A's worlds with the male worlds (§5.2).** They share no seed, and
   even equal seed numbers would not align the random streams. The two male lobes *are* paired
   (common seeds, the same boards). That pairing shows what a paired design buys: the per-world
   AUCs of L and R correlate at 0.915 within γ.

## 1. Sources and definitions

**Files** (all read-only):

| role | file | integrity |
|---|---|---|
| A, worlds | `results/genome/c6/checks/knockout_regrow/synthetic_worlds.csv` (270 rows, 45 worlds × 6 predictors) | equal to the pinned pre-run `connectome-seed-data/knockout_regrow/synthetic_rev3_prerun/synthetic_worlds.csv` (sha256 `7a2f0295…`, = `A_PRERUN_SHA256`, `knockout_regrow_male_cns.py:128`) on every column but `mechanism_description`, which differs in text only on 84 rows (Nf 30, No 30, M0.5 24: revision 3.2's rename, "ceiling_full" → "rule #2.1's ceiling_full") |
| male L, worlds | `results/genome/c6/checks/knockout_regrow_male_cns/synthetic_worlds_L.csv` | raw sha256 `50657631…` = `PRERUN_WORLDS_CSV_SHA256["L"]` (script line 110) = the pinned reference |
| male R, worlds | `…/synthetic_worlds_R.csv` | raw sha256 `e8476a93…` = `PRERUN_WORLDS_CSV_SHA256["R"]` = the pinned reference |
| A registration | `docs/plans/2026-09-24-knockout-regrow-registration.md` §3.6 (power-curve table, the three limits, the binomial note) | — |
| male registration | `docs/plans/2026-09-26-knockout-regrow-male-cns-arm-registration.md` §3.3.1 (d), §3.6, §3.7, §5, §6 | — |
| real-block values (context only) | `results/genome/c6/checks/knockout_regrow/RESULT.md` line 5; `…/knockout_regrow_male_cns/RESULT.md` lines 15, 46 | — |

**How the scripts compute "seen" and "R".** Located with the Orbit code graph (callers of
`make_world`, `world_specs`, `detection_limits`) and confirmed by grep. The two scripts are
identical here.

- **`p_P`** (leg P). For one world and one predictor, `p_P = (1 + #{permutations with null AUC
  ≥ AUC − TAU}) / 10,000` over 9,999 uniform within-block permutations
  (`knockout_regrow_male_cns.py:1590`; A `knockout_regrow.py:1069`).
- **Seen.** `seen[pk] = sum(p_P <= P_R)` with `P_R = 0.01`, per predictor, over the worlds at one
  γ (`detection_limits`, male `:2337`, A `:1750`). "Seen" without a predictor means rule #2.1.
- **R.** `n_r = sum(label == "R")` (male `:2338`, A `:1751`). A label is R only when both D1
  candidates read R (`read_label`, male `:1688–1730`, A `:1151–1185`). A candidate reads R when
  its leg S passes and its `p_P` is at most 0.01 (`reading_on`, male `:1633–1641`, A
  `:1105–1113`). Leg S passes when `n_ge = 0` of at least one valid shuffle. I rebuilt "label R ⇔
  the R letter on rule #2.1 and on BF_1" from the CSV columns `n_ge`, `n_valid_shuffles` and
  `p_P`. It holds for all 135 worlds.
- **The dense grid.** `DENSE_GRID` = γ ∈ {0.5, 0.6, 0.75, 0.85, 1.0}, families M0.5 … M1.0 with 5
  worlds each (male `:366`, A `:265`). The anchors Nf (γ = 0) and R (γ = 2.0) enter no limit.
- **The limit.** A limit is the smallest grid γ at which a majority (≥ 3 of 5) is seen or reads R
  (`grid_limit`, male `:2243–2262`).

**CSV columns used:** `family`, `seed`, `predictor`, `label`, `auc`, `p_P`, `n_ge`,
`n_valid_shuffles`, `lambda_ko`, `outside_density`.

## 2. The per-γ power curves

### 2.1 The quoted numbers, verified

Rule #2.1's seen/5 and label R/5, from each CSV's `rule #2.1` rows. These equal the quoted
figures, the A registration's §3.6 table, the arm's §3.3.1 (d) and §5 tables, and the script's
`A_CURVE_TEXT` (`knockout_regrow_male_cns.py:3291`):

| γ | A: seen, R | male L: seen, R | male R: seen, R |
|---|---|---|---|
| 0.5 | 1/5, 1/5 | 0/5, 0/5 | 1/5, 1/5 |
| 0.6 | 3/5, 2/5 | 2/5, 1/5 | 2/5, 2/5 |
| 0.75 | 5/5, 5/5 | 5/5, 4/5 | 5/5, 3/5 |
| 0.85 | 5/5, 5/5 | 4/5, 3/5 | 4/5, 4/5 |
| 1.0 | 5/5, 5/5 | 5/5, 5/5 | 5/5, 5/5 |

**All quoted numbers are confirmed.** One precision on Ark's and Zcode's "one world of five per
γ":

- It holds for rule #2.1's seen/n: the male count is at most one below A's at every γ.
- It does not hold for R/n. At one γ each lobe is two below A: L at 0.85 (3/5 against 5/5) and R
  at 0.75 (3/5 against 5/5).

### 2.2 Every predictor, both D1 candidates, the labels

Seen/5 for each predictor (column `p_P` ≤ 0.01). Then the R letter of each D1 candidate
(`n_ge` = 0 and `p_P` ≤ 0.01), label R/5, and the label counts R/W/G/U:

| γ | bank | seen: rule #2.1 / BF_1 / BF_2 / BF_3 / BF_4 | R letter: rule #2.1, BF_1 | label R | R/W/G/U | seeds |
|---|---|---|---|---|---|---|
| 0 (Nf) | A / L / R | 0/0/0/0/0 in all three | 0, 0 | 0/5 | 0/0/5/0 | 90110–14 / 92110–14 |
| 0.5 | A | 1/1/0/0/0 | 1, 1 | 1/5 | 1/0/4/0 | 90140–44 |
| | L | 0/2/0/0/0 | 0, 2 | 0/5 | 0/0/2/3 | 92140–44 |
| | R | 1/1/1/0/0 | 1, 1 | 1/5 | 1/0/2/2 | 92140–44 |
| 0.6 | A | 3/3/1/1/0 | 2, 3 | 2/5 | 2/0/0/3 | 90160–64 |
| | L | 2/2/1/1/1 | 2, 2 | 1/5 | 1/0/1/3 | 92160–64 |
| | R | 2/2/1/1/1 | 2, 2 | 2/5 | 2/0/2/1 | 92160–64 |
| 0.75 | A | 5/5/5/5/5 | 5, 5 | 5/5 | 5/0/0/0 | 90170–74 |
| | L | 5/4/4/3/3 | 5, 4 | 4/5 | 4/0/0/1 | 92170–74 |
| | R | 5/3/4/3/4 | 5, 3 | 3/5 | 3/0/0/2 | 92170–74 |
| 0.85 | A | 5/5/5/5/5 | 5, 5 | 5/5 | 5/0/0/0 | 90180–84 |
| | L | 4/4/4/4/4 | 3, 3 | 3/5 | 3/1/1/0 | 92180–84 |
| | R | 4/4/4/4/4 | 4, 4 | 4/5 | 4/0/1/0 | 92180–84 |
| 1.0 | A / L / R | 5/5/5/5/5 in all three | 5, 5 | 5/5 | 5/0/0/0 | 90150–54 / 92150–54 |
| 2.0 (R) | A / L / R | 5/5/5/5/5 in all three | 5, 5 | 5/5 | 5/0/0/0 | 90100–04 / 92100–04 |

## 3. Exact tests on the counts

### 3.1 Per γ

**Method.** Fisher's exact test on the 2 × 2 table (bank × seen), 5 worlds against 5. Every
two-sided p is **≥ 0.444**, and every one-sided p (A higher) is **≥ 0.222**, for every quantity
of §2.2 against either lobe:

- A 1-world difference (5 v 4, 3 v 2, 1 v 0) gives two-sided p = 1.000 and one-sided p = 0.500.
- A 2-world difference (5 v 3) gives two-sided p = 0.444 and one-sided p = 0.222.

### 3.2 Pooled over the dense grid

**Method.** The stratified exact test: the conditional distribution of A's total over the five
γ, given each γ's margins. This is the exact form of the Cochran–Mantel–Haenszel test, computed
by convolving the five hypergeometric laws.

| quantity (over 25 worlds) | A vs L: A, L; p one-sided / two-sided | A vs R: A, R; p one-sided / two-sided |
|---|---|---|
| rule #2.1 seen | 19, 16; 0.178 / 0.355 | 19, 17; 0.335 / 0.669 |
| BF_1 seen | 19, 17; 0.353 / 0.706 | 19, 15; 0.131 / 0.263 |
| BF_2 seen | 16, 14; 0.306 / 0.611 | 16, 15; 0.500 / 1.000 |
| BF_3 seen | 16, 13; 0.173 / 0.346 | 16, 13; 0.173 / 0.346 |
| BF_4 seen | 15, 13; 0.306 / 0.611 | 15, 14; 0.500 / 1.000 |
| R letter, rule #2.1 | 18, 15; 0.193 / 0.386 | 18, 17; 0.500 / 1.000 |
| R letter, BF_1 | 19, 16; 0.236 / 0.473 | 19, 15; 0.131 / 0.263 |
| label R | 18, 13; **0.049** / 0.097 | 18, 15; 0.227 / 0.454 |

**One nominal p ≤ 0.05 among 16 pooled tests.** It is one-sided, for label R, A against L. It
does not survive any correction for the 16 tests, and its two-sided p is 0.097.

### 3.3 What these tests can detect with 5 worlds per γ

- **One γ.** At one-sided α = 0.05, Fisher's test rejects only the tables (A, male) = (5, 0),
  (5, 1) and (4, 0).
  - If A always detects (p_A = 1), 80 % power needs p_M ≤ 0.16: a difference in detection
    probability of **at least 0.84**.
  - A true difference of 0.2 (1.0 against 0.8) is detected with probability 0.007. A difference
    of 0.4 is detected with probability 0.087.
- **Pooled over the grid.** Simulated with 20,000 replicates, taking A's observed fractions (0.2,
  0.6, 1, 1, 1) as its true curve (a plug-in; the true curve is not known). The power of the
  stratified exact test at one-sided 0.05:

| male true curve | power |
|---|---|
| equal to A's (the test's actual size) | 0.018 |
| L's observed fractions (0, 0.4, 1, 0.8, 1) | 0.235 |
| A's curve moved one grid step right (0, 0.2, 0.6, 1, 1) | 0.617 |
| A's curve minus 0.2 at every γ | 0.509 |
| A's curve minus 0.4 at every γ | 0.940 |
| two grid steps right (0, 0, 0.2, 0.6, 1) | 0.999 |

So a true shift of one full grid step, the size that separates γ\*_P = 0.6 from 0.75, would pass
unnoticed about 38 % of the time. A deficit the size of the observed one would pass unnoticed
about 77 % of the time.

## 4. The per-world continuous quantities

Seen/n throws away the distance from the threshold. The CSV keeps each world's AUC and `p_P`.

**Rule #2.1, per world** (columns `auc`, `p_P`; worlds in seed order):

| γ | A: AUC (p_P) | male L: AUC (p_P) | male R: AUC (p_P) |
|---|---|---|---|
| 0.5 | 0.735 (0.0004), 0.500 (0.50), 0.531 (0.34), 0.528 (0.36), 0.490 (0.55) | 0.517 (0.42), 0.641 (0.028), 0.657 (0.015), 0.514 (0.43), 0.652 (0.019) | 0.521 (0.40), 0.634 (0.033), 0.672 (0.0077), 0.514 (0.43), 0.664 (0.012) |
| 0.6 | 0.745 (0.0002), 0.565 (0.19), 0.730 (0.0008), 0.673 (0.0082), 0.636 (0.031) | 0.567 (0.18), 0.644 (0.024), 0.740 (0.0003), 0.657 (0.014), 0.670 (0.0090) | 0.582 (0.13), 0.591 (0.11), 0.742 (0.0003), 0.642 (0.024), 0.676 (0.0065) |
| 0.75 | 0.871, 0.876, 0.786, 0.725, 0.740 (all ≤ 0.0010) | 0.820, 0.691, 0.728, 0.680, 0.718 (0.0001–0.0063) | 0.758, 0.668, 0.689, 0.681, 0.696 (0.0004–0.0094) |
| 0.85 | 0.952, 0.776, 0.843, 0.840, 0.812 (all ≤ 0.0002) | 0.898, 0.746, 0.819, 0.702, **0.525 (0.37)** | 0.903, 0.771, 0.731, 0.725, **0.542 (0.29)** |
| 1.0 | 0.970, 0.954, 0.855, 0.974, 0.759 (all 0.0001) | 0.942, 0.970, 0.839, 0.949, 0.792 (all 0.0001) | 0.922, 0.945, 0.833, 0.934, 0.890 (all 0.0001) |

**Mean rule #2.1 AUC per γ:**

| bank | 0.5 | 0.6 | 0.75 | 0.85 | 1.0 |
|---|---|---|---|---|---|
| A | 0.557 | 0.670 | 0.800 | 0.844 | 0.902 |
| L | 0.596 | 0.656 | 0.728 | 0.738 | 0.898 |
| R | 0.601 | 0.647 | 0.699 | 0.734 | 0.905 |

Seed 92184 is the world that reads G at 0.85 in both lobes. Without it, the male means at 0.85
are 0.791 (L) and 0.783 (R), still below A's 0.844. The within-γ standard deviation of AUC
between worlds is 0.066–0.101 in A and 0.035–0.14 in the male lobes.

**Stratified exact rank tests.**

- **Method.** Midranks within each γ, with A's rank sums added over the five γ. The null
  distribution is exact: all 252 splits per γ, convolved over γ. The "A higher" direction is the
  one the "instrument weaker" claim predicts. A's lowest `p_P` counts as higher.
- **Results:**

| quantity | A vs L: p one-sided / two-sided | A vs R: p one-sided / two-sided |
|---|---|---|
| rule #2.1 AUC | 0.071 / 0.142 | **0.031** / 0.061 |
| rule #2.1 `p_P` | 0.093 / 0.187 | **0.023** / **0.045** |
| BF_1 AUC | **0.032** / 0.064 | **0.025** / **0.049** |
| BF_1 `p_P` | **0.031** / 0.062 | **0.031** / 0.062 |

**What this shows.**

- **The difference is not a shift of the whole curve.**
  - At γ = 0.5, three of five male worlds in each lobe have AUC 0.63–0.67, just short of or at
    the threshold. Four of A's five are at 0.49–0.53, and one is at 0.735 (seed 90140, A's only
    world seen at 0.5).
  - At 0.6 the banks overlap fully.
  - At 0.75 and 0.85 A is higher. At 0.75, 4 of lobe R's 5 AUCs lie below A's lowest (0.725);
    lobe L overlaps more (0.680–0.820 against 0.725–0.876).
  - At 1.0 the banks overlap again.
  - The male curve looks flatter than A's, not simply shifted. With 5 worlds per γ, that is not
    established either.
- **The per-γ tests at 0.75 separate A from R only.** For rule #2.1 the exact
  Mann–Whitney two-sided p is 0.032 on AUC and 0.016 on `p_P`. Against L they give 0.095 and
  0.103.
- **These p-values count for less than they look, for three reasons.**
  1. Eight pooled rank tests were run here, beside the 16 pooled count tests. None was
     registered, and the set was chosen after the data were seen.
  2. The A-vs-L and A-vs-R tests are not two replications. L and R are the same 25 draws seen
     through two nearly identical banks (§5.2), so their agreement is mostly the shared draw.
  3. With 5 worlds per γ and a between-world sd of about 0.07, the stratified rank test has
     one-sided 0.05 power of about 0.57 against a uniform AUC shift of 0.04, and about 0.87
     against 0.06 (simulation, normal approximation, 5,000 replicates). At a single γ, the
     exact 5 v 5 test has power 0.47 against a shift of 0.08 and 0.76 against 0.12.
- **Conclusion on the continuous data.** They are weak evidence, not established, that on the
  male banks the M worlds at γ 0.75–0.85 give lower AUCs than A's worlds. They carry more
  information than seen/n. They do not say why.

**Leg P's threshold, in AUC, is nearly the same on the three banks.**

- For a tie-free prediction on board `z`, `smallest_passing_auc` is 0.666015625 (682/1024) in A
  (A registration §3.3, line 832) and 0.671875 (688/1024) in both male lobes (arm §3.3.1, table
  in (c)). The difference is 6/1024, a property of the different permutation draws (seed 90000
  against 92000).
- In the worlds, the highest unseen AUC and the lowest seen AUC are:
  - A: 0.636 (90164) and 0.673 (90163);
  - L: 0.657 (92142) and 0.670 (92164);
  - R: 0.664 (92144) and 0.668 (92171).
- So the curves do not differ in how an AUC becomes "seen". They differ, if at all, in how much
  AUC a γ yields on a bank.

## 5. What makes the draws differ, and whether anything pairs them

### 5.1 A against male

| element | A (`knockout_regrow.py`) | male (`knockout_regrow_male_cns.py`) |
|---|---|---|
| world seeds | `SEED_WORLD` 90100 + 10 i + j (`:251`, `world_specs` `:659–662`); dense grid 90140–44 (M0.5), 90150–54 (M1.0), 90160–84 (M0.6–M0.85) | 92100 + 10 i + j (`:348`, `:1083–1086`); 92140–44, 92150–54, 92160–84 |
| random stream per world | `default_rng(seed)`: z for **49** others, z1 for 49, u (65 × 65), content indices into **572** cells (`make_world` `:701–728`) | the same order, but z and z1 for **39** placed others, and indices into the lobe's pool of **496 / 526** cells (`:1142–1172`) |
| grid | 65 types, every cell may exist | 55 placed types. Every cell with an unplaced endpoint is absent (asserted) |
| degree terms (c, a, b) | N1 fitted on flyvis-65's knockout view (`degree_terms` `:694–698`) | N1 fitted on the lobe's knockout view on the placed grid (`:1134–1139`) |
| outside density of the worlds | Nf mean 0.1365 (column `outside_density`: 0.1242–0.1425); M1.0 0.1634–0.1716 | L: Nf 0.1662–0.1749, M1.0 0.1888–0.2030. R: Nf 0.1746–0.1841, M1.0 0.2013–0.2145 |
| content | flyvis content with real offsets and signs | existence rows (the lobe's outside cells) |
| leg-P null | 9,999 permutations from `default_rng(90000)` | from `default_rng(92000)` |
| permuted-block ceilings | 90010–90029 | 92010–92029 |
| shuffles; ALS starts | seeds 0..98 (`harness.shuffled_bank`); `PCG64(30000 + j)` | the same seeds, applied to different banks |
| boards | `z`, `z'` on the 16 block types, by name | the same |

**A and the male worlds are not paired, and cannot be paired by seed number alone.** The seed
sets are disjoint: the male script's `assert_seeds_unique` requires it (`:1089–1101`), and A's
seeds sit in the male script's `A_SEEDS` (`:351`). But equal seeds would not help either:

- A draws 49 z values before u, and the male script draws 39. The streams would fall out of
  step after the first draw.
- The content indices point into pools of different sizes.
- The grid of existing cells differs.

A grep of `results/**/*.py` for `SEED_WORLD`, `90100` and `92100` finds no code that builds A's
seeds on a male bank, or male seeds on flyvis-65. The Orbit graph's callers of `make_world` are
only the two `build_bank`s, `spec_of`, the tests and the older column test. The GPU instrument
(`gpu_instrument/male_arm.py`) reuses the male script's `world_specs`. **No existing file lets
one compare A's worlds with the male worlds draw for draw.**

### 5.2 Lobe L against lobe R: the one paired comparison that exists

The lobes share their world seeds (arm §3.7: "the same seeds serve both lobes (common random
numbers)"). Their 45 world pairs carry the same board (arm §3.3.1 (d)). Their two banks differ on
36 of 2,961 outside cells (`WITHIN_ANIMAL_NOTE`, script `:331`). Over the 25 dense-grid pairs:

- **Rule #2.1 AUC, L − R:** mean +0.0062, sd 0.0348, median |d| 0.0156, maximum |d| 0.0977.
  Wilcoxon signed-rank p = 0.32.
- **Correlation of L's and R's AUC:** 0.964 raw and **0.915 within γ** (each γ centred). BF_1:
  0.923 within γ.
- **Seen by rule #2.1:** discordant in 1 pair (92142, R only). Exact McNemar p = 1.
- **Label R:** L only 92172; R only 92142, 92164, 92183. p = 0.625.

**What this shows.** Once the draw (z, u, content indices) is held fixed, a small change of bank
moves a world's AUC by a few hundredths. Between the draws at one γ, AUC varies by about 0.07.
So most of the world-to-world variance lies in the draw.

This bears on Q2 in two ways:

1. A paired design would remove most of the noise that currently hides any A-against-male
   difference.
2. The two lobes' shared "deficit" against A is one draw of 25 worlds seen twice, not two
   observations.

The arm's §3.3.1 (d), surprise 1, already says so: "the two lobes are not two independent
observations (common seeds)". The L–R pairing does not transfer to A against male. The male
banks differ from flyvis-65 far more than from each other (grid, degree terms, content), so the
size of the bank effect between A and the male banks is **not established**.

## 6. Conclusion, in the registrations' language

**On "the instrument on the male banks is weaker".**

- **Per lobe, on the quantities that define the limits** (seen/n and R/n per γ), the data do not
  support a weaker instrument beyond what a different draw of five worlds per γ gives. Here is
  why:
  - γ\*_P = 0.75 against 0.6 rests on 2/5 against 3/5 at γ = 0.6 (Fisher p = 1.0).
  - No pooled count test reaches two-sided 0.05.
  - The binomial note (A §3.6: "a limit is uncertain by about one grid step") already covers the
    move.
  - The arm's own §3.3.1 (d), surprise 1, reads the move the same way: "By the binomial note …
    this is within noise for each lobe".
- **The wording of revision 1.3 says more than the counts show.** That wording is "measured to be
  weaker" (§5) and "The instrument on lobe ℓ is weaker than A's" (S31). The counts show only that
  "a weaker instrument" is not excluded, and neither is "a different draw".
- **The per-world AUCs lean the same way at γ 0.75–0.85.** Against lobe R the two-sided p is
  0.045–0.06; against lobe L it is 0.06–0.19. They lean the other way at γ 0.5. That is weak,
  uncorrected evidence and **not established**.
- **Even if the difference is real, it is not separable from "the units of γ".** The male arm's
  §3.6 says the male banks differ from A's in degree terms, grid, density and content, and that
  "a limit in 'M-world units' … moves with them". Leg P's AUC threshold is almost the same on all
  banks (§4). So a γ that yields less AUC on the male banks could be a weaker fit on the male
  banks, or a γ that is a smaller signal on those banks. Nothing in the existing files tells the
  two apart.

**On the reading of the male G against flyvis-65's G.**

- The registered caution in the §5 G row stands on its own registered grounds. It is not
  challenged by these data:
  - "power of the male R not calibrated": the male R is a conjunction of two lobes (§4.2);
  - "each lobe's limits are measured on its own instrument-bank pair".
- What the data do not support is reading that caution as *a measured power deficit per lobe*.
  Per lobe, the male power curves cannot be told from A's at n = 5.
- The data also do not support equal power. The tests would miss a full one-grid-step shift
  about 38 % of the time.
- A reading the data support: "flyvis-65 and each male lobe read G against limits at the same
  grid γ_R (0.75 on all three banks) in M-world units that are not comparable across banks. A
  per-lobe difference in power between A and the male banks is not established, and neither is
  its absence. The male G therefore does not by itself exclude averaging as the explanation of
  flyvis-65's G, as registered."
- **Context only; decides nothing.** The real blocks' rule #2.1 readings are:
  - flyvis-65: AUC 0.5327, `p_P` 0.3288 (A `RESULT.md` line 5);
  - male L: AUC 0.5020, `p_P` 0.4905 (male `RESULT.md` line 15);
  - male R: AUC 0.5127, `p_P` 0.4318 (line 46).

  Each lies inside its own bank's Nf-world range (A 0.502–0.536; L 0.479–0.533; R 0.495–0.537;
  column `auc`, family Nf). All are far from the seen boundary near AUC 0.67. The curves differ,
  if at all, between γ 0.6 and 0.85. Whether the real blocks' structure falls in that range is
  **not established**, because a real block is not a 32/32 board and there is no registered map
  from a real AUC to γ.

## 7. What would separate the two (new runs; none is proposed here)

1. **Common random numbers across banks.**
   - Draw z and z1 for the 39 other types common to both grids first, in the same order, then the
     10 types that are placed only on flyvis-65.
   - Draw u on the common 55 × 55 cells identically.
   - Build each world on both banks and compare per-world AUC and `p_P` pairwise.

   §5.2 suggests that pairing removes most of the draw variance: within-γ correlation 0.915
   between L and R. Content cannot be paired (flyvis offsets against existence rows), which
   points to the next design.
2. **A crossed design, to separate "units of γ" from "the fit on the bank".**
   - Worlds from A's degree terms on the 55-type existence grid, and from the male degree terms
     on A's setting, beside the two existing arms.
   - The factor "generator's degree terms and density" then separates from the factor "grid and
     content that the fit sees".
3. **More worlds per γ.** The binomial note's one-grid-step error shrinks only with n. At n = 20
   per γ, a one-sided Fisher test at 0.05 has 80 % power for a difference in detection
   probability of 0.32 when p_A = 1.0, 0.35 when p_A = 0.95 and 0.38 when p_A = 0.9. At n = 5
   the figure is 0.84 (§3.3). Computed exactly, like §3.3.
4. **A bank-free unit for the limits.** For example, the AUC of the planted `z_s z_t` score on
   the outside cells, or the outside's information about z, instead of the logit coefficient γ.
   This would make limits comparable across banks as numbers, which the arm's §3.6 currently
   forbids.

## 8. Not established

- That the instrument on the male banks is weaker than A's, per lobe, in seen/n or R/n.
- That it is *not* weaker: the tests' power is too low to support equal power.
- Whether the lower male AUCs at γ 0.75–0.85 (§4) are a bank effect or a draw. Their p-values
  are uncorrected and post hoc, and the two lobes share one draw.
- If there is a bank effect: whether it comes from the fit on the male banks or from the meaning
  of γ on the male degree terms, grid and density.
- The shape of the male curve (flatter than A's, or shifted). At γ = 0.5 the male AUCs are
  higher and at γ 0.75–0.85 lower, with 5 worlds per γ.
- The male R conjunction's power, which the arm registers as uncalibrated (§4.2, §6). This note
  measures per-lobe curves only.
- Where the real blocks lie in γ (§6, last item).
