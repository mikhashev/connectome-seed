#!/usr/bin/env python3
"""Knock out and regrow, block A on flyvis-65 (ADR-005 decision 3).

Implements docs/plans/2026-09-24-knockout-regrow-registration.md, revision 3.4; section numbers
below refer to it, and main() follows its section 7 order (refusals and pins; machine checks;
synthetic worlds and the two-world check; the real arm; the verdict and outputs).

Revision 3 (2026-09-25, after the synthetic-only run of revision 2): the requirement rows of
section 3.6 (M worlds are a power curve, no stop; Nf never R or W, at least 3 of 5 read G); G is
"not detected above gamma*", with gamma* measured on the dense grid gamma in {0.5, 0.6, 0.75,
0.85, 1.0}; the mechanism of G is a description only; degenerate shuffles are excluded from leg S;
the U rule; the fixed lambda = 1 diagnostic (decides nothing). --from-raw now merges: it re-reads
the saved fits and fits only what is missing (the new worlds and the fixed-lambda fits).

Revision 3.1 (2026-09-25, the reviewers' pass on revision 3; text and code only, nothing run):
three limits instead of one (gamma*_P, the leg-P limit; gamma_R, the R level; the family limit,
the largest leg-P limit over the predictors), printed with the per-gamma fractions seen/n and
R/n, Johnny's binomial note and the width of the transition band [gamma*_P, gamma_R), where U is
read as "on the detection threshold; cannot be separated"; the lambda each knockout fit selected
goes on the verdict line, with a G reached through lambda = 100 named there; the registered run
writes its private and raw outputs to connectome-seed-data/knockout_regrow/<run>, and it must
reproduce the pre-run synthetic table (PRERUN_DIR, synthetic_worlds.csv) or the two-world check
stops it (revision 3.1 compared it byte for byte; revision 3.2 compares the deciding columns).

Revision 3.2 (2026-09-25, the reviewers' pass on revision 3.1; text and code only, no fitting
run): the reproduction gate compares the fresh synthetic_worlds.csv with the pinned one row by
row on the deciding columns (lattice columns exactly, continuous columns within
MACHINE_CHECK_TOL; mechanism_description reported, not gated), and records byte identity as a
fact only (csv_compare, check_prerun_reproduced); the whole pre-run SHA256SUMS.txt is checked
(check_prerun_files); a per-fit diagnostic compares the fresh raw fits with the pinned ones,
split by the worlds fitted by revision 2 and by revision 3 (raw_fits_diagnostic; decides
nothing); a --from-raw pass is reported as a re-read, not a reproduction; the manifest records
the BLAS, the machine and the four thread variables as found (machine_record); label_text takes
the U reasons, and a U whose reasons include ceiling_block below the gate is printed as a failed
fit, never renamed by the U rule; one threshold on two variables is split into GATE_CUT
(ceiling_block, the G gate) and MECHANISM_CUT (ceiling_full, the description of G), both 0.90;
the mechanism text names rule #2.1's ceiling_full, which changes the text of column 8 of
synthetic_worlds.csv (mechanism_description) on the rows that carry it, and with it the bytes
of that file; "weak leg" is replaced by "leg P".

Revision 3.3 (2026-09-25, the reviewers' pass on revision 3.2; text and code only, no fitting
run): csv_compare matches rows by key (family, j, seed, predictor), reports missing rows and a
change of row order separately, splits outcome 3 into (a) identity or lattice columns and (b)
continuous columns beyond MACHINE_CHECK_TOL, and checks that the column-8 differences are exactly
revision 3.2's rename; the treatment of outcome 3 names four layers and the self-test's outcomes
(repro_fail_treatment); the null inputs are digested into the manifest (null_input_digests);
--out is refused inside the pinned reference folder, on a byte copy of it, and with --arm
(out_dir_refusal); the U rule counts threshold U only, and a failed fit and a ceiling_block that
was not measured are separate U texts; raw_fits_diagnostic compares the score fields and marks a
re-read; new raw records store sign_n; a real-arm run with --allow-dirty says on its verdict line
that it is not the registered run; the manifest records the dirty paths and the --from-raw
file's sha256; check_prerun_files reports unlisted entries of the pre-run folder.

Revision 3.4 (2026-09-25, the reviewers' pass on revision 3.3; text and code only, no fitting
run): the treatment of outcome 3 traces the leg-P null by generator, one line each (uniform_perms
-> p_P, p_P_fixed_lambda1, smallest_passing_auc; rc_patterns -> p_P_rowcol); smallest_passing_auc
is a checked scalar, registered by board (SMALLEST_PASSING_AUC_BY_BOARD) and checked for every
world before the fits (check_smallest_passing_auc), a mismatch stopping the synthetic step; the
two excluded store fields carry their labels; each run prints how many ko1 records were copied
from the ko fit and how many were fitted (a convenience count, not a control).

    tools/.venv/Scripts/python.exe results/genome/c6/checks/knockout_regrow.py --synthetic-only --starts 10 --workers 30
    tools/.venv/Scripts/python.exe results/genome/c6/checks/knockout_regrow.py --arm flyvis65 --starts 10 --workers 30

--synthetic-only never builds, fits or scores a bank that holds the real block and fits no rule on
the real bank. From the real bank it reads only what section 3.6 allows before data: N1's degree
terms fitted on the real knockout view, the content of the non-block present cells, and (for the
section 1.4 tables) presence outside the block. Machine checks 3, 5, 6, 8 and 9 run in the real
arm only. Without --out it writes nothing. --smoke-* options shrink the synthetic check for
timing; a smoke run is marked as such and is refused in the real arm. CPU only: the instrument is
the pinned numpy harness; a GPU instrument would be a separate one (section 7).
"""
import os
THREAD_VARS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")
# Revision 3.2 (A4): the values found in the environment before setdefault, which does not
# override a value already set; the manifest records them beside the values in effect.
THREAD_ENV_FOUND = {_v: os.environ.get(_v) for _v in THREAD_VARS}
for _v in THREAD_VARS:
    os.environ.setdefault(_v, "1")          # one BLAS thread per process, as the harness sets
import argparse
import csv
import gzip
import hashlib
import io
import json
import math
import platform
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
C6 = HERE.parent
ROOT = C6.parents[2]                                   # the repository root
REGISTRATION = "docs/plans/2026-09-24-knockout-regrow-registration.md"
REGISTRATION_REVISION = "3.4"
OUT = HERE / "knockout_regrow"                         # section 7: committed, aggregates only
RULE_PATH = C6 / "rules" / "second_rule_v21" / "fit.py"
# Section 7 (revision 3.1): private and raw outputs live outside the repository. The registered
# run writes them to PRIVATE_ROOT / "<arm>_<UTC stamp>_<git head, 12>" (private_run_dir).
PRIVATE_ROOT = ROOT.parent / "connectome-seed-data" / "knockout_regrow"
# The pre-run synthetic outputs (copied there on 2026-09-25; SHA256SUMS.txt beside them). They
# are mixed: the fits of 30 worlds come from the revision-2 run (families R, Nf, No, W, M0.5,
# M1.0) and those of 15 worlds from the revision-3 run (M0.6, M0.75, M0.85); the table was written
# by a revision-3 --from-raw pass over those fits. The registered run must reproduce
# synthetic_worlds.csv on its deciding columns (sections 3.3, 7; revision 3.2).
# Revision 3.3 (A2): no run writes here. out_dir_refusal refuses --out at this folder or inside
# it, and on any folder that holds a byte copy of it; the reference is recreated only in a new
# folder, and moved here with PRERUN_SHA256 in one reviewed change (section 7).
PRERUN_DIR = PRIVATE_ROOT / "synthetic_rev3_prerun"
# Revision 3.2 (Ark N3): every file listed in the pre-run SHA256SUMS.txt is checked, against both
# the list and these pins (section 7's table, raw bytes).
PRERUN_SHA256 = {
    "SYNTHETIC.md": "4526d2239c6bf378b161b7fb92bab2c022b0ac648a88fcda8fa02f86f9e58264",
    "raw_fits.json.gz": "91035af838446b86bda502fe8bf719910550bbad72c1cb12563800a984819e60",
    "rev2_full.log": "fa5606e37ebcb8e7b4aac69ba592638e3f77cfea9cbff58b639be2ee8ea960d0",
    "synthetic_only.json": "ea812dfd87238a4a23ca54e06faf5c1d93c7802a36ee28eff9857183236377dd",
    "synthetic_worlds.csv": "7a2f02953207f8aacb1cbd8c5e61e7731135d5a6f800a40b359cb0ff12f9c8f1"}
PRERUN_WORLDS_CSV_SHA256 = PRERUN_SHA256["synthetic_worlds.csv"]
# Which run fitted each pre-run world (the per-fit diagnostic of revision 3.2 splits by it).
PRERUN_REV2_FAMILIES = ("R", "Nf", "No", "W", "M0.5", "M1.0")
PRERUN_REV3_FAMILIES = ("M0.6", "M0.75", "M0.85")

# Section 1.1: files and pins (LF-normalised sha256). The script refuses if any differs.
PINS = {
    "results/genome/bank/offsets.csv":
        "8c45e8508d8f6ae45e9ab3f9d95d58e4521894ccfa51954f6d77d41e550fa5f0",
    "results/genome/bank/types.csv":
        "237a195a36f62ce182fee8486394c27d2beb9825bc029cb215c39c0fa323a477",
    "results/genome/c6/folds.csv":
        "fb6f153b67fe1785a76c3823911e6fbb91cdda57ec952b36c40b4c95f1e213b8",
    "results/genome/c6/harness.py":
        "6fc809527c69ee84aadebfc15c0ba755c189ddc93c80c05c0fa11d969a8d7297",
    "results/genome/c6/rules/second_rule_v21/fit.py":
        "92eb6ab1524bb22379b2d21184d10f493ff4c803a41918be8ee16f389a58d16c",
    "results/genome/c6/rules/second_rule_v21/decode.py":
        "39a049013af18a1e89e534d9d378a5f59a772b894d7fab5b79f82f702723a15a",
    "results/genome/c6/decoders/bf_decode.py":
        "6404210c5e78bbaaa14c6cddc6df7fc41ce958e6ff957c062cc956faad59c1de",
    "results/genome/c6/decoders/n1_decode.py":
        "e9eb00e174fa3454046f8cc92439f2132f27697d5b7467bd3f22b64a37c8db96",
}
PYTHON_VERSION, NUMPY_VERSION = "3.10.20", "2.2.6"      # section 7


def sha256_lf(p):
    return hashlib.sha256(Path(p).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


# Section 1.1: the pins are read before the harness is imported, and checked in step 1.
PINS_READ = {f: sha256_lf(ROOT / f) for f in PINS}
sys.path.insert(0, str(C6))
import harness as H  # noqa: E402

# ------------------------------------------------------------------------------------------
# Section 1.2: the block. The ON/OFF and T4/T5 splits are the answer key: used only to score and
# to print strata, never to train. Block cell order: SOURCES x TARGETS, row-major; leg P's
# permutations index this order.
ON, OFF = ("Mi1", "Tm3", "Mi4", "Mi9"), ("Tm1", "Tm2", "Tm4", "Tm9")
T4, T5 = ("T4a", "T4b", "T4c", "T4d"), ("T5a", "T5b", "T5c", "T5d")
SOURCES, TARGETS = ON + OFF, T4 + T5
BLOCK_NAMES = [(s, t) for s in SOURCES for t in TARGETS]
BLOCK_CELLS = np.array([(H.IDX[s], H.IDX[t]) for s, t in BLOCK_NAMES], dtype=np.int64)
BLOCK = np.zeros((65, 65), bool)
BLOCK[BLOCK_CELLS[:, 0], BLOCK_CELLS[:, 1]] = True
N_BLOCK = 64
# Section 2.4: y_st = x_s * w_t in +-1 form; the board as reviewed.
X_SIGN = {**{s: 1 for s in ON}, **{s: -1 for s in OFF}}
W_SIGN = {**{t: 1 for t in T4}, **{t: -1 for t in T5}}
BOARD = np.array([X_SIGN[s] * W_SIGN[t] == 1 for s, t in BLOCK_NAMES])
QUADRANTS = {"ON x T4": [i for i, (s, t) in enumerate(BLOCK_NAMES) if s in ON and t in T4],
             "OFF x T5": [i for i, (s, t) in enumerate(BLOCK_NAMES) if s in OFF and t in T5],
             "ON x T5": [i for i, (s, t) in enumerate(BLOCK_NAMES) if s in ON and t in T5],
             "OFF x T4": [i for i, (s, t) in enumerate(BLOCK_NAMES) if s in OFF and t in T4]}
MASKS = {"ko": ~BLOCK, "full": np.ones((65, 65), bool), "block": BLOCK.copy()}

# Section 1.3: what is removed; the counts as registered.
N_TRAIN_CELLS, N_TRAIN_PRESENT = 4161, 572

# Section 1.4: the pre-data tables as registered. Sources: (training targets, training sources);
# targets: (training sources, training targets). Present cells outside the block, self-loops in.
ENDPOINTS_EXPECTED = {
    "Mi1": (25, 17), "Tm3": (18, 12), "Mi4": (23, 17), "Mi9": (21, 19),
    "Tm1": (24, 15), "Tm2": (18, 13), "Tm4": (18, 14), "Tm9": (9, 14),
    "T4a": (8, 9), "T4b": (6, 6), "T4c": (8, 7), "T4d": (6, 6),
    "T5a": (4, 7), "T5b": (5, 8), "T5c": (4, 7), "T5d": (6, 6)}
INFERABLE_MIN = 2                                      # Johnny's rule: >= 2 on both endpoints
INFERABLE_EXPECTED = 64
MIRRORS_EXPECTED = {("T4a", "Mi9"), ("T4b", "Mi9"), ("T4c", "Mi9"), ("T5b", "Tm2"),
                    ("T5c", "Tm2")}                    # (target, source), present
INFERABILITY_PROVENANCE = (                            # printed as registered; not recomputed
    ("FlyWire-30", "14 / 64", "provenance only (Johnny, review of 2026-09-24)"),
    ("male CNS v1.0", "64 / 64 at every pair threshold tried (Zcode, preliminary graph)",
     "control arm; recomputed from the built bank and printed before its data (section 8)"))
MIRROR_IDX = sorted(BLOCK_NAMES.index((s, t)) for (t, s) in MIRRORS_EXPECTED)

# Section 2: the predictors. The primary is rule #2.1 (D1 (i)); BF_1..BF_4; N1.
RANKS = (1, 2, 3, 4)
BF_KEYS = tuple(f"BF:{r}" for r in RANKS)
PRED_KEYS = ("rule",) + BF_KEYS + ("N1",)
PRED_NAME = {"rule": "rule #2.1", **{f"BF:{r}": f"BF_{r}" for r in RANKS}, "N1": "N1"}

# Sections 2.4 and 4: the cuts. Revision 3.2 (A5) splits revision 3.1's one CEILING_CUT, which
# was read on two variables, into two named constants with the same value, so nothing changes
# numerically: GATE_CUT gates G on rule #2.1's ceiling_block (section 4); MECHANISM_CUT picks the
# mechanism word of G on rule #2.1's ceiling_full (a description only, borrowed from the gate and
# not calibrated).
GATE_CUT = 0.90
MECHANISM_CUT = 0.90
P_R = 0.01                                             # leg P for R
P_W = 0.05 / len(RANKS)                                # leg P for W (0.0125, D6 (i))
P_G = 0.10                                             # G needs p_P > 0.10 for every predictor
N_DEG_NAME_ABOVE = 5                                   # section 3.2, D14 (ii): naming threshold
# 1e-9, the harness's tie band (revision 3.2, section 3.2). Inert in p_P and p_P_rowcol: with 32
# present of 64, every AUC there is a multiple of 1/2048, so x >= y - TAU holds exactly when
# x >= y. In n_ge a shuffle's margin is scored on the shuffled block, whose present count need not
# be 32, so it is a multiple of 1/(2 n_present n_absent); two unequal margins then differ by far
# more than TAU, and TAU can only turn a rounding difference between equal fractions into a tie.
# The tie band that matters is the lambda tie in fitting.
TAU = H.TAU
FIXED_LAMBDA = 1.0                                     # section 3.5: the fixed-lambda diagnostic
LAMBDA_TIE_TEXT = "1e-9"                               # harness.py:727-728 (fit_bf), literal
WITHIN_FLY_NOTE = ("within-fly variation, not a cut: one FlyWire column differs from FlyWire-30 "
                   "by a median of 34 extra and 27 missing pairs out of 900 cells (about 4 of 64 "
                   "cells if spread evenly; X_c = 0.54 shows it is not) (section 2.4)")

# Section 3.2: the legs.
N_SHUFFLES = H.N_SHUFFLES                              # 99, harness.shuffled_bank(base, sd)
N_PERM = 9999
RC_SWAPS = 20 * 32                                     # successful checkerboard swaps per draw
N_PERM_CEILINGS = 20                                   # section 2.4, D9

# Section 3.7: seeds, all new; asserted distinct in assert_seeds_unique.
SEED_PERM = 90000                                      # leg P uniform; permutation 0 = leakage
SEED_RC = 90001                                        # leg P row-and-column
SEED_PERM_CEIL = 90010                                 # + j, j = 0..19
SEED_WORLD = 90100                                     # + 10 i + j

# Section 3.6: the synthetic worlds. Family index i (seeds) is the position in this tuple.
# Revision 3 appends M0.6, M0.75 and M0.85 (i = 6, 7, 8; seeds 90160-90184), so that the worlds
# of revision 2 keep their seeds and their saved fits.
#   family, gamma on z, gamma on z1, block board
FAMILIES = (("R", 2.0, 0.0, "z"), ("Nf", 0.0, 0.0, "z"), ("No", 2.0, 0.0, "z'"),
            ("W", 1.5, 2.5, "z"), ("M0.5", 0.5, 0.0, "z"), ("M1.0", 1.0, 0.0, "z"),
            ("M0.6", 0.6, 0.0, "z"), ("M0.75", 0.75, 0.0, "z"), ("M0.85", 0.85, 0.0, "z"))
WORLDS_PER_FAMILY = 5
Z_PLUS = set(ON) | set(T4)                             # z = +1; z = -1 on OFF and T5
ZPRIME_PLUS = {"Mi1", "Tm3", "Tm1", "Tm2", "T4a", "T4b", "T5a", "T5b"}   # z' = +1; -1 on the rest
# Section 3.6 (revisions 3, 3.1): the dense grid on which the three limits are measured, and the
# two anchors printed beside it (Nf at gamma = 0, R at gamma = 2.0), which enter no limit.
DENSE_GRID = ((0.5, "M0.5"), (0.6, "M0.6"), (0.75, "M0.75"), (0.85, "M0.85"), (1.0, "M1.0"))
CURVE_ANCHORS = ((0.0, "Nf"), (2.0, "R"))
M_FAMILIES = tuple(f for _, f in DENSE_GRID)
LIMIT_KEYS = ("rule",) + BF_KEYS                       # each has its own leg-P limit
LAMBDA_MAX = max(H.BF_LAMBDAS)                         # the lambda at which the fit is N1's
BINOMIAL_PS = (0.2, 0.4)                               # Johnny's binomial note (section 3.6)

# Section 3.6 (revision 3): the requirement rows, one per family. Each code says what a label
# means for a world of that family:
#   ok      meets the requirement                 stop    fails it; the real arm does not run
#   miss    does not meet it; no stop by itself   nocont  no stop; the No contingency
#   curve   a point of the power curve; no requirement, no stop
# min_meet: the family stops if fewer worlds than this meet it. A family stops if any world reads
# a "stop" label or if fewer than min_meet worlds read an "ok" label.
LABELS = ("R", "W", "G", "U")
_CURVE = {"R": "curve", "W": "curve", "G": "curve", "U": "curve"}
REQUIREMENTS = (
    ("R",  "each of 5 worlds reads R, on both D1 candidates",
     {"R": "ok", "W": "stop", "G": "stop", "U": "stop"}, 5),
    ("Nf", "never R or W (stop); at least 3 of 5 read G",
     {"R": "stop", "W": "stop", "G": "ok", "U": "miss"}, 3),
    ("No", "never R or W (stop); reads G; a U triggers the No contingency",
     {"R": "stop", "W": "stop", "G": "ok", "U": "nocont"}, 0),
    ("W",  "each of 5 worlds reads W, on both D1 candidates",
     {"R": "stop", "W": "ok", "G": "stop", "U": "stop"}, 5),
) + tuple((f, "power curve: printed, no stop row; the three limits are taken from it", _CURVE, 0)
          for f in M_FAMILIES)
NO_CONTINGENCY = "The design cannot tell an orthogonal board from absence."
U_UNCALIBRATED = "insufficient evidence (uncalibrated)"
U_THRESHOLD = "on the detection threshold; cannot be separated"
# Revision 3.2 (A2): a U whose reasons include ceiling_block below GATE_CUT is a failed fit,
# printed as such whatever else is listed; the U rule's rename never applies to it.
FAILED_FIT_TEXT = "failed fit: rule #2.1 cannot hold the block even when trained on it alone"
CEILING_BLOCK_REASON = "rule #2.1's ceiling_block = "   # the prefix of that reason
# Revision 3.3 (A4): a ceiling_block that was not measured (None) is not a failed fit and is not
# "below 0.90"; it has its own reason and its own U text, and the U rule's rename never applies
# to it. The reason does not start with CEILING_BLOCK_REASON.
CEILING_BLOCK_NOT_MEASURED = ("rule #2.1's ceiling_block was not measured, so the G gate of "
                              "section 4 cannot be read")
NOT_MEASURED_TEXT = ("not measured: rule #2.1's ceiling_block was not measured; the G gate "
                     "cannot be read")
# Revision 3.3 (A7): a real-arm run made with --allow-dirty is not the registered run.
NOT_REGISTERED_TEXT = ("NOT THE REGISTERED RUN: made with --allow-dirty; this verdict cannot be "
                       "cited as the registered result (sections 3.3, 7).")
N_DEG_SENTENCE = ("{n} of {N} shuffles have no AUC on the block and are excluded from leg S, "
                  "which counts against {k} = {N} - {n} shuffles (smallest p_S {ps:.3f})")

# Section 3.4, check 8: the harness identity, as in bf1_p3.
BF1_FULL_BANK_MARGIN = 0.028150051052145946
IDENTITY_TOL = 1e-9
PARITY_TOL = 1e-9                                      # section 3.4, check 5
# Revision 3.2 (A1): the tolerance of the reproduction gate on the continuous columns of
# synthetic_worlds.csv, in each column's own units. The name is reused from
# results/genome/c6/checks/bf1_p3.py (MACHINE_CHECK_TOL = 1e-9); TAU is not reused for it.
MACHINE_CHECK_TOL = 1e-9


def log(m=""):
    print(m, flush=True)


def json_safe(x):
    """Section 7: summary.json must be valid JSON; NaN and infinities become null."""
    if isinstance(x, dict):
        return {str(k): json_safe(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [json_safe(v) for v in x]
    if isinstance(x, np.ndarray):
        return json_safe(x.tolist())
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if isinstance(x, (int, np.integer)):
        return int(x)
    if isinstance(x, (float, np.floating)):
        return float(x) if np.isfinite(x) else None
    return x


def dump_json(obj):
    return json.dumps(json_safe(obj), indent=1, allow_nan=False)


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                          check=True).stdout.rstrip()      # keeps porcelain's status column


def machine_record():
    """Revision 3.2 (A4), for the manifest: the BLAS numpy was built with
    (numpy.show_config), the BLAS loaded at run time (threadpoolctl, if installed), the machine
    and CPU, and the four thread variables as found before setdefault and as in effect."""
    rec = {}
    try:
        cfg = np.show_config(mode="dicts")
        rec["numpy_build"] = {k: cfg.get("Build Dependencies", {}).get(k)
                              for k in ("blas", "lapack")}
        rec["numpy_machine_information"] = cfg.get("Machine Information")
        rec["numpy_simd"] = cfg.get("SIMD Extensions")
    except Exception as e:                             # recorded, never fatal
        rec["numpy_build"] = {"error": repr(e)}
    try:
        import threadpoolctl
        # the library path is reduced to its file name: the manifest is committed, and an
        # absolute path names the user's home directory without telling the reader anything
        rec["blas_at_run_time"] = [{**i, "filepath": os.path.basename(i.get("filepath") or "")}
                                   for i in threadpoolctl.threadpool_info()]
    except Exception as e:
        rec["blas_at_run_time"] = {"error": repr(e)}
    # no host name: the manifest is committed, and the CPU, not the host, sets the BLAS kernel
    rec["machine"] = {"machine": platform.machine(),
                      "processor": platform.processor(), "platform": platform.platform(),
                      "cpu_count": os.cpu_count(),
                      "PROCESSOR_IDENTIFIER": os.environ.get("PROCESSOR_IDENTIFIER")}
    rec["thread_env"] = {v: {"found": THREAD_ENV_FOUND[v], "in_effect": os.environ.get(v)}
                         for v in THREAD_VARS}
    return rec


# ------------------------------------------------------------------------------------------
# Section 7 step 1: refusals; section 1.1: pins; section 3.4 check 1.

def refuse_if_dirty(allow_dirty):
    """Section 3.3: the real arm runs once, at a committed head, with the tree clean under
    results/genome/c6/ and docs/plans/ (the refusal of harness.rule_run, reused)."""
    d = git("status", "--porcelain", "--", "results/genome/c6", "docs/plans")
    if d and not allow_dirty:
        sys.exit("REFUSED: uncommitted changes under results/genome/c6/ or docs/plans/; a "
                 f"verdict must be tied to a commit ({REGISTRATION} and this script first).\n" + d)
    return d


def check_pins():
    """Section 3.4 check 1: every sha256 equals section 1.1's table, the versions are section
    7's, and rule #2.1 loads through harness.load_rule with RANK == 1."""
    bad = {f: (PINS_READ[f], PINS[f]) for f in PINS if PINS_READ[f] != PINS[f]}
    now = {f: sha256_lf(ROOT / f) for f in PINS}
    bad.update({f: (now[f], PINS[f]) for f in PINS if now[f] != PINS[f]})
    if bad:
        sys.exit("REFUSED: pins differ (section 1.1): " + json.dumps(bad, indent=1))
    py, npv = platform.python_version(), np.__version__
    if (py, npv) != (PYTHON_VERSION, NUMPY_VERSION):
        sys.exit(f"REFUSED: Python {py}, numpy {npv}; section 7 requires {PYTHON_VERSION}, "
                 f"{NUMPY_VERSION}")
    rule = H.load_rule(RULE_PATH)
    if rule.rank != 1:
        sys.exit(f"REFUSED: rule #2.1 loads with RANK = {rule.rank}, registered 1 (section 3.4)")
    return {"pins": now, "python": py, "numpy": npv, "rule_name": rule.name,
            "rule_rank": rule.rank, "passed": True}


# ------------------------------------------------------------------------------------------
# Section 3.4 checks 2, 3, 4, 5, 7: the block, the board, the pre-data tables, N1 parity, AUC.

def check_block_and_mask():
    """Check 2: 64 cells, 8 distinct sources and 8 distinct targets, all 16 names in NAMES; the
    training mask has 4,161 cells and none is a block cell; the ceiling_block mask is the 64."""
    ko, blk = MASKS["ko"], MASKS["block"]
    ok = (len(set(map(tuple, BLOCK_CELLS.tolist()))) == N_BLOCK
          and len(set(BLOCK_CELLS[:, 0].tolist())) == 8 and len(set(BLOCK_CELLS[:, 1].tolist())) == 8
          and not set(SOURCES) & set(TARGETS) and all(n in H.NAMES for n in SOURCES + TARGETS)
          and int(ko.sum()) == N_TRAIN_CELLS and not (ko & BLOCK).any()
          and int(blk.sum()) == N_BLOCK and np.array_equal(blk, BLOCK)
          and int(MASKS["full"].sum()) == 65 * 65
          and len(H.make_view(H.Bank("geometry", {}), ko).cells) == N_TRAIN_CELLS)
    if not ok:
        sys.exit("BLOCK OR MASK DIFFERS (section 3.4, check 2)")
    return {"cells": N_BLOCK, "sources": 8, "targets": 8, "training_cells": int(ko.sum()),
            "ceiling_block_cells": int(blk.sum()), "passed": True}


def check_board(bank):
    """Check 3 (real arm only): the block has 32 present cells, ON x T4 = 16, OFF x T5 = 16,
    cross = 0; equivalently y_st = x_s * w_t on all 64 cells."""
    y = bank.exists[BLOCK_CELLS[:, 0], BLOCK_CELLS[:, 1]]
    q = {k: int(y[v].sum()) for k, v in QUADRANTS.items()}
    ok = (int(y.sum()) == 32 and q == {"ON x T4": 16, "OFF x T5": 16, "ON x T5": 0,
                                       "OFF x T4": 0} and np.array_equal(y, BOARD))
    if not ok:
        print("BOARD DIFFERS FROM THE REVIEWED COUNT", flush=True)
        sys.exit(1)
    return {"present": 32, "quadrants": q, "y_equals_x_times_w": True, "passed": True}


def pre_data_tables(bank):
    """Section 1.4, from presence outside the block only: what each endpoint keeps, Johnny's
    inferability, the mirror cells, and the training present count (section 1.3)."""
    ex = bank.exists & ~BLOCK
    keep = {}
    for s in SOURCES:
        i = H.IDX[s]
        keep[s] = (int(ex[i, :].sum()), int(ex[:, i].sum()))
    for t in TARGETS:
        i = H.IDX[t]
        keep[t] = (int(ex[:, i].sum()), int(ex[i, :].sum()))
    inf = [(s, t) for s, t in BLOCK_NAMES
           if keep[s][0] >= INFERABLE_MIN and keep[t][0] >= INFERABLE_MIN]
    mirrors = {(t, s) for s, t in BLOCK_NAMES if ex[H.IDX[t], H.IDX[s]]}
    return {"endpoints": keep, "inferable": len(inf), "mirrors": sorted(mirrors),
            "training_present": int(ex.sum())}


def check_pre_data_tables(tables):
    """Check 4: the three tables of section 1.4 (and section 1.3's 572) as registered."""
    ok = (tables["endpoints"] == ENDPOINTS_EXPECTED and tables["inferable"] == INFERABLE_EXPECTED
          and set(map(tuple, tables["mirrors"])) == MIRRORS_EXPECTED
          and tables["training_present"] == N_TRAIN_PRESENT)
    if not ok:
        print("PRE-DATA TABLES DIFFER", flush=True)
        print(json.dumps(json_safe(tables), indent=1), flush=True)
        sys.exit(1)
    return {"passed": True, **tables}


def parity_D(z, y):
    """Section 2.3: D(z) = mean of z over the present block cells minus mean over the absent."""
    y = np.asarray(y, bool)
    if y.all() or not y.any():
        return None
    return float(np.mean(z[y]) - np.mean(z[~y]))


def n1_block_logit(n1data):
    """N1's existence logit on the 64 block cells, from the data as the decoder sees it."""
    c = H.cast(n1data)
    return c["ex_c"][0] + c["ex_a"][BLOCK_CELLS[:, 0]] + c["ex_b"][BLOCK_CELLS[:, 1]]


def check_n1_parity(n1data, y):
    """Check 5: |D(N1 logit)| < 1e-9 on the block: the board is balanced and N1 is additive."""
    d = parity_D(n1_block_logit(n1data), y)
    if d is None or abs(d) >= PARITY_TOL:
        print(f"N1 PARITY IDENTITY FAILS: D = {d}", flush=True)
        sys.exit(1)
    return {"D_N1_logit": d, "tolerance": PARITY_TOL, "passed": True}


def auc(p, y):
    """Section 3.1: the Mann-Whitney probability that a present cell outranks an absent one, ties
    counted as 1/2; None when the cells are all present or all absent."""
    p, y = np.asarray(p, np.float64), np.asarray(y, bool)
    pos, neg = p[y], p[~y]
    if len(pos) == 0 or len(neg) == 0:
        return None
    gt = int((pos[:, None] > neg[None, :]).sum())
    eq = int((pos[:, None] == neg[None, :]).sum())
    return (gt + 0.5 * eq) / (len(pos) * len(neg))


def avg_ranks(p):
    """1-based ranks with ties averaged (the Mann-Whitney convention)."""
    p = np.asarray(p, np.float64)
    order = np.argsort(p, kind="mergesort")
    sp = p[order]
    r = np.empty(len(p))
    i = 0
    while i < len(p):
        j = i
        while j + 1 < len(p) and sp[j + 1] == sp[i]:
            j += 1
        r[order[i:j + 1]] = 0.5 * (i + j) + 1.0
        i = j + 1
    return r


def auc_null(p, Y):
    """AUC of one fixed prediction against many label vectors (rows of Y), by the rank sum; equal
    to auc() on every row (check 7 tests it). Every row must hold the same number of presents."""
    Y = np.asarray(Y, bool)
    n1 = Y.sum(1)
    assert (n1 == n1[0]).all() and 0 < n1[0] < Y.shape[1]
    n1, n0 = int(n1[0]), Y.shape[1] - int(n1[0])
    return (Y.astype(np.float64) @ avg_ranks(p) - n1 * (n1 + 1) / 2) / (n1 * n0)


def check_auc_function():
    """Check 7: on hand-made inputs the AUC is exact: a perfect ranking gives 1, its reverse 0,
    all ties 0.5, and a mixed case with one tie 0.875; the rank-sum path agrees on each and on a
    random 32/32 case with ties."""
    y = np.array([1, 1, 0, 0], bool)
    cases = [([0.9, 0.8, 0.2, 0.1], y, 1.0), ([0.1, 0.2, 0.8, 0.9], y, 0.0),
             ([0.5, 0.5, 0.5, 0.5], y, 0.5),
             ([0.9, 0.5, 0.5, 0.1], np.array([1, 0, 1, 0], bool), 0.875)]
    got = [auc(p, yy) for p, yy, _ in cases]
    ranks = [float(auc_null(p, yy[None, :])[0]) for p, yy, _ in cases]
    rng = np.random.default_rng(12345)                 # a check input, not a registered seed
    p = np.round(rng.random(64), 2)                    # rounded, so that ties occur
    yy = np.zeros(64, bool)
    yy[rng.permutation(64)[:32]] = True
    ok = (all(g == e for g, (_, _, e) in zip(got, cases))
          and all(r == e for r, (_, _, e) in zip(ranks, cases))
          and float(auc_null(p, yy[None, :])[0]) == auc(p, yy)
          and auc(p, np.ones(64, bool)) is None)
    if not ok:
        print(f"AUC FUNCTION FAILS: {got}, {ranks}", flush=True)
        sys.exit(1)
    return {"hand_cases": [e for _, _, e in cases], "got": got, "rank_path": ranks,
            "passed": True}


def data_sha256(d):
    """The G-det comparison of rule #2.1 (same keys, dtypes and values), as one hash."""
    h = hashlib.sha256()
    for k in sorted(d):
        a = np.ascontiguousarray(np.asarray(d[k]))
        h.update(k.encode())
        h.update(str(a.dtype).encode())
        h.update(str(a.shape).encode())
        h.update(a.tobytes())
    return h.hexdigest()


# ------------------------------------------------------------------------------------------
# Sections 3.2 and 3.7: the permutations and the seeds.

_PERM_CACHE = {}


def uniform_perms():
    """Leg P: default_rng(90000), 9,999 x permutation(64) in order; permutation 0 is also the
    leakage check's."""
    if "u" not in _PERM_CACHE:
        rng = np.random.default_rng(SEED_PERM)
        _PERM_CACHE["u"] = np.array([rng.permutation(N_BLOCK) for _ in range(N_PERM)])
    return _PERM_CACHE["u"]


def perm_ceiling_perm(j):
    """Section 2.4, D9: permutation j of the block, default_rng(90010 + j).permutation(64)."""
    return np.random.default_rng(SEED_PERM_CEIL + j).permutation(N_BLOCK)


def rc_patterns(y):
    """Leg P, row-and-column variant (D4): 9,999 random 8 x 8 patterns with the block's row and
    column counts, each by 20 x 32 successful checkerboard swaps from the pattern y, one
    generator default_rng(90001) for all draws. The chains advance together: at every step one
    attempt (rows i, j; columns k, l) is drawn for every chain, rng.integers(8, size=(9999, 4));
    a chain that has its 640 swaps ignores its attempt. An attempt with i == j or k == l, or
    whose 2 x 2 is not a checkerboard, fails."""
    key = np.asarray(y, bool).tobytes()
    if key in _PERM_CACHE:
        return _PERM_CACHE[key]
    rng = np.random.default_rng(SEED_RC)
    yb = np.asarray(y, bool).reshape(8, 8)
    B = np.broadcast_to(yb, (N_PERM, 8, 8)).copy()
    succ = np.zeros(N_PERM, np.int64)
    n = np.arange(N_PERM)
    while (succ < RC_SWAPS).any():
        a = rng.integers(8, size=(N_PERM, 4))
        i, j, k, l = a[:, 0], a[:, 1], a[:, 2], a[:, 3]
        x11, x12, x21, x22 = B[n, i, k], B[n, i, l], B[n, j, k], B[n, j, l]
        ok = ((succ < RC_SWAPS) & (i != j) & (k != l) & (x11 == x22) & (x12 == x21)
              & (x11 != x12))
        m = n[ok]
        for r, c in ((i, k), (i, l), (j, k), (j, l)):
            B[m, r[ok], c[ok]] = ~B[m, r[ok], c[ok]]
        succ += ok
    assert (B.sum(2) == yb.sum(1)).all() and (B.sum(1) == yb.sum(0)).all()
    out = B.reshape(N_PERM, N_BLOCK)
    _PERM_CACHE[key] = out
    return out


def _array_sha256(a):
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()


def null_input_digests():
    """Revision 3.3 (F10): digests of the leg-P null inputs, exactly the objects the nulls are
    computed from: the uniform_perms() matrix, and each rc_patterns(y) matrix, keyed by the
    sha256 of the y bytes (the rc_patterns cache key). Computed in the main process, where every
    null is computed (evaluate_bank); pool workers compute no null (they use uniform_perms only
    for check 6's leak bank), so no per-worker digest is collected. Not needed for
    perm_ceiling_perm: its outputs are the |pc: fits, which are store keys, and evaluate_bank
    asserts their labels."""
    u = uniform_perms()
    rc = {hashlib.sha256(k).hexdigest(): {"sha256": _array_sha256(v), "dtype": str(v.dtype),
                                          "shape": list(v.shape)}
          for k, v in _PERM_CACHE.items() if isinstance(k, bytes)}
    return {"uniform_perms": {"sha256": _array_sha256(u), "dtype": str(u.dtype),
                              "shape": list(u.shape), "seed": SEED_PERM,
                              "computed_in": "main process"},
            "rc_patterns_by_y_sha256": rc, "rc_seed": SEED_RC}


def reserved_seeds(starts):
    """Section 3.7, "Untouched", and the reused ranges, read from the harness where it defines
    them."""
    dial = {10000 + 100 * fi + sd for fi in range(len(H.DIAL_F)) for sd in range(H.DIAL_SEEDS)}
    return ({60000, 61000} | set(range(70000, 71000)) | set(range(80000, 81000))
            | {H.PL_SEED, H.PL_SCRAMBLE_SEED, H.PRSH_SEED}
            | {H.RP_SEED_BASE + j for j in H.RP_SEEDS} | dial | {20260923}
            | set(range(N_SHUFFLES)) | {H.PERTURB_SEED_BASE + j for j in range(max(starts, 10))})


def world_specs():
    return [{"family": fam, "i": i, "j": j, "seed": SEED_WORLD + 10 * i + j, "gamma_z": gz,
             "gamma_z1": gz1, "board": board}
            for i, (fam, gz, gz1, board) in enumerate(FAMILIES) for j in range(WORLDS_PER_FAMILY)]


def assert_seeds_unique(starts):
    """Section 3.7: the new seeds (90000, 90001, 90010-90029, 90100-90184) are distinct, lie in
    90000-90999, and meet none of the untouched or reused seeds."""
    worlds = [w["seed"] for w in world_specs()]
    new = [SEED_PERM, SEED_RC] + [SEED_PERM_CEIL + j for j in range(N_PERM_CEILINGS)] + worlds
    ok = (len(new) == len(set(new)) == 2 + N_PERM_CEILINGS + len(FAMILIES) * WORLDS_PER_FAMILY
          and all(90000 <= s <= 90999 for s in new) and not set(new) & reserved_seeds(starts))
    if not ok:
        sys.exit("SEEDS NOT UNIQUE: " + str(sorted(new)))
    return {"new_seeds": len(new), "unique": True, "in_90000_90999": True,
            "disjoint_from_reserved_and_reused": True, "world_seeds": [min(worlds), max(worlds)]}


# ------------------------------------------------------------------------------------------
# Section 3.6: the synthetic worlds.

OTHERS = [i for i in range(65) if H.NAMES[i] not in set(SOURCES + TARGETS)]
BLOCK_TYPES = [H.IDX[n] for n in SOURCES + TARGETS]
Z_BLOCK = np.zeros(65)
ZPRIME = np.zeros(65)
for _n in SOURCES + TARGETS:
    Z_BLOCK[H.IDX[_n]] = 1.0 if _n in Z_PLUS else -1.0
    ZPRIME[H.IDX[_n]] = 1.0 if _n in ZPRIME_PLUS else -1.0
# Section 3.6, No: sum z z' = 0 over the sources and over the targets.
assert sum(Z_BLOCK[H.IDX[s]] * ZPRIME[H.IDX[s]] for s in SOURCES) == 0
assert sum(Z_BLOCK[H.IDX[t]] * ZPRIME[H.IDX[t]] for t in TARGETS) == 0
NONBLOCK_CELLS = sorted(k for k in H.REAL_CONTENT if not BLOCK[k])   # content pool, 572 cells


def degree_terms():
    """Section 3.6 (D8): N1's existence parameters (c, a, b), fitted on the real knockout view,
    outside-block cells only. The one fit on the real bank that --synthetic-only makes."""
    n1 = H.fit_n1(H.make_view(H.REAL, MASKS["ko"]))
    return float(n1["ex_c"][0]), np.asarray(n1["ex_a"], float), np.asarray(n1["ex_b"], float)


def make_world(spec, terms):
    """Section 3.6: default_rng(seed) draws, in order, z for the 49 other types (ascending harness
    index; +1 iff a uniform draw < 1/2), z1 for the 49 others (drawn in every family, used in W
    only), u (65 x 65), and the content indices (65 x 65 integers into the 572 non-block present
    cells, as planted_banks draws its pool). Outside cells: present iff u < sigmoid(c + a_s + b_t
    + gamma_z z_s z_t + gamma_z1 z1_s z1_t). Block cells: the board by z or z'."""
    rng = np.random.default_rng(spec["seed"])
    z = Z_BLOCK.copy()
    z[OTHERS] = np.where(rng.random(len(OTHERS)) < 0.5, 1.0, -1.0)
    z1 = np.zeros(65)
    z1[BLOCK_TYPES] = ZPRIME[BLOCK_TYPES]
    z1[OTHERS] = np.where(rng.random(len(OTHERS)) < 0.5, 1.0, -1.0)
    u = rng.random((65, 65))
    pool = rng.integers(len(NONBLOCK_CELLS), size=(65, 65))
    c, a, b = terms
    logit = (c + a[:, None] + b[None, :] + spec["gamma_z"] * np.outer(z, z)
             + spec["gamma_z1"] * np.outer(z1, z1))
    ex = u < 1.0 / (1.0 + np.exp(-logit))
    zb = Z_BLOCK if spec["board"] == "z" else ZPRIME
    ex[BLOCK] = (np.outer(zb, zb) > 0)[BLOCK]
    content = {}
    for s, t in zip(*np.nonzero(ex)):
        src = H.REAL_CONTENT[NONBLOCK_CELLS[pool[s, t]]]
        content[(int(s), int(t))] = {"offsets": dict(src["offsets"]), "hull": [],
                                     "sign": src["sign"]}
    bank = H.Bank(f"world.{spec['family']}.{spec['seed']}", content)
    assert int(bank.exists[BLOCK].sum()) == 32
    return bank


def spec_of(family, j):
    for w in world_specs():
        if w["family"] == family and w["j"] == j:
            return w
    raise KeyError((family, j))


def permute_block(bank, perm, name):
    """The bank with its block replaced by a within-block permutation: block cell i takes the
    label and content of block cell perm[i], so the new labels are y[perm]."""
    content = {k: v for k, v in bank.content.items() if not BLOCK[k]}
    for i, (s, t) in enumerate(BLOCK_CELLS.tolist()):
        src = tuple(BLOCK_CELLS[perm[i]].tolist())
        if src in bank.content:
            content[(s, t)] = bank.content[src]
    return H.Bank(name, content)


def build_bank(key, terms, synthetic_only):
    """Bank keys: "real" or "world:<family>:<j>", then optional "|sh:<sd>" (harness.shuffled_bank),
    "|pc:<j>" (permuted-block ceiling) or "|leak" (leg P's permutation 0). Under --synthetic-only a
    real key is refused, so no worker can build, fit or score the real block."""
    base, *mods = key.split("|")
    if base == "real":
        if synthetic_only:
            raise RuntimeError("REFUSED: --synthetic-only never builds a bank on the real block")
        bank = H.REAL
    else:
        _, fam, j = base.split(":")
        bank = make_world(spec_of(fam, int(j)), terms)
    for m in mods:
        if m.startswith("sh:"):
            bank = H.shuffled_bank(bank, int(m[3:]))[0]
        elif m.startswith("pc:"):
            bank = permute_block(bank, perm_ceiling_perm(int(m[3:])), f"{bank.name}.pc{m[3:]}")
        elif m == "leak":
            bank = permute_block(bank, uniform_perms()[0], f"{bank.name}.leak")
        else:
            raise KeyError(key)
    return bank


# ------------------------------------------------------------------------------------------
# Section 2: fitting, in a process pool. A task is (bank key, mask kind, predictor key); mask
# kinds: "ko" (the knockout, section 1.3), "full" (ceiling_full), "block" (ceiling_block),
# "ko1" (the knockout at fixed lambda = 1, the diagnostic of section 3.5; rule #2.1 and BF_r
# only), "ko#hash#<n>" (checks 6 and 9: the data dict's hash only), "cv:<f>" (check 8).

_W = {}


def _w_init(starts, terms, synthetic_only):
    H.STARTS = starts                                  # the harness global every fit reads
    os.environ.pop("SECOND_RULE_SPREAD_DIR", None)
    _W.update(starts=starts, terms=terms, syn=synthetic_only, rule=H.load_rule(RULE_PATH),
              bf={}, key=None, bank=None)


def _pred(key):
    if key == "rule":
        return _W["rule"]
    if key == "N1":
        return H.N1
    r = int(key.split(":")[1])
    if r not in _W["bf"]:
        _W["bf"][r] = H.bf_predictor(r)
    return _W["bf"][r]


def _lambda_of(pk, P, data):
    if pk == "rule":
        return float(P.fit.__globals__["LAST_FIT"]["lambda"])
    if "bf_lambda" in data:
        return float(np.asarray(data["bf_lambda"])[0])
    return None


def train_fixed_lambda(pk, P, bank, lam):
    """Section 3.5, the fixed-lambda diagnostic: the knockout fit with lambda fixed, nothing else
    changed; the pinned files are not modified. BF_r: harness.bf_als, the harness function that
    takes lambda, called as fit_bf's final fit calls it (fit_n1 on the view, its logit grid as
    offset, the view's grid; k = STARTS). Rule #2.1: its fit reads the grid from its module global
    LAMBDAS (fit.py:57, 128-142), and has no lambda argument; the global is set to [lam] for this
    one fit and restored, so the nested choice has one candidate and the final fit is at lam."""
    if pk == "rule":
        g = P.fit.__globals__
        saved = g["LAMBDAS"]
        g["LAMBDAS"] = [lam]
        try:
            data = P.train(bank, MASKS["ko"])
        finally:
            g["LAMBDAS"] = saved
        assert float(g["LAST_FIT"]["lambda"]) == lam
        return data
    r = int(pk.split(":")[1])
    view = H.make_view(bank, MASKS["ko"])
    n1 = H.fit_n1(view)
    M, Y = H._grid(view)
    U, V = H.bf_als(H._n1_logit_grid(n1), Y, M, r, lam, starts=H.STARTS)
    n1.update({"bf_U": U, "bf_V": V, "bf_lambda": np.array([float(lam)])})
    return n1


def _w_group(group):
    key = group[0][0]
    if _W["key"] != key:
        _W["bank"], _W["key"] = build_bank(key, _W["terms"], _W["syn"]), key
    bank = _W["bank"]
    out = []
    for bk, mk, pk in group:
        assert bk == key
        P = _pred(pk)
        t0 = time.time()
        if mk.startswith("cv:"):
            s = H.cv_fold(P, bank, int(mk[3:]))
            out.append(((bk, mk, pk), {"score": s, "secs": time.time() - t0}))
            continue
        if mk == "ko1":
            data = train_fixed_lambda(pk, P, bank, FIXED_LAMBDA)
        else:
            data = P.train(bank, MASKS[mk.split("#")[0]])
        if "#hash" in mk:
            out.append(((bk, mk, pk), {"data_sha256": data_sha256(data),
                                       "secs": time.time() - t0}))
            continue
        dec = P.decode(data, BLOCK_CELLS)
        sc = H.score(dec, bank, BLOCK_CELLS)
        out.append(((bk, mk, pk), {
            "p": np.asarray(dec["p_exist"], np.float64).tolist(),
            "y": bank.exists[BLOCK_CELLS[:, 0], BLOCK_CELLS[:, 1]].tolist(),
            "lam": _lambda_of(pk, P, data),
            # revision 3.3 (C7): sign_n (the integer) is stored beside the five fields of
            # earlier records; raw_fits_diagnostic compares the fields present in both
            "score": {k: sc[k] for k in ("existence", "offset", "counts", "sign", "sign_n",
                                         "n_ne")},
            "outside_density": float(bank.exists[~BLOCK].mean()),
            "secs": time.time() - t0}))
    return out


def run_groups(groups, workers, init_args, what):
    """Every group shares one bank; results keyed by (bank key, mask kind, predictor key)."""
    t0 = time.time()
    log(f"[{what}] {len(groups)} groups, {sum(len(g) for g in groups)} fits, workers = {workers}")
    res = {}
    if workers <= 1:
        _w_init(*init_args)
        for g in groups:
            res.update(dict(_w_group(g)))
    else:
        with ProcessPoolExecutor(max_workers=workers, initializer=_w_init,
                                 initargs=init_args) as ex:
            futs = [ex.submit(_w_group, g) for g in groups]
            done, step = 0, max(1, len(futs) // 20)
            for f in as_completed(futs):
                res.update(dict(f.result()))
                done += 1
                if done % step == 0 or done == len(futs):
                    el = time.time() - t0
                    log(f"[{what}] {done}/{len(futs)} groups, {el:.0f}s elapsed, about "
                        f"{el / done * (len(futs) - done):.0f}s left")
    log(f"[{what}] done in {time.time() - t0:.0f}s")
    return res


def plan_bank(base_key, n_sh, n_pc):
    """Section 7 step 4 for one bank: knockout fits and both ceilings for the six predictors, the
    permuted-block ceiling_full of the primary (D9), and the shuffles x 6 predictors (leg S). The
    base groups come first, since they are the longest."""
    groups = [[(base_key, mk, pk) for pk in PRED_KEYS] for mk in ("ko", "full", "block")]
    groups += [[(f"{base_key}|pc:{j}", "full", "rule")] for j in range(n_pc)]
    groups += [[(f"{base_key}|sh:{sd}", "ko", pk) for pk in PRED_KEYS] for sd in range(n_sh)]
    return groups


# ------------------------------------------------------------------------------------------
# Sections 3.1, 3.2, 3.5: what is computed and printed per predictor on one bank.

def precision_at_32(p, y):
    """Share of present cells among the 32 highest p_exist (ties broken in block cell order)."""
    order = np.argsort(-np.asarray(p, np.float64), kind="stable")[:32]
    return float(np.asarray(y, bool)[order].mean())


def regrown_share(a, ceiling):
    """(AUC - 0.5) / (AUC_ceiling - 0.5); "n/a" (None) when the ceiling is <= 0.5. Despite its
    name it is a ratio, not a share: it can exceed 1 and be negative (revision 3.2, section 3.1);
    the CSV column keeps its name."""
    if a is None or ceiling is None or ceiling <= 0.5:
        return None
    return (a - 0.5) / (ceiling - 0.5)


def smallest_passing_auc(y, Yu):
    """Section 3.2: the smallest AUC (on the k/1024 grid) that gives p_P <= 0.01 against this
    run's own 9,999 permutations, for a prediction without ties. Revision 3.3 (B1): it depends
    on the block's labels y through Yu = y[uniform_perms()], not only on their count, and on no
    fit, so it is the same at every gamma: a translation anchor between the AUC axis and P_R,
    not a gamma limit."""
    null = auc_null(np.arange(N_BLOCK, dtype=float), Yu)
    n1 = int(np.asarray(y, bool).sum())
    den = n1 * (N_BLOCK - n1)
    for k in range(den // 2, den + 1):
        a = k / den
        if (1 + int((null >= a - TAU).sum())) / (N_PERM + 1) <= P_R:
            return a
    return None


# Revision 3.4 (item 2): smallest_passing_auc as a checked scalar, registered by board. Pre-run
# values, read from the pinned synthetic_only.json (worlds[*].smallest_passing_auc) joined with
# the board column of the pinned synthetic_worlds.csv: 0.666015625 (682/1024) in all 40 worlds
# with board z, 0.6728515625 (689/1024) in all 5 worlds with board z' (the No family).
SMALLEST_PASSING_AUC_BY_BOARD = {"z": 0.666015625, "z'": 0.6728515625}
SMALLEST_PASSING_AUC_GATES = (
    "it gates one statistic of Yu = y[uniform_perms()] and the composition (the layout y, P_R, "
    "N_PERM), through auc_null on one tie-free prediction; it needs no fit. It does not see Yrc "
    "(rc_patterns), nor a change in the consumer at equal Yu (the p_P lines of evaluate_bank, "
    "avg_ranks on tied predictions, auc); the null-input digests remain for attribution. Under "
    "--from-raw, where y comes from the store and Yu is generated fresh, it is the only check of "
    "the fresh generator that stops the run (the comparison of the re-read table with the pinned "
    "one is for information only)")


def check_smallest_passing_auc(entries, expected=None):
    """Revision 3.4 (item 2): each world's smallest_passing_auc(y, y[uniform_perms()]) against the
    value registered for its board (SMALLEST_PASSING_AUC_BY_BOARD, or `expected`). entries: dicts
    with "world", "board" and "y" (the block labels, 64 booleans in block cell order). A board
    without a registered value is a mismatch. Run by run_synthetic before any fit; a mismatch
    stops the synthetic step. What it gates: SMALLEST_PASSING_AUC_GATES."""
    expected = dict(SMALLEST_PASSING_AUC_BY_BOARD if expected is None else expected)
    perms, cache, per = uniform_perms(), {}, []
    for e in entries:
        y = np.asarray(e["y"], bool)
        k = y.tobytes()
        if k not in cache:
            cache[k] = smallest_passing_auc(y, y[perms])
        got, want = cache[k], expected.get(e["board"])
        per.append({"world": e["world"], "board": e["board"], "computed": got,
                    "registered": want, "equal": want is not None and got == want})
    bad = [p for p in per if not p["equal"]]
    return {"registered_by_board": expected, "n_worlds": len(per),
            "n_equal": len(per) - len(bad), "mismatches": bad,
            "passed": bool(per) and not bad, "gates": SMALLEST_PASSING_AUC_GATES,
            "per_world": per}


def logit_of(p):
    p = np.clip(np.asarray(p, np.float64), 1e-300, 1 - 1e-16)
    return np.log(p / (1 - p))


def evaluate_bank(base_key, F, n_sh, n_pc):
    """Every number of section 3.5 for one bank, and its section 4 label."""
    base = {pk: F[(base_key, "ko", pk)] for pk in PRED_KEYS}
    y = np.asarray(base["N1"]["y"], bool)
    for pk in PRED_KEYS:
        for mk in ("ko", "full", "block"):
            assert np.array_equal(np.asarray(F[(base_key, mk, pk)]["y"], bool), y)
    Yu = y[uniform_perms()]
    Yrc = rc_patterns(y)
    sh = []
    for sd in range(n_sh):
        f = {pk: F[(f"{base_key}|sh:{sd}", "ko", pk)] for pk in PRED_KEYS}
        ysd = np.asarray(f["N1"]["y"], bool)
        a_n1 = auc(f["N1"]["p"], ysd)
        row = {"sd": sd, "present": int(ysd.sum()), "degenerate": a_n1 is None, "auc_N1": a_n1}
        for pk in PRED_KEYS:
            a = auc(f[pk]["p"], ysd)
            row[f"auc_{pk}"] = a
            row[f"M_{pk}"] = None if a is None else a - a_n1
            row[f"lam_{pk}"] = f[pk]["lam"]
        sh.append(row)
    n_deg = sum(r["degenerate"] for r in sh)
    a_n1 = auc(base["N1"]["p"], y)
    ll_n1 = base["N1"]["score"]["existence"]
    rest = [i for i in range(N_BLOCK) if i not in MIRROR_IDX]
    rows = {}
    for pk in PRED_KEYS:
        p = np.asarray(base[pk]["p"], np.float64)
        a = auc(p, y)
        cf = auc(F[(base_key, "full", pk)]["p"], y)
        cb = auc(F[(base_key, "block", pk)]["p"], y)
        m_real = a - a_n1
        # Section 3.2, D14 (ii) (revision 3): a shuffle with no AUC on the block is excluded;
        # leg S counts against n_sh - n_deg.
        n_ge = sum(r[f"M_{pk}"] >= m_real - TAU for r in sh if not r["degenerate"])
        n_valid = n_sh - n_deg
        null_u, null_rc = auc_null(p, Yu), auc_null(p, Yrc)
        per_type = {}
        for n in SOURCES + TARGETS:
            idx = [i for i, (s, t) in enumerate(BLOCK_NAMES) if n in (s, t)]
            per_type[n] = auc(p[idx], y[idx])
        sc = base[pk]["score"]
        rows[pk] = {
            "predictor": PRED_NAME[pk], "auc": a, "n_present": int(y.sum()),
            "n_absent": int((~y).sum()), "D": parity_D(logit_of(p), y),
            "logloss": sc["existence"], "logloss_margin_over_N1": ll_n1 - sc["existence"],
            "precision_at_32": precision_at_32(p, y),
            "quadrant_mean_p": {k: float(p[v].mean()) for k, v in QUADRANTS.items()},
            "ceiling_full": cf, "ceiling_block": cb,
            "regrown_share_full": regrown_share(a, cf), "regrown_share_block": regrown_share(a, cb),
            "M_real": m_real, "n_ge": int(n_ge), "n_shuffles": n_sh, "n_deg": int(n_deg),
            "n_valid_shuffles": int(n_valid),
            "leg_S_passes": bool(n_valid >= 1 and n_ge == 0),
            "p_S": (1 + n_ge) / (1 + n_valid),
            "p_P": (1 + int((null_u >= a - TAU).sum())) / (N_PERM + 1),
            "p_P_rowcol": (1 + int((null_rc >= a - TAU).sum())) / (N_PERM + 1),
            "lambda_ko": base[pk]["lam"], "lambda_full": F[(base_key, "full", pk)]["lam"],
            "lambda_block": F[(base_key, "block", pk)]["lam"],
            "mirror_partners_p": {f"{BLOCK_NAMES[i][0]}->{BLOCK_NAMES[i][1]}": float(p[i])
                                  for i in MIRROR_IDX},
            "auc_other_59": auc(p[rest], y[rest]),
            "per_type_auc": per_type,
            "present_cells_offset_counts_sign": {k: sc[k] for k in ("offset", "counts", "sign")},
        }
    perm_ceilings = []
    for j in range(n_pc):
        f = F[(f"{base_key}|pc:{j}", "full", "rule")]
        yj = np.asarray(f["y"], bool)
        assert np.array_equal(yj, y[perm_ceiling_perm(j)])
        perm_ceilings.append(auc(f["p"], yj))
    fixed = {}
    for pk in ("rule",) + BF_KEYS:                     # section 3.5: diagnostic, decides nothing
        f = F[(base_key, "ko1", pk)]
        assert np.array_equal(np.asarray(f["y"], bool), y) and f["lam"] == FIXED_LAMBDA
        a1 = auc(f["p"], y)
        fixed[pk] = {"predictor": PRED_NAME[pk], "lambda": f["lam"], "auc": a1,
                     "p_P": (1 + int((auc_null(np.asarray(f["p"], float), Yu) >= a1 - TAU)
                                     .sum())) / (N_PERM + 1),
                     "selected_lambda": rows[pk]["lambda_ko"], "selected_auc": rows[pk]["auc"],
                     "reused_from_selected_fit": bool(f.get("reused_from_ko", False))}
    return {"bank": base_key, "rows": rows, "per_shuffle": sh, "n_deg": int(n_deg),
            "fixed_lambda": fixed,
            "perm_ceilings_full_rule": perm_ceilings,
            "outside_density": base["N1"]["outside_density"], "block_present": int(y.sum()),
            "smallest_passing_auc": smallest_passing_auc(y, Yu), **read_label(rows)}


# ------------------------------------------------------------------------------------------
# Section 4: the reading rule.

def reading_on(primary, rows):
    """The R and W rows with `primary` as the primary; the W row ranges over BF_1..BF_4. Leg S
    passes at n_ge = 0 of the n_sh - n_deg shuffles that have an AUC (D14 (ii))."""
    r = rows[primary]
    R = r["leg_S_passes"] and r["p_P"] <= P_R
    passing = [k for k in BF_KEYS if rows[k]["leg_S_passes"] and rows[k]["p_P"] <= P_W]
    W = (not R) and bool(passing)
    return {"primary": PRED_NAME[primary], "letter": "R" if R else ("W" if W else "-"),
            "W_ranks": [PRED_NAME[k] for k in passing]}


def mechanism_description(pr):
    """Section 2.4 (revision 3): the mechanism of G is a description, read from nothing.
    Revision 3.2 (A5): it names whose ceiling_full it quotes (rule #2.1's; it is repeated on all
    six rows of a world in synthetic_worlds.csv), and its cut is MECHANISM_CUT, borrowed from the
    gate and not calibrated."""
    cf = pr["ceiling_full"]
    if cf is not None and cf >= MECHANISM_CUT:
        return f"no information (rule #2.1's ceiling_full = {fmt(cf)} >= {MECHANISM_CUT:.2f})"
    return f"orthogonal (rule #2.1's ceiling_full = {fmt(cf)} < {MECHANISM_CUT:.2f})"


def ceiling_block_reason(cb):
    """The U reason when rule #2.1's ceiling_block is below GATE_CUT (the wording of revision
    3.1's read_label, unchanged); label_text recognises it by CEILING_BLOCK_REASON. Revision 3.3
    (A4): a ceiling_block that was not measured (None) gets its own reason,
    CEILING_BLOCK_NOT_MEASURED, which is not the failed-fit branch and does not say "n/a is below
    0.90"."""
    if cb is None:
        return CEILING_BLOCK_NOT_MEASURED
    return (f"{CEILING_BLOCK_REASON}{fmt(cb)} is below {GATE_CUT:.2f}: the rule cannot hold the "
            "block even when trained on it alone")


def u_kind(reasons):
    """Revision 3.3 (A3, A4): which U a list of U reasons gives. "failed_fit" if a reason is
    ceiling_block below GATE_CUT (whatever else is listed); else "not_measured" if a reason is
    CEILING_BLOCK_NOT_MEASURED; else "threshold". Only threshold U enters the U rule."""
    rs = [str(r) for r in reasons or ()]
    if any(r.startswith(CEILING_BLOCK_REASON) for r in rs):
        return "failed_fit"
    if CEILING_BLOCK_NOT_MEASURED in rs:
        return "not_measured"
    return "threshold"


def read_label(rows):
    """Section 4: R, W, G, U in order. R and W are read on both D1 candidates and must agree,
    else U; if neither gives R or W, G and U are read on rule #2.1. The letter only: its text
    (G with the three limits, U by the U rule) is set by label_text once the synthetic run is
    read."""
    A, B = reading_on("rule", rows), reading_on("BF:1", rows)
    reasons = []
    pr = rows["rule"]
    mech = None
    if A["letter"] == B["letter"] and A["letter"] in ("R", "W"):
        label = A["letter"]
    elif A["letter"] in ("R", "W") or B["letter"] in ("R", "W"):
        label = "U"
        reasons.append(f"the two D1 candidates disagree on R/W: rule #2.1 reads {A['letter']}, "
                       f"BF_1 reads {B['letter']}")
    else:
        clear = all(rows[k]["p_P"] > P_G for k in ("rule",) + BF_KEYS)
        gate = pr["ceiling_block"] is not None and pr["ceiling_block"] >= GATE_CUT
        if clear and gate:
            label = "G"
            mech = mechanism_description(pr)
        else:
            label = "U"
            if not gate:
                reasons.append(ceiling_block_reason(pr["ceiling_block"]))
            if pr["leg_S_passes"] != (pr["p_P"] <= P_R):
                reasons.append(f"the legs disagree for rule #2.1: leg S n_ge = {pr['n_ge']} of "
                               f"{pr['n_valid_shuffles']}, leg P p_P = {pr['p_P']:.4f}")
            for k in ("rule",) + BF_KEYS:
                if rows[k]["p_P"] <= P_G:
                    reasons.append(f"{PRED_NAME[k]}: p_P = {rows[k]['p_P']:.4f} <= 0.10 without "
                                   f"R or W (n_ge = {rows[k]['n_ge']})")
    return {"label": label, "mechanism_description": mech, "reading_A_rule": A,
            "reading_B_BF1": B, "d1_agree_on_RW": A["letter"] == B["letter"],
            "U_reasons": reasons}


def fmt(x, d=4):
    return "n/a" if x is None else f"{x:.{d}f}"


def instrument_text(starts):
    """Section 3.6: what the three limits are measured with; printed with every G."""
    return (f"BF_LAMBDAS {list(H.BF_LAMBDAS)}, ties within {LAMBDA_TIE_TEXT} go to the larger "
            f"lambda (harness.py:727-728), STARTS = {starts}")


def limits_text(dl):
    """Section 3.6 (revision 3.1): the three limits with their brackets, the transition band,
    the per-gamma fractions seen/n and R/n, and the instrument; printed with every G."""
    lp, lr, fam, band = dl["leg_P"], dl["R"], dl["family"], dl["band"]
    return (f"gamma_R = {lr['text']} (bracket {lr['bracket_text']}); leg P from gamma*_P = "
            f"{lp['text']} (bracket {lp['bracket_text']}); family limit = {fam['text']}; "
            f"transition band {band['text']}; per gamma seen/n, R/n: {dl['curve_text']}; "
            f"M-world units; instrument: {dl['instrument']}")


def label_text(label, dl, u_rule, reasons, ceiling_block=None):
    """Section 4 (revisions 3.1, 3.2). G carries its gate variable (rule #2.1's ceiling_block),
    the three limits and the instrument. U: if its reasons include rule #2.1's ceiling_block
    below GATE_CUT, it is a failed fit, whatever else is listed, and the U rule's rename never
    applies to it (revision 3.2, A2); otherwise it is the signature of the leg-P detection limit
    gamma*_P, renamed by the U rule of section 3.6 when no dense-grid world read a threshold U.
    Revision 3.3 (A4): a U whose reasons say that ceiling_block was not measured prints
    NOT_MEASURED_TEXT, and is never renamed either (u_kind).
    Not to be confused with LABEL_TEXT, a dict in flywire_column_test.py (another test's
    labels)."""
    if label == "R":
        return "R: regrows"
    if label == "W":
        return "W: rule weaker than the information available"
    if label == "G":
        return (f"G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = "
                f"{fmt(ceiling_block)} >= {GATE_CUT:.2f}; {limits_text(dl)})")
    kind = u_kind(reasons)
    if kind == "failed_fit":
        return f"U: {FAILED_FIT_TEXT}"
    if kind == "not_measured":
        return f"U: {NOT_MEASURED_TEXT}"
    if u_rule["renamed"]:
        return f"U: {U_UNCALIBRATED}; never read as a finding"
    return (f"U: {U_THRESHOLD} (at the leg-P detection limit gamma*_P = {dl['leg_P']['text']}; "
            f"transition band {dl['band']['text']})")


def lam_text(x):
    return "n/a" if x is None else f"{x:g}"


def verdict_line(ev, dl, u_rule, no_contingency=False, not_registered=None):
    """Section 4: the label (G with the three limits and the instrument; U by the U rule); the
    mechanism description of G; the primary's AUC, p_S and p_P; both ceilings; the R/W reading on
    each D1 candidate; the lambda each knockout fit selected, and a G reached through lambda = 100
    named (revision 3.1, Zcode); the n_deg sentence above 5; the No contingency when triggered.
    The fixed-lambda diagnostic is not on this line (Johnny's condition). Revision 3.3 (A7): when
    not_registered is given (a real-arm run made with --allow-dirty), the line ends with it."""
    r = ev["rows"]["rule"]
    s = label_text(ev["label"], dl, u_rule, ev["U_reasons"], r["ceiling_block"])
    if ev["label"] == "G":
        s += f" [mechanism, description only: {ev['mechanism_description']}]"
    s += (f". rule #2.1: AUC = {fmt(r['auc'])} ({r['n_present']}/{r['n_absent']}), "
          f"p_S = {r['p_S']:.2f} (n_ge = {r['n_ge']} of {r['n_valid_shuffles']}, "
          f"n_deg = {r['n_deg']}), p_P = {r['p_P']:.4f}; ceiling_full = {fmt(r['ceiling_full'])}, "
          f"ceiling_block = {fmt(r['ceiling_block'])}; R/W reading: rule #2.1 -> "
          f"{ev['reading_A_rule']['letter']}, BF_1 -> {ev['reading_B_BF1']['letter']}")
    lams = {pk: ev["rows"][pk]["lambda_ko"] for pk in LIMIT_KEYS}
    s += ("; lambda selected by each knockout fit (nested inner folds): "
          + ", ".join(f"{PRED_NAME[pk]} {lam_text(v)}" for pk, v in lams.items()))
    at_max = [PRED_NAME[pk] for pk, v in lams.items() if v == LAMBDA_MAX]
    if ev["label"] == "G" and at_max:
        s += (f"; G reached through lambda = {lam_text(LAMBDA_MAX)} on {', '.join(at_max)}: "
              "there the interaction is shrunk to N1's additive prediction, so this G reads "
              "'weaker than the detection limit', not 'absent'")
    if ev["n_deg"] > N_DEG_NAME_ABOVE:
        k = r["n_shuffles"] - ev["n_deg"]
        s += "; " + N_DEG_SENTENCE.format(n=ev["n_deg"], N=r["n_shuffles"], k=k,
                                          ps=1 / (1 + k))
    s += "."
    if no_contingency:
        s += " " + NO_CONTINGENCY
    if not_registered:
        s += " " + not_registered
    return s


# ------------------------------------------------------------------------------------------
# Section 3.6: the two-world check, the gamma breakpoint.

def two_world_check(worlds, repro):
    """Section 3.6 (revision 3): each family's worlds, read by section 4, against its
    REQUIREMENTS row. A family stops if any world reads a label coded "stop", or if fewer than
    min_meet worlds read a label coded "ok". The M rows are the power curve and never stop.
    Revision 3.1: a pre-run table that is not reproduced (repro["passed"] is False) stops too."""
    out, stop, nocont = [], repro["passed"] is False, False
    for fam, text, codes, min_meet in REQUIREMENTS:
        per = []
        for w in (w for w in worlds if w["family"] == fam):
            code = codes[w["label"]]
            per.append({"seed": w["seed"], "label": w["label"], "code": code,
                        "meets": code == "ok", "mechanism": w["mechanism_description"]})
        if not per:
            continue
        n_stop = sum(p["code"] == "stop" for p in per)
        n_meet = sum(p["meets"] for p in per)
        stops = n_stop > 0 or n_meet < min_meet
        stop |= stops
        nocont |= any(p["code"] == "nocont" for p in per)
        out.append({"family": fam, "requirement": text, "codes": dict(codes),
                    "min_meet": min_meet, "worlds": per, "n_worlds": len(per),
                    "n_meet": n_meet, "n_stop_labels": n_stop, "stops": stops,
                    "labels": {L: sum(p["label"] == L for p in per) for L in LABELS}})
    return {"rows": out, "stop": stop, "no_contingency": nocont, "passed": not stop,
            "prerun_reproduction": repro}


def worlds_csv_bytes(worlds):
    """synthetic_worlds.csv as bytes (utf-8, the csv module's CRLF rows), exactly as written."""
    fh = io.StringIO(newline="")
    w = csv.writer(fh)
    w.writerow(WORLDS_CSV_HEADER)
    for x in worlds:
        for pk in PRED_KEYS:
            r = json_safe(x["rows"][pk])
            fl = x["fixed_lambda"].get(pk, {})
            w.writerow([x["family"], x["j"], x["seed"], x["gamma_z"], x["gamma_z1"],
                        x["board"], x["label"], x["mechanism_description"] or "",
                        x["outside_density"]]
                       + [r[k] for k in CSV_FIELDS]
                       + [json_safe(fl.get("auc")), json_safe(fl.get("p_P"))])
    return fh.getvalue().encode("utf-8")


def _cells_equal(a, b):
    """Exact comparison of two CSV cells: the same string, or the same float."""
    if a == b:
        return True
    try:
        return float(a) == float(b)
    except ValueError:
        return False


CSV_KEY_COLUMNS = ("family", "j", "seed", "predictor")  # revision 3.3: a row's key


def _mech_renamed_32(text):
    """Revision 3.3 (C5): a pre-run mechanism_description as revision 3.2's rename writes it."""
    return text.replace("(ceiling_full ", "(rule #2.1's ceiling_full = ")


def csv_compare(ref, got, limit=20):
    """Sections 3.3 and 7 (revisions 3.2, 3.3): two synthetic_worlds.csv byte strings compared
    on the deciding columns, rows matched by CSV_KEY_COLUMNS. Separate outputs: rows missing on
    either side (or a duplicated key); key-matched rows whose values differ (CSV_EXACT_COLUMNS
    exactly, CSV_CONTINUOUS_COLUMNS within MACHINE_CHECK_TOL); a change of row order (a fact, not
    an outcome). Column 8 is reported, and each difference there is checked against revision
    3.2's rename. Outcome 1: all equal; 2: continuous within tolerance only; 3: part "a"
    (identity or lattice, rows, header) and/or part "b" (continuous beyond tolerance)."""
    a = list(csv.reader(io.StringIO(ref.decode("utf-8"), newline="")))
    b = list(csv.reader(io.StringIO(got.decode("utf-8"), newline="")))
    head = list(WORLDS_CSV_HEADER)
    res = {"byte_identical": ref == got, "rows_prerun": max(len(a) - 1, 0),
           "rows_now": max(len(b) - 1, 0),
           "header_equal": bool(a and b and a[0] == head and b[0] == head),
           "key_columns": list(CSV_KEY_COLUMNS), "tolerance": MACHINE_CHECK_TOL,
           "malformed_rows": 0, "duplicate_keys": [], "rows_missing_now": [],
           "rows_missing_prerun": [], "row_order_differs": None,
           "exact_differences": 0, "first_exact_differences": [],
           "continuous_within_tolerance": {}, "continuous_beyond_tolerance": 0,
           "first_continuous_beyond_tolerance": [], "mechanism_description_differences": 0,
           "mechanism_description_explained_by_rename_3_2": 0,
           "mechanism_description_unexplained": 0,
           "first_mechanism_description_unexplained": []}
    if not res["header_equal"]:
        return {**res, "outcome": 3, "outcome_3_parts": ["a"], "passed": False,
                "reason": outcome_3_reason(["a"], "the header differs")}
    col = {c: k for k, c in enumerate(head)}

    def index(rows, side):
        out, order = {}, []
        for i, r in enumerate(rows[1:], start=1):
            if len(r) != len(head):
                res["malformed_rows"] += 1
                continue
            k = tuple(r[col[c]] for c in CSV_KEY_COLUMNS)
            if k in out:
                res["duplicate_keys"].append({"side": side, "key": list(k)})
                continue
            out[k] = (i, r)
            order.append(k)
        return out, order

    ia, oa = index(a, "prerun")
    ib, ob = index(b, "now")
    res["rows_missing_now"] = [list(k) for k in oa if k not in ib]
    res["rows_missing_prerun"] = [list(k) for k in ob if k not in ia]
    both = [k for k in oa if k in ib]
    res["row_order_differs"] = both != [k for k in ob if k in ia]
    for k in both:
        (i, ra), (_, rb) = ia[k], ib[k]
        where = {"row": i, "key": list(k)}
        exact = [c for c in CSV_EXACT_COLUMNS if not _cells_equal(ra[col[c]], rb[col[c]])]
        if exact:
            res["exact_differences"] += 1
            res["first_exact_differences"].append({**where, "columns": exact})
        for c in CSV_CONTINUOUS_COLUMNS:
            x, y = ra[col[c]], rb[col[c]]
            if x == y:
                continue
            try:
                d = abs(float(x) - float(y))
            except ValueError:                         # one cell empty ("n/a"), the other not
                d = math.inf
            if d == 0.0:
                continue
            if d <= MACHINE_CHECK_TOL:
                w = res["continuous_within_tolerance"]
                w[c] = max(w.get(c, 0.0), d)
            else:
                res["continuous_beyond_tolerance"] += 1
                res["first_continuous_beyond_tolerance"].append(
                    {**where, "column": c, "prerun": x, "now": y})
        m = col["mechanism_description"]
        if ra[m] != rb[m]:
            res["mechanism_description_differences"] += 1
            if _mech_renamed_32(ra[m]) == rb[m]:
                res["mechanism_description_explained_by_rename_3_2"] += 1
            else:
                res["mechanism_description_unexplained"] += 1
                res["first_mechanism_description_unexplained"].append(
                    {**where, "prerun": ra[m], "now": rb[m]})
    res["mechanism_description_all_explained_by_rename_3_2"] = (
        res["mechanism_description_unexplained"] == 0)
    counts = {f"n_{k}": len(res[k]) for k in ("duplicate_keys", "rows_missing_now",
                                               "rows_missing_prerun")}
    res.update(counts)
    for k in ("duplicate_keys", "rows_missing_now", "rows_missing_prerun",
              "first_exact_differences", "first_continuous_beyond_tolerance",
              "first_mechanism_description_unexplained"):
        res[k] = res[k][:limit]
    part_a = res["exact_differences"] or res["malformed_rows"] or any(counts.values())
    parts = (["a"] if part_a else []) + (["b"] if res["continuous_beyond_tolerance"] else [])
    if parts:
        return {**res, "outcome": 3, "outcome_3_parts": parts, "passed": False,
                "reason": outcome_3_reason(parts)}
    outcome = 2 if res["continuous_within_tolerance"] else 1
    return {**res, "outcome": outcome, "outcome_3_parts": [], "passed": True,
            "reason": PRERUN_OUTCOME_TEXT[outcome]}


PRERUN_OUTCOME_TEXT = {
    1: "every deciding column equal",
    2: "only continuous columns differ, each within MACHINE_CHECK_TOL",
    3: ("PRE-RUN TABLE NOT REPRODUCED; the real arm does not run, the table is not re-pinned, "
        "and the treatment of section 3.3 is followed")}
OUTCOME_3_PART_TEXT = {
    "a": ("(a) identity or lattice: the header, a missing, duplicated or malformed row, or an "
          "identity or lattice column differs"),
    "b": "(b) continuous: a continuous column differs beyond MACHINE_CHECK_TOL"}


def outcome_3_reason(parts, detail=None):
    """Revision 3.3 (F1): outcome 3's reason names which parts differed."""
    return (PRERUN_OUTCOME_TEXT[3] + ". What differed: "
            + "; ".join(OUTCOME_3_PART_TEXT[p] for p in parts)
            + (f" ({detail})" if detail else ""))


REPRO_LAYERS = (
    "Four layers can produce the difference; read them in this order. "
    "(1) The fits: the per-key diagnostic (raw_fits_diagnostic in synthetic_only.json), by kind "
    "(ko, full, block, ko1, sh, pc) over all 637 keys per world: p on the 64 cells, lambda, the "
    "labels and the score fields; read it first. "
    "(2) The leg-P null generator (uniform_perms, rc_patterns): the null-input digests in the "
    "manifest (null_input_digests); the pinned reference records none, so they can be compared "
    "only between runs of this code (for example the self-test below). "
    "(3) The consumer (auc_null, avg_ranks, auc, parity_D): with equal fits and equal null "
    "inputs, a difference in the null outputs or in auc or D is the consumer's. The null "
    "outputs are traced by generator, one line each, because the trace is for attribution: a "
    "difference in one column must tell which generator moved. "
    "uniform_perms (Yu) -> p_P and p_P_fixed_lambda1 (CSV columns) and smallest_passing_auc "
    "(a JSON scalar, checked by board before the fits). "
    "rc_patterns (Yrc) -> p_P_rowcol only. "
    "(4) The machine (the BLAS kernel that OpenBLAS's DYNAMIC_ARCH chooses for this CPU): what "
    "remains after (1) to (3); it cannot be separated today.")
REPRO_BRANCH = {
    "a": ("Part (a) differed (identity or lattice columns): all four layers are candidates; "
          "read (1), then (2), then (3); (4) is what remains."),
    "b": ("Part (b) differed (continuous columns beyond the tolerance): the continuous columns "
          "are functions of the fits' p (D, the log-losses) or of lattice columns (the regrown "
          "shares), and the null enters only lattice columns, by generator: uniform_perms (Yu) "
          "-> p_P and p_P_fixed_lambda1 (and the JSON scalar smallest_passing_auc); rc_patterns "
          "(Yrc) -> p_P_rowcol only. So layer (2) is not the cause; read (1), then (3); (4) is "
          "what remains."),
    "ab": ("Parts (a) and (b) both differed: read (1), then (2), then (3); (4) is what "
           "remains.")}
REPRO_SELF_TEST = (
    "The cross-configuration self-test: export OMP_NUM_THREADS, OPENBLAS_NUM_THREADS, "
    "MKL_NUM_THREADS and NUMEXPR_NUM_THREADS in the shell before launch (the script's setdefault "
    "does not override a value already set, so a naive rerun sets them to 1 again and is "
    "identical), rerun the synthetic step into a new --out folder, and compare the two runs. The "
    "code declares one BLAS thread per process, so varying the threads tests that claim, not the "
    "machine. Outcomes: (i) self-identical and still different from the pinned table: a code "
    "difference or a machine difference; they cannot be told apart today, and both are named; "
    "(ii) the rerun differs from itself: the gate itself is not self-consistent; stop and report "
    "'the reproduction gate is not self-consistent'. Either way the result goes to the chat. The "
    "pinned table is never re-pinned in answer to a red gate; a new reference is made only as "
    "section 7's 'Recreating the reference' says, with the reviewers' review and Mike's word "
    "before the real arm.")


def repro_fail_treatment(parts=("a", "b")):
    """Section 3.3 (revision 3.3: F1, item 26): the treatment of outcome 3, by its parts."""
    key = "".join(p for p in ("a", "b") if p in parts) or "ab"
    return ("If the pre-run table was not reproduced (outcome 3): do not re-pin it. "
            + REPRO_BRANCH[key] + " " + REPRO_LAYERS + " " + REPRO_SELF_TEST)


REPRO_FAIL_TREATMENT = repro_fail_treatment()                # both parts


def check_prerun_files():
    """Revision 3.2 (Ark N3): every file listed in PRERUN_DIR/SHA256SUMS.txt is read and its
    sha256 (raw bytes) must equal the listed value and PRERUN_SHA256; the list must name exactly
    the pinned files. Revision 3.3 (C6): entries of the folder that are neither listed nor
    pinned (such as the provenance/ subfolder) are reported in "unlisted", never failed."""
    sums = PRERUN_DIR / "SHA256SUMS.txt"
    if not sums.exists():
        return {"passed": False, "sums_file": str(sums), "files": {}, "unlisted": [],
                "reason": "SHA256SUMS.txt not found"}
    listed = {}
    for ln in sums.read_text(encoding="utf-8").splitlines():
        if ln.strip():
            h, name = ln.split(maxsplit=1)
            listed[name.lstrip("*")] = h
    files = {}
    for name in sorted(set(listed) | set(PRERUN_SHA256)):
        p = PRERUN_DIR / name
        files[name] = {"listed": listed.get(name), "pinned": PRERUN_SHA256.get(name),
                       "read": hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None}
    bad = [n for n, f in files.items() if not (f["read"] == f["listed"] == f["pinned"]
                                               and f["read"] is not None)]
    known = set(files) | {"SHA256SUMS.txt"}
    unlisted = [p.name + ("/" if p.is_dir() else "") for p in sorted(PRERUN_DIR.iterdir())
                if p.name not in known]
    return {"passed": not bad, "sums_file": str(sums), "files": files, "unlisted": unlisted,
            "reason": ("every listed file matches its listed and pinned sha256" if not bad
                       else "differs or missing: " + ", ".join(bad))
            + (f"; present but neither listed nor pinned (reported, not failed): "
               f"{', '.join(unlisted)}" if unlisted else "")}


def check_prerun_reproduced(got, comparable, reread=False):
    """Sections 3.3 and 7 (revisions 3.1, 3.2; Johnny, Zcode, Ark): the registered run
    recomputes the synthetic step from a clean committed tree and must reproduce the pre-run
    table, PRERUN_DIR/synthetic_worlds.csv, on its deciding columns (csv_compare; outcome 1 or 2
    passes, outcome 3 stops). Every pre-run file is first checked (check_prerun_files). Byte
    identity is recorded, not gated. passed is None when the run is not comparable (smoke, or
    starts != 10) and when the table was re-read from saved fits (--from-raw): a re-read is not a
    reproduction, and its comparison is printed for information only. False stops the two-world
    check."""
    ref_path = PRERUN_DIR / "synthetic_worlds.csv"
    base = {"prerun_path": str(ref_path), "prerun_sha256_pinned": PRERUN_WORLDS_CSV_SHA256,
            "recomputed_sha256": hashlib.sha256(got).hexdigest(),
            "reread_from_saved_fits": bool(reread), "byte_identical": None, "outcome": None}
    if not comparable:
        return {**base, "passed": None, "reason": "not comparable (smoke or starts != 10)"}
    files = check_prerun_files()
    base["prerun_files"] = files
    if not files["passed"]:
        return {**base, "passed": None if reread else False,
                "reason": "pre-run files do not match SHA256SUMS.txt and their pins: "
                          + files["reason"]}
    cmp = csv_compare(ref_path.read_bytes(), got)
    base.update(byte_identical=cmp["byte_identical"], outcome=cmp["outcome"],
                outcome_3_parts=cmp["outcome_3_parts"], comparison=cmp)
    order = {True: "differs", False: "equal"}.get(cmp["row_order_differs"], "not compared")
    detail = (f"outcome {cmp['outcome']}: {cmp['reason']}; "
              f"{'byte-identical' if cmp['byte_identical'] else 'not byte-identical'} (recorded, "
              f"not gated); rows matched by {'/'.join(CSV_KEY_COLUMNS)}: "
              f"{cmp.get('n_rows_missing_now', 0)} missing now, "
              f"{cmp.get('n_rows_missing_prerun', 0)} missing in the pre-run table, row order "
              f"{order} (a fact, not an outcome); "
              f"mechanism_description differs on {cmp['mechanism_description_differences']} rows "
              f"(reported, not gated), of which "
              f"{cmp['mechanism_description_explained_by_rename_3_2']} are exactly revision "
              f"3.2's rename and {cmp['mechanism_description_unexplained']} are not")
    if reread:
        return {**base, "passed": None,
                "reason": "re-read from saved fits (--from-raw), not a reproduction; compared "
                          "with the pre-run table for information only: " + detail}
    return {**base, "passed": cmp["passed"], "reason": detail}


def raw_fits_diagnostic(F, fresh=None, reread_note=None):
    """Revisions 3.2, 3.3 (A1, A6, A8): diagnostic, decides nothing. The fits of this run compared
    with the pinned PRERUN_DIR/raw_fits.json.gz, key by key (p_exist on the 64 block cells, the
    selected lambda, the labels, the score fields present in both records, SCORE_FIELDS, and the
    outside density; STORE_FIELDS_COMPARED), and secs and reused_from_ko excluded by name
    (STORE_FIELDS_EXCLUDED); every field seen must be declared in one of the two,
    split by the worlds that the revision-2 run fitted (30) and those that the revision-3 run
    fitted (15), and within each by kind (ko, full, block, ko1; sh for the shuffles, pc for the
    permuted-block ceilings). The ko1 fits of the revision-2 worlds were made in revision 3's pass
    (section 7). Under --from-raw, reread_note says what the comparison is, and "fitted_this_pass"
    counts the compared keys that this pass fitted (fresh): only those can carry information when
    the re-read store is the pinned one."""
    ref = read_raw(PRERUN_DIR / "raw_fits.json.gz")
    fresh = set(fresh or ())
    groups = {"revision_2_worlds": PRERUN_REV2_FAMILIES,
              "revision_3_worlds": PRERUN_REV3_FAMILIES}
    group_of = {f: g for g, fs in groups.items() for f in fs}
    out = {g: {"families": list(fs), "kinds": {}} for g, fs in groups.items()}
    counters = ("pinned", "missing_now", "compared", "fitted_this_pass", "p_differ",
                "lambda_differ", "labels_differ", "score_differ", "outside_density_differ")
    declared = set(STORE_FIELDS_COMPARED) | set(STORE_FIELDS_EXCLUDED)
    for key, v in ref.items():
        bk, mk, _ = key
        base, *mods = bk.split("|")
        if not base.startswith("world:") or base.split(":")[1] not in group_of:
            continue
        kind = mods[0].split(":")[0] if mods else mk
        s = out[group_of[base.split(":")[1]]]["kinds"].setdefault(
            kind, {**{n: 0 for n in counters}, "max_abs_dp": 0.0, "score_field_differ": {}})
        s["pinned"] += 1
        f = F.get(key)
        undeclared = (set(v) | set(f or {})) - declared
        assert not undeclared, f"undeclared store fields {sorted(undeclared)} in {key}"
        if f is None:
            s["missing_now"] += 1
            continue
        s["compared"] += 1
        s["fitted_this_pass"] += key in fresh
        p0, p1 = np.asarray(v["p"], np.float64), np.asarray(f["p"], np.float64)
        if p0.shape != p1.shape:
            s["p_differ"] += 1
            s["max_abs_dp"] = math.inf
        elif not np.array_equal(p0, p1):
            s["p_differ"] += 1
            s["max_abs_dp"] = max(s["max_abs_dp"], float(np.max(np.abs(p0 - p1))))
        s["lambda_differ"] += v.get("lam") != f.get("lam")
        s["labels_differ"] += [bool(x) for x in v["y"]] != [bool(x) for x in f["y"]]
        s0, s1 = json_safe(v.get("score") or {}), json_safe(f.get("score") or {})
        bad = [n for n in SCORE_FIELDS if n in s0 and n in s1 and s0[n] != s1[n]]
        s["score_differ"] += bool(bad)
        for n in bad:
            s["score_field_differ"][n] = s["score_field_differ"].get(n, 0) + 1
        s["outside_density_differ"] += v.get("outside_density") != f.get("outside_density")
    for g in out.values():
        k = g["kinds"].values()
        g["total"] = {n: sum(s[n] for s in k) for n in counters}
        g["total"]["max_abs_dp"] = max((s["max_abs_dp"] for s in k), default=0.0)
    return {"status": "diagnostic, decides nothing"
            + (f"; {reread_note}" if reread_note else ""), **out}


def majority(k, n):
    """Section 3.6: a majority of the worlds at one gamma (3 or more of 5)."""
    return 2 * k > n


def grid_limit(dense, key):
    """Section 3.6 (revision 3.1): the smallest dense-grid gamma at which a majority of the
    worlds count under `key`, with its bracket (the next grid gamma below it, gamma], gamma = 0
    below the first grid point; "> last" when no grid gamma has a majority."""
    grid = [r["gamma"] for r in dense]
    out = {"gamma": None, "reached": False, "grid_index": None,
           "majority_at_every_grid_gamma_above": None}
    if not grid:
        return {**out, "text": "n/a (no dense-grid world run)", "bracket_low": None,
                "bracket_text": "n/a"}
    hit = [r["gamma"] for r in dense if majority(r[key], r["n"])]
    if not hit:
        return {**out, "text": f"> {grid[-1]}", "bracket_low": grid[-1],
                "bracket_text": f"({grid[-1]}, not reached on the grid)"}
    g = min(hit)
    lo = max([x for x in grid if x < g], default=0.0)
    return {"gamma": g, "reached": True, "grid_index": grid.index(g), "text": f"{g}",
            "bracket_low": lo, "bracket_text": f"({lo}, {g}]",
            "majority_at_every_grid_gamma_above": all(majority(r[key], r["n"])
                                                      for r in dense if r["gamma"] >= g)}


def family_limit(per_pred, grid):
    """Section 3.6 (revision 3.1): the maximum over the predictors of each one's own leg-P
    limit; not reached if any predictor's limit is not reached on the grid."""
    if not grid:
        return {"gamma": None, "reached": False, "by": [], "text": "n/a (no dense-grid world run)"}
    miss = [PRED_NAME[pk] for pk, L in per_pred.items() if not L["reached"]]
    if miss:
        return {"gamma": None, "reached": False, "by": miss,
                "text": f"> {grid[-1]} (not reached on the grid by {', '.join(miss)})"}
    g = max(L["gamma"] for L in per_pred.values())
    by = [PRED_NAME[pk] for pk, L in per_pred.items() if L["gamma"] == g]
    return {"gamma": g, "reached": True, "by": by, "text": f"{g} (set by {', '.join(by)})"}


def transition_band(lp, lr, grid, u_worlds):
    """Sections 3.6 and 4 (revision 3.1): the grid gammas in [gamma*_P, gamma_R), where a
    majority passes leg P and no majority reads R. Its width in grid steps and in gamma,
    and where each dense-grid world that read U lies (below, inside, above)."""
    if not lp["reached"]:
        return {"gammas": [], "steps": None, "width_gamma": None, "open": None,
                "U_position": {"below": len(u_worlds), "inside": 0, "above": 0},
                "text": "n/a (the leg-P limit is not reached on the grid)"}
    i = lp["grid_index"]
    j = lr["grid_index"] if lr["reached"] else len(grid)
    gammas = grid[i:j]
    if lr["reached"]:
        width = round(lr["gamma"] - lp["gamma"], 10)
        text = (f"[{lp['gamma']}, {lr['gamma']}): {j - i} grid step(s), {width} in gamma"
                if j > i else "empty: the two limits coincide (0 grid steps, 0 in gamma)")
    else:
        width = None
        text = (f"[{lp['gamma']}, > {grid[-1]}): open, at least {j - i} grid step(s), more than "
                f"{round(grid[-1] - lp['gamma'], 10)} in gamma (gamma_R not reached)")

    def where(g):
        if g < lp["gamma"]:
            return "below"
        return "inside" if (not lr["reached"] or g < lr["gamma"]) else "above"

    pos = {"below": 0, "inside": 0, "above": 0}
    for g in u_worlds:
        pos[where(g)] += 1
    return {"gammas": gammas, "steps": j - i, "width_gamma": width, "open": not lr["reached"],
            "U_position": pos, "text": text}


def binomial_note(n):
    """Section 3.6 (revision 3.1, Johnny): the chance that a gamma whose true detection
    probability is p shows a majority of n worlds; with n = 5 a limit has an error of about one
    grid step."""
    k = n // 2 + 1
    tail = {p: sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))
            for p in BINOMIAL_PS}
    return {"n": n, "k": k, "tail": tail,
            "text": (f"with n = {n} worlds per gamma a limit has an error of about one grid step: "
                     f"a true detection probability of "
                     + " or ".join(f"{p}" for p in BINOMIAL_PS)
                     + f" gives '>= {k} of {n}' with probability "
                     + " or ".join(f"{tail[p]:.2f}" for p in BINOMIAL_PS) + " (Johnny)")}


def detection_limits(worlds, starts):
    """Section 3.6 (revision 3.1): the power curve and the three limits. Per gamma: n, the
    worlds seen by each predictor (p_P <= 0.01), the worlds read R, and the labels. The limits,
    each the smallest dense-grid gamma with a majority: gamma*_P (rule #2.1 seen; revision 3's
    gamma*), gamma_R (label R), and the family limit (the maximum over rule #2.1 and BF_1..BF_4
    of each one's own leg-P limit). The anchors Nf and R are printed and enter no limit."""
    rows = []
    for g, fam in sorted(DENSE_GRID + CURVE_ANCHORS):
        ws = [w for w in worlds if w["family"] == fam]
        if not ws:
            continue
        seen = {pk: sum(w["rows"][pk]["p_P"] <= P_R for w in ws) for pk in LIMIT_KEYS}
        n_r = sum(w["label"] == "R" for w in ws)
        rows.append({"gamma": g, "family": fam, "dense_grid": fam in M_FAMILIES, "n": len(ws),
                     "seen": seen["rule"], "not_seen": len(ws) - seen["rule"], "R": n_r,
                     "seen_frac": f"{seen['rule']}/{len(ws)}", "R_frac": f"{n_r}/{len(ws)}",
                     **{f"seen_{pk}": v for pk, v in seen.items()},
                     "majority_seen": majority(seen["rule"], len(ws)),
                     "majority_R": majority(n_r, len(ws)),
                     "labels": {L: sum(w["label"] == L for w in ws) for L in LABELS},
                     "rule_auc": [w["rows"]["rule"]["auc"] for w in ws],
                     "rule_lambda_ko": [w["rows"]["rule"]["lambda_ko"] for w in ws]})
    dense = [r for r in rows if r["dense_grid"]]
    grid = [r["gamma"] for r in dense]                 # the grid gammas that were run
    gamma_of = {f: g for g, f in DENSE_GRID}
    lp, lr = grid_limit(dense, "seen"), grid_limit(dense, "R")
    per = {pk: grid_limit(dense, f"seen_{pk}") for pk in LIMIT_KEYS}
    u_gammas = [gamma_of[w["family"]] for w in worlds
                if w["family"] in M_FAMILIES and w["label"] == "U"]

    def g_at_or_above(L):
        return ([] if not L["reached"] else
                [{"family": w["family"], "seed": w["seed"], "label": w["label"]}
                 for w in worlds if w["family"] in M_FAMILIES
                 and gamma_of[w["family"]] >= L["gamma"] and w["label"] == "G"])

    return {"rows": rows, "leg_P": lp, "R": lr, "per_predictor": per,
            "family": family_limit(per, grid), "band": transition_band(lp, lr, grid, u_gammas),
            "binomial_note": binomial_note(dense[0]["n"] if dense else WORLDS_PER_FAMILY),
            "curve_text": "; ".join(f"{r['gamma']}: {r['seen_frac']}, {r['R_frac']}"
                                    for r in dense),
            "grid_complete": len(dense) == len(DENSE_GRID), "instrument": instrument_text(starts),
            "G_at_or_above_leg_P": g_at_or_above(lp), "G_at_or_above_R": g_at_or_above(lr)}


def u_rule(worlds):
    """Section 3.6 (revision 3), the U rule, written before the dense grid was run: if at least
    one world on the dense grid reads U, U stays and its frequency is printed; if none does, U is
    renamed "insufficient evidence (uncalibrated)" and is never read as a finding. Revision 3.3
    (A3): the rule counts threshold U only (u_kind); a failed fit or a ceiling_block that was not
    measured is counted apart and neither keeps nor renames U."""
    dense = [w for w in worlds if w["family"] in M_FAMILIES]
    kinds = [u_kind(w.get("U_reasons")) for w in dense if w["label"] == "U"]
    n_u = len(kinds)
    n_thr, n_failed, n_nm = (kinds.count("threshold"), kinds.count("failed_fit"),
                             kinds.count("not_measured"))
    order = [f[0] for f in FAMILIES]
    fams = sorted({w["family"] for w in worlds}, key=order.index)
    freq = {f: {"U": sum(w["label"] == "U" for w in worlds if w["family"] == f),
                "n": sum(w["family"] == f for w in worlds)} for f in fams}
    split = (f"{n_thr} threshold U, {n_failed} failed fit, {n_nm} ceiling_block not measured")
    if n_thr:
        text = (f"threshold U read by {n_thr} of {len(dense)} dense-grid worlds ({split}): U "
                "stays; its frequency is printed")
    else:
        text = (f"no dense-grid world read a threshold U (0 of {len(dense)}; {split}): U is "
                f"renamed '{U_UNCALIBRATED}' and is never read as a finding")
    return {"dense_grid_worlds": len(dense), "dense_grid_U": n_u, "n_u_threshold": n_thr,
            "n_u_failed": n_failed, "n_u_not_measured": n_nm,
            "all_worlds": len(worlds), "all_U": sum(w["label"] == "U" for w in worlds),
            "frequency_by_family": freq, "renamed": n_thr == 0, "text": text}


def fixed_lambda_path_check(F, base_keys, workers, init_args):
    """The fixed-lambda diagnostic reuses a knockout fit whose selected lambda was already 1.
    That is the same computation; this checks it once. On the first bank whose five knockout
    fits (rule #2.1, BF_1..BF_4) all selected lambda = 1, the five are refitted by the
    fixed-lambda path, and each p_exist must equal the selected fit's exactly."""
    ks = ("rule",) + BF_KEYS
    for bk in base_keys:
        if all(F[(bk, "ko", pk)]["lam"] == FIXED_LAMBDA for pk in ks):
            got = run_groups([[(bk, "ko1", pk)] for pk in ks], min(workers, len(ks)), init_args,
                             "fixed-lambda path check")
            same = {pk: [float(x) for x in got[(bk, "ko1", pk)]["p"]]
                    == [float(x) for x in F[(bk, "ko", pk)]["p"]] for pk in ks}
            if not all(same.values()):
                print(f"FIXED-LAMBDA PATH DIFFERS FROM THE SELECTED FIT on {bk}: {same}",
                      flush=True)
                sys.exit(1)
            F.update(got)
            return {"bank": bk, "identical": same, "passed": True}
    return {"bank": None, "passed": None, "note": "no bank selected lambda = 1 on all five"}


def complete_fixed_lambda(F, base_keys, workers, init_args, what):
    """Section 3.5: the knockout fit at fixed lambda = 1 for rule #2.1 and BF_1..BF_4 on every
    bank. Where the selected lambda was 1, the selected fit is that fit and is reused; otherwise
    it is fitted."""
    todo, reused = [], 0
    for bk in base_keys:
        g = []
        for pk in ("rule",) + BF_KEYS:
            if (bk, "ko1", pk) in F:
                continue
            ko = F[(bk, "ko", pk)]
            if ko["lam"] == FIXED_LAMBDA:
                F[(bk, "ko1", pk)] = {**ko, "reused_from_ko": True}
                reused += 1
            else:
                g.append((bk, "ko1", pk))
        if g:
            todo.append(g)
    if todo:
        F.update(run_groups(todo, workers, init_args, what))
    return {"reused": reused, "fitted": sum(len(g) for g in todo)}


def fixed_lambda_summary(worlds):
    """Section 3.5, per family: the fixed lambda = 1 knockout AUC and p_P of rule #2.1 and each
    BF_r, beside the selected-lambda values. Diagnostic, decides nothing."""
    out = []
    for fam, *_ in FAMILIES:
        ws = [w for w in worlds if w["family"] == fam]
        if not ws:
            continue
        for pk in ("rule",) + BF_KEYS:
            a1 = [w["fixed_lambda"][pk]["auc"] for w in ws]
            p1 = [w["fixed_lambda"][pk]["p_P"] for w in ws]
            asel = [w["rows"][pk]["auc"] for w in ws]
            out.append({"family": fam, "predictor": PRED_NAME[pk], "n": len(ws),
                        "auc_lambda1": a1, "p_P_lambda1": p1,
                        "mean_auc_lambda1": float(np.mean(a1)),
                        "n_p_P_lambda1_le_0.01": sum(p <= P_R for p in p1),
                        "selected_lambda": [w["rows"][pk]["lambda_ko"] for w in ws],
                        "mean_auc_selected": float(np.mean(asel)),
                        "n_p_P_selected_le_0.01": sum(w["rows"][pk]["p_P"] <= P_R for w in ws)})
    return out


def run_synthetic(args, terms, F=None):
    """Section 7 step 3: the worlds, their legs and ceilings, each read by section 4; the three
    limits and the U rule; the pre-run reproduction and the two-world check. F, when given,
    holds saved fits (--from-raw): they are re-read, and only the fits missing from it are made.
    The caller stops on a failed requirement."""
    specs = [w for w in world_specs() if w["family"] in args.families
             and w["j"] < args.worlds_per_family]
    saved = dict(F or {})
    F = dict(saved)
    n_saved = len(F)
    init_args = (args.starts, terms, args.synthetic_only)
    groups = []
    for w in specs:
        for g in plan_bank(f"world:{w['family']}:{w['j']}", args.shuffles, args.perm_ceilings):
            g = [t for t in g if t not in F]
            if g:
                groups.append(g)
    fitted_main = sum(len(g) for g in groups)
    # Revision 3.4 (item 2): smallest_passing_auc against its registered value by board, before
    # any fit (it depends only on y and Yu). y is read from the saved store where it holds the
    # world's base knockout record (--from-raw), and otherwise from the world generator.
    spa_in = []
    for w in specs:
        bk = f"world:{w['family']}:{w['j']}"
        rec = saved.get((bk, "ko", "N1"))
        y = (rec["y"] if rec is not None
             else make_world(w, terms).exists[BLOCK_CELLS[:, 0], BLOCK_CELLS[:, 1]])
        spa_in.append({"world": bk, "board": w["board"], "y": y})
    spa = check_smallest_passing_auc(spa_in)
    log(f"smallest_passing_auc check (revision 3.4, before the fits): {spa['n_equal']} of "
        f"{spa['n_worlds']} worlds equal their registered value by board "
        f"{spa['registered_by_board']}; {spa['gates']}")
    if not spa["passed"]:
        log(f"SMALLEST PASSING AUC CHECK FAILED: {spa['mismatches']}; the synthetic step stops "
            "before any fit, and the real arm does not run (sections 3.3, 7)")
        sys.exit(1)
    if groups:
        F.update(run_groups(groups, args.workers, init_args, "synthetic worlds"))
    keys = [f"world:{w['family']}:{w['j']}" for w in specs]
    path_check = fixed_lambda_path_check(F, keys, args.workers, init_args)
    log(f"fixed-lambda path check: {path_check}")
    fl = complete_fixed_lambda(F, keys, args.workers, init_args, "fixed lambda = 1")
    # Revision 3.4 (item 3): ko1 records copied from the ko fit (reused_from_ko set) and fitted,
    # over the store this run reads; a convenience count, not a control.
    ko1 = [F[(bk, "ko1", pk)] for bk in keys for pk in ("rule",) + BF_KEYS]
    n_copied = sum(bool(r.get("reused_from_ko", False)) for r in ko1)
    n_path = len(path_check.get("identical") or {}) if path_check.get("bank") else 0
    ko1_count = {"ko1_records": len(ko1), "copied_from_ko": n_copied,
                 "fitted": len(ko1) - n_copied, "fitted_by_path_check": n_path,
                 "path_check_bank": path_check.get("bank"),
                 "this_pass": {"copied": fl["reused"], "fitted": fl["fitted"] + n_path},
                 "status": "a convenience count, not a control"}
    log(f"ko1 records (revision 3.4; a convenience count, not a control): {len(ko1)}; copied "
        f"from the ko fit (reused_from_ko) {n_copied}; fitted {len(ko1) - n_copied}, of which "
        f"{n_path} by the fixed-lambda path check ({path_check.get('bank')}); this pass copied "
        f"{fl['reused']} and fitted {fl['fitted'] + n_path}")
    worlds = []
    for w, s in zip(specs, spa["per_world"]):
        ev = evaluate_bank(f"world:{w['family']}:{w['j']}", F, args.shuffles, args.perm_ceilings)
        # revision 3.4 (item 2): the printed value is the value checked before the fits
        if ev["smallest_passing_auc"] != s["computed"]:
            log(f"SMALLEST PASSING AUC CHECK FAILED: {s['world']} printed "
                f"{ev['smallest_passing_auc']!r}, checked {s['computed']!r} before the fits")
            sys.exit(1)
        worlds.append({**w, **ev})
    dl = detection_limits(worlds, args.starts)
    ur = u_rule(worlds)
    for w in worlds:
        w["label_text"] = label_text(w["label"], dl, ur, w["U_reasons"],
                                     w["rows"]["rule"]["ceiling_block"])
        w["verdict_line"] = verdict_line(w, dl, ur)
    secs = {pk: [v["secs"] for (bk, mk, p), v in F.items() if p == pk and mk == "ko"]
            for pk in PRED_KEYS}
    comparable = (args.starts == 10 and args.worlds_per_family == WORLDS_PER_FAMILY
                  and args.shuffles == N_SHUFFLES and args.perm_ceilings == N_PERM_CEILINGS
                  and list(args.families) == [f[0] for f in FAMILIES])
    # Revision 3.2 (A3): a --from-raw pass re-reads saved fits; it is not a reproduction.
    reread = getattr(args, "from_raw", None) is not None
    repro = check_prerun_reproduced(worlds_csv_bytes(worlds), comparable, reread)
    log(f"pre-run table (section 7): {repro['reason']}; recomputed sha256 "
        f"{repro['recomputed_sha256']}")
    raw_diag = None
    if comparable and repro.get("prerun_files", {}).get("passed"):
        # revision 3.3 (A6): under --from-raw the comparison is marked for what it is
        fresh = {k for k, v in F.items() if saved.get(k) is not v}
        note = None
        if reread:
            rec = getattr(args, "from_raw_record", None) or {}
            if rec.get("sha256") == PRERUN_SHA256["raw_fits.json.gz"]:
                note = (f"re-read: compares the pinned store with itself; carries no information "
                        f"(apart from the {len(fresh)} fits this pass made, counted as "
                        f"fitted_this_pass)")
            else:
                note = ("re-read of a store other than the pinned one: compares that store's "
                        f"fits, and the {len(fresh)} fits this pass made, with the pinned ones; "
                        "not a reproduction")
        raw_diag = raw_fits_diagnostic(F, fresh, note)
        if note:
            log(f"per-fit diagnostic: {note}")
        log("per-fit diagnostic against the pre-run raw fits (decides nothing): " + "; ".join(
            f"{g}: {raw_diag[g]['total']}" for g in ("revision_2_worlds", "revision_3_worlds")))
    syn = {"worlds": worlds, "two_world_check": two_world_check(worlds, repro), "limits": dl,
           "u_rule": ur, "fixed_lambda_summary": fixed_lambda_summary(worlds),
           "fixed_lambda_path_check": path_check, "raw_fits_diagnostic": raw_diag,
           "fits": {"saved_reread": n_saved, "fitted_main": fitted_main, "fixed_lambda": fl,
                    "ko1_count": ko1_count},
           "smallest_passing_auc_check": spa,
           "mean_seconds_per_knockout_fit": {pk: float(np.mean(v)) if v else None
                                             for pk, v in secs.items()},
           # revision 3.3 (item 4): what the mean is over; a timing, not a claim about cost
           "mean_seconds_population": (
               f"every record with mask ko, per predictor: per world the base knockout fit and "
               f"the {args.shuffles} shuffled-bank knockout fits, {len(specs)} worlds, "
               f"{len(secs['N1'])} records per predictor; under --from-raw the secs saved by the "
               f"runs that made the fits; a timing, not a claim about cost")}
    return syn, F


# ------------------------------------------------------------------------------------------
# Printing (section 3.5 per bank; section 3.6 table).

def print_bank(ev, title):
    log(f"\n== {title} ==")
    log(f"outside density {ev['outside_density']:.4f}; block present {ev['block_present']}/64; "
        f"n_deg = {ev['n_deg']} of {ev['rows']['rule']['n_shuffles']}; smallest passing AUC "
        f"(p_P <= 0.01, own draws) = {fmt(ev['smallest_passing_auc'])}")
    log(f"{'predictor':10s} {'AUC':>6s} {'D':>7s} {'LL':>6s} {'LLm':>7s} {'P@32':>5s} "
        f"{'c_full':>6s} {'c_blk':>6s} {'sh_f':>5s} {'sh_b':>5s} {'M_real':>7s} {'n_ge':>4s} "
        f"{'p_S':>5s} {'p_P':>6s} {'p_Prc':>6s}  lambda ko/full/block")
    for pk in PRED_KEYS:
        r = ev["rows"][pk]
        log(f"{r['predictor']:10s} {fmt(r['auc'])} {fmt(r['D'], 3):>7s} {r['logloss']:.3f} "
            f"{r['logloss_margin_over_N1']:+.4f} {r['precision_at_32']:.3f} "
            f"{fmt(r['ceiling_full'])} {fmt(r['ceiling_block'])} "
            f"{fmt(r['regrown_share_full'], 2):>5s} {fmt(r['regrown_share_block'], 2):>5s} "
            f"{r['M_real']:+.4f} {r['n_ge']:4d} {r['p_S']:.2f} {r['p_P']:.4f} "
            f"{r['p_P_rowcol']:.4f}  {r['lambda_ko']}/{r['lambda_full']}/{r['lambda_block']}")
    log("(p_P defines leg P and the limits; p_Prc, the row-and-column p_P, is a diagnostic)")
    for pk in PRED_KEYS:
        r = ev["rows"][pk]
        log(f"  {r['predictor']:10s} quadrant mean p: " + ", ".join(
            f"{k} {v:.3f}" for k, v in r["quadrant_mean_p"].items())
            + "; mirrors: " + ", ".join(f"{k} {v:.3f}" for k, v in r["mirror_partners_p"].items())
            + f"; AUC on the other 59 = {fmt(r['auc_other_59'])}")
        log(f"  {'':10s} per-type AUC: " + ", ".join(f"{k} {fmt(v, 2)}"
                                                   for k, v in r["per_type_auc"].items()))
    if ev["perm_ceilings_full_rule"]:
        log(f"permuted-block ceiling_full of rule #2.1 ({len(ev['perm_ceilings_full_rule'])}): "
            + ", ".join(fmt(x, 3) for x in ev["perm_ceilings_full_rule"])
            + f"  (this block's ceiling_full {fmt(ev['rows']['rule']['ceiling_full'])})")
    log(f"reading A (rule #2.1): {ev['reading_A_rule']}; reading B (BF_1): {ev['reading_B_BF1']}")
    log(f"VERDICT LINE: {ev['verdict_line']}")
    if ev["U_reasons"]:
        log("U because: " + "; ".join(ev["U_reasons"]))
    log("fixed lambda = 1 on the knockout view (diagnostic, decides nothing; not on the verdict "
        "line): " + "; ".join(
            f"{v['predictor']} AUC {fmt(v['auc'])} p_P {v['p_P']:.4f} (selected lambda "
            f"{v['selected_lambda']}: AUC {fmt(v['selected_auc'])})"
            for v in ev["fixed_lambda"].values()))


def md_limits(dl):
    """Section 3.6 (revision 3.1): the three limits with the instrument, the per-predictor
    leg-P limits, the transition band with where the U worlds lie, the binomial note, and the
    M worlds that read G at or above each limit."""
    lp, lr, fam, band = dl["leg_P"], dl["R"], dl["family"], dl["band"]

    def misses(key):
        m = dl[key]
        return f"{len(m)}" + (" (" + ", ".join(f"{x['family']} {x['seed']}" for x in m) + ")"
                              if m else "")

    return [f"**The three limits** (in M-world units; instrument: {dl['instrument']}):", "",
            f"- gamma*_P, the leg-P limit (rule #2.1 p_P <= 0.01 in a majority of the worlds): "
            f"**{lp['text']}**, bracket {lp['bracket_text']}; majority seen at every grid gamma "
            f"above it: {lp['majority_at_every_grid_gamma_above']}.",
            f"- gamma_R (a majority of the worlds read R): **{lr['text']}**, bracket "
            f"{lr['bracket_text']}; majority R at every grid gamma above it: "
            f"{lr['majority_at_every_grid_gamma_above']}.",
            f"- family limit (the largest leg-P limit: the maximum of each predictor's own "
            f"leg-P limit): "
            f"**{fam['text']}**. Per predictor: "
            + ", ".join(f"{PRED_NAME[pk]} {L['text']}" for pk, L in dl["per_predictor"].items())
            + ". The limits use p_P <= 0.01 for every predictor and are not family-corrected, "
            f"unlike the W gate (p_P <= {P_W:g} = 0.05/{len(RANKS)}): a limit is a property of "
            "the instrument, not of a branch (revision 3.2).",
            f"- transition band [gamma*_P, gamma_R): {band['text']}. Dense-grid worlds that read "
            f"U: {band['U_position']['inside']} inside the band, {band['U_position']['below']} "
            f"below it, {band['U_position']['above']} above it. The band is the difference of two "
            "limits, each uncertain by about one grid step, so a one-step band is one of 0, 1 or 2 "
            "steps (revision 3.2).",
            f"- per gamma, seen/n and R/n: {dl['curve_text']}.",
            f"- binomial note: {dl['binomial_note']['text']}.",
            f"- M worlds that read G at or above gamma*_P: {misses('G_at_or_above_leg_P')}; "
            f"at or above gamma_R: {misses('G_at_or_above_R')} (printed, no stop).",
            f"- grid complete: {dl['grid_complete']}."]


def md_check_and_curve(syn):
    """Section 3.6 (revision 3.1): the requirement table, the pre-run reproduction, the power
    curve with the three limits and the instrument, the U rule, and the fixed lambda = 1
    diagnostic beside the limits."""
    c, gs, ur = syn["two_world_check"], syn["limits"], syn["u_rule"]
    rp = c["prerun_reproduction"]
    by_seed = {w["seed"]: w for w in syn["worlds"]}
    L = ["## Two-world check (section 3.6, revision 3)", "",
         "| family | seed | label | G mechanism (description only) | rule AUC | ceiling_full | "
         "ceiling_block | n_ge / n_valid | p_S | p_P | n_deg | lambda ko | code |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for row in c["rows"]:
        for p in row["worlds"]:
            r = by_seed[p["seed"]]["rows"]["rule"]
            L.append(f"| {row['family']} | {p['seed']} | {p['label']} | {p['mechanism'] or '-'} | "
                     f"{fmt(r['auc'])} | {fmt(r['ceiling_full'])} | {fmt(r['ceiling_block'])} | "
                     f"{r['n_ge']} / {r['n_valid_shuffles']} | {r['p_S']:.2f} | {r['p_P']:.4f} | "
                     f"{r['n_deg']} | {r['lambda_ko']} | {p['code']} |")
    L += ["", "| family | requirement | labels read (R/W/G/U) | meet (min) | stop labels | result |",
          "|---|---|---|---|---|---|"]
    for row in c["rows"]:
        lab = "/".join(str(row["labels"][k]) for k in LABELS)
        meet = ("n/a (power curve)" if set(row["codes"].values()) == {"curve"}
                else f"{row['n_meet']}/{row['n_worlds']} ({row['min_meet']})")
        L.append(f"| {row['family']} | {row['requirement']} | {lab} | {meet} | "
                 f"{row['n_stop_labels']} | {'STOP' if row['stops'] else 'no stop'} |")
    cmp = rp.get("comparison") or {}
    L += ["", f"Pre-run table (section 7, revisions 3.2, 3.3): {rp['reason']} (passed: "
          f"{rp['passed']}; "
          f"byte-identical: {rp['byte_identical']}; pinned {rp['prerun_sha256_pinned']}, "
          f"recomputed {rp['recomputed_sha256']}"
          + (f"; exact-column differences in {cmp['exact_differences']} rows, first: "
             f"{cmp['first_exact_differences']}" if cmp.get("exact_differences") else "")
          + (f"; continuous columns within {MACHINE_CHECK_TOL:g}: "
             f"{cmp['continuous_within_tolerance']}" if cmp.get("continuous_within_tolerance")
             else "")
          + (f"; continuous differences beyond it in {cmp['continuous_beyond_tolerance']} "
             f"cells, first: {cmp['first_continuous_beyond_tolerance']}"
             if cmp.get("continuous_beyond_tolerance") else "")
          + (f"; mechanism_description differences that are not revision 3.2's rename, "
             f"first: {cmp['first_mechanism_description_unexplained']}"
             if cmp.get("mechanism_description_unexplained") else "")
          + ").", "",
          "Per-fit diagnostic against the pre-run raw fits ("
          + (syn["raw_fits_diagnostic"]["status"] if syn.get("raw_fits_diagnostic")
             else "decides nothing") + "): "
          + (", ".join(f"{g}: {syn['raw_fits_diagnostic'][g]['total']}"
                       for g in ("revision_2_worlds", "revision_3_worlds"))
             if syn.get("raw_fits_diagnostic") else "not run") + ".", "",
          f"Two-world check passed: {c['passed']}. No contingency triggered: "
          f"{c['no_contingency']}." + (f" {NO_CONTINGENCY}" if c["no_contingency"] else ""), "",
          "## Power curve and the three limits (section 3.6, revision 3.1)", "",
          "| gamma | family | seen/n (rule #2.1 p_P <= 0.01) | R/n | seen/n BF_1, BF_2, BF_3, BF_4 "
          "| R/W/G/U | rule AUC | rule lambda ko |",
          "|---|---|---|---|---|---|---|---|"]
    for r in gs["rows"]:
        lab = "/".join(str(r["labels"][k]) for k in LABELS)
        tag = "" if r["dense_grid"] else " (anchor)"
        L.append(f"| {r['gamma']} | {r['family']}{tag} | {r['seen_frac']} | {r['R_frac']} | "
                 + ", ".join(f"{r[f'seen_{pk}']}/{r['n']}" for pk in BF_KEYS) + f" | {lab} | "
                 f"{', '.join(fmt(a, 3) for a in r['rule_auc'])} | "
                 f"{', '.join(lam_text(x) for x in r['rule_lambda_ko'])} |")
    L += [""] + md_limits(gs) + ["",
          f"**U rule:** {ur['text']}. U is read as '{U_THRESHOLD}', the signature of the leg-P "
          f"detection limit gamma*_P (revisions 3.1, 3.2), except a U whose reasons include "
          f"rule #2.1's ceiling_block below {GATE_CUT:.2f}, which reads '{FAILED_FIT_TEXT}', and "
          f"a U whose ceiling_block was not measured, which reads '{NOT_MEASURED_TEXT}' "
          f"(revision 3.3). "
          f"U across all {ur['all_worlds']} worlds: {ur['all_U']} ("
          + ", ".join(f"{f} {v['U']}/{v['n']}" for f, v in ur["frequency_by_family"].items())
          + ").", "",
          "## Fixed lambda = 1 on the knockout view (section 3.5): diagnostic, decides nothing", "",
          "Printed beside the limits, not on any verdict line. Where the selected lambda was 1 the "
          f"selected fit is reused (path check: {syn['fixed_lambda_path_check']}).", "",
          "| family | predictor | AUC at lambda 1 (per world) | mean | p_P <= 0.01 at lambda 1 | "
          "selected lambda | mean AUC selected | p_P <= 0.01 selected |",
          "|---|---|---|---|---|---|---|---|"]
    for r in syn["fixed_lambda_summary"]:
        L.append(f"| {r['family']} | {r['predictor']} | "
                 f"{', '.join(fmt(a, 3) for a in r['auc_lambda1'])} | {r['mean_auc_lambda1']:.3f} | "
                 f"{r['n_p_P_lambda1_le_0.01']}/{r['n']} | "
                 f"{', '.join(str(x) for x in r['selected_lambda'])} | "
                 f"{r['mean_auc_selected']:.3f} | {r['n_p_P_selected_le_0.01']}/{r['n']} |")
    f = syn["fits"]
    L += ["", f"Fits: {f['saved_reread']} re-read from saved fits, {f['fitted_main']} new world "
          f"fits, fixed lambda: {f['fixed_lambda']['reused']} reused, "
          f"{f['fixed_lambda']['fitted']} fitted.", ""]
    return L


def print_synthetic(syn):
    for w in syn["worlds"]:
        print_bank(w, f"world {w['family']} j={w['j']} seed={w['seed']} (gamma_z {w['gamma_z']}, "
                      f"gamma_z1 {w['gamma_z1']}, board {w['board']})")
    log("")
    for ln in md_check_and_curve(syn):
        log(ln)
    log("mean seconds per knockout fit: " + ", ".join(
        f"{PRED_NAME[k]} {fmt(v, 1)}" for k, v in syn["mean_seconds_per_knockout_fit"].items())
        + f" (population: {syn['mean_seconds_population']})")


# ------------------------------------------------------------------------------------------
# Section 7: outputs.

CSV_FIELDS = ("predictor", "auc", "D", "logloss", "logloss_margin_over_N1", "precision_at_32",
              "ceiling_full", "ceiling_block", "regrown_share_full", "regrown_share_block",
              "M_real", "n_ge", "n_shuffles", "n_deg", "n_valid_shuffles", "p_S", "p_P",
              "p_P_rowcol", "lambda_ko", "lambda_full", "lambda_block", "auc_other_59")
WORLDS_CSV_HEADER = (("family", "j", "seed", "gamma_z", "gamma_z1", "board", "label",
                      "mechanism_description", "outside_density") + CSV_FIELDS
                     + ("auc_fixed_lambda1", "p_P_fixed_lambda1"))  # 33 columns, as revision 3
# Revision 3.2 (A1): the columns of synthetic_worlds.csv by how the reproduction gate compares
# them. Exact: the identity columns of a row, and the lattice columns, whose values are exact
# dyadic or rational fractions with steps of at least 1e-4 (AUCs, p values, counts, lambdas, and
# outside_density, a count over 4,161 cells), so a tolerance adds nothing. Continuous, within
# MACHINE_CHECK_TOL: D, the log-losses, and the regrown_share ratios (not on a lattice).
# Reported, not gated: mechanism_description (column 8).
CSV_EXACT_COLUMNS = ("family", "j", "seed", "gamma_z", "gamma_z1", "board", "predictor",
                     "label", "outside_density", "auc", "precision_at_32", "ceiling_full",
                     "ceiling_block", "M_real", "n_ge", "n_shuffles", "n_deg",
                     "n_valid_shuffles", "p_S", "p_P", "p_P_rowcol", "lambda_ko", "lambda_full",
                     "lambda_block", "auc_other_59", "auc_fixed_lambda1", "p_P_fixed_lambda1")
CSV_CONTINUOUS_COLUMNS = ("D", "logloss", "logloss_margin_over_N1", "regrown_share_full",
                          "regrown_share_block")
CSV_REPORTED_COLUMNS = ("mechanism_description",)
assert (sorted(CSV_EXACT_COLUMNS + CSV_CONTINUOUS_COLUMNS + CSV_REPORTED_COLUMNS)
        == sorted(WORLDS_CSV_HEADER)) and len(WORLDS_CSV_HEADER) == 33
# Revision 3.3 (item 37): the fields of a raw_fits.json.gz record, by how raw_fits_diagnostic
# compares them, key by key (a world's base bank and its shuffled banks differ in
# outside_density, so only records of the same key are compared). Excluded by name: secs, a
# timing (the second non-reproducible field after the gzip mtime), and reused_from_ko, the flag
# of a ko1 record copied from a knockout fit that selected lambda = 1 (its p is compared).
# Revision 3.4 (item 3), the labels of the two excluded fields:
#   secs            non-reproducible (a timing).
#   reused_from_ko  derived from lam: set only on a ko1 record copied from a ko fit that selected
#                   lambda = FIXED_LAMBDA (complete_fixed_lambda); comparison redundant, since the
#                   record's p and lam are compared. The converse does not hold: the ko1 records
#                   of the fixed-lambda path check's bank are refitted there and carry no flag
#                   although their ko fit selected lambda = 1 (in the pinned store the 5 of
#                   world:W:0; 47 flagged + 5 = the 52 base ko fits of rule #2.1 and BF_r at 1).
SCORE_FIELDS = ("existence", "offset", "counts", "sign", "sign_n", "n_ne")
STORE_FIELDS_COMPARED = ("p", "y", "lam", "score", "outside_density")
STORE_FIELDS_EXCLUDED = ("secs", "reused_from_ko")
assert not set(STORE_FIELDS_COMPARED) & set(STORE_FIELDS_EXCLUDED)


def write_worlds_csv(worlds, path):
    Path(path).write_bytes(worlds_csv_bytes(worlds))


def private_run_dir(arm, head):
    """Section 7 (revision 3.1): where a registered run writes its private and raw outputs,
    outside the repository: connectome-seed-data/knockout_regrow/<arm>_<UTC stamp>_<head>."""
    return PRIVATE_ROOT / f"{arm}_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}_{head[:12]}"


def out_dir_refusal(out, arm=None):
    """Revision 3.3 (A2, C4): why --out must not be written, or None. Refused: --out with --arm
    (the real arm writes to private_run_dir and would ignore it); --out at PRERUN_DIR or inside
    it; and a folder that holds a byte copy of the reference (at least one file named like a
    pinned one is present, and every such present file matches its PRERUN_SHA256 pin). A missing
    pinned-name file is not a differing one. PRERUN_DIR and PRERUN_SHA256 are read at call time.
    Falsifier: the content guard can tell a reference copy from a fresh run's folder only because
    write_raw's raw_fits.json.gz is not byte-reproducible (gzip writes its mtime into the header);
    if write_raw becomes deterministic, this guard must be revisited (section 7)."""
    if out is None:
        return None
    if arm:
        return ("REFUSED: --out is not used with --arm; the real arm writes its private outputs "
                "to connectome-seed-data/knockout_regrow/<run> (section 7)")
    target, ref = Path(out).resolve(), Path(PRERUN_DIR).resolve()
    if target == ref or target.is_relative_to(ref):
        return (f"REFUSED: --out {target} is the pinned pre-run reference folder or inside it "
                f"({ref}); write to a new folder (section 7, 'Recreating the reference')")
    if target.is_dir():
        present = {n: hashlib.sha256((target / n).read_bytes()).hexdigest()
                   for n in PRERUN_SHA256 if (target / n).is_file()}
        if present and all(present[n] == PRERUN_SHA256[n] for n in present):
            return (f"REFUSED: --out {target} holds a byte copy of the pinned pre-run reference "
                    f"(present pinned-name files, each equal to its pin: "
                    f"{', '.join(sorted(present))}); write to a new folder "
                    "(section 7)")
    return None


def write_sha256sums(d):
    """SHA256SUMS.txt over every other file in d (raw bytes, sha256sum's binary format)."""
    d = Path(d)
    lines = [f"{hashlib.sha256(p.read_bytes()).hexdigest()} *{p.name}"
             for p in sorted(d.iterdir()) if p.is_file() and p.name != "SHA256SUMS.txt"]
    (d / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_per_shuffle_csv(ev, path):
    cols = ["sd", "present", "degenerate", "auc_N1"] + [f"{a}_{pk}" for pk in PRED_KEYS
                                                         for a in ("auc", "M", "lam")]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in ev["per_shuffle"]:
            r = json_safe(r)
            w.writerow([r[c] for c in cols])


def write_raw(F, path):
    """Every fit's p_exist and labels on the block, so that the worlds can be re-read
    (--from-raw) without refitting."""
    with gzip.open(path, "wt", encoding="utf-8") as fh:
        json.dump(json_safe({"||".join(k): v for k, v in F.items()}), fh, allow_nan=False)


def read_raw(path):
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        return {tuple(k.split("||")): v for k, v in json.load(fh).items()}


def quote_section(start_marker, end_marker):
    text = (ROOT / REGISTRATION).read_text(encoding="utf-8")
    s, e = text.index(start_marker), text.index(end_marker)
    return "\n".join(("> " + ln) if ln else ">" for ln in text[s:e].rstrip().splitlines())


def quote_row(label):
    """Section 4's table row for a label, verbatim (lesson f)."""
    key = {"R": "| **R: regrows**", "W": "| **W: rule weaker",
           "U": "| **U: on the detection threshold",
           "G": "| **G: not detected at the R level above γ_R**"}[label[0]]
    text = (ROOT / REGISTRATION).read_text(encoding="utf-8")
    return next(ln for ln in text.splitlines() if ln.startswith(key))


def md_bank_table(ev):
    L = ["| predictor | AUC (32/32) | D | log-loss | margin over N1 | P@32 | ceiling_full | "
         "ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | "
         "p_P row-col (diagnostic) | lambda ko/full/block |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for pk in PRED_KEYS:
        r = ev["rows"][pk]
        L.append(f"| {r['predictor']} | {fmt(r['auc'])} | {fmt(r['D'], 3)} | {r['logloss']:.4f} | "
                 f"{r['logloss_margin_over_N1']:+.4f} | {r['precision_at_32']:.3f} | "
                 f"{fmt(r['ceiling_full'])} | {fmt(r['ceiling_block'])} | "
                 f"{fmt(r['regrown_share_full'], 2)} | {fmt(r['regrown_share_block'], 2)} | "
                 f"{r['n_ge']} / {r['n_valid_shuffles']} | {r['p_S']:.2f} | {r['p_P']:.4f} | "
                 f"{r['p_P_rowcol']:.4f} | {r['lambda_ko']} / {r['lambda_full']} / "
                 f"{r['lambda_block']} |")
    return L


def md_synthetic(syn):
    L = md_check_and_curve(syn)
    for w in syn["worlds"]:
        L += [f"### World {w['family']}, seed {w['seed']}: {w['label_text']}", "",
              f"Outside density {w['outside_density']:.4f}; block present {w['block_present']}.",
              f"Verdict line: {w['verdict_line']}", ""] + md_bank_table(w) + [""]
    return L


def write_synthetic_outputs(out, syn, F, manifest):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "synthetic_only.json").write_text(dump_json({"manifest": manifest, **syn}),
                                             encoding="utf-8", newline="\n")
    write_worlds_csv(syn["worlds"], out / "synthetic_worlds.csv")
    write_raw(F, out / "raw_fits.json.gz")
    md = [f"# Knock out and regrow: synthetic step ({manifest['mode']})", "",
          f"Registration `{REGISTRATION}`, revision {REGISTRATION_REVISION}. "
          f"{'SMOKE RUN, NOT THE REGISTERED RUN. ' if manifest['smoke'] else ''}"
          f"git_head={manifest['git_head']}, runtime={manifest.get('runtime_s', 0):.0f}s.", ""]
    md += md_synthetic(syn)
    (out / "SYNTHETIC.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
    write_sha256sums(out)
    log(f"wrote {out}")


def write_committed(summary, syn, real):
    """Section 7: RESULT.md, summary.json, per_shuffle.csv, synthetic_worlds.csv (aggregates)."""
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(dump_json(summary), encoding="utf-8", newline="\n")
    write_per_shuffle_csv(real, OUT / "per_shuffle.csv")
    write_worlds_csv(syn["worlds"], OUT / "synthetic_worlds.csv")
    t = summary["pre_data_tables"]
    md = ["# Knock out and regrow: block A on flyvis-65", "",
          f"Registration `{REGISTRATION}`, revision {REGISTRATION_REVISION}. "
          f"git_head={summary['manifest']['git_head']}, runtime={summary['runtime_s']:.0f}s.", "",
          f"**Verdict: {real['verdict_line']}**", "",
          "The section 4 row, verbatim:", "", "> " + quote_row(real["label"]), "",
          WITHIN_FLY_NOTE + ".", "",
          "## Section 3.5 (flyvis-65, the real block)", ""] + md_bank_table(real)
    md += ["", "Permuted-block ceiling_full of rule #2.1: "
           + ", ".join(fmt(x, 3) for x in real["perm_ceilings_full_rule"])
           + f" (real block {fmt(real['rows']['rule']['ceiling_full'])}).", "",
           "Per-type AUC, mirrors, quadrant means and the D7 fields are in summary.json.", "",
           f"The limits: {limits_text(syn['limits'])}. Binomial note: "
           f"{syn['limits']['binomial_note']['text']}. Private and raw outputs: "
           f"{summary['manifest']['private_outputs']}.", "",
           "Fixed lambda = 1 on the knockout view, diagnostic, decides nothing: " + "; ".join(
               f"{v['predictor']} AUC {fmt(v['auc'])}, p_P {v['p_P']:.4f}"
               for v in real["fixed_lambda"].values()) + ".", "",
           "## Pre-data tables (section 1.4)", "",
           "| endpoint | kept (as in section 1.4) |", "|---|---|"]
    md += [f"| {k} | {v} |" for k, v in t["endpoints"].items()]
    md += ["", f"Inferable block cells: {t['inferable']} / 64. Mirror cells: {t['mirrors']}. "
           f"Training present cells: {t['training_present']} of {N_TRAIN_CELLS}.", ""]
    md += [f"- {b}: {v} ({s})" for b, v, s in INFERABILITY_PROVENANCE]
    md += [""] + md_synthetic(syn)
    md += ["## The registered reading (section 4, quoted)", "",
           quote_section("## 4. Reading rule", "## 5. What each outcome means"), ""]
    (OUT / "RESULT.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
    log(f"wrote {OUT}")


# ------------------------------------------------------------------------------------------

def machine_checks_real(a, terms, checks):
    """Section 3.4 checks 5, 6, 8, 9 (real arm only; check 3 runs before them)."""
    n1_ko = H.fit_n1(H.make_view(H.REAL, MASKS["ko"]))
    checks["5_n1_parity"] = check_n1_parity(
        n1_ko, H.REAL.exists[BLOCK_CELLS[:, 0], BLOCK_CELLS[:, 1]])
    log(f"check 5 (N1 parity): passed; D = {checks['5_n1_parity']['D_N1_logit']:.2e}")
    groups = ([[("real", "ko#hash#0", "rule")], [("real", "ko#hash#1", "rule")],
               [("real|leak", "ko#hash#0", "rule")]]
              + [[("real", f"cv:{f}", pk)] for pk in ("BF:1", "N1") for f in range(H.N_FOLDS)])
    det = run_groups(groups, a.workers, (a.starts, terms, False), "checks 6, 8, 9")
    h0 = det[("real", "ko#hash#0", "rule")]["data_sha256"]
    h1 = det[("real", "ko#hash#1", "rule")]["data_sha256"]
    hl = det[("real|leak", "ko#hash#0", "rule")]["data_sha256"]
    if h0 != hl:
        print("BLOCK LEAKS INTO TRAINING", flush=True)
        sys.exit(1)
    checks["6_leakage"] = {"knockout_sha256": h0, "permuted_block_knockout_sha256": hl,
                           "passed": True}
    bf = [det[("real", f"cv:{f}", "BF:1")]["score"] for f in range(H.N_FOLDS)]
    n1s = [det[("real", f"cv:{f}", "N1")]["score"] for f in range(H.N_FOLDS)]
    m = H.margin(bf, n1s, "existence")
    if abs(m - BF1_FULL_BANK_MARGIN) > IDENTITY_TOL:
        print(f"HARNESS IDENTITY FAILS: BF_1 margin {m!r}, registered {BF1_FULL_BANK_MARGIN!r}",
              flush=True)
        sys.exit(1)
    checks["8_harness_identity"] = {"BF1_margin": m, "registered": BF1_FULL_BANK_MARGIN,
                                    "difference": m - BF1_FULL_BANK_MARGIN, "passed": True}
    if h0 != h1:
        print("NOT DETERMINISTIC", flush=True)
        sys.exit(1)
    checks["9_determinism"] = {"sha256_fit_1": h0, "sha256_fit_2": h1, "passed": True}
    log("checks 6 (leakage), 8 (harness identity), 9 (determinism): passed")


def main():
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--synthetic-only", action="store_true",
                      help="steps 1-3 only; touches no real block cell")
    mode.add_argument("--arm", choices=["flyvis65"])
    ap.add_argument("--starts", type=int, choices=[3, 10], default=10)
    ap.add_argument("--workers", type=int, default=30)
    ap.add_argument("--out", default=None, help="with --synthetic-only: where to write")
    ap.add_argument("--allow-dirty", action="store_true",
                    help="real arm: not the registered run; recorded in the manifest")
    ap.add_argument("--from-raw", default=None,
                    help="with --synthetic-only: re-read an earlier run's raw_fits.json.gz and "
                         "fit only what it lacks (new worlds, fixed-lambda fits)")
    ap.add_argument("--smoke-worlds", type=int, default=None, help="worlds per family (smoke)")
    ap.add_argument("--smoke-shuffles", type=int, default=None, help="shuffles per bank (smoke)")
    ap.add_argument("--smoke-perm-ceilings", type=int, default=None)
    ap.add_argument("--smoke-families", default=None, help="comma-separated subset (smoke)")
    a = ap.parse_args()
    t0 = time.time()
    a.worlds_per_family = a.smoke_worlds if a.smoke_worlds is not None else WORLDS_PER_FAMILY
    a.shuffles = a.smoke_shuffles if a.smoke_shuffles is not None else N_SHUFFLES
    a.perm_ceilings = (a.smoke_perm_ceilings if a.smoke_perm_ceilings is not None
                       else N_PERM_CEILINGS)
    a.families = a.smoke_families.split(",") if a.smoke_families else [f[0] for f in FAMILIES]
    smoke = (a.worlds_per_family != WORLDS_PER_FAMILY or a.shuffles != N_SHUFFLES
             or a.perm_ceilings != N_PERM_CEILINGS or len(a.families) != len(FAMILIES))
    if a.arm and (smoke or a.from_raw or a.starts != 10):
        sys.exit("REFUSED: the real arm runs as registered: --starts 10, no smoke option, no "
                 "--from-raw (sections 3.3, 7)")
    # Revision 3.3 (A2, C4): before any write or mkdir, --out is refused at or inside the pinned
    # reference folder, on a byte copy of it, and with --arm.
    refusal = out_dir_refusal(a.out, a.arm)
    if refusal:
        sys.exit(refusal)
    H.STARTS = a.starts

    # Step 1: refusals and pins. --synthetic-only is run before commit (D11), so it records the
    # tree state instead of refusing.
    if a.arm:
        dirty = refuse_if_dirty(a.allow_dirty)
    else:
        dirty = git("status", "--porcelain", "--", "results/genome/c6", "docs/plans")
    pins = check_pins()
    log(f"registration: {REGISTRATION}, revision {REGISTRATION_REVISION}; "
        f"{'SYNTHETIC ONLY' if a.synthetic_only else 'arm ' + a.arm}"
        f"{'; SMOKE, not the registered run' if smoke else ''}; k = {a.starts}; "
        f"workers = {a.workers}; CPU (the pinned harness is numpy-only, section 7)")
    log(f"check 1 (pins, versions, rule #2.1 RANK = 1): passed; Python {pins['python']}, "
        f"numpy {pins['numpy']}")

    # Step 2: machine checks (section 3.4). Checks 3, 5, 6, 8 and 9 read the real block or fit a
    # rule on the real bank, so they run in the real arm only.
    checks = {"1_pins": pins, "2_block_and_mask": check_block_and_mask()}
    log(f"check 2 (block and mask): passed; {N_TRAIN_CELLS} training cells, 64 block cells")
    if a.arm:
        checks["3_board"] = check_board(H.REAL)
        log(f"check 3 (board as reviewed): passed; {checks['3_board']['quadrants']}")
    tables = pre_data_tables(H.REAL)                   # outside-block presence only
    checks["4_pre_data_tables"] = check_pre_data_tables(tables)
    log(f"check 4 (pre-data tables of section 1.4): passed; inferable {tables['inferable']}/64, "
        f"mirrors {tables['mirrors']}, training present {tables['training_present']}")
    checks["7_auc_function"] = check_auc_function()
    log("check 7 (AUC function on hand-made inputs): passed")
    seeds = assert_seeds_unique(a.starts)
    log(f"seeds (section 3.7): {seeds}")
    terms = degree_terms()
    log(f"section 3.6 degree terms: N1 (c, a, b) fitted on the real knockout view "
        f"({N_TRAIN_CELLS} outside-block cells; no block cell read); c = {terms[0]:+.4f}, "
        f"a in [{terms[1].min():+.3f}, {terms[1].max():+.3f}], "
        f"b in [{terms[2].min():+.3f}, {terms[2].max():+.3f}]")
    if a.arm:
        machine_checks_real(a, terms, checks)

    # Revision 3.3 (B6): the --from-raw file with its sha256 and whether it exists.
    a.from_raw_record = None
    if a.from_raw:
        fr = Path(a.from_raw)
        a.from_raw_record = {"path": str(fr), "exists": fr.is_file(),
                             "sha256": (hashlib.sha256(fr.read_bytes()).hexdigest()
                                        if fr.is_file() else None)}
        a.from_raw_record["is_the_pinned_store"] = (a.from_raw_record["sha256"]
                                                    == PRERUN_SHA256["raw_fits.json.gz"])
    head = git("rev-parse", "HEAD")
    private = private_run_dir(a.arm, head) if a.arm else (Path(a.out) if a.out else None)
    manifest = {"registration": REGISTRATION, "revision": REGISTRATION_REVISION,
                "registration_sha256_lf": sha256_lf(ROOT / REGISTRATION),
                "script_sha256_lf": sha256_lf(Path(__file__)), "git_head": head,
                "tree_dirty_under_c6_or_plans": bool(dirty),
                "tree_dirty_paths": dirty.splitlines() if dirty else [],
                "allow_dirty": bool(a.allow_dirty),
                "not_the_registered_run": (NOT_REGISTERED_TEXT if a.arm and a.allow_dirty
                                           else None),
                "mode": "synthetic-only" if a.synthetic_only else a.arm, "smoke": smoke,
                "worlds_per_family": a.worlds_per_family, "shuffles": a.shuffles,
                "perm_ceilings": a.perm_ceilings, "families": a.families, "starts": a.starts,
                "workers": a.workers, "python": pins["python"], "numpy": pins["numpy"],
                "device": "CPU", "from_raw": a.from_raw, "from_raw_record": a.from_raw_record,
                "private_outputs": str(private) if private else None,
                "prerun_dir": str(PRERUN_DIR),
                "prerun_worlds_csv_sha256": PRERUN_WORLDS_CSV_SHA256,
                "prerun_sha256": PRERUN_SHA256, "machine_record": machine_record(),
                "degree_terms": {"c": terms[0], "a": terms[1], "b": terms[2],
                                 "source": "N1 on the real knockout view (outside-block cells)"}}

    # Step 3: the synthetic worlds, the pre-run reproduction and the two-world check (3.6, 7).
    syn, F = run_synthetic(a, terms, read_raw(a.from_raw) if a.from_raw else None)
    print_synthetic(syn)
    rp = syn["two_world_check"]["prerun_reproduction"]
    # Revision 3.2 (A1): byte identity with the pre-run table is a recorded fact, not the gate.
    manifest["prerun_csv_byte_identical"] = rp["byte_identical"]
    manifest["prerun_comparison_outcome"] = rp["outcome"]
    manifest["prerun_reread_from_saved_fits"] = rp["reread_from_saved_fits"]
    manifest["prerun_comparison_outcome_3_parts"] = rp.get("outcome_3_parts")
    manifest["null_input_digests"] = null_input_digests()      # revision 3.3 (F10)
    log(f"null-input digests (revision 3.3): {manifest['null_input_digests']}")
    log(f"machine record (revision 3.2): thread variables "
        f"{manifest['machine_record']['thread_env']}; machine "
        f"{manifest['machine_record']['machine']}")
    manifest["runtime_s"] = time.time() - t0
    treatment = (repro_fail_treatment(rp.get("outcome_3_parts") or ("a", "b"))
                 if rp["passed"] is False else "")
    if a.arm:                                          # section 7: private and raw, before step 4
        write_synthetic_outputs(private, {**syn, "checks": checks, "seeds": seeds}, F, manifest)
    if a.synthetic_only:
        if a.out:
            write_synthetic_outputs(a.out, {**syn, "checks": checks, "seeds": seeds}, F, manifest)
        if not syn["two_world_check"]["passed"]:
            log("TWO-WORLD CHECK FAILED: a requirement marked stop failed, or the pre-run table "
                "was not reproduced (outcome 3); the real arm does not run (sections 3.6, 7). "
                + treatment)
            sys.exit(1)
        log(f"\n--synthetic-only: stopped before any real block score. {time.time() - t0:.0f}s")
        return
    if not syn["two_world_check"]["passed"]:
        log("TWO-WORLD CHECK FAILED: a requirement marked stop failed, or the pre-run table was "
            "not reproduced (outcome 3); the real arm does not run (sections 3.6, 7). No real "
            f"block score was computed. Private outputs: {private}. " + treatment)
        sys.exit(1)

    # Step 4: the real arm.
    Fr = run_groups(plan_bank("real", N_SHUFFLES, N_PERM_CEILINGS), a.workers,
                    (a.starts, terms, False), "real arm")
    complete_fixed_lambda(Fr, ["real"], a.workers, (a.starts, terms, False),
                          "real arm, fixed lambda = 1 (diagnostic)")
    real = evaluate_bank("real", Fr, N_SHUFFLES, N_PERM_CEILINGS)
    real["label_text"] = label_text(real["label"], syn["limits"], syn["u_rule"],
                                    real["U_reasons"], real["rows"]["rule"]["ceiling_block"])
    real["verdict_line"] = verdict_line(real, syn["limits"], syn["u_rule"],
                                        syn["two_world_check"]["no_contingency"],
                                        manifest["not_the_registered_run"])
    manifest["null_input_digests"] = null_input_digests()      # now with the real block's y
    write_raw(Fr, private / "raw_fits_real.json.gz")
    write_sha256sums(private)
    log(f"wrote {private}")

    # Step 5: the verdict, section 3.5, outputs.
    print_bank(real, "flyvis-65, the real block (section 3.5)")
    log(WITHIN_FLY_NOTE)
    log(f"\nVERDICT: {real['verdict_line']}")
    summary = {"manifest": manifest, "checks": checks, "seeds": seeds, "pre_data_tables": tables,
               "inferability_provenance": INFERABILITY_PROVENANCE, "real": real,
               "synthetic": syn, "runtime_s": time.time() - t0}
    write_committed(summary, syn, real)
    log(f"wall-clock {summary['runtime_s']:.0f}s")


if __name__ == "__main__":
    main()
