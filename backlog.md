---
project: connectome-seed
entry_level: h3
status_machine: v1
language_cutoff: 2026-09-13
---

# connectome-seed Backlog

> Mike decides. CC executes. Ark, Johnny and Warren review.
> Direction lives in `VISION.md`, the order of work in `ROADMAP.md`, the decisions in
> `docs/decisions/`. Format and validator: dpc-messenger `docs/BACKLOG_FORMAT.md`; check and rebuild
> the views from the dpc-messenger checkout with the path given explicitly and `--out` set to
> this directory. The `axis:` vocabulary (collective / knowledge / network / honesty / reach)
> is dpc-messenger's, adopted as-is because the checker is shared.

## OPEN



### A-BAND-TAKEN-FROM-EIGHT-RUNS-WAS-WRITTEN-DOWN-SO-THAT-TWO-OF-THE-EIGHT-FALL-OUTSIDE-IT: the migration acceptance band and gate 4's three sub-gates are both defective in the same way, and the defect only shows when a new run lands at an edge (MEDIUM, open, 2026-09-19 — CC, on trying to close the migration entry against its own acceptance condition)

- **Observed — the migration band does not contain its own sample.** The condition was "a full run's `iter_wall_median_all_s` inside **[0.0598, 0.0622]** — the band of all eight runs on record". Measured over those eight: `9991/001` = **0.062248** and `9991/004` = **0.059796**, i.e. **two of the eight sit outside**. The true range is [0.059796, 0.062248] and the quoted band was rounded to four decimals **inward**, excluding both of its own endpoints. Night 5: `0"` = 0.062199 (inside), `3'''` = **0.059288** (below the range of all eight, genuinely faster).
- **Observed — gate 4's three sub-gates are not independent.** Plateau and late bands alone permit ratios from **1.263 to 1.506**, while the ratio band is [1.30, 1.45]. So a run can pass both level bands and fail the ratio, which is what `0"` did (1.461). All three were taken from the same eight runs and then applied as if independent.
- **Observed — and the mechanism is that the phases move separately.** Both night-5 runs are faster than all eight in the late phase (0.0447, 0.0448 against a previous minimum of 0.0457) while their plateaus go in **opposite** directions (`3'''` below all eight, `0"` above all eight). The ratio is their quotient and so has a wider spread than either component band.
- **Inferred.** A band set from n = 8 describes a sample, not a property, and writing it to four decimals can make it exclude the very runs it was drawn from. This is the same error as an SD over three seeds presented as the population's, one level down, on the instrument rather than on the science.
- **First step.** Two candidates, and the choice is a decision rather than a preference: state bands as the observed min/max with the direction of rounding named (outward), or state them as a tolerance around a central value with the tolerance derived (a multiple of the checkpoint step). Either way a derived quantity such as a ratio does not get its own band on top of its components' — it gets one or the other. Not blocking any run; blocking a clean disposition of night 5's gate 4.
- **axis:** collective

### THE-CORRESPONDENCE-BETWEEN-A-RUN-AND-ITS-COLUMN-KEEPS-BEING-INFERRED-FROM-A-NAME-INSTEAD-OF-RECORDED: three times now the link has been left derivable, and twice it was wrong (MEDIUM, open, 2026-09-19 — Ark found the third instance in CC's night-5 table; CC recorded it)

- **Observed — instance 1, night 1.** Its checkpoint table names its columns `val_loss_A` / `val_loss_B` with **no legend anywhere in the repository**. Which run is which cannot be recovered from the file, and could not be recovered by byte comparison either, because night 4 prints full floats where the older reports print four decimals.
- **Observed — instance 2, the v1 resolver.** It derived run→column from wave-json bindings plus column names across nights and **could not map two of the eight runs**, refusing with exit 2. Removed in v7 in favour of the registered file's pinned header.
- **Observed — instance 3, the night-5 table.** Its first version declared a rule about itself: "`val_loss_seed<N>` followed by k `prime` tokens is the (k+1)-th run of seed N". True of `val_loss_seed0primeprime`; **false** of `val_loss_seed3primeprimeprime`, which carries three prime marks and is also a third run. Our own notation counts marks (`0"` two, `3'''` three) while the rule counts order, and they coincided for the first case only. Fixed the same day: `results/night5/run_columns.csv` carries the explicit mapping with `run_index_for_seed`, and the grammar is demoted to a comment explaining why it cannot be trusted.
- **Inferred.** The pattern is not three accidents; it is a standing preference for a correspondence that looks derivable over one that is written down. Each time the first case validated the rule and a later case broke it.
- **First step.** A checklist rule in `docs/CHECKLIST-research-repo.md`: a run→column, run→file or run→session correspondence is **recorded as a table beside the artefact**, never encoded in a name and never re-derived by a consumer; a naming convention may accompany it as a comment and may not be the source of truth.
- **axis:** collective

### THE-CHEAP-AND-THE-DEAR-ESTIMATE-ARE-TAKEN-UNDER-DIFFERENT-REGULARISATION-SO-TEST-B-HAS-TWO-CLASS-QUESTIONS: the C3 hook at 25,000 lies inside the activity-penalty regime and the top rung at 250,000 lies outside it, so "does the cheap estimate agree with the dear one" was measured as "does it agree with the dear one in another regime" (HIGH, open, 2026-09-18 — Ark, on reviewing CC's night summary: "если C3 и хук живут в разных режимах, то у (b) **два** класс-вопроса, а не один"; measurement by CC)

- **Observed.** `activity_penalty.stop_iter = 150000` in the resolved config of all eight runs, against `n_iters = 250000`: the penalty is applied for the first 150,000 iterations and then never again (`Penalty.__call__`, `solver.py:812-818` — past `stop_iter` it sets `self.activity_optim = None`). The C3 hook sits at 25,000, **inside** the penalised regime; the top rung sits at 250,008, **outside** it.
- **Observed.** The penalty acts on `nodes_bias` and on nothing else, and that is now a read rather than an inference (2026-09-18, CC, in the installed flyvis 1.2.0): `penalize` appears in exactly three network configs — `node_config/bias/bias.yaml:11` with `activity: true`, and `edge_config/syn_strength/syn_strength.yaml` and `edge_config/syn_count/syn_count.yaml` with `function: weight_decay, kwargs: {lambda: 0}`. `Penalty.init_optim` adds a parameter to the activity list only when `getattr(config, "activity", False)` holds, and to the function list only when `"function" in config and any(config.kwargs.values())` — which `lambda: 0` fails, so the weight-decay optimiser is never even constructed. The activity optimiser is built over `getattr(self.network, "nodes_bias")` alone.
- **Observed.** The two weights in the penalizer config are **one penalty with two branches**, not two families of term: `asymmetric_weighting(tensor, gamma, delta) = gamma·relu(tensor) − delta·relu(−tensor)` (`utils/tensor_utils.py:443-461`), applied to `activity_baseline − activity_mean` and then squared, so below-baseline deviations are weighted 1.0 and above-baseline 0.1. Ark's reading that the pair implies node and edge terms does not hold.
- **Observed.** `nodes_bias` carries one value per cell type — `bias.yaml` has `groupby: [type]`, and the connectome definition `flyvis/connectome/fib25-fib19_v2.2.json` lists **65** nodes, each with its own `bias` field (605 edge groups, for scale). Of the three penalisable families only the bias is *sampled*: `initial_dist: Normal, mode: sample, seed: 0`, against `syn_count`'s `mode: mean` and `syn_strength`'s `initial_dist: Value`, both deterministic. So `network.node_config.bias.seed` — the one parameter that differs between our individuals — can move only those 65 numbers, and they are exactly the ones the penalty pulls toward a common level for 60 % of training.
- **Inferred, and this is the entry's point.** Test (b) asks whether a cheap early estimate ranks individuals the way an expensive late one does. If the two are taken under different regularisation, "the cheap estimate is uninformative" and "the cheap estimate is informative about a differently-regularised system" are **two different failures with the same symptom**, and the design cannot tell them apart as it stands. What must be decided before the reading is which of the two (b) registers, because the answer changes what a null result licenses. Not a verdict on (b) — a statement that the question was underspecified.
- **Inferred.** One consequence favours the reachability endpoint: the checkpoint curves pass through **both** regimes within a single run, and the straddle is already printed, so the free test is the only instrument available that can see the regime break without leaving one curve (Ark).
- **First step.** Before the (c)4 reading, state in `docs/plans/2026-09-17-endpoint-before-n.md` which (b) is registered, and whether a rung inside the unpenalised regime — any checkpoint past 150,000 — is the honest cheap anchor instead of C3. No new run is needed to decide it: the eight curves on disk already span both regimes.
- **axis:** collective

### THE-INSTRUMENTS-WERE-AUDITED-THE-DAY-THEY-WERE-BUILT-AND-NINETEEN-FIXES-WAIT-ON-MIKES-WORD: the code audit of the diagnostics found witnesses that cannot veto, constants never checked against the pre-registration and an undocumented null-draw rule, and nineteen fixes with falsifiers wait on Mike's word to fix the tools (HIGH, open, 2026-09-15 — Ark 08:42/08:45/09:39/09:51, Zcode 09:04, CC; consolidated `docs/tool-hardening-package.md`; Mike's word «чини инструменты»)

- **Observed.** `docs/tool-hardening-package.md` (19 items): tier A, before the first analysis
  of night 3 — items 1, 2, 15, 16 (the seven `eval_rung` invariants into every evaluation json;
  a lattice-derived hook/per-item tolerance; a failed invariant sets `exit =
  "state_check_failed"` instead of staying `"ok"`; an idempotence control of the evaluator);
  tier B, before the new pre-registration — items 3a/3b (`--check-constants` against the
  pre-registration; no numbers in identifier names), 4–14 (connectome-checked module grouping,
  a scaled null beside the isotropic one, P0/P1/self-path as asserts, noise-band and state
  labels on every output, script-hash provenance, one evaluation entry point, the null-draw
  rule registered before any draw, duplicate-key refusal, per-metric-per-state floors, a paired
  re-draw for clamp censoring), 17 (preflight for a pending reboot / free VRAM), 19 (a
  provenance field for any quantity that crossed more than one formatter); tier C, before night
  3 — nothing, night 3 runs the current script unchanged. Source: 002 §5h code audit (Mike's
  question 08:40; Ark 08:42/08:45; CC's Explore agent on Sonnet; verified by CC), extended
  09:04–09:51 with items 14–19 and rules R1–R4. Item numbering: item 18 (the base-rate check)
  was folded into rule R2 when rules were separated from fixes; the gap is deliberate.
- **Inferred.** None of the 19 items recomputes a recorded number — only item 14's null
  calibration is re-run once, a second line beside the first; every falsifier is stated as a
  concrete test that fails today and must pass after the fix.
- **First step.** Mike's word «чини инструменты», then tier A (items 1 and 15 are tested
  together by one test; item 16 needs a purpose-built fixture); items 5 and 13 are
  design-first, not one-line changes. See
  [[THE-COMPOSITION-MARGIN-OVER-ITS-FLOOR-IS-SMALLER-THAN-A-NULL-SHIFTS-MEDIAN-DELTA]] (the (a)
  reading items 5/11 answer) and
  [[WINDOWS-UPDATE-RESTARTS-INSIDE-THE-NIGHT-WINDOW-BECAUSE-ACTIVE-HOURS-END-AT-0600]] (item
  17).
- **axis:** honesty

### DATAMATE-UNLINKS-AN-OPEN-HDF5-FILE-AND-WINDOWS-REFUSES: flyvis does not build its connectome on Windows because its storage layer deletes a file while an h5py handle is still open (MEDIUM, open, 2026-09-13 — found by CC while verifying the flow)

- **Observed.** `datamate/io.py`, `_write_h5`: `h5.File(path, mode="w")` is opened, the
  `except` branch runs while that handle is live, and `path.unlink()` raises `WinError 32`.
  The same shape sits in `_extend_h5`. `HDF5_USE_FILE_LOCKING=FALSE` changes nothing — it is
  not a locking problem. A close-before-unlink patch in both functions makes `Network()` build.
  `datamate` is a separate package (v1.0.0) under the same GitHub organisation as flyvis
  (`github.com/flyvis/datamate`) — Ark's point that it is a third-party dependency stands, and
  so does the consequence that a local patch breaks on upgrade.
- **First step.** Keep the patch in the scratch environment for the test; open an upstream
  issue or PR at `flyvis/datamate` with the two-line fix so the next install does not need it.
  Not before the test — the patch is not on the critical path once it holds.
- **axis:** honesty, reach

### THIRTEEN-LINKS-POINT-INTO-A-DIRECTORY-THAT-WILL-NOT-BE-PUSHED: README, literature and idea link into chat/, which is ignored from history, so every one of them resolves to nothing on GitHub (MEDIUM, open, 2026-09-13 — consequence of Mike's «chat/ в gitignore», 06:50 UTC)

- **Observed.** Counted before the first commit: README 8 distinct links, `literature.md` 4,
  `idea.md` 1. All of the form `chat/NN-name-hhmmss.md`. `chat/` is excluded by `.gitignore`
  from `8695d26`.
- **First step.** Replace each with a plain attribution — name, role, date, UTC — which is what
  the README already carries in prose; the information survives, the link does not. Mechanical;
  done in the same pass as the LICENSE and the translation. Child of [[ADR-001]].
- **axis:** reach

### EIGHT-PROCESSES-SHARE-THE-CARD-NO-FASTER-THAN-ONE: aggregate throughput saturates near 17.5 it/s whatever the process count, so only fewer kernel launches per iteration can shorten a night (MEDIUM, open, 2026-09-13 — CC, from the concurrency measurement committed in e797f02)

- **Observed.** Per process 0.0619 / 0.228 / 0.450 s/iter at k = 1 / 4 / 8; aggregate
  ≈ 17.5 it/s at every k; `Compute Mode: Default`, no MPS on Windows (sources: scratchpad
  `flyvis-probe/gpu_concb_*`, via `gpu_concb_analyze.py`; pre-registration §4, m = 1 fixed).
  3,104 kernel launches per iteration and GPU busy 45 % single-process — CC, 2026-09-13,
  not yet in a committed log.
- **Observed, batching proxy (2026-09-13).** Batch 4 / 8 / 16 in one process → 0.0654 /
  0.1215 / 0.2261 s/iter, 240 iterations each (`flyvis-probe/gpu_batch_9987_000..002.json`):
  3.46× the time for 4× the samples, a 16 % per-sample gain and no more. Batch 24 and 32 fail
  before the first iteration on flyvis's 16-sequence validation split (`RuntimeError: size of
  tensor a (32) must match … (16)`; `gpu_batch_9987_003/004.json`, `iteration_after: 0`).
  flyvis trains ensembles one process per member (`compute_cloud_utils.py:427-449`); no
  `vmap` / `functional_call` anywhere in the package. From both sides — processes and batch —
  the card's ceiling is ≈ 65–70 stimulus-samples/s.
- **Observed, extent 5 (2026-09-13).** `extent_probe/ext5_9986-*.json` against
  `ext15_9985-*.json`, 1,008 iterations × 4 runs per extent: extent 5 = 5,759 nodes /
  171,471 edges and still 734 free parameters (65 types, 604 pairs, none missing);
  0.0443 vs 0.0648 s/iter → 1.46× (3.08 h vs 4.50 h per run); GPU util 18–25 % at extent 5
  against 62–71 % at extent 15 — a fixed ≈ 40 ms per iteration (the 40-step Python loop,
  ~3,100 launches) that does not shrink with the lattice. Seeds spread on both extents at
  1,000 iterations (sd 0.29 / 0.52) against a replicate difference of 1–2e-5 (determinism
  off). Decision (CC's recommendation, sent 17:50 UTC; the ≥ 3× condition not met): the night
  stays on extent 15, extent 5 not adopted.
- **Inferred.** The one lever left is the fixed ≈ 40 ms: CUDA graphs or `torch.compile`
  around the simulation loop — up to ~1.6× at extent 15, ~3× at extent 5. Not before run 0:
  the change needs a control, and run 0 is that control.
- **First step.** After run 0, a 1,000-iteration CUDA-graph prototype compared to run 0's
  hook trajectory. See also [[HOW-MANY-FULL-RUNS-THE-TEST-IS-ALLOWED]], closed 2026-09-13 —
  this measurement is what bounds N per night.
- **axis:** knowledge

### FLYVIS-RESUME-AND-RECOVER-ARE-BROKEN-IN-1-2-0: five defects found by execution in the installed flyvis stand between anyone and a resumed run, and none of them is reported upstream (MEDIUM, open, 2026-09-14 — CC, from the interrupt-and-resume test of 2026-09-13)

- **Observed.** `night/resA_9989-000.json` and `night/resA_9989-000.resume2.stdout.log`
  (scratchpad): (1) `solver.recover()` cannot run — `resolve_checkpoints` signature
  `TypeError` at `solver.py:598`; (2) datamate refuses to re-open a NetworkDir
  (`FileExistsError` on `delete_if_exists`); (3) the checkpoint stores `iteration − 1`, so a
  48-iteration budget ran to 59; (4) no RNG or data-order state is saved — the first 12
  post-resume losses correlate 1.0000 with epoch 0's; (5) a penalty optimizer key mismatch
  (`activity_optim` vs `penalty_optims`) leaves it unrecovered. A sixth is already on the
  board: [[DATAMATE-UNLINKS-AN-OPEN-HDF5-FILE-AND-WINDOWS-REFUSES]].
- **Inferred.** The consequence for this test is registered: §7 counts an interrupted run
  as failed ([[RESUME-OF-AN-INTERRUPTED-RUN-IS-UNVALIDATED]], closed 2026-09-13). Upstream
  fixes would not change that rule; they change what the next user of flyvis 1.2.0 inherits.
- **First step.** On Mike's word, an upstream issue at `flyvis/flyvis` with the
  48-iteration minimal reproduction; until then the §7 rule stands.
- **axis:** knowledge


### WINDOWS-UPDATE-RESTARTS-INSIDE-THE-NIGHT-WINDOW-BECAUSE-ACTIVE-HOURS-END-AT-0600: a planned Windows Update restart killed seed 2 mid-run because active hours end at 06:00 while the night window runs to 11:30, and the launcher has no preflight for a pending reboot (HIGH, open, 2026-09-15 — CC, from the KB5129195 restart during night 2)

- **Observed.** System event log: "2026-09 Security Update (KB5129195)" (build 26200.9457)
  download started 02:33 local 2026-09-15, "Installation Started" 03:10:53 local, three planned
  restarts at 06:29:19 / 06:30:20 / 06:31:05 local (23:29Z–23:31Z 2026-09-14), two logged as
  User32 1074 "TrustedInstaller.exe … on behalf of NT AUTHORITY\SYSTEM … Operating System:
  Upgrade (Planned) 0x80020003", "Installation Successful" 06:33:45 local; no Kernel-Power 41 /
  6008 / 1001 — not a crash or power loss. Active hours on this machine are 12:00–06:00 local
  (`HKLM\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings`), so 06:29 was the first minute Windows
  was allowed to restart. Edition: Windows 11 Home (EditionID Core) — no gpedit, no
  WindowsUpdate policy keys exist.
- **Inferred.** The night window (02:00–11:30 local, per the tooling) runs five and a half
  hours past the end of active hours (06:00 local); nothing in `start_night.ps1` checks for a
  pending reboot or otherwise defends the run against an automatic restart. Follow-up to
  [[NIGHT-2-RUNS-SEEDS-1-AND-2-ON-MIKES-WORD]] — this restart is what killed its seed 2 run at
  iteration 12,700.
- **First step.** Mike chooses the protection: pause updates before each night, shift active
  hours to cover 02:00–11:30, or a policy value if one is documented for Home (the orchestrator
  is checking Microsoft's documentation now). Then `start_night.ps1` gets a preflight that
  refuses to launch when `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto
  Update\RebootRequired` or `…\Component Based Servicing\RebootPending` exists.
- **Observed, 2026-09-15 (CC).** The preflight fix is now item 17 of
  `docs/tool-hardening-package.md` (tier B, before the new pre-registration): refuse to launch
  on a pending reboot or insufficient free VRAM, falsifier — create the `RebootRequired` key in
  a test hive → `start_night.ps1` must refuse; today it launches. Execution waits on Mike's word
  «чини инструменты» —
  [[THE-INSTRUMENTS-WERE-AUDITED-THE-DAY-THEY-WERE-BUILT-AND-NINETEEN-FIXES-WAIT-ON-MIKES-WORD]].
- **axis:** collective

### THE-TUNING-BATTERY-CHECKS-WHETHER-THE-DOMINANT-ABLATION-TYPE-IS-FUNCTIONAL: flash and moving-edge tuning per cell type, compared against Maisak 2013, will show whether seed 2's R2, seed 3's Mi4 and seed 4's CT1 differ in tuning from the same type in the other five runs (HIGH, open, 2026-09-16 — CC, docs/plans/2026-09-16-functional-readout-plan.md step 2)

- **Observed.** `docs/experiments/003-night3-seeds-3-and-4.md` §6 item 2: each of the six runs
  has one cell type that dominates its own ablation profile (Tm5c / Mi4 / TmY15 / R2 / Mi4 /
  CT1(Lo1) for seeds 0/0′/1/2/3/4), and the dominant type differs run to run — "the type that
  blows up is different in every run that has one" (ablation README §5).
- **Inferred.** Whether the dominant type is doing anything *functionally* distinctive (its
  ON/OFF flash-response index or DSI/preferred direction, against the same type in the other
  five runs and against the literature) is a separate question from whether it dominates the
  ablation loss, and is untested.
- **First step.** CC's subagent computes, per seed at 250,008 and at iteration 0: flash-response
  index and DSI/preferred direction per type (65), using flyvis's own functions; brief reviewed
  by Ark and Zcode before launch, readings (a)–(d) of the plan fixed before data (twin trap in
  tuning space; dominant-type deviation ranked among 65, outcomes ≤3 / ≥30 / between;
  literature-polarity count per fly; iteration-0 as the null). All diagnostics, not tests.
- **2026-09-17 UTC (2026-09-18 local), CC:** Unblocked. Step 1 (gray stimulus) closed 2026-09-17, commit `32759e2` —
  see [[THE-GRAY-STIMULUS-CONTROL-TESTS-LEARNED-EQUALS-VISION-FROM-THE-SECOND-SIDE]] in
  `backlog_closed.md` — so this step's own prerequisite ("waits on step 1",
  `docs/briefs/2026-09-16-step2-tuning-battery.md`) is satisfied. The brief is ready; the launch
  itself still waits on the owner's word.
- **axis:** knowledge

### THE-GENOME-DESIGN-AROUND-S2-NEEDS-LABEL-PROVENANCE-BEFORE-EXTRACTION: Ark's design around S2 and CC's two-page "what is the genome here" note are the prerequisite for extracting the label array and rule bank (HIGH, open, 2026-09-16 — CC, docs/plans/2026-09-16-functional-readout-plan.md step 3)

- **Observed.** No design for the genome track exists yet beyond the plan's naming of it; the
  plan assigns provenance of the `groundtruth_utils` fields and the design rewrite around S2 to
  Ark, and a two-page "what is the genome here" note with source addresses to CC, written after
  Ark's design lands. Zcode owns the C6 control specification for the same track.
- **Inferred.** CC cannot extract the label array or the rule bank before Ark hands over the
  field list — the step is ordered, not parallel with its own prerequisite.
- **First step.** Ark writes the design around S2 with label provenance; CC extracts the label
  array and rule bank as soon as the field list is handed over, then writes the two-page note.
- **axis:** knowledge

### THE-LEARNED-GAIN-IS-SIXTY-LOSS-UNITS-ON-AN-UNTRAINED-LEVEL-OF-TWELVE-HUNDRED: rescaling the replicate difference and the between-seed sigma onto the learned-gain axis gives 21% and 6% respectively, a candidate basis for the next registration (HIGH, open, 2026-09-16 — CC, docs/experiments/003-night3-seeds-3-and-4.md §6c)

- **Observed.** `docs/experiments/003-night3-seeds-3-and-4.md` §6c: untrained held-out loss
  ≈1212.55 across six seeds, checkpoint-250,008 loss 1144.64–1160.98 → a learned gain of ≈60
  loss units. On that scale the twin replicate difference (12.73) is 21% and the between-seed σ
  at n=5 (3.54) is 6%.
- **Inferred.** This is a proposal for how a future pre-registration might state its tolerance
  (as a fraction of the learned gain rather than of the raw loss), not a re-reading of the
  existing one — §7's tolerance and its FAIL stand exactly as written and are not revisited by
  this observation.
- **First step.** Mike + reviewers decide, at the next pre-registration, whether a
  learned-gain-relative tolerance replaces or supplements the current raw-loss one.
- **axis:** honesty

### THE-POINT-STATISTICS-RHO-PREVIEW-AT-N-EQUALS-SIX-MUST-NOT-BE-CITED-AS-THE-TEST: the 0.8857 rank correlation between the C3 point statistic and the 250,000 hook at n=6 is a preview of the registered (b) test taken before N is chosen and rests on one pair, and any citation of it must carry that label (MEDIUM, open, 2026-09-17 — CC, from commit a7233dc and Ark/Zcode's confirmation)

- **Observed.** Commit `a7233dc` records Ark's (chat 2026-09-17 08:51:11Z) and Zcode's
  (08:52:47Z) confirmed reading of the ρ = 0.8857 point-statistic value reported in
  `results/diagnostics/window/README.md` §4: "a preview of the registered (b) test at n=6, before
  N is chosen, not a test and not a decision by itself — the registered test is read once at the
  final N with that N's own critical value" (`results/diagnostics/window/README.md:164-166`).
- **Observed.** The value rests on one pair: swapping the ranks of seeds 4 and 5 drops it to
  ρ = 0.714, below the n=6 critical value 0.829 (`results/diagnostics/window/README.md:167-171`).
- **Observed.** The label sits at the source — boxed directly under the ρ table in §4 of
  `results/diagnostics/window/README.md` (lines 164-171) — and is not restated anywhere else in
  that file or in `ROADMAP.md`.
- **Inferred.** The registered (b)/b2 test is defined at C3 with its own N rule and Holm
  correction (`docs/preregistration-cheap-vs-expensive.md`), and is read once, at the final N —
  it is not re-run at n=6. Any future citation of 0.8857 (or the 0.714 swap) outside its labelled
  source must carry the same preview caveat, not be presented as an interim reading of (b) or b2.
- **First step.** None scheduled; this entry is a standing caution against citing the number
  bare. It closes only when superseded by the registered N reading itself, or folded verbatim
  into a future registration's own text.
- **axis:** honesty

### THE-GENOME-TRACK-HANDOVER-OVERSTATES-WHAT-A-SEED-MOVES: `docs/briefs/2026-09-19-genome-track-handover.md` §3 calls the 65 biases "the whole of individuality" when the same seed also spends itself on the decoder and the data order (MEDIUM, open, 2026-09-20 — CC)

- **Observed.** `docs/briefs/2026-09-19-genome-track-handover.md:42`: "The 65 biases are the whole of individuality". `tools/night/run_individual.py:356` spends `--seed` on `network.node_config.bias.seed` alone, but `:282-284` and `:703-705` spend the *same* seed on the global `random`/`numpy`/`torch` RNGs, set before the solver is built and again before training ("data order / augmentation stream"). Two individuals therefore also differ in the decoder's 7,427 initial weights and in data order / augmentation. `VISION.md` and `ROADMAP.md` do not carry the sentence (checked this session, no match).
- **Inferred.** The claim holds for network parameters only, not for the individual as a whole. The confound was already on record in `docs/next-session-plan.md` (the bias-only / order-only 2×2, Ark and Zcode, 2026-09-15) and is now restated in `docs/notes/2026-09-20-what-is-the-genome-here.md` §3.
- **First step.** Correct the handover sentence — the correction must carry no result value, since the doc is required reading for the blind v2 author. `VISION.md` / `ROADMAP.md` need no matching edit; they do not carry the sentence.
- **axis:** knowledge

### THE-BOARD-CHECKER-REFUSES-ON-ROADMAP-AND-NOBODY-READS-THE-REFUSAL: `build.py --check` reports REFUSE on `ROADMAP.md` because its generated status block no longer matches the board, and the cure is regeneration, not a hand edit (MEDIUM, open, 2026-09-20 — CC)

- **Observed, 2026-09-20.** `uv run python tools/backlog/build.py --check C:/Users/mikha/Documents/dpc-research/connectome-seed/backlog.md` (run from `C:\Users\mikha\Documents\dpc-messenger`) prints: `REFUSE  ROADMAP.md` / `the generated status block no longer matches the decisions and the board it is rendered from. Run \`build.py --roadmap C:\Users\mikha\Documents\dpc-research\connectome-seed\backlog.md --out=C:\Users\mikha\Documents\dpc-research\connectome-seed\` — and if the new numbers are wrong, they are wrong at the source, which is the point of generating them`.
- **Observed.** The `--roadmap` mode exists and rewrites exactly that block: `if "--roadmap" in sys.argv:` (`tools/backlog/build.py:1483`), and the block itself is fenced by generated markers (`GEN_OPEN = "<!-- generated by tools/backlog/build.py --roadmap · do not edit inside -->"`, `build.py:422`).
- **Inferred.** The checker is right and the block is tool-generated; red predates 2026-09-20 (this run did not cause it).
- **First step.** On Mike's word, regenerate with the exact command the refusal names, then commit.
- **axis:** honesty

### SIXTEEN-MEGABYTES-OF-UNARCHIVED-SCRATCHPAD-MATERIAL-SITS-BESIDE-FLYVIS-PROBE: preregistration drafts, chat dumps, a PDF and a lora-work directory remain unarchived in the ended session's scratchpad, and Mike must decide their fate by hand (LOW, open, 2026-09-20 — CC)

- **Observed.** `C:\Users\mikha\AppData\Local\Temp\claude\c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx\63f3961a-96ce-4048-8338-72c162ea66f8\scratchpad\` holds ≈16 MB: preregistration drafts, chat dumps (`chatall.txt` etc.), `alphagenome-atlas.pdf`, `lora-work/`.
- **Observed, 2026-09-20 (this session).** `flyvis-probe` no longer exists at that path (`Test-Path` → `False`, checked 2026-09-20). It was archived and hash-verified earlier the same day per the prior record, and Mike had said to delete it; an automated deletion was blocked by a Claude Code safety guard, so the deletion (now apparently done) was Mike's by hand.
- **First step.** Mike decides whether the remaining files are archived to `connectome-seed-archive/` or discarded.
- **axis:** collective

### ROW-B-EXTRACTION-ON-NIGHTS-4-AND-5-NEEDS-THREE-SETTLED-POINTS-BEFORE-THE-FIRST-VALUE: Ark's field list for row B extraction on the checkpoints of nights 4 and 5 came with three points that are cheap to fix now and unfixable after the first value is read (HIGH, open, 2026-09-20 — Ark, group chat 19:13 local; script and first run CC's; launch an unregistered diagnostic on Mike's word)

- **Observed.** No existing entry names row B extraction (checked this session: no match for "row.b"/"rowB"/"ROW-B" in `backlog.md` or `backlog_closed.md`).
- **Observed — (a) two time axes.** "65 x 72" names two different axes: 72 is the training axis (checkpoints `chkpt_00000`..`chkpt_00071`); the simulation axis is `n_frames` per the run's own `_meta.yaml`, separate from the checkpoint count.
- **Observed — (b) the penalty's reduction is not the ablation's reduction.** The penalty reads one central cell per type and discards the first quarter of frames: `activity_mean = activity[:, n_frames // 4 :, self.central_cells_index].mean(dim=1)` (`tools/.venv/Lib/site-packages/flyvis/solver.py:869-872`). Ablation silences all nodes of a type: `make_mask` zeroes the mask entries for the ablated types (`results/night2/diagnostics/ablation/ablation.py:90-98`), applied via `net.register_state_hook(ablate_hook, mask=mask)` (`ablation.py:106`). **Correction to the field list as handed over:** the ablation citation given was `ablation.py:98-104`, in the flyvis package; there is no `ablation.py` under `tools/.venv/Lib/site-packages/flyvis` at all — the file is a project script, `results/night2/diagnostics/ablation/ablation.py`, and the lines that do the silencing are `:90-98` (mask construction) and `:106` (hook registration), not `:98-104`. So "65 numbers" is two instruments under one name and both must be written to the file.
- **Observed — (c) the type axis and the controls.** The type axis must be taken from the same source as row A (`net.connectome.nodes.type`), fingerprinted against `ablation_controls.json` (present at `results/night2/diagnostics/ablation/ablation_controls.json` and `results/night3/diagnostics/ablation/ablation_controls.json`). Controls P1/P2 do not transfer to a passive recording and must be reformulated: P1' — the recording hook does not change the loss; P2' — the instrument sees something.
- **Inferred.** Ark's free falsifier — print the penalised quantity per checkpoint to test whether the 150,000 boundary binds — is cheap and should run before the first row-B value is read.
- **First step.** CC writes the extraction script recording both instruments (penalty-style central-cell read and ablation-style full-type silencing) separately, with the type axis fingerprinted against the same controls file as row A; run only on Mike's word, as an unregistered diagnostic.
- **2026-09-20, CC:** script and protocol are **written and unrun**. `results/night5/diagnostics/rowB/rowB.py` (the extraction; CLI `--netdir`/`--night {4,5,all}`, `--chkpts all|i,j,k`, `--out-dir`, `--dry-run`, `--floor-repeat`, `--floor-summarize`) and `results/night5/diagnostics/rowB/README.md` (the protocol, written before any value exists — the two time axes and the two reductions named separately, axis provenance, P0/P1′/P2′ with P2′'s thresholds left null until a floor exists, the floor procedure, the twin trap, the launch commands, the cost estimate and its source). No checkpoint has been loaded and no network has been run: the only things executed were `python -m py_compile`, `--help`, and `--dry-run`, which resolves paths, h5py shapes, checkpoint counts and the type axis without importing torch or flyvis. `--dry-run` confirms 4 runs × 72 checkpoints keyed by netdir (`9991/903`, `9991/005`, `9991`-side night 4; `9992/000`, `9992/003`, night 5), the type axis identical to row A's census in both `results/night{2,3}/diagnostics/ablation/ablation_controls.json`, and a non-zero exit (code 3) if it ever is not. Two source corrections are recorded in the protocol: `connectome.unique_cell_types` order is asserted equal to the first-appearance order `ablation.py:164` used (they are the same list, now checked rather than assumed), and `side_of_150k` is written under both iteration conventions because `chkpt_iter.h5` stores `solver.iteration - 1`. Neither file is gitignored (`git check-ignore` clean). Launch is Mike's word.
- **axis:** knowledge

## IN PROGRESS

## BLOCKED ON DECISION


### THE-SPREAD-REPLICATE-RATIO-INVERTS-BETWEEN-C3-AND-THE-TOP-RUNG: the between-seed spread at 250,000 is smaller than the replicate offset while at rung C3 it is larger, so the plan's §3 branch is decidable and waits on Mike + reviewers (HIGH, open, 2026-09-15 — CC, from the night 2 rung SDs and the §7 replicate comparison, 2026-09-15)

- **Observed.** Held-out loss at rungs, seed 0/1/2 (docs/experiments/002-night2-seeds-1-and-2.md, results/night2/): 1,000: 1208.9363/1208.0556/1209.7639; 5,000: 1207.7673/1206.7832/1207.0115; 25,000 (C3): 1191.7375/1190.2235/1204.3618; 250,000: 1146.1958/1145.3572/1148.8000. Sample SD over seeds {0,1,2} (n=3): 0.8543/0.5151/7.7627/1.7953 respectively. Replicate |0′−0| (night 1, docs/experiments/001-run0-and-replicate.md §4): 0.0000/0.0025/0.3365/12.7279. Ratio SD/replicate ≈23 at 25,000 (C3, the primary rung), ≈0.14 at 250,000 — the between-seed spread at 250,000 (1.7953) is about seven times smaller than the replicate difference (12.7279), while at C3 it is about 23 times larger (7.7627 vs 0.3365).
- **Inferred.** n=3 gives an SD with 2 degrees of freedom; the §7 measurability clause is applied once at the registered N, so this is a distance, not a verdict — no rho, no ranks, no call on hypothesis (b)/(b2) yet. What it does settle is the branch itself: docs/next-session-plan.md §3's (a) top rung measurable / (b) not measurable is now decidable with these numbers. See [[NIGHT-2-RUNS-SEEDS-1-AND-2-ON-MIKES-WORD]] (closed) and [[THE-REPLICATE-DIFFERS-BY-ONE-POINT-ONE-PERCENT-AT-THE-TOP-RUNG]].
- **Observed, 2026-09-15 (diagnostics, docs/experiments/002-night2-seeds-1-and-2.md §5b):** the hook-path and stored-checkpoint reporting paths agree to ≈1e-4 at checkpoint 250,008 across all four runs, so the 0.7-2.6 top-rung gap between the two paths (§5a item 10) is weight movement over 8 iterations, not two instruments; evaluation noise on one checkpoint is float-level (max deviation 6.72e-5 across 8 re-evaluations plus the stored value). The run-0/run-0' twin weight-space distance at 250,008 is 4.2372, 0.52 of its own mean parameter norm and about three-quarters of the 0.59-0.78 range separating different-seed pairs at the same iteration; the +12.1749 per-item-mean loss gap between the twins is spread over 14 of 16 held-out items (bandage_1's three items carry 47%, ambush_2's three carry 28%), not concentrated in one outlier item.
- **Observed, 2026-09-17 (C3 diagnostic, results/diagnostics/c3/README.md):** the §4/§7 b2
  measurability threshold at C3 was set from a single replicate pair (0/0′, |Δ| 0.3365 at
  25,000). The second replicate pair does not reproduce it: |3′ − 3| at the 25,000 hook is
  5.1847, ≈ 15× larger (5.1847 / 0.3365 = 15.41), and the neighbouring checkpoint at 25,212 gives
  3′ − 3 = −2.9157 — opposite in sign to the registered +0.3365, and the same sign as
  the 25,000 reading, not a flip between the two checkpoints
  (`docs/experiments/004-night4-replicate-3prime-and-seed-5.md` §4, "The C3 finding"). A third
  throw of seed 3 (run 703) reads close to the replicate and far from the original at the C3 hook:
  (703,3) = −4.7582573890686035, (703,3′) = 0.4264798164367676
  (`results/diagnostics/c3/README.md` §7 reading (f)). So the C3/top-rung inversion this entry
  records is itself measured from a threshold — 0.3365 — that is not stable across replicates of
  the same seed; see `ROADMAP.md:154-160`.
- **First step:** Mike + reviewers read docs/experiments/002-night2-seeds-1-and-2.md and choose branch (a) (continue to the floor N, nights 3-5) or (b) (a new pre-registration for the expensive metric before any further N run) per docs/next-session-plan.md §3.
- **axis:** honesty
- **filed:** CC · 2026-09-15

### THE-COMPOSITION-MARGIN-OVER-ITS-FLOOR-IS-SMALLER-THAN-A-NULL-SHIFTS-MEDIAN-DELTA: the registered (a) splice reads "composes predictably" by a 0.40 margin over a floor borrowed from the replicate difference, while a null shift of the same norm moves the loss further and the reverse splice explodes (HIGH, open, 2026-09-15 — CC, from the splice_a diagnostic and Ark's null-shift calibration, 2026-09-15)

- **Observed.** Registered splice T2_A ← T2_B (B = seed 1, A = seed 0, checkpoint 250,008; docs/experiments/002-night2-seeds-1-and-2.md §5g, results/night2/diagnostics/splice_a/): Δ = +38.579946, 3.3583 % of L_A (1148.8074), 3.3659 % of the pre-registration's literal basis 1146.1958. By docs/preregistration-cheap-vs-expensive.md §5 (a)'s rule (floor 38.18, 5 % bound 57.31 on that basis): 38.18 < 38.58 < 57.31 → "composes predictably for this pair", margin 0.40. Self-splice A←A (the mandatory instrument control) is a no-op, +1.4e-5. A null-shift calibration written before the splice (Ark, chat 07:33) drew 20 isotropic random 26-vectors of the same norm as B−A (r = 0.38185): 4 diverge, the 16 finite |Δ| range 10.70-69.55, mean 44.44, median 46.07 — above the registered splice's own 38.58 — and 10 of 16 sit above the floor 38.18. The reverse splice (A→B) gives Δ = +2029.00 (+177.3 %), outside the registered test.
- **Reported.** Ark's calibration (chat 2026-09-15 07:33) and Zcode's bundling it with the splice run (07:43) were both proposed before the registered splice was evaluated; run order verified by the timestamps inside `splice_a/calibration.json` (07:54:06Z) and `splice_a/splice_result.json` (07:55:37Z).
- **Inferred.** The registered category is recorded as the pre-registration's rule reads it, but the margin above the floor (0.40) is smaller than what a directionless shift of the same size does to the loss on the median draw (46.07) — the floor (3× the replicate difference) was not measured from this operation's own null and may not be the right instrument for it.
- **First step.** Mike + reviewers decide the reading: stands as the rule reads it / relabelled uninformative by the calibration / the floor is re-registered from the operation's own null distribution — a floor measured from the operation's own null needs its own registration, not a retrofit onto this one. See [[THE-SPREAD-REPLICATE-RATIO-INVERTS-BETWEEN-C3-AND-THE-TOP-RUNG]].
- **axis:** honesty
- **filed:** CC · 2026-09-15

### N-EQUALS-EIGHT-IS-BELOW-THE-FILES-OWN-MINIMUM: §4 calls N = 10 the minimum at which the test is meaningful and in the same section lets N fall to 8, where power at a true rho of 0.5 is about a third (MEDIUM, open, 2026-09-13 — Zcode 3.3 and Ark 6, chat; filed by CC)

- **Observed.** `docs/preregistration-cheap-vs-expensive.md` §4: "N = 10 is the minimum at
  which the test is meaningful" and, in the rule, "N is never below 8". With m = 1 measured
  (commit e797f02) the rule yields N = 8 at four nights. Power at true ρ = 0.5: ≈ 32 % at
  N = 8, ≈ 41 % at N = 10 (figures as reported; not recomputed here).
- **Inferred.** At N = 8 the honest registered outcome is `inconclusive — underpowered`
  unless agreement is near-perfect; a floor of 10 costs 11 runs including run 0′, six nights
  at two per night.
- **Reported.** Zcode 3.3, Ark 6.
- **First step.** Mike chooses: floor 10 (11 runs incl. run 0′, six nights) or floor 8 with
  `inconclusive — underpowered` registered as the expected outcome. Parent task
  [[HOW-MANY-FULL-RUNS-THE-TEST-IS-ALLOWED]], closed 2026-09-13; one of the fifteen in
  [[PRE-LAUNCH-EDITS-TO-THE-PRE-REGISTRATION-BEFORE-RUN-0]], closed 2026-09-13.
- **axis:** honesty

### THE-REPLICATE-DIFFERS-BY-ONE-POINT-ONE-PERCENT-AT-THE-TOP-RUNG: seed 0 trained twice (run 0, run 0′) lands 1.11 % apart in held-out loss at iteration 250,000, past this file's own 1 % replicate tolerance (HIGH, open, 2026-09-14 — CC, from run 0 / run 0′ per §7)

- **Observed.** Rung table (run 0 / run 0′ held-out loss): 1,000 → 1208.9363 / 1208.9363
  (|Δ| 0.0000); 5,000 → 1207.7673 / 1207.7698 (0.0025); 25,000 → 1191.7375 / 1192.0739
  (0.3365, rel 2.8e-4); **250,000 → 1146.1958 / 1158.9237 (|Δ| 12.7279, rel 1.1104 % →
  FAIL, §7 tolerance is < 1 %)**. Over the 29 common checkpoints after iteration 150,000,
  run 0′ is above run 0 in 29 of 29; mean (run 0′ − run 0) = +12.64 (min 3.68, max 17.82);
  within-run checkpoint standard deviation 6.02 (run 0) / 3.30 (run 0′); the two replicates
  settle on different plateaus, ≈ 1151.7 vs ≈ 1164.3; divergence visible from roughly
  iteration 60,000. Run 0's own minimum held-out loss is 1141.0463 at iteration 219,612;
  held-out loss rose by +0.11 % (1147.5358 → 1148.8075) over the last 50,000 iterations
  (plateau: |change| < 0.2 %). Full tables:
  `results/night1/night_report.md`, `results/night1/night_report_checkpoints.csv`.
- **Inferred.** The instrument floor of the expensive evaluation is ≈ 1.1 % relative, set
  by trajectory divergence under non-deterministic training (determinism flags off, §7),
  not by single-iteration jitter. Per §7 as written, a rung whose between-seed standard
  deviation does not exceed the replicate difference is reported as *unmeasurable*, not as
  a failure of the surrogate — whether the 250,000 rung is measurable for hypothesis (b)
  depends on the between-seed spread at that iteration, unknown until further seeds run
  there (at iteration 1,000 it was 0.52 across 3 seeds, extent probe — a different
  population, not the N population).
- **First step.** Mike + reviewers decide: proceed as registered (the top rung may come out
  *unmeasurable* rather than a surrogate failure) or write a new pre-registration for the
  expensive metric before the N runs. **Proposed (CC), decision Mike + reviewers:** run
  seeds 1 and 2 to 250,000 next night (≈ 4 h each) to get the first between-seed distances
  at the plateau against the 12.64 mean replicate offset above.
- **Experiment record:** `docs/experiments/001-run0-and-replicate.md`; plan:
  `docs/next-session-plan.md`.
- **2026-09-15, CC:** Night 2 gives the top-rung between-seed distances: seed 0/1/2 held-out loss at 250,000 = 1146.1958/1145.3572/1148.8000, sample SD (n=3) = 1.7953, against the replicate |0′−0| of 12.7279 (1.11 %) above — SD/replicate ≈ 0.14, about seven times smaller than the replicate offset. At rung C3 (25,000) the same comparison inverts: SD 7.7627 vs replicate 0.3365, ≈23× larger. n=3 (2 degrees of freedom); no verdict on (b)/(b2) here — see [[THE-SPREAD-REPLICATE-RATIO-INVERTS-BETWEEN-C3-AND-THE-TOP-RUNG]] and docs/experiments/002-night2-seeds-1-and-2.md.
- **2026-09-15, CC (four more diagnostics, docs/experiments/002-night2-seeds-1-and-2.md §5d/§5f):** connectivity — the linear path between run 0 and run 0′ at 250,008 carries a barrier of 96.6 (variant 2) against their 12.7 endpoint gap, and is no better connected than the 0→1 control (115.2 at the same α); the self-path is flat to ≈1e-4, and the design's own resolution criterion is not met, so all barriers are lower bounds. ablation (unregistered) — the twin trap passes on both pre-declared metrics (Euclidean, Spearman) in all three item subsets, but the Euclidean margin over the (0′,1) different-seed pair is only 4 % and a post-hoc Pearson reverses it; the supported claim is that the twins agree in rank order of cell-type importance (ρ 0.72 vs 0.35–0.48 for different seeds), not in their largest single effects (seed 0's top type Tm5c +2,616.8 is +34.6 in seed 0′).
- **2026-09-15, CC:** Ark 10:00: the entry title states half the fact -- after night 2 the statement is "three different individuals sit closer to each other (SD 1.80) than one individual to its own replicate (12.73), seven times", and after the diagnostics "the two ends of one seed sit in different basins (barrier 96.6) like different seeds do"; the title is not rewritten (no backfilling per the format) -- the current statement lives in docs/experiments/002-night2-seeds-1-and-2.md §2/§5d and in [[THE-SPREAD-REPLICATE-RATIO-INVERTS-BETWEEN-C3-AND-THE-TOP-RUNG]].
- **2026-09-17 UTC (2026-09-18 local), CC (night 4 adds a second replicate pair; recomputed by CC from the
  committed values, arithmetic on numbers already in the repo, not a new measurement):**
  - **The second replicate pair.** 3′ − 3 = +10.4309 at 250,000, 0.905 % of seed 3
    (`docs/experiments/004-night4-replicate-3prime-and-seed-5.md:91`) — the same order of
    magnitude as the first pair's +12.7279 (1.11 %).
  - **The population fact.** σ = 1.7953 at the 250,000 hook is the sample sd over seeds {0,1,2}
    only, n=3 (`docs/experiments/002-night2-seeds-1-and-2.md:71`), while the sd over all six seeds
    {0..5} at the same rung is 5.1425 (`docs/experiments/004-night4-replicate-3prime-and-seed-5.md:81`)
    — a factor of 2.86 (5.1425 / 1.7953).
  - **The consequence for the replicate-cost estimate.** With r > (σ_rep/σ_between)², σ_rep from
    the single first pair (12.7279 / 1.128 = 11.28) and the n=3 σ (1.7953) gives r = (11.28 /
    1.7953)² = 39.5 ≈ 40, matching the figure already on record at
    `docs/experiments/002-night2-seeds-1-and-2.md:234-236` (≈ 53 nights at N = 8). Using instead
    the n=6 σ (5.1425) with both replicate pairs — σ_rep = mean(|12.7279|, |10.4309|) / 1.128 =
    11.5794 / 1.128 = 10.27 — gives r = (10.27 / 5.1425)² = 4.0, ≈ 5.3 nights in the same
    conversion (4.0 × 53/40). The cost estimate swings from ≈ 53 nights to ≈ 5 depending on which
    seed population supplies the denominator.
  - **The variance comparison.** Within-individual variance ≈ 105–127 (σ_rep 10.27² = 105.5 to
    11.28² = 127.2) sits above the between-seed variance at n=6, 5.1425² = 26.4 — the observed
    between-seed spread is smaller than the twin noise. The record's own 95 % χ² CI for σ(n=6) at
    250,000 is [3.2100, 12.6126]
    (`docs/experiments/004-night4-replicate-3prime-and-seed-5.md:105`).
  - **A units defect in the line above, found in review and corrected here** (Ark, 2026-09-17 UTC;
    verified by CC at source the same day). An earlier version of this note put that interval next
    to the twin gap 12.7279 and reported its upper bound as sitting "just below" it. Those are two
    kinds of quantity: on the left an interval for a **standard deviation**, on the right the
    **difference of two runs**. Brought to common units under the normal-difference convention
    σ = |Δ|/1.128379 — which is an **assumption, not a measurement** — the twin difference is
    σ_rep = 11.28, and then the n=6 interval [3.2100, 12.6126] **contains** it while the n=5
    interval [2.1225, 10.1801] does not. So the direction does not survive the change of units:
    with five individuals the spread is distinguishable from the replicate, with six it is not.
    The same comparison stands in `docs/next-session-plan.md` §2a and carries the same defect;
    an override is recorded there rather than a rewrite of the record.
  - **The source record's own wording**, kept for the trail
    (`docs/experiments/004-night4-replicate-3prime-and-seed-5.md:113-114`: "the CI upper bound
    (12.61) now sits just below the run-0/0′ replicate offset (12.73)").
  - **CC's reading, 2026-09-17 UTC (2026-09-18 local), not reviewed:** if the top rung's test-retest reliability is
    indistinguishable from zero, any cheap-vs-expensive correlation is bounded above by that
    reliability, so the ρ preview cannot be read as a statement about individuals until the top
    rung shows reliability above zero.
- **axis:** honesty
