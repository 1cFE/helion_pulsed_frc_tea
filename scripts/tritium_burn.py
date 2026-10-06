"""In-pulse tritium burn vs breed rate for the D-rich machine.

The machine basis stores bred tritium for decay (dhe3_f_T = 0): no triton
burns in-plasma. That is exact only for an instantaneous pulse. A triton
born mid-pulse sits in a D-rich plasma at fusion temperature for the rest
of the dwell and burns with probability

    f_T ~= (1/2) n_D <sigma v>_DT tau

(the 1/2 averages over birth times; D-T reactivity is 30-40x D-D at these
temperatures, so the triton is the most reactive species in the chamber
the moment it is born). The cost model carries no dwell time or density,
so both are scanned: Helion states the required confinement is "on the
order of hundreds of microseconds to milliseconds" (helionenergy.com/faq,
June 2026 capture in docs/sources/), and the ARPA-E ALPHA retrospective quotes 2-5 ms
at gain conditions for the transiting FRC (arXiv:1907.09921), giving a
0.1-3 ms band; compression-peak densities 1e22-1e23 m^-3 span Trenta-class
to reactor-class compression.

Two anchors make the scan robust to both unknowns:

- Identity to D burnup: f_T = (1/2)(sv_DT / sv_DD) f_D, where f_D is the
  per-shot D burnup fraction. The ratio is 30-40 at 20-70 keV, so
  percent-level D burnup per shot already implies tens-of-percent tritium
  burn. The store-and-decay fuel cycle is only self-consistent with low
  per-shot burnup bought back by rep rate.

- Priced consequence: the tier-2 rung and tier-3 coherent minimum rerun
  with dhe3_f_T at scan values. Each burned triton emits a 14.1 MeV
  neutron (5.8x the 2.45 MeV D-D neutron energy), so plant neutron power,
  the wall audit, and the throughput-scaled tritium-plant adder all move,
  while the burned alpha adds recoverable charged energy.
"""
import csv
import math

import numpy as np

from study import (  # noqa: I001  sets COSTINGFE_BACKEND before costingfe imports
    D_RICH_DEVICES,
    DEVICES,
    N_D_PATENT_M3,
    OUTPUT_DIR,
    SECONDS_PER_YEAR,
    apply_records,
    build_model,
    coherence_violations,
    load_config,
    run,
)

from costingfe.layers.physics import Q_DD_NHE3, Q_DD_PT, Q_DHE3, Q_DT
from costingfe.layers.reactivity import sigv_dd_n, sigv_dd_p, sigv_dhe3, sigv_dt

# f_t_from_burnup lives in study.py, where the coherence check uses it as
# the in-pulse tritium burn floor; re-exported here for the scans/tests.
from study import f_t_from_burnup  # noqa: E402, F401

M_T_KG = 3.016 * 1.66054e-27  # triton mass
T_MEAN_LIFE_YR = 12.33 / 0.6931  # decay store residence to He-3

T_I_KEV = (20.0, 50.0, 70.0)
N_D_M3 = (1e22, 3e22, 1e23)  # compression-peak D density
TAU_S = (1e-4, 3e-4, 1e-3, 3e-3)  # dwell at fusion conditions

# The points where the store-and-decay cycle applies: Helion's own device,
# the records, extrapolation and speculation devices, which store tritium
# at dd_frac 0.85, 0.80 and 0.70, the extrapolation stack on Helion's
# chamber at its 3 Hz ceiling (the tier-2 regression pin, which
# constraint 8 flags), and the deuterium-rich end's speculation design.
POINTS = {
    "helion": dict(tier="tier2", tier_cfgs=(), overrides={}),
    "records": dict(
        tier="tier2",
        tier_cfgs=DEVICES["records"]["configs"],
        overrides=DEVICES["records"]["overrides"],
    ),
    "extrap": dict(
        tier="tier2",
        tier_cfgs=DEVICES["extrap"]["configs"],
        overrides=DEVICES["extrap"]["overrides"],
    ),
    "tier2_rung": dict(
        tier="tier2", tier_cfgs=("best_case.yaml", "tier2.yaml"), overrides={},
    ),
    "spec_d_rich": dict(
        tier="tier3",
        tier_cfgs=D_RICH_DEVICES["spec"]["configs"],
        overrides=D_RICH_DEVICES["spec"]["overrides"],
    ),
    "spec": dict(
        tier="tier3",
        tier_cfgs=DEVICES["spec"]["configs"],
        overrides=DEVICES["spec"]["overrides"],
    ),
}
# 0.78 is the thermalized-triton limit at per-pulse burnup 0.15, the
# high-compression-density counterfactual (the patent basis 1.2e-4 gives a
# floor of 0.002, which dhe3_f_T = 0 satisfies within tolerance).
F_T_SCENARIOS = (0.0, 0.01, 0.04, 0.78)


# The patent's operating table gives the confinement its cycle assumes:
# 0.157 s without tritium removal and 0.103 s with it (US 11,469,003 B2).
# The burnup basis uses the vendor's stated pulse instead; the writeup's
# tritium-burn figure draws the closure across both.
PATENT_CONFINEMENT_S = (0.103, 0.157)


def in_pulse_burn_vs_dwell(tau_s, n_d_m3: float, t_i_kev: float):
    """(f_D, f_T) after a dwell tau_s at fusion conditions: the per-pulse
    deuterium burnup 1 - exp(-n_D <sv>_DD tau) and the thermalized-limit
    in-pulse burn of a bred triton it implies (f_t_from_burnup). Vectorized
    over tau_s; n_d_m3 and t_i_kev are the burn point."""
    sv_dd = float(sigv_dd_n(t_i_kev) + sigv_dd_p(t_i_kev))
    tau = np.asarray(tau_s, dtype=float)
    f_d = 1.0 - np.exp(-n_d_m3 * sv_dd * tau)
    f_t = np.vectorize(lambda fd: f_t_from_burnup(float(fd), t_i_kev))(f_d)
    return f_d, f_t


def burn_probability(n_d_m3: float, t_i_kev: float, tau_s: float) -> float:
    return 0.5 * n_d_m3 * float(sigv_dt(t_i_kev)) * tau_s


def reaction_rates(result):
    """Absolute reaction rates from the model's own power table and burn mix.

    Primary events split (1 - dd_frac) D-He3 / dd_frac D-D by count (the
    cas80 convention). Bred He-3 recycles through the exhaust loop and
    eventually fuses with cumulative probability f_He3_eff =
    bf / (1 - fr (1 - bf)) (the model's own crediting); those burns ride on
    the D-D event term, so total D-He3 burns exceed the primary count. The
    mean energy per primary event is the same q_eff cas80 uses, so
    rate x q_eff reproduces p_fus exactly. T production is the D-D T branch
    (half the D-D events); its decay-He3 return is NOT in the model."""
    p = result.params
    dd = p["dhe3_dd_frac"]
    f_t = p.get("dhe3_f_T", 0.0)
    bf_he3 = p.get("burn_fraction_he3")
    if bf_he3 is None:
        bf_he3 = p["burn_fraction"]
    fr = p["fuel_recovery"]
    f_he3_eff = bf_he3 / (1.0 - fr * (1.0 - bf_he3))
    q_eff_mev = (1.0 - dd) * Q_DHE3 + dd * (
        0.5 * (Q_DD_PT + Q_DD_NHE3)
        + 0.5 * f_t * Q_DT
        + 0.5 * f_he3_eff * Q_DHE3
    )
    p_fus_w = float(result.power_table.p_fus) * 1e6  # per module
    r = p_fus_w / (q_eff_mev * 1.602e-13)
    return dict(
        events=r,
        dd=dd * r,
        dhe3_primary=(1.0 - dd) * r,  # fed by purchased He-3 (cas80 charges these)
        dhe3_bred=0.5 * dd * f_he3_eff * r,  # fed by recycled bred He-3
        t_prod=0.5 * dd * r,
        he3_prod=0.5 * dd * r,
        f_he3_eff=f_he3_eff,
    )


def he3_over_d(r_dhe3_over_r_dd: float, t_i_kev: float) -> float:
    """Plasma composition implied by the burn-rate ratio:
    n_He3/n_D = (1/2) x (R_DHe3/R_DD) x <sv>_DD/<sv>_DHe3."""
    sv_dd = float(sigv_dd_n(t_i_kev) + sigv_dd_p(t_i_kev))
    return 0.5 * r_dhe3_over_r_dd * sv_dd / float(sigv_dhe3(t_i_kev))


def point_fwd(spec):
    cfg = load_config("baseline.yaml")
    fwd = dict(cfg["forward"])
    for c in spec["tier_cfgs"]:
        apply_records(fwd, c)
    fwd.update(spec["overrides"])
    return cfg, fwd


def breed_rate_kg_yr(result) -> float:
    """T breeding from the reaction rates: one triton per D-D T-branch
    reaction (half the D-D events). Not derived from neutron power, which
    mixes 2.45 and 14.1 MeV neutrons once dhe3_f_T > 0."""
    rr = reaction_rates(result)
    availability = float(result.params["availability"])
    r_t = rr["t_prod"] * int(result.solved_n_mod) * availability
    return r_t * SECONDS_PER_YEAR * M_T_KG


if __name__ == "__main__":
    print("== in-pulse burn probability f_T = (1/2) n_D <sv>_DT tau ==")
    print(f"{'T_i keV':>8} {'n_D m^-3':>10} " + " ".join(f"{t*1e3:>7.1f}ms" for t in TAU_S))
    for t_i in T_I_KEV:
        for n_d in N_D_M3:
            row = " ".join(f"{burn_probability(n_d, t_i, tau):>9.1%}" for tau in TAU_S)
            print(f"{t_i:>8.0f} {n_d:>10.0e} {row}")

    print("\n== identity: f_T per unit D burnup, (1/2) sv_DT/sv_DD ==")
    for t_i in T_I_KEV:
        ratio = 0.5 * float(sigv_dt(t_i)) / float(sigv_dd_n(t_i) + sigv_dd_p(t_i))
        print(f"  T_i {t_i:>4.0f} keV: f_T = {ratio:.1f} x f_D  "
              f"(1% D burnup/shot -> {ratio / 100:.0%} of bred T burns)")

    rows = []
    for name, spec in POINTS.items():
        cfg, fwd = point_fwd(spec)
        model = build_model(cfg)

        r0, d0 = run(model, dict(fwd))
        rr = reaction_rates(r0)
        n_mod = d0["n_mod"]
        f_rep = d0["f_rep_hz"]
        dhe3_total = rr["dhe3_primary"] + rr["dhe3_bred"]
        print(f"\n== {name}: reaction rates (model power table, dd_frac "
              f"{fwd.get('dhe3_dd_frac')}) ==")
        print(f"  per module: D-D {rr['dd']:.2e} /s; D-He3 {dhe3_total:.2e} /s "
              f"({rr['dhe3_primary']:.2e} purchased-fed + {rr['dhe3_bred']:.2e} "
              f"bred-recycle at f_He3_eff {rr['f_he3_eff']:.2f})")
        print(f"  per module bred: T {rr['t_prod']:.2e} /s (to decay store), "
              f"He-3 {rr['he3_prod']:.2e} /s (prompt)")
        print(f"  plant ({n_mod} mod): D-D {rr['dd'] * n_mod:.2e} /s, "
              f"D-He3 {dhe3_total * n_mod:.2e} /s, "
              f"T {rr['t_prod'] * n_mod:.2e} /s")
        print(f"  per shot ({f_rep:.2f} Hz): {(rr['dd'] + dhe3_total) / f_rep:.2e} "
              f"reactions, T bred {rr['t_prod'] / f_rep:.2e} "
              f"({rr['t_prod'] / f_rep * 5.008e-27 * 1e6:.2f} mg)")
        print(f"  He-3 balance per primary event: burn "
              f"{(dhe3_total) / rr['events']:.2f} vs bred prompt "
              f"{rr['he3_prod'] / rr['events']:.2f} + decay-store return "
              f"{rr['t_prod'] / rr['events']:.2f} (NOT credited by cas80)")
        for t_i in T_I_KEV:
            print(f"  T_i {t_i:>3.0f} keV: n_He3/n_D = "
                  f"{he3_over_d(dhe3_total / rr['dd'], t_i):.3f}")

        fb = float(r0.params["burn_fraction"])
        print(f"  burnup closure at the model's own burn_fraction {fb}: "
              + ", ".join(
                  f"f_T({t_i:.0f} keV) = {f_t_from_burnup(fb, t_i):.0%}"
                  for t_i in T_I_KEV))
        for t_i in (70.0,):
            ratio_half = 0.5 * float(sigv_dt(t_i)) / float(
                sigv_dd_n(t_i) + sigv_dd_p(t_i))
            fb_max = 0.01 / ratio_half
            mult_015 = 1.0 + (1 - fb) / fb * 0.01
            mult_low_99 = 1.0 + (1 - fb_max) / fb_max * 0.01
            mult_low_999 = 1.0 + (1 - fb_max) / fb_max * 0.001
            print(f"  store-and-decay (f_T <= 1%) needs burn_fraction <= "
                  f"{fb_max:.1e} at {t_i:.0f} keV; CAS80 fuel-loss multiplier "
                  f"then {mult_low_99:.1f}x at fuel_recovery 0.99 "
                  f"({mult_low_999:.2f}x at 0.999) vs {mult_015:.2f}x at "
                  f"burn_fraction {fb}")

        print(f"== {name}: priced consequence of dhe3_f_T ==")
        print(f"{'f_T':>5} {'LCOE':>6} {'P_n MW':>7} {'T kg/yr':>8} "
              f"{'store t':>8} {'adder M$':>9} {'coherent':>9}")
        for f_t in F_T_SCENARIOS:
            r, d = run(model, dict(fwd, dhe3_f_T=f_t))
            breed = breed_rate_kg_yr(r)
            stored = breed * (1.0 - f_t)
            inventory_t = stored * T_MEAN_LIFE_YR / 1e3
            p_n = float(r.power_table.p_neutron) * d["n_mod"]
            viol = coherence_violations(dict(fwd, dhe3_f_T=f_t), d, spec["tier"])
            rows.append(dict(
                point=name, f_T=f_t, lcoe=round(d["lcoe"], 2),
                p_neutron_mw=round(p_n, 1), t_breed_kg_yr=round(breed, 1),
                t_stored_kg_yr=round(stored, 1),
                inventory_tonnes=round(inventory_t, 2),
                tritium_adder_musd=round(d["tritium_adder_musd"], 1),
                coherent=not viol,
            ))
            print(f"{f_t:>5.2f} {d['lcoe']:>6.1f} {p_n:>7.0f} {breed:>8.1f} "
                  f"{inventory_t:>7.2f}t {d['tritium_adder_musd']:>9.0f} "
                  f"{'yes' if not viol else '; '.join(viol)}")

    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "tritium_burn.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
