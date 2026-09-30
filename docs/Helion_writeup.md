# The techno-economic floor of a Helion-class pulsed inductive fusion power plant

*Tal Rubin, Astera Institute*

In this work, we investigate how cheap fusion electricity can get if
direct energy conversion is the key technology for harnessing fusion
energy. It is one of six studies, each taking such a thesis to its
physically coherent limit and asking how low the levelized cost of
electricity (LCOE) can be driven.

Direct energy conversion is
attractive because it allows a much higher conversion efficiency from
energy in the plasma to electricity than the limit imposed by the
working temperature of a conventional working fluid. The direct energy
conversion system also replaces the conventional and expensive turbine
island. The best fusion fuel for this purpose is deuterium-helium-3 (D-He3),
whose fusion energy is carried largely by charged particles, and has relatively manageable photon emissions at fusion conditions.
One of the most efficient physical mechanisms for directly interacting with the plasma
is inductive recovery: a coil-driven magnetic field compresses the
plasma, and the plasma then expands against that field much as the gas
in an engine expands against a piston.
That is what Helion Energy is building, so this work takes Helion's
published design and results as its starting point and builds the
argument on them. Helion has stated a long-run ambition of electricity
at 1 cent/kWh ($10/MWh), and that figure is what the 1cFE residency at
Astera is set on investigating.

**The findings, in brief.** Four devices share the architecture and
differ only in the evidence grade of what they are granted: citable
records alone, Helion's own requirements at face value, labeled
extrapolations, and speculation. They read 112.1, 111.0, 26.8 and 10.6
$/MWh at 1 GWe. The speculation park reads 8.4 $/MWh at 3 GWe, so the
public 1 cent/kWh target is crossed by that one stack, through a 3% real
cost of capital (14.6 at 7%) and with the wall-and-coil replacement
included. Every number grants Helion's shot, 128 MJ from a 50 MJ bank,
which no record supports and which needs a burn of 0.3 to 0.7 s against
Helion's own stated pulse of hundreds of microseconds to milliseconds;
on citable records alone the machine makes no net power. At the
extrapolation device the largest lever is the capacitor cycle life,
worth three times the next two, the deuterium-rich burn mix and the
repetition rate. The three optimized devices do not burn Helion's mix.
Helion's patent point has He3/D = 0.158, half the fusion events D-D; the
design search picks a deuterium-rich mix with 85% of events D-D at every
grade, even carrying its higher bremsstrahlung fraction, because the
He-3 it breeds undercuts purchased He-3, and reverting the extrapolation
device to Helion's mix costs 12.0 $/MWh. That choice is what makes the
fuel cycle, not the driver, the load-bearing subsystem, with a
tonne-class tritium store intrinsic to He-3 self-supply. The data that
would move the ladder are all Polaris data, first among them the yield
of a burning shot at its measured burn time.

The costing uses the `1costingfe` bottom-up cost model [1], organized by
cost account (the CAS codes in the tables below) and built on publicly
available data and labeled extrapolations; the open-source code is
available [here](https://github.com/1cFE/1costingfe), with detailed
documentation [here](https://files.1cf.energy/1costingfe_paper.pdf), and
the commit is pinned under Reproducibility. Three of its behaviors carry
the results: the driver is priced per joule of stored energy and its
whole shot-cycled recovery chain (driver bank, recovery store, switch
stack) is replaced at the capacitor shot life; the conversion account is
priced on the energy the physics path actually returns; and the tritium
store's He-3 return is credited against purchases through a study-side
scaling of the He-3 price (Section 5.1).

This work is organized as follows: Section 2 describes Helion's device
from the published material, Section 3 defines the four devices and the
constraints they are optimized under, and Section 4 reports their cost.
Section 5 works out the He-3 economics, and Section 6 the bound that the
plasma's energy and burn time put on the yield of a shot, which is where
Helion's shot parts from Helion's stated pulse, and the recovery of the
driver energy through the expanding plasma.

## 2. Machine basis

The machine follows Helion's published architecture at face value [2, 3]. Two FRC plasmoids, formed by theta-pinch field reversal in opposed
formation sections, are accelerated and merged in a central compression
section, the collision converting their directed kinetic energy into ion
heat, and magnetic compression then does the adiabatic work to burn
conditions. The pulsed-power driver is the only heater. After the burn
the plasma expands against the field, returning driver energy and
charged fusion energy to the coil circuit as work; radiated power,
undirected charged power, and neutrons are not converted.

The design-basis shot is built from three public numbers: the driver
delivers 50 MJ per pulse (the sourced Polaris capacitor bank), the plant
fires at 1 Hz, and Orion, the first plant, is to supply Microsoft at
least 50 MW, which Helion describes as at least 50 MWe after an initial
ramp-up period [2]. Helion's stated product is the 50 MWe module: its
CEO describes a gigafactory with 50 MW generators coming off the line
and leaving on a truck, one a day [4]. No public source says how many
such modules make up Orion; this work takes it as one, as that framing
implies; the solved yield scales inversely with the count, while the
cost at fixed plant size is nearly indifferent to the split (Section 7).
The yield per shot is whatever makes the model turn that shot into 50
MWe at 1 Hz at the burn point Helion's patent discloses (Section 5):
128.1 MJ, a gain (fusion yield over delivered driver energy) of 2.56.
The gain is a consistency figure, not a disclosed measurement. The
chamber radius is 0.61 m, the smallest at which a 10 m cylinder wall
survives the shot under the tungsten flash bound of 1.5 MJ/m^2 per
pulse; the Helion device at 1 GWe is 20 modules at 1 Hz, and in general
a plant is an integer number of Helion-class modules, with the
repetition rate and module count solved jointly from the net-power
target under a rep-rate ceiling.

The public record as of September 2026 is D-T fusion on Polaris at 150
million degrees C. Helion has published no yield or recovered energy, and has withdrawn the term "net electricity" from its Polaris goals. [2, 5].
Helion does not report the data inputs a cost analysis needs, and this
work fills each gap with graded evidence tiers (Section 3): the yield of a burning
pulse and its burn time; the energy recovered with plasma present, which
the FAQ says has been measured on seven prototypes and gives no figure
for; the compression density and field of the reactor point; the
per-pulse separation rate and the per-pass fuel recovery of the exhaust
loop; and the duty cycle at which a machine fires for hours. The
capacitor cost at cycle life, the other datum the ladder rests on, is a
supplier's, not Helion's.

## 3. Method

***Notation.** 1costingfe model parameters keep their configuration-file
names. dd_frac (dhe3_dd_frac) is the D-D share of primary fusion events
by count, not an ion ratio: the patent's He3/D = 0.158 at 70 keV is
dd_frac 0.49, Helion's mix; the 3:1 D:He-3 mix is 0.31; the D-rich mix
is 0.85. dhe3_f_T is the fraction of bred tritium that burns in-pulse.
eta_dec is the circuit efficiency of inductive recovery, f_pdv the
fraction of the plasma's expansion work that reaches the coils, and
their product the composite recovery. chi is the plasma-thermal share of
the delivered driver energy and x_s the separatrix-to-coil radius ratio;
the other parameters are named where they enter.*

**Evidence ladder.** The plant environment is held in part and stepped
in part:

- Held at every grade: constant-dollar framing, and EPCM indirects at
  20% of direct cost [6], which the model scales with the build (CAS30 =
  fraction x CAS20 x (construction_time_yr / 6 yr)), so the effective
  fraction is 16.7% at a 5-year build, 10.8% at 3.25 years and 8.3% at
  2.5 years.
- Construction time, stepped: 5 years at the design basis and records
  grades (the serial Hualong One builds, about 60 months from first
  concrete to grid [7]), 3.25 years at extrapolations (the
  Kashiwazaki-Kariwa ABWR pair, 37 and 39 months from first concrete to
  fuel load [8], at the peak of a mature light-water supply chain), 2.5
  years at speculation (a combined-cycle gas turbine timeline for a
  fusion module with a tritium facility). An engineering entry, and the
  same ruling as the sister D-T study.
- Cost of capital, stepped: 7% real at the design basis and records
  grades (the IEA/NEA central case [9]), 5% at extrapolations (a
  loan-guarantee blend with precedent), 3% at speculation (the IEA/NEA
  low case [9], sovereign-class capital). It is the one entry that is
  financing rather than technology, and Figure 1 and the ladder table's
  at-7% column keep it separate.
- Book life, stepped: 30 years through the records grade (the model
  default and the low end of the fusion literature's 30-40 year cluster
  [10]), 80 years from the extrapolation grade (the US DOE hydropower
  lifespan [11]). An engineering entry: every core component is replaced
  on its own schedule and the unreplaceable structure sees negligible
  fluence.
- Availability, derived: 0.98 outside planned outages, less a routine
  outage every two years [12], a capacitor-bank swap at the bank's shot
  life, and a wall-and-coil changeout at the displacement-damage
  tolerance (dpa, displacements per atom; 20 dpa through the records
  grade, 50 above it): 0.893 at the records device, 0.924 at
  speculation, at the top of the fusion literature's 0.75 to 0.90.

The performance entries step the same way. The records device holds one
of Helion's two unrecorded claims at its evidence-supported value,
per-pulse fuel recovery 0.999 (the fuel-retention analogy to JET with
its ITER-like wall [13]); the other, the shot, has no evidence-supported
value above zero, so on evidence alone the records device makes no net
power, and it is priced at Helion's shot only so that a machine exists
to cost. The Helion device grants Helion's 0.9999 (four nines) and the
shot; the extrapolation and speculation stacks keep that grant and add
the labeled entries listed with the results in Section 4, the largest
being capacitor life 1e9 shots (Pacific Fusion's derating target for its
pulsed-power driver [14]). Every entry carries a source and grade in the
evidence ledger (`docs/ledger.md`, rendered to HTML alongside this
page); no extrapolation entry is a measured record.

**Coherence constraints.** Six couplings are enforced by the scripts on
every quoted point, and a seventh, derived in Section 6, is applied to
every quoted point in this text:

1. The radiated fraction is a function of the burn mix through a
   bremsstrahlung floor (f_rad = 0.28 at dd_frac 0.85, not Helion's
   stated 0.05).
2. Recovery efficiency is capped as the composite eta_dec x f_pdv (0.80
   through the extrapolation grade, 0.90 at speculation), because the
   only published figure speaks to the product.
3. The wall must survive both its steady flux, within the purchased wall
   class, and its per-shot flash energy, under the tungsten
   millisecond-melt bound. Two classes are purchasable: a panel wall,
   the actively cooled tungsten-on-steel panel of the ITER first-wall
   kind, qualified to about 2 MW/m^2 and priced at 0.35 M$/m^2; and a
   divertor-class wall, the monoblock of the ITER divertor kind,
   qualified to 10 MW/m^2 at 2.5 M$/m^2.
4. A mix with dd_frac at or above Helion's 0.49 carries its
   tritium-plant consequences, priced as an added fuel-handling cost of
   50 M$ fixed plus 0.657 M$ per MW of plant neutron power.
5. The in-plasma tritium burn dhe3_f_T is floored by the burnup closure
   of Section 5.2, so a low-burn claim at high per-pulse burnup is
   flagged as requiring prompt triton loss (at the patent basis the
   floor is 0.002 and the design's zero passes).
6. The expansion-work recovery fraction is capped per point: f_pdv =
   min(claim, 1 - (V_i/V_f)^(2/3)), where the claim is the grade's
   asserted f_pdv (the basis 0.80 through the extrapolation grade, 0.947
   at speculation), V_i the compressed flux volume at the 22 T basis
   field, and V_f the chamber, the whole volume stroke counted (Section
   6).
7. The shot yield is bounded by the plasma energy and the burn time,
   gain <= chi x burn time / breakeven time, with the breakeven time
   that of the plasma at the burn point, so every quoted point carries
   the burn time its shot implies, and the shot takes each device's
   grade rather than serving as a shared basis.

**Design search and reconciliation.** Each device except Helion's own
configuration is the argmin of a scan over shot yield (a free parameter
only at speculation, where the scan chooses it; the records and
extrapolation devices keep the design-basis shot), chamber length and
radius, wall class, and burn mix, discarding any design that violates a
constraint. Reconciliation then brackets each minimum with the model
gaps it cannot price internally (high-voltage DC switch duty, the
tritium-plant band, the driver-thermalization derate) and its
conservatisms (no thermal bottoming), yielding an honest band rather
than a point.

## 4. Results: the four devices and what carries the floor

| device | 1 GWe | 3 GWe | at 7% real cost of capital, 1 GWe |
|---|---|---|---|
| citable records | 112.1 | 107.8 | 112.1 |
| Helion's requirements | 111.0 | 106.9 | 111.0 |
| extrapolations | 26.8 | 23.6 | 33.9 |
| speculation | 10.6 | 8.4 | 17.9 |

LCOE in $/MWh. The at-7% column reprices each device at a 7% real cost
of capital with everything else unchanged, so the gap between it and the
1 GWe column is what the grade's cheaper money is worth: 7.1 $/MWh at
extrapolations and 7.2 at speculation. The records and Helion devices
already sit at 7%, so their two columns match. The stack and design
behind each row:

- **citable records**: fuel recovery 0.999 (JET analog); 7% real cost of
  capital, 30-year life, 5-year build; Helion's 128 MJ shot granted;
  optimum: that shot at 1 Hz in 10 m x 0.75 m panel-wall modules (25 of
  them), D-rich mix with its tritium plant
- **Helion's requirements**: Helion's configuration (50 MJ driver, 20
  modules in the smallest chamber that survives the shot, Helion's mix
  (dd_frac 0.49) with its 0.23 bremsstrahlung fraction and tritium
  plant; 7% real cost of capital, 30-year life, 5-year build) granted
  its two unrecorded claims: the 128 MJ shot that delivers the 50 MWe
  module at 1 Hz (a 0.3 to 0.7 s burn at the patent point, against
  Helion's stated pulse) and fuel recovery 0.9999
- **extrapolations**: records (with Helion's shot, here graded as the
  patent-implied 0.3 to 0.7 s burn) + capacitor life 1e9, a 3 Hz
  ceiling, a purchasable divertor-class wall, fuel recovery 0.9999, 5%
  real cost of capital, the 80-year civil-works life and a 3.25-year
  build; optimum: seven 10 m x 1.5 m panel-wall modules at 2.7 Hz
- **speculation**: extrapolations + 10 Hz, the composite recovery at its
  theory optimum 0.90, capacitors at 0.1 $/J and 1e10 shots, He-3 at 0.5
  M$/kg, 3% real cost of capital, a 2.5-year build; optimum: 300-1000 MJ
  of fusion yield per shot from the same 50 MJ driver (gain 6-20; 500 MJ
  carried, a 1 to 3 s burn at the patent point), chosen by the scan, in
  30 m x 1.5 m chambers

The coil account prices the chamber's coils along the plasma's own
expansion: the field they must hold falls from the compression value at
the burn section as the plasmoid expands down the chamber, so coil cost
grows only as the cube root of chamber length, while the expansion
volume that sets the recoverable fraction grows with radius squared. The
design search therefore trades length for radius, and the minima are
short, fat chambers. Reconciliation brackets the extrapolation device
within 21.8-31.1 $/MWh and the speculation device within 9.9-11.6 $/MWh
at 1 GWe. The D-rich mix is the strict optimum at every grade, because
it is the mix that breeds more He-3 than it burns: the 3:1 mix (dd_frac
0.31) sits 1.9 $/MWh behind at speculation and 15 $/MWh behind at
extrapolations, buying its He-3 at the stack's price entries, which
Section 5.1 shows no market supports.

The records device sits 1.1 $/MWh above Helion's requirements, 112.1
against 111.0, and two entries pull against each other to leave it there.
Reverting Helion's fourth nine of per-pulse fuel recovery to the
JET-supported three nines raises the device by about 8.3; granting the
60-year operating licence the fission fleet holds lowers it by about 7.2.
The evidentiary difference on the physics is still that one claim: At Helion's own configuration that claim
is worth about 49 $/MWh, because Helion's mix breeds less He-3 than it
burns and keeps buying (Section 5.2 derives the multiplier); the records
device escapes nearly all of it by running deuterium-rich, where the
store covers the need. The other unrecorded claim, the shot, has no
record value to revert to; both devices grant it. Both are also
dominated by scheduled replacement: the entire shot-cycled recovery
chain is replaced on the capacitor-life schedule, about eight times over
a 30-year life at the 1e8-shot record.

![The evidence ladder](figures/fig1_ladder.svg)

*Figure 1: The four devices at 1 and 3 GWe, one machine per evidence
grade, each bar split into the overnight cost recovered straight-line
over the book life (blue), the cost of money, interest during
construction and on the capital (orange), and O&M, fuel and scheduled
replacement (grey). Cost of capital 7% real at the records and Helion
devices, 5% at extrapolations, 3% at speculation; book life 30, 30, 80,
80 years.*

The two cheaper devices differ in kind. The extrapolation device changes
what is bought, each entry a labeled step beyond a record with a
physical argument behind it; the speculation device changes the prices
and the ceilings, none with a mechanism behind it. The tornado below is
drawn from the extrapolation device because its entries are the ones a
measurement could confirm or refute; the anatomy after it is drawn from
the speculation device because that is the floor.

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
at a third of its weight; then come the cost of capital (the grey
financing bar, 7.1 $/MWh), the fourth nine of fuel recovery (6.4 $/MWh,
most of it the He-3 bought while the store builds up), the 80-year book
life (4.5 $/MWh) and the 3.25-year build (1.7 $/MWh). f_pdv and the shot
are absent from the table: the extrapolation stack leaves f_pdv at the
basis 0.80 under a cap that does not bind, and the shot's record value
is no plant. The conversion efficiencies, once capped as a composite,
are worth little at the margin.

![Tornado from the extrapolation device](figures/fig2_tornado.svg)

*Figure 2: One-at-a-time reversion of each extrapolation entry to its
record value, from the 26.8 $/MWh extrapolation device. Red bars are
favorable reversions; the grey bar is the financing entry, every other
bar is physics or engineering.*

At the speculation device the capacitor-driver narrative is spent (the bank
is 5 M$ of a 666 M$ reactor account) and the floor is carried by
site and support infrastructure and by the fuel cycle (there is no
turbine island; the heat-rejection and electrical-plant accounts below
are not a steam cycle):

| item | M$ | $/MWh (approx) |
|---|---|---|
| buildings (CAS21) | 286 | 1.2 |
| CAS50, of which decommissioning provision 140 | 199 | 0.8 |
| fuel handling + tritium plant (C220500) | 190 | 0.8 |
| heat rejection + electrical plant (CAS24-26) | 170 | 0.7 |
| vacuum and exhaust (C220106), of which per-pulse pumping 78 | 107 | 0.4 |
| first wall of the 30 m chamber (C220101) | 106 | 0.4 |
| direct-conversion power electronics (C220109) | 65 | 0.3 |
| adiabat-priced coils (C220103) | 14 | 0.1 |
| O&M (CAS70), levelized in constant dollars | 34/yr | 4.3 |
| fuel (CAS80) | 2/yr | 0.3 |
| annualized capital, all-in (3% real cost of capital, 80 years) | 49/yr | 6.1 |

![What carries the floor](figures/fig3_anatomy.svg)

*Figure 3: Capital accounts carrying the speculation device. The driver
bank, the concept's narrative centerpiece, is the smallest bar; site
infrastructure and the fuel cycle dominate.*

## 5. The He-3 fuel cycle is the load-bearing subsystem

The fuel cycle is the one in Helion's patent [15], whose operating table
also fixes the burn point: a plasma with He3/D = 0.158 at 70 keV and 22
T (Helion's stated compression field of more than 15 T is consistent
with that density through pressure balance), radiating 23% of its fusion
power as bremsstrahlung and releasing 6% as neutrons. Slough [16],
citing the same patent, restates that mix as the self-sustained cycle's
limit, He-3 at roughly 16% of the fuel, and in the same paper leaves
D-He3 for a D-T design, putting the D-He3 gain at equal FRC conditions a
factor of 240 below D-T's. The D-D reactions are what close the cycle.
Half of them produce a He-3 atom directly (the prompt branch); the other
half produce a triton (the tritium branch), which is pumped out with the
exhaust after the pulse, separated, and stored on getter beds until it
decays into He-3 (12.3 yr half-life). Almost none of the tritium burns
before it is removed (dhe3_f_T = 0 in the basis). The plant therefore
has no lithium anywhere, and its tritium plant is an exhaust-processing
and storage plant.

### 5.1 The He-3 balance and the observed market

The tritium branch, 0.42 atoms per primary event, returns He-3 from the
store as (1 - e^-t/17.8 yr) builds from startup, and this work credits
that return atom for atom against purchases, levelized over the book
life at the grade's rate; the prompt bred He-3 counts as extra burns,
not as supply. A deuterium-rich plant buys He-3 only until the return
covers its need, about eight years, and its levelized purchase is 16% of
the perpetual one at the extrapolation device, 24% at the records
device's 7% and 30 years, and 11% at speculation; Helion's mix breeds
less than it burns and keeps buying, at 82%. The store's own capital,
inventory and licensing are priced regardless (constraint 4). Bought in
perpetuity at the ledger price instead, He-3 would cost the four devices
34, 4.5, 7.1 and 1.4 $/MWh more; free, it would save them 10.9, 20.3,
1.4 and 0.2 at their own mixes, and it would change the mix (Section 7).

The price matters because no cheap He-3 exists. The DOE Isotope
Program's 2011 allocation was 600 $/L to federal users and 1,000 $/L to
commercial users [17], 4.5 and 7.4 M$/kg, and prices have risen since.
The 2024-2026 transactions sit at 19-22 M$/kg on gram-to-kilogram
volumes, four to five times the 2011 allocation: spot near $2,500/L per
the Edelgas Group [18], Interlune's agreements with the DOE Isotope
Program and Maybell Quantum "at today's commercial market price", and
TAE's unpriced lunar supply option from Black Moon. The 2 M$/kg this
study charges sits below both, and the speculation entry, 0.5 M$/kg,
nine times below the 2011 allocation.

At the 2011 allocation the extrapolation device reads 28.5 $/MWh at the
D-rich mix and 67.6 at the 3:1 mix; at the commercial spot, 39.2 and
226. The deuterium-rich machine is nearly indifferent to the He-3 price,
because it buys only during the build-up; the 3:1-mix machine is not.
The credit is coupled to the burnup closure of Section 5.2, because the
decay return exists only if the tritium survives the pulse.

One consequence: a kilogram of He-3 burned at the floor produces about
$1.8M of electricity, but sold for $4.5M at the 2011 allocation and
sells for $19-22M today, so an early breeding plant earns more selling
He-3 into the thin cryogenics and quantum market than burning it, until
fleet supply floods that market.

The store that self-supply implies is large. At the speculation device
the module breeds tritium at half the D-D rate: 0.55 mg per shot, 56
kg/yr. The extrapolation stack on Helion's chamber carries 211 MW of
plant neutron power and breeds about 78 kg/yr. Store-for-decay fixes the
equilibrium inventory at production rate times the 17.8 yr mean life:
about 1.4 tonnes of tritium, which is 1.3e10 Ci, about 450 kW of
continuous decay heat, roughly 350x ITER's site authorization and 50x
the world's civilian tritium stock. The inventory is intrinsic to He-3
self-supply at this scale; shipping it to a central fuel facility
relocates it (and can hold the reactor site near ITER-class inventory
with weekly pickups) but cannot shrink it. This is why the ledger
refuses the "near-zero licensing" claim alongside the fuel credit, holds
O&M at its baseline, and treats the 200 M$ tritium-plant allowance as
more likely low than high.

The alternative to self-supply is a dedicated deuterium breeder, a
pure-D module of the same grade with its bred He-3 and tritium pumped
out every pulse, priced per kilogram delivered as module ownership plus
a throughput-sized tritium plant plus its net power at the device's own
LCOE (`scripts/breeder_loop.py`; the tables are in the ledger). It reads
the ledger's price back at the records grade, 2.2 M$/kg, cannot be
reached at the Helion device (6.9 M$/kg), and charges about 0.7 M$/kg at
extrapolations and 0.2 to 0.5 at speculation; since a self-supplying
device buys He-3 only for its build-up, it moves the ladder little
outside the Helion device, and it relocates the tritium inventory rather
than shrinking it.

### 5.2 Fuel recovery and the burnup closure

The store-and-decay idealization (dhe3_f_T = 0: no bred triton burns
in-plasma) is not a free choice; it is a claim about pulse kinetics. A
triton born mid-pulse sits in a deuterium-rich plasma at fusion
temperature for the rest of the burn, and D-T reactivity is 27-87x D-D
at 70-20 keV [19], so each unit of D burnup burns 14-43x as much of the
bred tritium. The per-pulse deuterium burnup pins the integrated
exposure x_DD = -ln(1 - f_D) = n_D <sigma v>_DD tau, and averaging over
triton births gives the thermalized-limit in-pulse tritium burn

    f_T = 1 - (1 - e^-x)/x,  x = (sv_DT / sv_DD) x_DD,

whose only physics input is the reactivity ratio. Prompt orbit loss from
the plasmoid, whose separatrix sits only a few ion gyroradii from the
field null, is the one mechanism that can hold the burn below this
floor; beam-target burn of the slowing triton can only add to it. This
closure is enforced as coherence constraint 5: any quoted point whose
dhe3_f_T sits materially below the floor is flagged as coherent only
under prompt triton loss.

The basis is the patent's burn point, n_D = 0.75e22 m^-3 at 70 keV, and
Helion's stated pulse, not the patent's confinement time (0.10 to 0.16
s, three to four orders beyond any demonstrated FRC confinement, and the
reason the shot is graded rather than priced). Over a full confinement
period at that point the D burn would be 2.5-3.8% and a thermalized
triton riding it would burn 28-38%, which is the patent's own case for
inter-pulse removal; over a sub-millisecond pulse the burnup is
1.2-2.5e-4 and the in-pulse tritium burn 0.2-0.3%, so dhe3_f_T = 0
satisfies its floor with two orders of margin. Figure 4 draws the
closure against burn time. At the 0.3 to 0.7 s the design-basis shot
needs under constraint 7, a thermalized triton burns 58 to 80% before
removal, and at the speculation shot's 1 to 3 s, 88 to 95%; the
store-and-decay cycle and the granted shot are coherent together only
under prompt triton loss, the branch the burnup axis of Figure 5 prices
at high burnup.

![The burnup closure against burn time](figures/fig4_tritium_burn.svg)

*Figure 4: The burnup closure against burn time at the patent point (n_D
0.75e22 m^-3, 70 keV): the per-pulse deuterium burnup (dashed) and the
in-pulse burn of a bred triton in the thermalized limit (solid). The
bands mark Helion's stated pulse, the patent's own confinement time, and
the burns the design-basis and speculation shots need under constraint 7
across x_s 0.5 to 0.85. The store-and-decay basis holds at the stated
pulse; at the burn the granted shot needs, most bred tritium burns in
the pulse unless it is promptly lost.*

Fuel therefore resides in the machine of order a thousand pulses before
burning, and the model carries the per-pulse pair burn_fraction = 1.2e-4
and burn_fraction_he3 = 4.1e-4 (He-3 burns 3.3x faster per pass), with
species-resolved recycle losses in the fuel account. A recirculating
nucleus faces the same race every pass, burn with probability bf
(burn_fraction) or leak with probability 1 - fr (fuel_recovery), so its
ultimate fate is the geometric series bf / (1 - fr (1 - bf)), set by the
ratio of the two rates:

| species (per-pass burn) | fr = 0.99 | fr = 0.999 | fr = 0.9999 |
|---|---|---|---|
| deuterium (1.2e-4) | 1.2% burns | 11% burns | 55% burns |
| He-3 (4.1e-4) | 3.9% burns | 29% burns | 80% burns |

At the four-nines basis, 80% of the He-3 burns and 20% is lost, while
deuterium splits nearly evenly between burning and leaking; at three
nines the loop is primarily a fuel-disposal device, wasting 71% of its
He-3, and at two nines nearly everything leaks. Tritium sees no
geometric series at all: it is extracted to the store on its first pass,
so separation loss hits it once, not compounded. With per-pulse
reprocessing the unburned-fuel repurchase multiplier is 84x at per-pass
recovery 0.99, 9.3x at 0.999, and 1.8x at 0.9999. A deuterium-rich plant
is self-sufficient in He-3 at three nines, so the multiplier bites only
on the He-3 bought while the store builds up and the fourth nine is
worth 6 $/MWh at the extrapolation device (Section 4); at Helion's mix,
which breeds less than it burns, it is worth 49. Hertz-rate isotope
separation and the tritium plant are the price of the store itself. The
JET figure behind the three-nines record is an analogy, not a per-pass
measurement: campaign retention measures co-deposited wall inventory
over many recycles, not single-transit loss, and none of the separation
slip a per-pulse reprocessing plant adds [13].

Both species' per-pass burn fractions derive from the same n tau, so the
axis is swept coherently: burn_fraction_he3 scales with burn_fraction at
the fixed 70 keV reactivity ratio (3.3x). Figure 5 shows the speculation
device's LCOE along that axis under both triton fates, at exhaust
recovery 0.99, 0.999, and 0.9999. At the patent burn point the per-pulse
fuel recovery sets the cost almost alone: 10.6 $/MWh at four nines, 12.2
at three, 27.0 at two. Toward higher compression density the recovery
requirement relaxes: above per-pulse burnup of about 1e-3 the three- and
four-nines curves converge near 10.0-10.3 $/MWh on the prompt-loss
branch, but that branch prices the fuel cycle only, since the orbit loss
that spares the tritium also removes the fusion protons, about four
fifths of the charged fusion energy at the D-rich mix, so it is a floor
on the fuel side, not an operating point. The thermalized branch turns
up past burnup 0.01 as the tritium burn grows (13-90%), so the
triton-fate question reopens exactly where the recovery question closes.
Per-pulse exhaust pumping is priced across the axis and peaks at the
patent burn point (78 M$ per module at the floor: 8300 pumped particles
per reaction).

![The burnup axis](figures/fig5_burnup.svg)

*Figure 5: LCOE at the speculation device across the per-pulse
burnup axis under the two triton fates and three exhaust-recovery
grades; the patent-density basis (dotted) is the hardest point for
fuel recovery.*

### 5.3 Neutron damage and the unshieldable throat

The replacement rate of the wall, coils, and vessel shell follows from
the D-T-equivalent neutron wall load and a dpa tolerance. The load
counts 10 dpa per MW yr/m^2 in Fe-based structure, with the 2.45 MeV D-D
flux folded at 0.4; the tolerance is taken at 20 dpa, the edge of the
irradiation database for reduced-activation ferritic-martensitic (RAFM)
steel, and at 50 dpa, the DEMO-class design target. The event carries
both the wall and the close-coupled coils (106 + 14 M$ at the
speculation device), since nothing 0.10 m behind the wall outlives it.
At the patent basis the spectrum is pure 2.45 MeV D-D at a
14-MeV-equivalent load of 0.20 MW/m^2, and the replacement cost is
modest (+0.3-1.2 $/MWh at 50-20 dpa). The damage story reopens only in
the high-burnup counterfactuals: if the reactor-point density pushes
per-pulse burnup toward the 0.1 regime with thermalized tritons, the
all-in gap between prompt-loss and thermalized reaches 8-16 $/MWh, and
on the extrapolation stack's divertor-class wall (2.5 M$/m^2, at
Helion's chamber) thermalized high-burnup replacement is prohibitive
(+52 to +134 $/MWh). Keeping the tritium out of the burn is therefore
free insurance at the patent burn point and worth double digits off it.

Shielding cannot buy the machine out of this, because a pulsed inductive
plant pays per pulse for every cubic meter of flux volume between coil
and plasma: W = (B^2/2mu0) x annulus volume, recovered only at the
composite efficiency. The 50 MJ driver at the 22 T basis field implies
about 0.26 m^3 of compression-section flux volume; a 0.4 m shield under
the compression coil multiplies the swept annulus by more than an order
of magnitude, growing the store to several hundred MJ per pulse and
dissipating tens of MJ per pulse at composite 0.90: order 100 MW or more
of recirculating loss at the speculation rep rate. Shielding is
affordable only where the guide field is low, far from the burn section,
so the coils nearest the burn are sacrificial, ceramic-insulated, and on
the wall-replacement schedule. The burn is also localized near the
compression section, so the uniform-cylinder audit understates the local
load; a localized audit would roughly double the damage costs.

The replacement schedule has a structural threshold. The wall, coils,
and vessel shell are 155 of about 370 M$ of per-module reactor hardware;
replacement of the wall-and-coil event (120 M$) outspends the module's
own capital service when its interval falls below about 10 years at the
speculation grade's 3% real cost of capital (5 years at 7%). At the
patent basis (D-D spectrum, 0.20 MW/m^2 equivalent) the interval is
about 10 to 25 years at 20 to 50 dpa: a capital asset at the design
target, at the edge of one at the RAFM database edge. The
consumable-core regime (1-3 year intervals, half the module's value
swapped near-annually) belongs to the high-burnup thermalized
counterfactual, where the core becomes a swappable cartridge and the
plant a manufacturing operation with a waste stream this study does not
price.

## 6. The yield a shot can return, and what the circuit recovers of it

Every number in this work grants Helion's shot. This section bounds what
a shot can return from the plasma's own energy and burn time, and finds
the design-basis shot incompatible with Helion's stated pulse. It then
sets out the two further bounds on what the circuit recovers of a shot,
the share of the driver energy that thermalizes and the expansion ratio
the chamber allows, beyond the composite cap of constraint 2 that stops
the two conversion efficiencies from being counted twice. A three-shot
sequence on Polaris would measure all three.

**The yield bound.** The plasma at peak compression holds a share chi of
the delivered driver energy E_del (50 MJ per pulse): merging shock and
compression work are the only heating, and chi is fixed by the FRC
equilibrium as a function of the separatrix-to-coil radius ratio alone,
chi(x_s) = 1.5 <beta> x_s^2 / (1.5 <beta> x_s^2 + 1 - x_s^2) with <beta>
= 1 - x_s^2/2 [20]: 0.30, 0.52 and 0.71 at x_s = 0.5, 0.7 and 0.85. That
energy sits at the energy density of a beta = 1 plasma, 1.5 B^2/2mu0,
and burns at the fusion power density of the burn point, so

    gain <= chi x burn time / breakeven time,

with the breakeven time the ratio of those two densities, the fusion
breakeven time of Lackner et al. [21]; the pulsed gain of Nicolas et al.
[22], fusion energy over plasma energy, is the same ratio against their
Lawson time. The patent point is n_D 0.75e22 m^-3, He3/D 0.158, 70 keV
and 22 T. At Bosch-Hale rates its breakeven time is 86 ms with
thermalized electrons, and 3.7 times shorter if the electrons could be
held at a tenth of the ion temperature. They cannot be held there: the
ion-electron equilibration time at that density is about 1 ms, well
inside the breakeven time [21]. Helion's stated pulse is hundreds of
microseconds to milliseconds [2]. Against it the bound reads: a 1 ms
burn returns 0.2 to 0.4 MJ from the 50 MJ bank across x_s 0.5 to 0.85,
less than the circuit loses per shot at any eta_dec in the ladder; the
design-basis 128 MJ shot needs 0.3 to 0.7 s; the speculation shot needs
1 to 3 s. The bound also reproduces the co-founder's own D-T design:
Slough [16] quotes a gain of 9.1 on the FRC energy over a 2 to 5 ms
transit at 34.8 T and 15 keV, and at that point's breakeven time the
same arithmetic gives a 3.4 ms burn. This is constraint 7, and it is why
the shot is a graded claim rather than a shared basis; every point the
scripts evaluate carries the burn time its shot implies at x_s 0.7. Two
independent reconstructions find Helion's fusion-to-bremsstrahlung ratio
3.6 to 9 times too favorable [22] or about an order of magnitude [21],
the provenance of the 0.05 radiated fraction that constraint 1 withdrew.

**Driver thermalization.** The same chi bounds the recovery of the
driver energy itself. The thermalized share can only return through the
same expansion channel as the fusion heat, at f_pdv, while the model
recovers all of it at the flat inductive efficiency. The uncaptured loss
is worth +1.4 to +3.3 $/MWh at the extrapolation device across the x_s
span, under 0.1 $/MWh at the speculation device, and order +10 $/MWh at
the low-gain Helion device; it is carried in the reconciliation bands.

**The expansion-ratio bound.** Constraint 6 caps f_pdv at the
adiabatic-stroke bound 1 - (V_i/V_f)^(2/3), with V_i = E_del/(B^2/2mu0),
about 0.26 m^3 at 50 MJ and 22 T. Applied per point: the extrapolation
device's 10 m x 1.5 m chamber caps f_pdv at 0.98, above its claimed
0.80, and the speculation device's 30 m x 1.5 m chamber caps it at
0.989, just above the claimed 0.947. The large chamber buys expansion
ratio, not merely wall area, and recovery cannot be improved without
more chamber. About a fifth of the expansion work is axial, against the
end-field gradient [23]; constraint 6 counts the whole volume stroke, as
Helion's own burn-cycle framework does, and whether the end circuits
return that fifth is a design question the shot sequence below measures.

The cycle is Diesel-type with an Atkinson over-expansion, the framing of
Helion's own burn-cycle analysis [24], which quotes about 60% for a
constant-pressure burn and above 90% for optimal cycles. Two published
figures sit against it. Nicolas et al. [22], whom Helion's FAQ cites for
recovery "exceeding 95%", give that number only as an ideal Carnot-form
bound and set it aside on the thin-cycle argument. Slough [16], the
co-founder whose patent supplies the fuel cycle, derives 40% as the most
an ejected FRC can return in a flux-conserving expansion chamber, where
it comes to rest holding 1.5 pV of thermal energy against the field it
has compressed, and states that an FRC does not free-expand. That is his
own recovery topology, not the discharged compression coil this work's
f_pdv assumes, so it is carried as a risk row rather than a cap: at
f_pdv 0.4 the extrapolation device reads 44.2 $/MWh (+17.4) and the
speculation device 14.8 (+4.2). There is no Carnot exemption in any of
this: cycle form, the compression and expansion ratios, and the entropy
of the deliberately irreversible merging set the efficiency, which is
what the composite cap encodes.

**Measurement protocol.** A three-shot sequence on Polaris separates the
whole chain: a vacuum shot measures eta_dec alone; a plasma no-burn shot
returns eta_dec[(1 - chi) + chi f_pdv], so its deficit against vacuum
measures chi(1 - f_pdv); a burning shot adds the fusion composite, and
its yield reads constraint 7 directly. This single protocol prices the
composite cap, the thermalization share, the shot, and (through the wall
budget) the rep-rate ceiling; published excluded-flux radii pin chi per
shot in the interim. It is Helion's own stated proof point: its FAQ
defines demonstrating electricity from fusion as showing that energy
returned to a capacitor bank came from fusion-driven expansion "rather
than only from ordinary inductive coupling in the circuit".

## 7. What reaches $10/MWh, and what gets it there

The target is reached only as a park. Two controlled sweeps at the
speculation stack (constant gain, constant wall loading, driver and
chamber scaled with module power) separate module count from plant size.
**Module count at fixed plant size is nearly free**: a park of 500 MWe
modules reads 10.1 $/MWh against the single 1 GWe module's 10.6 $/MWh
(the adiabat-priced coils reward smaller compressed volumes; 250 MWe
modules read 10.3), and even 50 MWe modules cost only four tenths of a
dollar more (11.0), because buildings, supplementary capital, and
balance of plant price plant totals; the only modularity tax is
per-module fixed items, biting below about 100 MWe. **Standalone plant
size is expensive**:

| plant | LCOE ($/MWh) | $/kW | dominant penalties |
|---|---|---|---|
| 1 GWe | 10.6 | 1492 | - |
| 250 MWe | 17.5 | 2268 | fixed site buildings, staffing^0.5 |
| 50 MWe | 43.3 | 6342 | O&M 17.2 $/MWh (staffing law), 141 M$ of buildings, tritium-plant fixed core |

The standalone penalty is about 138 M$ of fixed site buildings
calibrated on fission-class analogs, the P^0.5 staffing law of the Idaho
National Laboratory sodium-fast-reactor basis [25], and the absence of
any fleet-learning term on equipment, so this concept's economics live
in power parks, and the 50 MWe module of Helion's gigafactory framing
[4] is a manufacturing choice the model neither rewards nor punishes at
park scale.

Within that park, the entry that carries the full speculation stack
across is its financing: the 3 GWe park reads 8.4 $/MWh (10.6 at 1 GWe),
and at the design-basis 7% real cost of capital the same machine reads
14.6 $/MWh (17.9 at 1 GWe), so the 3% real cost of capital,
sovereign-class money with no mechanism behind it, is worth more than
the whole distance to the target. No physics or engineering entry
crosses it on its own, and the crossing needs the derived availability
of 0.92 (at the model default of 0.85 the park reads 9.0 $/MWh and at
0.95 it reads 8.2, so it holds at any availability above the default)
and Helion's shot granted, as for every number here (the park's 200 MJ
pulses are a burn of half a second to a second at the patent point). It
survives the wall-and-coil replacement, priced in Section 5.3 on top of
the model's figure: 0.4 $/MWh at the 50 dpa tolerance and 1.2 at the
demonstrated 20 dpa take the park to 8.8 to 9.6 $/MWh.

- **He-3 at zero cost** (6.5 $/MWh at 3 GWe): worth 1.9 $/MWh, and it
  changes the machine. The deuterium-rich park gains only 0.2 $/MWh,
  since it buys He-3 only while its store builds up; the design search
  re-run at zero price picks the He-3-rich mix (dd_frac 0.13) in 15 m
  chambers with no tritium plant, at 6.5 $/MWh.
- **Gas-class site and decommissioning analogs** (about 2 $/MWh at 1
  GWe, the whole of the buildings and CAS50 lines): defensible only for
  the 3:1-mix machine, which carries no tritium plant; the D-rich
  machine's tonne-class tritium inventory argues the other way.
- **A real fleet-learning term** on equipment, anchored beyond the fleet
  the nth-of-a-kind (NOAK) constants already assume, or it double counts:
  the only mechanism that rewards the mass-produced small-unit strategy at
  all.

None of these is in the evidence base at any grade.

## 8. Conclusions

Four devices on one architecture read 112.1, 111.0, 26.8 and 10.6 $/MWh
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

Of the data Helion does not report (Section 2), the shot gates the whole
plant, the recovery chain 2 to 17 $/MWh at the extrapolation grade, and
the fuel-cycle data a few $/MWh at the deuterium-rich mix and tens at
Helion's; the capacitor cost at cycle life, a supplier's datum, gates
tens.

The speculation stack is jointly heroic: 0.1 $/J capacitors with
1e10-shot life contradict the derating physics that connects capacitor
cost to life, the composite recovery sits at its theory optimum with
zero margin, and the 500 MJ shot is a burn of seconds. The floor is
conditional on the patent-basis compression field (a 10 T reactor point
adds about 2 $/MWh, a 5 T point about 11) and on the discharged-coil
recovery topology (Slough's 40% ceiling adds 4.2 $/MWh at speculation
and 17.4 at extrapolations); the neutron-damage costs are more likely
low than high, and the one conservatism, no thermal bottoming, is worth
-4.3 $/MWh at the extrapolation device.

The constructive reading: the floor, conditional on the shot, is low by
any thermal-plant standard, the architecture of factory modules, park
deployment and swappable cores fits the failure modes the physics
imposes, and the data that would move the ladder from speculation to
evidence, the shot first among them, are Polaris data.

## Reproducibility

Everything here is in the study repository at
[github.com/1cFE/helion_pulsed_frc_tea](https://github.com/1cFE/helion_pulsed_frc_tea):
the four evidence stacks in `config/`, the scripts in `scripts/` that
produce every number, every figure and the HTML, LaTeX and PDF
renderings of this page and the ledger (the README says what each one
does), the evidence ledger, the adversarial review, the capacitor
evidence, and the Helion slide and FAQ captures. The cost model is
`1costingfe` at commit 44434d9. The regression tests pin every quoted
device at both plant sizes, every constraint, the yield bound, the He-3
credit and the financing ladder, and fail loudly if the model moves
under this work.

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
16. Slough, J. (2025). "A compact fusion reactor based on the staged
   compression of a field reversed configuration." Nuclear Fusion 65,
   106019.
17. Congressional Research Service (2011). "The Helium-3 Shortage:
   Supply, Demand, and Options for Congress," R41419.
18. Edelgas Group (2024) helium-3 pricing, as reported in SpaceNews and
   Newsweek (2025); Interlune-DOE Isotope Program and Interlune-Maybell
   Quantum agreements (2025); TAE Technologies and Black Moon Energy
   Corporation helium-3 supply option (2026).
19. Bosch, H.-S., and Hale, G. M. (1992). "Improved formulas for fusion
   cross-sections and thermal reactivities." Nuclear Fusion 32, 611.
20. Tuszewski, M. (1988). "Field reversed configurations." Nuclear Fusion
   28, 2033.
21. Lackner, K., Burhenn, R., Fietz, S., von Müller, A., and Ball, J.
   (2026). "Comments on the Paper 'Fundamental Scaling of Adiabatic
   Compression of Field Reversed Configuration Thermonuclear Fusion
   Plasmas'." Journal of Fusion Energy 45, 12.
22. Nicolas, T., Goupil, C., Herbert, E., and Ball, J. (2026). "The
   Challenge for Adiabatically Heated FRC Based D-3He Fusion." Journal
   of Fusion Energy 45, 24.
23. Spencer, R. L., Tuszewski, M., and Linford, R. K. (1983). "Adiabatic
   compression of elongated field-reversed configurations." Physics of
   Fluids 26, 1564.
24. Kirtley, D. (2024). "Fundamental theory of the direct magnetic energy
   recovery in a thermonuclear field reversed configuration system." APS
   DPP 2024, abstract GO05.8; slide captures in `docs/sources/`.
25. Idaho National Laboratory. Advanced-reactor staffing studies.
