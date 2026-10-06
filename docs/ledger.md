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
their sources; the compression field and the driver bank, scanned by
grade; the coherent minimum and the $10 question; the breeder that
prices He-3; the robustness of the extrapolation device; and what the
ledger needs next.

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

| device | field, bank, shot | 1 GWe | at 7% real | 3 GWe | at 7% real |
|---|---|---|---|---|---|
| citable records (tier-1 stack, optimized) | 22 T, 50 MJ, 128 MJ | 112.1 | 112.1 | 108.2 | 108.2 |
| Helion's requirements (Helion's configuration) | 22 T, 50 MJ, 128 MJ | 105.9 | 105.9 | 102.1 | 102.1 |
| extrapolations (tier-2 stack, optimized) | 22 T, 100 MJ, 256 MJ | 29.1 | 37.2 | 26.2 | 33.8 |
| speculation (tier-3 stack, optimized) | 22 T, 200 MJ, 512 MJ | 11.6 | 19.5 | 9.4 | 16.2 |

The at-7% columns price the same machine at the design-basis cost of
capital with everything else as its grade has it (`scripts/tiers.py`,
`outputs/devices.csv`), so the financing part of each grade is the
difference: 8.1 and 7.6 $/MWh at extrapolations, 7.8 and 6.8 at
speculation, zero at the two 7% grades. Each 3 GWe park is the 1 GWe
device's module tripled. The field and the bank are design-search
dimensions graded by the ladder (their own section below): the records
grade holds both at the basis, the extrapolation grade holds the field
and doubles the bank, speculation takes the bank to 200 MJ and scans
the field to 50 T, and the coil bound (constraint 9) holds every device
at the basis field, so the fields above it are a priced sensitivity,
excluded from every device.

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
deuterium-rich end of the mix grid (dd_frac 0.85, in 25 modules at
0.985 Hz under the 1 Hz grant) with the tritium store's He-3 return
credited: on evidence alone the fuel cycle is uneconomic, and the
descent begins when the recovery extrapolations are granted.

**Design search and bands.** The optimized devices choose the
compression field and the driver bank (graded, their own section
below), the shot as a gain on the bank (the design-basis 2.56 through
the extrapolation grade, free at speculation), chamber, wall class,
burn mix (seven mixes from the He-3-rich preset to the D-rich end, each
on its bremsstrahlung floor) and firing rate (a ladder of `max_f_rep`
ceilings at and below the lower of the grade's grant and the duty bound
of constraint 8, each rung forcing costingfe into more, slower modules)
by `scripts/coherent_min.py` under the physics-consistency constraints
in `scripts/study.py`; every grade gets the design search, and
constraint 8 sets the mix and the rate together at every device (a
higher field would relax it until the wall binds, which is what the
field sensitivity is worth). Reconciliation bands around them (model
gaps and conservatisms, `scripts/reconciliation.py`): extrapolations
within 24.5-33.5, speculation within 10.9-12.9 at 1 GWe, a coil above
the basis field outside both. With the coils priced along the expansion
adiabat (conductor growing as L^(1/3)), the design search trades length
for radius: every optimized device is a fat panel-wall chamber, 10 m x
0.75 m at records, 10 m x 1.5 m at extrapolations and 15 m x 1.5 m at
speculation. Two open bands
dominate, each priced in its own section below: the compression coil
(the field and bank section) and the recovery topology at Slough's 40%
flux-conserver ceiling (constraint 6).

## Coherence constraints (enforced, not advisory)

Nine couplings are applied to every quoted point. Constraints 1, 2, 3,
5, 8 and 9 are checked by `study.coherence_violations`, and a stack
that violates one is flagged in the output of every script rather than
reported; constraints 4 and 6 are applied by construction in
`study.run`, which prices the tritium plant and caps f_pdv; and every
point carries the burn time the seventh implies at its own burn mix and
field (`tau_burn_implied_s`), which the eighth checks against the pulse
period:

   1. **f_rad is coupled to the burn mix.** A D-rich plasma radiates
   more, not less: Bosch-Hale + bremsstrahlung at the study calibration
   (the blog-derived pair f_rad 0.163 at dd_frac 0.314 implies T_i 60-70
   keV at T_e = T_i/2; Helion's own 0.23 at 0.488 with T_e = T_i sits
   above the floor) gives f_rad about 0.28 at dd_frac 0.85.
   `study.f_rad_floor` interpolates the review's computed anchors. 2.
   **Recovery is capped as a composite.** The only published figure on
   the plasma-to-electricity chain (Kirtley, APS DPP 2024: "optimal burn
   cycles exceeding 90% recovery") speaks to the product eta_dec x
   f_pdv. The extrapolation grade keeps engineering margin (composite <=
   0.80); speculation takes the theory optimum (0.90) with zero margin.
   3. **The wall must survive the shot.** Steady flux within the bought
   first-wall class limit (the panel class at 2 MW/m^2; the
   divertor-class monoblock, `hhf` in the configs, at 10 MW/m^2), and
   per-shot flash energy under the tungsten millisecond-melt bound (1.5
   MJ/m^2, no margin). 4. **The D-rich fuel credit travels with its
   consequences.** From Helion's own mix upward (dd_frac 0.488) the
   machine is a bulk tritium facility: Helion's device carries 104 MW of
   plant-level neutron power and breeds 38 kg of tritium per year, the
   records device (dd_frac 0.85) 404 MW and 145 kg/yr, the extrapolation
   device (0.80) 188 MW and 70 kg/yr, the speculation device (0.70, two
   modules) 111 MW and 41 kg/yr, and the D-rich extrapolation stack on
   Helion's chamber 211 MW and 78 kg/yr; Helion's own store-for-decay
   fuel cycle implies an equilibrium getter-bed inventory of production
   rate x mean decay time, 0.67 tonnes of tritium on site at Helion's
   device, 2.6 at the records device, 1.2 at extrapolations, 0.7 at
   speculation and 1.4 on that D-rich stack
   (writeup Section 5.1), against ITER's 4 kg site limit and the world's
   25-30 kg civilian stock. `study.run` charges a tritium-plant adder on
   C220500, unit-priced rather than anchored: 50 M$ fixed core plus
   0.657 M$ per MW of plant neutron power (a stated definition; the
   100-300 M$ reconciliation band at reference scale brackets it, and
   given the tonne-class inventory the allowance is more likely low than
   high). The adders, 118 M$ at Helion's device, 316 at the records
   device, 173 at the extrapolation device and 123 at speculation, are
   consequences of throughput, not identities; every device sits above
   the threshold. O&M stays at the baseline 27.5, never at an
   "aneutronic" discount. 5. **dhe3_f_T is
   floored by the burnup closure.** The per-pulse D burnup pins the
   thermalized in-pulse tritium burn (f_T = 1 - (1 - e^-x)/x, x =
   (sv_DT/sv_DD)(-ln(1 - f_D))); any point whose dhe3_f_T sits more than
   1% below that floor is flagged as coherent only under prompt
   MeV-triton loss. At the patent basis the floor is 0.002, so the
   design's dhe3_f_T = 0 passes at every device; the per-pulse burnup
   scales as B^2 with the density (`study.burnup_at_field`), so at 50
   T, the top of the field sensitivity, the floor would be 0.008, inside
   the tolerance, and at 55 T the zero would be flagged; the constraint
   exists to catch any high-burnup configuration that keeps the zero
   silently. 6. **f_pdv is derived, never asserted.** Each point's
   recovery fraction is min(claim, 1 - (V_i/V_f)^(2/3)) with V_i the
   compressed flux volume at the point's own bank and field
   (E_del/(B^2/2mu0): about 0.26 m^3 at 50 MJ and 22 T, 0.52 m^3 at the
   extrapolation device's 100 MJ, 1.0 m^3 at the speculation device's
   200 MJ) and V_f its own
   chamber, the whole volume stroke counted, as Helion's burn-cycle
   framework (Kirtley, APS DPP 2024) counts it (writeup Section 6). The enforced expression is the
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
   it is priced as a risk row (+20.3 / +7.4 $/MWh at the extrapolation /
   speculation device), not enforced. The records device's 10 m x 0.75
   m chamber bounds f_pdv at 0.940 and the extrapolation device's 10 m
   x 1.5 m at 0.962, above those stacks' 0.80 claim; the speculation
   device's 15 m x 1.5 m chamber at 200 MJ bounds it at 0.954, above
   the stack's 0.947 by 0.007, which stands. 7. **The shot is bounded by the plasma
   energy and the burn time.** The plasma at peak compression holds chi,
   the plasma-thermal share, of the delivered driver energy at the
   energy density of a beta = 1 plasma and burns at the fusion power
   density of the burn point, so gain <= chi x burn time / breakeven
   time, with the breakeven time the ratio of those two densities: 86
   ms at the patent point (22 T, 70 keV, n_D 0.75e22, He3/D 0.158,
   Bosch-Hale rates) with thermalized electrons, 3.7 times shorter with
   electrons held at a tenth of the ion temperature, which the 1 ms
   ion-electron equilibration time at that density forbids for any burn
   long enough to matter (Lackner et al. 2026, JFE 45:12; Nicolas et al.
   2026, JFE 45:24). The burn point follows the field: at beta = 1 and
   the patent's ion temperature the density scales as B^2 and the
   breakeven time as B^-2 (`study.breakeven_time_at_point_s`), 5.2
   times shorter at 50 T. Against Helion's stated pulse, "on the order
   of hundreds of microseconds to milliseconds" (helionenergy.com/faq,
   June 2026 capture in `docs/sources/`), a 1 ms burn returns 0.2 to
   0.4 MJ from the 50 MJ bank across separatrix-to-coil radius ratios
   x_s of 0.5 to 0.85, less than the 2.5 MJ the circuit loses per shot
   even at the ladder's best inductive efficiency, tier 3's eta_dec
   0.95, and 0.7 to 1.7 MJ from the speculation device's 200 MJ bank;
   the design-basis gain of 2.56 implies a 0.3 to 0.7 s burn from
   either bank, the design-basis 128 MJ shot and the speculation
   device's 512 MJ shot alike (`scripts/yield_bound.py`), and the bound
   reproduces Slough's (2025)
   own D-T design, where a gain of 9.1 on the FRC energy over a 2 to 5
   ms transit at 34.8 T and 15 keV is a 3.4 ms burn at that point's
   breakeven time (`study.breakeven_time_dt_s`). No record supports any
   yield, so the shot is a graded claim at every grade rather than a
   shared basis: the records device is priced at Helion's shot so that
   a machine exists to cost, and every point reports
   `tau_burn_implied_s` at x_s 0.7, at its own field and at the mix it
   actually burns, purchased He-3 plus the recycled bred He-3: 0.32 s
   at Helion's device (He3/D 0.22 with the recycled He-3 against the
   patent's purchased 0.16), 1.01 s at the records device, 0.62 s at
   the extrapolation device and 0.51 s at the speculation device's 512
   MJ shot. 8. **The burn must fit inside the pulse period.** One burn
   section holds one plasmoid and the next shot cannot fire while the
   last is still burning, so `tau_burn_implied_s` x f_rep <= 1
   (`study.DUTY_MAX`, checked in `study.coherence_violations`). The
   limit of 1.0 is the hard bound and leaves nothing for exhaust, refill
   and recharge, which a duty-cycle analysis would have to fit in the
   remainder. Since the implied burn is proportional to the yield, the
   duty is the module's fusion power over the cap chi E_del / breakeven
   time, whatever the split between shot size and rep rate; the cap
   rises with the bank and as the field squared, and the breakeven time
   lengthens with the deuterium content: at 22 T and 50 MJ, 65 ms at
   Helion's mix (401 MW), 126 ms at 0.80 with four nines (206 MW), 138
   at the D-rich 0.85 with four nines (188 MW) and 206 with three (126
   MW); at the extrapolation device's 100 MJ bank the 0.80 cap is 413
   MW, and at the speculation device's 200 MJ bank the 0.70 cap is 1.0
   GW. The rule is evaluated at the reference x_s 0.7; the table
   below the list reads it across the span (`scripts/yield_bound.py`,
   `outputs/duty.csv`). The rule excludes no mix; it sets the rate at
   which a mix can fire, and the design search chooses the rate with the
   mix: a grade's granted ceiling is permission, not obligation, and
   each optimized device carries `max_f_rep` at the lower of the grant
   and the duty bound of its own burn, so that costingfe builds it in
   the fewest modules whose rate fits. The deuterium-rich end of the mix
   grid (dd_frac 0.85), its best design at each grade under all nine
   constraints (`study.D_RICH_DEVICES`, `outputs/devices_d_rich.csv`),
   is the records device itself (112.1 / 108.2), reads 29.6 / 26.3 at
   extrapolations (7 modules at 1.37 Hz against the device's 6 at 1.56)
   and 12.0 / 9.7 at speculation (5 modules at 1.46 Hz on the doubled
   bank against the device's 2 at 1.67 on the 200 MJ bank); fired at
   the grants instead, in the fewest modules the grants permit, the
   extrapolation and speculation designs would read 26.5 and 10.6 at
   duties of 1.62 and 9.36 (`scripts/coherent_min.py`), and the rule
   excludes them, while the records design at the grant is the device
   (its 1.01 s burn against the 1.01 s period at 0.985 Hz). The rule
   therefore costs 0, 2.6 and 1.0 $/MWh at 1 GWe against the at-grant
   designs. 9. **The coil is checked against its own mechanics.** Every
   shot cycles the compression coil from zero to the magnetic pressure
   B^2/2mu0 (`study.coil_pressure_mpa`), 1e9 to 1e10 times over the book
   life: 193 MPa at the 22 T basis, at or above copper-alloy gigacycle
   fatigue strengths of 100 to 150 MPa, an open item on the basis coil
   itself. The bound is the same at every grade
   (`study.COIL_PRESSURE_CAP_MPA`, the basis at tier 2 and tier 3
   alike), on evidential grounds: the patent's 22 T is the only field
   with a source, its coil already cycles at or above the band, and no
   higher fatigue basis is sourced anywhere in this work, so a point
   above the basis field is flagged at every grade and no device rests
   on one. The speculation scan still prices 30, 40 and 50 T (the field
   and bank section below), each such row labelled in the scan's output
   as resting on a coil the model does not price, and reports them as a
   sensitivity.

Constraint 8 across the x_s span, at 1 GWe:

| design | dd_frac | field, bank | f_rep (Hz) | P_fus per module (MW) | cap at x_s 0.7 (MW) | duty at x_s 0.5 / 0.7 / 0.85 |
|---|---|---|---|---|---|---|
| citable records | 0.85 | 22 T, 50 MJ | 0.99 | 126 | 126 | 1.71 / 1.00 / 0.73 |
| Helion's requirements | 0.49 | 22 T, 50 MJ | 1.00 | 128 | 401 | 0.55 / 0.32 / 0.23 |
| extrapolations | 0.80 | 22 T, 100 MJ | 1.56 | 398 | 413 | 1.65 / 0.96 / 0.70 |
| speculation | 0.70 | 22 T, 200 MJ | 1.67 | 855 | 1000 | 1.46 / 0.86 / 0.62 |
| extrapolations, D-rich end | 0.85 | 22 T, 100 MJ | 1.37 | 351 | 378 | 1.59 / 0.93 / 0.68 |
| speculation, D-rich end | 0.85 | 22 T, 100 MJ | 1.46 | 375 | 378 | 1.70 / 0.99 / 0.72 |

The records and extrapolation devices sit at 96 to 100% of the bound at
the reference and the speculation device at 86%, since the search fires
each in the fewest modules whose rate fits its burn; all pass at the
fat-FRC edge and would be excluded at x_s 0.5, where chi is 0.30;
Helion's own device passes across the span. The speculation device's
two modules fire at 1.67 Hz under a cap the 200 MJ bank has raised to
1.0 GW at its 0.70 mix, one module short of overrunning it, with the
panel wall at 91% of the steady-flux limit. The deuterium-rich end's
designs, one module slower than the extrapolation device and three
more than the speculation device, sit at 93 and 99%.

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
chamber, 38.5 at the extrapolation device and 15.0 at the speculation
device, with plant neutron power about 5x higher, a dominant 14.1 MeV
component and the decay store shrunk to 0.14-0.52 t; those figures are
floors, because the wall audit checks surface heat only, not the
D-T-class neutron loading it would imply.

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
four nines at the basis field; 17x / 2.6x / 1.2x at 50 T, the top of
the field sensitivity, where the pair would be 6.2e-4 and 2.1e-3,
`scripts/mix.py`). Grade: published design intent; the compression
field moves the machine along the burnup axis as B^2
(`study.burnup_at_field`), every device sits at the patent point, and
the 50 T sensitivity would sit 5.2x to its right.

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
5.2), each point's own burnup on the axis beside the fixed grid. At the
patent-density basis the recovery nines carry the speculation device's
fuel line, which buys the He-3 its loop wastes: 11.6 $/MWh at fr
0.9999, 14.6 at 0.999, 45.1 at 0.99, so the fourth nine is worth 3.0
and the third 30.5. The axis minimum (10.9 on the prompt-loss branch
from burnup 3e-2 up, 11.0 at 1e-3 on the thermalized one) sits 0.6 to
0.7 $/MWh below the device's own point; with 70% of its events D-D the
thermalized branch turns up past burnup 0.003 as the tritium burn grows
(4 to 90%), to 14.3 at 0.3, so the triton-fate question reopens exactly
where the recovery question closes. Per-pulse exhaust pumping peaks at
the patent basis (106 M$ across the extrapolation device's six modules;
76 M$ across the speculation device's two).

The scan also reprices neutron damage, which the base model cannot see
(core_lifetime is inert for this concept): the exposed package is
levelized from the 14-MeV-equivalent neutron wall load at 20 and 50 dpa
on the basis set out in the writeup's Section 5.3. The event is C220101
+ C220103: the coil bore sits 0.10 m behind the wall with no blanket, so
the close-coupled copper coils see the same fluence and are replaced
with the wall (they are the cheap part: 51 vs 106 M$ across the
speculation device's two modules under the adiabat coil pricing, 85 vs
211 across the extrapolation device's six; ceramic insulation is a
prerequisite, since organics die at 1e9 rad in weeks at these fluxes).
At the patent basis the records and extrapolation devices carry 0.12
and 0.13 MW/m^2 equivalent, +0.3 to 2.7 $/MWh at 50 to 20 dpa at the
records device (a 17-year changeout interval at 20 dpa) and +0.2 to 1.4
at the extrapolation device (41 years at 50 dpa); the speculation
device's two 15 m walls carry 0.15 MW/m^2 at its 0.70 mix, +0.3 to 1.1
(35 years). The 8 to 18 $/MWh triton-fate spread at the speculation
device (16 to 32 at extrapolations) appears only in the
high-burnup counterfactual, where the extrapolation stack's
divertor-class wall makes replacement prohibitive (+52 to +134 $/MWh).
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
writeup's Section 5.3 derives, about 6.0 years at the speculation
grade's 3% real (2.9 at 7%) and 3.0 years at the extrapolation grade's
5%, the reactor line is replacement-dominated and the machine is opex.
The derived availability carries the changeout: 35 years at the
speculation device, 41 at extrapolations, 17 at the records device; the
consumable core (1-3 yr intervals, a fifth of the module's value
swapped near-annually) is the high-burnup thermalized counterfactual.
In that regime the honest design is Helion's factory logic taken to its
conclusion: a swappable irradiated cartridge with hot-spare bays (the
speculation device is two 500 MWe modules, and the derivation charges
each changeout as an 84-day plant outage once in 35 years, which the
0.927 it derives already carries; annual swaps would need a spare
module of extra capital), a refurbishment line, and a few hundred tonnes per year of
activated steel and copper that neither the CAS50 decommissioning
provision nor C220110 remote handling is scoped for. Consumable-core
economics are marginal-manufacturing economics, which is where the
missing fleet-learning term would finally bind on something real.

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
| lifetime_yr | 60 | 60 | 80 | 80 | engineering: what cannot be replaced sets it; bank and wall replacements are priced at every grade, so 80 yr is worth 0.6 $/MWh at the extrapolation device against 60; against the fusion literature's 30 yr (Böhnlein et al. 2026, median 30-40 yr; ARIES 40) the 60 yr entry is worth 5.1 $/MWh at the Helion device and 7.2 at the records device, and the 80 yr entries 5.4 at the extrapolation device and 3.6 at speculation (`outputs/devices.csv`) | 60: a series-consistency entry, not a record (see the note below the table); 80: US DOE hydropower lifespan 65-85 yr, every core component on its own replacement schedule |
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
| citable records | 0.893 | 4.7% | 2.8% (3.3) | 1.4% (16.8) |
| Helion's requirements | 0.901 | 4.7% | 2.9% (3.2) | 0.5% (43.9) |
| extrapolations | 0.924 | 4.7% | 0.45% (20.8) | 0.56% (41.0) |
| speculation | 0.927 | 4.7% | 0.05% (193.8) | 0.66% (34.7) |

The result sits just under the red-team review's 0.93-0.95 band and at
the top of the fusion literature's 0.75-0.90. Sensitivity, with
availability pinned instead of derived (`outputs/devices.csv`): the 3
GWe speculation park reads 10.0 $/MWh at the model default 0.85 and 9.2
at 0.95 (12.5 and 11.4 at 1 GWe); the extrapolation device moves 31.0
to 28.5 $/MWh over the same span and the records device 114.6 to 109.1.

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
| cap_shot_lifetime | 1e8 | 1e9 | Pacific Fusion (Langtry et al. 2025) sec. 4.1: 100 to 35 kV derating projected to reach about 1e9 shots at about 9x lower energy density; General Atomics Series DE capacitor cross-check (3e7-3e9 at 20% reversal). At the extrapolation device each module fires about 3.6e9 shots over its 80-year book life at 1.56 Hz, so the bank is replaced about 4x (every 20.8 years, charged to CAS72 by the model); the "1e9 outlives the plant" argument holds only below about 0.4 Hz. The largest lever at this device: +35.4 $/MWh reverted. | published target |
| fuel_recovery | 0.999 (tier-1 record) | 0.9999 | One nine beyond the JET-ILW retention record: the patent closed fuel cycle (US 2017/0011811) implies four-nines per-pulse recovery for the He-3 economy to close, and the physical argument (saturated walls, helium-dominated exhaust, direct re-injection without full reprocessing) points the right direction. No demonstration at any scale. Worth 10.5 $/MWh at the extrapolation device if reverted, with the store's He-3 return credited: the loop wastes 71% of what it buys at three nines, but the device breeds most of its He-3 and buys little; the less He-3-rich plasma's 0.89 s burn overruns the 0.72 s period at 1.39 Hz, so the reverted point also trips constraint 8. | patent-implied extrapolation |
| eta_dec | 0.85 | 0.90 | Bottom of the patent band, circuit-only, no fusion-inclusive measurement. Paired with the basis f_pdv under the composite cap (0.90 x 0.80 = 0.72 <= 0.80 at the extrapolation device, where the chamber's adiabatic bound, 0.962, sits above the claim). | weak-moderate |
| f_pdv | (derived) | min(claim, expansion bound) | Not a record: capped per point under coherence constraint 6 by the chamber's adiabatic expansion bound on the whole volume stroke; at the extrapolation device's 10 m x 1.5 m chamber and 100 MJ bank the bound (0.962) sits above the tier's 0.80 claim, so the claim stands. | constraint-derived |
| eta_pin | 0.95 | 0.98 | Solid-state pulsed-power wall-plug efficiency; plausible for modern semiconductor switching, no datasheet or Helion statement located. | UNSOURCED |
| max_f_rep | 1.0 | 3.0 granted; 1.613 used (6 modules at 1.56 Hz) | The grant: no public Helion statement of a numeric plant rep rate exists (Polaris target about 1/s; Trenta about 1/10 min; the 1-10 Hz band is the concept YAML's roadmap paraphrase). 3 Hz is what the bought wall supports at this tier's recovery parameters; it remains UNSOURCED as a demonstrated cadence (nothing MJ-class has run at 1 Hz continuously). The band top (10 Hz) is speculation. The rate used: a grant is permission, not obligation, and the design search sets the device's ceiling at the duty bound of its own 0.62 s burn (constraint 8), 1.61 Hz, so that costingfe builds it in the fewest modules whose rate fits, 6 at 1.56 Hz on the doubled bank. The grant above 1.6 Hz is worth nothing to this device; reverting the ceiling to the records grade's 1 Hz costs 5.5 $/MWh, the step from 6 modules to 10. | UNSOURCED-ROADMAP (grant); design choice (rate) |
| fw_class | panel | hhf | Machine-design purchase, not a record: divertor-grade monoblock wall (ITER divertor procurement anchor, 2.5 M$/m^2 NOAK, 10 MW/m^2 qualification) over the real 44.6 m^2 cylinder, 112 M$/module, to make 3 Hz admissible in the design-basis chamber. The extrapolation device instead buys a fatter chamber with the cheaper panel wall and fires at 1.6 Hz (see coherent minimum below). | design purchase |
| e_driver_mj | 50 (Polaris, sourced) | 100 (scan dimension; the field and bank section below) | A doubled bank, 256 MJ shots at the design-basis gain of 2.56: a procurement rather than a technology, since a bank is a count of modular capacitor units (Helion is tooling its Omega facility to produce about 2,500 of them for Orion, GeekWire 2025), and no record of Orion's bank energy exists. Halves the module count at the same burn and the same duty; worth 1.0 $/MWh against the best design on the Polaris bank (12 modules of 10 m x 0.75 m, 30.1) and 3.0 reverted in the device's own chamber. | engineering extrapolation (count, not technology) |
| b_center | 22 (patent, the design basis) | 22 (held) | The compression field is a scan dimension bounded at every grade by the coil (constraint 9): the basis coil already cycles at or above the copper-alloy gigacycle band, no conductor with a gigacycle record exists beyond it, and no higher fatigue basis is sourced anywhere in this work, so no field above the patent's has a basis at any grade. | held by the coil bound |
| dhe3_dd_frac | 0.488 (the patent's He3/D = 0.158 at 70 keV as a D-D event share) | 0.85 granted; 0.80 used | D-rich operation to raise in-situ He-3 breeding (prompt D-D He-3 plus stored-tritium decay) and cut the purchased-fuel line; the concept's own stated direction, but 0.85 is the top of a sweep, not a derived operating point. Adopted only jointly with f_rad 0.28 and the tritium-plant adder (coherence constraints 1 and 4). Slough (2025) restates the patent's mix as the self-sustained cycle's limit, citing the same patent, and puts the D-He3 gain at equal FRC conditions a factor of 240 below D-T's ("the D-T gain advantage of 240", from its eq. 5), which is why the reactor he designs there is D-T (verified against the paper; `docs/sources/slough_2025_notes.md`); 0.314, the blog's 3:1 D:He-3 bremsstrahlung minimum, is the floor's calibration anchor. The design search runs the extrapolation device one step short of the grant, at dd_frac 0.80 (29.1 $/MWh) against 29.6 at 0.85: the D-rich plasma's 0.68 s burn (four nines) overruns the 0.42 s period at the grant's 2.4 Hz (constraint 8, duty 1.62) but fits at 1.37 Hz in 7 modules, one more than the 0.80 mix needs at 1.56 Hz, and the extra module costs more than the He-3 the richer mix breeds. The mix is the second lever at this device: reverting it to Helion's 0.488 costs 12.3 $/MWh. | UNSOURCED |
| f_rad | 0.163 | 0.28 | Bremsstrahlung-consistent radiated fraction at dd_frac 0.85 under the study calibration; relativistic corrections would raise it another 10-25%. Not an optimistic move: it is the price of the fuel credit. The extrapolation device, at dd_frac 0.80, sits on its own floor, 0.27; Helion's 0.23 would sit below it and is not a coherent point there (0.4 $/MWh cheaper). | physics floor |
| interest_rate | 0.07 real | 0.05 real | Cost of capital (financing): federal loan guarantees blended with utility equity, a mechanism with precedent but no fusion record, between the IEA/NEA 2020 central and low cases. The one entry that is financing rather than technology; Figure 1 and the at-7% column keep it separate (worth 8.1 $/MWh at this device against 7%). | mechanism with precedent |
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
| max_f_rep | 10 granted; 1.952 used (2 modules at 1.67 Hz) | the grant is the top of the third-party roadmap band, and no duty-cycle analysis supports it; the speculation device's ceiling is the duty bound of its own 0.51 s burn (constraint 8), 1.95 Hz, so that costingfe builds it in the fewest modules whose rate fits, 2 at 1.67 Hz on the 200 MJ bank, 86% of the bound; the grant above 2 Hz is worth nothing to it (at the grant the same shot, chamber and mix is a single module at 3.33 Hz, duty 1.71, excluded, at 10.7) |
| cap_shot_lifetime | 1e10 | required for coherence with 10 Hz; no source at any price; jointly heroic with the $/J entry below. At the 1.67 Hz the device uses, each module fires about 4e9 shots over the 80-year book life, so the 1e10 bank outlives the plant (a 194-year swap interval); the entry is worth 6e9 shots of margin the device does not spend |
| eta_dec x f_pdv | 0.95 x 0.947 = 0.90 claimed and run | the theory-optimal composite taken at face value, zero engineering margin; the claimed f_pdv 0.947 stands under the 15 m x 1.5 m chamber's adiabatic bound at 22 T and 200 MJ (0.954, constraint 6), by 0.007, so the composite the device runs at is its cap exactly. The source figure (Kirtley, APS DPP 2024, 'optimal burn cycles exceeding 90%') is unreproducible: its numerator is independently verified but its input-accounting denominator is defined in neither slide nor talk (docs/sources/kirtley_dpp24_formulas.md) |
| b_center | 22 T (scan: 22, 30, 40, 50; bounded at 22 by the coil) | the compression field above the patent's 22 T has no record and no coil with a gigacycle record behind it, and the coil bound (constraint 9) holds at every grade, so the device sits at the basis. The fields above it are a priced sensitivity (the field and bank section below): the best design the coil alone excludes reads 10.9 at 30 T, 10.5 at 40 T and 10.2 at 50 T (8.6, 8.2 and 7.9 at the park), worth up to 1.4 $/MWh against the device, on a coil cycled to 358 to 995 MPa that the model prices below the 22 T coil |
| e_driver_mj | 200 MJ (scan: 50, 100, 200) | SPECULATION above the extrapolation grade's doubling: four times Polaris, the top of the grid, so the bank optimum is the grid's edge rather than an interior optimum; worth 0.7 $/MWh at 1 GWe and at the park (the Polaris bank reads 12.4 in 7 modules of 10 m x 0.75 m at 1.65 Hz, 10.1 at 3 GWe; the 100 MJ bank 12.0 in 5 modules), since the shot scales with the bank at the design-basis gain and the module count falls with it |
| c_cap_allin_per_joule | 0.1 | below the model's own documented range floor; contradicts the derating physics that buys the cap life above |
| u_he3 | 5e5 $/kg | no fleet-scale He-3 market exists at any price. The DOE Isotope Program's 2011 allocation was 600 $/L to federal and 1,000 $/L to commercial users (CRS R41419), 4.5-7.4 M$/kg, and prices have risen several-fold since: the 2024-2026 transactions are gram-to-kilogram scale at 19-22 M$/kg (Edelgas spot; Interlune's DOE and Maybell Quantum agreements at the commercial price; TAE's Black Moon lunar option undisclosed), with every new entrant building toward the high price. This entry is 9x below the 2011 allocation and 40x below the commercial spot. The breeder section below prices the He-3 each device buys: 2.0 M$/kg at the records grade against the ledger's 2, unexplainable at the Helion device (6.6 co-sited, 7.4 standalone), 0.84 co-sited at the extrapolation grade (1.21 standalone), and 0.32 co-sited at speculation (0.76 standalone) against this entry. The speculation device buys 44 kg/yr at it, 0.8 $/MWh of its 11.6. |
| dec_staged_recovery_factor | 0.5 | patent's unquantified "net reduction in cost and size", optimistic edge |
| c_inv_per_kw_net | 50 $/kW | small lever |
| multi_unit_labor_factor | 0.80 | small lever |
| interest_rate | 0.03 real | IEA/NEA 2020 low case: sovereign-class capital with no mechanism that delivers it to a first-of-a-kind fleet; financing, shown separately (worth 7.8 $/MWh at 1 GWe and 6.8 at 3 GWe against 7%) |
| construction_time_yr | 2.5 | CCGT-class build (Siemens Energy 1200 MW block in about 30 months) for a fusion module with a tritium facility; no fusion plant has a build record; effective indirects 8.3% at this build |
| yield_per_shot_mj | solved, not asserted; a graded claim at every grade (constraint 7); 512 MJ (the design-basis gain of 2.56 on the 200 MJ bank) used | no record supports any yield: Helion's stated pulse returns under half a megajoule from the 50 MJ bank and 0.7 to 1.7 MJ from the device's 200 MJ bank, and the design-basis gain implies a 0.3 to 0.7 s burn from either (`scripts/yield_bound.py`), so the records device is priced at Helion's shot only so that a machine exists to cost. Gain speculation is admitted, but the shot must be survivable in the chamber it is costed in: `coherent_min.py` solves gain, field, bank, chamber and rate jointly, and at the basis field the freed gain buys nothing: the device keeps the design-basis gain, the gain-3 shot (600 MJ) in the same two 15 m x 1.5 m modules reads within 0.01 $/MWh of it, and a larger gain lengthens the burn in proportion and costs modules. Gain 40 (2000 MJ on the Polaris bank) in the concept preset's 0.5 m x 10 m chamber deposits about 6.7 MJ/m^2 per shot, four times the tungsten flash-melt bound, and is excluded. |

## The coherent minimum, and the $10 question

`scripts/coherent_min.py` searches the design space the machine actually
controls (compression field, driver bank, gain, chamber size, wall
class, burn mix, firing rate) under the coherence constraints, at each
evidence level, the field and bank on the graded grids of their own
section below:

| device | LCOE | design |
|---|---|---|
| citable records, 1 GWe | **112.1** | the basis field and bank; Helion's shot at the deuterium-rich dd_frac 0.85 with its tritium plant, 25 modules of 10 m x 0.75 m at 0.985 Hz under a 0.986 Hz ceiling, the duty bound of its 1.01 s burn, which the 1 Hz grant also builds (the mix freedom every grade gets, and the rate with it: the 0.80 mix reads 115.3 in 24 modules at 0.98 Hz; the 15 m x 0.5 m chamber is 1.5 $/MWh behind, the 10 m x 1.0 m 1.8) |
| citable records, 3 GWe | **108.2** | the same design tripled, 75 modules at 0.985 Hz |
| extrapolations, 1 GWe | **29.1** | the basis field with the doubled bank (100 MJ; 256 MJ shots at the design-basis gain), 6 modules of 10 m x 1.5 m at 1.56 Hz under a 1.61 Hz ceiling, panel wall, dd_frac 0.80 with its tritium plant, the fewest modules whose rate fits the 0.62 s burn (the deuterium-rich end, 29.6, needs 7 modules at 1.37 Hz; Helion's mix reads 37.4 in 3 modules at 2.68 Hz, the 3:1 mix 41.0, the He-3-rich preset 44.5 on the Polaris bank; on the Polaris bank the best design is 12 modules of 10 m x 0.75 m at 1.58 Hz, 30.1; at the 3 Hz grant the device's own design is 4 modules at 2.32 Hz, duty 1.44, excluded, at 26.5) |
| extrapolations, 3 GWe | **26.2** | the same design tripled, 18 modules at 1.56 Hz |
| speculation, 1 GWe | **11.6** | the basis field (the coil bound) with a 200 MJ bank, 512 MJ shots at the design-basis gain in 2 modules of 15 m x 1.5 m at 1.67 Hz under a 1.95 Hz ceiling, the duty bound of its 0.51 s burn, panel wall at 91% of its steady-flux limit, dd_frac 0.70 with its tritium plant, duty 0.86 (the gain-3 shot reads within 0.01 $/MWh; the mix grid runs 11.6 to 13.0, the deuterium-rich end at 12.0 in 5 modules on the 100 MJ bank, Helion's mix at 12.6 as a single 800 MJ module on the 200 MJ bank and the He-3-rich preset at 13.0 as a single 500 MJ module in a 15 m x 1.5 m chamber on the Polaris bank; on the Polaris bank the stack's best design is 150 MJ shots in 7 modules of 10 m x 0.75 m at dd_frac 0.70, 12.4; at the 10 Hz grant the device's own shot, chamber and mix is a single module at 3.33 Hz, duty 1.71, excluded, at 10.7; the fields above the basis, excluded by the coil, would read 10.9, 10.5 and 10.2 at 30, 40 and 50 T) |
| speculation, 3 GWe | **9.4** | the same design tripled, 6 modules at 1.67 Hz (on the Polaris bank, 10.1 in 21; the coil-excluded fields would read 8.6, 8.2 and 7.9) |

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
every grade, 10 m x 0.75 m at records, 10 m x 1.5 m at extrapolations
and 15 m x 1.5 m at speculation, all inside the built length envelope;
the 30 m single module that one burn section at 50 T would need to
spread 1.77 GW of fusion power over a panel wall belongs to the field
sensitivity, not to any device. The public facility imagery also corroborates the cost
structure at today's prices: most of the Polaris building's floor is
the pulsed-power farm (about 2,500 stacked power units) with the fusion
machine in a small corner, which is precisely the picture the tier-3
capacitor $/J and shot-life entries claim will invert.

Reconciliation (`scripts/reconciliation.py`) puts honest bands around
these. The shot-cycled replacement of the recovery store and switch
stack (CAS72, with the bank) and the recovery-store markup (f_pdv (1 -
f_rad)) are inside costingfe and priced in every number above. What
remains outside: high-voltage DC switch repricing (+1.2 extrapolation /
+0.7 speculation), the driver-thermalization derate (below), the
tritium-plant band (both devices sit above dd_frac 0.5: -0.6 to +0.6
around the unit-priced 173 M$ adder at extrapolations, -0.4 to +0.4
around the 123 M$ at speculation), and a thermal-bottoming basis change
(-3.9 / -0.3): the extrapolation device lands in 24.5-33.5, the
speculation device in 10.9-12.9 at 1 GWe. A compression coil above the
basis field is outside both bands (the field and bank section below).

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
eta_dec chi (1 - f_pdv) p_driver is worth +1.5/+2.5/+3.5 $/MWh at the
extrapolation device across that x_s span (933 MW of circulating driver
power) and +0.1 to +0.3 at the speculation device (668 MW, at the same
gain, priced at a lower LCOE); at the low-gain Helion device it would
be order +10. The Polaris shot triplet (vacuum /
plasma no-burn / burning) separates eta_dec, chi (1 - f_pdv), and the
fusion composite, so the study's most-wanted measurement delivers chi as
a by-product; until then, published excluded-flux radii (x_s) pin it per
shot. The disposal of the FUSION heat is already in the model: f_rad
radiates to the wall, (1 - f_pdv) of the remainder is dumped undirected
at end of pulse, and eta_th = 0 discards the lot, which is what drives
the wall-flux audit and the bottoming credit. The expansion bound is
enforced as coherence constraint 6 (f_pdv capped per point by the
chamber's expansion ratio on the whole volume stroke): the records
device's 10 m x 0.75 m chamber caps it at 0.940 and the extrapolation
device's 10 m x 1.5 m at 0.962, above those stacks' claimed 0.80, and
the speculation device's 15 m x 1.5 m chamber at 200 MJ at 0.954,
above the stack's claimed 0.947 by 0.007, which stands; whether the
end circuits return the axial fifth of the work is resolvable by the
Polaris shot triplet.
Parallel particle
streaming through the exhaust is captured by nothing at any grade.

**The He-3 market makes the fuel accounting first-order.** At the DOE
Isotope Program's 2011 allocation of 4.5 M$/kg (he3_scan's 4.5e6 row)
the extrapolation device reads 32.2 $/MWh at its own mix (dd_frac
0.80), 58.5 at Helion's mix (0.5 in the scan's grid) and 68.7 at the
3:1 mix (0.314), in the same chamber at the same 1.61 Hz ceiling; at
the 19-22 M$/kg commercial spot (the 2e7 row), 51.4, 172.3 and 226.3:
the leaner mixes do not survive market-priced He-3, and the device,
which breeds most of its own, pays 22 $/MWh for the spot. The D-rich
column is nearer indifference (29.9 and 40.6) but overruns the device's
period at its ceiling (constraint 8) and is starred in the scan's
table; it fits one module slower. That reading follows from the model's
fuel accounting: prompt bred He-3 is credited through its
species-resolved cumulative recycle fraction (0.80 at the per-pulse
basis, where every device sits; it would be 0.96 at 50 T, since He-3
burns out of the loop 3.3x faster per pass than it leaks), and the
decay store's He-3 return, 0.5 dd_frac atoms per primary event and
equal to the prompt branch, is credited atom for atom against the
purchased 1 - dd_frac per event, levelized over the store's build-up at
the grade's rate (`study.he3_purchase_fraction`: 0.22 / 0.79 / 0.23 /
0.31 of the perpetual purchase down the ladder; `he3_decay_return=False`
restores the perpetual purchase). The extrapolation device imports 43
kg/yr and the speculation device 44 kg/yr, of which the store's return
covers three quarters and seven tenths, levelized. The u_he3 = 0 row
(26.6 $/MWh at the extrapolation device's own mix in its chamber) is
the free-fuel limit at that machine; at zero price the mix itself
changes: the design search re-run at u_he3 = 0
(`he3_scan.optimum_by_mix`, `outputs/he3_free_by_mix.csv`) picks the
He-3-rich mix (dd_frac 0.131) on the Polaris bank in 15 m x 0.75 m
chambers at the 3 Hz grant at 20.3 $/MWh for the extrapolation grade
(20.8 at the 3:1 mix, 22.4 at Helion's, 26.6 at the device's 0.80) and,
with 300 MJ shots on the Polaris bank in a 15 m x 1.5 m single module
at 4.47 Hz, 8.5 for speculation (17.7 and 6.5 at 3 GWe), with no
tritium plant, so a free-He-3 concession is worth 8.8 and 3.1 $/MWh at
1 GWe, against the 2.5 and 0.8 the devices show at their own mixes. The
credit is worth 8.2 $/MWh at the study's u_he3 at the extrapolation
device (37.3 without it), 35.3 at the records device (147.4 without it)
and 1.9 at the speculation device (13.5 without it), and it is coupled
to the burnup closure, because the return exists only if the tritium
survives the pulse.

**The $10/MWh target is reached as a park, on the coil the basis
already needs.** The full speculation stack as a 3 GWe park reads 9.4
$/MWh (11.6 at 1 GWe, 1.6 above the target), at the patent's 22 T, so
nothing in it rests on a field this work cannot price. The
reconciliation band on the same stack is 10.9 to 12.9 at 1 GWe, with
the wall-and-coil replacement hardware of `burnup_scan.py` adding 0.3
to 1.1 $/MWh at 50 to 20 dpa. Two entries bring the park there. The
cost of capital: the same machine at the design-basis 7% real reads
16.2 $/MWh (19.5 at 1 GWe), so the 3% real sovereign-class rate is
worth 6.8 $/MWh at the park, eleven times its 0.6 margin under the
target. And the bank: four times Polaris's, worth 0.7 $/MWh, and with
the bank at Polaris's value the stack sits at the target (10.1 at 3
GWe, 12.4 at 1 GWe), so the park crosses on the bank alone. The figure
also needs the derived availability of 0.927 (10.0 $/MWh at the model
default 0.85, 9.2 at 0.95), and its two modules fire at 86% of the duty
bound with the panel wall at 91% of its steady-flux limit. Fired at the
10 Hz grant in the fewest modules the grant permits, the device's own
shot, chamber and mix is a single module at 3.33 Hz, duty 1.71,
excluded at 10.7 (`scripts/coherent_min.py`); the device is the same
design fired slow enough to fit. He-3 at zero price takes the coherent
park to 6.5 $/MWh with the design search re-run at that price (the
He-3-rich preset, 300 MJ shots on the Polaris bank in a 15 m x 1.5 m
single module at 4.47 Hz, no tritium plant; `scripts/he3_scan.py`), 2.9
under the priced park. A field above the basis would take it further
still, 8.6, 8.2 and 7.9 at 30, 40 and 50 T, on a coil cycled to 358 to
995 MPa that the coil bound excludes at every grade (the field and bank
section below). What carries the floor at the speculation device is
not the capacitor bank (41 M$ of a 721 M$ reactor account across two
modules): it is buildings (CAS21 282 M$), CAS50 (201 M$), heat
rejection and electrical plant (CAS24-26 about 169 M$), fuel handling
with the tritium-plant allowance (163 M$), the first wall of the two 15
m chambers (106 M$), O&M (4.4 $/MWh) and the annualized capital (6.3
$/MWh); the He-3 it buys (44 kg/yr at 0.5 M$/kg) is 0.8 $/MWh. See
`docs/Helion_writeup.md` for the account-by-account anatomy and the
small-plant-penalty analysis.

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
| citable records | 176 | 12.8 | 2.0 | 2.3 | 112.2 / 113.6 |
| Helion's requirements | 98 | 5.6 | 6.6 | 7.4 | 151.1 / 159.2 |
| extrapolations | 43 | 28.0 | 0.84 | 1.21 | 27.6 / 28.1 |
| speculation | 44 | 52.4 | 0.32 | 0.76 | 11.3 / 12.1 |

The ledger price of 2 M$/kg is read back at the records grade (2.0
M$/kg co-sited), cannot be reached at the Helion device (a module that
breeds 5.6 kg/yr at a gain of 0.46), is beaten at the extrapolation
grade (0.84 M$/kg, so the device at its own breeder's price reads 27.6
$/MWh against 29.1 at the ledger price) and at speculation (0.32
against the 0.5 entry co-sited, a breeder module of the device's own
kind breeding 52 kg/yr; the standalone breeder, 0.76, would put the
device at 12.1). The three optimized devices breed most of the He-3
they burn, so the breeder price moves them by 1.5 $/MWh at most. A central facility
serving several devices reads 1.87 to 0.87 M$/kg at the extrapolation
grade for one to twenty devices (`outputs/breeder_siting.csv`), since
the fixed tritium core and the standalone intercept spread over more
kilograms. The scheme relocates the tritium inventory rather than
shrinking it.

## Robustness of the extrapolation device

One-at-a-time reversion from the 29.1 point (`scripts/tornado.py`;
reverted points that leave the coherent set are marked):

| knob reverted | LCOE | delta |
|---|---|---|
| cap_shot_lifetime -> 1e8 | 64.5 | +35.4 |
| dhe3_dd_frac -> 0.488, f_rad -> 0.23 (Helion's mix with its own radiated fraction, in the device's 6 modules under its 1.61 Hz ceiling) | 41.4 | +12.3 |
| fuel_recovery -> 0.999 (JET-analog; overruns the period, duty 1.24) | 39.6 | +10.5 |
| interest_rate -> 0.07 (financing) | 37.2 | +8.1 |
| max_f_rep -> 1 Hz (10 modules at 0.94 Hz against the device's 6 at 1.56) | 34.6 | +5.5 |
| e_driver_mj -> 50 MJ (the Polaris bank at the design-basis gain, in the device's own 10 m x 1.5 m chamber: 12 modules) | 32.1 | +3.0 |
| eta_dec -> 0.85 | 31.4 | +2.3 |
| construction_time_yr -> 5 yr | 30.9 | +1.9 |
| eta_pin -> 0.95 | 29.7 | +0.7 |
| lifetime_yr -> 60 | 29.7 | +0.6 |
| wall_dpa_tolerance -> 20 | 29.3 | +0.2 |
| f_rad -> 0.23 (Helion's own; below the 0.27 floor at dd_frac 0.80, so not a coherent point) | 28.7 | -0.4 |
| fw_class -> panel | 29.1 | +0.0 |

The cap-life lever counts the full shot-cycled recovery chain (bank,
store and switch stack, CAS72): at 1e8 shots everything that cycles is
replaced about every two years, about 40 times over the 80-year book
life. Five extrapolation entries carry the number: the capacitor life
at +35 (a published derating target), the burn mix at +12 (reverted to
Helion's mix the device breeds less He-3 and buys more), the per-pulse
fuel recovery at +10 with the store's He-3 return credited (an
extrapolated nine beyond the JET retention record; smaller here than
at Helion's mix, where it is worth 47, because the device breeds most
of its He-3), the rate at +6 (an unsourced roadmap band, but the
device uses only 1.6 Hz of the 3 Hz grant, so the row is the step from
6 modules to 10 rather than the grant's worth) and the bank at +3 (the
Polaris bank in the device's own chamber; against the best design on
that bank the doubling is worth 1.0); then the environment entries, the
cost of capital (financing, +8.1), the build (+1.9) and the book life
(+0.6 against the 60 years below it). f_pdv does not appear: the
extrapolation stack leaves it at the basis 0.80 under a cap that does
not bind; nor does the field, held at the basis by the coil. None is a
record. That is the honest quality of the 29.1 figure.

## Knobs with no effect

`core_lifetime_dhe3` moves LCOE by exactly zero at every operating point
quoted here. Recorded so it is not mistaken for an untested lever; which
is why wall replacement enters through the coherence constraints rather
than through that knob.

## The compression field and the driver bank

Both are design-search dimensions in `scripts/coherent_min.py`, carried
on every point as `b_center` and `e_driver_mj` and read at one place
each in `scripts/study.py` (`field_t`, `e_del_mj`), so that everything
the burn point sets follows them rather than being held at the basis
while the point moves: at beta = 1 and the patent's 70 keV the density
scales as B^2, so the breakeven time of constraint 7 falls as B^-2 and
the duty bound of constraint 8 (the cap on one burn section's fusion
power, chi E_del / breakeven time) rises as B^2 and with the bank; the
per-pulse burnup pair rises as B^2 at the vendor's stated dwell
(`study.burnup_at_field`), which moves the recycle losses, the
bred-He-3 credit, the exhaust pumping and the tritium in-pulse burn
floor of constraint 5; the compressed flux volume of constraint 6,
E_del/(B^2/2mu0), shrinks as B^-2 and grows with the bank; the shot at
a given gain scales with the bank (the design-basis gain of 2.56 is
held through the extrapolation grade, so the burn a shot implies is
unchanged by the bank and the duty falls with the module power per
shot); costingfe prices the coils at `b_center` and the driver and
conversion electronics per joule of `e_driver_mj`; and the wall's
steady flux and per-shot flash follow the fusion power and the shot
through constraint 3.

Graded by the evidence ladder, as the scan's grids:

| knob | records | extrapolations | speculation | basis and grade |
|---|---|---|---|---|
| b_center (compression field) | 22 T | 22 T | 22, 30, 40, 50 T scanned; 22 used, the coil bound holding at every grade | The patent's burn point (US 11,469,003 B2: n_D 0.75e22 m^-3 at 70 keV, 22 T at beta = 1) is the design basis, corroborated in class by Helion's stated compression field of more than 15 T; no record exists above it. Held at every grade by the coil (constraint 9): 193 MPa of magnetic pressure at 22 T, cycled 1e9 to 1e10 times, is at or above the copper-alloy gigacycle band (100-150 MPa), no conductor with a gigacycle record exists beyond it, and no higher fatigue basis is sourced anywhere in this work. The speculation scan prices the fields above the basis and labels every such point; they are a sensitivity, excluded from every device. |
| e_driver_mj (driver bank) | 50 MJ | 50, 100 MJ scanned; 100 used | 50, 100, 200 MJ scanned; 200 used | Polaris's 50 MJ bank is sourced (Helion's Polaris page: "50+ MJ"); Orion's is undisclosed, though Helion's Omega facility is tooled for about 2,500 capacitor units for it (GeekWire 2025), the count the ledger also quotes for Polaris's power-unit farm. A bank is a count of modular units, so doubling it is procurement rather than technology (extrapolation grade); four times Polaris is the speculation grid's top. |

What the scan finds (`outputs/coherent_min_console.txt`): at the
extrapolation grade the doubled bank halves the module count at the
same burn and the same duty and is worth 1.0 $/MWh (29.1 against 30.1
on the Polaris bank). At speculation the bank is worth 0.7 $/MWh at 1
GWe and at the park: the best coherent design per bank reads 12.4 on
the Polaris bank (150 MJ shots in 7 modules of 10 m x 0.75 m), 12.0 at
100 MJ (the deuterium-rich end in 5 modules of 10 m x 1.0 m) and 11.6
at 200 MJ (512 MJ shots in two 15 m x 1.5 m modules at dd_frac 0.70),
so the bank optimum sits at the top of the grid and the figure is the
grid's, not an interior optimum. The field above the basis is a
sensitivity the coil bound excludes from every device: the best design
the coil alone excludes reads 10.9 at 30 T (a 200 MJ bank, 600 MJ
shots at dd_frac 0.70 in a single 30 m x 1.5 m module at 2.82 Hz), 10.5
at 40 T and 10.2 at 50 T (a 100 MJ bank, 600 MJ shots at dd_frac 0.85
in a single 30 m x 1.5 m module at 2.94 Hz), 8.6, 8.2 and 7.9 at the
park, so a higher field would be worth 0.7, 1.2 and 1.4 $/MWh at either
plant size. What the field would change is what shapes the design: at
22 T the duty bound of constraint 8 sets the mix and the rate together
and every device fires at 86 to 100% of it; at 50 T the breakeven time
is 5.2 times shorter, one 30 m burn section carries 1.77 GW of fusion
power at 83% of the bound, and the panel wall's steady flux binds
instead at 97% of its limit. The mix stays deuterium-rich at every
field at the ledger's He-3 prices and inverts with He-3 free (8.5 at
the preset, at the basis field).

The coil is the item the field scan exposes, and it bounds the field
rather than being priced. The magnetic pressure B^2/2mu0 that the
compression coil cycles to on every shot is 193 MPa at 22 T, 358 at 30
T, 637 at 40 T and 995 at 50 T (`study.coil_pressure_mpa`), against
copper-alloy gigacycle fatigue strengths of 100 to 150 MPa; the basis
coil itself sits at or above that band, which is why the compression
coil's replacement schedule may be set by mechanical fatigue rather
than neutron dpa, a third member of the shot-cycled replacement family
that neither the damage scan nor CAS72 prices. costingfe's coil account
does not see the pressure: it prices conductor mass along the expansion
adiabat, whose compressed flux volume shrinks as B^-2, so at a fixed
bank the account falls as the field rises, 14.2 to 11.4 M$/module from
22 to 50 T on the extrapolation device's shot and chamber and 25.4 to
20.6 on the speculation device's (`scripts/reconciliation.py`), while
the structure the field needs is absent from it. That is why the field
is bounded in the constraint set at the basis at every grade rather
than left to the cost model, and why the 30 to 50 T designs are
reported as what they would be worth rather than built into a device.
The reconciliation RISK rows read the field the other way: the
speculation device at a 10 T reactor point, where the burn is 2.98 s
and the burnup 2.5e-5, reads 23.3 $/MWh (+11.7, 12 modules at 0.32
Hz); the extrapolation device at 10 T reads 85.8 (39 modules at 0.27
Hz). A lower field than the patent's lengthens the burn as B^-2 and
quarters the burnup per halving, and the module count carries the
first and the recovery nines the second.

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
   and the records and extrapolation devices sit at 96 to 100% of it,
   because the design search fires each in the fewest modules whose rate
   fits its burn; any allowance at all for the exhaust, refill and
   recharge that must fit in the remainder adds modules, at about 1.4
   $/MWh per module at the extrapolation device, while the speculation
   device's two modules, at 86% of the bound, leave 14% of their 600 ms
   period for them. The switch and capacitor cycle life, vacuum
   recovery at 600-1000 ms periods, and coil and chamber thermal
   management are unpriced.
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
6. The compression-field point and its coil: a stated reactor-point
   field (the basis is the patent's 22 T; the scan prices 30 to 50 T at
   speculation as a sensitivity worth up to 1.4 $/MWh at 1 GWe and
   excludes them from every device on the coil; each halving of B
   quarters the per-pulse burnup, quadruples the burn and multiplies
   the module count), and a fatigue basis for the compression coil at
   that field (193 MPa magnetic pressure cycled 1e9-1e10 times sits at
   or above copper-alloy gigacycle fatigue strengths, and 995 MPa at 50
   T sits beyond any conductor's record; the coil may be
   schedule-limited by mechanics, not neutrons). A sourced basis at the
   patent field is what would let the bound move at all.