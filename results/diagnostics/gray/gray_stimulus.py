"""Gray-stimulus control -- 6 runs x 2 checkpoints x 4 input conditions on the 16 held-out items.

PREVIEW DIAGNOSTIC -- NOT A TEST.  The protocol is fixed in
`docs/briefs/2026-09-16-step1-gray-stimulus.md` (v4, commit f915d59; v2 after review by Ark and
Zcode, v3/v3.1 after the v2 run stopped at the copy-fidelity gate, v4 after the v3.1 run stopped
there a second time).  The v2 launch (Mike's word, 2026-09-16 19:50:18Z) stopped at that gate
(README_v2_gate_stop.md); the v3.1 launch (2026-09-16 20:14:03Z) stopped at it again
(README_v31_gate_stop.md).  The v4 run was launched on Mike's explicit word in the DPC Research
chat, 2026-09-17 08:14:48Z: «@CC_windows «run step 1» (translated from Russian).

WHAT THIS SCRIPT DOES NOT DO: it never trains, never writes into
connectome-seed-data/results/flow/9991/*, never calls solver.checkpoint() or
solver.test(track_loss=True), and never registers an ablation hook (`net._state_hooks == ()` is
asserted before and after every evaluation).  The solver lives in a scratch datamate root; the six
runs' checkpoints are read with torch.load only.  Nothing under results/night2/ or results/night3/
is written.

NOTHING OF THE EVALUATION PATH IS RE-IMPLEMENTED.  `build_solver`, `chkpt_table`,
`load_checkpoint`, `hook_eval`, `per_item_eval`, `val_item_names` come from
`../../night2/diagnostics/diag1_eval_paths.py`; the seven eval_rung invariants from
`../../night2/diagnostics/rowB/rowB.py` (byte-identical to
`../../night3/diagnostics/rowB/rowB.py`, sha256 recorded for both), wrapped exactly as
`../../night3/diagnostics/ablation/ablation_night3.py:96-102`; `ablation.py` is imported only so
its sha256 can be recorded and so that the "no hook" assertion uses the same attribute the
ablation used.

The ONE thing this script adds is `per_item_eval_transformed` below: a line-for-line copy of
`diag1_eval_paths.py:176-201` `per_item_eval` in which the argument of line 191
(`solver.network.stimulus.add_input(data["lum"])`) is replaced by `transform(data["lum"], _i)`.
Everything else in the copy -- `t_pre=0.25`, `value=0.5` (:183-184), `augmentation(False)` (:187),
the decoder call (:196), the loss call (:198) -- is byte-identical.  The only other textual
difference is the loop variable `_` -> `_i` on the `for` of :188, needed to index the per-item
frame permutation of condition (d); it is recorded here and in README.md as a deviation from
"only the argument of line 191 changes".  Copy fidelity is measured, not assumed, by
--task control (brief v3.1 Sec 6): the copy with the identity transform (A) against each of FIVE
calls B_1..B_5 of D.per_item_eval on the same loaded checkpoint; the floor is the maximum
per-item |B_j - B_k| over all 10 pairs; pass iff max_k max per-item |A - B_k| <= floor, and at
iteration 0 equality must be bitwise.

v3.1 CHANGES TO THIS SCRIPT (after the v2 gate stop; conditions, the transform line and the
evaluator reuse are untouched): `copy_fidelity_control` (five-call floor, used by --task control
and --task main); --task main stops before the sweep if that control fails; --task repeat gates
max |delta loss_16| per checkpoint against 3 x the in-process floor on the 16-item mean recorded
in gray_controls.json and reports <= 1e-4 separately; --task readings implements brief Sec 7 v3 --
reading (ii) `excess_cond = L_trained,cond - L_untrained_gray`, >= 10 gain_s explodes /
<= 0.1 gain_s returns / else between (the v2 executor's provisional 3062.6 threshold is removed);
reading (iii) void when the two references lie within 0.2 gain_s.

v4 CHANGES TO THIS SCRIPT (after the v3.1 gate stop; conditions, transforms, the evaluator reuse and
the readings are untouched):
- Copy fidelity is a CODE GATE (`code_gate`, brief v4 Sec 6): the source of
  `per_item_eval_transformed` and of `D.per_item_eval` is extracted with `inspect.getsource`, and
  a unified diff is computed.  Pass iff (1) the executable body (the statements after the
  docstring) of the copy equals the original's body with exactly the two declared substitutions
  applied, at original file lines 188 (`for _, data` -> `for _i, data`) and 191
  (`add_input(data["lum"])` -> `add_input(transform(data["lum"], _i))`), and (2) the signature
  differs only by the function name and the inserted `transform` parameter (the vehicle of the
  line-191 transform).  The docstrings differ as text and are shown in the diff; they are not
  executable and are not gated.  The diff is printed and written into gray_controls.json.  Runs
  first in --task codegate / control / main, before the solver is built; failure -> stop.
- The numeric copy-vs-original comparisons (A vs five calls B_1..B_5 of D.per_item_eval, all 10
  B pairs, per-item and 16-item mean) are RECORDED, NOT GATING.  Stop only on the documented
  ceilings: per-item |A - B_k| > 1.5 x 0.0009765625 = 0.00146484375, or
  |mean(A) - mean(B_k)| > 1e-4, for any k.  At iteration 0 bitwise equality is recorded but not
  required (C3 Part B, results/diagnostics/c3/README.md: single D.per_item_eval calls at
  iteration 0 were occasionally one float64 step of the mean off); the same ceilings apply.
- --task repeat gates per cell on |delta loss_16| between the two processes <= 1e-4; per-item
  deltas and the in-process floor of each checkpoint (from gray_controls.json) are recorded next
  to the gate, not gating.

v5.1 CHANGES TO THIS SCRIPT (after the v4 run stopped at the 1e-4 mean ceiling; brief v5.1, commit
fc7239d; conditions, transforms, per_item_eval_transformed, the evaluator reuse, the code gate and
the readings logic are untouched).  Launched on Mike's explicit word in the DPC Research chat,
2026-09-17 08:37:30Z: «@CC_windows «run step 1» (v5)» (translated from Russian); v5.1 differs from v5 (b14f69f) only by
turning two single-call gates into records.
- Numeric copy/original comparison (brief v5 Sec 6): five copy calls A_1..A_5 (identity transform)
  and five original calls B_1..B_5 on the same checkpoint in the same process; the ONLY gating
  quantity is |mean(A_1..A_5) - mean(B_1..B_5)| on the 16-item mean, ceiling 1e-2 (a sanity bound,
  not a precision bound; derivation printed next to every number).  All per-item and pairwise
  numbers (B pairs, each A_i vs each B_k) are recorded, not gating.
- P0 (brief v5 Sec 6): mean of five calls of condition (c) minus the stored val_loss, ceiling 1e-3,
  applied in the control (A_1..A_5) and to the real cell (mean of five) of every one of the 12
  checkpoints in the sweep.  `per_item_mean - hook_eval()` is RECORDED, not gating (v5.1).
- Iteration 0: bitwise equality RECORDED, not required (v5.1); the same ceilings apply.
- Sweep (both processes): each of the 48 cells is the mean of five copy calls; per-call 16-item
  means and per-item vectors are recorded in the json; the csv's `loss_16` is the mean of the five
  calls' 16-item means and its per-item columns are the per-item means over the five calls.
- --task repeat gates per cell on |delta| of that five-call mean between the two processes <= 1e-2.
- Stops: crash; NaN/inf in any call; code-gate failure; any of the three ceilings; (run-dir file
  change is checked outside this script by listing diff).
"""

import os
import sys

# Same two environment variables, set the same way and in the same place as
# night/run_individual.py:46-49, diag1_eval_paths.py:27-32, ablation.py:22-26,
# ablation_night3.py:30-33.
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
os.environ.setdefault(
    "FLYVIS_ROOT_DIR", "C:/Users/mikha/Documents/dpc-research/connectome-seed-data"
)

CS = "C:/Users/mikha/Documents/dpc-research/connectome-seed"
DIAG_DIR = os.path.join(CS, "results/night2/diagnostics")
N2_ABL = os.path.join(DIAG_DIR, "ablation")
N2_ROWB = os.path.join(DIAG_DIR, "rowB")
N3_ROWB = os.path.join(CS, "results/night3/diagnostics/rowB")
N3_ABL = os.path.join(CS, "results/night3/diagnostics/ablation")
sys.path.insert(0, DIAG_DIR)
sys.path.insert(0, N2_ABL)
sys.path.insert(0, N2_ROWB)

import argparse
import ast
import difflib
import hashlib
import inspect
import json
import textwrap
import time
from pathlib import Path

import numpy as np
import torch

import diag1_eval_paths as D          # the evaluator, reused verbatim
import ablation as ABL                # imported for provenance + the no-hook attribute
import rowB as RB                     # the seven eval_rung invariants, reused verbatim

# ---------------------------------------------------------------- fixed protocol constants
RUNS6 = {"000": "seed0", "900": "seed0prime", "001": "seed1",
         "002": "seed2", "003": "seed3", "004": "seed4"}
LABELS6 = ["seed0", "seed0prime", "seed1", "seed2", "seed3", "seed4"]
# checkpoint index -> solver iteration, rowB.py:56-57 NAMED_CHKPTS; asserted at run time
CHKPTS = {0: 0, 71: 250008}                      # chkpt_00000 / chkpt_00071
CHKPT_NAMES = {0: "chkpt_00000", 71: "chkpt_00071"}
CONDITIONS = ["real", "gray", "zero", "shuffled"]
GRAY_VALUE = 0.5                                 # brief Sec 4
ZERO_VALUE = 0.0
SHUFFLE_SEED = 20260916                          # brief Sec 1/3: fixed, recorded here
P0_TOL = 1e-3                                    # brief Sec 6 v5: mean of five calls vs stored
FRESH_PROCESS_TOL = 1e-2                         # brief Sec 6 v5: per cell, mean of five calls
N_FLOOR_CALLS = 5                                # brief Sec 6 v5: five original calls B_1..B_5
N_COPY_CALLS = 5                                 # brief Sec 6 v5: five copy calls per quantity
COPY_MEAN_CEILING = 1e-2                         # brief Sec 6 v5: |mean(A1..A5) - mean(B1..B5)|
BRIEF_CHKPT_00071_SPREAD = 8.6e-05               # brief Sec 6 v4/v5: stated next to the repeat gate
COPY_CEILING_TEXT = (
    "ceiling 1e-2 on |mean(A_1..A_5) - mean(B_1..B_5)| (16-item mean) -- a SANITY bound, not a "
    "precision bound (Ark): ~50x above all measured noise on this comparison to date (<= 2.0e-4 "
    "between processes, C3 Part B, results/diagnostics/c3/README.md) and ~500x below the narrowest "
    "pre-registered reading band (0.1 * gain_s ~ 5-6, brief Sec 7); catches a wrong copy "
    "(checkpoint, data, index), an error in units")
P0_CEILING_TEXT = (
    "ceiling 1e-3 on |mean of five condition-(c) calls - stored val_loss| -- the largest value on "
    "record on this path is 7e-05 (brief Sec 6 v5)")
FRESH_CEILING_TEXT = (
    "ceiling 1e-2 per cell on |delta| between the two processes of the five-call mean (16-item "
    "mean) -- same derivation as the copy/original ceiling: ~50x above measured noise (<= 2.0e-4 "
    "between processes, C3 Part B), ~500x below 0.1 * gain_s ~ 5-6 (brief Sec 6 v5)")
# brief Sec 6 v4 / Sec 3 / Sec 9.10: the two declared differences of the copy, by original line
DECLARED_SUBSTITUTIONS = {
    188: ("for _, data in enumerate(dataloader):",
          "for _i, data in enumerate(dataloader):"),
    191: ('solver.network.stimulus.add_input(data["lum"])',
          'solver.network.stimulus.add_input(transform(data["lum"], _i))'),
}
BAND_FRACTION = 0.1                              # brief Sec 7 (i)/(iii): 0.1 * gain_s
EXPLODE_MULT = 10.0                              # brief Sec 7 (ii) v3: excess >= 10 gain_s
RETURN_FRACTION = 0.1                            # brief Sec 7 (ii) v3: excess <= 0.1 gain_s
VOID_FRACTION = 0.2                              # brief Sec 7 (iii) v3: refs within 0.2 gain_s
# brief Sec 7 (ii), pre-registered reference numbers
PREREG_SEED2_R2_DELTA = 21157.5
PREREG_SEED2_R1R8_CLAMP_EXCESS = 30626.0

STATUS = ("PREVIEW DIAGNOSTIC -- NOT A TEST (gray-stimulus control, brief "
          "docs/briefs/2026-09-16-step1-gray-stimulus.md v5.1; n=6 individuals)")


def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


SCRIPT_HASHES = {
    "results/diagnostics/gray/gray_stimulus.py": sha256_file(__file__),
    "results/night2/diagnostics/diag1_eval_paths.py": sha256_file(
        os.path.join(DIAG_DIR, "diag1_eval_paths.py")),
    "results/night2/diagnostics/ablation/ablation.py": sha256_file(
        os.path.join(N2_ABL, "ablation.py")),
    "results/night2/diagnostics/rowB/rowB.py": sha256_file(
        os.path.join(N2_ROWB, "rowB.py")),
    "results/night3/diagnostics/rowB/rowB.py": sha256_file(
        os.path.join(N3_ROWB, "rowB.py")),
    "results/night3/diagnostics/ablation/ablation_night3.py": sha256_file(
        os.path.join(N3_ABL, "ablation_night3.py")),
}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--task", required=True,
                   choices=["codegate", "control", "floor", "main", "repeat", "readings"])
    p.add_argument("--out-dir", required=True)
    p.add_argument("--netdir-root", required=False)
    return p.parse_args()


# ---------------------------------------------------------------- the four input conditions
def frame_permutation(item_index, n_frames):
    """Fixed per-item permutation of the frame axis (condition d).

    Derived from (SHUFFLE_SEED, item_index) alone -- not from a global RNG stream -- so it is
    the same permutation in every process, for every run and every checkpoint.
    """
    return np.random.default_rng([SHUFFLE_SEED, int(item_index)]).permutation(int(n_frames))


def make_transform(condition):
    if condition == "real":
        return lambda lum, i: lum
    if condition == "gray":
        return lambda lum, i: torch.full_like(lum, GRAY_VALUE)
    if condition == "zero":
        return lambda lum, i: torch.zeros_like(lum)
    if condition == "shuffled":
        def _t(lum, i):
            perm = frame_permutation(i, lum.shape[1])
            return lum[:, torch.as_tensor(np.asarray(perm), device=lum.device)]
        return _t
    raise ValueError(condition)


CONDITION_DEFS = {
    "real": ("condition (c): the unmodified data['lum'] -- the identity transform; "
             "diag1_eval_paths.py:191 unchanged"),
    "gray": ("condition (a): torch.full_like(data['lum'], 0.5) -- every input element 0.5, "
             "flyvis's own resting/background value (network.py:548-586, moving_bar.py:194)"),
    "zero": ("condition (b): torch.zeros_like(data['lum']) -- every input element 0.0, "
             "full-field black; NOT the resting state"),
    "shuffled": ("condition (d): data['lum'] with its frame axis (dim 1) permuted by "
                 "numpy.random.default_rng([SHUFFLE_SEED, item_index]).permutation(n_frames), "
                 "SHUFFLE_SEED=%d; content and per-frame image statistics preserved, temporal "
                 "ordering destroyed; the target is NOT permuted" % SHUFFLE_SEED),
}


# ---------------------------------------------------------------- the copied evaluator
def per_item_eval_transformed(solver, transform, t_pre=0.25):
    """diag1_eval_paths.py:176-201 `per_item_eval`, copied line for line; the ONLY changes are
    the argument of :191 (`data["lum"]` -> `transform(data["lum"], _i)`) and the loop variable
    `_` -> `_i` on :188."""
    task, dataloader = solver.task, solver.task.val_data
    solver._eval()
    solver.scheduler(solver.iteration)  # solver.py:504
    initial_state = solver.network.steady_state(
        t_pre=t_pre, dt=task.dataset.dt, batch_size=dataloader.batch_size, value=0.5)
    losses = {t: [] for t in task.dataset.tasks}
    with torch.no_grad():
        with task.dataset.augmentation(False):
            for _i, data in enumerate(dataloader):
                n_samples, n_frames, _, _ = data["lum"].shape
                solver.network.stimulus.zero(n_samples, n_frames)
                solver.network.stimulus.add_input(transform(data["lum"], _i))
                activity = solver.network(solver.network.stimulus(), task.dataset.dt,
                                          state=initial_state)
                for t in task.dataset.tasks:
                    y = data[t]
                    y_est = solver.decoder[t](activity)
                    losses[t].append(
                        task.loss(y_est, y, t, **data.get("loss_kwargs", {}))
                        .detach().cpu().item())
    solver._train()
    return losses


# ---------------------------------------------------------------- v4 code gate
def _split_function_source(fn):
    """(absolute start line, def-header lines, docstring lines, body lines) of `fn`, from
    inspect.getsourcelines; the split points come from the AST, not from text matching."""
    lines, start = inspect.getsourcelines(fn)
    tree = ast.parse(textwrap.dedent("".join(lines)))
    fdef = tree.body[0]
    assert isinstance(fdef, ast.FunctionDef), type(fdef)
    first = fdef.body[0]
    has_doc = (isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant)
               and isinstance(first.value.value, str))
    assert has_doc, fn.__name__
    doc_first = first.lineno - 1                 # 0-based index into `lines`
    doc_last = first.end_lineno - 1
    body_first = fdef.body[1].lineno - 1
    assert body_first == doc_last + 1, (fn.__name__, body_first, doc_last)
    return (start, lines[:doc_first], lines[doc_first:doc_last + 1], lines[body_first:],
            body_first)


def code_gate():
    """Brief v4 Sec 6: copy fidelity as a code diff, not a number.  Writes nothing."""
    orig_src_lines, orig_start = inspect.getsourcelines(D.per_item_eval)
    copy_src_lines, copy_start = inspect.getsourcelines(per_item_eval_transformed)
    orig_file = inspect.getsourcefile(D.per_item_eval)
    copy_file = inspect.getsourcefile(per_item_eval_transformed)
    full_diff = list(difflib.unified_diff(
        orig_src_lines, copy_src_lines,
        fromfile=f"diag1_eval_paths.py:per_item_eval (lines {orig_start}-"
                 f"{orig_start + len(orig_src_lines) - 1})",
        tofile=f"gray_stimulus.py:per_item_eval_transformed (lines {copy_start}-"
               f"{copy_start + len(copy_src_lines) - 1})"))

    o_start, o_hdr, o_doc, o_body, o_body_off = _split_function_source(D.per_item_eval)
    c_start, c_hdr, c_doc, c_body, c_body_off = _split_function_source(per_item_eval_transformed)
    body_diff = list(difflib.unified_diff(
        o_body, c_body,
        fromfile=f"diag1_eval_paths.py:per_item_eval body (lines {o_start + o_body_off}-"
                 f"{o_start + o_body_off + len(o_body) - 1})",
        tofile=f"gray_stimulus.py:per_item_eval_transformed body (lines "
               f"{c_start + c_body_off}-{c_start + c_body_off + len(c_body) - 1})"))

    # (1) body: the original body with exactly the declared substitutions applied must equal the
    #     copy's body, byte for byte (indentation included)
    expected = list(o_body)
    applied = {}
    for abs_line, (old, new) in DECLARED_SUBSTITUTIONS.items():
        idx = abs_line - (o_start + o_body_off)
        ok_idx = 0 <= idx < len(expected)
        line = expected[idx] if ok_idx else ""
        ok_old = ok_idx and line.strip() == old
        if ok_old:
            indent = line[:len(line) - len(line.lstrip())]
            expected[idx] = indent + new + "\n"
        applied[str(abs_line)] = {"original_line_text": line.rstrip("\n"),
                                  "declared_old": old, "declared_new": new,
                                  "original_line_matches_declared_old": bool(ok_old)}
    all_old_match = all(v["original_line_matches_declared_old"] for v in applied.values())
    body_equal = bool(all_old_match and expected == list(c_body))
    n_changed = sum(1 for a_, b_ in zip(o_body, c_body) if a_ != b_) if len(o_body) == len(
        c_body) else None

    # (2) signature: only the name and the inserted `transform` parameter differ
    so = inspect.signature(D.per_item_eval)
    sc = inspect.signature(per_item_eval_transformed)
    po = [(p.name, p.kind, p.default) for p in so.parameters.values()]
    pc = [(p.name, p.kind, p.default) for p in sc.parameters.values()
          if p.name != "transform"]
    sig_ok = bool(po == pc and "transform" in sc.parameters
                  and len(sc.parameters) == len(so.parameters) + 1)

    passed = bool(body_equal and sig_ok and n_changed == len(DECLARED_SUBSTITUTIONS))
    return {
        "rule": ("brief v4 Sec 6: the copied per_item_eval must differ from "
                 "diag1_eval_paths.py's per_item_eval only in the declared lines -- the "
                 "transform on the add_input argument (line 191) and the loop-variable rename "
                 "`_` -> `_i` (line 188); any other difference -> stop"),
        "operationalisation": (
            "pass iff (1) the executable body (statements after the docstring, located via "
            "ast) of the copy equals the original body with exactly the two declared "
            "substitutions applied at original lines 188 and 191, byte for byte, and exactly "
            "2 body lines differ; and (2) inspect.signature differs only by the function name "
            "and the inserted `transform` parameter.  The def line and the docstring necessarily "
            "differ as text; they are shown in full_unified_diff and not gated"),
        "original_file": orig_file, "copy_file": copy_file,
        "original_lines": [orig_start, orig_start + len(orig_src_lines) - 1],
        "copy_lines": [copy_start, copy_start + len(copy_src_lines) - 1],
        "original_signature": f"per_item_eval{so}",
        "copy_signature": f"per_item_eval_transformed{sc}",
        "declared_substitutions": applied,
        "n_body_lines_original": len(o_body), "n_body_lines_copy": len(c_body),
        "n_body_lines_differing": n_changed,
        "body_equals_original_with_declared_substitutions": body_equal,
        "signature_differs_only_by_name_and_transform_param": sig_ok,
        "body_unified_diff": "".join(body_diff),
        "full_unified_diff": "".join(full_diff),
        "code_gate_pass": passed,
    }


def run_code_gate():
    cg = code_gate()
    print("CODE GATE BODY DIFF\n" + cg["body_unified_diff"], flush=True)
    print("CODE GATE FULL DIFF\n" + cg["full_unified_diff"], flush=True)
    print("CODE GATE", json.dumps({k: v for k, v in cg.items()
                                   if k not in ("body_unified_diff", "full_unified_diff")}),
          flush=True)
    print("CODE GATE VERDICT", "PASS" if cg["code_gate_pass"] else "FAIL", flush=True)
    return cg


def eval_condition(solver, condition):
    """One 16-item evaluation under one input condition, wrapped in the seven eval_rung
    invariants (ablation_night3.py:96-102) and the no-ablation-hook assertion
    (ablation.py:104, 111)."""
    net = solver.network
    assert net._state_hooks == (), net._state_hooks
    before = RB.snapshot_state(solver)
    t0 = time.perf_counter()
    losses = per_item_eval_transformed(solver, make_transform(condition))
    wall = time.perf_counter() - t0
    inv = RB.invariants(before, RB.snapshot_state(solver))
    assert net._state_hooks == (), net._state_hooks
    if not all(inv.values()):
        print("INVARIANT FAILURE", condition, json.dumps(inv), flush=True)
        raise SystemExit("eval_rung invariant False -- stopping (brief Sec 10.9)")
    arr = np.array(losses["flow"], dtype=np.float64)
    require_finite(arr, f"copy call, condition={condition}")
    return arr, inv, wall


def require_finite(arr, what):
    """Brief Sec 6 v5 Stops: NaN/inf -> stop."""
    if not bool(np.all(np.isfinite(arr))):
        print("NAN/INF STOP", what, [repr(float(x)) for x in arr], flush=True)
        raise SystemExit(f"NaN/inf in {what} -- stopping (brief Sec 6 v5 Stops)")


def eval_cell(solver, condition):
    """Brief Sec 6 v5: one cell = the mean of N_COPY_CALLS calls of the copy under one
    condition; every call's per-item vector, invariants and wall are kept."""
    calls, invs, walls = [], [], []
    for _c in range(N_COPY_CALLS):
        items, inv, wall = eval_condition(solver, condition)
        calls.append(items)
        invs.append(inv)
        walls.append(wall)
    C = np.stack(calls)                                  # (5, 16)
    call_means = C.mean(axis=1)                          # 16-item mean of each call
    return {
        "calls": C,
        "call_means": call_means,
        "loss_16": float(call_means.mean()),             # mean of the five 16-item means
        "per_item": C.mean(axis=0),                      # per-item mean over the five calls
        "max_minus_min_loss_16": float(call_means.max() - call_means.min()),
        "invariants": invs, "walls": walls,
    }


def load_named(solver, run, chkpt_index):
    """rowB.py:287-295 load_named, reused in spirit: the index -> iteration mapping is asserted
    against chkpt_table at run time, never assumed."""
    tab = D.chkpt_table(run)
    assert len(tab) == 72, (run, len(tab))
    hit = [r for r in tab if r[0] == chkpt_index]
    assert len(hit) == 1, (run, chkpt_index)
    ci, stored_it, solver_it, path = hit[0]
    assert solver_it == CHKPTS[chkpt_index], (chkpt_index, solver_it)
    assert path.name == CHKPT_NAMES[chkpt_index], (path.name, chkpt_index)
    info = D.load_checkpoint(solver, path)
    return solver_it, path, info


def copy_fidelity_control(solver, run, ci):
    """Brief Sec 6 v5.1: copy-vs-original, mean of five vs mean of five; P0 on the mean of five.

    A_1..A_5 = five calls of the copy with the identity transform; B_1..B_5 = five calls of the
    ORIGINAL D.per_item_eval; same loaded checkpoint, same process.  GATING: |mean(A_1..A_5) -
    mean(B_1..B_5)| on the 16-item mean <= COPY_MEAN_CEILING (1e-2), and P0 |mean(A_1..A_5) -
    stored val_loss| <= P0_TOL (1e-3).  RECORDED, not gating: all 10 B pairs and all 10 A pairs
    (per-item max, 16-item mean), each A_i vs each B_k (per-item max, mean diff, bitwise),
    iteration-0 bitwise equality, `per_item_mean - hook_eval()`, and the raw per-item vectors.
    """
    solver_it, path, info = load_named(solver, run, ci)
    net = solver.network
    assert net._state_hooks == (), net._state_hooks
    A = []
    for _k in range(N_COPY_CALLS):
        a = np.array(per_item_eval_transformed(solver, make_transform("real"))["flow"],
                     dtype=np.float64)                    # the copy, identity transform
        assert net._state_hooks == (), net._state_hooks
        require_finite(a, f"control copy call A{_k + 1} {run}@{solver_it}")
        A.append(a)
    A = np.stack(A)
    B = []
    for _k in range(N_FLOOR_CALLS):
        b = np.array(D.per_item_eval(solver)["flow"], dtype=np.float64)   # the original
        assert net._state_hooks == (), net._state_hooks
        require_finite(b, f"control original call B{_k + 1} {run}@{solver_it}")
        B.append(b)
    B = np.stack(B)
    hook = D.hook_eval(solver)
    assert net._state_hooks == (), net._state_hooks
    require_finite(np.array([hook]), f"hook_eval {run}@{solver_it}")

    pairs = [(j, k) for j in range(N_FLOOR_CALLS) for k in range(j + 1, N_FLOOR_CALLS)]
    assert len(pairs) == 10, len(pairs)
    a_means = A.mean(axis=1)
    b_means = B.mean(axis=1)
    mean_A = float(a_means.mean())                        # mean of the five 16-item means
    mean_B = float(b_means.mean())
    gate_diff = mean_A - mean_B
    gate_ok = bool(abs(gate_diff) <= COPY_MEAN_CEILING)

    b_pair_item = {f"B{j + 1}-B{k + 1}": float(np.max(np.abs(B[j] - B[k]))) for j, k in pairs}
    b_pair_mean = {f"B{j + 1}-B{k + 1}": float(abs(float(b_means[j]) - float(b_means[k])))
                   for j, k in pairs}
    a_pair_item = {f"A{j + 1}-A{k + 1}": float(np.max(np.abs(A[j] - A[k]))) for j, k in pairs}
    a_pair_mean = {f"A{j + 1}-A{k + 1}": float(abs(float(a_means[j]) - float(a_means[k])))
                   for j, k in pairs}
    ab_item = {f"A{i + 1}-B{k + 1}": float(np.max(np.abs(A[i] - B[k])))
               for i in range(N_COPY_CALLS) for k in range(N_FLOOR_CALLS)}
    ab_mean = {f"A{i + 1}-B{k + 1}": float(a_means[i]) - float(b_means[k])
               for i in range(N_COPY_CALLS) for k in range(N_FLOOR_CALLS)}
    ab_bitwise = {f"A{i + 1}==B{k + 1}": bool(np.array_equal(A[i], B[k]))
                  for i in range(N_COPY_CALLS) for k in range(N_FLOOR_CALLS)}
    b_pair_bitwise = {f"B{j + 1}==B{k + 1}": bool(np.array_equal(B[j], B[k])) for j, k in pairs}
    a_pair_bitwise = {f"A{j + 1}==A{k + 1}": bool(np.array_equal(A[j], A[k])) for j, k in pairs}

    p0 = mean_A - info["stored_val_loss"]
    p0_ok = bool(abs(p0) <= P0_TOL)
    p0h = mean_A - hook
    rec = {
        "run": run, "chkpt": path.name, "solver_iteration": solver_it,
        "n_copy_calls": N_COPY_CALLS, "n_original_calls": N_FLOOR_CALLS,
        # ---- GATE 1: copy vs original, mean of five vs mean of five
        "gate_copy_vs_original_rule": COPY_CEILING_TEXT,
        "copy_means_A1_to_A5": [repr(float(x)) for x in a_means],
        "original_means_B1_to_B5": [repr(float(x)) for x in b_means],
        "mean_of_five_copy_A": repr(mean_A),
        "mean_of_five_original_B": repr(mean_B),
        "gate_mean_A_minus_mean_B": repr(gate_diff),
        "gate_abs_mean_A_minus_mean_B": repr(abs(gate_diff)),
        "gate_ceiling": repr(COPY_MEAN_CEILING),
        "gate_copy_vs_original_pass": gate_ok,
        # ---- recorded, not gating
        "recorded_B_pairs_max_abs_per_item": {k: repr(v) for k, v in b_pair_item.items()},
        "recorded_B_pairs_abs_mean_diff": {k: repr(v) for k, v in b_pair_mean.items()},
        "recorded_B_floor_max_abs_per_item_over_10_pairs": repr(max(b_pair_item.values())),
        "recorded_B_floor_max_abs_mean_over_10_pairs": repr(max(b_pair_mean.values())),
        "recorded_A_pairs_max_abs_per_item": {k: repr(v) for k, v in a_pair_item.items()},
        "recorded_A_pairs_abs_mean_diff": {k: repr(v) for k, v in a_pair_mean.items()},
        "recorded_A_spread_max_abs_per_item_over_10_pairs": repr(max(a_pair_item.values())),
        "recorded_A_spread_max_abs_mean_over_10_pairs": repr(max(a_pair_mean.values())),
        "recorded_Ai_vs_Bk_max_abs_per_item": {k: repr(v) for k, v in ab_item.items()},
        "recorded_Ai_vs_Bk_mean_diff": {k: repr(v) for k, v in ab_mean.items()},
        "recorded_Ai_vs_Bk_max_abs_per_item_overall": repr(max(ab_item.values())),
        "recorded_Ai_vs_Bk_max_abs_mean_diff_overall": repr(max(abs(v) for v in ab_mean.values())),
        "recorded_Ai_vs_Bk_bitwise_equal": ab_bitwise,
        "recorded_A_pairs_bitwise_equal": a_pair_bitwise,
        "recorded_B_pairs_bitwise_equal": b_pair_bitwise,
        "recorded_all_A_and_B_bitwise_equal": bool(
            all(ab_bitwise.values()) and all(a_pair_bitwise.values())
            and all(b_pair_bitwise.values())),
        "recorded_iteration0_bitwise_note": (
            "brief v5.1 Sec 6: at iteration 0 bitwise equality is recorded, not required; the "
            "ceilings apply there too"),
        "copy_A_per_item": [[repr(float(x)) for x in A[i]] for i in range(N_COPY_CALLS)],
        "original_B_per_item": [[repr(float(x)) for x in B[k]] for k in range(N_FLOOR_CALLS)],
        # ---- GATE 2: P0
        "gate_P0_rule": P0_CEILING_TEXT,
        "stored_checkpoint_val_loss": repr(info["stored_val_loss"]),
        "P0_mean_of_five_copy_calls": repr(mean_A),
        "gate_P0_mean_minus_stored": repr(p0),
        "gate_P0_ceiling": repr(P0_TOL),
        "gate_P0_pass": p0_ok,
        "recorded_P0_hook_path_value_single_call": repr(hook),
        "recorded_P0_mean_of_five_minus_hook": repr(p0h),
        "recorded_P0_mean_of_five_minus_hook_within_sanity_bound_1e-3": bool(abs(p0h) <= P0_TOL),
        "recorded_P0_hook_note": (
            "brief v5.1 Sec 6: per_item_mean - hook_eval() is recorded, not gating (C3 Part B "
            "measured up to 1.435e-4 on the same weights); its sanity bound is the P0 ceiling 1e-3"),
    }
    print(f"CONTROL GATE {run}@{solver_it} |mean(A1..A5) - mean(B1..B5)| = {abs(gate_diff)!r} "
          f"[{COPY_CEILING_TEXT}] -> {'PASS' if gate_ok else 'FAIL'}", flush=True)
    print(f"CONTROL P0 {run}@{solver_it} mean(A1..A5) - stored = {p0!r} "
          f"[{P0_CEILING_TEXT}] -> {'PASS' if p0_ok else 'FAIL'}", flush=True)
    print(f"CONTROL RECORDED {run}@{solver_it} mean(A1..A5) - hook_eval() = {p0h!r} "
          f"(recorded, not gating; sanity bound 1e-3); all A/B bitwise equal = "
          f"{rec['recorded_all_A_and_B_bitwise_equal']}", flush=True)
    return rec, bool(gate_ok and p0_ok)


def item_short(n):
    """rowB.py:296-297."""
    return n.replace("sequence_", "")


# ---------------------------------------------------------------- constant-output null
def constant_output_null(solver):
    """Brief Sec 6: the loss a constant prediction would incur on the 16 items, from the targets
    alone, with the evaluator's own `task.loss` (l2norm, flyvis/task/objectives.py:10-22).

    (i) per-item mean of y_gt over frames and hexals (the best possible constant per item) --
        this is `constant_output_null`;
    (ii) zero against y_gt -- weaker, illustrative only, NOT constant_output_null.
    """
    task, dataloader = solver.task, solver.task.val_data
    per_item_mean, per_item_zero = [], []
    with torch.no_grad():
        with task.dataset.augmentation(False):
            for _i, data in enumerate(dataloader):
                for t in task.dataset.tasks:
                    y = data[t]
                    # (i) best possible constant: the per-item mean over frames (dim 1) and
                    #     hexals (dim 3), kept per flow component (dim 2)
                    y_mean = y.mean(dim=(1, 3), keepdim=True).expand_as(y)
                    per_item_mean.append(
                        task.loss(y_mean, y, t, **data.get("loss_kwargs", {}))
                        .detach().cpu().item())
                    # (ii) zero
                    per_item_zero.append(
                        task.loss(torch.zeros_like(y), y, t, **data.get("loss_kwargs", {}))
                        .detach().cpu().item())
    m = np.array(per_item_mean, dtype=np.float64)
    z = np.array(per_item_zero, dtype=np.float64)
    return {
        "definition_i_per_item_mean": (
            "l2norm(y_gt.mean(dim=(1,3),keepdim=True).expand_as(y_gt), y_gt) via task.loss, "
            "16-item mean -- the tighter, best-possible-constant comparator"),
        "definition_ii_zero": (
            "l2norm(zeros_like(y_gt), y_gt) via task.loss, 16-item mean -- weaker, "
            "illustrative only, NOT constant_output_null"),
        "constant_output_null": repr(float(m.mean())),
        "constant_output_null_per_item": [repr(float(x)) for x in m],
        "zero_prediction_null": repr(float(z.mean())),
        "zero_prediction_null_per_item": [repr(float(x)) for x in z],
    }


# ---------------------------------------------------------------- csv
def write_losses_csv(path, rows, item_names, sha):
    hdr = (["run", "label", "checkpoint_iter", "condition", "loss_16"]
           + [f"loss_item_{item_short(n)}" for n in item_names])
    lines = ["# " + STATUS,
             f"# script_sha256={sha}",
             ",".join(hdr)]
    for r in rows:
        line = [r["run"], r["label"], str(r["checkpoint_iter"]), r["condition"],
                repr(float(r["loss_16"]))]
        line += [repr(float(x)) for x in r["per_item"]]
        lines.append(",".join(line))
    Path(path).write_text("\n".join(lines) + "\n")


def read_losses_csv(path):
    lines = [ln for ln in Path(path).read_text(encoding="utf-8").strip().split("\n")
             if not ln.startswith("#")]
    hdr = lines[0].split(",")
    out = {}
    for ln in lines[1:]:
        parts = ln.split(",")
        assert len(parts) == len(hdr), (len(parts), len(hdr))
        row = dict(zip(hdr, parts))
        key = (row["label"], int(row["checkpoint_iter"]), row["condition"])
        assert key not in out, f"duplicate key {key!r} -- refusing"
        out[key] = {"run": row["run"], "loss_16": float(row["loss_16"]),
                    "per_item": np.array([float(row[c]) for c in hdr[5:]],
                                         dtype=np.float64)}
    return out


# ---------------------------------------------------------------- the sweep
def sweep(solver, item_names, print_tag):
    """All 48 cells: 6 runs x 2 checkpoints x 4 conditions; each cell the mean of five copy
    calls (brief Sec 6 v5), every call recorded."""
    rows, per_cell = [], {}
    first_real_wall = None
    for run, label in RUNS6.items():
        for ci in sorted(CHKPTS):
            solver_it, path, info = load_named(solver, run, ci)
            for cond in CONDITIONS:
                cell = eval_cell(solver, cond)
                if cond == "real" and first_real_wall is None:
                    first_real_wall = cell["walls"][0]
                mean = cell["loss_16"]
                rows.append({"run": run, "label": label, "checkpoint_iter": solver_it,
                             "condition": cond, "loss_16": mean, "per_item": cell["per_item"]})
                per_cell[(label, solver_it, cond)] = {
                    "run": run, "chkpt": path.name,
                    "stored_checkpoint_val_loss": repr(info["stored_val_loss"]),
                    "n_calls": N_COPY_CALLS,
                    "loss_16_mean_of_five_calls": repr(mean),
                    "loss_16_per_call": [repr(float(x)) for x in cell["call_means"]],
                    "loss_16_max_minus_min_over_calls": repr(cell["max_minus_min_loss_16"]),
                    "per_item_mean_over_calls": [repr(float(x)) for x in cell["per_item"]],
                    "per_item_per_call": [[repr(float(x)) for x in cell["calls"][c]]
                                          for c in range(N_COPY_CALLS)],
                    "wall_s_per_call": [repr(w) for w in cell["walls"]],
                    "eval_rung_invariants_per_call": cell["invariants"],
                }
                if cond == "real":
                    p0 = mean - info["stored_val_loss"]
                    per_cell[(label, solver_it, cond)]["P0_mean_of_five_minus_stored"] = repr(p0)
                    per_cell[(label, solver_it, cond)]["P0_pass_le_1e-3"] = bool(
                        abs(p0) <= P0_TOL)
                print(print_tag, label, solver_it, cond, "mean_of_5", repr(mean),
                      "max-min", repr(cell["max_minus_min_loss_16"]),
                      "calls", [repr(float(x)) for x in cell["call_means"]],
                      "wall_5", repr(sum(cell["walls"])), flush=True)
                if cond == "real":
                    print(print_tag, "P0", label, solver_it, "mean_of_5 - stored", repr(p0),
                          f"[{P0_CEILING_TEXT}]", "PASS" if abs(p0) <= P0_TOL else "FAIL",
                          flush=True)
    return rows, per_cell, first_real_wall


# ---------------------------------------------------------------- tasks
def task_codegate(a):
    """Brief v4 Sec 6 code gate only; no solver, no GPU work.  Writes nothing."""
    return 0 if run_code_gate()["code_gate_pass"] else 3


def task_control(a):
    """Brief Sec 6 v5.1, step 1: code gate, then copy/original mean-of-five vs mean-of-five
    (ceiling 1e-2) + P0 on the mean of five (ceiling 1e-3).  Writes nothing."""
    if not run_code_gate()["code_gate_pass"]:
        return 3
    solver = D.build_solver(Path(a.netdir_root))
    import flyvis
    print("CONTROL META", json.dumps({
        "flyvis": flyvis.__version__, "torch": torch.__version__,
        "python": sys.version.split()[0],
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "device": str(flyvis.device), "netdir": str(solver.dir.path),
        "pid": os.getpid(),
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}), flush=True)
    ok = True
    for run in ("000",):
        for ci in sorted(CHKPTS):
            rec, passed = copy_fidelity_control(solver, run, ci)
            print("CONTROL", json.dumps(rec), flush=True)
            ok = ok and passed
    print("CONTROL VERDICT", "PASS" if ok else "FAIL", flush=True)
    return 0 if ok else 3


def task_floor(a):
    """Diagnosis of a --task control failure, added 2026-09-16 after the step-1 gate did not
    pass bitwise at chkpt_00071.  Writes nothing.

    5 repeats of D.per_item_eval (the ORIGINAL, no copy involved) and 5 repeats of the copy with
    the identity transform, interleaved, at both checkpoints of run 000.  If the original's
    repeat-to-repeat spread equals the copy-vs-original spread, the brief's "exactly equal"
    control is unsatisfiable at that checkpoint by a property of the evaluator, not of the copy.
    """
    solver = D.build_solver(Path(a.netdir_root))
    import flyvis
    print("FLOOR META", json.dumps({
        "flyvis": flyvis.__version__, "torch": torch.__version__,
        "python": sys.version.split()[0],
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "device": str(flyvis.device), "pid": os.getpid(),
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}), flush=True)
    for ci in sorted(CHKPTS):
        solver_it, path, info = load_named(solver, "000", ci)
        orig, copy = [], []
        for _ in range(5):
            assert solver.network._state_hooks == ()
            orig.append(np.array(D.per_item_eval(solver)["flow"], dtype=np.float64))
            copy.append(np.array(
                per_item_eval_transformed(solver, make_transform("real"))["flow"],
                dtype=np.float64))
        O = np.stack(orig)
        C = np.stack(copy)

        def spread(M):
            return float(np.max(np.abs(M[:, None, :] - M[None, :, :])))

        def cross(A, B):
            return float(np.max(np.abs(A[:, None, :] - B[None, :, :])))

        rec = {
            "run": "000", "chkpt": path.name, "solver_iteration": solver_it,
            "stored_checkpoint_val_loss": repr(info["stored_val_loss"]),
            "n_repeats_each": 5,
            "original_vs_original_max_abs_per_item": repr(spread(O)),
            "copy_vs_copy_max_abs_per_item": repr(spread(C)),
            "copy_vs_original_max_abs_per_item": repr(cross(C, O)),
            "original_means": [repr(float(x)) for x in O.mean(axis=1)],
            "copy_means": [repr(float(x)) for x in C.mean(axis=1)],
            "original_mean_spread": repr(float(O.mean(axis=1).max() - O.mean(axis=1).min())),
            "copy_mean_spread": repr(float(C.mean(axis=1).max() - C.mean(axis=1).min())),
            "mean_of_means_copy_minus_original": repr(
                float(C.mean() - O.mean())),
            "n_distinct_original_means": len(set(O.mean(axis=1).tolist())),
            "n_distinct_copy_means": len(set(C.mean(axis=1).tolist())),
            "any_copy_bitwise_equal_to_any_original": bool(
                any(np.array_equal(c, o) for c in C for o in O)),
            "n_copy_original_bitwise_pairs": int(
                sum(1 for c in C for o in O if np.array_equal(c, o))),
        }
        print("FLOOR", json.dumps(rec), flush=True)
    return 0


def task_main(a):
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    t_start = time.perf_counter()
    cg = run_code_gate()
    if not cg["code_gate_pass"]:
        print("CODE GATE FAIL (in --task main) -- stopping before the solver is built; "
              "nothing written", flush=True)
        return 3
    solver = D.build_solver(Path(a.netdir_root))
    import flyvis
    item_names = D.val_item_names(solver)
    assert len(item_names) == 16, item_names
    n2_meta = json.loads(
        (Path(N2_ABL) / "ablation_controls.json").read_text())["meta"]
    assert n2_meta["val_items"] == item_names, "evaluation set differs from night 2"

    meta = {
        "status": STATUS,
        "brief": ("docs/briefs/2026-09-16-step1-gray-stimulus.md (v5.1, commit fc7239d; v5.1 "
                  "differs from v5, b14f69f, only by turning two single-call gates into records: "
                  "per_item_mean - hook_eval() and iteration-0 bitwise equality)"),
        "launch": ("Mike's explicit word in the DPC Research chat, "
                   "2026-09-17T08:37:30Z: «@CC_windows «run step 1» (v5)» (translated from Russian); reviewer pass on "
                   "v5: Ark 08:27:19Z and 08:36:24Z, Zcode 08:28:59Z"),
        "ceilings": {"copy_vs_original": COPY_CEILING_TEXT, "P0": P0_CEILING_TEXT,
                     "fresh_process": FRESH_CEILING_TEXT},
        "n_copy_calls_per_cell": N_COPY_CALLS,
        "cell_definition": ("loss_16 = mean over the five copy calls of each call's 16-item "
                            "mean; per-item columns = per-item mean over the five calls"),
        "script_sha256": SCRIPT_HASHES,
        "flyvis": flyvis.__version__, "torch": torch.__version__,
        "python": sys.version.split()[0],
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "netdir": str(solver.dir.path), "device": str(flyvis.device),
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "pid": os.getpid(),
        "runs": RUNS6, "labels": LABELS6,
        "checkpoints": {CHKPT_NAMES[k]: v for k, v in CHKPTS.items()},
        "checkpoint_index_to_solver_iteration": {str(k): v for k, v in CHKPTS.items()},
        "conditions": CONDITION_DEFS,
        "shuffle_seed": SHUFFLE_SEED,
        "shuffle_derivation": ("numpy.random.default_rng([SHUFFLE_SEED, item_index])"
                               ".permutation(n_frames), item_index = the dataloader "
                               "enumeration index 0..15; identical in every process"),
        "val_items": item_names,
        "batch_size": int(solver.task.val_data.batch_size),
        "dt": float(solver.task.dataset.dt),
        "t_pre": 0.25, "steady_state_value": 0.5, "augmentation": False,
        "ablation_hook_registered": False,
        "copy_note": ("per_item_eval_transformed is a line-for-line copy of "
                      "diag1_eval_paths.py:176-201; only the argument of :191 and the loop "
                      "variable `_`->`_i` on :188 differ -- verified by code_gate (brief v4 "
                      "Sec 6), see code_gate in this json"),
    }
    print("META", json.dumps({k: v for k, v in meta.items() if k != "val_items"}), flush=True)

    # ------------------------------------------------------------------ controls (re-run here)
    controls = {}
    ctrl_ok = True
    for run in ("000",):
        for ci in sorted(CHKPTS):
            rec, passed = copy_fidelity_control(solver, run, ci)
            controls[f"{run}@{rec['solver_iteration']}"] = rec
            print("CONTROL", json.dumps(rec), flush=True)
            ctrl_ok = ctrl_ok and passed
    if not ctrl_ok:
        print("CONTROL VERDICT FAIL (in --task main: |mean(A1..A5) - mean(B1..B5)| > 1e-2 or "
              "|P0 mean of five - stored| > 1e-3) -- stopping before the sweep; nothing written",
              flush=True)
        return 3

    null = constant_output_null(solver)
    print("NULL constant_output_null", null["constant_output_null"],
          "zero_prediction_null", null["zero_prediction_null"], flush=True)

    # ------------------------------------------------------------------ the 48 cells
    rows, per_cell, first_real_wall = sweep(solver, item_names, "CELL")
    assert len(rows) == 48, len(rows)
    write_losses_csv(out / "gray_losses.csv", rows, item_names,
                     SCRIPT_HASHES["results/diagnostics/gray/gray_stimulus.py"])

    # per-item frame permutations actually used (recorded, not assumed)
    perms = {}
    with torch.no_grad():
        with solver.task.dataset.augmentation(False):
            for _i, data in enumerate(solver.task.val_data):
                nf = int(data["lum"].shape[1])
                p = frame_permutation(_i, nf)
                perms[item_short(item_names[_i])] = {
                    "item_index": _i, "n_frames": nf,
                    "permutation": [int(x) for x in p],
                    "is_identity": bool(np.array_equal(p, np.arange(nf)))}

    p0_all = {k: v["P0_mean_of_five_minus_stored"] for k, v in per_cell.items()
              if v.get("P0_mean_of_five_minus_stored") is not None}
    assert len(p0_all) == 12, len(p0_all)
    p0_all_ok = bool(all(abs(float(v)) <= P0_TOL for v in p0_all.values()))
    ctrl = {
        "meta": meta,
        "code_gate": cg,
        "copy_fidelity_and_P0": controls,
        "constant_output_null": null,
        "P0_rule": P0_CEILING_TEXT,
        "P0_mean_of_five_minus_stored_all_12_checkpoints": {
            f"{k[0]}@{k[1]}": v for k, v in p0_all.items()},
        "P0_max_abs_mean_of_five_minus_stored": repr(
            max(abs(float(v)) for v in p0_all.values())),
        "P0_all_12_within_1e-3": p0_all_ok,
        "cell_max_minus_min_loss_16_over_five_calls_max": repr(max(
            float(v["loss_16_max_minus_min_over_calls"]) for v in per_cell.values())),
        "frame_permutations": perms,
        "cells": {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in per_cell.items()},
        "n_cells": len(rows),
        "n_evaluations": len(rows) * N_COPY_CALLS,
        "first_evaluation_real_wall_s": repr(first_real_wall),
        "wall_s_total": repr(time.perf_counter() - t_start),
    }
    (out / "gray_controls.json").write_text(json.dumps(ctrl, indent=1))
    print("P0 MAX ABS (12 checkpoints, mean of five - stored)",
          ctrl["P0_max_abs_mean_of_five_minus_stored"], f"[{P0_CEILING_TEXT}]",
          "all_12_within_1e-3", p0_all_ok, flush=True)
    print("FIRST REAL EVAL WALL S", ctrl["first_evaluation_real_wall_s"], flush=True)
    print("TOTAL WALL S", ctrl["wall_s_total"], flush=True)
    if not p0_all_ok:
        print("P0 CEILING BREACHED in the sweep -- STOP (outputs written for the record)",
              flush=True)
        return 3
    return 0


def task_repeat(a):
    """Brief Sec 6 'Fresh process': all 48 cells again, in a second process."""
    out = Path(a.out_dir)
    t_start = time.perf_counter()
    solver = D.build_solver(Path(a.netdir_root))
    import flyvis
    item_names = D.val_item_names(solver)
    rows, per_cell, first_real_wall = sweep(solver, item_names, "REPEAT")
    assert len(rows) == 48, len(rows)
    write_losses_csv(out / "gray_losses_repeat.csv", rows, item_names,
                     SCRIPT_HASHES["results/diagnostics/gray/gray_stimulus.py"])

    first = read_losses_csv(out / "gray_losses.csv")
    second = read_losses_csv(out / "gray_losses_repeat.csv")
    assert set(first) == set(second), "cell sets differ"
    deltas = {f"{k[0]}|{k[1]}|{k[2]}": second[k]["loss_16"] - first[k]["loss_16"]
              for k in first}
    per_item_max = {f"{k[0]}|{k[1]}|{k[2]}":
                    float(np.max(np.abs(second[k]["per_item"] - first[k]["per_item"])))
                    for k in first}
    worst = max(deltas, key=lambda k: abs(deltas[k]))
    # brief Sec 6 v5: gate per cell on |delta| of the five-call mean <= 1e-2; the in-process
    # spread of each checkpoint (copy_fidelity_control in the --task main process, run 000, and
    # the max-min over the five calls of every cell in both processes) is stated next to the
    # gate, recorded, not gating; per-item deltas recorded, not gating
    first_ctrl = json.loads((out / "gray_controls.json").read_text(encoding="utf-8"))
    floors = {}
    for rec in first_ctrl["copy_fidelity_and_P0"].values():
        floors[int(rec["solver_iteration"])] = {
            "run": rec["run"], "chkpt": rec["chkpt"],
            "B_floor_max_abs_mean_over_10_pairs": float(
                rec["recorded_B_floor_max_abs_mean_over_10_pairs"]),
            "B_floor_max_abs_per_item_over_10_pairs": float(
                rec["recorded_B_floor_max_abs_per_item_over_10_pairs"]),
            "A_spread_max_abs_mean_over_10_pairs": float(
                rec["recorded_A_spread_max_abs_mean_over_10_pairs"])}
    first_cells = first_ctrl["cells"]
    per_ckpt = {}
    for it in sorted(floors):
        keys = [k for k in first if k[1] == it]
        assert len(keys) == 24, (it, len(keys))
        wk = max(keys, key=lambda k: abs(second[k]["loss_16"] - first[k]["loss_16"]))
        mx = abs(second[wk]["loss_16"] - first[wk]["loss_16"])
        wki = max(keys, key=lambda k: per_item_max[f"{k[0]}|{k[1]}|{k[2]}"])
        spread1 = max(float(first_cells[f"{k[0]}|{k[1]}|{k[2]}"][
            "loss_16_max_minus_min_over_calls"]) for k in keys)
        spread2 = max(float(per_cell[k]["loss_16_max_minus_min_over_calls"]) for k in keys)
        per_ckpt[str(it)] = {
            "gate": FRESH_CEILING_TEXT,
            "in_process_max_minus_min_over_five_calls_max_over_24_cells_process1": repr(spread1),
            "in_process_max_minus_min_over_five_calls_max_over_24_cells_process2": repr(spread2),
            "in_process_spread_this_run_recorded_not_gating": {
                k: (repr(v) if isinstance(v, float) else v) for k, v in floors[it].items()},
            "in_process_spread_stated_in_brief_chkpt_00071": repr(BRIEF_CHKPT_00071_SPREAD),
            "max_abs_delta_loss_16": repr(mx),
            "max_abs_delta_cell": f"{wk[0]}|{wk[1]}|{wk[2]}",
            "max_abs_per_item_delta_recorded_not_gating": repr(
                per_item_max[f"{wki[0]}|{wki[1]}|{wki[2]}"]),
            "max_abs_per_item_delta_cell": f"{wki[0]}|{wki[1]}|{wki[2]}",
            "n_cells": len(keys),
            "n_cells_bitwise_identical_loss_16": int(sum(
                1 for k in keys if second[k]["loss_16"] == first[k]["loss_16"])),
            "all_cells_pass_le_1e-2": bool(mx <= FRESH_PROCESS_TOL),
        }
    cell_gate = {}
    for k in first:
        d = abs(second[k]["loss_16"] - first[k]["loss_16"])
        cell_gate[f"{k[0]}|{k[1]}|{k[2]}"] = {
            "abs_delta_loss_16": repr(d), "threshold": repr(FRESH_PROCESS_TOL),
            "pass_le_1e-2": bool(d <= FRESH_PROCESS_TOL),
            "max_abs_per_item_delta_recorded_not_gating": repr(
                per_item_max[f"{k[0]}|{k[1]}|{k[2]}"])}
    rep = {
        "status": STATUS,
        "script_sha256": SCRIPT_HASHES,
        "pid": os.getpid(),
        "flyvis": flyvis.__version__, "torch": torch.__version__,
        "python": sys.version.split()[0],
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "gate": ("brief Sec 6 v5: " + FRESH_CEILING_TEXT + "; per-item repeat differences "
                 "recorded, not gating; the in-process spread of each checkpoint (five "
                 "D.per_item_eval calls on run 000, gray_controls.json; brief states 8.6e-05 at "
                 "chkpt_00071) stated next to the gate, not gating"),
        "per_checkpoint": per_ckpt,
        "per_cell_gate": cell_gate,
        "max_abs_delta_loss_16": repr(max(abs(v) for v in deltas.values())),
        "max_abs_delta_cell": worst,
        "n_cells_bitwise_identical_loss_16": int(sum(1 for v in deltas.values() if v == 0.0)),
        "max_abs_per_item_delta": repr(max(per_item_max.values())),
        "gate_pass": bool(all(v["pass_le_1e-2"] for v in cell_gate.values())),
        "n_cells_pass_le_1e-2": int(sum(1 for v in cell_gate.values() if v["pass_le_1e-2"])),
        "cells_this_process": {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in per_cell.items()},
        "delta_loss_16_per_cell": {k: repr(v) for k, v in deltas.items()},
        "max_abs_per_item_delta_per_cell": {k: repr(v) for k, v in per_item_max.items()},
        "first_evaluation_real_wall_s": repr(first_real_wall),
        "wall_s_total": repr(time.perf_counter() - t_start),
    }
    (out / "gray_repeat_controls.json").write_text(json.dumps(rep, indent=1))
    print("REPEAT MAX ABS DELTA", rep["max_abs_delta_loss_16"], rep["max_abs_delta_cell"],
          f"[{FRESH_CEILING_TEXT}]", "gate_pass_all_cells_le_1e-2", rep["gate_pass"],
          "n_cells_pass", rep["n_cells_pass_le_1e-2"], flush=True)
    print("REPEAT PER CHECKPOINT", json.dumps(per_ckpt), flush=True)
    print("TOTAL WALL S", rep["wall_s_total"], flush=True)
    return 0 if rep["gate_pass"] else 3


# ---------------------------------------------------------------- the pre-registered readings
def reading_ii_text(cls_gray, cls_zero):
    """Brief Sec 7 (ii) branches, verbatim; 'between' and 'returns' both count as not exploding."""
    expl_gray = cls_gray == "explodes"
    expl_zero = cls_zero == "explodes"
    if expl_gray and expl_zero:
        return "fragility to absence of drive is real"
    if not expl_gray and not expl_zero:
        return ("explosion only under the ablation's forced-zero state, i.e. neither (a) nor (b) "
                "explode -> the ablation deltas -- +21,158 (R2 single-type clamp-to-0) and "
                "+30,626 (full R1-R8 clamp-to-0) -- measure the dynamics' fragility to a zero "
                "clamp specifically, an instrument artefact, not a vision dependence, and the R2 "
                "ablation finding must be reworded accordingly")
    return ("only one of (a) gray and (b) zero explodes -- neither pre-registered branch "
            "applies; recorded as measured, no branch selected")


def task_readings(a):
    """Brief Sec 7, evaluated mechanically from gray_losses.csv.  No GPU, no interpretation."""
    out = Path(a.out_dir)
    f = read_losses_csv(out / "gray_losses.csv")
    U, T = 0, 250008                     # untrained / trained solver iterations

    def L(label, it, cond):
        return f[(label, it, cond)]["loss_16"]

    readings = {
        "status": STATUS,
        "script_sha256": SCRIPT_HASHES,
        "source": "gray_losses.csv (this directory)",
        "rule_source": "docs/briefs/2026-09-16-step1-gray-stimulus.md Sec 7, verbatim",
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "band_fraction": BAND_FRACTION,
        "per_seed": {},
    }
    for lab in LABELS6:
        gain = L(lab, U, "real") - L(lab, T, "real")
        band = BAND_FRACTION * gain
        d_i = L(lab, T, "gray") - L(lab, U, "gray")
        holds_i = bool(abs(d_i) <= band)
        d_iii_real = L(lab, T, "shuffled") - L(lab, T, "real")
        d_iii_gray = L(lab, T, "shuffled") - L(lab, U, "gray")
        near_real = bool(abs(d_iii_real) <= band)
        near_gray = bool(abs(d_iii_gray) <= band)
        # brief Sec 7 (iii) v3: exclusive branches; void when the two references lie within
        # 0.2 * gain_s of each other
        ref_sep = L(lab, T, "real") - L(lab, U, "gray")
        void_iii = bool(abs(ref_sep) <= VOID_FRACTION * gain)
        nearer = "L_trained_real" if abs(d_iii_real) <= abs(d_iii_gray) else "L_untrained_gray"
        if void_iii:
            text_iii = ("between -- void for this seed (the two references lie within "
                        "0.2 * gain_s of each other)")
        elif near_real and not near_gray:
            text_iii = "not about motion"
        elif near_gray and not near_real:
            text_iii = "about temporal content"
        else:
            text_iii = "between"
        # brief Sec 7 (ii) v3, computed for every seed (the pre-registered reading is seed 2)
        ii = {}
        for cond in ("gray", "zero"):
            exc = L(lab, T, cond) - L(lab, U, "gray")
            if exc >= EXPLODE_MULT * gain:
                cls = "explodes"
            elif exc <= RETURN_FRACTION * gain:
                cls = "returns"
            else:
                cls = "between"
            ii[cond] = {"L_trained": repr(L(lab, T, cond)),
                        "excess_over_untrained_gray": repr(exc),
                        "excess_in_units_of_gain_s": repr(exc / gain),
                        "class": cls}
        readings["per_seed"][lab] = {
            "L_untrained_real": repr(L(lab, U, "real")),
            "L_trained_real": repr(L(lab, T, "real")),
            "L_untrained_gray": repr(L(lab, U, "gray")),
            "L_trained_gray": repr(L(lab, T, "gray")),
            "L_untrained_zero": repr(L(lab, U, "zero")),
            "L_trained_zero": repr(L(lab, T, "zero")),
            "L_untrained_shuffled": repr(L(lab, U, "shuffled")),
            "L_trained_shuffled": repr(L(lab, T, "shuffled")),
            "gain_s": repr(gain),
            "band_0.1_gain_s": repr(band),
            "reading_i_delta_trained_gray_minus_untrained_gray": repr(d_i),
            "reading_i_abs_delta": repr(abs(d_i)),
            "reading_i_holds": holds_i,
            "reading_i_text": ("gray removes >= 90% of the learned gain"
                               if holds_i else
                               "gray does NOT remove >= 90% of the learned gain "
                               "(|L_trained_gray - L_untrained_gray| > 0.1 * gain_s)"),
            "control_untrained_gray_minus_untrained_real": repr(
                L(lab, U, "gray") - L(lab, U, "real")),
            "reading_iii_delta_to_trained_real": repr(d_iii_real),
            "reading_iii_delta_to_untrained_gray": repr(d_iii_gray),
            "reading_iii_within_band_of_trained_real": near_real,
            "reading_iii_within_band_of_untrained_gray": near_gray,
            "reading_iii_reference_separation_trained_real_minus_untrained_gray": repr(ref_sep),
            "reading_iii_void_threshold_0.2_gain_s": repr(VOID_FRACTION * gain),
            "reading_iii_void": void_iii,
            "reading_iii_nearer_reference": nearer,
            "reading_iii_text": text_iii,
            "reading_ii_excess_explodes_threshold_10_gain_s": repr(EXPLODE_MULT * gain),
            "reading_ii_excess_returns_threshold_0.1_gain_s": repr(RETURN_FRACTION * gain),
            "reading_ii_a_gray": ii["gray"],
            "reading_ii_b_zero": ii["zero"],
            "reading_ii_text": reading_ii_text(ii["gray"]["class"], ii["zero"]["class"]),
        }

    # ---- reading (ii): seed 2, on (a) gray and (b) zero separately (brief Sec 7 (ii) v3)
    p2 = readings["per_seed"]["seed2"]
    readings["reading_ii_seed2"] = {
        "definition": ("excess_cond(s) = L_trained,cond(s) - L_untrained_gray(s), cond in "
                       "{gray, zero}; >= 10 * gain_s -> explodes; <= 0.1 * gain_s -> returns; "
                       "otherwise between (brief Sec 7 (ii) v3, pre-registered at the gate stop)"),
        "seed2_L_untrained_gray": p2["L_untrained_gray"],
        "seed2_L_trained_real": p2["L_trained_real"],
        "seed2_gain_s": p2["gain_s"],
        "explodes_threshold_10_gain_s": p2["reading_ii_excess_explodes_threshold_10_gain_s"],
        "returns_threshold_0.1_gain_s": p2["reading_ii_excess_returns_threshold_0.1_gain_s"],
        "a_gray": p2["reading_ii_a_gray"],
        "b_zero": p2["reading_ii_b_zero"],
        "other_five_trained_real": {lab: repr(L(lab, T, "real"))
                                    for lab in LABELS6 if lab != "seed2"},
        "prereg_reference_R2_single_type_clamp_delta_16": PREREG_SEED2_R2_DELTA,
        "prereg_reference_R1_R8_clamp_excess": PREREG_SEED2_R1R8_CLAMP_EXCESS,
        "reading_ii_text": p2["reading_ii_text"],
    }
    readings["reading_i_summary"] = {
        "n_seeds_holding": int(sum(1 for lab in LABELS6
                                   if readings["per_seed"][lab]["reading_i_holds"])),
        "seeds_holding": [lab for lab in LABELS6
                          if readings["per_seed"][lab]["reading_i_holds"]],
    }
    readings["reading_iii_summary"] = {
        lab: readings["per_seed"][lab]["reading_iii_text"] for lab in LABELS6}
    (out / "gray_readings.json").write_text(json.dumps(readings, indent=1))
    for lab in LABELS6:
        p = readings["per_seed"][lab]
        print("READING_I", lab, "gain", p["gain_s"], "band", p["band_0.1_gain_s"],
              "|delta|", p["reading_i_abs_delta"], "holds", p["reading_i_holds"], flush=True)
    for lab in LABELS6:
        p = readings["per_seed"][lab]
        print("READING_III", lab, "d_real", p["reading_iii_delta_to_trained_real"],
              "d_untrained_gray", p["reading_iii_delta_to_untrained_gray"],
              "->", p["reading_iii_text"], flush=True)
    for lab in LABELS6:
        p = readings["per_seed"][lab]
        print("READING_II", lab, "gray", json.dumps(p["reading_ii_a_gray"]),
              "zero", json.dumps(p["reading_ii_b_zero"]), flush=True)
    print("READING_II_SEED2", json.dumps(readings["reading_ii_seed2"]), flush=True)
    return 0


def main():
    a = parse_args()
    return {"codegate": task_codegate, "control": task_control, "floor": task_floor,
            "main": task_main,
            "repeat": task_repeat, "readings": task_readings}[a.task](a)


if __name__ == "__main__":
    sys.exit(main())


# TRANSLATION NOTE, 2026-09-23 (appended at the end so that every line number cited elsewhere
# stays valid): the Russian launch-word quotes of this file -- two docstring lines and the "launch"
# string literal written into the output json's meta -- were translated into English on Mike's
# word.  The Russian original is in git history at commit 2488ecb72d14aa5398149d9a727b58852873a091.
# The recorded script_sha256 61eb8bf3068b0bc4a89568c144ab1a931c68a0c4a54659a24cd5b631fc067624
# (gray_* records, README.md) refers to that original revision and reproduces there, not from this
# revision.  The translated literal changes only outputs written from now on; outputs already on
# disk keep the original string.  Old and new hashes and the citing records:
# docs/notes/2026-09-23-translated-pinned-files.md.
