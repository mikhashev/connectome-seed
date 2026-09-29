#!/usr/bin/env python3
"""The failed-fit branch: a synthetic witness of known cause (calibration of block B's failed-fit U).

Implements docs/plans/2026-09-29-failed-fit-branch-calibration-registration.md, revision 1.8
("the registration"; section numbers below refer to it), with Mike's decisions M1-M8 (section 15):
items (i) + (v) without (iii); CPU only; the families FC, FN1 and FN2 only; uniform swaps; the
exact gate, with every AUC-based object printed a second time under TAU (*_tau).

This file is NEW. It imports block B's script (results/genome/c6/checks/knockout_regrow_block_b.py,
"the B script", imported as K) and the pinned harness, the way the B script imports from A's.
Nothing registered or hashed is edited: not the B script, its tests, fit.py, harness.py, the
capacity survey folder, the pinned stores, nor registrations A and B. Each script change of
section 14 is marked "S-C<n>" where it is made.

What is reused from the B script, unchanged (file:line at commit 10e806c):
  K.make_world's draws (knockout_regrow_block_b.py:1105-1133), copied in _draws/make_world_cal
  because FN changes the board (S-C2); K._fit_one (:1239-1265) for every registered fit;
  K.plan_bank (:1305-1312); K.evaluate_bank (:1441-1536) and K.read_label (:1599-1642) for the
  registered reading; K.auc (:791-800); K.u_kind (:1582-1596); K.label_text (:1666-1696);
  K.reserved_seeds (:1031-1041); K.check_pins (:587-613); K.check_block_and_mask (:646-665);
  K.check_auc_function (:829-857); K.out_dir_refusal (:2987-3019); K.write_sha256sums
  (:3022-3029); K.log / K.tee_to / K.untee (:436-482); K.dump_json (:528-529);
  K.write_text_synced (:3074-3079); K.write_raw (:3062-3066); K.permute_block (:1143-1151);
  K.perm_ceiling_perm (:888-890); K._pred (:1194-1202); K._w_init (:1187-1191).
From the harness (results/genome/c6/harness.py): fit_n1 (:350), make_view (:180), _grid (:702),
_n1_logit_grid (:697), bf_als (:666), shuffled_bank (:907), Bank (:158), TAU (:66).
From fit.py (through the loaded rule's globals, never edited): fit_existence (:119-146),
fit_uvw (:97-112), logit_grid (:115-116), groups (:82-85), LAMBDAS (:57), LAST_FIT (:74).

Run forms (always with PYTHONUTF8=1 when output is redirected):
    tools/.venv/Scripts/python.exe results/genome/c6/checks/failed_fit_calibration.py --dry-run
    tools/.venv/Scripts/python.exe results/genome/c6/checks/failed_fit_calibration.py --estimate --workers 30
    tools/.venv/Scripts/python.exe results/genome/c6/checks/failed_fit_calibration.py --out <new folder> --workers 30
The last form is the registered run. It refuses while REGISTRATION_SHA256_LF_PINNED is None (the
registration is under review) and it is expected to take more than 30 minutes on 30 workers
(--estimate), so it needs Mike's word. --fixture replaces the one real-bank fit (N1's degree terms)
by fixture terms and marks the run NOT THE REGISTERED RUN; with the --smoke-* options it is the
tests' mode.
"""
import sys

import os
import argparse
import contextlib
import csv
import hashlib
import io
import json
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import knockout_regrow_block_b as K  # noqa: E402  (also reconfigures stdout/stderr to UTF-8, S23)

H = K.H
ROOT = K.ROOT
C6 = K.C6

# ------------------------------------------------------------------------------------------
# Identity of this run's inputs.
REGISTRATION = "docs/plans/2026-09-29-failed-fit-branch-calibration-registration.md"
REGISTRATION_REVISION = "1.8"
# The registration is under review; its LF sha256 is pinned by the revision that closes the review.
# While None, the registered form refuses (gate_refusals). The value at rev 1.8 (commit 10e806c) is
# recorded for information only.
REGISTRATION_SHA256_LF_PINNED = None
REGISTRATION_SHA256_LF_AT_REV_1_8 = (
    "28666be9b9aa80d1ad405dc23c6e3d02d8ef4fb9a08f5879b8eedb3faef947ba")
# The B script this file imports, byte-unchanged (LF sha256 at commit 10e806c).
B_SCRIPT = "results/genome/c6/checks/knockout_regrow_block_b.py"
B_SCRIPT_SHA256_LF = "e650e47e5f6660500eca10fcb08f48ad68f41a25838892d3148fcc4616bb887b"
# S-C6: the survey's search is copied from SURVEY with its hash (not imported).
SURVEY_PY = "docs/prereg-scripts/2026-09-29-capacity-survey/survey.py"
SURVEY_PY_SHA256_LF = "0bbdd15cc5f1c9a2bc5b31b33cf36c7650eb8100d71b6535510e8d930b77c000"

# ------------------------------------------------------------------------------------------
# Section 4: the families (M1, M5, M6). Family index i = position (seeds 93100 + 10 i + j).
#   family, k swapped present + k swapped absent, grid of rule #2.1's block-only fit
FAMILIES_CAL = (("FC", 0, "forced"), ("FN1", 1, "registered"), ("FN2", 2, "registered"))
FAMILY_NAMES = tuple(f[0] for f in FAMILIES_CAL)
WORLDS_PER_FAMILY = 5
GAMMA_Z, GAMMA_Z1 = 0.0, 0.0                           # the Nf outside (section 4)
SEED_WORLD_CAL = 93100
N_PERM_REF = 99                                        # section 10
SEED_PERM_REF = 93200
SEED_CERT_STAGE1 = 93300                               # section 4, S-C6
SEED_CERT_REFINE = tuple(range(93301, 93306))
SEED_CERT_DEEP = (93306, 93307)
# S-C11: this registration's own ranges as literals (rev 1.5, Johnny).
LITERAL_WORLD_SEEDS = (set(range(93100, 93105)) | set(range(93110, 93115))
                       | set(range(93120, 93125)))
LITERAL_PERM_REF_SEEDS = set(range(93200, 93299))
LITERAL_CERT_SEEDS = set(range(93300, 93308))
LITERAL_UNUSED_FAMILY_SEEDS = set(range(93130, 93135)) | set(range(93140, 93145))
# Section 4, "Seeds of the design computations, not of this registration" (SURVEY README).
DESIGN_SEEDS = ({2026, 11, 20260929, 2026092901} | set(range(100, 105)) | {200, 201}
                | {0, 1, 2} | set(range(2026092902, 2026092907)))

# Section 5 and 9: numbers fixed before any fit.
FC_FORCED_LAMBDA = 100.0                               # S-C3
FC_REGISTERED_TWICE_COUNT = 480                        # 0.600000 = 240/400 = (2*162 + 156)/2/400
FC_CEIL_1_EXPECTED = 1.0                               # A2
LAMBDA_CAP = 1.0                                       # section 9, the grid's floor
STARTS_100 = 100                                       # ceil_1_starts100 (section 9)
CERT_CUT = K.GATE_CUT                                  # borrowed, not calibrated (section 9)
TAU = K.TAU                                            # harness.py:66
# Section 9: the cert budget, "to be fixed before values"; proposed as the survey rerun's staging
# (run_survey.py `stage`: K = 100 x 500 steps; 5 x K = 500 x 500 steps; 2 x K = 500 x 1,200 steps).
CERT_BUDGET_REGISTERED = {"K1": 100, "steps1": 500, "K2": 500, "steps2": 500,
                          "deep_K": 500, "deep_steps": 1200,
                          "status": "proposed (section 9: to be fixed before values)"}
CERT_BUDGET_TINY = {"K1": 8, "steps1": 100, "K2": 8, "steps2": 100, "deep_K": 8,
                    "deep_steps": 100, "status": "tiny (tests only)"}
FIXTURE_TERMS = (-2.5, np.zeros(65), np.zeros(65))     # the B tests' FIX_TERMS

NOT_REGISTERED_TEXT = "NOT THE REGISTERED RUN"
READING_LINE_FF_QUANT = ("FF-quant: fit side (the class holds the block); the registered "
                         "quantised representation cannot express the float fit.")   # section 3
GATE_ULP_SPLIT = "GATE_ULP_SPLIT"
STOP_RECORD_NAME = "stop_record.json"

# ------------------------------------------------------------------------------------------
# S-C6: the survey's search, copied verbatim from SURVEY survey.py (lines 5-52 of the file whose LF
# sha256 is SURVEY_PY_SHA256_LF). check_survey_copy asserts that this text is a substring of that
# file and that the file carries the pinned hash. It is executed into its own namespace.
SURVEY_SEARCH_SRC = '''def prep(boards):
    Y=np.asarray(boards).reshape(len(boards),-1)
    Pi=np.stack([np.flatnonzero(y==1) for y in Y]); Ni=np.stack([np.flatnonzero(y==0) for y in Y])
    return Pi,Ni
def best_auc(boards,S,T,K=500,steps=800,seed=0,chunk_pairs=3.0e8):
    """Search dynamics in float32 (identical to previous run); every 100 steps the exact count is taken
    in float64 from the float64-cast params: wins d>0, ties d==0, no tolerance.
    returns best count per board, n_pairs, best member per board (float64 a,b,u,v)."""
    boards=np.asarray(boards); nb=len(boards); Pi,Ni=prep(boards)
    npr,nn=Pi.shape[1],Ni.shape[1]; npairs=npr*nn
    per_board=max(1,int(chunk_pairs/(K*npairs*4*3)))
    out=np.zeros(nb); mem=[None]*nb; rng=np.random.default_rng(seed)
    for c0 in range(0,nb,per_board):
        idx=np.arange(c0,min(nb,c0+per_board)); B=len(idx)*K
        bo=np.repeat(np.arange(len(idx)),K); P_=Pi[idx][bo]; N_=Ni[idx][bo]
        P=[rng.normal(size=(B,k)).astype(F32) for k in (S,T,S,T)]
        M=[np.zeros_like(p) for p in P]; V=[np.zeros_like(p) for p in P]
        lr=F32(0.05)
        bestc=np.full(len(idx),-1.0); bestm=[None]*len(idx)
        def sc(P,dt=None):
            a,b,u,v=P
            if dt: a,b,u,v=[x.astype(dt) for x in P]
            return (a[:,:,None]+b[:,None,:]+u[:,:,None]*v[:,None,:]).reshape(B,-1)
        for i in range(steps):
            a,b,u,v=P; Sf=sc(P)
            Sp=np.take_along_axis(Sf,P_,1); Sn=np.take_along_axis(Sf,N_,1)
            temp=F32(0.01**(i/steps))
            d=(Sp[:,:,None]-Sn[:,None,:])/temp
            sg=1/(1+np.exp(-np.clip(d,-30,30))); W=sg*(1-sg)/temp
            Gf=np.zeros_like(Sf)
            np.put_along_axis(Gf,P_,-W.sum(2),1); np.put_along_axis(Gf,N_,W.sum(1),1)
            G=Gf.reshape(B,S,T)
            gr=[G.sum(2),G.sum(1),(G*v[:,None,:]).sum(2),(G*u[:,:,None]).sum(1)]
            for k in range(4):
                M[k]=0.9*M[k]+0.1*gr[k]; V[k]=0.999*V[k]+0.001*gr[k]**2
                P[k]=P[k]-lr*(M[k]/(1-0.9**(i+1)))/(np.sqrt(V[k]/(1-0.999**(i+1)))+1e-8)
            if i%100==99 or i==steps-1:
                Sf=sc(P,np.float64); Sp=np.take_along_axis(Sf,P_,1); Sn=np.take_along_axis(Sf,N_,1)
                d=Sp[:,:,None]-Sn[:,None,:]
                cnt=((d>0).sum((1,2))*2+(d==0).sum((1,2)))/2
                cb=cnt.reshape(len(idx),K); am=cb.argmax(1); mx=cb.max(1)
                for j in range(len(idx)):
                    if mx[j]>bestc[j]:
                        bestc[j]=mx[j]; k=j*K+am[j]
                        bestm[j]=[P[q][k].astype(np.float64).copy() for q in range(4)]
        out[idx]=bestc
        for j,g in enumerate(idx): mem[g]=bestm[j]
    return out,npairs,mem
def frac_count(Y,a,b,u,v):
    S,T=Y.shape
    sc=[[Fraction(float(a[i]))+Fraction(float(b[j]))+Fraction(float(u[i]))*Fraction(float(v[j])) for j in range(T)] for i in range(S)]
    P=[sc[i][j] for i in range(S) for j in range(T) if Y[i,j]==1]; N=[sc[i][j] for i in range(S) for j in range(T) if Y[i,j]==0]
    w=0
    for p in P:
        for q in N:
            w+=2 if p>q else (1 if p==q else 0)
    return w/2
'''
SV = {"np": np, "F32": np.float32, "Fraction": Fraction}
exec(compile(SURVEY_SEARCH_SRC, "survey.py (copied, S-C6)", "exec"), SV)


def check_survey_copy():
    """S-C6: the copied search text is a substring of SURVEY survey.py, and that file carries the
    pinned LF sha256."""
    text = (ROOT / SURVEY_PY).read_bytes().replace(b"\r\n", b"\n")
    got = hashlib.sha256(text).hexdigest()
    ok = got == SURVEY_PY_SHA256_LF and SURVEY_SEARCH_SRC.encode("utf-8") in text
    return {"survey_py": SURVEY_PY, "sha256_lf": got, "pinned": SURVEY_PY_SHA256_LF,
            "copy_is_substring": SURVEY_SEARCH_SRC.encode("utf-8") in text, "passed": ok}


# ------------------------------------------------------------------------------------------
# AUC with the tie rule of section 6a (S-C12).

def auc_counts(p, y):
    """The registered exact AUC (K.auc, B script lines 791-800) with its counts, and the *_tau
    value in which |d| <= TAU counts as a tie. twice = 2 wins + ties (an integer)."""
    p, y = np.asarray(p, np.float64), np.asarray(y, bool)
    pos, neg = p[y], p[~y]
    n = len(pos) * len(neg)
    if n == 0:
        return {"exact": None, "tau": None, "n_pairs": 0, "ulp_sensitive": False}
    d = pos[:, None] - neg[None, :]
    wins, ties = int((d > 0).sum()), int((d == 0).sum())
    wins_t, ties_t = int((d > TAU).sum()), int((np.abs(d) <= TAU).sum())
    exact = K.auc(p, y)
    assert exact == (wins + 0.5 * ties) / n
    tau = (wins_t + 0.5 * ties_t) / n
    return {"exact": exact, "tau": tau, "wins": wins, "ties": ties, "twice": 2 * wins + ties,
            "wins_tau": wins_t, "ties_tau": ties_t, "n_pairs": n, "ulp_sensitive": exact != tau,
            "levels": int(len(np.unique(p)))}


def split_at_cut(obj, cut=K.GATE_CUT):
    """Section 6a: the exact and the _tau value on opposite sides of the cut."""
    if obj.get("exact") is None or obj.get("tau") is None:
        return False
    return (obj["exact"] >= cut) != (obj["tau"] >= cut)


# ------------------------------------------------------------------------------------------
# Section 4: seeds (S-C11) and worlds (S-C1, S-C2).

def world_specs_cal(families=FAMILY_NAMES, per_family=WORLDS_PER_FAMILY):
    return [{"family": fam, "i": i, "j": j, "seed": SEED_WORLD_CAL + 10 * i + j, "k": k,
             "grid": grid, "gamma_z": GAMMA_Z, "gamma_z1": GAMMA_Z1, "board": "z"}
            for i, (fam, k, grid) in enumerate(FAMILIES_CAL) if fam in families
            for j in range(per_family)]


def spec_cal(family, j):
    for w in world_specs_cal():
        if w["family"] == family and w["j"] == j:
            return w
    raise KeyError((family, j))


def perm_ref_seeds(n=N_PERM_REF):
    return [SEED_PERM_REF + j for j in range(n)]


def cert_seeds():
    return [SEED_CERT_STAGE1, *SEED_CERT_REFINE, *SEED_CERT_DEEP]


def b_own_seeds():
    """Block B's own seeds (B section 3.7): SEED_PERM, SEED_RC, the permuted ceilings and the 45
    worlds (knockout_regrow_block_b.py:308-311, 1044-1047)."""
    return ({K.SEED_PERM, K.SEED_RC} | {K.SEED_PERM_CEIL + j for j in range(K.N_PERM_CEILINGS)}
            | {w["seed"] for w in K.world_specs()})


def assert_seeds_cal(starts):
    """S-C11: the seeds the code uses equal this registration's literals; the literal ranges are
    disjoint from one another, from the unused family indices 3 and 4, from reserved_seeds (B
    script lines 1031-1041, with the ALS starts up to STARTS_100), from block B's own seeds and from
    the design seeds. A failure stops before any folder exists."""
    worlds = {w["seed"] for w in world_specs_cal()}
    perm, cert = set(perm_ref_seeds()), set(cert_seeds())
    lits = (LITERAL_WORLD_SEEDS, LITERAL_PERM_REF_SEEDS, LITERAL_CERT_SEEDS)
    new = set().union(*lits)
    reserved = K.reserved_seeds(max(starts, STARTS_100))
    checks = {
        "worlds_equal_literal": worlds == LITERAL_WORLD_SEEDS,
        "perm_ref_equal_literal": perm == LITERAL_PERM_REF_SEEDS,
        "cert_equal_literal": cert == LITERAL_CERT_SEEDS,
        "literals_pairwise_disjoint": sum(len(x) for x in lits) == len(new),
        "unused_family_indices_untouched": not (new & LITERAL_UNUSED_FAMILY_SEEDS),
        "disjoint_from_reserved": not (new & reserved),
        "disjoint_from_B_own": not (new & b_own_seeds()),
        "disjoint_from_design_seeds": not (new & DESIGN_SEEDS),
        "counts": len(LITERAL_WORLD_SEEDS) == 15 and len(LITERAL_PERM_REF_SEEDS) == 99
        and len(LITERAL_CERT_SEEDS) == 8}
    return {"checks": checks, "passed": all(checks.values()), "n_new": len(new),
            "ranges": "worlds 93100-93104, 93110-93114, 93120-93124; permuted reference "
                      "93200-93298; cert 93300-93307"}


def fn_swap(y, k, rng):
    """S-C2 (M6, uniform): k present and k absent cells of the board swapped, drawn uniformly by
    rng (present first, then absent, as fc_anchor.py's `swapped`). 20 / 40 present is kept."""
    y = np.asarray(y, bool).copy()
    if k == 0:
        return y
    pres, absn = np.flatnonzero(y), np.flatnonzero(~y)
    y[rng.choice(pres, k, replace=False)] = False
    y[rng.choice(absn, k, replace=False)] = True
    return y


def _draws(spec):
    """The draws of K.make_world (B script lines 1112-1119) in their order, then the swaps of
    S-C2 from the same generator (ambiguity A-1 in the report). None of them depends on the degree
    terms, so the block pattern is known before any fit."""
    rng = np.random.default_rng(spec["seed"])
    z = K.Z_BLOCK.copy()
    z[K.OTHERS] = np.where(rng.random(len(K.OTHERS)) < 0.5, 1.0, -1.0)
    z1 = np.zeros(65)
    z1[K.BLOCK_TYPES] = K.ZPRIME[K.BLOCK_TYPES]
    z1[K.OTHERS] = np.where(rng.random(len(K.OTHERS)) < 0.5, 1.0, -1.0)
    u = rng.random((65, 65))
    pool = rng.integers(len(K.NONBLOCK_CELLS), size=(65, 65))
    yb = fn_swap(K.board_y("z"), spec["k"], rng)
    return z, z1, u, pool, yb


def world_block_y(spec):
    return _draws(spec)[4]


def make_world_cal(spec, terms):
    """S-C1, S-C2: K.make_world (B script lines 1105-1133) with the board replaced by the world's
    (the z board for FC, the swapped z board for FN) and the Nf outside (gamma_z = gamma_z1 = 0).
    For FC the bank equals K.make_world's for the same seed and board z (a test checks it). The
    assertion of 20 present block cells is kept."""
    z, z1, u, pool, yb = _draws(spec)
    c, a, b = terms
    logit = (c + a[:, None] + b[None, :] + spec["gamma_z"] * np.outer(z, z)
             + spec["gamma_z1"] * np.outer(z1, z1))
    ex = u < 1.0 / (1.0 + np.exp(-logit))
    ex[K.BLOCK] = False
    ex[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]] = yb
    content = {}
    for s, t in zip(*np.nonzero(ex)):
        src = H.REAL_CONTENT[K.NONBLOCK_CELLS[pool[s, t]]]
        content[(int(s), int(t))] = {"offsets": dict(src["offsets"]), "hull": [],
                                     "sign": src["sign"]}
    bank = H.Bank(f"world.{spec['family']}.{spec['seed']}", content)
    assert int(bank.exists[K.BLOCK].sum()) == K.N_WORLD_BLOCK_PRESENT
    return bank


PLACEHOLDER = {"offsets": {(0, 0): 2.0}, "hull": [], "sign": 1}


def constructed_bank(y, name):
    """A bank holding only the 40 block cells (present ones with a placeholder offset set), as
    SURVEY fc_anchor.py's bank_of; used for the permuted-board reference (ambiguity A-6)."""
    y = np.asarray(y, bool)
    content = {tuple(K.BLOCK_CELLS[i].tolist()): {"offsets": dict(PLACEHOLDER["offsets"]),
                                                  "hull": [], "sign": 1}
               for i in range(K.N_BLOCK) if y[i]}
    return H.Bank(name, content)


def perm_ref_y(j):
    """Section 10 (S-C8): permutation j of the z board's 40 labels, default_rng(93200 + j)."""
    perm = np.random.default_rng(SEED_PERM_REF + j).permutation(K.N_BLOCK)
    return K.board_y("z")[perm]


def planted_value(y):
    """Section 5: the exact AUC of the planted score z_s z_t on labels y, as a Fraction."""
    zs = np.array([K.Z_BLOCK[H.IDX[s]] for s, _ in K.BLOCK_NAMES])
    zt = np.array([K.Z_BLOCK[H.IDX[t]] for _, t in K.BLOCK_NAMES])
    sc = (zs * zt).astype(int)
    y = np.asarray(y, bool)
    twice = 0
    for p in sc[y]:
        for q in sc[~y]:
            twice += 2 if p > q else (1 if p == q else 0)
    return Fraction(twice, 2 * int(y.sum()) * int((~y).sum()))


def planted_formula(k):
    """Section 5: ((20 - k)^2 + (20 - k) k) / 400."""
    return Fraction((20 - k) ** 2 + (20 - k) * k, 400)


# ------------------------------------------------------------------------------------------
# Section 6 (S-C6): cert, the capacity search certificate.

def cert_search(y, budget):
    """The survey's staging on one block pattern: stage 1 (seed 93300), 5 refinement reruns (93301-
    93305), 2 deep reruns (93306-93307); the best member kept; its counts by the search (float64,
    exact), by Fraction and by the registered auc; the rerun spread over the 7 reruns."""
    Y = np.asarray(y, bool).reshape(K.N_SOURCES, K.N_TARGETS).astype(int)
    S, T = Y.shape
    best, n, mem = SV["best_auc"]([Y], S, T, K=budget["K1"], steps=budget["steps1"],
                                  seed=SEED_CERT_STAGE1)
    best, mem = float(best[0]), mem[0]
    stages = {"stage1": best, "refine": [], "deep": []}
    for sd in SEED_CERT_REFINE:
        c, _, m = SV["best_auc"]([Y], S, T, K=budget["K2"], steps=budget["steps2"], seed=sd)
        stages["refine"].append(float(c[0]))
        if c[0] > best:
            best, mem = float(c[0]), m[0]
    for sd in SEED_CERT_DEEP:
        c, _, m = SV["best_auc"]([Y], S, T, K=budget["deep_K"], steps=budget["deep_steps"],
                                 seed=sd)
        stages["deep"].append(float(c[0]))
        if c[0] > best:
            best, mem = float(c[0]), m[0]
    frac = SV["frac_count"](Y, *mem)
    a, b, u, v = [np.asarray(x, np.float64) for x in mem]
    score = (a[:, None] + b[None, :] + u[:, None] * v[None, :]).ravel()
    reg = auc_counts(score, y)
    reruns = stages["refine"] + stages["deep"]
    frac_value = Fraction(int(round(2 * frac)), 2 * n)
    return {"n_pairs": int(n), "count_search": best, "count_fraction": frac,
            "count_registered_auc": reg["twice"] / 2,
            "counts_agree": best == frac == reg["twice"] / 2,
            "exact": float(frac_value), "fraction": f"{frac_value.numerator}/{frac_value.denominator}",
            "tau": reg["tau"], "registered_auc_exact": reg["exact"],
            "ulp_sensitive": not (best == frac == reg["twice"] / 2) or reg["exact"] != reg["tau"],
            "rerun_spread": (max(reruns) - min(reruns)) if reruns else None,
            "reruns": reruns, "stages": stages, "budget": dict(budget),
            "member": {"a": a.tolist(), "b": b.tolist(), "u": u.tolist(), "v": v.tolist()}}


# ------------------------------------------------------------------------------------------
# Fits (workers). Every registered fit goes through K._fit_one; the calibration's own fits are
# the forced FC fit (S-C3), the separator's fits (S-C4, S-C4a, S-C4b) and the block fits of BF_r at
# lambda = 1 (S-C4).

@contextlib.contextmanager
def swapped_globals(g, **values):
    """Module globals of fit.py set for one call and restored (train_fixed_lambda's pattern, B
    script lines 1220-1227); fit.py itself is never modified."""
    saved = {k: g[k] for k in values}
    g.update(values)
    try:
        yield
    finally:
        g.update(saved)


def float_p(g, ex):
    """S-C12: the float fit's p on the block, the sigmoid of the float logit (the decoders'
    transform, decode.py line 15, bf_decode.py line 13)."""
    zf = g["logit_grid"](ex["O"], ex["U"], ex["V"], ex["W"], ex["G"])[K.BLOCK_CELLS[:, 0],
                                                                       K.BLOCK_CELLS[:, 1]]
    return 1.0 / (1.0 + np.exp(-zf))


def train_capturing(P, bank, grid):
    """The registered block-only path (P.train on MASKS["block"]) with the grid `grid`, with
    fit_existence's return value captured (fit.py:119-146 is called unchanged); returns (data,
    ex, lambda chosen)."""
    g = P.fit.__globals__
    orig, box = g["fit_existence"], {}

    def capture(*args, **kw):
        box["ex"] = orig(*args, **kw)
        return box["ex"]
    with swapped_globals(g, LAMBDAS=list(grid), fit_existence=capture):
        data = P.train(bank, K.MASKS["block"])
        lam = float(g["LAST_FIT"]["lambda"])
    return data, box["ex"], lam


def train_shortcut(P, bank, lam, starts=None):
    """S-C4b (Zcode's shortcut): with the grid set to [lam] (len(LAMBDAS) == 1), the fold loop is
    skipped: H.fit_n1 and fit_uvw at the one lambda are called directly (fit.py:124, 143-144),
    then fit.py's own quantisation, packing and decode (fit() unchanged). starts overrides the
    number of ALS starts of the final fit (ceil_1_starts100). Returns (data, ex)."""
    g = P.fit.__globals__
    box = {}

    def shortcut(view, st, rounds=g["ROUNDS"], x_on=True):
        assert len(g["LAMBDAS"]) == 1 and float(g["LAMBDAS"][0]) == float(lam)
        G = g["groups"](view.type_fields)
        n1 = H.fit_n1(view)
        M, Y = H._grid(view)
        O = H._n1_logit_grid(n1)
        U, V, W = g["fit_uvw"](O, Y, M, G, lam, st if starts is None else starts, rounds, x_on)
        box["ex"] = {"n1": n1, "O": O, "M": M, "Y": Y, "G": G, "lam": lam, "U": U, "V": V,
                     "W": W, "inner_ll": {}}
        return box["ex"]
    with swapped_globals(g, LAMBDAS=[lam], fit_existence=shortcut):
        data = P.train(bank, K.MASKS["block"])
        assert float(g["LAST_FIT"]["lambda"]) == float(lam)
    return data, box["ex"]


def train_full_path_fixed(P, bank, lam):
    """The full path with the grid forced to [lam] (the fold loop runs): the object S-C4b's
    shortcut must equal bit for bit."""
    g = P.fit.__globals__
    with swapped_globals(g, LAMBDAS=[lam]):
        data = P.train(bank, K.MASKS["block"])
        assert float(g["LAST_FIT"]["lambda"]) == float(lam)
    return data


def forced_block_fit(bk, bank, lam=FC_FORCED_LAMBDA):
    """S-C3: FC's block-only fit of rule #2.1 through the registered K._fit_one (B script lines
    1239-1265) with fit.LAMBDAS swapped to [lam] on MASKS["block"] (train_fixed_lambda's swap,
    which the B script hard-wires to MASKS["ko"], lines 1225, 1231). The chosen lambda is recorded
    (lam), and the stop of section 6 branch (a) reads it; nothing is asserted here."""
    P = K._pred("rule")
    with swapped_globals(P.fit.__globals__, LAMBDAS=[lam]):
        rec = K._fit_one(bk, "block", "rule", bank)
    rec["forced_grid"] = [lam]
    return rec


def separator_fits(bk, bank, forced):
    """S-C4, S-C4a, S-C4b for rule #2.1 on one bank's block: (1) the registered block-only path
    again (forced to [100] for FC), capturing the float fit at the chosen lambda_c; (2) ceil_1 by
    the shortcut at lambda = 1, quantised and float; (3) ceil_1_starts100, the same with 100 starts."""
    t0 = time.time()
    P = K._pred("rule")
    g = P.fit.__globals__
    grid = [FC_FORCED_LAMBDA] if forced else list(g["LAMBDAS"])
    data, ex, lam_c = train_capturing(P, bank, grid)
    out = {"grid": grid, "lambda_c": lam_c,
           "reg_p": np.asarray(P.decode(data, K.BLOCK_CELLS)["p_exist"], np.float64).tolist(),
           "reg_float_p": float_p(g, ex).tolist()}
    d1, e1 = train_shortcut(P, bank, LAMBDA_CAP)
    out["ceil1_p"] = np.asarray(P.decode(d1, K.BLOCK_CELLS)["p_exist"], np.float64).tolist()
    out["ceil1_float_p"] = float_p(g, e1).tolist()
    d100, e100 = train_shortcut(P, bank, LAMBDA_CAP, starts=STARTS_100)
    out["ceil1_s100_p"] = np.asarray(P.decode(d100, K.BLOCK_CELLS)["p_exist"],
                                     np.float64).tolist()
    out["ceil1_s100_float_p"] = float_p(g, e100).tolist()
    out["y"] = bank.exists[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]].tolist()
    out["secs"] = time.time() - t0
    return out


def bf_block_lambda1(pk, bank):
    """S-C4: BF_r's ceil_1 on the block mask: the B script's train_fixed_lambda BF branch (lines
    1230-1236) with MASKS["block"] in place of MASKS["ko"], decoded on the block."""
    t0 = time.time()
    r = int(pk.split(":")[1])
    view = H.make_view(bank, K.MASKS["block"])
    n1 = H.fit_n1(view)
    M, Y = H._grid(view)
    U, V = H.bf_als(H._n1_logit_grid(n1), Y, M, r, LAMBDA_CAP, starts=H.STARTS)
    n1.update({"bf_U": U, "bf_V": V, "bf_lambda": np.array([LAMBDA_CAP])})
    p = K._pred(pk).decode(n1, K.BLOCK_CELLS)["p_exist"]
    return {"p": np.asarray(p, np.float64).tolist(), "lam": LAMBDA_CAP,
            "y": bank.exists[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]].tolist(),
            "secs": time.time() - t0}


def is_fc(bk):
    return bk.split("|")[0].startswith("cal:FC:")


def build_bank_cal(key, terms):
    """Bank keys: "cal:<family>:<j>" (a calibration world) or "perm:<j>" (a permuted reference
    board, constructed), then optional "|sh:<sd>" (harness.shuffled_bank) or "|pc:<j>" (the B
    script's permuted-block ceiling, K.permute_block with K.perm_ceiling_perm)."""
    base, *mods = key.split("|")
    kind, *rest = base.split(":")
    if kind == "cal":
        bank = make_world_cal(spec_cal(rest[0], int(rest[1])), terms)
    elif kind == "perm":
        bank = constructed_bank(perm_ref_y(int(rest[0])), f"permref.{rest[0]}")
    else:
        raise KeyError(key)
    for m in mods:
        if m.startswith("sh:"):
            bank = H.shuffled_bank(bank, int(m[3:]))[0]
        elif m.startswith("pc:"):
            bank = K.permute_block(bank, K.perm_ceiling_perm(int(m[3:])), f"{bank.name}.pc{m[3:]}")
        else:
            raise KeyError(key)
    return bank


def pattern_of(key):
    """The block pattern of a bank key, from the seeds alone (no degree terms, no fit)."""
    kind, *rest = key.split("|")[0].split(":")
    if kind == "cal":
        return world_block_y(spec_cal(rest[0], int(rest[1])))
    if kind == "perm":
        return perm_ref_y(int(rest[0]))
    raise KeyError(key)


def cert_task(key):
    """S-C6: one cert search; module-level, so that the tests can replace it."""
    return cert_search(pattern_of(key), _CW["budget"])


def fit_task(bk, mk, pk, bank):
    """One task: the calibration's own kinds ("sep", "blk1", FC's forced block fit), else the
    registered K._fit_one. Module-level, so that the tests can replace it."""
    if mk == "sep":
        return separator_fits(bk, bank, forced=is_fc(bk))
    if mk == "blk1":
        return bf_block_lambda1(pk, bank)
    if mk == "block" and pk == "rule" and is_fc(bk):
        return forced_block_fit(bk, bank)
    return K._fit_one(bk, mk, pk, bank)


_CW = {}


def _cw_init(starts, terms, budget):
    K._w_init(starts, terms, True)                     # H.STARTS, rule #2.1 loaded (B :1187-1191)
    _CW.update(terms=terms, budget=budget, key=None, bank=None)


def _cw_group(group):
    key = group[0][0]
    if all(mk == "cert" for _, mk, _ in group):        # before any fit: no bank is built
        return [((bk, mk, pk), cert_task(bk)) for bk, mk, pk in group]
    if _CW["key"] != key:
        _CW["bank"], _CW["key"] = build_bank_cal(key, _CW["terms"]), key
    out = []
    for bk, mk, pk in group:
        assert bk == key
        out.append(((bk, mk, pk), fit_task(bk, mk, pk, _CW["bank"])))
    return out


def run_groups(groups, workers, init_args, what):
    """K.run_groups (B script lines 1280-1302) with this file's workers."""
    t0 = time.time()
    K.log(f"[{what}] {len(groups)} groups, {sum(len(g) for g in groups)} tasks, workers = {workers}")
    res = {}
    if workers <= 1:
        _cw_init(*init_args)
        for g in groups:
            res.update(dict(_cw_group(g)))
    else:
        with ProcessPoolExecutor(max_workers=workers, initializer=_cw_init,
                                 initargs=init_args) as ex:
            futs = [ex.submit(_cw_group, g) for g in groups]
            done, step = 0, max(1, len(futs) // 20)
            for f in as_completed(futs):
                res.update(dict(f.result()))
                done += 1
                if done % step == 0 or done == len(futs):
                    el = time.time() - t0
                    K.log(f"[{what}] {done}/{len(futs)} groups, {el:.0f}s elapsed, about "
                          f"{el / done * (len(futs) - done):.0f}s left")
    K.log(f"[{what}] done in {time.time() - t0:.0f}s")
    return res


# ------------------------------------------------------------------------------------------
# Plans.

def world_key(w):
    return f"cal:{w['family']}:{w['j']}"


def plan_world(key, n_sh, n_pc):
    """K.plan_bank (B script lines 1305-1312: ko, full, block for the six predictors, the permuted
    ceilings, the shuffles) and the separator's tasks."""
    return (K.plan_bank(key, n_sh, n_pc) + [[(key, "sep", "rule")]]
            + [[(key, "blk1", pk) for pk in K.BF_KEYS]])


def plan_perm_ref(j):
    """S-C8: block-only fits of one permuted board: BF_1-BF_4 by K._fit_one, rule #2.1 by the
    separator (whose first fit is the registered block path, ceiling_block)."""
    key = f"perm:{j}"
    return [[(key, "block", pk) for pk in K.BF_KEYS], [(key, "sep", "rule")]]


def complete_ko1(F, keys, workers, init_args):
    """K.complete_fixed_lambda (B script lines 2415-2435) with this file's workers: the ko fit at
    lambda = 1 is reused where the selected lambda was 1, else fitted by K._fit_one("ko1")."""
    todo, reused = [], 0
    for bk in keys:
        g = []
        for pk in ("rule",) + K.BF_KEYS:
            if (bk, "ko1", pk) in F:
                continue
            ko = F[(bk, "ko", pk)]
            if ko["lam"] == K.FIXED_LAMBDA:
                F[(bk, "ko1", pk)] = {**ko, "reused_from_ko": True}
                reused += 1
            else:
                g.append((bk, "ko1", pk))
        if g:
            todo.append(g)
    if todo:
        F.update(run_groups(todo, workers, init_args, "fixed lambda = 1 (ko1)"))
    return {"reused": reused, "fitted": sum(len(g) for g in todo)}


# ------------------------------------------------------------------------------------------
# Section 6: the separator's reading; section 7: outcome labels; section 8: gate options.

def ge(x, cut=K.GATE_CUT):
    return x is not None and x >= cut


def separator_reading(cb, cert, c1, c1f, clcf, c1s100):
    """The table of section 6, on the exact values (the registered form; section 6a). cert is the
    Fraction value. Returns (row, sub-kind names)."""
    if ge(cb):
        return "gate passed", []
    if not ge(cert):
        return "not separated: rank limit or fit (no witness either way)", []
    if ge(c1):
        if ge(clcf):
            return ("fit failure, FF-sel; and FF-quant at lambda_c (the float fit at lambda_c "
                    "passed, the quantised one did not)"), ["FF-sel", "FF-quant@lambda_c"]
        return "fit failure, FF-sel", ["FF-sel"]
    if ge(c1f):
        return "fit failure, FF-quant (at lambda = 1)", ["FF-quant"]
    if ge(c1s100):
        return ("fit failure, FF-struct or FF-opt, not separated; ceil_1_starts100 >= 0.90 names "
                "FF-opt"), ["FF-opt"]
    return "fit failure, FF-struct or FF-opt, not separated", ["FF-struct-or-FF-opt"]


GATE_OPTIONS = ("v-a", "v-b", "v-c", "v-d")


def label_under_option(ev, option):
    """S-C9 (section 8): the label each gate option would give, printed; only (v-a) sets the label.
    Before the gate the registered reading is kept (R, W, and the D1 R/W disagreement)."""
    if ev["label"] in ("R", "W") or ev["label_before_readability"] in ("R", "W"):
        return ev["label"]
    if ev["reading_A_rule"]["letter"] in ("R", "W") or ev["reading_B_BF1"]["letter"] in ("R", "W"):
        return ev["label"]
    rows = ev["rows"]
    cb = {pk: rows[pk]["ceiling_block"] for pk in ("rule",) + K.BF_KEYS}
    clear = all(rows[k]["p_P"] > K.P_G for k in ("rule",) + K.BF_KEYS)
    if option == "v-a":
        gate = ge(cb["rule"])
    elif option == "v-b":
        if ge(cb["rule"]) != ge(cb["BF:1"]):
            return "U (the D1 candidates disagree on the gate)"
        gate = ge(cb["rule"])
    elif option == "v-c":
        gate = any(ge(v) for v in cb.values())
    else:
        gate = all(ge(v) for v in cb.values())
    if not ev.get("readable", True):
        return "U (not readable)"
    if clear and gate:
        return "G"
    return "U, failed fit" if not gate else "U"


def outcome_labels(worlds, stops):
    """Section 7: C1-C6. C6 stands whatever the run gives; C5 when a stop row fires; C1/C2 from FC
    and the FN count; C3 when a world meeting the branch has cert >= 0.90, ceil_1 < 0.90 and
    neither diagnostic names the sub-kind."""
    labels = []
    fc = [w for w in worlds if w["family"] == "FC"]
    fn_met = [w for w in worlds if w["family"] != "FC" and w["branch_met"]]
    fc_ffsel = bool(fc) and all(w["branch_met"] and "FF-sel" in w["sep"]["subkinds"] for w in fc)
    fn_fit_row = any(w["sep"]["reading"].startswith("fit failure") for w in fn_met)
    c3 = [w["key"] for w in worlds if w["branch_met"] and ge(w["sep"]["cert"]["exact"])
          and not ge(w["sep"]["ceil_1"]["exact"])
          and w["sep"]["subkinds"] == ["FF-struct-or-FF-opt"]]
    if stops:
        labels.append("C5")
    else:
        if fc_ffsel and fn_fit_row:
            labels.append("C1")
        elif fc_ffsel and not fn_met:
            labels.append("C2")
        if c3:
            labels.append("C3")
    labels.append("C6")
    return {"labels": labels, "fc_reads_ff_sel_all": fc_ffsel,
            "fn_worlds_meeting_branch": f"{len(fn_met)} of "
            f"{sum(1 for w in worlds if w['family'] != 'FC')}",
            "fn_met_keys": [w["key"] for w in fn_met], "c3_worlds": c3}


OUTCOME_TEXT = {
    "C1": "fit side witnessed, natural and forced",
    "C2": "fit side witnessed, forced only",
    "C3": "sub-kind not identified",
    "C5": "branch not reached / stop",
    "C6": "no rank-limit witness on block B's shape (declared before values)"}


# ------------------------------------------------------------------------------------------
# Reading one world.

def read_world(w, F, n_sh, n_pc, certs):
    """The registered reading (K.evaluate_bank, K.read_label) and, beside it, the separator (S-C7),
    the tau values and flags (S-C12), the gate options (S-C9) and the stop rows of section 6."""
    key = world_key(w)
    ev = K.evaluate_bank(key, F, n_sh, n_pc)
    y = np.asarray(F[(key, "ko", "N1")]["y"], bool)
    sp = F[(key, "sep", "rule")]
    assert np.array_equal(np.asarray(sp["y"], bool), y)
    blk = F[(key, "block", "rule")]
    cert = certs[y.tobytes()]
    cb = auc_counts(blk["p"], y)
    sep = {"cert": {k: cert[k] for k in ("exact", "fraction", "tau", "counts_agree",
                                         "ulp_sensitive", "rerun_spread", "n_pairs",
                                         "count_search", "count_fraction",
                                         "count_registered_auc")},
           "ceiling_block": cb, "lambda_block": blk["lam"],
           "ceil_1": auc_counts(sp["ceil1_p"], y),
           "ceil_1_float": auc_counts(sp["ceil1_float_p"], y),
           "ceil_lambda_c_float": auc_counts(sp["reg_float_p"], y), "lambda_c": sp["lambda_c"],
           "ceil_1_starts100": auc_counts(sp["ceil1_s100_float_p"], y),
           "ceil_1_starts100_quantised": auc_counts(sp["ceil1_s100_p"], y),
           "block_fit_reproduced": [float(x) for x in sp["reg_p"]] == [float(x) for x in blk["p"]]}
    sep["bf"] = {pk: {"ceiling_block": auc_counts(F[(key, "block", pk)]["p"], y),
                      "lambda_block": F[(key, "block", pk)]["lam"],
                      "ceil_1": auc_counts(F[(key, "blk1", pk)]["p"], y)} for pk in K.BF_KEYS}
    reading, sub = separator_reading(cb["exact"], cert["exact"], sep["ceil_1"]["exact"],
                                     sep["ceil_1_float"]["exact"],
                                     sep["ceil_lambda_c_float"]["exact"],
                                     sep["ceil_1_starts100"]["exact"])
    sep["reading"], sep["subkinds"] = reading, sub
    if any(s.startswith("FF-quant") for s in sub):
        sep["reading_line"] = READING_LINE_FF_QUANT
    flags = []
    if split_at_cut(cb):
        flags.append(GATE_ULP_SPLIT)
    if split_at_cut(sep["ceil_1"]):
        flags.append("CEIL_1_ULP_SPLIT")
    if (cert["exact"] >= CERT_CUT) != (cert["tau"] >= CERT_CUT):
        flags.append("CERT_ULP_SPLIT")
    kind = K.u_kind(ev["U_reasons"]) if ev["label"] == "U" else None
    branch_met = ev["label"] == "U" and kind == "failed_fit"
    stops = []
    if ev["label"] in ("R", "W"):
        stops.append(f"{key}: reads {ev['label']} (a stop on a calibration world, as on B's Nf)")
    if not sep["block_fit_reproduced"]:
        stops.append(f"{key}: SCRIPT DEFECT: the separator's refit of the registered block-only "
                     "fit differs from it, so ceil_lambda_c_float is not the float of that fit")
    if w["family"] == "FC":
        if not branch_met:
            stops.append(f"{key}: FC does not read failed fit (label {ev['label']}, U kind {kind})")
        if cb["twice"] != FC_REGISTERED_TWICE_COUNT:
            if blk["lam"] != FC_FORCED_LAMBDA:
                br = "(a) LAST_FIT lambda != 100: the forcing did not act, a script defect"
            elif ge(cb["exact"]):
                br = "(b) the forcing acted and the value is >= 0.90: FC is not a witness"
            else:
                br = ("(c) not named by the registration: the forcing acted, the value is below "
                      "0.90 and differs from 0.600000")
            stops.append(f"{key}: ceiling_block {cb['exact']!r} != 0.600000 (240 of 400); {br}")
        if sep["ceil_1"]["exact"] != FC_CEIL_1_EXPECTED:
            stops.append(f"{key}: ceil_1 = {sep['ceil_1']['exact']!r} != 1.0: the registered "
                         "reproduction (A2) failed")
    label_text = (K.label_text(ev["label"], None, None, ev["U_reasons"],
                               ev["rows"]["rule"]["ceiling_block"])
                  if ev["label"] in ("R", "W") or kind in ("failed_fit", "not_readable",
                                                           "not_measured")
                  else f"{ev['label']} (its text needs block B's limits, which this run does not "
                       "measure)")
    return {**w, "key": key, "label": ev["label"], "u_kind": kind, "label_text": label_text,
            "branch_met": branch_met, "ev": ev, "sep": sep, "flags": flags, "stops": stops,
            "smallest_passing_auc": ev["smallest_passing_auc"],
            "gate_options": {o: label_under_option(ev, o) for o in GATE_OPTIONS},
            "planted": w["planted"]}


def read_perm_board(j, F, certs):
    """S-C8: one permuted board, printed; decides nothing."""
    key = f"perm:{j}"
    sp = F[(key, "sep", "rule")]
    y = np.asarray(sp["y"], bool)
    cert = certs[y.tobytes()]
    return {"j": j, "seed": SEED_PERM_REF + j, "present": int(y.sum()),
            "ceiling_block": auc_counts(sp["reg_p"], y), "lambda_c": sp["lambda_c"],
            "ceil_1": auc_counts(sp["ceil1_p"], y),
            "ceil_1_float": auc_counts(sp["ceil1_float_p"], y),
            "ceil_lambda_c_float": auc_counts(sp["reg_float_p"], y),
            "cert": {k: cert[k] for k in ("exact", "fraction", "tau", "counts_agree",
                                          "ulp_sensitive", "rerun_spread")},
            "bf_ceiling_block": {pk: auc_counts(F[(key, "block", pk)]["p"], y)
                                 for pk in K.BF_KEYS}}


# ------------------------------------------------------------------------------------------
# Outputs (ASCII headers; utf-8 files; "\n" line ends).

def v(x, d=6):
    return "" if x is None else (f"{x:.{d}f}" if isinstance(x, float) else str(x))


WORLDS_HEADER = ("family", "j", "seed", "k_swapped", "planted_value", "label", "u_kind",
                 "branch_met", "smallest_passing_auc", "lambda_block_rule",
                 "ceiling_block", "ceiling_block_tau", "ceiling_block_ulp_sensitive",
                 "cert", "cert_fraction", "cert_tau", "cert_counts_agree", "cert_rerun_spread",
                 "ceil_1", "ceil_1_tau", "ceil_1_float", "ceil_1_float_tau", "lambda_c",
                 "ceil_lambda_c_float", "ceil_lambda_c_float_tau", "ceil_1_starts100",
                 "ceil_1_starts100_tau", "separator_reading", "flags", "gate_v_a", "gate_v_b",
                 "gate_v_c", "gate_v_d", "stops")
BF_HEADER = ("family", "j", "seed", "predictor", "lambda_block", "ceiling_block",
             "ceiling_block_tau", "ceiling_block_ulp_sensitive", "ceil_1", "ceil_1_tau",
             "ceil_1_ulp_sensitive")
PERM_HEADER = ("j", "seed", "present", "ceiling_block", "ceiling_block_tau", "lambda_c",
               "ceil_1", "ceil_1_tau", "ceil_1_float", "ceil_1_float_tau", "ceil_lambda_c_float",
               "ceil_lambda_c_float_tau", "cert", "cert_tau", "cert_rerun_spread",
               "bf1_ceiling_block", "bf2_ceiling_block", "bf3_ceiling_block",
               "bf4_ceiling_block")
for _h in (WORLDS_HEADER, BF_HEADER, PERM_HEADER):
    assert all(c.isascii() for c in _h)


def csv_text(header, rows):
    fh = io.StringIO(newline="")
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(header)
    w.writerows(rows)
    return fh.getvalue()


def worlds_rows(worlds):
    out = []
    for w in worlds:
        s = w["sep"]
        out.append([w["family"], w["j"], w["seed"], w["k"], str(w["planted"]), w["label"],
                    w["u_kind"] or "", w["branch_met"], v(w["smallest_passing_auc"]),
                    v(s["lambda_block"]), v(s["ceiling_block"]["exact"]),
                    v(s["ceiling_block"]["tau"]), s["ceiling_block"]["ulp_sensitive"],
                    v(s["cert"]["exact"]), s["cert"]["fraction"], v(s["cert"]["tau"]),
                    s["cert"]["counts_agree"], v(s["cert"]["rerun_spread"]),
                    v(s["ceil_1"]["exact"]), v(s["ceil_1"]["tau"]),
                    v(s["ceil_1_float"]["exact"]), v(s["ceil_1_float"]["tau"]),
                    v(s["lambda_c"]), v(s["ceil_lambda_c_float"]["exact"]),
                    v(s["ceil_lambda_c_float"]["tau"]), v(s["ceil_1_starts100"]["exact"]),
                    v(s["ceil_1_starts100"]["tau"]), s["reading"], ";".join(w["flags"]),
                    *[w["gate_options"][o] for o in GATE_OPTIONS], " | ".join(w["stops"])])
    return out


def bf_rows(worlds):
    return [[w["family"], w["j"], w["seed"], K.PRED_NAME[pk], v(b["lambda_block"]),
             v(b["ceiling_block"]["exact"]), v(b["ceiling_block"]["tau"]),
             b["ceiling_block"]["ulp_sensitive"], v(b["ceil_1"]["exact"]),
             v(b["ceil_1"]["tau"]), b["ceil_1"]["ulp_sensitive"]]
            for w in worlds for pk, b in w["sep"]["bf"].items()]


def perm_rows(perms):
    return [[r["j"], r["seed"], r["present"], v(r["ceiling_block"]["exact"]),
             v(r["ceiling_block"]["tau"]), v(r["lambda_c"]), v(r["ceil_1"]["exact"]),
             v(r["ceil_1"]["tau"]), v(r["ceil_1_float"]["exact"]), v(r["ceil_1_float"]["tau"]),
             v(r["ceil_lambda_c_float"]["exact"]), v(r["ceil_lambda_c_float"]["tau"]),
             v(r["cert"]["exact"]), v(r["cert"]["tau"]), v(r["cert"]["rerun_spread"]),
             *[v(r["bf_ceiling_block"][pk]["exact"]) for pk in K.BF_KEYS]] for r in perms]


def report_md(result):
    m, oc = result["manifest"], result["outcome"]
    L = ["# Failed-fit branch calibration", "",
         f"Registration `{REGISTRATION}`, revision {REGISTRATION_REVISION}. "
         f"git_head={m['git_head']}.", ""]
    if m["not_registered"]:
        L += [f"**{m['not_registered']}**", ""]
    L += ["## Outcome (section 7)", ""]
    L += [f"- **{c}**: {OUTCOME_TEXT[c]}" for c in oc["labels"]]
    L += ["", f"FC reads FF-sel in all its worlds: {oc['fc_reads_ff_sel_all']}. FN worlds meeting "
          f"the branch: {oc['fn_worlds_meeting_branch']}. {GATE_ULP_SPLIT} rows: "
          f"{result['gate_ulp_split_count']}.", ""]
    if result["stops"]:
        L += ["## Stop rows (section 6)", ""] + [f"- {s}" for s in result["stops"]] + [""]
    L += ["## Worlds (registered label beside the separator; the label text is unchanged)", "",
          "| world | seed | label | ceiling_block (tau) | cert | ceil_1 (tau) | ceil_1_float | "
          "lambda_c | ceil_lambda_c_float | ceil_1_starts100 | reads | flags |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for w in result["worlds"]:
        s = w["sep"]
        L.append(f"| {w['key']} | {w['seed']} | {w['label_text']} | "
                 f"{v(s['ceiling_block']['exact'], 4)} ({v(s['ceiling_block']['tau'], 4)}) | "
                 f"{s['cert']['fraction']} | {v(s['ceil_1']['exact'], 4)} "
                 f"({v(s['ceil_1']['tau'], 4)}) | {v(s['ceil_1_float']['exact'], 4)} | "
                 f"{v(s['lambda_c'], 0)} | {v(s['ceil_lambda_c_float']['exact'], 4)} | "
                 f"{v(s['ceil_1_starts100']['exact'], 4)} | {s['reading']} | "
                 f"{', '.join(w['flags']) or '-'} |")
        if s.get("reading_line"):
            L.append(f"|  |  | {s['reading_line']} |  |  |  |  |  |  |  |  |  |")
    L += ["", "## Gate options (section 8; printed, only (v-a) sets the label)", "",
          "| world | " + " | ".join(GATE_OPTIONS) + " |", "|---|---|---|---|---|"]
    L += [f"| {w['key']} | " + " | ".join(w["gate_options"][o] for o in GATE_OPTIONS) + " |"
          for w in result["worlds"]]
    if result["perm_ref"]:
        pr = result["perm_ref"]
        n_fail = sum(1 for r in pr if not ge(r["ceiling_block"]["exact"]))
        n_cert = sum(1 for r in pr if ge(r["cert"]["exact"]))
        L += ["", "## Permuted-board reference (section 10; printed, decides nothing)", "",
              f"{len(pr)} boards; registered ceiling_block below 0.90 on {n_fail} of {len(pr)}; "
              f"cert >= 0.90 on {n_cert} of {len(pr)}. Per board in permuted_reference.csv.", ""]
    return "\n".join(L) + "\n"


def write_outputs(folder, result, F, certs):
    folder = Path(folder)
    K.write_text_synced(folder / "calibration.json", K.dump_json(result) + "\n")
    K.write_text_synced(folder / "worlds.csv", csv_text(WORLDS_HEADER, worlds_rows(result["worlds"])))
    K.write_text_synced(folder / "bf_block.csv", csv_text(BF_HEADER, bf_rows(result["worlds"])))
    K.write_text_synced(folder / "permuted_reference.csv",
                        csv_text(PERM_HEADER, perm_rows(result["perm_ref"])))
    K.write_text_synced(folder / "cert_members.json", K.dump_json(
        {hashlib.sha256(k).hexdigest()[:16]: {**c, "y": np.frombuffer(k, bool).astype(int)
                                              .tolist()} for k, c in certs.items()}) + "\n")
    K.write_raw(F, folder / "raw_fits.json.gz")
    K.write_text_synced(folder / "CALIBRATION.md", report_md(result))


def write_stop_record(folder, message, fields=None):
    if folder is None:
        return None
    path = Path(folder) / STOP_RECORD_NAME
    K.write_text_synced(path, K.dump_json({"stop": message, **(fields or {}), "utc": time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())}) + "\n")
    return path


# ------------------------------------------------------------------------------------------
# Refusals before any folder (arm_gate's pattern, B script lines 3399-3431).

def registered_form(a):
    return (not a.fixture and a.worlds_per_family == WORLDS_PER_FAMILY
            and a.shuffles == K.N_SHUFFLES and a.perm_ceilings == K.N_PERM_CEILINGS
            and a.perm_ref == N_PERM_REF and list(a.families) == list(FAMILY_NAMES)
            and a.cert_budget == "registered" and a.starts == 10)


def gate_refusals(a):
    """Every refusal that needs no fit and no folder: the B script's checks 1, 2 and 7 (pins and
    versions, block and mask, AUC function), the B script and SURVEY hashes, the seeds (S-C11), the
    --out folder (K.out_dir_refusal: never at or inside a reference; plus: it must not exist yet,
    so that no output can be placed before the run), the tree (a registered-form run from a dirty
    tree is refused unless --allow-dirty, which marks it NOT THE REGISTERED RUN), and the
    registration pin (a registered-form run refuses while REGISTRATION_SHA256_LF_PINNED is None or
    differs)."""
    out = {"pins": K.check_pins(), "block_and_mask": K.check_block_and_mask(),
           "auc_function": K.check_auc_function()}
    b_now = K.sha256_lf(ROOT / B_SCRIPT)
    if b_now != B_SCRIPT_SHA256_LF:
        sys.exit(f"REFUSED: {B_SCRIPT} has LF sha256 {b_now}, pinned {B_SCRIPT_SHA256_LF}")
    out["b_script_sha256_lf"] = b_now
    sv = check_survey_copy()
    if not sv["passed"]:
        sys.exit(f"REFUSED: the copied survey search does not match {SURVEY_PY}: {sv}")
    out["survey_copy"] = sv
    seeds = assert_seeds_cal(a.starts)
    if not seeds["passed"]:
        sys.exit(f"SEEDS NOT UNIQUE (S-C11): {seeds['checks']}")
    out["seeds"] = seeds
    if a.out is not None:
        r = K.out_dir_refusal(a.out)
        if r:
            sys.exit(r)
        if Path(a.out).exists():
            sys.exit(f"REFUSED: --out {a.out} exists; the calibration writes into a new folder, so "
                     "that no file can be placed there before the run")
    reg_now = K.sha256_lf(ROOT / REGISTRATION)
    out["registration_sha256_lf"] = reg_now
    dirty = K.tree_state()
    out["dirty"] = dirty
    refusals = []
    if registered_form(a):
        if REGISTRATION_SHA256_LF_PINNED is None:
            refusals.append("REFUSED: the registration is not pinned (REGISTRATION_SHA256_LF_PINNED "
                            "is None: it is under review); the registered run waits for the "
                            "revision that pins it")
        elif reg_now != REGISTRATION_SHA256_LF_PINNED:
            refusals.append(f"REFUSED: {REGISTRATION} has LF sha256 {reg_now}, pinned "
                            f"{REGISTRATION_SHA256_LF_PINNED}")
        if dirty and not a.allow_dirty:
            refusals.append("REFUSED: uncommitted changes under results/genome/c6/ or docs/plans/; "
                            "the calibration must be tied to a commit (or pass --allow-dirty to run "
                            f"it as {NOT_REGISTERED_TEXT}).\n" + dirty)
    out["refusals_of_a_run"] = refusals
    if refusals and a.out is not None and not (a.dry_run or a.estimate):
        sys.exit("\n".join(refusals))
    return out


# ------------------------------------------------------------------------------------------
# The wall-time estimate (a fixture-scale timing, not a world).

def estimate(a):
    """Times one task of each kind on a fixture-scale bank (FC world 0 built with FIXTURE_TERMS, so
    no real-bank fit) and one cert search at the registered budget, then scales by the registered
    task counts. No world is run. Returns the estimate, CPU-seconds and wall-seconds."""
    K._w_init(a.starts, FIXTURE_TERMS, True)
    _CW.update(terms=FIXTURE_TERMS, budget=CERT_BUDGET_REGISTERED, key=None, bank=None)
    spec = spec_cal("FC", 0)
    bank = make_world_cal(spec, FIXTURE_TERMS)
    fn_bank = make_world_cal(spec_cal("FN1", 0), FIXTURE_TERMS)
    t = {}

    def timed(name, fn):
        t0 = time.time()
        fn()
        t[name] = time.time() - t0
        K.log(f"[estimate] {name}: {t[name]:.1f}s")
    for pk in K.PRED_KEYS:
        timed(f"ko:{pk}", lambda pk=pk: K._fit_one("cal:FN1:0", "ko", pk, fn_bank))
    for pk in K.PRED_KEYS:
        timed(f"full:{pk}", lambda pk=pk: K._fit_one("cal:FN1:0", "full", pk, fn_bank))
    for pk in K.PRED_KEYS:
        timed(f"block:{pk}", lambda pk=pk: K._fit_one("cal:FN1:0", "block", pk, fn_bank))
    timed("block_forced:rule", lambda: forced_block_fit("cal:FC:0", bank))
    timed("sep:rule", lambda: separator_fits("cal:FN1:0", fn_bank, forced=False))
    timed("blk1:BF:4", lambda: bf_block_lambda1("BF:4", fn_bank))
    timed("cert", lambda: cert_search(world_block_y(spec_cal("FN2", 0)), CERT_BUDGET_REGISTERED))
    ko = sum(t[f"ko:{pk}"] for pk in K.PRED_KEYS)
    full = sum(t[f"full:{pk}"] for pk in K.PRED_KEYS)
    block = sum(t[f"block:{pk}"] for pk in K.PRED_KEYS)
    ko1 = sum(t[f"ko:{pk}"] for pk in ("rule",) + K.BF_KEYS)      # upper bound: never reused
    per_world = ((1 + K.N_SHUFFLES) * ko + full + block + K.N_PERM_CEILINGS * t["full:rule"]
                 + t["sep:rule"] + 4 * t["blk1:BF:4"] + ko1)
    per_perm = t["sep:rule"] + sum(t[f"block:{pk}"] for pk in K.BF_KEYS)
    n_worlds = len(FAMILY_NAMES) * WORLDS_PER_FAMILY
    n_patterns = 3 + N_PERM_REF                        # FC's 5 worlds share one board
    cpu = n_worlds * per_world + N_PERM_REF * per_perm + n_patterns * t["cert"]
    longest = max(t.values())
    wall = cpu / a.workers + longest
    return {"timings_s": t, "per_world_cpu_s": per_world, "per_perm_board_cpu_s": per_perm,
            "cert_s": t["cert"], "total_cpu_s": cpu, "workers": a.workers,
            "wall_s_estimate": wall, "wall_min_estimate": wall / 60,
            "over_30_min": wall > 1800,
            "method": "one task of each kind timed on a fixture-scale bank (fixture degree terms; "
                      "outside density differs from the real terms'), scaled by the registered "
                      "task counts; ko1 counted as fitted (upper bound); ideal division by the "
                      "workers plus the longest single task"}


# ------------------------------------------------------------------------------------------

def parse(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None, help="a new folder for the outputs")
    ap.add_argument("--workers", type=int, default=30)
    ap.add_argument("--starts", type=int, choices=[3, 10], default=10)
    ap.add_argument("--dry-run", action="store_true",
                    help="refusals, seeds, planted values and the task plan; no fit, no write")
    ap.add_argument("--estimate", action="store_true",
                    help="time one task of each kind on a fixture-scale bank; no world")
    ap.add_argument("--fixture", action="store_true",
                    help="fixture degree terms in place of the real-bank N1 fit; NOT the "
                         "registered run")
    ap.add_argument("--allow-dirty", action="store_true")
    ap.add_argument("--smoke-worlds", type=int, default=None)
    ap.add_argument("--smoke-shuffles", type=int, default=None)
    ap.add_argument("--smoke-perm-ceilings", type=int, default=None)
    ap.add_argument("--smoke-families", default=None)
    ap.add_argument("--smoke-perm-ref", type=int, default=None)
    ap.add_argument("--cert-budget", choices=["registered", "tiny"], default="registered")
    a = ap.parse_args(argv)
    a.worlds_per_family = a.smoke_worlds if a.smoke_worlds is not None else WORLDS_PER_FAMILY
    a.shuffles = a.smoke_shuffles if a.smoke_shuffles is not None else K.N_SHUFFLES
    a.perm_ceilings = (a.smoke_perm_ceilings if a.smoke_perm_ceilings is not None
                       else K.N_PERM_CEILINGS)
    a.families = a.smoke_families.split(",") if a.smoke_families else list(FAMILY_NAMES)
    a.perm_ref = a.smoke_perm_ref if a.smoke_perm_ref is not None else N_PERM_REF
    return a


def main(argv=None):
    a = parse(argv)
    t0 = time.time()
    K._LOG["buffer"].clear()
    K._LOG["output_errors"] = 0
    gate = gate_refusals(a)                            # before any folder (arm_gate's rule)
    head = K.git("rev-parse", "HEAD")
    not_registered = None
    if not registered_form(a):
        not_registered = (f"{NOT_REGISTERED_TEXT}: "
                          + ("fixture degree terms; " if a.fixture else "")
                          + "a smoke or non-registered form")
    elif gate["dirty"]:
        not_registered = f"{NOT_REGISTERED_TEXT}: made with --allow-dirty from an uncommitted tree"
    if a.estimate:
        est = estimate(a)
        K.log(f"ESTIMATE: {est['wall_min_estimate']:.1f} min on {a.workers} workers "
              f"(total CPU {est['total_cpu_s'] / 3600:.2f} h); over 30 min: {est['over_30_min']}")
        return {"estimate": est}
    specs = [w for w in world_specs_cal(a.families, a.worlds_per_family)]
    for w in specs:                                    # section 5: planted values, exact
        y = world_block_y(w)
        w["planted"] = planted_value(y)
        assert w["planted"] == planted_formula(w["k"]), (w, w["planted"])
    if a.dry_run or a.out is None:
        n_tasks = sum(len(g) for w in specs for g in plan_world(world_key(w), a.shuffles,
                                                                 a.perm_ceilings))
        K.log(f"DRY RUN: gate passed; {len(specs)} worlds, {n_tasks} world tasks (+ ko1), "
              f"{a.perm_ref} permuted boards; planted values "
              + ", ".join(f"{w['family']}:{w['j']} {w['planted']}" for w in specs)
              + "; nothing fitted, nothing written; a run in this form would be refused: "
              + (" / ".join(r.splitlines()[0] for r in gate["refusals_of_a_run"]) or "no"))
        return {"dry_run": True, "gate": gate, "worlds": specs}
    folder = Path(a.out)
    folder.mkdir(parents=True, exist_ok=False)
    K.tee_to(folder / "stdout.log")
    K._RUN.update(folder=folder, arm="failed-fit-calibration", head=head)  # rc_patterns' stop record
    completed = False
    try:
        result = _run(a, t0, head, gate, not_registered, specs, folder)
        completed = result.get("completed", False)
    finally:
        K.untee()
        K._RUN.update(folder=None, arm=None, head=None)
    if completed:
        K.write_sha256sums(folder)                     # last, only for a completed run
    else:
        sys.exit(1)
    return result


def _run(a, t0, head, gate, not_registered, specs, folder):
    budget = CERT_BUDGET_REGISTERED if a.cert_budget == "registered" else CERT_BUDGET_TINY
    K.log(f"registration: {REGISTRATION}, revision {REGISTRATION_REVISION}; LF sha256 "
          f"{gate['registration_sha256_lf']} (pinned: {REGISTRATION_SHA256_LF_PINNED})"
          + (f"; {not_registered}" if not_registered else "")
          + f"; k = {a.starts}; workers = {a.workers}; CPU (M2)")
    K.log(f"checks passed: pins and versions, block and mask, AUC function, B script LF sha256 "
          f"{gate['b_script_sha256_lf'][:12]}, survey copy, seeds ({gate['seeds']['ranges']})")
    K.log("planted values (section 5, exact): " + ", ".join(
        f"{w['family']}:{w['j']} {w['planted']}" for w in specs))
    # Section 6 (S-C6, A3): cert on every block pattern, before any fit.
    patterns = {}
    for w in specs:
        patterns.setdefault(world_block_y(w).tobytes(), f"cal:{w['family']}:{w['j']}")
    for j in range(a.perm_ref):
        patterns.setdefault(perm_ref_y(j).tobytes(), f"perm:{j}")
    init_args = (a.starts, FIXTURE_TERMS if a.fixture else None, budget)
    res = run_groups([[(key, "cert", "cert")] for key in patterns.values()], a.workers,
                     init_args, "cert (before any fit)")
    certs = {yk: res[(key, "cert", "cert")] for yk, key in patterns.items()}
    a3 = []
    for w in specs:
        c = certs[world_block_y(w).tobytes()]
        if Fraction(c["fraction"]) < w["planted"]:
            a3.append(f"cal:{w['family']}:{w['j']}: cert {c['fraction']} < planted {w['planted']}")
    if a3:
        msg = ("CERT BELOW THE PLANTED VALUE (A3): the search budget is too small; the run stops "
               "before any fit: " + "; ".join(a3))
        K.log(msg)
        write_stop_record(folder, msg, {"outcome": "C5"})
        return {"completed": False, "stops": [msg]}
    K.log("A3 (cert >= planted value on every FC and FN board): passed; " + ", ".join(
        f"{w['family']}:{w['j']} {certs[world_block_y(w).tobytes()]['fraction']}" for w in specs))
    # Section 4: N1's degree terms (the one real-bank fit), or the fixture's.
    terms = FIXTURE_TERMS if a.fixture else K.degree_terms()
    init_args = (a.starts, terms, budget)
    groups = []
    for w in specs:
        groups += plan_world(world_key(w), a.shuffles, a.perm_ceilings)
    for j in range(a.perm_ref):
        groups += plan_perm_ref(j)
    F = run_groups(groups, a.workers, init_args, "worlds and permuted boards")
    ko1 = complete_ko1(F, [world_key(w) for w in specs], a.workers, init_args)
    worlds = [read_world(w, F, a.shuffles, a.perm_ceilings, certs) for w in specs]
    perms = [read_perm_board(j, F, certs) for j in range(a.perm_ref)]
    stops = [s for w in worlds for s in w["stops"]]
    outcome = outcome_labels(worlds, stops)
    manifest = {"registration": REGISTRATION, "revision": REGISTRATION_REVISION,
                "registration_sha256_lf": gate["registration_sha256_lf"],
                "registration_pinned": REGISTRATION_SHA256_LF_PINNED,
                "script_sha256_lf": K.sha256_lf(Path(__file__)),
                "b_script_sha256_lf": gate["b_script_sha256_lf"], "git_head": head,
                "tree_dirty_paths": gate["dirty"].splitlines() if gate["dirty"] else [],
                "not_registered": not_registered, "fixture": a.fixture,
                "families": a.families, "worlds_per_family": a.worlds_per_family,
                "shuffles": a.shuffles, "perm_ceilings": a.perm_ceilings,
                "perm_ref": a.perm_ref, "starts": a.starts, "workers": a.workers,
                "cert_budget": budget, "device": "CPU",
                "command_environment": K.command_environment(),
                "machine_record": K.machine_record(), "seeds": gate["seeds"],
                "survey_copy": gate["survey_copy"], "ko1": ko1,
                "degree_terms": {"c": terms[0], "a": terms[1], "b": terms[2],
                                 "source": "fixture" if a.fixture else
                                 "N1 on the real bank's knockout view of block B"},
                "runtime_s": time.time() - t0, "log_output_errors": K._LOG["output_errors"]}
    result = {"manifest": manifest, "outcome": outcome, "stops": stops,
              "gate_ulp_split_count": sum(GATE_ULP_SPLIT in w["flags"] for w in worlds),
              "worlds": [{k: x for k, x in w.items() if k != "ev"} | {
                  "planted": str(w["planted"]), "rows": w["ev"]["rows"],
                  "U_reasons": w["ev"]["U_reasons"]} for w in worlds],
              "perm_ref": perms}
    write_outputs(folder, result, F, certs)            # on disk before the tables are printed
    for w in worlds:
        s = w["sep"]
        K.log(f"{w['key']} (seed {w['seed']}): label {w['label_text']}; ceiling_block "
              f"{v(s['ceiling_block']['exact'])} (tau {v(s['ceiling_block']['tau'])}, lambda "
              f"{v(s['lambda_block'])}); cert {s['cert']['fraction']} (tau {v(s['cert']['tau'])}); "
              f"ceil_1 {v(s['ceil_1']['exact'])} (tau {v(s['ceil_1']['tau'])}); ceil_1_float "
              f"{v(s['ceil_1_float']['exact'])}; ceil_lambda_c_float "
              f"{v(s['ceil_lambda_c_float']['exact'])} at lambda_c {v(s['lambda_c'])}; "
              f"ceil_1_starts100 {v(s['ceil_1_starts100']['exact'])}; reads: {s['reading']}; "
              f"flags {w['flags'] or '-'}; gate options {w['gate_options']}")
    K.log(f"OUTCOME: {', '.join(outcome['labels'])}; {outcome}")
    if stops:
        msg = "STOP ROWS FIRED (C5): " + " | ".join(stops)
        K.log(msg)
        write_stop_record(folder, msg, {"outcome": "C5"})
        return {**result, "completed": False}
    K.log(f"done in {time.time() - t0:.0f}s")
    return {**result, "completed": True}


if __name__ == "__main__":
    main()
