"""What the model cannot price at the coherent minima, and what it overprices.

Runs the tier-2 and tier-3 coherent-minimum points (from coherent_min.py)
and reports, on top of each:

ADDERS (model gaps the red-team review identified, still open in costingfe):
- Recovery-store + switch replacement: CAS72 replaces only C220107 (the
  driver bank); the recovery store (delta_cap) and switch stack (delta_switch)
  cycle once per shot with the same film physics and are never replaced.
  Charged here with the model's own levelized-replacement closed form at the
  same cap_shot_lifetime.
- Switch-stack duty repricing: delta_switch prices the stack at 6% of the
  cap bank (single-shot practice); a stack commuting GW-class average power
  continuously is HVDC-valve class, order 100 M$/GW of commutated power.
- Tritium-plant band: the D-rich branch carries a 200 M$ point adder in the
  stack (study.py); the band is 100-300.

CREDITS (model conservatisms):
- C220109 store sizing: markup_cap = eta_dec*(1 + q_sci*f_ch) - 1 sizes the
  recovery store for ALL charged fusion energy, but the physics path only
  returns eta_dec*(E_driver + f_pdv*(1-f_rad)*f_ch*Y) to the circuit. Rerun
  with the physics-consistent store via cost_overrides.
- Thermal bottoming: the machine basis discards p_th (eta_th = 0); a
  low-grade bottoming cycle (eta_th 0.30) on the rejected stream is a real
  design option the basis excludes. Run in-model as an add-back scenario.

Anatomy: top capital accounts at each point, so the writeup can name what
carries the floor instead of gesturing at it.
"""
import math

from study import (
    OUTPUT_DIR,
    apply_records,
    build_model,
    load_config,
    run,
)

# Coherent-minimum design points (scripts/coherent_min.py argmin rows).
POINTS = {
    "tier2_min": dict(
        tier_cfgs=("best_case.yaml", "tier2.yaml"),
        overrides=dict(chamber_length=20.0, plasma_t=0.5, r_bore=0.6,
                       fw_class="panel"),
    ),
    "tier3_min": dict(
        tier_cfgs=("best_case.yaml", "tier2.yaml", "tier3.yaml"),
        overrides=dict(yield_per_shot_mj=300.0, chamber_length=45.0,
                       plasma_t=1.0, r_bore=1.1, fw_class="panel"),
    ),
}

MARKUP_SWITCH_BIDIR = 0.06
HVDC_MUSD_PER_GW = 100.0  # continuous-commutation silicon, HVDC valve class
TRITIUM_BAND_MUSD = (100.0, 300.0)
TRITIUM_POINT_MUSD = 200.0
ETA_TH_BOTTOMING = 0.30


def crf(i, n):
    return i * (1 + i) ** n / ((1 + i) ** n - 1)


def levelized_replacement(event_cost, t_replace, i, n):
    """Mirror of costingfe.layers.economics.levelized_replacement_cost."""
    s = (1.0 + i) ** (-t_replace)
    n_rep = max(0.0, math.ceil(n / t_replace) - 1.0)
    pv = event_cost * s * (1.0 - s**n_rep) / (1.0 - s)
    return pv * crf(i, n)


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
    avail = fwd["availability"]
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

    # --- adders ---
    f_rep = diag["f_rep_hz"]
    shots_per_year = f_rep * 8760 * 3600 * avail
    t_replace = float(p["cap_shot_lifetime"]) / shots_per_year

    c220107 = d22.get("C220107", 0.0)
    q_sci = float(pt.q_sci)
    f_ch = 1.0 - float(pt.p_neutron) / float(pt.p_fus)
    eta_dec, f_pdv, f_rad = p["eta_dec"], p["f_pdv"], p["f_rad"]
    staged = float(p.get("dec_staged_recovery_factor", 1.0))
    markup_cap = max(eta_dec * (1 + q_sci * f_ch) - 1, 0.0)
    delta_cap = c220107 * markup_cap * staged
    delta_switch = c220107 * MARKUP_SWITCH_BIDIR

    rep_annual = levelized_replacement(
        (delta_cap + delta_switch) * n_mod, t_replace, i, n)
    adder_recovery_replacement = rep_annual * 1e6 / mwh_per_year

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

    print(f"  ADDER recovery-store+switch replacement (every "
          f"{t_replace:.1f} yr): +{adder_recovery_replacement:.2f} $/MWh")
    print(f"  ADDER switch stack at HVDC class ({p_commutated_gw:.2f} GW "
          f"commutated): +{adder_switch_repricing:.2f} $/MWh")
    if dd > 0.5:
        print(f"  ADDER tritium-plant band vs 200 M$ point: "
              f"{tri_lo:+.2f} / {tri_hi:+.2f} $/MWh")

    # --- credits (both rerun in-model) ---
    markup_cap_phys = max(
        eta_dec * (1 + q_sci * f_ch * f_pdv * (1 - f_rad)) - 1, 0.0)
    c220109 = d22.get("C220109", 0.0)
    c220109_phys = c220109 - (markup_cap - markup_cap_phys) * c220107 * staged
    import warnings as _w
    with _w.catch_warnings():
        _w.simplefilter("ignore")
        r_phys = model.forward(
            size_from_power=True, cost_overrides={"C220109": c220109_phys}, **fwd)
    credit_store = float(r_phys.costs.lcoe) - diag["lcoe"]
    print(f"  CREDIT physics-consistent recovery store "
          f"(C220109 {c220109:.0f} -> {c220109_phys:.0f} M$/module): "
          f"{credit_store:+.2f} $/MWh")

    _, diag_bottom = run(model, dict(fwd, eta_th=ETA_TH_BOTTOMING))
    credit_bottoming = diag_bottom["lcoe"] - diag["lcoe"]
    print(f"  CREDIT thermal bottoming at eta_th {ETA_TH_BOTTOMING} "
          f"(basis change): {credit_bottoming:+.2f} $/MWh")

    lo = (diag["lcoe"] + adder_recovery_replacement + tri_lo
          + min(credit_store, 0.0) + min(credit_bottoming, 0.0))
    hi = (diag["lcoe"] + adder_recovery_replacement + adder_switch_repricing
          + tri_hi)
    print(f"  HONEST BAND: {lo:.1f} - {hi:.1f} $/MWh")
    return diag["lcoe"], lo, hi


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)
    for label, spec in POINTS.items():
        analyze(label, spec)
