"""T-G6 (R1, D7, G2): the stamp check refuses a mocked torch version and a mocked DLL hash; with
no registered stamp it refuses unless the run is a validation run that says so, and then says
"STAMP NOT YET REGISTERED"; once a stamp is registered, --stamp-unregistered is refused.
Revision 1.5 (G17) registers V1's stamp as the module default."""
import json

import pytest

import instrument as I
from conftest import needs_gpu, run_torch

STAMP = {"python": "3.10.20", "numpy": "2.2.6", "torch": "2.9.1+cu128", "cuda": "12.8",
         "dll_sha256": {"cublas64_12.dll": "a" * 64, "cublasLt64_12.dll": "b" * 64,
                        "cusolver64_11.dll": "c" * 64},
         "driver": "596.86", "gpu_name": "NVIDIA RTX PRO 4500 Blackwell"}


def _copy(**kw):
    s = json.loads(json.dumps(STAMP))
    s.update(kw)
    return s


def test_equal_stamp_passes():
    assert I.check_stamp(_copy(), registered=STAMP)["passed"] is True


def test_mocked_torch_version_refuses():
    with pytest.raises(ValueError, match="REFUSED \\(R1\\).*torch"):
        I.check_stamp(_copy(torch="2.9.2+cu128"), registered=STAMP)


def test_mocked_dll_hash_refuses():
    s = _copy()
    s["dll_sha256"]["cusolver64_11.dll"] = "d" * 64
    with pytest.raises(ValueError, match="cusolver64_11.dll"):
        I.check_stamp(s, registered=STAMP)
    s = _copy()
    del s["dll_sha256"]["cublas64_12.dll"]
    with pytest.raises(ValueError, match="cublas64_12.dll"):
        I.check_stamp(s, registered=STAMP)


@pytest.mark.parametrize("field,value", [("python", "3.10.21"), ("numpy", "2.2.7"),
                                         ("cuda", "12.9"), ("driver", "597.00"),
                                         ("gpu_name", "another GPU")])
def test_every_field_refuses(field, value):
    with pytest.raises(ValueError, match=field):
        I.check_stamp(_copy(**{field: value}), registered=STAMP)


def test_unregistered_mode():
    # the behaviour before revision 1.5 (G17), with no stamp given and no module default
    with pytest.raises(ValueError, match="no registered environment stamp"):
        I.check_stamp(_copy(), use_module_default=False)
    r = I.check_stamp(_copy(), allow_unregistered=True, use_module_default=False)
    assert r["passed"] is None and r["status"].startswith("STAMP NOT YET REGISTERED")
    with pytest.raises(ValueError, match="not accepted once it is"):
        I.check_stamp(_copy(), registered=STAMP, allow_unregistered=True)


def test_registered_stamp_is_v1s():
    """G17 (revision 1.5): the module default is the stamp V1 measured, read from V1.json; once
    it is registered, --stamp-unregistered refuses and a different field refuses."""
    v1 = json.loads((I.VALIDATION_DIR / "V1.json").read_text(encoding="utf-8"))
    assert I.REGISTERED_STAMP == v1["details"]["stamp_to_register_in_instrument_REGISTERED_STAMP"]
    assert set(I.REGISTERED_STAMP) == set(I.STAMP_FIELDS)
    assert I.check_stamp(json.loads(json.dumps(I.REGISTERED_STAMP)))["passed"] is True
    with pytest.raises(ValueError, match="not accepted once it is"):
        I.check_stamp(json.loads(json.dumps(I.REGISTERED_STAMP)), allow_unregistered=True)
    bad = json.loads(json.dumps(I.REGISTERED_STAMP))
    bad["driver"] = "597.00"
    with pytest.raises(ValueError, match="driver"):
        I.check_stamp(bad)


@needs_gpu
def test_real_stamp_against_mocked_registered_stamp():
    code = ("import gpu_env, json, instrument as I\n"
            "s = gpu_env.stamp()\n"
            "assert set(s) == set(I.STAMP_FIELDS), s\n"
            "assert all(v for v in s['dll_sha256'].values()), s\n"
            "I.check_stamp(s, registered=json.loads(json.dumps(s)))\n"
            "bad = json.loads(json.dumps(s)); bad['torch'] = '0.0.0'\n"
            "try:\n"
            "    I.check_stamp(s, registered=bad)\n"
            "except ValueError as e:\n"
            "    print('refused', 'torch' in str(e))\n"
            "bad = json.loads(json.dumps(s)); bad['dll_sha256']['cublasLt64_12.dll'] = '0' * 64\n"
            "try:\n"
            "    I.check_stamp(s, registered=bad)\n"
            "except ValueError as e:\n"
            "    print('refused', 'cublasLt64_12.dll' in str(e))\n")
    r = run_torch(code)
    assert r.returncode == 0, r.stderr
    assert r.stdout.split() == ["refused", "True", "refused", "True"]
