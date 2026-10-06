"""Robustness of the tier-2 coherent minimum: one-at-a-time knob removal.

For each tier-2 ledger entry, revert it to its tier-1/baseline value and
re-run the tier-2 coherent-minimum point. The output ranks which entries
carry the number, so the ledger can say which weaknesses are load-bearing.
"""
import csv

from study import (
    E_DEL_BASIS_MJ,
    GAIN_BASIS,
    OUTPUT_DIR,
    apply_records,
    build_model,
    coherence_violations,
    device_fwd,
    e_del_mj,
    load_config,
    run,
)

def tier2_fwd():
    return device_fwd("extrap", 1000.0)


if __name__ == "__main__":
    cfg, fwd = tier2_fwd()
    model = build_model(cfg)
    _, diag0 = run(model, fwd)
    print(f"tier-2 coherent minimum: {diag0['lcoe']:.1f} $/MWh\n")

    # Revert target is the tier-1 STACK (baseline + tier-1 records), not the
    # bare baseline: tier-1 records can themselves override baseline knobs
    # (e.g. the fuel_recovery anti-record reversion).
    tier1_fwd = dict(load_config("baseline.yaml")["forward"])
    apply_records(tier1_fwd, "best_case.yaml")

    rows = []
    tier2 = load_config("tier2.yaml")["records"]
    for knob in tier2:
        reverted = dict(fwd)
        if knob in tier1_fwd:
            reverted[knob] = tier1_fwd[knob]
        elif knob == "fw_class":
            reverted[knob] = "panel"
        else:
            # knob has no tier-1 entry: fall back to the concept-YAML value
            # by deleting the override entirely
            reverted.pop(knob, None)
        # reverting the burn mix must also revert its coupled f_rad
        if knob == "dhe3_dd_frac":
            reverted["f_rad"] = tier1_fwd["f_rad"]
        _, diag = run(model, reverted)
        # A reverted point is priced whether or not it stays coherent (the
        # lever is what it is); the violations it trips are recorded so the
        # writeup can mark them.
        violations = coherence_violations(reverted, diag, "tier2")
        rows.append(dict(knob=knob, lcoe=diag["lcoe"],
                         delta=diag["lcoe"] - diag0["lcoe"],
                         kind=("financing" if knob == "interest_rate"
                               else "engineering"),
                         coherent=(not violations),
                         violations="; ".join(violations)))

    # The driver bank is a design-search dimension rather than a tier
    # record; where the device carries a bank above the sourced Polaris
    # 50 MJ, reverting it (the shot with it, at the design-basis gain, in
    # the device's own chamber at its own ceiling) is the bank's worth as
    # a one-at-a-time row.
    if e_del_mj(fwd) > E_DEL_BASIS_MJ:
        reverted = dict(fwd, e_driver_mj=E_DEL_BASIS_MJ,
                        yield_per_shot_mj=GAIN_BASIS * E_DEL_BASIS_MJ)
        _, diag = run(model, reverted)
        violations = coherence_violations(reverted, diag, "tier2")
        rows.append(dict(knob="e_driver_mj", lcoe=diag["lcoe"],
                         delta=diag["lcoe"] - diag0["lcoe"], kind="engineering",
                         coherent=(not violations),
                         violations="; ".join(violations)))
    rows.sort(key=lambda r: -abs(r["delta"]))
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "tornado.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(f"{r['knob']:<24} revert -> {r['lcoe']:>6.1f}  ({r['delta']:+.1f})  [{r['kind']}]"
              + (f"  NOT coherent: {r['violations']}" if not r["coherent"] else ""))
