# Row B — the activity profiles: does row B tell individuals apart, and where does `3‴` lie

> **OFF LIMITS TO A BLIND v2 AUTHOR.** This file contains result values. Under
> `docs/decisions/003-blind-authorship-after-the-numbers.md` (ADR-003), anyone who must author a
> criterion that has not yet been written must not read this file, and must not read
> `results/night5/diagnostics/rowB/profiles_reading_distances.csv`,
> `results/night5/diagnostics/rowB/profiles_twin_vs_foreign.svg` / `.png`,
> `results/night5/diagnostics/rowB/rowB_records_det.json`,
> `results/night5/diagnostics/rowB/rowB_profiles_*_det.csv`,
> `results/night5/diagnostics/rowB/rowB_steps_*_det.h5`, nor the four files
> `PENALISED-QUANTITY-READING.md` already places off limits. The protocol
> (`results/night5/diagnostics/rowB/README.md`) and the script (`rowB.py`) stay readable: they
> hold no values.

**Status:** unregistered diagnostic. `status: "unregistered_diagnostic"`,
`readable_as_verdict: false`. **No number in this file reads as a test.**

**Authorised by Mike, 2026-09-20 09:27 UTC, DPC Research group chat.** This is the first
authorised reading of the row B activity profiles by this repository.
`PENALISED-QUANTITY-READING.md` §7 item 7 records that no profile had been opened before today.

---

## 0. Declared before the profiles were opened

**Written and saved: 2026-09-20T09:30:25Z.** At the moment this section was saved, no value of
`rowB_profiles_*_det.csv`, no value inside `rowB_steps_*_det.h5`, and no matrix inside
`rowB_records_det.json` had been opened, printed or summarised by this reading. What had been
read is listed here so the claim is checkable: `README.md` (in full), `PENALISED-QUANTITY-READING.md`
(in full — it holds values, but of the **penalised quantity**, not of the profiles),
`run_notes.json`, `rowB_floor_det.json`, and the **file names** (not contents) in this
directory. Section 0 below is complete and is not edited after the profiles are opened; every
later section is an append.

### (a) The registered question, verbatim

> «does row B tell individuals apart; where on this axis does `3‴` lie after the boundary»
> (translated from Russian)

*Translated 2026-09-23 on Mike's word: until then this line stood in Ark's Russian, with the
English rendering "does row B tell individuals apart, and where does `3‴` lie on this axis after
the boundary" beside it as a translation, not a second original. The Russian original is in git
history at commit 2488ecb72d14aa5398149d9a727b58852873a091. See the note under §0z about the seal.*

Wording is Ark's, DPC Research group chat 2026-09-20 21:43 local, recorded in `README.md` §8
under "The question the profiles will be read for". It is quoted here from the repository, not
re-derived.

### (b) The instrument

**The record is the DETERMINISTIC full run.** Files with the `_det` suffix:
`rowB_records_det.json` (720 records = 10 runs × 72 checkpoints), `rowB_profiles_*_det.csv`
(720 files), `rowB_steps_*_det.h5` (10 files), with `rowB_axis_det.json` as the type axis and
`rowB_floor_det.json` as the floor.

Why this one and not the other: per `README.md` §16 ("Which run is the record"), Ark's rule is
that **if the deterministic full run completes cleanly it becomes the official record**,
because it recomputes to the bit; §16 records that it did complete cleanly (P0 720/720, P1′
720/720 as registered, no operator refused determinism, no exit-4 finding). Its mode is
`torch.use_deterministic_algorithms(True)`, `cudnn.deterministic = True`,
`cudnn.benchmark = False`, `reduction_path: "gpu"` (`README.md` §9, amendment A4).

**The floor in this mode is exactly zero.** `rowB_floor_det.json` records
`max_sigma_by_type = 0.0` and `max_abs_pairwise_difference = 0.0` for **both**
`mean_by_type` and `central_cell_mean_skip_first_quarter`, across three fresh processes on
the pair (`9992/003`, checkpoint 71), at `floor_k_inside_each_process = 5`. The **P2′
thresholds** that `rowB_floor_det.json` carries are therefore all `0.0` (rule: 10 × the
measured floor, §6b), on `reduction_path: "gpu"`, `deterministic: true` — the mode is part of
the threshold and this reading does not carry these numbers into the other mode.

**The trap this forecloses, restated from `README.md` §6 before any distance is read:** a floor
of exactly zero makes "the margin exceeds the floor" trivially satisfiable, and reading a zero
deterministic floor as "any nonzero difference is therefore huge" is a mistake about the floor,
not a finding about the individuals. **This reading does not use the floor to declare any
distance significant.** The floor's only role here is negative: it says that a nonzero distance
between two runs is not an artefact of the evaluator re-running.

**The normal-mode run is NOT pooled.** `rowB_records.json` and `rowB_profiles_*.csv` (no
suffix) are the `--no-determinism` instrument. `README.md` §9 and §16 forbid mixing the two in
one table, and nothing below does. They are used for **exactly one cross-check**, reported in
§1 as *instrument agreement* and never as a data point: the **maximum absolute difference per
profile between the deterministic and the normal-mode value of the same (run, checkpoint,
type)**, to see whether it is of the order of **1e-6** that Ark measured in his own sandbox on
2026-09-20 (`README.md` §8, honest note) against a between-run range of tens. If it is not of
that order, that is a statement about the instrument and is reported as such.

**Not used at all in this reading:** the superseded CPU-path outputs in
`superseded_cpu_path_first_run/`, the three-checkpoint scope in `three_checkpoint_gpu_path/`,
and the pre-sigma-guard floor summaries in `floor_summaries_before_sigma_guard/`
(`README.md` §10, §15 A7).

### (c) The quantities — two, reported separately, never merged

| | field | what it is |
|---|---|---|
| **primary** | `mean_by_type`, aggregated over the 16 held-out items → a **65-vector per run per checkpoint** | all nodes of each type, all frames — row A's population (`README.md` §3) |
| **secondary** | `central_cell_mean_skip_first_quarter`, same aggregation → a **65-vector per run per checkpoint** | the **penalty's own reduction**, exactly (`flyvis/solver.py:869-872`) |

**Both are reported at every checkpoint, in every table, in both distance forms. They are never
averaged together, never combined into a single score, and no conclusion is carried from one to
the other.** They are two instruments under one name (`README.md` §3) and have different
scales; a distance on one is not a distance on the other.

The other four matrices (`std_by_type`, `last_frame_by_type`, `central_cell_mean`,
`mean_by_type_skip_first_quarter`) are **not** read in this reading. The per-step `.h5`
tensors are **not** read either: the question of (a) is asked at the checkpoint level.

### (d) The statistic, fixed now

For a given checkpoint and a given quantity, each run has one 65-vector (types in
`rowB_axis_det.json`'s `type_labels` order, which `README.md` §4 asserts equal to row A's axis).
For each **pair of runs** the distance between their 65-vectors is stated in **two pre-declared
forms**, both reported always, neither preferred:

1. **Euclidean distance** on the raw 65-vectors — `sqrt(sum_t (a_t − b_t)^2)`. Scale-bearing:
   it answers "how far apart are these two activity profiles in their own units".
2. **`1 − Spearman ρ`** across the 65 types — ρ computed with the `spearman`/`rankdata` of
   `results/night2/diagnostics/ablation/ablation.py`, reused verbatim as `README.md` §9's reuse
   table requires. Scale-free: it answers "do these two runs rank the 65 types the same way".
   This is the measure `README.md` §7 names for the twin trap. **Pearson is context only and is
   not computed as a measure here** (§7: the two have already disagreed on this substrate, and
   choosing between them after a result is choosing by outcome).

**If the two forms disagree, the disagreement is the result** and is reported as MIXED under
(h). Neither is promoted to tie-breaker after the fact.

**Pair vocabulary, fixed now** (run identity from `rowB_records_det.json`'s `N` block and
`results/night5/run_columns.csv`, keyed by netdir, per `README.md` §7):

* six individuals: seed 0 (`9991/000`, `9991/900`, `9992/000`), seed 3 (`9991/003`,
  `9991/903`, `9992/003`), seed 1 (`9991/001`), seed 2 (`9991/002`), seed 4 (`9991/004`),
  seed 5 (`9991/005`);
* **twin pairs** = pairs of runs of the **same** individual. Seed 0 has three runs → **3 pairs**;
  seed 3 has three runs → **3 pairs**. **6 twin pairs in total**, and all of them belong to two
  individuals — see (g);
* **foreign pairs** = all pairs of runs from **different** individuals. Ten runs give 45 pairs
  in all, of which 6 are twin, so **39 foreign pairs**.

**The twin trap, as `README.md` §7 states it and as this reading applies it.** A twin distance
is **not** compared against a fixed foreign pair. For each twin pair `(x, y)` the comparison is
against the **NEAREST foreign pair involving either `x` or `y`** — i.e. the **minimum** over all
foreign pairs that contain `x` or contain `y`. This is Ark's correction of 2026-09-15 08:13 and
it makes the trap strictly harder than the rule it replaced. The reported statistic is

```
nearest_foreign(x,y) = min over foreign pairs p containing x or y  of  d(p)
ratio(x,y)           = nearest_foreign(x,y) / d(x,y)
```

so **ratio > 1 means the twin pair is closer to itself than either of its runs is to any
foreign run** — the direction the question asks about. Ratio, `d(twin)` and
`nearest_foreign` are all tabulated; the ratio never replaces the two numbers it is built
from.

### (e) The handling of run 9992/003 (seed 3‴) — declared now, before the profiles are opened

`README.md` §8 and `run_notes.json`'s `outlier_flag` both require that whoever opens the
profiles must not silently pool `9992/003` with its replicates as "a twin like the others", and
must not silently drop it either, and that **both choices be stated before the profiles are
opened**. The choice, stated here:

**EVERY table in this reading is given twice — once WITH `9992/003` and once WITHOUT it.** It
is neither pooled nor dropped: both readings are carried side by side to the end.

* **With 3‴:** all ten runs, 45 pairs, 6 twin pairs (seed 0: 3, seed 3: 3), 39 foreign.
* **Without 3‴:** nine runs, 36 pairs, **4** twin pairs (seed 0: 3, seed 3: 1 — the pair
  `9991/003`–`9991/903`), 32 foreign. Dropping the run removes the two twin pairs that contain
  it and every foreign pair that contains it.

**No conclusion is stated in this file that holds under only one of the two unless it is
explicitly labelled as holding only under that one.** A sentence with no such label holds under
both.

The reason this is not a free choice: `9992/003` is an outlier on the **central-cell activity
axis** (`PENALISED-QUANTITY-READING.md` §3a, §6) but **not** on held-out loss, where it is the
calmest of its three replicates. Pooling it silently would let one run's excursion decide the
answer; dropping it silently would hide the one run the question of (a) names.

### (f) The checkpoints to tabulate, fixed now

All ten runs share one `chkpt_iter` grid (`PENALISED-QUANTITY-READING.md` §2a, checked there as
an identical tuple for all ten). The tabulated checkpoints:

| `chkpt_index` | `chkpt_iter` | why this one |
|---|---|---|
| **0** | −1 | before training — the initialisation, the state the question's "does row B tell individuals apart" must be **false** at if the axis is measuring anything learned |
| **8** | 25,211 | ~25k, where the cheap probe sits |
| **42** | 147,611 | the **last** checkpoint before `stop_iter = 150,000` |
| **43** | 151,211 | the **first** checkpoint at or after `stop_iter = 150,000` |
| **71** | 250,007 | the end state |

The boundary pair (42, 43) is the sharpest the grid allows: spacing there is **3,600
iterations**, so `stop_iter` sits 2,389 iterations after 42 and 1,211 before 43, and anything
inside that window appears as exactly one difference (`PENALISED-QUANTITY-READING.md` §2a, §7
item 5). **This reading inherits that resolution limit and does not claim finer.**

**Plus the full trajectory** of the twin / nearest-foreign distances and of the ratio, over
**all 72 checkpoints**, as a figure (§3), with vertical lines at **25,000** and **150,000**.

### (g) N, and what this preview is not

**N = 6 individuals.** Ten runs; the four replicate runs **do not enter N**, because a
replicate is the same individual measured again — that is what makes it a floor rather than a
data point (`README.md` §7, §14; the `N` block of the records).

`docs/next-session-plan.md` §5 sets the floor for reading row B as a test at all: *"Do not read
row B as a test at N < 8."* Six is below it. `README.md` §14: *"Six is more individuals, not a
test."*

**And the sharper limit, stated before the numbers:** all **6 twin pairs live on just 2 of the
6 individuals** (seeds 0 and 3). Four of the six individuals contribute **no** twin pair at
all. Whatever the twin-versus-foreign comparison shows, it is a statement about **two**
individuals' replicate structure, generalised to nothing. Under the (e) "without 3‴" reading
it is **4** twin pairs on the same 2 individuals.

Accordingly, and fixed before any value is read:

* `readable_as_verdict: false`;
* **no p-values**, no significance language, no "significant", no confidence intervals, no
  hypothesis-test vocabulary anywhere in this file;
* no number here is an outcome of hypothesis (b)/(b2) of
  `docs/preregistration-cheap-vs-expensive.md`, nor a rung, nor an outcome of anything
  registered — today or later;
* **no threshold is invented after the fact** to resolve a case the rule of (h) leaves open.

### (h) What would count as which answer — stated before looking

Evaluated **at the end checkpoint (index 71)**, which is the state the question is about:

* **"ROW B TELLS INDIVIDUALS APART"** — **every** twin distance is smaller than its **nearest
  foreign** distance (i.e. `ratio > 1` for every twin pair), in **both** distance forms
  (Euclidean and `1 − ρ`), **both** with 3‴ and without it, and on the primary quantity
  `mean_by_type`. The secondary quantity is reported alongside and its agreement or
  disagreement is stated, but the answer under this clause is taken on the primary, as
  `README.md` §3 and the design document's Addendum point 3 make `mean_by_type` primary.
* **"IT DOES NOT"** — twin distances are comparable to, or larger than, their nearest-foreign
  distances in **most** twin pairs.
* **ANYTHING ELSE is reported as MIXED**, with the failing pairs **listed by name**, the
  quantity and distance form named for each, and **no threshold invented** to resolve it into
  one of the other two answers. A disagreement between the two distance forms, between the two
  quantities, or between the with-3‴ and without-3‴ readings is itself MIXED and is reported
  as such rather than adjudicated.

The `3‴` half of the question of (a) is **descriptive** and has no pass/fail clause: §4 reports
where `9992/003` sits — its distance to its two replicates against its distance to the other
individuals over the **last 30 checkpoints** — and **which cell types carry its excursion**, as
the top types by contribution to the squared distance, **named**, and classified only as
*input types (R1–R8)* / *T4–T5* / *other*, **with no biological interpretation beyond the
names**.

### What this reading does NOT do

* It does **not** perform the same question on the **weights**. That is the natural next
  comparison (Ark's 2026-09-15 weight-space measurement) and it is noted in §5 and not
  performed here.
* It does **not** re-measure anything. It opens files already on disk.
* It does **not** edit any file already written. `README.md`'s PENDING paragraph is updated to
  record the authorisation and this file's name, and nothing else.

### 0z. The seal

Section 0 above was written and saved **complete**, to
`results/night5/diagnostics/rowB/PROFILES-READING.md`, at **2026-09-20T09:30:25Z**, and its
sha256 **as saved at that moment — before any profile value was opened** — was taken at
**2026-09-20T09:31:44Z**:

```
a4d10e67f6eafa922f555625569ac5ca11db2de8bb27a01e597acbc0a945583d
```

**Note, 2026-09-23 (translation).** §0(a) above was translated into English on Mike's word, so
this digest cannot reproduce from this revision. It also **does not reproduce from any committed
revision**: the file has one commit before the translation, 9e101a5 (2026-09-20 17:03 +0700), and
at 2488ecb72d14aa5398149d9a727b58852873a091 (the last revision with the Russian line) the digest
was checked on 2026-09-23 against every prefix of the file ending at or just before the
`### 0z` heading, in LF and in CRLF, with zero, one or two trailing newlines, with and without the
`OFF LIMITS` header block and the English-rendering paragraph, and against §0 alone — no
variant gives `a4d10e67…`. The saved-at-09:30:25Z bytes it was taken over were never committed,
so the order "declaration, then values" rests on this file's own statement and on the commit
time, not on a digest anyone can recompute. Details:
[docs/notes/2026-09-23-translated-pinned-files.md](../../../../docs/notes/2026-09-23-translated-pinned-files.md).

That digest covers the file **up to and including the line above this subsection**; this
subsection and everything below it were appended afterwards, which is why the digest of the
finished file differs from it. The digest is recorded so that the order — declaration, then
values — is checkable and not merely asserted. Sections 1–8 below are appends. **Section 0 is
not edited by them.**

Everything below this line was written **after** the profiles were opened.

---

## 1. Instrument cross-check — the two modes agree

Declared in §0(b): the deterministic run is the record; the normal-mode run is used for **one**
cross-check and is not pooled. The cross-check is the maximum absolute difference, per profile,
between the deterministic and the normal-mode value of the same (run, checkpoint, cell type),
over all 720 profiles of each quantity.

### Instrument agreement, per profile

| quantity | max &#124;det &minus; normal&#124; over the 720 profiles | where | median over the 720 |
|---|---|---|---|
| `mean_by_type` | **3.206e-06** | 1, chkpt 5 | 8.245e-08 |
| `central_cell_mean_skip_first_quarter` | **1.043e-05** | 0", chkpt 6 | 4.003e-07 |

Scale to read those against: at the end checkpoint the **between-run** spread of `mean_by_type`, per type, reaches **59.47**; the largest single value in any profile is **340.91**.

**Read as instrument agreement, not as a result.** For the primary quantity the worst
disagreement anywhere in 720 profiles is **3.2e-6**, and the typical one is **8.2e-8** — the
order of **1e-6** that Ark's sandbox comparison sized on 2026-09-20 (`README.md` §8, honest
note). Ark's figure is confirmed for `mean_by_type`.

**One honest correction to that figure.** For the **secondary** quantity — the penalty's own
reduction — the worst disagreement is **1.0e-5**, one order of magnitude larger than 1e-6.
That is expected of a single-cell reduction (one central cell per type, not an average over
hundreds of nodes, so nothing averages the last-bit differences away), and it is still five to
six orders below the between-run spread. But "of order 1e-6" is a statement about
`mean_by_type`; for `central_cell_mean_skip_first_quarter` the honest figure is **of order
1e-5**.

Against either: at the end checkpoint the **between-run** spread of `mean_by_type` reaches
**59.47** on a single cell type. The mode difference is therefore between **6 and 7 orders of
magnitude** smaller than the quantity this reading is about. **No conclusion below could be
changed by having read the other mode's files instead.**

**The floor does no work here.** `rowB_floor_det.json` records the deterministic floor as
**exactly 0.0** for both quantities, so every distance below is nonzero-by-more-than-the-floor
trivially. As §0(b) declared in advance, this reading does not use that fact to call anything
large. Its only use is the negative one: a twin distance of 38 is not the evaluator wandering.

---

## 2. The tables

Each table is given **twice** — with `3‴` and without it — as §0(e) declared. `ratio` is
`nearest-foreign / twin`; **ratio > 1 means the twin pair is closer to itself than either of
its two runs is to any foreign run**. Run shorthand: `0`, `0'`, `0"` are the three runs of
individual 0 (`9991/000`, `9991/900`, `9992/000`); `3`, `3'`, `3‴` are the three runs of
individual 3 (`9991/003`, `9991/903`, `9992/003`); `1`, `2`, `4`, `5` are the single runs of
individuals 1, 2, 4 and 5.

#### WITH `3‴` &mdash; 10 runs, 6 twin pairs, 39 foreign pairs


**`mean_by_type` (primary) &mdash; Euclidean distance**

| chkpt | iter | twin pair | d(twin) | nearest foreign pair | d(nearest foreign) | ratio nf/twin | twin closer? |
|---|---|---|---|---|---|---|---|
| 0 | -1 | `0~0'` | **0** (exact) | `0~3` | 0.4893 | &infin; | **yes** |
| 0 | -1 | `0~0"` | **0** (exact) | `0~3` | 0.4893 | &infin; | **yes** |
| 0 | -1 | `0'~0"` | **0** (exact) | `0'~3` | 0.4893 | &infin; | **yes** |
| 0 | -1 | `3~3'` | **0** (exact) | `0~3` | 0.4893 | &infin; | **yes** |
| 0 | -1 | `3~3'''` | **0** (exact) | `0~3` | 0.4893 | &infin; | **yes** |
| 0 | -1 | `3'~3'''` | **0** (exact) | `0~3'` | 0.4893 | &infin; | **yes** |
| 8 | 25,211 | `0~0'` | 26.6382 | `0~2` | 46.7448 | 1.755 | **yes** |
| 8 | 25,211 | `0~0"` | 28.0356 | `0"~2` | 33.7957 | 1.205 | **yes** |
| 8 | 25,211 | `0'~0"` | 22.2154 | `0"~2` | 33.7957 | 1.521 | **yes** |
| 8 | 25,211 | `3~3'` | 82.8126 | `1~3'` | 55.0042 | 0.664 | no |
| 8 | 25,211 | `3~3'''` | 83.2918 | `1~3'''` | 60.3280 | 0.724 | no |
| 8 | 25,211 | `3'~3'''` | 39.7092 | `1~3'` | 55.0042 | 1.385 | **yes** |
| 42 | 147,611 | `0~0'` | 33.0214 | `0~2` | 32.8408 | 0.995 | no |
| 42 | 147,611 | `0~0"` | 52.8133 | `0~2` | 32.8408 | 0.622 | no |
| 42 | 147,611 | `0'~0"` | 41.9607 | `0'~3` | 32.9865 | 0.786 | no |
| 42 | 147,611 | `3~3'` | 16.3032 | `1~3'` | 14.7337 | 0.904 | no |
| 42 | 147,611 | `3~3'''` | 17.0170 | `1~3'''` | 13.5086 | 0.794 | no |
| 42 | 147,611 | `3'~3'''` | 7.8535 | `1~3'''` | 13.5086 | 1.720 | **yes** |
| 43 | 151,211 | `0~0'` | 33.0762 | `0'~3` | 32.7186 | 0.989 | no |
| 43 | 151,211 | `0~0"` | 54.7770 | `0~2` | 33.2771 | 0.608 | no |
| 43 | 151,211 | `0'~0"` | 45.2045 | `0'~3` | 32.7186 | 0.724 | no |
| 43 | 151,211 | `3~3'` | 17.5188 | `1~3'` | 13.7905 | 0.787 | no |
| 43 | 151,211 | `3~3'''` | 18.1574 | `1~3'''` | 13.0122 | 0.717 | no |
| 43 | 151,211 | `3'~3'''` | 8.3030 | `1~3'''` | 13.0122 | 1.567 | **yes** |
| 71 | 250,007 | `0~0'` | 59.2921 | `0'~3` | 41.7329 | 0.704 | no |
| 71 | 250,007 | `0~0"` | 77.9028 | `0~2` | 55.2474 | 0.709 | no |
| 71 | 250,007 | `0'~0"` | 57.1427 | `0'~3` | 41.7329 | 0.730 | no |
| 71 | 250,007 | `3~3'` | 14.7279 | `1~3'` | 18.0554 | 1.226 | **yes** |
| 71 | 250,007 | `3~3'''` | 50.6326 | `1~3` | 21.4374 | 0.423 | no |
| 71 | 250,007 | `3'~3'''` | 50.2313 | `1~3'` | 18.0554 | 0.359 | no |

**`mean_by_type` (primary) &mdash; 1 &minus; &rho; distance**

| chkpt | iter | twin pair | d(twin) | nearest foreign pair | d(nearest foreign) | ratio nf/twin | twin closer? |
|---|---|---|---|---|---|---|---|
| 0 | -1 | `0~0'` | **0** (exact) | `0~3` | 0.1192 | &infin; | **yes** |
| 0 | -1 | `0~0"` | **0** (exact) | `0~3` | 0.1192 | &infin; | **yes** |
| 0 | -1 | `0'~0"` | **0** (exact) | `0'~3` | 0.1192 | &infin; | **yes** |
| 0 | -1 | `3~3'` | **0** (exact) | `0~3` | 0.1192 | &infin; | **yes** |
| 0 | -1 | `3~3'''` | **0** (exact) | `0~3` | 0.1192 | &infin; | **yes** |
| 0 | -1 | `3'~3'''` | **0** (exact) | `0~3'` | 0.1192 | &infin; | **yes** |
| 8 | 25,211 | `0~0'` | 0.1246 | `0~3'''` | 0.2462 | 1.976 | **yes** |
| 8 | 25,211 | `0~0"` | 0.1783 | `0~3'''` | 0.2462 | 1.380 | **yes** |
| 8 | 25,211 | `0'~0"` | 0.0511 | `0"~3'''` | 0.2696 | 5.277 | **yes** |
| 8 | 25,211 | `3~3'` | 0.3579 | `1~3'` | 0.3298 | 0.921 | no |
| 8 | 25,211 | `3~3'''` | 0.2747 | `0~3'''` | 0.2462 | 0.896 | no |
| 8 | 25,211 | `3'~3'''` | 0.0907 | `0~3'''` | 0.2462 | 2.714 | **yes** |
| 42 | 147,611 | `0~0'` | 0.4346 | `0'~3'''` | 0.4490 | 1.033 | **yes** |
| 42 | 147,611 | `0~0"` | 0.4205 | `0"~3'''` | 0.4323 | 1.028 | **yes** |
| 42 | 147,611 | `0'~0"` | 0.1479 | `0"~3'''` | 0.4323 | 2.922 | **yes** |
| 42 | 147,611 | `3~3'` | 0.3848 | `1~3` | 0.3704 | 0.963 | no |
| 42 | 147,611 | `3~3'''` | 0.3530 | `1~3'''` | 0.3294 | 0.933 | no |
| 42 | 147,611 | `3'~3'''` | 0.2991 | `1~3'''` | 0.3294 | 1.101 | **yes** |
| 43 | 151,211 | `0~0'` | 0.4289 | `0'~3'''` | 0.4622 | 1.078 | **yes** |
| 43 | 151,211 | `0~0"` | 0.4135 | `0"~3'''` | 0.4554 | 1.101 | **yes** |
| 43 | 151,211 | `0'~0"` | 0.1394 | `0"~3'''` | 0.4554 | 3.266 | **yes** |
| 43 | 151,211 | `3~3'` | 0.3954 | `1~3` | 0.3764 | 0.952 | no |
| 43 | 151,211 | `3~3'''` | 0.3545 | `1~3'''` | 0.3261 | 0.920 | no |
| 43 | 151,211 | `3'~3'''` | 0.2969 | `1~3'''` | 0.3261 | 1.098 | **yes** |
| 71 | 250,007 | `0~0'` | 0.3487 | `0~3` | 0.4969 | 1.425 | **yes** |
| 71 | 250,007 | `0~0"` | 0.3550 | `0~3` | 0.4969 | 1.400 | **yes** |
| 71 | 250,007 | `0'~0"` | 0.2195 | `0"~3` | 0.5400 | 2.460 | **yes** |
| 71 | 250,007 | `3~3'` | 0.4042 | `1~3` | 0.4043 | 1.000 | **yes** |
| 71 | 250,007 | `3~3'''` | 0.3706 | `1~3` | 0.4043 | 1.091 | **yes** |
| 71 | 250,007 | `3'~3'''` | 0.4646 | `1~3'''` | 0.4081 | 0.878 | no |

**`central_cell_mean_skip_first_quarter` (secondary, the penalised reduction) &mdash; Euclidean distance**

| chkpt | iter | twin pair | d(twin) | nearest foreign pair | d(nearest foreign) | ratio nf/twin | twin closer? |
|---|---|---|---|---|---|---|---|
| 0 | -1 | `0~0'` | **0** (exact) | `0~3` | 0.4911 | &infin; | **yes** |
| 0 | -1 | `0~0"` | **0** (exact) | `0~3` | 0.4911 | &infin; | **yes** |
| 0 | -1 | `0'~0"` | **0** (exact) | `0'~3` | 0.4911 | &infin; | **yes** |
| 0 | -1 | `3~3'` | **0** (exact) | `0~3` | 0.4911 | &infin; | **yes** |
| 0 | -1 | `3~3'''` | **0** (exact) | `0~3` | 0.4911 | &infin; | **yes** |
| 0 | -1 | `3'~3'''` | **0** (exact) | `0~3'` | 0.4911 | &infin; | **yes** |
| 8 | 25,211 | `0~0'` | 31.0531 | `0~2` | 51.1944 | 1.649 | **yes** |
| 8 | 25,211 | `0~0"` | 32.1774 | `0"~2` | 41.7160 | 1.296 | **yes** |
| 8 | 25,211 | `0'~0"` | 24.6570 | `0"~2` | 41.7160 | 1.692 | **yes** |
| 8 | 25,211 | `3~3'` | 100.2344 | `1~3'` | 70.2523 | 0.701 | no |
| 8 | 25,211 | `3~3'''` | 102.7666 | `1~3` | 76.1243 | 0.741 | no |
| 8 | 25,211 | `3'~3'''` | 54.8441 | `1~3'` | 70.2523 | 1.281 | **yes** |
| 42 | 147,611 | `0~0'` | 38.4961 | `0~2` | 35.7006 | 0.927 | no |
| 42 | 147,611 | `0~0"` | 59.6995 | `0~2` | 35.7006 | 0.598 | no |
| 42 | 147,611 | `0'~0"` | 43.5442 | `0'~3` | 41.2863 | 0.948 | no |
| 42 | 147,611 | `3~3'` | 18.3855 | `1~3'` | 16.0007 | 0.870 | no |
| 42 | 147,611 | `3~3'''` | 19.1862 | `1~3'''` | 15.1354 | 0.789 | no |
| 42 | 147,611 | `3'~3'''` | 9.0301 | `1~3'''` | 15.1354 | 1.676 | **yes** |
| 43 | 151,211 | `0~0'` | 38.4761 | `0~2` | 36.1759 | 0.940 | no |
| 43 | 151,211 | `0~0"` | 61.9203 | `0~2` | 36.1759 | 0.584 | no |
| 43 | 151,211 | `0'~0"` | 46.9259 | `0'~3` | 41.0781 | 0.875 | no |
| 43 | 151,211 | `3~3'` | 19.7301 | `1~3'` | 15.2619 | 0.774 | no |
| 43 | 151,211 | `3~3'''` | 20.5937 | `1~3'''` | 15.0398 | 0.730 | no |
| 43 | 151,211 | `3'~3'''` | 9.8804 | `1~3'''` | 15.0398 | 1.522 | **yes** |
| 71 | 250,007 | `0~0'` | 66.7593 | `0'~3` | 50.3675 | 0.754 | no |
| 71 | 250,007 | `0~0"` | 87.8366 | `0~2` | 60.4624 | 0.688 | no |
| 71 | 250,007 | `0'~0"` | 61.6559 | `0'~3` | 50.3675 | 0.817 | no |
| 71 | 250,007 | `3~3'` | 16.5797 | `1~3'` | 19.8104 | 1.195 | **yes** |
| 71 | 250,007 | `3~3'''` | 56.1743 | `1~3` | 23.2855 | 0.415 | no |
| 71 | 250,007 | `3'~3'''` | 55.2493 | `1~3'` | 19.8104 | 0.359 | no |

**`central_cell_mean_skip_first_quarter` (secondary, the penalised reduction) &mdash; 1 &minus; &rho; distance**

| chkpt | iter | twin pair | d(twin) | nearest foreign pair | d(nearest foreign) | ratio nf/twin | twin closer? |
|---|---|---|---|---|---|---|---|
| 0 | -1 | `0~0'` | **0** (exact) | `0~3` | 0.1086 | &infin; | **yes** |
| 0 | -1 | `0~0"` | **0** (exact) | `0~3` | 0.1086 | &infin; | **yes** |
| 0 | -1 | `0'~0"` | **0** (exact) | `0'~3` | 0.1086 | &infin; | **yes** |
| 0 | -1 | `3~3'` | **0** (exact) | `0~3` | 0.1086 | &infin; | **yes** |
| 0 | -1 | `3~3'''` | **0** (exact) | `0~3` | 0.1086 | &infin; | **yes** |
| 0 | -1 | `3'~3'''` | **0** (exact) | `0~3'` | 0.1086 | &infin; | **yes** |
| 8 | 25,211 | `0~0'` | 0.1218 | `0~3'''` | 0.2566 | 2.107 | **yes** |
| 8 | 25,211 | `0~0"` | 0.1638 | `0~3'''` | 0.2566 | 1.567 | **yes** |
| 8 | 25,211 | `0'~0"` | 0.0543 | `0"~3'''` | 0.3069 | 5.653 | **yes** |
| 8 | 25,211 | `3~3'` | 0.3708 | `1~3'` | 0.3359 | 0.906 | no |
| 8 | 25,211 | `3~3'''` | 0.2823 | `0~3'''` | 0.2566 | 0.909 | no |
| 8 | 25,211 | `3'~3'''` | 0.0957 | `0~3'''` | 0.2566 | 2.681 | **yes** |
| 42 | 147,611 | `0~0'` | 0.4457 | `0'~3'''` | 0.4755 | 1.067 | **yes** |
| 42 | 147,611 | `0~0"` | 0.4235 | `0"~3'''` | 0.4585 | 1.083 | **yes** |
| 42 | 147,611 | `0'~0"` | 0.1408 | `0"~3'''` | 0.4585 | 3.256 | **yes** |
| 42 | 147,611 | `3~3'` | 0.4180 | `1~3` | 0.4088 | 0.978 | no |
| 42 | 147,611 | `3~3'''` | 0.3951 | `1~3'''` | 0.3212 | 0.813 | no |
| 42 | 147,611 | `3'~3'''` | 0.2903 | `1~3'''` | 0.3212 | 1.106 | **yes** |
| 43 | 151,211 | `0~0'` | 0.4323 | `0~2` | 0.4722 | 1.092 | **yes** |
| 43 | 151,211 | `0~0"` | 0.4170 | `0~2` | 0.4722 | 1.132 | **yes** |
| 43 | 151,211 | `0'~0"` | 0.1306 | `0"~3'''` | 0.4889 | 3.745 | **yes** |
| 43 | 151,211 | `3~3'` | 0.4170 | `1~3` | 0.4167 | 0.999 | no |
| 43 | 151,211 | `3~3'''` | 0.4198 | `1~3'''` | 0.3315 | 0.790 | no |
| 43 | 151,211 | `3'~3'''` | 0.2917 | `1~3'''` | 0.3315 | 1.137 | **yes** |
| 71 | 250,007 | `0~0'` | 0.3570 | `0~2` | 0.4966 | 1.391 | **yes** |
| 71 | 250,007 | `0~0"` | 0.3562 | `0~2` | 0.4966 | 1.394 | **yes** |
| 71 | 250,007 | `0'~0"` | 0.1873 | `0'~3'` | 0.5687 | 3.036 | **yes** |
| 71 | 250,007 | `3~3'` | 0.4292 | `1~3'` | 0.4369 | 1.018 | **yes** |
| 71 | 250,007 | `3~3'''` | 0.4121 | `1~3'''` | 0.4010 | 0.973 | no |
| 71 | 250,007 | `3'~3'''` | 0.4172 | `1~3'''` | 0.4010 | 0.961 | no |

#### WITHOUT `3‴` &mdash; 9 runs, 4 twin pairs, 32 foreign pairs


**`mean_by_type` (primary) &mdash; Euclidean distance**

| chkpt | iter | twin pair | d(twin) | nearest foreign pair | d(nearest foreign) | ratio nf/twin | twin closer? |
|---|---|---|---|---|---|---|---|
| 0 | -1 | `0~0'` | **0** (exact) | `0~3` | 0.4893 | &infin; | **yes** |
| 0 | -1 | `0~0"` | **0** (exact) | `0~3` | 0.4893 | &infin; | **yes** |
| 0 | -1 | `0'~0"` | **0** (exact) | `0'~3` | 0.4893 | &infin; | **yes** |
| 0 | -1 | `3~3'` | **0** (exact) | `0~3` | 0.4893 | &infin; | **yes** |
| 8 | 25,211 | `0~0'` | 26.6382 | `0~2` | 46.7448 | 1.755 | **yes** |
| 8 | 25,211 | `0~0"` | 28.0356 | `0"~2` | 33.7957 | 1.205 | **yes** |
| 8 | 25,211 | `0'~0"` | 22.2154 | `0"~2` | 33.7957 | 1.521 | **yes** |
| 8 | 25,211 | `3~3'` | 82.8126 | `1~3'` | 55.0042 | 0.664 | no |
| 42 | 147,611 | `0~0'` | 33.0214 | `0~2` | 32.8408 | 0.995 | no |
| 42 | 147,611 | `0~0"` | 52.8133 | `0~2` | 32.8408 | 0.622 | no |
| 42 | 147,611 | `0'~0"` | 41.9607 | `0'~3` | 32.9865 | 0.786 | no |
| 42 | 147,611 | `3~3'` | 16.3032 | `1~3'` | 14.7337 | 0.904 | no |
| 43 | 151,211 | `0~0'` | 33.0762 | `0'~3` | 32.7186 | 0.989 | no |
| 43 | 151,211 | `0~0"` | 54.7770 | `0~2` | 33.2771 | 0.608 | no |
| 43 | 151,211 | `0'~0"` | 45.2045 | `0'~3` | 32.7186 | 0.724 | no |
| 43 | 151,211 | `3~3'` | 17.5188 | `1~3'` | 13.7905 | 0.787 | no |
| 71 | 250,007 | `0~0'` | 59.2921 | `0'~3` | 41.7329 | 0.704 | no |
| 71 | 250,007 | `0~0"` | 77.9028 | `0~2` | 55.2474 | 0.709 | no |
| 71 | 250,007 | `0'~0"` | 57.1427 | `0'~3` | 41.7329 | 0.730 | no |
| 71 | 250,007 | `3~3'` | 14.7279 | `1~3'` | 18.0554 | 1.226 | **yes** |

**`mean_by_type` (primary) &mdash; 1 &minus; &rho; distance**

| chkpt | iter | twin pair | d(twin) | nearest foreign pair | d(nearest foreign) | ratio nf/twin | twin closer? |
|---|---|---|---|---|---|---|---|
| 0 | -1 | `0~0'` | **0** (exact) | `0~3` | 0.1192 | &infin; | **yes** |
| 0 | -1 | `0~0"` | **0** (exact) | `0~3` | 0.1192 | &infin; | **yes** |
| 0 | -1 | `0'~0"` | **0** (exact) | `0'~3` | 0.1192 | &infin; | **yes** |
| 0 | -1 | `3~3'` | **0** (exact) | `0~3` | 0.1192 | &infin; | **yes** |
| 8 | 25,211 | `0~0'` | 0.1246 | `0~3'` | 0.3432 | 2.755 | **yes** |
| 8 | 25,211 | `0~0"` | 0.1783 | `0~3'` | 0.3432 | 1.925 | **yes** |
| 8 | 25,211 | `0'~0"` | 0.0511 | `0"~3'` | 0.3582 | 7.010 | **yes** |
| 8 | 25,211 | `3~3'` | 0.3579 | `1~3'` | 0.3298 | 0.921 | no |
| 42 | 147,611 | `0~0'` | 0.4346 | `0~2` | 0.5114 | 1.177 | **yes** |
| 42 | 147,611 | `0~0"` | 0.4205 | `0~2` | 0.5114 | 1.216 | **yes** |
| 42 | 147,611 | `0'~0"` | 0.1479 | `0'~3'` | 0.5531 | 3.739 | **yes** |
| 42 | 147,611 | `3~3'` | 0.3848 | `1~3` | 0.3704 | 0.963 | no |
| 43 | 151,211 | `0~0'` | 0.4289 | `0~2` | 0.5185 | 1.209 | **yes** |
| 43 | 151,211 | `0~0"` | 0.4135 | `0~2` | 0.5185 | 1.254 | **yes** |
| 43 | 151,211 | `0'~0"` | 0.1394 | `0'~3'` | 0.5495 | 3.941 | **yes** |
| 43 | 151,211 | `3~3'` | 0.3954 | `1~3` | 0.3764 | 0.952 | no |
| 71 | 250,007 | `0~0'` | 0.3487 | `0~3` | 0.4969 | 1.425 | **yes** |
| 71 | 250,007 | `0~0"` | 0.3550 | `0~3` | 0.4969 | 1.400 | **yes** |
| 71 | 250,007 | `0'~0"` | 0.2195 | `0"~3` | 0.5400 | 2.460 | **yes** |
| 71 | 250,007 | `3~3'` | 0.4042 | `1~3` | 0.4043 | 1.000 | **yes** |

**`central_cell_mean_skip_first_quarter` (secondary, the penalised reduction) &mdash; Euclidean distance**

| chkpt | iter | twin pair | d(twin) | nearest foreign pair | d(nearest foreign) | ratio nf/twin | twin closer? |
|---|---|---|---|---|---|---|---|
| 0 | -1 | `0~0'` | **0** (exact) | `0~3` | 0.4911 | &infin; | **yes** |
| 0 | -1 | `0~0"` | **0** (exact) | `0~3` | 0.4911 | &infin; | **yes** |
| 0 | -1 | `0'~0"` | **0** (exact) | `0'~3` | 0.4911 | &infin; | **yes** |
| 0 | -1 | `3~3'` | **0** (exact) | `0~3` | 0.4911 | &infin; | **yes** |
| 8 | 25,211 | `0~0'` | 31.0531 | `0~2` | 51.1944 | 1.649 | **yes** |
| 8 | 25,211 | `0~0"` | 32.1774 | `0"~2` | 41.7160 | 1.296 | **yes** |
| 8 | 25,211 | `0'~0"` | 24.6570 | `0"~2` | 41.7160 | 1.692 | **yes** |
| 8 | 25,211 | `3~3'` | 100.2344 | `1~3'` | 70.2523 | 0.701 | no |
| 42 | 147,611 | `0~0'` | 38.4961 | `0~2` | 35.7006 | 0.927 | no |
| 42 | 147,611 | `0~0"` | 59.6995 | `0~2` | 35.7006 | 0.598 | no |
| 42 | 147,611 | `0'~0"` | 43.5442 | `0'~3` | 41.2863 | 0.948 | no |
| 42 | 147,611 | `3~3'` | 18.3855 | `1~3'` | 16.0007 | 0.870 | no |
| 43 | 151,211 | `0~0'` | 38.4761 | `0~2` | 36.1759 | 0.940 | no |
| 43 | 151,211 | `0~0"` | 61.9203 | `0~2` | 36.1759 | 0.584 | no |
| 43 | 151,211 | `0'~0"` | 46.9259 | `0'~3` | 41.0781 | 0.875 | no |
| 43 | 151,211 | `3~3'` | 19.7301 | `1~3'` | 15.2619 | 0.774 | no |
| 71 | 250,007 | `0~0'` | 66.7593 | `0'~3` | 50.3675 | 0.754 | no |
| 71 | 250,007 | `0~0"` | 87.8366 | `0~2` | 60.4624 | 0.688 | no |
| 71 | 250,007 | `0'~0"` | 61.6559 | `0'~3` | 50.3675 | 0.817 | no |
| 71 | 250,007 | `3~3'` | 16.5797 | `1~3'` | 19.8104 | 1.195 | **yes** |

**`central_cell_mean_skip_first_quarter` (secondary, the penalised reduction) &mdash; 1 &minus; &rho; distance**

| chkpt | iter | twin pair | d(twin) | nearest foreign pair | d(nearest foreign) | ratio nf/twin | twin closer? |
|---|---|---|---|---|---|---|---|
| 0 | -1 | `0~0'` | **0** (exact) | `0~3` | 0.1086 | &infin; | **yes** |
| 0 | -1 | `0~0"` | **0** (exact) | `0~3` | 0.1086 | &infin; | **yes** |
| 0 | -1 | `0'~0"` | **0** (exact) | `0'~3` | 0.1086 | &infin; | **yes** |
| 0 | -1 | `3~3'` | **0** (exact) | `0~3` | 0.1086 | &infin; | **yes** |
| 8 | 25,211 | `0~0'` | 0.1218 | `0~3'` | 0.3576 | 2.937 | **yes** |
| 8 | 25,211 | `0~0"` | 0.1638 | `0~3'` | 0.3576 | 2.184 | **yes** |
| 8 | 25,211 | `0'~0"` | 0.0543 | `0'~3'` | 0.3884 | 7.155 | **yes** |
| 8 | 25,211 | `3~3'` | 0.3708 | `1~3'` | 0.3359 | 0.906 | no |
| 42 | 147,611 | `0~0'` | 0.4457 | `0~2` | 0.4780 | 1.073 | **yes** |
| 42 | 147,611 | `0~0"` | 0.4235 | `0~2` | 0.4780 | 1.129 | **yes** |
| 42 | 147,611 | `0'~0"` | 0.1408 | `0'~3'` | 0.5631 | 3.999 | **yes** |
| 42 | 147,611 | `3~3'` | 0.4180 | `1~3` | 0.4088 | 0.978 | no |
| 43 | 151,211 | `0~0'` | 0.4323 | `0~2` | 0.4722 | 1.092 | **yes** |
| 43 | 151,211 | `0~0"` | 0.4170 | `0~2` | 0.4722 | 1.132 | **yes** |
| 43 | 151,211 | `0'~0"` | 0.1306 | `0'~3'` | 0.5589 | 4.281 | **yes** |
| 43 | 151,211 | `3~3'` | 0.4170 | `1~3` | 0.4167 | 0.999 | no |
| 71 | 250,007 | `0~0'` | 0.3570 | `0~2` | 0.4966 | 1.391 | **yes** |
| 71 | 250,007 | `0~0"` | 0.3562 | `0~2` | 0.4966 | 1.394 | **yes** |
| 71 | 250,007 | `0'~0"` | 0.1873 | `0'~3'` | 0.5687 | 3.036 | **yes** |
| 71 | 250,007 | `3~3'` | 0.4292 | `1~3'` | 0.4369 | 1.018 | **yes** |

### Summary: how many twin pairs are closer to themselves than to their nearest foreign run

| checkpoint | iter | quantity | Euclidean, with 3‴ | 1&minus;&rho;, with 3‴ | Euclidean, without 3‴ | 1&minus;&rho;, without 3‴ |
|---|---|---|---|---|---|---|
| 0 | -1 | `mean_by_type` | 6 / 6 | 6 / 6 | 4 / 4 | 4 / 4 |
| 0 | -1 | `central_cell_skip` | 6 / 6 | 6 / 6 | 4 / 4 | 4 / 4 |
| 8 | 25,211 | `mean_by_type` | 4 / 6 | 4 / 6 | 3 / 4 | 3 / 4 |
| 8 | 25,211 | `central_cell_skip` | 4 / 6 | 4 / 6 | 3 / 4 | 3 / 4 |
| 42 | 147,611 | `mean_by_type` | 1 / 6 | 4 / 6 | 0 / 4 | 3 / 4 |
| 42 | 147,611 | `central_cell_skip` | 1 / 6 | 4 / 6 | 0 / 4 | 3 / 4 |
| 43 | 151,211 | `mean_by_type` | 1 / 6 | 4 / 6 | 0 / 4 | 3 / 4 |
| 43 | 151,211 | `central_cell_skip` | 1 / 6 | 4 / 6 | 0 / 4 | 3 / 4 |
| 71 | 250,007 | `mean_by_type` | 1 / 6 | 5 / 6 | 1 / 4 | 4 / 4 |
| 71 | 250,007 | `central_cell_skip` | 1 / 6 | 4 / 6 | 1 / 4 | 4 / 4 |

### 2a. What the tables say, before any interpretation

**Checkpoint 0 is a clean control, and it passes perfectly.** Every twin distance is **exactly
0.0** — not small, zero — in both quantities and both distance forms, while foreign distances
are 0.11–0.49. Replicates of one seed share their initialisation exactly, and before training
row B separates the six individuals without error. This is a **sanity check on the axis, not a
finding about training**: it confirms that the 65-vector is reading the network state and that
replicate runs of a seed do start identical. It also confirms, empirically, what
`backlog.md`'s `NON-DETERMINISM-IN-TRAINING-MAY-BE-THE-SOURCE-OF-THE-REPLICATE-GAP` argues
from the code — that a replicate gap cannot come from a difference in initialisation, because
at iteration −1 there is none.

**The separation is then lost during training, and only partly recovered.** On the summary
counts the pattern is the same for both quantities: 6/6 at checkpoint 0, 4/6 at ~25k, **1/6**
at both sides of the 150,000 boundary on the Euclidean form, and 1/6 (Euclidean) versus 4–5/6
(rank) at the end.

**The 150,000 boundary does not show up as a break.** Checkpoint 42 (147,611) and checkpoint
43 (151,211) give the same counts in every one of the eight cells of the summary table, and
the individual distances move by roughly a percent across it — `0~0'` 33.021 → 33.076,
`3~3'` 16.303 → 17.519 on the primary quantity. This is consistent with, and independent of,
`PENALISED-QUANTITY-READING.md` §5, which found no response of the penalised quantity at the
boundary at this grid's 3,600-iteration resolution. **This reading adds nothing new about
`stop_iter` and does not re-open it.**

---

## 3. The figures

| file | what it shows |
|---|---|
| `profiles_twin_vs_foreign.svg` / `.png` | twin distance (coloured by individual) against its nearest-foreign distance (grey), over all 72 checkpoints; 4 rows (quantity × individual) × 2 columns (distance form); log y |
| `profiles_ratio_trajectory.svg` / `.png` | the full trajectory of the ratio nearest-foreign / twin, 2 rows (quantity) × 2 columns (distance form), all six twin pairs; a black line at ratio = 1 |

Both carry **vertical lines at 25,000 and at 150,000**, as §0(f) fixed. Identity is **not
carried by colour alone**: hue marks the individual (individual 0 blue, individual 3 orange),
line style distinguishes the three twin pairs within an individual, and every line is named in
the legend. The palette was checked for colour-vision separation before use.

**What the ratio figure shows.** All six pairs start far above 1 (off the top of the clipped
axis — at checkpoint 1, twelve iterations in, twins are still nearly identical), fall through
1 during the first ~25,000 iterations, sit **below** 1 for most of the middle of training on
the Euclidean form, and drift back toward and slightly above 1 in the last third. On the
rank form the recovery is stronger and the `0'~0"` pair never goes far below 1. The two
`3‴` pairs are the two lines that fall away after ~165,000 on the Euclidean panels.

Checkpoint 0 is omitted from the ratio figure because the twin distance there is exactly 0 and
the ratio is infinite; the figure's subtitle says so.

---

## 4. Where `3‴` lies after the boundary

### Where `3‴` sits &mdash; last 30 checkpoints (index 42&ndash;71, iter 147,611&ndash;250,007)

| quantity | form | mean d(3‴, its 2 replicates) | mean d(3‴, the 7 other-individual runs) | nearest other individual | closer to its own replicates? |
|---|---|---|---|---|---|
| `mean_by_type` | Euclidean | **38.1716** | 52.1008 | `1` (39.7360) | **yes** |
| `mean_by_type` | 1 &minus; &rho; | **0.3884** | 0.6104 | `1` (0.3705) | **no** |
| `central_cell_skip` | Euclidean | **42.9643** | 59.1744 | `1` (45.1355) | **yes** |
| `central_cell_skip` | 1 &minus; &rho; | **0.3943** | 0.6071 | `1` (0.3704) | **no** |


**Per-partner detail, `mean_by_type`, Euclidean, mean over those 30 checkpoints and at the end:**

| partner | same individual? | mean over last 30 | at end (250,007) |
|---|---|---|---|
| `3` | **yes (twin)** | 38.979 | 50.633 |
| `3'` | **yes (twin)** | 37.364 | 50.231 |
| `0` | no | 61.849 | 77.353 |
| `0'` | no | 51.593 | 62.946 |
| `0"` | no | 75.280 | 86.893 |
| `1` | no | 39.736 | 52.474 |
| `2` | no | 40.516 | 51.220 |
| `4` | no | 49.673 | 61.079 |
| `5` | no | 46.058 | 58.580 |

**Read plainly.** Over the last 30 checkpoints **as an average**, `3‴` is still nearer its own
two replicates than the average other-individual run, on the Euclidean form — but the margin
is thin: its mean distance to its replicates (38.17) is only just under its mean distance to
the single nearest other individual, run `1` (39.74). On the **rank** form the ordering
reverses: `3‴` is on average **closer to run `1` than to its own twins** (0.3705 against
0.3884). The two forms disagree, and per §0(d) that disagreement is the result.

**At the end checkpoint the averages stop protecting it.** `3‴` sits at 50.63 and 50.23 from
its two replicates, while `3` and `3'` sit at only 14.73 from each other and `1~3` is 21.44.
By checkpoint 71 `3‴` is, on the primary quantity and the Euclidean form, **further from both
of its own twins than any two different individuals in the set are from each other.**

**When it leaves.** Taking "left its neighbourhood" as both of its twin distances exceeding
twice the `3~3'` distance, the first checkpoint after the boundary at which that holds is
**index 49, `chkpt_iter` 172,811** — about **22,800 iterations after `stop_iter`** — on both
quantities, on the Euclidean form. On the rank form it **never** holds. This sits beside, and
is slightly later than, `PENALISED-QUANTITY-READING.md` §3a's finding that the penalised
quantity's own rise begins between 162,011 and 165,611. Neither is at the boundary.

### Which cell types carry `3‴`'s excursion


**`mean_by_type`, at the end checkpoint (71)** &mdash; share of the squared distance from `3‴` to its two replicates

| cell type | share of squared distance | class | `3‴` at end | `3` at end | `3'` at end |
|---|---|---|---|---|---|
| `Am` | 66.85 % | other | -40.966 | 0.605 | -0.071 |
| `L4` | 11.50 % | other | 18.153 | 0.837 | 1.265 |
| `Mi14` | 5.54 % | other | 17.993 | 7.268 | 5.075 |
| `T4c` | 4.26 % | **T4/T5** | 13.005 | 1.530 | 3.773 |
| `Tm3` | 1.56 % | other | 9.776 | 4.227 | 2.815 |
| `T4b` | 1.06 % | **T4/T5** | 7.587 | 0.869 | 4.616 |
| `T3` | 0.92 % | other | 3.949 | 10.791 | 4.234 |
| `T2a` | 0.81 % | other | 8.369 | 9.658 | 2.092 |

Class shares over all 65 types: input R1&ndash;R8 **0.8 %**, T4/T5 **5.7 %**, other **93.5 %**.


**`mean_by_type`, summed over the last 30 checkpoints** &mdash; share of the squared distance from `3‴` to its two replicates

| cell type | share of squared distance | class | `3‴` at end | `3` at end | `3'` at end |
|---|---|---|---|---|---|
| `Am` | 61.77 % | other | -40.966 | 0.605 | -0.071 |
| `L4` | 9.62 % | other | 18.153 | 0.837 | 1.265 |
| `Mi14` | 6.94 % | other | 17.993 | 7.268 | 5.075 |
| `T4c` | 4.56 % | **T4/T5** | 13.005 | 1.530 | 3.773 |
| `T3` | 2.10 % | other | 3.949 | 10.791 | 4.234 |
| `Tm3` | 1.97 % | other | 9.776 | 4.227 | 2.815 |
| `T4b` | 1.46 % | **T4/T5** | 7.587 | 0.869 | 4.616 |
| `T2a` | 1.42 % | other | 8.369 | 9.658 | 2.092 |

Class shares over all 65 types: input R1&ndash;R8 **0.8 %**, T4/T5 **6.7 %**, other **92.5 %**.


**`central_cell_mean_skip_first_quarter`, at the end checkpoint (71)** &mdash; share of the squared distance from `3‴` to its two replicates

| cell type | share of squared distance | class | `3‴` at end | `3` at end | `3'` at end |
|---|---|---|---|---|---|
| `Am` | 70.11 % | other | -46.372 | 0.620 | -0.068 |
| `L4` | 10.46 % | other | 19.390 | 1.120 | 1.626 |
| `Mi14` | 4.95 % | other | 19.924 | 8.753 | 6.420 |
| `T4c` | 4.18 % | **T4/T5** | 14.357 | 1.632 | 4.465 |
| `Tm3` | 1.10 % | other | 10.770 | 5.719 | 4.231 |
| `T4b` | 1.08 % | **T4/T5** | 8.539 | 0.797 | 5.847 |
| `T3` | 0.94 % | other | 3.983 | 11.581 | 4.864 |
| `Lawf2` | 0.81 % | other | 4.433 | 3.579 | -2.594 |

Class shares over all 65 types: input R1&ndash;R8 **0.8 %**, T4/T5 **5.8 %**, other **93.4 %**.


**`central_cell_mean_skip_first_quarter`, summed over the last 30 checkpoints** &mdash; share of the squared distance from `3‴` to its two replicates

| cell type | share of squared distance | class | `3‴` at end | `3` at end | `3'` at end |
|---|---|---|---|---|---|
| `Am` | 65.37 % | other | -46.372 | 0.620 | -0.068 |
| `L4` | 8.59 % | other | 19.390 | 1.120 | 1.626 |
| `Mi14` | 6.34 % | other | 19.924 | 8.753 | 6.420 |
| `T4c` | 4.52 % | **T4/T5** | 14.357 | 1.632 | 4.465 |
| `T3` | 2.00 % | other | 3.983 | 11.581 | 4.864 |
| `T4b` | 1.51 % | **T4/T5** | 8.539 | 0.797 | 5.847 |
| `Tm3` | 1.40 % | other | 10.770 | 5.719 | 4.231 |
| `T2a` | 1.29 % | other | 8.956 | 10.439 | 2.375 |

Class shares over all 65 types: input R1&ndash;R8 **0.7 %**, T4/T5 **7.0 %**, other **92.2 %**.

### 4a. Which types carry it — stated plainly

**One cell type carries most of it: `Am`.** It takes **66.9 %** of the squared distance at the
end checkpoint on the primary quantity and **70.1 %** on the penalised reduction; over the
last 30 checkpoints, 61.8 % and 65.4 %. The next three are `L4` (~9–11 %), `Mi14` (~5–7 %) and
`T4c` (~4–5 %). The top eight types account for over 90 % in every one of the four tables.

**By the classes §0(h) asked for, and no further:**

* **input types (R1–R8): essentially nothing** — under **1 %** of the squared distance in
  every table. Whatever `3‴` is doing, it is not doing it at the photoreceptors.
* **T4/T5: a small but real share — about 6 %**, carried mostly by `T4c` and `T4b`. `T5a`–`T5d`
  do not appear in any top-eight list.
* **other types: ~92–94 %**, and within that, `Am` alone is the majority.

**These are names, not interpretations.** This reading says which labelled rows of the
65-vector the distance is concentrated in. It says nothing about what those cell types do, and
nothing about why this run's `Am` value moved.

### 4b. An arithmetic cross-check against the earlier reading

`Am` is also, arithmetically, what makes `3‴` the outlier in
`PENALISED-QUANTITY-READING.md` §3a. Recomputing the penalty's `pre_weight` from the
deterministic per-item central-cell matrix (`rowB_profiles_*_250007_det.csv`, the
`central_skip_item_*` columns) with `flyvis/solver.py:868-883`'s formula reproduces the
record's value exactly, and splits as:

| run | `pre_weight` at the end (recomputed = recorded) | of which the `Am` column | `Am` share | `Am` activity |
|---|---|---|---|---|
| `3` | 17.62967 | 0.2961 | 1.7 % | +0.620 |
| `3'` | 19.06259 | 0.3953 | 2.1 % | −0.068 |
| **`3‴`** | **56.70470** | **40.7313** | **71.8 %** | **−46.372** |

So the excursion that `PENALISED-QUANTITY-READING.md` reported as a whole-run number
(19.8 → 56.7 after the boundary, +185 %) is, on the profile axis, **one cell type going to
about −46 while its two replicates stay near 0**. That is a decomposition of a number already
on record, not a new claim about the boundary: §3a's own conclusion — that the rise begins
well after `stop_iter` and is not adjudicated by the rule — stands untouched.

---

## 5. The same question for the weights is NOT part of this reading

The natural next comparison is the identical question asked of the **weights** rather than the
activity: do two runs of one seed have more similar parameters than two runs of different
seeds, and where does `9992/003` sit in weight space? Ark's weight-space measurement of
**2026-09-15** is the instrument for it.

**It is not performed here, and nothing above is evidence about it.** It is noted so the next
reader does not have to rediscover that it is the obvious next step. Row B is an **activity**
axis; a run can differ in weights and agree in activity, or the reverse, and this reading
cannot distinguish those cases (`README.md` §14: row B "shows where individuals differ, not
where the difference was made").

---

## 6. The answer, in the terms of §0(h)

### **MIXED.**

§0(h) set three outcomes and required the answer to be taken at the **end checkpoint**, on the
**primary** quantity, in **both** distance forms, **with and without `3‴`**. The result:

| | Euclidean | 1 − ρ |
|---|---|---|
| **with `3‴`** | **1 of 6** twin pairs closer to itself | **5 of 6** |
| **without `3‴`** | **1 of 4** | **4 of 4** |

* The clause **"row B tells individuals apart"** is **not met**. It required *every* twin pair
  to be closer to itself than to its nearest foreign run, in both forms, with and without
  `3‴`. On the Euclidean form only one twin pair qualifies in either scope.
* The clause **"it does not"** is **also not met as a whole**. It required twin distances to be
  comparable to or larger than nearest-foreign in *most* pairs — true on the Euclidean form
  (5 of 6 fail, 3 of 4 without `3‴`), but false on the rank form, where 5 of 6 and 4 of 4
  succeed.
* Therefore **MIXED**, and §0(h) requires the failing pairs listed rather than a threshold
  invented to resolve them.

**The pairs that fail, at checkpoint 71, named:**

| quantity | form | scope | pairs where the twin is NOT closer (ratio) |
|---|---|---|---|
| `mean_by_type` | Euclidean | with `3‴` | `0~0'` (0.704), `0~0"` (0.709), `0'~0"` (0.730), `3~3‴` (0.423), `3'~3‴` (0.359) |
| `mean_by_type` | Euclidean | without `3‴` | `0~0'` (0.704), `0~0"` (0.709), `0'~0"` (0.730) |
| `mean_by_type` | 1 − ρ | with `3‴` | `3'~3‴` (0.878) |
| `mean_by_type` | 1 − ρ | without `3‴` | *none* |
| `central_cell_skip` | Euclidean | with `3‴` | `0~0'` (0.754), `0~0"` (0.688), `0'~0"` (0.817), `3~3‴` (0.415), `3'~3‴` (0.359) |
| `central_cell_skip` | Euclidean | without `3‴` | `0~0'` (0.754), `0~0"` (0.688), `0'~0"` (0.817) |
| `central_cell_skip` | 1 − ρ | with `3‴` | `3~3‴` (0.973), `3'~3‴` (0.961) |
| `central_cell_skip` | 1 − ρ | without `3‴` | *none* |

### What the mixture is made of — three separate disagreements

**(i) The two distance forms disagree, and this is the main result.** The same 65-vectors, at
the same checkpoint, say "twins are not specially similar" when compared by **magnitude**
(Euclidean) and "twins are specially similar" when compared by **rank order across the 65
types** (1 − ρ). Both were declared in advance; neither is preferred after the fact. The
honest statement is: **on this sample, at the end of training, replicate runs of one seed
resemble each other in the *shape* of their activity profile across cell types more than
foreign runs do, and do not resemble each other in the *level* of that profile more than
foreign runs do.** That is one sentence and it is the whole finding. Whether the shape
agreement is the meaningful one is not decidable here, and §0(d) forbids picking the winner
now.

**(ii) The two quantities agree with each other almost everywhere.** `mean_by_type` and
`central_cell_mean_skip_first_quarter` give the **same** count in **9 of the 10 rows** of the
summary table; the one disagreement is at checkpoint 71 with `3‴` on the rank form (5/6 versus
4/6, because `3~3‴` lands at 0.973 on the penalised reduction and 1.091 on the primary). The
primary and the penalised reduction are therefore **not** telling different stories here — a
useful negative, since `README.md` §3 sets them up precisely so that a difference between them
could be detected.

**(iii) `3‴` changes the answer on the rank form and not on the Euclidean one.** Removing it
takes the rank form from 5/6 and 4/6 to **4/4 and 4/4** — i.e. without `3‴`, the rank form
satisfies the "tells individuals apart" clause completely. It leaves the Euclidean form
unchanged in substance (1/6 → 1/4; the three individual-0 pairs fail either way). **Per §0(e),
this is stated as holding only under the without-`3‴` reading and is not carried into the
overall answer**, which remains MIXED.

### The `3‴` half of the question, plainly

`3‴` lies, at the end, **outside its own individual** on the Euclidean form: further from both
of its twins (50.63, 50.23) than any two different individuals are from each other (`1~3`,
21.44). Averaged over the last 30 checkpoints it is still marginally inside (38.17 to its
twins against 39.74 to its nearest foreign individual), so **when in the window one looks
changes the answer** — another reason this is MIXED rather than resolved. It departs at
roughly `chkpt_iter` 172,811, about 22,800 iterations **after** the boundary, not at it. Its
excursion is carried overwhelmingly by the cell type **`Am`**, with `L4`, `Mi14` and `T4c`
behind it, and essentially not at all by the input types R1–R8.

### One thing that is surprising, and is recorded because it was not expected

**Individual 0 fails the Euclidean comparison while being the tightest individual on the rank
form.** Its three runs are the most mutually similar of anything in the set by rank (`0'~0"`
reaches ratio 3.04 on the penalised reduction) and are among the worst by magnitude (all three
pairs 0.69–0.82). **A single individual is simultaneously the best and among the worst case
for "row B tells individuals apart", depending only on which pre-declared distance is used.**
No threshold is invented here to decide between them.

---

## 7. Caveats

1. **N, and where the twins live.** N = **6 individuals** (`README.md` §7, §14; the `N` block
   of the records). The four replicate runs do not enter N. Worse for this particular
   question: **all 6 twin pairs sit on only 2 of the 6 individuals**, and four individuals
   contribute no twin pair at all. Every statement above about twins is a statement about
   seeds 0 and 3.
2. **A preview, not a test.** `status: "unregistered_diagnostic"`,
   `readable_as_verdict: false`. `docs/next-session-plan.md` §5: *"Do not read row B as a test
   at N < 8."* `README.md` §14: *"Six is more individuals, not a test."* No p-value, no
   significance claim and no confidence interval appears in this file, by the declaration of
   §0(g).
3. **16 held-out items.** Every 65-vector is aggregated over the registered **16** held-out
   items, batch 1, augmentation off (`README.md` §9). The 13- and 10-item subsets are context
   only per `README.md` §7 and were **not** computed here. A different item composition is a
   different measurement.
4. **The instrument is deterministic evaluation of NON-deterministically trained
   checkpoints.** This is the caveat that matters most for reading the twin distances.
   `--deterministic` makes the **evaluation** bit-reproducible; it does nothing to the
   **training** that produced the checkpoints, which ran under the nights' `--no-determinism`
   (`tools/night/start_night.ps1:68`) for 250,000 iterations. So a twin distance of 59.29
   between `9991/000` and `9991/900` is **a real property of those two training runs** — it is
   not evaluator noise, and the zero floor of §1 proves it is not — but its **source** is
   GPU operation order during training, not anything about the individual. Checkpoint 0's
   exactly-zero twin distances pin this down: the two runs began identical, so everything that
   separated them arose inside training. See `backlog.md`,
   `NON-DETERMINISM-IN-TRAINING-MAY-BE-THE-SOURCE-OF-THE-REPLICATE-GAP` (MEDIUM, open,
   2026-09-20, raised by Ark), which argues the same point from the code and notes that one
   `--seed` fixes decoder init, data order and the 65 biases alike — so the replicate gap
   cannot come from a difference in any of them. **If that entry's first step shows training
   non-determinism is the source, then the twin distances measured here are a property of our
   training configuration and not of the individuals, and the whole comparison above would
   need re-reading in that light.**
5. **Checkpoint-grid resolution.** 3,600 iterations around the boundary; `stop_iter` sits
   2,389 iterations after checkpoint 42 and 1,211 before checkpoint 43
   (`PENALISED-QUANTITY-READING.md` §2a). Nothing here localises an event at 150,000 more
   sharply than that window, and §2a's finding of "no break at the boundary" inherits the
   limit.
6. **Mode, path and scope.** Deterministic record, `reduction_path: "gpu"`,
   `floor_k: 1` inside the 720-pair run (`PENALISED-QUANTITY-READING.md` §10 (iii): "floor
   k=5" does **not** describe the 720-pair run). The superseded CPU-path outputs, the
   three-checkpoint scope and the pre-sigma-guard floor summaries were **not** read and
   nothing is pooled with them.
7. **Two reductions, not merged.** Reported separately throughout, per §0(c). They happen to
   agree; that is an observation, not a licence to merge them in a later reading.
8. **What was not read.** `std_by_type`, `last_frame_by_type`, `central_cell_mean`,
   `mean_by_type_skip_first_quarter`, and the per-step `.h5` tensors. The weights were not
   touched (§5). No item-level statistics were computed beyond the aggregation the quantities
   are defined by, and the §4b cross-check's per-item read of one checkpoint's central-cell
   matrix.

---

## 8. Files written by this reading

| file | what | holds values? |
|---|---|---|
| `results/night5/diagnostics/rowB/PROFILES-READING.md` | this file | **yes** |
| `results/night5/diagnostics/rowB/profiles_reading_distances.csv` | every pair × checkpoint × quantity × distance form: 45 pairs × 72 checkpoints × 2 quantities × 2 forms = **12,960 rows**, with the nearest-foreign pair and ratio under both the with-`3‴` and without-`3‴` scopes | **yes** |
| `results/night5/diagnostics/rowB/profiles_twin_vs_foreign.svg` / `.png` | twin vs nearest-foreign distance over training | **yes** |
| `results/night5/diagnostics/rowB/profiles_ratio_trajectory.svg` / `.png` | the ratio trajectory over training | **yes** |

**Columns of `profiles_reading_distances.csv`:** `run_a_netdir`, `run_a_label`,
`run_a_individual`, `run_b_netdir`, `run_b_label`, `run_b_individual`, `pair_kind`
(`twin`/`foreign`), `chkpt_index`, `chkpt_iter`, `side_of_150000`, `quantity`,
`distance_form`, `distance` (full float64 repr, not rounded),
`is_nearest_foreign_for_twin_with_3ppp`, `is_nearest_foreign_for_twin_without_3ppp`,
`nearest_foreign_distance_with_3ppp`, `ratio_nf_over_twin_with_3ppp`,
`nearest_foreign_distance_without_3ppp`, `ratio_nf_over_twin_without_3ppp`. The last four are
filled only on `twin` rows.

**Read from, and not modified:** `rowB_records_det.json`, `rowB_axis_det.json`,
`rowB_floor_det.json`, `rowB_profiles_seed3*_250007_det.csv` (§4b only), and
`rowB_records.json` (§1 cross-check only).

**Modified:** `results/night5/diagnostics/rowB/README.md` — the "PENDING, not yet authorised"
paragraph of §8 only, to record the authorisation and point at this file. Nothing else in that
file was touched.

**`spearman` / `rankdata` are reused verbatim** from
`results/night2/diagnostics/ablation/ablation.py:116-144`, as `README.md` §9's reuse table
requires; they were not re-implemented.
