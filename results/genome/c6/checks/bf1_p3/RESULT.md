# BF_1 alone: P3 against the 99 shuffled banks

Registration: `docs/plans/2026-09-24-bf1-p3-registration.md`. Machine check: True (this run 0.028150051052146 vs recorded 0.028150051052146, difference 0.00e+00).

## Existence (the decision field)

| real margin | shuffled mean | shuffled max | n shuffled >= real | p (one-sided) | gap (real - shuffled max) | branch |
|---|---|---|---|---|---|---|
| +0.02815 | -0.00033 | +0.00000 | 0 | 0.01 | +0.02815 | **A: BF_1 separates** |

## Other fields (reported, no reading -- 0 by construction, registration section 3)

| field | real margin | shuffled mean | shuffled max | n shuffled >= real | p |
|---|---|---|---|---|---|
| offset | +0.00000 | +0.00000 | +0.00000 | 99 | 1.00 |
| counts | +0.00000 | +0.00000 | +0.00000 | 99 | 1.00 |
| sign | +0.00000 | +0.00000 | +0.00000 | 99 | 1.00 |

n_shuffles=99, n_folds=10, starts_k=10, git_head=e3f17cbb74d00a2c5bb0156f54dc5bd0d8f42481, runtime=165.3s.
