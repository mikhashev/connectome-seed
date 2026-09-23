# C6 run: first_rule_k12

**C6 verdict for first_rule_k12 (k = 10 starts, r = 12): FAIL -- rule did not run; copy or marginal; below threshold for this family; family fits anything; ambient, not substantive structure**

Verdict labels are the spec's (section 5.2, A11), verbatim. Every number below is at k = 10 starts per trained fit and rank r = 12.

| stamp | value |
|---|---|
| git_head | `89683c68eab8858d90414a9afe5fadc8a9d977ee` |
| tree_dirty_under_c6_or_plans | `False` |
| harness_sha256_lf | `c01cd9eb02481132a0d254ffe63e90a655e79979112d620207ce39c75bdfbd86` |
| spec_sha256_lf | `5c58b02a53021f5a9d3ec5090e56dc183fb567568dfc1eda86e74ae8e28e7abd` |
| acceptance_sha256_lf | `['bd3697719aa96a2d6c39078d7d01823009746de50b694debecc0f0d450b43d3b', '4b6610e7ed30b6aaeccf6ea33008485fc3ec31a1869b93f74c78b7248f2e97f9', '16432647ffc568c2a3cb77bc61459abe8df50902ca945badf97fc20be9e2ac9f']` |
| folds_sha256_lf | `fb6f153b67fe1785a76c3823911e6fbb91cdda57ec952b36c40b4c95f1e213b8` |
| rule_file | `results/genome/c6/rules/first_rule/fit.py` |
| rule_file_sha256_lf | `b8da3b408944e777158b5d7f6640ad96bae3d0b890e1607752161c159d46d40e` |
| starts_k | `10` |
| rank_r | `12` |
| results/genome/c6/rules/first_rule/decode.py | `e7b4e7eb49936503578f042100c7e6b72ebf0d2e670be0e8151c9024031277c7` |

Wall time: 880.2 s with 30 workers.

## P1 (held-out, mean over 10 folds; k = 10)

| field | rule | N1 | N0 | N_EB | rule's fold wins / losses | pass |
|---|---|---|---|---|---|---|
| existence | 0.3670 | 0.3625 | 0.4103 | 0.3625 | wins vs N1 5 | False |
| offset | 0.4449 | 0.4204 | 0.4465 | 0.4842 | wins vs {'N1': 5, 'N0': 0, 'N_EB': 1} | False |
| counts | 1.0539 | 0.9861 | 1.0157 | 0.9076 | losses 10, mean not worse False | False |
| sign | 0.9768 | 0.9768 | 0.6225 | 0.9768 | losses 0, mean not worse True | True |

## P2 (in-sample; k = 10)

DL(rule) = 6992 bits (program 4440); limit DL(bank)/10 = 9481.2; length ok: True. k* = 0, k*_armed = 0.

| field | rule | D_k^N1 at k* | D_k^N0 at k*_armed | N1 | beats all three |
|---|---|---|---|---|---|
| existence | 0.2547 | 0.3354 | 0.4103 | 0.3354 | True |
| offset | 0.4368 | 0.4961 | 0.4467 | 0.4961 | False |

## P3 (margin over N1: real bank vs 99 shuffled banks)

| field | real margin | shuffled mean | shuffled max | shuffled >= real | one-sided p |
|---|---|---|---|---|---|
| existence | -0.0045 | -0.0643 | -0.0436 | 0 | 0.01 |
| offset | +0.0245 | +0.0425 | +0.0627 | 97 | 0.98 |
| counts | -0.0677 | -0.0381 | -0.0124 | 99 | 1.00 |
| sign | +0.0000 | +0.0000 | +0.0000 | 99 | 1.00 |

P3 passes (existence and offset strictly above all 99): False

## P4 (existence margin over N1, held-out; k = 10, r = 12)

rule -0.0045; random-projection threshold -0.0020; BF_r margin +0.0485 (lambda per fold [3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0]); threshold +0.0485; pass False.

## Did not run check

folds where N0 beats the rule: {'existence': 2, 'offset': 1, 'counts': 10, 'sign': 0}; did not run: True


## Attempts

1. **First attempt, crashed.** Harness at commit `958a976`, the same command. It crashed at
   44.9 s during the precompute with `FileNotFoundError: [Errno 2] No such file or directory:
   'results/genome/c6/rule_runs/first_rule/spread.jsonl'`: the rule's spread-log directory did
   not exist. The crash came before any verdict. **No outputs were produced or seen.** The
   directory was created and committed in `89683c6`.
2. **Second attempt, this record.** HEAD `89683c6`, clean tree, the same command, run once.
   Wall time 880.2 s with 30 workers.

## Spread-log validation

The rule writes one line per fit to `results/genome/c6/rule_runs/first_rule/spread.jsonl`.

| check | value |
|---|---|
| lines | 1,340 |
| lines that do not parse as JSON | 0 |
| rule fits the harness made | 1,341 (1,250 cross-validation + 65 leave-one-type-out + 26 in-sample) |
| line count equals fits | **no** (one fewer) |

**The spread log is marked unreliable.** The verdict above stands. The cause of the missing line
is not investigated, because that would need the rule's code, which the corrector has not read.
Details: `spread_log_validation.json`.

This record's outputs are in `rule_runs/first_rule_k12/`, named after the rule's `NAME`. The
spread log is in `rule_runs/first_rule/`, where the rule's run command put it.

## 2026-09-23 UTC — multiplicity caveat on P3's existence p-value

P3's existence one-sided p = 0.01 (table above: real margin -0.0045, strictly above all 99
shuffled margins, shuffled max -0.0436) is one of four fields tested (existence, offset, counts,
sign) with no correction for multiplicity. With four fields, a Bonferroni-adjusted p would be
**min(1, 4 x 0.01) = 0.04**. With 99 shuffles, the minimum attainable one-sided p is 1/100 =
0.01 (a real value strictly beating all 99 shuffles), so no field in this run could have passed
a corrected 0.01 bar, whatever its true effect: the shuffle count itself puts the floor at 0.01
per field, and Bonferroni over four fields puts the corrected floor at 0.04.

This does not change the FAIL verdict recorded above (P3 already reads "passes: False", since
offset and counts do not separate). It bears on how much weight the existence result (p = 0.01
uncorrected) can carry on its own when read as a single number, ahead of choosing a second rule.
