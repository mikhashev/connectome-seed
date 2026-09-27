# The seal of male block A was broken before this arm's verdict

The first registered run of the male CNS arm (head `01d2d05`, 2026-09-26) unsealed both lobes'
block A at 23:25:55 UTC, after every gate had passed, and then stopped on an output-encoding error
(`UnicodeEncodeError`, cp1252 stdout on Windows) before writing its outputs. Its log is committed
beside this note as `run1_20260926T192234Z.stdout.log`.

Seen before the second run: check 3 for both lobes (the male block is flyvis's board, the same in
both lobes) and lobe L's verdict line (G). Lobe R was not seen by anyone.

The second run is made with the same script (LF sha256
`1b952ca6aca7c5026061a5db21e27aef2176ecd255e8c19f4b658437495af7a9`, unchanged since `01d2d05`)
and `PYTHONUTF8=1`, on Mike's word (DPC Research chat, 2026-09-27 07:14 UTC), option (a) of the
reviewers (Ark 2026-09-26 23:35, Zcode 2026-09-27 05:43 UTC). Every verdict in this folder is to be
read with this note. The full record is in the registration,
`docs/plans/2026-09-26-knockout-regrow-male-cns-arm-registration.md`, section 11.
