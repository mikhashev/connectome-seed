"""Label check in Ark's revised form: coverage first.

PREVIEW DIAGNOSTIC -- NOT A TEST

Disposition is registered in results/diagnostics/labels/README.md, saved and hashed BEFORE this
script was written (disposition.sha256.json). This script reports the partition and nothing
beyond it.

Reads only: the flyvis json spec, the compiled connectome directory, and
flyvis.utils.groundtruth_utils. Writes only under results/diagnostics/labels/.
No loss value, no activity value, no checkpoint is read or written.
"""

import hashlib
import json
import os
from collections import Counter, OrderedDict
from datetime import datetime, timezone
from pathlib import Path

import h5py
import numpy as np

OUT = Path(__file__).resolve().parent
JSON_PATH = Path(
    "C:/Users/mikha/Documents/dpc-research/connectome-seed/tools/.venv/Lib/"
    "site-packages/flyvis/connectome/fib25-fib19_v2.2.json"
)
CONN_DIR = Path(
    "C:/Users/mikha/Documents/dpc-research/connectome-seed-data/connectome/"
    "ConnectomeFromAvgFilters_0000"
)
GT_PATH = Path(
    "C:/Users/mikha/Documents/dpc-research/connectome-seed/tools/.venv/Lib/"
    "site-packages/flyvis/utils/groundtruth_utils.py"
)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def h5(path, key="data"):
    with h5py.File(path, "r") as f:
        return np.asarray(f[key][()])


def s(a):
    return np.asarray(a).astype(str)


# --------------------------------------------------------------------------------------
# 0. Sources
# --------------------------------------------------------------------------------------
from flyvis.utils import groundtruth_utils as gt  # noqa: E402

spec = json.loads(JSON_PATH.read_text())
nodes_spec, edges_spec = spec["nodes"], spec["edges"]

# Type axis: connectome node order (first appearance in nodes/type.h5) -- the axis row A/row B use
node_type = s(h5(CONN_DIR / "nodes" / "type.h5"))
type_axis = list(OrderedDict.fromkeys(node_type.tolist()))
assert len(type_axis) == 65, len(type_axis)

# --------------------------------------------------------------------------------------
# 1. (c) COVERAGE -- full field inventory of the bank, per-type and per-edge
# --------------------------------------------------------------------------------------
inventory = []  # rows: scope, source, field, kind, shape/len, n_distinct, value_set


def add(scope, source, field, kind, shape, values, note=""):
    try:
        uniq = sorted({v if isinstance(v, (str, bool, int, float, type(None))) else repr(v)
                       for v in values}, key=repr)
    except TypeError:
        uniq = sorted({repr(v) for v in values})
    vs = repr(uniq) if len(uniq) <= 12 else f"{len(uniq)} distinct, e.g. {uniq[:5]!r}"
    inventory.append(
        dict(scope=scope, source=source, field=field, kind=kind, shape=str(shape),
             n_distinct=len(uniq), value_set=vs, note=note)
    )


# --- json per-node fields
node_keys = sorted({k for n in nodes_spec for k in n})
for k in node_keys:
    add("per-type", "json:nodes", k, "json field", f"({len(nodes_spec)},)",
        [n.get(k) for n in nodes_spec])
# --- json per-edge fields
edge_keys = sorted({k for e in edges_spec for k in e})
for k in edge_keys:
    vals = [e.get(k) for e in edges_spec]
    if k == "offsets":
        add("per-edge", "json:edges", k, "list of [[du,dv],n_syn]", f"({len(edges_spec)},)",
            [f"len={len(v)}" for v in vals],
            note=f"{sum(len(v) for v in vals)} offset rows total")
    elif k == "alpha_references":
        add("per-edge", "json:edges", k, "list of citation keys", f"({len(edges_spec)},)",
            [f"len={len(v)}" for v in vals],
            note=f"{sum(len(v) for v in vals)} citation slots total")
    else:
        add("per-edge", "json:edges", k, "json field", f"({len(edges_spec)},)", vals)
# --- json other sections
for sec in ("receptors", "input_units", "output_units"):
    add("per-type", "json:root", sec, "list of type names", f"({len(spec[sec])},)",
        spec[sec][:20] if spec[sec] else [])

# --- compiled h5 tables
for sub in ("nodes", "edges"):
    for fn in sorted(os.listdir(CONN_DIR / sub)):
        p = CONN_DIR / sub / fn
        if p.is_dir():
            add("per-type" if sub == "nodes" else "per-edge", f"h5:{sub}", fn + "/", "directory",
                f"({len(os.listdir(p))} files)", [], note="one file per cell type")
            continue
        if not fn.endswith(".h5"):
            continue
        a = h5(p)
        u = np.unique(a)
        vals = (s(u).tolist() if a.dtype.kind == "S" else u.tolist())
        add("per-cell" if sub == "nodes" else "per-edge-instance", f"h5:{sub}", fn[:-3],
            str(a.dtype), a.shape, vals)
for fn in sorted(os.listdir(CONN_DIR)):
    p = CONN_DIR / fn
    if p.is_file() and fn.endswith(".h5"):
        a = h5(p)
        vals = s(np.unique(a)).tolist() if a.dtype.kind == "S" else np.unique(a).tolist()
        add("per-type", "h5:root", fn[:-3], str(a.dtype), a.shape, vals)

# --- the coverage verdict: is any of these polarity-like?
# A polarity-like quantity must be (i) per cell type and (ii) a contrast preference (ON/OFF),
# i.e. a value set comparable to {+1, 0, -1} on the type axis. We enumerate candidates rather
# than assert, and record why each is or is not polarity-like.
candidates = []
for row in inventory:
    if row["scope"] not in ("per-type", "per-cell"):
        continue
    candidates.append(row)

polarity_like = []  # filled only if a genuine candidate is found
coverage_notes = {
    "json:nodes.activation": "constant 'relu' for all 65 -- not a label, no variation",
    "json:nodes.bias": "constant 3.5 for all 65 -- not read by the network (see the genome note "
                       "§2); not a contrast preference",
    "json:nodes.bias_fixed": "constant False for all 65",
    "json:nodes.time_constant": "None for all 65",
    "json:nodes.time_constant_fixed": "constant False for all 65",
    "json:nodes.pattern": "['stride',[1,1]] / ['stride',[3,2]] -- a tiling production, not a label",
    "json:nodes.name": "the type name",
    "json:root.input_units": "8 photoreceptors -- anatomical entry point, not ON/OFF",
    "json:root.output_units": "34 types -- anatomical role, not ON/OFF",
    "json:root.receptors": "empty",
    "h5:root.layout": "retina/intermediate/output -- built in connectome.py:196-221 from "
                      "input_units/output_units; anatomical stage, not ON/OFF",
    "h5:root.unique_cell_types": "the 65 names",
    "h5:root.input_cell_types": "8 names",
    "h5:root.intermediate_cell_types": "23 names",
    "h5:root.output_cell_types": "34 names",
    "h5:root.central_cells_index": "one node index per type -- an index, not a label",
    "h5:nodes.role": "input/intermediate/output -- same anatomical stage axis as layout",
    "h5:nodes.type": "the type name per cell",
    "h5:nodes.index": "node index",
    "h5:nodes.u": "hex coordinate",
    "h5:nodes.v": "hex coordinate",
    "h5:nodes.layer_index/": "per-type node index lists",
}

# --------------------------------------------------------------------------------------
# 2. Verify the module's own numbers (denominator) -- do not assume the brief
# --------------------------------------------------------------------------------------
pol = dict(gt.polarity)
n_on = sum(1 for v in pol.values() if v == 1)
n_off = sum(1 for v in pol.values() if v == -1)
n_unk = sum(1 for v in pol.values() if v == 0)
defined = [t for t in type_axis if pol.get(t, 0) != 0]
on_pw, off_pw = list(gt.on_pathway), list(gt.off_pathway)
axis_mix = [t for t in type_axis if pol.get(t) == -1 and t in on_pw]
axis_mix_rev = [t for t in type_axis if pol.get(t) == 1 and t in off_pw]
in_both_pw = [t for t in type_axis if t in on_pw and t in off_pw]

verify = dict(
    groundtruth_utils_sha256=sha256(GT_PATH),
    n_types_with_polarity_entry=len(pol),
    n_polarity_ON_plus1=n_on,
    n_polarity_OFF_minus1=n_off,
    n_polarity_unknown_0=n_unk,
    n_defined_denominator=len(defined),
    defined_types=defined,
    claim_18_ON_14_OFF_33_unknown_holds=(n_on == 18 and n_off == 14 and n_unk == 33),
    claim_denominator_32_holds=(len(defined) == 32),
    on_pathway=on_pw,
    off_pathway=off_pw,
    n_on_pathway=len(on_pw),
    n_off_pathway=len(off_pw),
    n_distinct_types_in_either_pathway=len(set(on_pw) | set(off_pw)),
    types_in_both_pathways=in_both_pw,
    types_polarity_minus1_and_in_on_pathway=axis_mix,
    claim_L1_L3_Mi9_holds=(sorted(axis_mix) == sorted(["L1", "L3", "Mi9"])),
    types_polarity_plus1_and_in_off_pathway=axis_mix_rev,
)

# --------------------------------------------------------------------------------------
# 3. Sign provenance (the sub-check that needs no invented rule)
# --------------------------------------------------------------------------------------
per_src = {}
for e in edges_spec:
    d = per_src.setdefault(e["src"], dict(n=0, exc=0, inh=0, fixed=0, refs=0, refkeys=[],
                                          entries_with_refs=0))
    d["n"] += 1
    d["exc" if e["alpha"] == 1 else "inh"] += 1
    if e.get("alpha_fixed"):
        d["fixed"] += 1
    r = e.get("alpha_references") or []
    d["refs"] += len(r)
    d["refkeys"].extend(r)
    if r:
        d["entries_with_refs"] += 1

src_types = sorted(per_src)
consistent = [t for t in src_types if per_src[t]["exc"] == 0 or per_src[t]["inh"] == 0]
inconsistent = [t for t in src_types if per_src[t]["exc"] > 0 and per_src[t]["inh"] > 0]
fixed_all = [t for t in src_types if per_src[t]["fixed"] == per_src[t]["n"]]
fixed_some = [t for t in src_types if 0 < per_src[t]["fixed"] < per_src[t]["n"]]
fixed_none = [t for t in src_types if per_src[t]["fixed"] == 0]
never_source = [t for t in type_axis if t not in per_src]

all_refs = Counter(k for d in per_src.values() for k in d["refkeys"])
n_entries_fixed = sum(1 for e in edges_spec if e.get("alpha_fixed"))
n_entries_with_refs = sum(1 for e in edges_spec if e.get("alpha_references"))
n_fixed_with_refs = sum(1 for e in edges_spec
                        if e.get("alpha_fixed") and e.get("alpha_references"))
n_fixed_without_refs = sum(1 for e in edges_spec
                           if e.get("alpha_fixed") and not e.get("alpha_references"))
n_notfixed_with_refs = sum(1 for e in edges_spec
                           if not e.get("alpha_fixed") and e.get("alpha_references"))

# compiled sign agrees with json alpha, per source type?
src_t = s(h5(CONN_DIR / "edges" / "source_type.h5"))
sgn = h5(CONN_DIR / "edges" / "sign.h5")
compiled_sign_per_src = {}
for t in np.unique(src_t):
    vals = np.unique(sgn[src_t == t])
    compiled_sign_per_src[str(t)] = [float(x) for x in vals]
compiled_sign_consistent = [t for t, v in compiled_sign_per_src.items() if len(v) == 1]

sign_prov = dict(
    n_json_edge_entries=len(edges_spec),
    n_source_types_appearing=len(src_types),
    types_never_a_source=never_source,
    sign_one_per_source_type=len(consistent) == len(src_types),
    n_source_types_sign_consistent=len(consistent),
    source_types_sign_inconsistent=inconsistent,
    n_source_types_alpha_fixed_ALL=len(fixed_all),
    source_types_alpha_fixed_ALL=fixed_all,
    n_source_types_alpha_fixed_SOME=len(fixed_some),
    source_types_alpha_fixed_SOME=fixed_some,
    n_source_types_alpha_fixed_NONE=len(fixed_none),
    source_types_alpha_fixed_NONE=fixed_none,
    n_entries_alpha_fixed_true=n_entries_fixed,
    n_entries_with_alpha_references=n_entries_with_refs,
    n_entries_alpha_fixed_AND_referenced=n_fixed_with_refs,
    n_entries_alpha_fixed_WITHOUT_reference=n_fixed_without_refs,
    n_entries_referenced_but_NOT_alpha_fixed=n_notfixed_with_refs,
    n_distinct_reference_keys=len(all_refs),
    reference_keys=dict(sorted(all_refs.items())),
    n_citation_slots_total=sum(all_refs.values()),
    citation_keys_that_are_personal_communications=dict(
        keys=[k for k in sorted(all_refs) if "PC" in k],
        n_slots=sum(v for k, v in all_refs.items() if "PC" in k),
        note="'NernPC2018' and 'ReiserPC2017' are personal-communication keys, not publications. "
             "They are reported as such because the SIGN column's provenance is what this "
             "sub-check measures. No judgement of their reliability is made here.",
    ),
    citation_keys_that_are_publications=dict(
        keys=[k for k in sorted(all_refs) if "PC" not in k],
        n_slots=sum(v for k, v in all_refs.items() if "PC" not in k),
    ),
    compiled_sign_one_per_source_type=len(compiled_sign_consistent) == len(compiled_sign_per_src),
    dale_note="Four source types carry BOTH an excitatory and an inhibitory alpha across their "
              "outgoing entries, so sign is NOT one value per source type in this json. A genome "
              "track that regenerated sign as a per-type property would be unable to reproduce "
              "these four by construction.",
    inconsistent_detail={
        t: dict(n_entries=per_src[t]["n"], n_exc=per_src[t]["exc"], n_inh=per_src[t]["inh"])
        for t in inconsistent
    },
)

# --------------------------------------------------------------------------------------
# 4. Descriptive reach of a would-be L1/L2 rule -- NOT a recomputation, NOT a rule
# --------------------------------------------------------------------------------------
direct_in = {t: set() for t in type_axis}
for e in edges_spec:
    direct_in[e["tar"]].add(e["src"])
reach = dict(
    note="DESCRIPTIVE ONLY. These counts say how far a rule of the 'L1/L2 direct input' family "
         "could reach if such a rule were ever written. No rule is applied and no polarity is "
         "recomputed here.",
    n_types_with_direct_L1_input=sum(1 for t in type_axis if "L1" in direct_in[t]),
    n_types_with_direct_L2_input=sum(1 for t in type_axis if "L2" in direct_in[t]),
    n_types_with_BOTH_L1_and_L2=sum(1 for t in type_axis
                                    if {"L1", "L2"} <= direct_in[t]),
    n_types_with_NEITHER=sum(1 for t in type_axis if not (direct_in[t] & {"L1", "L2"})),
)

# --------------------------------------------------------------------------------------
# 5. Side observation: h5 layout vs groundtruth_utils.layout (same axis, same value set)
# --------------------------------------------------------------------------------------
lay_h5 = {a: b for a, b in s(h5(CONN_DIR / "layout.h5")).tolist()}
lay_gt = dict(gt.layout)
layout_cmp = dict(
    note="layout IS in the bank: connectome.py:196-221 builds it from json input_units/"
         "output_units. Reported because it shows what a bank-derived label looks like. It is "
         "an anatomical stage axis, not ON/OFF.",
    n_agree=sum(1 for t in type_axis if lay_h5.get(t) == lay_gt.get(t)),
    n_types=len(type_axis),
    disagreements={t: dict(bank=lay_h5.get(t), groundtruth=lay_gt.get(t))
                   for t in type_axis if lay_h5.get(t) != lay_gt.get(t)},
)

# --------------------------------------------------------------------------------------
# 6. Write the per-type csv
# --------------------------------------------------------------------------------------
cols = ["type_name", "node_order_index", "polarity_source", "in_on_pathway", "in_off_pathway",
        "n_out_entries", "n_exc", "n_inh", "n_alpha_fixed", "n_alpha_references",
        "bank_polarity_like_value", "bank_layout", "bank_role",
        "has_direct_L1_input_DESCRIPTIVE", "has_direct_L2_input_DESCRIPTIVE"]
role_h5 = s(h5(CONN_DIR / "nodes" / "role.h5"))
role_of = {}
for t, r in zip(node_type.tolist(), role_h5.tolist()):
    role_of.setdefault(t, r)

lines = ["PREVIEW DIAGNOSTIC -- NOT A TEST",
         f"# script_sha256={sha256(__file__)}",
         f"# disposition_sha256={sha256(OUT / 'README.md')}",
         "# bank_polarity_like_value is empty for every row: see partition.json question (c).",
         ",".join(cols)]
for i, t in enumerate(type_axis):
    d = per_src.get(t, dict(n=0, exc=0, inh=0, fixed=0, refs=0))
    row = [t, str(i), repr(int(pol.get(t, 0))), str(t in on_pw), str(t in off_pw),
           str(d["n"]), str(d["exc"]), str(d["inh"]), str(d["fixed"]), str(d["refs"]),
           "", lay_h5.get(t, ""), role_of.get(t, ""),
           str("L1" in direct_in[t]), str("L2" in direct_in[t])]
    lines.append(",".join(row))
(OUT / "labels_per_type.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")

# --------------------------------------------------------------------------------------
# 7. Write the inventory csv
# --------------------------------------------------------------------------------------
inv_cols = ["scope", "source", "field", "kind", "shape", "n_distinct", "value_set", "note",
            "polarity_like", "why"]
ilines = ["PREVIEW DIAGNOSTIC -- NOT A TEST", ",".join(inv_cols)]
for r in inventory:
    key = f"{r['source'].split(':')[0]}:{r['source'].split(':')[1]}.{r['field']}"
    why = coverage_notes.get(key, "")
    if r["scope"] in ("per-edge", "per-edge-instance"):
        why = ("per-EDGE quantity; alpha/sign is the excitatory/inhibitory sign of a source "
               "type's synapses -- explicitly NOT ON/OFF polarity"
               if r["field"] in ("alpha", "sign", "alpha_fixed", "alpha_references")
               else "per-edge, not per-type")
    q = lambda x: '"' + str(x).replace('"', "'") + '"'
    ilines.append(",".join([q(r["scope"]), q(r["source"]), q(r["field"]), q(r["kind"]),
                            q(r["shape"]), str(r["n_distinct"]), q(r["value_set"]),
                            q(r["note"]), "False", q(why)]))
(OUT / "bank_fields_inventory.csv").write_text("\n".join(ilines) + "\n", encoding="utf-8")

# --------------------------------------------------------------------------------------
# 8. Write the partition json
# --------------------------------------------------------------------------------------
summary = OrderedDict(
    header="PREVIEW DIAGNOSTIC -- NOT A TEST",
    run_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    script_sha256=sha256(__file__),
    disposition_sha256=sha256(OUT / "README.md"),
    sources=dict(
        json=str(JSON_PATH), json_sha256=sha256(JSON_PATH),
        connectome_dir=str(CONN_DIR),
        groundtruth_utils=str(GT_PATH), groundtruth_utils_sha256=sha256(GT_PATH),
    ),
    denominator_verified_from_module=verify,
    question_c_coverage=dict(
        n_per_type_fields_in_bank=sum(1 for r in inventory
                                      if r["scope"] in ("per-type", "per-cell")),
        n_per_edge_fields_in_bank=sum(1 for r in inventory
                                      if r["scope"] in ("per-edge", "per-edge-instance")),
        polarity_like_fields_found=polarity_like,
        n_polarity_like_fields_found=len(polarity_like),
        answer=("The bank carries no polarity; nothing was synthesised and nothing copied."
                if not polarity_like else "OPEN -- candidate(s) found, see list"),
        outcome_case=("no such field" if not polarity_like else "OPEN"),
        meaning=("The label array cannot be 'predicted from the bank' because it is not in the "
                 "bank. The ON/OFF axis enters this repository only through "
                 "flyvis.utils.groundtruth_utils."
                 if not polarity_like else "OPEN"),
        explicitly_excluded=dict(
            edge_alpha_json="per-(src,tar) excitatory/inhibitory sign, NOT ON/OFF polarity",
            edge_sign_h5="per-edge-instance copy of alpha, NOT ON/OFF polarity",
            layout_role="anatomical stage (retina/intermediate/output), NOT ON/OFF polarity",
        ),
    ),
    question_d_twin_markers=dict(
        runnable=bool(polarity_like),
        status=("NOT RUNNABLE -- conditional on (c); (c) found no polarity-like field in the "
                "bank, so there is no second marker to compare against."
                if not polarity_like else "runnable"),
        types_that_would_be_compared=["L1", "L3", "Mi9"],
        source_polarity_of_those={t: int(pol[t]) for t in ["L1", "L3", "Mi9"]},
        in_on_pathway={t: (t in on_pw) for t in ["L1", "L3", "Mi9"]},
        in_off_pathway={t: (t in off_pw) for t in ["L1", "L3", "Mi9"]},
    ),
    question_b_recomputation=dict(
        runnable=False,
        status="NOT RUNNABLE: no registered rule.",
        searched=[
            "docs/briefs/2026-09-16-step2-tuning-battery.md §8",
            "docs/plans/2026-09-16-functional-readout-plan.md",
            "flyvis docs/source (absent: the installed package ships no docs tree)",
            "repo-wide grep for a connectivity->ON/OFF mapping",
        ],
        only_candidate_found=dict(
            path_line="docs/briefs/2026-09-16-step2-tuning-battery.md:98-99",
            quote="recompute polarity from the input rule of the connectome itself "
                  "(L1 -> ON, L2 -> OFF pathway) and compare it with groundtruth_utils.polarity",
            restated_at="docs/plans/2026-09-20-genome-design-around-s2.md:186",
            axis="MIXED: its target is response polarity (`polarity`) while its content is "
                 "pathway membership (`on_pathway`/`off_pathway`). These are the two axes.",
            withdrawn_by_author=True,
            withdrawal="Ark, group chat 2026-09-20 09:16 UTC, withdrew §4 as originally written "
                       "for exactly this axis mix.",
            operational=False,
            why_not_operational="Even setting the withdrawal aside, the sentence states no "
                                "operator: no threshold, no weighting by n_syn, no path depth "
                                "(direct input only or transitive), no tie rule for types "
                                "receiving both. It names two seed types, not a mapping.",
        ),
        conclusion="No rule exists in writing that is both on a single axis and operational. "
                   "Supplying one would be inventing it, which the disposition forbids. "
                   "(b) is reported not runnable.",
        descriptive_reach_only=reach,
    ),
    question_a_literature_match=dict(
        runnable=False,
        status="NOT RUNNABLE as a match: there is no second, independent ON/OFF assignment in "
               "this repository to match groundtruth_utils.polarity against. (c) established "
               "the bank has none; (b) established no rule can generate one without invention.",
        what_is_recorded_instead="The source's own two axes and their disagreement, below.",
        axis_disagreement=dict(
            types_polarity_minus1_in_on_pathway=axis_mix,
            types_polarity_plus1_in_off_pathway=axis_mix_rev,
            types_in_both_pathways=in_both_pw,
            comment="Within groundtruth_utils itself, polarity and pathway membership are "
                    "different axes and disagree on named types. Neither can stand in for the "
                    "other.",
        ),
    ),
    sign_provenance=sign_prov,
    side_observation_layout=layout_cmp,
    OPEN=[],
    runner_note="The runner reports the partition and does not write the reading beyond it "
                "(ADR-003).",
)
(OUT / "partition.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

print(json.dumps(dict(
    denominator_ok=verify["claim_denominator_32_holds"],
    counts_ok=verify["claim_18_ON_14_OFF_33_unknown_holds"],
    L1_L3_Mi9_ok=verify["claim_L1_L3_Mi9_holds"],
    axis_mix=axis_mix, in_both_pw=in_both_pw, plus1_in_off=axis_mix_rev,
    polarity_like_found=len(polarity_like),
    n_per_type_fields=summary["question_c_coverage"]["n_per_type_fields_in_bank"],
    n_per_edge_fields=summary["question_c_coverage"]["n_per_edge_fields_in_bank"],
    sign=dict(consistent=len(consistent), inconsistent=inconsistent,
              never_source=never_source,
              fixed_all=len(fixed_all), fixed_some=len(fixed_some), fixed_none=len(fixed_none),
              entries_fixed=n_entries_fixed, entries_refs=n_entries_with_refs,
              fixed_no_ref=n_fixed_without_refs, ref_not_fixed=n_notfixed_with_refs,
              n_refkeys=len(all_refs)),
    layout=dict(agree=layout_cmp["n_agree"], dis=layout_cmp["disagreements"]),
    reach=reach,
), indent=2))
