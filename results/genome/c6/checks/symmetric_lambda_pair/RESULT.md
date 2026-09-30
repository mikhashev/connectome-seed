# The symmetric pair: block A at lambda 100, block B's verdict at lambda 1 (post-data)

Registration: docs/plans/2026-09-30-symmetric-lambda-pair-registration.md, revision 1. Every AUC object is printed exact (tau).

git HEAD: b44d3836973602f32f7bd021d9f399ab5763b150. `git status --porcelain`: (empty).

## Object 1: branch of section 3.1

**(b) A would fail at lambda = 100 as B did**

cert_A >= 0.90 and ceil_100_A < 0.90: A would fail at lambda = 100 as B did: the A/B pair differs by the lambda choice, not shown to differ by the block.

Flags: none. Branch under the TAU reading: (b) A would fail at lambda = 100 as B did.

## Values

| object | exact | tau | pairs | levels |
|---|---|---|---|---|
| control ceiling_block, A at lambda 1 | 1.000000000000000 | 1.000000000000000 | 1024 | |
| cert_A | 1/1 = 1.000000 | 1.000000 | 1024 | |
| ceil_100_A | 0.500000 | 0.500000 | 1024 | 1 |
| ceil_100_A_float | 0.500000 | 0.500000 | 1024 | 1 |

cert counts agree: True; rerun spread 0.0. max |u.v| of the lambda = 100 fit on the block cells (diagnostic, decides nothing): 3.289222246986234e-19.

## Control (section 2)

ceiling_block of A at lambda = 1 = 1.0; expected 1.0; min gap between adjacent p levels 0.7500000437558088; p bit-equal to the store: True.

## Object 2: the reading (section 3.2), no fit

### Block B, block lambda at 1 (ceiling_block := ceil_1)

Label: **G**

G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = 0.9624 >= 0.90; gamma_R = 0.75 (bracket (0.6, 0.75]); leg P from gamma*_P = 0.75 (bracket (0.6, 0.75]); family limit = 0.75 (set by rule #2.1, BF_1, BF_2, BF_3, BF_4); transition band empty: the two limits coincide (0 grid steps, 0 in gamma); per gamma seen/n, R/n: 0.5: 1/5, 1/5; 0.6: 1/5, 1/5; 0.75: 4/5, 4/5; 0.85: 5/5, 5/5; 1.0: 5/5, 5/5; M-world units; instrument: BF_LAMBDAS [1, 3, 10, 30, 100], ties within 1e-9 go to the larger lambda (harness.py:727-728), STARTS = 10)

Deciding clause: G clause: not R and not W (rule #2.1 -> -, BF_1 -> -); every p_P > 0.10 (smallest: BF_4 0.2442); the gate is passed (rule #2.1's ceiling_block = 0.9624 >= 0.90).

Expected under the reading: G; as expected: True.

### Block A, block lambda at 100 (ceiling_block := ceil_100_A)

Label: **U**

U: failed fit: rule #2.1 cannot hold the block even when trained on it alone

Deciding clause: U clause: rule #2.1's ceiling_block = 0.5000 is below 0.90: the rule cannot hold the block even when trained on it alone. (The gate reads rule #2.1's ceiling_block = 0.5000; every p_P: rule #2.1 0.3288, BF_1 0.3837, BF_2 0.4912, BF_3 0.5119, BF_4 0.5042.)

### Pair table (the gate clause, both blocks, both lambdas)

| block | block lambda | ceiling_block | gate >= 0.90 | label |
|---|---|---|---|---|
| A | 1 | 1.0000 | True | G |
| A | 100 | 0.5000 | False | U |
| B | 1 | 0.9624 | True | G |
| B | 100 | 0.7744 | False | U |

### Lambda provenance of block B's stored verdict inputs

Selected lambda per predictor (knockout / full / block):

- rule: 1.0 / 1.0 / 100.0
- BF:1: 1.0 / 1.0 / 1.0
- BF:2: 1.0 / 3.0 / 1.0
- BF:3: 3.0 / 3.0 / 1.0
- BF:4: 3.0 / 3.0 / 1.0
- N1: None / None / None

Selected lambda of the 99 leg-S shuffle fits (count per lambda): {"rule": {"100": 97, "3": 2}, "BF:1": {"100": 97, "3": 2}, "BF:2": {"100": 99}, "BF:3": {"100": 99}, "BF:4": {"100": 98, "3": 1}}

## Inputs

- raw store sha256 3c20e837d07ebba10db20963712bf87a8633c410e8a483ac4b10d65c737e6006
- registration LF sha256 8865753ee1c7d9c946d434e08d7227c1f29ae0500fef6339f1b22e55fe507808
- this script LF sha256 1a084350251ce7ad212d45d26c7447471ec693c3e7f34f8d3121714ab99486da
- git HEAD b44d3836973602f32f7bd021d9f399ab5763b150
