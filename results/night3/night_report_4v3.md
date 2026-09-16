# Flyvis night report

### Run A: `C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/night/night3_9991-003.json`
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
| A | 0.0642 | 0.0447 | 0.0612 | 9723.2724 | 4596.6236 | 250008 |
| B | 0.0634 | 0.0462 | 0.0598 | 9770.7660 | 4820.8936 | 250008 |

(Note: precomputed `iter_wall_median_all_s` / `iter_wall_median_1000_2000_s` in the json, when present, cover different windows than this table; this table's medians/sums are computed here from `iter_wall_s` over the windows stated in the header.)
- A json field iter_wall_median_all_s: 0.0612
- A json field iter_wall_median_1000_2000_s: 0.0660
- B json field iter_wall_median_all_s: 0.0598
- B json field iter_wall_median_1000_2000_s: 0.0628

## Rung table

| iteration | val_loss A | val_loss B | B - A | relative (B-A)/A |
|---|---|---|---|---|
| 1000 | 1210.4139 | 1207.2574 | -3.1564 | -0.0026 |
| 5000 | 1205.5457 | 1206.3897 | 0.8440 | 0.0007 |
| 25000 | 1192.5858 | 1208.6099 | 16.0241 | 0.0134 |
| 250000 | 1152.5066 | 1153.1134 | 0.6069 | 0.0005 |

## Replicate difference at iteration 250,000 (pre-registration section 7 tolerance: < 1%)

- |A-B|/A at 250,000 = 0.0527%  -> PASS (< 1%)

## Checkpoint trajectory

Compact view (every 5th checkpoint by A's index; full 72-row list -> `results/night3/night_report_checkpoints_4v3.csv`):

| iteration | val_loss A | val_loss B |
|---|---|---|
| 0 | 1212.5497 | 1212.5379 |
| 12 | 1211.7933 | 1211.5978 |
| 3612 | 1206.8331 | 1206.0793 |
| 7212 | 1207.4437 | 1206.3119 |
| 10812 | 1206.1021 | 1206.7002 |
| 14412 | 1206.2946 | 1205.5813 |
| 18012 | 1204.1880 | 1206.9632 |
| 21612 | 1201.7573 | 1206.3360 |
| 25212 | 1190.0517 | 1203.2849 |
| 28812 | 1184.5230 | 1200.1395 |
| 32412 | 1174.2851 | 1199.8397 |
| 36012 | 1179.1252 | 1193.6561 |
| 39612 | 1174.0103 | 1199.5359 |
| 43212 | 1179.8168 | 1191.8077 |
| 46812 | 1168.8909 | 1193.7603 |
| 50412 | 1179.0335 | 1188.8332 |
| 54012 | 1171.3346 | 1192.8853 |
| 57612 | 1164.6277 | 1204.4671 |
| 61212 | 1174.0634 | 1189.0000 |
| 64812 | 1165.9828 | 1186.5255 |
| 68412 | 1174.3908 | 1181.1303 |
| 72012 | 1178.1888 | 1183.9026 |
| 75612 | 1166.0802 | 1191.7330 |
| 79212 | 1174.6413 | 1172.1331 |
| 82812 | 1164.9092 | 1171.6938 |
| 86412 | 1169.4652 | 1174.7523 |
| 90012 | 1171.1677 | 1174.6881 |
| 93612 | 1175.2162 | 1170.5908 |
| 97212 | 1173.9763 | 1168.6568 |
| 100812 | 1168.6564 | 1170.7871 |
| 104412 | 1172.8285 | 1168.4854 |
| 108012 | 1163.5787 | 1169.1170 |
| 111612 | 1161.7089 | 1164.0211 |
| 115212 | 1170.3667 | 1178.2952 |
| 118812 | 1174.6678 | 1170.6738 |
| 122412 | 1170.5868 | 1161.0397 |
| 126012 | 1167.1255 | 1166.7338 |
| 129612 | 1167.4171 | 1159.7117 |
| 133212 | 1168.2857 | 1164.9900 |
| 136812 | 1176.3770 | 1157.7596 |
| 140412 | 1163.0901 | 1165.0009 |
| 144012 | 1163.1483 | 1164.5611 |
| 147612 | 1161.3737 | 1157.6570 |
| 151212 | 1165.2208 | 1158.9330 |
| 154812 | 1165.6917 | 1153.7937 |
| 158412 | 1167.5395 | 1159.5167 |
| 162012 | 1181.6246 | 1158.1918 |
| 165612 | 1166.1481 | 1163.4019 |
| 169212 | 1171.6817 | 1164.2380 |
| 172812 | 1166.0327 | 1165.6907 |
| 176412 | 1158.8479 | 1164.7708 |
| 180012 | 1166.3808 | 1162.0929 |
| 183612 | 1169.6822 | 1158.0984 |
| 187212 | 1161.4556 | 1158.7704 |
| 190812 | 1162.5909 | 1155.6889 |
| 194412 | 1161.2928 | 1155.9827 |
| 198012 | 1152.6912 | 1150.0934 |
| 201612 | 1163.2382 | 1156.3831 |
| 205212 | 1162.3037 | 1155.4481 |
| 208812 | 1158.1978 | 1155.9806 |
| 212412 | 1160.7131 | 1150.1047 |
| 216012 | 1153.3346 | 1164.9290 |
| 219612 | 1157.4240 | 1150.2354 |
| 223212 | 1152.8706 | 1156.4332 |
| 226812 | 1155.5818 | 1151.3413 |
| 230412 | 1155.2349 | 1154.4686 |
| 234012 | 1156.2054 | 1156.1329 |
| 237612 | 1150.9345 | 1159.1522 |
| 241212 | 1153.4507 | 1156.4283 |
| 244812 | 1152.9011 | 1152.1362 |
| 248412 | 1153.6783 | 1151.6806 |
| 250008 | 1155.7706 | 1156.8285 |

(full checkpoint list written to `results/night3/night_report_checkpoints_4v3.csv`, 72 rows)

### Run A checkpoint detail

- iteration of minimum held-out (checkpoint) val_loss: 237612 (val_loss=1150.9345)
- loss near iteration 25000: 1190.0517 (nearest checkpoint at iteration 25212)
- loss near iteration 50000: 1179.0335 (nearest checkpoint at iteration 50412)
- loss near iteration 100000: 1168.6564 (nearest checkpoint at iteration 100812)
- loss near iteration 150000: 1165.2208 (nearest checkpoint at iteration 151212)
- loss near iteration 200000: 1163.2382 (nearest checkpoint at iteration 201612)
- loss near iteration 250000: 1155.7706 (nearest checkpoint at iteration 250008)
- relative change of held-out loss over the last 50,000 iterations (checkpoint near 200000 -> checkpoint near 250000, positive = rose): -0.0064 (1163.2382 -> 1155.7706; plateauing by a <1% heuristic)
- discrepancy: rung val_loss at iteration 250,000 (1152.5066) vs checkpoint val_loss at iteration 250008 (1155.7706) = 3.2641 over 8 extra iteration(s)
- training-loss (train_loss_per_iter) std over last 100 iterations: 613.6562 (mean 1212.2987) -- for judging whether the discrepancy above is within iteration-to-iteration noise

### Run B checkpoint detail

- iteration of minimum held-out (checkpoint) val_loss so far: 198012 (val_loss=1150.0934)
- training-loss std over last 100 iterations: 671.5713

## Per-rung / per-checkpoint replicate differences (section 7 instrument-floor input)

Rungs:
- iteration 1000: |A-B| = 3.1564
- iteration 5000: |A-B| = 0.8440
- iteration 25000: |A-B| = 16.0241
- iteration 250000: |A-B| = 0.6069

Common checkpoints (72):
- iteration 0: |A-B| = 0.0118
- iteration 12: |A-B| = 0.1956
- iteration 3612: |A-B| = 0.7538
- iteration 7212: |A-B| = 1.1318
- iteration 10812: |A-B| = 0.5981
- iteration 14412: |A-B| = 0.7133
- iteration 18012: |A-B| = 2.7752
- iteration 21612: |A-B| = 4.5787
- iteration 25212: |A-B| = 13.2332
- iteration 28812: |A-B| = 15.6165
- iteration 32412: |A-B| = 25.5546
- iteration 36012: |A-B| = 14.5309
- iteration 39612: |A-B| = 25.5256
- iteration 43212: |A-B| = 11.9909
- iteration 46812: |A-B| = 24.8694
- iteration 50412: |A-B| = 9.7998
- iteration 54012: |A-B| = 21.5507
- iteration 57612: |A-B| = 39.8394
- iteration 61212: |A-B| = 14.9365
- iteration 64812: |A-B| = 20.5427
- iteration 68412: |A-B| = 6.7395
- iteration 72012: |A-B| = 5.7138
- iteration 75612: |A-B| = 25.6529
- iteration 79212: |A-B| = 2.5082
- iteration 82812: |A-B| = 6.7846
- iteration 86412: |A-B| = 5.2872
- iteration 90012: |A-B| = 3.5204
- iteration 93612: |A-B| = 4.6254
- iteration 97212: |A-B| = 5.3194
- iteration 100812: |A-B| = 2.1308
- iteration 104412: |A-B| = 4.3431
- iteration 108012: |A-B| = 5.5383
- iteration 111612: |A-B| = 2.3121
- iteration 115212: |A-B| = 7.9285
- iteration 118812: |A-B| = 3.9940
- iteration 122412: |A-B| = 9.5471
- iteration 126012: |A-B| = 0.3917
- iteration 129612: |A-B| = 7.7054
- iteration 133212: |A-B| = 3.2956
- iteration 136812: |A-B| = 18.6174
- iteration 140412: |A-B| = 1.9108
- iteration 144012: |A-B| = 1.4129
- iteration 147612: |A-B| = 3.7167
- iteration 151212: |A-B| = 6.2878
- iteration 154812: |A-B| = 11.8979
- iteration 158412: |A-B| = 8.0229
- iteration 162012: |A-B| = 23.4329
- iteration 165612: |A-B| = 2.7462
- iteration 169212: |A-B| = 7.4437
- iteration 172812: |A-B| = 0.3420
- iteration 176412: |A-B| = 5.9228
- iteration 180012: |A-B| = 4.2879
- iteration 183612: |A-B| = 11.5839
- iteration 187212: |A-B| = 2.6852
- iteration 190812: |A-B| = 6.9020
- iteration 194412: |A-B| = 5.3101
- iteration 198012: |A-B| = 2.5977
- iteration 201612: |A-B| = 6.8551
- iteration 205212: |A-B| = 6.8556
- iteration 208812: |A-B| = 2.2172
- iteration 212412: |A-B| = 10.6084
- iteration 216012: |A-B| = 11.5944
- iteration 219612: |A-B| = 7.1886
- iteration 223212: |A-B| = 3.5626
- iteration 226812: |A-B| = 4.2404
- iteration 230412: |A-B| = 0.7664
- iteration 234012: |A-B| = 0.0725
- iteration 237612: |A-B| = 8.2177
- iteration 241212: |A-B| = 2.9776
- iteration 244812: |A-B| = 0.7649
- iteration 248412: |A-B| = 1.9977
- iteration 250008: |A-B| = 1.0578

- max |A-B| across rungs+common checkpoints: 39.8394
- median |A-B| across rungs+common checkpoints: 5.2986

