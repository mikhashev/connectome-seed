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

### Run B: `C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/night/night3_9991-003.json`
- id: `9991/003`
- seed: 3
- exit: `ok`
- final_iteration: 250008
- started_utc: 2026-09-15T20:35:26Z
- finished_utc: 2026-09-16T00:35:37Z
- total_train_wall_s: 14399.5953  (h:mm:ss = 3:59:59.5953)
- h_run (computed, total_train_wall_s/3600): 3.9999
- VRAM torch_max_memory_allocated_MiB: 1426.0952
- n checkpoints so far: 72
- errors: 0

## Two-phase price (activity_penalty.stop_iter = 150000)

| run | median s/iter [1,000-150,000] | median s/iter [150,001-end] | overall median s/iter | wall sum <=150,000 (s) | wall sum >150,000 (s) | iterations seen |
|---|---|---|---|---|---|---|
| A | 0.0644 | 0.0452 | 0.0614 | 9754.0554 | 4581.2000 | 250008 |
| B | 0.0642 | 0.0447 | 0.0612 | 9723.2724 | 4596.6236 | 250008 |

(Note: precomputed `iter_wall_median_all_s` / `iter_wall_median_1000_2000_s` in the json, when present, cover different windows than this table; this table's medians/sums are computed here from `iter_wall_s` over the windows stated in the header.)
- A json field iter_wall_median_all_s: 0.0614
- A json field iter_wall_median_1000_2000_s: 0.0647
- B json field iter_wall_median_all_s: 0.0612
- B json field iter_wall_median_1000_2000_s: 0.0660

## Rung table

| iteration | val_loss A | val_loss B | B - A | relative (B-A)/A |
|---|---|---|---|---|
| 1000 | 1208.9363 | 1210.4139 | 1.4776 | 0.0012 |
| 5000 | 1207.7673 | 1205.5457 | -2.2216 | -0.0018 |
| 25000 | 1191.7375 | 1192.5858 | 0.8484 | 0.0007 |
| 250000 | 1146.1958 | 1152.5066 | 6.3107 | 0.0055 |

## Replicate difference at iteration 250,000 (pre-registration section 7 tolerance: < 1%)

- |A-B|/A at 250,000 = 0.5506%  -> PASS (< 1%)

## Checkpoint trajectory

Compact view (every 5th checkpoint by A's index; full 72-row list -> `results/night3/night_report_checkpoints_3v0.csv`):

| iteration | val_loss A | val_loss B |
|---|---|---|
| 0 | 1212.5556 | 1212.5497 |
| 12 | 1212.2575 | 1211.7933 |
| 3612 | 1206.3210 | 1206.8331 |
| 7212 | 1206.1248 | 1207.4437 |
| 10812 | 1205.7025 | 1206.1021 |
| 14412 | 1206.0824 | 1206.2946 |
| 18012 | 1205.9267 | 1204.1880 |
| 21612 | 1199.3854 | 1201.7573 |
| 25212 | 1192.7493 | 1190.0517 |
| 28812 | 1184.2532 | 1184.5230 |
| 32412 | 1175.8663 | 1174.2851 |
| 36012 | 1170.1614 | 1179.1252 |
| 39612 | 1170.5515 | 1174.0103 |
| 43212 | 1170.5394 | 1179.8168 |
| 46812 | 1163.0753 | 1168.8909 |
| 50412 | 1166.7279 | 1179.0335 |
| 54012 | 1165.3890 | 1171.3346 |
| 57612 | 1163.9735 | 1164.6277 |
| 61212 | 1157.2235 | 1174.0634 |
| 64812 | 1163.9785 | 1165.9828 |
| 68412 | 1168.6454 | 1174.3908 |
| 72012 | 1156.2146 | 1178.1888 |
| 75612 | 1153.7558 | 1166.0802 |
| 79212 | 1155.2570 | 1174.6413 |
| 82812 | 1143.5370 | 1164.9092 |
| 86412 | 1155.3520 | 1169.4652 |
| 90012 | 1150.2037 | 1171.1677 |
| 93612 | 1146.0899 | 1175.2162 |
| 97212 | 1166.0588 | 1173.9763 |
| 100812 | 1159.3972 | 1168.6564 |
| 104412 | 1149.9424 | 1172.8285 |
| 108012 | 1152.2472 | 1163.5787 |
| 111612 | 1145.2592 | 1161.7089 |
| 115212 | 1162.6179 | 1170.3667 |
| 118812 | 1159.1506 | 1174.6678 |
| 122412 | 1149.5846 | 1170.5868 |
| 126012 | 1157.3147 | 1167.1255 |
| 129612 | 1155.5432 | 1167.4171 |
| 133212 | 1153.2944 | 1168.2857 |
| 136812 | 1155.7976 | 1176.3770 |
| 140412 | 1170.6714 | 1163.0901 |
| 144012 | 1154.2528 | 1163.1483 |
| 147612 | 1150.4220 | 1161.3737 |
| 151212 | 1152.8307 | 1165.2208 |
| 154812 | 1159.6491 | 1165.6917 |
| 158412 | 1148.1151 | 1167.5395 |
| 162012 | 1159.5074 | 1181.6246 |
| 165612 | 1168.3797 | 1166.1481 |
| 169212 | 1149.1648 | 1171.6817 |
| 172812 | 1154.8277 | 1166.0327 |
| 176412 | 1147.5207 | 1158.8479 |
| 180012 | 1148.9453 | 1166.3808 |
| 183612 | 1146.5118 | 1169.6822 |
| 187212 | 1150.2214 | 1161.4556 |
| 190812 | 1167.6187 | 1162.5909 |
| 194412 | 1153.1420 | 1161.2928 |
| 198012 | 1149.6872 | 1152.6912 |
| 201612 | 1147.5358 | 1163.2382 |
| 205212 | 1148.8634 | 1162.3037 |
| 208812 | 1149.8740 | 1158.1978 |
| 212412 | 1156.6829 | 1160.7131 |
| 216012 | 1152.8448 | 1153.3346 |
| 219612 | 1141.0463 | 1157.4240 |
| 223212 | 1153.7354 | 1152.8706 |
| 226812 | 1150.9120 | 1155.5818 |
| 230412 | 1148.4920 | 1155.2349 |
| 234012 | 1145.9390 | 1156.2054 |
| 237612 | 1146.7684 | 1150.9345 |
| 241212 | 1150.2581 | 1153.4507 |
| 244812 | 1147.7892 | 1152.9011 |
| 248412 | 1153.3329 | 1153.6783 |
| 250008 | 1148.8075 | 1155.7706 |

(full checkpoint list written to `results/night3/night_report_checkpoints_3v0.csv`, 72 rows)

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

- iteration of minimum held-out (checkpoint) val_loss so far: 237612 (val_loss=1150.9345)
- training-loss std over last 100 iterations: 613.6562

## Per-rung / per-checkpoint replicate differences (section 7 instrument-floor input)

Rungs:
- iteration 1000: |A-B| = 1.4776
- iteration 5000: |A-B| = 2.2216
- iteration 25000: |A-B| = 0.8484
- iteration 250000: |A-B| = 6.3107

Common checkpoints (72):
- iteration 0: |A-B| = 0.0059
- iteration 12: |A-B| = 0.4642
- iteration 3612: |A-B| = 0.5122
- iteration 7212: |A-B| = 1.3189
- iteration 10812: |A-B| = 0.3996
- iteration 14412: |A-B| = 0.2122
- iteration 18012: |A-B| = 1.7387
- iteration 21612: |A-B| = 2.3719
- iteration 25212: |A-B| = 2.6977
- iteration 28812: |A-B| = 0.2698
- iteration 32412: |A-B| = 1.5812
- iteration 36012: |A-B| = 8.9638
- iteration 39612: |A-B| = 3.4588
- iteration 43212: |A-B| = 9.2775
- iteration 46812: |A-B| = 5.8156
- iteration 50412: |A-B| = 12.3056
- iteration 54012: |A-B| = 5.9456
- iteration 57612: |A-B| = 0.6542
- iteration 61212: |A-B| = 16.8399
- iteration 64812: |A-B| = 2.0043
- iteration 68412: |A-B| = 5.7453
- iteration 72012: |A-B| = 21.9742
- iteration 75612: |A-B| = 12.3244
- iteration 79212: |A-B| = 19.3843
- iteration 82812: |A-B| = 21.3722
- iteration 86412: |A-B| = 14.1132
- iteration 90012: |A-B| = 20.9640
- iteration 93612: |A-B| = 29.1263
- iteration 97212: |A-B| = 7.9175
- iteration 100812: |A-B| = 9.2591
- iteration 104412: |A-B| = 22.8861
- iteration 108012: |A-B| = 11.3316
- iteration 111612: |A-B| = 16.4497
- iteration 115212: |A-B| = 7.7488
- iteration 118812: |A-B| = 15.5173
- iteration 122412: |A-B| = 21.0021
- iteration 126012: |A-B| = 9.8108
- iteration 129612: |A-B| = 11.8739
- iteration 133212: |A-B| = 14.9913
- iteration 136812: |A-B| = 20.5794
- iteration 140412: |A-B| = 7.5813
- iteration 144012: |A-B| = 8.8955
- iteration 147612: |A-B| = 10.9517
- iteration 151212: |A-B| = 12.3901
- iteration 154812: |A-B| = 6.0426
- iteration 158412: |A-B| = 19.4244
- iteration 162012: |A-B| = 22.1173
- iteration 165612: |A-B| = 2.2316
- iteration 169212: |A-B| = 22.5170
- iteration 172812: |A-B| = 11.2050
- iteration 176412: |A-B| = 11.3273
- iteration 180012: |A-B| = 17.4356
- iteration 183612: |A-B| = 23.1705
- iteration 187212: |A-B| = 11.2342
- iteration 190812: |A-B| = 5.0278
- iteration 194412: |A-B| = 8.1507
- iteration 198012: |A-B| = 3.0039
- iteration 201612: |A-B| = 15.7024
- iteration 205212: |A-B| = 13.4402
- iteration 208812: |A-B| = 8.3238
- iteration 212412: |A-B| = 4.0302
- iteration 216012: |A-B| = 0.4899
- iteration 219612: |A-B| = 16.3777
- iteration 223212: |A-B| = 0.8648
- iteration 226812: |A-B| = 4.6698
- iteration 230412: |A-B| = 6.7429
- iteration 234012: |A-B| = 10.2664
- iteration 237612: |A-B| = 4.1661
- iteration 241212: |A-B| = 3.1925
- iteration 244812: |A-B| = 5.1118
- iteration 248412: |A-B| = 0.3453
- iteration 250008: |A-B| = 6.9632

- max |A-B| across rungs+common checkpoints: 29.1263
- median |A-B| across rungs+common checkpoints: 8.0341

