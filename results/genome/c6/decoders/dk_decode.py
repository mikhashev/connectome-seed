"""D_k: k stored cells verbatim, N1 everywhere else (C6 spec section 3, A5, A6). Charged
program; its full program is n1_decode + store_decode + this file."""
import numpy as np

import n1_decode
import store_decode


def decode(data, type_fields, cells):
    out = n1_decode.decode(data, type_fields, cells)
    table = store_decode.stored(data)
    for i, a in enumerate((cells[:, 0] * 65 + cells[:, 1]).tolist()):
        if a in table:
            out["p_exist"][i] = 1.0
            out["offsets"][i] = dict(table[a][0])
            out["sign"][i] = table[a][1]
    return out
