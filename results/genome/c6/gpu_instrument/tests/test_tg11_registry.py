"""T-G11 (revision 1.5: G17, G18, G19, G-(10)); CPU only, no CUDA call.

G19: the closed set of arm modules. An arm run refuses every module (none is registered), block
B's script and A's included; a validation run accepts A's script under every label and the male
arm's script only under V8 / smoke with a lobe; any other module is refused; the registered driver
itself refuses block B's script in an arm run (subprocess, torch CPU device, CUDA hidden).
G18: the composition identity is three values compared together; the registered identity of A is
V1's triple; V8's lobes carry V1's refusal digest but not its identity; each axis refuses alone;
the CPU stage (G13) refuses a GPU stage whose identity differs.
G-(10): the registration label is derived from the text's content hash.
G17: the VRAM need at row_chunk 40,000 is V1's measured peak (12,550 MiB).
"""
import json
import os
import subprocess
import sys

import pytest

import instrument as I
from conftest import GI

DATA = I.DATA_ROOT
V1_RUN = DATA / "V1_run_20260926T132024Z_a0e16b696389"
V8_RUNS = {"L": DATA / "V8_L_20260926T164600Z_e50bf74fc609",
           "R": DATA / "V8_R_20260926T173837Z_e50bf74fc609"}
BLOCK_B = "knockout_regrow_block_b"
MALE = "knockout_regrow_male_cns"


@pytest.mark.parametrize("module,lobe", [("knockout_regrow", None), (BLOCK_B, None),
                                         (MALE, "L"), ("male_arm", "L"), ("anything", None)])
def test_g19_arm_runs_refuse_every_module(module, lobe):
    why = I.arm_module_refusal("arm", "x", module, lobe)
    assert why and "G19" in why and "D11" in why


@pytest.mark.parametrize("label", ["V0", "V1", "V4a", "V6", "V7", "smoke"])
def test_g19_validation_accepts_a(label):
    assert I.arm_module_refusal("validation", label, "knockout_regrow", None) is None


def test_g19_validation_male_and_others():
    assert I.arm_module_refusal("validation", "V8", MALE, "L") is None
    assert I.arm_module_refusal("validation", "smoke", MALE, "R") is None
    assert "D11" in I.arm_module_refusal("validation", "V1", MALE, "L")
    assert "needs --lobe" in I.arm_module_refusal("validation", "V8", MALE, None)
    assert "takes no lobe" in I.arm_module_refusal("validation", "V1", "knockout_regrow", "L")
    assert "G19" in I.arm_module_refusal("validation", "V1", BLOCK_B, None)


def test_g19_registries_as_revision_1_5_registers_them():
    assert I.REGISTERED_ARM_MODULES == {}
    assert set(I.VALIDATION_ARM_MODULES) == {"knockout_regrow", MALE}


def test_g19_driver_refuses_block_b_in_an_arm_run(tmp_path):
    env = dict(os.environ)
    for v in ("CUBLAS_WORKSPACE_CONFIG", "GPU_INSTRUMENT_FLAGS_OFF", "OMP_NUM_THREADS",
              "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        env.pop(v, None)
    env.update(GPU_INSTRUMENT_DEVICE="cpu", CUDA_VISIBLE_DEVICES="-1", PYTHONUTF8="1")
    r = subprocess.run([sys.executable, "run_registered.py", "--kind", "arm", "--label", "x",
                        "--arm-module", BLOCK_B, "--keys", "world:R:0", "--expect-identity", "A",
                        "--out", str(tmp_path / "o")], cwd=GI, capture_output=True, text=True,
                       env=env, timeout=600)
    out = r.stdout + r.stderr
    assert r.returncode != 0
    assert f"REFUSED (G19, D11): arm module '{BLOCK_B}'" in out
    assert not (tmp_path / "o").exists()


def _manifest(d):
    return json.loads((d / "manifest.json").read_text(encoding="utf-8"))


def _identity_of(m):
    return I.composition_identity(m["composition"]["refusal_digest"], m["degree_terms_digest"],
                                  m["arm"]["module"], m["arm"]["lobe"])


@pytest.mark.skipif(not V1_RUN.is_dir(), reason="V1's private run folder absent")
def test_g18_registered_identity_is_v1s_and_v8_differs():
    found = _identity_of(_manifest(V1_RUN))
    assert found == I.REGISTERED_COMPOSITION_IDENTITIES["A"]
    assert I.check_composition_identity(found, I.REGISTERED_COMPOSITION_IDENTITIES["A"])["passed"]
    for lobe, d in V8_RUNS.items():
        m = _manifest(d)
        assert m["composition"]["refusal_digest"] == I.REGISTERED_COMPOSITION_DIGESTS["A"]
        with pytest.raises(ValueError, match="G18") as e:
            I.check_composition_identity(_identity_of(m), I.REGISTERED_COMPOSITION_IDENTITIES["A"])
        assert "'world'" in str(e.value) and "'script'" in str(e.value)
        assert "'composition'" not in str(e.value).split(":")[0]


@pytest.mark.parametrize("axis", I.IDENTITY_AXES)
def test_g18_each_axis_refuses_alone(axis):
    ref = json.loads(json.dumps(I.REGISTERED_COMPOSITION_IDENTITIES["A"]))
    bad = json.loads(json.dumps(ref))
    bad[axis] = {"module": "knockout_regrow", "lobe": "L"} if axis == "script" else "0" * 64
    with pytest.raises(ValueError, match=f"\\['{axis}'\\]"):
        I.check_composition_identity(bad, ref)
    assert I.check_composition_identity(ref, None)["passed"] is None


def test_g18_cpu_stage_refuses_another_identity(tmp_path):
    import hybrid_arm
    terms = (0.0, [0.0], [0.0])
    keys = ["world:R:0"]
    d = tmp_path / "run"
    d.mkdir()
    m = {"kind": "arm", "keys": keys, "git_head": "x",
         "composition": {"ranks": [1, 2, 3, 4], "starts": 10,
                         "refusal_digest": I.composition_digest(keys, 10, (1, 2, 3, 4))},
         "degree_terms_digest": I.degree_terms_digest(terms),
         "arm": {"module": BLOCK_B, "lobe": None}, "stamp": {}, "overrides": {},
         "files": {"records": "raw_fits_gpu.json.gz"}}
    (d / "manifest.json").write_text(json.dumps(m), encoding="utf-8")
    I.write_json_gz(d / "raw_fits_gpu.json.gz", {})
    I.write_sha256sums(d)
    expected = I.composition_identity(m["composition"]["refusal_digest"],
                                      m["degree_terms_digest"], "knockout_regrow", None)
    with pytest.raises(hybrid_arm.GpuStageRefused, match="G18.*script"):
        hybrid_arm.check_gpu_stage(d, keys, m["composition"]["refusal_digest"], terms,
                                   registered_stamp={}, own_head="x", own_dirty=[],
                                   file_hashes={}, expected_identity=expected)


def test_g10_label_from_content(tmp_path):
    rec = I.registration_text_record()
    assert rec["sha256_lf"] in I.REGISTRATION_TEXTS
    assert (I.REGISTRATION_REVISION, I.REGISTRATION_COMMIT) == I.REGISTRATION_TEXTS[
        rec["sha256_lf"]][:2]
    p = tmp_path / "reg.md"
    p.write_bytes((I.ROOT / I.REGISTRATION).read_bytes().replace(b"\r\n", b"\n") + b"\nedit\n")
    other = I.registration_text_record(p)
    assert other["revision"] == "UNKNOWN" and other["commit"] is None
    crlf = tmp_path / "crlf.md"
    crlf.write_bytes((I.ROOT / I.REGISTRATION).read_bytes().replace(b"\r\n", b"\n")
                     .replace(b"\n", b"\r\n"))
    assert I.registration_text_record(crlf)["sha256_lf"] == rec["sha256_lf"]


def test_g10_v0_v7_records_carry_the_stale_constant():
    """The ledger fact of G-(10), read from the committed records (never edited): they name
    revision 1.3 at head a0e16b6, whose registration text maps to revision 1.4."""
    for n in ("V0", "V1", "V2", "V3", "V4", "V5", "V6", "V7"):
        row = json.loads((I.VALIDATION_DIR / f"{n}.json").read_text(encoding="utf-8"))
        assert row["head"].startswith("a0e16b6") and "revision 1.3 (ec5cbc0)" in row["registration"]
    r = subprocess.run(["git", "show", "a0e16b6:" + I.REGISTRATION], cwd=I.ROOT,
                       capture_output=True, check=True)
    import hashlib
    h = hashlib.sha256(r.stdout.replace(b"\r\n", b"\n")).hexdigest()
    assert I.REGISTRATION_TEXTS[h][0] == "1.4"


def test_g17_vram_need_is_v1s_peak():
    assert I.REGISTERED_VRAM_NEED_MIB[40000] == 12550
    if V1_RUN.is_dir():
        peak = _manifest(V1_RUN)["vram"]["torch_peak_alloc_mib"]
        assert int(round(peak)) == 12550


def test_block_b_folders_are_reference_dirs():
    refs = {p.resolve() for p in I.reference_dirs()}
    for d in I.BLOCK_B_REFERENCE_DIRS:
        assert d.resolve() in refs
        assert I.out_dir_refusal(d / "x") is not None
