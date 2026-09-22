"""C6 harness: the exam a regenerating rule must pass, shipped with NO rule.

Specification: docs/plans/2026-09-23-c6-control-specification.md, sections 2-6 and the
Amendment of 2026-09-23 (A1-A15). The harness refuses to run if the spec or folds.csv no longer
match the hashes recorded in folds.meta.json.

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
if sha256_lf(SPEC) != FMETA["spec"]["sha256_lf_normalised"]:
    sys.exit("REFUSED: the C6 specification changed after the folds were generated")

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
# 5. The arms
# ==========================================================================================
_CV_CACHE = {}


def cv(pred, bank, fold_grid=FOLD, n_folds=N_FOLDS, cache_key=None):
    key = (pred.name, bank.name, cache_key or "primary")
    if key in _CV_CACHE:
        return _CV_CACHE[key]
    out = []
    for f in range(n_folds):
        held = fold_grid == f
        cells = ALL_CELLS[held[ALL_CELLS[:, 0], ALL_CELLS[:, 1]]]
        data = pred.train(bank, ~held)
        out.append(score(pred.decode(data, cells), bank, cells))
    _CV_CACHE[key] = out
    return out


def insample(pred, bank):
    data = pred.train(bank, np.ones((65, 65), bool))
    return data, score(pred.decode(data, ALL_CELLS), bank, ALL_CELLS)


def p1(rule_s, n1_s):
    res = {}
    for f in ("existence", "offset"):
        w = sum(cmp(r, n, f) == 1 for r, n in zip(rule_s, n1_s))
        res[f] = {"wins": int(w), "pass": bool(w >= P1_MIN_WINS)}
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


def dl_dk(k, n1_full, content, order):
    d = dict(n1_full)
    d.update(store_data(content, order[:k]))
    return DK.dl(d)


def k_star(budget, n1_full, content):
    order = dk_order(content)
    if dl_dk(0, n1_full, content, order) > budget:
        return 0
    lo, hi = 0, len(order)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if dl_dk(mid, n1_full, content, order) <= budget:
            lo = mid
        else:
            hi = mid - 1
    return lo


def p2(pred, bank=REAL):
    data, s_rule = insample(pred, bank)
    dl_rule = pred.dl(data)
    bank_data, _ = insample(S_ALL, bank)
    dl_bank = S_ALL.dl(bank_data)
    n1_full, _ = insample(N1, bank)
    ks = k_star(dl_rule, n1_full, bank.content)
    k18 = k_star(M18, n1_full, bank.content)
    dk = Predictor(f"D_{ks}", DK_FILES, lambda v: fit_dk(v, ks))
    dk_data, s_dk = insample(dk, bank)
    dk18 = Predictor(f"D_{k18}", DK_FILES, lambda v: fit_dk(v, k18))
    _, s_dk18 = insample(dk18, bank)
    beats = {f: cmp(s_rule, s_dk, f) == 1 for f in ("existence", "offset")}
    length_ok = dl_rule <= dl_bank / 10
    return {"dl_rule_bits": dl_rule, "dl_rule_program_bits": pred.prog_bits,
            "dl_bank_bits": dl_bank, "dl_bank_over_10": dl_bank / 10,
            "k_star": ks, "dl_dk_star_bits": DK.dl(dk_data), "M18_bits": M18, "k18": k18,
            "insample_rule": s_rule, "insample_dk_star": s_dk, "insample_dk18": s_dk18,
            "length_ok": bool(length_ok), "beats_dk_star": {k: bool(v) for k, v in beats.items()},
            "below_M18": bool(dl_rule < M18),
            "pass": bool(length_ok and all(beats.values()))}


# ---- shuffled banks (A10) and the dial (A12) ---------------------------------------------
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


def shuffled_bank(seed):
    rng = np.random.Generator(np.random.PCG64(seed))
    content, succ, att = rewire_and_permute(REAL, rng, 1.0)
    b = Bank(f"shuffle{seed}", content)
    inv = {
        "n_nonempty": int(b.exists.sum()),
        "out_degrees_kept": bool((b.exists.sum(1) == REAL.exists.sum(1)).all()),
        "in_degrees_kept": bool((b.exists.sum(0) == REAL.exists.sum(0)).all()),
        "content_multiset_kept": sorted(map(canon_content, b.content.values()))
        == sorted(map(canon_content, REAL.content.values())),
        "successful_swaps": succ, "attempts": att,
        "cells_changed": int((b.exists != REAL.exists).sum() // 2),
    }
    return b, inv


def dial_bank(fi, seed):
    rng = np.random.Generator(np.random.PCG64(10000 + 100 * fi + seed))
    content, succ, att = rewire_and_permute(REAL, rng, DIAL_F[fi])
    return Bank(f"dial{fi}_{seed}", content), {"successful_swaps": succ, "attempts": att}


# ---- random projection (A11) -------------------------------------------------------------
def rank_of(pred, data_full):
    if pred.rank:
        return min(pred.rank, RP_RANK_CAP)
    n_real = sum(np.asarray(v).size for v in data_full.values() if np.asarray(v).dtype.kind == "f")
    return int(min(max(1, round(n_real / 130)), RP_RANK_CAP))


def rp_predictor(r, seed, side):
    return Predictor(f"RP_r{r}_s{seed}_side{side}", RP_FILES,
                     lambda v: rp_fit(v, r, seed, side), rank=r)


def rp_margins(r, bank=REAL):
    n1s = cv(N1, bank)
    out = []
    for j in RP_SEEDS:
        m = [margin(cv(rp_predictor(r, RP_SEED_BASE + j, side), bank), n1s, "existence")
             for side in (0, 1)]
        out.append({"seed": RP_SEED_BASE + j, "margin_side0": m[0], "margin_side1": m[1],
                    "margin": max(m)})
    return out


# ---- secondary split: leave one type out (spec 4.5, descriptive) --------------------------
def loto(pred, bank=REAL):
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
# 6. The whole exam for one predictor
# ==========================================================================================
def run_exam(pred, shuffled, dial, log=print):
    t0 = time.time()
    rule_s, n1_s, n0_s = cv(pred, REAL), cv(N1, REAL), cv(N0, REAL)
    r1 = p1(rule_s, n1_s)
    dnr = did_not_run(rule_s, n0_s)
    log(f"  [{pred.name}] P1 done {time.time() - t0:.0f}s")
    r2 = p2(pred)
    log(f"  [{pred.name}] P2 done {time.time() - t0:.0f}s")
    real_m = {f: margin(rule_s, n1_s, f) for f in FIELDS}
    sh_m = {f: [] for f in FIELDS}
    for b in shuffled:
        rs, ns = cv(pred, b), cv(N1, b)
        for f in FIELDS:
            sh_m[f].append(margin(rs, ns, f))
    r3 = {f: {"real_margin": real_m[f], "shuffled_max": float(np.max(sh_m[f])),
              "shuffled_mean": float(np.mean(sh_m[f])),
              "n_shuffled_ge_real": int(sum(m >= real_m[f] for m in sh_m[f])),
              "strictly_above_all": bool(all(real_m[f] > m for m in sh_m[f]))} for f in FIELDS}
    r3["pass"] = r3["existence"]["strictly_above_all"] and r3["offset"]["strictly_above_all"]
    log(f"  [{pred.name}] P3 done {time.time() - t0:.0f}s")
    full_data, _ = insample(pred, REAL)
    r = rank_of(pred, full_data)
    rpm = rp_margins(r)
    best_rp = max(x["margin"] for x in rpm)
    r4 = {"rank": r, "rule_margin_existence": real_m["existence"], "rp_max_margin": best_rp,
          "rp_margins": rpm, "pass": bool(real_m["existence"] > best_rp)}
    log(f"  [{pred.name}] P4 done {time.time() - t0:.0f}s")
    dial_out = []
    dk_star = Predictor(f"D_{r2['k_star']}", DK_FILES, lambda v: fit_dk(v, r2["k_star"]))
    for (fi, sd, b) in dial:
        rs, ns = cv(pred, b), cv(N1, b)
        _, s_rule = insample(pred, b)
        _, s_dk = insample(dk_star, b)
        dial_out.append({"f": DIAL_F[fi], "seed": sd,
                         "heldout_margin_over_N1": {f: margin(rs, ns, f) for f in FIELDS},
                         "insample_margin_over_Dk": {f: margin([s_rule], [s_dk], f)
                                                     for f in FIELDS}})
    log(f"  [{pred.name}] dial done {time.time() - t0:.0f}s")
    lo = loto(pred)
    labels = []
    if dnr["did_not_run"]:
        labels.append("rule did not run")
    if not r1["pass"]:
        labels.append("copy or marginal")
    if not r2["length_ok"]:
        labels.append("not a bottleneck")
    if not all(r2["beats_dk_star"].values()):
        labels.append("below threshold for this family")
    if not r3["pass"]:
        labels.append("family fits anything")
    if not r4["pass"]:
        labels.append("ambient, not substantive structure")
    verdict = "PASS" if not labels else "FAIL"
    log(f"  [{pred.name}] {verdict} {labels} ({time.time() - t0:.0f}s)")
    return {"name": pred.name, "program_files": [str(Path(f).relative_to(ROOT).as_posix())
                                                  for f in pred.program_files],
            "per_fold_rule": rule_s, "per_fold_N1": n1_s, "per_fold_N0": n0_s,
            "P1": r1, "did_not_run": dnr, "P2": r2, "P3": r3, "P4": r4,
            "dial": dial_out, "loto": lo, "labels": labels, "verdict": verdict}


def controls():
    t0 = time.time()
    print("building 99 shuffled banks")
    shuffled, invs = [], []
    for sd in range(N_SHUFFLES):
        b, inv = shuffled_bank(sd)
        shuffled.append(b)
        invs.append(inv)
    dial = []
    dial_inv = []
    for fi in range(len(DIAL_F)):
        for sd in range(DIAL_SEEDS):
            if DIAL_F[fi] == 0.0:
                b, info = Bank(f"dial0_{sd}", REAL.content), {"successful_swaps": 0,
                                                             "attempts": 0}
            else:
                b, info = dial_bank(fi, sd)
            dial.append((fi, sd, b))
            dial_inv.append({"f": DIAL_F[fi], "seed": sd, **info,
                             "target_swaps": SWAPS_PER_EDGE * int(round(DIAL_F[fi] * 604))})
    print(f"banks built {time.time() - t0:.0f}s")

    n1_real = cv(N1, REAL)
    n1_sh = [np.mean([s["existence"] for s in cv(N1, b)]) for b in shuffled]
    n1_sh_off = [np.mean([s["offset"] for s in cv(N1, b)]) for b in shuffled]
    control_d = {
        "invariants_all_hold": all(i["n_nonempty"] == 604 and i["out_degrees_kept"]
                                   and i["in_degrees_kept"] and i["content_multiset_kept"]
                                   and i["successful_swaps"] == SWAPS_PER_EDGE * 604
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
        "dial_banks": dial_inv,
    }
    print(f"(d) shuffled-bank invariants: {control_d['invariants_all_hold']}")

    oracle = Predictor("oracle", STORE_FILES, lambda v, b: fit_oracle(v, b), needs_bank=True)
    n1_rule = Predictor("N1 as a rule", [DEC / "n1_decode.py"], fit_n1)
    rp_rule = rp_predictor(8, 999, 0)
    rp_rule.name = "RP_r8 as a rule (seed 999)"
    out = {}
    for p in (oracle, n1_rule, rp_rule):
        out[p.name] = run_exam(p, shuffled, dial)

    # registered expectations (A14) -> behaves as designed?
    o, n, r = out["oracle"], out["N1 as a rule"], out["RP_r8 as a rule (seed 999)"]
    ofold = [{f: cmp(a, b, f) for f in FIELDS} for a, b in zip(o["per_fold_rule"],
                                                               o["per_fold_N1"])]
    checks = {
        "a_oracle_wins_all_four_fields_every_fold": all(all(v == 1 for v in d.values())
                                                        for d in ofold),
        "a_oracle_wins_per_field": {f: int(sum(d[f] == 1 for d in ofold)) for f in FIELDS},
        "a_oracle_ties_per_field": {f: int(sum(d[f] == 0 for d in ofold)) for f in FIELDS},
        "a_oracle_passes_P1": o["P1"]["pass"],
        "a_oracle_fails_P2_on_length": not o["P2"]["length_ok"],
        "a_oracle_dl_ge_bank": o["P2"]["dl_rule_bits"] >= o["P2"]["dl_bank_bits"],
        "a_oracle_does_not_pass_C6": o["verdict"] != "PASS",
        "b_N1_zero_wins_existence_offset": n["P1"]["existence"]["wins"] == 0
        and n["P1"]["offset"]["wins"] == 0,
        "b_N1_no_losses_counts_sign": n["P1"]["counts"]["losses"] == 0
        and n["P1"]["sign"]["losses"] == 0,
        "b_N1_does_not_pass_C6": n["verdict"] != "PASS",
        "c_RP_does_not_pass_C6": r["verdict"] != "PASS",
        "d_shuffle_invariants_hold": control_d["invariants_all_hold"],
    }
    res = {
        "what": "C6 harness controls: the exam run with no rule (Amendment A14).",
        "spec_sha256_lf": sha256_lf(SPEC), "folds_sha256_lf": sha256_lf(HERE / "folds.csv"),
        "harness_sha256_lf": sha256_lf(__file__),
        "decoder_sha256_lf": {p.name: sha256_lf(p) for p in sorted(DEC.glob("*.py"))},
        "numpy": np.__version__, "python": sys.version.split()[0],
        "program_bits": {"N1": N1.prog_bits, "N0": N0.prog_bits, "store": S_ALL.prog_bits,
                         "D_k": DK.prog_bits, "RP": rp_rule.prog_bits},
        "checks_against_A14": checks,
        "control_d_shuffled_banks": control_d,
        "controls": out,
        "runtime_s": round(time.time() - t0, 1),
    }
    (HERE / "harness_controls.json").write_text(
        json.dumps(res, indent=1, default=lambda x: x.item() if hasattr(x, "item") else str(x))
        + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(checks, indent=1))
    print(f"total {time.time() - t0:.0f}s")


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
