"""The two gate banks of docs/plans/2026-09-23-second-rule-proposal.md section 2.5: GB1 (signal)
and GB0 (null). Synthetic: existence, signs and the choice of template are drawn here; the
offset sets and counts are copied from real non-empty cells, as the proposal specifies.

Both use the real 65 types and their admissible fields (harness.TYPE_FIELDS) and the harness's
folds by cell position. One numpy Generator(PCG64(60000)), consumed in the registered order:
  1. a_s, b_t ~ N(0, 1) (65 + 65); u_s, v_t ~ N(0, 0.7^2) (65 + 65);
  2. per type, a source template and a target template: two indices, uniform with replacement,
     into the real bank's 604 non-empty cells in sorted (s, t) order [R8];
  3. per type, a target flag pi_t ~ Bernoulli(0.5);
  4. per source type, a sign: +1 with probability 0.62, else -1;
  5. per cell, u1 ~ U(0, 1) for existence, u2 ~ U(0, 1) for noise, and one uniform index into
     the 604 real non-empty cells [R8].
"""

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
C6 = HERE.parents[1]
if str(C6) not in sys.path:
    sys.path.insert(0, str(C6))
import harness as H  # noqa: E402
from fit import groups  # noqa: E402

SEED = 60000
SELFTEST_SEED = 61000
BASE = -2.0
NOISE = 0.2
P_TARGET = 0.5
P_PLUS = 0.62
# rows = source group, columns = target group, order (input, intermediate, output, stride-3)
W_STAR = np.array([[-1.5, +2.0, -1.0, 0.0],
                   [0.0, +1.0, +0.5, 0.0],
                   [-1.0, 0.0, +1.0, 0.0],
                   [0.0, +1.5, 0.0, -1.0]])


def draws(seed=SEED):
    rng = np.random.Generator(np.random.PCG64(seed))
    a = rng.normal(0.0, 1.0, 65)
    b = rng.normal(0.0, 1.0, 65)
    u = rng.normal(0.0, 0.7, 65)
    v = rng.normal(0.0, 0.7, 65)
    tmpl = rng.integers(0, 604, size=(65, 2))           # column 0 source, column 1 target
    pi = rng.random(65) < P_TARGET
    sign = np.where(rng.random(65) < P_PLUS, 1, -1)
    u1 = rng.random((65, 65))
    u2 = rng.random((65, 65))
    pool = rng.integers(0, 604, size=(65, 65))
    return dict(a=a, b=b, u=u, v=v, tmpl=tmpl, pi=pi, sign=sign, u1=u1, u2=u2, pool=pool)


def gate_bank(name):
    """GB1 or GB0; or ST0, the post-run self-test's bank: GB0's construction with seed 61000,
    so that the self-test never touches a gate bank."""
    assert name in ("GB1", "GB0", "ST0")
    d = draws(SELFTEST_SEED if name == "ST0" else SEED)
    real = sorted(H.REAL_CONTENT)
    G = groups(H.TYPE_FIELDS)
    Wst = W_STAR if name == "GB1" else np.zeros((4, 4))
    pi = d["pi"] if name == "GB1" else np.zeros(65, bool)
    logit = BASE + d["a"][:, None] + d["b"][None, :] + np.outer(d["u"], d["v"]) + \
        Wst[np.ix_(G, G)]
    p = 1.0 / (1.0 + np.exp(-logit))
    content = {}
    for s in range(65):
        for t in range(65):
            if not d["u1"][s, t] < p[s, t]:
                continue
            if d["u2"][s, t] < NOISE:
                src = real[d["pool"][s, t]]
            else:
                src = real[d["tmpl"][t, 1]] if pi[t] else real[d["tmpl"][s, 0]]
            content[(s, t)] = {"offsets": dict(H.REAL_CONTENT[src]["offsets"]), "hull": [],
                               "sign": int(d["sign"][s])}
    return H.Bank(name, content)


if __name__ == "__main__":
    for nm in ("GB1", "GB0"):
        b = gate_bank(nm)
        print(nm, "non-empty cells", len(b.content), "rate", round(len(b.content) / 4225, 4))
