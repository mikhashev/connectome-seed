"""N0, the global-marginal null (C6 spec section 3, Amendment A4). Charged program."""
import numpy as np


def decode(data, type_fields, cells):
    n = len(cells)
    offs = {(a, b): float(np.expm1(v)) for a, b, v in zip(
        data["n0_du"].tolist(), data["n0_dv"].tolist(), data["n0_cnt"].tolist())}
    sign = 1 if data["n0_sign__sym2"][0] == 1 else -1
    return {"p_exist": np.full(n, float(data["p0"][0])),
            "offsets": [dict(offs) for _ in range(n)], "sign": np.full(n, sign)}
