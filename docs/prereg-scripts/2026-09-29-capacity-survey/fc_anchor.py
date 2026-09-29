"""The number FC stands on (registration rev 1.4, A1): rule #2.1's registered block-only path
(train, then decode) on block B's planted boards, with the lambda grid forced to [100], to [1],
and left as registered. A constructed bank holds only the 40 block cells; present cells carry a
placeholder offset set, which enters no existence term. No fit reads the real bank.
"""
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(newline=chr(10))
C6 = Path(__file__).resolve().parents[3] / "results" / "genome" / "c6"
sys.path.insert(0, str(C6))
import harness as H  # noqa: E402

SOURCES = ("L1", "L2", "L3", "L4", "L5")
ON, OFF = ("Mi1", "Tm3", "Mi4", "Mi9"), ("Tm1", "Tm2", "Tm4", "Tm9")
TARGETS = ON + OFF
Z_PLUS = set(ON) | {"L1", "L3", "L5"}
ZPRIME_PLUS = {"Mi1", "Tm3", "Tm1", "Tm2", "L1", "L2", "L5"}
BLOCK = np.zeros((65, 65), bool)
for s in SOURCES:
    for t in TARGETS:
        BLOCK[H.IDX[s], H.IDX[t]] = True
CELLS = np.array([(H.IDX[s], H.IDX[t]) for s in SOURCES for t in TARGETS], dtype=np.int64)
PLACEHOLDER = {"offsets": {(0, 0): 2.0}, "hull": [], "sign": 1}


def board_bank(plus):
    z = {n: (1 if n in plus else -1) for n in SOURCES + TARGETS}
    content = {(H.IDX[s], H.IDX[t]): dict(PLACEHOLDER)
               for s in SOURCES for t in TARGETS if z[s] * z[t] > 0}
    return H.Bank(f"constructed.{len(content)}", content)


def auc(p, y):
    p, y = np.asarray(p, np.float64), np.asarray(y, bool)
    pos, neg = p[y], p[~y]
    gt = int((pos[:, None] > neg[None, :]).sum())
    eq = int((pos[:, None] == neg[None, :]).sum())
    return (gt + 0.5 * eq) / (len(pos) * len(neg)), gt, eq, len(pos) * len(neg)


def main():
    P = H.load_rule(C6 / "rules" / "second_rule_v21" / "fit.py")
    g = P.fit.__globals__
    registered = list(g["LAMBDAS"])
    for name, plus in (("z", Z_PLUS), ("z'", ZPRIME_PLUS)):
        bank = board_bank(plus)
        y = bank.exists[CELLS[:, 0], CELLS[:, 1]]
        n1 = H.fit_n1(H.make_view(bank, BLOCK))
        o = H._n1_logit_grid(n1)[CELLS[:, 0], CELLS[:, 1]]
        a = auc(o, y)
        print(f"board {name}: present {int(y.sum())} of 40; N1 alone on the block view: AUC {a[0]:.6f} "
              f"({a[1]} wins, {a[2]} ties of {a[3]})")
        for grid in ([100.0], [1.0], registered):
            g["LAMBDAS"] = list(grid)
            try:
                data = P.train(bank, BLOCK)
                lam = float(g["LAST_FIT"]["lambda"])
                dec = P.decode(data, CELLS)
                q = auc(dec["p_exist"], y)
                ex = g["fit_existence"](H.make_view(bank, BLOCK), H.STARTS)
                zf = g["logit_grid"](ex["O"], ex["U"], ex["V"], ex["W"], ex["G"])[CELLS[:, 0], CELLS[:, 1]]
                f = auc(zf, y)
                uv = float(np.max(np.abs(np.outer(ex["U"][:, 0], ex["V"][:, 0])[CELLS[:, 0], CELLS[:, 1]])))
            finally:
                g["LAMBDAS"] = registered
            print(f"  grid {grid}: chosen lambda {lam}; registered path (quantised, decoded) AUC {q[0]:.6f} "
                  f"({q[1]} wins, {q[2]} ties of {q[3]}); float fit before quantisation AUC {f[0]:.6f} "
                  f"({f[1]} wins, {f[2]} ties); max |u.v| on the block {uv:.3e}")
    print("done")


if __name__ == "__main__":
    main()
