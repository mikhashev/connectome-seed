"""M8 (registration rev 1.8, section 4 / 4a): a design computation on block B's real row profile.

50 boards of 5 x 8 with rows 2, 6, 4, 4, 3 present (19 of 40), reproduced exactly as bf4_check.py
draws them (default_rng(20260929), same calls, same order). Per board: cert (free-class search from
survey.py, stored member recounted with Fraction, also counted with |d| <= TAU as ties); N1 through
its decoder; rule #2.1's registered block-only path at forced lambda = 100 (quantised, decoded p)
and its float fit (sigmoid of the float logit); the registered path at lambda = 1 (ceil_1) and its
float fit. Every AUC exact and under TAU. Constructed banks only (the 40 block cells, placeholder
offsets); no fit reads the real bank. Design seeds: boards 20260929; search 2026092901 (stage 1),
2026092902-2026092906 (reruns).
"""
import csv
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fc_anchor as FA  # noqa: E402  (harness, constructed banks, auc2)
import survey as SV  # noqa: E402  (best_auc, frac_count)

sys.stdout.reconfigure(newline=chr(10))
H = FA.H
S, T = 5, 8
PROFILE = [2, 6, 4, 4, 3]
N_BOARDS = 50
SEED_BOARDS = 20260929
SEED_STAGE1 = 2026092901
SEED_RERUNS = [2026092902 + r for r in range(5)]


def boards():
    rng = np.random.default_rng(SEED_BOARDS)
    out = []
    for _ in range(N_BOARDS):
        rows = [sorted(rng.choice(T, k, replace=False).tolist()) for k in PROFILE]
        Y = np.zeros((S, T), int)
        for s, r in enumerate(rows):
            Y[s, r] = 1
        out.append(Y)
    return out


def auc_member(Y, m):
    a, b, u, v = [np.asarray(x, np.float64) for x in m]
    z = (a[:, None] + b[None, :] + u[:, None] * v[None, :]).ravel()
    return FA.auc2(z, Y.ravel().astype(bool))


def fits(y, P, g, registered):
    bank = FA.bank_of(y)
    res = {}
    n1 = H.N1.train(bank, FA.BLOCK)
    res["N1"] = FA.auc2(H.N1.decode(n1, FA.CELLS)["p_exist"], y)
    for lam in (100.0, 1.0):
        g["LAMBDAS"] = [lam]
        try:
            data = P.train(bank, FA.BLOCK)
            assert float(g["LAST_FIT"]["lambda"]) == lam
            p = np.asarray(P.decode(data, FA.CELLS)["p_exist"], np.float64)
            ex = g["fit_existence"](H.make_view(bank, FA.BLOCK), H.STARTS)
            zf = g["logit_grid"](ex["O"], ex["U"], ex["V"], ex["W"], ex["G"])[FA.CELLS[:, 0], FA.CELLS[:, 1]]
            pf = 1.0 / (1.0 + np.exp(-zf))
        finally:
            g["LAMBDAS"] = registered
        tag = "100" if lam == 100.0 else "1"
        res[f"q{tag}"] = FA.auc2(p, y)
        res[f"f{tag}"] = FA.auc2(pf, y)
    return res


def main():
    t0 = time.time()
    B = boards()
    # cert: stage 1, then 5 reruns on every board; best member kept; Fraction recount
    best, n, mem = SV.best_auc(B, S, T, K=100, steps=500, seed=SEED_STAGE1)
    spread = {i: [] for i in range(N_BOARDS)}
    for sd in SEED_RERUNS:
        c, _, m = SV.best_auc(B, S, T, K=500, steps=500, seed=sd)
        for i in range(N_BOARDS):
            spread[i].append(float(c[i]))
            if c[i] > best[i]:
                best[i], mem[i] = c[i], m[i]
    t_cert = time.time() - t0
    P = H.load_rule(FA.C6 / "rules" / "second_rule_v21" / "fit.py")
    g = P.fit.__globals__
    registered = list(g["LAMBDAS"])
    rows_out, members = [], {}
    for i, Y in enumerate(B):
        frac = SV.frac_count(Y, *mem[i])
        assert frac == best[i], (i, frac, best[i])
        ca = auc_member(Y, mem[i])
        y = Y.ravel().astype(bool)
        r = fits(y, P, g, registered)
        row = {"board": i, "rows_present_cols": json.dumps([np.flatnonzero(Y[s]).tolist() for s in range(S)],
                                                             separators=(",", ":")),
               "cert_exact": frac / n, "cert_count": frac, "cert_tau": ca[1],
               "cert_rerun_min": min(spread[i]), "cert_rerun_max": max(spread[i])}
        for k in ("N1", "q100", "f100", "q1", "f1"):
            row[f"{k}_exact"], row[f"{k}_tau"] = r[k][0], r[k][1]
        rows_out.append(row)
        members[str(i)] = {"rows": json.loads(row["rows_present_cols"]), "count": frac, "n_pairs": int(n),
                           "a": mem[i][0].tolist(), "b": mem[i][1].tolist(), "u": mem[i][2].tolist(),
                           "v": mem[i][3].tolist()}
        flags = [k for k in ("N1", "q100", "f100", "q1", "f1") if r[k][0] != r[k][1]]
        if ca[0] != ca[1]:
            flags.append("cert")
        print(f"board {i:2d}: cert {frac:.1f}/{n} = {frac / n:.4f} (tau {ca[1]:.4f}; reruns "
              f"{min(spread[i]):.0f}-{max(spread[i]):.0f}); N1 {r['N1'][0]:.4f}/{r['N1'][1]:.4f}; "
              f"lambda=100 quantised {r['q100'][0]:.4f}/{r['q100'][1]:.4f}, float {r['f100'][0]:.4f}/"
              f"{r['f100'][1]:.4f}; ceil_1 {r['q1'][0]:.4f}/{r['q1'][1]:.4f}, float {r['f1'][0]:.4f}/"
              f"{r['f1'][1]:.4f}  (exact/tau){'  ULP_SENSITIVE: ' + ','.join(flags) if flags else ''}")
    t_all = time.time() - t0
    with open(HERE / "m8_profile_boards.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows_out)
    with open(HERE / "m8_profile_members.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(members, f, indent=1)

    def dist(key):
        x = np.array([r[key] for r in rows_out])
        return (f"min {x.min():.4f}, p25 {np.percentile(x, 25):.4f}, median {np.median(x):.4f}, "
                f"p75 {np.percentile(x, 75):.4f}, max {x.max():.4f}")
    q100 = np.array([r["q100_exact"] for r in rows_out])
    q100t = np.array([r["q100_tau"] for r in rows_out])
    certs = np.array([r["cert_exact"] for r in rows_out])
    print(f"\nboards {N_BOARDS}; pairs per board {n}; cert search {t_cert:.0f}s; total {t_all:.0f}s")
    for key in ("cert_exact", "cert_tau", "N1_exact", "N1_tau", "q100_exact", "q100_tau", "f100_exact",
                "f100_tau", "q1_exact", "q1_tau", "f1_exact", "f1_tau"):
        print(f"  {key}: {dist(key)}")
    print(f"fit-side prediction (Ark): median of lambda=100 quantised in [0.60, 0.80] -> median "
          f"{np.median(q100):.4f}: {'HOLDS' if 0.60 <= np.median(q100) <= 0.80 else 'FAILS'}; no board >= 0.90 "
          f"-> {int((q100 >= 0.90).sum())} boards exact, {int((q100t >= 0.90).sum())} under tau: "
          f"{'HOLDS' if (q100 >= 0.90).sum() == 0 and (q100t >= 0.90).sum() == 0 else 'FAILS'}")
    if (q100 >= 0.90).any() or (q100t >= 0.90).any():
        print("  boards >= 0.90:", [int(i) for i in np.flatnonzero((q100 >= 0.90) | (q100t >= 0.90))])
    print(f"class-side prediction (Zcode): every cert >= 0.90 -> min {certs.min():.4f}, "
          f"{int((certs < 0.90).sum())} below: {'HOLDS' if (certs >= 0.90).all() else 'FAILS'}")
    q1 = np.array([r["q1_exact"] for r in rows_out])
    print(f"ceil_1 (registered path at lambda = 1): {int((q1 < 0.90).sum())} of {N_BOARDS} below 0.90")
    print("done")


if __name__ == "__main__":
    main()
