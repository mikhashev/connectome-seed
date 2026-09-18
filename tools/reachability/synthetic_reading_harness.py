"""Execute the one-shot reading script end to end on FABRICATED curves, three cases.

Why this exists. `read_reachability_endpoint.py` is allowed to run exactly once, on data
nobody may look at beforehand, and until 2026-09-18 it had never been executed at all --
three review rounds by three authors, all by reading. Static checks caught two would-be
crashes; the first run of this harness caught a resolver that could not map two of the
eight runs; and Ark's point after that was the sharpest of the three: the script has still
never reached a verdict, so the entire path after the mapping -- exclusion, disqualification,
the control, the criterion -- has never executed.

It is not a reading. The curves are fabricated, so no `cross(r, L)` of the substrate is
computed, and the verdict carries no information about the real runs: each case is built so
that the registered rules force a known answer.

  (i)   twins identical to their originals. Twin-gap is 0, which is <= one checkpoint
        step, so §5 disqualifies EVERY level and §5's whole-test rule fires.
        Expected: TEST UNREADABLE.
  (ii)  twins two checkpoints from their originals, individuals spread nine on average.
        Both gaps clear one step, and between-gap > twin-gap at every level.
        Expected: ACCEPT -- the branch the endpoint exists to reach.
  (iii) twins eleven checkpoints out, wider than the individuals. Both gaps clear one
        step, so levels are accepted, and then the §4 criterion fails.
        Expected: FAIL.

Three cases, three different verdicts, three different code paths. Ark proposed (i) and
(iii) as both UNREADABLE; reading §5 and §4 in the script says otherwise -- a level whose
between-gap exceeds one step is not disqualified, so (iii) reaches the criterion and fails
it, and FAIL and TEST UNREADABLE are different verdicts with different precedence (§10).
Getting three distinct verdicts is the stronger control, because two cases answering
"UNREADABLE" for different reasons is exactly the "verdict without its quantity" this
project spent a day retiring.

The construction, so the expectations are derived rather than hoped for. Every curve is the
same clean descent from 1212.0 delayed by a whole number of checkpoints, so
`cross(run, L)` differs between two runs by exactly their difference in delay. Canonical
seeds 0..5 take delays 0, 4, 8, 12, 16, 20, which puts the mean of the fifteen canonical
pairwise gaps at 35/15 x 4 = 9.33 checkpoints. Twin delays are then chosen relative to
their own original: +0 for case (i), +2 for case (ii), +11 for case (iii).

Discipline this harness keeps:
  * the canonical script is never modified. The pin makes fabricated input refuse by
    design, so the harness copies the script into its work directory and retargets
    INPUT_SHA256_REGISTERED in the COPY -- no flag, no environment override, no branch in
    the real script. The copy's own hash therefore differs, and the output says so.
  * every line of captured output is written with a `SYNTHETIC | ` prefix, so a grep for
    ACCEPT or TEST UNREADABLE over the results tree cannot mistake a fabricated verdict
    for a real one (Ark: a synthetic ACCEPT is a verdict without a substrate).
  * the outputs are kept, not thrown away, under results/diagnostics/reachability/harness/:
    a control that is not recorded is not a control.

Usage:
    python tools/reachability/synthetic_reading_harness.py [--repo DIR] [--out DIR]
                                                           [--workdir DIR]

Exit codes:
    0  every case produced the verdict its construction forces
    1  usage error, or the repository does not have the expected shape
    3  at least one case produced a different verdict, or reached no verdict at all
"""

import argparse
import csv
import hashlib
import io
import os
import re
import shutil
import sys
import subprocess
import tempfile

SUBSTRATE_REL = os.path.join("results", "night4", "night_report_checkpoints.csv")
SCRIPT_REL = os.path.join("tools", "reachability", "read_reachability_endpoint.py")

HEADER = ["iteration", "val_loss_seed0", "val_loss_seed0prime", "val_loss_seed1",
          "val_loss_seed2", "val_loss_seed3", "val_loss_seed4", "val_loss_seed3prime",
          "val_loss_seed5"]

CANONICAL_DELAY = {0: 0, 1: 4, 2: 8, 3: 12, 4: 16, 5: 20}

CASES = (
    ("i", 0, "TEST UNREADABLE",
     "twins identical: twin-gap 0 <= one step, so §5 disqualifies every level and the "
     "whole-test rule fires"),
    ("ii", 2, "ACCEPT",
     "twins 2 checkpoints out, individuals 9.33 on average: both gaps clear one step and "
     "between-gap > twin-gap everywhere"),
    ("iii", 11, "FAIL",
     "twins 11 checkpoints out, wider than the individuals: levels are accepted and the "
     "§4 criterion then fails"),
)


def real_iterations(repo):
    """The checkpoint grid's shape -- a structural quantity §11 names as inspectable."""
    with io.open(os.path.join(repo, SUBSTRATE_REL), encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    start = 0
    while rows[start] and rows[start][0].startswith("#"):
        start += 1
    if rows[start] != HEADER:
        raise SystemExit("the substrate's header is not the one this harness expects:\n"
                         "  %s" % rows[start])
    return [int(r[0]) for r in rows[start + 1:]]


def curve(n, delay):
    """The same descent from 1212.0 for every run, delayed by whole checkpoints.

    Flat until the delay elapses, then strictly decreasing, so `cross(run, L)` is the
    undelayed crossing index plus the delay -- which is what makes the gaps exact.
    """
    return [round(1212.0 - 60.0 * max(i - delay, 0) / 71.0, 4) for i in range(n)]


def write_substrate(path, iterations, twin_offset):
    n = len(iterations)
    delays = dict(CANONICAL_DELAY)
    columns = {
        "val_loss_seed0": curve(n, delays[0]),
        "val_loss_seed0prime": curve(n, delays[0] + twin_offset),
        "val_loss_seed1": curve(n, delays[1]),
        "val_loss_seed2": curve(n, delays[2]),
        "val_loss_seed3": curve(n, delays[3]),
        "val_loss_seed4": curve(n, delays[4]),
        "val_loss_seed3prime": curve(n, delays[3] + twin_offset),
        "val_loss_seed5": curve(n, delays[5]),
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["# SYNTHETIC -- fabricated curves, NOT the substrate; written by "
                         "tools/reachability/synthetic_reading_harness.py"])
        writer.writerow(["# twin offset %d checkpoints; canonical delays %s"
                         % (twin_offset, sorted(CANONICAL_DELAY.items()))])
        writer.writerow(HEADER)
        for i, iteration in enumerate(iterations):
            writer.writerow([iteration] + [columns[c][i] for c in HEADER[1:]])
    return path


def sha256_normalized(path):
    data = io.open(path, "rb").read()
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def retargeted_script(repo, workdir, new_pin):
    """A throwaway copy of the script whose input pin points at the fabricated file.

    The canonical script gets no flag and no override: the pin is meant to refuse exactly
    this kind of input, and a harness that could switch it off in the real script would be
    the hole the pin was added to close.
    """
    source = io.open(os.path.join(repo, SCRIPT_REL), encoding="utf-8").read()
    pattern = re.compile(r'^INPUT_SHA256_REGISTERED = "[0-9a-f]{64}"$', re.MULTILINE)
    if len(pattern.findall(source)) != 1:
        raise SystemExit("cannot retarget the pin: INPUT_SHA256_REGISTERED not found "
                         "exactly once in %s" % SCRIPT_REL)
    patched = pattern.sub('INPUT_SHA256_REGISTERED = "%s"' % new_pin, source)
    target = os.path.join(workdir, "read_reachability_endpoint__RETARGETED.py")
    io.open(target, "w", encoding="utf-8", newline="\n").write(patched)
    return target


VERDICT_TOKENS = ("CONTROL FAIL", "TEST UNREADABLE", "ACCEPT", "FAIL")


def verdict_of(text):
    """The verdict the script printed, or None if it never reached one.

    The verdict is not a `verdict: X` line -- the script prints a section banner reading
    `verdict`, a rule of dashes, and then the verdict itself on its own line. Reading the
    first token of that line rather than grepping the whole output matters: the words
    ACCEPT and FAIL also appear in the criterion's own description a few lines earlier,
    so a grep would have reported a verdict for a run that refused before reaching one.
    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip() != "verdict":
            continue
        for candidate in lines[i + 1:]:
            stripped = candidate.strip()
            if not stripped or set(stripped) <= set("-"):
                continue
            for token in VERDICT_TOKENS:
                if stripped.startswith(token):
                    return token
            return stripped[:40]
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", default=os.getcwd())
    parser.add_argument("--out", default=None,
                        help="where to keep the outputs (default: "
                             "<repo>/results/diagnostics/reachability/harness)")
    parser.add_argument("--workdir", default=None,
                        help="scratch directory (default: a temporary one, removed after)")
    args = parser.parse_args(argv)

    repo = os.path.abspath(args.repo)
    out_dir = args.out or os.path.join(repo, "results", "diagnostics", "reachability",
                                       "harness")
    for rel in (SUBSTRATE_REL, SCRIPT_REL):
        if not os.path.exists(os.path.join(repo, rel)):
            print("not found: %s" % rel)
            return 1

    iterations = real_iterations(repo)
    os.makedirs(out_dir, exist_ok=True)

    temp = args.workdir or tempfile.mkdtemp(prefix="reach_harness_")
    os.makedirs(temp, exist_ok=True)
    interpreter = os.path.join(repo, "tools", ".venv", "Scripts", "python.exe")
    if not os.path.exists(interpreter):
        interpreter = sys.executable

    results = []
    try:
        for case, twin_offset, expected, why in CASES:
            fake_repo = os.path.join(temp, "case_%s" % case)
            if os.path.isdir(fake_repo):
                shutil.rmtree(fake_repo)
            substrate = write_substrate(
                os.path.join(fake_repo, SUBSTRATE_REL), iterations, twin_offset)
            pin = sha256_normalized(substrate)
            script = retargeted_script(repo, fake_repo, pin)

            proc = subprocess.run(
                [interpreter, script, "--repo", fake_repo,
                 "--out", os.path.join(fake_repo, "reading_out")],
                capture_output=True, text=True, encoding="utf-8", errors="replace")
            text = (proc.stdout or "") + (proc.stderr or "")
            got = verdict_of(text)

            out_path = os.path.join(out_dir, "synthetic_case_%s.out" % case)
            with io.open(out_path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write("SYNTHETIC | substrate: synthetic (fabricated curves; NOT the "
                         "registered substrate). This file is a control, not a reading.\n")
                fh.write("SYNTHETIC | case %s: twin offset %d checkpoints; expected "
                         "verdict by construction: %s\n" % (case, twin_offset, expected))
                fh.write("SYNTHETIC | why: %s\n" % why)
                fh.write("SYNTHETIC | script: retargeted copy -- INPUT_SHA256_REGISTERED "
                         "replaced with the fabricated file's hash, so this copy's own "
                         "sha256 differs from the canonical script's on purpose.\n")
                fh.write("SYNTHETIC | exit code: %d ; verdict read back: %s\n"
                         % (proc.returncode, got if got is not None else "(none reached)"))
                fh.write("SYNTHETIC |\n")
                for line in text.splitlines():
                    fh.write("SYNTHETIC | " + line + "\n")

            ok = (got == expected)
            results.append((case, expected, got, proc.returncode, ok, out_path))
            print("case %-3s expected %-16s got %-16s exit %d  %s"
                  % (case, expected, got if got is not None else "(none)",
                     proc.returncode, "OK" if ok else "MISMATCH"))
            print("    %s" % out_path)
    finally:
        if args.workdir is None:
            shutil.rmtree(temp, ignore_errors=True)

    failed = [r for r in results if not r[4]]
    print()
    if failed:
        print("%d of %d cases did not produce the verdict their construction forces."
              % (len(failed), len(results)))
        print("Until every case matches, the path after the mapping is not known to work.")
        return 3
    print("all %d cases produced the verdict their construction forces; the exclusion "
          "rule, the disqualification rule, the control and the criterion have all now "
          "executed." % len(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
