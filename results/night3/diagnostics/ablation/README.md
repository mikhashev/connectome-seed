# Cell-type ablation profiles of seeds 3 and 4, and the six-run analysis

**Status: UNREGISTERED DIAGNOSTIC, applied under a PRE-REGISTERED READING.** The instrument is
the one fixed in `results/night2/diagnostics/ablation/README.md` (protocol §1–§8, written before
that script was first run). The *reading* applied to its output was fixed in
`docs/next-session-plan.md` §2a (Ark 08:23 / 08:28, Zcode 08:24), written and committed
**before** night 3 was launched. Nothing here is a test of hypothesis (b) or (b2), and nothing
here is a rung. A repeated observation is not a test.

**Run by:** CC's subagent (Opus), 2026-09-16. **Run dirs read only.** Another agent was computing
row B on the same GPU concurrently.

---

> **Override of the machine verdict (2026-09-16, on Mike's word "let's try it" — translated from
> Russian — reviewers
> Ark 05:27Z and Zcode 05:27Z concurring).** `ablation_reading.json`'s own `verdict` field reads
> `"positive_reading_triggered": true` and text *"POSITIVE: a single-type dependence exceeding
> 2863 appears in seed 3 or seed 4 -> the R2 finding becomes a REPEATED OBSERVATION, still not a
> test."* **That printed text is not this record's reading.** `docs/next-session-plan.md` §2a's
> rule was written with two different size definitions for the same clause — "of the size seen
> in seed 2, +21,157" in the sentence before, "exceeds 2863" (the twin discrepancy bound) in the
> operational clause the script (`ablation_night3.py:466-476`) actually evaluated. The script
> executed the operational clause literally and only that clause, which measures single-type
> *dominance* (a ratio against the second-largest type in the same run), not a repeat of R2's
> +21,157.5. It is not a repeat: Δ_R2 is +146.9 (seed 3) and +41.8 (seed 4) against +21,157.5
> (seed 2) — half an order of magnitude short, not "the size seen in seed 2". The threshold 2863
> is also met by 5 of the 6 runs on record (§5 below), so it does not discriminate a repeat from
> the background rate. **The outcome under the registered rule is therefore undetermined by
> defect of the rule, not positive** — this is recorded as a pre-registration defect (the rule's
> two clauses disagree with each other and the script could only execute one of them), not as a
> positive outcome, and not as a re-reading of what the script printed. `ablation_reading.json`
> itself is left unchanged, as the artefact of what the script printed under the rule as written
> — see checklist rule 16, `docs/CHECKLIST-research-repo.md`.

## 1. What was run, and what was reused

The protocol is the night-2 one, unchanged: `chkpt_00071` (iteration 250,008 in the CSV
convention; `chkpt_iter.h5` stores 250,007), the registered held-out split (6 scenes, 16 items,
batch size 1, augmentation off, `t_pre = 0.25`), the ablation = `state.nodes.activity` of all
nodes of one cell type multiplied by 0.0 at every Euler step and at the initial state, via
`Network.register_state_hook` (`flyvis/network/network.py:444-469`), 65 types, `Δ_T = loss(ablate T)
− loss(no ablation)` on the 16-item mean.

**Nothing of the protocol was re-implemented.** `ablation.py` was **imported, not copied**
(`ablation_night3.py:52`), so there is one copy of the hook and one copy of the statistics on
disk. The evaluator comes from `diag1_eval_paths.py` (`:51`), and the seven `eval_rung`
invariants from `rowB.py` (`:53`). sha256 of every module, recorded in every output json
(`ablation_night3.py:76-85`, hardening item 9) and verified against `sha256sum` after the run:

| file | sha256 |
|---|---|
| `results/night3/diagnostics/ablation/ablation_night3.py` | `c20013b4ab0826af6d89cccd653d1cfa601915017fbbd04156fe1628ffac156a` |
| `results/night2/diagnostics/ablation/ablation.py` (unchanged, imported) | `1545b53b14b64758f0cc5630a8be8a635ff1e3cf0a1083aec375d251b0eff328` |
| `results/night2/diagnostics/diag1_eval_paths.py` (unchanged, imported) | `bfb3ca5eb1d20b3084d09cac57e333efae2a34b7ec4b503d60602275d13bd9f1` |
| `results/night2/diagnostics/rowB/rowB.py` (unchanged, imported) | `195a89b555bedf3a0ff00a4c4e0542eafa6370243fbf9ed954f5fe8fbf7f4082` |

**Choices made here, with the line that makes them.**

1. *Import rather than copy* — `ablation_night3.py:37-39, 51-53`. Consequence: the night-2 script is
   byte-identical to the one that produced the night-2 numbers, and hardening item 10 (one
   evaluation entry point) is not violated by a second copy.
2. *The evaluation set and the type order are asserted equal to night 2's*, item for item and
   type for type, read out of `night2/.../ablation_controls.json` — `ablation_night3.py:159-162`.
   Without this the six-run distance table would silently compare two different populations.
3. *The four night-2 profiles are read from `night2/.../ablation_profiles.csv`, not recomputed*
   — `ablation_night3.py:105-141`. `delta_16`, `delta_13`, `delta_10` are recomputed from the 16
   per-item delta columns of that file and checked against its own stored columns: **max
   deviation 9.09e-13** (`night2_csv_recompute_max_dev` in `ablation_distances.json`). The four
   night-2 numbers therefore enter this analysis verified, not assumed.
4. *The normalised profile Δ_T / base divides by the 16-item base loss for all six runs, in all
   three item subsets* — `ablation_night3.py:343-347`. Night 2 divided by the *subset* base
   (`ablation.py:340-347`) but stored only the 16-item base in the CSV, so a subset base is not
   recoverable for the four old runs. One definition across six runs was preferred over matching
   night 2's subset-wise definition for two runs and not the other four. The field is labelled
   `normalized_profile_base` in `ablation_distances.json`. This affects only
   `euclidean_normalized_profiles` on the 13- and 10-item subsets; nothing in the report below
   rests on it.
5. *"Excess" = the signed Δ_T, and the ranking for the registered reading is by signed Δ_T, not
   |Δ_T|* — `ablation_night3.py:452`. The registered quantity is the *cost of silencing a
   type*; a type whose ablation lowers the loss is not a "dependence". Top-3 by |Δ_T| is recorded
   beside it (`top3_by_abs`) and is identical in both new seeds.
6. *Same-wave / cross-wave partition* — `ablation_night3.py:372-384`. (0, 0′) is night 1's pair
   and (3, 4) is night 3's. seed 1 (wave `night2`) and seed 2 (wave `night2b`, a solo re-run
   after the KB5129195 reboot) are **not** a same-wave pair; the 13 remaining pairs are the
   cross-wave set.
7. *The seven invariants are asserted, not only recorded* — `ablation_night3.py:96-103` (rule
   R4 / hardening item 15: a witness with the power to veto). All 138 evaluations of the main run
   and all 66 of the repeat passed all seven.
8. *Noise band and min |Δ_T| written into the output* — `ablation_night3.py:416-425` (hardening
   item 7). Band = 2e-3, the night-2 value (002 §5f, 2026-09-15 note).

## 2. Interpreter, commands, run time

```
PY="C:/Users/mikha/AppData/Local/Temp/claude/.../63f3961a-.../scratchpad/flyvis-probe/.venv/Scripts/python.exe"
OUT="C:/Users/mikha/Documents/dpc-research/connectome-seed/results/night3/diagnostics/ablation"
ND="C:/Users/mikha/AppData/Local/Temp/claude/.../03852100-.../scratchpad/abl3/netdir"

"$PY" "$OUT/ablation_night3.py" --out-dir "$OUT" --netdir-root "$ND"
"$PY" "$OUT/ablation_night3.py" --out-dir "$OUT" --netdir-root "${ND}2" --repeat-only
```

Python 3.10.20, torch 2.9.1+cu128, flyvis 1.2.0, device `cuda`, GPU `NVIDIA RTX PRO 4500
Blackwell`. **67.0 s wall** for the main command — 2 runs × (1 no-ablation + 1 hook-path + 1
empty-set + 2 essential-set + 65 single-type) = 138 evaluations; 66 more for the repeat.

**Run-dir integrity:** all 594 files under `results/flow/9991/{000,900,001,002,003,004}` listed
with size and mtime before and after — `diff` empty, **NO CHANGE to run dirs**. Nothing under
`connectome-seed-data` was written. Nothing was committed. One side effect outside this
directory: importing `rowB.py` created `results/night2/diagnostics/rowB/__pycache__/` (gitignored,
no `.py` file touched — the night-2 sources keep their 2026-09-15 mtimes).

## 3. Controls

### P0 — the evaluator reproduces the stored checkpoint value

| run | label | stored `val_loss` | no-ablation per-item mean | rung-hook value | mean − stored |
|---|---|---|---|---|---|
| 003 | seed 3 | 1155.7706489563 | 1155.7706360817 | 1155.7706546783 | **−1.29e-05** |
| 004 | seed 4 | 1156.8284645081 | 1156.8284053802 | 1156.8284387589 | **−5.91e-05** |

Both inside 1e-3. **P0 passes.** Seed 4's −5.91e-05 is the largest P0 deviation of the six runs; it is still inside the
6.72e-05 evaluation-noise band measured in 002 §5b(b), at 0.88 of the band.

### P1 — ablating the empty set

| run | empty-set mean − P0 mean | max per-item abs diff | bitwise identical |
|---|---|---|---|
| seed 3 | +1.34e-05 | 4.88e-04 | no |
| seed 4 | +6.39e-05 | 4.88e-04 | no |

Same behaviour as night 2 and for the same reason (the masked path allocates a fresh contiguous
tensor). **P1 passes as a no-op at the measurement's own precision; it is not bit-identical**, and
that is recorded as measured.

### P2 — the instrument can see something

| run | P2a: R1–R8 silenced | / base | P2b: the 34 decoder-input types | / base |
|---|---|---|---|---|
| seed 3 | +58.04 | +5.02 % | **+409.92** | **+35.47 %** |
| seed 4 | +79.26 | +6.85 % | **+388.15** | **+33.55 %** |
| *(night 2: seeds 0 / 0′ / 1 / 2)* | *+58.4 / +47.0 / +64.9 / +30,626* | | *+208.6 / +181.4 / +258.9 / +187.6* | *+18.2 / +15.6 / +22.6 / +16.4 %* |

**P2 passes.** Unregistered observation, recorded because it was computed: the trained-vs-constant
span of seeds 3 and 4 (+34 %) is **about twice** that of all four night-2 runs (+16–23 %). Neither
seed 3 nor seed 4 explodes under photoreceptor ablation the way seed 2 does.

## 4. Results — see the report in `docs/experiments/` for the prose

Files:

| file | what |
|---|---|
| `ablation_night3.py` | the driver; imports the night-2 evaluator, hook, statistics and invariants |
| `ablation_profiles.csv` | 130 rows = 2 runs × 65 types, same columns as night 2's |
| `ablation_controls.json` | P0 / P1 / P2a / P2b for seeds 3 and 4, the seven invariants per control, full metadata |
| `ablation_distances.json` | the **15** pairwise distances × 3 item subsets, the 15-pair twin trap, the same-wave pair, six-run sign agreement, noise band, top-10 and the full ranked list per run |
| `ablation_reading.json` | the pre-registered reading of `docs/next-session-plan.md` §2a, evaluated per seed |
| `ablation_repeatability.json` | seed 3's 65 profiles recomputed in a fresh process |

**Headline numbers** (16 items, signed Δ_T):

* Largest single-type dependence: **seed 3 `Mi4` +4,827.5** (3.59× its next type, `L5` +1,346.1);
  **seed 4 `CT1(Lo1)` +10,460.9** (7.96× its next type, `Tm5b` +1,314.1).
* Δ_R2 across the six runs: **+459.2 / +679.8 / −1.0 / +21,157.5 / +146.9 / +41.8**
  (seeds 0 / 0′ / 1 / 2 / 3 / 4). **R2 itself does not repeat.**
* Twin trap on 1−ρ over all **15** pairs: (0, 0′) = 0.2847 is still the global minimum, in all
  three item subsets. Nearest foreign pair is now **(1, 3) = 0.4558** (16 items).
* Twin trap on **Euclidean** over 15 pairs: **now fails** — (0′, 3) = 3,545 and (0, 3) = 4,705 are
  both below the twins' 4,798.
* Same-wave pair (3, 4): 1−ρ = **0.9017**, the **14th of 15** — the two runs of one night are
  nearly the farthest-apart pair in the set.
* Sign agreement 6/6: **39 of 65** types (16 items), all positive. Noise band (|Δ_T| < 2e-3):
  **exactly one type, `Mi11`**, in seed 3 and in seed 4 — the same single type as in all four
  night-2 runs.
* Repeatability (seed 3, fresh process, all 65): **max |ΔΔ_T| = 2.91e-04** (`Tm3`), median
  2.48e-05, ρ = 1.0000, base loss reproduced to 1.9e-06.

## 5. The pre-registered reading, evaluated

`docs/next-session-plan.md` §2a, verbatim: *negative* — if neither seed 3 nor seed 4 shows a
single-type dependence of the size seen in seed 2, the R2 finding remains a single observation;
*positive* (Ark 08:28) — if seed 3 **or** seed 4 shows one type whose excess exceeds **2863**
(the largest twin per-type discrepancy, `T2a`), the R2 finding becomes a repeated observation,
still not a test.

| run | largest Δ_T | value | next type | ratio max/next | > 2863? | order of magnitude above next? |
|---|---|---|---|---|---|---|
| seed 0 | `Tm5c` | +2,616.8 | `Mi4` +1,323.5 | 1.98× | no | no |
| seed 0′ | `Mi4` | +3,266.6 | `T2a` +3,171.9 | 1.03× | yes | no |
| seed 1 | `TmY15` | +3,959.5 | `T2a` +3,651.0 | 1.08× | yes | no |
| seed 2 | `R2` | +21,157.5 | `Mi4` +7,475.9 | 2.83× | yes | **no** |
| **seed 3** | **`Mi4`** | **+4,827.5** | `L5` +1,346.1 | **3.59×** | **yes** | no |
| **seed 4** | **`CT1(Lo1)`** | **+10,460.9** | `Tm5b` +1,314.1 | **7.96×** | **yes** | no |

**Verdict as the rule is written: POSITIVE for both seeds** (`ablation_reading.json`,
`verdict.positive_reading_triggered = true`). Both new seeds carry a single-type dependence above
2,863, so seed 2's R2 finding becomes a **repeated observation — still not a test**.

**Two things must be said with that verdict, both measured here and neither a re-reading of the
rule.**

1. **The 2,863 threshold is not discriminating.** Applied to the runs that already existed, it is
   met by seed 0′ (+3,266.6), seed 1 (+3,959.5) and seed 2 (+21,157.5) — **five of the six runs**
   pass it; only seed 0 does not. Whatever the rule selects, it is not rare.
2. **The rule's second clause is false of its own reference run.** §2a describes seed 2's R2 as
   "an order of magnitude above every other type in that run". It is not: R2 +21,157.5 against
   `Mi4` +7,475.9 is **2.83×**. On the *shape* the clause was reaching for — one type standing far
   above the rest of its own run — **seed 4's `CT1(Lo1)` (7.96×) is a sharper instance than seed
   2's R2 (2.83×)**, and seed 3's `Mi4` (3.59×) is also sharper.

**`R2` itself does not repeat.** Δ_R2 = **+459.2 / +679.8 / −1.0 / +21,157.5 / +146.9 / +41.8**
for seeds 0 / 0′ / 1 / 2 / 3 / 4. Seed 2 remains the only run whose end state collapses without
photoreceptor type R2; seeds 3 and 4 are at the low end of the non-seed-2 range. What repeats is
the *phenomenon class* — some one cell type carries a disproportionate share of an individual's
end state — not the identity of the type. The night-2 four-run numbers were reproduced from the
committed CSV to 9.09e-13 before this comparison was made, and the recorded one-decimal values
(459.2 / 679.8 / −1.0 / 21,157.5) agree with the full-precision values to ≤ 0.045.

**Not read as a test.** n = 6 end states of one configuration on one held-out set, one twin pair,
no null distribution. The type that blows up is different in every run that has one.
