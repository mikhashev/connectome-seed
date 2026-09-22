"""N1, the type-marginal null (C6 spec section 3, Amendment A4). Charged program."""
import numpy as np


def logit(data, cells):
    s, t = cells[:, 0], cells[:, 1]
    return data["ex_c"][0] + data["ex_a"][s] + data["ex_b"][t]


def decode(data, type_fields, cells):
    s, t = cells[:, 0], cells[:, 1]
    p = 1.0 / (1.0 + np.exp(-logit(data, cells)))
    start = np.concatenate([[0], np.cumsum(data["set_len"])])
    n0 = list(zip(data["n0_du"].tolist(), data["n0_dv"].tolist()))
    m = {(a, b): v for a, b, v in zip(data["m_du"].tolist(), data["m_dv"].tolist(),
                                      data["m_val"].tolist())}
    m_all = float(data["m_all"][0])
    offsets = []
    for si, ti in zip(s.tolist(), t.tolist()):
        if data["set_has"][si]:
            a, b = start[si], start[si + 1]
            offs = list(zip(data["set_du"][a:b].tolist(), data["set_dv"][a:b].tolist()))
        else:
            offs = n0
        base = float(data["cnt_a"][si] + data["cnt_b"][ti])
        offsets.append({o: float(np.expm1(m.get(o, m_all) + base)) for o in offs})
    n0_sign = 1 if data["n0_sign__sym2"][0] == 1 else -1
    sym = data["src_sign__sym3"][s]
    sign = np.where(sym == 0, -1, np.where(sym == 1, 1, n0_sign))
    return {"p_exist": p, "offsets": offsets, "sign": sign}
