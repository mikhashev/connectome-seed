# C6 run: second_rule_v21_r1

**C6 verdict for second_rule_v21_r1 (k = 10 starts, r = 1): FAIL -- copy or marginal; below threshold for this family; family fits anything**

<!-- second-rule post-run: start -->

Spread log: 1341 per-fit files for 1341 rule fits; all parse.

**Margins against BF_1-BF_4 (mandatory; k = 10):** rule margin over N1 +0.03378. rule - BF_1 = +0.00563 (BF_1 +0.02815) **the decision**; rule - BF_2 = +0.00555 (BF_2 +0.02823) context only; rule - BF_3 = -0.00656 (BF_3 +0.04034) context only; rule - BF_4 = -0.00595 (BF_4 +0.03972) context only.

**P4 tie band (registered):** Delta = rule margin - P4 threshold = +0.00563 (threshold +0.02815); reading: **passed (Delta > +0.002)**. Harness P4 pass: True.

**Interpretation lines (registration of rule #2.1, section 6; part of the record, cannot be dropped):**

1. **What the bank is.** The bank is flyvis's **FIB-25/FIB-19 type-level template** (Lappalainen et al. 2024). It holds mean synapse counts per (type pair, offset), **averaged over columns**, and it **merges two female flies by taking the larger of two estimates** (their equation 7). It is not one animal's wiring and holds no per-neuron weight. Source: `docs/notes/2026-09-23-where-our-bank-comes-from.md` sections 2-3. So any outcome answers "is a type-level template compressible?", not "is an individual brain compressible?".
2. **Column averaging is not between-individual stability.** Averaging removes the variation between columns inside one reconstruction. It does not show that the template is what carries over between flies. That stays plausible but unmeasured, and the bank cannot express between-fly variation (the same note, section 3).
3. **Many signs rest on personal communications.** 368 of 432 sign-citation slots (85 %) are personal communications, and 232 of the 272 `alpha_fixed` entries rest only on them (`results/genome/bank/README.md`, "Warning: most sign citations are personal communications", from `sign_citations`). The rule's sign is N1's by construction, so this bears on what the sign field means, not on the rule's sign margin.
4. **The family choice was informed** (the rule #2 proposal's section 3 caveat, carried over). Rule #2's family was chosen by an author who had seen rule #1's real-bank results and whole-bank regularity numbers. That caveat travels with any rule #2.1 result.

S2-8 paired read: Delta = rule - BF_1 = +0.00563, paired SE 0.00156, real-amount bar 0.00500; Delta >= bar: a real amount.

Reproduction checks: bf1_matches_record True; rp_max_matches_record True; loto_means_match_record True; bf3_reproduces_controls True; bf4_reproduces_controls True.
Written by `rules/second_rule_v21/post_run.py` after the record was committed; details in `post_run.json`.

<!-- second-rule post-run: end -->

Verdict labels are the spec's (section 5.2, A11), verbatim. Every number below is at k = 10 starts per trained fit and rank r = 1.

| stamp | value |
|---|---|
| git_head | `e243a41ca483128c03be99c0b7805cfc705f35ce` |
| tree_dirty_under_c6_or_plans | `False` |
| harness_sha256_lf | `6fc809527c69ee84aadebfc15c0ba755c189ddc93c80c05c0fa11d969a8d7297` |
| spec_sha256_lf | `5c58b02a53021f5a9d3ec5090e56dc183fb567568dfc1eda86e74ae8e28e7abd` |
| acceptance_sha256_lf | `['bd3697719aa96a2d6c39078d7d01823009746de50b694debecc0f0d450b43d3b', '4b6610e7ed30b6aaeccf6ea33008485fc3ec31a1869b93f74c78b7248f2e97f9', '16432647ffc568c2a3cb77bc61459abe8df50902ca945badf97fc20be9e2ac9f']` |
| folds_sha256_lf | `fb6f153b67fe1785a76c3823911e6fbb91cdda57ec952b36c40b4c95f1e213b8` |
| rule_file | `results/genome/c6/rules/second_rule_v21/fit.py` |
| rule_file_sha256_lf | `92eb6ab1524bb22379b2d21184d10f493ff4c803a41918be8ee16f389a58d16c` |
| starts_k | `10` |
| rank_r | `1` |
| results/genome/c6/rules/second_rule_v21/decode.py | `39a049013af18a1e89e534d9d378a5f59a772b894d7fab5b79f82f702723a15a` |

Wall time: 585.1 s with 30 workers.

## P1 (held-out, mean over 10 folds; k = 10)

| field | rule | N1 | N0 | N_EB | rule's fold wins / losses | pass |
|---|---|---|---|---|---|---|
| existence | 0.3287 | 0.3625 | 0.4103 | 0.3625 | wins vs N1 10 | True |
| offset | 0.4685 | 0.4204 | 0.4465 | 0.4842 | wins vs {'N1': 9, 'N0': 8, 'N_EB': 3} | False |
| counts | 0.9204 | 0.9861 | 1.0157 | 0.9076 | losses 0, mean not worse True | True |
| sign | 0.9768 | 0.9768 | 0.6225 | 0.9768 | losses 0, mean not worse True | True |

## P2 (in-sample; k = 10)

DL(rule) = 9217 bits (program 3904); limit DL(bank)/10 = 9481.2; length ok: True. k* = 0, k*_armed = 6.

| field | rule | D_k^N1 at k* | D_k^N0 at k*_armed | N1 | beats all three |
|---|---|---|---|---|---|
| existence | 0.2779 | 0.3354 | 0.4075 | 0.3354 | True |
| offset | 0.4762 | 0.4961 | 0.4482 | 0.4961 | False |

## P3 (margin over N1: real bank vs 99 shuffled banks)

| field | real margin | shuffled mean | shuffled max | shuffled >= real | one-sided p |
|---|---|---|---|---|---|
| existence | +0.0338 | -0.0007 | +0.0008 | 0 | 0.01 |
| offset | +0.0481 | +0.0421 | +0.0622 | 24 | 0.25 |
| counts | +0.0657 | +0.0104 | +0.0243 | 0 | 0.01 |
| sign | +0.0000 | +0.0000 | +0.0000 | 99 | 1.00 |

P3 passes (existence and offset strictly above all 99): False

## P4 (existence margin over N1, held-out; k = 10, r = 1)

rule +0.0338; random-projection threshold +0.0010; BF_r margin +0.0282 (lambda per fold [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]); threshold +0.0282; pass True.

## Did not run check

folds where N0 beats the rule: {'existence': 0, 'offset': 2, 'counts': 0, 'sign': 0}; did not run: False

