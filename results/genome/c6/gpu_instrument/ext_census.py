"""Extension X (block mask and fixed lambda; draft, not registered): the tie census of G16 for a
block of any size.

Plan: docs/plans/2026-09-29-gpu-instrument-extension-x-plan.md (draft for review).
census.py (G16, registered by revision 1.4) builds its all-pairs set from a fixed 64-cell block
(census.N_CELLS = 64, census._IU = triu_indices(64, 1)). Block B has 40 block cells, so census.py
cannot count the all-pairs set of a block B base view (its p has 40 entries; the 64-cell index
would fail). This module is the same census with the pair sets built from len(y):
  * "pa": the present x absent pairs by the fit's own y, n_pos * n_neg of them;
  * "all": the n (n - 1) / 2 unordered pairs of the n block cells (2,016 at n = 64, 780 at 40);
  * S(f): census.census_set_of, unchanged ("all" on a base view's ko or ko1 record, "pa" on
    every other record, block-mask records included: the block records enter only
    ceiling_block = auc(p, y), a present x absent read).
Every definition (order state, exact tie, smallest gap, flipped pair, at risk below 2^-23, counts
of tied PAIRS with per-fit denominators) is census.py's. On a 64-cell block every function here
returns what census.py returns (tests_ext/test_x1_census_equivalence.py checks it on A's pinned
store). census.py is not modified and stays the registered census of D1's scope.

Scope labels (the pending item of the backlog entry, revision 1.5 draft): family_summary_scoped
names every count with its scope, so that no census number leaves this module without saying
which fits it counts.
numpy only; no torch, no harness.
"""
import numpy as np

import census as C

BAND = C.BAND


def _pairs(y, which):
    y = np.asarray(y, bool)
    n = len(y)
    if which == "pa":
        pos, neg = np.flatnonzero(y), np.flatnonzero(~y)
        return np.repeat(pos, len(neg)), np.tile(neg, len(pos))
    if which == "all":
        return np.triu_indices(n, 1)
    raise ValueError(which)


def census_set_of(bank_key, mask):
    return C.census_set_of(bank_key, mask)


def pair_census(p, y, which):
    """census.pair_census for a block of len(y) cells."""
    p = np.asarray(p, np.float64)
    y = np.asarray(y, bool)
    if len(p) != len(y):
        raise ValueError(f"p has {len(p)} cells, y has {len(y)}")
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
    """census.census_fit for a block of len(y) cells."""
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
    """census.order_flips for a block of len(y) cells."""
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


def _summ(rows):
    gaps = [(r["gap"], rk) for rk, r in rows if r["gap"] is not None]
    g = min(gaps) if gaps else (None, None)
    return {"fits": len(rows), "fits_with_tie": sum(r["tied"] > 0 for _, r in rows),
            "tied_pairs": sum(r["tied"] for _, r in rows),
            "pairs_denominator_sum": sum(r["n_pairs"] for _, r in rows),
            "smallest_gap": g[0], "smallest_gap_at": g[1],
            "fits_gap_below_band": sum(r["gap"] is not None and r["gap"] < BAND
                                       for _, r in rows)}


def family_summary_scoped(entries, scope):
    """The census per column family, every count carrying its scope label. `scope` names the fits
    counted (for example "block-mask BF fits of B's 45 base views"); the three families are those
    of census.family_summary, with the pair set and the fits each one reads written into its
    name:
      * "auc family, present x absent pairs, every fit in scope";
      * "auc_null family, all pairs, the base-view ko/ko1 fits in scope" (empty on block records);
      * "S(f), every fit in scope".
    Returns {"scope": scope, "n_fits": ..., "families": {name: counts}}."""
    fam = {"auc family, present x absent pairs, every fit in scope": [],
           "auc_null family, all pairs, the base-view ko/ko1 fits in scope": [],
           "S(f), every fit in scope": []}
    for rk, c in entries:
        fam["auc family, present x absent pairs, every fit in scope"].append((rk, c["pa"]))
        if c["S"] == "all":
            fam["auc_null family, all pairs, the base-view ko/ko1 fits in scope"].append(
                (rk, c["all"]))
        fam["S(f), every fit in scope"].append((rk, {"tied": c["tied_S"],
                                                     "n_pairs": c["n_pairs_S"],
                                                     "gap": c["gap_S"]}))
    return {"scope": scope, "n_fits": len(entries),
            "families": {name: _summ(rows) for name, rows in fam.items()}}


def at_risk_list(entries, names=None):
    """census.at_risk_list (E2-III's named list), for a block of any size."""
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
