# Natural fit-failure replication

Registration `docs/plans/2026-09-29-natural-fit-failure-replication-registration.md`, revision 1.2. git_head=a9f1c82718c67b3b166c11341a490b43f17bc66b. Prediction commit b5513e3fd50c32caf9a1a30c01f6fb4423d4fa7b.

## Outcome (section 7)

- **RP1**: replicated

Secondary: **J89-reproduced** (same row as j = 89: 5; FF-opt named: 0; FF-quant at lambda = 1: 1; residuals).

## Predictions (section 6; hold / fail)

- P1: hold (failures / N_c = 171 / 300, in [0.40, 0.60])
- P2a (a design check, not a prediction): hold (every certified failure reads a fit-failure row)
- P2b: hold (failures not FF-sel = 6; decision line <= 10 of 300); beside it, deciding nothing: one-sided 5 % test of rate <= 1/30 (cut >= 16) does not reject
- P3: hold (each BF_r collapse rate within 0.5x-2x of the rule's; rule 171 of 300; BF_1 166 of 300 hold; BF_2 139 of 300 hold; BF_3 144 of 300 hold; BF_4 144 of 300 hold)
- P4': fail (passes with lambda_c = 1: 114 of 129 (>= 0.90); passes with lambda_c != 1 (the withdrawn P4's count, not evaluated): 15)
- P5 (a label, not independent evidence): hold ((i) hold: failures among lambda_c = 100: 171 of 186 (>= 0.90); (ii) hold: lambda_c = 100 among failures: 171 of 171 (>= 0.95)); beside it: FF-sel among lambda_c = 100: 165 of 186

Failures with ceil_1 in [0.90, 0.91): 3. GATE_ULP_SPLIT rows: 0. CEIL_1_ULP_SPLIT rows: 0. CERT_ULP_SPLIT rows: 0. DECODER_SPLIT_AT_LC rows: 3. CERT_BELOW_CUT rows: 0. CERT_COUNTS_DISAGREE rows: 0.

P3, rule failure x BF_r failure (certified boards):

| BF_r | both fail | rule only | BF only | both pass |
|---|---|---|---|---|
| BF_1 | 165 | 6 | 1 | 128 |
| BF_2 | 127 | 44 | 12 | 117 |
| BF_3 | 130 | 41 | 14 | 115 |
| BF_4 | 130 | 41 | 14 | 115 |

## Boards (every AUC object exact (tau))

| board | seed | cert | ceiling_block | lambda_c | ceil_1 | ceil_1_float | ceil_lambda_c_float | ceil_1_starts100 | ceil_1_starts100_quantised | reads | BF_1-4 rows | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fresh:0 | 94000 | 391/400 | 0.7050 (0.7050) | 100 | 0.9300 (0.9300) | 0.9200 (0.9200) | 0.7050 (0.7050) | 0.9200 (0.9200) | 0.9300 (0.9300) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:1 | 94001 | 199/200 | 0.9675 (0.9675) | 1 | 0.9675 (0.9675) | 0.9625 (0.9625) | 0.9625 (0.9625) | 0.9625 (0.9625) | 0.9675 (0.9675) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:2 | 94002 | 1/1 | 0.9975 (0.9975) | 1 | 0.9975 (0.9975) | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | 0.9975 (0.9975) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:3 | 94003 | 1/1 | 0.9900 (0.9900) | 1 | 0.9900 (0.9900) | 0.9875 (0.9875) | 0.9875 (0.9875) | 0.9875 (0.9875) | 0.9900 (0.9900) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:4 | 94004 | 199/200 | 0.9750 (0.9750) | 1 | 0.9750 (0.9750) | 0.9700 (0.9700) | 0.9700 (0.9700) | 0.9700 (0.9700) | 0.9750 (0.9750) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:5 | 94005 | 197/200 | 0.7362 (0.7362) | 100 | 0.9225 (0.9225) | 0.9250 (0.9250) | 0.7362 (0.7362) | 0.9250 (0.9250) | 0.9225 (0.9225) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:6 | 94006 | 1/1 | 1.0000 (1.0000) | 1 | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:7 | 94007 | 197/200 | 0.6625 (0.6625) | 100 | 0.9125 (0.9125) | 0.9125 (0.9125) | 0.6575 (0.6575) | 0.9125 (0.9125) | 0.9125 (0.9125) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:8 | 94008 | 199/200 | 0.7900 (0.7900) | 100 | 0.9275 (0.9275) | 0.9275 (0.9275) | 0.7875 (0.7875) | 0.9275 (0.9275) | 0.9275 (0.9275) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:9 | 94009 | 199/200 | 0.9700 (0.9700) | 1 | 0.9700 (0.9700) | 0.9600 (0.9600) | 0.9600 (0.9600) | 0.9600 (0.9600) | 0.9700 (0.9700) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:10 | 94010 | 199/200 | 0.9525 (0.9525) | 1 | 0.9525 (0.9525) | 0.9500 (0.9500) | 0.9500 (0.9500) | 0.9500 (0.9500) | 0.9525 (0.9525) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:11 | 94011 | 397/400 | 0.8225 (0.8225) | 100 | 0.9600 (0.9600) | 0.9575 (0.9575) | 0.8125 (0.8125) | 0.9575 (0.9575) | 0.9600 (0.9600) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:12 | 94012 | 1/1 | 0.9775 (0.9775) | 1 | 0.9775 (0.9775) | 0.9850 (0.9850) | 0.9850 (0.9850) | 0.9850 (0.9850) | 0.9775 (0.9775) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:13 | 94013 | 199/200 | 0.8700 (0.8700) | 100 | 0.9600 (0.9600) | 0.9600 (0.9600) | 0.8725 (0.8725) | 0.9600 (0.9600) | 0.9600 (0.9600) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:14 | 94014 | 1/1 | 0.8300 (0.8300) | 100 | 0.9800 (0.9800) | 0.9800 (0.9800) | 0.8275 (0.8300) | 0.9800 (0.9800) | 0.9800 (0.9800) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:15 | 94015 | 1/1 | 0.9550 (0.9550) | 1 | 0.9550 (0.9550) | 0.9550 (0.9550) | 0.9550 (0.9550) | 0.9550 (0.9550) | 0.9550 (0.9550) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:16 | 94016 | 1/1 | 0.9775 (0.9775) | 1 | 0.9775 (0.9775) | 0.9800 (0.9800) | 0.9800 (0.9800) | 0.9800 (0.9800) | 0.9775 (0.9775) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:17 | 94017 | 1/1 | 0.8700 (0.8700) | 100 | 0.9838 (0.9838) | 0.9825 (0.9825) | 0.8600 (0.8600) | 0.9825 (0.9825) | 0.9838 (0.9838) | fit failure, FF-sel | gate passed; gate passed; gate passed; gate passed | - |
| fresh:18 | 94018 | 199/200 | 0.7750 (0.7750) | 100 | 0.9575 (0.9575) | 0.9525 (0.9525) | 0.7800 (0.7800) | 0.9525 (0.9525) | 0.9575 (0.9575) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:19 | 94019 | 79/80 | 0.9350 (0.9350) | 1 | 0.9350 (0.9350) | 0.9300 (0.9300) | 0.9300 (0.9300) | 0.9300 (0.9300) | 0.9350 (0.9350) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:20 | 94020 | 99/100 | 0.7913 (0.7913) | 100 | 0.9450 (0.9450) | 0.9425 (0.9425) | 0.7900 (0.7900) | 0.9425 (0.9425) | 0.9450 (0.9450) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:21 | 94021 | 1/1 | 0.9900 (0.9900) | 1 | 0.9900 (0.9900) | 0.9875 (0.9875) | 0.9875 (0.9875) | 0.9875 (0.9875) | 0.9900 (0.9900) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:22 | 94022 | 197/200 | 0.7275 (0.7275) | 100 | 0.9350 (0.9350) | 0.9350 (0.9350) | 0.7275 (0.7275) | 0.9350 (0.9350) | 0.9350 (0.9350) | fit failure, FF-sel | gate passed; gate passed; gate passed; gate passed | - |
| fresh:23 | 94023 | 1/1 | 0.9575 (0.9575) | 1 | 0.9575 (0.9575) | 0.9625 (0.9625) | 0.9625 (0.9625) | 0.9625 (0.9625) | 0.9575 (0.9575) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:24 | 94024 | 199/200 | 0.8575 (0.8575) | 100 | 0.9650 (0.9650) | 0.9550 (0.9550) | 0.8475 (0.8475) | 0.9550 (0.9550) | 0.9650 (0.9650) | fit failure, FF-sel | BF fit failure, selection; gate passed; BF fit failure, selection; BF fit failure, selection | - |
| fresh:25 | 94025 | 1/1 | 0.7775 (0.7775) | 100 | 0.9125 (0.9125) | 0.9150 (0.9150) | 0.7725 (0.7725) | 0.9150 (0.9150) | 0.9125 (0.9125) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:26 | 94026 | 1/1 | 0.9775 (0.9775) | 100 | 1.0000 (1.0000) | 0.9950 (0.9950) | 0.9775 (0.9775) | 0.9950 (0.9950) | 1.0000 (1.0000) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:27 | 94027 | 1/1 | 0.9838 (0.9838) | 1 | 0.9838 (0.9838) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9838 (0.9838) | gate passed | gate passed; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:28 | 94028 | 1/1 | 0.8862 (0.8862) | 100 | 0.9725 (0.9725) | 0.9725 (0.9725) | 0.8875 (0.8875) | 0.9725 (0.9725) | 0.9725 (0.9725) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:29 | 94029 | 397/400 | 0.8187 (0.8187) | 100 | 0.9375 (0.9375) | 0.9400 (0.9400) | 0.8213 (0.8213) | 0.9400 (0.9400) | 0.9375 (0.9375) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:30 | 94030 | 1/1 | 0.9900 (0.9900) | 1 | 0.9900 (0.9900) | 0.9850 (0.9850) | 0.9850 (0.9850) | 0.9850 (0.9850) | 0.9900 (0.9900) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:31 | 94031 | 1/1 | 0.9250 (0.9250) | 100 | 0.9800 (0.9800) | 0.9800 (0.9800) | 0.9175 (0.9175) | 0.9800 (0.9800) | 0.9800 (0.9800) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:32 | 94032 | 1/1 | 0.7875 (0.7875) | 100 | 0.9525 (0.9525) | 0.9475 (0.9475) | 0.7850 (0.7850) | 0.9475 (0.9475) | 0.9525 (0.9525) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:33 | 94033 | 397/400 | 0.9800 (0.9800) | 1 | 0.9800 (0.9800) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9800 (0.9800) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:34 | 94034 | 1/1 | 0.7900 (0.7900) | 100 | 0.9375 (0.9375) | 0.9425 (0.9425) | 0.7900 (0.7900) | 0.9425 (0.9425) | 0.9375 (0.9375) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:35 | 94035 | 1/1 | 0.9900 (0.9900) | 1 | 0.9900 (0.9900) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9900 (0.9900) | gate passed | gate passed; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:36 | 94036 | 1/1 | 0.9775 (0.9775) | 1 | 0.9775 (0.9775) | 0.9750 (0.9750) | 0.9750 (0.9750) | 0.9750 (0.9750) | 0.9775 (0.9775) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:37 | 94037 | 1/1 | 0.8087 (0.8087) | 100 | 0.9700 (0.9700) | 0.9750 (0.9750) | 0.8075 (0.8075) | 0.9750 (0.9750) | 0.9700 (0.9700) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:38 | 94038 | 79/80 | 0.7500 (0.7500) | 100 | 0.9225 (0.9225) | 0.9225 (0.9225) | 0.7475 (0.7475) | 0.9225 (0.9225) | 0.9225 (0.9225) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:39 | 94039 | 1/1 | 0.9675 (0.9675) | 1 | 0.9675 (0.9675) | 0.9675 (0.9675) | 0.9675 (0.9675) | 0.9675 (0.9675) | 0.9675 (0.9675) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:40 | 94040 | 393/400 | 0.6963 (0.6963) | 100 | 0.8975 (0.8975) | 0.9025 (0.9025) | 0.6813 (0.6813) | 0.9025 (0.9025) | 0.8975 (0.8975) | fit failure, FF-quant (at lambda = 1) | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:41 | 94041 | 1/1 | 0.9775 (0.9775) | 1 | 0.9775 (0.9775) | 0.9775 (0.9775) | 0.9775 (0.9775) | 0.9775 (0.9775) | 0.9775 (0.9775) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:42 | 94042 | 1/1 | 0.9950 (0.9950) | 1 | 0.9950 (0.9950) | 0.9950 (0.9950) | 0.9950 (0.9950) | 0.9950 (0.9950) | 0.9950 (0.9950) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:43 | 94043 | 1/1 | 0.8425 (0.8425) | 100 | 0.9437 (0.9437) | 0.9475 (0.9475) | 0.8450 (0.8450) | 0.9475 (0.9475) | 0.9437 (0.9437) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:44 | 94044 | 1/1 | 0.9925 (0.9925) | 1 | 0.9925 (0.9925) | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.9925 (0.9925) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:45 | 94045 | 1/1 | 0.9850 (0.9850) | 1 | 0.9850 (0.9850) | 0.9775 (0.9775) | 0.9775 (0.9775) | 0.9775 (0.9775) | 0.9850 (0.9850) | gate passed | gate passed; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:46 | 94046 | 397/400 | 0.9625 (0.9625) | 1 | 0.9625 (0.9625) | 0.9650 (0.9650) | 0.9650 (0.9650) | 0.9650 (0.9650) | 0.9625 (0.9625) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:47 | 94047 | 199/200 | 0.8100 (0.8100) | 100 | 0.9500 (0.9500) | 0.9450 (0.9450) | 0.8050 (0.8050) | 0.9450 (0.9450) | 0.9500 (0.9500) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:48 | 94048 | 1/1 | 0.8225 (0.8225) | 100 | 0.9775 (0.9775) | 0.9800 (0.9800) | 0.8225 (0.8225) | 0.9800 (0.9800) | 0.9775 (0.9775) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:49 | 94049 | 1/1 | 0.8825 (0.8825) | 100 | 0.9875 (0.9875) | 0.9900 (0.9900) | 0.8750 (0.8750) | 0.9900 (0.9900) | 0.9875 (0.9875) | fit failure, FF-sel | gate passed; gate passed; gate passed; gate passed | - |
| fresh:50 | 94050 | 397/400 | 0.7550 (0.7550) | 100 | 0.9325 (0.9325) | 0.9275 (0.9275) | 0.7550 (0.7550) | 0.9275 (0.9275) | 0.9325 (0.9325) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:51 | 94051 | 199/200 | 0.9775 (0.9775) | 1 | 0.9775 (0.9775) | 0.9775 (0.9775) | 0.9775 (0.9775) | 0.9775 (0.9775) | 0.9775 (0.9775) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:52 | 94052 | 199/200 | 0.7875 (0.7875) | 100 | 0.9525 (0.9525) | 0.9525 (0.9525) | 0.7925 (0.7925) | 0.9525 (0.9525) | 0.9525 (0.9525) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:53 | 94053 | 397/400 | 0.7562 (0.7562) | 100 | 0.9175 (0.9175) | 0.9175 (0.9175) | 0.7562 (0.7562) | 0.9175 (0.9175) | 0.9175 (0.9175) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:54 | 94054 | 199/200 | 0.7275 (0.7275) | 100 | 0.9200 (0.9200) | 0.9250 (0.9250) | 0.7262 (0.7275) | 0.9250 (0.9250) | 0.9200 (0.9200) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:55 | 94055 | 1/1 | 0.8050 (0.8050) | 100 | 0.9675 (0.9675) | 0.9650 (0.9650) | 0.8025 (0.8050) | 0.9650 (0.9650) | 0.9675 (0.9675) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:56 | 94056 | 1/1 | 0.9575 (0.9575) | 1 | 0.9575 (0.9575) | 0.9575 (0.9575) | 0.9575 (0.9575) | 0.9575 (0.9575) | 0.9575 (0.9575) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:57 | 94057 | 197/200 | 0.9425 (0.9425) | 1 | 0.9425 (0.9425) | 0.9400 (0.9400) | 0.9400 (0.9400) | 0.9400 (0.9400) | 0.9425 (0.9425) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:58 | 94058 | 79/80 | 0.7300 (0.7300) | 100 | 0.9363 (0.9363) | 0.9375 (0.9375) | 0.7300 (0.7300) | 0.9375 (0.9375) | 0.9363 (0.9363) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:59 | 94059 | 49/50 | 0.7050 (0.7050) | 100 | 0.9250 (0.9250) | 0.9225 (0.9225) | 0.7050 (0.7075) | 0.9225 (0.9225) | 0.9250 (0.9250) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:60 | 94060 | 397/400 | 0.9725 (0.9725) | 1 | 0.9725 (0.9725) | 0.9700 (0.9700) | 0.9700 (0.9700) | 0.9700 (0.9700) | 0.9725 (0.9725) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:61 | 94061 | 49/50 | 0.6787 (0.6787) | 100 | 0.9100 (0.9100) | 0.9100 (0.9100) | 0.6787 (0.6787) | 0.9100 (0.9100) | 0.9100 (0.9100) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:62 | 94062 | 1/1 | 0.9875 (0.9875) | 1 | 0.9875 (0.9875) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9875 (0.9875) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:63 | 94063 | 1/1 | 0.9900 (0.9900) | 1 | 0.9900 (0.9900) | 0.9875 (0.9875) | 0.9875 (0.9875) | 0.9875 (0.9875) | 0.9900 (0.9900) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:64 | 94064 | 1/1 | 0.9900 (0.9900) | 1 | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.9900 (0.9900) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:65 | 94065 | 1/1 | 0.9900 (0.9900) | 1 | 0.9900 (0.9900) | 0.9875 (0.9875) | 0.9875 (0.9875) | 0.9875 (0.9875) | 0.9900 (0.9900) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:66 | 94066 | 1/1 | 0.9550 (0.9550) | 1 | 0.9550 (0.9550) | 0.9450 (0.9450) | 0.9450 (0.9450) | 0.9450 (0.9450) | 0.9550 (0.9550) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:67 | 94067 | 49/50 | 0.7175 (0.7175) | 100 | 0.9400 (0.9400) | 0.9350 (0.9350) | 0.7125 (0.7125) | 0.9350 (0.9350) | 0.9400 (0.9400) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:68 | 94068 | 1/1 | 0.9550 (0.9550) | 100 | 0.9900 (0.9900) | 0.9875 (0.9875) | 0.9575 (0.9575) | 0.9875 (0.9875) | 0.9900 (0.9900) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:69 | 94069 | 49/50 | 0.8200 (0.8200) | 100 | 0.9275 (0.9275) | 0.9275 (0.9275) | 0.8125 (0.8125) | 0.9300 (0.9300) | 0.9275 (0.9275) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:70 | 94070 | 1/1 | 0.8400 (0.8400) | 100 | 0.9675 (0.9675) | 0.9625 (0.9625) | 0.8250 (0.8250) | 0.9625 (0.9625) | 0.9675 (0.9675) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:71 | 94071 | 1/1 | 0.8925 (0.8925) | 100 | 0.9725 (0.9725) | 0.9750 (0.9750) | 0.8850 (0.8850) | 0.9750 (0.9750) | 0.9725 (0.9725) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:72 | 94072 | 1/1 | 0.7975 (0.7975) | 100 | 0.9725 (0.9725) | 0.9700 (0.9700) | 0.7975 (0.7975) | 0.9700 (0.9700) | 0.9725 (0.9725) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:73 | 94073 | 199/200 | 0.7300 (0.7300) | 100 | 0.9150 (0.9150) | 0.9150 (0.9150) | 0.7300 (0.7300) | 0.9150 (0.9150) | 0.9150 (0.9150) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:74 | 94074 | 99/100 | 0.7675 (0.7675) | 100 | 0.9337 (0.9337) | 0.9400 (0.9400) | 0.7675 (0.7675) | 0.9400 (0.9400) | 0.9337 (0.9337) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:75 | 94075 | 1/1 | 0.8150 (0.8150) | 100 | 0.9425 (0.9425) | 0.9375 (0.9375) | 0.8150 (0.8150) | 0.9375 (0.9375) | 0.9425 (0.9425) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:76 | 94076 | 199/200 | 0.9000 (0.9000) | 100 | 0.9675 (0.9675) | 0.9650 (0.9650) | 0.9000 (0.9000) | 0.9650 (0.9650) | 0.9675 (0.9675) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:77 | 94077 | 1/1 | 0.9600 (0.9600) | 1 | 0.9600 (0.9600) | 0.9550 (0.9550) | 0.9550 (0.9550) | 0.9550 (0.9550) | 0.9600 (0.9600) | gate passed | gate passed; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:78 | 94078 | 199/200 | 0.7500 (0.7500) | 100 | 0.9625 (0.9625) | 0.9625 (0.9625) | 0.7500 (0.7500) | 0.9625 (0.9625) | 0.9625 (0.9625) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:79 | 94079 | 1/1 | 0.8425 (0.8425) | 100 | 0.9575 (0.9575) | 0.9575 (0.9575) | 0.8375 (0.8375) | 0.9575 (0.9575) | 0.9575 (0.9575) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:80 | 94080 | 199/200 | 0.8175 (0.8175) | 100 | 0.9475 (0.9475) | 0.9500 (0.9500) | 0.8150 (0.8150) | 0.9500 (0.9500) | 0.9475 (0.9475) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:81 | 94081 | 1/1 | 1.0000 (1.0000) | 1 | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:82 | 94082 | 1/1 | 0.8200 (0.8200) | 100 | 0.9875 (0.9875) | 0.9875 (0.9875) | 0.8200 (0.8200) | 0.9875 (0.9875) | 0.9875 (0.9875) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:83 | 94083 | 99/100 | 0.8075 (0.8075) | 100 | 0.9550 (0.9550) | 0.9525 (0.9525) | 0.8075 (0.8075) | 0.9525 (0.9525) | 0.9550 (0.9550) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:84 | 94084 | 397/400 | 0.7800 (0.7800) | 100 | 0.9525 (0.9525) | 0.9500 (0.9500) | 0.7825 (0.7825) | 0.9500 (0.9500) | 0.9525 (0.9525) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:85 | 94085 | 199/200 | 0.8075 (0.8075) | 100 | 0.9350 (0.9350) | 0.9325 (0.9325) | 0.8075 (0.8075) | 0.9325 (0.9325) | 0.9350 (0.9350) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:86 | 94086 | 1/1 | 0.9875 (0.9875) | 1 | 0.9875 (0.9875) | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.9875 (0.9875) | gate passed | gate passed; gate passed; BF fit failure, selection; BF fit failure, selection | - |
| fresh:87 | 94087 | 1/1 | 0.9875 (0.9875) | 1 | 0.9875 (0.9875) | 0.9875 (0.9875) | 0.9875 (0.9875) | 0.9875 (0.9875) | 0.9875 (0.9875) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:88 | 94088 | 1/1 | 0.8450 (0.8450) | 100 | 0.9650 (0.9650) | 0.9625 (0.9625) | 0.8450 (0.8450) | 0.9625 (0.9625) | 0.9650 (0.9650) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:89 | 94089 | 1/1 | 0.9825 (0.9825) | 1 | 0.9825 (0.9825) | 0.9800 (0.9800) | 0.9800 (0.9800) | 0.9800 (0.9800) | 0.9825 (0.9825) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:90 | 94090 | 199/200 | 0.8375 (0.8375) | 100 | 0.9750 (0.9750) | 0.9775 (0.9775) | 0.8438 (0.8438) | 0.9775 (0.9775) | 0.9750 (0.9750) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:91 | 94091 | 199/200 | 0.8550 (0.8550) | 100 | 0.9688 (0.9688) | 0.9700 (0.9700) | 0.8550 (0.8550) | 0.9700 (0.9700) | 0.9688 (0.9688) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:92 | 94092 | 1/1 | 0.9825 (0.9825) | 1 | 0.9825 (0.9825) | 0.9800 (0.9800) | 0.9800 (0.9800) | 0.9800 (0.9800) | 0.9825 (0.9825) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:93 | 94093 | 199/200 | 0.8712 (0.8712) | 100 | 0.9750 (0.9750) | 0.9625 (0.9625) | 0.8725 (0.8725) | 0.9625 (0.9625) | 0.9750 (0.9750) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:94 | 94094 | 99/100 | 0.7612 (0.7612) | 100 | 0.9425 (0.9425) | 0.9450 (0.9450) | 0.7612 (0.7612) | 0.9450 (0.9450) | 0.9425 (0.9425) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:95 | 94095 | 1/1 | 0.9100 (0.9100) | 100 | 1.0000 (1.0000) | 1.0000 (1.0000) | 0.9100 (0.9100) | 1.0000 (1.0000) | 1.0000 (1.0000) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:96 | 94096 | 49/50 | 0.7212 (0.7212) | 100 | 0.9275 (0.9275) | 0.9250 (0.9250) | 0.7113 (0.7113) | 0.9250 (0.9250) | 0.9275 (0.9275) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:97 | 94097 | 1/1 | 0.9000 (0.9000) | 100 | 0.9925 (0.9925) | 0.9950 (0.9950) | 0.9000 (0.9000) | 0.9950 (0.9950) | 0.9925 (0.9925) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:98 | 94098 | 391/400 | 0.7150 (0.7150) | 100 | 0.9175 (0.9175) | 0.9150 (0.9150) | 0.7163 (0.7150) | 0.9150 (0.9150) | 0.9175 (0.9175) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:99 | 94099 | 389/400 | 0.7288 (0.7288) | 100 | 0.9150 (0.9150) | 0.9150 (0.9150) | 0.7288 (0.7288) | 0.9150 (0.9150) | 0.9150 (0.9150) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:100 | 94100 | 199/200 | 0.7750 (0.7750) | 100 | 0.9425 (0.9425) | 0.9425 (0.9425) | 0.7675 (0.7675) | 0.9425 (0.9425) | 0.9425 (0.9425) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:101 | 94101 | 199/200 | 0.9500 (0.9500) | 1 | 0.9500 (0.9500) | 0.9525 (0.9525) | 0.9525 (0.9525) | 0.9525 (0.9525) | 0.9500 (0.9500) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:102 | 94102 | 99/100 | 0.6987 (0.6987) | 100 | 0.9550 (0.9550) | 0.9475 (0.9475) | 0.6987 (0.6987) | 0.9475 (0.9475) | 0.9550 (0.9550) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:103 | 94103 | 1/1 | 0.9825 (0.9825) | 1 | 0.9825 (0.9825) | 0.9775 (0.9775) | 0.9775 (0.9775) | 0.9775 (0.9775) | 0.9825 (0.9825) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:104 | 94104 | 393/400 | 0.7850 (0.7850) | 100 | 0.9325 (0.9325) | 0.9350 (0.9350) | 0.7850 (0.7850) | 0.9350 (0.9350) | 0.9325 (0.9325) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:105 | 94105 | 1/1 | 0.9900 (0.9900) | 1 | 0.9900 (0.9900) | 0.9925 (0.9925) | 0.9925 (0.9925) | 0.9925 (0.9925) | 0.9900 (0.9900) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:106 | 94106 | 1/1 | 0.9875 (0.9875) | 1 | 0.9875 (0.9875) | 0.9875 (0.9875) | 0.9875 (0.9875) | 0.9875 (0.9875) | 0.9875 (0.9875) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:107 | 94107 | 1/1 | 0.9850 (0.9850) | 1 | 0.9850 (0.9850) | 0.9850 (0.9850) | 0.9850 (0.9850) | 0.9850 (0.9850) | 0.9850 (0.9850) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:108 | 94108 | 79/80 | 0.9500 (0.9500) | 1 | 0.9500 (0.9500) | 0.9475 (0.9475) | 0.9475 (0.9475) | 0.9475 (0.9475) | 0.9500 (0.9500) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:109 | 94109 | 197/200 | 0.7400 (0.7400) | 100 | 0.9500 (0.9500) | 0.9475 (0.9475) | 0.7400 (0.7400) | 0.9475 (0.9475) | 0.9500 (0.9500) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:110 | 94110 | 199/200 | 0.7575 (0.7575) | 100 | 0.9425 (0.9425) | 0.9450 (0.9450) | 0.7525 (0.7525) | 0.9450 (0.9450) | 0.9425 (0.9425) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:111 | 94111 | 199/200 | 0.8650 (0.8650) | 100 | 0.9550 (0.9550) | 0.9500 (0.9500) | 0.8575 (0.8575) | 0.9500 (0.9500) | 0.9550 (0.9550) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:112 | 94112 | 99/100 | 0.7950 (0.7950) | 100 | 0.9337 (0.9337) | 0.9300 (0.9300) | 0.7950 (0.7950) | 0.9300 (0.9300) | 0.9337 (0.9337) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:113 | 94113 | 1/1 | 0.9975 (0.9975) | 1 | 0.9975 (0.9975) | 0.9975 (0.9975) | 0.9975 (0.9975) | 0.9975 (0.9975) | 0.9975 (0.9975) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:114 | 94114 | 199/200 | 0.8500 (0.8500) | 100 | 0.9850 (0.9850) | 0.9850 (0.9850) | 0.8450 (0.8450) | 0.9850 (0.9850) | 0.9850 (0.9850) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:115 | 94115 | 1/1 | 0.8200 (0.8200) | 100 | 0.9200 (0.9200) | 0.9225 (0.9225) | 0.8200 (0.8200) | 0.9225 (0.9225) | 0.9200 (0.9200) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:116 | 94116 | 397/400 | 0.8287 (0.8287) | 100 | 0.9550 (0.9550) | 0.9550 (0.9550) | 0.8187 (0.8187) | 0.9550 (0.9550) | 0.9550 (0.9550) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:117 | 94117 | 99/100 | 0.9500 (0.9500) | 1 | 0.9500 (0.9500) | 0.9450 (0.9450) | 0.9450 (0.9450) | 0.9450 (0.9450) | 0.9500 (0.9500) | gate passed | gate passed; gate passed; BF fit failure, selection; BF fit failure, selection | - |
| fresh:118 | 94118 | 1/1 | 0.7425 (0.7425) | 100 | 0.9350 (0.9350) | 0.9325 (0.9325) | 0.7425 (0.7425) | 0.9325 (0.9325) | 0.9350 (0.9350) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:119 | 94119 | 199/200 | 0.8050 (0.8050) | 100 | 0.9250 (0.9250) | 0.9300 (0.9300) | 0.8050 (0.8050) | 0.9300 (0.9300) | 0.9250 (0.9250) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:120 | 94120 | 199/200 | 0.7750 (0.7750) | 100 | 0.9375 (0.9375) | 0.9300 (0.9300) | 0.7850 (0.7800) | 0.9300 (0.9300) | 0.9375 (0.9375) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:121 | 94121 | 199/200 | 0.7987 (0.7987) | 100 | 0.9450 (0.9450) | 0.9425 (0.9425) | 0.8013 (0.8013) | 0.9425 (0.9425) | 0.9450 (0.9450) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:122 | 94122 | 1/1 | 0.8325 (0.8325) | 100 | 0.9425 (0.9425) | 0.9225 (0.9225) | 0.8175 (0.8175) | 0.9225 (0.9225) | 0.9425 (0.9425) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:123 | 94123 | 99/100 | 0.7750 (0.7750) | 100 | 0.9387 (0.9387) | 0.9325 (0.9325) | 0.7700 (0.7700) | 0.9325 (0.9325) | 0.9387 (0.9387) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:124 | 94124 | 1/1 | 0.9950 (0.9950) | 1 | 0.9950 (0.9950) | 0.9925 (0.9925) | 0.9925 (0.9925) | 0.9925 (0.9925) | 0.9950 (0.9950) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:125 | 94125 | 197/200 | 0.7350 (0.7350) | 100 | 0.9375 (0.9375) | 0.9275 (0.9275) | 0.7375 (0.7375) | 0.9275 (0.9275) | 0.9375 (0.9375) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:126 | 94126 | 1/1 | 0.9975 (0.9975) | 1 | 0.9975 (0.9975) | 0.9950 (0.9950) | 0.9950 (0.9950) | 0.9950 (0.9950) | 0.9975 (0.9975) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:127 | 94127 | 99/100 | 0.8075 (0.8075) | 100 | 0.9425 (0.9425) | 0.9350 (0.9350) | 0.8075 (0.8075) | 0.9350 (0.9350) | 0.9425 (0.9425) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:128 | 94128 | 199/200 | 0.8250 (0.8250) | 100 | 0.9250 (0.9250) | 0.9250 (0.9250) | 0.8250 (0.8250) | 0.9250 (0.9250) | 0.9250 (0.9250) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:129 | 94129 | 1/1 | 0.9250 (0.9250) | 100 | 1.0000 (1.0000) | 1.0000 (1.0000) | 0.9250 (0.9250) | 1.0000 (1.0000) | 1.0000 (1.0000) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:130 | 94130 | 1/1 | 0.8425 (0.8425) | 100 | 0.9575 (0.9575) | 0.9475 (0.9475) | 0.8425 (0.8425) | 0.9475 (0.9475) | 0.9575 (0.9575) | fit failure, FF-sel | BF fit failure, selection; gate passed; BF fit failure, selection; BF fit failure, selection | - |
| fresh:131 | 94131 | 39/40 | 0.7175 (0.7175) | 100 | 0.9175 (0.9175) | 0.9150 (0.9150) | 0.7175 (0.7175) | 0.9150 (0.9150) | 0.9175 (0.9175) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:132 | 94132 | 1/1 | 0.8163 (0.8163) | 100 | 0.9363 (0.9363) | 0.9350 (0.9350) | 0.8163 (0.8163) | 0.9350 (0.9350) | 0.9363 (0.9363) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:133 | 94133 | 199/200 | 0.9750 (0.9750) | 1 | 0.9750 (0.9750) | 0.9650 (0.9650) | 0.9650 (0.9650) | 0.9650 (0.9650) | 0.9750 (0.9750) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:134 | 94134 | 397/400 | 0.7675 (0.7675) | 100 | 0.9500 (0.9500) | 0.9500 (0.9500) | 0.7675 (0.7675) | 0.9500 (0.9500) | 0.9500 (0.9500) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:135 | 94135 | 199/200 | 0.8625 (0.8625) | 100 | 0.9725 (0.9725) | 0.9750 (0.9750) | 0.8700 (0.8700) | 0.9750 (0.9750) | 0.9725 (0.9725) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:136 | 94136 | 199/200 | 0.7312 (0.7312) | 100 | 0.9275 (0.9275) | 0.9250 (0.9250) | 0.7188 (0.7188) | 0.9250 (0.9250) | 0.9275 (0.9275) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:137 | 94137 | 199/200 | 0.9625 (0.9625) | 1 | 0.9625 (0.9625) | 0.9575 (0.9575) | 0.9575 (0.9575) | 0.9575 (0.9575) | 0.9625 (0.9625) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:138 | 94138 | 199/200 | 0.7700 (0.7700) | 100 | 0.9150 (0.9150) | 0.9200 (0.9200) | 0.7550 (0.7550) | 0.9200 (0.9200) | 0.9150 (0.9150) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:139 | 94139 | 79/80 | 0.8013 (0.8013) | 100 | 0.9700 (0.9700) | 0.9675 (0.9675) | 0.7975 (0.7975) | 0.9675 (0.9675) | 0.9700 (0.9700) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:140 | 94140 | 1/1 | 0.8125 (0.8125) | 100 | 0.9500 (0.9500) | 0.9375 (0.9375) | 0.8125 (0.8125) | 0.9375 (0.9375) | 0.9500 (0.9500) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:141 | 94141 | 1/1 | 1.0000 (1.0000) | 1 | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:142 | 94142 | 1/1 | 0.8675 (0.8675) | 100 | 0.9750 (0.9750) | 0.9775 (0.9775) | 0.8675 (0.8675) | 0.9775 (0.9775) | 0.9750 (0.9750) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:143 | 94143 | 1/1 | 0.8350 (0.8350) | 100 | 1.0000 (1.0000) | 1.0000 (1.0000) | 0.8350 (0.8350) | 1.0000 (1.0000) | 1.0000 (1.0000) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:144 | 94144 | 1/1 | 0.9925 (0.9925) | 1 | 0.9925 (0.9925) | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.9925 (0.9925) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:145 | 94145 | 1/1 | 0.9012 (0.9012) | 100 | 0.9600 (0.9600) | 0.9550 (0.9550) | 0.8862 (0.8862) | 0.9550 (0.9550) | 0.9600 (0.9600) | gate passed | gate passed; gate passed; gate passed; gate passed | DECODER_SPLIT_AT_LC |
| fresh:146 | 94146 | 199/200 | 0.7425 (0.7425) | 100 | 0.8925 (0.8925) | 0.8900 (0.8900) | 0.7425 (0.7425) | 0.8900 (0.8900) | 0.8925 (0.8925) | fit failure, FF-struct or FF-opt, not separated | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:147 | 94147 | 397/400 | 0.8175 (0.8175) | 100 | 0.9650 (0.9650) | 0.9675 (0.9675) | 0.8213 (0.8213) | 0.9675 (0.9675) | 0.9650 (0.9650) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:148 | 94148 | 199/200 | 0.9825 (0.9825) | 1 | 0.9825 (0.9825) | 0.9775 (0.9775) | 0.9775 (0.9775) | 0.9775 (0.9775) | 0.9825 (0.9825) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:149 | 94149 | 199/200 | 0.8350 (0.8350) | 100 | 0.9650 (0.9650) | 0.9575 (0.9575) | 0.8325 (0.8325) | 0.9575 (0.9575) | 0.9650 (0.9650) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:150 | 94150 | 1/1 | 0.8200 (0.8200) | 100 | 0.9325 (0.9325) | 0.9325 (0.9325) | 0.8025 (0.8025) | 0.9313 (0.9325) | 0.9325 (0.9325) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:151 | 94151 | 397/400 | 0.7775 (0.7775) | 100 | 0.8875 (0.8875) | 0.8800 (0.8800) | 0.7775 (0.7775) | 0.8800 (0.8800) | 0.8800 (0.8800) | fit failure, FF-struct or FF-opt, not separated | BF: not separated; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:152 | 94152 | 1/1 | 0.9800 (0.9800) | 1 | 0.9800 (0.9800) | 0.9750 (0.9750) | 0.9750 (0.9750) | 0.9750 (0.9750) | 0.9800 (0.9800) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:153 | 94153 | 199/200 | 0.8363 (0.8363) | 100 | 0.9475 (0.9475) | 0.9425 (0.9425) | 0.8363 (0.8363) | 0.9425 (0.9425) | 0.9475 (0.9475) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:154 | 94154 | 199/200 | 0.8150 (0.8150) | 100 | 0.9250 (0.9250) | 0.9250 (0.9250) | 0.8150 (0.8150) | 0.9250 (0.9250) | 0.9250 (0.9250) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:155 | 94155 | 1/1 | 1.0000 (1.0000) | 1 | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:156 | 94156 | 1/1 | 0.9975 (0.9975) | 1 | 0.9975 (0.9975) | 0.9975 (0.9975) | 0.9975 (0.9975) | 0.9975 (0.9975) | 0.9975 (0.9975) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:157 | 94157 | 199/200 | 0.8275 (0.8275) | 100 | 0.9675 (0.9675) | 0.9700 (0.9700) | 0.8263 (0.8263) | 0.9700 (0.9700) | 0.9675 (0.9675) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:158 | 94158 | 1/1 | 0.9850 (0.9850) | 1 | 0.9850 (0.9850) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9850 (0.9850) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:159 | 94159 | 391/400 | 0.9325 (0.9325) | 1 | 0.9325 (0.9325) | 0.9350 (0.9350) | 0.9350 (0.9350) | 0.9350 (0.9350) | 0.9325 (0.9325) | gate passed | gate passed; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:160 | 94160 | 1/1 | 0.9950 (0.9950) | 1 | 0.9950 (0.9950) | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.9950 (0.9950) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:161 | 94161 | 1/1 | 0.9012 (0.9012) | 100 | 0.9875 (0.9875) | 0.9850 (0.9850) | 0.8925 (0.8925) | 0.9850 (0.9850) | 0.9875 (0.9875) | gate passed | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | DECODER_SPLIT_AT_LC |
| fresh:162 | 94162 | 397/400 | 0.9600 (0.9600) | 1 | 0.9600 (0.9600) | 0.9575 (0.9575) | 0.9575 (0.9575) | 0.9575 (0.9575) | 0.9600 (0.9600) | gate passed | gate passed; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:163 | 94163 | 1/1 | 0.9725 (0.9725) | 1 | 0.9725 (0.9725) | 0.9750 (0.9750) | 0.9750 (0.9750) | 0.9750 (0.9750) | 0.9725 (0.9725) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:164 | 94164 | 397/400 | 0.7500 (0.7500) | 100 | 0.9125 (0.9125) | 0.9100 (0.9100) | 0.7525 (0.7525) | 0.9100 (0.9100) | 0.9125 (0.9125) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:165 | 94165 | 389/400 | 0.7500 (0.7500) | 100 | 0.9100 (0.9100) | 0.9025 (0.9025) | 0.7500 (0.7500) | 0.9025 (0.9025) | 0.9100 (0.9100) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:166 | 94166 | 1/1 | 0.8575 (0.8575) | 100 | 0.9550 (0.9550) | 0.9550 (0.9550) | 0.8575 (0.8575) | 0.9550 (0.9550) | 0.9550 (0.9550) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:167 | 94167 | 197/200 | 0.7175 (0.7175) | 100 | 0.9175 (0.9175) | 0.9150 (0.9150) | 0.7175 (0.7175) | 0.9150 (0.9150) | 0.9175 (0.9175) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:168 | 94168 | 393/400 | 0.7600 (0.7600) | 100 | 0.9150 (0.9150) | 0.9225 (0.9225) | 0.7600 (0.7600) | 0.9225 (0.9225) | 0.9150 (0.9150) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:169 | 94169 | 1/1 | 0.8400 (0.8400) | 100 | 0.9700 (0.9700) | 0.9700 (0.9700) | 0.8350 (0.8350) | 0.9700 (0.9700) | 0.9700 (0.9700) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:170 | 94170 | 1/1 | 0.9325 (0.9325) | 1 | 0.9325 (0.9325) | 0.9375 (0.9375) | 0.9375 (0.9375) | 0.9375 (0.9375) | 0.9325 (0.9325) | gate passed | gate passed; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:171 | 94171 | 199/200 | 0.8025 (0.8025) | 100 | 0.9750 (0.9750) | 0.9725 (0.9725) | 0.8025 (0.8025) | 0.9725 (0.9725) | 0.9750 (0.9750) | fit failure, FF-sel | gate passed; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:172 | 94172 | 99/100 | 0.7200 (0.7200) | 100 | 0.9275 (0.9275) | 0.9150 (0.9150) | 0.7125 (0.7125) | 0.9150 (0.9150) | 0.9275 (0.9275) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:173 | 94173 | 1/1 | 0.9650 (0.9650) | 1 | 0.9650 (0.9650) | 0.9650 (0.9650) | 0.9650 (0.9650) | 0.9650 (0.9650) | 0.9650 (0.9650) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:174 | 94174 | 1/1 | 0.8150 (0.8150) | 100 | 0.9825 (0.9825) | 0.9700 (0.9700) | 0.8150 (0.8150) | 0.9700 (0.9700) | 0.9825 (0.9825) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:175 | 94175 | 199/200 | 0.7688 (0.7688) | 100 | 0.9062 (0.9062) | 0.9125 (0.9125) | 0.7688 (0.7688) | 0.9125 (0.9125) | 0.9062 (0.9062) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:176 | 94176 | 1/1 | 0.9950 (0.9950) | 1 | 0.9950 (0.9950) | 0.9925 (0.9925) | 0.9925 (0.9925) | 0.9925 (0.9925) | 0.9950 (0.9950) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:177 | 94177 | 397/400 | 0.7762 (0.7762) | 100 | 0.9475 (0.9475) | 0.9375 (0.9375) | 0.7762 (0.7762) | 0.9375 (0.9375) | 0.9475 (0.9475) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:178 | 94178 | 391/400 | 0.7550 (0.7550) | 100 | 0.9450 (0.9450) | 0.9350 (0.9350) | 0.7650 (0.7650) | 0.9350 (0.9350) | 0.9450 (0.9450) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:179 | 94179 | 389/400 | 0.6475 (0.6475) | 100 | 0.8975 (0.8975) | 0.8875 (0.8875) | 0.6450 (0.6450) | 0.8875 (0.8875) | 0.8975 (0.8975) | fit failure, FF-struct or FF-opt, not separated | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:180 | 94180 | 397/400 | 0.7712 (0.7712) | 100 | 0.9525 (0.9525) | 0.9475 (0.9475) | 0.7812 (0.7812) | 0.9475 (0.9475) | 0.9525 (0.9525) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:181 | 94181 | 197/200 | 0.9425 (0.9425) | 1 | 0.9425 (0.9425) | 0.9450 (0.9450) | 0.9450 (0.9450) | 0.9450 (0.9450) | 0.9425 (0.9425) | gate passed | gate passed; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:182 | 94182 | 1/1 | 0.9850 (0.9850) | 1 | 0.9850 (0.9850) | 0.9850 (0.9850) | 0.9850 (0.9850) | 0.9850 (0.9850) | 0.9850 (0.9850) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:183 | 94183 | 99/100 | 0.7262 (0.7262) | 100 | 0.9225 (0.9225) | 0.9275 (0.9275) | 0.7262 (0.7262) | 0.9275 (0.9275) | 0.9225 (0.9225) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:184 | 94184 | 79/80 | 0.9500 (0.9500) | 1 | 0.9500 (0.9500) | 0.9450 (0.9450) | 0.9450 (0.9450) | 0.9450 (0.9450) | 0.9500 (0.9500) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:185 | 94185 | 1/1 | 0.9825 (0.9825) | 1 | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9825 (0.9825) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:186 | 94186 | 199/200 | 0.7937 (0.7937) | 100 | 0.9150 (0.9150) | 0.9200 (0.9200) | 0.7937 (0.7937) | 0.9200 (0.9200) | 0.9150 (0.9150) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:187 | 94187 | 1/1 | 0.8550 (0.8550) | 100 | 0.9600 (0.9600) | 0.9475 (0.9475) | 0.8525 (0.8525) | 0.9475 (0.9475) | 0.9600 (0.9600) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:188 | 94188 | 397/400 | 0.8000 (0.8000) | 100 | 0.9600 (0.9600) | 0.9575 (0.9575) | 0.8000 (0.8000) | 0.9575 (0.9575) | 0.9600 (0.9600) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:189 | 94189 | 1/1 | 0.8888 (0.8888) | 100 | 0.9850 (0.9850) | 0.9850 (0.9850) | 0.8875 (0.8875) | 0.9850 (0.9850) | 0.9850 (0.9850) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:190 | 94190 | 1/1 | 0.8762 (0.8762) | 100 | 0.9650 (0.9650) | 0.9650 (0.9650) | 0.8762 (0.8762) | 0.9650 (0.9650) | 0.9650 (0.9650) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:191 | 94191 | 1/1 | 1.0000 (1.0000) | 1 | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:192 | 94192 | 199/200 | 0.9038 (0.9038) | 100 | 0.9712 (0.9712) | 0.9650 (0.9650) | 0.9062 (0.9062) | 0.9675 (0.9675) | 0.9663 (0.9663) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:193 | 94193 | 199/200 | 0.8100 (0.8100) | 100 | 0.9525 (0.9525) | 0.9550 (0.9550) | 0.8100 (0.8100) | 0.9550 (0.9550) | 0.9525 (0.9525) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:194 | 94194 | 1/1 | 0.8750 (0.8750) | 100 | 0.9675 (0.9675) | 0.9600 (0.9600) | 0.8650 (0.8650) | 0.9600 (0.9600) | 0.9675 (0.9675) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:195 | 94195 | 199/200 | 0.9625 (0.9625) | 1 | 0.9625 (0.9625) | 0.9625 (0.9625) | 0.9625 (0.9625) | 0.9625 (0.9625) | 0.9625 (0.9625) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:196 | 94196 | 199/200 | 0.7850 (0.7850) | 100 | 0.9600 (0.9600) | 0.9550 (0.9550) | 0.7800 (0.7800) | 0.9550 (0.9550) | 0.9600 (0.9600) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:197 | 94197 | 397/400 | 0.7913 (0.7913) | 100 | 0.9425 (0.9425) | 0.9375 (0.9375) | 0.7712 (0.7712) | 0.9375 (0.9375) | 0.9425 (0.9425) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:198 | 94198 | 1/1 | 0.9725 (0.9725) | 1 | 0.9725 (0.9725) | 0.9725 (0.9725) | 0.9725 (0.9725) | 0.9725 (0.9725) | 0.9725 (0.9725) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:199 | 94199 | 197/200 | 0.7538 (0.7538) | 100 | 0.9375 (0.9375) | 0.9200 (0.9200) | 0.7550 (0.7550) | 0.9200 (0.9200) | 0.9375 (0.9375) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:200 | 94200 | 1/1 | 0.9500 (0.9500) | 1 | 0.9500 (0.9500) | 0.9625 (0.9625) | 0.9625 (0.9625) | 0.9625 (0.9625) | 0.9500 (0.9500) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:201 | 94201 | 199/200 | 0.8438 (0.8438) | 100 | 0.9675 (0.9675) | 0.9625 (0.9625) | 0.8438 (0.8438) | 0.9625 (0.9625) | 0.9675 (0.9675) | fit failure, FF-sel | BF fit failure, selection; gate passed; BF fit failure, selection; BF fit failure, selection | - |
| fresh:202 | 94202 | 1/1 | 0.8075 (0.8075) | 100 | 0.9575 (0.9575) | 0.9625 (0.9625) | 0.8075 (0.8075) | 0.9625 (0.9625) | 0.9575 (0.9575) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:203 | 94203 | 1/1 | 0.8075 (0.8075) | 100 | 0.9700 (0.9700) | 0.9725 (0.9725) | 0.8175 (0.8175) | 0.9725 (0.9725) | 0.9700 (0.9700) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:204 | 94204 | 1/1 | 0.9975 (0.9975) | 1 | 0.9975 (0.9975) | 0.9975 (0.9975) | 0.9975 (0.9975) | 0.9975 (0.9975) | 0.9975 (0.9975) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:205 | 94205 | 1/1 | 0.9337 (0.9337) | 100 | 1.0000 (1.0000) | 1.0000 (1.0000) | 0.9300 (0.9300) | 1.0000 (1.0000) | 1.0000 (1.0000) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:206 | 94206 | 1/1 | 0.9900 (0.9900) | 1 | 0.9900 (0.9900) | 0.9875 (0.9875) | 0.9875 (0.9875) | 0.9875 (0.9875) | 0.9900 (0.9900) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:207 | 94207 | 397/400 | 0.8087 (0.8087) | 100 | 0.9400 (0.9400) | 0.9425 (0.9425) | 0.8087 (0.8087) | 0.9425 (0.9425) | 0.9400 (0.9400) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:208 | 94208 | 1/1 | 0.9900 (0.9900) | 1 | 0.9900 (0.9900) | 0.9950 (0.9950) | 0.9950 (0.9950) | 0.9950 (0.9950) | 0.9900 (0.9900) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:209 | 94209 | 1/1 | 1.0000 (1.0000) | 1 | 1.0000 (1.0000) | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.9900 (0.9900) | 1.0000 (1.0000) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:210 | 94210 | 1/1 | 0.8700 (0.8700) | 100 | 0.9725 (0.9725) | 0.9725 (0.9725) | 0.8600 (0.8600) | 0.9725 (0.9725) | 0.9725 (0.9725) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:211 | 94211 | 397/400 | 0.8237 (0.8237) | 100 | 0.9625 (0.9625) | 0.9550 (0.9550) | 0.8300 (0.8300) | 0.9550 (0.9550) | 0.9625 (0.9625) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:212 | 94212 | 199/200 | 0.9500 (0.9500) | 1 | 0.9500 (0.9500) | 0.9550 (0.9550) | 0.9550 (0.9550) | 0.9550 (0.9550) | 0.9500 (0.9500) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:213 | 94213 | 1/1 | 0.8400 (0.8400) | 100 | 0.9625 (0.9625) | 0.9700 (0.9700) | 0.8300 (0.8300) | 0.9700 (0.9700) | 0.9625 (0.9625) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:214 | 94214 | 1/1 | 0.8675 (0.8675) | 100 | 1.0000 (1.0000) | 1.0000 (1.0000) | 0.8675 (0.8675) | 1.0000 (1.0000) | 1.0000 (1.0000) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:215 | 94215 | 49/50 | 0.6737 (0.6737) | 100 | 0.9287 (0.9287) | 0.9300 (0.9300) | 0.6737 (0.6737) | 0.9300 (0.9300) | 0.9287 (0.9287) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:216 | 94216 | 1/1 | 0.9800 (0.9800) | 1 | 0.9800 (0.9800) | 0.9800 (0.9800) | 0.9800 (0.9800) | 0.9800 (0.9800) | 0.9800 (0.9800) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:217 | 94217 | 1/1 | 0.9850 (0.9850) | 1 | 0.9850 (0.9850) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9850 (0.9850) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:218 | 94218 | 1/1 | 0.9900 (0.9900) | 1 | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.9900 (0.9900) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:219 | 94219 | 391/400 | 0.6625 (0.6625) | 100 | 0.9150 (0.9150) | 0.9100 (0.9100) | 0.6625 (0.6625) | 0.9100 (0.9100) | 0.9150 (0.9150) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:220 | 94220 | 99/100 | 0.9625 (0.9625) | 1 | 0.9625 (0.9625) | 0.9575 (0.9575) | 0.9575 (0.9575) | 0.9575 (0.9575) | 0.9625 (0.9625) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:221 | 94221 | 1/1 | 0.8150 (0.8150) | 100 | 0.9750 (0.9750) | 0.9625 (0.9625) | 0.8150 (0.8150) | 0.9625 (0.9625) | 0.9750 (0.9750) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:222 | 94222 | 49/50 | 0.7050 (0.7050) | 100 | 0.8975 (0.8975) | 0.8900 (0.8900) | 0.7050 (0.7050) | 0.8900 (0.8900) | 0.8975 (0.8975) | fit failure, FF-struct or FF-opt, not separated | BF: not separated; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:223 | 94223 | 1/1 | 0.9700 (0.9700) | 1 | 0.9700 (0.9700) | 0.9675 (0.9675) | 0.9675 (0.9675) | 0.9675 (0.9675) | 0.9700 (0.9700) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:224 | 94224 | 1/1 | 0.7925 (0.7925) | 100 | 0.9263 (0.9263) | 0.9300 (0.9300) | 0.8025 (0.8025) | 0.9300 (0.9300) | 0.9263 (0.9263) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:225 | 94225 | 397/400 | 0.8200 (0.8200) | 100 | 0.9600 (0.9600) | 0.9550 (0.9550) | 0.8200 (0.8200) | 0.9550 (0.9550) | 0.9600 (0.9600) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:226 | 94226 | 1/1 | 0.9187 (0.9187) | 100 | 0.9925 (0.9925) | 0.9925 (0.9925) | 0.9150 (0.9150) | 0.9925 (0.9925) | 0.9925 (0.9925) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:227 | 94227 | 1/1 | 0.8350 (0.8350) | 100 | 0.9625 (0.9625) | 0.9600 (0.9600) | 0.8200 (0.8200) | 0.9600 (0.9600) | 0.9625 (0.9625) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:228 | 94228 | 1/1 | 0.8350 (0.8350) | 100 | 0.9625 (0.9625) | 0.9650 (0.9650) | 0.8250 (0.8250) | 0.9650 (0.9650) | 0.9625 (0.9625) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:229 | 94229 | 39/40 | 0.7013 (0.7013) | 100 | 0.8650 (0.8650) | 0.8700 (0.8700) | 0.6963 (0.6963) | 0.8700 (0.8700) | 0.8650 (0.8650) | fit failure, FF-struct or FF-opt, not separated | BF: not separated; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:230 | 94230 | 79/80 | 0.8375 (0.8375) | 100 | 0.9500 (0.9500) | 0.9425 (0.9425) | 0.8250 (0.8250) | 0.9425 (0.9425) | 0.9500 (0.9500) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:231 | 94231 | 199/200 | 0.7913 (0.7913) | 100 | 0.9400 (0.9400) | 0.9400 (0.9400) | 0.7913 (0.7913) | 0.9400 (0.9400) | 0.9400 (0.9400) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:232 | 94232 | 1/1 | 0.8200 (0.8200) | 100 | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.8050 (0.8050) | 0.9900 (0.9900) | 0.9900 (0.9900) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:233 | 94233 | 99/100 | 0.9150 (0.9150) | 1 | 0.9150 (0.9150) | 0.9150 (0.9150) | 0.9150 (0.9150) | 0.9150 (0.9150) | 0.9150 (0.9150) | gate passed | gate passed; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:234 | 94234 | 397/400 | 0.7500 (0.7500) | 100 | 0.9675 (0.9675) | 0.9650 (0.9650) | 0.7500 (0.7500) | 0.9650 (0.9650) | 0.9675 (0.9675) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:235 | 94235 | 1/1 | 0.9125 (0.9125) | 100 | 0.9750 (0.9750) | 0.9725 (0.9725) | 0.9100 (0.9100) | 0.9725 (0.9725) | 0.9750 (0.9750) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:236 | 94236 | 199/200 | 0.7100 (0.7100) | 100 | 0.9225 (0.9225) | 0.9250 (0.9250) | 0.7100 (0.7100) | 0.9250 (0.9250) | 0.9225 (0.9225) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:237 | 94237 | 1/1 | 1.0000 (1.0000) | 1 | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:238 | 94238 | 1/1 | 0.8413 (0.8413) | 100 | 0.9650 (0.9650) | 0.9575 (0.9575) | 0.8363 (0.8363) | 0.9575 (0.9575) | 0.9650 (0.9650) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:239 | 94239 | 1/1 | 0.9925 (0.9925) | 1 | 0.9925 (0.9925) | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.9925 (0.9925) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:240 | 94240 | 1/1 | 0.9938 (0.9938) | 1 | 0.9938 (0.9938) | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.9900 (0.9900) | 0.9938 (0.9938) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:241 | 94241 | 199/200 | 0.9825 (0.9825) | 1 | 0.9825 (0.9825) | 0.9850 (0.9850) | 0.9850 (0.9850) | 0.9850 (0.9850) | 0.9825 (0.9825) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:242 | 94242 | 199/200 | 0.9550 (0.9550) | 1 | 0.9550 (0.9550) | 0.9475 (0.9475) | 0.9475 (0.9475) | 0.9475 (0.9475) | 0.9550 (0.9550) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:243 | 94243 | 99/100 | 0.7113 (0.7113) | 100 | 0.9400 (0.9400) | 0.9425 (0.9425) | 0.7113 (0.7113) | 0.9425 (0.9425) | 0.9400 (0.9400) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:244 | 94244 | 389/400 | 0.6950 (0.6950) | 100 | 0.9200 (0.9200) | 0.9200 (0.9200) | 0.6975 (0.6975) | 0.9200 (0.9200) | 0.9200 (0.9200) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:245 | 94245 | 1/1 | 1.0000 (1.0000) | 1 | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:246 | 94246 | 199/200 | 0.9575 (0.9575) | 1 | 0.9575 (0.9575) | 0.9550 (0.9550) | 0.9550 (0.9550) | 0.9550 (0.9550) | 0.9575 (0.9575) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:247 | 94247 | 79/80 | 0.7475 (0.7475) | 100 | 0.9125 (0.9125) | 0.9125 (0.9125) | 0.7475 (0.7475) | 0.9125 (0.9125) | 0.9125 (0.9125) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:248 | 94248 | 199/200 | 0.8337 (0.8337) | 100 | 0.9575 (0.9575) | 0.9600 (0.9600) | 0.8313 (0.8313) | 0.9600 (0.9600) | 0.9575 (0.9575) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:249 | 94249 | 391/400 | 0.7500 (0.7500) | 100 | 0.9325 (0.9325) | 0.9375 (0.9375) | 0.7500 (0.7500) | 0.9375 (0.9375) | 0.9325 (0.9325) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:250 | 94250 | 199/200 | 0.9725 (0.9725) | 1 | 0.9725 (0.9725) | 0.9700 (0.9700) | 0.9700 (0.9700) | 0.9700 (0.9700) | 0.9725 (0.9725) | gate passed | gate passed; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:251 | 94251 | 1/1 | 0.8438 (0.8438) | 100 | 0.9575 (0.9575) | 0.9600 (0.9600) | 0.8438 (0.8438) | 0.9600 (0.9600) | 0.9575 (0.9575) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:252 | 94252 | 199/200 | 0.8425 (0.8425) | 100 | 0.9475 (0.9475) | 0.9425 (0.9425) | 0.8375 (0.8375) | 0.9425 (0.9425) | 0.9475 (0.9475) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:253 | 94253 | 199/200 | 0.9750 (0.9750) | 1 | 0.9750 (0.9750) | 0.9725 (0.9725) | 0.9725 (0.9725) | 0.9725 (0.9725) | 0.9750 (0.9750) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:254 | 94254 | 99/100 | 0.8000 (0.8000) | 100 | 0.9425 (0.9425) | 0.9450 (0.9450) | 0.8050 (0.8000) | 0.9450 (0.9450) | 0.9425 (0.9425) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:255 | 94255 | 199/200 | 0.8638 (0.8638) | 100 | 0.9625 (0.9625) | 0.9625 (0.9625) | 0.8488 (0.8488) | 0.9625 (0.9625) | 0.9625 (0.9625) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:256 | 94256 | 1/1 | 0.8750 (0.8750) | 100 | 0.9313 (0.9313) | 0.9300 (0.9300) | 0.8750 (0.8750) | 0.9300 (0.9300) | 0.9313 (0.9313) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:257 | 94257 | 199/200 | 0.8087 (0.8087) | 100 | 0.9575 (0.9575) | 0.9550 (0.9550) | 0.8087 (0.8087) | 0.9550 (0.9550) | 0.9575 (0.9575) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:258 | 94258 | 1/1 | 0.9900 (0.9900) | 1 | 0.9900 (0.9900) | 0.9850 (0.9850) | 0.9850 (0.9850) | 0.9850 (0.9850) | 0.9900 (0.9900) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:259 | 94259 | 1/1 | 0.9800 (0.9800) | 1 | 0.9800 (0.9800) | 0.9775 (0.9775) | 0.9775 (0.9775) | 0.9775 (0.9775) | 0.9800 (0.9800) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:260 | 94260 | 1/1 | 0.9850 (0.9850) | 1 | 0.9850 (0.9850) | 0.9875 (0.9875) | 0.9875 (0.9875) | 0.9875 (0.9875) | 0.9850 (0.9850) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:261 | 94261 | 1/1 | 0.9263 (0.9263) | 100 | 0.9925 (0.9925) | 0.9925 (0.9925) | 0.9213 (0.9213) | 0.9925 (0.9925) | 0.9925 (0.9925) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:262 | 94262 | 1/1 | 0.9475 (0.9475) | 1 | 0.9475 (0.9475) | 0.9525 (0.9525) | 0.9525 (0.9525) | 0.9525 (0.9525) | 0.9475 (0.9475) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:263 | 94263 | 79/80 | 0.9525 (0.9525) | 1 | 0.9525 (0.9525) | 0.9525 (0.9525) | 0.9525 (0.9525) | 0.9525 (0.9525) | 0.9525 (0.9525) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:264 | 94264 | 1/1 | 0.9800 (0.9800) | 1 | 0.9800 (0.9800) | 0.9775 (0.9775) | 0.9775 (0.9775) | 0.9775 (0.9775) | 0.9800 (0.9800) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:265 | 94265 | 199/200 | 0.9525 (0.9525) | 1 | 0.9525 (0.9525) | 0.9625 (0.9625) | 0.9625 (0.9625) | 0.9625 (0.9625) | 0.9525 (0.9525) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:266 | 94266 | 1/1 | 0.8988 (0.8988) | 100 | 0.9725 (0.9725) | 0.9700 (0.9700) | 0.9000 (0.9000) | 0.9700 (0.9700) | 0.9725 (0.9725) | fit failure, FF-sel; and FF-quant at lambda_c (the float fit at lambda_c passed, the quantised one did not) | gate passed; gate passed; gate passed; gate passed | DECODER_SPLIT_AT_LC |
| fresh:267 | 94267 | 1/1 | 0.8588 (0.8588) | 100 | 0.9950 (0.9950) | 0.9925 (0.9925) | 0.8625 (0.8625) | 0.9925 (0.9925) | 0.9950 (0.9950) | fit failure, FF-sel | gate passed; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:268 | 94268 | 1/1 | 0.9225 (0.9225) | 100 | 0.9862 (0.9862) | 0.9825 (0.9825) | 0.9150 (0.9150) | 0.9825 (0.9825) | 0.9862 (0.9862) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:269 | 94269 | 1/1 | 0.8375 (0.8375) | 100 | 0.9525 (0.9525) | 0.9500 (0.9500) | 0.8375 (0.8375) | 0.9500 (0.9500) | 0.9525 (0.9525) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:270 | 94270 | 1/1 | 0.9850 (0.9850) | 1 | 0.9850 (0.9850) | 0.9850 (0.9850) | 0.9850 (0.9850) | 0.9850 (0.9850) | 0.9850 (0.9850) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:271 | 94271 | 199/200 | 0.8425 (0.8425) | 100 | 0.9700 (0.9700) | 0.9725 (0.9725) | 0.8425 (0.8425) | 0.9725 (0.9725) | 0.9700 (0.9700) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:272 | 94272 | 397/400 | 0.8275 (0.8275) | 100 | 0.9625 (0.9625) | 0.9625 (0.9625) | 0.8275 (0.8275) | 0.9625 (0.9625) | 0.9625 (0.9625) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:273 | 94273 | 1/1 | 0.8688 (0.8688) | 100 | 0.9475 (0.9475) | 0.9450 (0.9450) | 0.8688 (0.8688) | 0.9450 (0.9450) | 0.9475 (0.9475) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:274 | 94274 | 1/1 | 0.9750 (0.9750) | 1 | 0.9750 (0.9750) | 0.9775 (0.9775) | 0.9775 (0.9775) | 0.9775 (0.9775) | 0.9750 (0.9750) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:275 | 94275 | 99/100 | 0.9525 (0.9525) | 1 | 0.9525 (0.9525) | 0.9450 (0.9450) | 0.9450 (0.9450) | 0.9450 (0.9450) | 0.9525 (0.9525) | gate passed | gate passed; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:276 | 94276 | 1/1 | 0.9800 (0.9800) | 1 | 0.9800 (0.9800) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9800 (0.9800) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:277 | 94277 | 1/1 | 0.7963 (0.7963) | 100 | 0.9175 (0.9175) | 0.9275 (0.9275) | 0.7963 (0.7963) | 0.9250 (0.9250) | 0.9150 (0.9150) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:278 | 94278 | 397/400 | 0.8075 (0.8075) | 100 | 0.9600 (0.9600) | 0.9550 (0.9550) | 0.8100 (0.8100) | 0.9550 (0.9550) | 0.9600 (0.9600) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:279 | 94279 | 1/1 | 0.9825 (0.9825) | 1 | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9825 (0.9825) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:280 | 94280 | 1/1 | 0.9775 (0.9775) | 1 | 0.9775 (0.9775) | 0.9750 (0.9750) | 0.9750 (0.9750) | 0.9750 (0.9750) | 0.9775 (0.9775) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:281 | 94281 | 397/400 | 0.7050 (0.7050) | 100 | 0.9550 (0.9550) | 0.9550 (0.9550) | 0.6937 (0.7050) | 0.9550 (0.9550) | 0.9550 (0.9550) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:282 | 94282 | 393/400 | 0.9350 (0.9350) | 1 | 0.9350 (0.9350) | 0.9375 (0.9375) | 0.9375 (0.9375) | 0.9375 (0.9375) | 0.9350 (0.9350) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:283 | 94283 | 391/400 | 0.6987 (0.6987) | 100 | 0.9000 (0.9000) | 0.9100 (0.9100) | 0.6987 (0.6987) | 0.9100 (0.9100) | 0.9000 (0.9000) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:284 | 94284 | 79/80 | 0.9600 (0.9600) | 1 | 0.9600 (0.9600) | 0.9600 (0.9600) | 0.9600 (0.9600) | 0.9600 (0.9600) | 0.9600 (0.9600) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:285 | 94285 | 397/400 | 0.7812 (0.7812) | 100 | 0.9450 (0.9450) | 0.9400 (0.9400) | 0.7800 (0.7800) | 0.9400 (0.9400) | 0.9450 (0.9450) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:286 | 94286 | 199/200 | 0.8087 (0.8087) | 100 | 0.9450 (0.9450) | 0.9500 (0.9500) | 0.8087 (0.8087) | 0.9500 (0.9500) | 0.9450 (0.9450) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:287 | 94287 | 1/1 | 0.8313 (0.8313) | 100 | 0.9650 (0.9650) | 0.9650 (0.9650) | 0.8313 (0.8313) | 0.9650 (0.9650) | 0.9650 (0.9650) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:288 | 94288 | 1/1 | 0.8750 (0.8750) | 100 | 0.9700 (0.9700) | 0.9700 (0.9700) | 0.8650 (0.8650) | 0.9700 (0.9700) | 0.9700 (0.9700) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:289 | 94289 | 79/80 | 0.7850 (0.7850) | 100 | 0.9350 (0.9350) | 0.9350 (0.9350) | 0.7800 (0.7800) | 0.9300 (0.9300) | 0.9325 (0.9325) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:290 | 94290 | 1/1 | 0.8375 (0.8375) | 100 | 0.9700 (0.9700) | 0.9625 (0.9625) | 0.8375 (0.8375) | 0.9625 (0.9625) | 0.9700 (0.9700) | fit failure, FF-sel | BF fit failure, selection; gate passed; gate passed; gate passed | - |
| fresh:291 | 94291 | 1/1 | 0.9550 (0.9550) | 1 | 0.9550 (0.9550) | 0.9575 (0.9575) | 0.9575 (0.9575) | 0.9575 (0.9575) | 0.9550 (0.9550) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:292 | 94292 | 49/50 | 0.7150 (0.7150) | 100 | 0.9075 (0.9075) | 0.9075 (0.9075) | 0.7150 (0.7150) | 0.9075 (0.9075) | 0.9075 (0.9075) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:293 | 94293 | 1/1 | 0.9825 (0.9825) | 1 | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9825 (0.9825) | 0.9825 (0.9825) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:294 | 94294 | 1/1 | 0.9650 (0.9650) | 1 | 0.9650 (0.9650) | 0.9650 (0.9650) | 0.9650 (0.9650) | 0.9650 (0.9650) | 0.9650 (0.9650) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:295 | 94295 | 197/200 | 0.7825 (0.7825) | 100 | 0.9275 (0.9275) | 0.9225 (0.9225) | 0.7775 (0.7775) | 0.9225 (0.9225) | 0.9275 (0.9275) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:296 | 94296 | 199/200 | 0.9437 (0.9437) | 1 | 0.9437 (0.9437) | 0.9375 (0.9375) | 0.9375 (0.9375) | 0.9375 (0.9375) | 0.9437 (0.9437) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:297 | 94297 | 199/200 | 0.6725 (0.6725) | 100 | 0.9125 (0.9125) | 0.9200 (0.9200) | 0.6750 (0.6750) | 0.9200 (0.9200) | 0.9125 (0.9125) | fit failure, FF-sel | BF fit failure, selection; BF fit failure, selection; BF fit failure, selection; BF fit failure, selection | - |
| fresh:298 | 94298 | 1/1 | 0.9725 (0.9725) | 1 | 0.9725 (0.9725) | 0.9725 (0.9725) | 0.9725 (0.9725) | 0.9725 (0.9725) | 0.9725 (0.9725) | gate passed | gate passed; gate passed; gate passed; gate passed | - |
| fresh:299 | 94299 | 397/400 | 0.9650 (0.9650) | 1 | 0.9650 (0.9650) | 0.9650 (0.9650) | 0.9650 (0.9650) | 0.9650 (0.9650) | 0.9650 (0.9650) | gate passed | gate passed; gate passed; gate passed; gate passed | - |

## (iii): passes at lambda = 1 (section 10; printed, decides nothing)

| key | j | seed | lambda_c | ceiling_block | ceiling_block_tau | ceil_1 | ceil_1_tau | n1_block | n1_block_tau | gap | gap_tau |
|---|---|---|---|---|---|---|---|---|---|---|---|
| fresh:1 | 1 | 94001 | 1.000000 | 0.967500 | 0.967500 | 0.967500 | 0.967500 | 0.752500 | 0.752500 | 0.215000 | 0.215000 |
| fresh:2 | 2 | 94002 | 1.000000 | 0.997500 | 0.997500 | 0.997500 | 0.997500 | 0.930000 | 0.930000 | 0.067500 | 0.067500 |
| fresh:3 | 3 | 94003 | 1.000000 | 0.990000 | 0.990000 | 0.990000 | 0.990000 | 0.877500 | 0.877500 | 0.112500 | 0.112500 |
| fresh:4 | 4 | 94004 | 1.000000 | 0.975000 | 0.975000 | 0.975000 | 0.975000 | 0.787500 | 0.787500 | 0.187500 | 0.187500 |
| fresh:6 | 6 | 94006 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 0.850000 | 0.850000 | 0.150000 | 0.150000 |
| fresh:9 | 9 | 94009 | 1.000000 | 0.970000 | 0.970000 | 0.970000 | 0.970000 | 0.797500 | 0.797500 | 0.172500 | 0.172500 |
| fresh:10 | 10 | 94010 | 1.000000 | 0.952500 | 0.952500 | 0.952500 | 0.952500 | 0.721250 | 0.721250 | 0.231250 | 0.231250 |
| fresh:12 | 12 | 94012 | 1.000000 | 0.977500 | 0.977500 | 0.977500 | 0.977500 | 0.817500 | 0.817500 | 0.160000 | 0.160000 |
| fresh:15 | 15 | 94015 | 1.000000 | 0.955000 | 0.955000 | 0.955000 | 0.955000 | 0.843750 | 0.843750 | 0.111250 | 0.111250 |
| fresh:16 | 16 | 94016 | 1.000000 | 0.977500 | 0.977500 | 0.977500 | 0.977500 | 0.825000 | 0.825000 | 0.152500 | 0.152500 |
| fresh:19 | 19 | 94019 | 1.000000 | 0.935000 | 0.935000 | 0.935000 | 0.935000 | 0.660000 | 0.660000 | 0.275000 | 0.275000 |
| fresh:21 | 21 | 94021 | 1.000000 | 0.990000 | 0.990000 | 0.990000 | 0.990000 | 0.827500 | 0.827500 | 0.162500 | 0.162500 |
| fresh:23 | 23 | 94023 | 1.000000 | 0.957500 | 0.957500 | 0.957500 | 0.957500 | 0.830000 | 0.830000 | 0.127500 | 0.127500 |
| fresh:27 | 27 | 94027 | 1.000000 | 0.983750 | 0.983750 | 0.983750 | 0.983750 | 0.881250 | 0.881250 | 0.102500 | 0.102500 |
| fresh:30 | 30 | 94030 | 1.000000 | 0.990000 | 0.990000 | 0.990000 | 0.990000 | 0.920000 | 0.920000 | 0.070000 | 0.070000 |
| fresh:33 | 33 | 94033 | 1.000000 | 0.980000 | 0.980000 | 0.980000 | 0.980000 | 0.757500 | 0.757500 | 0.222500 | 0.222500 |
| fresh:35 | 35 | 94035 | 1.000000 | 0.990000 | 0.990000 | 0.990000 | 0.990000 | 0.841250 | 0.841250 | 0.148750 | 0.148750 |
| fresh:36 | 36 | 94036 | 1.000000 | 0.977500 | 0.977500 | 0.977500 | 0.977500 | 0.860000 | 0.860000 | 0.117500 | 0.117500 |
| fresh:39 | 39 | 94039 | 1.000000 | 0.967500 | 0.967500 | 0.967500 | 0.967500 | 0.762500 | 0.762500 | 0.205000 | 0.205000 |
| fresh:41 | 41 | 94041 | 1.000000 | 0.977500 | 0.977500 | 0.977500 | 0.977500 | 0.777500 | 0.777500 | 0.200000 | 0.200000 |
| fresh:42 | 42 | 94042 | 1.000000 | 0.995000 | 0.995000 | 0.995000 | 0.995000 | 0.710000 | 0.710000 | 0.285000 | 0.285000 |
| fresh:44 | 44 | 94044 | 1.000000 | 0.992500 | 0.992500 | 0.992500 | 0.992500 | 0.777500 | 0.777500 | 0.215000 | 0.215000 |
| fresh:45 | 45 | 94045 | 1.000000 | 0.985000 | 0.985000 | 0.985000 | 0.985000 | 0.870000 | 0.870000 | 0.115000 | 0.115000 |
| fresh:46 | 46 | 94046 | 1.000000 | 0.962500 | 0.962500 | 0.962500 | 0.962500 | 0.705000 | 0.705000 | 0.257500 | 0.257500 |
| fresh:51 | 51 | 94051 | 1.000000 | 0.977500 | 0.977500 | 0.977500 | 0.977500 | 0.802500 | 0.802500 | 0.175000 | 0.175000 |
| fresh:56 | 56 | 94056 | 1.000000 | 0.957500 | 0.957500 | 0.957500 | 0.957500 | 0.880000 | 0.880000 | 0.077500 | 0.077500 |
| fresh:57 | 57 | 94057 | 1.000000 | 0.942500 | 0.942500 | 0.942500 | 0.942500 | 0.680000 | 0.680000 | 0.262500 | 0.262500 |
| fresh:60 | 60 | 94060 | 1.000000 | 0.972500 | 0.972500 | 0.972500 | 0.972500 | 0.783750 | 0.783750 | 0.188750 | 0.188750 |
| fresh:62 | 62 | 94062 | 1.000000 | 0.987500 | 0.987500 | 0.987500 | 0.987500 | 0.875000 | 0.875000 | 0.112500 | 0.112500 |
| fresh:63 | 63 | 94063 | 1.000000 | 0.990000 | 0.990000 | 0.990000 | 0.990000 | 0.825000 | 0.825000 | 0.165000 | 0.165000 |
| fresh:64 | 64 | 94064 | 1.000000 | 0.990000 | 0.990000 | 0.990000 | 0.990000 | 0.760000 | 0.760000 | 0.230000 | 0.230000 |
| fresh:65 | 65 | 94065 | 1.000000 | 0.990000 | 0.990000 | 0.990000 | 0.990000 | 0.731250 | 0.731250 | 0.258750 | 0.258750 |
| fresh:66 | 66 | 94066 | 1.000000 | 0.955000 | 0.955000 | 0.955000 | 0.955000 | 0.728750 | 0.728750 | 0.226250 | 0.226250 |
| fresh:77 | 77 | 94077 | 1.000000 | 0.960000 | 0.960000 | 0.960000 | 0.960000 | 0.771250 | 0.771250 | 0.188750 | 0.188750 |
| fresh:81 | 81 | 94081 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 0.881250 | 0.881250 | 0.118750 | 0.118750 |
| fresh:86 | 86 | 94086 | 1.000000 | 0.987500 | 0.987500 | 0.987500 | 0.987500 | 0.852500 | 0.852500 | 0.135000 | 0.135000 |
| fresh:87 | 87 | 94087 | 1.000000 | 0.987500 | 0.987500 | 0.987500 | 0.987500 | 0.750000 | 0.750000 | 0.237500 | 0.237500 |
| fresh:89 | 89 | 94089 | 1.000000 | 0.982500 | 0.982500 | 0.982500 | 0.982500 | 0.852500 | 0.852500 | 0.130000 | 0.130000 |
| fresh:92 | 92 | 94092 | 1.000000 | 0.982500 | 0.982500 | 0.982500 | 0.982500 | 0.737500 | 0.737500 | 0.245000 | 0.245000 |
| fresh:101 | 101 | 94101 | 1.000000 | 0.950000 | 0.950000 | 0.950000 | 0.950000 | 0.747500 | 0.747500 | 0.202500 | 0.202500 |
| fresh:103 | 103 | 94103 | 1.000000 | 0.982500 | 0.982500 | 0.982500 | 0.982500 | 0.752500 | 0.752500 | 0.230000 | 0.230000 |
| fresh:105 | 105 | 94105 | 1.000000 | 0.990000 | 0.990000 | 0.990000 | 0.990000 | 0.882500 | 0.882500 | 0.107500 | 0.107500 |
| fresh:106 | 106 | 94106 | 1.000000 | 0.987500 | 0.987500 | 0.987500 | 0.987500 | 0.805000 | 0.805000 | 0.182500 | 0.182500 |
| fresh:107 | 107 | 94107 | 1.000000 | 0.985000 | 0.985000 | 0.985000 | 0.985000 | 0.895000 | 0.895000 | 0.090000 | 0.090000 |
| fresh:108 | 108 | 94108 | 1.000000 | 0.950000 | 0.950000 | 0.950000 | 0.950000 | 0.710000 | 0.710000 | 0.240000 | 0.240000 |
| fresh:113 | 113 | 94113 | 1.000000 | 0.997500 | 0.997500 | 0.997500 | 0.997500 | 0.940000 | 0.940000 | 0.057500 | 0.057500 |
| fresh:117 | 117 | 94117 | 1.000000 | 0.950000 | 0.950000 | 0.950000 | 0.950000 | 0.782500 | 0.782500 | 0.167500 | 0.167500 |
| fresh:124 | 124 | 94124 | 1.000000 | 0.995000 | 0.995000 | 0.995000 | 0.995000 | 0.722500 | 0.722500 | 0.272500 | 0.272500 |
| fresh:126 | 126 | 94126 | 1.000000 | 0.997500 | 0.997500 | 0.997500 | 0.997500 | 0.928750 | 0.928750 | 0.068750 | 0.068750 |
| fresh:133 | 133 | 94133 | 1.000000 | 0.975000 | 0.975000 | 0.975000 | 0.975000 | 0.820000 | 0.820000 | 0.155000 | 0.155000 |
| fresh:137 | 137 | 94137 | 1.000000 | 0.962500 | 0.962500 | 0.962500 | 0.962500 | 0.807500 | 0.807500 | 0.155000 | 0.155000 |
| fresh:141 | 141 | 94141 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 0.910000 | 0.910000 | 0.090000 | 0.090000 |
| fresh:144 | 144 | 94144 | 1.000000 | 0.992500 | 0.992500 | 0.992500 | 0.992500 | 0.862500 | 0.862500 | 0.130000 | 0.130000 |
| fresh:148 | 148 | 94148 | 1.000000 | 0.982500 | 0.982500 | 0.982500 | 0.982500 | 0.850000 | 0.850000 | 0.132500 | 0.132500 |
| fresh:152 | 152 | 94152 | 1.000000 | 0.980000 | 0.980000 | 0.980000 | 0.980000 | 0.757500 | 0.757500 | 0.222500 | 0.222500 |
| fresh:155 | 155 | 94155 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 0.872500 | 0.872500 | 0.127500 | 0.127500 |
| fresh:156 | 156 | 94156 | 1.000000 | 0.997500 | 0.997500 | 0.997500 | 0.997500 | 0.865000 | 0.865000 | 0.132500 | 0.132500 |
| fresh:158 | 158 | 94158 | 1.000000 | 0.985000 | 0.985000 | 0.985000 | 0.985000 | 0.767500 | 0.767500 | 0.217500 | 0.217500 |
| fresh:159 | 159 | 94159 | 1.000000 | 0.932500 | 0.932500 | 0.932500 | 0.932500 | 0.700000 | 0.700000 | 0.232500 | 0.232500 |
| fresh:160 | 160 | 94160 | 1.000000 | 0.995000 | 0.995000 | 0.995000 | 0.995000 | 0.867500 | 0.867500 | 0.127500 | 0.127500 |
| fresh:162 | 162 | 94162 | 1.000000 | 0.960000 | 0.960000 | 0.960000 | 0.960000 | 0.770000 | 0.770000 | 0.190000 | 0.190000 |
| fresh:163 | 163 | 94163 | 1.000000 | 0.972500 | 0.972500 | 0.972500 | 0.972500 | 0.847500 | 0.847500 | 0.125000 | 0.125000 |
| fresh:170 | 170 | 94170 | 1.000000 | 0.932500 | 0.932500 | 0.932500 | 0.932500 | 0.820000 | 0.820000 | 0.112500 | 0.112500 |
| fresh:173 | 173 | 94173 | 1.000000 | 0.965000 | 0.965000 | 0.965000 | 0.965000 | 0.745000 | 0.745000 | 0.220000 | 0.220000 |
| fresh:176 | 176 | 94176 | 1.000000 | 0.995000 | 0.995000 | 0.995000 | 0.995000 | 0.825000 | 0.825000 | 0.170000 | 0.170000 |
| fresh:181 | 181 | 94181 | 1.000000 | 0.942500 | 0.942500 | 0.942500 | 0.942500 | 0.742500 | 0.742500 | 0.200000 | 0.200000 |
| fresh:182 | 182 | 94182 | 1.000000 | 0.985000 | 0.985000 | 0.985000 | 0.985000 | 0.787500 | 0.787500 | 0.197500 | 0.197500 |
| fresh:184 | 184 | 94184 | 1.000000 | 0.950000 | 0.950000 | 0.950000 | 0.950000 | 0.737500 | 0.737500 | 0.212500 | 0.212500 |
| fresh:185 | 185 | 94185 | 1.000000 | 0.982500 | 0.982500 | 0.982500 | 0.982500 | 0.790000 | 0.790000 | 0.192500 | 0.192500 |
| fresh:191 | 191 | 94191 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 0.862500 | 0.862500 | 0.137500 | 0.137500 |
| fresh:195 | 195 | 94195 | 1.000000 | 0.962500 | 0.962500 | 0.962500 | 0.962500 | 0.670000 | 0.670000 | 0.292500 | 0.292500 |
| fresh:198 | 198 | 94198 | 1.000000 | 0.972500 | 0.972500 | 0.972500 | 0.972500 | 0.730000 | 0.730000 | 0.242500 | 0.242500 |
| fresh:200 | 200 | 94200 | 1.000000 | 0.950000 | 0.950000 | 0.950000 | 0.950000 | 0.791250 | 0.791250 | 0.158750 | 0.158750 |
| fresh:204 | 204 | 94204 | 1.000000 | 0.997500 | 0.997500 | 0.997500 | 0.997500 | 0.883750 | 0.883750 | 0.113750 | 0.113750 |
| fresh:206 | 206 | 94206 | 1.000000 | 0.990000 | 0.990000 | 0.990000 | 0.990000 | 0.860000 | 0.860000 | 0.130000 | 0.130000 |
| fresh:208 | 208 | 94208 | 1.000000 | 0.990000 | 0.990000 | 0.990000 | 0.990000 | 0.842500 | 0.842500 | 0.147500 | 0.147500 |
| fresh:209 | 209 | 94209 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 0.855000 | 0.855000 | 0.145000 | 0.145000 |
| fresh:212 | 212 | 94212 | 1.000000 | 0.950000 | 0.950000 | 0.950000 | 0.950000 | 0.790000 | 0.790000 | 0.160000 | 0.160000 |
| fresh:216 | 216 | 94216 | 1.000000 | 0.980000 | 0.980000 | 0.980000 | 0.980000 | 0.787500 | 0.787500 | 0.192500 | 0.192500 |
| fresh:217 | 217 | 94217 | 1.000000 | 0.985000 | 0.985000 | 0.985000 | 0.985000 | 0.847500 | 0.847500 | 0.137500 | 0.137500 |
| fresh:218 | 218 | 94218 | 1.000000 | 0.990000 | 0.990000 | 0.990000 | 0.990000 | 0.855000 | 0.855000 | 0.135000 | 0.135000 |
| fresh:220 | 220 | 94220 | 1.000000 | 0.962500 | 0.962500 | 0.962500 | 0.962500 | 0.831250 | 0.831250 | 0.131250 | 0.131250 |
| fresh:223 | 223 | 94223 | 1.000000 | 0.970000 | 0.970000 | 0.970000 | 0.970000 | 0.750000 | 0.750000 | 0.220000 | 0.220000 |
| fresh:233 | 233 | 94233 | 1.000000 | 0.915000 | 0.915000 | 0.915000 | 0.915000 | 0.687500 | 0.687500 | 0.227500 | 0.227500 |
| fresh:237 | 237 | 94237 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 0.822500 | 0.822500 | 0.177500 | 0.177500 |
| fresh:239 | 239 | 94239 | 1.000000 | 0.992500 | 0.992500 | 0.992500 | 0.992500 | 0.955000 | 0.955000 | 0.037500 | 0.037500 |
| fresh:240 | 240 | 94240 | 1.000000 | 0.993750 | 0.993750 | 0.993750 | 0.993750 | 0.872500 | 0.872500 | 0.121250 | 0.121250 |
| fresh:241 | 241 | 94241 | 1.000000 | 0.982500 | 0.982500 | 0.982500 | 0.982500 | 0.740000 | 0.740000 | 0.242500 | 0.242500 |
| fresh:242 | 242 | 94242 | 1.000000 | 0.955000 | 0.955000 | 0.955000 | 0.955000 | 0.820000 | 0.820000 | 0.135000 | 0.135000 |
| fresh:245 | 245 | 94245 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 0.872500 | 0.872500 | 0.127500 | 0.127500 |
| fresh:246 | 246 | 94246 | 1.000000 | 0.957500 | 0.957500 | 0.957500 | 0.957500 | 0.687500 | 0.687500 | 0.270000 | 0.270000 |
| fresh:250 | 250 | 94250 | 1.000000 | 0.972500 | 0.972500 | 0.972500 | 0.972500 | 0.833750 | 0.833750 | 0.138750 | 0.138750 |
| fresh:253 | 253 | 94253 | 1.000000 | 0.975000 | 0.975000 | 0.975000 | 0.975000 | 0.827500 | 0.827500 | 0.147500 | 0.147500 |
| fresh:258 | 258 | 94258 | 1.000000 | 0.990000 | 0.990000 | 0.990000 | 0.990000 | 0.787500 | 0.787500 | 0.202500 | 0.202500 |
| fresh:259 | 259 | 94259 | 1.000000 | 0.980000 | 0.980000 | 0.980000 | 0.980000 | 0.735000 | 0.735000 | 0.245000 | 0.245000 |
| fresh:260 | 260 | 94260 | 1.000000 | 0.985000 | 0.985000 | 0.985000 | 0.985000 | 0.765000 | 0.765000 | 0.220000 | 0.220000 |
| fresh:262 | 262 | 94262 | 1.000000 | 0.947500 | 0.947500 | 0.947500 | 0.947500 | 0.797500 | 0.797500 | 0.150000 | 0.150000 |
| fresh:263 | 263 | 94263 | 1.000000 | 0.952500 | 0.952500 | 0.952500 | 0.952500 | 0.671250 | 0.671250 | 0.281250 | 0.281250 |
| fresh:264 | 264 | 94264 | 1.000000 | 0.980000 | 0.980000 | 0.980000 | 0.980000 | 0.810000 | 0.810000 | 0.170000 | 0.170000 |
| fresh:265 | 265 | 94265 | 1.000000 | 0.952500 | 0.952500 | 0.952500 | 0.952500 | 0.770000 | 0.770000 | 0.182500 | 0.182500 |
| fresh:270 | 270 | 94270 | 1.000000 | 0.985000 | 0.985000 | 0.985000 | 0.985000 | 0.790000 | 0.790000 | 0.195000 | 0.195000 |
| fresh:274 | 274 | 94274 | 1.000000 | 0.975000 | 0.975000 | 0.975000 | 0.975000 | 0.837500 | 0.837500 | 0.137500 | 0.137500 |
| fresh:275 | 275 | 94275 | 1.000000 | 0.952500 | 0.952500 | 0.952500 | 0.952500 | 0.780000 | 0.775000 | 0.172500 | 0.177500 |
| fresh:276 | 276 | 94276 | 1.000000 | 0.980000 | 0.980000 | 0.980000 | 0.980000 | 0.846250 | 0.846250 | 0.133750 | 0.133750 |
| fresh:279 | 279 | 94279 | 1.000000 | 0.982500 | 0.982500 | 0.982500 | 0.982500 | 0.811250 | 0.811250 | 0.171250 | 0.171250 |
| fresh:280 | 280 | 94280 | 1.000000 | 0.977500 | 0.977500 | 0.977500 | 0.977500 | 0.806250 | 0.806250 | 0.171250 | 0.171250 |
| fresh:282 | 282 | 94282 | 1.000000 | 0.935000 | 0.935000 | 0.935000 | 0.935000 | 0.727500 | 0.727500 | 0.207500 | 0.207500 |
| fresh:284 | 284 | 94284 | 1.000000 | 0.960000 | 0.960000 | 0.960000 | 0.960000 | 0.720000 | 0.720000 | 0.240000 | 0.240000 |
| fresh:291 | 291 | 94291 | 1.000000 | 0.955000 | 0.955000 | 0.955000 | 0.955000 | 0.735000 | 0.735000 | 0.220000 | 0.220000 |
| fresh:293 | 293 | 94293 | 1.000000 | 0.982500 | 0.982500 | 0.982500 | 0.982500 | 0.820000 | 0.820000 | 0.162500 | 0.162500 |
| fresh:294 | 294 | 94294 | 1.000000 | 0.965000 | 0.965000 | 0.965000 | 0.965000 | 0.780000 | 0.780000 | 0.185000 | 0.185000 |
| fresh:296 | 296 | 94296 | 1.000000 | 0.943750 | 0.943750 | 0.943750 | 0.943750 | 0.705000 | 0.705000 | 0.238750 | 0.238750 |
| fresh:298 | 298 | 94298 | 1.000000 | 0.972500 | 0.972500 | 0.972500 | 0.972500 | 0.745000 | 0.745000 | 0.227500 | 0.227500 |
| fresh:299 | 299 | 94299 | 1.000000 | 0.965000 | 0.965000 | 0.965000 | 0.965000 | 0.717500 | 0.717500 | 0.247500 | 0.247500 |

## Passes at lambda = 100 (separate)

| key | j | seed | lambda_c | ceiling_block | ceiling_block_tau | ceil_1 | ceil_1_tau | n1_block | n1_block_tau | gap | gap_tau |
|---|---|---|---|---|---|---|---|---|---|---|---|
| fresh:26 | 26 | 94026 | 100.000000 | 0.977500 | 0.977500 | 1.000000 | 1.000000 | 0.980000 | 0.980000 | -0.002500 | -0.002500 |
| fresh:31 | 31 | 94031 | 100.000000 | 0.925000 | 0.925000 | 0.980000 | 0.980000 | 0.927500 | 0.927500 | -0.002500 | -0.002500 |
| fresh:68 | 68 | 94068 | 100.000000 | 0.955000 | 0.955000 | 0.990000 | 0.990000 | 0.955000 | 0.955000 | 0.000000 | 0.000000 |
| fresh:76 | 76 | 94076 | 100.000000 | 0.900000 | 0.900000 | 0.967500 | 0.967500 | 0.900000 | 0.900000 | 0.000000 | 0.000000 |
| fresh:95 | 95 | 94095 | 100.000000 | 0.910000 | 0.910000 | 1.000000 | 1.000000 | 0.916250 | 0.916250 | -0.006250 | -0.006250 |
| fresh:97 | 97 | 94097 | 100.000000 | 0.900000 | 0.900000 | 0.992500 | 0.992500 | 0.900000 | 0.900000 | 0.000000 | 0.000000 |
| fresh:129 | 129 | 94129 | 100.000000 | 0.925000 | 0.925000 | 1.000000 | 1.000000 | 0.920000 | 0.920000 | 0.005000 | 0.005000 |
| fresh:145 | 145 | 94145 | 100.000000 | 0.901250 | 0.901250 | 0.960000 | 0.960000 | 0.910000 | 0.910000 | -0.008750 | -0.008750 |
| fresh:161 | 161 | 94161 | 100.000000 | 0.901250 | 0.901250 | 0.987500 | 0.987500 | 0.892500 | 0.892500 | 0.008750 | 0.008750 |
| fresh:192 | 192 | 94192 | 100.000000 | 0.903750 | 0.903750 | 0.971250 | 0.971250 | 0.905000 | 0.905000 | -0.001250 | -0.001250 |
| fresh:205 | 205 | 94205 | 100.000000 | 0.933750 | 0.933750 | 1.000000 | 1.000000 | 0.930000 | 0.930000 | 0.003750 | 0.003750 |
| fresh:226 | 226 | 94226 | 100.000000 | 0.918750 | 0.918750 | 0.992500 | 0.992500 | 0.915000 | 0.915000 | 0.003750 | 0.003750 |
| fresh:235 | 235 | 94235 | 100.000000 | 0.912500 | 0.912500 | 0.975000 | 0.975000 | 0.920000 | 0.920000 | -0.007500 | -0.007500 |
| fresh:261 | 261 | 94261 | 100.000000 | 0.926250 | 0.926250 | 0.992500 | 0.992500 | 0.915000 | 0.915000 | 0.011250 | 0.011250 |
| fresh:268 | 268 | 94268 | 100.000000 | 0.922500 | 0.922500 | 0.986250 | 0.986250 | 0.916250 | 0.916250 | 0.006250 | 0.006250 |
