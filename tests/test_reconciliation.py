"""Reconciliation bands the model cannot price internally (scripts/reconciliation.py)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from reconciliation import F_PDV_CEILING_SLOUGH, f_pdv_ceiling_risk  # noqa: E402
from study import build_model, device_fwd, load_config, run  # noqa: E402


@pytest.fixture(scope="module")
def model():
    return build_model(load_config("baseline.yaml"))


def test_slough_ceiling_is_the_flux_conserver_limit():
    """Slough (2025) eq. 18: eta = (1 - x_s^2)/(2.5 - x_s^2) -> 0.4 as x_s -> 0."""
    assert F_PDV_CEILING_SLOUGH == 0.4


def test_recovery_share_at_the_slough_ceiling_raises_the_extrapolation_device(model):
    _, fwd = device_fwd("extrap", 1000.0)
    _, base = run(model, fwd)
    lcoe, delta, f_pdv_eff = f_pdv_ceiling_risk(model, fwd, base)
    assert f_pdv_eff == pytest.approx(0.4)
    assert delta > 0
    assert lcoe == pytest.approx(base["lcoe"] + delta)
