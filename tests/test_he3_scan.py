"""He-3 price concessions re-optimize the burn mix (scripts/he3_scan.py)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from he3_scan import optimum_by_mix  # noqa: E402
from study import build_model, device_fwd, load_config, run  # noqa: E402

# The speculation device's own geometry plus the D-rich design's longer
# chamber, so the He-3-rich row can reproduce the ladder and the other
# mixes have the chamber they would choose.
GRID = dict(yields=(500.0,), lengths=(15.0, 30.0), radii=(1.5,), walls=("panel",))


@pytest.fixture(scope="module")
def model():
    return build_model(load_config("baseline.yaml"))


def test_ledger_price_reproduces_the_speculation_device(model):
    """At the ledger price the He-3-rich mix is the only admissible one in
    the speculation chamber (the richer mixes overrun the period at a
    single 1 GWe module's fusion power) and reproduces the device."""
    rows = optimum_by_mix(model, u_he3=5e5, net_electric_mw=1000.0, **GRID)
    assert [r["dd_frac"] for r in rows] == [0.131]
    he3_rich = rows[0]
    _, fwd = device_fwd("spec", 1000.0)
    _, diag = run(model, fwd)
    assert he3_rich["lcoe"] == pytest.approx(diag["lcoe"], abs=0.05)
    assert he3_rich["length_m"] == 15.0
    assert he3_rich["tritium_adder"] == 0.0


def test_free_he3_keeps_the_he3_rich_mix_and_widens_its_lead(model):
    rows = optimum_by_mix(model, u_he3=0.0, net_electric_mw=1000.0, **GRID)
    assert [r["dd_frac"] for r in rows] == [0.131]
    ledger = optimum_by_mix(model, u_he3=5e5, net_electric_mw=1000.0, **GRID)[0]
    assert rows[0]["lcoe"] < ledger["lcoe"] - 3.0
    assert rows[0]["tritium_adder"] == 0.0
