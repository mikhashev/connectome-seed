"""Timing of the first rule's fit, proposal section 2.4: "The timing is measured on shuffled bank 0
only." Nothing here fits or scores the real bank or any real fold. No decode, no score: the fit's
wall time only, plus (for the GPU comparison) the stage-1 J trajectory on shuffled bank 0.

Shuffled bank 0 is built exactly as the harness builds it: harness.shuffled_bank(REAL, 0), i.e.
rewire_and_permute with Generator(PCG64(0)). A fold-style training split of it is every cell
whose fold (folds.csv, by cell position, C6 A10) is not the held-out fold f.

Usage (from the repository root):
    tools/.venv/Scripts/python.exe results/genome/c6/rules/first_rule/timing.py serial
    tools/.venv/Scripts/python.exe results/genome/c6/rules/first_rule/timing.py parallel N_PROC N_FITS
    tools/.venv/Scripts/python.exe results/genome/c6/rules/first_rule/timing.py gpu
    tools/.venv/Scripts/python.exe results/genome/c6/rules/first_rule/timing.py bound
Writes timing_<mode>.json next to this file.
"""

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")                       # one CPU core per fit

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]))

N_FITS_C6 = 1315                                         # C6 A13
CAP_HOURS = 48                                           # proposal section 2.4
_ENV = {}


def shuffled0():
    if "bank" not in _ENV:
        import harness as H
        bank, inv = H.shuffled_bank(H.REAL, 0)
        assert inv["n_nonempty"] == 604 and inv["out_degrees_kept"] and inv["in_degrees_kept"]
        _ENV.update(H=H, bank=bank)
    return _ENV["H"], _ENV["bank"]


def view_for(fold):
    H, bank = shuffled0()
    return H.make_view(bank, H.FOLD != fold)


def data_hash(d):
    h = hashlib.sha256()
    for k in sorted(d):
        a = np.ascontiguousarray(d[k])
        h.update(k.encode() + str(a.dtype).encode() + str(a.shape).encode() + a.tobytes())
    return h.hexdigest()[:16]


def one_fit(args):
    fold, starts = args
    import fit as FR
    v = view_for(fold)
    t0 = time.perf_counter()
    d = FR.fit(v, starts=starts)
    dt = time.perf_counter() - t0
    return {"fold": fold, "starts": starts, "seconds": dt, "hash": data_hash(d),
            "sweeps_per_start": FR.LAST_FIT["sweeps_per_start"],
            "n_rules": FR.LAST_FIT["n_rules"], "n_motifs": FR.LAST_FIT["n_motifs"]}


def _warm(_):
    shuffled0()
    import fit  # noqa: F401
    time.sleep(0.3)
    return os.getpid()


def serial():
    shuffled0()
    out = {"what": "one full fit on shuffled bank 0, fold-0 training split, one CPU core",
           "threads": {k: os.environ.get(k) for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                                                      "MKL_NUM_THREADS")}}
    for starts in (10, 3):
        r = one_fit((0, starts))
        out[f"k{starts}"] = r
        print(f"k={starts}: {r['seconds']:.2f} s per fit; sweeps per start "
              f"{r['sweeps_per_start']}", flush=True)
    for starts in (10, 3):
        s = out[f"k{starts}"]["seconds"]
        out[f"k{starts}"]["projected_hours_1315_fits_1_core"] = N_FITS_C6 * s / 3600
    return out


def parallel(n_proc, n_fits, starts=10):
    import multiprocessing as mp
    shuffled0()
    tasks = [(i % 10, starts) for i in range(n_fits)]
    with mp.Pool(n_proc) as pool:
        pids = pool.map(_warm, range(4 * n_proc), chunksize=1)
        t0 = time.perf_counter()
        res = pool.map(one_fit, tasks, chunksize=1)
        wall = time.perf_counter() - t0
    # the same fits, serially in this process, must give identical data (determinism)
    ser = {}
    for f in sorted({t[0] for t in tasks})[:3]:
        ser[f] = one_fit((f, starts))["hash"]
    same = all(r["hash"] == ser[r["fold"]] for r in res if r["fold"] in ser)
    thr = n_fits / wall                                   # fits per second, whole machine
    out = {"what": f"{n_fits} fits of shuffled bank 0 fold-style splits (folds 0-9 cycled), "
                   f"k={starts}, on a pool of {n_proc} processes, one BLAS thread each",
           "n_proc": n_proc, "n_fits": n_fits, "starts": starts, "workers_seen": len(set(pids)),
           "wall_seconds": wall, "fits_per_hour": 3600 * thr,
           "mean_seconds_per_fit_inside_workers": float(np.mean([r["seconds"] for r in res])),
           "per_fit": res, "parallel_equals_serial_hash": same,
           "projected_hours_1315_fits": N_FITS_C6 / thr / 3600}
    print(f"pool {n_proc}, {n_fits} fits, k={starts}: wall {wall:.1f} s, "
          f"{3600 * thr:.0f} fits/h, projected {out['projected_hours_1315_fits']:.2f} h for "
          f"1,315 fits; parallel == serial: {same}", flush=True)
    return out


def bound():
    """An upper bound, not a run of the procedure: the cost of one sweep in the heaviest state
    the caps allow (40 rules, every label used), times 50 sweeps times k restarts. The
    primitives are timed on shuffled bank 0's fold-0 split with a random 40-rule state."""
    import fit as FR
    v = view_for(0)
    M, Y = FR.grid(v)
    rng = np.random.default_rng(1)
    E = rng.random((65, 12)) < 0.25
    Ef = E.astype(float)
    P = np.zeros((12, 12), bool)
    P.flat[rng.choice(144, FR.R_MAX, replace=False)] = True
    L = FR.rule_matrix(P, rng.integers(16, size=(12, 12)))
    S = Ef @ L @ Ef.T
    eps = FR.EPS[4]
    C = np.where(M, FR.cell_cost(S, eps, Y), 0.0)
    n = 2000
    t0 = time.perf_counter()
    for x in range(n):
        ix = np.ix_(np.flatnonzero(E[:, x % 12]), np.flatnonzero(E[:, (x // 12) % 12]))
        Sn = S[ix][None] + FR.LOG1M_RHO[:, None, None]
        Cn = np.where(M[ix][None], FR.cell_cost(Sn, eps, Y[ix][None]), 0.0)
        int(np.argmin((Cn - C[ix][None]).sum(axis=(1, 2))))
    t16 = (time.perf_counter() - t0) / n
    t0 = time.perf_counter()
    for x in range(n):
        t = x % 65
        srow = Ef @ (Ef[t] @ L)
        scol = Ef @ (L @ Ef[t])
        crow = np.where(M[t], FR.cell_cost(srow, eps, Y[t]), 0.0)
        ccol = np.where(M[:, t], FR.cell_cost(scol, eps, Y[:, t]), 0.0)
        float(np.sum(crow - C[t]) + np.sum(ccol - C[:, t]) - (ccol[t] - C[t, t]))
    tf = (time.perf_counter() - t0) / n
    t0 = time.perf_counter()
    for _ in range(200):
        np.where(M[None], FR.cell_cost(S[None], FR.EPS[:, None, None], Y[None]), 0.0).sum(axis=(1, 2))
    te = (time.perf_counter() - t0) / 200
    sweep = (144 + FR.R_MAX) * t16 + 65 * 12 * tf + te
    out = {"what": bound.__doc__, "candidate_16_levels_s": t16, "flip_s": tf, "leak_s": te,
           "worst_sweep_s": sweep}
    for k in (10, 3):
        f = FR.MAX_SWEEPS * k * sweep
        out[f"k{k}"] = {"worst_fit_s": f, "hours_1315_fits_1_core": N_FITS_C6 * f / 3600,
                        "hours_1315_fits_16_cores": N_FITS_C6 * f / 3600 / 16}
    print(out, flush=True)
    return out


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "serial":
        res = serial()
    elif mode == "parallel":
        n_proc, n_fits = int(sys.argv[2]), int(sys.argv[3])
        starts = int(sys.argv[4]) if len(sys.argv) > 4 else 10
        res = parallel(n_proc, n_fits, starts)
        mode = f"parallel_p{n_proc}_n{n_fits}_k{starts}"
    elif mode == "bound":
        res = bound()
    elif mode == "gpu":
        import gpu_stage1
        res = gpu_stage1.benchmark(view_for)
    else:
        sys.exit(__doc__)
    import platform
    res["machine"] = {"platform": platform.platform(), "processor": platform.processor(),
                      "cpu_count_logical": os.cpu_count(), "numpy": np.__version__,
                      "python": sys.version.split()[0]}
    (HERE / f"timing_{mode}.json").write_text(json.dumps(res, indent=1, default=str) + "\n",
                                              encoding="utf-8", newline="\n")
