"""Burnup as a design axis: one knob, four coupled accounts.

`burn_fraction` sizes the CAS80 unburned-fuel recycle loss, the bred-He-3
cumulative recycle credit (f_He3_eff = bf / (1 - fr (1 - bf))), and the
vacuum-pumping throughput; through the burnup closure
(`tritium_burn.f_t_from_burnup`) it also pins the in-pulse tritium burn.
This scan sweeps burn_fraction under the two triton-fate limits:

- thermalized: dhe3_f_T = f_T(burn_fraction) at the study's 70 keV
  calibration; the bred tritium burns and its 14.1 MeV neutrons are in the
  power balance (wall/shield repricing for that spectrum is NOT in the
  model, so high-burnup rows on this branch are LCOE floors).
- prompt loss: dhe3_f_T = 0; MeV tritons leave the small-s plasmoid before
  thermalizing and reach the store. The model still books the T-branch
  kinetic energy as charged, so this branch is slightly generous.

The store-and-decay fuel cycle at high burnup exists only on the
prompt-loss branch; the scan prices what each escape costs, at both the
declared fuel_recovery 0.99 and a tier-3-grade 0.999.
"""
import csv

from study import OUTPUT_DIR, build_model, load_config, run, wall_area_m2

from tritium_burn import POINTS, f_t_from_burnup, point_fwd, reaction_rates

from costingfe.layers.economics import levelized_replacement_cost

BURN_FRACTIONS = (3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 0.15, 0.3)
FUEL_RECOVERY = (0.99, 0.999)
T_I_CALIB_KEV = 70.0
MWH_PER_YR = 1000.0 * 8760.0  # at 1 GWe net; scaled by availability below

# Neutron-damage repricing (study-side; the model's core_lifetime knob is
# inert for this concept, so wall replacement under neutron load is charged
# here with the model's own levelized-replacement closed form).
# 1 MW/m^2 of 14 MeV neutron wall load produces about 10 dpa per full-power
# year in Fe-based structure (standard fusion-materials figure); 2.45 MeV
# D-D neutrons displace less per unit energy flux, folded in at 0.4
# 14-MeV-equivalent. Tolerance band: 20 dpa is the demonstrated RAFM
# database edge, 50 dpa the DEMO-class design target; both are quoted, no
# advanced-material speculation is taken.
DPA_PER_MWY_M2_14MEV = 10.0
DPA_REL_DD = 0.4
DPA_TOLERANCE = (20.0, 50.0)
E_N_DD_MEV = 2.45
E_N_DT_MEV = 14.07
MEV = 1.602e-13


def wall_damage_adder(result, f_t, fwd, mwh):
    """Levelized neutron-driven first-wall replacement [$ /MWh] at each
    dpa tolerance, from the machine's own reaction rates and wall area."""
    rr = reaction_rates(result)
    n_mod = int(result.solved_n_mod)
    area = wall_area_m2(result.params)
    p_n_dd_mw = 0.5 * rr["dd"] * E_N_DD_MEV * MEV / 1e6  # per module
    p_n_dt_mw = f_t * 0.5 * rr["dd"] * E_N_DT_MEV * MEV / 1e6
    gamma_eq = (p_n_dt_mw + DPA_REL_DD * p_n_dd_mw) / area  # 14 MeV-equiv MW/m^2
    dpa_per_fpy = DPA_PER_MWY_M2_14MEV * gamma_eq
    event = float(result.cas22_detail["C220101"]) * n_mod
    i, n = fwd["interest_rate"], fwd["lifetime_yr"]
    avail = fwd["availability"]
    out = {}
    for tol in DPA_TOLERANCE:
        t_cal = tol / dpa_per_fpy / avail if dpa_per_fpy > 0 else float("inf")
        out[tol] = float(
            levelized_replacement_cost(event, t_cal, i, n)) * 1e6 / mwh
    return out, gamma_eq


def scan_point(name, spec):
    cfg, fwd0 = point_fwd(spec)
    model = build_model(cfg)
    avail = fwd0["availability"]
    mwh = MWH_PER_YR * avail
    rows = []
    for fr in FUEL_RECOVERY:
        print(f"\n== {name} at fuel_recovery {fr} "
              f"(+dmg = wall replacement at 50/20 dpa) ==")
        print(f"{'bf':>7} {'f_T':>5} "
              f"{'LCOE(th)':>8} {'+dmg':>10} {'Gn':>5} "
              f"{'LCOE(pr)':>8} {'+dmg':>10}")
        for bf in BURN_FRACTIONS:
            f_t = f_t_from_burnup(bf, T_I_CALIB_KEV)
            f_he3 = bf / (1.0 - fr * (1.0 - bf))
            out = {}
            for branch, dhe3_f_t in (("th", f_t), ("pr", 0.0)):
                r, d = run(model, dict(
                    fwd0, burn_fraction=bf, fuel_recovery=fr, dhe3_f_T=dhe3_f_t))
                dmg, gamma = wall_damage_adder(r, dhe3_f_t, fwd0, mwh)
                out[branch] = dict(
                    lcoe=d["lcoe"],
                    fuel=float(r.costs.cas80) * 1e6 / mwh,
                    pump=float(r.cas22_detail["C220106_pump"]),
                    dmg=dmg, gamma=gamma,
                )
            th, pr = out["th"], out["pr"]
            print(f"{bf:>7.3g} {f_t:>5.0%} "
                  f"{th['lcoe']:>8.1f} +{th['dmg'][50.0]:.1f}/{th['dmg'][20.0]:.1f}"
                  f" {th['gamma']:>5.2f} "
                  f"{pr['lcoe']:>8.1f} +{pr['dmg'][50.0]:.1f}/{pr['dmg'][20.0]:.1f}")
            rows.append(dict(
                point=name, fuel_recovery=fr, burn_fraction=bf,
                f_t_thermalized=round(f_t, 3), f_he3_eff=round(f_he3, 3),
                lcoe_thermalized=round(th["lcoe"], 2),
                lcoe_prompt_loss=round(pr["lcoe"], 2),
                fuel_usd_mwh_thermalized=round(th["fuel"], 2),
                fuel_usd_mwh_prompt_loss=round(pr["fuel"], 2),
                wall_dmg_usd_mwh_th_50dpa=round(th["dmg"][50.0], 2),
                wall_dmg_usd_mwh_th_20dpa=round(th["dmg"][20.0], 2),
                wall_dmg_usd_mwh_pr_50dpa=round(pr["dmg"][50.0], 2),
                wall_dmg_usd_mwh_pr_20dpa=round(pr["dmg"][20.0], 2),
                gamma_eq_th_mw_m2=round(th["gamma"], 3),
                gamma_eq_pr_mw_m2=round(pr["gamma"], 3),
                pump_musd=round(pr["pump"], 1),
            ))
    return rows


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)
    all_rows = []
    for name, spec in POINTS.items():
        all_rows.extend(scan_point(name, spec))
    with open(OUTPUT_DIR / "burnup_scan.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(all_rows[0]))
        w.writeheader()
        w.writerows(all_rows)
