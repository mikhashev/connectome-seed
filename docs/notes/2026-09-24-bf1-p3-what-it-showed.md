# BF_1 alone on P3: what the run showed

Registration: `docs/plans/2026-09-24-bf1-p3-registration.md` (reviewed version `e3f17cb`).
Script: `results/genome/c6/checks/bf1_p3.py` (unchanged since `211b6d0`). Outputs:
`results/genome/c6/checks/bf1_p3/` (`RESULT.md`, `summary.json`, `per_shuffle.csv`), committed
in `0f718b2`. The run started at 2026-09-24 06:38:07 UTC and ended at 06:40:53 UTC, at git head
`e3f17cb`, with 30 workers. It took 165.3 s. It ran once.

## 1. Registered outcome

- **Machine check passed.** The real-bank margin is 0.028150051052145946. The recorded
  `exam.P4.bf.margin` is the same, and the difference is 0.0 (`summary.json` `machine_check`).
- **Branch A: BF_1 separates** (`summary.json` `branch`).

| existence | value (`summary.json` `fields.existence`) |
|---|---|
| real margin | +0.02815 |
| shuffled mean | −0.00033 |
| shuffled max | +0.00000 |
| n shuffled ≥ real | 0 |
| strictly above all | true |
| p (one-sided) | 0.01 |
| gap (real − shuffled max) | +0.02815 |

Offset, counts and sign are 0 on every bank, as the registration's §3 said they would be by
construction. They carry no reading.

By the registration's §6, branch A means that **the rank-1 term alone is enough** to separate the
real bank from its degree-preserving shuffles on existence. The rule's separation does not *need*
X. The second brain (FlyWire) therefore tests **whether the rank-1 structure is bank-specific**.

## 2. The shape of the shuffled margins (read from `per_shuffle.csv`, not registered)

- Of the 99 shuffled banks, 66 give a margin of exactly 0.0, 33 give a negative margin
  (minimum −0.00234), and none give a positive one.
- At fold level, 943 of the 990 shuffled-bank fold margins are exactly 0.0, and none are positive.

**Why so many exact zeros: a post-hoc diagnostic, one bank and one fold, not registered.** On
shuffle 0, outer fold 0, the nested choice of λ in `fit_bf` picked λ = 100, the largest value in
`BF_LAMBDAS`. The fitted term shrank to max |U Vᵀ| = 6.1e−20, so it changes no prediction and
the margin is 0.0. On the real bank, same fold, the choice was λ = 1 and max |U Vᵀ| = 4.54 logit
units. So on a shuffled bank, BF_1's own cross-validation usually finds nothing worth fitting and
falls back to N1. The negative margins are the folds where a smaller λ was picked and the term
fitted noise. The run did not record the λ chosen for each shuffled fold, so how often λ = 100 was
picked is not known beyond the one fold checked.

What this means for reading branch A: the separation is not a close call. Nothing on a shuffled
bank came near the real margin, and the reason is that the real residual `Y − sigmoid(N1)` holds
a rank-1 pattern that nested cross-validation accepts, while a shuffled residual holds none it
accepts.

## 3. What this run does not show

- **Whether X alone would also separate.** This run did not test that. Branch A says only that
  the rule's separation does not need X.
- **The rank-1 term inside the rule.** BF_1 here was fitted on its own on top of N1. Inside
  rule #2.1 the rank-1 term is fitted jointly with X, so it is not the same fitted object
  (registration §6, caveat).
- **A different brain.** The bank is still the flyvis FIB-25/FIB-19 type-level template: two
  female flies, column-averaged and merged. Whether the rank-1 pattern is a property of fly wiring
  or of this template is the question for the second brain.
- **A distribution.** This is one deterministic fit per bank, with fixed seeds.

## 4. Next step (by the registration, pending Mike's word)

The second brain (FlyWire right optic lobe, 48 of 65 types matched) gets its own registration,
and its question is now named: does BF_1, fitted on that bank, separate it from its own
degree-preserving shuffles on the matched types?
