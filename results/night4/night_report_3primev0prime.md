# Flyvis night report

### Run A: `C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/night/rep_9991-900.json`
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

### Run B: `C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/night/rep_9991-903.json`
- id: `9991/903`
- seed: 3
- exit: `ok`
- final_iteration: 250008
- started_utc: 2026-09-16T20:27:30Z
- finished_utc: 2026-09-17T00:28:12Z
- total_train_wall_s: 14435.3311  (h:mm:ss = 4:00:35.3311)
- h_run (computed, total_train_wall_s/3600): 4.0098
- VRAM torch_max_memory_allocated_MiB: 1426.0952
- n checkpoints so far: 72
- errors: 0

## Two-phase price (activity_penalty.stop_iter = 150000)

| run | median s/iter [1,000-150,000] | median s/iter [150,001-end] | overall median s/iter | wall sum <=150,000 (s) | wall sum >150,000 (s) | iterations seen |
|---|---|---|---|---|---|---|
| A | 0.0639 | 0.0451 | 0.0609 | 9665.5155 | 4574.0469 | 250008 |
| B | 0.0644 | 0.0454 | 0.0607 | 9747.1319 | 4606.7709 | 250008 |

(Note: precomputed `iter_wall_median_all_s` / `iter_wall_median_1000_2000_s` in the json, when present, cover different windows than this table; this table's medians/sums are computed here from `iter_wall_s` over the windows stated in the header.)
- A json field iter_wall_median_all_s: 0.0609
- A json field iter_wall_median_1000_2000_s: 0.0641
- B json field iter_wall_median_all_s: 0.0607
- B json field iter_wall_median_1000_2000_s: 0.0671

## Rung table

| iteration | val_loss A | val_loss B | B - A | relative (B-A)/A |
|---|---|---|---|---|
| 1000 | 1208.9363 | 1210.4302 | 1.4939 | 0.0012 |
| 5000 | 1207.7698 | 1205.5182 | -2.2517 | -0.0019 |
| 25000 | 1192.0739 | 1187.4011 | -4.6728 | -0.0039 |
| 250000 | 1158.9237 | 1162.9375 | 4.0137 | 0.0035 |

## Replicate difference at iteration 250,000 (pre-registration section 7 tolerance: < 1%)

- |A-B|/A at 250,000 = 0.3463%  -> PASS (< 1%)

## Checkpoint trajectory

Compact view (every 5th checkpoint by A's index; full 72-row list -> `results/night4/night_report_checkpoints_3primev0prime.csv`):

| iteration | val_loss A | val_loss B |
|---|---|---|
| 0 | 1212.5556 | 1212.5497 |
| 12 | 1212.2574 | 1211.7932 |
| 3612 | 1206.3057 | 1206.8111 |
| 7212 | 1206.1166 | 1207.4158 |
| 10812 | 1205.6864 | 1206.1364 |
| 14412 | 1206.0104 | 1206.4309 |
| 18012 | 1205.8643 | 1204.2230 |
| 21612 | 1200.0605 | 1201.7641 |
| 25212 | 1192.8249 | 1187.1360 |
| 28812 | 1183.6375 | 1182.3103 |
| 32412 | 1178.3090 | 1173.1151 |
| 36012 | 1170.5986 | 1180.7562 |
| 39612 | 1172.1209 | 1177.6193 |
| 43212 | 1171.6974 | 1188.7442 |
| 46812 | 1165.0034 | 1177.9724 |
| 50412 | 1165.7000 | 1182.3089 |
| 54012 | 1168.5220 | 1178.8657 |
| 57612 | 1165.8661 | 1170.8438 |
| 61212 | 1163.6425 | 1172.7128 |
| 64812 | 1165.2621 | 1171.4413 |
| 68412 | 1175.2381 | 1173.6945 |
| 72012 | 1165.7804 | 1174.2891 |
| 75612 | 1158.3737 | 1172.0935 |
| 79212 | 1161.6555 | 1186.6132 |
| 82812 | 1156.0002 | 1173.6684 |
| 86412 | 1161.0802 | 1167.4142 |
| 90012 | 1162.7695 | 1174.8151 |
| 93612 | 1158.1070 | 1178.7145 |
| 97212 | 1165.5258 | 1174.9573 |
| 100812 | 1165.9084 | 1174.2219 |
| 104412 | 1165.0306 | 1179.2206 |
| 108012 | 1165.1910 | 1166.1420 |
| 111612 | 1158.2587 | 1169.4737 |
| 115212 | 1167.6306 | 1177.8473 |
| 118812 | 1160.2479 | 1191.0984 |
| 122412 | 1157.1583 | 1177.2481 |
| 126012 | 1163.2417 | 1172.0775 |
| 129612 | 1160.7915 | 1169.4905 |
| 133212 | 1164.9485 | 1170.9121 |
| 136812 | 1165.1465 | 1171.7410 |
| 140412 | 1167.6292 | 1171.6224 |
| 144012 | 1166.6949 | 1166.6719 |
| 147612 | 1160.9485 | 1169.2592 |
| 151212 | 1165.0776 | 1176.7531 |
| 154812 | 1164.1412 | 1173.4061 |
| 158412 | 1160.1366 | 1170.5529 |
| 162012 | 1170.9093 | 1178.0680 |
| 165612 | 1172.0600 | 1177.2763 |
| 169212 | 1160.9524 | 1171.5277 |
| 172812 | 1165.7929 | 1169.5336 |
| 176412 | 1164.6906 | 1164.9236 |
| 180012 | 1161.0158 | 1168.1160 |
| 183612 | 1163.1875 | 1170.1282 |
| 187212 | 1167.1313 | 1165.8262 |
| 190812 | 1172.5036 | 1167.5396 |
| 194412 | 1163.9779 | 1169.7524 |
| 198012 | 1163.5246 | 1165.1895 |
| 201612 | 1162.2340 | 1171.1885 |
| 205212 | 1163.2771 | 1170.4310 |
| 208812 | 1163.9772 | 1165.5687 |
| 212412 | 1168.5996 | 1164.9207 |
| 216012 | 1164.6138 | 1162.0309 |
| 219612 | 1158.8616 | 1163.0354 |
| 223212 | 1165.0799 | 1163.0894 |
| 226812 | 1163.2940 | 1166.5121 |
| 230412 | 1161.3785 | 1165.8363 |
| 234012 | 1162.5076 | 1164.2868 |
| 237612 | 1163.5597 | 1163.1084 |
| 241212 | 1163.7693 | 1165.1503 |
| 244812 | 1163.0918 | 1163.0639 |
| 248412 | 1165.2531 | 1161.6192 |
| 250008 | 1160.9823 | 1163.3766 |

(full checkpoint list written to `results/night4/night_report_checkpoints_3primev0prime.csv`, 72 rows)

### Run A checkpoint detail

- iteration of minimum held-out (checkpoint) val_loss: 82812 (val_loss=1156.0002)
- loss near iteration 25000: 1192.8249 (nearest checkpoint at iteration 25212)
- loss near iteration 50000: 1165.7000 (nearest checkpoint at iteration 50412)
- loss near iteration 100000: 1165.9084 (nearest checkpoint at iteration 100812)
- loss near iteration 150000: 1165.0776 (nearest checkpoint at iteration 151212)
- loss near iteration 200000: 1162.2340 (nearest checkpoint at iteration 201612)
- loss near iteration 250000: 1160.9823 (nearest checkpoint at iteration 250008)
- relative change of held-out loss over the last 50,000 iterations (checkpoint near 200000 -> checkpoint near 250000, positive = rose): -0.0011 (1162.2340 -> 1160.9823; plateauing by a <1% heuristic)
- discrepancy: rung val_loss at iteration 250,000 (1158.9237) vs checkpoint val_loss at iteration 250008 (1160.9823) = 2.0586 over 8 extra iteration(s)
- training-loss (train_loss_per_iter) std over last 100 iterations: 677.9452 (mean 1281.8119) -- for judging whether the discrepancy above is within iteration-to-iteration noise

### Run B checkpoint detail

- iteration of minimum held-out (checkpoint) val_loss so far: 248412 (val_loss=1161.6192)
- training-loss std over last 100 iterations: 613.9042

## Per-rung / per-checkpoint replicate differences (section 7 instrument-floor input)

Rungs:
- iteration 1000: |A-B| = 1.4939
- iteration 5000: |A-B| = 2.2517
- iteration 25000: |A-B| = 4.6728
- iteration 250000: |A-B| = 4.0137

Common checkpoints (72):
- iteration 0: |A-B| = 0.0059
- iteration 12: |A-B| = 0.4643
- iteration 3612: |A-B| = 0.5054
- iteration 7212: |A-B| = 1.2993
- iteration 10812: |A-B| = 0.4500
- iteration 14412: |A-B| = 0.4204
- iteration 18012: |A-B| = 1.6413
- iteration 21612: |A-B| = 1.7036
- iteration 25212: |A-B| = 5.6889
- iteration 28812: |A-B| = 1.3272
- iteration 32412: |A-B| = 5.1939
- iteration 36012: |A-B| = 10.1576
- iteration 39612: |A-B| = 5.4983
- iteration 43212: |A-B| = 17.0468
- iteration 46812: |A-B| = 12.9690
- iteration 50412: |A-B| = 16.6089
- iteration 54012: |A-B| = 10.3437
- iteration 57612: |A-B| = 4.9777
- iteration 61212: |A-B| = 9.0704
- iteration 64812: |A-B| = 6.1792
- iteration 68412: |A-B| = 1.5436
- iteration 72012: |A-B| = 8.5086
- iteration 75612: |A-B| = 13.7198
- iteration 79212: |A-B| = 24.9577
- iteration 82812: |A-B| = 17.6683
- iteration 86412: |A-B| = 6.3341
- iteration 90012: |A-B| = 12.0456
- iteration 93612: |A-B| = 20.6075
- iteration 97212: |A-B| = 9.4315
- iteration 100812: |A-B| = 8.3135
- iteration 104412: |A-B| = 14.1900
- iteration 108012: |A-B| = 0.9510
- iteration 111612: |A-B| = 11.2149
- iteration 115212: |A-B| = 10.2167
- iteration 118812: |A-B| = 30.8505
- iteration 122412: |A-B| = 20.0898
- iteration 126012: |A-B| = 8.8358
- iteration 129612: |A-B| = 8.6991
- iteration 133212: |A-B| = 5.9635
- iteration 136812: |A-B| = 6.5944
- iteration 140412: |A-B| = 3.9932
- iteration 144012: |A-B| = 0.0230
- iteration 147612: |A-B| = 8.3108
- iteration 151212: |A-B| = 11.6755
- iteration 154812: |A-B| = 9.2648
- iteration 158412: |A-B| = 10.4163
- iteration 162012: |A-B| = 7.1587
- iteration 165612: |A-B| = 5.2163
- iteration 169212: |A-B| = 10.5753
- iteration 172812: |A-B| = 3.7406
- iteration 176412: |A-B| = 0.2330
- iteration 180012: |A-B| = 7.1003
- iteration 183612: |A-B| = 6.9407
- iteration 187212: |A-B| = 1.3051
- iteration 190812: |A-B| = 4.9640
- iteration 194412: |A-B| = 5.7745
- iteration 198012: |A-B| = 1.6649
- iteration 201612: |A-B| = 8.9545
- iteration 205212: |A-B| = 7.1539
- iteration 208812: |A-B| = 1.5915
- iteration 212412: |A-B| = 3.6789
- iteration 216012: |A-B| = 2.5830
- iteration 219612: |A-B| = 4.1738
- iteration 223212: |A-B| = 1.9905
- iteration 226812: |A-B| = 3.2181
- iteration 230412: |A-B| = 4.4578
- iteration 234012: |A-B| = 1.7792
- iteration 237612: |A-B| = 0.4512
- iteration 241212: |A-B| = 1.3811
- iteration 244812: |A-B| = 0.0279
- iteration 248412: |A-B| = 3.6340
- iteration 250008: |A-B| = 2.3942

- max |A-B| across rungs+common checkpoints: 30.8505
- median |A-B| across rungs+common checkpoints: 5.3573

