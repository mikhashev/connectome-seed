"""Launch a wave of run_individual.py processes and wait for them.

Seed/id mapping: seed s -> id <ENSEMBLE>/<s:03d>, tag <tag>.
--replicate-of S (repeatable) adds run S': --seed S --id <ENSEMBLE>/9<S:02d> --tag rep, placed right
  after seed S's own job if S is in --seeds else first; --replicate is --replicate-of 0.
Default: all runs start concurrently, staggered by --stagger seconds.
--sequential: each run waits for the previous one to exit (stagger unused).
--detach: the launcher re-spawns itself as a detached Windows process
  (DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP, stdin/stdout/stderr on files under
  <out-dir>, close_fds) so the runs survive the launching shell; it writes
  <out-dir>/wave_<tag>.pid with the detached launcher PID and prints it. The
  detached launcher writes <out-dir>/wave_<tag>.progress.log (one timestamped line
  per run start / exit) and its own stdout/stderr to <out-dir>/wave_<tag>.launcher.log.
--replicate-tag TAG renames those replicate jobs' tag (default "rep", as every wave up to
  night 5 used); the id keeps its 9xx marking either way.
--no-determinism is passed through to every run_individual.py; omitting it leaves
  run_individual.py's own default, which is determinism ON.
--stop-after-iter K is passed through to every run_individual.py when given (default: not
  passed at all, so --n-iters alone sets the horizon, as for nights 1-5).
--progress-every N is passed through to every run_individual.py; --progress-file too
  when given. With --sequential and no --progress-file every run's progress file is
  the wave's own <out-dir>/wave_<tag>.progress.log, so one file carries the START/EXIT
  lines and the iter/RUNG/CHECKPOINT/DONE lines of the job currently running
  (follow it with: Get-Content -Path <file> -Wait -Tail 20).
PIDs, commands, launch times and exit codes go to <out-dir>/wave_<tag>.json,
rewritten after every launch and every exit so a crash leaves the record.
Each child logs itself to <out-dir>/<tag>_<id>.log; its stdout/stderr go to
<out-dir>/<tag>_<id>.stdout.log (import-time crashes land there).
--dry prints the exact command lines and exits without starting anything.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_PY = str(HERE.parent / ".venv" / "Scripts" / "python.exe")
DETACHED_MARK = "--_detached-child"  # internal: set on the re-spawned launcher


def now_utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def parse_seeds(s: str):
    out = []
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, hi = part.split("-")
            out.extend(range(int(lo), int(hi) + 1))
        else:
            out.append(int(part))
    return out


def build_parser():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--tag", required=True)
    p.add_argument("--ensemble", default="9990")
    p.add_argument("--seeds", default="0-7", help="comma list and/or ranges, e.g. 0-7 or 1,2")
    p.add_argument("--replicate", action="store_true", help="add run 0': seed 0, id <ENS>/900, tag rep")
    p.add_argument("--replicate-of", type=int, action="append", default=[],
                   help="add run S': seed S, id <ENS>/9<S:02d>, tag rep; repeatable; --replicate is --replicate-of 0")
    p.add_argument("--replicate-tag", default="rep",
                   help="tag for the --replicate/--replicate-of jobs (default 'rep', the value every "
                        "wave up to night 5 used). Night 6 sets it to the wave tag so one prefix carries "
                        "the whole wave while the id keeps its 9xx replicate marking.")
    p.add_argument("--n-iters", type=int, default=250_000)
    p.add_argument("--rungs", default="1000,5000,25000,250000")
    p.add_argument("--stagger", type=float, default=5.0)
    p.add_argument("--sequential", action="store_true", help="run one after another")
    p.add_argument("--detach", action="store_true", help="re-spawn as a detached Windows process and return")
    p.add_argument("--no-determinism", action="store_true", help="pass --no-determinism to run_individual.py")
    p.add_argument("--stop-after-iter", type=int, default=None,
                   help="passed through to run_individual.py --stop-after-iter (must be one of --rungs and "
                        "< --n-iters there); default None: not passed, so --n-iters decides the horizon")
    p.add_argument("--progress-every", type=int, default=100, help="passed to run_individual.py --progress-every")
    p.add_argument("--progress-file", default=None,
                   help="passed to run_individual.py --progress-file for every run; default: the wave's "
                        "progress log when --sequential, else each run's own <tag>_<id>.progress.log")
    p.add_argument("--override", action="append", default=[],
                   help="extra Hydra override KEY=VAL, repeatable; passed as --override to every run_individual.py")
    p.add_argument("--python", default=DEFAULT_PY)
    p.add_argument("--out-dir", default=str(HERE))
    p.add_argument("--dry", action="store_true")
    p.add_argument(DETACHED_MARK, dest="detached_child", action="store_true", help=argparse.SUPPRESS)
    return p


def main():
    a = build_parser().parse_args()
    out_dir = Path(a.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    script = str(HERE / "run_individual.py")
    wave_path = out_dir / f"wave_{a.tag}.json"
    progress_path = out_dir / f"wave_{a.tag}.progress.log"
    pid_path = out_dir / f"wave_{a.tag}.pid"

    jobs = []
    for s in parse_seeds(a.seeds):
        jobs.append({"seed": s, "id": f"{a.ensemble}/{s:03d}", "tag": a.tag})
    seeds_in_wave = {j["seed"] for j in jobs}

    # job order: a replicate-of job (seed S, id <ENS>/9<S:02d>, tag rep) runs right AFTER seed S's own
    # job when S is in --seeds (so the pair that decides determinism finishes first), else it is placed
    # first (before any seed job); among several front-placed replicates, earlier --replicate-of wins.
    rep_seeds = ([0] if a.replicate else []) + list(a.replicate_of)
    seen_ids = {j["id"] for j in jobs}
    front_pos = 0
    for s in rep_seeds:
        if s >= 100:
            print(f"--replicate-of {s}: seed must be < 100", file=sys.stderr)
            return 2
        rep = {"seed": s, "id": f"{a.ensemble}/9{s:02d}", "tag": a.replicate_tag}
        if rep["id"] in seen_ids:
            print(f"--replicate-of {s}: id {rep['id']} already queued", file=sys.stderr)
            return 2
        seen_ids.add(rep["id"])
        if s in seeds_in_wave:
            pos = next(i + 1 for i, j in enumerate(jobs) if j["seed"] == s and j["tag"] == a.tag)
            jobs.insert(pos, rep)
        else:
            jobs.insert(front_pos, rep)
            front_pos += 1
    for j in jobs:
        j["cmd"] = [a.python, script, "--seed", str(j["seed"]), "--id", j["id"],
                    "--n-iters", str(a.n_iters), "--rungs", a.rungs, "--tag", j["tag"],
                    "--out-dir", str(out_dir)]
        if a.no_determinism:
            j["cmd"].append("--no-determinism")
        if a.stop_after_iter is not None:
            j["cmd"] += ["--stop-after-iter", str(a.stop_after_iter)]
        j["cmd"] += ["--progress-every", str(a.progress_every)]
        run_progress_file = a.progress_file or (str(progress_path) if a.sequential else None)
        if run_progress_file:
            j["cmd"] += ["--progress-file", run_progress_file]
        for o in a.override:
            j["cmd"] += ["--override", o]
        j["json"] = str(out_dir / f"{j['tag']}_{j['id'].replace('/', '-')}.json")
        j["stdout_log"] = str(out_dir / f"{j['tag']}_{j['id'].replace('/', '-')}.stdout.log")

    if a.dry:
        for j in jobs:
            print(subprocess.list2cmdline(j["cmd"]))
        print(f"[dry] {len(jobs)} commands; mode={'sequential' if a.sequential else 'concurrent'}; "
              f"detach={a.detach}; nothing started; wave json not written")
        return 0

    # ---------------- detach: re-spawn self and return ----------------
    if a.detach and not a.detached_child:
        argv = [sys.executable, str(Path(__file__).resolve())] + [x for x in sys.argv[1:] if x != "--detach"] + [DETACHED_MARK]
        flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
        launcher_log = out_dir / f"wave_{a.tag}.launcher.log"
        with open(launcher_log, "a", encoding="utf-8") as lf, open(os.devnull, "rb") as devnull:
            pr = subprocess.Popen(argv, stdin=devnull, stdout=lf, stderr=subprocess.STDOUT,
                                  creationflags=flags, close_fds=True, cwd=str(HERE))
        pid_path.write_text(str(pr.pid))
        print(f"DETACHED launcher pid={pr.pid} pidfile={pid_path} progress={progress_path} launcher_log={launcher_log}")
        print("detached cmd: " + subprocess.list2cmdline(argv))
        return 0

    def progress(line):
        msg = f"{now_utc()} {line}"
        with open(progress_path, "a", encoding="utf-8") as pf:
            pf.write(msg + "\n")
        print(msg, flush=True)

    wave = {"tag": a.tag, "ensemble": a.ensemble, "stagger_s": a.stagger, "dry": a.dry,
            "sequential": a.sequential, "detached": a.detached_child, "no_determinism": a.no_determinism,
            "launcher_pid": os.getpid(), "started_utc": now_utc(),
            "env": {"FLYVIS_ROOT_DIR": os.environ.get("FLYVIS_ROOT_DIR"),
                    "CUBLAS_WORKSPACE_CONFIG": os.environ.get("CUBLAS_WORKSPACE_CONFIG")},
            "jobs": jobs}

    def dump():
        tmp = wave_path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(wave, indent=1))
        os.replace(tmp, wave_path)

    def launch(j):
        f = open(j["stdout_log"], "w", encoding="utf-8")
        pr = subprocess.Popen(j["cmd"], stdin=subprocess.DEVNULL, stdout=f, stderr=subprocess.STDOUT, cwd=str(HERE))
        j["pid"] = pr.pid
        j["launched_utc"] = now_utc()
        j["launched_perf"] = time.perf_counter()
        progress(f"START pid={pr.pid} id={j['id']} seed={j['seed']} tag={j['tag']} cmd={subprocess.list2cmdline(j['cmd'])}")
        dump()
        return pr, f

    def finish(j, pr, f):
        f.close()
        j["exit_code"] = pr.returncode
        j["exited_utc"] = now_utc()
        j["wall_s"] = time.perf_counter() - j["launched_perf"]
        j["json_exists"] = Path(j["json"]).exists()
        if j["json_exists"]:
            try:
                d = json.loads(Path(j["json"]).read_text())
                j["json_exit"] = d.get("exit")
                j["json_final_iteration"] = d.get("final_iteration")
                j["json_n_rungs"] = len(d.get("rung_metrics", []))
                j["json_iter_wall_median_all_s"] = d.get("iter_wall_median_all_s")
            except Exception as e:  # noqa: BLE001
                j["json_read_error"] = repr(e)
        progress(f"EXIT pid={pr.pid} id={j['id']} rc={pr.returncode} wall={j['wall_s']:.1f}s "
                 f"json_exit={j.get('json_exit')} final_iteration={j.get('json_final_iteration')} "
                 f"median_iter_s={j.get('json_iter_wall_median_all_s')}")
        dump()

    progress(f"WAVE START tag={a.tag} launcher_pid={os.getpid()} mode={'sequential' if a.sequential else 'concurrent'} "
             f"detached={a.detached_child} no_determinism={a.no_determinism} n_jobs={len(jobs)}")
    dump()

    if a.sequential:
        for j in jobs:
            pr, f = launch(j)
            pr.wait()
            finish(j, pr, f)
    else:
        procs = []
        for i, j in enumerate(jobs):
            if i:
                time.sleep(a.stagger)
            procs.append((j,) + launch(j))
        pending = list(procs)
        while pending:
            time.sleep(2)
            still = []
            for j, pr, f in pending:
                if pr.poll() is None:
                    still.append((j, pr, f))
                else:
                    finish(j, pr, f)
            pending = still

    wave["finished_utc"] = now_utc()
    dump()
    bad = [j for j in jobs if j.get("exit_code") != 0]
    progress(f"WAVE DONE {len(jobs) - len(bad)}/{len(jobs)} ok; record {wave_path}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
