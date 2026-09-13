import math, numpy as np
from crit_rho import mc, rho_from_d2
# t quantile by numerical integration of the Student-t density (no scipy)
def t_pdf(x, df):
    return math.gamma((df+1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2))*(1+x*x/df)**(-(df+1)/2)
def t_ppf(p, df):
    lo, hi = 0.0, 20.0
    xs = np.linspace(0, 20, 400001); ys = np.array([t_pdf(x, df) for x in xs])
    cdf = 0.5 + np.cumsum((ys[1:]+ys[:-1])/2*(xs[1]-xs[0]))
    return xs[1:][np.searchsorted(cdf, p)]
for n in [8,10,12,16,20]:
    t = t_ppf(0.95, n-2); r_t = t/math.sqrt(n-2+t*t)
    line = f"N={n:2d} t(0.95,df={n-2})={t:.3f} rho_t_approx={r_t:.4f}"
    if n > 10:
        r2, p2 = mc(n, seed=1); line += f"  MC seed1 crit={r2:.4f} P={p2:.4f}"
    print(line)
