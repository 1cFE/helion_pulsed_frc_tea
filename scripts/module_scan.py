"""Untangle the small-modular question: module count vs plant size.

Two controlled sweeps at the tier-3 stack, holding the physics fixed
(constant Q_sci = 6, constant f_rep ceiling, wall loading held by scaling
chamber length with module power, driver energy scaled with yield):

1. Module-size sweep at fixed 1 GWe plant: what does the model charge for
   delivering the same plant from more, smaller modules?
2. Standalone plant-size sweep (one module = one plant): what does the
   model charge for selling small plants, Helion's actual product shape?

The point of the separation: "bias against small modular units" is two
different claims. The sweeps show the model is nearly neutral to module
count at fixed plant size (buildings/CAS50/BOP price plant totals), while
standalone plant size is heavily penalized by fixed site dollars and the
P^0.5 staffing law - an analog-class question and a fleet-operations
question respectively, not a modularity tax.
"""
import csv

from study import (
    OUTPUT_DIR,
    apply_records,
    build_model,
    load_config,
    run,
)

MODULE_MWE = (1000.0, 500.0, 250.0, 100.0, 50.0)
REF_YIELD_MJ = 300.0
REF_DRIVER_MJ = 50.0
REF_LENGTH_M = 60.0
MIN_LENGTH_M = 3.0


def tier3_fwd():
    cfg = load_config("baseline.yaml")
    fwd = dict(cfg["forward"])
    for c in ("best_case.yaml", "tier2.yaml", "tier3.yaml"):
        apply_records(fwd, c)
    return cfg, fwd


def scaled(fwd, module_mwe, plant_mwe):
    s = module_mwe / 1000.0
    return dict(
        fwd,
        net_electric_mw=plant_mwe,
        yield_per_shot_mj=REF_YIELD_MJ * s,
        e_driver_mj=REF_DRIVER_MJ * s,
        chamber_length=max(REF_LENGTH_M * s, MIN_LENGTH_M),
        plasma_t=0.75,
        r_bore=0.85,
        fw_class="panel",
    )


def sweep(model, fwd, plant_of_module):
    rows = []
    for module in MODULE_MWE:
        plant = plant_of_module(module)
        r, d = run(model, scaled(fwd, module, plant))
        c = r.costs
        mwh = plant * 8760 * fwd["availability"]
        rows.append(dict(
            module_mwe=module,
            plant_mwe=plant,
            n_mod=d["n_mod"],
            lcoe=d["lcoe"],
            capital_per_kw=round(d["capital_per_kw"]),
            cas21=round(float(c.cas21)),
            cas50=round(float(c.cas50)),
            cas22=round(float(c.cas22)),
            bop_24_26=round(float(c.cas24) + float(c.cas25) + float(c.cas26)),
            om_usd_mwh=round(float(c.cas70) * 1e6 / mwh, 1),
            tritium_adder_musd=round(d["tritium_adder_musd"]),
        ))
    return rows


def show(title, rows):
    print(f"\n== {title} ==")
    print(f"{'module':>7} {'plant':>6} {'n_mod':>5} {'LCOE':>6} {'$/kW':>6} "
          f"{'CAS21':>6} {'CAS50':>6} {'CAS22':>6} {'BOP':>5} {'O&M':>6} {'T-plant':>7}")
    for r in rows:
        print(f"{r['module_mwe']:>7.0f} {r['plant_mwe']:>6.0f} {r['n_mod']:>5} "
              f"{r['lcoe']:>6.1f} {r['capital_per_kw']:>6} {r['cas21']:>6} "
              f"{r['cas50']:>6} {r['cas22']:>6} {r['bop_24_26']:>5} "
              f"{r['om_usd_mwh']:>6.1f} {r['tritium_adder_musd']:>7}")


if __name__ == "__main__":
    cfg, fwd = tier3_fwd()
    model = build_model(cfg)
    fixed_plant = sweep(model, fwd, lambda m: 1000.0)
    standalone = sweep(model, fwd, lambda m: m)
    show("module size at fixed 1 GWe plant", fixed_plant)
    show("standalone plant of one module", standalone)
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "module_scan.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(fixed_plant[0]) + ["sweep"])
        w.writeheader()
        for r in fixed_plant:
            w.writerow(dict(r, sweep="fixed_plant"))
        for r in standalone:
            w.writerow(dict(r, sweep="standalone"))
