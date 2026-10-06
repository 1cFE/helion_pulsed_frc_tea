"""Untangle the small-modular question: module count vs plant size.

Two controlled sweeps at the speculation device, holding the physics
fixed (constant gain, constant f_rep ceiling and so constant duty, wall
loading held by scaling chamber length with module power, driver energy
scaled with yield), the shot and chamber scaled from the device's own
module (1 GWe over its module count):

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
    build_model,
    device_fwd,
    run,
)

MODULE_MWE = (1000.0, 500.0, 250.0, 100.0, 50.0)
REF_DRIVER_MJ = 50.0  # the sourced bank, when the point does not carry its own
MIN_LENGTH_M = 3.0


def tier3_fwd():
    """The speculation device at 1 GWe: the sweeps scale its shot and
    chamber with module power."""
    return device_fwd("spec", 1000.0)


def scaled(fwd, module_mwe, plant_mwe, module_mwe_ref=1000.0):
    """The point's shot and chamber scaled with module power: yield, driver
    energy and chamber length go as the module's share of the reference
    module (constant gain, duty and wall loading); radius, bore and wall
    class stay the point's own."""
    s = module_mwe / module_mwe_ref
    return dict(
        fwd,
        net_electric_mw=plant_mwe,
        yield_per_shot_mj=fwd["yield_per_shot_mj"] * s,
        e_driver_mj=fwd.get("e_driver_mj", REF_DRIVER_MJ) * s,
        chamber_length=max(fwd["chamber_length"] * s, MIN_LENGTH_M),
    )


def sweep(model, fwd, plant_of_module, module_mwe_ref):
    rows = []
    for module in MODULE_MWE:
        plant = plant_of_module(module)
        r, d = run(model, scaled(fwd, module, plant, module_mwe_ref))
        c = r.costs
        mwh = plant * 8760 * float(r.params["availability"])
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
    _, d0 = run(model, fwd)
    module_ref = fwd["net_electric_mw"] / d0["n_mod"]
    print(f"speculation device: {d0['n_mod']} modules of {module_ref:.0f} MWe "
          f"at {d0['f_rep_hz']:.2f} Hz, {d0['lcoe']:.1f} $/MWh; the sweeps "
          f"scale that module")
    fixed_plant = sweep(model, fwd, lambda m: 1000.0, module_ref)
    standalone = sweep(model, fwd, lambda m: m, module_ref)
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
