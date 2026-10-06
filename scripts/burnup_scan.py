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

from study import (
    DPA_PER_MWY_M2_14MEV,
    OUTPUT_DIR,
    build_model,
    burnup_at_field,
    field_t,
    load_config,
    run,
    wall_load_14mev_equivalent,
)

from tritium_burn import POINTS, f_t_from_burnup, point_fwd

from costingfe.layers.reactivity import sigv_dd_n, sigv_dd_p, sigv_dhe3

# Both species' per-pass burn fractions derive from the same n tau, so a
# coherent burnup sweep scales them together at the fixed reactivity ratio.
HE3_OVER_DD = float(sigv_dhe3(70.0)) / float(sigv_dd_n(70.0) + sigv_dd_p(70.0))

from costingfe.layers.economics import levelized_replacement_cost

BURN_FRACTIONS = (1.2e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 0.15, 0.3)
FUEL_RECOVERY = (0.99, 0.999, 0.9999)
T_I_CALIB_KEV = 70.0
MWH_PER_YR = 1000.0 * 8760.0  # at 1 GWe net; scaled by availability below

# Neutron-damage repricing (study-side; the model's core_lifetime knob is
# inert for this concept, so wall replacement under neutron load is charged
# here with the model's own levelized-replacement closed form). The dpa
# rate comes from study.wall_load_14mev_equivalent. Tolerance band: 20 dpa
# is the demonstrated RAFM database edge, 50 dpa the DEMO-class design
# target; both are quoted, no advanced-material speculation is taken.
DPA_TOLERANCE = (20.0, 50.0)


def wall_damage_adder(result, fwd, mwh):
    """Levelized neutron-driven first-wall replacement [$ /MWh] at each
    dpa tolerance, from the machine's own reaction rates and wall area."""
    n_mod = int(result.solved_n_mod)
    gamma_eq = wall_load_14mev_equivalent(result)
    dpa_per_fpy = DPA_PER_MWY_M2_14MEV * gamma_eq
    # The coil bore sits 0.10 m behind the wall (r_bore = plasma_t + vacuum_t,
    # no blanket), so the close-coupled copper coils see the same fluence and
    # cannot outlive the wall: the replacement event carries both accounts.
    event = (
        float(result.cas22_detail["C220101"])
        + float(result.cas22_detail["C220103"])
    ) * n_mod
    i, n = fwd["interest_rate"], fwd["lifetime_yr"]
    avail = float(result.params["availability"])
    out = {}
    for tol in DPA_TOLERANCE:
        t_cal = tol / dpa_per_fpy / avail if dpa_per_fpy > 0 else float("inf")
        out[tol] = float(
            levelized_replacement_cost(event, t_cal, i, n)) * 1e6 / mwh
    return out, gamma_eq


def scan_point(name, spec):
    cfg, fwd0 = point_fwd(spec)
    model = build_model(cfg)
    # The axis carries the point's own per-pulse burnup (the basis pair
    # scaled as B^2 to its compression field) beside the fixed grid, so a
    # device above the basis field is read at its own basis as well.
    bf_own, _ = burnup_at_field(fwd0)
    axis = sorted(set(BURN_FRACTIONS) | {bf_own})
    rows = []
    for fr in FUEL_RECOVERY:
        print(f"\n== {name} at fuel_recovery {fr} "
              f"(+dmg = wall replacement at 50/20 dpa; own basis "
              f"{bf_own:.2e} at {field_t(fwd0):.0f} T) ==")
        print(f"{'bf':>7} {'f_T':>5} "
              f"{'LCOE(th)':>8} {'+dmg':>10} {'Gn':>5} "
              f"{'LCOE(pr)':>8} {'+dmg':>10}")
        for bf in axis:
            f_t = f_t_from_burnup(bf, T_I_CALIB_KEV)
            f_he3 = bf / (1.0 - fr * (1.0 - bf))
            out = {}
            for branch, dhe3_f_t in (("th", f_t), ("pr", 0.0)):
                r, d = run(model, dict(
                    fwd0, burn_fraction=bf,
                    burn_fraction_he3=min(0.95, HE3_OVER_DD * bf),
                    fuel_recovery=fr, dhe3_f_T=dhe3_f_t))
                mwh = MWH_PER_YR * float(r.params["availability"])
                dmg, gamma = wall_damage_adder(r, fwd0, mwh)
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
                own_basis=(abs(bf - bf_own) < 1e-12),
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
