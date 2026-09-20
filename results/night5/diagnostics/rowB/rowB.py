"""Row B -- passive per-cell-type activity recording on the complete runs of nights 1-5.

UNREGISTERED DIAGNOSTIC -- NOT A TEST.  Every output record carries
`"status": "unregistered_diagnostic"` and `"readable_as_verdict": false`.  No number this
script produces may be read as an outcome of the pre-registered experiment, today or later.

Field list: Ark, DPC Research group chat 2026-09-20 19:13 local, as recorded in the backlog
entry ROW-B-EXTRACTION-ON-NIGHTS-4-AND-5-NEEDS-THREE-SETTLED-POINTS-BEFORE-THE-FIRST-VALUE.
Protocol: README.md beside this file, written and saved BEFORE this script was run for the
first time.  Launch is Mike's word; this file is written unrun.

WHAT THIS SCRIPT DOES NOT DO: it never trains, never writes into
`connectome-seed-data/results/flow/*`, and never calls `solver.checkpoint()` or
`solver.test(track_loss=True)`.  The solver lives in a scratch datamate root; the run
directories are read with `torch.load` and `h5py` only.  The recording hook returns the state
object it was given, unchanged, and asserts that it did.

WHAT IS REUSED, VERBATIM, AND FROM WHERE (nothing about the evaluation path is re-invented):
  * `results/night2/diagnostics/diag1_eval_paths.py` -- `build_solver` (which also fixes the
    determinism settings: `run_individual.py:284-286` with `--no-determinism`, the flag every
    night wave ran under), `load_checkpoint`, `per_item_eval`, `hook_eval`, `val_item_names`.
  * `results/night2/diagnostics/ablation/ablation.py` -- `node_type_array` (the type axis,
    taken exactly as row A takes it), `spearman`, `pearson`, `rankdata`.
  * `results/night2/diagnostics/rowB/rowB.py` -- `Recorder` (subclassed, see `RecorderB`),
    `snapshot_state`, `invariants` (the seven `eval_rung` invariants of
    `tools/night/run_individual.py:624-632`), `NoDupDict`, `script_sha256`.

WHAT IS NEW HERE, and why (each is a difference from the night-2/3 row B, stated before the
first run):
  N1  the run list is keyed by NETDIR, not by label.  Night 5 lives under ensemble 9992,
      which `diag1_eval_paths.FLOW_DIR` (hard-wired to 9991) cannot address; `chkpt_table` is
      therefore re-expressed as `chkpt_table_netdir(netdir)` -- the same two h5 reads and the
      same off-by-one, parameterised by directory.
  N2  the hook detaches before any reduction (Ark: `recording_detached`) and reduces ON THE
      DEVICE the activity already lives on; only the reduced per-type vectors (65) and the
      central-cell vector (65) are moved to CPU, in `_flush`, not per Euler step.  A float64
      index_add_ on the GPU may sum in a different order than the same reduction on the CPU,
      so the last bits can differ; the outputs written before 2026-09-20 21:00 (the
      three-checkpoint run in this directory) were reduced on the CPU.
  N3  the central cell of each type is recorded beside the all-nodes mean, because the
      penalty reads one central cell per type and discards the first quarter of the frames
      (`flyvis/solver.py:869-872`) while the ablation silences all nodes of a type
      (`ablation.py:90-98`, `:106`).  Two instruments under one name; both are written.
  N4  the free falsifier: the activity penalty's own pre-weight quantity, recomputed per
      checkpoint from the central cells with the run's own resolved baseline and weights.
  N5  P1/P2 are reformulated for a passive recording (P1', P2'), and P2's thresholds are left
      null until a floor exists.  A threshold is never derived from the data it judges.

AMENDMENTS OF 2026-09-20, after the first three-checkpoint run of this script and the review
it drew (Johnny, Ark, Zcode).  Each says what prompted it.  NONE of them touches the
registered P1' tolerance: 1e-6 stays exactly as it was registered, and the FAIL verdicts the
first run produced under it stand.  Training flags are not touched anywhere in this file.

  A1  SCOPE: ten runs, not four.  Prompted by the owner ("10"): nights 4 and 5 are four runs
      but the substrate has ten complete runs across nights 1-5, and a preview taken on four
      of them is a preview of the nights, not of the substrate.  `--night all10` resolves all
      ten from the committed results/night5/run_columns.csv, keyed by netdir, and REFUSES
      (exit 3) on any run whose chkpts directory does not hold exactly 72 checkpoints or whose
      netdir label is ambiguous on disk -- `9991/002_killed_by_reboot` sits beside `9991/002`
      and must never be picked by a prefix.  N IS COUNTED IN INDIVIDUALS, NOT RUNS: the ten
      runs are six seeds, so every record carries `individual` and `replicate_of` and the plan
      prints `n_individuals` beside `n_runs`.

  A2  LOSS-LEVEL FLOOR.  Prompted by Johnny, confirmed by Ark and Zcode: P1' is registered ON
      THE LOSS (README Sec 5), but the no-hook-vs-no-hook floor was recorded only for the
      per-item maximum -- the judged level had a criterion and no floor, the unjudged level had
      a floor and no criterion.  `abs_diff_loss_nohook_vs_nohook` is now recorded beside
      `abs_diff`, at the same level the verdict is taken at.

  A3  THE FLOOR IS NO LONGER A SAMPLE OF SIZE ONE.  Prompted by Ark: two evaluations give one
      difference, and one difference is not a bound.  `--floor-k K` (default 1, so the old
      behaviour is reproducible byte for byte) evaluates the same state with no hook K+1 times
      and records ALL K differences at BOTH levels plus their maxima.  The hook difference is
      compared against the maximum of the K in `descriptive_hook_diff_le_max_floor`, which
      carries `registered: false` and is DESCRIPTIVE ONLY -- it does not replace, soften or
      override the P1' pass/fail, which is still the registered 1e-6 on the loss.

  A4  DETERMINISTIC DIAGNOSTIC MODE.  Prompted by Ark; Zcode verified that
      `torch.use_deterministic_algorithms` is called nowhere in flyvis or in these scripts, and
      only at tools/night/run_individual.py:295, in the else-branch that `--no-determinism`
      never takes.  `--deterministic` sets `torch.use_deterministic_algorithms(True)`,
      `cudnn.deterministic = True`, `cudnn.benchmark = False` before any CUDA work (and
      re-applies the two cudnn flags after `build_solver`, which deliberately sets them to the
      --no-determinism values, diag1_eval_paths.py:90-93).  It writes `deterministic` into
      every record, the controls file and the h5 attrs, and writes ALL outputs under `_det`
      names so that the two instruments can never be mixed in one file.  If PyTorch refuses an
      operator, the script writes a small json naming the operator and the innermost
      flyvis/project frame of the traceback and exits 4: THAT OUTCOME IS A FINDING, NOT A
      CRASH.  The recording hook's own reduction uses `index_add_`, which is on PyTorch's
      nondeterministic list on CUDA, so A5 exists to test the forward without it.

  A5  `--reduce-on cpu|gpu` (default gpu, the owner's GPU-first instruction).  If `index_add_`
      is the operator that refuses under A4, the reduction can be moved off the GPU while the
      forward stays deterministic.  `reduction_device` already existed; `reduction_path`
      ("gpu"/"cpu") is now written into every record, csv header, controls file and h5 attrs.

  A6  THE P2' MULTIPLIER IS DECLARED BEFORE THE FLOOR EXISTS (Ark).  `P2_FLOOR_MULTIPLIER = 10`
      and the rule "threshold = 10 x the measured floor, same path, same mode" are constants in
      this file, declared 2026-09-20, before any floor has been measured.  `--floor-summarize`
      applies the rule and records its text and date; it computes, it does not judge.

AMENDMENTS OF 2026-09-20 (second round), after Ark's reading of rowB_floor_det.json, confirmed
by CC.  These fix how `--floor-summarize` computes and labels, not what it measures; the
outputs any earlier run of this script wrote keep their own `script_sha256` and were written by
the earlier revision -- see README.md for which files that applies to.

  B1  THE SIGMA GUARD.  `M.std(axis=0, ddof=1)` over three BITWISE-IDENTICAL float64 rows can
      return ~2e-15 instead of exactly 0 -- numpy's mean of identical values is not always
      exactly that value, so the variance computed from it is not always exactly zero either.
      `--floor-summarize` now guards both `sigma_by_type` and `max_sigma_by_type`: where the
      range (max - min) across the three processes is exactly 0 for a type, sigma for that type
      is written as exactly `0.0`, not numpy's rounding residue.

  B2  `floor_k` IN THE SUMMARY MEANT NOTHING.  Inside one process, `floor_k` is the number of
      no-hook floor repeats (K) -- a real setting of that run.  In `rowB_floor[_det].json` it
      was `service_fields()`'s `RUNTIME["floor_k"]`, i.e. `--floor-summarize`'s own (unused)
      default, disconnected from the K the three summarized processes actually ran under.  The
      summary now reads `floor_k_inside_each_process` FROM the three per-process record files
      and refuses (exit 3) if they disagree; the misleading top-level `floor_k` is dropped from
      the summary's output.

  B3  INSTRUMENT LABELS.  The provenance block written into every record and controls file now
      carries `cuda_runtime_version` (`torch.version.cuda`) and `driver_version` (read via
      `torch.cuda` where available, else parsed from `nvidia-smi --query-gpu=driver_version
      --format=csv,noheader`; "unavailable" if neither works -- this never fails the run).
      Reason: the `--deterministic` promise "recomputes to the bit" holds only for the same
      driver/library stack, and that stack was not being written down.

  B4  P2' THRESHOLD MODE, INLINE.  `--floor-summarize` now writes `reduction_path` and
      `deterministic` inside EACH threshold object of `p2prime_thresholds`, beside the number,
      not only in the file's header -- the mode is part of the threshold.
"""

import os
import sys

# Same two environment variables, set the same way and in the same place as
# tools/night/run_individual.py:46-49, diag1_eval_paths.py:30-33 and ablation.py:22-25.
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
os.environ.setdefault(
    "FLYVIS_ROOT_DIR", "C:/Users/mikha/Documents/dpc-research/connectome-seed-data"
)

import argparse
import hashlib
import importlib.util
import json
import subprocess
import time
from pathlib import Path

import h5py
import numpy as np
import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]                                    # <repo>/results/night5/diagnostics/rowB
N2_DIAG = REPO / "results" / "night2" / "diagnostics"
ROWA_CENSUS = N2_DIAG / "ablation" / "ablation_controls.json"
ROWA_CENSUS_WITNESS = REPO / "results" / "night3" / "diagnostics" / "ablation" / "ablation_controls.json"
RUN_COLUMNS = REPO / "results" / "night5" / "run_columns.csv"
WAVE4 = REPO / "results" / "night4" / "wave_night4.json"
WAVE5 = REPO / "tools" / "night" / "wave_night5.json"     # gitignored; used only as a witness
FLOW = Path(os.environ["FLYVIS_ROOT_DIR"]) / "results" / "flow"

STATUS = "unregistered_diagnostic"
P0_TOL = 1e-3          # the tolerance the ablation README uses (ablation/README.md Sec 5, P0)
P1_TOL = 1e-6          # Ark's field list: bitwise, or within 1e-6.  REGISTERED; NOT AMENDED.
T_PRE = 0.25           # diag1_eval_paths.per_item_eval default; the rung hook's value

# A6: declared 2026-09-20, BEFORE any floor for this metric exists.  A computation, not a
# judgement: --floor-summarize multiplies the measured floor by this and writes the product.
P2_FLOOR_MULTIPLIER = 10
P2_THRESHOLD_RULE = ("threshold for P2' = %d x the measured floor of README Sec 6, taken on "
                     "the SAME reduction path and the SAME determinism mode as the statistic "
                     "it judges. A computation, not a judgement." % P2_FLOOR_MULTIPLIER)
P2_THRESHOLD_RULE_DECLARED = "2026-09-20"

# A1: the ten complete runs.  Written here so that a run silently added to or dropped from
# run_columns.csv is a refusal rather than a different N.  The mapping itself is still READ
# from the csv; this list is only the count and the identity check.
TEN_RUN_IDS = ("9991/000", "9991/900", "9991/001", "9991/002", "9991/003",
               "9991/903", "9991/004", "9991/005", "9992/000", "9992/003")
CHKPTS_PER_COMPLETE_RUN = 72

# Set once in main() from the parsed arguments; read by service_fields() so that every writer
# stamps the same mode without threading three more parameters through every call site.
RUNTIME = {"deterministic": False, "reduction_path": "gpu", "floor_k": 1}

sys.path.insert(0, str(N2_DIAG))
sys.path.insert(0, str(N2_DIAG / "ablation"))


# ---------------------------------------------------------------- lazy imports
def _load_night2_rowB():
    """Import results/night2/diagnostics/rowB/rowB.py under a NON-colliding module name.

    `import rowB` from this file would import this file (sys.path[0] is this directory), so
    the night-2 measurement is loaded by explicit path as `rowB_night2`.
    """
    path = N2_DIAG / "rowB" / "rowB.py"
    spec = importlib.util.spec_from_file_location("rowB_night2", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["rowB_night2"] = mod
    spec.loader.exec_module(mod)
    return mod


def _gpu_imports(deterministic=False):
    """Everything that pulls torch / flyvis in.  Never called by --dry-run.

    A4: the determinism switches are thrown HERE -- after `import torch`, which allocates
    nothing on the device, and before any project module that can touch CUDA is imported.
    `CUBLAS_WORKSPACE_CONFIG=:4096:8` is already in the environment (set at the top of this
    file, before any import, exactly as run_individual.py:46-49 sets it), which is the
    precondition `torch.use_deterministic_algorithms(True)` needs for cuBLAS.
    """
    import torch  # noqa: F401
    det = apply_determinism(torch, deterministic, "before_any_cuda_work")
    import diag1_eval_paths as D
    import ablation as ABL
    RB = _load_night2_rowB()
    return torch, D, ABL, RB, det


def apply_determinism(torch, deterministic, when):
    """A4.  Returns what was actually set, so the record states the machine's answer.

    `torch.use_deterministic_algorithms(True)` is called WITHOUT `warn_only`: a refused
    operator must raise, be caught at top level and be written down as a finding (exit 4).
    run_individual.py:295 uses `warn_only=True` for training; this diagnostic wants the
    refusal, not a warning, because the refusal is the information.

    NOTHING about training is touched: this function is only ever called from this script's
    own process, and the only global state it writes is the three torch switches below.
    """
    rec = {"requested": bool(deterministic), "when": when,
           "CUBLAS_WORKSPACE_CONFIG": os.environ.get("CUBLAS_WORKSPACE_CONFIG")}
    if deterministic:
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        torch.use_deterministic_algorithms(True)
        rec["use_deterministic_algorithms"] = True
        rec["warn_only"] = False
    else:
        rec["use_deterministic_algorithms"] = False
        rec["note"] = ("not set -- the nights ran under --no-determinism and this is the "
                       "instrument that mirrors them")
    rec["cudnn_deterministic"] = bool(torch.backends.cudnn.deterministic)
    rec["cudnn_benchmark"] = bool(torch.backends.cudnn.benchmark)
    return rec


def gpu_instrument_labels(torch):
    """B3 (2026-09-20, Ark / CC): the CUDA runtime and driver version behind this run.

    The `--deterministic` promise "recomputes to the bit" holds only for the same
    driver/library stack; without these two fields a later re-run on a moved stack could look
    like a disagreement in the hook when it is really a disagreement in the substrate under it.

    `cuda_runtime_version` is `torch.version.cuda`.  `driver_version` is read via `torch.cuda`
    when it exposes one; otherwise by parsing `nvidia-smi --query-gpu=driver_version
    --format=csv,noheader`.  NEVER fails the run: any error here is swallowed and the field is
    written as the string "unavailable", not raised.
    """
    cuda_runtime = getattr(getattr(torch, "version", None), "cuda", None) or "unavailable"
    driver, source = "unavailable", "unavailable"
    try:
        if torch.cuda.is_available():
            v = getattr(torch.cuda, "driver_version", None)
            v = v() if callable(v) else v
            if v:
                driver, source = str(v), "torch.cuda"
    except Exception:  # noqa: BLE001 -- never fail the run over a label
        pass
    if driver == "unavailable":
        try:
            out = subprocess.run(
                ["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"],
                capture_output=True, text=True, timeout=10)
            v = out.stdout.strip().splitlines()[0].strip() if out.stdout.strip() else ""
            if out.returncode == 0 and v:
                driver = v
                source = "nvidia-smi --query-gpu=driver_version --format=csv,noheader"
        except Exception:  # noqa: BLE001 -- never fail the run over a label
            pass
    return {"cuda_runtime_version": cuda_runtime, "driver_version": driver,
            "driver_version_source": source}


# ---------------------------------------------------------------- small helpers
def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def sha256_obj(obj):
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def git_head():
    try:
        return subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"],
                              capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception as e:  # noqa: BLE001
        return f"unavailable: {e!r}"


class Refusal(SystemExit):
    """Non-zero exit with a stated reason.  Used for the axis check (Ark's hard refusal)."""

    def __init__(self, msg):
        print("REFUSE " + msg, flush=True)
        super().__init__(3)


def out_name(a, stem, ext):
    """Output file name, with the `_det` suffix of A4 applied to EVERY writer.

    The deterministic and the non-deterministic instrument must never write into one file:
    a records file that holds both is a file nobody can later split.  The suffix is derived
    from the flag, in one place, so no writer can forget it.
    """
    return f"{stem}{'_det' if a.deterministic else ''}.{ext}"


class NondeterministicOperator(SystemExit):
    """A4: PyTorch refused an operator under --deterministic.  A FINDING, not a crash.

    Exit code 4, distinct from the refusals (3), because it says something about the
    substrate -- which operator in this forward has no deterministic CUDA implementation --
    rather than about this script's inputs.  The operator name and the innermost flyvis /
    project frame are written to a json so the finding survives the terminal.
    """

    def __init__(self, path, payload):
        print("NONDETERMINISTIC_OPERATOR " + json.dumps(
            {k: payload[k] for k in ("operator", "innermost_frame")}), flush=True)
        print(f"WROTE {path}", flush=True)
        super().__init__(4)


def nondeterministic_finding(exc, a):
    """Name the operator and the innermost flyvis/project frame of a determinism refusal."""
    import traceback
    msg = str(exc)
    marker = "does not have a deterministic implementation"
    op = None
    if marker in msg:
        head = msg.split(marker)[0].strip()
        op = head.split()[-1].strip("'\"`,") if head.split() else None
    frames = traceback.extract_tb(exc.__traceback__)
    innermost, ours = None, None
    for fr in frames:                      # outermost -> innermost; keep the last match
        f = fr.filename.replace("\\", "/")
        innermost = f"{fr.filename}:{fr.lineno} in {fr.name}"
        if "/flyvis" in f or str(REPO).replace("\\", "/") in f:
            ours = f"{fr.filename}:{fr.lineno} in {fr.name}"
    return {
        "finding": "an operator on this forward has no deterministic implementation",
        "status": STATUS,
        "readable_as_verdict": False,
        "exit_code": 4,
        "deterministic": True,
        "reduction_path": a.reduce_on,
        "operator": op,
        "innermost_frame": ours or innermost,
        "innermost_frame_any": innermost,
        "innermost_frame_source": "the last traceback frame whose file is under flyvis or "
                                  "under this repository; the raw innermost frame is beside it",
        "message": msg,
        "traceback": traceback.format_exception(type(exc), exc, exc.__traceback__),
        "what_to_do": "if the operator is index_add_ (the recording hook's own reduction, on "
                      "PyTorch's nondeterministic CUDA list), re-run with --reduce-on cpu: the "
                      "forward is then tested deterministically with the reduction off the GPU",
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


# ---------------------------------------------------------------- the run registry
def read_run_columns():
    """results/night5/run_columns.csv -- the committed, EXPLICIT run -> column mapping.

    Its own header says why it exists: "Do not derive this from column names: the prime marks
    count marks, not order".  Night 5's launcher record (tools/night/wave_night5.json) is
    gitignored (.gitignore: `tools/night/*.json`), so this csv -- not a wave json -- is the
    committed source of the run list.  wave_night4.json and, when present, wave_night5.json
    are read as witnesses and any disagreement is a refusal.
    """
    lines = [ln for ln in RUN_COLUMNS.read_text(encoding="utf-8").splitlines()
             if ln.strip() and not ln.lstrip().lstrip('"').startswith("#")]
    hdr = lines[0].split(",")
    rows = [dict(zip(hdr, ln.split(","))) for ln in lines[1:]]
    reg = {}
    for r in rows:
        rid = r["run_id"]
        if rid in reg:
            raise Refusal(f"duplicate run_id {rid!r} in {RUN_COLUMNS}")
        reg[rid] = {
            "run_id": rid,
            "netdir": str(FLOW / rid),
            "run_label": r["column"].replace("val_loss_", ""),
            "seed": int(r["seed"]),
            "role": r["role"],
            "run_index_for_seed": int(r["run_index_for_seed"]),
            "night": int(r["night"]),
            "boot_session": r["boot_session"],
        }
    # twin_of: every other run of the same seed, canonical first.  Ark's field is singular;
    # a list is written because seed 3 has three runs and "the twin" is ambiguous for it.
    #
    # A1: `individual` and `replicate_of` are written beside them so that N is counted in
    # INDIVIDUALS and not in runs.  Ten runs are six seeds; a replicate is the same individual
    # measured again, and it does not enter N.  `is_individual_representative` marks the one
    # run per seed (the canonical, run_index_for_seed == 1) that stands for the individual.
    for rid, e in reg.items():
        sibs = [o for o in reg.values() if o["seed"] == e["seed"] and o["run_id"] != rid]
        sibs.sort(key=lambda o: o["run_index_for_seed"])
        e["twin_of"] = [o["run_id"] for o in sibs]
        can = [o["run_id"] for o in sibs if o["run_index_for_seed"] == 1]
        e["twin_of_canonical"] = can[0] if can else None
        e["individual"] = int(e["seed"])
        e["individual_label"] = f"seed{e['seed']}"
        own = [o["run_id"] for o in reg.values()
               if o["seed"] == e["seed"] and o["run_index_for_seed"] == 1]
        e["replicate_of"] = (own[0] if own and own[0] != rid else None) \
            if e["role"] == "replicate" else None
        e["is_individual_representative"] = bool(e["run_index_for_seed"] == 1)
        e["n_runs_of_this_individual"] = len(sibs) + 1
    return reg


def individuals_of(runs):
    """The N that may be quoted for a set of runs: distinct individuals, replicates folded in."""
    seeds = sorted({int(e["seed"]) for e in runs})
    return {
        "n_runs": len(runs),
        "n_individuals": len(seeds),
        "individuals": seeds,
        "n_replicate_runs": sum(1 for e in runs if e["role"] == "replicate"),
        "runs_per_individual": {str(s): sorted(e["run_id"] for e in runs
                                               if int(e["seed"]) == s) for s in seeds},
        "N_is_counted_in": "individuals; replicate runs of the same seed do NOT enter N",
    }


def cross_check_waves(reg):
    """Witness the registry against the launcher records that are on disk."""
    seen = {}
    for w in (WAVE4, WAVE5):
        if not w.exists():
            seen[str(w)] = "absent (gitignored or on another node) -- not used"
            continue
        d = json.loads(w.read_text(encoding="utf-8"))
        jobs = {j["id"]: int(j["seed"]) for j in d["jobs"]}
        for rid, s in jobs.items():
            if rid in reg and reg[rid]["seed"] != s:
                raise Refusal(f"{w}: seed {s} for {rid} disagrees with "
                              f"run_columns.csv seed {reg[rid]['seed']}")
        seen[str(w)] = {"tag": d.get("tag"), "jobs": jobs}
    return seen


def select_runs(reg, nights, netdirs):
    if netdirs:
        by_dir = {str(Path(e["netdir"])).replace("\\", "/"): e for e in reg.values()}
        by_id = {e["run_id"]: e for e in reg.values()}
        out = []
        for n in netdirs:
            k = str(Path(n)).replace("\\", "/")
            e = by_dir.get(k) or by_id.get(n) or by_id.get(k)
            if e is None:
                raise Refusal(f"--netdir {n!r} is not in {RUN_COLUMNS.name}")
            out.append(e)
        return out
    if nights == "all10":
        return select_ten(reg)
    want = {4, 5} if nights == "all" else {int(nights)}
    return [e for e in sorted(reg.values(), key=lambda x: (x["night"], x["run_id"]))
            if e["night"] in want]


def select_ten(reg):
    """A1: the ten complete runs of nights 1-5, in the order run_columns.csv lists them.

    Two refusals, both exit 3, both BEFORE any checkpoint is opened:
      * the csv's run set must be exactly TEN_RUN_IDS -- a run added or dropped changes N and
        must be a stop, not a different answer;
      * every selected netdir must be UNAMBIGUOUS on disk (see check_netdir_unambiguous).
    The 72-checkpoint requirement is enforced in check_run_complete, which needs the run
    directory's own chkpt tables and so runs once per run in both --dry-run and the real run.
    """
    have = set(reg)
    want = set(TEN_RUN_IDS)
    if have != want:
        raise Refusal(f"{RUN_COLUMNS.name} lists {sorted(have)}; the ten complete runs are "
                      f"{sorted(want)}; missing {sorted(want - have)}, "
                      f"unexpected {sorted(have - want)}")
    runs = [reg[rid] for rid in TEN_RUN_IDS]
    for e in runs:
        check_netdir_unambiguous(e)
    return runs


def check_netdir_unambiguous(e):
    """A run label must name exactly one directory on disk, by equality and never by prefix.

    `9991/002_killed_by_reboot` sits beside `9991/002` and holds a partial run.  Siblings that
    start with the label are listed as rejected candidates with their checkpoint counts; the
    label is a refusal only when it no longer picks one run -- the exact directory is missing,
    or a prefix sibling is complete too.
    """
    d = Path(e["netdir"])
    leaf = e["run_id"].split("/")[-1]
    if d.name != leaf:
        raise Refusal(f"{e['run_id']}: resolved netdir {d} does not end in {leaf!r}")
    if not d.is_dir():
        raise Refusal(f"{e['run_id']}: {d} is not a directory on disk")
    sibs = []
    for p in sorted(d.parent.iterdir()):
        if not p.is_dir() or p.name == leaf or not p.name.startswith(leaf):
            continue
        n = len(list((p / "chkpts").glob("chkpt_*"))) if (p / "chkpts").is_dir() else 0
        sibs.append({"name": p.name, "n_checkpoint_files": n, "picked": False,
                     "why_not": "its name is not equal to the run label; resolution is by "
                                "equality against run_columns.csv, never by prefix"})
    complete = [s["name"] for s in sibs if s["n_checkpoint_files"] >= CHKPTS_PER_COMPLETE_RUN]
    if complete:
        raise Refusal(f"{e['run_id']}: the label {leaf!r} is ambiguous under {d.parent} -- "
                      f"{complete} start with it and also hold >= "
                      f"{CHKPTS_PER_COMPLETE_RUN} checkpoints, so the label no longer names "
                      f"one run; this scope refuses rather than choose")
    return {"netdir": str(d), "leaf": leaf, "resolution": "exact directory-name equality",
            "rejected_prefix_siblings": sibs}


def check_run_complete(e, tab):
    """A1: a run in the ten-run scope holds exactly 72 checkpoints, or the script refuses."""
    on_disk = sorted((Path(e["netdir"]) / "chkpts").glob("chkpt_*"))
    if len(tab) != CHKPTS_PER_COMPLETE_RUN or len(on_disk) != CHKPTS_PER_COMPLETE_RUN:
        raise Refusal(
            f"{e['run_id']}: {len(tab)} entries in chkpt_index.h5 and {len(on_disk)} files in "
            f"{Path(e['netdir']) / 'chkpts'}; a complete run has exactly "
            f"{CHKPTS_PER_COMPLETE_RUN}. An incomplete run is not a tenth of this scope.")
    return len(on_disk)


# ---------------------------------------------------------------- run-dir facts, from disk
def chkpt_table_netdir(netdir):
    """[(chkpt_index, chkpt_iter, solver_iteration, path)] for one run directory.

    diag1_eval_paths.chkpt_table:62-77, re-expressed for an arbitrary netdir (N1) -- night 5
    is ensemble 9992 and that function is hard-wired to 9991.  The off-by-one is that
    function's and is kept verbatim: flyvis writes `chkpt_iter` as `self.iteration - 1`
    (flyvis/solver.py:463) and stores `"iteration": self.iteration - 1` inside the checkpoint
    (solver.py:453), while run_individual.py records `int(solver.iteration)` in the committed
    night_report_checkpoints.csv.  So solver_iteration == chkpt_iter + 1.  `chkpt_iter` below
    is READ from chkpt_iter.h5, never derived from the index.
    """
    d = Path(netdir)
    with h5py.File(d / "chkpt_index.h5", "r") as f:
        idx = [int(x) for x in f["data"][()]]
    with h5py.File(d / "chkpt_iter.h5", "r") as f:
        its = [int(x) for x in f["data"][()]]
    if len(idx) != len(its):
        raise Refusal(f"{d}: chkpt_index.h5 has {len(idx)} entries, chkpt_iter.h5 {len(its)}")
    return [(i, it, it + 1, d / "chkpts" / f"chkpt_{i:05}") for i, it in zip(idx, its)]


def announce_activity_h5(netdir):
    """The FIRST thing printed for any activity.h5 this script touches: shape and dtype.

    Ark's point (the backlog entry's own words): size is not an instrument.  No value from
    this file is ever read, printed or recorded -- only its shape and dtype, so that anyone
    reading the log can see that the 250,008-long per-iteration mean is a different object
    from the 65-per-checkpoint axis this script builds.
    """
    p = Path(netdir) / "activity.h5"
    if not p.exists():
        print(f"ACTIVITY_H5 {p} absent", flush=True)
        return {"path": str(p), "present": False}
    with h5py.File(p, "r") as f:
        ds = f["data"]
        rec = {"path": str(p), "present": True, "shape": list(ds.shape), "dtype": str(ds.dtype),
               "keys": sorted(f.keys())}
    print(f"ACTIVITY_H5 {p} shape={tuple(rec['shape'])} dtype={rec['dtype']} "
          f"(shape and dtype only; no value is read)", flush=True)
    return rec


def run_meta(netdir):
    """The run's OWN resolved config, from its _meta.yaml -- not the default solver.yaml."""
    m = yaml.safe_load((Path(netdir) / "_meta.yaml").read_text(encoding="utf-8"))
    cfg = m["config"]
    ap = cfg["penalizer"]["activity_penalty"]
    return {
        "network_name": cfg["network_name"],
        "description": cfg.get("description"),
        "status": m.get("status"),
        "connectome": cfg["network"]["connectome"],
        "dt_config": float(cfg["task"]["dataset"]["dt"]),
        "n_frames_config": int(cfg["task"]["dataset"]["n_frames"]),
        "n_iters": int(cfg["task"]["n_iters"]),
        "activity_penalty": {
            "activity_penalty": float(ap["activity_penalty"]),
            "activity_baseline": float(ap["activity_baseline"]),
            "stop_iter": int(ap["stop_iter"]),
            "below_baseline_penalty_weight": float(ap["below_baseline_penalty_weight"]),
            "above_baseline_penalty_weight": float(ap["above_baseline_penalty_weight"]),
        },
    }


def side_of_stop_iter(chkpt_iter, stop_iter):
    """Which side of the activity penalty's stop_iter a checkpoint sits on.

    Computed AT WRITE TIME from the chkpt_iter read out of chkpt_iter.h5 and the run's own
    resolved stop_iter -- never from the checkpoint index, and never from a constant 150000
    written into this file.  The penalty's own condition is `iteration < stop_iter` with
    `iteration == solver.iteration` (flyvis/solver.py:815-822, called at solver.py:350 after
    the optimizer step).  Because chkpt_iter == solver_iteration - 1, BOTH readings are
    recorded and the disagreement window is exactly one iteration.
    """
    solver_it = chkpt_iter + 1
    return {
        "stop_iter": int(stop_iter),
        "chkpt_iter": int(chkpt_iter),
        "solver_iteration": int(solver_it),
        "side_by_chkpt_iter": "before" if chkpt_iter < stop_iter else "at_or_after",
        "side_by_solver_iteration": "before" if solver_it < stop_iter else "at_or_after",
        "conventions_agree": bool((chkpt_iter < stop_iter) == (solver_it < stop_iter)),
        "penalty_active_at_this_iteration": bool(solver_it < stop_iter),
    }


# ---------------------------------------------------------------- the type axis
def find_connectome_dir(conn_cfg):
    """The flyvis data directory whose stored config equals the run's connectome config.

    Resolved from disk so that --dry-run needs neither torch nor flyvis; `find_spec` locates
    the package without executing it.  The real run takes the axis from `net.connectome` and
    asserts it equals this one.
    """
    spec = importlib.util.find_spec("flyvis")
    if spec is None or not spec.origin:
        raise Refusal("flyvis is not importable; cannot locate its connectome data directory")
    base = Path(spec.origin).parent / "data" / "connectome"
    want = {k: conn_cfg[k] for k in ("type", "file", "extent", "n_syn_fill")}
    hits = []
    for d in sorted(base.iterdir()):
        meta = d / "_meta.yaml"
        if not meta.exists() or not (d / "nodes" / "type.h5").exists():
            continue
        got = yaml.safe_load(meta.read_text(encoding="utf-8")).get("config", {})
        if all(got.get(k) == v for k, v in want.items()):
            hits.append(d)
    if len(hits) != 1:
        raise Refusal(f"{len(hits)} connectome dirs under {base} match {want}; expected 1")
    return hits[0]


def axis_from_disk(cdir):
    def rd(p):
        with h5py.File(p, "r") as f:
            return f["data"][()]

    uniq = [x.decode() if isinstance(x, bytes) else str(x) for x in rd(cdir / "unique_cell_types.h5")]
    types = np.array([x.decode() if isinstance(x, bytes) else str(x)
                      for x in rd(cdir / "nodes" / "type.h5")])
    central = [int(x) for x in rd(cdir / "central_cells_index.h5")]
    return build_axis(uniq, types, central, source=str(cdir))


def build_axis(unique_types, types_arr, central_index, source):
    """The axis block.  `unique_cell_types` order is asserted equal to the order ablation.py
    takes (`list(dict.fromkeys(node_type_array(net)))`, ablation.py:164) -- Ark's field list
    names the first, row A used the second, and they are the same list; the assertion is what
    makes that a fact rather than a coincidence.
    """
    first_seen = list(dict.fromkeys(types_arr.tolist()))
    if list(unique_types) != first_seen:
        raise Refusal("connectome.unique_cell_types order differs from the first-appearance "
                      "order of nodes.type, which is the order row A's ablation.py used "
                      "(ablation.py:164); the two axes are not the same list")
    counts = [int((types_arr == t).sum()) for t in unique_types]
    if len(central_index) != len(unique_types):
        raise Refusal(f"central_cells_index has {len(central_index)} entries for "
                      f"{len(unique_types)} types")
    at_central = [types_arr[i] for i in central_index]
    if at_central != list(unique_types):
        raise Refusal("central_cells_index is not aligned with unique_cell_types order")
    rowA_fields = {"type_labels": list(unique_types), "node_count_per_type": counts,
                   "n_nodes": int(len(types_arr)), "n_types": int(len(unique_types))}
    full = dict(rowA_fields, central_cell_index_per_type=[int(i) for i in central_index])
    return {
        "source": source,
        "order": "net.connectome.unique_cell_types, asserted == "
                 "list(dict.fromkeys(nodes.type)) (ablation.py:164)",
        "type_labels": rowA_fields["type_labels"],
        "node_count_per_type": counts,
        "central_cell_index_per_type": full["central_cell_index_per_type"],
        "n_nodes": rowA_fields["n_nodes"],
        "n_types": rowA_fields["n_types"],
        "axis_sha256": sha256_obj(full),
        "axis_rowA_sha256": sha256_obj(rowA_fields),
    }


def rowA_census_fingerprint(path):
    """The row-A census, from ablation_controls.json meta (types, type_counts, n_nodes)."""
    m = json.loads(Path(path).read_text(encoding="utf-8"))["meta"]
    labels = list(m["types"])
    fields = {"type_labels": labels,
              "node_count_per_type": [int(m["type_counts"][t]) for t in labels],
              "n_nodes": int(m["n_nodes"]), "n_types": int(m["n_types"])}
    return sha256_obj(fields), fields


def check_axis_against_rowA(axis):
    """Ark's hard refusal: a differing axis is a non-zero exit, not a warning."""
    out = {"tolerance": "exact; the axis is a list of labels and integer counts, not a measurement"}
    refs = []
    for p in (ROWA_CENSUS, ROWA_CENSUS_WITNESS):
        if not Path(p).exists():
            out[str(p)] = "absent"
            continue
        fp, fields = rowA_census_fingerprint(p)
        ok = (fp == axis["axis_rowA_sha256"])
        out[str(p)] = {"axis_rowA_sha256": fp, "matches": bool(ok)}
        refs.append((p, fp, fields, ok))
    if not refs:
        raise Refusal("no ablation_controls.json census found; the axis cannot be "
                      "fingerprinted against row A's")
    for p, fp, fields, ok in refs:
        if not ok:
            diffs = [t for t, c in zip(axis["type_labels"], axis["node_count_per_type"])
                     if t not in fields["type_labels"]
                     or fields["node_count_per_type"][fields["type_labels"].index(t)] != c]
            raise Refusal(f"type axis differs from row A's census in {p}: "
                          f"ours {axis['axis_rowA_sha256']}, row A {fp}; "
                          f"first differing labels {diffs[:8]}")
    out["verdict"] = "identical to row A's census"
    return out


# ---------------------------------------------------------------- the recorder (GPU path)
def make_recorder_class(torch, RB, reduce_on="gpu"):
    class RecorderB(RB.Recorder):
        """`rowB_night2.Recorder` with N2 and N3 applied, and nothing else changed.

        The state hook is called from `Network._state_api` (flyvis/network/network.py:430-433)
        -- the same site the ablation clamps at -- at the end of `_next_state` (network.py:413)
        and at the end of `_initial_state` (network.py:375).  This hook READS the state and
        returns the same object; it asserts after the read that `state.nodes.activity` is
        still the tensor it was handed, so `activity_mutated` is measured, not claimed.

        Phases are marked by a forward pre-hook on the Network module: `per_item_eval`
        (diag1_eval_paths.py:176-201) calls `network.steady_state()` once (phase 0) and then
        `network(...)` once per item (phases 1..n_items).

        N2: the reduction runs on the activity's OWN device (the GPU, in every run so far).
        Only the two reduced 65-vectors per Euler step leave it, and they leave in `_flush`.
        A float64 `index_add_` over 45,669 nodes accumulates in a hardware-dependent order, so
        the GPU sum and the CPU sum of the same activity can differ in the last bits; that is
        accepted here and recorded, not silently absorbed.

        A5 (`--reduce-on cpu`): the detached activity is moved to the host BEFORE the
        reduction, so the forward keeps running on the GPU while `index_add_` -- which is on
        PyTorch's nondeterministic CUDA list -- runs where it has a deterministic
        implementation.  That is the slower path (one 45,669-value copy per Euler step) and it
        exists for A4, not for speed; `reduction_path` records which one produced a file.
        """

        def __init__(self, type_index, counts, n_types, central_index):
            super().__init__(type_index, counts, n_types)   # tensors arrive on CPU
            self.central_index = central_index
            self.phases_central = []
            self.cur_central = None
            self._reduce_device = None                      # set by _align_to, once

        def _align_to(self, device):
            """Put type_index / counts / central_index on `device` ONCE, not per call.

            The hook runs once per Euler step (~650 per evaluation); a `.to()` inside it would
            re-copy the 45,669-long index every step, which is the cost this change removes.
            """
            if self._reduce_device == device:
                return
            self.type_index = self.type_index.to(device)
            self.counts = self.counts.to(device)
            if torch.is_tensor(self.central_index):
                self.central_index = self.central_index.to(device)
            self._reduce_device = device

        def new_phase(self, *a, **kw):
            self._flush()
            self.phase += 1
            self.cur = ([], [])
            self.cur_central = []

        def _flush(self):
            # The per-step 65-vectors stay on the reduction device until here; this is the
            # ONE host copy per phase, of (n_steps, 65) doubles rather than of (n_steps, 45669).
            if self.cur is not None:
                self.phases.append(torch.stack(self.cur[0]).double().cpu().numpy())
                self.phases_std.append(torch.stack(self.cur[1]).double().cpu().numpy())
                self.phases_central.append(
                    torch.stack(self.cur_central).double().cpu().numpy())
            self.cur = None
            self.cur_central = None

        def finish(self):
            self._flush()
            return self.phases, self.phases_std, self.phases_central

        def hook(self, state):
            x = state.nodes.activity
            assert x.shape[0] == 1, x.shape                 # batch 1
            # N2: detach inside the hook, before any reduction -- the recording never holds
            # the autograd graph.  The reduction stays on the activity's own device (the
            # owner's instruction: what can run on the GPU runs on the GPU), so the 45,669-node
            # tensor is never copied to the host; the accumulators are created there too.
            v = x[0].detach().to(dtype=torch.float64)
            if reduce_on == "cpu":                          # A5, off by default
                v = v.cpu()
            self._align_to(v.device)                        # once per device, not per call
            s1 = torch.zeros(self.n_types, dtype=torch.float64, device=v.device)
            s2 = torch.zeros(self.n_types, dtype=torch.float64, device=v.device)
            s1.index_add_(0, self.type_index, v)
            s2.index_add_(0, self.type_index, v * v)
            mean = s1 / self.counts
            var = torch.clamp(s2 / self.counts - mean * mean, min=0.0)
            if self.cur is None:
                self.new_phase()
            self.cur[0].append(mean)
            self.cur[1].append(torch.sqrt(var))
            self.cur_central.append(v[self.central_index])   # N3
            self.n_calls += 1
            assert state.nodes.activity is x, "the recording hook wrote into the state"
            return state                                     # unchanged

    return RecorderB


def eval_with_recorder(torch, D, RB, RecorderB, solver, ctx):
    """One n-item evaluation with the recorder attached.  Mirrors rowB_night2.eval_rowB."""
    net = solver.network
    assert net._state_hooks == (), net._state_hooks
    rec = RecorderB(*ctx)
    net.register_state_hook(rec.hook)
    ph = net.register_forward_pre_hook(rec.new_phase)
    before = RB.snapshot_state(solver)
    try:
        losses = D.per_item_eval(solver, t_pre=T_PRE)
    finally:
        ph.remove()
        net.clear_state_hooks()
    after = RB.snapshot_state(solver)
    assert net._state_hooks == ()
    means, stds, centrals = rec.finish()
    return (np.array(losses["flow"], dtype=np.float64), means, stds, centrals,
            RB.invariants(before, after), rec.n_calls)


# ---------------------------------------------------------------- reductions
def reduce_phases(means, stds, centrals, n_items):
    """Phases 1..n_items -> the six recorded matrices, all (n_items, n_types).

    TWO REDUCTIONS, NAMED SEPARATELY (backlog entry, observation (b)):
      * all nodes of the type, all frames            -> `mean_by_type`   (row A's population)
      * the type's ONE central cell, frames n//4 on  -> `central_cell_mean_skip_first_quarter`
        (exactly the penalised reduction, flyvis/solver.py:869-872)
    """
    if len(means) != n_items + 1:
        raise Refusal(f"{len(means)} phases recorded, expected {n_items + 1} "
                      f"(phase 0 = the grey steady state)")
    steps = [int(m.shape[0]) for m in means[1:]]
    if len(set(steps)) != 1:
        raise Refusal(f"items do not share a simulation length: {steps}")
    n_frames = steps[0]
    q = n_frames // 4                                   # solver.py:869, `n_frames // 4 :`
    M = [m for m in means[1:]]
    S = [s for s in stds[1:]]
    C = [c for c in centrals[1:]]
    return {
        "n_frames": n_frames,
        "skip_first_quarter_from_frame": q,
        "steps_steady_state": int(means[0].shape[0]),
        "mean_by_type": np.stack([m.mean(axis=0) for m in M]),
        "std_by_type": np.stack([s.mean(axis=0) for s in S]),
        "last_frame_by_type": np.stack([m[-1] for m in M]),
        "central_cell_mean": np.stack([c.mean(axis=0) for c in C]),
        "mean_by_type_skip_first_quarter": np.stack([m[q:].mean(axis=0) for m in M]),
        "central_cell_mean_skip_first_quarter": np.stack([c[q:].mean(axis=0) for c in C]),
        "steps_by_type": np.stack([m.T for m in M]),          # (item, type, frame)
        "steps_central": np.stack([c.T for c in C]),          # (item, type, frame)
    }


def penalised_quantity(central_skip, ap):
    """The activity penalty's PRE-WEIGHT quantity, recomputed exactly as solver.py computes it.

    flyvis/solver.py:868-883:
        activity_mean = activity[:, n_frames // 4 :, self.central_cells_index].mean(dim=1)
        penalty = self.activity_penalty * (asymmetric_weighting(
            self.activity_baseline - activity_mean,
            self.below_baseline_penalty_weight,
            self.above_baseline_penalty_weight) ** 2).mean()
    and asymmetric_weighting (flyvis/utils/tensor_utils.py:443-461) is
        f(x) = gamma * relu(x) - delta * relu(-x).
    Every constant comes from the run's own resolved config (`run_meta`); none is written into
    this file.  `pre_weight` is the `(...)**2).mean()`; `weighted` multiplies by
    activity_penalty.

    ONE DIFFERENCE FROM THE TRAINING-TIME QUANTITY, stated and not hidden: in training the
    tensor is the TRAINING batch's activity (n_samples == task.batch_size == 4, augmentation
    on, solver.py:350); here it is the held-out items, n_samples == n_items, batch 1,
    augmentation off.  The reduction is identical; the stimulus population is not.
    """
    x = ap["activity_baseline"] - central_skip
    w = (ap["below_baseline_penalty_weight"] * np.maximum(x, 0.0)
         - ap["above_baseline_penalty_weight"] * np.maximum(-x, 0.0))
    pre = float((w ** 2).mean())
    below = central_skip < ap["activity_baseline"]
    above = central_skip > ap["activity_baseline"]
    item_mean = central_skip.mean(axis=0)
    return {
        "formula": "(asymmetric_weighting(baseline - central_cell_mean_skip_first_quarter, "
                   "below_w, above_w) ** 2).mean()  [flyvis/solver.py:868-883]",
        "constants_source": "the run's own _meta.yaml config.penalizer.activity_penalty",
        "constants": dict(ap),
        "n_samples_here": int(central_skip.shape[0]),
        "n_samples_in_training": "task.batch_size (4), augmented -- a different population",
        "pre_weight": repr(pre),
        "weighted": repr(ap["activity_penalty"] * pre),
        "n_central_below_baseline": int(below.sum()),
        "n_central_above_baseline": int(above.sum()),
        "n_central_at_baseline": int((central_skip == ap["activity_baseline"]).sum()),
        "n_cells_total": int(central_skip.size),
        "n_types_below_baseline_on_the_item_mean": int((item_mean < ap["activity_baseline"]).sum()),
        "n_types_above_baseline_on_the_item_mean": int((item_mean > ap["activity_baseline"]).sum()),
        "n_types_below_in_all_items": int(below.all(axis=0).sum()),
        "n_types_above_in_all_items": int(above.all(axis=0).sum()),
    }


def floor_block(plains):
    """A3: the no-hook-vs-no-hook floor from K+1 evaluations of the SAME state.

    `plains[0]` is P0's reading; each of the other K is differenced against it, at BOTH
    levels -- the per-item maximum and the loss, the level P1' is registered on (A2).  ALL K
    differences are written, not only their maximum, because a maximum over K hides whether
    the K agreed; and the maximum is written beside them because that is what the descriptive
    comparison in `controls_block` uses.
    """
    k = len(plains) - 1
    per_item = [float(np.max(np.abs(p - plains[0]))) for p in plains[1:]]
    loss = [abs(float(p.mean()) - float(plains[0].mean())) for p in plains[1:]]
    return {
        "k": k,
        "n_no_hook_evaluations": len(plains),
        "what": "the same state, the same code path, no hook at all, evaluated K+1 times in "
                "ONE process; each repeat differenced against the first (P0's reading)",
        "registered": False,
        "differences_per_item_max": [repr(x) for x in per_item],
        "differences_loss": [repr(x) for x in loss],
        "max_difference_per_item_max": repr(max(per_item)) if per_item else None,
        "max_difference_loss": repr(max(loss)) if loss else None,
        "all_bitwise_identical": bool(all(np.array_equal(p, plains[0]) for p in plains[1:])),
        "note": "a within-process floor. The across-process floor of README Sec 6 is a "
                "different and larger quantity and is measured by --floor-repeat.",
    }


def controls_block(red, li, plains, hook_val, stored_val, input_type_idx):
    """P0, P1', P2' -- Ark's three, reformulated for a passive recording."""
    plain = plains[0]
    fl = floor_block(plains)
    p0 = float(plain.mean())
    p1 = float(li.mean())
    d1 = abs(p1 - p0)
    d1_item = float(np.max(np.abs(li - plain)))
    V = red["mean_by_type"]                                   # (n_items, n_types)
    inp = V[:, input_type_idx]                                # (n_items, n_input_types)
    pair = [float(np.max(np.abs(inp[i] - inp[j])))
            for i in range(inp.shape[0]) for j in range(i + 1, inp.shape[0])]
    agg = V.mean(axis=0)
    return {
        "P0_evaluation_without_recording_reproduces_the_stored_value": {
            "what": "the same evaluation with NO hook registered, against the val_loss stored "
                    "inside the checkpoint file",
            "tolerance": P0_TOL,
            "tolerance_source": "results/night2/diagnostics/ablation/README.md Sec 5 (P0)",
            "stored_checkpoint_val_loss": repr(stored_val),
            "per_item_mean_without_hook": repr(p0),
            "rung_hook_path_value": repr(hook_val),
            "abs_diff_per_item_mean_minus_stored": repr(abs(p0 - stored_val)),
            "abs_diff_hook_path_minus_stored": repr(abs(hook_val - stored_val)),
            "pass": bool(abs(p0 - stored_val) < P0_TOL),
        },
        "P1prime_the_recording_hook_does_not_change_the_loss": {
            "what": "the loss with the recording hook registered, against P0. The criterion is "
                    "ON THE LOSS -- the aggregate the rung reports -- and the per-item figures "
                    "are recorded beside it, at their own separately named level.",
            "tolerance": P1_TOL,
            "tolerance_status": "REGISTERED and NOT amended on 2026-09-20; the verdicts it "
                                "produced on the first run stand",
            "per_item_mean_with_recorder": repr(p1),
            # --- the judged level: the loss ---
            "abs_diff": repr(d1),
            "abs_diff_level": "loss (the per-item mean); this is the level `pass` is taken at",
            "abs_diff_loss_nohook_vs_nohook": fl["max_difference_loss"],   # A2
            "abs_diff_loss_nohook_vs_nohook_what":
                "the floor AT THE JUDGED LEVEL: the largest loss-level difference among the "
                "K no-hook repeats of the same state (A2, Johnny; confirmed by Ark and Zcode)",
            # --- the other level: per item ---
            "bitwise_identical_per_item": bool(np.array_equal(li, plain)),
            "per_item_max_abs_diff": repr(d1_item),
            "per_item_max_abs_diff_nohook_vs_nohook_FLOOR": fl["max_difference_per_item_max"],
            "per_item_max_abs_diff_in_float32_ulps": repr(
                float(d1_item / float(np.spacing(np.float32(np.max(np.abs(plain))))))),
            "ulps_level": "the ULP figure above is the PER-ITEM level; the loss-level "
                          "difference is a different and larger number of ULPs and is not "
                          "the same statistic",
            "abs_diff_loss_in_float32_ulps": repr(
                float(d1 / float(np.spacing(np.float32(abs(p0)))))),
            "floor_nohook_vs_nohook": fl,                                  # A3
            "descriptive_hook_diff_le_max_floor": {                        # A3, UNREGISTERED
                "registered": False,
                "replaces_the_verdict": False,
                "what": "is the with-hook difference no larger than the largest of the K "
                        "no-hook-vs-no-hook differences of the same state? Descriptive only: "
                        "it does not enter, soften or override the P1' pass/fail above, which "
                        "is the registered 1e-6 on the loss.",
                "k": fl["k"],
                "loss_level": {
                    "hook_diff": repr(d1),
                    "max_floor": fl["max_difference_loss"],
                    "hook_diff_le_max_floor":
                        (bool(d1 <= max(float(x) for x in fl["differences_loss"]))
                         if fl["differences_loss"] else None),
                },
                "per_item_level": {
                    "hook_diff": repr(d1_item),
                    "max_floor": fl["max_difference_per_item_max"],
                    "hook_diff_le_max_floor":
                        (bool(d1_item <= max(float(x)
                                             for x in fl["differences_per_item_max"]))
                         if fl["differences_per_item_max"] else None),
                },
                "caveat_at_k_1": "at --floor-k 1 the floor is a sample of size one and this "
                                 "comparison is a coin toss dressed as a bound",
            },
            "pass": bool(np.array_equal(li, plain) or d1 <= P1_TOL),
            "pass_level": "loss",
        },
        "P2prime_the_instrument_sees_something": {
            "what": "(i) the per-item vectors over the input cell types differ between items; "
                    "(ii) the 65-vector is not constant",
            "threshold_source": "the measured floor (README Sec 6); NEVER the data being judged",
            "threshold_rule": P2_THRESHOLD_RULE,                       # A6
            "threshold_rule_declared": P2_THRESHOLD_RULE_DECLARED,
            "threshold_rule_multiplier": P2_FLOOR_MULTIPLIER,
            "threshold_rule_applied_by": "--floor-summarize, which writes the products into "
                                         "rowB_floor[_det].json; this block keeps its nulls "
                                         "until that file exists",
            "i_input_type_vectors_differ_between_items": {
                "input_type_indices": [int(i) for i in input_type_idx],
                "n_item_pairs": len(pair),
                "min_pairwise_max_abs_diff": repr(float(min(pair))) if pair else None,
                "max_pairwise_max_abs_diff": repr(float(max(pair))) if pair else None,
                "threshold": None,
                "verdict": None,
                "verdict_status": "pending_floor",
            },
            "ii_the_65_vector_is_not_constant": {
                "population_sd_over_types": repr(float(agg.std(ddof=0))),
                "range_over_types": repr(float(agg.max() - agg.min())),
                "n_distinct_values": int(np.unique(agg).size),
                "threshold": None,
                "verdict": None,
                "verdict_status": "pending_floor",
            },
        },
    }


def service_fields():
    return {
        "status": STATUS,
        "readable_as_verdict": False,
        "hook_kind": "record",
        "activity_mutated": False,
        "recording_detached": True,
        "note": "recording_detached means the hook calls .detach() inside the hook; the "
                "reduction runs on the GPU and only the reduced per-type vectors (65) and the "
                "central-cell vector (65) are moved to CPU; activity_mutated=false is asserted "
                "in the hook (`state.nodes.activity is x` after the read), not assumed",
        "reduction_path": RUNTIME["reduction_path"],
        "reduction_device": (
            "the activity's own device (GPU)" if RUNTIME["reduction_path"] == "gpu"
            else "the host (CPU): the detached activity is moved off the GPU before the "
                 "reduction (A5, --reduce-on cpu)") +
            "; float64 index_add_ on the GPU may sum in a different order than on the CPU, so "
            "the last bits can differ. The three-checkpoint outputs of 2026-09-20 in this "
            "directory were produced on the CPU path and are SUPERSEDED, not mixed.",
        "deterministic": bool(RUNTIME["deterministic"]),
        "determinism_mode": (
            "torch.use_deterministic_algorithms(True), cudnn.deterministic=True, "
            "cudnn.benchmark=False (A4, --deterministic); outputs carry the _det suffix"
            if RUNTIME["deterministic"] else
            "as the nights ran: --no-determinism (diag1_eval_paths.build_solver:90-93, "
            "run_individual.py:284-286); use_deterministic_algorithms is NOT set"),
        "floor_k": int(RUNTIME["floor_k"]),
    }


# ---------------------------------------------------------------- csv
def write_profile_csv(path, entry, axis, item_names):
    keys = ["mean_by_type", "std_by_type", "last_frame_by_type", "central_cell_mean",
            "mean_by_type_skip_first_quarter", "central_cell_mean_skip_first_quarter"]
    hdr = (["netdir", "run_label", "individual", "replicate_of", "chkpt_index", "chkpt_iter",
            "type"]
           + [f"agg_{k}" for k in keys]
           + [f"mean_by_type_item_{n}" for n in item_names]
           + [f"central_skip_item_{n}" for n in item_names])
    lines = [f"# {STATUS}; readable_as_verdict=false",
             f"# axis_sha256={axis['axis_sha256']} script_sha256={sha256_file(__file__)}",
             f"# agg_* = mean over the {len(item_names)} held-out items",
             f"# reduction_path={RUNTIME['reduction_path']} "
             f"deterministic={str(bool(RUNTIME['deterministic'])).lower()}",
             ",".join(hdr)]
    V = entry["_arrays"]
    for i, T in enumerate(axis["type_labels"]):
        row = [entry["run"]["netdir"], entry["run"]["run_label"],
               str(entry["run"]["individual"]), str(entry["run"]["replicate_of"]),
               str(entry["run"]["chkpt_index"]), str(entry["run"]["chkpt_iter"]), T]
        row += [repr(float(V[k][:, i].mean())) for k in keys]
        row += [repr(float(x)) for x in V["mean_by_type"][:, i]]
        row += [repr(float(x)) for x in V["central_cell_mean_skip_first_quarter"][:, i]]
        lines.append(",".join(row))
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- dry run
def dry_run(a, reg, runs):
    plan = {"mode": "dry-run", **service_fields(), "utc": time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "git_head": git_head(),
        "script_sha256": sha256_file(__file__), "out_dir": str(Path(a.out_dir).resolve()),
        "run_registry_source": str(RUN_COLUMNS),
        "scope": ("the ten complete runs of nights 1-5 (--night all10)"
                  if a.night == "all10" else
                  (f"--night {a.night}" if a.night else f"--netdir {a.netdir}")),
        "N": individuals_of(runs),
        "wave_witnesses": cross_check_waves(reg), "runs": []}
    axis = None
    total_pairs = 0
    for e in runs:
        act = announce_activity_h5(e["netdir"])          # FIRST, always
        tab = chkpt_table_netdir(e["netdir"])
        label_check = check_netdir_unambiguous(e)
        n_files = check_run_complete(e, tab) if a.night == "all10" else len(
            list((Path(e["netdir"]) / "chkpts").glob("chkpt_*")))
        meta = run_meta(e["netdir"])
        if axis is None:
            cdir = find_connectome_dir(meta["connectome"])
            axis = axis_from_disk(cdir)
            plan["axis"] = {k: v for k, v in axis.items() if k not in
                            ("type_labels", "node_count_per_type", "central_cell_index_per_type")}
            plan["axis"]["type_labels_first8"] = axis["type_labels"][:8]
            plan["axis"]["type_labels_last4"] = axis["type_labels"][-4:]
            plan["axis"]["node_count_per_type_first8"] = axis["node_count_per_type"][:8]
            plan["axis"]["central_cell_index_per_type_first8"] = \
                axis["central_cell_index_per_type"][:8]
            plan["axis_vs_rowA"] = check_axis_against_rowA(axis)
        chosen = choose_chkpts(a.chkpts, tab)
        total_pairs += len(chosen)
        sides = [side_of_stop_iter(it, meta["activity_penalty"]["stop_iter"])
                 for _, it, _, _ in chosen]
        missing = [str(p) for _, _, _, p in chosen if not p.exists()]
        plan["runs"].append({
            "netdir": e["netdir"], "run_label": e["run_label"], "run_id": e["run_id"],
            "seed": e["seed"], "role": e["role"], "night": e["night"],
            "individual": e["individual"], "individual_label": e["individual_label"],
            "replicate_of": e["replicate_of"],
            "is_individual_representative": e["is_individual_representative"],
            "n_runs_of_this_individual": e["n_runs_of_this_individual"],
            "twin_of": e["twin_of"], "twin_of_canonical": e["twin_of_canonical"],
            "label_unambiguous_on_disk": label_check,
            "activity_h5": act,
            "n_checkpoint_files_on_disk": n_files,
            "n_checkpoints_on_disk": len(tab),
            "chkpt_index_range": [tab[0][0], tab[-1][0]],
            "chkpt_iter_first_last": [tab[0][1], tab[-1][1]],
            "solver_iteration_first_last": [tab[0][2], tab[-1][2]],
            "n_checkpoints_selected": len(chosen),
            "missing_checkpoint_files": missing,
            "activity_penalty_resolved": meta["activity_penalty"],
            "n_selected_before_stop_iter": sum(s["side_by_chkpt_iter"] == "before" for s in sides),
            "n_selected_at_or_after_stop_iter": sum(
                s["side_by_chkpt_iter"] == "at_or_after" for s in sides),
            "n_selected_where_the_two_conventions_disagree": sum(
                not s["conventions_agree"] for s in sides),
            "dt_config": meta["dt_config"], "n_frames_config": meta["n_frames_config"],
            "run_status": meta["status"],
        })
    n_types = axis["n_types"] if axis else None
    # Projected output size.  n_frames is not on disk (it is the simulation axis, resolved at
    # run time); the figure below is evaluated at the geometry recorded in
    # results/night2/diagnostics/rowB/README.md Sec 9 -- 40 simulation steps per item -- which
    # is axis metadata, not a measurement, and is re-derived at run time regardless.
    nf_assumed, ni_assumed = 40, 16
    per_pair = (2 * ni_assumed * (n_types or 0) * nf_assumed
                + 6 * ni_assumed * (n_types or 0)) * 8
    per_pair_evals = a.floor_k + 3
    plan["plan"] = {
        "n_runs": len(runs),
        "n_individuals": plan["N"]["n_individuals"],
        "n_run_checkpoint_pairs": total_pairs,
        "floor_k": a.floor_k,
        "evaluations_per_pair": per_pair_evals,
        "evaluations_total": per_pair_evals * total_pairs,
        "evaluations_breakdown": f"{a.floor_k + 1} no-hook per-item evaluations (P0, plus its "
                                 f"own no-hook-vs-no-hook floor of K={a.floor_k} differences "
                                 f"at both levels) + 1 rung-hook path (P0's second reading) "
                                 f"+ 1 with the recorder",
        "evaluations_total_at_floor_k_1": 4 * total_pairs,
        "evaluations_total_at_floor_k_5": 8 * total_pairs,
        "deterministic": bool(a.deterministic),
        "reduction_path": a.reduce_on,
        "output_suffix": "_det" if a.deterministic else "(none)",
        "projected_steps_h5_bytes_uncompressed": per_pair * total_pairs,
        "projected_steps_h5_note": f"at n_items={ni_assumed}, n_frames={nf_assumed}; gzip-4 is "
                                   f"applied, so the file on disk is smaller. Decide before "
                                   f"launching whether --chkpts all belongs in the repository.",
        "n_items": "resolved at run time from solver.task.val_seq_index (16 in every night so far)",
        "n_frames": "resolved at run time from the recorded steps per item; NOT the config's "
                    "n_frames (which is the pre-resampling count)",
        "t_pre": T_PRE,
        "n_types": n_types,
        "matrices_per_pair": ["mean_by_type", "std_by_type", "last_frame_by_type",
                              "central_cell_mean", "mean_by_type_skip_first_quarter",
                              "central_cell_mean_skip_first_quarter"],
        "matrix_shape": ["n_items", n_types],
        "steps_by_type_shape": ["n_items", n_types, "n_frames"],
        "outputs": [out_name(a, "rowB_records", "json"), out_name(a, "rowB_axis", "json"),
                    out_name(a, "rowB_controls", "json"),
                    out_name(a, "rowB_profiles_<run_label>_<chkpt_iter>", "csv"),
                    out_name(a, "rowB_steps_<run_label>", "h5")],
    }
    print(json.dumps(plan, indent=1))
    Path(a.out_dir).mkdir(parents=True, exist_ok=True)
    (Path(a.out_dir) / out_name(a, "rowB_dryrun", "json")).write_text(
        json.dumps(plan, indent=1), encoding="utf-8")
    print(f"DRY-RUN OK  runs={len(runs)}  individuals={plan['N']['n_individuals']}  "
          f"pairs={total_pairs}  floor_k={a.floor_k}  "
          f"evaluations={per_pair_evals * total_pairs}  "
          f"axis_sha256={axis['axis_sha256'] if axis else None}", flush=True)
    print("NOTHING WAS EVALUATED: no checkpoint was loaded, no network was run.", flush=True)
    return 0


def choose_chkpts(spec, tab):
    if spec == "all":
        return list(tab)
    want = [int(x) for x in spec.split(",") if x.strip()]
    by_i = {r[0]: r for r in tab}
    out = []
    for i in want:
        if i not in by_i:
            raise Refusal(f"checkpoint index {i} is not in this run's chkpt_index.h5")
        out.append(by_i[i])
    return out


# ---------------------------------------------------------------- the real run
def real_run(a, reg, runs):
    torch, D, ABL, RB, det_before = _gpu_imports(a.deterministic)
    import flyvis
    RecorderB = make_recorder_class(torch, RB, reduce_on=a.reduce_on)

    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    scratch = Path(a.netdir_root) if a.netdir_root else (out / "_scratch_netdir")
    t_start = time.perf_counter()

    solver = D.build_solver(scratch)
    # build_solver DELIBERATELY sets cudnn.deterministic = False and benchmark = False
    # (diag1_eval_paths.py:90-93, reproducing run_individual.py:284-286 under
    # --no-determinism).  Under --deterministic the two cudnn flags are therefore re-applied
    # after it, and BOTH applications are recorded, so the record shows the order rather than
    # a final state that could have come from either.
    det_after = apply_determinism(torch, a.deterministic, "after_build_solver")
    net = solver.network
    device = flyvis.device

    # ---- the axis, taken from net.connectome exactly as ablation.py takes it
    types_arr = ABL.node_type_array(net)                          # ablation.py:87-89
    unique_types = [x.decode() if isinstance(x, bytes) else str(x)
                    for x in net.connectome.unique_cell_types[:]]
    central = [int(x) for x in net.connectome.central_cells_index[:]]
    axis = build_axis(unique_types, types_arr, central, source="net.connectome (live)")
    axis_vs_rowA = check_axis_against_rowA(axis)                  # hard refusal inside
    n_types = axis["n_types"]

    t2i = {t: i for i, t in enumerate(unique_types)}
    type_index = torch.as_tensor(np.array([t2i[t] for t in types_arr]), dtype=torch.long)
    counts = torch.as_tensor(np.array(axis["node_count_per_type"], dtype=np.float64),
                             dtype=torch.float64)
    central_index = torch.as_tensor(np.array(central), dtype=torch.long)
    ctx = (type_index, counts, n_types, central_index)

    item_names = D.val_item_names(solver)
    n_items = len(item_names)
    input_types = [x.decode() if isinstance(x, bytes) else str(x)
                   for x in net.connectome.input_cell_types[:]]
    input_type_idx = [t2i[t] for t in input_types]
    assert int(solver.task.val_data.batch_size) == 1, solver.task.val_data.batch_size

    env = {
        "git_head": git_head(),
        "script_sha256": sha256_file(__file__),
        "torch": torch.__version__, "flyvis": flyvis.__version__, "numpy": np.__version__,
        "python": sys.version.split()[0],
        "CUBLAS_WORKSPACE_CONFIG": os.environ.get("CUBLAS_WORKSPACE_CONFIG"),
        "FLYVIS_ROOT_DIR": os.environ.get("FLYVIS_ROOT_DIR"),
        "device": str(device),
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "gpu_instrument": gpu_instrument_labels(torch),  # B3: driver/CUDA-runtime provenance
        "cudnn_deterministic": bool(torch.backends.cudnn.deterministic),
        "cudnn_benchmark": bool(torch.backends.cudnn.benchmark),
        "deterministic": bool(a.deterministic),
        "determinism_applied": {"before_any_cuda_work": det_before,
                                "after_build_solver": det_after},
        "determinism_note": "set by diag1_eval_paths.build_solver:90-93, which reproduces "
                            "run_individual.py:284-286 under --no-determinism, the flag every "
                            "night wave ran under (wave_night4.json / wave_night5.json "
                            "\"no_determinism\": true)"
                            + (" -- and then OVERRIDDEN by --deterministic (A4): "
                               "use_deterministic_algorithms(True), cudnn.deterministic=True, "
                               "cudnn.benchmark=False. This is a DIFFERENT instrument from the "
                               "nights' evaluation path and writes under _det names."
                               if a.deterministic else ""),
        "reduction_path": a.reduce_on,
        "floor_k": int(a.floor_k),
        "scratch_netdir": str(solver.dir.path),
    }
    (out / out_name(a, "rowB_axis", "json")).write_text(json.dumps(
        {**service_fields(), "env": env, "axis": axis, "axis_vs_rowA": axis_vs_rowA,
         "input_cell_types": input_types,
         "output_cell_types": [x.decode() if isinstance(x, bytes) else str(x)
                               for x in net.connectome.output_cell_types[:]]},
        indent=1), encoding="utf-8")

    records = {**service_fields(), "env": env, "axis_sha256": axis["axis_sha256"],
               "axis_rowA_sha256": axis["axis_rowA_sha256"],
               "N": individuals_of(runs), "entries": []}
    controls = {**service_fields(), "env": env, "N": individuals_of(runs),
                "p2prime_threshold_rule": {"rule": P2_THRESHOLD_RULE,
                                           "declared": P2_THRESHOLD_RULE_DECLARED,
                                           "multiplier": P2_FLOOR_MULTIPLIER},
                "entries": RB.NoDupDict()}

    for e in runs:
        announce_activity_h5(e["netdir"])                         # FIRST, always
        tab = chkpt_table_netdir(e["netdir"])
        check_netdir_unambiguous(e)
        if a.night == "all10":
            check_run_complete(e, tab)
        meta = run_meta(e["netdir"])
        ap = meta["activity_penalty"]
        if int(solver.penalty.activity_penalty_stop_iter) != ap["stop_iter"]:
            raise Refusal(
                f"{e['netdir']}: the run's own stop_iter {ap['stop_iter']} disagrees with the "
                f"scratch solver's {solver.penalty.activity_penalty_stop_iter}; the penalty "
                f"constants must come from the run, and the two must not diverge silently")
        chosen = choose_chkpts(a.chkpts, tab)
        h5path = out / out_name(a, f"rowB_steps_{e['run_label']}", "h5")
        if a.floor_repeat is not None:
            h5path = out / out_name(
                a, f"rowB_floor_steps_{e['run_label']}_proc{a.floor_repeat}", "h5")
        with h5py.File(h5path, "w") as fh:
            fh.attrs["status"] = STATUS
            fh.attrs["readable_as_verdict"] = False
            fh.attrs["axis_sha256"] = axis["axis_sha256"]
            fh.attrs["netdir"] = e["netdir"]
            fh.attrs["individual"] = int(e["individual"])
            fh.attrs["replicate_of"] = json.dumps(e["replicate_of"])
            fh.attrs["deterministic"] = bool(a.deterministic)     # A4
            fh.attrs["reduction_path"] = a.reduce_on              # A5/G
            fh.attrs["floor_k"] = int(a.floor_k)
            fh.attrs["type_labels"] = json.dumps(axis["type_labels"])
            fh.attrs["item_names"] = json.dumps(item_names)
            fh.attrs["axes"] = "steps_by_type[item, type, frame]"
            for ci, chkpt_iter, solver_it, path in chosen:
                if not path.exists():
                    raise Refusal(f"missing checkpoint {path}")
                info = D.load_checkpoint(solver, path)
                if int(info["stored_iteration"]) != int(chkpt_iter):
                    raise Refusal(f"{path}: chkpt_iter.h5 says {chkpt_iter}, the checkpoint "
                                  f"file says {info['stored_iteration']}")

                t0 = time.perf_counter()
                # A3: K+1 no-hook evaluations of the SAME state.  plains[0] is P0's reading;
                # the other K are the floor, differenced against it at both levels.
                plains = [np.array(D.per_item_eval(solver, t_pre=T_PRE)["flow"],
                                   dtype=np.float64) for _ in range(a.floor_k + 1)]
                hook_val = D.hook_eval(solver)
                li, means, stds, centrals, inv, ncalls = eval_with_recorder(
                    torch, D, RB, RecorderB, solver, ctx)
                wall = time.perf_counter() - t0

                red = reduce_phases(means, stds, centrals, n_items)
                if not all(inv.values()):
                    raise Refusal(f"{path}: eval_rung invariants failed {inv}")

                g = fh.create_group(f"chkpt_{ci:05d}")
                g.attrs["chkpt_iter"] = int(chkpt_iter)
                g.attrs["solver_iteration"] = int(solver_it)
                g.attrs["n_frames"] = int(red["n_frames"])
                g.attrs["skip_first_quarter_from_frame"] = int(red["skip_first_quarter_from_frame"])
                for k in ("steps_by_type", "steps_central", "mean_by_type", "std_by_type",
                          "last_frame_by_type", "central_cell_mean",
                          "mean_by_type_skip_first_quarter",
                          "central_cell_mean_skip_first_quarter"):
                    g.create_dataset(k, data=red[k], compression="gzip", compression_opts=4)

                entry = {
                    "run": {
                        "netdir": e["netdir"], "run_id": e["run_id"],
                        "run_label": e["run_label"], "seed": e["seed"], "role": e["role"],
                        "run_index_for_seed": e["run_index_for_seed"], "night": e["night"],
                        "individual": e["individual"],
                        "individual_label": e["individual_label"],
                        "replicate_of": e["replicate_of"],
                        "is_individual_representative": e["is_individual_representative"],
                        "n_runs_of_this_individual": e["n_runs_of_this_individual"],
                        "N_note": "N is counted in individuals, not runs; a replicate run is "
                                  "the same individual measured again and does not enter N",
                        "twin_of": e["twin_of"], "twin_of_canonical": e["twin_of_canonical"],
                        "chkpt_index": int(ci),
                        "chkpt_iter": int(chkpt_iter),
                        "chkpt_iter_source": "chkpt_iter.h5 (read, not derived from the index)",
                        "solver_iteration": int(solver_it),
                        "side_of_stop_iter": side_of_stop_iter(chkpt_iter, ap["stop_iter"]),
                        "checkpoint_sha256": sha256_file(path),
                        "checkpoint_path": str(path),
                        "git_head": env["git_head"],
                        "torch": env["torch"], "flyvis": env["flyvis"], "numpy": env["numpy"],
                        "CUBLAS_WORKSPACE_CONFIG": env["CUBLAS_WORKSPACE_CONFIG"],
                        "n_frames": int(red["n_frames"]),
                        "n_frames_source": "recorded steps per item (the simulation axis); the "
                                           "config's n_frames is the pre-resampling count",
                        "n_frames_config": meta["n_frames_config"],
                        "dt": float(solver.task.dataset.dt),
                        "dt_checkpoint": float(info["dt"]),
                        "t_pre": T_PRE,
                        "n_items": n_items,
                        "item_names": item_names,
                        "n_nodes": axis["n_nodes"],
                        "n_types": axis["n_types"],
                        "steps_steady_state": int(red["steps_steady_state"]),
                        "n_state_hook_calls": int(ncalls),
                        "eval_wall_s": round(wall, 3),
                    },
                    "axis_sha256": axis["axis_sha256"],
                    "axis_rowA_sha256": axis["axis_rowA_sha256"],
                    "values_file": str(h5path.name),
                    "values_group": g.name,
                    "aggregate_over_items": {
                        k: {T: repr(float(red[k][:, i].mean()))
                            for i, T in enumerate(axis["type_labels"])}
                        for k in ("mean_by_type", "std_by_type", "last_frame_by_type",
                                  "central_cell_mean", "mean_by_type_skip_first_quarter",
                                  "central_cell_mean_skip_first_quarter")
                    },
                    "falsifier_penalized_quantity": penalised_quantity(
                        red["central_cell_mean_skip_first_quarter"], ap),
                    "eval_rung_invariants": inv,
                    **service_fields(),
                }
                entry["_arrays"] = red
                key = (e["netdir"], int(ci))
                controls["entries"][repr(key)] = controls_block(
                    red, li, plains, hook_val, info["stored_val_loss"], input_type_idx)
                csv_name = (out_name(a, f"rowB_profiles_{e['run_label']}_{chkpt_iter}", "csv")
                            if a.floor_repeat is None else
                            out_name(a, f"rowB_floor_profiles_{e['run_label']}_{chkpt_iter}"
                                        f"_proc{a.floor_repeat}", "csv"))
                write_profile_csv(out / csv_name, entry, axis, item_names)
                del entry["_arrays"]
                if a.floor_repeat is not None:
                    entry["floor_repeat"] = {"proc": a.floor_repeat, "pid": os.getpid()}
                records["entries"].append(entry)
                print("ROWB", e["run_label"], "chkpt", ci, "iter", chkpt_iter,
                      "side", entry["run"]["side_of_stop_iter"]["side_by_chkpt_iter"],
                      "hooks", ncalls, "frames", red["n_frames"],
                      "wall_s", round(wall, 2), flush=True)

    controls["entries"] = dict(controls["entries"])
    records["wall_s_total"] = round(time.perf_counter() - t_start, 1)
    suffix = "" if a.floor_repeat is None else f"_floor_proc{a.floor_repeat}"
    (out / out_name(a, f"rowB_records{suffix}", "json")).write_text(
        json.dumps(records, indent=1), encoding="utf-8")
    (out / out_name(a, f"rowB_controls{suffix}", "json")).write_text(
        json.dumps(controls, indent=1), encoding="utf-8")
    print("DONE", records["wall_s_total"], "s", flush=True)
    return 0


# ---------------------------------------------------------------- floor summary (no GPU)
def floor_summarize(a):
    """sigma by type and sigma of the metric, from three fresh-process repeats.

    Not a measurement: arithmetic over files this script wrote.  The floor is measured for
    THIS metric at THIS (run, checkpoint), never borrowed from the ablation (README Sec 6).
    """
    out = Path(a.out_dir)
    procs = sorted(out.glob(out_name(a, "rowB_records_floor_proc*", "json")))
    if not RUNTIME["deterministic"]:
        # `proc*` also matches the `_det` files lying beside them once both modes exist;
        # the normal-mode summary must not pick up the other instrument's repeats.
        procs = [p for p in procs if not p.stem.endswith("_det")]
    if len(procs) < 3:
        raise Refusal(f"the floor needs 3 fresh-process repeats; found {len(procs)} in {out}")
    blocks = [json.loads(p.read_text(encoding="utf-8")) for p in procs]
    if any(len(b["entries"]) != 1 for b in blocks):
        raise Refusal("each floor process must hold exactly one (run, checkpoint) entry")
    # A6: "same path, same mode" is part of the rule, so it is checked and not assumed.
    modes = {(b.get("reduction_path"), bool(b.get("deterministic"))) for b in blocks}
    if len(modes) != 1:
        raise Refusal(f"the floor processes do not share one instrument: {sorted(modes)}; a "
                      f"threshold may only be built from a floor measured on the same "
                      f"reduction path and the same determinism mode")
    mode = sorted(modes)[0]
    # B2 (2026-09-20): `floor_k` means "K no-hook floor repeats inside one process" in the
    # per-process records/controls -- it is a real setting there.  In THIS summary it used to
    # be RUNTIME["floor_k"], i.e. --floor-summarize's own unused default, which meant nothing.
    # It is now read from the three per-process record files themselves, and a disagreement is
    # a refusal: a summary may not silently average over floors measured at different K.
    floor_ks_inside = {int(b["floor_k"]) for b in blocks}
    if len(floor_ks_inside) != 1:
        raise Refusal(f"the three floor processes do not share one floor_k (the K of no-hook "
                      f"repeats inside each process): {sorted(floor_ks_inside)}; a floor may "
                      f"not be summarized across processes run at different K")
    floor_k_inside_each_process = sorted(floor_ks_inside)[0]
    keys = ("mean_by_type", "central_cell_mean_skip_first_quarter")
    pairs = set()
    for b in blocks:
        for e in b["entries"]:
            pairs.add((e["run"]["netdir"], e["run"]["chkpt_index"]))
    if len(pairs) != 1:
        raise Refusal(f"the floor must be the SAME (run, checkpoint) in every process; got {pairs}")
    res = {**service_fields(), "n_processes": len(blocks), "source_files": [str(p) for p in procs],
           "pair": sorted(pairs)[0],
           "floor_instrument": {"reduction_path": mode[0], "deterministic": mode[1]},
           "by_quantity": {}}
    del res["floor_k"]  # B2: replaced by floor_k_inside_each_process below; see docstring.
    res["floor_k_inside_each_process"] = floor_k_inside_each_process
    res["floor_k_inside_each_process_source"] = "read from the three --floor-repeat record " \
        "files' own top-level floor_k, and refused (exit 3) if they disagree"
    for k in keys:
        mats = []
        for b in blocks:
            e = b["entries"][0]
            d = e["aggregate_over_items"][k]
            mats.append(np.array([float(d[t]) for t in d]))
        M = np.stack(mats)
        # B1 (2026-09-20, Ark / CC): M.std(axis=0, ddof=1) over three BITWISE-IDENTICAL float64
        # rows can return ~2e-15 instead of exactly 0 -- numpy's mean of identical values is not
        # always exactly that value, so the variance computed from it is not always exactly
        # zero either. Guard: where the range (max - min) across the three processes is exactly
        # 0 for a type, sigma for that type is exactly 0.0, never the rounding residue.
        rng = M.max(axis=0) - M.min(axis=0)
        raw_sigma = M.std(axis=0, ddof=1)
        sigma_by_type = np.where(rng == 0.0, 0.0, raw_sigma)
        res["by_quantity"][k] = {
            "sigma_by_type": [repr(float(x)) for x in sigma_by_type],
            "max_sigma_by_type": repr(float(sigma_by_type.max())),
            "max_abs_pairwise_difference": repr(float(np.max(
                [np.max(np.abs(M[i] - M[j])) for i in range(len(M)) for j in range(i + 1, len(M))]))),
        }
    res["p2prime_thresholds"] = p2prime_thresholds(res)
    path = out / out_name(a, "rowB_floor", "json")
    path.write_text(json.dumps(res, indent=1), encoding="utf-8")
    print("FLOOR WROTE", path, flush=True)
    print(f"P2' THRESHOLDS = {P2_FLOOR_MULTIPLIER} x the measured floor "
          f"(rule declared {P2_THRESHOLD_RULE_DECLARED}, before any floor existed)", flush=True)
    return 0


def p2prime_thresholds(res):
    """A6: apply the multiplier declared 2026-09-20 to the floor just measured.

    A COMPUTATION, NOT A JUDGEMENT.  The multiplier and the rule are constants at the top of
    this file, written down before any floor for this metric existed; this function only
    multiplies and records which floor it multiplied.

    Both P2' statistics are read off `mean_by_type` -- (i) the largest/smallest pairwise
    difference between item vectors restricted to the input types, (ii) the spread of the
    aggregate 65-vector -- so both take the `mean_by_type` floor.  The central-cell threshold
    is written beside them for the penalised reduction, which has its own scale.
    """
    base = res["by_quantity"]
    instrument = res["floor_instrument"]
    def scaled(q):
        f = float(base[q]["max_abs_pairwise_difference"])
        return {"floor_quantity": q,
                "floor_max_abs_pairwise_difference": base[q]["max_abs_pairwise_difference"],
                "floor_max_sigma_by_type": base[q]["max_sigma_by_type"],
                "multiplier": P2_FLOOR_MULTIPLIER,
                "threshold": repr(P2_FLOOR_MULTIPLIER * f),
                # B4 (2026-09-20): the mode is part of the threshold, stated on the same line
                # as the threshold and not only in this file's header.
                "reduction_path": instrument["reduction_path"],
                "deterministic": instrument["deterministic"],
                "mode_is_part_of_this_threshold": "this number is valid only for the "
                    "reduction_path and deterministic mode named on this same line; it is not "
                    "portable to the other mode even at the same multiplier"}
    return {
        "rule": P2_THRESHOLD_RULE,
        "rule_declared": P2_THRESHOLD_RULE_DECLARED,
        "rule_declared_before_any_floor_existed": True,
        "honest_note": "the P2' statistics of the three-checkpoint run of 2026-09-20 were "
                       "already visible to reviewers before this multiplier was declared; the "
                       "multiplier is a round number chosen for that reason and not tuned",
        "applies_to_instrument": res["floor_instrument"],
        "i_input_type_vectors_differ_between_items": scaled("mean_by_type"),
        "ii_the_65_vector_is_not_constant": scaled("mean_by_type"),
        "central_cell_mean_skip_first_quarter":
            scaled("central_cell_mean_skip_first_quarter"),
        "where_applied": "these thresholds are written HERE, in the floor file. The controls "
                         "files keep the nulls they were written with; nothing already "
                         "written is edited after the fact.",
    }


# ---------------------------------------------------------------- cli
def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Row B passive activity recording on the complete runs of nights 1-5. "
                    "UNREGISTERED DIAGNOSTIC -- no number it produces is a verdict.")
    p.add_argument("--netdir", action="append", default=[],
                   help="a run directory (or its run_id, e.g. 9992/003). Repeatable. "
                        "Runs are keyed by netdir, never by label.")
    p.add_argument("--night", choices=["4", "5", "all", "all10"], default=None,
                   help="select runs from results/night5/run_columns.csv: '4' / '5' one "
                        "night, 'all' nights 4 and 5 (four runs), 'all10' THE TEN COMPLETE "
                        "RUNS of nights 1-5 (six individuals; A1). 'all10' refuses (exit 3) "
                        "any run that does not hold exactly 72 checkpoints and any netdir "
                        "whose label is ambiguous on disk.")
    p.add_argument("--chkpts", default="all",
                   help="'all' or a comma-separated list of checkpoint INDICES, e.g. 0,8,71")
    p.add_argument("--out-dir", default=str(HERE))
    p.add_argument("--dry-run", action="store_true",
                   help="resolve paths, h5 shapes, checkpoint counts, the type axis and the "
                        "plan, and print them. Imports neither torch nor flyvis; loads no "
                        "checkpoint; runs no network.")
    p.add_argument("--floor-repeat", type=int, default=None, metavar="N",
                   help="mark this process as fresh-process repeat N of the floor procedure "
                        "(README Sec 6). Outputs are written under _floor_procN names.")
    p.add_argument("--floor-summarize", action="store_true",
                   help="no GPU: read the three --floor-repeat records already in --out-dir "
                        "and write rowB_floor[_det].json (sigma by type, sigma of the metric, "
                        "and the P2' thresholds from the rule declared 2026-09-20).")
    p.add_argument("--floor-k", type=int, default=1, metavar="K",
                   help="A3: evaluate the same state with NO hook K+1 times per (run, "
                        "checkpoint) and record all K no-hook-vs-no-hook differences at both "
                        "levels (per-item max and the loss) plus their maxima. Default 1, "
                        "which reproduces the earlier two-evaluation behaviour exactly. Costs "
                        "K+3 evaluations per pair instead of 4.")
    p.add_argument("--deterministic", action="store_true",
                   help="A4: set torch.use_deterministic_algorithms(True), "
                        "cudnn.deterministic=True, cudnn.benchmark=False before any CUDA work. "
                        "A DIFFERENT INSTRUMENT from the nights' path: every output is written "
                        "under a _det name so the two can never be mixed. If PyTorch refuses "
                        "an operator, the script names it in rowB_nondeterministic_op_det.json "
                        "and exits 4 -- that is a finding, not a crash. Training flags are not "
                        "touched.")
    p.add_argument("--reduce-on", choices=["gpu", "cpu"], default="gpu",
                   help="A5: where the hook's float64 index_add_ runs. Default gpu (the "
                        "owner's GPU-first instruction). 'cpu' moves the detached activity to "
                        "the host before reducing, so the forward can be tested under "
                        "--deterministic with index_add_ -- which is on PyTorch's "
                        "nondeterministic CUDA list -- off the GPU.")
    p.add_argument("--netdir-root", default=None,
                   help="scratch datamate root for the throw-away solver directory "
                        "(must contain 'scratchpad'; diag1_eval_paths.build_solver:116)")
    a = p.parse_args(argv)
    if a.floor_k < 1:
        p.error("--floor-k must be at least 1: a floor needs at least one repeat")
    if a.floor_summarize:
        return a
    if not a.netdir and a.night is None:
        p.error("one of --netdir or --night is required")
    if a.netdir and a.night is not None:
        p.error("--netdir and --night are mutually exclusive")
    if a.floor_repeat is not None and a.chkpts == "all":
        p.error("--floor-repeat needs a single checkpoint: pass --chkpts <index>")
    return a


def main(argv=None):
    a = parse_args(argv)
    RUNTIME["deterministic"] = bool(a.deterministic)
    RUNTIME["reduction_path"] = a.reduce_on
    RUNTIME["floor_k"] = int(a.floor_k)
    if a.floor_summarize:
        return floor_summarize(a)
    reg = read_run_columns()
    runs = select_runs(reg, a.night, a.netdir)
    if not runs:
        raise Refusal("no runs selected")
    if a.floor_repeat is not None and len(runs) != 1:
        raise Refusal("--floor-repeat needs exactly one --netdir")
    N = individuals_of(runs)
    print(f"# {STATUS}; readable_as_verdict=false; "
          f"{N['n_runs']} run(s) = {N['n_individuals']} individual(s) "
          f"(N is counted in individuals): {[r['run_label'] for r in runs]}; "
          f"reduction_path={a.reduce_on} deterministic={str(bool(a.deterministic)).lower()} "
          f"floor_k={a.floor_k}", flush=True)
    if a.dry_run:
        return dry_run(a, reg, runs)
    # A4: a refused operator is a FINDING.  It is caught here, at top level, named in a json
    # beside the other outputs, and exits 4 -- distinct from the refusals' 3.
    try:
        return real_run(a, reg, runs)
    except RuntimeError as exc:
        if "does not have a deterministic implementation" not in str(exc):
            raise
        payload = nondeterministic_finding(exc, a)
        outp = Path(a.out_dir)
        outp.mkdir(parents=True, exist_ok=True)
        path = outp / out_name(a, "rowB_nondeterministic_op", "json")
        path.write_text(json.dumps(payload, indent=1), encoding="utf-8")
        raise NondeterministicOperator(path, payload) from None


if __name__ == "__main__":
    sys.exit(main())
