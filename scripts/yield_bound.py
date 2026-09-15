"""Constraint 7: the shot against the plasma energy and the burn time.

The plasma at peak compression holds chi of the delivered driver energy
and burns at the fusion power density of the burn point, so a shot's yield
is bounded by gain <= chi x tau_burn / tau_f, with tau_f the plasma's
energy breakeven time (study.breakeven_time_s). This script prints the
bound for the design-basis and speculation shots across the reconciliation
x_s span and against the vendor's stated pulse; every point that
study.run evaluates carries the same quantity at the reference x_s as
diag["tau_burn_implied_s"].
"""
import csv

from study import (  # noqa: I001  sets COSTINGFE_BACKEND before costingfe imports
    OUTPUT_DIR,
    VENDOR_PULSE_S,
    breakeven_time_s,
    build_model,
    chi_from_xs,
    device_fwd,
    implied_burn_s,
    run,
    yield_bound_mj,
)

X_S_SPAN = (0.5, 0.7, 0.85)


def bound_table() -> list[dict]:
    """One row per (shot, x_s): the design-basis shot of the vendor device
    and the speculation shot, both from the sourced bank."""
    rows = []
    tau_f = breakeven_time_s()
    for name in ("helion", "spec"):
        cfg, fwd = device_fwd(name, 1000.0)
        result, _ = run(build_model(cfg), fwd)
        y = float(result.params["yield_per_shot_mj"])
        e = float(result.params["e_driver_mj"])
        for x_s in X_S_SPAN:
            rows.append(dict(
                device=name, yield_mj=y, e_driver_mj=e, x_s=x_s,
                chi=chi_from_xs(x_s),
                yield_at_vendor_pulse_mj=yield_bound_mj(e, x_s, VENDOR_PULSE_S, tau_f),
                tau_burn_s=implied_burn_s(y, e, x_s, tau_f),
            ))
    return rows


def main():
    tau_f = breakeven_time_s()
    tau_f_cold = breakeven_time_s(te_over_ti=0.1)
    print(f"breakeven time at the patent point: {tau_f*1e3:.0f} ms thermalized, "
          f"{tau_f_cold*1e3:.0f} ms with electrons at a tenth of the ion "
          f"temperature (x{tau_f/tau_f_cold:.1f})")
    print(f"vendor pulse: {VENDOR_PULSE_S*1e3:.0f} ms")
    print(f"{'device':8} {'yield MJ':>9} {'x_s':>5} {'chi':>5} "
          f"{'yield at pulse MJ':>18} {'burn implied s':>15}")
    rows = bound_table()
    for r in rows:
        print(f"{r['device']:8} {r['yield_mj']:9.1f} {r['x_s']:5.2f} {r['chi']:5.2f} "
              f"{r['yield_at_vendor_pulse_mj']:18.2f} {r['tau_burn_s']:15.2f}")
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "yield_bound.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
