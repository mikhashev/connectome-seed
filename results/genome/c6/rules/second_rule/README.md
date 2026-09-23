# The second rule: fitting code, gates and the post-run script

This directory implements the rule registered in `docs/plans/2026-09-23-second-rule-proposal.md`
(commit `c3f996d`): N1 + a rank-1 bilinear term + field groups (X_e) and target-side offset sets
(X_o). The proposal's §2.2 is the model, §2.3 the learner, §2.4 the data arrays, §2.5 the gates,
§1 the timing cap, and §5.2 and §6 the post-run outputs.

**Status.** Mike approved steps 4–5 (DPC Research group chat, 2026-09-23 14:40 UTC): the rule
code, the gates and the timing decision. He has **not** approved the C6 run on the real bank.

- The rule has **not** been fitted or scored on the real bank or on any real fold.
- No held-out number exists for it on the real bank.
- The harness has not been invoked with `--rule` for it.
- Non-synthetic data this code has touched: **shuffled bank 0** (`harness.shuffled_bank(REAL, 0)`)
  only, for G-bf (predictions compared, no score) and for the timing (fit time only, no score).
  The gate banks GB1 and GB0, and the self-test bank ST0, are synthetic: existence, signs and
  template choice are drawn, and offset sets and counts are copied from real non-empty cells, as
  the proposal's §2.5 specifies.

| file | what it is |
|---|---|
| `fit.py` | The learner, which is not charged. It is also the harness plug-in module: `NAME = "second_rule_r1"`, `PROGRAM_FILES`, `RANK = 1` and `fit(view, starts=10)`. The harness passes its `--starts` value to `starts`. |
| `decode.py` | The decoder. It is charged under C6 A5 and has no comments, because comments are charged. |
| `gate_banks.py` | The gate banks GB1 (signal) and GB0 (null) of §2.5, and the self-test bank ST0. |
| `gates.py` | The seven gates of §2.5, run once; writes `gates.json`. |
| `timing.py` | The timing cap of §1 on shuffled bank 0; writes `timing_k10.json`. |
| `post_run.py` | Runs after the record is committed: spread-log check, BF_1–BF_4 and RP_1 refits, per-type leave-one-type-out, the mandatory BF line and the tie-band reading in `RESULT.md`. Not run on the real bank. |
| `test_fit.py` | Unit tests on synthetic data only. |

Run everything from the repository root with `tools/.venv/Scripts/python.exe`.

## The rule in the harness's terms

- **Rank.** `RANK = 1`, the registered arithmetic r = round((130 + 16) / 130) = 1 (§1). The
  harness uses it directly, not its fallback count.
- **Data** (the §2.4 table; names and shapes are charged on top):

| array | contents | A5 cost at the caps |
|---|---|---|
| `Q__sym32` | a, b, u, v, α, β, A, B (8 × 65), W (16, row-major, rows = source group), m (one per library offset, in sorted (du, dv) order) | 3,008 |
| `c` | c, then the scales of (a, b), (u, v), (α, β), W, m; every value is float32 already | 210 |
| `L` | the library: per set its length, its du's, its dv's; sets in the order they were added | ≤ 800 |
| `e__sym8` | e (65), then f (65) | 466 |
| `s` | sign; True means +1 | 91 |

- **Decoder.** `decode.py` compresses to **494 bytes = 3,952 bits** under A5's lzma rule, against
  the 600-byte cap (G-size). It imports numpy only. So DL(rule) ≤ 3,008 + 210 + 800 + 466 + 91 +
  3,952 = **8,527 bits** at the caps, under the registered worst case of 9,375 and the one-tenth
  limit of 9,481.2.
- **What the decoder computes**, per cell (s, t):
  1. G(type) = 3 if `stride_u` > 1, else the role code (0 input, 1 intermediate, 2 output).
  2. logit = c + a_s + b_t + u_s·v_t + W[G(s), G(t)]; p = σ(logit).
  3. The offset set is library[B_t] if f_t > e_s, else library[A_s].
  4. Each offset o of the set gets n̂ = expm1(m_o + α_s + β_t).
  5. The sign is the stored boolean of the source.
- **The spread log** (§6). If the environment variable `SECOND_RULE_SPREAD_DIR` holds a
  directory, every call to `fit()` writes **one file** there, named
  `<bank name>__<first 16 hex of sha256 of the 65 × 65 training mask>.json`, written to a
  temporary name and renamed, so no two processes ever share a file. When it is unset, `fit()`
  writes nothing, and its data is byte-identical either way (`test_spread_log_one_file_per_fit`).
  The file holds the fit's diagnostics: λ and the inner log-likelihood per λ, the float W, κ, the
  penalised objective before and after the coordinate-descent pass and after c's refit, the
  number of moves, α_src and α_tar, the library's size and cost, the data bits, and e and f.
  1,341 fits make 1,341 distinct names (real: 10 + 65 + 1; each of 99 shuffled banks: 10; each
  of 25 dial banks: 11).

## Readings (marked [R n] in the code)

The proposal's text was followed wherever it decides. The list below gives each place where it
does not decide, and the reading taken. None was chosen after seeing any score.

1. **[R1] The harness's algorithms are imported, not copied.** §2.3 names `fit_n1`, `bf_als`,
   the nested schemes of BF_r and N_EB and the ridge logistic. `fit.py` imports them from
   `harness.py` (read-only), so "exactly as the harness does it" holds by construction; G-bf checks
   it. O is the harness's `_n1_logit_grid` (N1's terms after the float32 cast), as in `fit_bf`,
   so that round 1 step (i) is exactly the harness's BF_1 fit at that λ.
2. **[R2] The W step's rows.** The ridge logistic for W runs over the training cells in (s, t)
   row-major order. The order does not change the optimum.
3. **[R3] The scales are float32.** Each scale is max|x| · 16/15 rounded to float32 before the
   symbols are chosen, because the harness hands the decoder float32 values (A5). The learner's
   objective is computed with the values the decoder will see.
4. **[R4] The training loss** in the coordinate descent and in c's refit is the unclipped
   log-loss in nats, log(1 + e^z) − y·z, as BF's training objective (up to BF's 1e-300 guard).
5. **[R5] "The penalised training objective"** of the coordinate descent is the sum of the three
   fits' own objectives: training log-loss + ½(‖a‖² + ‖b‖²) (N1's λ = 1; c unpenalised) +
   (λ/2)(‖u‖² + ‖v‖²) at the chosen λ + (μ/2)‖W‖². It is evaluated on the rescaled u and v (after
   κ), which is the quantity stored.
6. **[R6] "Each symbol tries q ± 1".** Both moves are evaluated; the better one is kept if the
   objective falls by more than 1e-9; a tie between them goes to q − 1. Moves outside 0..31 are
   not tried. Each accepted move updates the state the next symbol sees.
7. **[R7] The library inside N_EB's nested α choice.** In each inner fold the candidate
   restriction is the library **rebuilt on that inner fold's training cells** by the same step-1
   procedure, just as N_EB's own nested scheme takes its candidates from the inner training
   cells. The final choice uses the library of the whole training view. The target side uses the
   same inner folds and its own α.
8. **[R8] The gate banks' draw shapes.** Step 2 draws `integers(0, 604, size=(65, 2))` (column 0
   the source template, column 1 the target template); step 5 draws u₁ as a (65, 65) array, then
   u₂, then the index array, each row-major in (s, t). The proposal fixes the order of the five
   steps, not the array shapes inside a step. GB0 makes the same draws and then uses W* = 0 and
   π_t = 0.
9. **[R9] Sign.** One boolean per type: N1's per-source majority, and for a source with a tie or
   no cell, N0's training majority (a tie there gives +1), exactly as `n1_decode` resolves it.
   `test_sign_equals_n1_everywhere` checks the equality on every cell.
10. **[R10] The bank name in the spread-log file name.** The harness hands `fit()` no bank name,
    but §6 names the file by it. `fit.py` reads `bank.name` from the caller's frame
    (`Predictor.train(self, bank, train_mask)`) and uses it for the file name only. Without the
    name, the five f = 0 dial banks and the real bank would give identical training views and
    colliding names. The training mask's sha256 is rebuilt from `view.cells`, which the harness
    cuts from exactly that mask.
11. **[R11] Rounding to a symbol** is numpy's `rint` (half to even), then clipped to 0..31.
12. **[R12] "A 5-bit symbol on [0, max m]"** is the 32-point grid value = max m · q / 31, so both
    ends are representable, as for the symmetric step.
13. **[R13] c is refitted in float64** by Newton to |gradient| < 1e-8 (the harness's Newton
    tolerance) and then stored as float32.
14. **Gates at k = 10.** Every gate runs at k = 10, the run's expected k. G-bf compares the
    learner with the harness's `fit_bf` **before** the float32 cast (u, v, λ and the held-out
    p = σ(O + u·v)): the cast would put about 1e-7 between two identical fits.
15. **Timing: ten fits at once.** The ten folds of shuffled bank 0 are fitted at the same time,
    one per process. The projection is the registered one: mean seconds per fit × 1,341 / the
    run's worker count.
16. **Who writes `RESULT.md`.** The harness's `rule_run` writes it (`render_md`). The harness is
    not changed. `post_run.py` inserts its block directly under the verdict line, between HTML
    comment markers, and replaces an older block if it is run again. The verdict line is not
    touched. For rule #1 the spread-log note and the multiplicity caveat were likewise added to
    the harness's `RESULT.md` after the run.
17. **"The run's attempts file".** No registered file defines it. It is read as a file in the
    run's output directory, `rule_runs/second_rule_r1/ATTEMPTS.md`, which the harness does not
    overwrite (it writes only `result.json`, `run_info.json` and `RESULT.md`). Following the
    glossary, it records **runs** and **crashed runs**, and, first, the timing-cap decision.

## Tests (synthetic only): `test_fit.py`

- `test_decoder_size`: ≤ 600 bytes, imports allowed.
- `test_rank_is_registered_value`: `RANK = 1`, and `harness.rank_of` returns 1.
- `test_data_layout_and_dl`, `test_worst_case_array_costs_match_proposal_table`: the arrays, the
  caps, and the §2.4 costs (3,008, 210, 466 and 91 bits at the worst case; 9,375 in all).
- `test_decode_matches_learner`: the decoder reproduces the quantised model and the side switch.
- `test_sign_equals_n1_everywhere`, `test_counts_are_n1_terms_on_the_step`.
- `test_coordinate_descent_never_raises_objective`, `test_determinism`.
- `test_x_off_one_round_is_harness_bf1`: G-bf in miniature on GB0 at k = 2.
- `test_library_caps_and_order`, `test_groups_from_fields` (groups of 8, 21, 34 and 2).
- `test_spread_log_one_file_per_fit`.

`post_run.py --selftest` runs every post-run step on the synthetic bank ST0 at k = 1, with a
deliberately short spread log, and checks the flag, the reproduction checks and the placement
under the verdict line.
