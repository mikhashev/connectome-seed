# Night-3 derivatives — commands, interpreter, provenance

**Date:** 2026-09-16 · **Built by:** CC's subagent on Sonnet, from
`results/night2/extract_night2.py`'s approach (same two-key slim, same
`iter_wall_s`/`train_loss_last1000` derivatives, same wave-file copies,
extended to a six-run checkpoint table) · **Verified by:** CC.

Night 3 ran seeds 3 and 4 to completion in one wave, no reboot, no partial
run — there is no `killed_*.partial.json` counterpart this time and only one
wave-file triple (`wave_night3.json`/`.launcher.log`/`.progress.log`).

## Hardening items applied (`docs/tool-hardening-package.md`)

- **Item 9** (script hash in provenance): `results/night3/extract_night3.py`
  sha256 = `65c3cabfcad07cea765a3adec9a441b767f583765fae20b84c3775a175582692`
  (`sha256sum results/night3/extract_night3.py`; git blob hash
  `1d235a6b7ba23aa73640682427b3a9cb449b556f` via `git hash-object`, recorded
  for cross-check even though the file is untracked at write time). Any
  regenerated output should be diffed against a fresh run of the script at
  this hash; if the hash changes, re-derive before trusting a number here.
- **Item 19** (formatter provenance): `night_report_checkpoints.csv` (this
  directory) is **full float**, written directly from the six run jsons'
  `checkpoint_metrics` by `extract_night3.py` — same convention as night 2's
  four-way file, **not** `tools/night/night_report.py`'s `r4()` 4-decimal
  formatter. The three pairwise `night_report_checkpoints_{3v0,4v0,4v3}.csv`
  files below **are** `r4()`-formatted (they come straight from
  `night_report.py`, unmodified) — any claim below 1e-4 must come from the
  full-float six-way file, not the pairwise ones. Stated once here rather
  than repeated per file.

## Interpreter

System `python` via the `py` launcher, 3.12.10 this session (standard
library only — `extract_night3.py` and `tools/night/night_report.py` need
no third-party package; the night-run venv, 3.10.20, was not needed, same
as night 2's provenance note).

## Commands, verbatim, in the order they were run

```bash
cd "c:/Users/mikha/Documents/dpc-research/connectome-seed"

# 1. slim jsons, iter_wall_s csv.gz, train_loss_last1000 csv, wave-file
#    copies, six-way checkpoint table, rung SD (n=5 vs n=3) with chi2 CI,
#    plateau/minimum/late-offset summary -- all in one script
py results/night3/extract_night3.py

# 2. pairwise night_report.py, unmodified, its only supported form
#    (--a/--b), against the RAW run jsons (not the slim ones -- night_report.py
#    needs iter_wall_s for the two-phase price table, which the slim jsons drop)
RAW="C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/night"

py tools/night/night_report.py --a "$RAW/night1_9991-000.json" --b "$RAW/night3_9991-003.json" \
    --checkpoints-csv results/night3/night_report_checkpoints_3v0.csv \
    > results/night3/night_report_3v0.md

py tools/night/night_report.py --a "$RAW/night1_9991-000.json" --b "$RAW/night3_9991-004.json" \
    --checkpoints-csv results/night3/night_report_checkpoints_4v0.csv \
    > results/night3/night_report_4v0.md

py tools/night/night_report.py --a "$RAW/night3_9991-003.json" --b "$RAW/night3_9991-004.json" \
    --checkpoints-csv results/night3/night_report_checkpoints_4v3.csv \
    > results/night3/night_report_4v3.md

# 3. sha256 / git blob hash of the extraction script, for the provenance
#    line above
sha256sum results/night3/extract_night3.py
git hash-object results/night3/extract_night3.py
```

`night_report.py`'s `--a`/`--b` labels are generic ("run A" / "run B", not "run 0" / "replicate")
— `3v0` reads run A = seed 0, run B = seed 3; `4v0` reads run A = seed 0, run B = seed 4; `4v3`
reads run A = seed 3, run B = seed 4 (the second same-wave pair, mirroring the (0, 0') position
in night 1's own wave).

## What each file is

- `night3_9991-00{3,4}.slim.json` — the raw `run_individual.py` json with `iter_wall_s` and
  `train_loss_per_iter` dropped; key set asserted equal to
  `results/night2/night2_9991-001.slim.json`'s key set by `extract_night3.py` (assertion in the
  script, printed as "key-set matches night2 slim reference" on success — it would raise
  `AssertionError` otherwise, not print a false "matches").
- `iter_wall_s_9991-00{3,4}.csv.gz` — full per-iteration wall time, one float per line, gzip,
  no header (250,008 rows each).
- `train_loss_last1000_9991-00{3,4}.csv` — last 1000 entries of `train_loss_per_iter`, one float
  per line, no header.
- `wave_night3.json` / `wave_night3.launcher.log` / `wave_night3.progress.log` — literal copies
  of the raw night-run wave files (one wave, both jobs, no reboot).
- `night_report_{3v0,4v0,4v3}.md` + `night_report_checkpoints_{3v0,4v0,4v3}.csv` —
  `tools/night/night_report.py` output, unmodified script, three pairwise invocations.
- `night_report_checkpoints.csv` — six-run (seed 0, 0', 1, 2, 3, 4) table over the 72 common
  checkpoint iterations, full float (item 19 above).
- `extract_night3.py` — this session's script (sha256 above).

## Verification performed

- Key-set equality of both night-3 slim jsons against a night-2 slim json reference: passed
  (assertion in `extract_night3.py`, no `AssertionError` raised).
- Rung values reproduced from the slim jsons match the task brief's independently-supplied
  hook values exactly (seed 3: 1210.4139 / 1205.5457 / 1192.5858 / 1152.5066; seed 4: 1207.2574
  / 1206.3897 / 1208.6099 / 1153.1134).
- SD(n=5) at the four rungs (1.2698 / 0.8173 / 8.3788 / 3.5426) and the plateau/minimum figures
  for seeds 3 and 4 (plateau 1154.4052 / 1154.4837; minimum 1150.9345 at 237,612 / 1150.0934 at
  198,012) reproduce the task brief's independently-supplied values exactly.
- 72 common checkpoints across all six runs, same as night 1/night 2's 72 (checkpoint cadence is
  set by `chkpt_every_epoch`/epoch length, not by seed).
