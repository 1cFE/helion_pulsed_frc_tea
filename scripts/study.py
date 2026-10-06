"""Shared runner for the Helion-class pulsed FRC TEA study.

Loads a study config, builds the costingfe model, and runs the rep-rate
sizing path (size_from_power=True): costingfe holds the cited shot fixed,
bisects f_rep against the per-module net target, and solves the integer
module count off the max_f_rep ceiling. Unlike Borealis there is no
geometric closure to write; the framework closes the machine. The ceiling
is therefore the study's firing-rate lever: a grade's granted ceiling is
permission, not obligation, and the design search (scripts/coherent_min.py)
sets max_f_rep at or below it, never above, to fire slower in more modules
where a point's burn needs the longer period.

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
- yield bound and duty: every point carries the burn time its shot
  implies at the point's own burn mix and compression field (constraint
  7), and that burn must fit inside the pulse period at the solved rep
  rate (constraint 8).
- coil mechanics: the magnetic pressure the compression coil cycles to
  on every shot, bounded at the basis coil at every grade, speculation
  included (constraint 9); a higher field is priced as a sensitivity
  only, never as a device.

The compression field (b_center) and the driver bank (e_driver_mj) are
design-search dimensions, graded by the evidence ladder; everything the
burn point sets (breakeven time, per-pulse burnup, compressed flux
volume, coil pressure) is derived from the point's own values through
field_t and e_del_mj, so a scaled field moves its consequences with it.
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
# flux volume is all delivered driver energy stored at the point's
# compression field: V_i = E_del/(B^2/2mu0), about 0.26 m^3 at the basis
# (50 MJ at 22 T). Adiabatic expansion to the chamber volume V_f caps the
# recoverable fraction at 1 - (V_i/V_f)^(2/3), so f_pdv_eff = min(claim,
# cap). The whole volume stroke counts: the vendor's burn-cycle framework
# (Kirtley, DPP24) defines its convergence and expansion ratios on volume,
# radial and axial together.
#
# The compression field and the driver bank are design-search dimensions
# (scripts/coherent_min.py), carried on a point as b_center [T] and
# e_driver_mj [MJ]; a point that carries neither sits at the basis. Both
# are read at one place each (field_t, e_del_mj) so that everything
# derived from the burn point follows them: at beta = 1 and the patent's
# ion temperature the density scales as B^2, so the breakeven time falls
# as B^-2 (constraints 7 and 8), the per-pulse burnup rises as B^2 at the
# vendor's stated dwell (the fuel cycle, the recycle losses and the
# tritium in-pulse burn), the compressed flux volume shrinks as B^-2 and
# grows with the bank (constraint 6), the coil account is priced by
# costingfe at the field (b_center) and the driver account per joule
# (e_driver_mj), and the magnetic pressure the coil must cycle rises as
# B^2 (constraint 9).
B_COMPRESSION_T = 22.0
E_DEL_BASIS_MJ = 50.0
_MU0 = 4e-7 * 3.141592653589793
# The design-basis gain: the solved 128.1 MJ shot on the sourced 50 MJ
# bank (config/baseline.yaml). A scaled bank at the records and
# extrapolation grades keeps this gain, so its shot scales with the bank
# and the burn its shot implies (gain / chi x breakeven time) does not.
GAIN_BASIS = 128.1 / E_DEL_BASIS_MJ

# Constraint 9 (the coil against its own mechanics). Every shot cycles the
# compression coil from zero to the magnetic pressure B^2/2mu0, 1e9 to
# 1e10 times over the book life at the rep rate: about 193 MPa at the 22
# T basis, at or above copper-alloy gigacycle fatigue strengths of 100 to
# 150 MPa, which the ledger carries as an open item on the basis coil
# itself. The bound is evidential, and it is the same at every grade,
# speculation included: the patent's 22 T is the only field with a
# source, its coil already cycles at or above the gigacycle band, and no
# higher fatigue basis is sourced anywhere in this work, so no grade may
# buy a field above the basis. The speculation scan still prices 30, 40
# and 50 T designs (about 1 GPa at 50 T) as a reported sensitivity, each
# labelled as resting on a coil this work cannot price and excluded from
# every device: costingfe's coil account prices conductor mass along the
# expansion adiabat, which shrinks with the compressed flux volume as the
# field rises, and carries no structure term for the pressure, so the
# cost model offers no resistance of its own to the field.
COIL_PRESSURE_BASIS_MPA = B_COMPRESSION_T**2 / (2.0 * _MU0) / 1e6
COIL_FATIGUE_BAND_MPA = (100.0, 150.0)
COIL_PRESSURE_CAP_MPA = {"tier2": COIL_PRESSURE_BASIS_MPA,
                         "tier3": COIL_PRESSURE_BASIS_MPA}

# Constraint 7 (the shot against the plasma energy and the burn time):
# gain <= chi x tau_burn / tau_f. The patent burn point (US 11,469,003 B2
# operating table, tritium-removal column) supplies the density and mix;
# B_COMPRESSION_T and _T_I_CALIB_KEV below are the same point. The vendor's
# stated pulse is "on the order of hundreds of microseconds to
# milliseconds" (helionenergy.com/faq, June 2026 capture in docs/sources/);
# 1 ms is its long edge. x_s 0.7 (chi 0.52) is the midpoint of the
# reconciliation span 0.5 to 0.85 and is the single reference at which
# every point reports the burn time its shot implies.
N_D_PATENT_M3 = 0.75e22
HE3_OVER_D_PATENT = 0.158
VENDOR_PULSE_S = 1e-3
X_S_REFERENCE = 0.7
# Concept-YAML per-pulse burnup pair at the basis field (the patent density
# over the vendor's stated sub-millisecond dwell): the D exposure behind
# the tritium in-pulse burn floor and the He-3 pass behind the recycle
# credit, when a point does not carry its own. Both scale as B^2 with the
# density (burnup_at_field).
_BF_DEFAULT = 1.2e-4
_BF_HE3_DEFAULT = 4.1e-4
_T_I_CALIB_KEV = 70.0
# Constraint 8: a shot's implied burn must fit inside the pulse period. One
# burn section holds one plasmoid, so the next shot cannot be fired while
# the last is still burning. 1.0 is the hard bound and leaves nothing for
# exhaust, refill and recharge, which a duty-cycle analysis would have to
# fit in the remainder.
DUTY_MAX = 1.0

# --- availability from the replacement schedule ----------------------------
# Availability is derived per point, not asserted: the US fission fleet's
# availability outside its planned outages (availability_steady_state) less
# the outage fraction of three planned events, one sourced duration each
# (config/baseline.yaml): a routine maintenance bundle every cycle (the
# fission refueling outage, which carries the fleet's routine work), the
# capacitor-bank swap every cap_shot_lifetime shots at the solved rep rate,
# and the wall-and-coil changeout when the 14-MeV-equivalent fluence
# reaches the dpa tolerance. Shots per calendar year use the steady-state
# availability; the correction of the outage on itself is second order.
SECONDS_PER_YEAR = 8760.0 * 3600.0
MEV_J = 1.602e-13
E_N_DD_MEV = 2.45
E_N_DT_MEV = 14.07
# 1 MW/m^2 of 14 MeV neutron wall load produces about 10 dpa per full-power
# year in Fe-based structure (standard fusion-materials figure); 2.45 MeV
# D-D neutrons displace less per unit energy flux, folded in at 0.4.
DPA_PER_MWY_M2_14MEV = 10.0
DPA_REL_DD = 0.4
STUDY_KEYS = ("availability_steady_state", "outage_days_routine",
              "routine_cycle_yr", "outage_days_bank_swap",
              "outage_days_wall", "wall_dpa_tolerance")


# The decay store's He-3 return. Half the D-D events breed a triton that is
# stored and decays to He-3 (12.33 yr half-life); from startup the return
# builds as (1 - e^-t/tau_T) and substitutes purchased He-3 atom for atom
# (both face the same recycle loop), so purchases per primary event fall
# from (1 - dd_frac) toward (1 - dd_frac) - 0.5 dd_frac and reach zero
# where the mix breeds more than it burns. The fuel account is a
# steady-state annual cost, so the credit enters as the levelized fraction
# of the perpetual purchase that remains over the book life at the rung's
# real rate, applied to the He-3 price (u_he3 x phi). The store's own
# capital, inventory and licensing are priced elsewhere (constraint 4).
T_MEAN_LIFE_YR = 12.33 / math.log(2.0)


def he3_purchase_fraction(dd_frac: float, interest_rate: float,
                          lifetime_yr: float, steps_per_yr: int = 12) -> float:
    """Levelized fraction of the perpetual He-3 purchase that remains once
    the decay store's return is credited; 1.0 when nothing is bred."""
    if dd_frac <= 0.0:
        return 1.0
    need = 1.0 - dd_frac
    ret = 0.5 * dd_frac
    n = max(1, int(round(lifetime_yr * steps_per_yr)))
    dt = lifetime_yr / n
    num = den = 0.0
    for k in range(n):
        t = (k + 0.5) * dt
        frac = max(0.0, 1.0 - ret * (1.0 - math.exp(-t / T_MEAN_LIFE_YR)) / need)
        w = math.exp(-interest_rate * t)
        num += frac * w
        den += w
    return num / den


def field_t(fwd: dict) -> float:
    """The point's compression field [T]: b_center where it carries one,
    the patent basis otherwise."""
    return float(fwd.get("b_center", B_COMPRESSION_T))


def e_del_mj(fwd: dict) -> float:
    """The point's delivered driver energy [MJ]: e_driver_mj where it
    carries one, the sourced Polaris bank otherwise."""
    return float(fwd.get("e_driver_mj", E_DEL_BASIS_MJ))


def density_scale(b_t: float) -> float:
    """n / n_patent at beta = 1 and the patent's ion temperature: B^2."""
    return (b_t / B_COMPRESSION_T) ** 2


def n_d_at_field(b_t: float) -> float:
    """The patent's deuterium density scaled to the field [m^-3]."""
    return N_D_PATENT_M3 * density_scale(b_t)


def burnup_at_field(fwd: dict) -> tuple[float, float]:
    """(burn_fraction, burn_fraction_he3) the point burns per pulse: its
    own where it carries them, else the basis pair scaled as B^2 with the
    density at the vendor's stated dwell."""
    from mix import _sv_ratio

    s = density_scale(field_t(fwd))
    bf = float(fwd.get("burn_fraction", _BF_DEFAULT * s))
    if "burn_fraction_he3" in fwd:
        bf_he3 = float(fwd["burn_fraction_he3"])
    elif "burn_fraction" in fwd:
        # Both species' per-pass burn fractions come from the same n tau,
        # so a point that carries only the D burnup implies the He-3 one
        # through the reactivity ratio at the calibration temperature.
        bf_he3 = bf * _sv_ratio(_T_I_CALIB_KEV)
    else:
        bf_he3 = _BF_HE3_DEFAULT * s
    return bf, bf_he3


def coil_pressure_mpa(b_t: float) -> float:
    """Magnetic pressure B^2/2mu0 [MPa], the stress the compression coil
    cycles to on every shot."""
    return b_t**2 / (2.0 * _MU0) / 1e6


def chi_from_xs(x_s: float) -> float:
    """Plasma-thermal share of the in-tank driver energy at peak compression.

    FRC radial equilibrium with the average-beta theorem <beta> = 1 - x_s^2/2
    (x_s = separatrix/coil radius ratio): plasma internal energy
    1.5 <beta> (B^2/2mu0) V_s against annulus field energy
    (B^2/2mu0)(V_c - V_s). End-region field and coil overhang lower this;
    profile and kinetic corrections are tens of percent."""
    beta = 1.0 - 0.5 * x_s**2
    u_p = 1.5 * beta * x_s**2
    return u_p / (u_p + 1.0 - x_s**2)


def breakeven_time_s(b_t: float = None, t_i_kev: float = None,
                     n_d_m3: float = N_D_PATENT_M3,
                     he3_over_d: float = HE3_OVER_D_PATENT,
                     te_over_ti: float = 1.0) -> float:
    """The plasma's energy breakeven time at the burn point: its energy
    density at beta = 1, 1.5 B^2/2mu0, over its fusion power density
    (D-He3 plus both D-D branches, Bosch-Hale rates, total reaction
    energy). n_d_m3 is the ion density with thermalized electrons; at fixed
    field, colder electrons admit (2 + 3r)/((1 + r) + (1 + 2r) te_over_ti)
    times that density (r = He3/D), which enters the power squared."""
    from costingfe.layers.physics import Q_DD_NHE3, Q_DD_PT, Q_DHE3
    from costingfe.layers.reactivity import sigv_dd_n, sigv_dd_p, sigv_dhe3

    b_t = B_COMPRESSION_T if b_t is None else b_t
    t_i_kev = _T_I_CALIB_KEV if t_i_kev is None else t_i_kev
    r = he3_over_d
    n_d = n_d_m3 * (2.0 + 3.0 * r) / ((1.0 + r) + (1.0 + 2.0 * r) * te_over_ti)
    n_he3 = r * n_d
    p_fus = (n_d * n_he3 * float(sigv_dhe3(t_i_kev)) * Q_DHE3
             + 0.5 * n_d * n_d * (float(sigv_dd_n(t_i_kev)) * Q_DD_NHE3
                                  + float(sigv_dd_p(t_i_kev)) * Q_DD_PT)) * MEV_J
    u = 1.5 * b_t**2 / (2.0 * _MU0)
    return u / p_fus


def breakeven_time_at_point_s(fwd: dict) -> float:
    """The breakeven time of the plasma this point actually burns.

    The burn point is the patent's at the point's own field: the ion
    temperature stays the patent's, the density scales as B^2 at beta = 1,
    so the breakeven time falls as B^-2. What changes with the burn mix is
    the composition, and with it the fusion power density. The composition
    counted is the one the model's own fuel accounting implies: purchased
    He-3 plus the bred He-3 that recycles and burns at f_He3_eff (at the
    point's own per-pulse burnup), which is why a D-rich point is less
    power-dense than the knob's naive He3/D map alone would say.
    """
    from mix import f_he3_eff, he3_over_d_from_burn

    dd = float(fwd["dhe3_dd_frac"])
    b_t = field_t(fwd)
    _, bf_he3 = burnup_at_field(fwd)
    f_he3 = f_he3_eff(bf_he3, float(fwd["fuel_recovery"]))
    return breakeven_time_s(b_t=b_t, n_d_m3=n_d_at_field(b_t),
                            he3_over_d=he3_over_d_from_burn(dd, f_he3))


def breakeven_time_dt_s(b_t: float, t_i_kev: float) -> float:
    """The same breakeven time for a balanced D-T plasma with thermalized
    electrons at beta = 1: the cross-check against Slough (2025, Nucl.
    Fusion 65 106019), whose compact D-T reactor quotes a gain of 9.1 on the
    FRC energy over a 2 to 5 ms transit at 34.8 T and the optimum 15 keV."""
    from costingfe.layers.physics import Q_DT
    from costingfe.layers.reactivity import sigv_dt

    p_b = b_t**2 / (2.0 * _MU0)
    n_i = p_b / (2.0 * t_i_kev * 1e3 * 1.602e-19)  # n_e = n_i, T_e = T_i
    n_d = n_t = 0.5 * n_i
    p_fus = n_d * n_t * float(sigv_dt(t_i_kev)) * Q_DT * MEV_J
    return 1.5 * p_b / p_fus


def yield_bound_mj(e_del_mj: float, x_s: float, tau_burn_s: float,
                   tau_f_s: float = None) -> float:
    """Largest shot yield the plasma can return in a burn of tau_burn_s:
    chi(x_s) E_del tau_burn / tau_f."""
    tau_f_s = breakeven_time_s() if tau_f_s is None else tau_f_s
    return chi_from_xs(x_s) * e_del_mj * tau_burn_s / tau_f_s


def implied_burn_s(yield_mj: float, e_del_mj: float, x_s: float,
                   tau_f_s: float = None) -> float:
    """Burn time a shot of yield_mj implies from a bank of e_del_mj: the
    inverse of yield_bound_mj."""
    tau_f_s = breakeven_time_s() if tau_f_s is None else tau_f_s
    return yield_mj / (chi_from_xs(x_s) * e_del_mj) * tau_f_s


def duty_bound_rate_hz(fwd: dict, e_del_mj: float) -> float:
    """The highest firing rate at which the burn a point's shot implies
    (constraint 7, at the reference x_s and the point's own mix) fits the
    pulse period (constraint 8): DUTY_MAX over the implied burn. The design
    search fires at or below min(granted ceiling, this)."""
    tau = implied_burn_s(float(fwd["yield_per_shot_mj"]), e_del_mj,
                         X_S_REFERENCE, breakeven_time_at_point_s(fwd))
    return DUTY_MAX / tau


def wall_load_14mev_equivalent(result) -> float:
    """14-MeV-equivalent neutron wall load [MW/m^2] per module from the
    model's own reaction rates: the D-D 2.45 MeV flux at DPA_REL_DD, the
    D-T branch (in-pulse tritium burn, dhe3_f_T) at full weight."""
    from tritium_burn import reaction_rates  # tritium_burn imports this module

    rr = reaction_rates(result)
    f_t = float(result.params.get("dhe3_f_T", 0.0))
    p_n_dd_mw = 0.5 * rr["dd"] * E_N_DD_MEV * MEV_J / 1e6
    p_n_dt_mw = f_t * 0.5 * rr["dd"] * E_N_DT_MEV * MEV_J / 1e6
    return (p_n_dt_mw + DPA_REL_DD * p_n_dd_mw) / wall_area_m2(result.params)


def replacement_intervals_yr(cap_shot_lifetime, f_rep_hz, wall_load_eq,
                             dpa_tolerance, a0):
    """(bank-swap, wall-changeout) intervals in calendar years."""
    t_bank = cap_shot_lifetime / (f_rep_hz * SECONDS_PER_YEAR * a0)
    dpa_per_fpy = DPA_PER_MWY_M2_14MEV * wall_load_eq
    t_wall = dpa_tolerance / dpa_per_fpy / a0 if dpa_per_fpy > 0 else math.inf
    return t_bank, t_wall


def outage_fractions(outage_days_routine, routine_cycle_yr,
                     outage_days_bank, t_bank_yr,
                     outage_days_wall, t_wall_yr) -> dict:
    """Fraction of calendar time lost to each planned event type."""
    return dict(
        routine=outage_days_routine / (365.0 * routine_cycle_yr),
        bank=outage_days_bank / (365.0 * t_bank_yr),
        wall=outage_days_wall / (365.0 * t_wall_yr),
    )


def derived_availability(a0, outage_days_routine, routine_cycle_yr,
                         outage_days_bank, t_bank_yr,
                         outage_days_wall, t_wall_yr) -> float:
    f = outage_fractions(outage_days_routine, routine_cycle_yr,
                         outage_days_bank, t_bank_yr,
                         outage_days_wall, t_wall_yr)
    return a0 * (1.0 - sum(f.values()))


def replacement_schedule(result, study: dict) -> dict:
    """Availability and the two replacement intervals of a sized machine."""
    a0 = study["availability_steady_state"]
    p = result.params
    gamma = wall_load_14mev_equivalent(result)
    t_bank, t_wall = replacement_intervals_yr(
        float(p["cap_shot_lifetime"]), float(p["f_rep"]), gamma,
        study["wall_dpa_tolerance"], a0)
    f = outage_fractions(study["outage_days_routine"], study["routine_cycle_yr"],
                         study["outage_days_bank_swap"], t_bank,
                         study["outage_days_wall"], t_wall)
    return dict(
        availability=a0 * (1.0 - sum(f.values())),
        t_bank_yr=t_bank,
        t_wall_yr=t_wall,
        wall_load_14mev_eq_mw_m2=gamma,
        outage_routine=f["routine"],
        outage_bank=f["bank"],
        outage_wall=f["wall"],
    )


def compressed_volume_m3(fwd: dict) -> float:
    """V_i = E_del/(B^2/2mu0) at the point's own bank and field."""
    return e_del_mj(fwd) * 1e6 / (field_t(fwd) ** 2 / (2 * _MU0))


def f_pdv_cap(fwd: dict, model: CostModel) -> float:
    ed = model._eng_defaults
    v_i = compressed_volume_m3(fwd)
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


# --- the four devices the writeup prices -----------------------------------
# One machine per evidence grade. records, extrap and spec are the coherent
# design-search optima (scripts/coherent_min.py); helion is the vendor
# configuration on the design basis. The search chooses the compression
# field and the driver bank (graded: both at the basis at records, the
# bank doubled at extrapolations, the bank to 200 MJ at speculation; the
# field is scanned to 50 T at speculation and bounded at the basis by
# the coil at every grade, so every device sits at 22 T), the shot gain
# (free at speculation only), the burn mix, the chamber, the wall class
# and the firing rate together, each mix on its bremsstrahlung floor,
# under constraint 8 (the burn must fit the pulse period, a cap on one
# burn section's fusion power of chi E_del / tau_f, which rises with the
# bank) and constraint 9 (the coil's magnetic pressure at the basis). The
# rate enters as max_f_rep: a grade's granted ceiling (1 Hz at the design
# basis and records, 3 Hz at extrapolations, 10 Hz at speculation) is
# permission, not obligation, and each optimized device carries the
# ceiling the search chose, the duty-bound rate of its own burn (1 /
# tau_burn, rounded down to the thousandth) at or below the grant, never
# above, so costingfe builds it in the fewest modules whose rate fits
# that burn:
# - records: the basis field and bank, Helion's 128.1 MJ shot at dd_frac
#   0.85 in 25 modules of 10 m x 0.75 m at 0.985 Hz (duty 0.999), under
#   the 1 Hz grant;
# - extrapolations: the basis field with the doubled bank (100 MJ, 256 MJ
#   shots at the design-basis gain) at dd_frac 0.80 in 6 modules of 10 m
#   x 1.5 m at 1.56 Hz, the fewest whose rate fits its 0.62 s burn, under
#   the 3 Hz grant; the bank is worth 1.0 $/MWh against the 12 modules of
#   10 m x 0.75 m the sourced bank needs;
# - speculation: the basis field with a 200 MJ bank (four times Polaris),
#   512 MJ shots at the design-basis gain (the freed gain buys nothing:
#   the gain-3 shot in the same chamber reads within 0.01 $/MWh) at
#   dd_frac 0.70 in 2 modules of 15 m x 1.5 m at 1.67 Hz, the fewest
#   whose rate fits its 0.51 s burn (duty 0.85), under the 10 Hz grant,
#   the panel wall at 91% of its steady-flux limit; the bank is worth 0.7
#   $/MWh against the 7 modules of 10 m x 0.75 m the sourced bank needs
#   (12.4). A field above the basis is a sensitivity the coil bound
#   excludes from every device: the best design the coil alone excludes
#   reads 10.9 at 30 T, 10.5 at 40 T and 10.2 at 50 T (8.6, 8.2 and 7.9
#   at the park), a single 30 m x 1.5 m module on a coil cycled to 358 to
#   995 MPa that this work cannot price.
# Every device is a panel-wall machine. The same module tripled makes the
# 3 GWe park, so no size_overrides remain; the slot is kept for a park that
# needs a different shot or chamber. Every script and test builds its
# forward dict from here, so a moved optimum is a one-place change.
DEVICES = {
    "records": dict(
        configs=("best_case.yaml",),
        overrides=dict(dhe3_dd_frac=0.85, f_rad=f_rad_floor(0.85),
                       chamber_length=10.0, plasma_t=0.75, r_bore=0.85,
                       fw_class="panel", max_f_rep=0.986),
        size_overrides={},
    ),
    "helion": dict(configs=(), overrides={}, size_overrides={}),
    "extrap": dict(
        configs=("best_case.yaml", "tier2.yaml"),
        overrides=dict(dhe3_dd_frac=0.8, f_rad=f_rad_floor(0.8),
                       e_driver_mj=100.0, yield_per_shot_mj=GAIN_BASIS * 100.0,
                       chamber_length=10.0, plasma_t=1.5, r_bore=1.6,
                       fw_class="panel", max_f_rep=1.613),
        size_overrides={},
    ),
    "spec": dict(
        configs=("best_case.yaml", "tier2.yaml", "tier3.yaml"),
        overrides=dict(dhe3_dd_frac=0.7, f_rad=f_rad_floor(0.7),
                       e_driver_mj=200.0, yield_per_shot_mj=GAIN_BASIS * 200.0,
                       chamber_length=15.0, plasma_t=1.5, r_bore=1.6,
                       fw_class="panel", max_f_rep=1.952),
        size_overrides={},
    ),
}
# The deuterium-rich end of the mix grid (dd_frac 0.85, the mix that
# breeds more He-3 than it burns): its best design at each grade under all
# nine constraints, the rate included. At the records grade it is the
# device itself; at extrapolations it sits 0.5 $/MWh behind the device's
# 0.80 mix, in one more module at a lower rate; at speculation it sits
# 0.4 behind the device's 0.70 mix, on the doubled bank in 5 modules of
# 10 m x 1.0 m at 1.46 Hz, 99% of the duty bound. These designs carry the
# largest tritium stores, so the tritium-store analysis
# (scripts/tritium_burn.py, scripts/burnup_scan.py) and the duty audit
# across x_s (scripts/yield_bound.py) price them beside the devices.
D_RICH_DEVICES = {
    "records": DEVICES["records"],
    "extrap": dict(
        configs=("best_case.yaml", "tier2.yaml"),
        overrides=dict(dhe3_dd_frac=0.85, f_rad=f_rad_floor(0.85),
                       e_driver_mj=100.0, yield_per_shot_mj=GAIN_BASIS * 100.0,
                       chamber_length=10.0, plasma_t=1.5, r_bore=1.6,
                       fw_class="panel", max_f_rep=1.473),
        size_overrides={},
    ),
    "spec": dict(
        configs=("best_case.yaml", "tier2.yaml", "tier3.yaml"),
        overrides=dict(dhe3_dd_frac=0.85, f_rad=f_rad_floor(0.85),
                       e_driver_mj=100.0, yield_per_shot_mj=GAIN_BASIS * 100.0,
                       chamber_length=10.0, plasma_t=1.0, r_bore=1.1,
                       fw_class="panel", max_f_rep=1.473),
        size_overrides={},
    ),
}
DEVICE_ORDER = (
    ("records", "citable records"),
    ("helion", "Helion's requirements"),
    ("extrap", "extrapolations"),
    ("spec", "speculation"),
)
PLANT_SIZES_MWE = (1000.0, 3000.0)


def device_fwd(name: str, net_electric_mw: float,
               devices: dict = DEVICES) -> tuple[dict, dict]:
    """(baseline cfg, forward dict) for one of the four devices at a plant
    size, or for the deuterium-rich end's design when
    devices=D_RICH_DEVICES. Sizes other than PLANT_SIZES_MWE have no device
    definition and raise KeyError."""
    if net_electric_mw not in PLANT_SIZES_MWE:
        raise KeyError(f"no device definition at {net_electric_mw} MWe")
    cfg = load_config("baseline.yaml")
    fwd = dict(cfg["forward"])
    dev = devices[name]
    for c in dev["configs"]:
        apply_records(fwd, c)
    fwd.update(dev["overrides"])
    fwd.update(dev["size_overrides"].get(net_electric_mw, {}))
    fwd["net_electric_mw"] = net_electric_mw
    return cfg, fwd


def run(model: CostModel, fwd: dict, tritium_adder: bool = True):
    """Forward with rep-rate sizing; returns (result, diagnostics dict).

    A probe forward sizes the machine (rep rate, module count, reaction
    rates); from it the runner derives availability (replacement_schedule)
    unless the caller pins `availability` explicitly, and raises the
    fuel-handling account C220500 by the tritium-plant adder when the burn
    mix is D-rich (dd_frac >= threshold; cost_overrides replace rather than
    add, hence the probe), and credits the decay store's He-3 return by
    scaling the He-3 price by he3_purchase_fraction (he3_decay_return=False
    restores the perpetual purchase). The study-only keys (STUDY_KEYS,
    he3_decay_return) never reach the model, which rejects unknown
    parameters. Captures the model's audit warnings and computes the wall
    metrics the coherence checks need.
    """
    fwd = dict(fwd)
    decay_return = fwd.pop("he3_decay_return", True)
    study = {k: fwd.pop(k) for k in STUDY_KEYS if k in fwd}
    phi = (he3_purchase_fraction(fwd.get("dhe3_dd_frac", 0.131),
                                 fwd["interest_rate"], fwd["lifetime_yr"])
           if decay_return else 1.0)
    fwd["u_he3"] = fwd.get("u_he3", float(model.cc.u_he3)) * phi
    derive = "availability" not in fwd
    if derive:
        missing = [k for k in STUDY_KEYS if k not in study]
        if missing:
            raise KeyError(
                f"availability derivation needs {missing} in the forward "
                f"dict (config/baseline.yaml carries them)")
    cap = f_pdv_cap(fwd, model)
    f_pdv_claim = fwd.get("f_pdv", float(model.cc.f_pdv))
    fwd["f_pdv"] = min(f_pdv_claim, cap)
    # The burn point follows the field: the per-pulse burnup pair the model
    # prices (fuel recycle losses, the bred-He-3 credit, exhaust pumping)
    # is the basis pair scaled as B^2 unless the point carries its own.
    fwd["burn_fraction"], fwd["burn_fraction_he3"] = burnup_at_field(fwd)

    # The probe sizes the machine; availability does not enter the sizing,
    # so the probe runs at the steady-state value when deriving.
    probe_fwd = (dict(fwd, availability=study["availability_steady_state"])
                 if derive else fwd)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        probe = model.forward(size_from_power=True, **probe_fwd)

    schedule = {}
    if derive:
        schedule = replacement_schedule(probe, study)
        fwd["availability"] = schedule["availability"]

    overrides = None
    tritium_musd = 0.0
    if tritium_adder and fwd.get("dhe3_dd_frac", 0.131) >= DD_FRAC_TRITIUM_THRESHOLD:
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
        "he3_purchase_fraction": phi,
        "tau_burn_implied_s": implied_burn_s(
            float(result.params["yield_per_shot_mj"]),
            float(result.params["e_driver_mj"]), X_S_REFERENCE,
            breakeven_time_at_point_s(fwd)),
        "b_center_t": field_t(fwd),
        "e_driver_mj": e_del_mj(fwd),
        "yield_per_shot_mj": float(result.params["yield_per_shot_mj"]),
        "burn_fraction": fwd["burn_fraction"],
        "coil_pressure_mpa": coil_pressure_mpa(field_t(fwd)),
        "p_fus_module_mw": float(pt.p_fus),
        "tritium_adder_musd": tritium_musd,
        "availability": float(result.params["availability"]),
        "t_bank_yr": schedule.get("t_bank_yr", float("nan")),
        "t_wall_yr": schedule.get("t_wall_yr", float("nan")),
        "wall_load_14mev_eq_mw_m2": schedule.get("wall_load_14mev_eq_mw_m2", float("nan")),
        "outage_routine": schedule.get("outage_routine", float("nan")),
        "outage_bank": schedule.get("outage_bank", float("nan")),
        "outage_wall": schedule.get("outage_wall", float("nan")),
        "warnings": sorted({str(w.message) for w in caught}),
    }
    return result, diag


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
    bf, _ = burnup_at_field(fwd)
    f_t_floor = f_t_from_burnup(bf, _T_I_CALIB_KEV)
    if fwd.get("dhe3_f_T", 0.0) < f_t_floor - F_T_FLOOR_TOL:
        v.append(
            f"dhe3_f_T {fwd.get('dhe3_f_T', 0.0):.3f} sits below the "
            f"thermalized in-pulse burn floor {f_t_floor:.3f} at this "
            f"burnup: coherent only under prompt MeV-triton loss")
    p_coil = coil_pressure_mpa(field_t(fwd))
    if p_coil > COIL_PRESSURE_CAP_MPA[tier] * (1 + 1e-9):
        v.append(
            f"coil pressure {p_coil:.0f} MPa at {field_t(fwd):.0f} T exceeds "
            f"the {tier} coil bound, the basis coil at "
            f"{COIL_PRESSURE_BASIS_MPA:.0f} MPa ({B_COMPRESSION_T:.0f} T)")
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
    duty = diag["tau_burn_implied_s"] * diag["f_rep_hz"]
    if duty > DUTY_MAX + 1e-9:
        v.append(
            f"duty {duty:.2f}: the implied burn "
            f"{diag['tau_burn_implied_s']:.2f} s exceeds the "
            f"{1.0 / diag['f_rep_hz']:.2f} s between shots at "
            f"{diag['f_rep_hz']:.2f} Hz")
    return v


def lcoe_segments(result) -> dict:
    """The three parts of a device's LCOE [$ /MWh], an exact partition of
    the model's own figure, LCOE = (CAS90 + CAS70 + CAS80) / annual MWh:
    the overnight cost recovered straight-line over the book life, the
    cost of money (CAS90 less that: interest during construction and on
    the capital), and operating costs (CAS70 O&M with scheduled
    replacement, CAS80 fuel). The annual MWh is taken from the model's own
    ratio so the partition is exact whatever derate the model applies."""
    c, p = result.costs, result.params
    annual_musd = float(c.cas90) + float(c.cas70) + float(c.cas80)
    usd_per_mwh_per_musd = float(c.lcoe) / annual_musd
    straight_musd = float(c.overnight_cost) / float(p["lifetime_yr"])
    return dict(
        straight_line=straight_musd * usd_per_mwh_per_musd,
        cost_of_money=(float(c.cas90) - straight_musd) * usd_per_mwh_per_musd,
        operating=(float(c.cas70) + float(c.cas80)) * usd_per_mwh_per_musd,
    )
