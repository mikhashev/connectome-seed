# Rule #2.1: rule #2 with the larger offset library (fix W1)

This directory is a **new rule version**, not an edit of rule #2. Rule #2's record in
[`../second_rule/`](../second_rule/README.md) is unchanged: its code, its single gate run
(`gates.json`, two of seven gates FAILED) and its diagnosis (`DIAGNOSIS.md`).

**What rule #2.1 is.** Mike chose option (1), "rule #2.1 = S1 + W1", in the DPC Research group
chat on 2026-09-23 at 18:36 UTC. Both fixes come from `../second_rule/DIAGNOSIS.md` §5:

- **W1**, a change to the rule: offset library caps of **64 sets, 1,400 bits and 64 distinct
  offsets**, instead of 32, 800 and 48. It lives here, in the code.
- **S1**, a change to gate G-e+: judge it on the mean over 10 folds. S1 is not in the rule's
  code. It is in the gate script `gates.py`, written after the rule #2.1 registration was
  committed.

**Status.**

- The registration is [`docs/plans/2026-09-23-rule-2-1-registration.md`](../../../../../docs/plans/2026-09-23-rule-2-1-registration.md)
  (commit `15da501`). It was committed **after** this code, because the decoder's measured size
  (below) is one of its inputs.
- **The single re-gate has run: all seven gates PASS** (section "Gates" below; `gates.py`
  committed at `00047d4` before it ran; `gates.json`).
- **Not fitted or scored on the real bank or on any real fold.** Shuffled bank 0 was used only by
  G-bf, which compares predictions and computes no score. **The timing cap was not measured**, and
  **no C6 run has been made**: the registration's §9 steps 5 and 6 are not taken. The C6 run needs
  Mike's separate word.
- Banks it has been fitted on: the self-test bank **ST0** (seed 61000; `selftest_st0.json` and the
  post-run self-test), the re-gate banks GB1/GB0 of **seed 80000**, and shuffled bank 0 (G-bf).
  Not the gate banks of seed 60000 and not the diagnostic seeds (70000–70999). No other seed of
  80000–80999 was used.

## What changed against rule #2, and what did not

| file | against `../second_rule/` |
|---|---|
| `fit.py` | **Changed, W1 only:** `LIB_MAX_SETS` 32 → 64, `LIB_MAX_BITS` 800 → 1,400, `LIB_MAX_OFFSETS` 48 → 64. A and B leave `Q__sym32` and go to a new 6-bit array `AB__sym64`. Two constants follow from these changes: `NAME` becomes `second_rule_v21_r1` and `DL_CAP_BITS` becomes 9,379. The docstrings changed to match. Every other line is rule #2's. |
| `decode.py` | **Changed, W1 only:** it reads A and B from `AB__sym64`, and W and m sit 130 places earlier in `Q__sym32` (W at 390, m from 406). The model it computes is rule #2's (§2.2 of the proposal). |
| `gate_banks.py` | **Byte-identical** (sha256 of the LF text `cd12c646…`, the same value `../second_rule/gates.json` stamps). `test_gate_bank_generator_is_rule_2s` checks this. |
| `timing.py`, `post_run.py` | Rule #2's scripts. Only their paths, the run-directory name and the self-test's temporary-directory prefix changed. |
| `test_fit.py` | Adapted: every test runs on **ST0** where rule #2's used GB1 or GB0, and the layout and DL tests follow W1. |
| `gates.py`, `gates.json` | New: rule #2's `gates.py` with S1 (G-e+ on the fold mean), the gate banks at seed 80000, and two hard asserts before G-size (the pinned decoder; worst-case DL ≤ 9,481.2). Run once; see "Gates" below. |
| `selftest_st0.py`, `selftest_st0.json` | New: determinism and DL on ST0 at k = 10. No score. |

The proposal's model (§2.2), learner (§2.3) and every other constant are unchanged. That covers
μ = 1, the three rounds, the λ grid, the 5-bit and 3-bit symbols, the concentration levels, the
side switch and its tie rule, the sign and the counts. So do r = 1 and the tests of G-bf and
G-det.

## The data arrays (§2.4 of the proposal, amended by W1)

| array | contents | A5 cost at the caps | rule #2 |
|---|---|---|---|
| `Q__sym32` | a, b, u, v, α, β (6 × 65), W (16), m (one per library offset, n_m ≤ 64, sorted (du, dv) order) | 470 × 5 + 64 (name) + 22 (shape) = **2,436** | 3,008 (584 symbols, with A and B) |
| `AB__sym64` | A (65), then B (65): library indices, 6-bit symbols 0..63 | 130 × 6 + 72 + 20 = **872** | (inside `Q__sym32`) |
| `c` | c, then the scales of (a, b), (u, v), (α, β), W, m | **210** | 210 |
| `L` | the library: per set its length, its du's, its dv's | **≤ 1,400** by the cap | ≤ 800 |
| `e__sym8` | e (65), then f (65) | **466** | 466 |
| `s` | sign; True means +1 | **91** | 91 |
| **data** | | **≤ 5,475** | ≤ 4,575 |

## The decoder and the worst-case DL (measured)

**Decoder.** `decode.py` compresses to **488 bytes = 3,904 bits** under A5's lzma rule
(`harness.program_bits`, the file alone). It imports numpy only. That is 112 bytes under
G-size's 600-byte cap. Rule #2's decoder was 494 bytes (3,952 bits). The W1 decoder is
**6 bytes shorter**, not longer: it reads A and B directly from their own array, so the
`astype(int)+16` step on the 5-bit slice is no longer needed.

**Worst-case DL at the caps** (every array at its largest; the sum is an upper bound):

| item | bits |
|---|---|
| `Q__sym32` | 2,436 |
| `AB__sym64` | 872 |
| `c` | 210 |
| `L` | 1,400 |
| `e__sym8` | 466 |
| `s` | 91 |
| **data** | **5,475** |
| decode program (measured, 488 bytes) | 3,904 |
| **DL(rule #2.1), worst case** | **9,379** |
| one-tenth limit (C6 P2) | 9,481.2 |
| **headroom** | **102.2** |

**The two numbers in DIAGNOSIS §2.2, kept apart** (Ark, 18:37 UTC):

- The diagnosis estimated **9,427** bits. It assumed the same six arrays and rule #2's decoder
  (3,952 bits), and left the decoder's growth unmeasured. With the measured decoder, the worst
  case is 9,427 − 48 = **9,379**.
- **Increase over rule #2:** +852 bits on rule #2's own worst case at its measured decoder
  (8,527), which is the diagnosis's "+900" less the 48 bits the decoder saved.
- **Headroom to the limit:** 102.2 bits, not 54.

**One consequence for the registration, stated plainly.** Rule #2's §2.4 bounded DL at 9,375
bits by charging the decoder at G-size's cap: 600 bytes = 4,800 bits. Under W1 that bound would
be 5,475 + 4,800 = 10,275, which is **over** the limit. So under rule #2.1, P2's length half is
guaranteed by **the committed `decode.py` at 488 bytes**, not by the 600-byte cap. The
registration therefore fixes the decoder's sha256 (LF text `39a04901…`). G-size itself is not
changed.

## ST0 check (`selftest_st0.json`; synthetic, seed 61000; k = 10; no score)

| fold | DL | library sets | offsets | library bits | λ |
|---|---|---|---|---|---|
| 0 | 9,251 | 43 | 39 | 1,397 | 100 |
| 1 | 9,253 | 44 | 40 | 1,394 | 100 |
| 2 | 9,250 | 42 | 39 | 1,396 | 100 |
| 3 | 9,253 | 44 | 40 | 1,394 | 100 |
| 4 | 9,213 | 49 | 31 | 1,399 | 100 |
| 5 | 9,254 | 42 | 39 | 1,400 | 100 |
| 6 | 9,253 | 43 | 39 | 1,399 | 100 |
| 7 | 9,252 | 42 | 39 | 1,398 | 100 |
| 8 | 9,257 | 44 | 40 | 1,398 | 100 |
| 9 | 9,252 | 43 | 40 | 1,393 | 100 |

- **Deterministic:** two fits of fold 0 give byte-identical data.
- **Largest DL: 9,257 bits**, under the worst case of 9,379 in every fold.
- On ST0 the **bit cap binds**: every library costs 1,393–1,400 bits and holds 42–49 sets. So
  more than 32 sets are in use, and the stored indices reach 39–42.
- λ = 100 ("no bilinear term", DIAGNOSIS §1.3) was chosen in every fold. It is recorded here and
  not read: ST0 exists to exercise the code, not to measure the rule.
- `post_run.py --selftest` (ST0, k = 1) passed: every reproduction check held, and the block
  was placed under the verdict line.

The run was made on the uncommitted working tree at `cbf148b`. The file hashes it stamps (fit
`92eb6ab1…`, decode `39a04901…`) identify the code, and they equal the files of this commit.

## Gates (registration §1.1, §3 and §9; run once at commit `00047d4`, k = 10; `gates.json`)

**All seven gates PASS.** Run once, 2026-09-23 at 19:32:46 UTC, runtime 26.2 s (the script's own
clock). The two hard asserts held before G-size: `decode.py` is the pinned decoder (LF sha256
`39a04901…`), and the worst-case DL at the caps is 5,475 + 3,904 = **9,379** bits ≤ 9,481.2.

| gate | criterion | expected | got | result |
|---|---|---|---|---|
| **G-size** | decode program ≤ 600 bytes under A5's lzma rule; numpy and stdlib only | pass | 488 bytes (3,904 bits); imports ok | **PASS** |
| **G-det** | two fits of GB1 fold 0 give byte-identical data | pass | identical sha256 (`96498644…`); DL 9,202 bits (data 5,298) | **PASS** |
| **G-bf** | X off (W = 0, one round), no quantisation: (u, v) and existence predictions equal the harness's BF_1 on shuffled bank 0, 10 folds, to 1e-9 | pass | largest difference 0.0 (u, v and held-out p); λ equal in all 10 folds (100 in each) | **PASS** |
| **G-e+** (S1) | GB1: mean over 10 folds of (rule's existence margin over N1 − BF_1's) > +0.002 | pass | **+0.00652** (rule +0.02241, BF_1 +0.01589) | **PASS** |
| **G-e0** | GB0: rule's mean existence margin over N1 minus BF_1's ≤ +0.002 | pass | −0.00150 (rule −0.00381, BF_1 −0.00231) | **PASS** |
| **G-o+** | GB1: rule's held-out offset Jaccard beats N_EB's in ≥ 9 of 10 folds | pass | 10 of 10 (0.7189 vs 0.5603) | **PASS** |
| **G-o0** | GB0: rule's mean offset Jaccard minus N_EB's in [−0.010, +0.010] | pass | −0.00038 | **PASS** |

Gate banks (seed 80000, `gate_banks.py` LF sha256 `cd12c646…`, rule #2's file): GB1 has 1,148
non-empty cells (content sha256 `50ccc591…`), GB0 853 (`2798a94f…`).

Recorded, not read as a verdict:

- G-e+: the rule beat BF_1 in 9 of 10 folds (it lost fold 2 by 0.00051). Under S1 the fold count
  is not the criterion; it is stored in `gates.json` as descriptive.
- G-o0: on GB0 the rule's offset Jaccard equals N_EB's in 9 of 10 folds; fold 1 differs by
  −0.0038.
- On GB0 both the rule and BF_1 have a **negative** mean existence margin over N1.

**What a green re-gate buys** (registration §9): only that the rule finds a planted signal on a
fresh synthetic bank, so a C6 run would be readable. It says nothing about the real bank. The
timing cap (§9 step 5) and the C6 run (§9 step 6, on Mike's separate word) are **not** done.

## Readings

Rule #2's readings [R1]–[R17] (`../second_rule/README.md`) apply unchanged. W1 adds two:

18. **[R18] `AB__sym64` always exists.** DIAGNOSIS §5 says "A and B become 6-bit symbols". Its
    cost estimate kept them in `Q__sym32` up to 32 sets and moved them out only above 32. Here
    they are **always** a separate 130-symbol array, whatever the library's size. This keeps
    every array shape fixed before data except the library and n_m, as in rule #2's §2.4, and
    gives the decoder a single path. Its cost: when the library has ≤ 32 sets, the data are
    222 bits longer than the variable layout would be (872 against 650). The worst case is the
    same either way. The choice was made before any fit.
19. **[R19] `NAME` is `second_rule_v21_r1`.** A new rule version writes a new run directory
    (`rule_runs/second_rule_v21_r1/`) and names its spread-log files by it. The spread-log
    environment variable is unchanged (`SECOND_RULE_SPREAD_DIR`).

## Tests (synthetic only; ST0 and hand-made inputs): `test_fit.py`

16 tests; all pass.

- `test_decoder_size`: ≤ 600 bytes, imports allowed.
- `test_rank_is_registered_value`: `RANK = 1`, and `harness.rank_of` returns 1.
- `test_data_layout_and_dl`: the six arrays and their shapes, the caps, and DL ≤ 9,379 < 9,481.2.
- `test_worst_case_array_costs_w1`: the table above, with the decoder at 3,904 bits.
- `test_decode_matches_learner`: the decoder reproduces the quantised model and the side switch.
- `test_decode_reads_indices_above_31`: a hand-made 64-set library; every index 0..63, on both
  sides of the switch.
- `test_sign_equals_n1_everywhere`, `test_counts_are_n1_terms_on_the_step`.
- `test_coordinate_descent_never_raises_objective`, `test_determinism`.
- `test_x_off_one_round_is_harness_bf1`: G-bf in miniature, on ST0 at k = 2.
- `test_library_caps_and_order`: the A4 order, the caps, and a library of more than 32 sets.
- `test_caps_are_w1`, `test_groups_from_fields`, `test_spread_log_one_file_per_fit`.
- `test_gate_bank_generator_is_rule_2s`: `gate_banks.py` is rule #2's file, byte for byte.

Run from the repository root:
`tools/.venv/Scripts/python.exe -m pytest -q results/genome/c6/rules/second_rule_v21/test_fit.py`
