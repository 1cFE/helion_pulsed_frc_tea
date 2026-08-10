"""What the model cannot price at the coherent minima, and what it overprices.

Runs the tier-2 and tier-3 coherent-minimum points (from coherent_min.py)
and reports, on top of each:

ADDERS (model gaps the red-team review identified, still open in costingfe):
- Switch-stack duty repricing: delta_switch prices the stack at 6% of the
  cap bank (single-shot practice); a stack commuting GW-class average power
  continuously is HVDC-valve class, order 100 M$/GW of commutated power.
- Tritium-plant band: the D-rich branch carries a 200 M$ point adder in the
  stack (study.py); the band is 100-300.

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

HVDC_MUSD_PER_GW = 100.0  # continuous-commutation silicon, HVDC valve class
TRITIUM_BAND_MUSD = (100.0, 300.0)
TRITIUM_POINT_MUSD = 200.0
ETA_TH_BOTTOMING = 0.30


def crf(i, n):
    return i * (1 + i) ** n / ((1 + i) ** n - 1)


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
    if dd > 0.5:
        print(f"  ADDER tritium-plant band vs 200 M$ point: "
              f"{tri_lo:+.2f} / {tri_hi:+.2f} $/MWh")

    # --- credit (rerun in-model) ---
    _, diag_bottom = run(model, dict(fwd, eta_th=ETA_TH_BOTTOMING))
    credit_bottoming = diag_bottom["lcoe"] - diag["lcoe"]
    print(f"  CREDIT thermal bottoming at eta_th {ETA_TH_BOTTOMING} "
          f"(basis change): {credit_bottoming:+.2f} $/MWh")

    lo = diag["lcoe"] + tri_lo + min(credit_bottoming, 0.0)
    hi = diag["lcoe"] + adder_switch_repricing + tri_hi
    print(f"  HONEST BAND: {lo:.1f} - {hi:.1f} $/MWh")
    return diag["lcoe"], lo, hi


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)
    for label, spec in POINTS.items():
        analyze(label, spec)
