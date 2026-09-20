# Retrospective — session S2026-09-20.2 (2026-09-19 19:47 UTC → 2026-09-20 10:06 UTC)

**Written by:** CC, on Mike's word (DPC Research group, 2026-09-20 10:06 UTC: close the session,
make the current state visible in all documents, everything in English). **Audience:** Mike and
the reviewers. Every claim below is Observed unless marked, and every one of them names the file
that carries it.

**This file carries no result value.** No loss, ratio, standard deviation, distance or p-value
appears in it; where a finding is numerical, the reading file that holds the number is cited
instead. Structural counts (runs, individuals, checkpoints, files, entries), dates, registered
configuration constants and the instrument's own timing ratios are not results and are written
plainly. The intent is that this page stays readable by the blind author of
[ADR-003](../decisions/003-blind-authorship-after-the-numbers.md); the generated list
([`docs/blind-author-exclusions.txt`](../blind-author-exclusions.txt)) is the authority on
whether it succeeded, not this paragraph.

**Session envelope.** The work is the local day 2026-09-20. Its seven commits run from
`effaff2` (2026-09-19T19:47Z) to `b9c86c6` (2026-09-20T10:03Z); Mike closed the session three
minutes after the last of them. The session identifier continues the board's scheme by hand:
the mechanical derivation in `docs/BACKLOG_FORMAT.md` § "The session identifier" reads reset
files that do not exist for this group, so `.2` is the next position after the `S2026-09-20.1`
already used in `backlog_closed.md` today.

---

## 1. What the session produced

- **The environment's residue is closed.** The venv move itself had been done on 2026-09-18/19;
  what was left was everything around it. The scratchpad's raw artefacts were copied to
  `connectome-seed-archive/flyvis-probe-63f3961a/` outside the repository and verified pairwise
  by hash, twice and independently (CC, Zcode), zero differing; the environment is pinned in
  `tools/night/requirements-frozen.txt` as a record rather than an install recipe; Mike deleted
  the scratchpad original by hand after the checks; the stale duplicate board entry was closed.
  Commit `effaff2`.
- **The note the grammar track was waiting on.**
  [`docs/notes/2026-09-20-what-is-the-genome-here.md`](../notes/2026-09-20-what-is-the-genome-here.md)
  — what is inherited, seeded and learned in one individual, read from source with `file:line`.
  Three things it establishes: the substrate holds one production over a lookup table that is
  not generative; an individual is an initial condition on wiring identical in every individual;
  and one `--seed` is spent on the cell-type biases *and* on the global RNGs, so two individuals
  differ in decoder initialisation and data order as well. The third corrects the 2026-09-19
  handover.
- **Row B, built and run on all ten runs in two modes.**
  `results/night5/diagnostics/rowB/` — instrument, protocol and controls written before any
  value existed, reviewed by three reviewers, with each reviewer's finding landing in the
  instrument rather than in a report. Ten runs, six individuals, 72 checkpoints each, reduction
  on the GPU. Both reductions of "65 numbers" are recorded separately, the type axis is
  fingerprinted against row A's, and every record carries its reduction path and determinism
  mode.
- **The penalised quantity, read once across its own boundary.**
  `results/night5/diagnostics/rowB/PENALISED-QUANTITY-READING.md`, on Mike's word, with the
  rule's branches stated before the first value.
- **The row B profiles, read once.**
  `results/night5/diagnostics/rowB/PROFILES-READING.md`, on Mike's word, the reading's rule
  hashed before any value was opened.
- **A label check that its own author revised before it ran.**
  `results/diagnostics/labels/` — disposition hashed first, in the form Ark rewrote after
  finding that his own input rule mixed two axes.
- **Step 0 of the genome design, verified against source.**
  [`docs/plans/2026-09-20-step0-label-inventory-verified.md`](../plans/2026-09-20-step0-label-inventory-verified.md)
  checks Ark's field inventory against `groundtruth_utils.py` itself rather than against the
  brief it was relayed from.
- **Ark's design placed, with its own withdrawal on the record.**
  [`docs/plans/2026-09-20-genome-design-around-s2.md`](../plans/2026-09-20-genome-design-around-s2.md),
  byte-identical to his copy, placed by CC because the repository is read-only to its author.
- **Night 6 prepared and not launched.**
  [`docs/briefs/2026-09-20-night6-deterministic-pairs.md`](../briefs/2026-09-20-night6-deterministic-pairs.md)
  and `results/night6/`: the feasibility probe, the determinism control on the training path,
  the gate that turned out blind and its replacement, four costed designs, and the launch
  commands dry-run from the repository.
- **`literature.md` §I — digital evolution with inheritance**, 24 entries read at source, each
  saying how far it was read and what it says to the idea's five points, with a list of what
  could not be verified.
- **The goal restored to the three top-level documents.** README, VISION and ROADMAP state the
  goal from `idea.md` by point number, and [ADR-004](../decisions/004-grammar-is-the-main-line.md)
  records the ordering. Commit `470f834`.
- **Housekeeping.** The blind-author values file was given a holder and a recorded path
  (`tools/contamination_scan.py` docstring); the exclusion list was regenerated after each
  commit that changed the tree, and the scanner now names today's new result directories
  outright, because a directory created today is covered by no earlier list; `tools/atlas`
  builds a single page for the owner from what the repository already holds machine-readable,
  with a hatch wherever no verdict exists; Mike wired the orbit index and the MCP hooks.

## 2. What was found

Each item names the file that carries its numbers. None of them is a test, and none changes a
registered rule.

1. **Evaluation non-repeatability is GPU operation order, not the recording hook.** The
   registered P1′ tolerance was never amended. In the mode the nights ran in it fails in most
   pairs; with deterministic algorithms on it passes in every pair of the full run, with an
   exactly zero difference and an exactly zero floor, and no operator refused. The deterministic
   run is the record because it recomputes to the bit; the two modes are never pooled.
   `results/night5/diagnostics/rowB/README.md`.
2. **The 150,000 boundary does not bind.** The penalised quantity is smooth across it in all ten
   runs, and held-out loss shows no step there either.
   `results/night5/diagnostics/rowB/PENALISED-QUANTITY-READING.md`. A claimed "loss step at
   150,100" in the thread was seconds per iteration, not loss — the two timing sub-gates of
   `docs/briefs/2026-09-17-night5.md` §4.4, which exist because the penalty optimiser is dropped
   at `stop_iter` and that changes the per-iteration cost, not the network.
3. **The whole replicate gap is made inside training.** Before training, replicates of one seed
   are identical; at the end they differ by the whole gap.
   `results/night5/diagnostics/rowB/PROFILES-READING.md`.
4. **An individual shows in the shape of its profile, and not where we had been looking.** At the
   end, replicates resemble each other by the rank *shape* of the 65-type profile and not by its
   *magnitude*, and not by held-out loss. The declared answer was MIXED and is reported as MIXED.
   Same file.
5. **Ark's review of (4), recorded as review** — *Ark, reviewer, DPC Research group, 2026-09-20
   09:45 UTC (translated from Russian):* count by margin, not by wins; one "win" is a tie at
   printed precision; the shape result rests on one individual of two when each pair is judged
   against the *nearest foreign* run; pairs within an individual are not independent, so the
   denominator is individuals and not pairs; and the rank order of types at the start is set by
   the connectome, not by the seed. This review is not yet a file of its own in the repository;
   this paragraph is its record.
6. **A later descriptive recomputation by CC, over the last 29 checkpoints** — post hoc,
   description only, never a verdict: by loss and by magnitude, replicates are as far apart as
   different individuals; by shape, different individuals are about twice as far apart as
   replicates, for both individuals that have replicates. **(5) and (6) are recorded side by
   side and neither is chosen.**
7. **The source of the replicate gap is established.** Ark read the configs and CC's control
   measured it: replicates are copies of one config to the last field, identical at iteration 0,
   differing by under one float32 step at iteration 12, and by the whole replicate gap at the
   end. The mechanism is GPU operation order in training.
8. **Determinism on the training path, measured for the first time.** Deterministic training
   costs about 3.33× the nights' mode and no operator refused; the same seed twice under
   determinism is bitwise identical over 2,000 iterations. Gate 7 turned out blind to the
   determinism flag, and gate 7b is registered.
   [`docs/briefs/2026-09-20-night6-deterministic-pairs.md`](../briefs/2026-09-20-night6-deterministic-pairs.md).
9. **The authorised night could not answer its own question.** Under determinism the replicate
   spread is undefined rather than zero, so there is nothing to compare a between-seed spread
   with. CC and Ark reached this separately; one full deterministic run costs about 13.4 h.
10. **The label bank carries no polarity-like quantity at all.** Nothing was copied and nothing
    synthesised; three of the four questions are not runnable and are recorded as such.
    `polarity` is therefore a genuinely external label on the 32 types it covers, and still
    unattributed; `layout` is wholly bank-derived and cannot judge anything; synapse sign is not
    one per source type — four types carry both — and most of its citations are personal
    communications. `results/diagnostics/labels/README.md`.
11. **Consequences from `literature.md` §I that the design must carry.** Birth ids that are
    never reused have to be decided before the first genome, and assigned at generation zero on
    the bank itself — 65 type names, 605 rows (Ark). "A rule instead of weights" is a bet with a
    measurable threshold, and here regularity is measured at the *rule* level, where it is
    maximal — the table is identical at extent 5 and extent 15, and `pattern` takes two values —
    and is **not** measured at the level of the type-pair table, which is where all the entropy
    sits and what a grammar would have to produce (Ark). HyperNEAT-style coordinate functions
    give modules no identity and so conflict with point 3's module inheritance (Ark). And
    noisy-selection cures do not transfer, because re-evaluating "the same point" here gives
    diverging trajectories rather than samples around a mean — the fix is to change what counts
    as the point, and define and select an individual by shape (Ark).

## 3. What was decided, and by whom

ADR-001 form: name, role, date, UTC, no chat links.

| decision | who | when (UTC) |
|---|---|---|
| The grammar track is the main line; measuring the fly is its instrument and runs in parallel. Recorded as [ADR-004](../decisions/004-grammar-is-the-main-line.md), accepted. | Mike Shevchenko, owner | 2026-09-20 09:27 |
| CC is the holder of the blind-author values file; its path is recorded in the scanner's docstring. | Mike Shevchenko, owner | 2026-09-20 |
| Row B's scope is extended from three checkpoints to all ten runs. | Mike Shevchenko, owner | 2026-09-20 |
| The penalised quantity is read once; the row B profiles are read once. | Mike Shevchenko, owner | 2026-09-20 |
| **`activity_penalty.stop_iter` is left untouched.** The "two regimes" card weakens at the boundary; its observation stands under a better name — the cheap probe at 25,000 sits in an unsettled phase. | Mike Shevchenko, owner | 2026-09-20 |
| The night is not spent: the authorised "two deterministic pairs" is not launched and the resources can go elsewhere. | Mike Shevchenko, owner | 2026-09-20 10:02 |
| The generated ROADMAP status block, rewritten mechanically during a rebuild without the word its entry asked for, is kept. | Mike Shevchenko, owner | 2026-09-20 |
| `atlas.html` and `tools/atlas/` are named in the blind-author exclusions regardless of the scan, together with this day's history. | Mike Shevchenko, owner | 2026-09-20 |
| Close the session; the current state must be visible in all documents; everything in the project in English. | Mike Shevchenko, owner | 2026-09-20 10:06 |

**Reviews that changed something, attributed.** Ark, reviewer — the profiles review of §2(5); the
withdrawal of his own §4 check in the S2 design after finding its input rule mixed two axes; the
three-branch wording of the boundary rule, recorded with the provenance that it was written after
the reading; the demand that today's new result directories be named in the scanner outright; the
perturbation target (an edge parameter, not `nodes_bias`, because the activity penalty is a
restoring force on the biases for the first 150,000 iterations). Johnny, reviewer — the no-hook
floor taken at the loss level, where P1′ is judged. Zcode, reviewer — the second independent hash
verification of the archived artefacts; with Ark, the RepliBench discrepancy in §I. Zcode and Ark
together caught that the exclusion list had not been regenerated for two commits.

## 4. What was not done

- **The perturbation ladder is proposed and not authorised.** Under deterministic training, one
  seed, one parameter nudged by a controlled amount, steps in float32 ULPs up to the full
  seed-to-seed difference, on an *edge* parameter; read by shape, against the night's own zero;
  its reading rule to be registered before launch. It measures how fast the system forgets its
  initial condition. Mike's word is owed.
- **Night 6 was not launched** and is superseded by the proposal above unless Mike revives it.
- **Ark's amendment to the S2 design is owed** — the axis mix-up, `L5` being a key and not a
  field, and the revised four-question form. CC's extraction of the rule bank and the label array
  is unblocked except for it.
- **Zcode's C6 control specification is not started**, and is blocked by nothing.
- **`literature.md` §I owes three address fixes** (see §5).
- **The 2026-09-19 handover still overstates what a seed moves.** Checked this session:
  `docs/briefs/2026-09-19-genome-track-handover.md` §3 still reads "The 65 biases are the whole
  of individuality". Its board entry stays open.
- **The blind v2 registration is still deferred, not cancelled** (ADR-003).
- **The nineteen tool-hardening fixes still wait on Mike's word**, as does the step 2 tuning
  battery, whose brief has been ready since 2026-09-16.
- **The pre-flight GPU-memory override is moot** until a night is launched.
- **The remaining unarchived scratchpad material is undecided** — Mike's call.

## 5. Errors this session, and whose

Stated plainly, because the pattern is the useful part.

**CC.**
1. **Three wrong cost estimates.** All three were reported to the thread before anything was
   measured, and all three were optimistic in the same direction. The class is the same one the
   2026-09-14 retrospective already named: extrapolating from a probe that did not cover the
   regime the claim was about.
2. **"Determinism on" claimed when it was off.** Reported in the group chat and written into a
   board entry's first wording; corrected in both places the same day. The nights ran with
   `--no-determinism` and the evaluation path mirrored them deliberately.
3. **An 11-of-12 count that was 10.** The handover said the with-hook difference equalled the
   no-hook floor in 11 of 12 pairs with one exception; it is 10 of 12 with two, and the second
   exception is an *under*-floor pair rather than an over-floor one. Found by recount.
4. **The goal rebuilt from paraphrase.** The project's goal was reconstructed from chat
   summaries and narrowed to the first of its five points while `idea.md` sat in the repository
   root. CC's first patch for this did the same thing again and cited two agents instead of the
   file beside it; Ark caught it, and the second patch is sourced by point number.
5. **One-line unformatted chat messages.** Findings were sent to the group as bare lines with no
   structure, which is how the "loss step at 150,100" and the "11 of 12" both travelled further
   than their evidence.
6. **A device bug in the first row B launch** — reduction tensors created on CUDA while the
   activity had been moved to CPU. Caught by execution on the first run, fixed the same day.
7. **The exclusion list was left unregenerated by two commits in a row**, recorded as "Not done"
   in each of their messages and then done.

**Ark.** His own §4 check in the S2 design is withdrawn by its author: the input rule mixed two
axes. He found it himself, by reading the same file again, and the amendment is owed rather than
disputed. The design's field inventory had also been relayed from a brief rather than read from
flyvis — the design says so and makes checking it step 0, which is why the error cost a check
rather than a result.

**Reviewers collectively.** `literature.md` §I owes three corrections its own reviewers named:
the negative claim "no peer-reviewed work combines all of it" needs its search instrument stated;
the quoted counts from Lehman & Stanley and the morphology-freeze figure must carry the address
of the paper actually read *in the sentence* (Ark); and RepliBench — the paper says five models,
the release blog says seven, so cite the paper's number and name the other with its address
(Zcode, Ark).

**The session's process finding.** Five times in one day, four agents passed on a paraphrase
instead of opening the source, and every one of the five was caught by somebody opening the file:
the goal itself, the ablation citation in the field list, the "loss step" that was seconds per
iteration, the field inventory relayed from a brief, and the label table. A paraphrase that
survives one hop is indistinguishable from a reading; what separated them each time was the file,
not the argument. The checklist rule this suggests is not new — it is rule 15 of
`docs/CHECKLIST-research-repo.md` applied to prose rather than to tables.

## 6. Open at close — all wait on Mike's word

1. **The perturbation ladder** — yes or no. Yes buys the first measurement of whether an
   individual survives a perturbation of its own initial condition, on GPU time far below a
   night. No leaves "does an individual exist" answered only descriptively.
2. **An additive `--run-columns` option for `rowB.py`** — yes or no. Yes lets any future night be
   read by the profile instrument without a new script; no means each night writes its own
   mapping again, which is the correspondence defect the board already carries.
3. **Ark's level-versus-shape decomposition of the MIXED reading** — free, descriptive only, and
   carries no verdict either way.
4. **Pre-flight GPU-memory override** — moot until a night is launched.
5. **Blind v2 registration** — still deferred, not cancelled.
6. **The remaining unarchived scratchpad material** — archive or discard.

Owners of what is next, on the grammar track: **Ark** amends the S2 design and then does the
design work proper; **Zcode** writes the C6 control specification, not started; **CC** extracts
the rule bank and the label array per the verified inventory, unblocked except for Ark's
amendment. All three read `literature.md` §I.1 before proposing a rule.

Next session: [`docs/briefs/2026-09-20-next-session-handover.md`](../briefs/2026-09-20-next-session-handover.md).
