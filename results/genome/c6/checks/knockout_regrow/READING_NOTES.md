# Reading notes beside block A's frozen outputs

These notes add to RESULT.md; they change no label.

## 1. Block A with its block-only fit forced to lambda = 100 (2026-09-30, post-data)

Registered in `docs/plans/2026-09-30-symmetric-lambda-pair-registration.md` (prediction commit
e7d973f), run from b44d383; carrier `results/genome/c6/checks/symmetric_lambda_pair/RESULT.md`; blind
review by the owner's separate session: follows (`BLIND_REVIEW_raw.md` there).

- Control: at lambda = 1 the route reproduced A's registered `ceiling_block` 1024/1024 with all 64 p
  bit-equal to the store.
- `cert_A` = 1024/1024: the class holds the block. The reviewer notes that A's pattern is exactly a
  rank-1 board (ON x T4 union OFF x T5), so one explicit member certifies it without a search.
- At lambda = 100: max |u.v| = 3.3e-19 and `ceil_100_A` = 0.5000, every p = 0.5 (1024 ties). The
  reviewer's explanation: every source and every target of A has 4 of 8 present, so N1 and W are zero,
  and with the interaction switched off nothing is left; 0.5 is the all-ties floor.
- A's own `read_label` with `ceiling_block` := 0.5000 reads **U**, "failed fit". Branch (b): A would
  fail at lambda = 100 as B did; the A/B pair differs by the lambda choice on the gate clause, not
  shown to differ by the block. The registered label G is not edited.
