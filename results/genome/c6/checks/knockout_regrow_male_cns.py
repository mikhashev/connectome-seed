#!/usr/bin/env python3
"""Knock out and regrow, the male CNS arm: block A in each optic lobe of one male (the animal
control of block A).

Implements docs/plans/2026-09-26-knockout-regrow-male-cns-arm-registration.md, revision 1.1
("the arm", section numbers below refer to it unless marked "A"), a delta on block A's
registration docs/plans/2026-09-24-knockout-regrow-registration.md, revision 3.4.1 ("A").
This file is a copy of A's script results/genome/c6/checks/knockout_regrow.py (at 74db080) with
the script changes S1-S28 of section 7.2, and is reviewed as a diff against it (D14 (i)); A's
script and the pinned harness are not edited. Each change is marked "S<n>" where it is made.

What differs from A, in one paragraph: the bank is the male CNS builder's existence bank, one per
optic lobe (L, R), read from the outside files only until the registered run unseals block A; the
grid is the 55 placed types (H.ALL_CELLS restricted to 3,025 cells, D1); the synthetic worlds are
rebuilt on each lobe (D6 (b)) with new seeds 92000-92999 (D7); leg S is decided by the count and
p_S is printed with four decimals and a mark when n_deg >= 1 (S28); a block on which leg P cannot
reach 0.01 reads a U of its own, "not readable" (D8); the row-and-column variant has an attempt
cap (D9); the two lobes are read into one male reading (D3) and a split is classified (D4).

    tools/.venv/Scripts/python.exe results/genome/c6/checks/knockout_regrow_male_cns.py --synthetic-only --lobe L --starts 10 --workers 30 --out <new folder>
    tools/.venv/Scripts/python.exe results/genome/c6/checks/knockout_regrow_male_cns.py --synthetic-only --lobe R --starts 10 --workers 30 --out <new folder>
    tools/.venv/Scripts/python.exe results/genome/c6/checks/knockout_regrow_male_cns.py --arm malecns --starts 10 --workers 30

--synthetic-only --lobe L|R (the pre-run, D15 (i)) never opens, hashes, counts or sizes a sealed
file: it reads the lobe's outside bank, fits N1's degree terms on its knockout view, builds the
45 worlds on it and writes the lobe's reference store to --out. While the lobe's PRERUN_* pins
are placeholders (None) it runs in pre-run mode: it makes a reference and checks none. A full
(comparable) pre-run refuses a dirty tree unless --allow-dirty, which marks it NOT A REFERENCE.

--arm malecns (the registered run) runs both lobes in one invocation (D2). It refuses
--allow-dirty (D10), a dirty tree, and any placeholder (PRERUN_* of either lobe, the amended A's
hash). It opens the sealed files only through open_sealed, only after checks 1, 2, 4, 7, 8 and
10, both lobes' synthetic steps with their stop rows and reproduction gates, and checks 6 and 9
on both lobes have passed (section 7.4). CPU only: the pinned numpy harness (D13 (i)).
"""
import os
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
# S2: this arm's registration and revision; the manifest records its LF sha256 at run time.
REGISTRATION = "docs/plans/2026-09-26-knockout-regrow-male-cns-arm-registration.md"
REGISTRATION_REVISION = "1.1"
# S2 (D11, D12, section 9.3): A's registration, from which quote_row and the A-literals line
# quote section 4's rows. It is pinned by its LF sha256 AFTER the amendment of section 9.3 (made
# in step 4 of D15). PLACEHOLDER: None until that revision registers the amended hash; while it is
# None the registered run refuses (check_registered_constants), and every other mode records the
# hash it reads.
A_REGISTRATION = "docs/plans/2026-09-24-knockout-regrow-registration.md"
A_REGISTRATION_SHA256_LF_AMENDED = None                # PLACEHOLDER (D15 step 4, section 9.3)
# The text under which the flyvis-65 verdict was made (revision 3.4.1, commit 74db080): history,
# recovered with `git show 74db080:docs/plans/2026-09-24-knockout-regrow-registration.md`.
A_REGISTRATION_SHA256_LF_FLYVIS65 = (
    "409184dead0a8f9b971bd4b480043725d4a0d1a3c53c20c35734a944a63facd6")
BUILDER_REGISTRATION = "docs/plans/2026-09-25-male-cns-bank-builder-registration.md"
OUT = HERE / "knockout_regrow_male_cns"                # S19: committed, aggregates only
RULE_PATH = C6 / "rules" / "second_rule_v21" / "fit.py"
# Section 7.4 (5): private and raw outputs live outside the repository. The registered run writes
# them to PRIVATE_ROOT / "malecns_<UTC stamp>_<git head, 12>" (private_run_dir).
PRIVATE_ROOT = ROOT.parent / "connectome-seed-data" / "knockout_regrow"
# S17 (sections 3.3, 7.5; D15): one pinned pre-run reference per lobe, made by the
# --synthetic-only pre-run of that lobe from a committed head. PLACEHOLDERS: the pins are
# registered in the revision of the registration that follows the pre-run, and the reference is
# moved to PRERUN_DIR[lobe] in that reviewed change. While a lobe's PRERUN_SHA256 or
# PRERUN_WORLDS_CSV_SHA256 is None, --arm malecns refuses, and --synthetic-only runs in pre-run
# mode (it makes a reference; it checks none). A's revision-2/3 split of its pre-run
# (PRERUN_REV2_FAMILIES, PRERUN_REV3_FAMILIES) and revision 3.2's rename check (_mech_renamed_32)
# are A's history and are not carried over (S17).
PRERUN_DIR = {"L": PRIVATE_ROOT / "synthetic_malecns_L_prerun",
              "R": PRIVATE_ROOT / "synthetic_malecns_R_prerun"}
PRERUN_SHA256 = {"L": None, "R": None}                 # PLACEHOLDER: {file name: raw sha256}
PRERUN_WORLDS_CSV_SHA256 = {"L": None, "R": None}      # PLACEHOLDER
PRERUN_FILES = ("SYNTHETIC.md", "raw_fits.json.gz", "synthetic_only.json", "synthetic_worlds.csv")
# S18: the other arms' references, which --out must never touch. A's is pinned (A section 7);
# block B's folder is the one B section 3.3 proposes, with no pins yet (B is not implemented), so
# only the path is refused for it.
A_PRERUN_DIR = PRIVATE_ROOT / "synthetic_rev3_prerun"
A_PRERUN_SHA256 = {
    "SYNTHETIC.md": "4526d2239c6bf378b161b7fb92bab2c022b0ac648a88fcda8fa02f86f9e58264",
    "raw_fits.json.gz": "91035af838446b86bda502fe8bf719910550bbad72c1cb12563800a984819e60",
    "rev2_full.log": "fa5606e37ebcb8e7b4aac69ba592638e3f77cfea9cbff58b639be2ee8ea960d0",
    "synthetic_only.json": "ea812dfd87238a4a23ca54e06faf5c1d93c7802a36ee28eff9857183236377dd",
    "synthetic_worlds.csv": "7a2f02953207f8aacb1cbd8c5e61e7731135d5a6f800a40b359cb0ff12f9c8f1"}
B_PRERUN_DIR = PRIVATE_ROOT / "synthetic_blockB_prerun"
B_PRERUN_SHA256 = None                                 # B's pins do not exist yet

# Section 1.1 (A section 1.1): A's eight pins (LF-normalised sha256), unchanged. The script
# refuses if any differs.
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
# S3, section 1.1: the male banks (sha256 over raw bytes). The build folder lies outside the
# repository (builder D11 (i)). bank.meta.json is pinned in both copies, the private one in the
# build folder and the committed one; they are byte-equal.
MALE_BUILD_DIR = (ROOT.parent / "connectome-seed-data" / "Janelia" / "derived"
                  / "male_cns_v1_20260926T084555Z_e0a3cd744c39")
MALE_PINS = {
    "male_cns_L_outside.csv": "16c5752a241b2e61d4caeaa23bc4b9b9385011c2bfa6a2db504195199bfe9fb0",
    "male_cns_R_outside.csv": "27a9079b656d1aeb1943702e173d2fa3009f7d8257a78f9e8b5c0f3712b4cf36",
    "pair_stats_outside.csv": "dd71e686c50c127fa9b3bf9f05f957adbd1340d579c839361d16c6c0f0db421f",
    "bank.meta.json": "5ff4af9df5b6ca8e6bfb8282bb27a3b00697a4123b1885118a6d11057ab32d8b"}
BANK_META_COMMITTED = "results/genome/c6/checks/male_cns_bank/bank.meta.json"
# S3, S21: the sealed files are kept apart. Their hashes are checked only inside open_sealed,
# which only the registered real arm calls, after every gate that does not need them (section
# 7.4). No other mode opens, hashes, counts or sizes them. SEALED_DIR is the build folder; the
# tests point it at fixture files and never at the build folder.
SEALED_DIR = MALE_BUILD_DIR
SEALED_NAME = {"L": "male_cns_L_blockA.sealed.csv", "R": "male_cns_R_blockA.sealed.csv"}
SEALED_SHA256 = {"L": "eb611f6805484c4f54c22f072a2ca74219a97b3265c6bfb8a4639e45108e8b8e",
                 "R": "c53a44670b784f7af1c8c3973ba440961b24bff08b039a0cf4c73bd32414da84"}
# S26: the seal record of this revision (section 11). If a registered amendment records a break
# of the seal before review, set it to "broken before review": every verdict line then ends with
# the builder's note (builder section 9).
SEAL_RECORD = "intact"
SEAL_BROKEN_NOTE = ("block A of the male CNS was read before its registration was reviewed "
                    "(builder section 9)")
PYTHON_VERSION, NUMPY_VERSION = "3.10.20", "2.2.6"      # section 7.1 (A section 7)
LOBES = ("L", "R")


def sha256_lf(p):
    return hashlib.sha256(Path(p).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def sha256_raw(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


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

# S3, S5 (sections 1.1, 1.3; D1 (i)): the builder's manifest, read from its committed copy (pinned
# in check 1: MALE_PINS["bank.meta.json"]); c* and the placed list come from it.
# LF-normalised: a git checkout on Windows writes the committed copy with CRLF; the private
# copy has no CR, so its raw sha256 equals the LF sha256 of the committed copy.
_BANK_META_BYTES = (ROOT / BANK_META_COMMITTED).read_bytes().replace(b"\r\n", b"\n")
BANK_META_SHA256_READ = hashlib.sha256(_BANK_META_BYTES).hexdigest()
BANK_META = json.loads(_BANK_META_BYTES.decode("utf-8"))
C_STAR = float(BANK_META["c_star"])
C_STAR_REGISTERED = 2.994356659142212                  # section 0 (bank.meta.json "c_star")
C_STAR_TEXT = "2.99436"                                # the lobe prefix of section 4.1 (1)
PLACED_NAMES = tuple(BANK_META["type_map"]["placed"])
NOT_PLACED_REGISTERED = {"Mi3", "Mi11", "Mi12", "Tm28", "R2", "R3", "R4", "R5", "R6",
                         "CT1(Lo1)"}                   # section 1.3, BUILD.md line 15
N_PLACED, N_PLACED_CELLS = 55, 55 * 55                 # 3,025 placed cells (D1)
PLACED_IDX = sorted(H.IDX[n] for n in PLACED_NAMES)
PLACED = np.zeros(65, bool)
PLACED[PLACED_IDX] = True
PLACED_GRID = np.outer(PLACED, PLACED)                 # the 3,025 placed cells, 65 x 65


def restrict_to_placed_grid():
    """S5 (D1 (i)): H.ALL_CELLS becomes the 3,025 placed cells, in the harness's own row-major
    order, as the FlyWire arm did (restrict_to_30_grid, flywire_bf_p3.py:73-75 at c55d3e3).
    H.FOLD, H.TYPE_FIELDS, H.PAIR_ID, H.NAMES and H.IDX are untouched (section 1.3's table).
    Called in main after check 8, and in _w_init for every worker (Windows spawns workers);
    idempotent."""
    H.ALL_CELLS = np.array([(s, t) for s in PLACED_IDX for t in PLACED_IDX], dtype=np.int64)


# Section 1.3 (S7): what is removed, per lobe; the counts as registered.
N_TRAIN_CELLS = 3025 - 64                              # 2,961 training cells per lobe
N_TRAIN_PRESENT = {"L": 496, "R": 526}
# Section 1.3's table: the 2,961 training cells per outer fold (65-grid: 414-419).
FOLD_TRAIN_CELLS_EXPECTED = (292, 301, 286, 293, 290, 300, 274, 304, 307, 314)

# S8, section 1.4: the pre-data tables as registered, per lobe. Sources: (training targets,
# training sources); targets: (training sources, training targets). Present cells outside the
# block, self-loops in.
ENDPOINTS_EXPECTED = {
    "L": {"Mi1": (22, 11), "Tm3": (19, 10), "Mi4": (17, 11), "Mi9": (18, 13),
          "Tm1": (17, 9), "Tm2": (17, 7), "Tm4": (16, 11), "Tm9": (5, 5),
          "T4a": (5, 9), "T4b": (5, 8), "T4c": (5, 9), "T4d": (5, 8),
          "T5a": (4, 7), "T5b": (4, 8), "T5c": (4, 8), "T5d": (4, 9)},
    "R": {"Mi1": (23, 11), "Tm3": (21, 10), "Mi4": (17, 11), "Mi9": (20, 14),
          "Tm1": (17, 9), "Tm2": (18, 7), "Tm4": (16, 12), "Tm9": (5, 8),
          "T4a": (6, 10), "T4b": (5, 8), "T4c": (5, 9), "T4d": (5, 8),
          "T5a": (4, 9), "T5b": (4, 8), "T5c": (4, 8), "T5d": (4, 9)}}
INFERABLE_MIN = 2                                      # Johnny's rule: >= 2 on both endpoints
INFERABLE_EXPECTED = 64
MIRRORS_EXPECTED = {("T4a", "Mi9"), ("T4b", "Mi9"), ("T4c", "Mi9")}   # (target, source), both lobes
# S8: R1's and CT1(M10)'s row and column at c* (present cells as a source, as a target), per
# lobe (section 0; BUILD.md lines 184-185); R1's cells are the same in both lobes (section 1.4).
POPULATION_ROWS_EXPECTED = {"R1": {"L": (3, 1), "R": (3, 1)},
                            "CT1(M10)": {"L": (9, 31), "R": (9, 30)}}
# S8: the lobe agreement outside the block (section 1.4), from pair_stats_outside.csv.
LOBE_AGREEMENT_EXPECTED = {"both": 493, "L_only": 3, "R_only": 33}
LOBE_L_ONLY_EXPECTED = {("Tm5a", "CT1(M10)"), ("Tm5c", "Am"), ("TmY5a", "CT1(M10)")}
LOBE_R_ONLY_EXPECTED = {
    ("C2", "Mi2"), ("C3", "Tm16"), ("C3", "Tm9"), ("L3", "TmY18"), ("L4", "L3"), ("L4", "Mi14"),
    ("L4", "Tm9"), ("L5", "Tm20"), ("Lawf1", "L3"), ("Mi1", "Mi14"), ("Mi10", "T4a"),
    ("Mi13", "Mi9"), ("Mi13", "Tm9"), ("Mi15", "Mi14"), ("Mi9", "T2"), ("Mi9", "T2a"),
    ("T4a", "Mi13"), ("T5a", "TmY15"), ("T5a", "TmY18"), ("Tm16", "TmY15"), ("Tm2", "T2a"),
    ("Tm20", "T2a"), ("Tm20", "TmY3"), ("Tm3", "Mi10"), ("Tm3", "Tm4"), ("Tm30", "Tm5b"),
    ("Tm5Y", "CT1(M10)"), ("Tm5Y", "Mi10"), ("Tm5a", "Tm30"), ("TmY13", "T2"), ("TmY14", "C3"),
    ("TmY9", "Lawf2"), ("TmY9", "Mi13")}
LOBE_DIFFER_NEAR_CUT_EXPECTED = 33                     # of the 36, both x in [0.5 c*, 2 c*]
# Section 1.4, "Folds": present outside cells per outer fold 0-9.
FOLD_PRESENT_EXPECTED = {"L": (51, 46, 47, 43, 47, 51, 56, 52, 47, 56),
                         "R": (53, 48, 48, 47, 49, 55, 57, 55, 50, 64)}
BAND = (0.5, 2.0)                                      # [0.5 c*, 2 c*], sections 1.4 and 4.3
INFERABILITY_PROVENANCE = (                            # printed as registered; not recomputed
    ("FlyWire-30", "14 / 64", "provenance only (Johnny, review of 2026-09-24)"),
    ("male CNS v1.0, A's row", "64 / 64 at every pair threshold tried (Zcode, preliminary graph)",
     "A section 1.4; a different object from this arm's row (clarification C1, section 11)"),
    ("male CNS v1.0, this arm", "64 / 64 at c* in each lobe",
     "recomputed from the outside files at run start (check 4, section 1.4)"))
MIRROR_IDX = sorted(BLOCK_NAMES.index((s, t)) for (t, s) in MIRRORS_EXPECTED)
N_OTHER_CELLS = N_BLOCK - len(MIRRORS_EXPECTED)        # S15: "the other 61 cells"

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
# S24: 1e-9, the harness's tie band (A revision 3.2, section 3.2), inert (section 3.2): with
# n_p present of 64 (n_p n_a <= 1,024), every AUC is a multiple of 1/(2 n_p n_a), so two unequal
# values on these lattices differ by at least 1/(4 * 1,024^2), about 2.4e-7, far more than TAU,
# and x >= y - TAU holds exactly when x >= y. In n_ge a shuffle's margin is scored on the
# shuffled block, whose present count need not be the real block's; the same lattice argument
# holds for it. TAU can only turn a rounding difference between equal fractions into a tie. The
# tie band that matters is the lambda tie in fitting.
TAU = H.TAU
FIXED_LAMBDA = 1.0                                     # section 3.5: the fixed-lambda diagnostic
LAMBDA_TIE_TEXT = "1e-9"                               # harness.py:727-728 (fit_bf), literal
# S24, section 3.5: the within-animal note replaces A's WITHIN_FLY_NOTE (about FlyWire).
WITHIN_ANIMAL_NOTE = ("within the animal, outside block A: the two lobes differ on 36 of 2,961 "
                      "outside cells at c* (1.22 %; about 0.8 of 64 cells if spread evenly); 33 "
                      "of the 36 are within a factor 2 of the cut")

# Section 3.2: the legs.
N_SHUFFLES = H.N_SHUFFLES                              # 99, harness.shuffled_bank(base, sd)
N_PERM = 9999
RC_SWAPS = 20 * 32                                     # successful checkerboard swaps per draw
RC_CAP_FACTOR = 100                                    # S13 (D9): at most 100 x 640 attempts
N_PERM_CEILINGS = 20                                   # section 2.4, D9

# S12, section 3.7 (D7 (ii)): seeds, all new, in 92000-92999, shared by both lobes; asserted
# distinct and disjoint from A's, B's and the reused ones in assert_seeds_unique.
SEED_PERM = 92000                                      # leg P uniform
SEED_RC = 92001                                        # leg P row-and-column
SEED_PERM_CEIL = 92010                                 # + j, j = 0..19
SEED_WORLD = 92100                                     # + 10 i + j (92100-92184)
SEED_RANGE = (92000, 92999)
# Section 3.7, "Untouched": A's own seeds and B's, beside A's reserved and reused list.
A_SEEDS = ({90000, 90001} | set(range(90010, 90030)) | set(range(90100, 90155))
           | set(range(90160, 90185)))
B_SEEDS = {91000, 91001} | set(range(91010, 91030)) | set(range(91100, 91185))

# Section 3.6: the synthetic worlds, A's nine families unchanged, in A's order (the seed index
# i is the position in this tuple: R, Nf, No, W, M0.5, M1.0, M0.6, M0.75, M0.85 = 0..8).
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
# S16, sections 3.2 and 4.1 (2) (D8): a block on which no AUC on the grid k / (n_p n_a) gives
# p_P <= 0.01 (smallest_passing_auc is None) reads its own U. It takes precedence over every
# other branch, is never renamed by the U rule and is not a threshold U. Its reason is its text.
NOT_READABLE_REASON = ("not readable: leg P cannot reach p_P <= 0.01 on this block (n_present = "
                       "{k} of 64)")
NOT_READABLE_PREFIX = "not readable: leg P cannot reach p_P <= 0.01 on this block"
# S9, check 3 (D8): a block with 0 or 64 present cells has no AUC; that lobe stops, with no label.
NO_AUC_TEXT = "BLOCK HAS NO AUC"
# Section 4.1 (4): "failed fit" keeps its text; on a male block it is read as below.
FAILED_FIT_READING = ("on a male block read as: a failed fit or a rank limit, not separated "
                      "(the block is not known to be rank 1; section 4.1, difference 4)")
# S28 (revision 1.1): the count decides leg S; p_S is printed as information, with four decimals
# and this mark when n_deg >= 1. A's N_DEG_SENTENCE printed the smallest p_S with three
# decimals; it prints four here (S28).
P_S_MARK = "[leg S decided by the count: n_ge = {n_ge} of {n_valid}]"
N_DEG_SENTENCE = ("{n} of {N} shuffles have no AUC on the block and are excluded from leg S, "
                  "which counts against {k} = {N} - {n} shuffles (smallest p_S {ps:.4f})")
# D10: the male arm never runs dirty. A's NOT_REGISTERED_TEXT (a dirty real-arm run) has no use
# here: --allow-dirty is refused with --arm malecns.
ALLOW_DIRTY_REFUSED = ("REFUSED: --allow-dirty is refused with --arm malecns (D10, section 7.4): "
                       "any run of the real arm opens the sealed files, which builder section 9 "
                       "allows in the registered run only; the registered run is made once, at a "
                       "committed head, with the tree clean")
NOT_A_REFERENCE_TEXT = ("NOT A REFERENCE: a full --synthetic-only run made with --allow-dirty "
                        "from an uncommitted tree; a lobe's reference is made from a committed "
                        "head (D15 (i))")

# Section 3.4, check 8: the harness identity, as in bf1_p3.
BF1_FULL_BANK_MARGIN = 0.028150051052145946
IDENTITY_TOL = 1e-9
PARITY_TOL = 1e-9                                      # section 3.4, check 5
# Revision 3.2 (A1): the tolerance of the reproduction gate on the continuous columns of
# synthetic_worlds.csv, in each column's own units. The name is reused from
# results/genome/c6/checks/bf1_p3.py (MACHINE_CHECK_TOL = 1e-9); TAU is not reused for it.
MACHINE_CHECK_TOL = 1e-9


class _Tee:
    """Section 7.4 (6): the stdout (and stderr) of the registered run is also written to the
    private folder. Everything printed before the folder exists is buffered and written first."""

    def __init__(self, stream, fh):
        self.stream, self.fh = stream, fh

    def write(self, s):
        self.stream.write(s)
        self.fh.write(s)
        return len(s)

    def flush(self):
        self.stream.flush()
        self.fh.flush()


_LOG_BUFFER = []


def log(m=""):
    print(m, flush=True)
    if not isinstance(sys.stdout, _Tee):
        _LOG_BUFFER.append(str(m))


def tee_to(path):
    """Section 7.4 (6): from here on stdout and stderr are also written to path; the lines
    logged before are written first."""
    fh = open(path, "a", encoding="utf-8", newline="\n")
    fh.write("\n".join(_LOG_BUFFER) + ("\n" if _LOG_BUFFER else ""))
    fh.flush()
    sys.stdout, sys.stderr = _Tee(sys.stdout, fh), _Tee(sys.stderr, fh)
    return fh


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
# Section 7.4 step 1: refusals; section 1.1: pins; section 3.4 check 1.

def refuse_if_dirty():
    """Sections 3.3 and 7.4 (D10): the real arm runs once, at a committed head, with the tree
    clean under results/genome/c6/ and docs/plans/ (A's scope, the refusal of harness.rule_run);
    unlike A, there is no --allow-dirty (it is refused in main before this)."""
    d = git("status", "--porcelain", "--", "results/genome/c6", "docs/plans")
    if d:
        sys.exit("REFUSED: uncommitted changes under results/genome/c6/ or docs/plans/; the male "
                 f"arm runs only from a committed head with the tree clean ({REGISTRATION} and "
                 "this script first; D10, section 7.4).\n" + d)
    return d


def placeholders_unset():
    """S2, S17 (D15): the constants that the revision after the pre-run registers. A name is
    listed while its value is None."""
    out = []
    if A_REGISTRATION_SHA256_LF_AMENDED is None:
        out.append("A_REGISTRATION_SHA256_LF_AMENDED (A's LF sha256 after the amendment of "
                   "section 9.3)")
    for lobe in LOBES:
        if PRERUN_SHA256[lobe] is None:
            out.append(f"PRERUN_SHA256['{lobe}']")
        if PRERUN_WORLDS_CSV_SHA256[lobe] is None:
            out.append(f"PRERUN_WORLDS_CSV_SHA256['{lobe}']")
    return out


def check_registered_constants():
    """S17, S20 (D15 (i)): the registered run refuses until the revision after the pre-run has
    set every placeholder (both lobes' references and A's amended hash)."""
    missing = placeholders_unset()
    if missing:
        sys.exit("REFUSED: --arm malecns needs the values that the revision after the pre-run "
                 "registers (D15 (i), sections 3.3, 9.3); still placeholders: "
                 + ", ".join(missing))
    return {"placeholders_unset": [], "passed": True}


def check_pins(real_arm=False):
    """Check 1 (sections 1.1, 3.4): A's eight pins (LF sha256), the four male files that every
    mode reads (raw sha256: both outside banks, pair_stats_outside.csv, bank.meta.json in both
    copies), c* and the placed list of bank.meta.json, Python 3.10.20 and numpy 2.2.6, and rule
    #2.1 through harness.load_rule with RANK == 1. The sealed files are not touched here: their
    hashes are checked in open_sealed only (S3, S21). In the real arm, A's registration must
    carry its amended LF sha256 (S2); in every other mode its hash is recorded."""
    bad = {f: (PINS_READ[f], PINS[f]) for f in PINS if PINS_READ[f] != PINS[f]}
    now = {f: sha256_lf(ROOT / f) for f in PINS}
    bad.update({f: (now[f], PINS[f]) for f in PINS if now[f] != PINS[f]})
    male = {n: sha256_raw(MALE_BUILD_DIR / n) for n in MALE_PINS}
    male["bank.meta.json (committed copy)"] = sha256_lf(ROOT / BANK_META_COMMITTED)
    male["bank.meta.json (committed copy, read at import)"] = BANK_META_SHA256_READ
    for n, h in male.items():
        want = MALE_PINS[n.split(" ")[0]]
        if h != want:
            bad[n] = (h, want)
    if bad:
        sys.exit("REFUSED: pins differ (section 1.1): " + json.dumps(bad, indent=1))
    not_placed = set(H.NAMES) - set(PLACED_NAMES)
    if (C_STAR != C_STAR_REGISTERED or len(PLACED_NAMES) != N_PLACED
            or len(set(PLACED_NAMES)) != N_PLACED or not_placed != NOT_PLACED_REGISTERED):
        sys.exit(f"REFUSED: bank.meta.json gives c* = {C_STAR!r} and {len(PLACED_NAMES)} placed "
                 f"types (not placed: {sorted(not_placed)}); registered {C_STAR_REGISTERED!r}, "
                 f"55, {sorted(NOT_PLACED_REGISTERED)} (sections 0, 1.3)")
    py, npv = platform.python_version(), np.__version__
    if (py, npv) != (PYTHON_VERSION, NUMPY_VERSION):
        sys.exit(f"REFUSED: Python {py}, numpy {npv}; section 7.1 requires {PYTHON_VERSION}, "
                 f"{NUMPY_VERSION}")
    rule = H.load_rule(RULE_PATH)
    if rule.rank != 1:
        sys.exit(f"REFUSED: rule #2.1 loads with RANK = {rule.rank}, registered 1 (section 3.4)")
    a_now = sha256_lf(ROOT / A_REGISTRATION)
    if real_arm and a_now != A_REGISTRATION_SHA256_LF_AMENDED:
        sys.exit(f"REFUSED: {A_REGISTRATION} has LF sha256 {a_now}; the registered run quotes "
                 f"section 4 from the amended A, pinned {A_REGISTRATION_SHA256_LF_AMENDED} (S2)")
    return {"pins": now, "male_pins": male, "python": py, "numpy": npv, "rule_name": rule.name,
            "rule_rank": rule.rank, "c_star": C_STAR, "placed_types": len(PLACED_NAMES),
            "a_registration_sha256_lf": a_now,
            "a_registration_pinned_amended": A_REGISTRATION_SHA256_LF_AMENDED,
            "a_registration_flyvis65_text": A_REGISTRATION_SHA256_LF_FLYVIS65,
            "builder_registration_sha256_lf": sha256_lf(ROOT / BUILDER_REGISTRATION),
            "passed": True}


# ------------------------------------------------------------------------------------------
# Section 3.4 checks 2, 3, 4, 5, 7, 10: the block, its print, the pre-data tables, N1 parity,
# AUC, the grid.

def check_block_and_mask():
    """Check 2 (S7): 64 cells, 8 distinct sources and 8 distinct targets, all 16 names in the
    placed set; on the placed grid the knockout view has 2,961 cells and none is a block cell,
    the full view 3,025, the block view 64; the 2,961 split by outer fold as section 1.3 says.
    Needs restrict_to_placed_grid() first."""
    ko, blk = MASKS["ko"], MASKS["block"]
    geo = H.Bank("geometry", {})
    views = {k: H.make_view(geo, MASKS[k]).cells for k in ("ko", "full", "block")}
    per_fold = tuple(int((H.FOLD[views["ko"][:, 0], views["ko"][:, 1]] == f).sum())
                     for f in range(H.N_FOLDS))
    ok = (len(set(map(tuple, BLOCK_CELLS.tolist()))) == N_BLOCK
          and len(set(BLOCK_CELLS[:, 0].tolist())) == 8 and len(set(BLOCK_CELLS[:, 1].tolist())) == 8
          and not set(SOURCES) & set(TARGETS)
          and all(n in PLACED_NAMES for n in SOURCES + TARGETS)
          and not (ko & BLOCK).any() and int(blk.sum()) == N_BLOCK and np.array_equal(blk, BLOCK)
          and len(views["ko"]) == N_TRAIN_CELLS and len(views["full"]) == N_PLACED_CELLS
          and len(views["block"]) == N_BLOCK
          and not BLOCK[views["ko"][:, 0], views["ko"][:, 1]].any()
          and per_fold == FOLD_TRAIN_CELLS_EXPECTED)
    if not ok:
        sys.exit(f"BLOCK OR MASK DIFFERS (section 3.4, check 2): views "
                 f"{ {k: len(v) for k, v in views.items()} }, per fold {per_fold}")
    return {"cells": N_BLOCK, "sources": 8, "targets": 8,
            "views": {k: len(v) for k, v in views.items()}, "training_cells_per_fold": per_fold,
            "passed": True}


def check_grid(banks=()):
    """Check 10 (new): len(H.ALL_CELLS) == 3,025 and every cell placed, in this process (after
    the restriction); each bank given has no present cell outside the placed set. _w_group
    asserts the grid in every fit in every worker."""
    ok_grid = (len(H.ALL_CELLS) == N_PLACED_CELLS
               and bool(PLACED_GRID[H.ALL_CELLS[:, 0], H.ALL_CELLS[:, 1]].all()))
    off = {b.name: int((b.exists & ~PLACED_GRID).sum()) for b in banks}
    if not ok_grid or any(off.values()):
        sys.exit(f"GRID DIFFERS (section 3.4, check 10): len(H.ALL_CELLS) = {len(H.ALL_CELLS)}, "
                 f"cells off the placed grid by bank {off}")
    return {"all_cells": len(H.ALL_CELLS), "banks_off_grid": off, "passed": True}


OUTSIDE_HEADER = ["src", "tar", "du", "dv", "n_syn", "sign"]


def parse_male_outside(text, name):
    """S4: one existence row per present outside cell (builder section 7): src, tar, du = dv = 0,
    n_syn = x, sign = +1. Refused, as load_flywire_bank does (flywire_bf_p3.py:85-98): a name
    outside the 55 placed types, a block-A cell ("BLOCK ROW IN OUTSIDE FILE"), an offset other
    than (0, 0), a sign other than +1, a duplicated cell, a malformed row or header."""
    rows = list(csv.reader(io.StringIO(text, newline="")))
    if not rows or rows[0] != OUTSIDE_HEADER:
        sys.exit(f"REFUSED: {name}: header {rows[0] if rows else None}, expected "
                 f"{OUTSIDE_HEADER} (S4)")
    placed, block = set(PLACED_NAMES), set(BLOCK_NAMES)
    content = {}
    for i, r in enumerate(rows[1:], start=2):
        if not r:
            continue
        if len(r) != len(OUTSIDE_HEADER):
            sys.exit(f"REFUSED: {name} line {i}: {len(r)} fields (S4)")
        s, t, du, dv, n, sg = r
        if s not in placed or t not in placed:
            sys.exit(f"REFUSED: {name} line {i}: {s} -> {t} names a type outside the 55 placed "
                     "types (S4)")
        if (s, t) in block:
            sys.exit(f"BLOCK ROW IN OUTSIDE FILE: {name} line {i}: {s} -> {t} (S4)")
        if (int(du), int(dv)) != (0, 0):
            sys.exit(f"REFUSED: {name} line {i}: offset ({du}, {dv}), an existence bank has "
                     "(0, 0) only (S4)")
        if int(sg) != 1:
            sys.exit(f"REFUSED: {name} line {i}: sign {sg}, an existence bank has +1 only (S4)")
        k = (H.IDX[s], H.IDX[t])
        if k in content:
            sys.exit(f"REFUSED: {name} line {i}: {s} -> {t} twice (S4)")
        content[k] = {"offsets": {(0, 0): float(n)}, "hull": [], "sign": 1}
    return content


def load_male_bank(lobe, path=None):
    """S4: the lobe's outside bank, read from male_cns_<lobe>_outside.csv after its raw sha256
    has been checked against MALE_PINS (a fixture path, given by a test, is not pinned). The
    "hull" key is written empty: the harness's canon_content reads it in every shuffle."""
    name = f"male_cns_{lobe}_outside.csv"
    p = Path(path) if path is not None else MALE_BUILD_DIR / name
    raw = p.read_bytes()
    if path is None and hashlib.sha256(raw).hexdigest() != MALE_PINS[name]:
        sys.exit(f"REFUSED: {name} differs from its pin (section 1.1)")
    return H.Bank(f"malecns_{lobe}", parse_male_outside(raw.decode("utf-8"), name))


def block_pattern(y):
    """S9, check 3 (D8): the print of the block after unsealing. The present count, the four
    quadrant counts, the row and column counts, whether y_st = x_s * w_t (flyvis's board) and
    whether the block is balanced (4 of 8 in every row and column); has_auc is False with 0 or
    64 present cells."""
    y = np.asarray(y, bool)
    Y = y.reshape(8, 8)
    rows = {s: int(Y[i].sum()) for i, s in enumerate(SOURCES)}
    cols = {t: int(Y[:, j].sum()) for j, t in enumerate(TARGETS)}
    n = int(y.sum())
    return {"present": n, "absent": N_BLOCK - n,
            "quadrants": {k: int(y[v].sum()) for k, v in QUADRANTS.items()},
            "row_counts": rows, "column_counts": cols,
            "y_equals_x_times_w": bool(np.array_equal(y, BOARD)),
            "balanced": all(v == 4 for v in rows.values()) and all(v == 4 for v in cols.values()),
            "has_auc": 0 < n < N_BLOCK}


def check_block_print(y, lobe):
    """S9, check 3 (after unsealing): no reviewed count exists (A section 8, section 1.5), so the
    block is printed, not compared. It stops that lobe only if the block has no AUC (0 or 64
    present: "BLOCK HAS NO AUC"): that lobe then has no label; the other lobe goes on (D8)."""
    d = block_pattern(y)
    log(f"check 3 (block print, lobe {lobe}): present {d['present']}/64; quadrants "
        f"{d['quadrants']}; rows {d['row_counts']}; columns {d['column_counts']}; y = x * w "
        f"(flyvis's board): {d['y_equals_x_times_w']}; balanced: {d['balanced']}")
    if not d["has_auc"]:
        log(f"{NO_AUC_TEXT} (lobe {lobe}: {d['present']} of 64 present): this lobe stops and has "
            "no label (check 3, D8)")
    return {**d, "stops_lobe": not d["has_auc"], "passed": d["has_auc"]}


def pre_data_tables(bank):
    """Section 1.4, from presence outside the block only (the lobe's outside bank): what each
    endpoint keeps, Johnny's inferability, the mirror cells, the training present count
    (section 1.3), R1's and CT1(M10)'s row and column (S8), and the present cells per fold."""
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
    pop = {n: (int(ex[H.IDX[n], :].sum()), int(ex[:, H.IDX[n]].sum()))
           for n in POPULATION_ROWS_EXPECTED}
    r1 = H.IDX["R1"]
    r1_cells = sorted([("R1", H.NAMES[t]) for t in np.flatnonzero(ex[r1, :])]
                      + [(H.NAMES[s], "R1") for s in np.flatnonzero(ex[:, r1])])
    return {"endpoints": keep, "inferable": len(inf), "mirrors": sorted(mirrors),
            "training_present": int(ex.sum()), "population_rows": pop, "R1_cells": r1_cells,
            "present_per_fold": tuple(int((ex & (H.FOLD == f)).sum()) for f in range(H.N_FOLDS))}


def lobe_agreement(banks):
    """S8, section 1.4: the lobe agreement outside the block, from pair_stats_outside.csv (after
    its pin in check 1): each lobe's 2,961 outside cells, none a block cell; each outside bank
    equals the present = 1 rows of its lobe, with n_syn = x; the cells present in both lobes, in
    L only and in R only; how many of the differing cells have x in [0.5 c*, 2 c*] in both
    lobes."""
    p = MALE_BUILD_DIR / "pair_stats_outside.csv"
    raw = p.read_bytes()
    if hashlib.sha256(raw).hexdigest() != MALE_PINS["pair_stats_outside.csv"]:
        sys.exit("REFUSED: pair_stats_outside.csv differs from its pin (section 1.1)")
    rows = {lobe: {} for lobe in LOBES}
    for r in csv.DictReader(io.StringIO(raw.decode("utf-8"), newline="")):
        rows[r["lobe"]][(r["src"], r["tar"])] = (float(r["x"]), int(r["present"]))
    problems = []
    for lobe in LOBES:
        if len(rows[lobe]) != N_TRAIN_CELLS or set(rows[lobe]) & set(BLOCK_NAMES):
            problems.append(f"lobe {lobe}: {len(rows[lobe])} rows, block rows "
                            f"{sorted(set(rows[lobe]) & set(BLOCK_NAMES))}")
        pres = {k: x for k, (x, pr) in rows[lobe].items() if pr == 1}
        bank = {(H.NAMES[s], H.NAMES[t]): c["offsets"][(0, 0)]
                for (s, t), c in banks[lobe].content.items()}
        if pres != bank:
            problems.append(f"lobe {lobe}: the outside bank differs from the present = 1 rows of "
                            "pair_stats_outside.csv")
    if set(rows["L"]) != set(rows["R"]):
        problems.append("the two lobes' outside cells differ")
    pl = {k for k, (_, pr) in rows["L"].items() if pr == 1}
    pr_ = {k for k, (_, pr) in rows["R"].items() if pr == 1}
    lo, hi = BAND[0] * C_STAR, BAND[1] * C_STAR
    differ = (pl - pr_) | (pr_ - pl)
    near = sum(1 for k in differ if all(lo <= rows[lobe][k][0] <= hi for lobe in LOBES))
    return {"both": len(pl & pr_), "L_only": len(pl - pr_), "R_only": len(pr_ - pl),
            "L_only_cells": sorted(pl - pr_), "R_only_cells": sorted(pr_ - pl),
            "differ_near_cut_both_lobes": near, "problems": problems}


def check_pre_data_tables(tables, agreement):
    """Check 4 (S8): section 1.4's tables per lobe (endpoints, 64 / 64 inferable, the three
    mirrors, the training present count 496 / 526, R1's and CT1(M10)'s row and column, R1's
    cells equal in both lobes, the present cells per fold) and the lobe agreement (493 / 3 / 33,
    the 36 cells by name, 33 of them near the cut). From the outside files only; else
    "PRE-DATA TABLES DIFFER"."""
    bad = []
    for lobe in LOBES:
        t = tables[lobe]
        for key, got, want in (
                ("endpoints", t["endpoints"], ENDPOINTS_EXPECTED[lobe]),
                ("inferable", t["inferable"], INFERABLE_EXPECTED),
                ("mirrors", set(map(tuple, t["mirrors"])), MIRRORS_EXPECTED),
                ("training_present", t["training_present"], N_TRAIN_PRESENT[lobe]),
                ("population_rows", t["population_rows"],
                 {n: v[lobe] for n, v in POPULATION_ROWS_EXPECTED.items()}),
                ("present_per_fold", t["present_per_fold"], FOLD_PRESENT_EXPECTED[lobe])):
            if got != want:
                bad.append(f"lobe {lobe} {key}: {got} (registered {want})")
    if tables["L"]["R1_cells"] != tables["R"]["R1_cells"]:
        bad.append(f"R1's cells differ between the lobes: {tables['L']['R1_cells']} / "
                   f"{tables['R']['R1_cells']}")
    for key, want in LOBE_AGREEMENT_EXPECTED.items():
        if agreement[key] != want:
            bad.append(f"lobe agreement {key}: {agreement[key]} (registered {want})")
    if set(agreement["L_only_cells"]) != LOBE_L_ONLY_EXPECTED:
        bad.append(f"L-only cells {agreement['L_only_cells']}")
    if set(agreement["R_only_cells"]) != LOBE_R_ONLY_EXPECTED:
        bad.append(f"R-only cells {agreement['R_only_cells']}")
    if agreement["differ_near_cut_both_lobes"] != LOBE_DIFFER_NEAR_CUT_EXPECTED:
        bad.append(f"differing cells near the cut: {agreement['differ_near_cut_both_lobes']} "
                   f"(registered {LOBE_DIFFER_NEAR_CUT_EXPECTED})")
    bad += agreement["problems"]
    if bad:
        log("PRE-DATA TABLES DIFFER")
        log(json.dumps(json_safe({"differences": bad, "tables": tables}), indent=1))
        sys.exit(1)
    return {"passed": True, "tables": tables, "lobe_agreement": agreement}


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
    """S10, check 5 (D8): D(N1 logit) on the block, printed with the block's balance (check 3).
    No stop: D is 0 only on a balanced block, and the male block is not known to be balanced
    (section 0). Decides nothing."""
    d = parity_D(n1_block_logit(n1data), y)
    bal = block_pattern(y)["balanced"]
    return {"D_N1_logit": d, "balanced": bal, "tolerance_of_A": PARITY_TOL,
            "within_A_tolerance": d is not None and abs(d) < PARITY_TOL,
            "status": "printed, decides nothing (D8)", "passed": None}


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
    random 32/32 case with ties. S11: one unbalanced 64-cell hand case, 16 present of 64: the
    prediction 63 - i on cell i, present on cells 0-14 and 63, so the 15 top cells outrank all 48
    absent cells and cell 63 none: AUC = 15 * 48 / (16 * 48) = 0.9375."""
    y = np.array([1, 1, 0, 0], bool)
    y64 = np.zeros(64, bool)
    y64[list(range(15)) + [63]] = True
    cases = [([0.9, 0.8, 0.2, 0.1], y, 1.0), ([0.1, 0.2, 0.8, 0.9], y, 0.0),
             ([0.5, 0.5, 0.5, 0.5], y, 0.5),
             ([0.9, 0.5, 0.5, 0.1], np.array([1, 0, 1, 0], bool), 0.875),
             (63.0 - np.arange(64), y64, 0.9375)]
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
    """Leg P: default_rng(92000), 9,999 x permutation(64) in order (S12). The same matrix serves
    both lobes (section 3.7, common random numbers)."""
    if "u" not in _PERM_CACHE:
        rng = np.random.default_rng(SEED_PERM)
        _PERM_CACHE["u"] = np.array([rng.permutation(N_BLOCK) for _ in range(N_PERM)])
    return _PERM_CACHE["u"]


def perm_ceiling_perm(j):
    """Section 2.4, D9: permutation j of the block, default_rng(92010 + j).permutation(64)."""
    return np.random.default_rng(SEED_PERM_CEIL + j).permutation(N_BLOCK)


_RC_CACHE = {}
RC_ONE_PATTERN_TEXT = "n/a: the row-and-column null has one pattern"
RC_CAP_STOP_TEXT = ("ROW-AND-COLUMN NULL: ATTEMPT CAP REACHED (chain {chain}, successes {succ}, "
                    "attempts {att})")
RC_CAP_REAL_TEXT = "n/a (attempt cap reached: chain {chain}, successes {succ}, attempts {att})"


def has_checkerboard(yb):
    """S13 (D9, guard 1): rows i, j and columns k, l with y[i,k] = y[j,l] != y[i,l] = y[j,k]
    exist iff, for some row pair, each row has a present cell where the other is absent."""
    yb = np.asarray(yb, bool)
    for i in range(yb.shape[0]):
        for j in range(i + 1, yb.shape[0]):
            if (yb[i] & ~yb[j]).any() and (~yb[i] & yb[j]).any():
                return True
    return False


def _rc_chains(y, n_chains, swaps):
    """A's chains with the attempt cap added; while no chain is capped, the draws and patterns
    are A's (one rng.integers(8, size=(n, 4)) per step while any chain is live)."""
    yb = np.asarray(y, bool).reshape(8, 8)
    if not has_checkerboard(yb):
        return {"status": "one_pattern", "patterns": None, "text": RC_ONE_PATTERN_TEXT}
    rng = np.random.default_rng(SEED_RC)
    B = np.broadcast_to(yb, (n_chains, 8, 8)).copy()
    succ = np.zeros(n_chains, np.int64)
    att = np.zeros(n_chains, np.int64)
    cap = RC_CAP_FACTOR * swaps
    n = np.arange(n_chains)
    while True:
        live = (succ < swaps) & (att < cap)
        if not live.any():
            break
        a = rng.integers(8, size=(n_chains, 4))
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


def rc_patterns(y, mode, n_chains=N_PERM, swaps=RC_SWAPS):
    """Leg P, row-and-column variant (A D4), with S13's guards (D9): no checkerboard gives
    RC_ONE_PATTERN_TEXT in either mode; each chain makes at most 100 x 640 attempts
    (harness.py:881-883); a cap hit stops a synthetic step (every block there is a 32/32 board)
    and gives "n/a (attempt cap reached: ...)" on a real block, whose run goes on. n_chains and
    swaps are for the tests; the registered calls use the defaults."""
    if mode not in ("synthetic", "real"):
        raise ValueError(mode)
    y = np.asarray(y, bool)
    key = (y.tobytes(), n_chains, swaps)
    if key not in _RC_CACHE:
        _RC_CACHE[key] = _rc_chains(y, n_chains, swaps)
    res = _RC_CACHE[key]
    if res["status"] == "cap":
        fields = {"chain": res["chain"], "succ": res["successes"], "att": res["attempts"]}
        if mode == "synthetic":
            log(RC_CAP_STOP_TEXT.format(**fields) + "; the synthetic step stops (S13, D9)")
            sys.exit(1)
        return {**res, "text": RC_CAP_REAL_TEXT.format(**fields)}
    return res


def _array_sha256(a):
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()


def null_input_digests():
    """Revision 3.3 (F10): digests of the leg-P null inputs (the uniform_perms() matrix; each
    registered-size rc_patterns matrix, keyed by the sha256 of its y bytes, or its status when
    it has no patterns). Computed in the main process, where every null is computed."""
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
    them (A's list), with A's own seeds and B's (S12)."""
    dial = {10000 + 100 * fi + sd for fi in range(len(H.DIAL_F)) for sd in range(H.DIAL_SEEDS)}
    return ({60000, 61000} | set(range(70000, 71000)) | set(range(80000, 81000))
            | {H.PL_SEED, H.PL_SCRAMBLE_SEED, H.PRSH_SEED}
            | {H.RP_SEED_BASE + j for j in H.RP_SEEDS} | dial | {20260923}
            | set(range(N_SHUFFLES)) | {H.PERTURB_SEED_BASE + j for j in range(max(starts, 10))}
            | A_SEEDS | B_SEEDS)


def world_specs():
    return [{"family": fam, "i": i, "j": j, "seed": SEED_WORLD + 10 * i + j, "gamma_z": gz,
             "gamma_z1": gz1, "board": board}
            for i, (fam, gz, gz1, board) in enumerate(FAMILIES) for j in range(WORLDS_PER_FAMILY)]


def assert_seeds_unique(starts):
    """S12, section 3.7 (D7): the new seeds (92000, 92001, 92010-92029, 92100-92184) are
    distinct, lie in 92000-92999, and meet none of the untouched, reused, A or B seeds."""
    worlds = [w["seed"] for w in world_specs()]
    new = [SEED_PERM, SEED_RC] + [SEED_PERM_CEIL + j for j in range(N_PERM_CEILINGS)] + worlds
    ok = (len(new) == len(set(new)) == 2 + N_PERM_CEILINGS + len(FAMILIES) * WORLDS_PER_FAMILY
          and all(SEED_RANGE[0] <= s <= SEED_RANGE[1] for s in new)
          and not set(new) & reserved_seeds(starts))
    if not ok:
        sys.exit("SEEDS NOT UNIQUE: " + str(sorted(new)))
    return {"new_seeds": len(new), "unique": True, "in_92000_92999": True,
            "disjoint_from_reserved_reused_A_and_B": True,
            "world_seeds": [min(worlds), max(worlds)]}


# ------------------------------------------------------------------------------------------
# Section 3.6: the synthetic worlds.

# S14: the other types are the 39 placed types outside the 16 block types (A: 49).
OTHERS = [i for i in range(65) if PLACED[i] and H.NAMES[i] not in set(SOURCES + TARGETS)]
assert len(OTHERS) == 39
BLOCK_TYPES = [H.IDX[n] for n in SOURCES + TARGETS]
Z_BLOCK = np.zeros(65)
ZPRIME = np.zeros(65)
for _n in SOURCES + TARGETS:
    Z_BLOCK[H.IDX[_n]] = 1.0 if _n in Z_PLUS else -1.0
    ZPRIME[H.IDX[_n]] = 1.0 if _n in ZPRIME_PLUS else -1.0
# Section 3.6, No: sum z z' = 0 over the sources and over the targets.
assert sum(Z_BLOCK[H.IDX[s]] * ZPRIME[H.IDX[s]] for s in SOURCES) == 0
assert sum(Z_BLOCK[H.IDX[t]] * ZPRIME[H.IDX[t]] for t in TARGETS) == 0


def board_y(board):
    """The block labels of a world with this board, in block cell order, as make_world sets
    them: present iff z_s z_t > 0 (board "z") or z'_s z'_t > 0 (board "z'")."""
    zb = Z_BLOCK if board == "z" else ZPRIME
    return (np.outer(zb, zb) > 0)[BLOCK_CELLS[:, 0], BLOCK_CELLS[:, 1]]


def content_pool(bank):
    """S14: the lobe's content pool, its present outside cells in sorted cell order (496 or 526
    existence rows; A: flyvis-65's 572 non-block cells)."""
    return [bank.content[k] for k in sorted(k for k in bank.content if not BLOCK[k])]


def degree_terms(bank):
    """S14, section 3.6: N1's existence parameters (c, a, b), fitted on the lobe's knockout view
    on the placed grid (the outside bank only; no sealed file). Needs the restriction."""
    assert len(H.ALL_CELLS) == N_PLACED_CELLS
    n1 = H.fit_n1(H.make_view(bank, MASKS["ko"]))
    return float(n1["ex_c"][0]), np.asarray(n1["ex_a"], float), np.asarray(n1["ex_b"], float)


def make_world(spec, terms, pool):
    """Section 3.6, S14: default_rng(seed) draws, in A's order, z for the 39 placed others
    (ascending harness index; +1 iff a uniform draw < 1/2), z1 for the 39 others (drawn in every
    family, used in W only), u (65 x 65), and the content indices (65 x 65 integers into the
    lobe's pool). Outside cells: present iff u < sigmoid(c + a_s + b_t + gamma_z z_s z_t +
    gamma_z1 z1_s z1_t), and every cell with an unplaced endpoint absent (asserted). Block cells:
    the board by z or z'. The content is the pool's existence rows."""
    rng = np.random.default_rng(spec["seed"])
    z = Z_BLOCK.copy()
    z[OTHERS] = np.where(rng.random(len(OTHERS)) < 0.5, 1.0, -1.0)
    z1 = np.zeros(65)
    z1[BLOCK_TYPES] = ZPRIME[BLOCK_TYPES]
    z1[OTHERS] = np.where(rng.random(len(OTHERS)) < 0.5, 1.0, -1.0)
    u = rng.random((65, 65))
    idx = rng.integers(len(pool), size=(65, 65))
    c, a, b = terms
    logit = (c + a[:, None] + b[None, :] + spec["gamma_z"] * np.outer(z, z)
             + spec["gamma_z1"] * np.outer(z1, z1))
    ex = u < 1.0 / (1.0 + np.exp(-logit))
    ex &= PLACED_GRID
    zb = Z_BLOCK if spec["board"] == "z" else ZPRIME
    ex[BLOCK] = (np.outer(zb, zb) > 0)[BLOCK]
    content = {}
    for s, t in zip(*np.nonzero(ex)):
        src = pool[idx[s, t]]
        content[(int(s), int(t))] = {"offsets": dict(src["offsets"]), "hull": [],
                                     "sign": src["sign"]}
    bank = H.Bank(f"world.{spec['family']}.{spec['seed']}", content)
    assert int(bank.exists[BLOCK].sum()) == 32
    assert not (bank.exists & ~PLACED_GRID).any()
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


FILL_CONTENT = {"offsets": {(0, 0): C_STAR_REGISTERED}, "hull": [], "sign": 1}


def fill_block(bank, y, name):
    """Checks 6 and T4: the bank with its block replaced by the pattern y (64 booleans in block
    cell order), each present cell an existence row at c*. The knockout view does not see it."""
    content = {k: v for k, v in bank.content.items() if not BLOCK[k]}
    for i, (s, t) in enumerate(BLOCK_CELLS.tolist()):
        if y[i]:
            content[(s, t)] = dict(FILL_CONTENT)
    return H.Bank(name, content)


def fill_pattern(spec):
    """The block fillings of checks 6 and T4: "absent" (every block cell absent, the outside
    bank as it is), "z" (the board z) and "rand<seed>" (a random pattern, a test input)."""
    if spec == "absent":
        return np.zeros(N_BLOCK, bool)
    if spec == "z":
        return board_y("z")
    if spec.startswith("rand"):
        return np.random.default_rng(int(spec[4:])).random(N_BLOCK) < 0.5
    raise KeyError(spec)


def real_bank(outside, block_cells, lobe):
    """S21: the lobe's bank in the real run, its outside bank and its present block cells from
    open_sealed (existence rows, n_syn = x)."""
    content = dict(outside.content)
    for (s, t), x in block_cells.items():
        assert BLOCK[s, t]
        content[(s, t)] = {"offsets": {(0, 0): float(x)}, "hull": [], "sign": 1}
    return H.Bank(f"malecns_{lobe}_real", content)


def build_bank(key, ctx):
    """Bank keys: "flyvis65" (check 8 only, on the full grid), "outside" (the lobe's outside
    bank: its block all absent), "real" (the lobe's bank with its unsealed block; refused unless
    the worker was given it), or "world:<family>:<j>"; then optional "|sh:<sd>"
    (harness.shuffled_bank), "|pc:<j>" (permuted-block ceiling) or "|fill:<spec>" (checks 6, T4).
    A "real" key is refused in every synthetic pool, so no synthetic worker can build, fit or
    score a bank that holds the real block (S6)."""
    base, *mods = key.split("|")
    if base == "flyvis65":
        bank = H.REAL
    elif base == "outside":
        bank = ctx["lobe_bank"]
    elif base == "real":
        if ctx["syn"] or ctx.get("real_block") is None:
            raise RuntimeError("REFUSED: this pool never builds a bank on the real block")
        bank = real_bank(ctx["lobe_bank"], ctx["real_block"], ctx["lobe"])
    else:
        _, fam, j = base.split(":")
        bank = make_world(spec_of(fam, int(j)), ctx["terms"], ctx["pool"])
    for m in mods:
        if m.startswith("sh:"):
            bank = H.shuffled_bank(bank, int(m[3:]))[0]
        elif m.startswith("pc:"):
            bank = permute_block(bank, perm_ceiling_perm(int(m[3:])), f"{bank.name}.pc{m[3:]}")
        elif m.startswith("fill:"):
            bank = fill_block(bank, fill_pattern(m[5:]), f"{bank.name}.fill_{m[5:]}")
        else:
            raise KeyError(key)
    return bank


# ------------------------------------------------------------------------------------------
# Section 2: fitting, in a process pool. A task is (bank key, mask kind, predictor key); mask
# kinds: "ko" (the knockout, section 1.3), "full" (ceiling_full), "block" (ceiling_block),
# "ko1" (the knockout at fixed lambda = 1, the diagnostic of section 3.5; rule #2.1 and BF_r
# only), "ko#hash#<n>" (checks 6, 6' and 9: the data dict's hash only), "cv:<f>" (check 8).

_W = {}


def _w_init(starts, terms, synthetic_only, lobe=None, restrict=True, real_block=None):
    """S5, S6: every worker restricts the grid (Windows spawns workers, which re-import this
    module with the full grid), except check 8's pool, which runs on flyvis-65 before any
    restriction and asserts that it sees the full grid. A lobe's pool loads the lobe's outside
    bank (pin-checked) and, only in the real arm after unsealing, is handed the present block
    cells (real_block); no worker opens a sealed file."""
    H.STARTS = starts                                  # the harness global every fit reads
    os.environ.pop("SECOND_RULE_SPREAD_DIR", None)
    if restrict:
        restrict_to_placed_grid()
    else:
        assert len(H.ALL_CELLS) == 65 * 65, "check 8's pool runs before any restriction"
    lobe_bank = load_male_bank(lobe) if lobe else None
    _W.update(starts=starts, terms=terms, syn=synthetic_only, lobe=lobe, restrict=restrict,
              lobe_bank=lobe_bank, pool=content_pool(lobe_bank) if lobe_bank else None,
              real_block=real_block, rule=H.load_rule(RULE_PATH), bf={}, key=None, bank=None)


def _w_grid_size():
    """T2: what a pool worker sees as len(H.ALL_CELLS)."""
    return len(H.ALL_CELLS)


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
    its decode and score on the 64 block cells. S6: outside_density is taken over the 2,961
    placed outside cells (S14)."""
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
        "outside_density": float(bank.exists[~BLOCK & PLACED_GRID].mean()),
        "secs": time.time() - t0}


def _w_group(group):
    """S5, check 10: every fit asserts the grid it runs on: 3,025 placed cells, or the full grid
    for check 8's flyvis-65 folds."""
    key = group[0][0]
    if _W["key"] != key:
        _W["bank"], _W["key"] = build_bank(key, _W), key
    bank = _W["bank"]
    want = 65 * 65 if key == "flyvis65" else N_PLACED_CELLS
    out = []
    for bk, mk, pk in group:
        assert bk == key
        assert len(H.ALL_CELLS) == want, f"grid {len(H.ALL_CELLS)} in a fit on {bk}, want {want}"
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
    broken in block cell order); A's precision at 32 on a 32/32 block. None with no present."""
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
    3.3, B1). None when no AUC on the grid reaches p_P <= 0.01 (for example 1 or 63 present):
    leg P cannot pass on that block, and the lobe reads the "not readable" U (D8). None also
    for a block with no AUC (0 or 64 present), which check 3 stops before."""
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


# Section 3.3: smallest_passing_auc as a checked scalar, registered by board (A revision 3.4,
# item 2), with one address, the lobe's pinned synthetic_only.json (A revision 3.4.1, item B).
# The male values do not exist yet; the revision after the pre-run states them. In the worlds
# both lobes' values must be equal board by board (same leg-P seed, same boards); the registered
# run asserts it. The two lobes' real blocks have their own values, printed, not compared.
SMALLEST_PASSING_AUC_GATES = (
    "it gates one statistic of Yu = y[uniform_perms()] and the composition (the layout y, P_R, "
    "N_PERM), through auc_null on one tie-free prediction; it needs no fit. It does not see Yrc "
    "(rc_patterns), nor a change in the consumer at equal Yu (the p_P lines of evaluate_bank, "
    "avg_ranks on tied predictions, auc); the null-input digests remain for attribution. Under "
    "--from-raw, where y comes from the store and Yu is generated fresh, it is the only check of "
    "the fresh generator that stops the run (the comparison of the re-read table with the pinned "
    "one is for information only)")


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
    with "world", "board" and "y" (the block labels, 64 booleans in block cell order). A board
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


MEANINGLESS_LABEL = "meaningless on an existence bank"      # S25 (D5, section 2)


def evaluate_bank(base_key, F, n_sh, n_pc, rc_mode):
    """Every number of section 3.5 for one bank, and its section 4 label. rc_mode is
    "synthetic" (a world: an rc_patterns cap hit stops) or "real" (a real block: it prints
    n/a and the run goes on; S13, D9)."""
    base = {pk: F[(base_key, "ko", pk)] for pk in PRED_KEYS}
    y = np.asarray(base["N1"]["y"], bool)
    for pk in PRED_KEYS:
        for mk in ("ko", "full", "block"):
            assert np.array_equal(np.asarray(F[(base_key, mk, pk)]["y"], bool), y)
    Yu = y[uniform_perms()]
    rc = rc_patterns(y, rc_mode)
    Yrc = rc["patterns"]
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
            "quadrant_mean_p": {k: float(p[v].mean()) for k, v in QUADRANTS.items()},
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
            "auc_other_61": auc(p[rest], y[rest]),
            "per_type_auc": per_type,
            "present_cells_offset_counts_sign": {
                "label": MEANINGLESS_LABEL,
                "values": {k: sc[k] for k in ("offset", "counts", "sign")}},
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
    return {"bank": base_key, "rows": rows, "per_shuffle": sh, "n_deg": int(n_deg),
            "fixed_lambda": fixed,
            "perm_ceilings_full_rule": perm_ceilings,
            "outside_density": base["N1"]["outside_density"], "block_present": int(y.sum()),
            "row_and_column_null": {k: v for k, v in rc.items() if k != "patterns"},
            "smallest_passing_auc": spa,
            **read_label(rows, n_present=int(y.sum()), readable=spa is not None)}


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


def not_readable_reason(n_present):
    """S16 (D8): the "not readable" reason, which is also its U text."""
    return NOT_READABLE_REASON.format(k=n_present)


def u_kind(reasons):
    """A revision 3.3 (A3, A4); S16: which U a list of U reasons gives. "not_readable" if a
    reason is the not-readable reason (D8; it takes precedence: leg P cannot pass on the block,
    whatever else is listed); else "failed_fit" if a reason is ceiling_block below GATE_CUT; else
    "not_measured" if a reason is CEILING_BLOCK_NOT_MEASURED; else "threshold". Only threshold U
    enters the U rule."""
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
    read. S16 (D8, section 4.1 (2)): a block that is not readable (no AUC on the grid reaches
    p_P <= 0.01; readable False) reads U with the not-readable reason first; it takes precedence
    over every branch and is never renamed. A's reasons are kept after it, for information.
    Leg S is the count (leg_S_passes), never p_S (section 4.1, revision 1.1)."""
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
    S16 (D8): a U whose reasons include the not-readable reason prints that reason as its text
    ("U: not readable: leg P cannot reach p_P <= 0.01 on this block (n_present = k of 64)"),
    never renamed. Not to be confused with LABEL_TEXT, a dict in flywire_column_test.py."""
    if label == "R":
        return "R: regrows"
    if label == "W":
        return "W: rule weaker than the information available"
    if label == "G":
        return (f"G: not detected at the R level above gamma_R (gate: rule #2.1's ceiling_block = "
                f"{fmt(ceiling_block)} >= {GATE_CUT:.2f}; {limits_text(dl)})")
    kind = u_kind(reasons)
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
    """S28 (revision 1.1): p_S as printed. Leg S is decided by the count (leg_S_passes: n_valid
    >= 1 and n_ge == 0); p_S is information. With n_deg >= 1 it is printed with four decimals and
    the mark naming the count; with n_deg = 0, as A (two decimals)."""
    if r["n_deg"] >= 1:
        return (f"{r['p_S']:.4f} "
                + P_S_MARK.format(n_ge=r["n_ge"], n_valid=r["n_valid_shuffles"]))
    return f"{r['p_S']:.2f}"


def lobe_prefix(lobe):
    """Section 4.1 (1): the lobe prefix of every verdict line."""
    return f"male CNS, lobe {lobe} (existence bank at c* = {C_STAR_TEXT}): "


def verdict_line(ev, dl, u_rule, no_contingency=False, lobe=None):
    """Section 4 (A section 4, verbatim in content): the label (G with the three limits and the
    instrument; U by the U rule, or as a failed fit, not measured, or not readable); the
    mechanism description of G; the primary's AUC with n_present/n_absent, p_S (S28) and p_P;
    both ceilings; the R/W reading on each D1 candidate; the lambda each knockout fit selected,
    and a G reached through lambda = 100 named; the n_deg sentence above 5; the No contingency
    when triggered. The fixed-lambda diagnostic is not on this line. With lobe: the lobe prefix
    (section 4.1 (1)), the reading of a failed fit on a male block (section 4.1 (4)), and, if
    SEAL_RECORD says the seal was broken before review, the builder's note (S26)."""
    r = ev["rows"]["rule"]
    s = label_text(ev["label"], dl, u_rule, ev["U_reasons"], r["ceiling_block"])
    if lobe is not None and u_kind(ev["U_reasons"]) == "failed_fit" and ev["label"] == "U":
        s += f" [{FAILED_FIT_READING}]"
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
    if lobe is not None:
        s = lobe_prefix(lobe) + s
        if SEAL_RECORD != "intact":
            s += " " + SEAL_BROKEN_NOTE + "."
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


def csv_compare(ref, got, limit=20):
    """Sections 3.3 and 7 (revisions 3.2, 3.3): two synthetic_worlds.csv byte strings compared
    on the deciding columns, rows matched by CSV_KEY_COLUMNS. Separate outputs: rows missing on
    either side (or a duplicated key); key-matched rows whose values differ (CSV_EXACT_COLUMNS
    exactly, CSV_CONTINUOUS_COLUMNS within MACHINE_CHECK_TOL); a change of row order (a fact, not
    an outcome). Column 8 (mechanism_description) is reported, not gated (S17: A's check against
    its revision 3.2 rename is A's history and is not carried over). Outcome 1: all equal; 2: continuous within tolerance only; 3: part "a"
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
    "(ko, full, block, ko1, sh, pc) over all 637 keys per world: p on the 64 cells, lambda, the "
    "labels and the score fields; read it first. "
    "(2) The leg-P null generator (uniform_perms, rc_patterns): the null-input digests in the "
    "manifest (null_input_digests); each male reference records them in its manifest "
    "(synthetic_only.json), so they can be compared with the lobe's reference. "
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


def reference_mode(lobe):
    """S17: True when the lobe's reference is registered (PRERUN_SHA256 and
    PRERUN_WORLDS_CSV_SHA256 set); False in pre-run mode, while they are placeholders."""
    return PRERUN_SHA256[lobe] is not None and PRERUN_WORLDS_CSV_SHA256[lobe] is not None


def check_prerun_files(lobe):
    """A revision 3.2 (Ark N3), per lobe (S17): every file listed in the lobe's
    PRERUN_DIR/SHA256SUMS.txt is read and its sha256 (raw bytes) must equal the listed value and
    PRERUN_SHA256[lobe]; the list must name exactly the pinned files. Entries of the folder that
    are neither listed nor pinned are reported in "unlisted", never failed."""
    d, pins = PRERUN_DIR[lobe], PRERUN_SHA256[lobe] or {}
    sums = d / "SHA256SUMS.txt"
    if not pins:
        return {"passed": False, "sums_file": str(sums), "files": {}, "unlisted": [],
                "reason": f"lobe {lobe}: no registered reference (PRERUN_SHA256 is a placeholder)"}
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
        p = d / name
        files[name] = {"listed": listed.get(name), "pinned": pins.get(name),
                       "read": hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None}
    bad = [n for n, f in files.items() if not (f["read"] == f["listed"] == f["pinned"]
                                               and f["read"] is not None)]
    known = set(files) | {"SHA256SUMS.txt"}
    unlisted = [p.name + ("/" if p.is_dir() else "") for p in sorted(d.iterdir())
                if p.name not in known]
    return {"passed": not bad, "sums_file": str(sums), "files": files, "unlisted": unlisted,
            "reason": ("every listed file matches its listed and pinned sha256" if not bad
                       else "differs or missing: " + ", ".join(bad))
            + (f"; present but neither listed nor pinned (reported, not failed): "
               f"{', '.join(unlisted)}" if unlisted else "")}


def check_prerun_reproduced(got, comparable, reread=False, lobe=None):
    """Sections 3.3, 7 (A revisions 3.1, 3.2), per lobe (S17): the synthetic step must reproduce
    the lobe's pinned table, PRERUN_DIR[lobe]/synthetic_worlds.csv, on its deciding columns
    (csv_compare; outcome 1 or 2 passes, outcome 3 stops). Byte identity is recorded, not gated.
    passed is None when the run is not comparable (smoke, or starts != 10), when the table was
    re-read from saved fits (--from-raw), and in pre-run mode (no registered reference: this run
    makes it). False stops the two-world check."""
    ref_path = PRERUN_DIR[lobe] / "synthetic_worlds.csv"
    base = {"lobe": lobe, "prerun_path": str(ref_path),
            "prerun_sha256_pinned": PRERUN_WORLDS_CSV_SHA256[lobe],
            "recomputed_sha256": hashlib.sha256(got).hexdigest(),
            "reread_from_saved_fits": bool(reread), "byte_identical": None, "outcome": None}
    if not reference_mode(lobe):
        return {**base, "passed": None,
                "reason": f"pre-run mode (lobe {lobe}): no registered reference; this run makes "
                          "it (D15 (i)), so there is nothing to reproduce"}
    if not comparable:
        return {**base, "passed": None, "reason": "not comparable (smoke or starts != 10)"}
    files = check_prerun_files(lobe)
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
              f"(reported, not gated)")
    if reread:
        return {**base, "passed": None,
                "reason": "re-read from saved fits (--from-raw), not a reproduction; compared "
                          "with the pre-run table for information only: " + detail}
    return {**base, "passed": cmp["passed"], "reason": detail}


def raw_fits_diagnostic(F, fresh=None, reread_note=None, ref=None, lobe=None):
    """A revisions 3.2, 3.3 (A1, A6, A8); diagnostic, decides nothing. The fits of this run
    compared with the lobe's pinned raw_fits.json.gz (or `ref`, that store already read), key by
    key (STORE_FIELDS_COMPARED; secs excluded by name, STORE_FIELDS_EXCLUDED; every field seen
    must be declared in one of the two). S17: split by kind of fit only (ko, full, block, ko1;
    sh for the shuffles, pc for the permuted-block ceilings): each male reference is made by one
    fitting run, so A's split by the run that fitted each world does not arise."""
    ref = read_raw(PRERUN_DIR[lobe] / "raw_fits.json.gz") if ref is None else ref
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
    n_nr = kinds.count("not_readable")                 # S16: counted apart, never a threshold U
    order = [f[0] for f in FAMILIES]
    fams = sorted({w["family"] for w in worlds}, key=order.index)
    freq = {f: {"U": sum(w["label"] == "U" for w in worlds if w["family"] == f),
                "n": sum(w["family"] == f for w in worlds)} for f in fams}
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
    its ko1 records of the world banks. The pinned store at revision 3.4 gives 225 records, 47
    copied and 178 fitted (5 of them by the path check, on world:W:0)."""
    return ko1_count(v for (bk, mk, _), v in ref.items()
                     if mk == "ko1" and bk.startswith("world:") and "|" not in bk)


KO1_COUNT_CONTROL = (
    "the provenance split of the ko1 records (reused_from_ko): a fresh synthetic step, comparable "
    "to the reference, must reproduce the registered count read from the pinned "
    "raw_fits.json.gz, or it stops; under --from-raw the count is read from the store this pass "
    "re-reads, so the check is informative; a smoke run or starts != 10 is not compared")


def check_ko1_count(got, registered, comparable, reread, prerun=False):
    """A revision 3.4.1 (item A): the ko1 count of this run (ko1_count over the world banks)
    against the registered one (registered_ko1_count on the lobe's pinned store). passed is True
    or False for a fresh comparable run (False stops the synthetic step), and None (informative)
    under --from-raw, when the run is not comparable, and in pre-run mode (S17: no registered
    store yet; this run's count is registered from the store it writes)."""
    equal = None if registered is None else got == registered
    if prerun:
        passed, status = None, ("pre-run mode: no registered store; this run's count is "
                                "registered from the store it writes (section 3.3, D15)")
    elif not comparable:
        passed, status = None, "not compared (smoke or starts != 10)"
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


def board_smallest_passing_auc():
    """Pre-run mode (S17): each board's smallest_passing_auc from its labels and uniform_perms()
    alone (section 3.3: it depends on nothing else), so it is lobe-independent by construction."""
    perms = uniform_perms()
    return {b: smallest_passing_auc(board_y(b), board_y(b)[perms]) for b in ("z", "z'")}


def run_synthetic(args, lobe, bank, terms, F=None):
    """Section 3.6, per lobe (D6 (b)): the 45 worlds on the lobe's degree terms, grid and
    content pool, their legs and ceilings, each read by section 4; the three limits and the U
    rule; the lobe's reproduction gate and the two-world check. F, when given, holds saved fits
    (--from-raw): they are re-read, and only the fits missing from it are made. In pre-run mode
    (the lobe's PRERUN_* are placeholders) the registered values are computed, not checked, and
    there is nothing to reproduce (S17). The caller stops on a failed requirement."""
    specs = [w for w in world_specs() if w["family"] in args.families
             and w["j"] < args.worlds_per_family]
    saved = dict(F or {})
    F = dict(saved)
    n_saved = len(F)
    init_args = (args.starts, terms, True, lobe, True, None)   # a synthetic pool (S5, S6)
    pool = content_pool(bank)
    ref_mode = reference_mode(lobe)
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
    # A revision 3.4.1 (items A, B), per lobe: the registered values of the smallest_passing_auc
    # check and of the ko1 count are read from the lobe's pinned reference, so its files are
    # verified first; a failure stops before any fit. Pre-run mode: no reference exists yet.
    if ref_mode:
        prerun_files = check_prerun_files(lobe)
        if not prerun_files["passed"]:
            log(f"PRE-RUN REFERENCE NOT VERIFIED (lobe {lobe}): {prerun_files['reason']}; the "
                "registered values of the smallest_passing_auc check and of the ko1 count are "
                "read from it, so the synthetic step stops before any fit, and the real arm does "
                "not run (section 3.3)")
            sys.exit(1)
        spa_reg = derive_smallest_passing_auc(PRERUN_DIR[lobe] / "synthetic_only.json")
    else:
        spa_reg = {"source": "pre-run mode: computed from each board's labels and uniform_perms()",
                   "passed": True, "by_board": board_smallest_passing_auc(),
                   "n_worlds_by_board": None, "reason": "pre-run mode (S17): no reference; the "
                   "values are registered from this run's synthetic_only.json (section 3.3)"}
        log(f"PRE-RUN MODE (lobe {lobe}): PRERUN_SHA256 and PRERUN_WORLDS_CSV_SHA256 are "
            "placeholders; this run makes the lobe's reference and checks none (D15 (i))")
    log(f"smallest_passing_auc registered values (lobe {lobe}; {spa_reg['source']}): "
        f"{spa_reg['by_board']}; worlds by board {spa_reg['n_worlds_by_board']}; "
        f"{spa_reg['reason']}")
    if not spa_reg["passed"]:
        log(f"SMALLEST PASSING AUC REGISTERED VALUES NOT DERIVED: {spa_reg['reason']}; the "
            "synthetic step stops before any fit, and the real arm does not run (sections 3.3, 7)")
        sys.exit(1)
    # Revision 3.4 (item 2): smallest_passing_auc against its registered value by board, before
    # any fit (it depends only on y and Yu). y is read from the saved store where it holds the
    # world's base knockout record (--from-raw), and otherwise from the world generator.
    spa_in = []
    for w in specs:
        bk = f"world:{w['family']}:{w['j']}"
        rec = saved.get((bk, "ko", "N1"))
        y = (rec["y"] if rec is not None
             else make_world(w, terms, pool).exists[BLOCK_CELLS[:, 0], BLOCK_CELLS[:, 1]])
        spa_in.append({"world": bk, "board": w["board"], "y": y})
    spa = check_smallest_passing_auc(spa_in, spa_reg["by_board"])
    spa["registered_source"] = spa_reg
    source = (spa_reg["source"] if not ref_mode
              else "derived from the lobe's pinned synthetic_only.json")
    log(f"smallest_passing_auc check (A revision 3.4, before the fits; lobe {lobe}): "
        f"{spa['n_equal']} of {spa['n_worlds']} worlds equal the value by board "
        f"{spa['registered_by_board']} ({source}); {spa['gates']}")
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
    # over the store this run reads. Revision 3.4.1 (item A): a registered control, against the
    # count derived from the pinned raw_fits.json.gz (read once here, and reused by the per-fit
    # diagnostic below); a fresh comparable run with a different count stops.
    got = ko1_count(F[(bk, "ko1", pk)] for bk in keys for pk in ("rule",) + BF_KEYS)
    n_path = len(path_check.get("identical") or {}) if path_check.get("bank") else 0
    ref_store = (read_raw(PRERUN_DIR[lobe] / "raw_fits.json.gz") if comparable and ref_mode
                 else None)
    ko1_check = check_ko1_count(got, registered_ko1_count(ref_store) if ref_store else None,
                                comparable, reread, prerun=not ref_mode)
    ko1_check.update(fitted_by_path_check=n_path, path_check_bank=path_check.get("bank"),
                     this_pass={"copied": fl["reused"], "fitted": fl["fitted"] + n_path})
    log(f"ko1 records (revision 3.4.1; {ko1_check['status']}): {got['ko1_records']}; copied "
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
        ev = evaluate_bank(f"world:{w['family']}:{w['j']}", F, args.shuffles, args.perm_ceilings,
                           "synthetic")
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
    repro = check_prerun_reproduced(worlds_csv_bytes(worlds), comparable, reread, lobe)
    log(f"pre-run table (section 7): {repro['reason']}; recomputed sha256 "
        f"{repro['recomputed_sha256']}")
    raw_diag = None
    if comparable and repro.get("prerun_files", {}).get("passed"):
        # revision 3.3 (A6): under --from-raw the comparison is marked for what it is
        fresh = {k for k, v in F.items() if saved.get(k) is not v}
        note = None
        if reread:
            rec = getattr(args, "from_raw_record", None) or {}
            if rec.get("sha256") == PRERUN_SHA256[lobe]["raw_fits.json.gz"]:
                note = (f"re-read: compares the pinned store with itself; carries no information "
                        f"(apart from the {len(fresh)} fits this pass made, counted as "
                        f"fitted_this_pass)")
            else:
                note = ("re-read of a store other than the pinned one: compares that store's "
                        f"fits, and the {len(fresh)} fits this pass made, with the pinned ones; "
                        "not a reproduction")
        raw_diag = raw_fits_diagnostic(F, fresh, note, ref_store, lobe)
        if note:
            log(f"per-fit diagnostic: {note}")
        log(f"per-fit diagnostic against the lobe's pre-run raw fits (decides nothing): "
            f"{raw_diag['total']}")
    syn = {"lobe": lobe, "reference_mode": ref_mode, "worlds": worlds, "two_world_check": two_world_check(worlds, repro), "limits": dl,
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
    log(f"outside density {ev['outside_density']:.4f}; block present {ev['block_present']}/64; "
        f"n_deg = {ev['n_deg']} of {ev['rows']['rule']['n_shuffles']}; smallest passing AUC "
        f"(p_P <= 0.01, own draws) = {fmt(ev['smallest_passing_auc'])}")
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
        "the count n_ge, p_S is information (S28))")
    for pk in PRED_KEYS:
        r = ev["rows"][pk]
        log(f"  {r['predictor']:10s} quadrant mean p: " + ", ".join(
            f"{k} {v:.3f}" for k, v in r["quadrant_mean_p"].items())
            + "; mirrors: " + ", ".join(f"{k} {v:.3f}" for k, v in r["mirror_partners_p"].items())
            + f"; AUC on the other {N_OTHER_CELLS} = {fmt(r['auc_other_61'])}")
        log(f"  {'':10s} per-type AUC: " + ", ".join(f"{k} {fmt(v, 2)}"
                                                   for k, v in r["per_type_auc"].items()))
        oc = r["present_cells_offset_counts_sign"]
        log(f"  {'':10s} offset, counts, sign ({oc['label']}): " + ", ".join(
            f"{k} {fmt(v)}" for k, v in oc["values"].items()))
    if ev["perm_ceilings_full_rule"]:
        log(f"permuted-block ceiling_full of rule #2.1 ({len(ev['perm_ceilings_full_rule'])}): "
            + ", ".join(fmt(x, 3) for x in ev["perm_ceilings_full_rule"])
            + f"  (this block's ceiling_full {fmt(ev['rows']['rule']['ceiling_full'])})")
    log(f"reading A (rule #2.1): {ev['reading_A_rule']}; reading B (BF_1): {ev['reading_B_BF1']}")
    log(f"VERDICT LINE: {ev['verdict_line']}")
    if ev["U_reasons"]:
        log("U because: " + "; ".join(ev["U_reasons"]))
    if ev["label"] == "U":
        log(f"N1's own p_P beside the U (decides nothing; section 3.5): "
            f"{ev['rows']['N1']['p_P']:.4f}")
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
    L = [f"## Two-world check, lobe {syn['lobe']} (section 3.6; A section 3.6)", "",
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
          "Per-fit diagnostic against the lobe's pre-run raw fits ("
          + (syn["raw_fits_diagnostic"]["status"] if syn.get("raw_fits_diagnostic")
             else "decides nothing") + "): "
          + (f"{syn['raw_fits_diagnostic']['total']}; by kind "
             f"{ {k: v['compared'] for k, v in syn['raw_fits_diagnostic']['kinds'].items()} }"
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

# S15: the arm's own column names (its references are written by this script): precision at
# n_present for precision at 32, the other 61 cells for the other 59; 33 columns, as A's.
CSV_FIELDS = ("predictor", "auc", "D", "logloss", "logloss_margin_over_N1", "precision_at_n_present",
              "ceiling_full", "ceiling_block", "regrown_share_full", "regrown_share_block",
              "M_real", "n_ge", "n_shuffles", "n_deg", "n_valid_shuffles", "p_S", "p_P",
              "p_P_rowcol", "lambda_ko", "lambda_full", "lambda_block", "auc_other_61")
WORLDS_CSV_HEADER = (("family", "j", "seed", "gamma_z", "gamma_z1", "board", "label",
                      "mechanism_description", "outside_density") + CSV_FIELDS
                     + ("auc_fixed_lambda1", "p_P_fixed_lambda1"))  # 33 columns, as revision 3
# Revision 3.2 (A1): the columns of synthetic_worlds.csv by how the reproduction gate compares
# them. Exact: the identity columns of a row, and the lattice columns, whose values are exact
# dyadic or rational fractions with steps of at least 1e-4 (AUCs, p values, counts, lambdas, and
# outside_density, a count over the 2,961 placed outside cells; S14), so a tolerance adds
# nothing. Continuous, within
# MACHINE_CHECK_TOL: D, the log-losses, and the regrown_share ratios (not on a lattice).
# Reported, not gated: mechanism_description (column 8).
CSV_EXACT_COLUMNS = ("family", "j", "seed", "gamma_z", "gamma_z1", "board", "predictor",
                     "label", "outside_density", "auc", "precision_at_n_present", "ceiling_full",
                     "ceiling_block", "M_real", "n_ge", "n_shuffles", "n_deg",
                     "n_valid_shuffles", "p_S", "p_P", "p_P_rowcol", "lambda_ko", "lambda_full",
                     "lambda_block", "auc_other_61", "auc_fixed_lambda1", "p_P_fixed_lambda1")
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
    """S20, section 7.4 (5): where the registered run writes its private and raw outputs,
    outside the repository: connectome-seed-data/knockout_regrow/malecns_<UTC stamp>_<head 12>."""
    return PRIVATE_ROOT / f"{arm}_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}_{head[:12]}"


def protected_references():
    """S18: the reference folders --out must never touch, each with its pins (None when it has
    none yet): A's, B's (the folder B section 3.3 proposes), and the two male references. Read
    at call time, so the tests can point them at temporary folders."""
    return ([("A", A_PRERUN_DIR, A_PRERUN_SHA256), ("B", B_PRERUN_DIR, B_PRERUN_SHA256)]
            + [(f"male {lobe}", PRERUN_DIR[lobe], PRERUN_SHA256[lobe]) for lobe in LOBES])


def out_dir_refusal(out, arm=None):
    """A revision 3.3 (A2, C4), S18: why --out must not be written, or None. Refused: --out with
    --arm (the real arm writes to private_run_dir); --out at or inside A's, B's or either male
    reference folder; and a folder that holds a byte copy of a pinned reference (at least one
    file named like a pinned one is present, and every such present file matches its pin). A
    missing pinned-name file is not a differing one; a reference without pins (B's, or a male
    one while its pins are placeholders) is guarded by its path only. Falsifier (A section 7):
    the content guard tells a copy from a fresh run's folder only because write_raw's gzip
    carries its mtime."""
    if out is None:
        return None
    if arm:
        return ("REFUSED: --out is not used with --arm; the real arm writes its private outputs "
                "to connectome-seed-data/knockout_regrow/<run> (section 7.4)")
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


def quote_section(start_marker, end_marker, registration=REGISTRATION):
    text = (ROOT / registration).read_text(encoding="utf-8")
    s, e = text.index(start_marker), text.index(end_marker)
    return "\n".join(("> " + ln) if ln else ">" for ln in text[s:e].rstrip().splitlines())


def quote_row(label):
    """A section 4's table row for a label, verbatim (lesson f). S2, D12: read from the amended
    A (A_REGISTRATION), never from this arm's registration, which holds no such row (quoting from
    it would raise StopIteration). The first line that starts with the key is A section 4's,
    since section 4 precedes section 5 and the amendment is appended after A's last line."""
    key = {"R": "| **R: regrows**", "W": "| **W: rule weaker",
           "U": "| **U: on the detection threshold",
           "G": "| **G: not detected at the R level above γ_R**"}[label[0]]
    text = (ROOT / A_REGISTRATION).read_text(encoding="utf-8")
    return next(ln for ln in text.splitlines() if ln.startswith(key))


def md_bank_table(ev):
    L = ["| predictor | AUC (n_p/n_a) | D | log-loss | margin over N1 | P@n_present | ceiling_full | "
         "ceiling_block | share (full) | share (block) | n_ge / n_valid | p_S | p_P | "
         "p_P row-col (diagnostic) | lambda ko/full/block |",
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
    md = [f"# Knock out and regrow, male CNS arm: synthetic step, lobe {syn['lobe']} "
          f"({manifest['mode']})", "",
          f"Registration `{REGISTRATION}`, revision {REGISTRATION_REVISION}. "
          f"{'SMOKE RUN, NOT THE REGISTERED RUN. ' if manifest['smoke'] else ''}"
          f"{NOT_A_REFERENCE_TEXT + '. ' if manifest.get('not_a_reference') else ''}"
          f"git_head={manifest['git_head']}, runtime={manifest.get('runtime_s', 0):.0f}s.", ""]
    md += md_synthetic(syn)
    (out / "SYNTHETIC.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
    write_sha256sums(out)
    log(f"wrote {out}")


# ------------------------------------------------------------------------------------------
# S23, sections 4.2, 4.3 and 5: the lobe comparison, the male reading, the joint reading.

OUTSIDE_DISAGREEMENT = (36, 2961)                      # section 1.4: 36 of 2,961 outside cells
K_STAR_REGISTERED = 4                                  # section 4.3
K_STAR_ALPHA = 0.01
SPLIT_CLASS_TEXT = {
    "S0": ("Block A is the same in both lobes at c*; the split comes from the instrument's "
           "response to the lobes' other differences (36 of 2,961 outside cells) or from the "
           "threshold of detection, not from block A."),
    "S1": ("Block A differs between the lobes in {k} of 64 cells, within the lobes' outside rate "
           "(36 / 2,961, expected about 0.8 of 64): not read as a difference specific to block A. "
           "Variation within the animal and a reconstruction difference are not separated."),
    "S2a": ("Block A differs between the lobes more than the rest of the lobe does ({k} of 64; "
            "P(X >= k) = {tail} under the outside rate), and no differing cell lies near the "
            "cut: a difference specific to block A. Its two explanations, variation within the "
            "animal and a difference of reconstruction or typing of the block types, are not "
            "separated by this test. The R1–R6 asymmetry is excluded as its carrier (R1 is not a "
            "block type, and R1's row and column are the same cells in both lobes at c*)."),
    "S2b": ("Block A differs between the lobes in {k} of 64 cells (P(X >= k) = {tail} under the "
            "outside rate), and {j} of them lie near the cut: block cells at the threshold; the "
            "same mechanism as 33 of the 36 differing outside cells; specificity to block A not "
            "established.")}


def binomial_tail(k, n, p):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))


def k_star():
    """Section 4.3: the smallest k with P(X >= k) <= 0.01 for X ~ Binomial(64, 36 / 2,961)."""
    p = OUTSIDE_DISAGREEMENT[0] / OUTSIDE_DISAGREEMENT[1]
    return next(k for k in range(N_BLOCK + 1) if binomial_tail(k, N_BLOCK, p) <= K_STAR_ALPHA)


def lobe_split_class(y_L, y_R, x_L, x_R, c_star=C_STAR):
    """S23, section 4.3 (revision 1.1): the class of the lobes' block difference. k = cells whose
    presence differs; k* = 4 (computed, asserted equal to the registration). S0: k = 0; S1:
    1 <= k < k*; S2a: k >= k* and every differing cell has x outside [0.5 c*, 2 c*] in both
    lobes; S2b: its complement (at least one differing cell with x in the band in at least one
    lobe). Printed with each differing cell, its presence and band flags, j (the differing cells
    that fail S2a's condition) and the direction count beside the outside's 3 against 33. The
    binomial reference is descriptive; the class decides no label."""
    yL, yR = np.asarray(y_L, bool), np.asarray(y_R, bool)
    xL, xR = np.asarray(x_L, float), np.asarray(x_R, float)
    ks = k_star()
    assert ks == K_STAR_REGISTERED, f"k* = {ks}, registered {K_STAR_REGISTERED}"
    lo, hi = BAND[0] * c_star, BAND[1] * c_star
    cells = []
    for i in np.flatnonzero(yL != yR):
        s, t = BLOCK_NAMES[i]
        inL, inR = bool(lo <= xL[i] <= hi), bool(lo <= xR[i] <= hi)
        cells.append({"cell": f"{s}->{t}", "present_L": bool(yL[i]), "present_R": bool(yR[i]),
                      "x_L_in_band": inL, "x_R_in_band": inR, "near_cut": inL or inR})
    k = len(cells)
    j = sum(c["near_cut"] for c in cells)
    p = OUTSIDE_DISAGREEMENT[0] / OUTSIDE_DISAGREEMENT[1]
    tail = binomial_tail(k, N_BLOCK, p)
    cls = "S0" if k == 0 else ("S1" if k < ks else ("S2a" if j == 0 else "S2b"))
    return {"class": cls, "k": k, "k_star": ks, "j_near_cut": j, "tail_P_X_ge_k": tail,
            "band": [lo, hi], "text": SPLIT_CLASS_TEXT[cls].format(k=k, j=j, tail=f"{tail:.4g}"),
            "direction": {"L_only": int((yL & ~yR).sum()), "R_only": int((~yL & yR).sum()),
                          "outside_L_only": LOBE_AGREEMENT_EXPECTED["L_only"],
                          "outside_R_only": LOBE_AGREEMENT_EXPECTED["R_only"]},
            "differing_cells": cells}


def split_class_committed(sc):
    """Section 7.4 (5): what the committed outputs hold of the lobe comparison: the class, the
    counts, and the differing cells by name with their presence (no x, no band flag per cell)."""
    return {k: v for k, v in sc.items() if k != "differing_cells"} | {
        "differing_cells": [{k: c[k] for k in ("cell", "present_L", "present_R")}
                            for c in sc["differing_cells"]]}


def lobe_status(ev=None, no_auc=None):
    """What section 4.2 reads from a lobe: its letter, and whether it can be read. A lobe with
    no AUC (check 3) or with the not-readable U (section 3.2) cannot be read."""
    if ev is None:
        return {"letter": None, "readable": False,
                "reason": f"{NO_AUC_TEXT} ({no_auc} of 64 present)", "W_ranks": []}
    if not ev.get("readable", True):
        return {"letter": "U", "readable": False, "reason": ev["U_reasons"][0], "W_ranks": []}
    return {"letter": ev["label"], "readable": True, "reason": None,
            "W_ranks": ev["reading_A_rule"]["W_ranks"]}


def male_reading(st):
    """S23, section 4.2 (D3): the male reading from the two lobes' statuses (lobe_status). A male
    R needs R in both lobes (a conjunction: stricter in power, hardly stricter in null); a common
    letter is the male letter; a lobe that cannot be read gives "one lobe only", never a male R;
    any other pair is a split, with no male label."""
    cannot = [lobe for lobe in LOBES if not st[lobe]["readable"]]
    if len(cannot) == 2:
        return {"label": "none", "text": "neither lobe can be read: " + "; ".join(
            f"lobe {lobe} ({st[lobe]['reason']})" for lobe in LOBES)}
    if len(cannot) == 1:
        bad = cannot[0]
        good = next(lobe for lobe in LOBES if lobe != bad)
        return {"label": "one lobe only",
                "text": (f"one lobe only: lobe {good} reads {st[good]['letter']}; lobe {bad} "
                         f"cannot be read ({st[bad]['reason']}). Not a male "
                         f"{st[good]['letter']}.")}
    a, b = st["L"]["letter"], st["R"]["letter"]
    if a == b:
        text = {"R": "R: regrows in both lobes of one animal",
                "W": (f"W in both lobes; the ranks that passed: lobe L "
                      f"{', '.join(st['L']['W_ranks'])}; lobe R {', '.join(st['R']['W_ranks'])}"),
                "G": "G in both lobes, each with its own limits",
                "U": "U in both lobes, each with its own U text"}[a]
        return {"label": a, "text": text}
    return {"label": "split", "text": (f"split: lobe L reads {a}, lobe R reads {b}. A split is not "
                                       "R, W or G on the male CNS")}


FLYVIS65_LABEL = "G"          # commit 1ed55ec, knockout_regrow/RESULT.md line 5 (section 0)
MALE_G_SENTENCE = ("power of the male R not calibrated; this G does not by itself exclude "
                   "averaging as the explanation of flyvis-65's G")
JOINT_READING = {
    "R": ("R on the male CNS only: a flag",
          "Neither verdict is overturned. flyvis-65's G stands. The male R reads: \"regrows in "
          "both lobes of one animal, on an existence bank at one cut; the template does not show "
          "it at the R level.\" The flag is a registered list of what must be examined, under a "
          "new registration, not by a rerun: (i) the averaging of flyvis-65 (per offset, merged "
          "over two flies, column-averaged) against one animal's type-pair means (builder "
          "section 8), the column-test anchor of A section 0 in the other direction; (ii) the "
          "threshold: the male block is cut at c*, chosen on outside cells, and flyvis's by eq. 8 "
          "per offset; (iii) the prior exposure of section 1.5; (iv) typing by connectivity in "
          "the male CNS (A section 6). No consequence for the forward path is drawn from a male "
          "R alone"),
    "W": ("any other pair",
          "flyvis-65's G stands alone. Printed beside it: \"in both lobes of one animal the "
          "outside implies block A for a BF_r while rule #2.1 misses; on the template no BF_r "
          "passed\". It bears on A's column-test anchor (averaging may hide information the "
          "animal carries) and on the rule (W); it changes no registered label"),
    "G": ("any other pair",
          "Agreement: \"not detected at the R level in the template or in either lobe of one "
          "animal, each against its own limits\". The limits are not compared across banks as "
          "numbers (section 3.6). A G in the animal does not strengthen flyvis-65's G beyond its "
          "own limits. " + MALE_G_SENTENCE[0].upper() + MALE_G_SENTENCE[1:]),
    "other": ("any other pair",
              "flyvis-65's G stands alone; the male reading, its lobe labels and, for a split, "
              "its class (section 4.3) are printed beside it")}


def joint_reading(male):
    """S23, section 5 (D16): the joint reading with flyvis-65's G, a table lookup."""
    row, text = JOINT_READING.get(male["label"], JOINT_READING["other"])
    return {"flyvis65": FLYVIS65_LABEL, "male": male["label"], "A_D13_row": row, "text": text}


def a_literals_line(ev, lobe, dl, ur, inferable):
    """Section 4.1 (3), S2: printed after each quoted row of A section 4: which literals of the
    row are A's (flyvis-65's) and this lobe's own values."""
    lab = ev["label"]
    if lab == "R":
        return (f"A's literal in the quoted row: \"on flyvis's averaged template\" names A's bank; "
                f"here the bank is lobe {lobe} of one male, an existence bank at c* = "
                f"{C_STAR_TEXT} (section 5).")
    if lab == "W":
        return (f"The quoted row carries no flyvis-65 value; the rank(s) that passed in lobe "
                f"{lobe}: {', '.join(ev['reading_A_rule']['W_ranks']) or 'none'}.")
    if lab == "G":
        return (f"A's literal in the quoted row: \"64/64 inferable\" is A's count on flyvis-65; "
                f"lobe {lobe}: {inferable}/64 inferable at c* (check 4). The limits and the "
                f"instrument on the label are lobe {lobe}'s own (section 3.6).")
    s = (f"A's literals in the quoted row: \"all 3 pre-run U worlds sit at γ = 0.6 = γ*_P\" are "
         f"A's flyvis-65 pre-run worlds; lobe {lobe}'s worlds: {ur['n_u_threshold']} threshold U "
         f"on the dense grid, gamma*_P = {dl['leg_P']['text']}; \"the block is rank 1\" is "
         f"flyvis-65's board (A section 2.4); lobe {lobe}'s block is not known to be rank 1, so a "
         f"failed fit reads as a failed fit or a rank limit, not separated (section 4.1 (4)).")
    if not ev.get("readable", True):
        s += (" This lobe's U is the \"not readable\" U of section 3.2, which A's row does not "
              "name (section 4.1 (2)).")
    return s


# ------------------------------------------------------------------------------------------
# S21, section 7.4: the unseal step, check 11.

SEALED_HEADER = ["src", "tar", "W", "n_tar", "x", "present"]
SEALED_TRAILER = "# cross_lobe_block_weight_total="
_UNSEAL = {"allowed": False}


def parse_sealed(text, lobe, c_star=C_STAR):
    """Check 11 (after the hash): the builder's fixed-width sealed format
    (male_cns_bank_builder.py write_sealed): the header, 64 rows src,tar,W,n_tar,x,present with
    W and n_tar 12-digit integers and x = W / n_tar printed as {x:.6e}, and one trailer line
    "# cross_lobe_block_weight_total=...". Required: 64 rows; the names exactly the 64 block
    cells, each once; the printed x equal to W / n_tar in the builder's format; present ==
    (x >= c* and x > 0) on every row, with x = W / n_tar (the exact value the builder cut, not
    its 7-digit print) and c* from bank.meta.json. Else "SEALED FILE INCONSISTENT", which stops
    the arm. Returns the block's labels and x in block cell order and the present cells with
    n_syn = x."""
    lines = [ln for ln in text.split("\n") if ln != ""]
    bad = []
    if not lines or lines[0].split(",") != SEALED_HEADER:
        bad.append(f"header {lines[0] if lines else None!r}")
    data = [ln for ln in lines[1:] if not ln.startswith("#")]
    trailer = [ln for ln in lines[1:] if ln.startswith("#")]
    if len(data) != N_BLOCK:
        bad.append(f"{len(data)} rows, 64 expected")
    if len(trailer) != 1 or not trailer[0].startswith(SEALED_TRAILER):
        bad.append(f"trailer {trailer!r}")
    rows = {}
    for ln in data:
        f = ln.split(",")
        if len(f) != len(SEALED_HEADER):
            bad.append(f"row {ln!r}: {len(f)} fields")
            continue
        s, t, W, n, xs, pr = f
        if (s, t) in rows or (s, t) not in set(BLOCK_NAMES):
            bad.append(f"row {s} -> {t}: not a block cell, or twice")
            continue
        try:
            W, n, pr = int(W), int(n), int(pr)
        except ValueError:
            bad.append(f"row {s} -> {t}: W, n_tar or present not an integer")
            continue
        if W < 0 or n <= 0 or pr not in (0, 1):
            bad.append(f"row {s} -> {t}: W {W}, n_tar {n}, present {pr}")
            continue
        x = W / n
        if xs != f"{x:.6e}":
            bad.append(f"row {s} -> {t}: x printed {xs}, W / n_tar gives {x:.6e}")
        if pr != int(x >= c_star and x > 0):
            bad.append(f"row {s} -> {t}: present {pr} contradicts x and c*")
        rows[(s, t)] = (x, bool(pr))
    if set(rows) != set(BLOCK_NAMES):
        bad.append(f"block cells missing: {sorted(set(BLOCK_NAMES) - set(rows))}")
    if bad:
        log(f"SEALED FILE INCONSISTENT (lobe {lobe}, check 11): " + "; ".join(bad[:10]))
        sys.exit(1)
    y = np.array([rows[k][1] for k in BLOCK_NAMES])
    x = np.array([rows[k][0] for k in BLOCK_NAMES])
    present = {(H.IDX[s], H.IDX[t]): rows[(s, t)][0] for s, t in BLOCK_NAMES if rows[(s, t)][1]}
    return {"lobe": lobe, "y": y, "x": x, "present_cells": present,
            "cross_lobe_line": trailer[0],
            "check_11": {"rows": len(data), "names_exact": True, "present_consistent": True,
                         "passed": True}}


def sealed_path(lobe):
    return Path(SEALED_DIR) / SEALED_NAME[lobe]


def verify_sealed_pins():
    """Section 7.4 (2): both sealed files' sha256 against their pins, before either is parsed,
    so that a mismatch in one lobe stops the arm with both seals intact ("SEALED FILE PIN
    DIFFERS"). Hashing reads the raw bytes; nothing is decoded or parsed."""
    got = {lobe: hashlib.sha256(sealed_path(lobe).read_bytes()).hexdigest() for lobe in LOBES}
    bad = {lobe: (h, SEALED_SHA256[lobe]) for lobe, h in got.items() if h != SEALED_SHA256[lobe]}
    if bad:
        log(f"SEALED FILE PIN DIFFERS: {bad}; no sealed file was parsed; the seal is intact "
            "(section 7.4 (2))")
        sys.exit(1)
    return {"sha256": got, "passed": True}


def open_sealed(lobe):
    """S21, section 7.4: the only reader of a sealed file. Refused unless the registered real
    arm has set _UNSEAL["allowed"] after every gate that does not need the sealed files (checks
    1, 2, 4, 7, 8, 10; both lobes' synthetic steps; checks 6 and 9 on both lobes). The raw
    bytes are hashed and compared with the pin before anything is decoded or parsed; a mismatch
    stops with "SEALED FILE PIN DIFFERS" and the file unparsed. Then check 11 (parse_sealed)."""
    if not _UNSEAL["allowed"]:
        raise RuntimeError("REFUSED: open_sealed is called only by the registered real arm, "
                           "after every gate that does not need the sealed files (section 7.4)")
    path = sealed_path(lobe)
    raw = path.read_bytes()
    h = hashlib.sha256(raw).hexdigest()
    if h != SEALED_SHA256[lobe]:
        log(f"SEALED FILE PIN DIFFERS (lobe {lobe}): {h}, pinned {SEALED_SHA256[lobe]}; the file "
            "was not parsed (section 7.4 (2))")
        sys.exit(1)
    return {**parse_sealed(raw.decode("utf-8"), lobe), "sha256": h}


# ------------------------------------------------------------------------------------------
# Sections 3.4, 7.4: the real arm's checks before and after unsealing (S22).

def check_harness_identity(a):
    """Check 8 (once; S6): BF_1's full-bank C6 existence margin on flyvis-65 reproduces
    0.028150051052145946 to 1e-9, before any grid restriction, in a pool whose initializer does
    not restrict (the FlyWire arm's "wrapper on flyvis bank, unpatched grid")."""
    assert len(H.ALL_CELLS) == 65 * 65, "check 8 runs before the restriction"
    groups = [[("flyvis65", f"cv:{f}", pk)] for pk in ("BF:1", "N1") for f in range(H.N_FOLDS)]
    det = run_groups(groups, a.workers, (a.starts, None, True, None, False, None),
                     "check 8 (flyvis-65, full grid)")
    bf = [det[("flyvis65", f"cv:{f}", "BF:1")]["score"] for f in range(H.N_FOLDS)]
    n1s = [det[("flyvis65", f"cv:{f}", "N1")]["score"] for f in range(H.N_FOLDS)]
    m = H.margin(bf, n1s, "existence")
    if abs(m - BF1_FULL_BANK_MARGIN) > IDENTITY_TOL:
        log(f"HARNESS IDENTITY FAILS: BF_1 margin {m!r}, registered {BF1_FULL_BANK_MARGIN!r}")
        sys.exit(1)
    return {"BF1_margin": m, "registered": BF1_FULL_BANK_MARGIN,
            "difference": m - BF1_FULL_BANK_MARGIN, "grid": 65 * 65, "passed": True}


def checks_before_unsealing(a, lobe, terms):
    """S22, checks 6 and 9 before unsealing (section 3.4): rule #2.1's knockout fit on the lobe's
    bank with its block filled two ways, all absent (the outside bank) and the board z, must give
    byte-identical data dicts (else "BLOCK LEAKS INTO TRAINING"); and the knockout fit twice on
    the lobe's knockout view must agree (else "NOT DETERMINISTIC"). A synthetic pool: no worker
    holds the real block. Returns the hash that check 6' compares after unsealing."""
    groups = [[("outside", "ko#hash#0", "rule")], [("outside", "ko#hash#1", "rule")],
              [("outside|fill:z", "ko#hash#0", "rule")]]
    det = run_groups(groups, a.workers, (a.starts, terms, True, lobe, True, None),
                     f"checks 6, 9 (lobe {lobe}, before unsealing)")
    h0 = det[("outside", "ko#hash#0", "rule")]["data_sha256"]
    h1 = det[("outside", "ko#hash#1", "rule")]["data_sha256"]
    hz = det[("outside|fill:z", "ko#hash#0", "rule")]["data_sha256"]
    if h0 != hz:
        log(f"BLOCK LEAKS INTO TRAINING (lobe {lobe}, check 6, before unsealing)")
        sys.exit(1)
    if h0 != h1:
        log(f"NOT DETERMINISTIC (lobe {lobe}, check 9)")
        sys.exit(1)
    return {"6_leakage": {"block_all_absent_sha256": h0, "block_board_z_sha256": hz,
                          "passed": True},
            "9_determinism": {"sha256_fit_1": h0, "sha256_fit_2": h1, "passed": True},
            "knockout_sha256": h0}


def real_arm_lobe(a, lobe, terms, bank, sealed, syn, h_before, inferable):
    """Section 7.4 (3), per lobe, after unsealing: check 10 on the real bank; check 3 (the print;
    no AUC stops this lobe only); check 5 (printed); the real arm's fits (knockout, both
    ceilings, the shuffles, the permuted-block ceilings, fixed lambda = 1) and check 6' (the
    knockout fit on the real bank must give the pre-unseal hash); the verdict line."""
    rb = real_bank(bank, sealed["present_cells"], lobe)
    grid = check_grid([rb])
    y = np.asarray(sealed["y"], bool)
    assert np.array_equal(rb.exists[BLOCK_CELLS[:, 0], BLOCK_CELLS[:, 1]], y)
    c3 = check_block_print(y, lobe)
    c5 = check_n1_parity(H.fit_n1(H.make_view(rb, MASKS["ko"])), y)
    log(f"check 5 (lobe {lobe}; printed, decides nothing): D(N1 logit) = {fmt(c5['D_N1_logit'])}, "
        f"block balanced: {c5['balanced']}")
    init = (a.starts, terms, False, lobe, True, sealed["present_cells"])
    groups = [[("real", "ko#hash#0", "rule")]]
    if c3["has_auc"]:
        groups += plan_bank("real", a.shuffles, a.perm_ceilings)
    Fr = run_groups(groups, a.workers, init, f"real arm, lobe {lobe}")
    h_real = Fr.pop(("real", "ko#hash#0", "rule"))["data_sha256"]
    if h_real != h_before:
        log(f"BLOCK LEAKS INTO TRAINING (lobe {lobe}, check 6', after unsealing): {h_real}, "
            f"before unsealing {h_before}")
        sys.exit(1)
    checks = {"10_grid_real_bank": grid, "3_block_print": c3, "5_n1_parity": c5,
              "6prime_leakage": {"real_knockout_sha256": h_real, "before_unsealing": h_before,
                                 "passed": True}}
    if not c3["has_auc"]:
        return {"lobe": lobe, "ev": None, "checks": checks, "fits": Fr,
                "status": lobe_status(None, c3["present"])}
    fl = complete_fixed_lambda(Fr, ["real"], a.workers, init,
                               f"real arm, lobe {lobe}, fixed lambda = 1 (diagnostic)")
    ev = evaluate_bank("real", Fr, a.shuffles, a.perm_ceilings, "real")
    ev["label_text"] = label_text(ev["label"], syn["limits"], syn["u_rule"], ev["U_reasons"],
                                  ev["rows"]["rule"]["ceiling_block"])
    ev["verdict_line"] = verdict_line(ev, syn["limits"], syn["u_rule"],
                                      syn["two_world_check"]["no_contingency"], lobe=lobe)
    ev["quoted_row"] = quote_row(ev["label"])
    ev["a_literals_line"] = a_literals_line(ev, lobe, syn["limits"], syn["u_rule"], inferable)
    ev["fixed_lambda_fits"] = fl
    return {"lobe": lobe, "ev": ev, "checks": checks, "fits": Fr, "status": lobe_status(ev)}


# ------------------------------------------------------------------------------------------
# S19, section 7.5: outputs.

def write_committed(summary, syn, real, reading, split, joint, cross_lines):
    """S19: RESULT.md, summary.json, per_shuffle_<lobe>.csv, synthetic_worlds_<lobe>.csv, all
    aggregates (section 7.4 (5)): the male reading first, then each lobe's verdict line, the
    quoted A section 4 row and the line naming A's literals; the lobe comparison; the joint
    reading with flyvis-65."""
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(dump_json(summary), encoding="utf-8", newline="\n")
    for lobe in LOBES:
        write_worlds_csv(syn[lobe]["worlds"], OUT / f"synthetic_worlds_{lobe}.csv")
        if real[lobe]["ev"] is not None:
            write_per_shuffle_csv(real[lobe]["ev"], OUT / f"per_shuffle_{lobe}.csv")
    md = ["# Knock out and regrow, male CNS arm: block A in each optic lobe of one male", "",
          f"Registration `{REGISTRATION}`, revision {REGISTRATION_REVISION}; A "
          f"`{A_REGISTRATION}` (amended, LF sha256 {A_REGISTRATION_SHA256_LF_AMENDED}). "
          f"git_head={summary['manifest']['git_head']}, runtime={summary['runtime_s']:.0f}s. "
          f"Seal record: {SEAL_RECORD}.", "",
          f"**Male reading: {reading['text']}**", ""]
    for lobe in LOBES:
        r, c = real[lobe], real[lobe]["checks"]
        md += [f"## Lobe {lobe}", ""]
        if r["ev"] is None:
            md += [f"**{lobe_prefix(lobe)}{r['status']['reason']}: no label (check 3).**", ""]
        else:
            ev = r["ev"]
            md += [f"**Verdict: {ev['verdict_line']}**", "",
                   "The A section 4 row, verbatim (from the amended A):", "",
                   "> " + ev["quoted_row"], "", ev["a_literals_line"], ""]
            if ev["label"] == "U":
                md += [f"N1's own p_P beside the U (decides nothing): "
                       f"{ev['rows']['N1']['p_P']:.4f}.", ""]
            md += md_bank_table(ev) + [
                "", f"Smallest passing AUC on this block (own draws; not compared with the other "
                f"lobe): {fmt(ev['smallest_passing_auc'])}. Row-and-column null: "
                f"{ev['row_and_column_null'].get('text') or ev['row_and_column_null']['status']}.",
                "", "Permuted-block ceiling_full of rule #2.1: "
                + ", ".join(fmt(x, 3) for x in ev["perm_ceilings_full_rule"])
                + f" (real block {fmt(ev['rows']['rule']['ceiling_full'])}).", "",
                "Fixed lambda = 1 on the knockout view, diagnostic, decides nothing: " + "; ".join(
                    f"{v['predictor']} AUC {fmt(v['auc'])}, p_P {v['p_P']:.4f}"
                    for v in ev["fixed_lambda"].values()) + ".", "",
                f"Offset, counts and sign fields: {MEANINGLESS_LABEL} (in summary.json).", ""]
        c3 = c["3_block_print"]
        md += [f"Check 3 (printed): present {c3['present']}/64; quadrants {c3['quadrants']}; row "
               f"counts {c3['row_counts']}; column counts {c3['column_counts']}; y = x * w: "
               f"{c3['y_equals_x_times_w']}; balanced: {c3['balanced']}. Check 5 (printed): "
               f"D(N1 logit) = {fmt(c['5_n1_parity']['D_N1_logit'])}.", ""]
    md += ["## The lobe comparison (section 4.3)", ""]
    if split is None:
        md += ["Not computed: a lobe's block was not unsealed.", ""]
    else:
        md += [f"Class {split['class']}: {split['text']} k = {split['k']} (k* = "
               f"{split['k_star']}), j = {split['j_near_cut']}; direction L-only "
               f"{split['direction']['L_only']} against R-only {split['direction']['R_only']} "
               f"(outside: 3 against 33). Differing cells: "
               + (", ".join(f"{d['cell']} (L {int(d['present_L'])}, R {int(d['present_R'])})"
                            for d in split["differing_cells"]) or "none") + ".", ""]
    md += ["## The joint reading with flyvis-65 (section 5)", "",
           f"flyvis-65 reads {joint['flyvis65']}; the male reading is {joint['male']} (A's D13 "
           f"row: {joint['A_D13_row']}). {joint['text']}.", "",
           WITHIN_ANIMAL_NOTE + ".", "",
           "Cross-lobe block weight, from the sealed files (printed after the verdicts): "
           + "; ".join(f"lobe {lobe}: {cross_lines[lobe]}" for lobe in LOBES) + ".", "",
           "## Pre-data tables (section 1.4)", ""]
    t4 = summary["checks"]["4_pre_data_tables"]
    for lobe in LOBES:
        t = t4["tables"][lobe]
        md += [f"Lobe {lobe}: inferable {t['inferable']}/64; mirrors {t['mirrors']}; training "
               f"present {t['training_present']} of {N_TRAIN_CELLS}; R1 and CT1(M10) rows and "
               f"columns {t['population_rows']}; endpoints {t['endpoints']}.", ""]
    ag = t4["lobe_agreement"]
    md += [f"Lobe agreement outside the block: both {ag['both']}, L only {ag['L_only']}, R only "
           f"{ag['R_only']}; near the cut in both lobes {ag['differ_near_cut_both_lobes']}.", ""]
    md += [f"- {b}: {v} ({s})" for b, v, s in INFERABILITY_PROVENANCE]
    for lobe in LOBES:
        md += ["", f"# Synthetic step, lobe {lobe}", ""] + md_synthetic(syn[lobe])
    md += ["## The registered reading of this arm (section 4, quoted)", "",
           quote_section("## 4. Reading rule", "## 5. What each outcome means"), ""]
    (OUT / "RESULT.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
    log(f"wrote {OUT}")


# ------------------------------------------------------------------------------------------
# S20: main. --synthetic-only --lobe L|R (the pre-run) and --arm malecns (the registered run).

def make_manifest(a, mode, head, dirty, pins, terms, private, lobes, smoke, extra=None):
    return {"registration": REGISTRATION, "revision": REGISTRATION_REVISION,
            "registration_sha256_lf": sha256_lf(ROOT / REGISTRATION),
            "a_registration": A_REGISTRATION,
            "a_registration_sha256_lf": pins["a_registration_sha256_lf"],
            "a_registration_pinned_amended": A_REGISTRATION_SHA256_LF_AMENDED,
            "a_registration_flyvis65_text": A_REGISTRATION_SHA256_LF_FLYVIS65,
            "builder_registration": BUILDER_REGISTRATION,
            "builder_registration_sha256_lf": pins["builder_registration_sha256_lf"],
            "bank_meta_json_sha256": BANK_META_SHA256_READ, "male_pins": MALE_PINS,
            "c_star": C_STAR, "seal_record": SEAL_RECORD,
            "script_sha256_lf": sha256_lf(Path(__file__)), "git_head": head,
            "tree_dirty_under_c6_or_plans": bool(dirty),
            "tree_dirty_paths": dirty.splitlines() if dirty else [],
            "allow_dirty": bool(a.allow_dirty), "mode": mode, "lobes": list(lobes),
            "smoke": smoke, "worlds_per_family": a.worlds_per_family, "shuffles": a.shuffles,
            "perm_ceilings": a.perm_ceilings, "families": a.families, "starts": a.starts,
            "workers": a.workers, "python": pins["python"], "numpy": pins["numpy"],
            "device": "CPU", "from_raw": a.from_raw,
            "from_raw_record": getattr(a, "from_raw_record", None),
            "private_outputs": str(private) if private else None,
            "prerun_dir": {lobe: str(PRERUN_DIR[lobe]) for lobe in LOBES},
            "prerun_worlds_csv_sha256": PRERUN_WORLDS_CSV_SHA256, "prerun_sha256": PRERUN_SHA256,
            "machine_record": machine_record(),
            "degree_terms": {lobe: {"c": terms[lobe][0], "a": terms[lobe][1], "b": terms[lobe][2],
                                    "source": f"N1 on lobe {lobe}'s knockout view on the placed "
                                              "grid (outside bank only)"} for lobe in terms},
            **(extra or {})}


def common_checks(a, pins):
    """Checks 2, 4, 7 and 10 and the seeds, in every mode, after the restriction: from the
    outside files only (both lobes' tables and the lobe agreement)."""
    restrict_to_placed_grid()
    banks = {lobe: load_male_bank(lobe) for lobe in LOBES}
    checks = {"1_pins": pins, "10_grid": check_grid(banks.values())}
    log(f"check 10 (grid): passed; len(H.ALL_CELLS) = {len(H.ALL_CELLS)}; both lobes' banks on "
        "the placed grid")
    checks["2_block_and_mask"] = check_block_and_mask()
    log(f"check 2 (block and mask): passed; views {checks['2_block_and_mask']['views']}")
    tables = {lobe: pre_data_tables(banks[lobe]) for lobe in LOBES}
    checks["4_pre_data_tables"] = check_pre_data_tables(tables, lobe_agreement(banks))
    log("check 4 (pre-data tables of section 1.4): passed; " + "; ".join(
        f"lobe {lobe}: inferable {tables[lobe]['inferable']}/64, mirrors {tables[lobe]['mirrors']}, "
        f"training present {tables[lobe]['training_present']}" for lobe in LOBES)
        + f"; lobe agreement {LOBE_AGREEMENT_EXPECTED}")
    checks["7_auc_function"] = check_auc_function()
    log("check 7 (AUC function on hand-made inputs): passed")
    seeds = assert_seeds_unique(a.starts)
    log(f"seeds (section 3.7): {seeds}")
    return banks, tables, checks, seeds


def log_terms(lobe, terms):
    log(f"section 3.6 degree terms, lobe {lobe}: N1 (c, a, b) on the lobe's knockout view "
        f"({N_TRAIN_CELLS} placed outside cells; no block cell read); c = {terms[0]:+.4f}, "
        f"a in [{terms[1].min():+.3f}, {terms[1].max():+.3f}], "
        f"b in [{terms[2].min():+.3f}, {terms[2].max():+.3f}]")


def run_synthetic_only(a, t0, smoke):
    """The pre-run (D15 (i)) and any later synthetic-only run of one lobe. It reads the outside
    files only; it never builds, fits or scores a bank that holds the real block, and never
    opens, hashes, counts or sizes a sealed file. A full (comparable) run refuses a dirty tree
    unless --allow-dirty, which marks it NOT A REFERENCE."""
    dirty = git("status", "--porcelain", "--", "results/genome/c6", "docs/plans")
    comparable = not smoke and a.starts == 10
    if dirty and comparable and not a.allow_dirty:
        sys.exit("REFUSED: a full --synthetic-only run makes the lobe's reference, which must come "
                 "from a committed head (D15 (i)); commit first, or pass --allow-dirty to run it "
                 "as NOT A REFERENCE.\n" + dirty)
    not_a_reference = bool(dirty) and comparable
    pins = check_pins()
    log(f"registration: {REGISTRATION}, revision {REGISTRATION_REVISION}; SYNTHETIC ONLY, lobe "
        f"{a.lobe}{'; SMOKE, not the registered run' if smoke else ''}"
        f"{'; ' + NOT_A_REFERENCE_TEXT if not_a_reference else ''}; k = {a.starts}; workers = "
        f"{a.workers}; CPU (the pinned harness is numpy-only, section 7.1)")
    log(f"check 1 (pins, versions, rule #2.1 RANK = 1): passed; Python {pins['python']}, numpy "
        f"{pins['numpy']}; c* = {C_STAR}; A's registration LF sha256 "
        f"{pins['a_registration_sha256_lf']} (recorded)")
    banks, tables, checks, seeds = common_checks(a, pins)
    terms = degree_terms(banks[a.lobe])
    log_terms(a.lobe, terms)
    a.from_raw_record = None
    if a.from_raw:
        fr = Path(a.from_raw)
        a.from_raw_record = {"path": str(fr), "exists": fr.is_file(),
                             "sha256": (hashlib.sha256(fr.read_bytes()).hexdigest()
                                        if fr.is_file() else None)}
        pins_l = PRERUN_SHA256[a.lobe] or {}
        a.from_raw_record["is_the_pinned_store"] = (a.from_raw_record["sha256"]
                                                    == pins_l.get("raw_fits.json.gz"))
    head = git("rev-parse", "HEAD")
    manifest = make_manifest(a, "synthetic-only", head, dirty, pins, {a.lobe: terms},
                             Path(a.out) if a.out else None, [a.lobe], smoke,
                             {"not_a_reference": NOT_A_REFERENCE_TEXT if not_a_reference
                              else None,
                              "reference_mode": reference_mode(a.lobe),
                              "sealed_files_touched": False})
    syn, F = run_synthetic(a, a.lobe, banks[a.lobe], terms,
                           read_raw(a.from_raw) if a.from_raw else None)
    print_synthetic(syn)
    rp = syn["two_world_check"]["prerun_reproduction"]
    manifest["prerun_csv_byte_identical"] = rp["byte_identical"]
    manifest["prerun_comparison_outcome"] = rp["outcome"]
    manifest["prerun_reread_from_saved_fits"] = rp["reread_from_saved_fits"]
    manifest["prerun_comparison_outcome_3_parts"] = rp.get("outcome_3_parts")
    manifest["null_input_digests"] = null_input_digests()
    log(f"null-input digests: {manifest['null_input_digests']}")
    log(f"machine record: thread variables {manifest['machine_record']['thread_env']}; machine "
        f"{manifest['machine_record']['machine']}")
    manifest["runtime_s"] = time.time() - t0
    if a.out:
        write_synthetic_outputs(a.out, {**syn, "checks": checks, "seeds": seeds}, F, manifest)
    if not syn["two_world_check"]["passed"]:
        treatment = (repro_fail_treatment(rp.get("outcome_3_parts") or ("a", "b"))
                     if rp["passed"] is False else "")
        log(f"TWO-WORLD CHECK FAILED (lobe {a.lobe}): a requirement marked stop failed, or the "
            "pre-run table was not reproduced (outcome 3); the real arm does not run (sections "
            "3.3, 3.6). " + treatment)
        sys.exit(1)
    log(f"\n--synthetic-only (lobe {a.lobe}): stopped before any real block; no sealed file was "
        f"touched. {time.time() - t0:.0f}s")
    return syn


def _untee(fh):
    for name in ("stdout", "stderr"):
        s = getattr(sys, name)
        if isinstance(s, _Tee):
            setattr(sys, name, s.stream)
    fh.close()


def run_real_arm(a, t0, smoke=False):
    """S20, sections 4.2 and 7.4 (D2, D10): the registered run, both lobes in one invocation
    from one committed head with one manifest. Order: refusals and pins; check 8 before any
    restriction; checks 2, 4, 7, 10; both lobes' synthetic steps (both must pass: stop rows and
    reproduction gates) and the lobes' equal smallest_passing_auc by board; checks 6 and 9 on
    both lobes; then, and only then, both sealed files' pins, their unsealing and check 11; both
    real arms; the male reading, the lobe comparison, the joint reading; the outputs."""
    constants = check_registered_constants()
    dirty = refuse_if_dirty()
    pins = check_pins(real_arm=True)
    head = git("rev-parse", "HEAD")
    private = private_run_dir("malecns", head)
    private.mkdir(parents=True, exist_ok=False)
    fh = tee_to(private / "stdout.log")
    try:
        return _run_real_arm(a, t0, smoke, constants, dirty, pins, head, private)
    finally:
        _untee(fh)


def _run_real_arm(a, t0, smoke, constants, dirty, pins, head, private):
    log(f"registration: {REGISTRATION}, revision {REGISTRATION_REVISION}; arm malecns (both "
        f"lobes, D2){'; SMOKE, not the registered run' if smoke else ''}; k = {a.starts}; "
        f"workers = {a.workers}; CPU; private outputs {private}")
    log(f"check 1 (pins, versions, rule #2.1 RANK = 1, the amended A): passed; Python "
        f"{pins['python']}, numpy {pins['numpy']}; c* = {C_STAR}")
    chk8 = check_harness_identity(a)
    log(f"check 8 (harness identity, full grid, before the restriction): passed; {chk8}")
    banks, tables, checks, seeds = common_checks(a, pins)
    checks["registered_constants"] = constants
    checks["8_harness_identity"] = chk8
    terms = {lobe: degree_terms(banks[lobe]) for lobe in LOBES}
    for lobe in LOBES:
        log_terms(lobe, terms[lobe])
    a.from_raw_record = None
    manifest = make_manifest(a, "malecns", head, dirty, pins, terms, private, LOBES, smoke)
    syn, F = {}, {}
    for lobe in LOBES:
        syn[lobe], F[lobe] = run_synthetic(a, lobe, banks[lobe], terms[lobe])
        print_synthetic(syn[lobe])
        write_synthetic_outputs(private / f"synthetic_{lobe}",
                                {**syn[lobe], "checks": checks, "seeds": seeds}, F[lobe],
                                {**manifest, "runtime_s": time.time() - t0})
    failed = [lobe for lobe in LOBES if not syn[lobe]["two_world_check"]["passed"]]
    if failed:
        rp = {lobe: syn[lobe]["two_world_check"]["prerun_reproduction"] for lobe in failed}
        log(f"TWO-WORLD CHECK FAILED in lobe(s) {failed}: a requirement marked stop failed, or the "
            "pre-run table was not reproduced (outcome 3). Both sealed files stay sealed; no real "
            f"block score exists (sections 3.3, 7.4). Private outputs: {private}. " + " ".join(
                repro_fail_treatment(r.get("outcome_3_parts") or ("a", "b"))
                for r in rp.values() if r["passed"] is False))
        sys.exit(1)
    spa = {lobe: syn[lobe]["smallest_passing_auc_check"]["registered_by_board"] for lobe in LOBES}
    got = {lobe: {p["board"]: p["computed"]
                  for p in syn[lobe]["smallest_passing_auc_check"]["per_world"]}
           for lobe in LOBES}
    if spa["L"] != spa["R"] or got["L"] != got["R"]:
        log(f"SMALLEST PASSING AUC DIFFERS BETWEEN THE LOBES (section 3.3): registered {spa}, "
            f"computed {got}; both sealed files stay sealed")
        sys.exit(1)
    log(f"smallest_passing_auc of the worlds, equal in both lobes board by board: {got['L']}")
    pre = {}
    for lobe in LOBES:
        pre[lobe] = checks_before_unsealing(a, lobe, terms[lobe])
        log(f"checks 6 (leakage) and 9 (determinism), lobe {lobe}, before unsealing: passed")
    checks["6_9_before_unsealing"] = {lobe: {k: v for k, v in pre[lobe].items()
                                             if k != "knockout_sha256"} for lobe in LOBES}

    # Section 7.4: the seal. Every gate that does not need the sealed files has passed.
    checks["sealed_pins"] = verify_sealed_pins()
    _UNSEAL["allowed"] = True
    log(f"UNSEALING at {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}: both lobes' "
        "synthetic steps and checks 1, 2, 4, 6, 7, 8, 9, 10 have passed (section 7.4 (1))")
    try:
        sealed = {lobe: open_sealed(lobe) for lobe in LOBES}
        for lobe in LOBES:
            checks[f"11_sealed_file_{lobe}"] = sealed[lobe]["check_11"]
            log(f"check 11 (sealed file, lobe {lobe}): passed")
        real = {lobe: real_arm_lobe(a, lobe, terms[lobe], banks[lobe], sealed[lobe], syn[lobe],
                                    pre[lobe]["knockout_sha256"], tables[lobe]["inferable"])
                for lobe in LOBES}
        return _finish_real_arm(a, t0, manifest, checks, seeds, tables, syn, sealed, real,
                                private)
    except BaseException as e:
        if not (isinstance(e, SystemExit) and e.code in (0, None)):
            log(f"FAILURE AFTER UNSEALING ({type(e).__name__}: {e}): the seal is broken without a "
                "verdict. The log and the private outputs are kept; the break is recorded in "
                "section 11's ledger; a second run from the same head only on Mike's word, with "
                "this run's log committed beside its outputs (section 7.4 (4)).")
        raise


def _finish_real_arm(a, t0, manifest, checks, seeds, tables, syn, sealed, real, private):
    for lobe in LOBES:
        r = real[lobe]
        if r["ev"] is not None:
            print_bank(r["ev"], f"male CNS, lobe {lobe}, the real block (section 3.5)")
            log(f"quoted A section 4 row: {r['ev']['quoted_row']}")
            log(r["ev"]["a_literals_line"])
        write_raw(r["fits"], private / f"raw_fits_real_{lobe}.json.gz")
    split = lobe_split_class(sealed["L"]["y"], sealed["R"]["y"], sealed["L"]["x"],
                             sealed["R"]["x"])
    reading = male_reading({lobe: real[lobe]["status"] for lobe in LOBES})
    joint = joint_reading(reading)
    if reading["label"] == "G":
        reading["text"] += f" ({MALE_G_SENTENCE})"
    log(WITHIN_ANIMAL_NOTE)
    for lobe in LOBES:
        ev = real[lobe]["ev"]
        log(f"\nVERDICT, lobe {lobe}: "
            + (ev["verdict_line"] if ev is not None
               else f"{lobe_prefix(lobe)}{real[lobe]['status']['reason']}"))
    log(f"\nMALE READING: {reading['text']}")
    log(f"lobe comparison (section 4.3): class {split['class']}: {split['text']} differing cells "
        f"{split['differing_cells']}; direction {split['direction']}")
    log(f"joint reading with flyvis-65 (section 5): {joint}")
    cross = {lobe: sealed[lobe]["cross_lobe_line"] for lobe in LOBES}
    log(f"cross-lobe block weight (printed after the verdicts; S21): {cross}")
    manifest["null_input_digests"] = null_input_digests()
    private_cells = {lobe: {"y": sealed[lobe]["y"], "x": sealed[lobe]["x"],
                            "sha256": sealed[lobe]["sha256"]} for lobe in LOBES}
    (private / "block_A_cells.json").write_text(
        dump_json({"per_cell_male_data": "private (section 7.4 (5))", "block_names":
                   [f"{s}->{t}" for s, t in BLOCK_NAMES], "lobes": private_cells,
                   "split_class": split}), encoding="utf-8", newline="\n")
    write_sha256sums(private)
    log(f"wrote {private}")
    summary = {"manifest": manifest, "checks": checks, "seeds": seeds,
               "inferability_provenance": INFERABILITY_PROVENANCE,
               "male_reading": reading, "joint_reading_with_flyvis65": joint,
               "lobe_comparison": split_class_committed(split),
               "cross_lobe_block_weight": cross,
               "real": {lobe: {"ev": real[lobe]["ev"], "status": real[lobe]["status"],
                               "checks": real[lobe]["checks"]} for lobe in LOBES},
               "synthetic": syn, "runtime_s": time.time() - t0}
    write_committed(summary, syn, real, reading, split_class_committed(split), joint, cross)
    log(f"wall-clock {summary['runtime_s']:.0f}s")
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--synthetic-only", action="store_true",
                      help="the pre-run of one lobe (--lobe); touches no sealed file")
    mode.add_argument("--arm", choices=["malecns"],
                      help="the registered run, both lobes (D2); opens the sealed files")
    ap.add_argument("--lobe", choices=list(LOBES), default=None,
                    help="with --synthetic-only: the lobe")
    ap.add_argument("--starts", type=int, choices=[3, 10], default=10)
    ap.add_argument("--workers", type=int, default=30)
    ap.add_argument("--out", default=None, help="with --synthetic-only: where to write")
    ap.add_argument("--allow-dirty", action="store_true",
                    help="--synthetic-only only: a full run from an uncommitted tree, marked NOT "
                         "A REFERENCE; refused with --arm malecns (D10)")
    ap.add_argument("--from-raw", default=None,
                    help="with --synthetic-only: re-read an earlier run's raw_fits.json.gz and "
                         "fit only what it lacks")
    ap.add_argument("--smoke-worlds", type=int, default=None, help="worlds per family (smoke)")
    ap.add_argument("--smoke-shuffles", type=int, default=None, help="shuffles per bank (smoke)")
    ap.add_argument("--smoke-perm-ceilings", type=int, default=None)
    ap.add_argument("--smoke-families", default=None, help="comma-separated subset (smoke)")
    a = ap.parse_args(argv)
    t0 = time.time()
    # D10, S20: refused before anything is read.
    if a.arm and a.allow_dirty:
        sys.exit(ALLOW_DIRTY_REFUSED)
    if a.arm and a.lobe:
        sys.exit("REFUSED: --arm malecns runs both lobes in one invocation (D2); --lobe is for "
                 "--synthetic-only")
    if a.synthetic_only and a.lobe is None:
        sys.exit("REFUSED: --synthetic-only needs --lobe L or R (the pre-run of one lobe, D15)")
    a.worlds_per_family = a.smoke_worlds if a.smoke_worlds is not None else WORLDS_PER_FAMILY
    a.shuffles = a.smoke_shuffles if a.smoke_shuffles is not None else N_SHUFFLES
    a.perm_ceilings = (a.smoke_perm_ceilings if a.smoke_perm_ceilings is not None
                       else N_PERM_CEILINGS)
    a.families = a.smoke_families.split(",") if a.smoke_families else [f[0] for f in FAMILIES]
    smoke = (a.worlds_per_family != WORLDS_PER_FAMILY or a.shuffles != N_SHUFFLES
             or a.perm_ceilings != N_PERM_CEILINGS or len(a.families) != len(FAMILIES))
    if a.arm and (smoke or a.from_raw or a.starts != 10):
        sys.exit("REFUSED: the real arm runs as registered: --starts 10, no smoke option, no "
                 "--from-raw (sections 3.3, 7.5)")
    refusal = out_dir_refusal(a.out, a.arm)
    if refusal:
        sys.exit(refusal)
    H.STARTS = a.starts
    if a.arm:
        return run_real_arm(a, t0)
    return run_synthetic_only(a, t0, smoke)


if __name__ == "__main__":
    main()
