"""The evidence ladder: baseline -> tier 1 -> tier 2 -> tier 3 at 1 GWe.

Tier 3's chamber geometry and yield come from the coherent scan
(scripts/coherent_min.py), not from a config assertion; this script runs the
first three rungs plus the tier-3 stack at the coherent-scan optimum so the
whole ladder prints from one place. Every rung reports its wall state and
any model audit warnings; a rung that violates a coherence constraint is
flagged in the output rather than silently reported.
"""
import csv

from study import (
    D_RICH_DEVICES,
    DEVICE_ORDER,
    OUTPUT_DIR,
    PLANT_SIZES_MWE,
    apply_records,
    build_model,
    coherence_violations,
    device_fwd,
    load_config,
    run,
)

# The ladder's rungs are the tier stacks evaluated on Helion's own chamber
# (0.61 m x 10 m) at each stack's granted rate ceiling, kept as regression
# pins; the resized-chamber optima, with the rate chosen, are owned by
# scripts/coherent_min.py and priced as the four devices below. The tier-2
# and tier-3 rungs carry the D-rich mix of tier2.yaml, whose burn does not
# fit the pulse period at their ceilings, so constraint 8 flags them here
# rather than reporting them silently. Override here only to make the
# ladder itself quote a different tier-3 design.
TIER3_GEOMETRY = {}


def ladder():
    base_cfg = load_config("baseline.yaml")
    model = build_model(base_cfg)

    rungs = []
    fwd = dict(base_cfg["forward"])
    rungs.append(("tier0_baseline", dict(fwd), "tier2"))
    apply_records(fwd, "best_case.yaml")
    rungs.append(("tier1_records", dict(fwd), "tier2"))
    apply_records(fwd, "tier2.yaml")
    rungs.append(("tier2_extrapolations", dict(fwd), "tier2"))
    apply_records(fwd, "tier3.yaml")
    fwd.update(TIER3_GEOMETRY)
    rungs.append(("tier3_speculative", dict(fwd), "tier3"))

    rows = []
    for label, f, tier in rungs:
        result, diag = run(model, f)
        violations = coherence_violations(f, diag, tier)
        _, diag3 = run(model, dict(f, net_electric_mw=3000.0))
        rows.append(
            dict(
                tier=label,
                lcoe=diag["lcoe"],
                lcoe_3gwe=diag3["lcoe"],
                n_mod=diag["n_mod"],
                f_rep_hz=round(diag["f_rep_hz"], 3),
                tau_burn_implied_s=round(diag["tau_burn_implied_s"], 2),
                q_wall_mw_m2=round(diag["q_wall_mw_m2"], 2),
                e_flash_mj_m2=round(diag["e_flash_mj_m2"], 3),
                capital_per_kw=round(diag["capital_per_kw"]),
                tritium_adder_musd=diag["tritium_adder_musd"],
                coherent=(not violations),
                violations="; ".join(violations),
                model_warnings="; ".join(diag["warnings"]),
            )
        )
    return rows


def devices():
    """The four writeup devices at both plant sizes, each also priced at the
    design-basis 7% real rate with everything else as the rung has it, so
    the financing part of each rung (lcoe - lcoe_at_7pct) is quotable, and
    at the fusion literature's 30-year book life, so the ledger's lifetime
    row can quote what the 60 and 80 years are worth."""
    model = build_model(load_config("baseline.yaml"))
    rows = []
    for name, label in DEVICE_ORDER:
        for p in PLANT_SIZES_MWE:
            _, fwd = device_fwd(name, p)
            _, d = run(model, fwd)
            _, d7 = run(model, dict(fwd, interest_rate=0.07))
            rows.append(dict(
                device=label, plant_mwe=p, lcoe=round(d["lcoe"], 1),
                b_center_t=d["b_center_t"], e_driver_mj=d["e_driver_mj"],
                yield_mj=round(d["yield_per_shot_mj"], 1),
                coil_pressure_mpa=round(d["coil_pressure_mpa"]),
                p_fus_module_mw=round(d["p_fus_module_mw"]),
                chamber_length_m=fwd.get("chamber_length", 10.0),
                plasma_t_m=fwd.get("plasma_t", 0.5),
                lcoe_at_7pct=round(d7["lcoe"], 1),
                financing_part=round(d["lcoe"] - d7["lcoe"], 1),
                interest_rate=fwd["interest_rate"], lifetime_yr=fwd["lifetime_yr"],
                availability=round(d["availability"], 3),
                outage_routine=round(d["outage_routine"], 4),
                outage_bank=round(d["outage_bank"], 4),
                outage_wall=round(d["outage_wall"], 4),
                t_bank_yr=round(d["t_bank_yr"], 1), t_wall_yr=round(d["t_wall_yr"], 1),
                lcoe_at_a085=round(run(model, dict(fwd, availability=0.85))[1]["lcoe"], 1),
                lcoe_at_a095=round(run(model, dict(fwd, availability=0.95))[1]["lcoe"], 1),
                lcoe_at_30yr=round(run(model, dict(fwd, lifetime_yr=30.0))[1]["lcoe"], 1),
                n_mod=d["n_mod"], f_rep_hz=round(d["f_rep_hz"], 2),
                max_f_rep=fwd.get("max_f_rep", model._eng_defaults["max_f_rep"]),
                tau_burn_implied_s=round(d["tau_burn_implied_s"], 2),
                duty=round(d["tau_burn_implied_s"] * d["f_rep_hz"], 2),
                f_pdv_cap=round(d["f_pdv_cap"], 3),
                f_pdv_eff=round(d["f_pdv_eff"], 3),
                tritium_adder_musd=round(d["tritium_adder_musd"], 1),
            ))
    return rows


def d_rich_end():
    """The deuterium-rich end of the mix grid (dd_frac 0.85): its best
    design at each grade under all nine constraints, the rate included,
    priced at both plant sizes beside the device it is compared against
    (at the records grade it is the device), so the writeup can quote what
    He-3 self-sufficiency costs at each grade."""
    model = build_model(load_config("baseline.yaml"))
    labels = dict(DEVICE_ORDER)
    rows = []
    for name in D_RICH_DEVICES:
        for p in PLANT_SIZES_MWE:
            _, fwd = device_fwd(name, p, D_RICH_DEVICES)
            _, d = run(model, fwd)
            _, dev = run(model, device_fwd(name, p)[1])
            tier = "tier3" if name == "spec" else "tier2"
            v = coherence_violations(fwd, d, tier)
            rows.append(dict(
                device=f"{labels[name]} (D-rich end)", plant_mwe=p,
                lcoe=round(d["lcoe"], 1), device_lcoe=round(dev["lcoe"], 1),
                b_center_t=d["b_center_t"], e_driver_mj=d["e_driver_mj"],
                yield_mj=round(d["yield_per_shot_mj"], 1),
                n_mod=d["n_mod"], f_rep_hz=round(d["f_rep_hz"], 2),
                max_f_rep=fwd["max_f_rep"],
                tau_burn_implied_s=round(d["tau_burn_implied_s"], 2),
                duty=round(d["tau_burn_implied_s"] * d["f_rep_hz"], 2),
                tritium_adder_musd=round(d["tritium_adder_musd"], 1),
                availability=round(d["availability"], 3),
                violations="; ".join(v),
            ))
    return rows


if __name__ == "__main__":
    rows = ladder()
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "tiers.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{'tier':<24} {'LCOE':>7} {'3GWe':>7} {'n_mod':>5} {'f_rep':>6} "
          f"{'q_wall':>7} {'flash':>6} {'$/kW':>6} {'burn s':>6}  coherent")
    for r in rows:
        print(
            f"{r['tier']:<24} {r['lcoe']:>7.1f} {r['lcoe_3gwe']:>7.1f} {r['n_mod']:>5} "
            f"{r['f_rep_hz']:>6.2f} {r['q_wall_mw_m2']:>7.2f} "
            f"{r['e_flash_mj_m2']:>6.2f} {r['capital_per_kw']:>6} "
            f"{r['tau_burn_implied_s']:>6.2f}  "
            f"{'yes' if r['coherent'] else 'NO: ' + r['violations']}"
        )
        if r["model_warnings"]:
            print(f"    model: {r['model_warnings'][:200]}")

    dev = devices()
    with open(OUTPUT_DIR / "devices.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(dev[0]))
        w.writeheader()
        w.writerows(dev)
    print(f"\n{'device':<22} {'MWe':>5} {'LCOE':>6} {'B T':>4} {'E MJ':>5} {'yield':>6} {'coil':>5} {'at 7%':>6} {'fin.':>5} "
          f"{'rate':>5} {'life':>5} {'avail':>6} {'rout.':>6} {'bank':>6} {'wall':>6} "
          f"{'t_bank':>6} {'t_wall':>6} {'n_mod':>5} {'ceil':>6} {'f_rep':>5} {'A=.85':>6} {'A=.95':>6} {'30 yr':>6} {'burn s':>6} "
          f"{'duty':>5} {'pdv cap':>7} {'T M$':>5}")
    for r in dev:
        print(f"{r['device']:<22} {r['plant_mwe']:>5.0f} {r['lcoe']:>6.1f} "
              f"{r['b_center_t']:>4.0f} {r['e_driver_mj']:>5.0f} {r['yield_mj']:>6.0f} "
              f"{r['coil_pressure_mpa']:>5.0f} "
              f"{r['lcoe_at_7pct']:>6.1f} {r['financing_part']:>+5.1f} "
              f"{r['interest_rate']:>5.2f} {r['lifetime_yr']:>5.0f} "
              f"{r['availability']:>6.3f} {r['outage_routine']:>6.4f} {r['outage_bank']:>6.4f} "
              f"{r['outage_wall']:>6.4f} {r['t_bank_yr']:>6.1f} {r['t_wall_yr']:>6.1f} "
              f"{r['n_mod']:>5} {r['max_f_rep']:>6.3f} {r['f_rep_hz']:>5.2f} {r['lcoe_at_a085']:>6.1f} {r['lcoe_at_a095']:>6.1f} {r['lcoe_at_30yr']:>6.1f} "
              f"{r['tau_burn_implied_s']:>6.2f} {r['duty']:>5.2f} {r['f_pdv_cap']:>7.3f} "
              f"{r['tritium_adder_musd']:>5.0f}")

    cf = d_rich_end()
    with open(OUTPUT_DIR / "devices_d_rich.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(cf[0]))
        w.writeheader()
        w.writerows(cf)
    print(f"\nthe deuterium-rich end (dd_frac 0.85), best design under all nine constraints:")
    print(f"{'design':<36} {'MWe':>5} {'LCOE':>6} {'device':>6} {'B T':>4} {'E MJ':>5} {'yield':>6} {'n_mod':>5} {'ceil':>6} "
          f"{'f_rep':>6} {'burn s':>6} {'duty':>5} {'T M$':>5}  violations")
    for r in cf:
        print(f"{r['device']:<36} {r['plant_mwe']:>5.0f} {r['lcoe']:>6.1f} "
              f"{r['device_lcoe']:>6.1f} {r['b_center_t']:>4.0f} {r['e_driver_mj']:>5.0f} "
              f"{r['yield_mj']:>6.0f} {r['n_mod']:>5} {r['max_f_rep']:>6.3f} "
              f"{r['f_rep_hz']:>6.2f} {r['tau_burn_implied_s']:>6.2f} "
              f"{r['duty']:>5.2f} {r['tritium_adder_musd']:>5.0f}  {r['violations'] or 'coherent'}")
