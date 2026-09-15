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

### Run B: `C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/night/night2b_9991-002.json`
- id: `9991/002`
- seed: 2
- exit: `ok`
- final_iteration: 250008
- started_utc: 2026-09-15T01:13:49Z
- finished_utc: 2026-09-15T05:12:17Z
- total_train_wall_s: 14296.6488  (h:mm:ss = 3:58:16.6488)
- h_run (computed, total_train_wall_s/3600): 3.9713
- VRAM torch_max_memory_allocated_MiB: 1426.0952
- n checkpoints so far: 72
- errors: 0

## Two-phase price (activity_penalty.stop_iter = 150000)

| run | median s/iter [1,000-150,000] | median s/iter [150,001-end] | overall median s/iter | wall sum <=150,000 (s) | wall sum >150,000 (s) | iterations seen |
|---|---|---|---|---|---|---|
| A | 0.0644 | 0.0452 | 0.0614 | 9754.0554 | 4581.2000 | 250008 |
| B | 0.0636 | 0.0454 | 0.0611 | 9619.3084 | 4595.3355 | 250008 |

(Note: precomputed `iter_wall_median_all_s` / `iter_wall_median_1000_2000_s` in the json, when present, cover different windows than this table; this table's medians/sums are computed here from `iter_wall_s` over the windows stated in the header.)
- A json field iter_wall_median_all_s: 0.0614
- A json field iter_wall_median_1000_2000_s: 0.0647
- B json field iter_wall_median_all_s: 0.0611
- B json field iter_wall_median_1000_2000_s: 0.0637

## Rung table

| iteration | val_loss A | val_loss B | B - A | relative (B-A)/A |
|---|---|---|---|---|
| 1000 | 1208.9363 | 1209.7639 | 0.8276 | 0.0007 |
| 5000 | 1207.7673 | 1207.0115 | -0.7558 | -0.0006 |
| 25000 | 1191.7375 | 1204.3618 | 12.6243 | 0.0106 |
| 250000 | 1146.1958 | 1148.8000 | 2.6042 | 0.0023 |

## Replicate difference at iteration 250,000 (pre-registration section 7 tolerance: < 1%)

- |A-B|/A at 250,000 = 0.2272%  -> PASS (< 1%)

## Checkpoint trajectory

Compact view (every 5th checkpoint by A's index; full 72-row list -> `C:/Users/mikha/Documents/dpc-research/connectome-seed/results/night2/night_report_checkpoints_2v0.csv`):

| iteration | val_loss A | val_loss B |
|---|---|---|
| 0 | 1212.5556 | 1212.5592 |
| 12 | 1212.2575 | 1211.8746 |
| 3612 | 1206.3210 | 1208.0228 |
| 7212 | 1206.1248 | 1206.3706 |
| 10812 | 1205.7025 | 1206.7138 |
| 14412 | 1206.0824 | 1206.7620 |
| 18012 | 1205.9267 | 1206.3075 |
| 21612 | 1199.3854 | 1205.1803 |
| 25212 | 1192.7493 | 1205.9782 |
| 28812 | 1184.2532 | 1200.7650 |
| 32412 | 1175.8663 | 1199.5604 |
| 36012 | 1170.1614 | 1196.1473 |
| 39612 | 1170.5515 | 1196.9538 |
| 43212 | 1170.5394 | 1193.0629 |
| 46812 | 1163.0753 | 1183.0116 |
| 50412 | 1166.7279 | 1175.8456 |
| 54012 | 1165.3890 | 1178.6471 |
| 57612 | 1163.9735 | 1168.6929 |
| 61212 | 1157.2235 | 1165.1369 |
| 64812 | 1163.9785 | 1149.7257 |
| 68412 | 1168.6454 | 1156.3343 |
| 72012 | 1156.2146 | 1168.7742 |
| 75612 | 1153.7558 | 1157.9509 |
| 79212 | 1155.2570 | 1147.7080 |
| 82812 | 1143.5370 | 1153.2110 |
| 86412 | 1155.3520 | 1154.2440 |
| 90012 | 1150.2037 | 1147.5056 |
| 93612 | 1146.0899 | 1156.8112 |
| 97212 | 1166.0588 | 1139.1152 |
| 100812 | 1159.3972 | 1149.9595 |
| 104412 | 1149.9424 | 1149.5918 |
| 108012 | 1152.2472 | 1149.0315 |
| 111612 | 1145.2592 | 1153.7517 |
| 115212 | 1162.6179 | 1141.7914 |
| 118812 | 1159.1506 | 1148.1022 |
| 122412 | 1149.5846 | 1144.9998 |
| 126012 | 1157.3147 | 1149.9144 |
| 129612 | 1155.5432 | 1152.9115 |
| 133212 | 1153.2944 | 1145.8231 |
| 136812 | 1155.7976 | 1142.9586 |
| 140412 | 1170.6714 | 1146.4059 |
| 144012 | 1154.2528 | 1149.9946 |
| 147612 | 1150.4220 | 1143.3270 |
| 151212 | 1152.8307 | 1144.9134 |
| 154812 | 1159.6491 | 1156.1772 |
| 158412 | 1148.1151 | 1148.1535 |
| 162012 | 1159.5074 | 1137.8219 |
| 165612 | 1168.3797 | 1152.2316 |
| 169212 | 1149.1648 | 1156.9998 |
| 172812 | 1154.8277 | 1139.5149 |
| 176412 | 1147.5207 | 1148.1521 |
| 180012 | 1148.9453 | 1156.9476 |
| 183612 | 1146.5118 | 1147.0188 |
| 187212 | 1150.2214 | 1149.0120 |
| 190812 | 1167.6187 | 1147.2483 |
| 194412 | 1153.1420 | 1152.4356 |
| 198012 | 1149.6872 | 1145.2095 |
| 201612 | 1147.5358 | 1150.5090 |
| 205212 | 1148.8634 | 1145.6015 |
| 208812 | 1149.8740 | 1150.0096 |
| 212412 | 1156.6829 | 1144.7976 |
| 216012 | 1152.8448 | 1154.1877 |
| 219612 | 1141.0463 | 1144.7344 |
| 223212 | 1153.7354 | 1151.4877 |
| 226812 | 1150.9120 | 1146.3343 |
| 230412 | 1148.4920 | 1147.0198 |
| 234012 | 1145.9390 | 1145.3685 |
| 237612 | 1146.7684 | 1146.1783 |
| 241212 | 1150.2581 | 1148.0285 |
| 244812 | 1147.7892 | 1143.3601 |
| 248412 | 1153.3329 | 1148.6122 |
| 250008 | 1148.8075 | 1147.7179 |

(full checkpoint list written to `C:/Users/mikha/Documents/dpc-research/connectome-seed/results/night2/night_report_checkpoints_2v0.csv`, 72 rows)

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

- iteration of minimum held-out (checkpoint) val_loss so far: 162012 (val_loss=1137.8219)
- training-loss std over last 100 iterations: 577.1513

## Per-rung / per-checkpoint replicate differences (section 7 instrument-floor input)

Rungs:
- iteration 1000: |A-B| = 0.8276
- iteration 5000: |A-B| = 0.7558
- iteration 25000: |A-B| = 12.6243
- iteration 250000: |A-B| = 2.6042

Common checkpoints (72):
- iteration 0: |A-B| = 0.0036
- iteration 12: |A-B| = 0.3829
- iteration 3612: |A-B| = 1.7019
- iteration 7212: |A-B| = 0.2458
- iteration 10812: |A-B| = 1.0113
- iteration 14412: |A-B| = 0.6796
- iteration 18012: |A-B| = 0.3808
- iteration 21612: |A-B| = 5.7949
- iteration 25212: |A-B| = 13.2288
- iteration 28812: |A-B| = 16.5119
- iteration 32412: |A-B| = 23.6941
- iteration 36012: |A-B| = 25.9860
- iteration 39612: |A-B| = 26.4024
- iteration 43212: |A-B| = 22.5235
- iteration 46812: |A-B| = 19.9363
- iteration 50412: |A-B| = 9.1177
- iteration 54012: |A-B| = 13.2581
- iteration 57612: |A-B| = 4.7194
- iteration 61212: |A-B| = 7.9133
- iteration 64812: |A-B| = 14.2528
- iteration 68412: |A-B| = 12.3112
- iteration 72012: |A-B| = 12.5597
- iteration 75612: |A-B| = 4.1952
- iteration 79212: |A-B| = 7.5489
- iteration 82812: |A-B| = 9.6740
- iteration 86412: |A-B| = 1.1080
- iteration 90012: |A-B| = 2.6981
- iteration 93612: |A-B| = 10.7213
- iteration 97212: |A-B| = 26.9436
- iteration 100812: |A-B| = 9.4377
- iteration 104412: |A-B| = 0.3506
- iteration 108012: |A-B| = 3.2157
- iteration 111612: |A-B| = 8.4925
- iteration 115212: |A-B| = 20.8264
- iteration 118812: |A-B| = 11.0483
- iteration 122412: |A-B| = 4.5848
- iteration 126012: |A-B| = 7.4003
- iteration 129612: |A-B| = 2.6316
- iteration 133212: |A-B| = 7.4713
- iteration 136812: |A-B| = 12.8390
- iteration 140412: |A-B| = 24.2654
- iteration 144012: |A-B| = 4.2581
- iteration 147612: |A-B| = 7.0950
- iteration 151212: |A-B| = 7.9173
- iteration 154812: |A-B| = 3.4719
- iteration 158412: |A-B| = 0.0384
- iteration 162012: |A-B| = 21.6855
- iteration 165612: |A-B| = 16.1482
- iteration 169212: |A-B| = 7.8351
- iteration 172812: |A-B| = 15.3127
- iteration 176412: |A-B| = 0.6314
- iteration 180012: |A-B| = 8.0023
- iteration 183612: |A-B| = 0.5071
- iteration 187212: |A-B| = 1.2094
- iteration 190812: |A-B| = 20.3705
- iteration 194412: |A-B| = 0.7064
- iteration 198012: |A-B| = 4.4778
- iteration 201612: |A-B| = 2.9732
- iteration 205212: |A-B| = 3.2620
- iteration 208812: |A-B| = 0.1356
- iteration 212412: |A-B| = 11.8853
- iteration 216012: |A-B| = 1.3429
- iteration 219612: |A-B| = 3.6881
- iteration 223212: |A-B| = 2.2477
- iteration 226812: |A-B| = 4.5777
- iteration 230412: |A-B| = 1.4722
- iteration 234012: |A-B| = 0.5705
- iteration 237612: |A-B| = 0.5900
- iteration 241212: |A-B| = 2.2296
- iteration 244812: |A-B| = 4.4291
- iteration 248412: |A-B| = 4.7208
- iteration 250008: |A-B| = 1.0896

- max |A-B| across rungs+common checkpoints: 26.9436
- median |A-B| across rungs+common checkpoints: 4.6521

