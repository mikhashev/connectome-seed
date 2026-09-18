"""List every verdict-shaped token this script would print, with its line.

Ark's rule, 2026-09-18: *a verdict line in an artefact's output is not evidence until the
quantity it was computed from is shown.* It was earned the hard way -- the reading script
printed `positive control outcome: PASS` for a control that cannot fail, so the one line
the next reader would have quoted certified a check that never ran.

A grep over a list of words is the obvious implementation and the wrong one: it can only
find the verdict words somebody thought of. This walks the AST instead, collects every
string constant that reaches a `print(...)` call -- including the ones assembled through
`.format()` and `.join()`, and including strings bound to a name that is later printed --
and reports every ALL-CAPS token of three or more letters. The output is meant to be read
by a person: each hit is either a computed verdict (fine, the quantity is printed beside
it) or a declaration (fine, if it says so), and the point is that no third kind can hide.

Usage:
    python tools/reachability/verdict_lines.py tools/reachability/read_reachability_endpoint.py

Exit codes:
    0  hits listed (or none found) -- this tool reports, it does not judge
    1  usage error
"""

import ast
import io
import re
import sys

CAPS = re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b")

# Words that are ALL-CAPS for reasons other than asserting a verdict. Kept short and
# explicit: every name here is one a reader can check, rather than a pattern that might
# quietly swallow the next real offender.
NOT_A_VERDICT = {
    "UTC", "CSV", "JSON", "SHA256", "NOT", "AND", "THE", "ALL", "ONE", "TWO",
    "ISO", "CPU", "GPU", "NNN", "IDS",
}


def string_constants(node):
    """Every string constant anywhere inside this expression."""
    out = []
    for child in ast.walk(node):
        if isinstance(child, ast.Constant) and isinstance(child.value, str):
            out.append((child.lineno, child.value))
    return out


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip().splitlines()[0])
        print("usage: verdict_lines.py <script.py>")
        return 1
    path = argv[1]
    source = io.open(path, encoding="utf-8").read()
    tree = ast.parse(source, filename=path)

    # Names bound to a string that is later handed to print(): `verdict = "..."` then
    # print(verdict). Collected separately because the constant and the print are in
    # different statements, which a grep over print lines cannot see.
    printed_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == "print":
            for arg in node.args:
                for sub in ast.walk(arg):
                    if isinstance(sub, ast.Name):
                        printed_names.add(sub.id)

    hits = []

    def record(lineno, text, how):
        for token in CAPS.findall(text):
            if token in NOT_A_VERDICT:
                continue
            hits.append((lineno, token, how, text.strip()[:96]))

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == "print":
            for arg in node.args:
                for lineno, text in string_constants(arg):
                    record(lineno, text, "print")
        elif isinstance(node, ast.Assign):
            targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
            if any(t in printed_names for t in targets):
                for lineno, text in string_constants(node.value):
                    record(lineno, text, "assigned->printed")

    if not hits:
        print("no verdict-shaped tokens found in printed strings")
        return 0

    seen = set()
    print("%-6s %-28s %-18s %s" % ("line", "token", "how", "string"))
    for lineno, token, how, text in sorted(hits):
        key = (lineno, token)
        if key in seen:
            continue
        seen.add(key)
        print("%-6d %-28s %-18s %s" % (lineno, token, how, text))
    print()
    print("%d distinct (line, token) hits. Each must be either computed -- with the "
          "quantity printed beside it -- or marked a declaration." % len(seen))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
