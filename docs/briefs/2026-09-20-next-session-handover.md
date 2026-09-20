# Handover — for the session that starts after 2026-09-20

**Written:** 2026-09-20 UTC, by CC, on Mike's word (DPC Research group, 2026-09-20 10:06 UTC:
make the current state visible in all documents, everything in English, and close the session).
**Audience:** whoever opens this repository next, human or agent.

**This file carries no result value** — no loss, ratio, standard deviation, distance or p-value.
Where a finding is numerical, the file that holds the number is named instead. Structural counts,
dates, registered configuration constants and the instrument's own timing ratios are not results.
It is written to be safe for the blind author of
[ADR-003](../decisions/003-blind-authorship-after-the-numbers.md) and is listed in
`tools/contamination_scan.py` as required reading, which means the scan refuses if it ever stops
being value-free.

**It does not replace [`2026-09-19-genome-track-handover.md`](2026-09-19-genome-track-handover.md).**
That file is still the handover for the grammar track and its §6 is still the blind-author rule.
This file says what changed after it, what is blocked on what today, and what is waiting for a
word. Where the two touch, the older one is cited rather than restated — with one correction,
named in §5 below, that the older file has not yet absorbed.

---

## 1. Before you read anything: say which of the two jobs you are

There are two jobs in this repository and they may not be the same session.

- **The sighted job** — the grammar track, the measurement track, the board, the documents. It
  may read everything.
- **The blind job** — the v2 registration of the reachability endpoint (ADR-003). It must not
  read the material that carries v1's numbers.

**Declare the role before opening a single file.** That rule is
[`2026-09-19-genome-track-handover.md`](2026-09-19-genome-track-handover.md) §6 and it is
unchanged. If you are the blind author, go to §5 of this file first and do nothing else until you
have done what it says.

## 2. The state in one page (2026-09-20)

**The goal** is the five points of [`idea.md`](../../idea.md) plus the evolutionary tree as the
main artefact (Mike Shevchenko, author, 2026-09-12 12:18), in English in
[`idea_en.md`](../../idea_en.md). It is quoted by point number and never restated from chat:
[ADR-004](../decisions/004-grammar-is-the-main-line.md). **The grammar track is the main line;
measuring the fly is its instrument and runs in parallel** — Mike, owner, 2026-09-20 09:27 UTC.
Growing anything stays blocked until Phase 2 has a number; *designing* is not growing, and the
prohibition is narrowed to the former.

**The measurement track.** Ten runs are on disk — six individuals, two of them run three times —
and nothing beyond that is a test. What was learned in this session, with the file that carries
each number: evaluation non-repeatability is GPU operation order and not the recording hook, and
under deterministic algorithms the registered control passes unamended
(`results/night5/diagnostics/rowB/README.md`); the 150,000 boundary does not bind — the penalised
quantity is smooth across it in all ten runs and held-out loss shows no step there
(`results/night5/diagnostics/rowB/PENALISED-QUANTITY-READING.md`), so **`stop_iter` is left
untouched** by Mike's decision of 2026-09-20; the whole replicate gap is made inside training, and
at the end an individual shows in the rank *shape* of its 65-type profile rather than in its
magnitude or in held-out loss, declared and reported MIXED
(`results/night5/diagnostics/rowB/PROFILES-READING.md`). Ark's review of that reading and a later
descriptive recomputation by CC are recorded side by side, without choosing, in
[`../retrospectives/2026-09-20-session-close.md`](../retrospectives/2026-09-20-session-close.md)
§2.

**Night 6 is prepared and was not launched.** The brief is
[`2026-09-20-night6-deterministic-pairs.md`](2026-09-20-night6-deterministic-pairs.md):
deterministic training measured at about 3.33× the nights' mode with no operator refusing, the
same seed twice bitwise identical over 2,000 iterations, gate 7 found blind to the determinism
flag and gate 7b registered. The authorised shape was dropped because it cannot answer its own
question — under determinism the replicate spread is undefined rather than zero, so there is
nothing to compare a between-seed spread with — and Mike declined to spend the night
(2026-09-20 10:02 UTC). A **perturbation ladder** is proposed in its place and is not authorised:
see §4.

**The grammar track.** The note is delivered
([`../notes/2026-09-20-what-is-the-genome-here.md`](../notes/2026-09-20-what-is-the-genome-here.md)).
Ark's design is placed
([`../plans/2026-09-20-genome-design-around-s2.md`](../plans/2026-09-20-genome-design-around-s2.md))
with an amendment owed by its author. The label check is done
(`results/diagnostics/labels/`) and step 0 verified the field inventory against source
([`../plans/2026-09-20-step0-label-inventory-verified.md`](../plans/2026-09-20-step0-label-inventory-verified.md)).
`literature.md` §I — digital evolution with inheritance, 24 entries read at source — is in, with
three address fixes owed.

## 3. Owners, and what is blocked on what

| piece | owner | state |
|---|---|---|
| Amendment to the S2 design (axis mix-up; `L5` is a key, not a field; the revised four-question form) | **Ark** | owed — **this is the only thing blocking the extraction** |
| The design work proper, after the amendment | Ark | not started |
| C6 control specification | **Zcode** | not started, **blocked by nothing** |
| Extraction of the rule bank and the label array, per the verified inventory | **CC** | unblocked except for Ark's amendment |
| Read `literature.md` §I.1 before proposing a rule | Ark, Zcode, CC | standing precondition |
| The note "what is the genome here" | CC | **delivered** |

Nothing on this track needs a GPU and nothing on it is blocked by the nightly accrual — true
since 2026-09-16 and rediscovered as a fresh idea more than once, which is why it is written here
as well.

Three things stay blocked on the owner rather than on work: the step 2 tuning battery (brief ready
since 2026-09-16), the nineteen tool-hardening fixes, and the blind v2 registration (deferred, not
cancelled).

## 4. Open decisions, and what each choice actually changes

1. **The perturbation ladder — run it or not.** Under deterministic training: one seed, one
   parameter nudged by a controlled amount, in steps of float32 units up to the full
   seed-to-seed difference, perturbing an **edge** parameter rather than the cell-type biases,
   because the activity penalty is a restoring force on the biases for the first 150,000
   iterations (Ark). Read by shape, against the night's own zero, with the reading rule
   registered before launch. *Yes* buys the first measurement of how fast the system forgets its
   initial condition, at GPU cost far below a night. *No* leaves "does an individual exist"
   answered only descriptively, from checkpoints already on disk.
2. **An additive `--run-columns` option for `rowB.py` — yes or no.** *Yes* lets a future night be
   read by the profile instrument without writing a new script, and writes the run→column
   correspondence down instead of deriving it from a name. *No* means the next night repeats the
   defect the board already carries under that name.
3. **Ark's level-versus-shape decomposition of the MIXED reading.** Free, descriptive only, and
   carries no verdict either way. Nothing depends on it.
4. **Pre-flight GPU-memory override.** Moot until a night is launched; it costs nothing to leave.
5. **Blind v2 registration.** Deferred, not cancelled. Each day of waiting lengthens the
   exclusion list, which is the cost ADR-003 accepted.
6. **The remaining unarchived scratchpad material** — archive it beside the raw artefacts, or
   discard it. Mike's call, by hand.

## 5. If you are the blind author

The rule is [ADR-003](../decisions/003-blind-authorship-after-the-numbers.md) and
[`2026-09-19-genome-track-handover.md`](2026-09-19-genome-track-handover.md) §6. Nothing here
loosens either of them. In order:

1. **Say that you are the blind author, before you open anything.**
2. **Regenerate the exclusion list first.** It is only as current as its last run, and this
   session added files to the tree. The command and the path of the values file are both in the
   docstring of [`tools/contamination_scan.py`](../../tools/contamination_scan.py) — a path is
   not a value, which is why it may be written down there. Pass this file to `--required`
   alongside the two documents already listed, so the list can never forbid its own required
   reading. The holder of the values file is CC.
3. **Read the regenerated
   [`docs/blind-author-exclusions.txt`](../blind-author-exclusions.txt), not this paragraph**, for
   what is off limits. It is generated; paths only; safe to read.
4. **The exclusions that no scan of tracked files can ever produce** are named by hand in the
   2026-09-19 handover §6 and in the scanner itself: `atlas.html` and `tools/atlas/`, which are
   ignored by git and are the densest view of every result in one page; the repository history
   for 2026-09-18, 2026-09-19 and **2026-09-20** (`git log` and `git show` — today's commit
   messages carry findings); the group thread from 2026-09-18 onward; and the result directories
   created today, which the scanner now names outright because a directory new today is covered by
   no earlier list.
5. **The sanitised skeleton you are owed** — v1's section structure with every value removed, its
   gate being that no decimal point survives — is described in the 2026-09-19 handover §6 and is
   not restated here. Its honest limit is also there: integers are not caught by that gate, so a
   short hand-written whitelist separates structure from outcome.
6. **One correction the older handover has not absorbed.** Its §3 says the cell-type biases are
   the whole of individuality. They are not: one `--seed` is also spent on the global random
   number generators, so two individuals differ in decoder initialisation and in data order as
   well. The correction is read from source in
   [`../notes/2026-09-20-what-is-the-genome-here.md`](../notes/2026-09-20-what-is-the-genome-here.md)
   §3, and the sentence itself is still unedited — it is a board entry, not a repair. Neither
   statement carries a value.

## 6. Reading order

**Everyone, first:**

1. [`idea_en.md`](../../idea_en.md) — the goal, verbatim in English, and the two annotations it
   carries about itself. (`idea.md` is the record.)
2. [`README.md`](../../README.md) § "State at 2026-09-20" and § "The goal, in the owner's own
   words".
3. [`../retrospectives/2026-09-20-session-close.md`](../retrospectives/2026-09-20-session-close.md)
   — what happened, what was decided and by whom, what was not done, and the errors.
4. This file, §§2–4.
5. [`ROADMAP.md`](../../ROADMAP.md) — track states, and the generated status block at the bottom,
   which is the only status in that file not typed by hand.
6. [`docs/CHECKLIST-research-repo.md`](../CHECKLIST-research-repo.md) and
   `docs/BACKLOG_FORMAT.md` (in `dpc-messenger`) — how this repository expects records to be
   written.

**Then, by job.** The grammar track:
[`2026-09-19-genome-track-handover.md`](2026-09-19-genome-track-handover.md) §§1–5,
[`../plans/2026-09-16-functional-readout-plan.md`](../plans/2026-09-16-functional-readout-plan.md)
§ "Step 3 — genome", the S2 design and its step-0 check, then `literature.md` §I.1 before
proposing any rule. The measurement track: `backlog.md`, then the reading files named in §2.
The blind job: §5 above, and nothing else until the list is regenerated.

## 7. Two habits this session paid for

- **Open the file.** Five times in one day a paraphrase was passed on instead of the source, and
  each was caught by somebody opening the file — including the project's own goal, which sat in
  the repository root while it was being reconstructed from chat. A paraphrase that survives one
  hop is indistinguishable from a reading.
- **A correspondence is written down, never derived from a name.** Run→column, run→file,
  run→session: a table beside the artefact. The board carries this as its own entry, with three
  instances and two of them wrong.
