"""G16: the tie census, one function used by the comparator (G9) and by every GPU run.

docs/plans/2026-09-26-gpu-instrument-registration.md, revision 1.3, section 5 (E2), with Ark's
review of revision 1.3 (chat 12:09 UTC), point 2: the census denominator is per fit.

Definitions (section 5):
  * pair sets of a fit, from its labels y (64 booleans in block cell order, read from the
    reference record where one exists):
      - "pa": the present x absent pairs by the fit's own y, n_pos * n_neg of them (the auc
        column family: auc, M_real, n_ge, p_S, auc_other_59, precision_at_32, auc_fixed_lambda1);
      - "all": the 2,016 unordered pairs of the 64 cells (the auc_null family: p_P, p_P_rowcol,
        p_P_fixed_lambda1), read only on a base view's ko (and ko1) fit;
      - S(f), the census pair set: pa on a shuffle (and on every record other than a base view's
        ko/ko1), all on a base view's ko/ko1, with pa printed as its own sub-count.
  * order state of a pair (i, j): sign(p_i - p_j), compared exactly on the decoded float64 p.
  * exact tie: a pair of the set with p_i == p_j; smallest gap: min |p_i - p_j| over the pairs of
    the set with p_i != p_j ("none" if p is constant on the set).
  * flipped pair (between a fit and its reference): order states differ, 0 against +-1 or +1
    against -1; counted over pairs, never cancelled.
  * at risk (E2-III): smallest gap on S(f) below 2^-23 (a named list, not a gate).
  * every count is a count of tied PAIRS on a named pair set, never of tie groups; the
    denominator of each count is the fit's own number of pairs in that set (n_pos * n_neg, or
    2,016), never a constant 1,024 (Ark, 12:09 UTC, point 2).
numpy only; no torch, no harness.
"""
import numpy as np

BAND = 2.0 ** -23                     # E2-III, revision 1.3: 2 * 2^-24
N_CELLS = 64
_IU = np.triu_indices(N_CELLS, 1)     # the 2,016 unordered pairs, i < j


def census_set_of(bank_key, mask):
    """S(f): 'all' on a base view's ko or ko1 record, 'pa' on every other record."""
    return "all" if ("|" not in bank_key and mask in ("ko", "ko1")) else "pa"


def _pairs(y, which):
    y = np.asarray(y, bool)
    if which == "pa":
        pos, neg = np.flatnonzero(y), np.flatnonzero(~y)
        i = np.repeat(pos, len(neg))
        j = np.tile(neg, len(pos))
        return i, j
    if which == "all":
        return _IU
    raise ValueError(which)


def pair_census(p, y, which):
    """Tied pairs, smallest gap and its pair, and pairs below the band, on one pair set."""
    p = np.asarray(p, np.float64)
    y = np.asarray(y, bool)
    i, j = _pairs(y, which)
    n = int(len(i))
    out = {"set": which, "n_pairs": n, "tied": 0, "gap": None, "pair": None,
           "n_below_band": 0, "n_below_1e5": 0}
    if n == 0:
        return out
    d = p[i] - p[j]
    tied = d == 0
    out["tied"] = int(tied.sum())
    ad = np.abs(d)
    nz = ~tied
    if nz.any():
        k = int(np.flatnonzero(nz)[np.argmin(ad[nz])])
        out["gap"] = float(ad[k])
        a, b = int(i[k]), int(j[k])
        out["pair"] = {"cells": [a, b], "labels": [bool(y[a]), bool(y[b])],
                       "p": [float(p[a]), float(p[b])]}
        out["n_below_band"] = int((ad[nz] < BAND).sum())
        out["n_below_1e5"] = int((ad[nz] < 1e-5).sum())
    return out


def census_fit(p, y, bank_key, mask, p_n1=None, all_pairs=False):
    """The census of one fit: S(f) (with its pa sub-count on a base view), the at-risk flag, and
    whether p equals its view's N1 p (the BF-active classification, Ark point 1; None when no N1
    p is given). all_pairs=True also computes the all-pairs census on a record whose S(f) is pa
    (for the store-wide counts of M20)."""
    y = np.asarray(y, bool)
    s = census_set_of(bank_key, mask)
    pa = pair_census(p, y, "pa")
    al = pair_census(p, y, "all") if (s == "all" or all_pairs) else None
    S = al if s == "all" else pa
    return {"S": s, "n_pos": int(y.sum()), "n_neg": int((~y).sum()),
            "pa": pa, "all": al,
            "tied_S": S["tied"], "n_pairs_S": S["n_pairs"], "gap_S": S["gap"], "pair_S": S["pair"],
            "at_risk": S["gap"] is not None and S["gap"] < BAND,
            "p_equals_n1": (None if p_n1 is None else
                            bool(np.array_equal(np.asarray(p, np.float64),
                                                np.asarray(p_n1, np.float64))))}


def order_flips(p_got, p_ref, y, bank_key, mask):
    """E2-II: the flipped pairs of S(f) between a fit (p_got) and its reference (p_ref); y is the
    reference's labels. Each entry names the two block cells, both sides' p and order states."""
    p_got = np.asarray(p_got, np.float64)
    p_ref = np.asarray(p_ref, np.float64)
    y = np.asarray(y, bool)
    i, j = _pairs(y, census_set_of(bank_key, mask))
    s_ref = np.sign(p_ref[i] - p_ref[j])
    s_got = np.sign(p_got[i] - p_got[j])
    k = np.flatnonzero(s_ref != s_got)
    return [{"cells": [int(i[t]), int(j[t])], "labels": [bool(y[i[t]]), bool(y[j[t]])],
             "p_ref": [float(p_ref[i[t]]), float(p_ref[j[t]])],
             "p_got": [float(p_got[i[t]]), float(p_got[j[t]])],
             "state_ref": int(s_ref[t]), "state_got": int(s_got[t])} for t in k]


def family_summary(entries):
    """The census per column family over a list of (record key, census_fit) entries (section 5's
    table): the auc family on the pa pairs of every fit; the auc_null family on all pairs of the
    base-view ko/ko1 fits; S(f). Each with fits, fits with a tie, tied pairs, the sum of the
    per-fit denominators (pairs), smallest gap and where, and fits at risk on that set."""
    fam = {"auc (pa pairs, every fit)": [], "auc_null (all pairs, base ko/ko1)": [],
           "S(f)": []}
    for rk, c in entries:
        fam["auc (pa pairs, every fit)"].append((rk, c["pa"]))
        if c["S"] == "all":
            fam["auc_null (all pairs, base ko/ko1)"].append((rk, c["all"]))
        fam["S(f)"].append((rk, {"tied": c["tied_S"], "n_pairs": c["n_pairs_S"],
                                 "gap": c["gap_S"], "n_below_band": None}))
    out = {}
    for name, rows in fam.items():
        gaps = [(r["gap"], rk) for rk, r in rows if r["gap"] is not None]
        g = min(gaps) if gaps else (None, None)
        out[name] = {"fits": len(rows), "fits_with_tie": sum(r["tied"] > 0 for _, r in rows),
                     "tied_pairs": sum(r["tied"] for _, r in rows),
                     "pairs_denominator_sum": sum(r["n_pairs"] for _, r in rows),
                     "smallest_gap": g[0], "smallest_gap_at": g[1],
                     "fits_gap_below_band": sum(r["gap"] is not None and r["gap"] < BAND
                                                for _, r in rows)}
    return out


def at_risk_list(entries, names=None):
    """E2-III's named list: every fit whose smallest gap on S(f) is below 2^-23, with the gap,
    the pair (block cells, labels, p) and whether its p equals its view's N1 p."""
    out = []
    for rk, c in entries:
        if c["at_risk"]:
            pr = c["pair_S"]
            e = {"key": rk, "gap": c["gap_S"], "set": c["S"], "cells": pr["cells"],
                 "labels": pr["labels"], "p": pr["p"], "p_equals_n1": c["p_equals_n1"]}
            if names is not None:
                e["cell_names"] = [names[pr["cells"][0]], names[pr["cells"][1]]]
            out.append(e)
    return out
