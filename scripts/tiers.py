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

# The tier-3 rung keeps the concept-YAML chamber (0.5 m x 10 m, coherent
# under the tier-2 hhf wall at the solved rep rate); the resized-chamber
# optimum (yield 300 MJ, 45 m x 1.0 m, panel wall, 17.0 at 1 GWe) is owned
# and reported by scripts/coherent_min.py. Override here only to make the
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
    the financing part of each rung (lcoe - lcoe_at_7pct) is quotable."""
    model = build_model(load_config("baseline.yaml"))
    rows = []
    for name, label in DEVICE_ORDER:
        for p in PLANT_SIZES_MWE:
            _, fwd = device_fwd(name, p)
            _, d = run(model, fwd)
            _, d7 = run(model, dict(fwd, interest_rate=0.07))
            rows.append(dict(
                device=label, plant_mwe=p, lcoe=round(d["lcoe"], 1),
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
                n_mod=d["n_mod"], f_rep_hz=round(d["f_rep_hz"], 2),
                tritium_adder_musd=round(d["tritium_adder_musd"], 1),
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
          f"{'q_wall':>7} {'flash':>6} {'$/kW':>6}  coherent")
    for r in rows:
        print(
            f"{r['tier']:<24} {r['lcoe']:>7.1f} {r['lcoe_3gwe']:>7.1f} {r['n_mod']:>5} "
            f"{r['f_rep_hz']:>6.2f} {r['q_wall_mw_m2']:>7.2f} "
            f"{r['e_flash_mj_m2']:>6.2f} {r['capital_per_kw']:>6}  "
            f"{'yes' if r['coherent'] else 'NO: ' + r['violations']}"
        )
        if r["model_warnings"]:
            print(f"    model: {r['model_warnings'][:200]}")

    dev = devices()
    with open(OUTPUT_DIR / "devices.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(dev[0]))
        w.writeheader()
        w.writerows(dev)
    print(f"\n{'device':<22} {'MWe':>5} {'LCOE':>6} {'at 7%':>6} {'fin.':>5} "
          f"{'rate':>5} {'life':>5} {'avail':>6} {'rout.':>6} {'bank':>6} {'wall':>6} "
          f"{'t_bank':>6} {'t_wall':>6} {'n_mod':>5} {'A=.85':>6} {'A=.95':>6}")
    for r in dev:
        print(f"{r['device']:<22} {r['plant_mwe']:>5.0f} {r['lcoe']:>6.1f} "
              f"{r['lcoe_at_7pct']:>6.1f} {r['financing_part']:>+5.1f} "
              f"{r['interest_rate']:>5.2f} {r['lifetime_yr']:>5.0f} "
              f"{r['availability']:>6.3f} {r['outage_routine']:>6.4f} {r['outage_bank']:>6.4f} "
              f"{r['outage_wall']:>6.4f} {r['t_bank_yr']:>6.1f} {r['t_wall_yr']:>6.1f} "
              f"{r['n_mod']:>5} {r['lcoe_at_a085']:>6.1f} {r['lcoe_at_a095']:>6.1f}")
