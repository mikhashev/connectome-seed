---
**Status:** registered, not yet run. Drafted by a CC subagent, 2026-09-24 UTC, on Mike's approval
of step 3 ("the second brain"), question (i) only (Johnny, chat 06:53 UTC), with three required
edits (3a per-fold lambda, 3b rank spectrum r = 1..4, 3c FlyWire-native shuffles + explicit
negative branch), all carried below. **Revised 2026-09-24 UTC** after Mike's decisions in chat
(07:28 UTC): the type set is **30** (column-assigned, name-matched types only, no imputation),
and a **second arm** is added -- the flyvis bank restricted to the same 30 types, run through the
same script -- with a pre-stated joint reading (§5). Every place a decision was made is marked
**"decided by Mike, chat 2026-09-24 07:28 UTC"**; no `[OPEN FOR MIKE]` items remain (§9 records
what was resolved and how; the handedness question is kept as a note, not an open item, since it
does not block this specific test). This registration must be committed before the bank builder
or the run script is executed (same discipline as `docs/plans/2026-09-24-bf1-p3-registration.md`,
its direct precedent). **No FlyWire bank, no BF value on FlyWire data, and no statistic of
FlyWire connectivity of any kind exists anywhere at the time this file is written.** Neither
script named below was run beyond reading file headers to learn column names, plus read-only
counting of already-committed files (§1, §8).
**Checked and corrected by CC before commit:** (1) the flyvis30 arm was cut from `H.REAL` after
the FlyWire arm had repointed it, so it would silently have been a copy of the FlyWire bank; it
is now cut from `FLYVIS_REAL`, the flyvis bank captured at import. (2) The joint-reading table
lumped B and C as "not A"; it now has one row per case, and the script raises on any pair it
does not cover (§5a). (3) The two readings of a B are cut at a fixed `f_real >= 0.5`, and both
are printed (§5). (4) The script now writes `RESULT.md`. One count was taken on the public
flyvis bank: 228 of its 604 nonempty pairs lie within the 30 types, above the 100-pair stop rule
(§6). No BF value on any 30-type bank was computed.
---

# Registration: BF_r on the FlyWire right optic lobe, P3 against its own shuffles

## 0. Question and why it is asked now

`docs/notes/2026-09-24-bf1-p3-what-it-showed.md` §4 named the next step: does the rank-1
bilinear term separate a *second* bank, built the same way but from a different animal and a
different reconstruction pipeline (FlyWire, right optic lobe), the way it separated the flyvis
bank (branch A: real +0.02815, shuffled max 0.00000, 0/99)? That is question (i) of step 3
(`idea.md`). Question (ii), "is it the same structure" (transfer, with its own null), is a later,
separate registration and is **not** run here.

This is a **second, independently built bank**, not a filtered view of our existing bank. It is
beside the 99 degree-preserving shuffles, not instead of them
(`docs/notes/2026-09-23-where-our-bank-comes-from.md` §5.4): a shuffle asks whether BF finds
structure that a random rewiring with the same marginals lacks; FlyWire asks whether what BF finds
survives a change of fly, sex-adjacent pipeline, and reconstruction method.

## 1. Sources, licence per file, and what may be committed

Data root (outside the repo, not committed):
`connectome-seed-data/FlyWire/` (see its `SOURCE.md`, read in full this session).

| File | Licence | Used for |
|---|---|---|
| `proofread_connections_783.feather`, `proofread_root_ids_783.npy` (Zenodo 10676866, v783) | **CC-BY-4.0** | neuron-to-neuron synapse counts (the connectivity itself) |
| `murthylab-visual-system-parts-list@0d8574d/` (pinned commit) | **Apache-2.0** | `neuron_table.csv`: cell ID -> resolved type, side, category (right/left, intrinsic/boundary). `README.md`'s stated synapse thresholds (2+ synapses in the optic lobes; §3). Type-name vocabulary. |
| `column_assignment.csv.gz` (Codex download) | **CC BY-NC 4.0. "Not for the CC-BY repository"** (per `SOURCE.md`) | the only source found for per-neuron hex column position `(p, q)` (and `x, y`), needed to compute offsets `(du, dv)` the way flyvis does (§2.2, note). |
| `visual_neuron_types.csv.gz`, `consolidated_cell_types.csv.gz` (Codex download) | CC BY-NC 4.0 | cross-check of type names against `neuron_table.csv`'s `resolved type` (§2) |
| `flywire_annotations/`, `Supplemental_file1_neuron_annotations.tsv` (Schlegel et al. 2024) | not re-checked this session | not used in this registration |

**Finding, flagged per the task's instruction 1: column assignment is only available from the NC
Codex file.** `column_assignment.csv.gz` is the only file in the data root with per-neuron
`(p, q)` hex coordinates; `proofread_connections_783.feather` and the Apache-2.0 parts-list carry
no column position. This repeats, independently, what
`docs/notes/2026-09-23-where-our-bank-comes-from.md` §5.1 already found for the Codex download
page in general.

**Consequence, decided by Mike, chat 2026-09-24 07:28 UTC (confirming the proposal below):**

- The **bank itself** — the derived type x type x offset table, which encodes column positions
  taken from the NC file — is built and kept **only under `connectome-seed-data/FlyWire/derived/`,
  never committed**, the same way the raw FlyWire files are already kept outside the repo.
- **The repo gets code, the manifest with hashes (including the column file's own identity, §1
  below), and the aggregate results** (`RESULT.md` / `summary.json` / `per_shuffle.csv`, numbers
  only, no per-neuron or per-column data) — Mike's own wording for what the repo holds.
- The connectivity counts (`proofread_connections_783.feather`, CC-BY) and the type/side table
  (`neuron_table.csv`, Apache-2.0) alone would be committable, but they cannot build the bank
  without column positions, so the whole derived bank inherits the NC-BY restriction transitively
  once column position is folded in. This is the same posture the repo already takes with the
  flyvis-derived bank's *source* json (kept outside the repo tree it came from originally) versus
  its *extracted, committed* `results/genome/bank/` tables — except here even the extracted table
  cannot be committed, because unlike flyvis's own licence, Codex's NC term attaches to derived
  works too as far as this session checked (not a legal opinion, but decided as the working
  posture above).

**Manifest requirement.** The bank builder's manifest must record the column file's full identity
-- name, size in bytes, sha256, download date -- not just a hash of the derived output: it is a
load-bearing input (§1's licence finding rests on it) that cannot be rebuilt from anything in the
repo if the Codex download page changes (it is explicitly a **live** file, updated ~weekly, per
`SOURCE.md`). `connectome-seed-data/FlyWire/SOURCE.md` and `SHA256SUMS.txt` already record this
for `column_assignment.csv.gz` (downloaded 2026-09-23 UTC, sha256
`bdf4ce7f62cc63493d53eefad3816ff2dfd08b190e97b35a492e0e453df2f0f6`, 462,838 bytes, verified this
session); the builder's manifest must carry these fields forward rather than only its own re-hash
of a derived file.

**Environment.** The builder needs `pyarrow` to read `proofread_connections_783.feather`.
`pyarrow` must **not** be installed into `tools/.venv`: that environment's digest
(`94f7f483...`, 21,650 files) is pinned by night 6 gate 8
(`docs/briefs/2026-09-20-night6-deterministic-pairs.md`, ~line 525), and installing a new package
would void the comparison with nights 1-5. The builder must run in a separate, throwaway
environment instead, e.g.:

```
uv run --no-project --with pyarrow --with numpy --with pandas python \
    results/genome/c6/checks/flywire_bank_builder.py [--out DIR] [--inspect-only]
```

The run script (`flywire_bf_p3.py`) stays on `tools/.venv/Scripts/python.exe` as usual: it only
ever reads the built bank's CSV output (§10), never the feather file, so it needs no `pyarrow`
and never touches the pinned environment.

## 2. The 30 built types (decided by Mike, chat 2026-09-24 07:28 UTC)

**Method** (this session, read-only): the 65 flyvis type names in `results/genome/bank/types.csv`
were intersected with the type-name columns of `column_assignment.csv.gz` (31 distinct names, all
column-assigned), `visual_neuron_types.csv.gz` (741 distinct names) and `consolidated_cell_types.csv.gz`
(`primary_type`, 8,772 distinct names), all three from the same FlyWire v783 snapshot. This is a
name match only, per the task's constraint: no existence matrix, density or connectivity statistic
was computed.

**Union of the three FlyWire files' type-name vocabularies gives 47 exact-spelling matches, plus
`Am` counted against FlyWire's `Am1`** (the one case where a differently-spelled name is treated as
the same type, following `docs/notes/2026-09-23-where-our-bank-comes-from.md` §5.2's own
convention) = **48 name-matched types**. Of those, only **31 FlyWire types carry a column
position at all** (`column_assignment.csv.gz`'s own vocabulary), so only **30 of the 48
name-matched types** have both a name match and a column position -- offsets `(du, dv)` (§3) need
column positions on both endpoints, so only these 30 can carry any offset row under this
registration's rules.

**Decided by Mike, chat 2026-09-24 07:28 UTC: the bank is built from these 30 types only, no
imputation for the other 18 ("придумывать нельзя").** This is **open decision #1 from the earlier
draft, resolved as option (a).**

```
C2, C3, L1, L2, L3, L4, L5, Mi1, Mi4, Mi9, R7, R8, T1, T2, T2a, T3,
T4a, T4b, T4c, T4d, T5a, T5b, T5c, T5d, Tm1, Tm2, Tm3, Tm4, Tm9, Tm20
```

**The 35 dropped types, in two groups, for two different reasons:**

*18 name-matched (part of the 48 above) but with no column assignment, dropped rather than
imputed, by Mike's decision:*

```
Lawf1, Lawf2, Mi2, Mi10, Mi13, Mi14, Mi15, Tm16, Tm5a, Tm5b, Tm5c,
TmY3, TmY4, TmY5a, TmY10, TmY14, TmY15, Am (<- FlyWire "Am1")
```

*17 not matched under any spelling checked, in any of the three FlyWire files, individually or by
an obvious split:*

```
R1, R2, R3, R4, R5, R6   -- the six lamina photoreceptor relay types; FlyWire's column-assignment
                            file (31 columnar types) does not include R1-R6 individually (checked
                            by name only; whether FlyWire types them under a merged "R1-6"/"R1-R6"
                            label elsewhere was not re-checked this session -- matches the earlier
                            note's finding, §5.2)
CT1(Lo1), CT1(M10)        -- FlyWire has one type "CT1"; splitting it by neuropil (medulla vs
                            lobula compartment) was not attempted -- an object match would need it,
                            so both are dropped rather than force-merged onto one FlyWire type
Mi3, Mi11, Mi12           -- not found under any spelling checked
Tm28, Tm30, Tm5Y          -- not found (Tm5Y is flyvis's own merge of a Tm5 subtype; FlyWire splits
                            Tm5 into Tm5a-Tm5f differently -- no attempt made to reconcile)
TmY9, TmY13, TmY18        -- not found (TmY9 splits into TmY9a/TmY9b in some sources; not present
                            under either spelling checked here)
```

**30/65 is a name-and-column match, not an object match — differences that remain even for the
30 built types** (task's instruction 3c, last sentence):

- **Sex.** FlyWire v783 is one female fly (`SOURCE.md`; Dorkenwald 2024). The flyvis template is
  built from at least two female flies (FIB-25, FIB-19). Sex is held fixed between this bank and
  the flyvis bank (both female), unlike the male optic-lobe alternative that was also surveyed and
  not chosen here.
- **Method.** FlyWire is whole-brain serial-section TEM with automated segmentation and human
  proofreading (Dorkenwald 2024). The flyvis sources are FIB-SEM (Takemura 2015, Shinomiya 2019).
  Takemura et al. 2015 report "about 1.5-fold as many T-bars" detected by FIB-SEM than by ssTEM on
  the same tissue class (`docs/notes/2026-09-23-where-our-bank-comes-from.md` §5.3), so raw synapse
  counts between the two pipelines are not directly comparable in scale; only *existence* under a
  named threshold is used here (§3), not raw counts, which is why the task restricts this run to
  existence.
- **Column count.** flyvis tiles a 31-column-across hexagonal disc, radius 15, giving 721 lattice
  positions per full-stride type (`docs/notes/2026-09-23-where-our-bank-comes-from.md` §2.3). The
  FlyWire right optic lobe's actual column count is on the order of 720-800
  ("the true number of columns in this optic lobe", Matsliah 2024, cited in the same note) but was
  not counted directly this session; the bank builder must report it (§6).
- **Lamina coverage.** R1-R6 (six of the 17 dropped types) are exactly the lamina photoreceptor
  relays. Dropping them removes the retina-to-lamina front end entirely; the 30-type bank starts
  one synaptic layer downstream of where the flyvis bank starts. This is a structural, not
  incidental, difference and should be stated plainly wherever this bank's result is read.
- **Type granularity elsewhere.** FlyWire's own splits (Tm5a-Tm5f vs flyvis's Tm5a/b/c/Y; TmY9a/b)
  were not reconciled; the 30 kept types are the ones with both a clean 1:1 spelling and a
  column position, not a
  biologically verified 1:1 mapping.

## 3. How the bank would be built (mirroring flyvis, §2 of the "where our bank comes from" note)

Every threshold named in advance, per the task's instruction 3.

1. **Neurons.** From `neuron_table.csv` (Apache-2.0): rows with `side (cell body) == "right"` and
   `category` containing `"intrinsic"` or `"boundary"` (i.e. any neuron with meaningful right-optic-
   lobe presence), restricted to `resolved type` in the 30-type set (§2, FlyWire spelling). **Only
   `hemisphere == "right"`** rows of `column_assignment.csv.gz` supply column position; a neuron
   without a column assignment there contributes no offset row and is dropped from the offset
   computation (matching flyvis's own reliance on assigned columns, `docs/notes/...` §2.1). No
   imputation for un-assigned columns -- **decided by Mike, chat 2026-09-24 07:28 UTC** (§2).

   **Verified this session (recomputed directly from `column_assignment.csv.gz`, not carried over
   from the Codex web page figure used in the earlier note's §5.2): 22,933 rows have
   `hemisphere == "right"`, 22,595 have `hemisphere == "left"`.** The earlier note's "22,578/23,452"
   figure comes from Codex's own "Visual Columns Challenge" web page, a different count (unclear
   whether it is right-only, both sides, or a different snapshot) -- it is not repeated here as a
   substitute for the file's own count.

2. **Synapse threshold, per connection: 2 or more synapses per individual pre->post connection**
   -- **decided by Mike, chat 2026-09-24 07:28 UTC** ("we have to start somewhere"), recorded as a
   starting choice, not derived. It matches the parts-list README's own stated optic-lobe
   threshold ("we have excluded connections with less than 2 synapses in the optic lobes ... based
   on empirical evidence", `murthylab-visual-system-parts-list@0d8574d/README.md`), which is why it
   was the proposal Mike accepted rather than a number invented for this task. The exact column
   names and units of `proofread_connections_783.feather` were **not verified this session** (no
   `pyarrow` in `tools/.venv`; §8) -- the builder script (§7) must print and log the file's schema
   before applying this threshold, and refuse if no synapse-count column is found.
3. **Offsets `(du, dv)`.** For each ordered pair of the 30 types `(s, t)` and each pair of
   right-optic-lobe neurons `(i in s, j in t)` connected above the synapse threshold: `du, dv =
   (p_j - p_i, q_j - q_i)` using `column_assignment.csv.gz`'s `p, q` fields (its own hex axial
   coordinates; `x, y` are a second, apparently redundant pair in the same file and are not used
   unless `p, q` turn out not to be axial -- to be confirmed by the builder, not assumed).

   **Note, not an open item:** sign/handedness of `(p, q)` relative to flyvis's `(u, v)` was
   **not** checked (`docs/notes/2026-09-23-where-our-bank-comes-from.md` §5.3 point 2 flags the
   same question, including that "FlyWire's image and dataset are mirror inverted relative to the
   native fly brain"). This registration does **not** attempt to align handedness, because the P3
   existence test below is invariant to any fixed relabelling of `(du, dv)` that is applied
   consistently to every pair (existence only asks whether an offset's *count*, not its axis
   label, clears the threshold) -- **except** that flyvis's autapse rule (`s == t and (du, dv) ==
   (0, 0)`) does depend on getting the origin right, which is unaffected by handedness (0,0 is
   0,0 under a mirror). So handedness does not need resolving for this test; it would matter for
   question (ii) (transfer / same-structure), not question (i).
4. **Column averaging.** For each `(s, t, du, dv)`: mean, over all target neurons `j` of type `t`
   at any right-optic-lobe column, of the summed above-threshold synapse count from source neurons
   `i` of type `s` at that relative offset -- the same "average number of synapses ... onto the
   postsynaptic dendrite" definition flyvis uses (`docs/notes/...` §2.2), re-applied here rather
   than invented.
5. **Pruning, named explicitly (flyvis's equation 8, re-applied):** drop `(s, t, du, dv)` rows
   with mean synapse count `< 1`; drop the self-offset `s == t, (du, dv) == (0, 0)` unconditionally
   (autapse rule). **No hull-fill (`n_syn_fill`) is applied -- decided by Mike, chat 2026-09-24
   07:28 UTC.** Hull-filled rows in the flyvis bank carry `n_syn = 1` by construction and were
   themselves called "mostly false positives" by the flyvis authors (`docs/notes/...` §2.4);
   reproducing that step on FlyWire would inject a flyvis-specific convention into an otherwise
   independent bank.

   **Verified this session, recounted directly from `results/genome/bank/offsets.csv`'s
   `provenance` column: 2,117 rows `in_json`, 238 rows `hull_filled`, 23 rows `dropped`.** So the
   flyvis bank has **238 hull-filled rows, all `n_syn = 1`**, and the FlyWire bank as specified
   here will have **none** -- a named method difference between the two banks, recorded rather
   than fixed, not a discrepancy to be reconciled.
6. **Existence rule, named** ("the flyvis existence rule, re-applied", per the task's instruction
   3): a type pair `(s, t)` **exists** iff at least one `(du, dv)` row survives step 5's pruning.
   This mirrors how `REAL_CONTENT` in `harness.py` is built from `offsets.csv`'s `provenance !=
   "dropped"` rows (harness.py L136-146): existence is "has a surviving offset entry", not "mean
   synapse total above some pair-level threshold" -- the same object, re-applied to a different
   source.
7. **Sign.** Not computed and not needed: `H.FIELDS` includes `sign`, but `bf1_p3.py`'s own
   precedent registration and outcome note record that `offset`, `counts` and `sign` are "0 by
   construction" for the BF-vs-N1 P3 test and "carry no reading" (`docs/notes/2026-09-24-bf1-p3-
   what-it-showed.md` §1). This run only needs `existence`. `Bank.content` still needs *some*
   `sign` value per pair for its shape (`c["sign"]`); **placeholder `+1` for every entry -- decided
   by Mike, chat 2026-09-24 07:28 UTC**, recorded as a starting choice (sign is not read anywhere
   in this test's decision field; a real sign assignment would be needed for a future
   question-(ii) run).

## 4. Reusing the harness without changing `harness.py`

`harness.py` sha256_lf pinned at `6fc809527c69ee84aadebfc15c0ba755c189ddc93c80c05c0fa11d969a8d7297`
(same value `bf1_p3.py` already pins). **No edit to the file.**

**Chosen approach: a thin wrapper that reassigns two module globals after `import harness as H`,
not a source edit.** Concretely, after import:

```python
H.ALL_CELLS = np.array([(s, t) for s in FLYWIRE_IDX for t in FLYWIRE_IDX], dtype=np.int64)
H.REAL = H.Bank("flywire_ol_right_30", flywire_content)   # flywire_content keyed by the SAME
                                                            # 65-index namespace as H.IDX (types.csv)
```

where `FLYWIRE_IDX` is the 30 `H.IDX[name]` values for the built type set (§2), and
`flywire_content` supplies `(s, t) -> {"offsets", "hull": [], "sign": +1}` only for `s, t` in
`FLYWIRE_IDX`.

**Why this is sufficient, and why every other hard-coded 65 survives unchanged, traced through
`harness.py` this session:**

- `Bank.__post_init__` still allocates a `(65, 65)` `exists` array; it is simply `False` almost
  everywhere except the 30x30 sub-block that has entries. This costs nothing and needs no change.
- `make_view` filters `ALL_CELLS` through `train_mask`; once `H.ALL_CELLS` only enumerates the
  900 (30x30) index pairs, no cell involving one of the 35 absent types is ever produced, in
  training or in test, on any fold -- **without touching `FOLD`**. `FOLD` stays the full `(65, 65)`
  array read from `folds.csv` (`harness.py` L148-153); `cv_fold`'s `held = FOLD == f` is still a
  `(65, 65)` mask, but `cells = ALL_CELLS[held[...]]` (L755) indexes it with the *patched*
  `ALL_CELLS`, so only the 30-type cells' fold membership is ever consulted. **This is the "reuse
  `folds.csv` restricted to the built types" option** the task asked to choose between; **no new
  randomness, no new seed** is needed, because restriction happens by which cells are ever asked
  for, not by re-deriving fold assignment.
- `fit_n0`/`fit_n1`/`fit_neb`/`fit_bf`/`bf_als` all loop `range(65)` internally and allocate
  `(65,)` or `(65, r)` arrays (e.g. `alpha = np.zeros(65)`, `bf_als`'s `U0 = ... (65, r)`
  L448/674). Rows and one-hot columns for the 35 absent types are allocated but **never
  constrained by any training cell** (no cell of theirs is ever in `view.cells`) and **never
  queried** (`decode` is only ever called on cells drawn from the patched `ALL_CELLS`). Ridge
  regularisation (`fit_n1`'s `pen`) pulls their unconstrained weights toward 0; BF's `lam *
  np.eye(r)` term does the same for their `U`/`V` rows. They are inert, not wrong.
- `TYPE_FIELDS`, `PAIR_ID`, `NAMES`/`IDX` stay the full 65-type flyvis arrays; they are only ever
  indexed by the type indices actually present in `view.cells`/`ALL_CELLS`, i.e. the 30-type
  subset, so their unused rows are harmless.
- `M18`, `RP_*`, `DIAL_F` and other constants computed from 65 are not read by this test (`bf1_p3.py`'s
  precedent already limits itself to `cv`, `margin`, `bf_predictor`, `shuffled_bank`; this wrapper
  does the same).

**Rejected alternative:** editing `harness.py` to make 65 a parameter. Rejected because it would
require a new registration to re-pin the sha (the task's instruction 4 lists the pinned sha as a
constraint to satisfy, not relax), and because the monkeypatch above demonstrably reaches the same
place with zero source changes -- the wrapper's own machine check (§5) is the proof.

## 4a. Two arms, one script: which bank each worker sees

Both arms (§5a) patch the same two globals (`H.REAL`, `H.ALL_CELLS`), but to **different** banks.
`ProcessPoolExecutor` on Windows uses `spawn`: a worker process re-imports the run script fresh
and does **not** inherit the parent's patched globals. Each shuffle-fitting task therefore carries
its arm name, and the pool is given a module-level `initializer` that re-loads that arm's bank
(the FlyWire manifest's sha is re-checked against the parent's, for the `flywire30` arm) and
re-applies the same two-global patch, inside every worker, before any fit runs. Every fitting
function additionally asserts `H.REAL.name` and `len(H.ALL_CELLS)` match the arm it was called
for, so a worker that was not correctly patched fails loudly instead of silently scoring the wrong
bank.

## 5. Machine check, the three numbers, branches, and the combined reading over ranks

**Machine check (before any FlyWire number is computed):** run the wrapper *unpatched* -- i.e.
call it with `H.REAL` and `H.ALL_CELLS` left as `harness.py` set them (the flyvis bank) -- and
confirm it reproduces `bf1_p3.py`'s own recorded real-bank existence margin
**0.028150051052145946** to the same `1e-9` tolerance `bf1_p3.py` uses. Passing this proves the
wrapper's plumbing (import, global patch mechanism, cv/margin calls) changes nothing when pointed
at the original bank, before it is ever pointed at FlyWire. This is a **stronger** machine check
than reusing the pre-recorded number from `rule_runs/`, because it exercises the wrapper itself,
not just `harness.py` directly.

**Per rank `r` in {1, 2, 3, 4} (task's edit 3b), on the real FlyWire bank and on 99
FlyWire-native shuffles (task's edit 3c):**

- real margin, shuffled mean/min/max, `n_shuffled >= real`, `p = (1 + n_ge) / (1 + 99)`, gap (real
  - shuffled max) -- same fields `bf1_p3.py` reports.
- **lambda record (task's edit 3a).** `cv_fold` already writes `s["bf_lambda"]` per fold when
  `"bf_lambda" in data` (`harness.py` L758-760, `fit_bf` sets `n1["bf_lambda"]` at L730). The run
  script must save, **per rank, per bank (real and each of the 99 shuffles), per outer fold**, the
  chosen `bf_lambda`, and report: the fraction of folds where `lambda == max(BF_LAMBDAS) == 100`,
  separately for the real bank and for the shuffles.
- **branches, exactly as `bf1_p3.py`'s (task's instruction 5), applied per rank:**
  - **A: BF_r separates** -- `strictly_above_all` and `n_shuffled_ge_real == 0` on existence.
  - **B: BF_r does not separate** -- `p_one_sided >= 0.05`.
  - **C: in between** -- neither A nor B.
- **How a negative result (B) is read, pre-stated (task's edit 3a, second sentence).** Let
  `f_real` be the fraction of the real bank's 10 outer folds whose chosen `bf_lambda` equals
  `max(BF_LAMBDAS)` = 100. Both readings below are substantive negative results about the second
  brain, and **both are printed in `RESULT.md`**, never folded silently into a branch label:
  - **B with `f_real >= 0.5` -- "absent":** on FlyWire, cross-validation switches the rank-r term
    off in most folds, the same signature the flyvis *shuffles* showed
    (`docs/notes/2026-09-24-bf1-p3-what-it-showed.md` §2). There is no rank-r structure that CV
    accepts on this bank.
  - **B with `f_real < 0.5` -- "present but not bank-specific":** the term is fitted on FlyWire,
    but the bank's own degree-preserving shuffles do as well. The structure it finds is carried by
    degrees, not by wiring the shuffle destroys.
  - Which of the two it is depends on the lambda record. Without the record, as for the unrecorded
    shuffled-fold lambdas of the flyvis BF_1 run, the two cannot be told apart after the fact. The
    0.5 cut is fixed here, before any FlyWire lambda exists (CC, before commit).
- **Combining ranks (task's edit 3b):** the registered decision is **per rank** -- four independent
  branch labels, one per `r`. The **headline** is `r = 1`, for continuity with the flyvis BF_1
  result. **A rank that separates while `r = 1` does not is its own named outcome**: "higher-rank
  structure survives where rank-1 does not" -- reported, not smoothed into a single verdict.
  **Multiplicity:** four ranks are tested; the per-rank `p` values are reported unadjusted (as
  `bf1_p3.py` does for its four fields), but the run script additionally reports the
  **Bonferroni-corrected threshold `alpha/4 = 0.0125`** next to each rank's `p`, so a reader can
  see which branch-A or borderline-C results would survive correction. No single combined p-value
  is computed across ranks (the four fits are not independent draws of one quantity; they are
  four different terms on the same real bank and the same 99 shuffles), so no meta-analytic
  combination is registered.

## 5a. Second arm: flyvis restricted to the same 30 types (decided by Mike, chat 2026-09-24 07:28 UTC)

**Both arms run through the same script, same ranks 1-4, same 99 shuffle seeds 0-98, built by
`H.shuffled_bank` on each arm's own restricted bank, with lambda recorded per fold (§5) -- the
only difference between arms is which bank `H.REAL` is patched to (§4a).**

- **Arm "flywire30"**: the FlyWire right-optic-lobe bank built by `flywire_bank_builder.py` (§3).
- **Arm "flyvis30"**: `harness.py`'s own `H.REAL` (the flyvis bank), restricted to pairs where
  both endpoints are among the same 30 types -- **no new data**, every kept offset row is the
  flyvis bank's own row, just as `H.ALL_CELLS` is restricted (§4). This restricted bank's own
  degree-preserving shuffles (99, seeds 0-98) are built the same way FlyWire's are, via
  `H.shuffled_bank` on the restricted flyvis bank -- **not the same 99 shuffles as the full-65
  flyvis run**, since degree preservation is computed on the 30-type grid, a different object.

**Relation to the existing full-65 BF_1 result
(`results/genome/c6/checks/bf1_p3/summary.json`, real margin `0.028150051052145946`):
flyvis30 is its own run on a different bank (30 of 65 types, its own fold subset, its own
shuffles), not a repeat and not a subset of that number.** The machine check (§5) still reproduces
the full-65 number, on the *unpatched* wrapper, before either arm's restricted bank is built; that
proves the wrapper, not that flyvis30's margin should match it.

**Pre-stated joint reading, headline `r = 1` for both arms (Mike, chat 2026-09-24 07:28 UTC /
Zcode):**

| flyvis30 (r=1) | FlyWire30 (r=1) | Reading |
|---|---|---|
| A | A | The pattern is present in the second brain. |
| A | B | The pattern did not carry over to the second brain. |
| A | C | Weak or partial carry-over: neither "present" nor "did not carry over" is supported. |
| B or C | B or C | flyvis-30 itself does not separate on the 30-type grid: the substrate is too narrow for this test to show anything. Read as **the test failing**, not as evidence about the hypothesis. |
| B or C | A | Unexpected direction: FlyWire separates where the flyvis restriction does not -- read as a flag to re-examine both fits, not as a substantive finding on its own. |

Every pair of branch labels lands in exactly one row. The run script's `joint_reading` implements
this table and raises on any pair it does not cover (revised by CC before commit: the draft
lumped B and C together as "not A", so a FlyWire C next to a flyvis A would have been printed as
"did not carry over").

**Mixed per-rank cases (r = 2, 3, 4):** each rank gets its own pair of branch labels (one per arm)
and its own row in this same four-way table, read the same way; the `r = 1` row is the headline,
the others are reported alongside it, not averaged into it (§5's "combining ranks" rule extends
unchanged to two arms: no cross-arm, cross-rank meta-p is computed).

## 6. Can the test separate both worlds on this bank? What must be reported first.

**From what is known without building the bank:** the flyvis bank has 604 nonempty type pairs out
of 4,225 possible (65x65), about 14.3% density, over 10 outer folds (~60 nonempty test pairs per
fold on average) with a further nested nine-fold split inside `fit_bf` for the lambda choice
(`harness.py` L713-728). The FlyWire 30-type sub-bank has at most 900 possible pairs (30x30).
Whether it reaches a comparable count or density is **not known without building it** -- FlyWire's
right optic lobe is one intact, densely reconstructed brain (unlike flyvis's synthetic maximum-of-
two-partial-volumes construction), so density could plausibly be *higher*; conversely restricting
to only the 30 built types, minus R1-R6's lamina front end and the 18 column-less matched types,
could concentrate the mass into fewer, denser pairs or could thin it out if those 30 types happen
to connect mostly through types
that were dropped. Both directions are plausible; this registration does not guess which.

**What the builder must report before any BF fit is attempted (task's instruction 6):**

1. total nonempty type pairs (existence count) and density among the 30x30 = 900 possible pairs;
2. per-outer-fold nonempty test-pair counts (all 10 folds), since `FOLD` is inherited from the
   original 65-type assignment and is **not** guaranteed to distribute the 30-type subset evenly;
3. per-source and per-target degree distribution (out-degree/in-degree counts, i.e. how many
   nonempty pairs each of the 30 types participates in) -- needed because `rewire_and_permute`
   (§ task's edit 3c) preserves these degrees exactly, and a degenerate degree distribution (many
   types with degree 0 or 1) limits how much a shuffle can differ from the real bank at all;
4. per-outer-fold, per-inner-fold nonempty counts inside `fit_bf`'s own nested split (L713-728),
   since an inner fold with too few cells cannot support a meaningful lambda comparison.

**Pre-stated stop rule (degenerate bank, task's instruction 6), applied independently to each
arm:** the run script refuses to fit BF (any rank) for that arm, and instead writes only that
arm's diagnostic counts above, if **any** of, for that arm's own bank:

- fewer than **100 nonempty type pairs** total (roughly a third of flyvis's 604, chosen so that
  the average outer-fold test set is not smaller than about 10 pairs, matching flyvis's own ~60-
  per-fold order of magnitude scaled down for a 30-type instead of 65-type universe);
- **any of the 10 outer folds has 0 nonempty test pairs** (a fold that trivially cannot be scored,
  since `margin` averages per-fold advantages and a fold with no cells contributes an undefined
  term);
- **any of the 9 possible outer-fold values with nonempty test pairs has an inner split (inside
  `fit_bf`) where some inner fold also has 0 test pairs**, since `fit_bf`'s own `ll` accumulation
  (L714-726) would then silently add nothing for that lambda comparison on that inner fold rather
  than fail loudly.

If the stop rule fires, `RESULT.md` states which condition tripped and the counts that tripped it,
and **no BF fit, no shuffle, no p-value is computed** -- the same discipline `bf1_p3.py` already
applies to its own machine check (§ its "MACHINE CHECK FAILED" exit path).

## 7. Cost estimate, outputs, and what this run cannot show

**Cost.** Both arms run the same per-rank machinery, so the estimate below is **per arm**; two
arms means roughly double the total wall-clock time of a single-arm estimate.

`bf1_p3.py`'s real run (`docs/notes/2026-09-24-bf1-p3-what-it-showed.md`) took 165.3 s
total for rank 1, 99 shuffles + 1 real bank, 30 workers, on the 65-type flyvis bank ("smoke timing
... 1.7 s per outer-fold fit" per the task brief). Each 30-type bank is smaller (30x30
= 900 vs 65x65 = 4,225 possible cells, i.e. roughly 0.21x the grid), so per-fit cost is expected
to be somewhat *lower* per fit at fixed rank, dominated by `bf_als`'s `O(65^2 r)`-ish inner solves
which still allocate at the full 65-width (§4) -- so the *lower bound* on savings is small; treat
FlyWire per-fit cost as **comparable to or somewhat below** the flyvis per-fit cost, not
proportionally smaller. Ranks 2-4 cost more per fit than rank 1 (`bf_als`'s Newton step solves an
`r x r` system per row per sweep; `BF_SWEEPS = 25`, `STARTS = 10`, both fixed, so cost scales with
`r` roughly linearly to quadratically through the `H = einsum(...) + lam * eye(r)` solve).
**Rough estimate, per arm: 4 ranks x (1 real + 99 shuffled) banks x 10 outer folds, at very
roughly 2-6 s per fit depending on rank, is on the order of 15-45 minutes** with comparable
parallelism (~30 workers) to `bf1_p3.py` -- an estimate, not a measurement; the run script must
print wall-clock time actually taken, as `bf1_p3.py` does. **Two arms run sequentially in
`main()`, so total wall-clock is roughly double the per-arm estimate**, on the order of
30 minutes to 1.5 hours.

**Outputs location**, mirroring `results/genome/c6/checks/bf1_p3/`:
`results/genome/c6/checks/flywire_bf_p3/`, with one subdirectory per arm --
`flywire30/per_shuffle_rank{1..4}.csv` and `flyvis30/per_shuffle_rank{1..4}.csv` (each including
the `bf_lambda_per_fold` column required by task edit 3a) -- plus a top-level `summary.json`
holding both arms' per-rank results, the headline `r=1` joint reading (§5a), and the per-rank
joint table. The FlyWire bank artifact itself (offsets, per-neuron data) is **not** written under
`results/`; it lives under `connectome-seed-data/FlyWire/derived/` (§1) and only its sha256 and
summary counts (§6) are written into the committed manifest. The flyvis30 arm needs no separate
artifact: it is rebuilt from `harness.py`'s own data every run (§5a).

**What this run cannot show (task's instruction 7, and §0):**

- Whether the *same* rank-r structure transfers between the two banks in the deeper sense of
  question (ii) (a model trained on one bank, tested on the other, against its own null, rather
  than each bank tested only against its own shuffles) -- named as the next, separate
  registration. The joint reading in §5a is a coarser, same-question-(i) comparison: whether each
  bank separates on its own terms, not whether one bank's fitted structure predicts the other.
- Whether X (the field-group terms) alone, or jointly with BF, would also separate FlyWire --
  untested, as for the flyvis precedent.
- Anything about the left optic lobe, the male optic lobe, or any bank beyond the one built here.
- A distribution: as with `bf1_p3.py`, this is one deterministic fit per (rank, bank), fixed
  seeds, run once.
- Whether the NC-licensed column-position step (§1) itself is a source of any large-scale
  distortion relative to a hypothetical non-Codex column source -- not checkable from this
  session's files.

## 8. What was and was not verified this session

**Observed, this session:** `neuron_table.csv` (139,255 rows, header confirmed), `README.md`'s
stated 2-synapse optic-lobe threshold, `column_assignment.csv.gz`'s header
(`root_id,hemisphere,type,column_id,x,y,p,q`) and first rows, `visual_neuron_types.csv.gz`'s and
`consolidated_cell_types.csv.gz`'s headers and type-name vocabularies (741 and 8,772 distinct
names respectively), the 48-name-match/17-unmatched split, and the further 30-column-assigned/
18-column-less split within the 48 (all recomputed by a short script, not carried over from the
earlier note's unverified script), `folds.csv`'s row count (4,227 = header rows +
4,225 pairs, i.e. every one of the 65x65 pairs present, none missing), `harness.py`'s
`Bank`/`make_view`/`cv`/`cv_fold`/`fit_bf`/`bf_als`/`shuffled_bank`/`rewire_and_permute` source in
full.

**Not verified this session, flagged rather than assumed:** the column schema of
`proofread_connections_783.feather` (no `pyarrow` in `tools/.venv`, so the file could not be
opened; the builder script (§7 file below) must inspect and print its schema before applying any
threshold, and must refuse rather than guess a column name); whether `column_assignment.csv.gz`'s
`p, q` are true axial hex coordinates or something else (assumed from column naming, not
confirmed against Codex documentation); the true column count of the FlyWire right optic lobe
(cited as "on the order of 720-800" from the earlier note, not recounted).

## 9. Decisions, all made by Mike, chat 2026-09-24 07:28 UTC

No `[OPEN FOR MIKE]` items remain. What was open in the earlier draft, and how each was resolved:

1. **§2, §3.1 (open decision #1): type set.** Resolved as **30 types**, the column-assigned,
   name-matched types only -- not 48 by pair-level synapse sum, not imputed columns. "No
   imputation" ("придумывать нельзя"). The 18 name-matched-but-column-less types are dropped and
   listed as dropped **for that reason**, distinct from the 17 dropped for no name match at all
   (§2's two-group table).
2. **§1: NC-licence transitivity.** Resolved: the bank stays outside the repo
   (`connectome-seed-data/FlyWire/derived/`); the repo gets code, the manifest (with the column
   file's own identity), and the aggregate results.
3. **§3.2: synapse threshold.** Resolved: **2 or more synapses per connection** ("we have to start
   somewhere"), recorded as a starting choice, not a derived or validated number for this specific
   use.
4. **§3.5: hull-fill.** Resolved: **no hull-fill** for the FlyWire bank (the flyvis bank keeps its
   238 hull-filled rows; §3 item 5). A named method difference, recorded, not fixed.
5. **§3.7: sign.** Resolved: **placeholder `+1`** for every entry, recorded as a starting choice
   (sign is unread by this test's decision field).
6. **§3.3: handedness.** Not an open item -- kept as a note (§3 item 3) since it does not affect
   this existence-only test; it was never put to Mike as a decision to make.

## 10. Files this registration commits alongside itself

- `results/genome/c6/checks/flywire_bank_builder.py` -- **not run** beyond reading input file
  headers this session. Builds the bank described in §3 under
  `connectome-seed-data/FlyWire/derived/` and writes a manifest with every input file's sha256 and
  every threshold from §3, following `results/genome/bank/`'s `# source=...` header convention.
  Refuses on a dirty tree and pins the same conventions `bf1_p3.py` uses (module-level worker
  functions, explicit refusal messages).
- `results/genome/c6/checks/flywire_bf_p3.py` -- **not run.** The wrapper of §4/§4a, run twice
  (once per arm, §5a) with the ranks-1-4, lambda-recording, branch-per-rank machinery of §5, the
  degenerate-bank stop rule of §6 applied per arm, writing outputs as specified in §7, and the
  joint reading of §5a. Follows `bf1_p3.py`'s conventions: refuses on dirty tree, pins the harness
  sha, module-level picklable worker (now arm-aware, §4a), machine check first (§5), before any
  shuffle is fit.
