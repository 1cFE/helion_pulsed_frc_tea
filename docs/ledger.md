# Evidence ledger

*Tal Rubin and Damien Scott, Astera Institute*

**What this is.** Every non-baseline value adopted in the ladder, with
the analog class named and the reason it applies. Tiers: tier 1 is a
citable record or published bound, tier 2 a labelled extrapolation from
a stated roadmap or physical argument, tier 3 labelled speculation with
no source. "Held at baseline" is the recorded outcome when no defensible
value exists.

**What is in here.** The coherence constraints the scripts enforce; the
plant environment, held and stepped; the tier 1, 2 and 3 records with
their sources; the compression field, graded, and the driver bank,
scanned by grade; the coherent minimum and the $10 question; the
breeder that prices He-3; the robustness of the extrapolation device;
and what the ledger needs next.

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
| extrapolations (tier-2 stack, optimized) | 30 T, 100 MJ, 256 MJ | 25.7 | 32.6 | 22.9 | 29.2 |
| speculation (tier-3 stack, optimized) | 40 T, 200 MJ, 800 MJ | 10.5 | 17.6 | 8.2 | 14.3 |

The at-7% columns price the same machine at the design-basis cost of
capital with everything else as its grade has it (`scripts/tiers.py`,
`outputs/devices.csv`), so the financing part of each grade is the
difference: 6.9 and 6.3 $/MWh at extrapolations, 7.1 and 6.1 at
speculation, zero at the two 7% grades. Each 3 GWe park is the 1 GWe
device's module tripled. The field is a stepped entry of the ladder and
the bank a design-search dimension graded by it (their own section
below): the records grade holds both at the basis; the extrapolation
grade is granted 30 T and may double the bank; speculation is granted
40 T and may take the bank to 200 MJ. Every optimized device takes its
grade's field, and the scan prices the field one grade ahead beside it
as a labelled sensitivity. The coil that would deliver a granted field
is neither designed nor priced; the coil audit records the pressure it
cycles to on every point.

**Regression pins.** Stack evaluations at Helion's configuration
(design-basis chamber), kept as internal regression pins: records 153.2
/ 148.5, extrapolations 31.6 / 28.2, speculation 11.4 / 8.8. The tier-2
and tier-3 stacks carry the D-rich mix of `config/tier2.yaml` at their
granted fields: at 30 T the mix's 0.35 s burn fits the period at the
2.73 Hz the tier-2 stack fires at on Helion's chamber in the fewest
modules the 3 Hz grant permits, so that pin passes; at 40 T the 0.19 s
burn overruns the 0.14 s period at the 7.1 Hz the 10 Hz grant builds,
so constraint 8 flags the tier-3 pin and nothing else does; the records
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
compression field (at or below the grade's grant) and the driver bank
(graded, their own section below), the shot as a gain on the bank (the
design-basis 2.56 through the extrapolation grade, free at
speculation), chamber, wall class, burn mix (seven mixes from the
He-3-rich preset to the D-rich end, each on its bremsstrahlung floor)
and firing rate (a ladder of `max_f_rep` ceilings at and below the
lower of the grade's grant and the duty bound of constraint 8, each
rung forcing costingfe into more, slower modules) by
`scripts/coherent_min.py` under the physics-consistency constraints in
`scripts/study.py`; every grade gets the design search. At the basis
field constraint 8 sets the mix and the rate together (the records
device); at the granted fields the burn shortens as B^-2, the duty
bound relaxes with it, and the wall's steady flux (constraint 3) is
what binds, so each device carries as its ceiling the lowest of its
grant, its duty bound and the wall bound of its own module
(`study.search_ceiling_hz`). Reconciliation bands around them (model
gaps and conservatisms, `scripts/reconciliation.py`): extrapolations
within 21.3-29.9, speculation within 9.8-11.6 at 1 GWe; neither band
carries the coil that would hold the granted field, because this work
does not design one. With the coils priced along the expansion adiabat
(conductor growing as L^(1/3)), the design search trades length for
radius: every optimized device is a fat panel-wall chamber, 10 m x 0.75
m at records, 15 m x 1.5 m at extrapolations and 30 m x 1.5 m at
speculation. Two open bands dominate, each priced in its own section
below: the compression coil (the field and bank section) and the
recovery topology at Slough's 40% flux-conserver ceiling (constraint
6).

## Coherence constraints (enforced, not advisory)

Eight couplings are carried on every quoted point. Constraints 1, 2, 3,
5 and 8 are checked by `study.coherence_violations`, and a stack that
violates one is flagged in the output of every script rather than
reported; constraints 4 and 6 are applied by construction in
`study.run`, which prices the tritium plant and caps f_pdv; every point
carries the burn time the seventh implies at its own burn mix and field
(`tau_burn_implied_s`), which the eighth checks against the pulse
period. A further coupling, the coil pressure every point reports, is an
audit rather than a constraint and is recorded after the list:

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
   MJ/m^2, no margin). At the granted fields the steady flux is the
   limit that binds: the extrapolation device's panel wall sits at 1.94
   MW/m^2 and the speculation device's at 1.99, 97 and 99.7% of the
   class, and each device's rate ceiling is the wall bound of its own
   module. The divertor-class wall, at seven times the panel's price
   per square meter, loses to more panel-wall chamber at both grades
   (32.0 against 25.7 $/MWh at extrapolations, 10.9 against 10.5 at
   speculation). 4. **The D-rich fuel credit travels with its
   consequences.** From Helion's own mix upward (dd_frac 0.488) the
   machine is a bulk tritium facility: Helion's device carries 104 MW of
   plant-level neutron power and breeds 38 kg of tritium per year, the
   records device (dd_frac 0.85) 404 MW and 145 kg/yr, the extrapolation
   device (0.85 at 30 T) 198 MW and 74 kg/yr, the speculation device
   (0.85 at 40 T, one module) 142 MW and 53 kg/yr, and the D-rich
   extrapolation stack on Helion's chamber 200 MW and 74 kg/yr; Helion's
   own store-for-decay fuel cycle implies an equilibrium getter-bed
   inventory of production rate x mean decay time, 0.67 tonnes of
   tritium on site at Helion's device, 2.6 at the records device, 1.3 at
   extrapolations, 0.9 at speculation and 1.3 on that D-rich stack
   (writeup Section 5.1), against ITER's 4 kg site limit and the world's
   25-30 kg civilian stock. `study.run` charges a tritium-plant adder on
   C220500, unit-priced rather than anchored: 50 M$ fixed core plus
   0.657 M$ per MW of plant neutron power (a stated definition; the
   100-300 M$ reconciliation band at reference scale brackets it, and
   given the tonne-class inventory the allowance is probably an
   underestimate). The adders, 118 M$ at Helion's device, 316 at the
   records device, 180 at the extrapolation device and 143 at speculation, are
   consequences of throughput, not identities; every device sits above
   the threshold. O&M stays at the baseline 27.5, never at an
   "aneutronic" discount. 5. **dhe3_f_T is
   floored by the burnup closure.** The per-pulse D burnup pins the
   thermalized in-pulse tritium burn (f_T = 1 - (1 - e^-x)/x, x =
   (sv_DT/sv_DD)(-ln(1 - f_D))); any point whose dhe3_f_T sits more than
   1% below that floor is flagged as coherent only under prompt
   MeV-triton loss. The per-pulse burnup scales as B^2 with the density
   (`study.burnup_at_field`), so the floor rises with the field: 0.0016
   at the patent basis (the records and Helion devices), 0.0031 at the
   extrapolation device's 30 T, 0.0054 at the speculation device's 40
   T, all inside the tolerance, so the design's dhe3_f_T = 0 passes at
   every device; at 50 T, the sensitivity above speculation, the floor
   would be 0.008, and at 55 T the zero would be flagged; the constraint
   exists to catch any high-burnup configuration that keeps the zero
   silently. Pricing the floor rather than the zero at the speculation
   device costs 1.4 $/MWh, not for the tritium but because the
   wall-bound single module nets a hair under the gigawatt with 0.54%
   of its bred tritium burning and snaps to two modules
   (`scripts/burnup_scan.py`). 6. **f_pdv is derived, never asserted.**
   Each point's recovery fraction is min(claim, 1 - (V_i/V_f)^(2/3))
   with V_i the compressed flux volume at the point's own bank and field
   (E_del/(B^2/2mu0): about 0.26 m^3 at 50 MJ and 22 T, 0.28 m^3 at the
   extrapolation device's 100 MJ and 30 T, 0.31 m^3 at the speculation
   device's 200 MJ and 40 T) and V_f its own
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
   m chamber bounds f_pdv at 0.940 and the extrapolation device's 15 m
   x 1.5 m at 0.981, above those stacks' 0.80 claim; the speculation
   device's 30 m x 1.5 m chamber at 200 MJ and 40 T bounds it at 0.987,
   above the stack's 0.947 by 0.04, which stands. 7. **The shot is bounded by the plasma
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
   breakeven time as B^-2 (`study.breakeven_time_at_point_s`), 1.9
   times shorter at the extrapolation device's 30 T and 3.3 times at
   the speculation device's 40 T. Against Helion's stated pulse, "on
   the order of hundreds of microseconds to milliseconds"
   (helionenergy.com/faq, June 2026 capture in `docs/sources/`), a 1 ms
   burn returns 0.2 to 0.4 MJ from the 50 MJ bank across
   separatrix-to-coil radius ratios x_s of 0.5 to 0.85, less than the
   2.5 MJ the circuit loses per shot even at the ladder's best inductive
   efficiency, tier 3's eta_dec 0.95, and 2.3 to 5.5 MJ from the
   speculation device's 200 MJ bank at 40 T; the design-basis gain of
   2.56 implies a 0.3 to 0.7 s burn at the patent point, and the
   speculation device's 800 MJ shot, a gain of 4.0 at a breakeven time
   3.3 times shorter, a 0.15 to 0.34 s burn (`scripts/yield_bound.py`),
   and the bound reproduces Slough's (2025)
   own D-T design, where a gain of 9.1 on the FRC energy over a 2 to 5
   ms transit at 34.8 T and 15 keV is a 3.4 ms burn at that point's
   breakeven time (`study.breakeven_time_dt_s`). No record supports any
   yield, so the shot is a graded claim at every grade rather than a
   shared basis: the records device is priced at Helion's shot so that
   a machine exists to cost, and every point reports
   `tau_burn_implied_s` at x_s 0.7, at its own field and at the mix it
   actually burns, purchased He-3 plus the recycled bred He-3: 0.32 s
   at Helion's device (He3/D 0.22 with the recycled He-3 against the
   patent's purchased 0.16), 1.01 s at the records device, 0.35 s at
   the extrapolation device (the same deuterium-rich mix at 30 T) and
   0.30 s at the speculation device's 800 MJ shot (the same mix at 40
   T). 8. **The burn must fit inside the pulse period.** One burn
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
   MW); at the extrapolation device's 100 MJ bank and 30 T the 0.85 cap
   is 738 MW, and at the speculation device's 200 MJ bank and 40 T it
   is 2.7 GW. The rule is evaluated at the reference x_s 0.7; the table
   below the list reads it across the span (`scripts/yield_bound.py`,
   `outputs/duty.csv`). The rule excludes no mix; it sets the rate at
   which a mix can fire, and the design search chooses the rate with the
   mix: a grade's granted ceiling is permission, not obligation, and
   each optimized device carries `max_f_rep` at the lowest of the grant,
   the duty bound of its own burn and the wall bound of its own module,
   so that costingfe builds it in the fewest modules whose rate fits.
   At the basis field the duty bound is the one that binds: the records
   device fires at 100% of it, and the deuterium-rich designs at that
   field, fired at the grants in the fewest modules the grants permit,
   overrun their period (26.5 $/MWh at a duty of 1.62 for the
   extrapolation stack's 256 MJ shot in 4 modules at 2.38 Hz,
   `scripts/coherent_min.py`). At the granted fields the burn shortens
   as B^-2 and the wall bound binds first (constraint 3): the
   extrapolation device fires at 82% of its duty bound and the
   speculation device at 66%. The deuterium-rich end of the mix grid
   (dd_frac 0.85), its best design at each grade under every enforced
   constraint (`study.D_RICH_DEVICES`, `outputs/devices_d_rich.csv`),
   is the device itself at every grade. The rule therefore costs
   nothing at any grade against a coherent at-grant design: the records
   design at the grant is the device (its 1.01 s burn against the 1.01
   s period at 0.985 Hz), the extrapolation device's own shot, chamber
   and mix at the 3 Hz grant is the same 4 modules at 1 GWe, and the
   speculation device's at the 10 Hz grant is the same single module.
**The coil audit.** The coil is recorded against its own mechanics, and
the record restricts no design. Every shot cycles the compression coil from zero to
   the magnetic pressure B^2/2mu0 (`study.coil_pressure_mpa`): 193 MPa
   at the 22 T basis, 358 MPa at the 30 T extrapolation grant, 637 MPa
   at the 40 T speculation grant, 1.7e9 to 5.5e9 times over a book
   life at the devices' rates (`coil_cycles_life` in
   `outputs/devices.csv`). No conductor or case has a gigacycle basis at
   any of these stresses, the basis field's own included, and the
   high-field pulsed-magnet art that reaches such fields operates at
   thousands to tens of thousands of shots, five or six orders below
   what a power plant needs. The coil that would deliver a granted field
   is neither designed nor priced here: the path from a stress
   allowable to a field (winding geometry, load sharing, pre-stress,
   heat treatment) is a design question this work does not undertake,
   so the field is graded as an entry of the ladder in its own right
   (the field and bank section below) and the pressure is reported on
   every point. The cost model offers no resistance of its own: its coil
   account prices conductor along the expansion adiabat with no
   containment term, so it falls with the field rather than rising.

Constraint 8 across the x_s span, at 1 GWe:

| design | dd_frac | field, bank | f_rep (Hz) | P_fus per module (MW) | cap at x_s 0.7 (MW) | duty at x_s 0.5 / 0.7 / 0.85 |
|---|---|---|---|---|---|---|
| citable records | 0.85 | 22 T, 50 MJ | 0.99 | 126 | 126 | 1.71 / 1.00 / 0.73 |
| Helion's requirements | 0.49 | 22 T, 50 MJ | 1.00 | 128 | 401 | 0.55 / 0.32 / 0.23 |
| extrapolations | 0.85 | 30 T, 100 MJ | 2.37 | 607 | 738 | 1.41 / 0.82 / 0.60 |
| speculation | 0.85 | 40 T, 200 MJ | 2.23 | 1786 | 2701 | 1.13 / 0.66 / 0.48 |

The records device sits at 100% of the bound at the reference, since
the search fires it in the fewest modules whose rate fits its burn; the
extrapolation and speculation devices sit at 82 and 66%, since at their
granted fields the wall binds first; all pass at the fat-FRC edge and
would be excluded at x_s 0.5, where chi is 0.30; Helion's own device
passes across the span. The speculation device's single module fires at
2.23 Hz under a cap the 200 MJ bank and the 40 T field have raised to
2.7 GW at its mix, with the panel wall at 99.7% of the steady-flux
limit; the extrapolation device's four modules fire at 2.37 Hz under a
738 MW cap with the wall at 97%.

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
Helion's chamber moves only +0.5 $/MWh, but plant neutron power rises
22% and each burned triton emits a 14.1 MeV neutron (5.8x the D-D
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
dhe3_f_T = 0.78 reads 44.6 at the extrapolation stack on Helion's
chamber (where it also overruns its period, duty 1.02), 35.8 at the
extrapolation device and 14.8 at the speculation device, with plant
neutron power about 5x higher, a dominant 14.1 MeV component and the
decay store shrunk to 0.14-0.52 t; those figures are floors, because
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
four nines at the basis field; 46x / 5.5x / 1.5x at the extrapolation
device's 30 T, where the pair is 2.2e-4 and 7.6e-4; 26x / 3.5x / 1.3x
at the speculation device's 40 T, where it is 4.0e-4 and 1.4e-3,
`scripts/mix.py`). Grade: published design intent; the compression
field moves the machine along the burnup axis as B^2
(`study.burnup_at_field`), the records and Helion devices sit at the
patent point, and the extrapolation and speculation devices 1.9x and
3.3x to its right.

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
speculation device's own point (4.0e-4 at 40 T) the recovery nines
carry its fuel line, which buys the He-3 its loop wastes: 10.5 $/MWh at
fr 0.9999, 12.3 at 0.999, 17.0 at 0.99 on the prompt-loss branch the
device's dhe3_f_T = 0 is, so the fourth nine is worth 1.9 and the third
4.7, less than at the patent point because the loop wastes less at the
higher burnup. The thermalized branch at the same point reads 11.9 at
four nines: the 1.4 $/MWh between the branches is the second module the
wall-bound single module snaps to once the 0.54% in-pulse tritium burn
takes energy into neutrons (constraint 5). The axis minimum (10.3 on
the prompt-loss branch from burnup 1e-3 up, 11.8 at 1e-3 on the
thermalized one) sits 0.2 $/MWh below the device's own point; with 85%
of its events D-D the thermalized branch turns up past burnup 0.003 as
the tritium burn grows (4 to 90%), to 14.8 at 0.3, so the triton-fate
question reopens exactly where the recovery question closes. Per-pulse
exhaust pumping is largest at the low-burnup end of the axis (58 M$
across the extrapolation device's four modules and 24 M$ in the
speculation device's one at their own points).

The scan also reprices neutron damage, which the base model cannot see
(core_lifetime is inert for this concept): the exposed package is
levelized from the 14-MeV-equivalent neutron wall load at 20 and 50 dpa
on the basis set out in the writeup's Section 5.3. The event is C220101
+ C220103: the coil bore sits 0.10 m behind the wall with no blanket, so
the close-coupled copper coils see the same fluence and are replaced
with the wall (they are the cheap part: 28 vs 106 M$ in the
speculation device's single module under the adiabat coil pricing, 61
vs 211 across the extrapolation device's four; ceramic insulation is a
prerequisite, since organics die at 1e9 rad in weeks at these fluxes).
At their own points the records and extrapolation devices carry 0.12
and 0.13 MW/m^2 equivalent, +0.3 to 2.7 $/MWh at 50 to 20 dpa at the
records device (a 17-year changeout interval at 20 dpa) and +0.2 to 1.3
at the extrapolation device (39 years at 50 dpa); the speculation
device's one 30 m wall carries 0.19 MW/m^2 at its mix, +0.3 to 1.2 (27
years). The 10 to 21 $/MWh triton-fate spread at the speculation device
(17 to 33 at extrapolations) appears only in the high-burnup
counterfactual, where the extrapolation stack's divertor-class wall
makes replacement prohibitive (+51 to +152 $/MWh). Two couplings the
damage column exposes: low burnup raises neutron damage as well as fuel
cost (more D-D events per MWh), and keeping the tritium out of the burn
is cheap insurance at the devices' own points and worth double digits
off them.

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
helium-per-dpa of 14 MeV neutrons, the adders are probably
underestimates.

**When replacement becomes rebuilding.** Below the interval the
writeup's Section 5.3 derives, about 5.7 years at the speculation
grade's 3% real (2.8 at 7%) and 3.3 years at the extrapolation grade's
5%, the reactor line is replacement-dominated and the machine is opex.
The derived availability carries the changeout: 27 years at the
speculation device, 39 at extrapolations, 17 at the records device; the
consumable core (1-3 yr intervals, a fifth of the module's value
swapped near-annually) is the high-burnup thermalized counterfactual.
In that regime the honest design is Helion's factory logic taken to its
conclusion: a swappable irradiated cartridge with hot-spare bays (the
speculation device is a single 1 GWe module, and the derivation charges
each changeout as an 84-day plant outage once in 27 years, which the
0.925 it derives already carries; annual swaps would need a spare
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
| lifetime_yr | 60 | 60 | 80 | 80 | engineering: what cannot be replaced sets it; bank and wall replacements are priced at every grade, so 80 yr is worth 0.6 $/MWh at the extrapolation device against 60; against the fusion literature's 30 yr (Böhnlein et al. 2026, median 30-40 yr; ARIES 40) the 60 yr entry is worth 5.1 $/MWh at the Helion device and 7.2 at the records device, and the 80 yr entries 4.6 at the extrapolation device and 3.0 at speculation (`outputs/devices.csv`) | 60: a series-consistency entry, not a record (see the note below the table); 80: US DOE hydropower lifespan 65-85 yr, every core component on its own replacement schedule |
| construction_time_yr | 5.0 | 5.0 | 3.25 | 2.5 | engineering: the build, which also sets the effective indirects through CAS30's build-time scaling; worth 1.6 $/MWh at the extrapolation device against 5 yr | 5 yr: the serial Hualong One builds, about 60 months from first concrete to grid (Zhangzhou 1, construction start October 2019 to grid 28 November 2024, World Nuclear News 2025); 3.25 yr: the Kashiwazaki-Kariwa ABWR pair, 37 and 39 months from first concrete to fuel load (Omoto 2002, Nuclear Engineering International), at the peak of a mature LWR supply chain; 2.5 yr: CCGT-class build (Siemens Energy 1200 MW block in about 30 months), which no fusion plant has a record of |
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
| extrapolations | 0.922 | 4.7% | 0.68% (13.7) | 0.59% (38.8) |
| speculation | 0.925 | 4.7% | 0.06% (144.9) | 0.85% (27.1) |

The result sits just under the red-team review's 0.93-0.95 band and at
the top of the fusion literature's 0.75-0.90. Sensitivity, with
availability pinned instead of derived (`outputs/devices.csv`): the 3
GWe speculation park reads 8.8 $/MWh at the model default 0.85 and 8.0
at 0.95 (11.3 and 10.2 at 1 GWe); the extrapolation device moves 27.3
to 25.1 $/MWh over the same span and the records device 114.6 to 109.1.

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
| cap_shot_lifetime | 1e8 | 1e9 | Pacific Fusion (Langtry et al. 2025) sec. 4.1: 100 to 35 kV derating projected to reach about 1e9 shots at about 9x lower energy density; General Atomics Series DE capacitor cross-check (3e7-3e9 at 20% reversal). At the extrapolation device each module fires about 5.5e9 shots over its 80-year book life at 2.37 Hz, so the bank is replaced about 6x (every 13.7 years, charged to CAS72 by the model); the "1e9 outlives the plant" argument holds only below about 0.4 Hz. The largest lever at this device: +36.2 $/MWh reverted. | published target |
| fuel_recovery | 0.999 (tier-1 record) | 0.9999 | One nine beyond the JET-ILW retention record: the patent closed fuel cycle (US 2017/0011811) implies four-nines per-pulse recovery for the He-3 economy to close, and the physical argument (saturated walls, helium-dominated exhaust, direct re-injection without full reprocessing) points the right direction. No demonstration at any scale. Worth 4.8 $/MWh at the extrapolation device if reverted, with the store's He-3 return credited: at the device's 30 T the loop wastes 57% of what it buys at three nines (71% at the basis field), the device breeds most of its He-3 and buys little, and the leaner recycled plasma's longer burn and lower output cost a fifth module at 1.97 Hz, coherent at a duty of 0.95. | patent-implied extrapolation |
| eta_dec | 0.85 | 0.90 | Bottom of the patent band, circuit-only, no fusion-inclusive measurement. Paired with the basis f_pdv under the composite cap (0.90 x 0.80 = 0.72 <= 0.80 at the extrapolation device, where the chamber's adiabatic bound, 0.981, sits above the claim). | weak-moderate |
| f_pdv | (derived) | min(claim, expansion bound) | Not a record: capped per point under coherence constraint 6 by the chamber's adiabatic expansion bound on the whole volume stroke; at the extrapolation device's 15 m x 1.5 m chamber, 100 MJ bank and 30 T the bound (0.981) sits above the tier's 0.80 claim, so the claim stands. | constraint-derived |
| eta_pin | 0.95 | 0.98 | Solid-state pulsed-power wall-plug efficiency; plausible for modern semiconductor switching, no datasheet or Helion statement located. | UNSOURCED |
| max_f_rep | 1.0 | 3.0 granted; 2.445 used (4 modules at 2.37 Hz) | The grant: no public Helion statement of a numeric plant rep rate exists (Polaris target about 1/s; Trenta about 1/10 min; the 1-10 Hz band is the concept YAML's roadmap paraphrase). 3 Hz is what the bought wall supports at this tier's recovery parameters; it remains UNSOURCED as a demonstrated cadence (nothing MJ-class has run at 1 Hz continuously). The band top (10 Hz) is speculation. The rate used: a grant is permission, not obligation, and the design search sets the device's ceiling at the lowest of the grant, the duty bound of its own 0.35 s burn (2.88 Hz, constraint 8) and the wall bound of its own module (2.445 Hz, constraint 3), so that costingfe builds it in the fewest modules whose rate fits, 4 at 2.37 Hz on the doubled bank with the panel wall at 97% of its limit, and the same module tripled makes the park. The grant above 2.4 Hz is worth nothing to this device; reverting the ceiling to the records grade's 1 Hz costs 9.2 $/MWh, the step from 4 modules to 10. | UNSOURCED-ROADMAP (grant); design choice (rate) |
| fw_class | panel | hhf | Machine-design purchase, not a record: divertor-grade monoblock wall (ITER divertor procurement anchor, 2.5 M$/m^2 NOAK, 10 MW/m^2 qualification) over the real 44.6 m^2 cylinder, 112 M$/module, to make 3 Hz admissible in the design-basis chamber. The extrapolation device instead buys a fatter chamber with the cheaper panel wall and fires at 2.4 Hz, the wall's own bound (see coherent minimum below); the best divertor-class design at this grade reads 32.0 $/MWh. | design purchase |
| e_driver_mj | 50 (Polaris, sourced) | 100 (scan dimension; the field and bank section below) | A doubled bank, 256 MJ shots at the design-basis gain of 2.56: a procurement rather than a technology, since a bank is a count of modular capacitor units (Helion is tooling its Omega facility to produce about 2,500 of them for Orion, GeekWire 2025), and no record of Orion's bank energy exists. Worth 0.3 $/MWh at 1 GWe against the best design on the Polaris bank (7 modules of 10 m x 1.5 m at 2.73 Hz, 26.0) and nothing at the park (22.8 against 22.9), and 2.8 reverted in the device's own chamber (8 modules at 2.39 Hz): at the granted field the wall, not the burn, limits the module, so a larger shot buys fewer modules only until the wall binds. | engineering extrapolation (count, not technology) |
| b_center | 22 (patent, the design basis) | 30 granted and used | The compression field is a stepped entry like max_f_rep (the field and bank section below). 30 T is a grant with no public roadmap behind it: Helion states compression fields of more than 15 T and the patent's table sits at 22 T, and nothing public names a higher reactor-point field. The burn point follows it (density 1.9x the patent's, breakeven time and implied burn 1.9x shorter, per-pulse burnup 1.9x higher). Worth 3.4 $/MWh against the best design at the basis (256 MJ shots at dd_frac 0.80 in 6 modules of 10 m x 1.5 m at 1.56 Hz, 29.1) and 5.4 reverted in the device's own chamber, bank and mix with the ceiling re-solved at the duty bound of the 0.68 s burn the shot needs at 22 T (7 modules at 1.37 Hz). The coil that would deliver it is neither designed nor priced (the coil audit: 358 MPa cycled 5.5e9 times). | UNSOURCED-ROADMAP |
| dhe3_dd_frac | 0.488 (the patent's He3/D = 0.158 at 70 keV as a D-D event share) | 0.85 granted and used | D-rich operation to raise in-situ He-3 breeding (prompt D-D He-3 plus stored-tritium decay) and cut the purchased-fuel line; the concept's own stated direction, but 0.85 is the top of a sweep, not a derived operating point. Adopted only jointly with f_rad 0.28 and the tritium-plant adder (coherence constraints 1 and 4). Slough (2025) restates the patent's mix as the self-sustained cycle's limit, citing the same patent, and puts the D-He3 gain at equal FRC conditions a factor of 240 below D-T's ("the D-T gain advantage of 240", from its eq. 5), which is why the reactor he designs there is D-T (verified against the paper; `docs/sources/slough_2025_notes.md`); 0.314, the blog's 3:1 D:He-3 bremsstrahlung minimum, is the floor's calibration anchor. At the 30 T grant the design search takes the mix to the grant: the D-rich plasma's burn shortens to 0.35 s, the wall rather than the duty bound limits the module, and the step from 0.80 (26.4 $/MWh, 4 modules at 2.31 Hz) to 0.85 (25.7, 4 at 2.37) costs no module. The mix is the second lever at this device: reverting it to Helion's 0.488 costs 11.4 $/MWh. | UNSOURCED |
| f_rad | 0.163 | 0.28 | Bremsstrahlung-consistent radiated fraction at dd_frac 0.85 under the study calibration; relativistic corrections would raise it another 10-25%. Not an optimistic move: it is the price of the fuel credit. The extrapolation device sits on this floor; Helion's 0.23 would sit below it and is not a coherent point there (0.5 $/MWh cheaper). | physics floor |
| interest_rate | 0.07 real | 0.05 real | Cost of capital (financing): federal loan guarantees blended with utility equity, a mechanism with precedent but no fusion record, between the IEA/NEA 2020 central and low cases. The one entry that is financing rather than technology; Figure 1 and the at-7% column keep it separate (worth 6.9 $/MWh at this device against 7%). | mechanism with precedent |
| lifetime_yr | 30 | 80 | Book life (engineering): US DOE hydropower lifespan (65-85 yr) with every core component replaced on its own schedule; the unreplaceable structure sees negligible neutron fluence (copper coils are replaced with the wall, D-D neutrons only). Bank and wall replacements are priced at every grade, so the model shows where 80 yr pays: 0.6 $/MWh here against the 60 yr below it, with the bank turned over about 6x. | civil-works record |
| construction_time_yr | 5.0 | 3.25 | Construction (engineering): the Kashiwazaki-Kariwa ABWR pair, 37 and 39 months from first concrete to fuel load (Omoto 2002, Nuclear Engineering International), at the peak of a mature LWR supply chain, against the 5 yr held at the design basis and records grades (the serial Hualong One builds, about 60 months from first concrete to grid (Zhangzhou 1, construction start October 2019 to grid 28 November 2024, World Nuclear News 2025)). Also lowers the effective indirects from 16.7% to 10.8% through CAS30's build-time scaling; worth 1.6 $/MWh at this device against 5 yr. | demonstrated once |
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
| max_f_rep | 10 granted; 2.238 used (1 module at 2.23 Hz) | the grant is the top of the third-party roadmap band, and no duty-cycle analysis supports it; the speculation device's ceiling is the wall bound of its own module (constraint 3), 2.24 Hz, under the 3.38 Hz duty bound of its 0.30 s burn (constraint 8), so that costingfe builds it in the fewest modules whose rate fits, one at 2.23 Hz on the 200 MJ bank at 40 T, 66% of the duty bound and 99.7% of the panel wall's limit; the grant above 2.24 Hz is worth nothing to it (at the grant the same shot, chamber and mix is the same single module at 2.23 Hz, since one module needs no more) |
| cap_shot_lifetime | 1e10 | required for coherence with 10 Hz; no source at any price; jointly heroic with the $/J entry below. At the 2.23 Hz the device uses, its module fires about 5.2e9 shots over the 80-year book life, so the 1e10 bank outlives the plant (a 145-year swap interval); the entry is worth 4.8e9 shots of margin the device does not spend |
| eta_dec x f_pdv | 0.95 x 0.947 = 0.90 claimed and run | the theory-optimal composite taken at face value, zero engineering margin; the claimed f_pdv 0.947 stands under the 30 m x 1.5 m chamber's adiabatic bound at 40 T and 200 MJ (0.987, constraint 6), by 0.04, so the composite the device runs at is its cap exactly. The source figure (Kirtley, APS DPP 2024, 'optimal burn cycles exceeding 90%') is unreproducible: its numerator is independently verified but its input-accounting denominator is defined in neither slide nor talk (docs/sources/kirtley_dpp24_formulas.md) |
| b_center | 40 T granted and used (scan: 22, 30, 40; 50 priced as the sensitivity above the grant) | SPECULATION: an explicit leap, nearly twice the patent's 22 T and ten tesla past the extrapolation grant, with no source at any grade; the burn point follows it (density 3.3x the patent's, breakeven time and implied burn 3.3x shorter, per-pulse burnup 3.3x higher). Worth 1.2 $/MWh against the best design at the basis (512 MJ shots at dd_frac 0.70 in two 15 m x 1.5 m modules at 1.67 Hz, 11.6; 9.4 at the park) and 0.4 against the best at 30 T (600 MJ shots at dd_frac 0.70 in a single 30 m x 1.5 m module at 2.82 Hz, 10.9; 8.6 at the park), and 3.2 reverted in the device's own chamber, bank and mix with the ceiling re-solved for the 1.06 s burn the shot needs at 22 T (3 modules at 0.75 Hz). The 50 T sensitivity reads 10.2 (7.9 at the park), 0.2 under the device, on a coil cycled to 995 MPa. The coil that would deliver 40 T is neither designed nor priced (the coil audit: 637 MPa cycled 5.2e9 times), and the model's coil account prices it below the 22 T coil (28.1 against 33.0 M$ in this chamber) |
| e_driver_mj | 200 MJ (scan: 50, 100, 200) | SPECULATION above the extrapolation grade's doubling: four times Polaris, the top of the grid, so the bank optimum is the grid's edge rather than an interior optimum; worth 0.1 $/MWh at 1 GWe and at the park (the Polaris bank reads 10.6 in 3 modules of 10 m x 1.5 m at 1.97 Hz, 8.3 at 3 GWe; the 100 MJ bank 10.5 in a single 30 m module firing 400 MJ shots at dd_frac 0.70 at 4.18 Hz), since at 40 T the wall, not the burn, limits the module and a larger shot buys fewer modules only until the wall binds |
| c_cap_allin_per_joule | 0.1 | below the model's own documented range floor; contradicts the derating physics that buys the cap life above |
| u_he3 | 5e5 $/kg | no fleet-scale He-3 market exists at any price. The DOE Isotope Program's 2011 allocation was 600 $/L to federal and 1,000 $/L to commercial users (CRS R41419), 4.5-7.4 M$/kg, and prices have risen several-fold since: the 2024-2026 transactions are gram-to-kilogram scale at 19-22 M$/kg (Edelgas spot; Interlune's DOE and Maybell Quantum agreements at the commercial price; TAE's Black Moon lunar option undisclosed), with every new entrant building toward the high price. This entry is 9x below the 2011 allocation and 40x below the commercial spot. The breeder section below prices the He-3 each device buys: 2.0 M$/kg at the records grade against the ledger's 2, unexplainable at the Helion device (6.6 co-sited, 7.4 standalone), 0.70 co-sited at the extrapolation grade (1.06 standalone), and 0.20 co-sited at speculation (0.58 standalone) against this entry. The speculation device buys 20 kg/yr at it, 0.1 $/MWh of its 10.5. No external route reaches the 20-176 kg/yr these devices would import if they did not breed: US production is about 1 kg/yr from weapons-stockpile tritium decay (CRS R41419, under 8,000 L/yr); the world civilian heavy-water tritium stock of 25-30 kg yields about 1.4 kg/yr as it decays (0.0563/yr on the 12.32 yr half-life); and transmutation using an accelerator, in its own design, DOE/LANL Accelerator Production of Tritium (1,700 MeV x 100 mA CW = 170 MW of beam for 3 kg T/yr; PAC'97 9B003, DOE EIS-0271 1999, decided against in favor of the commercial light water reactor route), would take seven plants and over 1 GW of beam to feed the speculation device alone, so that route fails on energy balance rather than on readiness. The price axis is scanned from zero regardless (`scripts/he3_scan.py`), so any route's best case is already bracketed. |
| dec_staged_recovery_factor | 0.5 | patent's unquantified "net reduction in cost and size", optimistic edge |
| c_inv_per_kw_net | 50 $/kW | small lever |
| multi_unit_labor_factor | 0.80 | small lever |
| interest_rate | 0.03 real | IEA/NEA 2020 low case: sovereign-class capital with no mechanism that delivers it to a first-of-a-kind fleet; financing, shown separately (worth 7.1 $/MWh at 1 GWe and 6.1 at 3 GWe against 7%) |
| construction_time_yr | 2.5 | CCGT-class build (Siemens Energy 1200 MW block in about 30 months) for a fusion module with a tritium facility; no fusion plant has a build record; effective indirects 8.3% at this build |
| yield_per_shot_mj | solved, not asserted; a graded claim at every grade (constraint 7); 800 MJ (a gain of 4.0 on the 200 MJ bank at 40 T) used | no record supports any yield: Helion's stated pulse returns under half a megajoule from the 50 MJ bank at the patent point and 2.3 to 5.5 MJ from the device's 200 MJ bank at 40 T, the design-basis gain implies a 0.3 to 0.7 s burn at the patent point and the device's gain of 4.0 a 0.15 to 0.34 s burn at its field (`scripts/yield_bound.py`), so the records device is priced at Helion's shot only so that a machine exists to cost. Gain speculation is admitted, but the shot must be survivable in the chamber it is costed in: `coherent_min.py` solves gain, field, bank, chamber and rate jointly, and the freed gain is worth 0.02 $/MWh: the design-basis-gain shot (512 MJ at dd_frac 0.80) in the same 30 m x 1.5 m module reads 10.5 as well, since at 40 T the wall, not the burn, limits the module and the gain only sets how often it fires. Gain 40 (2000 MJ on the Polaris bank) in the concept preset's 0.5 m x 10 m chamber deposits about 6.7 MJ/m^2 per shot, four times the tungsten flash-melt bound, and is excluded. |

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
| extrapolations, 1 GWe | **25.7** | the 30 T grant with the doubled bank (100 MJ; 256 MJ shots at the design-basis gain), 4 modules of 15 m x 1.5 m at 2.37 Hz under a 2.445 Hz ceiling, the wall bound of its own module (the duty bound of its 0.35 s burn is 2.88 Hz), panel wall at 97% of its steady-flux limit, the deuterium-rich dd_frac 0.85 with its tritium plant, duty 0.82 (the 0.80 mix reads 26.4 in the same 4 modules at 2.31 Hz; Helion's mix 35.3 in 3 modules at 2.67 Hz, the 3:1 mix 38.5, the He-3-rich preset 41.8 on the Polaris bank; on the Polaris bank the best design is 7 modules of 10 m x 1.5 m at 2.73 Hz, 26.0; at the basis field the best design is 256 MJ shots at dd_frac 0.80 in 6 modules of 10 m x 1.5 m at 1.56 Hz, 29.1; the 40 T sensitivity above the grant reads 25.3 in the same 4 modules) |
| extrapolations, 3 GWe | **22.9** | the same design tripled, 12 modules at 2.37 Hz (the 3 Hz grant would build 10 at 2.84 Hz, whose wall overruns at 2.11 MW/m^2; the wall bound keeps the park at 12) |
| speculation, 1 GWe | **10.5** | the 40 T grant with a 200 MJ bank, 800 MJ shots at a gain of 4.0 in a single module of 30 m x 1.5 m at 2.23 Hz under a 2.238 Hz ceiling, the wall bound of its own module (the duty bound of its 0.30 s burn is 3.38 Hz), panel wall at 99.7% of its steady-flux limit, the deuterium-rich dd_frac 0.85 with its tritium plant, duty 0.66 (the design-basis-gain shot at dd_frac 0.80 in the same module reads within 0.05 $/MWh; the mix grid runs 10.5 to 12.1 in single 30 m modules, with 0.70, 0.80 and 0.85 within 0.1 of each other, Helion's mix at 11.6 as a single 600 MJ module on the 100 MJ bank and the He-3-rich preset at 12.1 as a single 500 MJ module in a 15 m x 1.5 m chamber on the Polaris bank; on the Polaris bank the stack's best design is 300 MJ shots in 3 modules of 10 m x 1.5 m at 1.97 Hz, 10.6; at the 10 Hz grant the device's own shot, chamber and mix is the same single module; at the basis field the best design is 512 MJ shots at dd_frac 0.70 in two 15 m x 1.5 m modules at 1.67 Hz, 11.6, and at 30 T 600 MJ shots at dd_frac 0.70 in a single 30 m module at 2.82 Hz, 10.9; the 50 T sensitivity above the grant reads 10.2) |
| speculation, 3 GWe | **8.2** | the same design tripled, 3 modules at 2.23 Hz (on the Polaris bank, 8.3 in 9; at the basis field 9.4, at 30 T 8.6; the 50 T sensitivity 7.9) |

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
length for radius and the minimum is a fat panel-wall chamber at every
grade, 10 m x 0.75 m at records and 15 m x 1.5 m at extrapolations,
inside the built length envelope, and 30 m x 1.5 m at speculation,
where one burn section at 40 T spreads 1.79 GW of fusion power over a
panel wall at 99.7% of its limit and the chamber runs half again the
length of Polaris. The public facility imagery also corroborates the cost
structure at today's prices: most of the Polaris building's floor is
the pulsed-power farm (about 2,500 stacked power units) with the fusion
machine in a small corner, which is precisely the picture the tier-3
capacitor $/J and shot-life entries claim will invert.

Reconciliation (`scripts/reconciliation.py`) puts honest bands around
these. The shot-cycled replacement of the recovery store and switch
stack (CAS72, with the bank) and the recovery-store markup (f_pdv (1 -
f_rad)) are inside costingfe and priced in every number above. What
remains outside: high-voltage DC switch repricing (+1.3 extrapolation /
+0.6 speculation), the driver-thermalization derate (below), the
tritium-plant band (both devices sit above dd_frac 0.5: -0.6 to +0.6
around the unit-priced 180 M$ adder at extrapolations, -0.4 to +0.4
around the 143 M$ at speculation), and a thermal-bottoming basis change
(-3.8 / -0.2): the extrapolation device lands in 21.3-29.9, the
speculation device in 9.8-11.6 at 1 GWe. The compression coil that
would hold either device's granted field is outside both bands,
because this work does not design one (the field and bank section
below).

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
eta_dec chi (1 - f_pdv) p_driver is worth +1.3/+2.3/+3.1 $/MWh at the
extrapolation device across that x_s span (948 MW of circulating driver
power) and +0.1 to +0.2 at the speculation device (447 MW at a gain of
4.0, priced at a lower LCOE); at the low-gain Helion device it would
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
device's 15 m x 1.5 m at 30 T at 0.981, above those stacks' claimed
0.80, and the speculation device's 30 m x 1.5 m chamber at 200 MJ and
40 T at 0.987, above the stack's claimed 0.947 by 0.04, which stands;
whether the end circuits return the axial fifth of the work is
resolvable by the Polaris shot triplet.
Parallel particle
streaming through the exhaust is captured by nothing at any grade.

**The He-3 market makes the fuel accounting first-order.** At the DOE
Isotope Program's 2011 allocation of 4.5 M$/kg (he3_scan's 4.5e6 row)
the extrapolation device reads 27.2 $/MWh at its own mix (dd_frac
0.85), 52.3 at Helion's mix (0.5 in the scan's grid) and 63.0 at the
3:1 mix (0.314), in the same chamber at the same 2.445 Hz ceiling; at
the 19-22 M$/kg commercial spot (the 2e7 row), 36.3, 152.6 and 203.8:
the leaner mixes do not survive market-priced He-3, and the device,
which breeds most of its own, pays 10.6 $/MWh for the spot. A mix past
the grid's end, dd_frac 0.95, which breeds nearly all it burns, is
nearer indifference (26.8 at the allocation, 27.9 at the spot). That
reading follows from the model's fuel accounting: prompt bred He-3 is
credited through its species-resolved cumulative recycle fraction (0.80
at the patent basis, 0.88 at the extrapolation device's 30 T and 0.93
at the speculation device's 40 T, since He-3 burns out of the loop 3.3x
faster per pass than it leaks and the burnup rises as B^2), and the
decay store's He-3 return, 0.5 dd_frac atoms per primary event and
equal to the prompt branch, is credited atom for atom against the
purchased 1 - dd_frac per event, levelized over the store's build-up at
the grade's rate (`study.he3_purchase_fraction`: 0.22 / 0.79 / 0.16 /
0.11 of the perpetual purchase down the ladder; `he3_decay_return=False`
restores the perpetual purchase). The extrapolation device imports 29
kg/yr and the speculation device 20 kg/yr, of which the store's return
covers five sixths and nine tenths, levelized. The u_he3 = 0 row (24.5
$/MWh at the extrapolation device's own mix in its chamber) is the
free-fuel limit at that machine; at zero price the mix itself changes:
the design search re-run at u_he3 = 0 (`he3_scan.optimum_by_mix`,
`outputs/he3_free_by_mix.csv`) picks the He-3-rich mix (dd_frac 0.131)
on the Polaris bank in 15 m x 0.75 m chambers at the 3 Hz grant at
19.9 $/MWh for the extrapolation grade (20.4 at the 3:1 mix, 22.0 at
Helion's, 24.5 at the device's 0.85) and, with 300 MJ shots on the
Polaris bank at 40 T in a 15 m x 1.5 m single module at 4.47 Hz, 8.3
for speculation (17.4 and 6.2 at 3 GWe), with no tritium plant, so a
free-He-3 concession is worth 5.8 and 2.2 $/MWh at 1 GWe, against the
1.2 and 0.1 the devices show at their own mixes. The credit is worth
6.1 $/MWh at the study's u_he3 at the extrapolation device (31.8
without it), 35.3 at the records device (147.4 without it) and 1.1 at
the speculation device (11.6 without it), and it is coupled to the
burnup closure, because the return exists only if the tritium survives
the pulse.

**The $10/MWh target is reached as a park.** The full speculation
stack as a 3 GWe park reads 8.2 $/MWh (10.5 at 1 GWe, 0.5 above the
target), 1.8 under it. The reconciliation band on the same stack is
9.8 to 11.6 at 1 GWe, with the wall-and-coil replacement hardware of
`burnup_scan.py` adding 0.3 to 1.2 $/MWh at 50 to 20 dpa. Three
entries bring the park there. The cost of capital: the same machine at
the design-basis 7% real reads 14.3 $/MWh (17.6 at 1 GWe), so the 3%
real sovereign-class rate is worth 6.1 $/MWh at the park, three times
its 1.8 margin under the target. The field: at the 40 T grant the park
sits 1.2 $/MWh below the best design at the patent's 22 T (9.4, two 15
m x 1.5 m modules per gigawatt firing 512 MJ shots at dd_frac 0.70)
and 0.4 below the best at the 30 T extrapolation grant (8.6), on a
coil cycled to 637 MPa 5.2e9 times that this work neither designs nor
prices (the coil audit); at the basis field the park still crosses, at
9.4, so the target is reached on the coil the patent point already
needs, and the field takes the margin from 0.6 to 1.8. And the bank:
four times Polaris's, worth 0.1 $/MWh at this field (the Polaris bank
reads 8.3 at 3 GWe, 10.6 at 1 GWe). The figure also needs the derived
availability of 0.925 (8.8 $/MWh at the model default 0.85, 8.0 at
0.95), and its single module fires at 66% of the duty bound with the
panel wall at 99.7% of its steady-flux limit, 0.2% under its ceiling.
Fired at the 10 Hz grant the device's own shot, chamber and mix is the
same single module at 2.23 Hz (`scripts/coherent_min.py`); the grant
above 2.24 Hz buys it nothing. He-3 at zero price takes the coherent
park to 6.2 $/MWh with the design search re-run at that price (the
He-3-rich preset, 300 MJ shots on the Polaris bank at 40 T in a 15 m x
1.5 m single module at 4.47 Hz, no tritium plant;
`scripts/he3_scan.py`), 2.0 under the priced park. The 50 T
sensitivity above the grant would take it to 7.9, 0.2 further, on a
coil cycled to 995 MPa (the field and bank section below). What
carries the floor at the speculation device is not the capacitor bank
(20 M$ of a 645 M$ reactor account in one module): it is buildings
(CAS21 288 M$), CAS50 (198 M$), fuel handling with the tritium-plant
allowance (183 M$), heat rejection and electrical plant (CAS24-26 about
171 M$), the first wall of the 30 m chamber (106 M$), O&M (4.3 $/MWh)
and the annualized capital (6.0 $/MWh); the He-3 it buys (20 kg/yr at
0.5 M$/kg) is 0.1 $/MWh. See `docs/Helion_writeup.md` for the
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
| citable records | 176 | 12.8 | 2.0 | 2.3 | 112.2 / 113.6 |
| Helion's requirements | 98 | 5.6 | 6.6 | 7.4 | 151.1 / 159.2 |
| extrapolations | 29 | 43.9 | 0.70 | 1.06 | 25.0 / 25.2 |
| speculation | 20 | 126.9 | 0.20 | 0.58 | 10.4 / 10.5 |

The ledger price of 2 M$/kg is read back at the records grade (2.0
M$/kg co-sited), cannot be reached at the Helion device (a module that
breeds 5.6 kg/yr at a gain of 0.46), is beaten at the extrapolation
grade (0.70 M$/kg, so the device at its own breeder's price reads 25.0
$/MWh against 25.7 at the ledger price) and at speculation (0.20
against the 0.5 entry co-sited, a breeder module of the device's own
kind breeding 127 kg/yr at 40 T; the standalone breeder, 0.58, would
put the device at 10.5). The three optimized devices breed most of the
He-3 they burn, so the breeder price moves them by 0.7 $/MWh at most. A
central facility serving several devices reads 1.97 to 0.78 M$/kg at
the extrapolation grade for one to twenty devices
(`outputs/breeder_siting.csv`), since the fixed tritium core and the
standalone intercept spread over more kilograms. The scheme relocates
the tritium inventory rather than shrinking it.

## Robustness of the extrapolation device

One-at-a-time reversion from the 25.7 point (`scripts/tornado.py`;
reverted points that leave the coherent set are marked; the field's
reversion re-solves the ceiling at the duty bound of the longer burn,
as the search would):

| knob reverted | LCOE | delta |
|---|---|---|
| cap_shot_lifetime -> 1e8 | 61.9 | +36.2 |
| dhe3_dd_frac -> 0.488, f_rad -> 0.23 (Helion's mix with its own radiated fraction, in the device's 4 modules at 2.09 Hz under its 2.445 Hz ceiling) | 37.2 | +11.4 |
| max_f_rep -> 1 Hz (10 modules at 0.96 Hz against the device's 4 at 2.37) | 35.0 | +9.2 |
| interest_rate -> 0.07 (financing) | 32.6 | +6.9 |
| b_center -> 22 T (the patent basis; the 0.68 s burn the shot then needs re-solves the ceiling to 1.473 Hz, 7 modules at 1.37 Hz) | 31.1 | +5.4 |
| fuel_recovery -> 0.999 (JET-analog; the leaner recycled plasma costs a fifth module at 1.97 Hz, duty 0.95) | 30.6 | +4.8 |
| e_driver_mj -> 50 MJ (the Polaris bank at the design-basis gain, in the device's own 15 m x 1.5 m chamber: 8 modules at 2.39 Hz) | 28.5 | +2.8 |
| eta_dec -> 0.85 (5 modules at 2.13 Hz) | 28.0 | +2.3 |
| construction_time_yr -> 5 yr | 27.3 | +1.6 |
| lifetime_yr -> 60 | 26.3 | +0.6 |
| eta_pin -> 0.95 | 26.3 | +0.6 |
| wall_dpa_tolerance -> 20 | 25.9 | +0.2 |
| f_rad -> 0.23 (Helion's own; below the 0.28 floor at dd_frac 0.85, so not a coherent point) | 25.2 | -0.5 |
| fw_class -> panel | 25.7 | +0.0 |

The cap-life lever counts the full shot-cycled recovery chain (bank,
store and switch stack, CAS72): at 1e8 shots everything that cycles is
replaced about every 1.4 years, about 55 times over the 80-year book
life. Six extrapolation entries carry the number: the capacitor life
at +36 (a published derating target), the burn mix at +11 (reverted to
Helion's mix the device breeds less He-3 and buys more), the rate at
+9 (an unsourced roadmap band, but the device uses only 2.4 Hz of the
3 Hz grant, so the row is the step from 4 modules to 10 rather than
the grant's worth), the field at +5 (a grant with no roadmap behind
it: at 22 T the shot's burn lengthens to 0.68 s and the duty bound
forces 7 modules; against the best design at the basis the grant is
worth 3.4), the per-pulse fuel recovery at +5 with the store's He-3
return credited (an extrapolated nine beyond the JET retention record;
smaller here than at Helion's mix, where it is worth 47, because the
device breeds most of its He-3 and the loop wastes less at 30 T) and
the bank at +3 (the Polaris bank in the device's own chamber; against
the best design on that bank the doubling is worth 0.3); then the
environment entries, the cost of capital (financing, +6.9), the build
(+1.6) and the book life (+0.6 against the 60 years below it). f_pdv
does not appear: the extrapolation stack leaves it at the basis 0.80
under a cap that does not bind. None is a record. That is the honest
quality of the 25.7 figure.

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
through constraint 3. The field is a stepped entry of the ladder,
carried in the tier configs like max_f_rep and wall_dpa_tolerance; the
bank is a scan dimension graded in this section.

Graded by the evidence ladder, as the scan's grids:

| knob | records | extrapolations | speculation | basis and grade |
|---|---|---|---|---|
| b_center (compression field) | 22 T (30 T priced as the sensitivity above the grant) | 30 T granted and used (22, 30 scanned; 40 priced as the sensitivity) | 40 T granted and used (22, 30, 40 scanned; 50 priced as the sensitivity) | The patent's burn point (US 11,469,003 B2: n_D 0.75e22 m^-3 at 70 keV, 22 T at beta = 1) is the design basis and records value, corroborated in class by Helion's stated compression field of more than 15 T; no record exists above it. 30 T at extrapolations is a grant with no public roadmap behind it (UNSOURCED-ROADMAP, `config/tier2.yaml`); 40 T at speculation is an explicit leap (SPECULATION, `config/tier3.yaml`). Each grade's search may use any scanned field at or below its grant, and the scan prices the field one grade ahead as a labelled sensitivity excluded from the grade's devices. The coil that would deliver a granted field is neither designed nor priced; the coil audit records the pressure it cycles to. |
| e_driver_mj (driver bank) | 50 MJ | 50, 100 MJ scanned; 100 used | 50, 100, 200 MJ scanned; 200 used | Polaris's 50 MJ bank is sourced (Helion's Polaris page: "50+ MJ"); Orion's is undisclosed, though Helion's Omega facility is tooled for about 2,500 capacitor units for it (GeekWire 2025), the count the ledger also quotes for Polaris's power-unit farm. A bank is a count of modular units, so doubling it is procurement rather than technology (extrapolation grade); four times Polaris is the speculation grid's top. |

What the scan finds (`outputs/coherent_min_console.txt`): every
optimized device takes its grade's field. At the extrapolation grade
the 30 T grant is worth 3.4 $/MWh (25.7 against 29.1 at the basis,
22.9 against 26.2 at the park): the deuterium-rich mix's burn shortens
from 0.68 s to 0.35 s, the duty bound relaxes from 1.47 to 2.88 Hz, and
4 modules of 15 m x 1.5 m at 2.37 Hz carry the gigawatt where 6 of 10
m x 1.5 m at 1.56 Hz did at 22 T, now with the panel wall, not the
duty, binding at 97% of its limit. The doubled bank is worth 0.3 at 1
GWe (26.0 on the Polaris bank, 7 modules of 10 m x 1.5 m at 2.73 Hz)
and nothing at the park (22.8 against 22.9), because once the wall
binds a larger shot buys fewer modules only until the next module's
wall overruns. The 40 T sensitivity above the grant reads 25.3 (22.5
at the park), 0.4 under the device, in the same 4 modules with the
wall still at 97%. At speculation the 40 T grant is worth 1.2 $/MWh
against the best design at the basis (10.5 against 11.6; 8.2 against
9.4 at the park) and 0.4 against the best at 30 T (10.9; 8.6): the
breakeven time at the deuterium-rich mix falls from 206 to 39 ms, the
cap on one burn section rises to 2.7 GW, and a single 30 m x 1.5 m
module firing 800 MJ shots at 2.23 Hz carries the gigawatt with its
panel wall at 99.7% of its limit, where two 15 m modules at 22 T and
one 30 m module at 30 T did. The bank is worth 0.1 at this field (the
best admissible design per bank reads 10.6 on the Polaris bank, 300 MJ
shots in 3 modules of 10 m x 1.5 m; 10.5 at 100 MJ, 400 MJ shots at
dd_frac 0.70 in one 30 m module; 10.5 at 200 MJ), so the bank optimum
is the grid's top only nominally. The 50 T sensitivity reads 10.2 (7.9
at the park), 0.2 under the device, a single 30 m module at 2.94 Hz
with its wall at 97%. The field's worth falls up the ladder because at
the granted fields the wall, not the burn, limits the module, and a
shorter burn buys nothing once the wall binds; at the records grade,
where the duty bound still binds, a 30 T field would be worth 7.0 (the
same 25 modules under the 1 Hz grant at 105.1, the higher burnup
letting the three-nines loop waste less He-3). The mix stays at the
deuterium-rich end at every granted field at the ledger's He-3 prices
and inverts with He-3 free (8.3 at the preset at 40 T).

The coil is the item the field grading exposes, and it is audited
rather than priced. The magnetic pressure B^2/2mu0 that the
compression coil cycles to on every shot is 193 MPa at 22 T, 358 at 30
T, 637 at 40 T and 995 at 50 T (`study.coil_pressure_mpa`), 1.7e9 to
5.5e9 times over a book life at the devices' rates. No conductor or
case has a gigacycle basis at any of these stresses, the basis field's
own included; the high-field pulsed-magnet art that reaches such
fields operates at thousands to tens of thousands of shots, five or six
orders below what a power plant needs; and the path from a stress
allowable to a field (winding geometry, load sharing, pre-stress, heat
treatment) is a design question this work does not undertake, so the
compression coil's replacement schedule may be set by mechanical
fatigue rather than neutron dpa, a third member of the shot-cycled
replacement family that neither the damage scan nor CAS72 prices, at
any field. costingfe's coil account does not see the pressure: it
prices conductor mass along the expansion adiabat, whose compressed
flux volume shrinks as B^-2, so at a fixed bank the account falls as
the field rises, 16.5 to 13.2 M$/module from 22 to 50 T on the
extrapolation device's shot and chamber and 33.0 to 26.4 on the
speculation device's (`scripts/reconciliation.py`), while the
containment the field needs is absent from it. That is why the field
is graded in the ladder rather than left to the cost model, and why
each grade's field is an entry with a label (a grant with no roadmap,
an explicit leap) rather than a priced account. The reconciliation
RISK rows read the field the other way: the speculation device at a 10
T reactor point, where the burn is 6.6 s and the burnup 2.5e-5, reads
34.6 $/MWh (+24.1, 17 modules at 0.15 Hz), and reverted to the basis
field in its own chamber, bank and mix 13.7 (+3.2, 3 modules at 0.75
Hz); the extrapolation device at 10 T reads 103.6 (46 modules at 0.24
Hz) and at the basis 31.1 (+5.4, 7 modules at 1.37 Hz). A lower field
than a device's own lengthens the burn as B^-2 and quarters the burnup
per halving, and the module count carries the first and the recovery
nines the second.

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
   and the records device sits at 100% of it, because the design search
   fires it in the fewest modules whose rate fits its burn; any
   allowance at all for the exhaust, refill and recharge that must fit
   in the remainder adds modules there. The extrapolation and
   speculation devices, at 82 and 66% of the bound, leave 18 and 34% of
   their 420 and 450 ms periods for them, but stand at 97 and 99.7% of
   their panel wall's steady-flux limit instead, so any allowance
   against the wall adds modules at about 1.5 $/MWh each at the
   extrapolation device and 1.4 at speculation. The switch and
   capacitor cycle life, vacuum recovery at 400-1000 ms periods, and
   coil and chamber thermal management are unpriced.
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
   field (the basis is the patent's 22 T; the ladder grants 30 T at
   extrapolations and 40 T at speculation with no source behind either,
   worth 3.4 and 1.2 $/MWh against the basis; each halving of B
   quarters the per-pulse burnup, quadruples the burn and multiplies
   the module count), and a fatigue basis for the compression coil at
   that field (193, 358 and 637 MPa of magnetic pressure cycled 1.7e9
   to 5.5e9 times at the three fields, with no conductor or case having
   a gigacycle basis at any of them, and the pulsed-magnet art that
   reaches such fields five or six orders of cycles short; the coil may
   be schedule-limited by mechanics, not neutrons). A sourced basis at
   the patent field first is what would turn the field's grades from
   labels into priced entries.