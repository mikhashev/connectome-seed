"""GPU port of rule #2.1's existence fit (rules/second_rule_v21/fit.py, fit_existence), batched
across many views. A separate instrument, not reviewed; the registered CPU run does not use it.

What rule #2.1's fit does (fit.py:95-147, 358-399), and what is ported:
  * fit_existence: N1 on the view; lambda by the nested inner-fold scheme of BF_r (10 folds x
    5 lambdas); inside every inner fit and in the final fit, fit_uvw: ROUNDS = 3 rounds of
    (i) harness.bf_als at rank 1 with offset O + W[G, G] (k = starts), then (ii) W (16 entries)
    by harness.ridge_logistic on the group-pair indicators, offset O + u.v, penalty MU.
    Step (i) is the expensive part (3 x 51 bf_als calls per fit, three times BF_1's count) and is
    batched on the GPU here with gpu_bf2.bf_als_problems, across every (view x fold x lambda)
    problem of a round at once. Step (ii) stays on the CPU and is the exact harness call
    (harness.ridge_logistic, 16 parameters), made per problem between the batched rounds; the
    inner log-likelihood, the lambda rule (ties within 1e-9 to the larger lambda) and the
    returned dict are computed by the same expressions as fit_existence.
  * Everything after fit_existence -- quantisation (ExistQ), coordinate descent, refit of c,
    the offset library and N_EB-style sides (fit_offsets), counts and signs -- is NOT
    reimplemented: the rule's own fit() runs on the CPU, with fit_existence replaced, in a rule
    module object this instrument loaded itself (harness.load_rule), by a function that returns
    the GPU result for that exact view. fit.py on disk is not modified. That CPU part runs in
    pool workers (prep.rule_post_key, prep.install_existence), which never import torch.
"""
import time

import numpy as np
import torch

from gpu_bf2 import H, bf_als_problems

TIMES = {"bf_als_gpu": 0.0, "ridge_cpu": 0.0}           # accumulated wall seconds, per stage


def _rule_consts(g):
    return g["LAMBDAS"], g["ROUNDS"], g["MU"], g["LAMBDA_TIE"]


def batched_fit_uvw(problems, g, starts):
    """fit_uvw(O, Y, M, G, lam, starts) with x_on=True for every problem (dict O, Y, M, G, lam),
    rounds batched on the GPU. Returns lists U, V (65 x 1), W (4 x 4)."""
    _, rounds, mu, _ = _rule_consts(g)
    group_design = g["group_design"]
    n = len(problems)
    W = [np.zeros((4, 4)) for _ in range(n)]
    cells = [np.argwhere(p["M"] > 0) for p in problems]      # row-major, as fit_uvw
    X16 = [group_design(c, p["G"]) for c, p in zip(cells, problems)]
    y = [p["Y"][c[:, 0], c[:, 1]] for c, p in zip(cells, problems)]
    Ys = np.stack([p["Y"] for p in problems])
    Ms = np.stack([p["M"] for p in problems])
    lam = np.array([float(p["lam"]) for p in problems])
    U = V = None
    for _ in range(rounds):
        off = np.stack([p["O"] + W[i][np.ix_(p["G"], p["G"])] for i, p in enumerate(problems)])
        t0 = time.time()
        U, V = bf_als_problems(off, Ys, Ms, 1, lam, starts)
        if torch.cuda.is_available():
            torch.cuda.synchronize()
        t1 = time.time()
        for i, p in enumerate(problems):
            z = (p["O"] + U[i] @ V[i].T)[cells[i][:, 0], cells[i][:, 1]]
            W[i] = H.ridge_logistic(X16[i], y[i], z, np.ones(16), lam=mu).reshape(4, 4)
        TIMES["bf_als_gpu"] += t1 - t0
        TIMES["ridge_cpu"] += time.time() - t1
    return [U[i] for i in range(n)], [V[i] for i in range(n)], W


def batched_fit_existence(preps, g, starts):
    """fit_existence(view, starts) (x_on=True, rounds=ROUNDS) for every prepared view
    (prep.prepare_view output). Returns the dicts fit_existence returns, in order."""
    lambdas, _, _, tie = _rule_consts(g)
    G = g["groups"](H.TYPE_FIELDS.copy())
    logit_grid = g["logit_grid"]
    probs, owner = [], []
    for vi, pp in enumerate(preps):
        for fi in range(len(pp["folds"])):
            for lam in lambdas:
                probs.append({"O": pp["Oi"][fi], "Y": pp["Y"], "M": pp["Mi"][fi], "G": G,
                              "lam": lam})
                owner.append((vi, fi, lam))
    U, V, W = batched_fit_uvw(probs, g, starts)
    ll = [{lam: 0.0 for lam in lambdas} for _ in preps]
    for q, (vi, fi, lam) in enumerate(owner):             # folds outer, lambdas inner
        pp = preps[vi]
        p = np.clip(H._sig(logit_grid(pp["Oi"][fi], U[q], V[q], W[q], G)), *H.CLIP)
        ll[vi][lam] += float(np.sum(np.where(pp["Y"] > 0, np.log(p), np.log(1 - p))
                                    [pp["test"][fi]]))
    lam_ch = []
    for d in ll:
        best = max(d.values())
        lam_ch.append(max(l for l in lambdas if d[l] >= best - tie))
    finals = [{"O": pp["O"], "Y": pp["Y"], "M": pp["M"], "G": G, "lam": lam_ch[vi]}
              for vi, pp in enumerate(preps)]
    U, V, W = batched_fit_uvw(finals, g, starts)
    out = []
    for vi, pp in enumerate(preps):
        out.append({"n1": {k: np.array(v, copy=True) for k, v in pp["n1"].items()},
                    "O": pp["O"], "M": pp["M"], "Y": pp["Y"], "G": G, "lam": lam_ch[vi],
                    "U": U[vi], "V": V[vi], "W": W[vi], "inner_ll": ll[vi]})
    return out

