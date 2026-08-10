"""In-pulse tritium burn vs breed rate for the D-rich machine.

The machine basis stores bred tritium for decay (dhe3_f_T = 0): no triton
burns in-plasma. That is exact only for an instantaneous pulse. A triton
born mid-pulse sits in a D-rich plasma at fusion temperature for the rest
of the dwell and burns with probability

    f_T ~= (1/2) n_D <sigma v>_DT tau

(the 1/2 averages over birth times; D-T reactivity is 30-40x D-D at these
temperatures, so the triton is the most reactive species in the chamber
the moment it is born). The cost model carries no dwell time or density,
so both are scanned: Helion states the pulse lasts under a millisecond
(helionenergy.com/faq), and the ARPA-E ALPHA retrospective quotes 2-5 ms
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

from study import (  # noqa: I001  sets COSTINGFE_BACKEND before costingfe imports
    OUTPUT_DIR,
    apply_records,
    build_model,
    coherence_violations,
    load_config,
    run,
)

from costingfe.layers.reactivity import sigv_dd_n, sigv_dd_p, sigv_dt

E_N_DD_MJ = 2.45 * 1.602e-19 * 1e6  # J per D-D neutron
SECONDS_PER_YEAR = 8760.0 * 3600.0
M_T_KG = 3.016 * 1.66054e-27  # triton mass
T_MEAN_LIFE_YR = 12.33 / 0.6931  # decay store residence to He-3

T_I_KEV = (20.0, 50.0, 70.0)
N_D_M3 = (1e22, 3e22, 1e23)  # compression-peak D density
TAU_S = (1e-4, 3e-4, 1e-3, 3e-3)  # dwell at fusion conditions

# Ladder points that carry a D-rich burn (dd_frac 0.85).
POINTS = {
    "tier2_rung": dict(
        tier="tier2", tier_cfgs=("best_case.yaml", "tier2.yaml"), overrides={},
    ),
    "tier3_min": dict(
        tier="tier3",
        tier_cfgs=("best_case.yaml", "tier2.yaml", "tier3.yaml"),
        overrides=dict(
            yield_per_shot_mj=300.0, chamber_length=45.0, plasma_t=1.0,
            r_bore=1.1, fw_class="panel",
        ),
    ),
}
F_T_SCENARIOS = (0.0, 0.01, 0.04)


def burn_probability(n_d_m3: float, t_i_kev: float, tau_s: float) -> float:
    return 0.5 * n_d_m3 * float(sigv_dt(t_i_kev)) * tau_s


def point_fwd(spec):
    cfg = load_config("baseline.yaml")
    fwd = dict(cfg["forward"])
    for c in spec["tier_cfgs"]:
        apply_records(fwd, c)
    fwd.update(spec["overrides"])
    return cfg, fwd


def breed_rate_kg_yr(result) -> float:
    """T breeding from the plant's own D-D neutron count: the n and T
    branches are equiprobable, so one triton is born per 2.45 MeV neutron."""
    pt = result.power_table
    p_n_w = float(pt.p_neutron) * int(result.solved_n_mod) * 1e6
    availability = float(result.params["availability"])
    r_t = p_n_w / E_N_DD_MJ * availability  # tritons/s, calendar-averaged
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
        print(f"\n== {name}: priced consequence of dhe3_f_T ==")
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
