"""The (max_f_rep, yield) surface at 1 GWe: the study's signature figure.

Every (f_rep ceiling, yield) pair reaches 1 GWe by trading n_mod, so this
is LCOE over that plane at tier-2 economics, with coherence recorded per
point (wall flux, flash energy) so the evidence-band shading can distinguish
"cheap" from "survivable". Gain is the stronger lever than rep rate (capital
is set by e_driver alone; doubling f_rep doubles recirculating drive with
fusion power, doubling yield does not), and the surface shows it.
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

MAX_F_REPS = (0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0)
YIELDS_MJ = (50.0, 101.4, 150.0, 200.0, 300.0, 500.0, 1000.0, 2000.0)
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
    for f_max, y in itertools.product(MAX_F_REPS, YIELDS_MJ):
        fwd = dict(fwd0, max_f_rep=f_max, yield_per_shot_mj=y)
        try:
            _, diag = run(model, fwd)
        except SizingInfeasible:
            continue
        violations = coherence_violations(fwd, diag, "tier2")
        rows.append(dict(
            max_f_rep=f_max, yield_mj=y, lcoe=diag["lcoe"],
            n_mod=diag["n_mod"], f_rep_solved=round(diag["f_rep_hz"], 3),
            q_wall_mw_m2=round(diag["q_wall_mw_m2"], 2),
            e_flash_mj_m2=round(diag["e_flash_mj_m2"], 3),
            coherent=(not violations)))
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "locus_scan.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{'yield MJ \\ f_max':>16} " + "".join(f"{f:>8}" for f in MAX_F_REPS))
    for y in YIELDS_MJ:
        line = f"{y:>16.1f} "
        for f_max in MAX_F_REPS:
            r = next((x for x in rows
                      if x["max_f_rep"] == f_max and x["yield_mj"] == y), None)
            line += f"{r['lcoe']:>7.1f}{'*' if r and not r['coherent'] else ' '}" if r else f"{'--':>8}"
        print(line)
    print("(* = violates a coherence constraint at that point)")
