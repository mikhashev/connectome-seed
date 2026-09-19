"""List every tracked file that carries a contaminating value, so the exclusion list is
generated rather than maintained by hand.

Why this exists. ADR-003 requires that a criterion devised after its numbers are visible be
authored by someone who has not seen them, and protects that by excluding the contaminated
material **by path**. The first version of that list was written by hand and named five
paths. A scan found **seventeen** tracked markdown files carrying the same values on the same
day — including the ADR itself, and including VISION and ROADMAP, which the author has every
reason to open. A list that is wrong by twelve entries on its first day is not a list, it is a
recollection; and each of the three people who could have checked it had already seen the
numbers, so none of them would have noticed by reading.

The values never enter this repository. They are given in a file on the command line, kept by
whoever is *sighted*, and only the **paths** are written out — a path is not a value, so the
blind author may read the output. That is the whole design: the contaminating input stays
outside, the harmless output comes in.

Usage:
    python tools/contamination_scan.py --values <file outside the repo> \
        [--out docs/blind-author-exclusions.txt]

The values file is one literal per line; blank lines and lines starting with '#' are ignored.
Matching is literal and case-sensitive, because these are numbers and verdict strings.

Exit codes:
    0  the scan ran; the output names what it found
    1  usage error, or the values file is missing or empty
"""

import argparse
import io
import os
import subprocess
import sys


def tracked_files(repo):
    out = subprocess.run(["git", "-C", repo, "ls-files"],
                         capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        raise SystemExit("git ls-files failed: %s" % out.stderr.strip())
    return [p for p in out.stdout.splitlines() if p.strip()]


def load_values(path):
    values = []
    for line in io.open(path, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#"):
            values.append(line)
    return values


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--values", required=True,
                        help="file of contaminating literals, kept OUTSIDE this repository")
    parser.add_argument("--repo", default=os.getcwd())
    parser.add_argument("--out", default=None,
                        help="where to write the paths-only list (default: stdout only)")
    args = parser.parse_args(argv)

    if not os.path.exists(args.values):
        print("values file not found: %s" % args.values)
        return 1
    values = load_values(args.values)
    if not values:
        print("values file is empty: %s" % args.values)
        return 1
    if os.path.abspath(args.values).startswith(os.path.abspath(args.repo) + os.sep):
        print("REFUSED: the values file is inside the repository (%s). It must live outside, "
              "or committing it would publish exactly what this scan exists to withhold."
              % args.values)
        return 1

    hits = {}
    for rel in tracked_files(args.repo):
        full = os.path.join(args.repo, rel.replace("/", os.sep))
        try:
            text = io.open(full, encoding="utf-8", errors="ignore").read()
        except (OSError, UnicodeDecodeError):
            continue
        n = sum(1 for v in values if v in text)
        if n:
            hits[rel] = n

    lines = []
    lines.append("# Blind-author exclusion list — GENERATED, do not edit by hand.")
    lines.append("# Produced by tools/contamination_scan.py over %d tracked files against a"
                 % len(tracked_files(args.repo)))
    lines.append("# values file held outside this repository. Paths only: a path is not a")
    lines.append("# value, so this file is safe for the blind author to read. The values are")
    lines.append("# not recorded here and must not be added.")
    lines.append("#")
    lines.append("# Regenerate before any blind session begins. The hand-written list this")
    lines.append("# replaced named five paths; the first scan found 52, so it was wrong by 47")
    lines.append("# entries on its first day (ADR-003).")
    lines.append("#")
    lines.append("# %d files carry at least one contaminating literal:" % len(hits))
    for rel in sorted(hits):
        lines.append(rel)
    lines.append("#")
    lines.append("# Whole directories excluded regardless of scan, because their contents are")
    lines.append("# the values themselves or are untracked:")
    for extra in ("results/diagnostics/reachability/", "results/night5/",
                  "tools/night/night5_*", "the repository history for 2026-09-18 and "
                  "2026-09-19 (git log and git show)",
                  "the DPC Research group thread from 2026-09-18 onward"):
        lines.append(extra)

    text = "\n".join(lines) + "\n"
    print("%d of %d tracked files carry a contaminating literal"
          % (len(hits), len(tracked_files(args.repo))))
    for rel in sorted(hits):
        print("   %s" % rel)
    if args.out:
        out_path = os.path.join(args.repo, args.out)
        io.open(out_path, "w", encoding="utf-8", newline="\n").write(text)
        print("written: %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
