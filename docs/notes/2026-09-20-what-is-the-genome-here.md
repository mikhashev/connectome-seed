---
**Status:** NOTE — descriptive; registers nothing, decides nothing. Written by CC, 2026-09-20,
the deliverable assigned in `docs/plans/2026-09-16-functional-readout-plan.md` § "Step 3 —
genome" and `docs/briefs/2026-09-19-genome-track-handover.md` §2.
**Method:** every structural claim was read from the source named beside it and every count
recomputed this session from the compiled connectome and a committed run record; claims are
marked **Observed** or **Inferred**. **No measured results** — every number is a structural
integer from code, config or a compiled table
(`docs/decisions/003-blind-authorship-after-the-numbers.md`).
---

# What is the genome here

## 1. What one individual is made of

The whole parameter content of a network is five tensors, and a checkpoint carries exactly
those five (`connectome-seed-data/results/flow/9992/000/chkpts/chkpt_00000`, key `network` —
**Observed**, read this session):

| tensor | count | grouped by | trainable | seeded | initial value from |
|---|---|---|---|---|---|
| `nodes_bias` | 65 | cell type | yes | **yes** | a sampled Normal, `bias.yaml:3-9` |
| `nodes_time_const` | 65 | cell type | yes | no | a constant, `time_const.yaml:4-5` |
| `edges_syn_strength` | 604 | (source_type, target_type) | yes | no | ρ / ⟨N⟩ per pair, `initialization.py:500-505` |
| `edges_sign` | 604 | (source_type, target_type) | **no** | no | the json's `alpha`, `connectome.py:429` |
| `edges_syn_count` | 2355 | (source_type, target_type, du, dv) | **no** | no | the json's offsets, `initialization.py:441-451` |

Trainable total **734** = 65 + 65 + 604; fixed total **2,959** = 604 + 2,355. **Observed**, three
ways: `results/night2/diagnostics/diag2_requires_grad.json`; `n_params.network_trainable` in the
run's own `results/night5/night5_9992-000.slim.json`; and my recount of the compiled tables (§2).
The handover's 734 and its 65 seeded biases are both correct. The decoder adds **7,427**
trainable parameters (same json) — not connectome-constrained, and not invariant between
individuals (§3).

Grouping is what keeps the counts small (`initialization.py:345-357`, `:371-383`, `:401-418`,
`:441-464`, `:496-517`): all 45,669 cells of a type share one bias, all 1,513,231 synapse
instances of a type pair share one strength. **Observed.**

## 2. The table those parameters sit on

`fib25-fib19_v2.2.json` (**Observed**, parsed this session) holds `nodes` (65), `edges` (605),
`receptors` (empty), `input_units` (8), `output_units` (34). A node carries `name` and a
`pattern` — `["stride", [1,1]]` for 63 types, `["stride", [3,2]]` for 2 (Lawf1, Lawf2). An edge
carries `src`, `tar`, `alpha` (the sign, ±1), `lambda_mult`, `edge_type`, `alpha_fixed` (true on
272 entries, which carry literature citations in `alpha_references`) and `offsets`: a list of
`[[du, dv], n_synapses]` — **2,140 offset rows over the 605 entries**, 1 to 26 per entry, no |du|
or |dv| above 6. Only part is read: `name`/`pattern` from a node,
`src`/`tar`/`alpha`/`offsets`/`lambda_mult` from an edge (`connectome.py:182`, `:226-227`,
`:419-432`). The json's own node `bias` field is **not** read and is unrelated to the seeded bias
of §1 — worth saying, because the name invites the confusion.

Compiled at `extent: 15`: 45,669 cells and 1,513,231 edge instances, collapsing to **604**
distinct `(source_type, target_type)` pairs and **2,355** distinct
`(source_type, target_type, du, dv)` rows (**Observed**, recomputed from
`connectome-seed-data/connectome/ConnectomeFromAvgFilters_0000/edges/*.h5`). Against the json:
2,117 offset rows match a bank row one-to-one, 238 bank rows are added by the convex-hull fill
(`connectome.py:435-470`, `n_syn_fill: 1`), 23 json rows are dropped — all Lawf1/Lawf2
self-offsets that never land on their own `stride [3, 2]` lattice, suppressed by the `KeyError`
guard at `connectome.py:497-498`. This reproduces the plan's Step-3 boundary figures exactly.

## 3. So what plays the role of a genome today

**Inherited, identical in every individual:** the json and its per-run sha256 (`slim.json` key
`connectome_sha256`), the compiled tables, the form of all five parameter groups and the initial
values of four of them. Gate 7 holds the resolved config invariant across all ten runs, the only
varying fields being `ensemble_and_network_id`, `network_name`, `description`, `seed`
(`docs/experiments/005-night5-third-runs-of-seed-0-and-seed-3.md` §3). **Observed.**

**Seeded:** among network parameters, only `nodes_bias`. `bias.yaml:4-7` sets
`initial_dist: Normal`, `mode: sample`, `seed`; `Normal.__init__` opens a private
`torch.Generator`, seeds it and draws (`initialization.py:153-178`) — 65 independent draws, one
per cell type. The rest is deterministic: `time_const`, `syn_strength` and `sign` use `Value`,
`syn_count` uses `Lognormal` with `mode: mean`, which returns the mean without touching an RNG
(`initialization.py:156-157`). **Observed.**

**But the seed does not stop there.** `run_individual.py` takes one `--seed` and spends it
twice: as `network.node_config.bias.seed` (`:356`, asserted at `:408-409`) *and* as the global
`random`/`numpy`/`torch` seed, set before the solver is built (`:282-284`) and again before
training (`:703-705`, commented "data order / augmentation stream"). Two individuals therefore
differ in their 65 biases **and** in the decoder's 7,427 initial weights **and** in the order and
augmentation of the training stream. The handover's §3 sentence that the 65 biases "are the
whole of individuality" holds of the *network parameters*, not of the individual; the confound is
already on record in `docs/next-session-plan.md` (the bias-only / order-only 2×2, Ark and Zcode,
2026-09-15). **Observed** — a correction to the handover, not a new finding.

**Learned:** all 734, by Adam (`optim.yaml`). `nodes_bias` alone gets a second optimiser: it is
the only group configured `penalize: {activity: true}` (`bias.yaml:11-12`), hence the only member
of `param_list_act_pen` (`solver.py:746-764`), and that optimiser is dropped once the iteration
reaches `stop_iter` (`solver.py:822-828`) — 150,000 of `n_iters: 250000` (`penalizer.yaml:4`,
`task.yaml:44`). The two `weight_decay` entries on the edge parameters are inert: `lambda` is
zero and the guard at `solver.py:747` requires a non-zero kwarg. **Observed.**

So the genome today is **the json plus the type-level parameter tables plus the config** —
shared and unchanged across all ten runs — and an individual is **a point in a 65-dimensional
initial-condition space over identical wiring**. That is an initial condition, not a genome in
the generative sense: the map from seed to individual is 65 independent draws from one
distribution, with no production, no composition, no reuse, and no way for a mutation to add a
cell type, a type pair, an offset or a sign. **Inferred**, from §1–§3 together.

## 4. Phenotype and the readouts that exist

The phenotype is the trained network plus decoder, expressed as behaviour on held-out Sintel
flow. On disk (**Observed**): aggregate held-out loss at every checkpoint for ten runs
(`results/night5/night_report_checkpoints.csv`, with its explicit `run_columns.csv` mapping);
72 checkpoints per canonical run, each carrying all five tensors, so **the 65-bias profile is
readable at every checkpoint with no GPU**; per-cell-type activity profiles
(`results/night2/diagnostics/rowB/`, `results/night3/diagnostics/rowB/`); ablation profiles
(`.../ablation/`); input-condition diagnostics (`results/diagnostics/gray/`); weight-distance
trajectories (`.../weight_distance_trajectory.csv`). The tuning battery is specified
(`docs/briefs/2026-09-16-step2-tuning-battery.md`) and not run. **No readout on disk is a
function of the 65 biases as such** — weight-distance groups by parameter family, row B measures
activity. The bias trajectory (65 × 72 checkpoints × 10 runs) is not in
`results/night2/diagnostics/`, `results/night3/diagnostics/` or `results/diagnostics/`. That is
the blocked extraction step.

## 5. What a grammar would have to be

A grammar for the elephant goal is a compact rule that **generates the wiring table** — the cell
types, the per-type-pair offset lists with their counts, and the signs — not parameters laid on a
fixed table. The substrate already contains exactly one such rule: `pattern` is a production. `add_strided_nodes` (`connectome.py:326-343`) expands a single token
over the hex disc of radius `extent`, keeping `u % u_stride == 0 and v % v_stride == 0`. The disc
holds 3n²+3n+1 columns — 721 at extent 15, 91 at extent 5 — so 63 types at stride [1,1] plus 2 at
stride [3,2] give 63·721 + 2·123 = 45,669 cells and 63·91 + 2·13 = 5,759, matching both the
compiled table and `VISION.md`. And the bank is invariant under that parameter: I compiled the
`(source_type, target_type, du, dv)` table at extent 5 and at extent 15, and they agree on all
2,355 keys, with identical signs and zero difference in `n_syn`. **Observed**, both computed
this session.

So the substrate is a grammar of **one production — "tile this column motif over a hex disc of
radius n" — over a non-generative lookup table of 605 entries and 2,140 offsets.** What the
production does not cover: the 65 cell-type names, which are a literal list; which pairs connect,
at which offsets, with which counts or signs; any relation between one type pair and another, so
there is no family, symmetry group or series inside the bank for a rule to be fitted to as it
stands; and within-type specificity, discarded by construction. The practical consequence is the
one `ROADMAP.md` already states: raising `extent` adds columns, not types or motifs — scale, not
grammar. **Inferred**, from the two Observed paragraphs above.

## 6. Open questions the design must settle

1. **Which object is the rule fitted to — the json or the compiled bank?** The plan's Step-3
   boundary fences this (S2/C6 fit the bank; the json → bank transition is licensed by neither).
   Name one: 605 entries with 2,140 offsets, or 604 pairs with 2,355 rows including the 238
   hull-filled.
2. **Which fields may a predictor see?** `alpha_fixed` is true on 272 entries and
   `alpha_references` names the papers. If sign is the label, are these admissible predictors or
   leakage from the literature the readout is judged against?
3. **What is the held-out unit** — a row, an offset within a pair, a type pair (604), or a cell
   type (65)? Splitting by row leaks a pair's remaining offsets, and C6 must be specified against
   the same unit or it controls nothing.
4. **Does the population stay seed-only?** Any generative claim needs structural variation, which
   `docs/preregistration-cheap-vs-expensive.md` §8 fences off and which the bias-only /
   order-only 2×2 of `docs/next-session-plan.md` must precede (see §3).
5. **Which side of 150,000?** The bias is the only penalised group and the penalty stops at
   150,000 of 250,000, so a bias-profile statistic read across the 25,000 and 250,000 rungs spans
   two regularisation regimes. Before, after, or both — stated in advance.

**Field list the extraction would need**, once (1)–(3) are answered: per bank row —
`source_type`, `target_type`, `du`, `dv`, `n_syn`, `sign`, `n_syn_certainty`, plus provenance
flags `in_json` / `hull_filled` / `dropped`; per json entry — `alpha`, `alpha_fixed`,
`alpha_references`, `edge_type`, `lambda_mult`, raw `n_synapses`; per cell type — `name`,
`pattern` kind and strides, `role`, `central_cells_index`; per extraction — `extent`,
`n_syn_fill`, the connectome sha256, and the split-unit label.

## 7. What this note does not claim

It does not claim the 65 biases are the only thing distinguishing two of our individuals — §3
says the opposite. It does not claim a grammar exists, that the bank is learnable, or that any
rule family would fit it; it describes the shape of the object a rule would have to produce. It
reports no measured result and licenses no reading of any night. It does not draw the boundary of
§6(1), which is Ark's, and it registers nothing.
