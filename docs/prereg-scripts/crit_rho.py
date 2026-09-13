# Exact one-sided critical Spearman rho at alpha=0.05 by full permutation for N<=10,
# Monte Carlo (2e6 draws) for N>10, plus scipy t-approximation as a cross-check.
import itertools, math, sys
import numpy as np
try:
    from scipy import stats
    have_scipy = True
except Exception:
    have_scipy = False
print("scipy available:", have_scipy, "numpy", np.__version__)
def rho_from_d2(n, d2): return 1 - 6*d2/(n*(n*n-1))
def exact(n, alpha=0.05):
    base = np.arange(n)
    d2s = np.fromiter((int(((np.array(p)-base)**2).sum()) for p in itertools.permutations(range(n))), dtype=np.int64)
    rhos = np.sort(rho_from_d2(n, d2s))[::-1]
    total = len(rhos)
    # smallest rho such that P(rho_perm >= rho) <= alpha
    vals, counts = np.unique(rhos, return_counts=True)
    vals = vals[::-1]; counts = counts[::-1]
    cum = np.cumsum(counts)/total
    ok = vals[cum <= alpha]
    return ok[-1], cum[cum <= alpha][-1]
def mc(n, draws=2_000_000, alpha=0.05, seed=0):
    rng = np.random.default_rng(seed)
    base = np.arange(n)
    rhos = np.empty(draws)
    perms = np.argsort(rng.random((draws, n)), axis=1)
    d2 = ((perms - base)**2).sum(axis=1)
    rhos = rho_from_d2(n, d2)
    vals, counts = np.unique(rhos, return_counts=True)
    vals = vals[::-1]; counts = counts[::-1]
    cum = np.cumsum(counts)/draws
    ok = vals[cum <= alpha]
    return ok[-1], cum[cum <= alpha][-1]
for n in [8, 10, 12, 16, 20]:
    if n <= 10:
        r, p = exact(n); how = "exact permutation (%d perms)" % math.factorial(n)
    else:
        r, p = mc(n); how = "Monte Carlo 2e6 perms"
    tapprox = None
    if have_scipy:
        t = stats.t.ppf(0.95, n-2)
        tapprox = t/math.sqrt(n-2+t*t)
    print(f"N={n:2d}  crit_rho={r:.4f}  P(rho>=crit)={p:.4f}  [{how}]  t-approx={tapprox}")
