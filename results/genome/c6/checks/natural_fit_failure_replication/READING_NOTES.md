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

The registered outcome stands as RP1. Read beside it: under Warren's later criterion the rate
0.570 (95 % CP [0.512, 0.627]) is above the 0.5-centred band, so "rate shifted upward" is the
reading that criterion gives. The kind of failure replicated either way.
