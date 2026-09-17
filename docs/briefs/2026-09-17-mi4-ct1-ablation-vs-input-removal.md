# Brief — type ablation versus input removal, for Mi4 (seed 3) and CT1(Lo1) (seed 4)

**v1, 2026-09-17 (UTC; 2026-09-18 local, UTC+7).** **Status: DRAFT, awaiting review.** **Written
by:** CC (draft for review by Ark and Zcode before launch). **Not registered, not scheduled, not
approved.** This file decides nothing and launches nothing; it fixes a protocol so that whoever
reads the data next reads it against readings written down first. Launch requires Mike's explicit
word in the DPC Research chat, after the reviewer pass, exactly as every other brief in this
repository (`docs/briefs/2026-09-16-step1-gray-stimulus.md`, header).

Path aliases, following the convention of the template brief:
`FV` = `.../scratchpad/flyvis-probe/.venv/Lib/site-packages/flyvis` (flyvis 1.2.0)
`CS` = `C:\Users\mikha\Documents\dpc-research\connectome-seed`
`CSD` = `C:\Users\mikha\Documents\dpc-research\connectome-seed-data`

## 1. The question, in one sentence, and why it is owed now

**Does silencing Mi4 in seed 3, and silencing CT1(Lo1) in seed 4, measure the fly, or does it
measure the apparatus?**

This is item 6 of the current order of work, named as independent of the endpoint gate and
"never...set": *"the 'type ablation versus input removal' control for Mi4 and CT1(Lo1), which has
never been set"* (`docs/plans/2026-09-17-endpoint-before-n.md:108-112`).

It is owed now because the sibling case has already been resolved, and resolved *against* the
interesting reading. Seed 2's dominant-ablation type, R2, was found to explode under the existing
forced-zero clamp (+21,157.5 at 16 items) — but the gray-stimulus control (commit `32759e2`,
`results/diagnostics/gray/README.md`) showed seed 2 does **not** explode under either a
physiologically neutral input (gray, 0.5) or a literal absence of input (all-zero input): *"Neither
explodes, so the branch in the brief's words is: 'explosion only under the ablation's forced-zero
state, i.e. neither (a) nor (b) explode -> the ablation deltas ... measure the dynamics' fragility
to a zero clamp specifically, an instrument artefact, not a vision dependence, and the R2 ablation
finding must be reworded accordingly.'"* (`results/diagnostics/gray/README.md:204-208`). R2 was
resolved by contrasting the clamp against **input manipulation**, not by re-examining the clamp
itself.

The night-3 ablation record found the same *shape* — one type carrying a disproportionate share of
the single-type ablation delta — repeating in seed 3 (Mi4) and seed 4 (CT1(Lo1)), while explicitly
noting that R2 itself, the specific type, did not repeat: *"the class (one type carries a
disproportionate share) repeats, the type does not"*
(`docs/experiments/003-night3-seeds-3-and-4.md:284-286`). The gray-stimulus control tested R2's
*case*, not the *class*. Whether Mi4 and CT1(Lo1) are the same artefact as R2, or a real
type-specific dependence, has never been tested by anything other than the clamp itself.

## 2. The two interventions, stated precisely

Both interventions act on the trained network at checkpoint `chkpt_00071` (solver iteration
250,008) — the same checkpoint the night-3 ablation used
(`results/night2/diagnostics/ablation/ablation.py:42`, and independently corroborated: the stored
`val_loss` recorded in `ablation_controls.json` for seed 3 and seed 4, `1155.7706...` and
`1156.8284...`, match the iteration-250,008 row of the night-4 checkpoint table,
`docs/experiments/004-night4-replicate-3prime-and-seed-5.md:128`), on the same 16 held-out Sintel
items used by every diagnostic in this repository (`D.val_item_names(solver)`,
`results/night2/diagnostics/diag1_eval_paths.py:204`; item names visible verbatim in the header row
of `results/night3/diagnostics/ablation/ablation_profiles.csv:1`).

The network's dynamics, read from source, are:

```
params.edges.weight = params.edges.sign * params.edges.syn_count * params.edges.syn_strength
                                                              (FV/network/dynamics.py:165-167)

vel.nodes.activity = 1/max(time_const, dt) * ( -activity + bias
                        + target_sum(weight * activation(sources.activity))   # synaptic drive
                        + x_t )                                # external stimulus (photoreceptors)
                                                              (FV/network/dynamics.py:207-218)
```

`weight` is built once per forward call, from the **registered parameter** `net.edges_syn_strength`
(and `net.edges_sign`, `net.edges_syn_count`), grouped by `(source_type, target_type)`
(`FV/network/network.py:113-120,190-207`); each group's `(source_type, target_type)` pair is
recorded in that parameter's own `.keys` list, and each edge's group membership in its own
`.indices` (`FV/network/initialization.py:393-419`). `_param_api()` builds `params.edges.*` from
these once at the start of `forward()`/`simulate()`, not per timestep
(`FV/network/network.py:509-540` calls `_param_api()` at line 529; `:628-830` calls it again at
line 830 for the other entry point) — so editing the registered parameter before a forward call and
restoring it after is sufficient; there is no per-step re-derivation to fight.

**(a) The existing forced-zero clamp of the type's activity — as the night ablation does it,
unchanged.** For type `T`, a state hook multiplies `state.nodes.activity` for every node of type
`T` by 0, at the end of **every** `_state_api` call — both `_initial_state` (the grey steady state)
and every `_next_state` during the rollout (`FV/network/network.py:353-375,377-413,415-433`,
hook loop at `:430-433`; registered via `register_state_hook`/`clear_state_hooks`,
`FV/network/network.py:444-478`). The implementation is
`results/night2/diagnostics/ablation/ablation.py:63-84` (`ablate_hook`), invoked per evaluation by
`eval_items` (`:101-112`), which asserts `net._state_hooks == ()` both before registering the hook
and after clearing it. **This clamp forces `T`'s own state to exactly zero at all times** — it
removes what `T` contributes to every downstream neuron (via the source-gather step feeding
`target_sum`), removes `T`'s own bias-driven resting drive, and — for a type in R1–R8 — removes the
external-stimulus contribution too, all three at once, continuously through the rollout.

**(b) Input removal — zeroing the incoming edge weights of that type, not its state.** Zero
`net.edges_syn_strength` (equivalently, the resulting `weight`) **only for the groups whose
`target_type == T`**, found from that parameter's `.keys` list
(`FV/network/initialization.py:413-417`); leave `state.nodes.activity` for `T`'s own nodes free to
evolve from `bias` and, for a type in R1–R8, `x_t` alone; leave every edge whose **source** type is
`T` untouched, so `T`'s own projection to its downstream targets carries whatever value `T`'s
now-input-starved activity settles at, rather than being forced to zero. **Concretely, this removes
only what `T` receives from other neurons through the connectome — the synaptic channel into `T` —
and leaves `T`'s own membrane dynamics and its outward projections alone.** This is a materially
different lesion from (a): (a) deletes `T` as a unit (input processing and output signal, at every
instant); (b) deletes only the wiring feeding `T`, leaving `T` to still drive its downstream targets
on whatever bias/external-stimulus-only activity remains.

**No existing script implements (b).** `ablation.py` and `ablation_night3.py` implement only (a);
neither the evaluator (`diag1_eval_paths.py`) nor any diagnostic script in this repository edits
`net.edges_syn_strength`, `net.edges_sign`, or `net.edges_syn_count`. **This brief states plainly
that (b) requires new code.** The smallest addition, following the reuse convention every other
diagnostic in this repository uses (`results/night3/diagnostics/ablation/ablation_night3.py:1-20`,
"NOTHING OF THE PROTOCOL IS RE-IMPLEMENTED HERE"):

1. Import `diag1_eval_paths as D` and `ablation as ABL` exactly as `ablation_night3.py` does; reuse
   `D.build_solver`, `D.chkpt_table`, `D.load_checkpoint`, `D.per_item_eval`,
   `ABL.node_type_array`, and `ABL.CHKPT` unmodified.
2. For a target type `T`: read `net.edge_params["syn_strength"].keys` to find the indices of every
   group with `target_type == T`; save `net.edges_syn_strength.data[idx].clone()`; set those
   entries to `0.0`; call `D.per_item_eval(solver)` unmodified (no hook registered, no other
   change); restore the saved values; **assert** the restored tensor is bit-identical to a saved
   full-tensor snapshot taken before the edit — the same role `assert net._state_hooks == ()` plays
   for intervention (a) (`ablation.py:104,111`).
3. Do not register a state hook during this call (`net._state_hooks == ()` should hold before and
   after, same assertion, so the two interventions are never mixed inside one evaluation).
4. Do not edit `diag1_eval_paths.py`, `ablation.py`, or `ablation_night3.py` — read-only reuse, per
   this repository's convention (`docs/briefs/2026-09-16-step1-gray-stimulus.md:97`, "Do not edit").

This is comparable in size to `results/diagnostics/gray/gray_stimulus.py`, and smaller, since it
does not need that script's four-condition/permutation machinery — it needs only the group-index
lookup and the save/zero/evaluate/restore sequence above.

## 3. Targets, null cell and positive control

All four cells below use the **same checkpoint, same 16 items, same baseline** already on record —
no new P0 evaluation is needed, only the four new-intervention evaluations (two seeds × two cells:
target + positive-control set; the null cell is read the same way per seed).

| role | seed | type(s) | baseline (`base_loss_16`) | clamp Δ (existing, (a)) | Δ in gain_s units |
|---|---|---|---|---|---|
| **target** | 3 | Mi4 | `1155.7706360816956` | `+4827.536294460297` | ≈85×gain_s(seed3) |
| **target** | 4 | CT1(Lo1) | `1156.828405380249` | `+10460.885339736938` | ≈188×gain_s(seed4) |
| **null** | 3 | Mi11 | `1155.7706360816956` | `+2.384185791015625e-06` | ≈0 |
| **null** | 4 | Mi11 | `1156.828405380249` | `+4.291534423828125e-05` | ≈0 |
| **positive control** | 3 | 34 output/decoder-input types (P2b) | `1155.7706360816956` | `+409.9218420982361` | ≈7.2×gain_s(seed3) |
| **positive control** | 4 | 34 output/decoder-input types (P2b) | `1156.828405380249` | `+388.1520709991455` | ≈7.0×gain_s(seed4) |

Sources: Mi4 row — `results/night3/diagnostics/ablation/ablation_profiles.csv:25`; CT1(Lo1) row —
`:85`; Mi11 rows — `:28` (seed 3), `:93` (seed 4); these three also quoted rounded in
`docs/experiments/003-night3-seeds-3-and-4.md:277-278` (Mi4 4827.5, CT1(Lo1) 10,460.9) and `:298`
("noise band |Δ_T| < 2e-3: Mi11 only in seeds 3 and 4"). P2b (the 34-type output set) delta and
type list — `results/night3/diagnostics/ablation/ablation_controls.json:284-319` (the 34 types,
`T1`...`TmY18`), `:321` (seed 3 delta), `:457` (seed 4 delta); quoted rounded in
`docs/experiments/003-night3-seeds-3-and-4.md:265-268`. `gain_s`(seed 3) = `56.7791`
(`docs/experiments/004-night4-replicate-3prime-and-seed-5.md:156`); `gain_s`(seed 4) = `55.7095`
(`docs/experiments/004-night4-replicate-3prime-and-seed-5.md:160-161`). The gain_s-unit figures
above are my own arithmetic (division), marked "≈".

**Why the 34-type output set, not R1–R8, is the positive control.** R1–R8 (the photoreceptors) are
the network's external-stimulus entry point, not primarily recipients of recurrent synaptic drive —
under condition (a) they are also where the gray-stimulus brief's own input manipulations act
(`docs/briefs/2026-09-16-step1-gray-stimulus.md:82-96`). Input removal on a type whose main drive is
external stimulus, not synapses, risks being close to a no-op for reasons that have nothing to do
with whether the instrument works. The 34 output/decoder-input types are, by construction, the types
the decoder reads from — cells that must integrate substantial upstream synaptic input to carry a
useful signal — and their existing clamp delta (+409.92 / +388.15, ≈7×gain_s) is a large, clearly
non-null, already-measured effect (`ablation_controls.json:321,457`), unlike R1–R8's own clamp delta
for seeds 3/4 (+58.04 / +79.26, ≈1.0-1.4×gain_s, `ablation_controls.json:282,418` — much smaller
than seed 2's +30,626 outlier, and not chosen here for that reason too).

## 4. Pre-registered readings, fixed before any data

Define, for a target type `T` and seed `s`, using the **same** operationalisation and the **same**
thresholds already pre-registered for R2 in the template brief
(`docs/briefs/2026-09-16-step1-gray-stimulus.md:213-220`):

```
excess_(a)(T, s) = clamp_delta(T, s)              [already measured, table in §3]
excess_(b)(T, s) = mean16(loss under input-removal(T), same checkpoint) - base_loss_16(s)
                                                   [the new measurement]

excess >= 10 * gain_s(s)  -> "explodes"
excess <= 0.1 * gain_s(s) -> "returns"
otherwise                 -> "between"
```

`excess_(a)` is already known for both targets: Mi4 (seed 3) and CT1(Lo1) (seed 4) both **explode**
under (a), ≈85× and ≈188× `gain_s` respectively (§3). The branch below is decided entirely by
`excess_(b)`, computed once per target and never re-thresholded after looking.

- **`excess_(b)(T, s)` also explodes (>= 10×gain_s)** -> the dominant-type finding is a genuine
  dependence on that type's **synaptic input**: removing only what `T` receives (leaving `T`'s bias
  and, if applicable, external drive, and leaving `T`'s own downstream projections free) degrades
  performance about as severely as forcing `T`'s whole state to zero. The two instruments agree ->
  supports a real functional dependence, not a clamp artefact.
- **`excess_(b)(T, s)` returns (<= 0.1×gain_s)** -> the ablation delta for that type is, like R2,
  fragility to the forced-zero clamp specifically: `T` still receiving no useful synaptic drive
  barely moves the loss, while forcibly zeroing `T`'s own state (also erasing its bias-driven
  resting output and anything it would otherwise still contribute downstream) breaks the network far
  more. This is an instrument artefact of the clamp, and the R2 reword
  (`results/diagnostics/gray/README.md:204-208`) would extend to that type.
- **`excess_(b)(T, s)` is "between"** -> recorded as inconclusive for that type at this checkpoint;
  no branch is forced; this control alone does not resolve it.
- **Mi4 and CT1(Lo1) land on different branches from each other** -> recorded as such, not
  reconciled here: the class (one type carrying a disproportionate ablation share) would then not
  have one shared explanation across the two individuals, consistent with the night-3 record's own
  observation that "the class...repeats, the type does not"
  (`docs/experiments/003-night3-seeds-3-and-4.md:284-286`) — this control would extend that to two
  possible *mechanisms* as well, not just two types.

**Null cell (Mi11, both seeds).** Passes if `excess_(b)(Mi11, s)` stays within a tolerance of
`1e-3` — the nearest measured floor for a comparison of this shape in this repository, the P0
reproduction ceiling from the template brief
(`docs/briefs/2026-09-16-step1-gray-stimulus.md:141-146`), adopted here for lack of an
input-removal-specific floor (none has been measured; see §6 and §8). If Mi11 shows an excess
comparable in scale to the target types under (b), the group-index bookkeeping in the new script is
almost certainly wrong — see §5, void condition 2.

**Positive control (the 34-type output set, both seeds).** Passes if `excess_(b)` for that set is
unambiguously nonzero: above the same `1e-3` tolerance and at least "between" on the gain_s scale
(> 0.1×gain_s), given the clamp channel already shows ≈7×gain_s for the same set (§3). If it reads
at or near zero, the instrument cannot see an effect already known to exist under (a) — see §5, void
condition 1.

## 5. What would make the reading void

1. **Positive control fails** — the 34-type output set shows `excess_(b)` indistinguishable from
   zero (within the `1e-3` tolerance) in either seed. The instrument is then not shown to be able to
   detect an effect known to exist; nothing else in this brief is interpretable until this is
   understood.
2. **Null cell fails** — Mi11 shows a large `excess_(b)` in either seed, comparable in scale to a
   target type. This points to a bug in the group-index selection (e.g. zeroing entries belonging to
   a shared `(source_type, target_type)` group that also feeds other types, or an off-by-one in
   `.keys`/`.indices`), not a real Mi11 effect — the target-type readings are void until the
   selection is verified independently (e.g. by counting edges via `net._target_indices` together
   with the node-type array, not only trusting `.keys`, matching checklist rule 15's "verified by
   recomputation from the primary file" convention, `docs/CHECKLIST-research-repo.md:43-50`).
3. **Restoration is not bit-identical.** If the saved-and-restored `net.edges_syn_strength` (or
   whichever parameter is edited) does not compare bit-identical to its pre-edit snapshot before and
   after each cell, that cell is void and the run stops — the same role
   `assert net._state_hooks == ()` plays for intervention (a).
4. **NaN or Inf in any evaluation** — stop, as in the template brief's Stops list
   (`docs/briefs/2026-09-16-step1-gray-stimulus.md:180-183`).
5. **The reused numbers do not match a fresh read at execution time.** The clamp deltas, `gain_s`
   figures and P2b deltas cited in §3 are read from committed files as of this draft; if
   `ablation_profiles.csv`, `ablation_controls.json`, or the night-3/night-4 experiment docs are
   amended before this control runs, the executor must re-read them, not reuse the numbers printed
   here (checklist rule 15, `docs/CHECKLIST-research-repo.md:43-50`).
6. **Any target, null or positive-control type turns out to have no incoming-edge groups at all**
   (i.e. no entry in `parameter.keys` with that type as `target_type`) — input removal would then be
   a no-op for that type by construction, not a real intervention, and the cell must be flagged VOID
   rather than silently scored as "returns." **This has not been checked** — see §8.

## 6. Cost — ESTIMATE, not a measurement

No training. No new checkpoints. Reads the same stored checkpoints the night-3 ablation already
read: `CSD/results/flow/9991/003/chkpts/chkpt_00071` (seed 3) and
`CSD/results/flow/9991/004/chkpts/chkpt_00071` (seed 4) — `torch.load` only, same as
`ablation.py`/`ablation_night3.py`.

New evaluations needed: 2 seeds × 2 new cells each (target type + the 34-type positive-control set;
the null cell reuses the same per-type sweep pattern) — at minimum 4 new sixteen-item evaluations,
single call each. Measured single-call costs on this exact evaluation path: 0.18–0.34 s per
evaluation over 276 calls in night 2 (`results/night2/diagnostics/ablation/README.md:130-131`), and
`one_evaluation_wall_s` 0.492 s (seed 3) / 0.179 s (seed 4) recorded per-run in night 3
(`results/night3/diagnostics/ablation/ablation_controls.json:323,459`). Four such calls: on the
order of 1–2 s of pure evaluation wall time. Solver build overhead is not separately measured in
these files, but night 2's whole run — 4 solver builds plus 276 evaluations — took 113.8 s total
(`results/night2/diagnostics/ablation/README.md:130`), so two solver builds plus a handful of
evaluations should be well under one minute. **If the same multi-call robustness convention the
gray-stimulus brief adopted after its third gate stop (checklist rule 17,
`docs/CHECKLIST-research-repo.md:61-70`) were used here too** — five calls per cell, plus a
fresh-process repeat — the same four cells become on the order of 40 calls, still on the order of
seconds to low tens of seconds of pure evaluation time. **This entire section is an estimate
extrapolated from other scripts' measured costs, not a measurement of this control**, and it does
not include the time to write and exercise the new script from §2. No dedicated GPU allocation is
described anywhere in this repository's diagnostics as required for a run of this size; existing
runs of the same evaluator used `flyvis.device` (CUDA when available), and this control would use
the same default.

## 7. Boundaries — what this control will NOT establish

- **It decides nothing about R2 or seed 2.** That case is already resolved, by the gray-stimulus
  control, against the vision-dependence reading (`results/diagnostics/gray/README.md:204-208`,
  commit `32759e2`). This brief is about Mi4 (seed 3) and CT1(Lo1) (seed 4) only.
- **It is not an endpoint test.** It has no bearing on the reachability/ranking endpoint gated in
  `docs/plans/2026-09-17-endpoint-before-n.md`, which this control is explicitly listed as
  independent of (`docs/plans/2026-09-17-endpoint-before-n.md:108-112`).
- **Single checkpoint only** (`chkpt_00071`, iteration 250,008). Says nothing about earlier
  checkpoints or the training trajectory.
- **n = 1 per seed**, no replicate of the input-removal measurement itself. This control cannot
  distinguish "a genuine but individual-specific dependence" from "a seed-idiosyncratic
  fluctuation" the way a twin/replicate pair could.
- **The positive control is coarse, not scale-matched.** The 34-type output set is a much larger
  intervention than a single-type removal; passing it shows the instrument can detect *some* known
  effect, not that it has the same sensitivity at the scale of one type's contribution — a
  gross-functioning control, in the same sense the template brief's own positive control was later
  flagged as testing "gross functioning, not resolution"
  (`docs/plans/2026-09-17-endpoint-before-n.md:179-183`, item (j), about a different instrument).
- **It does not establish mechanism.** At most it tells us whether the loss is sensitive to `T`'s
  own node state or to `T`'s synaptic input; it does not identify which upstream types, or which
  downstream pathway, carries the dependence.
- **Not verified: whether Mi4, CT1(Lo1), Mi11, or the 34 output types actually have any
  incoming-edge groups in this connectome** — i.e. whether input removal is non-vacuous for each of
  them. No diagnostic or data read was run to check this while drafting this brief, per the task
  that produced it ("You will NOT run any experiment, training, evaluation or diagnostic script").
  This is void condition 6 in §5, and it must be the new script's first check, before any reading is
  interpreted.
- **No number in this brief beyond the code-path descriptions in §2 has been independently
  re-verified by recomputation** — the deltas and gain_s figures in §3 are read once from the cited
  files; checklist rule 15 requires recomputation from the primary file before any table is used in
  a verdict, and that recomputation has not been done here (it is a task for the executor, at
  execution time, per void condition 5 in §5).

## 8. Do not

1. Do not train, do not call `solver.checkpoint()` or `solver.test(track_loss=True)`.
2. Do not write anything under `CSD/results/flow/9991/**`; list all files with size and mtime before
   and after, as every prior diagnostic in this repository does.
3. Do not edit `diag1_eval_paths.py`, `ablation.py`, or `ablation_night3.py` — reuse only, per §2.
4. Do not leave `net.edges_syn_strength` (or whichever parameter is edited) modified after a cell —
   restore and assert bit-identical, per §5 condition 3.
5. Do not register a state hook during an input-removal evaluation, and do not edit edge parameters
   during a state-clamp evaluation — keep the two interventions in separate calls.
6. Do not round any number in a csv or json; use `repr(float(x))`, matching every other diagnostic
   here.
7. Do not commit, do not push, do not touch the `connectome-seed` working tree beyond a new,
   separate output directory for this control (this brief does not name one; the executor names it
   when the control is registered).
8. Do not treat this brief as approved. It is a draft for Ark's and Zcode's review; launch requires
   Mike's explicit word afterward, as with every other brief in this repository.

---

## Reviewer note — CC, 2026-09-17 UTC (2026-09-18 local), on the draft above

Verified at source, then two findings. The draft was written by a CC subagent; this note is the
author's own check of it before it goes to Ark and Zcode.

**Verified.** The ablation deltas are exact at
`results/night3/diagnostics/ablation/ablation_profiles.csv`: Mi4 in seed 3 is
`4827.536294460297` (line 25), CT1(Lo1) in seed 4 is `10460.885339736938` (line 85), and Mi11 is
`2.384185791015625e-06` in seed 3 (line 28) and `4.291534423828125e-05` in seed 4 (line 93). The
record's asymmetry holds too and belongs in the reading: Mi4 in **seed 4** is only `372.67`
(line 90) and CT1(Lo1) in **seed 3** only `7.19` (line 20) — each type's large delta appears in
exactly one individual, which is the "the class repeats, the type does not" observation the
night-3 record already carries.

**1. Void condition 6 is discharged for both targets — input removal is well defined.** The draft
left unchecked whether these types have incoming edge groups at all, which would have made the
whole intervention vacuous. They do. From the recorded per-type parameter inventory
(`param_share_by_type.json`, the artefact behind
`docs/preregistration-cheap-vs-expensive.md:37`, read 2026-09-17): **Mi4 — 17 incoming edge
groups** (k=19, 2 node parameters, rank 6 of 65); **CT1(Lo1) — 7 incoming groups** (k=9, rank 40).
Both are well above zero, so intervention (b) has something to zero in each case.

**2. The null cell is degenerate, and its zero was predictable from the connectome rather than
from its function.** The same inventory gives **Mi11 — 1 incoming group, and 0 outgoing** (k=3,
rank 61 of 65). A type that sends nothing to anyone must have a near-zero ablation delta whatever
its tuning is: its `2.4e-06` is topology, not evidence that the instrument is insensitive to
unimportant types. And as an input-removal cell it is not intervention-matched either — zeroing
**1** group against the targets' **17** and **7** is a different size of intervention, so a
"returns" result from Mi11 cannot fail and therefore validates nothing. This is the same class as
a control that cannot blush.

**What the null needs instead:** a type matched on incoming-group count (roughly 7–17 groups) whose
clamp delta is nevertheless small, so that "returns" is a result the cell could have failed to
produce. The inventory has the counts for all 65 types, so the choice costs a lookup and no
measurement. Until that swap is made, the null cell should be described as testing **the code
path only** — that the save/zero/evaluate/restore sequence runs and restores bit-identically — and
not as evidence about sensitivity. The choice of the replacement type is the reading's design and
belongs to the reviewers, not to this note; nothing in §3 is changed here.

**Still open, and named rather than fixed:** the 1e-3 tolerance borrowed from the gray brief's P0
ceiling has no measured floor of its own for an input-removal intervention (draft's own boundary),
and none of the §3 numbers has been recomputed from a second source, which checklist rule 15 asks
for before a verdict is drawn — both remain the executor's obligation, as the draft states.
