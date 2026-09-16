"""He-3 price concessions re-optimize the burn mix (scripts/he3_scan.py)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from he3_scan import optimum_by_mix  # noqa: E402
from study import build_model, device_fwd, load_config, run  # noqa: E402

# The speculation device's own geometry plus the 3:1 mix's preferred
# chamber, so the D-rich row can reproduce the ladder and the other
# mixes have a chamber they would choose.
GRID = dict(yields=(500.0,), lengths=(20.0, 30.0), radii=(1.5,), walls=("panel",))


@pytest.fixture(scope="module")
def model():
    return build_model(load_config("baseline.yaml"))


def test_ledger_price_reproduces_the_speculation_device(model):
    rows = optimum_by_mix(model, u_he3=5e5, net_electric_mw=1000.0, **GRID)
    d_rich = next(r for r in rows if r["dd_frac"] == 0.85)
    _, fwd = device_fwd("spec", 1000.0)
    _, diag = run(model, fwd)
    assert d_rich["lcoe"] == pytest.approx(diag["lcoe"], abs=0.05)
    assert d_rich["length_m"] == 30.0
    assert min(rows, key=lambda r: r["lcoe"])["dd_frac"] == 0.85


def test_free_he3_moves_the_optimum_off_the_d_rich_mix(model):
    rows = optimum_by_mix(model, u_he3=0.0, net_electric_mw=1000.0, **GRID)
    assert len(rows) == 3
    best = min(rows, key=lambda r: r["lcoe"])
    d_rich = next(r for r in rows if r["dd_frac"] == 0.85)
    assert best["dd_frac"] < 0.85
    assert best["lcoe"] < d_rich["lcoe"]
    assert best["tritium_adder"] == 0.0
