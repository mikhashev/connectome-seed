"""Execute the one-shot reading script end to end on FABRICATED curves.

Why this exists. `read_reachability_endpoint.py` is allowed to run exactly once, on data
nobody may look at beforehand, and until 2026-09-18 it had never been executed at all --
three review rounds by three authors, all by reading. Static checks had already caught two
would-be crashes (a deleted name, a renamed dict key), but static checks do not catch
behaviour. This harness builds a throwaway copy of `results/` whose checkpoint CSVs carry
invented numbers, runs the real script against that copy, and records what it did.

It is not a reading. The curves are fabricated, so no `cross(r, L)` of the substrate is
computed, and the verdict carries no information about the real runs: the answer is fixed
by construction before the script sees the file.

  case A -- each twin is identical to its original, so every twin gap is zero while
            different individuals are separated. Expected, if the script reaches the
            criterion: ACCEPT.
  case B -- each twin is displaced far from its original, so twin gaps dominate.
            Expected: the disqualification rule fires and the test is UNREADABLE.

That makes it the live control the registration does not have. The registered positive
control is empty by construction and its failure branch unreachable (registration §6), so
nothing in the real run can tell a working instrument from a broken one; here the expected
answer is known in advance and the instrument can be seen to produce it, or not.

What the first two runs of this harness found, none of which reading had found:

  * The script never reaches the criterion on the current repository. Runs 9991/000 and
    9991/900 resolve to no column, and the script refuses with exit 2. See the commit that
    added this file for the two-part cause.
  * The resolver's "candidate columns disagree on the curve" check fires correctly, and
    caught this harness's own first attempt at fabricating data, which gave every
    `val_loss_A` column seed 0's series regardless of which pair the file names.
  * The layout guard requires a checkpoint CSV in every night directory, which the first
    attempt discovered by deleting them.
  * The provenance ordering holds under execution: the script's own sha256, then every
    input CSV's sha256, then the constants line -- all printed before §3 step 1, so the
    registered constants cannot have been chosen to fit a crossing time that was already
    on screen.

Usage:
    python tools/reachability/synthetic_reading_harness.py [--repo DIR] --workdir DIR

Exit codes:
    0  both cases ran; read the per-case output files named on stdout
    1  usage error, or the repository does not have the expected shape
"""

import argparse
import csv
import glob
import io
import os
import re
import shutil
import subprocess
import sys

PAIRWISE = re.compile(r"night_report_checkpoints_(.+?)v(.+?)\.csv$")


def read_shape(path):
    """(number of comment lines, header, iteration values) -- all structural."""
    with io.open(path, encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    ncomment = 0
    while ncomment < len(rows) and rows[ncomment] and rows[ncomment][0].startswith("#"):
        ncomment += 1
    return ncomment, rows[ncomment], [int(r[0]) for r in rows[ncomment + 1:]]


def descent(n, end_offset, shift=0.0):
    """A clean synthetic descent from 1212.0, deliberately unlike any real curve."""
    return [round(1212.0 - 60.0 * (i / float(n - 1)) - end_offset * (i / float(n - 1))
                  + shift * (i / float(n - 1)), 4) for i in range(n)]


def series_for(case, n):
    """One synthetic series per column name the reports use."""
    ind = {s: descent(n, 2.0 * s) for s in range(6)}
    if case == "A":
        twin0, twin3 = list(ind[0]), list(ind[3])
    else:
        twin0 = descent(n, 0.0, shift=30.0)
        twin3 = descent(n, 6.0, shift=30.0)
    out = {"val_loss_seed0": ind[0], "val_loss_seed0prime": twin0,
           "val_loss_seed1": ind[1], "val_loss_seed2": ind[2],
           "val_loss_seed3": ind[3], "val_loss_seed4": ind[4],
           "val_loss_seed3prime": twin3, "val_loss_seed5": ind[5]}
    for name, (a, b) in (("diff_1_minus_0", (ind[1], ind[0])),
                         ("diff_2_minus_0", (ind[2], ind[0])),
                         ("diff_2_minus_1", (ind[2], ind[1]))):
        out[name] = [round(x - y, 4) for x, y in zip(a, b)]
    return out


def rewrite(path, case):
    """Fill one CSV with synthetic curves that agree with every other file.

    A pairwise file's val_loss_A/val_loss_B take the series its own filename names, and
    night 1's anonymous A/B are run 0 and its twin. The first version of this function
    ignored both rules and the resolver refused, correctly, because candidate columns for
    the same run then disagreed.
    """
    ncomment, header, iters = read_shape(path)
    cols = dict(series_for(case, len(iters)))
    match = PAIRWISE.search(os.path.basename(path))
    if match:
        cols["val_loss_A"] = cols["val_loss_seed" + match.group(1)]
        cols["val_loss_B"] = cols["val_loss_seed" + match.group(2)]
    elif os.path.basename(os.path.dirname(path)) == "night1":
        cols["val_loss_A"] = cols["val_loss_seed0"]
        cols["val_loss_B"] = cols["val_loss_seed0prime"]

    missing = [c for c in header[1:] if c not in cols]
    if missing:
        raise KeyError("no synthetic series for %s in %s" % (missing, path))

    with io.open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        for k in range(ncomment):
            writer.writerow(["# SYNTHETIC case %s -- fabricated numbers, NOT the substrate "
                             "(comment line %d)" % (case, k + 1)])
        writer.writerow(header)
        for i, iteration in enumerate(iters):
            writer.writerow([iteration] + [cols[c][i] for c in header[1:]])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", default=os.getcwd(),
                        help="the repository to copy results/ from (default: cwd)")
    parser.add_argument("--workdir", required=True,
                        help="a scratch directory for the fake trees and the output")
    args = parser.parse_args(argv)

    script = os.path.join(args.repo, "tools", "reachability",
                          "read_reachability_endpoint.py")
    results = os.path.join(args.repo, "results")
    for path in (script, results):
        if not os.path.exists(path):
            print("not found: %s" % path)
            return 1

    interpreter = os.path.join(args.repo, "tools", ".venv", "Scripts", "python.exe")
    if not os.path.exists(interpreter):
        interpreter = sys.executable

    for case, expected in (("A", "ACCEPT"), ("B", "UNREADABLE")):
        fake = os.path.join(args.workdir, "fake_repo_%s" % case)
        if os.path.isdir(fake):
            shutil.rmtree(fake)
        os.makedirs(fake)
        shutil.copytree(results, os.path.join(fake, "results"))

        targets = sorted(glob.glob(os.path.join(
            fake, "results", "night*", "night_report_checkpoints*.csv")))
        for path in targets:
            rewrite(path, case)

        out_path = os.path.join(args.workdir, "synthetic_%s.out" % case)
        proc = subprocess.run(
            [interpreter, script, "--repo", fake,
             "--out", os.path.join(args.workdir, "synthetic_out_%s" % case)],
            capture_output=True, text=True, encoding="utf-8", errors="replace")
        text = (proc.stdout or "") + (proc.stderr or "")
        io.open(out_path, "w", encoding="utf-8").write(text)

        print("case %s: %d CSVs fabricated; expected by construction: %s"
              % (case, len(targets), expected))
        print("   exit code %d, %d lines -> %s"
              % (proc.returncode, len(text.splitlines()), out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
