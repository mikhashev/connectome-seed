"""The number FC stands on (registration rev 1.4, A1; rev 1.6: the B script's decode path and the tie
rule). Rule #2.1's registered block-only path on block B's planted boards, with the lambda grid forced
to [100], to [1], and (boards z, z' only) left as registered. Every AUC is taken on p, as the B script
takes it: P.train, P.decode(data, cells)["p_exist"] as float64 (knockout_regrow_block_b.py:1254,
1258), auc (:791). N1 likewise goes through its decoder (H.N1.train / H.N1.decode). Each AUC is
printed twice: exact comparison (the registered auc) and with |d| <= TAU = 1e-9 counted as a tie.
A constructed bank holds only the 40 block cells; present cells carry a placeholder offset set,
which enters no existence term. No fit reads the real bank.

FN1 / FN2 boards here are illustrative only: swaps drawn with a design seed (20260929), not the
registered world seeds, and fitted only at the forced grids, never the registered nested grid, so
that nothing previews whether FN's nested choice collapses.
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
TAU = H.TAU


def board_labels(plus):
    z = {n: (1 if n in plus else -1) for n in SOURCES + TARGETS}
    return np.array([z[s] * z[t] > 0 for s in SOURCES for t in TARGETS])


def bank_of(y):
    content = {tuple(CELLS[i].tolist()): dict(PLACEHOLDER) for i in range(40) if y[i]}
    return H.Bank(f"constructed.{int(y.sum())}", content)


def auc2(p, y):
    p, y = np.asarray(p, np.float64), np.asarray(y, bool)
    d = p[y][:, None] - p[~y][None, :]
    n = d.size
    ex = (int((d > 0).sum()) + 0.5 * int((d == 0).sum())) / n
    tau = (int((d > TAU).sum()) + 0.5 * int((np.abs(d) <= TAU).sum())) / n
    return ex, tau, int((d > 0).sum()), int((d == 0).sum()), int((np.abs(d) <= TAU).sum()), n


def fmt(name, p, y):
    ex, tau, w, t0, tt, n = auc2(p, y)
    lv = len(np.unique(np.asarray(p, np.float64)))
    flag = "  ULP_SENSITIVE" if ex != tau else ""
    return (f"{name}: exact {ex:.6f} ({w} wins, {t0} ties of {n}); tau {tau:.6f} ({tt} ties within "
            f"1e-9); distinct p levels {lv}{flag}")


def run(name, y, grids, P, g, registered):
    bank = bank_of(y)
    print(f"board {name}: present {int(y.sum())} of 40")
    n1data = H.N1.train(bank, BLOCK)
    print("  " + fmt("N1 (decoded p)", H.N1.decode(n1data, CELLS)["p_exist"], y))
    for grid in grids:
        g["LAMBDAS"] = list(grid)
        try:
            data = P.train(bank, BLOCK)
            lam = float(g["LAST_FIT"]["lambda"])
            p = np.asarray(P.decode(data, CELLS)["p_exist"], np.float64)
            ex = g["fit_existence"](H.make_view(bank, BLOCK), H.STARTS)
            zf = g["logit_grid"](ex["O"], ex["U"], ex["V"], ex["W"], ex["G"])[CELLS[:, 0], CELLS[:, 1]]
            pf = 1.0 / (1.0 + np.exp(-zf))
            uv = float(np.max(np.abs(np.outer(ex["U"][:, 0], ex["V"][:, 0])[CELLS[:, 0], CELLS[:, 1]])))
        finally:
            g["LAMBDAS"] = registered
        print(f"  grid {grid}: chosen lambda {lam}; max |u.v| on the block {uv:.3e}")
        print("    " + fmt("registered path (quantised, decoded p)", p, y))
        print("    " + fmt("float fit before quantisation (sigmoid of the float logit)", pf, y))


def swapped(y, k, rng):
    y = y.copy()
    pres, absn = np.flatnonzero(y), np.flatnonzero(~y)
    y[rng.choice(pres, k, replace=False)] = False
    y[rng.choice(absn, k, replace=False)] = True
    return y


def main():
    P = H.load_rule(C6 / "rules" / "second_rule_v21" / "fit.py")
    g = P.fit.__globals__
    registered = list(g["LAMBDAS"])
    z, zp = board_labels(Z_PLUS), board_labels(ZPRIME_PLUS)
    run("z", z, ([100.0], [1.0], registered), P, g, registered)
    run("z'", zp, ([100.0], [1.0], registered), P, g, registered)
    rng = np.random.default_rng(20260929)
    for k, fam in ((1, "FN1"), (2, "FN2")):
        for j in range(2):
            y = swapped(z, k, rng)
            run(f"{fam}-illustrative-{j} (z with {k}+{k} swapped, design seed)", y,
                ([100.0], [1.0]), P, g, registered)
    print("done")


if __name__ == "__main__":
    main()
