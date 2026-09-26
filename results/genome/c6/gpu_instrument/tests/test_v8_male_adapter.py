"""V8's male adapter (G7 for knockout_regrow_male_cns, male_arm.py) and V8's refusals.

GPU instrument registration, revision 1.4, section 7 (V8) and G7; the male arm's registration,
revision 1.1, D13 (iii). Fixtures: the male arm's outside files (pinned, read by the male
script's own loader) and small synthetic stores in pytest's tmp folders. No test opens, hashes,
parses or sizes a sealed file: the autouse guard replaces the male script's sealed-file readers
(open_sealed, verify_sealed_pins, parse_sealed, sealed_path, real_bank) with functions that record
the call and raise, and every test must end with zero calls.

  * the adapter's banks equal the male script's own banks key by key (exists, content), and so do
    the degree terms and every GPU input prepared from them (N1, grids, folds, SVD starts are
    computed from the bank, so equal banks and equal grids give bit-equal inputs; they are
    compared as well);
  * the lobe and the grid restriction hold in every prep worker (spawned pool);
  * no sealed path is reachable; a real (or any non-world) key is refused;
  * V8 refuses cleanly (exit 2, before any GPU stage) when a lobe's store is absent or unfinished,
    and when the store's inputs differ from the adapter's; on a verified fixture store it prints
    the BF-active classification before the GPU stage (--inputs-only);
  * the comparator uses the male leg P (seeds 92000, 92001) for p_P and p_P_rowcol;
  * the driver refuses the male arm outside V8 (torch venv), and a GPU smoke of two banks.
"""
import argparse
import gzip
import json
import os
import pathlib
import subprocess
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pytest

import instrument as I
from conftest import GI, needs_gpu

MALE = "knockout_regrow_male_cns"
KEYS = ("world:R:0", "world:No:3|sh:0", "world:W:4|sh:84", "world:M0.85:2|sh:98")
SEALED_READERS = ("open_sealed", "verify_sealed_pins", "parse_sealed", "sealed_path", "real_bank")


@pytest.fixture(scope="module")
def M():
    import knockout_regrow_male_cns
    return knockout_regrow_male_cns


@pytest.fixture(scope="module")
def outside_files(M):
    missing = [lobe for lobe in M.LOBES
               if not (M.MALE_BUILD_DIR / f"male_cns_{lobe}_outside.csv").is_file()]
    if missing:
        pytest.skip(f"the male outside files are absent ({missing})")
    return True


@pytest.fixture(autouse=True)
def isolate(monkeypatch, M):
    """Restore the harness grid and STARTS, prep's arm state and the male worker context after
    each test (the male restriction is process-wide), and guard the seal."""
    import harness as H
    import prep
    saved = (H.ALL_CELLS, H.STARTS, dict(prep._ARM), dict(prep._TERMS), dict(M._W))
    calls = []

    def reader(name):
        def refuse(*a, **k):
            calls.append(name)
            raise RuntimeError(f"TEST GUARD: {name} called")
        return refuse
    for name in SEALED_READERS:
        monkeypatch.setattr(M, name, reader(name))
    monkeypatch.setattr(M, "SEALED_DIR", M.SEALED_DIR)          # restored after the test
    monkeypatch.setitem(M._UNSEAL, "allowed", False)
    yield calls
    H.ALL_CELLS, H.STARTS = saved[0], saved[1]
    prep._ARM.clear()
    prep._ARM.update(saved[2])
    prep._TERMS.clear()
    prep._TERMS.update(saved[3])
    M._W.clear()
    M._W.update(saved[4])
    assert calls == [], f"a sealed-file reader was called: {calls}"


def _full_grid():
    import harness as H
    H.ALL_CELLS = np.array([(s, t) for s in range(65) for t in range(65)], dtype=np.int64)


def _male_own(M, lobe, keys):
    """The male script's own path, as its --synthetic-only main and its pool worker run it:
    restriction, the lobe's outside bank, degree terms; _w_init(10, terms, True, lobe, True,
    None); build_bank(key, _W); and its own _fit_one's N1 record (y, outside_density, p)."""
    import harness as H
    _full_grid()
    M._W.clear()
    M.restrict_to_placed_grid()
    terms = M.degree_terms(M.load_male_bank(lobe))
    M._w_init(10, terms, True, lobe, True, None)
    banks = {k: M.build_bank(k, M._W) for k in keys}
    n1 = {k: M._fit_one(k, "ko", "N1", banks[k]) for k in keys}
    import prep
    views = {k: prep.prepare_view(H.make_view(banks[k], M.MASKS["ko"])) for k in keys}
    return terms, banks, n1, views


def _content_equal(a, b):
    if set(a) != set(b):
        return False
    return all(a[k]["offsets"] == b[k]["offsets"] and a[k]["sign"] == b[k]["sign"]
               and list(a[k]["hull"]) == list(b[k]["hull"]) for k in a)


@pytest.mark.parametrize("lobe", ["L", "R"])
def test_adapter_banks_equal_the_male_scripts_own(M, outside_files, lobe):
    import harness as H
    import prep
    terms_m, banks_m, n1_m, views_m = _male_own(M, lobe, KEYS)
    # The adapter, as gpu_stage's main process and a fresh (spawned) prep worker run it.
    _full_grid()
    M._W.clear()
    K = prep.set_arm(MALE, lobe)
    assert K.__name__ == "male_arm" and prep._ARM["adapter"] == "male_arm"
    prep.restrict_grid(K)
    terms_a = K.degree_terms()
    assert terms_a[0] == terms_m[0]
    assert np.array_equal(terms_a[1], terms_m[1]) and np.array_equal(terms_a[2], terms_m[2])
    assert I.degree_terms_digest(terms_a) == I.degree_terms_digest(terms_m)
    _full_grid()
    M._W.clear()
    prep.init_arm_worker(MALE, lobe, terms_a)
    assert len(H.ALL_CELLS) == 3025
    for k in KEYS:
        b = K.build_bank(k, terms_a, True)
        assert b.name == banks_m[k].name
        assert np.array_equal(b.exists, banks_m[k].exists), k
        assert _content_equal(b.content, banks_m[k].content), k
        assert not (b.exists & ~M.PLACED_GRID).any()
        pp = prep.prepare_key_compact(k)
        v = views_m[k]
        assert np.array_equal(pp["O"][0], v["O"]) and np.array_equal(pp["O"][1:], v["Oi"])
        assert np.array_equal(pp["M"][0], v["M"]) and np.array_equal(pp["M"][1:], v["Mi"])
        assert np.array_equal(pp["Y"], v["Y"]) and np.array_equal(pp["test"][1:], v["test"])
        assert sorted(pp["n1"]) == sorted(v["n1"])
        assert all(np.array_equal(pp["n1"][f], v["n1"][f]) for f in v["n1"])
        # the record fields the GPU stage takes from the bank, against the male _fit_one's
        assert pp["y_block"].tolist() == n1_m[k]["y"]
        assert pp["outside_density"] == n1_m[k]["outside_density"]
        assert np.array_equal(pp["p_n1"], np.asarray(n1_m[k]["p"], np.float64))


def test_workers_hold_the_lobe_and_the_restriction(M, outside_files):
    """Spawned prep workers (Windows spawn re-imports everything with the full grid): every
    worker that runs a task reports the lobe, 3,025 cells, a synthetic pool with no real block
    and the seal guard, and prepares the bank the male script builds in this process."""
    import prep
    lobe = "R"
    terms, banks_m, _, views_m = _male_own(M, lobe, KEYS[:1])
    with ProcessPoolExecutor(max_workers=2, initializer=prep.init_arm_worker,
                             initargs=(MALE, lobe, terms, False)) as ex:
        recs = list(ex.map(prep.worker_record, range(6)))
        pp = ex.submit(prep.prepare_key_compact, KEYS[0]).result()
    for r in recs:
        w = r["arm"]
        s = w["arm_state"]
        assert (w["arm"], w["lobe"], w["adapter"], w["n_all_cells"]) == (MALE, lobe, "male_arm",
                                                                         3025)
        assert w["grid_restricted"] and w["starts"] == 10
        assert (s["lobe"], s["pool_lobe"], s["synthetic_only"], s["real_block_is_none"],
                s["restrict"], s["n_all_cells"]) == (lobe, lobe, True, True, True, 3025)
        assert s["content_pool_rows"] == 526                    # lobe R's present outside cells
        assert s["unseal_allowed"] is False and s["sealed_dir_exists"] is False
        assert r["degree_terms_digest"] == I.degree_terms_digest(terms)
    v = views_m[KEYS[0]]
    assert np.array_equal(pp["O"][0], v["O"]) and np.array_equal(pp["Y"], v["Y"])
    assert np.array_equal(pp["M"][0], v["M"])


@pytest.mark.parametrize("key", ["real", "real|sh:0", "outside", "outside|fill:z", "flyvis65",
                                 "world:R:0|pc:1", "world:R:0|fill:z"])
def test_non_world_keys_refused(M, outside_files, key):
    import prep
    K = prep.set_arm(MALE, "L")
    terms = K.degree_terms()
    prep.init_arm_worker(MALE, "L", terms)
    with pytest.raises(ValueError, match="REFUSED"):
        K.build_bank(key, terms, True)
    with pytest.raises(ValueError, match="REFUSED"):
        prep.prepare_key_compact(key)


def test_adapter_refuses_without_lobe_and_other_pools(M, outside_files):
    import prep
    import male_arm as MA
    with pytest.raises(RuntimeError, match="needs a lobe"):
        prep.set_arm(MALE, None)
    with pytest.raises(RuntimeError, match="lobe"):
        prep.set_arm(MALE, "X")
    K = prep.set_arm(MALE, "L")
    terms = K.degree_terms()
    # a pool initialised by the male script for the other lobe, or for the real arm, is refused
    M._w_init(10, terms, True, "R", True, None)
    with pytest.raises(RuntimeError, match="pool's lobe"):
        K.build_bank("world:R:0", terms, True)
    M._w_init(10, terms, False, "L", True, None)
    with pytest.raises(RuntimeError, match="not a synthetic pool"):
        K.build_bank("world:R:0", terms, True)
    K._w_init(10, terms, True)
    other = (terms[0] + 1.0, terms[1], terms[2])
    with pytest.raises(RuntimeError, match="degree terms"):
        K.build_bank("world:R:0", other, True)
    with pytest.raises(RuntimeError, match="synthetic"):
        K._w_init(10, terms, False)
    assert MA.outside_density is K.outside_density


def test_no_code_path_calls_a_sealed_reader():
    """Text check of the GPU side: no call of a sealed-file reader in any instrument file."""
    import re
    pat = re.compile(r"\b(" + "|".join(SEALED_READERS) + r")\s*\(")
    for p in sorted(GI.glob("*.py")):
        hits = [m.group(0) for m in pat.finditer(p.read_text(encoding="utf-8"))]
        assert not hits, (p.name, hits)


# ------------------------------------------------------------------------------------------
# V8's refusals and its input check.

@pytest.fixture
def v8_env(monkeypatch, tmp_path):
    """validation.py with its committed outputs redirected to tmp and the GPU stage forbidden."""
    import validation as VAL
    monkeypatch.setattr(I, "VALIDATION_DIR", tmp_path / "validation")
    monkeypatch.setattr(VAL, "TABLE", tmp_path / "validation" / "table.json")
    monkeypatch.setattr(I, "DATA_ROOT", tmp_path / "data")

    def no_gpu(*a, **k):
        raise AssertionError("the GPU stage must not be launched")
    monkeypatch.setattr(VAL, "run_gpu", no_gpu)
    return VAL


def _args(lobe, store=None, sha=None, inputs_only=False):
    return argparse.Namespace(lobe=lobe, male_store=store, male_store_sha256=sha,
                              inputs_only=inputs_only, allow_dirty=False, parts=None, run="V8")


@pytest.mark.parametrize("lobe", ["L", "R"])
def test_v8_refuses_cleanly_when_the_store_is_absent(v8_env, monkeypatch, tmp_path, lobe):
    VAL = v8_env
    monkeypatch.setattr(I, "MALE_PRERUN_STORES", {lb: tmp_path / f"absent_{lb}"
                                                  for lb in ("L", "R")})
    with pytest.raises(SystemExit) as e:
        VAL.v8(_args(lobe))
    assert e.value.code == 2
    table = json.loads(VAL.TABLE.read_text(encoding="utf-8"))
    assert table[f"V8_{lobe}"]["outcome"] == "REFUSED CLEANLY: inputs absent"
    assert "absent or not finished" in table[f"V8_{lobe}"]["text"]
    row = json.loads((I.VALIDATION_DIR / f"V8_{lobe}.json").read_text(encoding="utf-8"))
    assert "never an input to a male gate" in row["details"]["for"]


def test_v8_refuses_an_unfinished_store_and_a_missing_lobe(v8_env, tmp_path):
    VAL = v8_env
    d = tmp_path / "writing"
    d.mkdir()
    (d / "raw_fits.json.gz").write_bytes(b"not yet")          # no SHA256SUMS.txt yet
    with pytest.raises(SystemExit) as e:
        VAL.v8(_args("L", str(d)))
    assert e.value.code == 2
    with pytest.raises(SystemExit) as e:
        VAL.v8(_args(None))
    assert e.value.code == 2
    table = json.loads(VAL.TABLE.read_text(encoding="utf-8"))
    assert "--lobe L or R is required" in table["V8"]["text"]


def _fixture_store(M, VAL, folder, lobe, terms, script_sha=None, active=("world:R:0", 1),
                   full=True):
    """A complete synthetic store of V8's composition in the male store format: every planned BF
    ko record and its view's N1 record; BF p equal to N1's p (lambda 100) except one BF-active
    fit (lambda 1). Written as the male write_synthetic_outputs writes, SHA256SUMS.txt last.
    full=False writes no record (for the refusals that stop before the store is read)."""
    keys = VAL.male_keys(M) if full else []
    rng = np.random.default_rng(5)
    y = M.board_y("z")
    F = {}
    for k in keys:
        p = rng.random(64)
        F[f"{k}||ko||N1"] = {"p": p.tolist(), "y": y.tolist(), "lam": None,
                              "score": {"existence": 0.5}, "outside_density": 0.1, "secs": 0.0}
        for r in (1, 2, 3, 4):
            q = p.copy()
            lam = 100.0
            if (k, r) == active:
                q[0] = min(q[0] + 1e-3, 0.999)
                lam = 1.0
            F[f"{k}||ko||BF:{r}"] = {"p": q.tolist(), "y": y.tolist(), "lam": lam,
                                     "score": {"existence": 0.5}, "outside_density": 0.1,
                                     "secs": 0.0}
    folder.mkdir(parents=True)
    with gzip.open(folder / "raw_fits.json.gz", "wt", encoding="utf-8") as fh:
        json.dump(F, fh)
    man = {"mode": "synthetic-only", "smoke": False, "starts": 10, "worlds_per_family": 5,
           "shuffles": 99, "lobes": [lobe], "families": [f[0] for f in M.FAMILIES],
           "script_sha256_lf": script_sha or I.sha256_lf(VAL.MALE_SCRIPT), "git_head": "fixture",
           "not_a_reference": None, "reference_mode": False,
           "degree_terms": {lobe: {"c": terms[0], "a": terms[1].tolist(),
                                   "b": terms[2].tolist()}}}
    (folder / "synthetic_only.json").write_text(json.dumps({"manifest": man}), encoding="utf-8")
    I.write_sha256sums(folder)
    return folder


@pytest.fixture(scope="module")
def terms_L(M, outside_files):
    import harness as H
    saved = H.ALL_CELLS
    M.restrict_to_placed_grid()
    t = M.degree_terms(M.load_male_bank("L"))
    H.ALL_CELLS = saved
    return t


def test_v8_inputs_only_prints_bf_active_before_any_gpu(v8_env, M, terms_L, tmp_path, capsys):
    VAL = v8_env
    d = _fixture_store(M, VAL, tmp_path / "store_L", "L", terms_L)
    VAL.v8(_args("L", str(d), inputs_only=True))
    out = capsys.readouterr().out
    assert "D10: the adapter's degree terms equal the pre-run's" in out
    assert "before the GPU stage: the BF-active classification of the male worlds (4500 banks, " \
           "18000 BF ko fits)" in out
    assert "1 of 18000 fits have p different from their view's N1 p" in out
    assert not VAL.TABLE.exists()                                   # --inputs-only records nothing


def test_v8_refuses_other_inputs(v8_env, M, terms_L, tmp_path):
    VAL = v8_env
    other = (terms_L[0] + 2.0 ** -40, terms_L[1], terms_L[2])
    d = _fixture_store(M, VAL, tmp_path / "terms", "L", other, full=False)
    with pytest.raises(SystemExit) as e:
        VAL.v8(_args("L", str(d)))
    assert e.value.code == 2
    t = json.loads(VAL.TABLE.read_text(encoding="utf-8"))["V8_L"]
    assert t["outcome"] == "REFUSED CLEANLY: the adapter's inputs differ from the pre-run's"
    d2 = _fixture_store(M, VAL, tmp_path / "script", "L", terms_L, script_sha="0" * 64,
                        full=False)
    with pytest.raises(SystemExit) as e:
        VAL.v8(_args("L", str(d2)))
    assert e.value.code == 2
    t = json.loads(VAL.TABLE.read_text(encoding="utf-8"))["V8_L"]
    assert t["outcome"] == "REFUSED CLEANLY: the male store does not verify"
    assert "made by the male script" in t["text"]
    with pytest.raises(SystemExit) as e:                                  # wrong lobe
        VAL.v8(_args("R", str(d2 / "raw_fits.json.gz")))
    assert e.value.code == 2
    (d / "raw_fits.json.gz").write_bytes(b"changed")                    # SHA256SUMS fails
    with pytest.raises(SystemExit) as e:
        VAL.v8(_args("L", str(d)))
    assert e.value.code == 2
    t = json.loads(VAL.TABLE.read_text(encoding="utf-8"))["V8_L"]
    assert "SHA256SUMS" in t["text"]


def test_comparator_uses_the_male_leg_p(M, outside_files, monkeypatch):
    """p_P and p_P_rowcol of a base view under the male adapter are the male evaluate_bank's
    (uniform_perms default_rng(92000); rc_patterns default_rng(92001)), not A's (90000, 90001)."""
    import gpu_equivalence as G
    import male_arm as MA
    y = M.board_y("z")
    p = np.random.default_rng(11).random(64)
    a = M.auc(p, y)
    Yu = y[M.uniform_perms()]
    Yrc = M.rc_patterns(y, "synthetic")["patterns"]
    want = ((1 + int((M.auc_null(p, Yu) >= a - M.TAU).sum())) / (M.N_PERM + 1),
            (1 + int((M.auc_null(p, Yrc) >= a - M.TAU).sum())) / (M.N_PERM + 1))
    assert G.p_P_pair(p, y, MA) == want
    # A's null inputs differ (another seed): the cache is per arm
    Yu_a, _ = G.null_inputs(y)
    assert not np.array_equal(Yu_a, Yu)
    # compare_fit on a base view at risk takes the male p_P
    q = p.copy()
    q[1] = q[0] + 2.0 ** -30                                  # a gap below 2^-23 on the base view
    rec = {"p": q.tolist(), "y": y.tolist(), "lam": 1.0, "score": {"existence": 0.5},
           "outside_density": 0.1}
    ent = G.compare_fit("world:R:0||ko||BF:1", rec, rec, arm=MA)
    assert ent["at_risk"] and ent["e1"]["passed"] and ent["n_flips"] == 0
    assert ent["at_risk_outputs"]["p_P_ref"] == G.p_P_pair(q, y, MA)


# ------------------------------------------------------------------------------------------
# The driver (torch venv).

def _driver(args):
    env = dict(os.environ)
    for v in ("CUBLAS_WORKSPACE_CONFIG", "GPU_INSTRUMENT_FLAGS_OFF", "GPU_INSTRUMENT_DEVICE",
              "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
              "NUMEXPR_NUM_THREADS"):
        env.pop(v, None)
    return subprocess.run([str(I.TORCH_PY), "run_registered.py"] + args, cwd=GI,
                          capture_output=True, text=True, env=env)


@needs_gpu
def test_driver_refuses_the_male_arm_outside_v8(tmp_path):
    r = _driver(["--kind", "arm", "--label", "x", "--arm-module", MALE, "--lobe", "L", "--keys",
                 "world:R:0", "--expect-digest", "0" * 64, "--out", str(tmp_path / "a")])
    assert r.returncode != 0 and "D11" in (r.stdout + r.stderr)
    r = _driver(["--kind", "validation", "--label", "V1", "--arm-module", MALE, "--lobe", "L",
                 "--keys", "world:R:0", "--allow-dirty", "--stamp-unregistered", "--out",
                 str(tmp_path / "b")])
    assert r.returncode != 0 and "D11" in (r.stdout + r.stderr)
    r = _driver(["--kind", "validation", "--label", "V8", "--arm-module", MALE, "--keys",
                 "world:R:0", "--allow-dirty", "--stamp-unregistered", "--out",
                 str(tmp_path / "c")])
    assert r.returncode != 0 and "needs --lobe" in (r.stdout + r.stderr)


@needs_gpu
def test_gpu_smoke_two_male_banks(M, outside_files, tmp_path):
    """The registered driver on two male banks of lobe L (seconds of GPU): the manifest records
    the adapter, the lobe and the restriction in the prep worker, the degree terms of the male
    script's own path, the revision 1.4 registration, and R6-conform records."""
    out = tmp_path / "smoke"
    r = _driver(["--kind", "validation", "--label", "smoke", "--arm-module", MALE, "--lobe", "L",
                 "--keys", "world:R:0,world:R:0|sh:0", "--workers", "2", "--allow-dirty",
                 "--stamp-unregistered", "--out", str(out)])
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-3000:]
    assert f"revision {I.REGISTRATION_REVISION} ({I.REGISTRATION_COMMIT}" in r.stdout
    m = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    assert m["revision"] == "1.4" and m["registration_commit"] == "e2fab47"
    assert m["arm"]["module"] == MALE and m["arm"]["adapter"] == "male_arm"
    w = m["arm"]["worker_init"]
    assert w["lobe"] == "L" and w["n_all_cells"] == 3025
    assert w["arm_state"]["real_block_is_none"] and not w["arm_state"]["unseal_allowed"]
    terms, _, n1, _ = _male_own(M, "L", ("world:R:0", "world:R:0|sh:0"))
    assert m["degree_terms_digest"] == I.degree_terms_digest(terms)
    recs = I.read_store(out / "raw_fits_gpu.json.gz")
    assert sorted(recs) == sorted(f"{k}||ko||BF:{r}" for k in ("world:R:0", "world:R:0|sh:0")
                                  for r in (1, 2, 3, 4))
    for rk, rec in recs.items():
        k = rk.split("||")[0]
        assert rec["y"] == n1[k]["y"] and rec["outside_density"] == n1[k]["outside_density"]
