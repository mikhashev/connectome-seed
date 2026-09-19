# Closed entries

## 2026-09-19 — closed by CC

### THE-REGISTERED-READING-SCRIPT-CANNOT-COMPLETE-ON-THE-SUBSTRATE-IT-IS-REGISTERED-AGAINST: two of the eight runs resolve to no column, so the one permitted run of the reachability reading refuses with exit 2 before computing a single crossing time (HIGH, open, 2026-09-18 — CC, by executing the mapping stage after Ark asked whether the script refuses a non-canonical input; three review rounds by three authors had not found it)

- **Observed.** On the real tree, mapping stage only, no `cross(r, L)` computed: `9991/000` and `9991/900` get **zero** candidate columns and `assign_runs` raises `MappingRefusal` → exit 2, whose own banner reads "the reading did not happen". Reproduced end to end through `tools/reachability/synthetic_reading_harness.py` on fabricated data: both cases exit 2 at §3 step 1.
- **Observed — the cause is in two independent places.** (i) `build_candidates` accepts a combined `val_loss_seed<N>[prime]` column only when that run is bound in **the night whose file carries the column** (`spec[0] in info["bound"]`). The per-night reports accumulate, so `val_loss_seed0` and `val_loss_seed0prime` appear in nights 2, 3 and 4, while only night 1 binds those two runs — all six columns are therefore discarded as unmapped. (ii) `assign_runs` additionally requires a candidate **in the run's registered night** (`c["night"] == reg_night`), and night 1's own report names its columns `val_loss_A` / `val_loss_B`, which match no registered grammar and which night 1 has no pairwise files to disambiguate.
- **Observed.** Night 1's `val_loss_A` / `val_loss_B` are **undocumented**: no record in the repository says which run is which, and they cannot be identified by byte equality either — neither matches night 4's `val_loss_seed0` or `val_loss_seed0prime` as strings, because night 4's report is full-float from the run jsons while the older reports are 4-decimal (night 4's own header comment says so).
- **Observed — the obvious fix makes it worse, measured.** Relaxing (i) to "bound in any night's waves" gives runs 0 and 0′ three candidates each, and takes the failure count from **2 to 6**: runs 1, 2, 3 and 4 then acquire off-night candidates whose printed precision differs from their on-night column, and the bitwise agreement check refuses. Reverted; the script's sha256 is unchanged.
- **Inferred, and this is the direction rather than a patch.** The registered substrate is **night 4's file alone** (registration §2: "the one file that carries all eight runs — 72 data rows, 8 run columns"), and that file already carries all eight runs as seed-named columns. The mapping the test needs is entirely inside the registered file; the night-scoped resolver logic is what breaks it. A fix that makes the registered substrate the primary source, and treats other nights' reports as corroboration compared **numerically** rather than bytewise, addresses both halves. It is a change to the resolver, which Zcode wrote and which both reviewers have just closed review on, so it needs their round rather than my patch.
- **Blocks.** The (c)4 reading, for which Mike gave the word on 2026-09-18 08:05 UTC. The word stands; the instrument does not run. Nothing was read: no crossing time of the substrate has been computed at any point.
- **axis:** collective
**Closed:** S2026-09-19.1 · 2026-09-19 · fixed · the multi-night resolver was removed (v7, `eb4aaf1`, −234 lines, 17 identifiers, zero dangling references) and replaced by the registered file alone with its pinned header as the mapping and its LF-normalised sha256 `f61c5aaf…` as the identity, checked before anything is read. The reading then ran to completion on 2026-09-18 09:30:53Z and returned `TEST UNREADABLE`; raw output in `results/diagnostics/reachability/`. The defect was found by execution after three review rounds by three authors had not found it.

### THE-SCRIPTS-REGISTERED-IDENTITY-IS-ITS-SHA256-AND-THAT-NUMBER-DEPENDS-ON-THE-CHECKOUTS-LINE-ENDINGS: the reading script hashes its own working-tree bytes, `core.autocrlf` is true and there is no `.gitattributes`, so the identity the reading prints is not the identity the repository stores (MEDIUM, open, 2026-09-18 — CC, on noticing the hash change after `git checkout` of an unmodified file)

- **Observed.** Same commit, same file, two numbers: the committed blob (LF) is `5c8d87017a77887d17e4beda66dd17f1d88a73f8b256f48670de22d77cc461bf`; the working-tree file (CRLF) is `d67278e74a5b056b3ea23ec29c091db5fa22c8be34b9e3a99dd46af07dda3b06`. `git config core.autocrlf` = `true`, and the repository has no `.gitattributes`.
- **Observed.** The script hashes `Path(__file__).resolve().read_bytes()`, so what it prints at the head of the reading is the **working-tree** value — `d67278e7…` on this checkout, and `5c8d8701…` on any checkout that keeps LF. The registration's §10 rests on that number: "its identity is its sha256, printed at the head of its own output; a line count is not registered, because it moves with every edit while looking checkable". The sha256 moves with the checkout while looking checkable, which is the same property the line count was rejected for.
- **Observed — I published the wrong one.** The v5 commit message states "the script is untouched and its sha256 stands at `5c8d8701…`". That is the blob's hash, not the number the reading will print. Right number, wrong object: the same class as a measurement labelled with a set it was not measured over.
- **First step.** Decide between `.gitattributes` with `* text eol=lf` (makes working tree and blob agree, but rewrites every file's line endings and so moves the printed hash once, deliberately), and recording both numbers in §10 with what each one is (docs-only, no rewrite). The second is available immediately; the first is the durable one and is cheapest to do in the same round as the resolver fix, since that round moves the hash anyway. See [[THE-REGISTERED-READING-SCRIPT-CANNOT-COMPLETE-ON-THE-SUBSTRATE-IT-IS-REGISTERED-AGAINST]].
- **axis:** collective
**Closed:** S2026-09-19.2 · 2026-09-19 · fixed · every hashed input and the script's own bytes are normalised to LF before hashing (v7), so the printed identity equals the git blob's content hash and does not move with `core.autocrlf`. Verified by three witnesses on the substrate: working tree with 73 CRLF pairs, `HEAD` blob with none, and the registered value — one number, `f61c5aaf…`.

### A-REACHABILITY-ENDPOINT-IS-PROPOSED-AND-NOT-REGISTERED-WHILE-ITS-SUBSTRATE-ALREADY-SITS-ON-DISK: iterations-to-cross a fixed aggregate val_loss level is proposed as the endpoint class that survives run-to-run scatter, the 72-checkpoint curves of all eight runs are already stored, and nothing about it is pre-registered (HIGH, open, 2026-09-17 — CC, from the 2026-09-17 USPEX review thread; drafting assigned to Zcode)

- **Observed.** The USPEX statistic our own (b) test was compared against counts **steps to a target fixed outside the run** (generations and structures to `E = 90.912`), not the order of final states — `research/uspex/2026-09-17-uspex-analogue-to-adr-002.md` §(b)1, §(c)4. Run-to-run scatter moves a time-to-target and destroys an order of finals.
- **Observed.** The substrate is already stored, so the test costs no GPU and no night: 72 aggregate `val_loss` checkpoints per run for all eight runs, on a grid that is **not uniform** — iterations 0, 12, then 3,600 apart, with a final step of 1,596 to 250,008 (`results/night4/night_report_checkpoints.csv`).
- **Observed.** The curve is a **different field** from the 250,000 hook and its replicate gaps are its own: at 250,008 the curve gives `0′ − 0 = 12.1749` and `3′ − 3 = 7.6059` against the hook's 12.7279 and 10.4309, with a trained spread of 18.7403 (same file; recomputed by CC 2026-09-17 UTC from the stored values).
- **Observed.** A positive control exists in the same table: the untrained level is 1212.5556 and the learned gain within the curve field is 63.7481 for seed 0 — about five times the largest replicate gap.
- **Inferred.** Because §(c)1a leaves the cost of N unestimable (the moment estimate of the between-individual variance is negative), this free test is the only step that can settle the **class** of the endpoint before any night is bought. It is a recommendation of the review thread, **not a decision**: no rule changes until it is registered and read.
- **First step.** Zcode drafts the registration in the repository's style — threshold grid stated as a rule, acceptance criterion in one sentence, the measured resolution, a disqualification clause for the case where the replicate difference is ≲ one grid step, the positive control above, the field named, and the inherited item-weighting fragility — per `docs/plans/2026-09-17-endpoint-before-n.md` §4; Ark and CC review it **before any data is touched**.
- **axis:** knowledge
**Closed:** S2026-09-19.3 · 2026-09-19 · fixed · registered as `docs/preregistration-reachability-endpoint.md` (seven revisions, three review rounds by three authors), read **once** on Mike's word 2026-09-18, verdict `TEST UNREADABLE` (16 of 23 levels dropped, all on the twin side). Closed in that form and not to be re-read — see [[ADR-003]] on blind authorship.

### MACHINE-STATE-WAS-ADDED-TO-THE-RUN-JSON-BUT-NEVER-EXERCISED-BY-A-RUN: a machine-state snapshot field landed in the night runner on 2026-09-17, after night 4 had already finished, and no run or diagnostic since has taken that code path (MEDIUM, open, 2026-09-17 — CC, from commit 4f1b30c and a grep of the four completed nights)

- **Observed.** Commit `4f1b30c` (2026-09-17T08:38:54Z UTC) adds two call sites to
  `tools/night/run_individual.py`: `rec["machine_state_start"] = _machine_state()` at line 699,
  before the training reseed and the wall-clock start, and `rec["machine_state_end"] =
  _machine_state()` at line 749, inside the existing `finally:` block.
- **Observed.** No json under `results/night1`, `results/night2`, `results/night3` or
  `results/night4` contains the string `machine_state` — all four completed nights predate the
  patch.
- **Observed.** Step 1 (gray stimulus, commit `32759e2`, same day) ran through
  `results/diagnostics/gray/gray_stimulus.py`, which imports `diag1_eval_paths`, `ablation` and
  `rowB` (`gray_stimulus.py:127-129`) and does not import `run_individual` — step 1 never took
  the patched code path either.
- **Observed.** `4f1b30c` landed 2026-09-17T08:38:54Z (UTC); night 4's last commit `f3b02e2` was
  2026-09-17T05:56:41Z (UTC) — the patch landed after night 4 had already finished and been
  recorded, not before it.
- **Observed.** `results/diagnostics/c3/machine_state.json` is a separate artefact — the C3
  diagnostic's own 5-record machine-state log (`results/diagnostics/c3/README.md:27`: "5 records:
  start, after B, before A1, after A1/before B′, end"), written by that diagnostic's own harness,
  not by the `rec["machine_state_start"/"_end"]` field this entry is about.
- **Inferred.** The commit's own verification (git apply, py_compile, parse_args byte-identity, a
  standalone `_machine_state()` call) checks the patch statically; none of it exercises the field
  inside an actual training run. The field's first real exercise is whatever night run comes next.
- **First step.** The next night run will be the first to carry `machine_state_start` and
  `machine_state_end` in its json; check their presence and shape then.
- **axis:** honesty
**Closed:** S2026-09-19.4 · 2026-09-19 · fixed · night 5 is the first run to carry the field, and it did the job it was added for: all four records report `boot_time_utc = 2026-09-14T23:31:12Z` and strictly increasing `uptime_s` within each run and across the pair, which is what establishes that both new runs belong to boot session B — the fact the degrees-of-freedom arithmetic of the night depends on. Its first use also fired the slim-json key check in `extract_night5.py`, correctly, because the two keys are new against the night-4 reference.

### THE-ONLY-RUNNABLE-ENVIRONMENT-LIVES-IN-A-SCRATCHPAD-OF-A-SESSION-THAT-HAS-ENDED: every night since 2026-09-13 ran from a venv under a temporary per-session directory whose owning session is gone, and the repository's own copy of the launcher cannot start a night at all (HIGH, in progress, 2026-09-17 — Mike «Переезд — надо сделать обязательно, заведи таску HIGH в новой сесси с него начнем потом»; raised by Ark, confirmed by CC)

- **Observed.** All nine job records across the five wave files name one interpreter and one script copy, under `%LOCALAPPDATA%\Temp\claude\c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx\63f3961a-96ce-4048-8338-72c162ea66f8\scratchpadlyvis-probe\` (Ark, 2026-09-17, from `results/night{1,2,3,4}/wave_*.json`). That session id is **not** the session running today, so the directory has no owner: nothing refreshes it, and any cleanup of stale per-session scratchpads takes the project's only venv with it (CC, 2026-09-17).
- **Observed.** The copy has not drifted: `run_individual.py`, `launch_wave.py` and `start_night.ps1` are byte-identical between `tools/night/` and that scratchpad (sha256 `be007c74…`, `ad206bd8…`, `117379c8…`; CC, 2026-09-17). The risk is disappearance, not divergence.
- **Observed.** The repository copy cannot launch a night as it stands. `start_night.ps1:46` derives the interpreter as `Split-Path -Parent $PSScriptRoot` + `.venv\Scripts\python.exe` — from `tools/night/` that is `tools/.venv`, which does not exist — and `:56` throws `venv python not found: $py`. `launch_wave.py:35` has the same broken default but `:77` accepts `--python`, so that one file is usable when the interpreter is passed explicitly: the default is broken, not the capability (CC, 2026-09-17).
- **Inferred.** A migration that moves only the venv and leaves the launcher deriving its interpreter from the script's parent directory exchanges one orphaned directory for another. The move and a launcher that runs from the repository are one task, not two (Ark, 2026-09-17).
- **Done, 2026-09-18 (CC).** The environment was copied out of the ended session's scratchpad into `tools/.venv` — 25,221 files, 4.85 GiB, robocopy reporting 0 failures — and answers from its new path: `python 3.10.20`, `torch 2.9.1+cu128` with `torch.cuda.is_available() == True`, `flyvis 1.2.0`. No launcher change was needed after all: `start_night.ps1:43-46` derives the interpreter as the script's parent plus `.venv\Scripts\python.exe`, which from the committed `tools/night/` is exactly `tools/.venv`, so putting the venv at that path makes the existing derivation correct instead of broken. Ark's "the move and a launcher that runs from the repository are one task" holds, and the cheaper half of it turned out to be a copy to the right place rather than a new `--python` argument.
- **Done, 2026-09-18 (CC).** `tools\night\start_night.ps1 -DryRun -Tag night5 -Ensemble 9992 -Seeds "3,0" -NoReplicate`, run **from the repository**, reaches the launcher and prints its two jobs (`9992/003` seed 3 first, `9992/000` seed 0 second, both tag `night5`) and `[dry] 2 commands; mode=sequential; detach=True; nothing started`. This is the first time the committed copy has been shown to start a night; before it, it threw at `:56` before reaching the launcher.
- **Observed, 2026-09-18 (CC).** The move changes where a night's raw output lands: `--out-dir` is the launcher's own directory and `start_night.ps1` never overrides it, so night 5 onward writes its per-run json/log/stdout triples and the wave's pid/progress/launcher files **into `tools/night/` inside the repository**, where nights 1-4 wrote into the scratchpad. Ignore rules were added for exactly those names (`tools/night/*.json`, `tools/night/*.log`, `tools/night/wave_*.pid`) and verified with `git check-ignore` against the seven filenames night 5 will write, because a wave in flight would otherwise leave the tree dirty — the state a pre-registration's own guard refuses to run in. Nothing of that shape has ever been in history; the committed trace stays the distilled `results/night*/`.
- **Observed, 2026-09-18 (CC).** A copy is an assumption until it is hashed, so both trees were hashed file by file (sha256, `__pycache__` excluded) and compared by a combined digest over the sorted (path, hash) pairs. **Result: identical** — 21,650 files on each side with `__pycache__` excluded, combined digest `94f7f483e8410e54887c98b20d520872823f1ba5ad9fa1c12d6b95359da7e318` on both, zero files differing and zero present in one tree only. The requirement now lives as a gate in `docs/briefs/2026-09-17-night5.md` §4 gate 8: if the digests ever disagree, night 5's curves are not comparable to nights 1-4's.
- **Still open.** Ark's acceptance condition is unmet by construction: it requires a **full run's** `json_iter_wall_median_all_s` to land inside **[0.0598, 0.0622]**, which no dry run can supply. The entry stays open until a night has run from `tools/.venv` and its timing gates are read (night 5's §4 gate 4 is the instrument). Also unresolved: the scratchpad copy is still the only place nights 1-4's raw artefacts exist, and deleting it is a separate decision from moving the environment.
- **First step.** Give the environment a home outside `Temp` and outside any session-scoped path; make `start_night.ps1` accept an explicit interpreter path (or resolve one that exists in the repository layout); then re-verify with `-DryRun` from the repository copy, and accept the move only if a full run's `json_iter_wall_median_all_s` stays inside **[0.0598, 0.0622]** — the band of all eight runs on record, spread 4.10 % across four days and one restart (Ark, 2026-09-17). Mike's word: start the next session with this.
- **axis:** collective
**Closed:** S2026-09-19.5 · 2026-09-19 · fixed · the environment lives at `tools/.venv`, hash-identical to the copy that trained nights 1–4 (21,650 files, one combined digest, zero differing), and **night 5 ran from it** — the first night launched from the repository. Comparability confirmed by gate 7 rather than by timing: 162 of 162 invariant config lines match for both runs. Ark's timing acceptance band is **not** used as the closing evidence, because the band is itself defective — spun out as its own entry below.

## 2026-09-17 — closed by CC

### NIGHT-4-RUNS-REPLICATE-3-PRIME-AND-SEED-5-TO-COMPLETION: replicate 3prime (seed 3, id 9991/903) and seed 5 (id 9991/005) trained to 250,000 in one wave with no reboot, the third same-wave pair on record, pushing the individual population to n=6 at the top rung (HIGH, closed, 2026-09-17 — CC, from wave_night4.json: WAVE DONE 2/2 ok 2026-09-17T04:29:27Z; launch pre-registered in docs/next-session-plan.md sec2a (Ark 19:58Z/Zcode 20:14Z, committed 874cc32))

**Closed:** S2026-09-17.1 · 2026-09-17 · fixed · replicate 3prime (9991/903) EXIT rc=0, 250008 iterations, 14444.2s; seed 5 (9991/005) EXIT rc=0, 250008 iterations, 14474.1s; WAVE DONE 2/2 ok 2026-09-17T04:29:27Z; eight-run rung SD at n=6: 1.3012/0.9639/8.0614/5.1425 vs replicate 0.0000/0.0025/0.3365/12.7279; record docs/experiments/004-night4-replicate-3prime-and-seed-5.md and results/night4/ · closed by CC

- **Observed.** wave_night4.json/.launcher.log: WAVE START tag=night4 2026-09-16T20:27:29Z, replicate 3prime (9991/903) EXIT rc=0 250008 iterations 14444.2s (launcher wall), seed 5 (9991/005) EXIT rc=0 250008 iterations 14474.1s, WAVE DONE 2/2 ok 2026-09-17T04:29:27Z, one wave start to end no reboot, 72 checkpoints each, errors 0; rung SD at n=6 (individuals 0,1,2,3,4,5): 1.3012/0.9639/8.0614/5.1425 against replicate |0prime-0| 0.0000/0.0025/0.3365/12.7279 (docs/experiments/004-night4-replicate-3prime-and-seed-5.md sec2); second replicate pair |3prime-3|=10.4309 at 250000 rules out the position-effect explanation P (docs/next-session-plan.md sec2a); C3 replicate offset 0.3365 (pair 0/0prime) not reproduced by |3prime-3|=5.1847 at 25000, about 15x larger (sec4)
- **First step:** None -- closed on completion; the C3 threshold instability and the position-effect ruling are recorded as observations in docs/experiments/004-night4-replicate-3prime-and-seed-5.md sec4, no rule changed
- **axis:** honesty
- **filed:** CC · 2026-09-17

### THE-GRAY-STIMULUS-CONTROL-TESTS-LEARNED-EQUALS-VISION-FROM-THE-SECOND-SIDE: replacing the visual input with constant gray or zero on all seven checkpoints should return ~1212 for five runs and reproduce seed 2's explosion only if the photoreceptor-ablation dependence is real (HIGH, closed, 2026-09-16 — CC, docs/plans/2026-09-16-functional-readout-plan.md step 1)

**Closed:** S2026-09-17.2 · 2026-09-17 · fixed · v5.1 (commit `32759e2`, launched on Mike's word
2026-09-17 08:37:30Z, run by a CC subagent 08:49–09:05Z): reading (i) holds for all six seeds —
gray removes ≥ 90 % of the learned gain (`results/diagnostics/gray/README.md:187`); reading (ii)
seed 2 does not explode without drive — gray excess −3.260504627227874 ("returns"), zero-clamp
excess −0.6886240005492255 ("returns") (`results/diagnostics/gray/README.md:199-202`), so by the
brief's own pre-registered branch the R2 photoreceptor-ablation explosion (+21,158) is an
instrument artefact of the forced-zero clamp, not a vision dependence, and the R2 finding is to be
reworded accordingly (`results/diagnostics/gray/README.md:204-208`); reading (iii) shuffled frames
read worse (higher loss) than untrained gray in every one of the six seeds
(`results/diagnostics/gray/README.md:229-231`); summarised in `ROADMAP.md:213-217` · closed by CC

- **Observed.** `docs/experiments/003-night3-seeds-3-and-4.md` §6c: held-out loss at iteration 0
  is ≈1212.55 across all six seeds; R1–R8 silenced (photoreceptor ablation) returns five of six
  seeds to 0.91–1.42× that level (essentially the whole learned gain removed) while seed 2
  explodes to 31,773.93, 26× the untrained level. The reading that "five of six runs barely
  depend on input" is withdrawn by its authors (Ark, Zcode, 06:03–06:04Z) precisely because
  ablation *does* remove the gain in those five.
- **Inferred.** Ablation forces photoreceptor activity to zero via a state hook; a gray/zero
  stimulus control is a second, independent way to remove visual information. If it reproduces (i)
  ≈1212 for five seeds and (ii) an explosion for seed 2, "learned = vision" is closed from a second
  side and seed 2's dependence is confirmed as real rather than an ablation-hook artefact.
- **Observed 2026-09-17 (v5.1, commit `32759e2`, `results/diagnostics/gray/README.md`).** All
  three readings ran to completion against the six trained checkpoints and each run's iteration-0
  checkpoint, same 16 items and evaluator, no ablation hook registered
  (`net._state_hooks == ()` asserted before and after every call). Reading (i), all 6 seeds:
  |L_trained_gray − L_untrained_gray| ≤ 0.1·gain_s holds in every seed, i.e. gray input removes
  ≥ 90 % of the learned gain (`README.md:187-197`). Reading (ii), seed 2: gray excess
  `-3.260504627227874` and zero excess `-0.6886240005492255`, both classified "returns" under the
  brief's ≤ 0.1·gain_s rule — seed 2 does *not* explode without drive (`README.md:199-202`); per
  the brief's own branch text this makes the ablation deltas (+21,158 R2 single-type clamp-to-0,
  +30,626 full R1–R8 clamp-to-0) "the dynamics' fragility to a zero clamp specifically, an
  instrument artefact, not a vision dependence" (`README.md:204-208`). Reading (iii), shuffled: all
  6 seeds read "between" the two references and, recorded separately, the shuffled loss sits
  *above both* references in every seed (≈ 1.2–1.9 gain_s above L_untrained_gray) — shuffled frames
  are worse than an untrained network (`README.md:215-231`).
- **First step.** None — closed on completion. See also
  [[THE-LEARNED-GAIN-IS-SIXTY-LOSS-UNITS-ON-AN-UNTRAINED-LEVEL-OF-TWELVE-HUNDRED]] and
  [[THE-TUNING-BATTERY-CHECKS-WHETHER-THE-DOMINANT-ABLATION-TYPE-IS-FUNCTIONAL]] (step 2, now
  unblocked).
- **axis:** knowledge
- **filed:** CC · 2026-09-16

### A-WINDOW-INTEGRAL-STATISTIC-WAS-COMPUTED-AND-REJECTED-BY-ITS-OWN-CRITERION: a checkpoint-window mean was proposed as a cheaper stand-in for the C3 point statistic, and every window variant's rank correlation with the 250,000 hook falls below the point statistic's own, failing the brief's own pre-registered promotion rule (MEDIUM, closed, 2026-09-17 — CC, docs/briefs/2026-09-17-window-integral-cheap-statistic.md, computed by window_integral.py)

**Closed:** S2026-09-17.2 · 2026-09-17 · disproved · commit `155e3f4`: per-window Spearman ρ
against the 250,000 hook (n=6 individuals) ranges 0.4857–0.7143 across the five window variants
tested (A narrow, A wide, W1, W2, W3), all below the point statistic's own ρ = 0.8857
(`results/diagnostics/window/README.md:155-162`); the brief's promotion criterion requires both a
reduced within-seed spread AND ρ(window) ≥ ρ(point), and condition (ii) fails for every window
regardless of how the third throw of seed 3 (run 703) is handled in condition (i)
(`results/diagnostics/window/README.md §7`, table `:222-228`, conclusion `:230-233`: "no window
statistic is a candidate for the next registration on this record") · closed by CC

- **Observed.** `docs/briefs/2026-09-17-window-integral-cheap-statistic.md` v1.1 registered five
  window variants (checkpoint-window means at two widths plus three shifted windows) and a
  promotion criterion: both (i) within-seed spread reduced to ≤ 0.5× the point statistic's spread,
  and (ii) ρ(window) with the 250,000 hook ≥ ρ(point) = 0.8857, must hold for a window to become a
  candidate for the next pre-registration.
- **Observed.** `window_integral.py` (sha256 `9a10dbad…`) computed all quantities from the eight
  stored run jsons and run 703, CPU only, no GPU, no write to `connectome-seed-data`, no change to
  `docs/preregistration-cheap-vs-expensive.md`. Every window variant's ρ with the 250,000 hook
  (0.4857–0.7143) sits below the point statistic's ρ (0.8857); condition (i) alone clears for some
  windows depending on whether run 703 is included in the seed-3 set, but condition (ii) never
  clears for any window (`results/diagnostics/window/README.md` §7 table).
- **Inferred.** By the brief's own fixed rule ("either condition failing … means not a candidate as
  proposed"), no window statistic on this record is a candidate for the next registration. This is
  the pre-registered criterion mechanically applied, not a new judgment about the window
  statistic's worth (`results/diagnostics/window/README.md` §8).
- **First step.** None — closed on completion; the point statistic's own ρ = 0.8857 at n=6 is
  itself a preview, not a test — see
  [[THE-POINT-STATISTICS-RHO-PREVIEW-AT-N-EQUALS-SIX-MUST-NOT-BE-CITED-AS-THE-TEST]].
- **axis:** honesty
- **filed:** CC · 2026-09-17

## 2026-09-16 — closed by CC

### THE-MACHINE-VERDICT-ON-THE-NIGHT-3-ABLATION-READING-WAS-OVERRIDDEN: ablation_reading.json's own POSITIVE verdict evaluated only one of the pre-registered rule's two conflicting size definitions, and R2 itself did not repeat (HIGH, closed, 2026-09-16 — Mike «давайте пробовать», reviewers Ark 05:27Z and Zcode 05:27Z concurring)

**Closed:** S2026-09-16.1 · 2026-09-16 · fixed · override note inserted at the top of
`docs/experiments/003-night3-seeds-3-and-4.md` §6 (before item 1 of the ablation block) and at
the top of `results/night3/diagnostics/ablation/README.md`; checklist rule 16 added
(`docs/CHECKLIST-research-repo.md`); `ablation_reading.json` left unchanged as the artefact of
what the script printed · closed by CC

- **Observed.** `results/night3/diagnostics/ablation/ablation_reading.json`:
  `"verdict": {"positive_reading_triggered": true, "text": "POSITIVE: a single-type dependence
  exceeding 2863 appears in seed 3 or seed 4 -> the R2 finding becomes a REPEATED OBSERVATION,
  still not a test."}`. `docs/next-session-plan.md` §2a's rule carries two different size
  definitions for the same clause ("of the size seen in seed 2, +21,157" vs "exceeds 2863", the
  twin discrepancy bound); `ablation_night3.py:466-476` executed only the second, operational
  one. Δ_R2 across the six runs is +459.2 / +679.8 / −1.0 / +21,157.5 / +146.9 / +41.8 for
  seeds 0/0′/1/2/3/4 (`docs/experiments/003-night3-seeds-3-and-4.md` §6 item 2) — seeds 3 and 4
  are at +146.9 / +41.8, not the +21,157.5 seen in seed 2. The 2863 threshold is met by 5 of the
  6 runs on record, so it does not discriminate a repeat from the background rate.
- **Inferred.** The rule's own internal contradiction means the outcome under the rule as
  written is undetermined by defect of the rule, not positive as the json's `verdict` field
  states. This is a pre-registration defect, recorded in the record with a dated override note
  rather than corrected in the json, which stays as the artefact of what the script printed —
  checklist rule 16 generalises this.
- **First step.** None — closed on completion.
- **axis:** honesty
- **filed:** CC · 2026-09-16

### NIGHT-3-RUNS-SEEDS-3-AND-4-ON-MIKES-WORD: seeds 3 and 4 trained to 250,000 in one wave with no reboot, the second same-wave pair after seeds 0/0prime, pushing the rung SD to n=5 (HIGH, closed, 2026-09-16 — Mike, DPC Research chat 2026-09-16T04:46Z: «Ночной прогон завершен»)

**Closed:** S2026-09-16.1 · 2026-09-16 · fixed · seed 3 (9991/003) EXIT rc=0, 250,008 iterations, 14415.1s; seed 4 (9991/004) EXIT rc=0, 250,008 iterations, 14684.5s; WAVE DONE 2/2 ok 2026-09-16T04:40:23Z, one wave no reboot; six-run rung SD at n=5: 1.2698/0.8173/8.3788/3.5426 vs replicate 0.0000/0.0025/0.3365/12.7279; record docs/experiments/003-night3-seeds-3-and-4.md and results/night3/ · closed by CC

- **Observed.** wave_night3.json/.launcher.log: WAVE START tag=night3 2026-09-15T20:35:23Z, seed 3 (9991/003) EXIT rc=0 250,008 iterations 14415.1s, seed 4 (9991/004) EXIT rc=0 250,008 iterations 14684.5s, WAVE DONE 2/2 ok 2026-09-16T04:40:23Z, one wave start to end, no reboot, 72 checkpoints each, VRAM 1426.1 MiB, errors 0; rung SD at n=5 (seeds 0,1,2,3,4): 1.2698/0.8173/8.3788/3.5426 against replicate |0prime-0| 0.0000/0.0025/0.3365/12.7279 (docs/experiments/003-night3-seeds-3-and-4.md sec2); within-wave second same-wave pair (seed4-seed3) is positive at only 6/29 late checkpoints, vs (0prime-0) 29/29 (sec3)
- **First step:** None -- closed on completion; the pre-registered ablation/rowB readings of docs/next-session-plan.md sec2a are evaluated in results/night3/diagnostics/{ablation,rowB}/, not here
- **axis:** honesty
- **filed:** CC · 2026-09-16

## 2026-09-15 — closed by CC

### ROW-B-CELL-TYPE-ACTIVITY-PROFILES-RUN-AS-A-PREVIEW-AT-N-EQUALS-FIVE-OR-SIX: row B (65 per-type activity profiles across P0/P1/P2 and the twin trap) runs from the 72 saved checkpoints of seeds 0, 0′, 1, 2 as a preview diagnostic, never read as a test until N ≥ 8 (MEDIUM, closed, 2026-09-15 — Mike 09:56 «делай ряд B»; protocol `docs/proposals/mi-axis-per-cell-type-design.md`; taken by CC)

**Closed:** S2026-09-15.1 · 2026-09-15 · fixed · rowB.py run against the 72 saved checkpoints of seeds 0, 0prime, 1, 2 (results/night2/diagnostics/rowB/); P0 graduated ladder at iter 0 in order (0,0prime)=0.000000, (0,1)=0.1736, (1,2)=0.2110; floor (3 fresh processes, seed0@250008) rank rho=1.0000, max|deltaB|=8.25e-8; P2 (silence R1-R8) moves B on 64-65/65 types per seed, loss +58.43/+47.02/+64.87/+30626.21; twin-trap PASS: d(0,0prime)=0.3487 is the minimum of the six pairs, nearest foreign (0,2)=0.5455, margin 0.1968 over floor 0.0, minimum in 16/16 items; B vs row-A within-individual rho=+0.389/+0.481/+0.563/+0.653; write-up docs/experiments/002-night2-seeds-1-and-2.md sec5i; PREVIEW DIAGNOSTIC n=4, not read as a test · closed by CC

- **Observed.** Mike's word (DPC Research chat, 2026-09-15 09:56 UTC: «делай ряд B»). Protocol:
  `docs/proposals/mi-axis-per-cell-type-design.md` — 65 per-type means + within-type spread, P0
  (cross-process reproducibility), P1, P2, the twin trap, Spearman ρ pre-fixed as the measure,
  all 16 held-out items. Source: the 72 saved checkpoints of seeds 0, 0′, 1, 2 (`results/night1/`,
  `results/night2/`).
- **Inferred.** At n = 5–6 seeds the critical ρ is 0.90–1.00
  (`docs/next-session-plan.md` §5: "Do not read row B as a test at N < 8"); this run is a
  preview and cannot be read as a hypothesis test.
- **First step.** CC runs the protocol against the 72 checkpoints; results to
  `results/night2/diagnostics/rowB/`.
- **axis:** knowledge
- **taken:** CC · 2026-09-15

### RUN-0-SHOWS-WHERE-THE-LOSS-PLATEAUS: run 0's rungs and checkpoints will show where held-out loss stops moving, and if that is far before 250,000 the expensive evaluation could be redefined cheaper — only by a new pre-registration written before the N runs (LOW, closed, 2026-09-14 — Ark, chat 2026-09-13; filed by CC)

**Closed:** S2026-09-13.1 · 2026-09-15 · disproved · docs/experiments/001-run0-and-replicate.md §4: minimum checkpoint loss 1141.0463 at iteration 219,612; held-out loss rose +0.11% (1147.5358 -> 1148.8075) over the last 50,000 iterations; docs/preregistration-cheap-vs-expensive.md §7 "Plateau facts"; the redefine-expensive-via-the-plateau reading judged not viable by reviewers, 002 §5a item 12 (docs/experiments/002-night2-seeds-1-and-2.md); a plateau is an interpretation of the tail, not a datum · closed by CC

- **Observed 2026-09-14 (run 0).** Plateau reached: minimum held-out (checkpoint) loss
  1141.0463 at iteration 219,612; held-out loss rose by +0.11 % (1147.5358 → 1148.8075) over
  the last 50,000 iterations (checkpoint near 200,000 → checkpoint near 250,000); plateau:
  |change| < 0.2 %. Rung-vs-checkpoint jitter: the
  evaluation-hook rung at iteration 250,000 (1146.1958) and the checkpoint at iteration
  250,008 (1148.8075) differ by 2.61 over the 8 extra iterations. Full trajectory in
  `results/night1/night_report.md` and `results/night1/night_report_checkpoints.csv`.
- **Reported.** Ark: a free lever — run 0's plateau could redefine "expensive" together with
  the ladder.
- **Inferred.** The redefinition is a change to §3 after seeing run 0 — allowed for the
  population only if registered anew *before* the N runs, and not available at all once (b)
  has been seen.
- **First step.** After run 0, plot held-out loss against iteration from the rung and
  checkpoint metrics; if a plateau sits far before 250,000, propose a new pre-registration
  to Mike before any N run starts. Parent task
  [[PRE-REGISTER-THE-CHEAP-VERSUS-EXPENSIVE-TEST]], closed 2026-09-13.
- **axis:** knowledge

### RESEARCH-REPO-START-CHECKLIST-WRITTEN-ON-MIKES-WORD: fourteen rules distilled from this session's incidents, so a new research repository starts by reading them rather than re-deriving the principles (LOW, closed, 2026-09-15 — Mike 09:56 «пиши чек-лист»; drafted by Ark 08:50/09:39/09:51, written by CC)

**Closed:** S2026-09-13.1 · 2026-09-15 · fixed · `docs/CHECKLIST-research-repo.md` written (14
rules with incident addresses, header carrying Mike's word and the authorship line, closing
links to `docs/tool-hardening-package.md` and `docs/preregistration-cheap-vs-expensive.md` §7);
linked from `README.md`; verified on disk by CC · commit: not yet committed this session (Mike's
instruction: do not commit) · closed by CC

- **Observed.** Ark proposed the checklist three times (08:50, 09:39, 09:51) as the rules
  emerged from the 002 §5h code audit and the tool-hardening package; Mike's word (DPC Research
  chat, 2026-09-15 09:56 UTC): «пиши чек-лист». The file carries the same 14 items in the same
  order as the rules Ark and Zcode named through the day, plus R1–R4 from
  `docs/tool-hardening-package.md`.
- **First step.** None — closed on completion; a future incident that adds a rule appends a
  15th item rather than reopening this entry.
- **axis:** honesty, reach

### NIGHT-2-RUNS-SEEDS-1-AND-2-ON-MIKES-WORD: seeds 1 and 2 trained to 250,000, sequential, no replicate, are the first between-seed distances against the run 0 / run 0′ replicate offset (HIGH, closed, 2026-09-14 — CC, from the experiment record and next-session plan)

**Closed:** S2026-09-13.1 · 2026-09-15 · fixed · seed 1 (9991/001) EXIT rc=0, 250,008 iterations, 14,532.9 s; seed 2 killed at iteration 12,700 by the KB5129195 restart, partial dir renamed to flow/9991/002_killed_by_reboot, excluded under §7's resume rule; re-run as wave night2b (9991/002), started 2026-09-15T01:13:46Z, EXIT rc=0, 250,008 iterations, 14,296.6 s, done 05:12:18Z; Mike, chat 05:19Z: «прогон завершен»; record docs/experiments/002-night2-seeds-1-and-2.md and results/night2/ · commit: (this commit) · closed by CC

- **Observed.** Tooling ready: `tools/night/start_night.ps1` takes `-NoReplicate` (this
  commit), dry-run quoted (ids `9991/001`, `9991/002`; ensemble 9991 already holds `000` and
  `900` — the ids differ, no collision). Command in `docs/next-session-plan.md` §2.
- **Observed 2026-09-15 (CC).** Mike's word given (DPC Research chat, 2026-09-15 18:32 local:
  «вноси да и напиши мне команду…», then «запустил»); launched. Launcher log: `WAVE START
  tag=night2` 2026-09-14T19:12:31Z, launcher PID 32124, mode sequential, detached, determinism
  off, 2 jobs. First run id 9991/001, seed 1, PID 16460, `--n-iters 250000 --rungs
  1000,5000,25000,250000 --no-determinism`; progress log at iteration 700: 0.066 s/iter, VRAM
  1426 MiB, ETA first run ≈ 23:46Z. Second run 9991/002, seed 2, follows sequentially.
  `flow/9991` now holds 000, 001, 900. The b2 amendment (`9c395d5`) and the review edits plus
  `rho_ci.py` (`21fa5ab`) were committed before the launch.
- **Observed 2026-09-15, later (CC).** Seed 1 (9991/001) completed: `EXIT rc=0
  final_iteration=250008 wall=14548.9s` at 23:15:00Z. Seed 2 (9991/002) started 23:15:00Z; last
  progress line iteration 12,700/250,000 at 23:29:04Z; killed at 23:29:19Z by a Windows Update
  planned restart (KB5129195) — see
  [[WINDOWS-UPDATE-RESTARTS-INSIDE-THE-NIGHT-WINDOW-BECAUSE-ACTIVE-HOURS-END-AT-0600]]. Under the
  registered §7 resume rule (an interrupted run is a failed run, re-run from the same seed, no
  resume) seed 2 is re-run from scratch. Pending Mike's decision: remove or rename
  `results/flow/9991/002` (`run_individual.py:301-308` refuses to start if it exists, and a new
  tag such as `night2b` keeps the partial `night2_9991-002.*` / `wave_night2.*` records intact),
  then `-Tag night2b -Seeds 2 -NoReplicate`.
- **First step.** Mike's word (the standing rule,
  [[THE-NIGHT-RUN-STARTS-ONLY-ON-MIKES-EXPLICIT-WORD]], closed), then launch by Mike; morning
  comparison against the replicate offset (+12.64 mean / 1.11 % at 250,000,
  `docs/experiments/001-run0-and-replicate.md` §4) per the decision rule already registered
  in `docs/preregistration-cheap-vs-expensive.md` §7.
- **axis:** collective
- **taken:** CC · 2026-09-15

### A-TRAINED-SURROGATE-IS-NOT-A-PREFIX-OF-THE-SAME-PROCESS: AlphaGenome Atlas shows a cheap evaluation that works, but it is a trained surrogate validated at the top of its ranking, while this project's cheap evaluation is a prefix of the expensive process, the kind 2508.17464 found not to rank (MEDIUM, closed, 2026-09-13 — Ark, 17:51 UTC, on Mike's link of 17:50 UTC; source read by CC 2026-09-14)

**Closed:** S2026-09-13.1 · 2026-09-15 · fixed · Mike decided yes 2026-09-15 18:05 local, DPC Research chat: «ок давай впишем»; the form is written into docs/preregistration-cheap-vs-expensive.md as secondary hypothesis (b2) — §1 bullet, §4 statistic X = |Top-k(C3) ∩ Top-k(250,000)| with exact hypergeometric tails for N = 8/10/12/16/20 and k = 2/3 from docs/prereg-scripts/topk_tail.py (8!-permutation self-check passed, Python 3.12.10), §5 decision rule and timing rule, §7 measurability paragraph, §8 exclusions, §9 provenance; k = 2 fixed, marked (proposed — fix in review) until seeds 1 and 2 start · commit: (this commit) · closed by CC

- **Observed.** Source read at source 2026-09-14 (`literature.md` §H): the blog says
  *"testing each one in the lab is practically impossible"* and that collaborators
  *"experimentally verify key variants"*; the PDF says the DNM1 variant was *"the top ranked
  variant by AVI"* and a minigene assay across 5 cell lines confirmed it. What was validated is
  the top of a trained model's ranking against an external experiment, not agreement over a
  population.
- **Reported.** Ark, 17:51 UTC: two kinds of cheap evaluation — a trained surrogate
  (AlphaGenome's; works) versus a prefix of the same process (ours; what 2508.17464 measured
  and found not to rank). Three conditions they had and we lack: a surrogate trained on real
  measurements, a finite enumerable space, one fixed genome. Their success does not license
  our kind.
- **Inferred.** Hypothesis (b) as registered asks for rank agreement over the whole
  population; a weaker, untested-by-2508.17464 form is "does the cheap evaluation find the
  top-k of the expensive ranking?". Proposed, not registered.
- **First step.** Mike decides whether "finds the top-k" enters the pre-registration as a
  secondary hypothesis before the N runs; run 0 is unaffected. Parent task
  [[PRE-REGISTER-THE-CHEAP-VERSUS-EXPENSIVE-TEST]], closed 2026-09-13.
- **axis:** knowledge

## 2026-09-13 — closed by CC

### HOW-MANY-FULL-RUNS-THE-TEST-IS-ALLOWED: K runs to convergence is the whole cost of Phase 2, and it is not a hardware question (HIGH, closed, 2026-09-13 — asked by Ark, Johnny and Warren independently, 07:16–07:20 UTC)

**Closed:** S2026-09-11.1 · 2026-09-13 · fixed · K = 1 decided by Mike 2026-09-13 (run 0 only); N is no longer a number to name but a rule in docs/preregistration-cheap-vs-expensive.md §4, N = floor(m · H_avail / h_run) − 1 with m = 1 measured (e797f02) and h_run from run 0; the floor 8 vs 10 remains Mike's choice as [[N-EQUALS-EIGHT-IS-BELOW-THE-FILES-OWN-MINIMUM]] · commit: (this commit) · closed by CC

- **Observed.** The GPU is local and the money is zero; the cost is K × 250,000 iterations,
  overnight. K bounds the statistic in the pre-registration, so it is needed *before* the
  file is final, not after.
- **First step.** Mike names K. Parent task [[PRE-REGISTER-THE-CHEAP-VERSUS-EXPENSIVE-TEST]].
- **Decided 2026-09-13 (Mike): K = 1 to begin with.** Run 0 only; N for the test follows from
  its measured cost by the rule in ADR-002 Q1. Entry stays open until N is set.
- **axis:** honesty

### IDEA-MD-IS-VERBATIM-RUSSIAN-IN-A-REPOSITORY-THAT-OPENS-IN-ENGLISH: the idea is 62 % Cyrillic by character because it is the author's text as written, and the public version must be English without ceasing to be the record (LOW, closed, 2026-09-13 — Mike, 06:46 UTC: «там всё на английском должно быть»)

**Closed:** S2026-09-11.1 · 2026-09-13 · fixed · commit 30dc626: idea_en.md is in the repository as a marked English translation beside idea.md, and idea.md stays verbatim as the record · closed by CC

- **Observed.** Measured 2026-09-13: README 0.5 % Cyrillic, `literature.md` 1.0 %,
  `idea.md` 62.4 %, `chat/` 70–95 %, whole folder 50.5 %.
- **First step.** Publish `idea.md` as a marked translation with the Russian original kept
  beside it — a translation labelled as one is not a retelling passed off as the source.
  Child of [[ADR-001]].
- **axis:** reach

### ONE-GPU-ITERATION-BEFORE-ANY-OVERNIGHT-RUN: the price of the expensive evaluation on this card is an estimate until one training iteration has been timed here (HIGH, closed, 2026-09-13 — Mike, 07:20 UTC: «сначала весь флоу проверить, а долгие прогоны ночью»)

**Closed:** S2026-09-11.1 · 2026-09-13 · fixed · measured 2026-09-13 on the RTX PRO 4500 Blackwell, torch 2.9.1+cu128: 0.0619 s per training iteration (n=22, min 0.0589, max 0.0694), peak VRAM 1,402 MiB allocated / 4,568 MiB on the card, loss finite 24/24, so 250,000 iterations = 4.30 h and about 4.6 h all-in with checkpoints; two runs per ~10 h night sequential, concurrency not measured; source scratchpad/flyvis-probe/gpu_price_probe_instrumented.json · closed by CC

- **Observed.** The flow runs on this machine on CPU: `Network()` builds in 13.1 s; a
  full-node synthetic stimulus (5,768 photoreceptors, 20 frames) runs forward in 0.06 s and
  backward in 0.05 s with non-zero gradients. No GPU iteration has run. The card is occupied
  by production (28,395 of 32,623 MiB at last check), so this needs a maintenance window.
  Warren's 10–50 ms per GPU iteration is Inferred by its author and is not adopted here.
- **First step.** In a window with production down: one iteration of the stock training loop
  on the GPU, its wall-clock and VRAM recorded. Only then is K × 250,000 iterations turned into
  a night. Blocked by [[PRE-REGISTER-THE-CHEAP-VERSUS-EXPENSIVE-TEST]]; was blocked by
  [[SINTEL-IS-THE-ONE-UNVERIFIED-LINK-IN-THE-FLOW]], closed 2026-09-13.
- **2026-09-13:** dataset on disk and the flow task builds and yields samples on CPU (see the closed Sintel entry). This entry is now blocked only by the pre-registration review and the maintenance window.
- **axis:** honesty

### PRE-LAUNCH-EDITS-TO-THE-PRE-REGISTRATION-BEFORE-RUN-0: two reviews asked for fifteen text edits before run 0, and any of them applied after the run would be indistinguishable from an edit made after looking (HIGH, closed, 2026-09-13 — Ark 15:45 UTC and Zcode 16:24 UTC, chat; the K1 lesson)

**Closed:** S2026-09-11.1 · 2026-09-13 · fixed · 24 exact replacements applied to docs/preregistration-cheap-vs-expensive.md on Mike's word 17:06 UTC; floor 8/10 left as Mike's choice in §4 · commit: (this commit) · closed by CC

- **Observed.** The fifteen: the N-rule off-by-one and the "four nights" prose; the H_avail
  horizon; floor 8 vs 10 (Mike chooses); C3 as the primary rung with Holm for C1/C2; the
  inconclusive band by permutation CI; the negative branch narrowed and the positive one
  sharpened; a two-sided (a) criterion with the self-splice as instrument control; σ instead
  of range in §7; the determinism sentence, false since Mike's 16:20 UTC decision; a resume
  rule; one h_run definition; the 4.6 h arithmetic; exact rows N = 12/16/20 and the two
  tails; the "independent re-run" line; the status line. Commit e797f02 applied the measured
  facts and left every semantic edit for Mike's word. A scratchpad draft of the edits was
  named (`prereg-edits-draft.md`); draft written 23:29 local and applied (CC,
  2026-09-13).
- **Inferred.** "Decided in advance" stays distinguishable from "decided after looking" only
  if the edits land in a commit that precedes run 0's first checkpoint.
- **First step.** Mike says which edits go in; CC applies them by exact replacement and
  commits before the launch word. Parent task [[PRE-REGISTER-THE-CHEAP-VERSUS-EXPENSIVE-TEST]].
  Blocks [[THE-NIGHT-RUN-STARTS-ONLY-ON-MIKES-EXPLICIT-WORD]].
- **axis:** honesty

### PRE-REGISTER-THE-CHEAP-VERSUS-EXPENSIVE-TEST: the test has a verified flow and no written reading, so a run today would produce a number nobody could interpret (HIGH, closed, 2026-09-13 — Mike, 07:27 UTC: «всё ты делаешь, мы ревьювим»; the demand for numbers first is Johnny's, Ark's and Warren's, independently)

**Closed:** S2026-09-11.1 · 2026-09-13 · fixed · docs/preregistration-cheap-vs-expensive.md written 2026-09-13, reviewed by Ark (15:45 UTC) and Zcode (16:24 UTC), the fifteen edits applied on Mike's word in 5175239; the two decisions still open live in their own entries — the floor 8 vs 10 ([[N-EQUALS-EIGHT-IS-BELOW-THE-FILES-OWN-MINIMUM]]) and top-k as a secondary hypothesis ([[A-TRAINED-SURROGATE-IS-NOT-A-PREFIX-OF-THE-SAME-PROCESS]]); Johnny and Warren have not reviewed, noted and not waited on · commit: (this commit) · closed by CC

- **Observed.** Three reviewers converged on the same missing file: what *cheap* and
  *expensive* are in iterations, the number of individuals and seeds, the statistic and its
  threshold, the decision rule per outcome, and a named prediction for composition. None of
  the five exists in writing. The only number already fixed is flyvis's default for
  *expensive*: `n_iters: 250000`, batch 4, lr 5e-5 → 5e-6.
- **Inferred.** Hypotheses (a) "a spliced module behaves predictably" and (b) "cheap agrees
  with expensive" must be registered separately with separate rules, or a month from now it
  will not be possible to say which one fell. A splice of two identical copies is a control
  that can only pass — the same shape as a zero-initialised adapter — so the splice joins two
  *different* members or types, and the prediction is written before the run.
- **First step.** One file in this repository with the five items as numbers; two of the
  numbers are not the writer's — K (Mike) and what is spliced (Ark's proposal, in review).
  Child of [[ADR-002]]. Blocks [[ONE-GPU-ITERATION-BEFORE-ANY-OVERNIGHT-RUN]].
- **2026-09-13:** draft in the repository (`docs/preregistration-cheap-vs-expensive.md`), scripts beside it; seven marked proposals open for review (source of variation; splice pair and cell type — Ark; ladder and prefix definition; held-out split and metric; N = 10 minimum and the N rule; the 5 % tolerance for (a); the 1 % replicate tolerance). Entry stays open until reviewed.
- **axis:** honesty

### RESUME-OF-AN-INTERRUPTED-RUN-IS-UNVALIDATED: the night plan kills run 0′ at a checkpoint and resumes it the next night, and nobody has checked what a resumed replicate restores or what §7 counts it as (HIGH, closed, 2026-09-13 — Zcode review 3.4, 16:24 UTC; filed by CC)

**Closed:** S2026-09-11.1 · 2026-09-13 · fixed · 48-iteration interrupt-and-resume test 2026-09-13: flyvis recover() fails as installed (resolve_checkpoints TypeError, datamate FileExistsError); replica restores no RNG/data order, penalty optimizer not recovered, counter off by one (48 → 59); resumed − uninterrupted at rungs 24/36/48 = −0.096/−0.141/−0.187 vs replicate noise ≤ 1.1e-4; rule registered in §7: interrupted run = failed run, re-run from the same seed, resume never used · commit: (this commit) · closed by CC

- **Observed.** The night plan is run 0 then run 0′, 8.6–9.2 h together at the measured
  4.3–4.6 h per run, inside an 8–9 h window — so run 0′ is interrupted at a checkpoint and
  resumed the following night. `docs/preregistration-cheap-vs-expensive.md` §7 has no rule
  for what a resumed replicate is, and what flyvis `resume=true` restores — optimizer state,
  scheduler, RNG, data order — has not been checked.
- **Inferred.** Until both are settled, a resumed run 0′ is not the replicate §7 describes,
  and the 1 % replicate tolerance would be measured against the wrong object.
- **Reported.** Zcode 3.4 (chat, 16:24 UTC).
- **First step.** A 48-iteration interrupt-and-resume test against an uninterrupted control,
  both with determinism off; compare the hook trajectories at rungs 24/36/48 against the
  replicate noise. Running now (CC subagent). The resume rule itself is one of the fifteen
  edits in [[PRE-LAUNCH-EDITS-TO-THE-PRE-REGISTRATION-BEFORE-RUN-0]].
- **axis:** honesty

### SINTEL-IS-THE-ONE-UNVERIFIED-LINK-IN-THE-FLOW: everything up to the dataset runs on this machine, and the dataset is five gigabytes of a third party's data under its own terms (HIGH, closed, 2026-09-13 — CC, 07:26 UTC, asked before pulling it)

**Closed:** S2026-09-11.1 · 2026-09-13 · fixed · archive 5,627,783,629 B = server size, CRC clean over 8,753 members; 23/23 sequences in training/final and training/flow; MultiTaskSintel(tasks=[flow]) builds (69 items) and yields lum (9,1,721) / flow (9,2,721); no licence file in the tree, README carries copyright 2012 Butler et al. and a cite request only; commit: (this commit) · closed by CC

- **Observed.** flyvis's flow task reads `training/final` (images, 1.7 GB) and
  `training/flow` (ground truth, 3.1 GB) from MPI-Sintel and downloads them itself via
  `download_sintel()`; the depth split is only needed for a depth task. Disk free: 516 GB.
  The dataset's README carries its own terms; they were not read.
- **First step.** Mike's word; then one call, and the flow is verified end to end.
- **axis:** honesty

### THE-ATTRIBUTION-STRING-FOR-CC-BY-IS-NOT-WRITTEN: the licence is chosen and the LICENSE file cannot be written without saying who the author is (MEDIUM, closed, 2026-09-13 — Mike, 06:55 UTC: «ок CC BY 4.0»)

**Closed:** S2026-09-11.1 · 2026-09-13 · fixed · LICENSE at repo root with the string; README ## Licence; commit: (this commit) · closed by CC

- **Observed.** README names Mike and three agents by role. CC BY 4.0 requires an
  attribution; the string is a decision, not a default.
- **First step.** Mike names it; the LICENSE file follows in the same pass as the links.
  Child of [[ADR-001]].
- **axis:** reach

### THE-SECOND-VOICE-IN-THE-IDEA-TRANSCRIPT-IS-GROK-AND-UNNAMED: the review pasted inside the idea's transcript is a model's output that the public documents cite without a source (MEDIUM, closed, 2026-09-13 — Mike, 06:53 UTC, on who the second voice is)

**Closed:** S2026-09-11.1 · 2026-09-13 · fixed · commit: (this commit); git grep for 'second voice' in tracked files returns only the ADR-001 decided line · closed by CC

- **Observed.** All three entries in the transcript are attributed to `Mike Shevchenko`; Mike
  stated he showed the idea to Grok. The name «Безногим» does not occur anywhere in this
  repository. README and `idea.md` say "the second voice".
- **Inferred.** It is Mike's own conversation with a model and his to publish; the standard
  that a quote carries its source (Johnny) is what is unmet. CC's recommendation: drop it from
  the public version — each of its points is either superseded by the reviews or wrong.
- **First step.** Mike: name it as *Grok, 2026-09-12, shown the idea by Mike*, or drop it.
  Child of [[ADR-001]].
- **axis:** reach

## 2026-09-14 — closed by CC

### THE-NIGHT-RUN-STARTS-ONLY-ON-MIKES-EXPLICIT-WORD: the launcher is ready and dry-printed, and nothing starts until Mike says so (HIGH, closed, 2026-09-13 — Mike, 16:22 UTC: «полный ночной прогон не запускаем пока я явно это не скажу»)

**Closed:** S2026-09-13.1 · 2026-09-14 · fixed · launched by Mike 18:40 UTC (run 0), sequential replicate run 0′ followed automatically; both runs exit ok, 0 errors, 250,008 iterations each; WAVE DONE 2/2 ok at 2026-09-14T02:39:52Z; results recorded in `results/night1/` · commit: (this commit) · closed by CC

- **Observed.** Launcher `flyvis-probe/night/launch_wave.py` in the scratchpad (8,643 B,
  2026-09-13); command `launch_wave.py --tag night1 --ensemble 9991 --seeds 0 --replicate
  --sequential --detach --no-determinism`, dry-printed; ensemble 9991 unused; determinism
  off decided by Mike at 16:20 UTC.
- **Observed, 17:07 UTC.** Mike asks for console progress logging so he can launch from
  PowerShell himself and watch; being added to the launcher.
- **Observed, 2026-09-13 late.** Extent 5 measured and rejected — 1.46×, not the ≥ 3× that
  would have moved the night ([[EIGHT-PROCESSES-SHARE-THE-CARD-NO-FASTER-THAN-ONE]]); the
  night stays on extent 15. Tooling final: `night/run_individual.py` (rung hook, progress
  lines, `--override`), `night/launch_wave.py` (`--sequential --detach`, replicate right
  after seed 0), `night/start_night.ps1` (`-DryRun`, `-FollowOnly`, `-Extent`), all
  exercised on 24–48-iteration runs; launch instructions sent to Mike 17:55 UTC; the launch
  is Mike's own PowerShell command. Everything sits in the session scratchpad —
  [[THE-NIGHT-TOOLING-LIVES-IN-A-TEMPORARY-SCRATCHPAD]].
- **Observed, 2026-09-14.** Run 0 (`9991/000`) started 2026-09-13T18:40:31Z, finished
  2026-09-13T22:40:56Z, 250,008 iterations, exit ok, 0 errors. Run 0′ (`9991/900`, the §7
  replicate) started 2026-09-13T22:40:59Z, finished 2026-09-14T02:39:51Z, 250,008
  iterations, exit ok, 0 errors. `wave_night1.json`: `"finished_utc": "2026-09-14T02:39:52Z"`;
  progress log: `WAVE DONE 2/2 ok`. Results and the pre-registration §3/§6/§7 record in
  `docs/preregistration-cheap-vs-expensive.md` and `results/night1/`.
- **First step.** The word. Then launch, and the PID and the first rung (1,000) reported to
  the chat. Was blocked by [[PRE-LAUNCH-EDITS-TO-THE-PRE-REGISTRATION-BEFORE-RUN-0]] and by
  [[RESUME-OF-AN-INTERRUPTED-RUN-IS-UNVALIDATED]], both closed 2026-09-13. Done — see Closed
  line above.
- **axis:** collective
