# Evidence ledger

*Tal Rubin, Astera Institute*

Every non-baseline value adopted in the ladder, with the analog class named
and the reason it applies. Tiers follow the Borealis convention: tier 1 is a
citable record or published bound, tier 2 a labelled extrapolation from a
stated roadmap or physical argument, tier 3 labelled speculation with no
source. "Held at baseline" is the recorded outcome when no defensible value
exists.

Orientation: the machine is a pulsed inductive direct-conversion
generator with no turbine, its burning plasma a D-He3 FRC, 1 GWe as an
integer count of Helion-class modules; design basis in
`config/baseline.yaml`, capacitor and pulsed-power evidence in
`docs/capacitor_technology_report.md`, adversarial findings in
`docs/red_team_review.md` (all of whose verdicts are folded into the
tier composition below), narrative answer in `docs/writeup.md`, whose
Notation paragraph (Section 3) defines the symbols and knob names used
here.

Design-basis note: the shot is solved, not cited. The driver energy is
the sourced 50 MJ; the yield is the smallest value, to 0.1 MJ, at which
one module (the 50 MWe unit Helion's CEO describes coming off a
gigafactory line, one a day, on a truck: Kirtley, Lex Fridman Podcast
485, 17 November 2025, at 2:17:48) at Helion's own burn point
(`config/baseline.yaml`: dd_frac 0.488, f_rad 0.23) nets the
power-purchase agreement's 50 MWe at the 1 Hz ceiling: 128.1 MJ, gain
2.56. The concept preset's yield pin (101.4 MJ, gain 2.03) rests on the
preset's default 1:1 D:He-3 mix, which no source outside the model
supports, and is not used. On the preset's 0.5 m chamber the solved shot
puts 1.75 MJ/m^2 per shot on the wall against the 1.5 tungsten bound, so
the Helion device is costed in the smallest chamber that survives it:
plasma radius 0.61 m (wall radius 0.71 m, the coil bore right behind it)
at the preset's 10 m length, where the flash reads 1.48 MJ/m^2. The 1
GWe Helion device is 20 modules at 1 Hz, the 3 GWe park 60. The
power-purchase figure is a commercial commitment, not a physics
disclosure; the model reproduces it only with this shot. The shot is
also beyond Helion's own stated pulse: at the patent burn point a
millisecond burn returns under half a megajoule from the bank and 128 MJ
implies a 0.3 to 0.7 s burn (constraint 7), so the shot is a graded
claim at every grade, and the records device is priced at it only so
that a machine exists to cost.

All numbers at costingfe `44434d9` (cylinder geometry + wall-flux audit
for linear pulsed concepts; shot-cycled CAS72 replacement scope;
physics-consistent recovery-store markup; per-pulse fuel-cycle semantics
with species-resolved DHE3 recycle losses), pinned by the regression
tests in `tests/`. Account codes (CAS21, C220101 and the like) are the
model's cost-account structure. The tier stacks are
`config/best_case.yaml`, `config/tier2.yaml`, `config/tier3.yaml`;
`scripts/tiers.py` reproduces the ladder end to end.

The writeup presents one device per evidence grade, all on the plant
environment of the held-and-stepped section below: **citable records**
is the tier-1 stack design-optimized, **Helion's requirements** is
Helion's configuration on the design basis, **extrapolations** and
**speculation** are the tier-2 and tier-3 stacks design-optimized.
Devices at 1 / 3 GWe:

| device | 1 GWe | at 7% real | 3 GWe | at 7% real |
|---|---|---|---|---|
| citable records (tier-1 stack, optimized) | 119.3 | 119.3 | 114.6 | 114.6 |
| Helion's requirements (Helion's configuration) | 111.0 | 111.0 | 106.9 | 106.9 |
| extrapolations (tier-2 stack, optimized) | 26.8 | 33.9 | 23.6 | 30.1 |
| speculation (tier-3 stack, optimized) | 10.6 | 17.9 | 8.4 | 14.6 |

The at-7% columns price the same machine at the design-basis cost of
capital with everything else as its grade has it (`scripts/tiers.py`,
`outputs/devices.csv`), so the financing part of each grade is the
difference: 7.1 and 6.5 $/MWh at extrapolations, 7.2 and 6.2 at speculation, zero at the two 7% grades.

Stack evaluations at Helion's configuration (design-basis chamber), kept
as internal regression pins: records 160.5 / 155.2, extrapolations 32.4 / 29.0, speculation 12.0 / 9.4. The records device sits above Helion's
requirements because reverting Helion's per-pulse fuel recovery to the
JET-analog three nines is worth about 49 $/MWh at Helion's own mix
(dd_frac 0.49), nearly all of which the records device's deuterium-rich
mix recovers with the tritium store's He-3 return credited: on evidence
alone the fuel cycle is uneconomic, and the descent begins when the
recovery extrapolations are granted.

The optimized devices choose chamber, wall class, and burn mix by
`scripts/coherent_min.py` under the physics-consistency constraints in
`scripts/study.py`; every grade gets the design search. Reconciliation
bands around them (model gaps and conservatisms,
`scripts/reconciliation.py`): extrapolations within 21.8-31.1, speculation within 9.9-11.6 at 1 GWe. With the coils
priced along the expansion adiabat (conductor growing as L^(1/3)), the design
search trades length for radius: the minima are fat short chambers. The dominant open
band is the compression field: the burnup basis is the patent's 22 T
point, and a 10 T / 5 T machine adds +2.3 / +11.4 $/MWh at the
speculation device. The recovery topology is the other: at the 40%
ceiling Slough (2025, Nucl. Fusion 65 106019, eq. 18) derives for a
flux-conserving expansion chamber, f_pdv 0.4 adds +17.4 at the extrapolation device and +4.2 at speculation (`reconciliation.py`,
RISK row).

## Coherence constraints (enforced, not advisory)

Seven physics couplings are enforced on every quoted point (five checked
by `study.coherence_violations`, the sixth and seventh applied by
construction in `study.run`); a stack that violates one of the five is
flagged in the output of every script rather than reported, and every
point carries the burn time the seventh implies:

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
4. **The D-rich fuel credit travels with its consequences.** Above
   dd_frac 0.5 the machine is a bulk tritium facility: the extrapolation
   device carries 211 MW of plant-level neutron power and breeds about
   78 kg of tritium per year, and Helion's own store-for-decay fuel
   cycle implies an equilibrium getter-bed inventory of production rate
   x mean decay time, about 1.4 tonnes of tritium on site. For scale:
   that inventory is 1.3e10 Ci, dissipates about 450 kW of continuous
   decay heat in the store, is roughly 350x ITER's 4 kg site limit and
   about 50x the world's civilian tritium stock (about 25-30 kg,
   CANDU-derived). `study.run` charges a tritium-plant adder on C220500,
   unit-priced rather than anchored: 50 M$ fixed core plus 0.657 M$ per
   MW of plant neutron power (a stated definition; the 100-300 M$
   reconciliation band at reference scale brackets it, and given the
   tonne-class inventory the allowance is more likely low than high).
   The extrapolation device's 189 M$ adder is a consequence of its
   throughput, not an identity. O&M stays at the baseline 27.5, never at
   an "aneutronic" discount.
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
   50 MJ) and V_f its own chamber, the whole volume stroke counted:
   Helion's burn-cycle framework (Kirtley, APS DPP 2024) defines its
   convergence and expansion ratios on volume, radial and axial
   together, so the axial fifth of the boundary work (Spencer 1983
   scalings) is not deducted; whether the end circuits return it is a
   design question the shot triplet on Polaris, Helion's operating
   prototype (a vacuum shot, a plasma shot without burn, and a burning
   shot), measures. The enforced expression is the Otto/Atkinson-form
   adiabatic-stroke bound at gamma = 5/3; the machine's actual cycle is
   Diesel-type (constant-pressure burn at the beta = 1 force balance)
   with an Atkinson over-expansion, the same generalized Diesel/Otto
   framework with axial and radial expansion that Helion's cited
   burn-cycle analysis (Kirtley, APS DPP 2024) uses, and the Diesel-form
   ideal value sits 1-2 percentage points below the enforced cap at the
   study's ratios, so the cap is strict and slightly generous. There is
   no Carnot exemption: cycle form, ratios, and merging entropy set the
   efficiency, which is what the composite cap encodes. Recovery cannot
   be claimed independently of the geometry that must deliver it. The
   adiabatic scalings say elongation falls as B^(1/5) during expansion,
   so nothing maintains aspect ratio; the plasmoid grows more oblate as
   it expands, and since tilt stability prefers prolate FRCs, the late
   expansion trades toward the tilt boundary, an unmodeled truncation
   risk on f_pdv that the composite cap's engineering margin partially
   absorbs at the extrapolation grade and speculation's zero margin does
   not. Slough (2025) caps the recoverable share of an FRC ejected into
   a flux-conserving expansion chamber at (1 - x_s^2)/(2.5 - x_s^2), 0.4
   at most, and holds that an FRC does not free-expand; that is the
   co-founder's own topology, not the discharged coil assumed here, and
   it is priced as a risk row (+17.4 / +4.2 $/MWh at the extrapolation / speculation device), not enforced.
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
   than the circuit loses per shot at any eta_dec in the ladder; the
   design-basis 128 MJ shot implies a 0.3 to 0.7 s burn and the
   speculation shot 1 to 3 s (`scripts/yield_bound.py`), and the bound
   reproduces Slough's (2025) own D-T design, where a gain of 9.1 on the
   FRC energy over a 2 to 5 ms transit at 34.8 T and 15 keV is a 3.4 ms
   burn at that point's breakeven time (`study.breakeven_time_dt_s`). No
   record supports any yield, so the shot is a graded claim at every
   grade rather than a shared basis: the records device is priced at
   Helion's shot so that a machine exists to cost, and every point
   reports `tau_burn_implied_s` at x_s 0.7 (`study.run`).

The store-and-decay idealization itself (dhe3_f_T = 0: no bred triton
burns in-plasma) is checked in `scripts/tritium_burn.py`. A triton born
mid-pulse burns before the pulse ends with probability (1/2) n_D <sigma
v>_DT tau, and because D-T reactivity is 27-87x D-D at 70-20 keV (each
unit of D burnup burns 14-43x as much bred tritium), each percent of
per-shot D burnup burns 14-43% of the bred tritium in-plasma; the fuel
cycle is only self-consistent with low per-shot burnup bought back by
rep rate. At Helion's stated pulse of hundreds of microseconds to
milliseconds (helionenergy.com/faq, June 2026 capture in
`docs/sources/`) and the densities of the Trenta prototype (1e22-3e22
m^-3) the burn fraction stays below about 1% and dhe3_f_T = 0 is a good
approximation; at reactor-class compression (1e23 m^-3) with
millisecond-plus burn times it reaches 4-13%. Priced at dhe3_f_T = 0.04
the extrapolation stack at Helion's chamber moves only +0.5 $/MWh, but
plant neutron power rises 23% and each burned triton emits a 14.1 MeV
neutron (5.8x the D-D neutron energy), so the LCOE story is insensitive
while the shielding basis and wall spectrum are not.

The model's own `burn_fraction` closes the same loop with no density or
burn-time input: the per-shot D burnup pins the integrated exposure n_D
<sigma v> tau, so f_T = 1 - (1 - e^-x)/x with x = (sv_DT/sv_DD)(-ln(1 -
f_D)). At the concept YAML's burn_fraction 0.15 (an unsourced
magnetized-inertial-fusion literature midpoint; Helion publishes gain,
not burnup) the implied in-pulse tritium burn is **78-93%** across 70-20
keV if tritons thermalize and stay confined - inconsistent with dhe3_f_T
= 0. The inconsistency is internal to the preset's assumption pair, not
an inference about Helion's machine; it partitions the operating space
into three regimes, each priced, none free: (a) per-shot burnup at or
below about 7e-4, which multiplies the CAS80 recycle-loss line 15x at
fuel_recovery 0.99 (2.4x at 0.999), collapses the bred-He-3 recycle
credit (its effective recycle fraction falls from 0.95 to 0.05-0.3), and
inflates the vacuum-pumping throughput the same knob sizes by two
orders; (b) prompt loss of the 1 MeV tritons from the plasmoid, whose
separatrix sits a few ion gyroradii from the field null, before they
thermalize, a fast-ion confinement question measurable on Polaris, which
also moves about 1 MeV per T branch from recoverable to undirected, and,
since the D-D proton is born with the triton's momentum and the D-He3
proton with 2.2 times it, the same orbit loss removes about four fifths
of the charged fusion energy at the D-rich mix, which the fuel-cycle
price of this regime excludes; (c) accept the burn: priced at dhe3_f_T =
0.78 the extrapolation stack at Helion's chamber is 44.8 and the
speculation device 14.5, plant neutron power rises about 5x with a
dominant 14.1 MeV component, and the decay store shrinks to about
0.2-0.3 t - and those LCOE figures are floors, because the wall/shield
audit checks surface heat only, not the D-T-class neutron loading it
would imply.

**The fuel-cycle basis and its patent source.** Helion's fuel-cycle
patent (published as US 2017/0011811, granted as US 11,469,003 B2)
publishes an operating table (n_D = 0.75e22 m^-3, T = 70 keV, tau =
0.157 s without tritium removal / 0.103 s with it) and states tritium
"may be removed between each pulse ... prior to undesired D-T reactions
taking place". Under the closure at 70 keV: D burn per confinement
period 2.5-3.8%, thermalized triton burn over that period 28-38% (the
patent's own case for inter-pulse removal); per sub-millisecond pulse at
the patent density, burnup 1.2-2.5e-4 and in-pulse tritium burn
0.2-0.3%, consistent with dhe3_f_T = 0. The model basis carries the
per-pulse pair (burn_fraction 1.2e-4, burn_fraction_he3 4.1e-4,
species-resolved recycle losses, fuel_recovery 0.9999), under which fuel
resides for of order a thousand pulses and the load-bearing claims are
four-nines per-pulse recovery and hertz-rate isotope separation
(unburned-fuel multiplier 84x / 9.3x / 1.8x at two / three / four
nines). Grade: published design intent; the reactor-point compression
density may exceed the patent value, which would move the machine right
along the burnup axis.

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

`scripts/burnup_scan.py` prices the whole axis coherently: both species'
per-pass burn fractions derive from the same n tau, so burn_fraction_he3
scales with burn_fraction at the fixed 70 keV reactivity ratio (3.3x),
with dhe3_f_T tied to the closure (thermalized branch) or held at zero
(prompt-loss branch), at fuel_recovery 0.99, 0.999, and 0.9999. At the
patent-density basis the recovery nines carry everything at the
speculation device: 10.6 $/MWh at fr 0.9999, 12.2 at 0.999, 27.0 at 0.99
(the fourth nine is worth 1.6 $/MWh, the third 15). Toward higher
compression density the recovery requirement relaxes: above per-pulse
burnup of about 1e-3 the three- and four-nines curves converge near
10.0-10.3 $/MWh prompt-loss, and the axis minimum (10.0 at burnup 1e-2
to 3e-1) sits about 0.6 $/MWh below the basis, while the thermalized
branch turns up past burnup 0.01 as the tritium burn grows: the
triton-fate question reopens exactly where the recovery question closes.
Per-pulse exhaust pumping peaks at the basis (78 M$ per module at the
floor).

The scan also reprices neutron damage, which the base model cannot see
(core_lifetime is inert for this concept): replacement of the exposed
package is levelized from the 14-MeV-equivalent neutron wall load (10
dpa, displacements per atom, per MW yr/m^2 in Fe-based structure, 2.45
MeV D-D flux folded at 0.4) at two tolerances, 20 dpa (the edge of the
irradiation database for reduced-activation ferritic-martensitic, RAFM,
steel) and 50 dpa (the DEMO-class design target). The event is C220101 +
C220103: the coil bore sits 0.10 m behind the wall with no blanket, so
the close-coupled copper coils see the same fluence and are replaced
with the wall (they are the cheap part: 14 vs 106 M$ at the speculation
device under the adiabat coil pricing; ceramic insulation is a
prerequisite, since organics die at 1e9 rad in weeks at these fluxes).
At the patent basis the spectrum is pure 2.45 MeV D-D at a
14-MeV-equivalent load of 0.20 MW/m^2 and the adder is modest (+0.3-1.2
$/MWh at 50-20 dpa, replacement intervals 10-26 years). The 8-16 $/MWh
triton-fate spread survives only as the high-burnup counterfactual
(reactor-point density well above the patent value with thermalized
tritons), where the extrapolation stack's divertor-class wall makes
replacement prohibitive (+52 to +134 $/MWh). Two couplings the damage
column exposes: low burnup raises neutron damage as well as fuel cost
(more D-D events per MWh), and keeping the tritium out of the burn is
free insurance at the basis and worth double digits off it.

**Why the blanket escape is closed for the compression section.** A
pulsed inductive machine pays per pulse for every cubic meter of flux
volume between coil and plasma: W = (B^2 / 2 mu0) x annulus volume,
recovered only at the composite efficiency. The 50 MJ driver at the
22 T basis field implies about 0.26 m^3 of compression-section flux
volume (bore of order 0.1-0.2 m); a 0.4 m shield under the compression
coil then multiplies the swept annulus by more than an order of
magnitude (C220107 and its CAS72 schedule scale with the store), and
the extra hundreds of MJ/pulse cycled at composite 0.90 dissipate tens
of MJ/pulse: order 100+ MW of recirculating loss at the tier-3 rep
rate, and more than the module's output at the tier-2 composite. Eddy screening
is the lesser problem (steel skin depth is about 16 mm at ms rise
times, so structure must be laminated; FLiBe at 200 S/m is
magnetically transparent); the irreducible cost is the magnetized
volume itself. A shield is energetically cheap only around the
low-field regions of the machine (W scales as B^2: MJ-class per pulse
at 0.5 T and below). The coils nearest the burn are therefore
sacrificial, ceramic-insulated, and on the wall-replacement schedule,
which sharpens the tritium argument: the unshieldable compression
section is exactly where a 14 MeV spectrum hurts most. Honesty note the other way: the scan spreads neutrons
uniformly over the cylinder, but the burn is localized near the
compression section, whose wall and coils see several times the
average load on 15-20% of the event value; a localized audit would
raise the damage adders by very roughly 2x. Together with the
fission-spectrum 20 dpa edge and the 10x helium-per-dpa of 14 MeV
neutrons, the adders are more likely low than high.

**When replacement becomes rebuilding.** The exposed package (wall +
coils + vessel shell, 155 of about 370 M$ per-module reactor hardware at
the speculation device) crosses from maintenance into machine-
replacement when the wall-and-coil event (120 M$) recurs faster than
event / (capital recovery factor x module hardware), about 10 years at
the speculation grade's 3% real (5 at 7%): under that, the reactor line
is replacement-dominated and the machine is opex. At the patent basis
(D-D spectrum) the interval is about 10 to 25 years at 20 to 50 dpa, a
capital asset at the design target and at the line at the RAFM database
edge (the derived availability carries this changeout: 25 years at the
speculation device, 42 at extrapolations, 17 at the records device); the
consumable core (1-3 yr intervals, half the module's value swapped
near-annually) is the high-burnup thermalized counterfactual. In that
regime the honest design is Helion's factory logic taken to its
conclusion: a swappable irradiated cartridge with hot-spare bays (a
single-module 1 GWe plant cannot hold its derived 0.92 availability
through annual month-scale swaps; a multi-module park can, at roughly
one spare module of extra capital), a refurbishment line, and a few
hundred tonnes per year of activated steel and copper that neither the
CAS50 decommissioning provision (140 M$) nor C220110 remote handling (16
M$) is scoped for. Consumable- core economics are marginal-manufacturing
economics, which is where the missing fleet-learning term would finally
bind on something real.

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
records the Magnetic D-T Corridor ladder uses and reaching the
CCGT-class build only at speculation. Derived at every point, never
asserted: availability, from the replacement schedule the model already
prices.

Held at every grade:

| knob | repo default | value | why it applies | source (grade) |
|---|---|---|---|---|
| inflation_rate | 0.02 (code default) | 0.0 | Constant-dollar framing. With inflation_rate 0 the model discounts capital, replacement events, and operating costs at one real rate. The code default escalates only the operating costs (the overnight cost and replacement events are never escalated), a hybrid in which the nominal rate acts as a real rate on capital and the operating costs carry a 23% levelization premium at 30 years. Constant dollars is the IEA/NEA, EIA AEO, and NREL ATB practice. | Framing choice; see interest_rate (convention) |
| indirect_fraction | 0.20 | 0.20 (16.7 / 16.7 / 10.8 / 8.3% effective by grade) | Large industrial engineering, procurement and construction (EPC) analog, on the same cost-basis scope as NETL's EPCM line (fraction of total direct cost), at the NETL 20% that is also the model default. The model computes CAS30 = fraction x CAS20 x (construction_time_yr / 6 yr), so the effective fraction follows the build: 16.7% at the 5 yr grades, 10.8% at 3.25 yr, 8.3% at 2.5 yr. The Borealis ledger forces 8% effective at every grade by entering 0.192 at its 2.5 yr build; see the consistency table. | US DOE/NETL Quality Guidelines for Energy System Studies (strong) |

Stepped with the tiers:

| knob | design basis | records | extrapolations | speculation | what it is | source |
|---|---|---|---|---|---|---|
| interest_rate (real) | 0.07 | 0.07 | 0.05 | 0.03 | financing: the cost of capital, a change of risk-bearer rather than of technology; Figure 1 and the at-7% column keep it separate | IEA/NEA 2020 (3%, 7%, 10% real cases, 7% central); 5% a loan-guarantee blend with precedent, 3% sovereign-class capital with no mechanism; no fusion plant has a record at any grade |
| lifetime_yr | 30 | 30 | 80 | 80 | engineering: what cannot be replaced sets it; bank and wall replacements are priced at every grade, so 80 yr is worth 4.5 $/MWh at the extrapolation device against 30 | 30: model default and the low end of the fusion literature (Böhnlein et al. 2026, median 30-40 yr; ARIES 40); 80: US DOE hydropower lifespan 65-85 yr, every core component on its own replacement schedule |
| construction_time_yr | 5.0 | 5.0 | 3.25 | 2.5 | engineering: the build, which also sets the effective indirects through CAS30's build-time scaling; worth 1.7 $/MWh at the extrapolation device against 5 yr | 5 yr: the serial Hualong One builds, about 60 months from first concrete to grid (Zhangzhou 1, construction start October 2019 to grid 28 November 2024, World Nuclear News 2025); 3.25 yr: the Kashiwazaki-Kariwa ABWR pair, 37 and 39 months from first concrete to fuel load (Omoto 2002, Nuclear Engineering International), at the peak of a mature LWR supply chain; 2.5 yr: CCGT-class build (Siemens Energy 1200 MW block in about 30 months), which no fusion plant has a record of; the same ruling as the Magnetic D-T Corridor ladder |
| availability | derived | derived | derived | derived | 0.98 outside planned outages, less a routine bundle (34 d every 2 yr), the bank swaps (34 d each at the shot life) and the wall-and-coil changeouts (84 d each at the dpa tolerance); `study.replacement_schedule` | US fission fleet (WNA, EIA, IAEA PRIS) for the 0.98 and the 34 d; Thea Energy Helios for the 84 d; see below |
| wall_dpa_tolerance | 20 | 20 | 50 | 50 | engineering: sets the changeout interval in the availability derivation (0.2 $/MWh at the extrapolation device) | 20 dpa: demonstrated RAFM database edge; 50 dpa: DEMO-class design target |

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

Derived availability per device at 1 GWe (`outputs/devices.csv`; the
3 GWe parks are within 0.001), with the three outage terms as fractions
of calendar time:

| device | availability | routine | bank swaps (every yr) | wall changeouts (every yr) |
|---|---|---|---|---|
| citable records | 0.893 | 4.7% | 2.8% (3.3) | 1.4% (16.8) |
| Helion's requirements | 0.901 | 4.7% | 2.9% (3.2) | 0.5% (43.9) |
| extrapolations | 0.921 | 4.7% | 0.8% (11.8) | 0.5% (42.5) |
| speculation | 0.924 | 4.7% | 0.1% (91.6) | 0.9% (25.4) |

The result sits just under the red-team review's 0.93-0.95 band and at
the top of the fusion literature's 0.75-0.90. Sensitivity, with
availability pinned instead of derived (`outputs/devices.csv`): the
3 GWe speculation park reads 9.0 $/MWh at the model default 0.85 and 8.2 at 0.95, so it crosses $10/MWh at any availability above the default and, with the wall-and-coil replacement hardware of 0.4 to 1.2 $/MWh added, reads 8.8 to 9.6; the extrapolation device moves 28.4 to 26.2 $/MWh over the same span and the records device 121.1 to 115.1.

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
| lifetime_yr (30) | No fusion plant has a book-life record, so the design-basis 30 yr holds here; the 80 yr civil-works entry is a tier-2 extrapolation. With the 1e8-shot bank at 1 Hz the bank turns over about eight times in 30 years, and the model prices every one of them. |
| c_cap_allin_per_joule (0.5) | Already at the optimistic end of its own documented 0.5-4.0 range; the industry statement is that Hz-rate operation still requires a 5-10x cost reduction. No record below the baseline exists. |
| eta_dec (0.85) | 0.97 is not tier-1-admissible: it is the top of a patent's prophetic circuit-only band (US 2024/0275198 A1), and Helion's "95% proven" statements trace to no-fusion circuit tests. Tier 2 carries 0.90 under the composite cap. |
| cap_shot_lifetime (1e8) | The 1e9 figure is a published NOAK *target* (Pacific Fusion's pulsed-power driver; Langtry et al. 2025, arXiv:2504.10680) resting on a vendor-catalog derating extrapolation, not a life test; the largest rep-rated MJ-class precedent is 1.3e4 shots. Tier-2 material by the study's own convention. |

## Tier 2: labelled extrapolations

| knob | baseline | value | basis | grade |
|------|----------|-------|-------|-------|
| cap_shot_lifetime | 1e8 | 1e9 | Pacific Fusion (Langtry et al. 2025) sec. 4.1: 100 to 35 kV derating projected to reach about 1e9 shots at about 9x lower energy density; General Atomics Series DE capacitor cross-check (3e7-3e9 at 20% reversal). At the extrapolation device the plant fires about 7e9 shots over its 80-year book life, so the bank is replaced about 7x (charged to CAS72 by the model); the "1e9 outlives the plant" argument holds only below about 0.4 Hz. | published target |
| fuel_recovery | 0.999 (tier-1 record) | 0.9999 | One nine beyond the JET-ILW retention record: the patent closed fuel cycle (US 2017/0011811) implies four-nines per-pulse recovery for the He-3 economy to close, and the physical argument (saturated walls, helium-dominated exhaust, direct re-injection without full reprocessing) points the right direction. No demonstration at any scale. Worth 6.4 $/MWh at the extrapolation device if reverted, with the store's He-3 return credited. | patent-implied extrapolation |
| eta_dec | 0.85 | 0.90 | Bottom of the patent band, circuit-only, no fusion-inclusive measurement. Paired with the basis f_pdv under the composite cap (0.90 x 0.80 = 0.72 <= 0.80 at the extrapolation device, where the chamber's adiabatic bound, 0.98, sits above the claim). | weak-moderate |
| f_pdv | (derived) | min(claim, expansion bound) | Not a record: capped per point under coherence constraint 6 by the chamber's adiabatic expansion bound on the whole volume stroke; at the extrapolation device's chamber the bound (0.98) sits above the tier's 0.80 claim, so the claim stands. | constraint-derived |
| eta_pin | 0.95 | 0.98 | Solid-state pulsed-power wall-plug efficiency; plausible for modern semiconductor switching, no datasheet or Helion statement located. | UNSOURCED |
| max_f_rep | 1.0 | 3.0 | No public Helion statement of a numeric plant rep rate exists (Polaris target about 1/s; Trenta about 1/10 min; the 1-10 Hz band is the concept YAML's roadmap paraphrase). 3 Hz is what the bought wall supports at this tier's recovery parameters; it remains UNSOURCED as a demonstrated cadence (nothing MJ-class has run at 1 Hz continuously). The band top (10 Hz) is speculation. | UNSOURCED-ROADMAP |
| fw_class | panel | hhf | Machine-design purchase, not a record: divertor-grade monoblock wall (ITER divertor procurement anchor, 2.5 M$/m^2 NOAK, 10 MW/m^2 qualification) over the real 44.6 m^2 cylinder, 112 M$/module, to make 3 Hz admissible in the design-basis chamber. The extrapolation device instead buys a fatter chamber with the cheaper panel wall (see coherent minimum below). | design purchase |
| dhe3_dd_frac | 0.488 (the patent's He3/D = 0.158 at 70 keV as a D-D event share) | 0.85 | D-rich operation to raise in-situ He-3 breeding (prompt D-D He-3 plus stored-tritium decay) and cut the purchased-fuel line; the concept's own stated direction, but 0.85 is the top of a sweep, not a derived operating point. Adopted only jointly with f_rad 0.28 and the tritium-plant adder (coherence constraints 1 and 4). Slough (2025) restates the patent's mix as the self-sustained cycle's limit, citing the same patent; 0.314, the blog's 3:1 D:He-3 bremsstrahlung minimum, is the floor's calibration anchor. | UNSOURCED |
| f_rad | 0.163 | 0.28 | Bremsstrahlung-consistent radiated fraction at dd_frac 0.85 under the study calibration; relativistic corrections would raise it another 10-25%. Not an optimistic move: this knob *costs* 1.1 $/MWh against the incoherent alternative, and is the price of the fuel credit. | physics floor |
| interest_rate | 0.07 real | 0.05 real | Cost of capital (financing): federal loan guarantees blended with utility equity, a mechanism with precedent but no fusion record, between the IEA/NEA 2020 central and low cases. The one entry that is financing rather than technology; Figure 1 and the at-7% column keep it separate (worth 7.1 $/MWh at this device against 7%). | mechanism with precedent |
| lifetime_yr | 30 | 80 | Book life (engineering): US DOE hydropower lifespan (65-85 yr) with every core component replaced on its own schedule; the unreplaceable structure sees negligible neutron fluence (copper coils are replaced with the wall, D-D neutrons only). Bank and wall replacements are priced at every grade, so the model shows where 80 yr pays: 4.5 $/MWh here against 30 yr, with the bank turned over about 7x. | civil-works record |
| construction_time_yr | 5.0 | 3.25 | Construction (engineering): the Kashiwazaki-Kariwa ABWR pair, 37 and 39 months from first concrete to fuel load (Omoto 2002, Nuclear Engineering International), at the peak of a mature LWR supply chain, against the 5 yr held at the design basis and records grades (the serial Hualong One builds, about 60 months from first concrete to grid (Zhangzhou 1, construction start October 2019 to grid 28 November 2024, World Nuclear News 2025)). Also lowers the effective indirects from 16.7% to 10.8% through CAS30's build-time scaling; worth 1.7 $/MWh at this device against 5 yr. Same ruling as the Magnetic D-T Corridor ladder. | demonstrated once |
| wall_dpa_tolerance | 20 | 50 | DEMO-class RAFM first-wall design target against the demonstrated 20 dpa database edge; enters only through the changeout interval in the derived availability (0.2 $/MWh). | design target |

**Held at baseline in tier 2, harmonized with the Borealis ledger:**
om_cost_dhe3 (27.5: already the lowest documented CCGT fixed-O&M figure;
also required by coherence constraint 4), installation_frac (0.14: no
defensible record on the model's cost basis), f_rad as an independent
mover (a coupled variable, not a knob).

## Tier 3: labelled speculation

No entry has a source; each is the optimistic edge of a stated argument or
an explicit leap. See `config/tier3.yaml` for the per-knob notes.

| knob | value | note |
|------|-------|------|
| max_f_rep | 10 | top of the third-party roadmap band; no duty-cycle analysis supports it |
| cap_shot_lifetime | 1e10 | required for coherence with 10 Hz; no source at any price; jointly heroic with the $/J entry below |
| eta_dec x f_pdv | 0.95 x 0.947 = 0.90 | the theory-optimal composite taken at face value, zero engineering margin; f_pdv 0.947 sits within 0.04 of the 30 m chamber's adiabatic bound (0.989). The source figure (Kirtley, APS DPP 2024, 'optimal burn cycles exceeding 90%') is unreproducible: its numerator is independently verified but its input-accounting denominator is defined in neither slide nor talk (docs/sources/kirtley_dpp24_formulas.md) |
| c_cap_allin_per_joule | 0.1 | below the model's own documented range floor; contradicts the derating physics that buys the cap life above |
| u_he3 | 5e5 $/kg | no fleet-scale He-3 market exists at any price. The DOE Isotope Program's 2011 allocation was 600 $/L to federal and 1,000 $/L to commercial users (CRS R41419), 4.5-7.4 M$/kg, and prices have risen several-fold since: the 2024-2026 transactions are gram-to-kilogram scale at 19-22 M$/kg (Edelgas spot; Interlune's DOE and Maybell Quantum agreements at the commercial price; TAE's Black Moon lunar option undisclosed), with every new entrant building toward the high price. This entry is 9x below the 2011 allocation and 40x below the commercial spot. The breeder section below prices the He-3 each device buys: the ledger's 2 M$/kg is reproduced at the records grade, unexplainable at the Helion device (6.4-7.2 M$/kg), conservative at the extrapolation grade, and this entry sits inside the speculation-grade 0.2-0.5 M$/kg band. |
| dec_staged_recovery_factor | 0.5 | patent's unquantified "net reduction in cost and size", optimistic edge |
| c_inv_per_kw_net | 50 $/kW | small lever |
| multi_unit_labor_factor | 0.80 | small lever |
| interest_rate | 0.03 real | IEA/NEA 2020 low case: sovereign-class capital with no mechanism that delivers it to a first-of-a-kind fleet; financing, shown separately (worth 7.2 $/MWh at 1 GWe and 6.2 at 3 GWe against 7%) |
| construction_time_yr | 2.5 | CCGT-class build (Siemens Energy 1200 MW block in about 30 months) for a fusion module with a tritium facility; no fusion plant has a build record; effective indirects 8.3% at this build |
| yield_per_shot_mj | solved, not asserted; a graded claim at every grade (constraint 7) | no record supports any yield: Helion's stated pulse returns under half a megajoule from the 50 MJ bank, the design-basis 128 MJ shot implies a 0.3 to 0.7 s burn and the speculation shot 1 to 3 s (`scripts/yield_bound.py`), so the records device is priced at Helion's shot only so that a machine exists to cost. Gain speculation is admitted, but the shot must be survivable in the chamber it is costed in: `coherent_min.py` solves yield and chamber jointly. The optimum is a broad plateau (200-1000 MJ in a 30 m x 1.5 m single-module chamber, 1.8-9.0 Hz, panel wall at its flux limit, all within 0.1 $/MWh). Gain 40 (2000 MJ) in the concept preset's 0.5 m x 10 m chamber deposits about 6.7 MJ/m^2 per shot, four times the tungsten flash-melt bound, and is excluded. |

## The coherent minimum, and the $10 question

`scripts/coherent_min.py` searches the design space the machine actually
controls (yield, chamber size, wall class, burn mix) under the coherence
constraints, at each evidence level:

| device | LCOE | design |
|---|---|---|
| citable records, 1 GWe | **119.3** | design-basis shot, D-rich mix with tritium plant, 25 modules of 10 m x 0.75 m at 1 Hz (records-only optimum; the mix freedom every grade gets; the 15 m x 0.5 m chamber is 1.5 $/MWh behind, the best row at the 3:1 D:He-3 mix 43 behind) |
| extrapolations, 1 GWe | **26.8** | design-basis shot (128.1 MJ), 7 modules at 2.7 Hz, 10 m x 1.5 m chambers, panel wall, D-rich mix with tritium plant (the best row at the 3:1 mix, 40.8, is 15 behind) |
| speculation, 1 GWe | **10.6** | 300-1000 MJ shots in the same 30 m x 1.5 m panel-wall chamber sit at 10.6-10.7, within model precision (500 MJ at 3.5 Hz carried: the plateau's middle, with a 0.54 MJ/m^2 flash margin), single module, D-rich. The 3:1 mix (dd_frac 0.314) is 1.9 behind (12.5 in a 20 m x 1.5 m chamber), the preset's He-3-rich mix (0.131) 2.4 behind, and both rest on the tier-3 0.5 M$/kg He-3 entry |
| speculation, 3 GWe | **8.4** | 3 modules of the 200 MJ / 30 m design at 9.0 Hz (larger shots trip the wall audit once the integer module count snaps down) |

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
length for radius and the minima are fat short chambers (10 m x 0.75 m
to 30 m x 1.5 m), inside or near the built length envelope. The public
facility imagery also corroborates the cost structure at today's prices:
most of the Polaris building's floor is the pulsed-power farm (about
2,500 stacked power units) with the fusion machine in a small corner,
which is precisely the picture the tier-3 capacitor $/J and shot-life
entries claim will invert.

Reconciliation (`scripts/reconciliation.py`) puts honest bands around
these. The shot-cycled replacement of the recovery store and switch
stack (CAS72, with the bank) and the recovery-store markup (f_pdv (1 -
f_rad)) are inside costingfe and priced in every number above. What
remains outside: high-voltage DC switch repricing (+1.3 extrapolation /
+0.5 speculation), the driver-thermalization derate (below),
tritium-plant band (+-0.6 / +-0.4), and a thermal-bottoming basis change
(-4.3 / -0.3): the extrapolation device lands in 21.8-31.1, the
speculation device in 9.9-11.6 at 1 GWe.

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
eta_dec chi (1 - f_pdv) p_driver is worth +1.4/+2.4/+3.3 $/MWh at the extrapolation device across that x_s span (960 MW of circulating driver
power) and +0.03 to +0.07 at the speculation device; at the low-gain
Helion device it would be order +10. The Polaris shot triplet (vacuum /
plasma no-burn / burning) separates eta_dec, chi (1 - f_pdv), and the
fusion composite, so the study's most-wanted measurement delivers chi as
a by-product; until then, published excluded-flux radii (x_s) pin it per
shot. The disposal of the FUSION heat is already in the model: f_rad
radiates to the wall, (1 - f_pdv) of the remainder is dumped undirected
at end of pulse, and eta_th = 0 discards the lot, which is what drives
the wall-flux audit and the bottoming credit. The expansion bound is
enforced as coherence constraint 6 (f_pdv capped per point by the
chamber's expansion ratio on the whole volume stroke): the extrapolation
device's 10 m x 1.5 m chamber caps it at 0.98, above the claimed 0.80,
and the speculation device's 30 m chamber at 0.989, just above the
claimed 0.947; whether the end circuits return the axial fifth of the
work is resolvable by the Polaris shot triplet. Parallel particle
streaming through the exhaust is captured by nothing at any grade.

**The He-3 market makes the fuel accounting first-order.** At the DOE
Isotope Program's 2011 allocation of 4.5 M$/kg (he3_scan's 4.5e6 row)
the extrapolation device reads 28.5 $/MWh at dd_frac 0.85 and 67.6 $/MWh at the 3:1 mix (dd_frac 0.314); at the 19-22 M$/kg commercial spot (the
2e7 row), 39.2 and 226: the 3:1 mix does not survive market-priced He-3,
the D-rich mix nearly does. That reading follows from the model's fuel
accounting: prompt bred He-3 is credited through its species-resolved
cumulative recycle fraction (0.80 at the per-pulse basis: He-3 burns out
of the loop 3.3x faster per pass than it leaks), and the decay store's
He-3 return, 0.42 atoms per primary event and equal to the prompt
branch, is credited atom for atom against the purchased 1 - dd_frac per
event, levelized over the store's build-up at the grade's rate
(`study.he3_purchase_fraction`: 0.24 / 0.82 / 0.16 / 0.11 of the
perpetual purchase down the ladder; `he3_decay_return=False` restores
the perpetual purchase). Without the credit the machine would import
about 34 kg/yr in perpetuity; with it the D-rich device buys only during
the build-up. The u_he3 = 0 row (25.4 $/MWh) is the full steady-state
self-supply limit at the D-rich mix. At zero price the mix itself
changes: the design search re-run at u_he3 = 0
(`he3_scan.optimum_by_mix`, `outputs/he3_free_by_mix.csv`) picks the
He-3-rich mix (dd_frac 0.131) in 15 m x 0.75 m chambers at 20.3 $/MWh for the extrapolation grade and, in 15 m x 1.5 m chambers, 8.5 for
speculation (17.7 and 6.5 at 3 GWe), with no tritium plant, so a free-He-3 concession is worth 6.5 and 2.1 $/MWh at 1 GWe, not the 1.4
and 0.2 the D-rich machines show. The distance between those two
readings, 25.4 vs 39.2 at the same machine, is what the D-rich machine's
build-up purchases cost at the market price. The credit is worth 7.1
$/MWh at the study's u_he3 (33.9 without it), about 3 at the 2011 DOE
allocation of 4.5 M$/kg and about 14 at today's commercial spot; it is
coupled to the burnup closure, because the return exists only if the
tritium survives the pulse.

**The $10/MWh target is crossed by the full speculation stack as a 3 GWe
park (8.4 $/MWh; 10.6 at 1 GWe), and by nothing below it; with the
wall-and-coil replacement hardware of `burnup_scan.py`, 0.4 to 1.2
$/MWh, the park reads 8.8 to 9.6.** What carries it there is the cost of
capital, not a physics or engineering entry: the same machine at the
design-basis 7% real reads 14.6 $/MWh (17.9 at 1 GWe), so the 3% real
sovereign-class rate is worth more than the whole distance to the
target; the figure also needs the derived availability of 0.92 (9.0
$/MWh at the model default 0.85). He-3 at zero price takes the 3 GWe
park to 8.2 $/MWh at the D-rich mix and to 6.5 with the design search
re-run at that price, where the optimum is the He-3-rich mix (dd_frac
0.131, 200 MJ shots in 15 m x 1.5 m chambers, no tritium plant;
`scripts/he3_scan.py`). What carries the floor at the speculation device
is not the capacitor bank: it is buildings (CAS21 286 M$), heat
rejection and electrical plant (CAS24-26 about 170 M$), CAS50 (199 M$,
of which 140 is the decommissioning provision), fuel handling plus the
tritium plant (about 190 M$), and the first wall of the big chamber (106
M$). See `docs/writeup.md` for the account-by-account anatomy and the
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
| citable records | 176 | 12.8 | 2.2 | 2.5 | 120.1 / 121.8 |
| Helion's requirements | 98 | 5.6 | 6.9 | 7.9 | 161.2 / 170.4 |
| extrapolations | 34 | 26.4 | 0.70 | 1.04 | 25.9 / 26.1 |
| speculation | 25 | 133 | 0.18 | 0.54 | 10.5 / 10.6 |

The ledger price of 2 M$/kg is read back within a tenth at the records
grade (2.2 M$/kg co-sited), cannot be reached at the Helion device (a
module that breeds 5.6 kg/yr at a gain of 0.46), and is conservative
from the extrapolation grade on. A central facility serving several
devices reads 1.9 to 0.8 M$/kg at the extrapolation grade for one to
twenty devices (`outputs/breeder_siting.csv`), since the fixed tritium
core and the standalone intercept spread over more kilograms. The scheme
relocates the tritium inventory rather than shrinking it.

## Robustness of the extrapolation device

One-at-a-time reversion from the 26.8 point (`scripts/tornado.py`):

| knob reverted | LCOE | delta |
|---|---|---|
| cap_shot_lifetime -> 1e8 | 63.6 | +36.8 |
| dhe3_dd_frac -> 0.488 (with its f_rad) | 38.8 | +12.0 |
| max_f_rep -> 1 Hz | 38.4 | +11.6 |
| interest_rate -> 0.07 (financing) | 33.9 | +7.1 |
| fuel_recovery -> 0.999 (JET-analog) | 33.2 | +6.4 |
| lifetime_yr -> 30 | 31.3 | +4.5 |
| eta_dec -> 0.85 | 28.7 | +1.9 |
| construction_time_yr -> 5 yr | 28.5 | +1.7 |
| f_rad -> 0.23 (incoherent: floor violated) | 25.3 | -1.5 |
| eta_pin -> 0.95 | 27.4 | +0.6 |
| wall_dpa_tolerance -> 20 | 27.0 | +0.2 |

The cap-life lever counts the full shot-cycled recovery chain (bank,
store and switch stack, CAS72): at 1e8 shots everything that cycles is
replaced about 0.9 times a year, some 70 times over the 80-year book
life. Four extrapolation entries carry the number: the capacitor life
dominates at +37 $/MWh (a published derating target), the burn mix and the rep rate follow at +12 and +12 (an unsourced sweep endpoint and an
unsourced roadmap band), and the per-pulse fuel recovery, +6 with the
store's He-3 return credited (an extrapolated nine beyond the JET
retention record), sits with the two environment entries, the cost of capital (financing, +7.1), the book life (+4.5) and the build (+1.7); f_pdv does not
appear: the extrapolation stack leaves it at the basis 0.80 under a cap
that does not bind. None is a record. That is the honest quality of the 26.8 figure.

## Consistency with the Borealis ledger

Both studies price NOAK plants with the same framework, so a knob gets the
same ruling in both unless a physics or technology difference is stated.

| knob | Borealis | Helion | divergence justified by |
|---|---|---|---|
| interest_rate | 0.07 / 0.07 / 0.05 / 0.03 real by grade | same | same ladder: the cost of capital steps with the tiers as financing and is shown separately in both studies (composition figure, at-7% column) |
| inflation_rate | 0.0 | 0.0 | same: constant-dollar framing |
| construction_time_yr | 2.5 held | 5.0 / 5.0 / 3.25 / 2.5 by grade | **divergent**: this study steps the build with the tiers on the fission build records (the serial Hualong One builds at about 60 months, the Kashiwazaki-Kariwa ABWR pair at 37 and 39 months to fuel load) and reserves the CCGT-class 2.5 yr for speculation, as the Magnetic D-T Corridor ladder does; the Borealis ledger holds 2.5 yr at every grade and should adopt the same ruling |
| indirect_fraction | 0.192 (8% effective at 2.5 yr) | 0.20 nominal (16.7 / 16.7 / 10.8 / 8.3% effective by grade) | **divergent**: this study enters the NETL 20% at the model default and lets CAS30's build-time scaling set the effective fraction; Borealis forces 8% effective at every grade; one convention should be chosen and the effective fraction stated in both |
| installation_frac | held 0.14 | held 0.14 | same |
| om_cost | held | held | same; additionally forced here by the tritium facility |
| f_rad_fus / f_rad | held | coupled variable | **stated physics reason**: here f_rad is a function of the burn mix (bremsstrahlung floor), not an independent knob; Borealis's photon fraction is set by its own burn physics and was held |
| availability | derived per grade, 0.927 to 0.932 | derived per grade, 0.893 to 0.924 | same derivation (the fission fleet's 0.98 outside planned outages, less a 34-day routine bundle every two years and 84-day wall changeouts on the model's own schedule); **stated technology reason** for the gap: the shot-cycled bank swaps and the unshielded wall's fluence-limited changeouts, which the mirror does not have |
| lifetime_yr | 30 / 30 / 80 / 80 by grade | same | same ladder: 30 yr (the model default and the literature's low end) through the records grade, the 80-year civil-works life from the extrapolation grade in both |
| eta_th | 0.53 (combined cycle) | 0 (basis), 0.30 as reconciliation add-back | **stated technology reason**: no thermal conversion path in the machine basis; the rejected-heat stream at the extrapolation grade makes bottoming worth -4.3 $/MWh, carried as an add-back exactly as Borealis carried its excluded direct-conversion add-back |
| conductor_cost_rebco | held | not applicable | copper pulsed coils, no superconductor |
| fw_class / q_surface_max | hhf / 10 (machine design) | panel or hhf, design-optimized | same treatment: the wall package is machine design, not a record; here the wall is audited in-model against the declared class |
| unsourced first-order inputs | p_input quoted as a range | max_f_rep and yield quoted as a surface (`locus_scan.py`) | same treatment |

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
reconciliation: +2.3 / +11.4 $/MWh at the speculation device for 10 T /
5 T); (b) the magnetic pressure at 22 T is about 193 MPa, cycled
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
2. A duty-cycle analysis for any rep rate above about 1 Hz: switch and
   capacitor cycle life, vacuum recovery at 100-300 ms periods, coil and
   chamber thermal management.
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