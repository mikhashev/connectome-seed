"""Execute the one-shot reading script end to end on FABRICATED curves, four cases.

Why this exists. `read_reachability_endpoint.py` is allowed to run exactly once, on data
nobody may look at beforehand, and until 2026-09-18 it had never been executed at all --
three review rounds by three authors, all by reading. Static checks caught two would-be
crashes; the harness's first run caught a resolver that could not map two of the eight runs;
and Ark's point after that was the sharpest of the day -- the script had still never
reached a verdict, so the whole path after the mapping had never executed.

It is not a reading. The curves are fabricated, so no `cross(r, L)` of the substrate is
computed, and no verdict here carries information about the real runs: each case is built
so that the registered rules force a known answer.

WHAT THIS HARNESS DOES NOT SHOW (the first of three limits Ark and Zcode both asked to be
stated here, because four green cases otherwise read as validation of the instrument):

  1. It shows that the ACCEPT branch is REACHABLE and that the registered rules produce the
     verdict they force on constructed data. It does NOT show that the endpoint works, or
     that an ACCEPT on real data would mean anything: every answer here was chosen when the
     file was written.
  2. The grid sizes in these outputs are their own -- the anchors are computed from the
     fabricated curves, so the "19 of 19" in cases (i), (ii) and (iv) and the "18 of 18"
     in case (iii) are those cases' grids, NOT the registered grid of 23 tested levels.
     Do not read one for the other. (Measured from the outputs, not assumed: the four
     grids came out 19, 19, 18, 19.)
  3. The harness reads two things from the real substrate and nothing else: its header and
     its iteration column, both structural quantities §11 names as inspectable. It never
     reads a loss value and never computes a crossing time of the substrate.

The four cases:

  (i)   twins identical to their originals. Twin-gap is 0, which is <= one checkpoint
        step, so §5 disqualifies EVERY level and §5's whole-test rule fires.
        Expected: TEST UNREADABLE.
  (ii)  twins two checkpoints from their originals, individuals spread nine on average.
        Both gaps clear one step, and between-gap > twin-gap at every level.
        Expected: ACCEPT -- the branch the endpoint exists to reach.
  (iii) twins eleven checkpoints out, wider than the individuals. Both gaps clear one
        step, so levels are accepted, and then the §4 criterion fails.
        Expected: FAIL.
  (iv)  as (ii), except that one twin descends through the whole grid, rises back ABOVE
        the top of it, and only then settles below again. Expected: ACCEPT under §2 --
        and FAIL when the crossing convention is swapped. See below.

Provenance of the case list, since a claim about who predicted what belongs in the
artefact and not in anyone's memory. Cases (i)-(iii) were proposed by Ark, whose list had
(i) as TEST UNREADABLE from the start. The expectation "identical twins give ACCEPT" was
CC's, in CC's own first description of this harness, and it was wrong for the reason Ark
gave: twin-gap 0 is below one step, so §5 disqualifies rather than accepts. The commit
message of `eb4aaf1` attributes that expectation to Ark. **That attribution is wrong: the
expectation was CC's own.** The commit body is immutable, so the correction lives here,
found by Ark and confirmed by Zcode. Ark's own error in the same exchange was calling case
(iii) "UNREADABLE by criterion failure" -- the criterion fails to FAIL, a different verdict
with different precedence. Case (iv) is Ark's, in the strengthened form he gave after
Zcode asked for it.

Case (iv) and why "the verdict does not change" would have been a test that cannot fail.
The first version of (iv) was "one non-monotone curve; the verdict must not change". Ark's
objection: a script implementing the *stable* crossing rule -- the first checkpoint after
which the curve stays at or below L -- would pass that test too, and §2 registers the FIRST
crossing, explicitly refusing "stable crossing, last crossing, or any requirement that the
curve stay below L afterwards". So the test would not distinguish the convention it exists
to protect. The discriminating construction: `val_loss_seed0prime` descends on its twin's
schedule through the entire grid, then rises above the grid's top, then settles below it
again. Under §2 every crossing is the early one, so the verdict is what case (ii) gives;
under the stable rule every crossing moves to the final descent, the twin gap becomes far
larger than the between gap, and the verdict becomes FAIL. The harness therefore runs (iv)
twice -- once with the script as registered, once with the crossing call swapped in a
throwaway copy -- and requires the two verdicts to DIFFER. That is a positive control on
the convention itself rather than on its absence.

This is not exotic. The real substrate already contains such a curve: seed 5 at iteration
90,012 reads 1306.4735, above the entire field.

The construction, so the expectations are derived rather than hoped for. Every monotone
curve is the same clean descent from 1212.0 delayed by a whole number of checkpoints, so
`cross(run, L)` differs between two runs by exactly their difference in delay. Canonical
seeds 0..5 take delays 0, 4, 8, 12, 16, 20, which puts the mean of the fifteen canonical
pairwise gaps at 140/15 = 9.33 checkpoints. Twin delays are chosen relative to their own
original: +0 for (i), +2 for (ii) and (iv), +11 for (iii).

Discipline this harness keeps:
  * the canonical script is never modified. The pin makes fabricated input refuse by
    design, so the harness copies the script into its work directory and retargets
    INPUT_SHA256_REGISTERED in the COPY -- no flag, no environment override, no branch in
    the real script. Case (iv)'s second run patches the crossing call in a second copy the
    same way. Every copy's own hash therefore differs, and the outputs say so.
  * every line of captured output is written with a `SYNTHETIC | ` prefix, so a grep for
    ACCEPT or TEST UNREADABLE over the results tree cannot mistake a fabricated verdict
    for a real one.
  * the outputs are kept under results/diagnostics/reachability/harness/: a control that is
    not recorded is not a control.

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

# (iv)'s rise window, in checkpoint indices. The twin is below the whole grid by
# BELOW_BY (verified in-run by the ACCEPT verdict itself, which requires every run to
# cross every level), rises to the top over (BELOW_BY, RISE_END], and settles back over
# (RISE_END, last].
BELOW_BY = 53
RISE_END = 62
RISE_TOP = 1212.0

# The one call site the alternative convention replaces, and its replacement. A single
# exact line, so a change to the script's crossing code makes this patch fail loudly
# rather than silently test nothing.
CROSS_CALL = "            cross_idx[(rid, L)] = first_index_at_or_below(curves[rid], L)"
CROSS_CALL_SWAPPED = "            cross_idx[(rid, L)] = _HARNESS_stable_index(curves[rid], L)"
ANCHOR_BEFORE = "def run_reading(repo, started):"
STABLE_DEF = '''

def _HARNESS_stable_index(values, level):
    """The STABLE crossing: the first index after which the curve stays <= level.

    Injected only into a throwaway copy of the script, by
    tools/reachability/synthetic_reading_harness.py, to check that the registered FIRST
    crossing of §2 is actually what the script implements. §2 refuses this convention by
    name; if the two conventions gave the same verdict on case (iv), the case would not be
    testing the convention at all.
    """
    last_above = None
    for i, value in enumerate(values):
        if value > level:
            last_above = i
    if last_above is None:
        return 0 if values else None
    if last_above == len(values) - 1:
        return None
    return last_above + 1
'''


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


def curve_rise_and_settle(n, delay):
    """As `curve`, but rising above the grid after BELOW_BY and settling below it again.

    The shape §2 exists to define: the curve is at or below a level early, is above it for
    a stretch, and is below it again at the end. §2 takes the early crossing; the stable
    convention takes the late one.
    """
    base = curve(n, delay)
    out = list(base)
    pivot = base[BELOW_BY]
    for i in range(BELOW_BY + 1, RISE_END + 1):
        frac = (i - BELOW_BY) / float(RISE_END - BELOW_BY)
        out[i] = round(pivot + (RISE_TOP - pivot) * frac, 4)
    for i in range(RISE_END + 1, n):
        frac = (i - RISE_END) / float(n - 1 - RISE_END)
        out[i] = round(RISE_TOP + (base[-1] - RISE_TOP) * frac, 4)
    return out


CASES = (
    ("i", 0, False, "TEST UNREADABLE",
     "twins identical: twin-gap 0 <= one step, so §5 disqualifies every level and the "
     "whole-test rule fires"),
    ("ii", 2, False, "ACCEPT",
     "twins 2 checkpoints out, individuals 9.33 on average: both gaps clear one step and "
     "between-gap > twin-gap everywhere"),
    ("iii", 11, False, "FAIL",
     "twins 11 checkpoints out, wider than the individuals: levels are accepted and the "
     "§4 criterion then fails"),
    ("iv", 2, True, "ACCEPT",
     "as (ii), but one twin rises back above the grid after crossing it and settles below "
     "again: §2 takes the early crossing, so the verdict is (ii)'s -- and the swapped "
     "convention must give a different verdict"),
)


def write_substrate(path, iterations, twin_offset, non_monotone):
    n = len(iterations)
    delays = dict(CANONICAL_DELAY)
    twin0_delay = delays[0] + twin_offset
    columns = {
        "val_loss_seed0": curve(n, delays[0]),
        "val_loss_seed0prime": (curve_rise_and_settle(n, twin0_delay) if non_monotone
                                else curve(n, twin0_delay)),
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
        writer.writerow(["# twin offset %d checkpoints; canonical delays %s; "
                         "non-monotone twin: %s"
                         % (twin_offset, sorted(CANONICAL_DELAY.items()), non_monotone)])
        writer.writerow(HEADER)
        for i, iteration in enumerate(iterations):
            writer.writerow([iteration] + [columns[c][i] for c in HEADER[1:]])
    return path


def sha256_normalized_file(path):
    return hashlib.sha256(io.open(path, "rb").read().replace(b"\r\n", b"\n")).hexdigest()


PIN_RE = re.compile(r'^INPUT_SHA256_REGISTERED = "[0-9a-f]{64}"$', re.MULTILINE)


def prepared_script(repo, workdir, new_pin, swap_convention=False):
    """A throwaway copy of the script, with the pin retargeted and optionally the
    crossing convention swapped.

    The canonical script gets no flag and no override: the pin is meant to refuse exactly
    this kind of input, and a harness able to switch it off in the real script would be
    the hole the pin was added to close.
    """
    source = io.open(os.path.join(repo, SCRIPT_REL), encoding="utf-8").read()
    if len(PIN_RE.findall(source)) != 1:
        raise SystemExit("cannot retarget the pin: INPUT_SHA256_REGISTERED not found "
                         "exactly once in %s" % SCRIPT_REL)
    patched = PIN_RE.sub('INPUT_SHA256_REGISTERED = "%s"' % new_pin, source)
    suffix = "RETARGETED"
    if swap_convention:
        if patched.count(CROSS_CALL) != 1:
            raise SystemExit(
                "cannot swap the crossing convention: the expected call site is not "
                "present exactly once. The script's crossing code changed, so this "
                "control would silently test nothing.\n  looked for: %s" % CROSS_CALL)
        patched = patched.replace(CROSS_CALL, CROSS_CALL_SWAPPED)
        # The definition must be bound BEFORE run_reading executes. Appending it to the
        # end of the file put it after `sys.exit(main())`, and the copy died with a
        # NameError on the one line this control exists to exercise -- caught by running
        # it, which is the whole argument of this harness.
        if patched.count(ANCHOR_BEFORE) != 1:
            raise SystemExit("cannot place the stable-crossing definition: the anchor "
                             "%r is not present exactly once" % ANCHOR_BEFORE)
        patched = patched.replace(ANCHOR_BEFORE, STABLE_DEF + "\n" + ANCHOR_BEFORE)
        suffix = "RETARGETED_STABLE_CONVENTION"
    target = os.path.join(workdir, "read_reachability_endpoint__%s.py" % suffix)
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


def run_script(interpreter, script, fake_repo, tag):
    proc = subprocess.run(
        [interpreter, script, "--repo", fake_repo,
         "--out", os.path.join(fake_repo, "reading_out_%s" % tag)],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    text = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, text, verdict_of(text)


def write_output(out_path, banner_lines, text):
    with io.open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        for line in banner_lines:
            fh.write("SYNTHETIC | " + line + "\n")
        fh.write("SYNTHETIC |\n")
        for line in text.splitlines():
            fh.write("SYNTHETIC | " + line + "\n")


LIMITS = (
    "LIMIT 1: this shows the ACCEPT branch is REACHABLE and that the registered rules "
    "produce the verdict they force on constructed data. It does NOT show that the "
    "endpoint works: the answer was chosen when the file was written.",
    "LIMIT 2: the grid size below is this case's own -- the anchors are computed from the "
    "fabricated curves. It is NOT the registered grid of 23 tested levels.",
    "LIMIT 3: the harness reads only the substrate's header and iteration column "
    "(structural, §11); it reads no loss value and computes no crossing time of the "
    "substrate.",
)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", default=os.getcwd())
    parser.add_argument("--out", default=None)
    parser.add_argument("--workdir", default=None)
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
        for case, twin_offset, non_monotone, expected, why in CASES:
            fake_repo = os.path.join(temp, "case_%s" % case)
            if os.path.isdir(fake_repo):
                shutil.rmtree(fake_repo)
            substrate = write_substrate(
                os.path.join(fake_repo, SUBSTRATE_REL), iterations, twin_offset,
                non_monotone)
            pin = sha256_normalized_file(substrate)

            script = prepared_script(repo, fake_repo, pin)
            code, text, got = run_script(interpreter, script, fake_repo, "as_registered")

            banner = [
                "substrate: synthetic (fabricated curves; NOT the registered substrate). "
                "This file is a control, not a reading.",
                "case %s: twin offset %d checkpoints; non-monotone twin: %s"
                % (case, twin_offset, non_monotone),
                "expected verdict by construction (§2, first crossing): %s" % expected,
                "why: %s" % why,
                "script: retargeted copy -- INPUT_SHA256_REGISTERED replaced with the "
                "fabricated file's hash, so this copy's own sha256 differs from the "
                "canonical script's on purpose.",
                "exit code: %d ; verdict read back: %s"
                % (code, got if got is not None else "(none reached)"),
            ]
            banner.extend(LIMITS)

            ok = (got == expected)
            detail = ""

            if non_monotone:
                swapped_script = prepared_script(repo, fake_repo, pin,
                                                 swap_convention=True)
                code2, text2, got2 = run_script(interpreter, swapped_script, fake_repo,
                                                "stable_convention")
                differs = (got2 is not None and got2 != got)
                ok = ok and differs
                detail = " ; swapped convention -> %s (%s)" % (
                    got2 if got2 is not None else "(none)",
                    "differs, as required" if differs
                    else "SAME as §2 -- the case tests nothing")
                banner.append(
                    "CONVENTION CONTROL: the same substrate was read a second time by a "
                    "copy whose crossing call was replaced with the STABLE crossing (the "
                    "first checkpoint after which the curve stays <= L), the convention "
                    "§2 refuses by name. It returned %s against %s here. The two must "
                    "differ, or case (iv) would not be testing the convention at all."
                    % (got2 if got2 is not None else "(no verdict)",
                       got if got is not None else "(no verdict)"))
                write_output(os.path.join(out_dir,
                                          "synthetic_case_%s_stable_convention.out" % case),
                             ["substrate: synthetic. CONVENTION CONTROL run -- the crossing "
                              "call was swapped to the STABLE crossing, which §2 refuses. "
                              "This output exists to be DIFFERENT from the case's own.",
                              "case %s, swapped convention: exit %d ; verdict %s"
                              % (case, code2, got2 if got2 is not None else "(none)")]
                             + list(LIMITS),
                             text2)

            write_output(os.path.join(out_dir, "synthetic_case_%s.out" % case), banner, text)
            results.append((case, expected, got, code, ok))
            print("case %-4s expected %-16s got %-16s exit %d%s  %s"
                  % (case, expected, got if got is not None else "(none)", code, detail,
                     "OK" if ok else "MISMATCH"))
    finally:
        if args.workdir is None:
            shutil.rmtree(temp, ignore_errors=True)

    failed = [r for r in results if not r[4]]
    print()
    if failed:
        print("%d of %d cases did not meet their construction." % (len(failed), len(results)))
        return 3
    print("all %d cases met their construction. The exclusion rule, the disqualification "
          "rule, the control, the criterion and all three verdict branches have executed, "
          "and the registered first-crossing convention is distinguished from the stable "
          "crossing it refuses." % len(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
