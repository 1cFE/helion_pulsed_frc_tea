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

from study import OUTPUT_DIR, build_model, load_config, run

from tritium_burn import POINTS, f_t_from_burnup, point_fwd

BURN_FRACTIONS = (3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 0.15, 0.3)
FUEL_RECOVERY = (0.99, 0.999)
T_I_CALIB_KEV = 70.0
MWH_PER_YR = 1000.0 * 8760.0  # at 1 GWe net; scaled by availability below


def scan_point(name, spec):
    cfg, fwd0 = point_fwd(spec)
    model = build_model(cfg)
    avail = fwd0["availability"]
    mwh = MWH_PER_YR * avail
    rows = []
    for fr in FUEL_RECOVERY:
        print(f"\n== {name} at fuel_recovery {fr} ==")
        print(f"{'bf':>7} {'f_T':>5} {'f_He3':>6} "
              f"{'LCOE(th)':>8} {'fuel':>5} {'LCOE(pr)':>8} {'fuel':>5} {'pump M$':>8}")
        for bf in BURN_FRACTIONS:
            f_t = f_t_from_burnup(bf, T_I_CALIB_KEV)
            f_he3 = bf / (1.0 - fr * (1.0 - bf))
            out = {}
            for branch, dhe3_f_t in (("th", f_t), ("pr", 0.0)):
                r, d = run(model, dict(
                    fwd0, burn_fraction=bf, fuel_recovery=fr, dhe3_f_T=dhe3_f_t))
                out[branch] = dict(
                    lcoe=d["lcoe"],
                    fuel=float(r.costs.cas80) * 1e6 / mwh,
                    pump=float(r.cas22_detail["C220106_pump"]),
                )
            print(f"{bf:>7.3g} {f_t:>5.0%} {f_he3:>6.2f} "
                  f"{out['th']['lcoe']:>8.1f} {out['th']['fuel']:>5.1f} "
                  f"{out['pr']['lcoe']:>8.1f} {out['pr']['fuel']:>5.1f} "
                  f"{out['pr']['pump']:>8.0f}")
            rows.append(dict(
                point=name, fuel_recovery=fr, burn_fraction=bf,
                f_t_thermalized=round(f_t, 3), f_he3_eff=round(f_he3, 3),
                lcoe_thermalized=round(out["th"]["lcoe"], 2),
                lcoe_prompt_loss=round(out["pr"]["lcoe"], 2),
                fuel_usd_mwh_thermalized=round(out["th"]["fuel"], 2),
                fuel_usd_mwh_prompt_loss=round(out["pr"]["fuel"], 2),
                pump_musd=round(out["pr"]["pump"], 1),
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
