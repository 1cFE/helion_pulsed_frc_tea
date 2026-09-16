"""Burn-mix translation between the He3/D ion ratio and dd_frac (scripts/mix.py)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from mix import (  # noqa: E402
    STUDY_DD_FRACS,
    dd_frac_from_he3_over_d,
    he3_over_d_from_burn,
    he3_over_d_from_dd_frac,
)
from study import HE3_OVER_D_PATENT  # noqa: E402
from tritium_burn import he3_over_d  # noqa: E402


def test_patent_ion_ratio_is_helions_dd_frac_at_70_kev():
    """The writeup's Notation paragraph: He3/D = 0.158 at 70 keV is 0.49."""
    assert dd_frac_from_he3_over_d(HE3_OVER_D_PATENT, 70.0) == pytest.approx(0.488, abs=0.001)


def test_three_to_one_label_matches_the_calibration_anchor():
    """dd_frac 0.314 is the blog's bremsstrahlung-minimum anchor; a 3:1
    D:He-3 ion mix at 70 keV lands within 0.005 of it."""
    assert dd_frac_from_he3_over_d(1.0 / 3.0, 70.0) == pytest.approx(0.314, abs=0.005)


def test_knob_map_round_trips_at_every_study_mix():
    for dd in STUDY_DD_FRACS.values():
        assert dd_frac_from_he3_over_d(he3_over_d_from_dd_frac(dd)) == pytest.approx(dd)


def test_burn_map_agrees_with_tritium_burn_when_nothing_recycles():
    dd = 0.85
    primary_ratio = (1.0 - dd) / dd
    assert he3_over_d_from_burn(dd, 0.0, 70.0) == pytest.approx(he3_over_d(primary_ratio, 70.0))
