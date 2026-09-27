import itertools
from collections import defaultdict
import numpy as np
from scipy.stats import fisher_exact, hypergeom, binom, mannwhitneyu

# 1. Fisher 5 v 5: which tables reject at two-sided 0.05; power when p_A = 1 and p_A = 0.9
rej = {}
for a in range(6):
    for m in range(6):
        p2 = fisher_exact([[a, 5 - a], [m, 5 - m]])[1]
        p1 = fisher_exact([[a, 5 - a], [m, 5 - m]], alternative="greater")[1]
        rej[(a, m)] = (p2, p1)
print("tables (A seen, male seen) with two-sided p <= 0.05:",
      sorted(k for k, v in rej.items() if v[0] <= 0.05))
print("tables with one-sided (A>male) p <= 0.05:",
      sorted(k for k, v in rej.items() if v[1] <= 0.05))
print("difference 1 world (5v4):", rej[(5, 4)], " 2 worlds (5v3):", rej[(5, 3)], "(3v1)", rej[(3, 1)])


def power_fisher(pa, pm, side=1):
    s = 0
    for a in range(6):
        for m in range(6):
            p = rej[(a, m)][side]
            if p <= 0.05:
                s += binom.pmf(a, 5, pa) * binom.pmf(m, 5, pm)
    return s


for pa in (1.0, 0.9, 0.8):
    pms = np.linspace(0, pa, 101)
    pw = [power_fisher(pa, pm, 1) for pm in pms]
    best = max(pm for pm, w in zip(pms, pw) if w >= 0.8) if any(w >= 0.8 for w in pw) else None
    print(f"one-sided Fisher, p_A={pa}: largest p_M with power>=0.8: {best}; "
          f"power at p_M=pa-0.2: {power_fisher(pa, max(pa - 0.2, 0), 1):.3f}; "
          f"at pa-0.4: {power_fisher(pa, max(pa - 0.4, 0), 1):.3f}")

# 2. stratified exact (sum of A's seen, conditional on margins), power by simulation
rng = np.random.default_rng(12345)


def strat_p1(xa, xm):
    dist = {0: 1.0}
    for a, m in zip(xa, xm):
        t = a + m
        lo, hi = max(0, t - 5), min(5, t)
        pmf = {k: hypergeom.pmf(k, 10, t, 5) for k in range(lo, hi + 1)}
        nd = defaultdict(float)
        for s, p in dist.items():
            for k, q in pmf.items():
                nd[s + k] += p * q
        dist = nd
    obs = sum(xa)
    return sum(p for s, p in dist.items() if s >= obs)


cache = {}


def cp(xa, xm):
    k = (tuple(xa), tuple(xm))
    if k not in cache:
        cache[k] = strat_p1(xa, xm)
    return cache[k]


def power_strat(pa, pm, reps=20000):
    hit = 0
    for _ in range(reps):
        xa = rng.binomial(5, pa)
        xm = rng.binomial(5, pm)
        hit += cp(xa, xm) <= 0.05
    return hit / reps


PA = np.array([0.2, 0.6, 1.0, 1.0, 1.0])       # A's observed fractions (plug-in)
scen = {
    "male = A (null)": PA,
    "male one grid step right (0, .2, .6, 1, 1)": np.array([0.0, 0.2, 0.6, 1.0, 1.0]),
    "male = observed L fractions (0, .4, 1, .8, 1)": np.array([0.0, 0.4, 1.0, 0.8, 1.0]),
    "uniform -0.2 (0, .4, .8, .8, .8)": np.clip(PA - 0.2, 0, 1),
    "uniform -0.4": np.clip(PA - 0.4, 0, 1),
    "two steps right (0, 0, .2, .6, 1)": np.array([0.0, 0.0, 0.2, 0.6, 1.0]),
}
for name, pm in scen.items():
    print(f"stratified exact one-sided 0.05, A true {PA.tolist()}, {name}: power {power_strat(PA, pm):.3f}")

# 3. continuous: stratified rank-sum test power for a mean AUC shift, per-world sd 0.07 (A's within-gamma sd)
def strat_rank_p1(xs):
    # normal approx of van Elteren (equal n) for speed in simulation; exact values reported elsewhere
    W = 0.0
    E = 0.0
    V = 0.0
    for xa, xm in xs:
        allv = np.concatenate([xa, xm])
        r = allv.argsort().argsort() + 1
        W += r[:5].sum()
        E += 5 * 11 / 2
        V += 5 * 5 * 11 / 12
    z = (W - E) / np.sqrt(V)
    from scipy.stats import norm
    return 1 - norm.cdf(z)


for sd in (0.07,):
    for d in (0.02, 0.04, 0.06, 0.08, 0.10):
        hits = 0
        reps = 5000
        for _ in range(reps):
            xs = [(rng.normal(0, sd, 5) + d, rng.normal(0, sd, 5)) for _ in range(5)]
            hits += strat_rank_p1(xs) <= 0.05
        print(f"stratified rank-sum (normal approx), 5 strata x 5 v 5, sd {sd}, uniform AUC shift {d}: "
              f"power {hits / reps:.3f}")
    for d in (0.05, 0.08, 0.10, 0.12, 0.15):
        hits = 0
        for _ in range(5000):
            hits += mannwhitneyu(rng.normal(0, sd, 5) + d, rng.normal(0, sd, 5),
                                 alternative="greater", method="exact").pvalue <= 0.05
        print(f"single gamma exact MWU 5 v 5, sd {sd}, shift {d}: power {hits / 5000:.3f}")
