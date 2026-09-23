---
**Status:** REGISTERED. Reviewed by Zcode (rule side), Ark and Johnny (exam side) in the group chat,
2026-09-23 19:13–19:25 UTC; their edits applied. **S1 and W1 are committed in the git commit that
adds this file** (a file cannot carry its own hash; `git log --follow` on this path gives it). The single re-gate on the reserved seeds runs only after
that commit, and no gate or re-gate result for rule #2.1 exists before it** (Johnny, group chat,
2026-09-23 18:55 UTC, as relayed by the coordinator).
**What it is:** an **amendment** to the registered rule #2 proposal,
[`docs/plans/2026-09-23-second-rule-proposal.md`](2026-09-23-second-rule-proposal.md) (commit
`c3f996d`). That proposal **stays the governing text for everything this file does not change**.
Where the two disagree, this file governs. The proposal itself is not edited.
**Decided by:** Mike chose option (1), "rule #2.1 = S1 + W1", in the DPC Research group chat on
2026-09-23 at 18:36 UTC. S1 and W1 are candidate fixes S1 and W1 of
[`results/genome/c6/rules/second_rule/DIAGNOSIS.md`](../../results/genome/c6/rules/second_rule/DIAGNOSIS.md) §5
(commit `4dc24f2`).
**Written by:** CC (subagent), 2026-09-23 UTC, on CC's brief.
**Code:** W1's code is in commit `6ffce66`,
[`results/genome/c6/rules/second_rule_v21/`](../../results/genome/c6/rules/second_rule_v21/README.md).
It was written and measured **before** this file, because W1 could be registered only if its
decoder fitted the budget (DIAGNOSIS §5: "Before W1 is registered, its decoder must be written
and its size measured"). S1 has no code yet. It goes into the gate script, which is written after
this file is committed. That script must first assert the pinned decoder and the DL bound (§9,
step 3).
**Judged by:** the C6 specification as amended (A1–A24) and the three acceptance files, as for
rule #2. If C6 is amended again, **C6 governs**.
**Blindness.** §1.2 carries rule content: the offset library. The other sections name no
mechanism beyond what DIAGNOSIS.md already states. The blind reader reads **only §8**. Ark read
DIAGNOSIS.md in full (his message of 18:37 UTC says so), and W1's cap numbers were posted in the
group chat (CC, 18:32 UTC). Recorded here, not hidden.
**Blindness record (Zcode, 19:25 UTC).** Ark and Johnny read §1.2 of this draft for their reviews,
despite the instruction to read only §8. There is no practical contamination. The caps 64 / 1,400
had already been posted in the group chat before they read it (CC, 18:32 UTC), and their
predictions at r = 1 are silent on quantity (§7; the addendum, §4).
**New numbers in this file.** Three kinds, and no others:
- W1's decoder size and worst-case DL, measured at `6ffce66`.
- The ST0 self-test's DL. ST0 is synthetic, and no score was computed.
- One descriptive split of the committed diagnosis rows (§5.2), computed for this draft from
  `diagnosis_power_rows.json` without any new fit.
Every other number is quoted from a committed record, which is named each time.
---

# Rule #2.1: rule #2 with S1 (G-e+ on the fold mean) and W1 (a larger offset library)

## 0. In plain words

Rule #2 stopped at its gates: two of seven failed (`results/genome/c6/rules/second_rule/gates.json`,
commit `e7e31fb`). The diagnosis found a different fault behind each one:

- **G-e+ failed because of the gate.** Counting "≥ 9 of 10 folds" fails even a model that
  **knows** the planted group table, on 7 of 100 fresh banks.
- **G-o0 failed because of the rule.** A 32-set, 800-bit offset library cannot hold what N_EB
  chooses from.

Rule #2.1 changes exactly two things:

- the **form** of G-e+ (S1): the fold mean instead of a fold count;
- the **size** of the rule's offset library (W1).

Nothing else changes. The re-gate runs **once**, on fresh banks from the reserved seed range.
Any red gate stops rule #2.1, exactly as it stopped rule #2.

## 1. Changes, and only these

### 1.1 S1: gate G-e+ is judged on the fold mean

**Replaces** the G-e+ row of the proposal's §2.5 table.

| id | criterion | expected |
|---|---|---|
| **G-e+** | On GB1, the **mean over the 10 folds** of (the rule's held-out existence margin over N1 − BF_1's held-out existence margin over N1) is **> +0.002** nats. | pass |

- In the harness's terms:
  Δ_e+ = `margin(rule, N1, "existence") − margin(BF_1, N1, "existence")` over GB1's 10 folds.
  This equals the mean over folds of (BF_1's held-out log-loss − the rule's).
- It is the same quantity that G-e0 bounds on GB0, and the same form P4 uses on the real bank.
- **The +0.002 is not a new number.** It is the **P4 tie band** of the rule #2 proposal, §1,
  line 60 ("A Δ within ±0.002 is read as a tie, not a pass … P4 counts as passed only if
  **Δ > +0.002**"; Zcode's ruling, registered at `c3f996d`). S1 cites that band and declares no
  threshold of its own. DIAGNOSIS §3 records the same provenance: "'+0.002' is the P4 tie band of
  §1".
- The old criterion, "beats BF_1 (A7's τ) in ≥ 9 of 10 folds", is withdrawn **for G-e+ only**.

### 1.2 W1: the offset library caps (rule content)

**Replaces** the numbers 32, 800 and 48 wherever the proposal's §2.2, §2.3 ("Offset sets",
step 1), §2.4 and §7 give them.

- **Library caps:** a set is added if, after adding it, the library holds **at most 64 sets**,
  its own A5 cost is **at most 1,400 bits**, and it contains **at most 64 distinct offsets**.
  The scan order and the skip rule are unchanged.
- **Index width:** A_s and B_t become **6-bit** symbols (0..63). They are stored in their own
  array `AB__sym64` (A, then B), always 130 symbols, whatever the library's size (reading [R18] of
  the code's README). `Q__sym32` keeps a, b, u, v, α, β, W and m.
- **§2.4's table, amended** (measured at `6ffce66`; `second_rule_v21/README.md`):

| item | A5 cost, worst case at the caps (bits) | rule #2 |
|---|---|---|
| `Q__sym32` (470 symbols at n_m = 64) | 2,436 | 3,008 |
| `AB__sym64` (130 symbols) | 872 | (in `Q__sym32`) |
| `c` | 210 | 210 |
| `L` | ≤ 1,400 | ≤ 800 |
| `e__sym8` | 466 | 466 |
| `s` | 91 | 91 |
| **data** | **5,475** | 4,575 |
| decode program, **measured**: 488 bytes | 3,904 | 4,800 (the 600-byte cap) |
| **DL(rule #2.1), worst case** | **9,379** | 9,375 |
| one-tenth limit | 9,481.2 | 9,481.2 |

- **The two numbers of DIAGNOSIS §2.2, kept apart** (Ark, 18:37 UTC):
  - **Headroom to the limit:** 102.2 bits. The diagnosis's 54 was computed before the decoder
    was measured. The decoder came out 6 bytes (48 bits) **shorter** than rule #2's 494 bytes,
    not longer.
  - **Increase over rule #2's worst case at its measured decoder (8,527 bits):** +852 bits.
- **The decoder is fixed by this registration.** `decode.py` is the file at `6ffce66`, sha256 of
  its LF text `39a04901…`. The learner is `fit.py` at `6ffce66`, `92eb6ab1…`.
  - Rule #2's §2.4 bounded DL by charging the decoder at G-size's cap: 600 bytes = 4,800 bits.
    Under W1 that bound would be 5,475 + 4,800 = 10,275 bits, **over** the limit.
  - So **P2's length half is definitional only for this decoder**: DL ≤ 9,379 < 9,481.2.
  - Any other decoder is a new registration.
  - G-size itself is unchanged (≤ 600 bytes; the measured size is 488). On its own, G-size would
    pass a different decoder of up to 600 bytes, whose worst case would be 10,275 bits. So the
    gate script must assert the pin and the bound **before** G-size (§9, step 3; Zcode).
- **Self-test only** (ST0, seed 61000, k = 10; no score): the rule is deterministic, and its
  largest DL over 10 folds is 9,257 bits. The bit cap binds there, with libraries of 42–49 sets.
- W1 changes **no existence term**. The existence fit, its quantisation and its coordinate
  descent never read the library. So every existence number in DIAGNOSIS §1 applies to rule #2.1
  exactly. This was checked on ST0 folds 0 and 3 at k = 10: rule #2 and rule #2.1 store identical
  symbols for a, b, u, v, α, β and W, identical signs, and identical values of c and of the first
  four scales. Only m's scale and the offset part can differ. This was a code check for this draft
  and was not committed.
- The rule's run name becomes `second_rule_v21_r1` (reading [R19]). It is bookkeeping only.

### 1.3 Nothing else changes

Unchanged, as registered at `c3f996d` (section numbers in this list are the proposal's):

- **The rule**, apart from W1: the model (§2.2), the learner (§2.3), the quantisation, μ = 1,
  the three rounds, the λ grid {1, 3, 10, 30, 100}, the side switch and its tie rule, the counts
  and the sign.
- **The rank:** r = round((130 + 16) / 130) = **1** (§1). W1 adds no fitted interaction number.
- **The gates G-size, G-det, G-bf, G-e0, G-o+ and G-o0, and their thresholds:**
  - G-e0: ≤ +0.002;
  - G-o+: ≥ 9 of 10 folds;
  - G-o0: [−0.010, +0.010];
  - G-bf: 1e-9 on shuffled bank 0, 10 folds;
  - G-size: 600 bytes;
  - G-det: GB1, fold 0.
- **The timing cap:** k = 10 unless the projection exceeds 12 hours, then k = 3 (§1).
- **The rest of §1:** the P4 tie band, the mandatory BF_1–BF_4 line and the P4 threshold rule.
- **§4–§6:** the descriptive post-run checks and "no harness change".
- **The gate banks' construction (§2.5):** the five draws, W\*, BASE, the 0.5 target share, the
  0.2 noise and the 0.62 sign share. Only the **seed** changes (§3).

## 2. S1 is calibration, not fitting, and what it costs

### 2.1 Why it is calibration

Sources: DIAGNOSIS §1.4 (100 diagnostic GB1 draws at W\* × 1, 100 GB0 draws; seeds
70000–70099); Johnny (18:35 UTC) and Ark (18:37 UTC) in the group chat.

- **A model that knows the answer fails the old gate.** O-W\* knows the planted group table W\*
  exactly and estimates only the per-type terms, as the rule must. It passes "≥ 9 of 10 folds" on
  only **93 of 100** fresh banks.
  - A gate that turns away a perfect detector 7 % of the time says nothing about a rule that
    fails it.
  - O-W\*'s behaviour does not depend on the rule's design. So judging the gate by O-W\* calibrates
    the gate; it does not tune it to the rule (Johnny).
- **The gate was stricter than the exam arm it guards.** P4 compares fold means:
  `harness.py` line 1031, `"pass": bool(real_m["existence"] - thr > TAU)`, plus the registered
  tie band. It never counts folds. G-e+ stood in front of P4 with a harsher rule than P4's own
  (Ark: "the gate was stricter than the exam, which is backwards").
- **The threshold carries no weight. The form of the criterion does** (Ark).
  - The largest GB0 (null) mean of rule − BF_1 over the 100 draws is **+0.00058**
    (`diagnosis_summary.json`, `GB0_diagnostic.G_e0.max`).
  - The **smallest** rule mean over the 100 GB1 draws is **+0.0075**
    (`power_GB1_diagnostic.Wstar_x1.models.rule.bank_mean_advantage_min` = 0.00751).
  - Any threshold between the two gives the same verdicts: the rule 100/100, the null 0/100.
    +0.002 sits inside that range, and so would +0.006.
  - What moved the pass rate from 89 to 100 is the change from a fold **count** to a fold
    **mean**, not the choice of number.
  - Correction to Ark's wording: he called +0.0075 "the best" rule mean. It is the **smallest**
    of the 100, which is what makes the argument hold.
- **Measured effect** (DIAGNOSIS §1.4 table):

| criterion | rule, W\* × 1 | O-W\*, W\* × 1 | rule on 100 GB0 draws (false pass) |
|---|---|---|---|
| ≥ 9 of 10 folds (rule #2's G-e+) | 0.89 | 0.93 | 0.00 |
| **fold mean > +0.002 (S1)** | **1.00** | **1.00** | **0.00** |

- **Johnny's two conditions (18:35 UTC) are both met:**
  - (1) +0.002 is the registered P4 tie band (§1.1), not a number fitted on the 100 banks.
  - (2) the calibration banks and the re-gate banks are separate sets (§3).

### 2.2 Disclosure, stated plainly

**S1 was chosen after seeing that the rule passes it on 100 of 100 diagnostic banks.** It was
also chosen knowing that the burned registered GB1 (seed 60000) clears it: its mean is +0.00781
(DIAGNOSIS §1.1). That bank is not used again.

What keeps this from being a choice made to get a pass:

- the reason is the O-W\* calibration above, not the rule's own result;
- the criterion copies an existing, registered exam rule, and its threshold is the registered
  tie band;
- the verdict does not change for any threshold from +0.00058 to +0.0075, a range about 13 times
  wide;
- the re-gate runs on banks that no calibration has seen (§3), once (§4).

The reader should still weigh a green G-e+ knowing the order in which things were done.

### 2.3 What S1 costs (Ark, point 3)

After S1, **G-e+ copies P4's criterion** (the fold mean, the +0.002 band) and is **no longer
independent of it.** If P4's form is wrong, for example a tie band that is too narrow or a mean
that hides a split between folds, G-e+ inherits the fault and cannot show it. Under rule #2 the
gate was a flawed but **different** instrument. Now **one criterion stands in two places**. This
is accepted, since a gate ought to judge by the exam's standard, but it is recorded as a loss.

## 3. The seed sets are separate

| range | use | status |
|---|---|---|
| 60000 | rule #2's registered GB1 and GB0 | burned by rule #2's gate run and re-used by the diagnosis. **Not used by rule #2.1.** |
| 61000 | ST0, the self-test bank | code checks only; never a gate bank |
| **70000–70099** | **calibration banks**: the 100 diagnostic seeds of DIAGNOSIS.md, from which S1's and W1's rates come | used; **never a gate bank** |
| **80000–80999** | **reserved for the re-gate**: nothing generated, fitted or scored (`diagnosis.py` refuses the range) | one seed, chosen by the rule below |

**The re-gate banks, by a rule fixed now:**

- **Seed rule:** the **lowest seed of 80000–80999 not yet generated, fitted or scored**. No seed
  in the range has been touched (DIAGNOSIS "Seed discipline"; `diagnosis.py` asserts it), so this
  is **seed 80000**.
- **One seed gives both banks**, as §2.5 builds GB1 and GB0 from one seed:
  - **GB1** = `gate_banks.draws(80000)` with W\* and the target flags;
  - **GB0** = the same draws with W\* = 0 and π_t = 0.
- **Generator:** `gate_banks.py` of rule #2, LF sha256 `cd12c646…`, committed at `dd4dc92`.
  The copy in `second_rule_v21/` at `6ffce66` is byte-identical, and a unit test checks this. The
  construction and consumption order are §2.5's, unchanged. Only the seed argument differs.
- **G-det** uses the new GB1, fold 0. **G-bf** uses shuffled bank 0, as before; it has no seed
  from these ranges. Every gate runs at k = 10.
- The re-gate is recorded in `second_rule_v21/gates.json`, with the seed, both banks' non-empty
  counts and the sha256 of each bank's content.

## 4. Decision rule on a red gate, fixed before the run

- **One run of the gate script. No redraw of the banks, no second seed, no second attempt.**
- **Any failed gate stops rule #2.1**, as a failed gate stopped rule #2 (§2.5). The rule is then
  not run on C6, and any further fix is a new registration with its own reserved seeds.
- **A crashed run is not a verdict** (glossary, "run"). If the gate script stops before it has
  recorded all seven verdicts because of the machine or the process, not the rule, it may be
  re-executed with the **same commit and the same seed 80000**. Every fit is deterministic
  (G-det), so a re-execution cannot change a verdict. The crash is recorded.
- **An exception raised by the rule's own code** inside a gate fit (for example, Newton on c not
  converging) **fails that gate**. It is not a crash.
- **An exception raised by the harness's own code** (`harness.py`) during a gate or a fit **voids
  the run** (Zcode). It is not a gate result, and it is recorded.
  - Any fix to `harness.py` needs an A20 `--controls` re-run with every verdict unchanged, and
    Mike's word.
  - The re-gate then re-uses the **same rule commit and the same seed 80000**. No new draw is
    made.

**The risk, named before the run.** A single fresh bank is a draw, and W1 does not make every
gate certain.

| gate | chance of red on one fresh bank | source | what it is |
|---|---|---|---|
| **G-o0** | **about 10 %** | DIAGNOSIS §2.2 (`diagnosis_summary.json`, `GB0_diagnostic.caps`, the row with sets and offsets uncapped and a 1,400-bit cap): 90 of 100 GB0 draws pass; mean −0.0037; **worst −0.01697** against the ±0.010 band | **Structural, not gate noise.** The side switch is not fixed: "even an unlimited library leaves the side switch", with 2 of 100 draws out of band (worst −0.0154). The rest is the library restriction still left at 1,400 bits. The gate's own paired noise is small (SD 0.00085). |
| **G-o+** | **about 9 %**, measured under rule #2's library (32 sets / 800 bits / 48 offsets); not re-measured under W1 | DIAGNOSIS §3 (`power_GB1_diagnostic.Wstar_x1.G_o_plus.pass_rate_9_of_10` = 0.91): the "≥ 9 of 10" count failed on 9 of 100 GB1 draws at × 1 | The same count weakness as the old G-e+. S4 (the matching fix) was **not** chosen, so it is carried. **Expected to be conservative**, an upper estimate under W1: W1 removes most of the library loss, which cost −0.0291 on GB0 (DIAGNOSIS §2.1). Expected (Johnny, Zcode), **not measured**. |
| G-e+ (S1) | 0 of 100 | DIAGNOSIS §1.4; W1 does not touch existence | — |
| G-e0 | 0 of 100 | DIAGNOSIS §3 | — |
| G-size, G-det, G-bf | deterministic | 488 bytes; ST0 determinism; G-bf is the unchanged learner | — |

- **What the G-o0 rate measured, precisely.** The 0.90 comes from the diagnosis's cap sweep, in
  the configuration **with no set cap, no offset cap and a 1,400-bit cap**. That is not W1's exact
  caps (64 / 1,400 / 64). In that sweep the largest final library held 62 sets and 49 offsets,
  under W1's 64 and 64, so the final libraries would be the same under W1. The inner-fold
  libraries were not recorded, so this is not certain for them.
- **The joint all-green rate was not measured** (Ark). What is known:
  - G-o0's ≈ 0.90 comes from the configuration above, not from W1's exact caps.
  - G-o+'s ≈ 0.91 comes from rule #2's 32-set library.
  - Both gate banks come from **one draw** (seed 80000: GB1 and GB0 share the same draws), so the
    two gates are **not independent**.
  - The **direction** of the dependence is unknown. If a bad draw tends to fail both gates, their
    failures are positively correlated, and the chance that both pass is **at least** the product.
    Only a negative dependence would make it lower.
  - So the product 0.90 × 0.91 ≈ 0.82 is **neither an expectation nor a bound**. No all-green
    probability is claimed.
- **What is stated before the run:** a red G-o0 or G-o+ on the single re-gate is a known,
  measured possibility of the order of one in ten for each gate. It is stated now so that a red
  gate is not read afterwards as a surprise or a reason to redraw.

## 5. Known defects carried, not fixed

### 5.1 The λ grid has three live values, not five (DIAGNOSIS §1.3)

- In all 20 registered folds, at λ = 10, 30 and 100 the rank-1 term is **exactly zero**, for the
  rule and for BF_1. Rank-1 ALS with this ridge has u = v = 0 as its solution there.
- So the grid has three live choices: λ = 1, λ = 3 and "off". The nested scheme's tie rule labels
  "off" as λ = 100.
- **This affects BF_r too.** But in every BF fit recorded on the real bank, BF chose a **live**
  value in every fold, so **no C6 verdict changed**:
  - **BF_1**, the one that sets rule #2.1's P4 threshold, chose **λ = 1** in all 10 folds
    (`harness_controls.json`, `controls["real/N0 as a rule"].P4.bf.lambdas`);
  - BF_3, BF_4, BF_8, BF_16 and rule #1's BF_12 chose λ = 3 in all 10 folds (the same file,
    other controls; `first_rule_k12/RESULT.md`, P4 line).
  - Correction: the group chat (Johnny, 18:35 UTC, citing Zcode) said "BF chose λ = 3". For BF_1
    it chose λ = 1. The conclusion stands, because neither is a dead value.
- It is **not fixed** here. W5, the fix that would address it, was not chosen, and fixing it would
  also change BF_1-likeness and G-bf.

### 5.2 How the "off" folds enter S1's mean (Johnny, 18:35 UTC)

Under the old count, each fold was one vote. Under S1, each fold's size counts. On the diagnostic
GB1 draws at W\* × 1:

- **The rule chose "off" in 49.9 % of folds.** BF_1 did so in 3.7 %, and O-W\* in 49.5 %.
- Per bank, the rule's "off" folds ran from 0 to 10, with a median of 5.5.
- So S1's mean averages **two different models**:
  - in the "off" folds, N1 + W, set against BF_1's N1 + u·v;
  - in the λ = 3 folds, N1 + u·v + W, set against BF_1.
- The split, computed for this draft from `diagnosis_power_rows.json` (1,000 fold rows,
  commit `4dc24f2`; no new fit):

| folds | share | rule − BF_1, mean per fold | contribution to the bank mean (mean over banks) | O-W\*, same split |
|---|---|---|---|---|
| rule chose "off" | 0.499 | +0.0139 | +0.0069 | +0.0150 ("off" share 0.495) |
| rule chose λ = 3 | 0.501 | +0.0162 | +0.0081 | +0.0177 |
| all | 1.000 | +0.0151 | +0.0151 | +0.0164 |

- **Reading:** both halves carry a positive advantage of similar size. The mean is not produced by
  one kind of fold alone. S1 judges **the rule as it chooses**, "off" folds included. That is how
  P4 judges the rule on the real bank: P4 averages the folds whatever λ each fold chose.
- **What this does not say:** how the split will fall on the re-gate bank or on the real bank.
  The rule's choice there is unknown and is not predicted here.

### 5.3 G-o+ keeps its fold count

S4 was not chosen. G-o+ still counts "≥ 9 of 10 folds", with the weakness DIAGNOSIS §3 measured:
9 of 100 draws fail, and the fewest wins seen was 5. See §4's risk table.

### 5.4 The G-o0 band has no stated source

DIAGNOSIS §3 records that "±0.010 has no stated source". It stays as registered. It is about
12 paired-noise SDs wide (DIAGNOSIS §2.3), so it is wide rather than tight.

## 6. Interpretation lines for any later C6 `RESULT.md`

If a C6 run of rule #2.1 ever happens, its `RESULT.md` prints the following lines **directly
under the verdict line**, next to the mandatory BF_1–BF_4 line of §1 (Johnny, 18:35 UTC; Ark,
18:37 UTC). They are part of the record and cannot be dropped. The post-run script is extended to
print them before any C6 run. That is a text change with no number, committed separately and
reviewed.

1. **What the bank is.** The bank is flyvis's **FIB-25/FIB-19 type-level template**
   (Lappalainen et al. 2024). It holds mean synapse counts per (type pair, offset), **averaged
   over columns**, and it **merges two female flies by taking the larger of two estimates**
   (their equation 7). It is not one animal's wiring and holds no per-neuron weight. Source:
   [`docs/notes/2026-09-23-where-our-bank-comes-from.md`](../notes/2026-09-23-where-our-bank-comes-from.md)
   §2–§3. So any outcome answers "is a type-level template compressible?", not "is an individual
   brain compressible?" (Johnny).
2. **Column averaging is not between-individual stability.** Averaging removes the variation
   between columns inside one reconstruction. It does not show that the template is what carries
   over between flies. That stays plausible but unmeasured, and the bank cannot express
   between-fly variation (the note, §3; Ark).
3. **Many signs rest on personal communications.**
   - 368 of 432 sign-citation slots (85 %) are personal communications.
   - 232 of the 272 `alpha_fixed` entries rest only on them.
   - Source: [`results/genome/bank/README.md`](../../results/genome/bank/README.md), "Warning: most
     sign citations are personal communications", from `sign_citations`.
   - The rule's sign is N1's by construction, so this bears on what the sign field means, not on
     the rule's sign margin.
4. **The family choice was informed** (the proposal's §3 caveat, carried over). Rule #2's family
   was chosen by an author who had seen rule #1's real-bank results and whole-bank regularity
   numbers. That caveat travels with any rule #2.1 result.

**A correction for the record** (relayed by the coordinator with Johnny's 18:55 UTC line).
**Rule #2 has never been fitted on the real bank.** The numbers 0.3670 against 0.3625 (held-out existence, rule against N1) and P4 at
−0.053 belong to **rule #1** (`first_rule_k12/RESULT.md`; the addendum, §5). Ark's message of
18:37 UTC cited them as rule #2's. They are not evidence about rule #2 or rule #2.1.

## 7. Registered predictions: what carries over

The registered predictions
([`2026-09-23-first-rule-failure-predictions.md`](2026-09-23-first-rule-failure-predictions.md),
`b8ca3dd` and `32a4ae9`) and their
[addendum](../notes/2026-09-23-predictions-addendum-after-tau.md) were written for rule #2's C6
run. The note on rule #2's stop says items carry over "only where that registration says so
explicitly". **This section says so, item by item.**

They carry over **unchanged, on the same branches as rule #2's §4.4**, because what selects a
branch is unchanged:

- r = 1, so P4's threshold is BF_1's (+0.02815 at k = 10; the run's printed threshold governs);
- the fields touched: existence yes, offset sets yes, counts yes through the offset sets with no
  new per-node counts term, sign no;
- the exam's thresholds and the P4 tie band.

| registered item | branch (as rule #2's §4.4) | carried over |
|---|---|---|
| P-J1 | prediction (existence touched). **Silent on quantity** this round (addendum §4: at r = 1 the margin falls in its own refuting zone; Johnny's live reading is "margin ≈ BF_1 within ±0.002") | yes, with the addendum's silence |
| P-J3 | prediction, judged on the harness's P4 verdict. Band [+0.02315, +0.02815]. A Δ in (0, +0.002] refutes it on the harness verdict, while the tie band reads it as a tie. Both are printed. | yes |
| P-J4 | prediction (offset touched): the Jaccard bar ≥ 0.4831, essentially N_EB's 0.48417 | yes |
| P-J5 | **no prediction** (offset touched) | yes |
| P-A1 | no prediction unless m(0.0) ≥ +0.040. Ark registered no dial reading this round (addendum §4). | yes |
| P-A3 | prediction. **Only the claim (P4 fails) is testable.** Its quantity is empty at r = 1 (proposal §4.4; addendum §4). | yes |
| P-A4 | prediction (offset touched): m_off(1.0) − m_off(0.0) ≥ +0.005 | yes |
| P-A6 | prediction (offset touched): in-sample offset margin ≤ τ versus > τ | yes |
| P-B1 | prediction (P3 existence passes; margin ≥ +0.040; gap ≥ +0.015) | yes |
| P-B2 | prediction (P3 offset fails unless Jaccard > 0.4842) | yes |
| P-B3 | prediction. Its rule half needs the k = 3 descriptive run (the proposal's §5.3). | yes |
| P-B4 | **does not apply** (r = 1 < 8) | yes (as not applying) |
| P-B5 | prediction (P4 fails; rule − BF_1 < +0.005) | yes |
| P-B6 | prediction (≥ 9 of 10 existence wins against N1) | yes |
| LOTO registration note | does not hold by construction: X_e does not vanish on an unseen type | yes |
| author's S2-1 … S2-9 (proposal §4.2) | as registered, with the same numbers and probabilities | yes |

**Changed branch: none.**

- W1 changes the offset mechanism **inside** the "offset sets touched" branch. It does not change
  which fields are touched, the rank or any threshold. So no item moves to another branch.
- S1 changes a **gate**, not an exam arm, a threshold or a branch condition.
- Some reasoning texts describe rule #2's library: the proposal's §7 ("restricts every choice to
  a 32-set library") and the reasoning behind S2-2 and S2-7. Read them as describing rule #2's
  caps. Their **claims, quantities and probabilities are not revised**: revising them now would be
  informed by the diagnosis's synthetic results.

Johnny's stake, as he stated it (18:35 UTC): P-J3 (Δ ≤ 0 against BF_1) is refuted if the rule
behaves on the real bank as it did on GB1. It stays the one item that directly contradicts the
author's prior.

## 8. Blind-safe summary (rule #2's §8, updated for rule #2.1)

This section gives only the registration fields, the thresholds and the arms touched. It gives
no mechanism, no latent variables and no fitting details.

- **What changed against rule #2:**
  - **S1**, one gate's form: G-e+ is judged on the fold mean, above the registered +0.002 tie
    band, not on a fold count.
  - **W1**, one capacity limit inside the rule's offset part.
  - Nothing else: rank, fields touched, exam thresholds, the other six gates, the timing cap and
    the predictions' branches.
- **Rank, computed by A11's rule:** r = round((130 + 16) / 130) = 1, unchanged.
  - 130 is the number of fitted per-type numbers in the rule's interaction terms.
  - 16 is the number of fitted numbers in a term on a fixed partition, which has no per-type
    coordinates.
  - The harness's fallback count would also give 1, by a degenerate count.
  - At r = 4 the threshold would be +0.03972, and the author's P4 prior would drop from 0.5 to
    0.15.
- **P4 threshold:** +0.02815 at k = 10 (BF_1's margin over N1). The run's own printed threshold
  governs.
- **P4 tie band:** a margin within ±0.002 of the threshold is a tie, not a pass. P4 counts as
  passed only if the margin exceeds the threshold by more than 0.002. A "real amount" is at least
  max(0.005, 2 × the paired standard error).
- **Mandatory printing:** under the verdict line, the record prints the margin against BF_1 (the
  decision) and against BF_2, BF_3 and BF_4 (context). It also prints the four interpretation
  lines of §6: a type-level template averaged over columns and merged across two flies; column
  averaging is not between-fly stability; many signs rest on personal communications; the
  family choice was informed.
- **τ:** P3 and P4 require a margin to exceed its comparison by more than τ = 1e-9 (`1789aeb`).
- **Timing cap:** 10 starts, unless the projected wall time measured on shuffled bank 0 exceeds
  12 hours; then 3 for the whole run.
- **Fields touched:** existence yes; offset sets yes; counts yes (scored on changed offset sets,
  with no new per-node counts term); **sign no** (identical to N1's on every cell).
- **By construction:** P1 sign ties N1, and P3 sign is 0 on all 100 banks. Neither of §4c's
  by-construction fails applies. DL is at most **9,379 bits** with the registered decoder, under
  the one-tenth limit of 9,481.2 (rule #2: 9,375).
- **Registered-prediction branches:** unchanged from rule #2 (§7 lists them). P-J4, P-A4, P-A6
  and P-B2 are predictions (offset touched). P-J5 is "no prediction". P-J1, P-J3, P-A3, P-B1, P-B5
  and P-B6 are predictions (existence touched): P-J1 is silent on quantity, and only P-A3's claim
  is testable. P-B4 does not apply. P-A1 makes no prediction unless the real margin reaches
  +0.040. **No branch changed.**
- **The author's expectations by arm** (unchanged): P1 existence pass; P1 offset fail against
  N_EB; P1 counts pass; P2 pass; P3 existence pass; P3 offset fail; P4 about even odds of a
  margin above BF_1's and 0.4 of clearing the tie band; whole exam FAIL expected (probability of a
  pass ≤ 5 %).
- **Gates before any C6 run:** seven, run **once** on fresh synthetic banks from seed 80000
  (reserved, untouched). **Any red gate stops rule #2.1.** Known chance of a red: about 10 % on
  one gate and about 9 % on another, stated before the run (§4).
- **What S1 costs:** G-e+ now uses P4's own criterion, so it is no longer an independent check
  on P4.
- **Rule #2 has never been fitted on the real bank.** No real-bank number exists for it or for
  rule #2.1.
- **Descriptive only, after the run** (no verdict): unchanged from rule #2.

## 9. The run sequence after the commit

1. **Review** (group chat, 19:13–19:25 UTC; requested 19:06 UTC): Zcode on the rule side (§1.2, the code at `6ffce66`); Ark
   and Johnny on S1 (§2–§4) and on §5–§8.
2. **Commit this file.** Its commit is the one that adds this file (the status line says so). Then regenerate
   `docs/blind-author-exclusions.txt`.
3. **Write the gate script** `second_rule_v21/gates.py`: rule #2's `gates.py` with G-e+ as §1.1
   and the banks of §3 (seed 80000), and nothing else changed except two hard asserts at its start.
   Commit it **before** it runs. Only the §3 banks and shuffled bank 0 may be built. **Before
   G-size and before any bank is built**, the script must hard-assert, in this order (Zcode,
   19:25 UTC):
   1. `harness.sha256_lf(decode.py) == "39a049013af18a1e89e534d9d378a5f59a772b894d7fab5b79f82f702723a15a"`, the decoder pinned in §1.2;
   2. the worst-case data bits at the caps (every array at its largest: `Q__sym32` with
      6 × 65 + 16 + `LIB_MAX_OFFSETS` symbols, `AB__sym64` with 130, `c`, `L` at `LIB_MAX_BITS`,
      `e__sym8` and `s`) plus `harness.program_bits(PROGRAM_FILES)` is ≤ `fit.DL_LIMIT_BITS`
      (= 9,481.2, the one-tenth limit). At `6ffce66` this sum is 9,379.

   A failed assert stops the script before any gate. It is not a gate result.
   - **Why:** without the pin, a different decoder of up to 600 bytes would pass G-size with a
     worst case of 5,475 + 4,800 = 10,275 bits, over the limit (§1.2).
   - `gates.py` is still written **after** this file is committed. This file registers the
     requirement.
4. **Re-gate once** on seed 80000 (§3), at k = 10. Commit `gates.json` whatever it shows.
   - **Any red gate:** rule #2.1 stops (§4). Record it the way rule #2's stop was recorded.
5. **Only if all seven gates are green:** measure the timing cap on shuffled bank 0 (`timing.py`)
   and write the decision to the run's attempts file before any real-bank fit, as the proposal's §1
   requires.
6. **The C6 run happens only on Mike's separate word.** A green re-gate does not authorise it.
   The run then goes through the harness's `--rule` path, followed by `post_run.py`, with the §6
   lines under the verdict.

**What a green re-gate buys, and what it does not** (Ark, 18:37 UTC). It shows only that the rule
finds a **planted** signal on a fresh synthetic bank, so that a C6 run would be **readable**. It
says nothing about the real bank. The author's prior for a C6 pass stays at most 5 %.

## Files opened for this draft

- `results/genome/c6/rules/second_rule/DIAGNOSIS.md`, `README.md`, `fit.py`, `decode.py`,
  `gates.py`, `gate_banks.py`, `diagnosis.py`, `test_fit.py`, `timing.py`, `post_run.py`;
  `diagnosis_summary.py` (the DL estimate); `diagnosis_summary.json` and
  `diagnosis_power_rows.json` (by script, for the numbers cited in §2.1 and §5.2); `gates.json`
  (its hash lines)
- `results/genome/c6/rules/second_rule_v21/` (written for this amendment, commit `6ffce66`)
- `docs/plans/2026-09-23-second-rule-proposal.md`; `docs/plans/2026-09-23-first-rule-failure-predictions.md`
- `docs/notes/2026-09-23-second-rule-stopped-at-gates.md`,
  `docs/notes/2026-09-23-where-our-bank-comes-from.md` (§1–§4),
  `docs/notes/2026-09-23-predictions-addendum-after-tau.md`
- `results/genome/bank/README.md` (the sign-citation warning); `results/genome/c6/harness.py`
  (lines 190–330, 511–523, 1020–1040 and 1498–1542); `GLOSSARY.md` (grep)
- DPC Research group chat, messages 18:18–18:52 UTC on 2026-09-23 (read whole). Johnny's
  18:55 UTC line was relayed by the coordinator.
