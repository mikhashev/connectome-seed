# Flyvis night report

### Run A: `C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/night/night1_9991-000.json`
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

### Run B: `C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/night/night4_9991-005.json`
- id: `9991/005`
- seed: 5
- exit: `ok`
- final_iteration: 250008
- started_utc: 2026-09-17T00:28:16Z
- finished_utc: 2026-09-17T04:29:27Z
- total_train_wall_s: 14460.3758  (h:mm:ss = 4:01:00.3758)
- h_run (computed, total_train_wall_s/3600): 4.0168
- VRAM torch_max_memory_allocated_MiB: 1426.0952
- n checkpoints so far: 72
- errors: 0

## Two-phase price (activity_penalty.stop_iter = 150000)

| run | median s/iter [1,000-150,000] | median s/iter [150,001-end] | overall median s/iter | wall sum <=150,000 (s) | wall sum >150,000 (s) | iterations seen |
|---|---|---|---|---|---|---|
| A | 0.0644 | 0.0452 | 0.0614 | 9754.0554 | 4581.2000 | 250008 |
| B | 0.0640 | 0.0457 | 0.0609 | 9713.3306 | 4666.0059 | 250008 |

(Note: precomputed `iter_wall_median_all_s` / `iter_wall_median_1000_2000_s` in the json, when present, cover different windows than this table; this table's medians/sums are computed here from `iter_wall_s` over the windows stated in the header.)
- A json field iter_wall_median_all_s: 0.0614
- A json field iter_wall_median_1000_2000_s: 0.0647
- B json field iter_wall_median_all_s: 0.0609
- B json field iter_wall_median_1000_2000_s: 0.0643

## Rung table

| iteration | val_loss A | val_loss B | B - A | relative (B-A)/A |
|---|---|---|---|---|
| 1000 | 1208.9363 | 1207.3300 | -1.6063 | -0.0013 |
| 5000 | 1207.7673 | 1208.2387 | 0.4714 | 0.0004 |
| 25000 | 1191.7375 | 1204.7794 | 13.0420 | 0.0109 |
| 250000 | 1146.1958 | 1159.1158 | 12.9200 | 0.0113 |

## Replicate difference at iteration 250,000 (pre-registration section 7 tolerance: < 1%)

- |A-B|/A at 250,000 = 1.1272%  -> FAIL (>= 1%)

## Checkpoint trajectory

Compact view (every 5th checkpoint by A's index; full 72-row list -> `results/night4/night_report_checkpoints_5v0.csv`):

| iteration | val_loss A | val_loss B |
|---|---|---|
| 0 | 1212.5556 | 1212.5467 |
| 12 | 1212.2575 | 1212.0451 |
| 3612 | 1206.3210 | 1205.1753 |
| 7212 | 1206.1248 | 1206.8535 |
| 10812 | 1205.7025 | 1206.6615 |
| 14412 | 1206.0824 | 1206.3603 |
| 18012 | 1205.9267 | 1206.2544 |
| 21612 | 1199.3854 | 1206.6749 |
| 25212 | 1192.7493 | 1213.5255 |
| 28812 | 1184.2532 | 1200.9585 |
| 32412 | 1175.8663 | 1193.8305 |
| 36012 | 1170.1614 | 1189.6421 |
| 39612 | 1170.5515 | 1181.0526 |
| 43212 | 1170.5394 | 1179.9459 |
| 46812 | 1163.0753 | 1176.7960 |
| 50412 | 1166.7279 | 1169.9621 |
| 54012 | 1165.3890 | 1159.0972 |
| 57612 | 1163.9735 | 1173.8967 |
| 61212 | 1157.2235 | 1197.2148 |
| 64812 | 1163.9785 | 1168.9665 |
| 68412 | 1168.6454 | 1164.7707 |
| 72012 | 1156.2146 | 1165.1124 |
| 75612 | 1153.7558 | 1154.7896 |
| 79212 | 1155.2570 | 1166.8570 |
| 82812 | 1143.5370 | 1166.6891 |
| 86412 | 1155.3520 | 1188.8464 |
| 90012 | 1150.2037 | 1306.4735 |
| 93612 | 1146.0899 | 1188.1393 |
| 97212 | 1166.0588 | 1180.2319 |
| 100812 | 1159.3972 | 1195.9462 |
| 104412 | 1149.9424 | 1193.9646 |
| 108012 | 1152.2472 | 1191.7150 |
| 111612 | 1145.2592 | 1182.2868 |
| 115212 | 1162.6179 | 1172.0938 |
| 118812 | 1159.1506 | 1209.2466 |
| 122412 | 1149.5846 | 1261.6149 |
| 126012 | 1157.3147 | 1303.0241 |
| 129612 | 1155.5432 | 1200.9613 |
| 133212 | 1153.2944 | 1170.9588 |
| 136812 | 1155.7976 | 1194.0654 |
| 140412 | 1170.6714 | 1181.5870 |
| 144012 | 1154.2528 | 1176.1111 |
| 147612 | 1150.4220 | 1169.2778 |
| 151212 | 1152.8307 | 1168.6911 |
| 154812 | 1159.6491 | 1162.8660 |
| 158412 | 1148.1151 | 1163.1878 |
| 162012 | 1159.5074 | 1160.8299 |
| 165612 | 1168.3797 | 1170.0790 |
| 169212 | 1149.1648 | 1160.8200 |
| 172812 | 1154.8277 | 1161.7554 |
| 176412 | 1147.5207 | 1167.2268 |
| 180012 | 1148.9453 | 1165.2338 |
| 183612 | 1146.5118 | 1161.8835 |
| 187212 | 1150.2214 | 1157.8814 |
| 190812 | 1167.6187 | 1159.0685 |
| 194412 | 1153.1420 | 1152.4383 |
| 198012 | 1149.6872 | 1152.0758 |
| 201612 | 1147.5358 | 1158.4730 |
| 205212 | 1148.8634 | 1158.7704 |
| 208812 | 1149.8740 | 1155.2645 |
| 212412 | 1156.6829 | 1154.8303 |
| 216012 | 1152.8448 | 1150.5741 |
| 219612 | 1141.0463 | 1158.3133 |
| 223212 | 1153.7354 | 1143.1055 |
| 226812 | 1150.9120 | 1149.8725 |
| 230412 | 1148.4920 | 1152.9744 |
| 234012 | 1145.9390 | 1147.6558 |
| 237612 | 1146.7684 | 1152.5891 |
| 241212 | 1150.2581 | 1149.3406 |
| 244812 | 1147.7892 | 1152.6918 |
| 248412 | 1153.3329 | 1151.1478 |
| 250008 | 1148.8075 | 1156.3866 |

(full checkpoint list written to `results/night4/night_report_checkpoints_5v0.csv`, 72 rows)

### Run A checkpoint detail

- iteration of minimum held-out (checkpoint) val_loss: 219612 (val_loss=1141.0463)
- loss near iteration 25000: 1192.7493 (nearest checkpoint at iteration 25212)
- loss near iteration 50000: 1166.7279 (nearest checkpoint at iteration 50412)
- loss near iteration 100000: 1159.3972 (nearest checkpoint at iteration 100812)
- loss near iteration 150000: 1152.8307 (nearest checkpoint at iteration 151212)
- loss near iteration 200000: 1147.5358 (nearest checkpoint at iteration 201612)
- loss near iteration 250000: 1148.8075 (nearest checkpoint at iteration 250008)
- relative change of held-out loss over the last 50,000 iterations (checkpoint near 200000 -> checkpoint near 250000, positive = rose): 0.0011 (1147.5358 -> 1148.8075; plateauing by a <1% heuristic)
- discrepancy: rung val_loss at iteration 250,000 (1146.1958) vs checkpoint val_loss at iteration 250008 (1148.8075) = 2.6117 over 8 extra iteration(s)
- training-loss (train_loss_per_iter) std over last 100 iterations: 679.6031 (mean 1283.4386) -- for judging whether the discrepancy above is within iteration-to-iteration noise

### Run B checkpoint detail

- iteration of minimum held-out (checkpoint) val_loss so far: 223212 (val_loss=1143.1055)
- training-loss std over last 100 iterations: 663.4988

## Per-rung / per-checkpoint replicate differences (section 7 instrument-floor input)

Rungs:
- iteration 1000: |A-B| = 1.6063
- iteration 5000: |A-B| = 0.4714
- iteration 25000: |A-B| = 13.0420
- iteration 250000: |A-B| = 12.9200

Common checkpoints (72):
- iteration 0: |A-B| = 0.0089
- iteration 12: |A-B| = 0.2124
- iteration 3612: |A-B| = 1.1457
- iteration 7212: |A-B| = 0.7287
- iteration 10812: |A-B| = 0.9590
- iteration 14412: |A-B| = 0.2779
- iteration 18012: |A-B| = 0.3277
- iteration 21612: |A-B| = 7.2895
- iteration 25212: |A-B| = 20.7762
- iteration 28812: |A-B| = 16.7053
- iteration 32412: |A-B| = 17.9642
- iteration 36012: |A-B| = 19.4808
- iteration 39612: |A-B| = 10.5011
- iteration 43212: |A-B| = 9.4065
- iteration 46812: |A-B| = 13.7207
- iteration 50412: |A-B| = 3.2342
- iteration 54012: |A-B| = 6.2917
- iteration 57612: |A-B| = 9.9232
- iteration 61212: |A-B| = 39.9912
- iteration 64812: |A-B| = 4.9880
- iteration 68412: |A-B| = 3.8748
- iteration 72012: |A-B| = 8.8978
- iteration 75612: |A-B| = 1.0339
- iteration 79212: |A-B| = 11.6000
- iteration 82812: |A-B| = 23.1521
- iteration 86412: |A-B| = 33.4944
- iteration 90012: |A-B| = 156.2698
- iteration 93612: |A-B| = 42.0494
- iteration 97212: |A-B| = 14.1731
- iteration 100812: |A-B| = 36.5489
- iteration 104412: |A-B| = 44.0222
- iteration 108012: |A-B| = 39.4679
- iteration 111612: |A-B| = 37.0276
- iteration 115212: |A-B| = 9.4759
- iteration 118812: |A-B| = 50.0961
- iteration 122412: |A-B| = 112.0302
- iteration 126012: |A-B| = 145.7094
- iteration 129612: |A-B| = 45.4182
- iteration 133212: |A-B| = 17.6644
- iteration 136812: |A-B| = 38.2678
- iteration 140412: |A-B| = 10.9156
- iteration 144012: |A-B| = 21.8583
- iteration 147612: |A-B| = 18.8558
- iteration 151212: |A-B| = 15.8604
- iteration 154812: |A-B| = 3.2169
- iteration 158412: |A-B| = 15.0728
- iteration 162012: |A-B| = 1.3226
- iteration 165612: |A-B| = 1.6993
- iteration 169212: |A-B| = 11.6553
- iteration 172812: |A-B| = 6.9278
- iteration 176412: |A-B| = 19.7061
- iteration 180012: |A-B| = 16.2885
- iteration 183612: |A-B| = 15.3717
- iteration 187212: |A-B| = 7.6601
- iteration 190812: |A-B| = 8.5502
- iteration 194412: |A-B| = 0.7037
- iteration 198012: |A-B| = 2.3886
- iteration 201612: |A-B| = 10.9372
- iteration 205212: |A-B| = 9.9070
- iteration 208812: |A-B| = 5.3905
- iteration 212412: |A-B| = 1.8526
- iteration 216012: |A-B| = 2.2707
- iteration 219612: |A-B| = 17.2670
- iteration 223212: |A-B| = 10.6298
- iteration 226812: |A-B| = 1.0395
- iteration 230412: |A-B| = 4.4825
- iteration 234012: |A-B| = 1.7168
- iteration 237612: |A-B| = 5.8208
- iteration 241212: |A-B| = 0.9175
- iteration 244812: |A-B| = 4.9026
- iteration 248412: |A-B| = 2.1852
- iteration 250008: |A-B| = 7.5791

- max |A-B| across rungs+common checkpoints: 156.2698
- median |A-B| across rungs+common checkpoints: 9.9151

