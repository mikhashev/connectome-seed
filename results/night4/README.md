# Night-4 derivatives — commands, interpreter, provenance

**Date:** 2026-09-17 · **Built by:** CC's subagent on Sonnet, from
`results/night3/extract_night3.py`'s approach (same two-key slim, same
`iter_wall_s`/`train_loss_last1000` derivatives, same wave-file copies,
extended to an eight-run checkpoint table) · **Verified by:** CC.

Night 4 ran two jobs in one wave, no reboot, no partial run — replicate 3′
(seed 3, id `9991/903`, tag `rep`) FIRST, then the new seed 5 (id
`9991/005`, tag `night4`) — there is no `killed_*.partial.json`
counterpart and only one wave-file triple
(`wave_night4.json`/`.launcher.log`/`.progress.log`).

## Hardening items applied (`docs/tool-hardening-package.md`)

- **Item 9** (script hash in provenance): `results/night4/extract_night4.py`
  sha256 = `480e3855d2468701a298ae128cf33771a0b08214fab30e77db8c1189e87d61d0`
  (`sha256sum results/night4/extract_night4.py`; git blob hash
  `fc7c8113a449c19a922ff56eac55582c6f9d0f18` via `git hash-object`, recorded
  for cross-check even though the file is untracked at write time). Any
  regenerated output should be diffed against a fresh run of the script at
  this hash; if the hash changes, re-derive before trusting a number here.
- **Item 19** (formatter provenance): `night_report_checkpoints.csv` (this
  directory) is **full float**, written directly from the eight run jsons'
  `checkpoint_metrics` by `extract_night4.py` — same convention as night 3's
  six-way file (`results/night3/README.md`), extended from six to eight
  runs, **not** `tools/night/night_report.py`'s `r4()` 4-decimal formatter.
  The three pairwise `night_report_checkpoints_{3primev3,5v0,3primev0prime}.csv`
  files below **are** `r4()`-formatted (they come straight from
  `night_report.py`, unmodified) — any claim below 1e-4 must come from the
  full-float eight-way file, not the pairwise ones. Stated once here rather
  than repeated per file. (The task brief describes this file as an
  "eight-row CSV of checkpoints" — read here, per night 3's own naming
  convention ("six-run", not "six-row", for the analogous six-column file),
  as the eight-*run* table: rows are the 72 common checkpoint iterations,
  columns are the eight runs. This is the structure the downstream
  selected-checkpoint-difference numbers in `docs/experiments/004-*.md`
  need — a literal 8-row table of one summary value per run would not
  support them.)

## Interpreter

System `python` via the `py` launcher, 3.12.10 this session (standard
library only — `extract_night4.py` and `tools/night/night_report.py` need
no third-party package; the night-run venv, 3.10.20, was not needed, same
as night 2/3's provenance note).

## Commands, verbatim, in the order they were run

```bash
cd "c:/Users/mikha/Documents/dpc-research/connectome-seed"

# 1. slim jsons, iter_wall_s csv.gz, train_loss_last1000 csv, wave-file
#    copies, eight-way checkpoint table, rung SD (n=6 vs n=5) with chi2 CI,
#    plateau/minimum/learned-gain/late-offset summary -- all in one script
py results/night4/extract_night4.py

# 2. pairwise night_report.py, unmodified, its only supported form
#    (--a/--b), against the RAW run jsons (not the slim ones -- night_report.py
#    needs iter_wall_s for the two-phase price table, which the slim jsons drop)
RAW="C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/night"

py tools/night/night_report.py --a "$RAW/night3_9991-003.json" --b "$RAW/rep_9991-903.json" \
    --checkpoints-csv results/night4/night_report_checkpoints_3primev3.csv \
    > results/night4/night_report_3primev3.md

py tools/night/night_report.py --a "$RAW/night1_9991-000.json" --b "$RAW/night4_9991-005.json" \
    --checkpoints-csv results/night4/night_report_checkpoints_5v0.csv \
    > results/night4/night_report_5v0.md

py tools/night/night_report.py --a "$RAW/rep_9991-900.json" --b "$RAW/rep_9991-903.json" \
    --checkpoints-csv results/night4/night_report_checkpoints_3primev0prime.csv \
    > results/night4/night_report_3primev0prime.md

# 3. sha256 / git blob hash of the extraction script, for the provenance
#    line above
sha256sum results/night4/extract_night4.py
git hash-object results/night4/extract_night4.py
```

`night_report.py`'s `--a`/`--b` labels are generic ("run A" / "run B", not "run 0" / "replicate")
— `3primev3` reads run A = seed 3 (`9991/003`), run B = replicate 3′ (`9991/903`); `5v0` reads
run A = seed 0 (`9991/000`), run B = seed 5 (`9991/005`); `3primev0prime` reads run A = replicate
0′ (`9991/900`), run B = replicate 3′ (`9991/903`) — these are the three pairs the task brief
named (3′ vs 3), (5 vs 0), (3′ vs 0′), not a mechanical mirror of night 3's own three pairs (which
were new-vs-seed0, new-vs-seed0, new-vs-new); night 4 has one new seed (5, comparable to seed 0)
and one replicate (3′, comparable to 0′), so the natural pairing differs from night 3's two
same-cohort seeds.

## What each file is

- `rep_9991-903.slim.json` / `night4_9991-005.slim.json` — the raw
  `run_individual.py` json with `iter_wall_s` and `train_loss_per_iter` dropped; key set
  asserted equal to `results/night2/night2_9991-001.slim.json`'s key set by
  `extract_night4.py` (assertion in the script, printed as "key-set matches night2 slim
  reference" on success — it would raise `AssertionError` otherwise, not print a false
  "matches").
- `iter_wall_s_9991-{903,005}.csv.gz` — full per-iteration wall time, one float per line, gzip,
  no header (250,008 rows each).
- `train_loss_last1000_9991-{903,005}.csv` — last 1000 entries of `train_loss_per_iter`, one
  float per line, no header.
- `wave_night4.json` / `wave_night4.launcher.log` / `wave_night4.progress.log` — literal copies
  of the raw night-run wave files (one wave, both jobs, no reboot). (The source directory also
  holds a `wave_night4.pid` file; night 3's script did not copy the `.pid` file for its wave and
  this one mirrors that omission — it is a live-run artifact, not a night record.)
- `night_report_{3primev3,5v0,3primev0prime}.md` + their
  `night_report_checkpoints_{3primev3,5v0,3primev0prime}.csv` —
  `tools/night/night_report.py` output, unmodified script, three pairwise invocations.
- `night_report_checkpoints.csv` — eight-run (seed 0, 0′, 1, 2, 3, 4, 3′, 5) table over the 72
  common checkpoint iterations, full float (item 19 above).
- `extract_night4.py` — this session's script (sha256 above).

## Verification performed

- Key-set equality of both night-4 slim jsons against the night-2 slim json reference: passed
  (assertion in `extract_night4.py`, no `AssertionError` raised).
- Rung values reproduced from the slim jsons match the task brief's independently-supplied hook
  values exactly (3′: 1210.4302 / 1205.5182 / 1187.4011 / 1162.9375; seed 3 unchanged from night
  3: 1210.4139 / 1205.5457 / 1192.5858 / 1152.5066; seed 5: 1207.3300 / 1208.2387 / 1204.7794 /
  1159.1158).
- Checkpoint at final_iteration 250,008: 3′ 1163.3766, seed 3 1155.7706 (diff +7.6059); 0′
  1160.9823, seed 0 1148.8075 (diff +12.1749) — both match the task brief exactly.
- Learned gain (checkpoint 0 − checkpoint 250,008): seed 3 56.7791, 3′ 49.1732, seed 5 56.1601 —
  match the task brief exactly (all other six runs' learned gains are printed by the script too,
  not carried into the task brief's list, and not otherwise used in this record).
- Tail (29 common checkpoints after iteration 150,000): 3′−3 positive 27/29, min −3.5566, median
  +7.9409, max +12.4983, mean +7.0032; 0′−0 positive 29/29, min +3.6803, median +12.2470, max
  +17.8153, mean +12.6406 — match the task brief exactly.
- Selected checkpoint differences 3′−3 at iterations 25,212 / 72,012 / 79,212 / 151,212 / 180,012:
  −2.9157 / −3.8997 / +11.9719 / +11.5324 / +1.7352 — match the task brief exactly (to the fourth
  decimal the brief rounds to three).
- Spread of the six individuals (0, 1, 2, 3, 4, 5) at the 250,000 hook: SD(n=6) = 5.1425 (full
  precision 5.142473), mean 1150.8481 (rounds to 1150.848); 95 % χ² interval for σ at n=6 (5
  degrees of freedom, χ²₀.₉₇₅,₅ = 12.8325, χ²₀.₀₂₅,₅ = 0.8312) = [3.2100, 12.6126] (rounds to
  [3.210, 12.613]); SD at n=5 (seeds 0..4) = 3.5426 — all match the task brief exactly (this is
  the same SD(n=5) figure already on record in `results/night3/README.md`, reproduced here for
  the n=5-vs-n=6 comparison, not recomputed from new data).
- Wall (launcher `wall_s`, `wave_night4.json`): 903 = 14444.199462300021 s (rounds to 14444.2),
  005 = 14474.074574700004 s (rounds to 14474.1); `WAVE DONE 2/2 ok` at
  `wave_night4.json`'s `finished_utc` = `2026-09-17T04:29:27Z` — all match the task brief exactly.
  (Each run's own `total_train_wall_s` field — 14435.3311 for 903, 14460.3758 for 005 — is a
  different, slightly shorter quantity than the launcher's `wall_s`; the task brief's "Wall"
  figures are the launcher ones, consistent with how night 1–3's "wall (launcher)" column was
  reported in `docs/experiments/00{1,2,3}-*.md` §1.)
- 72 checkpoints each, `errors: []` for both runs — match the task brief exactly.
- `argv` of `9991/903` differs from `9991/003`'s only in `--id` (`9991/903` vs `9991/003`), `--tag`
  (`rep` vs `night3`) and `--progress-file` (`wave_night4.progress.log` vs
  `wave_night3.progress.log`) — every other argv element (`--seed 3`, `--n-iters 250000`,
  `--rungs 1000,5000,25000,250000`, `--out-dir`, `--no-determinism`, `--progress-every 100`) is
  byte-identical, confirmed by direct comparison of both jsons' `argv` lists.
- `connectome_sha256` (`bfbb0766251ff09e22723d0ebbf7b14793e70b3ae8ad0eea64eac9d28223351a`) and
  `versions` (`flyvis 1.2.0`, `torch 2.9.1+cu128`, `numpy 2.2.6`, `python 3.10.20`, `cuda 12.8`,
  `cudnn 91002`, `gpu NVIDIA RTX PRO 4500 Blackwell`) are identical across `night3_9991-003.json`,
  `rep_9991-903.json` and `night4_9991-005.json`.

## Provenance

- `results/night4/extract_night4.py` — this session's script; sha256
  `480e3855d2468701a298ae128cf33771a0b08214fab30e77db8c1189e87d61d0` (hardening item 9,
  `docs/tool-hardening-package.md`); builds the slim jsons, the two `iter_wall_s_*.csv.gz`, the
  two `train_loss_last1000_*.csv`, copies the wave json/launcher-log/progress-log triple, and
  builds the eight-way `night_report_checkpoints.csv` (full float — hardening item 19; see the
  note above). Its own equality assertion checks that both night-4 slim jsons carry exactly
  `results/night2/night2_9991-001.slim.json`'s key set.
- `tools/night/night_report.py` — run unmodified, three times (`--a`/`--b` pairwise, its only
  supported form), against the raw run jsons (the slim jsons drop `iter_wall_s`, which the
  two-phase price table needs): `night_report_3primev3.md`, `night_report_5v0.md`,
  `night_report_3primev0prime.md` (plus their own
  `night_report_checkpoints_3primev3.csv` / `_5v0.csv` / `_3primev0prime.csv`, `r4()`-formatted —
  see the item-19 note above on which files are full float and which are not).
- Interpreter: system `python` via the `py` launcher (3.12.10 this session; the night-run venv,
  3.10.20, was not needed — both scripts use only the standard library).
- Inputs read (not modified): raw run jsons in the night scratchpad (`night1_9991-000.json`,
  `rep_9991-900.json`, `night3_9991-003.json`, `rep_9991-903.json`, `night4_9991-005.json`, and
  the three `wave_night4.*` files), `results/night1/night1_9991-000.slim.json`,
  `results/night1/rep_9991-900.slim.json`, `results/night2/night2_9991-001.slim.json`,
  `results/night2/night2b_9991-002.slim.json`, `results/night3/night3_9991-003.slim.json`,
  `results/night3/night3_9991-004.slim.json`.
- Written by: CC's subagent on Sonnet, 2026-09-17. Verified by: CC.
