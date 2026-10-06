"""He-3 price concessions re-optimize the burn mix (scripts/he3_scan.py)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from he3_scan import optimum_by_mix  # noqa: E402
from study import build_model, device_fwd, load_config, run  # noqa: E402

# The speculation device's own field, bank, shot and chamber; each mix
# takes the rate the ladder gives it there. One 30 m x 1.5 m module at 50
# T carries 1 GWe at every mix, so the rate is set by the plant power
# and the mix trade is the fuel line against the tritium plant.
GRID = dict(fields=(50.0,), banks=(100.0,), gains=(6.0,), lengths=(30.0,),
            radii=(1.5,), walls=("panel",))


@pytest.fixture(scope="module")
def model():
    return build_model(load_config("baseline.yaml"))


def test_ledger_price_reproduces_the_speculation_device(model):
    """At the ledger price every mix is admissible in the speculation
    chamber as a single module, the duty rising with the deuterium
    content (the richer the mix, the longer the burn), and the
    deuterium-rich end is the cheapest and reproduces the device, with the
    whole grid inside 2.4 $/MWh."""
    rows = optimum_by_mix(model, u_he3=5e5, net_electric_mw=1000.0, **GRID)
    assert [r["dd_frac"] for r in rows] == [0.131, 0.314, 0.488, 0.6, 0.7, 0.8, 0.85]
    assert all(r["n_mod"] == 1 for r in rows)
    duties = [r["duty"] for r in rows]
    assert duties == sorted(duties) and duties[-1] <= 1.0
    best = min(rows, key=lambda r: r["lcoe"])
    assert best["dd_frac"] == 0.85
    _, fwd = device_fwd("spec", 1000.0)
    _, diag = run(model, fwd)
    assert best["lcoe"] == pytest.approx(diag["lcoe"], abs=0.05)
    assert best["n_mod"] == diag["n_mod"]
    assert best["tritium_adder"] > 0
    assert max(r["lcoe"] for r in rows) - best["lcoe"] < 2.5


def test_free_he3_moves_the_optimum_to_the_he3_rich_preset(model):
    """With He-3 free the He-3-rich preset wins in this chamber (no
    tritium plant, a duty of 0.07), by about 1.2 $/MWh over the
    deuterium-rich device re-priced at zero, and the ranking of the mix
    grid inverts end to end."""
    rows = optimum_by_mix(model, u_he3=0.0, net_electric_mw=1000.0, **GRID)
    best = min(rows, key=lambda r: r["lcoe"])
    assert best["dd_frac"] == 0.131 and best["tritium_adder"] == 0.0
    ledger = {r["dd_frac"]: r for r in optimum_by_mix(model, u_he3=5e5, net_electric_mw=1000.0, **GRID)}
    free = {r["dd_frac"]: r for r in rows}
    assert free[0.85]["lcoe"] < ledger[0.85]["lcoe"]
    assert best["lcoe"] < free[0.85]["lcoe"] - 1.0
    lcoes_free = [free[dd]["lcoe"] for dd in sorted(free)]
    lcoes_ledger = [ledger[dd]["lcoe"] for dd in sorted(ledger)]
    assert lcoes_free == sorted(lcoes_free)
    assert lcoes_ledger == sorted(lcoes_ledger, reverse=True)
    # the lcoe order reverses with the price: the richer the mix, the less it cares
    assert ledger[0.131]["lcoe"] - free[0.131]["lcoe"] > ledger[0.85]["lcoe"] - free[0.85]["lcoe"]
