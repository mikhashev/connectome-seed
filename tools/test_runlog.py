"""Unit tests for tools/runlog.py (tmp_path only; no real data)."""
import io
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runlog import RunLog  # noqa: E402

import subprocess

REPO = None                                            # set by the autouse fixture below


def _git(cwd, *a):
    subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True)


@pytest.fixture(autouse=True)
def clean_repo(tmp_path_factory):
    """A throwaway git repository with one commit and a clean tree, so check_tree() passes."""
    global REPO
    r = tmp_path_factory.mktemp("repo")
    _git(r, "init", "-q")
    _git(r, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "c")
    REPO = r
    yield r


def read(p):
    return Path(p).read_bytes()


def test_lf_only_utf8_and_header_footer(tmp_path, capsys):
    out = tmp_path / "out"
    with RunLog(repo_root=REPO, argv=["x.py", "--a"]) as rl:
        rl.check_tree(); rl.attach(out)
        print("line one\r\nline two")
        sys.stderr.write("err line\r\n")
        print("café ≥")
    raw = read(out / "run.log")
    assert b"\r" not in raw
    lines = raw.decode("utf-8").splitlines()
    assert lines[0] == "runlog: command: x.py --a"
    assert lines[1].startswith("runlog: start UTC: 20") and lines[1].endswith("Z")
    assert lines[2].startswith("runlog: git HEAD: ") and len(lines[2].split()[-1]) == 40
    assert "line two" in lines and "err line" in lines and "café ≥" in lines
    assert lines[-2].startswith("runlog: end UTC: ")
    assert lines[-1] == "runlog: exit status: 0"
    cap = capsys.readouterr()
    assert "line one" in cap.out and "err line" in cap.err   # console still receives output


def test_exception_path_writes_footer_and_propagates(tmp_path):
    out = tmp_path / "out"
    with pytest.raises(ValueError):
        with RunLog(repo_root=REPO, argv=["x"]) as rl:
            rl.check_tree(); rl.attach(out)
            print("before")
            raise ValueError("boom")
    text = read(out / "run.log").decode()
    assert "before" in text and "ValueError: boom" in text and "Traceback" in text
    assert text.splitlines()[-1] == "runlog: exit status: 1"
    assert "runlog: end UTC: " in text


@pytest.mark.parametrize("code,want", [(3, 3), (None, 0), ("REFUSED: x", 1)])
def test_system_exit_statuses(tmp_path, code, want):
    out = tmp_path / "o"
    with pytest.raises(SystemExit):
        with RunLog(repo_root=REPO, argv=["x"]) as rl:
            rl.check_tree(); rl.attach(out)
            sys.exit(code)
    text = read(out / "run.log").decode()
    assert text.splitlines()[-1] == f"runlog: exit status: {want}"
    if isinstance(code, str):
        assert code in text


def test_nothing_on_disk_before_attach_and_refusal_leaves_no_file(tmp_path):
    out = tmp_path / "out"
    with pytest.raises(SystemExit):
        with RunLog(repo_root=REPO, argv=["x"]):
            print("checking")
            assert not out.exists()
            sys.exit("REFUSED: dirty tree")
    assert not out.exists()                                # refused before attach: no folder, no log
    assert list(tmp_path.iterdir()) == []


def test_lines_before_attach_are_in_the_log(tmp_path):
    out = tmp_path / "out"
    with RunLog(repo_root=REPO, argv=["x"]) as rl:
        print("pre-check line")
        rl.check_tree(); rl.attach(out)
        print("post-check line")
    lines = read(out / "run.log").decode().splitlines()
    assert lines.index("pre-check line") < lines.index("post-check line")
    assert lines[0].startswith("runlog: command:")         # header first


def test_attach_refuses_existing_log(tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    (out / "run.log").write_text("old")
    with pytest.raises(FileExistsError):
        with RunLog(repo_root=REPO, argv=["x"]) as rl:
            rl.check_tree(); rl.attach(out)
    assert (out / "run.log").read_text() == "old"


def test_streams_restored(tmp_path):
    before = (sys.stdout, sys.stderr)
    with RunLog(repo_root=REPO, argv=["x"]) as rl:
        rl.check_tree(); rl.attach(tmp_path / "o")
    assert (sys.stdout, sys.stderr) == before


def test_cp1252_console_does_not_break_and_log_keeps_unicode(tmp_path, monkeypatch):
    raw = io.BytesIO()
    console = io.TextIOWrapper(raw, encoding="cp1252", errors="strict", newline="\r\n")
    monkeypatch.setattr(sys, "stdout", console)
    out = tmp_path / "out"
    with RunLog(repo_root=REPO, argv=["x"]) as rl:
        rl.check_tree(); rl.attach(out)
        print("ok ≥ 0.9 — café")             # the >= sign is not in cp1252
    console.flush()
    shown = raw.getvalue().decode("cp1252")
    assert "café" in shown and "\\u2265" in shown     # console got an escape
    text = read(out / "run.log").decode("utf-8")
    assert "ok ≥ 0.9 — café\n" in text and "\r" not in text


def test_crlf_split_across_writes_is_one_line_break(tmp_path):
    out = tmp_path / "out"
    with RunLog(repo_root=REPO, argv=["x"]) as rl:
        rl.check_tree(); rl.attach(out)
        sys.stdout.write("a\r")
        sys.stdout.write("\nb\r")                      # split CRLF, then a bare CR
        sys.stdout.write("c\n")
        sys.stdout.write("end\r")                      # a bare CR as the very last byte
    text = read(out / "run.log").decode()
    body = text.splitlines()[4:-2]                    # header (3) + check line, footer (2)
    assert body == ["a", "b", "c", "end"]
    assert "\r" not in text


def test_attach_writes_gitattributes(tmp_path):
    out = tmp_path / "out"
    with RunLog(repo_root=REPO, argv=["x"]) as rl:
        rl.check_tree(); rl.attach(out)
    assert read(out / ".gitattributes") == b"* -text\n"


def test_attach_before_check_tree_refuses_and_writes_nothing(tmp_path):
    out = tmp_path / "out"
    with pytest.raises(RuntimeError):
        with RunLog(repo_root=REPO, argv=["x"]) as rl:
            rl.attach(out)
    assert not out.exists()


def test_dirty_tree_refuses_before_any_folder(tmp_path):
    (REPO / "stray.txt").write_text("x")
    out = REPO / "results" / "run1"
    with pytest.raises(SystemExit) as e:
        with RunLog(repo_root=REPO, argv=["x"]) as rl:
            rl.check_tree()
            rl.attach(out)
    assert "not clean" in str(e.value.code) and "stray.txt" in str(e.value.code)
    assert not out.exists()


def test_scope_limits_the_check_and_snapshot_is_returned(tmp_path):
    (REPO / "elsewhere.txt").write_text("x")           # dirty outside the scope
    (REPO / "results").mkdir()
    with RunLog(repo_root=REPO, argv=["x"]) as rl:
        head, porcelain = rl.check_tree(["results"])
        rl.attach(REPO / "results" / "run1")
    assert len(head) == 40 and porcelain == "" and rl.snapshot == (head, porcelain)
    text = (REPO / "results" / "run1" / "run.log").read_text(encoding="utf-8")
    assert f"runlog: clean-tree check: HEAD {head}; scope results; porcelain empty" in text


def test_refused_attach_into_existing_folder_leaves_it_as_it_was(tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    (out / "run.log").write_text("old")
    with pytest.raises(FileExistsError):
        with RunLog(repo_root=REPO, argv=["x"]) as rl:
            rl.check_tree(); rl.attach(out)
    assert sorted(x.name for x in out.iterdir()) == ["run.log"]   # no .gitattributes added


def test_sys_exit_true_logs_status_1(tmp_path):
    out = tmp_path / "out"
    with pytest.raises(SystemExit):
        with RunLog(repo_root=REPO, argv=["x"]) as rl:
            rl.check_tree(); rl.attach(out)
            sys.exit(True)
    assert read(out / "run.log").decode().splitlines()[-1] == "runlog: exit status: 1"
