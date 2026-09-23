# C6 run: standin-PR

**C6 verdict for standin-PR (k = 10 starts, r = 4): FAIL -- rule did not run; copy or marginal; below threshold for this family; family fits anything; ambient, not substantive structure**

Verdict labels are the spec's (section 5.2, A11), verbatim. Every number below is at k = 10 starts per trained fit and rank r = 4.

| stamp | value |
|---|---|
| git_head | `402e6c22652f0a904ca950fc213ec01c20dfbc63` |
| tree_dirty_under_c6_or_plans | `True` |
| harness_sha256_lf | `c01cd9eb02481132a0d254ffe63e90a655e79979112d620207ce39c75bdfbd86` |
| spec_sha256_lf | `5c58b02a53021f5a9d3ec5090e56dc183fb567568dfc1eda86e74ae8e28e7abd` |
| acceptance_sha256_lf | `['bd3697719aa96a2d6c39078d7d01823009746de50b694debecc0f0d450b43d3b', '4b6610e7ed30b6aaeccf6ea33008485fc3ec31a1869b93f74c78b7248f2e97f9', '16432647ffc568c2a3cb77bc61459abe8df50902ca945badf97fc20be9e2ac9f']` |
| folds_sha256_lf | `fb6f153b67fe1785a76c3823911e6fbb91cdda57ec952b36c40b4c95f1e213b8` |
| rule_file | `results/genome/c6/rule_runs/_standin/fit.py` |
| rule_file_sha256_lf | `23641d42189e61c5dca173a0d89c8ba1debea4be560752b9207a1d5f3cb6487b` |
| starts_k | `10` |
| rank_r | `4` |
| results/genome/c6/decoders/planted_decode.py | `56cf9fd3e5d18661136c5c66dd2159641161dd2e1ebd527561161bf6578c3d77` |

Wall time: 45.4 s with 30 workers.

## P1 (held-out, mean over 10 folds; k = 10)

| field | rule | N1 | N0 | N_EB | rule's fold wins / losses | pass |
|---|---|---|---|---|---|---|
| existence | 0.4100 | 0.3625 | 0.4103 | 0.3625 | wins vs N1 0 | False |
| offset | 0.4400 | 0.4204 | 0.4465 | 0.4842 | wins vs {'N1': 5, 'N0': 0, 'N_EB': 1} | False |
| counts | 1.0207 | 0.9861 | 1.0157 | 0.9076 | losses 10, mean not worse False | False |
| sign | 0.7072 | 0.9768 | 0.6225 | 0.9768 | losses 10, mean not worse False | False |

## P2 (in-sample; k = 10)

DL(rule) = 4448 bits (program 2912); limit DL(bank)/10 = 9481.2; length ok: True. k* = 0, k*_armed = 0.

| field | rule | D_k^N1 at k* | D_k^N0 at k*_armed | N1 | beats all three |
|---|---|---|---|---|---|
| existence | 0.4064 | 0.3354 | 0.4103 | 0.3354 | False |
| offset | 0.4467 | 0.4961 | 0.4467 | 0.4961 | False |

## P3 (margin over N1: real bank vs 99 shuffled banks)

| field | real margin | shuffled mean | shuffled max | shuffled >= real | one-sided p |
|---|---|---|---|---|---|
| existence | -0.0476 | -0.0483 | -0.0448 | 28 | 0.29 |
| offset | +0.0196 | +0.0425 | +0.0627 | 99 | 1.00 |
| counts | -0.0346 | +0.0177 | +0.0307 | 99 | 1.00 |
| sign | -0.2697 | +0.0431 | +0.1024 | 99 | 1.00 |

P3 passes (existence and offset strictly above all 99): False

## P4 (existence margin over N1, held-out; k = 10, r = 4)

rule -0.0476; random-projection threshold +0.0012; BF_r margin +0.0397 (lambda per fold [3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0]); threshold +0.0397; pass False.

## Did not run check

folds where N0 beats the rule: {'existence': 4, 'offset': 3, 'counts': 6, 'sign': 1}; did not run: True

