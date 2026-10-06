# Evidence ledger

*Tal Rubin, Astera Institute*

**What this is.** Every non-baseline value adopted in the ladder, with
the analog class named and the reason it applies. Tiers: tier 1 is a
citable record or published bound, tier 2 a labelled extrapolation from
a stated roadmap or physical argument, tier 3 labelled speculation with
no source. "Held at baseline" is the recorded outcome when no defensible
value exists.

**What is in here.** The coherence constraints the scripts enforce; the
plant environment, held and stepped; the tier 1, 2 and 3 records with
their sources; the coherent minimum and the $10 question; the breeder
that prices He-3; the robustness of the extrapolation device; and what
the ledger needs next.

**Orientation.** The machine is a pulsed inductive direct-conversion
generator with no turbine, its burning plasma a D-He3 FRC, 1 GWe as an
integer count of Helion-class modules; design basis in
`config/baseline.yaml`, capacitor and pulsed-power evidence in
`docs/capacitor_technology_report.md`, adversarial findings in
`docs/red_team_review.md` (all of whose verdicts are folded into the
tier composition below), narrative answer in `docs/Helion_writeup.md`,
whose Notation paragraph (Section 3) defines the symbols and knob names
used here.

**The design-basis shot.** The shot is solved, not cited. The driver
energy is the sourced 50 MJ; the yield is the smallest value, to 0.1 MJ,
at which one module (the 50 MWe unit Helion's CEO describes coming off a
gigafactory line, one a day, on a truck: Kirtley, Lex Fridman Podcast
485, 17 November 2025, at 2:17:48) at Helion's own burn point
(`config/baseline.yaml`: dd_frac 0.488, f_rad 0.23) nets the
power-purchase agreement's 50 MWe at the 1 Hz ceiling: 128.1 MJ, gain
2.56. The concept preset's yield pin (101.4 MJ, gain 2.03) rests on the
preset's default 1:1 D:He-3 mix, which no source outside the model
supports, and is not used.

On the preset's 0.5 m chamber the solved shot puts 1.75 MJ/m^2 per shot
on the wall against the 1.5 tungsten bound, so the Helion device is
costed in the smallest chamber that survives it: plasma radius 0.61 m
(wall radius 0.71 m, the coil bore right behind it) at the preset's 10 m
length, where the flash reads 1.48 MJ/m^2. The 1 GWe Helion device is 20
modules at 1 Hz, the 3 GWe park 60.

The power-purchase figure is a commercial commitment, not a physics
disclosure; the model reproduces it only with this shot. The shot is
also beyond Helion's own stated pulse: at the patent burn point a
millisecond burn returns under half a megajoule from the bank and 128 MJ
implies a 0.3 to 0.7 s burn (constraint 7), so the shot is a graded
claim at every grade, and the records device is priced at it only so
that a machine exists to cost.

**Version pin.** All numbers at costingfe `44434d9` (cylinder geometry +
wall-flux audit for linear pulsed concepts; shot-cycled CAS72
replacement scope; physics-consistent recovery-store markup; per-pulse
fuel-cycle semantics with species-resolved DHE3 recycle losses), pinned
by the regression tests in `tests/`. Account codes (CAS21, C220101 and
the like) are the model's cost-account structure. The tier stacks are
`config/best_case.yaml`, `config/tier2.yaml`, `config/tier3.yaml`;
`scripts/tiers.py` reproduces the ladder end to end.

**The four devices.** The writeup presents one device per evidence
grade, all on the plant environment of the held-and-stepped section
below: **citable records** is the tier-1 stack design-optimized,
**Helion's requirements** is Helion's configuration on the design basis,
**extrapolations** and **speculation** are the tier-2 and tier-3 stacks
design-optimized. Devices at 1 / 3 GWe:

| device | 1 GWe | at 7% real | 3 GWe | at 7% real |
|---|---|---|---|---|
| citable records (tier-1 stack, optimized) | 113.3 | 113.3 | 108.6 | 108.6 |
| Helion's requirements (Helion's configuration) | 105.9 | 105.9 | 102.1 | 102.1 |
| extrapolations (tier-2 stack, optimized) | 30.1 | 38.5 | 27.3 | 35.1 |
| speculation (tier-3 stack, optimized) | 12.4 | 20.5 | 10.1 | 17.3 |

The at-7% columns price the same machine at the design-basis cost of
capital with everything else as its grade has it (`scripts/tiers.py`,
`outputs/devices.csv`), so the financing part of each grade is the
difference: 8.4 and 7.8 $/MWh at extrapolations, 8.2 and 7.2 at
speculation, zero at the two 7% grades. Each 3 GWe park is the 1 GWe
device's module tripled.

**Regression pins.** Stack evaluations at Helion's configuration
(design-basis chamber), kept as internal regression pins: records 153.2
/ 148.5, extrapolations 32.4 / 29.0, speculation 12.0 / 9.4. The tier-2
and tier-3 stacks carry the D-rich mix of `config/tier2.yaml`, whose
0.68 s burn overruns the period at their granted ceilings (2.7 and 7.4
Hz on Helion's chamber in the fewest modules the grants permit), so
constraint 8 flags those two pins and nothing else does; the records
stack passes. The pins fire at the grants; the rate lever belongs to
the design search. The records device sits above Helion's requirements
because reverting Helion's per-pulse fuel recovery to the JET-analog
three nines is worth about 47 $/MWh at Helion's own mix (dd_frac 0.49),
most of which the records device recovers by running at the
deuterium-rich end of the mix grid (dd_frac 0.85, in 26 modules at 0.95
Hz under the 1 Hz grant) with the tritium store's He-3 return credited:
on evidence alone the fuel cycle is uneconomic, and the descent begins
when the recovery extrapolations are granted.

**Design search and bands.** The optimized devices choose chamber, wall
class, burn mix (seven mixes from the He-3-rich preset to the D-rich
end, each on its bremsstrahlung floor) and firing rate (a ladder of
`max_f_rep` ceilings at and below the lower of the grade's grant and
the duty bound of constraint 8, each rung forcing costingfe into more,
slower modules) by `scripts/coherent_min.py` under the
physics-consistency constraints in `scripts/study.py`; every grade gets
the design search, and constraint 8 sets the mix and the rate together.
Reconciliation bands around them (model gaps and conservatisms,
`scripts/reconciliation.py`): extrapolations within 24.6-34.6,
speculation within 11.3-13.6 at 1 GWe. With the coils priced along the
expansion adiabat (conductor growing as L^(1/3)), the design search
trades length for radius: the minimum is the same fat short chamber, 10
m x 0.75 m, at every grade. Two
open bands dominate, each priced in its own section below: the
compression field (the compression-field basis) and the recovery
topology at Slough's 40% flux-conserver ceiling (constraint 6).

## Coherence constraints (enforced, not advisory)

Eight couplings are applied to every quoted point. Constraints 1, 2, 3,
5 and 8 are checked by `study.coherence_violations`, and a stack that
violates one is flagged in the output of every script rather than
reported; constraints 4 and 6 are applied by construction in
`study.run`, which prices the tritium plant and caps f_pdv; and every
point carries the burn time the seventh implies at its own burn mix
(`tau_burn_implied_s`), which the eighth checks against the pulse
period:

1. **f_rad is coupled to the burn mix.** A D-rich plasma radiates more,
   not less: Bosch-Hale + bremsstrahlung at the study calibration (the
   blog-derived pair f_rad 0.163 at dd_frac 0.314 implies T_i 60-70 keV
   at T_e = T_i/2; Helion's own 0.23 at 0.488 with T_e = T_i sits above
   the floor) gives f_rad about 0.28 at dd_frac 0.85.
   `study.f_rad_floor` interpolates the review's computed anchors.
2. **Recovery is capped as a composite.** The only published figure on
   the plasma-to-electricity chain (Kirtley, APS DPP 2024: "optimal burn
   cycles exceeding 90% recovery") speaks to the product eta_dec x
   f_pdv. The extrapolation grade keeps engineering margin (composite <=
   0.80); speculation takes the theory optimum (0.90) with zero margin.
3. **The wall must survive the shot.** Steady flux within the bought
   first-wall class limit (the panel class at 2 MW/m^2; the
   divertor-class monoblock, `hhf` in the configs, at 10 MW/m^2), and
   per-shot flash energy under the tungsten millisecond-melt bound (1.5
   MJ/m^2, no margin).
4. **The D-rich fuel credit travels with its consequences.** From
   Helion's own mix upward (dd_frac 0.488) the machine is a bulk tritium
   facility: Helion's device carries 104 MW of plant-level neutron power
   and breeds 38 kg of tritium per year, the records device (dd_frac
   0.85) 405 MW and 146 kg/yr, the extrapolation device (0.80) 190 MW
   and 71 kg/yr, the speculation device (0.70) 112 MW and 42 kg/yr, and
   the D-rich extrapolation stack on Helion's chamber 211 MW and 78
   kg/yr; Helion's own store-for-decay fuel cycle implies an equilibrium
   getter-bed inventory of production rate x mean decay time, 0.67
   tonnes of tritium on site at Helion's device, 2.6 at the records
   device, 1.3 at extrapolations, 0.75 at speculation and 1.4 on that
   D-rich stack (writeup Section 5.1), against ITER's 4 kg site limit
   and the world's 25-30 kg civilian stock. `study.run` charges a
   tritium-plant adder on C220500, unit-priced rather than anchored: 50
   M$ fixed core plus 0.657 M$ per MW of plant neutron power (a stated
   definition; the 100-300 M$ reconciliation band at reference scale
   brackets it, and given the tonne-class inventory the allowance is
   more likely low than high). The adders, 118 M$ at Helion's device,
   316 at the records device, 175 at the extrapolation device and 124 at
   speculation, are consequences of throughput, not identities; every
   device sits above the threshold. O&M stays at the baseline 27.5,
   never at an "aneutronic" discount.
5. **dhe3_f_T is floored by the burnup closure.** The per-pulse D burnup
   pins the thermalized in-pulse tritium burn (f_T = 1 - (1 - e^-x)/x, x
   = (sv_DT/sv_DD)(-ln(1 - f_D))); any point whose dhe3_f_T sits more
   than 1% below that floor is flagged as coherent only under prompt
   MeV-triton loss. At the patent basis the floor is 0.002, so the
   design's dhe3_f_T = 0 passes; the constraint exists to catch any
   future high-burnup configuration that keeps the zero silently.
6. **f_pdv is derived, never asserted.** Each point's recovery fraction
   is min(claim, 1 - (V_i/V_f)^(2/3)) with V_i the compressed flux
   volume at the 22 T basis field (E_del/(B^2/2mu0), about 0.26 m^3 at
   50 MJ) and V_f its own chamber, the whole volume stroke counted, as
   Helion's burn-cycle framework (Kirtley, APS DPP 2024) counts it
   (writeup Section 6). The enforced expression is the
   Otto/Atkinson-form adiabatic-stroke bound at gamma = 5/3, and the
   Diesel-form ideal value of the machine's actual cycle sits 1-2
   percentage points below it at the study's ratios, so the cap is
   strict and slightly generous. Recovery cannot be claimed
   independently of the geometry that must deliver it. The adiabatic
   scalings say elongation falls as B^(1/5) during expansion, so nothing
   maintains aspect ratio; the plasmoid grows more oblate as it expands,
   and since tilt stability prefers prolate FRCs, the late expansion
   trades toward the tilt boundary, an unmodeled truncation risk on
   f_pdv that the composite cap's engineering margin partially absorbs
   at the extrapolation grade and speculation's zero margin does not.
   Slough (2025) caps the recoverable share of an FRC ejected into a
   flux-conserving expansion chamber at (1 - x_s^2)/(2.5 - x_s^2), 0.4
   at most, and holds that an FRC does not free-expand; that is the
   co-founder's own topology, not the discharged coil assumed here, and
   it is priced as a risk row (+21.8 / +8.2 $/MWh at the extrapolation /
   speculation device), not enforced. The 10 m x 0.75 m chamber the
   three optimized devices share bounds f_pdv at 0.940, above the
   extrapolation stack's 0.80 claim and below the speculation stack's
   0.947, which it clips.
7. **The shot is bounded by the plasma energy and the burn time.** The
   plasma at peak compression holds chi, the plasma-thermal share, of
   the delivered driver energy at the energy density of a beta = 1
   plasma and burns at the fusion power density of the burn point, so
   gain <= chi x burn time / breakeven time, with the breakeven time the
   ratio of those two densities: 86 ms at the patent point (22 T, 70
   keV, n_D 0.75e22, He3/D 0.158, Bosch-Hale rates) with thermalized
   electrons, 3.7 times shorter with electrons held at a tenth of the
   ion temperature, which the 1 ms ion-electron equilibration time at
   that density forbids for any burn long enough to matter (Lackner et
   al. 2026, JFE 45:12; Nicolas et al. 2026, JFE 45:24). Against
   Helion's stated pulse, "on the order of hundreds of microseconds to
   milliseconds" (helionenergy.com/faq, June 2026 capture in
   `docs/sources/`), a 1 ms burn returns 0.2 to 0.4 MJ from the 50 MJ
   bank across separatrix-to-coil radius ratios x_s of 0.5 to 0.85, less
   than the 2.5 MJ the circuit loses per shot even at the ladder's best
   inductive efficiency, tier 3's eta_dec 0.95; the design-basis 128 MJ
   shot implies a 0.3 to 0.7 s burn and the speculation shot, 150 MJ,
   0.4 to 0.9 s (`scripts/yield_bound.py`), and the bound reproduces
   Slough's (2025)
   own D-T design, where a gain of 9.1 on the FRC energy over a 2 to 5
   ms transit at 34.8 T and 15 keV is a 3.4 ms burn at that point's
   breakeven time (`study.breakeven_time_dt_s`). No record supports any
   yield, so the shot is a graded claim at every grade rather than a
   shared basis: the records device is priced at Helion's shot so that a
   machine exists to cost, and every point reports `tau_burn_implied_s`
   at x_s 0.7 and at the mix it actually burns, purchased He-3 plus the
   recycled bred He-3 (`study.breakeven_time_at_point_s`): 0.32 s at
   Helion's device (He3/D 0.22 with the recycled He-3 against the
   patent's purchased 0.16), 1.02 s at the records device, 0.62 s at the
   extrapolation device and 0.60 s at the speculation device's 150 MJ
   shot.
8. **The burn must fit inside the pulse period.** One burn section holds
   one plasmoid and the next shot cannot fire while the last is still
   burning, so `tau_burn_implied_s` x f_rep <= 1 (`study.DUTY_MAX`,
   checked in `study.coherence_violations`). The limit of 1.0 is the
   hard bound and leaves nothing for exhaust, refill and recharge, which
   a duty-cycle analysis would have to fit in the remainder. Since the
   implied burn is proportional to the yield, the duty is the module's
   fusion power over the cap chi E_del / breakeven time, whatever the
   split between shot size and rep rate, and the breakeven time
   lengthens with the deuterium content: 15 ms at the He-3-rich preset
   (a 1.76 GW cap), 65 at Helion's mix (401 MW), 104 at dd_frac 0.70
   (250 MW), 126 at 0.80 with four nines (206 MW) and 182 with three
   (144 MW), 138 at the D-rich 0.85 with four nines (188 MW) and 207
   with three (126 MW). The rule is evaluated at the reference x_s 0.7;
   the table below the list reads it across the span
   (`scripts/yield_bound.py`, `outputs/duty.csv`). The rule excludes no
   mix; it sets the rate at which a mix can fire, and the design search
   chooses the rate with the mix: a grade's granted ceiling is
   permission, not obligation, and each optimized device carries
   `max_f_rep` at the duty bound of its own burn, below the grant, so
   that costingfe builds it in the fewest modules whose rate fits. The
   deuterium-rich end of the mix grid (dd_frac 0.85), its best design at
   each grade under all eight constraints (`study.D_RICH_DEVICES`,
   `outputs/devices_d_rich.csv`), reads 113.3 / 108.6 (the records
   device itself), 30.8 / 27.4 and 13.0 / 10.7 $/MWh at 1 / 3 GWe;
   fired at the grants instead, in the fewest modules the grants permit,
   those designs would read 112.1, 26.8 and 10.6 at duties of 1.00, 1.87
   and 9.39 (`scripts/coherent_min.py`), and the rule excludes them. The
   rule therefore costs 1.2, 3.3 and 1.8 $/MWh at 1 GWe against the
   at-grant designs, and keeps the speculation park above the $10 target
   (10.1).

Constraint 8 across the x_s span, at 1 GWe:

| design | dd_frac | f_rep (Hz) | P_fus per module (MW) | cap at x_s 0.7 (MW) | duty at x_s 0.5 / 0.7 / 0.85 |
|---|---|---|---|---|---|
| citable records | 0.85 | 0.95 | 122 | 126 | 1.66 / 0.97 / 0.71 |
| Helion's requirements | 0.49 | 1.00 | 128 | 401 | 0.55 / 0.32 / 0.23 |
| extrapolations | 0.80 | 1.58 | 202 | 206 | 1.68 / 0.98 / 0.72 |
| speculation | 0.70 | 1.65 | 248 | 250 | 1.70 / 0.99 / 0.72 |
| extrapolations, D-rich end | 0.85 | 1.39 | 179 | 188 | 1.63 / 0.95 / 0.69 |
| speculation, D-rich end | 0.85 | 1.25 | 187 | 188 | 1.70 / 1.00 / 0.73 |

The three optimized devices sit at 97 to 99% of the bound at the
reference, since the search fires each in the fewest modules whose rate
fits its burn, pass at the fat-FRC edge, and would all be excluded at
x_s 0.5, where chi is 0.30; Helion's own device passes across the span.
The deuterium-rich end's designs at the two upper grades, two and three
modules slower than the devices, sit at 95 and 100%.

The store-and-decay idealization itself (dhe3_f_T = 0: no bred triton
burns in-plasma) is checked in `scripts/tritium_burn.py` against the
closure derived in the writeup's Section 5.2, under which the fuel cycle
is self-consistent only at low per-shot burnup bought back by rep rate.
At Helion's stated pulse of hundreds of microseconds to milliseconds
(helionenergy.com/faq, June 2026 capture in `docs/sources/`) and the
densities of the Trenta prototype (1e22-3e22 m^-3) the burn fraction
stays below about 1% and dhe3_f_T = 0 is a good approximation; at
reactor-class compression (1e23 m^-3) with millisecond-plus burn times
it reaches 4-13%. Priced at dhe3_f_T = 0.04 the extrapolation stack at
Helion's chamber moves only +0.6 $/MWh, but plant neutron power rises
23% and each burned triton emits a 14.1 MeV neutron (5.8x the D-D
neutron energy), so the LCOE story is insensitive while the shielding
basis and wall spectrum are not.

The model's own `burn_fraction` closes the same loop with no density or
burn-time input: the per-shot D burnup pins the integrated exposure n_D
<sigma v> tau, so f_T = 1 - (1 - e^-x)/x with x = (sv_DT/sv_DD)(-ln(1 -
f_D)). The concept YAML's burn_fraction 0.15 (an unsourced
magnetized-inertial-fusion literature midpoint; Helion publishes gain,
not burnup) implies an in-pulse tritium burn of 78-93% across 70-20 keV
if tritons thermalize and stay confined, inconsistent with dhe3_f_T = 0,
so that preset pair is not used. The operating space it spans is priced
rather than assumed. At or below about 7e-4 per-shot burnup the CAS80
recycle-loss line multiplies 15x at fuel_recovery 0.99 (2.4x at 0.999),
the bred-He-3 recycle credit collapses (effective recycle fraction 0.95
to 0.05-0.3) and vacuum-pumping throughput rises two orders. Prompt loss
of the 1 MeV tritons before they thermalize, a fast-ion confinement
question measurable on Polaris, also removes about four fifths of the
charged fusion energy at the D-rich mix, since the D-D proton is born
with the triton's momentum and the D-He3 proton with 2.2 times it; the
fuel-cycle price of that regime excludes it. Accepting the burn at
dhe3_f_T = 0.78 reads 46.2 at the extrapolation stack on Helion's
chamber, 40.6 at the extrapolation device, 15.5 at the speculation
device and 17.5 at the deuterium-rich end's speculation design, with
plant neutron power about 5x higher, a dominant 14.1 MeV component and
the decay store shrunk to 0.15-0.3 t; those figures are floors, because
the wall audit checks surface heat only, not the D-T-class neutron
loading it would imply.

**The fuel-cycle basis and its patent source.** Helion's fuel-cycle
patent (published as US 2017/0011811, granted as US 11,469,003 B2)
publishes an operating table (n_D = 0.75e22 m^-3, T = 70 keV, tau =
0.157 s without tritium removal / 0.103 s with it) and states tritium
"may be removed between each pulse ... prior to undesired D-T reactions
taking place". Read against the closure (writeup Section 5.2) the table
is its own case for inter-pulse removal, and the sub-millisecond pulse
satisfies dhe3_f_T = 0 with two orders of margin. The model basis
carries the per-pulse pair (burn_fraction 1.2e-4, burn_fraction_he3
4.1e-4, species-resolved recycle losses, fuel_recovery 0.9999), under
which fuel resides for of order a thousand pulses and the load-bearing
claims are four-nines per-pulse recovery and hertz-rate isotope
separation (unburned-fuel multiplier 84x / 9.3x / 1.8x at two / three /
four nines). Grade: published design intent; the reactor-point
compression density may exceed the patent value, which would move the
machine right along the burnup axis.

**Patents as sources.** A patent, granted or not, is evidence of design
intent, not of working physics: prophetic operating tables are legally
permitted, and grant examination tests claim novelty and formal
enablement, not whether the physics closes. This ledger therefore uses
patent numbers only in the design-basis grade and in tier-2
extrapolations accompanied by a physical argument, never as records: the
same discipline applied to the recovery-circuit patent's "up to 90% and
higher" band (graded prophetic under eta_dec). The fuel-cycle table
carries its own proof of prophecy: its tau column implies n tau of
2-3e21 s/m^3 at 70 keV, three to four orders beyond any demonstrated FRC
confinement (Wurzel and Hsu 2022, Phys. Plasmas 29 062103, is the
uniform triple-product ledger this claim is measured against), and the
study accordingly uses the table's density and temperature (whose field
companion, B = 22 T, follows from pressure balance and is corroborated
in class by Helion's stated compression field of more than 15 T) but
never its confinement time.

`scripts/burnup_scan.py` prices the whole axis coherently, sweeping both
triton branches at fuel_recovery 0.99, 0.999 and 0.9999 (writeup Section
5.2). At the patent-density basis the recovery nines carry the
speculation device's fuel line, which buys the He-3 its loop wastes:
12.4 $/MWh at fr 0.9999, 15.7 at 0.999, 46.6 at 0.99 (the fourth nine
is worth 3.3 $/MWh, the third 31; the device breeds most of its He-3,
so the nines bite on less than they would at a leaner mix). The axis
minimum (11.6 on the prompt-loss branch from burnup 1e-2 up, 11.8 at
1e-3 on the thermalized one) sits 0.6 to 0.8 $/MWh below the basis;
with 70% of its events D-D the thermalized branch turns up past burnup
0.003 as the tritium burn grows (4 to 90%), to 14.8 at 0.3, so the
triton-fate question reopens exactly where the recovery question
closes, and the deuterium-rich end's speculation design (13.0 / 15.0 /
31.0 at four / three / two nines) reads the same way. Per-pulse exhaust
pumping peaks at the basis (77 M$ across the speculation device's seven
modules, 107 across the extrapolation device's twelve).

The scan also reprices neutron damage, which the base model cannot see
(core_lifetime is inert for this concept): the exposed package is
levelized from the 14-MeV-equivalent neutron wall load at 20 and 50 dpa
on the basis set out in the writeup's Section 5.3. The event is C220101
+ C220103: the coil bore sits 0.10 m behind the wall with no blanket, so
the close-coupled copper coils see the same fluence and are replaced
with the wall (they are the cheap part: 75 vs 131 M$ across the
speculation device's seven modules under the adiabat coil pricing;
ceramic insulation is a prerequisite, since organics die at 1e9 rad in
weeks at these fluxes). At the patent basis the three optimized devices,
which share a chamber and fire at 95 to 100% of the duty bound, all
carry 0.12 MW/m^2 equivalent: +0.2 to 1.1 $/MWh at 50 to 20 dpa at the
speculation device (a 42-year changeout interval at 50 dpa), +0.3 to 1.6
at the extrapolation device (43 years) and +0.3 to 2.7 at the records
device (17.5 years at 20 dpa). The 8 to 19 $/MWh triton-fate spread at
the speculation device (17 to 36 at extrapolations) appears only in the
high-burnup counterfactual, where the extrapolation stack's
divertor-class wall makes replacement prohibitive (+52 to +135 $/MWh).
Two couplings the damage column exposes: low burnup raises
neutron damage as well as fuel cost (more D-D events per MWh), and
keeping the tritium out of the burn is free insurance at the basis and
worth double digits off it.

**Why the blanket escape is closed for the compression section.** The
flux-volume argument is in the writeup's Section 5.3. A 0.4 m shield
under the compression coil then multiplies the swept annulus by more
than an order of magnitude (C220107 and its CAS72 schedule scale with
the store), and the extra hundreds of MJ/pulse cycled at composite 0.90
dissipate tens of MJ/pulse: order 100+ MW of recirculating loss at the
tier-3 rep rate, and more than the module's output at the tier-2
composite. Eddy screening is the lesser problem (steel skin depth is
about 16 mm at ms rise times, so structure must be laminated; FLiBe at
200 S/m is magnetically transparent); the irreducible cost is the
magnetized volume itself. A shield is energetically cheap only around
the low-field regions of the machine (W scales as B^2: MJ-class per
pulse at 0.5 T and below). The coils nearest the burn are therefore
sacrificial, ceramic-insulated, and on the wall-replacement schedule,
which sharpens the tritium argument: the unshieldable compression
section is exactly where a 14 MeV spectrum hurts most. Honesty note the
other way: the scan spreads neutrons uniformly over the cylinder, but
the burn is localized near the compression section, whose wall and coils
see several times the average load on 15-20% of the event value; a
localized audit would raise the damage adders by very roughly 2x.
Together with the fission-spectrum 20 dpa edge and the 10x
helium-per-dpa of 14 MeV neutrons, the adders are more likely low than
high.

**When replacement becomes rebuilding.** Below the interval the
writeup's Section 5.3 derives, about 7 years at the speculation grade's
3% real (3.4 at 7%) and 3.4 years at the extrapolation grade's 5%, the
reactor line is replacement-dominated and the machine is opex. The
derived availability carries the changeout: 42 years at the speculation
device, 43 at extrapolations, 17.5 at the records device; the
consumable core (1-3 yr intervals, a quarter of the module's value
swapped near-annually) is the high-burnup thermalized counterfactual.
In that regime the honest design is Helion's factory logic taken to its
conclusion: a swappable irradiated cartridge with hot-spare bays (a
seven-module 1 GWe plant cannot hold its derived 0.93 availability
through annual month-scale swaps without a spare, at roughly one spare
module of extra capital), a refurbishment line, and a few hundred
tonnes per year of
activated steel and copper that neither the CAS50 decommissioning
provision nor C220110 remote handling is scoped for.
Consumable- core economics are marginal-manufacturing economics, which
is where the missing fleet-learning term would finally bind on something
real.

## Plant environment: held and stepped

The plant environment is priced in constant dollars (real framing) and
its entries fall in three classes. Held at every grade, carried in
`config/baseline.yaml`: the indirects, an analog transfer with the
reason below. Stepped with the tiers, as records in `config/tier2.yaml`
and `config/tier3.yaml`: the cost of capital, which is financing (a
change of risk-bearer, not of technology, and the one entry that Figure
1 and the ladder table's at-7% column keep separate from physics and
engineering); the book life, which is engineering (what cannot be
replaced sets it; nothing escalates with time in the real framing); and
the construction time, engineering as well, graded on the fission build
records and reaching the CCGT-class build only at speculation. Derived
at every point, never asserted: availability, from the replacement
schedule the model already prices.

Held at every grade:

| knob | repo default | value | why it applies | source (grade) |
|---|---|---|---|---|
| inflation_rate | 0.02 (code default) | 0.0 | Constant-dollar framing. With inflation_rate 0 the model discounts capital, replacement events, and operating costs at one real rate. The code default escalates only the operating costs (the overnight cost and replacement events are never escalated), a hybrid in which the nominal rate acts as a real rate on capital and the operating costs carry a 23% levelization premium at 30 years. Constant dollars is the IEA/NEA, EIA AEO, and NREL ATB practice. | Framing choice; see interest_rate (convention) |
| indirect_fraction | 0.20 | 0.20 (16.7 / 16.7 / 10.8 / 8.3% effective by grade) | Large industrial engineering, procurement and construction (EPC) analog, on the same cost-basis scope as NETL's EPCM line (fraction of total direct cost), at the NETL 20% that is also the model default. The model computes CAS30 = fraction x CAS20 x (construction_time_yr / 6 yr), so the effective fraction follows the build: 16.7% at the 5 yr grades, 10.8% at 3.25 yr, 8.3% at 2.5 yr. | US DOE/NETL Quality Guidelines for Energy System Studies (strong) |

Stepped with the tiers:

| knob | design basis | records | extrapolations | speculation | what it is | source |
|---|---|---|---|---|---|---|
| interest_rate (real) | 0.07 | 0.07 | 0.05 | 0.03 | financing: the cost of capital, a change of risk-bearer rather than of technology; Figure 1 and the at-7% column keep it separate | IEA/NEA 2020 (3%, 7%, 10% real cases, 7% central); 5% a loan-guarantee blend with precedent, 3% sovereign-class capital with no mechanism; no fusion plant has a record at any grade |
| lifetime_yr | 60 | 60 | 80 | 80 | engineering: what cannot be replaced sets it; bank and wall replacements are priced at every grade, so 80 yr is worth 0.6 $/MWh at the extrapolation device against 60; against the fusion literature's 30 yr (Böhnlein et al. 2026, median 30-40 yr; ARIES 40) the 60 yr entry is worth 5.1 $/MWh at the Helion device and 7.8 at the records device, and the 80 yr entries 5.5 at the extrapolation device and 3.6 at speculation (`outputs/devices.csv`) | 60: a series-consistency entry, not a record (see the note below the table); 80: US DOE hydropower lifespan 65-85 yr, every core component on its own replacement schedule |
| construction_time_yr | 5.0 | 5.0 | 3.25 | 2.5 | engineering: the build, which also sets the effective indirects through CAS30's build-time scaling; worth 1.9 $/MWh at the extrapolation device against 5 yr | 5 yr: the serial Hualong One builds, about 60 months from first concrete to grid (Zhangzhou 1, construction start October 2019 to grid 28 November 2024, World Nuclear News 2025); 3.25 yr: the Kashiwazaki-Kariwa ABWR pair, 37 and 39 months from first concrete to fuel load (Omoto 2002, Nuclear Engineering International), at the peak of a mature LWR supply chain; 2.5 yr: CCGT-class build (Siemens Energy 1200 MW block in about 30 months), which no fusion plant has a record of |
| availability | derived | derived | derived | derived | 0.98 outside planned outages, less a routine bundle (34 d every 2 yr), the bank swaps (34 d each at the shot life) and the wall-and-coil changeouts (84 d each at the dpa tolerance); `study.replacement_schedule` | US fission fleet (WNA, EIA, IAEA PRIS) for the 0.98 and the 34 d; Thea Energy Helios for the 84 d; see below |
| wall_dpa_tolerance | 20 | 20 | 50 | 50 | engineering: sets the changeout interval in the availability derivation (0.2 $/MWh at the extrapolation device) | 20 dpa: demonstrated RAFM database edge; 50 dpa: DEMO-class design target |

**The 60-year book life is a series-consistency entry, not the fission
record.** It is adopted to bring this plant in line with the other
candidate corridor studies, which hold 60 at their records rung, and
the ledger does not present it as demonstrated. The evidence beside it:
thirteen US plants hold NRC subsequent licence renewals to 80 years as
of June 2026 (Turkey Point 3 and 4, Peach Bottom 2 and 3, Surry 1 and
2, North Anna 1 and 2, Monticello, Oconee 1-3, Summer, Point Beach,
Browns Ferry 1-3, Dresden 2 and 3, Robinson 2, St. Lucie 1 and 2, Hatch
1 and 2; US NRC, Subsequent License Renewal,
nrc.gov/reactors/operating/licensing/renewal/subsequent-license-renewal);
the longest demonstrated operation is about 57 years (Beznau 1, in
service since 1969; Ginna at 55.9 years); and 60 years is the standard
first-renewal term, which is neither the licensed bound (80) nor
demonstrated operation (about 57). With the 1e8-shot bank at 1 Hz the
bank turns over about 17 times in 60 years, and the model prices every
one of them. The 80 years at the extrapolation grade rest on their own
mechanism, the US DOE hydropower civil-works lifespan.

The availability sources: 0.98 is the US fleet's capacity factor (over
90% since 2002, 92% in 2024; WNA, EIA) less refueling outages of 34-38 d
per 18-24 month cycle, which leaves 1-3% of unplanned loss; the fleet's
unplanned capability loss factor on IAEA Power Reactor Information
System data is 1.6% against a 4.1% world average (Glorian, WEC/Solomon;
IAEA RDS-2 2025 gives 4.2% world for 2022-2024). The 34 d routine bundle
is the EIA 2024 refueling outage, on a 24-month cycle, the long end of
the fleet's 18-24 month range, since this plant has no fuel reason to
open. The 84 d changeout is Thea Energy's Helios planned outage (arXiv
2512.08027), one every two years.

Derived availability per device at 1 GWe (`outputs/devices.csv`; the 3
GWe parks are within 0.001), with the three outage terms as fractions of
calendar time:

| device | availability | routine | bank swaps (every yr) | wall changeouts (every yr) |
|---|---|---|---|---|
| citable records | 0.895 | 4.7% | 2.7% (3.4) | 1.3% (17.5) |
| Helion's requirements | 0.901 | 4.7% | 2.9% (3.2) | 0.5% (43.9) |
| extrapolations | 0.925 | 4.7% | 0.45% (20.5) | 0.54% (43.0) |
| speculation | 0.929 | 4.7% | 0.05% (195.9) | 0.54% (42.4) |

The result sits just under the red-team review's 0.93-0.95 band and at
the top of the fusion literature's 0.75-0.90. Sensitivity, with
availability pinned instead of derived (`outputs/devices.csv`): the 3
GWe speculation park reads 10.8 $/MWh at the model default 0.85 and 9.9
at 0.95, so a pinned 0.95, 0.02 above the derived value, would put it
0.1 under the target; the extrapolation device moves 32.1 to 29.5 $/MWh
over the same span and the records device 116.0 to 110.4.

## Tier 1: records and published bounds

The records device grants the Helion device's claims except one: the
fourth nine of per-pulse fuel recovery, held below at its
evidence-supported value. The other unrecorded claim, the shot, has no
evidence-supported value above zero and is granted to both (constraint
7). The records device is then design-optimized like every other device.

**fuel_recovery: 0.9999 at the Helion basis, held at 0.999 (analog
argument).** An anti-record reversion: the Helion-implied four nines is
a concept-viability requirement (the He-3 economy fails without it),
which the hard nth-of-a-kind (NOAK) rule forbids as a basis value. The
per-pulse loss channel is wall retention plus pump slip in a sealed
loop; the closest measured analog is machine-scale gas-balance long-term
fuel retention on JET with its ITER-like wall (JET-ILW), 0.1-0.3% of
injected throughput (Brezinsek et al.). The analogy has category gaps in
both directions: campaign retention is co-deposition-dominated inventory
over many wall recycles, not single-transit loss (per-transit loss could
be far lower), and it measures none of the separation slip a per-pulse
isotope-processing plant adds (could be far higher); helium behaves
differently again. 0.999 is the defensible center of a range spanning at
least 0.99-0.9999, and the model default carries it.

**Held at baseline in tier 1:**

| knob | why not moved |
|------|---------------|
| c_cap_allin_per_joule (0.5) | Already at the optimistic end of its own documented 0.5-4.0 range; the industry statement is that Hz-rate operation still requires a 5-10x cost reduction. No record below the baseline exists. |
| eta_dec (0.85) | 0.97 is not tier-1-admissible: it is the top of a patent's prophetic circuit-only band (US 2024/0275198 A1), and Helion's "95% proven" statements trace to no-fusion circuit tests. Tier 2 carries 0.90 under the composite cap. |
| cap_shot_lifetime (1e8) | The 1e9 figure is a published NOAK *target* (Pacific Fusion's pulsed-power driver; Langtry et al. 2025, arXiv:2504.10680) resting on a vendor-catalog derating extrapolation, not a life test; the largest rep-rated MJ-class precedent is 1.3e4 shots. Tier-2 material by the study's own convention. |

## Tier 2: labelled extrapolations

Each entry carries its own grade in the table: a published target, a
record transferred from another industry, a physics floor, a design
purchase, or an unsourced roadmap step. None is a measured record of
this machine. See `config/tier2.yaml` for the per-knob notes.

| knob | baseline | value | basis | grade |
|------|----------|-------|-------|-------|
| cap_shot_lifetime | 1e8 | 1e9 | Pacific Fusion (Langtry et al. 2025) sec. 4.1: 100 to 35 kV derating projected to reach about 1e9 shots at about 9x lower energy density; General Atomics Series DE capacitor cross-check (3e7-3e9 at 20% reversal). At the extrapolation device each module fires about 3.7e9 shots over its 80-year book life at 1.58 Hz, so the bank is replaced about 4x (every 20.5 years, charged to CAS72 by the model); the "1e9 outlives the plant" argument holds only below about 0.4 Hz. The largest lever at this device: +36.0 $/MWh reverted. | published target |
| fuel_recovery | 0.999 (tier-1 record) | 0.9999 | One nine beyond the JET-ILW retention record: the patent closed fuel cycle (US 2017/0011811) implies four-nines per-pulse recovery for the He-3 economy to close, and the physical argument (saturated walls, helium-dominated exhaust, direct re-injection without full reprocessing) points the right direction. No demonstration at any scale. Worth 10.1 $/MWh at the extrapolation device if reverted, with the store's He-3 return credited: the loop wastes 71% of what it buys at three nines, but the device breeds most of its He-3 and buys little; the less He-3-rich plasma's 0.89 s burn overruns the 0.66 s period at 1.52 Hz, so the reverted point also trips constraint 8. | patent-implied extrapolation |
| eta_dec | 0.85 | 0.90 | Bottom of the patent band, circuit-only, no fusion-inclusive measurement. Paired with the basis f_pdv under the composite cap (0.90 x 0.80 = 0.72 <= 0.80 at the extrapolation device, where the chamber's adiabatic bound, 0.940, sits above the claim). | weak-moderate |
| f_pdv | (derived) | min(claim, expansion bound) | Not a record: capped per point under coherence constraint 6 by the chamber's adiabatic expansion bound on the whole volume stroke; at the extrapolation device's chamber the bound (0.940) sits above the tier's 0.80 claim, so the claim stands. | constraint-derived |
| eta_pin | 0.95 | 0.98 | Solid-state pulsed-power wall-plug efficiency; plausible for modern semiconductor switching, no datasheet or Helion statement located. | UNSOURCED |
| max_f_rep | 1.0 | 3.0 granted; 1.608 used (12 modules at 1.58 Hz) | The grant: no public Helion statement of a numeric plant rep rate exists (Polaris target about 1/s; Trenta about 1/10 min; the 1-10 Hz band is the concept YAML's roadmap paraphrase). 3 Hz is what the bought wall supports at this tier's recovery parameters; it remains UNSOURCED as a demonstrated cadence (nothing MJ-class has run at 1 Hz continuously). The band top (10 Hz) is speculation. The rate used: a grant is permission, not obligation, and the design search sets the device's ceiling at the duty bound of its own 0.62 s burn (constraint 8), 1.61 Hz, so that costingfe builds it in the fewest modules whose rate fits, 12 at 1.58 Hz. The grant above 1.6 Hz is worth nothing to this device; reverting the ceiling to the records grade's 1 Hz costs 6.0 $/MWh, the step from 12 modules to 20. | UNSOURCED-ROADMAP (grant); design choice (rate) |
| fw_class | panel | hhf | Machine-design purchase, not a record: divertor-grade monoblock wall (ITER divertor procurement anchor, 2.5 M$/m^2 NOAK, 10 MW/m^2 qualification) over the real 44.6 m^2 cylinder, 112 M$/module, to make 3 Hz admissible in the design-basis chamber. The extrapolation device instead buys a fatter chamber with the cheaper panel wall and fires at 1.6 Hz (see coherent minimum below). | design purchase |
| dhe3_dd_frac | 0.488 (the patent's He3/D = 0.158 at 70 keV as a D-D event share) | 0.85 granted; 0.80 used | D-rich operation to raise in-situ He-3 breeding (prompt D-D He-3 plus stored-tritium decay) and cut the purchased-fuel line; the concept's own stated direction, but 0.85 is the top of a sweep, not a derived operating point. Adopted only jointly with f_rad 0.28 and the tritium-plant adder (coherence constraints 1 and 4). Slough (2025) restates the patent's mix as the self-sustained cycle's limit, citing the same patent, and puts the D-He3 gain at equal FRC conditions a factor of 240 below D-T's ("the D-T gain advantage of 240", from its eq. 5), which is why the reactor he designs there is D-T (verified against the paper; `docs/sources/slough_2025_notes.md`); 0.314, the blog's 3:1 D:He-3 bremsstrahlung minimum, is the floor's calibration anchor. The design search runs the extrapolation device one step short of the grant, at dd_frac 0.80 (30.1 $/MWh) against 30.8 at 0.85: the D-rich plasma's 0.68 s burn (four nines) overruns the 0.36 s period at the grant's 2.7 Hz (constraint 8, duty 1.87) but fits at 1.40 Hz in 14 modules, two more than the 0.80 mix needs at 1.58 Hz, and the extra modules cost more than the He-3 the richer mix breeds. The mix is the second lever at this device: reverting it to Helion's 0.488 costs 11.6 $/MWh. | UNSOURCED |
| f_rad | 0.163 | 0.28 | Bremsstrahlung-consistent radiated fraction at dd_frac 0.85 under the study calibration; relativistic corrections would raise it another 10-25%. Not an optimistic move: it is the price of the fuel credit. The extrapolation device, at dd_frac 0.80, sits on its own floor, 0.27; Helion's 0.23 would sit below it and is not a coherent point there (0.4 $/MWh cheaper). | physics floor |
| interest_rate | 0.07 real | 0.05 real | Cost of capital (financing): federal loan guarantees blended with utility equity, a mechanism with precedent but no fusion record, between the IEA/NEA 2020 central and low cases. The one entry that is financing rather than technology; Figure 1 and the at-7% column keep it separate (worth 8.4 $/MWh at this device against 7%). | mechanism with precedent |
| lifetime_yr | 30 | 80 | Book life (engineering): US DOE hydropower lifespan (65-85 yr) with every core component replaced on its own schedule; the unreplaceable structure sees negligible neutron fluence (copper coils are replaced with the wall, D-D neutrons only). Bank and wall replacements are priced at every grade, so the model shows where 80 yr pays: 0.6 $/MWh here against the 60 yr below it, with the bank turned over about 4x. | civil-works record |
| construction_time_yr | 5.0 | 3.25 | Construction (engineering): the Kashiwazaki-Kariwa ABWR pair, 37 and 39 months from first concrete to fuel load (Omoto 2002, Nuclear Engineering International), at the peak of a mature LWR supply chain, against the 5 yr held at the design basis and records grades (the serial Hualong One builds, about 60 months from first concrete to grid (Zhangzhou 1, construction start October 2019 to grid 28 November 2024, World Nuclear News 2025)). Also lowers the effective indirects from 16.7% to 10.8% through CAS30's build-time scaling; worth 1.9 $/MWh at this device against 5 yr. | demonstrated once |
| wall_dpa_tolerance | 20 | 50 | DEMO-class RAFM first-wall design target against the demonstrated 20 dpa database edge; enters only through the changeout interval in the derived availability (0.2 $/MWh). | design target |

**Held at baseline in tier 2:** om_cost_dhe3 (27.5: already the lowest
documented CCGT fixed-O&M figure; also required by coherence constraint
4), installation_frac (0.14: no defensible record on the model's cost
basis), f_rad as an independent mover (a coupled variable, not a knob).

## Tier 3: labelled speculation

No entry has a source; each is the optimistic edge of a stated argument
or an explicit leap. See `config/tier3.yaml` for the per-knob notes.

| knob | value | note |
|------|-------|------|
| max_f_rep | 10 granted; 1.663 used (7 modules at 1.65 Hz) | the grant is the top of the third-party roadmap band, and no duty-cycle analysis supports it; the speculation device fires at the duty bound of its own 0.60 s burn (constraint 8), 1.66 Hz, in the fewest modules whose rate fits, so the grant above 1.7 Hz is worth nothing to it |
| cap_shot_lifetime | 1e10 | required for coherence with 10 Hz; no source at any price; jointly heroic with the $/J entry below. At the 1.65 Hz the device uses, each module fires about 4e9 shots over the 80-year book life, so the 1e10 bank outlives the plant (a 196-year swap interval); the entry is worth 5e9 shots of margin the device does not spend |
| eta_dec x f_pdv | 0.95 x 0.947 = 0.90 claimed; 0.95 x 0.940 = 0.89 run | the theory-optimal composite taken at face value, zero engineering margin; the claimed f_pdv 0.947 is clipped to 0.940 by the 10 m x 0.75 m chamber's adiabatic bound (constraint 6), so the composite the device runs at is 0.89. The source figure (Kirtley, APS DPP 2024, 'optimal burn cycles exceeding 90%') is unreproducible: its numerator is independently verified but its input-accounting denominator is defined in neither slide nor talk (docs/sources/kirtley_dpp24_formulas.md) |
| c_cap_allin_per_joule | 0.1 | below the model's own documented range floor; contradicts the derating physics that buys the cap life above |
| u_he3 | 5e5 $/kg | no fleet-scale He-3 market exists at any price. The DOE Isotope Program's 2011 allocation was 600 $/L to federal and 1,000 $/L to commercial users (CRS R41419), 4.5-7.4 M$/kg, and prices have risen several-fold since: the 2024-2026 transactions are gram-to-kilogram scale at 19-22 M$/kg (Edelgas spot; Interlune's DOE and Maybell Quantum agreements at the commercial price; TAE's Black Moon lunar option undisclosed), with every new entrant building toward the high price. This entry is 9x below the 2011 allocation and 40x below the commercial spot. The breeder section below prices the He-3 each device buys: 2.1 M$/kg at the records grade against the ledger's 2, unexplainable at the Helion device (6.6 co-sited, 7.4 standalone), 0.9 co-sited at the extrapolation grade (1.3 standalone), and 0.4 co-sited at speculation (0.8 standalone) against this entry. The speculation device buys 45 kg/yr at it, 0.9 $/MWh of its 12.4. |
| dec_staged_recovery_factor | 0.5 | patent's unquantified "net reduction in cost and size", optimistic edge |
| c_inv_per_kw_net | 50 $/kW | small lever |
| multi_unit_labor_factor | 0.80 | small lever |
| interest_rate | 0.03 real | IEA/NEA 2020 low case: sovereign-class capital with no mechanism that delivers it to a first-of-a-kind fleet; financing, shown separately (worth 8.2 $/MWh at 1 GWe and 7.2 at 3 GWe against 7%) |
| construction_time_yr | 2.5 | CCGT-class build (Siemens Energy 1200 MW block in about 30 months) for a fusion module with a tritium facility; no fusion plant has a build record; effective indirects 8.3% at this build |
| yield_per_shot_mj | solved, not asserted; a graded claim at every grade (constraint 7) | no record supports any yield: Helion's stated pulse returns under half a megajoule from the 50 MJ bank, the design-basis 128 MJ shot implies a 0.3 to 0.7 s burn and the speculation shot, 150 MJ, 0.4 to 0.9 s (`scripts/yield_bound.py`), so the records device is priced at Helion's shot only so that a machine exists to cost. Gain speculation is admitted, but the shot must be survivable in the chamber it is costed in: `coherent_min.py` solves yield, chamber and rate jointly. With the rate a design choice the optimum sits at the design-basis shot's neighbourhood: 128.1, 150 and 200 MJ shots at dd_frac 0.70 in 7 modules of 10 m x 0.75 m panel-wall chambers read within 0.02 $/MWh of each other (12.4), 300 MJ 0.3 behind, and the He-3-rich single-module designs of 200 to 750 MJ in a 15 m x 1.5 m chamber 0.6 behind (13.0); 150 MJ is carried, and the gain speculation buys nothing. Gain 40 (2000 MJ) in the concept preset's 0.5 m x 10 m chamber deposits about 6.7 MJ/m^2 per shot, four times the tungsten flash-melt bound, and is excluded. |

## The coherent minimum, and the $10 question

`scripts/coherent_min.py` searches the design space the machine actually
controls (yield, chamber size, wall class, burn mix) under the coherence
constraints, at each evidence level:

| device | LCOE | design |
|---|---|---|
| citable records, 1 GWe | **113.3** | design-basis shot at the deuterium-rich dd_frac 0.85 with its tritium plant, 26 modules of 10 m x 0.75 m at 0.95 Hz under a 0.98 Hz ceiling, the duty bound of its 1.02 s burn (the mix freedom every grade gets, and the rate with it: at the 1 Hz grant the same design is 25 modules at 0.98 Hz, duty 1.00, excluded, at 112.1; the 0.80 mix reads 115.3 in 24 modules at 0.98 Hz; the 15 m x 0.5 m chamber is 1.6 $/MWh behind, the 10 m x 1.0 m 1.9) |
| citable records, 3 GWe | **108.6** | the same design, 76 modules at 0.97 Hz |
| extrapolations, 1 GWe | **30.1** | design-basis shot (128.1 MJ), 12 modules of 10 m x 0.75 m at 1.58 Hz under a 1.61 Hz ceiling, panel wall, dd_frac 0.80 with its tritium plant, the fewest modules whose rate fits the 0.62 s burn (the deuterium-rich end, 30.8, needs 14 modules at 1.40 Hz; Helion's mix reads 37.7 in 6 modules at 2.70 Hz, the 3:1 mix 41.4, the He-3-rich preset 44.5; at the 3 Hz grant the device's own design is 7 modules at 2.67 Hz, duty 1.66, excluded, at 26.5) |
| extrapolations, 3 GWe | **27.3** | the same design tripled, 36 modules at 1.58 Hz |
| speculation, 1 GWe | **12.4** | 150 MJ shots in 7 modules of 10 m x 0.75 m at 1.65 Hz under a 1.66 Hz ceiling, panel wall, dd_frac 0.70 with its tritium plant (the 128.1 and 200 MJ shots read the same, within 0.02 $/MWh; the whole mix grid sits within 0.6: 0.60 at 12.8 in 6 modules, 0.80 at 12.7 in 9, Helion's mix 12.9 in 4, the 3:1 mix 13.0 in 3, the deuterium-rich end 13.0 in 10 and the He-3-rich preset 13.0 as a single 500 MJ module in a 15 m x 1.5 m chamber at the grant, the one design the grant itself builds; at the 10 Hz grant the device's own design is 2 modules at 5.7 Hz, duty 3.4, excluded, at 10.7) |
| speculation, 3 GWe | **10.1** | the same design tripled, 21 modules at 1.65 Hz (the deuterium-rich end's park reads 10.7 in 30 modules at 1.25 Hz) |

Chamber length is a design variable, not an evidence-tier entry, the
same category as the wall class: nothing about a longer vessel with more
coil sections requires undemonstrated technology, and the design search
is entitled to choose it. For context, the built envelope is Trenta 15 m
and Polaris 19 m (the length of Orion, the first plant, is undisclosed),
with Helion's published geometry symmetric (formation and acceleration
at both ends, merge-compression central, expansion back against the same
compression coils). Every added meter is active pulsed structure (coils
ramped each cycle, switched into the recovery circuit, fatigue-cycled
every shot), and the model prices it: C220103 integrates the solenoid
ampere-turn identity along the machine's own expansion adiabat, so
conductor grows as L^(1/3). Under that pricing the design search trades
length for radius and the minimum is the same fat short chamber at
every grade (10 m x 0.75 m), inside the built length envelope. The
public
facility imagery also corroborates the cost structure at today's prices:
most of the Polaris building's floor is the pulsed-power farm (about
2,500 stacked power units) with the fusion machine in a small corner,
which is precisely the picture the tier-3 capacitor $/J and shot-life
entries claim will invert.

Reconciliation (`scripts/reconciliation.py`) puts honest bands around
these. The shot-cycled replacement of the recovery store and switch
stack (CAS72, with the bank) and the recovery-store markup (f_pdv (1 -
f_rad)) are inside costingfe and priced in every number above. What
remains outside: high-voltage DC switch repricing (+1.2 extrapolation /
+0.7 speculation), the driver-thermalization derate (below), the
tritium-plant band (both devices sit above dd_frac 0.5: -0.6 to +0.6
around the unit-priced 175 M$ adder at extrapolations, -0.4 to +0.4
around the 124 M$ at speculation), and a thermal-bottoming basis change
(-4.9 / -0.7): the extrapolation device lands in 24.6-34.6, the
speculation device in 11.3-13.6 at 1 GWe.

The driver-thermalization derate closes a disposal channel the physics
path misses: it recovers the entire delivered driver energy at flat
eta_dec (the model's net electric power is p_dee = eta_dec (p_driver +
p_pdv) - p_driver, from the driver and expansion-work streams), as if
all of it stayed in field form, but the machine has no auxiliary heating
(merging shock plus compression work ARE the heating, all driver-fed),
so the plasma-thermal share chi can only return through the same
expansion channel as the fusion heat, at f_pdv. chi is not a free
parameter: at peak compression the FRC equilibrium pins it through the
average-beta theorem (<beta> = 1 - x_s^2/2), giving chi = 1.5 <beta>
x_s^2 / (1.5 <beta> x_s^2 + 1 - x_s^2), a function of the
separatrix-to-coil radius ratio alone: x_s 0.5/0.7/0.85 maps to chi
0.30/0.52/0.71, so fat FRCs are high-chi machines and good FRC
confinement physics pushes the derate up. The extra recirculating loss
eta_dec chi (1 - f_pdv) p_driver is worth +1.6/+2.7/+3.7 $/MWh at the
extrapolation device across that x_s span (947 MW of circulating driver
power) and +0.1 to +0.3 at the speculation device (578 MW); at the
low-gain
Helion device it would be order +10. The Polaris shot triplet (vacuum /
plasma no-burn / burning) separates eta_dec, chi (1 - f_pdv), and the
fusion composite, so the study's most-wanted measurement delivers chi as
a by-product; until then, published excluded-flux radii (x_s) pin it per
shot. The disposal of the FUSION heat is already in the model: f_rad
radiates to the wall, (1 - f_pdv) of the remainder is dumped undirected
at end of pulse, and eta_th = 0 discards the lot, which is what drives
the wall-flux audit and the bottoming credit. The expansion bound is
enforced as coherence constraint 6 (f_pdv capped per point by the
chamber's expansion ratio on the whole volume stroke): the 10 m x 0.75
m chamber the three optimized devices share caps it at 0.940, above the
extrapolation device's claimed 0.80 and below the speculation stack's
claimed 0.947, which it clips; whether the end circuits return the
axial fifth of the work is resolvable by the Polaris shot triplet.
Parallel particle
streaming through the exhaust is captured by nothing at any grade.

**The He-3 market makes the fuel accounting first-order.** At the DOE
Isotope Program's 2011 allocation of 4.5 M$/kg (he3_scan's 4.5e6 row)
the extrapolation device reads 33.3 $/MWh at its own mix (dd_frac
0.80), 59.1 at Helion's mix (0.488) and 70.1 at the 3:1 mix (0.314), in
the same chamber at the same 1.61 Hz ceiling; at the 19-22 M$/kg
commercial spot (the 2e7 row), 52.8, 174.3 and 229.6: the leaner mixes
do not survive market-priced He-3, and the device, which breeds most of
its own, pays 23 $/MWh for the spot. The D-rich column is nearer
indifference (31.8 and 42.6) but overruns the device's period at its
ceiling (constraint 8) and is starred in the scan's table; it fits two
modules slower. That reading follows from the model's fuel accounting:
prompt bred He-3 is credited through its species-resolved cumulative
recycle fraction (0.80 at the per-pulse basis: He-3 burns out of the
loop 3.3x faster per pass than it leaks), and the decay store's He-3
return, 0.5 dd_frac atoms per primary event and equal to the prompt
branch, is credited atom for atom against the purchased 1 - dd_frac per
event, levelized over the store's build-up at the grade's rate
(`study.he3_purchase_fraction`: 0.22 / 0.79 / 0.23 / 0.31 of the
perpetual purchase down the ladder; `he3_decay_return=False` restores
the perpetual purchase). The extrapolation device imports 44 kg/yr and
the speculation device 45 kg/yr, of which the store's return covers
three quarters and two thirds, levelized. The u_he3 = 0 row (27.6 $/MWh
at the device's own mix in its chamber) is the free-fuel limit at that
machine; at zero price the mix itself changes: the design search re-run
at u_he3 = 0 (`he3_scan.optimum_by_mix`, `outputs/he3_free_by_mix.csv`)
picks the He-3-rich mix (dd_frac 0.131) in 15 m x 0.75 m chambers at
the 3 Hz grant at 20.3 $/MWh for the extrapolation grade (21.0 at the
3:1 mix, 22.6 at Helion's, 27.6 at the device's 0.80) and, with 300 MJ
shots in a 15 m x 1.5 m single-module chamber at the 10 Hz grant, 8.5
for speculation (17.7 and 6.5 at 3 GWe), with no tritium plant, so a
free-He-3 concession is worth 9.8 and 3.9 $/MWh at 1 GWe, against the
2.5 and 0.8 the devices show at their own mixes. The credit is worth 8.4
$/MWh at the study's u_he3 at the extrapolation device (38.5 without
it) and 35.4 at the records device (148.7 without it), and it is coupled
to the burnup closure, because the return exists only if the tritium
survives the
pulse.

**No stack crosses the $10/MWh target.** The full speculation stack as a
3 GWe park reads 10.1 $/MWh (12.4 at 1 GWe), 0.1 above it, with the
wall-and-coil replacement hardware of `burnup_scan.py` adding 0.2 to 1.1
$/MWh at 50 to 20 dpa. What brings it that close is the cost of capital,
not a physics or engineering entry: the same machine at the design-basis
7% real reads 17.3 $/MWh (20.5 at 1 GWe), so the 3% real
sovereign-class rate is worth 7.2 $/MWh at the park, seventy times the
remaining gap; the figure also needs the derived availability of 0.93
(10.8 $/MWh at the model default 0.85), and it sits at 99% of the duty
bound, with nothing in the period left for exhaust, refill and
recharge. Fired at the 10 Hz grant in the fewest modules the grant
permits, the deuterium-rich speculation design would cross, 10.6 at 1
GWe at a duty of 9.4 (`scripts/coherent_min.py`); fired slow enough to
fit it reads 13.0 and 10.7 (`outputs/devices_d_rich.csv`). He-3 at zero
price takes the coherent park to 6.5 $/MWh with the design search
re-run at that price (the He-3-rich preset, 200 MJ shots in a 15 m x
1.5 m chamber at 6.8 Hz, no tritium plant; `scripts/he3_scan.py`), so
the He-3 price alone is the whole distance to the target. What carries
the floor at the speculation device is not the capacitor bank (36 M$ of
a 784 M$ reactor account across seven modules): it is buildings (CAS21
284 M$), CAS50 (204 M$), heat rejection and electrical plant (CAS24-26
about 171 M$), fuel handling with the tritium-plant allowance (164 M$),
the first walls of the seven chambers (131 M$), O&M (4.8 $/MWh) and the
annualized capital (6.6 $/MWh); the He-3 it buys (45 kg/yr at 0.5
M$/kg) is 0.9 $/MWh. See `docs/Helion_writeup.md` for the
account-by-account anatomy and the small-plant-penalty analysis.

## The breeder as the price of He-3

`scripts/breeder_loop.py` prices the He-3 each device buys as the output
of a dedicated pure-deuterium breeder of the same grade (the device's
own module, shot with the He-3 taken out of the fill, its prompt He-3
and tritium pumped out every pulse): module ownership plus a
throughput-sized tritium plant plus its net power at the device's own
LCOE, per kilogram delivered at an equilibrium decay store. Co-sited
prices the breeder as reactor-plant equipment in the park and standalone
as its own plant; financing the decay wait at the grade's rate adds 1.2
to 1.4x. Each device is then re-run at that price with its own LCOE as
the power price.

| device | He-3 bought (kg/yr) | breeder output (kg/yr per module) | co-sited (M$/kg) | standalone (M$/kg) | device at co-sited / standalone price ($/MWh) |
|---|---|---|---|---|---|
| citable records | 177 | 12.3 | 2.1 | 2.3 | 113.6 / 115.0 |
| Helion's requirements | 98 | 5.6 | 6.6 | 7.4 | 151.1 / 159.2 |
| extrapolations | 44 | 14.2 | 0.89 | 1.26 | 28.7 / 29.2 |
| speculation | 45 | 15.2 | 0.36 | 0.80 | 12.1 / 12.9 |

The ledger price of 2 M$/kg is read back at the records grade (2.1
M$/kg co-sited), cannot be reached at the Helion device (a module that
breeds 5.6 kg/yr at a gain of 0.46), is beaten at the extrapolation
grade (0.89 M$/kg, so the device at its own breeder's price reads 28.7
$/MWh against 30.1 at the ledger price) and at speculation (0.36 against
the 0.5 entry co-sited; the standalone breeder, 0.80, would take the
device to 12.9). The three optimized devices breed most of the He-3
they burn, so the breeder price moves them by 1.4 $/MWh at most. A
central facility serving several devices reads 1.75 to 0.91
M$/kg at the extrapolation grade for one to twenty devices
(`outputs/breeder_siting.csv`), since the fixed tritium core and the
standalone intercept spread over more kilograms. The scheme relocates
the tritium inventory rather than shrinking it.

## Robustness of the extrapolation device

One-at-a-time reversion from the 30.1 point (`scripts/tornado.py`;
reverted points that leave the coherent set are marked):

| knob reverted | LCOE | delta |
|---|---|---|
| cap_shot_lifetime -> 1e8 | 66.1 | +36.0 |
| dhe3_dd_frac -> 0.488, f_rad -> 0.23 (Helion's mix with its own radiated fraction, in the device's 12 modules under its 1.61 Hz ceiling) | 41.8 | +11.6 |
| fuel_recovery -> 0.999 (JET-analog; overruns the period, duty 1.36) | 40.2 | +10.1 |
| interest_rate -> 0.07 (financing) | 38.5 | +8.4 |
| max_f_rep -> 1 Hz (20 modules at 0.97 Hz against the device's 12 at 1.58) | 36.2 | +6.0 |
| eta_dec -> 0.85 | 32.6 | +2.4 |
| construction_time_yr -> 5 yr | 32.1 | +1.9 |
| eta_pin -> 0.95 | 31.6 | +1.4 |
| lifetime_yr -> 60 | 30.8 | +0.6 |
| wall_dpa_tolerance -> 20 | 30.3 | +0.2 |
| f_rad -> 0.23 (Helion's own; below the 0.27 floor at dd_frac 0.80, so not a coherent point) | 29.7 | -0.4 |
| fw_class -> panel | 30.1 | +0.0 |

The cap-life lever counts the full shot-cycled recovery chain (bank,
store and switch stack, CAS72): at 1e8 shots everything that cycles is
replaced about every two years, about 40 times over the 80-year book
life. Four extrapolation entries carry the number: the capacitor life
at +36 (a published derating target), the burn mix at +12 (reverted to
Helion's mix the device breeds less He-3 and buys more), the per-pulse
fuel recovery at +10 with the store's He-3 return credited (an
extrapolated nine beyond the JET retention record; smaller here than
at Helion's mix, where it is worth 47, because the device breeds most
of its He-3) and the rate at +6 (an unsourced roadmap band, but the
device uses only 1.6 Hz of the 3 Hz grant, so the row is the step from
12 modules to 20 rather than the grant's worth); then the environment
entries, the cost of capital (financing, +8.4), the build (+1.9) and
the book life (+0.6 against the 60 years below it). f_pdv does not
appear: the extrapolation stack leaves it at the basis 0.80 under a cap
that does not bind. None is a record. That is the honest quality of the
30.1 figure.

## Knobs with no effect

`core_lifetime_dhe3` moves LCOE by exactly zero at every operating point
quoted here. Recorded so it is not mistaken for an untested lever; which
is why wall replacement enters through the coherence constraints rather
than through that knob.

## The compression-field basis

The coil account prices all coils at the 22 T basis field (conservative:
the expander's guide coils run far lower), the compressed flux volume
behind constraint 6 and the shield-magnetization argument uses the same
field, and the fuel-cycle burnup follows from its density companion: one
operating point, used consistently. Two consequences are open items: (a)
if the reactor-point field is lower, burnup falls as B^2 and the
recovery nines bind harder (the field/density RISK rows in
reconciliation: +3.1 / +14.0 $/MWh at the speculation device for 10 T /
5 T, +8.3 / +38.4 at the extrapolation device); (b) the magnetic
pressure at 22 T is about 193 MPa, cycled
1e9-1e10 times at the rep rate, at or above copper-alloy gigacycle
fatigue strengths (100-150 MPa): the compression coil's replacement
schedule may be set by mechanical fatigue rather than neutron dpa, a
third member of the shot-cycled replacement family that neither the
damage scan nor CAS72 currently prices.

## What the ledger needs next

1. The burning shot on Polaris: its yield at its measured burn time,
   read against constraint 7 (the whole plant hangs on it: at Helion's
   stated pulse the bank returns under half a megajoule), and its
   fusion-inclusive round-trip recovery efficiency, separating the
   circuit factor eta_dec from the expansion-work factor f_pdv, which
   gates the composite-recovery entries directly and, through the
   wall-load budget, the honest rep-rate ceiling. Every other open item
   moves single $/MWh; the recovery efficiency moves tens, and the yield
   moves everything.
2. A duty-cycle analysis for any rep rate above about 1 Hz. Constraint
   8 holds only the burn inside the period, at the hard bound of 1.0,
   and the three optimized devices sit at 97 to 99% of it, because the
   design search fires each in the fewest modules whose rate fits its
   burn; any allowance at all for the exhaust, refill and recharge that
   must fit in the remainder adds modules, at about 0.3 $/MWh per module
   at the speculation device and 0.75 at the extrapolation device. The
   switch and capacitor cycle life, vacuum recovery at 600-1000 ms
   periods, and coil and chamber thermal management are unpriced.
3. A sourced capacitor cost-at-life curve, replacing the single Pacific
   Fusion target point and resolving the c_cap / cap_shot_lifetime joint
   optimism the tier-3 stack currently carries.
4. A costed tritium plant scope for the D-rich fuel cycle (the 100-300
   M$ band here is an allowance, not an estimate), including its
   licensing posture.
5. A measured per-pulse burnup and extraction cycle for the
   reactor-scale machine. Helion's patent (US 2017/0011811) settles the
   design intent: low per-pulse burnup (about 1e-4 at its published
   density) with inter-pulse tritium removal, which validates dhe3_f_T =
   0 and rules out the concept preset's burn_fraction 0.15 as a
   per-pulse value. What remains unmeasured: the reactor-point
   compression density (higher density moves the machine right along the
   burnup axis and revives the in-pulse burn), the demonstrated
   per-pulse isotope-separation rate, and the per-pass fuel recovery,
   four nines of which are required at the published point. The same
   knob set sizes the vacuum pumping, the fuel recycle loss, and the
   bred-He-3 credit (`scripts/tritium_burn.py`,
   `scripts/burnup_scan.py`).
6. The compression-field point: a stated reactor-point field (the basis
   is the patent's 22 T; each halving of B quarters the per-pulse burnup
   and tightens the recovery-nines requirement), and a fatigue basis for
   the compression coil at that field (193 MPa magnetic pressure cycled
   1e9-1e10 times sits at or above copper-alloy gigacycle fatigue
   strengths; the coil may be schedule-limited by mechanics, not
   neutrons).