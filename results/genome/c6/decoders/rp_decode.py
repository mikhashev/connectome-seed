"""RP_r: N1 plus a rank-r term with one side a fixed random projection (C6 Amendment A11).
Charged program; its full program is n1_decode + this file."""
import numpy as np

import n1_decode


def projection(seed, r):
    rng = np.random.Generator(np.random.PCG64(int(seed)))
    return rng.normal(0.0, np.sqrt(1.0 / r), size=(65, r))


def decode(data, type_fields, cells):
    out = n1_decode.decode(data, type_fields, cells)
    B, Bc = data["rp_B"], data["rp_Bc"]
    G = projection(data["rp_seed"][0], B.shape[1])
    s, t = cells[:, 0], cells[:, 1]
    if data["rp_side__sym2"][0] == 0:        # random on the source side, fitted target side
        g, h = G[s], B[t]
        gc, hc = G[s], Bc[t]
    else:                                    # random on the target side, fitted source side
        g, h = G[t], B[s]
        gc, hc = G[t], Bc[s]
    z = n1_decode.logit(data, cells) + np.sum(g * h, axis=1)
    out["p_exist"] = 1.0 / (1.0 + np.exp(-z))
    extra = np.sum(gc * hc, axis=1)
    for i, offs in enumerate(out["offsets"]):
        out["offsets"][i] = {o: float(np.expm1(np.log1p(v) + extra[i])) for o, v in offs.items()}
    return out
