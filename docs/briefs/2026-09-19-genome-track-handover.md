# Handover — the genome track, for a session that starts fresh

**Written:** 2026-09-19 UTC, by CC, on Mike's word ("давай в новой сессии это сделаем, начни
подготовку"). **Nothing here needs a GPU** and nothing here is blocked by the nightly accrual.

This file exists so a new session can start working without reading a two-day chat thread.
It states what the track is, who owns which piece, what is actually blocked, and — separately
and deliberately — one thing a new session must **not** read if it is to do the other job that
is waiting.

---

## 1. The track in one paragraph

The nights measure a single number per run: aggregate held-out loss. Everything the project
has argued about for two days — whether individuals can be ranked, whether a cheap early
estimate predicts a dear late one — is downstream of that one number, and it has now been
measured to be as noisy between two copies of one individual as it is between six different
individuals (`docs/experiments/005-night5-third-runs-of-seed-0-and-seed-3.md`). The genome
track asks a different question on the same runs: **what actually differs between two
individuals**, in the 65 cell-type biases that are the only thing a seed moves, and what that
difference does downstream. It is a readout question, not a training question, so it runs on
checkpoints already on disk.

## 2. Who owns what

| piece | owner | state |
|---|---|---|
| Design around S2, with label provenance | Ark | not started; the design is the deliverable, not code |
| The two-page note "what is the genome here" | **CC** | not started |
| C6 control specification | Zcode | not started, and **not blocked by anything** |
| Extraction of the field list | CC | **blocked**: waits on Ark's design naming the fields |

Sources: `docs/plans/2026-09-16-functional-readout-plan.md` § "Step 3 — genome", and
`ROADMAP.md` under "Diagnostics while N accrues — the functional-readout track".

**Only one item is blocked**, and it is the extraction. The design, the note and the C6 spec
can all start now, in parallel with each other.

## 3. What the track can already stand on

- **The 65 biases are the whole of individuality, and this is a read rather than an
  inference.** `network.node_config.bias.seed` is the only seeded network parameter;
  `bias.yaml` has `groupby: [type]`, `initial_dist: Normal`, `mode: sample`, while
  `syn_count` is `mode: mean` and `syn_strength` is `initial_dist: Value` — both
  deterministic, so the seed cannot move them. The connectome definition
  `flyvis/connectome/fib25-fib19_v2.2.json` lists 65 nodes, each with its own `bias`. All of
  it is visible in the runs' own committed `resolved_config_yaml` as well: the varying `seed`
  line sits inside the `node_config.bias` block, four lines above `penalize: {activity: true}`,
  while the invariant `seed: 0` beside `n_folds`/`fold` is the data-split seed.
- **Those same 65 parameters are actively pulled toward a common level for the first 60 % of
  training.** `activity_penalty` acts on `nodes_bias` and on nothing else, with
  `stop_iter = 150000` against `n_iters = 250000`. The penalty is one term with two asymmetry
  weights, not two families: `asymmetric_weighting(x, γ, δ) = γ·relu(x) − δ·relu(−x)` applied
  to `baseline − mean_activity`, then squared, with below-baseline weighted 1.0 and
  above-baseline 0.1.
- **The knob is reachable without a code change**, which matters if the design wants a
  contrast: `--override penalizer.activity_penalty.stop_iter=N` on `run_individual.py`,
  verified by composing the config (0 and 250000 both take). See §5 for what it costs.
- **Ten runs are on disk**, six individuals and two of them with three runs each:
  `results/night1` … `results/night5`, and the ten-run checkpoint table at
  `results/night5/night_report_checkpoints.csv`.

## 4. What a new session should read, in order

1. `docs/plans/2026-09-16-functional-readout-plan.md` § "Step 3 — genome" — the design brief.
2. `docs/experiments/005-night5-third-runs-of-seed-0-and-seed-3.md` — the state of the loss
   side, and why the genome question is not a detour from it.
3. `backlog.md` — in particular the entry on the cheap and the dear estimate being taken under
   different regularisation, which is the same 150,000 boundary.
4. `docs/CHECKLIST-research-repo.md` and `docs/BACKLOG_FORMAT.md` (the latter in
   `dpc-messenger`) — how this repository expects records to be written.

## 5. The one decision this track will run into, stated now so it is not discovered late

If the design asks "does the activity penalty cause the weak coupling between the cheap and
the dear estimate", the direct experiment is a pair of runs with `stop_iter` set to 0 and to
250000. **That is a new series, not a fix**: all ten runs on record carry
`stop_iter: 150000` as an invariant config line, and gate 7
(`tools/night/config_invariants.py`) refuses a run whose invariant lines differ — its negative
control was built on this very key, moving 150000 to 200000 and catching it. So such runs
would be comparable to each other and to nothing we have.

The cheap version of the same question needs no GPU at all: the 65-bias profiles of the twins
are on the checkpoints already, before and after 150,000.

## 6. What a new session must NOT read, if it is to be the blind author

Separate job, separate constraint. Ark and Zcode have asked that the **v2 registration of the
reachability endpoint** be written by someone who has not seen v1's numbers, because a rule
chosen after seeing them cannot be signed by anyone who saw them, and all three of us have.
A session that takes that job must not read:

- `results/diagnostics/reachability/` — the v1 reading's stdout and JSON;
- the DPC Research group chat from 2026-09-18 onward;
- §2 and §3 of `docs/experiments/005-...md` above.

**These two jobs are therefore not for the same session.** The genome track above is safe to
read everything; the v2 author is not. Whoever starts, say which of the two they are before
they read anything.
