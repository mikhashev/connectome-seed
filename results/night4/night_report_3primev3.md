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
| A | 0.0642 | 0.0447 | 0.0612 | 9723.2724 | 4596.6236 | 250008 |
| B | 0.0644 | 0.0454 | 0.0607 | 9747.1319 | 4606.7709 | 250008 |

(Note: precomputed `iter_wall_median_all_s` / `iter_wall_median_1000_2000_s` in the json, when present, cover different windows than this table; this table's medians/sums are computed here from `iter_wall_s` over the windows stated in the header.)
- A json field iter_wall_median_all_s: 0.0612
- A json field iter_wall_median_1000_2000_s: 0.0660
- B json field iter_wall_median_all_s: 0.0607
- B json field iter_wall_median_1000_2000_s: 0.0671

## Rung table

| iteration | val_loss A | val_loss B | B - A | relative (B-A)/A |
|---|---|---|---|---|
| 1000 | 1210.4139 | 1210.4302 | 0.0163 | 0.0000 |
| 5000 | 1205.5457 | 1205.5182 | -0.0276 | -0.0000 |
| 25000 | 1192.5858 | 1187.4011 | -5.1847 | -0.0043 |
| 250000 | 1152.5066 | 1162.9375 | 10.4309 | 0.0091 |

## Replicate difference at iteration 250,000 (pre-registration section 7 tolerance: < 1%)

- |A-B|/A at 250,000 = 0.9051%  -> PASS (< 1%)

## Checkpoint trajectory

Compact view (every 5th checkpoint by A's index; full 72-row list -> `results/night4/night_report_checkpoints_3primev3.csv`):

| iteration | val_loss A | val_loss B |
|---|---|---|
| 0 | 1212.5497 | 1212.5497 |
| 12 | 1211.7933 | 1211.7932 |
| 3612 | 1206.8331 | 1206.8111 |
| 7212 | 1207.4437 | 1207.4158 |
| 10812 | 1206.1021 | 1206.1364 |
| 14412 | 1206.2946 | 1206.4309 |
| 18012 | 1204.1880 | 1204.2230 |
| 21612 | 1201.7573 | 1201.7641 |
| 25212 | 1190.0517 | 1187.1360 |
| 28812 | 1184.5230 | 1182.3103 |
| 32412 | 1174.2851 | 1173.1151 |
| 36012 | 1179.1252 | 1180.7562 |
| 39612 | 1174.0103 | 1177.6193 |
| 43212 | 1179.8168 | 1188.7442 |
| 46812 | 1168.8909 | 1177.9724 |
| 50412 | 1179.0335 | 1182.3089 |
| 54012 | 1171.3346 | 1178.8657 |
| 57612 | 1164.6277 | 1170.8438 |
| 61212 | 1174.0634 | 1172.7128 |
| 64812 | 1165.9828 | 1171.4413 |
| 68412 | 1174.3908 | 1173.6945 |
| 72012 | 1178.1888 | 1174.2891 |
| 75612 | 1166.0802 | 1172.0935 |
| 79212 | 1174.6413 | 1186.6132 |
| 82812 | 1164.9092 | 1173.6684 |
| 86412 | 1169.4652 | 1167.4142 |
| 90012 | 1171.1677 | 1174.8151 |
| 93612 | 1175.2162 | 1178.7145 |
| 97212 | 1173.9763 | 1174.9573 |
| 100812 | 1168.6564 | 1174.2219 |
| 104412 | 1172.8285 | 1179.2206 |
| 108012 | 1163.5787 | 1166.1420 |
| 111612 | 1161.7089 | 1169.4737 |
| 115212 | 1170.3667 | 1177.8473 |
| 118812 | 1174.6678 | 1191.0984 |
| 122412 | 1170.5868 | 1177.2481 |
| 126012 | 1167.1255 | 1172.0775 |
| 129612 | 1167.4171 | 1169.4905 |
| 133212 | 1168.2857 | 1170.9121 |
| 136812 | 1176.3770 | 1171.7410 |
| 140412 | 1163.0901 | 1171.6224 |
| 144012 | 1163.1483 | 1166.6719 |
| 147612 | 1161.3737 | 1169.2592 |
| 151212 | 1165.2208 | 1176.7531 |
| 154812 | 1165.6917 | 1173.4061 |
| 158412 | 1167.5395 | 1170.5529 |
| 162012 | 1181.6246 | 1178.0680 |
| 165612 | 1166.1481 | 1177.2763 |
| 169212 | 1171.6817 | 1171.5277 |
| 172812 | 1166.0327 | 1169.5336 |
| 176412 | 1158.8479 | 1164.9236 |
| 180012 | 1166.3808 | 1168.1160 |
| 183612 | 1169.6822 | 1170.1282 |
| 187212 | 1161.4556 | 1165.8262 |
| 190812 | 1162.5909 | 1167.5396 |
| 194412 | 1161.2928 | 1169.7524 |
| 198012 | 1152.6912 | 1165.1895 |
| 201612 | 1163.2382 | 1171.1885 |
| 205212 | 1162.3037 | 1170.4310 |
| 208812 | 1158.1978 | 1165.5687 |
| 212412 | 1160.7131 | 1164.9207 |
| 216012 | 1153.3346 | 1162.0309 |
| 219612 | 1157.4240 | 1163.0354 |
| 223212 | 1152.8706 | 1163.0894 |
| 226812 | 1155.5818 | 1166.5121 |
| 230412 | 1155.2349 | 1165.8363 |
| 234012 | 1156.2054 | 1164.2868 |
| 237612 | 1150.9345 | 1163.1084 |
| 241212 | 1153.4507 | 1165.1503 |
| 244812 | 1152.9011 | 1163.0639 |
| 248412 | 1153.6783 | 1161.6192 |
| 250008 | 1155.7706 | 1163.3766 |

(full checkpoint list written to `results/night4/night_report_checkpoints_3primev3.csv`, 72 rows)

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

- iteration of minimum held-out (checkpoint) val_loss so far: 248412 (val_loss=1161.6192)
- training-loss std over last 100 iterations: 613.9042

## Per-rung / per-checkpoint replicate differences (section 7 instrument-floor input)

Rungs:
- iteration 1000: |A-B| = 0.0163
- iteration 5000: |A-B| = 0.0276
- iteration 25000: |A-B| = 5.1847
- iteration 250000: |A-B| = 10.4309

Common checkpoints (72):
- iteration 0: |A-B| = 0.0000
- iteration 12: |A-B| = 0.0002
- iteration 3612: |A-B| = 0.0220
- iteration 7212: |A-B| = 0.0279
- iteration 10812: |A-B| = 0.0342
- iteration 14412: |A-B| = 0.1363
- iteration 18012: |A-B| = 0.0351
- iteration 21612: |A-B| = 0.0068
- iteration 25212: |A-B| = 2.9157
- iteration 28812: |A-B| = 2.2127
- iteration 32412: |A-B| = 1.1701
- iteration 36012: |A-B| = 1.6310
- iteration 39612: |A-B| = 3.6090
- iteration 43212: |A-B| = 8.9273
- iteration 46812: |A-B| = 9.0815
- iteration 50412: |A-B| = 3.2754
- iteration 54012: |A-B| = 7.5311
- iteration 57612: |A-B| = 6.2162
- iteration 61212: |A-B| = 1.3506
- iteration 64812: |A-B| = 5.4585
- iteration 68412: |A-B| = 0.6963
- iteration 72012: |A-B| = 3.8997
- iteration 75612: |A-B| = 6.0133
- iteration 79212: |A-B| = 11.9719
- iteration 82812: |A-B| = 8.7592
- iteration 86412: |A-B| = 2.0509
- iteration 90012: |A-B| = 3.6474
- iteration 93612: |A-B| = 3.4983
- iteration 97212: |A-B| = 0.9811
- iteration 100812: |A-B| = 5.5655
- iteration 104412: |A-B| = 6.3920
- iteration 108012: |A-B| = 2.5632
- iteration 111612: |A-B| = 7.7647
- iteration 115212: |A-B| = 7.4806
- iteration 118812: |A-B| = 16.4306
- iteration 122412: |A-B| = 6.6613
- iteration 126012: |A-B| = 4.9519
- iteration 129612: |A-B| = 2.0734
- iteration 133212: |A-B| = 2.6264
- iteration 136812: |A-B| = 4.6361
- iteration 140412: |A-B| = 8.5323
- iteration 144012: |A-B| = 3.5236
- iteration 147612: |A-B| = 7.8855
- iteration 151212: |A-B| = 11.5324
- iteration 154812: |A-B| = 7.7144
- iteration 158412: |A-B| = 3.0134
- iteration 162012: |A-B| = 3.5566
- iteration 165612: |A-B| = 11.1282
- iteration 169212: |A-B| = 0.1540
- iteration 172812: |A-B| = 3.5009
- iteration 176412: |A-B| = 6.0756
- iteration 180012: |A-B| = 1.7352
- iteration 183612: |A-B| = 0.4459
- iteration 187212: |A-B| = 4.3706
- iteration 190812: |A-B| = 4.9487
- iteration 194412: |A-B| = 8.4596
- iteration 198012: |A-B| = 12.4983
- iteration 201612: |A-B| = 7.9503
- iteration 205212: |A-B| = 8.1273
- iteration 208812: |A-B| = 7.3709
- iteration 212412: |A-B| = 4.2075
- iteration 216012: |A-B| = 8.6962
- iteration 219612: |A-B| = 5.6113
- iteration 223212: |A-B| = 10.2188
- iteration 226812: |A-B| = 10.9303
- iteration 230412: |A-B| = 10.6014
- iteration 234012: |A-B| = 8.0814
- iteration 237612: |A-B| = 12.1739
- iteration 241212: |A-B| = 11.6997
- iteration 244812: |A-B| = 10.1628
- iteration 248412: |A-B| = 7.9409
- iteration 250008: |A-B| = 7.6059

- max |A-B| across rungs+common checkpoints: 16.4306
- median |A-B| across rungs+common checkpoints: 5.0683

