#!/usr/bin/env python
"""Derive night-3 committed artefacts the same way night 1/night 2's were derived.

Reproduces, for night 3 (seeds 3 and 4 of ensemble 9991), the same derivative
files that live in results/night1/ and results/night2/:

  - <tag>_<id-dash>.slim.json   -- the run_individual.py json with the two
    large per-iteration arrays (iter_wall_s, train_loss_per_iter) removed.
    Verified byte-for-byte equal to the raw json on every other top-level
    key, AND asserted to carry the same key set as the night-2 slim jsons
    (task requirement: "same field set as night-2 slim jsons -- assert
    equality of key sets").
  - iter_wall_s_<id-dash>.csv.gz  -- the full per-iteration wall-time array,
    one float per line, gzip-compressed (no header).
  - train_loss_last1000_<id-dash>.csv -- the last 1000 entries of
    train_loss_per_iter, one float per line (no header).

Also builds a SIX-run (seed 0, 0', 1, 2, 3, 4) checkpoint table -- extending
night 2's four-way table with the two new night-3 runs -- and the between-
seed SD at n=5 (seeds 0,1,2,3,4) beside n=3, with 95% chi-squared confidence
intervals for sigma at n=5 (4 degrees of freedom).

Hardening item 9 (tool-hardening-package.md): this script's own sha256 is
printed by README.md's provenance section, computed with
`git hash-object`/`sha256sum` against the checked-in copy, not recomputed
inline here (a hash of a running script cannot include its own output).

Hardening item 19: the six-run checkpoint CSV built here is FULL FLOAT from
the run jsons themselves, not tools/night/night_report.py's `r4()` 4-decimal
formatter -- stated explicitly in the CSV's own header comment line, per the
provenance rule (a quantity claimed at 1e-4 precision must name the
formatter that produced it).

Usage:
    python extract_night3.py
"""
import gzip
import json
import math
import os
import statistics

NIGHT_RAW = (
    r"C:\Users\mikha\AppData\Local\Temp\claude"
    r"\c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx"
    r"\63f3961a-96ce-4048-8338-72c162ea66f8\scratchpad\flyvis-probe\night"
)
REPO = r"C:\Users\mikha\Documents\dpc-research\connectome-seed"
NIGHT1_DIR = os.path.join(REPO, "results", "night1")
NIGHT2_DIR = os.path.join(REPO, "results", "night2")
OUT_DIR = os.path.join(REPO, "results", "night3")

DROP_KEYS = ("iter_wall_s", "train_loss_per_iter")

# 95% chi-squared quantiles at 4 degrees of freedom (n=5), as given in the
# task brief: chi2_0.975,4 = 11.143 (upper tail cutoff), chi2_0.025,4 =
# 0.4844 (lower tail cutoff). CI for sigma: sigma*sqrt(df/chi2_upper) ..
# sigma*sqrt(df/chi2_lower).
CHI2_UPPER_4DF = 11.143
CHI2_LOWER_4DF = 0.4844
DF = 4


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def make_slim(raw_path, slim_path, reference_keys=None):
    d = load(raw_path)
    slim = {k: v for k, v in d.items() if k not in DROP_KEYS}
    # verify: slim has exactly the raw keys minus DROP_KEYS, no value drift
    # on anything kept.
    assert set(d.keys()) - set(slim.keys()) == set(DROP_KEYS) & set(d.keys())
    for k in slim:
        assert slim[k] == d[k]
    if reference_keys is not None:
        assert set(slim.keys()) == reference_keys, (
            f"{slim_path}: key set differs from night-2 slim json reference\n"
            f"  only in night3 slim: {set(slim.keys()) - reference_keys}\n"
            f"  only in night2 slim: {reference_keys - set(slim.keys())}"
        )
    with open(slim_path, "w", encoding="utf-8") as f:
        json.dump(slim, f, indent=1)
    return d


def write_iter_wall_csv_gz(raw_json, out_path):
    iw = raw_json.get("iter_wall_s") or []
    with gzip.open(out_path, "wt", encoding="utf-8") as f:
        for v in iw:
            f.write(f"{v}\n")
    return len(iw)


def write_train_loss_last1000(raw_json, out_path):
    tlpi = raw_json.get("train_loss_per_iter") or []
    last = tlpi[-1000:]
    with open(out_path, "w", encoding="utf-8") as f:
        for v in last:
            f.write(f"{v}\n")
    return len(last)


def two_phase_price(raw_json, split_iter=150000):
    iw = raw_json.get("iter_wall_s") or []
    n = len(iw)
    phase1 = iw[999:split_iter] if n > 999 else []
    phase2 = iw[split_iter:] if n > split_iter else []
    return (
        statistics.median(phase1) if phase1 else None,
        statistics.median(phase2) if phase2 else None,
        n,
    )


def chi2_ci_for_sigma(sd):
    lo = sd * math.sqrt(DF / CHI2_UPPER_4DF)
    hi = sd * math.sqrt(DF / CHI2_LOWER_4DF)
    return lo, hi


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # reference key set from an already-committed night-2 slim json
    ref_keys = set(load(os.path.join(NIGHT2_DIR, "night2_9991-001.slim.json")).keys())

    jobs = [
        ("night3_9991-003.json", "night3_9991-003.slim.json",
         "iter_wall_s_9991-003.csv.gz", "train_loss_last1000_9991-003.csv"),
        ("night3_9991-004.json", "night3_9991-004.slim.json",
         "iter_wall_s_9991-004.csv.gz", "train_loss_last1000_9991-004.csv"),
    ]

    raws = {}
    for raw_name, slim_name, iw_name, tl_name in jobs:
        raw_path = os.path.join(NIGHT_RAW, raw_name)
        d = make_slim(raw_path, os.path.join(OUT_DIR, slim_name), reference_keys=ref_keys)
        n_iw = write_iter_wall_csv_gz(d, os.path.join(OUT_DIR, iw_name))
        n_tl = write_train_loss_last1000(d, os.path.join(OUT_DIR, tl_name))
        p1, p2, n = two_phase_price(d)
        overall = statistics.median((d.get("iter_wall_s") or [])[999:]) if n > 999 else None
        print(f"{raw_name}: slim written, key-set matches night2 slim reference, "
              f"iter_wall rows={n_iw}, train_loss_last1000 rows={n_tl}, "
              f"phase1_median={p1}, phase2_median={p2}, overall_median={overall}, "
              f"n_iters_seen={n}")
        raws[raw_name] = d

    # --- wave json/launcher.log/progress.log copies (one wave, no reboot) --
    for fname in [
        "wave_night3.json", "wave_night3.launcher.log", "wave_night3.progress.log",
    ]:
        src = os.path.join(NIGHT_RAW, fname)
        dst = os.path.join(OUT_DIR, fname)
        with open(src, "rb") as f:
            content = f.read()
        with open(dst, "wb") as f:
            f.write(content)
        print(f"{fname} copied, {len(content)} bytes")

    # --- combined SIX-way (0, 0', 1, 2, 3, 4) checkpoint table --------------
    seed0 = load(os.path.join(NIGHT1_DIR, "night1_9991-000.slim.json"))
    seed0p = load(os.path.join(NIGHT1_DIR, "rep_9991-900.slim.json"))
    seed1 = load(os.path.join(NIGHT2_DIR, "night2_9991-001.slim.json"))
    seed2 = load(os.path.join(NIGHT2_DIR, "night2b_9991-002.slim.json"))
    seed3 = load(os.path.join(OUT_DIR, "night3_9991-003.slim.json"))
    seed4 = load(os.path.join(OUT_DIR, "night3_9991-004.slim.json"))

    def ckpts_by_iter(run):
        return {c["iteration"]: c["val_loss"] for c in run.get("checkpoint_metrics") or []}

    c0, c0p, c1, c2, c3, c4 = (
        ckpts_by_iter(r) for r in (seed0, seed0p, seed1, seed2, seed3, seed4)
    )
    common = sorted(set(c0) & set(c0p) & set(c1) & set(c2) & set(c3) & set(c4))
    print(f"common checkpoints across seed0, seed0', seed1, seed2, seed3, seed4: {len(common)}")

    csv_path = os.path.join(OUT_DIR, "night_report_checkpoints.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        f.write(
            "# FULL FLOAT from the run jsons' checkpoint_metrics (not "
            "tools/night/night_report.py's r4() 4-decimal formatter) -- "
            "hardening item 19 (docs/tool-hardening-package.md), same "
            "convention as results/night2/night_report_checkpoints.csv.\n"
        )
        f.write(
            "# script: results/night3/extract_night3.py -- see README.md "
            "for its sha256 and the exact command that produced this file.\n"
        )
        import csv
        w = csv.writer(f)
        w.writerow([
            "iteration",
            "val_loss_seed0", "val_loss_seed0prime", "val_loss_seed1",
            "val_loss_seed2", "val_loss_seed3", "val_loss_seed4",
        ])
        for it in common:
            v0, v0p, v1, v2, v3, v4 = c0[it], c0p[it], c1[it], c2[it], c3[it], c4[it]
            w.writerow([it, v0, v0p, v1, v2, v3, v4])
    print(f"night_report_checkpoints.csv written, {len(common)} rows -> {csv_path}")

    # --- rung table: SD at n=5 (seeds 0,1,2,3,4) vs n=3, chi2 CI for sigma --
    rung_by_seed = {}
    for name, run in [("0", seed0), ("0p", seed0p), ("1", seed1), ("2", seed2),
                       ("3", seed3), ("4", seed4)]:
        rung_by_seed[name] = {r["iteration"]: r["val_loss"] for r in run["rung_metrics"]}

    print("\nRung table, n=5 (seeds 0,1,2,3,4) vs n=3 (seeds 0,1,2), with chi2 CI for sigma at n=5:")
    for it in [1000, 5000, 25000, 250000]:
        vals5 = [rung_by_seed[s][it] for s in ("0", "1", "2", "3", "4")]
        vals3 = [rung_by_seed[s][it] for s in ("0", "1", "2")]
        sd5 = statistics.stdev(vals5)
        sd3 = statistics.stdev(vals3)
        lo, hi = chi2_ci_for_sigma(sd5)
        rep = abs(rung_by_seed["0p"][it] - rung_by_seed["0"][it])
        ratio = "undefined (div0)" if rep == 0 else f"{sd5 / rep:.4f}"
        print(f"  iter={it}: SD(n=5)={sd5:.4f} SD(n=3)={sd3:.4f} "
              f"95%CI(sigma,n=5)=[{lo:.4f}, {hi:.4f}] replicate|0p-0|={rep:.4f} "
              f"SD5/replicate={ratio}")

    # --- checkpoint plateau / minimum / late offsets for all six runs ------
    last10 = common[-10:]
    print("\nPlateau (mean of last 10 common checkpoints) and minimum per seed:")
    for name, c in [("seed0", c0), ("seed0prime", c0p), ("seed1", c1),
                     ("seed2", c2), ("seed3", c3), ("seed4", c4)]:
        plateau = statistics.mean(c[it] for it in last10)
        min_it = min(c, key=lambda k: c[k])
        print(f"  {name}: plateau(last10 common)={plateau:.4f} "
              f"min_ckpt_loss={c[min_it]:.4f} at iter {min_it}")

    after = [it for it in common if it > 150000]
    print(f"\nafter-150000 rows: {len(after)}")
    for name, (ca, cb) in [
        ("3-0", (c3, c0)), ("4-0", (c4, c0)), ("4-3", (c4, c3)),
    ]:
        d = [ca[it] - cb[it] for it in after]
        pos = sum(1 for x in d if x > 0)
        print(f"  {name}: mean={statistics.mean(d):.4f} min={min(d):.4f} "
              f"max={max(d):.4f} positive={pos}/{len(d)}")

    # within-pair offset (0,0') for reference, same window
    d0 = [c0p[it] - c0[it] for it in after]
    pos0 = sum(1 for x in d0 if x > 0)
    print(f"  0p-0 (reference): mean={statistics.mean(d0):.4f} min={min(d0):.4f} "
          f"max={max(d0):.4f} positive={pos0}/{len(d0)}")


if __name__ == "__main__":
    main()
