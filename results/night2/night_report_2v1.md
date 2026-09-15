# Flyvis night report

### Run A: `C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/night/night2_9991-001.json`
- id: `9991/001`
- seed: 1
- exit: `ok`
- final_iteration: 250008
- started_utc: 2026-09-14T19:12:34Z
- finished_utc: 2026-09-14T23:14:59Z
- total_train_wall_s: 14532.8769  (h:mm:ss = 4:02:12.8769)
- h_run (computed, total_train_wall_s/3600): 4.0369
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
| A | 0.0647 | 0.0459 | 0.0622 | 9797.1024 | 4653.0757 | 250008 |
| B | 0.0636 | 0.0454 | 0.0611 | 9619.3084 | 4595.3355 | 250008 |

(Note: precomputed `iter_wall_median_all_s` / `iter_wall_median_1000_2000_s` in the json, when present, cover different windows than this table; this table's medians/sums are computed here from `iter_wall_s` over the windows stated in the header.)
- A json field iter_wall_median_all_s: 0.0622
- A json field iter_wall_median_1000_2000_s: 0.0655
- B json field iter_wall_median_all_s: 0.0611
- B json field iter_wall_median_1000_2000_s: 0.0637

## Rung table

| iteration | val_loss A | val_loss B | B - A | relative (B-A)/A |
|---|---|---|---|---|
| 1000 | 1208.0556 | 1209.7639 | 1.7083 | 0.0014 |
| 5000 | 1206.7832 | 1207.0115 | 0.2283 | 0.0002 |
| 25000 | 1190.2235 | 1204.3618 | 14.1383 | 0.0119 |
| 250000 | 1145.3572 | 1148.8000 | 3.4428 | 0.0030 |

## Replicate difference at iteration 250,000 (pre-registration section 7 tolerance: < 1%)

- |A-B|/A at 250,000 = 0.3006%  -> PASS (< 1%)

## Checkpoint trajectory

Compact view (every 5th checkpoint by A's index; full 72-row list -> `C:/Users/mikha/Documents/dpc-research/connectome-seed/results/night2/night_report_checkpoints_2v1.csv`):

| iteration | val_loss A | val_loss B |
|---|---|---|
| 0 | 1212.5530 | 1212.5592 |
| 12 | 1211.7471 | 1211.8746 |
| 3612 | 1207.6736 | 1208.0228 |
| 7212 | 1205.8514 | 1206.3706 |
| 10812 | 1206.3547 | 1206.7138 |
| 14412 | 1206.7229 | 1206.7620 |
| 18012 | 1204.7626 | 1206.3075 |
| 21612 | 1202.0727 | 1205.1803 |
| 25212 | 1192.4103 | 1205.9782 |
| 28812 | 1182.0623 | 1200.7650 |
| 32412 | 1172.8651 | 1199.5604 |
| 36012 | 1172.3336 | 1196.1473 |
| 39612 | 1170.7335 | 1196.9538 |
| 43212 | 1158.2845 | 1193.0629 |
| 46812 | 1163.7274 | 1183.0116 |
| 50412 | 1164.7514 | 1175.8456 |
| 54012 | 1158.0555 | 1178.6471 |
| 57612 | 1161.5895 | 1168.6929 |
| 61212 | 1163.1893 | 1165.1369 |
| 64812 | 1160.8496 | 1149.7257 |
| 68412 | 1158.3862 | 1156.3343 |
| 72012 | 1161.1806 | 1168.7742 |
| 75612 | 1167.0807 | 1157.9509 |
| 79212 | 1168.7346 | 1147.7080 |
| 82812 | 1164.0633 | 1153.2110 |
| 86412 | 1161.1872 | 1154.2440 |
| 90012 | 1163.5721 | 1147.5056 |
| 93612 | 1164.9666 | 1156.8112 |
| 97212 | 1156.5755 | 1139.1152 |
| 100812 | 1174.5950 | 1149.9595 |
| 104412 | 1156.3830 | 1149.5918 |
| 108012 | 1159.6918 | 1149.0315 |
| 111612 | 1158.5442 | 1153.7517 |
| 115212 | 1159.0099 | 1141.7914 |
| 118812 | 1158.6544 | 1148.1022 |
| 122412 | 1157.7469 | 1144.9998 |
| 126012 | 1153.2412 | 1149.9144 |
| 129612 | 1154.6189 | 1152.9115 |
| 133212 | 1158.1896 | 1145.8231 |
| 136812 | 1156.6087 | 1142.9586 |
| 140412 | 1153.7491 | 1146.4059 |
| 144012 | 1152.1816 | 1149.9946 |
| 147612 | 1151.5075 | 1143.3270 |
| 151212 | 1153.5651 | 1144.9134 |
| 154812 | 1159.3759 | 1156.1772 |
| 158412 | 1157.6256 | 1148.1535 |
| 162012 | 1149.2913 | 1137.8219 |
| 165612 | 1149.6651 | 1152.2316 |
| 169212 | 1148.1312 | 1156.9998 |
| 172812 | 1151.7816 | 1139.5149 |
| 176412 | 1145.0673 | 1148.1521 |
| 180012 | 1148.6651 | 1156.9476 |
| 183612 | 1146.4211 | 1147.0188 |
| 187212 | 1149.1065 | 1149.0120 |
| 190812 | 1148.6975 | 1147.2483 |
| 194412 | 1146.5436 | 1152.4356 |
| 198012 | 1147.9998 | 1145.2095 |
| 201612 | 1147.0294 | 1150.5090 |
| 205212 | 1140.2280 | 1145.6015 |
| 208812 | 1142.9587 | 1150.0096 |
| 212412 | 1145.1025 | 1144.7976 |
| 216012 | 1143.7317 | 1154.1877 |
| 219612 | 1141.9546 | 1144.7344 |
| 223212 | 1143.8520 | 1151.4877 |
| 226812 | 1142.2662 | 1146.3343 |
| 230412 | 1141.4983 | 1147.0198 |
| 234012 | 1141.9582 | 1145.3685 |
| 237612 | 1142.3555 | 1146.1783 |
| 241212 | 1141.8480 | 1148.0285 |
| 244812 | 1141.7745 | 1143.3601 |
| 248412 | 1139.7140 | 1148.6122 |
| 250008 | 1144.6362 | 1147.7179 |

(full checkpoint list written to `C:/Users/mikha/Documents/dpc-research/connectome-seed/results/night2/night_report_checkpoints_2v1.csv`, 72 rows)

### Run A checkpoint detail

- iteration of minimum held-out (checkpoint) val_loss: 248412 (val_loss=1139.7140)
- loss near iteration 25000: 1192.4103 (nearest checkpoint at iteration 25212)
- loss near iteration 50000: 1164.7514 (nearest checkpoint at iteration 50412)
- loss near iteration 100000: 1174.5950 (nearest checkpoint at iteration 100812)
- loss near iteration 150000: 1153.5651 (nearest checkpoint at iteration 151212)
- loss near iteration 200000: 1147.0294 (nearest checkpoint at iteration 201612)
- loss near iteration 250000: 1144.6362 (nearest checkpoint at iteration 250008)
- relative change of held-out loss over the last 50,000 iterations (checkpoint near 200000 -> checkpoint near 250000, positive = rose): -0.0021 (1147.0294 -> 1144.6362; plateauing by a <1% heuristic)
- discrepancy: rung val_loss at iteration 250,000 (1145.3572) vs checkpoint val_loss at iteration 250008 (1144.6362) = -0.7210 over 8 extra iteration(s)
- training-loss (train_loss_per_iter) std over last 100 iterations: 645.6156 (mean 1255.7309) -- for judging whether the discrepancy above is within iteration-to-iteration noise

### Run B checkpoint detail

- iteration of minimum held-out (checkpoint) val_loss so far: 162012 (val_loss=1137.8219)
- training-loss std over last 100 iterations: 577.1513

## Per-rung / per-checkpoint replicate differences (section 7 instrument-floor input)

Rungs:
- iteration 1000: |A-B| = 1.7083
- iteration 5000: |A-B| = 0.2283
- iteration 25000: |A-B| = 14.1383
- iteration 250000: |A-B| = 3.4428

Common checkpoints (72):
- iteration 0: |A-B| = 0.0062
- iteration 12: |A-B| = 0.1276
- iteration 3612: |A-B| = 0.3492
- iteration 7212: |A-B| = 0.5192
- iteration 10812: |A-B| = 0.3591
- iteration 14412: |A-B| = 0.0391
- iteration 18012: |A-B| = 1.5449
- iteration 21612: |A-B| = 3.1076
- iteration 25212: |A-B| = 13.5679
- iteration 28812: |A-B| = 18.7027
- iteration 32412: |A-B| = 26.6953
- iteration 36012: |A-B| = 23.8138
- iteration 39612: |A-B| = 26.2203
- iteration 43212: |A-B| = 34.7784
- iteration 46812: |A-B| = 19.2841
- iteration 50412: |A-B| = 11.0942
- iteration 54012: |A-B| = 20.5916
- iteration 57612: |A-B| = 7.1034
- iteration 61212: |A-B| = 1.9476
- iteration 64812: |A-B| = 11.1238
- iteration 68412: |A-B| = 2.0519
- iteration 72012: |A-B| = 7.5936
- iteration 75612: |A-B| = 9.1298
- iteration 79212: |A-B| = 21.0266
- iteration 82812: |A-B| = 10.8522
- iteration 86412: |A-B| = 6.9431
- iteration 90012: |A-B| = 16.0665
- iteration 93612: |A-B| = 8.1553
- iteration 97212: |A-B| = 17.4602
- iteration 100812: |A-B| = 24.6355
- iteration 104412: |A-B| = 6.7912
- iteration 108012: |A-B| = 10.6603
- iteration 111612: |A-B| = 4.7925
- iteration 115212: |A-B| = 17.2184
- iteration 118812: |A-B| = 10.5522
- iteration 122412: |A-B| = 12.7471
- iteration 126012: |A-B| = 3.3268
- iteration 129612: |A-B| = 1.7074
- iteration 133212: |A-B| = 12.3665
- iteration 136812: |A-B| = 13.6501
- iteration 140412: |A-B| = 7.3432
- iteration 144012: |A-B| = 2.1869
- iteration 147612: |A-B| = 8.1804
- iteration 151212: |A-B| = 8.6517
- iteration 154812: |A-B| = 3.1987
- iteration 158412: |A-B| = 9.4721
- iteration 162012: |A-B| = 11.4694
- iteration 165612: |A-B| = 2.5665
- iteration 169212: |A-B| = 8.8686
- iteration 172812: |A-B| = 12.2667
- iteration 176412: |A-B| = 3.0847
- iteration 180012: |A-B| = 8.2825
- iteration 183612: |A-B| = 0.5977
- iteration 187212: |A-B| = 0.0946
- iteration 190812: |A-B| = 1.4492
- iteration 194412: |A-B| = 5.8920
- iteration 198012: |A-B| = 2.7903
- iteration 201612: |A-B| = 3.4796
- iteration 205212: |A-B| = 5.3735
- iteration 208812: |A-B| = 7.0508
- iteration 212412: |A-B| = 0.3049
- iteration 216012: |A-B| = 10.4559
- iteration 219612: |A-B| = 2.7797
- iteration 223212: |A-B| = 7.6358
- iteration 226812: |A-B| = 4.0681
- iteration 230412: |A-B| = 5.5215
- iteration 234012: |A-B| = 3.4102
- iteration 237612: |A-B| = 3.8228
- iteration 241212: |A-B| = 6.1805
- iteration 244812: |A-B| = 1.5856
- iteration 248412: |A-B| = 8.8982
- iteration 250008: |A-B| = 3.0816

- max |A-B| across rungs+common checkpoints: 34.7784
- median |A-B| across rungs+common checkpoints: 6.9970

