"""Generator PG1 of docs/plans/2026-09-23-first-rule-search-criterion.md section 3: planted tables
from the first rule's own model family, under its caps, on 65 type indices. No real content.

pg1(seed) -> dict with "content" (harness bank content), "data" (the planted genome, packed as the
rule's data), "stage1" (E, P, Q, eps level: what J is computed from), "density", "data_bits",
"attempts".
"""

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]))

import fit as FR  # noqa: E402

P_LABEL = 0.12
N_RULES = 12
RHO_LEVELS = (11, 16)
N_MOTIFS = 12
MOTIF_SIZE = (2, 7)
PI_LEVELS = (8, 16)
W_LEVELS = (12, 26)
AB_MEAN, AB_SD = 8, 1.5
W0_LEVELS = (8, 20)
EPS_LEVEL = 9
P_PLUS = 0.6
COUNT_NOISE_SD = 0.3
DENSITY = (0.12, 0.17)
DATA_BITS = (2200, 3600)
MAX_ATTEMPTS = 1000
D2 = [(0, 0)] + [(u, v) for u in range(-2, 3) for v in range(-2, 3)
                 if (u, v) != (0, 0) and max(abs(u), abs(v), abs(u + v)) <= 2]
assert len(D2) == 19


def _decoder():
    import importlib.util
    spec = importlib.util.spec_from_file_location("first_rule_decode", HERE / "decode.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def pg1(seed):
    import harness as H
    dec = _decoder()
    rng = np.random.Generator(np.random.PCG64(seed))
    for att in range(1, MAX_ATTEMPTS + 1):
        E = rng.random((65, 12)) < P_LABEL
        pairs = np.sort(rng.choice(144, N_RULES, replace=False))
        rq = rng.integers(*RHO_LEVELS, N_RULES)
        shapes = [((0, 0),)]
        while len(shapes) < N_MOTIFS:
            n = int(rng.integers(*MOTIF_SIZE))
            picks = rng.choice(18, n - 1, replace=False) + 1
            s = FR.canon([D2[0]] + [D2[i] for i in picks])
            if s not in shapes:
                shapes.append(s)
        pis = [rng.integers(*PI_LEVELS, len(s)) for s in shapes]
        m = rng.integers(N_MOTIFS, size=N_RULES)
        g = rng.integers(12, size=N_RULES)
        w = rng.integers(*W_LEVELS, N_RULES)
        a = np.clip(np.round(rng.normal(AB_MEAN, AB_SD, 65)), 0, 15).astype(np.int64)
        b = np.clip(np.round(rng.normal(AB_MEAN, AB_SD, 65)), 0, 15).astype(np.int64)
        w0 = int(rng.integers(*W0_LEVELS))
        sign = rng.random(65) < P_PLUS
        u = rng.random((65, 65))
        z = rng.normal(0, COUNT_NOISE_SD, (65, 65, 6))
        P = np.zeros((12, 12), bool)
        Q = np.zeros((12, 12), np.int64)
        for x, q in zip(pairs, rq):
            P[x // 12, x % 12], Q[x // 12, x % 12] = True, q
        Ef = E.astype(np.float64)
        p = 1 - (1 - FR.EPS[EPS_LEVEL]) * np.exp(Ef @ FR.rule_matrix(P, Q) @ Ef.T)
        ex = u < p
        R = np.array([[x // 12, x % 12, mm, gg, q] for x, q, mm, gg in zip(pairs, rq, m, g)],
                     np.int64)
        data = {"E": E, "S": sign, "R__sym16": R,
                "W__sym32": np.concatenate([w, [w0]]).astype(np.int64),
                "A__sym16": np.concatenate([a, b, [EPS_LEVEL]]).astype(np.int64),
                "L": np.array([len(s) for s in shapes], np.int64),
                "O": np.array([o for s in shapes for o in s], np.int64).reshape(-1, 2),
                "P__sym16": np.concatenate(pis).astype(np.int64)}
        bits = H.data_bits(data)
        dens = float(ex.mean())
        ok = (DENSITY[0] <= dens <= DENSITY[1] and E.any(axis=0).all()
              and not any((E[:, x] == E[:, y]).all() for x in range(12) for y in range(x))
              and DATA_BITS[0] <= bits <= DATA_BITS[1])
        if not ok:
            continue
        cells = np.array([(s, t) for s in range(65) for t in range(65) if ex[s, t]], np.int64)
        out = dec.decode(H.cast(data), H.TYPE_FIELDS.copy(), cells.copy())
        content = {}
        for n, (s, t) in enumerate(cells.tolist()):
            offs = {(int(du), int(dv)): float(v) * float(np.exp(z[s, t, k]))
                    for k, ((du, dv), v) in enumerate(out["offsets"][n].items())}
            content[(s, t)] = {"offsets": offs, "hull": [], "sign": int(out["sign"][n])}
        return {"content": content, "data": data, "stage1": (E, P, Q, EPS_LEVEL),
                "density": dens, "data_bits": bits, "attempts": att}
    raise RuntimeError(f"PG1 seed {seed}: no accepted draw in {MAX_ATTEMPTS} attempts")
