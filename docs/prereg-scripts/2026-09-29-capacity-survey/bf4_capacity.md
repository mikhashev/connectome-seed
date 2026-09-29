# BF_4 can reach AUC 1 on every 5 × 8 block pattern

Carrier for the claim in `docs/plans/2026-09-29-failed-fit-branch-calibration-registration.md`
(rev 1.4, §8), asked for by Johnny's review of rev 1.3 (DPC Research chat, 2026-09-29 05:35:45 UTC).
It is a design computation on constructed boards and is not a value of any registered run. The
check script is `bf4_check.py` and its output is `bf4_check_out.txt` (hashes in this folder's
README).

## 1. The class

BF_r is `harness.fit_bf` (`results/genome/c6/harness.py:710–733`), decoded by
`decoders/bf_decode.py`. On the cells it scores, its existence logit is

    z_st = O_st + Σ_{k=1..r} U_sk V_tk,

with the following parts:

- **O** is N1's logit grid, `c + a_s + b_t`. It is fitted first by `fit_n1` (ridge, `harness.py:350–399`)
  and held fixed (`_n1_logit_grid`, `harness.py:697–699`). **O is additive: it cannot represent
  anything that a_s + b_t cannot.**
- **U** and **V** are the rank-r factors from `bf_als` (`harness.py:666–697`), penalised by
  ½λ(|U|² + |V|²) at the nested λ.
- **Decode:** `bf_decode.py` adds `U_s · V_t` to N1's logit after the harness's float32 cast
  (`cast`, `harness.py:273–278`). There is no quantisation.

**Capacity.** The *capacity* is the supremum of the in-sample AUC over all U, V of rank ≤ r, with O
held at whatever N1 gave. It is a property of the class, not of any fit: the penalty and the nested
λ decide which member the fitter reaches, not which members exist.

## 2. The claim

**For every 0/1 pattern Y on 5 source rows × 8 target columns that holds at least one present and
one absent cell, and for every additive offset O, some member with r = 4 orders every present cell
above every absent cell (AUC = 1).** The claim needs no condition on row counts, column counts or
rank.

## 3. The argument

Write each column t of Y as a sign vector p_t ∈ {−1, +1}^5 (+1 = present).

1. **A hyperplane that avoids the columns.**
   - A board has at most 8 distinct column patterns; {−1, +1}^5 has 32.
   - The pairs {w, −w} number 16, so at least 8 pairs have neither member among the columns.
   - Pick such a w ∈ {−1, +1}^5.
2. **U spans w⊥.** Let U = [w_5 e_i − w_i e_5]_{i=1..4}, a 5 × 4 matrix.
   - Its columns are orthogonal to w and independent (column i has w_5 ≠ 0 in row i, and 0 in the
     other first four rows).
   - So its column space is exactly the hyperplane w⊥.
3. **Each column pattern is reachable in w⊥.** Take a column pattern p (p ≠ ±w).
   - p ∘ w has both signs. Let P⁺ = {s : w_s p_s > 0} and P⁻ = {s : w_s p_s < 0}; both are
     non-empty.
   - Set x_s = p_s / |P⁺| for s ∈ P⁺ and x_s = p_s / |P⁻| for s ∈ P⁻.
   - Then sign(x) = p, and w · x = Σ_{P⁺} 1/|P⁺| − Σ_{P⁻} 1/|P⁻| = 1 − 1 = 0, so x ∈ w⊥.
   - Put V_t = (x_1, …, x_4) / w_5. Then (U V_t)_s = x_s for all five rows (row 5: −Σ_i w_i x_i / w_5
     = w_5 x_5 / w_5 = x_5, using w · x = 0 and w_5² = 1).
4. **The additive offset is dominated.** Let M = U Vᵀ, so M_st has the sign of the cell and
   |M_st| ≥ δ = min |x| > 0.
   - For any additive O with range R = max O − min O, take K > R / (2δ).
   - Every present cell then scores ≥ min O + Kδ, which is more than max O − Kδ, the most any absent
     cell scores. So AUC = 1.
   - K·U has rank 4, so the member O + (K U)Vᵀ is in the BF_4 class.
5. **The offset contributes nothing needed and can prevent nothing.** O is fixed and additive, and a
   large enough K overrides any finite O. So N1's fit, whatever it is on a given block view, does not
   limit BF_4's capacity. Conversely, O is not used by the construction.

**What the claim does not say:**
- It does not say that BF_4's *fit* reaches AUC 1. The fit is penalised at the nested λ, and its
  choice can collapse to λ = 100, as rule #2.1's did on block B.
- It does not say anything about BF_1–BF_3. Rank 3 spans hyperplanes of codimension 2 and does not
  reach every orthant pattern in general.
- On block B's real block, BF_2–BF_4 had `ceiling_block` 1.0 (`RESULT.md` lines 33–35). That is
  consistent with the claim but is not evidence for it.

## 4. The check (`bf4_check.py`, exact rational arithmetic)

**Boards** (seed `default_rng(20260929)` for the constructed ones):

| set | count |
|---|---|
| the 571 survey 5 × 8 boards (`survey_boards.csv`) | 571 |
| boards with the row profile 2, 6, 4, 4, 3 (block B's real row counts), cells drawn at random | 50 |
| boards with random unequal row counts 0–8 (at least one present and one absent cell) | 200 |
| edge cases: one full row with the others empty; one full column; a hand-made board | 3 |
| **total** | **824** |

**Method.** For each board the script builds w, U, V and x as in §3, and asserts w · x = 0 and
U V_t = x exactly. It then scores two offsets:
- O = 0;
- a random additive O with integer a_s, b_t ∈ [−10, 10].

Each is scaled by K = R/(2δ) + 1 and counted with `fractions.Fraction`.

**Result** (`bf4_check_out.txt`): **0 of 824 boards × 2 offsets fall short of AUC 1.**
- The constructed term has rank 1 on 2 boards, 2 on 8, 3 on 125 and 4 on 689, never above 4.
- The smallest margin δ over all boards is 1/4.
