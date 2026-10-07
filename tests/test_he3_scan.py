"""He-3 price concessions re-optimize the burn mix (scripts/he3_scan.py)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from he3_scan import optimum_by_mix  # noqa: E402
from study import build_model, device_fwd, load_config, run  # noqa: E402

# The speculation device's own field, bank, shot and chamber (the granted
# 40 T, a 200 MJ bank, 800 MJ shots at a gain of 4.0, 30 m x 1.5 m); each
# mix takes the rate the ladder gives it there, so the mix trade is the
# fuel line and the tritium plant against the modules a longer burn
# needs.
GRID = dict(fields=(40.0,), banks=(200.0,), gains=(4.0,), lengths=(30.0,),
            radii=(1.5,), walls=("panel",))
MIXES = [0.131, 0.314, 0.488, 0.6, 0.7, 0.8, 0.85]


@pytest.fixture(scope="module")
def model():
    return build_model(load_config("baseline.yaml"))


def test_ledger_price_reproduces_the_speculation_device(model):
    """At the ledger price every mix is admissible in the speculation
    device's chamber as a single module (at 40 T the 800 MJ shot's burn
    fits the period at every mix, the lean mixes firing slower), the
    ranking runs monotonically from the He-3-rich preset down to the
    deuterium-rich end, which is the cheapest and reproduces the device,
    with the whole grid inside 2.6 $/MWh."""
    rows = optimum_by_mix(model, u_he3=5e5, net_electric_mw=1000.0, **GRID)
    assert [r["dd_frac"] for r in rows] == MIXES
    assert all(r["duty"] <= 1.0 for r in rows)
    assert [r["n_mod"] for r in rows] == [1] * len(MIXES)
    lcoes = [r["lcoe"] for r in rows]
    assert lcoes == sorted(lcoes, reverse=True)
    best = min(rows, key=lambda r: r["lcoe"])
    assert best["dd_frac"] == 0.85
    _, fwd = device_fwd("spec", 1000.0)
    _, diag = run(model, fwd)
    assert best["lcoe"] == pytest.approx(diag["lcoe"], abs=0.05)
    assert best["n_mod"] == diag["n_mod"]
    assert best["tritium_adder"] > 0
    assert rows[0]["tritium_adder"] == 0.0
    assert max(lcoes) - best["lcoe"] < 2.6


def test_free_he3_moves_the_optimum_to_the_leanest_mix(model):
    """With He-3 free the He-3-rich preset wins in this chamber (no
    tritium plant, a duty of 0.06), by about 1.2 $/MWh over the device's
    0.85 mix re-priced at zero, and the mix grid's ranking inverts to run
    monotonically from the lean end: the richer the mix, the less the
    price matters to it."""
    rows = optimum_by_mix(model, u_he3=0.0, net_electric_mw=1000.0, **GRID)
    best = min(rows, key=lambda r: r["lcoe"])
    assert best["dd_frac"] == 0.131 and best["tritium_adder"] == 0.0
    ledger = {r["dd_frac"]: r for r in optimum_by_mix(model, u_he3=5e5, net_electric_mw=1000.0, **GRID)}
    free = {r["dd_frac"]: r for r in rows}
    assert free[0.85]["lcoe"] < ledger[0.85]["lcoe"]
    assert best["lcoe"] < free[0.85]["lcoe"] - 1.2
    lcoes_free = [free[dd]["lcoe"] for dd in MIXES]
    assert lcoes_free == sorted(lcoes_free)
    assert ledger[0.131]["lcoe"] - free[0.131]["lcoe"] > ledger[0.85]["lcoe"] - free[0.85]["lcoe"]
