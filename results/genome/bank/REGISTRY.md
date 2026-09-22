# Birth-id registry: generation zero

**Written:** 2026-09-23 local time (2026-09-22 UTC), by CC (subagent). **Revised (v1):**
2026-09-23, by CC (subagent), on Ark's review. The ids are now derived from the element's name.
**Status:** proposal for the genome track. The rule below is what `birth_ids.csv` implements.
Whether it is adopted is for the owner and the track to decide.

**Why this exists.** `literature.md` §I entry 18 (NEAT, Stanley and Miikkulainen 2002): crossing
two networks without a record of which gene is which damages the offspring. NEAT's fix is a
*historical marking*, a number given to every gene when it first appears and never changed.
"What this changes for us", item 3, says: every heritable element needs a birth id that is never
reused and never renumbered, and this has to be decided before the first genome is written. So
the ids are given here, on the bank itself, at generation zero.

## Revision v1 — 2026-09-23: ids are derived from the entity, not from a counter

**Why it changed** (Ark, DPC Research chat, 2026-09-23 20:10 UTC, translated from Russian and
paraphrased): the first registry numbered elements 1–670 in sort order. A re-extraction from
another flyvis version, or later from a second connectome, would sort a different list, silently
give different numbers to the same types and pairs, and crossing two banks would then match the
wrong homologues. Ark's rule: *the id is a function of the element's canonical name; a counter is
for display only.* This revision implements that. The earlier counter ids are kept as
`display_no`, and every earlier id maps to exactly one new id (checked by the migration in
`extract_bank.py`, see below).

## The rule

1. **Every heritable element has a birth id, and it is derived from the element itself.**

   | element | canonical string (UTF-8) | birth id |
   |---|---|---|
   | cell type | `cs-birth-v1\|type\|<name>` | first 12 hex digits of its sha256 |
   | ordered type pair | `cs-birth-v1\|pair\|<src name>-><tar name>` | first 12 hex digits of its sha256 |

   Example: `type:Mi1` has the id computed from `cs-birth-v1|type|Mi1`. `cs-birth-v1` is the
   rule's version tag. A different rule would carry a different tag, so its ids can never be
   confused with these.
2. **The function is defined for every ordered pair of the 65 × 65 grid**, not only the 605
   pairs the json lists. Cells that are not pairs of the bank are not registered elements (they
   have no row in `birth_ids.csv`), but their id is already fixed: if a mutation later creates
   the pair, it is born with the id its names give it. The C6 folds key on these ids for the
   empty cells too (`docs/plans/2026-09-23-c6-control-specification.md`, Amendment).
3. **Ids are never reused and never reassigned.** A name, once bound to an element, is never
   bound to a different element. If a later source uses an existing name for a different type,
   the newcomer must be given a qualified name (for example `Mi1#2`) before it gets an id.
4. **`display_no` is a counter for people, never a key.** Types are numbered by the Unicode code
   point of their name (`Am` = 1, `TmY9` = 65), then pairs by `(source, target)` code point
   (66–670). It equals the pre-v1 integer id. `next_display_no=671` is in the header of
   `birth_ids.csv`. Nothing may join, sort for identity, or cross on it.
5. **Changing a value does not create an element.** A sign flip, a new synapse count or a
   shifted offset changes the content of an element that already has an id, and the id stays.
   A *new* type, a *new* type pair, or a *duplicated* module is a new element and gets a new id.
   (This split is the proposal most likely to need revising once real operators exist. It is
   written down now so that it is not decided silently later.)
6. **The generation-zero root of the evolutionary tree is this registry.** Every later genome's
   elements trace back, through `parent_ids`, either to a row here or to a later birth.

**Elements born later, by operators.** A duplicated type does not have a name from a connectome.
Its canonical string must still be built only from things that identify it: the parent's id,
the operator, and the event that made it (for example
`cs-birth-v1|type|dup(<parent id>)@<lineage event id>`). The exact form is decided when the first
operator exists. What is fixed now: it must be a function of the element's own record, never of
a position in a list.

### Collisions

- **Checked, none.** `extract_bank.py` computes the id of all 65 types and all 4,225 ordered
  pairs of the grid (4,290 strings) and asserts they are distinct. They are. At 48 bits, the
  chance of any collision among 4,290 strings is about 3 × 10⁻⁸.
- **If one ever occurs** (a later, larger domain): the script stops. It does not truncate less,
  re-salt, or pick a winner silently. The fix is a new rule version with a longer id (for
  example `cs-birth-v2`, 16 hex digits), applied to every element at once and recorded here,
  with the v1 → v2 map kept like the counter → v1 map below.

### Renames

- A rename in a later source (for example another flyvis version calling a type by another
  name) would, under the bare function, produce a new id and orphan the old one. That is
  *visible*: the old id disappears and a new one appears. It is not a silent reassignment of
  someone else's number, which is what the counter did.
- **Policy:** the id is bound to the name the element had **at birth** (`birth_key`). A later
  name is recorded as an **alias** of that birth name, by hand and with its evidence. The alias
  is never inferred. Canonical strings always use the birth name, with aliases resolved first.
  So a pair keeps its id when one of its types is renamed.
- A tool that crosses two banks must stop on any name it cannot resolve to a birth name. It must
  not guess. The alias table does not exist yet, because no rename has happened.

### What was kept from generation zero

- **The content hash is only a record of birth.** `content_sha256` (sha256 of the element's json
  object, keys sorted, compact separators) records what the element *was* when it was born. The
  id is derived from the element's *name*, not from its content. Content is exactly what
  evolution changes, so an id derived from content would change with every mutation.
- **The unexpressed pair keeps its id.** `Lawf1>Lawf1` (`16031c360590`, display 198) is in the
  json but never appears in the compiled bank (see `README.md`). It is heritable and silent,
  like a pseudogene, and `expressed_in_compiled_bank=False` records that. If it were left out,
  a later mutation that made it land (for example a change of Lawf1's stride) would look like a
  new element when it is not.
- **Pair rows still name their two types by id** (`src_birth_id`, `tar_birth_id`), now as hex.

### The migration from counter ids, and the guard

`extract_bank.py` refuses to overwrite `birth_ids.csv` if its regenerated registry differs from
the one on disk. The one exception is the v1 migration. It runs only with the explicit flag
`--migrate-from-counter-ids`, and only if every old row maps to exactly one new row by
`birth_key`, the old integer equals the new `display_no`, and no other field of any row
changed. After writing, the script re-reads the registry and re-derives every id from its
`birth_key` alone.

Re-extraction after the change: `types.csv`, `type_pairs.csv`, `offsets.csv` and
`birth_ids.csv` are identical to the pre-v1 files in every non-id column and every row. Every
old id maps to its new id through `display_no`. The only other changes are the first `#` line of
each csv, which carries the script's sha256, and the `script`, `outputs` and `birth_ids` blocks
of `bank.meta.json`. `regularity.py` does not read ids. Re-run on the new files, its
`regularity_results.json` differs from the previous one only in the three recorded input hashes
and the run timestamp. Every measured value is identical.

## Offsets do not get ids of their own

An offset is addressed as **(pair birth id, du, dv)**, and it inherits its pair's id. The
reasons:

- **The address is already stable.** `(du, dv)` is a coordinate on the hex lattice, not a
  counter. Nothing can renumber it, so a second counter would add bookkeeping and no stability.
- **The substrate does not treat offsets as separately heritable units.** A pair has one sign
  and one trainable strength, shared by all its offsets
  (`docs/notes/2026-09-20-what-is-the-genome-here.md` §1). The offsets are the spatial kernel of
  one connection. They are not independent connections.
- **Crossover should not split a kernel.** Crossover matches homologous elements by id. Matching
  at offset level would let a child inherit half of one parent's kernel and half of the other's
  for the same pair. That is a variation operator someone might want, but it should be a
  deliberate choice, not a side effect of how the ids were cut.
- **Hull-filled offsets are phenotype, not genome.** The 238 `hull_filled` rows are produced by
  the decoder (`connectome.py` `fill_hull`, `n_syn_fill = 1`) from the json offsets. They are
  not inherited. They are regrown each time the genome is decoded. Only json offsets
  (`in_json` and `dropped`) are heritable content.

**When to revisit.** If a grammar makes offsets independently mutable modules, for example a
kernel motif that is duplicated and reused across pairs, then the *motif* is a new heritable
element and gets a birth id under rule 3. The per-pair offsets would still be addressed by
coordinate.

## The two readings (von Neumann, `literature.md` §I entry 31)

The test: a description has to be usable twice, in two different ways. It is *copied* without
being understood, to be inherited, and it is *interpreted*, to build the body. How the registry
and the bank pass it:

- **Copy, without interpretation.** `birth_ids.csv` and the three bank tables are plain UTF-8
  byte files. Their sha256 values are in `bank.meta.json`. Copying them is a byte copy, and a
  copier needs to know nothing about types, pairs or offsets. A copy is checked by comparing
  hashes, again without interpretation. The v1 ids change nothing here: they are 12 more
  characters of text.
- **Decode, separately.** `extract_bank.py` rebuilds the flyvis json from `types.csv`,
  `type_pairs.csv` and the json rows of `offsets.csv` (plus the constant fields listed in
  `bank.meta.json`). The rebuilt json is equal to the source element by element. The script then
  compiles the rebuilt json with flyvis's own `add_nodes` and `add_edges` at extent 5. The
  result equals the extent-15 compiled bank on all 2,355 `(source, target, du, dv)` keys, with
  identical `n_syn` and sign (`bank.meta.json` → `two_readings`). The decoder is flyvis, not
  this repository, so the second reading does not depend on the author of the first. The
  decoder does not read the ids, so the new ids cannot change this reading. It was re-run after
  the change and still passes.
- **What v1 adds: the ids survive both readings on their own.** A counter id survives a copy,
  but after decoding, nothing in the phenotype can recover it: it depended on where the element
  sat in a sorted list. A v1 id can be re-derived from what the decoded element carries, its
  name and, for a pair, its two types' names. The script checks this every run: it re-reads the
  written registry and recomputes every id from `birth_key` alone
  (`bank.meta.json` → `birth_ids.ids_rederived_from_birth_keys`). So the id is carried through
  decoding onto the element it names, which the test below asks of a grammar.
- **What the test does not show.** It shows that the *generation-zero description* passes. It
  says nothing about a grammar that does not exist yet. A grammar will have to pass the same test
  on its own genome, and the birth ids have to survive both readings with it: copied as data,
  and carried through decoding onto every element they name.
