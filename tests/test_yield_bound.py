"""Constraint 7: the shot yield against the plasma energy and the burn time.

gain <= chi x burn time / breakeven time, with chi the plasma-thermal share
of the delivered driver energy (chi_from_xs) and the breakeven time the
plasma's energy density over its fusion power density at the burn point.
Pinned at costingfe 44434d9 on the patent burn point of config/baseline.yaml
(22 T, 70 keV, n_D 0.75e22 m^-3, He3/D 0.158).
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
    the burn time its shot implies at the reference x_s (0.7, chi 0.52)."""
    assert X_S_REFERENCE == 0.7
    assert chi_from_xs(X_S_REFERENCE) == pytest.approx(0.52, abs=0.01)
    _, fwd = device_fwd("helion", 1000.0)
    _, diag = run(model, fwd)
    assert diag["tau_burn_implied_s"] == pytest.approx(0.42, abs=0.02)
    _, fwd = device_fwd("spec", 1000.0)
    _, diag = run(model, fwd)
    assert diag["tau_burn_implied_s"] == pytest.approx(1.65, abs=0.05)


def test_bound_table_lists_both_shots_across_the_xs_span():
    from yield_bound import bound_table
    rows = bound_table()
    shots = sorted({r["yield_mj"] for r in rows})
    assert shots == [128.1, 500.0]
    assert sorted({r["x_s"] for r in rows}) == [0.5, 0.7, 0.85]
    row = next(r for r in rows if r["yield_mj"] == 128.1 and r["x_s"] == 0.85)
    assert row["tau_burn_s"] == pytest.approx(0.31, abs=0.02)
    assert row["yield_at_vendor_pulse_mj"] == pytest.approx(0.41, abs=0.03)


def test_slough_cfr2_design_point_satisfies_the_bound():
    """Slough (2025, Nucl. Fusion 65 106019): a D-T FRC at 34.8 T and the
    optimum 15 keV, gain 9.1 on the FRC energy over a 2 to 5 ms transit.
    gain x breakeven time must land inside that transit."""
    from study import breakeven_time_dt_s
    tau_f = breakeven_time_dt_s(34.8, 15.0)
    assert 2e-3 <= 9.1 * tau_f <= 5e-3
    assert tau_f == pytest.approx(0.4e-3, rel=0.15)
