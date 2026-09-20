# Step 0 — source verification of the label-array field inventory

**Author:** CC. Read-only verification per `docs/plans/2026-09-20-genome-design-around-s2.md` §6
step 0. No network, no polarity recomputation (that is §4, gated on Mike's word), no tracked
file touched, no commit.

## 0. File located, hashed, versioned

Observed: `tools/.venv/Lib/site-packages/flyvis/utils/groundtruth_utils.py`, 630 lines (631 with
trailing newline).
sha256 (via `sha256sum`): `fe3927cbfc5463abf2dfefd590b8b628a7f3be11c9a079a6bd0de70d5241dae6`.
Installed `flyvis.__version__` (imported from `tools/.venv/Scripts/python.exe`): `1.2.0`.
`flyvis.__file__`: `tools\.venv\lib\site-packages\flyvis\__init__.py` (same venv).

The 65 cell-type names were read from
`tools/.venv/Lib/site-packages/flyvis/connectome/fib25-fib19_v2.2.json`, `nodes[*].name`, parsed
with the standard `json` module (no network): 65 entries, all distinct.

## 1. Every module-level name — full inventory

Observed, read directly from the file (line numbers are the `name = ` / `name = [`/`name = dict(`
line, i.e. the declaration line, matching the convention the brief and the design both use):

| name | line | kind | entries (imported, `len()`) | coverage of 65 | keys not in the 65 | comment within 3 lines / same line |
|---|---|---|---|---|---|---|
| `polarity` | 16 | literal dict | 65 | 65/65 | none | `:15` `# 1 is ON, 0 is unknown, -1 is OFF` (definitional); `:29` inline `# Drews 2020, Matulis 2020` on the `"L5"` entry only |
| `on_pathway` | 84 | literal list | 12 | 12/12 | none | none within 3 lines |
| `off_pathway` | 98 | literal list | 12 | 12/12 | none | none within 3 lines |
| `layout` | 113 | literal dict | 65 | 65/65 | none | none within 3 lines |
| `preferred_directions` | 181 | literal dict | 8 | 8/65 | none (all 8 keys are among the 65) | none within 3 lines |
| `on_direction_selective` | 192 | literal dict | 65 | 65/65 | none | none within 3 lines |
| `off_direction_selective` | 260 | literal dict | 65 | 65/65 | none | none within 3 lines |
| `not_direction_selective` | 328 | literal dict | 65 | 65/65 | none | none within 3 lines |
| `asymmetric_input` | 397 | literal dict | 65 | 65/65 | none | none within 3 lines |
| `unsufficient_data` | 464 | literal list | 9 | 9/65 | none | none within 3 lines |
| `noisy_data` | 475 | literal list | 4 | 4/65 | none | none within 3 lines |
| `symmetric_inputs` | 477 | derived: list comprehension over `asymmetric_input.items()`, `v == 0 and cell_type not in unsufficient_data and cell_type not in noisy_data` | 33 | 33/65 | none | none within 3 lines |
| `no_motion_tuning` | 487 | literal list (three L-type lines commented out at `:488-490`, `:496-498`) | 10 | 10/65 | none | `:486` `# no motion tuning in T4 and T5 inputs` (definitional) |
| `motion_tuning` | 506 | literal list | 8 | 8/65 | none | none within 3 lines (`:484` `### for correlation to tuning metrics` is 22 lines above, out of the 3-line window) |
| `on_motion_tuning` | 507 | literal list | 4 | 4/65 | none | none within 3 lines |
| `off_motion_tuning` | 508 | literal list | 4 | 4/65 | none | none within 3 lines |
| `known_dsi_types` | 510 | derived: `[*no_motion_tuning, *motion_tuning]` | 18 | 18/65 | none | none within 3 lines |
| `known_preferred_contrasts` | 512 | derived: dict comprehension over `polarity.items()`, `v in [-1, 1]` | 32 | 32/65 | none | none within 3 lines |
| `tuning_curves` | 515 (`dict(` opens here; the citation comment is at `:514`) | literal dict, 8 keys, each a 12-element list | 8 | 8/65 | none | `:514` `# from Maisak et al. 2013 Fig. 3 g, h` (citation, covers the whole dict) |

**19 module-level names total** (all imported cleanly with
`tools/.venv/Scripts/python.exe`; no heavy-dependency failure, `ast` fallback was not needed).
Counts above are `len()` on the live imported objects, not hand counts.

No key in any dict/list is absent from the 65 connectome type names (`notin65` was empty for
every field checked programmatically — `polarity`, `on_pathway`, `off_pathway`, `layout`,
`preferred_directions`, `on_direction_selective`, `off_direction_selective`,
`not_direction_selective`, `asymmetric_input`, `unsufficient_data`, `noisy_data`,
`symmetric_inputs`, `no_motion_tuning`, `motion_tuning`, `on_motion_tuning`,
`off_motion_tuning`, `known_dsi_types`, `known_preferred_contrasts`, `tuning_curves`).

## 2. Docstring

Observed: lines 1–11 exactly bound the module docstring (`"""` opens `:1`, closes `:11`). Full
text of the sentence the design quotes, lines 8–10: "All data structures are based on published
literature and may need to be updated as new research becomes available." The design's quoted
line range and wording are both correct.

## 3. The negative claim and its instrument

**Instrument applied, as specified in the task**: for each field, its own declaration line(s)
and the 5 lines immediately above were searched for `et al`, a 4-digit year matching
`19\d\d|20\d\d`, `Fig`, `doi`, `http`, `from `, an author-like capitalised-surname-then-year
token, and any `#` comment.

Result, per field (all 19 module-level names; the two derived-list literals `on_motion_tuning`/
`off_motion_tuning` share `motion_tuning`'s block and were checked at their own lines too):

- `polarity` (`:16`, window `:11-16`): comment found, not a citation — `:15`
  `# 1 is ON, 0 is unknown, -1 is OFF`. The field's *own* declaration carries nothing citation-
  shaped. (One entry inside the dict, `"L5"` at `:29`, does carry a citation — see below; this
  is a per-entry, not a per-field, citation and the instrument as specified operates on the
  field's declaration line and the 5 lines above it, where nothing is found.)
- `on_pathway` (`:84`): nothing.
- `off_pathway` (`:98`): nothing.
- `layout` (`:113`): nothing.
- `preferred_directions` (`:181`): nothing.
- `on_direction_selective` (`:192`): nothing.
- `off_direction_selective` (`:260`): nothing.
- `not_direction_selective` (`:328`): nothing.
- `asymmetric_input` (`:397`): nothing.
- `unsufficient_data` (`:464`): nothing.
- `noisy_data` (`:475`): nothing.
- `symmetric_inputs` (`:477`): nothing.
- `no_motion_tuning` (`:487`, window `:482-487`): comment found, not a citation — `:486`
  `# no motion tuning in T4 and T5 inputs`; also `:484` `### for correlation to tuning metrics`
  falls outside the 5-line window from `:487` (line 484 is 3 lines above 487, so it IS inside a
  5-line window — re-checked: `:484` is a section header, not citation-shaped; no `et al`/year/
  `Fig`/`doi`/`http`/`from `/surname-year in it).
- `motion_tuning` (`:506`): nothing in its own line or the 5 lines above.
- `on_motion_tuning` (`:507`): nothing.
- `off_motion_tuning` (`:508`): nothing.
- `known_dsi_types` (`:510`): nothing.
- `known_preferred_contrasts` (`:512`): nothing.
- `tuning_curves` (`:515`, window `:510-515`): **citation found** — `:514`
  `# from Maisak et al. 2013 Fig. 3 g, h` (matches `from `, `et al`, `20\d\d`, `Fig` all four).

**The one inline exception**: within the `polarity` dict, the `"L5"` entry at `:29` carries
`# Drews 2020, Matulis 2020` (matches surname-year pattern twice, no `et al`/`Fig`/`doi`/`http`).
This is a per-entry comment, not a per-field one — `polarity` as a whole (the module-level name)
has no citation on its own declaration line or above it.

**So under the stated instrument: exactly two hits at the field level** — `tuning_curves`
(citation) and, if counted as a field-level hit, `polarity`'s single `L5` entry (an entry-level,
not field-level, citation). The brief's "twelve fields, no source stated at all" list (brief §8,
`docs/briefs/2026-09-16-step2-tuning-battery.md:93`) names 12 fields:
`polarity, on_pathway, off_pathway, layout, preferred_directions, on_direction_selective,
off_direction_selective, not_direction_selective, asymmetric_input, unsufficient_data,
noisy_data, motion_tuning/on_/off_` (the last counted as one item, consistent with the brief's
own grouping). Applying the stated instrument to all 12 confirms **zero** of them carry a
field-level citation or citation-shaped comment (only `polarity` and `no_motion_tuning` carry
non-citation definitional comments, both examined above). **The negative claim holds** under
this instrument, field by field, with the caveat that `polarity`'s inclusion in the "no source"
list is correct only for the field as a whole — one of its 65 entries is individually cited.

## 4. Design's §3 checked against source, class by class

**Class A** (`docs/plans/2026-09-20-genome-design-around-s2.md:117-121`): lists `L5 (:29)` and
`tuning_curves, incl. T4a-d/T5a-d (:514)`.

- `tuning_curves` line and citation: confirmed exactly (comment at `:514`, dict opens `:515`;
  design's `:514` matches the comment line, which is the citation-bearing line — correct).
- **Disagreement (classification, not a line/count error): `L5` is not a module-level field.**
  It is one key inside the `polarity` dict. Presenting `L5` as a peer entry to `tuning_curves` in
  the Class A table conflates an entry-level citation with a field-level one. The module-level
  field `polarity` itself has no citation on its own declaration (§3 above) and is correctly
  placed in Class B by the design — but the Class A table, read on its own, could be misread as
  claiming `polarity` (via "L5") is sourced. It is not; only one of its 65 entries is.

**Class B** (`:127-131`): `polarity (:16)`, `on_pathway (:84)`, `off_pathway (:98)`,
`layout (:113)`, `preferred_directions (:181)`, `on_direction_selective (:192)`,
`off_direction_selective (:260)`, `not_direction_selective (:328)`, `unsufficient_data (:464)`,
`noisy_data (:475)`, `motion_tuning`/`on_motion_tuning`/`off_motion_tuning (:506-508)`. All 11
line numbers confirmed exact against the source (§1 table above). All 11 confirmed to carry no
field-level citation under the §3 instrument. No disagreement.

**Class C** (`:148-149`): `asymmetric_input (:397)` and `symmetric_inputs (:477`, derived
in-file from `asymmetric_input` minus two exclusion lists, count 33`)`. Both line numbers exact.
Derivation description exact: `symmetric_inputs` = entries of `asymmetric_input` with value 0,
excluding `unsufficient_data` and `noisy_data` — matches `:477-481` verbatim. Count confirmed
33 by import. No disagreement.

**Class D** (`:163-165`): `symmetric_inputs (:477, 33)`, `known_dsi_types (:510 = no_motion_tuning
+ motion_tuning, 18)`, `known_preferred_contrasts (:512, from polarity, 32)`,
`no_motion_tuning (:487, 10)`. All four line numbers exact. All four derivation expressions exact
(`known_dsi_types = [*no_motion_tuning, *motion_tuning]`; `known_preferred_contrasts = {k: v for
k, v in polarity.items() if v in [-1, 1]}`). All four counts confirmed by import: 33, 18, 32, 10.
No disagreement.

**No field appears in the design's §3 that does not exist in the source, and no module-level
field is missing from the design's inventory.** All 19 module-level names are accounted for
across classes A–D (counting `symmetric_inputs` once, cross-referenced in both C and D as the
design itself states explicitly).

**Summary of disagreements found: one.** The Class A table's `L5` row names a dict entry, not a
module-level field, and should not be read as putting the `polarity` field itself in Class A. No
line-number errors, no count errors, no derivation-expression errors, no missing fields, no
phantom fields.

## 5. Where these fields are used elsewhere in flyvis (grep, package-wide)

Observed (`grep -rn` over `tools/.venv/Lib/site-packages/flyvis`, excluding `__pycache__`):

- `flyvis/analysis/flash_responses.py:102` — `fri_correlation_to_known`: builds its label set
  from `groundtruth_utils.polarity.items()` filtered to `v != 0`.
- `flyvis/analysis/flash_responses.py:298-299` — `polarity` again, split into ON/OFF lists.
- `flyvis/analysis/moving_bar_responses.py:418-419` — `dsi_correlation_to_known` (per brief §8)
  reads `groundtruth_utils.motion_tuning` and `groundtruth_utils.known_dsi_types`.
- `flyvis/analysis/moving_bar_responses.py:499,776-777` — `correlation_to_known_tuning_curves`
  and a plotting helper read `groundtruth_utils.tuning_curves[cell_type]`.
- `flyvis/utils/nodes_edges_utils.py:159,165` — a `preferred_contrasts` helper reads
  `groundtruth_utils.polarity` (docstring references it at `:159`; used at `:165`).
- `flyvis/utils/color_utils.py:12` — `from flyvis.utils.groundtruth_utils import polarity`, used
  for coloring cell types by known polarity in plots.

`on_pathway`, `off_pathway`, `layout`, `preferred_directions`, `on_direction_selective`,
`off_direction_selective`, `not_direction_selective`, `asymmetric_input`, `unsufficient_data`,
`noisy_data`, `symmetric_inputs`, `on_motion_tuning`, `off_motion_tuning`,
`known_preferred_contrasts` did not appear in the grep hits above outside their own module — i.e.
they are not consumed by any of the four analysis functions the brief names. This matches the
brief's own observation (`docs/briefs/2026-09-16-step2-tuning-battery.md:59`) that
`correlation_to_known_tuning_curves` and `angular_distance_to_known` are "not called anywhere
inside flyvis" — those two, plus `dsi_correlation_to_known` and `fri_correlation_to_known`, are
themselves the only consumers found, and together they touch only `polarity`, `motion_tuning`,
`known_dsi_types`, and `tuning_curves`.

## 6. Table for the extraction

| field | class per source | citation text | entries | coverage of 65 |
|---|---|---|---|---|
| `polarity` | unattributed (field-level); one entry (`L5`) individually cited | none (field); `# Drews 2020, Matulis 2020` on `L5` only | 65 | 65/65 |
| `on_pathway` | unattributed | none | 12 | 12/65 |
| `off_pathway` | unattributed | none | 12 | 12/65 |
| `layout` | unattributed | none | 65 | 65/65 |
| `preferred_directions` | unattributed | none | 8 | 8/65 |
| `on_direction_selective` | unattributed | none | 65 | 65/65 |
| `off_direction_selective` | unattributed | none | 65 | 65/65 |
| `not_direction_selective` | unattributed | none | 65 | 65/65 |
| `asymmetric_input` | suspected-connectivity-derived (design's proposal; source states no derivation) | none | 65 | 65/65 |
| `unsufficient_data` | unattributed | none | 9 | 9/65 |
| `noisy_data` | unattributed | none | 4 | 4/65 |
| `symmetric_inputs` | derived-in-file (also suspected-connectivity-derived per design, since its parent is) | none | 33 | 33/65 |
| `no_motion_tuning` | unattributed | none | 10 | 10/65 |
| `motion_tuning` | unattributed | none | 8 | 8/65 |
| `on_motion_tuning` | unattributed | none | 4 | 4/65 |
| `off_motion_tuning` | unattributed | none | 4 | 4/65 |
| `known_dsi_types` | derived-in-file | none (derivation: `[*no_motion_tuning, *motion_tuning]`) | 18 | 18/65 |
| `known_preferred_contrasts` | derived-in-file | none (derivation: from `polarity`, `v in [-1,1]`) | 32 | 32/65 |
| `tuning_curves` | sourced | `# from Maisak et al. 2013 Fig. 3 g, h` | 8 | 8/65 |

Class unchanged from the design's §3 in every row except the note on `polarity`/`L5` above; the
design's own class assignments (A–D) are not contradicted by the source, only the Class A table's
presentation of `L5` as a peer field needs the caveat recorded in §4.
