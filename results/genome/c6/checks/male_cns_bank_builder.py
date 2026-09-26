#!/usr/bin/env python3
"""The male CNS bank builder: two existence banks, one per optic lobe, from the Janelia male CNS
v1.0 flat connectome. Implements docs/plans/2026-09-25-male-cns-bank-builder-registration.md,
revision 2, with each decision's recommended option (its section 13); section numbers below
refer to it.

Modes (section 10.3): --self-test runs the fixture tests of section 11; --inspect-only is the
dry run (pins, the weight file's schema and metadata, the annotations, the map, the side rule,
the section 3.3 self-test; no weight column is read); no flag is the build.

Block A is sealed (section 9): its cells go only to the fixed-width sealed files, and nothing
else printed or written is computed from a block row.

    uv run --no-project --python 3.13.14 --with pyarrow==25.0.1 --with numpy==2.5.3 \
        --with pandas==3.0.6 --with psutil \
        python results/genome/c6/checks/male_cns_bank_builder.py [--self-test | --inspect-only] [--allow-dirty]
"""
import os
THREAD_VARS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")
# The values found before setdefault (which does not override a value already set); the
# manifest records them beside the values in effect.
THREAD_ENV_FOUND = {_v: os.environ.get(_v) for _v in THREAD_VARS}
for _v in THREAD_VARS:
    os.environ.setdefault(_v, "1")
import argparse
import dataclasses
import hashlib
import json
import math
import platform
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import psutil
import pyarrow as pa
import pyarrow.feather
import pyarrow.ipc

HERE = Path(__file__).resolve().parent
C6 = HERE.parent
ROOT = C6.parents[2]                                   # the repository root
REGISTRATION = "docs/plans/2026-09-25-male-cns-bank-builder-registration.md"
REGISTRATION_REVISION = "2"
TEST_FILE = HERE / "test_male_cns_bank_builder.py"

# Section 1.1: inputs and pins.
DATA_DIR = ROOT.parent / "connectome-seed-data" / "Janelia"
DERIVED = DATA_DIR / "derived"                         # section 10.1 (D11): private outputs
ANNOTATIONS = "body-annotations-male-cns-v1.0-minconf-0.5.feather"
WEIGHTS = "connectome-weights-male-cns-v1.0-minconf-0.5.feather"
JANELIA_PINS = {  # file -> (bytes, sha256)
    ANNOTATIONS: (14_483_314, "2177e246113e4cfbf1e7772ec37c6da1955ff22e8063d0b1f833101f99a9a3b2"),
    WEIGHTS: (1_051_241_946, "e35da783d1c686b2b58b3b87cd6a403ae43bfcfba8bff28e08ef752c1a56afc1")}
DOWNLOADED = "2026-09-23 UTC"                          # connectome-seed-data/Janelia/SOURCE.md
SOURCE_NOTE = ("Male CNS v1.0 (Berg et al. 2026), flat connectome files from "
               "https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome/; "
               "licence CC-BY (SOURCE.md)")
FLYVIS_PINS = {  # LF-normalised sha256
    "results/genome/bank/offsets.csv":
        "8c45e8508d8f6ae45e9ab3f9d95d58e4521894ccfa51954f6d77d41e550fa5f0",
    "results/genome/bank/types.csv":
        "237a195a36f62ce182fee8486394c27d2beb9825bc029cb215c39c0fa323a477"}
WEIGHT_ROWS = 151_856_684                              # section 1.2: the pandas metadata `stop`
WEIGHT_SCHEMA = (("body_pre", "int64"), ("body_post", "int64"), ("weight", "int64"))
VERSIONS = {"python": "3.13.14", "numpy": "2.5.3", "pandas": "3.0.6", "pyarrow": "25.0.1"}
MEMORY_CAP = 4 * 1024 ** 3                             # section 6.4

# Section 3: the type map. Canonical column `type`; a closed override table of three flyvis
# names reads `flywireType`. Section 3.2 leaves the R1-R6 string to the dry run, which prints it.
CANONICAL = "type"
OVERRIDE_COLUMN = "flywireType"
SPECIAL = {
    **{r: ("type", "R1-R6") for r in ("R1", "R2", "R3", "R4", "R5", "R6")},   # one population
    "R7": ("flywireType", "R7"),                       # override: the R7 roll-up
    "R8": ("flywireType", "R8"),                       # override: the R8 roll-up
    "TmY9": ("flywireType", "TmY9q"),                  # override, flagged (D5)
    "CT1(Lo1)": ("type", "CT1"), "CT1(M10)": ("type", "CT1"),   # one cell per lobe
    "Am": ("type", "Am1"),                             # renamed
}
ABSENT = ("Mi3", "Mi11", "Mi12", "Tm28")
FLIP = frozenset({"CT1"})                              # section 4: declared, not inferred
SIDE_COLUMNS = ("somaSide", "rootSide", "instance")
SUFFIX_RE = re.compile(r"(?s).+_(L|R)")                # section 4: ends in _L/_R, not "_L" alone
LOBES = ("L", "R")

# The block (knockout registration section 1.2): sources x targets, row-major.
ON, OFF = ("Mi1", "Tm3", "Mi4", "Mi9"), ("Tm1", "Tm2", "Tm4", "Tm9")
T4, T5 = ("T4a", "T4b", "T4c", "T4d"), ("T5a", "T5b", "T5c", "T5d")
SOURCES, TARGETS = ON + OFF, T4 + T5
BLOCK_NAMES = [(s, t) for s in SOURCES for t in TARGETS]
INFERABLE_MIN = 2                                      # Johnny's rule, knockout section 1.4

# Section 5.3: the registered targets.
REGISTERED_COLLAPSE = "pooled"                         # D15 (ii)
REGISTERED_TARGETS = {
    "pooled": {"omega": 2961, "present": 511, "T": 0.172577, "K": 1022},
    "restrict": {"omega": 2961, "present": 497, "T": 0.167849, "K": 994},
    "full_grid_b_prime": {"omega_full": 4161, "present_full": 572, "T": 0.137467, "K": 814}}
W_MIN = 1                                              # D2
DIAG_W_MINS = (1, 2, 3)
FIXED_CUTS = (0.5, 1.0, 2.0)
FIELD_MAX = 10 ** 12                                   # section 9: integers zero-padded to 12


class Stop(Exception):
    """A registered stop. The message is printed; the build writes nothing after it."""


@dataclasses.dataclass
class Config:
    data_dir: Path = DATA_DIR
    annotations: str = ANNOTATIONS
    weights: str = WEIGHTS
    janelia_pins: dict = dataclasses.field(default_factory=lambda: dict(JANELIA_PINS))
    weight_rows: int = WEIGHT_ROWS
    repo_root: Path = ROOT
    flyvis_pins: dict = dataclasses.field(default_factory=lambda: dict(FLYVIS_PINS))
    special: dict = dataclasses.field(default_factory=lambda: dict(SPECIAL))
    absent: tuple = ABSENT
    flip: frozenset = FLIP
    canonical: str = CANONICAL
    registered_targets: dict = dataclasses.field(default_factory=lambda: dict(REGISTERED_TARGETS))
    collapse: str = REGISTERED_COLLAPSE
    memory_cap: int = MEMORY_CAP
    derived: Path = DERIVED


class Report:
    """Every printed line goes through here; BUILD.md is these lines."""

    def __init__(self, stream=None):
        self.lines, self.stream = [], stream if stream is not None else sys.stdout

    def say(self, m=""):
        self.lines.append(str(m))
        print(m, file=self.stream, flush=True)


# ------------------------------------------------------------------------------------------
# Small helpers

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_lf(p):
    return hashlib.sha256(Path(p).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def id_hex(kind, name):
    """harness.id_hex, re-implemented: the builder imports nothing from the harness (10.4)."""
    return hashlib.sha256(f"cs-birth-v1|{kind}|{name}".encode()).hexdigest()[:12]


def round_half_up(x):
    return int(math.floor(x + 0.5))


def git(*args, root=ROOT):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True,
                          check=True).stdout.rstrip()


def dirty_listing(root=ROOT):
    return git("status", "--porcelain", "--", "results/genome/c6", "docs/plans", root=root)


def peak_memory_bytes():
    """Peak working set where the platform reports it (Windows), else the current resident
    size; the caller keeps the maximum over its probes."""
    mi = psutil.Process().memory_info()
    return int(getattr(mi, "peak_wset", 0) or mi.rss)


def machine_record():
    """As knockout_regrow.machine_record: build and run-time BLAS (library file name only), the
    machine and CPU (no host name), the four thread variables as found and as in effect."""
    rec = {}
    try:
        cfg = np.show_config(mode="dicts")
        rec["numpy_build"] = {k: cfg.get("Build Dependencies", {}).get(k)
                              for k in ("blas", "lapack")}
        rec["numpy_machine_information"] = cfg.get("Machine Information")
        rec["numpy_simd"] = cfg.get("SIMD Extensions")
    except Exception as e:                             # recorded, never fatal
        rec["numpy_build"] = {"error": repr(e)}
    try:
        import threadpoolctl
        rec["blas_at_run_time"] = [{**i, "filepath": os.path.basename(i.get("filepath") or "")}
                                   for i in threadpoolctl.threadpool_info()]
    except Exception as e:
        rec["blas_at_run_time"] = {"error": repr(e)}
    rec["machine"] = {"machine": platform.machine(),
                      "processor": platform.processor(), "platform": platform.platform(),
                      "cpu_count": os.cpu_count(),
                      "PROCESSOR_IDENTIFIER": os.environ.get("PROCESSOR_IDENTIFIER")}
    rec["thread_env"] = {v: {"found": THREAD_ENV_FOUND[v], "in_effect": os.environ.get(v)}
                         for v in THREAD_VARS}
    return rec


def versions_found():
    return {"python": platform.python_version(), "numpy": np.__version__,
            "pandas": pd.__version__, "pyarrow": pa.__version__, "psutil": psutil.__version__}


def check_versions(R):
    v = versions_found()
    bad = {k: (v[k], VERSIONS[k]) for k in VERSIONS if v[k] != VERSIONS[k]}
    R.say(f"versions: {v} (psutil not pinned, section 10.4)")
    if bad:
        raise Stop(f"VERSIONS DIFFER (section 10.4): {bad}")
    return v


# ------------------------------------------------------------------------------------------
# Section 1.1: pins

def check_pins(cfg, R):
    rec = {"flyvis": {}, "janelia": {}}
    for rel, pin in cfg.flyvis_pins.items():
        p = cfg.repo_root / rel
        with open(p, encoding="utf-8") as fh:
            first = fh.readline()
        if not first.startswith("# source=flyvis"):
            raise Stop(f"PINS DIFFER: {rel} line 1 does not start with '# source=flyvis'")
        got = sha256_lf(p)
        if got != pin:
            raise Stop(f"PINS DIFFER: {rel} sha256 (LF) {got}, pinned {pin}")
        rec["flyvis"][rel] = {"sha256_lf": got}
    for name, (size, pin) in cfg.janelia_pins.items():
        p = cfg.data_dir / name
        got_size, got = p.stat().st_size, sha256_file(p)
        if (got_size, got) != (size, pin):
            raise Stop(f"PINS DIFFER: {name} size {got_size} sha256 {got}; pinned {size} {pin}")
        rec["janelia"][name] = {"size_bytes": got_size, "sha256": got, "downloaded": DOWNLOADED,
                                "source": SOURCE_NOTE}
    R.say("pins: flyvis-65 CSVs and both Janelia files equal section 1.1")
    for rel, r in rec["flyvis"].items():
        R.say(f"  {rel}: sha256 (LF) {r['sha256_lf']}")
    for name, r in rec["janelia"].items():
        R.say(f"  {name}: {r['size_bytes']} bytes, sha256 {r['sha256']}, downloaded {DOWNLOADED}")
    return rec


# ------------------------------------------------------------------------------------------
# Section 1.2: the weight file's schema and metadata (no weight column read)

def weight_file_header(cfg, R):
    p = cfg.data_dir / cfg.weights
    reader = pa.ipc.open_file(pa.memory_map(str(p), "r"))
    schema = tuple((f.name, str(f.type)) for f in reader.schema)
    if schema != WEIGHT_SCHEMA:
        raise Stop(f"WEIGHT SCHEMA DIFFERS: {schema}, expected {WEIGHT_SCHEMA}")
    md = json.loads(reader.schema.metadata[b"pandas"])
    idx = md["index_columns"][0]
    if not (isinstance(idx, dict) and idx.get("kind") == "range" and idx.get("start") == 0
            and idx.get("step") == 1):
        raise Stop(f"ROW COUNT DIFFERS: the pandas metadata index is not a range from 0: {idx}")
    stop = int(idx["stop"])
    R.say(f"weight file: schema {[f'{n}: {t}' for n, t in schema]}; "
          f"{reader.num_record_batches} record batches; pandas metadata stop {stop}; "
          f"written by {md.get('creator')}")
    R.say(f"  uncompressed int64 data would be {stop * 24} bytes; the file is "
          f"{p.stat().st_size} bytes (the codec is not read: that needs a record batch)")
    if stop != cfg.weight_rows:
        raise Stop(f"ROW COUNT DIFFERS: pandas metadata stop {stop}, registered {cfg.weight_rows}")
    return {"schema": [list(x) for x in schema], "num_record_batches": reader.num_record_batches,
            "metadata_stop": stop, "creator": md.get("creator")}


# ------------------------------------------------------------------------------------------
# Section 3: flyvis-65, the map, the placed grid

def read_flyvis(cfg):
    """types.csv in birth-id order (harness order); presence under C6: a key with at least one
    non-dropped row."""
    rd = lambda rel: pd.read_csv(cfg.repo_root / rel, skiprows=1, dtype=str,
                                 keep_default_na=False, encoding="utf-8")
    T = rd("results/genome/bank/types.csv").sort_values("birth_id").reset_index(drop=True)
    names = T.type_name.tolist()
    birth = dict(zip(T.type_name, T.birth_id))
    if len(names) != 65 or any(birth[n] != id_hex("type", n) for n in names):
        raise Stop("FLYVIS TYPES DIFFER: types.csv does not give 65 names with harness birth ids")
    idx = {n: i for i, n in enumerate(names)}
    O = rd("results/genome/bank/offsets.csv")
    present = np.zeros((65, 65), bool)
    for s, t, prov in zip(O.src, O.tar, O.provenance):
        if prov != "dropped":
            present[idx[s], idx[t]] = True
    if int(present.sum()) != 604:
        raise Stop("FLYVIS BANK DIFFERS: present cells are not the harness's 604")
    return names, birth, present


def build_map(names, birth, cfg):
    """Section 3.2 (D4): names sharing a male string form one population, placed at the member
    whose birth id sorts first. Populations come back in harness order of that member."""
    mapped = {}
    for n in names:
        if n in cfg.absent:
            continue
        mapped[n] = cfg.special.get(n, (cfg.canonical, n))
    groups = {}
    for n, key in mapped.items():
        groups.setdefault(key, []).append(n)
    pops = []
    for (col, s), members in groups.items():
        members = sorted(members, key=lambda m: birth[m])
        pops.append({"name": members[0], "members": members, "column": col, "string": s})
    order = {n: i for i, n in enumerate(names)}
    pops.sort(key=lambda p: order[p["name"]])
    return mapped, pops


def block_mask(placed):
    ix = {n: i for i, n in enumerate(placed)}
    missing = [n for n in SOURCES + TARGETS if n not in ix]
    if missing:
        raise Stop(f"BLOCK TYPE NOT PLACED: {missing}")
    B = np.zeros((len(placed), len(placed)), bool)
    for s, t in BLOCK_NAMES:
        B[ix[s], ix[t]] = True
    return B


def collapse(present65, names, pops, mode):
    """D15. 'restrict': a placed index reads its own flyvis row and column. 'pooled': the
    logical OR over its population's members."""
    idx = {n: i for i, n in enumerate(names)}
    rows = [[idx[m] for m in (p["members"] if mode == "pooled" else [p["name"]])] for p in pops]
    P = len(pops)
    C = np.zeros((P, P), bool)
    for a in range(P):
        for b in range(P):
            C[a, b] = present65[np.ix_(rows[a], rows[b])].any()
    return C


def density_targets(present65, names, pops, cfg, R):
    """Section 5.3 in the order of 5.2 (map frozen, then T and K); the block is removed after
    the collapse and before any count."""
    placed = [p["name"] for p in pops]
    B = block_mask(placed)
    omega = ~B
    n_omega = int(omega.sum())
    out = {}
    for mode in ("pooled", "restrict"):
        C = collapse(present65, names, pops, mode)
        present = int((C & omega).sum())
        T = present / n_omega
        out[mode] = {"omega": n_omega, "present": present, "T": round(T, 6),
                     "T_exact": T, "K": round_half_up(T * 2 * n_omega)}
    idx = {n: i for i, n in enumerate(names)}
    B65 = np.zeros((65, 65), bool)
    for s, t in BLOCK_NAMES:
        B65[idx[s], idx[t]] = True
    pf, nf = int((present65 & ~B65).sum()), int((~B65).sum())
    Tf = pf / nf
    out["full_grid_b_prime"] = {"omega_full": nf, "present_full": pf, "T": round(Tf, 6),
                                "T_exact": Tf, "K": round_half_up(Tf * 2 * n_omega)}
    R.say(f"density targets (section 5.3; placed grid {len(placed)} types, "
          f"|Omega| = {n_omega} outside cells):")
    for mode, r in out.items():
        reg = cfg.registered_targets.get(mode)
        tag = " <- registered (D15)" if mode == cfg.collapse else ""
        R.say(f"  {mode:18s} {({k: v for k, v in r.items() if k != 'T_exact'})}; "
              f"registered {reg}{tag}")
    reg, got = cfg.registered_targets[cfg.collapse], out[cfg.collapse]
    if any(got[k] != reg[k] for k in reg):
        raise Stop(f"DENSITY TARGET DIFFERS: {cfg.collapse} {got} vs registered {reg} "
                   "(section 5.2: a map changed without an amendment)")
    return out, B


# ------------------------------------------------------------------------------------------
# Sections 3.3 and 4: annotations, the side rule, the self-test

def suffix_side(inst):
    """Section 4: the unchanged string ends with exactly _L or _R and is not '_L' or '_R'
    alone; anything else (null, _L_1, (L), _l) is no suffix."""
    if not isinstance(inst, str):
        return None
    m = SUFFIX_RE.fullmatch(inst)
    return m.group(1) if m else None


def side_rule(soma, root, inst):
    n = len(soma)
    side = np.full(n, None, object)
    step = np.full(n, "unassigned", object)
    for i in range(n):
        if isinstance(soma[i], str) and soma[i] in LOBES:
            side[i], step[i] = soma[i], "somaSide"
        elif isinstance(root[i], str) and root[i] in LOBES:
            side[i], step[i] = root[i], "rootSide"
        else:
            s = suffix_side(inst[i])
            if s is not None:
                side[i], step[i] = s, "instance"
    return side, step


ANN_COLUMNS = ("bodyId", "type", "flywireType", "somaSide", "rootSide", "instance", "status",
               "assignedOlHex1")


def read_annotations(cfg, R):
    p = cfg.data_dir / cfg.annotations
    t = pa.feather.read_table(p)
    names = set(t.schema.names)
    if "bodyId" not in names:
        raise Stop("ZERO NAME MATCHES: the annotation file has no bodyId column")
    n = t.num_rows
    cols = {"bodyId": t.column("bodyId").to_numpy().astype(np.int64)}
    for c in ANN_COLUMNS[1:]:
        if c in names:
            cols[c] = np.array(t.column(c).to_pylist(), dtype=object)
        else:
            cols[c] = np.full(n, None, object)
            R.say(f"annotation column {c!r} absent from the file; read as null")
    if len(np.unique(cols["bodyId"])) != n:
        raise Stop("BODY IN TWO TYPES: bodyId is not unique in the annotation file")
    R.say(f"annotations: {n} rows, {len(t.schema.names)} columns")
    return cols


SPECIAL_PATTERN = re.compile(r"^(R\d|CT1|Am|TmY9)")


def print_special_strings(cols, cfg, R):
    """Sections 3.2, 10.3: the special cases' strings as they stand in the file, with body
    counts over all sides (annotation counts, not connectivity)."""
    out = {}
    R.say("special-case strings in the name columns (section 3.2; body counts, all sides):")
    for col in (cfg.canonical, OVERRIDE_COLUMN):
        vals = sorted(v for v in cols[col] if isinstance(v, str) and SPECIAL_PATTERN.match(v))
        cnt = {}
        for v in vals:
            cnt[v] = cnt.get(v, 0) + 1
        out[col] = cnt
        R.say(f"  {col}: {cnt}")
    for name in cfg.absent:
        hits = {col: int(sum(1 for v in cols[col] if v == name))
                for col in (cfg.canonical, OVERRIDE_COLUMN)}
        out[f"absent:{name}"] = hits
        R.say(f"  absent {name}: bodies by column {hits}")
    return out


def apply_map(cols, pops, cfg, R):
    """Section 3.3 self-test and the section 4 side rule. Stops: ZERO NAME MATCHES, MAP STRING
    NOT FOUND, BODY IN TWO TYPES, TYPE WITH NO CELLS."""
    n = len(cols["bodyId"])
    masks = [np.asarray(cols[p["column"]] == p["string"], bool) for p in pops]
    canon_hits = sum(int(m.sum()) for p, m in zip(pops, masks) if p["column"] == cfg.canonical)
    if canon_hits == 0:
        raise Stop(f"ZERO NAME MATCHES: the canonical column {cfg.canonical!r} matches none of "
                   "the mapped strings (section 3.3)")
    special_keys = sorted(set(cfg.special.values()))
    missing = [f"{c}={s!r}" for c, s in special_keys
               if not any(p["column"] == c and p["string"] == s and int(m.sum()) > 0
                          for p, m in zip(pops, masks))]
    if missing:
        raise Stop(f"MAP STRING NOT FOUND: {missing}; the map returns to review (section 3.3)")
    claims = np.zeros(n, np.int64)
    pop_of = np.full(n, -1, np.int64)
    for i, m in enumerate(masks):
        claims += m
        pop_of[m] = i
    if (claims > 1).any():
        raise Stop("BODY IN TWO TYPES: a body is claimed by two flyvis types (section 3.1)")
    side, step = side_rule(cols["somaSide"], cols["rootSide"], cols["instance"])
    lobe = np.full(n, -1, np.int64)
    flip = np.array([pops[k]["string"] in cfg.flip if k >= 0 else False for k in pop_of])
    for i in range(n):
        if pop_of[i] >= 0 and side[i] is not None:
            li = LOBES.index(side[i])
            lobe[i] = 1 - li if flip[i] else li
    P = len(pops)
    n_tar = np.zeros((2, P), np.int64)
    side_i = np.array([LOBES.index(s) if s is not None else -1 for s in side])
    table = []
    for k, p in enumerate(pops):
        m = pop_of == k
        for li in (0, 1):
            n_tar[li, k] = int((m & (lobe == li)).sum())
        steps = {s: [int((m & (step == s) & (side == L)).sum()) for L in LOBES]
                 for s in SIDE_COLUMNS}
        steps["unassigned"] = int((m & (step == "unassigned")).sum())
        lobe_k = np.where(side_i >= 0, 1 - side_i, -1) if p["string"] in cfg.flip else side_i

        def per_lobe(mm):
            return [int((mm & (lobe_k == li)).sum()) for li in (0, 1)]
        in_type = np.asarray(cols["type"] == p["string"], bool)
        in_fw = np.asarray(cols["flywireType"] == p["string"], bool)
        under_type, under_fw = per_lobe(in_type), per_lobe(in_fw)
        disagree = int(sum(1 for i in np.flatnonzero(in_type | in_fw)
                           if cols["type"][i] != cols["flywireType"][i]))
        where = np.flatnonzero(m)
        st = {}
        for i in where:
            key = cols["status"][i] if cols["status"][i] is not None else "null"
            st[key] = st.get(key, 0) + 1
        hex1 = int(sum(1 for i in where if cols["assignedOlHex1"][i] is not None))
        table.append({"type": p["name"], "carries": p["members"], "column": p["column"],
                      "string": p["string"], "flip": p["string"] in cfg.flip,
                      "bodies_L": int(n_tar[0, k]), "bodies_R": int(n_tar[1, k]),
                      "claimed": int(m.sum()), "side_rule": steps,
                      "type_col_L_R": under_type, "flywireType_col_L_R": under_fw,
                      "type_ne_flywireType": disagree, "status": dict(sorted(st.items())),
                      "assignedOlHex1_nonnull": hex1})
    R.say("")
    R.say("type map as applied (section 3.2). L, R: bodies per lobe after the side rule and the "
          "flip. side rule: [L, R] per step that assigned the side (before the flip). under "
          "type / flywireType: all bodies whose column equals the mapped string, per lobe. "
          "disagree: bodies where either column equals it and the two columns differ")
    for r in table:
        flag = " FLIP" if r["flip"] else ""
        carries = "" if r["carries"] == [r["type"]] else f" carries {r['carries']}"
        R.say(f"  {r['type']:9s} <- {r['column']}={r['string']!r}{flag}{carries}: "
              f"L {r['bodies_L']}, R {r['bodies_R']}; side rule {r['side_rule']}; "
              f"under type {r['type_col_L_R']}, under flywireType {r['flywireType_col_L_R']}; "
              f"disagree {r['type_ne_flywireType']}; assignedOlHex1 non-null "
              f"{r['assignedOlHex1_nonnull']}; status {r['status']}")
    R.say(f"placed types: {P}; mapped flyvis names: {sum(len(p['members']) for p in pops)}")
    empty = [(pops[k]["name"], LOBES[li]) for li in (0, 1) for k in range(P) if n_tar[li, k] == 0]
    if empty:
        raise Stop(f"TYPE WITH NO CELLS: {empty} (section 3.3)")
    R.say("self-test of the map (section 3.3): ZERO NAME MATCHES, MAP STRING NOT FOUND, BODY IN "
          "TWO TYPES, TYPE WITH NO CELLS: all pass")
    return {"pop_of": pop_of, "lobe": lobe, "n_tar": n_tar, "table": table}


# ------------------------------------------------------------------------------------------
# Section 6: the weights, by record batch

def make_lookup(cols, mp, placed):
    """Placed bodies with a lobe: sorted ids, placed index, lobe, and compact indices of the
    block's source and target bodies (for the fixed-size bit set of the duplicate check)."""
    keep = (mp["pop_of"] >= 0) & (mp["lobe"] >= 0)
    ids = cols["bodyId"][keep]
    order = np.argsort(ids, kind="stable")
    ids = ids[order]
    tix = mp["pop_of"][keep][order]
    lobe = mp["lobe"][keep][order]
    is_src = np.isin(tix, [placed.index(s) for s in SOURCES])
    is_tar = np.isin(tix, [placed.index(t) for t in TARGETS])
    bsrc = np.full(len(ids), -1, np.int64)
    btar = np.full(len(ids), -1, np.int64)
    bsrc[is_src] = np.arange(int(is_src.sum()))
    btar[is_tar] = np.arange(int(is_tar.sum()))
    return {"ids": ids, "tix": tix, "lobe": lobe, "bsrc": bsrc, "btar": btar,
            "n_bsrc": int(is_src.sum()), "n_btar": int(is_tar.sum())}


def stream_weights(cfg, lk, B, memory=peak_memory_bytes):
    """Sections 6.2-6.4. The outside accumulators are returned for printing; the block
    accumulators only under '_sealed', for the sealed files."""
    p = cfg.data_dir / cfg.weights
    reader = pa.ipc.open_file(pa.memory_map(str(p), "r"))
    md = json.loads(reader.schema.metadata[b"pandas"])
    meta_stop = int(md["index_columns"][0]["stop"])
    P = B.shape[0]
    ids, tix, lobe = lk["ids"], lk["tix"], lk["lobe"]
    nid = len(ids)
    W = np.zeros((len(DIAG_W_MINS), 2, P, P), np.int64)       # outside, same lobe
    cross = np.zeros((P, P), np.int64)                          # outside, across lobes
    tot_src, same_src = np.zeros(P, np.int64), np.zeros(P, np.int64)
    tot_tar, same_tar = np.zeros(P, np.int64), np.zeros(P, np.int64)
    Wb = np.zeros((2, P, P), np.int64)                          # block, same lobe (sealed)
    cross_b = 0                                                 # block, across lobes (sealed)
    bits = np.zeros((lk["n_bsrc"] * lk["n_btar"] + 7) // 8, np.uint8)
    out_keys = []
    rows = autapse = out_same_rows = out_cross_rows = batches = 0
    peak = memory()
    nb = reader.num_record_batches
    for bi in range(nb):
        b = reader.get_batch(bi)
        batches += 1
        pre = b.column(0).to_numpy()
        post = b.column(1).to_numpy()
        w = b.column(2).to_numpy()
        rows += len(pre)
        if nid == 0:
            continue
        ip = np.clip(np.searchsorted(ids, pre), 0, nid - 1)
        jp = np.clip(np.searchsorted(ids, post), 0, nid - 1)
        keep = (ids[ip] == pre) & (ids[jp] == post)
        autapse += int((keep & (pre == post)).sum())
        keep &= (pre != post) & (w >= W_MIN)
        a, c, ww = ip[keep], jp[keep], w[keep]
        s, t, la, lc = tix[a], tix[c], lobe[a], lobe[c]
        blk = B[s, t]
        same = la == lc
        o = ~blk
        # section 4: lobe consistency, outside type pairs only
        so, to, wo, sm = s[o], t[o], ww[o], same[o]
        tot_src += np.bincount(so, weights=wo, minlength=P).astype(np.int64)
        same_src += np.bincount(so[sm], weights=wo[sm], minlength=P).astype(np.int64)
        tot_tar += np.bincount(to, weights=wo, minlength=P).astype(np.int64)
        same_tar += np.bincount(to[sm], weights=wo[sm], minlength=P).astype(np.int64)
        m = o & same
        out_same_rows += int(m.sum())
        flat = (la[m] * P + s[m]) * P + t[m]
        wm_ = ww[m]
        for k, wmin in enumerate(DIAG_W_MINS):
            sel = wm_ >= wmin
            W[k] += np.bincount(flat[sel], weights=wm_[sel],
                                minlength=2 * P * P).astype(np.int64).reshape(2, P, P)
        mc = o & ~same
        out_cross_rows += int(mc.sum())
        cross += np.bincount(s[mc] * P + t[mc], weights=ww[mc],
                             minlength=P * P).astype(np.int64).reshape(P, P)
        out_keys.append(a[o].astype(np.int64) * nid + c[o])
        # block rows: sealed accumulators only
        mb = blk & same
        Wb += np.bincount((la[mb] * P + s[mb]) * P + t[mb], weights=ww[mb],
                          minlength=2 * P * P).astype(np.int64).reshape(2, P, P)
        cross_b += int(ww[blk & ~same].sum())
        kb = lk["bsrc"][a[blk]] * lk["n_btar"] + lk["btar"][c[blk]]
        if len(kb):
            byte, bit = kb >> 3, np.left_shift(np.uint8(1), (kb & 7).astype(np.uint8))
            if len(np.unique(kb)) != len(kb) or (bits[byte] & bit).any():
                raise Stop("DUPLICATE KEY AMONG BLOCK ROWS (section 6.3; no number is given)")
            np.bitwise_or.at(bits, byte, bit)
        peak = max(peak, memory())
        if peak > cfg.memory_cap:
            raise Stop(f"MEMORY CAP: peak resident memory above {cfg.memory_cap} bytes "
                       "(section 6.4)")
    if batches != nb:
        raise Stop(f"ROW COUNT DIFFERS: {batches} batches read of {nb}")
    if rows != meta_stop or rows != cfg.weight_rows:
        raise Stop(f"ROW COUNT DIFFERS: rows read {rows}, metadata stop {meta_stop}, "
                   f"registered {cfg.weight_rows}")
    keys = np.sort(np.concatenate(out_keys)) if out_keys else np.zeros(0, np.int64)
    dup_out = int((np.diff(keys) == 0).sum()) if len(keys) else 0
    del keys, out_keys
    peak = max(peak, memory())
    return {"W": W, "cross": cross, "tot_src": tot_src, "same_src": same_src,
            "tot_tar": tot_tar, "same_tar": same_tar, "rows_read": rows, "batches_read": batches,
            "num_record_batches": nb, "metadata_stop": meta_stop, "autapse_rows_dropped": autapse,
            "outside_rows_same_lobe": out_same_rows, "outside_rows_across_lobes": out_cross_rows,
            "duplicate_outside_keys": dup_out, "peak_memory_bytes": peak,
            "_sealed": {"Wb": Wb, "cross_b": cross_b}}


# ------------------------------------------------------------------------------------------
# Section 4: the lobe-consistency check

def lobe_consistency(st, pops, cfg, R):
    shares, bad = {}, []
    ratio = lambda a, b: int(a) / int(b) if b else None
    for k, p in enumerate(pops):
        tot = int(st["tot_src"][k] + st["tot_tar"][k])
        sh = ratio(st["same_src"][k] + st["same_tar"][k], tot)
        shares[p["name"]] = {"share": sh, "as_source": ratio(st["same_src"][k], st["tot_src"][k]),
                             "as_target": ratio(st["same_tar"][k], st["tot_tar"][k]),
                             "weight": tot, "flip": p["string"] in cfg.flip}
        if sh is not None and sh < 0.5:
            bad.append(p["name"])
    R.say("")
    R.say("lobe consistency (section 4): same-lobe share of each placed type's outside weight, "
          "as source and target together (as source / as target)")
    f = lambda v: "n/a" if v is None else f"{v:.4f}"
    for n, r in shares.items():
        R.say(f"  {n:9s} {f(r['share'])} ({f(r['as_source'])} / {f(r['as_target'])})"
              f"{'  FLIP' if r['flip'] else ''}")
    if bad:
        raise Stop(f"LOBE ASSIGNMENT INCONSISTENT: same-lobe share below 0.5 for {bad} "
                   f"(FLIP = {sorted(cfg.flip)})")
    R.say("lobe consistency: every placed type >= 0.5 (FLIP applied)")
    return shares


# ------------------------------------------------------------------------------------------
# Section 5: the cut

def choose_cut(values, K):
    """Section 5.2 steps 2-3: c = the K-th largest value; present iff x >= c and x > 0; ties all
    present (excess); fewer than K positive values -> c = the smallest positive (shortfall)."""
    v = np.sort(np.asarray(values, float))[::-1]
    pos = v[v > 0]
    if K >= 1 and len(pos) >= K:
        c = float(v[K - 1])
        n_present = int((v >= c).sum())
        return {"c": c, "present": n_present, "excess": n_present - K, "shortfall": 0}
    c = float(pos.min()) if len(pos) else math.inf
    return {"c": c, "present": int(len(pos)), "excess": 0, "shortfall": int(K - len(pos))}


def outside_tables(present, B, placed):
    """Knockout section 1.4 from outside presence only: what each block endpoint keeps, the
    inferable block cells, the mirror cells."""
    ex = present & ~B
    ix = {n: i for i, n in enumerate(placed)}
    keep = {s: int(ex[ix[s], :].sum()) for s in SOURCES}       # training targets
    keep.update({t: int(ex[:, ix[t]].sum()) for t in TARGETS})  # training sources
    inferable = sum(1 for s, t in BLOCK_NAMES
                    if keep[s] >= INFERABLE_MIN and keep[t] >= INFERABLE_MIN)
    mirrors = sum(1 for s, t in BLOCK_NAMES if ex[ix[t], ix[s]])
    smallest = min(keep, key=lambda n: (keep[n], n))
    return {"inferable": inferable, "mirrors": mirrors,
            "smallest_endpoint_keep": [smallest, keep[smallest]]}


def diagnostics(x_all, omega, B, placed, targets, K_reg, R):
    """Section 5.4, after c* is fixed; outside block A only. Density-matched cuts are recomputed
    on each w_min's own x table."""
    n_omega = int(omega.sum())
    K_other = targets["restrict"]["K"]
    K_full = targets["full_grid_b_prime"]["K"]
    K_lobe = round_half_up(targets[REGISTERED_COLLAPSE]["T_exact"] * n_omega)
    rows = []
    R.say("")
    R.say(f"diagnostics (section 5.4; decide nothing; outside block A only; |Omega| = {n_omega} "
          f"per lobe)")
    for k, wmin in enumerate(DIAG_W_MINS):
        xL, xR = x_all[k, 0][omega], x_all[k, 1][omega]
        pooled = np.concatenate([xL, xR])
        cuts = [("c* (pooled collapse, registered)", choose_cut(pooled, K_reg)["c"]),
                ("c* (restrict-only collapse)", choose_cut(pooled, K_other)["c"]),
                ("c* (b', full-grid density)", choose_cut(pooled, K_full)["c"]),
                ("c*_L (left lobe alone)", choose_cut(xL, K_lobe)["c"]),
                ("c*_R (right lobe alone)", choose_cut(xR, K_lobe)["c"])]
        cuts += [(f"c = {c:g}", c) for c in FIXED_CUTS]
        rank1 = int((pooled >= 1.0).sum())
        R.say(f"  w_min = {wmin}: c = 1 has rank {rank1} of {2 * n_omega} pooled outside values "
              f"(values >= 1)")
        for label, c in cuts:
            for li, L in enumerate(LOBES):
                pres = (x_all[k, li] >= c) & (x_all[k, li] > 0) & omega
                tabs = outside_tables(pres, B, placed)
                n_p = int(pres.sum())
                rows.append({"w_min": wmin, "cut": label, "c": c, "lobe": L, "present": n_p,
                             "density": n_p / n_omega, **tabs})
                R.say(f"    {label:34s} c = {c:.6g}  lobe {L}: present {n_p}, density "
                      f"{n_p / n_omega:.6f}, inferable {tabs['inferable']}/64, mirrors "
                      f"{tabs['mirrors']}, smallest endpoint keep "
                      f"{tabs['smallest_endpoint_keep'][0]} {tabs['smallest_endpoint_keep'][1]}")
        rows.append({"w_min": wmin, "c_equals_1_rank": rank1, "pooled_values": 2 * n_omega})
    return rows


# ------------------------------------------------------------------------------------------
# Outputs (sections 7, 9, 10.1)

def fmt_int(v):
    if not (0 <= v < FIELD_MAX):
        raise Stop("SEALED FIELD TOO WIDE (section 9; no number is given)")
    return f"{int(v):012d}"


def write_sealed(path, lobe_i, sealed, n_tar, placed, c_star):
    """Section 9: all 64 rows, fixed width, at the registered w_min and c*, and one line with
    the cross-lobe weight of the block type pairs (both directions)."""
    ix = {n: i for i, n in enumerate(placed)}
    lines = ["src,tar,W,n_tar,x,present"]
    for s, t in BLOCK_NAMES:
        Wv = int(sealed["Wb"][lobe_i, ix[s], ix[t]])
        n = int(n_tar[lobe_i, ix[t]])
        x = Wv / n
        lines.append(f"{s},{t},{fmt_int(Wv)},{fmt_int(n)},{x:.6e},{int(x >= c_star and x > 0)}")
    lines.append(f"# cross_lobe_block_weight_total={fmt_int(sealed['cross_b'])}")
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_outside_bank(path, lobe_i, present, x1, omega, placed):
    """Section 7 (D8 (i)): one (0, 0) row per present outside cell, n_syn = x, sign +1."""
    lines = ["src,tar,du,dv,n_syn,sign"]
    P = len(placed)
    for a in range(P):
        for b in range(P):
            if omega[a, b] and present[lobe_i, a, b]:
                lines.append(f"{placed[a]},{placed[b]},0,0,{repr(float(x1[lobe_i, a, b]))},1")
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_pair_stats(path, st, x1, present, n_tar, omega, placed):
    lines = ["lobe,src,tar," + ",".join(f"W_wmin{w}" for w in DIAG_W_MINS)
             + ",n_tar,x,present,cross_lobe_W"]
    P = len(placed)
    for li, L in enumerate(LOBES):
        for a in range(P):
            for b in range(P):
                if not omega[a, b]:
                    continue
                Ws = ",".join(str(int(st["W"][k, li, a, b])) for k in range(len(DIAG_W_MINS)))
                lines.append(f"{L},{placed[a]},{placed[b]},{Ws},{int(n_tar[li, b])},"
                             f"{repr(float(x1[li, a, b]))},{int(present[li, a, b])},"
                             f"{int(st['cross'][a, b])}")
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_sha256sums(d):
    d = Path(d)
    lines = [f"{sha256_file(p)} *{p.name}"
             for p in sorted(d.iterdir()) if p.is_file() and p.name != "SHA256SUMS.txt"]
    (d / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def json_safe(x):
    if isinstance(x, dict):
        return {str(k): json_safe(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [json_safe(v) for v in x]
    if isinstance(x, np.ndarray):
        return json_safe(x.tolist())
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if isinstance(x, (int, np.integer)):
        return int(x)
    if isinstance(x, (float, np.floating)):
        return float(x) if np.isfinite(x) else None
    return x


# ------------------------------------------------------------------------------------------
# The run

def run(cfg, mode, allow_dirty=False, out_dir=None, clock=time.perf_counter,
        memory=peak_memory_bytes, stream=None, utc_stamp=None):
    """mode 'inspect' or 'build'. Raises Stop on a registered stop. The clock and the memory
    probe are parameters so that the blindness test can fix them."""
    t0 = clock()
    R = Report(stream)
    R.say(f"male CNS bank builder; registration {REGISTRATION}, revision {REGISTRATION_REVISION}")
    head = git("rev-parse", "HEAD")
    dirty = dirty_listing()
    registered = not dirty
    R.say(f"git head {head}; tree under results/genome/c6/ and docs/plans/: "
          f"{'clean' if not dirty else 'DIRTY'}")
    if mode == "build" and dirty and not allow_dirty:
        raise Stop("REFUSED: uncommitted changes under results/genome/c6/ or docs/plans/ "
                   "(section 10.3); commit first or pass --allow-dirty\n" + dirty)
    if mode == "build" and dirty:
        R.say("NOT THE REGISTERED BUILD (--allow-dirty on a dirty tree)")
    versions = check_versions(R)
    inputs = check_pins(cfg, R)
    header = weight_file_header(cfg, R)

    names, birth, present65 = read_flyvis(cfg)
    mapped, pops = build_map(names, birth, cfg)
    placed = [p["name"] for p in pops]
    R.say(f"map: {len(mapped)} flyvis names mapped, {len(placed)} placed; not placed: "
          f"{[n for n in names if n not in placed]}")
    targets, B = density_targets(present65, names, pops, cfg, R)
    omega = ~B

    cols = read_annotations(cfg, R)
    specials = print_special_strings(cols, cfg, R)
    mp = apply_map(cols, pops, cfg, R)
    summary = {"placed": placed, "targets": targets, "specials": specials,
               "type_table": mp["table"], "header": header, "lines": R.lines}
    if mode == "inspect":
        R.say("--inspect-only: stopping before any weight column is read (section 10.3)")
        return summary

    out = Path(out_dir) if out_dir else cfg.derived / (
        f"male_cns_v1_{utc_stamp or time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}_{head[:12]}")
    if out.exists():
        raise Stop(f"REFUSED: the output folder exists: {out}")
    lk = make_lookup(cols, mp, placed)
    R.say("")
    R.say(f"weight pass: {len(lk['ids'])} placed bodies with a lobe")
    st = stream_weights(cfg, lk, B, memory=memory)
    sealed = st.pop("_sealed")
    R.say(f"  rows read {st['rows_read']} (metadata stop {st['metadata_stop']}); batches "
          f"{st['batches_read']} of {st['num_record_batches']}; autapse rows dropped "
          f"{st['autapse_rows_dropped']}")
    R.say(f"  outside rows kept: same lobe {st['outside_rows_same_lobe']}, across lobes "
          f"{st['outside_rows_across_lobes']}; duplicate outside keys "
          f"{st['duplicate_outside_keys']}; cross-lobe weight of outside type pairs "
          f"{int(st['cross'][omega].sum())}")
    shares = lobe_consistency(st, pops, cfg, R)

    # Sections 5.1-5.2: x, then c*, before any diagnostic.
    n_tar = mp["n_tar"]
    x_all = st["W"] / n_tar[None, :, None, :]
    x1 = x_all[DIAG_W_MINS.index(W_MIN)]
    K = targets[cfg.collapse]["K"]
    cut = choose_cut(np.concatenate([x1[0][omega], x1[1][omega]]), K)
    c_star = cut["c"]
    present = (x1 >= c_star) & (x1 > 0) & omega[None]
    n_omega = int(omega.sum())
    dens = {L: int(present[li].sum()) / n_omega for li, L in enumerate(LOBES)}
    R.say("")
    R.say(f"the cut (section 5.2, D1 (b), D15 {cfg.collapse}): K = {K}; w_min = {W_MIN}; "
          f"c* = {c_star!r}; pooled present {cut['present']}; tie excess {cut['excess']}; "
          f"shortfall {cut['shortfall']}{' (density below target)' if cut['shortfall'] else ''}")
    for li, L in enumerate(LOBES):
        R.say(f"  lobe {L}: present outside cells {int(present[li].sum())} of {n_omega}, "
              f"density {dens[L]:.6f}")
    diag = diagnostics(x_all, omega, B, placed, targets, K, R)

    out.mkdir(parents=True)
    for li, L in enumerate(LOBES):
        write_sealed(out / f"male_cns_{L}_blockA.sealed.csv", li, sealed, n_tar, placed, c_star)
    del sealed
    for li, L in enumerate(LOBES):
        write_outside_bank(out / f"male_cns_{L}_outside.csv", li, present, x1, omega, placed)
    write_pair_stats(out / "pair_stats_outside.csv", st, x1, present, n_tar, omega, placed)
    files = {}
    for name in [f"male_cns_{L}_outside.csv" for L in LOBES] + ["pair_stats_outside.csv"]:
        files[name] = {"sha256": sha256_file(out / name), "size_bytes": (out / name).stat().st_size}
    for L in LOBES:                                  # section 9: sha256 only, never the size
        files[f"male_cns_{L}_blockA.sealed.csv"] = {
            "sha256": sha256_file(out / f"male_cns_{L}_blockA.sealed.csv")}
    runtime = clock() - t0
    peak = max(st["peak_memory_bytes"], memory())
    manifest = {
        "registration": REGISTRATION, "registration_revision": REGISTRATION_REVISION,
        "registration_sha256_lf": sha256_lf(ROOT / REGISTRATION),
        "registered_build": registered,
        "note": None if registered else "NOT THE REGISTERED BUILD",
        "git_head": head, "dirty_listing": dirty.splitlines(),
        "builder_sha256": sha256_file(Path(__file__)),
        "tests_sha256": sha256_file(TEST_FILE) if TEST_FILE.exists() else None,
        "inputs": inputs, "weight_file_header": header,
        "versions": versions, "machine_record": machine_record(),
        "type_map": {"canonical": cfg.canonical,
                     "special": {n: list(v) for n, v in cfg.special.items()},
                     "absent": list(cfg.absent), "placed": placed,
                     "not_placed": [n for n in names if n not in placed],
                     "per_type": mp["table"], "special_strings": specials},
        "flip": sorted(cfg.flip), "lobe_consistency": shares,
        "collapse": cfg.collapse, "density_targets": {
            k: {kk: vv for kk, vv in v.items() if kk != "T_exact"} for k, v in targets.items()},
        "w_min": W_MIN, "K": K, "c_star": c_star, "cut": cut,
        "outside_density": dens,
        "outside_present": {L: int(present[li].sum()) for li, L in enumerate(LOBES)},
        "diagnostics": diag,
        "stream": {k: st[k] for k in ("rows_read", "batches_read", "num_record_batches",
                                      "metadata_stop", "autapse_rows_dropped",
                                      "outside_rows_same_lobe", "outside_rows_across_lobes",
                                      "duplicate_outside_keys")},
        "cross_lobe_weight_outside_pairs": int(st["cross"][omega].sum()),
        "peak_memory_mib": round(peak / 2 ** 20), "runtime_s": round(runtime, 1),
        "out_folder": out.name, "outputs": files,
        "order_of_files": "the sealed files, the outside banks and pair_stats are written "
                          "before this manifest; BUILD.md (the printed report, which ends with "
                          "this manifest's sha256) and SHA256SUMS.txt after it"}
    (out / "bank.meta.json").write_text(json.dumps(json_safe(manifest), indent=1,
                                                   allow_nan=False) + "\n",
                                        encoding="utf-8", newline="\n")
    R.say("")
    R.say(f"peak memory {round(peak / 2 ** 20)} MiB; runtime {round(runtime, 1)} s")
    R.say(f"written to {out}:")
    for n, r in files.items():
        R.say(f"  {n}: sha256 {r['sha256']}" + (f", {r['size_bytes']} bytes"
                                                  if "size_bytes" in r else ""))
    R.say(f"  bank.meta.json: sha256 {sha256_file(out / 'bank.meta.json')}")
    header_md = "" if registered else "**NOT THE REGISTERED BUILD**\n\n"
    (out / "BUILD.md").write_text(header_md + "```\n" + "\n".join(R.lines) + "\n```\n",
                                  encoding="utf-8", newline="\n")
    write_sha256sums(out)
    summary.update({"out": out, "manifest": manifest, "c_star": c_star, "present": present,
                    "x1": x1, "n_tar": n_tar})
    return summary


def run_self_test():
    """Section 10.3: the fixture tests of section 11, without pytest."""
    sys.path.insert(0, str(HERE))
    import test_male_cns_bank_builder as TT
    tests = [(n, f) for n, f in vars(TT).items() if n.startswith("test_") and callable(f)]
    failed = []
    for n, f in tests:
        try:
            f()
            print(f"PASS {n}", flush=True)
        except Exception as e:                         # report every test, then fail
            failed.append(n)
            print(f"FAIL {n}: {type(e).__name__}: {e}", flush=True)
    print(f"self-test: {len(tests) - len(failed)} of {len(tests)} passed", flush=True)
    return 1 if failed else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--self-test", action="store_true")
    g.add_argument("--inspect-only", action="store_true")
    ap.add_argument("--allow-dirty", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        sys.exit(run_self_test())
    try:
        run(Config(), "inspect" if a.inspect_only else "build", allow_dirty=a.allow_dirty)
    except Stop as e:
        print(f"STOP: {e}", flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
