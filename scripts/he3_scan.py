"""He-3 price x burn-mix sweep: what the fleet-scale-supply concession is worth.

No defensible record exists for a He-3 price at fleet scale at ANY figure;
the baseline 2e6 $/kg already prices a kilogram as though supply were
liquid. This sweep shows what the concession is worth across the burn-mix
span, at the tier-2 coherent-minimum machine. f_rad is coupled to the mix
via the bremsstrahlung floor; the tritium adder fires on the D-rich side.
"""
import csv

from study import (
    OUTPUT_DIR,
    apply_records,
    build_model,
    f_rad_floor,
    load_config,
    run,
)

U_HE3_USD_KG = (2e6, 1e6, 5e5, 1e5, 0.0)
DD_FRACS = (0.131, 0.314, 0.5, 0.7, 0.85)
TIER2_MIN_OVERRIDES = dict(
    chamber_length=20.0, plasma_t=0.5, r_bore=0.6, fw_class="panel")

if __name__ == "__main__":
    cfg = load_config("baseline.yaml")
    model = build_model(cfg)
    fwd0 = dict(cfg["forward"])
    apply_records(fwd0, "best_case.yaml")
    apply_records(fwd0, "tier2.yaml")
    fwd0.update(TIER2_MIN_OVERRIDES)

    rows = []
    for u in U_HE3_USD_KG:
        for dd in DD_FRACS:
            fwd = dict(fwd0, u_he3=u, dhe3_dd_frac=dd, f_rad=f_rad_floor(dd))
            _, diag = run(model, fwd)
            rows.append(dict(u_he3=u, dd_frac=dd, f_rad=round(f_rad_floor(dd), 3),
                             lcoe=diag["lcoe"],
                             tritium_adder=diag["tritium_adder_musd"]))
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "he3_scan.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{'u_he3 $/kg':>12} " + "".join(f"dd={d:<6}" for d in DD_FRACS))
    for u in U_HE3_USD_KG:
        line = f"{u:>12.0f} "
        for d in DD_FRACS:
            r = next(x for x in rows if x["u_he3"] == u and x["dd_frac"] == d)
            line += f"{r['lcoe']:<9.1f}"
        print(line)
