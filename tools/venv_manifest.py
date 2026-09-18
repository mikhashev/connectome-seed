"""Hash a Python environment file by file, and compare two of them.

Why this exists. Until 2026-09-18 the only runnable environment for this project lived in
a session scratchpad under %LOCALAPPDATA%\\Temp whose owning session had ended; it was
copied to tools/.venv so that the committed launcher could start a night. A copy is an
assumption until it is hashed -- robocopy verifies size and timestamp, not content -- and
the claim that has to hold is stronger than "the files came across": the environment that
trains night 5 must be the same one that trained nights 1-4, or their loss curves are not
comparable and every timing gate in the night-5 brief can pass while the comparison is
already void.

So this is the executable form of gate 8 of docs/briefs/2026-09-17-night5.md: a per-file
sha256 of a tree, a combined digest over the sorted (relative path, hash) pairs, and a
diff of two trees naming every file that differs or exists on one side only.

__pycache__ is excluded by default. Compiled caches are regenerated on import, embed the
source's mtime, and differ legitimately between two copies of the same environment; a
digest that included them would report a difference on every run and teach the reader to
ignore it.

Usage:
    python tools/venv_manifest.py <tree>                      write one manifest
    python tools/venv_manifest.py <tree_a> <tree_b>            compare two trees
    python tools/venv_manifest.py <tree_a> <tree_b> --out m.json

Exit codes:
    0  the trees are identical (or a single manifest was written)
    1  usage error, or a tree is missing
    3  the trees differ -- a file is missing on one side, or a hash disagrees

Measured on 2026-09-18: 21,650 files per side, about 85 s per tree for 4.85 GiB.
"""

import argparse
import hashlib
import json
import os
import sys
import time

EXCLUDE_DIRS = ("__pycache__",)
CHUNK = 1 << 20


def hash_tree(root, exclude_dirs=EXCLUDE_DIRS):
    """Return {relative posix path: sha256 hex} for every file under root.

    A file that cannot be read is recorded as "ERROR:<class>" rather than skipped, so an
    unreadable file can never look like an absent one in the comparison below.
    """
    manifest = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace("\\", "/")
            digest = hashlib.sha256()
            try:
                with open(full, "rb") as handle:
                    for chunk in iter(lambda: handle.read(CHUNK), b""):
                        digest.update(chunk)
            except OSError as exc:
                manifest[rel] = "ERROR:%s" % exc.__class__.__name__
                continue
            manifest[rel] = digest.hexdigest()
    return manifest


def combined_digest(manifest):
    """One sha256 over the sorted (path, hash) pairs.

    Path and hash are both fed in with separators, so that no rename can be absorbed by a
    neighbouring field -- the digest changes if a file moves, not only if it changes.
    """
    digest = hashlib.sha256()
    for rel in sorted(manifest):
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(manifest[rel].encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("tree_a")
    parser.add_argument("tree_b", nargs="?", default=None)
    parser.add_argument("--out", default=None, help="write the manifest/report as json")
    parser.add_argument("--include-pycache", action="store_true",
                        help="do not exclude __pycache__ (see the module docstring)")
    args = parser.parse_args(argv)

    exclude = () if args.include_pycache else EXCLUDE_DIRS

    for tree in (args.tree_a, args.tree_b):
        if tree is not None and not os.path.isdir(tree):
            print("not a directory: %s" % tree)
            return 1

    started = time.time()
    print("hashing %s ..." % args.tree_a)
    sys.stdout.flush()
    man_a = hash_tree(args.tree_a, exclude)
    dig_a = combined_digest(man_a)
    print("  %d files, %.1f s" % (len(man_a), time.time() - started))
    print("  combined sha256: %s" % dig_a)

    report = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "excluded_dirs": list(exclude),
        "tree_a": {"root": os.path.abspath(args.tree_a),
                   "file_count": len(man_a),
                   "combined_sha256": dig_a,
                   "per_file_sha256": man_a},
    }

    if args.tree_b is None:
        if args.out:
            with open(args.out, "w", encoding="utf-8") as handle:
                json.dump(report, handle, indent=1, sort_keys=True)
            print("manifest written: %s" % args.out)
        return 0

    mark = time.time()
    print("hashing %s ..." % args.tree_b)
    sys.stdout.flush()
    man_b = hash_tree(args.tree_b, exclude)
    dig_b = combined_digest(man_b)
    print("  %d files, %.1f s" % (len(man_b), time.time() - mark))
    print("  combined sha256: %s" % dig_b)

    only_a = sorted(set(man_a) - set(man_b))
    only_b = sorted(set(man_b) - set(man_a))
    differ = sorted(r for r in (set(man_a) & set(man_b)) if man_a[r] != man_b[r])
    identical = not (only_a or only_b or differ)

    print()
    print("IDENTICAL" if identical else "NOT IDENTICAL")
    print("  only in %s : %d" % (args.tree_a, len(only_a)))
    for rel in only_a[:20]:
        print("     %s" % rel)
    print("  only in %s : %d" % (args.tree_b, len(only_b)))
    for rel in only_b[:20]:
        print("     %s" % rel)
    print("  present in both but differing : %d" % len(differ))
    for rel in differ[:20]:
        print("     %s" % rel)

    report["tree_b"] = {"root": os.path.abspath(args.tree_b),
                        "file_count": len(man_b),
                        "combined_sha256": dig_b,
                        "per_file_sha256": man_b}
    report["identical"] = identical
    report["only_in_tree_a"] = only_a
    report["only_in_tree_b"] = only_b
    report["differing"] = differ

    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=1, sort_keys=True)
        print("report written: %s" % args.out)

    print("total %.1f s" % (time.time() - started))
    return 0 if identical else 3


if __name__ == "__main__":
    sys.exit(main())
