# Addendum to the registered predictions, after the τ alignment

**Written:** 2026-09-23 UTC, by CC, at Ark's request (group chat, 14:32 UTC), with Zcode (14:36 UTC)
and Johnny (14:37 UTC) agreeing.
**Applies to:** [`docs/plans/2026-09-23-first-rule-failure-predictions.md`](../plans/2026-09-23-first-rule-failure-predictions.md)
(registered at `b8ca3dd` and `32a4ae9`). That file is not edited. This note is appended beside it,
in the same way the τ change is recorded beside the spec
([`2026-09-23-c6-harness-tau-in-p3-p4.md`](2026-09-23-c6-harness-tau-in-p3-p4.md)).
No rule #2 run existed when this note was written.

## 1. A sentence of the registration is false after `1789aeb`

§4c of the registration says that P4's pass test is a plain strict `>` with no τ. It concludes that,
unless rule #2's existence predictions are bit-identical to BF_r's, a difference of about 1e-12
"decides P4 in either direction". The same reading appears in the §4c branch table.

Commit `1789aeb` changed the harness so that P4 passes only if `margin − threshold > TAU` (τ = 1e-9,
spec A7). A margin within τ of the threshold is now a tie, and a tie fails. So:

- **The branch "existence not touched → P4 is decided by noise" no longer exists.** A sub-τ
  difference is a fail by construction.
- **The definitional reading is one-sided.** If X does not touch existence, P4 fails, whether the
  predictions are bit-identical to BF_r's or differ from them by noise.
- None of this changes P4's threshold or any registered prediction's quantity. Rule #2 touches
  existence (its proposal, §8), so its run is in the other column of the table anyway.

## 2. Shifted line numbers in `harness.py`

`1789aeb` added three lines. Citations of `harness.py` at line 1019 or later in the registration,
the blind reader's report and the rule #2 proposal refer to the harness those records stamp
(`c01cd9eb…`). In the current harness (`6fc80952…`) they move by +3:

| cited | now | what |
|---|---|---|
| 1019 | 1022 | P3 `strictly_above_all` |
| 1028 | 1031 | P4 `pass` |
| 1043 | 1046 | `loto` |
| 1324 / 1329 | 1327 / 1332 | `dial_ratio` definition / call |

Lines before 1019 (for example 277 and 666–695) did not move.

## 3. The "BF rank profile" is five reference points, not a profile

The registration (§2 row 4, §4c) speaks of a "BF rank profile, r = 1..16". Ark traced each number
in `harness_controls.json`. Each one is the `P4.bf` of a **different** control exam, fitted at the
rank that control's `rank_of` gave. Nobody swept the rank.

| r | BF_r margin over N1 | control it comes from |
|---|---|---|
| 1 | +0.0281500511 | `real/N0 as a rule` |
| 3 | +0.0403407861 | `real/N1 as a rule` |
| 4 | +0.0397237501 | `real/PR` |
| 8 | +0.0493311002 | `real/RP_r8 as a rule (seed 999)` |
| 16 | +0.0485136115 | `real/oracle` |

Consequences:

- **No BF value exists in the record for r = 2, 5–7 or 9–15.** The §4c instruction "at other r, read
  the value off the profile" cannot be carried out for those ranks. P4 always recomputes the
  threshold at the rule's own rank (`bf_margin(r, bank)`), so the verdict is unaffected. Only the
  pre-run reading is.
- **The points are not monotone:** r = 3 is above r = 4.
- **r = 1 is the minimum of the five points:** 0.0116 below r = 4 and 0.0212 below r = 8.

The name "profile" should read "reference points" from here on.

## 4. Registered quantities that are empty or silent at rule #2's r = 1

Rule #2's rank, computed by A11, is r = 1, so its P4 threshold is BF_1 = +0.02815. Two registered
quantities were anchored to levels computed at other ranks (BF_3, BF_12). At r = 1 they cannot hold.
Their authors state this themselves and do **not** edit them, because moving a bar after seeing the
declared r would be fishing.

- **P-A3 (Ark).** "Margin ≥ +0.040 **and** rule − BF_r < +0.005" is empty at r = 1: a margin
  ≥ +0.040 implies rule − BF_1 ≥ +0.0119. Only the claim ("P4 fails") can be tested.
- **P-J1 (Johnny).** "Margin ≥ +0.040, refuted below +0.030": if rule #2 inherits BF_1's margin
  (+0.02815), that falls inside P-J1's own refuting zone. Johnny registers, before the run, that
  P-J1 is silent on quantity in this round. His live reading is "margin ≈ BF_1 within the ±0.002
  tie band". Anything outside [0.026, 0.030] is the addition's effect, not BF inheritance.
- **P-A1 (Ark).** Its guard `m(0.0) ≥ +0.040` will most likely stay closed at r = 1. Ark registers,
  before the run, that his report will have no reading on the dial axis in this round.
- **The §4c table's existence-not-touched row for P-J1** lists r = 4, 8 and 12, not r = 1. Rule #2
  touches existence, so that row does not apply here.

Ark's own assessment, recorded as he gave it: the discriminating power of his set in this round is
low. Only P-A4's signature (the offset margin grows under destruction) is not a consensus. Johnny's
P-J3 (Δ ≤ 0 against BF_1) is the one item that directly contradicts the rule author's prior
(about 0.5 that the margin lands above BF_1).

## 5. The first rule's verdict is the same under both harness versions

Ark computed the first rule's own gaps from `rule_runs/first_rule_k12/result.json`:

| arm | gap |
|---|---|
| P3 existence | +0.03904 |
| P3 offset | −0.03820 |
| P3 counts | −0.05533 |
| P3 sign | 0.0 |
| P4 | −0.05302 |

The one positive gap is seven orders of magnitude above τ, so first_rule_k12's FAIL stands under
both `c01cd9eb` and `6fc80952`. It is recorded because the two rules are now judged by different
harness versions.
