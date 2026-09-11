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
from study import (
    DEVICES,
    OUTPUT_DIR,
    apply_records,
    build_model,
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


def crf(i, n):
    return i * (1 + i) ** n / ((1 + i) ** n - 1)


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

    print(f"\n=== {label}: LCOE {diag['lcoe']:.1f} $/MWh, n_mod {n_mod}, "
          f"f_rep {diag['f_rep_hz']:.2f} Hz, {diag['capital_per_kw']} $/kW ===")

    # --- anatomy: top per-module CAS22 accounts + plant accounts ---
    top = sorted(d22.items(), key=lambda kv: -kv[1])[:8]
    print("  top CAS22 accounts (M$/module):",
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
    for label, musd in (
        ("buildings (CAS21)", float(c.cas21)),
        ("CAS50 incl. decommissioning", float(c.cas50)),
        ("fuel handling + tritium plant (C220500)", d22["C220500"] * n_mod),
        ("heat rejection + electrical plant (CAS24-26)",
         float(c.cas24) + float(c.cas25) + float(c.cas26)),
        ("vacuum + exhaust (C220106)", d22["C220106"] * n_mod),
        ("first wall (C220101)", d22["C220101"] * n_mod),
        ("DEC power electronics (C220109)", d22["C220109"] * n_mod),
        ("coils (C220103)", d22["C220103"] * n_mod),
    ):
        print(f"    {label:<46} {musd:7.0f} M$  {musd * lev:5.2f} $/MWh")
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

    # --- field/density risk (the dominant open band) ---
    # The per-pulse burnup basis is the patent triple at 22 T; if the
    # reactor-point compression field is lower, density and burnup fall as
    # B^2 and the recovery nines bind harder. Priced by scaling both
    # species' per-pulse burn fractions.
    for b_t in (10.0, 5.0):
        scale = (b_t / 22.0) ** 2
        _, d_b = run(model, dict(
            fwd, burn_fraction=1.2e-4 * scale,
            burn_fraction_he3=4.1e-4 * scale))
        print(f"  RISK field/density: at a {b_t:.0f} T-consistent burn point "
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
