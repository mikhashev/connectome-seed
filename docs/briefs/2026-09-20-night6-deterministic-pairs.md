# Brief — night 6: two deterministic pairs (same seed twice, and two different seeds)

**v1, 2026-09-20 (UTC). Draft. Launch requires Mike's explicit word, and one of the four
compositions in §6 has to be chosen by him before any command is typed — the measured cost of
deterministic training makes the authorised shape ("a night with two deterministic pairs")
impossible in one night, and that is this brief's first finding rather than a footnote.**

Written by: CC, for review by Ark and Zcode, then Mike. All timestamps UTC. No local times.

This file registers what night 6 measures and what gates it, before any full run exists. It does
not launch anything and does not schedule itself (§9). It mirrors the form of
`docs/briefs/2026-09-17-night5.md`: pre-flight, composition, pre-registered reading, gates, void
conditions, cost, boundaries.

**What is already measured, before the night — and what it changed.** Five things were measured
on 2026-09-20 and are reported in §3a, §5 and §6 rather than assumed:

1. **Deterministic training costs 3.33× the s/iter of the mode nights 1–5 ran in**, measured back
   to back on this machine within four minutes. A single 250,000-iteration deterministic run is
   about **13.4 hours**; three of them are about **40 hours**. The night the owner authorised does
   not fit in a night.
2. **No operator refuses.** `nondeterministic_ops` is empty over 600 deterministic training
   iterations including the backward pass and one held-out evaluation. Nothing was switched to
   `warn_only` to make that true — see §5.2, which is about a flag that was already set.
3. **Gate 7 is blind to this night's one distinguishing property**, and that was established by
   running it, not by reading it (§7, gate 7). A new gate 7b is registered here.
4. **Control (a) passes at 2,000 iterations: bitwise identical**, 89 of 89 checkpoint tensors and
   all 14 logged arrays, with the checkpoint's wall-clock `time` string the only difference
   anywhere in the comparison (§5.3). That is the answer to (a) at short horizon, and §5.3 states
   exactly how far it reaches.
5. **Held-out loss is the wrong channel to read this night in alone.** The row B profile reading
   that came back the same day finds the individual, where it finds it at all, in the *shape* of
   the 65-type activity profile and not in a scalar. A second readout is therefore registered for
   both (a) and (b) (§3a), together with what `rowB.py` needs before it can address night-6
   directories — which a `--netdir` call alone does not supply.

## 0. Before you launch — run the pre-flight, do not recall it

Night 5's pre-flight is reused as written, with the four parameters it already takes:

```
powershell -ExecutionPolicy Bypass -File tools\night\preflight_night5.ps1 -Ensemble 9994 -Tag night6
```

Exit 0 means every check passed; **exit 1 means the night must not start**; exit 2 means something
needs a human decision. Nothing in it starts anything.

**Two of its checks will behave differently for night 6, and both are decisions rather than
defects.**

- **Its check 1 (GPU memory ≤ 6,000 MiB) will REFUSE, and it is right to refuse and wrong to be
  obeyed here.** `llama-server.exe` holds about 25 GiB of the 32,623 MiB card and must not be
  stopped (standing instruction, 2026-09-20). The band that check enforces was calibrated when the
  card was free. **What was never available to night 5 and is available now is a measurement of
  what that resident process costs this workload: nothing detectable.** Normal-mode training
  measured today with `llama-server` resident runs at **0.0658 s/iter**, inside the 0.0640–0.0672
  band night 5 records for the first 5,000 iterations of all eight runs then on disk
  (`docs/briefs/2026-09-17-night5.md` §4.4). So the refusal must be overridden deliberately by the
  owner, on that measurement, and the override recorded in the night's record — not silenced by
  editing the pre-flight.
- **Its check 2** looks for `<ensemble>/000` and `<ensemble>/003`. Night 6 also uses
  `<ensemble>/900`, which check 2 does not know about; §4 below states the three directories that
  must be absent and the operator checks the third by hand until a night-6 pre-flight exists.
- **Its check 7** dry-runs night 5's own two-job command; it will not match night 6's command. The
  night-6 dry runs are pasted in §8 and were executed from the repository on 2026-09-20.

## 1. The question, as the team stated it

Replicates of one individual are copies of one config down to the last field: identical at
iteration 0 to the last printed digit, already different by iteration 12 by less than one float32
step, and by the end separated by as much as different individuals are. All five nights ran with
`--no-determinism` (`tools/night/start_night.ps1` passed it unconditionally until the switch added
for this night; `tools/night/run_individual.py:285-302` sets `cudnn.deterministic` and
`torch.use_deterministic_algorithms` from it). The replicate gap is therefore produced by GPU
operation order, and the backlog entry
`NON-DETERMINISM-IN-TRAINING-MAY-BE-THE-SOURCE-OF-THE-REPLICATE-GAP` names the candidate. Night 6
asks two things, both in **deterministic** training:

- **(a) CONTROL — the same seed twice.** Are the two trajectories bit-identical on the *training*
  path? Bitwise identity was shown for *evaluation* (30/30 pairs and 3/3 fresh processes,
  `results/night5/diagnostics/rowB/rowB_controls_det.json` and the three
  `rowB_controls_floor_proc*_det.json`). It has never been measured for training.
- **(b) THE QUESTION — two different seeds.** Do they separate, and by how much compared with the
  replicate gap of nights 1–5? If different seeds still separate while same-seed runs are
  identical, a seed does define an individual and the ranking question becomes answerable. If two
  different seeds end as close as the old replicates were, "individual" is not defined by the seed
  on this axis.

## 2. The trap, named in advance by Ark, and how this night's reading avoids it

**With determinism on, σ_rep is exactly zero.** The ADR-002 ratio (between-individual spread over
replicate spread) then goes to infinity and its condition is "met" — vacuously. **The denominator
vanished; it did not shrink.** A night read that way would ratify the method instead of testing
it, and would do so by comparing a training run that no longer resembles the nights on record
against a spread measured under the old setting.

**Registered here, before any full run exists:**

- **The ADR-002 ratio is not computed for night 6, in any form, at any rung.** Not as a number, not
  as "large", not as "passes". Any later text that quotes a night-6 ratio is quoting something this
  brief forbids.
- **(b) is read as a comparison of two measured quantities and against a systematic reference**:
  the deterministic between-seed separation, reported beside the replicate gap recorded in
  `docs/experiments/005-night5-third-runs-of-seed-0-and-seed-3.md` §2, and beside a **systematic**
  perturbation of the same class. Both comparisons are cross-setting — deterministic against
  normal-mode — and that is stated in the reading rather than hidden by it (§3, "what (b) cannot
  say").
- **The 2×2 "bias-only / order-only" design is the systematic comparison, and it is NOT part of
  this night.** It is recorded in `docs/next-session-plan.md` ("2×2 refinement (Ark 08:28)"), it
  needs a second script argument — one `--seed` currently feeds both
  `network.node_config.bias.seed` and the global RNGs — and therefore a new registration. Night 6
  does not run it, does not prepare it, and does not pre-empt its reading.
- **N = 2 seeds is an existence check, not a test.** One difference between two individuals. No
  p-value, no standard deviation, no degrees-of-freedom arithmetic, no pooling with the ten
  normal-mode runs. Night 5's gates 9 and 10, which exist to police exactly that kind of
  arithmetic, do not apply because night 6 computes none of it (§7).

## 3. Composition

**One ensemble, `9994`, which has never been used.** The directory listing of
`connectome-seed-data/results/flow` on 2026-09-20 holds `9983`–`9992` and `9995`–`9999`; `9993`
was taken by this brief's own probe and control (§5), so `9994` is the first free id and the night
takes it. `run_individual.py:375-382` refuses to start on an existing network dir (exit 2, "nothing
deleted"), so a collision cannot overwrite anything — but it would kill a job hours in, which is
why the id is chosen here and checked in §4.

**Seeds 0 and 3, because they are the two individuals with the most normal-mode data on record** —
three runs each (`docs/experiments/005-…` §2). Whatever night 6's two seeds do in deterministic
mode is therefore read against the richest normal-mode reference this project has.

| position | label | seed | id | tag | determinism | role |
|---|---|---|---|---|---|---|
| 1st | `A1` | 0 | `9994/000` | `night6` | **ON** | the reference run of pair (a) and of pair (b) |
| 2nd | `A2` | 0 | `9994/900` | `night6` | **ON** | the repeat of `A1`; pair (a) = `A1`/`A2` |
| 3rd | `B` | 3 | `9994/003` | `night6` | **ON** | the different seed; pair (b) = `A1`/`B`, and `A2`/`B` for free |

**Three runs, not four — and the third pair is free.** Pair (a) is `A1`/`A2`; pair (b) is `A1`/`B`;
`A2`/`B` costs nothing and is reported. A fourth run buys a fourth pair that is determined by the
other three.

**`A2` takes the `9xx` id and keeps the wave's tag, and this reverses night 5's choice on purpose.**
Night 5 refused `--replicate-of` because it hard-codes both the `9xx` id and `tag="rep"`
(`launch_wave.py:108`), and because `9xx` "distinguishes *a* replicate from an original and has no
way to say *which* repeat" — seed 3 was then getting its **third** run. Here seed 0 gets exactly
**two** runs in ensemble 9994, and `A2` is a replicate of `A1` in the strictest sense the
repository has ever used the word: same seed, same config, same horizon, deterministic. So `9994/900`
says what is true. The tag objection is a real one and was fixed rather than paid: a
`--replicate-tag` option was added to `launch_wave.py` (§8) so the wave writes one file prefix,
`night6_9994-000.*`, `night6_9994-900.*`, `night6_9994-003.*`, and a collector keyed on the tag or
on the ensemble sees all three.

**Order: `A1`, `A2`, `B`.** A night can fail to reach its last run. `A1`+`A2` is pair (a), which is
the one this night can *settle*; `B` alone settles nothing. Under either composition of §6 the
launcher places the replicate-of job immediately after its own seed's job
(`launch_wave.py:113-115`), which is this order, verified by the dry run in §8 and not read off the
code.

**What (b) cannot say, written before the number exists.** Pair (b) compares a deterministic
between-seed separation against a normal-mode replicate gap. Those are two settings. A large
separation therefore licenses "under determinism, two seeds separate by more than the old
replicates did" and nothing stronger — in particular it does not license any statement about
whether the *normal-mode* ranking failure was caused by operation order. That question needs the
systematic arm, which is not this night.

## 3a. The second readout — the row B activity profile, not only a scalar

**Added 2026-09-20, after the row B profile reading came back and before any night-6 run
exists.** The finding is recorded in `results/night5/diagnostics/rowB/PROFILES-READING.md` (§2,
§2a and §6; values are not copied here, so that this brief stays off the blind-author exclusion
list). In one sentence, and with no number: **before training, replicates of one seed have
identical 65-type activity profiles; at the end of training replicates are closer to each other
than to their nearest foreign run by profile SHAPE (`1 − Spearman ρ` over the 65 types) in nearly
all twin pairs, but NOT by profile MAGNITUDE (Euclidean), and not by held-out loss.** The reading's
own verdict under its §0(h) rule is **MIXED**, and that is what it is cited as.

**The consequence for night 6, stated before the night rather than after it: an individual, if it
exists on this substrate, shows in the shape of the profile rather than in a scalar.** A night that
reads only held-out loss would therefore be reading the one channel in which nights 1–5 found
nothing, and would return "no individual" by construction. So a second readout is registered
alongside held-out loss, for **both** (a) and (b).

**The instrument** is `results/night5/diagnostics/rowB/rowB.py` in its record mode —
`--deterministic`, `--reduce-on gpu` — the same mode whose evaluator floor `rowB_floor_det.json`
records as **exactly zero** on both quantities across three fresh processes (§1 of the reading).
Taken on night 6's own checkpoints.

**The quantities and the distances, both pre-declared, neither preferred, never merged** — the
same pair `PROFILES-READING.md` §0(c)/§0(d) fixes, reused verbatim so that night 6's numbers land
in the same table as nights 1–5's:

| | quantity | distance forms |
|---|---|---|
| primary | `mean_by_type`, aggregated over the 16 held-out items → a 65-vector per run per checkpoint | **Euclidean** on the raw 65-vectors *and* **`1 − Spearman ρ`** across the 65 types |
| secondary | `central_cell_mean_skip_first_quarter` — the penalty's own reduction | the same two |

**Checkpoint indices:** **0**, **8**, the **last before** and the **first after** 150,000, and
**71** — `PROFILES-READING.md` §0(f)'s five. Under designs α and β only indices 0 and 8 exist
(§6); under γ and δ the full-length runs carry all five and `A2` carries 0 and 8. **If the two
distance forms disagree, the disagreement is the result** and is reported as MIXED, exactly as the
night-5 reading reports it; neither form is promoted to tie-breaker after the fact.

**Registered reading of (a) on this readout.** Same seed twice, deterministic training → **the two
runs' profiles are identical at every tabulated checkpoint: distance exactly 0, both quantities,
both forms.** Pass/fail, no tolerance — which is meaningful here only because the deterministic
*evaluator* floor is itself exactly zero, so a nonzero distance cannot be the evaluator wandering.
**Checkpoint 0 carries no information for (a)**: nights 1–5 already give exactly 0 there for every
twin pair, deterministic training or not, because replicates share their initialisation. The
informative checkpoints are the trained ones.

**Registered reading of (b) on this readout.** Two different seeds → report `A1`–`B`'s profile
distance in **both** forms and **both** quantities, at each reachable index, **beside** the twin
distances and the nearest-foreign distances recorded for nights 1–5 in `PROFILES-READING.md` §2
(cited, not restated). Pre-stated meanings, fixed now:

- **Different seeds separated in SHAPE while same-seed runs are exactly identical** → the seed
  defines an individual, **in shape** — and only in shape, since magnitude and held-out loss are
  the two channels the night-5 reading found it absent from.
- **Different seeds as close in shape as same-seed replicates were in nights 1–5** → it does not.
- **The two forms disagree** → MIXED, reported with the checkpoint and quantity named, no threshold
  invented afterwards to resolve it.

**The vacuity trap applies here too, one level in.** With (a) exactly zero, *any* nonzero (b)
distance is infinitely larger than the same-seed distance — the same vanished denominator as §2's
σ_rep, in the profile channel. **So (b) on this readout is read against the nights 1–5 twin and
nearest-foreign distances, never against night 6's own zero, and no ratio of the two is computed.**

**N stays explicit: two seeds is an existence check, not a test.** One pair of individuals. The
night-5 reading is already marked `readable_as_verdict: false` at six individuals, against
`docs/next-session-plan.md` §5's floor of "do not read row B as a test at N < 8"; night 6 is at
**two** and is further from that floor, not nearer it. No p-value, no significance language, no
threshold.

### What rowB.py needs in order to address night-6 netdirs — checked, not assumed

**A `--netdir` call alone does NOT suffice.** `rowB.py` resolves *every* run through
`results/night5/run_columns.csv`, including the `--netdir` path: `select_runs` looks the directory
up in the registry that `read_run_columns` builds from that csv and raises
`Refusal("--netdir ... is not in run_columns.csv")` when it is not there. `9994/000`, `9994/900`
and `9994/003` are not there, so the call fails before any checkpoint is opened. **I have not
modified `rowB.py` and have not touched `run_columns.csv`** — both are under `results/night5/`.

Three facts settle what the fix has to look like, all read from the script:

1. **The 72-checkpoint refusal is not the obstacle.** `check_run_complete` is applied **only**
   under `--night all10`; on the `--netdir` path the script merely counts the checkpoint files. So
   a night-6 run stopped after 26,000 iterations, with nine checkpoints instead of seventy-two, is
   not refused on that ground.
2. **`check_netdir_unambiguous` does run on the `--netdir` path**, and the three night-6
   directories satisfy it: each name equals its run-id leaf and no prefix sibling exists under
   `9994/`.
3. **Simply adding the three night-6 rows to `results/night5/run_columns.csv` would break the
   nights 1–5 scope.** `select_ten` asserts that the csv's run set is *exactly* its hard-coded ten
   ids — "a run added or dropped changes N and must be a stop, not a different answer" — so
   `--night all10` would begin refusing with exit 3. The guard is working as designed; it simply
   means the night-6 registry cannot be that file.

**The change that is needed, described and left to the coordinator:** give `rowB.py` an additive
`--run-columns PATH` (default: the night-5 csv, so every existing call is unchanged), and put
night 6's three rows in a new `results/night6/run_columns.csv` in the same column form. `select_ten`
and `TEN_RUN_IDS` then keep guarding `--night all10` against the night-5 csv exactly as today.
Two smaller points belong with that decision: a copy of `rowB.py` under `results/night6/` would
create a second source of truth for the instrument, which is the defect this repository has
corrected twice, so the one script should stay where it is and gain the argument; and the record's
`instrument_stack.json` should be re-taken for night 6, because the profile values are only
comparable on the recorded driver and library stack.

## 4. The three output coordinates must be absent before launch

`9994/000`, `9994/900`, `9994/003` under
`C:\Users\mikha\Documents\dpc-research\connectome-seed-data\results\flow\`. Night 5's pre-flight
checks only `000` and `003` for the ensemble it is given; **`900` is checked by hand** until a
night-6 pre-flight exists. A collision is refused per run, so a collision on the *third* job kills
only that job — after the first two have already been spent.

## 5. What was measured before this brief was written

All of it on 2026-09-20, ensemble **9993**, into the session scratchpad, with `--n-iters 250000`
unchanged and `--stop-after-iter` used so that the learning-rate schedule and the epoch count stay
the night runs' (`run_individual.py:95-99`).

**Ensemble 9993 is now consumed** and is not the night's: four network directories exist under the
data root — `9993/000` (deterministic probe), `9993/001` (normal-mode probe), `9993/010` and
`9993/011` (the control pair). They are scratch, and the owner may delete them; nothing in the
night reads them. The night takes **9994** (§3).

The distilled record is committed under `results/night6/`: `probe_speed.json` (§5.1, both probe
runs' argv, timings, determinism blocks, `nondeterministic_ops`, VRAM and the measured ratio),
`control_a_runs.json` (§5.3, both control runs' argv, rung and checkpoint metrics, determinism
blocks), `control_a_bitwise.json` (the comparison report) and `compare_bitwise.py` (the comparison
itself, so the reading is a script and not a description). The raw jsons and logs stay in the
scratchpad.

### 5.1 Feasibility probe: deterministic training costs 3.33×

Two runs of seed 0, 600 completed iterations each, back to back within four minutes, identical in
everything but the determinism flag.

| | id | tag | s/iter, median of iterations 100–600 | s/iter, median of all 600 | first iteration | torch peak |
|---|---|---|---|---|---|---|
| determinism **ON** | `9993/000` | `night6probe` | **0.219134** | 0.218915 | 0.4454 s | 1470.9 MiB |
| determinism off | `9993/001` | `night6probenorm` | **0.065762** | 0.065666 | 0.1822 s | 1426.1 MiB |

**Ratio 3.332.** The normal-mode figure is the control that makes that ratio mean "determinism"
rather than "the card is busy": 0.0658 sits inside the **0.0640–0.0672** band night 5 records for
the first 5,000 iterations of every run then on disk (`docs/briefs/2026-09-17-night5.md` §4.4),
**with `llama-server` resident throughout**. Determinism also costs 44.8 MiB of extra peak
allocation, which is the `CUBLAS_WORKSPACE_CONFIG=:4096:8` workspace.

`nvidia-smi` read 25,589 MiB of 32,623 in use before the probe and 26,994 MiB during it, so one run
adds about **1,405 MiB** to the driver's view and about **7.0 GiB** was free.

### 5.2 No operator refuses — and the flag this is measured under

`nondeterministic_ops` is **empty** for both probe runs: no operator emitted "does not have a
deterministic implementation" in the forward pass, the backward pass, or the held-out evaluation at
iteration 600.

**`run_individual.py:295` already calls `torch.use_deterministic_algorithms(True, warn_only=True)`,
and has since the script was written.** This brief did not choose that, did not switch to it, and
states it plainly because a warn-only run is not in general a deterministic run: under `warn_only`
an operator with no deterministic implementation *warns and proceeds non-deterministically*. What
makes it harmless here is measured rather than argued — **nothing warned.** The training graph is
fixed (`cudnn.benchmark = False`, no autotuning, the same ops every iteration), so an operator that
would refuse would have refused in the first 600 iterations. On this graph `warn_only=True` and
strict mode are therefore the same run, and the empty `nondeterministic_ops` in each night-6 run
json is what keeps saying so (gate 7b). **If a future run records a non-empty
`nondeterministic_ops`, that run is not a deterministic run and pair (a) built on it is void** —
§7, void conditions.

### 5.3 Control (a) at short horizon — the answer, and its boundary

Two runs of **seed 0**, determinism ON, **fresh processes**, separate network ids `9993/010` and
`9993/011`, sequential, **2,000 completed iterations** each (the horizon chosen so both finish
inside about fifteen minutes; nights 1–5's replicates already differed at iteration 12 in normal
mode). Compared with no tolerance at all, by the script recorded as
`results/night6/compare_bitwise.py`: every logged training-loss value in `loss.h5`, byte for byte,
and every tensor of the final checkpoint by sha256 over the tensor's own bytes.

**RESULT: BITWISE IDENTICAL.** Report: `results/night6/control_a_bitwise.json`, exit 0.

| what was compared | result |
|---|---|
| the 14 loss / iteration arrays the runs wrote (`loss.h5`, `loss_flow.h5`, and the `training/`, `training_batch/`, `validation/`, `validation_batch/` triples) | **all 14 identical by sha256 over their raw bytes** |
| held-out `val_loss` at the rung hooks, iterations **1,000** and **2,000**, computed from the live network state | **identical to the last stored digit, both rungs** |
| held-out `val_loss` at flyvis's own checkpoint passes (iterations 0 and 12) | **identical** |
| every tensor of the last shared checkpoint, sha256 over each tensor's own bytes | **89 of 89 identical, 0 differing, none on one side only** |
| `final_iteration` | 1,999 and 1,999 |
| `determinism` block and `nondeterministic_ops` | identical; both `{}` |

**The one difference in the whole comparison is the string `time` inside the checkpoint** — the
wall clock at save, `Sun Sep 20 16:39:10 2026` against `16:46:54 2026`, which is why the two
checkpoint *files* have different sha256 while all 89 tensors inside them agree. It is reported
separately and is not excused as a tolerance; nothing else was excluded.

**Two honest limits on how far that evidence reaches, both of which change the night's design.**
(i) **flyvis flushes the loss arrays only as far as the last checkpoint**, and at this horizon that
is checkpoint index 1, `chkpt_iter` 11 — so `loss.h5` holds twelve values, not two thousand, and
the array comparison certifies the first twelve iterations rather than the first two thousand.
(ii) For the same reason the tensor comparison is of the checkpoint at iteration 11. **What
actually reaches iteration 2,000 is the third row of the table**: the rung hook's held-out
`val_loss` is computed from the live network at exactly that iteration, and in deterministic mode
that evaluation is itself bitwise repeatable (`rowB_controls_det.json`, 30/30 pairs and 3/3 fresh
processes), so an identical value is evidence of identical state and not of a coincidence in a
reduction — though it is a scalar, and a scalar is weaker evidence than a tensor.
**Consequence for §6: at the 26,000 horizon this limit disappears** — the last checkpoint is index
8 at `chkpt_iter` 25,211, so the arrays carry ~25,212 values and the tensor comparison is of a
network trained 25,212 iterations. It is a third reason to prefer 26,000 over any shorter reduced
horizon.

**This is answer (a) at short horizon, and it is not answer (a) at 250,000.** Identity at 2,000
iterations does not prove identity at 250,000. What it does establish is that no divergence
mechanism operates on the scale at which one was already visible in normal mode: there, two
replicates of one seed differed by iteration 12, and here the same comparison is made 166 times
further along. The residual risk that pair (a) at full length exists to close is a mechanism that
appears only later — a kernel choice that depends on memory pressure being the obvious candidate,
since `llama-server`'s residency varies.

## 6. Four compositions, all costed — the owner chooses

At 0.219134 s/iter, and taking the normal-mode full-run wall times on record as 14.3–14.7 ks
(`docs/briefs/2026-09-17-night5.md` §6), a **full 250,000-iteration deterministic run is 47.6–49.0
ks, about 13.4 hours** — longer than any *night* this project has run. Horizons below 150,000 are
entirely inside the plateau regime, so 0.219134 s/iter applies to them directly: 26,000 iterations
is 5,697 s (1.58 h) and 50,000 is 10,957 s (3.04 h).

| design | what runs | wall, sequential | reads (a) at | reads (b) at | row-B checkpoints reached |
|---|---|---|---|---|---|
| **α** | `A1`,`A2`,`B`, all stopped after iteration **26,000** | **4.8 h** — one night, with room | 26,000 | 1,000 / 5,000 / 25,000 | indices **0–8** |
| **β** | the same three, stopped after **50,000** | **9.2 h** — one long night | 50,000 | the rungs plus the shared checkpoints | indices **0–14** |
| **γ** (recommended) | `A1` full, `B` full, plus `A2` at 26,000 | **28.4 h** — two nights | 26,000 | **1,000 / 5,000 / 25,000 / 250,000** | `A1`,`B`: **0–71**; `A2`: **0–8** |
| **δ** | all three full | **40.2 h** — three nights | 250,000 | all four rungs | **0–71** for all three |

**Why 26,000 and not 25,000, which looks like the obvious horizon.** The checkpoint grid is
`chkpt_iter = −1, 11, 3,611, …` in steps of 3,600, so **checkpoint index 8 sits at
`chkpt_iter` 25,211, i.e. after completed iteration 25,212** — the index the row-B reading of
§3a names as its ~25k comparison point, and the one `docs/experiments/005-…` and
`PROFILES-READING.md` §0(f) both tabulate. A run stopped after iteration 25,000 stops **272
iterations short of it** and would carry no comparable profile at all. Stopping after 26,000
reaches index 8, still evaluates the canonical 1,000 / 5,000 / 25,000 rungs, and costs four
minutes per run. This is the kind of off-by-one that is free to find now and expensive to find
in the morning.

Per-run overhead beyond training is about one minute (solver build 5.4 s measured, plus imports and
the connectome hash).

**Why γ and not α, although α is the one that fits the authorisation.** The rung table in
`docs/next-session-plan.md` §2 records that at **25,000** the normal-mode instrument already
separates seeds by a wide margin over the replicate gap, while at **250,000** it does not — and the
inversion between those two rungs is on the board as
`THE-SPREAD-REPLICATE-RATIO-INVERTS-BETWEEN-C3-AND-THE-TOP-RUNG`. The ranking failure that ADR-002's
condition hangs on lives at the **top rung**. A deterministic night that stops at 25,000 therefore
answers a question that was not in doubt: **α is a shakedown of the deterministic instrument, not
an experiment on (b).** Choosing it because it fits the night would be an arrangement arrived at for
an unrelated reason and justified afterwards — the failure night 5's brief §1 records about its own
run order.

**One thing cuts the other way, and is recorded because it weakens my own recommendation.** The
row-B profile reading of §3a tabulates checkpoint index 8 (~25k) as one of its five comparison
points, and at that index the nights 1–5 twin-versus-foreign result is already mixed rather than
settled. So α is **not** empty on the profile channel the way it is on the loss channel: it would
place night 6's two seeds on an existing table. What it still cannot do is reach checkpoint 71,
which is the index at which the profile reading's shape signal is strongest and at which the loss
reading fails. That is why the recommendation stands, and why it stands less firmly than it would
have yesterday.

**What γ gives up, stated so the choice is real.** (i) Pair (a) at full length: it is kept at
26,000 (1.6 h) rather than 250,000 (13.4 h), on §5.3's reasoning. (ii) One night becomes two, which
doubles the exposure to the Windows-Update restart this project has already lost a run to (§7 gate
1, §9). (iii) `A1` and `B` run on different calendar days and may land in different boot sessions;
under the definition of replicate noise that night 5's gate 10 calls (ii), a seam between them is
a confound for (b) — and unlike night 5 there is no third run to measure the seam with. **If the
seam matters more to the reviewers than the top rung does, α is the right answer and γ is the wrong
one.** That is the trade, and it is not mine to settle.

**Concurrency is not proposed.** Two runs fit the card's memory — about 7.0 GiB free against about
1.4 GiB added per run (§5.1) — but the throughput was not measured, and the board entry
`EIGHT-PROCESSES-SHARE-THE-CARD-NO-FASTER-THAN-ONE` records m = 1 for this workload in normal mode.
Proposing concurrency on an unmeasured assumption is exactly what this file may not do.

**And one thing the owner should not spend time on:** freeing the GPU will not help. §5.1 measured
normal-mode training with `llama-server` resident and found it inside the band measured on a free
card. The 3.33× is determinism.

## 7. Acceptance — the gates, and which of night 5's do not apply

Each item is a gate that can fail; a failed gate voids the run or the pair built on it.

**Registered as the reading of (a):** *bitwise* identity of `A1` and `A2` — every logged training
loss value in `loss.h5` byte for byte, and every tensor of the final shared checkpoint by sha256 of
its bytes. **Pass/fail, no tolerance.** On a fail, the first differing iteration index is reported,
which is the quantity nights 1–5 never had.

**Registered as the reading of (b):** the separation of `A1` and `B` in held-out `val_loss` at each
rung the composition reaches and at the last shared checkpoint, reported **beside** the replicate
gaps of nights 1–5 as recorded in `docs/experiments/005-…` §2 and beside the between-individual
spread recorded in the same section — cited, not restated, so that this brief stays off the
blind-author exclusion list (`docs/blind-author-exclusions.txt`, ADR-003). `A2`/`B` is reported
beside it; if (a) passes it is the same number as `A1`/`B`, and saying so is a check on the whole
chain.

**And in both cases a second readout beside held-out loss: the row B activity profile, in both
pre-declared distance forms and both quantities, at the checkpoint indices §3a fixes.** The loss
reading alone would be reading the channel nights 1–5 found nothing in; §3a states why, what the
profile readout's pass condition for (a) is (distance exactly 0), what each (b) outcome means, and
that the same vacuity trap applies to it one level in. Whether the rung reading and the profile
reading agree is itself part of the record, and a disagreement between them is reported as a
disagreement rather than adjudicated.

1. **`uptime_s` strictly increases** between each run's `machine_state_start` and
   `machine_state_end`, and across the runs of a wave. Carried from night 5 gate 1 unchanged. Under
   γ the two nights are separate waves and the comparison is made across them by hand.
2. **`boot_time_utc` printed, not gated.** Carried unchanged (night 5 gate 2): it is computed as
   `time.time() − uptime_s` and drifts with the wall clock.
3. **An independent witness from the Windows event log** — Kernel-General id 12, EventLog id 6013,
   and Kernel-Power 42/107 for the sleep/resume pair — queried for the night's own window and
   recorded beside each run even if empty. Carried unchanged (night 5 gate 3).
4. **Night 5's four s/iter sub-gates DO NOT APPLY, and nothing replaces them as a gate.** Bands
   4a–4c were measured on eight normal-mode runs; night 6 runs 3.33× slower by construction and
   would fail all three. Gate 4d (the transition at iteration 150,000) does not apply to any horizon
   below 150,000, which is every horizon except γ's two full runs. **Registered instead: night 6's
   s/iter is printed, not gated** — median over the run, median over iterations 100–2,000, and for
   a full run the plateau/late split at 150,000 — against this brief's single measurement of
   0.219134 s/iter. One probe of 600 iterations is not a band. A band for deterministic mode can be
   derived after night 6 and gated on from night 7, which is the same order in which night 5's own
   bands came into being.
5. **`machine_state_start` and `machine_state_end` present in every run json.** Carried unchanged
   (night 5 gate 5); night 5 was the field's first live exercise and it is no longer new.
6. **`results/night6/` assembled in the same commit as the night's record**, on
   `results/night5/extract_night5.py`'s template. The raw wave output lands in `tools/night/`, which
   is gitignored by name for `*.json`, `*.log` and `wave_*.pid`. **Ignored is not saved:** until the
   extract runs the night exists only on this disk.
7. **Config invariants — carried, and measured to be insufficient.**
   ```
   python tools/night/config_invariants.py --gate results/night6/<run>.slim.json \
       --against results/night1/*.slim.json results/night2/*.slim.json \
       results/night3/*.slim.json results/night4/*.slim.json results/night5/*.slim.json
   ```
   **What it will do, established by running it on the deterministic probe rather than by reading
   the code (2026-09-20):** it derives 166 lines, 162 invariant and 4 varying
   (`ensemble_and_network_id`, `network_name`, `description`, `seed`), reports **all 162 invariant
   lines matching**, prints the four varying lines, and **exits 0**. A deterministic run passes it
   clean. **That is the finding: gate 7 is blind to determinism.** The flags are not Hydra config —
   `resolved_config_yaml` contains no occurrence of the string `determin` at all — they are process
   state, recorded in the run json's own `determinism` block and in `argv`. Gate 7 therefore
   certifies that night 6 trained the same *model* as nights 1–5, which is exactly what it is for,
   and says nothing about the one property that makes night 6 a different night.
7b. **NEW — the determinism gate, because gate 7 cannot be it.** In every night-6 run json:
   `determinism.requested`, `determinism.cudnn_deterministic`,
   `determinism.use_deterministic_algorithms` and `determinism.mode_query` are all `true`;
   `determinism.cudnn_benchmark` is `false`; `determinism.cublas_workspace_config` is `":4096:8"`;
   `nondeterministic_ops` is `{}`; and `--no-determinism` does **not** appear in `argv`. Any one of
   these failing makes the run a normal-mode run wearing a deterministic night's tag, and both
   pairs built on it are void. The eight recorded values are exactly what §5.1's probe produced, so
   this gate has been seen to pass on a real run before it was relied on.
8. **The training environment is the one that trained nights 1–5**, by content. Night 5's form
   compared `tools/.venv` against the scratchpad copy; **that copy no longer exists** (the
   `flyvis-probe` tree was deleted on 2026-09-20 — backlog,
   `THE-NIGHT-TOOLING-LIVES-IN-A-TEMPORARY-SCRATCHPAD`), so the two-tree comparison cannot be run
   and pretending otherwise would be the defect this repository keeps correcting. Registered
   instead: the single-tree form,
   ```
   python tools/venv_manifest.py tools\.venv --out results/night6/venv_manifest.json
   ```
   and its combined digest compared by eye with the one night 5 recorded,
   `94f7f483e8410e54887c98b20d520872823f1ba5ad9fa1c12d6b95359da7e318` over 21,650 files
   (`docs/briefs/2026-09-17-night5.md` §4.8). A disagreement voids the comparison with nights 1–5,
   not the night's internal pair (a).
9. **Night 5's gate 9 (the pair table and its estimator) does not apply.** It exists to stop a
   pooled σ being taken over dependent differences. Night 6 computes no σ, no pooled spread and no
   ratio (§2). Its pair table is §3's three rows and nothing is averaged across them.
10. **Night 5's gate 10 (degrees of freedom) does not apply.** Night 6 adds **zero** degrees of
    freedom to the normal-mode replicate variance, because none of its runs is a normal-mode run.
    It adds one deterministic individual pair and one deterministic replicate pair, and both are
    existence checks. Stated here so that no later protocol counts night 6's runs toward an N.

## 8. The launch commands, dry-run from the repository (2026-09-20 UTC)

The launcher gained three switches, all additive and all no-ops when absent, so that a command
without them produces byte-for-byte the argument list nights 1–5 used. Verified by dry-running
night 5's own command after the change: it still emits
`--sequential --detach --no-determinism`, the two jobs `9992/000` then `9992/003`, and
`[dry] 2 commands; mode=sequential; detach=True; nothing started; wave json not written`.

- `start_night.ps1 -Deterministic` — omit `--no-determinism` (absent = pass it, as nights 1–5 did).
- `start_night.ps1 -StopAfterIter K` — pass `--stop-after-iter K` through (absent = not passed).
- `start_night.ps1 -ReplicateTag T` / `launch_wave.py --replicate-tag T` — tag the replicate-of job
  `T` instead of the built-in `rep` (absent = `rep`).

`launch_wave.py` gained the matching `--stop-after-iter` and `--replicate-tag`. Nothing else
changed; no default any night relied on was touched.

### Design α — one command, one night

```
tools\night\start_night.ps1 -Tag night6 -Ensemble 9994 -Seeds "0,3" -NoReplicate `
    -ReplicateOf "0" -ReplicateTag night6 -Deterministic `
    -Rungs "1000,5000,25000,26000,250000" -StopAfterIter 26000
```

`-DryRun`, executed from the repository 2026-09-20, prints, in this order:

```
run_individual.py --seed 0 --id 9994/000 --n-iters 250000 --rungs 1000,5000,25000,26000,250000 --tag night6 --out-dir ...\tools\night --stop-after-iter 26000 --progress-every 100 --progress-file ...\wave_night6.progress.log
run_individual.py --seed 0 --id 9994/900 --n-iters 250000 --rungs 1000,5000,25000,26000,250000 --tag night6 --out-dir ...\tools\night --stop-after-iter 26000 --progress-every 100 --progress-file ...\wave_night6.progress.log
run_individual.py --seed 3 --id 9994/003 --n-iters 250000 --rungs 1000,5000,25000,26000,250000 --tag night6 --out-dir ...\tools\night --stop-after-iter 26000 --progress-every 100 --progress-file ...\wave_night6.progress.log
[dry] 3 commands; mode=sequential; detach=True; nothing started; wave json not written
```

preceded by the three lines the new switches print and nothing else prints:

```
determinism     : ON (--no-determinism NOT passed; nights 1-5 passed it)
stop after iter : 26000  (must be one of --rungs; --n-iters stays 250000, so the schedule is the night runs')
replicate tag   : night6  (instead of the built-in 'rep')
```

`26000` is added to the rung ladder because `--stop-after-iter` requires its value to be one of
`--rungs` (`run_individual.py:226-230`); the canonical 1,000 / 5,000 / 25,000 rungs are all still
evaluated, and `--n-iters` stays 250,000 so the learning-rate schedule and epoch count are the
night runs'.

Note that `--no-determinism` is absent from all three job commands, which is the whole point, and
that the ids and their order are `9994/000`, `9994/900`, `9994/003` — `A1`, `A2`, `B`.

### Design γ — three waves, two nights

```
# night 1, ~13.4 h:  A1, seed 0, full length
tools\night\start_night.ps1 -Tag night6a -Ensemble 9994 -Seeds "0" -NoReplicate -Deterministic

# night 1 tail or night 2 head, ~1.6 h:  A2, the repeat of seed 0, through checkpoint index 8
tools\night\start_night.ps1 -Tag night6c -Ensemble 9994 -Seeds " " -NoReplicate `
    -ReplicateOf "0" -ReplicateTag night6c -Deterministic `
    -Rungs "1000,5000,25000,26000,250000" -StopAfterIter 26000

# night 2, ~13.4 h:  B, seed 3, full length
tools\night\start_night.ps1 -Tag night6b -Ensemble 9994 -Seeds "3" -NoReplicate -Deterministic
```

Their `-DryRun` output, job lines only:

```
run_individual.py --seed 0 --id 9994/000 --n-iters 250000 --rungs 1000,5000,25000,250000 --tag night6a --out-dir ...\tools\night --progress-every 100 --progress-file ...\wave_night6a.progress.log
[dry] 1 commands; mode=sequential; detach=True; nothing started; wave json not written

run_individual.py --seed 0 --id 9994/900 --n-iters 250000 --rungs 1000,5000,25000,26000,250000 --tag night6c --out-dir ...\tools\night --stop-after-iter 26000 --progress-every 100 --progress-file ...\wave_night6c.progress.log
[dry] 1 commands; mode=sequential; detach=True; nothing started; wave json not written

run_individual.py --seed 3 --id 9994/003 --n-iters 250000 --rungs 1000,5000,25000,250000 --tag night6b --out-dir ...\tools\night --progress-every 100 --progress-file ...\wave_night6b.progress.log
[dry] 1 commands; mode=sequential; detach=True; nothing started; wave json not written
```

**`-Seeds " "` is not a typo.** The A2-only wave has no plain-seed job at all, only the
replicate-of job; PowerShell rejects `-Seeds ""` with "Missing an argument for parameter 'Seeds'",
and a single space parses to an empty seed list in `launch_wave.py:43-54`. Recorded because it will
otherwise look like a mistake to the next reader, and because it was found by running the command,
not by reading it.

Each wave detaches; closing the window stops only the follower. To stop the runs:
`taskkill /T /F /PID (Get-Content tools\night\wave_<tag>.pid)`. To re-attach:
`start_night.ps1 -FollowOnly -Tag <tag>`.

## 9. Void conditions and stop conditions

- **A reboot during a run.** Gate 1 catches it after the fact; the run is void, and under γ a
  reboot between the two full runs puts `A1` and `B` in different boot sessions, which is a confound
  for (b) with no third run available to measure it (§6).
- **The Windows-Update precaution is the same one already on the backlog and it is not optional
  here.** `WINDOWS-UPDATE-RESTARTS-INSIDE-THE-NIGHT-WINDOW-BECAUSE-ACTIVE-HOURS-END-AT-0600`: a
  planned restart killed a run at iteration 12,700 on 2026-09-15 because Windows defers an update
  restart **only inside** active hours. Before launch, the owner either pauses updates or sets
  active hours to cover the whole window. A 13.4-hour run is longer than any span this project has
  protected so far, and γ needs two of them.
- **A run does not reach its horizon** — `final_iteration` **250,008** for a full run, or
  **K − 1** for a run stopped after completed iteration K, because `solver.iteration` is
  incremented after the batch and `--stop-after-iter` fires inside it: the probe stopped after 600
  and recorded `final_iteration` 599, the control after 2,000 and recorded 1,999. Both values are
  measured, not predicted. A partial run is a failed run (`docs/next-session-plan.md`, night 2's
  `002_killed_by_reboot`).
- **`nondeterministic_ops` is non-empty in any run** (§5.2, gate 7b): that run is not a
  deterministic run, and the pairs built on it are void.
- **Gate 7b fails in any other way**: the run trained in normal mode and the night did not happen.
- **The wave is launched under an ensemble that is not free**, or `9994/900` is not checked (§4).
- **Any text derived from this night quotes an ADR-002 ratio** (§2). That is not a run failure; it
  is a reading failure, and it voids the reading rather than the runs.

## 10. What this file does not do

This brief does not launch training, does not run any diagnostic or evaluation script beyond the
probe and control of §5 — which were run on the owner's standing authorisation for the cheap
determinism control named in the backlog entry's "First step" — and does not modify `backlog.md`,
`README.md`, `VISION.md`, `ROADMAP.md`, `literature.md`, anything under `docs/decisions/` or
`docs/plans/`, `docs/next-session-plan.md`, `results/night5/**`, or any other brief. It is a draft.
The composition is **not chosen**: §6 lays out four and recommends one, and the choice between α and
γ trades the top rung against a boot seam and belongs to Mike and the reviewers.
