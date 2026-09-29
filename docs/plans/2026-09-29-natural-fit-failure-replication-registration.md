---
**Status: draft rev 1, text only, not reviewed.** Drafted 2026-09-29 UTC by a CC subagent on Mike's
choice of option A (DPC Research chat, 2026-09-29): a replication registration of the natural fit
failure seen on the permuted boards of the failed-fit calibration. Nothing was run, fitted or
committed by the drafting agent. The only reads of data were the calibration's committed outputs
(and the `secs` timing field of its raw fits, for the compute estimate, §9); every recount in §1 was
done from `permuted_reference.csv` and `bf_block.csv`.
---

# Registration: replicating the natural fit failure of rule #2.1 on fresh permuted boards

**This registration is NOT blind (Ark).** The 99 permuted boards of the failed-fit calibration
(seeds 93200–93298) and every number in §1 were seen, by the reviewers and by the drafting agent,
before this text was written. Nothing seen is re-read as evidence here. **What is registered is a
replication on FRESH boards** (§4): the same construction, new seeds, predictions written and
committed before the run (§6).

"CAL" is `docs/plans/2026-09-29-failed-fit-branch-calibration-registration.md` (rev 1.9, the pinned
registration of the run from `255a03d`); "CAL-OUT" is
`results/genome/c6/checks/failed_fit_calibration/`; "the CAL script" is
`results/genome/c6/checks/failed_fit_calibration.py` (line numbers at HEAD `5d65baf`; that commit
changed reporting and tests only, not the fits or the board construction); "the B script" is
`results/genome/c6/checks/knockout_regrow_block_b.py`. None of these is edited by this file.

## 0. What the question is, in plain words

The calibration built 99 boards by shuffling the 40 block labels of board z at random (CAL §10,
CAL:1116–1127). Every one of them is a pattern the model class can hold: the capacity certificate
`cert` is ≥ 0.975 on all 99 (§1). Yet on about half of them rule #2.1's registered block-only fit
fell below the gate 0.90. In each such case the nested λ choice picked λ = 100, where the rule's
interaction term collapses, while the same path forced to λ = 1 passes. By the definitions of CAL §3
(CAL:497–505) that is **FF-sel**: a failure of the λ selection, not of the class and not of the
optimiser.

These boards were a printed reference that decided nothing (CAL:1116–1124). The replication asks
whether this is a stable property of the registered fitter on such boards, or an accident of those
99 seeds:
- how often it happens (the rate);
- whether it is always FF-sel;
- whether the rarer kind seen once (board j = 89, below) comes back;
- whether the BF family collapses with it;
- whether the chosen λ marks the failure.

## 1. What was seen (post-data; recomputed from CAL-OUT by the drafting agent)

All counts come from `permuted_reference.csv` (header at line 1, board j at line j + 2) and
`bf_block.csv`. The sub-kind is read by hand with CAL §6's table (CAL:886–893), since the CAL script
does not print a separator row for permuted boards (§8, item 1).

| claim relayed in the chat | recomputed | matches? |
|---|---|---|
| 99 boards, seeds 93200–93298 | 99 rows, seeds 93200 (line 2) to 93298 (line 100) | yes |
| `ceiling_block` < 0.90 on 53 of 99 | 53 of 99 (also CAL-OUT `CALIBRATION.md`:54); the `_tau` value agrees on every board, so no `GATE_ULP_SPLIT` | yes |
| `cert` ≥ 0.90 on all 99, min 0.975 | 99 of 99, min 0.975 (board j = 57, line 59; `CALIBRATION.md`:54; BLIND_REVIEW.md:91) | yes |
| 52 of the 53 are FF-sel (λ_c = 100, `ceil_1` ≥ 0.90) (Ark 10:39:27, Zcode 10:44:08 UTC) | 52 of 53. **One of the 52 sits exactly at the cut:** j = 57, `ceil_1` = 0.900000 (line 59), FF-sel only by "≥" | yes, with the at-the-cut note |
| one borderline: j = 89, seed 93289, `ceil_1` 0.895, `cert` 0.9875 | line 91: `ceiling_block` 0.730, λ_c 100, `ceil_1` 0.895 (exact = `_tau`), `ceil_1_float` 0.895, `ceil_λc_float` 0.730, `cert` 0.9875 (exact = `_tau`), cert rerun spread 5 pairs. By CAL §6 it reads **"fit failure, FF-struct or FF-opt, not separated"** unless `ceil_1_starts100` ≥ 0.90; that value is not in any CSV (§8, item 1). All four BF_r read 0.725 there | yes |
| λ = 100 chosen on all 53 failures | 53 of 53 | yes |
| λ = 1 chosen on all 43 passes | **there are 46 passes, not 43.** 43 chose λ = 1; **3 passed at λ = 100**: j = 15 (0.9275, line 17), j = 49 (0.915, line 51), j = 76 (0.915, line 78). λ took only the values 1 and 100 (56 × 100, 43 × 1; BLIND_REVIEW.md:101–102) | **no: 43 of 46** |
| BF collapse on the 53: `bf1` ≥ 0.90 on 3, `bf2` 11, `bf3` 9, `bf4` 9 (Zcode) | 3, 11, 9, 9 of 53. On the 46 passes: 46, 40, 40, 40. Over all 99, BF_r < 0.90 on 50, 48, 50, 50. 39 of the 53 failures have every BF_r < 0.90 | yes |
| Ark: λ = 100 marks failure, "52 of 56" | of the 56 boards with λ_c = 100, **53** fail and 3 pass (above). 52 of 56 is the FF-sel count among them | the count is 53 of 56; 52 counts FF-sel only |

**Two further facts seen, recorded so that no later text reads them as new:**
- **Board j = 49 passes the gate through the decoder** (line 51): at λ_c = 100 the float fit gives
  0.895 < 0.90 ≤ 0.915, the quantised registered value. This is the pattern of CAL's board 41
  (CAL:743–748), now seen on a permuted board: the gate's verdict depends on the 5-bit decoder.
- **Ulp sensitivity** occurs only in `ceil_λc_float`, on 4 boards (j = 17, 46, 57, 94), and never
  crosses 0.90. Every `ceiling_block`, `ceil_1`, `ceil_1_float` and `cert` is equal exact and under
  `TAU`.
- Every permuted board has 20 of 40 present (the permutation keeps the count), but the rows are
  not 4 per row, so CAL §2a's floor does not apply to them (CAL:1121–1123).

## 2. Object and decision rule

**Object.** A permuted 40-cell block pattern, built exactly as CAL §10 builds it:
`default_rng(seed).permutation(40)` applied to board z's 40 labels (`perm_ref_y`, CAL script
366–369), on a constructed bank that holds only the 40 block cells (`constructed_bank`, 353–363;
CAL §14a item 6, CAL:1260). **The board counts only if its class capacity is certified:** `cert` ≥
0.90 as an exact `Fraction` count of a stored member (CAL §6, CAL:843–867; `cert_search`, CAL script
393–431).
- A board with `cert` < 0.90 is **not dropped**: it is printed, counted under its own name
  (`CERT_BELOW_CUT`) and excluded from the denominators of P1–P5. On the 99 seen boards this never
  happened (min 0.975), so it is not expected.
- **No real bank is read.** The constructed bank needs no degree terms. The CAL script fitted N1 on
  the real bank only for its worlds (`K.degree_terms()`, CAL script 1322), and this run has no
  worlds.

**Decision rule, rule #2.1.** The sub-kind is read by CAL §6's separator table (CAL:886–893;
`separator_reading`, CAL script 746–763), imported unchanged. This time it is **printed per board**:
the calibration applied it to worlds only (`read_world`, 874–877), and `read_perm_board` (935–949)
never calls it. Orbit's CALLS edges into `separator_reading` come from `read_world` and one test
only; `grep` confirms no other call site in the CAL script.
- **Every AUC object is printed as an exact and `_tau` pair**, with its `ulp_sensitive` flag (CAL
  §6a, CAL:907–913): `ceiling_block`, `ceil_1`, `ceil_1_float`, `ceil_λc_float`, `ceil_1_starts100`
  (float, the value the separator reads; CAL:531–533) and its quantised twin, and `cert`.
- **The split flags of CAL §6a** are raised and counted by name: `GATE_ULP_SPLIT`,
  `CEIL_1_ULP_SPLIT` and `CERT_ULP_SPLIT` (CAL:915–923, 979–980). Each board's reading follows the
  exact value.
- **New printed flag, deciding nothing:** `DECODER_SPLIT_AT_LC`, raised when `ceil_λc_float` and
  `ceiling_block` fall on opposite sides of 0.90 (seen once, j = 49, §1).

**Decision rule, the BF family (Zcode).** For each BF_r, r = 1–4, the following are printed per
board, each exact and `_tau`:
- `ceiling_block` and its `lambda_block` (the permuted CSV of CAL printed no BF λ; CAL script
  970–974);
- `ceil_1` at λ = 1 on the block mask (`bf_block_lambda1`, CAL script 565–578, which the CAL script
  ran for worlds only: `plan_world`, 701–705, against `plan_perm_ref`, 708–712).

The BF separator row is:

| BF_r `ceiling_block` | BF_r `ceil_1` | reads |
|---|---|---|
| ≥ 0.90 | any | gate passed |
| < 0.90 | ≥ 0.90 | **BF fit failure, selection** (the fit at λ = 1 is a class member that passes) |
| < 0.90 | < 0.90 | **BF: not separated** for r = 1–3. For r = 4, **BF fit failure, not selection**, since BF_4 holds every 5 × 8 pattern at AUC 1 by construction (CAL §8, CAL:1057–1075) |

- **Why no `cert` for BF.** BF_r's class is N1's *fixed* additive offset plus `U Vᵀ` (CAL:446–447).
  It does not contain the free class, so rule #2.1's `cert` is not a lower bound for it.
- **BF is not quantised** (CAL:484–486), so there is no FF-quant row.

## 3. Seeds (fresh; outside every used range)

**Proposed:**

| use | seeds |
|---|---|
| boards, j = 0 … N − 1 | **94000 + j**: 94000–94299 for N = 300 |
| `cert` search: stage 1, 5 refinement reruns, 2 deep reruns | **94500; 94501–94505; 94506–94507** |

**Every range in use, and what checked it:**

| owner | seeds | where |
|---|---|---|
| A | 90000, 90001, 90010–90029, 90100–90154, 90160–90184 | B script 314–315 (`A_SEEDS`) |
| B | 91000, 91001, 91010–91029, 91100–91184 | B script 308–311 |
| male arm | 92000, 92001, 92010–92029, 92100–92184, declared range 92000–92999 | B script 317; `knockout_regrow_male_cns.py`:345–349 |
| calibration worlds | 93100–93104, 93110–93114, 93120–93124; indices 3 and 4 kept unused (93130–93134, 93140–93144) | CAL script 95–99 |
| calibration permuted reference | **93200–93298** | CAL script 97 |
| calibration `cert` | 93300–93307 | CAL script 91–93, 98 |
| untouched and reused (`reserved_seeds`) | 60000, 61000, 70000–70999, 80000–80999, `PL_SEED` 4242, `PL_SCRAMBLE_SEED` 99, `PRSH_SEED` 7, `RP_SEED_BASE` 1000 + 0–19, dial 10000 + 100 fi + sd (10000–10404), 20260923, shuffles 0–98, ALS starts `PCG64(30000 + j)` | B script 1031–1041; `harness.py`:71–76, 540, 1078–1079, 1153 |
| design seeds (SURVEY, M8) | 2026, 11, 100–104, 200–201, 0–2, 20260929, 2026092901–2026092906 | CAL script 101–102 |
| other fixed seeds in `.py` | 12345 (B script, A script, `power.py`) | `git grep` |

**Grep checks (2026-09-29).**
- `git grep -n -E '\b94[0-9]{3}\b' -- '*.py'` finds only `DL_BANK_REAL_REGISTERED = 94812`
  (`harness.py`:545), which is a bit count, not a seed, and lies outside both proposed ranges.
- The same pattern over `docs/*.md` finds no seed use.
- The ALS starts reach at most 30099 (with `ceil_1_starts100`'s 100 starts).

So both proposed ranges are disjoint from every row above.

**The script's own seed check (Zcode's rider 4).** It takes its own ranges as literals, as CAL's
S-C11 does (CAL:1244; `assert_seeds_cal`, CAL script 267–290). It asserts:
- the literals are pairwise disjoint;
- they are disjoint from `K.reserved_seeds(100)` (A, the male arm, the untouched list, the shuffles
  and the ALS starts), from B's own seeds, from **every calibration literal** (worlds, the unused
  indices, **93200–93298** and 93300–93307, imported from the CAL script rather than retyped), and
  from the design seeds;
- **no fresh board's pattern equals any seen pattern**: board z, z′, the 10 FN boards and the 99
  permuted boards of the calibration. This is a pattern check, not a seed check. A collision has
  probability about 1/C(40, 20) ≈ 7e-12 per pair, but the check makes "fresh" structural.

A failure stops the run before any folder exists.

## 4. N, power and compute

**Proposed N = 300 boards.**

**Power for the rate near 0.5 (P1).**
- The seen rate is 53/99 = 0.535.
- At N = 300 the 95% half-width of a rate near 0.5 is about 0.057.
- If the true rate is 0.5, P(120 ≤ count ≤ 180) = 0.9996. If it is 0.535, the probability is 0.990.
- At N = 100 these probabilities are 0.965 and 0.918, and the half-width is 0.098, as wide as P1's
  band. That is too loose.

**Power for the j = 89 class at ≤ 1 in 30 (P2b).**
- At a true rate of 1/30, N = 300 expects 10 such boards.
- The one-sided 5% test of "rate ≤ 1/30" rejects at **16 or more** (P(X ≥ 16 | 1/30) = 0.046).
- At a rate of 1/10 it rejects with probability 0.999.
- If the class is as rare as the seen 1 in 99, N = 300 finds at least one with probability 0.95.
  N = 100 would find one with probability only 0.64, and N = 200 with 0.87.

(Binomial arithmetic, this draft, `scipy.stats.binom`.)

**CPU time, from the calibration run.**
- **The calibration's whole run took 2,857 s** on 30 workers (`stdout.log`:85; `calibration.json`
  `runtime_s` 2856.2). Of that, the cert phase took 97 s for 110 patterns (`stdout.log`:4, 27),
  the fit phase took 2,722 s for 15 worlds plus 99 boards (`stdout.log`:29, 51), and the ko1 phase
  took 5 s (`stdout.log`:68).
- **The worlds dominate that total.** From the raw fits' per-task `secs`:
  - the 9,630 world tasks used 78,275 CPU-s;
  - the 495 permuted-board tasks used 2,970 CPU-s, **30.0 CPU-s per board** (min 24.4, max 32.1).
  - Of the 30.0: the separator (the registered block path, `ceil_1` and `ceil_1_starts100`) took
    11.3; BF_1–BF_4's block fits took 2.8, 4.4, 5.4 and 6.1.
  - These are timings under a full 30-worker load, so they already include the contention.
  - Cross-check: about 81,200 fit CPU-s plus about 2,900 cert CPU-s, divided by 30 workers, is
    about 2,800 s, against 2,857 s measured.
- **Per fresh board:**
  - fits, 30.0 CPU-s;
  - BF `ceil_1` fits (new here), at most 18.7 CPU-s (bounded by the nested BF block fits, which do
    more work);
  - `cert`, about 26.5 CPU-s (97 s × 30 workers / 110 patterns).
  - Total ≤ 75 CPU-s.
- **N = 300: about 22,600 CPU-s, or about 12.5 min wall on 30 workers.** With a 1.5× margin for
  pool start-up and uneven tails it is about 19 min.
- **Mike's rule.** A run over 30 min needs his word. This estimate is under 30 min. **The script's
  `--estimate` is run first. If it reports over 30 min, the run waits for Mike's word.** Either way
  the registered run starts only after the reviewers' yes, the prediction commit (§6) and Mike's
  order, as the calibration's did (CAL script 68–71).

## 5. Compute on the CPU

Every number is computed on the CPU. The GPU instrument is not validated for block fits in a
tie-carrying regime:
- The extension X plan withholds from any pass of VX1/VX2/VX6/VX7 "any composition whose block
  fits carry ties on S(f)". For such a composition a **VX8-like cross-check** is mandatory, "and it
  needs a CPU pre-run store of those worlds as its witness. The order is: **CPU pre-run → VX8 →
  GPU**" (`docs/plans/2026-09-29-gpu-instrument-extension-x-plan.md`:153–157; recorded as Ark's
  point at :275–276).
- It names **"the failed-fit calibration's block fits, in particular"**: the calibration stays on the
  CPU (:158–160, :168–171).
- It also withholds **the block λ branch**, λ other than 1 on a block view, which is not witnessed on
  A or B (:161; :96). λ = 100 on a block view is exactly this run's object.
- Rule #2.1 is excluded as well (:162).

## 6. Predictions (written before any value; committed on their own before the run)

**The prediction commit (Warren and Johnny's rule, CAL:778–779).** The predictions below, with
their thresholds, are committed in a commit of their own, containing this file only, **before** the
registered run. The script records that commit's hash, and refuses the registered form unless the
hash is an ancestor of HEAD and the registration's LF sha256 equals the pin. The blind review checks
the order from git.

Denominators:
- N_c is the number of boards with `cert` ≥ 0.90.
- A **failure** is a board with rule #2.1's `ceiling_block` < 0.90, read exactly.
- A **pass** is the complement within N_c.

Zcode's predictions (1)–(4) are given in substance as posted; Ark's is P5.

| # | prediction | holds if | fails if |
|---|---|---|---|
| **P1** (Zcode 1) | the natural collapse rate on fresh seeds is in [0.4, 0.6] | failures / N_c ∈ [0.40, 0.60] (120–180 of 300) | outside |
| **P2a** (Zcode 2) | all failures are fit-side, and the rule's failures are FF-sel apart from the j = 89 class | every failure reads a **fit-failure** row of CAL §6, and none reads "not separated: rank limit or fit" | any failure reads "not separated" |
| **P2b** (Zcode 2) | FF-struct/opt candidates of the j = 89 class are at most 1 per 30 boards | the count of failures whose row is not FF-sel (FF-struct or FF-opt, FF-opt named, FF-quant at λ = 1) is ≤ 15 of 300 (the one-sided 5% binomial bound at 1/30, §4) | ≥ 16 of 300 |
| **P3** (Zcode 3) | the BF family collapses at a rate of the same order | for each r = 1–4, the rate of BF_r `ceiling_block` < 0.90 over N_c is between 0.5× and 2× the rule's failure rate | any r outside that band |
| **P4** (Zcode 4) | every passing board chooses λ = 1 | 0 passes with λ_c ≠ 1 | ≥ 1 |
| **P5** (Ark) | choosing λ = 100 marks failure | (i) ≥ 90% of the boards with λ_c = 100 fail, **and** (ii) ≥ 95% of the failures have λ_c = 100 | either part fails |

Notes written before values:
- **P4 is already contradicted by the seen set:** 3 of 46 passes chose λ = 100 (§1). It is
  registered as posted. If that rate held (3/46 ≈ 6.5%) and about 140 boards passed, P4 would fail
  with near certainty. Whether Zcode wants a stated tolerance is Q-Z1 (§11).
- **P5's thresholds** are drafted from the seen 53/56 = 0.946 and 53/53. Ark's "52 of 56" counted
  FF-sel boards, not failures (§1); P5 counts failures (Q-A1).
- **P3's band** 0.5×–2× is the drafting agent's reading of "the same order". On the seen set every
  ratio is 48/53 to 50/53, about 0.9–0.94 (Q-Z2).
- **At-the-cut cases** follow CAL: "≥ 0.90" is inclusive. The seen j = 57 is FF-sel at `ceil_1` =
  0.900 exactly. The count of failures with `ceil_1` in [0.90, 0.91) is printed.

## 7. Outcome labels (named before values; the outcome is the list of those that hold)

| label | condition | what it licenses |
|---|---|---|
| **RP1: replicated** | P1 and P2a and P2b hold | the natural FF-sel collapse is a stable property of the registered block-only fitter on permuted 20/40 boards of block B's 5 × 8 shape, at the rate stated; a later registration may cite the rate with its interval |
| **RP2: collapse replicated, rate shifted** | P2a and P2b hold, P1 fails, and failures ≥ 30 of 300 (≥ 0.10) | the kind replicates, the rate does not; the rate is reported with its interval, and no text cites 0.5 |
| **RP3: kind not replicated** | P2a holds, P2b fails | failures are fit-side, but not dominantly FF-sel; the sub-kind mix is reported |
| **RP4: not replicated** | failures < 30 of 300 (rate < 0.10) | the seen 53 of 99 is not reproduced on fresh seeds; the seen reference is read as a property of those 99 seeds, or of a difference between the runs (examined before any reading) |
| **RP5: class-side finding** | any board with `cert` < 0.90, or any failure reading "not separated" | a permuted board below the certificate: a design finding for CAL §2a and C6's scope, reported by board |
| **RP6: stop** | a stop of §8 fires (seed or pattern assert, prediction commit not an ancestor, script-defect refit mismatch, `cert` counts void) | a design error; nothing is read |

P3, P4 and P5 are reported as **hold / fail** lines beside the labels. They enter no label, because
none is needed to name what replicated.

**Secondary outcome: does the j = 89 class reproduce?**
- **J89-reproduced** if at least one certified failure reads "FF-struct or FF-opt, not separated"
  or "FF-opt" (`ceil_1_starts100` ≥ 0.90). The count is split by row: FF-opt named against
  FF-struct/opt not separated. FF-quant at λ = 1 is counted separately.
- **J89-not-reproduced** if there are none.
- No sub-kind is witnessed by construction (CAL §7, CAL:1004–1008). These rows are **residuals**,
  named as such.

## 8. Script

**A new small script** is proposed:
`results/genome/c6/checks/natural_fit_failure_replication.py`, with its test file
`test_natural_fit_failure_replication.py`.
- It **imports** the CAL script (as the CAL script imports the B script, CAL script 56–58), whose
  bytes are pinned by LF sha256.
- It adds no new mode to the CAL script, because the CAL script is registered and hashed (its
  manifest carries `script_sha256_lf`).
- It reuses, unchanged:
  - `perm_ref_y`'s construction, re-seeded (see S-R1);
  - `constructed_bank`, `cert_search` and `cert_patterns`' dedupe logic;
  - `separator_fits` and `bf_block_lambda1`;
  - `auc_counts`, `split_at_cut` and `separator_reading`;
  - `run_groups`' pattern;
  - the output helpers of the B script (`write_text_synced`, `dump_json`, `write_sha256sums`).

**S-items:**

| # | item |
|---|---|
| S-R1 | `fresh_y(j)`: `default_rng(94000 + j).permutation(40)` on board z's labels. `perm_ref_y` hard-wires `SEED_PERM_REF` (CAL script 366–369), so the construction is repeated with the seed as an argument, and a test asserts it equals `perm_ref_y(j)` when given 93200 + j |
| S-R2 | seed and pattern asserts (§3), literals in the file, the calibration's literals imported |
| S-R3 | `cert` per pattern at CAL's registered budget (`CERT_BUDGET_REGISTERED`, CAL script 117–119), with this file's seeds 94500–94507. `cert_search` takes its seeds from module globals (CAL script 399–413), so the call runs under a scoped swap of those globals (the `swapped_globals` pattern, 439–448) or through a thin copy asserted equal on board z with CAL's seeds. **Q-J1** |
| S-R4 | per board: `sep` (CAL `separator_fits`: the registered block path, `ceil_1`, `ceil_1_starts100`, float and quantised); BF_1–BF_4 block fits by `K._fit_one`; BF_1–BF_4 `ceil_1` by `bf_block_lambda1` (new for permuted boards) |
| S-R5 | per board: the rule's CAL §6 row (`separator_reading`), the BF row (§2), every AUC object exact and `_tau` with `ulp_sensitive`, the flags `GATE_/CEIL_1_/CERT_ULP_SPLIT`, `DECODER_SPLIT_AT_LC` and `CERT_BELOW_CUT`, λ_c for the rule and each BF_r |
| S-R6 | the script-defect stop of CAL (a refit not bit-equal to the registered block fit, CAL:975–978) |
| S-R7 | P1–P5 evaluated by the thresholds of §6; the labels of §7 as a list; the secondary outcome; the (iii) population table (§10) |
| S-R8 | outputs: `boards.csv` (one row per board, every column of S-R5), `replication.json`, `cert_members.json`, `raw_fits.json.gz` (to the data folder, as CAL), `REPLICATION.md`, `stdout.log`, `SHA256SUMS.txt` last and only on a completed run; `stop_record.json` and exit 1 on a stop (CAL:981–984) |
| S-R9 | refusals before any folder: the CAL script's and the B script's LF sha256 pinned; this registration's pin; the prediction commit an ancestor of HEAD; a clean tree; `--out` new; CPU only |
| S-R10 | `--estimate` (times one board's tasks and one `cert`, scales to N) and `--dry-run`, as the CAL script has them (1159–1207, 1265–1273) |

**Tests:**
- S-R1 equality with `perm_ref_y` on three seen seeds.
- The seed and pattern asserts refuse a seen seed and a seen pattern.
- `separator_reading` rows reproduced on synthetic inputs, including the at-the-cut case.
- The BF row table.
- The flags, including `DECODER_SPLIT_AT_LC` on j = 49's seen values.
- P1–P5 and every label at their boundaries: 119, 120, 180 and 181 for P1; 15 and 16 for P2b.
- The `cert` seed swap restores the CAL globals.
- The refusals.
- **The seen board j = 89 read by hand from `permuted_reference.csv` gives "FF-struct or FF-opt, not
  separated"** when `ceil_1_starts100` < 0.90.

**The tripwire lesson (commit `5d65baf`).** Every refusal test traps `fit_task`, the run body
`_run` and **every process pool** (`run_groups`).
- The reason: the `cert` phase runs in a worker pool before any fit, and a monkeypatch does not
  reach worker processes (`test_failed_fit_calibration.py`:385–395; commit message of `5d65baf`).
- The new file's refusal tests use a tripwire fixture of the same form. It traps this script's own
  `_run` and pool, **and** the imported CAL `run_groups`, so that a refused form can neither fit
  nor search.

**Windows encoding rules.**
- Every run and test is launched with `PYTHONUTF8=1`, since a redirected cp1252 stdout once killed a
  registered run after unsealing.
- Every file write and read names `encoding="utf-8"`. CSVs are written with `lineterminator="\n"`
  (CAL script 979–984). Every text file is LF.
- CSV headers are ASCII (asserted, as CAL script 975–976).

## 9. Compute record, restated

CPU, 30 workers, N = 300, estimate about 12.5 min (≤ 19 min with margin; §4). No bank is read, and
no GPU is used (§5).

## 10. (iii): the passing boards as a population (Ark)

The boards that pass at λ = 1 are a natural population for the interaction question of CAL §13
(CAL:1173–1225): a gate passed with the interaction term live. For each such board the script
prints:
- rule #2.1's `ceiling_block` and `ceil_1`;
- N1's block AUC through its decoder (the additive part alone, exact and `_tau`);
- the gap between `ceiling_block` and N1.

This population is **printed and decides nothing here.** It is material for a later (iii)
registration, and no label, prediction or stop reads it. Passes at λ = 100, like the seen j = 15,
49 and 76, are printed in a separate table, since there the gate may be passed on the additive part
(compare CAL's board 41, CAL:735–742).

## 11. Open questions (each with a recommendation)

**For Ark.**
- **Q-A1.** P5 counts failures among λ = 100 boards, with thresholds (i) ≥ 90% and (ii) ≥ 95%. Your
  "52 of 56" counted FF-sel boards; the failure count is 53 of 56. *Recommendation:* keep P5 on
  failures, with the thresholds as drafted, and print the FF-sel-only count beside it.
- **Q-A2.** Should j = 89's `ceil_1_starts100` be read now from the calibration's raw fits (it is on
  disk, in the `sep` record of `perm:89`) and recorded as seen before the prediction commit? It
  would tell whether the seen case is FF-opt or FF-struct/opt. *Recommendation:* yes. It is
  post-data on a seen board, costs no fit, and sharpens J89's definition; read it by a script
  named in the chat, before the commit.

**For Johnny.**
- **Q-J1.** How should `cert` get the fresh search seeds (S-R3)? The options are a scoped swap of
  the CAL module globals, or a thin copy asserted equal. *Recommendation:* the scoped swap, with the
  test that the CAL globals are restored and that the swap reproduces CAL's `cert` on board z. No
  search code is duplicated.
- **Q-J2.** Fresh `cert` search seeds (94500–94507) or CAL's 93300–93307? A search seed makes no
  data, so reuse would keep the instrument identical. *Recommendation:* fresh, so that the one
  rule "no seed reused" holds without exceptions.

**For Warren.**
- **Q-W1.** Is the prediction-commit refusal (S-R9: the prediction commit must be an ancestor of
  HEAD) the right way to enforce your rule, or is a hash in the manifest enough? *Recommendation:*
  refuse. A manifest hash only records what a refusal enforces.
- **Q-W2.** P2b's threshold (≤ 15 of 300) is a one-sided 5% test of "≤ 1 in 30". Is a test the
  reading you want, rather than the plain "≤ 10 of 300"? *Recommendation:* the test. At a true rate
  of exactly 1/30 the plain count fails about half the time.

**For Zcode.**
- **Q-Z1.** P4 is contradicted by the seen set (3 of 46 passes at λ = 100; §1). Keep it verbatim, or
  restate it with a tolerance, for example "≥ 90% of passes choose λ = 1", before the commit?
  *Recommendation:* keep (4) verbatim as posted, since it was your prediction. If you want the
  tolerant form, post it as a separate prediction (4′) before the commit, stating that the seen
  count was known.
- **Q-Z2.** Is 0.5×–2× the rule's rate your meaning of "the same order" for P3, per BF_r?
  *Recommendation:* yes, per r, with the 2 × 2 table (rule failure × BF_r failure) printed.

**For Mike.**
- **Q-M1.** N = 300, about 12.5 min estimated (≤ 19 min with margin) on the CPU. *Recommendation:*
  approve N = 300. It is under your 30-minute line, and it gives P1 and P2b their power (§4). If
  `--estimate` reads over 30 min, the run waits for your word.
- **Q-M2.** The run order: reviewers' yes → the prediction commit (this file alone) → the script and
  its tests, reviewed → the pin → your order → the run → a blind review. *Recommendation:* approve
  this order. It is the calibration's order, plus the separate prediction commit.
