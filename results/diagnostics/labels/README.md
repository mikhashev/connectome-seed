# Label check in Ark's revised form — coverage first

**Runner:** CC, 2026-09-20. **Owner's word:** Mike, 2026-09-20 09:27 UTC —
«чек меток в форме Ark, покрытие первым — да».
**Form:** Ark's REVISED four questions (group chat 2026-09-20 09:16 UTC). Ark's
`docs/plans/2026-09-20-genome-design-around-s2.md` §4 **as originally written is WITHDRAWN by its
author**: its input rule "L1 → ON, L2 → OFF" mixed two axes — in flyvis
`polarity["L1"] == -1` while `"L1"` is listed in `on_pathway`.

**No measured training results are involved.** No loss, no activity, no checkpoint value is read
or written by this check. Every number below is a structural integer or a string from a compiled
table, a json spec, or a source module.

---

## Disposition, written before the run — 2026-09-20

This section is written, saved and hashed **before the script runs**. It is not movable
afterwards. The runner reports the partition; **the runner does not write the reading beyond the
partition** (ADR-003, and Ark's §4 third clause).

### The four questions, in the order Ark fixed

**(c) COVERAGE — first, and free.** Does the bank — the json
`flyvis/connectome/fib25-fib19_v2.2.json`, the compiled tables under
`connectome-seed-data/connectome/ConnectomeFromAvgFilters_0000/`, or anything else in the flyvis
package that feeds the network — carry **any per-cell-type quantity that plays the role of ON/OFF
polarity**? The step is: first establish what exists — list every per-type and per-edge field
(names, shapes, value sets) — and only then ask whether any of them is polarity-like. Ark states
explicitly that he does not know whether the bank has such a field.

**Caution registered in advance:** the bank's edge `sign` (compiled) / `alpha` (json) is the
**excitatory/inhibitory sign of a source type's synapses**. That is **not** ON/OFF polarity, and
the two are not to be equated. A ±1 per-edge quantity is not a per-type contrast preference.

**(d) TWIN MARKERS.** Only meaningful if (c) finds a polarity-like field. If it does, compare it
with `groundtruth_utils.polarity` on the three types that carry polarity −1 while sitting in
`on_pathway`: **L1, L3, Mi9**.

**(a) LITERATURE MATCH** and **(b) RECOMPUTATION FROM CONNECTIVITY.** (b) needs a **rule** mapping
connectivity to ON/OFF. **No rule is to be invented by the runner.** The runner searches for one
already in writing — `docs/briefs/2026-09-16-step2-tuning-battery.md` §8,
`docs/plans/2026-09-16-functional-readout-plan.md`, flyvis `docs/source` — and:

- if a written rule exists: quote it with `path:line`, state whether it is about **pathway
  membership** or **response polarity** (the two axes Ark's withdrawn §4 mixed), and apply it
  **only on the axis it is about** — a pathway rule is compared with `on_pathway`/`off_pathway`,
  **not** with `polarity`;
- if no written rule exists: report **"(b) not runnable: no registered rule."** That is itself a
  finding, not a failure of the run.

### The denominator, fixed before running

Verified from `tools/.venv/Lib/site-packages/flyvis/utils/groundtruth_utils.py:15-82`, the module
whose own comment at `:15` reads `# 1 is ON, 0 is unknown, -1 is OFF`:

- **65** types have a `polarity` entry; **33** of them are `0` = *unknown*;
- **18** are `+1` (ON); **14** are `−1` (OFF);
- **the check operates on the 32 defined types, not on 65.**

**The 32 defined types (the denominator), listed here before the run:**

*18 ON (+1):* `R1`, `R2`, `R3`, `R4`, `R5`, `R6`, `R7`, `R8`, `L5`, `C3`, `CT1(M10)`, `Mi1`,
`Mi4`, `Tm3`, `T4a`, `T4b`, `T4c`, `T4d`.

*14 OFF (−1):* `L1`, `L2`, `L3`, `L4`, `CT1(Lo1)`, `Mi9`, `Tm1`, `Tm2`, `Tm4`, `Tm9`, `T5a`,
`T5b`, `T5c`, `T5d`.

*The 33 unknown (0), outside the denominator:* `Lawf1`, `Lawf2`, `Am`, `C2`, `Mi2`, `Mi3`, `Mi10`,
`Mi11`, `Mi12`, `Mi13`, `Mi14`, `Mi15`, `T1`, `T2`, `T2a`, `T3`, `Tm5Y`, `Tm5a`, `Tm5b`, `Tm5c`,
`Tm16`, `Tm20`, `Tm28`, `Tm30`, `TmY3`, `TmY4`, `TmY5a`, `TmY9`, `TmY10`, `TmY13`, `TmY14`,
`TmY15`, `TmY18`.

The three axis-mixing types to be verified against the module, not assumed: **L1, L3, Mi9** carry
`polarity == −1` and appear in `on_pathway`. (`L3` additionally appears in **both** `on_pathway`
and `off_pathway`, which is why pathway membership, at 12 + 12 entries over 23 distinct types,
cannot be read as a two-valued label.)

### What each outcome would mean

Taken from Ark's §4 dispositions where still valid, and from his revised message:

**For (c), the coverage question:**

| outcome | meaning, registered in advance |
|---|---|
| the bank carries a polarity-like per-type field, **definite on all 65** | **synthesis**: the bank states a contrast label for every type, including the 33 the literature leaves unknown. The label array would then be predictable from the bank, and using it to judge a model of the bank is circular (Ark §4, "Match"). |
| the bank carries a polarity-like per-type field, but **leaves unknown what the source leaves unknown** | **copying**: the bank's field is a transcription of the literature field, not an independent quantity. It adds no information and cannot serve as an external yardstick either. |
| **no such field exists in the bank** | *"The bank carries no polarity; nothing was synthesised and nothing copied."* The label array **cannot be "predicted from the bank" because it is not in the bank.** The ON/OFF axis enters the repository only through `groundtruth_utils`, and the design's §4 route — recomputation as a provenance test — has no object to operate on. |

**For (d):** meaningful only under the first two outcomes. Under the third it is **not runnable**,
and is reported as such rather than answered.

**For (a) and (b):** (b) is runnable only if a written rule is found. A written rule that is
about pathway membership is applied to `on_pathway`/`off_pathway` only; it is **not** evidence
about `polarity`, and a match or a mismatch on the pathway axis is reported on that axis alone.

**Anything that does not fit the cases above is reported as OPEN**, and is not assigned to the
nearest case. An empty partition is a failure of the instrument, not a verdict of independence
(Ark §7 falsifier).

### The sub-check that needs no invented rule — provenance of the SIGN column

Run regardless of (c)'s outcome, because **sign is what a genome track would actually have to
regenerate**, and the json's sign carries its own provenance fields:

1. Is the excitatory/inhibitory `alpha` of each **source** type consistent across all of that
   type's outgoing edge entries — one sign per source type, or not?
2. How many source types have `alpha_fixed: true` on **all** / **some** / **none** of their
   entries?
3. Do the `alpha_references` citations exist per entry — counted, listed by reference key.

This is descriptive provenance of a bank column. It is **not** a polarity recomputation and is
not to be read as one.

### What the runner does not do

- does not invent a connectivity → ON/OFF rule;
- does not equate edge `sign` / `alpha` with ON/OFF polarity;
- does not move a type into or out of the denominator after seeing numbers;
- does not write the reading beyond the partition;
- writes only under `results/diagnostics/labels/`;
- carries no loss value and no activity value into any output.

---

## Outputs this check writes

- `labels_per_type.csv` — 65 rows, one per cell type, **in connectome node order**
  (`nodes/type.h5`, first-appearance order, the same axis row A and row B use). Columns:
  `polarity` (source), `in_on_pathway`, `in_off_pathway`, source-sign summary
  (`n_out_entries`, `n_exc`, `n_inh`, `n_alpha_fixed`), and any bank polarity-like value found.
- `partition.json` — the partition, the denominator, and the field inventory summary.
- `bank_fields_inventory.csv` — every per-type and per-edge field of the json and the compiled
  tables, with shape and value set: the evidence for (c).
- `check_labels.py` — the script.

`disposition.sha256.json` records the sha256 and UTC time of **this file**, taken before the
script ran.
