import csv
import numpy as np
from scipy.stats import fisher_exact, binom
n = 20
rej = np.zeros((n + 1, n + 1), bool)
for a in range(n + 1):
    for m in range(n + 1):
        rej[a, m] = fisher_exact([[a, n - a], [m, n - m]], alternative="greater")[1] <= 0.05
def pw(pa, pm):
    return sum(binom.pmf(a, n, pa) * binom.pmf(m, n, pm) for a in range(n + 1) for m in range(n + 1) if rej[a, m])
for pa in (1.0, 0.95, 0.9):
    best = max((pm for pm in np.linspace(0, pa, 201) if pw(pa, pm) >= 0.8), default=None)
    print(pa, "largest pm with power>=.8:", round(best, 3), "diff", round(pa - best, 3))
R = "C:/Users/mikha/Documents/dpc-research/connectome-seed/results/genome/c6/checks/knockout_regrow/synthetic_worlds.csv"
v = [float(r["outside_density"]) for r in csv.DictReader(open(R, encoding="utf-8")) if r["family"] == "Nf" and r["predictor"] == "rule #2.1"]
print("A Nf mean density", np.mean(v))
