"""BF_r (A19): N1 plus a trained rank-r bilinear term U_s . V_t on the existence logit.
Charged program; its full program is n1_decode + this file."""
import numpy as np

import n1_decode


def decode(data, type_fields, cells):
    out = n1_decode.decode(data, type_fields, cells)
    z = n1_decode.logit(data, cells) + np.sum(data["bf_U"][cells[:, 0]] *
                                              data["bf_V"][cells[:, 1]], axis=1)
    out["p_exist"] = 1.0 / (1.0 + np.exp(-z))
    return out
