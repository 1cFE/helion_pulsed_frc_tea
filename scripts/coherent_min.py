"""Constrained minimum-LCOE hunt: the study's answer to "how low can this go".

Instead of asserting a speculative operating point (the earlier draft's
Q = 40 in a chamber that flash-melts at that yield), this scan searches the
design space the machine actually controls - shot yield, chamber size, wall
class, burn mix - under the red-team coherence constraints (study.py):
bremsstrahlung-consistent f_rad, composite recovery cap, steady wall flux
within the bought wall class, per-shot flash energy under tungsten melt,
tritium plant charged whenever the mix is D-rich.

Two evidence levels:
- tier2: the extrapolation stack; the shot is the design-basis one
  (config/baseline.yaml: 128.1 MJ, the yield that reproduces the PPA at
  the patent burn point), so the only freedoms are geometry, wall class,
  and burn mix.
- tier3: the speculation stack; yield is also free (gain speculation),
  because tier 3 already concedes it is unevidenced - but it must still be
  survivable in the chamber it is costed in.

The chamber is resized honestly: the coil bore tracks the plasma radius
(r_bore = plasma_t + gap), and the cylinder wall, vessel, and structure are
repriced by the model at the scanned size.
"""
import csv
import itertools

from costingfe.model import SizingInfeasible

from study import (
    OUTPUT_DIR,
    apply_records,
    build_model,
    coherence_violations,
    load_config,
    run,
)

BURN_BRANCHES = (
    {"dhe3_dd_frac": 0.131, "f_rad": 0.123},  # YAML-lean mix at its brems floor
    {"dhe3_dd_frac": 0.314, "f_rad": 0.163},  # He-3-lean: buy fuel, few neutrons
    {"dhe3_dd_frac": 0.85, "f_rad": 0.28},    # D-rich: breed He-3, tritium plant
)
FW_CLASSES = ("panel", "hhf")
LENGTHS_M = (10.0, 15.0, 20.0, 30.0, 45.0, 60.0)
RADII_M = (0.5, 0.75, 1.0, 1.5)
YIELDS_MJ = (128.1, 150.0, 200.0, 300.0, 500.0, 750.0, 1000.0, 1500.0, 2000.0)

_VACUUM_T = 0.10


def tier_fwd(tier: str) -> dict:
    base_cfg = load_config("baseline.yaml")
    fwd0 = dict(base_cfg["forward"])
    apply_records(fwd0, "best_case.yaml")
    if tier in ("tier2", "tier3"):
        apply_records(fwd0, "tier2.yaml")
    if tier == "tier3":
        apply_records(fwd0, "tier3.yaml")
    return fwd0


def point_fwd(fwd0, y, length, radius, fw, branch) -> dict:
    fwd = dict(fwd0, **branch)
    fwd["yield_per_shot_mj"] = y
    fwd["chamber_length"] = length
    fwd["plasma_t"] = radius
    fwd["r_bore"] = radius + _VACUUM_T  # coil bore tracks the chamber
    fwd["fw_class"] = fw
    return fwd


def scan(tier: str):
    base_cfg = load_config("baseline.yaml")
    model = build_model(base_cfg)

    fwd0 = tier_fwd(tier)
    yields = YIELDS_MJ if tier == "tier3" else (fwd0["yield_per_shot_mj"],)
    # tier-1 coherence uses the tier-2 cap set (no tier-1-specific caps exist)
    

    rows = []
    for y, length, radius, fw, branch in itertools.product(
        yields, LENGTHS_M, RADII_M, FW_CLASSES, BURN_BRANCHES
    ):
        fwd = point_fwd(fwd0, y, length, radius, fw, branch)
        try:
            _, diag = run(model, fwd)
        except SizingInfeasible:
            continue
        violations = coherence_violations(
            fwd, diag, "tier2" if tier == "tier1" else tier)
        rows.append(
            dict(
                tier=tier,
                yield_mj=y,
                length_m=length,
                radius_m=radius,
                fw_class=fw,
                dd_frac=branch["dhe3_dd_frac"],
                lcoe=diag["lcoe"],
                n_mod=diag["n_mod"],
                f_rep_hz=round(diag["f_rep_hz"], 3),
                q_wall_mw_m2=round(diag["q_wall_mw_m2"], 2),
                e_flash_mj_m2=round(diag["e_flash_mj_m2"], 3),
                capital_per_kw=round(diag["capital_per_kw"]),
                coherent=(not violations),
                violations="; ".join(violations),
            )
        )
    return rows


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)
    all_rows = []
    for tier in ("tier1", "tier2", "tier3"):
        rows = scan(tier)
        all_rows.extend(rows)
        ok = [r for r in rows if r["coherent"]]
        ok.sort(key=lambda r: r["lcoe"])
        print(f"\n== {tier}: {len(ok)} coherent of {len(rows)} scanned ==")
        print(f"{'LCOE':>6} {'yield':>7} {'L':>5} {'r':>5} {'wall':>6} "
              f"{'dd':>5} {'n_mod':>5} {'f_rep':>6} {'q_wall':>6} {'flash':>6}")
        for r in ok[:10]:
            print(
                f"{r['lcoe']:>6.1f} {r['yield_mj']:>7.1f} {r['length_m']:>5.0f} "
                f"{r['radius_m']:>5.2f} {r['fw_class']:>6} {r['dd_frac']:>5.2f} "
                f"{r['n_mod']:>5} {r['f_rep_hz']:>6.2f} {r['q_wall_mw_m2']:>6.2f} "
                f"{r['e_flash_mj_m2']:>6.2f}"
            )
        if ok:
            # The same designs sold as a 3 GWe park (same module, more of them).
            # Sizing snaps to an integer module count, so a design that is
            # coherent at 1 GWe can trip the wall audit at 3; take the best
            # design that stays coherent at the larger plant.
            model3 = build_model(load_config("baseline.yaml"))
            best3 = None
            for cand in ok[:20]:
                branch = next(
                    b for b in BURN_BRANCHES if b["dhe3_dd_frac"] == cand["dd_frac"]
                )
                fwd3 = point_fwd(
                    tier_fwd(tier), cand["yield_mj"], cand["length_m"],
                    cand["radius_m"], cand["fw_class"], branch,
                )
                fwd3["net_electric_mw"] = 3000.0
                try:
                    _, d3 = run(model3, fwd3)
                except SizingInfeasible:
                    continue
                if coherence_violations(
                        fwd3, d3, "tier2" if tier == "tier1" else tier):
                    continue
                if best3 is None or d3["lcoe"] < best3[1]["lcoe"]:
                    best3 = (cand, d3)
            if best3 is not None:
                cand, d3 = best3
                print(f"  best coherent at 3 GWe: LCOE {d3['lcoe']:.1f}, "
                      f"yield {cand['yield_mj']:.0f} MJ, L {cand['length_m']:.0f} m, "
                      f"n_mod {d3['n_mod']}, f_rep {d3['f_rep_hz']:.2f} Hz")
    with open(OUTPUT_DIR / "coherent_min.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(all_rows[0]))
        w.writeheader()
        w.writerows(all_rows)
