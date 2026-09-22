# Birth-id registry: generation zero

**Written:** 2026-09-23 local time (2026-09-22 UTC), by CC (subagent). **Status:** proposal for
the genome track. The rule below is what `birth_ids.csv` already implements. Whether it is
adopted is for the owner and the track to decide.

**Why this exists.** `literature.md` §I entry 18 (NEAT, Stanley and Miikkulainen 2002): crossing
two networks without a record of which gene is which damages the offspring. NEAT's fix is a
*historical marking*, a number given to every gene when it first appears and never changed.
"What this changes for us", item 3, says: every heritable element needs a birth id that is never
reused and never renumbered, and this has to be decided before the first genome is written. So
the ids are given here, on the bank itself, at generation zero.

## The rule

1. **Every heritable element has a birth id.** It is a positive integer, drawn from one global
   counter shared by all kinds of element, as NEAT does with innovation numbers.
2. **Ids are never reused and never renumbered.** When an element is lost in some lineage, its
   id is retired, not given back. Nothing is ever compacted or re-sorted.
3. **A new element gets the next id.** The next free id is written in the header of
   `birth_ids.csv` (`next_birth_id=671`). A new row carries the generation it appeared in and
   the ids of the elements it came from (`parent_ids`), for example the type a duplicated type
   was copied from.
4. **Changing a value does not create an element.** A sign flip, a new synapse count or a
   shifted offset changes the content of an element that already has an id, and the id stays.
   A *new* type, a *new* type pair, or a *duplicated* module is a new element and gets a new id.
   (This split is the proposal most likely to need revising once real operators exist. It is
   written down now so that it is not decided silently later.)
5. **The generation-zero root of the evolutionary tree is this registry.** Every later genome's
   elements trace back, through `parent_ids`, either to a row here or to a later birth.

## How generation zero was numbered

- **Types first (ids 1–65).** Sorted by the Unicode code point of the type name (`Am` = 1,
  `TmY9` = 65).
- **Then type pairs (ids 66–670).** One per json edge entry, sorted by `(source name, target
  name)` code point. Each pair row also holds the birth ids of its source and target type
  (`src_birth_id`, `tar_birth_id`). So a pair is anchored to its two types' ids, not to their
  names.
- **Why sort by name.** The sort does not depend on the json's row order, on the connectome's
  node order, or on any index flyvis computes. It depends only on the names, and the names are
  fixed at generation zero. Anyone holding the same json gets the same 670 ids, whatever order
  they read it in.
- **The content-derived key is only for birth.** `birth_key` (`type:Mi1`, `pair:Mi1>Tm3`) and
  `content_sha256` (sha256 of the element's json object, keys sorted, compact separators) record
  what the element *was* when it was born. After birth the id is a name, not a description. It
  is never recomputed from content, because content is exactly what evolution changes.
- **The unexpressed pair keeps its id.** `Lawf1>Lawf1` (id 198) is in the json but never
  appears in the compiled bank (see `README.md`). It is heritable and silent, like a pseudogene,
  and `expressed_in_compiled_bank=False` records that. If it were left out, a later mutation that
  made it land (for example a change of Lawf1's stride) would look like a new element when it is
  not.

`extract_bank.py` refuses to overwrite `birth_ids.csv` if its regenerated registry differs from
the one on disk. Generation zero can be re-derived, but it cannot be silently renumbered.

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
  hashes, again without interpretation.
- **Decode, separately.** `extract_bank.py` rebuilds the flyvis json from `types.csv`,
  `type_pairs.csv` and the json rows of `offsets.csv` (plus the constant fields listed in
  `bank.meta.json`). The rebuilt json is equal to the source element by element. The script then
  compiles the rebuilt json with flyvis's own `add_nodes` and `add_edges` at extent 5. The
  result equals the extent-15 compiled bank on all 2,355 `(source, target, du, dv)` keys, with
  identical `n_syn` and sign (`bank.meta.json` → `two_readings`). The decoder is flyvis, not
  this repository, so the second reading does not depend on the author of the first.
- **What the test does not show.** It shows that the *generation-zero description* passes. It
  says nothing about a grammar that does not exist yet. A grammar will have to pass the same test
  on its own genome, and the birth ids have to survive both readings with it: copied as data,
  and carried through decoding onto every element they name.
