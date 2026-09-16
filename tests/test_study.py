"""Closure, config-integrity, and ladder-regression tests.

Regression values are pinned at costingfe 44434d9 with the plant
environment of docs/ledger.md: cost of capital 7/7/5/3% real and book
life 30/30/80/80 yr stepping with the tiers, availability derived from the
replacement schedule. If costingfe moves and a number shifts, the ladder
in docs/ledger.md must be re-based in the same change that updates the pin
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
    device_fwd,
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
    # adiabatic bound clamps it to the cap at the concept chamber before
    # the run, and the composite at that cap is still over 0.80, which the
    # composite-cap check reports
    assert diag["f_pdv_cap"] < 0.95
    assert diag["f_pdv_eff"] == pytest.approx(diag["f_pdv_cap"], rel=1e-6)
    assert "composite cap" in v


def test_recovery_share_is_not_a_study_parameter(model, base_cfg):
    """The radial-only share was dropped: f_pdv is capped by the adiabatic
    bound alone, and the old key is rejected like any unknown parameter."""
    fwd = dict(base_cfg["forward"])
    with pytest.raises(Exception):
        run(model, dict(fwd, f_pdv_radial_share=0.8))


# --- ladder regression (costingfe 44434d9) ---------------------------------

def _ladder_lcoe(model, base_cfg, *cfgs):
    fwd = dict(base_cfg["forward"])
    for c in cfgs:
        apply_records(fwd, c)
    _, diag = run(model, fwd)
    return diag


def test_helion_requirements_device(model, base_cfg):
    # the vendor configuration on the design basis (7% real, 30 yr, derived
    # availability)
    diag = _ladder_lcoe(model, base_cfg)
    assert diag["lcoe"] == pytest.approx(103.9, abs=0.2)
    assert diag["n_mod"] == 20
    _, diag3 = run(model, dict(base_cfg["forward"], net_electric_mw=3000.0))
    assert diag3["lcoe"] == pytest.approx(100.2, abs=0.2)


def test_records_device(model, base_cfg):
    """The citable-records device: design-optimized under the record
    stack alone (the optimum is already the D-rich mix with its
    tritium plant, in fat panel-wall chambers)."""
    _, fwd = device_fwd("records", 1000.0)
    _, diag = run(model, fwd)
    assert diag["lcoe"] == pytest.approx(110.4, abs=0.2)
    assert not coherence_violations(fwd, diag, "tier2")
    _, diag3 = run(model, dict(fwd, net_electric_mw=3000.0))
    assert diag3["lcoe"] == pytest.approx(106.1, abs=0.2)


def test_tier1_rung(model, base_cfg):
    diag = _ladder_lcoe(model, base_cfg, "best_case.yaml")
    assert diag["lcoe"] == pytest.approx(153.1, abs=0.2)


def test_tier2_rung(model, base_cfg):
    diag = _ladder_lcoe(model, base_cfg, "best_case.yaml", "tier2.yaml")
    assert diag["lcoe"] == pytest.approx(31.5, abs=0.2)
    # D-rich mix carries its plant; the adder is unit-priced
    # (50 M$ + 0.657 M$/MW of plant neutron power), so the rung's value is a
    # consequence of its throughput, not an identity
    assert diag["tritium_adder_musd"] == pytest.approx(188.7, abs=1.0)


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
    assert diag["lcoe"] == pytest.approx(12.0, abs=0.2)


def test_tier2_coherent_minimum(model, base_cfg):
    _, fwd = device_fwd("extrap", 1000.0)
    _, diag = run(model, fwd)
    assert diag["lcoe"] == pytest.approx(26.1, abs=0.2)
    assert not coherence_violations(fwd, diag, "tier2")
    _, diag3 = run(model, dict(fwd, net_electric_mw=3000.0))
    assert diag3["lcoe"] == pytest.approx(23.0, abs=0.2)


def test_tier3_coherent_minimum(model, base_cfg):
    _, fwd = device_fwd("spec", 1000.0)
    _, diag = run(model, fwd)
    assert diag["lcoe"] == pytest.approx(10.6, abs=0.2)
    assert not coherence_violations(fwd, diag, "tier3")
    assert diag["e_flash_mj_m2"] < E_FLASH_MELT_MJ_M2
    # the 3 GWe park uses the 200 MJ design: larger shots trip the wall
    # audit once the integer module count snaps down
    _, fwd3 = device_fwd("spec", 3000.0)
    _, diag3 = run(model, fwd3)
    assert diag3["lcoe"] == pytest.approx(8.4, abs=0.2)
    assert not coherence_violations(fwd3, diag3, "tier3")


def test_tier_stacks_are_coherent(model, base_cfg):
    """Every published rung, and the records stack evaluated on the vendor's
    own 0.61 m chamber (a controlled comparison, not a published device),
    must pass its own tier's coherence check."""
    for cfgs, tier in ((("best_case.yaml",), "tier2"),
                       (("best_case.yaml", "tier2.yaml"), "tier2"),
                       (TIER_CONFIGS, "tier3")):
        f = dict(base_cfg["forward"])
        for c in cfgs:
            apply_records(f, c)
        _, diag = run(model, f)
        violations = coherence_violations(f, diag, tier)
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


def test_in_pulse_burn_vs_dwell_spans_the_stated_pulse_and_the_shot():
    """The closure against burn time at the patent point (0.75e22 m^-3,
    70 keV): under 1% tritium burn across the vendor's stated pulse, 28-38%
    over the patent's own 0.103-0.157 s confinement, and above half at the
    burn the design-basis shot implies under constraint 7."""
    import numpy as np
    from study import N_D_PATENT_M3, VENDOR_PULSE_S
    from tritium_burn import PATENT_CONFINEMENT_S, in_pulse_burn_vs_dwell
    from yield_bound import bound_table

    _, f_t = in_pulse_burn_vs_dwell(np.array([1e-4, VENDOR_PULSE_S]), N_D_PATENT_M3, 70.0)
    assert f_t.max() < 0.01
    f_d, f_t = in_pulse_burn_vs_dwell(np.array(PATENT_CONFINEMENT_S), N_D_PATENT_M3, 70.0)
    assert f_d == pytest.approx([0.025, 0.038], abs=0.002)
    assert f_t == pytest.approx([0.28, 0.38], abs=0.02)
    shot = min(r["tau_burn_s"] for r in bound_table() if r["device"] == "helion")
    _, f_t = in_pulse_burn_vs_dwell(shot, N_D_PATENT_M3, 70.0)
    assert f_t > 0.5


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
    _, fwd = device_fwd("spec", 1000.0)
    _, diag = run(model, fwd)
    assert not coherence_violations(fwd, diag, "tier3")
    v = "; ".join(coherence_violations(dict(fwd, burn_fraction=0.15), diag, "tier3"))
    assert "in-pulse burn floor" in v


# --- device definitions ------------------------------------------------------

def test_device_fwd_matches_the_pinned_definitions(base_cfg):
    """study.DEVICES is the single source of the four devices; the 3 GWe
    speculation park swaps to its 200 MJ design and nothing else changes."""
    from study import DEVICES, DEVICE_ORDER, device_fwd

    assert [name for name, _ in DEVICE_ORDER] == ["records", "helion", "extrap", "spec"]
    cfg, fwd = device_fwd("extrap", 1000.0)
    assert cfg == base_cfg
    assert fwd["net_electric_mw"] == 1000.0
    assert fwd["chamber_length"] == DEVICES["extrap"]["overrides"]["chamber_length"]
    _, f1 = device_fwd("spec", 1000.0)
    _, f3 = device_fwd("spec", 3000.0)
    assert f1["yield_per_shot_mj"] == 500.0
    assert f3["yield_per_shot_mj"] == 200.0
    assert f3["net_electric_mw"] == 3000.0
    skip = ("yield_per_shot_mj", "net_electric_mw")
    assert {k: v for k, v in f1.items() if k not in skip} == \
        {k: v for k, v in f3.items() if k not in skip}
    with pytest.raises(KeyError):
        device_fwd("spec", 2000.0)


# --- availability from the replacement schedule ----------------------------

def test_replacement_intervals_anchor():
    """A 1e8-shot bank at 1 Hz swaps every 3.24 calendar years at the 0.98
    steady state; a 0.20 MW/m^2 14-MeV-equivalent wall at 20 dpa lasts
    10.2 years (2 dpa per full-power year)."""
    from study import replacement_intervals_yr

    t_bank, t_wall = replacement_intervals_yr(1e8, 1.0, 0.20, 20.0, 0.98)
    assert t_bank == pytest.approx(1e8 / (3.1536e7 * 0.98), rel=1e-6)
    assert t_wall == pytest.approx(20.0 / 2.0 / 0.98, rel=1e-6)
    _, t_inf = replacement_intervals_yr(1e8, 1.0, 0.0, 20.0, 0.98)
    assert t_inf == float("inf")


def test_derived_availability_anchor():
    """Records-grade illustration: a 34-day routine outage every 2 yr, 34
    days per swap every 3.2357 yr and 84 days per changeout every 10.204 yr
    take 9.8% off the 0.98 steady state."""
    from study import derived_availability, outage_fractions

    f = outage_fractions(34.0, 2.0, 34.0, 3.2357, 84.0, 10.204)
    assert f["routine"] == pytest.approx(34 / 730, rel=1e-9)
    a = derived_availability(0.98, 34.0, 2.0, 34.0, 3.2357, 84.0, 10.204)
    assert a == pytest.approx(0.98 * (1 - sum(f.values())), rel=1e-9)
    assert a == pytest.approx(0.884, abs=0.001)
    assert derived_availability(0.98, 34.0, 2.0, 34.0, 3.2357, 84.0, float("inf")) > a


def test_run_derives_availability_and_pins_honored(model):
    _, fwd = device_fwd("helion", 1000.0)
    res, diag = run(model, fwd)
    assert 0.85 < diag["availability"] < 0.98
    assert float(res.params["availability"]) == pytest.approx(diag["availability"])
    assert diag["t_bank_yr"] > 0 and diag["t_wall_yr"] > diag["t_bank_yr"]
    assert diag["outage_routine"] + diag["outage_bank"] + diag["outage_wall"] == \
        pytest.approx(1 - diag["availability"] / fwd["availability_steady_state"], rel=1e-9)
    # the derivation is a fixed point: pinning the derived value reproduces
    # the run exactly (the probe's capital accounts do not see availability)
    _, diag2 = run(model, dict(fwd, availability=diag["availability"]))
    assert diag2["lcoe"] == pytest.approx(diag["lcoe"], rel=1e-9)
    assert diag2["tritium_adder_musd"] == pytest.approx(diag["tritium_adder_musd"], rel=1e-9)
    # an explicit pin is honored and no study-only key reaches the model
    _, diag3 = run(model, dict(fwd, availability=0.5))
    assert diag3["availability"] == 0.5
    assert "wall_dpa_tolerance" not in res.params


def test_availability_rises_up_the_ladder(model):
    """Longer capacitor life and higher rep rate stretch the bank-swap
    interval: both cheaper devices sit above the records device."""
    a = {}
    for name in ("records", "extrap", "spec"):
        _, fwd = device_fwd(name, 1000.0)
        _, d = run(model, fwd)
        a[name] = d["availability"]
    assert a["records"] < min(a["extrap"], a["spec"]) < 0.98


def test_missing_schedule_inputs_fail_loudly(model, base_cfg):
    fwd = dict(base_cfg["forward"])
    del fwd["outage_days_wall"]
    with pytest.raises(KeyError, match="outage_days_wall"):
        run(model, fwd)


def test_financing_and_book_life_ladder():
    """Cost of capital steps 7/7/5/3% real with the tiers; book life
    30/30/80/80 yr is an engineering entry; nothing else in the environment
    moves between rungs."""
    from study import PLANT_SIZES_MWE

    expect = {"records": (0.07, 30.0), "helion": (0.07, 30.0),
              "extrap": (0.05, 80.0), "spec": (0.03, 80.0)}
    held = ("inflation_rate", "construction_time_yr", "indirect_fraction",
            "availability_steady_state", "outage_days_routine", "routine_cycle_yr",
            "outage_days_bank_swap", "outage_days_wall")
    _, base = device_fwd("helion", PLANT_SIZES_MWE[0])
    for name, (rate, life) in expect.items():
        _, fwd = device_fwd(name, PLANT_SIZES_MWE[0])
        assert (fwd["interest_rate"], fwd["lifetime_yr"]) == (rate, life), name
        assert "availability" not in fwd, name
        for k in held:
            assert fwd[k] == base[k], (name, k)


def test_lcoe_segments_sum_to_the_lcoe(model):
    """Figure 1's three parts are an exact partition of the model's LCOE:
    overnight cost straight-line over the book life, the cost of money
    (CAS90 less that), and operating costs (CAS70 + CAS80)."""
    from study import lcoe_segments

    for name in ("helion", "spec"):
        _, fwd = device_fwd(name, 1000.0)
        res, diag = run(model, fwd)
        seg = lcoe_segments(res)
        assert seg["straight_line"] + seg["cost_of_money"] + seg["operating"] == \
            pytest.approx(diag["lcoe"], rel=1e-9), name
        assert seg["straight_line"] > 0 and seg["operating"] > 0
        # at any positive real rate the annuity exceeds straight-line recovery
        assert seg["cost_of_money"] > 0


# --- the decay store's He-3 return ------------------------------------------

def test_he3_purchase_fraction_falls_with_breeding_and_book_life():
    """The store returns 0.5 dd_frac He-3 per primary event as
    (1 - e^-t/17.8 yr) builds; purchases (1 - dd_frac per event) fall to
    zero once the return covers them. phi is the levelized fraction of the
    perpetual purchase that remains over the book life at the rung's rate."""
    from study import he3_purchase_fraction
    assert he3_purchase_fraction(0.0, 0.05, 80) == pytest.approx(1.0)
    d_rich = he3_purchase_fraction(0.85, 0.05, 80)
    assert 0.05 < d_rich < 0.30
    vendor = he3_purchase_fraction(0.488, 0.07, 30)
    assert 0.65 < vendor < 0.90
    assert he3_purchase_fraction(0.85, 0.07, 30) > d_rich
    assert he3_purchase_fraction(0.85, 0.05, 80) < he3_purchase_fraction(0.85, 0.05, 30)


def test_run_credits_the_decay_return_through_the_he3_price(model, base_cfg):
    from study import he3_purchase_fraction
    _, fwd = device_fwd("extrap", 1000.0)
    _, d = run(model, fwd)
    phi = he3_purchase_fraction(fwd["dhe3_dd_frac"], fwd["interest_rate"], fwd["lifetime_yr"])
    assert d["he3_purchase_fraction"] == pytest.approx(phi)
    _, free = run(model, dict(fwd, u_he3=0.0))
    _, perpetual = run(model, dict(fwd, he3_decay_return=False))
    assert free["lcoe"] < d["lcoe"] < perpetual["lcoe"]
    assert d["lcoe"] == pytest.approx(free["lcoe"] + phi * (perpetual["lcoe"] - free["lcoe"]), abs=0.05)
