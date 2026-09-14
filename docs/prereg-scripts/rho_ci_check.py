# Checks for rho_ci.py - the one-sided 95 % upper confidence bound on Spearman rho used by
# the second bullet of section 5 of docs/preregistration-cheap-vs-expensive.md.
#
# Every check prints OK or FAIL; the script exits non-zero if any check FAILs. Pure
# standard library, same interpreter as crit_rho_check.py and topk_tail.py:
#   C:/Users/mikha/AppData/Local/Programs/Python/Python312/python.exe rho_ci_check.py
#
# The checks, in the order of the brief:
#   (1) the two Spearman formulas agree on 1,000 random tie-free N = 8 pairs;
#   (2) positive controls: rho_obs = 1 -> primary upper = 1 within 1e-6; identical lists
#       -> rho = 1; reversed lists -> rho = -1;
#   (3) the Fisher-z upper bound at rho_obs = 0 for N = 8 and N = 10, printed to 4
#       decimals and compared with the closed form tanh(1.6449 * 1.06 / sqrt(N - 3));
#   (4) the bootstrap is deterministic: two runs with seed 0 give identical output;
#   (5) a fabricated N = 8 example with rho_obs between -0.2 and 0.2 whose verdict is
#       `inconclusive - underpowered`, and an N = 10 example that reaches the negative
#       outcome if the table says it is reachable at N = 10.
#
# The data in check (5) are FABRICATED for the purpose of exercising the decision rule.
# They are not measurements of any flyvis individual. Only run 0 / run 0' losses in
# section 6 of the pre-registration are real, and this file uses none of them as a pair.
import math
import random
import sys

from rho_ci import (
    BOOTSTRAP_B,
    BOOTSTRAP_SEED,
    CI_THRESHOLD,
    CRIT_RHO,
    Z_95,
    bootstrap_upper,
    fisher_upper,
    midranks,
    reach,
    se_bonett_wright,
    se_fhp,
    spearman,
    spearman_shortcut,
    verdict,
)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

FAILURES = []


def report(name, ok, detail=""):
    status = "OK" if ok else "FAIL"
    if not ok:
        FAILURES.append(name)
    print("  [{}] {}{}".format(status, name, ("  " + detail) if detail else ""))


print("rho_ci_check.py - checks for rho_ci.py")
print("python", sys.version.split()[0], "| executable:", sys.executable)
print()

# ---------------------------------------------------------------- (1) no-tie equality
print("(1) midrank-Pearson Spearman == 1 - 6*sum(d^2)/(N(N^2-1)) when there are no ties")
rng = random.Random(1)
worst = 0.0
n_trials = 1000
for _ in range(n_trials):
    while True:
        cheap = [rng.uniform(1100.0, 1300.0) for _ in range(8)]
        expensive = [rng.uniform(1100.0, 1300.0) for _ in range(8)]
        if len(set(cheap)) == 8 and len(set(expensive)) == 8:
            break
    worst = max(worst, abs(spearman(cheap, expensive) - spearman_shortcut(cheap, expensive)))
report("1,000 random tie-free N = 8 pairs agree",
       worst <= 1e-12, "max |difference| = {:.3g}".format(worst))

# a tied case, to show the shortcut is the one that is wrong (not a pass/fail, a witness)
tied_cheap = [1.0, 2.0, 2.0, 4.0, 5.0, 6.0, 7.0, 8.0]
tied_expensive = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
print("      witness, with one tie in cheap: midrank-Pearson {:.6f} vs shortcut {:.6f} "
      "(they differ, as expected)".format(
          spearman(tied_cheap, tied_expensive), spearman_shortcut(tied_cheap, tied_expensive)))
print()

# ---------------------------------------------------------------- (2) positive controls
print("(2) positive controls")
ident = [1191.7, 1190.2, 1195.4, 1188.9, 1193.1, 1189.5, 1196.8, 1192.3]
rho_ident = spearman(ident, ident)
report("identical lists -> rho = 1", abs(rho_ident - 1.0) <= 1e-12,
       "rho = {:.12f}".format(rho_ident))

rev_expensive = list(reversed(sorted(ident)))
rev_cheap = sorted(ident)
rho_rev = spearman(rev_cheap, rev_expensive)
report("reversed lists -> rho = -1", abs(rho_rev + 1.0) <= 1e-12,
       "rho = {:.12f}".format(rho_rev))

for n in sorted(CRIT_RHO):
    up = fisher_upper(1.0, se_fhp(n))
    report("rho_obs = 1 at N = {:>2} -> primary upper = 1 within 1e-6".format(n),
           abs(up - 1.0) <= 1e-6, "upper = {:.12f}, 1 - upper = {:.3g}".format(up, 1.0 - up))
    up_bw = fisher_upper(1.0, se_bonett_wright(n, 1.0))
    report("rho_obs = 1 at N = {:>2} -> Bonett-Wright upper = 1 within 1e-6".format(n),
           abs(up_bw - 1.0) <= 1e-6, "upper = {:.12f}".format(up_bw))

# the identical-list case must be the "reaches critical" branch at both reachable N
tag_ident, _ = verdict(8, rho_ident, fisher_upper(rho_ident, se_fhp(8)))
report("identical lists at N = 8 -> verdict 'reaches critical'",
       tag_ident == "reaches critical", "verdict = {}".format(tag_ident))
print()

# ---------------------------------------------------------------- (3) upper at rho_obs = 0
print("(3) Fisher-z upper bound at rho_obs = 0, against the closed form "
      "tanh(1.6449 * 1.06 / sqrt(N - 3))")
for n in (8, 10):
    got = fisher_upper(0.0, se_fhp(n))
    closed = math.tanh(Z_95 * 1.06 / math.sqrt(n - 3))
    print("      N = {:>2}: upper(rho_obs = 0) = {:.4f}   (closed form {:.4f}; "
          "full precision {:.12f} vs {:.12f})".format(n, got, closed, got, closed))
    report("N = {:>2} upper(rho_obs = 0) matches the closed form".format(n),
           abs(got - closed) <= 1e-12, "|difference| = {:.3g}".format(abs(got - closed)))
    side = "above" if got >= CI_THRESHOLD else "below"
    print("      N = {:>2}: that bound is {} the 0.6 threshold of section 5, so rho_obs = 0 "
          "gives `{}`".format(
              n, side,
              "inconclusive \u2014 underpowered" if got >= CI_THRESHOLD else "No cheap surrogate"))
print()

# ---------------------------------------------------------------- (4) bootstrap determinism
print("(4) bootstrap determinism, seed {}, B = {}".format(BOOTSTRAP_SEED, BOOTSTRAP_B))
boot_cheap = [1191.74, 1192.07, 1190.55, 1193.20, 1189.88, 1194.61, 1192.99, 1190.01]
boot_expensive = [1146.20, 1158.92, 1151.70, 1164.30, 1148.81, 1141.05, 1155.40, 1147.53]
r1 = bootstrap_upper(boot_cheap, boot_expensive)
r2 = bootstrap_upper(boot_cheap, boot_expensive)
report("two runs with seed {} give identical output".format(BOOTSTRAP_SEED), r1 == r2,
       "upper = {:.12f} both times ({} usable resamples, {} dropped)".format(r1[0], r1[1], r1[2]))
r3 = bootstrap_upper(boot_cheap, boot_expensive, seed=1)
r4 = bootstrap_upper(boot_cheap, boot_expensive, seed=2)
print("      (for contrast, seed 1 -> {:.6f}, seed 2 -> {:.6f}. Seeds 0 and 1 land on the "
      "SAME value: at N = 8 the bootstrap rho distribution takes only about 330 distinct "
      "values, so its 95th percentile is coarse and often coincides across seeds. That "
      "coarseness is one reason the bootstrap is a CONTROL here and never the decision "
      "input.)".format(r3[0], r4[0]))
print()

# ---------------------------------------------------------------- (5) verdict examples
print("(5) fabricated examples exercising the section 5 decision rule")
print("      (these numbers are FABRICATED to exercise the rule, not measurements)")

# N = 8 with rho_obs in (-0.2, 0.2): expect `inconclusive - underpowered`
# The cheap losses are increasing, so their ranks are 1..8 in order; the expensive losses
# follow the permutation (0, 3, 5, 6, 7, 4, 2, 1), whose sum d^2 = 84 gives
# rho = 1 - 6*84/(8*63) = exactly 0 - inside the (-0.2, 0.2) band the brief asks for.
ex8_cheap = [1189.0 + i for i in range(8)]
ex8_expensive = [1140.0 + j for j in (0, 3, 5, 6, 7, 4, 2, 1)]
rho8 = spearman(ex8_cheap, ex8_expensive)
up8 = fisher_upper(rho8, se_fhp(8))
tag8, line8 = verdict(8, rho8, up8)
print("      N = 8: rho_obs = {:.6f}, primary upper = {:.6f}, critical = {:.6f}".format(
    rho8, up8, CRIT_RHO[8]))
print("      -> {}".format(line8))
report("N = 8 example has rho_obs in (-0.2, 0.2)", -0.2 < rho8 < 0.2,
       "rho_obs = {:.6f}".format(rho8))
report("N = 8 example verdict is `inconclusive \u2014 underpowered`",
       tag8 == "inconclusive \u2014 underpowered", "verdict = {}".format(tag8))

# N = 10: reach the negative outcome if the table says it is reachable at N = 10
r10 = reach(10)
print("      N = 10: the largest rho_obs whose primary upper bound is below {:.1f} is "
      "{}".format(CI_THRESHOLD, "unreachable" if r10 is None else "{:.3f}".format(r10)))
if r10 is None:
    report("N = 10 negative outcome reachable", False,
           "the table says it is unreachable at N = 10; no example can be built")
else:
    # The expensive losses follow the permutation (0, 9, 4, 3, 6, 7, 2, 5, 8, 1), whose
    # sum d^2 = 160 gives rho = 1 - 160/165 = 0.030303 - just below the 0.034 reach, so
    # this is a near-zero rho that still reaches the negative outcome, not a trivial
    # full reversal. (The full reversal is checked separately below.)
    ex10_cheap = [1189.0 + i for i in range(10)]
    ex10_expensive = [1140.0 + j for j in (0, 9, 4, 3, 6, 7, 2, 5, 8, 1)]
    rho10 = spearman(ex10_cheap, ex10_expensive)
    up10 = fisher_upper(rho10, se_fhp(10))
    tag10, line10 = verdict(10, rho10, up10)
    print("      N = 10: rho_obs = {:.6f}, primary upper = {:.6f}, critical = {:.6f}".format(
        rho10, up10, CRIT_RHO[10]))
    print("      -> {}".format(line10))
    report("N = 10 example reaches the negative outcome",
           tag10 == "No cheap surrogate", "verdict = {}".format(tag10))

    # and the boundary itself: rho_obs just at / just above the reach must flip the verdict
    at_reach = r10
    just_above = r10 + 0.001
    tag_at, _ = verdict(10, at_reach, fisher_upper(at_reach, se_fhp(10)))
    tag_above, _ = verdict(10, just_above, fisher_upper(just_above, se_fhp(10)))
    report("N = 10 boundary: rho_obs = {:.3f} -> No cheap surrogate".format(at_reach),
           tag_at == "No cheap surrogate", "verdict = {}".format(tag_at))
    report("N = 10 boundary: rho_obs = {:.3f} -> inconclusive".format(just_above),
           tag_above == "inconclusive \u2014 underpowered", "verdict = {}".format(tag_above))

    # a full reversal, the extreme case, must also reach the negative outcome
    rev10 = spearman([1189.0 + i for i in range(10)], [1160.0 - i for i in range(10)])
    tag_rev, _ = verdict(10, rev10, fisher_upper(rev10, se_fhp(10)))
    report("N = 10 full reversal (rho = {:.0f}) -> No cheap surrogate".format(rev10),
           tag_rev == "No cheap surrogate", "verdict = {}".format(tag_rev))
print()

# ---------------------------------------------------------------- (6) refusal on unknown N
print("(6) an N outside the section 4 table is refused, not approximated")
try:
    verdict(9, 0.5, 0.5)
    report("verdict(N = 9) refuses", False, "it returned instead of raising")
except ValueError as exc:
    report("verdict(N = 9) refuses", True, "ValueError: {}...".format(str(exc)[:60]))

# ---------------------------------------------------------------- (7) midrank sanity
mr = midranks([5.0, 1.0, 1.0, 3.0])
report("midranks([5,1,1,3]) == [4, 1.5, 1.5, 3]", mr == [4.0, 1.5, 1.5, 3.0],
       "got {}".format(mr))
print()

if FAILURES:
    print("FAILED checks: {}".format(", ".join(FAILURES)))
    sys.exit(1)
print("All checks OK.")
