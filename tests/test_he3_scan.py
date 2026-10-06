"""He-3 price concessions re-optimize the burn mix (scripts/he3_scan.py)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from he3_scan import optimum_by_mix  # noqa: E402
from study import build_model, device_fwd, load_config, run  # noqa: E402

# The speculation device's own shot and chamber; each mix takes the rate
# the ladder gives it there. The He-3-rich preset finds no coherent rate
# in this chamber (its short burn keeps the ladder near the 10 Hz grant,
# where the panel wall's steady flux is overrun), so six mixes appear.
GRID = dict(yields=(150.0,), lengths=(10.0,), radii=(0.75,), walls=("panel",))


@pytest.fixture(scope="module")
def model():
    return build_model(load_config("baseline.yaml"))


def test_ledger_price_reproduces_the_speculation_device(model):
    """At the ledger price every mix from the 3:1 one up is admissible in
    the speculation chamber at its own rate, each in the fewest modules
    whose rate fits its burn (more modules the richer the mix), and the
    0.70 mix is the cheapest and reproduces the device."""
    rows = optimum_by_mix(model, u_he3=5e5, net_electric_mw=1000.0, **GRID)
    assert [r["dd_frac"] for r in rows] == [0.314, 0.488, 0.6, 0.7, 0.8, 0.85]
    n_mods = [r["n_mod"] for r in rows]
    assert n_mods == sorted(n_mods) and len(set(n_mods)) == len(n_mods)
    assert all(0.5 < r["duty"] <= 1.0 for r in rows)
    best = min(rows, key=lambda r: r["lcoe"])
    assert best["dd_frac"] == 0.7
    _, fwd = device_fwd("spec", 1000.0)
    _, diag = run(model, fwd)
    assert best["lcoe"] == pytest.approx(diag["lcoe"], abs=0.05)
    assert best["n_mod"] == diag["n_mod"]
    assert best["tritium_adder"] > 0


def test_free_he3_moves_the_optimum_to_the_leanest_admissible_mix(model):
    """With He-3 free the mix that buys its fuel and makes few neutrons,
    the 3:1 one, wins in this chamber (four modules at 2.5 Hz, no tritium
    plant), by about 2 $/MWh over the 0.70 device re-priced at zero."""
    rows = optimum_by_mix(model, u_he3=0.0, net_electric_mw=1000.0, **GRID)
    best = min(rows, key=lambda r: r["lcoe"])
    assert best["dd_frac"] == 0.314 and best["tritium_adder"] == 0.0
    ledger = {r["dd_frac"]: r for r in optimum_by_mix(model, u_he3=5e5, net_electric_mw=1000.0, **GRID)}
    free = {r["dd_frac"]: r for r in rows}
    assert free[0.7]["lcoe"] < ledger[0.7]["lcoe"] - 0.5
    assert best["lcoe"] < free[0.7]["lcoe"] - 1.5
    # the lcoe order reverses with the price: the richer the mix, the less it cares
    assert ledger[0.314]["lcoe"] - free[0.314]["lcoe"] > ledger[0.85]["lcoe"] - free[0.85]["lcoe"]
