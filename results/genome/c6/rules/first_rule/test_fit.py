"""Unit tests of the first rule's learner and decoder, on SYNTHETIC data only.

No real bank, no real fold and no shuffled bank is fitted or scored here. The harness is imported
only for its interface (Bank, make_view, Predictor, data_bits, score), which it applies to the
synthetic bank built below.

Run (from the repository root):
    tools/.venv/Scripts/python.exe results/genome/c6/rules/first_rule/test_fit.py
"""

import ast
import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "results" / "genome" / "c6"))

import fit as FR  # noqa: E402

DECODER_CAP_BYTES = 560                     # proposal section 2.2


# ---- a planted instance whose labels and rules are known ---------------------------------
def planted(seed=2, prev=0.3, eps_q=10):
    """Three true labels (Bernoulli(prev) per type), three true rules in a cycle 0->1->2->0,
    each with its own motif, orientation and strength, and a leak at level eps_q. Signs per
    source type. seed 2 is an instance where the registered search is known to reach the planted
    code length (other seeds can stop at sweep 1 with no rule: see README)."""
    rng = np.random.default_rng(seed)
    E = rng.random((65, 3)) < prev
    rules = [(0, 1, 15, 0, 0), (1, 2, 15, 1, 3), (2, 0, 14, 2, 6)]  # i, j, rho q, motif, g
    motifs = [[(0, 0)], [(0, 0), (1, 0)], [(0, 0), (1, 0), (0, 1), (-1, 1)]]
    w = [3.0, 2.0, 1.2]
    eps = FR.EPS[eps_q]
    r2 = np.random.default_rng(seed + 1000)
    a, b = r2.normal(0, 0.3, 65), r2.normal(0, 0.3, 65)
    sign = np.where(r2.random(65) < 0.6, 1, -1)
    content = {}
    for s in range(65):
        for t in range(65):
            F = [r for r in range(3) if E[s, rules[r][0]] and E[t, rules[r][1]]]
            p = 1 - (1 - eps) * np.prod([1 - FR.RHO[rules[r][2]] for r in F])
            if rng.random() >= p:
                continue
            if F:
                r = max(F, key=lambda r: (rules[r][2], -r))
                offs = FR.image(motifs[rules[r][3]], rules[r][4])
                tot = math.exp(w[r] + a[s] + b[t])
            else:
                offs, tot = [(0, 0)], math.exp(1.0 + a[s] + b[t])
            pi = np.exp(0.35 * np.arange(len(offs)))
            pi /= pi.sum()
            content[(s, t)] = {"offsets": {o: float(tot * x) for o, x in zip(offs, pi)},
                               "hull": [], "sign": int(sign[s])}
    return E, rules, eps_q, content


def split_mask(seed=3):
    rng = np.random.default_rng(seed)
    return rng.random((65, 65)) >= 0.1          # ~90 % training cells


def true_J(E_true, rules, view, eps_q):
    """J of the planted genome itself (its labels padded with unused labels) on the view."""
    M, Y = FR.grid(view)
    P = np.zeros((E_true.shape[1],) * 2, bool)
    Q = np.zeros_like(P, dtype=np.int64)
    for i, j, q, *_ in rules:
        P[i, j], Q[i, j] = True, q
    Ef = E_true.astype(float)
    S = Ef @ FR.rule_matrix(P, Q) @ Ef.T
    return FR.total_J(S, eps_q, M, Y, len(rules))


# ---- tests ------------------------------------------------------------------------------
def test_decoder_size():
    import harness as H
    b = H.program_bits(FR.PROGRAM_FILES)
    H.check_imports(FR.PROGRAM_FILES)
    assert b <= 8 * DECODER_CAP_BYTES, b
    return {"decoder_lzma_bytes": b // 8, "decoder_bits": b}


def test_d6_matches_regularity():
    src = (ROOT / "results" / "genome" / "bank" / "regularity.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in ("rot", "refl", "d6_images",
                                                              "canon_pattern"):
            exec(compile(ast.Module([node], []), "regularity.py", "exec"), ns)
    rng = np.random.default_rng(0)
    for _ in range(200):
        pts = [tuple(int(x) for x in rng.integers(-3, 4, 2)) for _ in range(rng.integers(1, 6))]
        pts = sorted(set(pts))
        imgs = ns["d6_images"]([(p, 1) for p in pts])
        for g in range(12):
            assert sorted(FR.image(pts, g)) == sorted(uv for uv, _ in imgs[g])
        assert FR.canon(pts) == ns["canon_pattern"]([(p, 1) for p in pts], False, True)


def test_planted_recovery(starts=10, search="v1"):
    import harness as H
    E_true, rules, eps_q, content = planted()
    bank = H.Bank("synthetic", content)
    train = split_mask()
    view = H.make_view(bank, train)
    t0 = time.time()
    data = FR.fit(view, starts=starts, search=search)
    dt = time.time() - t0
    info = dict(FR.LAST_FIT)
    M, Y = FR.grid(view)
    J_fit = min(info["J_per_start"])
    J_true = true_J(np.pad(E_true, ((0, 0), (0, 9))), rules, view, eps_q)
    J_empty = FR.total_J(np.zeros((65, 65)), FR.eps_level_nearest(M, Y), M, Y, 0)
    P = H.Predictor("first_rule(synthetic)", FR.PROGRAM_FILES, lambda v: data)
    # the fit must reach (about) the planted genome's own code length, far below no rules
    assert J_fit <= J_true + 1e-6, (J_fit, J_true)
    assert J_fit < 0.5 * J_empty, (J_fit, J_empty)
    # v1: the recovered labels used by rules are the planted ones (up to relabelling). v2 is held
    # to the code length and to held-out N1 only: on this instance it reaches a J at or below
    # the planted one with a different label decomposition (reported, not asserted away).
    info["rule_label_sets"] = sorted(sorted(np.flatnonzero(data["E"][:, l]).tolist())
                                     for l in sorted({int(x) for x in
                                                      data["R__sym16"][:, :2].ravel()}))
    if search == "v1":
        _check_labels(data, E_true)
    return _report(search, dt, starts, J_fit, J_true, J_empty, info, P, data, bank, held=None,
                   train=train, view=view)


def _check_labels(data, E_true):
    E_fit = data["E"]
    used = sorted({int(x) for x in data["R__sym16"][:, :2].ravel()})
    got = sorted(tuple(E_fit[:, l].tolist()) for l in used)
    assert got == sorted(tuple(E_true[:, l].tolist()) for l in range(3)), "labels not recovered"
    assert len(data["R__sym16"]) == 3


def _report(search, dt, starts, J_fit, J_true, J_empty, info, P, data, bank, held, train, view):
    import harness as H
    # held-out: decode through the harness's own machinery and score on the synthetic bank
    held = H.ALL_CELLS[~train[H.ALL_CELLS[:, 0], H.ALL_CELLS[:, 1]]]
    s_rule = H.score(P.decode(data, held), bank, held)
    n1 = H.fit_n1(view)
    s_n1 = H.score(H.N1.decode(n1, held), bank, held)
    assert s_rule["existence"] < s_n1["existence"], (s_rule, s_n1)
    assert s_rule["offset"] > s_n1["offset"], (s_rule, s_n1)
    dl = P.dl(data)
    return {"search": search, "fit_seconds": round(dt, 2), "starts": starts,
            "J_fit": round(J_fit, 2),
            "J_planted": round(J_true, 2), "J_no_rules": round(J_empty, 2),
            "n_rules": info["n_rules"], "n_motifs": info["n_motifs"],
            "rule_label_sets": info["rule_label_sets"],
            "heldout_synthetic": {"rule": {k: s_rule[k] for k in ("existence", "offset",
                                                                   "counts", "sign")},
                                  "N1": {k: s_n1[k] for k in ("existence", "offset",
                                                             "counts", "sign")}},
            "DL_bits_synthetic": dl, "data_bits_synthetic": dl - P.prog_bits}


def test_planted_recovery_v2():
    return test_planted_recovery(search="v2")


def test_v1_unchanged():
    """SEARCH v1 is byte-identical to the procedure committed in 05c1a8d (hash of its data on
    this instance, computed with that commit's fit.py)."""
    import harness as H
    import timing
    _, _, _, content = planted()
    view = H.make_view(H.Bank("synthetic", content), split_mask())
    assert timing.data_hash(FR.fit(view, starts=10, search="v1")) == "27e347eff741efbf"


def test_determinism(starts=2):
    import harness as H
    _, _, _, content = planted(seed=2)
    view = H.make_view(H.Bank("synthetic2", content), split_mask(5))
    for search in ("v1", "v2"):
        a = FR.fit(view, starts=starts, search=search)
        ja = list(FR.LAST_FIT["J_per_start"])
        b = FR.fit(view, starts=starts, search=search)
        jb = list(FR.LAST_FIT["J_per_start"])
        assert a.keys() == b.keys()
        for k in a:
            assert a[k].dtype == b[k].dtype and np.array_equal(a[k], b[k]), (search, k)
        assert ja == jb
    # a different seed set gives a different first restart
    E0, E1 = FR.initial_labels(0), FR.initial_labels(1)
    assert not np.array_equal(E0, E1)
    assert np.array_equal(FR.initial_labels(0), E0)


def test_data_types():
    """Every array is int, bool or symbol-coded: no 32-bit reals (proposal section 2.1)."""
    import harness as H
    _, _, _, content = planted(seed=5)
    view = H.make_view(H.Bank("synthetic3", content), split_mask(9))
    d = FR.fit(view, starts=1)
    assert all(np.asarray(v).dtype.kind in "biu" for v in d.values())
    assert d["E"].shape == (65, 12) and d["R__sym16"].shape[1] == 5
    assert len(d["R__sym16"]) <= FR.R_MAX and len(d["L"]) <= FR.M_MAX
    assert d["O"].shape[0] <= FR.O_MAX
    R = d["R__sym16"]
    assert [tuple(x) for x in R[:, :2].tolist()] == sorted(tuple(x) for x in R[:, :2].tolist())
    # random-label arm: expression is the frozen seed-20260923 draw
    dr = FR.fit(view, labels="random", search="v2")
    assert np.array_equal(dr["E"], np.random.default_rng(20260923).random((65, 12)) < 0.25)


def test_spread_log(tmp=None):
    """FIRST_RULE_SPREAD_LOG set: one JSON line per fit call; unset: data unchanged, no file."""
    import json
    import os
    import tempfile
    import harness as H
    import timing
    _, _, _, content = planted()
    view = H.make_view(H.Bank("synthetic", content), split_mask())
    os.environ.pop(FR.SPREAD_ENV, None)
    h0 = timing.data_hash(FR.fit(view, starts=3, search="v1"))
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "spread.jsonl")
        os.environ[FR.SPREAD_ENV] = path
        try:
            h1 = timing.data_hash(FR.fit(view, starts=3, search="v1"))
            FR.fit(view, starts=2, search="v2")
        finally:
            os.environ.pop(FR.SPREAD_ENV, None)
        lines = [json.loads(x) for x in open(path, encoding="utf-8").read().splitlines()]
    assert h0 == h1 and len(lines) == 2
    a, b = lines
    assert a["search"] == "v1" and a["k"] == 3 and len(a["J_per_restart"]) == 3
    assert b["search"] == "v2" and b["k"] == 2 and b["second_restart"] is not None
    assert a["n_train_cells"] == len(view.cells) and a["view_sha256_16"] == FR.view_hash(view)
    assert a["J_per_restart"][a["chosen_restart"]] == min(a["J_per_restart"])
    assert all(len(r) == 5 for r in a["best_rules"])
    assert not os.environ.get(FR.SPREAD_ENV)


def test_empty_library_decodes():
    """A genome with no rules and no motifs still decodes (fallback, empty offset sets)."""
    import harness as H
    d = {"E": np.zeros((65, 12), bool), "S": np.ones(65, bool),
         "R__sym16": np.zeros((0, 5), np.int64), "W__sym32": np.array([10], np.int64),
         "A__sym16": np.array([8] * 130 + [4], np.int64), "L": np.zeros(0, np.int64),
         "O": np.zeros((0, 2), np.int64), "P__sym16": np.zeros(0, np.int64)}
    P = H.Predictor("empty", FR.PROGRAM_FILES, lambda v: d)
    out = P.decode(d, H.ALL_CELLS[:5])
    assert np.allclose(out["p_exist"], FR.EPS[4]) and all(o == {} for o in out["offsets"])


if __name__ == "__main__":
    results = {}
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            t0 = time.time()
            r = fn()
            print(f"PASS {name} ({time.time() - t0:.1f}s){'' if r is None else ' ' + str(r)}",
                  flush=True)
