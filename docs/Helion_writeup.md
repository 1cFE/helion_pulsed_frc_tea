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
extrapolations, and speculation. They read 115.3, 105.9, 37.7 and 13.0
$/MWh at 1 GWe, and the speculation park reads 11.0 $/MWh at 3 GWe, so
none of the four reaches the public 1 cent/kWh target at either plant
size: the cheapest coherent machine misses it by 1.0 $/MWh, on a 3% real
cost of capital that is worth 4.4 (15.4 at 7%).

Every number grants Helion's shot, 128 MJ from a 50 MJ bank, which no
record supports and which needs a burn of 0.3 to 0.7 s against Helion's
own stated pulse of hundreds of microseconds to milliseconds; on citable
records alone the machine makes no net power. That burn also has to fit
between shots, and the bound it puts on repetition rate is what fixes
each device's fuel mix (Sections 4 and 6). The fuel cycle, not the
driver, is the load-bearing subsystem either way: the cheap devices buy
He-3 at prices no market supports (a 15 $/MWh fuel line at the
extrapolation device), and the deuterium-rich designs, Helion's own
device and the records device among them, hold a tritium store of two
thirds of a tonne to two tonnes while it decays. The data that would
move the ladder are all Polaris data, first among them the yield of a
burning shot at its measured burn time.

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
target under a rep-rate ceiling.

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
configuration is the minimum-LCOE design of a scan over shot yield (a
free parameter only at speculation, where the scan chooses it; the
records and extrapolation devices keep the design-basis shot), chamber
length and radius, wall class (constraint 3), and burn mix (seven mixes
from the He-3-rich preset to the deuterium-rich end, each on its
bremsstrahlung floor), discarding any design that violates one of the
coherence constraints below. Reconciliation then brackets each minimum
with the model gaps it cannot price internally (high-voltage DC switch
duty, the tritium-plant band, the driver-thermalization derate) and its
conservatisms (no thermal bottoming), yielding an honest band rather
than a point.

**Evidence ladder.** The plant environment is held in part and stepped
in part:

- Held at every grade: constant-dollar framing, and EPCM indirects at
  20% of direct cost [6], which the model scales with the build time (CAS30 =
  fraction x CAS20 x (construction_time_yr / 6 yr)), so the effective
  fraction is 16.7% at a 5-year build, 10.8% at 3.25 years and 8.3% at
  2.5 years.
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
  grade, 50 above it): 0.895 at the records device, 0.932 at
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

**Coherence constraints.** Eight couplings are applied to every quoted
point. Six are enforced by the scripts as checks; the seventh, derived
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
   throughput takes to 189 M$ at the extrapolation device.
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
   evaluated for the plasma at the burn point and at the mix the point
   actually burns (purchased He-3 plus the bred He-3 that recycles), so
   every quoted point carries the burn time its shot implies, and the
   shot takes each device's grade rather than serving as a shared basis.
8. A shot's implied burn must fit inside the pulse period: burn time x
   repetition rate <= 1, because one burn section holds one plasmoid and
   the next shot cannot fire while the last is still burning. The bound
   is hard at 1.0, with nothing reserved for exhaust, refill and
   recharge. Equivalently it caps one burn section's fusion power at chi
   E_del / breakeven time, which tightens as the mix turns
   deuterium-rich; Section 6 gives the cap per design and the span
   across x_s.

## 4. Results: the four devices and what carries the cost floor

| device | 1 GWe | 3 GWe | at 7% real cost of capital, 1 GWe |
|---|---|---|---|
| citable records | 115.3 | 111.0 | 115.3 |
| Helion's requirements | 105.9 | 102.1 | 105.9 |
| extrapolations | 37.7 | 34.9 | 44.3 |
| speculation | 13.0 | 11.0 | 18.2 |

LCOE in $/MWh. The at-7% column reprices each device at a 7% real cost
of capital with everything else unchanged, so the gap between it and the
1 GWe column is what the grade's cheaper money is worth: 6.6 $/MWh at
extrapolations and 5.2 at speculation. The records and Helion devices
already sit at 7%, so their two columns match. The stack and design
behind each row:

- **citable records**: fuel recovery 0.999 (JET analog); 7% real cost of
  capital, 60-year life, 5-year build; Helion's 128 MJ shot granted;
  optimum: that shot at 1 Hz in 10 m x 0.75 m panel-wall modules (24 of
  them) at dd_frac 0.80 with its tritium plant, the richest deuterium
  mix whose burn fits the 1 Hz period
- **Helion's requirements**: Helion's configuration (50 MJ driver, 20
  modules in the smallest chamber that survives the shot, Helion's mix
  (dd_frac 0.49) with its 0.23 bremsstrahlung fraction and tritium
  plant; 7% real cost of capital, 60-year life, 5-year build) granted
  its two unrecorded claims: the 128 MJ shot that delivers the 50 MWe
  module at 1 Hz (a 0.3 to 0.7 s burn at the patent point, against
  Helion's stated pulse) and fuel recovery 0.9999
- **extrapolations**: the records stack with Helion's shot (graded here
  as the patent-implied 0.3 to 0.7 s burn), plus capacitor life 1e9
  shots, a 3 Hz repetition-rate ceiling (1 Hz at the design basis), a
  purchasable divertor-class wall, fuel recovery 0.9999, 5% real cost of
  capital, the 80-year civil-works life and a 3.25-year build; optimum:
  six 15 m x 0.75 m panel-wall modules at 2.7 Hz at Helion's own mix
  (dd_frac 0.49) with its tritium plant, the richest mix whose burn fits
  that period; the 3 GWe park (17 modules) takes the 10 m x 1.5 m
  chamber, since the 15 m x 0.75 m one trips the panel wall's steady
  flux once the module count snaps
- **speculation**: the extrapolation stack, plus a 10 Hz ceiling, the
  composite recovery at its theory optimum 0.90, capacitors at 0.1 $/J
  and 1e10 shots, He-3 at 0.5 M$/kg, 3% real cost of capital, a 2.5-year
  build; optimum: 200-750 MJ of fusion yield per shot from the same 50
  MJ driver (gain 4-15; 500 MJ carried, a 1 to 3 s burn at the patent
  point and 0.28 s at its own He-3-rich mix), chosen by the scan, a
  single module in a 15 m x 1.5 m chamber at the He-3-rich preset mix
  (dd_frac 0.13) with no tritium plant; the 3 GWe park is three modules
  of the 200 MJ design at 6.8 Hz

The coil account prices the chamber's coils along the plasma's own
expansion: the field they must hold falls from the compression value at
the burn section as the plasmoid expands down the chamber, so coil cost
grows only as the cube root of chamber length, while the expansion
volume that sets the recoverable fraction grows with radius squared. The
design search therefore trades length for radius, and the minima are
short, fat chambers. Reconciliation brackets the extrapolation device
within 32.1-41.8 $/MWh and the speculation device within 12.6-13.5 $/MWh
at 1 GWe.

The burn mix is set by constraint 8 at every grade. The deuterium-rich
mix (dd_frac 0.85) breeds more He-3 than it burns, so on the He-3 bill
alone it would be the optimum everywhere. Its plasma is power-sparse,
though: its breakeven time is 138 ms at four nines of recovery and 207
ms at three, against 65 ms at Helion's mix and 15 ms at the He-3-rich
one. The burn its shot needs therefore does not fit between shots at the
rate each grade runs.

The deuterium-rich designs the rule excludes read 112.1, 26.8 and 10.6
$/MWh, at duties of 1.00, 1.87 and 9.39. The records design is the
narrowest case: a 1.02 s burn against the 1.01 s period at 1 Hz. The
search instead runs each grade as deuterium-rich as its period allows:
dd_frac 0.80 at 1 Hz, Helion's 0.49 at 2.7 Hz with six modules, and the
He-3-rich 0.13 where a single 1 GWe module carries the whole plant's
fusion power.

That costs 3.2 $/MWh at the records grade, 10.9 at extrapolations and
2.4 at speculation. What the cheap machine buys instead of breeding is
He-3: the extrapolation device's fuel line is 15.2 $/MWh at the ledger's
2 M$/kg, and the speculation device buys 76 kg/yr at 0.5 M$/kg (4.5
$/MWh), at price entries Section 5.1 shows no market supports.

The records device sits 9.4 $/MWh above Helion's requirements, 115.3
against 105.9, on one claim: Helion's fourth nine of per-pulse fuel
recovery, reverted to the JET-supported three nines. At Helion's own
configuration that claim is worth about 47 $/MWh, because Helion's mix
breeds less He-3 than it burns and keeps buying (Section 5.2 derives
the multiplier); the records device escapes most of it by running as
deuterium-rich as its 1 Hz period allows, where the store covers most
of the need. The other unrecorded claim, the shot, has no record value
to revert to; both devices grant it. Both are also dominated by
scheduled replacement: the entire shot-cycled recovery chain is
replaced on the capacitor-life schedule, about 17 times over a 60-year
life at the 1e8-shot record.

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
and the ceilings, none with a mechanism behind it. The tornado below is
drawn from the extrapolation device because its entries are the ones a
measurement could confirm or refute; the anatomy after it is drawn from
the speculation device because that is the floor.

One-at-a-time reversion from the extrapolation device ranks the levers:

| parameter reverted | LCOE ($/MWh) | delta ($/MWh) |
|---|---|---|
| fuel_recovery -> 0.999 (JET-analog; the reverted point overruns its period, duty 1.03) | 73.0 | +35.2 |
| cap_shot_lifetime -> 1e8 shots | 71.6 | +33.8 |
| max_f_rep -> 1 Hz | 47.9 | +10.2 |
| interest_rate -> 0.07 (financing) | 44.3 | +6.6 |
| eta_dec -> 0.85 (the reverted point trips the panel wall's steady flux, 2.38 MW/m^2) | 40.0 | +2.2 |
| construction_time_yr -> 5 yr | 39.2 | +1.4 |
| f_rad -> 0.23 (Helion's own, above the 0.20 floor; trips the wall's steady flux, 2.10 MW/m^2) | 38.6 | +0.8 |
| eta_pin -> 0.95 (driver wall-plug) | 38.6 | +0.8 |
| lifetime_yr -> 60 | 38.3 | +0.6 |
| wall_dpa_tolerance -> 20 | 37.8 | +0.1 |

The fourth nine of fuel recovery and the capacitor cycle life dominate,
each worth about 35 $/MWh; the rep rate follows at a third of their
weight; then come the cost of capital (the grey financing bar, 6.6
$/MWh), the inductive efficiency (2.2), the 3.25-year build (1.4) and
the 80-year book life (0.6 $/MWh against the 60 years below it). The
fourth nine is worth 35 here, against 6 at a deuterium-rich machine,
because the extrapolation device buys most of its He-3: at three nines
the loop wastes 71% of what it buys (Section 5.2), and the plasma, with
less recycled He-3, burns for 0.38 s instead of 0.32, over the 0.37 s
period at 2.7 Hz, so the reverted point also leaves the coherent set.
The burn mix does not appear as a lever: the device already burns
Helion's mix, so reverting it changes only the radiated fraction, to
Helion's 0.23. f_pdv and the shot are absent from the table: the
extrapolation stack leaves f_pdv at the basis 0.80 under a cap that does
not bind, and the shot's record value is no plant. The conversion
efficiencies, once capped as a composite, are worth little at the
margin.

![Tornado from the extrapolation device](figures/fig2_tornado.svg)

*Figure 2: One-at-a-time reversion of each extrapolation entry to its
record value, from the 37.7 $/MWh extrapolation device. The grey bar is
the financing entry, every other bar is physics or engineering; the
reversions that leave the coherent set are marked in the table.*

At the speculation device the capacitor-driver narrative is spent (the
bank is 5 M$ of a 363 M$ reactor account) and the cost floor is carried
by site and support infrastructure, by operations and by the He-3 the
machine buys (there is no turbine island; the heat-rejection and
electrical-plant accounts below are not a steam cycle):

| item | M$ | $/MWh (approx) |
|---|---|---|
| buildings (CAS21) | 254 | 1.0 |
| CAS50, the decommissioning provision and supplementary capital | 184 | 0.8 |
| heat rejection + electrical plant (CAS24-26) | 154 | 0.6 |
| vacuum and exhaust (C220106), of which per-pulse pumping 59 | 73 | 0.3 |
| direct-conversion power electronics (C220109) | 70 | 0.3 |
| first wall of the 15 m chamber (C220101) | 53 | 0.2 |
| fuel handling (C220500), no tritium plant at this mix | 40 | 0.2 |
| adiabat-priced coils (C220103) | 11 | 0.04 |
| driver capacitor bank (C220107) | 5 | 0.02 |
| O&M (CAS70), levelized in constant dollars | 34/yr | 4.1 |
| fuel (CAS80): 76 kg/yr of He-3 at 0.5 M$/kg | 37/yr | 4.5 |
| annualized capital, all-in (3% real cost of capital, 80 years) | 36/yr | 4.4 |

![What carries the cost floor](figures/fig3_anatomy.svg)

*Figure 3: Capital accounts carrying the speculation device. The driver
bank, the concept's narrative centerpiece, is the smallest bar; site
infrastructure dominates the capital, and the purchased He-3 and O&M
match it in the levelized cost.*

## 5. The He-3 fuel cycle is the load-bearing subsystem

**The finding.** The cycle rests on three things, and the ladder prices
each: He-3 at a price no one has paid at tonne scale, which the cheap
devices buy (a 15 $/MWh fuel line at the extrapolation device at 2
M$/kg, 4.5 at the speculation device at 0.5 M$/kg) or breed on site; a
site inventory of tritium held while it decays, two thirds of a tonne
at Helion's own device, 2.2 tonnes at the records device and 1 to 1.4
tonnes at the deuterium-rich designs, 170 to 550 times ITER's
authorization; and per-pulse fuel recovery at four nines, the fourth of
which is worth 35 $/MWh at the extrapolation device and 47 at Helion's
own mix. A fourth condition is not a price but a fact about the pulse:
the store works only if bred tritium does not burn before it is pumped
out, which holds at Helion's stated pulse and fails at the burn the
granted shot needs.

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
nuclei per primary event: 0.42 at the deuterium-rich mix, 0.40 at the
records device's dd_frac 0.80, 0.24 at Helion's mix, which the
extrapolation device shares, and 0.07 at the speculation device's
He-3-rich mix; each decays to He-3 on the 17.8 yr mean life of that 12.3
yr half-life. That He-3 is fuel for the reactor: it replaces purchased
He-3 atom for atom, and from an empty store the replacement builds as 1
- e^(-t/17.8 yr), reaching its full value against the 1 - dd_frac the
plant burns only at equilibrium. This work levelizes the credit over the
book life at the grade's rate, applied as a scaling of the He-3 price
outside the cost model; the prompt bred He-3 counts as extra burns, not
as supply, and the store's own capital, inventory and licensing are
priced regardless (constraint 4).

A deuterium-rich plant therefore buys He-3 only until the store covers
its need, about eight years, which takes its levelized purchase to a
fraction of the perpetual one: 30% at the records device, whose dd_frac
0.80 breeds more than it burns but whose 7% rate weights the build-up
years most. A mix that breeds less than it burns keeps buying: 79% at
Helion's own device and 75% at the extrapolation device, both at
Helion's mix, and 95% at the He-3-rich speculation device. Bought in
perpetuity at the ledger price instead, He-3 would cost the four devices
37.4, 5.2, 5.0 and 0.2 $/MWh more; free, it would save them 16.2, 19.7,
15.1 and 4.4 at their own mixes, and it would change the mix (Section
7).

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

At the 2011 allocation the extrapolation device reads 55.7 $/MWh at its
own mix, Helion's, and 67.3 at the 3:1 mix; at the commercial spot,
169.5 and 225.2. A deuterium-rich machine would be nearly indifferent
to the He-3 price, 28.2 at the allocation and 38.9 at the spot in the
same chamber, because it buys only during the build-up, but its burn
does not fit that chamber's 2.7 Hz period; the machines that fit are
not indifferent. The credit is coupled to the burnup closure of Section
5.2, because the decay return exists only if the tritium survives the
pulse.

One consequence: a kilogram of He-3 bought by the speculation device
becomes 1.4 M$ of electricity at that device's own price, and 3.8 M$ at
the extrapolation device, but it sold for 4.5 M$ at the 2011 allocation
and sells for 19-22 M$ today, so an early breeding plant earns more
selling He-3 into the thin cryogenics and quantum market than burning
it, until fleet supply floods that market.

The store that breeding implies is large. Every module breeds tritium
at half its D-D rate. Helion's own device breeds 0.07 mg per shot, 38
kg/yr across its 20 modules, from 104 MW of plant neutron power; the
records device, at dd_frac 0.80 in 24 modules, 0.18 mg per shot and 122
kg/yr from 340 MW; the extrapolation device, at Helion's mix in six
modules, 31 kg/yr from 84 MW. The deuterium-rich designs constraint 8
excludes breed 56 kg/yr at the speculation grade (0.55 mg per shot) and
78 kg/yr on the extrapolation stack in Helion's chamber (211 MW of
neutron power). Store-for-decay fixes the equilibrium inventory at
production rate times the 17.8 yr mean life: 0.67 tonnes of tritium at
Helion's device, 2.2 at the records device, 0.55 at the extrapolation
device, 1.0 to 1.4 at the deuterium-rich designs; a tonne is 1e10 Ci,
about 320 kW of continuous decay heat, 250x ITER's site authorization
and 35x the world's civilian tritium stock. The inventory is intrinsic
to breeding at this scale; shipping it to a central fuel facility
relocates it (and can hold the reactor site near ITER-class inventory
with weekly pickups) but cannot shrink it. Only the He-3-rich
speculation device escapes it, at 4.6 kg/yr and 80 kg stored, by buying
its He-3. This is why the ledger refuses the "near-zero licensing" claim
alongside the fuel credit, holds O&M at its baseline, and treats the
tritium-plant allowance as more likely low than high.

The alternative to breeding in the power module is a dedicated
deuterium breeder, a pure-D module of the same grade with its bred He-3
and tritium pumped out every pulse, priced per kilogram delivered as
module ownership plus a throughput-sized tritium plant plus its net
power at the device's own LCOE (`scripts/breeder_loop.py`; the tables
are in the ledger). It reads 2.4 M$/kg at the records grade, near the
ledger's 2.0, cannot be reached at the Helion device (6.6 M$/kg),
charges about 1.4 M$/kg at extrapolations, where the device at that
price reads 32.8 $/MWh against its 37.7 at the ledger's 2 M$/kg, and 0.5
at speculation, the ledger's own entry (12.9 against 13.0); it relocates
the tritium inventory rather than shrinking it.

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
orders of margin. Figure 4 draws the closure against burn time. At the
0.3 to 0.7 s the design-basis shot needs under constraint 7, a
thermalized triton burns 58 to 80% before removal, and at the
speculation shot's 1 to 3 s, 88 to 95%; the store-and-decay cycle and
the granted shot are coherent together only under prompt triton loss,
the branch the burnup axis of Figure 5 prices at high burnup.

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
is self-sufficient in He-3 at three nines, so there the multiplier
bites only on the He-3 bought while the store builds up (6.7 $/MWh on
the deuterium-rich extrapolation stack in Helion's chamber); at
Helion's mix, which breeds less than it burns, the fourth nine is worth
47 at Helion's device and 35 at the extrapolation device (Section 4).
Hertz-rate isotope separation and the tritium plant are the price of
the store itself.

The JET figure behind the three-nines record is an analogy, not a
per-pass measurement: campaign retention measures co-deposited wall
inventory over many recycles, not single-transit loss, and none of the
separation slip a per-pulse reprocessing plant adds [13].

Both species' per-pass burn fractions derive from the same n tau, so the
axis is swept coherently: burn_fraction_he3 scales with burn_fraction at
the fixed 70 keV reactivity ratio (3.3x). Figure 5 shows the speculation
device's LCOE along that axis under both triton fates, at exhaust
recovery 0.99, 0.999, and 0.9999. At the patent burn point the per-pulse
fuel recovery sets the cost almost alone, and harder than at a
deuterium-rich machine because the He-3 the loop wastes is bought: 13.0
$/MWh at four nines, 21.7 at three, 108 at two.

Toward higher compression density the recovery requirement relaxes:
above per-pulse burnup of about 3e-3 the three- and four-nines curves
converge near 11.8 $/MWh. At the He-3-rich mix the two triton fates
coincide to within 0.1 $/MWh, since only 13% of the events are D-D and
the device breeds 4.6 kg/yr of tritium; the triton-fate question lives
on the deuterium-rich counterfactual, where the same sweep converges
near 10.0 $/MWh on the prompt-loss branch and the thermalized branch
turns up past burnup 0.01 as the tritium burn grows (13-90%), so there
the question reopens exactly where the recovery question closes. The
prompt-loss branch is a floor on the fuel side rather than an operating
point, because the same orbit loss that spares the tritium also removes
the fusion protons, about four fifths of the charged fusion energy at
the deuterium-rich mix. Per-pulse exhaust pumping is priced across the
axis and peaks at the patent burn point (59 M$ per module at the
speculation device, 78 at the deuterium-rich design).

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
both the wall and the close-coupled coils (53 + 11 M$ at the
speculation device), since nothing 0.10 m behind the wall outlives it.
At the patent basis the spectrum is pure 2.45 MeV D-D, and the
14-MeV-equivalent load follows the mix: 0.03 MW/m^2 at the He-3-rich
speculation device, where the replacement cost is negligible (under
0.1 $/MWh at 20 dpa), 0.07 at the extrapolation device (+0.04 to 0.4
$/MWh at 50 to 20 dpa), 0.11 at the records device (+0.2 to 1.9) and
0.20 at the deuterium-rich speculation design (+0.3 to 1.2). The damage
story reopens only in the high-burnup counterfactuals: if the
reactor-point density pushes per-pulse burnup toward the 0.1 regime
with thermalized tritons, the all-in gap between prompt-loss and
thermalized reaches 8-16 $/MWh at a deuterium-rich machine, and on the
extrapolation stack's divertor-class wall (2.5 M$/m^2, at Helion's
chamber) thermalized high-burnup replacement is prohibitive (+52 to
+135 $/MWh). Keeping the tritium out of the burn is therefore free
insurance at the patent burn point and worth double digits off it.

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

The replacement schedule has a structural threshold. The wall and coils
are 63 M$ of the speculation device's 363 M$ reactor account (243 of
1322 M$ at the extrapolation device); their levelized replacement
outspends the account's own capital service when the interval falls
below about 5 years at the speculation grade's 3% real cost of capital
(2.4 years at 7%) and 3.4 years at the extrapolation grade's 5%. At the
patent basis the derived interval is far above that: 156 years at the
speculation device and 73 at the extrapolation device at 50 dpa, 19 at
the records device at the 20 dpa database edge. The consumable-core
regime (1-3 year intervals, a sixth of the module's value swapped
near-annually) belongs to the high-burnup thermalized counterfactual,
where the core becomes a swappable cartridge and the plant a
manufacturing operation with a waste stream this study does not price.

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
a shot can return from the plasma's own energy and burn time, then sets
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
The speculation shot needs 1 to 3 s.

The bound also reproduces the co-founder's own D-T design: Slough [16]
quotes a gain of 9.1 on the FRC energy over a 2 to 5 ms transit at 34.8
T and 15 keV, and at that point's breakeven time the same arithmetic
gives a 3.4 ms burn. This is constraint 7, and it is why the shot is a
graded claim rather than a shared basis; every point the scripts
evaluate carries the burn time its shot implies at x_s 0.7 and at the
mix it actually burns, purchased He-3 plus the bred He-3 that recycles:
0.32 s at Helion's device, whose accounting holds He3/D at 0.22 with the
recycled He-3 against the patent's purchased 0.16, 0.89 s at the records
device (dd_frac 0.80 with three nines of recovery), 0.32 s at the
extrapolation device and 0.28 s at the speculation device's 500 MJ
He-3-rich shot. The same two papers bear on constraint 1: their
independent reconstructions find Helion's fusion-to-bremsstrahlung ratio
3.6 to 9 times too favorable [22] or about an order of magnitude [21],
which would put the radiated fraction well above the floor constraint 1
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

| design (1 GWe) | dd_frac | breakeven time (ms) | fusion power per module (MW) | cap at x_s 0.7 (MW) | duty at x_s 0.5 / 0.7 / 0.85 |
|---|---|---|---|---|---|
| citable records | 0.80 | 182 | 126 | 144 | 1.50 / 0.88 / 0.64 |
| Helion's requirements | 0.49 | 65 | 128 | 401 | 0.55 / 0.32 / 0.23 |
| extrapolations | 0.49 | 65 | 345 | 401 | 1.48 / 0.86 / 0.63 |
| speculation | 0.13 | 15 | 1334 | 1759 | 1.30 / 0.76 / 0.55 |
| records, deuterium-rich | 0.85 | 207 | 126 | 126 | 1.72 / 1.00 / 0.73 |
| extrapolations, deuterium-rich | 0.85 | 138 | 351 | 188 | 3.20 / 1.87 / 1.36 |
| speculation, deuterium-rich | 0.85 | 138 | 1767 | 188 | 16.1 / 9.39 / 6.85 |

The three optimized devices pass at the reference with margins of 12 to
24% and with room at the fat-FRC edge (x_s 0.85), and all three would be
excluded at x_s 0.5, where a thin FRC holds only 30% of the driver
energy; Helion's own device, at 128 MW per module, passes across the
span. The deuterium-rich records design fails at the reference by half
a percent and is admitted only at the fat edge; the deuterium-rich
extrapolation and speculation designs fail across the whole span. The
bound is a statement about the fusion power one burn section can carry,
not about the shot alone.

**Driver thermalization.** The same chi bounds the recovery of the
driver energy itself. The thermalized share can only return through the
same expansion channel as the fusion heat, at f_pdv, while the model
recovers all of it at the flat inductive efficiency. The uncaptured loss
is worth +1.7 to +3.9 $/MWh at the extrapolation device across the x_s
span, under 0.1 $/MWh at the speculation device, and order +10 $/MWh at
the low-gain Helion device; it is carried in the reconciliation bands.

**The expansion-ratio bound.** Constraint 6 caps f_pdv at the
adiabatic-stroke bound 1 - (V_i/V_f)^(2/3), with V_i = E_del/(B^2/2mu0),
about 0.26 m^3 at 50 MJ and 22 T. Applied per point: the extrapolation
device's 15 m x 0.75 m chamber caps f_pdv at 0.954, above its claimed
0.80, and the speculation device's 15 m x 1.5 m chamber caps it at
0.982, above the claimed 0.947. The large chamber buys expansion
ratio, not merely wall area, and recovery cannot be improved without
more chamber. About a fifth of the expansion work is axial, against the
end-field gradient [23]; constraint 6 counts the whole volume stroke, as
Helion's own burn-cycle framework does, and whether the end circuits
return that fifth is a design question the shot sequence below measures.

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
reads 68.8 $/MWh (+31.0) and the speculation device 21.5 (+8.5). There
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

No stack reaches the target, and the closest approach is a park. Two
controlled sweeps at the speculation device (constant gain, constant
wall loading, driver and chamber scaled with module power) separate
module count from plant size. **Module count at fixed plant size is
nearly free**: a park of 500 MWe modules reads 12.7 $/MWh against the
single 1 GWe module's 13.0 $/MWh (the adiabat-priced coils reward
smaller compressed volumes; 250 MWe modules read 12.8), and even 50 MWe
modules cost only six tenths of a dollar more (13.6), because buildings,
supplementary capital, and balance of plant price plant totals; the only
modularity tax is per-module fixed items, biting below about 100 MWe.
**Standalone plant size is expensive**:

| plant | LCOE ($/MWh) | $/kW | dominant penalties |
|---|---|---|---|
| 1 GWe | 13.0 | 1089 | - |
| 250 MWe | 19.2 | 1692 | fixed site buildings, staffing^0.5 |
| 50 MWe | 41.6 | 4887 | O&M 17.1 $/MWh (staffing law), 139 M$ of buildings |

The standalone penalty is about 139 M$ of fixed site buildings
calibrated on fission-class analogs, the P^0.5 staffing law of the Idaho
National Laboratory sodium-fast-reactor basis [25], and the absence of
any fleet-learning term on equipment, so this concept's economics live
in power parks, and the 50 MWe module of Helion's gigafactory framing
[4] is a manufacturing choice the model neither rewards nor punishes at
park scale.

As a park the full speculation stack reads 11.0 $/MWh at 3 GWe (13.0 at
1 GWe), 1.0 $/MWh short of the target, and its financing is what brings
it that close: at the design-basis 7% real cost of capital the same
machine reads 15.4 $/MWh (18.2 at 1 GWe), so the 3% real cost of
capital, sovereign-class money with no mechanism behind it, is worth
4.4 $/MWh at the park, more than four times the remaining gap. The park
holds its figure at the derived availability of 0.93 (11.5 $/MWh at the
model default of 0.85, 10.9 at 0.95), with Helion's shot granted, as for
every number here (its 200 MJ pulses are a burn of half a second to a
second at the patent point and 0.11 s at their own He-3-rich mix), and
the wall-and-coil replacement of Section 5.3 adds nothing measurable at
the He-3-rich mix. The deuterium-rich speculation design would cross:
10.6 $/MWh at 1 GWe and 8.4 as a 3 GWe park of three 200 MJ modules at
9 Hz; constraint 8 excludes it at a duty of 9.4 and 9.6, its burn ten
times the period between shots. What would take the coherent park
across, none of it in the evidence base at any grade:

- **He-3 at zero cost**: worth 4.4 $/MWh at the device's own mix (8.6 at
  1 GWe), and with the design search re-run at zero price 8.5 $/MWh at
  1 GWe and 6.5 at 3 GWe (300 and 200 MJ shots in the same 15 m x 1.5 m
  chamber at 4.5 and 6.8 Hz, no tritium plant). The He-3 price is the
  whole distance: at the ledger's 0.5 M$/kg the park misses by 1.0, at
  zero it clears by 3.5.
- **Gas-class site and decommissioning analogs** (about 1.8 $/MWh at 1
  GWe, the whole of the buildings and CAS50 lines): defensible for this
  machine, which carries no tritium plant and stores 80 kg of tritium,
  in a way it is not for the deuterium-rich designs or the records and
  extrapolation devices, whose tonne-class inventories argue the other
  way.
- **A real fleet-learning term** on equipment, anchored beyond the fleet
  the nth-of-a-kind (NOAK) constants already assume, or it double counts:
  the only mechanism that rewards the mass-produced small-unit strategy at
  all.

## 8. Conclusions

Four devices on one architecture read 115.3, 105.9, 37.7 and 13.0 $/MWh
at 1 GWe by evidence grade. No stack is under the target: the
speculation park at 3 GWe reads 11.0 $/MWh, and a 3% real cost of
capital rather than physics takes it that close. The floor is carried by
site infrastructure, operations and purchased He-3, not the driver bank,
and at the extrapolation device the fourth nine of per-pulse fuel
recovery and the capacitor cycle life are the largest levers, each worth
three times the repetition rate.

Every number grants Helion's shot, 128 MJ from a 50 MJ bank, which at
the patent point needs a burn of 0.3 to 0.7 s against Helion's stated
pulse of a millisecond or less; over such a burn most bred tritium fuses
before it can be removed, so the fuel cycle and the shot hold together
only under prompt triton loss. The burn must also fit between shots,
and that bound, not the He-3 bill, sets the fuel mix: the
deuterium-rich mix that breeds more He-3 than it burns would be the
cheapest at every grade (8.4 $/MWh as a 3 GWe park), but its
power-sparse plasma burns for longer than the period between shots, so
the cheap machine runs each grade as deuterium-rich as its period
allows, Helion's own mix at the extrapolation grade and the He-3-rich
preset at speculation, and buys He-3 at prices no market supports. The
tonne-class tritium store is not escaped, only moved: 0.67 tonnes at
Helion's own device, 2.2 at the records device; and a per-pass fuel
recovery of four nines that no per-pass measurement supports is worth
35 $/MWh at the extrapolation device.

Of the data Helion does not report (Section 2), the shot gates the whole
plant, the recovery chain 2 to 31 $/MWh at the extrapolation grade, and
the fuel-cycle data tens of $/MWh at every mix; the capacitor cost at
cycle life, a supplier's datum, gates tens.

The speculation stack is jointly heroic: 0.1 $/J capacitors with
1e10-shot life contradict the derating physics that connects capacitor
cost to life, the composite recovery sits at its theory optimum with
zero margin, and the 500 MJ shot is a burn of seconds at the patent
point. The floor is conditional on the patent-basis compression field
(a 10 T reactor point adds about 5 $/MWh, a 5 T point about 23) and on
the discharged-coil recovery topology (Slough's 40% ceiling adds 8.5
$/MWh at speculation and 31 at extrapolations); the neutron-damage
costs are more likely low than high, and the one conservatism, no
thermal bottoming, is worth -5.6 $/MWh at the extrapolation device.

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
device at both plant sizes, every constraint, the yield and duty bounds,
the deuterium-rich counterfactuals, the He-3 credit and the financing
ladder, and fail loudly if the model moves under this work.

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
