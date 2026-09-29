#!/usr/bin/env python3
"""The natural fit failure of rule #2.1, replicated on fresh permuted boards.

Implements docs/plans/2026-09-29-natural-fit-failure-replication-registration.md, rev 1.2 (the
prediction commit b5513e3); section numbers refer to it. This file is NEW: it imports the
failed-fit calibration's script (C, pinned by LF sha256) as that script imports block B's (K).
Nothing registered or hashed is edited.

S-R map (C = failed_fit_calibration.py and K = knockout_regrow_block_b.py, lines at 5d65baf):
  S-R1  board_y_seeded: C.perm_ref_y (C:366-369) with the seed as an argument.
  S-R2  assert_seeds_rep: C.assert_seeds_cal's form (C:267-290), C literals (C:95-102),
        C.b_own_seeds (C:260-264), K.reserved_seeds (K:1031-1041). assert_patterns_fresh:
        C.world_block_y (C:324-325), C.perm_ref_y, K.permute_block (K:1143-1151).
  S-R3  cert_fresh: C.cert_search (C:393-431) under C.swapped_globals (C:439-448) of C's own
        SEED_CERT_* (C:91-93), entered in the worker; dedupe of C.cert_patterns (C:617-628).
  S-R4  fit_task -> C.fit_task (C:636-645) -> C.separator_fits (C:541-562),
        C.bf_block_lambda1 (C:565-578), K._fit_one (K:1239-1265); C.constructed_bank
        (C:353-363); run_pool is C.run_groups' pattern (C:669-691), workers via C._cw_init.
  S-R5  read_board: C.auc_counts (C:209-225), C.split_at_cut (C:228-232), C.separator_reading
        (C:746-763), C.read_world's field set (C:853-873).
  S-R6  the script-defect stop of C.read_world (C:895-900).
  S-R8  C.csv_text (C:979-984), C.v (C:955-956), C.write_stop_record (C:1085-1091),
        K.write_text_synced, K.dump_json, K.write_raw, K.write_sha256sums.
  S-R9  gate_refusals: C.gate_refusals' form (C:1104-1153), K.out_dir_refusal (K:2987-3019).
  S-R10 estimate: C.estimate's form (C:1159-1207), on a SEEN board only; --dry-run (C:1265-1273).

Run from the repository root, with PYTHONUTF8=1:
    tools/.venv/Scripts/python.exe results/genome/c6/checks/natural_fit_failure_replication.py --dry-run
    tools/.venv/Scripts/python.exe results/genome/c6/checks/natural_fit_failure_replication.py --estimate --workers 30
    tools/.venv/Scripts/python.exe results/genome/c6/checks/natural_fit_failure_replication.py --out <new folder> --workers 30
--fixture replaces the fresh boards by the calibration's SEEN boards (93200 + j), so that no fresh
board is fitted outside the registered run.
"""
import sys

import argparse
import contextlib
import hashlib
import os
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import failed_fit_calibration as C  # noqa: E402  (imports K, which sets UTF-8 streams)

K = C.K
H = C.H
ROOT = C.ROOT

REGISTRATION = "docs/plans/2026-09-29-natural-fit-failure-replication-registration.md"
REGISTRATION_REVISION = "1.2"
REGISTRATION_SHA256_LF_PINNED = "0739ac5d1d1a7b20a93f08304e697c92033c324d111447410e8594bb6a1eb76c"  # rev 1.2; Mike's order for A: DPC Research chat 2026-09-29 11:04:22 UTC
PREDICTION_COMMIT_PINNED = "b5513e3fd50c32caf9a1a30c01f6fb4423d4fa7b"  # rev 1.1, the prediction commit
CAL_SCRIPT = "results/genome/c6/checks/failed_fit_calibration.py"
CAL_SCRIPT_SHA256_LF = "220201c229800097aed62afba242a7e3593d9f7205274fc015207ab795d3af43"
B_SCRIPT = C.B_SCRIPT
B_SCRIPT_SHA256_LF = C.B_SCRIPT_SHA256_LF
CAL_OUT = HERE / "failed_fit_calibration"

N_BOARDS = 300
SEED_BOARD = 94000
SEED_CERT_STAGE1 = 94500
SEED_CERT_REFINE = tuple(range(94501, 94506))
SEED_CERT_DEEP = (94506, 94507)
LITERAL_BOARD_SEEDS = set(range(94000, 94300))
LITERAL_CERT_SEEDS = set(range(94500, 94508))
OTHER_FIXED_SEEDS = {12345}
B_DECLARED_RANGE = set(range(K.SEED_RANGE[0], K.SEED_RANGE[1] + 1))
MALE_DECLARED_RANGE = set(range(92000, 93000))

CUT = K.GATE_CUT
CUT_FR = Fraction(9, 10)
STARTS_100 = C.STARTS_100

P1_BAND = (Fraction(2, 5), Fraction(3, 5))
P2B_DECISION_MAX = 10
P2B_TEST_CUT = 16
P3_BAND = (Fraction(1, 2), Fraction(2))
P4P_MIN_SHARE = Fraction(9, 10)
P5_I_MIN = Fraction(9, 10)
P5_II_MIN = Fraction(19, 20)
RATE_FLOOR = Fraction(1, 10)
AT_CUT_BAND = (0.90, 0.91)

CAL_PER_BOARD_CPU_S = 30.0
CAL_CERT_CPU_S = 26.5

NOT_REGISTERED_TEXT = "NOT THE REGISTERED RUN"
STOP_RECORD_NAME = C.STOP_RECORD_NAME
FLAG_NAMES = ("GATE_ULP_SPLIT", "CEIL_1_ULP_SPLIT", "CERT_ULP_SPLIT", "DECODER_SPLIT_AT_LC",
              "CERT_BELOW_CUT", "CERT_COUNTS_DISAGREE")
NOT_SEPARATED_PREFIX = "not separated"
J89_ROW = "fit failure, FF-struct or FF-opt, not separated"


# ------------------------------------------------------------------------------------------
# S-R1: the boards.

def board_y_seeded(seed):
    perm = np.random.default_rng(seed).permutation(K.N_BLOCK)
    return K.board_y("z")[perm]


def fresh_y(j):
    return board_y_seeded(SEED_BOARD + j)


def board_keys(n, fixture):
    return [f"{'seen' if fixture else 'fresh'}:{j}" for j in range(n)]


def key_j(key):
    return int(key.split(":")[1])


def board_seed(key):
    return (SEED_BOARD if key.startswith("fresh:") else C.SEED_PERM_REF) + key_j(key)


def pattern_of(key):
    kind = key.split(":")[0]
    if kind == "fresh":
        return fresh_y(key_j(key))
    if kind == "seen":
        return C.perm_ref_y(key_j(key))
    raise KeyError(key)


def build_bank_rep(key):
    return C.constructed_bank(pattern_of(key), f"rep.{key.replace(':', '.')}")


# ------------------------------------------------------------------------------------------
# S-R2: seed and pattern asserts (section 3).

def cert_seeds():
    return [SEED_CERT_STAGE1, *SEED_CERT_REFINE, *SEED_CERT_DEEP]


def assert_seeds_rep(n, starts):
    boards = {SEED_BOARD + j for j in range(n)}
    certs = set(cert_seeds())
    lits = (LITERAL_BOARD_SEEDS, LITERAL_CERT_SEEDS)
    new = set().union(*lits) | boards | certs
    cal_literals = (C.LITERAL_WORLD_SEEDS | C.LITERAL_PERM_REF_SEEDS | C.LITERAL_CERT_SEEDS
                    | C.LITERAL_UNUSED_FAMILY_SEEDS)
    cal_code = ({w["seed"] for w in C.world_specs_cal()} | set(C.perm_ref_seeds())
                | set(C.cert_seeds()))
    checks = {
        "boards_within_literal": boards <= LITERAL_BOARD_SEEDS,
        "boards_equal_literal_at_N": n != N_BOARDS or boards == LITERAL_BOARD_SEEDS,
        "cert_equal_literal": certs == LITERAL_CERT_SEEDS,
        "literals_pairwise_disjoint": sum(len(x) for x in lits) == len(set().union(*lits)),
        "disjoint_from_reserved": not (new & K.reserved_seeds(max(starts, STARTS_100))),
        "disjoint_from_B_own": not (new & C.b_own_seeds()),
        "disjoint_from_B_range": not (new & B_DECLARED_RANGE),
        "disjoint_from_male_range": not (new & MALE_DECLARED_RANGE),
        "disjoint_from_calibration_literals": not (new & cal_literals),
        "disjoint_from_calibration_code_seeds": not (new & cal_code),
        "disjoint_from_design_seeds": not (new & C.DESIGN_SEEDS),
        "disjoint_from_other_fixed_seeds": not (new & OTHER_FIXED_SEEDS),
        "counts": len(LITERAL_BOARD_SEEDS) == N_BOARDS and len(LITERAL_CERT_SEEDS) == 8}
    return {"checks": checks, "passed": all(checks.values()),
            "ranges": f"boards {SEED_BOARD}-{SEED_BOARD + n - 1}; cert 94500-94507"}


def seen_patterns():
    """Board z, z', the calibration's world boards and 99 permuted boards, and block B's 20
    permuted-ceiling boards."""
    seen = {}
    seen.setdefault(K.board_y("z").tobytes(), "board z")
    seen.setdefault(K.board_y("z'").tobytes(), "board z'")
    for w in C.world_specs_cal():
        seen.setdefault(C.world_block_y(w).tobytes(), f"cal:{w['family']}:{w['j']}")
    for j in range(C.N_PERM_REF):
        seen.setdefault(C.perm_ref_y(j).tobytes(), f"perm:{j}")
    zb = C.constructed_bank(K.board_y("z"), "z")
    for j in range(K.N_PERM_CEILINGS):
        pb = K.permute_block(zb, K.perm_ceiling_perm(j), f"z.pc{j}")
        seen.setdefault(pb.exists[K.BLOCK_CELLS[:, 0], K.BLOCK_CELLS[:, 1]].tobytes(),
                        f"B permuted ceiling {j}")
    return seen


def assert_patterns_fresh(n):
    """No fresh pattern equals a seen one. Fresh boards equal to one another are reported (and
    certified once), not refused."""
    seen = seen_patterns()
    hits, own = [], {}
    for j in range(n):
        y = fresh_y(j)
        assert int(y.sum()) == K.N_WORLD_BLOCK_PRESENT
        if y.tobytes() in seen:
            hits.append(f"fresh:{j} = {seen[y.tobytes()]}")
        own.setdefault(y.tobytes(), []).append(j)
    return {"passed": not hits, "collisions": hits,
            "fresh_duplicates": [x for x in own.values() if len(x) > 1],
            "n_seen_patterns": len(seen), "n_fresh": n}


# ------------------------------------------------------------------------------------------
# S-R3: cert with this file's seeds.

@contextlib.contextmanager
def fresh_cert_seeds(stage1=SEED_CERT_STAGE1, refine=SEED_CERT_REFINE, deep=SEED_CERT_DEEP):
    """C.cert_search reads its seeds from C's module globals at call time; they are swapped for
    one call and restored. Must be entered in the process that calls cert_search."""
    with C.swapped_globals(C.__dict__, SEED_CERT_STAGE1=stage1, SEED_CERT_REFINE=tuple(refine),
                           SEED_CERT_DEEP=tuple(deep)):
        yield


def cert_fresh(y, budget):
    with fresh_cert_seeds():
        return C.cert_search(y, budget)


def cert_patterns_rep(keys):
    patterns = {}
    for key in keys:
        patterns.setdefault(pattern_of(key).tobytes(), key)
    return patterns


# ------------------------------------------------------------------------------------------
# S-R4: the fits (workers).

def plan_board(key):
    """Rule #2.1's registered block fit, N1's block fit (section 10) and BF_1-4's block fits; the
    separator; BF_1-4's ceil_1 at lambda = 1."""
    return [[(key, "block", "rule"), (key, "block", "N1")]
            + [(key, "block", pk) for pk in K.BF_KEYS],
            [(key, "sep", "rule")],
            [(key, "blk1", pk) for pk in K.BF_KEYS]]


def cert_task(key):
    return cert_fresh(pattern_of(key), _RW["budget"])


def fit_task(bk, mk, pk, bank):
    return C.fit_task(bk, mk, pk, bank)


_RW = {}


def _rw_init(starts, budget):
    C._cw_init(starts, None, budget)
    _RW.update(budget=budget, key=None, bank=None)


def _rw_group(group):
    key = group[0][0]
    if all(mk == "cert" for _, mk, _ in group):
        return [((bk, mk, pk), cert_task(bk)) for bk, mk, pk in group]
    if _RW["key"] != key:
        _RW["bank"], _RW["key"] = build_bank_rep(key), key
    out = []
    for bk, mk, pk in group:
        assert bk == key
        out.append(((bk, mk, pk), fit_task(bk, mk, pk, _RW["bank"])))
    return out


def run_pool(groups, workers, init_args, what):
    t0 = time.time()
    K.log(f"[{what}] {len(groups)} groups, {sum(len(g) for g in groups)} tasks, workers = {workers}")
    res = {}
    if workers <= 1:
        _rw_init(*init_args)
        for g in groups:
            res.update(dict(_rw_group(g)))
    else:
        with ProcessPoolExecutor(max_workers=workers, initializer=_rw_init,
                                 initargs=init_args) as ex:
            futs = [ex.submit(_rw_group, g) for g in groups]
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
# S-R5, S-R6: one board's reading.

def cert_ok(cert):
    """The exact Fraction against 9/10. C.separator_reading takes the float (cert['exact']) and
    compares it with the float cut; the two routes are asserted to agree. (Passing the Fraction
    itself would misread 9/10, since Fraction(9, 10) < 0.9 as a float.)"""
    ok = Fraction(cert["fraction"]) >= CUT_FR
    assert ok == C.ge(cert["exact"]), (cert["fraction"], cert["exact"])
    return ok


def bf_reading(r, cb, c1):
    if C.ge(cb):
        return "gate passed"
    if C.ge(c1):
        return "BF fit failure, selection"
    if r == 4:
        return "BF fit failure, not selection"
    return "BF: not separated"


def flags_of(cb, c1, cert, clcf):
    flags = []
    if C.split_at_cut(cb):
        flags.append("GATE_ULP_SPLIT")
    if C.split_at_cut(c1):
        flags.append("CEIL_1_ULP_SPLIT")
    if (cert["exact"] >= CUT) != (cert["tau"] >= CUT):
        flags.append("CERT_ULP_SPLIT")
    if C.ge(clcf["exact"]) != C.ge(cb["exact"]):
        flags.append("DECODER_SPLIT_AT_LC")
    if not cert_ok(cert):
        flags.append("CERT_BELOW_CUT")
    if not cert["counts_agree"]:
        flags.append("CERT_COUNTS_DISAGREE")
    return flags


CERT_FIELDS = ("exact", "fraction", "tau", "counts_agree", "ulp_sensitive", "rerun_spread",
               "n_pairs", "count_search", "count_fraction", "count_registered_auc")


def read_board(key, F, certs):
    y = np.asarray(pattern_of(key), bool)
    blk, sp = F[(key, "block", "rule")], F[(key, "sep", "rule")]
    assert np.array_equal(np.asarray(sp["y"], bool), y)
    assert np.array_equal(np.asarray(blk["y"], bool), y)
    cert = {k: certs[y.tobytes()][k] for k in CERT_FIELDS}
    cb = C.auc_counts(blk["p"], y)
    b = {"key": key, "j": key_j(key), "seed": board_seed(key), "present": int(y.sum()),
         "cert": cert, "cert_ok": cert_ok(cert),
         "ceiling_block": cb, "lambda_block": float(blk["lam"]), "lambda_c": float(sp["lambda_c"]),
         "ceil_1": C.auc_counts(sp["ceil1_p"], y),
         "ceil_1_float": C.auc_counts(sp["ceil1_float_p"], y),
         "ceil_lambda_c_float": C.auc_counts(sp["reg_float_p"], y),
         "ceil_1_starts100": C.auc_counts(sp["ceil1_s100_float_p"], y),
         "ceil_1_starts100_quantised": C.auc_counts(sp["ceil1_s100_p"], y),
         "n1_block": C.auc_counts(F[(key, "block", "N1")]["p"], y),
         "block_fit_reproduced": ([float(x) for x in sp["reg_p"]] == [float(x) for x in blk["p"]]
                                  and float(sp["lambda_c"]) == float(blk["lam"]))}
    b["reading"], b["subkinds"] = C.separator_reading(
        cb["exact"], cert["exact"], b["ceil_1"]["exact"], b["ceil_1_float"]["exact"],
        b["ceil_lambda_c_float"]["exact"], b["ceil_1_starts100"]["exact"])
    b["bf"] = {}
    for pk in K.BF_KEYS:
        bcb = C.auc_counts(F[(key, "block", pk)]["p"], y)
        bc1 = C.auc_counts(F[(key, "blk1", pk)]["p"], y)
        b["bf"][pk] = {"ceiling_block": bcb, "lambda_block": F[(key, "block", pk)]["lam"],
                       "ceil_1": bc1,
                       "reading": bf_reading(int(pk.split(":")[1]), bcb["exact"], bc1["exact"])}
    b["flags"] = flags_of(cb, b["ceil_1"], cert, b["ceil_lambda_c_float"])
    b["stops"] = []
    if not b["block_fit_reproduced"]:
        b["stops"].append(f"{key}: SCRIPT DEFECT: the separator's refit of the registered "
                          "block-only fit differs from it (S-R6)")
    return b


# ------------------------------------------------------------------------------------------
# S-R7: predictions (section 6), labels (section 7), J89, (iii).

def is_fail(b):
    return not C.ge(b["ceiling_block"]["exact"])


def status(x):
    return "n/a" if x is None else ("hold" if x else "fail")


def _share(k, n):
    return None if n == 0 else Fraction(k, n)


def evaluate_predictions(boards):
    """P1, P2a (design check), P2b, P3, P4', P5 over the certified boards. P4 is withdrawn and
    not evaluated; its count (passes with lambda_c != 1) is printed as part of P4'."""
    cb = [b for b in boards if b["cert_ok"]]
    nc = len(cb)
    fails = [b for b in cb if is_fail(b)]
    passes = [b for b in cb if not is_fail(b)]
    rate = _share(len(fails), nc)
    P = {"N": len(boards), "N_c": nc, "failures": len(fails), "passes": len(passes),
         "rate": None if rate is None else str(rate)}
    P["P1"] = {"holds": None if rate is None else P1_BAND[0] <= rate <= P1_BAND[1],
               "text": f"failures / N_c = {len(fails)} / {nc}, in [0.40, 0.60]"}
    ns = [b["key"] for b in fails if b["reading"].startswith(NOT_SEPARATED_PREFIX)]
    nfit = [b["key"] for b in fails if not b["reading"].startswith("fit failure")]
    P["P2a"] = {"holds": not ns and not nfit, "design_check": True,
                "text": "every certified failure reads a fit-failure row",
                "not_separated": ns, "not_fit_row": nfit}
    nonsel = [b for b in fails if "FF-sel" not in b["subkinds"]]
    P["P2b"] = {"holds": len(nonsel) <= P2B_DECISION_MAX, "count": len(nonsel),
                "test_5pct": {"cut": P2B_TEST_CUT, "rejects": len(nonsel) >= P2B_TEST_CUT,
                              "decides": False},
                "text": f"failures not FF-sel = {len(nonsel)}; decision line <= "
                        f"{P2B_DECISION_MAX} of 300",
                "keys": [b["key"] for b in nonsel]}
    p3 = {}
    for pk in K.BF_KEYS:
        bff = [b for b in cb if not C.ge(b["bf"][pk]["ceiling_block"]["exact"])]
        brate = _share(len(bff), nc)
        both = sum(1 for b in bff if is_fail(b))
        p3[pk] = {"holds": None if rate is None else P3_BAND[0] * rate <= brate <= P3_BAND[1] * rate,
                  "count": len(bff), "rate": None if brate is None else str(brate),
                  "ratio": None if not rate else float(brate / rate),
                  "table_2x2": {"rule_fail_bf_fail": both, "rule_fail_bf_pass": len(fails) - both,
                                "rule_pass_bf_fail": len(bff) - both,
                                "rule_pass_bf_pass": len(passes) - (len(bff) - both)}}
    P["P3"] = {"holds": None if rate is None else all(x["holds"] for x in p3.values()),
               "per_r": p3, "text": "each BF_r collapse rate within 0.5x-2x of the rule's"}
    l1 = [b for b in passes if b["lambda_block"] == 1.0]
    s4 = _share(len(l1), len(passes))
    P["P4p"] = {"holds": None if s4 is None else s4 >= P4P_MIN_SHARE,
                "passes_lambda_1": len(l1), "passes_lambda_not_1": len(passes) - len(l1),
                "text": f"passes with lambda_c = 1: {len(l1)} of {len(passes)} (>= 0.90); "
                        f"passes with lambda_c != 1 (the withdrawn P4's count, not evaluated): "
                        f"{len(passes) - len(l1)}"}
    l100 = [b for b in cb if b["lambda_block"] == 100.0]
    f100 = [b for b in l100 if is_fail(b)]
    ffsel100 = [b for b in l100 if "FF-sel" in b["subkinds"]]
    fl100 = [b for b in fails if b["lambda_block"] == 100.0]
    si, sii = _share(len(f100), len(l100)), _share(len(fl100), len(fails))
    pi = None if si is None else si >= P5_I_MIN
    pii = None if sii is None else sii >= P5_II_MIN
    P["P5"] = {"holds": None if pi is None or pii is None else (pi and pii),
               "i": {"holds": pi, "text": f"failures among lambda_c = 100: {len(f100)} of "
                                          f"{len(l100)} (>= 0.90)"},
               "ii": {"holds": pii, "text": f"lambda_c = 100 among failures: {len(fl100)} of "
                                            f"{len(fails)} (>= 0.95)"},
               "ff_sel_count": len(ffsel100),
               "text": f"FF-sel among lambda_c = 100: {len(ffsel100)} of {len(l100)}"}
    P["at_cut_ceil_1"] = sum(1 for b in fails
                             if AT_CUT_BAND[0] <= b["ceil_1"]["exact"] < AT_CUT_BAND[1])
    return P


def outcome_labels(boards, P, stops):
    """RP1-RP6 as a list of those that hold; RP6 alone when a stop fired (nothing is read)."""
    if stops:
        return ["RP6"]
    h = {k: bool(P[k]["holds"]) for k in ("P1", "P2a", "P2b")}
    rate = None if P["N_c"] == 0 else Fraction(P["failures"], P["N_c"])
    labels = []
    if h["P1"] and h["P2a"] and h["P2b"]:
        labels.append("RP1")
    if h["P2a"] and h["P2b"] and not h["P1"] and rate is not None and rate >= RATE_FLOOR:
        labels.append("RP2")
    if h["P2a"] and not h["P2b"]:
        labels.append("RP3")
    if rate is not None and rate < RATE_FLOOR:
        labels.append("RP4")
    if (any(not b["cert_ok"] for b in boards)
            or any(is_fail(b) and b["reading"].startswith(NOT_SEPARATED_PREFIX) for b in boards)):
        labels.append("RP5")
    return labels


OUTCOME_TEXT = {"RP1": "replicated", "RP2": "collapse replicated, rate shifted",
                "RP3": "kind not replicated", "RP4": "not replicated",
                "RP5": "class-side finding", "RP6": "stop"}


def j89_outcome(boards):
    """J89-reproduced iff a certified failure reads j = 89's own row; FF-opt named and FF-quant
    at lambda = 1 are counted apart and do not reproduce it."""
    fails = [b for b in boards if b["cert_ok"] and is_fail(b)]
    same = [b["key"] for b in fails if b["reading"] == J89_ROW]
    opt = [b["key"] for b in fails if b["subkinds"] == ["FF-opt"]]
    q = [b["key"] for b in fails if b["subkinds"] == ["FF-quant"]]
    return {"label": "J89-reproduced" if same else "J89-not-reproduced",
            "same_row_as_j89": same, "ff_opt_named": opt, "ff_quant_at_lambda_1": q,
            "note": "residual rows, named as such (CAL section 7)"}


def population_iii(boards):
    def row(b):
        cb, n1 = b["ceiling_block"], b["n1_block"]
        return {"key": b["key"], "j": b["j"], "seed": b["seed"], "lambda_c": b["lambda_block"],
                "ceiling_block": cb["exact"], "ceiling_block_tau": cb["tau"],
                "ceil_1": b["ceil_1"]["exact"], "ceil_1_tau": b["ceil_1"]["tau"],
                "n1_block": n1["exact"], "n1_block_tau": n1["tau"],
                "gap": cb["exact"] - n1["exact"], "gap_tau": cb["tau"] - n1["tau"]}
    passes = [b for b in boards if b["cert_ok"] and not is_fail(b)]
    return {"lambda_1": [row(b) for b in passes if b["lambda_block"] == 1.0],
            "lambda_100": [row(b) for b in passes if b["lambda_block"] == 100.0],
            "lambda_other": [row(b) for b in passes if b["lambda_block"] not in (1.0, 100.0)]}


# ------------------------------------------------------------------------------------------
# S-R8: outputs.

v = C.v
AUC_OBJECTS = ("ceiling_block", "ceil_1", "ceil_1_float", "ceil_lambda_c_float", "ceil_1_starts100",
               "ceil_1_starts100_quantised", "n1_block")
BOARDS_HEADER = (("j", "seed", "key", "present", "cert", "cert_fraction", "cert_tau",
                  "cert_ulp_sensitive", "cert_counts_agree", "cert_rerun_spread", "cert_ok",
                  "lambda_block", "lambda_c")
                 + tuple(f"{o}{s}" for o in AUC_OBJECTS for s in ("", "_tau", "_ulp_sensitive"))
                 + ("separator_reading", "subkinds", "flags")
                 + tuple(f"bf{r}_{c}" for r in K.RANKS
                         for c in ("lambda_block", "ceiling_block", "ceiling_block_tau",
                                   "ceiling_block_ulp_sensitive", "ceil_1", "ceil_1_tau",
                                   "ceil_1_ulp_sensitive", "reading"))
                 + ("stops",))
POP_HEADER = ("key", "j", "seed", "lambda_c", "ceiling_block", "ceiling_block_tau", "ceil_1",
              "ceil_1_tau", "n1_block", "n1_block_tau", "gap", "gap_tau")
assert all(c.isascii() for c in BOARDS_HEADER + POP_HEADER)
assert len(set(BOARDS_HEADER)) == len(BOARDS_HEADER)


def boards_rows(boards):
    out = []
    for b in boards:
        c = b["cert"]
        row = [b["j"], b["seed"], b["key"], b["present"], v(c["exact"]), c["fraction"], v(c["tau"]),
               c["ulp_sensitive"], c["counts_agree"], v(c["rerun_spread"]), b["cert_ok"],
               v(b["lambda_block"]), v(b["lambda_c"])]
        for o in AUC_OBJECTS:
            row += [v(b[o]["exact"]), v(b[o]["tau"]), b[o]["ulp_sensitive"]]
        row += [b["reading"], ";".join(b["subkinds"]), ";".join(b["flags"])]
        for pk in K.BF_KEYS:
            f = b["bf"][pk]
            row += [v(f["lambda_block"]), v(f["ceiling_block"]["exact"]),
                    v(f["ceiling_block"]["tau"]), f["ceiling_block"]["ulp_sensitive"],
                    v(f["ceil_1"]["exact"]), v(f["ceil_1"]["tau"]), f["ceil_1"]["ulp_sensitive"],
                    f["reading"]]
        row.append(" | ".join(b["stops"]))
        out.append(row)
    return out


def prediction_lines(P):
    t = P["P2b"]["test_5pct"]
    return [
        f"P1: {status(P['P1']['holds'])} ({P['P1']['text']})",
        f"P2a (a design check, not a prediction): {status(P['P2a']['holds'])} "
        f"({P['P2a']['text']})",
        f"P2b: {status(P['P2b']['holds'])} ({P['P2b']['text']}); beside it, deciding nothing: "
        f"one-sided 5 % test of rate <= 1/30 (cut >= {t['cut']}) "
        f"{'rejects' if t['rejects'] else 'does not reject'}",
        f"P3: {status(P['P3']['holds'])} ({P['P3']['text']}; rule {P['failures']} of "
        f"{P['N_c']}; " + "; ".join(f"{K.PRED_NAME[pk]} {x['count']} of {P['N_c']} "
                                    f"{status(x['holds'])}"
                                    for pk, x in P["P3"]["per_r"].items()) + ")",
        f"P4': {status(P['P4p']['holds'])} ({P['P4p']['text']})",
        f"P5 (a label, not independent evidence): {status(P['P5']['holds'])} "
        f"((i) {status(P['P5']['i']['holds'])}: {P['P5']['i']['text']}; "
        f"(ii) {status(P['P5']['ii']['holds'])}: {P['P5']['ii']['text']}); "
        f"beside it: {P['P5']['text']}"]


def pop_table(rows):
    L = ["| " + " | ".join(POP_HEADER) + " |", "|" + "---|" * len(POP_HEADER)]
    for r in rows:
        L.append("| " + " | ".join(v(r[c]) if isinstance(r[c], float) else str(r[c])
                                   for c in POP_HEADER) + " |")
    return L


def report_md(result):
    m, P, j = result["manifest"], result["predictions"], result["j89"]
    L = ["# Natural fit-failure replication", "",
         f"Registration `{REGISTRATION}`, revision {REGISTRATION_REVISION}. "
         f"git_head={m['git_head']}. Prediction commit {m['prediction_commit_pinned']}.", ""]
    if m["not_registered"]:
        L += [f"**{m['not_registered']}**", ""]
    L += ["## Outcome (section 7)", ""]
    L += [f"- **{c}**: {OUTCOME_TEXT[c]}" for c in result["labels"]] or ["- (none of RP1-RP6)"]
    L += ["", f"Secondary: **{j['label']}** (same row as j = 89: {len(j['same_row_as_j89'])}; "
          f"FF-opt named: {len(j['ff_opt_named'])}; FF-quant at lambda = 1: "
          f"{len(j['ff_quant_at_lambda_1'])}; residuals).", "",
          "## Predictions (section 6; hold / fail)", ""]
    L += [f"- {x}" for x in prediction_lines(P)]
    L += ["", f"Failures with ceil_1 in [0.90, 0.91): {P['at_cut_ceil_1']}. "
          + ". ".join(f"{n} rows: {result['flag_counts'][n]}" for n in FLAG_NAMES) + ".", "",
          "P3, rule failure x BF_r failure (certified boards):", "",
          "| BF_r | both fail | rule only | BF only | both pass |", "|---|---|---|---|---|"]
    for pk, x in P["P3"]["per_r"].items():
        t = x["table_2x2"]
        L.append(f"| {K.PRED_NAME[pk]} | {t['rule_fail_bf_fail']} | {t['rule_fail_bf_pass']} | "
                 f"{t['rule_pass_bf_fail']} | {t['rule_pass_bf_pass']} |")
    if result["stops"]:
        L += ["", "## Stops", ""] + [f"- {s}" for s in result["stops"]]
    L += ["", "## Boards (every AUC object exact (tau))", "",
          "| board | seed | cert | ceiling_block | lambda_c | ceil_1 | ceil_1_float | "
          "ceil_lambda_c_float | ceil_1_starts100 | ceil_1_starts100_quantised | reads | "
          "BF_1-4 rows | flags |", "|" + "---|" * 13]
    for b in result["boards"]:
        def pr(o):
            return f"{v(b[o]['exact'], 4)} ({v(b[o]['tau'], 4)})"
        L.append(f"| {b['key']} | {b['seed']} | {b['cert']['fraction']} | {pr('ceiling_block')} | "
                 f"{v(b['lambda_c'], 0)} | {pr('ceil_1')} | {pr('ceil_1_float')} | "
                 f"{pr('ceil_lambda_c_float')} | {pr('ceil_1_starts100')} | "
                 f"{pr('ceil_1_starts100_quantised')} | {b['reading']} | "
                 + "; ".join(b["bf"][pk]["reading"] for pk in K.BF_KEYS)
                 + f" | {', '.join(b['flags']) or '-'} |")
    pop = result["population_iii"]
    L += ["", "## (iii): passes at lambda = 1 (section 10; printed, decides nothing)", ""]
    L += pop_table(pop["lambda_1"])
    L += ["", "## Passes at lambda = 100 (separate)", ""] + pop_table(pop["lambda_100"])
    if pop["lambda_other"]:
        L += ["", "## Passes at another lambda", ""] + pop_table(pop["lambda_other"])
    return "\n".join(L) + "\n"


def write_outputs(folder, result, F, certs):
    folder = Path(folder)
    K.write_text_synced(folder / "replication.json", K.dump_json(result) + "\n")
    K.write_text_synced(folder / "boards.csv",
                        C.csv_text(BOARDS_HEADER, boards_rows(result["boards"])))
    K.write_text_synced(folder / "cert_members.json", K.dump_json(
        {hashlib.sha256(k).hexdigest()[:16]: {**c, "y": np.frombuffer(k, bool).astype(int)
                                              .tolist()} for k, c in certs.items()}) + "\n")
    K.write_raw(F, folder / "raw_fits.json.gz")
    K.write_text_synced(folder / "REPLICATION.md", report_md(result))


# ------------------------------------------------------------------------------------------
# S-R9: refusals before any folder.

def registered_form(a):
    return (not a.fixture and a.n == N_BOARDS and a.cert_budget == "registered"
            and a.starts == 10)


def git_is_ancestor(commit):
    r = subprocess.run(["git", "merge-base", "--is-ancestor", commit, "HEAD"], cwd=ROOT,
                       capture_output=True, text=True)
    if r.returncode == 0:
        return True, ""
    if r.returncode == 1:
        return False, f"{commit} is not an ancestor of HEAD"
    return False, f"git merge-base failed for {commit!r}: {r.stderr.strip()}"


def prediction_commit_refusal(pinned):
    if pinned is None:
        return "REFUSED: the prediction commit is not pinned (PREDICTION_COMMIT_PINNED is None)"
    ok, why = git_is_ancestor(pinned)
    return None if ok else f"REFUSED: prediction commit: {why}"


def cwd_refusal():
    cwd = Path(os.getcwd()).resolve()
    if cwd != Path(ROOT).resolve():
        return f"REFUSED: run from the repository root {ROOT}, not {cwd} (S-R9)"
    return None


def out_refusal(out):
    r = K.out_dir_refusal(out)
    if r:
        return r
    target, ref = Path(out).resolve(), Path(CAL_OUT).resolve()
    if target == ref or target.is_relative_to(ref):
        return (f"REFUSED: --out {target} is the calibration's reference folder or inside it "
                f"({ref}); write to a new folder")
    if Path(out).exists():
        return f"REFUSED: --out {out} exists; the run writes into a new folder"
    return None


def gate_refusals(a):
    r = cwd_refusal()
    if r:
        sys.exit(r)
    out = {"pins": K.check_pins(), "block_and_mask": K.check_block_and_mask(),
           "auc_function": K.check_auc_function()}
    for key, path, pin in (("b_script_sha256_lf", B_SCRIPT, B_SCRIPT_SHA256_LF),
                           ("cal_script_sha256_lf", CAL_SCRIPT, CAL_SCRIPT_SHA256_LF)):
        now = K.sha256_lf(ROOT / path)
        if now != pin:
            sys.exit(f"REFUSED: {path} has LF sha256 {now}, pinned {pin}")
        out[key] = now
    sv = C.check_survey_copy()
    if not sv["passed"]:
        sys.exit(f"REFUSED: the copied survey search does not match: {sv}")
    out["survey_copy"] = sv
    seeds = assert_seeds_rep(a.n, a.starts)
    if not seeds["passed"]:
        sys.exit(f"SEEDS NOT UNIQUE (section 3; RP6): {seeds['checks']}")
    out["seeds"] = seeds
    pats = assert_patterns_fresh(a.n)
    if not pats["passed"]:
        sys.exit(f"FRESH PATTERN EQUALS A SEEN ONE (section 3; RP6): {pats['collisions']}")
    out["patterns"] = pats
    if a.out is not None:
        r = out_refusal(a.out)
        if r:
            sys.exit(r)
    reg_now = K.sha256_lf(ROOT / REGISTRATION)
    out["registration_sha256_lf"] = reg_now
    dirty = K.tree_state()
    out["dirty"] = dirty
    refusals = []
    if registered_form(a):
        if REGISTRATION_SHA256_LF_PINNED is None:
            refusals.append("REFUSED: the registration is not pinned (REGISTRATION_SHA256_LF_PINNED "
                            "is None)")
        elif reg_now != REGISTRATION_SHA256_LF_PINNED:
            refusals.append(f"REFUSED: {REGISTRATION} has LF sha256 {reg_now}, pinned "
                            f"{REGISTRATION_SHA256_LF_PINNED}")
        pc = prediction_commit_refusal(PREDICTION_COMMIT_PINNED)
        if pc:
            refusals.append(pc)
        if dirty:
            refusals.append("REFUSED: uncommitted changes under results/genome/c6/ or docs/plans/; "
                            "the replication must be tied to a commit.\n" + dirty)
    out["refusals_of_a_run"] = refusals
    if refusals and a.out is not None and not (a.dry_run or a.estimate):
        sys.exit("\n".join(refusals))
    return out


# ------------------------------------------------------------------------------------------
# S-R10: the estimate, on a seen board.

def estimate(a):
    """Times every task of plan_board on "seen:0" (the calibration's permuted board 0) and one
    cert, in this process, and scales to N_BOARDS. raw: as measured, unloaded. anchored: the
    calibration's loaded 30.0 CPU-s for sep + BF blocks, scaled by this plan's measured ratio of
    all fits to that subset, plus its 26.5 CPU-s per cert."""
    budget = C.CERT_BUDGET_REGISTERED if a.cert_budget == "registered" else C.CERT_BUDGET_TINY
    _rw_init(a.starts, budget)
    key = "seen:0"
    bank = build_bank_rep(key)
    t = {}
    for g in plan_board(key):
        for bk, mk, pk in g:
            t0 = time.time()
            fit_task(bk, mk, pk, bank)
            t[f"{mk}:{pk}"] = time.time() - t0
            K.log(f"[estimate] {mk}:{pk}: {t[f'{mk}:{pk}']:.1f}s")
    t0 = time.time()
    cert_fresh(pattern_of(key), budget)
    t["cert"] = time.time() - t0
    K.log(f"[estimate] cert ({a.cert_budget} budget): {t['cert']:.1f}s")
    fits = sum(x for k, x in t.items() if k != "cert")
    cal_subset = t["sep:rule"] + sum(t[f"block:{pk}"] for pk in K.BF_KEYS)
    raw_cpu = N_BOARDS * (fits + t["cert"])
    ratio = fits / cal_subset if cal_subset > 0 else 1.0
    anch_board = CAL_PER_BOARD_CPU_S * ratio
    anch_cpu = N_BOARDS * (anch_board + CAL_CERT_CPU_S)
    wall_raw = raw_cpu / a.workers + max(t.values())
    wall_anch = anch_cpu / a.workers
    return {"timings_s": t, "fits_per_board_s": fits, "cal_subset_s": cal_subset,
            "ratio_all_fits_to_cal_subset": ratio, "n_boards": N_BOARDS,
            "workers": a.workers, "raw_total_cpu_s": raw_cpu, "raw_wall_min": wall_raw / 60,
            "anchored_per_board_cpu_s": anch_board + CAL_CERT_CPU_S,
            "anchored_total_cpu_s": anch_cpu, "anchored_wall_min": wall_anch / 60,
            "anchored_wall_min_margin_1_5": 1.5 * wall_anch / 60,
            "over_30_min": max(wall_raw, 1.5 * wall_anch) > 1800,
            "board": key, "cert_budget": a.cert_budget}


# ------------------------------------------------------------------------------------------

def parse(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None, help="a new folder for the outputs")
    ap.add_argument("--workers", type=int, default=30)
    ap.add_argument("--starts", type=int, choices=[3, 10], default=10)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--estimate", action="store_true",
                    help="time one SEEN board's tasks and one cert; no fresh board")
    ap.add_argument("--fixture", action="store_true",
                    help="the calibration's seen boards in place of the fresh ones; NOT the "
                         "registered run")
    ap.add_argument("--smoke-n", type=int, default=None)
    ap.add_argument("--cert-budget", choices=["registered", "tiny"], default="registered")
    a = ap.parse_args(argv)
    a.n = a.smoke_n if a.smoke_n is not None else N_BOARDS
    if not 1 <= a.n <= N_BOARDS:
        ap.error(f"--smoke-n must be in 1..{N_BOARDS}")
    return a


def main(argv=None):
    a = parse(argv)
    t0 = time.time()
    K._LOG["buffer"].clear()
    K._LOG["output_errors"] = 0
    gate = gate_refusals(a)                            # before any folder
    head = K.git("rev-parse", "HEAD")
    not_registered = None
    if not registered_form(a):
        not_registered = (f"{NOT_REGISTERED_TEXT}: "
                          + ("the calibration's seen boards (fixture); " if a.fixture else "")
                          + "a smoke or non-registered form")
    if a.estimate:
        est = estimate(a)
        K.log(f"ESTIMATE ({est['board']}, cert {est['cert_budget']}): raw "
              f"{est['raw_wall_min']:.1f} min; anchored {est['anchored_wall_min']:.1f} min "
              f"({est['anchored_wall_min_margin_1_5']:.1f} with 1.5x) on {a.workers} workers for "
              f"N = {N_BOARDS}; over 30 min: {est['over_30_min']}")
        return {"estimate": est}
    keys = board_keys(a.n, a.fixture)
    if a.dry_run or a.out is None:
        n_tasks = sum(len(g) for k in keys for g in plan_board(k))
        K.log(f"DRY RUN: gate passed; {len(keys)} boards ({keys[0]} .. {keys[-1]}), "
              f"{len(cert_patterns_rep(keys))} cert patterns, {n_tasks} fit tasks; nothing "
              "fitted, nothing written; a run in this form would be refused: "
              + (" / ".join(r.splitlines()[0] for r in gate["refusals_of_a_run"]) or "no"))
        return {"dry_run": True, "gate": gate, "keys": keys}
    folder = Path(a.out)
    folder.mkdir(parents=True, exist_ok=False)
    K.tee_to(folder / "stdout.log")
    completed = False
    try:
        result = _run(a, t0, head, gate, not_registered, keys, folder)
        completed = result.get("completed", False)
    finally:
        K.untee()
    if completed:
        K.write_sha256sums(folder)                     # last, only for a completed run
    else:
        sys.exit(1)
    return result


def _run(a, t0, head, gate, not_registered, keys, folder):
    budget = C.CERT_BUDGET_REGISTERED if a.cert_budget == "registered" else C.CERT_BUDGET_TINY
    K.log(f"registration: {REGISTRATION}, revision {REGISTRATION_REVISION}; LF sha256 "
          f"{gate['registration_sha256_lf']} (pinned: {REGISTRATION_SHA256_LF_PINNED}); "
          f"prediction commit {PREDICTION_COMMIT_PINNED}"
          + (f"; {not_registered}" if not_registered else "")
          + f"; k = {a.starts}; workers = {a.workers}; CPU")
    K.log(f"checks passed: pins, block and mask, AUC function, B script "
          f"{gate['b_script_sha256_lf'][:12]}, CAL script {gate['cal_script_sha256_lf'][:12]}, "
          f"survey copy, seeds ({gate['seeds']['ranges']}), patterns (none of "
          f"{gate['patterns']['n_fresh']} fresh equals any of "
          f"{gate['patterns']['n_seen_patterns']} seen)")
    patterns = cert_patterns_rep(keys)
    init_args = (a.starts, budget)
    res = run_pool([[(key, "cert", "cert")] for key in patterns.values()], a.workers, init_args,
                   "cert (before any fit; seeds 94500-94507)")
    certs = {yk: res[(key, "cert", "cert")] for yk, key in patterns.items()}
    disagree = [f"{key}: counts {certs[yk]['count_search']}, {certs[yk]['count_fraction']}, "
            f"{certs[yk]['count_registered_auc']}" for yk, key in patterns.items()
            if not certs[yk]["counts_agree"]]
    manifest = {"registration": REGISTRATION, "revision": REGISTRATION_REVISION,
                "registration_sha256_lf": gate["registration_sha256_lf"],
                "registration_pinned": REGISTRATION_SHA256_LF_PINNED,
                "prediction_commit_pinned": PREDICTION_COMMIT_PINNED,
                "script_sha256_lf": K.sha256_lf(Path(__file__)),
                "cal_script_sha256_lf": gate["cal_script_sha256_lf"],
                "b_script_sha256_lf": gate["b_script_sha256_lf"], "git_head": head,
                "tree_dirty_paths": gate["dirty"].splitlines() if gate["dirty"] else [],
                "not_registered": not_registered, "fixture": a.fixture,
                "boards": f"{keys[0]} .. {keys[-1]}", "n": a.n, "starts": a.starts,
                "workers": a.workers, "cert_budget": budget, "cert_seeds": cert_seeds(),
                "device": "CPU", "seeds": gate["seeds"], "patterns": gate["patterns"],
                "survey_copy": gate["survey_copy"],
                "command_environment": K.command_environment(),
                "machine_record": K.machine_record()}
    K.log(f"cert: {len(certs)} patterns; the three counts disagree on {len(disagree)} "
          f"(flagged CERT_COUNTS_DISAGREE, not a stop; the Fraction count is the certificate)"
          + (f": {'; '.join(disagree)}" if disagree else "") + "; below 0.90 on "
          f"{sum(1 for c in certs.values() if Fraction(c['fraction']) < CUT_FR)}")
    F = run_pool([g for k in keys for g in plan_board(k)], a.workers, init_args, "boards")
    boards = [read_board(k, F, certs) for k in keys]
    stops = [s for b in boards for s in b["stops"]]
    P = evaluate_predictions(boards)
    labels = outcome_labels(boards, P, stops)
    j89 = j89_outcome(boards)
    pop = population_iii(boards)
    manifest.update(runtime_s=time.time() - t0, log_output_errors=K._LOG["output_errors"])
    result = {"manifest": manifest, "labels": labels, "stops": stops, "predictions": P,
              "j89": j89, "population_iii": pop,
              "flag_counts": {n: sum(n in b["flags"] for b in boards) for n in FLAG_NAMES},
              "boards": boards}
    write_outputs(folder, result, F, certs)            # on disk before anything is printed
    for b in boards:
        c = b["cert"]
        K.log(f"{b['key']} (seed {b['seed']}): cert {c['fraction']} (tau {v(c['tau'])}); "
              f"ceiling_block {v(b['ceiling_block']['exact'])} (tau "
              f"{v(b['ceiling_block']['tau'])}) at lambda_c {v(b['lambda_block'], 0)}; ceil_1 "
              f"{v(b['ceil_1']['exact'])} (tau {v(b['ceil_1']['tau'])}); ceil_1_float "
              f"{v(b['ceil_1_float']['exact'])} (tau {v(b['ceil_1_float']['tau'])}); "
              f"ceil_lambda_c_float {v(b['ceil_lambda_c_float']['exact'])} (tau "
              f"{v(b['ceil_lambda_c_float']['tau'])}); ceil_1_starts100 "
              f"{v(b['ceil_1_starts100']['exact'])} (tau {v(b['ceil_1_starts100']['tau'])}); "
              f"quantised {v(b['ceil_1_starts100_quantised']['exact'])}; N1 "
              f"{v(b['n1_block']['exact'])}; reads: {b['reading']}; BF: "
              + "; ".join(f"{K.PRED_NAME[pk]} {v(f['ceiling_block']['exact'])} / ceil_1 "
                          f"{v(f['ceil_1']['exact'])}: {f['reading']}"
                          for pk, f in b["bf"].items())
              + f"; flags {', '.join(b['flags']) or '-'}")
    for line in prediction_lines(P):
        K.log(line)
    K.log(f"(iii) population: {len(pop['lambda_1'])} passes at lambda = 1 (printed, decides "
          f"nothing); passes at lambda = 100: {len(pop['lambda_100'])}; at another lambda: "
          f"{len(pop['lambda_other'])}")
    K.log(f"SECONDARY: {j89['label']}")
    K.log(f"OUTCOME: {', '.join(labels) or '(none)'}")
    if stops:
        msg = "STOP (RP6): " + " | ".join(stops)
        K.log(msg)
        C.write_stop_record(folder, msg, {"outcome": "RP6"})
        return {**result, "completed": False}
    K.log(f"done in {time.time() - t0:.0f}s")
    return {**result, "completed": True}


if __name__ == "__main__":
    main()
