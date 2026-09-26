"""T-G2 (R6, G7): every entry point refuses real, real|sh:0, real|pc:0, real|leak, world:R:0|pc:0
and a malformed key: instrument.check_key, the composition digest, prep.prepare_key_compact, the
comparator's run reader, the CPU stage's import (G13), and the driver (a subprocess)."""
import json

import pytest

import instrument as I
from conftest import needs_gpu, run_torch

BAD = ["real", "real|sh:0", "real|pc:0", "real|leak", "world:R:0|pc:0", "world:R:0|leak",
       "world:R", "world:R:x", "world:R:0|sh:", "world:R:0||ko", " world:R:0", "WORLD:R:0"]
GOOD = ["world:R:0", "world:M0.85:2|sh:79", "world:Nf:4|sh:0"]


@pytest.mark.parametrize("key", BAD)
def test_check_key_refuses(key):
    with pytest.raises(ValueError, match="REFUSED"):
        I.check_key(key)


@pytest.mark.parametrize("key", GOOD)
def test_check_key_accepts(key):
    assert I.check_key(key) == key


@pytest.mark.parametrize("key", BAD)
def test_digest_refuses(key):
    with pytest.raises(ValueError, match="REFUSED"):
        I.composition_digest(["world:R:0", key], 10, (1, 2, 3, 4))


@pytest.mark.parametrize("key", BAD)
def test_prep_refuses(key):
    import prep
    with pytest.raises(ValueError, match="REFUSED"):
        prep.prepare_key_compact(key)


def _fake_run(tmp_path, keys):
    d = tmp_path / "run"
    d.mkdir()
    m = {"kind": "arm", "keys": keys, "composition": {"ranks": [1, 2, 3, 4], "starts": 10},
         "files": {"records": "raw_fits_gpu.json.gz"}}
    (d / "manifest.json").write_text(json.dumps(m), encoding="utf-8")
    I.write_json_gz(d / "raw_fits_gpu.json.gz", {})
    I.write_sha256sums(d)
    return d


@pytest.mark.parametrize("key", ["real", "real|pc:0", "world:R:0|pc:0"])
def test_comparator_refuses(tmp_path, key):
    import gpu_equivalence as G
    d = _fake_run(tmp_path, ["world:R:0", key])
    with pytest.raises(ValueError, match="REFUSED"):
        G.read_gpu_run(d)


@pytest.mark.parametrize("key", ["real", "real|sh:0", "world:R:0|pc:0"])
def test_cpu_stage_import_refuses(tmp_path, key):
    import hybrid_arm
    d = _fake_run(tmp_path, ["world:R:0", key])
    with pytest.raises(hybrid_arm.GpuStageRefused, match="R6"):
        hybrid_arm.check_gpu_stage(d, ["world:R:0"], "0" * 64, (0.0, [0.0], [0.0]),
                                   registered_stamp={}, own_head="x", own_dirty=[],
                                   file_hashes={})
    with pytest.raises(ValueError, match="REFUSED"):
        hybrid_arm.check_gpu_stage(d, ["world:R:0", key], "0" * 64, (0.0, [0.0], [0.0]),
                                   registered_stamp={}, own_head="x", own_dirty=[],
                                   file_hashes={})


@needs_gpu
@pytest.mark.parametrize("key", ["real", "real|leak", "world:R:0|pc:0"])
def test_driver_refuses(key, tmp_path):
    r = run_torch("import sys, runpy; sys.argv = ['run_registered.py', '--kind', 'validation', "
                  f"'--label', 'smoke', '--keys', 'world:R:0,{key}', '--stamp-unregistered', "
                  f"'--allow-dirty', '--out', r'{tmp_path / 'o'}']; "
                  "runpy.run_path('run_registered.py', run_name='__main__')")
    assert r.returncode != 0
    assert "REFUSED (R6)" in (r.stdout + r.stderr)
    assert not (tmp_path / "o").exists()
