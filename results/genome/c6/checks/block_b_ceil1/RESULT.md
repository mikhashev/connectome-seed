# Block B, real block: ceil_1 and cert (post-data)

Registration: docs/plans/2026-09-30-block-b-ceil1-registration.md, revision 1. Every AUC object is printed exact (tau).

## Branch (section 3)

**(c) FF-sel on the real block**

cert >= 0.90, ceil_1 >= 0.90 and ceil_1_float >= 0.90: FF-sel on the real block; the U is the lambda choice; the word 'cannot' in B's label is wider than the measurement.

Flags: none. Branch under the TAU reading: (c) FF-sel on the real block.

## Values

| object | exact | tau | pairs | levels |
|---|---|---|---|---|
| control ceiling_block (lambda 100) | 0.774436090225564 | 0.774436090225564 | 399 | |
| cert | 132/133 = 0.992481 | 0.992481 | 399 | |
| ceil_1 | 0.962406 | 0.962406 | 399 | 35 |
| ceil_1_float | 0.959900 | 0.959900 | 399 | 35 |
| ceil_1_starts100_float | 0.959900 | 0.959900 | 399 | 35 |
| ceil_1_starts100_quantised | 0.962406 | 0.962406 | 399 | 35 |

cert counts agree: True; rerun spread 0.0; ceil_1_starts100 is a diagnostic and decides nothing.

## Control (section 2)

ceiling_block at lambda = 100 = 0.7744360902255639; expected 0.7744360902255639; min gap between adjacent p levels 0.0032461317507782583; p bit-equal to the store: True.

## Inputs

- raw store sha256 2461d921048b39479926878a9761aaf34bb4c5bedfc8a9e1c17882fd4ee398c6
- registration LF sha256 bea61287c426dd893deb1a331a8e24f4d525b22a2299b121b1f061d055ed2e5b
- this script LF sha256 e4b85ff168f33614c8bb7c9132267054024153752bac26dc50d1263d6355391b
