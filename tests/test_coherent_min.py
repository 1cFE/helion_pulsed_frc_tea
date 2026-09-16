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


def test_every_burn_branch_is_admissible_in_the_speculation_chamber(model):
    fwd0 = tier_fwd("tier3")
    for b in BURN_BRANCHES:
        fwd = point_fwd(fwd0, 500.0, 30.0, 1.5, "panel", b)
        _, diag = run(model, fwd)
        assert coherence_violations(fwd, diag, "tier3") == []
