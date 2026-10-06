"""Closure, config-integrity, and ladder-regression tests.

Regression values are pinned at costingfe 44434d9 with the plant
environment of docs/ledger.md: cost of capital 7/7/5/3% real and book
life 60/60/80/80 yr stepping with the tiers, availability derived from the
replacement schedule, the compression field and the driver bank scanned
by grade (the basis at records, the bank doubled at extrapolations, the
field to 50 T and the bank to 200 MJ at speculation). If costingfe moves and a number shifts, the ladder
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
    breakeven_time_at_point_s,
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
    # the vendor configuration on the design basis (7% real, 60 yr, derived
    # availability)
    diag = _ladder_lcoe(model, base_cfg)
    assert diag["lcoe"] == pytest.approx(105.9, abs=0.2)
    assert diag["n_mod"] == 20
    _, diag3 = run(model, dict(base_cfg["forward"], net_electric_mw=3000.0))
    assert diag3["lcoe"] == pytest.approx(102.1, abs=0.2)


def test_records_device(model, base_cfg):
    """The citable-records device: design-optimized under the record
    stack alone at the basis field and bank (no record exists above
    either), the deuterium-rich end of the mix grid (dd_frac 0.85 with
    its tritium plant, in fat panel-wall chambers) fired under its own
    1.01 s burn's duty bound, 25 modules at 0.985 Hz, a hair under the 1
    Hz grant; the 3 GWe park is the same module tripled."""
    _, fwd = device_fwd("records", 1000.0)
    _, diag = run(model, fwd)
    assert (diag["b_center_t"], diag["e_driver_mj"]) == (22.0, 50.0)
    assert diag["lcoe"] == pytest.approx(112.1, abs=0.2)
    assert (diag["n_mod"], round(diag["f_rep_hz"], 2)) == (25, 0.99)
    assert 0.99 < diag["tau_burn_implied_s"] * diag["f_rep_hz"] <= 1.0
    assert not coherence_violations(fwd, diag, "tier2")
    assert diag["tritium_adder_musd"] > 0
    _, diag3 = run(model, dict(fwd, net_electric_mw=3000.0))
    assert diag3["lcoe"] == pytest.approx(108.2, abs=0.2)
    assert diag3["n_mod"] == 75
    assert not coherence_violations(dict(fwd, net_electric_mw=3000.0), diag3, "tier2")


def test_tier1_rung(model, base_cfg):
    diag = _ladder_lcoe(model, base_cfg, "best_case.yaml")
    assert diag["lcoe"] == pytest.approx(153.2, abs=0.2)


def test_tier2_rung(model, base_cfg):
    diag = _ladder_lcoe(model, base_cfg, "best_case.yaml", "tier2.yaml")
    assert diag["lcoe"] == pytest.approx(32.4, abs=0.2)
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
    """The extrapolation device holds the basis field (the coil bound,
    constraint 9) and takes the doubled bank, 256 MJ shots at the
    design-basis gain, at dd_frac 0.80 with its tritium plant in 6
    modules of 10 m x 1.5 m at 1.56 Hz, the fewest modules whose rate
    fits its 0.62 s burn, under the 3 Hz grant; the 3 GWe park is the
    same module tripled. Fired at the grant instead, the same machine
    overruns its period (and the panel wall's steady flux) in 4 modules;
    on the sourced 50 MJ bank it needs 12 modules of 10 m x 0.75 m and
    reads 1.0 $/MWh more."""
    from study import GAIN_BASIS

    _, fwd = device_fwd("extrap", 1000.0)
    _, diag = run(model, fwd)
    assert fwd["dhe3_dd_frac"] == pytest.approx(0.8)
    assert (diag["b_center_t"], diag["e_driver_mj"]) == (22.0, 100.0)
    assert diag["yield_per_shot_mj"] == pytest.approx(GAIN_BASIS * 100.0)
    assert diag["lcoe"] == pytest.approx(29.1, abs=0.2)
    assert (diag["n_mod"], round(diag["f_rep_hz"], 2)) == (6, 1.56)
    assert diag["tau_burn_implied_s"] == pytest.approx(0.62, abs=0.01)
    assert not coherence_violations(fwd, diag, "tier2")
    assert diag["tritium_adder_musd"] > 0
    _, fwd3 = device_fwd("extrap", 3000.0)
    _, diag3 = run(model, fwd3)
    assert diag3["lcoe"] == pytest.approx(26.2, abs=0.2)
    assert diag3["n_mod"] == 18
    assert not coherence_violations(fwd3, diag3, "tier2")
    at_grant = dict(fwd, max_f_rep=3.0)
    _, dg = run(model, at_grant)
    v = "; ".join(coherence_violations(at_grant, dg, "tier2"))
    assert dg["n_mod"] == 4 and "duty" in v and "wall flux" in v
    polaris = dict(fwd, e_driver_mj=50.0, yield_per_shot_mj=128.1,
                   plasma_t=0.75, r_bore=0.85)
    _, dp = run(model, polaris)
    assert dp["lcoe"] == pytest.approx(30.1, abs=0.2)
    assert dp["n_mod"] == 12
    assert dp["tau_burn_implied_s"] == pytest.approx(diag["tau_burn_implied_s"], rel=1e-6)


def test_tier3_coherent_minimum(model, base_cfg):
    """The speculation device: 50 T and a 100 MJ bank, 600 MJ shots (gain
    6) at dd_frac 0.85 with a tritium plant, a single 30 m x 1.5 m
    panel-wall module at 2.94 Hz carrying 1.77 GW of fusion power, where
    the wall's steady flux binds (97% of the panel limit) before the 0.28
    s burn's duty does (0.83); the 3 GWe park is the same module tripled.
    The coil cycles to 995 MPa, past the basis coil, which constraint 9
    admits at this grade and labels. The 30 m chamber's adiabatic bound
    (0.994) sits above the tier's f_pdv claim (0.947), so the claim
    stands and the composite sits at the speculation cap."""
    from study import COIL_PRESSURE_BASIS_MPA, Q_LIM

    _, fwd = device_fwd("spec", 1000.0)
    _, diag = run(model, fwd)
    assert fwd["dhe3_dd_frac"] == pytest.approx(0.85)
    assert (diag["b_center_t"], diag["e_driver_mj"], diag["yield_per_shot_mj"]) == (50.0, 100.0, 600.0)
    assert diag["lcoe"] == pytest.approx(10.2, abs=0.2)
    assert (diag["n_mod"], round(diag["f_rep_hz"], 2)) == (1, 2.94)
    assert diag["p_fus_module_mw"] == pytest.approx(1766, rel=0.01)
    assert diag["tau_burn_implied_s"] == pytest.approx(0.28, abs=0.01)
    assert 0.8 < diag["tau_burn_implied_s"] * diag["f_rep_hz"] < 0.85
    assert 0.95 < diag["q_wall_mw_m2"] / Q_LIM["panel"] < 1.0
    assert not coherence_violations(fwd, diag, "tier3")
    assert diag["coil_pressure_mpa"] == pytest.approx(995, abs=1)
    assert diag["coil_pressure_mpa"] > COIL_PRESSURE_BASIS_MPA
    assert diag["e_flash_mj_m2"] < E_FLASH_MELT_MJ_M2
    assert diag["tritium_adder_musd"] > 0
    assert diag["f_pdv_eff"] == pytest.approx(0.947) and diag["f_pdv_cap"] > 0.947
    _, fwd3 = device_fwd("spec", 3000.0)
    _, diag3 = run(model, fwd3)
    assert diag3["lcoe"] == pytest.approx(7.9, abs=0.2)
    assert diag3["n_mod"] == 3
    assert not coherence_violations(fwd3, diag3, "tier3")
    # the same design is excluded at the extrapolation grade by the coil
    # bound alone
    assert [v for v in coherence_violations(fwd, diag, "tier2") if "coil" in v]


def test_the_field_moves_the_burn_point_with_it(model):
    """At beta = 1 and the patent's ion temperature the density scales as
    B^2: the breakeven time falls as B^-2, the per-pulse burnup rises as
    B^2 (so the He-3 recycle loop wastes less), the compressed flux volume
    shrinks as B^-2 (so the same chamber caps f_pdv higher), the coil
    pressure rises as B^2, and the model's own coil account, which prices
    conductor along the shrinking adiabat, falls with the field rather
    than rising: the structure the pressure needs is not in it."""
    from study import (breakeven_time_at_point_s, burnup_at_field,
                       coil_pressure_mpa, compressed_volume_m3)

    _, fwd = device_fwd("extrap", 1000.0)
    base = dict(fwd)
    high = dict(fwd, b_center=44.0)
    assert breakeven_time_at_point_s(high) < breakeven_time_at_point_s(base) / 3.5
    assert burnup_at_field(high)[0] == pytest.approx(4 * burnup_at_field(base)[0])
    assert burnup_at_field(high)[1] == pytest.approx(4 * burnup_at_field(base)[1])
    assert compressed_volume_m3(high) == pytest.approx(compressed_volume_m3(base) / 4)
    assert coil_pressure_mpa(44.0) == pytest.approx(4 * coil_pressure_mpa(22.0))
    r_b, d_b = run(model, base)
    r_h, d_h = run(model, high)
    assert d_h["tau_burn_implied_s"] == pytest.approx(d_b["tau_burn_implied_s"] / 4, rel=0.15)
    assert d_h["f_pdv_cap"] > d_b["f_pdv_cap"]
    assert float(r_h.cas22_detail["C220103"]) < float(r_b.cas22_detail["C220103"])
    assert float(r_h.costs.cas80) < float(r_b.costs.cas80)
    # a point that carries its own burnup keeps it
    assert burnup_at_field(dict(high, burn_fraction=1e-3, burn_fraction_he3=3e-3)) == (1e-3, 3e-3)


def test_the_bank_scales_the_driver_accounts_and_the_flux_volume(model):
    """A doubled bank at the design-basis gain doubles the shot, the
    driver and conversion-electronics accounts and the compressed flux
    volume (so the same chamber caps f_pdv lower and the flash energy
    doubles), leaves the implied burn unchanged, and halves the module
    count at the same rate."""
    from study import GAIN_BASIS, compressed_volume_m3

    _, fwd = device_fwd("extrap", 1000.0)
    one = dict(fwd, e_driver_mj=50.0, yield_per_shot_mj=GAIN_BASIS * 50.0)
    two = dict(fwd, e_driver_mj=100.0, yield_per_shot_mj=GAIN_BASIS * 100.0)
    r1, d1 = run(model, one)
    r2, d2 = run(model, two)
    assert compressed_volume_m3(two) == pytest.approx(2 * compressed_volume_m3(one))
    assert d2["f_pdv_cap"] < d1["f_pdv_cap"]
    assert float(r2.cas22_detail["C220107"]) == pytest.approx(2 * float(r1.cas22_detail["C220107"]), rel=1e-6)
    assert float(r2.cas22_detail["C220109"]) == pytest.approx(2 * float(r1.cas22_detail["C220109"]), rel=0.02)
    assert d2["e_flash_mj_m2"] == pytest.approx(2 * d1["e_flash_mj_m2"], rel=0.02)
    assert d2["tau_burn_implied_s"] == pytest.approx(d1["tau_burn_implied_s"], rel=1e-9)
    assert d2["n_mod"] == d1["n_mod"] // 2


def test_the_deuterium_rich_end_fits_its_period_in_more_modules(model):
    """The deuterium-rich end of the mix grid (dd_frac 0.85) breeds more
    He-3 than it burns. At the records and speculation grades it is the
    device itself; at extrapolations, fired at the 3 Hz grant its
    power-sparse burn overruns the period, and fired slower in one more
    module it is coherent and 0.5 $/MWh behind the device's 0.80 mix."""
    from study import D_RICH_DEVICES, DEVICES

    assert D_RICH_DEVICES["records"] is DEVICES["records"]
    assert D_RICH_DEVICES["spec"] is DEVICES["spec"]
    _, cf = device_fwd("extrap", 1000.0, D_RICH_DEVICES)
    _, dcf = run(model, cf)
    assert not coherence_violations(cf, dcf, "tier2")
    assert dcf["tau_burn_implied_s"] * dcf["f_rep_hz"] <= 1.0
    assert dcf["lcoe"] == pytest.approx(29.6, abs=0.2)
    assert dcf["n_mod"] == 7
    _, dev = device_fwd("extrap", 1000.0)
    _, ddev = run(model, dev)
    assert ddev["lcoe"] <= dcf["lcoe"] < ddev["lcoe"] + 0.8
    at_grant = dict(cf, max_f_rep=3.0)
    _, dg = run(model, at_grant)
    assert any(x.startswith("duty") for x in coherence_violations(at_grant, dg, "tier2"))
    assert dg["n_mod"] < dcf["n_mod"] and dg["lcoe"] < dcf["lcoe"]
    _, cf3 = device_fwd("extrap", 3000.0, D_RICH_DEVICES)
    _, dcf3 = run(model, cf3)
    assert dcf3["lcoe"] == pytest.approx(26.3, abs=0.2)
    assert not coherence_violations(cf3, dcf3, "tier2")


def test_every_optimized_device_fires_at_or_below_its_grant_and_its_duty_bound(model):
    """The rate the search chose: each optimized device's ceiling is the
    lower of its grade's grant and the duty-bound rate of its own burn
    (rounded down to the thousandth), its solved rate sits under the
    ceiling, its burn fits the period, and it is built in the fewest
    modules whose rate fits: one module fewer would have to fire above
    the ceiling. The records and extrapolation devices fire at 96 to
    100% of the duty bound; the speculation device's single module fires
    at the rate 1 GWe needs, 83% of the bound, with the wall binding
    instead. Where the grant sits above the ceiling, raising the ceiling
    to the grant either overruns the period (extrapolations) or changes
    nothing (the single-module speculation device, whose rate the plant
    power sets)."""
    from study import DEVICES, duty_bound_rate_hz, e_del_mj

    grants = {"records": 1.0, "extrap": 3.0, "spec": 10.0}
    for name, grant in grants.items():
        _, fwd = device_fwd(name, 1000.0)
        bound = duty_bound_rate_hz(fwd, e_del_mj(fwd))
        ceiling = DEVICES[name]["overrides"]["max_f_rep"]
        assert ceiling == pytest.approx(min(grant, bound), abs=0.001), name
        _, d = run(model, fwd)
        assert d["f_rep_hz"] <= ceiling * (1 + 1e-9), name
        duty = d["tau_burn_implied_s"] * d["f_rep_hz"]
        assert duty <= 1.0, (name, duty)
        if name == "spec":
            assert d["n_mod"] == 1 and 0.8 < duty < 0.85
        else:
            assert 0.95 <= duty, (name, duty)
            assert d["f_rep_hz"] * d["n_mod"] / (d["n_mod"] - 1) > ceiling, name
        if ceiling < grant:
            _, dg = run(model, dict(fwd, max_f_rep=grant))
            if dg["n_mod"] == d["n_mod"]:
                assert dg["f_rep_hz"] == pytest.approx(d["f_rep_hz"], rel=1e-6), name
            else:
                assert dg["tau_burn_implied_s"] * dg["f_rep_hz"] > 1.0, name


def test_tier_stacks_are_coherent(model, base_cfg):
    """The records stack evaluated on the vendor's own 0.61 m chamber (a
    controlled comparison, not a published device) passes its tier's
    coherence check; the tier-2 and tier-3 stacks on that chamber carry
    the D-rich mix of tier2.yaml, whose 0.68 s burn overruns the period at
    their rep rates, so constraint 8 flags them and nothing else does."""
    for cfgs, tier, duty_only in ((("best_case.yaml",), "tier2", False),
                                  (("best_case.yaml", "tier2.yaml"), "tier2", True),
                                  (TIER_CONFIGS, "tier3", True)):
        f = dict(base_cfg["forward"])
        for c in cfgs:
            apply_records(f, c)
        _, diag = run(model, f)
        violations = coherence_violations(f, diag, tier)
        if duty_only:
            assert violations and all(v.startswith("duty") for v in violations), (cfgs, tier)
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
    under prompt triton loss); at the patent basis it passes, and at the
    speculation device's 50 T, where the burnup is 5.2x the basis, the
    floor (0.008) sits just inside the 1% tolerance."""
    from study import burnup_at_field, f_t_from_burnup

    _, fwd = device_fwd("spec", 1000.0)
    _, diag = run(model, fwd)
    assert not coherence_violations(fwd, diag, "tier3")
    bf, _ = burnup_at_field(fwd)
    assert bf == pytest.approx(1.2e-4 * (50.0 / 22.0) ** 2)
    assert 0.005 < f_t_from_burnup(bf, 70.0) < 0.01
    v = "; ".join(coherence_violations(dict(fwd, burn_fraction=0.15), diag, "tier3"))
    assert "in-pulse burn floor" in v
    # at 55 T the floor crosses the tolerance and the zero is flagged
    v = "; ".join(coherence_violations(dict(fwd, b_center=55.0), diag, "tier3"))
    assert "in-pulse burn floor" in v


def test_coil_bound_holds_the_field_at_the_basis_below_speculation(model):
    """Constraint 9: a point above the 22 T basis is excluded at the
    records and extrapolation grades by the coil's magnetic pressure (the
    basis coil already sits at or above the copper-alloy gigacycle band),
    and admitted at speculation, where every such point reports the
    pressure it rests on."""
    from study import COIL_PRESSURE_BASIS_MPA, COIL_PRESSURE_CAP_MPA, coil_pressure_mpa

    assert COIL_PRESSURE_BASIS_MPA == pytest.approx(192.6, abs=0.5)
    assert COIL_PRESSURE_CAP_MPA["tier2"] == COIL_PRESSURE_BASIS_MPA
    assert COIL_PRESSURE_CAP_MPA["tier3"] == float("inf")
    assert coil_pressure_mpa(50.0) == pytest.approx(994.7, abs=1)
    _, fwd = device_fwd("extrap", 1000.0)
    _, diag = run(model, fwd)
    assert not [v for v in coherence_violations(fwd, diag, "tier2") if "coil" in v]
    high = dict(fwd, b_center=30.0)
    _, dh = run(model, high)
    assert [v for v in coherence_violations(high, dh, "tier2") if "coil" in v]
    assert not [v for v in coherence_violations(high, dh, "tier3") if "coil" in v]
    assert dh["coil_pressure_mpa"] == pytest.approx(coil_pressure_mpa(30.0))


# --- device definitions ------------------------------------------------------

def test_device_fwd_matches_the_pinned_definitions(base_cfg):
    """study.DEVICES is the single source of the four devices; each
    optimized device carries its burn mix on the bremsstrahlung floor and
    the rate ceiling the search chose; the 3 GWe parks are the same
    module tripled, so only the plant power changes."""
    from study import DEVICES, DEVICE_ORDER, device_fwd

    from study import GAIN_BASIS, field_t, e_del_mj

    assert [name for name, _ in DEVICE_ORDER] == ["records", "helion", "extrap", "spec"]
    geometry = {"records": (10.0, 0.75), "extrap": (10.0, 1.5), "spec": (30.0, 1.5)}
    for name, dd in (("records", 0.85), ("extrap", 0.8), ("spec", 0.85)):
        _, f = device_fwd(name, 1000.0)
        assert f["dhe3_dd_frac"] == pytest.approx(dd)
        assert f["f_rad"] == pytest.approx(f_rad_floor(dd))
        assert f["max_f_rep"] == DEVICES[name]["overrides"]["max_f_rep"]
        assert (f["chamber_length"], f["plasma_t"]) == geometry[name]
        assert f["r_bore"] == pytest.approx(f["plasma_t"] + 0.10)
        assert f["fw_class"] == "panel"
    cfg, fwd = device_fwd("extrap", 1000.0)
    assert cfg == base_cfg
    assert fwd["net_electric_mw"] == 1000.0
    _, helion = device_fwd("helion", 1000.0)
    assert "max_f_rep" not in helion  # Helion's configuration fires at its 1 Hz grant
    assert "b_center" not in helion and "e_driver_mj" not in helion  # the basis
    for name in ("records", "extrap", "spec"):
        _, f1 = device_fwd(name, 1000.0)
        _, f3 = device_fwd(name, 3000.0)
        assert f3["net_electric_mw"] == 3000.0
        assert {k: v for k, v in f1.items() if k != "net_electric_mw"} == \
            {k: v for k, v in f3.items() if k != "net_electric_mw"}
    # the field and the bank, graded: the basis at records, the bank
    # doubled at the design-basis gain at extrapolations, both scaled at
    # speculation
    _, f = device_fwd("records", 1000.0)
    assert (field_t(f), e_del_mj(f), f["yield_per_shot_mj"]) == (22.0, 50.0, 128.1)
    _, f = device_fwd("extrap", 1000.0)
    assert (field_t(f), e_del_mj(f)) == (22.0, 100.0)
    assert f["yield_per_shot_mj"] == pytest.approx(GAIN_BASIS * 100.0)
    _, f = device_fwd("spec", 1000.0)
    assert (field_t(f), e_del_mj(f), f["yield_per_shot_mj"]) == (50.0, 100.0, 600.0)
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
    """Longer capacitor life stretches the bank-swap interval: both
    cheaper devices sit above the records device."""
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
    60/60/80/80 yr and construction time 5/5/3.25/2.5 yr are engineering
    entries; nothing else in the environment moves between rungs (the
    indirect fraction is the nominal 0.20 everywhere; its effective value
    follows the build through CAS30 = f x CAS20 x T/6)."""
    from study import PLANT_SIZES_MWE

    expect = {"records": (0.07, 60.0, 5.0), "helion": (0.07, 60.0, 5.0),
              "extrap": (0.05, 80.0, 3.25), "spec": (0.03, 80.0, 2.5)}
    held = ("inflation_rate", "indirect_fraction",
            "availability_steady_state", "outage_days_routine", "routine_cycle_yr",
            "outage_days_bank_swap", "outage_days_wall")
    _, base = device_fwd("helion", PLANT_SIZES_MWE[0])
    for name, (rate, life, build) in expect.items():
        _, fwd = device_fwd(name, PLANT_SIZES_MWE[0])
        assert (fwd["interest_rate"], fwd["lifetime_yr"], fwd["construction_time_yr"]) == (rate, life, build), name
        assert fwd["indirect_fraction"] == 0.20, name
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


def test_breakeven_time_follows_the_point_s_own_burn_mix():
    """The plasma's breakeven time is a property of what it burns, not of
    the patent's mix: a D-rich plasma is less power-dense and takes longer,
    a He-3-rich one takes less. The composition counted is the one the
    model's fuel accounting implies, recycled bred He-3 included."""
    tau_patent = breakeven_time_at_point_s(
        dict(dhe3_dd_frac=0.488, burn_fraction_he3=4.1e-4, fuel_recovery=0.9999))
    tau_drich = breakeven_time_at_point_s(
        dict(dhe3_dd_frac=0.85, burn_fraction_he3=4.1e-4, fuel_recovery=0.9999))
    tau_he3rich = breakeven_time_at_point_s(
        dict(dhe3_dd_frac=0.314, burn_fraction_he3=4.1e-4, fuel_recovery=0.9999))
    assert tau_he3rich < tau_patent < tau_drich
    assert tau_drich == pytest.approx(0.138, abs=0.005)
    assert tau_patent == pytest.approx(0.065, abs=0.005)


def test_duty_cycle_constraint_catches_a_burn_longer_than_its_period():
    """Constraint 8: a shot's implied burn must fit inside the pulse
    period, since the next shot cannot start while the last one is still
    burning. Flagged from the point's own implied burn and rep rate."""
    fwd = dict(dhe3_dd_frac=0.85, f_rad=0.28, eta_dec=0.90, f_pdv=0.80,
               dhe3_f_T=0.0, burn_fraction=1.2e-4, fw_class="panel")
    ok = dict(q_wall_mw_m2=0.5, e_flash_mj_m2=0.5, f_pdv_eff=0.80,
              tau_burn_implied_s=0.40, f_rep_hz=1.0)
    bad = dict(ok, tau_burn_implied_s=1.65, f_rep_hz=3.53)
    assert not [v for v in coherence_violations(fwd, ok, "tier2") if "duty" in v]
    v = "; ".join(coherence_violations(fwd, bad, "tier2"))
    assert "duty" in v and "5.8" in v
