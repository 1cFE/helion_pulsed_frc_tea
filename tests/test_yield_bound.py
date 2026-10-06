"""Constraints 7 and 8: the shot yield against the plasma energy and the
burn time, and the burn against the pulse period.

gain <= chi x burn time / breakeven time, with chi the plasma-thermal share
of the delivered driver energy (chi_from_xs) and the breakeven time the
plasma's energy density over its fusion power density at the burn point.
Pinned at costingfe 44434d9 on the patent burn point of config/baseline.yaml
(22 T, 70 keV, n_D 0.75e22 m^-3, He3/D 0.158); each device's own burn is
read at the mix it actually burns (study.breakeven_time_at_point_s).
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from study import (  # noqa: E402
    VENDOR_PULSE_S,
    X_S_REFERENCE,
    breakeven_time_s,
    build_model,
    chi_from_xs,
    device_fwd,
    implied_burn_s,
    load_config,
    run,
    yield_bound_mj,
)


@pytest.fixture(scope="module")
def model():
    return build_model(load_config("baseline.yaml"))


def test_breakeven_time_at_the_patent_point_with_thermalized_electrons():
    assert breakeven_time_s() == pytest.approx(0.086, abs=0.002)


def test_cold_electrons_shorten_breakeven_by_the_pressure_balance_factor():
    """At fixed field, electrons at a tenth of the ion temperature admit
    (1.158 + 1.316) / (1.158 + 0.1316) = 1.92x the ion density; fusion
    power goes as its square."""
    assert breakeven_time_s() / breakeven_time_s(te_over_ti=0.1) == pytest.approx(3.68, rel=0.01)


def test_vendor_pulse_returns_under_half_a_megajoule_from_the_bank():
    """A 1 ms burn from the 50 MJ bank across x_s 0.5 to 0.85."""
    assert VENDOR_PULSE_S == 1e-3
    assert yield_bound_mj(50.0, 0.5, VENDOR_PULSE_S) == pytest.approx(0.17, abs=0.02)
    assert yield_bound_mj(50.0, 0.85, VENDOR_PULSE_S) == pytest.approx(0.41, abs=0.03)


def test_design_basis_shot_implies_a_burn_of_a_third_to_three_quarters_of_a_second():
    assert implied_burn_s(128.1, 50.0, 0.85) == pytest.approx(0.31, abs=0.02)
    assert implied_burn_s(128.1, 50.0, 0.5) == pytest.approx(0.73, abs=0.03)


def test_speculation_shot_implies_a_burn_of_seconds():
    assert implied_burn_s(500.0, 50.0, 0.85) == pytest.approx(1.2, abs=0.1)
    assert implied_burn_s(500.0, 50.0, 0.5) == pytest.approx(2.9, abs=0.1)


def test_bound_and_implied_burn_are_inverses():
    tau = implied_burn_s(128.1, 50.0, 0.7)
    assert yield_bound_mj(50.0, 0.7, tau) == pytest.approx(128.1, rel=1e-9)


def test_run_reports_the_implied_burn_of_every_point(model):
    """The seventh constraint is applied by construction: every point carries
    the burn time its shot implies at the reference x_s (0.7, chi 0.52),
    at its own burn mix and at its own compression field. Helion's device
    holds He3/D 0.22 with the recycled bred He-3 counted (the patent's
    0.16 is the purchased share), so its 128 MJ shot reads 0.32 s against
    0.42 s at the patent mix; the speculation device's 600 MJ shot from
    its 100 MJ bank at 50 T and dd_frac 0.85 reads 0.28 s, the gain of 6
    at a breakeven time 5.2x shorter than the basis field's."""
    assert X_S_REFERENCE == 0.7
    assert chi_from_xs(X_S_REFERENCE) == pytest.approx(0.52, abs=0.01)
    _, fwd = device_fwd("helion", 1000.0)
    _, diag = run(model, fwd)
    assert diag["tau_burn_implied_s"] == pytest.approx(0.32, abs=0.02)
    assert implied_burn_s(128.1, 50.0, X_S_REFERENCE) == pytest.approx(0.42, abs=0.02)
    _, fwd = device_fwd("spec", 1000.0)
    _, diag = run(model, fwd)
    assert diag["tau_burn_implied_s"] == pytest.approx(0.28, abs=0.02)
    # the density scaling alone is B^2 (burnup pinned); at the point's own
    # burnup the field also lets more bred He-3 burn in the loop, so the
    # plasma it accounts for is richer and the ratio is larger still
    from study import breakeven_time_at_point_s
    pinned = dict(fwd, burn_fraction=1.2e-4, burn_fraction_he3=4.1e-4)
    assert breakeven_time_at_point_s(dict(pinned, b_center=22.0)) / breakeven_time_at_point_s(pinned) \
        == pytest.approx((50.0 / 22.0) ** 2, rel=1e-6)
    assert breakeven_time_at_point_s(dict(fwd, b_center=22.0)) / breakeven_time_at_point_s(fwd) \
        > (50.0 / 22.0) ** 2


def test_duty_table_reads_constraint_8_across_the_xs_span():
    """At the reference x_s every design fits its period: the records
    and extrapolation designs at 93 to 100% of it, since the search fires
    each in the fewest modules whose rate fits its burn, and the
    speculation device at 83%, its single module firing at the rate 1
    GWe needs with the wall binding first; at x_s 0.5 (chi 0.30) every
    optimized design would overrun, and at 0.85 all pass. The duty is the
    module's fusion power over the cap chi E_del / breakeven time, which
    the speculation device's field and bank raise to 2.1 GW. The records
    and speculation devices are the deuterium-rich end itself, so each is
    listed once."""
    from yield_bound import duty_table

    rows = duty_table()
    designs = {r["design"] for r in rows}
    assert designs == {"records", "helion", "extrap", "spec", "extrap (D-rich)"}
    for r in rows:
        assert r["duty"] == pytest.approx(r["p_fus_module_mw"] / r["p_fus_cap_mw"], rel=1e-9)
        if r["x_s"] == 0.7:
            assert r["duty"] <= 1.0
    ref = {r["design"]: r["duty"] for r in rows if r["x_s"] == 0.7}
    assert ref["helion"] == pytest.approx(0.32, abs=0.01)
    for d in ("records", "extrap", "extrap (D-rich)"):
        assert 0.93 <= ref[d] <= 1.0, d
    assert ref["spec"] == pytest.approx(0.83, abs=0.01)
    cap = {r["design"]: r["p_fus_cap_mw"] for r in rows if r["x_s"] == 0.7}
    assert cap["spec"] == pytest.approx(2140, rel=0.01)
    assert cap["extrap"] == pytest.approx(2 * cap["records"] * 206.3 / 126.1, rel=0.02)
    thin = {r["design"]: r["duty"] for r in rows if r["x_s"] == 0.5}
    fat = {r["design"]: r["duty"] for r in rows if r["x_s"] == 0.85}
    assert all(thin[d] > 1.0 for d in designs - {"helion"})
    assert thin["helion"] < 1.0
    assert all(fat[d] < 1.0 for d in designs)


def test_bound_table_lists_both_shots_across_the_xs_span():
    from yield_bound import bound_table
    rows = bound_table()
    shots = sorted({r["yield_mj"] for r in rows})
    assert shots == [128.1, 600.0]
    assert sorted({r["x_s"] for r in rows}) == [0.5, 0.7, 0.85]
    row = next(r for r in rows if r["yield_mj"] == 128.1 and r["x_s"] == 0.85)
    assert row["b_center_t"] == 22.0
    assert row["tau_burn_s"] == pytest.approx(0.31, abs=0.02)
    assert row["yield_at_vendor_pulse_mj"] == pytest.approx(0.41, abs=0.03)
    # the speculation shot is read at its own point: 50 T, where the
    # patent-mix breakeven time is 17 ms, and from its 100 MJ bank
    row = next(r for r in rows if r["yield_mj"] == 600.0 and r["x_s"] == 0.7)
    assert (row["b_center_t"], row["e_driver_mj"]) == (50.0, 100.0)
    assert row["tau_f_s"] == pytest.approx(0.0166, abs=0.0005)
    assert row["tau_burn_s"] == pytest.approx(0.19, abs=0.01)
    assert row["yield_at_vendor_pulse_mj"] == pytest.approx(3.1, abs=0.1)


def test_slough_cfr2_design_point_satisfies_the_bound():
    """Slough (2025, Nucl. Fusion 65 106019): a D-T FRC at 34.8 T and the
    optimum 15 keV, gain 9.1 on the FRC energy over a 2 to 5 ms transit.
    gain x breakeven time must land inside that transit."""
    from study import breakeven_time_dt_s
    tau_f = breakeven_time_dt_s(34.8, 15.0)
    assert 2e-3 <= 9.1 * tau_f <= 5e-3
    assert tau_f == pytest.approx(0.4e-3, rel=0.15)
