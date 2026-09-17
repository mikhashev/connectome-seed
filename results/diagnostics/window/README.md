# Window-integral cheap statistic — computed readings

Computes exactly the quantities pre-registered in
`docs/briefs/2026-09-17-window-integral-cheap-statistic.md` v1.1 (§5, including the v1.1
additions from Ark and Zcode's reviewer pass), from the stored run jsons the brief's §2
lists. CPU only, reads only. No GPU used, no write to `connectome-seed-data`, no change to
`docs/preregistration-cheap-vs-expensive.md`.

**Script:** `window_integral.py`, sha256 `9a10dbad7535e32f6446cc3eda28352b9c0739ceb7189fc334c7fd7bc6e8c60c`
(also recorded inside `window_readings.json` as `script_sha256`, computed from the script's
own bytes at run time). **Output:** `window_readings.json` (full floats, every number below
is read from it). Run with
`C:/Users/mikha/AppData/Local/Programs/Python/Python312/python.exe window_integral.py`.

## 0. Two deviations from the brief's §2, found while reading

- **Filenames.** §2 names the full-run files `night1_9991-000.json` etc. On disk in this
  repository they exist only as `*.slim.json` with the same base name (e.g.
  `night1_9991-000.slim.json`; `results/night1/`, `results/night2/`, `results/night3/`,
  `results/night4/`). Read as the same run record — no bare `.json` file with this content
  exists anywhere in the repository. `results/diagnostics/c3/partA/jitter_9991-703.json` (703)
  matches the brief exactly, no `.slim` suffix.
- **`train_loss_per_iter`.** §2 states it "exists for all 8" full runs. On disk it exists
  only for 703 (25,212 entries, index = iteration). The 7 full-run `*.slim.json` files carry
  no per-iteration train loss beyond `train_loss_last1000_9991-*.csv` (the final 1,000
  iterations, ≈249,009–250,008 — nowhere near the 18k–32k window). Option (B) (§4) is
  therefore computed here for **703 only**; see §5 below. This does not touch any (A)/(C)/§5
  quantity, all of which use `checkpoint_metrics` and `rung_metrics`, present in every file as
  the brief describes.

Both are stated here, not silently absorbed into the brief's wording; nothing else in §2's
description of the record was found to differ from what is on disk.

## 1. Per-run table

Checkpoint grid used throughout: 18,012 / 21,612 / 25,212 / 28,812 / 32,412 (703 has only the
first three). Onset = first downward crossing of val_loss = 1,200, by linear interpolation
between the two bracketing points, from `checkpoint_metrics` for the 7 full runs and from
`rung_metrics` (dense) for 703 — this is brief §5(C)'s definition, not yet the calibration of
§2 below.

| run | point @25,000 (hook) | point @250,000 (hook) | ckpt 18012 | ckpt 21612 | ckpt 25212 | ckpt 28812 | ckpt 32412 | onset (level 1200) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| seed 0 (000) | 1191.7375 | 1146.1958 | 1205.9267 | 1199.3854 | 1192.7493 | 1184.2532 | 1175.8663 | 21,273.7 (bracket 18012–21612) |
| seed 1 (001) | 1190.2235 | 1145.3572 | 1204.7626 | 1202.0727 | 1192.4103 | 1182.0623 | 1172.8651 | 22,384.2 (bracket 21612–25212) |
| seed 2 (002b) | 1204.3618 | 1148.8000 | 1206.3075 | 1205.1803 | 1205.9782 | 1200.7650 | 1199.5604 | 31,098.2 (bracket 28812–32412) |
| seed 3 (003) | 1192.5858 | 1152.5066 | 1204.1880 | 1201.7573 | 1190.0517 | 1184.5230 | 1174.2851 | 22,152.4 (bracket 21612–25212) |
| seed 4 (004) | 1208.6099 | 1153.1134 | 1206.9632 | 1206.3360 | 1203.2849 | 1200.1395 | 1199.8397 | 30,487.2 (bracket 28812–32412) |
| seed 5 (005) | 1204.7794 | 1159.1158 | 1206.2544 | 1206.6749 | 1213.5255 | 1200.9585 | 1193.8305 | 29,296.1 (bracket 28812–32412) |
| 0′ (900, replicate) | 1192.0739 | 1158.9237 | 1205.8643 | 1200.0605 | 1192.8249 | 1183.6375 | 1178.3090 | 21,642.1 (bracket 21612–25212) |
| 3′ (903, replicate) | 1187.4011 | 1162.9375 | 1204.2230 | 1201.7641 | 1187.1360 | 1182.3103 | 1173.1151 | 22,046.1 (bracket 21612–25212) |
| 703 (jitter, no 250k) | 1187.8276 | n/a — no 250,000 hook | 1204.2896 | 1202.3969 | 1187.9687 | **missing** | **missing** | 21,428.6 (bracket 21400–21500, dense) |

Note: `seed 5`'s checkpoint at 25,212 (1213.5255) sits above both its neighbours (1206.6749
and 1200.9585) — a single-checkpoint non-monotonic read, consistent with §3's read-noise
residual sd ≈ 1.8–2.2 the brief already flags at the finer 703 grid; it is carried through the
window means as read, not smoothed or excluded.

**Window means, per run** (checkpoint-window mean, §4(A) / §5(v1.1) shifted windows):

| run | A narrow 20k–30k {21612,25212,28812} | A wide 18012–32412 (5pt) | W1 18012–25212 | W2 21612–28812 (= A narrow) | W3 25212–32412 |
|---|---:|---:|---:|---:|---:|
| seed 0 | 1192.1293 | 1191.6362 | 1199.3538 | 1192.1293 | 1184.2896 |
| seed 1 | 1192.1818 | 1190.8346 | 1199.7485 | 1192.1818 | 1182.4459 |
| seed 2 | 1203.9745 | 1203.5583 | 1205.8220 | 1203.9745 | 1202.1012 |
| seed 3 | 1192.1106 | 1190.9610 | 1198.6656 | 1192.1106 | 1182.9533 |
| seed 4 | 1203.2535 | 1203.3127 | 1205.5280 | 1203.2535 | 1201.0880 |
| seed 5 | 1207.0530 | 1204.2488 | 1208.8183 | 1207.0530 | 1202.7715 |
| 0′ | 1192.1743 | 1192.1392 | 1199.5832 | 1192.1743 | 1184.9238 |
| 3′ | 1190.4035 | 1189.7097 | 1197.7077 | 1190.4035 | 1180.8538 |
| 703 | 1195.1828 (2 pts, 28812 missing) | 1198.2184 (3 pts, 28812/32412 missing) | 1198.2184 (3 pts, complete) | 1195.1828 (2 pts, 28812 missing) | 1187.9687 (1 pt only, 28812/32412 missing — **not a mean**) |

**Where each window lies relative to that run's own onset** (brief §4(A), v1.1/Ark: "A is not
interpretable without C — read together"), using each run's onset estimate from the table
above and the two §4(A) windows:

| run | onset | A narrow 20k–30k (21612–28812) | A wide 18012–32412 |
|---|---:|---|---|
| seed 0 | 21,273.7 | onset before window (window post-onset) | straddles onset |
| seed 1 | 22,384.2 | straddles onset | straddles onset |
| seed 2 | 31,098.2 | onset after window (window pre-onset) | straddles onset |
| seed 3 | 22,152.4 | straddles onset | straddles onset |
| seed 4 | 30,487.2 | onset after window (window pre-onset) | straddles onset |
| seed 5 | 29,296.1 | onset after window (window pre-onset) | straddles onset |
| 0′ | 21,642.1 | straddles onset (barely — window starts 21,612, 30 iters before onset) | straddles onset |
| 3′ | 22,046.1 | straddles onset | straddles onset |
| 703 | 21,428.6 (dense) | onset before window (703's narrower 21612–25212 window is post-onset) | onset before window (703's narrower 18012–25212 window straddles onset since it starts at 18,012) |

Read plainly: A narrow (20k–30k) is **not the same kind of window across runs** — for three
of the six individuals (seeds 2, 4, 5) the entire window sits *before* that run's own onset
(still on the plateau), while for the other three (seeds 0, 1, 3) it straddles the onset. A
wide (18012–32412) straddles the onset for every run. This is exactly the confound §1 of the
brief names (a point, and by extension a narrow window, "ranks runs partly by phase of
descent") — stated here per-run, not resolved.

## 2. Within-seed spread vs individual (n=6) spread, with the named 0.5x factor

Sample standard deviation (n−1 denominator; n=2 reduces to |x1−x2|/√2). Two ways for the
seed-3 set wherever 703's window is incomplete, per §4(A)'s "report both ways" rule: the
**trio with 703 included** (703's own narrower mean used) and the **pair with 703 excluded**
(003, 903 only, matching window). Condition (i) of the promotion criterion, v1.1: "reduced"
means sd(window) ≤ 0.5 × sd(point @25,000), checked separately for the seed-0 pair and for
whichever seed-3 set is reported.

| statistic | seed-0 pair sd (000,900) | ratio to point, seed-0 | clears 0.5x? | seed-3 trio sd (003,903,703-incl) | ratio, seed-3 trio | clears 0.5x? | seed-3 pair sd (003,903, 703 excl.) | ratio, seed-3 pair | clears 0.5x? | individuals n=6 sd |
|---|---:|---:|:--:|---:|---:|:--:|---:|---:|:--:|---:|
| point @25,000 | 0.2379 | 1.000 | — (reference) | 2.8782 | 1.000 | — (reference) | 3.6662 | 1.000 | — (reference) | 8.0614 |
| A narrow 20k–30k | 0.0318 | 0.1338 | **yes** | 2.4219 | 0.8415 | **no** | 1.2072 | 0.3293 | **yes** | 7.0290 |
| A wide 18012–32412 | 0.3557 | 1.4952 | no | 4.5941 | 1.5962 | no | 0.8848 | 0.2413 | **yes** | 6.8931 |
| W1 18012–25212 | 0.1622 | 0.6819 | no | 0.4793 | 0.1665 | **yes** | 0.6774 | 0.1848 | **yes** | 4.2628 |
| W2 21612–28812 (=A narrow) | 0.0318 | 0.1338 | **yes** | 2.4219 | 0.8415 | no | 1.2072 | 0.3293 | **yes** | 7.0290 |
| W3 25212–32412 | 0.4485 | 1.8849 | no | 3.6557 | 1.2701 | no | 1.4845 | 0.4049 | **yes** | 10.3054 |

Direction, stated plainly and descriptively (n=2/n=3, no test): every window's individual
(n=6) sd is smaller than the point's individual sd, so window means do compress the
between-individual spread somewhat at this N. Whether the *within-seed* spread compresses
the same way is not uniform: it depends on which seed-3 set is used. With 703 excluded (the
seed-3 **pair**, matching windows only) every window statistic clears the 0.5x factor for
both seed sets. With 703 **included** (the seed-3 **trio**, 703's narrower mean substituted
in), only W1 clears 0.5x for the seed-3 side; A narrow/W2, A wide and W3 do not, because
703's narrower window (2 or fewer matching points) sits further from 003/903 than the
matching-window pair does. This is a property of comparing a 3-point mean (003, 903) against
a narrower 1–2-point mean (703) at the same nominal window, stated as such — not a claim
about the seed-3 individual's own spread.

## 3. Rank stability across shifted windows (n=6 individuals, seeds 0–5)

Windows: **W1 = {18,012, 21,612, 25,212}**, **W2 = {21,612, 25,212, 28,812}** (identical set
to §4(A)'s narrow 20k–30k window), **W3 = {25,212, 28,812, 32,412}**.

Ranks (1 = lowest loss = "best"), by seed 0..5 in order:

| window | seed0 | seed1 | seed2 | seed3 | seed4 | seed5 |
|---|--:|--:|--:|--:|--:|--:|
| W1 | 2 | 3 | 5 | 1 | 4 | 6 |
| W2 | 2 | 3 | 5 | 1 | 4 | 6 |
| W3 | 3 | 1 | 5 | 2 | 4 | 6 |

Pairwise Spearman ρ (descriptive, n=6, midranks — same construction as
`docs/prereg-scripts/rho_ci.py`):

- W1 vs W2: **ρ = 1.000**
- W1 vs W3: **ρ = 0.8286**
- W2 vs W3: **ρ = 0.8286**

**No critical value applies to these numbers** (brief §5, v1.1/Zcode): the pre-registration's
table gives the critical ρ at n = 6 as **0.829**. W1-vs-W2 (1.000) sits above it; W1-vs-W3
and W2-vs-W3 (0.8286 each) sit a hair *below* 0.829 — closer to it than to any other value in
this readout. Per the brief's v1.1 language, this reads as "did not visibly fail" for
W1-vs-W2 and as indistinguishable-from-the-resolution-limit for the other two pairs, not as a
pass/fail statement; at n = 6 nothing below 0.829 is resolvable from chance.

## 4. Spearman ρ with the 250,000 hook (n=6 individuals, descriptive only)

| statistic | ρ with 250,000 hook |
|---|---:|
| point @25,000 (hook) | 0.8857 |
| A narrow 20k–30k | 0.4857 |
| A wide 18012–32412 | 0.7143 |
| W1 18012–25212 | 0.4857 |
| W2 21612–28812 (=A narrow) | 0.4857 |
| W3 25212–32412 | 0.7143 |

Critical ρ at n = 6 is **0.829** (same table, same caveat as §3). Read plainly: the point
statistic's ρ (0.8857) is above that value; every window statistic's ρ (0.4857–0.7143) is
below it. **This is not the registered (b) test** (that test is defined at C3 with its own N
rule and Holm correction, and is not re-run here at N=6); no p-value or reject/accept label
attaches to any of these six numbers, stated per the brief's do-not (§6).

## 5. Run 703 onset calibration (§5, v1.1/Ark) and the reliability mark

- **Dense-read onset** (703's `rung_metrics`, 139 points, iterations 1,000–26,000, level
  1,200): **iteration 21,428.56**, bracketed between the dense reads at 21,400 (val_loss
  above 1,200) and 21,500 (below).
- **Checkpoint-grid-like subsample onset** (703's own `checkpoint_metrics`, the same 9-point
  grid the 7 full runs are read on: 0, 12, 3612, 7212, 10812, 14412, 18012, 21612, 25212):
  **iteration 22,210.05**, bracketed between 21,612 and 25,212.
- **Difference (subsample − dense): 781.49 iterations.**
- **One checkpoint interval = 3,600 iterations.** 781.49 < 3,600, so by the brief's v1.1 rule
  the two estimates do **not** disagree by more than one checkpoint interval.
- **Mark: the §4(C) onset estimate on the seven full runs is RELIABLE** (not marked
  unreliable) by this calibration.

## 6. Option (B): train-loss window mean, 703 only (§4(B), §0 deviation above)

`train_loss_per_iter` (25,212 entries, index = iteration) exists only for 703 among the 8
runs; computed here for 703 only, reported but not compared to (A)/point on the same axis
(brief §4(B)'s own restriction — train loss on augmented batches, sd order 650–680, is not
the held-out metric):

| window | mean | sd | iterations used |
|---|---:|---:|---:|
| A narrow 20k–30k | 1285.9654 | 655.5057 | 21612–25211 (3,600 iters; window's 28,812 end clipped to 703's last stored iteration, 25,211) |
| A wide 18012–32412 | 1298.6442 | 651.7875 | 18012–25211 (7,200 iters; clipped, same reason) |
| W1 18012–25212 | 1298.6442 | 651.7875 | 18012–25211 (7,200 iters; requested end 25,212 clipped to 25,211, the last stored index) |
| W2 21612–28812 (=A narrow) | 1285.9654 | 655.5057 | 21612–25211 (3,600 iters; clipped) |
| W3 25212–32412 | n/a | n/a | window (25,212–32,412) entirely beyond 703's stored range (0–25,211) |

For the 7 full runs, (B) is **not computed** — no per-iteration train loss exists for them in
this iteration range (§0).

## 7. Promotion criterion (§5, fixed by the brief; applied here, not re-derived)

Both conditions must hold (i AND ii); condition (i) is evaluated once with 703 excluded (the
matching-window seed-3 pair) and once with 703 included (the seed-3 trio, 703's narrower
mean), per §4(A)'s "report both ways" rule; condition (ii) does not involve 703 (it is n=6
individuals only).

| window | (i) both seed sets clear 0.5x, 703 excluded (pair) | (i) both seed sets clear 0.5x, 703 included (trio) | (ii) ρ(window) ≥ ρ(point) = 0.8857 | ρ(window) |
|---|:--:|:--:|:--:|---:|
| A narrow 20k–30k | **yes** | no (seed-3 trio 0.8415 > 0.5) | no | 0.4857 |
| A wide 18012–32412 | **yes** | no (seed-0 1.4952 and seed-3 trio 1.5962 both > 0.5) | no | 0.7143 |
| W1 18012–25212 | **yes** | no (seed-0 0.6819 > 0.5) | no | 0.4857 |
| W2 21612–28812 | **yes** | no (seed-3 trio 0.8415 > 0.5) | no | 0.4857 |
| W3 25212–32412 | **yes** | no (seed-0 1.8849, seed-3 trio 1.2701, both > 0.5) | no | 0.7143 |

Per the brief's own rule ("either condition failing … means not a candidate as proposed"):
**no window statistic is a candidate for the next registration on this record** — condition
(ii) fails for every window regardless of how 703 is handled in (i), because every window's
ρ with the 250,000 hook (0.4857–0.7143) is below the point value's ρ (0.8857). This is the
brief's own pre-registered criterion applied to the numbers above; no verdict beyond it is
drawn here.

## 8. What this does not say

No number above is a test, a p-value, or a reject/accept decision (brief §6). The ρ values in
§3 and §4 are descriptive at n=6, below the table's own critical value of 0.829 in every
case except the point statistic's ρ with the 250,000 hook and the W1-vs-W2 shift comparison.
§7's "not a candidate as proposed" is the brief's own fixed criterion mechanically applied,
not a new judgment about the window statistic's worth. The onset-aligned window named in the
brief's §7 is not built here — it was conditional on §5's reliability mark, which came back
reliable, so it remains available as the next step, not run in this pass.
