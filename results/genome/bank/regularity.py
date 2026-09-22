"""Regularity of the type-pair table: the measures declared in REGULARITY-DECLARATION.md.

DESCRIPTIVE. No threshold, no verdict. Refuses to run unless REGULARITY-DECLARATION.md matches
the sha256 recorded in REGULARITY-DECLARATION.sha256.json (hashed before this script existed).

Reads only the bank extracted next to this file (types.csv, type_pairs.csv, offsets.csv).
Writes regularity_results.json (UTF-8) next to this file.

Usage (from the repository root):
    tools/.venv/Scripts/python.exe results/genome/bank/regularity.py
"""

import hashlib
import json
import lzma
import math
import sys
import zlib
from collections import Counter, OrderedDict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent
DECL = OUT / "REGULARITY-DECLARATION.md"
DECL_REC = json.loads((OUT / "REGULARITY-DECLARATION.sha256.json").read_text(encoding="utf-8"))


def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


if sha256_file(DECL) != DECL_REC["sha256"]:
    sys.exit("REFUSED: REGULARITY-DECLARATION.md does not match its recorded sha256.")

N_AD = 2000   # null draws for (a) and (d)
N_C = 10000   # null draws for (c)
rng = np.random.default_rng(20260923)


def read_csv(name):
    return pd.read_csv(OUT / name, skiprows=1, dtype=str, keep_default_na=False,
                       encoding="utf-8")


T = read_csv("types.csv")
P = read_csv("type_pairs.csv")
O = read_csv("offsets.csv")
types = T.sort_values("node_order_index", key=lambda c: c.astype(int)).type_name.tolist()
idx = {t: i for i, t in enumerate(types)}
nT = len(types)
assert nT == 65

Ob = O[O.provenance.isin(["in_json", "hull_filled"])].copy()   # compiled bank
Oj = O[O.provenance.isin(["in_json", "dropped"])].copy()       # raw json offsets
for D in (Ob, Oj):
    D["du"] = D.du.astype(int)
    D["dv"] = D.dv.astype(int)
    D["sign"] = D.sign.astype(int)
Ob["n"] = Ob.n_syn.astype(float)
Oj["n"] = Oj.n_syn_json.astype(float)
assert len(Ob) == 2355 and len(Oj) == 2140

# ------------------------------------------------------------------------------------------
# Matrices
# ------------------------------------------------------------------------------------------
pairs_b = Ob.groupby(["src", "tar"], sort=False).agg(
    N=("n", lambda x: math.fsum(x)), sign=("sign", "first"), K=("n", "size")).reset_index()
assert len(pairs_b) == 604
C = np.zeros((nT, nT), np.uint8)
S = np.zeros((nT, nT), np.int8)
Nm = np.zeros((nT, nT), np.float64)
K = np.zeros((nT, nT), np.uint8)
for r in pairs_b.itertuples():
    i, j = idx[r.src], idx[r.tar]
    C[i, j] = 1
    S[i, j] = r.sign
    Nm[i, j] = r.N
    K[i, j] = r.K
Q = np.where(C == 1, np.round(2 * np.log2(1 + Nm)), 0).astype(np.uint8)
N32 = Nm.astype(np.float32)
L = np.log1p(Nm)
mats = OrderedDict(C=C, S=S, Q=Q, K=K, N32=N32)


def zsize(b):
    return len(zlib.compress(b, 9))


def xsize(b):
    return len(lzma.compress(b, format=lzma.FORMAT_XZ, preset=9))


COMP = OrderedDict(zlib=zsize, lzma=xsize)


def summarise(obs, null):
    null = np.asarray(null, float)
    sd = float(null.std(ddof=1))
    return OrderedDict(
        observed=obs, null_mean=float(null.mean()), null_sd=sd, null_min=float(null.min()),
        null_p2_5=float(np.percentile(null, 2.5)), null_p50=float(np.percentile(null, 50)),
        null_p97_5=float(np.percentile(null, 97.5)), null_max=float(null.max()),
        frac_null_le_observed=(int((null <= obs).sum()) + 1) / (len(null) + 1),
        frac_null_ge_observed=(int((null >= obs).sum()) + 1) / (len(null) + 1),
        z=(obs - float(null.mean())) / sd if sd > 0 else None, n_draws=len(null))


# ------------------------------------------------------------------------------------------
# (a) Compressibility
# ------------------------------------------------------------------------------------------
res_a = OrderedDict()
for mname, M in mats.items():
    raw = M.tobytes(order="C")
    obs = {c: f(raw) for c, f in COMP.items()}
    nulls = {(nl, c): [] for nl in ("P-indep", "P-sym", "E-shuffle") for c in COMP}
    for nl in ("P-indep", "P-sym", "E-shuffle"):
        for _ in range(N_AD):
            if nl == "P-indep":
                Mp = M[rng.permutation(nT)][:, rng.permutation(nT)]
            elif nl == "P-sym":
                p = rng.permutation(nT)
                Mp = M[p][:, p]
            else:
                Mp = rng.permutation(M.ravel()).reshape(M.shape)
            b = np.ascontiguousarray(Mp).tobytes(order="C")
            for c, f in COMP.items():
                nulls[(nl, c)].append(f(b))
    res_a[mname] = OrderedDict(
        raw_bytes=len(raw), dtype=str(M.dtype),
        observed_bytes=obs,
        observed_ratio={c: obs[c] / len(raw) for c in COMP},
        nulls={f"{nl}/{c}": summarise(obs[c], v) for (nl, c), v in nulls.items()})

# (a') repeated rows / columns
def groups_identical(M, axis):
    vecs = [M[i].tobytes() if axis == 0 else M[:, i].tobytes() for i in range(nT)]
    g = OrderedDict()
    for i, v in enumerate(vecs):
        g.setdefault(v, []).append(types[i])
    return [v for v in g.values() if len(v) > 1], len(g)


res_a1 = OrderedDict()
for mname in ("C", "S", "Q"):
    M = mats[mname]
    gr, nr = groups_identical(M, 0)
    gc, nc = groups_identical(M, 1)
    res_a1[mname] = OrderedDict(n_distinct_rows=nr, n_distinct_columns=nc,
                                shared_out_rows=gr if mname in ("C", "S") else None,
                                shared_in_columns=gc if mname in ("C", "S") else None)

# ------------------------------------------------------------------------------------------
# (b) Offset patterns
# ------------------------------------------------------------------------------------------
def rot(u, v):
    return (u + v, -u)


def refl(u, v):
    return (v, u)


def d6_images(pts):
    """pts: list of ((u, v), w). Returns the 12 images under the hex lattice symmetries."""
    out = []
    cur = pts
    for _ in range(6):
        out.append(cur)
        out.append([(refl(*uv), w) for uv, w in cur])
        cur = [(rot(*uv), w) for uv, w in cur]
    return out


def canon_pattern(pts, with_w, sym):
    def key(ps):
        return tuple(sorted((uv, w) if with_w else uv for uv, w in ps))
    if not sym:
        return key(pts)
    return min(key(im) for im in d6_images(pts))


def patterns(D):
    per = OrderedDict()
    for (src, tar), grp in D.groupby(["src", "tar"], sort=False):
        tot = math.fsum(grp.n)
        per[(src, tar)] = [((int(a.du), int(a.dv)), round(a.n / tot, 2))
                           for a in grp.itertuples()]
    return per


def pattern_stats(per):
    out = OrderedDict()
    for lvl, (with_w, sym) in OrderedDict(
            L1=(False, False), L2=(True, False), L3=(False, True), L4=(True, True)).items():
        keys = {pr: canon_pattern(pts, with_w, sym) for pr, pts in per.items()}
        cnt = Counter(keys.values())
        groups = sorted(cnt.items(), key=lambda kv: (-kv[1], repr(kv[0])))
        top = []
        for k, n in groups[:10]:
            members = [f"{a}>{b}" for (a, b), kk in keys.items() if kk == k]
            top.append(OrderedDict(size=n, pattern=repr(k), members_first_12=members[:12]))
        out[lvl] = OrderedDict(
            n_pairs=len(per), n_distinct=len(cnt),
            n_pairs_in_shared_patterns=sum(n for n in cnt.values() if n > 1),
            n_singleton_patterns=sum(1 for n in cnt.values() if n == 1),
            n_shared_patterns=sum(1 for n in cnt.values() if n > 1),
            largest_groups=top)
    sizes = Counter(len(p) for p in per.values())
    out["support_size_distribution"] = dict(sorted(sizes.items()))
    out["n_pairs_support_origin_only"] = sum(
        1 for p in per.values() if [uv for uv, _ in p] == [(0, 0)])
    return out


res_b = OrderedDict(compiled=pattern_stats(patterns(Ob)), json=pattern_stats(patterns(Oj)))

# ------------------------------------------------------------------------------------------
# (c) Sign from source type
# ------------------------------------------------------------------------------------------
src_arr = pairs_b.src.to_numpy()
tar_arr = pairs_b.tar.to_numpy()
sgn = pairs_b.sign.to_numpy().astype(int)


def H(counts):
    c = np.asarray([x for x in counts if x > 0], float)
    p = c / c.sum()
    return float(-(p * np.log2(p)).sum())


def cond_stats(group, y):
    df = pd.DataFrame(dict(g=group, y=y))
    tab = df.groupby(["g", "y"]).size().unstack(fill_value=0)
    n = tab.to_numpy().sum()
    hc = sum(row.sum() / n * H(row) for row in tab.to_numpy())
    acc = tab.to_numpy().max(axis=1).sum() / n
    return hc, float(acc)


h_sign = H(Counter(sgn).values())
hs_obs, accs_obs = cond_stats(src_arr, sgn)
ht_obs, acct_obs = cond_stats(tar_arr, sgn)
null_hs, null_as, null_ht, null_at = [], [], [], []
for _ in range(N_C):
    y = rng.permutation(sgn)
    a, b = cond_stats(src_arr, y)
    c, d = cond_stats(tar_arr, y)
    null_hs.append(a); null_as.append(b); null_ht.append(c); null_at.append(d)

Pi = P.set_index(["src", "tar"])
mixed = OrderedDict()
for t in types:
    m = sgn[src_arr == t]
    if len(m) and len(set(m)) > 1:
        cnt = Counter(m)
        minority = min(cnt, key=lambda k: (cnt[k], k))
        rows = []
        for tt in tar_arr[(src_arr == t) & (sgn == minority)]:
            r = Pi.loc[(t, tt)]
            rows.append(OrderedDict(target=tt, alpha_fixed=r.alpha_fixed,
                                    alpha_references=r.alpha_references))
        mixed[t] = OrderedDict(n_pairs=int(len(m)), n_exc=int(cnt.get(1, 0)),
                               n_inh=int(cnt.get(-1, 0)), minority_sign=int(minority),
                               minority_pairs=rows)
res_c = OrderedDict(
    n_pairs=int(len(sgn)), n_exc=int((sgn == 1).sum()), n_inh=int((sgn == -1).sum()),
    H_sign_bits=h_sign,
    n_source_types=int(len(set(src_arr))), n_target_types=int(len(set(tar_arr))),
    H_sign_given_source=summarise(hs_obs, null_hs),
    majority_accuracy_by_source=summarise(accs_obs, null_as),
    H_sign_given_target=summarise(ht_obs, null_ht),
    majority_accuracy_by_target=summarise(acct_obs, null_at),
    mixed_sign_source_types=mixed,
    n_pairs_not_matching_source_majority=int(round((1 - accs_obs) * len(sgn))),
)

# ------------------------------------------------------------------------------------------
# (d) Low-rank structure
# ------------------------------------------------------------------------------------------
def spec_stats(M):
    s = np.linalg.svd(M.astype(float), compute_uv=False)
    e = s ** 2
    cum = np.cumsum(e) / e.sum()
    p = s / s.sum()
    p = p[p > 0]
    return OrderedDict(
        top_energy={k: float(cum[k - 1]) for k in (1, 2, 3, 5, 10)},
        k90=int(np.searchsorted(cum, 0.90) + 1), k95=int(np.searchsorted(cum, 0.95) + 1),
        effective_rank=float(np.exp(-(p * np.log(p)).sum())),
        stable_rank=float(e.sum() / e[0]),
        numerical_rank=int((s > s[0] * 1e-10).sum()),
    ), s


def spec_null(obs, draws):
    out = OrderedDict()
    for k in ("effective_rank", "stable_rank", "k90", "k95"):
        out[k] = summarise(obs[k], [d[k] for d in draws])
    for kk in (1, 2, 3, 5, 10):
        out[f"top{kk}_energy"] = summarise(obs["top_energy"][kk],
                                           [d["top_energy"][kk] for d in draws])
    return out


res_d = OrderedDict()
nz = np.nonzero(L)
for mname, M in (("L", L), ("C", C.astype(float))):
    obs, s = spec_stats(M)
    dE = [spec_stats(rng.permutation(M.ravel()).reshape(M.shape))[0] for _ in range(N_AD)]
    entry = OrderedDict(observed=obs, singular_values=[float(x) for x in s],
                        null_D_E=spec_null(obs, dE))
    if mname == "L":
        dS = []
        vals = M[nz]
        for _ in range(N_AD):
            Mp = np.zeros_like(M)
            Mp[nz] = rng.permutation(vals)
            dS.append(spec_stats(Mp)[0])
        entry["null_D_S"] = spec_null(obs, dS)
    res_d[mname] = entry

# ------------------------------------------------------------------------------------------
out = OrderedDict(
    header="DESCRIPTIVE -- no threshold, no verdict (REGULARITY-DECLARATION.md)",
    run_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    declaration_sha256=DECL_REC["sha256"], declaration_recorded_utc=DECL_REC["recorded_utc"],
    script_sha256=sha256_file(__file__),
    inputs={n: sha256_file(OUT / n) for n in ("types.csv", "type_pairs.csv", "offsets.csv")},
    rng="numpy.random.default_rng(20260923)", n_draws_a_d=N_AD, n_draws_c=N_C,
    density=OrderedDict(n_pairs=int(C.sum()), n_cells=nT * nT, fraction=float(C.mean())),
    a_compressibility=res_a, a1_repeated_rows_columns=res_a1,
    b_offset_patterns=res_b, c_sign_from_source=res_c, d_low_rank=res_d,
)
(OUT / "regularity_results.json").write_text(
    json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
print("written regularity_results.json")
