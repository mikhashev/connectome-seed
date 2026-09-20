# atlas — one page that says where the project is

`build.py` reads what already exists in machine-readable form in this repository and writes a
single self-contained file, `atlas.html`, at the repository root: inline CSS, inline JS, inline
JSON, no CDN, no fonts, no network. It opens from `file://`. The reader is the owner, not a
specialist; the UI text is plain English and technical identifiers are left as they are.

Standard library only (`argparse`, `csv`, `json`, `re`, `subprocess`, `pathlib`, `datetime`).
No GPU, no third-party imports, no LLM call. It reads `results/` and never writes there, and it
never opens a `*_steps_*.h5`.

## Run

```
python tools/atlas/build.py                 # writes atlas.html at the repository root
python tools/atlas/build.py --out /tmp/a.html
python tools/atlas/build.py --check         # what was found / missing / unparsed; no file written
```

Takes well under a second. `--check` exits 0 even when optional data is absent; a non-zero exit
means the script itself crashed.

## What it reads

| section | fed from |
|---|---|
| A "Where we are" | `verdicts.json` (sourced from `VISION.md`, experiment 005) + `git log` / `git status` / `git rev-list` |
| B "Awaiting Mike's word" | open `backlog.md` entries whose envelope or body says *Mike's word* / *Mike decides*, or that `verdicts.json` flags `awaits_mike: true`; plus the uncommitted-file and unpushed-commit counts from git |
| C "Night timeline" | `results/night*/wave_*.json`, `results/night*/*.slim.json`, `results/night*/*killed*.json`, `docs/experiments/00N-*.md` |
| D "Flies" | `results/night5/run_columns.csv` — the explicit run → column → seed → role mapping |
| E "Learning curves" | `results/night5/night_report_checkpoints.csv`, columns resolved through `run_columns.csv`; the second chart from `results/night5/diagnostics/rowB/penalised_quantity_by_checkpoint.csv` |
| F "Instruments and controls" | each diagnostic directory's `*controls*.json` / `*readings*.json`, counting boolean `pass` fields; links to each instrument's README |
| G "Board" / "Decisions" | `backlog.md`, `backlog_closed.md`, `docs/decisions/*.md` front matter |
| H "Recent activity" | `git log -15` |

**Run identity is never derived from a column name.** `run_columns.csv` says why: the prime
marks count marks, not order. The page shows the recorded `run_id` and builds its human label
from the recorded `seed` and `run_index_for_seed`.

**Numbers are shown as recorded.** Nothing is re-estimated. The script computes only counts,
dates, durations and the axis bounds a chart needs.

**Anything that cannot be parsed becomes a hatched card naming the file, never a guess.** The
hatch labels are `not measured`, `not explained`, `not read yet`, `source not parsed` and
`no plain-language summary yet`, and each one says which file it is about. Several older controls
files record their controls as differences rather than as boolean `pass` fields; those tiles
hatch `not measured` on purpose.

## Adding a verdict

`verdicts.json` holds the plain-language texts, keyed by card id. A card with no entry renders a
hatched `not explained` block, so the debt is visible on the page rather than hidden.

```json
"diag:connectivity": {
  "text": "One or two sentences in plain English.",
  "source": ["results/night2/diagnostics/connectivity/README.md"]
}
```

Card ids: `where_we_are`, `flies`, `curves`, `penalised`, `board`, `night1`…`night5`, and
`diag:<id>` for each tile in `DIAGNOSTICS` in `build.py`. `build.py --check` prints every card
that is still without a verdict. A backlog entry's NAME can also be used as a key, with
`"awaits_mike": true`, to put that entry into section B when its text does not carry the phrase.

## Restating a board entry in plain language

Sections B and G show board entries. A board entry is written for the people working on it, and
its envelope sentence assumes the whole context. `verdicts.json` → `backlog_plain`, keyed by the
entry's NAME, holds a plain-language restatement and the decision being asked for. An entry with
no restatement shows its own board sentence under a hatched `no plain-language summary yet`
label, so that debt is visible too.

```json
"backlog_plain": {
  "SOME-ENTRY-NAME": {
    "text": "What the entry records, in everyday words, without softening.",
    "ask": "The decision needed, put as a question that can be answered in a word.",
    "source": ["backlog.md"]
  }
}
```

Write the `ask` from the entry's own **First step** line; do not invent an option the entry does
not offer.

**Write only what a document in this repository already says, and put that document's path in
`source`.** The source line is rendered under the verdict, so a reader can go and check it. Do
not interpret; if the repository has not concluded something, leave the card hatched.

## Rebuild after each commit

The owner pastes this; agents do not edit `.claude/`. It is a second entry in the existing
`PostToolUse` → `Bash` hooks array of `.claude/settings.local.json`, beside the orbit hook and
in the same format:

```json
{
  "type": "command",
  "if": "Bash(git commit*)",
  "command": "python \"${CLAUDE_PROJECT_DIR:-.}/tools/atlas/build.py\" >/dev/null 2>&1 || exit 0",
  "timeout": 60,
  "statusMessage": "atlas rebuild"
}
```

`|| exit 0` keeps a failed rebuild from failing the commit; run `build.py --check` by hand when
the page looks stale.

## Contamination

`atlas.html` is a **view full of result values**, and it is in `.gitignore` beside the other
built views. It must never be committed.

It is also **off limits to a blind v2 author** under
`docs/decisions/003-blind-authorship-after-the-numbers.md`: the page carries ten runs' loss
curves, the penalised quantity, the row-B control counts and the reachability verdict on one
screen, which is the densest single leak in the repository. **`verdicts.json` carries measured
values too** — its plain-language texts quote results — and is off limits with the page; the
scan lists it and the whole of `tools/atlas/` is named among the exclusions. This README and
`build.py` carry none. (An earlier revision of this paragraph said `verdicts.json` carried no
values. It did; found on 2026-09-20 during the language pass.)

`docs/briefs/2026-09-19-genome-track-handover.md` §6 lists what is excluded regardless of the
scan. `atlas.html` belongs on that list and is not there yet — that edit is the owner's to make.
