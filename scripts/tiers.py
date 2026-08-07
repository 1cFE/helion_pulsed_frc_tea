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
    OUTPUT_DIR,
    apply_records,
    build_model,
    coherence_violations,
    load_config,
    run,
)

# The tier-3 rung keeps the concept-YAML chamber (0.5 m x 10 m, coherent
# under the tier-2 hhf wall at the solved rep rate); the resized-chamber
# optimum (yield 300 MJ, 45 m x 1.0 m, panel wall, 16.1 at 1 GWe) is owned
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
