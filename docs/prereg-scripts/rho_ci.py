# One-sided 95 % upper confidence bound on Spearman rho at the primary rung C3, for the
# second bullet of section 5 of docs/preregistration-cheap-vs-expensive.md:
#
#   "If rho at the primary rung does not reach critical: the outcome is 'No cheap
#    surrogate at <= 10 % of expensive on this substrate' only if the upper bound of the
#    one-sided 95 % permutation confidence interval on rho at the primary rung is below
#    0.6; otherwise the outcome is `inconclusive - underpowered`."
#
# WHAT THAT PHRASE COULD NOT MEAN LITERALLY, AND HOW IT IS RESOLVED HERE.
# A permutation test of rank correlation randomises the pairing and so generates the
# distribution of rho under H0: rho = 0 only. It yields a p-value, not an interval: there
# is no non-null permutation distribution to invert, because permuting the labels destroys
# exactly the association whose magnitude an interval would have to bound. So the words
# "permutation confidence interval" in section 5 do not name a computable object, and the
# design below was fixed by CC, the orchestrator, and is marked "(proposed - fix in
# review)" for the reviewers exactly as the rest of section 5's open marks are.
#
# PRIMARY construction, the only decision input:
#     z     = atanh(rho_obs)            (rho_obs clipped to +-0.999999 first)
#     se    = 1.06 / sqrt(N - 3)        Fieller-Hartley-Pearson
#     upper = tanh(z + 1.6449 * se)     one-sided 95 %
# The 1.06/sqrt(N-3) standard error is not a new choice: it is the same Fisher-z standard
# error section 4 already uses for the registered power figures under floor option (B)
# ("CC's recomputation with se = 1.06/sqrt(N - 3) and the critical values of the table
# gives 32.6 % / 41.2 %"). Using it here keeps the interval and the registered power on one
# and the same approximation, so the section 5 band and the section 4 power statement
# cannot disagree with each other.
#
# SECOND COLUMN, reported, not decisive: Bonett & Wright (2000) se = sqrt((1 + rho^2/2)/(N - 3)).
# CONTROL, reported, not decisive: percentile bootstrap. B = 20,000 resamples of the N
# (cheap, expensive) pairs with replacement, seed 0, Spearman with midranks (ties do arise
# inside resamples), upper bound = the 95th percentile of the bootstrap rho distribution.
# It is a control on the Fisher-z approximation, not a decision input: at N = 8 or 10 a
# percentile bootstrap of a rank statistic is badly discrete and known to be
# anticonservative, which is why it does not decide anything here.
#
# ALTERNATIVES NOT TAKEN, named so the reviewers can substitute one:
#   (1) inverting a *non-null* permutation scheme (e.g. rotation / Fisher-z-shifted
#       resampling of the ranks) to obtain a genuine permutation interval;
#   (2) BCa or studentised bootstrap instead of the plain percentile control;
#   (3) an exact interval from the null distribution of Spearman's S by test inversion
#       against a shift family, which needs a family the pre-registration does not name;
#   (4) taking Bonett-Wright as primary and Fieller-Hartley-Pearson as the second column;
#   (5) the plain Fisher se = 1/sqrt(N - 3), which is the Pearson case and is known to be
#       too small for a rank correlation - it would give a *narrower* interval and so make
#       the negative outcome easier to reach, which is why it is not used.
#
# Spearman rho is computed by ranking both lists with midranks and taking the Pearson
# correlation of the ranks. The 1 - 6*sum(d^2)/(N(N^2-1)) shortcut is WRONG under ties and
# is implemented here only as a self-test: the two agree exactly when there are no ties.
#
# Pure standard library (random, math, statistics) to match crit_rho.py and topk_tail.py:
# no numpy, no scipy. Run with the same interpreter as those:
#   C:/Users/mikha/AppData/Local/Programs/Python/Python312/python.exe rho_ci.py --table
#   C:/Users/mikha/AppData/Local/Programs/Python/Python312/python.exe rho_ci.py \
#       --cheap 1191.7 ... --expensive 1146.2 ...
#   C:/Users/mikha/AppData/Local/Programs/Python/Python312/python.exe rho_ci.py --json pairs.json
import argparse
import json
import math
import random
import statistics
import sys

try:  # section 5's own words carry a dash and a "<=" glyph; the Windows console is cp1252
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Critical one-sided rho at alpha = 0.05, hard-coded from the table in section 4 of
# docs/preregistration-cheap-vs-expensive.md ("Critical values computed on 2026-09-13 for
# this draft, not quoted from a table"): N = 8 and N = 10 exact over all N! permutations;
# N = 12 / 16 / 20 exact by a dynamic programme over subsets, Reported from Ark and Zcode.
# Any other N is refused here rather than silently approximated - section 4 says the
# critical rho for an N not in the table is computed by crit_rho.py and written into the
# pre-registration first.
CRIT_RHO = {
    8: 0.6429,
    10: 0.5636,
    12: 0.503497,
    16: 0.429412,
    20: 0.380451,
}

Z_95 = 1.6449          # one-sided 95 % normal quantile, as used for the section 4 power
RHO_CLIP = 0.999999    # atanh(+-1) is infinite; clip first
CI_THRESHOLD = 0.6     # section 5: "the upper bound ... is below 0.6"
BOOTSTRAP_B = 20000
BOOTSTRAP_SEED = 0
TABLE_NS = (8, 10, 12, 16, 20)
TABLE_GRID = 0.001


def midranks(values):
    """Ranks, ascending (rank 1 = smallest value = lowest loss = best), ties averaged."""
    n = len(values)
    order = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0  # 1-based midrank of the tied block
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def pearson(xs, ys):
    n = len(xs)
    mx = statistics.fmean(xs)
    my = statistics.fmean(ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 0.0 or syy <= 0.0:
        raise ZeroDivisionError("zero variance in one of the two rank vectors")
    return sxy / math.sqrt(sxx * syy)


def spearman(cheap, expensive):
    """Spearman rho: Pearson correlation of the midranks. Correct under ties."""
    if len(cheap) != len(expensive):
        raise ValueError("cheap and expensive must have the same length")
    if len(cheap) < 3:
        raise ValueError("need at least 3 pairs")
    return pearson(midranks(cheap), midranks(expensive))


def spearman_shortcut(cheap, expensive):
    """1 - 6*sum(d^2)/(N(N^2-1)) on midranks. WRONG under ties; self-test use only."""
    n = len(cheap)
    rc = midranks(cheap)
    re = midranks(expensive)
    d2 = sum((a - b) ** 2 for a, b in zip(rc, re))
    return 1.0 - 6.0 * d2 / (n * (n * n - 1))


def se_fhp(n):
    """Fieller-Hartley-Pearson standard error of atanh(rho_spearman). Section 4's se."""
    return 1.06 / math.sqrt(n - 3)


def se_bonett_wright(n, rho):
    """Bonett & Wright (2000) standard error of atanh(rho_spearman)."""
    return math.sqrt((1.0 + rho * rho / 2.0) / (n - 3))


def fisher_upper(rho, se):
    """One-sided 95 % upper confidence bound on rho via Fisher z."""
    r = max(-RHO_CLIP, min(RHO_CLIP, rho))
    return math.tanh(math.atanh(r) + Z_95 * se)


def bootstrap_upper(cheap, expensive, b=BOOTSTRAP_B, seed=BOOTSTRAP_SEED):
    """Percentile bootstrap upper bound (CONTROL, never a decision input).

    Resamples the N (cheap, expensive) PAIRS with replacement, so the pairing - the thing
    rho measures - is preserved and only the sample of individuals varies. A resample in
    which every drawn pair is identical has zero rank variance and no defined rho; such
    resamples are dropped and counted, and the count is printed. At N = 8 the probability
    of one is 8 * (1/8)^8 = 4.8e-7 per draw.
    """
    rng = random.Random(seed)
    n = len(cheap)
    rhos = []
    degenerate = 0
    for _ in range(b):
        idx = [rng.randrange(n) for _ in range(n)]
        c = [cheap[i] for i in idx]
        e = [expensive[i] for i in idx]
        try:
            rhos.append(spearman(c, e))
        except ZeroDivisionError:
            degenerate += 1
    rhos.sort()
    m = len(rhos)
    # 95th percentile: the smallest sample value at or below which at least 95 % of the
    # bootstrap distribution lies (ceil(0.95 * m) - 1 in 0-based index terms).
    k = max(0, min(m - 1, math.ceil(0.95 * m) - 1))
    return rhos[k], m, degenerate


def verdict(n, rho_obs, upper_primary):
    """The section 5 decision line for hypothesis (b) at the primary rung C3."""
    if n not in CRIT_RHO:
        raise ValueError(
            "N = {} is not in the section 4 critical-value table {}; compute its critical "
            "rho with crit_rho.py and write it into the pre-registration before any "
            "analysis (section 4: 'The critical rho for that N is read from the table "
            "above (or computed by the same script if N is not in the table) and written "
            "next to it')".format(n, sorted(CRIT_RHO))
        )
    crit = CRIT_RHO[n]
    if rho_obs >= crit:
        return (
            "reaches critical",
            'rho_obs {:.6f} >= critical {:.6f} at N = {} -> "A cheap surrogate exists at '
            '10 % of expensive."'.format(rho_obs, crit, n),
        )
    if upper_primary < CI_THRESHOLD:
        return (
            "No cheap surrogate",
            "rho_obs {:.6f} < critical {:.6f} and the one-sided 95 % upper bound {:.6f} "
            "is below {:.1f} -> \u201cNo cheap surrogate at \u2264 10 % of expensive on "
            "this substrate\u201d".format(rho_obs, crit, upper_primary, CI_THRESHOLD),
        )
    return (
        "inconclusive \u2014 underpowered",
        "rho_obs {:.6f} < critical {:.6f} but the one-sided 95 % upper bound {:.6f} is "
        "not below {:.1f} -> `inconclusive \u2014 underpowered` (rho below critical, but "
        "the data do not exclude a useful surrogate)".format(
            rho_obs, crit, upper_primary, CI_THRESHOLD
        ),
    )


def self_test(trials=200, n=8, seed=12345):
    """Both Spearman formulas must agree exactly when there are no ties."""
    rng = random.Random(seed)
    worst = 0.0
    for _ in range(trials):
        while True:
            cheap = [rng.uniform(1100.0, 1300.0) for _ in range(n)]
            expensive = [rng.uniform(1100.0, 1300.0) for _ in range(n)]
            if len(set(cheap)) == n and len(set(expensive)) == n:
                break
        worst = max(worst, abs(spearman(cheap, expensive) - spearman_shortcut(cheap, expensive)))
    return worst


def analyse(cheap, expensive):
    n = len(cheap)
    rho_obs = spearman(cheap, expensive)
    s_fhp = se_fhp(n)
    s_bw = se_bonett_wright(n, rho_obs)
    up_fhp = fisher_upper(rho_obs, s_fhp)
    up_bw = fisher_upper(rho_obs, s_bw)
    up_boot, kept, degenerate = bootstrap_upper(cheap, expensive)
    ties_cheap = n - len(set(cheap))
    ties_expensive = n - len(set(expensive))

    print("rho_ci.py - one-sided 95 % upper bound on Spearman rho, section 5 of")
    print("            docs/preregistration-cheap-vs-expensive.md (hypothesis (b), rung C3)")
    print("python", sys.version.split()[0], "| executable:", sys.executable)
    print()
    print("  N                              = {}".format(n))
    print("  cheap    (held-out loss at C3) = {}".format(
        " ".join("{:.6g}".format(v) for v in cheap)))
    print("  expensive (held-out loss @250k)= {}".format(
        " ".join("{:.6g}".format(v) for v in expensive)))
    print("  ties in cheap / expensive      = {} / {}".format(ties_cheap, ties_expensive))
    print("  rho_obs (midranks, Pearson of ranks) = {:.6f}".format(rho_obs))
    if ties_cheap == 0 and ties_expensive == 0:
        print("  rho_obs (1 - 6*sum(d^2) shortcut)    = {:.6f}  (agrees: no ties)".format(
            spearman_shortcut(cheap, expensive)))
    else:
        print("  shortcut formula NOT printed: ties present, the shortcut is invalid")
    print()
    print("  one-sided 95 % upper bounds on rho")
    print("    PRIMARY  Fisher z, se = 1.06/sqrt(N-3) = {:.6f}  ->  upper = {:.6f}".format(
        s_fhp, up_fhp))
    print("    second   Bonett-Wright, se            = {:.6f}  ->  upper = {:.6f}".format(
        s_bw, up_bw))
    print("    CONTROL  percentile bootstrap, B = {}, seed {}  ->  upper = {:.6f}".format(
        BOOTSTRAP_B, BOOTSTRAP_SEED, up_boot))
    print("             ({} usable resamples, {} degenerate and dropped)".format(
        kept, degenerate))
    print("    (only the PRIMARY bound enters the section 5 decision)")
    print()
    tag, line = verdict(n, rho_obs, up_fhp)  # raises if N is not in the section 4 table
    print("  critical rho at N = {} (section 4 table) = {:.6f}".format(n, CRIT_RHO[n]))
    print()
    print("  VERDICT (section 5, hypothesis (b)): {}".format(tag))
    print("    {}".format(line))

    # The control is reported whether it agrees or not. It is NOT allowed to move the
    # verdict; at N = 8 or 10 a percentile bootstrap of a rank statistic is coarse (only a
    # few hundred distinct values) and skewed upward, so a disagreement is expected rather
    # than alarming - but it is printed, because a silent control is not a control.
    agree = (up_boot < CI_THRESHOLD) == (up_fhp < CI_THRESHOLD)
    print()
    if agree:
        print("  control: the bootstrap upper bound {:.6f} falls on the same side of "
              "{:.1f} as the primary bound {:.6f}.".format(up_boot, CI_THRESHOLD, up_fhp))
    else:
        print("  control: the bootstrap upper bound {:.6f} falls on the OPPOSITE side of "
              "{:.1f} from the primary bound {:.6f}.".format(up_boot, CI_THRESHOLD, up_fhp))
        print("           The verdict above stands - the bootstrap is a control, not a "
              "decision input (see the header of this file) - but the disagreement is "
              "reported alongside the verdict and never suppressed.")
    return rho_obs, up_fhp, up_bw, up_boot, tag


def reach(n, threshold=CI_THRESHOLD, grid=TABLE_GRID):
    """Largest rho_obs on the grid whose PRIMARY upper bound is still below `threshold`.

    Searched on a 0.001 grid from -1 upward, as registered. Returns None if even
    rho_obs = -1 gives an upper bound at or above the threshold.
    """
    se = se_fhp(n)
    best = None
    steps = int(round(2.0 / grid))
    for i in range(steps + 1):
        r = -1.0 + i * grid
        if fisher_upper(r, se) < threshold:
            best = r
        else:
            break
    return best


def table():
    print("rho_ci.py --table - the reach of the negative outcome of section 5")
    print("python", sys.version.split()[0], "| executable:", sys.executable)
    print()
    print("For each N: the critical rho of section 4; the PRIMARY one-sided 95 % upper")
    print("bound at rho_obs = 0; and the LARGEST rho_obs (0.001 grid, searched from -1")
    print("upward) whose PRIMARY upper bound is still below 0.6 - i.e. the largest")
    print("observed rho for which section 5 permits \u201cNo cheap surrogate\u201d rather")
    print("than `inconclusive \u2014 underpowered`.")
    print()
    hdr = "  {:>2}  {:>10}  {:>12}  {:>13}  {:>13}  {}".format(
        "N", "crit rho", "se=1.06/sqrt", "upper(rho=0)", "largest rho", "upper at that rho")
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    for n in TABLE_NS:
        se = se_fhp(n)
        u0 = fisher_upper(0.0, se)
        r = reach(n)
        if r is None:
            print("  {:>2}  {:>10.6f}  {:>12.6f}  {:>13.6f}  negative outcome unreachable "
                  "at this N".format(n, CRIT_RHO[n], se, u0))
        else:
            print("  {:>2}  {:>10.6f}  {:>12.6f}  {:>13.6f}  {:>13.3f}  {:.6f}".format(
                n, CRIT_RHO[n], se, u0, r, fisher_upper(r, se)))
    print("  " + "-" * (len(hdr) - 2))
    print()
    for n in TABLE_NS:
        r = reach(n)
        if r is None:
            print("  N = {:>2}: negative outcome unreachable at this N".format(n))
        elif r < 0:
            print("  N = {:>2}: \u201cNo cheap surrogate\u201d needs rho_obs <= {:.3f} - a "
                  "NEGATIVE observed rank correlation; any rho_obs above it that fails "
                  "the critical value {:.6f} lands in `inconclusive \u2014 underpowered`."
                  .format(n, r, CRIT_RHO[n]))
        else:
            print("  N = {:>2}: \u201cNo cheap surrogate\u201d needs rho_obs <= {:.3f}; "
                  "between {:.3f} and the critical value {:.6f} the outcome is "
                  "`inconclusive \u2014 underpowered`.".format(n, r, r, CRIT_RHO[n]))


def main(argv=None):
    p = argparse.ArgumentParser(
        description="One-sided 95 % upper confidence bound on Spearman rho for section 5 "
                    "of docs/preregistration-cheap-vs-expensive.md.")
    p.add_argument("--cheap", nargs="+", type=float,
                   help="held-out losses at the cheap rung C3, one per individual")
    p.add_argument("--expensive", nargs="+", type=float,
                   help="held-out losses at 250,000 iterations, same individuals, same order")
    p.add_argument("--json", metavar="PATH",
                   help='read {"cheap": [...], "expensive": [...]} from this file')
    p.add_argument("--table", action="store_true",
                   help="print the reach of the negative outcome for N = 8, 10, 12, 16, 20")
    p.add_argument("--no-self-test", action="store_true",
                   help="skip the no-ties agreement self-test of the two Spearman formulas")
    args = p.parse_args(argv)

    if not args.no_self_test:
        worst = self_test()
        print("self-test: midrank-Pearson vs 1-6*sum(d^2) shortcut agree on 200 tie-free "
              "N = 8 pairs, max |difference| = {:.3g}  OK".format(worst))
        if worst > 1e-12:
            print("self-test FAILED", file=sys.stderr)
            return 2
        print()

    if args.table:
        table()
        return 0

    cheap = expensive = None
    if args.json:
        with open(args.json, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
        cheap = [float(v) for v in payload["cheap"]]
        expensive = [float(v) for v in payload["expensive"]]
    if args.cheap is not None or args.expensive is not None:
        if cheap is not None:
            p.error("give --json or --cheap/--expensive, not both")
        if args.cheap is None or args.expensive is None:
            p.error("--cheap and --expensive must both be given")
        cheap, expensive = args.cheap, args.expensive
    if cheap is None:
        p.error("nothing to do: give --cheap/--expensive, --json PATH, or --table")
    if len(cheap) != len(expensive):
        p.error("--cheap has {} values but --expensive has {}".format(len(cheap), len(expensive)))
    if len(cheap) not in CRIT_RHO:
        p.error(
            "N = {} is not in the section 4 critical-value table {}. Section 4: the "
            "critical rho for an N not in the table is computed by crit_rho.py and "
            "written into the pre-registration before any analysis. Refusing to guess."
            .format(len(cheap), sorted(CRIT_RHO)))
    analyse(cheap, expensive)
    return 0


if __name__ == "__main__":
    sys.exit(main())
