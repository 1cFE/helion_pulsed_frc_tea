"""Robustness of the tier-2 coherent minimum: one-at-a-time knob removal.

For each tier-2 ledger entry, revert it to its tier-1/baseline value and
re-run the tier-2 coherent-minimum point. The output ranks which entries
carry the number, so the ledger can say which weaknesses are load-bearing.
scripts/make_figures.py draws Figure 2 from the same rows.
"""
import csv
import math

from study import (
    E_DEL_BASIS_MJ,
    GAIN_BASIS,
    OUTPUT_DIR,
    apply_records,
    build_model,
    coherence_violations,
    device_fwd,
    duty_bound_rate_hz,
    e_del_mj,
    load_config,
    run,
)

def tier2_fwd():
    return device_fwd("extrap", 1000.0)


def tier1_stack() -> dict:
    """The revert target: the tier-1 STACK (baseline + tier-1 records),
    not the bare baseline, since tier-1 records can themselves override
    baseline knobs (the fuel_recovery anti-record reversion)."""
    fwd = dict(load_config("baseline.yaml")["forward"])
    apply_records(fwd, "best_case.yaml")
    return fwd


def reverted_point(fwd: dict, knob: str, tier1_fwd: dict) -> dict:
    """The device with one tier-2 entry reverted to its tier-1 value (the
    concept-YAML value where tier 1 carries none), its coupled entries
    moving with it: the burn mix takes its own radiated fraction, and the
    compression field re-solves the rate ceiling, because a field's first
    consequence is the duty bound (the burn lengthens as B^-2), so the
    reverted point is built in the modules that fit its longer burn, as
    the design search would build it, at or below the device's own
    ceiling and rounded down to the thousandth as the device's is."""
    reverted = dict(fwd)
    if knob in tier1_fwd:
        reverted[knob] = tier1_fwd[knob]
    elif knob == "fw_class":
        reverted[knob] = "panel"
    else:
        reverted.pop(knob, None)
    if knob == "dhe3_dd_frac":
        reverted["f_rad"] = tier1_fwd["f_rad"]
    if knob == "b_center":
        bound = duty_bound_rate_hz(reverted, e_del_mj(reverted))
        reverted["max_f_rep"] = min(float(fwd["max_f_rep"]),
                                    math.floor(bound * 1000.0) / 1000.0)
    return reverted


def tornado_rows(model, fwd: dict) -> tuple[dict, list[dict]]:
    """(the device's diagnostics, one row per reverted entry), the rows
    sorted by the size of the move. A reverted point is priced whether or
    not it stays coherent (the lever is what it is); the violations it
    trips are recorded so the writeup can mark them. The driver bank is a
    design-search dimension rather than a tier record; where the device
    carries a bank above the sourced Polaris 50 MJ, reverting it (the
    shot with it, at the design-basis gain, in the device's own chamber
    at its own ceiling) is the bank's worth as a one-at-a-time row."""
    _, diag0 = run(model, fwd)
    tier1_fwd = tier1_stack()
    rows = []

    def row(knob, reverted):
        _, diag = run(model, reverted)
        violations = coherence_violations(reverted, diag, "tier2")
        rows.append(dict(
            knob=knob, lcoe=diag["lcoe"], delta=diag["lcoe"] - diag0["lcoe"],
            kind=("financing" if knob == "interest_rate" else "engineering"),
            n_mod=diag["n_mod"], f_rep_hz=round(diag["f_rep_hz"], 2),
            max_f_rep=round(float(reverted.get("max_f_rep", model._eng_defaults["max_f_rep"])), 3),
            duty=round(diag["tau_burn_implied_s"] * diag["f_rep_hz"], 2),
            coherent=(not violations), violations="; ".join(violations)))

    for knob in load_config("tier2.yaml")["records"]:
        row(knob, reverted_point(fwd, knob, tier1_fwd))
    if e_del_mj(fwd) > E_DEL_BASIS_MJ:
        row("e_driver_mj", dict(fwd, e_driver_mj=E_DEL_BASIS_MJ,
                                yield_per_shot_mj=GAIN_BASIS * E_DEL_BASIS_MJ))
    rows.sort(key=lambda r: -abs(r["delta"]))
    return diag0, rows


if __name__ == "__main__":
    cfg, fwd = tier2_fwd()
    model = build_model(cfg)
    diag0, rows = tornado_rows(model, fwd)
    print(f"tier-2 coherent minimum: {diag0['lcoe']:.1f} $/MWh "
          f"({diag0['n_mod']} modules at {diag0['f_rep_hz']:.2f} Hz)\n")
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "tornado.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(f"{r['knob']:<24} revert -> {r['lcoe']:>6.1f}  ({r['delta']:+.1f})  [{r['kind']}]"
              f"  {r['n_mod']} modules at {r['f_rep_hz']:.2f} Hz under {r['max_f_rep']:.3f} Hz, duty {r['duty']:.2f}"
              + (f"  NOT coherent: {r['violations']}" if not r["coherent"] else ""))
