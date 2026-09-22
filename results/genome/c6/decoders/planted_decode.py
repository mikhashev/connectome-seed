# planted rule PR: 4 classes; per class pair rate, offset set, log count; sign per class
import numpy as np


def decode(d, f, c):
    a = d["cls__sym4"][c[:, 0]]
    j = a * 4 + d["cls__sym4"][c[:, 1]]
    s = np.concatenate([[0], np.cumsum(d["n"])])
    o = []
    for q in j.tolist():
        m = float(np.expm1(d["mu"][q]))
        o.append({(u, v): m for u, v in zip(d["du"][s[q]:s[q + 1]].tolist(),
                                            d["dv"][s[q]:s[q + 1]].tolist())})
    return {"p_exist": d["p"][j], "offsets": o, "sign": np.where(d["sg__sym2"][a] == 1, 1, -1)}
