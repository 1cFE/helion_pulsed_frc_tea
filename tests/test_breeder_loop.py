"""Two-machine fuel economy: dedicated pure-D breeder modules feeding lean
D-He3 power modules, with the breeder's capital, replacement, tritium plant
and electricity consumption inside the park (scripts/breeder_loop.py).

Regression values are pinned at costingfe 44434d9 on the plant environment
of docs/ledger.md, like tests/test_study.py.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from breeder_loop import (  # noqa: E402
    Q_DD_AVG_MEV,
    breeder_module,
    central_unit_cost,
    close_loop,
    device_at_breeder_price,
    device_fwd,
    he3_demand_kg_yr,
    per_module_costs,
    unit_cost_breakdown,
)
from study import build_model, f_rad_floor, run  # noqa: E402
from tritium_burn import SECONDS_PER_YEAR  # noqa: E402
from costingfe.layers.physics import E_N_DD, M_HE3_KG  # noqa: E402

MEV_J = 1.602e-13


@pytest.fixture(scope="module")
def helion():
    cfg, fwd = device_fwd("helion")
    model = build_model(cfg)
    res, _ = run(model, fwd)
    return model, fwd, res


@pytest.fixture(scope="module")
def extrap():
    cfg, fwd = device_fwd("extrap")
    model = build_model(cfg)
    res, _ = run(model, fwd)
    return model, fwd, res


def test_pure_d_fill_on_the_vendor_shot_is_a_net_consumer(helion):
    model, _, res = helion
    br = breeder_module(model, res, "extract")
    assert br["yield_mj"] < res.params["yield_per_shot_mj"]
    assert br["gain"] < 1.0
    assert br["p_net"] < 0.0


def test_extract_mode_yields_one_he3_per_dd_event_half_via_tritium(extrap):
    model, _, res = extrap
    br = breeder_module(model, res, "extract")
    assert br["he3_prompt_kg_yr"] == pytest.approx(br["t_prod_kg_yr"], rel=1e-9)
    events_s = br["p_fus"] * 1e6 / (Q_DD_AVG_MEV * MEV_J)
    eventual = events_s * res.params["availability"] * SECONDS_PER_YEAR * M_HE3_KG
    assert br["he3_prompt_kg_yr"] + br["t_prod_kg_yr"] == pytest.approx(eventual, rel=1e-6)


def test_burn_mode_trades_prompt_he3_for_yield(extrap):
    model, _, res = extrap
    ex = breeder_module(model, res, "extract")
    bu = breeder_module(model, res, "burn")
    assert bu["yield_mj"] > ex["yield_mj"]
    assert bu["he3_prompt_kg_yr"] < ex["he3_prompt_kg_yr"]
    assert bu["t_prod_kg_yr"] == pytest.approx(ex["t_prod_kg_yr"], rel=1e-9)


def test_decay_delay_raises_breeder_count_and_park_lcoe(extrap):
    model, fwd, res = extrap
    lean, _ = run(model, dict(fwd, dhe3_dd_frac=0.131, f_rad=f_rad_floor(0.131), u_he3=0.0))
    br = breeder_module(model, res, "extract")
    loop = close_loop(lean, br, per_module_costs(res), "rpe", res.params["interest_rate"])
    assert loop["pv"]["n_b"] > loop["eq"]["n_b"]
    assert loop["pv"]["lcoe"] > loop["eq"]["lcoe"]


def test_breeders_in_the_loop_cost_more_than_free_he3(extrap):
    model, fwd, res = extrap
    lean_fwd = dict(fwd, dhe3_dd_frac=0.131, f_rad=f_rad_floor(0.131), u_he3=0.0)
    lean, diag_lean = run(model, lean_fwd)
    br = breeder_module(model, res, "extract")
    loop = close_loop(lean, br, per_module_costs(res), "rpe", res.params["interest_rate"])
    assert loop["eq"]["lcoe"] > diag_lean["lcoe"]
    demand, _ = he3_demand_kg_yr(lean)
    assert loop["eq"]["n_b"] * (br["he3_prompt_kg_yr"] + br["t_prod_kg_yr"]) < demand


def test_two_machine_economy_pins(helion, extrap):
    """Park LCOE with breeders (extract mode, co-sited basis, equilibrium
    store) and the implied He-3 cost: the vendor grade prices its own He-3
    far above the 2 M$/kg baseline entry; the extrapolation grade below 1."""
    model, fwd, res = helion
    lean, _ = run(model, dict(fwd, dhe3_dd_frac=0.314, f_rad=f_rad_floor(0.314), u_he3=0.0))
    br = breeder_module(model, res, "extract")
    loop = close_loop(lean, br, per_module_costs(res), "rpe", res.params["interest_rate"])
    assert loop["eq"]["lcoe"] == pytest.approx(148.8, abs=0.2)
    assert loop["eq"]["he3_musd_kg"] == pytest.approx(5.28, abs=0.02)

    model, fwd, res = extrap
    lean, _ = run(model, dict(fwd, dhe3_dd_frac=0.131, f_rad=f_rad_floor(0.131), u_he3=0.0))
    br = breeder_module(model, res, "extract")
    loop = close_loop(lean, br, per_module_costs(res), "rpe", res.params["interest_rate"])
    assert loop["eq"]["lcoe"] == pytest.approx(28.4, abs=0.2)
    assert loop["eq"]["he3_musd_kg"] == pytest.approx(0.64, abs=0.02)


def test_neutron_power_per_he3_bred_is_the_dd_branch_identity(extrap):
    """Half a 2.45 MeV neutron per D-D event, one eventual He-3 per event:
    1.225 MeV of neutron per He-3 bred, wherever it is bred."""
    model, _, res = extrap
    br = breeder_module(model, res, "extract")
    out = br["he3_prompt_kg_yr"] + br["t_prod_kg_yr"]
    mw_per_kg_yr = (0.5 * E_N_DD * MEV_J * 1e-6) / (
        res.params["availability"] * SECONDS_PER_YEAR * M_HE3_KG)
    assert br["p_neutron"] / out == pytest.approx(mw_per_kg_yr, rel=1e-6)


def test_unit_cost_is_ownership_plus_tritium_plant_plus_power(helion, extrap):
    for fx, consumer in ((helion, True), (extrap, False)):
        model, _, res = fx
        br = breeder_module(model, res, "extract")
        parts = unit_cost_breakdown(br, per_module_costs(res), "rpe", 1.0, res.costs.lcoe)
        assert parts["total"] == pytest.approx(
            parts["ownership"] + parts["tritium_plant"] + parts["power"], rel=1e-9)
        assert bool(parts["power"] > 0.0) is consumer
        assert bool(parts["mwh_per_kg"] > 0.0) is consumer


def test_vendor_breeder_prices_he3_above_the_ledger_and_extrapolation_below(helion, extrap):
    for fx, above in ((helion, True), (extrap, False)):
        model, fwd, res = fx
        br = breeder_module(model, res, "extract")
        u, lcoe = device_at_breeder_price(model, fwd, res, br, per_module_costs(res), "rpe", 1.0)
        assert bool(u > res.params["u_he3"]) is above
        assert bool(lcoe > res.costs.lcoe) is above


def test_central_facility_unit_cost_falls_with_fleet_and_converges(extrap):
    model, fwd, res = extrap
    br = breeder_module(model, res, "extract")
    cm = per_module_costs(res)
    u_marginal = unit_cost_breakdown(br, cm, "rpe", 1.0, res.costs.lcoe)["total"]
    fleet = [central_unit_cost(model, fwd, res, br, cm, n, res.costs.lcoe)["unit"]
             for n in (1, 2, 5, 10, 20)]
    assert all(a >= b for a, b in zip(fleet, fleet[1:]))
    assert fleet[0] > 2.0 * u_marginal
    assert fleet[-1] < 1.15 * u_marginal


def test_unit_cost_pins(helion, extrap):
    """Co-sited breeder, equilibrium store, power at the device's own LCOE at
    the breeder price (fixed point)."""
    model, fwd, res = helion
    br = breeder_module(model, res, "extract")
    u, lcoe = device_at_breeder_price(model, fwd, res, br, per_module_costs(res), "rpe", 1.0)
    assert u == pytest.approx(6.53e6, rel=0.01)
    assert lcoe == pytest.approx(164.7, abs=0.3)
    model, fwd, res = extrap
    br = breeder_module(model, res, "extract")
    u, lcoe = device_at_breeder_price(model, fwd, res, br, per_module_costs(res), "rpe", 1.0)
    assert u == pytest.approx(6.55e5, rel=0.01)
    assert lcoe == pytest.approx(27.7, abs=0.2)
