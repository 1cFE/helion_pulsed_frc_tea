"""He-3 price concessions re-optimize the burn mix (scripts/he3_scan.py)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from he3_scan import optimum_by_mix  # noqa: E402
from study import GAIN_BASIS, build_model, device_fwd, load_config, run  # noqa: E402

# The speculation device's own field, bank, shot and chamber (the basis
# field, a 200 MJ bank, the design-basis gain, 15 m x 1.5 m); each mix
# takes the rate the ladder gives it there, so the mix trade is the fuel
# line and the tritium plant against the modules a longer burn needs.
GRID = dict(fields=(22.0,), banks=(200.0,), gains=(GAIN_BASIS,), lengths=(15.0,),
            radii=(1.5,), walls=("panel",))
MIXES = [0.314, 0.488, 0.6, 0.7, 0.8, 0.85]


@pytest.fixture(scope="module")
def model():
    return build_model(load_config("baseline.yaml"))


def test_ledger_price_reproduces_the_speculation_device(model):
    """At the ledger price every mix but the He-3-rich preset (whose
    short burn admits only a single module, which overruns the panel
    wall at 1 GWe) is admissible in the speculation device's chamber,
    in two modules up to the device's 0.70 mix and three beyond it,
    where the longer burn costs a module; the 0.70 mix is the cheapest
    and reproduces the device, with the whole grid inside 2.1 $/MWh."""
    rows = optimum_by_mix(model, u_he3=5e5, net_electric_mw=1000.0, **GRID)
    assert [r["dd_frac"] for r in rows] == MIXES
    assert all(r["duty"] <= 1.0 for r in rows)
    assert [r["n_mod"] for r in rows] == [2, 2, 2, 2, 3, 3]
    best = min(rows, key=lambda r: r["lcoe"])
    assert best["dd_frac"] == 0.7
    _, fwd = device_fwd("spec", 1000.0)
    _, diag = run(model, fwd)
    assert best["lcoe"] == pytest.approx(diag["lcoe"], abs=0.05)
    assert best["n_mod"] == diag["n_mod"]
    assert best["tritium_adder"] > 0
    assert max(r["lcoe"] for r in rows) - best["lcoe"] < 2.1


def test_free_he3_moves_the_optimum_to_the_leanest_mix(model):
    """With He-3 free the leanest admissible mix wins in this chamber
    (the 3:1 mix, no tritium plant, a duty of 0.27), by about 0.9 $/MWh
    over the device's 0.70 mix re-priced at zero, and the mix grid's
    ranking turns monotone from the lean end: the richer the mix, the
    less the price matters to it."""
    rows = optimum_by_mix(model, u_he3=0.0, net_electric_mw=1000.0, **GRID)
    best = min(rows, key=lambda r: r["lcoe"])
    assert best["dd_frac"] == 0.314 and best["tritium_adder"] == 0.0
    ledger = {r["dd_frac"]: r for r in optimum_by_mix(model, u_he3=5e5, net_electric_mw=1000.0, **GRID)}
    free = {r["dd_frac"]: r for r in rows}
    assert free[0.7]["lcoe"] < ledger[0.7]["lcoe"]
    assert best["lcoe"] < free[0.7]["lcoe"] - 0.9
    lcoes_free = [free[dd]["lcoe"] for dd in MIXES]
    assert lcoes_free == sorted(lcoes_free)
    lcoes_ledger = [ledger[dd]["lcoe"] for dd in MIXES]
    assert lcoes_ledger.index(min(lcoes_ledger)) == MIXES.index(0.7)
    assert lcoes_ledger[:4] == sorted(lcoes_ledger[:4], reverse=True)
    assert ledger[0.314]["lcoe"] - free[0.314]["lcoe"] > ledger[0.85]["lcoe"] - free[0.85]["lcoe"]
