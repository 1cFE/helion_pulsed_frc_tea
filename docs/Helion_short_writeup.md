# The techno-economic floor of a Helion-class pulsed inductive fusion power plant

*Tal Rubin, Astera Institute*

This work asks how cheap fusion electricity can get if direct energy
conversion is the key technology for harnessing fusion energy. It is one
of six studies, each taking such a thesis to its physically coherent
limit and asking how low the levelized cost of electricity (LCOE) can be
driven.

Direct energy conversion escapes the working-temperature limit of a
conventional working fluid and replaces the turbine island. The fuel
best suited to it is deuterium-helium-3 (D-He3), whose fusion energy is
carried largely by charged particles, and one of the best mechanisms is
inductive recovery: a magnetic field compresses the plasma, which then
expands against that field as the gas in an engine expands against a
piston. That is what Helion Energy is building, and it has stated a
long-run ambition of electricity at 1 cent/kWh ($10/MWh), the figure the
1cFE residency at Astera is set on investigating. This work takes
Helion's published design and results as its starting point.

**The findings, in brief.** Four devices share the architecture and
differ only in the evidence grade of what they are granted: citable
records alone, Helion's own requirements at face value, labeled
extrapolations, and speculation. They read 119.3, 111.0, 26.8 and 10.6
$/MWh at 1 GWe. The speculation park reads 8.4 $/MWh at 3 GWe, so the
target is crossed by that one stack, through a 3% real cost of capital
(14.6 at 7%) and with the wall-and-coil replacement included. Every
number grants Helion's shot, 128 MJ from a 50 MJ bank, which no record
supports and which needs a burn of 0.3 to 0.7 s against Helion's own
stated pulse of hundreds of microseconds to milliseconds; on citable
records alone the machine makes no net power. At the extrapolation
device the largest lever is the capacitor cycle life, worth three times
the next two, the deuterium-rich burn mix and the repetition rate. The
three optimized devices do not burn Helion's mix. Helion's patent point
has He3/D = 0.158, half the fusion events D-D; the design search picks a
deuterium-rich mix with 85% of events D-D at every grade, even carrying
its higher bremsstrahlung fraction, because the He-3 it breeds undercuts
purchased He-3, and reverting the extrapolation device to Helion's mix
costs 12.0 $/MWh. That choice is what makes the fuel cycle, not the
driver, the load-bearing subsystem, with a tonne-class tritium store
intrinsic to He-3 self-supply. The data that would move the ladder are
all Polaris data, first among them the yield of a burning shot at its
measured burn time.

The costing uses the `1costingfe` bottom-up cost model [1]
([code](https://github.com/1cFE/1costingfe),
[documentation](https://files.1cf.energy/1costingfe_paper.pdf)). Section
2 describes the device, Section 3 the four devices and their
constraints, Section 4 their cost, Section 5 the He-3 fuel cycle, and
Section 6 the bound on the yield of a shot and the recovery physics.

## 2. Machine basis

Two field-reversed configuration (FRC) plasmoids are formed in opposed
formation sections, merged in a central compression section, where the
collision converts their directed kinetic energy into ion heat, and
magnetically compressed to burn conditions [2, 3]. The pulsed-power
driver is the only heater. After the burn the plasma expands against the
field, returning driver energy and charged fusion energy to the coil
circuit as work; radiated power, undirected charged power, and neutrons
are not converted.

The design-basis shot is built from three public numbers: the driver
delivers 50 MJ per pulse (the Polaris capacitor bank), the plant fires
at 1 Hz, and Orion, the first plant, is to supply Microsoft at least 50
MWe [2], taken here as one module, the 50 MWe unit Helion's CEO
describes coming off a gigafactory line, one a day, on a truck [4]. The
yield per shot is whatever turns that shot into 50 MWe at 1 Hz at the
burn point Helion's patent discloses (Section 5): 128.1 MJ, a gain of
2.56 over the delivered driver energy, a consistency figure rather than
a disclosed measurement. The chamber radius is 0.61 m, the smallest at
which a 10 m cylinder wall survives the shot under the tungsten flash
bound of 1.5 MJ/m^2 per pulse; the Helion device at 1 GWe is 20 modules.
The public record as of September 2026 is D-T fusion on Polaris with no
published yield or recovered electricity, from a company that has
withdrawn "net electricity" from its own goals [2, 5].

Helion does not report the data a costing needs, and this work fills
each gap by grading it (Section 3): the yield of a burning pulse and its
burn time; the energy recovered with plasma present, measured on seven
prototypes per the FAQ with no figure given; the reactor-point density
and field; the per-pulse separation rate and per-pass fuel recovery; and
the duty cycle of multi-hertz operation. The capacitor cost at cycle
life, the other datum the ladder rests on, is a supplier's, not
Helion's.

## 3. Method

***Notation.** Model parameters keep their configuration-file names.
dd_frac is the D-D share of primary fusion events by count (Helion's mix
0.49, the D-rich mix 0.85); dhe3_f_T the fraction of bred tritium that
burns in-pulse; eta_dec and f_pdv the circuit efficiency of inductive
recovery and the fraction of the plasma's expansion work that reaches
the coils, their product the composite recovery; chi the plasma-thermal
share of the delivered driver energy and x_s the separatrix-to-coil
radius ratio.*

**Evidence ladder.** Held at every grade: constant-dollar framing and
EPCM indirects at 20% of direct cost [6], which the model scales with
the build, so the effective fraction is 16.7% at a 5-year build, 10.8%
at 3.25 years and 8.3% at 2.5 years. Construction time steps 5 years at
the design basis and records grades (the serial Hualong One builds,
about 60 months [7]), 3.25 at extrapolations (the Kashiwazaki-Kariwa
ABWR pair, 37 and 39 months to fuel load [8]) and 2.5 at speculation (a
combined-cycle gas turbine timeline). The cost of capital steps 7% real
at the design basis and records grades (the IEA/NEA central case [9]),
5% at extrapolations, 3% at speculation (the IEA/NEA low case [9]); it
is the one financing entry, kept separate in Figure 1 and the at-7%
column. Book life steps from 30 years through the records grade [10] to
80 years above it (the US DOE hydropower lifespan [11]). Availability is
derived from 0.98 outside planned outages, less a routine outage every
two years [12], a capacitor-bank swap at the bank's shot life, and a
wall-and-coil changeout at the displacement-damage tolerance (20 dpa
through the records grade, 50 above it): 0.893 at the records device,
0.924 at speculation.

Helion makes two unrecorded claims. The records device holds one at its
evidence-supported value, per-pulse fuel recovery 0.999 (the
fuel-retention analogy to JET [13]); the other, the shot, has no
evidence-supported value above zero, so on evidence alone the records
device makes no net power, and it is priced at Helion's shot only so
that a machine exists to cost. The Helion device grants Helion's 0.9999
(four nines) and the shot; the extrapolation and speculation stacks keep
that grant and add the labeled entries listed in Section 4, the largest
being capacitor life 1e9 shots (Pacific Fusion's derating target [14]).
Every entry carries a source and grade in the evidence ledger
(`docs/ledger.md`); no extrapolation entry is a measured record.

**Coherence constraints.** Six couplings are enforced by the scripts on
every quoted point, and a seventh, derived in Section 6, is applied to
every quoted point in this text:

1. The radiated fraction follows the burn mix through a bremsstrahlung
   floor (f_rad = 0.28 at dd_frac 0.85, not Helion's stated 0.05).
2. Recovery is capped as the composite eta_dec x f_pdv (0.80 through
   the extrapolation grade, 0.90 at speculation), because the only
   published figure speaks to the product.
3. The wall must survive its steady flux within the purchased class (a
   panel wall of the ITER first-wall kind at about 2 MW/m^2, or a
   divertor-class monoblock at 10 MW/m^2) and its per-shot flash under
   the tungsten millisecond-melt bound.
4. A mix with dd_frac at or above Helion's 0.49 carries its tritium
   plant: 50 M$ fixed plus 0.657 M$ per MW of plant neutron power.
5. dhe3_f_T is floored by the burnup closure of Section 5.2 (floor
   0.002 at the patent basis; the design's zero passes).
6. f_pdv is capped per point at the adiabatic-stroke bound
   1 - (V_i/V_f)^(2/3), V_i the compressed flux volume at 22 T and V_f
   the chamber (Section 6).
7. The shot yield is bounded by the plasma energy and the burn time,
   gain <= chi x burn time / breakeven time, so every quoted point
   carries the burn time its shot implies, and the shot takes each
   device's grade rather than serving as a shared basis.

Each device except Helion's own configuration is the argmin of a scan
over shot yield (free only at speculation), chamber length and radius,
wall class, and burn mix, discarding designs that violate a constraint.
Reconciliation brackets each minimum with the model gaps it cannot price
internally (switch duty, the tritium-plant band, driver thermalization)
and its conservatisms (no thermal bottoming).

## 4. Results: the four devices and what carries the floor

| device | 1 GWe | 3 GWe | at 7% real cost of capital, 1 GWe |
|---|---|---|---|
| citable records | 119.3 | 114.6 | 119.3 |
| Helion's requirements | 111.0 | 106.9 | 111.0 |
| extrapolations | 26.8 | 23.6 | 33.9 |
| speculation | 10.6 | 8.4 | 17.9 |

LCOE in $/MWh. The at-7% column reprices each device at a 7% real cost
of capital with everything else unchanged; the gap is what the grade's
cheaper money is worth, 7.1 $/MWh at extrapolations and 7.2 at
speculation. The stacks:

- **citable records**: fuel recovery 0.999, 7% real cost of capital,
  30-year life, 5-year build, Helion's shot granted; optimum: 25
  panel-wall modules of 10 m x 0.75 m at 1 Hz, D-rich mix with its
  tritium plant
- **Helion's requirements**: Helion's configuration (20 modules in the
  smallest chamber that survives the shot, Helion's mix with its tritium
  plant, 7% real cost of capital, 30-year life, 5-year build) granted
  the shot and fuel recovery 0.9999
- **extrapolations**: records + capacitor life 1e9, a 3 Hz ceiling, a
  purchasable divertor-class wall, fuel recovery 0.9999, 5% real cost of
  capital, 80-year life, 3.25-year build; optimum: seven 10 m x 1.5 m
  panel-wall modules at 2.7 Hz
- **speculation**: extrapolations + 10 Hz, the composite at its theory
  optimum 0.90, capacitors at 0.1 $/J and 1e10 shots, He-3 at 0.5 M$/kg,
  3% real cost of capital, 2.5-year build; optimum: 300-1000 MJ per shot
  from the same 50 MJ driver (500 MJ carried, a 1 to 3 s burn at the
  patent point) in 30 m x 1.5 m chambers

Coil cost grows as the cube root of chamber length while the recoverable
fraction grows with radius squared, so the minima are short, fat
chambers. Reconciliation brackets the extrapolation device within 21.8-31.1 $/MWh and the speculation device within 9.9-11.6 $/MWh at 1
GWe. The D-rich mix is the strict optimum at every grade because it
breeds more He-3 than it burns.

The records device sits 8.3 $/MWh above Helion's requirements on one
claim, Helion's fourth nine of fuel recovery. At Helion's own mix, which
breeds less He-3 than it burns and keeps buying, that claim is worth
about 49 $/MWh (Section 5.2 derives the multiplier); the records device
escapes nearly all of it by running deuterium-rich. Both devices are
dominated by scheduled replacement of the recovery chain, about eight
times over a 30-year life at the 1e8-shot record.

![The evidence ladder](figures/fig1_ladder.svg)

*Figure 1: The four devices at 1 and 3 GWe, each bar split into
overnight cost over the book life (blue), the cost of money (orange),
and O&M, fuel and replacement (grey).*

The extrapolation device changes what is bought, each entry a labeled
step beyond a record with a physical argument behind it; the speculation
device changes prices and ceilings, none with a mechanism behind it.
One-at-a-time reversion from the extrapolation device ranks the levers:

| parameter reverted | LCOE ($/MWh) | delta ($/MWh) |
|---|---|---|
| cap_shot_lifetime -> 1e8 | 63.6 | +36.8 |
| dhe3_dd_frac -> 0.49 (with its f_rad) | 38.8 | +12.0 |
| max_f_rep -> 1 Hz | 38.4 | +11.6 |
| interest_rate -> 0.07 (financing) | 33.9 | +7.1 |
| fuel_recovery -> 0.999 (JET-analog) | 33.2 | +6.4 |
| lifetime_yr -> 30 | 31.3 | +4.5 |
| eta_dec -> 0.85 | 28.7 | +1.9 |
| construction_time_yr -> 5 yr | 28.5 | +1.7 |
| f_rad -> 0.23 (incoherent) | 25.3 | -1.5 |
| eta_pin -> 0.95 (driver wall-plug) | 27.4 | +0.6 |
| wall_dpa_tolerance -> 20 | 27.0 | +0.2 |

The capacitor cycle life dominates; the burn mix and the rep rate follow
at a third of its weight; then the cost of capital, the fourth nine of
fuel recovery, the 80-year book life and the 3.25-year build. f_pdv and
the shot are absent: the extrapolation stack leaves f_pdv at 0.80 under
a cap that does not bind, and the shot's record value is no plant.

![Tornado from the extrapolation device](figures/fig2_tornado.svg)

*Figure 2: One-at-a-time reversion of each extrapolation entry to its
record value. Red bars are favorable reversions; the grey bar is the
financing entry.*

At the speculation device the capacitor-driver narrative is spent: the
bank is 5 M$ of a 666 M$ reactor account, and buildings (286 M$),
decommissioning (199 M$), the tritium plant (190 M$), and heat rejection
and electrical plant (170 M$) each outweigh the 65 M$ of conversion
electronics and 14 M$ of coils.

![What carries the floor](figures/fig3_anatomy.svg)

*Figure 3: Capital accounts carrying the speculation device. The driver
bank is the smallest bar; site infrastructure and the fuel cycle
dominate.*

## 5. The He-3 fuel cycle is the load-bearing subsystem

The fuel cycle is the one in Helion's patent [15], whose operating table
also fixes the burn point: He3/D = 0.158 at 70 keV and 22 T, radiating
23% of its fusion power as bremsstrahlung and releasing 6% as neutrons.
The D-D reactions close the cycle: half produce a He-3 atom directly
(the prompt branch); the other half a triton (the tritium branch),
pumped out with the exhaust after the pulse, separated, and stored until
it decays into He-3 (12.3 yr half-life). Almost none of the tritium
burns before it is removed (dhe3_f_T = 0 in the basis). The plant has no
lithium; its tritium plant is an exhaust-processing and storage plant.

### 5.1 The He-3 balance and the observed market

The tritium branch, half of the D-D events, produces 0.42 tritium nuclei
per primary event at the D-rich mix, and each decays to He-3 on the 17.8
yr mean life of that 12.3 yr half-life. That He-3 is fuel for the
reactor: it replaces purchased He-3 atom for atom, and from an empty
store the replacement builds as 1 - e^(-t/17.8 yr), reaching the full
0.42 per event against the 1 - dd_frac the plant burns only at
equilibrium. This work levelizes the credit over the book life at the
grade's rate; the prompt bred He-3 counts as extra burns, not as supply.
A deuterium-rich plant buys He-3 only until the store covers its need,
about eight years, so its levelized purchase is 16% of the perpetual one
at the extrapolation device and 11% at speculation; Helion's mix keeps
buying, at 82%. Bought in perpetuity at the ledger price, He-3 would
cost the four devices 34, 4.5, 7.1 and 1.4 $/MWh more; free, it would
save them 10.9, 20.3, 1.4 and 0.2, and re-run at zero price the
extrapolation and speculation devices leave the D-rich mix for the
He-3-rich one (dd_frac 0.13) with no tritium plant, at 20.3 and 8.5
$/MWh.

The price matters because no cheap He-3 exists. The DOE Isotope
Program's 2011 allocation was 600 $/L to federal and 1,000 $/L to
commercial users [16], 4.5 and 7.4 M$/kg; the 2024-2026 transactions
(Edelgas spot, the Interlune agreements, TAE's lunar option [17]) sit at
19-22 M$/kg on gram-to-kilogram volumes. The 2 M$/kg this study charges
sits below both, and the speculation entry, 0.5 M$/kg, nine times below
the 2011 allocation. A kilogram of He-3 burned at the floor produces
about $1.8M of electricity but sells for $19-22M today, so an early
breeding plant earns more selling He-3 than burning it.

The store that self-supply implies is large. At the speculation device
the module breeds tritium at half the D-D rate, 0.55 mg per shot and 56
kg/yr. Store-for-decay fixes the equilibrium inventory at production
rate times the 17.8 yr mean life: about 1.4 tonnes of tritium, 1.3e10
Ci, about 450 kW of decay heat, roughly 350x ITER's site authorization
and 50x the world's civilian stock. The inventory is intrinsic to He-3
self-supply at this scale; a central fuel facility relocates it but
cannot shrink it. This is why the ledger refuses the "near-zero
licensing" claim, holds O&M at its baseline, and treats the 200 M$
tritium-plant allowance as more likely low than high.

### 5.2 Fuel recovery and the burnup closure

Helion's cycle depends on pumping the bred tritium out of the exhaust
before it burns, so whether the shot and the fuel plan are compatible is
a question about pulse length, not a modeling choice. The
store-and-decay idealization (dhe3_f_T = 0) is therefore a claim about
pulse kinetics: a triton born mid-pulse sits in a deuterium-rich plasma
at fusion temperature for the rest of the burn, and D-T reactivity is
27-87x D-D at 70-20 keV [18]. The per-pulse deuterium burnup pins the
integrated exposure x_DD = -ln(1 - f_D) = n_D <sigma v>_DD tau, and
averaging over triton births gives the thermalized-limit in-pulse
tritium burn

    f_T = 1 - (1 - e^-x)/x,  x = (sv_DT / sv_DD) x_DD,

whose only physics input is the reactivity ratio. Prompt orbit loss from
the plasmoid, whose separatrix sits only a few ion gyroradii from the
field null, is the one mechanism that can hold the burn below this
floor. This is constraint 5.

The basis is the patent's burn point, n_D = 0.75e22 m^-3 at 70 keV, and
Helion's stated pulse, not the patent's confinement time (0.10 to 0.16
s, three to four orders beyond any demonstrated FRC confinement). Over a
sub-millisecond pulse the burnup is 1.2-2.5e-4 and the in-pulse tritium
burn 0.2-0.3%, so dhe3_f_T = 0 passes with two orders of margin. Figure
4 draws the closure against burn time: at the 0.3 to 0.7 s the
design-basis shot needs under constraint 7, a thermalized triton burns
58 to 80% before removal (88 to 95% at the speculation shot's 1 to 3 s),
so the store-and-decay cycle and the granted shot are coherent together
only under prompt triton loss, the branch the burnup axis of Figure 5
prices at high burnup.

![The burnup closure against burn time](figures/fig4_tritium_burn.svg)

*Figure 4: The burnup closure against burn time at the patent point:
per-pulse deuterium burnup (dashed) and the thermalized-limit in-pulse
burn of a bred triton (solid), with Helion's stated pulse, the patent's
confinement time, and the burns the design-basis and speculation shots
need under constraint 7 marked. The store-and-decay basis holds at the
stated pulse, not at the burn the granted shot needs.*

Fuel therefore resides in the machine of order a thousand pulses before
burning, and a recirculating nucleus burns with probability bf (the
per-pass burn fraction) or leaks with probability 1 - fr (the per-pass
exhaust recovery) each pass, so its ultimate fate is bf / (1 - fr (1 -
bf)):

| species (per-pass burn) | fr = 0.99 | fr = 0.999 | fr = 0.9999 |
|---|---|---|---|
| deuterium (1.2e-4) | 1.2% burns | 11% burns | 55% burns |
| He-3 (4.1e-4) | 3.9% burns | 29% burns | 80% burns |

At four nines 80% of the He-3 burns; at three nines the loop wastes 71%
of it; at two nines nearly everything leaks. A deuterium-rich plant is
self-sufficient in He-3 at three nines, so the fourth nine is worth 6
$/MWh at the extrapolation device; at Helion's mix it is worth 49.

Both species' per-pass burn fractions derive from the same n tau, so the
axis is swept coherently (Figure 5). At the patent burn point the
per-pulse fuel recovery sets the speculation device's cost almost alone:
10.6 $/MWh at four nines, 12.2 at three, 27.0 at two. Above per-pulse
burnup of about 1e-3 the three- and four-nines curves converge near
10.0-10.3 $/MWh on the prompt-loss branch, but the orbit loss that
spares the tritium also removes the fusion protons, about four fifths of
the charged fusion energy at the D-rich mix, so that branch prices the
fuel cycle only. The thermalized branch turns up past burnup 0.01 as the
tritium burn grows (13-90%), so the triton-fate question reopens exactly
where the recovery question closes.

![The burnup axis](figures/fig5_burnup.svg)

*Figure 5: LCOE at the speculation device across the per-pulse burnup
axis under the two triton fates and three exhaust-recovery grades; the
patent-density basis (dotted) is the hardest point for fuel recovery.*

### 5.3 Neutron damage and the unshieldable throat

The replacement rate of the wall, coils, and vessel shell follows from
the D-T-equivalent neutron wall load (10 dpa per MW yr/m^2, the 2.45 MeV
D-D flux folded at 0.4) and a tolerance of 20 dpa (the edge of the RAFM
steel irradiation database) or 50 (the DEMO-class target). At the patent
basis the spectrum is pure D-D at a 14-MeV-equivalent load of 0.20
MW/m^2 and the cost is modest (+0.3-1.2 $/MWh at 50-20 dpa); the
wall-and-coil interval of 10 to 25 years makes the core a capital asset.
The story reopens only in the high-burnup counterfactuals: with
per-pulse burnup toward 0.1 and thermalized tritons the gap against
prompt loss reaches 8-16 $/MWh, and on the extrapolation stack's
divertor-class wall it is prohibitive (+52 to +134 $/MWh), a
consumable-core regime with a waste stream this study does not price.

Shielding cannot buy the machine out of this, because a pulsed inductive
plant pays per pulse for every cubic meter of flux volume between coil
and plasma, W = (B^2/2mu0) x annulus volume, recovered only at the
composite efficiency. The 50 MJ driver at 22 T implies about 0.26 m^3 of
compression-section flux volume; a 0.4 m shield under the compression
coil multiplies the swept annulus by more than an order of magnitude,
which at composite 0.90 is order 100 MW or more of recirculating loss
at the speculation rep rate. The coils nearest the burn are therefore
sacrificial, ceramic-insulated, and on the wall-replacement schedule.

## 6. The yield a shot can return, and what the circuit recovers of it

Every number in this work grants Helion's shot. This section bounds what
a shot can return from the plasma's own energy and burn time, and finds
the design-basis shot incompatible with Helion's stated pulse; it then
sets out the two further bounds on what the circuit recovers, the share
of the driver energy that thermalizes and the expansion ratio the
chamber allows, beyond the composite cap of constraint 2 that stops the
two conversion efficiencies from being counted twice.

**The yield bound.** The plasma at peak compression holds a share chi of
the delivered driver energy E_del (50 MJ per pulse): merging shock and
compression work are the only heating, and chi is fixed by the FRC
equilibrium as a function of the separatrix-to-coil radius ratio alone,
chi(x_s) = 1.5 <beta> x_s^2 / (1.5 <beta> x_s^2 + 1 - x_s^2) with <beta>
= 1 - x_s^2/2 [19]: 0.30, 0.52 and 0.71 at x_s = 0.5, 0.7 and 0.85. That
energy sits at the energy density of a beta = 1 plasma, 1.5 B^2/2mu0,
and burns at the fusion power density of the burn point, so

    gain <= chi x burn time / breakeven time,

with the breakeven time the ratio of those two densities, the fusion
breakeven time of Lackner et al. [20]. At the patent point the
Bosch-Hale breakeven time is 86 ms with thermalized electrons, and 3.7
times shorter if the electrons could be held at a tenth of the ion
temperature; they cannot, since the ion-electron equilibration time at
that density is about 1 ms. Helion's stated pulse is hundreds of
microseconds to milliseconds [2]. Against it the bound reads: a 1 ms
burn returns 0.2 to 0.4 MJ from the 50 MJ bank across x_s 0.5 to 0.85,
less than the circuit loses per shot at any eta_dec in the ladder; the
design-basis 128 MJ shot needs 0.3 to 0.7 s; the speculation shot needs
1 to 3 s. This is constraint 7 and the reason the shot is a graded claim
rather than a shared basis.

**Driver thermalization.** The same chi bounds the recovery of the
driver energy itself: the thermalized share can only return through the
same expansion channel as the fusion heat, at f_pdv, while the model
recovers all of it at the flat inductive efficiency. The uncaptured loss
is worth +1.4 to +3.3 $/MWh at the extrapolation device and order +10 at
the low-gain Helion device; it is carried in the reconciliation bands.

**The expansion-ratio bound.** Constraint 6 caps f_pdv at 1 -
(V_i/V_f)^(2/3), with V_i = E_del/(B^2/2mu0), about 0.26 m^3 at 50 MJ
and 22 T. The extrapolation device's 10 m x 1.5 m chamber caps f_pdv at
0.98, above its claimed 0.80; the speculation device's 30 m x 1.5 m
chamber at 0.989, just above its claimed 0.947.

Two published figures sit against the model's Diesel-type cycle with
Atkinson over-expansion [21]. Nicolas et al. [22], whom Helion's FAQ
cites for recovery "exceeding 95%", give that number only as an ideal
bound. Slough [23] derives 40% as the most an ejected FRC can return in
a flux-conserving expansion chamber, where it comes to rest holding 1.5
pV of thermal energy against the field it has compressed. That is his
own recovery topology, not the discharged compression coil this work's
f_pdv assumes, so it is carried as a risk row rather than a cap: at
f_pdv 0.4 the extrapolation device reads 44.2 $/MWh (+17.4) and the
speculation device 14.8 (+4.2).

**Measurement protocol.** A three-shot sequence on Polaris separates the
chain: a vacuum shot measures eta_dec alone; a plasma no-burn shot
returns eta_dec[(1 - chi) + chi f_pdv], so its deficit against vacuum
measures chi(1 - f_pdv); a burning shot adds the fusion composite, and
its yield reads constraint 7 directly. It is Helion's own stated proof
point: energy returned to a capacitor bank from fusion-driven expansion
"rather than only from ordinary inductive coupling in the circuit"
(Helion FAQ).

## 7. What reaches $10/MWh, and what gets it there

The target is reached only as a park. Two controlled sweeps at the
speculation stack separate module count from plant size. **Module count
at fixed plant size is nearly free**: a park of 500 MWe modules reads
10.1 $/MWh against the single 1 GWe module's 10.6, and even 50 MWe
modules cost only four tenths of a dollar more (11.0), because
buildings, supplementary capital, and balance of plant price plant
totals. **Standalone plant size is expensive**:

| plant | LCOE ($/MWh) | $/kW | dominant penalties |
|---|---|---|---|
| 1 GWe | 10.6 | 1492 | - |
| 250 MWe | 17.5 | 2268 | fixed site buildings, staffing^0.5 |
| 50 MWe | 43.3 | 6342 | O&M 17.2 $/MWh (staffing law), 141 M$ of buildings, tritium-plant fixed core |

The penalty is about 138 M$ of fixed site buildings on fission-class
analogs, the P^0.5 staffing law, and the absence of any fleet-learning
term on equipment, so this concept's economics live in power parks; the
50 MWe module of Helion's gigafactory framing [4] is a manufacturing
choice the model neither rewards nor punishes at park scale.

Within that park, the entry that carries the full speculation stack
across is its financing: the 3 GWe park reads 8.4 $/MWh (10.6 at 1 GWe),
and at a 7% real cost of capital the same machine reads 14.6 $/MWh (17.9 at 1 GWe), so the 3% real cost of capital, sovereign-class money with no
mechanism behind it, is worth more than the whole distance to the
target. The crossing needs the derived availability of 0.92 (at the
model default of 0.85 the park reads 9.0 $/MWh) and Helion's shot
granted. It survives the wall-and-coil replacement: 0.4 $/MWh at 50 dpa
and 1.2 at 20 dpa take the park to 8.8 to 9.6 $/MWh. Three concessions
outside the evidence base would lower it further: free He-3 (1.9 $/MWh
at 3 GWe, moving the design to the He-3-rich mix with no tritium plant),
gas-class site and decommissioning analogs (about 2 $/MWh at 1 GWe), and
a fleet-learning term on equipment.

## 8. Conclusions

Four devices on one architecture read 119.3, 111.0, 26.8 and 10.6 $/MWh
at 1 GWe by evidence grade. Only the speculation park at 3 GWe, 8.4
$/MWh, is under the target, and a 3% real cost of capital rather than
physics takes it there. The floor is carried by site infrastructure and
the fuel cycle, not the driver bank, and at the extrapolation device the
capacitor cycle life is the largest lever, worth three times the burn
mix and the repetition rate.

Every number grants Helion's shot, 128 MJ from a 50 MJ bank, which at
the patent point needs a burn of 0.3 to 0.7 s against Helion's stated
pulse of a millisecond or less; over such a burn most bred tritium fuses
before it can be removed, so the fuel cycle and the shot hold together
only under prompt triton loss. The cheap machine is not the machine
Helion describes: the design search picks a deuterium-rich mix at every
grade because bred He-3 undercuts purchased He-3, and self-supply
implies a tritium store of about 1.4 tonnes and a per-pass fuel recovery
of three nines that no per-pass measurement supports.

The speculation stack is jointly heroic: 0.1 $/J capacitors with
1e10-shot life contradict the derating physics that connects capacitor
cost to life, the composite recovery sits at its theory optimum with
zero margin, and the 500 MJ shot is a burn of seconds. The floor is
conditional on the patent-basis compression field (a 10 T reactor point
adds about 2 $/MWh, a 5 T point about 11) and on the discharged-coil
recovery topology (Slough's 40% ceiling adds 4.2 $/MWh at speculation
and 17.4 at extrapolations); the one conservatism, no thermal bottoming,
is worth -4.3 $/MWh at the extrapolation device.

The constructive reading: the floor, conditional on the shot, is low by
any thermal-plant standard, the architecture of factory modules, park
deployment and swappable cores fits the failure modes the physics
imposes, and the data that would move the ladder from speculation to
evidence, the shot first among them, are Polaris data.

## Reproducibility

Everything here is in the study repository at
[github.com/1cFE/helion_pulsed_frc_tea](https://github.com/1cFE/helion_pulsed_frc_tea):
the four evidence stacks in `config/`, the scripts in `scripts/` that
produce every number and figure, the evidence ledger, the adversarial
review, and the Helion slide and FAQ captures. The cost model is
`1costingfe` at commit 44434d9. Regression tests pin every quoted
device, constraint, and credit. This page is the short form of
`docs/Helion_writeup.md`, which carries the full argument.

## Conflict of interest

Tal Rubin and Damien Scott are co-founders of a proton-boron-11 fusion
startup.

## References

1. Rubin, T. (2026). 1costingfe: a bottom-up fusion power plant cost
   model. Repository at commit `44434d9`.
2. Helion Energy. Technology and FAQ pages (helionenergy.com/technology,
   /faq); the 20 April and 5 June 2026 FAQ captures are archived in
   `docs/sources/`. Microsoft power purchase agreement announcement
   (2023).
3. Kirtley, D., and Milroy, R. (2023). "Fundamental scaling of adiabatic
   compression of field reversed configuration thermonuclear fusion
   plasmas." Journal of Fusion Energy 42, 30.
4. Kirtley, D. (2025). Interview on the Lex Fridman Podcast, episode
   485, 17 November 2025, at 2:17:48.
5. Axios Pro (2026). "Helion hedges on how soon it expects to sell
   electricity from fusion," 8 September 2026.
6. US DOE/NETL. Quality Guidelines for Energy System Studies: EPCM
   indirect-cost basis.
7. World Nuclear News (2025). "Zhangzhou unit 1 enters commercial
   operation," 2 January 2025; and (2021) "First Hualong One begins
   commercial operation," 30 January 2021.
8. Omoto, A. (2002). "Ten reactor years of ABWR experience." Nuclear
   Engineering International, 3 May 2002.
9. IEA/NEA (2020). Projected Costs of Generating Electricity, 2020
   edition.
10. Böhnlein, S., et al. (2026). "Too cheap to meter? A stochastic
   analysis of projected future fusion costs." arXiv:2606.26536.
11. US DOE Water Power Technologies Office. Hydropower Basics.
12. Thea Energy (2025). "Overview of the Helios Design: A Practical
   Planar Coil Stellarator Fusion Power Plant." arXiv:2512.08027.
13. Brezinsek, S., et al. (2013). "Fuel retention studies with the
   ITER-Like Wall in JET." Nuclear Fusion 53, 083023.
14. Langtry, A., et al. (2025). "Affordable, manageable, practical
   Z-pinch driver (AMPS)." arXiv:2504.10680.
15. Helion Energy (Slough, J., Kirtley, D., and Pihl, C.). "Advanced fuel
   cycle and fusion reactors utilizing the same." US 11,469,003 B2,
   granted 11 October 2022; published as US 2017/0011811.
16. Congressional Research Service (2011). "The Helium-3 Shortage:
   Supply, Demand, and Options for Congress," R41419.
17. Edelgas Group (2024) helium-3 pricing, as reported in SpaceNews and
   Newsweek (2025); Interlune-DOE Isotope Program and Interlune-Maybell
   Quantum agreements (2025); TAE Technologies and Black Moon Energy
   Corporation helium-3 supply option (2026).
18. Bosch, H.-S., and Hale, G. M. (1992). "Improved formulas for fusion
   cross-sections and thermal reactivities." Nuclear Fusion 32, 611.
19. Tuszewski, M. (1988). "Field reversed configurations." Nuclear Fusion
   28, 2033.
20. Lackner, K., Burhenn, R., Fietz, S., von Müller, A., and Ball, J.
   (2026). "Comments on the Paper 'Fundamental Scaling of Adiabatic
   Compression of Field Reversed Configuration Thermonuclear Fusion
   Plasmas'." Journal of Fusion Energy 45, 12.
21. Kirtley, D. (2024). "Fundamental theory of the direct magnetic energy
   recovery in a thermonuclear field reversed configuration system." APS
   DPP 2024, abstract GO05.8; slide captures in `docs/sources/`.
22. Nicolas, T., Goupil, C., Herbert, E., and Ball, J. (2026). "The
   Challenge for Adiabatically Heated FRC Based D-3He Fusion." Journal
   of Fusion Energy 45, 24.
23. Slough, J. (2025). "A compact fusion reactor based on the staged
   compression of a field reversed configuration." Nuclear Fusion 65,
   106019.
