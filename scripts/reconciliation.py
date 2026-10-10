"""What the model cannot price at the coherent minima, and what it overprices.

Runs the tier-2 and tier-3 coherent-minimum points (from coherent_min.py)
and reports, on top of each:

ADDERS (model gaps the red-team review identified, still open in costingfe):
- Switch-stack duty repricing: delta_switch prices the stack at 6% of the
  cap bank (single-shot practice); a stack commuting GW-class average power
  continuously is HVDC-valve class, order 100 M$/GW of commutated power.
- Tritium-plant band: the D-rich branch carries a 200 M$ point adder in the
  stack (study.py); the band is 100-300.
- Driver-thermalization derate: the physics path recovers the entire
  delivered driver energy at flat eta_dec (p_dee = eta_dec*(p_driver +
  p_pdv) - p_driver), as if it all stayed in field form. In
  merging-compression the plasma-thermal share chi returns only through
  the expansion channel at f_pdv. chi is not free: at peak compression
  the FRC equilibrium pins it via the average-beta theorem
  (<beta> = 1 - x_s^2/2), giving chi(x_s) = 1.5<beta>x_s^2 /
  (1.5<beta>x_s^2 + 1 - x_s^2); the priced band chi = 0.3/0.5/0.7 is
  x_s = 0.5/0.7/0.85, bracketing the realistic separatrix-to-coil
  ratios (fat FRCs are high-chi machines). Extra recirculating loss =
  eta_dec * chi * (1 - f_pdv) * p_driver, priced as a net-output
  haircut. The Polaris shot triplet (vacuum / plasma no-burn / burn)
  separates eta_dec, chi*(1 - f_pdv), and the fusion composite.

CREDITS (model conservatisms):
- Thermal bottoming: the machine basis discards p_th (eta_th = 0); a
  low-grade bottoming cycle (eta_th 0.30) on the rejected stream is a real
  design option the basis excludes. Run in-model as an add-back scenario.

Two former entries are now inside costingfe and priced on every quoted
number rather than reconciled here: the CAS72 replacement event includes
the shot-cycled recovery store and switch (C220109_cap / C220109_switch),
and the store markup is sized for the physics-returned energy
(f_pdv, 1 - f_rad).

Anatomy: top capital accounts at each point, so the writeup can name what
carries the floor instead of gesturing at it.
"""
import warnings

from study import (
    B_COMPRESSION_T,
    DEVICES,
    OUTPUT_DIR,
    apply_records,
    build_model,
    chi_from_xs,
    coil_pressure_mpa,
    duty_bound_rate_hz,
    e_del_mj,
    field_t,
    load_config,
    run,
)

# Coherent-minimum design points (scripts/coherent_min.py argmin rows).
POINTS = {
    "tier2_min": dict(tier_cfgs=DEVICES["extrap"]["configs"],
                      overrides=DEVICES["extrap"]["overrides"]),
    "tier3_min": dict(tier_cfgs=DEVICES["spec"]["configs"],
                      overrides=DEVICES["spec"]["overrides"]),
}

HVDC_MUSD_PER_GW = 100.0  # continuous-commutation silicon, HVDC valve class
TRITIUM_BAND_MUSD = (100.0, 300.0)
TRITIUM_POINT_MUSD = 200.0
ETA_TH_BOTTOMING = 0.30

# Slough (2025, Nucl. Fusion 65 106019, eq. 18): in a flux-conserving
# expansion chamber the ejected FRC comes to rest in equilibrium at a
# radius ratio x_s, retaining 1.5 p V of thermal energy against the field
# it has compressed, so the recoverable share is (1 - x_s^2)/(2.5 - x_s^2),
# at most 0.4. That is the co-founder's own recovery topology and his
# published view that an FRC does not free-expand; the study's higher
# f_pdv assumes the compression coil is discharged under the expanding
# plasma. Priced here as a risk row, not enforced.
F_PDV_CEILING_SLOUGH = 0.4


def f_pdv_ceiling_risk(model, fwd, diag, ceiling=F_PDV_CEILING_SLOUGH):
    """(LCOE, delta, effective f_pdv) with f_pdv held at the
    ceiling; study.run keeps min(claim, adiabatic cap), so a claim
    below the cap sticks."""
    _, d = run(model, dict(fwd, f_pdv=ceiling))
    return d["lcoe"], d["lcoe"] - diag["lcoe"], d["f_pdv_eff"]



def crf(i, n):
    return i * (1 + i) ** n / ((1 + i) ** n - 1)


# costingfe's CAS22 detail is per module for the C2201xx reactor accounts
# and plant-wide from C220200 up (C220000 = per-module equipment x n_mod
# + labor at the multi-unit factor + plant-wide), so the anatomy scales
# the reactor accounts by the module count and the fuel-handling account
# (with the tritium adder study.run charges once) not at all.
PER_MODULE_PREFIX = "C2201"


def anatomy_items(result) -> list[tuple[str, float]]:
    """The capital accounts carrying a device, as (label, plant M$)."""
    d22 = {k: float(v) for k, v in result.cas22_detail.items()}
    n_mod = int(result.solved_n_mod)
    c = result.costs

    def acct(key):
        return d22[key] * (n_mod if key.startswith(PER_MODULE_PREFIX) else 1)

    length = float(result.params["chamber_length"])
    return [
        ("buildings (CAS21)", float(c.cas21)),
        ("CAS50 incl. decommissioning", float(c.cas50)),
        ("fuel handling + tritium plant (C220500)", acct("C220500")),
        ("heat rejection + electrical plant (CAS24-26)",
         float(c.cas24) + float(c.cas25) + float(c.cas26)),
        ("vacuum + exhaust (C220106)", acct("C220106")),
        (f"first wall, {n_mod} x {length:.0f} m chambers (C220101)"
         if n_mod > 1 else f"first wall, {length:.0f} m chamber (C220101)",
         acct("C220101")),
        ("DEC power electronics (C220109)", acct("C220109")),
        ("coils (C220103)", acct("C220103")),
        ("driver capacitor bank (C220107)", acct("C220107")),
    ]


def _model_fwd(fwd, b_t):
    """The device's forward dict at another field, with the study-only keys
    the model rejects removed and the burnup pair at that field, for a
    costing-only probe (no availability derivation)."""
    from study import STUDY_KEYS, burnup_at_field

    f = {k: v for k, v in fwd.items() if k not in STUDY_KEYS and k != "he3_decay_return"}
    f["b_center"] = b_t
    f["burn_fraction"], f["burn_fraction_he3"] = burnup_at_field(f)
    f.setdefault("availability", fwd["availability_steady_state"])
    return f


def analyze(label, spec):
    base_cfg = load_config("baseline.yaml")
    model = build_model(base_cfg)
    fwd = dict(base_cfg["forward"])
    for cfg in spec["tier_cfgs"]:
        apply_records(fwd, cfg)
    fwd.update(spec["overrides"])

    result, diag = run(model, fwd)
    p = result.params
    pt = result.power_table
    d22 = {k: float(v) for k, v in result.cas22_detail.items()}
    n_mod = diag["n_mod"]
    i, n = fwd["interest_rate"], fwd["lifetime_yr"]
    avail = float(result.params["availability"])
    mwh_per_year = 1000.0 * 8760.0 * avail  # plant MWh/yr at 1 GWe net

    print(f"\n=== {label}: LCOE {diag['lcoe']:.1f} $/MWh, {field_t(fwd):.0f} T, "
          f"{e_del_mj(fwd):.0f} MJ bank, {float(p['yield_per_shot_mj']):.0f} MJ shots, "
          f"n_mod {n_mod}, f_rep {diag['f_rep_hz']:.2f} Hz, "
          f"{diag['capital_per_kw']:.0f} $/kW ===")

    # --- anatomy: top CAS22 accounts (C2201xx per module, the rest
    # plant-wide) + plant accounts ---
    top = sorted(d22.items(), key=lambda kv: -kv[1])[:8]
    print("  top CAS22 accounts (M$; C2201xx per module, C2202xx and up plant-wide):",
          ", ".join(f"{k} {v:.0f}" for k, v in top if v > 0.5))
    c = result.costs
    for name in ("cas10", "cas21", "cas22", "cas23", "cas24", "cas25",
                 "cas26", "cas27", "cas28", "cas29", "cas30", "cas40",
                 "cas50", "cas60", "cas70", "cas80", "cas90"):
        v = getattr(c, name, None)
        if v is not None and float(v) > 1.0:
            print(f"    {name}: {float(v):.0f} M$")
    # Levelized weight of each capital account: the model's own annualized
    # capital (CAS90, at the rung's rate and book life) per M$ of total
    # capital, per MWh, so the writeup's anatomy table can quote $/MWh.
    lev = float(c.cas90) / float(c.total_capital) * 1e6 / mwh_per_year
    print(f"  levelized capital: {lev * 1e3:.3f} $/MWh per G$ of total capital "
          f"(CAS90 {float(c.cas90):.1f} M$/yr over {mwh_per_year / 1e6:.2f} TWh/yr)")
    for label, musd in anatomy_items(result):
        print(f"    {label:<46} {musd:7.0f} M$  {musd * lev:5.2f} $/MWh")
    print(f"    {'of which per-pulse exhaust pumping (C220106_pump)':<46} "
          f"{d22['C220106_pump'] * n_mod:7.0f} M$")
    print(f"    {'of which the tritium-plant adder':<46} "
          f"{diag['tritium_adder_musd']:7.0f} M$")
    # The wall-and-coil replacement event against the reactor account's
    # own capital service: below this interval the levelized replacement
    # (the model's closed form, as burnup_scan.py prices it) outspends
    # CAS22 x CRF, and the reactor line is replacement-dominated.
    from costingfe.layers.economics import levelized_replacement_cost

    event = (d22["C220101"] + d22["C220103"]) * n_mod

    def replacement_threshold_yr(rate):
        service = float(c.cas22) * crf(rate, n)
        lo, hi = 0.25, 400.0
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if float(levelized_replacement_cost(event, mid, rate, n)) > service:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    print(f"  wall-and-coil event (C220101 + C220103) {event:.0f} M$ against the "
          f"reactor account {float(c.cas22):.0f} M$: replacement outspends the "
          f"account's capital service below an interval of "
          f"{replacement_threshold_yr(i):.1f} yr at {i:.0%} real "
          f"({replacement_threshold_yr(0.07):.1f} yr at 7%)")
    print(f"    {'O&M (CAS70)':<46} {float(c.cas70):7.0f} M$/yr  "
          f"{float(c.cas70) * 1e6 / mwh_per_year:5.2f} $/MWh")
    print(f"    {'fuel (CAS80)':<46} {float(c.cas80):7.0f} M$/yr  "
          f"{float(c.cas80) * 1e6 / mwh_per_year:5.2f} $/MWh")
    print(f"    {'annualized capital, all-in (CAS90)':<46} {float(c.cas90):7.0f} M$/yr  "
          f"{float(c.cas90) * 1e6 / mwh_per_year:5.2f} $/MWh")

    # --- adders ---
    f_rep = diag["f_rep_hz"]
    f_ch = 1.0 - float(pt.p_neutron) / float(pt.p_fus)
    eta_dec, f_pdv, f_rad = p["eta_dec"], p["f_pdv"], p["f_rad"]
    delta_switch = d22.get("C220109_switch", 0.0)

    p_driver = float(p["e_driver_mj"]) * f_rep  # per-module average [MW]
    p_commutated_gw = (p_driver + eta_dec * f_pdv
                      * (1 - f_rad) * f_ch * float(pt.p_fus)) * n_mod / 1e3
    switch_capital_delta = max(
        HVDC_MUSD_PER_GW * p_commutated_gw - delta_switch * n_mod, 0.0)
    adder_switch_repricing = switch_capital_delta * crf(i, n) * 1e6 / mwh_per_year

    dd = p.get("dhe3_dd_frac", 0.131)
    tri_lo, tri_hi = (
        ((TRITIUM_BAND_MUSD[0] - TRITIUM_POINT_MUSD) * crf(i, n) * 1e6 / mwh_per_year,
         (TRITIUM_BAND_MUSD[1] - TRITIUM_POINT_MUSD) * crf(i, n) * 1e6 / mwh_per_year)
        if dd > 0.5 else (0.0, 0.0)
    )

    print(f"  ADDER switch stack at HVDC class ({p_commutated_gw:.2f} GW "
          f"commutated): +{adder_switch_repricing:.2f} $/MWh")

    p_driver_plant = p_driver * n_mod
    chi_adders = {
        round(chi_from_xs(xs), 2): diag["lcoe"]
        * (eta_dec * chi_from_xs(xs) * (1.0 - f_pdv) * p_driver_plant)
        / 1000.0
        for xs in (0.5, 0.7, 0.85)
    }
    adder_driver_thermal = chi_adders[round(chi_from_xs(0.7), 2)]
    print(f"  ADDER driver-thermalization derate (plant driver "
          f"{p_driver_plant:.0f} MW; chi(x_s 0.5/0.7/0.85) = "
          + "/".join(f"{c:.2f}" for c in chi_adders) + "): "
          + " / ".join(f"+{v:.2f}" for v in chi_adders.values())
          + " $/MWh")
    if dd > 0.5:
        print(f"  ADDER tritium-plant band vs 200 M$ point: "
              f"{tri_lo:+.2f} / {tri_hi:+.2f} $/MWh")

    # --- compression-field risk (the dominant open band) ---
    # The device's field is a graded design choice; every consequence of
    # the burn point follows it (study.py). Priced here: the field below
    # the device's own, with the rate ceiling re-solved at the duty bound of
    # the longer burn (so the plant needs more modules) and the per-pulse
    # burnup falling as B^2 (so the recovery nines bind harder); and, where
    # the device sits above the 22 T basis, the same design reverted to the
    # basis field, the grade's field entry withdrawn (the coil that would
    # deliver the granted field is neither designed nor priced, so the
    # basis-field reading is the device without that grant).
    lcoe_c, delta_c, f_pdv_c = f_pdv_ceiling_risk(model, fwd, diag)
    print(f"  RISK f_pdv at Slough's flux-conserver ceiling "
          f"(f_pdv {f_pdv_c:.2f} against {diag['f_pdv_eff']:.2f}): "
          f"LCOE {lcoe_c:.1f} ({delta_c:+.1f}) $/MWh")
    b_dev = field_t(fwd)
    # The coil account against the field at the device's own bank, shot and
    # chamber: costingfe prices conductor along the expansion adiabat, whose
    # compressed flux volume shrinks as B^-2, so the account falls as the
    # field (and the pressure it must hold) rises.
    coil_by_field = []
    for b_t in (22.0, 30.0, 40.0, 50.0):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r_b = model.forward(size_from_power=True, **_model_fwd(fwd, b_t))
        coil_by_field.append((b_t, float(r_b.cas22_detail["C220103"])))
    print("  coil account (C220103, M$/module) against the field at this "
          "device's bank, shot and chamber: "
          + ", ".join(f"{b:.0f} T {c:.1f}" for b, c in coil_by_field)
          + "; magnetic pressure "
          + ", ".join(f"{coil_pressure_mpa(b):.0f}" for b, _ in coil_by_field) + " MPa")
    print(f"  AUDIT coil: {coil_pressure_mpa(b_dev):.0f} MPa "
          f"magnetic pressure at {b_dev:.0f} T, cycled from zero every shot, "
          f"{diag['coil_cycles_life']:.1e} times over the {fwd['lifetime_yr']:.0f} yr "
          f"book life at {diag['f_rep_hz']:.2f} Hz; no conductor or case has a "
          f"gigacycle basis at this stress, and the coil that delivers the "
          f"field is neither designed nor priced here")
    fields = ([B_COMPRESSION_T] if b_dev > B_COMPRESSION_T else []) + [10.0, 5.0]
    for b_t in fields:
        f_b = dict(fwd, b_center=b_t)
        f_b["max_f_rep"] = min(float(fwd.get("max_f_rep", model._eng_defaults["max_f_rep"])),
                               duty_bound_rate_hz(f_b, e_del_mj(f_b)))
        _, d_b = run(model, f_b)
        label = ("field reverted to the basis" if b_t == B_COMPRESSION_T
                 else "field/density")
        print(f"  RISK {label}: the device at {b_t:.0f} T (burn "
              f"{d_b['tau_burn_implied_s']:.2f} s, {d_b['n_mod']} modules at "
              f"{d_b['f_rep_hz']:.2f} Hz, burnup {d_b['burn_fraction']:.1e}): "
              f"LCOE {d_b['lcoe']:.1f} ({d_b['lcoe'] - diag['lcoe']:+.1f}) $/MWh")

    # --- credit (rerun in-model) ---
    _, diag_bottom = run(model, dict(fwd, eta_th=ETA_TH_BOTTOMING))
    credit_bottoming = diag_bottom["lcoe"] - diag["lcoe"]
    print(f"  CREDIT thermal bottoming at eta_th {ETA_TH_BOTTOMING} "
          f"(basis change): {credit_bottoming:+.2f} $/MWh")

    lo = diag["lcoe"] + tri_lo + min(credit_bottoming, 0.0)
    hi = (diag["lcoe"] + adder_switch_repricing + tri_hi
          + adder_driver_thermal)
    print(f"  HONEST BAND: {lo:.1f} - {hi:.1f} $/MWh")
    return diag["lcoe"], lo, hi


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)
    for label, spec in POINTS.items():
        analyze(label, spec)
