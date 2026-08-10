"""He-3 price x burn-mix sweep: what the fleet-scale-supply concession is worth.

No defensible record exists for a He-3 price at fleet scale at ANY figure.
The only observed transactions are gram-to-kilogram scale at about
19-22 M$/kg (2024 spot about $2,500/L per Edelgas; Interlune's 2025 DOE
and Maybell agreements reference "today's commercial market price"; the
2026 TAE / Black Moon lunar option discloses no price), so the 2.0e+7
row is the observed-market anchor and the baseline 2e6 $/kg is already a
10x supply-at-scale concession against it. This sweep shows what each
concession is worth across the burn-mix span, at the tier-2
coherent-minimum machine. f_rad is coupled to the mix via the
bremsstrahlung floor; the tritium adder fires on the D-rich side. The
dd_frac 0.95 column probes how close deeper breeding gets to He-3
self-sufficiency (price-insensitivity is the test).
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

U_HE3_USD_KG = (2e7, 2e6, 1e6, 5e5, 1e5, 0.0)
DD_FRACS = (0.131, 0.314, 0.5, 0.7, 0.85, 0.95)
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

    # Super-speculation floor: the tier-3 coherent 3 GWe design
    # (coherent_min.py footer) with the He-3 price concession stacked on top.
    fwd3 = dict(cfg["forward"])
    for c in ("best_case.yaml", "tier2.yaml", "tier3.yaml"):
        apply_records(fwd3, c)
    fwd3.update(yield_per_shot_mj=200.0, chamber_length=45.0, plasma_t=1.0,
                r_bore=1.1, fw_class="panel", net_electric_mw=3000.0)
    print("\ntier-3 coherent 3 GWe design, He-3 price concession on top:")
    for u in (5e5, 0.0):
        _, d3 = run(model, dict(fwd3, u_he3=u))
        print(f"  u_he3 {u:>8.0f} $/kg: LCOE {d3['lcoe']:.1f}")
