# Gray-stimulus control, v5.1: complete, no stop

**Status: PREVIEW DIAGNOSTIC -- NOT A TEST.** Protocol:
`docs/briefs/2026-09-16-step1-gray-stimulus.md` **v5.1** (commit `fc7239d`). **v5.1 differs from v5
(`b14f69f`) only in two places.** Two single-call gates became records: `per_item_mean − hook_eval()`
and iteration-0 bitwise equality. The launch word and the reviewer pass were given on v5.

- **Launch word:** Mike, in the DPC Research chat, 2026-09-17 08:37:30Z: «@CC_windows «запускай шаг 1» (v5)».
- **Reviewer pass on v5:** Ark 08:27:19Z and 08:36:24Z; Zcode 08:28:59Z.
- **Run by:** a CC subagent (Opus), 2026-09-17 08:49-09:05Z.

Earlier records in this directory are unchanged. `README_v4_gate_stop.md` is the v4 README,
renamed, with its content unchanged. `README_v31_gate_stop.md` and `README_v2_gate_stop.md` are
kept as they were.

No stop condition fired. The run went in this order: listing before → script update → code gate →
controls (run 000, both checkpoints) → constant-output null → 48 cells → fresh-process repeat →
readings → listing after.

What was not done:
- Nothing was committed or pushed.
- No file outside this directory and the executor's scratchpad was written.
- Nothing was trained.
- No ablation hook was registered. `net._state_hooks == ()` was asserted before and after every
  call.
- Nothing is rounded. Numbers are the `repr` strings from the files named. Where this README says
  "≈", the figure is my own arithmetic, stated as such.

## 1. Files

| file | what | sha256 |
|---|---|---|
| `gray_stimulus.py` | driver, updated v4 (`2c66e661…`, committed `b7c2879`) -> v5.1 (§2); uncommitted | `61eb8bf3068b0bc4a89568c144ab1a931c68a0c4a54659a24cd5b631fc067624` |
| `gray_losses.csv` | 48 cells, process 1; `loss_16` = mean of five calls | `5b652389f4201fa4c3098b0ef1814d75a18d1865434cef1be9109f832c0546c8` |
| `gray_controls.json` | meta, code gate (with diffs), controls, null, P0 ×12, permutations, per-call values of every cell | `2f3bfa47837232012fae6341b1f5f8e9ecd0761b2424c988f067c34f63a0807f` |
| `gray_losses_repeat.csv` | 48 cells, process 2 | `0b751784813d7ee8c29f19b2786fab1887ee2537638a736a4b795c438ca14c2a` |
| `gray_repeat_controls.json` | fresh-process gate per cell, spreads, per-call values of process 2 | `0d4b868afe5c184453ce8dd11af83e7becf93add9ed38d77c2e1f8299b497323` |
| `gray_readings.json` | readings (i)/(ii)/(iii), brief §7 | `0481a783a37a8aba7573d16c82158c184cbb3506b7f736424fb2f3e753d41037` |
| `gray_v51_main.log` | stdout+stderr, `--task main` | `4c630eb5bdfa7644b269f4908ff19bb4d7825a691034cc429ba41b457aa3c8d2` |
| `gray_v51_repeat.log` | stdout+stderr, `--task repeat` | `70f55894743c65bafc07d8b104590d2ea7bbc733aac52ad1ed6de5f95245ee90` |
| `gray_v51_readings.log` | stdout+stderr, `--task readings` | `9a467ff507eabeac04b3ae69df1612838b3748e4882bb1d74f7d80622943a650` |
| `README_v4_gate_stop.md` | v4 README, renamed, content unchanged | `70f147702a656cfab3071033d02fc833aaa2367a5a97ca6894e1a0ef325134bd` |

All three outputs record the script sha256 as `61eb8bf3…`. The imported scripts were not changed:
`diag1_eval_paths.py` `bfb3ca5e…`, `ablation.py` `1545b53b…`, `rowB.py` (night2 = night3)
`195a89b5…`, `ablation_night3.py` `c20013b4…`. Their full hashes are in each json.

## 2. Script changes v4 -> v5.1

Unchanged: conditions, transforms, `per_item_eval_transformed`, the evaluator reuse, `code_gate`,
readings logic, and `--task floor`.

- **`copy_fidelity_control`:**
  - It now makes five copy calls A_1..A_5 (identity transform), then five original calls B_1..B_5,
    then one `hook_eval`.
  - **Gate:** |mean(A_1..A_5) − mean(B_1..B_5)| on the 16-item mean ≤ 1e-2.
  - **Gate:** P0, |mean(A_1..A_5) − stored `val_loss`| ≤ 1e-3.
  - **Recorded, not gating:** all 10 A pairs and all 10 B pairs, all 25 A_i–B_k pairs (per-item
    max, mean difference, bitwise), iteration-0 bitwise equality, `mean(A) − hook_eval()`, and the
    raw per-item vectors.
  - The v4 per-item and 1e-4 mean ceilings were removed.
  - Each gate line in the log prints the ceiling with its derivation.
- **`eval_cell` (new):** one cell is five copy calls, each wrapped in the seven invariants and the
  hook assertion.
  - `loss_16` is the mean of the five calls' 16-item means.
  - The csv per-item columns are per-item means over the five calls.
  - Every call's 16-item mean, per-item vector, wall time and invariants go to json:
    `gray_controls.json` `cells`, and `gray_repeat_controls.json` `cells_this_process`.
- **`require_finite` (new):** NaN or inf in any call → stop.
- **Sweep P0:** each real cell's mean of five minus stored is checked against 1e-3 at all 12
  checkpoints. A breach stops the run after the outputs are written.
- **`--task repeat`:** per cell, |Δ five-call mean| ≤ 1e-2 between the processes. Written next to
  the gate, as records: per-item Δ, the controls' B floor and A spread, the max over the 24 cells of
  the five-call max−min in both processes, and the brief's 8.6e-05.
- Strings changed: STATUS, brief, launch, and the gate texts. The docstring gains a v5.1 section.

**Exercised before launch** (CPU, scratchpad, nothing written in this directory):
- `py_compile` passed. `--task codegate` on the real copy returned PASS.
- A synthetic harness (`…/scratchpad/gray_v51/synth_harness.py`) monkeypatched the solver, the
  evaluator calls and the null, then drove `task_main`, `task_repeat` and `task_readings`:
  - clean case: rc 0, 48 cells, csv and json written;
  - copy off by 0.05 → control FAIL, rc 3, nothing written;
  - one stored `val_loss` off by 5e-3 → sweep P0 FAIL, rc 3;
  - NaN in one call → stop;
  - repeat with one cell shifted 5e-3 → pass; shifted 2e-2 → gate False, rc 3;
  - readings ran without error.

## 3. Code gate (brief §6, unchanged since v4): **PASS**

Result: 2 body lines differ (22 vs 22), and the signature differs only by the name and the
`transform` parameter.

```
--- diag1_eval_paths.py:per_item_eval body (lines 180-201)
+++ gray_stimulus.py:per_item_eval_transformed body (lines 252-273)
-            for _, data in enumerate(dataloader):
+            for _i, data in enumerate(dataloader):
-                solver.network.stimulus.add_input(data["lum"])
+                solver.network.stimulus.add_input(transform(data["lum"], _i))
```
The full diff, including the def line and the docstring, is in `gray_controls.json` `code_gate`
and in the log.

## 4. Controls, run 000 (process 1: PID 40352, solver built 08:56:17Z)

The ceiling next to each number is quoted from the brief:
- **Copy/original, 1e-2.** A sanity bound, not a precision bound. It is ≈ 50x above all measured
  noise on this comparison (≤ 2.0e-4 between processes, C3 Part B) and ≈ 500x below the narrowest
  reading band (0.1·gain_s ≈ 5–6).
- **P0, 1e-3.** The largest value on record on this path is 7e-05.

| | `chkpt_00000` (iter 0) | `chkpt_00071` (iter 250008) |
|---|---|---|
| mean(A_1..A_5) | `1212.5555891990662` | `1148.8074624061585` |
| mean(B_1..B_5) | `1212.5555891990662` | `1148.807447528839` |
| **GATE** mean(A)−mean(B) vs 1e-2 | **`0.0` PASS** | **`1.4877319472361705e-05` PASS** |
| stored `val_loss` | `1212.5555891990662` | `1148.8074851036072` |
| **GATE P0** mean(A)−stored vs 1e-3 | **`0.0` PASS** | **`-2.2697448684994015e-05` PASS** |
| recorded: hook_eval (1 call) / mean(A)−hook | `1212.5555891990662` / `0.0` | `1148.8074359893799` / `2.641677860992786e-05` |
| recorded: B floor, per-item / mean (10 pairs) | `0.0` / `0.0` | `0.000732421875` / `7.62939453125e-05` |
| recorded: A spread, per-item / mean (10 pairs) | `0.0` / `0.0` | `0.0009765625` / `7.867813110351562e-05` |
| recorded: max A_i–B_k, per-item / mean (25 pairs) | `0.0` / `0.0` | `0.0009765625` / `9.012222290039062e-05` |
| recorded: all A and B bitwise equal | True | False |

**P0 on all 12 checkpoints (sweep real cells, mean of five − stored, ceiling 1e-3): all PASS.**
- All six iteration-0 checkpoints give `0.0`.
- At 250008:
  - seed0 `-5.493164053405053e-05`
  - seed0′ `1.468658456360572e-05`
  - seed1 `9.5367431640625e-07`
  - seed2 `3.3855438232421875e-05`
  - seed3 `1.296997061217553e-05`
  - seed4 `-3.5190582366340095e-05`
- The largest |·| is `5.493164053405053e-05`.

Other checks:
- All seven invariants were True on all 240 sweep calls in process 1 and all 240 in process 2.
- No NaN or inf occurred.

## 5. Constant-output null (brief §6)

- `constant_output_null` (per-item mean of `y_gt` over frames and hexals) = **`1039.84645986557`**.
- Zero prediction against `y_gt` (illustrative, not the null) = `1209.561125278473`.

## 6. The 48 cells (process 1)

Each value is the mean of five calls of the 16-item loss. In brackets: max−min over the five calls.
The csv has the full values, and `gray_controls.json` has every call.

| run | chkpt | real | gray 0.5 | zero 0.0 | shuffled |
|---|---|---|---|---|---|
| 000 seed0 | 00000 | 1212.5555891990662 [0.0] | 1212.5542159080505 [0.0] | 1212.556869983673 [0.0] | 1212.5552258491516 [0.0] |
| 000 seed0 | 00071 | 1148.8074301719666 [8.296966552734375e-05] | 1211.1668436050415 [2.956390380859375e-05] | 1206.2047726631165 [1.049041748046875e-05] | 1334.6297996520996 [0.00016689300537109375] |
| 900 seed0′ | 00000 | 1212.5555891990662 [0.0] | 1212.5542159080505 [0.0] | 1212.556869983673 [0.0] | 1212.5552260398865 [9.5367431640625e-07] |
| 900 seed0′ | 00071 | 1160.9823588371278 [2.765655517578125e-05] | 1212.0450295448304 [3.6716461181640625e-05] | 1213.713426208496 [1.3828277587890625e-05] | 1305.5371885299683 [9.393692016601562e-05] |
| 001 seed1 | 00000 | 1212.5529980659485 [0.0] | 1212.5516066551208 [0.0] | 1212.55433177948 [0.0] | 1212.5525994300842 [0.0] |
| 001 seed1 | 00071 | 1144.6362342834473 [7.82012939453125e-05] | 1210.090726661682 [1.049041748046875e-05] | 1237.468939590454 [3.0517578125e-05] | 1314.9330160140992 [0.0001201629638671875] |
| 002 seed2 | 00000 | 1212.5592331886292 [0.0] | 1212.5578484535217 [0.0] | 1212.560553073883 [0.0] | 1212.558837890625 [0.0] |
| 002 seed2 | 00071 | 1147.7179069519043 [5.817413330078125e-05] | 1209.2973438262939 [3.8623809814453125e-05] | 1211.8692244529725 [7.152557373046875e-06] | 1293.171664237976 [8.106231689453125e-05] |
| 003 seed3 | 00000 | 1212.549735546112 [0.0] | 1212.548363685608 [0.0] | 1212.5510201454163 [0.0] | 1212.549370765686 [0.0] |
| 003 seed3 | 00071 | 1155.7706619262694 [3.337860107421875e-05] | 1207.1018383026124 [9.059906005859375e-06] | 1208.8911716461182 [6.67572021484375e-06] | 1305.3612551689148 [0.00010347366333007812] |
| 004 seed4 | 00000 | 1212.5379438400269 [0.0] | 1212.5366048812866 [0.0] | 1212.5392270088196 [0.0] | 1212.5375485420227 [0.0] |
| 004 seed4 | 00071 | 1156.8284293174743 [7.486343383789062e-05] | 1210.6953570365906 [3.24249267578125e-05] | 1217.0418340682984 [1.0013580322265625e-05] | 1284.5165537834168 [6.198883056640625e-05] |

Recorded, no reading attached:
- At iteration 0, runs 000 and 900 give identical values for real, gray and zero. Their shuffled
  values differ by 1.9e-07.
- The recorded control L_untrained_gray − L_untrained_real is −0.001338958740234375 to
  −0.0013914108276367188 across the six seeds.

## 7. Fresh process (process 2: PID 48156, 08:57:42–08:59:06Z)

Gate: per cell, |Δ five-call mean| ≤ 1e-2. The derivation is the same as for the copy/original
ceiling. **48/48 cells pass.**

| chkpt | max \|Δ\| (cell) | vs 1e-2 | cells bitwise equal | recorded: max per-item \|Δ\| | recorded: in-process max−min of five, proc 1 / proc 2 | recorded: brief's spread |
|---|---|---|---|---|---|---|
| 00000 | `1.907349087559851e-07` (seed0 shuffled) | PASS | 23/24 | `3.0517578011313162e-06` | `9.5367431640625e-07` / `9.5367431640625e-07` | 8.6e-05 (at 00071) |
| 00071 | `6.322860713225964e-05` (seed4 shuffled) | PASS | 0/24 | `0.00048828125` | `0.00016689300537109375` / `0.00011444091796875` | 8.6e-05 |

## 8. Readings (brief §7, v3 thresholds)

Readings were computed by `--task readings` from `gray_losses.csv`. I recomputed gain_s
independently from the csv and it matched in all six seeds. The csv `loss_16` equals the json
five-call mean in all 48 cells.

**(i)** holds if |L_trained_gray − L_untrained_gray| ≤ 0.1·gain_s. **It holds for all 6 seeds: "gray
removes ≥ 90% of the learned gain".**

| seed | gain_s | 0.1·gain_s | \|L_tr,gray − L_untr,gray\| | (i) |
|---|---|---|---|---|
| seed0 | 63.74815902709952 | 6.374815902709952 | 1.3873723030089877 | holds |
| seed0′ | 51.573230361938386 | 5.157323036193839 | 0.5091863632201239 | holds |
| seed1 | 67.91676378250122 | 6.791676378250123 | 2.460879993438766 | holds |
| seed2 | 64.84132623672485 | 6.484132623672486 | 3.260504627227874 | holds |
| seed3 | 56.77907361984262 | 5.677907361984262 | 5.44652538299556 | holds |
| seed4 | 55.70951452255258 | 5.570951452255258 | 1.8412478446959994 | holds |

**(ii), seed 2.** The rule: excess = L_trained,cond − L_untrained_gray (`1212.5578484535217`).
"Explodes" means ≥ 10·gain_s = 648.4132623672485. "Returns" means ≤ 0.1·gain_s = 6.484132623672486.
- (a) gray: excess `-3.260504627227874` (`-0.05028436055308795` gain_s) → **returns**.
- (b) zero: excess `-0.6886240005492255` (`-0.010620140588043715` gain_s) → **returns**.

Neither explodes, so the branch in the brief's words is: **"explosion only under the ablation's
forced-zero state, i.e. neither (a) nor (b) explode -> the ablation deltas -- +21,158 (R2 single-type
clamp-to-0) and +30,626 (full R1-R8 clamp-to-0) -- measure the dynamics' fragility to a zero clamp
specifically, an instrument artefact, not a vision dependence, and the R2 ablation finding must be
reworded accordingly."**

The same classification for the other seeds, recorded but not pre-registered as a reading:
- gray returns in all six seeds;
- zero returns in five seeds;
- seed1 zero is **between**: excess `24.917332935333206`, `0.3668804511229254` gain_s.

**(iii), shuffled.** The two references are L_trained_real and L_untrained_gray. The band is
0.1·gain_s. The reading is void if the references lie within 0.2·gain_s of each other; they are
63.7/51.6/67.9/64.8/56.8/55.7 apart, so no seed is void. **All 6 seeds: "between".** Shuffled is
farther than 0.1·gain_s from both references.

| seed | L_trained_shuffled | − L_trained_real | − L_untrained_gray |
|---|---|---|---|
| seed0 | 1334.6297996520996 | 185.82236948013292 | 122.07558374404903 |
| seed0′ | 1305.5371885299683 | 144.55482969284049 | 92.98297262191772 |
| seed1 | 1314.9330160140992 | 170.2967817306519 | 102.38140935897832 |
| seed2 | 1293.171664237976 | 145.45375728607178 | 80.61381578445435 |
| seed3 | 1305.3612551689148 | 149.59059324264535 | 92.81289148330688 |
| seed4 | 1284.5165537834168 | 127.68812446594256 | 71.97994890213022 |

Recorded fact, not a reading: in every seed the shuffled loss lies **above both** references
(≈ 1.2–1.9 gain_s above L_untrained_gray, my arithmetic), not numerically between them. The brief's
"between" branch ("otherwise") covers this case. The brief has no separate branch for it.

## 9. Run-dir integrity (brief §9.2)

All 594 files under `connectome-seed-data/results/flow/9991/{000,900,001,002,003,004}` were listed,
files only, with `find … -type f -printf "%p %s %T@\n" | sort`:
- The before listing was taken at 08:49:38Z, before any edit.
- The after listing was taken at 08:59:29Z.
- **The diff is empty (0 bytes).** Both listings hash to
  `64d84e68e0bcd4bbeca6ac8664069e367094a267a184af695cc41863d83106f7`, the same hash as the v2, v3.1
  and v4 runs.
- `find connectome-seed-data -newermt "2026-09-17 08:49 UTC" -type f` returns nothing.
- In `connectome-seed`, the only files newer than 08:49Z are in this directory.

The listings are in `…/03852100-…/scratchpad/gray_v51/v51_{before,after}.txt` and
`v51_listing.diff`. The scratch netdirs are `…/scratchpad/gray_v51/netdir_v51_{main,repeat}`.

## 10. Interpreter, commands, timings, GPU

```
PY=".../63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/.venv/Scripts/python.exe"
cd C:/Users/mikha/Documents/dpc-research/connectome-seed
FLYVIS_ROOT_DIR=C:/Users/mikha/Documents/dpc-research/connectome-seed-data PYTHONIOENCODING=utf-8 \
  "$PY" -u results/diagnostics/gray/gray_stimulus.py --task main   --out-dir results/diagnostics/gray --netdir-root ".../scratchpad/gray_v51/netdir_v51_main"
  "$PY" -u results/diagnostics/gray/gray_stimulus.py --task repeat --out-dir results/diagnostics/gray --netdir-root ".../scratchpad/gray_v51/netdir_v51_repeat"
  CUDA_VISIBLE_DEVICES="" "$PY" -u results/diagnostics/gray/gray_stimulus.py --task readings --out-dir results/diagnostics/gray
```
The environment was Python 3.10.20, torch 2.9.1+cu128 and flyvis 1.2.0, on `cuda` with an NVIDIA
RTX PRO 4500 Blackwell.

| task | wall | exit | notes |
|---|---|---|---|
| main | 08:55:42–08:57:25Z; in-script total `101.41197570000077` s | 0 | the first real call took `0.1845086999819614` s; the 240 sweep calls took `0.1825247000087984`–`0.3928217000211589` s |
| repeat | 08:57:42–08:59:06Z; in-script `82.65351289999671` s | 0 | the 240 calls took `0.1802828999934718`–`0.47487370000453666` s |
| readings | 08:59:14–08:59:15Z | 0 | CPU only |

GPU before the start (08:49Z and 08:55Z): no python process in `nvidia-smi`. The only python
processes on the machine were the two dpc-messenger `run_service.py`, identified by CommandLine. No
training wave was running. GPU after the end (08:59Z): no python process, 2909 MiB used by desktop
apps, 0 % utilisation.

The log contains a torch `UserWarning` ("non-tuple sequence for multidimensional indexing"). It is
emitted once, before the first control call, and the v4 log has it once too.

## 11. Deviations and interpretations

1. **Code gate scope, unchanged from v4.** The executable body and the signature are gated. The
   def-line text and the docstring are shown in the diff but not gated.
2. **P0's 1e-3 ceiling was also applied to the real cells of all 12 checkpoints in the sweep**, per
   "each checkpoint's stored `val_loss`". A breach there would have stopped the run after writing
   the outputs. None occurred.
3. **An explicit NaN/inf check was added** (`require_finite`), per the brief's §6 v5 Stops. v4 had no
   explicit check.
4. **CSV definition.** `loss_16` is the mean of the five calls' 16-item means. The per-item columns
   are per-item means over the five calls. Per-call values are only in the json files.
5. `hook_eval` is a single call per control checkpoint, as in v4. It is recorded only.
6. **Call order.** A_1..A_5 ran as a block before B_1..B_5, with no interleaving. This keeps v4's
   A-before-B order.
7. `PYTHONIOENCODING=utf-8` was set for all three invocations; it affects stdout encoding only.
   `CUDA_VISIBLE_DEVICES=""` was set for `--task readings`, which is CPU only.
8. The repeat json adds a record next to the gate: the per-cell five-call max−min in both processes.
   Other additions are the csv `gray_losses_repeat.csv` (present since v3.1) and three log files
   (`gray_v51_*.log`).
