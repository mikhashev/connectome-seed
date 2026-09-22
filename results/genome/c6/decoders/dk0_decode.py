"""D_k armed (A17): k stored cells verbatim, N0 everywhere else. Charged program; its full
program is n0_decode + store_decode + this file, charged once (one basis, one charge)."""
import n0_decode
import store_decode


def decode(data, type_fields, cells):
    out = n0_decode.decode(data, type_fields, cells)
    table = store_decode.stored(data)
    for i, a in enumerate((cells[:, 0] * 65 + cells[:, 1]).tolist()):
        if a in table:
            out["p_exist"][i] = 1.0
            out["offsets"][i] = dict(table[a][0])
            out["sign"][i] = table[a][1]
    return out
