# The first rule: fitting code (preparation only)

This directory implements the rule registered in `docs/plans/2026-09-23-first-rule-proposal.md`
(commit `5a46886`): §2.1 the genome, §2.2 the decoder, §2.4 the fitting procedure and §4.3 the
random-label arm.

**Status.** Mike approved *preparation* (group chat, 2026-09-23 21:59 UTC). He has not approved
the rule run.

- The rule has **not** been fitted or scored on the real bank or on any real fold.
- No held-out number exists for it.
- The harness has not been invoked with `--rule`.
- The only non-synthetic data this code has touched is **shuffled bank 0**, for timing (§2.4
  allows this).

| file | what it is |
|---|---|
| `fit.py` | The learner, which is not charged. It is also the harness plug-in module: it defines `NAME`, `PROGRAM_FILES`, `RANK = 12` and `fit(view, starts=10)`. The harness passes its `--starts` value to `starts`. |
| `decode.py` | The decoder. It is charged under C6 A5 and has no comments, because comments are charged. It is explained below. |
| `test_fit.py` | Unit tests on synthetic data only. |
| `timing.py` | Timing on shuffled bank 0, in four modes: `serial`, `parallel`, `gpu` and `bound`. |
| `gpu_stage1.py` | Stage 1 in torch. It exists only for the CPU-versus-GPU comparison. |
| `timing_*.json` | The timing measurements. They contain no score of any kind. `timing_v2_*.json` are the measurements for SEARCH v2. |
| `planted.py` | Generator PG1 of the search criterion: planted tables from the rule's own model family. |
| `gates.py` | The search criterion's gates and the v1 measurement. |
| `gates_dev_*.json`, `gates_gate_*.json` | The development runs, and the single gate run. They hold scores on **synthetic and shuffled tables only**. |

Run everything from the repository root with `tools/.venv/Scripts/python.exe`.

## SEARCH v2: the search fix (option B, Mike, 2026-09-23 22:38 UTC)

**What happened, in order.**

1. The criterion was registered first: `docs/plans/2026-09-23-first-rule-search-criterion.md`,
   commit `1eca0ac`.
2. v2 was designed on the development tables only (planted PG1 3000–3009, shuffled 1100–1109).
3. v2 was declared in the proposal's appendix and committed (`abea719`).
4. The gate tables were then run once: planted PG1 2000–2019, and `harness.shuffled_bank(REAL,
   s)` for s = 1000–1019, which is outside the exam's null 0–98.

**v2 in one sentence.** Where v1 stops (a sweep that changes nothing), v2 tries an escape: a new
rule on fresh label(s), seeded from one training non-empty cell or from an existing label,
refined by greedy flips, and kept only if J falls. `fit.SEARCH = "v2"` is the default. v1 is
callable as `search="v1"` and is byte-identical to commit `05c1a8d`, which `test_v1_unchanged`
checks.

**What is frozen.** The model, the decoder (555 bytes), J, the caps, the 25-bit rule cost and
stages 2–4.

**Gates (k = 10), expected against what they gave:**

| gate | expected | got | result |
|---|---|---|---|
| positive: finds the planted rule (F1: J ≤ 1.01 × J_planted, and F2: held-out existence beats N1) | ≥ 15 of 20 | **18 of 20** (F1 18, F2 20) | PASS |
| negative: false finds on shuffled banks (held-out existence beats N1) | ≤ 1 of 20 | **0 of 20** | PASS |

**The two misses.** Seeds 2000 and 2013 beat N1 but fail F1: J is 9.8 % and 3.4 % above the
planted J.

**The same tables under v1 (a measurement, not a verdict):**

| | planted | shuffled |
|---|---|---|
| finds (F1 and F2) | 0 of 20 | |
| beats N1 on held-out existence | 8 of 20 | 0 of 20 (false finds) |
| restarts that end with zero rules | 82.5 % | 95.5 % |
| tables whose best restart has zero rules | 10 of 20 | 15 of 20 |

**Timing of v2 (shuffled bank 0, fold-0 split):**

| measurement | k = 10 | k = 3 |
|---|---|---|
| one full fit, 1 core | 7.07 s | 2.39 s |
| 1,315 fits on 1 core, projected | 2.6 h | 0.87 h |
| 1,315 fits actually run on a 32-process pool | **740 s wall** (0.21 h) | 219 s wall |
| 320 fits on a 16-process pool | 271 s wall | |

- **Against the 48-hour cap.** Every figure is far below it. The choice between 10 and 3 restarts
  is Mike's.
- **Determinism.** Fits run in worker processes are byte-identical to the same fits run serially.
- **GPU.** `gpu_stage1.py` implements v1 only, and `fit(stage1_fn=...)` refuses v2.

**What v2 does differently (reported, not a gate).**

- **Fewer rules than planted.** v2 fits use 6–8 rules where PG1 plants 12, and they often reach a
  training J below the planted genome's. The labels are not charged in J, so fewer rules over
  broader labels, plus some fitting of noise, can cost less. The same happens on the small
  unit-test instance: J 640 against 692 planted, with 7 rules and a different label decomposition.
- **Restarts converge.** They now mostly reach the same genome, because the escape is
  deterministic and data-seeded. The rules of the best and second-best restarts will therefore
  agree often. That bears on reading proposal §4.4 (ii).
- **Shuffled banks.** v2 finds 6–7 rules on them, and J falls from about 2,280 to about 1,800
  bits, but it never beats N1 on held-out existence. Degree-like structure is found, and it does
  not generalise beyond what N1 already has.

## The decoder and its budget

- **Size.** `decode.py` compresses to **555 bytes = 4,440 bits** under A5's lzma rule. The cap
  in §2.2 is 560 bytes (4,480 bits). The harness's own `program_bits` gives the same figure, and
  `test_decoder_size` checks it.
- **The margin is 5 bytes.** Any edit to `decode.py`, even a comment, has to be re-measured.
- **Imports.** It imports numpy only, and it passes `harness.check_imports`.
- **Data layout.** All values are integers, symbols or booleans, with no 32-bit reals:

| array | shape | content | bits |
|---|---|---|---|
| `E` | (65, 12) bool | expression `e_t` | 780 |
| `S` | (65,) bool | sign; True means +1 | 65 |
| `R__sym16` | (n_rules, 5) | i, j, motif, orientation g, ρ level; rows in (i, j) order | 20 per rule |
| `W__sym32` | (n_rules + 1,) | w level of each rule; the last entry is `w_0` | 5 per entry |
| `A__sym16` | (131,) | a levels (65), then b levels (65), then the ε level | 4 per entry |
| `L` | (n_motifs,) int | motif lengths | Elias-gamma |
| `O` | (n_offsets, 2) int | motif offsets (du, dv), canonical shape | Elias-gamma |
| `P__sym16` | (n_offsets,) | π weight levels | 4 per entry |

Array names and shapes are charged on top of the bits in the table.

- **Size at the caps.** 40 rules, 16 motifs and 64 offsets, with offsets within ±2 (±4), come to
  a data length of 3,627 (3,817) bits.
- **Total at the caps** is 8,067 (8,257) bits.
- **Against the limit.** Proposal §2.5 estimated ≈ 8,550 bits against a ceiling of ≈ 9,000. The
  registered DL(bank)/10 is 9,481 bits.

**What `decode.py` does**, step by step against §2.2:

1. It splits `O` and `P` into motifs by `L`.
2. It picks the fallback motif: the motif whose shape is `{(0,0)}`, otherwise the motif named by
   the most rules.
3. For each cell it finds the firing rules. Existence is `1 − (1 − ε)·Π(1 − ρ)`, clipped to
   [0.001, 0.999].
4. The winning rule is the one with the largest ρ, with ties going to the lowest (i, j). The
   decoder computes this itself and does not rely on the storage order.
5. It maps the motif by `g` (`2q` = rot^q, `2q+1` = refl∘rot^q) and sets
   `n̂ = exp(0.17·w + a_s + b_t)·π`.
6. The sign is `σ_s`.

## Tests (synthetic only): `test_fit.py`, all pass

- **`test_decoder_size`.** 555 bytes, which is at most 560, and the imports are allowed.
- **`test_d6_matches_regularity`.**
  - `image` and `canon` equal `regularity.py`'s `d6_images` and `canon_pattern`.
  - The check runs on 200 random point sets.
  - The functions are extracted from the file's source, so the module itself is not run.
- **`test_planted_recovery`.** A planted instance with 3 true labels, 3 true rules (each with its
  own motif, orientation and strength), a leak and per-source signs. It is fitted with k = 10.
  - The best J reaches the planted genome's own code length, 692.3 bits, against 3,236 bits with
    no rules.
  - The labels used by the rules are exactly the planted ones.
  - Exactly 3 rules are found.
  - Decoded through the harness's `Predictor` and scored with the harness's `score`, on held-out
    **synthetic** cells, the rule beats N1 on existence and on offset set.
- **`test_determinism`.** The same seeds give byte-identical data and identical per-start J.
  `timing.py parallel` also checks that fits run in worker processes are byte-identical to the
  same fits run serially.
- **`test_data_types`.** The data holds no floats and respects the caps. Rules are in (i, j)
  order. The random-label arm uses the frozen seed-20260923 draw.
- **`test_empty_library_decodes`.** A genome with no rules and no motifs decodes: p = ε, and every
  offset set is empty.

## Timing (proposal §2.4; shuffled bank 0 only)

The measurements are in `timing_*.json`. Shuffled bank 0 is `harness.shuffled_bank(REAL, 0)`.
Each fit uses a fold-style training split, meaning every cell whose fold is not f. The machine is
a Ryzen 9950X (16 physical / 32 logical cores) with one BLAS thread per process.

| measurement | k = 10 | k = 3 |
|---|---|---|
| one full fit (stages 1–4), fold-0 split, 1 core | 0.19 s | 0.09 s |
| 1,315 fits, 1 core (1,315 × that) | 0.07 h | 0.03 h |
| **measured**: 1,315 real fits on shuffled bank 0 splits, 32-process pool | **17.9 s wall** (264,000 fits/h) | **9.0 s wall** |
| measured: 32 fits, pool of 32 / pool of 16 | 0.51 s / 0.62 s wall | |
| measured: 320 fits, pool of 32 / pool of 16 | 4.5 s / 6.4 s wall | |
| **worst-case bound** (`bound`): 50 sweeps × k restarts, 40 rules, all labels used | 11.3 s per fit; 4.1 h for 1,315 fits on 1 core, 0.26 h on 16 cores | 3.4 s; 1.2 h on 1 core |

**Against the 48-hour cap.** Every figure is far below 48 hours, and that includes the worst-case
bound run serially on one core, which is how the harness runs its fits today. This file records
the measurement only. **The choice between 10 and 3 restarts is Mike's**, and it is not recorded
here.

**GPU versus CPU (`timing_gpu.json`).** Stage 1 is a sequential greedy search, so it cannot be
batched over the candidate toggles or flips without becoming a different algorithm (Jacobi instead
of Gauss–Seidel). `gpu_stage1.py` therefore batches only what is independent: the 16 levels of one
candidate, and the chains, meaning the restarts and several fits run in lockstep. The order of
decisions inside each chain is kept exactly.

| | CPU (1 core) | GPU (RTX PRO 4500, float64) |
|---|---|---|
| one fit, k = 10, stage 1 | 0.26 s | 3.77 s |
| 32 fits × 10 restarts batched (320 chains), stage 1, per fit | 0.21 s | 0.63 s |

- **Same results.** The GPU gives the same final state in every restart, the same number of
  sweeps, and identical fitted data (same hash). The largest J difference along any trajectory is
  4.5e-13 bits.
- **Why the CPU wins.** The GPU is slower per fit even before the CPU's 16–32 cores are counted,
  because each of the roughly 1,000 sequential steps per sweep is a handful of tiny kernels.

## Readings and deviations (marked [R n] in `fit.py`)

The proposal's text was followed wherever it decides. The list below gives each place where it
does not decide, and the reading taken. **None of them has been checked against the real bank.**

1. **[R1] "J falls".** A change is kept only if J falls by more than 1e-9 bits. This is a
   numerical guard against rounding noise in floating-point sums. It also makes the GPU and CPU
   runs identical.
2. **[R2] J uses the clipped p.** J is computed on p clipped to [0.001, 0.999], as the decoder
   outputs it (§2.2 step 2).
3. **[R3] How the initial labels are drawn.** `default_rng(seed).random((65, 12)) < 0.25`,
   drawn row-major, so the types come in index order. The text does not name the numpy call.
4. **[R4] The starting leak.** "The ε level nearest the training base rate" is read as nearest
   in absolute value, with ties going to the lower level.
5. **[R5] Re-choosing ρ and ε.** Rules are re-chosen one at a time in (i, j) order, each on the
   state the previous one left. A level changes only if it lowers J by more than [R1]'s
   tolerance. The best level is the argmin, with ties going to the lowest level. ε is re-chosen
   the same way.
6. **[R6] Filling the motif library.** "Stop adding motifs when the offset total would exceed
   64" is read as stopping at the first shape that does not fit, not skipping it and trying
   smaller ones.
7. **[R7] Aligning a symmetric shape.** For a shape with a non-trivial symmetry, the "D6-aligned"
   profile uses the lowest image index g with g(motif) equal to the cell.
8. **[R8] Anchoring π on the log scale.** π is defined only up to scale, so the most-weighted
   offset is put at level 15. Every other offset gets 15 + round(ln(π̄/π̄_max)/0.35), clipped at
   0.
9. **[R9] A rule whose shape is not in the library.**
   - The rule's most frequent shape is found with ties broken by shape string, as for the
     library.
   - If that shape is not in the library, the rule takes the motif with the highest mean, over
     the rule's won cells, of each cell's best-orientation Jaccard. Ties go to the lowest library
     index.
   - The other reading, one orientation shared by all cells, was not used.
10. **[R10] The orientation g_r.** It is the mode, over **all** of the rule's won cells, of each
    cell's lowest best-Jaccard orientation of the chosen motif. Ties go to the lowest index.
11. **[R11] Rules that win nothing, and cells where no rule fires.**
    - A rule that wins no training non-empty cell has no motif in the text. It gets the fallback
      motif with g = 0.
    - The fallback itself (a cell where no rule fires) also uses g = 0, since the text gives it
      no orientation.
    - An empty library decodes to empty offset sets.
12. **[R12] Stage 3: the ridge and the coordinate descent.**
    - The ridge has no intercept, penalises every coefficient (λ = 1e-3), and uses the won cells
      only.
    - The coordinate descent minimises the squared error over those same won cells, not over the
      fallback cells, and it leaves w_0 out.
    - A level changes only if it strictly lowers the error. So a type with no won cell on a side
      keeps level 8, as the text requires.
13. **[R13] Seeds and ties at k restarts.** k restarts use seeds 0 … k−1, so seeds 0–2 at k = 3.
    Ties in J go to the lower seed.
14. **Offsets for every cell.** The decoder returns an offset set for every cell, whatever its p,
    as N1 and PR do. §2.2's "expressed if p > 0.5" is not applied to what C6 scores.
15. **Packing.** ε is the last entry of `A__sym16`, and w_0 is the last entry of `W__sym32`. This
    saves two array names. The bits per value are those of §2.5.
16. **Flips on unused labels are skipped.** A flip of a label that no rule uses changes no cell,
    so its ΔJ is exactly 0. It is skipped, which changes the speed and not the result.
17. **Distinct labels are not enforced in fold fits.** The rule that no two labels share an
    expression set (§2.1) applies to the generation-0 genome. Fold fits do not enforce it; they
    report the count in `fit.LAST_FIT["duplicate_label_sets"]`.
18. **The random-label arm runs once.** With frozen labels and no rules at the start, every
    restart would be identical.

## Findings from preparation (the rule's own procedure; nothing adjusted)

(Finding 1 below describes SEARCH v1. It is what led to option B and SEARCH v2, above.)

1. **Restarts that stop at once with no rule.**
   - On shuffled bank 0's fold-0 split, **8 of 10 restarts stop after the first sweep with no
     rule at all**. At k = 3, only restart 0 finds a rule.
   - **Why.** No single label-pair rule on Bernoulli(0.25) random labels earns its 25 bits.
     Only seeds 0 and 7 have any candidate with a net gain (ΔJ < 0). Without a rule no flip can
     change J, so the sweep changes nothing and the restart stops, as §2.4 says it should.
   - **Synthetic instances do the same.** On synthetic planted instances (prevalence 0.2 and 0.3,
     seeds 0–2), in 4 of 6 no restart out of 10 reaches the planted code length, and many stop
     at sweep 1.
   - **Why it matters.** This bears on §4.4 (ii), the restarts-disagree reading, and possibly on
     "rule did not run". Whoever runs the rule should know it before the run.
2. **Unused motifs are kept and charged.**
   - The library is the ≤ 16 most frequent shapes among **all** won cells (§2.4). It is not
     pruned to the motifs that rules use.
   - The fold-0 fit on shuffled bank 0 has 1 rule and 16 motifs. Fifteen of them are stored and
     charged, but only the fallback reads them.
   - This follows the text as written.
3. **No hooks in the harness yet.**
   - `harness.py --rule` still exits: a rule run is not enabled.
   - The restart spread that §2.4 and §4.4 (ii) ask to record (J of every restart, and the
     best and second-best rule sets) lives in `fit.LAST_FIT`. The harness has no hook that saves
     it next to each fit.
   - No such hook was added here.

## The restart spread log (proposal §2.4 and §4.4 (ii))

The harness is not edited for this. If the environment variable `FIRST_RULE_SPREAD_LOG` holds a
path, every call to `fit()` appends one JSON line to that file. When it is unset, `fit()` writes
nothing and its data is byte-identical; `test_spread_log` and `test_v1_unchanged` check both.

The line has these keys:

- `view_sha256_16`: the harness hands `fit` no bank name, so the training view is identified by
  a hash of its cells, existence and contents.
- `n_train_cells` and `n_train_nonempty`.
- `search`, `k` and `labels`.
- `J_per_restart` and `restart_seeds`.
- `chosen_restart` and `second_restart`.
- `best_rules` and `second_rules`: each rule is `[i, j, rho_level, source-label member types,
  target-label member types]`. The member sets are what §4.4 (ii) matches rules by.
