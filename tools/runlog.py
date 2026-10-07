"""Run scripts capture their own stdout and stderr into <output folder>/run.log.

Why this exists (backlog RUN-SCRIPTS-MUST-CAPTURE-THEIR-OWN-STDOUT...): run.log used to be made
by a shell redirect outside the script and copied into the output folder, so it had CRLF line
endings, and a log written inside the repository during the run would trip the script's own
`git status --porcelain` clean-tree check.

Usage in a run script (the order is the point):

    sys.path.insert(0, str(Path(__file__).resolve().parents[N] / "tools"))   # N: up to the repo root
    from runlog import RunLog

    with RunLog(repo_root=ROOT) as rl:
        refusals(...)                                  # pins, cwd, output folder absent
        head, porcelain = rl.check_tree(SCOPE)         # refuses (SystemExit) if dirty
        rl.attach(out_dir)                             # ONLY NOW: out_dir, run.log, .gitattributes
        ...                                            # the run; everything printed lands in run.log
        write_outputs(out_dir, head=head, porcelain=porcelain, ...)   # the licensed snapshot

SCOPE is the pathspec of the clean-tree check: the part of the tree that holds the output folder
and everything the run reads or writes (e.g. ["results/genome/c6", "docs/plans"]); None checks the
whole repository. The outputs record the snapshot check_tree() returned, never a second
`git status`: after attach() the output folder itself shows as untracked.

Ordering argument. From __enter__ on, everything printed is teed to the console and to an
in-memory buffer; nothing touches the disk. attach() creates out_dir/run.log (mode "x": it
refuses to overwrite) and flushes the buffer into it, so the log starts with the lines printed
before the check, including the header. A run refused before attach() leaves no file, so a
refusal cannot leave an untracked folder behind, and the porcelain check always sees the tree as
the run started. After attach() the tree is dirty by design (the run's own outputs), exactly as
it was when the outputs were written after the check; the check has already been passed and
recorded. attach() refuses (RuntimeError) unless check_tree() passed first, so the order is
enforced, not a convention. The header's `git rev-parse HEAD` is read at __enter__; check_tree()
logs the HEAD and porcelain it licensed, and that is the pair the outputs carry.

attach() also writes out_dir/.gitattributes (`* -text`) if the folder has none, so the committed
bytes are not rewritten by line-ending conversion; an existing .gitattributes is left as it is.

The file is UTF-8 with LF endings whatever the console encoding; a console that cannot encode a
character gets it as a backslash escape, the log keeps it. The footer (UTC end time and exit
status) is written and fsynced in __exit__ even when the body raised (the exception is not
suppressed; its traceback is logged first). If the body ends before attach(), nothing is written.
Exit status: 0 on normal end or sys.exit(0/None), the integer for sys.exit(int), 1 for
sys.exit(str) and for any other exception.

Not captured: output written below Python's sys.stdout (C extensions writing to fd 1, child
processes such as multiprocessing workers, and threads that still hold the old stream after
__exit__ restored it). A script whose workers print must return the text and print it in the
parent.
"""
import datetime
import os
import subprocess
import sys
import threading
import traceback
from pathlib import Path

LOG_NAME = "run.log"


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git_head(repo_root=None):
    try:
        r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_root, capture_output=True,
                           text=True, check=True)
        return r.stdout.strip()
    except Exception as e:                             # a missing git must not stop a refusal
        return f"unknown ({type(e).__name__})"


def exit_status(exc):
    """The process exit status an exception (or None) will produce."""
    if exc is None:
        return 0
    if isinstance(exc, SystemExit):
        c = exc.code
        if c is None:
            return 0
        if isinstance(c, bool):                       # bool is an int; sys.exit(True) exits 1
            return int(c)
        return c if isinstance(c, int) else 1
    return 1


class _Tee:
    """A text stream that writes to the original stream and to the RunLog."""

    def __init__(self, orig, owner):
        self._orig, self._owner = orig, owner

    def write(self, s):
        if not isinstance(s, str):
            s = str(s)
        self._owner._record(s)
        try:
            self._orig.write(s)
        except UnicodeError:                           # console cannot encode; the log has it
            enc = getattr(self._orig, "encoding", None) or "ascii"
            self._orig.write(s.encode(enc, "backslashreplace").decode(enc, "replace"))
        return len(s)

    def flush(self):
        try:
            self._orig.flush()
        except (OSError, ValueError):
            pass

    def __getattr__(self, name):                       # encoding, isatty, fileno, ...
        return getattr(self._orig, name)


class RunLog:
    def __init__(self, repo_root=None, argv=None):
        self.repo_root = repo_root
        self.argv = list(sys.argv if argv is None else argv)
        self.path = None
        self._fh = None
        self._buf = []
        self._lock = threading.Lock()
        self._saved = None
        self._cr_pending = False
        self.snapshot = None                           # (head, porcelain) licensed by check_tree()

    # --- recording -------------------------------------------------------------------------
    def _norm(self, s):
        # A CRLF can arrive split across two writes ("...\r" then "\n..."): a trailing CR is
        # held back until the next write shows whether an LF follows it.
        if self._cr_pending:
            s = "\r" + s
            self._cr_pending = False
        if s.endswith("\r"):
            s, self._cr_pending = s[:-1], True
        return s.replace("\r\n", "\n").replace("\r", "\n")

    def _record(self, s):
        with self._lock:
            s = self._norm(s)
            if self._fh is not None:
                self._fh.write(s)
                self._fh.flush()
            else:
                self._buf.append(s)

    def _line(self, s):
        self._record(s + "\n")

    # --- lifecycle -------------------------------------------------------------------------
    def __enter__(self):
        self.start_utc = utc_now()
        self._line(f"runlog: command: {' '.join(self.argv)}")
        self._line(f"runlog: start UTC: {self.start_utc}")
        self._line(f"runlog: git HEAD: {git_head(self.repo_root)}")
        self._saved = (sys.stdout, sys.stderr)
        sys.stdout, sys.stderr = _Tee(sys.stdout, self), _Tee(sys.stderr, self)
        return self

    def check_tree(self, scope=None):
        """The clean-tree check. Reads HEAD and `git status --porcelain [-- scope]`; refuses
        (SystemExit) if the porcelain text is not empty. Returns (head, porcelain) and keeps it as
        self.snapshot: the pair the run's outputs must record. Nothing is written to disk."""
        args = ["git", "status", "--porcelain"] + (["--"] + list(scope) if scope else [])
        head = git_head(self.repo_root)
        r = subprocess.run(args, cwd=self.repo_root, capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"REFUSED: git status failed (rc {r.returncode}): {r.stderr.strip()}")
        porcelain = r.stdout
        self._line(f"runlog: clean-tree check: HEAD {head}; scope "
                   f"{' '.join(scope) if scope else '(whole repository)'}; porcelain "
                   f"{'empty' if not porcelain.strip() else 'NOT EMPTY'}")
        if porcelain.strip():
            raise SystemExit("REFUSED: the working tree is not clean:\n" + porcelain)
        self.snapshot = (head, porcelain)
        return self.snapshot

    def attach(self, out_dir):
        """Create out_dir/run.log and flush what was printed so far. Refuses (RuntimeError)
        unless check_tree() passed first, and refuses to overwrite an existing log. Writes
        out_dir/.gitattributes (`* -text`) if the folder has none, after the log is created, so
        a refusal leaves an existing folder as it was."""
        out_dir = Path(out_dir)
        with self._lock:
            if self.snapshot is None:
                raise RuntimeError("RunLog.attach called before a passed check_tree()")
            if self._fh is not None:
                raise RuntimeError("RunLog.attach called twice")
            out_dir.mkdir(parents=True, exist_ok=True)
            self.path = out_dir / LOG_NAME
            fh = open(self.path, "x", encoding="utf-8", newline="\n")
            ga = out_dir / ".gitattributes"            # committed bytes stay LF (no eol rewrite)
            if not ga.exists():
                ga.write_text("* -text\n", encoding="utf-8", newline="\n")
            fh.write("".join(self._buf))
            fh.flush()
            os.fsync(fh.fileno())
            self._buf.clear()
            self._fh = fh
        return self.path

    def __exit__(self, exc_type, exc, tb):
        sys.stdout.flush()
        sys.stderr.flush()
        if exc is not None and not isinstance(exc, SystemExit):
            self._record("".join(traceback.format_exception(exc_type, exc, tb)))
        elif isinstance(exc, SystemExit) and isinstance(exc.code, str):
            self._line(exc.code)                       # the interpreter prints it after exit
        status = exit_status(exc)
        if self._cr_pending:                           # a bare CR at the very end: a line break
            self._cr_pending = False
            self._record("\n")
        self._line(f"runlog: end UTC: {utc_now()}")
        self._line(f"runlog: exit status: {status}")
        sys.stdout, sys.stderr = self._saved
        with self._lock:
            fh, self._fh = self._fh, None
            self._buf.clear()
        if fh is not None:
            fh.flush()
            os.fsync(fh.fileno())
            fh.close()
        return False
