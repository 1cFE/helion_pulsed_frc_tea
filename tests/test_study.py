"""Closure, config-integrity, and ladder-regression tests.

Regression values are pinned at costingfe 44434d9 (cylinder geometry +
wall audit, shot-cycled CAS72 scope, physics-consistent store markup,
per-pulse fuel-cycle semantics). If costingfe moves and a number shifts, the ladder in
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
    # the double-booked f_pdv = 0.95 cannot execute: the chamber-coupled
    # radial bound clamps it before the run (0.8 x cap at the concept
    # chamber), so the composite never reaches the incoherent value
    assert diag["f_pdv_eff"] == pytest.approx(0.8 * diag["f_pdv_cap"], rel=1e-6)
    assert 0.97 * diag["f_pdv_eff"] < 0.80


# --- ladder regression (costingfe 44434d9) ---------------------------------

def _ladder_lcoe(model, base_cfg, *cfgs):
    fwd = dict(base_cfg["forward"])
    for c in cfgs:
        apply_records(fwd, c)
    _, diag = run(model, fwd)
    return diag


def test_helion_requirements_device(model, base_cfg):
    # the vendor configuration on the common plant-environment basis
    # (financing and availability shared by all four devices)
    diag = _ladder_lcoe(model, base_cfg)
    assert diag["lcoe"] == pytest.approx(121.4, abs=0.2)
    assert diag["n_mod"] == 28
    _, diag3 = run(model, dict(base_cfg["forward"], net_electric_mw=3000.0))
    assert diag3["lcoe"] == pytest.approx(116.9, abs=0.2)


def test_records_device(model, base_cfg):
    """The citable-records device: design-optimized under the record
    stack alone (the optimum is already the D-rich mix with its
    tritium plant, in fat panel-wall chambers)."""
    fwd = dict(base_cfg["forward"])
    apply_records(fwd, "best_case.yaml")
    fwd.update(dhe3_dd_frac=0.85, f_rad=0.28, chamber_length=10.0,
               plasma_t=1.0, r_bore=1.1, fw_class="panel")
    _, diag = run(model, fwd)
    assert diag["lcoe"] == pytest.approx(172.3, abs=0.2)
    assert not coherence_violations(fwd, diag, "tier2")
    _, diag3 = run(model, dict(fwd, net_electric_mw=3000.0))
    assert diag3["lcoe"] == pytest.approx(168.7, abs=0.2)


def test_tier1_rung(model, base_cfg):
    diag = _ladder_lcoe(model, base_cfg, "best_case.yaml")
    assert diag["lcoe"] == pytest.approx(206.2, abs=0.2)


def test_tier2_rung(model, base_cfg):
    diag = _ladder_lcoe(model, base_cfg, "best_case.yaml", "tier2.yaml")
    assert diag["lcoe"] == pytest.approx(55.9, abs=0.2)
    # D-rich mix carries its plant; the adder is unit-priced
    # (50 M$ + 0.657 M$/MW of plant neutron power), so the rung's value is a
    # consequence of its throughput, not an identity
    assert diag["tritium_adder_musd"] == pytest.approx(213.0, abs=1.0)


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
    assert diag["lcoe"] == pytest.approx(20.3, abs=0.2)


def test_tier2_coherent_minimum(model, base_cfg):
    fwd = dict(base_cfg["forward"])
    apply_records(fwd, "best_case.yaml")
    apply_records(fwd, "tier2.yaml")
    fwd.update(chamber_length=10.0, plasma_t=1.5, r_bore=1.6, fw_class="panel")
    _, diag = run(model, fwd)
    assert diag["lcoe"] == pytest.approx(45.1, abs=0.2)
    assert not coherence_violations(fwd, diag, "tier2")
    _, diag3 = run(model, dict(fwd, net_electric_mw=3000.0))
    assert diag3["lcoe"] == pytest.approx(41.1, abs=0.2)


def test_tier3_coherent_minimum(model, base_cfg):
    fwd = dict(base_cfg["forward"])
    for c in TIER_CONFIGS:
        apply_records(fwd, c)
    fwd.update(yield_per_shot_mj=500.0, chamber_length=30.0, plasma_t=1.5,
               r_bore=1.6, fw_class="panel")
    _, diag = run(model, fwd)
    assert diag["lcoe"] == pytest.approx(18.6, abs=0.2)
    assert not coherence_violations(fwd, diag, "tier3")
    assert diag["e_flash_mj_m2"] < E_FLASH_MELT_MJ_M2
    # the 3 GWe park uses the 200 MJ design: larger shots trip the wall
    # audit once the integer module count snaps down
    fwd3 = dict(fwd, yield_per_shot_mj=200.0, net_electric_mw=3000.0)
    _, diag3 = run(model, fwd3)
    assert diag3["lcoe"] == pytest.approx(15.4, abs=0.2)
    assert not coherence_violations(fwd3, diag3, "tier3")


def test_tier_stacks_are_coherent(model, base_cfg):
    """Every published rung must pass its own tier's coherence check. The
    records stack evaluated on the vendor's own 0.5 m chamber is a
    controlled comparison, not a published device, and sits a few percent
    over the wall flash bound there (the reverted recovery share dumps more
    conversion waste on the wall), which is one reason the records device
    moves to fat chambers."""
    for cfgs, tier in ((("best_case.yaml",), "tier2"),
                       (("best_case.yaml", "tier2.yaml"), "tier2"),
                       (TIER_CONFIGS, "tier3")):
        f = dict(base_cfg["forward"])
        for c in cfgs:
            apply_records(f, c)
        _, diag = run(model, f)
        violations = coherence_violations(f, diag, tier)
        if cfgs == ("best_case.yaml",):
            assert violations and all("flash" in v for v in violations), violations
        else:
            assert not violations, (cfgs, tier)


def test_tritium_in_pulse_burn_anchors():
    """The dhe3_f_T = 0 audit: reactor-class corner (1e23 m^-3, 50 keV,
    1 ms) burns about 4% of bred tritium in-pulse; the Trenta-class
    sub-millisecond corner stays under 1%."""
    from tritium_burn import burn_probability

    assert burn_probability(1e23, 50.0, 1e-3) == pytest.approx(0.043, abs=0.005)
    assert burn_probability(3e22, 50.0, 3e-4) < 0.01


def test_burnup_closure_contradicts_store_and_decay():
    """The concept YAML's burn_fraction 0.15 implies 78-93% in-pulse T burn
    (thermalized-triton limit); store-and-decay (f_T under 1%) requires
    per-shot burnup below about 7e-4."""
    from tritium_burn import f_t_from_burnup

    assert f_t_from_burnup(0.15, 70.0) == pytest.approx(0.78, abs=0.02)
    assert f_t_from_burnup(0.15, 20.0) == pytest.approx(0.93, abs=0.02)
    assert f_t_from_burnup(7.3e-4, 70.0) < 0.011


def test_chi_from_xs_equilibrium_anchors():
    """FRC average-beta theorem pins the driver-thermalization share:
    x_s 0.5/0.7/0.85 -> chi 0.30/0.52/0.71."""
    from reconciliation import chi_from_xs

    assert chi_from_xs(0.5) == pytest.approx(0.304, abs=0.01)
    assert chi_from_xs(0.7) == pytest.approx(0.52, abs=0.01)
    assert chi_from_xs(0.85) == pytest.approx(0.71, abs=0.01)


def test_tritium_burn_floor_constraint(model, base_cfg):
    """dhe3_f_T = 0 at high per-pulse burnup must be flagged (coherent only
    under prompt triton loss); at the patent basis it passes."""
    fwd = dict(base_cfg["forward"])
    for c in TIER_CONFIGS:
        apply_records(fwd, c)
    fwd.update(yield_per_shot_mj=500.0, chamber_length=30.0, plasma_t=1.5,
               r_bore=1.6, fw_class="panel")
    _, diag = run(model, fwd)
    assert not coherence_violations(fwd, diag, "tier3")
    v = "; ".join(coherence_violations(dict(fwd, burn_fraction=0.15), diag, "tier3"))
    assert "in-pulse burn floor" in v
