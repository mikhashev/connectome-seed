# Flyvis night-2 report (combined)

`tools/night/night_report.py` takes exactly one `--a` and one `--b` run json
(argparse, both required) — it is strictly pairwise, confirmed by reading the
script (`ap.add_argument("--a", ...)`, `ap.add_argument("--b", ...)`, no
variadic option). This file is the four-way (seed 0, seed 0′, seed 1, seed 2)
combination built by hand from three pairwise runs of that script plus one
extra script (`extract_night2.py`, same directory), not itself an invocation
of `night_report.py`.

Pairwise reports run verbatim (`python tools/night/night_report.py --a <A>
--b <B> --checkpoints-csv <path>`), one per pair, saved as:

- `night_report_1v0.md` — A = seed 0 (`night1_9991-000.json`), B = seed 1
  (`night2_9991-001.json`); diff column = B−A = seed1 − seed0.
- `night_report_2v0.md` — A = seed 0, B = seed 2 (`night2b_9991-002.json`);
  diff = seed2 − seed0.
- `night_report_2v1.md` — A = seed 1, B = seed 2; diff = seed2 − seed1.

Each pairwise checkpoint CSV: `night_report_checkpoints_1v0.csv`,
`_2v0.csv`, `_2v1.csv`. The combined four-seed checkpoint CSV
(`night_report_checkpoints.csv`, 72 rows: iteration, val_loss for seed0 /
seed0′ / seed1 / seed2, and the three same-population diffs 1−0, 2−0, 2−1)
is built by `extract_night2.py`, not by `night_report.py`.

## Runs

| run | id | seed | started_utc (run json) | finished_utc (run json) | total_train_wall_s | final_iteration | exit |
|---|---|---|---|---|---|---|---|
| seed 0 | `9991/000` | 0 | 2026-09-13T18:40:31Z | 2026-09-13T22:40:56Z | 14417.6889 | 250008 | ok |
| seed 0′ | `9991/900` | 0 | 2026-09-13T22:40:59Z | 2026-09-14T02:39:51Z | 14319.9398 | 250008 | ok |
| seed 1 | `9991/001` | 1 | 2026-09-14T19:12:34Z | 2026-09-14T23:14:59Z | 14532.8769 | 250008 | ok |
| seed 2 (killed) | `9991/002` (night2) | 2 | 2026-09-14T23:15:02Z | — (killed) | n/a | none (last progress-log iteration 12,700 at 2026-09-14T23:29:04Z) | `training` (interrupted) |
| seed 2 (re-run) | `9991/002` (night2b) | 2 | 2026-09-15T01:13:49Z | 2026-09-15T05:12:17Z | 14296.6488 | 250008 | ok |

Source: `night1_9991-000.slim.json`, `rep_9991-900.slim.json` (both
`results/night1/`), `night2_9991-001.slim.json`, `night2b_9991-002.slim.json`,
`killed_9991-002.partial.json` (all `results/night2/`).

## Two-phase price (median s/iter, phase split at iteration 150,000)

| run | phase1 [1,000-150,000] | phase2 [150,001-end] | overall median |
|---|---|---|---|
| seed 0 | 0.0644 | 0.0452 | 0.0614 |
| seed 0′ | 0.0639 | 0.0451 | n/a (not recomputed here; see `docs/experiments/001-run0-and-replicate.md` §4) |
| seed 1 | 0.0647 | 0.0459 | 0.0622 |
| seed 2 | 0.0636 | 0.0454 | 0.0611 |

Source: `night_report_1v0.md` / `night_report_2v0.md` / `night_report_2v1.md`
(the "Two-phase price" table, rows A/B), cross-checked against
`extract_night2.py`'s own `two_phase_price()` printout (same medians to
printed precision) and `iter_wall_s_9991-001.csv.gz` / `iter_wall_s_9991-002.csv.gz`.

## Rung table (held-out loss, evaluation hook)

| iteration | seed 0 | seed 0′ | seed 1 | seed 2 | \|1-0\| | \|2-0\| | \|2-1\| | SD(0,1,2) n=3 | replicate \|0′-0\| | SD/replicate |
|---|---|---|---|---|---|---|---|---|---|---|
| 1,000 | 1208.9363 | 1208.9363 | 1208.0556 | 1209.7639 | 0.8807 | 0.8276 | 1.7083 | 0.8543 | 0.0000 | inf |
| 5,000 | 1207.7673 | 1207.7698 | 1206.7832 | 1207.0115 | 0.9841 | 0.7558 | 0.2283 | 0.5151 | 0.0025 | 206.03 |
| 25,000 | 1191.7375 | 1192.0739 | 1190.2235 | 1204.3618 | 1.5140 | 12.6243 | 14.1383 | 7.7627 | 0.3365 | 23.08 |
| 250,000 | 1146.1958 | 1158.9237 | 1145.3572 | 1148.8000 | 0.8386 | 2.6042 | 3.4428 | 1.7953 | 12.7279 | 0.14 |

Source: rung tables in `night_report_1v0.md`, `night_report_2v0.md`,
`night_report_2v1.md` (the "Rung table" B−A rows); SD and SD/replicate
computed directly from the eight numbers above (orchestrator-supplied,
cross-checked by `statistics.stdev([s0,s1,s2], ddof=1)` in this session — see
task report).

## Checkpoints

72 common checkpoint iterations across all four runs (seed0, seed0′, seed1,
seed2) — source: `night_report_checkpoints.csv`, built by
`extract_night2.py` from the four `checkpoint_metrics` arrays.

See `docs/experiments/002-night2-seeds-1-and-2.md` §3 for the after-150,000
subset (29 checkpoints), plateau and minimum-loss figures per seed.

## Provenance

Generated 2026-09-15 by `results/night2/extract_night2.py` (combined table,
copies) plus three direct invocations of `tools/night/night_report.py`
(pairwise reports) — see `docs/experiments/002-night2-seeds-1-and-2.md` §6.
