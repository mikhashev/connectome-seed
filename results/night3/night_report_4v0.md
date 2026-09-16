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

### Run B: `C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/night/night3_9991-004.json`
- id: `9991/004`
- seed: 4
- exit: `ok`
- final_iteration: 250008
- started_utc: 2026-09-16T00:35:40Z
- finished_utc: 2026-09-16T04:40:22Z
- total_train_wall_s: 14671.0791  (h:mm:ss = 4:04:31.0791)
- h_run (computed, total_train_wall_s/3600): 4.0753
- VRAM torch_max_memory_allocated_MiB: 1426.0952
- n checkpoints so far: 72
- errors: 0

## Two-phase price (activity_penalty.stop_iter = 150000)

| run | median s/iter [1,000-150,000] | median s/iter [150,001-end] | overall median s/iter | wall sum <=150,000 (s) | wall sum >150,000 (s) | iterations seen |
|---|---|---|---|---|---|---|
| A | 0.0644 | 0.0452 | 0.0614 | 9754.0554 | 4581.2000 | 250008 |
| B | 0.0634 | 0.0462 | 0.0598 | 9770.7660 | 4820.8936 | 250008 |

(Note: precomputed `iter_wall_median_all_s` / `iter_wall_median_1000_2000_s` in the json, when present, cover different windows than this table; this table's medians/sums are computed here from `iter_wall_s` over the windows stated in the header.)
- A json field iter_wall_median_all_s: 0.0614
- A json field iter_wall_median_1000_2000_s: 0.0647
- B json field iter_wall_median_all_s: 0.0598
- B json field iter_wall_median_1000_2000_s: 0.0628

## Rung table

| iteration | val_loss A | val_loss B | B - A | relative (B-A)/A |
|---|---|---|---|---|
| 1000 | 1208.9363 | 1207.2574 | -1.6788 | -0.0014 |
| 5000 | 1207.7673 | 1206.3897 | -1.3776 | -0.0011 |
| 25000 | 1191.7375 | 1208.6099 | 16.8725 | 0.0142 |
| 250000 | 1146.1958 | 1153.1134 | 6.9176 | 0.0060 |

## Replicate difference at iteration 250,000 (pre-registration section 7 tolerance: < 1%)

- |A-B|/A at 250,000 = 0.6035%  -> PASS (< 1%)

## Checkpoint trajectory

Compact view (every 5th checkpoint by A's index; full 72-row list -> `results/night3/night_report_checkpoints_4v0.csv`):

| iteration | val_loss A | val_loss B |
|---|---|---|
| 0 | 1212.5556 | 1212.5379 |
| 12 | 1212.2575 | 1211.5978 |
| 3612 | 1206.3210 | 1206.0793 |
| 7212 | 1206.1248 | 1206.3119 |
| 10812 | 1205.7025 | 1206.7002 |
| 14412 | 1206.0824 | 1205.5813 |
| 18012 | 1205.9267 | 1206.9632 |
| 21612 | 1199.3854 | 1206.3360 |
| 25212 | 1192.7493 | 1203.2849 |
| 28812 | 1184.2532 | 1200.1395 |
| 32412 | 1175.8663 | 1199.8397 |
| 36012 | 1170.1614 | 1193.6561 |
| 39612 | 1170.5515 | 1199.5359 |
| 43212 | 1170.5394 | 1191.8077 |
| 46812 | 1163.0753 | 1193.7603 |
| 50412 | 1166.7279 | 1188.8332 |
| 54012 | 1165.3890 | 1192.8853 |
| 57612 | 1163.9735 | 1204.4671 |
| 61212 | 1157.2235 | 1189.0000 |
| 64812 | 1163.9785 | 1186.5255 |
| 68412 | 1168.6454 | 1181.1303 |
| 72012 | 1156.2146 | 1183.9026 |
| 75612 | 1153.7558 | 1191.7330 |
| 79212 | 1155.2570 | 1172.1331 |
| 82812 | 1143.5370 | 1171.6938 |
| 86412 | 1155.3520 | 1174.7523 |
| 90012 | 1150.2037 | 1174.6881 |
| 93612 | 1146.0899 | 1170.5908 |
| 97212 | 1166.0588 | 1168.6568 |
| 100812 | 1159.3972 | 1170.7871 |
| 104412 | 1149.9424 | 1168.4854 |
| 108012 | 1152.2472 | 1169.1170 |
| 111612 | 1145.2592 | 1164.0211 |
| 115212 | 1162.6179 | 1178.2952 |
| 118812 | 1159.1506 | 1170.6738 |
| 122412 | 1149.5846 | 1161.0397 |
| 126012 | 1157.3147 | 1166.7338 |
| 129612 | 1155.5432 | 1159.7117 |
| 133212 | 1153.2944 | 1164.9900 |
| 136812 | 1155.7976 | 1157.7596 |
| 140412 | 1170.6714 | 1165.0009 |
| 144012 | 1154.2528 | 1164.5611 |
| 147612 | 1150.4220 | 1157.6570 |
| 151212 | 1152.8307 | 1158.9330 |
| 154812 | 1159.6491 | 1153.7937 |
| 158412 | 1148.1151 | 1159.5167 |
| 162012 | 1159.5074 | 1158.1918 |
| 165612 | 1168.3797 | 1163.4019 |
| 169212 | 1149.1648 | 1164.2380 |
| 172812 | 1154.8277 | 1165.6907 |
| 176412 | 1147.5207 | 1164.7708 |
| 180012 | 1148.9453 | 1162.0929 |
| 183612 | 1146.5118 | 1158.0984 |
| 187212 | 1150.2214 | 1158.7704 |
| 190812 | 1167.6187 | 1155.6889 |
| 194412 | 1153.1420 | 1155.9827 |
| 198012 | 1149.6872 | 1150.0934 |
| 201612 | 1147.5358 | 1156.3831 |
| 205212 | 1148.8634 | 1155.4481 |
| 208812 | 1149.8740 | 1155.9806 |
| 212412 | 1156.6829 | 1150.1047 |
| 216012 | 1152.8448 | 1164.9290 |
| 219612 | 1141.0463 | 1150.2354 |
| 223212 | 1153.7354 | 1156.4332 |
| 226812 | 1150.9120 | 1151.3413 |
| 230412 | 1148.4920 | 1154.4686 |
| 234012 | 1145.9390 | 1156.1329 |
| 237612 | 1146.7684 | 1159.1522 |
| 241212 | 1150.2581 | 1156.4283 |
| 244812 | 1147.7892 | 1152.1362 |
| 248412 | 1153.3329 | 1151.6806 |
| 250008 | 1148.8075 | 1156.8285 |

(full checkpoint list written to `results/night3/night_report_checkpoints_4v0.csv`, 72 rows)

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

- iteration of minimum held-out (checkpoint) val_loss so far: 198012 (val_loss=1150.0934)
- training-loss std over last 100 iterations: 671.5713

## Per-rung / per-checkpoint replicate differences (section 7 instrument-floor input)

Rungs:
- iteration 1000: |A-B| = 1.6788
- iteration 5000: |A-B| = 1.3776
- iteration 25000: |A-B| = 16.8725
- iteration 250000: |A-B| = 6.9176

Common checkpoints (72):
- iteration 0: |A-B| = 0.0176
- iteration 12: |A-B| = 0.6598
- iteration 3612: |A-B| = 0.2417
- iteration 7212: |A-B| = 0.1871
- iteration 10812: |A-B| = 0.9977
- iteration 14412: |A-B| = 0.5010
- iteration 18012: |A-B| = 1.0365
- iteration 21612: |A-B| = 6.9506
- iteration 25212: |A-B| = 10.5356
- iteration 28812: |A-B| = 15.8864
- iteration 32412: |A-B| = 23.9734
- iteration 36012: |A-B| = 23.4948
- iteration 39612: |A-B| = 28.9845
- iteration 43212: |A-B| = 21.2683
- iteration 46812: |A-B| = 30.6850
- iteration 50412: |A-B| = 22.1054
- iteration 54012: |A-B| = 27.4963
- iteration 57612: |A-B| = 40.4936
- iteration 61212: |A-B| = 31.7764
- iteration 64812: |A-B| = 22.5469
- iteration 68412: |A-B| = 12.4848
- iteration 72012: |A-B| = 27.6880
- iteration 75612: |A-B| = 37.9773
- iteration 79212: |A-B| = 16.8761
- iteration 82812: |A-B| = 28.1568
- iteration 86412: |A-B| = 19.4003
- iteration 90012: |A-B| = 24.4844
- iteration 93612: |A-B| = 24.5009
- iteration 97212: |A-B| = 2.5980
- iteration 100812: |A-B| = 11.3899
- iteration 104412: |A-B| = 18.5430
- iteration 108012: |A-B| = 16.8698
- iteration 111612: |A-B| = 18.7618
- iteration 115212: |A-B| = 15.6773
- iteration 118812: |A-B| = 11.5233
- iteration 122412: |A-B| = 11.4550
- iteration 126012: |A-B| = 9.4191
- iteration 129612: |A-B| = 4.1685
- iteration 133212: |A-B| = 11.6956
- iteration 136812: |A-B| = 1.9620
- iteration 140412: |A-B| = 5.6705
- iteration 144012: |A-B| = 10.3084
- iteration 147612: |A-B| = 7.2350
- iteration 151212: |A-B| = 6.1023
- iteration 154812: |A-B| = 5.8553
- iteration 158412: |A-B| = 11.4016
- iteration 162012: |A-B| = 1.3156
- iteration 165612: |A-B| = 4.9778
- iteration 169212: |A-B| = 15.0732
- iteration 172812: |A-B| = 10.8631
- iteration 176412: |A-B| = 17.2501
- iteration 180012: |A-B| = 13.1476
- iteration 183612: |A-B| = 11.5866
- iteration 187212: |A-B| = 8.5491
- iteration 190812: |A-B| = 11.9298
- iteration 194412: |A-B| = 2.8406
- iteration 198012: |A-B| = 0.4062
- iteration 201612: |A-B| = 8.8473
- iteration 205212: |A-B| = 6.5847
- iteration 208812: |A-B| = 6.1066
- iteration 212412: |A-B| = 6.5782
- iteration 216012: |A-B| = 12.0843
- iteration 219612: |A-B| = 9.1891
- iteration 223212: |A-B| = 2.6979
- iteration 226812: |A-B| = 0.4293
- iteration 230412: |A-B| = 5.9766
- iteration 234012: |A-B| = 10.1939
- iteration 237612: |A-B| = 12.3839
- iteration 241212: |A-B| = 6.1702
- iteration 244812: |A-B| = 4.3470
- iteration 248412: |A-B| = 1.6524
- iteration 250008: |A-B| = 8.0210

- max |A-B| across rungs+common checkpoints: 40.4936
- median |A-B| across rungs+common checkpoints: 10.4220

