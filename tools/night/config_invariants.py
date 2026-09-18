"""Derive the invariant part of the training config from the runs on record, and gate a
new run against it.

Why derived and not handwritten (Ark, 2026-09-18). Gate 7 of the night-5 brief first said
"the resolved config must differ from night 4's in the seed and the id and nothing else".
That list was written by hand from memory of what ought to vary, and it was short by one:
across the eight runs on record the varying part is *four* fields, not three, and the
fourth is `description` -- the wave tag. Night 5's tag is `night5`, which matches no
previous run, so the handwritten form of the gate would have fired on the tag and the
explanation would have arrived *after* the firing. That is the failure mode this file
exists to remove: the gate compares the lines that are invariant across the runs already
on disk, and the set of varying keys is computed from those same runs rather than
remembered.

What it does:

    --derive <slim.json ...>        print the invariant/varying split over the given runs
    --gate <new.slim.json> --against <slim.json ...>
                                   check a new run against the invariants of the others

The comparison is line-based on `resolved_config_yaml` as stored in each run json, because
that string is what the run actually trained under -- not a re-serialisation of it, which
would compare our parser instead of the config.

Exit codes:
    0  derived, or the new run matches every invariant line
    1  usage error, or a file is missing the field
    3  the new run differs on a line that is invariant across the reference runs
"""

import argparse
import collections
import io
import json
import os
import sys


def load_config_lines(path):
    with io.open(path, encoding="utf-8") as handle:
        rec = json.load(handle)
    text = rec.get("resolved_config_yaml")
    if text is None:
        raise KeyError("%s has no resolved_config_yaml" % path)
    return [line.rstrip("\n") for line in text.splitlines()]


def split_invariant(paths):
    """Return (invariant_lines, varying_by_position) over several runs.

    Lines are compared by position. Every run so far serialises the same key order -- a
    property that is asserted rather than assumed: if the line counts differ, the caller
    is told and nothing is derived, because a positional comparison of configs with
    different shapes would silently compare unrelated keys.
    """
    per_run = {}
    for path in paths:
        per_run[path] = load_config_lines(path)

    lengths = {path: len(lines) for path, lines in per_run.items()}
    if len(set(lengths.values())) != 1:
        raise ValueError("configs differ in line count, so a positional comparison is "
                         "not defined: %s" % lengths)

    length = next(iter(lengths.values()))
    invariant, varying = [], collections.OrderedDict()
    for i in range(length):
        values = {path: per_run[path][i] for path in paths}
        distinct = set(values.values())
        if len(distinct) == 1:
            invariant.append((i, next(iter(distinct))))
        else:
            varying[i] = values
    return invariant, varying, length


def key_of(line):
    """The config key a line carries, or "" for a line that is not a key: value."""
    stripped = line.strip()
    if ":" not in stripped:
        return ""
    return stripped.split(":", 1)[0].strip().strip("-").strip()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--derive", nargs="+", metavar="SLIM",
                        help="run jsons to derive the invariant set from")
    parser.add_argument("--gate", metavar="NEW",
                        help="a new run json to check against the derived invariants")
    parser.add_argument("--against", nargs="+", metavar="SLIM",
                        help="the reference run jsons for --gate")
    args = parser.parse_args(argv)

    if args.gate and not args.against:
        parser.error("--gate requires --against")
    if not args.gate and not args.derive:
        parser.error("give --derive or --gate")

    reference = args.against if args.gate else args.derive
    for path in reference + ([args.gate] if args.gate else []):
        if not os.path.exists(path):
            print("missing: %s" % path)
            return 1

    try:
        invariant, varying, length = split_invariant(reference)
    except (KeyError, ValueError) as exc:
        print("refused: %s" % exc)
        return 1

    print("reference runs (%d):" % len(reference))
    for path in reference:
        print("   %s" % path)
    print("resolved_config_yaml: %d lines; %d invariant, %d varying"
          % (length, len(invariant), len(varying)))

    varying_keys = collections.OrderedDict()
    for i, values in varying.items():
        varying_keys.setdefault(key_of(reference and list(values.values())[0]), []).append(i)
    print("varying keys (%d distinct):" % len(varying_keys))
    for key, positions in varying_keys.items():
        print("   %-28s at line%s %s"
              % (key or "(no key)", "" if len(positions) == 1 else "s",
                 ", ".join(str(p + 1) for p in positions)))

    if not args.gate:
        return 0

    new_lines = load_config_lines(args.gate)
    print()
    print("gating %s" % args.gate)
    if len(new_lines) != length:
        print("DIFFERS: the new config has %d lines against %d in the reference set"
              % (len(new_lines), length))
        return 3

    offenders = [(i, expected, new_lines[i])
                 for i, expected in invariant if new_lines[i] != expected]
    if not offenders:
        print("every one of the %d invariant lines matches; the %d varying lines were not "
              "compared, by construction" % (len(invariant), len(varying)))
        print("varying lines in the new run, printed for the record:")
        for i in varying:
            print("   line %-4d %s" % (i + 1, new_lines[i].strip()))
        return 0

    print("DIFFERS on %d invariant line(s) -- night-5 gate 7 calls this a void "
          "comparison:" % len(offenders))
    for i, expected, got in offenders:
        print("   line %d" % (i + 1))
        print("      reference: %s" % expected.strip())
        print("      new run  : %s" % got.strip())
    return 3


if __name__ == "__main__":
    sys.exit(main())
