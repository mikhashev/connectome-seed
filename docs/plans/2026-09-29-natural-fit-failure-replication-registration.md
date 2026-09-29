---
**Status: rev 1.2, a consistency-only revision of rev 1.1 (reviewed: all four yes). Rev 1.1 is the
prediction commit `b5513e3`, an ancestor of rev 1.2; it stays the pinned prediction commit.** Rev 1 was drafted 2026-09-29 UTC by a CC subagent on Mike's choice of option A
(DPC Research chat, 2026-09-29): a replication registration of the natural fit failure seen on the
permuted boards of the failed-fit calibration. Nothing was run, fitted or committed by the drafting
agents. The only reads of data were the calibration's committed outputs, the `secs` timing field of
its raw fits (for the compute estimate, §9) and, in rev 1.1, board j = 89's stored separator record
(§1, `j89_read.py`); every recount in §1 was done from `permuted_reference.csv` (the permuted
boards; `bf_block.csv` holds the worlds only).
---

**Rev 1.1 (2026-09-29 UTC), after the reviews in the DPC Research chat** (Warren 14:01:36, Zcode
14:02:09, Ark 14:05:32 with an inner message of 14:04:30, Johnny 14:07:54; all four voted yes):
- **Ark and Zcode (Q-A2):** j = 89's `ceil_1_starts100` was read from the calibration's raw fits
  before the prediction commit (§1); j = 89 is classified under §6's table, and the J89 secondary
  outcome is restated (§7).
- **Zcode (Q-Z1, as the prediction's author):** P4 withdrawn before the prediction commit and P4′
  registered (§6). Ark and Johnny's view (keep P4 with an "expected to fail" note) is recorded.
- **Zcode:** P2a labelled a design check, not a prediction (§6); Zcode's BF figures added to §1,
  recomputed.
- **Ark (Q-A1):** P5 kept on failures with the FF-sel count printed beside it; P5 marked a label,
  not independent evidence (§6). The BF_4 carrier in §2 cites `bf4_capacity.md` and `bf4_check.py`.
- **Warren (Q-W1, Q-W2):** the prediction commit's hash pinned in the script, with the
  `git merge-base --is-ancestor` refusal and every run from the repo root (§8, S-R9); P2b restated
  in Warren's wording (§6, §4).
- **Johnny (Q-J1, Q-J2):** fresh `cert` seeds 94500–94507 by a scoped swap of the CAL module
  globals, with two tests (§8, S-R3); the §4 timing carrier made exact.

**Rev 1.2 (2026-09-29 UTC), consistency only, written while the script was drafted and before any
value of a fresh board.** No prediction, threshold or label condition of §6–§7 changes. Each item
either restates what the §6 table row already says or defines what the text left undefined:
- **P2b (§6 note, §8 tests).** At the prediction commit `b5513e3`, the §6 table row named 10 as the
  decision line ("if > 10, the prediction is refuted", Warren, Q-W2, 14:01:36 UTC), while the §6
  note ended "the verdict is the test's" and §8's tests put P2b's boundary at 15/16. The
  contradiction is resolved in favour of the table row: 10 is the decision line (10 holds, 11
  fails); the one-sided 5 % test (15 does not reject, 16 rejects) is printed and decides nothing.
- **RP6, "`cert` counts void" (§7).** Undefined at rev 1.1. It follows the calibration's resolution
  (CAL §6a; CAL §14a, A-3): the exact `Fraction` count is the certificate, and a disagreement between
  the search's three counts is printed as the flag `CERT_COUNTS_DISAGREE`, not a stop. RP6 is
  restated as the stops only (§7).
- **The cut on `cert` (§2).** Stated as applied: exact `Fraction` ≥ 9/10, with the float route
  asserted equal.
- **What the script does that §8 and §10 did not name:** the S-R6 refit task, N1's block fit for
  §10, a third table for passes at another λ, and empty denominators read "n/a" (§8, §10).
- **`raw_fits.json.gz`** stays in the `--out` folder under `connectome-seed-data`; CC copies only the
  small outputs into the repo, as with the calibration (§8, S-R8).
- **Seen patterns (§3):** block B's 20 permuted-ceiling boards added to the list.
- **The prediction commit's content (§6):** `b5513e3` touches only this file; "this file only" is
  checked from git by the blind review.

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

All counts come from `permuted_reference.csv` (header at line 1, board j at line j + 2; its
`bf1`–`bf4_ceiling_block` columns carry the BF values of the permuted boards, since `bf_block.csv`
holds the 15 worlds only). The sub-kind is read by hand with CAL §6's table (CAL:886–893), since the CAL script
does not print a separator row for permuted boards (§8, item 1).

| claim relayed in the chat | recomputed | matches? |
|---|---|---|
| 99 boards, seeds 93200–93298 | 99 rows, seeds 93200 (line 2) to 93298 (line 100) | yes |
| `ceiling_block` < 0.90 on 53 of 99 | 53 of 99 (also CAL-OUT `CALIBRATION.md`:54); the `_tau` value agrees on every board, so no `GATE_ULP_SPLIT` | yes |
| `cert` ≥ 0.90 on all 99, min 0.975 | 99 of 99, min 0.975 (board j = 57, line 59; `CALIBRATION.md`:54; BLIND_REVIEW.md:91) | yes |
| 52 of the 53 are FF-sel (λ_c = 100, `ceil_1` ≥ 0.90) (Ark 10:39:27, Zcode 10:44:08 UTC) | 52 of 53. **One of the 52 sits exactly at the cut:** j = 57, `ceil_1` = 0.900000 (line 59), FF-sel only by "≥" | yes, with the at-the-cut note |
| one borderline: j = 89, seed 93289, `ceil_1` 0.895, `cert` 0.9875 | line 91: `ceiling_block` 0.730, λ_c 100, `ceil_1` 0.895 (exact = `_tau`), `ceil_1_float` 0.895, `ceil_λc_float` 0.730, `cert` 0.9875 (exact = `_tau`), cert rerun spread 5 pairs. By CAL §6 it reads **"fit failure, FF-struct or FF-opt, not separated"** unless `ceil_1_starts100` ≥ 0.90; that value is not in any CSV. **Rev 1.1: it was read from the raw fits and is 0.895 (SEEN; below)**, so the row stands. All four BF_r read 0.725 there | yes |
| λ = 100 chosen on all 53 failures | 53 of 53 | yes |
| λ = 1 chosen on all 43 passes | **there are 46 passes, not 43.** 43 chose λ = 1; **3 passed at λ = 100**: j = 15 (0.9275, line 17), j = 49 (0.915, line 51), j = 76 (0.915, line 78). λ took only the values 1 and 100 (56 × 100, 43 × 1; BLIND_REVIEW.md:101–102) | **no: 43 of 46** |
| BF collapse on the 53: `bf1` ≥ 0.90 on 3, `bf2` 11, `bf3` 9, `bf4` 9 (Zcode) | 3, 11, 9, 9 of 53 | yes |
| Zcode's further BF figures (rev 1.1): BF_r < 0.90 on 50, 48, 50, 50 of all 99; BF_r ≥ 0.90 on 46, 40, 40, 40 of the 46 passes; 39 of the 53 failures have the whole family failing | recomputed in rev 1.1 from `permuted_reference.csv` (`bf1`–`bf4_ceiling_block`, `ceiling_block`): 50, 48, 50, 50 of 99; 46, 40, 40, 40 of 46; 39 of 53 with every BF_r < 0.90 | yes |
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

**SEEN in rev 1.1, before the prediction commit: board j = 89's separator record (Q-A2).**
- **The read.** `docs/prereg-scripts/2026-09-29-capacity-survey/j89_read.py` (output
  `j89_read_out.txt`; both hashed in that folder's README) opens the calibration run's
  `raw_fits.json.gz` read-only (its sha256 `3b053b70…afd04` is the one listed in the run's
  `SHA256SUMS.txt`) and reads the task `perm:89 || sep || rule` (the key of `plan_perm_ref`), the four
  `perm:89 || block || BF:r` tasks and the board's `cert` member. Every AUC is recomputed from the
  stored p and y by an exact count (checked with `Fraction`) and under `TAU`. No fit was made.
- **The values** (exact = `_tau` on every one; none is ulp-sensitive):

  | object | value | counts (of 400 pairs) |
  |---|---|---|
  | `ceiling_block` (λ grid 1, 3, 10, 30, 100; λ_c = 100) | 0.730 | 277 wins, 30 ties |
  | `ceil_λc_float` | 0.730 | 277 wins, 30 ties |
  | `ceil_1` (quantised) | 0.895 | 358 wins, 0 ties |
  | `ceil_1_float` | 0.895 | 358 wins, 0 ties |
  | **`ceil_1_starts100` (float; the separator reads it)** | **0.895** | 358 wins, 0 ties |
  | `ceil_1_starts100_quantised` | 0.895 | 358 wins, 0 ties |
  | `cert` (recounted from the stored member) | 0.9875 = 79/80 | 395 wins, 0 ties |
  | BF_1–BF_4 `ceiling_block`, each at λ = 100 | 0.725 each | 271 wins, 38 ties |

  The 100-start fit's p differs from the 1-start fit's, but it reaches the same count. The four
  separator values equal the printed CSV row. BF `ceil_1` was not fitted on permuted boards
  (`plan_perm_ref`), so none exists.
- **Classification under §6's table (CAL §6):** `ceil_1_starts100` = 0.895 < 0.90, so j = 89 is
  **"fit failure, FF-struct or FF-opt, not separated"**, not FF-opt named. Neither 100 ALS starts
  nor dropping the quantisation lifts it, while a class member reaches 0.9875.
- **What the J89 secondary outcome now tests (§7).** The seen case is of the row "FF-struct or
  FF-opt, not separated". So J89-reproduced now asks whether that exact row, a certified failure
  that stays below 0.90 at λ = 1 under 1 start, 100 starts, float and quantised alike, recurs on
  fresh boards. FF-opt named (`ceil_1_starts100` ≥ 0.90) is a different, unseen row. It is counted
  and printed, but it no longer reproduces j = 89.

## 2. Object and decision rule

**Object.** A permuted 40-cell block pattern, built exactly as CAL §10 builds it:
`default_rng(seed).permutation(40)` applied to board z's 40 labels (`perm_ref_y`, CAL script
366–369), on a constructed bank that holds only the 40 block cells (`constructed_bank`, 353–363;
CAL §14a item 6, CAL:1260). **The board counts only if its class capacity is certified:** `cert` ≥
0.90 as an exact `Fraction` count of a stored member (CAL §6, CAL:843–867; `cert_search`, CAL script
393–431).
- **The cut is applied as exact `Fraction` ≥ 9/10** (rev 1.2), and the float route that
  `separator_reading` takes (`cert` as a float against the float cut 0.90) is asserted equal on
  every board. A `Fraction` must not be passed to the float cut itself: in Python,
  `Fraction(9, 10) < 0.9` holds, since the float 0.9 lies just above 9/10.
- **The three counts of the search** (search, `Fraction`, registered AUC) are printed. A
  disagreement raises the flag `CERT_COUNTS_DISAGREE` and is not a stop; the `Fraction` count is the
  certificate (CAL §6a; CAL §14a, A-3; rev 1.2).
- A board with `cert` < 0.90 is **not dropped**: it is printed, counted under its own name
  (`CERT_BELOW_CUT`) and excluded from the denominators of every prediction of §6. On the 99 seen
  boards this never happened (min 0.975), so it is not expected.
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
| < 0.90 | < 0.90 | **BF: not separated** for r = 1–3. For r = 4, **BF fit failure, not selection**, since BF_4 holds every 5 × 8 pattern at AUC 1 by construction (CAL §8, CAL:1057–1075; the argument is `docs/prereg-scripts/2026-09-29-capacity-survey/bf4_capacity.md`, checked by `bf4_check.py` on 824 boards × 2 offsets, including 50 boards with block B's row profile 2, 6, 4, 4, 3, with 0 failures) |

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
  permuted boards of the calibration, and block B's 20 permuted-ceiling boards (seeds 91010–91029,
  `K.permute_block` of board z; added in rev 1.2). This is a pattern check, not a seed check. A collision has
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
- At the seen rate of 1/99, N = 300 expects 3.03 such boards with SD 1.73, so the stated count 10
  is about 4 SD above the mean, and the test's cut of 16 lies further still (P2b's note, §6).
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
  - **So the 30.0 CPU-s includes the separator and BF block fits from the calibration; BF `ceil_1`
    is new and adds up to 18.7** (Johnny; 2.8 + 4.4 + 5.4 + 6.1 = 18.7).
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
script is pinned and before the registered run. **The prediction commit's hash is pinned in the
script as a literal** (Warren, Q-W1). The script refuses the registered form unless
`git merge-base --is-ancestor <pinned> HEAD` holds and the registration's LF sha256 equals its pin.
Every run, `--estimate` included, is launched from the repo root, and the script refuses otherwise.
The blind review checks the order from git. **Rev 1.2:** the prediction commit `b5513e3` touches only
this file; "this file only" is checked from git by the blind review.

Denominators:
- N_c is the number of boards with `cert` ≥ 0.90.
- A **failure** is a board with rule #2.1's `ceiling_block` < 0.90, read exactly.
- A **pass** is the complement within N_c.

Zcode's predictions (1)–(3) are given in substance as posted, (4) is withdrawn and replaced by
(4′), and Ark's is P5.

| # | prediction | holds if | fails if |
|---|---|---|---|
| **P1** (Zcode 1) | the natural collapse rate on fresh seeds is in [0.4, 0.6] | failures / N_c ∈ [0.40, 0.60] (120–180 of 300) | outside |
| **P2a** (Zcode 2) — **a design check, not a prediction** | all failures are fit-side | every failure reads a **fit-failure** row of CAL §6, and none reads "not separated: rank limit or fit" | any failure reads "not separated" |
| **P2b** (Zcode 2; Warren's wording) | FF-struct/opt candidates of the j = 89 class are at most 1 per 30 boards: **the prediction is ≤ 10 of 300** | **decision line (Warren, Q-W2, 14:01:36 UTC): "if > 10, the prediction is refuted".** It holds if the count of failures whose row is not FF-sel (FF-struct or FF-opt not separated, FF-opt named, FF-quant at λ = 1) is ≤ 10 of 300. Printed beside it, deciding nothing: the one-sided 5 % test of "rate ≤ 1/30" (cut ≥ 16 of 300, P(X ≥ 16 \| 1/30) = 0.046, §4). Note (CC): at a true rate of exactly 1/30 the line of 10 fails about half the time; at the seen rate of 1/99 it is about 4 SD above the mean (Warren) | > 10 of 300 |
| **P3** (Zcode 3) | the BF family collapses at a rate of the same order | for each r = 1–4, the rate of BF_r `ceiling_block` < 0.90 over N_c is between 0.5× and 2× the rule's failure rate | any r outside that band |
| ~~**P4**~~ (Zcode 4) | ~~every passing board chooses λ = 1~~ — **withdrawn by its author before the prediction commit: contradicted by the seen set (3 of 46 passes at lambda = 100), which was in the author's own count and dropped in phrasing** | — | — |
| **P4′** (Zcode 4′) | **at least 90 % of passing boards choose λ = 1** (seen: 43 of 46 = 93.5 %) | passes with λ_c = 1 / passes ≥ 0.90 | < 0.90 |
| **P5** (Ark) — **a label, not independent evidence** | choosing λ = 100 marks failure | (i) ≥ 90% of the boards with λ_c = 100 fail, **and** (ii) ≥ 95% of the failures have λ_c = 100 | either part fails |

Notes written before values:
- **P2a is a design check.** Given `cert` ≥ 0.90, every failure reads a fit-failure row of CAL §6
  by construction: the only row that is not a fit failure, "not separated: rank limit or fit", needs
  `cert` < 0.90, and such boards are `CERT_BELOW_CUT` and leave the denominators (§2). So P2a can
  fail only through a script defect. **The predictive weight sits in P2b** (Zcode).
- **P2b (Warren, Q-W2).** At the seen rate of 1/99, N = 300 expects about 3 such boards (SD 1.7),
  so 10 is about 4 SD above the mean, and the one-sided 5% test at 1/30 (cut 16) is conservative.
  The count is printed beside the verdict. **The verdict is the table row's decision line: ≤ 10
  holds, > 10 fails** (rev 1.2; at rev 1.1 this note ended "the verdict is the test's", which
  contradicted the table row, and the table row prevails, Warren 14:01:36 UTC). The one-sided 5 %
  test (cut ≥ 16) is printed beside it and decides nothing.
- **P4 withdrawn; P4′ registered (Zcode, the author).** P4 as posted, "every passing board chooses
  λ = 1", is withdrawn in the author's words above. Ark and Johnny had proposed keeping P4 with an
  "expected to fail" note; the author's withdrawal prevails, and their view is recorded here. P4′
  is written knowing the seen 43 of 46 (93.5 %).
- **P5 (Ark, Q-A1)** stays on failures, not on FF-sel boards, with thresholds drafted from the seen
  53/56 = 0.946 and 53/53. **The count of FF-sel boards among the λ_c = 100 boards is printed beside
  it** (Ark's "52 of 56" on the seen set). P5(ii) nearly follows from P2a (Ark): a fit-side failure
  that is FF-sel has a passing fit at λ = 1, so its λ_c is not 1, and on the seen set λ took only
  the values 1 and 100. So **P5 is a label, not independent evidence**.
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
| **RP6: stop** | a stop of §8 fires: before any folder, the seed or pattern assert or the prediction commit not an ancestor of HEAD (the run refuses and writes nothing); after the fits, the script-defect stop (the separator's refit not bit-equal to the registered block fit, or its λ_c not equal to that fit's λ). Rev 1.2: a disagreement of `cert`'s counts is a flag, not a stop (§2); no stop compares `cert` with a planted value, since a permuted board has none | a design error; nothing is read; when RP6 holds it is the only label |

P3, P4′ and P5 are reported as **hold / fail** lines beside the labels. They enter no label, because
none is needed to name what replicated. **Empty denominators (rev 1.2):** a prediction whose
denominator is 0 (for example P4′ with no passes, or P5 (i) with no λ_c = 100 board) is printed
"n/a" and does not hold wherever a label reads it. The withdrawn P4 is not evaluated; its count (passes with
λ_c ≠ 1) is printed as part of P4′. P2a enters RP1–RP3 as the design check it is (§6).

**Secondary outcome: does the j = 89 class reproduce?** (restated in rev 1.1 after the read of §1)
- j = 89 is SEEN as **"fit failure, FF-struct or FF-opt, not separated"**: `ceil_1_starts100` =
  0.895 < 0.90, with `cert` 0.9875 (§1).
- **J89-reproduced** if at least one certified failure reads that same row, "fit failure, FF-struct
  or FF-opt, not separated" (`ceil_1`, `ceil_1_float` and `ceil_1_starts100` all < 0.90 with `cert`
  ≥ 0.90). This is what the outcome now tests: whether a certified pattern that the registered
  fitter cannot reach at λ = 1, even with 100 starts and without quantisation, recurs on fresh
  boards.
- **FF-opt named** (`ceil_1_starts100` ≥ 0.90) and **FF-quant at λ = 1** are counted and printed
  separately. They are not the seen class and do not make J89-reproduced. All three still count in
  P2b's non-FF-sel total.
- **J89-not-reproduced** if no certified failure reads the row of j = 89.
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
| S-R3 | `cert` per pattern at CAL's registered budget (`CERT_BUDGET_REGISTERED`, CAL script 117–119), with this file's **fresh** seeds 94500–94507 (Q-J2: 94500 stage 1, 94501–94505 refinement, 94506–94507 deep). `cert_search` takes its seeds from module globals (`SEED_CERT_STAGE1`, `SEED_CERT_REFINE`, `SEED_CERT_DEEP`, CAL script 91–93, read at 399–413), so **the call runs under a scoped swap of the CAL module's globals, reusing its `swapped_globals` pattern** (439–448); no search code is copied (Q-J1, Johnny). The swap is made inside the worker that calls `cert_search`, since a swap in the parent does not reach a worker process |
| S-R4 | per board: `sep` (CAL `separator_fits`: the registered block path, `ceil_1`, `ceil_1_starts100`, float and quantised); BF_1–BF_4 block fits by `K._fit_one`; BF_1–BF_4 `ceil_1` by `bf_block_lambda1` (new for permuted boards). **Rev 1.2, as implemented:** also rule #2.1's registered block fit by `K._fit_one` (the fit that S-R6's refit is compared with; `ceiling_block` and λ_c are read from it) and N1's block fit by `K._fit_one` (for §10) |
| S-R5 | per board: the rule's CAL §6 row (`separator_reading`), the BF row (§2), every AUC object exact and `_tau` with `ulp_sensitive`, the flags `GATE_/CEIL_1_/CERT_ULP_SPLIT`, `DECODER_SPLIT_AT_LC` and `CERT_BELOW_CUT`, λ_c for the rule and each BF_r |
| S-R6 | the script-defect stop of CAL (a refit not bit-equal to the registered block fit, CAL:975–978). Rev 1.2: the separator's first fit is the refit; it is compared bit for bit with the registered block fit of S-R4, and its λ_c with that fit's λ; either mismatch stops (RP6) |
| S-R7 | P1, P2a, P2b, P3, P4′ and P5 evaluated by the thresholds of §6 (the withdrawn P4 is not evaluated); P2b's count printed beside the ≤ 10 statement and the test's verdict; P5's FF-sel count printed beside it; the labels of §7 as a list; the secondary outcome; the (iii) population table (§10) |
| S-R8 | outputs: `boards.csv` (one row per board, every column of S-R5, with the flag `CERT_COUNTS_DISAGREE` beside those of S-R5), `replication.json`, `cert_members.json`, `raw_fits.json.gz` (rev 1.2: it stays in the `--out` folder, which lives under `connectome-seed-data`; CC copies only the small outputs into the repo, as with the calibration), `REPLICATION.md`, `stdout.log`, `SHA256SUMS.txt` last and only on a completed run; `stop_record.json` and exit 1 on a stop (CAL:981–984) |
| S-R9 | refusals before any folder: the CAL script's and the B script's LF sha256 pinned; this registration's pin; **the prediction commit's hash pinned as a literal, and `git merge-base --is-ancestor <pinned> HEAD` must hold** (Warren, Q-W1); **the working directory is the repo root, for every run including `--estimate` and `--dry-run`**; a clean tree; `--out` new; CPU only |
| S-R10 | `--estimate` (times one board's tasks and one `cert`, scales to N) and `--dry-run`, as the CAL script has them (1159–1207, 1265–1273) |

**Tests:**
- S-R1 equality with `perm_ref_y` on three seen seeds.
- The seed and pattern asserts refuse a seen seed and a seen pattern.
- `separator_reading` rows reproduced on synthetic inputs, including the at-the-cut case.
- The BF row table.
- The flags, including `DECODER_SPLIT_AT_LC` on j = 49's seen values.
- P1, P2b, P3, P4′ and P5 and every label at their boundaries: 119, 120, 180 and 181 for P1; **10
  and 11 for P2b's decision line (10 holds, 11 fails), and 15 and 16 for the printed 5 % test, which
  decides nothing** (rev 1.2; at rev 1.1 this line had the two swapped, against the §6 table row);
  P4′ at exactly 90 % and just below.
- Rev 1.2: a `cert` count disagreement is flagged `CERT_COUNTS_DISAGREE` and the run completes; the
  S-R6 stop fires on a refit mismatch and on a λ_c mismatch.
- **The `cert` seed swap restores the CAL module's globals** (`SEED_CERT_STAGE1`,
  `SEED_CERT_REFINE`, `SEED_CERT_DEEP` equal 93300, 93301–93305, 93306–93307 after the call, also
  when the call raises) (Johnny, Q-J1).
- **The swap reproduces the calibration's `cert` on board z:** with CAL's seeds swapped in, the
  swapped call gives the same result as CAL's own `cert_search` on board z (at the tiny test budget),
  so the swap changes nothing but the seeds (Johnny, Q-J1).
- The prediction-commit refusal: a pinned hash that is not an ancestor of HEAD, and a run launched
  outside the repo root, are each refused before any folder.
- The refusals.
- **The seen board j = 89** (from `permuted_reference.csv` and the `ceil_1_starts100` = 0.895 read in
  §1) gives "fit failure, FF-struct or FF-opt, not separated", and counts as J89-reproduced.

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

**As implemented (rev 1.2).** N1's block AUC is that of N1's own block fit by `K._fit_one` (S-R4).
Passes at a λ other than 1 and 100 are printed in a third table when any exist. All three tables
count certified boards only.

## 11. Open questions (each with a recommendation; rev 1.1 marks those resolved)

**For Ark.**
- **Q-A1.** P5 counts failures among λ = 100 boards, with thresholds (i) ≥ 90% and (ii) ≥ 95%. Your
  "52 of 56" counted FF-sel boards; the failure count is 53 of 56. *Recommendation:* keep P5 on
  failures, with the thresholds as drafted, and print the FF-sel-only count beside it.
  *Resolved (rev 1.1):* as recommended; P5 is marked a label, not independent evidence (§6).
- **Q-A2.** Should j = 89's `ceil_1_starts100` be read now from the calibration's raw fits (it is on
  disk, in the `sep` record of `perm:89`) and recorded as seen before the prediction commit? It
  would tell whether the seen case is FF-opt or FF-struct/opt. *Recommendation:* yes. It is
  post-data on a seen board, costs no fit, and sharpens J89's definition; read it by a script
  named in the chat, before the commit.
  *Resolved (rev 1.1):* read by `j89_read.py`: `ceil_1_starts100` = 0.895, so j = 89 is "FF-struct or
  FF-opt, not separated" (§1); J89 restated (§7).

**For Johnny.**
- **Q-J1.** How should `cert` get the fresh search seeds (S-R3)? The options are a scoped swap of
  the CAL module globals, or a thin copy asserted equal. *Recommendation:* the scoped swap, with the
  test that the CAL globals are restored and that the swap reproduces CAL's `cert` on board z. No
  search code is duplicated.
  *Resolved (rev 1.1):* the scoped swap, with both tests (§8, S-R3).
- **Q-J2.** Fresh `cert` search seeds (94500–94507) or CAL's 93300–93307? A search seed makes no
  data, so reuse would keep the instrument identical. *Recommendation:* fresh, so that the one
  rule "no seed reused" holds without exceptions.
  *Resolved (rev 1.1):* fresh, 94500–94507.

**For Warren.**
- **Q-W1.** Is the prediction-commit refusal (S-R9: the prediction commit must be an ancestor of
  HEAD) the right way to enforce your rule, or is a hash in the manifest enough? *Recommendation:*
  refuse. A manifest hash only records what a refusal enforces.
  *Resolved (rev 1.1):* the hash pinned in the script, `git merge-base --is-ancestor <pinned> HEAD`
  enforced, every run from the repo root (§6, S-R9).
- **Q-W2.** P2b's threshold (≤ 15 of 300) is a one-sided 5% test of "≤ 1 in 30". Is a test the
  reading you want, rather than the plain "≤ 10 of 300"? *Recommendation:* the test. At a true rate
  of exactly 1/30 the plain count fails about half the time.
  *Resolved (rev 1.1), Warren's wording:* the prediction is ≤ 10 of 300 and, in Warren's own words
  (14:01:36 UTC), "if > 10, the prediction is refuted": 10 is the decision line (CC, rev 1.1). The
  one-sided 5% test (cut ≥ 16) is printed beside it and decides nothing; 10 is about 4 SD above the
  seen rate's mean (§6).

**For Zcode.**
- **Q-Z1.** P4 is contradicted by the seen set (3 of 46 passes at λ = 100; §1). Keep it verbatim, or
  restate it with a tolerance, for example "≥ 90% of passes choose λ = 1", before the commit?
  *Recommendation:* keep (4) verbatim as posted, since it was your prediction. If you want the
  tolerant form, post it as a separate prediction (4′) before the commit, stating that the seen
  count was known.
  *Resolved (rev 1.1), Zcode's decision as the author:* P4 withdrawn before the prediction commit and
  P4′ (≥ 90 % of passes choose λ = 1) registered; Ark and Johnny's "keep with an expected-to-fail
  note" is recorded, and the author's withdrawal prevails (§6).
- **Q-Z2.** Is 0.5×–2× the rule's rate your meaning of "the same order" for P3, per BF_r?
  *Recommendation:* yes, per r, with the 2 × 2 table (rule failure × BF_r failure) printed.

**For Mike.**
- **Q-M1.** N = 300, about 12.5 min estimated (≤ 19 min with margin) on the CPU. *Recommendation:*
  approve N = 300. It is under your 30-minute line, and it gives P1 and P2b their power (§4). If
  `--estimate` reads over 30 min, the run waits for your word.
- **Q-M2.** The run order: reviewers' yes → the prediction commit (this file alone) → the script and
  its tests, reviewed → the pin → your order → the run → a blind review. *Recommendation:* approve
  this order. It is the calibration's order, plus the separate prediction commit.
