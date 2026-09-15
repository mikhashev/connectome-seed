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

### Run B: `C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/night/night2_9991-001.json`
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

## Two-phase price (activity_penalty.stop_iter = 150000)

| run | median s/iter [1,000-150,000] | median s/iter [150,001-end] | overall median s/iter | wall sum <=150,000 (s) | wall sum >150,000 (s) | iterations seen |
|---|---|---|---|---|---|---|
| A | 0.0644 | 0.0452 | 0.0614 | 9754.0554 | 4581.2000 | 250008 |
| B | 0.0647 | 0.0459 | 0.0622 | 9797.1024 | 4653.0757 | 250008 |

(Note: precomputed `iter_wall_median_all_s` / `iter_wall_median_1000_2000_s` in the json, when present, cover different windows than this table; this table's medians/sums are computed here from `iter_wall_s` over the windows stated in the header.)
- A json field iter_wall_median_all_s: 0.0614
- A json field iter_wall_median_1000_2000_s: 0.0647
- B json field iter_wall_median_all_s: 0.0622
- B json field iter_wall_median_1000_2000_s: 0.0655

## Rung table

| iteration | val_loss A | val_loss B | B - A | relative (B-A)/A |
|---|---|---|---|---|
| 1000 | 1208.9363 | 1208.0556 | -0.8807 | -0.0007 |
| 5000 | 1207.7673 | 1206.7832 | -0.9841 | -0.0008 |
| 25000 | 1191.7375 | 1190.2235 | -1.5140 | -0.0013 |
| 250000 | 1146.1958 | 1145.3572 | -0.8386 | -0.0007 |

## Replicate difference at iteration 250,000 (pre-registration section 7 tolerance: < 1%)

- |A-B|/A at 250,000 = 0.0732%  -> PASS (< 1%)

## Checkpoint trajectory

Compact view (every 5th checkpoint by A's index; full 72-row list -> `C:/Users/mikha/Documents/dpc-research/connectome-seed/results/night2/night_report_checkpoints_1v0.csv`):

| iteration | val_loss A | val_loss B |
|---|---|---|
| 0 | 1212.5556 | 1212.5530 |
| 12 | 1212.2575 | 1211.7471 |
| 3612 | 1206.3210 | 1207.6736 |
| 7212 | 1206.1248 | 1205.8514 |
| 10812 | 1205.7025 | 1206.3547 |
| 14412 | 1206.0824 | 1206.7229 |
| 18012 | 1205.9267 | 1204.7626 |
| 21612 | 1199.3854 | 1202.0727 |
| 25212 | 1192.7493 | 1192.4103 |
| 28812 | 1184.2532 | 1182.0623 |
| 32412 | 1175.8663 | 1172.8651 |
| 36012 | 1170.1614 | 1172.3336 |
| 39612 | 1170.5515 | 1170.7335 |
| 43212 | 1170.5394 | 1158.2845 |
| 46812 | 1163.0753 | 1163.7274 |
| 50412 | 1166.7279 | 1164.7514 |
| 54012 | 1165.3890 | 1158.0555 |
| 57612 | 1163.9735 | 1161.5895 |
| 61212 | 1157.2235 | 1163.1893 |
| 64812 | 1163.9785 | 1160.8496 |
| 68412 | 1168.6454 | 1158.3862 |
| 72012 | 1156.2146 | 1161.1806 |
| 75612 | 1153.7558 | 1167.0807 |
| 79212 | 1155.2570 | 1168.7346 |
| 82812 | 1143.5370 | 1164.0633 |
| 86412 | 1155.3520 | 1161.1872 |
| 90012 | 1150.2037 | 1163.5721 |
| 93612 | 1146.0899 | 1164.9666 |
| 97212 | 1166.0588 | 1156.5755 |
| 100812 | 1159.3972 | 1174.5950 |
| 104412 | 1149.9424 | 1156.3830 |
| 108012 | 1152.2472 | 1159.6918 |
| 111612 | 1145.2592 | 1158.5442 |
| 115212 | 1162.6179 | 1159.0099 |
| 118812 | 1159.1506 | 1158.6544 |
| 122412 | 1149.5846 | 1157.7469 |
| 126012 | 1157.3147 | 1153.2412 |
| 129612 | 1155.5432 | 1154.6189 |
| 133212 | 1153.2944 | 1158.1896 |
| 136812 | 1155.7976 | 1156.6087 |
| 140412 | 1170.6714 | 1153.7491 |
| 144012 | 1154.2528 | 1152.1816 |
| 147612 | 1150.4220 | 1151.5075 |
| 151212 | 1152.8307 | 1153.5651 |
| 154812 | 1159.6491 | 1159.3759 |
| 158412 | 1148.1151 | 1157.6256 |
| 162012 | 1159.5074 | 1149.2913 |
| 165612 | 1168.3797 | 1149.6651 |
| 169212 | 1149.1648 | 1148.1312 |
| 172812 | 1154.8277 | 1151.7816 |
| 176412 | 1147.5207 | 1145.0673 |
| 180012 | 1148.9453 | 1148.6651 |
| 183612 | 1146.5118 | 1146.4211 |
| 187212 | 1150.2214 | 1149.1065 |
| 190812 | 1167.6187 | 1148.6975 |
| 194412 | 1153.1420 | 1146.5436 |
| 198012 | 1149.6872 | 1147.9998 |
| 201612 | 1147.5358 | 1147.0294 |
| 205212 | 1148.8634 | 1140.2280 |
| 208812 | 1149.8740 | 1142.9587 |
| 212412 | 1156.6829 | 1145.1025 |
| 216012 | 1152.8448 | 1143.7317 |
| 219612 | 1141.0463 | 1141.9546 |
| 223212 | 1153.7354 | 1143.8520 |
| 226812 | 1150.9120 | 1142.2662 |
| 230412 | 1148.4920 | 1141.4983 |
| 234012 | 1145.9390 | 1141.9582 |
| 237612 | 1146.7684 | 1142.3555 |
| 241212 | 1150.2581 | 1141.8480 |
| 244812 | 1147.7892 | 1141.7745 |
| 248412 | 1153.3329 | 1139.7140 |
| 250008 | 1148.8075 | 1144.6362 |

(full checkpoint list written to `C:/Users/mikha/Documents/dpc-research/connectome-seed/results/night2/night_report_checkpoints_1v0.csv`, 72 rows)

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

- iteration of minimum held-out (checkpoint) val_loss so far: 248412 (val_loss=1139.7140)
- training-loss std over last 100 iterations: 645.6156

## Per-rung / per-checkpoint replicate differences (section 7 instrument-floor input)

Rungs:
- iteration 1000: |A-B| = 0.8807
- iteration 5000: |A-B| = 0.9841
- iteration 25000: |A-B| = 1.5140
- iteration 250000: |A-B| = 0.8386

Common checkpoints (72):
- iteration 0: |A-B| = 0.0026
- iteration 12: |A-B| = 0.5104
- iteration 3612: |A-B| = 1.3526
- iteration 7212: |A-B| = 0.2734
- iteration 10812: |A-B| = 0.6521
- iteration 14412: |A-B| = 0.6405
- iteration 18012: |A-B| = 1.1641
- iteration 21612: |A-B| = 2.6873
- iteration 25212: |A-B| = 0.3390
- iteration 28812: |A-B| = 2.1908
- iteration 32412: |A-B| = 3.0012
- iteration 36012: |A-B| = 2.1722
- iteration 39612: |A-B| = 0.1820
- iteration 43212: |A-B| = 12.2549
- iteration 46812: |A-B| = 0.6521
- iteration 50412: |A-B| = 1.9765
- iteration 54012: |A-B| = 7.3334
- iteration 57612: |A-B| = 2.3840
- iteration 61212: |A-B| = 5.9658
- iteration 64812: |A-B| = 3.1290
- iteration 68412: |A-B| = 10.2592
- iteration 72012: |A-B| = 4.9660
- iteration 75612: |A-B| = 13.3249
- iteration 79212: |A-B| = 13.4777
- iteration 82812: |A-B| = 20.5262
- iteration 86412: |A-B| = 5.8351
- iteration 90012: |A-B| = 13.3684
- iteration 93612: |A-B| = 18.8767
- iteration 97212: |A-B| = 9.4833
- iteration 100812: |A-B| = 15.1978
- iteration 104412: |A-B| = 6.4406
- iteration 108012: |A-B| = 7.4446
- iteration 111612: |A-B| = 13.2849
- iteration 115212: |A-B| = 3.6080
- iteration 118812: |A-B| = 0.4962
- iteration 122412: |A-B| = 8.1623
- iteration 126012: |A-B| = 4.0735
- iteration 129612: |A-B| = 0.9243
- iteration 133212: |A-B| = 4.8952
- iteration 136812: |A-B| = 0.8110
- iteration 140412: |A-B| = 16.9223
- iteration 144012: |A-B| = 2.0712
- iteration 147612: |A-B| = 1.0854
- iteration 151212: |A-B| = 0.7344
- iteration 154812: |A-B| = 0.2732
- iteration 158412: |A-B| = 9.5105
- iteration 162012: |A-B| = 10.2161
- iteration 165612: |A-B| = 18.7146
- iteration 169212: |A-B| = 1.0335
- iteration 172812: |A-B| = 3.0460
- iteration 176412: |A-B| = 2.4533
- iteration 180012: |A-B| = 0.2802
- iteration 183612: |A-B| = 0.0907
- iteration 187212: |A-B| = 1.1148
- iteration 190812: |A-B| = 18.9212
- iteration 194412: |A-B| = 6.5984
- iteration 198012: |A-B| = 1.6874
- iteration 201612: |A-B| = 0.5064
- iteration 205212: |A-B| = 8.6355
- iteration 208812: |A-B| = 6.9152
- iteration 212412: |A-B| = 11.5804
- iteration 216012: |A-B| = 9.1131
- iteration 219612: |A-B| = 0.9084
- iteration 223212: |A-B| = 9.8834
- iteration 226812: |A-B| = 8.6458
- iteration 230412: |A-B| = 6.9937
- iteration 234012: |A-B| = 3.9807
- iteration 237612: |A-B| = 4.4128
- iteration 241212: |A-B| = 8.4101
- iteration 244812: |A-B| = 6.0147
- iteration 248412: |A-B| = 13.6190
- iteration 250008: |A-B| = 4.1713

- max |A-B| across rungs+common checkpoints: 20.5262
- median |A-B| across rungs+common checkpoints: 3.7944

