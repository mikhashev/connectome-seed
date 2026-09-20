---
**Status:** PROPOSAL — not registered. Written by Ark (DPC Research chat, 2026-09-15 08:09 local, on Mike's word "yes, write it out" — translated from Russian — 08:08). Copied from the chat into this repository by CC, 2026-09-15, and rendered into English on 2026-09-20 under the repository's language rule (docs/CHECKLIST-research-repo.md § Language); the translation is faithful and changes no number, identifier or claim. Ark's own file `research/mi-axis-per-cell-type-design.md` lives on his node; this copy is the one the repository cites.
**What it is:** a design for a second, observational readout — the mean activity of each of the 65 cell types (row B) at every saved checkpoint (row C), with the controls of `docs/experiments/002-night2-seeds-1-and-2.md` §5f (P0/P1/P2, twin trap) — and the question whether row B predicts the causal ablation profile (row A, §5f).
**What is not fixed yet (CC's reading, to be fixed before any B value is looked at):** the verdict threshold and rule of §5 (numbers not written); P0 for row B cannot be "agrees with the stored value" because no per-type values are stored — it is cross-process reproducibility, as for the ablation profiles; the closeness measure between rows B and A in §3 is not named.
**Update 08:13:** the three unfixed points are addressed in the Addendum at the end (Ark); the design remains a proposal until a registration document exists.
**Implementation note (CC):** row B is recoverable from the saved checkpoints by one validation forward per checkpoint with per-type accumulation, so no hook enters the night run script; night 3 runs the registered script unchanged and rows B/C for seeds 3 and 4 are computed post hoc, exactly as for seeds 0, 0′, 1, 2. Execution waits on Mike's word.
---

# The MI axis per cell type — design

*(Ark's text, translated from Russian; the identifiers, numbers and structure are his.)*

## 1. What carries over, and what does not

**Three things carry over** from LLM-Microscope:
1. the axis is collected **automatically at every checkpoint** — zero extra GPU;
2. **the unit of measurement is the natural one for the substrate.** There it is a layer, here it is the **cell type** (65) and the simulation step;
3. the pattern "snapshot → intervention → snapshot → delta"; here it has already been worked through as ablation.

**What does not carry over:** MI as a verdict on (b). MI returned UNINFORMATIVE in S137 **not by accident** — for the reason written into its own pre-registration: it was measuring global geometry, while the effect was about one particular element. The same class as loss.

## 2. What is computed, and where

Right now `activity.h5` is **one number per iteration** (the mean over nodes) plus min/max. A cousin of loss: one scalar number about the whole organism.

**Proposal:** **65 numbers per checkpoint** — the mean activity of each cell type plus the within-type spread. A hook into the same forward pass that is already made for validation. **Zero GPU, zero new runs.**

Why the cell type in particular: the **genotype** channel (65 `nodes_bias`) and the **phenotype** channel are indexed by **the same thing**. "What changed → what lies behind it" reads off with no intermediary. In an LLM there is no such coincidence: what you patch and what was trained are different objects.

## 3. Three rows, at different prices

| row | what it is | price | do we have it? |
|---|---|---|---|
| **A. ablation profile** | 65 contributions, causal | 65 forwards | yes (yesterday) |
| **B. activity profile** | 65 means + spread, observational | **0** (the same pass) | no — proposed here |
| **C. trajectory of B** | 65 × 72 per run | **0** | no |

Row A is expensive, B is free. **Hence the real question: does B predict row A?** If it does, we have a cheap, readable substitute for an expensive test. That is what carrying the lesson over actually means: not "another instrument instead of loss", but **a second axis for free, plus the question whether it is related to the causal one**.

## 4. Controls (taken one-for-one from §3.9)

- **P0 — reproduction:** with no intervention, row B agrees with the stored value to 10⁻⁴ (threshold measured: 2.5·10⁻⁵ within a process, 3.8·10⁻⁵ between processes).
- **P1 — empty intervention:** an empty set of types → a shift of 10⁻⁵.
- **P2 — known positive:** ablation of R1–R8 (measured: +47…+65 in three seeds, +30,626 in seed 2). If it does not go red, the instrument does not work.
- **Twin trap (mandatory):** row B is required to separate 0 and 0′ **more weakly** than 0 and 1. Otherwise it is measuring launch noise. This is P1 in its purest form.
- **Refusing to read the ambiguous:** a duplicate key = **a refusal**, not "the freshest file". This is the defect in `analyze_mi_channel.collect()` ("last one wins, no warning"), repaired by refusing. Here `results/night2/` is already full and will keep growing.

## 5. To be fixed BEFORE the first look

- **The carrying measure is Spearman's ρ** over the 65 types. Why: in the twins, Pearson parts company with Spearman (r 0.351 against ρ 0.715), and that has **already been observed**. Choosing the measure after the result = choosing by the outcome.
- **The task composition is all 16**, with per-item beside it. Trimming the unstable ones **loses** the separation (over 10 tasks the twins converge more weakly).
- **The threshold and the verdict rule** — from P0/P1, written down before the run.
- **Instrument failure:** (i) B separates 0/0′ no more weakly than 0/1; (ii) P2 does not go red; (iii) the measure is forced to change after the result. A failure is **a result**, not grounds for re-measuring.

## 6. Limits

- Row B is **not causal** — it shows where a difference is visible, not where it was made. It does not replace A; it asks whether A can be made cheaper.
- **It does not judge (b)** — a new readout after the data of nights 1–2 is a new document.
- **It does not get around the floor** — if the difference between seeds is smaller than B's own wandering, it is invisible here too.
- **It does not save us from homogeneity** — 65 biases out of 8161; the question of road C stays open.
- **The critical ρ:** at N = 4–5, ρ = 0.90–1.00, so the test is impossible in principle. A registered reading is only at N ≥ 8. Until then B is a **preview diagnostic** and must not be read as a test.

## 7. Order of work

1. **Night 3** (seeds 3, 4) — with row B, if the hook fits into the same pass; otherwise without it, hook on night 4.
2. **From what is already on disk:** row B for seeds 0, 0′, 1, 2 (taken afresh — per-type activity was not saved), the twin trap, P0/P1/P2.
3. **Preview:** does B(25k) predict B(250k)? As a preview, not as a test.
4. **Rows A and B on one population, N ≥ 8** — under a document that is registered by then.

---

Two words on why this and not "take MI": MI was measuring the **global geometry of the model**, and its null was predicted in advance. The unit here is a different one — 65 types, which is the same axis the genotype lies along. And the price is different: **zero**.

What I myself dislike about this design, so that it does not look smooth: row B is still **blind to what it does not itself touch** — it sees where individuals come apart, but it does not say why. That is, if it shows "seed 2 stands on R2", that still does not mean "seed 2 bet on R2" — it may have been compensating for a shortfall (the same counter-argument I wrote yesterday about ablation). There is nothing to separate the two with except night 3 with seeds 3–4 — if the R2 effect repeats in a new seed, it is no longer an anecdote.

---
## Addendum — Ark, 2026-09-15 08:13 local (copied from the DPC Research chat by CC and translated from Russian; still a PROPOSAL, not registered)

Agreed, and your simplification is better than mine: if B is taken from the checkpoints, no hook enters training at all, the risk of breaking a run is zero, and my question about the price of the Euler step falls away by itself. Row C (65 × 72) becomes free too. As for the three unfixed points — they are mine; here is the text to be added to `docs/proposals/mi-axis-per-cell-type-design.md`.

## Point 1 (yours): P0 for B

You are right that there is nothing to compare B against — no per-type values are stored. But there is a control stronger than "reproducibility between processes", and it is free, because it is sitting in the same checkpoints:

**Iteration 0, the pairs (0, 0′) and (0, 1).** Yesterday's diagnostic already measured it: at iteration 0 the distance (0, 0′) = **0.000**, while (0, 1) = 0.557 and (0, 2) = 0.538. So we have three calibration points at once:

| control | what goes in | what B is obliged to show |
|---|---|---|
| (0, 0′) at iteration 0 | the same weights, the same data order | **bit for bit the same** (within a process, exactly; between processes, up to noise) |
| (0, 1) at iteration 0 | a difference in exactly 65 `nodes_bias` | **small, but not zero** |
| (0, 1) at 250,008 | genuinely different individuals | the full difference |

This is better than a single P0: it gives a **graduated ruler** — "zero difference" → "the smallest possible difference" → "the real thing". If B does not tell the first row apart from zero, or collapses the third the same way as the second, the instrument is broken, and that is visible before any interpretation.

## Point 2 (yours): the threshold and the verdict rule

I will put a number on it, with one correction to the criterion as stated: the twins must be compared **not against (0, 1)** but against **the nearest foreign pair**, because it turned out yesterday that the binding pair is (0′, 1) at 4798, with the twins at 4798 against 5007 — that is, a margin of 4 %, not 21 %. A rule against (0, 1) is weaker than what is already known.

- **Measure:** Spearman's ρ over the 65 types, fixed (Pearson turns it over: 0.351 in the twins against 0.588 in (0′, 1); choosing the measure after the result = choosing by the outcome).
- **Distance between individuals:** 1 − ρ.
- **Condition for passing the trap:** d(0, 0′) is the minimum over all pairs **and** below the nearest foreign pair by more than the measured floor. Take the nearest foreign pair by the minimum, not as (0, 1).
- **Floor:** the spread of ρ when **one and the same** checkpoint is taken in three fresh processes. Do not borrow it from ablation — ρ has a scale of its own and the floor has to be measured. Three runs instead of one; minutes either way.
- **Failure:** if the margin over the nearest foreign pair is inside the floor, B is **uninformative**, and differences between individuals by B are not interpreted. That is a result, not grounds for changing the measure.

## Point 3 (yours): the measure of closeness between B and A

Two different questions, both legitimate; one must be chosen before the first look:

- **(i) within an individual:** ρ(B_A, T_A) over the 65 types — does the observational axis agree with the causal one in a single organism? 65 points of freedom.
- **(ii) between individuals:** agreement of the distance matrices — by B and by A, over all pairs. This is exactly the "cheap replaces expensive" test. But at N = 4 that is 6 distances, so no conclusion is possible, only a preview.

**The primary one is (i)**, because 65 degrees of freedom against six, and because the question "is it readable" comes before the question "is it replaceable". Print (ii) beside it as a preview. Both on a fixed task composition.

## And three points I should have written into the design and did not

1. **Compute B per-item as well (65 × 16).** Otherwise we repeat yesterday: the differences may turn out to sit in three tasks, and the aggregate will not show us that. The composition is fixed, per-item goes beside it.
2. **Which moment of the simulation to read.** Activity differs from step to step; the choice of statistic (mean over the window, last step, maximum) is a choice that cannot be made afterwards. I fix it: **primary — the mean over the whole simulation window**, secondary — the value at the last step. Row C (by step) is kept in full, so that the choice can be checked rather than replayed.
3. **R1–R8 in the profile.** The eight photoreceptors at the input: their activity is to a large extent set by the stimulus and not by the individual's weights — so in the profile it is by construction almost a constant. Ablation showed that in seeds 0, 0′ and 1 they stand at 47–65, and in seed 2 at 30,626, so they cannot be excluded. I write it down this way: **the primary profile is all 65, the secondary is 57 without R1–R8**; the choice between them was made not now but before this conversation, and that has to be said outright (we already knew the breakdown by type when we decided it).

## What this gives us in the morning

Row B over seeds 3 and 4 is **the first replication test for the R2 finding**. Yesterday I noted that one organism does not tell "bet on R2" apart from "compensated for a shortfall". Seeds 3 and 4 separate that fork: if one more new individual stands on R2, it is already a property and not an anecdote; if not, seed 2 stays a single observation.

## What is mine to do

The text above — to be added into the design, and the measures, the composition and the moment to be fixed there as well. After that, mine is the review of the profiles once they are taken. Execution is CC's; the word on "row B" and on night 3 is Mike's, not mine. And separately: row B is a **preview diagnostic**, the critical ρ at N = 4–5 is 0.90–1.00, so no figure from it reads as a test, today or tomorrow.

**Executed 2026-09-15 as a preview:** see 002 §5i.

**Addendum 2026-09-15 10:25 (Ark):** rows A and B are different instruments and will name
different cells; a divergence between them is not a contradiction and not a failed replication
(002 §5i, second pass).
