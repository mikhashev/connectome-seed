import csv, itertools, math
from collections import defaultdict, Counter
import numpy as np
from scipy.stats import fisher_exact, hypergeom, wilcoxon

R = "C:/Users/mikha/Documents/dpc-research/connectome-seed/results/genome/c6/checks/"
SRC = {"A": R + "knockout_regrow/synthetic_worlds.csv",
       "L": R + "knockout_regrow_male_cns/synthetic_worlds_L.csv",
       "R": R + "knockout_regrow_male_cns/synthetic_worlds_R.csv"}
GRID = [(0.5, "M0.5"), (0.6, "M0.6"), (0.75, "M0.75"), (0.85, "M0.85"), (1.0, "M1.0")]
PK = ["rule #2.1", "BF_1", "BF_2", "BF_3", "BF_4"]


def load(p):
    W = defaultdict(dict)
    for r in csv.DictReader(open(p, encoding="utf-8", newline="")):
        W[(r["family"], int(r["j"]), int(r["seed"]))][r["predictor"]] = r
    return W


D = {k: load(v) for k, v in SRC.items()}


def worlds(b, fam):
    return sorted([(k, v) for k, v in D[b].items() if k[0] == fam], key=lambda x: x[0][1])


def legS(r):
    return int(r["n_valid_shuffles"]) >= 1 and int(r["n_ge"]) == 0


def Rletter(r):
    return legS(r) and float(r["p_P"]) <= 0.01


for b in D:
    for k, v in D[b].items():
        lab = v["rule #2.1"]["label"]
        both = Rletter(v["rule #2.1"]) and Rletter(v["BF_1"])
        assert (lab == "R") == both, (b, k, lab)
print("label R == R-letter on both D1 candidates: verified for all worlds in A, L, R")

tab = {}
print("\n== seen per predictor / R-letter per D1 candidate / label R ==")
for g, fam in [(0.0, "Nf")] + GRID + [(2.0, "R")]:
    line = [f"{g:>4} {fam:5}"]
    for b in "ALR":
        ws = worlds(b, fam)
        n = len(ws)
        seen = {pk: sum(float(v[pk]["p_P"]) <= 0.01 for _, v in ws) for pk in PK}
        rl = {pk: sum(Rletter(v[pk]) for _, v in ws) for pk in ("rule #2.1", "BF_1")}
        nR = sum(v["rule #2.1"]["label"] == "R" for _, v in ws)
        labs = Counter(v["rule #2.1"]["label"] for _, v in ws)
        tab[(b, fam)] = dict(n=n, seen=seen, rl=rl, nR=nR, labs=labs, seeds=[k[2] for k, _ in ws])
        line.append(f"{b}: seen r/B1/B2/B3/B4 {'/'.join(str(seen[p]) for p in PK)} | Rlet r,B1 "
                    f"{rl['rule #2.1']},{rl['BF_1']} | R {nR}/{n} | "
                    f"{''.join(f'{L}{labs.get(L, 0)}' for L in 'RWGU')} seeds "
                    f"{min(tab[(b, fam)]['seeds'])}-{max(tab[(b, fam)]['seeds'])}")
    print("\n   ".join(line))


def fe(a, n1, c, n2):
    t = [[a, n1 - a], [c, n2 - c]]
    return fisher_exact(t, alternative="two-sided")[1], fisher_exact(t, alternative="greater")[1]


def strat_exact(pairs):
    dist = {0: 1.0}
    obs = 0
    E = 0
    for xa, na, xm, nm in pairs:
        m = xa + xm
        N = na + nm
        lo, hi = max(0, m - nm), min(na, m)
        pmf = {k: hypergeom.pmf(k, N, m, na) for k in range(lo, hi + 1)}
        E += sum(k * p for k, p in pmf.items())
        nd = defaultdict(float)
        for t, p in dist.items():
            for k, q in pmf.items():
                nd[t + k] += p * q
        dist = dict(nd)
        obs += xa
    p_greater = sum(p for t, p in dist.items() if t >= obs)
    pobs = dist[obs]
    p_two = sum(p for t, p in dist.items() if p <= pobs * (1 + 1e-9))
    return obs, E, p_greater, p_two, dist


print("\n== Fisher exact per gamma and stratified exact over the dense grid ==")
for what in ["rule #2.1", "BF_1", "BF_2", "BF_3", "BF_4", "Rlet rule", "Rlet BF_1", "label R"]:
    for m in "LR":
        pairs = []
        row = []
        for g, fam in GRID:
            a, mm = tab[("A", fam)], tab[(m, fam)]
            if what.startswith("Rlet"):
                key = "rule #2.1" if what.endswith("rule") else "BF_1"
                xa, xm = a["rl"][key], mm["rl"][key]
            elif what == "label R":
                xa, xm = a["nR"], mm["nR"]
            else:
                xa, xm = a["seen"][what], mm["seen"][what]
            pairs.append((xa, 5, xm, 5))
            p2, p1 = fe(xa, 5, xm, 5)
            row.append(f"{g}: {xa} v {xm} p2={p2:.3f} p1={p1:.3f}")
        obs, E, pg, pt, _ = strat_exact(pairs)
        print(f"{what:10} A vs {m}: " + "; ".join(row)
              + f" || pooled: A {obs}/25 v {sum(p[2] for p in pairs)}/25, E[A]={E:.2f}, "
                f"exact p1={pg:.3f}, p2={pt:.3f}")

print("\n== L vs R paired by seed ==")
for what in ["rule #2.1", "BF_1", "label R"]:
    b01 = b10 = 0
    rows = []
    for g, fam in GRID:
        wl = {k[2]: v for k, v in worlds("L", fam)}
        wr = {k[2]: v for k, v in worlds("R", fam)}
        assert set(wl) == set(wr)
        for s in sorted(wl):
            if what == "label R":
                xl, xr = wl[s]["rule #2.1"]["label"] == "R", wr[s]["rule #2.1"]["label"] == "R"
            else:
                xl, xr = float(wl[s][what]["p_P"]) <= 0.01, float(wr[s][what]["p_P"]) <= 0.01
            if xl and not xr:
                b10 += 1
                rows.append(f"{s}:L only")
            if xr and not xl:
                b01 += 1
                rows.append(f"{s}:R only")
    n = b01 + b10
    p = min(1, 2 * sum(math.comb(n, i) for i in range(0, min(b01, b10) + 1)) / 2 ** n) if n else 1
    print(what, "L-only", b10, "R-only", b01, "exact McNemar p", round(p, 3), rows)


def ranks(x):
    x = np.asarray(x, float)
    o = np.argsort(x, kind="mergesort")
    r = np.empty(len(x))
    xs = x[o]
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and xs[j + 1] == xs[i]:
            j += 1
        r[o[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    return r


def strat_rank(strata):
    dist = {0.0: 1.0}
    obs = 0.0
    for xa, xm in strata:
        allv = list(xa) + list(xm)
        r = ranks(allv)
        na = len(xa)
        obs += r[:na].sum()
        c = Counter()
        combs = list(itertools.combinations(range(len(allv)), na))
        for cmb in combs:
            c[round(r[list(cmb)].sum(), 6)] += 1
        nd = defaultdict(float)
        for t, p in dist.items():
            for k, q in c.items():
                nd[round(t + k, 6)] += p * q / len(combs)
        dist = dict(nd)
    obs = round(obs, 6)
    E = sum(t * p for t, p in dist.items())
    pg = sum(p for t, p in dist.items() if t >= obs - 1e-9)
    pt = sum(p for t, p in dist.items() if abs(t - E) >= abs(obs - E) - 1e-9)
    return obs, E, pg, pt


print("\n== continuous per world ==")
for pk in ["rule #2.1", "BF_1"]:
    for g, fam in GRID:
        s = []
        for b in "ALR":
            ws = worlds(b, fam)
            s.append(f"{b} AUC " + ",".join(f"{float(v[pk]['auc']):.3f}" for _, v in ws)
                     + " | pP " + ",".join(f"{float(v[pk]['p_P']):.4f}" for _, v in ws)
                     + " | lam " + ",".join(v[pk]['lambda_ko'] for _, v in ws))
        print(pk, g, "\n   " + "\n   ".join(s))
for pk in ["rule #2.1", "BF_1"]:
    for col, sign in [("auc", 1), ("p_P", -1)]:
        for m in "LR":
            strata = []
            per = []
            for g, fam in GRID:
                xa = [sign * float(v[pk][col]) for _, v in worlds("A", fam)]
                xm = [sign * float(v[pk][col]) for _, v in worlds(m, fam)]
                o, E, pg, pt = strat_rank([(xa, xm)])
                per.append(f"{g}: W_A={o:g} p1={pg:.3f} p2={pt:.3f}")
                strata.append((xa, xm))
            o, E, pg, pt = strat_rank(strata)
            print(f"{pk} {col} A vs {m}: " + "; ".join(per)
                  + f" || stratified: A rank sum {o:g} (E {E:g}), p1(A higher)={pg:.3f}, p2={pt:.3f}")

for pk in ["rule #2.1", "BF_1"]:
    dd = []
    l, r = [], []
    for g, fam in GRID:
        wl = {k[2]: v for k, v in worlds("L", fam)}
        wr = {k[2]: v for k, v in worlds("R", fam)}
        for s in sorted(wl):
            l.append(float(wl[s][pk]["auc"]))
            r.append(float(wr[s][pk]["auc"]))
    dd = np.array(l) - np.array(r)
    print(pk, "L-R AUC paired diffs: mean", dd.mean().round(4), "sd", dd.std(ddof=1).round(4),
          "median abs", np.median(abs(dd)).round(4), "max abs", abs(dd).max().round(4),
          "wilcoxon p", round(wilcoxon(dd).pvalue, 3))
    lc, rc = [], []
    for i in range(5):
        L_ = np.array(l[5 * i:5 * i + 5])
        R_ = np.array(r[5 * i:5 * i + 5])
        lc += list(L_ - L_.mean())
        rc += list(R_ - R_.mean())
    print("  L-R AUC corr raw", np.corrcoef(l, r)[0, 1].round(3), "within-gamma centred",
          np.corrcoef(lc, rc)[0, 1].round(3))
    for b in "ALR":
        sds = [np.std([float(v[pk]['auc']) for _, v in worlds(b, fam)], ddof=1) for _, fam in GRID]
        means = [np.mean([float(v[pk]['auc']) for _, v in worlds(b, fam)]) for _, fam in GRID]
        print("  ", b, "mean AUC per gamma", [round(x, 3) for x in means], "sd", [round(x, 3) for x in sds])
for b in "ALR":
    for fam in ["Nf", "M0.5", "M0.75", "M1.0"]:
        print(b, fam, "outside_density", [round(float(v['rule #2.1']['outside_density']), 4) for _, v in worlds(b, fam)])
