# atlas — one page that says where the project is

`build.py` reads what already exists in machine-readable form in this repository and writes a
single self-contained file, `atlas.html`, at the repository root: inline CSS, inline JS, inline
JSON, no CDN, no fonts, no network. It opens from `file://`. The reader is the owner, not a
specialist; the UI text is Russian and technical identifiers are left as they are.

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
| A «Где мы сейчас» | `verdicts.json` (sourced from `VISION.md`, experiment 005) + `git log` / `git status` / `git rev-list` |
| B «Ждёт слова Mike» | open `backlog.md` entries whose envelope or body says *Mike's word* / *Mike decides*, or that `verdicts.json` flags `awaits_mike: true`; plus the uncommitted-file and unpushed-commit counts from git |
| C «Лента ночей» | `results/night*/wave_*.json`, `results/night*/*.slim.json`, `results/night*/*killed*.json`, `docs/experiments/00N-*.md` |
| D «Мухи» | `results/night5/run_columns.csv` — the explicit run → column → seed → role mapping |
| E «Кривые обучения» | `results/night5/night_report_checkpoints.csv`, columns resolved through `run_columns.csv`; the second chart from `results/night5/diagnostics/rowB/penalised_quantity_by_checkpoint.csv` |
| F «Приборы и контроли» | each diagnostic directory's `*controls*.json` / `*readings*.json`, counting boolean `pass` fields; links to each instrument's README |
| G «Борд» / «Решения» | `backlog.md`, `backlog_closed.md`, `docs/decisions/*.md` front matter |
| H «Последние события» | `git log -15` |

**Run identity is never derived from a column name.** `run_columns.csv` says why: the prime
marks count marks, not order. The page shows the recorded `run_id` and builds its human label
from the recorded `seed` and `run_index_for_seed`.

**Numbers are shown as recorded.** Nothing is re-estimated. The script computes only counts,
dates, durations and the axis bounds a chart needs.

**Anything that cannot be parsed becomes a hatched card naming the file, never a guess.** The
hatch labels are `не измерено`, `не объяснено`, `ещё не прочитано` and `источник не разобран`,
and each one says which file it is about. Several older controls files record their controls as
differences rather than as boolean `pass` fields; those tiles hatch `не измерено` on purpose.

## Adding a verdict

`verdicts.json` holds the plain-language texts, keyed by card id. A card with no entry renders a
hatched `не объяснено` block, so the debt is visible on the page rather than hidden.

```json
"diag:connectivity": {
  "text": "Одно-два предложения обычным языком.",
  "source": ["results/night2/diagnostics/connectivity/README.md"]
}
```

Card ids: `where_we_are`, `flies`, `curves`, `penalised`, `board`, `night1`…`night5`, and
`diag:<id>` for each tile in `DIAGNOSTICS` in `build.py`. `build.py --check` prints every card
that is still without a verdict. A backlog entry's NAME can also be used as a key, with
`"awaits_mike": true`, to put that entry into section B when its text does not carry the phrase.

## Translating a board entry

Sections B and G show board entries. The entries themselves are English; the reader is not.
`verdicts.json` → `backlog_ru`, keyed by the entry's NAME, holds the Russian restatement and the
decision being asked for. An entry with no Russian text shows its English sentence under a
hatched `не переведено` label, so that debt is visible too.

```json
"backlog_ru": {
  "SOME-ENTRY-NAME": {
    "text": "Что записано, своими словами, без смягчения.",
    "ask": "Какое решение нужно — вопросом, на который можно ответить словом.",
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
screen, which is the densest single leak in the repository. `verdicts.json` and this README
carry no measured values and stay readable; `build.py` carries none either.

`docs/briefs/2026-09-19-genome-track-handover.md` §6 lists what is excluded regardless of the
scan. `atlas.html` belongs on that list and is not there yet — that edit is the owner's to make.
