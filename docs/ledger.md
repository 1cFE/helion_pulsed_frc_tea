# Evidence ledger

Every non-baseline value adopted in the ladder, with the analog class named
and the reason it applies. Tiers follow the Borealis convention: tier 1 is a
citable record or published bound, tier 2 a labelled extrapolation from a
stated roadmap or physical argument, tier 3 labelled speculation with no
source. "Held at baseline" is the recorded outcome when no defensible value
exists.

Orientation: the machine is a pulsed inductive-DEC generator with no
turbine, its burning plasma a D-He3 FRC, 1 GWe as an integer count of
Helion-class modules; design basis in
`config/baseline.yaml`, capacitor and pulsed-power evidence in
`docs/capacitor_technology_report.md`, adversarial findings in
`docs/red_team_review.md` (all of whose verdicts are folded into the tier
composition below), narrative answer in `docs/writeup.md`.

All numbers at costingfe `44434d9` (cylinder geometry + wall-flux audit
for linear pulsed concepts; shot-cycled CAS72 replacement scope;
physics-consistent recovery-store markup; per-pulse fuel-cycle
semantics with species-resolved DHE3 recycle losses), pinned by the regression tests
in `tests/test_study.py`. The tier stacks are `config/best_case.yaml`,
`config/tier2.yaml`, `config/tier3.yaml`; `scripts/tiers.py` reproduces the
ladder end to end.

Ladder at 1 GWe / 3 GWe (config stacks, concept-YAML chamber):

| rung | 1 GWe | 3 GWe |
|---|---|---|
| design baseline (Helion's implied point) | 145.4 | 140.7 |
| tier 1 records | 217.9 | 214.2 |
| tier 2 extrapolations | 49.2 | 45.3 |
| tier 3 speculation | 18.3 | 14.8 |

The tier-1 rows sit above the design baseline: reverting the vendor's
per-pulse fuel recovery to the JET-analog three nines and the recovery
share to radial-only costs more than every finance record saves, so on
evidence alone the fuel cycle is uneconomic and the descent begins
when the recovery extrapolations are granted at tier 2.

Design-optimized coherent minima (chamber, wall class, and burn mix
chosen by `scripts/coherent_min.py` under the physics-consistency
constraints in `scripts/study.py`; every tier gets the design search):
**tier 1: 173.0**, **tier 2: 41.0**, **tier 3: 16.8** at 1 GWe
(169.6 / 37.3 / 13.5 at 3 GWe). Reconciliation bands around the minima
(model gaps and conservatisms, `scripts/reconciliation.py`): tier 2
within 31.4-48.8, tier 3 within 15.6-18.1 at 1 GWe. With the coils
priced along the expansion adiabat (conductor ~ L^(1/3)), the design
search trades length for radius: the minima are fat short chambers. The dominant open
band is the compression field: the burnup basis is the patent's 22 T
point, and a 10 T / 5 T machine adds +6.1 / +32.0 $/MWh at the tier-3
minimum.

## Coherence constraints (enforced, not advisory)

Six physics couplings are enforced on every quoted point (five checked
by `study.coherence_violations`, the sixth applied by construction in
`study.run`); a stack that violates one is flagged in the output of
every script rather than reported:

1. **f_rad is coupled to the burn mix.** A D-rich plasma radiates more, not
   less: Bosch-Hale + bremsstrahlung at the study calibration (baseline
   f_rad 0.163 at dd_frac 0.314 implies T_i 60-70 keV) gives f_rad about
   0.28 at dd_frac 0.85. `study.f_rad_floor` interpolates the review's
   computed anchors.
2. **Recovery is capped as a composite.** The only published figure on the
   plasma-to-electricity chain (APS DPP24: "optimal burn cycles exceeding
   90% recovery") speaks to the product eta_dec x f_pdv. Tier 2 keeps
   engineering margin (composite <= 0.80); tier 3 takes the theory optimum
   (0.90) with zero margin.
3. **The wall must survive the shot.** Steady flux within the bought
   first-wall class limit (panel 2, hhf 10 MW/m^2), and per-shot flash
   energy under the tungsten millisecond-melt bound (1.5 MJ/m^2, no
   margin).
4. **The D-rich fuel credit travels with its consequences.** Above
   dd_frac 0.5 the machine is a bulk tritium facility: the tier-2 machine
   carries 248 MW of plant-level neutron power and breeds about 95 kg of
   tritium per year, and Helion's own store-for-decay fuel cycle implies an
   equilibrium getter-bed inventory of production rate x mean decay time,
   about 1.7 tonnes of tritium on site. For scale: that inventory is
   1.6e10 Ci, dissipates about 550 kW of continuous decay heat in the
   store, is roughly 420x ITER's 4 kg site limit and about 60x the world's
   civilian tritium stock (about 25-30 kg, CANDU-derived). `study.run`
   charges a tritium-plant adder on C220500, unit-priced rather than
   anchored: 50 M$ fixed core plus 0.657 M$ per MW of plant neutron
   power (a stated definition; the 100-300 M$ reconciliation band at
   reference scale brackets it, and given the tonne-class inventory the
   allowance is more likely low than high). The tier-2 rung's 213 M$ is
   a consequence of its throughput, not an identity. O&M stays at
   the baseline 27.5, never at an "aneutronic" discount.
5. **dhe3_f_T is floored by the burnup closure.** The per-pulse D burnup
   pins the thermalized in-pulse tritium burn (f_T = 1 - (1 - e^-x)/x,
   x = (sv_DT/sv_DD)(-ln(1 - f_D))); any point whose dhe3_f_T sits more
   than 1% below that floor is flagged as coherent only under prompt
   MeV-triton loss. At the patent basis the floor is 0.002, so the
   design's dhe3_f_T = 0 passes; the constraint exists to catch any
   future high-burnup configuration that keeps the zero silently.
6. **f_pdv is derived, never asserted.** Each point's recovery fraction
   is min(claim, share x [1 - (V_i/V_f)^(2/3)]) with V_i the compressed
   flux volume at the 22 T basis field (E_del/(B^2/2mu0), about
   0.26 m^3 at 50 MJ), V_f its own chamber, and share the radial
   fraction of the boundary work: 0.8 from tier 1 (the free-expansion
   adiabatic partition, per the Spencer 1983 scalings the vendor's own
   talk invokes for the radial-axial coupling; no source asserts
   recovery of the axial work), 1.0
   at tier 3 (by axial capture with switched end circuits, or by axial
   suppression with static end-field shaping, which the published
   symmetric geometry's high-field end sections make
   architecture-consistent though unquantified) and at the unchallenged
   vendor baseline. The enforced expression is the Otto/Atkinson-form
   adiabatic-stroke bound at gamma = 5/3; the machine's actual cycle is
   Diesel-type (constant-pressure burn at the beta = 1 force balance)
   with an Atkinson over-expansion, the same generalized Diesel/Otto
   framework with axial and radial expansion that the vendor's cited
   burn-cycle analysis (Kirtley, APS DPP24) uses, and the Diesel-form
   ideal value sits 1-2 percentage points below the enforced cap at the
   study's ratios, so the cap is strict and slightly generous. There is
   no Carnot exemption: cycle form, ratios, and merging entropy set the
   efficiency, which is what the composite cap encodes. Recovery cannot
   be claimed independently of the
   geometry that must deliver it. The 4/5 radial share is the FRC's own
   adiabatic partition (r_s ~ B^-2/5 against l_s ~ B^-1/5), not a
   design choice: the expanding plasmoid does most of its work against
   the field radially without help. The same scalings say elongation
   falls as B^(1/5) during expansion, so nothing maintains aspect
   ratio; the plasmoid grows more oblate as it expands, and since tilt
   stability prefers prolate FRCs, the late expansion trades toward the
   tilt boundary, an unmodeled truncation risk on f_pdv that the
   composite cap's engineering margin partially absorbs at tier 2 and
   tier 3's zero margin does not.

The store-and-decay idealization itself (dhe3_f_T = 0: no bred triton
burns in-plasma) is checked in `scripts/tritium_burn.py`. A triton born
mid-pulse burns before the pulse ends with probability
(1/2) n_D <sigma v>_DT tau, and because D-T reactivity is 27-87x D-D at
70-20 keV (each unit of D burnup burns 14-43x as much bred tritium), each percent of per-shot D burnup burns 14-43% of the bred
tritium in-plasma; the fuel cycle is only self-consistent with low
per-shot burnup bought back by rep rate. At Helion's stated
sub-millisecond dwell (helionenergy.com/faq) and Trenta-class densities
(1e22-3e22 m^-3) the burn fraction stays below about 1% and dhe3_f_T = 0
is a good approximation; at reactor-class compression (1e23 m^-3) with
millisecond-plus dwell it reaches 4-13%. Priced at dhe3_f_T = 0.04 the
tier-2 rung moves only +0.3 $/MWh, but plant neutron power rises 23% and
each burned triton emits a 14.1 MeV neutron (5.8x the D-D neutron
energy), so the LCOE story is insensitive while the shielding basis and
wall spectrum are not.

The model's own `burn_fraction` closes the same loop with no density or
dwell input: the per-shot D burnup pins the integrated exposure
n_D <sigma v> tau, so f_T = 1 - (1 - e^-x)/x with
x = (sv_DT/sv_DD)(-ln(1 - f_D)). At the concept YAML's burn_fraction
0.15 (an unsourced MIF-literature midpoint; the vendor publishes Q, not
burnup) the implied in-pulse tritium burn is **78-93%** across 70-20 keV
if tritons thermalize and stay confined - inconsistent with
dhe3_f_T = 0. The inconsistency is internal to the study's assumption
pair, not an inference about the vendor's machine; it partitions the
operating space into three regimes, each priced, none free: (a) per-shot burnup at or below
about 7e-4, which multiplies the CAS80 recycle-loss line 15x at
fuel_recovery 0.99 (2.4x at 0.999), collapses the bred-He-3 recycle
credit (f_He3_eff 0.95 -> 0.05-0.3), and inflates the vacuum-pumping
throughput the same knob sizes by two orders; (b) prompt loss of the
1 MeV tritons from the small-s plasmoid before they thermalize, a
fast-ion confinement question measurable on Polaris, which also moves
about 1 MeV per T branch from recoverable to undirected; (c) accept the
burn: priced at dhe3_f_T = 0.78 the tier-2 rung is 49.1 and the tier-3
minimum 19.0, plant neutron power rises about 5x with a dominant
14.1 MeV component, and the decay store shrinks to about 0.2-0.3 t - and
those LCOE figures are floors, because the wall/shield audit checks
surface heat only, not the D-T-class neutron loading it would imply.

**The fuel-cycle basis and its patent source.** The vendor's fuel-cycle
patent (published as US 2017/0011811, granted as US 11,469,003 B2)
publishes an operating table (n_D = 0.75e22 m^-3, T = 70 keV,
tau = 0.157 s without tritium removal / 0.103 s with it) and states
tritium "may be removed between each pulse ... prior to undesired D-T
reactions taking place". Under the closure at 70 keV: D burn per
confinement period 2.5-3.8%, thermalized triton burn over that period
28-38% (the patent's own case for inter-pulse removal); per
sub-millisecond pulse at the patent density, burnup 1.2-2.5e-4 and
in-pulse tritium burn 0.2-0.3%, consistent with dhe3_f_T = 0. The
model basis carries the per-pulse pair (burn_fraction 1.2e-4,
burn_fraction_he3 4.1e-4, species-resolved recycle losses,
fuel_recovery 0.9999), under which fuel resides for of order a
thousand pulses and the load-bearing claims are four-nines per-pulse
recovery and hertz-rate isotope separation (unburned-fuel multiplier
84x / 9.3x / 1.8x at two / three / four nines). Grade: published
design intent; the reactor-point compression density may exceed the
patent value, which would move the machine right along the burnup
axis.

**Patents as sources.** A patent, granted or not, is evidence of design
intent, not of working physics: prophetic operating tables are legally
permitted, and grant examination tests claim novelty and formal
enablement, not whether the physics closes. This ledger therefore uses
patent numbers only in the design-basis rung and in tier-2
extrapolations accompanied by a physical argument, never as records:
the same discipline already applied to the recovery-circuit patent's
"up to 90% and higher" band (demoted as prophetic under eta_dec). The
fuel-cycle table carries its own proof of prophecy: its tau column
implies n tau of 2-3e21 s/m^3 at 70 keV, three to four orders beyond
any demonstrated FRC confinement, and the study accordingly uses the
table's density and temperature (whose field companion, B = 22 T,
follows from pressure balance and is corroborated in class by the
vendor's stated >15 T compression hardware) but never its confinement
time.

`scripts/burnup_scan.py` prices the whole axis coherently: both
species' per-pass burn fractions derive from the same n tau, so
burn_fraction_he3 scales with burn_fraction at the fixed 70 keV
reactivity ratio (3.3x), with dhe3_f_T tied to the closure
(thermalized branch) or held at zero (prompt-loss branch), at
fuel_recovery 0.99, 0.999, and 0.9999. At the patent-density basis the
recovery nines carry everything: 17.0 $/MWh at fr 0.9999, 27.5 at
0.999, 148 at 0.99 (the fourth nine is worth 10 $/MWh, the third
120 $/MWh). Toward higher compression density the recovery
requirement relaxes: above per-pulse burnup of about 3e-3 the three-
and four-nines curves converge near 15.5-16.0 $/MWh prompt-loss, and
the axis minimum (15.5 at burnup 1e-2 to 3e-1) sits about 1.5 $/MWh
below the basis, while the thermalized branch turns up past burnup
0.01 as the tritium burn grows: the triton-fate question reopens
exactly where the recovery question closes. Per-pulse exhaust pumping
peaks at the basis (79 M$ per module at the floor).

The scan also reprices neutron damage, which the base model cannot see
(core_lifetime is inert for this concept): replacement of the exposed
package is levelized from the 14-MeV-equivalent neutron wall load
(10 dpa per MW yr/m^2 in Fe-based structure, 2.45 MeV D-D flux folded
at 0.4) at two tolerances, 20 dpa (demonstrated RAFM database edge) and
50 dpa (DEMO design target). The event is C220101 + C220103: the coil
bore sits 0.10 m behind the wall with no blanket, so the close-coupled
copper coils see the same fluence and are replaced with the wall (they
are the cheap part: 14 vs 106 M$ at the tier-3 minimum under the adiabat coil pricing; ceramic
insulation is a prerequisite, since organics die at 1e9 rad in weeks at
these fluxes). At the patent basis the spectrum is pure 2.45 MeV D-D at
a 14-MeV-equivalent load of 0.20 MW/m^2 and the adder is modest
(+0.3-1.2 $/MWh at 50-20 dpa, replacement intervals 10-26 years). The
8-17 $/MWh triton-fate spread survives only as the high-burnup
counterfactual (reactor-point density well above the patent value with
thermalized tritons), where the tier-2 rung's hhf wall makes
replacement brutal (+53 to +161 $/MWh). Two couplings the damage
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
coils + vessel shell, 155 of about 370 M$ per-module reactor hardware
at the tier-3 minimum) crosses from maintenance into machine-
replacement when the wall-and-coil event (120 M$) recurs faster than
event / (CRF x module hardware), about 8 years: under that, the
reactor line is replacement-dominated and the machine is opex. At the
patent basis (D-D spectrum) the interval is 10-26 years at 20-50 dpa,
a capital asset though near the line at the RAFM database edge; the
consumable core (1-3 yr intervals, half the module's value swapped
near-annually) is the high-burnup thermalized counterfactual. In that regime the honest
design is Helion's factory logic taken to its conclusion: a swappable
irradiated cartridge with hot-spare bays (a single-module 1 GWe plant
cannot hold availability 0.95 through annual month-scale swaps; a
multi-module park can, at roughly one spare module of extra capital), a
refurbishment line, and a few hundred tonnes per year of activated
steel and copper that neither the CAS50 decommissioning provision
(140 M$) nor C220110 remote handling (16 M$) is scoped for. Consumable-
core economics are marginal-manufacturing economics, which is where the
missing fleet-learning term (gap 1 of the alignment note) would finally
bind on something real.

## Tier 1: records and published bounds

| knob | baseline | value | analog class | why it applies | source | grade |
|------|----------|-------|--------------|----------------|--------|-------|
| interest_rate | 0.07 | 0.0425 | Sovereign-backed utility-scale generation with contracted offtake | Same structural argument as the Borealis study: a de-risked NOAK plant with firm long-term offtake can reach the same class of project finance. The licensing leg of the argument is weaker here than the fuel label suggests: at the D-rich burn mix this is a bulk tritium facility (see coherence constraint 4), so "minimal licensing" cannot be claimed alongside the fuel credit. The finance analog survives on the offtake/de-risking argument alone. | Apostoleris et al., Prog. Photovolt. 2021, implied 4.25% WACC from the Dubai MBR3 PPA. | strong |
| inflation_rate | 0.0245 | 0.02 | Developed-economy central-bank targeting | The interest-rate record is only coherent against a credible 2% backdrop. | Federal Reserve longer-run goals statement. | strong |
| construction_time_yr | 6.0 | 2.5 | Large single-block CCGT | Applies more strongly here than to the mirror: the plant is an integer count of factory-built modules, closer to CCGT block construction than to a single large bespoke machine. | Siemens Energy, 1200 MW CCGT block in about 30 months. | strong |
| indirect_fraction | 0.20 | 0.08 | Large industrial/power-plant EPC | Same cost-basis scope as NETL's EPCM line (fraction of total direct cost); 0.08 is the low end of the cited 8-10% band. | US DOE/NETL QGESS. | strong |
| availability | 0.85 | 0.95 | Geothermal baseload, derated for shot-cycled hardware | Geothermal's 97-98% has no analogue for a machine that swaps a multi-thousand-unit capacitor bank every few years (2.7e9 shots fired at the tier-2 point against a 1e9-shot bank). Staggered bank swaps plausibly cost 0.5-1.5%: 0.95 is the defensible figure. DIVERGES from Borealis's 0.98 with this stated technology reason. | US DOE Geothermal FAQs, derated per red-team Finding 9. | moderate |
| fuel_recovery | 0.9999 (vendor basis) | 0.999 | Machine-scale recirculating-wall fuel retention | ANTI-RECORD REVERSION, same pattern as lifetime_yr: the vendor-implied four nines is a concept-viability requirement (the He-3 economy fails without it), which the hard-NOAK rule forbids as a basis value. The per-pulse loss channel is wall retention plus pump slip in a sealed loop; the closest measured analog is JET-ILW gas-balance long-term fuel retention at 0.1-0.3% of injected throughput. The analogy has category gaps in both directions: campaign retention is co-deposition-dominated inventory over many wall recycles, not single-transit loss (per-transit loss could be far lower), and it measures none of the separation slip a per-pulse isotope-processing plant adds (could be far higher); helium behaves differently again. 0.999 is the defensible center of a range spanning at least 0.99-0.9999. The model default carries this value. | JET-ILW gas-balance retention studies (Brezinsek et al.). | analog argument |

**Held at baseline in tier 1:**

| knob | why not moved |
|------|---------------|
| lifetime_yr (30) | 80 years is an *anti-record* on this concept at tier-1 capacitor life: replacement accumulates faster than the capital-recovery benefit. Adopted in tier 3, where cap_shot_lifetime is high enough to invert the sign. The clearest case in the study of a record that does not travel between concepts. |
| c_cap_allin_per_joule (0.5) | Already at the optimistic end of its own documented 0.5-4.0 range; the industry statement is that Hz-rate operation still requires a 5-10x cost reduction. No record below the baseline exists. |
| eta_dec (0.85) | The 0.97 an earlier draft placed here is not tier-1-admissible: it is the top of a patent's prophetic circuit-only band (US 2024/0275198 A1), and Helion's "95% proven" statements trace to no-fusion circuit tests. Moved to tier 2 at 0.90 under the composite cap. |
| cap_shot_lifetime (1e8) | The 1e9 figure is a published NOAK *target* (Pacific Fusion AMPS) resting on a vendor-catalog derating extrapolation, not a life test; the largest rep-rated MJ-class precedent is 1.3e4 shots. Tier-2 material by the study's own convention. |

## Tier 2: labelled extrapolations

| knob | baseline | value | basis | grade |
|------|----------|-------|-------|-------|
| cap_shot_lifetime | 1e8 | 1e9 | Pacific Fusion AMPS sec. 4.1: 100 to 35 kV derating projected to reach about 1e9 shots at about 9x lower energy density; GA Series DE cross-check (3e7-3e9 at 20% reversal). At the tier-2 point the plant fires 2.7e9 shots, so the bank is still replaced about 1.7x (charged to CAS72 by the model); the "1e9 outlives the plant" argument holds only below about 1.1 Hz. | published target |
| fuel_recovery | 0.999 (tier-1 record) | 0.9999 | One nine beyond the JET-ILW retention record: the patent closed fuel cycle (US 2017/0011811) implies four-nines per-pulse recovery for the He-3 economy to close, and the physical argument (saturated walls, helium-dominated exhaust, direct re-injection without full reprocessing) points the right direction. No demonstration at any scale. Ties capacitor life as the largest lever under the tier-2 minimum (+43.9 $/MWh if reverted). | patent-implied extrapolation |
| eta_dec | 0.85 | 0.90 | Bottom of the patent band, circuit-only, no fusion-inclusive measurement. Paired with the derived f_pdv under the composite cap (0.90 x 0.78 = 0.70 <= 0.80 at the tier-2 minimum's chamber). | weak-moderate |
| f_pdv | (derived) | share x expansion bound | Not a record: derived per point under coherence constraint 6 as the chamber's adiabatic expansion bound times the radial work share (0.8 at this tier). The vendor's talk states the radial-axial coupling (Spencer 1983 scaling), not recovery of the axial work; capture is admitted only at tier 3 through the share. | constraint-derived |
| eta_pin | 0.95 | 0.98 | Solid-state pulsed-power wall-plug efficiency; plausible for modern semiconductor switching, no datasheet or Helion statement located. | UNSOURCED |
| max_f_rep | 1.0 | 3.0 | No public Helion statement of a numeric plant rep rate exists (Polaris target about 1/s; Trenta about 1/10 min; the 1-10 Hz band is the concept YAML's roadmap paraphrase). 3 Hz is what the bought wall supports at this tier's recovery parameters; it remains UNSOURCED as a demonstrated cadence (nothing MJ-class has run at 1 Hz continuously). The band top (10 Hz) is tier 3. | UNSOURCED-ROADMAP |
| fw_class | panel | hhf | Machine-design purchase, not a record: divertor-grade monoblock wall (ITER divertor procurement anchor, 2.5 M$/m^2 NOAK, 10 MW/m^2 qualification) over the real 37.7 m^2 cylinder, about 94 M$/module, to make 3 Hz admissible in the concept-YAML chamber. The design-optimized tier-2 minimum instead buys a longer chamber with the cheaper panel wall (see coherent minimum below). | design purchase |
| dhe3_dd_frac | 0.314 | 0.85 | D-rich operation to raise in-situ He-3 breeding (prompt D-D He-3 plus stored-tritium decay) and cut the purchased-fuel line; the concept's own stated direction, but 0.85 is the top of a sweep, not a derived operating point. Adopted only jointly with f_rad 0.28 and the tritium-plant adder (coherence constraints 1 and 4). | UNSOURCED |
| f_rad | 0.163 | 0.28 | Bremsstrahlung-consistent radiated fraction at dd_frac 0.85 under the study calibration; relativistic corrections would raise it another 10-25%. Not an optimistic move: this knob *costs* 3.2 $/MWh against the incoherent alternative, and is the price of the fuel credit. | physics floor |

**Held at baseline in tier 2, harmonized with the Borealis ledger:**
om_cost_dhe3 (27.5: already the lowest documented CCGT fixed-O&M figure;
also required by coherence constraint 4), installation_frac (0.14: no
defensible record on the model's cost basis), f_rad as an independent
mover (withdrawn; it is now a coupled variable, not a knob).

## Tier 3: labelled speculation

No entry has a source; each is the optimistic edge of a stated argument or
an explicit leap. See `config/tier3.yaml` for the per-knob notes.

| knob | value | note |
|------|-------|------|
| max_f_rep | 10 | top of the third-party roadmap band; no duty-cycle analysis supports it |
| cap_shot_lifetime | 1e10 | required for coherence with 10 Hz; no source at any price; jointly heroic with the $/J entry below |
| eta_dec x f_pdv | 0.95 x 0.947 = 0.90 | the theory-optimal composite taken at face value, zero engineering margin; f_pdv 0.947 additionally claims capture of the axial expansion channel (about 1/5 of boundary work), which the tier-2 radial-only bound excludes. The source figure (Kirtley DPP24, 'optimal burn cycles exceeding 90%') is unreproducible: its numerator is independently verified but its input-accounting denominator is defined in neither slide nor talk (docs/sources/kirtley_dpp24_formulas.md) |
| c_cap_allin_per_joule | 0.1 | below the model's own documented range floor; contradicts the derating physics that buys the cap life above |
| u_he3 | 5e5 $/kg | no fleet-scale He-3 market exists at any price. The only observed transactions are gram-to-kilogram scale at 19-22 M$/kg (2024 spot about $2,500/L per Edelgas; Interlune's 2025 DOE and Maybell Quantum agreements priced "at approximately today's commercial market price"; TAE's 2026 Black Moon lunar supply option discloses no price). This entry is 40x below every observed price, and the new entrants (lunar: Interlune, Black Moon; terrestrial: Pulsar Helium) are building toward the high price, not under it. |
| dec_staged_recovery_factor | 0.5 | patent's unquantified "net reduction in cost and size", optimistic edge |
| c_inv_per_kw_net | 50 $/kW | small lever |
| multi_unit_labor_factor | 0.80 | small lever |
| lifetime_yr | 80 | adopted only here, where cap life makes it favourable rather than an anti-record |
| yield_per_shot_mj | solved, not asserted | gain speculation is admitted, but the shot must be survivable in the chamber it is costed in: `coherent_min.py` solves yield and chamber jointly. The optimum is a broad plateau (200-750 MJ in a 45 m x 1.0 m single-module chamber, 2-9 Hz, panel wall at its flux limit). The earlier draft's Q = 40 (2000 MJ) in the 0.5 m x 10 m chamber deposits about 6.7 MJ/m^2 per shot, four times the tungsten flash-melt bound, and is excluded. |

## The coherent minimum, and the $10 question

`scripts/coherent_min.py` searches the design space the machine actually
controls (yield, chamber size, wall class, burn mix) under the coherence
constraints, at each evidence level:

| evidence level | minimum | design at the minimum |
|---|---|---|
| tier 1, 1 GWe | **173.0** | cited shot, D-rich mix with tritium plant, 35 modules of 10 m x 1.5 m at 1 Hz (records-only optimum; the mix freedom every tier gets) |
| tier 2, 1 GWe | **41.0** | cited shot (101.4 MJ), 9 modules at 2.9 Hz, 10 m x 1.5 m chambers, panel wall, D-rich mix with tritium plant |
| tier 3, 1 GWe | **16.8** | 300-750 MJ shots, single module at 3.5 Hz, 30 m x 1.5 m chamber, panel wall |
| tier 3, 3 GWe | **13.5** | 3 modules of the 200 MJ / 30 m design at 9.0 Hz (larger shots trip the wall audit once the integer module count snaps down) |

Chamber length is a design variable, not an evidence-tier entry, the
same category as the wall class: nothing about a longer vessel with
more coil sections requires undemonstrated technology, and the design
search is entitled to choose it. For context, the built envelope is
Trenta 15 m and Polaris 19 m (Orion's length is undisclosed), with
Helion's published geometry symmetric (formation and acceleration at
both ends, merge-compression central, expansion back against the same
compression coils). Every added meter is active pulsed structure (coils ramped each
cycle, switched into the recovery circuit, fatigue-cycled every
shot), and the model now prices it: C220103 integrates the solenoid
ampere-turn identity along the machine's own expansion adiabat, so
conductor grows as L^(1/3) (resolved open item 8). Under that pricing
the design search trades length for radius and the minima are fat
short chambers (10-30 m x 1.5 m), inside or near the built length
envelope. The public
facility imagery also corroborates the cost structure at today's
prices: most of the Polaris building's floor is the pulsed-power farm
(about 2,500 stacked power units) with the fusion machine in a small
corner, which is precisely the picture the tier-3 capacitor $/J and
shot-life entries claim will invert. The public facility imagery also corroborates the
cost structure at today's prices: most of the Polaris building's floor
is the pulsed-power farm (about 2,500 stacked power units), with the
fusion machine and its vault in a small corner, which is precisely the
picture the tier-3 capacitor $/J and shot-life entries claim will
invert.

Reconciliation (`scripts/reconciliation.py`) puts honest bands around
these. The recovery-store/switch replacement gap and the over-sized
recovery store are now inside costingfe (CAS72 replaces the shot-cycled
C220109_cap and C220109_switch with the bank; markup_cap carries
f_pdv (1 - f_rad)) and are priced in every number above. What remains
outside: HVDC-class switch repricing (+1.6 tier 2 / +0.7 tier 3), the
driver-thermalization derate (below), tritium-plant band (+-0.7 /
+-0.5), and a thermal-bottoming basis change (-8.7 / -0.7): tier 2
lands in 27.7-39.0, tier 3 in 14.8-17.2 at 1 GWe.

The driver-thermalization derate closes a disposal channel the physics
path misses: it recovers the entire delivered driver energy at flat
eta_dec (p_dee = eta_dec (p_driver + p_pdv) - p_driver), as if all of
it stayed in field form, but the machine has no auxiliary heating
(merging shock plus compression work ARE the heating, all driver-fed),
so the plasma-thermal share chi can only return through the same
expansion channel as the fusion heat, at f_pdv. chi is not a free
parameter: at peak compression the FRC equilibrium pins it through the
average-beta theorem (<beta> = 1 - x_s^2/2), giving
chi = 1.5 <beta> x_s^2 / (1.5 <beta> x_s^2 + 1 - x_s^2), a function of
the separatrix-to-coil radius ratio alone: x_s 0.5/0.7/0.85 maps to
chi 0.30/0.52/0.71, so fat FRCs are high-chi machines and good FRC
confinement physics pushes the derate up. The extra recirculating loss
eta_dec chi (1 - f_pdv) p_driver is worth +3.3/+5.7/+7.8 $/MWh at the
tier-2 minimum across that x_s span (1310 MW of circulating driver
power, widened by the radial-only f_pdv) and +0.1 at the tier-3
minimum; at the low-Q baseline rung it
would be order +10. The Polaris shot triplet (vacuum / plasma no-burn /
burning) separates eta_dec, chi (1 - f_pdv), and the fusion composite,
so the study's most-wanted measurement delivers chi as a by-product;
until then, published excluded-flux radii (x_s) pin it per shot. The disposal of the FUSION heat is already in the
model: f_rad radiates to the wall, (1 - f_pdv) of the remainder is
dumped undirected at end of pulse, and eta_th = 0 discards the lot,
which is what drives the wall-flux audit and the bottoming credit.
The expansion bound and the axial channel are enforced as coherence
constraint 6 (f_pdv derived per point from the chamber's expansion
ratio times the radial share): the tier-2 minimum's 30 m chamber
delivers 0.75, the tier-3 minimum's 60 m chamber supports the claimed
0.947 only because the axial channel is granted there, and the
tier-2 to tier-3 recovery step is exactly the axial-capture claim,
resolvable by the Polaris shot triplet. Parallel particle streaming
through the exhaust is captured by nothing at any tier.

**The observed He-3 market makes the fuel accounting first-order.** At the
observed 19-22 M$/kg spot (he3_scan's 2e7 row) the tier-2 minimum
machine reads 150 $/MWh at dd_frac 0.85 and 380 $/MWh lean: no mix
survives market-priced He-3. That reading follows from the model's fuel accounting: prompt bred
He-3 is credited through its species-resolved cumulative recycle
fraction (0.80 at the per-pulse basis: He-3 burns out of the loop 3.3x
faster per pass than it leaks), but the decay store's He-3 return,
0.42 atoms per primary event and equal to the prompt branch, is never
netted against the purchased 1 - dd_frac per event. Without the decay
return the machine imports about 45 kg/yr; crediting it flips the
plant to a net exporter. The u_he3 = 0 row (28.9 $/MWh) is the full
steady-state self-supply limit. The distance between
those two readings, 28.0 vs 151 at the same machine, is the value of an
open accounting question: the study prices the decay store's capital,
inventory, and licensing consequences but does not credit its product,
which is conservative-incoherent in the same sense constraint 4 forbids
optimistic-incoherence. Worth about 8 $/MWh at the study's u_he3 and
80+ at the observed spot; item 6 below.

**The $10/MWh target is not reached by any coherent stack in this study.**
The closest approaches: 13.6 at 3 GWe on full tier-3 speculation, and 10.9
if He-3 is additionally free (u_he3 = 0, `scripts/he3_scan.py` footer),
one more speculation than tier 3
already carries - and even that no longer breaks 10 once the tritium plant
scales with the throughput that breeds the He-3. What carries the floor at
the tier-3 minimum is no longer the capacitor bank: it is buildings (CAS21
286 M$), heat rejection and electrical plant (CAS24-26 about 170 M$), CAS50 (196 M$,
of which 140 is the decommissioning provision), fuel handling plus the
tritium plant (about 203 M$), and the first wall of the big chamber
(109 M$). See `docs/writeup.md` for the account-by-account anatomy and the
small-plant-penalty analysis.

## Robustness of the tier-2 coherent minimum

One-at-a-time reversion from the 41.0 point (`scripts/tornado.py`):

| knob reverted | LCOE | delta |
|---|---|---|
| fuel_recovery -> 0.999 (JET-analog) | 84.9 | +43.9 |
| cap_shot_lifetime -> 1e8 | 82.0 | +41.0 |
| dhe3_dd_frac -> 0.314 (with its f_rad) | 56.7 | +15.7 |
| max_f_rep -> 1 Hz | 54.9 | +14.0 |
| eta_dec -> 0.85 | 44.6 | +3.6 |
| f_rad -> 0.163 (incoherent: floor violated) | 37.1 | -3.9 |
| eta_pin -> 0.95 | 42.1 | +1.2 |

The cap-life lever doubled when the CAS72 replacement event was widened
to the full shot-cycled recovery chain (bank + store + switch): at 1e8
shots everything that cycles is replaced about 8 times over plant life.
Four tier-2 entries carry the number: the per-pulse fuel recovery and
the capacitor life co-dominate at +41 to +44 $/MWh each (f_pdv no
longer appears: it is derived per point under constraint 6, not a
knob) (an extrapolated
nine beyond the JET retention record, and a published derating target),
followed by the burn mix and the rep rate (an unsourced sweep endpoint
and an unsourced roadmap band). None is a record. That is the honest
quality of the 41.0 figure.

## Consistency with the Borealis ledger

Both studies price NOAK plants with the same framework, so a knob gets the
same ruling in both unless a physics or technology difference is stated.

| knob | Borealis | Helion | divergence justified by |
|---|---|---|---|
| interest_rate | 0.0425 | 0.0425 | same |
| inflation_rate | 0.02 | 0.02 | same |
| construction_time_yr | 2.5 | 2.5 | same; argument stronger here (factory modules) |
| indirect_fraction | 0.08 | 0.08 | same |
| installation_frac | held 0.14 | held 0.14 | same |
| om_cost | held | held | same; additionally forced here by the tritium facility |
| f_rad_fus / f_rad | held | coupled variable | **stated physics reason**: here f_rad is a function of the burn mix (bremsstrahlung floor), not an independent knob; Borealis's photon fraction is set by its own burn physics and was held |
| availability | 0.98 | 0.95 | **stated technology reason**: shot-cycled capacitor bank replaced about 1.7x over plant life; the geothermal analog has no such outage |
| lifetime_yr | 80 | 30 at tiers 1-2, 80 at tier 3 | **stated technology reason**: capacitor replacement makes 80 yr an anti-record until cap life reaches about 1e10 at the operating rep rate |
| eta_th | 0.53 (combined cycle) | 0 (basis), 0.30 as reconciliation add-back | **stated technology reason**: no thermal conversion path in the machine basis; the rejected-heat stream at tier 2 makes bottoming worth -5 $/MWh, carried as an add-back exactly as Borealis carried its excluded-DEC add-back |
| conductor_cost_rebco | held | not applicable | copper pulsed coils, no HTS |
| fw_class / q_surface_max | hhf / 10 (machine design) | panel or hhf, design-optimized | same treatment: the wall package is machine design, not a record; here the wall is audited in-model against the declared class |
| unsourced first-order inputs | p_input quoted as a range | max_f_rep and yield quoted as a surface (`locus_scan.py`) | same treatment |

## Knobs with no effect

`core_lifetime_dhe3` moves LCOE by exactly zero at every operating point
quoted here. Recorded so it is not mistaken for an untested lever; it is
also why wall replacement had to enter through the coherence constraints
rather than through a lifetime knob the model ignores.

**The compression-field basis and its consistencies.** The coil account
prices all coils at the 22 T basis field (conservative: the expander's
guide coils run far lower), the compressed flux volume behind
constraint 6 and the shield-magnetization argument uses the same
field, and the fuel-cycle burnup follows from its density companion:
one operating point, used consistently. Two consequences are open
items: (a) if the reactor-point field is lower, burnup falls as B^2
and the recovery nines bind harder (the field/density RISK rows in
reconciliation: +6.2 / +32.3 $/MWh at the tier-3 minimum for 10 T /
5 T); (b) the magnetic pressure at 22 T is about 193 MPa, cycled
1e9-1e10 times at the rep rate, at or above copper-alloy gigacycle
fatigue strengths (100-150 MPa): the compression coil's replacement
schedule may be set by mechanical fatigue rather than neutron dpa, a
third member of the shot-cycled replacement family that neither the
damage scan nor CAS72 currently prices.

## What the ledger needs next

1. A measured, fusion-inclusive round-trip recovery efficiency on Polaris,
   separating the circuit factor from the PdV factor. It gates the
   composite-recovery entries directly and, through the wall-load budget,
   the honest rep-rate ceiling. Every other open item moves single $/MWh;
   this one moves tens.
2. A duty-cycle analysis for any rep rate above about 1 Hz: switch and
   capacitor cycle life, vacuum recovery at 100-300 ms periods, coil and
   chamber thermal management.
3. A sourced capacitor cost-at-life curve, replacing the single AMPS
   target point and resolving the c_cap / cap_shot_lifetime joint
   optimism the tier-3 stack currently carries.
4. A costed tritium plant scope for the D-rich fuel cycle (the 100-300 M$
   band here is an allowance, not an estimate), including its licensing
   posture.
5. A measured per-pulse burnup and extraction cycle for the
   reactor-scale machine. The vendor's patent (US 2017/0011811) settles
   the design intent: low per-pulse burnup (about 1e-4 at its published
   density) with inter-pulse tritium removal, which validates
   dhe3_f_T = 0 and exposes the study's burn_fraction 0.15 as a
   cumulative single-pass figure misapplied as per-pulse exposure. What
   remains unmeasured: the reactor-point compression density (higher
   density moves the machine right along the burnup axis and revives
   the in-pulse burn), the demonstrated per-pulse isotope-separation
   rate, and the per-pass fuel recovery, four nines of which are
   required at the published point. The same knob set sizes the vacuum
   pumping, the fuel recycle loss, and the bred-He-3 credit
   (`scripts/tritium_burn.py`, `scripts/burnup_scan.py`).
6. A resolved steady-state He-3 balance in the fuel account: whether
   NOAK operation may net the decay store's He-3 return against primary
   D-He3 burn (costingfe credits prompt bred He-3 via the recycle
   fraction but charges 1 - dd_frac purchased He-3 per event with no
   decay return). At the study's u_he3 this is an 8 $/MWh question; at
   the observed 19-22 M$/kg spot it decides whether the concept works at
   all outside full self-sufficiency. Coupled to item 5: the decay
   return only exists if the tritium survives the pulse.
7. The compression-field point: a stated reactor-point field (the
   basis is the patent's 22 T; each halving of B quarters the per-pulse
   burnup and tightens the recovery-nines requirement), and a fatigue
   basis for the compression coil at that field (193 MPa magnetic
   pressure cycled 1e9-1e10 times sits at or above copper-alloy
   gigacycle fatigue strengths; the coil may be schedule-limited by
   mechanics, not neutrons).
8. RESOLVED in-model: PULSED_FRC coils are now priced along the
   machine's own expansion adiabat (B(z) = b_center (z_c/z)^(2/3) in
   the uniform cylinder, integrated with the solenoid ampere-turn
   identity; conductor grows as L^(1/3)), so chamber length is active
   structure with a physics-derived cost and no coil architecture is
   assumed beyond the cylinder the geometry already declares. The
   integral is a floor: formation and acceleration duty on the same
   coils, and per-section recovery switching, are not added. The
   design search responded by trading length for radius (the minima
   are now fat short chambers).
