"""Fixture tests of the male CNS bank builder (registration
docs/plans/2026-09-25-male-cns-bank-builder-registration.md, section 11). No male CNS data is
read: every world is a small synthetic feather pair written to a temporary folder. The pinned
flyvis-65 CSVs of the repository are read (test 5 and the map).

Run through the builder (no pytest needed), in the environment of section 10.4:
    python results/genome/c6/checks/male_cns_bank_builder.py --self-test
or with pytest: python -m pytest -p no:cacheprovider results/genome/c6/checks/test_male_cns_bank_builder.py
"""
import contextlib
import hashlib
import io
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.feather as pf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import male_cns_bank_builder as B  # noqa: E402

ANN, WTS = "ann.feather", "weights.feather"
N_PER = {"CT1": 1, "Am1": 1}                           # bodies per lobe; 3 otherwise
R16_PER_LOBE = (5, 4)                                  # R1-R6 bodies, L and R: unequal on purpose
OVERRIDE_TYPE = {"R7": "R7p", "R8": "R8y", "TmY9q": "TmY9b"}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def flyvis():
    cfg = B.Config()
    names, birth, present = B.read_flyvis(cfg)
    _, pops = B.build_map(names, birth, cfg)
    return names, birth, present, pops


def make_world(d, block="board", ct1_opposite=True, drop=None, drop_string=None,
               rename_type=False, two_types=False, stop_delta=0, chunk=97, dup_block=False,
               dup_outside=False):
    """A synthetic male CNS in folder d. Everything but the block rows comes from one random
    stream (seed 1) and is identical across block patterns; the block rows (same count, same
    weights) come from their own stream and differ only in which body pairs carry them.
    Returns (number of weight rows, the body table, the weight table)."""
    rng = np.random.default_rng(1)
    _, _, _, pops = flyvis()
    bodies, ids = [], {}                               # ids[(pop name, lobe index)] = [bodyId]
    bid = 1000

    def body(**kw):
        nonlocal bid
        bid += 1
        row = {"bodyId": bid, "type": None, "flywireType": None, "somaSide": None,
               "rootSide": None, "instance": None, "status": "Traced", **kw}
        bodies.append(row)
        return bid

    for p in pops:
        col, s = p["column"], p["string"]
        if s == drop_string:
            continue
        for li, L in enumerate(B.LOBES):
            if drop == (p["name"], L):
                continue
            n = R16_PER_LOBE[li] if s == "R1-R6" else N_PER.get(s, 3)
            for j in range(n):
                label = ("R" if L == "L" else "L") if (s == "CT1" and ct1_opposite) else L
                kw = {"status": "Anchor" if j == 1 else "Traced"}
                if col == "type":
                    kw.update(type=s, flywireType={"R1-R6": "R1-6"}.get(s, s))
                else:
                    kw.update(type=OVERRIDE_TYPE[s], flywireType=s)
                if s == "R1-R6" and j == 0:
                    kw.update(rootSide=label)                         # the second step
                elif s == "R1-R6":
                    kw.update(somaSide="M", instance=f"R1-R6_{label}")  # the third step
                else:
                    kw.update(somaSide=label, instance=f"{kw['type']}_{label}")
                ids.setdefault((p["name"], li), []).append(body(**kw))
    unassigned = [body(type="Mi1", flywireType="Mi1", rootSide="unknown", instance="Mi1_l"),
                  body(type="Mi1", flywireType="Mi1", instance="Mi1_L_1")]
    other = [body(type="DNp01", flywireType="DNp01", somaSide="L", instance="DNp01_L")
             for _ in range(4)]
    if two_types:
        body(type="Mi1", flywireType="R7", somaSide="L")

    placed = [p["name"] for p in pops]
    Bm = B.block_mask(placed)
    rows, keys = [], set()

    def edge(pre, post, w):
        if pre != post and (pre, post) not in keys:
            keys.add((pre, post))
            rows.append((pre, post, int(w)))

    P = len(placed)
    for li in (0, 1):
        for a in range(P):
            for b in range(P):
                if Bm[a, b]:
                    continue
                pa_, pb_ = ids.get((placed[a], li)), ids.get((placed[b], li))
                if rng.random() < 0.25 and pa_ and pb_:
                    for _ in range(int(rng.integers(1, 4))):
                        edge(int(rng.choice(pa_)), int(rng.choice(pb_)), rng.integers(1, 6))
                qb = ids.get((placed[b], 1 - li))
                if rng.random() < 0.02 and pa_ and qb:
                    edge(int(rng.choice(pa_)), int(rng.choice(qb)), rng.integers(1, 3))
    mi1 = ids.get(("Mi1", 0)) or ids[("Mi1", 1)]
    for i in mi1[:3]:
        rows.append((i, i, 7))                        # autapses, dropped
    for o in other:
        for i in mi1[:2]:
            edge(o, i, 4)
            edge(i, o, 2)                             # an unplaced partner, dropped
    t4a = ids[("T4a", 0)]
    for u in unassigned:
        edge(u, t4a[0], 5)                            # an unassigned end, dropped
    if dup_outside:
        rows.append(rows[0])
    n_fixed = len(rows)

    # block rows: the only part that depends on `block`
    rb = np.random.default_rng({"board": 11, "random": 12}[block])
    board = [(s, t) for s in B.ON for t in B.T4] + [(s, t) for s in B.OFF for t in B.T5]
    wts = [3, 4, 5, 6, 7, 8]
    blk_rows, bkeys = [], set()
    k = 0
    complete = [li for li in (0, 1) if all((n, li) in ids for n in B.SOURCES + B.TARGETS)]
    for li in complete:
        for cell in board:
            for _ in range(2):
                s, t = cell if block == "board" else B.BLOCK_NAMES[int(rb.integers(64))]
                while True:
                    pre = int(rb.choice(ids[(s, li)]))
                    post = int(rb.choice(ids[(t, li)]))
                    if (pre, post) not in bkeys:
                        break
                    s, t = cell if block == "board" else B.BLOCK_NAMES[int(rb.integers(64))]
                bkeys.add((pre, post))
                blk_rows.append((pre, post, wts[k % len(wts)]))
                k += 1
    for j in range(4 if complete == [0, 1] else 0):   # across lobes: sealed total only
        s, t = ("Mi1", "T4a") if block == "board" else B.BLOCK_NAMES[int(rb.integers(64))]
        pre, post = ids[(s, 0)][j % len(ids[(s, 0)])], ids[(t, 1)][j % len(ids[(t, 1)])]
        if (pre, post) in bkeys:
            post = ids[(t, 1)][(j + 1) % len(ids[(t, 1)])]
        bkeys.add((pre, post))
        blk_rows.append((pre, post, 2))
    if dup_block:
        blk_rows.append(blk_rows[0])
    allrows = rows + blk_rows
    order = np.random.default_rng(5).permutation(len(allrows))
    assert len(allrows) == n_fixed + len(blk_rows)
    arr = np.array([allrows[i] for i in order], dtype=np.int64)
    ann = pd.DataFrame(bodies)
    if rename_type:
        ann = ann.rename(columns={"type": "type_renamed"})
    pf.write_feather(pa.Table.from_pandas(ann, preserve_index=False), d / ANN,
                     compression="uncompressed")
    w = pd.DataFrame({"body_pre": arr[:, 0], "body_post": arr[:, 1], "weight": arr[:, 2]})
    tab = pa.Table.from_pandas(w)
    md = json.loads(tab.schema.metadata[b"pandas"])
    assert md["index_columns"][0]["stop"] == len(w)
    if stop_delta:
        md["index_columns"][0]["stop"] += stop_delta
        tab = tab.replace_schema_metadata({b"pandas": json.dumps(md).encode()})
    pf.write_feather(tab, d / WTS, compression="uncompressed", chunksize=chunk)
    return len(w) + stop_delta, ann, w


def cfg_for(d, n_rows, **kw):
    pins = {f: ((d / f).stat().st_size, sha(d / f)) for f in (ANN, WTS)}
    return B.Config(data_dir=d, annotations=ANN, weights=WTS, janelia_pins=pins,
                    weight_rows=n_rows, derived=d / "derived", **kw)


def run_world(cfg, mode="build", out=None):
    buf = io.StringIO()
    s = B.run(cfg, mode, allow_dirty=True, out_dir=out, clock=lambda: 0.0, memory=lambda: 0,
              stream=buf)
    return s, buf.getvalue()


def expect_stop(fn, phrase):
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            fn()
    except B.Stop as e:
        assert phrase in str(e), f"stopped with {e!s}, expected {phrase}"
        return str(e)
    raise AssertionError(f"no stop; expected {phrase}")


def world(tmp, **kw):
    d = Path(tmp)
    d.mkdir(parents=True, exist_ok=True)
    n, ann, w = make_world(d, **kw)
    return d, n, ann, w


# ------------------------------------------------------------------------------------------
# 1. Blindness (section 9)

SEALED = [f"male_cns_{L}_blockA.sealed.csv" for L in B.LOBES]
PLAIN = [f"male_cns_{L}_outside.csv" for L in B.LOBES] + ["pair_stats_outside.csv"]


def build_both_worlds(tmp):
    """Each world is built in the same folder (so every printed path is equal), then read."""
    work, res = Path(tmp) / "work", {}
    for blk in ("board", "random"):
        if work.exists():
            shutil.rmtree(work)
        work.mkdir()
        n, _, _ = make_world(work, block=blk)
        _, out = run_world(cfg_for(work, n), out=work / "out")
        res[blk] = {"stdout": out, "wsha": sha(work / WTS), "wsize": (work / WTS).stat().st_size,
                    "files": {p.name: p.read_bytes() for p in (work / "out").iterdir()}}
    return res["board"], res["random"]


def world_differences(A, Bw):
    """Every difference between the two worlds' prints and outputs other than the sealed files'
    bytes and the hashes that necessarily differ: the weight file's (its block rows differ), the
    sealed files', and the two files that print those hashes (the manifest, BUILD.md)."""
    diffs = []
    if A["wsize"] != Bw["wsize"]:
        diffs.append("weight file sizes differ")
    for f in SEALED:
        if A["files"][f] == Bw["files"][f]:
            diffs.append(f"{f}: identical (the worlds do not differ in the block)")
        if len(A["files"][f]) != len(Bw["files"][f]):
            diffs.append(f"{f}: sizes differ")
    for f in PLAIN:
        if A["files"][f] != Bw["files"][f]:
            diffs.append(f"{f}: bytes differ")
    if set(A["files"]) != set(Bw["files"]):
        diffs.append("file sets differ")

    def tokens(r):
        t = {r["wsha"]: "<WEIGHTS>"}
        for f in SEALED:
            t[hashlib.sha256(r["files"][f]).hexdigest()] = f"<{f}>"
        t[hashlib.sha256(r["files"]["bank.meta.json"]).hexdigest()] = "<MANIFEST>"
        return t

    def norm(text, r, extra=()):
        for k, v in list(tokens(r).items()) + list(extra):
            text = text.replace(k, v)
        return text

    for key, ta, tb in [("stdout", A["stdout"], Bw["stdout"]),
                        ("bank.meta.json", A["files"]["bank.meta.json"].decode(),
                         Bw["files"]["bank.meta.json"].decode()),
                        ("BUILD.md", A["files"]["BUILD.md"].decode(),
                         Bw["files"]["BUILD.md"].decode())]:
        if norm(ta, A) != norm(tb, Bw):
            diffs.append(f"{key}: differs beyond the named hashes")
    bm = [(hashlib.sha256(r["files"]["BUILD.md"]).hexdigest(), "<BUILD>") for r in (A, Bw)]
    if norm(A["files"]["SHA256SUMS.txt"].decode(), A, [bm[0]]) != \
            norm(Bw["files"]["SHA256SUMS.txt"].decode(), Bw, [bm[1]]):
        diffs.append("SHA256SUMS.txt: differs beyond the named hashes")
    for r in (A, Bw):
        man = json.loads(r["files"]["bank.meta.json"])
        for f in SEALED:
            if set(man["outputs"][f]) != {"sha256"}:
                diffs.append(f"manifest records more than the sha256 of {f}")
    return diffs


def test_blindness():
    with tempfile.TemporaryDirectory() as tmp:
        A, Bw = build_both_worlds(tmp)
        assert A["wsha"] != Bw["wsha"]
        assert world_differences(A, Bw) == []


def test_blindness_test_catches_a_leak():
    """Positive control: one number computed from the block rows (the count of non-empty block
    cells), written into pair_stats_outside.csv, must make the comparison fail."""
    orig_sealed, orig_stats, leak = B.write_sealed, B.write_pair_stats, []

    def leaky_sealed(path, lobe_i, sealed, *a):
        leak.append(int((sealed["Wb"] > 0).sum()))
        return orig_sealed(path, lobe_i, sealed, *a)

    def leaky_stats(path, *a):
        orig_stats(path, *a)
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(f"# {leak[-1]}\n")
    B.write_sealed, B.write_pair_stats = leaky_sealed, leaky_stats
    try:
        with tempfile.TemporaryDirectory() as tmp:
            A, Bw = build_both_worlds(tmp)
    finally:
        B.write_sealed, B.write_pair_stats = orig_sealed, orig_stats
    assert "pair_stats_outside.csv: bytes differ" in world_differences(A, Bw)


# ------------------------------------------------------------------------------------------
# 1a. The suffix parser and the side rule (section 4)

def test_suffix_parser():
    cases = {"X_L": "L", "X_R": "R", "DNp01(GF)_R": "R", "X_L_1": None, "X(L)": None,
             "X_l": None, "_L": None, "_R": None, None: None, "X_L ": None, "x_r": None}
    for s, want in cases.items():
        assert B.suffix_side(s) == want, (s, B.suffix_side(s), want)
    side, step = B.side_rule(np.array(["L", "M", None, None, None], object),
                             np.array(["R", "R", "unknown", None, None], object),
                             np.array([None, "Y_L", "Y_L", "Y_R", "Y_L_1"], object))
    assert list(side) == ["L", "R", "L", "R", None]
    assert list(step) == ["somaSide", "rootSide", "instance", "instance", "unassigned"]


# ------------------------------------------------------------------------------------------
# 2. The flip (section 4)

def test_flip():
    with tempfile.TemporaryDirectory() as tmp:
        d, n, _, _ = world(Path(tmp) / "a", ct1_opposite=True)
        s, _ = run_world(cfg_for(d, n), out=d / "out")         # passes with FLIP = {CT1}
        assert s["manifest"]["lobe_consistency"]["CT1(M10)"]["share"] >= 0.5
        expect_stop(lambda: run_world(cfg_for(d, n, flip=frozenset()), out=d / "out2"),
                    "LOBE ASSIGNMENT INCONSISTENT")
        d, n, _, _ = world(Path(tmp) / "b", ct1_opposite=False)
        msg = expect_stop(lambda: run_world(cfg_for(d, n), out=d / "out"),
                          "LOBE ASSIGNMENT INCONSISTENT")
        assert "CT1(M10)" in msg


# ------------------------------------------------------------------------------------------
# 3. The map's self-test (section 3.3)

def test_zero_name_matches():
    with tempfile.TemporaryDirectory() as tmp:
        d, n, _, _ = world(tmp, rename_type=True)
        expect_stop(lambda: run_world(cfg_for(d, n), "inspect"), "ZERO NAME MATCHES")


def test_type_with_no_cells():
    with tempfile.TemporaryDirectory() as tmp:
        d, n, _, _ = world(tmp, drop=("Mi1", "L"))
        msg = expect_stop(lambda: run_world(cfg_for(d, n), "inspect"), "TYPE WITH NO CELLS")
        assert "('Mi1', 'L')" in msg


def test_map_string_not_found():
    with tempfile.TemporaryDirectory() as tmp:
        d, n, _, _ = world(tmp, drop_string="Am1")
        msg = expect_stop(lambda: run_world(cfg_for(d, n), "inspect"), "MAP STRING NOT FOUND")
        assert "Am1" in msg


def test_body_in_two_types():
    with tempfile.TemporaryDirectory() as tmp:
        d, n, _, _ = world(tmp, two_types=True)
        expect_stop(lambda: run_world(cfg_for(d, n), "inspect"), "BODY IN TWO TYPES")


def test_inspect_passes_and_reads_no_weight():
    with tempfile.TemporaryDirectory() as tmp:
        d, n, _, _ = world(tmp)
        orig = B.stream_weights
        B.stream_weights = lambda *a, **k: (_ for _ in ()).throw(AssertionError("weights read"))
        try:
            s, out = run_world(cfg_for(d, n), "inspect")
        finally:
            B.stream_weights = orig
        assert "all pass" in out and "--inspect-only: stopping" in out
        assert len(s["placed"]) == 55


# ------------------------------------------------------------------------------------------
# 4. Chunked equals whole (section 6.5)

def whole_table(d, cfg):
    """An independent whole-table path: pandas reads everything, maps both ends, groups."""
    R = B.Report(io.StringIO())
    names, birth, _ = B.read_flyvis(cfg)
    _, pops = B.build_map(names, birth, cfg)
    placed = [p["name"] for p in pops]
    cols = B.read_annotations(cfg, R)
    mp = B.apply_map(cols, pops, cfg, R)
    ok = (mp["pop_of"] >= 0) & (mp["lobe"] >= 0)
    typ = dict(zip(cols["bodyId"][ok].tolist(), mp["pop_of"][ok].tolist()))
    lob = dict(zip(cols["bodyId"][ok].tolist(), mp["lobe"][ok].tolist()))
    df = pd.read_feather(d / WTS)
    df = df[df.body_pre.isin(typ) & df.body_post.isin(typ) & (df.body_pre != df.body_post)]
    df = df.assign(s=df.body_pre.map(typ), t=df.body_post.map(typ), la=df.body_pre.map(lob),
                   lc=df.body_post.map(lob))
    Bm = B.block_mask(placed)
    df = df.assign(blk=Bm[df.s.to_numpy(), df.t.to_numpy()])
    P = len(placed)
    W = np.zeros((3, 2, P, P), np.int64)
    same = df[(df.la == df.lc) & ~df.blk]
    for k, wmin in enumerate(B.DIAG_W_MINS):
        g = same[same.weight >= wmin].groupby(["la", "s", "t"]).weight.sum()
        for (la, s, t), v in g.items():
            W[k, la, s, t] = v
    cross = np.zeros((P, P), np.int64)
    for (s, t), v in df[(df.la != df.lc) & ~df.blk].groupby(["s", "t"]).weight.sum().items():
        cross[s, t] = v
    Wb = np.zeros((2, P, P), np.int64)
    for (la, s, t), v in df[(df.la == df.lc) & df.blk].groupby(["la", "s", "t"]).weight.sum().items():
        Wb[la, s, t] = v
    return W, cross, Wb, (cols, mp, placed, Bm)


def test_chunked_equals_whole():
    with tempfile.TemporaryDirectory() as tmp:
        for chunk in (7, 97, 1_000_000):
            d, n, _, _ = world(Path(tmp) / str(chunk), chunk=chunk)
            cfg = cfg_for(d, n)
            W, cross, Wb, (cols, mp, placed, Bm) = whole_table(d, cfg)
            st = B.stream_weights(cfg, B.make_lookup(cols, mp, placed), Bm, memory=lambda: 0)
            assert np.array_equal(st["W"], W) and np.array_equal(st["cross"], cross)
            assert np.array_equal(st["_sealed"]["Wb"], Wb)
            assert W[0].sum() > 0 and cross.sum() > 0
            assert st["autapse_rows_dropped"] == 3 and st["duplicate_outside_keys"] == 0


def test_duplicates():
    with tempfile.TemporaryDirectory() as tmp:
        d, n, _, _ = world(Path(tmp) / "o", dup_outside=True)
        s, _ = run_world(cfg_for(d, n), out=d / "out")
        assert s["manifest"]["stream"]["duplicate_outside_keys"] == 1
        d, n, _, _ = world(Path(tmp) / "b", dup_block=True)
        msg = expect_stop(lambda: run_world(cfg_for(d, n), out=d / "out"),
                          "DUPLICATE KEY AMONG BLOCK ROWS")
        assert not any(ch.isdigit() for ch in msg.split("(")[0])


# ------------------------------------------------------------------------------------------
# 5. The density rule (section 5.2) and the targets (section 5.3)

def test_density_rule():
    v = [5, 4, 4, 4, 3, 0, 0]
    assert B.choose_cut(v, 1) == {"c": 5.0, "present": 1, "excess": 0, "shortfall": 0}
    assert B.choose_cut(v, 2) == {"c": 4.0, "present": 4, "excess": 2, "shortfall": 0}
    assert B.choose_cut(v, 5) == {"c": 3.0, "present": 5, "excess": 0, "shortfall": 0}
    assert B.choose_cut(v, 6) == {"c": 3.0, "present": 5, "excess": 0, "shortfall": 1}
    assert B.choose_cut([0, 0], 1)["shortfall"] == 1


def test_density_targets_registered_and_moved():
    names, birth, present, pops = flyvis()
    R = B.Report(io.StringIO())
    out, _ = B.density_targets(present, names, pops, B.Config(), R)
    assert {k: out["pooled"][k] for k in ("omega", "present", "T", "K")} == \
        {"omega": 2961, "present": 511, "T": 0.172577, "K": 1022}
    assert {k: out["restrict"][k] for k in ("omega", "present", "T", "K")} == \
        {"omega": 2961, "present": 497, "T": 0.167849, "K": 994}
    assert {k: out["full_grid_b_prime"][k] for k in ("omega_full", "present_full", "T", "K")} \
        == {"omega_full": 4161, "present_full": 572, "T": 0.137467, "K": 814}
    cfg2 = B.Config(absent=B.ABSENT + ("TmY9",))                # a changed map: 54 types
    _, pops2 = B.build_map(names, birth, cfg2)
    expect_stop(lambda: B.density_targets(present, names, pops2, cfg2, R),
                "DENSITY TARGET DIFFERS")
    cfg3 = B.Config(absent=B.ABSENT + ("TmY9",), registered_targets={"pooled": {}})
    moved, _ = B.density_targets(present, names, pops2, cfg3, R)
    assert (moved["pooled"]["omega"], moved["pooled"]["K"]) != (2961, 1022)


def test_density_target_differs_stops_the_run():
    with tempfile.TemporaryDirectory() as tmp:
        d, n, _, _ = world(tmp)
        expect_stop(lambda: run_world(cfg_for(d, n, absent=B.ABSENT + ("TmY9",)), "inspect"),
                    "DENSITY TARGET DIFFERS")


# ------------------------------------------------------------------------------------------
# 6. Row count; pins; an existing output folder

def test_row_count_differs():
    with tempfile.TemporaryDirectory() as tmp:
        d, n, _, _ = world(Path(tmp) / "a", stop_delta=1)      # metadata stop = rows + 1
        expect_stop(lambda: run_world(cfg_for(d, n), out=d / "out"), "ROW COUNT DIFFERS")
        d, n, _, _ = world(Path(tmp) / "b")
        expect_stop(lambda: run_world(cfg_for(d, n + 5), "inspect"), "ROW COUNT DIFFERS")


def test_pins_and_output_folder():
    with tempfile.TemporaryDirectory() as tmp:
        d, n, _, _ = world(tmp)
        cfg = cfg_for(d, n)
        cfg.janelia_pins[WTS] = (cfg.janelia_pins[WTS][0], "0" * 64)
        expect_stop(lambda: run_world(cfg, "inspect"), "PINS DIFFER")
        (d / "out").mkdir()
        expect_stop(lambda: run_world(cfg_for(d, n), out=d / "out"), "output folder exists")


# ------------------------------------------------------------------------------------------
# 7. One index per population

def test_one_index_per_population():
    with tempfile.TemporaryDirectory() as tmp:
        d, n, ann, w = world(tmp)
        s, _ = run_world(cfg_for(d, n), out=d / "out")
        unplaced = {"R2", "R3", "R4", "R5", "R6", "CT1(Lo1)", "Mi3", "Mi11", "Mi12", "Tm28"}
        for f in PLAIN:
            names = set()
            for line in (d / "out" / f).read_text(encoding="utf-8").splitlines()[1:]:
                names.update(line.split(",")[:3])
            assert not names & unplaced, (f, names & unplaced)
        stats = pd.read_csv(d / "out" / "pair_stats_outside.csv")
        for li, L in enumerate(B.LOBES):
            assert set(stats[(stats.lobe == L) & (stats.tar == "R1")].n_tar) == {R16_PER_LOBE[li]}
            assert set(stats[(stats.lobe == L) & (stats.tar == "CT1(M10)")].n_tar) == {1}
        r16 = set(ann[ann["type"] == "R1-R6"].bodyId)
        side, _ = B.side_rule(*(ann[c].to_numpy(object) for c in B.SIDE_COLUMNS))
        lobe = dict(zip(ann.bodyId, side))
        mine = w[w.body_pre.isin(r16) & w.body_post.isin(r16) & (w.body_pre != w.body_post)]
        mine = mine[[lobe[a] == lobe[b] for a, b in zip(mine.body_pre, mine.body_post)]]
        got = stats[(stats.src == "R1") & (stats.tar == "R1")].W_wmin1.sum()
        assert got == mine.weight.sum()
        assert s["placed"].count("R1") == 1 and "CT1(M10)" in s["placed"]
