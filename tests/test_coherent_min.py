"""The design search's burn branches (scripts/coherent_min.py)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from coherent_min import BURN_BRANCHES, point_fwd, tier_fwd  # noqa: E402
from study import (  # noqa: E402
    build_model,
    coherence_violations,
    f_rad_floor,
    load_config,
    run,
)


@pytest.fixture(scope="module")
def model():
    return build_model(load_config("baseline.yaml"))


def test_every_burn_branch_sits_on_its_own_bremsstrahlung_floor():
    for b in BURN_BRANCHES:
        assert b["f_rad"] >= f_rad_floor(b["dhe3_dd_frac"])


def test_the_grid_spans_the_mix_from_the_preset_to_the_d_rich_end():
    """Constraint 8 makes the mix a continuous trade, so the grid carries
    Helion's own mix and the deuterium side densely."""
    dds = [b["dhe3_dd_frac"] for b in BURN_BRANCHES]
    assert dds == sorted(dds)
    assert dds[0] == 0.131 and dds[-1] == 0.85
    assert 0.314 in dds and 0.488 in dds
    assert sum(1 for d in dds if d > 0.488) >= 3


def test_only_the_he3_rich_branch_fits_the_speculation_chamber(model):
    """In the speculation device's chamber (500 MJ, 15 m x 1.5 m, a single
    1 GWe module) the He-3-rich branch is admissible; every richer mix
    overruns the pulse period (constraint 8), whatever else it trips."""
    fwd0 = tier_fwd("tier3")
    for b in BURN_BRANCHES:
        fwd = point_fwd(fwd0, 500.0, 15.0, 1.5, "panel", b)
        _, diag = run(model, fwd)
        v = coherence_violations(fwd, diag, "tier3")
        if b["dhe3_dd_frac"] == 0.131:
            assert v == []
        else:
            assert any(x.startswith("duty") for x in v), b
