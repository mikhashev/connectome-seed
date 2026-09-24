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



### SECOND-RULE-POST-RUN-ROOT-RESOLVES-TO-RESULTS-NOT-THE-REPOSITORY-ROOT: results/genome/c6/rules/second_rule/post_run.py sets ROOT = C6.parents[1], which is results/ and not the repository root (LOW, open, 2026-09-25 — listed in docs/briefs/2026-09-24-next-session-handover.md section 4)

- **Observed.** post_run.py:52-54: HERE = the second_rule directory, C6 = HERE.parents[1] = results/genome/c6, ROOT = C6.parents[1] = results/. Rule #2 never ran on C6, so it never mattered.
- **First step:** change to C6.parents[2] (or derive from the git root) before rule #2 is ever run on C6.
- **axis:** honesty
- **filed:** CC · 2026-09-25

### THE-EXTERNAL-REVIEW-PROMPT-NEEDS-THE-EDITS-AGREED-IN-THE-CHAT: the external-review prompt Ark drafted in the chat lacks the bank-origin note, cites an unverified NeurIPS 2025 reference and omits the bf1_p3.py quick check (LOW, open, 2026-09-25 — agreed in the DPC Research group chat; listed in docs/briefs/2026-09-24-next-session-handover.md section 4)

- **Observed.** Handover section 4: add the bank-origin note to the reading route, drop the unverified NeurIPS 2025 reference, add the bf1_p3.py quick check.
- **First step:** apply the three edits to Ark's draft before the prompt is sent to any outside reviewer.
- **axis:** reach, honesty
- **filed:** CC · 2026-09-25

### THE-BACKWARD-LADDER-TO-LARVA-AND-C-ELEGANS-GETS-ITS-OWN-ADR-ONLY-WHEN-A-NUMBER-DEMANDS-IT: the rungs below the adult fly are written down so they are not rediscovered, and stay closed until a forward number needs one (LOW, open, 2026-09-25 — Zcode, Johnny, Ark, DPC Research group, 2026-09-24 17:40-17:51 UTC; recorded in ADR-005 agreed point 7)

- **Observed.** Larva (Winding et al. 2023) after the column test; fly embryo not a step (no public full connectome found by Zcode's search, no vision); C. elegans (Cook 2019; Witvliet 2021, eight individuals L1 to adult, not averaged) needs a separate ADR. Johnny's view that other species are a new project is recorded.
- **First step:** deferred: none until a number demands the first rung; none of the three sources is read at source in literature.md yet.
- **2026-09-25, CC:** Correction (2026-09-25, Zcode's review): "no vision" above is ambiguous; the fly embryo is recorded as a vision, not a step, because no public full connectome was found (ADR-005 point 7).
- **axis:** knowledge
- **filed:** CC · 2026-09-25

### KNOCK-OUT-AND-REGROW-TESTS-WHETHER-THE-RULE-GENERATES-A-BLOCK-IT-WAS-NOT-SHOWN: removing a biologically chosen block of the flyvis-65 bank, training on the rest and scoring the regrowth against N1, shuffles and a permuted-block null tells generation from smoothing (HIGH, open, 2026-09-25 — Mike, DPC Research group, 2026-09-24 17:53 UTC: knock out and regrow as the next registration, YES; ADR-005)

- **Observed.** Proposed by CC, second null by Zcode (docs/decisions/005-backward-before-forward.md, agreed point 6). Standard: literature.md section 28, Lenski et al. 2003 knockout and reversal.
- **Inferred.** Known risk: indirect leakage through degrees; a rule that regrows a permuted block as well as the real one is smoothing, not generating.
- **First step:** draft the registration: name the block (for example a whole pathway) before any data is seen, give the biological reason, state everything removed with it, and say aloud that the generation-zero bank is a synthetic template of at least two flies.
- **axis:** knowledge, honesty
- **filed:** CC · 2026-09-25

### THE-COLUMN-TEST-MEASURES-HOW-MUCH-ORDER-AVERAGING-REMOVES-AND-THE-SEPARATE-VOLUMES-READING-MEASURES-THE-MERGE: per-column type-pair tables within one FlyWire fly, read beside whether flyvis exposes the FIB-25 and FIB-19 estimates before its max merge, split agreement made by biology from agreement made by averaging (HIGH, open, 2026-09-25 — Mike, DPC Research group, 2026-09-24 17:53 UTC: column test plus the separate-volumes reading, YES; ADR-005)

- **Observed.** The generation-zero bank is flyvis's column-averaged template of at least two flies, fused by taking the larger of the FIB-25 and FIB-19 estimates (docs/notes/2026-09-23-where-our-bank-comes-from.md sections 1-2, Lappalainen Supplementary Note 1 equation 7).
- **Inferred.** The column test measures one component, the order averaging removes; it is not a proxy for between-bank overlap (Johnny's objection, Zcode's reconciliation). The separate-volumes reading, if the estimates exist, measures the merge's contribution directly as overlap(one volume vs FlyWire) against overlap(merged vs FlyWire) (Zcode).
- **First step:** read flyvis 1.2.0 for per-volume estimates (files or code) and record the answer with its location; then register the column test before any value is computed.
- **2026-09-25, CC:** Correction (2026-09-25, reviews by Ark, Johnny and Zcode in the DPC Research chat): the column test is Ark's proposal; Johnny objected; Zcode reconciled. The test gives a lower bound on the order our processing produces, since column averaging is one of four steps (Zcode). ADR-005 point 4 carries the same wording.
- **axis:** honesty, knowledge
- **filed:** CC · 2026-09-25

### QUESTION-II-TRANSFER-IS-PAUSED-UNTIL-THE-COLUMN-TEST-MEASURES-WHAT-AVERAGING-CONTRIBUTES: question (ii), whether the structure found in one brain is the same structure in the other, is paused because agreement between two averaged banks cannot yet be told apart from agreement made by the averaging (MEDIUM, open, 2026-09-25 — Mike, DPC Research group, 2026-09-24 17:53 UTC: question (ii) PAUSED, YES; ADR-005)

- **Observed.** docs/briefs/2026-09-24-next-session-handover.md section 2 named question (ii) as the next task. Mike paused it on 2026-09-24 17:53 UTC pending the column test (docs/decisions/005-backward-before-forward.md, decision 2).
- **Inferred.** 159 of 165 FlyWire-30 pairs lie inside flyvis-30 (Ark), but both are averages, so a positive transfer could be arithmetic rather than biology.
- **First step:** none until the column test returns; when (ii) is registered it carries every item of ADR-005 agreed point 5 (two arms, cell-stratified scoring, null 2c, headline r = 2 with Ark's falsifier, lambda by the source's own CV, existence-only scope, the FlyWire typing caveat).
- **axis:** knowledge, honesty
- **filed:** CC · 2026-09-25

### PROFILES-READING-SECTION-0-HASH-DOES-NOT-REPRODUCE-FROM-ANY-COMMITTED-REVISION: the sha256 sealed in section 0 of PROFILES-READING.md as taken before the profiles were opened cannot be recomputed from any revision of the file in this repository's history (MEDIUM, open, 2026-09-23 — recorded in the file's own dated note; filed by CC)

- **Observed.** results/night5/diagnostics/rowB/PROFILES-READING.md section 0z (and docs/notes/2026-09-23-translated-pinned-files.md:46,76) records that the digest a4d10e67f6eafa922f555625569ac5ca11db2de8bb27a01e597acbc0a945583d, declared taken at 2026-09-20T09:31:44Z over the file as saved at 09:30:25Z, does not reproduce from any committed revision, in either line ending; the two hashes that do reproduce from commit 2488ecb are a different pair (d5a75ac9... / b2ca1f0e...).\n- **Observed.** PROFILES-READING.md's own pre-reading declaration states plainly that 'the bytes that were hashed were never committed, so the claim that the rule preceded the values cannot be checked from this repository'
- **Inferred.** the dated note already carries the honest statement of the defect in the file itself and in docs/notes/2026-09-23-translated-pinned-files.md; what is missing is a backlog entry so the open question is visible on the board rather than only inside the file it concerns
- **First step:** no further action is owed by this entry alone -- the file already states the non-reproduction, and the record it would need (the actual saved bytes at 09:30:25Z, if they still exist anywhere off-repository) is Mike's or Ark's to locate, not something a note can manufacture
- **axis:** honesty
- **filed:** CC · 2026-09-23

### FOUR-CITATIONS-OF-ARKS-2026-09-20-21-43-RULE-WRITE-BARE-LOCAL-TIMESTAMPS-NOT-RECONCILED-AGAINST-THE-SAME-FILES-OWN-UTC-STAMPS: results/night5/diagnostics/rowB/README.md (lines 9, 375, 376, 417) and PENALISED-QUANTITY-READING.md:75 all cite Ark's DRIFT/SMOOTH/AMBIGUOUS rule by a bare local clock, unreconciled against the same files' own UTC stamps (MEDIUM, open, 2026-09-23 — found while checking the C6/genome commits for date/time handling; filed by CC)

- **Observed.** README.md:9 -- 'Ark, DPC Research group chat 2026-09-20 19:13 local'; :375 -- 'written down by Ark on 2026-09-20 21:43 local, AFTER the reading'; :376 -- 'message on the field list, 19:13 local'; :417 -- 'wording Ark's, group chat 21:43 local'. PENALISED-QUANTITY-READING.md:75 -- 'Ark wrote it down on 2026-09-20 21:43 local -- after this reading'. None of the five states whose local clock it is, and README.md:415 reads 'AUTHORISED by Mike 2026-09-20 09:27 UTC' three lines below one of the local citations with no stated offset.\n- **Observed.** This is the same class of defect commit 2c095558 corrected in PROFILES-READING.md section 0 ('a quoted time that joined a local date to a UTC time is corrected, with the original wording kept in brackets') -- that fix was not carried to these five citations of the same 21:43 event elsewhere in the repository
- **Inferred.** not yet shown to be a wrong reading -- Bangkok local (UTC+7) is consistent with the UTC stamps at every point checked (19:13 local roughly 12:13 UTC, after Mike's 09:27 UTC authorisation; 21:43 local roughly 14:43 UTC, later the same day) -- so this is an unreconciled-notation defect, not a demonstrated ordering error, until someone states the offset and checks all five against every UTC stamp in both files
- **First step:** CC adds one line at each of the five citations naming the timezone or the UTC equivalent in brackets, as PROFILES-READING.md section 0 already does, and confirms no two citations of the same 21:43 event disagree once converted
- **axis:** honesty
- **filed:** CC · 2026-09-23

### THE-S2-DESIGN-NAMES-THE-SHUVAEV-DECODER-AS-A-FIXED-PROJECTION-WHEN-THE-SOURCE-PAPER-TRAINS-IT: docs/plans/2026-09-20-genome-design-around-s2.md describes the genomic-bottleneck decoder as a fixed random projection, but the paper it cites trains it (MEDIUM, open, 2026-09-23 — recorded while reading the section I.1 sources at source for the first rule proposal; filed by CC)

- **Observed.** docs/plans/2026-09-23-first-rule-proposal.md (commit 5a46886) states, after reading the section I.1 sources at source: 'the S2 design describes the genomic-bottleneck decoder as a fixed random projection, while that paper's Methods describe a trained network over fixed labels.'\n- **Observed.** results/genome/c6/decoders/bf_decode.py and the C6 harness's BF_r opponent are a trained bilinear factorisation, not a fixed projection, so the C6 exam itself does not inherit this error -- but the design document that named the genome track's decoder framing still does
- **Inferred.** if the S2 design's decoder framing is carried into the extraction or into a rule's decode step uncorrected, a rule that should be compared against a trained g-network gets compared against a fixed one instead, which is an easier bar
- **First step:** Ark, who owns docs/plans/2026-09-20-genome-design-around-s2.md, corrects the decoder description against the genomic-bottleneck paper's own Methods section, with a dated amendment note (repository is read-only to him; not CC's edit)
- **axis:** knowledge
- **filed:** CC · 2026-09-23

### A-BAND-TAKEN-FROM-EIGHT-RUNS-WAS-WRITTEN-DOWN-SO-THAT-TWO-OF-THE-EIGHT-FALL-OUTSIDE-IT: the migration acceptance band and gate 4's three sub-gates are both defective in the same way, and the defect only shows when a new run lands at an edge (MEDIUM, open, 2026-09-19 — CC, on trying to close the migration entry against its own acceptance condition)

- **Observed — the migration band does not contain its own sample.** The condition was "a full run's `iter_wall_median_all_s` inside **[0.0598, 0.0622]** — the band of all eight runs on record". Measured over those eight: `9991/001` = **0.062248** and `9991/004` = **0.059796**, i.e. **two of the eight sit outside**. The true range is [0.059796, 0.062248] and the quoted band was rounded to four decimals **inward**, excluding both of its own endpoints. Night 5: `0"` = 0.062199 (inside), `3'''` = **0.059288** (below the range of all eight, genuinely faster).
- **Observed — gate 4's three sub-gates are not independent.** Plateau and late bands alone permit ratios from **1.263 to 1.506**, while the ratio band is [1.30, 1.45]. So a run can pass both level bands and fail the ratio, which is what `0"` did (1.461). All three were taken from the same eight runs and then applied as if independent.
- **Observed — and the mechanism is that the phases move separately.** Both night-5 runs are faster than all eight in the late phase (0.0447, 0.0448 against a previous minimum of 0.0457) while their plateaus go in **opposite** directions (`3'''` below all eight, `0"` above all eight). The ratio is their quotient and so has a wider spread than either component band.
- **Inferred.** A band set from n = 8 describes a sample, not a property, and writing it to four decimals can make it exclude the very runs it was drawn from. This is the same error as an SD over three seeds presented as the population's, one level down, on the instrument rather than on the science.
- **First step.** Two candidates, and the choice is a decision rather than a preference: state bands as the observed min/max with the direction of rounding named (outward), or state them as a tolerance around a central value with the tolerance derived (a multiple of the checkpoint step). Either way a derived quantity such as a ratio does not get its own band on top of its components' — it gets one or the other. Not blocking any run; blocking a clean disposition of night 5's gate 4.
- **2026-09-23, CC:** paused by Mike's word of 2026-09-20 10:15 UTC (ADR-004 amendment); stays open.
- **axis:** collective

### THE-CORRESPONDENCE-BETWEEN-A-RUN-AND-ITS-COLUMN-KEEPS-BEING-INFERRED-FROM-A-NAME-INSTEAD-OF-RECORDED: three times now the link has been left derivable, and twice it was wrong (MEDIUM, open, 2026-09-19 — Ark found the third instance in CC's night-5 table; CC recorded it)

- **Observed — instance 1, night 1.** Its checkpoint table names its columns `val_loss_A` / `val_loss_B` with **no legend anywhere in the repository**. Which run is which cannot be recovered from the file, and could not be recovered by byte comparison either, because night 4 prints full floats where the older reports print four decimals.
- **Observed — instance 2, the v1 resolver.** It derived run→column from wave-json bindings plus column names across nights and **could not map two of the eight runs**, refusing with exit 2. Removed in v7 in favour of the registered file's pinned header.
- **Observed — instance 3, the night-5 table.** Its first version declared a rule about itself: "`val_loss_seed<N>` followed by k `prime` tokens is the (k+1)-th run of seed N". True of `val_loss_seed0primeprime`; **false** of `val_loss_seed3primeprimeprime`, which carries three prime marks and is also a third run. Our own notation counts marks (`0"` two, `3'''` three) while the rule counts order, and they coincided for the first case only. Fixed the same day: `results/night5/run_columns.csv` carries the explicit mapping with `run_index_for_seed`, and the grammar is demoted to a comment explaining why it cannot be trusted.
- **Inferred.** The pattern is not three accidents; it is a standing preference for a correspondence that looks derivable over one that is written down. Each time the first case validated the rule and a later case broke it.
- **First step.** A checklist rule in `docs/CHECKLIST-research-repo.md`: a run→column, run→file or run→session correspondence is **recorded as a table beside the artefact**, never encoded in a name and never re-derived by a consumer; a naming convention may accompany it as a comment and may not be the source of truth.
- **2026-09-23, CC:** paused by Mike's word of 2026-09-20 10:15 UTC (ADR-004 amendment); stays open.
- **axis:** collective

### THE-CHEAP-AND-THE-DEAR-ESTIMATE-ARE-TAKEN-UNDER-DIFFERENT-REGULARISATION-SO-TEST-B-HAS-TWO-CLASS-QUESTIONS: the C3 hook at 25,000 lies inside the activity-penalty regime and the top rung at 250,000 lies outside it, so "does the cheap estimate agree with the dear one" was measured as "does it agree with the dear one in another regime" (HIGH, open, 2026-09-18 — Ark, on reviewing CC's night summary: "if C3 and the hook live in different regimes, then (b) has **two** class questions, not one" — translated from Russian; measurement by CC)

- **Observed.** `activity_penalty.stop_iter = 150000` in the resolved config of all eight runs, against `n_iters = 250000`: the penalty is applied for the first 150,000 iterations and then never again (`Penalty.__call__`, `solver.py:812-818` — past `stop_iter` it sets `self.activity_optim = None`). The C3 hook sits at 25,000, **inside** the penalised regime; the top rung sits at 250,008, **outside** it.
- **Observed.** The penalty acts on `nodes_bias` and on nothing else, and that is now a read rather than an inference (2026-09-18, CC, in the installed flyvis 1.2.0): `penalize` appears in exactly three network configs — `node_config/bias/bias.yaml:11` with `activity: true`, and `edge_config/syn_strength/syn_strength.yaml` and `edge_config/syn_count/syn_count.yaml` with `function: weight_decay, kwargs: {lambda: 0}`. `Penalty.init_optim` adds a parameter to the activity list only when `getattr(config, "activity", False)` holds, and to the function list only when `"function" in config and any(config.kwargs.values())` — which `lambda: 0` fails, so the weight-decay optimiser is never even constructed. The activity optimiser is built over `getattr(self.network, "nodes_bias")` alone.
- **Observed.** The two weights in the penalizer config are **one penalty with two branches**, not two families of term: `asymmetric_weighting(tensor, gamma, delta) = gamma·relu(tensor) − delta·relu(−tensor)` (`utils/tensor_utils.py:443-461`), applied to `activity_baseline − activity_mean` and then squared, so below-baseline deviations are weighted 1.0 and above-baseline 0.1. Ark's reading that the pair implies node and edge terms does not hold.
- **Observed.** `nodes_bias` carries one value per cell type — `bias.yaml` has `groupby: [type]`, and the connectome definition `flyvis/connectome/fib25-fib19_v2.2.json` lists **65** nodes, each with its own `bias` field (605 edge groups, for scale). Of the three penalisable families only the bias is *sampled*: `initial_dist: Normal, mode: sample, seed: 0`, against `syn_count`'s `mode: mean` and `syn_strength`'s `initial_dist: Value`, both deterministic. So `network.node_config.bias.seed` — the one parameter that differs between our individuals — can move only those 65 numbers, and they are exactly the ones the penalty pulls toward a common level for 60 % of training.
- **Inferred, and this is the entry's point.** Test (b) asks whether a cheap early estimate ranks individuals the way an expensive late one does. If the two are taken under different regularisation, "the cheap estimate is uninformative" and "the cheap estimate is informative about a differently-regularised system" are **two different failures with the same symptom**, and the design cannot tell them apart as it stands. What must be decided before the reading is which of the two (b) registers, because the answer changes what a null result licenses. Not a verdict on (b) — a statement that the question was underspecified.
- **Inferred.** One consequence favours the reachability endpoint: the checkpoint curves pass through **both** regimes within a single run, and the straddle is already printed, so the free test is the only instrument available that can see the regime break without leaving one curve (Ark).
- **First step.** Before the (c)4 reading, state in `docs/plans/2026-09-17-endpoint-before-n.md` which (b) is registered, and whether a rung inside the unpenalised regime — any checkpoint past 150,000 — is the honest cheap anchor instead of C3. No new run is needed to decide it: the eight curves on disk already span both regimes.
- **2026-09-20, CC.** (a) The First step above ("before the (c)4 reading, state ... which (b) is registered") was **not** done before the reading. `git log`: commit `031c9e2` ("The question was underspecified, and the file that says so had to be written by someone") is dated `2026-09-18T14:44:41+07:00`; commit `23547f7` ("The reading happened: TEST UNREADABLE, 16 of 23 levels left the test, and every one of them on the twin side") is dated `2026-09-18T16:33:21+07:00` — the reading followed the registration card by about 1h49m the same day, both authored by CC. It cannot be done retroactively; CC's position, recorded here, is to register (b) inside the blind v2 session. (b) `PENALISED-QUANTITY-READING.md` (read 2026-09-20 on Mike's word): the penalised quantity is SMOOTH through the 150,000 boundary in 10 of 10 runs at 3,600-iteration resolution (no run's boundary jump exceeds ~1.8× its own local step, and the one that does, seed 3′, moves toward baseline, not away); one run (seed 3‴, `9992/003`) rises ~15,600 iterations after the boundary — not classified by the SMOOTH/DRIFT rule as written; three runs (seed 0′, seed 2, seed 5) drift toward baseline after the boundary, a direction the rule does not describe either. (c) Recomputed from `results/night5/night_report_checkpoints.csv` myself (not from the prior report): median |Δ| across the ten runs between checkpoints 147,612 and 151,212 (flanking 150,000) is **2.2332** (sorted diffs 0.5868, 1.2760, 1.4809, 1.5864, 2.0577, 2.4087, 3.8470, 4.1292, 6.7006, 7.4939). Comparing the same computation at the other eight 25,000-multiple boundaries in the file: 25,000 → 8.4490; 50,000 → 3.9945; 75,000 → 6.7998; 100,000 → 5.2875; 125,000 → 5.6189; 175,000 → 6.0928; 200,000 → 6.1443; 225,000 → 3.1230. **Correction to what I was told:** the 150,000 median (2.2332) is not merely "of the same size" as the others — it is the **smallest of the nine** boundary medians, below the full [3.12, 8.45] range of the other eight, which is a stronger form of "no step at 150,000" than "same size," not a weaker one. (d) Correction of the group-chat statement (Ark, 2026-09-20): the step at iteration 150,100 "from 0.0625–0.0670 to 0.0445–0.0495" is seconds per iteration, not loss. `docs/briefs/2026-09-17-night5.md` §4.4: "(4a) plateau level, median of `s/iter`... → band **[0.0625, 0.0670]**" and "(4b) late level, median over iterations 150,100–250,008... → band **[0.0445, 0.0495]**" — both explicitly `s/iter` sub-gates on wall-clock timing, replacing a single median because the penalty optimiser being dropped at `stop_iter` changes the per-iteration cost, not the network. **Inferred.** The "two regimes" reading weakens at the 150,000 boundary (per (b)/(c)) but the card does not close: at 25,000, where the cheap probe (C3) sits, the penalised quantity is markedly higher and more variable in most runs (pre-150k maxima 21.9–129.8 vs post-150k maxima 16.3–60.6, `PENALISED-QUANTITY-READING.md` §5), so "the cheap probe sits in an unsettled phase" remains open as its own question. Recommendation recorded, not decided here: leave `stop_iter` untouched; Mike's decision. <!-- no-refs -->
- **2026-09-20, CC — decided, and the observation renamed.** **Mike, owner, 2026-09-20: `activity_penalty.stop_iter` is left untouched.** The card does not close; it changes name. What weakens is the *boundary* half of it — the penalised quantity is smooth through 150,000 in all ten runs and held-out loss carries no step there either (`results/night5/diagnostics/rowB/PENALISED-QUANTITY-READING.md`), so by the time the penalty is dropped it was no longer holding the network. What stands, and is now the entry's live claim under its own name, is the *phase* half: at 25,000, where the C3 probe sits, the penalised quantity is markedly higher and more variable in most runs — **the cheap probe is taken while the system is unsettled**, which is a statement about the probe's placement rather than about two regularisation regimes. The distinction matters for what a null on (b) would license, which is what this entry was opened to protect. No registered rule changes; no run is needed to decide it further. Restated in `ROADMAP.md` Phase 2 item 3(vi) and in `VISION.md` § "And what it looks like one day later (2026-09-20)". <!-- no-refs -->
- **First step, replacing the one above (which was not done before the (c)4 reading and cannot be done retroactively).** Register which (b) is meant — the probe-placement question or the regularisation question — inside the blind v2 session, and state whether a rung past 150,000 is the honest cheap anchor instead of C3. The curves that decide it are already on disk.
- **2026-09-23, CC:** paused by Mike's word of 2026-09-20 10:15 UTC (ADR-004 amendment); stays open.
- **axis:** collective

### THE-INSTRUMENTS-WERE-AUDITED-THE-DAY-THEY-WERE-BUILT-AND-NINETEEN-FIXES-WAIT-ON-MIKES-WORD: the code audit of the diagnostics found witnesses that cannot veto, constants never checked against the pre-registration and an undocumented null-draw rule, and nineteen fixes with falsifiers wait on Mike's word to fix the tools (HIGH, open, 2026-09-15 — Ark 08:42/08:45/09:39/09:51, Zcode 09:04, CC; consolidated `docs/tool-hardening-package.md`; Mike's word "fix the instruments", translated from Russian)

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
- **First step.** Mike's word "fix the instruments" (translated from Russian), then tier A (items 1 and 15 are tested
  together by one test; item 16 needs a purpose-built fixture); items 5 and 13 are
  design-first, not one-line changes. See
  [[THE-COMPOSITION-MARGIN-OVER-ITS-FLOOR-IS-SMALLER-THAN-A-NULL-SHIFTS-MEDIAN-DELTA]] (the (a)
  reading items 5/11 answer) and
  [[WINDOWS-UPDATE-RESTARTS-INSIDE-THE-NIGHT-WINDOW-BECAUSE-ACTIVE-HOURS-END-AT-0600]] (item
  17).
- **2026-09-23, CC:** paused by Mike's word of 2026-09-20 10:15 UTC (ADR-004 amendment); stays open.
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

### THIRTEEN-LINKS-POINT-INTO-A-DIRECTORY-THAT-WILL-NOT-BE-PUSHED: README, literature and idea link into chat/, which is ignored from history, so every one of them resolves to nothing on GitHub (MEDIUM, open, 2026-09-13 — consequence of Mike's "chat/ goes in gitignore", translated from Russian, 06:50 UTC)

- **Observed.** Counted before the first commit: README 8 distinct links, `literature.md` 4,
  `idea.md` 1. All of the form `chat/NN-name-hhmmss.md`. `chat/` is excluded by `.gitignore`
  from `8695d26`.
- **First step.** Replace each with a plain attribution — name, role, date, UTC — which is what
  the README already carries in prose; the information survives, the link does not. Mechanical;
  done in the same pass as the LICENSE and the translation. Child of [[ADR-001]].
- **2026-09-25, CC:** Ark's recount, recorded in docs/briefs/2026-09-24-next-session-handover.md section 4: twenty tracked lines mention chat/ by name and none is a link. What remains is the mentions, not links.
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
  "fix the instruments" (translated from Russian) —
  [[THE-INSTRUMENTS-WERE-AUDITED-THE-DAY-THEY-WERE-BUILT-AND-NINETEEN-FIXES-WAIT-ON-MIKES-WORD]].
- **2026-09-23, CC:** paused by Mike's word of 2026-09-20 10:15 UTC (ADR-004 amendment); stays open.
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
- **2026-09-23, CC:** paused by Mike's word of 2026-09-20 10:15 UTC (ADR-004 amendment); stays open.
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
- **2026-09-23, CC:** two entries this design fed close today: birth ids are now content-derived (extract_bank.py, commit 9ed0dae, see backlog_closed.md), and the type-pair table's own regularity is now measured (results/genome/bank/REGULARITY-READING.md, commits 9116ff9/9ed0dae, see backlog_closed.md). Neither closure reaches this entry's own claim about label provenance in docs/plans/2026-09-20-genome-design-around-s2.md, and a fresh mismatch was found in that same document today between its decoder description and the source paper it cites -- see THE-S2-DESIGN-NAMES-THE-SHUVAEV-DECODER-AS-A-FIXED-PROJECTION-WHEN-THE-SOURCE-PAPER-TRAINS-IT. This entry stays open on its own terms.
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
- **2026-09-23, CC:** paused by Mike's word of 2026-09-20 10:15 UTC (ADR-004 amendment); stays open.
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
- **2026-09-23, CC:** paused by Mike's word of 2026-09-20 10:15 UTC (ADR-004 amendment); stays open.
- **axis:** honesty

### THE-GENOME-TRACK-HANDOVER-OVERSTATES-WHAT-A-SEED-MOVES: `docs/briefs/2026-09-19-genome-track-handover.md` §3 calls the 65 biases "the whole of individuality" when the same seed also spends itself on the decoder and the data order (MEDIUM, open, 2026-09-20 — CC)

- **Observed.** `docs/briefs/2026-09-19-genome-track-handover.md:42`: "The 65 biases are the whole of individuality". `tools/night/run_individual.py:356` spends `--seed` on `network.node_config.bias.seed` alone, but `:282-284` and `:703-705` spend the *same* seed on the global `random`/`numpy`/`torch` RNGs, set before the solver is built and again before training ("data order / augmentation stream"). Two individuals therefore also differ in the decoder's 7,427 initial weights and in data order / augmentation. `VISION.md` and `ROADMAP.md` do not carry the sentence (checked this session, no match).
- **Inferred.** The claim holds for network parameters only, not for the individual as a whole. The confound was already on record in `docs/next-session-plan.md` (the bias-only / order-only 2×2, Ark and Zcode, 2026-09-15) and is now restated in `docs/notes/2026-09-20-what-is-the-genome-here.md` §3.
- **First step.** Correct the handover sentence — the correction must carry no result value, since the doc is required reading for the blind v2 author. `VISION.md` / `ROADMAP.md` need no matching edit; they do not carry the sentence.
- **2026-09-20, CC — checked at the session close, and NOT done.** `docs/briefs/2026-09-19-genome-track-handover.md` §3 still opens with "The 65 biases are the whole of individuality, and this is a read rather than an inference." The entry stays open. The correction is now stated in three places that are not that sentence — `docs/notes/2026-09-20-what-is-the-genome-here.md` §3 (read from source), this entry, and `docs/briefs/2026-09-20-next-session-handover.md` §5 item 6, which tells the next reader of the 2026-09-19 handover that the sentence is known to be wrong and unedited. That is a signpost, not the repair: the handover is required reading for the blind author and a reader who opens only it still reads the overstatement.
- **axis:** knowledge


### SIXTEEN-MEGABYTES-OF-UNARCHIVED-SCRATCHPAD-MATERIAL-SITS-BESIDE-FLYVIS-PROBE: preregistration drafts, chat dumps, a PDF and a lora-work directory remain unarchived in the ended session's scratchpad, and Mike must decide their fate by hand (LOW, open, 2026-09-20 — CC)

- **Observed.** `C:\Users\mikha\AppData\Local\Temp\claude\c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx\63f3961a-96ce-4048-8338-72c162ea66f8\scratchpad\` holds ≈16 MB: preregistration drafts, chat dumps (`chatall.txt` etc.), `alphagenome-atlas.pdf`, `lora-work/`.
- **Observed, 2026-09-20 (this session).** `flyvis-probe` no longer exists at that path (`Test-Path` → `False`, checked 2026-09-20). It was archived and hash-verified earlier the same day per the prior record, and Mike had said to delete it; an automated deletion was blocked by a Claude Code safety guard, so the deletion (now apparently done) was Mike's by hand.
- **First step.** Mike decides whether the remaining files are archived to `connectome-seed-archive/` or discarded.
- **axis:** collective




### NON-DETERMINISM-IN-TRAINING-MAY-BE-THE-SOURCE-OF-THE-REPLICATE-GAP: the same GPU-operation-order mechanism that makes evaluation non-repeatable ran uncontrolled for 250,000 training iterations, and is a candidate explanation for why replicates of one seed diverge (MEDIUM, open, 2026-09-20 — raised by Ark in the group chat after the row-B deterministic-mode result)

- **Observed.** All nights ran with `--no-determinism` (`tools/night/start_night.ps1:68`). [[A-TRAINED-CHECKPOINTS-EVALUATION-IS-NOT-BITWISE-REPEATABLE-BETWEEN-TWO-CALLS-IN-ONE-PROCESS]] shows that turning determinism on at evaluation drives the hook-vs-no-hook and no-hook-vs-no-hook differences to exactly zero, 30/30 pairs and 3/3 fresh processes (`rowB_controls_det.json`, `rowB_controls_floor_proc{1,2,3}_det.json`) — the whole non-repeatability there was GPU operation order.
- **Inferred (Ark).** The same order-of-operations mechanism, compounded over 250,000 training iterations rather than one evaluation call, is the first candidate explanation for why replicates of one seed (e.g. run 0 vs run 0′, |Δ| 12.7279 at the top rung, [[THE-REPLICATE-DIFFERS-BY-ONE-POINT-ONE-PERCENT-AT-THE-TOP-RUNG]]) diverge. If so, σ_rep is an artefact of our own training configuration rather than a property of the individuals.
- **Trap named by Ark.** Switching determinism on in training would drive σ_rep toward zero and make the ADR-002 ratio pass — a right-looking answer built from two wrong numbers (a training run that no longer resembles the nights on record, compared against a spread measured under the old setting). Such a result would ratify the method, not test it.
- **Also recorded (CC).** One `--seed` also seeds decoder init and data order, not only the 65 biases (`docs/notes/2026-09-20-what-is-the-genome-here.md` §3; see [[THE-GENOME-TRACK-HANDOVER-OVERSTATES-WHAT-A-SEED-MOVES]]). Replicates of one seed share all of these — decoder init, data order, and the bias draw — so the replicate gap cannot be explained by a difference in any of them; it has to come from something that varies *within* one fixed seed, which non-deterministic operation order is a candidate for and a differing seed value is not.
- **2026-09-20, CC — the source is established, and the entry's question splits in two (Ark's restatement, adopted).** The candidate above is no longer a candidate for the *source*. Replicates of one seed are copies of one config to the last field: identical at iteration 0, apart by under one float32 step at iteration 12, apart by the whole replicate gap at the end (Ark read the configs; CC's control measured it). Since replicates share the bias draw, the decoder initialisation and the data order, the gap has to come from something that varies *within* one fixed seed, and GPU operation order in training is that thing. So the entry now carries two separate questions where it carried one:
  - **(1) The control on the training path — DONE, at a short horizon.** Deterministic training was measured for the first time: about 3.33× the nights' mode, no operator refusing, and the same seed twice **bitwise identical over 2,000 iterations** (`docs/briefs/2026-09-20-night6-deterministic-pairs.md` §5, `results/night6/`). That is exactly the "two short runs of one seed, determinism on vs off" the First step asked for, and its prediction held. Gate 7 turned out blind to the determinism flag; **gate 7b is registered** as the repair.
  - **(2) "Does an individual exist" — OPEN, and it is not answered by more of (1).** Under determinism the replicate spread is not zero, it is **undefined**: there are no replicates, because the same seed gives the same run. So there is nothing for a between-seed spread to be compared *with*, and the authorised night's shape — two deterministic pairs — is vacuous by construction. CC and Ark reached this separately before launch. The question that remains is not "how big is σ_rep under determinism" but "how far can an individual be perturbed and still be itself", which is the perturbation ladder, opened as [[THE-PERTURBATION-LADDER-MEASURES-HOW-FAST-AN-INDIVIDUAL-FORGETS-ITS-INITIAL-CONDITION]].
- **Mike's word, 2026-09-20 10:02 UTC.** He does not want to spend the night; one full deterministic run is about 13.4 h and the resources can go elsewhere. Night 6 is prepared and **not launched**. Ark's trap above is unchanged by any of this and is the reason nothing follows automatically: switching determinism on in training would drive the replicate spread toward zero and ratify the method rather than test it.
- **First step.** Nothing on this entry until Mike answers the ladder. When he does, (2) moves there and this entry closes as superseded; if he declines it, this entry is the record that the source is known and the individuality question is not answered.
- **2026-09-23, CC:** paused by Mike's word of 2026-09-20 10:15 UTC (ADR-004 amendment); stays open.
- **axis:** honesty



### THE-S2-DESIGN-CARRIES-A-CHECK-ITS-OWN-AUTHOR-HAS-WITHDRAWN: `docs/plans/2026-09-20-genome-design-around-s2.md` §4 as written mixes two axes, and until its author amends it the extraction has nothing settled to extract against (HIGH, open, 2026-09-20 — Ark, who withdrew his own §4; filed by CC)

- **Observed.** `results/diagnostics/labels/README.md:6-8` records the withdrawal in the design's own terms: §4 **as originally written is WITHDRAWN by its author**, because its input rule treated pathway membership and response polarity as one axis — `polarity["L1"] == -1` while `"L1"` is listed in `on_pathway`, and `L3` appears in **both** `on_pathway` and `off_pathway`. The label check was therefore run in Ark's revised form, coverage first.
- **Observed.** Two further corrections are owed to the same file: `L5` is a **key** and not a field, and the four-question form is to be restated as revised.
- **Observed.** The design was placed by CC because the repository is read-only to its author, byte-identical to his copy; correcting it is his edit, not CC's.
- **Inferred.** This is the only thing blocking the extraction of the rule bank and the label array — the verified inventory (`docs/plans/2026-09-20-step0-label-inventory-verified.md`) already names the fields, so the block is the design's own internal contradiction and not a missing input.
- **First step.** **Ark** amends §4 in place, with a dated amendment note rather than a silent rewrite (the checklist's rule 16 convention), and restates the four questions. CC then starts the extraction. Related to [[THE-GENOME-DESIGN-AROUND-S2-NEEDS-LABEL-PROVENANCE-BEFORE-EXTRACTION]].
- **axis:** knowledge

### LITERATURE-SECTION-I-OWES-THREE-ADDRESSES-ITS-OWN-REVIEWERS-NAMED: a negative claim without its search instrument and two quoted figures without the address of the paper read are the same defect this file exists to prevent (MEDIUM, open, 2026-09-20 — Ark and Zcode, reviewing §I on the day it landed; filed by CC)

- **Observed.** §I of `literature.md` — digital evolution with inheritance, 24 entries read at source — was added 2026-09-20 and its reviewers named three fixes it owes:
  1. the negative claim that **no peer-reviewed work combines all of it** must state the **instrument of the search** — which engine, which queries, which language, which day — because an absent result is not an absent work, and §I.9 already writes that limit down for one of its own searches;
  2. the quoted counts from **Lehman & Stanley** and the **morphology-freeze figure** must carry the address of the paper actually read **inside the sentence that quotes them**, not only in the entry's header (Ark);
  3. **RepliBench**: the paper says five models and the release blog says seven — cite the paper's number, and name the other with its own address (Zcode, Ark).
- **Inferred.** All three are the same defect one level up from what the file is for: a figure whose address is in a different sentence than the figure travels without it, which is how the "loss step at 150,100" and the "11 of 12" both moved through the thread this session.
- **First step.** **CC** applies the three fixes in `literature.md` §I in one pass, each as an edit to the sentence that carries the claim rather than as a footnote; the reviewers who named them check the result.
- **axis:** honesty

### THE-OPENWORM-DATE-IS-CORRECTED-IN-ONE-SECTION-AND-STILL-WRONG-IN-FOUR-PLACES: `literature.md` §I.9 records that OpenWorm dates from 2011 and says so explicitly of §E and `idea.md` (then `idea_en.md`), which both still printed 2014, as do README and VISION (LOW, open, 2026-09-20 — Zcode found it, §I.9 records it; filed by CC)

- **Observed.** `literature.md:1121-1128`: *"OpenWorm 'since 2011' against this repository's 'since 2014' — Zcode is right, and both `idea_en.md` and §E of this file are wrong."* The project's own history page records the idea as a tweet of 2010-01-01 and the naming in early January 2011. The same passage says neither file was edited by that pass and that *"the correction lives here and should be carried wherever the date is next used."*
- **Observed — where it is still printed.** Four places, one correction, recorded in a fifth. Named by section rather than by line, because three of the four files were edited on the day this entry was written and a line number would already be stale: `idea.md` (then `idea_en.md`), the closing annotation under the block quote ("Two claims in the text did not survive the thread"); `literature.md` §E, first sentence; `README.md` § "The goal, in the owner's own words", the paragraph "Two annotations the idea carries about itself"; `VISION.md` § "What this is not", first bullet.
- **Inferred, and this is the whole difficulty.** `idea.md` (then `idea_en.md`) is a **verbatim translation file**: the sentence sits in the *annotation* under the block quote, not in the quote. So the idea itself never needs touching, and the annotation is the writers' own prose and may be corrected.
- **First step — proposed, not decided, because it touches a record file.** (a) In `idea.md` (then `idea_en.md`), leave the block quote untouched and correct the annotation's parenthesis to read *OpenWorm since 2011*, with a dated marker — **Corrected 2026-09-20 (Zcode):** the earlier annotation said 2014 — and a pointer to `literature.md` §I.9, so the change is visible as a change; `idea.md`, the Russian record, is not touched at all and the translation header already says it is not the record. (b) `README.md` and `VISION.md` carry the date in their own prose and are corrected outright. (c) `literature.md` §E is the one real question: §A–§H were deliberately not rewritten by the §I pass, so either §E gets the same dated marker or it keeps a pointer to §I.9 — **Mike's or the reviewers' call, not CC's**. No result value is involved anywhere.
- **Update 2026-09-23.** On Mike's word the repository became English throughout: `idea_en.md` was folded into `idea.md` (the Russian original of 2026-09-12 is in git history at `2488ecb`), and its annotation now reads *OpenWorm since 2011*, marked "corrected 2026-09-23" with a pointer to `literature.md` §I.9. Part (a) is done; `README.md`, `VISION.md` and §E still print 2014.
- **axis:** honesty, reach

### LAYOUT-IS-WHOLLY-BANK-DERIVED-AND-THEREFORE-CANNOT-JUDGE-ANYTHING-BUILT-FROM-THE-BANK: using it as a label would be circular, and it is the kind of field that gets picked up as an external yardstick precisely because it looks like one (MEDIUM, open, 2026-09-20 — from the label check, `results/diagnostics/labels/`; filed by CC)

- **Reported (the label check, `results/diagnostics/labels/`, run 2026-09-20 with its disposition hashed before any value).** `layout` is **wholly derived from the bank**. Anything predicted from the bank will therefore match it, and a match proves nothing about a model of the bank — it is the "synthesis ⇒ circular" case the check registered in advance (`results/diagnostics/labels/README.md`, the outcome table for (c)).
- **Observed, for contrast.** `polarity` is the opposite case and is the field that survives as external: it covers **32 of 65** types, it enters the repository only through `groundtruth_utils`, and the bank carries no polarity-like quantity at all (`results/diagnostics/labels/README.md`, "The denominator, fixed before running").
- **Inferred.** The risk is not that somebody argues for `layout`; it is that it is present, per-type, and tidy, so it gets used without the question being asked. The prohibition belongs somewhere a designer will hit it.
- **First step.** One line in the S2 design's field list and one in `docs/CHECKLIST-research-repo.md`: a bank-derived field is never an external label for a model of that bank, and every field proposed as a label states which of the two it is. Owner: **Ark** for the design, **CC** for the checklist line.
- **axis:** honesty

### THE-SIGN-COLUMNS-PROVENANCE-IS-MOSTLY-PERSONAL-COMMUNICATIONS-AND-IT-IS-WHAT-THE-GRAMMAR-MUST-REGENERATE: the one column a genome track would actually have to produce rests on citations that cannot be opened, and it is not one sign per source type (HIGH, open, 2026-09-20 — from the label check, `results/diagnostics/labels/`; filed by CC)

- **Observed (the check's own framing, registered before it ran).** `results/diagnostics/labels/README.md:102-113`: the sign sub-check runs *"regardless of (c)'s outcome, because **sign is what a genome track would actually have to regenerate**"*, and it asks of each source type's outgoing edge entries — *"one sign per source type, or not?"*
- **Reported (the answer, 2026-09-20).** It is **not** one sign per source type: **four types carry both**. And most of the column's citations are **personal communications** — sources that cannot be opened, checked or cited onward.
- **Inferred.** Two consequences for the grammar track, both named now rather than discovered later. (1) A grammar that emits one sign per type cannot reproduce the bank it is fitted to, so the representation has to carry sign at the level the bank does. (2) A target whose provenance is unopenable is a **named risk on the result**, not a defect of the bank: anything the grammar reproduces about sign inherits the confidence of a personal communication, and that has to be written into whatever is claimed, not discovered by a reader.
- **First step.** **Ark**, in the amended S2 design: state at which level the representation carries sign, and add a provenance line saying what a sign-level result may and may not claim. **CC** carries the same sentence into the extraction's README when the bank is extracted.
- **axis:** knowledge, honesty

### THE-GRAMMAR-IS-THE-MAIN-LINE-DECISION-IS-ACCEPTED-WITH-ITS-CONFIRMATION-LIST-UNTICKED: ADR-004 is accepted and its six confirmation boxes are all empty in the file, although its acceptance checklist was run before the commit (LOW, open, 2026-09-20 — CC, on reading the decision record at the session close)

- **Observed.** `docs/decisions/004-grammar-is-the-main-line.md` § "Confirmation" carries six items and every one of them is written `- [ ]`. The commit that placed the ADR (`470f834`) states in its message that *"Ark's acceptance checklist was run item by item before this commit"*, so the run happened and only its record is missing.
- **Observed — and most of the six are now true and checkable.** README, VISION and ROADMAP each state the goal with all five points and cite `idea.md` by author and date; ROADMAP has a grammar-track section with named owners outside the diagnostics section; the prohibition line distinguishes *growing* from *designing* in as many words; the line-number references below the edited regions were swept again in this session's close and converted to section pointers; the exclusion list was regenerated with `--required` passing and README is not on it.
- **Inferred.** An unticked confirmation list on an accepted ADR is the same class of defect as an `Updated:` field: it reports nothing, and a reader cannot tell "not done" from "done and not recorded". It is cheap to close and it will not close itself.
- **Open and genuinely undecided — the ADR's own Q2, for Mike.** *"What exactly is 'the elephant' beyond the grammar?"* The five-point reading is unopposed and unconfirmed, and no alternative reading has ever been written down. Q1 was answered on 2026-09-20; Q2 was not, and nothing in this session touched it.
- **First step.** **CC** ticks the confirmation items that are verified, naming the evidence beside each, and leaves unticked any that is not — a dated edit to the ADR's Confirmation section, not a rewrite of the decision. **Mike** answers Q2 if he wants it answered; if he does not, the ADR records that the question stands.
- **axis:** knowledge

### NEW-RUN-RECORDS-MUST-NAME-THE-CONNECTOME-AS-PACKAGE-VERSION-FILE-NOT-AN-ABSOLUTE-SCRATCHPAD-PATH: 25 of 113 tracked run records carry absolute Windows paths into a scratchpad that Mike deleted on 2026-09-20, and they resolve to nothing for any reader (LOW, open, 2026-09-23 — CC)

- **Observed.** `docs/notes/2026-09-23-scratchpad-paths-in-records.md`: a search of `results/**/*.json` for the scratchpad session id finds it in 25 of 113 files (fields such as `meta.netdir`, `env.scratch_netdir`, `connectome_file`, a launch's `argv`, a wave's `jobs[]`). The scratchpad itself was deleted by Mike on 2026-09-20; the paths now resolve to nothing for anyone. The existing records are left as written — several are pinned by hash — and the note is the reading key.
- **Inferred.** The defect repeats unless new records are written differently: the connectome is not reproduced in this repository, it ships inside the installed `flyvis` package, so a path into a session's private scratchpad was never the right handle for it.
- **First step.** New run records name the connectome as **package + version + file** (`flyvis 1.2.0 : connectome/fib25-fib19_v2.2.json`) and run directories relative to `FLYVIS_ROOT_DIR`, not as absolute paths on one machine.
- **axis:** collective


## IN PROGRESS

### C6-EXAM-BUILT-BLIND-AMENDED-ON-REGISTERED-CRITERIA-FIFTEEN-OF-SIXTEEN-PASS-R1-FAILS: the C6 exam was built without having read the rule proposal, found two defects and a toothless test in itself before scoring anything, was amended under acceptance criteria registered first, and the first rule run is still not approved (HIGH, in-progress, 2026-09-23 — CC as harness builder; Ark, Zcode, Johnny as reviewers; Mike, owner)

- **Observed.** results/genome/c6/harness.py (commit d443cf6) implements the exam with four controls -- an oracle, the null N1, a random projection, and 99 degree-preserving shuffles -- and a plug-in slot for a rule that carries nothing. The controls behaved as registered. The run also found, before any rule was scored: the size-matched stored-table comparison had no teeth (N1 alone costs about twice the size limit); N1 is weaker than the simpler N0 on offset sets; the random-projection arm always scores below N1. HARNESS-CONTROLS.md records all three, and two harness conventions not in the original spec are named. The harness builder had not read the rule proposal.\n- **Observed.** The amendment was registered before it was built, on Mike's word. docs/plans/2026-09-23-c6-amendment-acceptance.md (commit 4332d17) states what the amended exam must be able to do (reject a stored table, accept a planted small non-additive rule, stay non-trivial), what it may not do (introduce monotonicity), and freezing rules for its tuned constants -- written by the harness builder before the fix, under Mike's word of 2026-09-23 21:01 UTC to take option A. The amendment itself (commit dd34f9d) arms the budget arm, strengthens the offset-set target, raises P4 to a trained bilinear factorisation of the same rank, and adds a planted-rule acceptance suite; all controls re-ran with no rule.\n- **Observed.** 15 of 16 registered criteria pass; R1 fails and is recorded, not re-tuned. results/genome/c6/HARNESS-CONTROLS.md: at N1's own size the armed table does not beat N1 -- R1 fails as registered, reported rather than fixed by moving the goalposts.\n- **Observed.** The narrow-band finding. results/genome/c6/README.md, 'What the budget arm is for' (Ark, 2026-09-23 21:35 and 21:44 UTC, translated): in the 7.7-9.5 kbit band the verdict rests on N1 and the shuffle, not on storage -- R1's failure and this narrow band are recorded as one fact, home docs/plans/2026-09-23-c6-amendment-acceptance-2.md section 2.\n- **Observed.** Hubs, 14 of 18. HARNESS-CONTROLS.md section 4: H18 (top 18 types by leverage at rank k90) and U18 (top 18 types by fraction of cells unmoved by the 99 shuffles) overlap on 14 of 18 types (5.0 expected by chance, hypergeometric p = 1.1e-7); H18 is not the same object as k90 itself (a component count, not a set of types) -- P3 is reported unchanged by this finding, as registered.\n- **Observed.** A6 and the arm-role line are registered. docs/plans/2026-09-23-c6-amendment-acceptance-2.md (commit c75139a) registers the weak object A6 (PR-sh, which must lose on the budget arm alone) and the feasibility check A6-D with the corrector's prior written before the run, plus the budget arm's role in Ark's words and the scope of A1. Commit 678afbd then runs A6: PR-sh fails every arm, and A6-D fails on both banks -- within the size limit the armed table is worse than N1 in-sample at every affordable k, so the budget arm cannot be the sole reason a rule fails, matching the registered prior. Commit 2e36a6d registers search-budget parity (every trained opponent gets the rule's own number of restarts k, chosen on the training objective only) before the code for it exists.\n- **Observed.** A restart-parity request from Ark is in progress. docs/plans/2026-09-23-c6-amendment-acceptance-3.md (commit 2e36a6d): Ark, genome track, 2026-09-23 21:48 UTC, relayed and paraphrased -- 'search is free in description length, so an opponent given less search than the rule is a weaker opponent.' The registration (start-0 = SVD start, seeded perturbed starts, best-on-training-loss selection) is committed; the harness code for it is not yet built.\n- **Reported, not independently verified from this repository (Mike, 2026-09-23).** Mike's separate word at 21:59 UTC gave 'yes to preparation' -- yes to finishing A6 and BF restart parity and to measuring fitting-code timing, not yet yes to running the rule.\n- **Reported, not independently verified from this repository (Mike, 2026-09-23).** Zcode, the mechanical reviewer, disclosed at 21:43 UTC that he had opened the rule proposal -- a fact about a reviewer's own blindness, recorded here because the reviewers below must weigh it
- **Inferred.** the exam's own construction discipline -- folds and birth ids committed before any rule (9ed0dae), the rule proposal registered separately and unread by the harness builder (5a46886), acceptance criteria registered before each fix (4332d17, c75139a, 2e36a6d) -- is what makes R1's FAIL and the 15/16 pass rate readable as a result rather than as a number tuned to look good. The content of the rule proposal is deliberately not restated here or anywhere on this board: reviewers Ark (content) and Johnny read the backlog and must stay blind to the rule until they review it on its own terms; see docs/plans/2026-09-23-first-rule-proposal.md, registered at commit 5a46886, not yet run
- **First step:** finish A6 and the BF restart-parity code; implement the rule's fitting code; measure timing on shuffled bank 0; only then does Mike give his separate, explicit yes on running the rule against the exam. The first rule run is NOT yet approved. Reviewers: Ark (content review, has not opened the rule), Zcode (mechanical review only; disclosed 2026-09-23 21:43 UTC that he has opened the rule), Johnny (has not opened the rule)
- **2026-09-23, CC:** **2026-09-24, CC — the first rule was run once and FAILS C6.** On Mike's word (2026-09-24 06:58 UTC), the rule path went in at 958a976; the first attempt crashed at 44.9 s on a missing log directory, before any verdict (89683c6); the single real run is 8528061. Verdict, verbatim: 'FAIL -- rule did not run; copy or marginal; below threshold for this family; family fits anything; ambient, not substantive structure' (k = 10, r = 12). DL 6,992 bits, within the 9,481.2 limit. Held-out existence 0.3670 against N1 0.3625 (5 of 10 folds, 9 needed); in-sample 0.2547 against 0.3354. Offset set is worse than N0 and N_EB; counts lose to N0 in 10 of 10 folds; sign equals N1 by construction. P3 existence p = 0.01 (the real margin is above all 99 shuffles), offset p = 0.98. The spread log is 1,340 of 1,341 lines, marked unreliable. Records: results/genome/c6/rule_runs/first_rule_k12/RESULT.md. Next: Ark's check of the verdict; a failure analysis against the proposal's section 4 before any second rule.
- **2026-09-23, CC:** **2026-09-23, CC — date correction to the note above:** it is headed 2026-09-24 and quotes Mike's word at '2026-09-24 06:58 UTC'; both are 2026-09-23 (Mike, 06:58 UTC; the run was committed on 2026-09-23 UTC). Nothing else in the note changes.
- **axis:** honesty, knowledge
- **filed:** CC · 2026-09-23

## BLOCKED ON DECISION

### THE-PERTURBATION-LADDER-MEASURES-HOW-FAST-AN-INDIVIDUAL-FORGETS-ITS-INITIAL-CONDITION: under deterministic training, one seed with one parameter nudged by a controlled amount answers a question the authorised night could not, and it waits on Mike's word (HIGH, open, 2026-09-20 — CC and Ark, after both concluded the authorised night 6 shape is vacuous; Mike, owner, 2026-09-20 10:02 UTC: he does not want to spend the night)

- **Observed — why the night it replaces was dropped.** The authorised shape ("two deterministic pairs") was **not launched**. Under determinism the same seed gives the same run, so the replicate spread is not zero, it is **undefined**: there is nothing for a between-seed spread to be compared with, and the night would have cost about 13.4 h per full run to produce a comparison with no second term. CC and Ark reached this separately, before launch, and the brief records the design as written with the decision left to the owner (`docs/briefs/2026-09-20-night6-deterministic-pairs.md`).
- **Observed — what is already measured, and what it licenses.** Deterministic training costs about **3.33×** the nights' mode with **no operator refusing**, and the same seed twice under determinism is **bitwise identical over 2,000 iterations** — the first measurement of determinism on the *training* path (`docs/briefs/2026-09-20-night6-deterministic-pairs.md` §5, `results/night6/`). Bitwise identity is exactly what makes a ladder readable: under determinism the night has an exact zero of its own, so any movement is the perturbation and nothing else.
- **The design, as proposed and NOT authorised.** One seed, trained deterministically, with **one parameter nudged by a controlled amount**; the nudge stepped in float32 units of least precision, from one step up to the full difference between two different seeds. The perturbed parameter is an **edge** parameter and **not** `nodes_bias` — Ark's condition, because the activity penalty is a restoring force on the biases for the first 150,000 iterations, so a nudge there is actively pushed back and the ladder would measure the penalty rather than the system. Read **by shape**, the readout the profiles pointed at, against the night's own exact zero.
- **Inferred.** What it measures is not σ_rep. It is how fast the system forgets its initial condition — how large a perturbation an individual survives and still reads as itself — which is the "does an individual exist" half of [[NON-DETERMINISM-IN-TRAINING-MAY-BE-THE-SOURCE-OF-THE-REPLICATE-GAP]], and is the operational form of the literature's own advice that the fix for noisy selection is to change what counts as the point (`literature.md` §I.5).
- **First step.** **Mike's word, yes or no.** On yes: the reading rule is written and registered **before launch** — what counts as "still the same individual", at which rung, by which distance, and what each outcome licenses — and reviewed, before a single rung is run; the ladder's cost is then set by how many rungs the rule asks for, not by a night. On no: this entry closes and the individuality question stays answered only descriptively, from checkpoints already on disk.
- **2026-09-23, CC:** paused by Mike's word of 2026-09-20 10:15 UTC (ADR-004 amendment); stays open.
- **axis:** honesty

### ROWB-PY-CANNOT-ADDRESS-A-FUTURE-NIGHTS-RUNS-WITHOUT-AN-ADDITIVE-RUN-COLUMNS-OPTION: the profile instrument selects runs by night, so any night after night 5 needs either a script change or a new script, and the cheap fix is one additive switch (MEDIUM, open, 2026-09-20 — CC, from preparing night 6 against the existing instrument)

- **Observed.** `results/night5/diagnostics/rowB/rowB.py` selects what it reads with `--night {4,5,all}` and `--netdir`; there is no way to hand it an explicit list of runs and the columns they belong to. Night 6 was prepared against it, which is how the gap was found (`docs/briefs/2026-09-20-night6-deterministic-pairs.md`, the section on what `rowB.py` needs in order to address night-6 netdirs).
- **Observed — the defect it would also cure.** The board already carries [[THE-CORRESPONDENCE-BETWEEN-A-RUN-AND-ITS-COLUMN-KEEPS-BEING-INFERRED-FROM-A-NAME-INSTEAD-OF-RECORDED]] with three instances, two of them wrong. A `--run-columns` option that takes the mapping **as a file** is the same cure applied to the instrument: the correspondence is handed in, written down, and never re-derived from a directory name.
- **Inferred.** Additive means additive: existing invocations must produce byte-identical output, the way the three launcher switches added this session did (legacy dry runs byte-identical, `docs/briefs/2026-09-20-night6-deterministic-pairs.md`). A non-additive change to an instrument that has already produced a committed record would make the record unreproducible by its own script.
- **First step.** **Mike's word, yes or no.** On yes: **CC** adds `--run-columns <file>` reading an explicit run→column→netdir table, leaves every existing flag and default untouched, and proves additivity by re-running one committed dry run and diffing the bytes — before any new night is launched, not during one. On no: every future night writes its own mapping again, and the correspondence entry above gets its fourth instance.
- **2026-09-23, CC:** paused by Mike's word of 2026-09-20 10:15 UTC (ADR-004 amendment); stays open.
- **axis:** collective

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
  the same seed; see `ROADMAP.md` Phase 2 item 3(i). *(Citation de-numbered 2026-09-20, CC: it read `ROADMAP.md:154-160`, which is a position and moves with every edit above it.)*
- **First step:** Mike + reviewers read docs/experiments/002-night2-seeds-1-and-2.md and choose branch (a) (continue to the floor N, nights 3-5) or (b) (a new pre-registration for the expensive metric before any further N run) per docs/next-session-plan.md §3.
- **2026-09-23, CC:** paused by Mike's word of 2026-09-20 10:15 UTC (ADR-004 amendment); stays open.
- **axis:** honesty
- **filed:** CC · 2026-09-15

### THE-COMPOSITION-MARGIN-OVER-ITS-FLOOR-IS-SMALLER-THAN-A-NULL-SHIFTS-MEDIAN-DELTA: the registered (a) splice reads "composes predictably" by a 0.40 margin over a floor borrowed from the replicate difference, while a null shift of the same norm moves the loss further and the reverse splice explodes (HIGH, open, 2026-09-15 — CC, from the splice_a diagnostic and Ark's null-shift calibration, 2026-09-15)

- **Observed.** Registered splice T2_A ← T2_B (B = seed 1, A = seed 0, checkpoint 250,008; docs/experiments/002-night2-seeds-1-and-2.md §5g, results/night2/diagnostics/splice_a/): Δ = +38.579946, 3.3583 % of L_A (1148.8074), 3.3659 % of the pre-registration's literal basis 1146.1958. By docs/preregistration-cheap-vs-expensive.md §5 (a)'s rule (floor 38.18, 5 % bound 57.31 on that basis): 38.18 < 38.58 < 57.31 → "composes predictably for this pair", margin 0.40. Self-splice A←A (the mandatory instrument control) is a no-op, +1.4e-5. A null-shift calibration written before the splice (Ark, chat 07:33) drew 20 isotropic random 26-vectors of the same norm as B−A (r = 0.38185): 4 diverge, the 16 finite |Δ| range 10.70-69.55, mean 44.44, median 46.07 — above the registered splice's own 38.58 — and 10 of 16 sit above the floor 38.18. The reverse splice (A→B) gives Δ = +2029.00 (+177.3 %), outside the registered test.
- **Reported.** Ark's calibration (chat 2026-09-15 07:33) and Zcode's bundling it with the splice run (07:43) were both proposed before the registered splice was evaluated; run order verified by the timestamps inside `splice_a/calibration.json` (07:54:06Z) and `splice_a/splice_result.json` (07:55:37Z).
- **Inferred.** The registered category is recorded as the pre-registration's rule reads it, but the margin above the floor (0.40) is smaller than what a directionless shift of the same size does to the loss on the median draw (46.07) — the floor (3× the replicate difference) was not measured from this operation's own null and may not be the right instrument for it.
- **First step.** Mike + reviewers decide the reading: stands as the rule reads it / relabelled uninformative by the calibration / the floor is re-registered from the operation's own null distribution — a floor measured from the operation's own null needs its own registration, not a retrofit onto this one. See [[THE-SPREAD-REPLICATE-RATIO-INVERTS-BETWEEN-C3-AND-THE-TOP-RUNG]].
- **2026-09-23, CC:** paused by Mike's word of 2026-09-20 10:15 UTC (ADR-004 amendment); stays open.
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
- **2026-09-23, CC:** paused by Mike's word of 2026-09-20 10:15 UTC (ADR-004 amendment); stays open.
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
- **2026-09-23, CC:** paused by Mike's word of 2026-09-20 10:15 UTC (ADR-004 amendment); stays open.
- **axis:** honesty
