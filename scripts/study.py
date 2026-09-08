"""Shared runner for the Helion-class pulsed FRC TEA study.

Loads a study config, builds the costingfe model, and runs the rep-rate
sizing path (size_from_power=True): costingfe holds the cited shot fixed,
bisects f_rep against the per-module net target, and solves the integer
module count off the max_f_rep ceiling. Unlike Borealis there is no
geometric closure to write; the framework closes the machine.

This module also carries the study's coherence constraints, which encode
the red-team review's physics findings so no scan point can silently
combine values the review ruled mutually inconsistent:

- f_rad_floor(dd_frac): bremsstrahlung floor coupled to the burn mix
  (D-rich plasmas radiate more, not less).
- composite recovery cap: eta_dec * f_pdv bounded by the one published
  projection ("optimal burn cycles exceeding 90% recovery"), which speaks
  to the product, not to each factor separately.
- wall limits: steady flux against the declared first-wall class, and a
  per-shot flash-energy bound against tungsten melt.
- tritium adder: a D-rich burn mix breeds tens of kg of tritium per year;
  the fuel-handling account is raised to a tritium-plant scope whenever
  the mix crosses into that regime.
"""
import os

os.environ.setdefault("COSTINGFE_BACKEND", "numpy")  # float64; set before costingfe import

import math
import warnings
from pathlib import Path

import yaml
from costingfe import ConfinementConcept, CostModel, Fuel

CONFIG_DIR = Path(__file__).resolve().parents[1] / "config"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs"

# --- coherence constants (sources: docs/red_team_review.md) -----------------

# Bremsstrahlung-consistent radiated fraction vs burn mix, at the study's own
# calibration: the blog-derived pair f_rad 0.163 at dd_frac 0.314 (a 3:1
# D:He-3 plasma at its bremsstrahlung minimum) implies T_i about 60-70 keV
# at T_e = T_i/2 under Bosch-Hale reactivities + non-relativistic
# bremsstrahlung. Linear interpolation between the review's two computed
# anchors; relativistic corrections would raise it another 10-25%. The
# vendor's own point (baseline.yaml: 0.23 at 0.488, T_e = T_i) sits above
# this floor, as a floor requires.
_F_RAD_ANCHORS = ((0.314, 0.163), (0.85, 0.28))

# Composite plasma-to-electricity recovery cap, eta_dec * f_pdv. The only
# source speaking to the chain is the APS DPP24 projection "optimal burn
# cycles exceeding 90% recovery", which is the PRODUCT for an optimal cycle
# in theory. Tier 2 keeps engineering margin below it; tier 3 takes the
# theory optimum at face value.
COMPOSITE_RECOVERY_CAP = {"tier2": 0.80, "tier3": 0.90}

# Per-shot wall flash-energy bound [MJ/m^2]: tungsten melt threshold about
# 50 MJ m^-2 s^-1/2 for a millisecond-class deposition (sqrt(1 ms) = 0.0316),
# with NO engineering margin. A real wall wants to sit well below this.
E_FLASH_MELT_MJ_M2 = 1.5

# First-wall steady-state qualification limits [MW/m^2], mirroring
# costing_constants.yaml fw_class_q_limit.
Q_LIM = {"panel": 2.0, "hhf": 10.0, "beam_dump": 20.0}

# Tritium-plant capital [M$, plant-level] charged when the burn mix is D-rich
# enough to make the machine a bulk tritium facility (tens of kg/yr bred).
# Red-team band 100-300 M$ (allowance, not an estimate) anchored at this
# study's tier-2 reference machine: 1 GWe, dd_frac 0.85, about 228 MW of
# plant-level neutron power and about 87 kg/yr of bred tritium; mid-band
# point, swept in reconciliation.py. The plant splits into a fixed core
# (isotope separation, safety envelope, getter-bed decay store) and a
# throughput-scaled balance, so a small plant is not charged the full
# reference facility and a bigger one is charged more.
# Unit-priced, not anchored: the throughput-scaled balance is a stated
# price per MW of plant neutron power (a definition the reconciliation
# band 100-300 M$ at reference scale brackets), so the reference machine's
# adder is a consequence, not an identity.
TRITIUM_FIXED_MUSD = 50.0
TRITIUM_MUSD_PER_MW_NEUTRON = 0.657
# The adder fires from the vendor's own catalyzed mix upward: the basis fuel
# cycle (patent He3/D = 0.158, dd_frac 0.488 at 70 keV) stores bred tritium
# by design, so any device at or above it is a bulk tritium facility.
DD_FRAC_TRITIUM_THRESHOLD = 0.488

# Chamber-coupled recovery bound (coherence constraint 6). The compressed
# flux volume is estimated as all delivered driver energy stored at the
# basis compression field (patent triple, B = 22 T): V_i = E_del/(B^2/2mu0),
# about 0.26 m^3 at 50 MJ. Adiabatic expansion to the chamber volume V_f
# caps the recoverable fraction at 1 - (V_i/V_f)^(2/3); the radial channel
# carries about 0.8 of the boundary work (FRC adiabatic scalings), so
# f_pdv_eff = min(claim, share x cap) with share = 0.8 unless axial-channel
# capture is claimed (tier 3) or the point is the unchallenged vendor basis
# (share 1.0 default).
B_COMPRESSION_T = 22.0
_MU0 = 4e-7 * 3.141592653589793
F_PDV_RADIAL_SHARE_DEFAULT = 1.0


def f_pdv_cap(fwd: dict, model: CostModel) -> float:
    ed = model._eng_defaults
    e_del_j = fwd.get("e_driver_mj", ed["e_driver_mj"]) * 1e6
    v_i = e_del_j / (B_COMPRESSION_T**2 / (2 * _MU0))
    r = fwd.get("plasma_t", ed["plasma_t"])
    length = fwd.get("chamber_length", ed["chamber_length"])
    v_f = 3.141592653589793 * r * r * length
    return 1.0 - (v_i / v_f) ** (2.0 / 3.0)

_VACUUM_T_DEFAULT = 0.10  # m; concept YAML plasma-to-wall gap


def load_config(name: str) -> dict:
    with open(CONFIG_DIR / name) as f:
        return yaml.safe_load(f)


def build_model(cfg: dict) -> CostModel:
    return CostModel(
        concept=ConfinementConcept(cfg["concept"]),
        fuel=Fuel(cfg["fuel"]),
    )


def apply_records(fwd: dict, cfg_name: str) -> dict:
    """Overlay a tier config's records onto a forward dict (in place)."""
    for key, rec in load_config(cfg_name)["records"].items():
        fwd[key] = rec["value"]
    return fwd


def f_rad_floor(dd_frac: float) -> float:
    """Bremsstrahlung-consistent f_rad at the study calibration (see above)."""
    (x0, y0), (x1, y1) = _F_RAD_ANCHORS
    f = y0 + (y1 - y0) * (dd_frac - x0) / (x1 - x0)
    return max(f, 0.08)  # review side-finding: floor at the YAML mix is 0.08+


def wall_area_m2(fwd: dict) -> float:
    """Pulsed-cylinder first-wall area, matching costingfe compute_geometry."""
    r_w = fwd.get("plasma_t", 0.5) + fwd.get("vacuum_t", _VACUUM_T_DEFAULT)
    return 2.0 * math.pi * r_w * fwd.get("chamber_length", 10.0)


def run(model: CostModel, fwd: dict, tritium_adder: bool = True):
    """Forward with rep-rate sizing; returns (result, diagnostics dict).

    Captures the model's audit warnings rather than letting them scroll by,
    and computes the wall metrics the coherence checks need. When the burn
    mix is D-rich (dd_frac > threshold) the fuel-handling account C220500 is
    raised by TRITIUM_PLANT_MUSD via cost_overrides (probe run first, since
    overrides replace rather than add).
    """
    fwd = dict(fwd)
    share = fwd.pop("f_pdv_radial_share", F_PDV_RADIAL_SHARE_DEFAULT)
    cap = f_pdv_cap(fwd, model)
    f_pdv_claim = fwd.get("f_pdv", float(model.cc.f_pdv))
    fwd["f_pdv"] = min(f_pdv_claim, share * cap)
    overrides = None
    tritium_musd = 0.0
    if tritium_adder and fwd.get("dhe3_dd_frac", 0.131) >= DD_FRAC_TRITIUM_THRESHOLD:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            probe = model.forward(size_from_power=True, **fwd)
        base_c220500 = float(probe.cas22_detail["C220500"])
        p_neutron_total = float(probe.power_table.p_neutron) * int(probe.solved_n_mod)
        tritium_musd = (
            TRITIUM_FIXED_MUSD + TRITIUM_MUSD_PER_MW_NEUTRON * p_neutron_total
        )
        overrides = {"C220500": base_c220500 + tritium_musd}

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = model.forward(size_from_power=True, cost_overrides=overrides, **fwd)

    pt = result.power_table
    f_rep = float(result.params.get("f_rep", 0.0))
    area = wall_area_m2(result.params)
    p_wall = float(pt.p_wall)  # per-module chamber surface load [MW]
    diag = {
        "lcoe": float(result.costs.lcoe),
        "n_mod": int(result.solved_n_mod),
        "f_rep_hz": f_rep,
        "q_wall_mw_m2": p_wall / area,
        "e_flash_mj_m2": (p_wall / f_rep / area) if f_rep > 0 else float("inf"),
        "capital_per_kw": float(result.costs.capital_per_kw),
        "f_pdv_eff": fwd["f_pdv"],
        "f_pdv_cap": cap,
        "tritium_adder_musd": tritium_musd,
        "warnings": sorted({str(w.message) for w in caught}),
    }
    return result, diag


# Concept-YAML per-pulse D burnup: the default exposure behind the tritium
# in-pulse burn floor when a point does not override burn_fraction.
_BF_DEFAULT = 1.2e-4
_T_I_CALIB_KEV = 70.0
F_T_FLOOR_TOL = 0.01  # flag only when the shortfall is material


def f_t_from_burnup(f_d: float, t_i_kev: float) -> float:
    """Thermalized-limit in-pulse tritium burn implied by the D burnup.

    The per-pass D burnup pins the integrated exposure -ln(1 - f_d); a
    triton born mid-pulse sees the remainder scaled by the DT/DD
    reactivity ratio. Averaging over births: f_T = 1 - (1 - e^-x)/x.
    Assumes the triton thermalizes and stays confined; prompt loss from
    the small-s plasmoid is the one escape below this floor."""
    from costingfe.layers.reactivity import sigv_dd_n, sigv_dd_p, sigv_dt

    x_dd = -math.log1p(-f_d)
    ratio = float(sigv_dt(t_i_kev)) / float(sigv_dd_n(t_i_kev) + sigv_dd_p(t_i_kev))
    x = ratio * x_dd
    return 1.0 - (1.0 - math.exp(-x)) / x


def coherence_violations(fwd: dict, diag: dict, tier: str) -> list[str]:
    """Return the list of red-team constraints a run violates (empty = coherent)."""
    v = []
    f_t_floor = f_t_from_burnup(fwd.get("burn_fraction", _BF_DEFAULT),
                                _T_I_CALIB_KEV)
    if fwd.get("dhe3_f_T", 0.0) < f_t_floor - F_T_FLOOR_TOL:
        v.append(
            f"dhe3_f_T {fwd.get('dhe3_f_T', 0.0):.3f} sits below the "
            f"thermalized in-pulse burn floor {f_t_floor:.3f} at this "
            f"burnup: coherent only under prompt MeV-triton loss")
    dd = fwd.get("dhe3_dd_frac", 0.131)
    floor = f_rad_floor(dd)
    if fwd.get("f_rad", 0.05) < floor - 1e-9:
        v.append(f"f_rad {fwd.get('f_rad')} below bremsstrahlung floor {floor:.3f} at dd_frac {dd}")
    comp = fwd.get("eta_dec", 0.85) * diag.get("f_pdv_eff",
                                                fwd.get("f_pdv", 0.80))
    cap = COMPOSITE_RECOVERY_CAP[tier]
    if comp > cap + 1e-9:
        v.append(f"eta_dec*f_pdv = {comp:.3f} exceeds the {tier} composite cap {cap}")
    q_lim = Q_LIM[fwd.get("fw_class", "panel")]
    if diag["q_wall_mw_m2"] > q_lim * (1 + 1e-9):
        v.append(f"steady wall flux {diag['q_wall_mw_m2']:.2f} MW/m^2 over '{fwd.get('fw_class', 'panel')}' limit {q_lim}")
    if diag["e_flash_mj_m2"] > E_FLASH_MELT_MJ_M2:
        v.append(f"per-shot flash {diag['e_flash_mj_m2']:.2f} MJ/m^2 over tungsten melt bound {E_FLASH_MELT_MJ_M2}")
    return v
