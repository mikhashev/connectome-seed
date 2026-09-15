# Cell-type ablation profiles of the four saved end states — protocol, commands, outputs

**Status: UNREGISTERED DIAGNOSTIC.** This is not a test of hypothesis (b) or (b2) of
`docs/preregistration-cheap-vs-expensive.md`, it is not a rung, and no number here may be
reported as an outcome of the pre-registered experiment. It is a descriptive instrument
applied to four end states that already exist; its own decisive check (the twin trap, below)
is what decides whether the instrument says anything about individual identity at all.

**Asked for by:** Ark (DPC Research chat 2026-09-15 07:39) with Zcode's item-composition
addition (07:43); run on Mike's word (07:43, «делай что можно до ночного прогона»).
**Run by:** CC's subagent (Opus). **Repository HEAD at the time of writing:** `0485e8f`.

Nothing here trains, commits, or writes into `connectome-seed-data`. The four run
directories under `results/flow/9991/{000,900,001,002}` are read with `torch.load` and
`h5py` only; the solver that runs the evaluation lives in a scratch datamate root.

---

## Protocol, fixed before any profile was looked at

This section was written into this file and the file saved **before `ablation.py` was run
for the first time**. Nothing in it was changed afterwards; the results sections below were
appended.

**1. Individuals.** The four saved end states, `results/flow/9991/{000,900,001,002}/chkpts/chkpt_00071`
— iteration 250,008 in the CSV convention (`chkpt_iter.h5` stores 250,007; the mapping is
`diag1_eval_paths.py:chkpt_table`). 000 = seed 0, 900 = seed 0′ (the §7 replicate of seed 0),
001 = seed 1, 002 = seed 2.

**2. Evaluation set.** The registered held-out split (§3 of the pre-registration): 6 scenes,
16 items, batch size 1, augmentation off, all simulation time steps, `t_pre = 0.25`. This is
the same evaluation as the rung hook. Per-item losses are recorded for every ablation.

**3. Intervention.** For one cell type T, the activity of all nodes of type T is clamped to
zero at every integration step of the simulation, with the network otherwise unchanged.

*Mechanism (flyvis's own, not a patch):* `Network.register_state_hook`
(`flyvis/network/network.py:444-469`) registers a callable that is invoked inside
`Network._state_api` (`network.py:430-433`). `_state_api` is called at the end of
`_next_state` (`network.py:413`) — i.e. **after** the Euler state update
(`network.py:404-411`) and **before** the source/target gathers that feed the next step
(`network.py:435-440`) — and also at the end of `_initial_state` (`network.py:375`). The
value `forward` yields to the decoder is `state.nodes.activity` of the state returned by
`_next_state` (`network.py:538-540`), i.e. the hooked value. So a hook that multiplies
`state.nodes.activity` by a 0/1 mask over the 45,669 nodes clamps exactly what the protocol
asks: the clamped activity is what the next velocity sees (`dynamics.py:211,214`) and what
the decoder reads. The hook is registered before `solver.test` is entered, so the grey-screen
steady state (`solver.py:508-513`) is computed with T already silenced too.

*What is clamped:* `state.nodes.activity`, the node's membrane voltage in flyvis's
`PPNeuronIGRSynapses` dynamics (`flyvis/network/dynamics.py:152-218`).

*Why zero and not the resting value.* The voltage is relative to a resting potential — the
trained `nodes_bias` — so zero is not the resting state. Zero is chosen anyway, and this is
the single rule applied to all 65 types, because zero is the **rectification point** in both
places where a node's activity leaves the node: the synaptic current is
`weight * relu(source.activity)` (`dynamics.py:214`, activation `ReLU` in this config) and
the decoder rectifies its input, `x = relu(dvs_channels.output)` (`task/decoder.py:288`).
Activity ≤ 0 therefore transmits nothing and contributes nothing to the readout: clamping to
zero is "this cell type is silent", which is the intended meaning of an ablation. Clamping to
the resting bias instead would leave a constant non-zero output wherever the bias is
positive, which is a different intervention (a "frozen" cell, not a silent one). Rule fixed
before running: **clamp to 0.0, all 65 types, every integration step.**

**4. Profile.** For individual i and type T, `Δ_T = loss(ablate T) − loss(no ablation)` on the
16-item aggregate (the mean over items, the same aggregate the rung reports), plus the 16×65
per-item matrix of per-item Δ. Normalized profile `Δ_T / loss(no ablation)`.

**5. Controls, run and written before any profile comparison.**

* **P0 — the evaluator reproduces the stored value.** The no-ablation evaluation of each of
  the four checkpoints must reproduce the `val_loss` stored inside the checkpoint file to
  ≲ 1e-3.
* **P1 — ablating an empty set is a no-op.** The hook is registered with an all-ones mask
  (no type selected) and the evaluation must return exactly P0. This tests the hook
  machinery, not the biology.
* **P2 — the instrument can see something.** Two sets known to be essential to the readout
  are ablated and the loss increase reported: **P2a** the photoreceptors R1–R8
  (`connectome.input_cell_types`, the only nodes the stimulus is injected into,
  `network/stimulus.py:128-131`), and **P2b** the 34 types the decoder reads from
  (`connectome.output_cell_types`, `task/decoder.py:230`, `utils/activity_utils.py:145`).

**6. Twin trap — the decisive check, pre-declared.** Distances between the four 65-vectors of
Δ_T, Euclidean and Spearman-rank (reported as ρ and as 1−ρ), for all six pairs (0,0′), (0,1),
(0,2), (1,2), (0′,1), (0′,2). **The instrument is informative about individual identity ONLY
if d(0,0′) < d(0,1) and d(0,0′) < d(0,2)** — the twins closer to each other than either is to
a different seed. If the twins are as far apart as different seeds, the profile measures run
noise and is reported as such. Also reported: how many of the 65 types have the same sign of
Δ_T across all four runs, and the top-10 types by |Δ_T| for each run.

**7. Item-composition caveat (Zcode).** The 16-item aggregate is dominated by a few items
(§5b(c), §5c of `docs/experiments/002-night2-seeds-1-and-2.md`). The distances of §6 are
therefore reported three times: on all 16 items, on the 13 items excluding the three
`ambush_2` items, and on the 10 items excluding `ambush_2` and `bandage_1`.

**8. What this cannot show.** A profile distance is a statement about four end states of one
configuration on one held-out set. There is no replicate of the ablation measurement itself
beyond the deterministic-to-1e-4 evaluator noise already measured (§5b(b): 6.7e-5), and there
are only two twins, so the twin trap is a single comparison, not a test with a distribution
under the null.

---

## Interpreter, commands, run time

```
PY="C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/63f3961a-96ce-4048-8338-72c162ea66f8/scratchpad/flyvis-probe/.venv/Scripts/python.exe"
OUT="C:/Users/mikha/Documents/dpc-research/connectome-seed/results/night2/diagnostics/ablation"
ND="C:/Users/mikha/AppData/Local/Temp/claude/c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx/03852100-01fd-45ef-82c3-e22ac607b0f7/scratchpad/abl/netdir"
```

Python 3.10.20, torch 2.9.1+cu128, flyvis 1.2.0, device `cuda`, GPU `NVIDIA RTX PRO 4500
Blackwell` — the night venv, the same interpreter as `../README.md`. `FLYVIS_ROOT_DIR` and
`CUBLAS_WORKSPACE_CONFIG` are set inside `ablation.py` itself (`:21-25`), the same way as
`night/run_individual.py:46-49`, so nothing has to be exported first.

```bash
# snapshot of the four run dirs before anything (repeated after; diff empty)
cd /c/Users/mikha/Documents/dpc-research/connectome-seed-data/results/flow/9991 \
  && find 000 900 001 002 -type f -printf "%p %s %T@\n" | sort > before.txt

# the profiles, controls and distances (this run produced every output file except
# ablation_repeatability.json)
"$PY" "$OUT/ablation.py" --out-dir "$OUT" --netdir-root "$ND"

# POST-HOC repeatability control (Sec 9), a fresh process, writes only ablation_repeatability.json
"$PY" "$OUT/ablation.py" --out-dir "$OUT" --netdir-root "$ND" --repeat-only
```

**Run time:** 113.8 s wall for the whole first command — 4 runs x (1 no-ablation + 1 empty-set
+ 2 essential-set + 65 single-type) = 276 evaluations of the 16 held-out items, 0.18–0.34 s
per evaluation. The repeat command is 260 more evaluations, about 105 s. Peak load on the card
is one 16-item forward pass at batch size 1; it ran while other agents used the same GPU.

**Run-dir integrity:** all 396 files under `results/flow/9991/{000,900,001,002}` listed with
size and mtime before and after — `diff` empty ("NO CHANGE to run dirs"). Nothing under
`connectome-seed-data` was written. Nothing was committed.

## Output files

| file | what |
|---|---|
| `ablation.py` | the script; the evaluator is imported from `../diag1_eval_paths.py`, not re-implemented |
| `ablation_profiles.csv` | 260 rows = 4 runs x 65 types: run, label, type, base loss, delta on 16 items, delta normalized, delta on 13 items, delta on 10 items, and the 16 per-item deltas |
| `ablation_controls.json` | P0 / P1 / P2a / P2b for each of the four runs, plus the full metadata (65 types with node counts, input and output cell types, the 16 item names, the activation) |
| `ablation_distances.json` | the 6 pairwise distances x 3 item subsets, twin-trap verdict, sign agreement, top-10 per run, profile scale |
| `ablation_repeatability.json` | the post-hoc repeat of all 260 single-type profiles in a fresh process (Sec 9) |

---

## Results

### P0 — the evaluator reproduces the stored checkpoint value

| run | label | stored `val_loss` | no-ablation per-item mean | rung-hook value | mean minus stored |
|---|---|---|---|---|---|
| 000 | seed 0 | 1148.8074851 | 1148.8074613 | 1148.8074570 | -2.38e-05 |
| 900 | seed 0' | 1160.9823442 | 1160.9823613 | 1160.9823594 | +1.72e-05 |
| 001 | seed 1 | 1144.6362333 | 1144.6362472 | 1144.6362381 | +1.38e-05 |
| 002 | seed 2 | 1147.7178731 | 1147.7178860 | 1147.7179179 | +1.29e-05 |

All four inside 4.5e-05, i.e. inside the 1e-3 the protocol required and inside the 6.72e-05
evaluation-noise band already measured in `docs/experiments/002-night2-seeds-1-and-2.md`
Sec 5b(b). **P0 passes.**

### P1 — ablating the empty set

| run | empty-set mean minus P0 mean | max per-item abs diff | bitwise identical |
|---|---|---|---|
| seed 0 | +1.29e-05 | 4.88e-04 | no |
| seed 0' | -1.19e-05 | 6.10e-05 | no |
| seed 1 | -3.34e-06 | 2.29e-04 | no |
| seed 2 | +2.91e-05 | 4.88e-04 | no |

**P1 passes as a no-op at the measurement's own precision, but it is NOT bit-identical** and
this is recorded as measured, not as expected. Registering the hook with an all-ones mask
inserts a `state.nodes.activity * mask` multiplication, which is exact in IEEE-754 but
produces a freshly allocated, contiguous tensor where the un-hooked path passes an expanded
view; that changes which reduction kernels run downstream. The resulting aggregate shift is
1.2e-05 to 2.9e-05 — the same order as the P0 deviations and as the Sec 5b(b) noise floor, and
four to five orders of magnitude below the smallest single-type delta reported below. The
largest per-item deviation, 4.88e-04, sits on items whose loss is about 4,000, i.e. 1.2e-07
relative.

### P2 — the instrument can see something

| run | P2a: R1–R8 silenced (the 8 input types) | P2a / base | P2b: the 34 decoder-input types silenced | P2b / base |
|---|---|---|---|---|
| seed 0 | +58.43 | +5.09 % | +208.58 | +18.16 % |
| seed 0' | +47.02 | +4.05 % | +181.38 | +15.62 % |
| seed 1 | +64.87 | +5.67 % | +258.94 | +22.62 % |
| seed 2 | **+30,626.21** | +2,668 % | +187.63 | +16.35 % |

**P2 passes** — every value is orders of magnitude above the noise floor. Two things must be
said with it, both of which bound how the single-type numbers may be read:

1. **The dynamic range of this loss is narrow.** Silencing every one of the 34 types the
   decoder reads leaves the decoder with an all-zero input (the decoder rectifies, so a
   clamped-to-zero cell contributes exactly nothing), i.e. it reduces the network to a
   constant output — and that costs only +16 % to +23 % of the base loss. So the base loss of
   about 1,148 is mostly an irreducible floor, and a single-type delta of, say, +35 (the
   median) is about 0.2 % of base and about 1.7 % of the whole trained-vs-constant span.
2. **Seed 2 is qualitatively different under photoreceptor ablation.** Its +30,626 is not a
   spread-out effect: silencing `R2` alone in seed 2 costs +21,157, against +459 / +680 / -1.0
   for the same type in seeds 0 / 0' / 1. Seed 2's end state diverges when that input is
   removed; nothing in the un-ablated evaluation shows it (seed 2's base loss, 1147.72, is the
   second best of the four).

### The twin trap

Distances between the four 65-vectors of delta_T, all six pairs, on the three item subsets.
`1-rho` is the Spearman distance; `rho` in brackets.

| pair | 16 items: Euclid | 1-rho (rho) | 13 items: Euclid | 1-rho (rho) | 10 items: Euclid | 1-rho (rho) |
|---|---|---|---|---|---|---|
| **(0, 0')** | **4,798.0** | **0.285 (0.715)** | **5,336.2** | **0.297 (0.703)** | **5,622.8** | **0.317 (0.683)** |
| (0, 1) | 6,059.4 | 0.524 (0.476) | 6,888.9 | 0.546 (0.455) | 6,951.7 | 0.624 (0.376) |
| (0, 2) | 22,254.3 | 0.647 (0.353) | 23,092.0 | 0.605 (0.395) | 22,981.5 | 0.584 (0.416) |
| (1, 2) | 22,627.2 | 0.560 (0.440) | 23,606.1 | 0.643 (0.357) | 23,558.0 | 0.613 (0.387) |
| (0', 1) | 5,006.7 | 0.559 (0.441) | 5,880.7 | 0.614 (0.387) | 6,048.5 | 0.595 (0.405) |
| (0', 2) | 21,632.8 | 0.557 (0.443) | 22,379.7 | 0.554 (0.446) | 22,202.0 | 0.543 (0.457) |

**Verdict: the twin trap is passed on both pre-declared metrics and in all three item
subsets** — d(0,0') < d(0,1) and d(0,0') < d(0,2) every time, and in fact d(0,0') is the
smallest of all six pairs in all six columns. On the Spearman metric the separation is clean
(rho = 0.68–0.72 for the twins against 0.35–0.48 for every different-seed pair); on Euclid
among the three non-exploding runs the twin margin is thinner (4,798 against 5,007 for (0',1),
a 4 % margin), and the large Euclidean numbers in the seed-2 rows are carried by the `R2`
divergence described under P2. Euclidean distances between the normalized profiles
(delta_T / base loss) are in `ablation_distances.json` as
`euclidean_normalized_profiles` and give the same ordering.

**A post-hoc metric that disagrees, reported because it was computed.** Pearson r over the
same 65 delta_T (not pre-declared; `pearson_r` in `ablation_distances.json`) puts (0',1) at
r = 0.588 and the twins at r = 0.351 — on that metric the twin trap fails. Pearson is
dominated by the few largest entries, and the twins do not agree on those: the largest single
effect in seed 0 is `Tm5c` at +2,616.8, and in seed 0' the same type is +34.6. So the reading
the two pre-declared metrics support is the weaker one — *the rank ordering of the 65 types is
more similar between twins than between different seeds* — and not the stronger claim that the
twins' biggest-effect types agree. They do not.

### Sign agreement and top-10 types

Types with the same sign of delta_T in all four runs: **44 of 65** on 16 items (all 44
positive; no type is negative in all four), **51 of 65** on 13 items, **43 of 65** on 10 items.
Per run, the number of types whose ablation *lowers* the loss is 7 / 5 / 8 / 9 (seed 0 / 0' /
1 / 2), with the most negative values -5.9 / -6.0 / -5.0 / -14.0; medians of delta_T are
+35.7 / +34.6 / +34.8 / +26.5.

Top 10 types by absolute delta_T, 16 items (all positive):

| rank | seed 0 | seed 0' | seed 1 | seed 2 |
|---|---|---|---|---|
| 1 | Tm5c 2616.8 | Mi4 3266.6 | TmY15 3959.5 | R2 21157.5 |
| 2 | Mi4 1323.5 | T2a 3171.9 | T2a 3651.0 | Mi4 7475.9 |
| 3 | R8 1040.4 | L5 1995.0 | Mi4 2380.2 | Mi2 4434.2 |
| 4 | CT1(M10) 953.4 | R2 679.8 | R8 1622.3 | L1 709.9 |
| 5 | R2 459.2 | CT1(M10) 583.6 | Mi2 1151.7 | T2a 709.2 |
| 6 | T3 427.4 | T2 568.9 | Mi1 530.0 | L4 567.6 |
| 7 | Tm16 379.2 | T4b 567.1 | Tm28 346.3 | R6 547.1 |
| 8 | L5 378.7 | TmY18 328.3 | Tm1 200.5 | CT1(M10) 167.2 |
| 9 | Mi1 363.6 | Mi1 246.1 | Tm30 156.8 | Mi9 165.8 |
| 10 | T2a 308.9 | Tm5b 242.0 | T4d 140.3 | TmY18 123.3 |

`Mi4` is top-3 in all four runs; `T2a`, `Mi1` and `CT1(M10)` recur. Everything else moves.

## 9. Post-hoc control: does the profile repeat? (added after the profiles were computed)

Not part of the fixed protocol — added at CC's initiative after the numbers above existed, and
it cannot change the verdict, only bound the instrument's own repeatability. All 260
single-type profiles were recomputed in a fresh process (`--repeat-only`) and compared to the
first run:

| run | max abs difference between the two repeats | median abs difference | Euclidean distance between the two repeats | Spearman |
|---|---|---|---|---|
| seed 0 | 3.1e-04 (R1) | 5e-05 | 0.0013 | 1.0000 |
| seed 0' | 2.6e-04 (CT1(M10)) | 2e-05 | 0.0004 | 1.0000 |
| seed 1 | 2.4e-04 (T2a) | 2e-05 | 0.0002 | 1.0000 |
| seed 2 | 6.1e-04 (R2) | 2e-05 | 0.0013 | 1.0000 |

The profile of one end state repeats to 6e-04 in its worst entry, and the self-distance of a
profile (about 1e-03) is **six to seven orders of magnitude below** the smallest between-run
distance (4,798). The rank ordering repeats exactly (rho = 1.0000). So none of the between-run
structure above is measurement noise; it is difference between end states. What it is *not* is
a statement with a null distribution: there are two twins and one comparison.
