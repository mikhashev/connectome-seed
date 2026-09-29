"""Torch-free pieces of the registered GPU instrument, shared by the GPU stage (torch venv) and the
CPU side (tools/.venv): key refusals, the batch-composition digest, the environment-stamp
comparison, the output guard, file and array hashes, the degree-term digest, store I/O.

Registration: docs/plans/2026-09-26-gpu-instrument-registration.md. The revision label that runs
print and record is derived from the file's content (its LF sha256 looked up in REGISTRATION_TEXTS,
G-(10) of revision 1.5), never hand-set; a text not in the table is labelled UNKNOWN.
Revision 1.5 (draft: docs/plans/2026-09-29-gpu-instrument-revision-1.5-draft.md) adds G17-G19:
  * R6 / G7 / T-G2: check_key accepts only "world:<family>:<j>" and "world:<family>:<j>|sh:<sd>".
  * R4 / D5 / G3 / T-G3: composition_digest over (ordered keys, starts, rank order); row_chunk and
    the chunk boundaries are recorded beside it (composition_record), outside the digest.
  * R4 / G18 / T-G11: the composition identity, three values compared together (an AND, not a
    re-hash): composition (the refusal digest of the keys), world (the degree-term digest, the
    content), script (arm module and lobe, a label). REGISTERED_COMPOSITION_IDENTITIES.
  * G19 / D11 / T-G11: arm_module_refusal, the closed set of arm modules each run kind may load
    (REGISTERED_ARM_MODULES for arm runs, empty until a revision names an arm;
    VALIDATION_ARM_MODULES for the validation labels).
  * R1 / D7 / G2 / G17 / T-G6: check_stamp against REGISTERED_STAMP, the stamp V1 measured
    (witnessed again by Ark on 2026-09-29); once it is registered, --stamp-unregistered refuses.
  * G11: out_dir_refusal, A's out_dir_refusal rule reimplemented (A's script is not modified).
  * D10: degree_terms_digest.
Nothing here imports torch. knockout_regrow (A's script, read-only) is imported lazily.
"""
import gzip
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent            # results/genome/c6/gpu_instrument
C6 = HERE.parent
ROOT = C6.parents[2]                                        # the repository root
for _p in (str(HERE), str(C6), str(C6 / "checks")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
REGISTRATION = "docs/plans/2026-09-26-gpu-instrument-registration.md"
# G-(10): the registration's texts by LF sha256 -> (revision, commit, note). The label a run
# prints and records is looked up from the file's content at import; the V0-V7 records carry
# the hand-set constant "1.3 (ec5cbc0)" of a0e16b6 while the text there was 0f5be2fc (revision
# 1.4); those records are not edited. A new revision adds its own row when it is merged.
REGISTRATION_TEXTS = {
    "97737b4c9dedcac025ab862653e2ad6a7b9f4ff2a4f7b82461e5988a8304f2ef": ("1", "fedeec5", ""),
    "2715e1a0723c53e4c852a2fb4231a683da7725a960794c8b06af64f4a1e82a32": ("1.1", "345acf2", ""),
    "a741367e7c3ae65548661c1819090af7ffa1f80cdcc3b376fe5162a9b90cea9a": ("1.2", "5983385", ""),
    "7d5d7ea921d41a440147cf6502ea52a41cb51068038d5d9fef1995317a49e540": ("1.3", "ec5cbc0", ""),
    "dffec1dc8e3d697555b007e6a0709cf9fd3b24c13aa3eae4c57a4486e666f99a": ("1.4", "e2fab47", ""),
    "0f5be2fc2133eba14b93f7525a80c594111a3ad42b7c6a76547eedafc7815c54": (
        "1.4", "e2fab47",
        "section 15.5 (Zcode's vote on revisions 1.3 and 1.4) added in a0e16b6"),
}


def registration_text_record(path=None):
    """G-(10): the registration's LF sha256 and the (revision, commit, note) it maps to."""
    p = ROOT / REGISTRATION if path is None else pathlib.Path(path)
    h = hashlib.sha256(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    rev, commit, note = REGISTRATION_TEXTS.get(
        h, ("UNKNOWN", None, f"text sha256 {h} is not a registered revision (REGISTRATION_TEXTS)"))
    return {"path": REGISTRATION, "sha256_lf": h, "revision": rev, "commit": commit, "note": note}


# Printed by the driver and the validation runner and recorded in manifests and validation rows;
# no digest and no refusal reads these strings.
REGISTRATION_TEXT = registration_text_record()
REGISTRATION_REVISION = REGISTRATION_TEXT["revision"]
REGISTRATION_COMMIT = REGISTRATION_TEXT["commit"]
REGISTRATION_NOTE = REGISTRATION_TEXT["note"] or f"text sha256 {REGISTRATION_TEXT['sha256_lf']}"
APPLIED_AHEAD = ("none: Ark's review of revision 1.3 (chat 12:09 UTC), points 1-3 (the BF-active "
                 "classification printed by the comparator; the per-fit census denominator; V6 on "
                 "the BF-active subset with 'uninformative' a recorded outcome), applied in the "
                 "code ahead of revision 1.4, is part of revision 1.4 (section 15.4, edits 1, 4 "
                 "and 5)")

# Section 1.3 / D7: the two environments.
TORCH_PY = ROOT.parent / "autoresearch-win-rtx" / ".venv" / "Scripts" / "python.exe"
CPU_PY = ROOT / "tools" / ".venv" / "Scripts" / "python.exe"
# Section 7: private run folders.
DATA_ROOT = ROOT.parent / "connectome-seed-data" / "gpu_instrument"
VALIDATION_DIR = HERE / "validation"                       # committed aggregates (section 7)

# ------------------------------------------------------------------------------------------
# R6 / G7: the keys a registered GPU run accepts.

KEY_RE = re.compile(r"^world:[A-Za-z][A-Za-z0-9.]*:[0-9]+(\|sh:[0-9]+)?$")


def check_key(key):
    """R6: only world:<family>:<j> and world:<family>:<j>|sh:<sd>. Refused: any base that is not
    world: (real, real|sh:, real|pc:, real|leak), any |pc: or |leak key (D1 (a)), anything
    malformed. Returns the key; raises ValueError("REFUSED ...") otherwise."""
    if not isinstance(key, str) or not KEY_RE.match(key):
        raise ValueError(f"REFUSED (R6): key {key!r} is not world:<family>:<j> or "
                         "world:<family>:<j>|sh:<sd>; the GPU instrument fits synthetic worlds "
                         "and their shuffles only (no real, |pc: or |leak key)")
    return key


def is_base_view(bank_key):
    return "|" not in bank_key


def split_record_key(rk):
    """'world:R:0|sh:3||ko||BF:2' -> ('world:R:0|sh:3', 'ko', 'BF:2')."""
    parts = rk.split("||")
    if len(parts) != 3:
        raise ValueError(f"REFUSED: malformed record key {rk!r}")
    return tuple(parts)


def bf_record_key(bank_key, r):
    return f"{bank_key}||ko||BF:{r}"


# ------------------------------------------------------------------------------------------
# R4 / D5 / G3: the batch composition.

def _canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def composition_digest(keys, starts, ranks):
    """The refusal digest: sha256 of the ordered key list, starts and the rank order. row_chunk
    is not in it (D5 (a), A3)."""
    keys = list(keys)
    for k in keys:
        check_key(k)
    return hashlib.sha256(_canon({"keys": keys, "starts": int(starts),
                                  "ranks": [int(r) for r in ranks]}).encode()).hexdigest()


def chunk_boundaries(n_problems, row_chunk, starts):
    """solve_problems' blocks (gpu_bf3.py:131, :142-143): per = max(1, row_chunk // starts)
    problems per block; boundaries are the block starts, and n_problems closes the last."""
    per = max(1, int(row_chunk) // int(starts))
    return {"problems": int(n_problems), "per_block": per,
            "boundaries": list(range(0, int(n_problems), per)) + [int(n_problems)]}


def composition_record(keys, starts, ranks, row_chunk, n_folds, n_lambdas):
    """The manifest's batch composition: the refusal digest and what it covers, and beside it
    (recorded, not refused on) row_chunk and every chunk boundary of every rank: the inner
    (bank, fold, lambda) problems of fit_bf_all, then the final fits (gpu_bf3.py:174-195)."""
    keys = list(keys)
    nb = len(keys)
    return {"refusal_digest": composition_digest(keys, starts, ranks),
            "refusal_digest_covers": "ordered key list, starts, rank order (D5 (a))",
            "keys_sha256": hashlib.sha256(_canon(keys).encode()).hexdigest(),
            "n_keys": nb, "starts": int(starts), "ranks": [int(r) for r in ranks],
            "recorded_not_refused": {
                "row_chunk": int(row_chunk), "n_folds": int(n_folds), "n_lambdas": int(n_lambdas),
                "problem_order": "bank, fold, lambda (gpu_bf3.fit_bf_all)",
                "chunks_per_rank": {
                    "inner": chunk_boundaries(nb * n_folds * n_lambdas, row_chunk, starts),
                    "final": chunk_boundaries(nb, row_chunk, starts)},
                "same_for_every_rank": True}}


def check_composition(found_digest, expected_digest):
    """R4: a registered GPU run must use the registered composition. expected None: nothing to
    compare (a validation run with no expected digest records its own)."""
    if expected_digest is None:
        return {"expected": None, "found": found_digest, "passed": None,
                "status": "no expected digest given (validation run: recorded, not compared)"}
    if found_digest != expected_digest:
        raise ValueError(f"REFUSED (R4): composition digest {found_digest} differs from the "
                         f"registered {expected_digest}")
    return {"expected": expected_digest, "found": found_digest, "passed": True,
            "status": "equal to the expected digest"}


# Registered compositions by name (D5 (a); G17, revision 1.5): the refusal digest V1 measured
# for A's 45 worlds x (99 shuffles + base view), starts 10, ranks 1-4 (V1's three manifests).
REGISTERED_COMPOSITION_DIGESTS = {
    "A": "a6a8a0dfd445f0dcc69fe29602af50b074e4534418082d37757c4580fdd72e8e"}

# G18 (revision 1.5): the composition identity. The refusal digest covers the key strings only,
# which are the same in every arm (V1 and V8 L, R share a6a8a0df...), so R4 compares three values
# together: composition (the refusal digest), world (the degree-term digest: what the banks are
# built from, the content), script (arm module and lobe: a label). No re-hash of the three.
IDENTITY_AXES = ("composition", "world", "script")
REGISTERED_COMPOSITION_IDENTITIES = {
    "A": {"composition": REGISTERED_COMPOSITION_DIGESTS["A"],
          "world": "d48adfbd3c27c90e16c699041c5f1e3d99be21838857b2816278e9dbcc5d9d6b",
          "script": {"module": "knockout_regrow", "lobe": None}}}


def composition_identity(composition_digest_value, degree_terms_digest_value, arm_module, lobe):
    return {"composition": composition_digest_value, "world": degree_terms_digest_value,
            "script": {"module": arm_module, "lobe": lobe}}


def check_composition_identity(found, expected):
    """R4 / G18: every axis equal, or ValueError naming the axes that differ."""
    if expected is None:
        return {"expected": None, "found": found, "passed": None,
                "status": "no expected identity given (validation run: recorded, not compared)"}
    diff = {ax: {"found": found.get(ax), "expected": expected.get(ax)} for ax in IDENTITY_AXES
            if found.get(ax) != expected.get(ax)}
    if diff:
        raise ValueError("REFUSED (R4, G18): the composition identity differs on "
                         f"{sorted(diff)}: {json.dumps(diff, sort_keys=True)}")
    return {"expected": expected, "found": found, "passed": True,
            "status": "equal to the expected identity on composition, world and script"}


# G19 (revision 1.5; D11): the arm modules each run kind may load. An arm run: only a module a
# revision registers for it, with its lobes and the names of its registered identities; none is
# registered (block A never, the male arm and block B stay on the CPU). A validation run: A's
# script under every label; the male arm's script only as V8 and the adapter's smoke test.
REGISTERED_ARM_MODULES = {}
VALIDATION_ARM_MODULES = {
    "knockout_regrow": {"labels": None, "lobes": (None,)},
    "knockout_regrow_male_cns": {"labels": ("V8", "smoke"), "lobes": ("L", "R")}}


def arm_module_refusal(kind, label, module, lobe):
    """G19: why `module` (with `lobe`) may not be loaded by a run of this kind and label, or
    None. The set is closed: a module named in neither registry is refused."""
    if kind == "arm":
        reg = REGISTERED_ARM_MODULES.get(module)
        if reg is None:
            return (f"REFUSED (G19, D11): arm module {module!r} is not in REGISTERED_ARM_MODULES "
                    f"({sorted(REGISTERED_ARM_MODULES) or 'none registered'}); an arm uses the "
                    "instrument only after a revision names it before its pre-run")
        if lobe not in reg["lobes"]:
            return f"REFUSED (G19): arm module {module!r} with lobe {lobe!r}; registered lobes " \
                   f"{reg['lobes']}"
        return None
    reg = VALIDATION_ARM_MODULES.get(module)
    if reg is None:
        return (f"REFUSED (G19, D11): arm module {module!r} is not a validation module "
                f"({sorted(VALIDATION_ARM_MODULES)})")
    if reg["labels"] is not None and label not in reg["labels"]:
        return (f"REFUSED (G19, D11): --arm-module {module} outside validation labels "
                f"{reg['labels']} (D11: that arm stays on the CPU; V8 is an unregistered "
                "cross-check)")
    if lobe not in reg["lobes"]:
        return (f"REFUSED (G19): --arm-module {module} needs --lobe L or R" if None not in
                reg["lobes"] else f"REFUSED (G19): --arm-module {module} takes no lobe")
    return None


# R4: the registered VRAM need before the upload, by row_chunk. Revision 1.5: at 40,000 the torch
# peak V1 measured under D6 (12,550 MiB, all three runs; M10's flag-free 12,526 was the value of
# revisions 1-1.4); at 100,000 the README's 26.5 GB (README:299-301; V4 (c) measured 24,300).
# Too little free VRAM stops the run; there is no automatic fallback.
REGISTERED_VRAM_NEED_MIB = {40000: 12550, 100000: int(26.5 * 1024)}

# ------------------------------------------------------------------------------------------
# R1 / D7 / G2: the environment stamp.

STAMP_FIELDS = ("python", "numpy", "torch", "cuda", "dll_sha256", "driver", "gpu_name")
STAMP_DLLS = ("cublas64_12.dll", "cublasLt64_12.dll", "cusolver64_11.dll")
# D7: "The registered stamp is the one measured in V1 and written into the revision that
# registers V1's results". Before revision 1.5 it was None, and only a validation run that
# declared it (allow_unregistered) could proceed.
# G17 (revision 1.5): the stamp V1 measured (equal in its three runs, V1.json), read again field by
# field by Ark on 2026-09-29 (DPC Research chat 08:37:58 UTC). Two witnesses.
REGISTERED_STAMP = {
    "python": "3.10.20", "numpy": "2.2.6", "torch": "2.9.1+cu128", "cuda": "12.8",
    "dll_sha256": {
        "cublas64_12.dll": "9513540e4ec4c51ee9e7304138c2cc255c29a8c181f9e80c38efa25738becd99",
        "cublasLt64_12.dll": "b199d1ff892a81b7fd3d57ba1781549609b41500b36008fef326038393ad46c7",
        "cusolver64_11.dll": "3d4f7a66b5f352db56d4bb5962bb453a42d5feb2d831779f4a0bebc9971c36fb"},
    "driver": "596.86", "gpu_name": "NVIDIA RTX PRO 4500 Blackwell"}
STAMP_NOT_REGISTERED_TEXT = ("STAMP NOT YET REGISTERED: validation run; the stamp is recorded "
                             "and compared with nothing (D7: V1 measures the registered stamp)")


def check_stamp(found, registered=None, allow_unregistered=False, use_module_default=True):
    """R1: the run's stamp against the registered one, field by field (STAMP_FIELDS; the DLL
    hashes one by one). Refuses (ValueError) on any difference. With no registered stamp:
    refuses unless allow_unregistered, and then returns status STAMP_NOT_REGISTERED_TEXT."""
    if registered is None and use_module_default:
        registered = REGISTERED_STAMP
    if registered is None:
        if not allow_unregistered:
            raise ValueError("REFUSED (R1): no registered environment stamp exists yet (D7: it is "
                             "the stamp measured in V1); only a validation run may proceed, and "
                             "it must say so (--stamp-unregistered)")
        return {"passed": None, "status": STAMP_NOT_REGISTERED_TEXT, "found": found,
                "registered": None, "differences": {}}
    if allow_unregistered:
        raise ValueError("REFUSED (R1): a stamp is registered; --stamp-unregistered is not "
                         "accepted once it is")
    diff = {}
    for f in STAMP_FIELDS:
        a, b = found.get(f), registered.get(f)
        if f == "dll_sha256":
            for d in sorted(set((a or {})) | set((b or {}))):
                if (a or {}).get(d) != (b or {}).get(d):
                    diff[f"dll_sha256.{d}"] = {"found": (a or {}).get(d),
                                               "registered": (b or {}).get(d)}
        elif a != b:
            diff[f] = {"found": a, "registered": b}
    if diff:
        raise ValueError("REFUSED (R1): the environment stamp differs from the registered one: "
                         + json.dumps(diff, sort_keys=True))
    return {"passed": True, "status": "equal to the registered stamp, field by field",
            "found": found, "registered": registered, "differences": {}}


# ------------------------------------------------------------------------------------------
# Hashes.

def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def sha256_lf(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def array_sha256(a):
    """sha256 of the raw little-endian float64 bytes (the probe's method): U, V, lambda, p."""
    import numpy as np
    return hashlib.sha256(np.ascontiguousarray(np.asarray(a, dtype="<f8")).tobytes()).hexdigest()


def degree_terms_digest(terms):
    """D10: sha256 over c, a, b as little-endian float64 bytes, in that order, with their shapes."""
    import numpy as np
    c, a, b = terms
    h = hashlib.sha256()
    for name, x in (("c", np.array([c], dtype="<f8")), ("a", np.asarray(a, dtype="<f8")),
                    ("b", np.asarray(b, dtype="<f8"))):
        h.update(name.encode())
        h.update(str(x.shape).encode())
        h.update(np.ascontiguousarray(x).tobytes())
    return h.hexdigest()


def instrument_file_hashes():
    """G2: the LF sha256 of every file of the instrument (the .py files and the README of this
    directory, tests included) and of A's pinned files, A's script and the harness."""
    out = {}
    for p in sorted(HERE.rglob("*.py")):
        if "__pycache__" in p.parts:
            continue
        out[p.relative_to(ROOT).as_posix()] = sha256_lf(p)
    out[(HERE / "README.md").relative_to(ROOT).as_posix()] = sha256_lf(HERE / "README.md")
    return out


def a_pinned_file_hashes():
    import knockout_regrow as K                            # read-only import
    out = {f: sha256_lf(ROOT / f) for f in K.PINS}
    out["results/genome/c6/checks/knockout_regrow.py"] = sha256_lf(C6 / "checks" /
                                                                   "knockout_regrow.py")
    return {"files": out, "pins_equal": all(out[f] == K.PINS[f] for f in K.PINS)}


# ------------------------------------------------------------------------------------------
# git: R7.

TREE_PATHS = ("results/genome/c6", "docs/plans")
# Validation runs write their committed aggregates here, so a later validation run excludes it
# from its tree check (recorded). A registered arm run excludes nothing.
VALIDATION_EXCLUDED = "results/genome/c6/gpu_instrument/validation/"


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                          check=True).stdout.rstrip()


def git_head():
    return git("rev-parse", "HEAD")


def tree_dirty_paths(exclude_validation=False):
    d = git("status", "--porcelain", "--", *TREE_PATHS)
    lines = [ln for ln in d.splitlines() if ln.strip()]
    if exclude_validation:
        lines = [ln for ln in lines if VALIDATION_EXCLUDED not in ln]
    return lines


# ------------------------------------------------------------------------------------------
# G11: the output guard.

# V8's inputs: the male arm's CPU pre-run stores, one per lobe (the male script's --synthetic-only
# --lobe L|R --out <folder>, started 2026-09-26 13:12:49 UTC; the male script's store format:
# raw_fits.json.gz, synthetic_only.json, synthetic_worlds.csv, SYNTHETIC.md, SHA256SUMS.txt).
MALE_PRIVATE_ROOT = ROOT.parent / "connectome-seed-data" / "knockout_regrow"
MALE_PRERUN_STORES = {lobe: MALE_PRIVATE_ROOT / f"malecns_prerun_{lobe}_20260926T131249Z"
                      for lobe in ("L", "R")}
# The male arm's registered reference folders (its PRERUN_DIR, S17), whatever their pins.
MALE_PRERUN_DIRS = [MALE_PRIVATE_ROOT / f"synthetic_malecns_{lobe}_prerun" for lobe in ("L", "R")]


def reference_dirs():
    """The reference folders no GPU run writes at or in: A's pinned pre-run folder, the
    registered flyvis-65 run's private folder (the store the unregistered v2/v3 runs read), and
    the male arm's pre-run folders (V8's inputs and the male PRERUN_DIR of both lobes). An arm
    that registers a pre-run folder of its own adds it here in that revision."""
    import knockout_regrow as K
    return ([pathlib.Path(K.PRERUN_DIR),
             pathlib.Path(K.PRIVATE_ROOT) / "flyvis65_20260925T171656Z_74de0401a21f"]
            + list(MALE_PRERUN_STORES.values()) + list(MALE_PRERUN_DIRS)
            + list(BLOCK_B_REFERENCE_DIRS))


# Revision 1.5 (R.7 (3)): block B's pinned pre-run folder and its registered run's folder
# (extension X's references), refused as output folders like the others.
BLOCK_B_REFERENCE_DIRS = (
    MALE_PRIVATE_ROOT / "synthetic_blockB_prerun_20260927T211052Z_5f9cc51b9a24",
    MALE_PRIVATE_ROOT / "flyvis65_blockB_20260928T143258Z_7a10d88ec95e")


def out_dir_refusal(out):
    """G11 (A's out_dir_refusal rule, reimplemented): why `out` must not be written, or None.
    Refused: `out` at or inside a reference folder; a folder that holds a byte copy of A's
    pinned reference (at least one file named like a pinned one is present, and every such
    present file equals its PRERUN_SHA256 pin)."""
    import knockout_regrow as K
    target = pathlib.Path(out).resolve()
    for ref in reference_dirs():
        ref = ref.resolve()
        if target == ref or target.is_relative_to(ref):
            return (f"REFUSED (G11): {target} is a pinned reference folder or inside one ({ref})")
    if target.is_dir():
        present = {n: sha256_file(target / n) for n in K.PRERUN_SHA256 if (target / n).is_file()}
        if present and all(present[n] == K.PRERUN_SHA256[n] for n in present):
            return (f"REFUSED (G11): {target} holds a byte copy of the pinned pre-run reference "
                    f"({', '.join(sorted(present))})")
    return None


def private_run_dir(tag, head):
    return DATA_ROOT / f"{tag}_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}_{head[:12]}"


def write_sha256sums(d):
    """SHA256SUMS.txt over every other file in d (raw bytes, sha256sum's binary format)."""
    d = pathlib.Path(d)
    lines = [f"{sha256_file(p)} *{p.name}" for p in sorted(d.iterdir())
             if p.is_file() and p.name != "SHA256SUMS.txt"]
    (d / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def check_sha256sums(d):
    """Every file listed in d/SHA256SUMS.txt exists and matches. Returns (passed, detail)."""
    d = pathlib.Path(d)
    sums = d / "SHA256SUMS.txt"
    if not sums.is_file():
        return False, {"reason": "SHA256SUMS.txt missing"}
    bad = {}
    for ln in sums.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        h, name = ln.split(maxsplit=1)
        name = name.lstrip("*")
        p = d / name
        got = sha256_file(p) if p.is_file() else None
        if got != h:
            bad[name] = {"listed": h, "read": got}
    return not bad, {"differs_or_missing": bad}


# ------------------------------------------------------------------------------------------
# Stores: A's raw_fits.json.gz format (K.write_raw / K.read_raw): {"bank||mask||pk": record}.

def json_safe(x):
    import knockout_regrow as K
    return K.json_safe(x)


def write_json(path, obj):
    pathlib.Path(path).write_text(json.dumps(json_safe(obj), indent=1, allow_nan=False),
                                  encoding="utf-8", newline="\n")


def write_json_gz(path, obj):
    with gzip.open(path, "wt", encoding="utf-8") as fh:
        json.dump(json_safe(obj), fh, allow_nan=False)


def read_json_gz(path):
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        return json.load(fh)


def read_store(path):
    """A store in A's format, keyed by the record key string."""
    return read_json_gz(path)
