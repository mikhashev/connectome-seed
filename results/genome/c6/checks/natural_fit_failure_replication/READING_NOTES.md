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
