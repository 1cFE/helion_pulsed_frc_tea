# Evidence ledger

Every non-baseline value adopted in the ladder, with the analog class named
and the reason it applies. Tiers follow the Borealis convention: tier 1 is a
citable record or published bound, tier 2 a labelled extrapolation from a
stated roadmap or physical argument, tier 3 labelled speculation with no
source. "Held at baseline" is the recorded outcome when no defensible value
exists.

Orientation: the machine is a pulsed D-He3 FRC with inductive DEC and no
turbine, 1 GWe as an integer count of Helion-class modules; design basis in
`config/baseline.yaml`, capacitor and pulsed-power evidence in
`docs/capacitor_technology_report.md`, adversarial findings in
`docs/red_team_review.md` (all of whose verdicts are folded into the tier
composition below), narrative answer in `docs/writeup.md`.

All numbers at costingfe `ac2d1a8` (cylinder geometry + wall-flux audit
for linear pulsed concepts; shot-cycled CAS72 replacement scope;
physics-consistent recovery-store markup), pinned by the regression tests
in `tests/test_study.py`. The tier stacks are `config/best_case.yaml`,
`config/tier2.yaml`, `config/tier3.yaml`; `scripts/tiers.py` reproduces the
ladder end to end.

Ladder at 1 GWe / 3 GWe (config stacks, concept-YAML chamber):

| rung | 1 GWe | 3 GWe |
|---|---|---|
| design baseline (Helion's implied point) | 133.3 | 129.8 |
| tier 1 records | 104.5 | 100.9 |
| tier 2 extrapolations | 38.6 | 35.3 |
| tier 3 speculation | 16.6 | 13.2 |

Design-optimized coherent minima (chamber, wall class, and burn mix chosen
by `scripts/coherent_min.py` under the physics-consistency constraints in
`scripts/study.py`): **tier 2: 33.9** at 1 GWe; **tier 3: 15.8** at 1 GWe,
**12.4** at 3 GWe. Reconciliation bands around the minima (model gaps and
conservatisms, `scripts/reconciliation.py`): tier 2 within 27.7-38.9, tier 3
within 14.8-17.2 at 1 GWe.

## Coherence constraints (enforced, not advisory)

Four physics couplings from the red-team review are enforced on every
quoted point by `study.coherence_violations`; a stack that violates one is
flagged in the output of every script rather than reported:

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
   carries 185 MW of plant-level neutron power and breeds about 71 kg of
   tritium per year, and Helion's own store-for-decay fuel cycle implies an
   equilibrium getter-bed inventory of production rate x mean decay time,
   about 1.3 tonnes of tritium on site. For scale: that inventory is
   1.2e10 Ci, dissipates about 410 kW of continuous decay heat in the
   store, is roughly 300x ITER's 4 kg site limit and about 45x the world's
   civilian tritium stock (about 25-30 kg, CANDU-derived). `study.run`
   charges a tritium-plant adder on C220500: 50 M$ fixed core plus a
   throughput-scaled balance anchored at 200 M$ for the tier-2 reference
   machine (band 100-300 swept in reconciliation; given the tonne-class
   inventory, the allowance is more likely low than high). O&M stays at
   the baseline 27.5, never at an "aneutronic" discount.

The store-and-decay idealization itself (dhe3_f_T = 0: no bred triton
burns in-plasma) is checked in `scripts/tritium_burn.py`. A triton born
mid-pulse burns before the pulse ends with probability
(1/2) n_D <sigma v>_DT tau, and because D-T reactivity is 14-43x D-D at
20-70 keV, each percent of per-shot D burnup burns 14-43% of the bred
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
if tritons thermalize and stay confined - flatly inconsistent with
dhe3_f_T = 0. Three ways out, none free: (a) per-shot burnup at or below
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

`scripts/burnup_scan.py` prices the whole axis: burn_fraction swept from
3e-4 to 0.3 with dhe3_f_T tied to the closure (thermalized branch) or
held at zero (prompt-loss branch), at fuel_recovery 0.99 and 0.999. At
the tier-3 minimum the headline 15.8 exists only at the high-burnup
prompt-loss corner. If tritons thermalize, the coherent optimum shifts
to partial burnup (0.01-0.03); the store-purist corner (f_T at or
below 1%, burnup at or below 1e-3) costs 19.8 even at fuel_recovery
0.999 and 63.0 at 0.99. fuel_recovery 0.999 is load-bearing everywhere
below burnup 0.01. Vacuum pumping never binds (at most 35 M$ across the
axis); the fuel recycle loss is the penalty that explodes at low burnup.

The scan also reprices neutron damage, which the base model cannot see
(core_lifetime is inert for this concept): replacement of the exposed
package is levelized from the 14-MeV-equivalent neutron wall load
(10 dpa per MW yr/m^2 in Fe-based structure, 2.45 MeV D-D flux folded
at 0.4) at two tolerances, 20 dpa (demonstrated RAFM database edge) and
50 dpa (DEMO design target). The event is C220101 + C220103: the coil
bore sits 0.10 m behind the wall with no blanket, so the close-coupled
copper coils see the same fluence and are replaced with the wall (they
are the cheap part: 17 vs 109 M$ at the tier-3 minimum; ceramic
insulation is a prerequisite, since organics die at 1e9 rad in weeks at
these fluxes). All-in at the tier-3 minimum: prompt-loss 16.1-16.8
versus thermalized 24.5-33.3 at the declared burnup 0.15, so **keeping
the tritium from burning is worth 8-17 $/MWh at the floor**;
re-optimizing burnup on the thermalized branch (damage-aware optimum
near 0.03) narrows it to about 5-9 at fuel_recovery 0.99 and 2-5 at
0.999. Two couplings the damage column exposes: low burnup raises
neutron damage as well as fuel cost (the dying recycle credit forces
more D-D events per MWh), and the tier-2 rung's hhf wall makes
high-f_T replacement brutal (+45 to +122 $/MWh).

**Why the blanket escape is closed for the compression section.** A
pulsed inductive machine pays per pulse for every cubic meter of flux
volume between coil and plasma: W = (B^2 / 2 mu0) x annulus volume,
recovered only at the composite efficiency. The 50 MJ driver at 10 T
implies about 1.2 m^3 of compression-section flux volume (bore around
0.3 m); a 0.4 m shield under the compression coil multiplies the swept
annulus about 5x, so the store grows to roughly 270 MJ/pulse
(C220107 and its CAS72 schedule scale with it), and the extra
220 MJ/pulse cycled at composite 0.90 dissipates about 20 MJ/pulse:
order 100 MW of recirculating loss at the tier-3 rep rate, and more
than the module's output at the tier-2 composite 0.765. Eddy screening
is the lesser problem (steel skin depth is about 16 mm at ms rise
times, so structure must be laminated; FLiBe at 200 S/m is
magnetically transparent); the irreducible cost is the magnetized
volume itself. A shield is energetically cheap only around the
low-field expansion chamber (W scales as B^2: MJ-class per pulse at
0.5 T and below). The emerging neutron architecture is therefore
sacrificial ceramic-insulated throat coils on the wall-replacement
schedule plus a shielded expander, and it sharpens the tritium
argument: the unshieldable throat is exactly where a 14 MeV spectrum
hurts most. Honesty note the other way: the scan spreads neutrons
uniformly over the cylinder, but the burn is localized near the
compression section, whose wall and coils see several times the
average load on 15-20% of the event value; a localized audit would
raise the damage adders by very roughly 2x. Together with the
fission-spectrum 20 dpa edge and the 10x helium-per-dpa of 14 MeV
neutrons, the adders are more likely low than high.

**When replacement becomes rebuilding.** The exposed package (wall +
coils + vessel shell, 159 of 294 M$ per-module reactor hardware at the
tier-3 minimum) crosses from maintenance into machine-replacement when
its interval falls below event / (CRF x module hardware), about 12
years: under that, the reactor line is replacement-dominated and the
machine is opex. Prompt-loss at 50 dpa (28 yr interval) is a capital
asset; prompt-loss at 20 dpa (11 yr) sits on the line; thermalized at
the declared burnup (1.1-2.6 yr) is a consumable core, with 54% of
module value swapped roughly annually, outspending the module's own
capital service by an order of magnitude. In that regime the honest
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
| eta_dec | 0.85 | 0.90 | Bottom of the patent band, circuit-only, no fusion-inclusive measurement. Paired with f_pdv under the composite cap (0.90 x 0.85 = 0.765 <= 0.80). | weak-moderate |
| f_pdv | 0.80 | 0.85 | Consistent with an about 18x adiabatic volume expansion, 1 - (V0/V1)^(2/3); leaves margin for incomplete fusion-product thermalization (14.7 MeV proton slowing time is ms-class at these conditions) and expansion-phase transport. | argued |
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
| eta_dec x f_pdv | 0.95 x 0.947 = 0.90 | the theory-optimal composite taken at face value, zero engineering margin |
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
| tier 2, 1 GWe | **33.9** | cited shot (101.4 MJ), 8 modules at 2.9 Hz, 20 m x 0.5 m chambers, panel wall at 1.8 MW/m^2, D-rich mix with tritium plant |
| tier 3, 1 GWe | **15.8** | 300 MJ shots (Q about 6), single module at 5.9 Hz, 45 m x 1.0 m chamber, panel wall at 1.9 MW/m^2 (a 200-750 MJ plateau ties within 0.1) |
| tier 3, 3 GWe | **12.4** | 3 modules of the 200 MJ / 45 m design at 8.9 Hz (larger shots trip the wall audit once the integer module count snaps down) |

Reconciliation (`scripts/reconciliation.py`) puts honest bands around
these. The recovery-store/switch replacement gap and the over-sized
recovery store are now inside costingfe (CAS72 replaces the shot-cycled
C220109_cap and C220109_switch with the bank; markup_cap carries
f_pdv (1 - f_rad)) and are priced in every number above. What remains
outside: HVDC-class switch repricing (+1.6 tier 2 / +0.7 tier 3), the
driver-thermalization derate (below), tritium-plant band (+-0.7 /
+-0.5), and a thermal-bottoming basis change (-5.5 / -0.5): tier 2
lands in 27.7-38.9, tier 3 in 14.8-17.2 at 1 GWe.

The driver-thermalization derate closes a disposal channel the physics
path misses: it recovers the entire delivered driver energy at flat
eta_dec (p_dee = eta_dec (p_driver + p_pdv) - p_driver), as if all of
it stayed in field form, but in merging-compression the plasma-thermal
share chi (merging kinetic energy is the heating, plus compression
work; about half at beta of order 1) can only return through the same
expansion channel as the fusion heat, at f_pdv. The extra recirculating
loss eta_dec chi (1 - f_pdv) p_driver is worth +1.6/+2.6/+3.7 $/MWh at
the tier-2 minimum for chi 0.3/0.5/0.7 (1160 MW of circulating driver
power) and +0.1 at the tier-3 minimum; at the low-Q baseline rung it
would be order +10. The disposal of the FUSION heat is already in the
model: f_rad radiates to the wall, (1 - f_pdv) of the remainder is
dumped undirected at end of pulse, and eta_th = 0 discards the lot,
which is what drives the wall-flux audit and the bottoming credit.
Related geometric check: adiabatic expansion caps the recoverable
fraction at 1 - (V_i/V_f)^(2/3), so f_pdv is chamber-coupled: the
tier-2 minimum's 20 m chamber supports about 0.82 against the claimed
0.85, and the tier-3 45 m chamber about 0.96 against 0.947, both at
the edge; the big chamber buys expansion ratio, not just wall area.

**The observed He-3 market makes the fuel accounting first-order.** At the
observed 19-22 M$/kg spot (he3_scan's 2e7 row) the tier-2 minimum machine
reads 110 $/MWh at dd_frac 0.85 and 293 lean: no mix survives market-priced
He-3. That reading follows from the model's fuel accounting: prompt bred He-3
is credited nearly fully (cumulative recycle fraction
bf / (1 - fr (1 - bf)) = 0.95 at the concept's burn/recovery pair), but
the decay store's He-3 return, 0.42 atoms per primary event and equal to
the prompt branch, is never netted against the purchased
1 - dd_frac per event. The plant burns 0.55 He-3 per primary event
against 0.42 prompt bred, so without the decay return it imports about
35 kg/yr; crediting the return flips it to a net exporter. The
u_he3 = 0 row (25.5) is the full steady-state self-supply limit. The distance between
those two readings, 25.5 vs 110 at the same machine, is the value of an
open accounting question: the study prices the decay store's capital,
inventory, and licensing consequences but does not credit its product,
which is conservative-incoherent in the same sense constraint 4 forbids
optimistic-incoherence. Worth about 8 $/MWh at the study's u_he3 and
80+ at the observed spot; item 6 below.

**The $10/MWh target is not reached by any coherent stack in this study.**
The closest approaches: 12.4 at 3 GWe on full tier-3 speculation, and 10.4
if He-3 is additionally free (u_he3 = 0, `scripts/he3_scan.py` footer),
one more speculation than tier 3
already carries - and even that no longer breaks 10 once the tritium plant
scales with the throughput that breeds the He-3. What carries the floor at
the tier-3 minimum is no longer the capacitor bank: it is buildings (CAS21
286 M$), heat rejection and BOP (CAS24-26 about 170 M$), CAS50 (196 M$,
of which 140 is the decommissioning provision), fuel handling plus the
tritium plant (about 203 M$), and the first wall of the big chamber
(109 M$). See `docs/writeup.md` for the account-by-account anatomy and the
small-plant-penalty analysis.

## Robustness of the tier-2 coherent minimum

One-at-a-time reversion from the 33.9 point (`scripts/tornado.py`):

| knob reverted | LCOE | delta |
|---|---|---|
| cap_shot_lifetime -> 1e8 | 73.2 | +39.2 |
| dhe3_dd_frac -> 0.314 (with its f_rad) | 46.8 | +12.9 |
| max_f_rep -> 1 Hz | 45.4 | +11.4 |
| f_rad -> 0.163 (incoherent: floor violated) | 31.0 | -3.0 |
| eta_dec -> 0.85 | 36.6 | +2.7 |
| f_pdv -> 0.80 | 35.8 | +1.9 |
| eta_pin -> 0.95 | 35.8 | +1.9 |

The cap-life lever doubled when the CAS72 replacement event was widened
to the full shot-cycled recovery chain (bank + store + switch): at 1e8
shots everything that cycles is replaced about 8 times over plant life.
The three load-bearing tier-2 entries are the capacitor life, the burn
mix, and the rep rate - respectively a published target, an unsourced
sweep endpoint, and an unsourced roadmap band. None is a record. That is
the honest quality of the 33.9 figure.

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
5. A sourced per-shot burnup fraction and the fast-triton confinement
   physics for the reactor-scale machine. The declared burn_fraction 0.15
   and dhe3_f_T = 0 are mutually inconsistent by an order of magnitude
   (78-93% implied in-pulse T burn in the thermalized limit,
   `scripts/tritium_burn.py`); the same knob sizes the vacuum pumping,
   the fuel recycle loss, and the bred-He-3 credit, so its resolution
   moves four accounts at once. Prompt MeV-triton loss from the small-s
   plasmoid is the one escape that preserves store-and-decay at high
   burnup, and it is measurable on Polaris.
6. A resolved steady-state He-3 balance in the fuel account: whether
   NOAK operation may net the decay store's He-3 return against primary
   D-He3 burn (costingfe credits prompt bred He-3 via the recycle
   fraction but charges 1 - dd_frac purchased He-3 per event with no
   decay return). At the study's u_he3 this is an 8 $/MWh question; at
   the observed 19-22 M$/kg spot it decides whether the concept works at
   all outside full self-sufficiency. Coupled to item 5: the decay
   return only exists if the tritium survives the pulse.
