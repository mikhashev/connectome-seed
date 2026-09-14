# Flyvis night report

### Run A: `night/night1_9991-000.json`
- id: `9991/000`
- seed: 0
- exit: `ok`
- final_iteration: 250008
- started_utc: 2026-09-13T18:40:31Z
- finished_utc: 2026-09-13T22:40:56Z
- total_train_wall_s: 14417.6889  (h:mm:ss = 4:00:17.6889)
- h_run (computed, total_train_wall_s/3600): 4.0049
- VRAM torch_max_memory_allocated_MiB: 1426.0952
- n checkpoints so far: 72
- errors: 0

### Run B: `night/rep_9991-900.json`
- id: `9991/900`
- seed: 0
- exit: `ok`
- final_iteration: 250008
- started_utc: 2026-09-13T22:40:59Z
- finished_utc: 2026-09-14T02:39:51Z
- total_train_wall_s: 14319.9398  (h:mm:ss = 3:58:39.9398)
- h_run (computed, total_train_wall_s/3600): 3.9778
- VRAM torch_max_memory_allocated_MiB: 1426.0952
- n checkpoints so far: 72
- errors: 0

## Two-phase price (activity_penalty.stop_iter = 150000)

| run | median s/iter [1,000-150,000] | median s/iter [150,001-end] | overall median s/iter | wall sum <=150,000 (s) | wall sum >150,000 (s) | iterations seen |
|---|---|---|---|---|---|---|
| A | 0.0644 | 0.0452 | 0.0614 | 9754.0554 | 4581.2000 | 250008 |
| B | 0.0639 | 0.0451 | 0.0609 | 9665.5155 | 4574.0469 | 250008 |

(Note: precomputed `iter_wall_median_all_s` / `iter_wall_median_1000_2000_s` in the json, when present, cover different windows than this table; this table's medians/sums are computed here from `iter_wall_s` over the windows stated in the header.)
- A json field iter_wall_median_all_s: 0.0614
- A json field iter_wall_median_1000_2000_s: 0.0647
- B json field iter_wall_median_all_s: 0.0609
- B json field iter_wall_median_1000_2000_s: 0.0641

## Rung table

| iteration | val_loss A | val_loss B | B - A | relative (B-A)/A |
|---|---|---|---|---|
| 1000 | 1208.9363 | 1208.9363 | 0.0000 | 0.0000 |
| 5000 | 1207.7673 | 1207.7698 | 0.0025 | 0.0000 |
| 25000 | 1191.7375 | 1192.0739 | 0.3365 | 0.0003 |
| 250000 | 1146.1958 | 1158.9237 | 12.7279 | 0.0111 |

## Replicate difference at iteration 250,000 (pre-registration section 7 tolerance: < 1%)

- |A-B|/A at 250,000 = 1.1104%  -> FAIL (>= 1%)

## Checkpoint trajectory

Compact view (every 5th checkpoint by A's index; full 72-row list -> `C:\Users\mikha\AppData\Local\Temp\claude\c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx\63f3961a-96ce-4048-8338-72c162ea66f8\scratchpad\flyvis-probe\night_report_checkpoints.csv`):

| iteration | val_loss A | val_loss B |
|---|---|---|
| 0 | 1212.5556 | 1212.5556 |
| 12 | 1212.2575 | 1212.2574 |
| 3612 | 1206.3210 | 1206.3057 |
| 7212 | 1206.1248 | 1206.1166 |
| 10812 | 1205.7025 | 1205.6864 |
| 14412 | 1206.0824 | 1206.0104 |
| 18012 | 1205.9267 | 1205.8643 |
| 21612 | 1199.3854 | 1200.0605 |
| 25212 | 1192.7493 | 1192.8249 |
| 28812 | 1184.2532 | 1183.6375 |
| 32412 | 1175.8663 | 1178.3090 |
| 36012 | 1170.1614 | 1170.5986 |
| 39612 | 1170.5515 | 1172.1209 |
| 43212 | 1170.5394 | 1171.6974 |
| 46812 | 1163.0753 | 1165.0034 |
| 50412 | 1166.7279 | 1165.7000 |
| 54012 | 1165.3890 | 1168.5220 |
| 57612 | 1163.9735 | 1165.8661 |
| 61212 | 1157.2235 | 1163.6425 |
| 64812 | 1163.9785 | 1165.2621 |
| 68412 | 1168.6454 | 1175.2381 |
| 72012 | 1156.2146 | 1165.7804 |
| 75612 | 1153.7558 | 1158.3737 |
| 79212 | 1155.2570 | 1161.6555 |
| 82812 | 1143.5370 | 1156.0002 |
| 86412 | 1155.3520 | 1161.0802 |
| 90012 | 1150.2037 | 1162.7695 |
| 93612 | 1146.0899 | 1158.1070 |
| 97212 | 1166.0588 | 1165.5258 |
| 100812 | 1159.3972 | 1165.9084 |
| 104412 | 1149.9424 | 1165.0306 |
| 108012 | 1152.2472 | 1165.1910 |
| 111612 | 1145.2592 | 1158.2587 |
| 115212 | 1162.6179 | 1167.6306 |
| 118812 | 1159.1506 | 1160.2479 |
| 122412 | 1149.5846 | 1157.1583 |
| 126012 | 1157.3147 | 1163.2417 |
| 129612 | 1155.5432 | 1160.7915 |
| 133212 | 1153.2944 | 1164.9485 |
| 136812 | 1155.7976 | 1165.1465 |
| 140412 | 1170.6714 | 1167.6292 |
| 144012 | 1154.2528 | 1166.6949 |
| 147612 | 1150.4220 | 1160.9485 |
| 151212 | 1152.8307 | 1165.0776 |
| 154812 | 1159.6491 | 1164.1412 |
| 158412 | 1148.1151 | 1160.1366 |
| 162012 | 1159.5074 | 1170.9093 |
| 165612 | 1168.3797 | 1172.0600 |
| 169212 | 1149.1648 | 1160.9524 |
| 172812 | 1154.8277 | 1165.7929 |
| 176412 | 1147.5207 | 1164.6906 |
| 180012 | 1148.9453 | 1161.0158 |
| 183612 | 1146.5118 | 1163.1875 |
| 187212 | 1150.2214 | 1167.1313 |
| 190812 | 1167.6187 | 1172.5036 |
| 194412 | 1153.1420 | 1163.9779 |
| 198012 | 1149.6872 | 1163.5246 |
| 201612 | 1147.5358 | 1162.2340 |
| 205212 | 1148.8634 | 1163.2771 |
| 208812 | 1149.8740 | 1163.9772 |
| 212412 | 1156.6829 | 1168.5996 |
| 216012 | 1152.8448 | 1164.6138 |
| 219612 | 1141.0463 | 1158.8616 |
| 223212 | 1153.7354 | 1165.0799 |
| 226812 | 1150.9120 | 1163.2940 |
| 230412 | 1148.4920 | 1161.3785 |
| 234012 | 1145.9390 | 1162.5076 |
| 237612 | 1146.7684 | 1163.5597 |
| 241212 | 1150.2581 | 1163.7693 |
| 244812 | 1147.7892 | 1163.0918 |
| 248412 | 1153.3329 | 1165.2531 |
| 250008 | 1148.8075 | 1160.9823 |

(full checkpoint list written to `C:\Users\mikha\AppData\Local\Temp\claude\c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx\63f3961a-96ce-4048-8338-72c162ea66f8\scratchpad\flyvis-probe\night_report_checkpoints.csv`, 72 rows)

### Run A checkpoint detail

- iteration of minimum held-out (checkpoint) val_loss: 219612 (val_loss=1141.0463)
- loss near iteration 25000: 1192.7493 (nearest checkpoint at iteration 25212)
- loss near iteration 50000: 1166.7279 (nearest checkpoint at iteration 50412)
- loss near iteration 100000: 1159.3972 (nearest checkpoint at iteration 100812)
- loss near iteration 150000: 1152.8307 (nearest checkpoint at iteration 151212)
- loss near iteration 200000: 1147.5358 (nearest checkpoint at iteration 201612)
- loss near iteration 250000: 1148.8075 (nearest checkpoint at iteration 250008)
- relative drop over last 50,000 iterations (checkpoint near 200000 -> checkpoint near 250000): -0.0011 (1147.5358 -> 1148.8075; plateauing by a <1% heuristic)
- discrepancy: rung val_loss at iteration 250,000 (1146.1958) vs checkpoint val_loss at iteration 250008 (1148.8075) = 2.6117 over 8 extra iteration(s)
- training-loss (train_loss_per_iter) std over last 100 iterations: 679.6031 (mean 1283.4386) -- for judging whether the discrepancy above is within iteration-to-iteration noise

### Run B checkpoint detail

- iteration of minimum held-out (checkpoint) val_loss so far: 82812 (val_loss=1156.0002)
- training-loss std over last 100 iterations: 677.9452

## Per-rung / per-checkpoint replicate differences (section 7 instrument-floor input)

Rungs:
- iteration 1000: |A-B| = 0.0000
- iteration 5000: |A-B| = 0.0025
- iteration 25000: |A-B| = 0.3365
- iteration 250000: |A-B| = 12.7279

Common checkpoints (72):
- iteration 0: |A-B| = 0.0000
- iteration 12: |A-B| = 0.0001
- iteration 3612: |A-B| = 0.0153
- iteration 7212: |A-B| = 0.0083
- iteration 10812: |A-B| = 0.0162
- iteration 14412: |A-B| = 0.0719
- iteration 18012: |A-B| = 0.0623
- iteration 21612: |A-B| = 0.6751
- iteration 25212: |A-B| = 0.0756
- iteration 28812: |A-B| = 0.6156
- iteration 32412: |A-B| = 2.4427
- iteration 36012: |A-B| = 0.4373
- iteration 39612: |A-B| = 1.5695
- iteration 43212: |A-B| = 1.1580
- iteration 46812: |A-B| = 1.9281
- iteration 50412: |A-B| = 1.0279
- iteration 54012: |A-B| = 3.1330
- iteration 57612: |A-B| = 1.8927
- iteration 61212: |A-B| = 6.4189
- iteration 64812: |A-B| = 1.2836
- iteration 68412: |A-B| = 6.5927
- iteration 72012: |A-B| = 9.5659
- iteration 75612: |A-B| = 4.6179
- iteration 79212: |A-B| = 6.3985
- iteration 82812: |A-B| = 12.4631
- iteration 86412: |A-B| = 5.7282
- iteration 90012: |A-B| = 12.5658
- iteration 93612: |A-B| = 12.0171
- iteration 97212: |A-B| = 0.5329
- iteration 100812: |A-B| = 6.5111
- iteration 104412: |A-B| = 15.0882
- iteration 108012: |A-B| = 12.9438
- iteration 111612: |A-B| = 12.9995
- iteration 115212: |A-B| = 5.0127
- iteration 118812: |A-B| = 1.0974
- iteration 122412: |A-B| = 7.5737
- iteration 126012: |A-B| = 5.9270
- iteration 129612: |A-B| = 5.2483
- iteration 133212: |A-B| = 11.6541
- iteration 136812: |A-B| = 9.3489
- iteration 140412: |A-B| = 3.0422
- iteration 144012: |A-B| = 12.4421
- iteration 147612: |A-B| = 10.5264
- iteration 151212: |A-B| = 12.2470
- iteration 154812: |A-B| = 4.4922
- iteration 158412: |A-B| = 12.0215
- iteration 162012: |A-B| = 11.4019
- iteration 165612: |A-B| = 3.6803
- iteration 169212: |A-B| = 11.7876
- iteration 172812: |A-B| = 10.9653
- iteration 176412: |A-B| = 17.1699
- iteration 180012: |A-B| = 12.0705
- iteration 183612: |A-B| = 16.6757
- iteration 187212: |A-B| = 16.9099
- iteration 190812: |A-B| = 4.8849
- iteration 194412: |A-B| = 10.8359
- iteration 198012: |A-B| = 13.8373
- iteration 201612: |A-B| = 14.6982
- iteration 205212: |A-B| = 14.4137
- iteration 208812: |A-B| = 14.1033
- iteration 212412: |A-B| = 11.9167
- iteration 216012: |A-B| = 11.7691
- iteration 219612: |A-B| = 17.8153
- iteration 223212: |A-B| = 11.3446
- iteration 226812: |A-B| = 12.3820
- iteration 230412: |A-B| = 12.8865
- iteration 234012: |A-B| = 16.5687
- iteration 237612: |A-B| = 16.7913
- iteration 241212: |A-B| = 13.5112
- iteration 244812: |A-B| = 15.3026
- iteration 248412: |A-B| = 11.9202
- iteration 250008: |A-B| = 12.1749

- max |A-B| across rungs+common checkpoints: 17.8153
- median |A-B| across rungs+common checkpoints: 8.4613

