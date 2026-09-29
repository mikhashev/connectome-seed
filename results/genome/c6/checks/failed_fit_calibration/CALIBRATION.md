# Failed-fit branch calibration

Registration `docs/plans/2026-09-29-failed-fit-branch-calibration-registration.md`, revision 1.9. git_head=255a03da4785adda816640fdeeb6959265c8a9f3.

## Outcome (section 7)

- **C2**: fit side witnessed, forced only
- **C6**: no rank-limit witness on block B's shape (declared before values)

FC reads FF-sel in all its worlds: True. FN worlds meeting the branch: 0 of 10. GATE_ULP_SPLIT rows: 0.

## Worlds (registered label beside the separator; the label text is unchanged)

| world | seed | label | ceiling_block (tau) | cert | ceil_1 (tau) | ceil_1_float | lambda_c | ceil_lambda_c_float | ceil_1_starts100 | reads | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cal:FC:0 | 93100 | U: failed fit: rule #2.1 cannot hold the block even when trained on it alone | 0.6000 (0.6000) | 1/1 | 1.0000 (1.0000) | 1.0000 | 100 | 0.4800 | 1.0000 | fit failure, FF-sel | - |
| cal:FC:1 | 93101 | U: failed fit: rule #2.1 cannot hold the block even when trained on it alone | 0.6000 (0.6000) | 1/1 | 1.0000 (1.0000) | 1.0000 | 100 | 0.4800 | 1.0000 | fit failure, FF-sel | - |
| cal:FC:2 | 93102 | U: failed fit: rule #2.1 cannot hold the block even when trained on it alone | 0.6000 (0.6000) | 1/1 | 1.0000 (1.0000) | 1.0000 | 100 | 0.4800 | 1.0000 | fit failure, FF-sel | - |
| cal:FC:3 | 93103 | U: failed fit: rule #2.1 cannot hold the block even when trained on it alone | 0.6000 (0.6000) | 1/1 | 1.0000 (1.0000) | 1.0000 | 100 | 0.4800 | 1.0000 | fit failure, FF-sel | - |
| cal:FC:4 | 93104 | U: failed fit: rule #2.1 cannot hold the block even when trained on it alone | 0.6000 (0.6000) | 1/1 | 1.0000 (1.0000) | 1.0000 | 100 | 0.4800 | 1.0000 | fit failure, FF-sel | - |
| cal:FN1:0 | 93110 | G (its text needs block B's limits, which this run does not measure) | 0.9975 (0.9975) | 1/1 | 0.9975 (0.9975) | 0.9975 | 1 | 0.9975 | 0.9975 | gate passed | - |
| cal:FN1:1 | 93111 | G (its text needs block B's limits, which this run does not measure) | 0.9975 (0.9975) | 1/1 | 0.9975 (0.9975) | 0.9975 | 1 | 0.9975 | 0.9975 | gate passed | - |
| cal:FN1:2 | 93112 | G (its text needs block B's limits, which this run does not measure) | 0.9975 (0.9975) | 1/1 | 0.9975 (0.9975) | 0.9975 | 1 | 0.9975 | 0.9975 | gate passed | - |
| cal:FN1:3 | 93113 | G (its text needs block B's limits, which this run does not measure) | 0.9975 (0.9975) | 1/1 | 0.9975 (0.9975) | 0.9975 | 1 | 0.9975 | 0.9975 | gate passed | - |
| cal:FN1:4 | 93114 | G (its text needs block B's limits, which this run does not measure) | 0.9975 (0.9975) | 1/1 | 0.9975 (0.9975) | 0.9975 | 1 | 0.9975 | 0.9975 | gate passed | - |
| cal:FN2:0 | 93120 | G (its text needs block B's limits, which this run does not measure) | 0.9950 (0.9950) | 1/1 | 0.9950 (0.9950) | 0.9925 | 1 | 0.9925 | 0.9925 | gate passed | - |
| cal:FN2:1 | 93121 | G (its text needs block B's limits, which this run does not measure) | 0.9850 (0.9850) | 1/1 | 0.9850 (0.9850) | 0.9850 | 1 | 0.9850 | 0.9850 | gate passed | - |
| cal:FN2:2 | 93122 | G (its text needs block B's limits, which this run does not measure) | 0.9850 (0.9850) | 1/1 | 0.9850 (0.9850) | 0.9850 | 1 | 0.9850 | 0.9850 | gate passed | - |
| cal:FN2:3 | 93123 | G (its text needs block B's limits, which this run does not measure) | 0.9975 (0.9975) | 1/1 | 0.9975 (0.9975) | 0.9975 | 1 | 0.9975 | 0.9975 | gate passed | - |
| cal:FN2:4 | 93124 | G (its text needs block B's limits, which this run does not measure) | 0.9925 (0.9925) | 1/1 | 0.9925 (0.9925) | 0.9925 | 1 | 0.9925 | 0.9925 | gate passed | - |

## Gate options (section 8; printed, only (v-a) sets the label)

| world | v-a | v-b | v-c | v-d |
|---|---|---|---|---|
| cal:FC:0 | U, failed fit | U (the D1 candidates disagree on the gate) | G | U, failed fit |
| cal:FC:1 | U, failed fit | U (the D1 candidates disagree on the gate) | G | U, failed fit |
| cal:FC:2 | U, failed fit | U (the D1 candidates disagree on the gate) | G | U, failed fit |
| cal:FC:3 | U, failed fit | U (the D1 candidates disagree on the gate) | G | U, failed fit |
| cal:FC:4 | U, failed fit | U (the D1 candidates disagree on the gate) | G | U, failed fit |
| cal:FN1:0 | G | G | G | G |
| cal:FN1:1 | G | G | G | G |
| cal:FN1:2 | G | G | G | G |
| cal:FN1:3 | G | G | G | G |
| cal:FN1:4 | G | G | G | G |
| cal:FN2:0 | G | G | G | G |
| cal:FN2:1 | G | G | G | G |
| cal:FN2:2 | G | G | G | G |
| cal:FN2:3 | G | G | G | G |
| cal:FN2:4 | G | G | G | G |

## Permuted-board reference (section 10; printed, decides nothing)

99 boards; registered ceiling_block below 0.90 on 53 of 99; cert >= 0.90 on 99 of 99. Per board in permuted_reference.csv.

