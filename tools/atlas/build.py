#!/usr/bin/env python3
"""Build atlas.html -- a single self-contained page that says where the project is.

Reads only what already exists in machine-readable form in this repository and
writes ONE file (inline CSS + inline JS + inline JSON). Standard library only,
no network, no GPU, no LLM. Nothing under results/ is written or modified; no
*_steps_*.h5 is opened.

Every number on the page is a number this script read off a committed artefact,
or a count / date / duration / axis bound computed from it. No statistic is
recomputed. A source that cannot be parsed becomes a hatched card naming the
file, never a guess.

CLI:
    python tools/atlas/build.py [--out PATH] [--check]
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import io
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
VERDICTS_PATH = HERE / "verdicts.json"

PRIORITIES = ("CRITICAL", "BLOCKER", "HIGH", "MEDIUM", "LOW")
MIKE_PATTERNS = (
    re.compile(r"mike'?s word", re.I),
    re.compile(r"mike decides", re.I),
)


# --------------------------------------------------------------------------
# collector: what was found, what was missing, what refused to parse
# --------------------------------------------------------------------------
class Sources:
    def __init__(self) -> None:
        self.found: list[str] = []
        self.missing: list[str] = []
        self.unparsed: list[dict] = []

    def rel(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(REPO).as_posix()
        except Exception:
            return str(path)

    def hit(self, path: Path) -> None:
        r = self.rel(path)
        if r not in self.found:
            self.found.append(r)

    def gone(self, path: Path) -> None:
        r = self.rel(path)
        if r not in self.missing:
            self.missing.append(r)

    def broke(self, path: Path, reason: str) -> None:
        self.unparsed.append({"path": self.rel(path), "reason": reason})


SRC = Sources()


def read_text(path: Path) -> str | None:
    """Read a text file, tolerating a file that vanishes or is being rewritten."""
    if not path.exists():
        SRC.gone(path)
        return None
    for enc in ("utf-8", "utf-8-sig", "cp1251", "latin-1"):
        try:
            text = path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
        except OSError as exc:
            SRC.broke(path, f"не читается: {exc.__class__.__name__}")
            return None
        SRC.hit(path)
        return text
    SRC.broke(path, "не удалось подобрать кодировку")
    return None


def load_json(path: Path) -> object | None:
    text = read_text(path)
    if text is None:
        return None
    try:
        return json.loads(text)
    except Exception as exc:
        SRC.broke(path, f"JSON не разобран: {exc.__class__.__name__}")
        return None


def read_csv_rows(path: Path) -> list[list[str]] | None:
    """CSV rows with the repository's '#'-comment convention stripped."""
    text = read_text(path)
    if text is None:
        return None
    try:
        rows = list(csv.reader(io.StringIO(text)))
    except Exception as exc:
        SRC.broke(path, f"CSV не разобран: {exc.__class__.__name__}")
        return None
    return [r for r in rows if r and not r[0].lstrip().startswith("#")]


# --------------------------------------------------------------------------
# git
# --------------------------------------------------------------------------
def git(*args: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", *args],
            cwd=str(REPO),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except Exception:
        return None
    if out.returncode != 0:
        return None
    return out.stdout.rstrip("\n")


def collect_git() -> dict:
    info: dict = {"available": False}
    head = git("log", "-1", "--format=%H\x1f%h\x1f%s\x1f%cI")
    if not head:
        return info
    full, short, subject, when = (head.split("\x1f") + ["", "", "", ""])[:4]
    info.update(
        available=True,
        head=full,
        head_short=short,
        head_subject=subject,
        head_date=when,
        branch=git("rev-parse", "--abbrev-ref", "HEAD") or "",
    )

    status = git("status", "--porcelain")
    dirty_lines = [l for l in (status or "").splitlines() if l.strip()]
    info["dirty_count"] = len(dirty_lines)
    tracked = [l for l in dirty_lines if not l.startswith("??")]
    untracked = [l for l in dirty_lines if l.startswith("??")]
    info["dirty_tracked"] = len(tracked)
    info["dirty_untracked"] = len(untracked)
    info["tracked_paths"] = [l[3:].strip().strip('"') for l in tracked][:12]
    # untracked output is dominated by whatever job is writing right now; group it
    groups: dict[str, int] = {}
    for line in untracked:
        path = line[3:].strip().strip('"')
        parts = [p for p in path.replace("\\", "/").split("/") if p]
        key = "/".join(parts[:3]) if len(parts) > 3 else (
            "/".join(parts[:-1]) if len(parts) > 1 else path)
        groups[key or path] = groups.get(key or path, 0) + 1
    info["untracked_groups"] = sorted(
        ({"dir": k, "n": v} for k, v in groups.items()),
        key=lambda g: -g["n"],
    )[:3]

    upstream = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    ahead = None
    if upstream:
        n = git("rev-list", "--count", f"{upstream}..HEAD")
        if n and n.strip().isdigit():
            ahead = int(n.strip())
    info["upstream"] = upstream
    info["ahead"] = ahead

    log = git("log", "-15", "--format=%h\x1f%s\x1f%cI\x1f%an")
    commits = []
    for line in (log or "").splitlines():
        parts = line.split("\x1f")
        if len(parts) == 4:
            commits.append(
                {"sha": parts[0], "subject": parts[1], "date": parts[2], "author": parts[3]}
            )
    info["commits"] = commits

    day = git("log", "--since=24.hours", "--format=%h")
    info["commits_24h"] = len([l for l in (day or "").splitlines() if l.strip()])
    return info


def collect_today(today: _dt.date) -> dict:
    """What moved in the last day: counted, never described."""
    changed: list[str] = []
    for spec in DIAGNOSTICS:
        ddir = REPO / spec["dir"]
        if not ddir.is_dir():
            continue
        for name in spec["controls"]:
            path = ddir / name
            try:
                mtime = _dt.date.fromtimestamp(path.stat().st_mtime)
            except OSError:
                continue
            if mtime == today and spec["title"] not in changed:
                changed.append(spec["title"])
    return {"diagnostics_touched": changed}


# --------------------------------------------------------------------------
# runs: the explicit run -> column mapping, plus each run's own record
# --------------------------------------------------------------------------
RUN_COLUMNS = Path("results/night5/run_columns.csv")


def collect_runs() -> tuple[list[dict], dict]:
    path = REPO / RUN_COLUMNS
    rows = read_csv_rows(path)
    runs: list[dict] = []
    if not rows:
        return runs, {"source": RUN_COLUMNS.as_posix(), "parsed": False}

    header = [h.strip() for h in rows[0]]
    try:
        idx = {name: header.index(name) for name in
               ("run_id", "column", "seed", "role", "run_index_for_seed", "night", "boot_session")}
    except ValueError as exc:
        SRC.broke(path, f"нет ожидаемого столбца: {exc}")
        return runs, {"source": RUN_COLUMNS.as_posix(), "parsed": False}

    for row in rows[1:]:
        if len(row) < len(header):
            continue
        try:
            runs.append(
                {
                    "run_id": row[idx["run_id"]].strip(),
                    "column": row[idx["column"]].strip(),
                    "seed": int(row[idx["seed"]]),
                    "role": row[idx["role"]].strip(),
                    "run_index": int(row[idx["run_index_for_seed"]]),
                    "night": int(row[idx["night"]]),
                    "boot_session": row[idx["boot_session"]].strip(),
                }
            )
        except Exception:
            SRC.broke(path, "строка не разобрана, пропущена")

    # each run's own record: results/night*/*.slim.json, keyed by the "id" inside
    records: dict[str, dict] = {}
    for slim in sorted(REPO.glob("results/night*/*.slim.json")):
        data = load_json(slim)
        if not isinstance(data, dict):
            continue
        rid = str(data.get("id", "")).strip()
        if not rid:
            continue
        records[rid] = {
            "seed": data.get("seed"),
            "started_utc": data.get("started_utc"),
            "finished_utc": data.get("finished_utc"),
            "exit": data.get("exit"),
            "wall_s": data.get("total_train_wall_s"),
            "final_iteration": data.get("final_iteration"),
            "record": SRC.rel(slim),
        }

    for run in runs:
        rec = records.get(run["run_id"])
        if rec:
            run.update({k: v for k, v in rec.items() if k != "seed"})
        else:
            run["record"] = None
        run["label"] = f"особь {run['seed']} · прогон {run['run_index']}"
        run["short"] = f"{run['seed']}.{run['run_index']}"

    meta = {
        "source": RUN_COLUMNS.as_posix(),
        "parsed": True,
        "n_runs": len(runs),
        "n_individuals": len({r["seed"] for r in runs}),
        "records_found": len([r for r in runs if r.get("record")]),
    }
    return runs, meta


# --------------------------------------------------------------------------
# nights
# --------------------------------------------------------------------------
def collect_nights(runs: list[dict]) -> list[dict]:
    nights: list[dict] = []
    for n in range(1, 6):
        ndir = REPO / f"results/night{n}"
        if not ndir.is_dir():
            SRC.gone(ndir)
            continue
        waves = []
        for wave in sorted(ndir.glob("wave_*.json")):
            data = load_json(wave)
            if not isinstance(data, dict):
                continue
            waves.append(
                {
                    "tag": data.get("tag"),
                    "started_utc": data.get("started_utc"),
                    "finished_utc": data.get("finished_utc"),
                    "n_jobs": len(data.get("jobs") or []),
                    "source": SRC.rel(wave),
                }
            )
        killed = []
        for part in sorted(ndir.glob("*killed*.json")):
            data = load_json(part)
            if not isinstance(data, dict):
                continue
            killed.append(
                {
                    "run_id": data.get("id"),
                    "seed": data.get("seed"),
                    "started_utc": data.get("started_utc"),
                    "exit": data.get("exit"),
                    "source": SRC.rel(part),
                }
            )
        night_runs = [r for r in runs if r["night"] == n]
        starts = [r.get("started_utc") for r in night_runs if r.get("started_utc")]
        ends = [r.get("finished_utc") for r in night_runs if r.get("finished_utc")]
        if not starts:
            starts = [w["started_utc"] for w in waves if w.get("started_utc")]
        if not ends:
            ends = [w["finished_utc"] for w in waves if w.get("finished_utc")]
        readmes = []
        for cand in ("README.md", "night_report.md"):
            if (ndir / cand).exists():
                readmes.append(f"results/night{n}/{cand}")
        nights.append(
            {
                "n": n,
                "started_utc": min(starts) if starts else None,
                "finished_utc": max(ends) if ends else None,
                "runs": [r["run_id"] for r in night_runs],
                "killed": killed,
                "waves": waves,
                "readmes": readmes,
                "experiment": experiment_doc(n),
            }
        )
    return nights


def experiment_doc(n: int) -> str | None:
    matches = sorted((REPO / "docs/experiments").glob(f"{n:03d}-*.md"))
    if matches:
        SRC.hit(matches[0])
        return SRC.rel(matches[0])
    return None


# --------------------------------------------------------------------------
# learning curves
# --------------------------------------------------------------------------
CHECKPOINTS = Path("results/night5/night_report_checkpoints.csv")
PENALISED_CSV = Path("results/night5/diagnostics/rowB/penalised_quantity_by_checkpoint.csv")
PENALISED_MD = Path("results/night5/diagnostics/rowB/PENALISED-QUANTITY-READING.md")


def collect_curves(runs: list[dict]) -> dict:
    path = REPO / CHECKPOINTS
    rows = read_csv_rows(path)
    out: dict = {"source": CHECKPOINTS.as_posix(), "parsed": False, "series": [], "iterations": []}
    if not rows or len(rows) < 2:
        return out
    header = [h.strip() for h in rows[0]]
    if header[0] != "iteration":
        SRC.broke(path, "первый столбец не 'iteration'")
        return out
    by_column = {r["column"]: r for r in runs}
    iterations: list[int] = []
    columns: dict[str, list] = {h: [] for h in header[1:]}
    for row in rows[1:]:
        if len(row) != len(header):
            continue
        try:
            iterations.append(int(float(row[0])))
        except ValueError:
            continue
        for i, name in enumerate(header[1:], start=1):
            cell = row[i].strip()
            try:
                columns[name].append(float(cell))
            except ValueError:
                columns[name].append(None)
    series = []
    unmapped = []
    for name in header[1:]:
        run = by_column.get(name)
        if run is None:
            unmapped.append(name)
            continue
        series.append(
            {
                "column": name,
                "run_id": run["run_id"],
                "seed": run["seed"],
                "role": run["role"],
                "run_index": run["run_index"],
                "night": run["night"],
                "label": run["label"],
                "values": columns[name],
            }
        )
    series.sort(key=lambda x: (x["seed"], x["run_index"]))
    out.update(
        parsed=True,
        iterations=iterations,
        series=series,
        n_points=len(iterations),
        unmapped_columns=unmapped,
        mapping_source=RUN_COLUMNS.as_posix(),
    )
    return out


def collect_penalised(runs: list[dict]) -> dict:
    """The free falsifier's tidy extract: one row per (run, checkpoint).

    Plotted the way the reading's own figure plots it (PENALISED-QUANTITY-READING.md
    §9): `pre_weight` against `chkpt_iter`, one hue per individual.
    """
    csv_path = REPO / PENALISED_CSV
    md_path = REPO / PENALISED_MD
    out = {
        "csv": PENALISED_CSV.as_posix(),
        "md": PENALISED_MD.as_posix(),
        "present": csv_path.exists(),
        "reading_present": md_path.exists(),
        "parsed": False,
        "series": [],
    }
    if md_path.exists():
        SRC.hit(md_path)
    if not csv_path.exists():
        SRC.gone(csv_path)
        return out
    rows = read_csv_rows(csv_path)
    if not rows or len(rows) < 2:
        SRC.broke(csv_path, "пустой или без заголовка")
        return out
    header = [h.strip() for h in rows[0]]
    need = {}
    for want, alts in (
        ("run", ("run_id", "run_label")),
        ("x", ("chkpt_iter", "solver_iteration", "iteration")),
        ("y", ("pre_weight", "weighted")),
    ):
        for alt in alts:
            if alt in header:
                need[want] = header.index(alt)
                need[want + "_name"] = alt
                break
    if not {"run", "x", "y"} <= set(need):
        SRC.broke(csv_path, "нет столбцов run_id / chkpt_iter / pre_weight")
        return out

    by_run: dict[str, list[list[float]]] = {}
    for row in rows[1:]:
        if len(row) < len(header):
            continue
        try:
            x = float(row[need["x"]])
            y = float(row[need["y"]])
        except ValueError:
            continue
        by_run.setdefault(row[need["run"]].strip(), []).append([x, y])

    lookup = {r["run_id"]: r for r in runs}
    series = []
    for key, pts in by_run.items():
        pts.sort(key=lambda p: p[0])
        run = lookup.get(key)
        series.append(
            {
                "key": key,
                "run_id": key,
                "seed": run["seed"] if run else None,
                "role": run["role"] if run else "canonical",
                "run_index": run["run_index"] if run else None,
                "label": run["label"] if run else key,
                "points": pts,
            }
        )
    series.sort(key=lambda s: (s["seed"] if s["seed"] is not None else 99,
                               s["run_index"] or 0))
    out.update(
        parsed=bool(series),
        series=series,
        x_column=need.get("x_name"),
        y_column=need.get("y_name"),
        n_rows=sum(len(s["points"]) for s in series),
    )
    return out


# --------------------------------------------------------------------------
# diagnostics
# --------------------------------------------------------------------------
DIAGNOSTICS = [
    {
        "id": "ablation-night2",
        "title": "Абляция (ночь 2)",
        "dir": "results/night2/diagnostics/ablation",
        "readme": "results/night2/diagnostics/ablation/README.md",
        "controls": ["ablation_controls.json"],
    },
    {
        "id": "ablation-night3",
        "title": "Абляция (ночь 3)",
        "dir": "results/night3/diagnostics/ablation",
        "readme": "results/night3/diagnostics/ablation/README.md",
        "controls": ["ablation_controls.json"],
    },
    {
        "id": "rowB-night2",
        "title": "Ряд B (ночь 2)",
        "dir": "results/night2/diagnostics/rowB",
        "readme": "results/night2/diagnostics/rowB/README.md",
        "controls": ["rowB_controls.json"],
    },
    {
        "id": "rowB-night3",
        "title": "Ряд B (ночь 3)",
        "dir": "results/night3/diagnostics/rowB",
        "readme": "results/night3/diagnostics/rowB/README.md",
        "controls": ["rowB_controls.json"],
    },
    {
        "id": "rowB-night5",
        "title": "Ряд B, ночь 5 — обычный режим",
        "instrument": "обычный режим (как шли ночи): --no-determinism",
        "dir": "results/night5/diagnostics/rowB",
        "readme": "results/night5/diagnostics/rowB/README.md",
        "controls": [
            "rowB_controls.json",
            "rowB_controls_floor_proc1.json",
            "rowB_controls_floor_proc2.json",
            "rowB_controls_floor_proc3.json",
        ],
    },
    {
        "id": "rowB-night5-det",
        "title": "Ряд B, ночь 5 — детерминированный режим",
        "instrument": "детерминированный режим: отдельный прибор, файлы с суффиксом _det",
        "dir": "results/night5/diagnostics/rowB",
        "readme": "results/night5/diagnostics/rowB/README.md",
        "controls": [
            "rowB_controls_det.json",
            "rowB_controls_floor_proc1_det.json",
            "rowB_controls_floor_proc2_det.json",
            "rowB_controls_floor_proc3_det.json",
        ],
    },
    {
        "id": "gray",
        "title": "Серый стимул",
        "dir": "results/diagnostics/gray",
        "readme": "results/diagnostics/gray/README.md",
        "controls": ["gray_controls.json", "gray_repeat_controls.json"],
    },
    {
        "id": "c3",
        "title": "C3 — джиттер траектории и пол оценщика",
        "dir": "results/diagnostics/c3",
        "readme": "results/diagnostics/c3/README.md",
        "controls": ["readings.json"],
    },
    {
        "id": "reachability",
        "title": "Достижимость (зарегистрированный endpoint)",
        "dir": "results/diagnostics/reachability",
        "readme": None,
        "controls": ["reachability_reading.json"],
        "verdict_field": "verdict",
    },
    {
        "id": "window",
        "title": "Оконный интеграл",
        "dir": "results/diagnostics/window",
        "readme": "results/diagnostics/window/README.md",
        "controls": ["window_readings.json"],
    },
    {
        "id": "connectivity",
        "title": "Связность",
        "dir": "results/night2/diagnostics/connectivity",
        "readme": "results/night2/diagnostics/connectivity/README.md",
        "controls": ["connectivity_summary.json"],
    },
    {
        "id": "dropk",
        "title": "Drop-k",
        "dir": "results/night2/diagnostics/dropk",
        "readme": "results/night2/diagnostics/dropk/README.md",
        "controls": ["dropk_results.json"],
    },
]

PASS_KEY = re.compile(r"(^|_)pass(_|$)", re.I)

# a heading under which a README states what its instrument shows
SHOWS_HEADING = re.compile(
    r"^#{2,4}\s*[\d.]*\s*.*?(what this (?:does not |cannot )?(?:show|say|do)|"
    r"what this is not|conclusion|verdict).*$",
    re.I | re.M,
)
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-ZА-Я«\"'`*])")


def first_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    parts = SENTENCE_END.split(text, maxsplit=1)
    out = parts[0].strip()
    return out[:400]


def readme_quote(readme_rel: str | None) -> dict | None:
    """One sentence from the instrument's own README, quoted in its own language.

    Preferred: the paragraph under a 'what this does not show' heading. Failing
    that, the README's leading bold status line. Nothing is paraphrased here.
    """
    if not readme_rel:
        return None
    path = REPO / readme_rel
    text = read_text(path)
    if not text:
        return None
    m = SHOWS_HEADING.search(text)
    if m:
        after = text[m.end():].lstrip("\n")
        para = after.split("\n\n", 1)[0]
        para = re.sub(r"^\s*[>|]\s*", "", para)
        sentence = first_sentence(para)
        if len(sentence) > 25:
            return {"text": sentence, "path": readme_rel, "kind": "what-this-shows"}
    for line in text.splitlines()[:30]:
        if re.match(r"^\s*\*\*(status|статус)", line, re.I):
            sentence = first_sentence(re.sub(r"\*\*", "", line))
            if len(sentence) > 10:
                return {"text": sentence, "path": readme_rel, "kind": "status"}
    return None


def count_pass_fields(obj: object) -> dict:
    """Count boolean fields whose key names a pass, anywhere in the document.

    The repository writes its controls' verdicts as boolean `pass` fields (or
    `pass_le_1e-2`, `pass_all`, ...). Nothing here interprets them: the counts
    are counts, grouped by the field's own name.
    """
    per_name: dict[str, dict[str, int]] = {}

    def walk(node: object) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, bool) and PASS_KEY.search(str(key)):
                    slot = per_name.setdefault(str(key), {"true": 0, "false": 0})
                    slot["true" if value else "false"] += 1
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(obj)
    total_t = sum(v["true"] for v in per_name.values())
    total_f = sum(v["false"] for v in per_name.values())
    return {"by_field": per_name, "passed": total_t, "failed": total_f}


def collect_diagnostics() -> list[dict]:
    tiles = []
    for spec in DIAGNOSTICS:
        ddir = REPO / spec["dir"]
        tile = {
            "id": spec["id"],
            "title": spec["title"],
            "instrument": spec.get("instrument"),
            "dir": spec["dir"],
            "readme": spec.get("readme"),
            "quote": None,
            "ran": False,
            "controls": [],
            "passed": 0,
            "failed": 0,
            "recorded_verdict": None,
            "status_line": None,
            "sources": [],
        }
        if not ddir.is_dir():
            SRC.gone(ddir)
            tiles.append(tile)
            continue
        if tile["readme"] and not (REPO / tile["readme"]).exists():
            tile["readme"] = None
        tile["quote"] = readme_quote(tile["readme"])
        for name in spec["controls"]:
            cpath = ddir / name
            if not cpath.exists():
                SRC.gone(cpath)
                tile["controls"].append({"file": name, "present": False})
                continue
            data = load_json(cpath)
            if data is None:
                tile["controls"].append(
                    {"file": name, "present": True, "parsed": False,
                     "reason": "JSON не разобран"}
                )
                continue
            counts = count_pass_fields(data)
            entry = {
                "file": name,
                "present": True,
                "parsed": True,
                "passed": counts["passed"],
                "failed": counts["failed"],
                "by_field": counts["by_field"],
            }
            if isinstance(data, dict):
                status = data.get("status")
                if isinstance(status, str):
                    entry["status"] = status
                    tile["status_line"] = tile["status_line"] or status
                n_entries = data.get("entries")
                if isinstance(n_entries, dict):
                    entry["n_entries"] = len(n_entries)
                vfield = spec.get("verdict_field")
                if vfield and isinstance(data.get(vfield), str):
                    tile["recorded_verdict"] = data[vfield]
            tile["controls"].append(entry)
            tile["ran"] = True
            tile["passed"] += counts["passed"]
            tile["failed"] += counts["failed"]
            tile["sources"].append(f"{spec['dir']}/{name}")
        if not tile["ran"]:
            # a directory with outputs but no parseable controls still "ran"
            outputs = [p for p in ddir.glob("*.json")]
            tile["ran"] = bool(outputs)
        tiles.append(tile)
    return tiles


# --------------------------------------------------------------------------
# backlog
# --------------------------------------------------------------------------
ENVELOPE = re.compile(
    r"^###\s+(?P<name>[A-Z0-9][A-Z0-9-]*):\s*(?P<sentence>.*?)\s*"
    r"\((?P<priority>CRITICAL|BLOCKER|HIGH|MEDIUM|LOW),\s*"
    r"(?P<status>[a-z][a-z \-]*?),\s*(?P<date>\d{4}-\d{2}-\d{2})\s*"
    r"(?:—|--|–)\s*(?P<origin>.*)\)\s*$"
)


def parse_backlog(path: Path) -> tuple[list[dict], int]:
    text = read_text(path)
    if text is None:
        return [], 0
    lines = text.splitlines()
    headers = [(i, l) for i, l in enumerate(lines) if l.startswith("### ")]
    entries: list[dict] = []
    unparsed = 0
    for pos, (i, line) in enumerate(headers):
        m = ENVELOPE.match(line)
        # a long envelope may be wrapped over several lines
        j = i
        while m is None and j + 1 < len(lines) and j - i < 5:
            nxt = lines[j + 1].strip()
            if not nxt or nxt.startswith(("#", "- ", "* ", ">")):
                break
            j += 1
            line = line.rstrip() + " " + nxt
            m = ENVELOPE.match(line)
        if not m:
            unparsed += 1
            continue
        end = headers[pos + 1][0] if pos + 1 < len(headers) else len(lines)
        body = "\n".join(lines[i + 1:end])
        axis = None
        am = re.search(r"\*\*axis:\*\*\s*([a-z]+)", body)
        if am:
            axis = am.group(1)
        haystack = line + "\n" + body
        awaits = any(p.search(haystack) for p in MIKE_PATTERNS)
        entries.append(
            {
                "name": m.group("name"),
                "sentence": m.group("sentence"),
                "priority": m.group("priority"),
                "status": m.group("status"),
                "date": m.group("date"),
                "origin": m.group("origin"),
                "axis": axis,
                "awaits_mike_text": awaits,
                "source": SRC.rel(path),
            }
        )
    return entries, unparsed


def collect_backlog(today: _dt.date) -> dict:
    open_entries, open_bad = parse_backlog(REPO / "backlog.md")
    closed_entries, closed_bad = parse_backlog(REPO / "backlog_closed.md")
    for entry in open_entries + closed_entries:
        try:
            d = _dt.date.fromisoformat(entry["date"])
            # the board's dates are calendar days written by hand; this machine is
            # UTC+7, so an entry filed today can look like tomorrow. Never negative.
            entry["age_days"] = max(0, (today - d).days)
        except Exception:
            entry["age_days"] = None
    by_priority: dict[str, int] = {}
    by_status: dict[str, int] = {}
    for e in open_entries:
        by_priority[e["priority"]] = by_priority.get(e["priority"], 0) + 1
        by_status[e["status"]] = by_status.get(e["status"], 0) + 1
    iso_today = today.isoformat()
    return {
        "open": open_entries,
        "closed_count": len(closed_entries),
        "open_count": len(open_entries),
        "unparsed_headers": open_bad + closed_bad,
        "by_priority": by_priority,
        "by_status": by_status,
        "opened_today": len([e for e in open_entries if e["date"] == iso_today]),
        "closed_today": len([e for e in closed_entries if e["date"] == iso_today]),
        "sources": ["backlog.md", "backlog_closed.md"],
        "view": "backlog.html",
        "view_present": (REPO / "backlog.html").exists(),
    }


# --------------------------------------------------------------------------
# decisions
# --------------------------------------------------------------------------
def collect_decisions() -> list[dict]:
    out = []
    ddir = REPO / "docs/decisions"
    if not ddir.is_dir():
        SRC.gone(ddir)
        return out
    for path in sorted(ddir.glob("*.md")):
        if path.name == "TEMPLATE.md":
            continue
        text = read_text(path)
        if text is None:
            continue
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
        if not m:
            SRC.broke(path, "нет front matter")
            continue
        fm = m.group(1)

        def field(name: str) -> str | None:
            fm_m = re.search(rf"^{name}:\s*(.+?)\s*$", fm, re.M)
            if not fm_m:
                return None
            return fm_m.group(1).strip().strip('"').strip("'")

        out.append(
            {
                "adr": field("adr"),
                "title": field("title"),
                "status": field("status"),
                "date": field("date"),
                "axis": field("axis"),
                "path": SRC.rel(path),
            }
        )
    return out


# --------------------------------------------------------------------------
# verdicts
# --------------------------------------------------------------------------
def collect_verdicts() -> tuple[dict, dict]:
    """Card verdicts, and the Russian restatements of board entries beside them."""
    data = load_json(VERDICTS_PATH)
    if not isinstance(data, dict):
        return {}, {}

    ru: dict[str, dict] = {}
    raw_ru = data.get("backlog_ru")
    if isinstance(raw_ru, dict):
        for name, value in raw_ru.items():
            if name.startswith("_") or not isinstance(value, dict):
                continue
            src = value.get("source")
            if isinstance(src, str):
                src = [src]
            elif not isinstance(src, list):
                src = ["backlog.md"]
            ru[name] = {
                "text": value.get("text"),
                "ask": value.get("ask"),
                "source": [str(s) for s in src],
            }

    clean: dict[str, dict] = {}
    for key, value in data.items():
        if key.startswith("_") or key == "backlog_ru":
            continue
        if not isinstance(value, dict):
            continue
        sources = value.get("source")
        if isinstance(sources, str):
            sources = [sources]
        elif not isinstance(sources, list):
            sources = []
        clean[key] = {
            "text": value.get("text"),
            "source": [str(s) for s in sources],
            "awaits_mike": bool(value.get("awaits_mike", False)),
            "title": value.get("title"),
        }
    return clean, ru


# --------------------------------------------------------------------------
# assembly
# --------------------------------------------------------------------------
def build_data() -> dict:
    now = _dt.datetime.now(_dt.timezone.utc)
    today = now.date()
    runs, runs_meta = collect_runs()
    verdicts, backlog_ru = collect_verdicts()
    data = {
        "built_utc": now.replace(microsecond=0).isoformat(),
        "built_local": _dt.datetime.now().replace(microsecond=0).isoformat(sep=" "),
        "repo": REPO.name,
        "git": collect_git(),
        "runs": runs,
        "runs_meta": runs_meta,
        "nights": collect_nights(runs),
        "curves": collect_curves(runs),
        "penalised": collect_penalised(runs),
        "diagnostics": collect_diagnostics(),
        "backlog": collect_backlog(today),
        "decisions": collect_decisions(),
        "verdicts": verdicts,
        "backlog_ru": backlog_ru,
        "today": collect_today(today),
    }
    data["sources"] = {
        "found": SRC.found,
        "missing": SRC.missing,
        "unparsed": SRC.unparsed,
    }
    return data


# --------------------------------------------------------------------------
# the page
# --------------------------------------------------------------------------
PAGE = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Атлас — connectome-seed</title>
<style>
:root{
  color-scheme: light;
  --bg:#f7f7f5; --surface:#fcfcfb; --surface-2:#f1f0ed; --line:#dedcd6;
  --ink:#131312; --ink-2:#52514e; --ink-3:#7a7873;
  --accent:#1c5cab; --ok:#1baf7a; --bad:#e34948; --warn:#eda100;
  --hatch:#c9c6bd; --hatch-bg:#efeee9;
  --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --s4:#eda100; --s5:#e87ba4; --s6:#008300;
  --grid:#e4e2dc;
}
@media (prefers-color-scheme: dark){
  :root{
    color-scheme: dark;
    --bg:#131312; --surface:#1a1a19; --surface-2:#232321; --line:#383835;
    --ink:#f4f3ef; --ink-2:#c3c2b7; --ink-3:#8f8e86;
    --accent:#6da7ec; --ok:#199e70; --bad:#e66767; --warn:#c98500;
    --hatch:#4a4a45; --hatch-bg:#232321;
    --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; --s5:#d55181; --s6:#008300;
    --grid:#2e2e2b;
  }
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{
  background:var(--bg); color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif;
  font-size:15px; line-height:1.5; overflow-x:hidden;
}
.wrap{max-width:1100px; margin:0 auto; padding:24px 16px 72px}
h1{font-size:22px; margin:0 0 4px; letter-spacing:-0.01em}
h2{font-size:15px; margin:40px 0 12px; text-transform:uppercase; letter-spacing:0.08em; color:var(--ink-2); font-weight:600}
h3{font-size:15px; margin:0 0 6px; font-weight:600}
p{margin:0 0 8px}
a{color:var(--accent)}
a:focus-visible,button:focus-visible,[tabindex]:focus-visible{outline:2px solid var(--accent); outline-offset:2px; border-radius:3px}
code,.mono{font-family:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace; font-size:0.92em}
.sub{color:var(--ink-2); font-size:13px}
.card{background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:16px}
.grid{display:grid; gap:12px}
.g2{grid-template-columns:repeat(auto-fit,minmax(310px,1fr))}
.g3{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.verdict{font-size:17px; line-height:1.45; color:var(--ink); font-weight:500; margin:0 0 10px}
.src{font-size:12px; color:var(--ink-3); margin-top:10px; word-break:break-word}
.src b{font-weight:600; color:var(--ink-3)}
.hatch{
  border:1px dashed var(--hatch); border-radius:6px; padding:10px 12px; margin:0 0 10px;
  background-image:repeating-linear-gradient(45deg,var(--hatch-bg),var(--hatch-bg) 6px,transparent 6px,transparent 12px);
  color:var(--ink-2); font-size:14px;
}
.hatch b{display:block; font-size:12px; text-transform:uppercase; letter-spacing:0.06em; color:var(--ink-3); margin-bottom:3px; font-weight:600}
.kv{display:flex; flex-wrap:wrap; gap:6px 16px; font-size:13px; color:var(--ink-2); margin:6px 0 0}
.kv span b{color:var(--ink); font-weight:600}
.pill{display:inline-block; padding:1px 7px; border-radius:999px; border:1px solid var(--line); font-size:12px; background:var(--surface-2); color:var(--ink-2); white-space:nowrap}
.pill.ok{border-color:var(--ok); color:var(--ok)}
.pill.bad{border-color:var(--bad); color:var(--bad)}
.pill.warn{border-color:var(--warn); color:var(--warn)}
.strip{display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:12px}
.night{background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:12px}
.night h3{font-size:14px}
.runrow{display:flex; gap:8px; align-items:baseline; flex-wrap:wrap; padding:8px 0; border-top:1px solid var(--line)}
.runrow:first-of-type{border-top:0}
.chip{display:inline-flex; align-items:center; gap:6px; flex-wrap:wrap; border:1px solid var(--line); border-radius:6px; padding:3px 9px; font-size:12.5px; background:var(--surface-2); max-width:100%}
.chip .mono{white-space:nowrap}
.chip .dot{width:9px; height:9px; border-radius:2px; flex:none}
.chip.rep{border-style:dashed}
.chip .mono{color:var(--ink-2)}
table{border-collapse:collapse; width:100%; font-size:13px}
th,td{text-align:left; padding:6px 10px 6px 0; border-bottom:1px solid var(--line); vertical-align:top}
th{color:var(--ink-3); font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:0.05em}
ul{margin:0 0 8px; padding-left:18px}
li{margin:0 0 5px}
button{font:inherit; color:var(--ink); background:var(--surface-2); border:1px solid var(--line); border-radius:6px; padding:4px 10px; cursor:pointer}
button:hover{background:var(--surface)}
button[aria-pressed="true"]{border-color:var(--accent); color:var(--accent)}
.chartbox{overflow-x:auto; overflow-y:hidden; -webkit-overflow-scrolling:touch}
.chartbox svg{display:block; min-width:660px}
.legend{display:flex; flex-wrap:wrap; gap:6px; margin:10px 0 0}
.legend button{display:inline-flex; align-items:center; gap:6px; font-size:12.5px; padding:3px 8px}
.legend button[aria-pressed="false"]{opacity:0.42}
.legend svg{flex:none}
#tip{
  position:fixed; pointer-events:none; z-index:20; opacity:0;
  background:var(--surface); border:1px solid var(--line); border-radius:6px;
  padding:6px 9px; font-size:12.5px; color:var(--ink); box-shadow:0 2px 10px rgba(0,0,0,0.13);
  max-width:260px;
}
.axlabel{font-size:11px; fill:var(--ink-3)}
.marklabel{font-size:11px; fill:var(--ink-2)}
.endlabel{font-size:10.5px; fill:var(--ink-2)}
.foot{margin-top:48px; padding-top:14px; border-top:1px solid var(--line); color:var(--ink-3); font-size:12.5px}
header.top{padding:0 0 4px}
.stamp{color:var(--ink-3); font-size:12.5px; margin:2px 0 10px}
nav.mini{
  position:sticky; top:0; z-index:10; margin:0 -16px 8px; padding:8px 16px;
  background:var(--bg); border-bottom:1px solid var(--line);
  display:flex; flex-wrap:wrap; gap:4px 6px;
}
nav.mini a{
  font-size:12.5px; color:var(--ink-2); text-decoration:none; white-space:nowrap;
  border:1px solid var(--line); border-radius:999px; padding:2px 9px; background:var(--surface);
}
nav.mini a:hover{color:var(--accent); border-color:var(--accent)}
section{scroll-margin-top:56px}
.quote{
  margin:8px 0 0; padding:8px 10px; border-left:3px solid var(--line);
  background:var(--surface-2); color:var(--ink-2); font-size:13px;
}
.quote b{display:block; font-size:11px; text-transform:uppercase; letter-spacing:0.06em; color:var(--ink-3); margin-bottom:3px}
.quote b .path{text-transform:none; letter-spacing:0; word-break:break-all}
.pill.wrap{white-space:normal; word-break:break-word; max-width:100%}
.ask{margin:8px 0 0; font-size:14px; color:var(--ink)}
.ask b{color:var(--ink-3); font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:0.06em; display:block; margin-bottom:2px}
.repo{font-size:13px; padding:12px 14px}
.repo h3{font-size:13px; color:var(--ink-2)}
.instr{font-size:12.5px; color:var(--ink-2); margin:0 0 6px}
.toolbar{display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin:4px 0 10px}
.toolbar .sub{margin-right:2px}
@media (max-width:560px){
  .wrap{padding:16px 16px 56px}
  h1{font-size:19px}
  .verdict{font-size:16px}
}
</style>
</head>
<body>
<div class="wrap" id="app"></div>
<div id="tip" role="status" aria-live="polite"></div>
<script id="atlas-data" type="application/json">__DATA__</script>
<script>
"use strict";
const D = JSON.parse(document.getElementById("atlas-data").textContent);
const app = document.getElementById("app");

function esc(s){
  return String(s == null ? "" : s).replace(/[&<>"']/g, c =>
    ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}
function el(html){ const t = document.createElement("template"); t.innerHTML = html.trim(); return t.content.firstElementChild; }
function plural(n, one, few, many){
  const a = Math.abs(n) % 100, b = a % 10;
  if (a > 10 && a < 20) return many;
  if (b > 1 && b < 5) return few;
  if (b === 1) return one;
  return many;
}
function fmtDate(iso){
  if (!iso) return "—";
  const d = new Date(iso);
  if (isNaN(d)) return esc(iso);
  const p = n => String(n).padStart(2, "0");
  return d.getFullYear() + "-" + p(d.getMonth()+1) + "-" + p(d.getDate());
}
function fmtDateTime(iso){
  if (!iso) return "—";
  const d = new Date(iso);
  if (isNaN(d)) return esc(iso);
  const p = n => String(n).padStart(2, "0");
  return fmtDate(iso) + " " + p(d.getHours()) + ":" + p(d.getMinutes());
}
function fmtDur(sec){
  if (sec == null || isNaN(sec)) return null;
  let h = Math.floor(sec / 3600), m = Math.round((sec - h*3600) / 60);
  if (m === 60){ h += 1; m = 0; }          // 3 ч 60 мин is not a duration
  return h > 0 ? (h + " ч " + String(m).padStart(2,"0") + " мин") : (m + " мин");
}
function srcLine(paths){
  const list = [...new Set((paths || []).filter(Boolean))];
  if (!list.length) return "";
  return '<div class="src"><b>источник:</b> ' + list.map(p => '<span class="mono">' + esc(p) + "</span>").join(" · ") + "</div>";
}
function hatch(kind, text){
  return '<div class="hatch"><b>' + esc(kind) + "</b>" + esc(text) + "</div>";
}
// A card's plain-language verdict, or the visible debt of not having one.
function verdictBlock(id){
  const v = D.verdicts[id];
  if (v && v.text) {
    return '<p class="verdict">' + esc(v.text) + "</p>" + srcLine(v.source);
  }
  return hatch("не объяснено", "Для карточки «" + id + "» нет текста в tools/atlas/verdicts.json.");
}
function hasVerdict(id){ const v = D.verdicts[id]; return !!(v && v.text); }
function verdictText(id){
  const v = D.verdicts[id];
  return (v && v.text) ? '<p class="verdict">' + esc(v.text) + "</p>" : "";
}
function verdictSources(id){ const v = D.verdicts[id]; return (v && v.source) || []; }

const SERIES_VARS = ["--s1","--s2","--s3","--s4","--s5","--s6"];
const seeds = [...new Set(D.runs.map(r => r.seed))].sort((a,b) => a-b);
function seedColor(seed){
  const i = seeds.indexOf(seed);
  return "var(" + SERIES_VARS[(i < 0 ? 0 : i) % SERIES_VARS.length] + ")";
}

const NAV = [
  ["a","Где мы сейчас"], ["b","Ждёт слова Mike"], ["c","Лента ночей"], ["d","Мухи"],
  ["e","Кривые обучения"], ["f","Приборы и контроли"], ["g","Борд"], ["h","Последние события"],
];
function sectionHeader(){
  const g = D.git || {};
  const h = el("<header class=\"top\"></header>");
  h.innerHTML =
    "<h1>Атлас — connectome-seed</h1>" +
    '<div class="stamp">собрано: <b>' + esc(D.built_local) + "</b> · HEAD <span class=\"mono\">" +
      esc(g.head_short || "—") + "</span> · ветка <span class=\"mono\">" + esc(g.branch || "—") + "</span></div>" +
    '<nav class="mini" aria-label="Разделы">' +
      NAV.map(([id, name]) => '<a href="#' + id + '">' + esc(name) + "</a>").join("") +
    "</nav>";
  return h;
}

/* ------------------------------------------------------------------ A */
function whatsNew(){
  const g = D.git || {}, b = D.backlog, t = (D.today || {});
  const bits = [];
  const c = g.commits_24h;
  if (c != null) bits.push(c === 0 ? "коммитов за сутки нет" :
    c + " " + plural(c,"коммит","коммита","коммитов") + " за сутки");
  if (b.opened_today) bits.push(b.opened_today + " " + plural(b.opened_today,"новая запись","новые записи","новых записей") + " в борде");
  if (b.closed_today) bits.push(b.closed_today + " " + plural(b.closed_today,"запись закрыта","записи закрыты","записей закрыто") + " сегодня");
  const touched = t.diagnostics_touched || [];
  if (touched.length) bits.push("контроли писались сегодня: " + touched.join(", "));
  if (!bits.length) bits.push("за сутки ничего не менялось");
  return '<p class="ask"><b>Что нового за последние сутки</b>' + esc(bits.join(" · ")) + "</p>";
}

function sectionWhere(){
  const g = D.git || {};
  const ahead = g.ahead;
  const s = el('<section id="a"><h2>Где мы сейчас</h2><div class="card"></div></section>');
  const card = s.querySelector(".card");
  card.innerHTML = verdictBlock("where_we_are") +
    whatsNew() +
    '<div class="kv" style="margin-top:10px">' +
      "<span>HEAD: <b class=\"mono\">" + esc(g.head_short || "—") + "</b></span>" +
      "<span>изменено отслеживаемых: <b>" + (g.dirty_tracked == null ? "—" : g.dirty_tracked) + "</b></span>" +
      "<span>не запушено: <b>" + (ahead == null ? "неизвестно (нет upstream)" : ahead + " " + plural(ahead,"коммит","коммита","коммитов")) + "</b></span>" +
    "</div>" +
    '<div class="sub" style="margin-top:6px">' + esc(g.head_subject || "") + "</div>";
  return s;
}

/* ------------------------------------------------------------------ B */
function ageText(days){
  if (days == null) return "—";
  if (days === 0) return "сегодня";
  return days + " " + plural(days,"день","дня","дней");
}
// A board entry as the owner should read it: Russian if we have it, the English
// envelope under a visible hatch if we do not.
function entryCard(e, extraClass){
  const ru = (D.backlog_ru || {})[e.name];
  const card = el('<div class="card' + (extraClass ? " " + extraClass : "") + '"></div>');
  let body = "";
  if (ru && ru.text){
    body += '<p class="verdict" style="font-size:16px">' + esc(ru.text) + "</p>";
    if (ru.ask) body += '<p class="ask"><b>что от тебя нужно</b>' + esc(ru.ask) + "</p>";
  } else {
    body += hatch("не переведено",
      "Для записи «" + e.name + "» нет русского текста в verdicts.json → backlog_ru. Ниже — фраза из борда как она записана.") +
      '<p class="sub">' + esc(e.sentence) + "</p>";
  }
  body += '<div class="kv" style="margin-top:8px">' +
      '<span><span class="pill ' + priClass(e.priority) + '">' + esc(e.priority) + "</span></span>" +
      "<span>ждёт <b>" + ageText(e.age_days) + "</b></span>" +
      "<span>с <b>" + esc(e.date) + "</b></span>" +
    "</div>" +
    '<div class="src"><b>источник:</b> <span class="mono">' + esc(e.source) + "</span> · <span class=\"mono\">" +
      esc(e.name) + "</span>" + (ru && ru.source && ru.source.length ?
      " · пересказ по <span class=\"mono\">" + ru.source.map(esc).join("</span>, <span class=\"mono\">") + "</span>" : "") + "</div>";
  card.innerHTML = body;
  return card;
}

function sectionAwaiting(){
  const items = D.backlog.open.filter(e => {
    const v = D.verdicts[e.name];
    return e.awaits_mike_text || (v && v.awaits_mike);
  });
  const s = el('<section id="b"><h2>Ждёт слова Mike</h2><div class="grid g2"></div></section>');
  const grid = s.querySelector(".grid");

  if (!items.length){
    grid.appendChild(el('<div class="card">' + hatch("не найдено",
      "В backlog.md нет открытых записей с «Mike's word» / «Mike decides», и ни одна запись не помечена awaits_mike в verdicts.json.") + "</div>"));
  } else {
    items.sort((a,b) => (PRI.indexOf(a.priority) - PRI.indexOf(b.priority)) || ((b.age_days||0) - (a.age_days||0)));
    for (const e of items) grid.appendChild(entryCard(e));
  }

  // repo state: after the decisions, and smaller — it is housekeeping, not a question
  const g = D.git || {};
  const groups = (g.untracked_groups || []).map(x =>
    '<span class="pill">' + esc(x.dir) + " · " + x.n + "</span>").join(" ");
  const repo = el('<div class="card repo" style="margin-top:12px"></div>');
  repo.innerHTML = "<h3>Состояние репозитория</h3>" +
    "<ul>" +
      "<li>изменено отслеживаемых файлов: <b>" + (g.dirty_tracked == null ? "—" : g.dirty_tracked) + "</b>" +
        ((g.tracked_paths || []).length ? ' <span class="sub mono">' + g.tracked_paths.slice(0,4).map(esc).join(", ") + "</span>" : "") + "</li>" +
      "<li>новых (неотслеживаемых) файлов: <b>" + (g.dirty_untracked == null ? "—" : g.dirty_untracked) +
        "</b>" + (groups ? ' <span class="sub">в основном:</span> ' + groups : "") + "</li>" +
      "<li>коммитов не отправлено: <b>" + (g.ahead == null ? "неизвестно" : g.ahead) + "</b>" +
        (g.upstream ? ' <span class="sub mono">(' + esc(g.upstream) + ")</span>" : "") + "</li>" +
    "</ul>" +
    '<div class="src"><b>источник:</b> <span class="mono">git status --porcelain</span> · <span class="mono">git rev-list</span></div>';
  s.appendChild(repo);
  return s;
}
const PRI = ["CRITICAL","BLOCKER","HIGH","MEDIUM","LOW"];
function priClass(p){ return (p === "HIGH" || p === "CRITICAL" || p === "BLOCKER") ? "bad" : (p === "MEDIUM" ? "warn" : ""); }

/* ------------------------------------------------------------------ C */
function sectionNights(){
  const s = el('<section id="c"><h2>Лента ночей</h2><div class="strip"></div></section>');
  const strip = s.querySelector(".strip");
  for (const n of D.nights){
    const box = el('<div class="night"></div>');
    const runs = n.runs.map(id => D.runs.find(r => r.run_id === id)).filter(Boolean);
    const chips = runs.map(r => runChip(r)).join(" ");
    const killed = n.killed.map(k =>
      '<span class="pill bad">убит: ' + esc(k.run_id || "?") + (k.exit ? " (" + esc(k.exit) + ")" : "") + "</span>").join(" ");
    const walls = runs.map(r => fmtDur(r.wall_s)).filter(Boolean);
    const exits = runs.map(r => r.exit).filter(Boolean);
    const allOk = exits.length === runs.length && exits.every(e => e === "ok");
    const vid = "night" + n.n;
    box.innerHTML =
      "<h3>Ночь " + n.n + " <span class=\"sub\">" + fmtDate(n.started_utc) + "</span></h3>" +
      (hasVerdict(vid)
        ? '<p class="verdict" style="font-size:15px">' + esc(D.verdicts[vid].text) + "</p>"
        : hatch("не объяснено", "нет текста для карточки «" + vid + "»")) +
      '<div style="margin:8px 0">' + chips + (killed ? " " + killed : "") + "</div>" +
      '<div class="kv">' +
        "<span>" + (runs.length ? (allOk ? '<span class="pill ok">дошли до конца</span>' :
            '<span class="pill warn">' + esc(exits.join(", ") || "статус не записан") + "</span>") : '<span class="pill">прогонов нет</span>') + "</span>" +
        (walls.length ? "<span>время: <b>" + esc(walls.join(" · ")) + "</b></span>" : "<span>время не записано</span>") +
      "</div>" +
      srcLine((hasVerdict(vid) ? D.verdicts[vid].source : []).concat(
        [n.experiment].concat(n.waves.map(w => w.source)).filter(Boolean)));
    strip.appendChild(box);
  }
  return s;
}
function runChip(r){
  const rep = r.role !== "canonical";
  return '<span class="chip' + (rep ? " rep" : "") + '">' +
    '<span class="dot" style="background:' + seedColor(r.seed) + '"></span>' +
    esc(r.label) + ' <span class="mono">' + esc(r.run_id) + "</span>" +
    (rep ? ' <span class="sub">повтор</span>' : "") +
    "</span>";
}

/* ------------------------------------------------------------------ D */
function sectionFlies(){
  const s = el('<section id="d"><h2>Мухи</h2><div class="card"></div></section>');
  const card = s.querySelector(".card");
  let rows = "";
  for (const seed of seeds){
    const rs = D.runs.filter(r => r.seed === seed).sort((a,b) => a.run_index - b.run_index);
    const canonical = rs.find(r => r.role === "canonical");
    rows += '<div class="runrow">' +
      '<div style="min-width:132px"><b>особь ' + seed + "</b> " +
      '<span class="sub">' + rs.length + " " + plural(rs.length,"прогон","прогона","прогонов") + "</span></div>" +
      "<div>" + rs.map(r =>
        '<span class="chip' + (r.role === "canonical" ? "" : " rep") + '">' +
          '<span class="dot" style="background:' + seedColor(seed) + (r.role === "canonical" ? "" : ";opacity:.6") + '"></span>' +
          "ночь " + r.night + ' <span class="mono">' + esc(r.run_id) + "</span>" +
          (r.role === "canonical" ? "" : ' <span class="sub">повтор' + (canonical ? " от " + esc(canonical.run_id) : "") + "</span>") +
        "</span>").join(" ") + "</div></div>";
  }
  card.innerHTML = verdictBlock("flies") + rows +
    srcLine([D.runs_meta.source]);
  return s;
}

/* ------------------------------------------------------------------ E */
function sectionCurves(){
  const s = el('<section id="e"><h2>Кривые обучения</h2><div class="card" id="curvecard"></div></section>');
  const card = s.querySelector("#curvecard");
  const c = D.curves;
  if (!c.parsed || !c.series.length){
    card.innerHTML = hatch("источник не разобран",
      "Не удалось прочитать " + c.source + " или сопоставить его столбцы с " + (c.mapping_source || "run_columns.csv") + ".") +
      srcLine([c.source]);
    return s;
  }
  card.innerHTML =
    verdictBlock("curves") +
    '<div class="toolbar">' +
      '<span class="sub">ось Y:</span>' +
      '<button id="ylin" aria-pressed="true">линейная</button>' +
      '<button id="ylog" aria-pressed="false">логарифм</button>' +
      '<span class="sub" style="margin-left:6px">итерации:</span>' +
      '<button id="xall" aria-pressed="true">все</button>' +
      '<button id="xcut" aria-pressed="false">с 50 000</button>' +
      '<span class="sub" id="axrange"></span>' +
    "</div>" +
    '<div class="chartbox" id="chartbox"></div>' +
    '<div class="legend" id="legend"></div>' +
    srcLine((D.verdicts.curves ? D.verdicts.curves.source : []).concat([c.source, c.mapping_source]));
  setTimeout(() => drawCurves(), 0);
  return s;
}

// end labels are drawn last and nudged apart, so two curves that finish at the
// same height do not print on top of each other
function drawEndLabels(labels){
  labels.sort((a,b) => a.y - b.y);
  for (let i = 1; i < labels.length; i++)
    if (labels[i].y - labels[i-1].y < 12) labels[i].y = labels[i-1].y + 12;
  return labels.map(l => '<text class="endlabel" x="' + l.x + '" y="' + l.y + '">' +
    esc(l.t) + "</text>").join("");
}

const XCUT = 50000;
const CHART = { logY:false, xcut:false, off:new Set() };

function drawCurves(){
  const c = D.curves, box = document.getElementById("chartbox");
  if (!box) return;
  const W = Math.max(660, Math.min(1060, box.clientWidth || 660)), H = 380;
  const m = {t:16, r:104, b:44, l:62};
  const its = c.iterations;
  const active = c.series.filter(s => !CHART.off.has(s.column));
  const inWindow = i => !CHART.xcut || its[i] >= XCUT;
  const idxs = its.map((v,i) => i).filter(inWindow);
  let xmin = its[idxs[0]], xmax = its[idxs[idxs.length-1]];
  let ymin = Infinity, ymax = -Infinity;
  for (const s of (active.length ? active : c.series))
    for (const i of idxs){
      const v = s.values[i];
      if (v != null && isFinite(v)){ if (v < ymin) ymin = v; if (v > ymax) ymax = v; }
    }
  if (!isFinite(ymin)){ ymin = 0; ymax = 1; }
  const pad = (ymax - ymin) * 0.05 || 1;
  let lo = ymin - pad, hi = ymax + pad;
  const useLog = CHART.logY && lo > 0;
  const X = v => m.l + (v - xmin) / (xmax - xmin || 1) * (W - m.l - m.r);
  const Y = v => {
    if (useLog){
      const a = Math.log10(lo), b = Math.log10(hi);
      return m.t + (b - Math.log10(v)) / (b - a || 1) * (H - m.t - m.b);
    }
    return m.t + (hi - v) / (hi - lo || 1) * (H - m.t - m.b);
  };
  const rng = document.getElementById("axrange");
  const r2 = v => Math.round(v * 100) / 100;
  if (rng) rng.textContent = "видимые значения: " + r2(ymin) + " … " + r2(ymax);

  const parts = [];
  parts.push('<svg viewBox="0 0 ' + W + " " + H + '" width="' + W + '" height="' + H +
    '" role="img" aria-label="Held-out loss по итерациям для десяти прогонов">');
  // grid + y ticks
  const ticks = [];
  for (let i = 0; i <= 4; i++){
    const v = useLog ? Math.pow(10, Math.log10(lo) + (Math.log10(hi)-Math.log10(lo)) * i/4)
                     : lo + (hi - lo) * i / 4;
    ticks.push(v);
  }
  for (const v of ticks){
    const y = Y(v);
    parts.push('<line x1="' + m.l + '" x2="' + (W-m.r) + '" y1="' + y + '" y2="' + y +
      '" stroke="var(--grid)" stroke-width="1"/>');
    parts.push('<text class="axlabel" x="' + (m.l-8) + '" y="' + (y+3.5) + '" text-anchor="end">' +
      (Math.round(v*100)/100) + "</text>");
  }
  // x ticks on the round 50 000 grid, clipped to the window
  for (let v = Math.ceil(xmin / 50000) * 50000; v <= xmax; v += 50000){
    parts.push('<text class="axlabel" x="' + X(v) + '" y="' + (H-m.b+16) + '" text-anchor="middle">' +
      v.toLocaleString("ru-RU") + "</text>");
  }
  parts.push('<line x1="' + m.l + '" x2="' + (W-m.r) + '" y1="' + (H-m.b) + '" y2="' + (H-m.b) +
    '" stroke="var(--line)" stroke-width="1"/>');
  parts.push('<text class="axlabel" x="' + m.l + '" y="' + (H-6) + '">итерация</text>');

  // marked iterations
  const marks = [[150000, "штраф активности снимается"], [25000, "дешёвая проба C3"]];
  for (const [it, label] of marks){
    if (it < xmin || it > xmax) continue;
    const x = X(it);
    parts.push('<line x1="' + x + '" x2="' + x + '" y1="' + m.t + '" y2="' + (H-m.b) +
      '" stroke="var(--ink-3)" stroke-width="1" stroke-dasharray="3 3"/>');
    parts.push('<text class="marklabel" x="' + (x+4) + '" y="' + (m.t+11) + '">' + esc(label) + "</text>");
    parts.push('<text class="marklabel" x="' + (x+4) + '" y="' + (m.t+24) + '">' + it.toLocaleString("ru-RU") + "</text>");
  }

  // series
  // an end label only where a seed has replicates: the curve a reader has to
  // match its dashed twins against. The legend carries every other identity.
  const repSeeds = new Set(c.series.filter(s => s.role !== "canonical").map(s => s.seed));
  const endLabels = [];
  for (const s of c.series){
    if (CHART.off.has(s.column)) continue;
    const rep = s.role !== "canonical";
    let d = "", pen = false;
    for (const i of idxs){
      const v = s.values[i];
      if (v == null || !isFinite(v) || (useLog && v <= 0)){ pen = false; continue; }
      d += (pen ? "L" : "M") + X(its[i]).toFixed(2) + " " + Y(v).toFixed(2) + " ";
      pen = true;
    }
    parts.push('<path d="' + d + '" fill="none" stroke="' + seedColor(s.seed) +
      '" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"' +
      (rep ? ' stroke-dasharray="6 4" opacity="0.72"' : "") + "/>");
    if (!rep && repSeeds.has(s.seed)){
      let last = -1;
      for (let k = idxs.length - 1; k >= 0; k--){
        const v = s.values[idxs[k]];
        if (v != null && isFinite(v)){ last = idxs[k]; break; }
      }
      if (last >= 0) endLabels.push({x: X(its[last])+6, y: Y(s.values[last])+3.5, t: "особь " + s.seed});
    }
  }
  parts.push(drawEndLabels(endLabels));
  parts.push('<line id="cross" x1="0" x2="0" y1="' + m.t + '" y2="' + (H-m.b) +
    '" stroke="var(--ink-3)" stroke-width="1" opacity="0"/>');
  parts.push('<circle id="dot" r="4" fill="none" stroke-width="2" opacity="0"/>');
  parts.push('<rect id="hit" x="' + m.l + '" y="' + m.t + '" width="' + (W-m.l-m.r) + '" height="' + (H-m.t-m.b) +
    '" fill="transparent"/>');
  parts.push("</svg>");
  box.innerHTML = parts.join("");

  // hover
  const svg = box.querySelector("svg"), tip = document.getElementById("tip");
  const cross = box.querySelector("#cross"), dot = box.querySelector("#dot");
  const hit = box.querySelector("#hit");
  function move(ev){
    const r = svg.getBoundingClientRect();
    const px = (ev.clientX - r.left) * (W / r.width);
    const py = (ev.clientY - r.top) * (H / r.height);
    // nearest column first, then the nearest curve in that column: a whole
    // vertical strip is a hit target, so the curves are easy to reach
    let ni = -1, nd = Infinity;
    for (const i of idxs){
      const dx = Math.abs(X(its[i]) - px);
      if (dx < nd){ nd = dx; ni = i; }
    }
    let best = null, bd = Infinity;
    if (ni >= 0){
      for (const s of c.series){
        if (CHART.off.has(s.column)) continue;
        const v = s.values[ni];
        if (v == null || !isFinite(v) || (useLog && v <= 0)) continue;
        const dy = Math.abs(Y(v) - py);
        if (dy < bd){ bd = dy; best = {s, i: ni, v}; }
      }
    }
    if (!best || bd > 60){ hide(); return; }
    const x = X(its[best.i]), y = Y(best.v);
    cross.setAttribute("x1", x); cross.setAttribute("x2", x); cross.setAttribute("opacity", "0.55");
    dot.setAttribute("cx", x); dot.setAttribute("cy", y);
    dot.setAttribute("stroke", seedColor(best.s.seed)); dot.setAttribute("opacity", "1");
    tip.innerHTML = "<b>" + esc(best.s.label) + "</b><br>" +
      '<span class="mono">' + esc(best.s.run_id) + " · " + esc(best.s.column) + "</span><br>" +
      "итерация " + its[best.i].toLocaleString("ru-RU") + "<br>val_loss " + best.v;
    tip.style.opacity = "1";
    const tw = tip.offsetWidth, th = tip.offsetHeight;
    tip.style.left = Math.min(window.innerWidth - tw - 8, ev.clientX + 14) + "px";
    tip.style.top = Math.max(8, ev.clientY - th - 12) + "px";
  }
  function hide(){
    tip.style.opacity = "0";
    cross.setAttribute("opacity", "0");
    dot.setAttribute("opacity", "0");
  }
  hit.addEventListener("mousemove", move);
  hit.addEventListener("mouseleave", hide);

  // legend
  const legend = document.getElementById("legend");
  if (legend && !legend.dataset.built){
    legend.dataset.built = "1";
    for (const s of c.series){
      const rep = s.role !== "canonical";
      const b = el('<button type="button" aria-pressed="true">' +
        '<svg width="18" height="8" aria-hidden="true"><line x1="0" y1="4" x2="18" y2="4" stroke="' +
        seedColor(s.seed) + '" stroke-width="2"' + (rep ? ' stroke-dasharray="5 3" opacity="0.72"' : "") + "/></svg>" +
        "<span>" + esc(s.label) + (rep ? " · повтор" : "") + "</span></button>");
      b.addEventListener("click", () => {
        if (CHART.off.has(s.column)){ CHART.off.delete(s.column); b.setAttribute("aria-pressed","true"); }
        else { CHART.off.add(s.column); b.setAttribute("aria-pressed","false"); }
        drawCurves();
      });
      legend.appendChild(b);
    }
  }
  const lin = document.getElementById("ylin"), lg = document.getElementById("ylog");
  const xa = document.getElementById("xall"), xc = document.getElementById("xcut");
  if (lin && !lin.dataset.wired){
    lin.dataset.wired = "1";
    const set = (logY) => { CHART.logY = logY;
      lin.setAttribute("aria-pressed", String(!logY)); lg.setAttribute("aria-pressed", String(logY)); drawCurves(); };
    lin.addEventListener("click", () => set(false));
    lg.addEventListener("click", () => set(true));
    const setx = (cut) => { CHART.xcut = cut;
      xa.setAttribute("aria-pressed", String(!cut)); xc.setAttribute("aria-pressed", String(cut)); drawCurves(); };
    xa.addEventListener("click", () => setx(false));
    xc.addEventListener("click", () => setx(true));
  }
}

function sectionPenalised(){
  const p = D.penalised || {};
  const s = el('<section><div class="card"></div></section>');
  const card = s.querySelector(".card");
  const head = "<h3>Штрафуемая величина по чекпойнтам</h3>";
  if (!p.parsed || !(p.series || []).length){
    card.innerHTML = head +
      (p.present
        ? hatch("источник не разобран",
            "Файл " + (p.csv || "") + " есть, но нужных столбцов (run_id / chkpt_iter / pre_weight) в нём не нашлось.")
        : hatch("ещё не прочитано",
            "Файла " + (p.csv || "") + " на диске нет" +
            (p.reading_present ? ", хотя чтение " + p.md + " уже написано" : "; чтение " + (p.md || "") + " тоже не написано") +
            ". Свободный фальсификатор (README ряда B, §8) ещё не выполнен.")) +
      srcLine([p.csv, p.md]);
    return s;
  }
  card.innerHTML = head +
    (hasVerdict("penalised") ? verdictBlock("penalised")
      : hatch("не объяснено", "нет текста для карточки «penalised» в verdicts.json")) +
    '<div class="sub">по оси Y — <span class="mono">' + esc(p.y_column) + "</span>, по оси X — <span class=\"mono\">" +
      esc(p.x_column) + '</span>; ' + p.series.length + " прогонов, " + p.n_rows + " точек, как записано</div>" +
    '<div class="toolbar">' +
      '<span class="sub">ось Y:</span>' +
      '<button id="pylin" aria-pressed="false">линейная</button>' +
      '<button id="pylog" aria-pressed="true">логарифм</button>' +
      '<span class="sub" style="margin-left:6px">итерации:</span>' +
      '<button id="pxall" aria-pressed="true">все</button>' +
      '<button id="pxcut" aria-pressed="false">с 50 000</button>' +
    "</div>" +
    '<div class="chartbox" id="penbox"></div>' +
    srcLine([p.csv, p.reading_present ? p.md : null]);
  setTimeout(() => {
    drawPenalised();
    const lin = document.getElementById("pylin"), lg = document.getElementById("pylog");
    const xa = document.getElementById("pxall"), xc = document.getElementById("pxcut");
    if (!lin || lin.dataset.wired) return;
    lin.dataset.wired = "1";
    const sety = v => { PEN.logY = v;
      lin.setAttribute("aria-pressed", String(!v)); lg.setAttribute("aria-pressed", String(v)); drawPenalised(); };
    lin.addEventListener("click", () => sety(false));
    lg.addEventListener("click", () => sety(true));
    const setx = v => { PEN.xcut = v;
      xa.setAttribute("aria-pressed", String(!v)); xc.setAttribute("aria-pressed", String(v)); drawPenalised(); };
    xa.addEventListener("click", () => setx(false));
    xc.addEventListener("click", () => setx(true));
  }, 0);
  return s;
}

// one early checkpoint of one run reaches into the millions, so this chart is
// logarithmic by default; the linear view is one click away
const PEN = { logY:true, xcut:false };

function drawPenalised(){
  const p = D.penalised || {};
  const box = document.getElementById("penbox");
  if (!box || !p.parsed) return;
  const W = 700, H = 240, m = {t:14, r:78, b:34, l:66};
  const keep = pt => !PEN.xcut || pt[0] >= XCUT;
  let xmin = Infinity, xmax = -Infinity, ymin = Infinity, ymax = -Infinity;
  for (const se of p.series) for (const pt of se.points){
    if (!keep(pt)) continue;
    if (pt[0] < xmin) xmin = pt[0]; if (pt[0] > xmax) xmax = pt[0];
    if (pt[1] < ymin) ymin = pt[1]; if (pt[1] > ymax) ymax = pt[1];
  }
  if (!isFinite(xmin)){ box.innerHTML = ""; return; }
  const useLog = PEN.logY && ymin > 0;
  const X = v => m.l + (v - xmin) / (xmax - xmin || 1) * (W - m.l - m.r);
  const Y = v => {
    if (useLog){
      const a = Math.log10(ymin), b = Math.log10(ymax);
      return m.t + (b - Math.log10(v)) / (b - a || 1) * (H - m.t - m.b);
    }
    return m.t + (ymax - v) / (ymax - ymin || 1) * (H - m.t - m.b);
  };
  const parts = ['<svg viewBox="0 0 ' + W + " " + H + '" width="' + W + '" height="' + H +
    '" role="img" aria-label="Штрафуемая величина pre_weight по чекпойнтам, десять прогонов">'];
  parts.push('<line x1="' + m.l + '" x2="' + (W-m.r) + '" y1="' + (H-m.b) + '" y2="' + (H-m.b) +
    '" stroke="var(--line)" stroke-width="1"/>');
  for (let i = 0; i <= 3; i++){
    const v = useLog
      ? Math.pow(10, Math.log10(ymin) + (Math.log10(ymax)-Math.log10(ymin)) * i/3)
      : ymin + (ymax - ymin) * i / 3;
    const y = Y(v);
    parts.push('<line x1="' + m.l + '" x2="' + (W-m.r) + '" y1="' + y + '" y2="' + y +
      '" stroke="var(--grid)" stroke-width="1"/>');
    parts.push('<text class="axlabel" x="' + (m.l-8) + '" y="' + (y+3.5) + '" text-anchor="end">' +
      (v >= 1000 ? Math.round(v).toLocaleString("ru-RU") : Math.round(v*100)/100) + "</text>");
  }
  for (let v = Math.max(0, Math.ceil(xmin / 50000) * 50000); v <= xmax; v += 50000){
    parts.push('<text class="axlabel" x="' + X(v) + '" y="' + (H-m.b+15) + '" text-anchor="middle">' +
      v.toLocaleString("ru-RU") + "</text>");
  }
  if (150000 >= xmin && 150000 <= xmax){
    const x = X(150000);
    parts.push('<line x1="' + x + '" x2="' + x + '" y1="' + m.t + '" y2="' + (H-m.b) +
      '" stroke="var(--ink-3)" stroke-width="1" stroke-dasharray="3 3"/>');
    parts.push('<text class="marklabel" x="' + (x+4) + '" y="' + (m.t+11) + '">штраф активности снимается</text>');
    parts.push('<text class="marklabel" x="' + (x+4) + '" y="' + (m.t+24) + '">150 000</text>');
  }
  const repSeeds = new Set(p.series.filter(x => x.role !== "canonical").map(x => x.seed));
  const endLabels = [];
  for (const se of p.series){
    const rep = se.role !== "canonical";
    let d = "", pen = false;
    for (const pt of se.points){
      if (!keep(pt) || (useLog && pt[1] <= 0)){ pen = false; continue; }
      d += (pen ? "L" : "M") + X(pt[0]).toFixed(2) + " " + Y(pt[1]).toFixed(2) + " ";
      pen = true;
    }
    parts.push('<path d="' + d + '" fill="none" stroke="' + seedColor(se.seed) +
      '" stroke-width="1.7" stroke-linejoin="round"' + (rep ? ' stroke-dasharray="6 4" opacity="0.72"' : "") + "/>");
    const pts = se.points.filter(keep);
    const last = pts[pts.length - 1];
    if (last && !rep && repSeeds.has(se.seed))
      endLabels.push({x: X(last[0])+5, y: Y(last[1])+3.5, t: "особь " + se.seed});
  }
  parts.push(drawEndLabels(endLabels));
  parts.push("</svg>");
  box.innerHTML = parts.join("");
}

/* ------------------------------------------------------------------ F */
function sectionInstruments(){
  const s = el('<section id="f"><h2>Приборы и контроли</h2><div class="grid g2"></div></section>');
  const grid = s.querySelector(".grid");
  for (const t of D.diagnostics){
    const card = el('<div class="card"></div>');
    const vid = "diag:" + t.id;
    let body = "<h3>" + esc(t.title) + "</h3>";
    if (t.instrument) body += '<p class="instr">' + esc(t.instrument) + "</p>";
    body += '<div class="kv"><span>' +
      (t.ran ? '<span class="pill ok">запускался</span>' : '<span class="pill">не запускался</span>') +
      "</span>";
    if (t.ran && (t.passed || t.failed)){
      body += '<span><span class="pill ok">прошло ' + t.passed + "</span></span>";
      body += '<span><span class="pill ' + (t.failed ? "bad" : "") + '">не прошло ' + t.failed + "</span></span>";
    }
    body += "</div>";
    // the hatched debt and the README quote sit under the verdict, not above it
    let pending = "";
    if (t.ran && !t.passed && !t.failed){
      pending += hatch("не измерено",
        "Контроли этого прибора записаны не булевыми полями `pass`, а разностями, поэтому счёт «прошло / не прошло» отсюда не читается. Файлы: " +
        (t.controls || []).filter(c => c.present).map(c => c.file).join(", "));
      if (t.quote) pending += '<div class="quote"><b>из README <span class="path mono">' +
        esc(t.quote.path) + "</span></b>" + esc(t.quote.text) + "</div>";
    }
    if (t.status_line) body += '<p class="sub mono">' + esc(t.status_line) + "</p>";
    if (t.recorded_verdict) body += '<p class="sub">записанный вердикт: <b>' + esc(t.recorded_verdict) + "</b></p>";
    body += hasVerdict(vid) ? verdictText(vid)
      : hatch("не объяснено", "нет текста для карточки «" + vid + "» в verdicts.json");
    body += pending;
    const fields = [];
    for (const c of (t.controls || [])){
      if (!c.present){ fields.push('<span class="pill">нет файла: ' + esc(c.file) + "</span>"); continue; }
      if (c.parsed === false){ fields.push('<span class="pill bad">не разобран: ' + esc(c.file) + "</span>"); continue; }
      const names = Object.keys(c.by_field || {});
      const detail = names.map(n => esc(n) + " " + c.by_field[n].true + "/" +
        (c.by_field[n].true + c.by_field[n].false)).join(", ");
      fields.push('<span class="pill wrap">' + esc(c.file) + (c.n_entries ? " · " + c.n_entries + " пар" : "") +
        (detail ? " · " + detail : "") + "</span>");
    }
    if (fields.length) body += '<div class="kv" style="margin-top:8px">' + fields.join(" ") + "</div>";
    if (t.readme) body += '<div class="src"><a href="' + esc(t.readme) + '">' + esc(t.readme) + "</a></div>";
    body += srcLine(verdictSources(vid)
      .concat(t.sources || [])
      .concat(t.quote ? [t.quote.path] : []));
    card.innerHTML = body;
    grid.appendChild(card);
  }
  return s;
}

/* ------------------------------------------------------------------ G */
function sectionBoard(){
  const s = el('<section id="g"><h2>Борд</h2><div class="grid g2"></div></section>');
  const grid = s.querySelector(".grid");
  const b = D.backlog;

  const counts = el('<div class="card"></div>');
  const pri = PRI.filter(p => b.by_priority[p]).map(p =>
    '<span class="pill ' + priClass(p) + '">' + p + " · " + b.by_priority[p] + "</span>").join(" ");
  const st = Object.keys(b.by_status).sort().map(k =>
    '<span class="pill">' + esc(k) + " · " + b.by_status[k] + "</span>").join(" ");
  counts.innerHTML = "<h3>Счёт</h3>" +
    (hasVerdict("board") ? verdictBlock("board") : "") +
    '<div class="kv"><span>открыто: <b>' + b.open_count + "</b></span><span>закрыто: <b>" + b.closed_count + "</b></span></div>" +
    '<div class="kv" style="margin-top:8px">' + pri + "</div>" +
    '<div class="kv" style="margin-top:6px">' + st + "</div>" +
    (b.unparsed_headers ? hatch("источник не разобран",
        b.unparsed_headers + " заголовков не подошли под конверт «### ИМЯ: фраза (ПРИОРИТЕТ, статус, дата — происхождение)» и не сосчитаны.") : "") +
    (b.view_present ? '<div class="src"><a href="' + esc(b.view) + '">' + esc(b.view) + "</a></div>" : "") +
    srcLine(b.sources);
  grid.appendChild(counts);

  const high = b.open.filter(e => e.priority === "HIGH" || e.priority === "CRITICAL" || e.priority === "BLOCKER");
  const hiCard = el('<div class="card"></div>');
  hiCard.innerHTML = "<h3>HIGH, открытые (" + high.length + ")</h3><ul>" +
    high.map(e => {
      const ru = (D.backlog_ru || {})[e.name];
      const text = (ru && ru.text) ? esc(ru.text)
        : '<span class="pill warn">не переведено</span> ' + esc(firstSentence(e.sentence));
      const ask = (ru && ru.ask) ? '<br><span class="sub"><b>нужно:</b> ' + esc(ru.ask) + "</span>" : "";
      return "<li>" + text + ' <span class="sub">(' + esc(e.date) + ", " + ageText(e.age_days) + ")</span>" + ask + "</li>";
    }).join("") +
    "</ul>" + srcLine(["backlog.md", "tools/atlas/verdicts.json"]);
  grid.appendChild(hiCard);

  const adr = el('<div class="card"></div>');
  adr.innerHTML = "<h3>Решения (ADR)</h3><table><tbody>" +
    D.decisions.map(d => "<tr><td class=\"mono\">ADR-" + esc(d.adr) + "</td><td>" + esc(d.title) +
      '</td><td><span class="pill ' + (d.status === "accepted" ? "ok" : "") + '">' + esc(d.status) + "</span></td>" +
      "<td>" + esc(d.date || "") + "</td></tr>").join("") +
    "</tbody></table>" + srcLine(D.decisions.map(d => d.path));
  grid.appendChild(adr);
  return s;
}
function firstSentence(text){
  const m = String(text || "").split(/(?<=[.!?])\s/);
  return (m[0] || text || "").trim();
}

/* ------------------------------------------------------------------ H */
function sectionCommits(){
  const s = el('<section id="h"><h2>Последние события</h2><div class="card"></div></section>');
  const card = s.querySelector(".card");
  const cs = (D.git && D.git.commits) || [];
  if (!cs.length){
    card.innerHTML = hatch("источник не разобран", "git log не дал ответа.");
    return s;
  }
  card.innerHTML = "<table><tbody>" + cs.map(c =>
    '<tr><td class="mono" style="white-space:nowrap">' + esc(c.sha) + "</td>" +
    '<td class="sub" style="white-space:nowrap">' + fmtDateTime(c.date) + "</td>" +
    "<td>" + esc(c.subject) + "</td></tr>").join("") + "</tbody></table>" +
    '<div class="src"><b>источник:</b> <span class="mono">git log -15</span></div>';
  return s;
}

/* ------------------------------------------------------------------ foot */
function sectionFoot(){
  const u = (D.sources && D.sources.unparsed) || [];
  const f = el('<div class="foot"></div>');
  f.innerHTML =
    "<p>Страница собрана скриптом <span class=\"mono\">tools/atlas/build.py</span> из того, что лежит в репозитории в машиночитаемом виде. " +
    "Числа показаны так, как они записаны: ничего не пересчитано. Тексты вердиктов — из <span class=\"mono\">tools/atlas/verdicts.json</span>.</p>" +
    "<p>Прочитано источников: <b>" + ((D.sources && D.sources.found) || []).length + "</b>; не найдено: <b>" +
    ((D.sources && D.sources.missing) || []).length + "</b>; не разобрано: <b>" + u.length + "</b>.</p>" +
    (u.length ? '<div class="hatch"><b>источник не разобран</b>' +
      u.map(x => esc(x.path) + " — " + esc(x.reason)).join("<br>") + "</div>" : "") +
    "<p><b>Эта страница — вид, а не запись.</b> Она никогда не коммитится (" +
    "<span class=\"mono\">atlas.html</span> в <span class=\"mono\">.gitignore</span>) и закрыта для слепого автора v2 (ADR-003).</p>";
  return f;
}

for (const make of [sectionHeader, sectionWhere, sectionAwaiting, sectionNights, sectionFlies,
                    sectionCurves, sectionPenalised, sectionInstruments,
                    sectionBoard, sectionCommits, sectionFoot]){
  try { app.appendChild(make()); }
  catch (err) {
    app.appendChild(el('<div class="card"><div class="hatch"><b>источник не разобран</b>' +
      "Секция не построена: " + esc(err && err.message) + "</div></div>"));
  }
}
let rt;
window.addEventListener("resize", () => {
  clearTimeout(rt);
  rt = setTimeout(() => { drawCurves(); drawPenalised(); }, 180);
});
</script>
</body>
</html>
"""


def render(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # never let the data close the script element
    payload = payload.replace("</", "<\\/")
    return PAGE.replace("__DATA__", payload)


# --------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Собрать atlas.html из артефактов репозитория.")
    ap.add_argument("--out", default=str(REPO / "atlas.html"), help="куда писать (по умолчанию atlas.html в корне)")
    ap.add_argument("--check", action="store_true", help="только отчёт о найденных/пропавших источниках")
    args = ap.parse_args(argv)

    # a Windows console is cp1252/cp866 by default and would abort on Cyrillic
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    data = build_data()

    if args.check:
        print(f"atlas --check · репозиторий {REPO}")
        print(f"  найдено источников : {len(SRC.found)}")
        for p in SRC.found:
            print(f"    + {p}")
        print(f"  не найдено         : {len(SRC.missing)}")
        for p in SRC.missing:
            print(f"    - {p}")
        print(f"  не разобрано       : {len(SRC.unparsed)}")
        for item in SRC.unparsed:
            print(f"    ? {item['path']}: {item['reason']}")
        cards = ["where_we_are", "flies", "curves", "penalised", "board"]
        cards += [f"night{n['n']}" for n in data["nights"]]
        cards += [f"diag:{t['id']}" for t in data["diagnostics"]]
        missing_v = [c for c in cards if c not in data["verdicts"] or not data["verdicts"][c].get("text")]
        print(f"  карточек без вердикта: {len(missing_v)} из {len(cards)}")
        for c in missing_v:
            print(f"    ~ {c}")
        return 0

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    page = render(data)
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page)

    n_series = len(data["curves"].get("series", []))
    cards_total = 5 + len(data["nights"]) + len(data["diagnostics"])
    have = sum(
        1 for c in (["where_we_are", "flies", "curves", "penalised", "board"]
                    + [f"night{n['n']}" for n in data["nights"]]
                    + [f"diag:{t['id']}" for t in data["diagnostics"]])
        if c in data["verdicts"] and data["verdicts"][c].get("text")
    )
    print(
        f"atlas: {out.name} {out.stat().st_size // 1024} КБ · "
        f"{len(data['runs'])} прогонов / {data['runs_meta'].get('n_individuals', 0)} особей · "
        f"{n_series} кривых · {len(data['diagnostics'])} приборов · "
        f"{data['backlog']['open_count']} открытых записей · "
        f"вердиктов {have}/{cards_total} · "
        f"источников {len(SRC.found)} найдено, {len(SRC.missing)} нет, {len(SRC.unparsed)} не разобрано"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
