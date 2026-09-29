# Reading notes beside the frozen outputs (CC, 2026-09-29)

These notes add to REPLICATION.md; they change no label.

## 1. The registered reading

RP1, replicated: on 300 fresh certified permuted boards the registered block fit of rule #2.1
fails the gate on 171 (0.570), and every failure reads a fit-failure row (165 FF-sel, 5
"FF-struct or FF-opt, not separated", 1 FF-quant at lambda 1). The BF family collapses at the same
order (166/139/144/144). Choosing lambda = 100 marks failure (171 of 186). P4' fails: 15 of 129
passes chose lambda = 100 (11.6 %, against 3 of 46 = 6.5 % in the seen set). The j = 89 class
reproduced on 5 boards. The blind review (BLIND_REVIEW.md) found the recorded outcome follows.

## 2. Disclosure: a reviewer's later criterion that did not reach the prediction commit

CC built rev 1.1 from a chat read that ended at 14:07 UTC. Warren's second message on Q-W2
(DPC Research chat, 2026-09-29 14:11:17 UTC) proposed, instead of the fixed lines: for P1 a
one-sided 5 % test around 0.5, i.e. 136-164 of 300; for the j = 89 class a line of <= 7. CC missed
that message; it did not enter b5513e3 or rev 1.2. This is a process error, not a decision.

| | registered | under Warren's 14:11 criterion |
|---|---|---|
| P1: 171 of 300 | holds ([0.40, 0.60] = 120-180) | outside 136-164, so the label would be RP2 "rate shifted" |
| P2b: 6 not FF-sel | holds (<= 10) | holds (<= 7) |

The registered outcome stands as RP1 (Warren 14:47:29 and Ark 14:49:16 UTC agree). Read beside it:

- **Warren:** 171 against the band edge 164 is 7 boards, about 1.2 SD from the centre, so the
  reading under his criterion is "at the upper edge", not "far outside".
- **Ark (his arithmetic, normal approximation):** both criteria are centred on 0.50 and differ only
  in width. Against 0.50 the fresh rate is z = +2.42; against the seen rate 53/99 = 0.5354, which
  is what a replication compares with, it is z = +1.20 (p = 0.23). The fresh set is also
  indistinguishable from the seen set in the share choosing lambda = 100 (62.0 % against 56.6 %,
  z = 0.95) and in the passes at lambda = 100 (z = 0.68). P4' failed at 114/129 = 0.884 against a
  seen 43/46 = 0.935 (z = -0.98): the 0.90 line sat within noise of the seen value.
- **The rule this leaves (Ark):** a decision rule is derived from a named null and a named alpha,
  not taken as a round band. This was the second time in the session that pre-run material arrived
  inside the writing window (the first: the M8 predictions not committed on their own).

## 3. Three natural instances of the decoder split (Ark)

DECODER_SPLIT_AT_LC flags fresh:145 and 161 (quantised passes at 0.90125, float fails) and
fresh:266 (quantised fails at 0.89875, float exactly 0.9000): natural mirrors of the calibration's
board 41, in addition to j = 49 of the seen set.

## 4. Johnny's three points (14:55:20 UTC)

- The P1 sensitivity is a finding about the decision rule, not a footnote: the label flips with the
  choice between two criteria the team proposed, while the substantive result (collapse near 57 %,
  FF-sel dominant) holds under both. Read against the seen rate it is not a shift (section 2, Ark).
- P4' failing is material for (iii), not a weakness of the replication: the 15 passes at
  lambda = 100 are additive-dominated boards (the board 41 class).
- Process rule: when two criteria are proposed, the author chooses one explicitly and records the
  choice in the prediction commit.

## 5. (iii-a) and (iii-b) after the run (DPC Research chat, 15:00-15:18 UTC)

- (iii-a) as a gate is withdrawn (Ark 15:00:23; Johnny, Warren, Zcode agree; CC's earlier
  recommendation withdrawn): on all 414 boards (300 fresh, 99 seen, 15 worlds) no board passes at
  the chosen lambda and fails at lambda = 1, while lambda = 1 passes 98 % and passes FC's forced
  world. It is recorded as a property of the class, not a gate.
- The (iii-b) diagnostic on these recorded fits is in docs/prereg-scripts/2026-09-29-iiib-diagnostic/
  (post-data; any (iii-b) registration is not blind to it).

## 6. (iii-b) closed as a diagnostic; the lambda law (Mike's choice "1 then 2", 2026-09-29)

(iii-b) stays a diagnostic (option 1). Ark (15:56:11 UTC) read iiib_diag_boards.csv and CC
re-checked it: on all 414 boards lambda_c takes only 1 and 100. The 247 boards at lambda_c = 100
carry |u.v| <= 1.31e-15 (R3 = 0.5000 under TAU on every one) and read 229 U, 18 G. The 167 boards
at lambda_c = 1 carry |u.v| >= 1.079 and all 167 pass. The verdict follows the lambda choice;
at lambda = 100 the additive part decides (Johnny, 16:10:00). Block A passed at block lambda 1.0
(knockout_regrow/RESULT.md:17, 1.0000); block B failed at 100 (knockout_regrow_block_b/RESULT.md:31,
0.7744). Option 2 becomes text only: declare the structural class "a verdict taken at lambda_c =
100 with u.v = 0 is not evidence about the rule" in a registration.
