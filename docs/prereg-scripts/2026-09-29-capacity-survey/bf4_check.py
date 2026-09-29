"""Explicit BF_4 members reaching AUC 1 on 5 x 8 boards (bf4_capacity.md). Exact rational arithmetic.

For each board: pick w in {-1,+1}^5 with sign(w) and -sign(w) outside the board's column patterns;
U = [w5 e_i - w_i e5], i = 1..4 (a basis of w-perp); for each column pattern p, x = p * alpha in
w-perp with alpha > 0; v = x[:4] / w5, so U v = x. The member's logit is O + K * U V^T with O any
additive offset c + a_s + b_t and K > range(O) / (2 delta), delta = min |x|. Checked with O = 0 and
with a random additive offset of range up to 20 (the bound applies to any O).
"""
import csv
import itertools
import json
import sys
from fractions import Fraction

import numpy as np

sys.stdout.reconfigure(newline=chr(10))
S, T = 5, 8


def column_patterns(Y):
    return {tuple(1 if Y[s][t] else -1 for s in range(S)) for t in range(T)}


def choose_w(Y):
    pats = column_patterns(Y)
    for w in itertools.product((1, -1), repeat=S):
        neg = tuple(-x for x in w)
        if w not in pats and neg not in pats:
            return w
    return None


def member(Y):
    w = choose_w(Y)
    U = [[Fraction(0)] * 4 for _ in range(S)]
    for i in range(4):
        U[i][i] = Fraction(w[4])
        U[4][i] = Fraction(-w[i])
    V = []
    X = [[None] * T for _ in range(S)]
    for t in range(T):
        p = [1 if Y[s][t] else -1 for s in range(S)]
        pos = [s for s in range(S) if w[s] * p[s] > 0]
        neg = [s for s in range(S) if w[s] * p[s] < 0]
        assert pos and neg
        alpha = [Fraction(1, len(pos)) if s in pos else Fraction(1, len(neg)) for s in range(S)]
        x = [p[s] * alpha[s] for s in range(S)]
        assert sum(Fraction(w[s]) * x[s] for s in range(S)) == 0
        v = [x[i] / w[4] for i in range(4)]
        V.append(v)
        for s in range(S):
            X[s][t] = sum(U[s][k] * v[k] for k in range(4))
            assert X[s][t] == x[s]
    return w, U, V, X


def exact_auc(Y, Z):
    P = [Z[s][t] for s in range(S) for t in range(T) if Y[s][t]]
    N = [Z[s][t] for s in range(S) for t in range(T) if not Y[s][t]]
    w = sum(2 if p > q else (1 if p == q else 0) for p in P for q in N)
    return Fraction(w, 2 * len(P) * len(N)), len(P) * len(N)


def check(Y, rng):
    w, U, V, X = member(Y)
    delta = min(abs(X[s][t]) for s in range(S) for t in range(T))
    rank = int(np.linalg.matrix_rank(np.array([[float(X[s][t]) for t in range(T)] for s in range(S)])))
    out = []
    a = [Fraction(int(x)) for x in rng.integers(-10, 11, S)]
    b = [Fraction(int(x)) for x in rng.integers(-10, 11, T)]
    for name, O in (("O=0", [[Fraction(0)] * T for _ in range(S)]),
                    ("O=random additive", [[a[s] + b[t] for t in range(T)] for s in range(S)])):
        rngO = max(max(r) for r in O) - min(min(r) for r in O)
        K = rngO / (2 * delta) + 1
        Z = [[O[s][t] + K * X[s][t] for t in range(T)] for s in range(S)]
        auc, npairs = exact_auc(Y, Z)
        out.append((name, auc, npairs, K))
    return w, delta, rank, out


def board_from_rows(rows):
    Y = [[0] * T for _ in range(S)]
    for s, r in enumerate(rows):
        for t in r:
            Y[s][t] = 1
    return Y


def main():
    rng = np.random.default_rng(20260929)
    sets = []
    with open("survey_boards.csv") as f:
        for r in csv.DictReader(f):
            if r["shape"] == "5x8":
                sets.append(("survey 5x8 #" + r["board_id"], board_from_rows(json.loads(r["rows_present_cols"]))))
    prof = [2, 6, 4, 4, 3]
    for j in range(50):
        sets.append((f"profile 2,6,4,4,3 #{j}",
                     board_from_rows([sorted(rng.choice(T, k, replace=False).tolist()) for k in prof])))
    for j in range(200):
        while True:
            ks = rng.integers(0, T + 1, S)
            if 0 < ks.sum() < S * T:
                break
        sets.append((f"random unequal rows {ks.tolist()} #{j}",
                     board_from_rows([sorted(rng.choice(T, int(k), replace=False).tolist()) for k in ks])))
    sets.append(("edge: one full row, others empty", board_from_rows([list(range(T)), [], [], [], []])))
    sets.append(("edge: one full column", board_from_rows([[0]] * S)))
    sets.append(("edge: all 8 columns distinct, alternating", board_from_rows([[0, 2, 4, 6], [0, 1, 4, 5], [0, 1, 2, 3], [1, 3, 5, 7], [0, 7]])))
    fails = []
    ranks = {}
    min_delta = None
    for name, Y in sets:
        w, delta, rank, out = check(Y, rng)
        ranks[rank] = ranks.get(rank, 0) + 1
        min_delta = delta if min_delta is None else min(min_delta, delta)
        for oname, auc, npairs, K in out:
            if auc != 1:
                fails.append((name, oname, str(auc)))
    n_survey = sum(1 for n, _ in sets if n.startswith("survey"))
    print(f"boards checked: {len(sets)} (survey 5x8: {n_survey}; profile 2,6,4,4,3: 50; random unequal rows: 200; edge: 3)")
    print(f"each board: two offsets (O = 0; a random additive O with integer a in [-10,10], b in [-10,10]); exact Fraction count")
    print(f"rank of the constructed K*U V^T term on the 5 x 8 block: {dict(sorted(ranks.items()))} (all <= 4)")
    print(f"smallest margin delta over all boards: {min_delta}")
    print(f"boards x offsets with AUC != 1: {len(fails)}")
    for f in fails[:20]:
        print("  FAIL", f)
    print("done")


if __name__ == "__main__":
    main()
