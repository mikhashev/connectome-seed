# Capacity survey of the class a_s + b_t + u_s v_t on small boards

**What this is.** A design computation on constructed 0/1 boards, cited by
`docs/plans/2026-09-29-failed-fit-branch-calibration-registration.md` (rev 1.8: §2, §2a, §4, §4a, §5b, §6, §6a, §8, §16).
It is **not a value of any registered run**. It reads no bank, neither flyvis-65 nor any world of a
registered arm, and it decides no label.

Every number is a **lower bound** on the capacity of the free class `a_s + b_t + u_s v_t`:
- the class has free parameters, no penalty, no N1 offset, no W term and no quantisation;
- each number is the best in-sample AUC found for an explicit member;
- that member is stored and rechecked exactly;
- nothing here shows that the class cannot do better.

## When and by whom

| run | where | when | what |
|---|---|---|---|
| **the rerun (top level; cited)** | CC's scratchpad, copied here by CC | about 31 min of compute (169 + 254 + 536 + 891 s by the log); finished 2026-09-29 05:21 +07:00 = 2026-09-28 22:21 UTC (file times) | the same boards and seeds as the first run; exact counting; every stored member rechecked with `Fraction`; a deeper search on the lowest boards |
| **the first run (`prev/`)** | the same | 2026-09-28, about 21:11–21:35 UTC | kept only because rev 1.2 of the registration cited it |

**The first run is superseded:**
- its float32 counting with a 1e-6 tie tolerance;
- its 8 × 8 minimum of 887/1,024 (0.8662);
- its 5 × 8 minimum of 376/400.

The rerun counts exactly and gives 892/1,024 and 377/400.

CC reran `verify_members.py` independently: 1,052 members rechecked, 0 mismatches. This README was
written by a CC subagent, which reran nothing of the survey; it wrote and ran `bf4_check.py` and `fc_anchor.py` (below).

## Method (the rerun)

- **Search dynamics** (`survey.py`, `best_auc`): Adam (learning rate 0.05) on the sum of sigmoids of
  score differences between present and absent cells. The temperature anneals from 1 to 0.01, and
  the arithmetic is float32.
- **Counting.** Every 100 steps, and at the end, the parameters are cast to float64 and the pairs are
  counted **exactly**: a win is d > 0 and a tie is d == 0, with no tolerance. The best member per
  board is kept as float64.
- **Recheck.** Every stored member is recounted with `fractions.Fraction`, i.e. exact rational
  arithmetic on the stored floats (`frac_count`). The log prints the mismatches, and every list is
  empty.
- **Stages per shape** (`run_survey.py`, `stage`):
  1. every board with K = 100 starts, 500 steps, seed 11;
  2. the 10 lowest boards with 5 reruns of K = 500, 500 steps, seeds 100–104 (K = 300 on 13 × 13);
  3. the 10 lowest after stage 2 with 2 deep reruns of K = 500 (300 on 13 × 13), 1,200 steps,
     seeds 200–201.

  A board's value is the best over all stages.
- **Boards.** `numpy.random.default_rng(2026)`, generated in the file's order. The order is identical
  to the first run's.
- **Flagged "unstable".** A board whose stage-2 and stage-3 counts spread by more than 2/400 of its
  pairs.
- **`auc_search.py`** (board F and the RL2 control):
  - sigmoid surrogate with 2,000 starts × seeds 0–2;
  - logistic loss with seeds 0–1;
  - a discrete local search (a, b, v in −3..3, u in {−1, 0, 1}) with `default_rng(0)`, 600 restarts
    on F and 200 on RL2.

  Counting is exact float64 and the best member is rechecked with `Fraction`.

## Results (`survey_log_v2.txt`; per board in `survey_boards.csv`; members in `members_*.json`)

**5 × 8, 4 present per row: 571 boards, 400 pairs each.**

| group | boards | min | median | max |
|---|---|---|---|---|
| random rows (`rand`) | 300 | 0.945 | 0.9875 | 1.0 |
| all 5-sets of the 7 non-constant Walsh–Hadamard rows (`WH`) | 21 | 0.9425 | 0.945 | 0.95 |
| 5 of the WH rows and their complements (`WH+-`) | 150 | 0.9425 | 0.975 | 0.98 |
| `flat` (see "Naming" below) | 100 | 0.9775 | 1.0 | 1.0 |
| **all** | **571** | **0.9425 (377/400)** | 0.985 | 1.0 |

No board is below 0.90 and none is at or below 0.85. No board is flagged unstable.

**Board F and the RL2 control** (`auc_search_out.txt`, `auc_search_members.json`):
- **F** reaches 378/400 = 0.945 (surrogate, seed 2). The `Fraction` recount gives 378. The logistic
  loss reaches 376, and the discrete search 350.5.
- **RL2** reaches 400/400 by every method.

**Larger shapes, about half present per row:**

| shape | boards | min (board) | boards < 0.90 | boards ≤ 0.85 | lowest board that is not circulant | flagged unstable (spread in counts) |
|---|---|---|---|---|---|---|
| 8 × 8, 4 per row | 220 | 892/1,024 = 0.8711 (#163, circulant) | 22 | 0 | 0.8926 | #153 (7), #158 (7), #159 (6) |
| 10 × 10, 5 per row | 160 | 2,115/2,500 = 0.846 (#138, circulant) | 17 | 3 (#138, #127, #134; all circulant) | 0.8896 | #52 (14), #123 (20), #127 (18), #129 (19), #131 (20), #134 (25) |
| 13 × 13, 6 per row | 101 | 5,728/7,098 = 0.8070 (#100, the Paley board) | 61 | 12, all circulant (the log lists them with `is_circulant`) | 0.8629 | #62 (93), #63 (59), #66 (104), #72 (46), #73 (61), #74 (40), #75 (85), #79 (48), #100 (54) |

**Sources for the table:**
- The "lowest board that is not circulant" column was checked by the subagent against
  `survey_boards.csv` with the same `is_circulant` rule. On 8 × 8 and 10 × 10 the log itself prints it
  only per group.
- The 8 × 8 "< 0.90" count is 20 circulant boards and 2 others.

## Added for the registration's rev 1.4 (2026-09-29, by a CC subagent)

These files are design computations on constructed boards; none is a value of any registered run.

- **`bf4_capacity.md`, `bf4_check.py`, `bf4_check_out.txt`: BF_4's capacity on 5 × 8** (Johnny's
  review).
  - The argument: every 5 × 8 pattern, with any row profile and any additive offset, has a BF_4
    member at AUC 1.
  - The check: 824 boards × 2 offsets (the 571 survey boards, 50 boards with block B's real row
    profile 2, 6, 4, 4, 3, 200 with random unequal rows, 3 edge cases), exact `Fraction` counting,
    seed `default_rng(20260929)`.
  - Result: 0 failures. Run with `tools/.venv` (Python 3.10, numpy 2.2.6), `PYTHONUTF8=1`, in
    seconds.
- **`fc_anchor.py`, `fc_anchor_out.txt`: the number FC stands on** (Ark's review, A1).
  - It runs rule #2.1's registered block-only path (`P.train` + `P.decode`, loaded by
    `harness.load_rule`) on a constructed bank that holds only block B's 40 cells, laid out as
    board z and as board z′. Present cells carry a placeholder offset set, which enters no
    existence term.
  - The λ grid is forced to [100], forced to [1], or left as registered.
  - **No fit reads the real bank.** Importing `harness` loads the bank's files and checks their pins
    at import, as every harness user does, but nothing is fitted or scored on them.
  - **Rev 1.6: every AUC is now taken on the B script's decode path.** That is `P.decode` →
    `p_exist` → float64 → `auc`, and N1 goes through its own decoder. Each value is printed exact and
    with |d| ≤ `TAU` = 1e-9 counted as a tie, and `ULP_SENSITIVE` marks a difference. The rev 1.4
    version took N1 and the float fit from logits; those two values (0.600 and 0.555) are withdrawn.
  - Result on board z:
    - forced to [100]: **0.600000 exact and under `TAU`** (162 wins, 156 ties; not ulp-sensitive);
      the float fit is 0.480 exact against 0.600 under `TAU` (ulp-sensitive); max |u·v| 1.4e-20;
    - [1]: 1.000000;
    - registered grid: λ 1 and 1.000000.
  - Board z′: 0.600000, 1.000000, and λ 1 with 1.000000. None is ulp-sensitive.
  - N1, decoded: **0.720 exact and 0.600 under `TAU` on z** (3 levels, reproducing Ark's pin), and
    0.600 on z′.
  - Four illustrative FN boards (design seed 20260929, not the registered world seeds), at the
    forced grids only:
    - the quantised path is not ulp-sensitive on any;
    - the float fit and N1 are ulp-sensitive on one board.

## Added for the registration's rev 1.8 (2026-09-29, by a CC subagent): M8

- **`m8_profile_check.py`, `m8_profile_out.txt`, `m8_profile_boards.csv`,
  `m8_profile_members.json`: M8, the design check on block B's real row profile.** Mike approved it
  (DPC Research chat, 2026-09-29 08:14:45 UTC). It is a design computation, not a world, and not a
  value of any registered run.
  - **Boards.** 50 boards of 5 × 8 with rows 2, 6, 4, 4, 3, the same boards `bf4_check.py` draws. They
    are reproduced by the same `default_rng(20260929)` calls, and `bf4_check.py` is imported by
    neither script and not modified.
  - **Printed per board.**
    - `cert`: the free-class search from `survey.py`, with design seeds 2026092901 (stage 1) and
      2026092902–2026092906 (reruns). The stored member is recounted with `Fraction`.
    - N1 decoded.
    - Rule #2.1's registered path at forced lambda = 100 (quantised and float) and at lambda = 1.
    - Every AUC exact and with |d| <= TAU as ties.
  - **Results.**
    - `cert` min 0.9825, median 1.0.
    - Forced lambda = 100, quantised: min 0.7005, median 0.8039, max 0.9048 (board 41 >= 0.90).
    - `ceil_1` min 0.9123.
    - No AUC is ulp-sensitive.
  - **Run.** `tools/.venv`, `PYTHONUTF8=1`, stdout redirected; 379 s for the recorded run. A first
    run (428 s) came before the script's file writes got `encoding="utf-8"`. The rerun reproduced
    its CSV and JSON byte for byte. Every output is ASCII with LF line ends; the hashes below were
    recomputed from the bytes on disk.
- **Encoding note on `bf4_check.py` (not changed).** It opens `survey_boards.csv` with the platform
  default encoding. That is harmless here, because the file is ASCII. The file is kept as committed,
  since its hash and output are recorded. New scripts open every file with `encoding="utf-8"`.

## Files (sha256 of the bytes as stored; `.gitattributes` holds `* -text`, so git stores them as written)

| file | sha256 |
|---|---|
| `m8_profile_check.py` | `82b1dfd0cb97d4edb786f4b7f1d0d8719b9c898d1fa2783d834842bb69d0e147` |
| `m8_profile_out.txt` | `e22f641d9e02cd0b0a679f58ee6f0253eeba410d041de11834531d29a62631e7` |
| `m8_profile_boards.csv` | `716fbabd7e27d081690ea0f75c2d4beaf93899b995c8ce45824f1c49e77f3e88` |
| `m8_profile_members.json` | `c5f3cb513b28ef3e7027856882394c1ca56ff4b338d493f95176ffc3d89c220f` |
| `bf4_capacity.md` | `e8c37a1a6916867bc9ca402608ddbe5f8bccc81447e76bac804e35136591faf7` |
| `bf4_check.py` | `8a747563bbdfc740da6d076947be5cf63378f9de1ad4e00a4d56f74d245257ea` |
| `bf4_check_out.txt` | `986529a3c88565d7e921af37b63bb0c7eb1824cf2cd2299b705c2529cb0e337d` |
| `fc_anchor.py` | `171a2bbff2e37a6fa22d0b112b3c904519e8e81344ae2828f02ca2fa68fd49f3` |
| `fc_anchor_out.txt` | `17cec83f557946bc2db587060fae5e2ad6ff3248b2998e1faaf9fcdc606bd0c8` |
| `.gitattributes` | `705fd4d6451a31d36b3df7de96f83f30ac976c9b4a6d1e51671d8e2f33e2d0da` |
| `auc_search.py` | `c605a6555afec91af311d39e4ae4e5a4fa9ac4db403204d6bcad34764518899e` |
| `auc_search_members.json` | `6f188ae856f8135d681930f40c77bd443bd86fe0fdf1b96f14cf921e767b73f9` |
| `auc_search_out.txt` | `1f3f1caefbcffd1e3da4030d80e1fe3c17bb1615e091e2d380b8d75caa2e2803` |
| `members_5x8.json` | `a3aec57e1b7e0738fe3d02245eb579e9940cdfa330fc43de5f539c98818c9b30` |
| `members_8x8.json` | `748dd1824c5782def7caf54642ba8abcecc91b18b30b9e64cd4b801deb7a222a` |
| `members_10x10.json` | `433d14306c89759b92788cc03874742ad967e8844c3a85c792087f7b8de1aa27` |
| `members_13x13.json` | `ab7f974894cf92cd69998e6dd48aa3f5dc6912873a25218027e26b92123f80db` |
| `run_survey.py` | `77552190a391828d7f0758cbe9c5fb167e1b1f53ad33d6e171251425734e149a` |
| `survey.py` | `0bbdd15cc5f1c9a2bc5b31b33cf36c7650eb8100d71b6535510e8d930b77c000` |
| `survey_boards.csv` | `cdaeb7df4474b40b4d310d605a24f5553063c5fff7cfce77e4001bc7b36b1db3` |
| `survey_log_v2.txt` | `6c0b580f89bc6f89322ca37a9232d6fdceb883714c55cec33b028a0f18a97d78` |
| `verify_members.py` | `31818eaa7137999e399896ef4959a10491cc7c382fc388096fa9fce89ac316d4` |
| `prev/auc_search.py` | `258ff53b56e643ac44f53eb25c735fbacf9b255d91cba25a2c401f7960f9d7a3` |
| `prev/run_survey.py` | `0fed3f4b4409cd8b74b1b8690ca78b6a6a9e5fc8365aad85d0110077b072e220` |
| `prev/survey.log` | `0d37170c17801bb3d2b82d68fde30ef48a6ec8d66af0a7f1e3eef9be632d6ce2` |
| `prev/survey.py` | `84fbc864552b216049a675060fb4090e86bbb2276c09e0efc984476435a4b30a` |

(This README is not in the table.)

## Limits and remarks (read before citing)

1. **Lower bounds only.** A low value may be a search miss. The unstable boards above show that the
   search does not always find its own best: on 13 × 13 the spread reaches 104 of 7,098 pairs.
2. **The search dynamics are float32; the counts are not.** A count is exact for the stored float64
   member, which is the witness. The float32 dynamics only affect which members are found.
3. **Scope.** All 5 × 8 boards hold 4 present per row. Boards with unequal rows (block B's real
   block had 2, 6, 4, 4, 3) were not surveyed.
4. **The class is not the fitter.** Rule #2.1's registered fit is penalised, sequential (N1 first) and
   quantised to 5-bit symbols (registration §3). The class here has none of that.
5. **Naming.** `flat_board` / group `flat` makes 1–2 **always-present** and 1–2 **never-present**
   columns, with the rest random. It is not the "flat columns" (column counts as even as possible) of
   the registration's rev 1.1 board F.
6. **A local path in an output.** `auc_search_out.txt` line 11 is a numpy overflow warning (from
   `exp` in the logistic-loss gradient; harmless to the counts) that prints the scratchpad path of
   the script as it ran.
7. **Line endings.** `auc_search.py` and `run_survey.py` have CRLF line ends and the other files LF.
   `.gitattributes` keeps both as written.
