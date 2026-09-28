#!/usr/bin/env python3
"""Knock out and regrow, block B on flyvis-65: L1-L5 x the eight motion-pathway inputs (40 cells).

Implements docs/plans/2026-09-25-knockout-regrow-block-b-registration.md, revision 1.7.3 ("B";
section numbers below refer to it unless marked "A"), a delta on block A's registration
docs/plans/2026-09-24-knockout-regrow-registration.md, revision 3.4.1 with its Amendment 1 ("A").
This file is a copy of A's script results/genome/c6/checks/knockout_regrow.py (D13 (i)) with the
script changes S1-S40 of B section 7, and is reviewed as a diff against it; A's script, the male
CNS arm's script and the pinned harness are not edited. Each change is marked "S<n>" where it is
made. Forms taken from the male CNS arm's script (results/genome/c6/checks/
knockout_regrow_male_cns.py, LF sha256 290ecb56... at 01d2d05) are ported by name, each marked
"# port: male <function/line> -> S<nn>" (B section 7, "The plan of the port"); the male world
(8 x 8 blocks, two lobes, the seal) is not imported. Male S-numbers are never reused: a port of a
male requirement is marked "(the male arm's SNN)".

A's revision history (3 to 3.4.1) is in A's script and applies to this copy; what differs from
A, in one paragraph: the block is B's 40 cells (S3); its present count is printed, not checked
(D3 (ii); S8); check 5 is a print (D6; S9); the section 1.4 table is registered by its hash
(D2 (ii); S6); the worlds are rebuilt on block B's knockout view with B's planted boards (D4,
D5; S14); new seeds 91000-91999 (S13); the row-and-column null has a (5, 8) shape, an attempt
cap and a stop record (D7; S12, S39); a block on which leg P cannot pass reads the "not readable"
U (S38); p_S carries a mark when n_deg >= 1 (S36); the pre-run's provenance is checked (S37);
and the output path is hardened: UTF-8 streams (S23), a log that cannot kill a run (S24), fits
and verdict lines on disk before any print (S25), the command's environment in the manifest
(S28), SHA256SUMS.txt written last (S29), earlier real-arm runs found at run time (S27), and a
full --synthetic-only run refused on a dirty tree unless --allow-dirty (S40).

    tools/.venv/Scripts/python.exe results/genome/c6/checks/knockout_regrow_block_b.py --synthetic-only --starts 10 --workers 30 --out <new folder>
    tools/.venv/Scripts/python.exe results/genome/c6/checks/knockout_regrow_block_b.py --arm flyvis65_blockB --starts 10 --workers 30

(Both with PYTHONUTF8=1 when the output is redirected; B section 7.) The run commands are pinned in
the revision after the pre-run (B section 7). --synthetic-only never builds, fits or scores a bank
that holds the real block and fits no rule on the real bank. From the real bank it reads only
what B section 3.6 allows before data: N1's degree terms fitted on block B's knockout view, the
content of the present cells outside block B, and (for the section 1.4 table) presence outside
block B. While PRERUN_SHA256 is a placeholder (None; D10 (i)) it runs in pre-run mode: it makes
block B's reference and checks none. Machine checks 3, 5, 6, 8 and 9 run in the real arm only.
Without --out it writes nothing. CPU only: the pinned numpy harness (D12 (i)).
"""
# S23 (UTF-8 at the top): before any other statement that can print, stdout and stderr are
# reconfigured to UTF-8 with backslashreplace, so that a console or a redirect in cp1252 or ASCII
# cannot kill a run on a character such as gamma (the male arm's run 1, B section 7, S23). The
# encodings found before the change are recorded for the manifest (S28).
import sys
STREAM_ENCODING_FOUND = {"stdout": getattr(sys.stdout, "encoding", None),
                         "stderr": getattr(sys.stderr, "encoding", None)}


def utf8_streams():
    """S23: sys.stdout and sys.stderr as UTF-8 with backslashreplace; a stream that cannot be
    reconfigured (no reconfigure method, or a detached buffer) is left as it is."""
    for name in ("stdout", "stderr"):
        s = getattr(sys, name)
        try:
            s.reconfigure(encoding="utf-8", errors="backslashreplace")
        except (AttributeError, ValueError, OSError):
            pass


utf8_streams()
import os
THREAD_VARS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")
# Revision 3.2 (A4): the values found in the environment before setdefault, which does not
# override a value already set; the manifest records them beside the values in effect.
THREAD_ENV_FOUND = {_v: os.environ.get(_v) for _v in THREAD_VARS}
# S28: the command's environment as found at import, for the manifest (command_environment).
COMMAND_ENV_VARS = ("PYTHONUTF8", "PYTHONIOENCODING", "PYTHONHASHSEED")
COMMAND_ENV_FOUND = {_v: os.environ.get(_v) for _v in COMMAND_ENV_VARS}
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
import re
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
C6 = HERE.parent
ROOT = C6.parents[2]                                   # the repository root
# S2: this file's registration and revision; the manifest records its LF sha256 at run time.
REGISTRATION = "docs/plans/2026-09-25-knockout-regrow-block-b-registration.md"
REGISTRATION_REVISION = "1.7.3"
# S2: A's registration, from which quote_row and quote_section quote section 4 (B section 4 does
# not restate it). Pinned after A's Amendment 1 and checked at run start in every mode
# (check_pins); an Amendment 2 of A stops the run on this pin, read as "A changed", not as a
# defect of the environment (revision 1.3).
# port: male A_REGISTRATION, A_REGISTRATION_SHA256_LF_AMENDED (lines 73-75) -> S2
A_REGISTRATION = "docs/plans/2026-09-24-knockout-regrow-registration.md"
A_REGISTRATION_SHA256_LF_AMENDED = (
    "fc41505690365ff6d82fa618b00b482cc992bb36d708ed3b6fbbe6f54f96dbec")
# The text under which block A's flyvis-65 verdict was made (revision 3.4.1, commit 74db080):
# informational, recorded, not checked (B header).
# port: male A_REGISTRATION_SHA256_LF_FLYVIS65 (lines 78-79) -> S2
A_REGISTRATION_SHA256_LF_FLYVIS65 = (
    "409184dead0a8f9b971bd4b480043725d4a0d1a3c53c20c35734a944a63facd6")
OUT = HERE / "knockout_regrow_block_b"                 # S19: committed, aggregates only
RULE_PATH = C6 / "rules" / "second_rule_v21" / "fit.py"
# Section 7: private and raw outputs live outside the repository. The registered run writes them
# to PRIVATE_ROOT / "<arm>_<UTC stamp>_<git head, 12>" (private_run_dir).
PRIVATE_ROOT = ROOT.parent / "connectome-seed-data" / "knockout_regrow"
# S17 (sections 3.3, 7; D10 (i)): block B's own pre-run reference, a new folder, made by one
# --synthetic-only run from a committed head on Mike's word. Its pins are set, with
# PRERUN_GIT_HEAD and PRERUN_SCRIPT_SHA256_LF (S37), by the revision after the pre-run (B 1.7),
# in one reviewed change. While PRERUN_SHA256 is None, --synthetic-only runs in pre-run mode (it
# makes the reference and checks none) and the real arm refuses. Each pin is the sha256 of a
# file's raw bytes (read_bytes(), .gz included): integrity, not reproducibility; what a rerun must
# reproduce is carried by the column gate (csv_compare). A red pin is never answered by re-pinning
# (A section 7, "Recreating the reference"). A's revision-2/3 split of its pre-run and revision
# 3.2's rename check (_mech_renamed_32) are A's history and are not carried over.
# port: male PRERUN_DIR / PRERUN_SHA256 placeholders, reference_mode (lines 86-116, 2068-2071)
# -> S17
# B revision 1.7 (D10 (i), step (4)): the pre-run was made on Mike's word (2026-09-27, 21:10:52 to
# 23:23:00 UTC) from clean master 5f9cc51 into a new stamped folder; PRERUN_DIR and the pins move
# to it together, here. The path revisions 1-1.6.1 named (".../synthetic_blockB_prerun") was never
# written into and is no longer a reference. Every pin below was recomputed from the folder's
# files (sha256sum on raw bytes) and equals its line of the folder's SHA256SUMS.txt, which lists
# exactly these five files (B section 10, "Revision 1.7").
PRERUN_DIR = PRIVATE_ROOT / "synthetic_blockB_prerun_20260927T211052Z_5f9cc51b9a24"
PRERUN_SHA256 = {                                      # {file name: raw sha256}; D10 (i)
    "SYNTHETIC.md": "685c5e1fb8ead1d12a3f2f781b314b581671b44f5ce883f33428cf2be47ac7bf",
    "raw_fits.json.gz": "5d08f6e697c3c06182bbe5e18543fb8838575d0ea8a0b5f0bee0f97b9fb0dbd5",
    "stdout.log": "aea98de00476b80d65132118ff4b4fcff774953dce4971e270d1950cc33e490f",
    "synthetic_only.json": "f77fd8445b51eee4067c59b319b72b0ebc9a85a315ed9dd7c79b480fb97a85d9",
    "synthetic_worlds.csv": "2187ce8983a840417f68aafe4f2678f139d77aecbc5a349cb1aa97a9b8740dcb"}
PRERUN_WORLDS_CSV_SHA256 = PRERUN_SHA256["synthetic_worlds.csv"]
# S37 (the male arm's S30): the head and the LF sha256 of the script that WROTE the reference
# (read from the reference's synthetic_only.json manifest after check_prerun_files passes). The
# script that reads the reference is intentionally another one (the revision after the pre-run
# writes PRERUN_* into it), so its own hash differs by design and is not a mismatch.
# port: male PRERUN_GIT_HEAD, PRERUN_SCRIPT_SHA256_LF (lines 118-127) -> S37
# B revision 1.7: read from the reference's synthetic_only.json manifest (git_head,
# script_sha256_lf) and recomputed with `git show 5f9cc51:<this file> | tr -d '\r' | sha256sum`.
PRERUN_GIT_HEAD = "5f9cc51b9a247514870ea2af518cdb41b0e4cacf"
PRERUN_SCRIPT_SHA256_LF = "2bb92b433565de50aea4db5e4235a3a964b0fa776a5e957c470af63fb27abe69"
# S18: the other references, which --out must never touch: A's and the two male references,
# each guarded by its path and recognised as a byte copy by its pins; block B's own (PRERUN_DIR)
# was guarded by its path only until its pins existed; from B revision 1.7 it is guarded by both.
# port: male A_PRERUN_DIR, A_PRERUN_SHA256, PRERUN_DIR, PRERUN_SHA256 (lines 97-137) -> S18
A_PRERUN_DIR = PRIVATE_ROOT / "synthetic_rev3_prerun"
A_PRERUN_SHA256 = {
    "SYNTHETIC.md": "4526d2239c6bf378b161b7fb92bab2c022b0ac648a88fcda8fa02f86f9e58264",
    "raw_fits.json.gz": "91035af838446b86bda502fe8bf719910550bbad72c1cb12563800a984819e60",
    "rev2_full.log": "fa5606e37ebcb8e7b4aac69ba592638e3f77cfea9cbff58b639be2ee8ea960d0",
    "synthetic_only.json": "ea812dfd87238a4a23ca54e06faf5c1d93c7802a36ee28eff9857183236377dd",
    "synthetic_worlds.csv": "7a2f02953207f8aacb1cbd8c5e61e7731135d5a6f800a40b359cb0ff12f9c8f1"}
MALE_PRERUN_DIR = {"L": PRIVATE_ROOT / "synthetic_malecns_L_prerun",
                   "R": PRIVATE_ROOT / "synthetic_malecns_R_prerun"}
MALE_PRERUN_SHA256 = {
    "L": {"SYNTHETIC.md": "97797a5120eab60bdf7c5ea94aaeb5835430f54a3af9c2e27c12b0d81741363f",
          "raw_fits.json.gz": "e0e1114d9c7fc6bcb316a131aaea572b426ef46e6f1c4f8786fdb63d2783dad2",
          "synthetic_only.json":
              "9498de82d33444ff98e090b2cff895d2ab760f433fbf41d22e12e9b67b61f649",
          "synthetic_worlds.csv":
              "506576312638005e5bd09876c9da0ffe9a8a753641a59a2b354c0c59bed25d91"},
    "R": {"SYNTHETIC.md": "6f4b94b1c9096b45a8532395a2e45f47b5484663431d66532548d68db4753e84",
          "raw_fits.json.gz": "183b9376315dd98bb421015fb721d941cddf2dd1949f96be82055d1f4c5acade",
          "synthetic_only.json":
              "8acf217d77fbe21d29561f47cc33373769e74f3cc50150def97eca4f6b49f219",
          "synthetic_worlds.csv":
              "e8476a936356d3965aa5715d7f04a82c3587ff0795569db81071822fbca9cae0"}}

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


def real_bank():
    """The real bank, flyvis-65 (H.REAL). Every use of the real bank goes through this function,
    so that the tests can put a fixture bank in its place (B section 7: no test reads block B's
    cells of the real bank)."""
    return H.REAL


# ------------------------------------------------------------------------------------------
# Section 1.2 (S3): block B, L1-L5 x block A's eight sources. The targets' ON/OFF split and the
# answer key are used only to score and to print strata, never to train. Block cell order:
# SOURCES x TARGETS, row-major; leg P's permutations index this order. A's X_SIGN, W_SIGN and
# BOARD are removed: block B has no reviewed board (D3).
SOURCES = ("L1", "L2", "L3", "L4", "L5")
ON, OFF = ("Mi1", "Tm3", "Mi4", "Mi9"), ("Tm1", "Tm2", "Tm4", "Tm9")   # the targets' split
TARGETS = ON + OFF
# The answer key of section 1.2 (candidates note section 2B), present by the key. Not stated in
# any file opened for the registration: L4's and L5's targets, and whether L1 -> OFF and L2 -> ON
# are absent. It enters no computation; it is printed.
ANSWER_KEY_PRESENT = (("L1", "Mi1"), ("L1", "Tm3"), ("L2", "Tm1"), ("L2", "Tm2"), ("L2", "Tm4"),
                      ("L3", "Mi9"), ("L3", "Tm9"))
BLOCK_NAMES = [(s, t) for s in SOURCES for t in TARGETS]
BLOCK_CELLS = np.array([(H.IDX[s], H.IDX[t]) for s, t in BLOCK_NAMES], dtype=np.int64)
BLOCK = np.zeros((65, 65), bool)
BLOCK[BLOCK_CELLS[:, 0], BLOCK_CELLS[:, 1]] = True
N_BLOCK = 40
N_SOURCES, N_TARGETS = len(SOURCES), len(TARGETS)      # the (5, 8) shape of the block
# Check 2's addition: block A's 64 cells, ordinary training cells here.
BLOCK_A_SOURCES = ON + OFF
BLOCK_A_TARGETS = ("T4a", "T4b", "T4c", "T4d", "T5a", "T5b", "T5c", "T5d")
BLOCK_A = np.zeros((65, 65), bool)
for _s in BLOCK_A_SOURCES:
    for _t in BLOCK_A_TARGETS:
        BLOCK_A[H.IDX[_s], H.IDX[_t]] = True
# S4 (section 3.1): the six strata, source type x the targets' ON/OFF split of the key (in place
# of A's four quadrants); {L3, L4, L5} is not a polarity claim.
L345 = ("L3", "L4", "L5")
STRATA = {name: [i for i, (s, t) in enumerate(BLOCK_NAMES) if s in src and t in tar]
          for name, src, tar in (("L1 x ON", ("L1",), ON), ("L1 x OFF", ("L1",), OFF),
                                 ("L2 x ON", ("L2",), ON), ("L2 x OFF", ("L2",), OFF),
                                 ("L3-L5 x ON", L345, ON), ("L3-L5 x OFF", L345, OFF))}
assert sorted(i for v in STRATA.values() for i in v) == list(range(N_BLOCK))
MASKS = {"ko": ~BLOCK, "full": np.ones((65, 65), bool), "block": BLOCK.copy()}

# Section 1.3 (S5): what is removed. The training present count is not registered (D3): the real
# arm prints it at run start.
N_TRAIN_CELLS = 65 * 65 - N_BLOCK                      # 4,185

# Section 1.4 (S6; D2 (ii)): the endpoint table is registered by its hash, in the canonical form
# of section 1.4 ("The canonical form, exactly"); 40 / 40 inferable; the 9 mirrors (target,
# source), present. A's FlyWire-30 and male-CNS provenance rows are removed.
ENDPOINTS_SHA256 = "aa0920288e6d38230c6a275c1690614120fdaf9104476264d42208ecf04f7705"
INFERABLE_MIN = 2                                      # Johnny's rule: >= 2 on both endpoints
INFERABLE_EXPECTED = 40
MIRRORS_EXPECTED = {("Mi1", "L1"), ("Mi1", "L5"), ("Mi4", "L2"), ("Mi9", "L3"), ("Tm1", "L2"),
                    ("Tm1", "L5"), ("Tm2", "L2"), ("Tm2", "L5"), ("Tm3", "L1")}
MIRROR_IDX = sorted(BLOCK_NAMES.index((s, t)) for (t, s) in MIRRORS_EXPECTED)
N_OTHER_CELLS = N_BLOCK - len(MIRRORS_EXPECTED)        # S15: "the other 31 cells"

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
# port: male TAU comment, the lattice text made generic (lines 321-327; the male arm's S24) -> S21
# S21: 1e-9, the harness's tie band (revision 3.2, section 3.2), inert (B section 3.2): with
# n_p present of N_BLOCK, every AUC is a multiple of 1/(2 n_p n_a), 2 n_p n_a <= 800 on block B,
# so two unequal values on these lattices differ by at least 1/800^2 (about 1.6e-6), far more than
# TAU, and x >= y - TAU holds exactly when x >= y. In n_ge a shuffle's margin is scored on the
# shuffled block, whose present count need not be the real block's; the same lattice argument
# holds for it. TAU can only turn a rounding difference between equal fractions into a tie. The
# tie band that matters is the lambda tie in fitting.
TAU = H.TAU
FIXED_LAMBDA = 1.0                                     # section 3.5: the fixed-lambda diagnostic
LAMBDA_TIE_TEXT = "1e-9"                               # harness.py:727-728 (fit_bf), literal
# S21 (B section 2.4): the within-fly note scaled to the block; a note, not a cut.
WITHIN_FLY_NOTE = ("within-fly variation, not a cut: one FlyWire column differs from FlyWire-30 "
                   "by a median of 34 extra and 27 missing pairs out of 900 cells (61 differing "
                   "cells; about 2.7 of 40 cells if spread evenly; X_c = 0.54 shows it is not) "
                   "(B section 2.4)")

# Section 3.2: the legs.
N_SHUFFLES = H.N_SHUFFLES                              # 99, harness.shuffled_bank(base, sd)
N_PERM = 9999
RC_SWAPS = 20 * 32                                     # successful checkerboard swaps per draw
# S12 (D7): at most RC_CAP_FACTOR x RC_SWAPS = 64,000 attempts per chain, on the pattern of the
# harness's rewiring (harness.py:881-883, cap = 100 * target).
# port: male RC_CAP_FACTOR (line 340) -> S12
RC_CAP_FACTOR = 100
N_PERM_CEILINGS = 20                                   # section 2.4, D9

# Section 3.7 (S13): seeds, all new, in 91000-91999; asserted distinct, in range, and disjoint from
# A's reserved and reused list, block A's own seeds and the male arm's in assert_seeds_unique.
SEED_PERM = 91000                                      # leg P uniform; permutation 0 = leakage
SEED_RC = 91001                                        # leg P row-and-column
SEED_PERM_CEIL = 91010                                 # + j, j = 0..19
SEED_WORLD = 91100                                     # + 10 i + j (91100-91184)
SEED_RANGE = (91000, 91999)
# port: male A_SEEDS (lines 351-352) -> S13
A_SEEDS = ({90000, 90001} | set(range(90010, 90030)) | set(range(90100, 90155))
           | set(range(90160, 90185)))
# S13 (revision 1.2): the male CNS arm's seeds (male arm registration section 3.7).
MALE_SEEDS = {92000, 92001} | set(range(92010, 92030)) | set(range(92100, 92185))

# Section 3.6: the synthetic worlds. Family index i (seeds) is the position in this tuple, A's
# order (R, Nf, No, W, M0.5, M1.0, M0.6, M0.75, M0.85 = 0..8).
#   family, gamma on z, gamma on z1, block board
FAMILIES = (("R", 2.0, 0.0, "z"), ("Nf", 0.0, 0.0, "z"), ("No", 2.0, 0.0, "z'"),
            ("W", 1.5, 2.5, "z"), ("M0.5", 0.5, 0.0, "z"), ("M1.0", 1.0, 0.0, "z"),
            ("M0.6", 0.6, 0.0, "z"), ("M0.75", 0.75, 0.0, "z"), ("M0.85", 0.85, 0.0, "z"))
WORLDS_PER_FAMILY = 5
# S14 (D4 (i)): the latent polarity on the 13 block types. Targets as in A (z = +1 on Mi1, Tm3,
# Mi4, Mi9; -1 on Tm1, Tm2, Tm4, Tm9); sources L1 +1, L2 -1 (the note's ON and OFF sides), and
# L3 +1, L4 -1, L5 +1, fixed by rule, not by biology: the worlds calibrate the instrument on a
# planted rank-1 board of block B's shape, not the biology of L3-L5.
Z_PLUS = set(ON) | {"L1", "L3", "L5"}                  # z = +1; z = -1 on OFF, L2, L4
# S14 (D5 (i)): z' on the targets is A's z' (+1 on Mi1, Tm3, Tm1, Tm2; -1 on Mi4, Mi9, Tm4,
# Tm9), exactly orthogonal to z over the eight targets with classes of 2; on the sources
# z' = (+1, +1, -1, -1, +1) for L1-L5, so that sum z z' = +1 over the five sources.
ZPRIME_PLUS = {"Mi1", "Tm3", "Tm1", "Tm2", "L1", "L2", "L5"}   # z' = +1; -1 on the rest
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
# S38 (the male arm's S16, its not-readable part; B sections 3.2 and 4): a block on which no AUC
# on the grid k / (n_p n_a) gives p_P <= 0.01 (smallest_passing_auc is None) reads a U of its own
# kind. It takes precedence over R, W and G alike, is never renamed by the U rule, is not a
# threshold U, and is counted apart. Its reason is its text; block B's literal says "of 40".
# port: male NOT_READABLE_REASON, NOT_READABLE_PREFIX (lines 407-412) -> S38
NOT_READABLE_REASON = ("not readable: leg P cannot reach p_P <= 0.01 on this block (n_present = "
                       "{k} of 40)")
NOT_READABLE_PREFIX = "not readable: leg P cannot reach p_P <= 0.01 on this block"
# S8, check 3 (B section 3.4): a block with 0 or 40 present cells has no AUC; the run stops.
# port: male NO_AUC_TEXT (line 414) -> S8
NO_AUC_TEXT = "BLOCK HAS NO AUC"
# S30, B section 4 (D9): "failed fit" keeps its text; on block B it is read as below, printed
# beside a failed-fit U only.
# port: male FAILED_FIT_READING (lines 416-417) -> S30
FAILED_FIT_READING = ("on block B read as: a failed fit or a rank limit, not separated (the real "
                      "block is not known to be rank 1; B section 4, D9)")
# S30, B section 4 (D8): the outcome note, printed beside a U only, with N1's own p_P.
ADDITIVE_CHANNEL_NOTE = ("on block B, N1's additive score can order part of the block (B section "
                         "0), so the additive (degree) channel is a second possible source of this "
                         "U: a rule that follows it can pass leg P and fail leg S (B section 4, D8)")
# Revision 3.3 (A7): a real-arm run made with --allow-dirty is not the registered run.
NOT_REGISTERED_TEXT = ("NOT THE REGISTERED RUN: made with --allow-dirty; this verdict cannot be "
                       "cited as the registered result (sections 3.3, 7).")
N_DEG_SENTENCE = ("{n} of {N} shuffles have no AUC on the block and are excluded from leg S, "
                  "which counts against {k} = {N} - {n} shuffles (smallest p_S {ps:.3f})")
# S36 (the male arm's S28): the count decides leg S; p_S is printed as information, with four
# decimals and this mark when n_deg >= 1.
# port: male P_S_MARK (line 421) -> S36
P_S_MARK = "[leg S decided by the count: n_ge = {n_ge} of {n_valid}]"
# S37 (the male arm's S30): the stop of a reference whose manifest names other code.
PROVENANCE_DIFFERS_TEXT = "PRE-RUN PROVENANCE DIFFERS"
# S39: the stop record of a row-and-column chain that reached its attempt cap.
STOP_RECORD_NAME = "stop_record.json"
# S27: the marker of a started real arm, and the three outcomes of the search for earlier ones.
REAL_ARM_MARKER = "REAL_ARM_STARTED.json"
EARLIER_RUNS_TEXT = {
    "missing": "root does not exist: {root}",
    "unreadable": "root exists and cannot be read: {root} ({error})",
    "read": "root read: {root}, folders `{arm}_*`; {n} found{names}"}

# Section 3.4, check 8: the harness identity, as in bf1_p3.
BF1_FULL_BANK_MARGIN = 0.028150051052145946
IDENTITY_TOL = 1e-9
PARITY_TOL = 1e-9                                      # A section 3.4, check 5 (printed only here)
# Revision 3.2 (A1): the tolerance of the reproduction gate on the continuous columns of
# synthetic_worlds.csv, in each column's own units. The name is reused from
# results/genome/c6/checks/bf1_p3.py (MACHINE_CHECK_TOL = 1e-9); TAU is not reused for it.
MACHINE_CHECK_TOL = 1e-9

# S24, S29: the log. Every line goes to the tee's file first (stdout.log in the run's folder,
# opened with encoding utf-8), then to the console inside a guard; a console error is counted
# (log_output_errors in the manifest) and the line is written again with backslashreplace; log
# never raises. Lines logged before the folder exists are buffered and written first.
# port: male _LOG_BUFFER, tee_to, _untee (lines 461-477, 3789-3794) -> S24, S29 (the male _Tee,
# which wrote to the console before the file, is not carried)
_LOG = {"fh": None, "buffer": [], "output_errors": 0}


def log(m="", stream=None):
    """S24: write one line to the tee's file (or its buffer), then to the console (sys.stdout, or
    `stream`); a UnicodeError or OSError of the console is counted, the line is written again
    with backslashreplace, and nothing is raised."""
    s = f"{m}\n"
    fh = _LOG["fh"]
    if fh is not None:
        fh.write(s)
        fh.flush()
    else:
        _LOG["buffer"].append(s)
    out = sys.stdout if stream is None else stream
    try:
        out.write(s)
        out.flush()
    except (UnicodeError, OSError):
        _LOG["output_errors"] += 1
        try:
            enc = getattr(out, "encoding", None) or "ascii"
            out.write(s.encode(enc, "backslashreplace").decode(enc, "replace"))
            out.flush()
        except Exception:                              # the file holds the line; never raise
            try:
                out.write(s.encode("ascii", "backslashreplace").decode("ascii"))
                out.flush()
            except Exception:
                pass


def tee_to(path):
    """S24, S29: from here on every log line is also written to path (utf-8); the lines logged
    before are written first."""
    fh = open(path, "a", encoding="utf-8", newline="\n")
    fh.write("".join(_LOG["buffer"]))
    fh.flush()
    _LOG["buffer"].clear()
    _LOG["fh"] = fh
    return fh


def untee():
    """S29: close the tee's file; no line is written to it afterwards."""
    fh, _LOG["fh"] = _LOG["fh"], None
    if fh is not None:
        fh.flush()
        os.fsync(fh.fileno())
        fh.close()


def command_environment():
    """S28: the command's environment for the manifest: sys.argv, the encodings of stdout and
    stderr (as found at import and in effect), PYTHONUTF8, PYTHONIOENCODING, PYTHONHASHSEED (as
    found at import; None when unset) and the four BLAS thread variables (found before setdefault
    and in effect)."""
    return {"argv": list(sys.argv),
            "stdout_encoding": getattr(sys.stdout, "encoding", None),
            "stderr_encoding": getattr(sys.stderr, "encoding", None),
            "stream_encoding_found_at_import": dict(STREAM_ENCODING_FOUND),
            **{v: COMMAND_ENV_FOUND[v] for v in COMMAND_ENV_VARS},
            "thread_env": {v: {"found": THREAD_ENV_FOUND[v], "in_effect": os.environ.get(v)}
                           for v in THREAD_VARS}}


def count_where(rows, field, key, cond=None):
    """S34: a count over a filtered set, stated with its denominator. The filter keeps the rows
    whose `field` equals `key`; n is the number of rows it matched and k the number of those for
    which cond(row) holds (all of them when cond is None). A filter that matches no row stops
    with "FILTER MATCHED NOTHING: <key>" instead of returning 0."""
    matched = [r for r in rows if r.get(field) == key]
    if not matched:
        sys.exit(f"FILTER MATCHED NOTHING: {key} (field {field!r}, {len(rows)} rows searched)")
    k = sum(1 for r in matched if cond is None or cond(r))
    return {"k": k, "n": len(matched), "text": f"{k} of {len(matched)}"}


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

def tree_state():
    """The tree's state under results/genome/c6/ and docs/plans/ (git status --porcelain); one
    function, so that the tests can give a flow a clean tree."""
    return git("status", "--porcelain", "--", "results/genome/c6", "docs/plans")


def refuse_if_dirty(allow_dirty):
    """Section 3.3: the real arm runs once, at a committed head, with the tree clean under
    results/genome/c6/ and docs/plans/ (the refusal of harness.rule_run, reused)."""
    d = tree_state()
    if d and not allow_dirty:
        sys.exit("REFUSED: uncommitted changes under results/genome/c6/ or docs/plans/; a "
                 f"verdict must be tied to a commit ({REGISTRATION} and this script first).\n" + d)
    return d


def check_pins():
    """Section 3.4 check 1: every sha256 equals section 1.1's table, the versions are section
    7's, and rule #2.1 loads through harness.load_rule with RANK == 1. S2: A's registration, from
    which section 4 is quoted, must carry its LF sha256 after Amendment 1 (every mode); the hash
    of the text of A's verdict is recorded beside it, not checked."""
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
    # port: male check_pins, the A-registration clause (lines 610-613) -> S2
    a_now = sha256_lf(ROOT / A_REGISTRATION)
    if a_now != A_REGISTRATION_SHA256_LF_AMENDED:
        sys.exit(f"REFUSED: {A_REGISTRATION} has LF sha256 {a_now}; block B quotes section 4 "
                 f"from A after Amendment 1, pinned {A_REGISTRATION_SHA256_LF_AMENDED} (S2): A "
                 "changed")
    return {"pins": now, "python": py, "numpy": npv, "rule_name": rule.name,
            "rule_rank": rule.rank, "a_registration_sha256_lf": a_now,
            "a_registration_pinned_amended": A_REGISTRATION_SHA256_LF_AMENDED,
            "a_registration_flyvis65_text": A_REGISTRATION_SHA256_LF_FLYVIS65, "passed": True}


def reference_mode():
    """S17: True when block B's reference is registered (PRERUN_SHA256 and
    PRERUN_WORLDS_CSV_SHA256 set); False in pre-run mode, while they are placeholders."""
    # port: male reference_mode (lines 2068-2071) -> S17
    return PRERUN_SHA256 is not None and PRERUN_WORLDS_CSV_SHA256 is not None


def placeholders_unset():
    """S17, S37 (D10 (i)): the constants that the revision after the pre-run registers; a name is
    listed while its value is None."""
    # port: male placeholders_unset (lines 552-564) -> S17
    return [n for n in ("PRERUN_SHA256", "PRERUN_WORLDS_CSV_SHA256", "PRERUN_GIT_HEAD",
                        "PRERUN_SCRIPT_SHA256_LF") if globals()[n] is None]


def check_registered_constants():
    """S17, S37: the real arm refuses until the revision after the pre-run has set every
    placeholder (block B's reference pins, its head and its script)."""
    # port: male check_registered_constants (lines 567-575) -> S17
    missing = placeholders_unset()
    if missing:
        sys.exit("REFUSED: --arm flyvis65_blockB needs the values that the revision after the "
                 "pre-run registers (D10 (i), sections 3.3, 7); still placeholders: "
                 + ", ".join(missing))
    return {"placeholders_unset": [], "passed": True}


# ------------------------------------------------------------------------------------------
# Section 3.4 checks 2, 3, 4, 5, 7: the block, its print, the pre-data table, N1 parity, AUC.

def check_block_and_mask():
    """Check 2 (S7): 40 cells, 5 distinct sources and 8 distinct targets, all 13 names in NAMES,
    sources and targets disjoint; the training mask has 4,185 cells and none is a block cell; the
    ceiling_block mask is the 40; all 64 cells of block A are in the training mask (since the mask
    is ~BLOCK, exactly BLOCK_A & BLOCK = empty)."""
    ko, blk = MASKS["ko"], MASKS["block"]
    ok = (len(set(map(tuple, BLOCK_CELLS.tolist()))) == N_BLOCK
          and len(set(BLOCK_CELLS[:, 0].tolist())) == N_SOURCES
          and len(set(BLOCK_CELLS[:, 1].tolist())) == N_TARGETS
          and not set(SOURCES) & set(TARGETS) and all(n in H.NAMES for n in SOURCES + TARGETS)
          and int(ko.sum()) == N_TRAIN_CELLS and not (ko & BLOCK).any()
          and int(blk.sum()) == N_BLOCK and np.array_equal(blk, BLOCK)
          and int(MASKS["full"].sum()) == 65 * 65
          and int(BLOCK_A.sum()) == 64 and bool(ko[BLOCK_A].all()) and not (BLOCK_A & BLOCK).any()
          and len(H.make_view(H.Bank("geometry", {}), ko).cells) == N_TRAIN_CELLS)
    if not ok:
        sys.exit("BLOCK OR MASK DIFFERS (section 3.4, check 2)")
    return {"cells": N_BLOCK, "sources": N_SOURCES, "targets": N_TARGETS,
            "training_cells": int(ko.sum()), "ceiling_block_cells": int(blk.sum()),
            "block_A_cells_in_training": int(ko[BLOCK_A].sum()), "passed": True}


def block_print(y):
    """S8, check 3: the block's present count and its six strata counts (B section 3.4); has_auc
    is False with 0 or 40 present cells. has_auc means "the AUC is defined" (0 < n < 40), not
    "leg P can pass": n = 1 and n = 39 pass check 3 and are read by S38 (the "not readable" U,
    smallest_passing_auc is None), not stopped here (revision 1.5, A1)."""
    y = np.asarray(y, bool)
    n = int(y.sum())
    return {"present": n, "absent": N_BLOCK - n,
            "strata": {k: f"{int(y[v].sum())} of {len(v)}" for k, v in STRATA.items()},
            "has_auc": 0 < n < N_BLOCK}


def check_block_print(y):
    """S8, check 3 (real arm only, at run start, before any fit on the real bank): no reviewed
    count exists (D3), so the block's present count and six strata counts are printed, not
    compared. The run stops only if the block has no AUC (0 or 40 present: "BLOCK HAS NO AUC");
    a block with an AUC on which leg P cannot pass reads the "not readable" U (S38), not a stop."""
    # port: male check_block_print (lines 734-745) -> S8 (no seal: printed at run start; the
    # whole run stops, there is no other lobe)
    # has_auc is "AUC defined" (0 < n < 40), not "leg P can pass": n = 1 and 39 pass this check
    # and are read by S38 (revision 1.5, A1).
    d = block_print(y)
    log(f"check 3 (block print): present {d['present']} of {N_BLOCK}; strata {d['strata']}")
    if not d["has_auc"]:
        log(f"{NO_AUC_TEXT} ({d['present']} of {N_BLOCK} present): the run stops, with no label "
            "(check 3, B section 3.4)")
        sys.exit(1)
    return {**d, "passed": True}


def endpoint_table(bank):
    """Section 1.4's table in its canonical form (B section 1.4, "The canonical form, exactly"):
    keys the 13 names as str; for a source [training targets, training sources], for a target
    [training sources, training targets], each a Python int; presence ex = exists & ~BLOCK, so
    no value of a block-B cell is read; self-loops counted."""
    ex = bank.exists & ~BLOCK
    keep = {}
    for s in SOURCES:
        i = H.IDX[s]
        keep[s] = [int(ex[i, :].sum()), int(ex[:, i].sum())]
    for t in TARGETS:
        i = H.IDX[t]
        keep[t] = [int(ex[:, i].sum()), int(ex[i, :].sum())]
    return keep


def endpoint_table_sha256(keep):
    """The registered hash of section 1.4: sha256 of the UTF-8 bytes of
    json.dumps({"endpoints": keep}, sort_keys=True, separators=(",", ":")), no trailing newline."""
    canon = json.dumps({"endpoints": keep}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def pre_data_tables(bank):
    """Section 1.4, from presence outside the block only: what each endpoint keeps (the table
    and its hash), Johnny's inferability, the mirror cells, and the training present count
    (section 1.3; printed, not checked, D3)."""
    ex = bank.exists & ~BLOCK
    keep = endpoint_table(bank)
    inf = [(s, t) for s, t in BLOCK_NAMES
           if keep[s][0] >= INFERABLE_MIN and keep[t][0] >= INFERABLE_MIN]
    mirrors = {(t, s) for s, t in BLOCK_NAMES if ex[H.IDX[t], H.IDX[s]]}
    return {"endpoints": keep, "endpoints_sha256": endpoint_table_sha256(keep),
            "inferable": len(inf), "mirrors": sorted(mirrors),
            "training_present": int(ex.sum())}


def check_pre_data_tables(tables, real_arm):
    """Check 4 (S6): the endpoint table's sha256, 40 / 40 inferable and the 9 mirrors as
    registered, else "PRE-DATA TABLES DIFFER" (the hashes and counts are printed, not the table's
    values). In the real arm the table and the training present count are returned for printing
    at run start (D2 (ii), D3); in --synthetic-only only the hash, the inferable count and the
    mirrors are returned, so that no output of the pre-run carries a count from which block B's
    content follows by subtraction."""
    # Printed in the real arm only (B sections 1.3, 1.4, revision 1.5; D3 (ii)). If printed in
    # --synthetic-only (the pre-run), two routes would give block B's content before the
    # registered run: 604 minus the training present count is block B's present count, and the
    # table's per-name [out, in] pairs with the public whole-bank degrees (A section 1.4) give
    # presence inside the block per name.
    ok = (tables["endpoints_sha256"] == ENDPOINTS_SHA256
          and tables["inferable"] == INFERABLE_EXPECTED
          and set(map(tuple, tables["mirrors"])) == MIRRORS_EXPECTED)
    if not ok:
        log("PRE-DATA TABLES DIFFER")
        log(json.dumps(json_safe({"endpoints_sha256": tables["endpoints_sha256"],
                                  "registered": ENDPOINTS_SHA256,
                                  "inferable": tables["inferable"],
                                  "mirrors": tables["mirrors"]}), indent=1))
        sys.exit(1)
    out = {"passed": True, "endpoints_sha256": tables["endpoints_sha256"],
           "inferable": tables["inferable"], "mirrors": tables["mirrors"]}
    if real_arm:
        out.update(endpoints=tables["endpoints"], training_present=tables["training_present"],
                   training_present_status="printed, not checked (D3)")
    return out


def parity_D(z, y):
    """Section 2.3: D(z) = mean of z over the present block cells minus mean over the absent."""
    y = np.asarray(y, bool)
    if y.all() or not y.any():
        return None
    return float(np.mean(z[y]) - np.mean(z[~y]))


def n1_block_logit(n1data):
    """N1's existence logit on the 40 block cells, from the data as the decoder sees it."""
    c = H.cast(n1data)
    return c["ex_c"][0] + c["ex_a"][BLOCK_CELLS[:, 0]] + c["ex_b"][BLOCK_CELLS[:, 1]]


def check_n1_parity(n1data, y):
    """S9, check 5 (D6 (i)): D(N1 logit) on the block, printed; no stop. The parity identity
    cannot hold on any non-degenerate 5 x 8 block (B section 0), so D is printed beside the
    verdict and decides nothing."""
    # port: male check_n1_parity (lines 863-871) -> S9 (without the male balance field: a 5 x 8
    # block is never balanced)
    d = parity_D(n1_block_logit(n1data), y)
    return {"D_N1_logit": d, "tolerance_of_A": PARITY_TOL,
            "within_A_tolerance": d is not None and abs(d) < PARITY_TOL,
            "status": "printed, decides nothing (D6)", "passed": None}


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
    random 32/32 case with ties. S10: one unbalanced 40-cell hand case, 10 present of 40: the
    prediction 39 - i on cell i, present on cells 0-8 and 39, so the 9 top cells outrank all 30
    absent cells and cell 39 none: AUC = 9 * 30 / (10 * 30) = 0.9."""
    # port: male check_auc_function, its unbalanced hand case (lines 912-924) -> S10
    y = np.array([1, 1, 0, 0], bool)
    y40 = np.zeros(40, bool)
    y40[list(range(9)) + [39]] = True
    cases = [([0.9, 0.8, 0.2, 0.1], y, 1.0), ([0.1, 0.2, 0.8, 0.9], y, 0.0),
             ([0.5, 0.5, 0.5, 0.5], y, 0.5),
             ([0.9, 0.5, 0.5, 0.1], np.array([1, 0, 1, 0], bool), 0.875),
             (39.0 - np.arange(40), y40, 0.9)]
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
        log(f"AUC FUNCTION FAILS: {got}, {ranks}")
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
    """Leg P: default_rng(91000), 9,999 x permutation(40) in order (S11); permutation 0 is also the
    leakage check's."""
    # port: male uniform_perms (line 960): permutation(N_BLOCK) -> S11
    if "u" not in _PERM_CACHE:
        rng = np.random.default_rng(SEED_PERM)
        _PERM_CACHE["u"] = np.array([rng.permutation(N_BLOCK) for _ in range(N_PERM)])
    return _PERM_CACHE["u"]


def perm_ceiling_perm(j):
    """Section 2.4, D9 (S11): permutation j of the block, default_rng(91010 + j).permutation(40)."""
    return np.random.default_rng(SEED_PERM_CEIL + j).permutation(N_BLOCK)


# S12, S39 (D7): the row-and-column variant on the (5, 8) block, with its guards.
# port: male _RC_CACHE, RC_ONE_PATTERN_TEXT, RC_CAP_STOP_TEXT (lines 974-977) -> S12
_RC_CACHE = {}
RC_ONE_PATTERN_TEXT = "n/a: the row-and-column null has one pattern"
RC_CAP_STOP_TEXT = ("ROW-AND-COLUMN NULL: ATTEMPT CAP REACHED (chain {chain}, successes {succ}, "
                    "attempts {att})")
# S39: the run's own folder, arm and head, set by main when the run folder is known (the real
# arm's private folder; the --out folder in --synthetic-only), for the stop record.
_RUN = {"folder": None, "arm": None, "head": None}


def has_checkerboard(yb):
    """S12 (D7, guard 2): rows i, j and columns k, l with y[i,k] = y[j,l] != y[i,l] = y[j,k]
    exist iff, for some row pair, each row has a present cell where the other is absent."""
    # port: male has_checkerboard (lines 981-989) -> S12
    yb = np.asarray(yb, bool)
    for i in range(yb.shape[0]):
        for j in range(i + 1, yb.shape[0]):
            if (yb[i] & ~yb[j]).any() and (~yb[i] & yb[j]).any():
                return True
    return False


def write_stop_record(fields, message):
    """S39: before the attempt-cap stop exits, stop_record.json is written into the run's own
    folder (flushed, synced and closed), holding the stop message, the chain index, succ, att,
    the arm and the git head. Returns the path, or None when the run has no folder."""
    folder = _RUN["folder"]
    if folder is None:
        # B section 3.2 (3), S39 (revision 1.5, OPEN 2): a --synthetic-only run without --out
        # has no folder (it writes nothing, A section 7), so no record is written and the stop
        # message says so. Seen from outside: no folder (legitimate without --out) / a folder
        # with stop_record.json and no sums (stopped) / a folder with sums (completed).
        return None
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / STOP_RECORD_NAME
    rec = {"stop": message, **fields, "arm": _RUN["arm"], "head": _RUN["head"],
           "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(dump_json(rec) + "\n")
        fh.flush()
        os.fsync(fh.fileno())
    return path


def _rc_chains(y, n_chains, swaps):
    """S12: A's chains on the (5, 8) block. The pattern is reshaped to (N_SOURCES, N_TARGETS) (A's
    reshape(8, 8) raises ValueError on 40 labels); each step draws one attempt per chain, rows i,
    j in range(5) and columns k, l in range(8), with one rng.integers call (A drew all four from
    integers(8), which raises IndexError on a 5-row pattern); each chain makes at most
    RC_CAP_FACTOR x swaps attempts (harness.py:881-883). A pattern with no checkerboard 2 x 2
    admits no swap: its null has one pattern and the loop is not entered."""
    # port: male _rc_chains (lines 992-1024) -> S12 (the reshape and the per-axis ranges are
    # block B's own)
    yb = np.asarray(y, bool).reshape(N_SOURCES, N_TARGETS)
    if not has_checkerboard(yb):
        return {"status": "one_pattern", "patterns": None, "text": RC_ONE_PATTERN_TEXT}
    rng = np.random.default_rng(SEED_RC)
    B = np.broadcast_to(yb, (n_chains, N_SOURCES, N_TARGETS)).copy()
    succ = np.zeros(n_chains, np.int64)
    att = np.zeros(n_chains, np.int64)
    cap = RC_CAP_FACTOR * swaps
    high = np.array([N_SOURCES, N_SOURCES, N_TARGETS, N_TARGETS])
    n = np.arange(n_chains)
    while True:
        live = (succ < swaps) & (att < cap)
        if not live.any():
            break
        a = rng.integers(0, high, size=(n_chains, 4))
        i, j, k, l = a[:, 0], a[:, 1], a[:, 2], a[:, 3]
        x11, x12, x21, x22 = B[n, i, k], B[n, i, l], B[n, j, k], B[n, j, l]
        att += live
        ok = live & (i != j) & (k != l) & (x11 == x22) & (x12 == x21) & (x11 != x12)
        m = n[ok]
        for r, c in ((i, k), (i, l), (j, k), (j, l)):
            B[m, r[ok], c[ok]] = ~B[m, r[ok], c[ok]]
        succ += ok
    capped = np.flatnonzero(succ < swaps)
    if capped.size:
        c = int(capped[0])
        return {"status": "cap", "patterns": None, "chain": c, "successes": int(succ[c]),
                "attempts": int(att[c]), "n_chains_capped": int(capped.size), "cap": cap}
    assert (B.sum(2) == yb.sum(1)).all() and (B.sum(1) == yb.sum(0)).all()
    return {"status": "complete", "patterns": B.reshape(n_chains, N_BLOCK), "text": None,
            "max_attempts": int(att.max()), "cap": cap}


def rc_patterns(y, n_chains=N_PERM, swaps=RC_SWAPS):
    """Leg P, row-and-column variant (A D4; printed, decides nothing): 9,999 random 5 x 8
    patterns with the block's row and column counts, each by 20 x 32 successful checkerboard
    swaps from the pattern y, one generator default_rng(91001) for all draws (_rc_chains). A
    pattern with no checkerboard gives RC_ONE_PATTERN_TEXT and no patterns. A chain that reaches
    the attempt cap stops the run (D7, kept; unlike the male arm's real block, which goes on),
    in the synthetic step and in the real arm alike: the stop record is written first (S39),
    then the stop message is logged and the run exits with status 1. n_chains and swaps are for
    the tests; the registered calls use the defaults."""
    # port: male rc_patterns (lines 1027-1046) -> S12, S39 (one mode: the cap always stops)
    y = np.asarray(y, bool)
    key = (y.tobytes(), n_chains, swaps)
    if key not in _RC_CACHE:
        _RC_CACHE[key] = _rc_chains(y, n_chains, swaps)
    res = _RC_CACHE[key]
    if res["status"] == "cap":
        fields = {"chain": res["chain"], "succ": res["successes"], "att": res["attempts"]}
        msg = RC_CAP_STOP_TEXT.format(**fields)
        path = write_stop_record(fields, msg)
        log(f"{msg}; arm {_RUN['arm']}, head {_RUN['head']}; stop record: "
            f"{path if path is not None else 'none (the run has no folder)'}; the run stops "
            "(D7, S39)")
        sys.exit(1)
    return res


def _array_sha256(a):
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()


def null_input_digests():
    """Revision 3.3 (F10): digests of the leg-P null inputs (the uniform_perms() matrix; each
    registered-size rc_patterns matrix, keyed by the sha256 of its y bytes, or its status when
    it has no patterns). Computed in the main process, where every null is computed."""
    # port: male null_input_digests (lines 1053-1069) -> S12
    u = uniform_perms()
    rc = {}
    for (yk, n_chains, swaps), v in _RC_CACHE.items():
        if n_chains != N_PERM or swaps != RC_SWAPS:
            continue
        p = v["patterns"]
        rc[hashlib.sha256(yk).hexdigest()] = (
            {"sha256": _array_sha256(p), "dtype": str(p.dtype), "shape": list(p.shape)}
            if p is not None else {"status": v["status"]})
    return {"uniform_perms": {"sha256": _array_sha256(u), "dtype": str(u.dtype),
                              "shape": list(u.shape), "seed": SEED_PERM,
                              "computed_in": "main process"},
            "rc_patterns_by_y_sha256": rc, "rc_seed": SEED_RC}


def reserved_seeds(starts):
    """Section 3.7, "Untouched", and the reused ranges, read from the harness where it defines
    them (A's list), with block A's own seeds and the male arm's (S13)."""
    # port: male reserved_seeds (lines 1072-1080) -> S13 (the male list reserves A's and B's;
    # block B's reserves A's and the male arm's)
    dial = {10000 + 100 * fi + sd for fi in range(len(H.DIAL_F)) for sd in range(H.DIAL_SEEDS)}
    return ({60000, 61000} | set(range(70000, 71000)) | set(range(80000, 81000))
            | {H.PL_SEED, H.PL_SCRAMBLE_SEED, H.PRSH_SEED}
            | {H.RP_SEED_BASE + j for j in H.RP_SEEDS} | dial | {20260923}
            | set(range(N_SHUFFLES)) | {H.PERTURB_SEED_BASE + j for j in range(max(starts, 10))}
            | A_SEEDS | MALE_SEEDS)


def world_specs():
    return [{"family": fam, "i": i, "j": j, "seed": SEED_WORLD + 10 * i + j, "gamma_z": gz,
             "gamma_z1": gz1, "board": board}
            for i, (fam, gz, gz1, board) in enumerate(FAMILIES) for j in range(WORLDS_PER_FAMILY)]


def assert_seeds_unique(starts):
    """S13, section 3.7: the new seeds (91000, 91001, 91010-91029, 91100-91184) are distinct, lie
    in 91000-91999, and meet none of the untouched, reused, block-A or male-arm seeds."""
    worlds = [w["seed"] for w in world_specs()]
    new = [SEED_PERM, SEED_RC] + [SEED_PERM_CEIL + j for j in range(N_PERM_CEILINGS)] + worlds
    ok = (len(new) == len(set(new)) == 2 + N_PERM_CEILINGS + len(FAMILIES) * WORLDS_PER_FAMILY
          and all(SEED_RANGE[0] <= s <= SEED_RANGE[1] for s in new)
          and not set(new) & reserved_seeds(starts))
    if not ok:
        sys.exit("SEEDS NOT UNIQUE: " + str(sorted(new)))
    return {"new_seeds": len(new), "unique": True, "in_91000_91999": True,
            "disjoint_from_reserved_reused_A_and_male": True,
            "world_seeds": [min(worlds), max(worlds)]}


# ------------------------------------------------------------------------------------------
# Section 3.6: the synthetic worlds.

# S14: the other types are the 52 types outside the 13 block types (A: 49).
OTHERS = [i for i in range(65) if H.NAMES[i] not in set(SOURCES + TARGETS)]
assert len(OTHERS) == 52
BLOCK_TYPES = [H.IDX[n] for n in SOURCES + TARGETS]
Z_BLOCK = np.zeros(65)
ZPRIME = np.zeros(65)
for _n in SOURCES + TARGETS:
    Z_BLOCK[H.IDX[_n]] = 1.0 if _n in Z_PLUS else -1.0
    ZPRIME[H.IDX[_n]] = 1.0 if _n in ZPRIME_PLUS else -1.0
# S14, section 3.6 (D5 (i)), No: exact orthogonality and class sizes of 2 over the targets;
# |sum z z'| = 1 over the sources (0 is impossible with five). Only the targets' orthogonality is
# needed for the No world's exact 0.5 (B section 3.6's algebra; test_knockout_regrow_block_b.py).
assert sum(Z_BLOCK[H.IDX[t]] * ZPRIME[H.IDX[t]] for t in TARGETS) == 0
assert all(sum(1 for t in TARGETS if (Z_BLOCK[H.IDX[t]], ZPRIME[H.IDX[t]]) == c) == 2
           for c in ((1, 1), (1, -1), (-1, 1), (-1, -1)))
assert abs(sum(Z_BLOCK[H.IDX[s]] * ZPRIME[H.IDX[s]] for s in SOURCES)) == 1
# S14: the content pool, the real bank's present cells outside block B (block A's included).
NONBLOCK_CELLS = sorted(k for k in H.REAL_CONTENT if not BLOCK[k])
N_WORLD_BLOCK_PRESENT = 20                             # S14: every world's board, 20 of 40


def board_y(board):
    """The block labels of a world with this board, in block cell order, as make_world sets
    them: present iff z_s z_t > 0 (board "z") or z'_s z'_t > 0 (board "z'")."""
    # port: male board_y (lines 1121-1125) -> S14
    zb = Z_BLOCK if board == "z" else ZPRIME
    return (np.outer(zb, zb) > 0)[BLOCK_CELLS[:, 0], BLOCK_CELLS[:, 1]]


def degree_terms():
    """Section 3.6 (S14): N1's existence parameters (c, a, b), fitted on the real bank's knockout
    view of block B, outside-block-B cells only (block A's cells included). The one fit on the
    real bank that --synthetic-only makes."""
    n1 = H.fit_n1(H.make_view(real_bank(), MASKS["ko"]))
    return float(n1["ex_c"][0]), np.asarray(n1["ex_a"], float), np.asarray(n1["ex_b"], float)


def make_world(spec, terms):
    """Section 3.6 (S14): default_rng(seed) draws, in A's order, z for the 52 other types
    (ascending harness index; +1 iff a uniform draw < 1/2), z1 for the 52 others (drawn in every
    family, used in W only), u (65 x 65), and the content indices (65 x 65 integers into the
    present cells outside block B, as planted_banks draws its pool). Outside cells: present iff
    u < sigmoid(c + a_s + b_t + gamma_z z_s z_t + gamma_z1 z1_s z1_t). Block cells: the board by
    z or z', 20 present of 40."""
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
    assert int(bank.exists[BLOCK].sum()) == N_WORLD_BLOCK_PRESENT
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
        bank = real_bank()
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


def _fit_one(bk, mk, pk, bank):
    """One task on one bank (A's _w_group body): a check-8 fold, a hash-only fit, or a fit with
    its decode and score on the 40 block cells. A module-level function, so that the tests can
    replace the fit by a deterministic stand-in (fixture banks only)."""
    # port: male _fit_one (lines 1336-1361) -> S25, S26 (the tests' seam; the body is A's)
    P = _pred(pk)
    t0 = time.time()
    if mk.startswith("cv:"):
        return {"score": H.cv_fold(P, bank, int(mk[3:])), "secs": time.time() - t0}
    if mk == "ko1":
        data = train_fixed_lambda(pk, P, bank, FIXED_LAMBDA)
    else:
        data = P.train(bank, MASKS[mk.split("#")[0]])
    if "#hash" in mk:
        return {"data_sha256": data_sha256(data), "secs": time.time() - t0}
    dec = P.decode(data, BLOCK_CELLS)
    sc = H.score(dec, bank, BLOCK_CELLS)
    return {
        "p": np.asarray(dec["p_exist"], np.float64).tolist(),
        "y": bank.exists[BLOCK_CELLS[:, 0], BLOCK_CELLS[:, 1]].tolist(),
        "lam": _lambda_of(pk, P, data),
        # revision 3.3 (C7): sign_n (the integer) is stored beside the five fields of
        # earlier records; raw_fits_diagnostic compares the fields present in both
        "score": {k: sc[k] for k in ("existence", "offset", "counts", "sign", "sign_n",
                                     "n_ne")},
        "outside_density": float(bank.exists[~BLOCK].mean()),
        "secs": time.time() - t0}


def _w_group(group):
    key = group[0][0]
    if _W["key"] != key:
        _W["bank"], _W["key"] = build_bank(key, _W["terms"], _W["syn"]), key
    bank = _W["bank"]
    out = []
    for bk, mk, pk in group:
        assert bk == key
        out.append(((bk, mk, pk), _fit_one(bk, mk, pk, bank)))
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

def precision_at_n_present(p, y):
    """S15, section 3.1: the share of present cells among the n_present highest p_exist (ties
    broken in block cell order); A's precision at 32 on a 32/32 block. It is not accuracy when
    the labels are unbalanced. None with no present cell."""
    # port: male precision_at_n_present (lines 1418-1426) -> S15
    y = np.asarray(y, bool)
    n = int(y.sum())
    if n == 0:
        return None
    order = np.argsort(-np.asarray(p, np.float64), kind="stable")[:n]
    return float(y[order].mean())


def regrown_share(a, ceiling):
    """(AUC - 0.5) / (AUC_ceiling - 0.5); "n/a" (None) when the ceiling is <= 0.5. Despite its
    name it is a ratio, not a share: it can exceed 1 and be negative (revision 3.2, section 3.1);
    the CSV column keeps its name."""
    if a is None or ceiling is None or ceiling <= 0.5:
        return None
    return (a - 0.5) / (ceiling - 0.5)


def smallest_passing_auc(y, Yu):
    """Section 3.2, S16: the smallest AUC on the grid k / (n_p n_a) (A: k / 1024) that gives
    p_P <= 0.01 against this run's own 9,999 permutations, for a prediction without ties. It
    depends on the block's labels y through Yu = y[uniform_perms()] and on no fit (A revision
    3.3, B1). None when no AUC on the grid reaches p_P <= 0.01: leg P cannot pass on that block,
    and the block reads the "not readable" U (S38). None also for a block with no AUC (0 or 40
    present), which check 3 stops before."""
    # port: male smallest_passing_auc (lines 1438-1454): the docstring and the den == 0 guard
    # -> S16
    n1 = int(np.asarray(y, bool).sum())
    den = n1 * (N_BLOCK - n1)
    if den == 0:
        return None
    null = auc_null(np.arange(N_BLOCK, dtype=float), Yu)
    for k in range(den // 2, den + 1):
        a = k / den
        if (1 + int((null >= a - TAU).sum())) / (N_PERM + 1) <= P_R:
            return a
    return None


# A revision 3.4 (item 2), 3.4.1 (item B): smallest_passing_auc as a checked scalar, registered by
# board, with one address, block B's pinned synthetic_only.json (derive_smallest_passing_auc,
# after check_prerun_files). Block B's values do not exist yet (B section 3.3): the revision after
# the pre-run states them. In pre-run mode each board's value is computed from its labels and
# uniform_perms() alone (board_smallest_passing_auc) and checked on every world before the fits.
SMALLEST_PASSING_AUC_GATES = (
    "it gates one statistic of Yu = y[uniform_perms()] and the composition (the layout y, P_R, "
    "N_PERM), through auc_null on one tie-free prediction; it needs no fit. It does not see Yrc "
    "(rc_patterns), nor a change in the consumer at equal Yu (the p_P lines of evaluate_bank, "
    "avg_ranks on tied predictions, auc); the null-input digests remain for attribution. Under "
    "--from-raw, where y comes from the store and Yu is generated fresh, it is the only check of "
    "the fresh generator that stops the run (the comparison of the re-read table with the pinned "
    "one is for information only)")


def board_smallest_passing_auc():
    """Pre-run mode (S17): each board's smallest_passing_auc from its labels and uniform_perms()
    alone (it depends on nothing else); one layout per board (D4 (i))."""
    # port: male board_smallest_passing_auc (lines 2515-2519) -> S17
    perms = uniform_perms()
    return {b: smallest_passing_auc(board_y(b), board_y(b)[perms]) for b in ("z", "z'")}


def derive_smallest_passing_auc(path):
    """Revision 3.4.1 (item B): the registered smallest_passing_auc by board, derived from a
    synthetic_only.json (in run_synthetic, the pinned one, read after check_prerun_files has
    verified it against PRERUN_SHA256). Exactly one value per board is required: a board that
    carries two or more values, a world without a board or a value, or no world at all fails
    (passed False), and run_synthetic stops before any fit."""
    worlds = json.loads(Path(path).read_text(encoding="utf-8")).get("worlds") or []
    values, counts, incomplete = {}, {}, []
    for w in worlds:
        b, v = w.get("board"), w.get("smallest_passing_auc")
        if b is None or v is None:
            incomplete.append(w.get("seed"))
            continue
        values.setdefault(b, set()).add(v)
        counts[b] = counts.get(b, 0) + 1
    several = {b: sorted(v) for b, v in values.items() if len(v) != 1}
    passed = bool(values) and not several and not incomplete
    reason = ("one value per board" if passed else "; ".join(
        (["no world with a board and a value"] if not values else [])
        + [f"board {b!r} carries {len(v)} values {v}" for b, v in several.items()]
        + ([f"{len(incomplete)} worlds without a board or a value (seeds {incomplete})"]
           if incomplete else [])))
    return {"source": str(path), "passed": passed,
            "by_board": {b: next(iter(v)) for b, v in values.items()} if passed else None,
            "n_worlds_by_board": counts, "boards_with_several_values": several,
            "worlds_without_board_or_value": incomplete, "reason": reason}


def check_smallest_passing_auc(entries, expected):
    """Revision 3.4 (item 2): each world's smallest_passing_auc(y, y[uniform_perms()]) against the
    value registered for its board, `expected` (revision 3.4.1, item B: in run_synthetic, the
    values derive_smallest_passing_auc reads from the pinned synthetic_only.json). entries: dicts
    with "world", "board" and "y" (the block labels, 40 booleans in block cell order). A board
    without a registered value is a mismatch. Run by run_synthetic before any fit; a mismatch
    stops the synthetic step. What it gates: SMALLEST_PASSING_AUC_GATES."""
    expected = dict(expected or {})
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
    """Every number of section 3.5 for one bank, and its section 4 label (with the not-readable
    U of S38 before A's branches). The row-and-column variant stops the run on a capped chain
    (rc_patterns, S12, S39)."""
    base = {pk: F[(base_key, "ko", pk)] for pk in PRED_KEYS}
    y = np.asarray(base["N1"]["y"], bool)
    for pk in PRED_KEYS:
        for mk in ("ko", "full", "block"):
            assert np.array_equal(np.asarray(F[(base_key, mk, pk)]["y"], bool), y)
    Yu = y[uniform_perms()]
    rc = rc_patterns(y)
    Yrc = rc["patterns"]
    sh = []
    for sd in range(n_sh):
        f = {pk: F[(f"{base_key}|sh:{sd}", "ko", pk)] for pk in PRED_KEYS}
        ysd = np.asarray(f["N1"]["y"], bool)
        a_n1 = auc(f["N1"]["p"], ysd)
        row = {"sd": sd, "present": int(ysd.sum()), "degenerate": a_n1 is None}
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
        null_u = auc_null(p, Yu)
        null_rc = auc_null(p, Yrc) if Yrc is not None else None
        per_type = {}
        for n in SOURCES + TARGETS:
            idx = [i for i, (s, t) in enumerate(BLOCK_NAMES) if n in (s, t)]
            per_type[n] = auc(p[idx], y[idx])
        sc = base[pk]["score"]
        rows[pk] = {
            "predictor": PRED_NAME[pk], "auc": a, "n_present": int(y.sum()),
            "n_absent": int((~y).sum()), "D": parity_D(logit_of(p), y),
            "logloss": sc["existence"], "logloss_margin_over_N1": ll_n1 - sc["existence"],
            "precision_at_n_present": precision_at_n_present(p, y),
            "strata_mean_p": {k: float(p[v].mean()) for k, v in STRATA.items()},
            "ceiling_full": cf, "ceiling_block": cb,
            "regrown_share_full": regrown_share(a, cf), "regrown_share_block": regrown_share(a, cb),
            "M_real": m_real, "n_ge": int(n_ge), "n_shuffles": n_sh, "n_deg": int(n_deg),
            "n_valid_shuffles": int(n_valid),
            "leg_S_passes": bool(n_valid >= 1 and n_ge == 0),
            "p_S": (1 + n_ge) / (1 + n_valid),
            "p_P": (1 + int((null_u >= a - TAU).sum())) / (N_PERM + 1),
            "p_P_rowcol": (None if null_rc is None
                           else (1 + int((null_rc >= a - TAU).sum())) / (N_PERM + 1)),
            "p_P_rowcol_note": rc["text"],
            "lambda_ko": base[pk]["lam"], "lambda_full": F[(base_key, "full", pk)]["lam"],
            "lambda_block": F[(base_key, "block", pk)]["lam"],
            "mirror_partners_p": {f"{BLOCK_NAMES[i][0]}->{BLOCK_NAMES[i][1]}": float(p[i])
                                  for i in MIRROR_IDX},
            "auc_other_31": auc(p[rest], y[rest]),
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
    spa = smallest_passing_auc(y, Yu)
    # port: male evaluate_bank, read_label(rows, n_present=..., readable=spa is not None)
    # (line 1627) -> S38 (A's evaluate_bank calls read_label(rows), knockout_regrow.py line 1099)
    return {"bank": base_key, "rows": rows, "per_shuffle": sh, "n_deg": int(n_deg),
            "fixed_lambda": fixed,
            "perm_ceilings_full_rule": perm_ceilings,
            "outside_density": base["N1"]["outside_density"], "block_present": int(y.sum()),
            "row_and_column_null": {k: v for k, v in rc.items() if k != "patterns"},
            "smallest_passing_auc": spa,
            **read_label(rows, n_present=int(y.sum()), readable=spa is not None)}


# ------------------------------------------------------------------------------------------
# Section 4: the reading rule (A section 4, with the not-readable U of S38 before its branches).

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


def not_readable_reason(n_present):
    """S38: the "not readable" reason, which is also its U text (block B's literal, "of 40")."""
    # port: male not_readable_reason (lines 1667-1669) -> S38
    return NOT_READABLE_REASON.format(k=n_present)


def u_kind(reasons):
    """A revision 3.3 (A3, A4); S38: which U a list of U reasons gives. "not_readable" if a reason
    is the not-readable reason (it takes precedence: leg P cannot pass on the block, whatever
    else is listed); else "failed_fit" if a reason is ceiling_block below GATE_CUT; else
    "not_measured" if a reason is CEILING_BLOCK_NOT_MEASURED; else "threshold". Only threshold U
    enters the U rule."""
    # port: male u_kind (lines 1672-1685) -> S38
    rs = [str(r) for r in reasons or ()]
    if any(r.startswith(NOT_READABLE_PREFIX) for r in rs):
        return "not_readable"
    if any(r.startswith(CEILING_BLOCK_REASON) for r in rs):
        return "failed_fit"
    if CEILING_BLOCK_NOT_MEASURED in rs:
        return "not_measured"
    return "threshold"


def read_label(rows, n_present=None, readable=True):
    """Section 4: R, W, G, U in order. R and W are read on both D1 candidates and must agree,
    else U; if neither gives R or W, G and U are read on rule #2.1. The letter only: its text
    (G with the three limits, U by the U rule) is set by label_text once the synthetic run is
    read. S38 (B sections 3.2, 4): a block that is not readable (no AUC on the grid reaches
    p_P <= 0.01; readable False) reads U with the not-readable reason first; it takes precedence
    over R, W and G alike and is never renamed. A's reasons are kept after it, for information,
    and the letter A's branches gave is kept as label_before_readability."""
    # port: male read_label (lines 1688-1730) -> S38
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
    label_by_A = label
    if not readable:
        label, mech = "U", None
        reasons.insert(0, not_readable_reason(n_present))
    return {"label": label, "mechanism_description": mech, "reading_A_rule": A,
            "reading_B_BF1": B, "d1_agree_on_RW": A["letter"] == B["letter"],
            "U_reasons": reasons, "readable": bool(readable),
            "label_before_readability": label_by_A}


def fmt(x, d=4):
    return "n/a" if x is None else f"{x:.{d}f}"


def instrument_text(starts):
    """Section 3.6: what the three limits are measured with; printed with every G."""
    return (f"BF_LAMBDAS {list(H.BF_LAMBDAS)}, ties within {LAMBDA_TIE_TEXT} go to the larger "
            f"lambda (harness.py:727-728), STARTS = {starts}")


def limits_text(dl):
    """Section 3.6 (revision 3.1): the three limits with their brackets, the transition band,
    the per-gamma fractions seen/n and R/n, and the instrument; printed with every G. Block B's
    own limits, measured on block B's worlds (B section 3.6), in M-world units."""
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
    NOT_MEASURED_TEXT, and is never renamed either (u_kind). S38: a U whose reasons include the
    not-readable reason prints that reason as its text ("U: not readable: leg P cannot reach
    p_P <= 0.01 on this block (n_present = k of 40)"), never renamed.
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
    # port: male label_text, the not-readable branch (lines 1772-1773) -> S38
    if kind == "not_readable":
        return "U: " + next(str(r) for r in reasons if str(r).startswith(NOT_READABLE_PREFIX))
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


def p_s_text(r):
    """S36 (the male arm's S28): p_S as printed. Leg S is decided by the count (leg_S_passes:
    n_valid >= 1 and n_ge == 0); p_S is information. With n_deg >= 1 it is printed with four
    decimals and the mark naming the count; with n_deg = 0, as A (two decimals, no mark)."""
    # port: male p_s_text (lines 1788-1795) -> S36
    if r["n_deg"] >= 1:
        return (f"{r['p_S']:.4f} "
                + P_S_MARK.format(n_ge=r["n_ge"], n_valid=r["n_valid_shuffles"]))
    return f"{r['p_S']:.2f}"


def verdict_line(ev, dl, u_rule, no_contingency=False, not_registered=None):
    """Section 4: the label (G with the three limits and the instrument; U by the U rule, or as a
    failed fit, not measured, or not readable); the mechanism description of G; the primary's
    AUC with n_present/n_absent, p_S (S36) and p_P; both ceilings; the R/W reading on each D1
    candidate; the lambda each knockout fit selected, and a G reached through lambda = 100 named
    (revision 3.1, Zcode); the n_deg sentence above 5; the No contingency when triggered. The
    fixed-lambda diagnostic is not on this line (Johnny's condition), nor are D(N1 logit), N1's
    p_P and the conditional lines of S30 (conditional_lines: printed beside it). Revision 3.3
    (A7): when not_registered is given (a real-arm run made with --allow-dirty), the line ends
    with it."""
    r = ev["rows"]["rule"]
    s = label_text(ev["label"], dl, u_rule, ev["U_reasons"], r["ceiling_block"])
    if ev["label"] == "G":
        s += f" [mechanism, description only: {ev['mechanism_description']}]"
    s += (f". rule #2.1: AUC = {fmt(r['auc'])} ({r['n_present']}/{r['n_absent']}), "
          f"p_S = {p_s_text(r)} (n_ge = {r['n_ge']} of {r['n_valid_shuffles']}, "
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


def a_literals_line(ev, dl, ur, inferable):
    """S19, S30 (B section 4, D9 (i)): printed after the quoted A section 4 row when that row
    carries block A's literals, which only the G and U rows do ("64/64 inferable"; "all 3 pre-run
    U worlds sit at ..." and "the block is rank 1"); None for R and W, whose rows carry none. The
    line names each literal as block A's and gives block B's own value."""
    # port: male a_literals_line (lines 3223-3246) -> S19 (its R and W lines are not carried: on
    # block B the R row's "flyvis's averaged template" is block B's bank too)
    lab = ev["label"]
    if lab == "G":
        return (f"Block A's literal in the quoted row: \"64/64 inferable\" is block A's count; "
                f"block B: {inferable}/40 inferable (check 4). The limits and the instrument on "
                "the label are block B's own (B section 3.6).")
    if lab != "U":
        return None
    s = ("Block A's literals in the quoted row: \"all 3 pre-run U worlds sit at γ = 0.6 = γ*_P\" "
         f"are block A's pre-run worlds; block B's worlds: {ur['n_u_threshold']} threshold U on "
         f"the dense grid, gamma*_P = {dl['leg_P']['text']} (the U-rule paragraph); \"the block "
         "is rank 1\" is block A's board (A section 2.4); block B's real block is not known to be "
         "rank 1 (B section 2.4).")
    if not ev.get("readable", True):
        s += (" This U is the \"not readable\" U of B section 3.2, which A's row does not name "
              "(S38).")
    return s


def conditional_lines(ev, dl, ur, inferable):
    """S30: the conditional texts printed beside a verdict, each only when its condition holds:
    the A-literals line (a G or U row, D9), the reading of a failed fit on block B (a failed-fit
    U, D9), the additive-channel outcome note and N1's own p_P (a U, D8). A list of (key, text);
    the verdict line itself carries none of them."""
    out = []
    lit = a_literals_line(ev, dl, ur, inferable)
    if lit:
        out.append(("a_literals", lit))
    if ev["label"] == "U":
        if u_kind(ev["U_reasons"]) == "failed_fit":
            out.append(("failed_fit_reading", f"The failed fit is {FAILED_FIT_READING}."))
        out.append(("additive_channel_note", f"Beside this U: {ADDITIVE_CHANNEL_NOTE}."))
        out.append(("n1_p_P", f"N1's own p_P beside this U (decides nothing; B section 3.5): "
                              f"{ev['rows']['N1']['p_P']:.4f}"))
    return out


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


def csv_compare(ref, got, limit=20):
    """Sections 3.3 and 7 (revisions 3.2, 3.3): two synthetic_worlds.csv byte strings compared
    on the deciding columns, rows matched by CSV_KEY_COLUMNS. Separate outputs: rows missing on
    either side (or a duplicated key); key-matched rows whose values differ (CSV_EXACT_COLUMNS
    exactly, CSV_CONTINUOUS_COLUMNS within MACHINE_CHECK_TOL); a change of row order (a fact, not
    an outcome). Column 8 (mechanism_description) is reported, not gated (S17: A's check against
    its revision 3.2 rename is A's history and is not carried over). Outcome 1: all
    equal; 2: continuous within tolerance only; 3: part "a" (identity or lattice, rows, header)
    and/or part "b" (continuous beyond tolerance)."""
    # port: male csv_compare (lines 1903-1992), without A's rename check -> S17
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
           "first_mechanism_description_differences": []}
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
            res["first_mechanism_description_differences"].append(
                {**where, "prerun": ra[m], "now": rb[m]})
    counts = {f"n_{k}": len(res[k]) for k in ("duplicate_keys", "rows_missing_now",
                                               "rows_missing_prerun")}
    res.update(counts)
    for k in ("duplicate_keys", "rows_missing_now", "rows_missing_prerun",
              "first_exact_differences", "first_continuous_beyond_tolerance",
              "first_mechanism_description_differences"):
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
    "(ko, full, block, ko1, sh, pc) over all 637 keys per world: p on the 40 cells, lambda, the "
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
    """A revision 3.2 (Ark N3), S17: every file listed in PRERUN_DIR/SHA256SUMS.txt is read and
    its sha256 (raw bytes, read_bytes(), .gz included) must equal the listed value and
    PRERUN_SHA256; the list must name exactly the pinned files. A revision 3.3 (C6): entries of
    the folder that are neither listed nor pinned are reported in "unlisted", never failed. In
    pre-run mode (PRERUN_SHA256 is None) there is no registered reference: passed False."""
    # port: male check_prerun_files, its placeholder branch (lines 2074-2083) -> S17
    pins = PRERUN_SHA256 or {}
    sums = PRERUN_DIR / "SHA256SUMS.txt"
    if not pins:
        return {"passed": False, "sums_file": str(sums), "files": {}, "unlisted": [],
                "reason": "no registered reference (PRERUN_SHA256 is a placeholder)"}
    if not sums.exists():
        return {"passed": False, "sums_file": str(sums), "files": {}, "unlisted": [],
                "reason": "SHA256SUMS.txt not found"}
    listed = {}
    for ln in sums.read_text(encoding="utf-8").splitlines():
        if ln.strip():
            h, name = ln.split(maxsplit=1)
            listed[name.lstrip("*")] = h
    files = {}
    for name in sorted(set(listed) | set(pins)):
        p = PRERUN_DIR / name
        files[name] = {"listed": listed.get(name), "pinned": pins.get(name),
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


def prerun_provenance(head, script_sha256_lf):
    """S37 (the male arm's S30): which code made block B's reference and which code makes this
    run. The reference's files are verified first (check_prerun_files); its manifest's git_head
    and script_sha256_lf must equal PRERUN_GIT_HEAD and PRERUN_SCRIPT_SHA256_LF (else passed
    False, and the caller stops with "PRE-RUN PROVENANCE DIFFERS" before any fit). The reading
    script's own hash differs from the writing script's by design (D10 (i)); that difference is
    not a mismatch. The text names both. Revision 1.6 (A4; Ark 18:00): a reference whose manifest
    carries a non-null not_a_reference (an --allow-dirty run, S40) is refused (passed False)."""
    # port: male prerun_provenance (lines 2109-2137) -> S37
    out = {"registered_git_head": PRERUN_GIT_HEAD,
           "registered_script_sha256_lf": PRERUN_SCRIPT_SHA256_LF,
           "this_run_git_head": head, "this_run_script_sha256_lf": script_sha256_lf}
    files = check_prerun_files()
    if not files["passed"]:
        return {**out, "passed": False, "reason": "reference not verified: " + files["reason"],
                "text": None}
    man = json.loads((PRERUN_DIR / "synthetic_only.json")
                     .read_text(encoding="utf-8"))["manifest"]
    # Revision 1.6 (A4; Ark 18:00): a folder whose manifest carries not_a_reference (an
    # --allow-dirty run, S40) is never a reference, whatever its pins and its head.
    if man.get("not_a_reference"):
        return {**out, "passed": False, "not_a_reference": man["not_a_reference"],
                "reason": "the reference's manifest carries not_a_reference ("
                          + str(man["not_a_reference"]) + "); such a folder is never block B's "
                          "reference (S40, revision 1.6)", "text": None}
    ph, ps = man.get("git_head"), man.get("script_sha256_lf")
    ok = (PRERUN_GIT_HEAD is not None and PRERUN_SCRIPT_SHA256_LF is not None
          and ph == PRERUN_GIT_HEAD and ps == PRERUN_SCRIPT_SHA256_LF)
    text = (f"pre-run made by head {str(ph)[:7]}, script {str(ps)[:8]} (LF sha256 {ps}); this "
            f"run by head {str(head)[:7]}, script {script_sha256_lf[:8]} (LF sha256 "
            f"{script_sha256_lf})"
            + ("; the same script" if ps == script_sha256_lf else
               "; different code by design (D10 (i): the revision after the pre-run wrote PRERUN_* "
               "into the reading script); the reference is checked by its pins and the column "
               "gate"))
    return {**out, "prerun_git_head": ph, "prerun_script_sha256_lf": ps,
            "same_script": ps == script_sha256_lf, "passed": ok,
            "reason": ("the reference's manifest names the registered head and script" if ok
                       else f"the reference's manifest names head {ph} and script {ps}; "
                            f"registered {PRERUN_GIT_HEAD} and {PRERUN_SCRIPT_SHA256_LF}"),
            "text": text}


def is_the_pinned_store(sha256):
    """Revision 1.6 (A4; Ark 18:00, Zcode 18:05): True only when a --from-raw store's raw sha256
    equals block B's pinned raw_fits.json.gz. False, not vacuously True, when the pins are absent
    (pre-run mode) or the file is absent (sha256 None): before 1.6 the record compared None with
    None. The raw store's key carries no block name, so this sha256 is the only link between a
    loaded store and block B."""
    pinned = (PRERUN_SHA256 or {}).get("raw_fits.json.gz")
    return sha256 is not None and pinned is not None and sha256 == pinned


def check_prerun_reproduced(got, comparable, reread=False, pinned_store=False):
    """Sections 3.3 and 7 (A revisions 3.1, 3.2): the synthetic step must reproduce block B's
    pinned table, PRERUN_DIR/synthetic_worlds.csv, on its deciding columns (csv_compare; outcome
    1 or 2 passes, outcome 3 stops). Every pre-run file is first checked (check_prerun_files).
    Byte identity is recorded, not gated. passed is None when the run is not comparable (smoke,
    or starts != 10), when the table was re-read from saved fits (--from-raw), and in pre-run
    mode (no registered reference: this run makes it). False stops the two-world check.
    Revision 1.6 (A4): a re-read is compared with the pinned table only when its store is block
    B's own pinned store (pinned_store, from is_the_pinned_store); a re-read of any other store
    takes its labels from that store unchecked, so it is not compared and no outcome is
    recorded. passed stays None for every re-read."""
    # port: male check_prerun_reproduced, its pre-run branch (lines 2152-2155) -> S17
    ref_path = PRERUN_DIR / "synthetic_worlds.csv"
    base = {"prerun_path": str(ref_path), "prerun_sha256_pinned": PRERUN_WORLDS_CSV_SHA256,
            "recomputed_sha256": hashlib.sha256(got).hexdigest(),
            "reread_from_saved_fits": bool(reread), "byte_identical": None, "outcome": None}
    if not reference_mode():
        return {**base, "passed": None,
                "reason": "pre-run mode: no registered reference; this run makes it (D10 (i)), so "
                          "there is nothing to reproduce"}
    if not comparable:
        return {**base, "passed": None, "reason": "not comparable (smoke or starts != 10)"}
    files = check_prerun_files()
    base["prerun_files"] = files
    if not files["passed"]:
        return {**base, "passed": None if reread else False,
                "reason": "pre-run files do not match SHA256SUMS.txt and their pins: "
                          + files["reason"]}
    if reread and not pinned_store:
        return {**base, "passed": None, "pinned_store": False,
                "reason": "re-read (--from-raw) of a store that is not block B's pinned "
                          "raw_fits.json.gz (is_the_pinned_store False): its labels come from "
                          "that store unchecked, so it is not compared with the pinned table "
                          "(revision 1.6, A4)"}
    if reread:
        base["pinned_store"] = True
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
              f"(reported, not gated)")
    if reread:
        return {**base, "passed": None,
                "reason": "re-read of block B's pinned store (--from-raw), not a reproduction; "
                          "compared with the pre-run table for information only: " + detail}
    return {**base, "passed": cmp["passed"], "reason": detail}


def raw_fits_diagnostic(F, fresh=None, reread_note=None, ref=None):
    """A revisions 3.2, 3.3 (A1, A6, A8); diagnostic, decides nothing. The fits of this run
    compared with block B's pinned raw_fits.json.gz (or `ref`, that store already read), key by
    key (STORE_FIELDS_COMPARED; secs excluded by name, STORE_FIELDS_EXCLUDED; every field seen
    must be declared in one of the two). S17: split by kind of fit only (ko, full, block, ko1;
    sh for the shuffles, pc for the permuted-block ceilings): block B's reference is made by one
    fitting run, so A's split by the run that fitted each world does not arise."""
    # port: male raw_fits_diagnostic (lines 2183-2235) -> S17
    ref = read_raw(PRERUN_DIR / "raw_fits.json.gz") if ref is None else ref
    fresh = set(fresh or ())
    out = {"kinds": {}}
    counters = ("pinned", "missing_now", "compared", "fitted_this_pass", "p_differ",
                "lambda_differ", "labels_differ", "score_differ", "outside_density_differ",
                "reused_from_ko_differ")
    declared = set(STORE_FIELDS_COMPARED) | set(STORE_FIELDS_EXCLUDED)
    for key, v in ref.items():
        bk, mk, _ = key
        base, *mods = bk.split("|")
        if not base.startswith("world:"):
            continue
        kind = mods[0].split(":")[0] if mods else mk
        s = out["kinds"].setdefault(
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
        # revision 3.4.1 (item A): provenance, compared by key; missing reads False
        s["reused_from_ko_differ"] += (bool(v.get("reused_from_ko", False))
                                       != bool(f.get("reused_from_ko", False)))
    k = out["kinds"].values()
    out["total"] = {n: sum(s[n] for s in k) for n in counters}
    out["total"]["max_abs_dp"] = max((s["max_abs_dp"] for s in k), default=0.0)
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
        # S34: each count over the family's worlds carries its denominator (count_where); the
        # fractions keep A's printed form "seen/n", "R/n" (A section 4's G label).
        seen_c = {pk: count_where(ws, "family", fam,
                                  lambda w, pk=pk: w["rows"][pk]["p_P"] <= P_R)
                  for pk in LIMIT_KEYS}
        seen = {pk: c["k"] for pk, c in seen_c.items()}
        n_r = count_where(ws, "family", fam, lambda w: w["label"] == "R")["k"]
        rows.append({"gamma": g, "family": fam, "dense_grid": fam in M_FAMILIES, "n": len(ws),
                     "seen_of_n": seen_c["rule"]["text"],
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
    measured is counted apart and neither keeps nor renames U. S38: a not-readable U is counted
    apart too, never as a threshold U."""
    dense = [w for w in worlds if w["family"] in M_FAMILIES]
    kinds = [u_kind(w.get("U_reasons")) for w in dense if w["label"] == "U"]
    n_u = len(kinds)
    n_thr, n_failed, n_nm = (kinds.count("threshold"), kinds.count("failed_fit"),
                             kinds.count("not_measured"))
    n_nr = kinds.count("not_readable")                 # S38: counted apart
    order = [f[0] for f in FAMILIES]
    fams = sorted({w["family"] for w in worlds}, key=order.index)
    freq = {}
    for f in fams:                                     # S34: k of n over the family's worlds
        c = count_where(worlds, "family", f, lambda w: w["label"] == "U")
        freq[f] = {"U": c["k"], "n": c["n"]}
    split = (f"{n_thr} threshold U, {n_failed} failed fit, {n_nm} ceiling_block not measured, "
             f"{n_nr} not readable")
    if n_thr:
        text = (f"threshold U read by {n_thr} of {len(dense)} dense-grid worlds ({split}): U "
                "stays; its frequency is printed")
    else:
        text = (f"no dense-grid world read a threshold U (0 of {len(dense)}; {split}): U is "
                f"renamed '{U_UNCALIBRATED}' and is never read as a finding")
    return {"dense_grid_worlds": len(dense), "dense_grid_U": n_u, "n_u_threshold": n_thr,
            "n_u_failed": n_failed, "n_u_not_measured": n_nm, "n_u_not_readable": n_nr,
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
                log(f"FIXED-LAMBDA PATH DIFFERS FROM THE SELECTED FIT on {bk}: {same}")
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


def ko1_count(records):
    """Revision 3.4 (item 3), a registered control since revision 3.4.1 (item A): over ko1
    records, how many were copied from the ko fit (reused_from_ko set, complete_fixed_lambda) and
    how many were fitted (train_fixed_lambda, the fixed-lambda path check included). A record
    without reused_from_ko reads False (missing == False)."""
    records = list(records)
    copied = sum(bool(r.get("reused_from_ko", False)) for r in records)
    return {"ko1_records": len(records), "copied_from_ko": copied,
            "fitted": len(records) - copied}


def registered_ko1_count(ref):
    """Revision 3.4.1 (item A): the registered ko1 count, derived from a store (in run_synthetic,
    the pinned raw_fits.json.gz, read after check_prerun_files has verified it): ko1_count over
    its ko1 records of the world banks. A's pinned store at A's revision 3.4 (A's reference,
    synthetic_rev3_prerun) gives 225 records, 47 copied and 178 fitted (5 of them by the path
    check, on world:W:0). B revision 1.7.1: block B's own pinned store (PRERUN_DIR, B revision
    1.7) gives 225 records, 50 copied and 175 fitted (0 by the path check), recomputed with this
    function on its raw_fits.json.gz (B section 10, "Revision 1.7.1")."""
    return ko1_count(v for (bk, mk, _), v in ref.items()
                     if mk == "ko1" and bk.startswith("world:") and "|" not in bk)


KO1_COUNT_CONTROL = (
    "the provenance split of the ko1 records (reused_from_ko): a fresh synthetic step, comparable "
    "to the reference, must reproduce the registered count read from the pinned "
    "raw_fits.json.gz, or it stops; under --from-raw the count is read from the store this pass "
    "re-reads, so the check is informative; a smoke run or starts != 10 is not compared")


def check_ko1_count(got, registered, comparable, reread, prerun=False, pinned_store=False):
    """A revision 3.4.1 (item A): the ko1 count of this run (ko1_count over the world banks)
    against the registered one (registered_ko1_count on block B's pinned store). passed is True
    or False for a fresh comparable run (False stops the synthetic step), and None (informative)
    under --from-raw, when the run is not comparable, and in pre-run mode (S17: no registered
    store yet; this run's count is registered from the store it writes, B section 3.3).
    Revision 1.6.1 (Ark 18:32; the rule of its twin check_prerun_reproduced): under --from-raw
    the count is compared with the registered value only when the re-read store is block B's own
    pinned store (pinned_store, from is_the_pinned_store); a re-read of any other store is not
    compared and records no equality (equal None). passed stays None for every re-read, so no
    gate changes."""
    # port: male check_ko1_count, its prerun branch (lines 2472-2490) -> S17
    compare = registered is not None and not (reread and not pinned_store)
    equal = got == registered if compare else None
    if prerun:
        passed, status = None, ("pre-run mode: no registered store; this run's count is "
                                "registered from the store it writes (B section 3.3, D10 (i))")
    elif not comparable:
        passed, status = None, "not compared (smoke or starts != 10)"
    elif reread and not pinned_store:
        passed, status = None, ("informative, not compared: under --from-raw of a store that is "
                                "not block B's pinned raw_fits.json.gz (is_the_pinned_store "
                                "False) the count is that store's, unchecked (revision 1.6.1)")
    elif reread:
        passed, status = None, ("informative: under --from-raw the count is read from the store "
                                "this pass re-reads, not produced by this pass")
    else:
        passed, status = equal, "a registered control: a different count stops the synthetic step"
    return {"counted": got, "registered": registered, "equal": equal, "passed": passed,
            "status": status, "control": KO1_COUNT_CONTROL}


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
    In pre-run mode (PRERUN_SHA256 is a placeholder, D10 (i)) the registered values are computed,
    not checked, and there is nothing to reproduce (S17). The caller stops on a failed
    requirement, and writes the synthetic outputs before it prints the tables (S25)."""
    # port: male run_synthetic, its pre-run mode (lines 2522-2679) -> S17
    specs = [w for w in world_specs() if w["family"] in args.families
             and w["j"] < args.worlds_per_family]
    saved = dict(F or {})
    F = dict(saved)
    n_saved = len(F)
    init_args = (args.starts, terms, args.synthetic_only)
    ref_mode = reference_mode()
    groups = []
    for w in specs:
        for g in plan_bank(f"world:{w['family']}:{w['j']}", args.shuffles, args.perm_ceilings):
            g = [t for t in g if t not in F]
            if g:
                groups.append(g)
    fitted_main = sum(len(g) for g in groups)
    comparable = (args.starts == 10 and args.worlds_per_family == WORLDS_PER_FAMILY
                  and args.shuffles == N_SHUFFLES and args.perm_ceilings == N_PERM_CEILINGS
                  and list(args.families) == [f[0] for f in FAMILIES])
    # Revision 3.2 (A3): a --from-raw pass re-reads saved fits; it is not a reproduction.
    reread = getattr(args, "from_raw", None) is not None
    # A revision 3.4.1 (items A, B): the registered values of the smallest_passing_auc check and
    # of the ko1 count are read from block B's pinned reference, so its files are verified first;
    # a failure stops before any fit. Pre-run mode: no reference exists yet.
    if ref_mode:
        prerun_files = check_prerun_files()
        if not prerun_files["passed"]:
            log(f"PRE-RUN REFERENCE NOT VERIFIED: {prerun_files['reason']}; the registered values "
                "of the smallest_passing_auc check and of the ko1 count are read from it, so the "
                "synthetic step stops before any fit, and the real arm does not run (sections "
                "3.3, 7)")
            sys.exit(1)
        spa_reg = derive_smallest_passing_auc(PRERUN_DIR / "synthetic_only.json")
    else:
        spa_reg = {"source": "pre-run mode: computed from each board's labels and uniform_perms()",
                   "passed": True, "by_board": board_smallest_passing_auc(),
                   "n_worlds_by_board": None, "reason": "pre-run mode (S17): no reference; the "
                   "values are registered from this run's synthetic_only.json (B section 3.3)"}
        log("PRE-RUN MODE: PRERUN_SHA256 and PRERUN_WORLDS_CSV_SHA256 are placeholders; this run "
            "makes block B's reference and checks none (D10 (i))")
    source = spa_reg["source"] if not ref_mode else "derived from the pinned synthetic_only.json"
    log(f"smallest_passing_auc registered values ({source}): {spa_reg['by_board']}; worlds by board "
        f"{spa_reg['n_worlds_by_board']}; {spa_reg['reason']}")
    if not spa_reg["passed"]:
        log(f"SMALLEST PASSING AUC REGISTERED VALUES NOT DERIVED: {spa_reg['reason']}; the "
            "synthetic step stops before any fit, and the real arm does not run (sections 3.3, 7)")
        sys.exit(1)
    # A revision 3.4 (item 2): smallest_passing_auc against its registered value by board, before
    # any fit (it depends only on y and Yu). y is read from the saved store where it holds the
    # world's base knockout record (--from-raw), and otherwise from the world generator.
    spa_in = []
    for w in specs:
        bk = f"world:{w['family']}:{w['j']}"
        rec = saved.get((bk, "ko", "N1"))
        y = (rec["y"] if rec is not None
             else make_world(w, terms).exists[BLOCK_CELLS[:, 0], BLOCK_CELLS[:, 1]])
        spa_in.append({"world": bk, "board": w["board"], "y": y})
    spa = check_smallest_passing_auc(spa_in, spa_reg["by_board"])
    spa["registered_source"] = spa_reg
    log(f"smallest_passing_auc check (A revision 3.4, before the fits): {spa['n_equal']} of "
        f"{spa['n_worlds']} worlds equal the value by board {spa['registered_by_board']}; "
        f"{spa['gates']}")
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
    # A revision 3.4 (item 3), 3.4.1 (item A): ko1 records copied from the ko fit and fitted, a
    # registered control against the count derived from the pinned raw_fits.json.gz; in pre-run
    # mode it is recorded, not compared.
    got = ko1_count(F[(bk, "ko1", pk)] for bk in keys for pk in ("rule",) + BF_KEYS)
    n_path = len(path_check.get("identical") or {}) if path_check.get("bank") else 0
    ref_store = (read_raw(PRERUN_DIR / "raw_fits.json.gz") if comparable and ref_mode
                 else None)
    rec = getattr(args, "from_raw_record", None) or {}
    pinned_store = bool(rec.get("is_the_pinned_store"))          # revision 1.6 (A4)
    ko1_check = check_ko1_count(got, registered_ko1_count(ref_store) if ref_store else None,
                                comparable, reread, prerun=not ref_mode,
                                pinned_store=pinned_store)       # revision 1.6.1 (Ark 18:32)
    ko1_check.update(fitted_by_path_check=n_path, path_check_bank=path_check.get("bank"),
                     this_pass={"copied": fl["reused"], "fitted": fl["fitted"] + n_path})
    log(f"ko1 records (A revision 3.4.1; {ko1_check['status']}): {got['ko1_records']}; copied "
        f"from the ko fit (reused_from_ko) {got['copied_from_ko']}; fitted {got['fitted']}, of "
        f"which {n_path} by the fixed-lambda path check ({path_check.get('bank')}); this pass "
        f"copied {fl['reused']} and fitted {fl['fitted'] + n_path}; registered (pinned store) "
        f"{ko1_check['registered']}; equal {ko1_check['equal']}")
    if ko1_check["passed"] is False:
        log(f"KO1 COUNT CHECK FAILED: this run counts {got}, the pinned store registers "
            f"{ko1_check['registered']}; the synthetic step stops, and the real arm does not run "
            "(sections 3.3, 7)")
        sys.exit(1)
    worlds = []
    for w, s in zip(specs, spa["per_world"]):
        ev = evaluate_bank(f"world:{w['family']}:{w['j']}", F, args.shuffles, args.perm_ceilings)
        # A revision 3.4 (item 2): the printed value is the value checked before the fits
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
    repro = check_prerun_reproduced(worlds_csv_bytes(worlds), comparable, reread, pinned_store)
    log(f"pre-run table (section 7): {repro['reason']}; recomputed sha256 "
        f"{repro['recomputed_sha256']}")
    raw_diag = None
    if comparable and repro.get("prerun_files", {}).get("passed"):
        # revision 3.3 (A6): under --from-raw the comparison is marked for what it is
        fresh = {k for k, v in F.items() if saved.get(k) is not v}
        note = None
        if reread:
            if pinned_store:
                note = (f"re-read: compares the pinned store with itself; carries no information "
                        f"(apart from the {len(fresh)} fits this pass made, counted as "
                        f"fitted_this_pass)")
            else:
                note = ("re-read of a store other than the pinned one: compares that store's "
                        f"fits, and the {len(fresh)} fits this pass made, with the pinned ones; "
                        "not a reproduction")
        raw_diag = raw_fits_diagnostic(F, fresh, note, ref_store)
        if note:
            log(f"per-fit diagnostic: {note}")
        log(f"per-fit diagnostic against the pre-run raw fits (decides nothing): "
            f"{raw_diag['total']}")
    syn = {"reference_mode": ref_mode, "worlds": worlds,
           "two_world_check": two_world_check(worlds, repro), "limits": dl,
           "u_rule": ur, "fixed_lambda_summary": fixed_lambda_summary(worlds),
           "fixed_lambda_path_check": path_check, "raw_fits_diagnostic": raw_diag,
           "fits": {"saved_reread": n_saved, "fitted_main": fitted_main, "fixed_lambda": fl,
                    "ko1_count": ko1_check},
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
    log(f"outside density {ev['outside_density']:.4f}; block present {ev['block_present']} of "
        f"{N_BLOCK}; n_deg = {ev['n_deg']} of {ev['rows']['rule']['n_shuffles']}; smallest "
        f"passing AUC (p_P <= 0.01, own draws) = {fmt(ev['smallest_passing_auc'])}")
    log(f"{'predictor':10s} {'AUC':>6s} {'D':>7s} {'LL':>6s} {'LLm':>7s} {'P@np':>5s} "
        f"{'c_full':>6s} {'c_blk':>6s} {'sh_f':>5s} {'sh_b':>5s} {'M_real':>7s} {'n_ge':>4s} "
        f"{'p_S':>5s} {'p_P':>6s} {'p_Prc':>6s}  lambda ko/full/block")
    for pk in PRED_KEYS:
        r = ev["rows"][pk]
        log(f"{r['predictor']:10s} {fmt(r['auc'])} {fmt(r['D'], 3):>7s} {r['logloss']:.3f} "
            f"{r['logloss_margin_over_N1']:+.4f} {fmt(r['precision_at_n_present'], 3)} "
            f"{fmt(r['ceiling_full'])} {fmt(r['ceiling_block'])} "
            f"{fmt(r['regrown_share_full'], 2):>5s} {fmt(r['regrown_share_block'], 2):>5s} "
            f"{r['M_real']:+.4f} {r['n_ge']:4d} {p_s_text(r)} {r['p_P']:.4f} "
            f"{fmt(r['p_P_rowcol'])}  {r['lambda_ko']}/{r['lambda_full']}/{r['lambda_block']}")
    log("(p_P defines leg P and the limits; p_Prc, the row-and-column p_P, is a diagnostic"
        + (f": {ev['rows']['rule']['p_P_rowcol_note']}"
           if ev["rows"]["rule"].get("p_P_rowcol_note") else "")
        + f"; P@np is the precision at n_present = {ev['block_present']}; leg S is decided by "
        "the count n_ge, p_S is information (S36))")
    for pk in PRED_KEYS:
        r = ev["rows"][pk]
        log(f"  {r['predictor']:10s} strata mean p: " + ", ".join(
            f"{k} {v:.3f}" for k, v in r["strata_mean_p"].items())
            + "; mirror partners: " + ", ".join(f"{k} {v:.3f}"
                                                for k, v in r["mirror_partners_p"].items())
            + f"; AUC on the other {N_OTHER_CELLS} = {fmt(r['auc_other_31'])}")
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


def u_positions(worlds, dl):
    """S32: where block B's threshold U worlds of the dense grid lie against block B's own
    gamma*_P: by gamma, and at, below or above it (all below when gamma*_P is not reached)."""
    gamma_of = {f: g for g, f in DENSE_GRID}
    us = sorted(gamma_of[w["family"]] for w in worlds if w["family"] in M_FAMILIES
                and w["label"] == "U" and u_kind(w.get("U_reasons")) == "threshold")
    lp = dl["leg_P"]
    pos = {"at": 0, "below": 0, "above": 0}
    for g in us:
        if not lp["reached"] or g < lp["gamma"]:
            pos["below"] += 1
        elif g == lp["gamma"]:
            pos["at"] += 1
        else:
            pos["above"] += 1
    by = {g: us.count(g) for g in sorted(set(us))}
    return {"n": len(us), "by_gamma": by, "position": pos,
            "all_at_gamma_star_P": bool(us) and pos["at"] == len(us)}


def u_rule_paragraph(syn, real=None):
    """S32: the U-rule paragraph of SYNTHETIC.md and RESULT.md, from block B's own synthetic
    step: the U rule, the gamma of block B's threshold U worlds against block B's own gamma*_P,
    and whether they lie in block A's position (at gamma*_P) or not; A's reading of a threshold U
    is not printed as block B's. S38 (revision 1.4, B section 3.5): the not-readable U is counted
    on a line of its own, never added into the threshold U count."""
    ur, dl, worlds = syn["u_rule"], syn["limits"], syn["worlds"]
    up = u_positions(worlds, dl)
    lp = dl["leg_P"]
    if not up["n"]:
        where = "there are none, so their position says nothing"
    elif up["all_at_gamma_star_P"]:
        where = "all lie at gamma*_P, the position block A's U worlds had (A section 4)"
    else:
        where = "they do not all lie at gamma*_P"
    by = ", ".join(f"{g}: {k}" for g, k in up["by_gamma"].items()) or "none"
    text = (f"**U rule (block B's own U reading, B section 3.6; S32):** {ur['text']}. Block B's "
            f"threshold U worlds on the dense grid: {up['n']} of {ur['dense_grid_worlds']} (by "
            f"gamma: {by}); against block B's own gamma*_P = {lp['text']}: {up['position']['at']} "
            f"at it, {up['position']['below']} below it, {up['position']['above']} above it; "
            f"{where}. Block A's reading of a threshold U as the signature of its leg-P limit is "
            f"block A's and is not carried to block B beyond these positions. A U whose reasons "
            f"include rule #2.1's ceiling_block below {GATE_CUT:.2f} reads '{FAILED_FIT_TEXT}', and "
            f"a U whose ceiling_block was not measured reads '{NOT_MEASURED_TEXT}'; neither is "
            f"renamed. U across all {ur['all_worlds']} worlds: {ur['all_U']} ("
            + ", ".join(f"{f} {v['U']} of {v['n']}" for f, v in ur["frequency_by_family"].items())
            + ").")
    nr = (f"Not-readable U (S38; counted apart, never a threshold U): "
          f"{ur.get('n_u_not_readable', 0)} of {ur['dense_grid_worlds']} dense-grid worlds")
    if real is not None:
        nr += (f"; the real block: {0 if real.get('readable', True) else 1} of 1 "
               f"({'not readable' if not real.get('readable', True) else 'readable'})")
    return [text, "", nr + "."]


def md_check_and_curve(syn, real=None):
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
                     f"{r['n_ge']} / {r['n_valid_shuffles']} | {p_s_text(r)} | {r['p_P']:.4f} | "
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
          + (f"; mechanism_description differences (reported, not gated), first: "
             f"{cmp['first_mechanism_description_differences']}"
             if cmp.get("mechanism_description_differences") else "")
          + ").", "",
          "Per-fit diagnostic against the pre-run raw fits ("
          + (syn["raw_fits_diagnostic"]["status"] if syn.get("raw_fits_diagnostic")
             else "decides nothing") + "): "
          + (f"{syn['raw_fits_diagnostic']['total']}"
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
    L += [""] + md_limits(gs) + [""] + u_rule_paragraph(syn, real) + ["",
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

# S15: block B's own CSV column names (its reference is written by this script, so no
# compatibility with A's CSV is needed): precision_at_n_present, auc_other_31.
CSV_FIELDS = ("predictor", "auc", "D", "logloss", "logloss_margin_over_N1",
              "precision_at_n_present", "ceiling_full", "ceiling_block", "regrown_share_full", "regrown_share_block",
              "M_real", "n_ge", "n_shuffles", "n_deg", "n_valid_shuffles", "p_S", "p_P",
              "p_P_rowcol", "lambda_ko", "lambda_full", "lambda_block", "auc_other_31")
WORLDS_CSV_HEADER = (("family", "j", "seed", "gamma_z", "gamma_z1", "board", "label",
                      "mechanism_description", "outside_density") + CSV_FIELDS
                     + ("auc_fixed_lambda1", "p_P_fixed_lambda1"))  # 33 columns, as revision 3
# Revision 3.2 (A1): the columns of synthetic_worlds.csv by how the reproduction gate compares
# them. Exact: the identity columns of a row, and the lattice columns, whose values are exact
# dyadic or rational fractions with steps of at least 1e-4 (AUCs, p values, counts, lambdas, and
# outside_density, a count over 4,185 cells), so a tolerance adds nothing. Continuous, within
# MACHINE_CHECK_TOL: D, the log-losses, and the regrown_share ratios (not on a lattice).
# Reported, not gated: mechanism_description (column 8).
CSV_EXACT_COLUMNS = ("family", "j", "seed", "gamma_z", "gamma_z1", "board", "predictor",
                     "label", "outside_density", "auc", "precision_at_n_present", "ceiling_full",
                     "ceiling_block", "M_real", "n_ge", "n_shuffles", "n_deg",
                     "n_valid_shuffles", "p_S", "p_P", "p_P_rowcol", "lambda_ko", "lambda_full",
                     "lambda_block", "auc_other_31", "auc_fixed_lambda1", "p_P_fixed_lambda1")
CSV_CONTINUOUS_COLUMNS = ("D", "logloss", "logloss_margin_over_N1", "regrown_share_full",
                          "regrown_share_block")
CSV_REPORTED_COLUMNS = ("mechanism_description",)
assert (sorted(CSV_EXACT_COLUMNS + CSV_CONTINUOUS_COLUMNS + CSV_REPORTED_COLUMNS)
        == sorted(WORLDS_CSV_HEADER)) and len(WORLDS_CSV_HEADER) == 33
# Revision 3.3 (item 37): the fields of a raw_fits.json.gz record, by how raw_fits_diagnostic
# compares them, key by key (a world's base bank and its shuffled banks differ in
# outside_density, so only records of the same key are compared). Excluded by name: secs, a
# timing (the second non-reproducible field after the gzip mtime).
# Revision 3.4 (item 3), the label of the excluded field:
#   secs            non-reproducible (a timing).
# Revision 3.4.1 (item A; Johnny 16:29 #1, Zcode 16:36 UTC; Ark had it at #131), the label of
# reused_from_ko, moved from the excluded to the compared fields:
#   reused_from_ko  provenance of the ko1 record; comparison required. Set (True) on a ko1 record
#                   copied from the ko fit by complete_fixed_lambda; absent on a ko1 record fitted
#                   by train_fixed_lambda. It is not a function of lam: complete_fixed_lambda skips
#                   a ko1 record that already exists, so the five of the fixed-lambda path check's
#                   bank are fitted, bit-equal to their ko fit and unflagged (in the pinned store:
#                   52 base ko fits of rule #2.1 and BF_r at lambda = 1, 47 flagged ko1 records;
#                   the other 5 are world:W:0's). Compared by key on every compared record; a
#                   record without the field reads False (missing == False). The ko1 count it
#                   carries is a registered control (registered_ko1_count, check_ko1_count).
SCORE_FIELDS = ("existence", "offset", "counts", "sign", "sign_n", "n_ne")
STORE_FIELDS_COMPARED = ("p", "y", "lam", "score", "outside_density", "reused_from_ko")
STORE_FIELDS_EXCLUDED = ("secs",)
assert not set(STORE_FIELDS_COMPARED) & set(STORE_FIELDS_EXCLUDED)


def write_worlds_csv(worlds, path):
    Path(path).write_bytes(worlds_csv_bytes(worlds))


def private_run_dir(arm, head):
    """Section 7, S20: where a registered run writes its private and raw outputs, outside the
    repository: connectome-seed-data/knockout_regrow/<arm>_<UTC stamp>_<head 12>, the arm name
    (flyvis65_blockB) keeping block B's folders apart from A's (flyvis65_*)."""
    # port: male private_run_dir(arm, head) (line 2930) -> S20
    return PRIVATE_ROOT / f"{arm}_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}_{head[:12]}"


def protected_references():
    """S18: the reference folders --out must never touch, each with its pins (None when it has
    none yet): A's, block B's own (path only until the pre-run's revision sets its pins), and the
    two male references. Read at call time, so the tests can point them at temporary folders."""
    # port: male protected_references (lines 2936-2941) -> S18
    return ([("A", A_PRERUN_DIR, A_PRERUN_SHA256), ("B", PRERUN_DIR, PRERUN_SHA256)]
            + [(f"male {lobe}", MALE_PRERUN_DIR[lobe], MALE_PRERUN_SHA256[lobe])
               for lobe in ("L", "R")])


def out_dir_refusal(out, arm=None):
    """A revision 3.3 (A2, C4), S18: why --out must not be written, or None. Refused: --out with
    --arm (the real arm writes to private_run_dir); --out at or inside A's, block B's or either
    male reference folder; and a folder that holds a byte copy of a pinned reference (at least
    one file named like a pinned one is present, and every such present file matches its pin). A
    missing pinned-name file is not a differing one; a folder in which no pinned-name file is
    present is not a copy (B section 3.3, revision 1.4 (a)); a reference without pins (block B's
    until the pre-run's revision) is guarded by its path only. Falsifier (A section 7, B section
    3.3 (b)): the content guard tells a copy from a fresh run's folder only because write_raw's
    gzip carries its mtime."""
    # port: male out_dir_refusal (lines 2944-2974) -> S18
    if out is None:
        return None
    if arm:
        return ("REFUSED: --out is not used with --arm; the real arm writes its private outputs "
                "to connectome-seed-data/knockout_regrow/<run> (section 7)")
    target = Path(out).resolve()
    for name, d, pins in protected_references():
        ref = Path(d).resolve()
        if target == ref or target.is_relative_to(ref):
            return (f"REFUSED: --out {target} is {name}'s reference folder or inside it ({ref}); "
                    "write to a new folder (S18; A section 7, 'Recreating the reference')")
    if target.is_dir():
        for name, d, pins in protected_references():
            if not pins:
                continue
            present = {n: hashlib.sha256((target / n).read_bytes()).hexdigest()
                       for n in pins if (target / n).is_file()}
            if present and all(present[n] == pins[n] for n in present):
                return (f"REFUSED: --out {target} holds a byte copy of {name}'s pinned reference "
                        f"(present pinned-name files, each equal to its pin: "
                        f"{', '.join(sorted(present))}); write to a new folder (S18)")
    return None


def write_sha256sums(d):
    """SHA256SUMS.txt over every other file in d (raw bytes, sha256sum's binary format). S29: it
    is called last, after the tee is closed, and only by a run that completed; nothing is written
    to d afterwards. A stopped run writes none (S39)."""
    d = Path(d)
    lines = [f"{hashlib.sha256(p.read_bytes()).hexdigest()} *{p.name}"
             for p in sorted(d.iterdir()) if p.is_file() and p.name != "SHA256SUMS.txt"]
    (d / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def verify_sha256sums(d):
    """S29: every entry of d/SHA256SUMS.txt against the file's raw bytes; the entries that do not
    verify (empty when all do)."""
    d = Path(d)
    bad = []
    for ln in (d / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        if ln.strip():
            h, name = ln.split(maxsplit=1)
            p = d / name.lstrip("*")
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != h:
                bad.append(name)
    return bad


PER_SHUFFLE_COLUMNS = (["sd", "present", "degenerate"]
                       + [f"{a}_{pk}" for pk in PRED_KEYS for a in ("auc", "M", "lam")])
# S33: the header has unique names (A's and the male header wrote auc_N1 twice).
assert len(set(PER_SHUFFLE_COLUMNS)) == len(PER_SHUFFLE_COLUMNS)


def write_per_shuffle_csv(ev, path):
    """S33: per_shuffle.csv; auc_N1 comes once, from the predictor loop."""
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(PER_SHUFFLE_COLUMNS)
        for r in ev["per_shuffle"]:
            r = json_safe(r)
            w.writerow([r[c] for c in PER_SHUFFLE_COLUMNS])


def write_raw(F, path):
    """Every fit's p_exist and labels on the block, so that the worlds can be re-read
    (--from-raw) without refitting. The file is closed (flushed) when this returns (S25)."""
    with gzip.open(path, "wt", encoding="utf-8") as fh:
        json.dump(json_safe({"||".join(k): v for k, v in F.items()}), fh, allow_nan=False)


def read_raw(path):
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        return {tuple(k.split("||")): v for k, v in json.load(fh).items()}


def write_text_synced(path, text):
    """S25: a text file written, flushed and synced before the function returns."""
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
        fh.flush()
        os.fsync(fh.fileno())


def quote_section(start_marker, end_marker):
    """S2: a section of A's registration (as it now stands, pinned by its LF sha256), quoted."""
    text = (ROOT / A_REGISTRATION).read_text(encoding="utf-8")
    s, e = text.index(start_marker), text.index(end_marker)
    return "\n".join(("> " + ln) if ln else ">" for ln in text[s:e].rstrip().splitlines())


def quote_row(label):
    """A section 4's table row for a label, verbatim (lesson f). S2: read from A's registration
    (A_REGISTRATION), never from block B's, which holds no such row. The first line that starts
    with the key is A section 4's, since section 4 precedes section 5 and Amendment 1 is appended
    after A's last line."""
    # port: male quote_row, read from A_REGISTRATION (lines 3014-3023) -> S2
    key = {"R": "| **R: regrows**", "W": "| **W: rule weaker",
           "U": "| **U: on the detection threshold",
           "G": "| **G: not detected at the R level above γ_R**"}[label[0]]
    text = (ROOT / A_REGISTRATION).read_text(encoding="utf-8")
    return next(ln for ln in text.splitlines() if ln.startswith(key))


def md_bank_table(ev):
    # port: male md_bank_table (lines 3026-3041): AUC (n_p/n_a), P@n_present, p_s_text and the
    # row-and-column note -> S15, S36
    L = ["| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | "
         "ceiling_full | ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | "
         "p_P | p_P row-col (diagnostic) | lambda ko/full/block |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for pk in PRED_KEYS:
        r = ev["rows"][pk]
        L.append(f"| {r['predictor']} | {fmt(r['auc'])} ({r['n_present']}/{r['n_absent']}) | "
                 f"{fmt(r['D'], 3)} | {r['logloss']:.4f} | "
                 f"{r['logloss_margin_over_N1']:+.4f} | {fmt(r['precision_at_n_present'], 3)} | "
                 f"{fmt(r['ceiling_full'])} | {fmt(r['ceiling_block'])} | "
                 f"{fmt(r['regrown_share_full'], 2)} | {fmt(r['regrown_share_block'], 2)} | "
                 f"{r['n_ge']} / {r['n_valid_shuffles']} | {p_s_text(r)} | {r['p_P']:.4f} | "
                 f"{r['p_P_rowcol_note'] or fmt(r['p_P_rowcol'])} | {r['lambda_ko']} / "
                 f"{r['lambda_full']} / {r['lambda_block']} |")
    return L


# S31: every quantity B section 3.5 says is printed has a header or a line in RESULT.md; the
# test maps each item to its header string and compares the values with summary.json's.
SECTION_3_5_HEADERS = {
    "strata_means": "Six strata, mean p_exist (B section 3.1)",
    "precision_at_n_present": "P@n_present",
    "mirror_partners": "The 9 mirror partners, p_exist (B section 1.4)",
    "auc_other_31": "AUC on the other 31 cells (not mirror partners)",
    "per_type": "Per-type AUC, the 13 block types (where a type's block cells hold both labels)",
    "perm_ceilings": "Permuted-block ceiling_full of rule #2.1 (20)",
    "fixed_lambda": "Fixed lambda = 1 on the knockout view (diagnostic, decides nothing)",
    "D_N1_logit": "D(N1 logit), former check 5 (printed, decides nothing)",
    "n1_p_P_beside_U": "N1's own p_P beside this U (decides nothing; B section 3.5)"}


def md_section_3_5(real, checks):
    """S31: the section 3.5 quantities of the real block as tables and lines of RESULT.md."""
    H35 = SECTION_3_5_HEADERS
    rows = real["rows"]
    L = [f"**{H35['strata_means']}:**", "",
         "| predictor | " + " | ".join(STRATA) + " |",
         "|---|" + "---|" * len(STRATA)]
    L += [f"| {rows[pk]['predictor']} | "
          + " | ".join(f"{rows[pk]['strata_mean_p'][k]:.3f}" for k in STRATA) + " |"
          for pk in PRED_KEYS]
    mp = list(rows["rule"]["mirror_partners_p"])
    L += ["", f"**{H35['mirror_partners']}** and **{H35['auc_other_31']}:**", "",
          "| predictor | " + " | ".join(mp) + f" | {H35['auc_other_31']} |",
          "|---|" + "---|" * (len(mp) + 1)]
    L += [f"| {rows[pk]['predictor']} | "
          + " | ".join(f"{rows[pk]['mirror_partners_p'][k]:.3f}" for k in mp)
          + f" | {fmt(rows[pk]['auc_other_31'])} |" for pk in PRED_KEYS]
    L += ["", f"**{H35['per_type']}:**", "",
          "| predictor | " + " | ".join(SOURCES + TARGETS) + " |",
          "|---|" + "---|" * len(SOURCES + TARGETS)]
    L += [f"| {rows[pk]['predictor']} | "
          + " | ".join(fmt(rows[pk]["per_type_auc"][n], 2) for n in SOURCES + TARGETS) + " |"
          for pk in PRED_KEYS]
    L += ["", f"**{H35['perm_ceilings']}:** "
          + ", ".join(fmt(x, 3) for x in real["perm_ceilings_full_rule"])
          + f" (real block {fmt(rows['rule']['ceiling_full'])}).", "",
          f"**{H35['fixed_lambda']}:**", "",
          "| predictor | lambda | AUC | p_P | selected lambda | AUC at the selected lambda |",
          "|---|---|---|---|---|---|"]
    L += [f"| {v['predictor']} | {lam_text(v['lambda'])} | {fmt(v['auc'])} | {v['p_P']:.4f} | "
          f"{lam_text(v['selected_lambda'])} | {fmt(v['selected_auc'])} |"
          for v in real["fixed_lambda"].values()]
    d = (checks.get("5_n1_parity") or {}).get("D_N1_logit")
    L += ["", f"**{H35['D_N1_logit']}:** {fmt(d, 6)}."]
    if real["label"] == "U":
        L += ["", f"**{H35['n1_p_P_beside_U']}:** {rows['N1']['p_P']:.4f}."]
    return L


def md_synthetic(syn, real=None):
    L = md_check_and_curve(syn, real)
    for w in syn["worlds"]:
        L += [f"### World {w['family']}, seed {w['seed']}: {w['label_text']}", "",
              f"Outside density {w['outside_density']:.4f}; block present {w['block_present']} "
              f"of {N_BLOCK}.",
              f"Verdict line: {w['verdict_line']}", ""] + md_bank_table(w) + [""]
    return L


def write_synthetic_outputs(out, syn, F, manifest):
    """Section 7: the synthetic step's outputs. S25: called before the synthetic tables are
    printed, in both modes. S29: no SHA256SUMS.txt here; the sums are written last, by main,
    after the tee is closed and only when the run completed."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    manifest["log_output_errors"] = _LOG["output_errors"]
    write_text_synced(out / "synthetic_only.json", dump_json({"manifest": manifest, **syn}))
    write_worlds_csv(syn["worlds"], out / "synthetic_worlds.csv")
    write_raw(F, out / "raw_fits.json.gz")
    md = [f"# Knock out and regrow, block B: synthetic step ({manifest['mode']})", "",
          f"Registration `{REGISTRATION}`, revision {REGISTRATION_REVISION}. "
          f"{'SMOKE RUN, NOT THE REGISTERED RUN. ' if manifest['smoke'] else ''}"
          f"{manifest['not_a_reference'] + '. ' if manifest.get('not_a_reference') else ''}"
          f"git_head={manifest['git_head']}, runtime={manifest.get('runtime_s', 0):.0f}s.", ""]
    md += md_synthetic(syn)
    write_text_synced(out / "SYNTHETIC.md", "\n".join(md) + "\n")
    log(f"wrote {out}")


def write_verdict_json(private, real):
    """S25: the real block's verdict lines on disk (verdict.json in the private folder), written
    and synced before the first print of the real block's table or verdict."""
    write_text_synced(Path(private) / "verdict.json", dump_json({
        "label": real["label"], "label_text": real["label_text"],
        "verdict_line": real["verdict_line"], "quoted_row": real["quoted_row"],
        "a_literals_line": real["a_literals_line"],
        "conditional_lines": real["conditional_lines"]}) + "\n")


BLOCK_B_HEADER_LINE = ("Block B is the second block tested on this bank, chosen after block A's "
                       "verdict G; each block is read on its own, block A's G stands, and the "
                       "cuts are not corrected for two blocks (B section 5, D11). Block B runs on "
                       "the same averaged template as block A, so its label is no evidence for "
                       "or against averaging (B section 0).")


def write_committed(summary, syn, real):
    """Section 7, S19, S31: RESULT.md, summary.json, per_shuffle.csv, synthetic_worlds.csv
    (aggregates) in OUT."""
    OUT.mkdir(parents=True, exist_ok=True)
    summary["manifest"]["log_output_errors"] = _LOG["output_errors"]
    (OUT / "summary.json").write_text(dump_json(summary), encoding="utf-8", newline="\n")
    write_per_shuffle_csv(real, OUT / "per_shuffle.csv")
    write_worlds_csv(syn["worlds"], OUT / "synthetic_worlds.csv")
    t = summary["checks"]["4_pre_data_tables"]
    man = summary["manifest"]
    prov = man.get("prerun_provenance") or {}
    md = ["# Knock out and regrow: block B on flyvis-65", "",
          f"Registration `{REGISTRATION}`, revision {REGISTRATION_REVISION} (a delta on "
          f"`{A_REGISTRATION}`, pinned by its LF sha256 {A_REGISTRATION_SHA256_LF_AMENDED}). "
          f"git_head={man['git_head']}, runtime={summary['runtime_s']:.0f}s.", "",
          BLOCK_B_HEADER_LINE, "",
          f"Code (S37): {prov.get('text') or 'no registered pre-run reference was read'}.", "",
          f"Earlier real-arm runs of this arm (S27): {man['earlier_real_arm_runs']['text']}.", "",
          f"**Verdict: {real['verdict_line']}**", "",
          "The section 4 row of A, verbatim:", "", "> " + real["quoted_row"], ""]
    md += [ln + "\n" for _, ln in real["conditional_lines"]]
    md += [WITHIN_FLY_NOTE + ".", "",
           "## Section 3.5 (flyvis-65, the real block B)", ""] + md_bank_table(real)
    md += [""] + md_section_3_5(real, summary["checks"])
    md += ["", f"The limits (block B's own, B section 3.6): {limits_text(syn['limits'])}. "
           f"Binomial note: {syn['limits']['binomial_note']['text']}. Private and raw outputs: "
           f"{man['private_outputs']}.", "",
           "## Pre-data table (section 1.4)", "",
           f"Endpoint table's sha256 {t['endpoints_sha256']} (registered {ENDPOINTS_SHA256}).", "",
           "| endpoint | kept (as in section 1.4) |", "|---|---|"]
    md += [f"| {k} | {v} |" for k, v in (t.get("endpoints") or {}).items()]
    md += ["", f"Inferable block cells: {t['inferable']} of {N_BLOCK}. Mirror cells: "
           f"{t['mirrors']}. Training present cells: "
           f"{t.get('training_present')} of {N_TRAIN_CELLS} (printed, not checked; D3).", ""]
    md += [""] + md_synthetic(syn, real)
    md += ["## The registered reading (A section 4, quoted)", "",
           quote_section("## 4. Reading rule", "## 5. What each outcome means"), ""]
    (OUT / "RESULT.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
    log(f"wrote {OUT}")


# ------------------------------------------------------------------------------------------
# S27: the record of earlier real-arm runs, read at run time (block B has no seal).

def find_earlier_runs(root, arm):
    """S27 (revision 1.3: three outcomes, each with the scope searched): (a) the root does not
    exist; (b) the root exists and cannot be read; (c) the root was read, and N folders
    <arm>_* holding the real-arm marker were found (N = 0 included). (a) and (b) are never
    written as "0 found" (S34's rule applied to the search)."""
    root = Path(root)
    if not root.exists():
        return {"outcome": "missing", "root": str(root), "folders": None,
                "text": EARLIER_RUNS_TEXT["missing"].format(root=root)}
    try:
        entries = list(root.iterdir())
        found = sorted(p.name for p in entries if p.is_dir() and p.name.startswith(f"{arm}_")
                       and (p / REAL_ARM_MARKER).is_file())
    except OSError as e:
        return {"outcome": "unreadable", "root": str(root), "folders": None,
                "text": EARLIER_RUNS_TEXT["unreadable"].format(root=root, error=repr(e))}
    names = (": " + ", ".join(found)) if found else ""
    return {"outcome": "read", "root": str(root), "folders": found,
            "text": EARLIER_RUNS_TEXT["read"].format(root=root, arm=arm, n=len(found),
                                                     names=names)}


# ------------------------------------------------------------------------------------------
# S35: fenced drafts inside a registration are marked.

FENCE_MARKER = "**Fenced draft, not a section.**"
_FENCE_OPEN = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def fences(text):
    """S35: the fenced blocks of a Markdown text: (opening line number, 1-based; closing line
    number or None when unclosed)."""
    out, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        m = _FENCE_OPEN.match(lines[i])
        if not m:
            i += 1
            continue
        tick, start = m.group(1), i
        i += 1
        while i < len(lines) and not lines[i].lstrip().startswith(tick):
            i += 1
        out.append((start + 1, i + 1 if i < len(lines) else None))
        i += 1
    return out


def unmarked_fences(text):
    """S35: the opening line numbers of the fences not introduced by FENCE_MARKER within the two
    lines before them (empty when every fence is marked)."""
    lines = text.splitlines()
    return [o for o, _ in fences(text)
            if not any(FENCE_MARKER in ln for ln in lines[max(0, o - 3):o - 1])]


def headings(text):
    """S35: the file's own Markdown headings; a heading inside a fence is never counted."""
    inside = set()
    for o, c in fences(text):
        inside.update(range(o, (c or len(text.splitlines())) + 1))
    return [ln for k, ln in enumerate(text.splitlines(), start=1)
            if k not in inside and re.match(r"^#{1,6} ", ln)]


# ------------------------------------------------------------------------------------------

def check_harness_identity(a, terms):
    """Check 8 (real arm only): BF_1's full-bank C6 existence margin over N1, through the
    harness's cv folds, equals 0.028150051052145946 to 1e-9."""
    groups = [[("real", f"cv:{f}", pk)] for pk in ("BF:1", "N1") for f in range(H.N_FOLDS)]
    det = run_groups(groups, a.workers, (a.starts, terms, False), "check 8")
    bf = [det[("real", f"cv:{f}", "BF:1")]["score"] for f in range(H.N_FOLDS)]
    n1s = [det[("real", f"cv:{f}", "N1")]["score"] for f in range(H.N_FOLDS)]
    m = H.margin(bf, n1s, "existence")
    if abs(m - BF1_FULL_BANK_MARGIN) > IDENTITY_TOL:
        log(f"HARNESS IDENTITY FAILS: BF_1 margin {m!r}, registered {BF1_FULL_BANK_MARGIN!r}")
        sys.exit(1)
    return {"BF1_margin": m, "registered": BF1_FULL_BANK_MARGIN,
            "difference": m - BF1_FULL_BANK_MARGIN, "passed": True}


def machine_checks_real(a, terms, checks, y_real):
    """Section 3.4 checks 5, 6, 8, 9 (real arm only; check 3 runs before them). Check 5 is a
    print (S9)."""
    n1_ko = H.fit_n1(H.make_view(real_bank(), MASKS["ko"]))
    checks["5_n1_parity"] = check_n1_parity(n1_ko, y_real)
    log(f"check 5 (N1 parity, printed, decides nothing; D6): D(N1 logit) = "
        f"{fmt(checks['5_n1_parity']['D_N1_logit'], 6)}")
    groups = [[("real", "ko#hash#0", "rule")], [("real", "ko#hash#1", "rule")],
              [("real|leak", "ko#hash#0", "rule")]]
    det = run_groups(groups, a.workers, (a.starts, terms, False), "checks 6, 9")
    h0 = det[("real", "ko#hash#0", "rule")]["data_sha256"]
    h1 = det[("real", "ko#hash#1", "rule")]["data_sha256"]
    hl = det[("real|leak", "ko#hash#0", "rule")]["data_sha256"]
    if h0 != hl:
        log("BLOCK LEAKS INTO TRAINING")
        sys.exit(1)
    checks["6_leakage"] = {"knockout_sha256": h0, "permuted_block_knockout_sha256": hl,
                           "passed": True}
    checks["8_harness_identity"] = check_harness_identity(a, terms)
    if h0 != h1:
        log("NOT DETERMINISTIC")
        sys.exit(1)
    checks["9_determinism"] = {"sha256_fit_1": h0, "sha256_fit_2": h1, "passed": True}
    log("checks 6 (leakage), 8 (harness identity), 9 (determinism): passed")


NOT_A_REFERENCE_TEXT = ("NOT A REFERENCE: a full --synthetic-only run made with --allow-dirty "
                        "from an uncommitted tree; block B's reference is made from a committed "
                        "head (D10 (i))")
# Revision 1.6.1 (Ark 18:32): a --synthetic-only run not in the registered form (a smoke option
# or --starts != 10) is marked too, with its own reason; the mark names the actual cause.
NOT_A_REFERENCE_FORM_TEXT = ("NOT A REFERENCE: a --synthetic-only run not in the registered form "
                             "(a smoke option or --starts != 10); block B's reference is a full "
                             "run with --starts 10 from a committed head (S17, D10 (i))")


def not_a_reference_text(dirty, comparable):
    """Revision 1.6.1 (Ark 18:32), S40: the NOT A REFERENCE mark with its actual cause, or None.
    Being a reference needs both the registered form (comparable: no smoke option, --starts 10)
    and a clean committed tree. A comparable dirty run (--allow-dirty) carries
    NOT_A_REFERENCE_TEXT, as in revision 1.5; a non-registered form carries
    NOT_A_REFERENCE_FORM_TEXT, naming the uncommitted tree as well when there is one."""
    if comparable and not dirty:
        return None
    if comparable:
        return NOT_A_REFERENCE_TEXT
    return NOT_A_REFERENCE_FORM_TEXT + ("; also from an uncommitted tree" if dirty else "")
FROM_RAW_OUT_REFUSED_TEXT = ("REFUSED: block B's reference is made by one fresh fitting run "
                             "(S17, D10 (i)); an --out folder can be a reference, and a re-read "
                             "is not one. Run --from-raw without --out.")


def arm_gate(a, head):
    """Revision 1.7.2 (S27, S37; the reviewers' vote on 1.7.1): the real arm's checks that can
    refuse without reading the bank, run in main before the private folder and REAL_ARM_MARKER
    exist and before real_bank() is called, so that a refusal shows nothing of block B (no check 3
    line, no section 1.4 table) and leaves no folder and no marker. In _run's order: check 1
    (pins, versions, rule #2.1, A's registration, S2), check 2 (block and mask: pure geometry on
    an empty H.Bank("geometry", {}), no real cell), check 7 (AUC function on hand-made inputs),
    the seeds (section 3.7), and the pre-run's provenance (S37, with check_prerun_files). The
    results are handed to _run, which logs them at their places in section 7's order (the log's
    order is unchanged; only the PRE-RUN PROVENANCE DIFFERS line of a refusal moves ahead of the
    first line). The gate holds every check that refuses without reading the bank (five today);
    the ones that guard the show are why the rule exists (revision 1.7.3, T2; no behaviour
    changed)."""
    pins = check_pins()
    block_and_mask = check_block_and_mask()
    auc_function = check_auc_function()
    seeds = assert_seeds_unique(a.starts)
    # S37 moved here from _run (revision 1.7.2). Safe to move: prerun_provenance's verdict
    # ("passed") depends only on PRERUN_DIR's content (check_prerun_files and the manifest of
    # synthetic_only.json) and the registered constants (PRERUN_SHA256, PRERUN_GIT_HEAD,
    # PRERUN_SCRIPT_SHA256_LF); its arguments, this run's head and script hash, enter only its
    # record and its text. check_registered_constants has already passed in the arm, so
    # reference_mode() holds here and check_prerun_files never meets pre-run mode's placeholder.
    prov = prerun_provenance(head, sha256_lf(Path(__file__)))
    if not prov["passed"]:
        # By design, a refusal here leaves only the console (stdout and stderr): the line goes to
        # the log's buffer and no folder exists to receive it. Do not "fix" this by creating the
        # folder earlier: no folder and no marker before the reference and the pins are verified
        # is the rule (revision 1.7.2).
        log(f"{PROVENANCE_DIFFERS_TEXT} (S37): {prov['reason']}; no fit was made")
        sys.exit(1)
    return {"pins": pins, "block_and_mask": block_and_mask, "auc_function": auc_function,
            "seeds": seeds, "prov": prov}


def main(argv=None):
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--synthetic-only", action="store_true",
                      help="steps 1-3 only; touches no real block cell")
    mode.add_argument("--arm", choices=["flyvis65_blockB"])          # S20
    ap.add_argument("--starts", type=int, choices=[3, 10], default=10)
    ap.add_argument("--workers", type=int, default=30)
    ap.add_argument("--out", default=None, help="with --synthetic-only: where to write")
    ap.add_argument("--allow-dirty", action="store_true",
                    help="real arm: not the registered run; --synthetic-only: a full run from "
                         "an uncommitted tree, marked NOT A REFERENCE")
    ap.add_argument("--from-raw", default=None,
                    help="with --synthetic-only: re-read an earlier run's raw_fits.json.gz and "
                         "fit only what it lacks (new worlds, fixed-lambda fits); a diagnostic, "
                         "refused with --out (revision 1.6, A4)")
    ap.add_argument("--smoke-worlds", type=int, default=None, help="worlds per family (smoke)")
    ap.add_argument("--smoke-shuffles", type=int, default=None, help="shuffles per bank (smoke)")
    ap.add_argument("--smoke-perm-ceilings", type=int, default=None)
    ap.add_argument("--smoke-families", default=None, help="comma-separated subset (smoke)")
    a = ap.parse_args(argv)
    t0 = time.time()
    _LOG["buffer"].clear()
    _LOG["output_errors"] = 0
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
    if a.arm:
        check_registered_constants()                   # S17, S37 (D10 (i))
    # A revision 3.3 (A2, C4), S18: before any write or mkdir, --out is refused at or inside a
    # reference folder, on a byte copy of a pinned one, and with --arm.
    refusal = out_dir_refusal(a.out, a.arm)
    if refusal:
        sys.exit(refusal)
    H.STARTS = a.starts
    head = git("rev-parse", "HEAD")
    not_a_reference = None
    gate, prov = None, None
    if a.arm:
        dirty = refuse_if_dirty(a.allow_dirty)
        earlier = find_earlier_runs(PRIVATE_ROOT, a.arm)        # S27, before this run's folder
        # Revision 1.7.2: nothing is shown and no folder or marker exists until every check that
        # can refuse without reading the bank has passed (arm_gate: pins, block and mask, AUC
        # function, seeds, the pre-run's provenance). REAL_ARM_STARTED.json therefore means "the
        # reference and the pins verified, the arm began"; a run that fails later still leaves it.
        gate = arm_gate(a, head)
        prov = gate["prov"]
        folder = private_run_dir(a.arm, head)
        folder.mkdir(parents=True, exist_ok=False)
        write_text_synced(folder / REAL_ARM_MARKER, dump_json(
            {"arm": a.arm, "head": head, "started_utc": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime())}) + "\n")
    else:
        # port: male run_synthetic_only, its dirty-tree refusal (lines 3721-3727) -> S40
        # A tightening relative to A (A's --synthetic-only recorded the tree state; B refuses):
        # block B's reference (D10 (i)) cannot be made from an uncommitted tree without the
        # NOT A REFERENCE mark (log, manifest, SYNTHETIC.md).
        # Revision 1.6 (A4; Ark 17:58 and 18:00, Zcode 18:05, Johnny 17:54): block B's
        # reference is made by one fresh fitting run (S17, D10 (i)). The raw store's key
        # ("||".join(k), write_raw/read_raw) carries no block name and a loaded store is not
        # checked against block B, so a re-read cannot make a folder that could be pinned:
        # --from-raw with --out is refused before any folder is made; without --out it is a
        # diagnostic (the male section 3.3.1 (h) precedent).
        if a.from_raw and a.out:
            sys.exit(FROM_RAW_OUT_REFUSED_TEXT)
        dirty = tree_state()
        comparable = not smoke and a.starts == 10
        if dirty and comparable and not a.allow_dirty:
            sys.exit("REFUSED: a full --synthetic-only run makes block B's reference, which must "
                     "come from a committed head (D10 (i)); commit first, or pass --allow-dirty to "
                     "run it as NOT A REFERENCE.\n" + dirty)
        # Revision 1.6.1 (Ark 18:32): "or not comparable" (was "and comparable"): a reference
        # needs the registered form and a clean committed tree; for a comparable run this equals
        # "dirty", so the pre-run is unchanged.
        not_a_reference = (not_a_reference_text(dirty, comparable) if (dirty or not comparable)
                           else None)
        earlier = None                                 # S27 runs in the real arm only
        folder = Path(a.out) if a.out else None
        if folder is not None:
            folder.mkdir(parents=True, exist_ok=True)
    _RUN.update(folder=folder, arm=a.arm or "synthetic-only", head=head)
    if folder is not None:
        tee_to(folder / "stdout.log")                  # S24, S29
    completed = False
    try:
        result = _run(a, t0, smoke, head, dirty, folder, earlier, not_a_reference, gate, prov)
        completed = True
    finally:
        untee()
        _RUN.update(folder=None, arm=None, head=None)
    # S29: the sums, last, after the tee is closed, only for a run that completed (a stopped run
    # writes none, S39); nothing is written to these folders afterwards.
    if completed and folder is not None:
        write_sha256sums(folder)
        if a.arm:
            # S29, read literally (revision 1.5, OPEN 3): the committed folder OUT gets its sums
            # too, a delta from A (A's committed folder had none); .gitignore does not cover
            # the file, and it is committed with the registered run's artifacts. Revision 1.6
            # (Ark, Zcode; item 44): these sums cover the committed folder's files and are not a
            # reference pin; they are never compared with PRERUN_SHA256.
            write_sha256sums(OUT)
    return result


def _run(a, t0, smoke, head, dirty, folder, earlier, not_a_reference, gate=None, prov=None):
    """Section 7's order: pins; machine checks (check 3 and the pre-data table before any fit on
    the real bank); the pre-run's provenance before any fit (S37); the synthetic step, its
    outputs on disk before its tables are printed (S25); then, in the real arm, the real block,
    its fits and verdict lines on disk before any print of them (S25), and the outputs.
    Revision 1.7.2: in the real arm, checks 1, 2 and 7, the seeds and the provenance have run in
    main (arm_gate) before the folder existed; gate and prov carry their results, logged here at
    their places, and prov enters the manifest as before. In --synthetic-only (gate None) they
    run here, as in 1.7.1."""
    pins = gate["pins"] if gate else check_pins()
    log(f"registration: {REGISTRATION}, revision {REGISTRATION_REVISION}; A's registration LF "
        f"sha256 {pins['a_registration_sha256_lf']} (pinned after Amendment 1; S2); "
        f"{'SYNTHETIC ONLY' if a.synthetic_only else 'arm ' + a.arm}"
        f"{'; SMOKE, not the registered run' if smoke else ''}"
        f"{'; ' + not_a_reference if not_a_reference else ''}; k = {a.starts}; "
        f"workers = {a.workers}; CPU (the pinned harness is numpy-only, section 7)")
    log(f"check 1 (pins, versions, rule #2.1 RANK = 1, A's registration): passed; Python "
        f"{pins['python']}, numpy {pins['numpy']}")
    if earlier is not None:
        log(f"earlier real-arm runs of this arm (S27): {earlier['text']}")

    # Step 2: machine checks (section 3.4). Checks 3, 5, 6, 8 and 9 read the real block or fit a
    # rule on the real bank, so they run in the real arm only.
    checks = {"1_pins": pins,
              "2_block_and_mask": gate["block_and_mask"] if gate else check_block_and_mask()}
    log(f"check 2 (block and mask): passed; {N_TRAIN_CELLS} training cells, {N_BLOCK} block "
        "cells, block A's 64 cells in training")
    bank = real_bank()
    y_real = None
    if a.arm:
        y_real = bank.exists[BLOCK_CELLS[:, 0], BLOCK_CELLS[:, 1]]
        checks["3_block_print"] = check_block_print(y_real)
    tables = pre_data_tables(bank)                     # outside-block presence only
    checks["4_pre_data_tables"] = check_pre_data_tables(tables, real_arm=bool(a.arm))
    log(f"check 4 (pre-data table of section 1.4): passed; endpoint table sha256 "
        f"{tables['endpoints_sha256']} = registered; inferable {tables['inferable']} of "
        f"{N_BLOCK}; mirrors {tables['mirrors']}")
    if a.arm:
        log(f"section 1.4 table (printed at run start, D2 (ii)): {tables['endpoints']}; training "
            f"present cells {tables['training_present']} of {N_TRAIN_CELLS} (printed, not "
            "checked; D3)")
    checks["7_auc_function"] = gate["auc_function"] if gate else check_auc_function()
    log("check 7 (AUC function on hand-made inputs): passed")
    seeds = gate["seeds"] if gate else assert_seeds_unique(a.starts)
    log(f"seeds (section 3.7): {seeds}")
    # S37: which code made the reference, before any fit (degree_terms is the first). Revision
    # 1.7.2: the real arm checked it in main (arm_gate) before its folder existed; here it runs
    # for --synthetic-only in reference mode only (the one-time --from-raw diagnostic re-read goes
    # through it), never twice in the arm, and never in pre-run mode.
    if reference_mode() and not a.arm:
        prov = prerun_provenance(head, sha256_lf(Path(__file__)))
        if not prov["passed"]:
            log(f"{PROVENANCE_DIFFERS_TEXT} (S37): {prov['reason']}; no fit was made")
            sys.exit(1)
    if prov is not None:
        log(f"pre-run provenance (S37): {prov['text']}")
    terms = degree_terms()
    log(f"section 3.6 degree terms: N1 (c, a, b) fitted on the real bank's knockout view of block "
        f"B ({N_TRAIN_CELLS} cells outside block B; no block-B cell read); c = {terms[0]:+.4f}, "
        f"a in [{terms[1].min():+.3f}, {terms[1].max():+.3f}], "
        f"b in [{terms[2].min():+.3f}, {terms[2].max():+.3f}]")
    if a.arm:
        machine_checks_real(a, terms, checks, y_real)

    # A revision 3.3 (B6): the --from-raw file with its sha256 and whether it exists.
    a.from_raw_record = None
    if a.from_raw:
        fr = Path(a.from_raw)
        a.from_raw_record = {"path": str(fr), "exists": fr.is_file(),
                             "sha256": (hashlib.sha256(fr.read_bytes()).hexdigest()
                                        if fr.is_file() else None)}
        a.from_raw_record["is_the_pinned_store"] = is_the_pinned_store(
            a.from_raw_record["sha256"])
    private = folder if a.arm else None
    manifest = {"registration": REGISTRATION, "revision": REGISTRATION_REVISION,
                "registration_sha256_lf": sha256_lf(ROOT / REGISTRATION),
                "a_registration": A_REGISTRATION,
                "a_registration_sha256_lf": pins["a_registration_sha256_lf"],
                "a_registration_flyvis65_text_sha256_lf": A_REGISTRATION_SHA256_LF_FLYVIS65,
                "script_sha256_lf": sha256_lf(Path(__file__)), "git_head": head,
                "tree_dirty_under_c6_or_plans": bool(dirty),
                "tree_dirty_paths": dirty.splitlines() if dirty else [],
                "allow_dirty": bool(a.allow_dirty),
                "not_the_registered_run": (NOT_REGISTERED_TEXT if a.arm and a.allow_dirty
                                           else None),
                "not_a_reference": not_a_reference,
                "mode": "synthetic-only" if a.synthetic_only else a.arm, "smoke": smoke,
                "worlds_per_family": a.worlds_per_family, "shuffles": a.shuffles,
                "perm_ceilings": a.perm_ceilings, "families": a.families, "starts": a.starts,
                "workers": a.workers, "python": pins["python"], "numpy": pins["numpy"],
                "device": "CPU", "from_raw": a.from_raw, "from_raw_record": a.from_raw_record,
                "run_folder": str(folder) if folder is not None else None,
                "private_outputs": str(private) if private else None,
                "reference_mode": reference_mode(), "prerun_dir": str(PRERUN_DIR),
                "prerun_worlds_csv_sha256": PRERUN_WORLDS_CSV_SHA256,
                "prerun_sha256": PRERUN_SHA256, "prerun_provenance": prov,
                "earlier_real_arm_runs": earlier,
                "command_environment": command_environment(),          # S28
                "log_output_errors": _LOG["output_errors"],            # S24
                "machine_record": machine_record(),
                "degree_terms": {"c": terms[0], "a": terms[1], "b": terms[2],
                                 "source": "N1 on the real bank's knockout view of block B "
                                           "(cells outside block B)"}}

    # Step 3: the synthetic worlds, the pre-run reproduction and the two-world check (3.6, 7).
    syn, F = run_synthetic(a, terms, read_raw(a.from_raw) if a.from_raw else None)
    rp = syn["two_world_check"]["prerun_reproduction"]
    # A revision 3.2 (A1): byte identity with the pre-run table is a recorded fact, not the gate.
    manifest["prerun_csv_byte_identical"] = rp["byte_identical"]
    manifest["prerun_comparison_outcome"] = rp["outcome"]
    manifest["prerun_reread_from_saved_fits"] = rp["reread_from_saved_fits"]
    manifest["prerun_comparison_outcome_3_parts"] = rp.get("outcome_3_parts")
    manifest["null_input_digests"] = null_input_digests()      # A revision 3.3 (F10)
    manifest["runtime_s"] = time.time() - t0
    # S25 (revision 1.3, both modes): the synthetic step's fits and outputs on disk before the
    # first print of its tables.
    if folder is not None:
        write_synthetic_outputs(folder, {**syn, "checks": checks, "seeds": seeds}, F, manifest)
    print_synthetic(syn)
    log(f"null-input digests (A revision 3.3): {manifest['null_input_digests']}")
    log(f"machine record (A revision 3.2): thread variables "
        f"{manifest['machine_record']['thread_env']}; machine "
        f"{manifest['machine_record']['machine']}")
    treatment = (repro_fail_treatment(rp.get("outcome_3_parts") or ("a", "b"))
                 if rp["passed"] is False else "")
    if not syn["two_world_check"]["passed"]:
        log("TWO-WORLD CHECK FAILED: a requirement marked stop failed, or the pre-run table was "
            "not reproduced (outcome 3); the real arm does not run (sections 3.6, 7). No real "
            f"block score was computed. Run folder: {folder}. " + treatment)
        # S29 (revision 1.5, OPEN 4): the folder of a run that did not complete has no
        # SHA256SUMS.txt, this exit included (A wrote them before this exit).
        sys.exit(1)
    if a.synthetic_only:
        log(f"\n--synthetic-only: stopped before any real block score. {time.time() - t0:.0f}s")
        return {**syn, "manifest": manifest}

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
    real["quoted_row"] = quote_row(real["label"])
    real["a_literals_line"] = a_literals_line(real, syn["limits"], syn["u_rule"],
                                              checks["4_pre_data_tables"]["inferable"])
    real["conditional_lines"] = conditional_lines(real, syn["limits"], syn["u_rule"],
                                                  checks["4_pre_data_tables"]["inferable"])
    # S25: the real fits and the verdict lines on disk before any print of the real block.
    write_raw(Fr, private / "raw_fits_real.json.gz")
    write_verdict_json(private, real)
    manifest["null_input_digests"] = null_input_digests()      # now with the real block's y

    # Step 5: the verdict, section 3.5, outputs.
    print_bank(real, "flyvis-65, the real block B (section 3.5)")
    log(f"quoted A section 4 row: {real['quoted_row']}")
    for _, ln in real["conditional_lines"]:
        log(ln)
    log(f"D(N1 logit), former check 5 (printed, decides nothing): "
        f"{fmt(checks['5_n1_parity']['D_N1_logit'], 6)}")
    log(WITHIN_FLY_NOTE)
    log(f"\nVERDICT: {real['verdict_line']}")
    summary = {"manifest": manifest, "checks": checks, "seeds": seeds, "real": real,
               "synthetic": syn, "runtime_s": time.time() - t0}
    write_committed(summary, syn, real)
    log(f"wall-clock {summary['runtime_s']:.0f}s")
    return summary


if __name__ == "__main__":
    main()
