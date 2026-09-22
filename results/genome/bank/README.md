# The generation-zero bank

**Written:** 2026-09-23 local time (2026-09-22 UTC), by CC (subagent), on the grammar step's first pieces
(`docs/decisions/004-grammar-is-the-main-line.md` and its 2026-09-20 amendment: work goes to point 1 of
`idea.md`, the representation of the genome). **Status:** extraction and descriptive measurement.
**No training result is read or written here.** Every number is a structural integer, a string,
or a count from the connectome json and its compiled tables.

This directory holds **the object a genome grammar has to regenerate**: the fly's 65 cell types, its
605 type-pair entries and their offsets, taken from the connectome that ships with flyvis. It
also holds the birth ids that make those elements heritable, and a measurement of how regular
the type-pair table is.

## What is here

| file | what it is |
|---|---|
| `types.csv` | 65 rows in connectome node order: name, birth id, `pattern` kind and strides, role, layout, in/out entry counts, cells at extent 15 and 5, central cell index (extent 15) |
| `type_pairs.csv` | 605 rows, one per json edge entry, in json order: birth id, src, tar, `alpha` (sign), `alpha_fixed`, `alpha_references` (joined with `;`), `lambda_mult`, `edge_type`, offset and synapse totals in the json and in the compiled bank, `instantiated` |
| `offsets.csv` | 2,378 rows: the 2,355 compiled `(src, tar, du, dv)` rows (2,117 `in_json`, 238 `hull_filled`) plus the 23 json rows that never compile (`dropped`); compiled `n_syn`, the json literal `n_syn_json`, sign, pair birth id |
| `birth_ids.csv` | the generation-zero registry: 65 types + 605 pairs = 670 ids, `next_birth_id=671` |
| `REGISTRY.md` | the birth-id rule, why offsets inherit their pair's id, and the two-readings test |
| `bank.meta.json` | provenance: package, version, relative source file, sha256 of the json, of the compiled tables and of every output; constant fields; checks |
| `extract_bank.py` | writes all of the above |
| `REGULARITY-DECLARATION.md` + `.sha256.json` | the regularity measures and nulls, hashed before the script existed |
| `regularity.py`, `regularity_results.json` | the measurement (refuses to run if the declaration's hash changed) |
| `REGULARITY-READING.md` | what the numbers say and do not say, in plain words |

Every csv starts with one `#` line naming the source as **package + version + file**
(`flyvis 1.2.0 : connectome/fib25-fib19_v2.2.json`), the json sha256
(`bfbb0766…223351a`) and the generating script's sha256. The compiled tables are named relative
to `FLYVIS_ROOT_DIR` (`connectome/ConnectomeFromAvgFilters_0000`, extent 15, `n_syn_fill` 1).
No absolute path on one machine is recorded (`docs/notes/2026-09-23-scratchpad-paths-in-records.md`).

## Fields that do not vary (not repeated per row)

- Every node: `activation = "relu"`, `bias = 3.5`, `bias_fixed = false`, `time_constant = null`,
  `time_constant_fixed = false`. The json `bias` is **not** read by the network and is unrelated to
  the seeded bias (`docs/notes/2026-09-20-what-is-the-genome-here.md` §2).
- Every edge: `edge_type = "chem"` (kept as a column anyway, as asked), `time_constant = null`,
  `time_constant_fixed = false`.
- `receptors` is empty. `input_units` = R1–R8 (8), `output_units` = 34 types. `role` and
  `layout` in `types.csv` are derived from these two lists.
- `pattern` is `stride` for all 65 types: `[1, 1]` for 63 and `[3, 2]` for Lawf1 and Lawf2.

## The one pair that never instantiates, and the 23 rows that are dropped

`Lawf1 → Lawf1` (birth id 198) is in the json with a single offset `(1, 0)`, 1 synapse. Lawf1 cells
exist only where `u % 3 == 0` and `v % 2 == 0`, so a Lawf1 cell shifted by `(1, 0)` never lands on
another Lawf1 cell. `connectome.py:497-498` suppresses the resulting `KeyError`, so no edge
instance is ever made. That leaves **605 json entries and 604 compiled pairs**. The **23 dropped
json offset rows** are all self-offsets of the two `stride [3, 2]` types: 1 from Lawf1 → Lawf1 and
22 of Lawf2 → Lawf2's 24. All 238 hull-fill points land. On the 2,117 matched rows the compiled
`n_syn` equals the json value up to a float32 cast (max |Δ| 6.5e-6). This reproduces
`docs/notes/2026-09-20-what-is-the-genome-here.md` §2 exactly.

## Regenerate

From the repository root, with `FLYVIS_ROOT_DIR` pointing at the data directory that holds the
compiled connectome:

```
tools/.venv/Scripts/python.exe results/genome/bank/extract_bank.py   # ~5 s
tools/.venv/Scripts/python.exe results/genome/bank/regularity.py     # ~6 min, CPU
```

`extract_bank.py` is deterministic and writes UTF-8 with an explicit encoding and `\n` line
ends. It asserts every count above. It checks that the csvs decode back to the source json and
that flyvis compiles that rebuilt json at extent 5 to the same 2,355 rows. It will **not**
overwrite `birth_ids.csv` with a different registry. The script's own sha256 is in each csv
header, so any edit to the script changes the headers (and only the headers) of the outputs.

## Label provenance: linked, not repeated

The per-type labels that come from flyvis's `groundtruth_utils` (polarity, pathways, motion
tuning, and so on) are **not** in this directory. Their provenance classes (sourced / asserted but
unattributed / suspected connectivity-derived / derived in-file), the source verification and
the coverage check are in:

- `docs/plans/2026-09-20-genome-design-around-s2.md` §3: the four classes;
- `docs/plans/2026-09-20-step0-label-inventory-verified.md`: every field checked against source
  (2 of 19 module-level names carry a citation);
- `results/diagnostics/labels/`: the coverage check. **The bank carries no ON/OFF polarity**, so
  that label cannot be "predicted from the bank" (`partition.json`, question c).

**Warning: `layout` cannot judge anything.** `types.csv`'s `layout` (retina / intermediate /
output) is built by `connectome.py:196-221` from the json's `input_units` and `output_units`.
`groundtruth_utils.layout` agrees with it on 65 of 65 types
(`results/diagnostics/labels/partition.json`, `side_observation_layout`). It is bank-derived.
Using it to score a model of the bank would score the bank against itself.

## Warning: most sign citations are personal communications

From the json (`bank.meta.json` → `sign_citations`):

- 605 entries. **267 carry no reference at all.** 338 carry at least one.
- The 338 carry **432 citation slots** under 5 keys: `NernPC2018` 286, `ReiserPC2017` 82,
  `Hardie1989` 40, `Karuppudurai2014` 12, `Lin2016` 12. **368 of 432 slots (85 %) are personal
  communications** (`…PC20xx`).
- **286 of the 338 referenced entries (85 %) cite only personal communications.** 52 cite at least
  one publication, and no entry mixes the two kinds.
- `alpha_fixed` is true on 272 entries, all referenced; **232 of those 272 rest only on personal
  communications**. 66 entries are referenced but not fixed.
- All 10 exceptions to "one sign per source type" (the minority pairs of Am, C2, C3 and R8) are
  `alpha_fixed` and cite only `NernPC2018` (`REGULARITY-READING.md` §1).

This records provenance only. It is not a judgement of those sources' reliability. A
genome that "recovers the signs" recovers mostly unpublished assignments.

## Blind-author exclusions

This directory holds structural data only: no loss, no activity, no checkpoint value, no
verdict string. A literal scan of all thirteen files in this directory against the contamination values file
(`tools/contamination_scan.py`'s input, held outside the repository; counts only, no value
printed) found **0 hits in every file**. So `results/genome/` **should not need to be listed** in
`docs/blind-author-exclusions.txt`. Listing it would also forbid a blind grammar author the
very object the grammar has to regenerate.

One convention points the other way. On 2026-09-20, directories new that day were listed as
whole directories "anyway" (`tools/contamination_scan.py:126-130`). Whether that convention
extends to this directory is the integrator's call. The scan result above is the evidence
against needing it. The files are untracked until committed, so the tool's own `git ls-files`
scan has not covered them yet. It should be re-run after the commit.
