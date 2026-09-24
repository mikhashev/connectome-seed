#!/usr/bin/env python3
"""The column test: a lower bound on how much agreement our processing produces.

Implements docs/plans/2026-09-24-column-test-registration.md, revision 2.3; section numbers below
refer to it, and main() follows its section 7 order.

Environment. The full run reads proofread_connections_783.feather and needs pyarrow, which must
NOT go into tools/.venv (digest pinned by night 6 gate 8). numpy and pandas are pinned to
tools/.venv's versions so the seeded worlds match a --synthetic-only run there:

    uv run --no-project --with pyarrow --with numpy==2.2.6 --with pandas==2.3.3 python \
        results/genome/c6/checks/flywire_column_test.py

--synthetic-only reads only the bank-level sets B and F and needs no pyarrow:

    tools/.venv/Scripts/python.exe results/genome/c6/checks/flywire_column_test.py --synthetic-only

Licence (section 1): anything keyed by column goes to connectome-seed-data/FlyWire/derived/
column_test/; the committed flywire_column_test/ gets aggregates only.
"""
import argparse
import csv
import gzip
import hashlib
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
C6 = HERE.parent
ROOT = C6.parents[2]                                   # the repository root
REGISTRATION = "docs/plans/2026-09-24-column-test-registration.md"
REGISTRATION_REVISION = "2.3"
DATA_ROOT = ROOT.parent / "connectome-seed-data" / "FlyWire"
DERIVED = DATA_ROOT / "derived"
PRIVATE_OUT = DERIVED / "column_test"                 # section 1: not for the repository
OUT = HERE / "flywire_column_test"                    # section 7: committed, aggregates only
BUILDER = HERE / "flywire_bank_builder.py"


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# Section 2.1: the builder's sha256 is read before its constants are imported, and checked in
# step 2 (refuse_if_inputs_differ).
BUILDER_SHA_READ = sha256_file(BUILDER)
sys.path.insert(0, str(HERE))
from flywire_bank_builder import (FLYWIRE_NAME_OF, SYNAPSE_THRESHOLD, MEAN_PRUNE_BELOW,  # noqa: E402
                                  HEX_NEIGHBOURS, COLUMN_ASSIGNMENT_DOWNLOAD_DATE)
from flywire_sensitivity import read_flyvis30  # noqa: E402  (section 1: the same 228-pair cut)

# Section 2.1, 1, 3.6: registered identities of the inputs.
EXPECTED_BUILDER_SHA = "b109fd17d0d1cf88ddb94343f2b6234c68eeb7eeccab3a6d58af4ce3c20b0750"
EXPECTED_OFFSETS_SHA = "25c5ff1d8ac9dc29e663d1383754c48ef23efae12b65714c66103cd4384d42eb"
EXPECTED_COLUMN_FILE_SHA_HEAD, EXPECTED_COLUMN_FILE_SHA_TAIL = "bdf4ce7f", "f0f6"
EXPECTED_COLUMN_FILE_SIZE = 462838
BANK_META = DERIVED / "bank.meta.json"
BANK_OFFSETS = DERIVED / "flywire_ol_right_30_offsets.csv"
BANK_ROWS = 393

TYPES = sorted(FLYWIRE_NAME_OF)                        # 30 types; cell = 30 * i(s) + i(t)
TI = {t: i for i, t in enumerate(TYPES)}
NT = len(TYPES)
NCELL = NT * NT                                        # section 3: the 900-pair universe
N_COLUMNS = 796                                        # section 2.2

# Section 3.1: reference counts, asserted against B and F as read.
REF_B, REF_F, REF_BF = 165, 228, 159
MACHINE_TOL = 1e-12                                    # sections 3.2, 3.6

# Section 3.2: the curve.
K_GRID = (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 796)
N_SAMPLES = 50
PERCENTILES = (5, 25, 50, 75, 95)                      # numpy.percentile, linear interpolation


def curve_seed(k, j):
    return 1000 * k + j


# Section 2.3: inclusion stop rule. Section 3.5: S4 seeds.
MIN_INCLUDED = 100
S4_SEEDS = tuple(range(20))

# Section 3.8: synthetic worlds. Rates as fractions.
THIN_P = (0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.10)
UNIFORM_R = (0.05, 0.10, 0.20, 0.40)                   # calibration, seeds 250 + 10 i + j
UNIFORM_VAL = ((305, 0.05), (310, 0.10), (320, 0.20), (330, 0.30), (340, 0.40))
INF_QF = (0.05, 0.10, 0.20, 0.30, 0.40)                # calibration, seeds 400 + 10 i + j
INF_VAL = ((530, 0.30), (540, 0.40))
N_THIN_CAL_REPEATS = 5                                 # seeds 150 + 10 i + j, j = 0-4
N_EXTRAS_CAL_REPEATS = 5                               # revision 2.3: a point is a median of 5
N_WORLDS = (len(THIN_P) * (1 + N_THIN_CAL_REPEATS)                        # 48
            + len(UNIFORM_R) * N_EXTRAS_CAL_REPEATS + len(UNIFORM_VAL)    # 20 + 5
            + len(INF_QF) * N_EXTRAS_CAL_REPEATS + len(INF_VAL))          # 25 + 2
assert N_WORLDS == 100


def thin_val_seed(i):
    return 100 + i


def thin_cal_seed(i, j):
    return 150 + 10 * i + j


def uniform_cal_seed(i, j):
    return 250 + 10 * i + j


def inf_cal_seed(i, j):
    return 400 + 10 * i + j


# Section 4: the cuts on k*. Section 3.7: the Q3/P95 secondary label.
K_STAR_A, K_STAR_B = 0.05, 0.20
Q3_SHARE, P95_SHARE = 0.25, 0.05
Q3P95_NOTE = "secondary, non-monotonic in the thinning rate (§3.7); decides nothing"

K_STAR_OBS_EPS = 1e-12                                 # section 4: R_in − X "zero to rounding"
K_STAR_F_NOTE = " (read only under (c))"               # sections 3.8, 4
B_LABEL_NOTE = ("the label rests on the definition of the threshold (the uniform-extras "
                "calibration), not on a measured boundary (section 3.8)")
PLOT_CAPTION = ("synthetic curves average with denominator k, the real curve with n_K(t); "
                "intermediate k are not directly comparable; Δ uses only k = 1 and k = 796")

LABEL_TEXT = {"(a)": "(a) averaging adds little", "(b)": "(b) averaging manufactures agreement",
              "(c)": "(c) averaging removes agreement", "unclear": "unclear"}


def log(m=""):
    print(m, flush=True)


def json_safe(x):
    """Section 7: summary.json must be valid JSON; NaN and infinities become null."""
    if isinstance(x, dict):
        return {k: json_safe(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [json_safe(v) for v in x]
    if isinstance(x, (float, np.floating)):
        return float(x) if np.isfinite(x) else None
    return x


def dump_json(obj):
    return json.dumps(json_safe(obj), indent=2, allow_nan=False)


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                          check=True).stdout.strip()


# ------------------------------------------------------------------------------------------
# Section 7 steps 1 and 2: refusals and input identities.

def refuse_if_unsafe(allow_dirty):
    """Step 1: refuse on a dirty tree or a missing data root."""
    if not allow_dirty:
        d = git("status", "--porcelain")
        if d:
            sys.exit(f"REFUSED: uncommitted changes; commit {REGISTRATION} and this script "
                     "first.\n" + d)
    if not DATA_ROOT.exists():
        sys.exit(f"REFUSED: data root not found: {DATA_ROOT}")


def refuse_if_inputs_differ(need_column_file):
    """Step 2: the builder's sha256 (section 2.1), the column file's sha256 and size (section 1),
    the bank offsets file's sha256 (section 3.6)."""
    meta = json.loads(BANK_META.read_text(encoding="utf-8"))
    if BUILDER_SHA_READ != EXPECTED_BUILDER_SHA or meta["builder_sha256"] != EXPECTED_BUILDER_SHA:
        sys.exit(f"REFUSED: builder sha256 {BUILDER_SHA_READ}, bank.meta.json records "
                 f"{meta['builder_sha256']}, registered {EXPECTED_BUILDER_SHA}")
    offsets_sha = sha256_file(BANK_OFFSETS)
    if offsets_sha != EXPECTED_OFFSETS_SHA or meta["offsets_sha256"] != EXPECTED_OFFSETS_SHA:
        sys.exit(f"REFUSED: bank offsets sha256 {offsets_sha}, registered {EXPECTED_OFFSETS_SHA}")
    inputs = {"builder": {"sha256": BUILDER_SHA_READ},
              "bank_offsets": {"file": BANK_OFFSETS.name, "sha256": offsets_sha,
                               "size_bytes": BANK_OFFSETS.stat().st_size},
              "bank_meta": {"sha256": sha256_file(BANK_META),
                            "size_bytes": BANK_META.stat().st_size},
              "flyvis_offsets_csv": {"sha256": sha256_file(ROOT / "results/genome/bank/offsets.csv")},
              "registration": {"file": REGISTRATION, "sha256": sha256_file(ROOT / REGISTRATION)}}
    if need_column_file:
        p = DATA_ROOT / "column_assignment.csv.gz"
        sha, size = sha256_file(p), p.stat().st_size
        rec = meta["inputs"]["column_assignment"]
        if (sha != rec["sha256"] or size != rec["size_bytes"] or size != EXPECTED_COLUMN_FILE_SIZE
                or not sha.startswith(EXPECTED_COLUMN_FILE_SHA_HEAD)
                or not sha.endswith(EXPECTED_COLUMN_FILE_SHA_TAIL)):
            sys.exit(f"REFUSED: column_assignment.csv.gz sha256 {sha}, size {size}; registered "
                     f"{EXPECTED_COLUMN_FILE_SHA_HEAD}...{EXPECTED_COLUMN_FILE_SHA_TAIL}, "
                     f"{EXPECTED_COLUMN_FILE_SIZE} bytes")
        inputs["column_assignment"] = {"file": p.name, "sha256": sha, "size_bytes": size,
                                       "downloaded": COLUMN_ASSIGNMENT_DOWNLOAD_DATE}
        f = DATA_ROOT / "proofread_connections_783.feather"
        fsha = sha256_file(f)
        inputs["proofread_connections_783.feather"] = {
            "sha256": fsha, "size_bytes": f.stat().st_size,
            "equals_bank_meta": fsha == meta["inputs"]["proofread_connections_783.feather"]["sha256"]}
    return meta, inputs


def read_bank_rows():
    """The registered bank's offset rows (section 3.6)."""
    with open(BANK_OFFSETS, newline="", encoding="utf-8") as fh:
        return {(r["src"], r["tar"], int(r["du"]), int(r["dv"])): float(r["n_syn"])
                for r in csv.DictReader(fh)}


def cell(s, t):
    return TI[s] * NT + TI[t]


def mask_of(pairs):
    m = np.zeros(NCELL, dtype=bool)
    for s, t in pairs:
        m[cell(s, t)] = True
    return m


def read_B_and_F():
    """Section 3: B = the registered FlyWire-30 bank, F = flyvis-30; stops unless their counts
    are the registered ones (section 3.1)."""
    bank_rows = read_bank_rows()
    B = mask_of({(s, t) for s, t, _, _ in bank_rows})
    F = mask_of({(s, t) for s, t, _, _ in read_flyvis30()})
    nB, nF, nBF = int(B.sum()), int(F.sum()), int((B & F).sum())
    if (nB, nF, nBF, len(bank_rows)) != (REF_B, REF_F, REF_BF, BANK_ROWS):
        sys.exit(f"REFUSED: |B|, |F|, |B∩F|, bank rows = {nB}, {nF}, {nBF}, {len(bank_rows)}; "
                 f"registered {REF_B}, {REF_F}, {REF_BF}, {BANK_ROWS} (sections 3.1, 3.6)")
    return bank_rows, B, F


def reference_numbers(B, F):
    """Section 3.1, printed verbatim under their names."""
    nB, nF, nBF = int(B.sum()), int(F.sum()), int((B & F).sum())
    nU = int((B | F).sum())
    return {"R_in": {"value": nBF / nB, "as_registered": "159/165 = 0.9636 (the 96.4 %)"},
            "R_cov": {"value": nBF / nF, "as_registered": "159/228 = 0.6974"},
            "R_jac": {"value": nBF / nU, "as_registered": "159/234 = 0.6795"},
            "chance": {"value": nF / NCELL, "as_registered": "228/900 = 0.2533"}}


# ------------------------------------------------------------------------------------------
# Shared arithmetic.

def containment(A, F):
    """Section 3: C(A) = |A ∩ F| / |A| per row of A (rows x 900). Returns sizes, intersections
    and C, NaN where A is empty (left out of every quantile)."""
    A = np.atleast_2d(A)
    size = A.sum(1)
    inter = (A & F).sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        C = np.where(size > 0, inter / np.where(size > 0, size, 1), np.nan)
    return size, inter, C


def quantiles(v):
    """Sections 3.2, 3.3: n, min, 5/25/50/75/95th percentiles, max, mean (lesson g: with n)."""
    v = np.asarray(v, dtype=float)
    v = v[~np.isnan(v)]
    if len(v) == 0:
        return {"n": 0}
    d = {"n": int(len(v)), "min": float(v.min())}
    for p in PERCENTILES:
        d[f"p{p}"] = float(np.percentile(v, p))
    d["max"] = float(v.max())
    d["mean"] = float(v.mean())
    return d


def chance_corrected(q, chance):
    """Section 3.3: (C − chance)/(1 − chance) on every quantile (affine, so it commutes)."""
    return {k: (v if k == "n" else (v - chance) / (1 - chance)) for k, v in q.items()}


def indicator(samples):
    M = np.zeros((len(samples), N_COLUMNS))
    for i, s in enumerate(samples):
        M[i, s] = 1.0
    return M


def curve_samples():
    """Section 3.2: columns 0-795 in ascending (p, q). k = 1: every column once; k = 2-512:
    50 samples by default_rng(1000 k + j).choice(796, size=k, replace=False); k = 796: all."""
    out = {}
    for k in K_GRID:
        if k == 1:
            out[k] = [np.array([c]) for c in range(N_COLUMNS)]
        elif k == N_COLUMNS:
            out[k] = [np.arange(N_COLUMNS)]
        else:
            out[k] = [np.random.default_rng(curve_seed(k, j)).choice(N_COLUMNS, size=k,
                                                                     replace=False)
                      for j in range(N_SAMPLES)]
    return out


def curve_point(A, F, chance):
    """Section 3.2, per k: samples, empty A_K, quantiles of C(A_K) (raw, chance-corrected) and of
    |A_K| (an empty set's size 0 is included)."""
    size, _, C = containment(A, F)
    qC = quantiles(C)
    return {"n_samples": int(len(size)), "n_empty": int((size == 0).sum()), "C": qC,
            "C_chance_corrected": chance_corrected(qC, chance), "size": quantiles(size)}


def q3p95_label(size, inter, nB, nBF):
    """Section 3.7: (a) iff at least 25 % of non-empty columns have C_c >= R_in; (b) iff at most
    5 % do; else unclear. Integer comparison, so a column equal to B sits exactly at R_in."""
    ok = size > 0
    at_or_above = (inter[ok] * nB >= nBF * size[ok])
    share = float(at_or_above.mean()) if ok.any() else float("nan")
    lab = "(a)" if share >= Q3_SHARE else ("(b)" if share <= P95_SHARE else "unclear")
    return {"label": lab, "share_at_or_above_R_in": share, "n": int(ok.sum()), "note": Q3P95_NOTE}


# ------------------------------------------------------------------------------------------
# Section 3.8: synthetic worlds, calibration, envelope L, two-world check.

def world_specs():
    specs = []
    for i, p in enumerate(THIN_P):
        specs.append({"family": "thinning", "role": "validation", "rate": p,
                      "seed": thin_val_seed(i)})
        for j in range(N_THIN_CAL_REPEATS):
            specs.append({"family": "thinning", "role": "calibration", "rate": p,
                          "seed": thin_cal_seed(i, j)})
    for i, r in enumerate(UNIFORM_R):
        for j in range(N_EXTRAS_CAL_REPEATS):
            specs.append({"family": "uniform", "role": "calibration", "rate": r,
                          "seed": uniform_cal_seed(i, j)})
    for seed, r in UNIFORM_VAL:
        specs.append({"family": "uniform", "role": "validation", "rate": r, "seed": seed})
    for i, q in enumerate(INF_QF):
        for j in range(N_EXTRAS_CAL_REPEATS):
            specs.append({"family": "in_F", "role": "calibration", "rate": q,
                          "seed": inf_cal_seed(i, j)})
    for seed, q in INF_VAL:
        specs.append({"family": "in_F", "role": "validation", "rate": q, "seed": seed})
    return specs


def assert_seeds_unique(specs):
    """Section 3.8, "Seeds, all disjoint": world seeds unique, none in 0-19 (S4), none among the
    curve's 1000 k + j."""
    seeds = [s["seed"] for s in specs]
    curve = {curve_seed(k, j) for k in K_GRID if 1 < k < N_COLUMNS for j in range(N_SAMPLES)}
    if (len(seeds) != N_WORLDS or len(set(seeds)) != N_WORLDS or set(seeds) & set(S4_SEEDS)
            or set(seeds) & curve):
        sys.exit("SEEDS NOT UNIQUE: " + str(sorted(seeds)))
    return {"n_world_seeds": len(seeds), "unique": True, "disjoint_from_S4_0_19": True,
            "disjoint_from_curve_seeds": True}


def make_world(spec, B, F):
    """Section 3.8: 796 synthetic columns on the full 900-cell grid, one draw per (column, cell)
    from default_rng(seed).random((796, 900)). Thinning keeps a B cell iff its draw >= p;
    uniform adds a non-B cell iff its draw < r * 165 / 735; in-F adds a cell of F \\ B iff its
    draw < q_F."""
    u = np.random.default_rng(spec["seed"]).random((N_COLUMNS, NCELL))
    Bm = np.broadcast_to(B, u.shape)
    if spec["family"] == "thinning":
        return Bm & (u >= spec["rate"])
    if spec["family"] == "uniform":
        q = spec["rate"] * int(B.sum()) / int((~B).sum())
        return Bm | (np.broadcast_to(~B, u.shape) & (u < q))
    return Bm | (np.broadcast_to(F & ~B, u.shape) & (u < spec["rate"]))


def average_synthetic(W, M, k):
    """Section 3.8: a present cell carries SYNAPSE_THRESHOLD; the mean over K (denominator |K|)
    is pruned below MEAN_PRUNE_BELOW. No autapse row: a cell stands for two distinct neurons."""
    counts = M @ W.astype(np.float64)
    return ~((SYNAPSE_THRESHOLD * counts / k) < MEAN_PRUNE_BELOW)


def run_world(spec, B, F, indicators, chance):
    """One world: its curve on the real k grid and samples, its Delta computed as the real one
    (section 3.2), its Q3/P95 label (section 3.7)."""
    W = make_world(spec, B, F)
    curve = {}
    for k in K_GRID:
        A = average_synthetic(W, indicators[k], k)
        curve[k] = curve_point(A, F, chance)
        if k == 1:
            size1, inter1, C1 = containment(A, F)
        if k == N_COLUMNS:
            c_full = containment(A, F)[2][0]
    delta = float(c_full - np.median(C1[~np.isnan(C1)]))
    out = dict(spec)
    out.update({"delta": delta, "C_full": float(c_full),
                "q3p95": q3p95_label(size1, inter1, int(B.sum()), int((B & F).sum())),
                "median_extras": float(np.median((W & ~B).sum(1))),
                "median_losses": float(np.median((B & ~W).sum(1))),
                "curve": {str(k): v for k, v in curve.items()}})
    return out


def calibrate(worlds):
    """Section 3.8, "Calibration": Delta_cal(r) = median Delta of the 5 uniform worlds at r, with
    Delta_cal(0) = 0; Delta_calF(r_F) likewise on the in-F worlds, Delta_calF(0) = 0 (revision
    2.3); L = the minimum Delta over all 48 thinning worlds, nothing subtracted."""
    def per_rate(fam, rates):
        out = []
        for r in rates:
            ds = [w["delta"] for w in worlds if w["family"] == fam
                  and w["role"] == "calibration" and w["rate"] == r]
            assert len(ds) == N_EXTRAS_CAL_REPEATS
            out.append((float(np.median(ds)), ds))
        return out

    uni, inf = per_rate("uniform", UNIFORM_R), per_rate("in_F", INF_QF)
    cal = {"uniform_r": [0.0] + list(UNIFORM_R),
           "uniform_delta": [0.0] + [m for m, _ in uni],
           "uniform_delta_all": [[]] + [ds for _, ds in uni],
           "inF_qF": [0.0] + list(INF_QF),
           "inF_rF": [0.0] + [q * (REF_F - REF_BF) / REF_B for q in INF_QF],
           "inF_delta": [0.0] + [m for m, _ in inf],
           "inF_delta_all": [[]] + [ds for _, ds in inf]}
    thin = [w for w in worlds if w["family"] == "thinning"]
    assert len(thin) == 48
    cal["L"] = float(min(w["delta"] for w in thin))
    cal["L_from"] = [{"p": w["rate"], "seed": w["seed"], "role": w["role"], "delta": w["delta"]}
                     for w in thin]
    ud, fd = np.array(cal["uniform_delta"]), np.array(cal["inF_delta"])
    cal["uniform_strictly_increasing"] = bool(np.all(np.diff(ud) > 0))
    cal["inF_strictly_decreasing"] = bool(np.all(np.diff(fd) < 0))
    cal["delta_cal_5"] = float(ud[cal["uniform_r"].index(K_STAR_A)])
    cal["delta_cal_20"] = float(ud[cal["uniform_r"].index(K_STAR_B)])
    return cal


def k_star(delta, cal):
    """Section 3.8: k* interpolates r against Delta_cal(r); "< 0 %" below 0, "> 40 %" above."""
    xs, ys = cal["uniform_delta"], cal["uniform_r"]
    if delta < xs[0]:
        return None, "< 0 %"
    if delta > xs[-1]:
        return None, f"> {100 * ys[-1]:.0f} %"
    v = float(np.interp(delta, xs, ys))
    return v, f"{100 * v:.2f} %"


def k_star_F(delta, cal):
    """Section 3.8: k*_F interpolates r_F against Delta_calF(r_F) (decreasing); "> 16.7 %"
    below Delta_calF(16.7 %); "< 0 %" above 0, reachable only if L > 0."""
    xs, ys = cal["inF_delta"][::-1], cal["inF_rF"][::-1]
    if delta < xs[0]:
        return None, f"> {100 * ys[0]:.1f} %"
    if delta > xs[-1]:
        return None, "< 0 %"
    v = float(np.interp(delta, xs, ys))
    return v, f"{100 * v:.2f} %"


def read_label(delta, cal):
    """Section 4: (c) first; the rest only when Delta >= L, read on Delta by the registered
    equivalent forms k* <= 5 % <=> Delta <= Delta_cal(5 %), k* >= 20 % <=> Delta >= Delta_cal(20 %)."""
    if delta < cal["L"]:
        return "(c)"
    if delta <= cal["delta_cal_5"]:
        return "(a)"
    if delta < cal["delta_cal_20"]:
        return "unclear"
    return "(b)"


def two_world_check(worlds):
    """Section 3.8, "Two-world check": the fresh-seed worlds read by the section 4 rule."""
    req = []
    for w in worlds:
        if w["role"] != "validation":
            continue
        fam, r, lab = w["family"], w["rate"], w["label"]
        if fam == "thinning":
            need, ok = "must read (a)", lab == "(a)"
        elif fam == "uniform" and r in (0.30, 0.40):
            need, ok = "must read (b)", lab == "(b)"
        elif fam == "uniform" and r == 0.20:
            need, ok = "must not read (a)", lab != "(a)"
        elif fam == "uniform" and r == 0.10:
            need, ok = "must read unclear", lab == "unclear"
        elif fam == "uniform" and r == 0.05:
            need, ok = "must not read (b)", lab != "(b)"
        elif fam == "in_F":
            need, ok = "must read (c)", lab == "(c)"
        else:
            raise AssertionError(w)
        req.append({"family": fam, "rate": r, "seed": w["seed"], "delta": w["delta"],
                    "label": lab, "requirement": need, "passed": bool(ok)})
    return req


def run_synthetic(B, F, indicators, chance):
    """Section 7 step 5: seed assertion, 100 worlds, calibrations and their monotonicity, then the
    two-world check. Stops on any failure."""
    specs = world_specs()
    seeds = assert_seeds_unique(specs)
    worlds = [run_world(s, B, F, indicators, chance) for s in specs]
    cal = calibrate(worlds)
    if not (cal["uniform_strictly_increasing"] and cal["inF_strictly_decreasing"]):
        log("CALIBRATION NOT MONOTONE")
        log(f"  uniform Delta_cal: {cal['uniform_delta']}")
        log(f"  in-F Delta_calF:   {cal['inF_delta']}")
        sys.exit(1)
    for w in worlds:
        w["label"] = read_label(w["delta"], cal)
        w["k_star"], w["k_star_text"] = k_star(w["delta"], cal)
    checks = two_world_check(worlds)
    syn = {"seeds": seeds, "calibration": cal, "two_world_check": checks,
           "two_world_check_passed": all(c["passed"] for c in checks), "worlds": worlds}
    print_synthetic(syn)
    if not syn["two_world_check_passed"]:
        log("TWO-WORLD CHECK FAILED: no real curve point or S1-S4 value is computed (section 3.8).")
        sys.exit(1)
    return syn


def print_synthetic(syn):
    cal = syn["calibration"]
    log("\n== Section 3.8: synthetic calibration ==")
    fmt5 = lambda ds: ", ".join(f"{d:+.5f}" for d in ds) if ds else "defined as 0, no world"
    log("uniform extras, Delta_cal(r) = median of the 5 worlds per rate (the 5 in brackets):")
    for r, d, ds in zip(cal["uniform_r"], cal["uniform_delta"], cal["uniform_delta_all"]):
        log(f"  r={100 * r:g}%: {d:+.5f}  [{fmt5(ds)}]")
    log("in-F extras, Delta_calF(r_F) = median of the 5 worlds per rate (the 5 in brackets):")
    for q, rf, d, ds in zip(cal["inF_qF"], cal["inF_rF"], cal["inF_delta"], cal["inF_delta_all"]):
        log(f"  q_F={100 * q:g}% (r_F={100 * rf:.1f}%): {d:+.5f}  [{fmt5(ds)}]")
    log(f"L (minimum Delta over the 48 thinning worlds) = {cal['L']:+.5f}")
    log(f"monotone: uniform {cal['uniform_strictly_increasing']}, "
        f"in-F {cal['inF_strictly_decreasing']}")
    log("thinning Deltas by p (validation seed first, then the 5 calibration seeds):")
    for p in THIN_P:
        ws = [w for w in syn["worlds"] if w["family"] == "thinning" and w["rate"] == p]
        log(f"  p={100 * p:g}%: " + ", ".join(f"{w['delta']:+.5f}" for w in ws)
            + "   Q3/P95: " + ", ".join(w["q3p95"]["label"] for w in ws))
    log("\n== Section 3.8: two-world check ==")
    for c in syn["two_world_check"]:
        log(f"  {c['family']:8s} rate={100 * c['rate']:g}% seed={c['seed']}: "
            f"Delta={c['delta']:+.5f} label={c['label']:8s} {c['requirement']:18s} "
            f"{'PASS' if c['passed'] else 'FAIL'}")
    log(f"two-world check passed: {syn['two_world_check_passed']}")
    log("\nevery world (family, role, rate, seed, Delta, label, Q3/P95 label and share, k*):")
    for w in syn["worlds"]:
        log(f"  {w['family']:8s} {w['role']:11s} {100 * w['rate']:5g}% seed {w['seed']:3d}: "
            f"Delta={w['delta']:+.5f} {w['label']:8s} Q3/P95 {w['q3p95']['label']:8s} "
            f"({w['q3p95']['share_at_or_above_R_in']:.3f}) k*={w['k_star_text']}")


# ------------------------------------------------------------------------------------------
# Section 7 step 3, section 2.4: per-column target-anchored tables x_c for all 796 columns.

def build_columns():
    """Sections 2.1, 2.2, 2.4: neurons and kept connections as the builder (its lines 202-231);
    columns = distinct (p, q), indexed ascending. x_c(s, t, du, dv) = syn(i -> j) for the
    type-t neuron j in c and the type-s neuron i at (p_c - du, q_c - dv)."""
    import pandas as pd

    pos, type_of = {}, {}
    with gzip.open(DATA_ROOT / "column_assignment.csv.gz", "rt", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["hemisphere"] != "right" or r["type"] not in FLYWIRE_NAME_OF:
                continue
            rid = int(r["root_id"])
            if rid in pos:
                sys.exit("REFUSED: a root id has two right-hemisphere column rows (section 2.1)")
            pos[rid] = (int(r["p"]), int(r["q"]))
            type_of[rid] = r["type"]
    cols = sorted(set(pos.values()))
    if len(cols) != N_COLUMNS:
        sys.exit(f"REFUSED: {len(cols)} right-hemisphere columns, registered {N_COLUMNS}")
    col_index = {xy: i for i, xy in enumerate(cols)}
    H = np.zeros((N_COLUMNS, NT))                       # H[c, t] = 1 iff c holds a type-t neuron
    for rid, t in type_of.items():
        c = col_index[pos[rid]]
        if H[c, TI[t]]:
            sys.exit("REFUSED: a column holds two neurons of the same type (section 2.2)")
        H[c, TI[t]] = 1.0
    n_of_type = {t: int(H[:, TI[t]].sum()) for t in TYPES}

    df = pd.read_feather(DATA_ROOT / "proofread_connections_783.feather",
                         columns=["pre_pt_root_id", "post_pt_root_id", "syn_count"])
    ids = pd.Index(list(pos))
    df = df[df.pre_pt_root_id.isin(ids) & df.post_pt_root_id.isin(ids)]
    df = df.groupby(["pre_pt_root_id", "post_pt_root_id"], as_index=False)["syn_count"].sum()
    df = df[df.syn_count >= SYNAPSE_THRESHOLD]

    entries, seen = [], set()                           # (c, s, t, du, dv, syn)
    for pre, post, n in df.itertuples(index=False):
        s, t = type_of[pre], type_of[post]
        du, dv = pos[post][0] - pos[pre][0], pos[post][1] - pos[pre][1]
        key = (col_index[pos[post]], s, t, du, dv)
        if key in seen:
            sys.exit("REFUSED: two entries for one (column, s, t, du, dv) (section 2.4)")
        seen.add(key)
        entries.append((*key, int(n)))

    row_keys = sorted({(s, t, du, dv) for _, s, t, du, dv, _ in entries})
    row_of = {k: i for i, k in enumerate(row_keys)}
    X = np.zeros((N_COLUMNS, len(row_keys)))
    for c, s, t, du, dv, n in entries:
        X[c, row_of[(s, t, du, dv)]] = n
    row_cell = np.array([cell(s, t) for s, t, _, _ in row_keys])
    P = np.zeros((len(row_keys), NCELL), dtype=np.float32)   # row -> its type pair
    P[np.arange(len(row_keys)), row_cell] = 1.0
    log(f"per-column tables: {N_COLUMNS} columns, {len(entries)} kept neuron pairs, "
        f"{len(row_keys)} distinct (s, t, du, dv) rows")
    return {"cols": cols, "H": H, "n_of_type": n_of_type, "entries": entries,
            "row_keys": row_keys, "X": X, "P": P,
            "row_t": np.array([TI[t] for _, t, _, _ in row_keys]),
            "row_autapse": np.array([s == t and (du, dv) == (0, 0) for s, t, du, dv in row_keys]),
            "row_bin": np.array([min(max(abs(du), abs(dv)), 3) for _, _, du, dv in row_keys])}


def existence_sets(D):
    """Section 2.5: E_c = pairs with x_c > 0 at some offset, the self offset excluded."""
    live = (D["X"] > 0) & ~D["row_autapse"][None, :]
    return (live.astype(np.float32) @ D["P"]) > 0


# ------------------------------------------------------------------------------------------
# Section 7 step 4, section 3.6: machine check.

def machine_check(D, bank_rows, meta):
    """Section 3.6: sum over all 796 columns of x_c / N_t, autapse dropped, pruned below 1, is the
    bank exactly. Plain summation over the entries, a code path apart from the curve's matrix
    product. On failure: "MACHINE CHECK FAILED" and nothing else."""
    sums = {}
    for _, s, t, du, dv, n in D["entries"]:
        sums[(s, t, du, dv)] = sums.get((s, t, du, dv), 0) + n
    rebuilt = {}
    for (s, t, du, dv), total in sums.items():
        mean = total / D["n_of_type"][t]
        if s == t and (du, dv) == (0, 0):
            continue
        if mean < MEAN_PRUNE_BELOW:
            continue
        rebuilt[(s, t, du, dv)] = mean
    ok = (D["n_of_type"] == meta["neurons_per_type"]
          and set(rebuilt) == set(bank_rows) and len(rebuilt) == BANK_ROWS
          and all(abs(rebuilt[k] - bank_rows[k]) <= MACHINE_TOL for k in bank_rows)
          and len({(s, t) for s, t, _, _ in rebuilt}) == REF_B
          and sha256_file(BANK_OFFSETS) == EXPECTED_OFFSETS_SHA
          and BUILDER_SHA_READ == meta["builder_sha256"] == EXPECTED_BUILDER_SHA)
    if not ok:
        print("MACHINE CHECK FAILED", flush=True)
        sys.exit(1)
    maxdiff = max(abs(rebuilt[k] - bank_rows[k]) for k in bank_rows)
    log(f"machine check passed: {BANK_ROWS} rows, {REF_B} pairs, max |n_syn difference| = "
        f"{maxdiff:.1e}")
    return {"passed": True, "rows": len(rebuilt), "pairs": REF_B, "max_abs_diff": maxdiff}


# ------------------------------------------------------------------------------------------
# Section 3.2: the sample average with the builder's rule, restricted to K.

def average_real(D, M):
    """Section 3.2: n_K(t) = columns of K holding type t; mean_K = sum over K of x_c / n_K(t)
    where n_K(t) >= 1; autapse row dropped; mean_K < 1 dropped; (s, t) exists iff a row
    survives. M: samples x 796 indicator. Returns (A_K, means, kept rows)."""
    sums = M @ D["X"]
    nK = (M @ D["H"])[:, D["row_t"]]
    with np.errstate(invalid="ignore", divide="ignore"):
        mean = np.where(nK > 0, sums / np.where(nK > 0, nK, 1.0), 0.0)
    keep = (nK > 0) & ~D["row_autapse"][None, :] & ~(mean < MEAN_PRUNE_BELOW)
    A = (keep.astype(np.float32) @ D["P"]) > 0
    return A, mean, keep


def rows_equal_bank(D, mean, keep, bank_rows):
    got = {D["row_keys"][i]: float(mean[i]) for i in np.nonzero(keep)[0]}
    return (set(got) == set(bank_rows)
            and all(abs(got[k] - bank_rows[k]) <= MACHINE_TOL for k in bank_rows))


def real_curve(D, E, B, F, indicators, bank_rows, chance):
    """Section 7 step 6, section 3.2: the curve on all 796 columns; at k = 796 the anchor check
    ("CURVE ANCHOR FAILED"); at k = 1 the registered identity A_K = E_c is asserted."""
    curve = {}
    for k in K_GRID:
        A, mean, keep = average_real(D, indicators[k])
        if k == 1 and not np.array_equal(A, E):
            print("CURVE K=1 PATH DIFFERS FROM E_c", flush=True)
            sys.exit(1)
        if k == N_COLUMNS and not (np.array_equal(A[0], B)
                                   and rows_equal_bank(D, mean[0], keep[0], bank_rows)):
            print("CURVE ANCHOR FAILED", flush=True)
            sys.exit(1)
        curve[k] = curve_point(A, F, chance)
    log(f"curve anchor passed: A_796 = B, {BANK_ROWS} rows equal to {MACHINE_TOL:g}")
    return curve


def column_descriptors(E, B, F):
    """Section 3.9 per column: |E_c \\ B|, |B \\ E_c|, X_c = |E_c ∩ (F \\ B)| / |E_c \\ B|."""
    extras = (E & ~B).sum(1)
    losses = (B & ~E).sum(1)
    inF = (E & F & ~B).sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        X = np.where(extras > 0, inF / np.where(extras > 0, extras, 1), np.nan)
    return extras, losses, X


def section_3_9(E, B, F, idx):
    extras, losses, X = column_descriptors(E[idx], B, F)
    return {"n_columns": int(len(idx)), "n_no_nonB_pair": int((extras == 0).sum()),
            "X_c": quantiles(X), "extras_E_minus_B": quantiles(extras),
            "losses_B_minus_E": quantiles(losses),
            "reference_points": "uniform extras give 69/735 = 0.0939; in-F extras give 1",
            "note": "decides nothing; no label is read from it"}


def verdict(E, B, F, cal, R_in):
    """Sections 3.2 and 4: Delta = R_in − median over the 796 (non-empty E_c) of C(E_c), its
    label, k*, k*_F, k*_obs = Delta / (R_in − median X_c), medians of |E_c \\ B|, |B \\ E_c|."""
    size, _, C = containment(E, F)
    delta = float(R_in - np.median(C[~np.isnan(C)]))
    extras, losses, X = column_descriptors(E, B, F)
    Xmed = float(np.median(X[~np.isnan(X)])) if (~np.isnan(X)).any() else float("nan")
    ks, ks_text = k_star(delta, cal)
    kf, kf_text = k_star_F(delta, cal)
    lab = read_label(delta, cal)
    if np.isnan(Xmed) or abs(R_in - Xmed) < K_STAR_OBS_EPS:       # section 4: "n/a"
        kobs, kobs_text = None, "n/a"
    else:
        kobs = delta / (R_in - Xmed)
        kobs_text = f"{100 * kobs:.2f} %"
    return {"delta": delta, "label": lab, "label_text": LABEL_TEXT[lab], "L": cal["L"],
            "k_star": ks, "k_star_text": ks_text, "k_star_F": kf, "k_star_F_text": kf_text,
            "k_star_F_read": lab == "(c)", "k_star_obs": kobs, "k_star_obs_text": kobs_text,
            "X_median_796": None if np.isnan(Xmed) else Xmed,
            "median_extras_796": float(np.median(extras)),
            "median_losses_796": float(np.median(losses)),
            "n_empty_E_c_796": int((size == 0).sum()), "n_columns": N_COLUMNS}


# ------------------------------------------------------------------------------------------
# Section 7 step 7, section 2.3: inclusion.

def inclusion(D):
    """Section 2.3, D1: included iff all 30 types and all six axial neighbours among the 796."""
    colset = set(D["cols"])
    complete = D["H"].sum(1) == NT
    interior = np.array([all((p + a, q + b) in colset for a, b in HEX_NEIGHBOURS)
                         for p, q in D["cols"]])
    inc = np.nonzero(complete & interior)[0]
    return inc, {"columns": N_COLUMNS, "complete_30_types": int(complete.sum()),
                 "included_complete_and_interior": int(len(inc)),
                 "removed_lacking_a_type": int((~complete).sum()),
                 "removed_complete_but_not_interior": int((complete & ~interior).sum()),
                 "columns_with_at_least_28_types": int((D["H"].sum(1) >= 28).sum()),
                 "columns_missing_type": {t: int((D["H"][:, TI[t]] == 0).sum()) for t in TYPES}}


# ------------------------------------------------------------------------------------------
# Section 7 step 8: S1-S4, Zcode's falsifier, offset bins.

def s1(E, F, inc, cal, R_in, chance):
    """Section 3.3: C(E_c) and |E_c| over the included; Delta_294 and its label (decides
    nothing); the Q3/P95 label on the 294 (section 3.7)."""
    size, inter, C = containment(E[inc], F)
    qC = quantiles(C)
    d294 = float(R_in - np.median(C[~np.isnan(C)]))
    return {"n_columns": int(len(inc)), "n_empty": int((size == 0).sum()), "C": qC,
            "C_chance_corrected": chance_corrected(qC, chance), "size": quantiles(size),
            "delta_294": d294, "delta_294_label": read_label(d294, cal),
            "delta_294_k_star": k_star(d294, cal)[1],
            "q3p95": q3p95_label(size, inter, REF_B, REF_BF)}


def s2(E, inc, R_in, R_jac):
    """Section 3.4: every unordered pair of included columns: Jaccard and overlap coefficient,
    raw and against the density-matched expectation (expected intersection ab/900 plugged into
    each ratio). Pairs with an empty set counted and left out. Q3/P95 labels: overlap against
    R_in, Jaccard against R_jac."""
    Ei = E[inc].astype(np.float64)
    inter = Ei @ Ei.T
    a = Ei.sum(1)
    iu = np.triu_indices(len(inc), 1)
    I, sa, sb = inter[iu], a[iu[0]], a[iu[1]]
    ok = (sa > 0) & (sb > 0)
    I, sa, sb = I[ok], sa[ok], sb[ok]
    mn, un = np.minimum(sa, sb), sa + sb - I
    ov, jac = I / mn, I / un
    e = sa * sb / NCELL
    ov0, jac0 = e / mn, e / (sa + sb - e)
    share_ov = float((I * REF_B >= REF_BF * mn).mean())
    share_jac = float((I * (REF_B + REF_F - REF_BF) >= REF_BF * un).mean())
    lab = lambda s: "(a)" if s >= Q3_SHARE else ("(b)" if s <= P95_SHARE else "unclear")
    return {"n_column_pairs": int(len(iu[0])), "n_pairs_with_empty_set": int((~ok).sum()),
            "overlap": quantiles(ov), "overlap_chance_corrected": quantiles((ov - ov0) / (1 - ov0)),
            "jaccard": quantiles(jac),
            "jaccard_chance_corrected": quantiles((jac - jac0) / (1 - jac0)),
            "reference_R_in_overlap_B_F": R_in, "reference_R_jac": R_jac,
            "q3p95_overlap_vs_R_in": {"label": lab(share_ov), "share_at_or_above": share_ov,
                                      "note": Q3P95_NOTE},
            "q3p95_jaccard_vs_R_jac": {"label": lab(share_jac), "share_at_or_above": share_jac,
                                       "note": Q3P95_NOTE}}


def s3(E, B, inc):
    """Section 3.5, S3: |E_c ∩ B| / |E_c| and |E_c ∩ B| / |B| over the included (empty left out)."""
    Ei = E[inc]
    size, inB = Ei.sum(1), (Ei & B).sum(1)
    ok = size > 0
    return {"n_columns": int(len(inc)), "n_empty": int((~ok).sum()),
            "share_of_column_in_B": quantiles(inB[ok] / size[ok]),
            "share_of_B_in_column": quantiles(inB[ok] / REF_B)}


def s4(D, F, pop, chance):
    """Section 3.5, S4: seeds 0-19, default_rng(seed).permutation(len(pop)), first half = the
    first len(pop)//2; each half averaged by the section 3.2 rule. Overlap and Jaccard between
    halves, C of each half (40 values pooled). Returns (aggregate, private half sets)."""
    ov, jac, Cs, private = [], [], [], []
    h = len(pop) // 2
    for seed in S4_SEEDS:
        perm = np.random.default_rng(seed).permutation(len(pop))
        halves = [pop[perm[:h]], pop[perm[h:]]]
        A, _, _ = average_real(D, indicator(halves))
        a, b = A[0], A[1]
        I, mn = int((a & b).sum()), min(int(a.sum()), int(b.sum()))
        ov.append(I / mn if mn else np.nan)
        jac.append(I / (a | b).sum() if (a | b).any() else np.nan)
        Cs.extend(containment(A, F)[2].tolist())
        private.append({"seed": seed, "halves": [x.tolist() for x in halves],
                        "pair_sets": [np.nonzero(x)[0].tolist() for x in (a, b)]})
    qC = quantiles(Cs)
    return {"n_splits": len(S4_SEEDS), "half_size": h, "population": int(len(pop)),
            "overlap": quantiles(ov), "jaccard": quantiles(jac), "C_halves_pooled": qC,
            "C_halves_pooled_chance_corrected": chance_corrected(qC, chance)}, private


def zcode_falsifier(D, B, F, inc, bank_rows):
    """Section 3.2: the 294-average by the builder rule; printed, no role in the verdict."""
    A, mean, keep = average_real(D, indicator([inc]))
    a = A[0]
    return {"reproduces_bank_rows_to_1e-12": bool(rows_equal_bank(D, mean[0], keep[0], bank_rows)),
            "pairs": int(a.sum()), "pairs_in_B": int((a & B).sum()),
            "C": float((a & F).sum() / a.sum()) if a.any() else None,
            "note": "printed without any role in the verdict"}


def offset_bins(D, idx):
    """Section 2.4: per-column rows (x_c > 0, self offset excluded) by max(|du|, |dv|) in 0, 1,
    2, 3+; and per-column existences by the smallest bin that carries them."""
    live = (D["X"][idx] > 0) & ~D["row_autapse"][None, :]
    names = ("0", "1", "2", "3+")
    rows, first = {}, {}
    carried = np.zeros((len(idx), NCELL), dtype=bool)
    for b in range(4):
        sel = D["row_bin"] == b
        rows[names[b]] = int(live[:, sel].sum())
        here = (live[:, sel].astype(np.float32) @ D["P"][sel]) > 0
        first[names[b]] = int((here & ~carried).sum())
        carried |= here
    return {"n_columns": int(len(idx)), "rows_by_max_abs_offset": rows,
            "existences_by_smallest_bin": first}


# ------------------------------------------------------------------------------------------
# Section 7 step 9: outputs.

def write_private(D, E, samples, s4_private, inc, manifest_inputs):
    """Section 1: every file keyed by column, outside the repository, with a hash manifest."""
    PRIVATE_OUT.mkdir(parents=True, exist_ok=True)
    files = []
    p = PRIVATE_OUT / "per_column_rows.csv.gz"
    with gzip.open(p, "wt", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["column_index", "p", "q", "src", "tar", "du", "dv", "syn"])
        for c, s, t, du, dv, n in sorted(D["entries"]):
            w.writerow([c, *D["cols"][c], s, t, du, dv, n])
    files.append(p)
    p = PRIVATE_OUT / "per_column_existence.csv.gz"
    with gzip.open(p, "wt", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["column_index", "p", "q", "src", "tar"])
        for c, x in zip(*np.nonzero(E)):
            w.writerow([int(c), *D["cols"][c], TYPES[x // NT], TYPES[x % NT]])
    files.append(p)
    p = PRIVATE_OUT / "included_columns.csv"
    with open(p, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["column_index", "p", "q"])
        for c in inc:
            w.writerow([int(c), *D["cols"][c]])
    files.append(p)
    p = PRIVATE_OUT / "curve_samples.json"
    p.write_text(json.dumps({str(k): [s.tolist() for s in v] for k, v in samples.items()
                             if 1 < k < N_COLUMNS}), encoding="utf-8")
    files.append(p)
    p = PRIVATE_OUT / "s4_halves.json"
    p.write_text(json.dumps(s4_private), encoding="utf-8")
    files.append(p)
    man = {"registration": REGISTRATION, "inputs": manifest_inputs,
           "files": {f.name: {"sha256": sha256_file(f), "size_bytes": f.stat().st_size}
                     for f in files}}
    (PRIVATE_OUT / "manifest.json").write_text(json.dumps(man, indent=2), encoding="utf-8")


def quote_sections():
    """Section 7 outputs: sections 4 and 5 of the registration, quoted, not paraphrased."""
    text = (ROOT / REGISTRATION).read_text(encoding="utf-8")
    start = text.index("## 4. Reading rule")
    end = text.index("## 6. What the test cannot show")
    return "\n".join(("> " + ln) if ln else ">" for ln in text[start:end].rstrip().splitlines())


def fmt_q(q, digits=4):
    if not q.get("n"):
        return "n = 0"
    keys = ["min", "p5", "p25", "p50", "p75", "p95", "max", "mean"]
    return f"n = {q['n']}; " + ", ".join(f"{k} {q[k]:.{digits}f}" for k in keys if k in q)


def svg_plot(real_pts, worlds, path):
    """Section 7 outputs: the real curve (median, 5-95 band) against log2 k with the calibration
    worlds' median curves. Aggregate only; plain SVG, so no plotting package is needed."""
    W, H, ml, mr, mt, mb = 760, 490, 64, 190, 40, 80
    ks = list(K_GRID)
    xs = np.log2(ks)
    cal = [w for w in worlds if w["role"] == "calibration"]
    vals = [real_pts[k]["C"][q] for k in ks for q in ("p5", "p95")]
    vals += [w["curve"][str(k)]["C"]["p50"] for w in cal for k in ks]
    lo, hi = np.floor(min(vals) * 20) / 20, 1.0
    X = lambda x: ml + (x - xs[0]) / (xs[-1] - xs[0]) * (W - ml - mr)
    Y = lambda y: mt + (hi - y) / (hi - lo) * (H - mt - mb)
    poly = lambda pts: " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in pts)
    colours = {"thinning": "#9a9a92", "uniform": "#eb6834", "in_F": "#1baf7a"}
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'font-family="sans-serif" font-size="12"><rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="{ml}" y="22" font-size="14" fill="#222">Containment in flyvis-30 of the '
         f'average over k columns (median; band 5-95 %)</text>']
    for y in np.arange(lo, hi + 1e-9, 0.05):
        o.append(f'<line x1="{ml}" x2="{W - mr}" y1="{Y(y):.1f}" y2="{Y(y):.1f}" '
                 f'stroke="#e6e6e3"/><text x="{ml - 6}" y="{Y(y) + 4:.1f}" text-anchor="end" '
                 f'fill="#555">{y:.2f}</text>')
    for k, x in zip(ks, xs):
        o.append(f'<text x="{X(x):.1f}" y="{H - mb + 16}" text-anchor="middle" fill="#555">'
                 f'{k}</text>')
    o.append(f'<text x="{(ml + W - mr) / 2}" y="{H - mb + 34}" text-anchor="middle" '
             f'fill="#333">k (columns averaged, log2 scale)</text>')
    head, tail = PLOT_CAPTION.split("; intermediate")
    for i, line in enumerate((f"Note (section 7): {head};", f"intermediate{tail}.")):
        o.append(f'<text x="{ml}" y="{H - 24 + 14 * i}" font-size="11" fill="#555">'
                 f'{line}</text>')
    for w in cal:
        pts = [(x, w["curve"][str(k)]["C"]["p50"]) for k, x in zip(ks, xs)]
        op = "0.35" if w["family"] == "thinning" else "0.9"
        o.append(f'<polyline points="{poly(pts)}" fill="none" stroke="{colours[w["family"]]}" '
                 f'stroke-width="1.2" opacity="{op}"/>')
    band = [(x, real_pts[k]["C"]["p95"]) for k, x in zip(ks, xs)]
    band += [(x, real_pts[k]["C"]["p5"]) for k, x in reversed(list(zip(ks, xs)))]
    o.append(f'<polygon points="{poly(band)}" fill="#2a78d6" opacity="0.18"/>')
    med = [(x, real_pts[k]["C"]["p50"]) for k, x in zip(ks, xs)]
    o.append(f'<polyline points="{poly(med)}" fill="none" stroke="#2a78d6" stroke-width="2"/>')
    for x, y in med:
        o.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="4" fill="#2a78d6" '
                 f'stroke="#ffffff" stroke-width="2"/>')
    legend = [("#2a78d6", "FlyWire columns (real)"), (colours["uniform"], "uniform-extras worlds"),
              (colours["in_F"], "in-F extras worlds"), (colours["thinning"], "thinning worlds")]
    for i, (c, name) in enumerate(legend):
        y = mt + 10 + 20 * i
        o.append(f'<line x1="{W - mr + 14}" x2="{W - mr + 38}" y1="{y}" y2="{y}" stroke="{c}" '
                 f'stroke-width="2"/><text x="{W - mr + 44}" y="{y + 4}" fill="#333">{name}</text>')
    o.append("</svg>")
    path.write_text("\n".join(o), encoding="utf-8")


def write_committed(summary, syn):
    """Section 7: RESULT.md, summary.json and curve.svg, aggregates only."""
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(dump_json(summary), encoding="utf-8")
    svg_plot({int(k): v for k, v in summary["real_curve"].items()}, syn["worlds"],
             OUT / "curve.svg")
    v, cal, ref = summary["verdict"], syn["calibration"], summary["reference_numbers"]
    md = ["# The column test: a lower bound on how much agreement our processing produces", "",
          f"Registration: `{REGISTRATION}`, revision {REGISTRATION_REVISION}. "
          f"git_head={summary['manifest']['git_head']}, runtime={summary['runtime_s']:.1f}s.", "",
          "Not a proxy for the overlap between banks (section 0). A lower bound on the FlyWire "
          "side only.", "",
          f"**Verdict: {v['label_text']}.** Δ = {v['delta']:+.5f}, L = {v['L']:+.5f}, "
          f"k* = {v['k_star_text']}, k*_obs = {v['k_star_obs_text']} (diagnostic), "
          f"k*_F = {v['k_star_F_text']}"
          + ("" if v["k_star_F_read"] else K_STAR_F_NOTE)
          + f"; median |E_c \\ B| = {v['median_extras_796']:g}, median |B \\ E_c| = "
          f"{v['median_losses_796']:g} (over the 796 columns).", ""]
    if v["label"] == "(b)":
        md += [f"Under (b), {B_LABEL_NOTE}.", ""]
    if summary.get("S1"):
        s = summary["S1"]
        md += [f"Beside it (decides nothing): Δ_294 = {s['delta_294']:+.5f}, label "
               f"{LABEL_TEXT[s['delta_294_label']]}, k* = {s['delta_294_k_star']}."
               + ("  **The 796-column and 294-column readings disagree.**"
                  if s["delta_294_label"] != v["label"] else ""), ""]
    md += ["## Reference numbers (section 3.1)", "", "| name | value | as registered |",
           "|---|---|---|"]
    md += [f"| `{n}` | {r['value']:.4f} | {r['as_registered']} |" for n, r in ref.items()]
    md += ["", "## Synthetic calibration (section 3.8)", "",
           "| family | rate | extra pairs, share of \\|B\\| | Δ_cal (median of 5) | the 5 worlds |",
           "|---|---|---|---|---|"]
    fmt5 = lambda ds: ", ".join(f"{d:+.5f}" for d in ds) if ds else "defined as 0, no world"
    md += [f"| uniform extras | r = {100 * r:g} % | {100 * r:g} % | {d:+.5f} | {fmt5(ds)} |"
           for r, d, ds in zip(cal["uniform_r"], cal["uniform_delta"], cal["uniform_delta_all"])]
    md += [f"| in-F extras | q_F = {100 * q:g} % | {100 * rf:.1f} % | {d:+.5f} | {fmt5(ds)} |"
           for q, rf, d, ds in zip(cal["inF_qF"], cal["inF_rF"], cal["inF_delta"],
                                   cal["inF_delta_all"])]
    md += ["", f"L = minimum Δ over the 48 thinning worlds = {cal['L']:+.5f}.", "",
           "| p | Δ of the 6 thinning worlds (validation, then calibration) | Q3/P95 labels |",
           "|---|---|---|"]
    for p in THIN_P:
        ws = [w for w in syn["worlds"] if w["family"] == "thinning" and w["rate"] == p]
        md.append(f"| {100 * p:g} % | " + ", ".join(f"{w['delta']:+.5f}" for w in ws) + " | "
                  + ", ".join(w["q3p95"]["label"] for w in ws) + " |")
    md += ["", "Two-world check:", "", "| world | seed | Δ | label | requirement | result |",
           "|---|---|---|---|---|---|"]
    md += [f"| {c['family']} {100 * c['rate']:g} % | {c['seed']} | {c['delta']:+.5f} | "
           f"{c['label']} | {c['requirement']} | {'pass' if c['passed'] else 'FAIL'} |"
           for c in syn["two_world_check"]]
    md += ["", "## The real curve (section 3.2)", "",
           "| k | samples | empty | C p5 | p25 | p50 | p75 | p95 | mean | chance-corr. p50 | "
           "\\|A_K\\| p50 |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, pt in summary["real_curve"].items():
        c = pt["C"]
        md.append(f"| {k} | {pt['n_samples']} | {pt['n_empty']} | {c['p5']:.4f} | "
                  f"{c['p25']:.4f} | {c['p50']:.4f} | {c['p75']:.4f} | {c['p95']:.4f} | "
                  f"{c['mean']:.4f} | {pt['C_chance_corrected']['p50']:.4f} | "
                  f"{pt['size']['p50']:g} |")
    md += ["", "![curve](curve.svg)", "",
           "## Where single columns' extra pairs lie (section 3.9; decides nothing)", ""]
    for name, d in summary["section_3_9"].items():
        md += [f"- **{name}** ({d['n_columns']} columns; {d['n_no_nonB_pair']} with no non-B "
               f"pair): X_c {fmt_q(d['X_c'])}; |E_c \\ B| {fmt_q(d['extras_E_minus_B'], 1)}; "
               f"|B \\ E_c| {fmt_q(d['losses_B_minus_E'], 1)}"]
    md += ["", "Reference points: uniform extras give 69/735 = 0.0939; in-F extras give 1.", "",
           "## Inclusion (section 2.3)", "", f"`{json.dumps(summary['inclusion'])}`", ""]
    if summary.get("S1"):
        s1v, s2v, s3v = summary["S1"], summary["S2"], summary["S3"]
        md += ["## S1: each included column inside flyvis-30 (section 3.3)", "",
               f"- C(E_c): {fmt_q(s1v['C'])}; empty columns: {s1v['n_empty']}",
               f"- chance-corrected: {fmt_q(s1v['C_chance_corrected'])}",
               f"- |E_c|: {fmt_q(s1v['size'], 1)}",
               f"- Q3/P95 label: {s1v['q3p95']['label']} (share at or above R_in "
               f"{s1v['q3p95']['share_at_or_above_R_in']:.4f} of {s1v['q3p95']['n']}); "
               f"{Q3P95_NOTE}", "",
               "## S2: included columns against each other (section 3.4)", "",
               f"- {s2v['n_column_pairs']} column pairs; with an empty set: "
               f"{s2v['n_pairs_with_empty_set']}",
               f"- overlap: {fmt_q(s2v['overlap'])}; chance-corrected: "
               f"{fmt_q(s2v['overlap_chance_corrected'])}; "
               f"R_in = {s2v['reference_R_in_overlap_B_F']:.4f}",
               f"- Jaccard: {fmt_q(s2v['jaccard'])}; chance-corrected: "
               f"{fmt_q(s2v['jaccard_chance_corrected'])}; R_jac = {s2v['reference_R_jac']:.4f}",
               f"- Q3/P95 labels: overlap vs R_in {s2v['q3p95_overlap_vs_R_in']['label']}, "
               f"Jaccard vs R_jac {s2v['q3p95_jaccard_vs_R_jac']['label']}; {Q3P95_NOTE}", "",
               "## S3: single columns against their own averaged bank (section 3.5)", "",
               f"- |E_c ∩ B| / |E_c|: {fmt_q(s3v['share_of_column_in_B'])}",
               f"- |E_c ∩ B| / |B|: {fmt_q(s3v['share_of_B_in_column'])}", "",
               "## S4: split-half averages (section 3.5; description only)", ""]
        for name in ("S4_294", "S4_796"):
            d = summary[name]
            md += [f"- **{name}** ({d['n_splits']} splits of {d['population']} into halves of "
                   f"{d['half_size']}): overlap {fmt_q(d['overlap'])}; Jaccard "
                   f"{fmt_q(d['jaccard'])}; C of each half (both pooled) "
                   f"{fmt_q(d['C_halves_pooled'])}"]
        md += ["", "## Zcode's falsifier (section 3.2; no role in the verdict)", "",
               f"`{json.dumps(summary['zcode_falsifier'])}`", ""]
    else:
        md += [f"S1-S4 not computed: fewer than {MIN_INCLUDED} columns included (section 2.3).",
               ""]
    md += ["## Offset bins (section 2.4)", ""]
    md += [f"- `{json.dumps(d)}`" for d in summary["offset_bins"].values()]
    md += ["", "## Checks", "",
           f"- machine check (section 3.6): `{json.dumps(summary['machine_check'])}`",
           "- curve anchor (section 3.2): passed", "",
           "## The registered reading (sections 4 and 5, quoted)", "", quote_sections(), ""]
    (OUT / "RESULT.md").write_text("\n".join(md), encoding="utf-8", newline="\n")


# ------------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--synthetic-only", action="store_true",
                    help="section 3.8 only: worlds, calibration, two-world check (B and F only)")
    ap.add_argument("--out", default=None, help="with --synthetic-only: write synthetic_only.json")
    ap.add_argument("--allow-dirty", action="store_true",
                    help="not the registered run; recorded in the manifest")
    a = ap.parse_args()
    t0 = time.time()

    if a.synthetic_only:                                           # step 1
        if not DATA_ROOT.exists():
            sys.exit(f"REFUSED: data root not found: {DATA_ROOT}")
    else:
        refuse_if_unsafe(a.allow_dirty)
    meta, inputs = refuse_if_inputs_differ(need_column_file=not a.synthetic_only)   # step 2
    bank_rows, B, F = read_B_and_F()
    ref = reference_numbers(B, F)
    R_in, R_jac, chance = ref["R_in"]["value"], ref["R_jac"]["value"], ref["chance"]["value"]
    log(f"registration: {REGISTRATION}, revision {REGISTRATION_REVISION}")
    log(f"|B| = {int(B.sum())}, |F| = {int(F.sum())}, |B & F| = {int((B & F).sum())}; "
        f"R_in = {R_in:.4f}, chance = {chance:.4f}")
    samples = curve_samples()
    indicators = {k: indicator(v) for k, v in samples.items()}

    if a.synthetic_only:
        syn = run_synthetic(B, F, indicators, chance)
        if a.out:
            Path(a.out).mkdir(parents=True, exist_ok=True)
            (Path(a.out) / "synthetic_only.json").write_text(dump_json(syn),
                                                             encoding="utf-8")
        log(f"\n--synthetic-only: stopped before any per-column data. {time.time() - t0:.1f}s")
        return

    D = build_columns()                                            # step 3
    mc = machine_check(D, bank_rows, meta)                         # step 4
    syn = run_synthetic(B, F, indicators, chance)                  # step 5
    E = existence_sets(D)                                          # step 6
    curve = real_curve(D, E, B, F, indicators, bank_rows, chance)
    v = verdict(E, B, F, syn["calibration"], R_in)
    log(f"\nVERDICT: {v['label_text']}; Delta = {v['delta']:+.5f}, L = {v['L']:+.5f}, "
        f"k* = {v['k_star_text']}, k*_obs = {v['k_star_obs_text']}, "
        f"k*_F = {v['k_star_F_text']}{'' if v['k_star_F_read'] else K_STAR_F_NOTE}; "
        f"median |E_c \\ B| = {v['median_extras_796']:g}, "
        f"median |B \\ E_c| = {v['median_losses_796']:g}")
    if v["label"] == "(b)":
        log(f"under (b), {B_LABEL_NOTE}")
    inc, inc_counts = inclusion(D)                                 # step 7
    log(f"inclusion: {inc_counts}")
    summary = {"manifest": {"registration": REGISTRATION, "revision": REGISTRATION_REVISION,
                            "git_head": git("rev-parse", "HEAD"),
                            "allow_dirty": bool(a.allow_dirty),
                            "script_sha256": sha256_file(Path(__file__)),
                            "builder_sha256": BUILDER_SHA_READ, "inputs": inputs,
                            "numpy": np.__version__, "python": platform.python_version()},
               "reference_numbers": ref, "machine_check": mc,
               "curve_anchor": {"passed": True}, "inclusion": inc_counts,
               "synthetic": syn, "real_curve": {str(k): p for k, p in curve.items()},
               "verdict": v,
               "section_3_9": {"all_796": section_3_9(E, B, F, np.arange(N_COLUMNS))},
               "offset_bins": {"all_796": offset_bins(D, np.arange(N_COLUMNS))}}
    s4_private = {}
    if len(inc) >= MIN_INCLUDED:                                   # step 8
        summary["S1"] = s1(E, F, inc, syn["calibration"], R_in, chance)
        if summary["S1"]["delta_294_label"] != v["label"]:
            log("the 796-column and 294-column readings disagree")
        summary["section_3_9"]["included_294"] = section_3_9(E, B, F, inc)
        summary["S2"] = s2(E, inc, R_in, R_jac)
        summary["S3"] = s3(E, B, inc)
        summary["S4_294"], s4_private["S4_294"] = s4(D, F, inc, chance)
        summary["S4_796"], s4_private["S4_796"] = s4(D, F, np.arange(N_COLUMNS), chance)
        summary["zcode_falsifier"] = zcode_falsifier(D, B, F, inc, bank_rows)
        summary["offset_bins"]["included_294"] = offset_bins(D, inc)
    else:
        log(f"S1-S4 not computed: {len(inc)} < {MIN_INCLUDED} included columns (section 2.3)")
    summary["runtime_s"] = time.time() - t0                        # step 9
    write_private(D, E, samples, s4_private, inc, inputs)
    write_committed(summary, syn)
    log(f"wrote {OUT} (aggregates) and {PRIVATE_OUT} (per-column, not committed); "
        f"wall-clock {summary['runtime_s']:.1f}s")


if __name__ == "__main__":
    main()
