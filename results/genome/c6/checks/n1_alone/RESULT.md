# N1-alone existence-separation check

Answers the handover question (`docs/briefs/2026-09-23-next-session-handover.md` §3 step 0):
does N1 by itself (not the rule's margin over N1) separate the real bank from the 99 shuffled
banks on existence?

Registration commit: `ae89705972728c22f9e892abe8b0daee1a8ba07d`
(`docs/plans/2026-09-23-n1-alone-check-registration.md`), committed before this script ran.

Command:

```
tools/.venv/Scripts/python.exe results/genome/c6/checks/n1_alone.py
```

CPU, single process, 24.3 s. Deterministic (N1's fit has no random starts; shuffle seeds are
`range(99)`, the same seeds `make_env`/P3 use).

## Table (real vs. 99 shuffles, N1's own held-out score, mean over 10 folds)

| field | lower is better | real | shuffled min | shuffled mean | shuffled max | n shuffled >= real | one-sided p | separates |
|---|---|---|---|---|---|---|---|---|
| existence | yes | 0.36248 | 0.35938 | 0.36234 | 0.36564 | 56 | 0.57 | **no** |
| offset | no | 0.42040 | 0.38254 | 0.40368 | 0.42210 | 2 | 0.03 | no |
| counts | yes | 0.98614 | 1.01534 | 1.03664 | 1.05410 | 0 | 0.01 | yes |
| sign | no | 0.97683 | 0.51954 | 0.57910 | 0.63701 | 0 | 0.01 | yes |

"n shuffled >= real" and "separates" use the field's own direction (existence/counts:
lower-is-better, so "at least as good" means <= real; offset/sign: higher-is-better, so "at
least as good" means >= real). "separates" = real strictly better than all 99 shuffles
(p = 0.01), the same bar P3 uses for its own pass condition.

## Verdict, per the registered decision rule

**Decision field is existence. N1 does not separate the real bank from the 99 shuffled banks on
existence** (p = 0.57; 56 of 99 shuffles are as good as or better than real; real sits inside the
shuffled range, close to the shuffled mean).

What this means, per the handover's step 0 (corrected by CC in the commit after `3b65f7d`; the
registration's branch text swaps the handover's two readings. Its decision rule and its
prediction are unaffected, and the registration is left as committed):

- N1 is a per-node model and the shuffle preserves per-node degree exactly, so N1 scoring the
  same on real and shuffled banks is what a degree-only model should do. N1 alone does **not**
  explain the first run's P3 existence result.
- That P3 result (the rule's margin over N1: real -0.0045, strictly above all 99 shuffled margins,
  max -0.0436, p = 0.01) therefore reflects structure in the real bank that is **beyond degree**
  and that the shuffle destroys: on the real bank the rule comes close to N1, while on shuffled
  banks it falls well below N1.
- Handover branch "N1 does not separate": a **non-marginal structure exists**, and the next rule
  should model the **residual after the marginal (N1) model** rather than compete with N1 on raw
  existence. This does not make a second rule pointless. It says what the second rule should
  aim at.
- Caveats that still apply: the P3 p = 0.01 is one of four fields with no multiplicity
  correction (handover step 1), and the first rule's margin is still negative on held-out data
  (P1 existence 0.3670 vs N1 0.3625).

Offset, counts and sign are reported descriptively only, per the registration (the verdict above
is stated for existence). Counts and sign do separate (p = 0.01 each); offset does not (p = 0.03,
2 of 99 shuffles at least as good as real).

## Consistency check against `harness_controls.json`

`results/genome/c6/harness_controls.json`'s `control_d_shuffled_banks` (from an independent code
path, the harness's own `controls()`, run separately under `--controls`) already carried the
aggregate form of the existence and offset numbers above (real value and shuffled
min/mean/max, no per-shuffle breakdown). This run's `summary.json` reproduces those four numbers
exactly:

| quantity | harness_controls.json | this run | match |
|---|---|---|---|
| N1 existence real | 0.362476 | 0.362476 | yes |
| N1 existence shuffled min/mean/max | 0.359376 / 0.362336 / 0.365642 | 0.359376 / 0.362336 / 0.365642 | yes |
| N1 offset real | 0.420403 | 0.420403 | yes |
| N1 offset shuffled min/mean/max | 0.382539 / 0.403682 / 0.422097 | 0.382539 / 0.403682 / 0.422097 | yes |

No mismatch found (`summary.json`'s `consistency_check_vs_harness_controls_json.all_match =
true`). This is why the registration could predict the existence verdict before running the
per-shuffle script: the aggregate check already showed real inside the shuffled range.

## Shuffle mechanism, for reference

`harness.shuffled_bank` (`results/genome/c6/harness.py`, `rewire_and_permute` /
`shuffled_bank`) does a degree-preserving double-edge swap (`SWAPS_PER_EDGE = 20` attempted swaps
per edge) over the full set of non-empty (source, target) cells, then permutes the *content*
(offsets/hull/sign) across the swapped edges. Verified invariants, checked again by this script
for all 99 shuffles before scoring: `out_degrees_kept` and `in_degrees_kept` both `True` (exact
per-node row/column sums of the 65x65 existence matrix), `content_multiset_kept` `True` (the same
bag of edge contents, relocated). `fit_n1`'s existence arm is a ridge-logistic regression on
per-source-node and per-target-node one-hot indicators only -- i.e., a per-node-identity model,
closely tied to per-node degree, which the shuffle preserves exactly at the full-matrix level.
That mechanism is why real and shuffled N1 existence scores land close together (not identical:
the shuffle preserves full-matrix degree, not the per-fold train/held-out split of it, and the
fit is ridge-penalized).

Outputs: `per_shuffle.csv` (100 rows: real + 99 shuffles; per-field mean score and per-fold
existence values), `summary.json` (this table's numbers, git HEAD, file hashes, consistency
check).

## 2026-09-23 UTC — by-construction limitation (Ark, DPC Research group, 2026-09-23 09:02 UTC)

This check cannot, by construction, distinguish "structure beyond degree exists" from "the bank
is fully described by degree": the shuffle keeps per-node degree exactly and N1 uses only
per-node indicators, so N1 not separating is the predicted outcome in both worlds.
