# connectome-seed — a lineage of artificial organisms grown from a real connectome

Grow a lineage of artificial organisms from a real fly connectome — "to learn to make an elephant
out of a fly". The first step is writing down the "genome": the heritable grammar that generates
the wiring instead of copying it. The five points of the idea are in [idea.md](idea.md).

## The goal, in the owner's own words

The goal is not a paraphrase and does not have to be reconstructed from discussion: it is in this
repository, verbatim and dated, as [idea.md](idea.md) (English; the Russian original of 2026-09-12 is in git history at
`2488ecb`). Mike Shevchenko, author, 2026-09-12 12:18. Restated by him
in one line as the project's description on 2026-09-19: **"to learn to make an elephant out of a
fly"** (translated from Russian). The two say the same thing: the idea opens with **"Not
'emulate a fly and call it an elephant', but grow a lineage of creatures from a real
connectome-seed"**, and the restatement promotes that distinction from a disclaimer to the goal.

It is five points, an artefact, and a named first step. All five are the goal; none of them is a
later addition.

1. **The seed is a heritable grammar, not all the weights** — neuron types, E/I balance, recurring
   graph motifs, sensory and motor circuits. "This is the first genome, not a cemented brain."
2. **Body and brain grow together** — the genome says which segments, joints and sensors the body
   has and how neuromodules are duplicated, connected and specialised. **Not a "fly → elephant"
   jump, but a curriculum:** fly → beetle → six-legged truck → small quadruped → heavy quadruped.
3. **USPEX operations, on a living graph** — heredity of working brain and body modules from two
   ancestors; softmutation where the controller is plastic rather than random axon-cutting;
   permutation of a module's role, type or sensory channel; random embryos and a diversity archive.
4. **A short "youth" before fitness is measured** — limited plasticity in several safe worlds, and
   only then the measurement: "we evaluate not the raw embryo, but what it stably settles into."
5. **Multi-objective fitness on a held-out set of arenas** — energy, stability, speed, recovery
   after a broken sensor or joint, novelty, transfer to unseen terrain; the arenas are held out
   "otherwise the winner is whoever found a hole in MuJoCo".

**The main artefact is not a single elephant video, but an evolutionary tree:** which mutation
appeared, which module was inherited from the fly, what grew, where a line broke, and which skills
survived the change of body.

**The first step is the author's own, and it is the one open now.** From the same message: *"the
most interesting next step, in my view, is formalising the representation of the genome (exactly
how the heritable grammar of modules and growth rules is written down). Almost everything else
depends on it."* That is point 1, and it is the track being worked on — see
[ROADMAP.md](ROADMAP.md) § "The grammar track". It is the first point, not the whole goal: points 2,
3 and 5 are designed for and not run, and nothing is grown until the condition below has a number.

**What the elephant means, operationally.** An elephant is not a bigger fly: more cells of the same
types is a lattice parameter, it does not add types, motifs or knobs, and the wiring is given to us
rather than produced. An elephant is a rule that *generates* the wiring — more cell types and
specific connections between them. Measured against that test, what we run on today holds a single
production over a lookup table that is not generative, and an individual is an initial condition on
wiring identical in every individual — not a genome in the generative sense
([docs/notes/2026-09-20-what-is-the-genome-here.md](docs/notes/2026-09-20-what-is-the-genome-here.md)).

## Where things stand

The current state of the condition is in [ADR-002](docs/decisions/002-file-under-condition.md)
§ "Status of the condition"; the only status that is not typed by hand is the generated block at
the bottom of [ROADMAP.md](ROADMAP.md). No result value appears here — where a finding is
numerical, the file that carries the number is named. The condition itself ("show that a cheap
evaluation of an individual is consistent with an expensive one") is stated in the
[origin file](docs/history/2026-09-13-origin.md).

The main findings, each as the question it answers and the file that carries it:

- **Rule #1 on the C6 exam** (does a first regenerating rule pass the C6 exam?) — [RESULT](results/genome/c6/rule_runs/first_rule_k12/RESULT.md), 2026-09-23.
- **Rule #2.1 on the C6 exam** (does the second rule pass P1–P4?) — [note](docs/notes/2026-09-23-rule-2-1-c6-what-it-showed.md), 2026-09-23.
- **BF_1 alone on P3** (does one rank-1 term separate the real bank from shuffles?) — [note](docs/notes/2026-09-24-bf1-p3-what-it-showed.md), 2026-09-24.
- **A second brain, FlyWire, on P3** (does the same test hold on another fly's wiring?) — [note](docs/notes/2026-09-24-flywire-p3-what-it-showed.md), 2026-09-24.
- **Knock out and regrow, block A** (does a rule regrow a removed 64-cell block it was not shown?) — [RESULT](results/genome/c6/checks/knockout_regrow/RESULT.md), 2026-09-26.
- **Knock out and regrow, block B** (the same question for a second, 40-cell block) — [RESULT](results/genome/c6/checks/knockout_regrow_block_b/RESULT.md), 2026-09-28; reading under review: [block B notes](results/genome/c6/checks/knockout_regrow_block_b/READING_NOTES.md) §1, §7, §9 carry it; the λ continuation is in [replication notes](results/genome/c6/checks/natural_fit_failure_replication/READING_NOTES.md) §6.
- **Failed-fit branch calibration** (can the reading tell a failed fit from a rank limit?) — [CALIBRATION](results/genome/c6/checks/failed_fit_calibration/CALIBRATION.md), 2026-09-29.
- **Natural fit-failure replication** (does the failed fit recur on fresh boards?) — [REPLICATION](results/genome/c6/checks/natural_fit_failure_replication/REPLICATION.md), [notes](results/genome/c6/checks/natural_fit_failure_replication/READING_NOTES.md), 2026-09-29.
- **Rule #2.1 on the real block B at a fixed λ = 1** (was B's failure the λ choice or a limit of the rule?) — [RESULT](results/genome/c6/checks/block_b_ceil1/RESULT.md), [review record](results/genome/c6/checks/block_b_ceil1/BLIND_REVIEW.md), 2026-09-30.
- **The symmetric λ pair** (do blocks A and B differ when both are read at the same λ?) — [RESULT](results/genome/c6/checks/symmetric_lambda_pair/RESULT.md), [blind review](results/genome/c6/checks/symmetric_lambda_pair/BLIND_REVIEW_raw.md), 2026-09-30.
- **GPU instrument** (a separate, faster fitter for the synthetic worlds) — [README](results/genome/c6/gpu_instrument/README.md), 2026-09-26.

## Map of the repository

| Path | What is there | Where it lives |
|---|---|---|
| `GLOSSARY.md` | one meaning per term, with the file that defines it | repo |
| `LICENSE` | CC BY 4.0 | repo |
| `ROADMAP.md` | phases ordered by what blocks them; generated status block at the bottom | repo |
| `VISION.md` | what we are trying to find out, and why | repo |
| `idea.md` | the owner's five points, verbatim, in English | repo |
| `literature.md` | every source, how it was verified, numbers and quotes | repo |
| `atlas.html` | one self-contained page of where the project is, built by `tools/atlas/build.py` | gitignored (regenerated) |
| `backlog.md`, `backlog_closed.md` | open and closed tasks; edited only through the shared backlog tool of dpc-messenger, never by hand | repo |
| `backlog.html`, `graph.html`, `graph.json` | board view, entry graph and its data, built from `backlog.md` | gitignored (regenerated) |
| `chat/` | the group-chat thread, one file per message | gitignored, local only |
| `docs/` | `plans/` registrations, `notes/` what each run showed, `decisions/` ADRs, `briefs/` handovers, `experiments/` and `retrospectives/` records, `prereg-scripts/` scripts committed before a reading, `proposals/` design proposals, `history/` moved-out old text | repo |
| `research/` | notes imported from Ark's sandbox (AlphaGenome atlas, the cheap-step analysis, USPEX analogue) | repo |
| `results/` | committed run outputs: `night1`–`night6` (measurement line), `genome/` (the C6 exam, rules, checks, GPU instrument), `diagnostics/` | repo |
| `sources/` | two full-text source copies and the open-access Shuvaev PDF; `sources/local/` holds copies with no redistribution licence | repo; `sources/local/` gitignored |
| `tools/` | `atlas/` page builder, `night/` overnight run launcher, `reachability/` and `viz/` (reading harness; Blender explanatory figures and film), `contamination_scan.py`, `venv_manifest.py`, `.venv/` | repo; `.venv/` and raw `night/` logs gitignored |
| `.claude/` | agents' working trees: a second copy of the tree; searches of the repo must exclude it | excluded locally (`.git/info/exclude`), never committed |
| `../connectome-seed-data/` | raw connectomes (FlyWire, Hemibrain, Janelia male CNS), Sintel data, raw outputs of runs, renderings | outside the repo |

## How to read a result

- **Predictions are committed before the run**, in a separate commit — once they sat uncommitted in the working tree, and once a reviewer's criterion arrived during writing and was missed.
- **Every load-bearing number has a carrier file and a pinned hash** of its inputs and registration — a number without a carrier cannot be checked.
- **A post-data registration says "not blind to X" in its first line, and the blind review is separate** — post-data readings were once read as blind.

## How to run

- Python is `tools/.venv/Scripts/python.exe` (Windows); scripts run from the repository root.
- Set `PYTHONUTF8=1` — a cp1252 console encoding once killed a registered run.
- Raw data and raw run outputs are in `../connectome-seed-data/`, not in the repo.

## Read next

[GLOSSARY.md](GLOSSARY.md) · [ROADMAP.md](ROADMAP.md) · [VISION.md](VISION.md) · [docs/CHECKLIST-research-repo.md](docs/CHECKLIST-research-repo.md) · [docs/history/2026-09-13-origin.md](docs/history/2026-09-13-origin.md) — the origin day: readers' findings with names and timestamps, the condition, the literature answer.

## Licence

This repository is licensed under the Creative Commons Attribution 4.0 International License
(CC BY 4.0, [LICENSE](LICENSE)); attribution is required as "Mike Shevchenko, DPC Research —
https://github.com/mikhashev/". The PDF in `sources/` carries its own CC BY 4.0 attribution
to its authors (Shuvaev et al., PNAS 2024), stated on its first page.
