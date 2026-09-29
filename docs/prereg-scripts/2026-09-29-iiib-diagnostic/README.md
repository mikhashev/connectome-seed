# (iii-b) diagnostic on already-recorded fits

**This is a post-data diagnostic.** It was computed on fits that were already recorded: the natural
fit-failure replication's run and the failed-fit calibration's run. No fit was run, and no number
here was predicted beforehand. **Any future registration of (iii-b) is NOT blind to these numbers,
and must say so on its first line.**

- **Asked by:** the reviewers, Ark (15:00:23 UTC) and Zcode (15:18:35 UTC), DPC Research chat,
  2026-09-29. They wanted a $0 diagnostic before any registration.
- **Run by:** a CC subagent on 2026-09-29, about 15:45 UTC.
- **Compute:** read-only, under 1 s.
- **What it is not:** it decides no label, and it proposes no cut.

## The object

The object is option (iii-b) of `docs/plans/2026-09-29-failed-fit-branch-calibration-registration.md`
§13. The registration defines it as "AUC of the fitted `u_s v_t` term alone, or the full score's
AUC minus its additive part's". Zcode's words for it are "the AUC of the u.v term on N1's residual".

### What the records hold

The records hold `p` and `y` only. U, V and W are not stored. Each `sep||rule` record carries six
probability vectors:
- at λ = 1: `ceil1_p` (quantised), `ceil1_float_p` (float), and the 100-start pair;
- at the chosen λ_c: `reg_p` and `reg_float_p`.

Fresh boards and calibration worlds also carry a `block||N1` record with N1's `p`. The permuted
("seen") boards have no N1 record.

### What `p` still allows, with each premise checked on every board

- **The float logit.** It is `O + u_s v_t + W[G(s),G(t)]`, where O is N1's fixed offset (fit.py
  `fit_uvw`; `float_p` in `failed_fit_calibration.py`).
- **W on block B.** All five sources L1–L5 have the same group, so on block B W is a column effect
  `w_g(t)`.
- **The residual.** N1's `p` is sigmoid(O) on the same view. So logit(p_float) − logit(p_N1) =
  `u_s v_t + w_g(t)`.
  - Checked: after centring each column, this residual is rank 1 to 2.3e-15 on all 630 fits that
    have an N1 record.
- **The double-centred logit** equals `(u_s − ū)(v_t − v̄)`. Every additive term drops out: c, a, b,
  W's column effect, and the quantised a, b, c.
- **The carriers.** The recomputed AUCs equal the carriers' `ceil_1`, `ceil_1_float`,
  `ceil_lambda_c_float`, `n1_block` and `ceiling_block` in 1842 of 1842 comparisons.

### The readings computed (names used in the output and the CSV)

| name | object | available on |
|---|---|---|
| R0 | AUC of `u_s v_t` alone, in the fitter's own gauge | **not computable**: needs U and V. From `p`, only `u v + w_g(t)` is identified (u → u + k moves k·v_t into the column effect) |
| R1a | full AUC − AUC of N1 (additive part = O, W not counted) | fresh, worlds |
| R1b | full AUC − AUC of the additive projection (row + column means) of the full logit (W counted as additive) | all |
| R2 | AUC of logit(p_float) − logit(p_N1) = `u v + w_g(t)` (Zcode's reading) | fresh, worlds; float fits only |
| R3 | AUC of the double-centred logit = AUC of `(u−ū)(v−v̄)`, the u·v term with its additive gauge removed | all; float and quantised |

Every reading is given at λ = 1 (suffix `l1`) and at the chosen λ_c (suffix `lc`). Every AUC is
counted exactly and under TAU = 1e-9. TAU is applied on the object's own scale: logit units for R2,
R3 and the projection, and p for the full scores and N1.

## Files

| file | sha256 (LF) |
|---|---|
| `iiib_diag.py` | `29acac74b163403480daf9362ca460312ef91dffd6e97255b272a89ce45b39f9` |
| `iiib_diag_out.txt` | `2e8eeaa62738763b80f303ab47dd6511b78a2f919432fd62ec33fdf57e7fd776` |
| `iiib_diag_boards.csv` (414 boards: 300 fresh, 99 seen, 15 worlds) | `f50d2dad5718f6ae85b9cd12f625ade5f5a4599a8506189d4d65bc28c680d4e3` |

Inputs, checked by the script against these hashes:

| input | sha256 |
|---|---|
| `natural_fit_failure_replication_20260929T143137Z_a9f1c82/raw_fits.json.gz` | `ca7bf71c10965f65fa74cd0285002f1db9a50af6c06a95d8961acd34be8621f0` |
| `natural_fit_failure_replication_20260929T143137Z_a9f1c82/boards.csv` | `38f9c4fdd0bbff6c4dd360630ff1e8e762990d1fff5f7e9901e144931609c201` |
| `failed_fit_calibration_20260929T094748Z_255a03d/raw_fits.json.gz` | `3b053b705eb7dddc7b98e92685585f18906a7bd1a115bab9a3af247f213afd04` |
| `failed_fit_calibration_20260929T094748Z_255a03d/permuted_reference.csv` | `b88a7c3326ac8ad78d912064983b6dfd012c2cbae4e0f3876c717cc64e1c68e2` |
| `failed_fit_calibration_20260929T094748Z_255a03d/worlds.csv` | `60dd12359a9f3ecc3c9e925c16eae6e6994e39e4d4745d5d7b18b8ca7a5d7be2` |

They equal the script's `SHA` table and the runs' `SHA256SUMS.txt`.

To reproduce, run `PYTHONUTF8=1 python iiib_diag.py > iiib_diag_out.txt`. The rerun output is
byte-identical.

## Read with care

- **R1a is coupled to N1 by arithmetic.** On a board with N1 ≥ 0.90, R1a ≤ 1 − 0.90 = 0.10 by
  construction. So how well R1a separates the N1 ≥ 0.90 class is largely arithmetic, not evidence.
- **R2 carries W's column effect.** At λ_c = 100, u·v has collapsed (the double-centred logit is
  ~1e-16), yet R2 still reads 0.525–0.725 under TAU. That residue is W alone.
- **At λ = 100, R3's exact value is noise.** R3 exact ranges from 0.25 to 0.70 there, while R3
  under TAU is 0.5000 on every board. Only the TAU value means anything at that λ.
