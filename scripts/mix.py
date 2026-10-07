"""Burn-mix translation: He3/D ion ratio <-> the model's D-D event share.

The writeup and ledger quote burn mixes as the cost model's knob
(dhe3_dd_frac in the configs), the D-D share of primary fusion events by
count. The He3/D ion ratio is the quantity a reader can picture, and
Helion's patent states its mix that way (He3/D = 0.158 at 70 keV, which
is dd_frac 0.488). At one ion temperature the two are a fixed map through
the Bosch-Hale reactivities:

    R_DD   = (1/2) n_D^2 <sv>_DD          (both D-D branches)
    R_DHe3 = n_D n_He3 <sv>_DHe3

    dd_frac = R_DD / (R_DD + R_DHe3)
            = 1 / (1 + 2 r <sv>_DHe3 / <sv>_DD),   r = n_He3 / n_D

That is the map for the knob's own definition, where every D-He3 event is
a primary (purchased-fed) event. The model also lets bred He-3 recycle and
burn with cumulative probability f_He3_eff = bf / (1 - fr (1 - bf)) (half
a He-3 per D-D event, prompt branch), and prices those burns, so the
plasma it actually accounts for burns D-He3 at (1 - dd_frac + 0.5 dd_frac
f_He3_eff) per primary event. The "burn" functions below give the He3/D
ratio consistent with that total burn-rate ratio (the composition
scripts/tritium_burn.py prints); the plain functions give the knob's own
map. The two agree only when nothing recycles (f_He3_eff = 0).

Run as a script to print the study's mixes at the 70 keV basis (and at
20 and 50 keV for reference), under both maps.
"""
import os

os.environ.setdefault("COSTINGFE_BACKEND", "numpy")

from costingfe.layers.reactivity import sigv_dd_n, sigv_dd_p, sigv_dhe3

T_I_BASIS_KEV = 70.0


def _sv_ratio(t_i_kev: float) -> float:
    """<sv>_DHe3 / <sv>_DD (both D-D branches) at t_i_kev."""
    sv_dd = float(sigv_dd_n(t_i_kev) + sigv_dd_p(t_i_kev))
    return float(sigv_dhe3(t_i_kev)) / sv_dd


def dd_frac_from_he3_over_d(he3_over_d: float, t_i_kev: float = T_I_BASIS_KEV) -> float:
    """D-D share of primary fusion events for an He3/D ion ratio."""
    return 1.0 / (1.0 + 2.0 * he3_over_d * _sv_ratio(t_i_kev))


def he3_over_d_from_dd_frac(dd_frac: float, t_i_kev: float = T_I_BASIS_KEV) -> float:
    """He3/D ion ratio that gives a D-D share dd_frac of primary events."""
    return (1.0 / dd_frac - 1.0) / (2.0 * _sv_ratio(t_i_kev))


def f_he3_eff(burn_fraction_he3: float, fuel_recovery: float) -> float:
    """Cumulative fusion probability of a bred He-3 atom in the recycle loop."""
    return burn_fraction_he3 / (1.0 - fuel_recovery * (1.0 - burn_fraction_he3))


def he3_over_d_from_burn(dd_frac: float, f_he3: float, t_i_kev: float = T_I_BASIS_KEV) -> float:
    """He3/D ion ratio consistent with the model's total D-He3 burn rate,
    primary events plus recycled bred He-3 (f_he3 = f_He3_eff)."""
    r_dhe3_over_r_dd = (1.0 - dd_frac + 0.5 * dd_frac * f_he3) / dd_frac
    return 0.5 * r_dhe3_over_r_dd / _sv_ratio(t_i_kev)


def dd_frac_from_he3_over_d_burn(he3_over_d: float, f_he3: float, t_i_kev: float = T_I_BASIS_KEV) -> float:
    """Knob value at which the model's total D-He3 burn rate matches an
    He3/D ion ratio, with recycled bred He-3 burning at f_he3."""
    return 1.0 / (1.0 + 2.0 * he3_over_d * _sv_ratio(t_i_kev) - 0.5 * f_he3)


# The study's mixes, as the configs and ledger carry them.
STUDY_DD_FRACS = {
    "He-3-rich, the concept preset (1:1)": 0.131,
    "3:1 D:He-3 (the floor's calibration anchor)": 0.314,
    "Helion's mix (patent He3/D = 0.158)": 0.488,
    "speculation device": 0.7,
    "extrapolation device": 0.8,
    "D-rich end (records device)": 0.85,
}

if __name__ == "__main__":
    # recycle burn probabilities at the study's per-pass basis
    # (burn_fraction_he3 4.1e-4): four nines of recovery (Helion's mix and
    # the extrapolation and speculation grades) and three (records grade)
    F_FOUR_NINES = f_he3_eff(4.1e-4, 0.9999)
    F_THREE_NINES = f_he3_eff(4.1e-4, 0.999)
    for t_i in (T_I_BASIS_KEV, 50.0, 20.0):
        print(f"== T_i = {t_i:.0f} keV ==")
        print(f"  {'mix':<46} {'dd_frac':>8} {'He3/D knob':>10} "
              f"{'He3/D burn (fr 0.9999)':>22} {'(fr 0.999)':>10}")
        for label, dd in STUDY_DD_FRACS.items():
            print(f"  {label:<46} {dd:>8.3f} "
                  f"{he3_over_d_from_dd_frac(dd, t_i):>10.3f} "
                  f"{he3_over_d_from_burn(dd, F_FOUR_NINES, t_i):>22.3f} "
                  f"{he3_over_d_from_burn(dd, F_THREE_NINES, t_i):>10.3f}")
        print(f"  knob map round trip: He3/D 0.158 -> dd_frac "
              f"{dd_frac_from_he3_over_d(0.158, t_i):.3f}; burn map at fr 0.9999: "
              f"{dd_frac_from_he3_over_d_burn(0.158, F_FOUR_NINES, t_i):.3f}")
    print(f"\nf_He3_eff: {F_FOUR_NINES:.3f} at four nines, {F_THREE_NINES:.3f} at three")
    # The recycle race at each graded field (the basis, where the records
    # and Helion devices sit; the 30 T extrapolation grant; the 40 T
    # speculation grant) and at 50 T, the sensitivity above speculation
    # (the per-pulse pair scales as B^2 with the density): the share of
    # each species that eventually burns, and the unburned-fuel repurchase
    # multiplier 1 + (1 - bf)(1 - fr)/bf the fuel account carries.
    from study import burnup_at_field, field_t

    for label, fwd in (("basis field", {}),
                       ("extrapolation grant", {"b_center": 30.0}),
                       ("speculation grant", {"b_center": 40.0}),
                       ("sensitivity above speculation", {"b_center": 50.0})):
        bf_d, bf_he3 = burnup_at_field(fwd)
        print(f"\nrecycle race at the {label} ({field_t(fwd):.0f} T; per-pass burn "
              f"D {bf_d:.1e}, He-3 {bf_he3:.1e}):")
        print(f"  {'fuel_recovery':>14} {'D burns':>8} {'He-3 burns':>11} {'repurchase x':>13}")
        for fr in (0.99, 0.999, 0.9999):
            mult = 1.0 + (1.0 - bf_d) * (1.0 - fr) / bf_d
            print(f"  {fr:>14} {f_he3_eff(bf_d, fr):>8.1%} {f_he3_eff(bf_he3, fr):>11.1%} {mult:>13.2f}")
