# Tool-hardening package

**Status:** SPECIFICATION — proposed 2026-09-15 by Ark, Zcode and CC from the code audit of the
diagnostics and the night tooling; execution waits on Mike's word «чини инструменты». No item
recomputes a recorded number; the null calibration is re-run once (item 14) and gets a second
line beside the first.

Structure per Ark's review 09:43: each fix carries a falsifier; grouped by urgency; rules
separated from fixes.

## A. Before the first analysis of night 3

| # | fix | what it defends | the 2026-09-15 incident it answers | where in code | status | falsifier |
|---|-----|------------------|-------------------------------------|----------------|--------|-----------|
| 1 | Seven post-evaluation invariants of `eval_rung` (`run_individual.py:550-558`) recorded into `hook_eval` and every evaluation json | that an evaluation left the model/optimizer state it found | witness left behind when the evaluator was copied — none of the six diagnostics scripts records any of the seven (002 §5h(v)) | `run_individual.py:550-558` | proposed | an evaluation json without the seven keys must be rejected by the reader |
| 2 | `assert \|hook − per_item_mean\| < tol` inside `evaluate()` (`splice_a.py:169-182`), tol expressed in lattice steps of the value's float32 lattice (2⁻¹⁶ at loss ≈ 3174, 2⁻²¹ at ≈ 1148), not in relative ppm | that the hook/per-item agreement check has a tolerance tied to the actual float32 accumulation lattice, not an arbitrary ppm figure that can silently pass or fail off-lattice | bit-identical 0.0 found by hand a day later (002 §5h bit-identity test) | `splice_a.py:169-182` | proposed | feed `evaluate()` two values one lattice step apart → must pass; 100 steps apart → must fail; today no comparison exists |
| 15 | Failed invariants set `rec["exit"] = "state_check_failed"` (`run_individual.py:571-573`, currently exit stays `"ok"` at `:635`) and `night_report.py` prints the error strings, not the count (`:149`) | that a failed invariant actually changes the run's recorded outcome and is legible, not just counted | witness without power — "the witness records but cannot veto" (002 §5h night-tooling audit) | `run_individual.py:571-573, 635`, `night_report.py:149` | proposed | inject a deliberately broken solver state (set `ds.augment = False` before the hook returns) → the run json must report `exit != "ok"`; today it reports `ok` |
| 16 | Idempotence control of the evaluator: evaluate a state twice, compare result and parameters bitwise | that evaluation does not mutate the state it measures | flyvis clamps in place on forward (`network.py:527`); the evaluator mutates what it measures | `network.py:527` / evaluator | proposed | evaluate a state with a negative synapse slot twice → parameters must be bitwise unchanged after the first evaluation; today the slot reads 0.0 |

## B. Before the new pre-registration

| # | fix | what it defends | the 2026-09-15 incident it answers | where in code | status | falsifier |
|---|-----|------------------|-------------------------------------|----------------|--------|-----------|
| 3a | `--check-constants` stage: read §2/§5 of the pre-registration and fail on mismatch with `K`, `PREREG_SOURCES`, `FLOOR_REL`, `BASIS_PREREG`, `FLOOR_ABS_PREREG`, `BOUND_ABS_PREREG` | that hard-coded constants stay identical to the registered document instead of drifting silently | constants copied, never checked against the pre-registration (002 §5h(iv)) | `splice_a.py:73-86` | proposed | edit `FLOOR_ABS_PREREG` to 38.19 → `--check-constants` must fail; today nothing fails |
| 3b | No numbers in identifier names (`n_above_floor_38.18`, `:376, 410-411`) | that an identifier cannot silently embed a constant value that drifts out of sync with the registered value it names | constants copied, never checked against the pre-registration (002 §5h(iv)) | `splice_a.py:376, 410-411` | proposed | grep source files for identifiers embedding a numeric literal that duplicates a registered constant (e.g. `n_above_floor_38.18`) → the check must fail on any match; today `n_above_floor_38.18` ships in production code and nothing flags it |
| 4 | Module grouping recomputed from the connectome in `stage_indices`, beside `PREREG_SOURCES` | that the source-type grouping used at runtime matches the connectome, not just the document's prose | code checked against the document, not the connectome (002 §5h(iv)); Zcode verified against HDF5 once by hand | `splice_a.py:73-86` / `stage_indices` | proposed | swap one source type in `PREREG_SOURCES` → the connectome grouping must disagree and the stage must fail |
| 5 | Scaled null drawn per slot in each slot's scale, beside the isotropic one | a null that respects per-slot scale, so an isotropic-vs-scaled disagreement is visible rather than assumed away | isotropic draw in raw space decided the (a) reading (002 §5g) | `splice_a.py` null-draw path | proposed | the output must carry the scaled-null field alongside the isotropic one; a reader asserting on it fails today |
| 6 | P0 / P1 / self-path as asserts with thresholds in `ablation.py` and `connectivity.py` | that these controls block a bad report instead of only appearing in it | controls recorded, not enforced — "refuses to report without them" (002 §5h(v); Ark) | `ablation.py`, `connectivity.py` | proposed | corrupt P0 (perturb one weight before the no-ablation baseline) → `ablation.py` must abort; today it records and continues |
| 7 | Min \|Δ_T\| and the count of types inside the noise band written into every profile output | that a sign-agreement claim always carries the band it was read against | sign-agreement claim reported without its noise band (002 §5f) | ablation profile output | proposed | the output must carry the min \|Δ_T\| and in-band-count fields; a reader asserting on them fails today |
| 8 | Every per-item / drop-k output labelled with its state (checkpoint 250,008, per-item path) | that a per-item or drop-k number can be traced to the checkpoint and path that produced it | registered hook at 250,000 has no decomposition, and the 250,000/250,008 gap is undeclared in outputs (002 §5e, night-tooling audit(iii)) | per-item / drop-k output writers | proposed | the output must carry the state label (checkpoint, per-item path); a reader asserting on it fails today |
| 9 | Script hash (git blob or sha256) in every output json, and a version line per table in 002 | that a result can be matched to the exact script revision that produced it | `splice_a.py` revised after the run, byte-exact version not on disk (002 §5g provenance) | all diagnostics output writers | proposed | regenerate an output json and diff its `script_sha256` against `git hash-object`; today no field exists |
| 10 | One evaluation entry point, and a test that fails if a second implementation of the evaluation appears in the diagnostics directory | against silent divergence between two copies of "the same" evaluation | two copies plus four diagnostics found in the audit (002 §5h) | diagnostics directory / test suite | proposed | add a second `def hook_eval` anywhere under diagnostics/ → the test must fail |
| 11 | The null-draw rule written into the record before any draw is evaluated (registration, not code) | that the null-draw rule (isotropic vs scaled, orthant) is a pre-registered fact, not an implementation detail that happens to decide a reading | the isotropic rule lived only in code and decided the (a) reading (002 §5g) | pre-registration document | proposed | run any diagnostic without a null-draw rule (isotropic vs scaled, orthant) stated in the pre-registration document → the run must refuse; today the code runs on whatever draw is hard-coded, without checking the document at all |
| 12 | Duplicate key = refusal, never "latest file wins" | against silently overwritten records under a reused key | incident carried from autoresearch `analyze_mi_channel.collect()` | diagnostics/night output collectors | proposed | place two files with one key → the reader must refuse; today the latest wins |
| 13 | Floor-calibration code measures and stores an independent floor per metric per state (e.g. two separate floors for the replicate state and the ablation state), never reusing one across a metric/state pair | against a floor computed for one metric/state being reused for another where it does not apply | (a)'s floor borrowed from the replicate; the ablation floor nearly reused for ρ; the floor is state-dependent (002 §5h; Ark 08:54) | floor-calibration code | proposed | reuse the floor measured for (a) at the replicate state as the floor for ρ at the ablation state → floor-calibration code must reject the reuse (mismatched metric/state key); today it accepts the reused figure without complaint |
| 14 | Null re-drawn in the non-negative orthant on the SAME 20 seeds (paired), with a separate time-constant sign control (node slots are unclamped) | that clamp censoring in the original null draw is visible by direct comparison, seed for seed | clamp censoring (002 §5g) | `splice_a.py` null-draw path | proposed — re-run once, second line beside the first | the paired re-draw: for each of the 20 seeds, the orthant draw must have zero negative synapse slots and the same seed; a divergence that persists on the same seed is then attributable to dynamics |
| 17 | Preflight in `start_night.ps1`: refuse to launch on a pending reboot (`RebootRequired` / `RebootPending` keys) or insufficient free VRAM | against a run silently killed mid-night by an unrelated system event | KB5129195 restart killed seed 2 (board entry) | `start_night.ps1` | proposed | create the `RebootRequired` key in a test hive / mock → `start_night.ps1` must refuse; today it launches |
| 19 | Provenance line for every quantity that entered the analysis through more than one formatter | against a claim at a precision its source formatter cannot support | night-1 pairwise CSVs from `night_report.py` are `r4()` 4-decimal strings (claims at 1e-5 impossible from them); the night-2 four-way CSV from `extract_night2.py` is full float — name the file for any argument at 1e-4 (002 §5h night-tooling audit(ii)) | `night_report.py` (`r4()`, `:60-64`), `extract_night2.py` | proposed | the output must carry the provenance/formatter-source field for any quantity at 1e-4 precision; a reader asserting on it fails today |

## C. Before night 3

Nothing; night 3 runs the current script unchanged.

## Rules for the repository checklist (not code fixes)

These go to `docs/CHECKLIST-research-repo.md` on Mike's word «пиши чек-лист».

(R1) Each metric brings its own measured floor, per metric and per state; inheritance is
forbidden. Bought twice on 2026-09-15: (a)'s floor from the replicate; the ablation floor nearly
reused for ρ.

(R2) Before an exact coincidence of two independently computed values is treated as evidence,
measure the base rate of such coincidences at that precision. The 0.0 of 2026-09-15: lattice
2⁻¹⁶, spread 25–46 steps, base rate ≈ 1/35, observed 1–2 %.

## Checks already verified today (no code change needed)

- The (a) margin 0.40 = ≈ 52,000 lattice steps at loss 1148 (2⁻¹⁷ = 7.6e-6), so not a rounding
  artefact (Ark 09:39).
- 3173.6400756835938 = 207,987,676 × 2⁻¹⁶ exactly (Ark 09:39).
- The (a) margin is ≈ 52,000 lattice steps — four orders above the grid — so (a)'s weak point is
  not the arithmetic but the threshold borrowed from another quantity: "the number is right, the
  instrument is wrong" (Ark 09:43).

Night 3 runs the current script unchanged; nothing here touches the numbers of nights 1–2.
