"""Extract the generation-zero bank: the object a genome grammar must regenerate.

Structural extraction only. Reads the connectome json shipped with flyvis and the compiled
connectome tables (FLYVIS_ROOT_DIR/connectome/ConnectomeFromAvgFilters_0000); reads no
checkpoint, no loss, no activity. Writes only next to this file.

Outputs (all UTF-8, written with an explicit encoding and "\n" line ends):
    types.csv        65 rows, connectome node order
    type_pairs.csv   605 rows, one per json edge entry, json order
    offsets.csv      2,355 compiled (src, tar, du, dv) rows + the 23 json rows that were dropped
    birth_ids.csv    the generation-zero registry; ids derived from names (see REGISTRY.md)
    bank.meta.json   provenance: package, version, relative source file, hashes, checks

Every csv begins with one '#' comment line naming the source (package + version + file, never
an absolute path), the json sha256 and this script's sha256; the full record is bank.meta.json.

Deterministic: no randomness; every ordering is stated; floats are written with repr().
birth_ids.csv is never silently changed: if it already exists and the regenerated registry
differs from it byte for byte, the script stops instead of overwriting it. The one exception is
the audited, flagged migration from the pre-v1 counter ids (--migrate-from-counter-ids).

Usage (from the repository root):
    tools/.venv/Scripts/python.exe results/genome/bank/extract_bank.py
"""

import hashlib
import json
import math
import os
import re
import sys
from collections import OrderedDict
from pathlib import Path

import h5py
import numpy as np
import pandas as pd

import flyvis
from flyvis.connectome import connectome as fv_conn

OUT = Path(__file__).resolve().parent
PKG_ROOT = Path(flyvis.__file__).resolve().parent
JSON_REL = "connectome/fib25-fib19_v2.2.json"
JSON_PATH = PKG_ROOT / JSON_REL
ROOT_DIR = Path(os.environ.get(
    "FLYVIS_ROOT_DIR", "C:/Users/mikha/Documents/dpc-research/connectome-seed-data"))
CONN_REL = "connectome/ConnectomeFromAvgFilters_0000"
CONN_DIR = ROOT_DIR / CONN_REL
EXTENT_COMPILED = 15
EXTENT_DECODE_CHECK = 5
N_SYN_FILL = 1


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(p):
    return sha256_bytes(Path(p).read_bytes())


def h5(path, key="data"):
    with h5py.File(path, "r") as f:
        return np.asarray(f[key][()])


def s(a):
    return np.asarray(a).astype(str)


def canon(obj):
    """Canonical JSON text of an element, for content hashes."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def csv_field(x):
    x = "" if x is None else str(x)
    if any(c in x for c in ',"\n'):
        return '"' + x.replace('"', '""') + '"'
    return x


def write_csv(path, header_comment, cols, rows):
    lines = ["# " + header_comment, ",".join(cols)]
    lines += [",".join(csv_field(r[c]) for c in cols) for r in rows]
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


# ------------------------------------------------------------------------------------------
# 0. Sources
# ------------------------------------------------------------------------------------------
json_bytes = JSON_PATH.read_bytes()
spec = json.loads(json_bytes.decode("utf-8"))
nodes_spec, edges_spec = spec["nodes"], spec["edges"]
JSON_SHA = sha256_bytes(json_bytes)
SCRIPT_SHA = sha256_file(__file__)
SOURCE = f"flyvis {flyvis.__version__} : {JSON_REL}"
HEADER = (f"source={SOURCE}; json_sha256={JSON_SHA}; "
          f"compiled=FLYVIS_ROOT_DIR/{CONN_REL} (extent {EXTENT_COMPILED}, n_syn_fill "
          f"{N_SYN_FILL}); script=results/genome/bank/extract_bank.py sha256={SCRIPT_SHA}; "
          f"see bank.meta.json")

assert len(nodes_spec) == 65 and len(edges_spec) == 605
node_keys = list(nodes_spec[0].keys())
edge_keys = list(edges_spec[0].keys())
assert all(list(n.keys()) == node_keys for n in nodes_spec)
assert all(list(e.keys()) == edge_keys for e in edges_spec)

# Type axis: connectome node order (first appearance in nodes/type.h5), the axis of row A/B
node_type = s(h5(CONN_DIR / "nodes" / "type.h5"))
type_axis = list(OrderedDict.fromkeys(node_type.tolist()))
assert len(type_axis) == 65
json_order = [n["name"] for n in nodes_spec]
axis_equals_json_order = type_axis == json_order

# ------------------------------------------------------------------------------------------
# 1. Constant and varying fields
# ------------------------------------------------------------------------------------------
def value_set(vals):
    return sorted({canon(v) for v in vals})


node_field_values = {k: value_set([n[k] for n in nodes_spec]) for k in node_keys}
edge_field_values = {k: value_set([e[k] for e in edges_spec]) for k in edge_keys
                     if k not in ("offsets",)}
node_constants = {k: json.loads(v[0]) for k, v in node_field_values.items() if len(v) == 1}
edge_constants = {k: json.loads(v[0]) for k, v in edge_field_values.items() if len(v) == 1}

# ------------------------------------------------------------------------------------------
# 2. The compiled bank, collapsed to (src, tar, du, dv)
# ------------------------------------------------------------------------------------------
E = CONN_DIR / "edges"
df = pd.DataFrame(dict(
    src=s(h5(E / "source_type.h5")), tar=s(h5(E / "target_type.h5")),
    du=h5(E / "du.h5").astype(int), dv=h5(E / "dv.h5").astype(int),
    n_syn=h5(E / "n_syn.h5"), sign=h5(E / "sign.h5"),
    cert=h5(E / "n_syn_certainty.h5"),
))
n_edge_instances = len(df)
g = df.groupby(["src", "tar", "du", "dv"], sort=False)
agg = g.agg(n_syn=("n_syn", "first"), n_syn_nu=("n_syn", "nunique"),
            sign=("sign", "first"), sign_nu=("sign", "nunique"),
            cert=("cert", "first"), cert_nu=("cert", "nunique"),
            n_instances=("n_syn", "size")).reset_index()
assert (agg.n_syn_nu == 1).all() and (agg.sign_nu == 1).all() and (agg.cert_nu == 1).all()
bank = {(r.src, r.tar, int(r.du), int(r.dv)): r for r in agg.itertuples(index=False)}
assert len(bank) == 2355, len(bank)
bank_pairs = {(k[0], k[1]) for k in bank}
assert len(bank_pairs) == 604

# ------------------------------------------------------------------------------------------
# 3. Provenance of every offset: json / hull fill (flyvis's own fill_hull) / dropped
# ------------------------------------------------------------------------------------------
offset_rows = []
pair_rows = []
seen_bank_keys = set()
n_hull_points_total = 0
n_hull_points_dropped = 0
max_abs_dn_matched = 0.0
for j, e in enumerate(edges_spec):
    src, tar = e["src"], e["tar"]
    raw = e["offsets"]
    filled = (fv_conn.fill_hull(raw, N_SYN_FILL)
              if N_SYN_FILL > 0 and len(raw) >= 3 else raw)
    hull_part = filled[len(raw):]
    n_hull_points_total += len(hull_part)
    rows_here = []
    for order, ((du, dv), n) in enumerate(raw):
        key = (src, tar, int(du), int(dv))
        in_bank = key in bank
        r = dict(src=src, tar=tar, du=int(du), dv=int(dv),
                 n_syn=repr(float(bank[key].n_syn)) if in_bank else repr(float(n)),
                 n_syn_json=json.dumps(n), sign=int(e["alpha"]),
                 provenance="in_json" if in_bank else "dropped",
                 json_index=j, json_offset_order=order)
        if in_bank:
            max_abs_dn_matched = max(max_abs_dn_matched, abs(float(bank[key].n_syn) - n))
            assert int(bank[key].sign) == int(e["alpha"])
            seen_bank_keys.add(key)
        rows_here.append(r)
    for (du, dv), n in hull_part:
        key = (src, tar, int(du), int(dv))
        if key in bank:
            assert float(bank[key].n_syn) == float(N_SYN_FILL)
            seen_bank_keys.add(key)
            rows_here.append(dict(src=src, tar=tar, du=int(du), dv=int(dv),
                                  n_syn=repr(float(bank[key].n_syn)), n_syn_json="",
                                  sign=int(e["alpha"]), provenance="hull_filled",
                                  json_index=j, json_offset_order=""))
        else:
            n_hull_points_dropped += 1
    offset_rows.extend(rows_here)
    inst = (src, tar) in bank_pairs
    comp = [r for r in rows_here if r["provenance"] != "dropped"]
    # the compiled lambda_mult is stored per edge instance as n_syn_certainty (float32 cast)
    if inst:
        certs = {float(bank[(src, tar, r["du"], r["dv"])].cert) for r in comp}
        assert certs == {float(np.float32(e["lambda_mult"]))}, (src, tar, certs)
    note = ""
    if not inst:
        note = ("never instantiated: its only offset(s) never land on a cell of the target's "
                "stride lattice, and connectome.py:497-498 suppresses the KeyError")
    pair_rows.append(dict(
        json_index=j, src=src, tar=tar, alpha=int(e["alpha"]),
        alpha_fixed=bool(e["alpha_fixed"]),
        alpha_references=";".join(e["alpha_references"]),
        lambda_mult=repr(float(e["lambda_mult"])), edge_type=e["edge_type"],
        n_offsets_json=len(raw),
        n_synapses_json_total=repr(math.fsum(float(o[1]) for o in raw)),
        instantiated=inst,
        n_offsets_compiled=len(comp),
        n_offsets_hull_filled=sum(r["provenance"] == "hull_filled" for r in rows_here),
        n_offsets_dropped=sum(r["provenance"] == "dropped" for r in rows_here),
        n_synapses_compiled_total=repr(math.fsum(float(r["n_syn"]) for r in comp)),
        note=note,
    ))

assert seen_bank_keys == set(bank), "a compiled row is neither in the json nor a hull fill"
prov_counts = {p: sum(r["provenance"] == p for r in offset_rows)
               for p in ("in_json", "hull_filled", "dropped")}
assert prov_counts == {"in_json": 2117, "hull_filled": 238, "dropped": 23}, prov_counts
not_instantiated = [(r["src"], r["tar"]) for r in pair_rows if not r["instantiated"]]
assert not_instantiated == [("Lawf1", "Lawf1")], not_instantiated
dropped_pairs = sorted({(r["src"], r["tar"]) for r in offset_rows
                        if r["provenance"] == "dropped"})

# ------------------------------------------------------------------------------------------
# 4. types.csv
# ------------------------------------------------------------------------------------------
role_h5 = s(h5(CONN_DIR / "nodes" / "role.h5"))
role_of = {}
for t, r in zip(node_type.tolist(), role_h5.tolist()):
    role_of.setdefault(t, set()).add(r)
assert all(len(v) == 1 for v in role_of.values())
layout_of = {a: b for a, b in s(h5(CONN_DIR / "layout.h5")).tolist()}
cci = h5(CONN_DIR / "central_cells_index.h5")
n_cells = {t: int((node_type == t).sum()) for t in type_axis}
spec_by_name = {n["name"]: (i, n) for i, n in enumerate(nodes_spec)}


def n_cells_formula(extent, su, sv):
    return sum(1 for u in range(-extent, extent + 1)
               for v in range(max(-extent, -extent - u), min(extent, extent - u) + 1)
               if u % su == 0 and v % sv == 0)


type_rows = []
for i, t in enumerate(type_axis):
    ji, n = spec_by_name[t]
    kind, strides = n["pattern"]
    assert kind == "stride"
    su, sv = strides
    assert n_cells[t] == n_cells_formula(EXTENT_COMPILED, su, sv)
    type_rows.append(dict(
        node_order_index=i, type_name=t, json_index=ji, pattern_kind=kind,
        stride_u=su, stride_v=sv, role=next(iter(role_of[t])), layout=layout_of[t],
        in_input_units=t in spec["input_units"], in_output_units=t in spec["output_units"],
        n_out_entries=sum(e["src"] == t for e in edges_spec),
        n_in_entries=sum(e["tar"] == t for e in edges_spec),
        n_cells_extent15=n_cells[t], n_cells_extent5=n_cells_formula(5, su, sv),
        central_cells_index_extent15=int(cci[i]),
    ))
type_cols = list(type_rows[0].keys())

# ------------------------------------------------------------------------------------------
# 5. Birth ids (generation zero). Rule in REGISTRY.md (version BIRTH_ID_VERSION).
#    The id is DERIVED FROM THE ENTITY: the first 12 hex digits of the sha256 of a versioned
#    canonical string built from the element's canonical name (a type: its name; an ordered
#    pair: "SRC->TAR"). It does not depend on any enumeration order, so a re-extraction from
#    another flyvis version or another connectome gives a homologue the same id.
#    display_no is a counter kept for human display only (types by name code point, then pairs
#    by (src, tar) code point); it is never a key. It equals the pre-v1 integer birth id.
# ------------------------------------------------------------------------------------------
BIRTH_ID_VERSION = "cs-birth-v1"
BIRTH_ID_HEX = 12


def type_birth_id(name):
    return sha256_bytes(f"{BIRTH_ID_VERSION}|type|{name}".encode("utf-8"))[:BIRTH_ID_HEX]


def pair_birth_id(src, tar):
    return sha256_bytes(f"{BIRTH_ID_VERSION}|pair|{src}->{tar}".encode("utf-8"))[:BIRTH_ID_HEX]


type_names_sorted = sorted(n["name"] for n in nodes_spec)
assert all(re.fullmatch(r"[A-Za-z0-9()]+", t) for t in type_names_sorted)  # no - > | : or space
# Collision check over every element the ids can ever be asked about here: 65 types and the
# full 65 x 65 ordered-pair grid (4,225 cells, including the 3,621 that are not pairs of the
# bank). The folds of C6 key on pair ids of empty cells too.
all_ids = [type_birth_id(t) for t in type_names_sorted] + [
    pair_birth_id(a, b) for a in type_names_sorted for b in type_names_sorted]
n_id_domain = len(all_ids)
assert n_id_domain == 65 + 65 * 65
assert len(set(all_ids)) == n_id_domain, "birth-id collision: see REGISTRY.md collision policy"

type_bid = {}
bid_rows = []
counter = 0
for name in type_names_sorted:
    counter += 1
    type_bid[name] = type_birth_id(name)
    _, n = spec_by_name[name]
    bid_rows.append(dict(
        birth_id=type_bid[name], display_no=counter, kind="type", birth_key=f"type:{name}",
        generation_born=0, parent_ids="", src_birth_id="", tar_birth_id="",
        expressed_in_compiled_bank=True,
        content_sha256=sha256_bytes(canon(n).encode("utf-8")),
    ))
edge_by_pair = {(e["src"], e["tar"]): e for e in edges_spec}
assert len(edge_by_pair) == 605
for (src, tar) in sorted(edge_by_pair):
    counter += 1
    bid_rows.append(dict(
        birth_id=pair_birth_id(src, tar), display_no=counter, kind="pair",
        birth_key=f"pair:{src}>{tar}", generation_born=0,
        parent_ids="", src_birth_id=type_bid[src], tar_birth_id=type_bid[tar],
        expressed_in_compiled_bank=(src, tar) in bank_pairs,
        content_sha256=sha256_bytes(canon(edge_by_pair[(src, tar)]).encode("utf-8")),
    ))
next_display_no = counter + 1
pair_bid = {r["birth_key"][5:]: r["birth_id"] for r in bid_rows if r["kind"] == "pair"}
for r in pair_rows:
    r["birth_id"] = pair_bid[f"{r['src']}>{r['tar']}"]
for r in type_rows:
    r["birth_id"] = type_bid[r["type_name"]]
for r in offset_rows:
    r["pair_birth_id"] = pair_bid[f"{r['src']}>{r['tar']}"]

# ------------------------------------------------------------------------------------------
# 6. Write the tables
# ------------------------------------------------------------------------------------------
type_cols = ["node_order_index", "type_name", "birth_id"] + [
    c for c in type_cols if c not in ("node_order_index", "type_name")]
write_csv(OUT / "types.csv", HEADER, type_cols, type_rows)

pair_cols = ["json_index", "birth_id", "src", "tar", "alpha", "alpha_fixed", "alpha_references",
             "lambda_mult", "edge_type", "n_offsets_json", "n_synapses_json_total",
             "instantiated", "n_offsets_compiled", "n_offsets_hull_filled", "n_offsets_dropped",
             "n_synapses_compiled_total", "note"]
write_csv(OUT / "type_pairs.csv", HEADER, pair_cols, pair_rows)

# offsets: compiled rows + dropped, ordered by json entry then json offset order, hull after
off_cols = ["pair_birth_id", "src", "tar", "du", "dv", "n_syn", "n_syn_json", "sign",
            "provenance", "json_index", "json_offset_order"]
write_csv(OUT / "offsets.csv", HEADER, off_cols, offset_rows)

bid_cols = ["birth_id", "display_no", "kind", "birth_key", "generation_born", "parent_ids",
            "src_birth_id", "tar_birth_id", "expressed_in_compiled_bank", "content_sha256"]
bid_header = (HEADER + f"; birth_id=sha256('{BIRTH_ID_VERSION}|type|NAME' or "
              f"'{BIRTH_ID_VERSION}|pair|SRC->TAR')[:{BIRTH_ID_HEX}]; "
              f"next_display_no={next_display_no}; rule=REGISTRY.md")
bid_path = OUT / "birth_ids.csv"
tmp = OUT / "birth_ids.csv.new"
write_csv(tmp, bid_header, bid_cols, bid_rows)
if bid_path.exists():
    old_lines = bid_path.read_text(encoding="utf-8").split("\n")
    new_body = tmp.read_bytes().split(b"\n", 1)[1]
    old_body = bid_path.read_bytes().split(b"\n", 1)[1]
    if old_lines[1].startswith("birth_id,kind,"):
        # One-time, audited migration from the pre-v1 counter registry: allowed only with the
        # explicit flag, and only if every old row maps to exactly one new row by birth_key,
        # its old integer id equals the new display_no, and nothing else in the row changed.
        if "--migrate-from-counter-ids" not in sys.argv:
            tmp.unlink()
            sys.exit("REFUSED: birth_ids.csv holds pre-v1 counter ids. Re-run with "
                     "--migrate-from-counter-ids to perform the audited migration.")
        old = pd.read_csv(bid_path, skiprows=1, dtype=str, keep_default_na=False)
        new = pd.read_csv(tmp, skiprows=1, dtype=str, keep_default_na=False)
        old_by_key = {r.birth_key: r for r in old.itertuples(index=False)}
        new_by_key = {r.birth_key: r for r in new.itertuples(index=False)}
        assert set(old_by_key) == set(new_by_key) and len(old) == len(new) == 670
        old_int_to_new = {old_by_key[k].birth_id: new_by_key[k].birth_id for k in old_by_key}
        for k in old_by_key:
            o, nw = old_by_key[k], new_by_key[k]
            assert nw.display_no == o.birth_id, k
            for c in ("kind", "generation_born", "parent_ids", "expressed_in_compiled_bank",
                      "content_sha256"):
                assert getattr(o, c) == getattr(nw, c), (k, c)
            for c in ("src_birth_id", "tar_birth_id"):
                assert (getattr(o, c) == "" and getattr(nw, c) == "") or \
                    old_int_to_new[getattr(o, c)] == getattr(nw, c), (k, c)
    elif old_body != new_body:
        tmp.unlink()
        sys.exit("REFUSED: birth_ids.csv exists and the regenerated registry differs. Birth ids "
                 "are never reassigned (REGISTRY.md). Nothing was overwritten.")
os.replace(tmp, bid_path)

# Third check on the ids themselves: re-read the written registry and re-derive every id from
# its birth_key alone. The id travels with the entity, not with a position in a list.
_R = pd.read_csv(bid_path, skiprows=1, dtype=str, keep_default_na=False)
for r in _R.itertuples(index=False):
    kind, name = r.birth_key.split(":", 1)
    want = type_birth_id(name) if kind == "type" else pair_birth_id(*name.split(">"))
    assert r.birth_id == want, r.birth_key
ids_rederived_from_keys = True

# ------------------------------------------------------------------------------------------
# 7. The two readings (von Neumann, literature.md §I entry 31)
#    Reading 1, copy: the files are bytes; their sha256 is recorded below.
#    Reading 2, decode: rebuild the json from the csvs alone, compare to the source, then
#    compile it with flyvis's own add_nodes/add_edges at extent 5 and compare to the bank.
# ------------------------------------------------------------------------------------------
def read_csv(path):
    return pd.read_csv(path, comment=None, skiprows=1, dtype=str, keep_default_na=False,
                       encoding="utf-8")


T = read_csv(OUT / "types.csv")
P = read_csv(OUT / "type_pairs.csv")
O = read_csv(OUT / "offsets.csv")
rec_nodes = []
for _, r in T.sort_values("json_index", key=lambda c: c.astype(int)).iterrows():
    n = {"name": r.type_name, "pattern": [r.pattern_kind, [int(r.stride_u), int(r.stride_v)]]}
    n.update(node_constants)
    rec_nodes.append({k: n[k] for k in node_keys})
rec_edges = []
Oj = O[O.provenance != "hull_filled"].copy()
Oj["ji"] = Oj.json_index.astype(int)
Oj["oo"] = Oj.json_offset_order.astype(int)
Oj = Oj.sort_values(["ji", "oo"])
offs_by_j = {j: [[[int(a.du), int(a.dv)], json.loads(a.n_syn_json)] for a in grp.itertuples()]
             for j, grp in Oj.groupby("ji")}
for _, r in P.sort_values("json_index", key=lambda c: c.astype(int)).iterrows():
    e = {"src": r.src, "tar": r.tar, "offsets": offs_by_j[int(r.json_index)],
         "alpha": int(r.alpha), "alpha_fixed": r.alpha_fixed == "True",
         "alpha_references": r.alpha_references.split(";") if r.alpha_references else [],
         "lambda_mult": float(r.lambda_mult), "edge_type": r.edge_type}
    for k, v in edge_constants.items():
        e.setdefault(k, v)
    rec_edges.append({k: e[k] for k in edge_keys})
rec_spec = {"nodes": rec_nodes, "edges": rec_edges, "receptors": spec["receptors"],
            "input_units": [t for t in T.type_name if T.set_index("type_name").loc[t,
                            "in_input_units"] == "True"],
            "output_units": [t for t in T.type_name if T.set_index("type_name").loc[t,
                             "in_output_units"] == "True"]}
# unit lists follow the json's own order, which the csv does not carry: compare as sets
json_roundtrip_equal = (rec_nodes == nodes_spec and rec_edges == edges_spec
                        and set(rec_spec["input_units"]) == set(spec["input_units"])
                        and set(rec_spec["output_units"]) == set(spec["output_units"])
                        and rec_spec["receptors"] == spec["receptors"])
assert json_roundtrip_equal

seq_n, seq_e = [], []
fv_conn.add_nodes(seq_n, rec_nodes, EXTENT_DECODE_CHECK)
fv_conn.add_edges(seq_e, seq_n, rec_edges, N_SYN_FILL)
dec = {}
for ed in seq_e:
    k = (ed.source.type, ed.target.type, ed.target.u - ed.source.u, ed.target.v - ed.source.v)
    dec.setdefault(k, (float(np.float32(ed.n_syn)), int(ed.sign)))
decode_equal = (set(dec) == set(bank) and all(
    dec[k][0] == float(bank[k].n_syn) and dec[k][1] == int(bank[k].sign) for k in bank))
assert decode_equal

# ------------------------------------------------------------------------------------------
# 8. Meta
# ------------------------------------------------------------------------------------------
refs = {}
for e in edges_spec:
    for k in e["alpha_references"]:
        refs[k] = refs.get(k, 0) + 1
pc_keys = sorted(k for k in refs if re.search(r"PC\d{4}$", k))  # e.g. NernPC2018
entries_with_refs = [e for e in edges_spec if e["alpha_references"]]
entries_pc_only = [e for e in entries_with_refs
                   if all(k in pc_keys for k in e["alpha_references"])]
entries_any_pub = [e for e in entries_with_refs
                   if any(k not in pc_keys for k in e["alpha_references"])]

compiled_files = sorted(p for p in CONN_DIR.rglob("*") if p.is_file())
compiled_digest = hashlib.sha256()
for p in compiled_files:
    compiled_digest.update(p.relative_to(CONN_DIR).as_posix().encode("utf-8") + b"\0")
    compiled_digest.update(sha256_file(p).encode("ascii") + b"\n")

outputs = ["types.csv", "type_pairs.csv", "offsets.csv", "birth_ids.csv"]
meta = OrderedDict(
    what="Generation-zero bank for the genome track: extraction of the flyvis connectome json "
         "and its compiled tables. Structural integers and strings only; no training result.",
    source=OrderedDict(package="flyvis", version=flyvis.__version__, file=JSON_REL,
                       sha256=JSON_SHA),
    compiled=OrderedDict(
        location=f"FLYVIS_ROOT_DIR/{CONN_REL}",
        meta_yaml=(CONN_DIR / "_meta.yaml").read_text(encoding="utf-8"),
        n_files=len(compiled_files),
        digest_sha256=compiled_digest.hexdigest(),
        digest_rule="sha256 over, per file in sorted relative-path order: "
                    "'<relative posix path>\\0<sha256 hex>\\n'",
        n_edge_instances=n_edge_instances, n_cells=int(len(node_type))),
    script=OrderedDict(path="results/genome/bank/extract_bank.py", sha256=SCRIPT_SHA,
                       python=sys.version.split()[0], numpy=np.__version__,
                       pandas=pd.__version__, h5py=h5py.__version__),
    outputs={o: sha256_file(OUT / o) for o in outputs},
    type_axis=OrderedDict(
        order="connectome node order: first appearance in nodes/type.h5",
        equals_json_node_order=axis_equals_json_order),
    constant_node_fields=node_constants,
    constant_edge_fields=edge_constants,
    varying_node_fields=[k for k in node_keys if k not in node_constants],
    varying_edge_fields=[k for k in edge_keys if k not in edge_constants],
    root_sections=OrderedDict(receptors=spec["receptors"],
                              n_input_units=len(spec["input_units"]),
                              n_output_units=len(spec["output_units"])),
    counts=OrderedDict(
        n_types=65, n_json_entries=605, n_json_offset_rows=sum(len(e["offsets"])
                                                              for e in edges_spec),
        n_compiled_pairs=604, n_compiled_offset_rows=2355, provenance=prov_counts,
        n_hull_points_generated=n_hull_points_total,
        n_hull_points_not_landing=n_hull_points_dropped,
        pairs_with_dropped_json_rows=[f"{a}>{b}" for a, b in dropped_pairs],
        not_instantiated=[f"{a}>{b}" for a, b in not_instantiated],
        max_abs_n_syn_json_minus_compiled_on_matched=max_abs_dn_matched),
    sign_citations=OrderedDict(
        reference_key_slots=dict(sorted(refs.items())),
        personal_communication_keys=pc_keys,
        n_citation_slots=sum(refs.values()),
        n_slots_personal_communication=sum(refs[k] for k in pc_keys),
        n_entries_with_any_reference=len(entries_with_refs),
        n_entries_citing_only_personal_communications=len(entries_pc_only),
        n_entries_citing_at_least_one_publication=len(entries_any_pub),
        n_entries_alpha_fixed=sum(bool(e["alpha_fixed"]) for e in edges_spec)),
    birth_ids=OrderedDict(
        n_types=65, n_pairs=605, rule="REGISTRY.md", version=BIRTH_ID_VERSION,
        derivation=f"first {BIRTH_ID_HEX} hex of sha256 over UTF-8 "
                   f"'{BIRTH_ID_VERSION}|type|<name>' or '{BIRTH_ID_VERSION}|pair|<src>-><tar>'",
        collision_domain=f"65 types + the full 65 x 65 ordered-pair grid = {n_id_domain} strings",
        n_collisions=0,
        display_no=OrderedDict(first=1, last=counter, next_display_no=next_display_no,
                               note="display only; equals the pre-v1 integer birth id"),
        ids_rederived_from_birth_keys=ids_rederived_from_keys),
    two_readings=OrderedDict(
        copy="outputs are byte files with the sha256 above; copying needs no interpretation",
        decode_json_roundtrip_equal=json_roundtrip_equal,
        decode_json_roundtrip_note="nodes and edges equal element for element in json order; "
                                   "input_units/output_units compared as sets (their list "
                                   "order is not carried by the csv)",
        decode_compile_extent=EXTENT_DECODE_CHECK,
        decode_compiled_equals_bank=decode_equal,
        decode_note="the json rebuilt from the csvs was compiled with flyvis's own "
                    "add_nodes/add_edges at extent 5; its (src,tar,du,dv) keys, n_syn and sign "
                    "equal the extent-15 compiled bank on all 2,355 keys"),
)
(OUT / "bank.meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n",
                                    encoding="utf-8", newline="\n")
print(json.dumps(dict(prov=prov_counts, not_instantiated=not_instantiated,
                      hull_total=n_hull_points_total, hull_dropped=n_hull_points_dropped,
                      max_dn=max_abs_dn_matched, roundtrip=json_roundtrip_equal,
                      decode=decode_equal, next_display_no=next_display_no,
                      node_constants=node_constants, edge_constants=edge_constants,
                      axis_eq_json=axis_equals_json_order,
                      cites=meta["sign_citations"]), indent=1, default=str))
