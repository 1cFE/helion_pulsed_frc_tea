# The techno-economic floor of a Helion-class pulsed inductive fusion power plant

*Tal Rubin, Astera Institute*

In this work, we investigate how cheap fusion electricity can get if
direct energy conversion is the key technology for harnessing fusion
energy. It is one of six studies, each taking such a thesis to its
physically coherent limit and asking how low the levelized cost of
electricity (LCOE) can be driven.

Direct energy conversion is attractive because it allows a much higher
conversion efficiency from energy in the plasma to electricity than the
limit imposed by the working temperature of a conventional working
fluid. The direct energy conversion system also replaces the
conventional and expensive turbine island. The best fusion fuel for this
purpose is deuterium-helium-3 (D-He3), whose fusion energy is carried
largely by charged particles, and has relatively manageable photon
emissions at fusion conditions. One of the most efficient physical
mechanisms for directly interacting with the plasma is inductive
recovery: a coil-driven magnetic field compresses the plasma, and the
plasma then expands against that field much as the gas in an engine
expands against a piston. That is what Helion Energy is building, so
this work takes Helion's published design and results as its starting
point and builds the argument on them. Helion has stated a long-run
ambition of electricity at 1 cent/kWh ($10/MWh), and that figure is what
the 1cFE residency at Astera is set on investigating.

**The findings, in brief.** Four devices share the architecture and
differ only in the evidence grade of what they are granted: citable
records alone, Helion's own requirements at face value, labeled
extrapolations, and speculation. They read 112.1, 105.9, 29.1 and 11.6
$/MWh at 1 GWe, and the speculation park reads 9.4 $/MWh at 3 GWe, so
the cheapest coherent machine sits 1.6 $/MWh above the public 1
cent/kWh target as a 1 GWe plant and 0.6 under it as a park, on a 3%
real cost of capital worth 6.8 $/MWh at the park (16.2 at 7%), on a
driver bank four times Polaris's worth 0.7, and on the compression coil
the patent's own 22 T point already needs, the one coil this work can
stand on.

The compression field and the driver bank are design choices here, not
Polaris's values held fixed: the burn point moves with the field (the
density as B^2 at beta = 1, the breakeven time as B^-2, the per-pulse
burnup as B^2), and the bank sets the shot at a given gain. The records
grade holds both at the patent's 22 T and Polaris's 50 MJ, since no
record exists above either; the extrapolation grade holds the field and
doubles the bank, worth 1.0 $/MWh; speculation takes the bank to 200
MJ, worth 0.7, and scans the field to 50 T, but the coil bounds the
field at the basis at every grade: the 22 T coil already cycles at or
above the copper-alloy gigacycle band, no higher fatigue basis is
sourced anywhere in this work, and the cost model offers no resistance
of its own, since its coil account prices conductor along an expansion
adiabat that shrinks as the compressed flux volume does and carries no
structure for the magnetic pressure. A higher field is therefore priced
as a sensitivity and excluded from every device: it would be worth up
to 1.4 $/MWh at 50 T, on a coil cycled to 1 GPa that this work cannot
price, and Section 4 reports it as such.

Every number grants Helion's shot, 128 MJ from a 50 MJ bank at the
patent point, which no record supports and which needs a burn of 0.3 to
0.7 s against Helion's own stated pulse of hundreds of microseconds to
milliseconds; on citable records alone the machine makes no net power.
That burn also has to fit between shots, and that bound sets each
device's fuel mix and firing rate together: every optimized device runs
deuterium-rich and slow, in more modules than its granted rate ceiling
would need, the records and extrapolation devices at 96 to 100% of the
bound and the speculation device, two 15 m burn sections on the 200 MJ
bank, at 86% (Sections 4 and 6). The mix is a fuel-price result rather
than a physics one: with He-3 free the search returns to the He-3-rich
preset at every grade. The fuel cycle, not the driver, is the load-bearing
subsystem either way: every device breeds most of its He-3 and holds a
tritium store of two thirds of a tonne to 2.6 tonnes while it decays,
and what He-3 it still buys is priced at entries no market supports.
The data that would move the ladder are all Polaris data, first among
them the yield of a burning shot at its measured burn time.

The costing uses the `1costingfe` bottom-up cost model [1], organized by
cost account (the CAS codes in the tables below) and built on publicly
available data and labeled extrapolations; the open-source code is
available [here](https://github.com/1cFE/1costingfe), with detailed
documentation [here](https://files.1cf.energy/1costingfe_paper.pdf), and
the commit is pinned under Reproducibility.

This work is organized as follows: Section 2 describes Helion's device
from the published material, Section 3 defines the four devices and the
constraints they are optimized under, and Section 4 reports their cost.
Section 5 works out the He-3 economics, and Section 6 the bound that the
plasma's energy and burn time put on the yield of a shot, which is where
Helion's shot parts from Helion's stated pulse, and the recovery of the
driver energy through the expanding plasma.

## 2. Machine basis

The machine follows Helion's published architecture at face value [2, 3]. 
Two FRC plasmoids, formed by theta-pinch field reversal in opposed
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
target under a rep-rate ceiling. That ceiling is a design choice in
this work: a grade's granted ceiling is permission, not obligation, and
the design search sets each device's ceiling at or below its grant,
never above, so that a plant may fire slower in more modules (Section
3). The compression field and the bank are design choices as well,
Polaris's values being a prototype's rather than a plant's: the burn
point is the patent's at the field a device compresses to, and the bank
is a count of modular capacitor units; both are scanned by grade, the
bank bounded by the grades and the field by the coil (Section 3).

The public record as of September 2026 is D-T fusion on Polaris at 150
million degrees C. Helion has published no yield or recovered energy,
and has withdrawn the term "net electricity" from its Polaris goals [2,
5]. Helion does not report the data inputs a cost analysis needs, and
this work fills each gap with graded evidence tiers (Section 3): the
yield of a burning pulse and its burn time; the energy recovered with
plasma present, which the FAQ says has been measured on seven prototypes
and gives no figure for; the compression density and field of the
reactor point; the per-pulse separation rate and the per-pass fuel
recovery of the exhaust loop; and the duty cycle at which a machine
fires for hours. The capacitor cost at cycle life, the other datum the
ladder rests on, is a supplier's, not Helion's.

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

**Design search and reconciliation.** Each device except Helion's own
configuration is the minimum-LCOE design of a scan over the compression
field and the driver bank (graded below), the shot as a gain on the
bank (the design-basis gain of 2.56 through the extrapolation grade, so
the shot scales with the bank and the burn it implies does not; the
gain free at speculation, where the scan chooses it), chamber length
and radius, wall class (constraint 3), burn mix (seven mixes from the
He-3-rich preset to the deuterium-rich end, each on its bremsstrahlung
floor), and firing rate (a ladder of rate ceilings at and below the
lower of the grade's granted ceiling and the duty bound of constraint
8, down to half of it, each rung forcing the plant into more, slower
modules), discarding any design that violates one of the coherence
constraints below. The cost model builds every plant in the fewest
modules its ceiling permits, firing just under the ceiling, so the
ceiling is how the search prices the trade between hardware (more
modules) and a slower bank (replaced less often, with the derived
availability rising). Reconciliation then brackets each minimum with
the model gaps it cannot price internally (high-voltage DC switch duty,
the tritium-plant band, the driver-thermalization derate) and its
conservatisms (no thermal bottoming), yielding an honest band rather
than a point.

**The field and the bank, graded.** The patent's burn point (22 T, n_D
0.75e22 m^-3, 70 keV) and Polaris's 50 MJ bank are the design basis,
and no record exists above either. The records grade holds both. The
extrapolation grade holds the field and doubles the bank to 100 MJ, a
procurement rather than a technology, since a bank is a count of the
modular capacitor units Helion is tooling its Omega facility to produce
for Orion (about 2,500 of them [27]). The speculation grade takes the
bank to 200 MJ, four times Polaris, and scans the field to 50 T (30, 40
and 50 T), but the coil bounds the field at the basis at every grade
(constraint 9): the 22 T coil already cycles to a magnetic pressure at
or above what copper alloys survive for a billion cycles, no conductor
with a gigacycle record exists beyond that band, and no higher fatigue
basis is sourced anywhere in this work, so no grade may buy a field
above the basis. The fields above it are priced as a sensitivity, what
a higher field would be worth on a coil this work cannot price, and
excluded from every device. The burn point follows the field at every
scanned point: at beta = 1 and the patent's ion temperature the density
scales as B^2, so the breakeven time of constraint 7 falls as B^-2 (126
ms at the extrapolation device's mix and 104 ms at the speculation
device's, both at 22 T; 5.2 times shorter at 50 T), the per-pulse
burnup of Section 5.2 rises as B^2 (1.2e-4 at the basis, 6.2e-4 at 50
T), the compressed flux volume of constraint 6, E_del/(B^2/2mu0),
shrinks as B^-2 and grows with the bank, and the magnetic pressure of
constraint 9 rises as B^2. The cost model prices the coils at the field
(`b_center`) and the driver per joule (`e_driver_mj`), and the wall's
steady flux and per-shot flash follow the fusion power and the shot
through constraint 3.

**Evidence ladder.** The plant environment is held in part and stepped
in part:

- Held at every grade: constant-dollar framing, and EPCM indirects at
  20% of direct cost [6], which the model scales with the build time
  (CAS30 = fraction x CAS20 x (construction_time_yr / 6 yr)), so the
  effective fraction is 16.7% at a 5-year build, 10.8% at 3.25 years and
  8.3% at 2.5 years.
- Construction time, stepped: 5 years at the design basis and records
  grades (the serial Hualong One builds, about 60 months from first
  concrete to grid [7]), 3.25 years at extrapolations (the
  Kashiwazaki-Kariwa ABWR pair, 37 and 39 months from first concrete to
  fuel load [8], at the peak of a mature light-water supply chain), 2.5
  years at speculation (a combined-cycle gas turbine timeline for a
  fusion module with a tritium facility). An engineering entry.
- Cost of capital, stepped: 7% real at the design basis and records
  grades (the IEA/NEA central case [9]), 5% at extrapolations (a
  loan-guarantee blend with precedent), 3% at speculation (the IEA/NEA
  low case [9], sovereign-class capital). It is the one entry that is
  financing rather than technology, and Figure 1 and the ladder table's
  at-7% column keep it separate.
- Book life, stepped: 60 years through the records grade, a
  series-consistency entry rather than a record, adopted because the
  other candidate corridor studies hold 60 at their records rung. Sixty
  years is the standard first-renewal licence term, which is neither the
  licensed bound (thirteen US plants hold subsequent renewals to 80
  years [26]) nor demonstrated operation (about 57 years: Beznau 1,
  1969, and Ginna at 55.9), and it sits above the fusion literature's
  30-40 year cluster [10]. 80 years from the extrapolation grade (the US
  DOE hydropower lifespan [11]). An engineering entry: every core
  component is replaced on its own schedule and the unreplaceable
  structure sees negligible fluence.
- Availability, derived: 0.98 outside planned outages, less a routine
  outage every two years [12], a capacitor-bank swap at the bank's shot
  life, and a wall-and-coil changeout at the displacement-damage
  tolerance (dpa, displacements per atom; 20 dpa through the records
  grade, 50 above it): 0.893 at the records device, 0.927 at
  speculation, at the top of the fusion literature's 0.75 to 0.90.

The performance entries step the same way. The records device holds one
of Helion's two unrecorded claims at its evidence-supported value,
per-pulse fuel recovery 0.999 (the fuel-retention analogy to JET with
its ITER-like wall [13]). The other, the shot, has no evidence-supported
value above zero, and a machine whose shots return nothing has no power
to sell and cannot be costed at all. The records device is therefore
granted Helion's shot, as every device here is, and the figure reported
for it is the cost of a machine resting on that one unsupported number,
not the cost of what the records support. The Helion device grants
Helion's 0.9999 (four nines) and the shot; the extrapolation and
speculation stacks keep that grant and add the labeled entries listed
with the results in Section 4, the largest being capacitor life 1e9
shots (Pacific Fusion's derating target for its pulsed-power driver
[14]). Every entry carries a source and grade in the evidence ledger
(`docs/ledger.md`, rendered to HTML alongside this page); no
extrapolation entry is a measured record.

**Coherence constraints.** Nine couplings are applied to every quoted
point. Seven are enforced by the scripts as checks; the seventh, derived
in Section 6, is applied by construction, every point carrying the burn
time its shot implies; and the eighth is enforced on that burn time:

1. The radiated fraction is a function of the burn mix through a
   bremsstrahlung floor, because a deuterium-rich plasma radiates more of
   its fusion power, not less: 0.28 at dd_frac 0.85 against 0.20 at
   Helion's 0.488. Helion's own patent figure, 0.23, sits above its
   floor, so the Helion device is priced at the patent's value.
2. Recovery efficiency is capped as the composite eta_dec x f_pdv (0.80
   through the extrapolation grade, 0.90 at speculation), because the
   only published figure speaks to the product.
3. The wall must survive two different loads. Its steady flux must stay
   within the limit the purchased wall class is qualified to, which is
   what the coolant can carry away continuously; and its per-shot flash
   energy, deposited in about a millisecond before conduction can spread
   it, must stay under the tungsten melt bound of 1.5 MJ/m^2, taken with
   no margin. Two classes are purchasable: a panel wall, the actively
   cooled tungsten-on-steel panel of the ITER first-wall kind, qualified
   to about 2 MW/m^2 and priced at 0.35 M$/m^2; and a divertor-class
   wall, the monoblock of the ITER divertor kind, qualified to 10 MW/m^2
   at 2.5 M$/m^2.
4. A mix with dd_frac at or above Helion's 0.49 carries its
   tritium-plant consequences, priced as an added fuel-handling cost of
   50 M$ fixed plus 0.657 M$ per MW of plant neutron power: a
   unit-priced allowance rather than a costed scope, which its
   throughput takes to 173 M$ at the extrapolation device and 123 M$ at
   the speculation device.
5. The in-plasma tritium burn dhe3_f_T is floored by the burnup closure
   of Section 5.2, so a low-burn claim at high per-pulse burnup is
   flagged as requiring prompt triton loss (at the patent basis the
   floor is 0.002 and the design's zero passes).
6. The expansion-work recovery fraction is capped per point: f_pdv =
   min(claim, 1 - (V_i/V_f)^(2/3)), where the claim is the grade's
   asserted f_pdv (the basis 0.80 through the extrapolation grade, 0.947
   at speculation), V_i the compressed flux volume at the point's own
   bank and field, E_del/(B^2/2mu0), and V_f the chamber, the whole
   volume stroke counted (Section 6).
7. The shot yield is bounded by the plasma energy and the burn time,
   gain <= chi x burn time / breakeven time, with the breakeven time
   evaluated for the plasma at the burn point of the point's own field
   and at the mix the point actually burns (purchased He-3 plus the bred
   He-3 that recycles), so every quoted point carries the burn time its
   shot implies, and the shot takes each device's grade rather than
   serving as a shared basis.
8. A shot's implied burn must fit inside the pulse period: burn time x
   repetition rate <= 1, because one burn section holds one plasmoid and
   the next shot cannot fire while the last is still burning. The bound
   is hard at 1.0, with nothing reserved for exhaust, refill and
   recharge. Equivalently it caps one burn section's fusion power at chi
   E_del / breakeven time, which tightens as the mix turns
   deuterium-rich and loosens as the field squared and with the bank;
   Section 6 gives the cap per design and the span across x_s. The rate
   is a design choice under it: the search fires each device at or below
   the lower of its grant and the bound, in the fewest modules whose
   rate fits its burn.
9. The compression coil is checked against its own mechanics. Every
   shot cycles it from zero to the magnetic pressure B^2/2mu0, a billion
   to ten billion times over the book life: 193 MPa at the 22 T basis,
   at or above the 100 to 150 MPa gigacycle fatigue strengths of copper
   alloys, which is an open item on the basis coil itself. The bound is
   evidential and the same at every grade, speculation included: the
   patent's 22 T is the only field with a source, its coil already
   cycles at or above the band, and no higher fatigue basis is sourced
   anywhere in this work, so no grade may buy a field above the basis.
   The bound has to live in the constraint set because the cost model
   offers no resistance of its own: at 50 T the pressure is 995 MPa, and
   the coil account, which prices conductor along the expansion adiabat,
   falls with the field rather than rising, because the compressed flux
   volume it integrates over shrinks as B^-2. The scan still prices 30,
   40 and 50 T designs, as a sensitivity labeled as resting on a coil
   this work cannot price and excluded from every device.

## 4. Results: the four devices and what carries the cost floor

| device | field, bank, shot | 1 GWe | 3 GWe | at 7% real cost of capital, 1 GWe |
|---|---|---|---|---|
| citable records | 22 T, 50 MJ, 128 MJ | 112.1 | 108.2 | 112.1 |
| Helion's requirements | 22 T, 50 MJ, 128 MJ | 105.9 | 102.1 | 105.9 |
| extrapolations | 22 T, 100 MJ, 256 MJ | 29.1 | 26.2 | 37.2 |
| speculation | 22 T, 200 MJ, 512 MJ | 11.6 | 9.4 | 19.5 |

LCOE in $/MWh. The at-7% column reprices each device at a 7% real cost
of capital with everything else unchanged, so the gap between it and the
1 GWe column is what the grade's cheaper money is worth: 8.1 $/MWh at
extrapolations and 7.8 at speculation. The records and Helion devices
already sit at 7%, so their two columns match. Every device is a
panel-wall machine, and each 3 GWe park is the same module tripled. The
stack and design behind each row:

- **citable records**: fuel recovery 0.999 (JET analog); 7% real cost of
  capital, 60-year life, 5-year build; the patent field and Polaris
  bank, since no record exists above either; Helion's 128 MJ shot
  granted; optimum: that shot at the deuterium-rich dd_frac 0.85 with
  its tritium plant, the mix that breeds more He-3 than it burns, in 25
  modules of 10 m x 0.75 m at 0.985 Hz under the 1 Hz grant, the fewest
  modules whose rate fits its 1.01 s burn, at 99.9% of the duty bound
- **Helion's requirements**: Helion's configuration (50 MJ driver at 22
  T, 20 modules in the smallest chamber that survives the shot, Helion's
  mix (dd_frac 0.49) with its 0.23 bremsstrahlung fraction and tritium
  plant; 7% real cost of capital, 60-year life, 5-year build) granted
  its two unrecorded claims: the 128 MJ shot that delivers the 50 MWe
  module at 1 Hz (a 0.3 to 0.7 s burn at the patent point, against
  Helion's stated pulse) and fuel recovery 0.9999
- **extrapolations**: the records stack with Helion's gain (2.56, graded
  here as the patent-implied 0.3 to 0.7 s burn), plus capacitor life 1e9
  shots, a 3 Hz repetition-rate ceiling (1 Hz at the design basis), a
  purchasable divertor-class wall, fuel recovery 0.9999, 5% real cost of
  capital, the 80-year civil-works life and a 3.25-year build; the
  field at 22 T (the coil bound, constraint 9) and the bank doubled to
  100 MJ; optimum: 256 MJ shots at dd_frac 0.80 with its tritium plant
  in 6 modules of 10 m x 1.5 m at 1.56 Hz under the 3 Hz grant, the
  fewest modules whose rate fits its 0.62 s burn, at 96% of the duty
  bound; the 3 GWe park is 18 of them. The doubled bank is worth 1.0
  $/MWh: on the Polaris bank the same stack is 128 MJ shots in 12
  modules of 10 m x 0.75 m at 1.58 Hz, 30.1 $/MWh
- **speculation**: the extrapolation stack, plus a 10 Hz ceiling, the
  composite recovery at its theory optimum 0.90, capacitors at 0.1 $/J
  and 1e10 shots, He-3 at 0.5 M$/kg, 3% real cost of capital, a 2.5-year
  build; the bank free to 200 MJ, the field scanned to 50 T and bounded
  at the basis by the coil (constraint 9); optimum: 22 T and a 200 MJ
  bank, 512 MJ shots at the design-basis gain of 2.56 (the freed gain
  buys nothing: the gain-3 shot in the same chamber reads within 0.01
  $/MWh), a burn of 0.3 to 0.7 s at the patent point and 0.51 s at its
  own mix, at dd_frac 0.70 with its tritium plant, in 2 modules of 15 m
  x 1.5 m at 1.67 Hz under the 10 Hz grant, the fewest modules whose
  rate fits that burn, at 86% of the duty bound, with the panel wall at
  1.82 MW/m^2 against its 2 MW/m^2 limit; the 3 GWe park is 6 of them.
  The bank is worth 0.7 $/MWh: on the Polaris bank the same stack is
  150 MJ shots in 7 modules of 10 m x 0.75 m at 1.65 Hz, 12.4 $/MWh.
  The coil cycles to the basis 193 MPa, the same open item every device
  carries

The field above the basis is priced and reported, and excluded from
every device by the coil. The best design the coil bound alone excludes
reads 10.9 $/MWh at 30 T (a 200 MJ bank firing 600 MJ shots at dd_frac
0.70 in a single 30 m x 1.5 m module at 2.82 Hz), 10.5 at 40 T, and
10.2 at 50 T (a 100 MJ bank firing 600 MJ shots at dd_frac 0.85 in a
single 30 m x 1.5 m module at 2.94 Hz, where the panel wall's steady
flux binds at 97% of its limit before the duty does, at 0.83), with
8.6, 8.2 and 7.9 at the park: a field this work cannot stand on would
be worth 0.7, 1.2 and 1.4 $/MWh at either plant size, on a coil cycled
to 358, 637 and 995 MPa. Below speculation the bank alone is scanned,
and it is worth 1.0 $/MWh at the extrapolation grade; the records
device holds both at the basis.

The coil account prices the chamber's coils along the plasma's own
expansion: the field they must hold falls from the compression value at
the burn section as the plasmoid expands down the chamber, so coil cost
grows only as the cube root of chamber length, while the expansion
volume that sets the recoverable fraction grows with radius squared.
The design search therefore trades length for radius, and every
optimized device is a fat panel-wall chamber. The same pricing makes
the coil account fall with the field at a fixed bank, 14.2 to 11.4
M$/module from 22 to 50 T on the extrapolation device's shot and
chamber and 25.4 to 20.6 on the speculation device's, because the
compressed flux volume the adiabat integrates over shrinks as B^-2 and
so does the conductor that holds it; the magnetic pressure the
structure must carry rises as B^2 at the same time, and the model has
no term for it. That is why the field is bounded in the constraint set
rather than left to the cost model, and why the 30 to 50 T designs are
a reported sensitivity rather than devices: the reconciliation band
brackets the extrapolation device within 24.5-33.5 $/MWh and the
speculation device within 10.9-12.9 at 1 GWe, and a coil above the
basis is outside both. The field reads the other way as well: at a 10
T reactor point, with its rate re-solved for the 2.98 s burn its shot
then needs (12 modules at 0.32 Hz), the speculation device reads 23.3
$/MWh.

The burn mix and the firing rate are set together by constraint 8, and
at the basis field, where every device sits, the bound is what shapes
the cheap machines. The deuterium-rich mix (dd_frac 0.85) breeds more
He-3 than it burns, so on the He-3 bill alone it would be the optimum
everywhere. Its plasma is power-sparse, though: at 22 T its breakeven
time is 138 ms at four nines of recovery and 206 ms at three, against
126 ms at the 0.80 mix, 104 ms at the 0.70 mix and 65 ms at Helion's
mix, and the burn its shot needs does not fit between shots at the rate
each grade's grant
would allow in the fewest modules. Fired at their grants, the
deuterium-rich designs at the extrapolation grade read 26.5 $/MWh at a
duty of 1.62, and the rule excludes them; the records design is the
narrowest case, a 1.01 s burn against the 1.01 s period at 0.985 Hz,
and the search carries it a hair under the 1 Hz grant. The same burn
fits at a lower rate in more modules, and the search prices that trade
at every mix.

The trade reads one way everywhere: each added module costs more than
the slower bank saves. At the extrapolation device's shot, chamber and
mix the rate ladder reads 26.5 $/MWh at the 3 Hz grant (4 modules at
2.32 Hz, duty 1.44, excluded), 29.1 at the 6 modules at 1.55 Hz that
first fit the 0.62 s burn, and 37.3 at 12 modules at 0.79 Hz: the bank
is swapped less often and the derived availability climbs from 0.920 to
0.929, but each module adds about 1.4 $/MWh of hardware. The optimum at
every mix is therefore the fewest modules whose rate fits the burn, and
the mix trade is a trade between the He-3 a richer mix breeds and the
modules its longer burn needs. At the extrapolation grade the best
design per mix runs from 44.5 $/MWh at the He-3-rich preset (the
Polaris bank in 5 modules at 2.82 Hz; every other mix takes the doubled
bank) through 37.4 at Helion's mix (3 modules at 2.68 Hz) to a minimum
of 29.1 at dd_frac 0.80 (6 at 1.55), with the deuterium-rich end 0.5
behind it at 29.6 (7 at 1.37): the deuterium side beats Helion's mix by
8.3 $/MWh, and that last step to 0.85 costs one more module than the
He-3 it breeds pays for. At the records grade the step runs the other
way, 115.3 at 0.80 (24 modules at 0.98 Hz) against 112.1 at 0.85 (25 at
0.985), because at three nines of recovery the He-3 the loop wastes is
dearer.

At speculation the same bound governs, on a bank four times Polaris's.
The 200 MJ bank quadruples the cap on one burn section's fusion power
at a given mix (1.0 GW at the 0.70 mix, against 250 MW on the Polaris
bank), so two modules carry the gigawatt where seven would be needed on
Polaris's bank, and the best design per mix runs from 13.0 $/MWh at
the He-3-rich preset (a single 500 MJ module in a 15 m x 1.5 m chamber
on the Polaris bank at 2.67 Hz, at a duty of 0.76 and no tritium
plant) through 12.8 at the 3:1 mix, 12.6 at Helion's (a single 800 MJ
module on the 200 MJ bank at 1.93 Hz) and 12.3 at 0.60 (3 modules at
1.81 Hz) to a minimum of 11.6 at 0.70 (2 at 1.67), with 0.80 and 0.85
at 12.0 (5 modules at 1.43 and 1.46 Hz on the 100 MJ bank): the
deuterium-rich end sits 0.4 behind the device because its 0.68 s burn
needs five modules against the 0.70 mix's two, more hardware than the
He-3 it breeds pays for at 0.5 M$/kg. The rate rule costs the
speculation device 1.0 $/MWh against the best design at the grant (a
500 MJ single module on the Polaris bank at the deuterium-rich mix,
3.53 Hz, duty 9.4, excluded at 10.6), 2.6 at the extrapolation grade
against the best at-grant design, and nothing at the records grade,
whose at-grant design is the device itself. What a higher field would
do to this trade is the sensitivity above: at 50 T the breakeven time
is 5.2 times shorter, the cap on one burn section rises to 2.1 GW at
the deuterium-rich mix, and a single 30 m module carries the gigawatt
with its panel wall binding before the duty does; that design is 1.4
$/MWh cheaper and excluded by its coil.

What the cheap machines still buy is He-3: the extrapolation device's
fuel line is 2.6 $/MWh at the ledger's 2 M$/kg (43 kg/yr bought), and
the speculation device buys 44 kg/yr at 0.5 M$/kg (a 0.9 $/MWh fuel
line, of which He-3 is 0.8). The prices are entries Section 5.1 shows
no market supports. The larger consequence of running deuterium-rich is
the tritium every device stores (Section 5.1), and the duty: the
records and extrapolation devices fire at 96 to 100% of the bound and
the speculation device at 86%, with nothing in the period reserved for
exhaust, refill and recharge.

The mix is a fuel-price result rather than a physics one. At the
ledger's He-3 prices breeding beats buying at every grade, and with
He-3 free the ranking inverts: at the extrapolation grade the He-3-rich
preset wins at 20.3 $/MWh and the deuterium-rich end comes last at
28.2, against 44.5 and 29.6 when He-3 is priced; at speculation the
He-3-rich preset wins at 8.5 (6.5 at the park), a single 300 MJ module
on the Polaris bank firing at 4.47 Hz with no tritium plant, against
13.0 priced (`scripts/he3_scan.py`). A He-3-rich plasma burns fast
enough that the duty bound leaves room, at duties of 0.20 and 0.76 at
the two grades.

The records device sits 6.2 $/MWh above Helion's requirements, 112.1
against 105.9, on one claim: Helion's fourth nine of per-pulse fuel
recovery, reverted to the JET-supported three nines. At Helion's own
configuration that claim is worth about 47 $/MWh, because Helion's mix
breeds less He-3 than it burns and keeps buying (Section 5.2 derives
the multiplier); the records device escapes most of it by running at
the deuterium-rich end, in 25 modules at 0.985 Hz, where the store
covers most of the need. The other unrecorded claim, the shot, has no
record value to revert to; both devices grant it. Both are also
dominated by scheduled replacement: the entire shot-cycled recovery
chain is replaced on the capacitor-life schedule, about 17 times over a
60-year life at the 1e8-shot record.

![The evidence ladder](figures/fig1_ladder.svg)

*Figure 1: The four devices at 1 and 3 GWe, one machine per evidence
grade, each bar split into the overnight cost recovered straight-line
over the book life (blue), the cost of money, interest during
construction and on the capital (orange), and O&M, fuel and scheduled
replacement (grey). Cost of capital 7% real at the records and Helion
devices, 5% at extrapolations, 3% at speculation; book life 60, 60, 80,
80 years.*

The two cheaper devices differ in kind. The extrapolation device changes
what is bought, each entry a labeled step beyond a record with a
physical argument behind it; the speculation device changes the prices
and the ceilings, none with a mechanism behind it, and takes the bank
to four times Polaris's. The
tornado below is drawn from the extrapolation device because its
entries are the ones a measurement could confirm or refute; the anatomy
after it is drawn from the speculation device because that is the
floor.

One-at-a-time reversion from the extrapolation device ranks the levers:

| parameter reverted | LCOE ($/MWh) | delta ($/MWh) |
|---|---|---|
| cap_shot_lifetime -> 1e8 shots | 64.5 | +35.4 |
| dhe3_dd_frac -> 0.49, Helion's mix, with its 0.23 radiated fraction | 41.4 | +12.3 |
| fuel_recovery -> 0.999 (JET-analog; the reverted point overruns its period, duty 1.24) | 39.6 | +10.5 |
| interest_rate -> 0.07 (financing) | 37.2 | +8.1 |
| max_f_rep -> 1 Hz (10 modules at 0.94 Hz against the device's 6 at 1.56) | 34.6 | +5.5 |
| e_driver_mj -> 50 MJ, the Polaris bank, at the design-basis gain in the device's own chamber (12 modules) | 32.1 | +3.0 |
| eta_dec -> 0.85 | 31.4 | +2.3 |
| construction_time_yr -> 5 yr | 30.9 | +1.9 |
| eta_pin -> 0.95 (driver wall-plug) | 29.7 | +0.7 |
| lifetime_yr -> 60 | 29.7 | +0.6 |
| wall_dpa_tolerance -> 20 | 29.3 | +0.2 |
| f_rad -> 0.23 (Helion's own; below the 0.27 floor at dd_frac 0.80, so not a coherent point) | 28.7 | -0.4 |

The capacitor cycle life dominates at 35 $/MWh; then come the burn mix
(12 $/MWh: reverted to Helion's mix the device breeds less He-3 and
buys more), the fourth nine of fuel recovery (10), the cost of capital
(the grey financing bar, 8.1), the firing rate (5.5), the bank (3.0 in
the device's own chamber, 1.0 against the best design on the Polaris
bank), the inductive efficiency (2.3), the 3.25-year build (1.9), the
driver wall-plug efficiency (0.7) and the 80-year book life (0.6 $/MWh
against the 60 years below it). The fourth nine is worth 10 here,
against 47 at Helion's own mix, because the extrapolation device breeds
most of its He-3: at three nines the loop wastes 71% of what it buys
(Section 5.2), but it buys little, and the plasma, with less recycled
He-3, burns for 0.89 s instead of 0.62, over the 0.72 s period at 1.39
Hz, so the reverted point also leaves the coherent set. The rate row is
not the grant's worth: the device already fires at 1.56 Hz under its 3
Hz grant, so reverting the ceiling to the records grade's 1 Hz costs
the step from 6 modules to 10, and the grant above 1.6 Hz is worth
nothing to this device. The reverted radiated fraction, Helion's 0.23,
sits below the floor the 0.80 mix requires, so that row is not a
coherent point. f_pdv, the field and the shot are absent from the
table: the extrapolation stack leaves f_pdv at the basis 0.80 under a
cap that does not bind, the field is held at the basis by the coil, and
the shot's record value is no plant. The conversion efficiencies, once
capped as a composite, are worth little at the margin.

![Tornado from the extrapolation device](figures/fig2_tornado.svg)

*Figure 2: One-at-a-time reversion of each extrapolation entry to its
record value, from the 29.1 $/MWh extrapolation device, the bank's
reversion to Polaris's 50 MJ among them. The grey bar is the financing
entry, every other bar is physics or engineering; the reversions that
leave the coherent set are marked in the table.*

At the speculation device the capacitor-driver narrative is spent (the
bank is 41 M$ of a 721 M$ reactor account across its two modules) and
the cost floor is carried by site and support infrastructure, by
operations and by the capital of the modules themselves (there is no
turbine island; the heat-rejection and electrical-plant accounts below
are not a steam cycle):

| item | M$ | $/MWh (approx) |
|---|---|---|
| buildings (CAS21) | 282 | 1.2 |
| CAS50, the decommissioning provision and supplementary capital | 201 | 0.8 |
| heat rejection + electrical plant (CAS24-26) | 169 | 0.7 |
| fuel handling (C220500), of which the tritium-plant allowance 123 | 163 | 0.7 |
| first wall of two 15 m chambers (C220101) | 106 | 0.4 |
| vacuum and exhaust (C220106), of which per-pulse pumping 76 | 95 | 0.4 |
| direct-conversion power electronics (C220109) | 86 | 0.4 |
| adiabat-priced coils (C220103), with no structure for the 193 MPa they cycle to | 51 | 0.2 |
| driver capacitor bank (C220107) | 41 | 0.2 |
| O&M (CAS70), levelized in constant dollars | 36/yr | 4.4 |
| fuel (CAS80): 44 kg/yr of He-3 at 0.5 M$/kg | 7/yr | 0.9 |
| annualized capital, all-in (3% real cost of capital, 80 years) | 51/yr | 6.3 |

![What carries the cost floor](figures/fig3_anatomy.svg)

*Figure 3: Capital accounts carrying the speculation device. The driver
bank, the concept's narrative centerpiece, is the smallest bar; site
infrastructure dominates the capital, and O&M is seven tenths of the
annualized capital in the levelized cost.*

## 5. The He-3 fuel cycle is the load-bearing subsystem

**The finding.** The cycle rests on three things, and the ladder prices
each: He-3 at a price no one has paid at tonne scale, which every
device breeds most of on site and buys the rest of (a 2.6 $/MWh fuel
line at the extrapolation device at 2 M$/kg, 0.9 at the speculation
device at 0.5 M$/kg); a site inventory of tritium held while it decays,
two thirds of a tonne at Helion's own device, 2.6 tonnes at the records
device, 1.2 at the extrapolation device and 0.7 at speculation, 170 to
650 times ITER's authorization; and per-pulse fuel recovery at four
nines, the fourth of which is worth 10 $/MWh at the extrapolation
device, 47 at Helion's own mix and 3 at the speculation device. A
fourth condition is not a price but a fact about the pulse: the store
works only if bred tritium does not burn before it is pumped out, which
holds at Helion's stated pulse and fails at the burn the granted shot
needs, at every grade.

The fuel cycle is the one in Helion's patent [15], whose operating table
also fixes the burn point: a plasma with He3/D = 0.158 at 70 keV and 22
T (Helion's stated compression field of more than 15 T is consistent
with that density through pressure balance), radiating 23% of its fusion
power as bremsstrahlung and releasing 6% as neutrons. Slough [16],
citing the same patent, restates that mix as the self-sustained cycle's
limit, He-3 at roughly 16% of the fuel, and puts the D-He3 gain at equal
FRC conditions a factor of 240 below D-T's, which is why the reactor he
designs in that paper is D-T. The D-D reactions are what close the
cycle. Half of them produce a He-3 atom directly (the prompt branch);
the other half produce a triton (the tritium branch), which is pumped
out with the exhaust after the pulse, separated, and stored on getter
beds until it decays into He-3 (12.3 yr half-life). Almost none of the
tritium burns before it is removed (dhe3_f_T = 0 in the basis). The
plant therefore has no lithium anywhere, and its tritium plant is an
exhaust-processing and storage plant.

### 5.1 The He-3 balance and the observed market

The tritium branch, half of the D-D events, produces 0.5 dd_frac tritium
nuclei per primary event, so a quarter of them at Helion's mix and a
third to two fifths at the optimized devices; each decays to He-3 on the
17.8 yr mean life of that 12.3 yr half-life. That He-3 is fuel for the
reactor: it replaces purchased He-3 atom for atom, and from an empty
store the replacement builds as 1 - e^(-t/17.8 yr), reaching its full
value against the 1 - dd_frac the plant burns only at equilibrium. This
work levelizes the credit over the book life at the grade's rate,
applied as a scaling of the He-3 price outside the cost model; the
prompt bred He-3 counts as extra burns, not as supply, and the store's
own capital, inventory and licensing are priced regardless (constraint
4).

A deuterium-rich plant therefore buys He-3 only until the store covers
its need, which takes its levelized purchase to a fifth to a third of
the perpetual one across the three optimized devices (0.22 at the
records device, 0.23 at extrapolations, 0.31 at speculation). A mix
that breeds less than it burns keeps buying, and Helion's own device
pays 79% of the perpetual bill. That exposure is what the mix is worth:
bought in perpetuity at the ledger price, He-3 would cost Helion's
device 5.2 $/MWh more, the records device 35.3, the extrapolation
device 8.2 and the speculation device 1.9, and free it would save them
19.7, 9.7, 2.5 and 0.8, which would also change the mix (Section 7).

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

At the 2011 allocation the extrapolation device reads 32.2 $/MWh against
58.5 for Helion's mix in the same chamber at the same rate, and at the
commercial spot 51.4 against 172.3. Breeding most of its He-3 makes it
far less exposed than Helion's mix, because it buys only during the
build-up, but not indifferent: the spot adds 22 $/MWh. The
deuterium-rich end would be nearer indifference still, at one more
module. The credit is coupled to the burnup closure of Section 5.2,
because the decay return exists only if the tritium survives the pulse.

One consequence: a kilogram of He-3 bought by the speculation device
becomes 2.1 M$ of electricity at that device's own price, and 5.4 M$ at
the extrapolation device, but it sold for 4.5 M$ at the 2011 allocation
and sells for 19-22 M$ today, so an early breeding plant earns more
selling He-3 into the thin cryogenics and quantum market than burning
it, until fleet supply floods that market.

The store that breeding implies is large. Every module breeds tritium at
half its D-D rate, which across a plant is 38 kg/yr at Helion's mix and
41 to 145 kg/yr at the optimized devices, the records device highest on
both its mix and its module count, and each of the speculation
device's two modules breeding 0.4 mg per shot. Store-for-decay then
fixes the equilibrium inventory at the production rate times the 17.8
yr mean life, which is 0.67 tonnes of tritium at Helion's device and
0.7 to 2.6 tonnes at the others. A tonne is 1e10 Ci, about 320 kW of continuous
decay heat, 250 times ITER's site authorization and 35 times the world's
civilian tritium stock. The inventory is intrinsic to breeding at this
scale; shipping it to a central fuel facility relocates it (and can hold
the reactor site near ITER-class inventory with weekly pickups) but
cannot shrink it. No device escapes it: the He-3-rich preset, which
breeds 4.6 kg/yr and stores 80 kg as a single 1 GWe module at the
speculation grade, buys its He-3 and reads 13.0 $/MWh against the
device's 11.6. This is why the ledger refuses the "near-zero licensing"
claim alongside the fuel credit, holds O&M at its baseline, and treats
the tritium-plant allowance as more likely low than high.

The alternative to breeding in the power module is a dedicated
deuterium breeder, a pure-D module of the same grade with its bred He-3
and tritium pumped out every pulse, priced per kilogram delivered as
module ownership plus a throughput-sized tritium plant plus its net
power at the device's own LCOE (`scripts/breeder_loop.py`; the tables
are in the ledger). It reads 2.0 M$/kg at the records grade, at the
ledger's 2.0, cannot be reached at the Helion device (6.6 M$/kg),
charges about 0.8 M$/kg at extrapolations, where the device at that
price reads 27.6 $/MWh against its 29.1 at the ledger's 2 M$/kg, and 0.3
at speculation against the ledger's 0.5 (11.3 against 11.6), a breeder
module of the device's own kind delivering 52 kg/yr; it relocates the
tritium inventory rather than shrinking it.

### 5.2 Fuel recovery and the burnup closure

Helion's cycle depends on pumping the bred tritium out of the exhaust
before it burns, so whether the shot and the fuel plan are compatible is
a question about pulse length, not a modeling choice. The
store-and-decay idealization (dhe3_f_T = 0: no bred triton burns
in-plasma) is therefore a claim about pulse kinetics. A triton born
mid-pulse sits in a deuterium-rich plasma at fusion temperature for the
rest of the burn, and D-T reactivity is 27-87x D-D at 70-20 keV [19], so
each unit of D burnup burns 14-43x as much of the bred tritium. The
per-pulse deuterium burnup pins the integrated exposure x_DD = -ln(1 -
f_D) = n_D <sigma v>_DD tau, and averaging over triton births gives the
thermalized-limit in-pulse tritium burn

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
inter-pulse removal.

Over a sub-millisecond pulse the burnup is 1.2-2.5e-4 and the in-pulse
tritium burn 0.2-0.3%, so dhe3_f_T = 0 satisfies its floor with two
orders of margin. Every device sits at that point. The closure scales
with the density, so a higher field would move a device along it: at
50 T, the top of the field sensitivity, the density is 5.2 times the
patent's, the per-pulse burnup at the stated pulse 6.2e-4, and the
floor on the in-pulse tritium burn 0.8%, just inside the 1% tolerance
constraint 5 allows (at 55 T the zero would be flagged). Figure 4 draws
the closure against burn time at the patent point. At the 0.3 to 0.7 s
the design-basis shot needs under constraint 7, a thermalized triton
burns 58 to 80% before removal, and the speculation device's 512 MJ
shot from its 200 MJ bank, the same gain at the same point, needs the
same burn; the store-and-decay cycle and the granted shot are coherent
together only under prompt triton loss, the branch the burnup axis of
Figure 5 prices at high burnup.

![The burnup closure against burn time](figures/fig4_tritium_burn.svg)

*Figure 4: The burnup closure against burn time at the patent point (n_D
0.75e22 m^-3, 70 keV): the per-pulse deuterium burnup (orange, dashed)
and the in-pulse burn of a bred triton in the thermalized limit (blue).
The bands mark Helion's stated pulse, the patent's own confinement time,
and the burn the design-basis shot (128 MJ from the 50 MJ bank) and the
speculation device's shot (512 MJ from its 200 MJ bank, the same gain)
need under constraint 7 across x_s 0.5 to 0.85. The store-and-decay
basis holds at the stated pulse; at the burn the granted shot needs,
most bred tritium burns in the pulse unless it is promptly lost.*

Fuel therefore resides in the machine of order a thousand pulses before
burning, and the model carries the per-pulse pair burn_fraction = 1.2e-4
and burn_fraction_he3 = 4.1e-4 at the basis field (He-3 burns 3.3x
faster per pass), scaled as B^2 with the density at a device's own
field, with species-resolved recycle losses in the fuel account. A
recirculating nucleus faces the same race every pass, burn with
probability bf (burn_fraction) or leak with probability 1 - fr
(fuel_recovery), so its ultimate fate is the geometric series bf / (1 -
fr (1 - bf)), set by the ratio of the two rates:

| species (per-pass burn) | fr = 0.99 | fr = 0.999 | fr = 0.9999 |
|---|---|---|---|
| deuterium (1.2e-4 at 22 T) | 1.2% burns | 11% burns | 55% burns |
| He-3 (4.1e-4 at 22 T) | 3.9% burns | 29% burns | 80% burns |
| He-3 (2.1e-3 at 50 T, the top of the field sensitivity) | 17% burns | 68% burns | 96% burns |

At the four-nines basis, 80% of the He-3 burns and 20% is lost, while
deuterium splits nearly evenly between burning and leaking; at three
nines the loop is primarily a fuel-disposal device, wasting 71% of its
He-3, and at two nines nearly everything leaks. A higher field would
tilt the race toward burning (96% of the He-3 burns at four nines and
68% at three at 50 T), which is part of what the field sensitivity of
Section 4 is worth. Tritium sees no geometric series at all: it is
extracted to the store on its first pass, so separation loss hits it
once, not compounded. With per-pulse reprocessing the unburned-fuel
repurchase multiplier at the basis field is 84x at per-pass recovery
0.99, 9.3x at 0.999, and 1.8x at 0.9999 (17x, 2.6x and 1.2x at 50 T). A
deuterium-rich plant is self-sufficient in He-3 at three nines, so there
the multiplier bites only on the He-3 bought while the store builds up
(6.7 $/MWh on the deuterium-rich extrapolation stack in Helion's
chamber); at Helion's mix, which breeds less than it burns, the fourth
nine is worth 47 at Helion's device, 10 at the extrapolation device,
which breeds most of its own, and 3 at the speculation device, whose
0.70 mix breeds a little less of it (Section 4). Hertz-rate isotope
separation and the tritium plant are the price of the store itself.

The JET figure behind the three-nines record is an analogy, not a
per-pass measurement: campaign retention measures co-deposited wall
inventory over many recycles, not single-transit loss, and none of the
separation slip a per-pulse reprocessing plant adds [13].

Both species' per-pass burn fractions derive from the same n tau, so the
axis is swept coherently: burn_fraction_he3 scales with burn_fraction at
the fixed 70 keV reactivity ratio (3.3x). Figure 5 shows the speculation
device's LCOE along that axis under both triton fates, at exhaust
recovery 0.99, 0.999, and 0.9999. At the patent burn point the per-pulse
fuel recovery sets the cost almost alone: 11.6 $/MWh at four nines,
14.6 at three, 45.1 at two at the speculation device, which breeds most
of its He-3 and buys the rest, and 106, 155 and 639 at Helion's own
device, which buys more.

Toward higher compression density the recovery requirement relaxes:
above per-pulse burnup of about 1e-3 the three- and four-nines curves
converge, near 11.0 $/MWh on the thermalized branch and on a floor of
10.9 on the prompt-loss one. With 70% of its events D-D the device is
where the triton fate matters: the thermalized branch turns up past
burnup 0.003 as the tritium burn grows (4 to 90%), to 14.3 $/MWh at
burnup 0.3, so the triton-fate question reopens exactly where the
recovery question closes. The prompt-loss branch is a floor on the fuel
side rather than an operating point, because the same orbit loss that
spares the tritium also removes the fusion protons, about four fifths
of the charged fusion energy at the deuterium-rich mix. Per-pulse
exhaust pumping is priced across the axis and peaks at the patent burn
point (106 M$ across the extrapolation device's six modules; 76 M$
across the speculation device's two).

![The burnup axis](figures/fig5_burnup.svg)

*Figure 5: LCOE at the speculation device across the per-pulse
burnup axis under the two triton fates and three exhaust-recovery
grades; the patent-density basis (dotted, grey), where every device
sits, is the hardest point for fuel recovery.*

### 5.3 Neutron damage and the unshieldable throat

The replacement rate of the wall, coils, and vessel shell follows from
the D-T-equivalent neutron wall load and a dpa tolerance. The load
counts 10 dpa per MW yr/m^2 in Fe-based structure, with the 2.45 MeV D-D
flux folded at 0.4; the tolerance is taken at 20 dpa, the edge of the
irradiation database for reduced-activation ferritic-martensitic (RAFM)
steel, and at 50 dpa, the DEMO-class design target. The event carries
both the wall and the close-coupled coils (106 + 51 M$ across the
speculation device's two modules, 211 + 85 across the extrapolation
device's six), since nothing 0.10 m behind the wall outlives it. At the
patent basis the spectrum is pure 2.45 MeV D-D, and the
14-MeV-equivalent load follows the mix and the duty: the records and
extrapolation devices carry 0.12 and 0.13 MW/m^2, which prices at +0.3
to 2.7 $/MWh at 50 to 20 dpa at the records device and +0.2 to 1.4 at
the extrapolation device, and the speculation device, whose two 15 m
walls carry a plant's neutrons at the 0.70 mix, 0.15 MW/m^2, +0.3 to
1.1. The damage story reopens in the high-burnup counterfactuals: if
the reactor-point density pushes per-pulse burnup toward the 0.1 regime
with thermalized tritons, the all-in gap between prompt-loss and
thermalized reaches 8 to 18 $/MWh at the speculation device and 16 to
32 at the extrapolation device, and on the
extrapolation stack's divertor-class wall (2.5 M$/m^2, at Helion's
chamber) thermalized high-burnup replacement is prohibitive (+52 to
+134 $/MWh). Keeping the tritium out of the burn is therefore cheap
insurance at the patent burn point and worth double digits off it.

Shielding cannot buy the machine out of this, because a pulsed inductive
plant pays per pulse for every cubic meter of flux volume between coil
and plasma: W = (B^2/2mu0) x annulus volume, recovered only at the
composite efficiency. The 50 MJ driver at the 22 T basis field implies
about 0.26 m^3 of compression-section flux volume, and the speculation
device's 200 MJ at the same field about 1.0 m^3; a 0.4 m shield under
the compression coil multiplies the swept annulus by more than an order
of magnitude, growing the store to several hundred MJ per pulse and
dissipating tens of MJ per pulse at composite 0.90: order 100 MW or more
of recirculating loss at the devices' rep rates (and the energy per
cubic meter of annulus would be five times higher at 50 T than at 22
T, one more cost the field sensitivity does not carry). Shielding is
affordable only where the guide field is low, far from the burn
section, so the coils nearest the burn are sacrificial,
ceramic-insulated, and on the wall-replacement schedule. The burn is
also localized near the compression section, so the uniform-cylinder
audit understates the local load; a localized audit would roughly
double the damage costs, and at the speculation device, each of whose
two 15 m chambers carries 855 MW of fusion power, the localization is
half the plant's.

The replacement schedule has a structural threshold. The wall and coils
are 156 M$ of the speculation device's 721 M$ reactor account (296 of
1855 M$ at the extrapolation device); their levelized replacement
outspends the account's own capital service when the interval falls
below about 6.0 years at the speculation grade's 3% real cost of capital
(2.9 years at 7%) and 3.0 years at the extrapolation grade's 5%. At the
patent basis the derived interval is well above that: 35 years at the
speculation device and 41 at the extrapolation device at 50 dpa, 17 at
the records device at the 20 dpa database edge. The consumable-core
regime (1-3 year intervals, a fifth of the module's value swapped
near-annually) belongs to the high-burnup thermalized counterfactual,
where the core becomes a swappable cartridge and the plant a
manufacturing operation with a waste stream this study does not price;
the compression coil's fatigue schedule (constraint 9) is a third
member of the shot-cycled family that none of this prices, at the
basis field itself.

## 6. The yield a shot can return, and what the circuit recovers of it

**The finding.** Helion's public numbers cannot all be true at once: the
shot Orion needs, the plasma conditions in the patent, and the stated
millisecond pulse are mutually inconsistent. At that pulse the fusion
energy a shot can return is a fraction of what the circuit loses in
firing it, and the shot Orion needs implies a burn hundreds of times
longer than Helion describes. That makes the disclosed design point
incoherent, not the machine impossible: something Helion has not said
publicly would have to close the gap, or the patent no longer describes
the machine.

Every number in this work grants Helion's shot. This section bounds what
a shot can return from the plasma's own energy and burn time, shows
what the compression field and the bank do to that bound, then sets
out the two further bounds on what the circuit recovers of it, the share
of the driver energy that thermalizes and the expansion ratio the
chamber allows, beyond the composite cap of constraint 2 that stops the
two conversion efficiencies from being counted twice. A three-shot
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
Lawson time.

**What the bound reads at Helion's numbers.** The patent point is n_D
0.75e22 m^-3, He3/D 0.158, 70 keV and 22 T. At Bosch-Hale rates its
breakeven time is 86 ms with thermalized electrons, and 3.7 times
shorter if the electrons could be held at a tenth of the ion
temperature. They cannot be held there: the ion-electron equilibration
time at that density is about 1 ms, well inside the breakeven time [21].
Helion's stated pulse is hundreds of microseconds to milliseconds [2],
and against it the bound reads three ways. A 1 ms burn returns 0.2 to
0.4 MJ from the 50 MJ bank across x_s 0.5 to 0.85, against the 2.5 MJ
the circuit loses per shot even at the ladder's best inductive
efficiency, eta_dec 0.95. The design-basis 128 MJ shot needs a burn of
0.3 to 0.7 s, three to seven hundred times the stated pulse; both scale
inversely with the number of modules Orion turns out to be (Section 2).

**What the field and the bank do to it.** At beta = 1 the plasma
pressure is the magnetic pressure, so at the patent's ion temperature
the density scales as B^2 and the fusion power density as B^4, while
the energy density scales as B^2: the breakeven time falls as B^-2, 86
ms at 22 T at the patent mix and 5.2 times shorter at 50 T. The bank
does nothing to the burn a shot of a given gain needs (gain / chi x
breakeven time), but at a fixed module power a larger shot is fired
less often, so the duty falls as the bank grows. The speculation device
fires 512 MJ shots from a 200 MJ bank at the basis field, the
design-basis gain: a 1 ms burn there returns 0.7 to 1.7 MJ across x_s,
and the shot needs the same 0.3 to 0.7 s burn as the design-basis shot,
three to seven hundred times the stated pulse. A higher field would
shorten the burn a shot of a given gain needs by the density ratio, 5.2
at 50 T, and a larger gain would lengthen it back; no field closes the
distance to Helion's pulse in kind, because the shot's burn is set by
the gain and the breakeven time, and a gain of 2.56 is 2.56 breakeven
times over chi at any field.

The bound also reproduces the co-founder's own D-T design: Slough [16]
quotes a gain of 9.1 on the FRC energy over a 2 to 5 ms transit at 34.8
T and 15 keV, and at that point's breakeven time the same arithmetic
gives a 3.4 ms burn. This is constraint 7, and it is why the shot is a
graded claim rather than a shared basis; every point the scripts
evaluate carries the burn time its shot implies at x_s 0.7, at its own
field and at the mix it actually burns, purchased He-3 plus the bred
He-3 that recycles: 0.32 s at Helion's device, whose accounting holds
He3/D at 0.22 with the recycled He-3 against the patent's purchased
0.16, 1.01 s at the records device (dd_frac 0.85 with three nines of
recovery), 0.62 s at the extrapolation device (0.80 on the doubled
bank) and 0.51 s at the speculation device's 512 MJ shot (0.70 on a
bank four times Polaris's).
The same two papers bear on constraint 1: their independent
reconstructions find Helion's fusion-to-bremsstrahlung ratio 3.6 to 9
times too favorable [22] or about an order of magnitude [21], which
would put the radiated fraction well above the floor constraint 1
enforces.

**The duty bound.** The burn a shot implies must also fit inside the
pulse period, since one burn section holds one plasmoid and the next
shot cannot fire while the last is still burning: burn time x
repetition rate <= 1, constraint 8, with the limit at the hard bound of
1.0 and nothing reserved for exhaust, refill and recharge. Because the
implied burn is proportional to the yield, the product is the module's
fusion power over the cap chi E_del / breakeven time, and it is
evaluated at x_s 0.7, where a coil-filling FRC holds half the driver
energy. Across the span the reading changes with chi:

| design (1 GWe) | dd_frac | field, bank | breakeven time (ms) | fusion power per module (MW) | cap at x_s 0.7 (MW) | duty at x_s 0.5 / 0.7 / 0.85 |
|---|---|---|---|---|---|---|
| citable records | 0.85 | 22 T, 50 MJ | 206 | 126 | 126 | 1.71 / 1.00 / 0.73 |
| Helion's requirements | 0.49 | 22 T, 50 MJ | 65 | 128 | 401 | 0.55 / 0.32 / 0.23 |
| extrapolations | 0.80 | 22 T, 100 MJ | 126 | 398 | 413 | 1.65 / 0.96 / 0.70 |
| speculation | 0.70 | 22 T, 200 MJ | 104 | 855 | 1000 | 1.46 / 0.86 / 0.62 |
| extrapolations, deuterium-rich end | 0.85 | 22 T, 100 MJ | 138 | 351 | 378 | 1.59 / 0.93 / 0.68 |
| speculation, deuterium-rich end | 0.85 | 22 T, 100 MJ | 138 | 375 | 378 | 1.70 / 0.99 / 0.72 |

The records and extrapolation devices sit at 96 to 100% of the bound at
the reference and the speculation device at 86%, because the search
fires each in the fewest modules whose rate fits its burn, and they
pass with room at the fat-FRC edge (x_s 0.85); every optimized device
would be excluded at x_s 0.5, where a thin FRC holds only 30% of the
driver energy. Helion's own device, at 128 MW per module, passes across
the span. The cap is doubled by the doubled bank at the extrapolation
device and quadrupled by the 200 MJ bank at the speculation device, to
1.0 GW for one burn section at the 0.70 mix, which is why two modules
carry the gigawatt there and one cannot. The deuterium-rich end's
designs, one module slower than the extrapolation device and three
more than the speculation device, sit at 93 and 99%. Because the rate
is a design choice, the bound excludes no mix; it sets the fewest
modules each mix needs, and Section 4 prices the ladder. The bound is a
statement about the fusion power one burn section can carry, not about
the shot alone: the bank raises it in proportion, and a higher field
would raise it as B^2, which is the whole of what the field
sensitivity of Section 4 buys.

**Driver thermalization.** The same chi bounds the recovery of the
driver energy itself. The thermalized share can only return through the
same expansion channel as the fusion heat, at f_pdv, while the model
recovers all of it at the flat inductive efficiency. The uncaptured loss
is worth +1.5 to +3.5 $/MWh at the extrapolation device across the x_s
span, +0.1 to +0.3 $/MWh at the speculation device (668 MW of
circulating driver power against the extrapolation device's 933, at a
lower price per MWh), and order +10 $/MWh at the low-gain Helion
device; it is carried in the reconciliation bands.

**The expansion-ratio bound.** Constraint 6 caps f_pdv at the
adiabatic-stroke bound 1 - (V_i/V_f)^(2/3), with V_i = E_del/(B^2/2mu0):
about 0.26 m^3 at 50 MJ and 22 T, 0.52 m^3 at the extrapolation
device's 100 MJ, and 1.0 m^3 at the speculation device's 200 MJ, since
the bank grows the flux volume (a higher field would compress it as
B^-2). Applied per point: the records device's 10 m x 0.75 m chamber
caps f_pdv at 0.940 and the extrapolation device's 10 m x 1.5 m at
0.962, both above the 0.80 those grades claim; the speculation device's
15 m x 1.5 m chamber caps it at 0.954, above the stack's claimed 0.947
by 0.007, so the claim stands, narrowly, and the composite the device
runs at is 0.95 x 0.947 = 0.90, its cap exactly. The large chamber buys
expansion ratio, not merely wall area, and recovery cannot be improved
without more chamber; a higher field would buy the same ratio in less
chamber. About a fifth
of the expansion work is axial, against the end-field gradient [23];
constraint 6 counts the whole volume stroke, as Helion's own burn-cycle
framework does, and whether the end circuits return that fifth is a
design question the shot sequence below measures.

The cycle is Diesel-type with an Atkinson over-expansion (burn at
roughly constant pressure, then expand further than the compression
stroke), the framing of Helion's own burn-cycle analysis [24], which
quotes about 60% for a constant-pressure burn and above 90% for optimal
cycles. Two published figures sit against it. Nicolas et al. [22], whom
Helion's FAQ cites for recovery "exceeding 95%", give that number only
as an ideal Carnot-form bound and set it aside on the thin-cycle
argument. Slough [16], the co-founder whose patent supplies the fuel
cycle, derives 40% as the most an ejected FRC can return in a
flux-conserving expansion chamber, where it comes to rest holding 1.5 pV
of thermal energy against the field it has compressed, and states that
an FRC does not free-expand. That is his own recovery topology, not the
discharged compression coil this work's f_pdv assumes, so it is carried
as a risk row rather than a cap: at f_pdv 0.4 the extrapolation device
reads 49.4 $/MWh (+20.3) and the speculation device 19.0 (+7.4). There
is no Carnot exemption in any of this: cycle form, the compression and
expansion ratios, and the entropy of the deliberately irreversible
merging set the efficiency, which is what the composite cap encodes.

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

## 7. What would reach $10/MWh, and what stands in the way

One device reaches the target, and only as a park. Two controlled
sweeps at the speculation device (constant gain, constant wall loading,
driver and chamber scaled with module power) separate module count from
plant size, scaling the device's own 500 MWe module. **Module count at
fixed plant size is nearly free**: across a twentyfold range in module
size, from a single 1 GWe module at 11.5 $/MWh through the device's two
at 11.6 to 20 of 50 MWe at 13.6, the whole spread is 2.1 $/MWh, because
buildings, supplementary capital, and balance of plant price plant
totals; the only modularity tax is per-module fixed items, biting below
about 100 MWe. **Standalone plant size is expensive**:

| plant | LCOE ($/MWh) | $/kW | dominant penalties |
|---|---|---|---|
| 1 GWe (the device, two modules) | 11.6 | 1549 | - |
| 250 MWe (one module) | 18.4 | 2339 | fixed site buildings, staffing^0.5 |
| 50 MWe (one module) | 44.2 | 6422 | O&M 17.2 $/MWh (staffing law), 141 M$ of buildings |

The standalone penalty is about 141 M$ of fixed site buildings
calibrated on fission-class analogs, the P^0.5 staffing law of the Idaho
National Laboratory sodium-fast-reactor basis [25], and the absence of
any fleet-learning term on equipment, so this concept's economics live
in power parks, and the 50 MWe module of Helion's gigafactory framing
[4] is a manufacturing choice the model neither rewards nor punishes at
park scale.

As a park the full speculation stack reads 9.4 $/MWh at 3 GWe (11.6 at
1 GWe, 1.6 above the target), 0.6 under it, and it does so on a coil
that exists: the park sits at the patent's 22 T, on the coil the basis
already needs, and nothing in it rests on a field this work cannot
price. Two things bring it there. The first is financing: at the
design-basis 7% real cost of capital the same machine reads 16.2 $/MWh
(19.5 at 1 GWe), so the 3% real cost of capital, sovereign-class money
with no mechanism behind it, is worth 6.8 $/MWh at the park, eleven
times the margin under the target. The second is the bank, four times
Polaris's and worth 0.7 $/MWh: with the bank at Polaris's value the
same stack sits at the target (10.1 at 3 GWe, 12.4 at 1 GWe), so the
park crosses on the bank, and on the bank alone. The figure moves with
the availability it is derived at, 10.0 $/MWh at the model default of
0.85 and 9.2 at a pinned 0.95. It also grants Helion's gain, as every
number here does, carries the wall-and-coil replacement of Section 5.3,
and fires its two burn sections at 86% of the duty bound with nothing
else reserved in the period. What would take the coherent park further,
none of it in the evidence base at any grade:

- **He-3 at zero cost**: worth 0.8 $/MWh at the device's own mix (10.8
  at 1 GWe), and 8.5 $/MWh at 1 GWe and 6.5 at 3 GWe with the design
  search re-run at zero price, which moves it to the He-3-rich preset
  (a single 300 MJ module on the Polaris bank, firing at 4.47 Hz with
  no tritium plant). The He-3 price is the whole of the mix: at the
  ledger's 0.5 M$/kg the park breeds, at zero it buys, and the two read
  2.9 $/MWh apart.
- **Gas-class site and decommissioning analogs** (about 2.0 $/MWh at 1
  GWe, the whole of the buildings and CAS50 lines): not defensible for
  this machine, which carries a tritium plant and stores 0.7 tonnes of
  tritium. The He-3-rich single-module design that would make the case,
  with no tritium plant and 80 kg stored, reads 13.0 $/MWh at 1 GWe, so
  it would need the analog and more.
- **A real fleet-learning term** on equipment, anchored beyond the fleet
  the nth-of-a-kind (NOAK) constants already assume, or it double
  counts: the only mechanism that rewards the mass-produced small-unit
  strategy at all.
- **A coil for a higher field.** The field is scanned to 50 T and
  excluded at every grade by the coil. The best design the coil bound
  alone excludes reads 10.9, 10.5 and 10.2 $/MWh at 30, 40 and 50 T
  (8.6, 8.2 and 7.9 at the park), so a higher field would be worth up
  to 1.4 $/MWh at either plant size, and the model prices the coil that
  would deliver it below the 22 T coil, 20.6 against 25.4 M$ per module
  in the speculation device's chamber, because the adiabat it
  integrates over shrinks. A structure that cycles to 1 GPa ten billion
  times is not in the model or in any record, and the 193 MPa the basis
  coil cycles to is itself at or above the copper-alloy gigacycle band:
  a fatigue basis for the compression coil, at the basis field first,
  is the open item that would make a higher field a priced one.

## 8. Conclusions

Four devices on one architecture read 112.1, 105.9, 29.1 and 11.6 $/MWh
at 1 GWe by evidence grade. One stack reaches the target: the
speculation park at 3 GWe reads 9.4 $/MWh, 0.6 under it, on a 3% real
cost of capital worth 6.8 and on a driver bank four times Polaris's
worth 0.7, at the patent's 22 T on the coil that point already needs;
at Polaris's bank it sits at the target. The floor is carried by site
infrastructure, operations and the capital of the modules, not the
driver bank, and at the extrapolation device the capacitor cycle life
is the largest lever at 35 $/MWh, with the burn mix, the fourth nine of
per-pulse fuel recovery and the cost of capital at 8 to 12 and the
doubled bank at 3.

The compression field and the driver bank scale with the plant, as
Helion's CEO advised, and the study scans both. The bank is a
procurement: doubled at the extrapolation grade it halves the module
count at the same burn and is worth 1.0 $/MWh, and quadrupled at
speculation it is worth 0.7. The field is physics: at beta = 1 the
density scales as B^2, so the breakeven time and the burn a shot needs
fall as B^-2 and the fusion power one burn section can carry rises as
B^2, and at 50 T a single 30 m module would deliver 1 GWe with its
panel wall binding before the duty bound does. The scan prices that
design, at 10.2 $/MWh (7.9 at the park), 1.4 under the device, and
excludes it, at every grade, on the coil: the 22 T coil already cycles
at or above the copper-alloy gigacycle band, no higher fatigue basis is
sourced anywhere in this work, and the cost model's coil account, which
prices conductor and no structure, falls with the field rather than
rising, so the bound has to be a bound in the constraint set. The
field above the basis is therefore reported as what it would be worth,
on a coil this work cannot price, and no device rests on it.

Every optimized device burns deuterium-rich, against the He-3-rich mix
Helion publishes, and that is a fuel-price result rather than a physics
one: with He-3 free the search returns to the He-3-rich preset at every
grade. Helion's own mix is the one choice in this ladder that pays only
if He-3 is close to free. At the prices charged here it sits 8.3 $/MWh
behind the optimum at the extrapolation grade and 1.0 behind it at
speculation; only at zero price does its half of the mix grid win. The
published design therefore presumes a He-3 supply the public record
does not describe, whether an unpublished source, a separation path
cheaper than the one priced here, or a cost of self-supply this work
puts too high.

Every number grants Helion's gain, 128 MJ from a 50 MJ bank, which at
the patent point needs a burn of 0.3 to 0.7 s against Helion's stated
pulse of a millisecond or less, and the speculation device's 512 MJ
shot from its 200 MJ bank is the same gain and the same burn; over such
a burn most bred tritium fuses before it can be removed, so the fuel
cycle and the shot hold together only under prompt triton loss. The
burn must also fit between shots, and that bound sets the fuel mix and
the firing rate together: the deuterium-rich mixes that breed most or
all of their He-3 are the cheapest at every grade once the plant is
allowed to fire slower in more modules than its granted rate ceiling
would need, so the records, extrapolation and speculation devices run
deuterium-rich at 0.985, 1.56 and 1.67 Hz in 25, 6 and 2 modules, at
86 to 100% of the duty bound, with nothing in the period left for
exhaust, refill and recharge, and the rate ceilings granted above that
are worth nothing to them. The tonne-class tritium store is escaped by
no device: 0.67 tonnes at Helion's own, 2.6 at the records device, 1.2
and 0.7 at the two cheap ones; and a per-pass fuel recovery of four
nines that no per-pass measurement supports is worth 10 $/MWh at the
extrapolation device, 47 at Helion's mix, and 3 at the speculation
device.

Of the data Helion does not report (Section 2), the shot gates the whole
plant, the recovery chain 2 to 20 $/MWh at the extrapolation grade, and
the fuel-cycle data tens of $/MWh at every mix; the capacitor cost at
cycle life, a supplier's datum, gates tens; and the compression field of
the reactor point, with the coil that holds it, gates the last 1.4
$/MWh and whether the basis coil itself survives its cycle count.

The speculation stack is jointly heroic: 0.1 $/J capacitors with
1e10-shot life contradict the derating physics that connects capacitor
cost to life, the composite recovery sits at its theory optimum with
zero margin, and the 512 MJ shot is a burn of 0.3 to 0.7 s, three to
seven hundred times Helion's stated pulse. The floor is conditional on
the field (a 10 T reactor point, with the burn it implies and the 12
modules that fit it, reads 23.3 $/MWh) and on the discharged-coil
recovery topology (Slough's 40% ceiling adds 7.4 $/MWh at speculation
and 20 at extrapolations); the neutron-damage costs are more likely
low than high, and the one conservatism, no thermal bottoming, is worth
-3.9 $/MWh at the extrapolation device.

The constructive reading: the floor, conditional on the gain, is low by
any thermal-plant standard, the architecture of factory modules, park
deployment and swappable cores fits the failure modes the physics
imposes, and the data that would move the ladder from speculation to
evidence, the shot first among them and the compression coil's cycle
life beside it, are Polaris data.

## Reproducibility

Everything here is in the study repository at
[github.com/1cFE/helion_pulsed_frc_tea](https://github.com/1cFE/helion_pulsed_frc_tea):
the four evidence stacks in `config/`, the scripts in `scripts/` that
produce every number, every figure and the HTML, LaTeX and PDF
renderings of this page and the ledger (the README says what each one
does), the evidence ledger, the adversarial review, the capacitor
evidence, and the Helion slide and FAQ captures. The cost model is
`1costingfe` at commit 44434d9. The regression tests pin every quoted
device at both plant sizes, every constraint, the yield and duty bounds
at each device's own field and bank, the graded field and bank grids
and the coil bound, the rate ladder the search climbs down and the
deuterium-rich end's designs, the He-3 credit and the financing ladder,
and fail loudly if the model moves under this work.

## Acknowledgements

We thank David Kirtley, Helion's co-founder and CEO, for his engagement
with this work <https://x.com/dkirtley/status/2107277032015253549>. His
comments were incorporated into this work: the compression field and
the pulsed-power bank are scanned as plant-scale design choices rather
than held at Polaris's values, with the burn point, the pulse width and
every account that depends on them following. The bank scales the
devices, doubled at the extrapolation grade and four times Polaris's at
speculation. The field is scanned to 50 T and priced at every point,
and excluded above the patent's 22 T at every grade by the compression
coil, whose pressure at the basis field already sits at or above the
copper-alloy gigacycle band and for which no higher fatigue basis is
sourced, so the higher fields are reported as what they would be worth
rather than built into any device. The results are what Sections 4, 6
and 7 report.

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
26. US Nuclear Regulatory Commission. Subsequent License Renewal,
    status as of June 2026:
    nrc.gov/reactors/operating/licensing/renewal/subsequent-license-renewal.
27. GeekWire (2025). "Helion's next big bet is manufacturing fusion
    power at scale, but tech uncertainty remains": the Omega facility
    and its roughly 2,500 capacitor units for the Orion plant.
