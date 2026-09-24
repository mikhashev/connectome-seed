# The grammar track — where it stands, and the next three steps

**Written:** CC, 2026-09-23, for Mike. Plain-English summary; it decides nothing and reports no
measured result. The project's goal is the five points of `idea.md`; this page is about point 1,
the representation of the genome, which is the main line since ADR-004 and the only active line
since the measurement line was paused (Mike, 2026-09-20 10:15 UTC).

## What we have now

| piece | what it is, in one line | where | state |
|---|---|---|---|
| **The bank** | The fly's wiring as one table: for each pair of cell types, which offsets connect, with how many synapses and which sign. This is what a genome would have to regenerate. | `results/genome/bank/` | extracted (`results/genome/bank/README.md`) |
| **Birth ids** | A permanent id for each of the 65 cell types and each type pair, never reused — so that later, inherited pieces can be matched between parents and the family tree can be drawn. | `results/genome/bank/` | assigned (`results/genome/bank/birth_ids.csv`) |
| **Regularity measurement** | How much repeated structure the type-pair table has. A rule only pays off if there is enough of it (Clune et al. 2011). | `results/genome/bank/REGULARITY-READING.md` | done |
| **C6 control** | The exam a candidate rule has to pass, written *before* any rule exists so it cannot be bent to fit one. | `docs/plans/2026-09-23-c6-control-specification.md` | built and run; three rules tried (`results/genome/c6/README.md`) |
| **S2 design, amended** | Ark's design of what the genome track predicts and which labels may judge it, with the review's corrections recorded. | `docs/plans/2026-09-20-genome-design-around-s2.md` (§ Amendment — 2026-09-23) | amended; Ark to confirm |

## What the first candidate rule will be tested against

The rule is shown most of the table and must fill in **type pairs it has never seen** — whether
they connect, at which offsets, how strongly, with which sign. To pass, it must do three things
at once:

1. **Beat a simple "type averages" guess** — one that only knows how busy each cell type is. If
   the rule cannot beat that, it has learned nothing about how the types relate.
2. **Be much smaller than the table** (at most a tenth of its size), and do better than simply
   storing the same number of table entries directly. If the fly's wiring is not regular enough,
   storing entries wins; that is a real, publishable outcome, not an embarrassment.
3. **Lose its advantage when the table is shuffled.** If the rule does just as well on a scrambled
   fly, its success came from flexibility, not from the fly.

## Read before proposing a rule — `literature.md` §I.1

- **Sims 1994 (entry 9)** — one graph encodes body and brain and is read as growth instructions;
  the original, and it already has "graft a module from the other parent".
- **Hornby & Pollack 2001 (entry 10)** — L-systems: rewrite rules with re-use, and the constraints
  that kept them decodable.
- **CPPN (entry 11) and HyperNEAT (entry 12)** — a function of coordinates that outputs wiring;
  the existing baseline to beat. **Caveat (Ark):** it gives modules no identity, so there is
  nothing to inherit or splice (point 3), and nothing a birth id can attach to.
- **Clune et al. 2011 (entry 13)** — below a regularity threshold, a rule loses to a plain table.
  This is why the regularity measurement and C6 exist.

## The next three steps

| # | step | owner | GPU? |
|---|---|---|---|
| 1 | **Finish the bank:** extraction, birth ids, and the regularity reading — read *after* the C6 spec is committed, so the exam is fixed first. | CC (in progress) | No |
| 2 | **Build the C6 harness with no rule in it:** the fold file (keyed by birth ids, hashed and committed), the "type averages" guess, the size-matched stored table, the shuffled tables. Reviewed by Zcode before it is used. | CC; Zcode reviews | No |
| 3 | **Propose the first candidate rule**, after the §I.1 reading and with the regularity reading in hand, aimed at the type-pair table — and run it through C6. Needs your word, because a rule design is not yet licensed. | Proposer: your choice (Ark is the natural one); Mike licenses | No — the rule and C6 run on CPU. A GPU is needed only later, to check a regenerated fly actually works, and that waits on the measurement line resuming. |
