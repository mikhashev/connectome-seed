# The seal of male block A was broken before this arm's verdict

The first registered run of the male CNS arm (head `01d2d05`, 2026-09-26) unsealed both lobes'
block A at 23:25:55 UTC, after every gate had passed, and then stopped on an output-encoding error
(`UnicodeEncodeError`, cp1252 stdout on Windows) before writing its outputs. Its log is committed
beside this note as `run1_20260926T192234Z.stdout.log`.

Seen before the second run: check 3 for both lobes (the male block is flyvis's board, the same in
both lobes) and lobe L's verdict line (G). Lobe R was not seen by anyone.

The second run is made with the same script (LF sha256
`290ecb565759def6d11e3b76811635ce033a6b008461427ecede4704245e8e32`, unchanged since `01d2d05`;
this note first gave `1b952ca6…`, the hash before `01d2d05` set A's amended hash in it)
and `PYTHONUTF8=1`, on Mike's word (DPC Research chat, 2026-09-27 07:14 UTC), option (a) of the
reviewers (Ark 2026-09-26 23:35, Zcode 2026-09-27 05:43 UTC). Every verdict in this folder is to be
read with this note. The full record is in the registration,
`docs/plans/2026-09-26-knockout-regrow-male-cns-arm-registration.md`, section 11.

## The second run (2026-09-27, head `e07e347`, 07:16–11:32 UTC)

Checks against the first run, registered before it ran (registration section 11):

1. Each lobe's synthetic store, fit by fit (28,665 keys per lobe; `lam`, `outside_density`, `p`,
   `reused_from_ko`, `score`, `y`): 0 keys missing, 0 fields differ, in both lobes; the worlds
   tables are byte-identical (L `506576…`, R `e8476a…`).
2. Lobe L's table and verdict line: identical to the first run's printed lines (31 lines, `diff`
   empty); both lobes' check 3 lines identical.
3. Lobe R: no base in the first run; its numbers here are a first measurement.

Result: lobe L G, lobe R G; male reading G in both lobes; block difference S0 (k = 0); joint
reading with flyvis-65's G: agreement, with the registered caution that the male R's power is not
calibrated and this G does not by itself exclude averaging.
