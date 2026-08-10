"""Closure, config-integrity, and ladder-regression tests.

Regression values are pinned at costingfe ac2d1a8 (cylinder geometry +
wall audit + shot-cycled CAS72 replacement scope + physics-consistent
store markup). If costingfe moves and a number shifts, the ladder in
docs/ledger.md must be re-based in the same change that updates the pin
here - the red-team review's reproducibility finding is the reason this
file exists.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from study import (  # noqa: E402
    E_FLASH_MELT_MJ_M2,
    apply_records,
    build_model,
    coherence_violations,
    f_rad_floor,
    load_config,
    run,
    wall_area_m2,
)

TIER_CONFIGS = ("best_case.yaml", "tier2.yaml", "tier3.yaml")


@pytest.fixture(scope="module")
def base_cfg():
    return load_config("baseline.yaml")


@pytest.fixture(scope="module")
def model(base_cfg):
    return build_model(base_cfg)


# --- config integrity ------------------------------------------------------

def test_every_record_has_value_and_source():
    for name in TIER_CONFIGS:
        for knob, rec in load_config(name)["records"].items():
            assert "value" in rec and "source" in rec, (name, knob)
            assert isinstance(rec["value"], (int, float, str)), (
                f"{name}:{knob} value parsed as {type(rec['value'])} - "
                "YAML scientific notation needs a signed exponent (1.0e+9)"
            )


def test_numeric_records_are_numeric():
    # every record except fw_class must be a number (the YAML 1.0e9-as-string
    # trap actually bit this study once)
    for name in TIER_CONFIGS:
        for knob, rec in load_config(name)["records"].items():
            if knob == "fw_class":
                continue
            assert isinstance(rec["value"], (int, float)), (name, knob)


def test_records_move_the_model(model, base_cfg):
    """Each tier-2 record, applied alone to the tier-1 stack, changes LCOE.

    Guards against silent no-op knobs (a typo'd key would be absorbed into
    params without effect).
    """
    fwd1 = dict(base_cfg["forward"])
    apply_records(fwd1, "best_case.yaml")
    _, diag1 = run(model, fwd1)
    coupled = {"dhe3_dd_frac": {"f_rad": 0.28}}  # mix moves with its floor
    for knob, rec in load_config("tier2.yaml")["records"].items():
        if knob == "f_rad":
            continue  # tested through dhe3_dd_frac's coupling
        fwd = dict(fwd1, **{knob: rec["value"]}, **coupled.get(knob, {}))
        _, diag = run(model, fwd)
        assert diag["lcoe"] != pytest.approx(diag1["lcoe"], rel=1e-6), knob


# --- coherence helpers -----------------------------------------------------

def test_f_rad_floor_anchors():
    assert f_rad_floor(0.314) == pytest.approx(0.163)
    assert f_rad_floor(0.85) == pytest.approx(0.28)
    assert f_rad_floor(0.0) == pytest.approx(0.0944, rel=1e-2)
    # D-rich radiates more, not less
    assert f_rad_floor(0.85) > f_rad_floor(0.314) > f_rad_floor(0.131)


def test_wall_area_matches_costingfe_cylinder():
    fwd = {"plasma_t": 0.5, "chamber_length": 10.0}
    assert wall_area_m2(fwd) == pytest.approx(37.699, rel=1e-3)


def test_coherence_catches_the_withdrawn_tier2_point(model, base_cfg):
    """The earlier draft's tier-2 point (f_rad 0.05 at dd_frac 0.85,
    eta_dec 0.97 x f_pdv 0.95) must be flagged, not silently accepted."""
    fwd = dict(base_cfg["forward"])
    apply_records(fwd, "best_case.yaml")
    apply_records(fwd, "tier2.yaml")
    fwd.update(dhe3_dd_frac=0.85, f_rad=0.05, eta_dec=0.97, f_pdv=0.95,
               max_f_rep=10.0)
    _, diag = run(model, fwd)
    v = "; ".join(coherence_violations(fwd, diag, "tier2"))
    assert "bremsstrahlung floor" in v
    assert "composite cap" in v


# --- ladder regression (costingfe ac2d1a8) ---------------------------------

def _ladder_lcoe(model, base_cfg, *cfgs):
    fwd = dict(base_cfg["forward"])
    for c in cfgs:
        apply_records(fwd, c)
    _, diag = run(model, fwd)
    return diag


def test_baseline_rung(model, base_cfg):
    diag = _ladder_lcoe(model, base_cfg)
    assert diag["lcoe"] == pytest.approx(133.3, abs=0.2)
    assert diag["n_mod"] == 24


def test_tier1_rung(model, base_cfg):
    diag = _ladder_lcoe(model, base_cfg, "best_case.yaml")
    assert diag["lcoe"] == pytest.approx(104.5, abs=0.2)


def test_tier2_rung(model, base_cfg):
    diag = _ladder_lcoe(model, base_cfg, "best_case.yaml", "tier2.yaml")
    assert diag["lcoe"] == pytest.approx(38.6, abs=0.2)
    # D-rich mix carries its plant; the adder is anchored at 200 M$ for this
    # rung's own throughput (185 MW plant neutron power)
    assert diag["tritium_adder_musd"] == pytest.approx(200.0, abs=0.5)


def test_tritium_adder_scales_with_throughput(model, base_cfg):
    """A 3 GWe D-rich plant pays about 3x the reference tritium plant; the
    facility does not amortize away with scale."""
    fwd = dict(base_cfg["forward"], net_electric_mw=3000.0)
    apply_records(fwd, "best_case.yaml")
    apply_records(fwd, "tier2.yaml")
    _, diag = run(model, fwd)
    assert diag["tritium_adder_musd"] == pytest.approx(500.0, rel=0.1)


def test_tier3_rung(model, base_cfg):
    diag = _ladder_lcoe(model, base_cfg, *TIER_CONFIGS)
    assert diag["lcoe"] == pytest.approx(16.6, abs=0.2)


def test_tier2_coherent_minimum(model, base_cfg):
    fwd = dict(base_cfg["forward"])
    apply_records(fwd, "best_case.yaml")
    apply_records(fwd, "tier2.yaml")
    fwd.update(chamber_length=20.0, plasma_t=0.5, r_bore=0.6, fw_class="panel")
    _, diag = run(model, fwd)
    assert diag["lcoe"] == pytest.approx(33.9, abs=0.2)
    assert not coherence_violations(fwd, diag, "tier2")


def test_tier3_coherent_minimum(model, base_cfg):
    fwd = dict(base_cfg["forward"])
    for c in TIER_CONFIGS:
        apply_records(fwd, c)
    fwd.update(yield_per_shot_mj=300.0, chamber_length=45.0, plasma_t=1.0,
               r_bore=1.1, fw_class="panel")
    _, diag = run(model, fwd)
    assert diag["lcoe"] == pytest.approx(15.8, abs=0.2)
    assert not coherence_violations(fwd, diag, "tier3")
    assert diag["e_flash_mj_m2"] < E_FLASH_MELT_MJ_M2


def test_tier_stacks_are_coherent(model, base_cfg):
    """Every published rung must pass its own tier's coherence check."""
    fwd = dict(base_cfg["forward"])
    for cfgs, tier in ((("best_case.yaml",), "tier2"),
                       (("best_case.yaml", "tier2.yaml"), "tier2"),
                       (TIER_CONFIGS, "tier3")):
        f = dict(base_cfg["forward"])
        for c in cfgs:
            apply_records(f, c)
        _, diag = run(model, f)
        assert not coherence_violations(f, diag, tier), (cfgs, tier)


def test_tritium_in_pulse_burn_anchors():
    """The dhe3_f_T = 0 audit: reactor-class corner (1e23 m^-3, 50 keV,
    1 ms) burns about 4% of bred tritium in-pulse; the Trenta-class
    sub-millisecond corner stays under 1%."""
    from tritium_burn import burn_probability

    assert burn_probability(1e23, 50.0, 1e-3) == pytest.approx(0.043, abs=0.005)
    assert burn_probability(3e22, 50.0, 3e-4) < 0.01
