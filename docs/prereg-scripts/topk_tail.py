# Exact hypergeometric tails for hypothesis (b2) of
# docs/preregistration-cheap-vs-expensive.md: X = |Top-k(cheap) intersect Top-k(expensive)|
# under H0 (uniform random ranking) is Hypergeometric(N, k, k):
#     P(X = x) = C(k, x) * C(N - k, k - x) / C(N, k).
# One-sided test, H1: X larger than chance, alpha = 0.05; reject if P(X >= x_obs) <= 0.05.
#
# Pure standard library on purpose: no numpy, no scipy. Fractions are exact, so the
# decimals printed below are rounded from exact rationals and not from floating point
# accumulation. Run with the same interpreter as crit_rho.py:
#   C:/Users/mikha/AppData/Local/Programs/Python/Python312/python.exe topk_tail.py
import itertools
import sys
from fractions import Fraction
from math import comb

NS = (8, 10, 12, 16, 20)
KS = (2, 3)
ALPHA = Fraction(5, 100)


def pmf(N, k, x):
    """P(X = x) for X ~ Hypergeometric(N, k, k), exact."""
    if x < 0 or x > k or k - x > N - k:
        return Fraction(0, 1)
    return Fraction(comb(k, x) * comb(N - k, k - x), comb(N, k))


def upper_tail(N, k, x):
    """P(X >= x), exact."""
    return sum((pmf(N, k, j) for j in range(x, k + 1)), Fraction(0, 1))


def brute_force_distribution(N, k):
    """Enumerate all N! rankings and count the overlap, no formula involved.

    The cheap ranking is fixed as the identity; a uniformly random expensive ranking is a
    permutation p, so Top-k(cheap) = {0..k-1} and Top-k(expensive) = {i : p[i] < k}.
    """
    counts = [0] * (k + 1)
    total = 0
    for p in itertools.permutations(range(N)):
        x = sum(1 for i in range(k) if p[i] < k)
        counts[x] += 1
        total += 1
    return [Fraction(c, total) for c in counts], total


def main():
    print("topk_tail.py - exact hypergeometric tails for (b2)")
    print("python", sys.version.split()[0], "| executable:", sys.executable)
    print("X = |Top-k(cheap) cap Top-k(expensive)|; H0: uniform random ranking;")
    print("X ~ Hypergeometric(N, k, k); one-sided, reject if P(X >= x_obs) <= 0.05")
    print()
    header = "  {:>2}  {:>1}  {:>1}  {:>16}  {:>8}  {:>16}  {:>8}  {}".format(
        "N", "k", "x", "P(X = x)", "decimal", "P(X >= x)", "decimal", "reject at 0.05?"
    )
    print(header)
    print("  " + "-" * (len(header) - 2))
    for k in KS:
        for N in NS:
            for x in range(0, k + 1):
                p_eq = pmf(N, k, x)
                p_ge = upper_tail(N, k, x)
                rej = "yes" if p_ge <= ALPHA else "no"
                print(
                    "  {:>2}  {:>1}  {:>1}  {:>16}  {:>8}  {:>16}  {:>8}  {}".format(
                        N,
                        k,
                        x,
                        "{}/{}".format(p_eq.numerator, p_eq.denominator),
                        "{:.4f}".format(float(p_eq)),
                        "{}/{}".format(p_ge.numerator, p_ge.denominator),
                        "{:.4f}".format(float(p_ge)),
                        rej,
                    )
                )
            print("  " + "-" * (len(header) - 2))
    print()
    print("Smallest x that rejects at alpha = 0.05, per (N, k):")
    for k in KS:
        for N in NS:
            xs = [x for x in range(0, k + 1) if upper_tail(N, k, x) <= ALPHA]
            if xs:
                x0 = min(xs)
                t = upper_tail(N, k, x0)
                print(
                    "  N = {:>2}, k = {}: x >= {}  (P = {}/{} = {:.4f}){}".format(
                        N, k, x0, t.numerator, t.denominator, float(t),
                        "  - only X = k rejects" if x0 == k else "",
                    )
                )
            else:
                print("  N = {:>2}, k = {}: no x rejects at alpha = 0.05".format(N, k))
    print()
    print("Self-check: all 8! = 40320 permutations enumerated, overlaps counted,")
    print("compared with the hypergeometric pmf term by term.")
    for k in KS:
        emp, total = brute_force_distribution(8, k)
        for x in range(0, k + 1):
            theo = pmf(8, k, x)
            assert emp[x] == theo, (8, k, x, emp[x], theo)
            print(
                "  N = 8, k = {}, x = {}: enumerated {}/{} == formula {}/{}  OK".format(
                    k, x,
                    emp[x].numerator, emp[x].denominator,
                    theo.numerator, theo.denominator,
                )
            )
        assert sum(emp, Fraction(0, 1)) == 1
        print("  (permutations counted: {}; probabilities sum to 1)".format(total))
    print()
    print("Self-check passed: enumeration and formula agree exactly for N = 8, k = 2 and k = 3.")


if __name__ == "__main__":
    main()
