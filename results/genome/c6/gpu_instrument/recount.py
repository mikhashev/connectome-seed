"""V6's independent brute-force recount (registration revision 1.3, section 7, V6 and 7.1).

Pure Python over the saved p, lam and y of both sides, fit by fit, sharing no code with the
comparator (gpu_equivalence.py) or the census (census.py): no numpy, no knockout_regrow. For each
fit it counts what the comparator reports (gpu_equivalence.compact): y equal, lambda equal, label
differences, AUC equal, bit-equal, max |dp|, flipped pairs on S(f), at risk (smallest gap on S(f)
below 2^-23 on either side). V6 passes only if the two agree on every fit.
"""
BAND = 2.0 ** -23


def _auc(p, y):
    pos = [a for a, t in zip(p, y) if t]
    neg = [a for a, t in zip(p, y) if not t]
    if not pos or not neg:
        return None
    gt = eq = 0
    for a in pos:
        for b in neg:
            if a > b:
                gt += 1
            elif a == b:
                eq += 1
    return (gt + 0.5 * eq) / (len(pos) * len(neg))


def _pairs(bank, mask, y):
    n = len(y)
    if "|" not in bank and mask in ("ko", "ko1"):
        return [(i, j) for i in range(n) for j in range(i + 1, n)]
    return [(i, j) for i in range(n) if y[i] for j in range(n) if not y[j]]


def _sign(x):
    return (x > 0) - (x < 0)


def _min_gap(p, pairs):
    g = None
    for i, j in pairs:
        d = abs(p[i] - p[j])
        if d != 0 and (g is None or d < g):
            g = d
    return g


def recount_fit(rk, got, ref):
    bank, mask, _ = rk.split("||")
    y = [bool(v) for v in ref["y"]]
    yg = [bool(v) for v in got["y"]]
    pr = [float(v) for v in ref["p"]]
    pg = [float(v) for v in got["p"]]
    pairs = _pairs(bank, mask, y)
    flips = sum(1 for i, j in pairs if _sign(pr[i] - pr[j]) != _sign(pg[i] - pg[j]))
    gr, gg = _min_gap(pr, pairs), _min_gap(pg, pairs)
    return {"key": rk, "y_equal": y == yg, "lam_equal": float(got["lam"]) == float(ref["lam"]),
            "label_diffs": sum(1 for a, b in zip(pg, pr) if (a >= 0.5) != (b >= 0.5)),
            "auc_equal": _auc(pg, y) == _auc(pr, y), "bit_equal": pg == pr,
            "max_abs_dp": max(abs(a - b) for a, b in zip(pg, pr)),
            "n_flips": flips,
            "at_risk": (gr is not None and gr < BAND) or (gg is not None and gg < BAND)}


def agree(comparator_rows, got, ref):
    """Every comparator row against the recount of the same fit. Returns (agree, mismatches)."""
    mism = []
    for row in comparator_rows:
        rc = recount_fit(row["key"], got[row["key"]], ref[row["key"]])
        diff = {k: (row[k], rc[k]) for k in rc if k != "key" and row[k] != rc[k]}
        if diff:
            mism.append({"key": row["key"], "comparator_vs_recount": diff})
    return not mism, mism
