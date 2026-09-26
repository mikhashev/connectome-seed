"""T-G8 (G12, D9 (b)): the arm's path check passes a BF record with lambda, labels and AUC equal and
no flipped pair (its |dp| printed), and fails one with a flipped pair or with another lambda; rule
#2.1 stays exact. Fixtures: world:W:0, the bank of A's path check (its five ko fits selected
lambda = 1; its ko1 records are the fitted refits, bit-equal in the pinned store)."""
import copy

import numpy as np

import hybrid_arm as HA

BK = "world:W:0"


def _F(pinned):
    return {tuple(k.split("||")): v for k, v in pinned.items() if k.startswith(BK + "||")}


def test_equal_record_passes_with_dp_printed(pinned):
    for r in (1, 2, 3, 4):
        cpu = pinned[f"{BK}||ko1||BF:{r}"]
        gpu = pinned[f"{BK}||ko||BF:{r}"]
        res = HA.path_check_bf(cpu, gpu, BK)
        assert res["passed"] and res["n_flips"] == 0 and "max_abs_dp" in res


def test_small_dp_without_flip_passes(pinned):
    cpu = pinned[f"{BK}||ko1||BF:1"]
    gpu = copy.deepcopy(pinned[f"{BK}||ko||BF:1"])
    p = np.asarray(gpu["p"])
    i = int(np.argmax(p))
    gpu["p"][i] = float(np.nextafter(p[i], 1.0))
    res = HA.path_check_bf(cpu, gpu, BK)
    assert res["passed"] and not res["bit_equal"] and res["max_abs_dp"] > 0


def test_flipped_pair_fails(pinned):
    cpu = pinned[f"{BK}||ko1||BF:2"]
    gpu = copy.deepcopy(pinned[f"{BK}||ko||BF:2"])
    p = np.asarray(gpu["p"])
    o = np.argsort(p)
    a, b = next((int(u), int(v)) for u, v in zip(o[:-1], o[1:]) if p[u] != p[v])
    gpu["p"][a], gpu["p"][b] = float(p[b]), float(p[a])   # an opposite order (all pairs, base)
    res = HA.path_check_bf(cpu, gpu, BK)
    assert res["n_flips"] >= 1 and not res["passed"]


def test_other_lambda_fails(pinned):
    cpu = pinned[f"{BK}||ko1||BF:3"]
    gpu = copy.deepcopy(pinned[f"{BK}||ko||BF:3"])
    gpu["lam"] = 3.0
    assert not HA.path_check_bf(cpu, gpu, BK)["passed"]


def test_rule_stays_exact(pinned):
    rec = pinned[f"{BK}||ko||rule"]
    assert HA.path_check_rule(copy.deepcopy(rec), rec)["passed"]
    moved = copy.deepcopy(rec)
    moved["p"][0] = float(np.nextafter(moved["p"][0], 1.0))
    assert not HA.path_check_rule(moved, rec)["passed"]


def test_hybrid_path_check_on_w0(pinned):
    F = _F(pinned)

    def refit(bk, pk):
        return pinned[f"{bk}||ko1||{pk}"]
    res = HA.fixed_lambda_path_check_hybrid(F, [BK], refit)
    assert res["bank"] == BK and res["passed"] is True
    F2 = dict(F)
    g = copy.deepcopy(F[(BK, "ko", "BF:4")])
    g["lam"] = 3.0
    F2[(BK, "ko", "BF:4")] = g
    assert HA.fixed_lambda_path_check_hybrid(F2, [BK], refit)["bank"] is None


def test_r5_prerun_reproduced(tmp_path):
    """R5 (with G6's sidecar): equal hash sidecars pass; one changed hash refuses."""
    import json
    import instrument as I
    import pytest

    def mk(name, hashes):
        d = tmp_path / name
        d.mkdir()
        (d / "manifest.json").write_text(json.dumps(
            {"composition": {"refusal_digest": "d"}, "files": {"hashes": "fit_hashes.json"}}),
            encoding="utf-8")
        (d / "fit_hashes.json").write_text(json.dumps(hashes), encoding="utf-8")
        I.write_sha256sums(d)
        return d
    h = {"world:R:0||ko||BF:1": {"U": "a", "V": "b", "lambda": "c", "p": "d"}}
    assert HA.check_prerun_reproduced(mk("pre", h), mk("run", h))["passed"]
    h2 = {"world:R:0||ko||BF:1": {"U": "a", "V": "b", "lambda": "c", "p": "e"}}
    with pytest.raises(HA.GpuStageRefused, match="R5"):
        HA.check_prerun_reproduced(tmp_path / "pre", mk("run2", h2))
