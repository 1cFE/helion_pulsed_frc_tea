"""The breeder as the price of He-3: dedicated pure-D modules in the loop.

Every ladder device buys the He-3 it does not breed itself, at a ledger
price no market supports (u_he3 = 2e6 $/kg through the extrapolation grade,
5e5 at speculation). The vendor's fuel-cycle patent (US 11,469,003 B2) lets
the harvested He-3 fuel "subsequent fusion reactions in the same or a
different fusion reactor", and Polaris is billed as the first commercial
He-3 producer. This script prices that embodiment: a dedicated
pure-deuterium breeder module, so the purchased He-3 carries an explainable
unit cost (the breeder's ownership, tritium plant, and power per kilogram
delivered) instead of an assumed one.

Construction, per ladder device:
- The breeder is the device's own module and shot with the He-3 taken out
  of the fill. At dd_frac 0.85 the device is already 85% D-D by event count,
  so this is a small perturbation of what it does; on the vendor's lean
  shot it is not, and the gain collapses. At the same ion density,
  temperature, dwell and volume (pressure balance at the basis field;
  merging heats per ion) the D-D primary yield is the device yield times
  dd_frac x Q_DD / ((1 - x_He3)^2 q_eff), with x_He3 the He-3 ion fraction
  the device's burn-rate ratio implies (tritium_burn.he3_over_d at the
  study calibration temperature) and q_eff the device's mean energy per
  primary event. The expansion chamber is kept: the thermalized share of
  the driver energy returns only through it, whatever the fuel.
- Two modes. EXTRACT pumps prompt He-3 and tritium out every pulse (one
  eventual He-3 per D-D event: half prompt, half after the 17.8 yr mean
  tritium life). BURN lets the prompt He-3 recycle and burn in the breeder
  at the model's own cumulative fraction and exports the decay half plus
  the unburned remainder; it is the D-rich device minus its purchased 15%.
- Neutrons: half a 2.45 MeV neutron per D-D event and one eventual He-3 per
  event, so 1.225 MeV of neutron per He-3 bred wherever it is bred. Per
  module the breeder carries the D-rich device's neutron power times the
  density gain from removing the He-3 ions, on the same chamber, and
  inherits the study's shielding conclusion (no shield in the compression
  section; sacrificial coils on the wall schedule).
- The breeder's power table is the model's own pulsed chain at the device
  rep rate. Per-module cost is the device's own costing: the 'rpe' basis is
  the reactor-plant-equipment share (CAS22 / n_mod) at the all-in capital
  multiplier and effective CRF plus its CAS72 replacement (a breeder
  co-sited in the park); the 'full' basis is (CAS90 + CAS70) / n_mod (a
  standalone breeder plant). The tritium plant is study.run's adder at the
  breeder's neutron power; the fixed core is a facility-level item. The
  recovery store and conversion electronics would be smaller for a breeder
  and it needs no He-3 injection, so the basis is conservative.
- Unit cost [$ /kg] = (module cost + throughput tritium adder + net power
  at a stated price) / He-3 delivered. 'eq' delivers at an equilibrium
  decay store; 'pv' discounts the delayed half at the financing rate,
  lambda / (lambda + r). The device is re-run at u_he3 = unit cost with its
  own LCOE as the power price (fixed point).
- Siting: a co-sited breeder is priced at the marginal unit cost (and with
  whole modules); a central facility serving n devices carries integer
  modules, the model's own standalone fixed-cost intercept, and the fixed
  tritium core, with surplus He-3 unvalued.
- The lean-park closure (power modules at a lean mix with free He-3, fed by
  breeders inside the park, the breeder's consumption in the park's net
  output) is kept as a cross-check of the unit-cost reading.
"""
import csv
import math
import warnings

from study import (  # noqa: I001  sets COSTINGFE_BACKEND before costingfe imports
    OUTPUT_DIR,
    TRITIUM_FIXED_MUSD,
    TRITIUM_MUSD_PER_MW_NEUTRON,
    _T_I_CALIB_KEV,
    apply_records,
    build_model,
    f_rad_floor,
    load_config,
    run,
)
from module_scan import scaled
from tritium_burn import SECONDS_PER_YEAR, T_MEAN_LIFE_YR, he3_over_d, reaction_rates

from costingfe.layers.physics import M_HE3_KG, Q_DD_NHE3, Q_DD_PT, Q_DHE3

MEV_J = 1.602e-13
Q_DD_AVG_MEV = 0.5 * (Q_DD_PT + Q_DD_NHE3)
LAMBDA_T_PER_YR = 1.0 / T_MEAN_LIFE_YR
LEAN_MIXES = (0.131, 0.314)
MODES = ("extract", "burn")
BASES = ("rpe", "full")
FLEET_DEVICES = (1, 2, 5, 10, 20)
_FIXED_POINT_ITERS = 4
_INTERCEPT_MWE = 250.0

# The four ladder devices, as tests/test_study.py pins them.
DEVICES = {
    "records": dict(configs=("best_case.yaml",),
                    overrides=dict(dhe3_dd_frac=0.85, f_rad=0.28, chamber_length=10.0,
                                   plasma_t=1.5, r_bore=1.6, fw_class="panel")),
    "helion": dict(configs=(), overrides={}),
    "extrap": dict(configs=("best_case.yaml", "tier2.yaml"),
                   overrides=dict(chamber_length=10.0, plasma_t=1.5, r_bore=1.6,
                                  fw_class="panel")),
    "spec": dict(configs=("best_case.yaml", "tier2.yaml", "tier3.yaml"),
                 overrides=dict(yield_per_shot_mj=500.0, chamber_length=30.0,
                                plasma_t=1.5, r_bore=1.6, fw_class="panel")),
}


def device_fwd(name: str):
    cfg = load_config("baseline.yaml")
    fwd = dict(cfg["forward"])
    for c in DEVICES[name]["configs"]:
        apply_records(fwd, c)
    fwd.update(DEVICES[name]["overrides"])
    return cfg, fwd


def _kg_per_atom_s(res) -> float:
    return float(res.params["availability"]) * SECONDS_PER_YEAR * M_HE3_KG


def he3_demand_kg_yr(res):
    """Purchased-He-3 demand of a D-He3 plant [kg/yr] (primary events with the
    model's recycle-loss multiplier) and its own equilibrium T-decay return."""
    rr = reaction_rates(res)
    p = res.params
    bf = p.get("burn_fraction_he3") or p["burn_fraction"]
    loss_he3 = (1.0 - bf) / bf * (1.0 - p["fuel_recovery"])
    scale = int(res.solved_n_mod) * _kg_per_atom_s(res)
    return rr["dhe3_primary"] * (1.0 + loss_he3) * scale, rr["t_prod"] * scale


def breeder_module(model, res, mode: str) -> dict:
    """One pure-D breeder on the device's hardware and shot."""
    p = dict(res.params)
    rr = reaction_rates(res)
    y = he3_over_d((rr["dhe3_primary"] + rr["dhe3_bred"]) / rr["dd"], _T_I_CALIB_KEV)
    x_he3 = y / (1.0 + y)
    q_eff = float(res.power_table.p_fus) * 1e6 / (rr["events"] * MEV_J)
    ratio = p["dhe3_dd_frac"] * Q_DD_AVG_MEV / ((1.0 - x_he3) ** 2 * q_eff)
    yield_primary_mj = p["yield_per_shot_mj"] * ratio

    p.update(dhe3_dd_frac=1.0, f_rad=f_rad_floor(1.0), dhe3_f_T=0.0)
    if mode == "extract":
        # Pumped out every pulse: no recycle burn. The model derives the
        # power table's recycle burn from burn_fraction_he3, so it is driven
        # to a negligible value there; the product accounting takes it as zero.
        p["burn_fraction_he3"] = 1e-12
        f_he3_eff = 0.0
    else:
        f_he3_eff = model._dhe3_f_He3_eff(p)
    yield_mj = yield_primary_mj * (Q_DD_AVG_MEV + 0.5 * f_he3_eff * Q_DHE3) / Q_DD_AVG_MEV
    f_rep = float(p["f_rep"])
    pt = model._pulsed_forward(p, yield_mj * f_rep, p["e_driver_mj"], f_rep)
    dd_events_s = yield_primary_mj * 1e6 * f_rep / (Q_DD_AVG_MEV * MEV_J)
    kg = _kg_per_atom_s(res)
    return dict(
        mode=mode, ratio=ratio, x_he3=x_he3, yield_mj=yield_mj, f_rep=f_rep,
        gain=yield_mj / p["e_driver_mj"],
        p_fus=float(pt.p_fus), p_net=float(pt.p_net), p_neutron=float(pt.p_neutron),
        he3_prompt_kg_yr=0.5 * dd_events_s * (1.0 - f_he3_eff) * kg,
        t_prod_kg_yr=0.5 * dd_events_s * kg,
    )


def per_module_costs(res) -> dict:
    c = res.costs
    n = int(res.solved_n_mod)
    crf_eff = c.cas90 / c.total_capital
    cap_mult = c.total_capital / c.cas20
    return dict(
        rpe=(c.cas22 / n) * cap_mult * crf_eff + c.cas72 / n,
        full=(c.cas90 + c.cas70) / n,
        crf_eff=crf_eff,
        cap_mult=cap_mult,
        availability=float(res.params["availability"]),
        interest_rate=float(res.params["interest_rate"]),
    )


def pv_weight(cm: dict) -> float:
    """Worth of the delayed (decay) half at the financing rate."""
    return LAMBDA_T_PER_YR / (LAMBDA_T_PER_YR + cm["interest_rate"])


def unit_cost_breakdown(br: dict, cm: dict, basis: str, w: float, elec_usd_mwh: float) -> dict:
    """He-3 unit cost [$ /kg] of one breeder module and its three parts:
    module ownership, throughput tritium plant, and net power at the given
    price (a cost when the breeder consumes, a credit when it produces)."""
    out = br["he3_prompt_kg_yr"] + br["t_prod_kg_yr"] * w
    ann = cm["cap_mult"] * cm["crf_eff"]
    mwh_per_kg = -br["p_net"] * 8760.0 * cm["availability"] / out
    parts = dict(
        ownership=cm[basis] * 1e6 / out,
        tritium_plant=TRITIUM_MUSD_PER_MW_NEUTRON * br["p_neutron"] * ann * 1e6 / out,
        power=mwh_per_kg * elec_usd_mwh,
        mwh_per_kg=mwh_per_kg,
        output_kg_yr=out,
    )
    parts["total"] = parts["ownership"] + parts["tritium_plant"] + parts["power"]
    return parts


def device_at_breeder_price(model, fwd, res, br, cm, basis, w):
    """Re-run the device with its purchased He-3 at the breeder unit cost,
    the breeder's power priced at the device's own resulting LCOE."""
    lcoe = float(res.costs.lcoe)
    u = 0.0
    for _ in range(_FIXED_POINT_ITERS):
        u = unit_cost_breakdown(br, cm, basis, w, lcoe)["total"]
        _, diag = run(model, dict(fwd, u_he3=max(u, 0.0)))
        lcoe = diag["lcoe"]
    return u, lcoe


def _annual(res) -> float:
    c = res.costs
    return c.cas90 + c.cas70 + c.cas80


def fixed_intercept(model, fwd, res) -> float:
    """The model's own standalone fixed cost [M$/yr]: linear intercept of the
    plant's annual cost between 250 MWe and 1 GWe. A device whose 1 GWe plant
    is a single module scales its shot with plant size (module_scan.scaled);
    a multi-module device just carries fewer modules."""
    if int(res.solved_n_mod) == 1:
        small = scaled(fwd, _INTERCEPT_MWE, _INTERCEPT_MWE)
    else:
        small = dict(fwd, net_electric_mw=_INTERCEPT_MWE)
    a_small = _annual(run(model, small)[0])
    a_ref = _annual(res)
    x = _INTERCEPT_MWE / fwd["net_electric_mw"]
    return (a_small - x * a_ref) / (1.0 - x)


def central_unit_cost(model, fwd, res, br, cm, n_devices: int, elec_usd_mwh: float) -> dict:
    """A standalone breeder facility serving n devices' He-3 purchases: whole
    modules, the standalone fixed cost, the fixed tritium core, surplus
    He-3 unvalued."""
    bought, _ = he3_demand_kg_yr(res)
    out = br["he3_prompt_kg_yr"] + br["t_prod_kg_yr"]
    n_mod = math.ceil(n_devices * bought / out)
    ann = cm["cap_mult"] * cm["crf_eff"]
    per_module = unit_cost_breakdown(br, cm, "rpe", 1.0, elec_usd_mwh)["total"] * out / 1e6
    fixed = fixed_intercept(model, fwd, res) + TRITIUM_FIXED_MUSD * ann
    total = fixed + n_mod * per_module
    return dict(unit=total * 1e6 / (n_devices * bought), n_modules=n_mod, fixed_musd_yr=fixed)


def close_loop(res_lean, br: dict, cm: dict, basis: str, r: float) -> dict:
    """Lean plant plus the breeders that supply it, at an equilibrium store
    ('eq') and with the delayed half discounted at the financing rate ('pv')."""
    demand, own_t = he3_demand_kg_yr(res_lean)
    c = res_lean.costs
    p = res_lean.params
    avail = float(p["availability"])
    p_lean = float(res_lean.power_table.p_net) * int(res_lean.solved_n_mod)
    out = {}
    for tag, w in (("eq", 1.0), ("pv", LAMBDA_T_PER_YR / (LAMBDA_T_PER_YR + r))):
        n_b = (demand - own_t * w) / (br["he3_prompt_kg_yr"] + br["t_prod_kg_yr"] * w)
        adder_musd = TRITIUM_FIXED_MUSD + TRITIUM_MUSD_PER_MW_NEUTRON * br["p_neutron"] * n_b
        breeder_annual = n_b * cm[basis] + adder_musd * cm["cap_mult"] * cm["crf_eff"]
        annual = c.cas90 + c.cas70 + c.cas80 + breeder_annual
        p_park = p_lean + n_b * br["p_net"]
        lcoe = annual * 1e6 / (p_park * 8760.0 * avail)
        elec_musd = -n_b * br["p_net"] * 8760.0 * avail * lcoe / 1e6
        out[tag] = dict(
            n_b=n_b, lcoe=lcoe, p_park=p_park,
            he3_musd_kg=(breeder_annual + elec_musd) / demand,
            t_store_kg=n_b * br["t_prod_kg_yr"] * T_MEAN_LIFE_YR,
            breeder_mw_fus=n_b * br["p_fus"], demand_kg_yr=demand,
        )
    return out


def _devices():
    for name in DEVICES:
        cfg, fwd = device_fwd(name)
        model = build_model(cfg)
        res, diag = run(model, fwd)
        yield name, model, fwd, res, diag


def unit_cost_table():
    """Per device: the He-3 it buys, the breeder unit cost band, the device
    at that price, and the co-sited equilibrium breakdown."""
    rows = []
    for name, model, fwd, res, diag in _devices():
        cm = per_module_costs(res)
        bought, _ = he3_demand_kg_yr(res)
        _, d0 = run(model, dict(fwd, u_he3=0.0))
        br = breeder_module(model, res, "extract")
        row = dict(device=name, ladder_lcoe=round(diag["lcoe"], 1),
                   u_he3_ledger=float(res.params["u_he3"]),
                   he3_bought_kg_yr=round(bought, 1),
                   he3_line_ledger=round(diag["lcoe"] - d0["lcoe"], 1),
                   breeder_gain=round(br["gain"], 2),
                   breeder_p_net_mw=round(br["p_net"], 1),
                   breeder_p_neutron_mw=round(br["p_neutron"], 1),
                   breeder_output_kg_yr=round(br["he3_prompt_kg_yr"] + br["t_prod_kg_yr"], 1))
        for basis in BASES:
            for tag, w in (("eq", 1.0), ("pv", pv_weight(cm))):
                u, lcoe = device_at_breeder_price(model, fwd, res, br, cm, basis, w)
                row[f"unit_{basis}_{tag}_musd_kg"] = round(u / 1e6, 2)
                row[f"lcoe_{basis}_{tag}"] = round(lcoe, 1)
                row[f"he3_line_{basis}_{tag}"] = round(lcoe - d0["lcoe"], 1)
        parts = unit_cost_breakdown(br, cm, "rpe", 1.0, row["lcoe_rpe_eq"])
        row.update(ownership_musd_kg=round(parts["ownership"] / 1e6, 2),
                   tritium_plant_musd_kg=round(parts["tritium_plant"] / 1e6, 2),
                   power_musd_kg=round(parts["power"] / 1e6, 2),
                   mwh_per_kg=round(parts["mwh_per_kg"]))
        rows.append(row)
    return rows


def siting_table():
    """Per device: co-sited marginal and whole-module unit costs against a
    central facility serving 1-20 devices, power at the device LCOE."""
    rows = []
    for name, model, fwd, res, diag in _devices():
        cm = per_module_costs(res)
        br = breeder_module(model, res, "extract")
        bought, _ = he3_demand_kg_yr(res)
        out = br["he3_prompt_kg_yr"] + br["t_prod_kg_yr"]
        lcoe = diag["lcoe"]
        parts = unit_cost_breakdown(br, cm, "rpe", 1.0, lcoe)
        n1 = math.ceil(bought / out)
        core = TRITIUM_FIXED_MUSD * cm["cap_mult"] * cm["crf_eff"]
        whole = (n1 * parts["total"] * out / 1e6 + core) * 1e6 / bought
        row = dict(device=name, he3_bought_kg_yr=round(bought, 1),
                   module_output_kg_yr=round(out, 1),
                   cosited_marginal_musd_kg=round(parts["total"] / 1e6, 2),
                   cosited_whole_modules=n1,
                   cosited_whole_musd_kg=round(whole / 1e6, 2))
        for n in FLEET_DEVICES:
            c = central_unit_cost(model, fwd, res, br, cm, n, lcoe)
            row[f"central_{n}_musd_kg"] = round(c["unit"] / 1e6, 2)
            row[f"central_{n}_modules"] = c["n_modules"]
        row["fixed_musd_yr"] = round(c["fixed_musd_yr"], 1)
        rows.append(row)
    return rows


def sweep():
    """Lean-park closure: lean power modules fed by breeders inside the park."""
    rows = []
    for name, model, fwd, res, diag in _devices():
        cm = per_module_costs(res)
        r = cm["interest_rate"]
        breeders = {m: breeder_module(model, res, m) for m in MODES}
        for dd in LEAN_MIXES:
            lean_fwd = dict(fwd, dhe3_dd_frac=dd, f_rad=f_rad_floor(dd), u_he3=0.0)
            lean, diag_lean = run(model, lean_fwd)
            for mode in MODES:
                for basis in BASES:
                    loop = close_loop(lean, breeders[mode], cm, basis, r)
                    rows.append(dict(
                        device=name, ladder_lcoe=round(diag["lcoe"], 1),
                        lean_dd_frac=dd, lean_free_he3_lcoe=round(diag_lean["lcoe"], 1),
                        mode=mode, basis=basis,
                        breeder_gain=round(breeders[mode]["gain"], 2),
                        breeder_p_net_mw=round(breeders[mode]["p_net"], 1),
                        n_b_eq=round(loop["eq"]["n_b"], 2), n_b_pv=round(loop["pv"]["n_b"], 2),
                        park_lcoe_eq=round(loop["eq"]["lcoe"], 1),
                        park_lcoe_pv=round(loop["pv"]["lcoe"], 1),
                        he3_musd_kg_eq=round(loop["eq"]["he3_musd_kg"], 2),
                        he3_musd_kg_pv=round(loop["pv"]["he3_musd_kg"], 2),
                        park_net_mw=round(loop["eq"]["p_park"]),
                        t_store_kg=round(loop["eq"]["t_store_kg"]),
                    ))
    return rows


def _write(name, rows):
    with open(OUTPUT_DIR / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    warnings.simplefilter("ignore")
    OUTPUT_DIR.mkdir(exist_ok=True)

    unit = unit_cost_table()
    _write("breeder_unit_cost.csv", unit)
    print("== He-3 unit cost from a breeder of the same grade (M$/kg) and the device at that price ==")
    print(f"{'device':<8} {'LCOE':>6} {'bought':>7} {'line':>5} {'gain':>5} "
          f"{'rpe eq':>7} {'rpe pv':>7} {'full eq':>8} {'full pv':>8} "
          f"{'LCOE rpe eq':>11} {'full pv':>8}")
    for x in unit:
        print(f"{x['device']:<8} {x['ladder_lcoe']:>6.1f} {x['he3_bought_kg_yr']:>7.1f} "
              f"{x['he3_line_ledger']:>5.1f} {x['breeder_gain']:>5.2f} "
              f"{x['unit_rpe_eq_musd_kg']:>7.2f} {x['unit_rpe_pv_musd_kg']:>7.2f} "
              f"{x['unit_full_eq_musd_kg']:>8.2f} {x['unit_full_pv_musd_kg']:>8.2f} "
              f"{x['lcoe_rpe_eq']:>11.1f} {x['lcoe_full_pv']:>8.1f}")
    print("\n== breakdown, co-sited breeder, equilibrium store (M$/kg) ==")
    print(f"{'device':<8} {'output':>7} {'p_n MW':>7} {'own':>6} {'T-plant':>8} {'power':>6} "
          f"{'MWh/kg':>7} {'total':>6}")
    for x in unit:
        print(f"{x['device']:<8} {x['breeder_output_kg_yr']:>7.1f} {x['breeder_p_neutron_mw']:>7.1f} "
              f"{x['ownership_musd_kg']:>6.2f} {x['tritium_plant_musd_kg']:>8.2f} "
              f"{x['power_musd_kg']:>+6.2f} {x['mwh_per_kg']:>7} {x['unit_rpe_eq_musd_kg']:>6.2f}")

    siting = siting_table()
    _write("breeder_siting.csv", siting)
    print("\n== siting: co-sited vs central facility serving n devices (M$/kg, power at device LCOE) ==")
    print(f"{'device':<8} {'marginal':>8} {'whole':>6} " + "".join(f"{'n=' + str(n):>8}" for n in FLEET_DEVICES)
          + f" {'fixed M$/yr':>11}")
    for x in siting:
        print(f"{x['device']:<8} {x['cosited_marginal_musd_kg']:>8.2f} "
              f"{x['cosited_whole_musd_kg']:>6.2f} "
              + "".join(f"{x[f'central_{n}_musd_kg']:>8.2f}" for n in FLEET_DEVICES)
              + f" {x['fixed_musd_yr']:>11.1f}")

    rows = sweep()
    _write("breeder_loop.csv", rows)
    print("\n== lean-park closure (extract mode) ==")
    print(f"{'device':<8} {'dd':>5} {'free':>5} {'basis':<5} {'N_b eq':>6} {'pv':>5} "
          f"{'LCOE eq':>7} {'pv':>6} {'T kg':>5}")
    for x in rows:
        if x["mode"] != "extract":
            continue
        print(f"{x['device']:<8} {x['lean_dd_frac']:>5} {x['lean_free_he3_lcoe']:>5.1f} "
              f"{x['basis']:<5} {x['n_b_eq']:>6.1f} {x['n_b_pv']:>5.1f} "
              f"{x['park_lcoe_eq']:>7.1f} {x['park_lcoe_pv']:>6.1f} {x['t_store_kg']:>5}")
