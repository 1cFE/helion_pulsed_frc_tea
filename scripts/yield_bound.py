"""Constraints 7 and 8: the shot against the plasma energy and the burn
time, and the burn against the pulse period.

The plasma at peak compression holds chi of the delivered driver energy
and burns at the fusion power density of the burn point, so a shot's yield
is bounded by gain <= chi x tau_burn / tau_f, with tau_f the plasma's
energy breakeven time (study.breakeven_time_s). This script prints the
bound for the design-basis and speculation shots across the reconciliation
x_s span at the patent point and against the vendor's stated pulse; every
point that study.run evaluates carries the same quantity at the reference
x_s and at its own burn mix as diag["tau_burn_implied_s"].

The duty table then reads constraint 8 across the same span: for the four
devices and the deuterium-rich end's designs where they differ from the
device, the burn the shot implies at the point's own mix
(study.breakeven_time_at_point_s) times the solved rep rate. The
constraint is enforced at x_s 0.7, where the design search sets each
device's rate; the table shows where a design would sit at the fat-FRC
edge (0.85) and the thin one (0.5). Since duty = (yield x f_rep) x tau_f
/ (chi E_del), the constraint is a cap on the fusion power of one burn
section, chi E_del / tau_f, whatever the split between shot size and rep
rate; the table prints that cap beside the module's fusion power.
"""
import csv

from study import (  # noqa: I001  sets COSTINGFE_BACKEND before costingfe imports
    D_RICH_DEVICES,
    DEVICES,
    DUTY_MAX,
    OUTPUT_DIR,
    VENDOR_PULSE_S,
    X_S_REFERENCE,
    breakeven_time_at_point_s,
    breakeven_time_dt_s,
    breakeven_time_s,
    build_model,
    chi_from_xs,
    device_fwd,
    field_t,
    implied_burn_s,
    n_d_at_field,
    run,
    yield_bound_mj,
)

X_S_SPAN = (0.5, 0.7, 0.85)


def bound_table() -> list[dict]:
    """One row per (shot, x_s): the design-basis shot of the vendor device
    and the speculation shot, each from its own bank at the patent mix and
    its own compression field (the patent point's density scaled as B^2),
    so the burn a shot implies is read at the point the device compresses
    to."""
    rows = []
    for name in ("helion", "spec"):
        cfg, fwd = device_fwd(name, 1000.0)
        result, _ = run(build_model(cfg), fwd)
        y = float(result.params["yield_per_shot_mj"])
        e = float(result.params["e_driver_mj"])
        b_t = field_t(fwd)
        tau_f = breakeven_time_s(b_t=b_t, n_d_m3=n_d_at_field(b_t))
        for x_s in X_S_SPAN:
            rows.append(dict(
                device=name, yield_mj=y, e_driver_mj=e, b_center_t=b_t,
                n_d_m3=n_d_at_field(b_t), x_s=x_s,
                chi=chi_from_xs(x_s), tau_f_s=tau_f,
                yield_at_vendor_pulse_mj=yield_bound_mj(e, x_s, VENDOR_PULSE_S, tau_f),
                tau_burn_s=implied_burn_s(y, e, x_s, tau_f),
            ))
    return rows


def duty_table() -> list[dict]:
    """One row per (design, x_s): the four devices and the deuterium-rich
    end's designs at 1 GWe, each with the breakeven time of its own burn
    mix, the burn its shot implies at that x_s, and the duty that burn
    makes at the solved rep rate."""
    rows = []
    for table, tag in ((DEVICES, ""), (D_RICH_DEVICES, " (D-rich)")):
        for name in table:
            if table is D_RICH_DEVICES and D_RICH_DEVICES[name] is DEVICES[name]:
                continue  # the device is the deuterium-rich end itself
            cfg, fwd = device_fwd(name, 1000.0, table)
            result, diag = run(build_model(cfg), fwd)
            y = float(result.params["yield_per_shot_mj"])
            e = float(result.params["e_driver_mj"])
            tau_f = breakeven_time_at_point_s(fwd)
            for x_s in X_S_SPAN:
                tau = implied_burn_s(y, e, x_s, tau_f)
                rows.append(dict(
                    design=name + tag, dd_frac=fwd["dhe3_dd_frac"],
                    b_center_t=field_t(fwd), e_driver_mj=e,
                    yield_mj=y, f_rep_hz=diag["f_rep_hz"], x_s=x_s,
                    tau_f_s=tau_f, tau_burn_s=tau,
                    duty=tau * diag["f_rep_hz"],
                    p_fus_module_mw=y * diag["f_rep_hz"],
                    p_fus_cap_mw=chi_from_xs(x_s) * e / tau_f,
                ))
    return rows


def main():
    tau_f = breakeven_time_s()
    tau_f_cold = breakeven_time_s(te_over_ti=0.1)
    print(f"breakeven time at the patent point: {tau_f*1e3:.0f} ms thermalized, "
          f"{tau_f_cold*1e3:.0f} ms with electrons at a tenth of the ion "
          f"temperature (x{tau_f/tau_f_cold:.1f})")
    print(f"vendor pulse: {VENDOR_PULSE_S*1e3:.0f} ms")
    print(f"{'device':8} {'yield MJ':>9} {'bank MJ':>8} {'B T':>5} {'tau_f ms':>9} "
          f"{'x_s':>5} {'chi':>5} {'yield at pulse MJ':>18} {'burn implied s':>15}")
    rows = bound_table()
    for r in rows:
        print(f"{r['device']:8} {r['yield_mj']:9.1f} {r['e_driver_mj']:8.0f} "
              f"{r['b_center_t']:5.0f} {r['tau_f_s'] * 1e3:9.1f} {r['x_s']:5.2f} "
              f"{r['chi']:5.2f} {r['yield_at_vendor_pulse_mj']:18.2f} "
              f"{r['tau_burn_s']:15.3f}")
    # The burnup closure over each shot's burn span (writeup Section 5.2):
    # the thermalized-limit in-pulse tritium burn at the device's own
    # compression point (the patent density scaled as B^2).
    from tritium_burn import in_pulse_burn_vs_dwell

    for name in ("helion", "spec"):
        rr = [r for r in rows if r["device"] == name]
        lo, hi = min(r["tau_burn_s"] for r in rr), max(r["tau_burn_s"] for r in rr)
        f_d, f_t = in_pulse_burn_vs_dwell([lo, hi], rr[0]["n_d_m3"], 70.0)
        print(f"  {rr[0]['yield_mj']:.0f} MJ shot from a {rr[0]['e_driver_mj']:.0f} MJ "
              f"bank, burn {lo:.3f} to {hi:.3f} s at {rr[0]['b_center_t']:.0f} T "
              f"(n_D {rr[0]['n_d_m3']:.2e} m^-3): D burnup {f_d[0]:.1%} to "
              f"{f_d[1]:.1%}, thermalized in-pulse tritium burn {f_t[0]:.0%} to "
              f"{f_t[1]:.0%}")
    tau_dt = breakeven_time_dt_s(34.8, 15.0)
    print(f"cross-check, Slough 2025 CFR2 (D-T, 34.8 T, 15 keV): breakeven "
          f"{tau_dt*1e3:.2f} ms; gain 9.1 on the FRC energy is a "
          f"{9.1*tau_dt*1e3:.1f} ms burn, inside the paper's 2 to 5 ms transit")
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "yield_bound.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"\nconstraint 8 across x_s (enforced at {X_S_REFERENCE}, "
          f"duty <= {DUTY_MAX}): burn at the design's own mix x solved rep rate")
    print(f"{'design':18} {'dd':>5} {'B T':>4} {'bank':>5} {'yield MJ':>9} "
          f"{'f_rep Hz':>9} {'tau_f ms':>9} {'P_fus MW':>9} {'cap@0.7':>8} "
          + " ".join(f"{'x_s ' + str(x):>14}" for x in X_S_SPAN))
    duty = duty_table()
    designs = []
    for r in duty:
        if r["design"] not in designs:
            designs.append(r["design"])
    for d in designs:
        rr = [r for r in duty if r["design"] == d]
        r0 = rr[0]
        cap = next(r for r in rr if r["x_s"] == X_S_REFERENCE)["p_fus_cap_mw"]
        print(f"{d:18} {r0['dd_frac']:>5.2f} {r0['b_center_t']:>4.0f} "
              f"{r0['e_driver_mj']:>5.0f} {r0['yield_mj']:>9.1f} "
              f"{r0['f_rep_hz']:>9.2f} {r0['tau_f_s'] * 1e3:>9.1f} "
              f"{r0['p_fus_module_mw']:>9.0f} {cap:>8.0f} "
              + " ".join(f"{r['tau_burn_s']:>6.3f} s {r['duty']:>5.2f}"
                         for r in rr))
    with open(OUTPUT_DIR / "duty.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(duty[0].keys()))
        w.writeheader()
        w.writerows(duty)


if __name__ == "__main__":
    main()
