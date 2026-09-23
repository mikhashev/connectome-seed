"""Stand-in rule for testing the harness's rule path (not a candidate rule).

It is the planted family PR with PL1's class vector (C6 acceptance file (a); generator seed
4242), run on the real bank. The controls already ran exactly this object as criterion N2, so
this exposes nothing new. It is self-contained: the harness loads it only through the plug-in
interface (NAME, PROGRAM_FILES, fit, RANK), like any rule. `fit` accepts `starts` and ignores it.
"""
import math
from collections import Counter

import numpy as np

NAME = "standin-PR"
PROGRAM_FILES = ["../../decoders/planted_decode.py"]
RANK = 4


def _classes():
    rng = np.random.Generator(np.random.PCG64(4242))
    pi = rng.permutation(65)
    cls = np.zeros(65, dtype=np.int64)
    for j, i in enumerate(pi):
        cls[i] = j % 4
    return cls


CLS = _classes()


def _most_frequent_set(sets):
    c = Counter(tuple(sorted(s)) for s in sets)
    return min(c, key=lambda k: (-c[k], len(k), k))


def fit(view, starts=None):
    cls = CLS
    bp = cls[view.cells[:, 0]] * 4 + cls[view.cells[:, 1]]
    p = np.array([view.exists[bp == q].mean() if (bp == q).any() else 0.0 for q in range(16)])
    n, du, dv, mu = [], [], [], []
    for q in range(16):
        cells = [k for k in view.content if cls[k[0]] * 4 + cls[k[1]] == q]
        if not cells:
            n.append(0)
            mu.append(0.0)
            continue
        st = _most_frequent_set([view.content[k]["offsets"].keys() for k in cells])
        n.append(len(st))
        du += [o[0] for o in st]
        dv += [o[1] for o in st]
        mu.append(float(np.mean([math.log1p(x) for k in cells
                                 for x in view.content[k]["offsets"].values()])))
    sg = np.ones(4, dtype=np.int64)
    for a in range(4):
        signs = [c["sign"] for k, c in view.content.items() if cls[k[0]] == a]
        if sum(x == -1 for x in signs) > sum(x == 1 for x in signs):
            sg[a] = 0
    return {"cls__sym4": cls.copy(), "p": p, "n": np.array(n, dtype=np.int64),
            "du": np.array(du, dtype=np.int64), "dv": np.array(dv, dtype=np.int64),
            "mu": np.array(mu), "sg__sym2": sg}
