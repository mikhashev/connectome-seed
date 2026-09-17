# C3: trajectory jitter at 25,000 and the evaluator floor by path

**Status: PREVIEW DIAGNOSTIC -- NOT A TEST.** Protocol:
`docs/briefs/2026-09-17-c3-jitter-and-evaluator-floor.md` **v1.2** (commit `97b48bb`), with its patch
`docs/briefs/2026-09-17-c3-run_individual.patch`. Launch word: Mike in the DPC Research chat,
2026-09-17 06:16:45Z («@CC_windows запускай замер C3»). Reviewer pass: Ark 06:31:27Z, Zcode 06:41:05Z.
**Run by:** CC's subagent (Opus), 2026-09-17 06:47-07:31Z. Nothing here is interpreted beyond the
brief's wording. All numbers are the `repr` strings from the files named; nothing is rounded except
where this README says "≈".

No stop condition fired. Order run: machine state → Part B (P1, P2, P3) → patch + commit → A0 → A1 →
B′ → readings → machine state. A2 was not run.

## 1. Files

| file | what |
|---|---|
| `c3_evaluator_floor.py` | Part B / B′ driver (E1/E2/E3 via D, ABL, RB; imports as `ablation_night3.py:30-53`) |
| `c3_jitter_reading.py` | readings (a)…(h), CPU only; written and hashed before A1 launched |
| `partB/c3B_proc{1,2,3}.json` | one file per process: every call's 16-item mean, per-item vectors (E2/E3), invariants, P0 |
| `partB/c3B_floor.json`, `partB/c3B_means.csv` | within/cross-process floors and path differences over the three processes |
| `partB/c3Bprime_proc1.json` | B′: run 703, checkpoints 7 and 8, P1 only |
| `partA/SHA256.txt` | hashes recorded at 06:59:15Z, before the A1 launch |
| `partA/jitter_9991-703.{json,log,progress.log}` | run 703 as written by `run_individual.py` |
| `A0smoke/` | copy of the A0 outputs (the run wrote them to the scratchpad, as the brief says) |
| `readings.json` | readings (a) (a′) (b) (c) (d) (e) (f) (g) (h), controls, B′ summary |
| `machine_state.json` | 5 records: start, after B, before A1, after A1/before B′, end |
| `listings/` | run-dir listings (`find 9991 [9983] -printf "%p %s %T@"`) before/after each part, and diffs |
| `logs/` | stdout/stderr of every invocation; `argv_check.txt` (§4 byte-identity check) |

sha256 of the scripts: `c3_evaluator_floor.py` `d402eb4140ead741a9c3fcf603647dbfd210ff7facd034b0bbe943ea7f57e531`;
`c3_jitter_reading.py` `25b9050319fc78ae4cc8894c31fc8753c07b6f5edc6eccc5c90e91f8985cc705`. Imported,
unchanged: `diag1_eval_paths.py`, `ablation.py`, `rowB.py` — hashes inside every Part B json.
Hashes of every output file: §9.

## 2. Part B — evaluator floor (runs 003, 903; checkpoints 0 / 25,212 / 250,008)

Three processes, one after another (P1 06:51:07-06:52:04Z, P2 06:52:13-06:53:03Z, P3 06:53:05-06:53:55Z),
netdir roots `<scratchpad>/c3_netdir_proc{1,2,3}`. Each: build (36.5 / 31.4 / 31.2 s), then per
(run, checkpoint) five rounds of E1, E2, E3 = 90 calls, call wall 0.202–0.337 s.
**Gates:** no crash; no NaN/inf; all seven invariants True on all 270 calls; P0 (P1, mean of five E2 −
stored) ≤ 1e-4 in all six cells; run-dir listing unchanged (diff 0 bytes, 878 lines, both
`af794420…b2e3ea`).

Within = max over 30 pairs (10 per process); cross = max over 75 pairs; |Δ| on the 16-item mean;
per-item max |Δ| (ulps of float32 at the largest per-item value) for E2/E3.

| run | iter | E1 within / cross | E2 within / cross (per-item, ulps) | E3 within / cross (per-item, ulps) |
|---|---|---|---|---|
| 003 | 0 | 9.5367431640625e-07 / 9.5367431640625e-07 | 9.5367431640625e-07 / same (1.52587890625e-05, 0.03125) | 0.0 / 0.0 (0.0) |
| 003 | 25212 | 4.1484832763671875e-05 / 4.6253204345703125e-05 | 3.9577484130859375e-05 / 4.100799560546875e-05 (0.00048828125, 1.0) | 4.0531158447265625e-05 / 3.7670135498046875e-05 (0.00048828125, 1.0) |
| 003 | 250008 | 3.910064697265625e-05 / 4.3392181396484375e-05 | 8.106231689453125e-05 / 6.628036499023438e-05 (0.00048828125, 1.0) | 8.106231689453125e-05 / 8.678436279296875e-05 (0.00048828125, 1.0) |
| 903 | 0 | 9.5367431640625e-07 / 9.5367431640625e-07 | 9.5367431640625e-07 / same (1.52587890625e-05, 0.03125) | 0.0 / 0.0 (0.0) |
| 903 | 25212 | 4.100799560546875e-05 / 4.76837158203125e-05 | 3.8623809814453125e-05 / 3.9577484130859375e-05 (0.00048828125, 1.0) | 4.57763671875e-05 / 4.8160552978515625e-05 (0.00048828125, 1.0) |
| 903 | 250008 | 0.00013685226440429688 / 0.000202178955078125 | 0.0001087188720703125 / 0.00011730194091796875 (0.0009765625, 2.0) | 0.00011587142944335938 / 0.00012922286987304688 (0.0009765625, 2.0) |

Same-state path differences on the 16-item mean, 75 call pairs (25 per process), max |·|:

| run | iter | E1−E2 | E1−E3 | E2−E3 (per-item max) |
|---|---|---|---|---|
| 003 | 0 | 9.5367431640625e-07 | 9.5367431640625e-07 | 9.5367431640625e-07 (1.52587890625e-05) |
| 003 | 25212 | 4.7206878662109375e-05 | 4.2438507080078125e-05 | 4.38690185546875e-05 (0.00048828125) |
| 003 | 250008 | 6.389617919921875e-05 | 7.534027099609375e-05 | 6.914138793945312e-05 (0.000732421875) |
| 903 | 0 | 9.5367431640625e-07 | 9.5367431640625e-07 | 9.5367431640625e-07 (1.52587890625e-05) |
| 903 | 25212 | 4.38690185546875e-05 | 4.9591064453125e-05 | 4.8160552978515625e-05 (0.00048828125) |
| 903 | 250008 | 0.00014352798461914062 | 0.00014495849609375 | 0.00011730194091796875 (0.00146484375) |

P0 (mean of five E2 − stored), P1 / P2 / P3: 003@0 `1.907349087559851e-07` / `0.0` / `3.814698175119702e-07`;
003@25212 `-2.4890899567253655e-05` / `-1.020431523102161e-05` / `-2.069473271149036e-05`;
003@250008 `-1.9073486328125e-05` / `6.00814814788464e-06` / `3.337860107421875e-06`;
903@0 `0.0` / `0.0` / `1.907349087559851e-07`; 903@25212 `1.8978118987433845e-05` /
`2.2029876618034905e-05` / `2.346038809264428e-05`; 903@250008 `2.7751922516472405e-05` /
`-1.688003544586536e-05` / `6.866455123599735e-06`. Largest single-call |E2 − stored| over all
processes: `6.961822509765625e-05` (903@250008, P1); single-call |E1 − stored|: `0.00014352798461914062`
(903@250008, P2).

Recorded, no reading attached: at iteration 0 the calls are not all bitwise equal to the stored
value in this session — single E1 and E2 values of `1212.5497364997864` (one float64 step of the
mean, 9.5367431640625e-07) occur in P1 (E2) and P3 (E1, E2); E3 was bitwise constant at iteration 0
in all three processes. §1 of the brief records "0.0 at iteration 0" for five `per_item_eval` calls
in the night-2 diagnostics.

## 3. Patch, byte-identity, commit

`git apply --check` then `git apply` of the brief's patch; `git diff --numstat` → `20	0	tools/night/run_individual.py`.
parse_args on night 4's argv (`rep_9991-903.slim.json`): original (HEAD `97b48bb`, sha256
`5ccd38b8…eb55a4a`) 12 keys, patched 13; all 12 common keys equal; extra `stop_after_iter: None`
(`logs/argv_check.txt`). Refusal path (`--rungs 24 --stop-after-iter 25`): printed the refusal, rc 2,
no out-dir created. Patched sha256 `4aafb2c481551e2b51a7ca65f02a04fd691c81d80a14a591b72688b8534e7d5d`,
identical in the repo and in `FP/night/run_individual.py` after copy. Commit
**`a8a800813448ec2979a717a380a58955a17fea6a`** (that file alone), pushed `97b48bb..a8a8008` to
origin/master before any training.

## 4. A0 smoke

`--seed 3 --id 9983/000 --tag c3smoke --n-iters 250000 --rungs 24 --stop-after-iter 24 --no-determinism
--out-dir <scratchpad>/c3smoke`, 06:56:18–06:56:31Z, rc 0. As expected: `exit` "ok",
`stopped_after_iter` 24, `final_iteration` 23, one rung (24, `1211.4668221473694`, seven checks True,
`solver_iteration_at_hook` 23), checkpoints at 0 (`1212.549735546112`) and 12
(`1211.7933382987976`), `errors` []. Listing: 0 lines removed/changed, 35 added, all under `9983`.

## 5. A1 — run 703

Command exactly brief §3 A1 with the 139 rungs of §3 (the "65" in the A1 line of the brief is the
stale v1 count; the list used is the v1.2 list), on the committed file. Launched 06:59:28Z; json
`started_utc` 06:59:29Z, `finished_utc` 07:28:45Z. **Wall time: `total_train_wall_s` 1749.582802799996
s (29 min 10 s)**, `solver_init_s` 4.53; the 25,000 hook at `wall_s_since_start` 1670.910881799995
(003: 1647.5, 903: 1681.0). Hook wall 0.219–0.359 s. Median iteration wall 0.0643995 s.

Controls: pre-condition c(0) `1212.549735546112` == registered value, bitwise (read from the json at
the `CHECKPOINT 0` line, 06:59:36Z). `exit` "ok", `stopped_after_iter` 26000, `final_iteration` 25999,
139/139 rungs recorded, all seven invariants True at every rung, `errors` [],
`nondeterministic_ops` {}; checkpoints at 0, 12, 3612, 7212, 10812, 14412, 18012, 21612, 25212;
`schedule.stop_iter` 250000; `lr_net_at_iter` 25000 = 4.5e-05. argv vs `night3_9991-003`: differs in
`--id`, `--tag`, `--rungs`, `--out-dir`, `--progress-file` (absent), `--stop-after-iter` — the expected
set, nothing else. `connectome_sha256` and `versions` equal to 003 and 903. Listing: the only
pre-existing entry that changed is the directory `9991` itself (mtime `1789604901.54` → `1789628371.40`,
the parent of the new `703`); no pre-existing file changed; 41 entries added, all under `9991/703`.

## 6. B′ — run 703, checkpoints 7 (21,612) and 8 (25,212), P1 only

07:29:38–07:30:17Z, gates as Part B, all passed; listing unchanged (diff 0). P0: 21612
`2.002715973503655e-06`, 25212 `1.077651972991589e-05`. Within-process max |Δ| E1/E2/E3: 21612
`6.198883056640625e-06` / `1.621246337890625e-05` / `1.1920928955078125e-05`; 25212
`2.9087066650390625e-05` / `1.239776611328125e-05` / `1.33514404296875e-05`. Path differences max |·|
E1−E2 / E1−E3 / E2−E3: 21612 `1.239776611328125e-05` / `1.52587890625e-05` / `1.9073486328125e-05`;
25212 `3.6716461181640625e-05` / `4.673004150390625e-05` / `2.2411346435546875e-05`. In-process v −
offline mean of five E1: 21612 `-2.384185791015625e-06`, 25212 `-1.1634826705630985e-05`.

## 7. Readings (brief §5), from `readings.json`

- **(a) Amplitude**, 61 reads 20,000…26,000 step 100: slope `-0.0027439063620403265`/iteration;
  residual sd (ddof 2) `1.8435756851405782`; max |residual| `4.7518281515533545` at k = 25,100.
  ÷ 0.3365: `-0.008154253676197107`, `5.478679599229058`, `14.121331802535972`.
  ÷ 56.7791: `-4.83259925226065e-05`, `0.03246926571820579`, `0.08368974061852609`.
- **(b) Band** over 24,500…25,500 (11 reads): B = [`1185.3134717941284`, `1194.4994478225708`].
  Night 3 v(25,000) `1192.585838317871`: inside B yes, nearer edge `1.913609504699707`, (value − fit at
  25,000 `1190.3396905818859`) ÷ residual sd `1.2183648081765392`. Night 4 `1187.4011011123657`: inside
  yes, `2.0876293182373047`, `-1.5939619366893865`.
- **(c) Autocorrelation**, lag-1 Pearson of the (a) residuals, 60 pairs: `0.2095491356032063`.
- **(d) Same state, in process:** c(21,612) − v(21,612) = `1.430511474609375e-06`; c(25,212) −
  v(25,212) = `-1.1920928955078125e-05`. c(25,212) − v(25,000) = `0.14109230041503906` = movement
  v(25,212) − v(25,000) `0.14110422134399414` + path `-1.1920928955078125e-05`.
- **(a′) Fine window**, 81 reads 24,000…26,000 step 25: slope `-0.003280290585115593`; residual sd
  `2.199216379401043`; max |residual| `8.012769758877084` at 25,650 (÷ 0.3365: `-0.009748263254429696`,
  `6.535561305798047`, `23.81209438002105`; ÷ 56.7791: `-5.777285277708863e-05`, `0.038732850281195774`,
  `0.1411218169868329`). |v(k+25) − v(k)| over 80 pairs: median `1.9052255153656006`, max
  `8.780489921569824` (25,625→25,650); beside 3.2640862464904785 (003) and 0.4390707015991211 (903).
- **(f) Third throw of seed 3.** Hook at 25,000: (3′,3) `-5.184737205505371`, (703,3)
  `-4.7582573890686035`, (703,3′) `0.4264798164367676`. Checkpoint 25,212: (3′,3) `-2.9156599044799805`,
  (703,3) `-2.0830202102661133`, (703,3′) `0.8326396942138672`.
- **(g) Lag scaling**, residuals of the (a′) line: median |Δresidual| at lag 25 / 50 / 75 / 100 =
  `1.9862185473580212` / `1.6540263185227104` / `2.0508139596399815` / `1.8792339343472122`; slope of
  log median |Δ| on log lag `-0.004133398975094453` (brief: ≈ 0.5 random walk; ≈ 0 mean reversion);
  extrapolated at lag 8 `1.9014757602442094`, beside 3.26 / 0.44.
- **(h) Transient.** v703(25,000) `1187.8275809288025`: − 003 `-4.7582573890686035`, − 903
  `0.4264798164367676`; below the band of seeds 2/4/5 [`1204.361764907837`, `1208.6099381446838`].
  1,000-step grid of 703: 1,000 `1210.443347454071`; 5,000 `1205.5127868652344`; 6,000–19,000 between
  `1204.0650634765625` and `1207.9424142837524`; 20,000 `1201.8268303871155`; 21,000
  `1201.2669897079468`; 22,000 `1198.4467635154724`; 23,000 `1197.995331287384`; 24,000
  `1197.4838695526123`; 25,000 `1187.8275809288025`; 26,000 `1184.6153693199158` (full list in json).
- **(e) Recorded only.** v(1,000): 703 `1210.443347454071`, 003 `1210.4138760566711`, 903
  `1210.4301586151123`. v(5,000): `1205.5127868652344` / `1205.5457439422607` / `1205.5181617736816`.
  c(12): 703 `1211.793152332306`, 003 `1211.7933373451233`, 903 `1211.7931632995605` — **not bitwise
  equal to either**; c(0) equal in all three. c at 3,612…25,212 for all three runs in the json.

Operationalisations fixed in the reading script's docstring before the data existed: (a) divides slope,
sd and max |residual| each by both constants as written; (b) nearer edge = min distance to either
edge; (g) "local linear trend" = the (a′) OLS line, lags as index lags 1–4, slope = OLS of log median
on log lag over the four lags; (h) band = [min, max] of the recorded 25,000 hooks of 002, 004, 005.
Recomputation check: (a) slope, sd and (c) re-derived with `np.polyfit` from the primary json — agree
within 2e-15 relative (slope `-0.002743906362040359`, sd `1.843575685140577`, lag-1 `0.20954913560320787`).

## 8. Machine state, environment, deviations

Machine state (`machine_state.json`): at start (06:49:09Z) and end (07:30:41Z) no python process on
the `nvidia-smi` compute list (only desktop apps; PIDs 2524 `dwm`, 17208 `Taskmgr` shown as
"Insufficient Permissions"); GPU memory used 3220 → 2838 MiB; uptime 55.30 → 55.99 h (boot
2026-09-14T23:31:17Z). CPU-only python processes of dpc-messenger (`run_service.py`, backlog tooling)
ran on the machine during the session; recorded by CommandLine, not touched. Environment: Python
3.10.20, torch 2.9.1+cu128, flyvis 1.2.0, numpy 2.2.6, CUDA 12.8, cuDNN 91002, NVIDIA RTX PRO 4500
Blackwell, `--no-determinism`, `CUBLAS_WORKSPACE_CONFIG=:4096:8`, `FLYVIS_ROOT_DIR=C:/Users/mikha/Documents/dpc-research/connectome-seed-data`.

Deviations from the brief:
1. **Rule 12 / brief §2, §5:** `c3_evaluator_floor.py` and `c3_jitter_reading.py` were **not
   committed** before they ran — the executor's instruction was to commit only the patched
   `run_individual.py`. Their sha256 is in every output and, for both, in `partA/SHA256.txt`
   (06:59:15Z, before A1); the reading script was exercised on a synthetic json in the scratchpad
   before A1. Uncommitted; for CC to commit.
2. The listing tool lists directories as well as files; the directory `9991` mtime change in A1 is
   the parent of the added `703` (§5), no file changed.
3. B′ output lives in `partB/` as `c3Bprime_proc1.json`; A0 outputs are copied into `A0smoke/`.
4. The A1 line of the brief says "the 65 above"; the 139-rung v1.2 list from brief §3 was used.

## 9. sha256 of outputs

See `SHA256SUMS.txt` in this directory (generated after this README was written; it covers every
file here except itself).
