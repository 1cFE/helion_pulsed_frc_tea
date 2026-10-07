"""The design search's burn branches, graded grids and rate ladder
(scripts/coherent_min.py)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from coherent_min import (  # noqa: E402
    BANKS_MJ,
    BURN_BRANCHES,
    FIELDS_T,
    GAINS,
    RATE_STEPS,
    admissible,
    at_plant_size,
    granted_field_t,
    point_fwd,
    point_rows,
    rate_ceilings_hz,
    rate_designs,
    scan_grid,
    sensitivity,
    tier_fwd,
)
from study import (  # noqa: E402
    build_model,
    coherence_violations,
    duty_bound_rate_hz,
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


def test_only_the_he3_rich_branch_fits_a_single_module_at_the_grant(model):
    """At the speculation grant (10 Hz) and the basis field a 500 MJ shot
    in a 15 m x 1.5 m chamber makes a single 1 GWe module, in which only
    the He-3-rich branch is admissible; every richer mix overruns the
    pulse period (constraint 8), whatever else it trips."""
    fwd0 = tier_fwd("tier3")
    for b in BURN_BRANCHES:
        fwd = point_fwd(fwd0, 500.0, 15.0, 1.5, "panel", b)
        _, diag = run(model, fwd)
        v = coherence_violations(fwd, diag, "tier3")
        if b["dhe3_dd_frac"] == 0.131:
            assert v == []
        else:
            assert any(x.startswith("duty") for x in v), b


def test_the_rate_ladder_sits_at_and_below_the_grant_and_the_duty_bound(model):
    """A grant is permission, not obligation: the ceilings scanned at a
    point are RATE_STEPS times min(grant, 1 / implied burn), never above
    the grant, and the grant itself is priced first wherever the burn
    overruns its period. Helion's mix on the design-basis shot at the
    basis field fits the 3 Hz grant (its bound is above it); the
    deuterium-rich mix does not."""
    assert RATE_STEPS[0] == 1.0 and list(RATE_STEPS) == sorted(RATE_STEPS, reverse=True)
    fwd0 = tier_fwd("tier2")
    lean = point_fwd(fwd0, 128.1, 10.0, 0.75, "panel", BURN_BRANCHES[2])
    assert duty_bound_rate_hz(lean, 50.0) > 3.0
    ladder = rate_ceilings_hz(lean, model)
    assert ladder[0] == 3.0 and len(ladder) == len(RATE_STEPS)
    rich = point_fwd(fwd0, 128.1, 10.0, 0.75, "panel", BURN_BRANCHES[-1])
    bound = duty_bound_rate_hz(rich, 50.0)
    assert bound < 3.0
    ladder = rate_ceilings_hz(rich, model)
    assert ladder[0] == 3.0 and ladder[1] == pytest.approx(bound)
    assert ladder == sorted(ladder, reverse=True) and max(ladder) <= 3.0
    assert ladder[-1] == pytest.approx(0.5 * bound)


def test_the_search_evaluates_sub_ceiling_rates_and_they_admit_the_rich_mixes(model):
    """Down the ladder the module count rises and the solved rate falls;
    the deuterium-rich mix at the basis field is excluded at the 3 Hz
    grant by constraint 8 and admitted one rung down, where the search
    prices it. Each rung that binds is a distinct design (a rung the
    previous rate already clears is skipped)."""
    fwd0 = tier_fwd("tier2")
    rich = point_fwd(fwd0, 128.1, 10.0, 0.75, "panel", BURN_BRANCHES[-1])
    designs = list(rate_designs(model, rich))
    assert len(designs) >= 4
    n_mods = [d["n_mod"] for _, d in designs]
    rates = [d["f_rep_hz"] for _, d in designs]
    assert n_mods == sorted(n_mods) and len(set(n_mods)) == len(n_mods)
    assert rates == sorted(rates, reverse=True)
    assert all(f["max_f_rep"] <= 3.0 for f, _ in designs)
    status = [coherence_violations(f, d, "tier2") for f, d in designs]
    assert any(x.startswith("duty") for x in status[0])
    assert status[1] == [] and all(not v for v in status[1:])
    assert all(d["tau_burn_implied_s"] * d["f_rep_hz"] <= 1.0 for _, d in designs[1:])
    # the slower bank lives longer and the plant is available more, but
    # the hardware of the added modules outweighs it at every rung
    lcoes = [d["lcoe"] for _, d in designs[1:]]
    assert lcoes == sorted(lcoes)
    assert designs[2][1]["availability"] > designs[1][1]["availability"]
    assert designs[2][1]["t_bank_yr"] > designs[1][1]["t_bank_yr"]


def test_the_field_and_the_bank_are_graded_by_the_evidence_ladder():
    """The patent's 22 T and Polaris's 50 MJ are the design basis and no
    record exists above either. The field is a stepped entry read from
    the tier configs (22 T at records, 30 T granted at extrapolations, 40
    T at speculation), and each grade's grid runs from the basis to one
    step above its grant, the step above priced as a sensitivity. The
    bank: held at records, doubled at extrapolations, to 200 MJ at
    speculation. The shot is a gain on the bank: the design-basis gain
    alone below speculation, free there, with the sourced bank
    reproducing the 128 to 2000 MJ yield grid."""
    from study import B_COMPRESSION_T, E_DEL_BASIS_MJ, GAIN_BASIS

    grants = {tier: granted_field_t(tier_fwd(tier)) for tier in ("tier1", "tier2", "tier3")}
    assert grants == {"tier1": B_COMPRESSION_T, "tier2": 30.0, "tier3": 40.0}
    assert load_config("tier2.yaml")["records"]["b_center"]["value"] == 30.0
    assert load_config("tier3.yaml")["records"]["b_center"]["value"] == 40.0
    assert FIELDS_T["tier1"] == (B_COMPRESSION_T, 30.0)
    assert FIELDS_T["tier2"] == (B_COMPRESSION_T, 30.0, 40.0)
    assert FIELDS_T["tier3"] == (B_COMPRESSION_T, 30.0, 40.0, 50.0)
    for tier, fields in FIELDS_T.items():
        assert fields[0] == B_COMPRESSION_T
        assert sum(1 for b in fields if b > grants[tier]) == 1, tier
        assert grants[tier] in fields
    assert BANKS_MJ["tier1"] == (E_DEL_BASIS_MJ,)
    assert BANKS_MJ["tier2"] == (E_DEL_BASIS_MJ, 100.0)
    assert BANKS_MJ["tier3"] == (E_DEL_BASIS_MJ, 100.0, 200.0)
    assert GAINS["tier1"] == GAINS["tier2"] == (GAIN_BASIS,)
    assert [round(g * E_DEL_BASIS_MJ, 1) for g in GAINS["tier3"]] == \
        [128.1, 150.0, 200.0, 300.0, 500.0, 750.0, 1000.0, 1500.0, 2000.0]
    assert len(scan_grid("tier1")) == 2 * 6 * 4 * 2 * 7
    assert len(scan_grid("tier2")) == 3 * 2 * 6 * 4 * 2 * 7
    assert len(scan_grid("tier3")) == 4 * 3 * 9 * 6 * 4 * 2 * 7


def test_a_point_above_the_grant_is_labelled_as_a_sensitivity_not_excluded_by_the_coil(model):
    """A 40 T point in a 15 m x 1.5 m chamber on the doubled bank carries
    the coil pressure it would cycle to (637 MPa, an audit) and no coil
    violation at any grade. At the extrapolation grade (30 T granted) it
    is above the grant: coherent rows are a sensitivity, none is
    admissible; at speculation (40 T granted) the same rows are
    admissible. A 50 T point is above the speculation grant. The flash
    prune ends a ladder whose shot the wall cannot survive."""
    from study import E_FLASH_MELT_MJ_M2, GAIN_BASIS

    branch = BURN_BRANCHES[-1]
    point = (40.0, 100.0, GAIN_BASIS, 15.0, 1.5, "panel", branch)
    rows2 = point_rows(model, "tier2", tier_fwd("tier2"), point)
    assert rows2 and all(r["field_t"] == 40.0 and r["granted_t"] == 30.0 for r in rows2)
    assert all(r["field_above_grant"] and not admissible(r) for r in rows2)
    assert all("coil" not in r["violations"] for r in rows2)
    assert rows2[0]["coil_pressure_mpa"] == pytest.approx(636.6, abs=1)
    assert any(sensitivity(r) for r in rows2)
    rows3 = point_rows(model, "tier3", tier_fwd("tier3"), point)
    assert all(r["granted_t"] == 40.0 and not r["field_above_grant"] for r in rows3)
    assert any(admissible(r) for r in rows3) and not any(sensitivity(r) for r in rows3)
    high = point_rows(model, "tier3", tier_fwd("tier3"), (50.0,) + point[1:])
    assert all(r["field_above_grant"] for r in high)
    assert high[0]["coil_pressure_mpa"] == pytest.approx(994.7, abs=1)
    melt = (22.0, 50.0, 40.0, 10.0, 0.5, "panel", branch)
    rows_melt = point_rows(model, "tier3", tier_fwd("tier3"), melt)
    assert len(rows_melt) == 1 and rows_melt[0]["e_flash_mj_m2"] > E_FLASH_MELT_MJ_M2


def test_a_design_carries_the_tightest_ceiling_it_fits(model):
    """When the grant rung's design already clears the next rung's
    ceiling, the design is carried under that lower ceiling, so a re-size
    to another plant power keeps it under the duty bound rather than
    snapping a hair over it: the records design at 1 GWe."""
    from study import duty_bound_rate_hz

    fwd0 = tier_fwd("tier1")
    rich = point_fwd(fwd0, 128.1, 10.0, 0.75, "panel", BURN_BRANCHES[-1])
    designs = rate_designs(model, rich)
    bound = duty_bound_rate_hz(rich, 50.0)
    assert bound < 1.0
    f, d = designs[0]
    assert f["max_f_rep"] == pytest.approx(bound)
    assert d["f_rep_hz"] <= bound and d["n_mod"] == 25


def test_a_park_re_size_keeps_the_module_under_its_wall_bound(model):
    """The extrapolation device's scan row (30 T, 100 MJ, 15 m x 1.5 m,
    dd_frac 0.85, carried under the 2.593 Hz ladder rung) tripled at that
    rung snaps to 11 modules at 2.58 Hz and overruns the panel wall;
    at_plant_size re-sizes under the lower of the rung and the module's
    wall bound (2.445 Hz), 12 modules at 2.37 Hz, coherent, which is how
    the device definition is built."""
    from study import GAIN_BASIS

    row = dict(field_t=30.0, bank_mj=100.0, gain=GAIN_BASIS, length_m=15.0,
               radius_m=1.5, fw_class="panel", dd_frac=0.85, max_f_rep=2.5933)
    d, v = at_plant_size(model, "tier2", row, 3000.0)
    assert not v and d["n_mod"] == 12 and d["f_rep_hz"] == pytest.approx(2.37, abs=0.01)
    assert d["q_wall_mw_m2"] < 2.0
    from coherent_min import row_fwd
    _, raw = run(model, row_fwd("tier2", row, 3000.0))
    assert raw["n_mod"] == 11 and raw["q_wall_mw_m2"] > 2.0
