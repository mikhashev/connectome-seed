"""Stored cells, verbatim (C6 Amendment A5 storage format). Charged program.

A stored cell exists, with its offsets, counts and sign. An unstored cell is empty."""
import numpy as np


def stored(data):
    out = {}
    start = np.concatenate([[0], np.cumsum(data["cell_noff"])])
    for i, addr in enumerate(data["cell_addr__sym4225"].tolist()):
        a, b = start[i], start[i + 1]
        offs = {(u, v): n for u, v, n in zip(data["off_du"][a:b].tolist(),
                                             data["off_dv"][a:b].tolist(),
                                             data["off_n"][a:b].tolist())}
        out[addr] = (offs, 1 if data["cell_sign"][i] else -1)
    return out


def decode(data, type_fields, cells):
    table = stored(data)
    addr = (cells[:, 0] * 65 + cells[:, 1]).tolist()
    p = np.array([1.0 if a in table else 0.0 for a in addr])
    offsets = [dict(table[a][0]) if a in table else {} for a in addr]
    sign = np.array([table[a][1] if a in table else 1 for a in addr])
    return {"p_exist": p, "offsets": offsets, "sign": sign}
