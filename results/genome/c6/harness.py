"""C6 harness: the exam a regenerating rule must pass, shipped with NO rule.

Specification: docs/plans/2026-09-23-c6-control-specification.md, sections 2-6, Amendment 1
(A1-A15) and Amendment 2 (A16-A22), judged against the acceptance criteria registered in
docs/plans/2026-09-23-c6-amendment-acceptance.md. The harness refuses to run if folds.csv no
longer matches folds.meta.json, if the spec's fold-time text (its first 41,349 bytes) changed,
or if either acceptance file changed (A23): amendments may only append.

Plug-in interface for a rule (A5). A rule is a Python file defining
    NAME            str
    PROGRAM_FILES   list of paths; the decode program, charged in full (lzma raw, A5). The last
                    file is the decode module; earlier files may be imported by it by stem name.
                    Only the standard library, numpy and those stems may be imported.
    fit(view)       the learner (uncharged). view.cells (n, 2) training cells as type indices
                    0-64, view.exists (n,) bool, view.content {(s, t): {"offsets": {(du, dv):
                    n_syn}, "sign": +-1}} for the training non-empty cells (in_json offsets only),
                    view.type_fields (65, 4) ints: stride_u, stride_v, role code, layout code.
                    Returns data: a dict of named numpy arrays (float, int, bool). An int array
                    whose name ends in "__sym<m>" is charged as symbols of an alphabet of size m.
    RANK            optional int, the dimension of the rule's per-type latent representation.
The decode module defines decode(data, type_fields, cells) -> {"p_exist": (n,), "offsets":
[{(du, dv): n_syn}], "sign": (n,)}. The harness re-executes the program from source before every
decode, casts every float array to float32, and hands it copies (A5).

Usage (from the repository root):
    tools/.venv/Scripts/python.exe results/genome/c6/harness.py --controls
    tools/.venv/Scripts/python.exe results/genome/c6/harness.py --rule path/to/rule.py
The second form exists for later use; this commit runs only the controls (A14).
"""

import argparse
import ast
import hashlib
import importlib.util
import json
import lzma
import math
import re
import sys
import time
import types as pytypes
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BANK_DIR = ROOT / "results" / "genome" / "bank"
DEC = HERE / "decoders"
SPEC = ROOT / "docs" / "plans" / "2026-09-23-c6-control-specification.md"

# ---- registered constants (spec + Amendment A15) -----------------------------------------
N_FOLDS = 10
CLIP = (0.001, 0.999)
TAU = 1e-9
LAMBDA = 1.0
NEWTON_TOL = 1e-8
N_SHUFFLES = 99
SWAPS_PER_EDGE = 20
RP_SEEDS = list(range(20))
RP_SEED_BASE = 1000
RP_RANK_CAP = 64
M18 = 18 * (65 + 65) * 32
DIAL_F = [0.0, 0.25, 0.5, 0.75, 1.0]
DIAL_SEEDS = 5
P1_MIN_WINS = 9
P1_MAX_LOSSES = 2
DNR_MAX = 5
FIELDS = ("existence", "offset", "counts", "sign")
LOWER_IS_BETTER = {"existence": True, "offset": False, "counts": True, "sign": False}


def sha256_lf(p):
    return hashlib.sha256(Path(p).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def id_hex(kind, name):
    return hashlib.sha256(f"cs-birth-v1|{kind}|{name}".encode()).hexdigest()[:12]


# ==========================================================================================
# 1. The bank, the folds
# ==========================================================================================
def read_csv(p):
    return pd.read_csv(p, skiprows=1, dtype=str, keep_default_na=False, encoding="utf-8")


FMETA = json.loads((HERE / "folds.meta.json").read_text(encoding="utf-8"))
if sha256_lf(HERE / "folds.csv") != FMETA["output"]["sha256_lf_normalised"]:
    sys.exit("REFUSED: folds.csv does not match folds.meta.json")
SPEC_FOLD_TIME_BYTES = 41349          # the spec's LF-normalised length when the folds were made
ACCEPTANCE = ROOT / "docs" / "plans" / "2026-09-23-c6-amendment-acceptance.md"
ACCEPTANCE_SHA = "bd3697719aa96a2d6c39078d7d01823009746de50b694debecc0f0d450b43d3b"
_spec_lf = SPEC.read_bytes().replace(b"\r\n", b"\n")
if hashlib.sha256(_spec_lf[:SPEC_FOLD_TIME_BYTES]).hexdigest() != FMETA["spec"]["sha256_lf_normalised"]:
    sys.exit("REFUSED: the C6 specification's fold-time text changed (amendments may only append)")
if sha256_lf(ACCEPTANCE) != ACCEPTANCE_SHA:
    sys.exit("REFUSED: the registered acceptance criteria changed")
ACCEPTANCE2 = ROOT / "docs" / "plans" / "2026-09-23-c6-amendment-acceptance-2.md"
ACCEPTANCE2_SHA = "4b6610e7ed30b6aaeccf6ea33008485fc3ec31a1869b93f74c78b7248f2e97f9"
if sha256_lf(ACCEPTANCE2) != ACCEPTANCE2_SHA:
    sys.exit("REFUSED: the registered acceptance criteria, part 2, changed")

T = read_csv(BANK_DIR / "types.csv")
T = T.sort_values("birth_id").reset_index(drop=True)          # A1: index by birth id order
NAMES = T.type_name.tolist()
IDX = {n: i for i, n in enumerate(NAMES)}
assert len(NAMES) == 65 and all(T.birth_id[i] == id_hex("type", n) for i, n in enumerate(NAMES))


def codes(col):
    u = sorted(set(col))
    return [u.index(x) for x in col]


TYPE_FIELDS = np.array([T.stride_u.astype(int), T.stride_v.astype(int), codes(T.role.tolist()),
                        codes(T.layout.tolist())]).T.astype(np.int64)
PAIR_ID = np.array([[id_hex("pair", f"{a}->{b}") for b in NAMES] for a in NAMES])

O = read_csv(BANK_DIR / "offsets.csv")
REAL_CONTENT = {}
for r in O.itertuples(index=False):
    if r.provenance == "dropped":
        continue
    k = (IDX[r.src], IDX[r.tar])
    c = REAL_CONTENT.setdefault(k, {"offsets": {}, "hull": [], "sign": int(r.sign)})
    if r.provenance == "in_json":
        c["offsets"][(int(r.du), int(r.dv))] = float(r.n_syn)
    else:
        c["hull"].append((int(r.du), int(r.dv)))
assert len(REAL_CONTENT) == 604 and sum(len(c["offsets"]) for c in REAL_CONTENT.values()) == 2117

F = read_csv(HERE / "folds.csv")
FOLD = np.full((65, 65), -1, dtype=int)
for r in F.itertuples(index=False):
    FOLD[IDX[r.src], IDX[r.tar]] = int(r.fold)
    assert r.pair_birth_id == PAIR_ID[IDX[r.src], IDX[r.tar]]
assert (FOLD >= 0).all()
ALL_CELLS = np.array([(s, t) for s in range(65) for t in range(65)], dtype=np.int64)


@dataclass
class Bank:
    name: str
    content: dict                      # (s, t) -> {"offsets", "hull", "sign"}
    exists: np.ndarray = None

    def __post_init__(self):
        self.exists = np.zeros((65, 65), bool)
        for (s, t) in self.content:
            self.exists[s, t] = True


REAL = Bank("real", REAL_CONTENT)


@dataclass
class View:
    type_fields: np.ndarray
    cells: np.ndarray
    exists: np.ndarray
    content: dict


def make_view(bank, train_mask):
    cells = ALL_CELLS[train_mask[ALL_CELLS[:, 0], ALL_CELLS[:, 1]]]
    ex = bank.exists[cells[:, 0], cells[:, 1]]
    content = {(int(s), int(t)): {"offsets": dict(bank.content[(s, t)]["offsets"]),
                                  "sign": bank.content[(s, t)]["sign"]}
               for s, t in cells[ex].tolist()}
    return View(TYPE_FIELDS.copy(), cells.copy(), ex.copy(), content)


# ==========================================================================================
# 2. Programs, data, description length (A5)
# ==========================================================================================
_STDLIB = set(sys.stdlib_module_names)


def check_imports(files):
    stems = {Path(f).stem for f in files}
    for f in files:
        tree = ast.parse(Path(f).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            mods = []
            if isinstance(node, ast.Import):
                mods = [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    raise ValueError(f"{f}: relative import")
                mods = [node.module.split(".")[0]]
            for m in mods:
                if m not in _STDLIB and m != "numpy" and m not in stems:
                    raise ValueError(f"{f}: import of {m} is not allowed (A5)")


def program_bits(files):
    src = b"".join(Path(f).read_bytes().replace(b"\r\n", b"\n") for f in files)
    comp = lzma.compress(src, format=lzma.FORMAT_RAW,
                         filters=[{"id": lzma.FILTER_LZMA2, "preset": 9 | lzma.PRESET_EXTREME}])
    return 8 * len(comp)


_CODE = {}


def load_program(files):
    """Fresh module objects, executed from source, every call (A5: no state survives)."""
    mod = None
    added = []
    try:
        for f in files:
            f = Path(f)
            if f not in _CODE:
                _CODE[f] = compile(f.read_text(encoding="utf-8"), str(f), "exec")
            mod = pytypes.ModuleType(f.stem)
            sys.modules[f.stem] = mod
            added.append(f.stem)
            exec(_CODE[f], mod.__dict__)
    finally:
        for s in added:
            sys.modules.pop(s, None)
    return mod


def gamma_bits(n):
    n = np.asarray(n, dtype=np.int64)
    assert (n >= 1).all()
    return int(np.sum(2 * np.floor(np.log2(n.astype(np.float64))).astype(np.int64) + 1))


def int_bits(x):
    x = np.asarray(x, dtype=np.int64)
    z = np.where(x >= 0, 2 * x, -2 * x - 1)
    return gamma_bits(z + 1) if x.size else 0


def data_bits(data):
    bits = 0
    for name, arr in data.items():
        arr = np.asarray(arr)
        bits += 8 * len(name) + int_bits(np.array([arr.ndim] + list(arr.shape)))
        m = re.search(r"__sym(\d+)$", name)
        if m:
            assert arr.dtype.kind in "iu"
            bits += math.ceil(math.log2(int(m.group(1)))) * arr.size if int(m.group(1)) > 1 else 0
        elif arr.dtype.kind == "b":
            bits += arr.size
        elif arr.dtype.kind in "iu":
            bits += int_bits(arr.ravel())
        elif arr.dtype.kind == "f":
            bits += 32 * arr.size
        else:
            raise TypeError(f"{name}: dtype {arr.dtype} is not allowed (A5)")
    return bits


def cast(data):
    out = {}
    for k, v in data.items():
        v = np.asarray(v)
        out[k] = v.astype(np.float32).astype(np.float64) if v.dtype.kind == "f" else v.copy()
    return out


@dataclass
class Predictor:
    name: str
    program_files: list
    fit: Callable
    rank: Optional[int] = None
    needs_bank: bool = False           # the oracle only: fit(view, bank, held_out_cells)

    def __post_init__(self):
        check_imports(self.program_files)
        self.prog_bits = program_bits(self.program_files)

    def train(self, bank, train_mask):
        view = make_view(bank, train_mask)
        return self.fit(view, bank) if self.needs_bank else self.fit(view)

    def decode(self, data, cells):
        mod = load_program(self.program_files)
        return mod.decode(cast(data), TYPE_FIELDS.copy(), np.asarray(cells).copy())

    def dl(self, data):
        return self.prog_bits + data_bits(data)


# ==========================================================================================
# 3. Learners of the built-in predictors (uncharged)
# ==========================================================================================
def ridge_logistic(X, y, offset, pen, lam=LAMBDA):
    w = np.zeros(X.shape[1])
    for _ in range(200):
        p = 1.0 / (1.0 + np.exp(-(X @ w + offset)))
        g = X.T @ (p - y) + lam * pen * w
        if np.linalg.norm(g) < NEWTON_TOL:
            return w
        H = X.T @ (X * (p * (1 - p))[:, None]) + lam * np.diag(pen)
        w = w - np.linalg.solve(H, g)
    raise RuntimeError("Newton did not converge")


def most_frequent_set(sets):
    """A4 tie rule: most frequent; then smaller set; then lexicographically smaller list."""
    c = Counter(tuple(sorted(s)) for s in sets)
    return min(c, key=lambda k: (-c[k], len(k), k))


def training_rows(view):
    return [(s, t, o, math.log1p(n)) for (s, t), c in view.content.items()
            for o, n in c["offsets"].items()]


def fit_n0(view):
    sets = [c["offsets"].keys() for c in view.content.values()]
    n0 = most_frequent_set(sets)
    rows = training_rows(view)
    med = [float(np.median([v for (_, _, o, v) in rows if o == oo])) for oo in n0]
    signs = [c["sign"] for c in view.content.values()]
    maj = 1 if sum(x == 1 for x in signs) >= sum(x == -1 for x in signs) else -1
    return {"p0": np.array([view.exists.mean()]),
            "n0_du": np.array([o[0] for o in n0], dtype=np.int64),
            "n0_dv": np.array([o[1] for o in n0], dtype=np.int64),
            "n0_cnt": np.array(med), "n0_sign__sym2": np.array([1 if maj == 1 else 0])}


def fit_n1(view):
    n0 = fit_n0(view)
    s, t = view.cells[:, 0], view.cells[:, 1]
    X = np.zeros((len(s), 131))
    X[:, 0] = 1
    X[np.arange(len(s)), 1 + s] = 1
    X[np.arange(len(s)), 66 + t] = 1
    pen = np.ones(131)
    pen[0] = 0
    w = ridge_logistic(X, view.exists.astype(float), np.zeros(len(s)), pen)
    # offset sets per source type
    set_has = np.zeros(65, bool)
    set_len = np.zeros(65, np.int64)
    du, dv = [], []
    for si in range(65):
        sets = [c["offsets"].keys() for (a, _), c in view.content.items() if a == si]
        if sets:
            best = most_frequent_set(sets)
            set_has[si], set_len[si] = True, len(best)
            du += [o[0] for o in best]
            dv += [o[1] for o in best]
    # counts: m_o + alpha_s + beta_t on log1p
    rows = training_rows(view)
    by_o = {}
    for (_, _, o, v) in rows:
        by_o.setdefault(o, []).append(v)
    m = {o: float(np.mean(v)) for o, v in by_o.items()}
    r1 = {}
    for (a, _, o, v) in rows:
        r1.setdefault(a, []).append(v - m[o])
    alpha = np.zeros(65)
    for a, v in r1.items():
        alpha[a] = np.mean(v)
    r2 = {}
    for (a, b, o, v) in rows:
        r2.setdefault(b, []).append(v - m[o] - alpha[a])
    beta = np.zeros(65)
    for b, v in r2.items():
        beta[b] = np.mean(v)
    mo = sorted(m)
    # sign per source: 0 = -1, 1 = +1, 2 = fall back to N0
    sym = np.full(65, 2, dtype=np.int64)
    for si in range(65):
        sg = [c["sign"] for (a, _), c in view.content.items() if a == si]
        pos, neg = sum(x == 1 for x in sg), sum(x == -1 for x in sg)
        if pos > neg:
            sym[si] = 1
        elif neg > pos:
            sym[si] = 0
    return {"ex_c": w[:1], "ex_a": w[1:66], "ex_b": w[66:131],
            "set_has": set_has, "set_len": set_len,
            "set_du": np.array(du, dtype=np.int64), "set_dv": np.array(dv, dtype=np.int64),
            "n0_du": n0["n0_du"], "n0_dv": n0["n0_dv"],
            "m_du": np.array([o[0] for o in mo], dtype=np.int64),
            "m_dv": np.array([o[1] for o in mo], dtype=np.int64),
            "m_val": np.array([m[o] for o in mo]),
            "m_all": np.array([float(np.mean([v for *_, v in rows]))]),
            "cnt_a": alpha, "cnt_b": beta,
            "src_sign__sym3": sym, "n0_sign__sym2": n0["n0_sign__sym2"]}


def store_data(content, cells):
    """A5 storage format for the given non-empty cells, in the given order."""
    addr, sign, noff, du, dv, nn = [], [], [], [], [], []
    for (s, t) in cells:
        c = content[(s, t)]
        addr.append(s * 65 + t)
        sign.append(c["sign"] == 1)
        offs = sorted(c["offsets"])
        noff.append(len(offs))
        du += [o[0] for o in offs]
        dv += [o[1] for o in offs]
        nn += [c["offsets"][o] for o in offs]
    return {"cell_addr__sym4225": np.array(addr, dtype=np.int64),
            "cell_sign": np.array(sign, dtype=bool), "cell_noff": np.array(noff, dtype=np.int64),
            "off_du": np.array(du, dtype=np.int64), "off_dv": np.array(dv, dtype=np.int64),
            "off_n": np.array(nn, dtype=np.float64)}


def dk_order(content):
    """A6: decreasing total in_json n_syn, ties by pair birth id."""
    return sorted(content, key=lambda k: (-math.fsum(content[k]["offsets"].values()),
                                          PAIR_ID[k[0], k[1]]))


def fit_dk(view, k):
    d = fit_n1(view)
    d.update(store_data(view.content, dk_order(view.content)[:k]))
    return d


def fit_oracle(view, bank):
    return store_data(bank.content, sorted(bank.content))


def rp_fit(view, r, seed, side, n1=None):
    n1 = fit_n1(view) if n1 is None else n1
    rng = np.random.Generator(np.random.PCG64(int(seed)))
    G = rng.normal(0.0, np.sqrt(1.0 / r), size=(65, r))
    c1 = cast(n1)
    s, t = view.cells[:, 0], view.cells[:, 1]
    off = c1["ex_c"][0] + c1["ex_a"][s] + c1["ex_b"][t]
    y = view.exists.astype(float)
    rnd, grp = (s, t) if side == 0 else (t, s)
    B = np.zeros((65, r))
    for g in range(65):
        m = grp == g
        if m.any():
            B[g] = ridge_logistic(G[rnd[m]], y[m], off[m], np.ones(r))
    # counts: ridge least squares on N1's per-row residuals (descriptive, A11)
    m_o = {(a, b): v for a, b, v in zip(c1["m_du"].tolist(), c1["m_dv"].tolist(),
                                        c1["m_val"].tolist())}
    Bc = np.zeros((65, r))
    rows = training_rows(view)
    for g in range(65):
        sel = [(a, b, o, v) for (a, b, o, v) in rows if (b if side == 0 else a) == g]
        if not sel:
            continue
        Xg = np.array([G[a if side == 0 else b] for (a, b, _, _) in sel])
        yg = np.array([v - m_o.get(o, c1["m_all"][0]) - c1["cnt_a"][a] - c1["cnt_b"][b]
                       for (a, b, o, v) in sel])
        Bc[g] = np.linalg.solve(Xg.T @ Xg + LAMBDA * np.eye(r), Xg.T @ yg)
    d = dict(n1)
    d.update({"rp_seed": np.array([seed], dtype=np.int64),
              "rp_side__sym2": np.array([side], dtype=np.int64), "rp_B": B, "rp_Bc": Bc})
    return d


N1 = Predictor("N1", [DEC / "n1_decode.py"], fit_n1)
N0 = Predictor("N0", [DEC / "n0_decode.py"], fit_n0)
STORE_FILES = [DEC / "store_decode.py"]
DK_FILES = [DEC / "n1_decode.py", DEC / "store_decode.py", DEC / "dk_decode.py"]
RP_FILES = [DEC / "n1_decode.py", DEC / "rp_decode.py"]
DK = Predictor("D_k", DK_FILES, lambda v: fit_dk(v, 0))
S_ALL = Predictor("S_all", STORE_FILES, lambda v, b: fit_oracle(v, b), needs_bank=True)


# ==========================================================================================
# 4. Scoring (spec 4.1 table, A3, A4 clipping, A7 ties)
# ==========================================================================================
def score(pred, bank, cells):
    cells = np.asarray(cells)
    y = bank.exists[cells[:, 0], cells[:, 1]]
    p = np.clip(np.asarray(pred["p_exist"], float), *CLIP)
    ll = float(np.mean(-(y * np.log(p) + (~y) * np.log(1 - p))))
    jac, err, sign_ok = [], [], 0
    for i in np.flatnonzero(y):
        c = bank.content[(int(cells[i, 0]), int(cells[i, 1]))]
        po = pred["offsets"][i]
        a, b = set(po), set(c["offsets"])
        jac.append(len(a & b) / len(a | b) if (a | b) else 1.0)
        for o, n in c["offsets"].items():
            # harness convention (HARNESS-CONTROLS.md): a predicted count below 0 is read as 0
            err.append(abs(math.log1p(n) - math.log1p(max(po.get(o, 0.0), 0.0))))
        sign_ok += int(pred["sign"][i]) == c["sign"]
    n_ne = int(y.sum())
    return {"existence": ll, "offset": float(np.mean(jac)) if jac else float("nan"),
            "counts": float(np.mean(err)) if err else float("nan"),
            "sign": sign_ok / n_ne if n_ne else float("nan"), "sign_n": sign_ok, "n_ne": n_ne}


def cmp(a, b, f):
    """+1 if score a beats score b on field f, -1 if worse, 0 tie (A7)."""
    if f == "sign":
        return int(np.sign(a["sign_n"] - b["sign_n"]))
    d = (b[f] - a[f]) if LOWER_IS_BETTER[f] else (a[f] - b[f])
    return 1 if d > TAU else (-1 if d < -TAU else 0)


def margin(rule_scores, null_scores, f):
    """Mean over folds of the rule's advantage over the null, signed larger = better."""
    d = [(n[f] - r[f]) if LOWER_IS_BETTER[f] else (r[f] - n[f])
         for r, n in zip(rule_scores, null_scores)]
    return float(np.mean(d))




# ==========================================================================================
# 5. New opponents of Amendment 2: armed D_k (A17), N_EB (A18), BF_r (A19)
# ==========================================================================================
DK0_FILES = [DEC / "n0_decode.py", DEC / "store_decode.py", DEC / "dk0_decode.py"]
BF_FILES = [DEC / "n1_decode.py", DEC / "bf_decode.py"]
DK0 = Predictor("D_k armed", DK0_FILES, lambda v: fit_dk0(v, 0))
EB_ALPHAS = [0.5, 1, 2, 4, 8, 16, 32, 64, 128]
BF_LAMBDAS = [1, 3, 10, 30, 100]
BF_SWEEPS = 25
BF_NEWTON_ITERS = 20
BF_TOL = 1e-6
R3_MIN_CELLS = 5
A5_MAX_RATIO = 0.25
M3_CONTROL = 0.4465
DL_BANK_REAL_REGISTERED = 94812


def fit_dk0(view, k):
    d = fit_n0(view)
    d.update(store_data(view.content, dk_order(view.content)[:k]))
    return d


def inner_folds(view):
    return FOLD[view.cells[:, 0], view.cells[:, 1]]


def subview(view, keep):
    cells = view.cells[keep]
    ex = view.exists[keep]
    content = {(int(s), int(t)): view.content[(int(s), int(t))] for s, t in cells[ex].tolist()}
    return View(view.type_fields, cells, ex, content)


# ---- N_EB: smoothed per-source offset-set distribution, expected-Jaccard optimal set -----
def _set_key(s):
    return (len(s), s)


def eb_tables(view):
    """Distinct offset sets of the view's non-empty cells, and their pairwise Jaccard."""
    keys = sorted(view.content)
    sets = [tuple(sorted(view.content[k]["offsets"])) for k in keys]
    uniq = sorted(set(sets), key=_set_key)
    sid = {s: i for i, s in enumerate(uniq)}
    offs = sorted({o for s in uniq for o in s})
    oid = {o: i for i, o in enumerate(offs)}
    X = np.zeros((len(uniq), len(offs)))
    for i, s in enumerate(uniq):
        X[i, [oid[o] for o in s]] = 1
    inter = X @ X.T
    size = X.sum(1)
    union = size[:, None] + size[None, :] - inter
    J = np.where(union > 0, inter / np.maximum(union, 1), 1.0)
    cell_sid = np.array([sid[s] for s in sets])
    cell_src = np.array([k[0] for k in keys])
    cell_fold = FOLD[[k[0] for k in keys], [k[1] for k in keys]]
    return uniq, J, cell_sid, cell_src, cell_fold


def eb_choose(J, cell_sid, cell_src, train, alpha):
    """Per source: argmax over observed training sets of expected Jaccard under
    p_s = (c_s + alpha g) / (n_s + alpha). Ties: smaller set, then lexicographic (A4) --
    the set ids are already in that order, so the first maximum wins."""
    tr_sid, tr_src = cell_sid[train], cell_src[train]
    cand = np.unique(tr_sid)
    g = np.bincount(tr_sid, minlength=J.shape[0])[cand] / len(tr_sid)
    Jc = J[np.ix_(cand, cand)]
    choice = np.zeros(65, dtype=int)
    for s in range(65):
        m = tr_src == s
        c = np.bincount(tr_sid[m], minlength=J.shape[0])[cand]
        p = (c + alpha * g) / (m.sum() + alpha)
        ej = Jc @ p
        choice[s] = cand[int(np.flatnonzero(ej >= ej.max() - 1e-12)[0])]
    return choice


def fit_neb(view):
    uniq, J, cell_sid, cell_src, cell_fold = eb_tables(view)
    folds = sorted(set(cell_fold.tolist()))
    best, best_alpha = -1.0, None
    for alpha in EB_ALPHAS:                                   # A18: nested choice of alpha
        tot, n = 0.0, 0
        for f in folds:
            train, test = cell_fold != f, cell_fold == f
            if not test.any() or not train.any():
                continue
            ch = eb_choose(J, cell_sid, cell_src, train, alpha)
            tot += J[ch[cell_src[test]], cell_sid[test]].sum()
            n += int(test.sum())
        score_a = tot / n
        if score_a >= best - 1e-12:                           # ties go to the larger alpha
            best, best_alpha = score_a, alpha
    ch = eb_choose(J, cell_sid, cell_src, np.ones(len(cell_sid), bool), best_alpha)
    d = fit_n1(view)
    du, dv, ln = [], [], []
    for s in range(65):
        st = uniq[ch[s]]
        ln.append(len(st))
        du += [o[0] for o in st]
        dv += [o[1] for o in st]
    d.update({"set_has": np.ones(65, bool), "set_len": np.array(ln, dtype=np.int64),
              "set_du": np.array(du, dtype=np.int64), "set_dv": np.array(dv, dtype=np.int64),
              "eb_alpha": np.array([float(best_alpha)])})
    return d


NEB = Predictor("N_EB", [DEC / "n1_decode.py"], fit_neb)


# ---- BF_r: trained bilinear factorisation on the existence logit -------------------------
def _sig(z):
    return 1.0 / (1.0 + np.exp(-z))


def _newton_rows(O, Y, M, V, U, lam):
    r = U.shape[1]
    for _ in range(BF_NEWTON_ITERS):
        P = _sig(O + U @ V.T)
        G = ((P - Y) * M) @ V + lam * U
        if np.sqrt((G ** 2).sum(1)).max() < BF_TOL:
            break
        W = M * P * (1 - P)
        H = np.einsum("st,tk,tl->skl", W, V, V) + lam * np.eye(r)
        U = U - np.linalg.solve(H, G[..., None])[..., 0]
    return U


def bf_als(O, Y, M, r, lam):
    E = np.where(M > 0, Y - _sig(O), 0.0)
    u, sv, vt = np.linalg.svd(E)
    U = u[:, :r] * np.sqrt(sv[:r])
    V = vt[:r].T * np.sqrt(sv[:r])
    for _ in range(BF_SWEEPS):
        U = _newton_rows(O, Y, M, V, U, lam)
        V = _newton_rows(O.T, Y.T, M.T, U, V, lam)
    return U, V


def _n1_logit_grid(n1data):
    c = cast(n1data)
    return c["ex_c"][0] + c["ex_a"][:, None] + c["ex_b"][None, :]


def _grid(view):
    M = np.zeros((65, 65))
    Y = np.zeros((65, 65))
    M[view.cells[:, 0], view.cells[:, 1]] = 1
    Y[view.cells[:, 0], view.cells[:, 1]] = view.exists
    return M, Y


def fit_bf(view, r):
    n1 = fit_n1(view)
    M, Y = _grid(view)
    folds = sorted(set(inner_folds(view).tolist()))
    ll = {lam: 0.0 for lam in BF_LAMBDAS}
    for f in folds:                                           # A19: nested choice of lambda
        keep = inner_folds(view) != f
        sv_ = subview(view, keep)
        Oi = _n1_logit_grid(fit_n1(sv_))
        Mi, _ = _grid(sv_)
        test = np.zeros((65, 65), bool)
        hc = view.cells[~keep]
        test[hc[:, 0], hc[:, 1]] = True
        for lam in BF_LAMBDAS:
            U, V = bf_als(Oi, Y, Mi, r, lam)
            p = np.clip(_sig(Oi + U @ V.T), *CLIP)
            ll[lam] += float(np.sum(np.where(Y > 0, np.log(p), np.log(1 - p))[test]))
    best = max(ll.values())
    lam = max(l for l in BF_LAMBDAS if ll[l] >= best - 1e-9)   # ties go to the larger lambda
    U, V = bf_als(_n1_logit_grid(n1), Y, M, r, lam)
    n1.update({"bf_U": U, "bf_V": V, "bf_lambda": np.array([float(lam)])})
    return n1


def bf_predictor(r):
    return Predictor(f"BF_r{r}", BF_FILES, lambda v: fit_bf(v, r), rank=r)


# ==========================================================================================
# 6. The arms
# ==========================================================================================
_CV_CACHE = {}


def cv(pred, bank, cache_key=None):
    key = (pred.name, bank.name, cache_key or "primary")
    if key in _CV_CACHE:
        return _CV_CACHE[key]
    out, datas = [], []
    for f in range(N_FOLDS):
        held = FOLD == f
        cells = ALL_CELLS[held[ALL_CELLS[:, 0], ALL_CELLS[:, 1]]]
        data = pred.train(bank, ~held)
        s = score(pred.decode(data, cells), bank, cells)
        for k in ("eb_alpha", "bf_lambda"):
            if k in data:
                s[k] = float(np.asarray(data[k])[0])
        out.append(s)
    _CV_CACHE[key] = out
    return out


_IS_CACHE = {}


def insample(pred, bank):
    key = (pred.name, bank.name)
    if key not in _IS_CACHE:
        data = pred.train(bank, np.ones((65, 65), bool))
        _IS_CACHE[key] = (data, score(pred.decode(data, ALL_CELLS), bank, ALL_CELLS))
    return _IS_CACHE[key]


def p1(rule_s, n1_s, n0_s, neb_s):
    res = {"existence": {"wins": int(sum(cmp(r, n, "existence") == 1
                                         for r, n in zip(rule_s, n1_s)))}}
    res["existence"]["pass"] = res["existence"]["wins"] >= P1_MIN_WINS
    # A18: the offset set must beat EACH of N1, N0 and N_EB in >= 9 of 10 folds
    w = {nm: int(sum(cmp(r, n, "offset") == 1 for r, n in zip(rule_s, ns)))
         for nm, ns in (("N1", n1_s), ("N0", n0_s), ("N_EB", neb_s))}
    res["offset"] = {"wins_vs": w, "wins": min(w.values()),
                     "pass": all(v >= P1_MIN_WINS for v in w.values())}
    for f in ("counts", "sign"):
        losses = sum(cmp(r, n, f) == -1 for r, n in zip(rule_s, n1_s))
        if f == "sign":
            mean_ok = sum(r["sign_n"] for r in rule_s) >= sum(n["sign_n"] for n in n1_s)
        else:
            mean_ok = np.mean([r[f] for r in rule_s]) <= np.mean([n[f] for n in n1_s]) + TAU
        res[f] = {"losses": int(losses), "mean_not_worse": bool(mean_ok),
                  "pass": bool(losses <= P1_MAX_LOSSES and mean_ok)}
    res["pass"] = all(res[f]["pass"] for f in FIELDS)
    return res


def did_not_run(rule_s, n0_s):
    beaten = {f: int(sum(cmp(n, r, f) == 1 for r, n in zip(rule_s, n0_s))) for f in FIELDS}
    return {"folds_where_N0_beats_rule": beaten,
            "did_not_run": any(v > DNR_MAX for v in beaten.values())}


def _k_star(budget, base, dlfun, order):
    if dlfun(0) > budget:
        return 0
    lo, hi = 0, len(order)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if dlfun(mid) <= budget:
            lo = mid
        else:
            hi = mid - 1
    return lo


def k_star(budget, n1_full, content):
    order = dk_order(content)

    def f(k):
        d = dict(n1_full)
        d.update(store_data(content, order[:k]))
        return DK.dl(d)
    return _k_star(budget, n1_full, f, order)


def k_star_armed(budget, n0_full, content):
    order = dk_order(content)

    def f(k):
        d = dict(n0_full)
        d.update(store_data(content, order[:k]))
        return DK0.dl(d)
    return _k_star(budget, n0_full, f, order)


def dl_bank(bank):
    d, _ = insample(S_ALL, bank)
    return S_ALL.dl(d)


def p2(pred, bank):
    data, s_rule = insample(pred, bank)
    dl_rule = pred.dl(data)
    dlb = dl_bank(bank)
    n1_full, s_n1 = insample(N1, bank)
    n0_full, _ = insample(N0, bank)
    ks = k_star(dl_rule, n1_full, bank.content)
    ka = k_star_armed(dl_rule, n0_full, bank.content)
    k18 = k_star(M18, n1_full, bank.content)
    dk = Predictor(f"D_{ks}", DK_FILES, lambda v: fit_dk(v, ks))
    dk_data, s_dk = insample(dk, bank)
    dka = Predictor(f"D0_{ka}", DK0_FILES, lambda v: fit_dk0(v, ka))
    dka_data, s_dka = insample(dka, bank)
    beats = {"dk_star": {f: cmp(s_rule, s_dk, f) == 1 for f in ("existence", "offset")},
             "dk_armed": {f: cmp(s_rule, s_dka, f) == 1 for f in ("existence", "offset")},
             "n1_insample": {f: cmp(s_rule, s_n1, f) == 1 for f in ("existence", "offset")}}
    length_ok = dl_rule <= dlb / 10
    all_beats = all(all(v.values()) for v in beats.values())
    return {"dl_rule_bits": dl_rule, "dl_rule_program_bits": pred.prog_bits,
            "dl_bank_bits": dlb, "dl_bank_over_10": dlb / 10,
            "k_star": ks, "dl_dk_star_bits": DK.dl(dk_data),
            "k_star_armed": ka, "dl_dk_armed_bits": DK0.dl(dka_data),
            "M18_bits": M18, "k18": k18,
            "insample_rule": s_rule, "insample_dk_star": s_dk, "insample_dk_armed": s_dka,
            "insample_n1": s_n1, "length_ok": bool(length_ok),
            "beats": {k: {f: bool(x) for f, x in v.items()} for k, v in beats.items()},
            "below_M18": bool(dl_rule < M18), "all_opponents_beaten": bool(all_beats),
            "pass": bool(length_ok and all_beats)}


# ---- shuffled banks (A10) and the dial (A12), for any base bank ------------------------
def rewire_and_permute(bank, rng, frac=1.0):
    edges = sorted(bank.content)
    n = len(edges)
    if frac >= 1.0:
        chosen = np.arange(n)
    else:
        chosen = np.sort(rng.choice(n, size=int(round(frac * n)), replace=False))
    occ = bank.exists.copy()
    E = [edges[i] for i in chosen]
    target = SWAPS_PER_EDGE * len(E)
    cap = 100 * target
    succ = att = 0
    while len(E) >= 2 and succ < target and att < cap:
        att += 1
        i, j = rng.integers(len(E), size=2)
        if i == j:
            continue
        (s1, t1), (s2, t2) = E[i], E[j]
        if s1 == s2 or t1 == t2 or occ[s1, t2] or occ[s2, t1]:
            continue
        occ[s1, t1] = occ[s2, t2] = False
        occ[s1, t2] = occ[s2, t1] = True
        E[i], E[j] = (s1, t2), (s2, t1)
        succ += 1
    perm = rng.permutation(len(E))
    chosen_set = set(chosen.tolist())
    content = {e: bank.content[e] for i, e in enumerate(edges) if i not in chosen_set}
    for i, e in enumerate(E):
        content[e] = bank.content[edges[chosen[perm[i]]]]
    return content, succ, att


def canon_content(c):
    return (tuple(sorted(c["offsets"].items())), tuple(sorted(c["hull"])), c["sign"])


def shuffled_bank(base, seed):
    rng = np.random.Generator(np.random.PCG64(seed))
    content, succ, att = rewire_and_permute(base, rng, 1.0)
    b = Bank(f"{base.name}.shuffle{seed}", content)
    ne = len(base.content)
    inv = {
        "n_nonempty": int(b.exists.sum()),
        "out_degrees_kept": bool((b.exists.sum(1) == base.exists.sum(1)).all()),
        "in_degrees_kept": bool((b.exists.sum(0) == base.exists.sum(0)).all()),
        "content_multiset_kept": sorted(map(canon_content, b.content.values()))
        == sorted(map(canon_content, base.content.values())),
        "successful_swaps": succ, "attempts": att, "target_swaps": SWAPS_PER_EDGE * ne,
        "cells_changed": int((b.exists != base.exists).sum() // 2),
    }
    return b, inv


def dial_banks(base):
    out = []
    for fi in range(len(DIAL_F)):
        for sd in range(DIAL_SEEDS):
            if DIAL_F[fi] == 0.0:
                out.append((fi, sd, Bank(f"{base.name}.dial0_{sd}", base.content)))
                continue
            rng = np.random.Generator(np.random.PCG64(10000 + 100 * fi + sd))
            content, _, _ = rewire_and_permute(base, rng, DIAL_F[fi])
            out.append((fi, sd, Bank(f"{base.name}.dial{fi}_{sd}", content)))
    return out


# ---- P4: the old random-projection threshold, and the trained factorisation (A19) -------
def rank_of(pred, data_full):
    if pred.rank:
        return min(pred.rank, RP_RANK_CAP)
    n_real = sum(np.asarray(v).size for v in data_full.values() if np.asarray(v).dtype.kind == "f")
    return int(min(max(1, round(n_real / 130)), RP_RANK_CAP))


def rp_predictor(r, seed, side):
    return Predictor(f"RP_r{r}_s{seed}_side{side}", RP_FILES,
                     lambda v: rp_fit(v, r, seed, side), rank=r)


def rp_margins(r, bank):
    n1s = cv(N1, bank)
    out = []
    for j in RP_SEEDS:
        m = [margin(cv(rp_predictor(r, RP_SEED_BASE + j, side), bank), n1s, "existence")
             for side in (0, 1)]
        out.append({"seed": RP_SEED_BASE + j, "margin": max(m)})
    return out


def bf_margin(r, bank):
    s = cv(bf_predictor(r), bank)
    return {"rank": r, "margin": margin(s, cv(N1, bank), "existence"),
            "lambdas": [x["bf_lambda"] for x in s],
            "folds_beating_N1": int(sum(cmp(a, b, "existence") == 1
                                        for a, b in zip(s, cv(N1, bank))))}


# ---- secondary split: leave one type out (spec 4.5, descriptive) --------------------------
def loto(pred, bank):
    rs, ns = [], []
    for i in range(65):
        held = np.zeros((65, 65), bool)
        held[i, :] = held[:, i] = True
        cells = ALL_CELLS[held[ALL_CELLS[:, 0], ALL_CELLS[:, 1]]]
        for P, acc in ((pred, rs), (N1, ns)):
            d = P.train(bank, ~held)
            acc.append(score(P.decode(d, cells), bank, cells))
    return {f: {"rule_mean": float(np.nanmean([r[f] for r in rs])),
                "n1_mean": float(np.nanmean([n[f] for n in ns]))} for f in FIELDS}


# ==========================================================================================
# 7. The whole exam for one predictor on one bank
# ==========================================================================================
@dataclass
class Env:
    bank: Bank
    shuffled: list
    dial: list


def run_exam(pred, env, log=print):
    t0 = time.time()
    bank = env.bank
    rule_s, n1_s, n0_s = cv(pred, bank), cv(N1, bank), cv(N0, bank)
    neb_s = cv(NEB, bank)
    r1 = p1(rule_s, n1_s, n0_s, neb_s)
    dnr = did_not_run(rule_s, n0_s)
    r2 = p2(pred, bank)
    real_m = {f: margin(rule_s, n1_s, f) for f in FIELDS}
    sh_m = {f: [] for f in FIELDS}
    for b in env.shuffled:
        rs, ns = cv(pred, b), cv(N1, b)
        for f in FIELDS:
            sh_m[f].append(margin(rs, ns, f))
    r3 = {f: {"real_margin": real_m[f], "shuffled_max": float(np.max(sh_m[f])),
              "shuffled_mean": float(np.mean(sh_m[f])),
              "n_shuffled_ge_real": int(sum(m >= real_m[f] for m in sh_m[f])),
              "strictly_above_all": bool(all(real_m[f] > m for m in sh_m[f]))} for f in FIELDS}
    r3["pass"] = r3["existence"]["strictly_above_all"] and r3["offset"]["strictly_above_all"]
    full_data, _ = insample(pred, bank)
    r = rank_of(pred, full_data)
    rpm = rp_margins(r, bank)
    rp_thr = max(x["margin"] for x in rpm)
    bfm = bf_margin(r, bank)
    thr = max(rp_thr, bfm["margin"])
    r4 = {"rank": r, "rule_margin_existence": real_m["existence"], "rp_threshold": rp_thr,
          "bf": bfm, "threshold": thr, "pass": bool(real_m["existence"] > thr)}
    dial_out = []
    dks = Predictor(f"D_{r2['k_star']}", DK_FILES, lambda v: fit_dk(v, r2["k_star"]))
    dka = Predictor(f"D0_{r2['k_star_armed']}", DK0_FILES,
                    lambda v: fit_dk0(v, r2["k_star_armed"]))
    for (fi, sd, b) in env.dial:
        rs, ns = cv(pred, b), cv(N1, b)
        _, s_rule = insample(pred, b)
        _, s_dk = insample(dks, b)
        _, s_dka = insample(dka, b)
        dial_out.append({"f": DIAL_F[fi], "seed": sd,
                         "heldout_margin_over_N1": {f: margin(rs, ns, f) for f in FIELDS},
                         "insample_margin_over_Dk_star": {f: margin([s_rule], [s_dk], f)
                                                          for f in FIELDS},
                         "insample_margin_over_Dk_armed": {f: margin([s_rule], [s_dka], f)
                                                           for f in FIELDS}})
    lo = loto(pred, bank)
    labels = []
    if dnr["did_not_run"]:
        labels.append("rule did not run")
    if not r1["pass"]:
        labels.append("copy or marginal")
    if not r2["length_ok"]:
        labels.append("not a bottleneck")
    if not r2["all_opponents_beaten"]:
        labels.append("below threshold for this family")
    if not r3["pass"]:
        labels.append("family fits anything")
    if not r4["pass"]:
        labels.append("ambient, not substantive structure")
    verdict = "PASS" if not labels else "FAIL"
    log(f"  [{pred.name} on {bank.name}] {verdict} {labels} ({time.time() - t0:.0f}s)")
    return {"name": pred.name, "bank": bank.name,
            "program_files": [str(Path(f).relative_to(ROOT).as_posix())
                              for f in pred.program_files],
            "per_fold_rule": rule_s, "per_fold_N1": n1_s, "per_fold_N0": n0_s,
            "per_fold_N_EB": neb_s, "P1": r1, "did_not_run": dnr, "P2": r2, "P3": r3, "P4": r4,
            "dial": dial_out, "loto": lo, "labels": labels, "verdict": verdict}


# ==========================================================================================
# 8. The planted generator and the planted rule (acceptance file, section (a))
# ==========================================================================================
PL_SEED = 4242
PL_SCRAMBLE_SEED = 99
PL_D = 0.1425


def planted_banks():
    rng = np.random.Generator(np.random.PCG64(PL_SEED))
    pi = rng.permutation(65)
    cls = np.zeros(65, dtype=np.int64)
    for j, i in enumerate(pi):
        cls[i] = j % 4
    U_ex = rng.random((65, 65))
    real_cells = sorted(REAL_CONTENT)
    tmpl_idx = rng.choice(len(real_cells), size=16, replace=False)
    sig = np.where(rng.random(4) < 0.62, 1, -1)
    u = rng.random((65, 65))
    pool = rng.integers(len(real_cells), size=(65, 65))
    delta = np.array([[1 if b == (a + 1) % 4 else -1 for b in range(4)] for a in range(4)])
    p_delta = np.where(delta == 1, 0.45, 0.04)
    templates = []
    for q in range(16):
        c = REAL_CONTENT[real_cells[tmpl_idx[q]]]
        mu = float(np.mean([math.log1p(n) for n in c["offsets"].values()]))
        templates.append((sorted(c["offsets"]), mu))
    banks = {}
    for rho, nm in ((1.0, "PL1"), (0.5, "PL05"), (0.0, "PL0")):
        p = PL_D + rho * (p_delta - PL_D)
        content = {}
        for s in range(65):
            for t in range(65):
                a, b = cls[s], cls[t]
                if U_ex[s, t] >= p[a, b]:
                    continue
                if u[s, t] < rho:
                    offs, mu = templates[a * 4 + b]
                    content[(s, t)] = {"offsets": {o: math.expm1(mu) for o in offs},
                                       "hull": [], "sign": int(sig[a])}
                else:
                    c = REAL_CONTENT[real_cells[pool[s, t]]]
                    content[(s, t)] = {"offsets": dict(c["offsets"]), "hull": [],
                                       "sign": c["sign"]}
        banks[nm] = Bank(nm, content)
    return cls, banks


def fit_planted(view, cls):
    bp = cls[view.cells[:, 0]] * 4 + cls[view.cells[:, 1]]
    p = np.array([view.exists[bp == q].mean() if (bp == q).any() else 0.0 for q in range(16)])
    n, du, dv, mu = [], [], [], []
    for q in range(16):
        cells = [k for k in view.content if cls[k[0]] * 4 + cls[k[1]] == q]
        if not cells:
            n.append(0)
            mu.append(0.0)
            continue
        st = most_frequent_set([view.content[k]["offsets"].keys() for k in cells])
        n.append(len(st))
        du += [o[0] for o in st]
        dv += [o[1] for o in st]
        mu.append(float(np.mean([math.log1p(x) for k in cells
                                 for x in view.content[k]["offsets"].values()])))
    sg = np.ones(4, dtype=np.int64)
    for a in range(4):
        signs = [c["sign"] for k, c in view.content.items() if cls[k[0]] == a]
        if sum(x == -1 for x in signs) > sum(x == 1 for x in signs):
            sg[a] = 0
    return {"cls__sym4": cls.copy(), "p": p, "n": np.array(n, dtype=np.int64),
            "du": np.array(du, dtype=np.int64), "dv": np.array(dv, dtype=np.int64),
            "mu": np.array(mu), "sg__sym2": sg}


def planted_predictor(name, cls):
    return Predictor(name, [DEC / "planted_decode.py"], lambda v: fit_planted(v, cls), rank=4)


# ==========================================================================================
# 9. The hub check (acceptance file, section (g); report only)
# ==========================================================================================
def hub_check(shuffled):
    Nm = np.zeros((65, 65))
    for (s, t), c in REAL_CONTENT.items():
        Nm[s, t] = math.fsum(c["offsets"].values()) + len(c["hull"]) * 1.0
    L = np.log1p(Nm)
    Uu, sv, Vt = np.linalg.svd(L)
    lev = 0.5 * ((Uu[:, :18] ** 2).sum(1) + (Vt[:18].T ** 2).sum(1))
    stay = np.zeros(65)
    for i in range(65):
        cells = [(s, t) for (s, t) in REAL_CONTENT if s == i or t == i]
        stay[i] = np.mean([np.mean([b.exists[c] for c in cells]) for b in shuffled])
    H = set(np.argsort(-lev, kind="stable")[:18].tolist())
    Uset = set(np.argsort(-stay, kind="stable")[:18].tolist())
    k = len(H & Uset)
    N, K, n = 65, 18, 18
    pval = sum(math.comb(K, x) * math.comb(N - K, n - x) for x in range(k, n + 1)) / math.comb(N, n)
    rk = lambda x: np.argsort(np.argsort(x, kind="stable"), kind="stable")
    rho = float(np.corrcoef(rk(lev), rk(stay))[0, 1])
    in_u = np.array([[s in Uset or t in Uset for t in range(65)] for s in range(65)])
    share = float((L ** 2)[in_u].sum() / (L ** 2).sum())
    in_h = np.array([[s in H or t in H for t in range(65)] for s in range(65)])
    deg = REAL.exists.sum(0) + REAL.exists.sum(1)
    return {"k90_used": 18, "overlap": k, "expected_overlap": K * n / N,
            "hypergeometric_p_ge": pval, "spearman_leverage_vs_unmoved": rho,
            "L_energy_share_cells_touching_U": share,
            "L_energy_share_cells_touching_H": float((L ** 2)[in_h].sum() / (L ** 2).sum()),
            "H_types": sorted(NAMES[i] for i in H), "U_types": sorted(NAMES[i] for i in Uset),
            "overlap_types": sorted(NAMES[i] for i in H & Uset),
            "unmoved_fraction_range": [float(stay.min()), float(stay.max())],
            "spearman_degree_vs_unmoved": float(np.corrcoef(rk(deg), rk(stay))[0, 1])}


# ==========================================================================================
# 10. Controls and acceptance
# ==========================================================================================
def make_env(base, log):
    t = time.time()
    sh, invs = [], []
    for sd in range(N_SHUFFLES):
        b, inv = shuffled_bank(base, sd)
        sh.append(b)
        invs.append(inv)
    log(f"{base.name}: 99 shuffled banks + dial built ({time.time() - t:.0f}s)")
    return Env(base, sh, dial_banks(base)), invs


def controls():
    t0 = time.time()
    log = lambda m: print(m, flush=True)
    real_env, invs = make_env(REAL, log)
    n1_real = cv(N1, REAL)
    n1_sh = [np.mean([s["existence"] for s in cv(N1, b)]) for b in real_env.shuffled]
    n1_sh_off = [np.mean([s["offset"] for s in cv(N1, b)]) for b in real_env.shuffled]
    control_d = {
        "invariants_all_hold": all(i["n_nonempty"] == 604 and i["out_degrees_kept"]
                                   and i["in_degrees_kept"] and i["content_multiset_kept"]
                                   and i["successful_swaps"] == i["target_swaps"]
                                   for i in invs),
        "per_bank": invs,
        "cells_changed_min_max": [min(i["cells_changed"] for i in invs),
                                  max(i["cells_changed"] for i in invs)],
        "N1_existence_logloss_real": float(np.mean([s["existence"] for s in n1_real])),
        "N1_existence_logloss_shuffled_min_mean_max": [float(np.min(n1_sh)),
                                                       float(np.mean(n1_sh)),
                                                       float(np.max(n1_sh))],
        "N1_offset_jaccard_real": float(np.mean([s["offset"] for s in n1_real])),
        "N1_offset_jaccard_shuffled_min_mean_max": [float(np.min(n1_sh_off)),
                                                    float(np.mean(n1_sh_off)),
                                                    float(np.max(n1_sh_off))],
    }
    log(f"(d) shuffled-bank invariants: {control_d['invariants_all_hold']}")
    nulls = {nm: {f: float(np.mean([s[f] for s in cv(P, REAL)])) for f in FIELDS}
             for nm, P in (("N0", N0), ("N1", N1), ("N_EB", NEB))}
    nulls["N_EB_alpha_per_fold"] = [s["eb_alpha"] for s in cv(NEB, REAL)]
    nulls["N_EB_alpha_insample"] = float(insample(NEB, REAL)[0]["eb_alpha"][0])
    log(f"nulls on the real bank: {json.dumps(nulls)}")
    bf8 = bf_margin(8, REAL)
    log(f"BF_8 on the real bank: {bf8}")

    oracle = Predictor("oracle", STORE_FILES, lambda v, b: fit_oracle(v, b), needs_bank=True)
    n1_rule = Predictor("N1 as a rule", [DEC / "n1_decode.py"], fit_n1)
    n0_rule = Predictor("N0 as a rule", [DEC / "n0_decode.py"], fit_n0)
    rp_rule = rp_predictor(8, 999, 0)
    rp_rule.name = "RP_r8 as a rule (seed 999)"
    cls, pl = planted_banks()
    pr = planted_predictor("PR", cls)
    perm = np.random.Generator(np.random.PCG64(PL_SCRAMBLE_SEED)).permutation(65)
    pr_scr = planted_predictor("PR, scrambled genome", cls[perm])

    out = {}
    for p in (oracle, n1_rule, rp_rule, n0_rule, pr):
        out[f"real/{p.name}"] = run_exam(p, real_env, log)
    pl_desc = {nm: {"n_nonempty": len(b.content), "dl_bank_bits": dl_bank(b)}
               for nm, b in pl.items()}
    log(f"planted banks: {pl_desc}")
    pl1_env, pl1_invs = make_env(pl["PL1"], log)
    for p in (pr, n1_rule, n0_rule, oracle, pr_scr):
        out[f"PL1/{p.name}"] = run_exam(p, pl1_env, log)
    pl0_env, _ = make_env(pl["PL0"], log)
    out["PL0/PR"] = run_exam(pr, pl0_env, log)
    pl05_env, _ = make_env(pl["PL05"], log)
    out["PL05/PR"] = run_exam(pr, pl05_env, log)

    n0_full, _ = insample(N0, REAL)
    r3_k = k_star_armed(dl_bank(REAL) / 10, n0_full, REAL.content)
    hub = hub_check(real_env.shuffled)
    log(f"hub check: {hub}")

    # ---- the A14 checks, re-run ---------------------------------------------------------
    o, n = out["real/oracle"], out["real/N1 as a rule"]
    ofold = [{f: cmp(a, b, f) for f in FIELDS} for a, b in zip(o["per_fold_rule"],
                                                               o["per_fold_N1"])]
    a14 = {
        "a_oracle_wins_all_four_fields_every_fold": all(all(v == 1 for v in d.values())
                                                        for d in ofold),
        "a_oracle_fails_P2_on_length": not o["P2"]["length_ok"],
        "a_oracle_does_not_pass_C6": o["verdict"] != "PASS",
        "b_N1_zero_wins_existence_offset": n["P1"]["existence"]["wins"] == 0
        and n["P1"]["offset"]["wins_vs"]["N1"] == 0,
        "b_N1_no_losses_counts_sign": n["P1"]["counts"]["losses"] == 0
        and n["P1"]["sign"]["losses"] == 0,
        "b_N1_does_not_pass_C6": n["verdict"] != "PASS",
        "c_RP_does_not_pass_C6": out["real/RP_r8 as a rule (seed 999)"]["verdict"] != "PASS",
        "d_shuffle_invariants_hold": control_d["invariants_all_hold"],
    }

    # ---- the acceptance criteria (docs/plans/2026-09-23-c6-amendment-acceptance.md) -------
    def dial_ratio(res):
        m = {f: np.mean([x["heldout_margin_over_N1"]["existence"] for x in res["dial"]
                         if x["f"] == f]) for f in (0.0, 1.0)}
        return float(m[1.0] / m[0.0]) if m[0.0] > 0 else float("inf"), m

    ratio, dm = dial_ratio(out["PL1/PR"])
    n1r, n0r = out["real/N1 as a rule"], out["real/N0 as a rule"]
    crit = [
        ("R1", "N1 submitted as a rule, on the real bank, does not beat the armed table D_k^N0 at "
               "its own description length, in-sample, on at least one of existence and offset "
               "set.", "P2 fails with 'below threshold for this family'",
         f"beats armed D_k: {n1r['P2']['beats']['dk_armed']} (k*_armed={n1r['P2']['k_star_armed']}); "
         f"labels {n1r['labels']}",
         (not all(n1r["P2"]["beats"]["dk_armed"].values()))
         and "below threshold for this family" in n1r["labels"]),
        ("R2", "N0 submitted as a rule, on the real bank, is within the length limit and does not "
               "beat the armed table at its own length.",
         "P2 fails with 'below threshold for this family' and not with 'not a bottleneck'",
         f"length_ok={n0r['P2']['length_ok']} (DL {n0r['P2']['dl_rule_bits']}); beats armed "
         f"D_k: {n0r['P2']['beats']['dk_armed']} (k*_armed={n0r['P2']['k_star_armed']}); "
         f"labels {n0r['labels']}",
         n0r["P2"]["length_ok"] and not all(n0r["P2"]["beats"]["dk_armed"].values())
         and "below threshold for this family" in n0r["labels"]
         and "not a bottleneck" not in n0r["labels"]),
        ("R3", "At a budget of DL(bank)/10 the armed table stores k*_armed >= 5 cells.",
         ">= 5", f"k*_armed = {r3_k}", r3_k >= R3_MIN_CELLS),
        ("A1", "PR on PL1 passes C6 (P1, P2, P3, P4 as amended, and not 'did not run').", "PASS",
         f"{out['PL1/PR']['verdict']} {out['PL1/PR']['labels']}",
         out["PL1/PR"]["verdict"] == "PASS"),
        ("A2", "N1 as a rule and N0 as a rule on PL1 fail C6.", "both FAIL",
         f"N1: {out['PL1/N1 as a rule']['verdict']}; N0: {out['PL1/N0 as a rule']['verdict']}",
         out["PL1/N1 as a rule"]["verdict"] == "FAIL"
         and out["PL1/N0 as a rule"]["verdict"] == "FAIL"),
        ("A3", "The oracle on PL1 fails on size.", "FAIL with 'not a bottleneck'",
         f"{out['PL1/oracle']['verdict']} {out['PL1/oracle']['labels']}",
         out["PL1/oracle"]["verdict"] == "FAIL"
         and "not a bottleneck" in out["PL1/oracle"]["labels"]),
        ("A4", "A foreign genome of the same size loses: PR with its class vector permuted by "
               "PCG64(99), on PL1, fails C6.", "FAIL",
         f"{out['PL1/PR, scrambled genome']['verdict']} {out['PL1/PR, scrambled genome']['labels']}"
         f"; DL {out['PL1/PR, scrambled genome']['P2']['dl_rule_bits']} vs PR "
         f"{out['PL1/PR']['P2']['dl_rule_bits']}",
         out["PL1/PR, scrambled genome"]["verdict"] == "FAIL"),
        ("A5", "PR's held-out existence margin over N1 on PL1's dial at f = 1 is at most 0.25 x "
               "its margin at f = 0.", "ratio <= 0.25",
         f"ratio = {ratio:.4f} (f=0: {dm[0.0]:.4f}, f=1: {dm[1.0]:.4f})",
         ratio <= A5_MAX_RATIO),
        ("N1", "PR on PL0 (strength 0) fails C6.", "FAIL",
         f"{out['PL0/PR']['verdict']} {out['PL0/PR']['labels']}",
         out["PL0/PR"]["verdict"] == "FAIL"),
        ("N2", "The PR family on the real fly bank fails C6.", "FAIL",
         f"{out['real/PR']['verdict']} {out['real/PR']['labels']}",
         out["real/PR"]["verdict"] == "FAIL"),
        ("N3", "On the real bank the A14 controls still do not pass: oracle, N1 as a rule, "
               "RP_r8 as a rule.", "all three FAIL",
         ", ".join(f"{k}: {out['real/' + k]['verdict']}" for k in
                   ("oracle", "N1 as a rule", "RP_r8 as a rule (seed 999)")),
         all(out["real/" + k]["verdict"] == "FAIL" for k in
             ("oracle", "N1 as a rule", "RP_r8 as a rule (seed 999)"))),
        ("M1", "The A5 bit table and the one-tenth constant are untouched; DL(bank) on the real "
               "bank is still 94,812 bits.", "94812",
         f"{dl_bank(REAL)}", dl_bank(REAL) == DL_BANK_REAL_REGISTERED),
        ("M2", "P2 opponents are only added: old D_k^N1 at k*, plus armed D_k^N0 and N1 in-sample;"
               " P2 requires all three wins.", "three opponents in P2",
         f"{sorted(out['real/oracle']['P2']['beats'])}",
         sorted(out["real/oracle"]["P2"]["beats"]) == ["dk_armed", "dk_star", "n1_insample"]),
        ("M3", "The offset-set target only gets stronger: N_EB's mean held-out Jaccard on the "
               "real bank >= 0.4465.", ">= 0.4465",
         f"{nulls['N_EB']['offset']:.4f} (N0 {nulls['N0']['offset']:.4f}, "
         f"N1 {nulls['N1']['offset']:.4f})", nulls["N_EB"]["offset"] >= M3_CONTROL),
        ("M4", "P4 is replaced, not deleted: BF_8's mean held-out existence margin over N1 on "
               "the real bank > 0.", "> 0",
         f"{bf8['margin']:+.5f} nats; beats N1 in {bf8['folds_beating_N1']}/10 folds; "
         f"lambdas {bf8['lambdas']}", bf8["margin"] > 0),
        ("M5", "Smoothing and penalty frozen by the registered rules; chosen values recorded.",
         "recorded", f"alpha per fold {nulls['N_EB_alpha_per_fold']}, in-sample "
                     f"{nulls['N_EB_alpha_insample']}; BF_8 lambda per fold {bf8['lambdas']}",
         True),
    ]
    acc = [{"id": c[0], "criterion": c[1], "expected": c[2], "got": c[3],
            "result": "PASS" if c[4] else "FAIL"} for c in crit]
    for a in acc:
        log(f"{a['result']:4s} {a['id']}: {a['criterion']}\n       expected: {a['expected']}"
            f"\n       got:      {a['got']}")
    harness_sha = sha256_lf(__file__)
    res = {
        "what": "C6 harness controls after Amendment 2: the exam run with no rule, plus the "
                "planted-rule acceptance suite.",
        "harness_sha256_lf": harness_sha,
        "spec_sha256_lf": sha256_lf(SPEC), "acceptance_sha256_lf": sha256_lf(ACCEPTANCE),
        "folds_sha256_lf": sha256_lf(HERE / "folds.csv"),
        "decoder_sha256_lf": {p.name: sha256_lf(p) for p in sorted(DEC.glob("*.py"))},
        "numpy": np.__version__, "python": sys.version.split()[0],
        "program_bits": {"N1": N1.prog_bits, "N0": N0.prog_bits, "store": S_ALL.prog_bits,
                         "D_k (N1 base)": DK.prog_bits, "D_k armed (N0 base)": DK0.prog_bits,
                         "RP": rp_rule.prog_bits, "BF": bf_predictor(8).prog_bits,
                         "PR": pr.prog_bits},
        "acceptance": acc,
        "checks_against_A14": a14,
        "nulls_real_bank": nulls, "BF_8_real_bank": bf8,
        "R3_k_star_armed_at_limit": r3_k,
        "planted_banks": pl_desc, "planted_classes": cls.tolist(),
        "hub_check": hub,
        "control_d_shuffled_banks": control_d,
        "controls": out,
        "runtime_s": round(time.time() - t0, 1),
    }
    (HERE / "harness_controls.json").write_text(
        json.dumps(res, indent=1, default=lambda x: x.item() if hasattr(x, "item") else str(x))
        + "\n", encoding="utf-8", newline="\n")
    log(f"A14: {json.dumps(a14)}")
    log(f"harness sha256 {harness_sha}; total {time.time() - t0:.0f}s")


def load_rule(path):
    spec = importlib.util.spec_from_file_location("c6_rule", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return Predictor(m.NAME, [Path(f) for f in m.PROGRAM_FILES], m.fit,
                     rank=getattr(m, "RANK", None))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--controls", action="store_true")
    ap.add_argument("--rule")
    a = ap.parse_args()
    if a.controls:
        controls()
    elif a.rule:
        sys.exit("A rule run is not enabled in this version: no rule is registered (C6 A14).")
    else:
        ap.print_help()
