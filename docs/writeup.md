# The techno-economic floor of a Helion-class pulsed inductive fusion power plant

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
One of the best physical mechanisms for directly interacting with the plasma
is inductive recovery: a coil-driven magnetic field compresses the
plasma, and the plasma then expands against that field much as the gas
in an engine expands against a piston.
That is what Helion Energy is building, so this work takes Helion's
published design and results as its starting point and builds the
argument on them.

Helion Energy has made a compelling case to its investors, raising
more than $1.5B (the Series G round closed at $500M in September 2026
at a $15.5B post-money valuation), and has already secured a power
purchase agreement with a customer. Markedly, it stated a long-run
ambition of electricity at 1 cent/kWh ($10/MWh), and that figure is
what the 1cFE residency at Astera is set on investigating.

Helion realizes inductive recovery in a pulsed linear device: two
field-reversed configuration (FRC) plasmoids are formed, merged, and
magnetically compressed to burn, and the expanding plasma returns the
driver energy and part of the fusion energy to the capacitor banks
through the same coils.

**The findings, in brief.** Four devices share the architecture and
differ only in the evidence grade of what they are granted: citable
records alone, Helion's own requirements at face value, labeled
extrapolations, and speculation. They read 110.4, 103.9, 26.1 and 10.6
$/MWh at 1 GWe. The speculation park reads 8.4 $/MWh at 3 GWe, so the
public 1 cent/kWh target is crossed by that one stack, through 3% real
financing (14.6 at 7%) and with the wall-and-coil replacement included.
Every number grants Helion's shot, 128 MJ from a 50 MJ bank, which no
record supports and which needs a burn of 0.3 to 0.7 s against Helion's
own stated pulse of hundreds of microseconds to milliseconds; on citable
records alone the machine makes no net power. At the extrapolation
device the largest lever is the capacitor cycle life, worth three times
the next two, the deuterium-rich burn mix and the repetition rate. The
fuel cycle, not the driver, is the load-bearing subsystem, with a
tonne-class tritium store intrinsic to He-3 self-supply. The
measurements that would move the ladder are all available on Polaris,
Helion's operating prototype, first among them the yield of a burning
shot at its measured burn time.

The costing uses the `1costingfe` bottom-up cost model, built on
publicly available data and labeled extrapolations; the open-source
code is available [here](https://github.com/1cFE/1costingfe),
with detailed documentation
[here](https://files.1cf.energy/1costingfe_paper.pdf).

This work is organized as follows: Section 2 describes Helion's device
from the published material. Section 3 defines the four devices on one
plant environment, each optimized to its best cost under enforced
physics constraints. Section 4 reports the cost of each of the four
devices. Section 5 deals with the helium-3 economics, purchased fuel
being a fifth of the Helion device's LCOE at first blush, and works out
the He-3 recycling, the system that takes the unburnt fuel out between
shots and stores the bred tritium until it decays into the next He-3,
and Section 6 deals with the recovery of the driver energy through the
expanding plasma and with the bound that the plasma's energy and burn
time put on the yield of a shot, which is where Helion's shot parts from
Helion's stated pulse; each is gated by a few unmeasured plasma
properties that the developer's own next machine could resolve.

## 2. Machine basis

The machine follows Helion's published architecture at face value
(Helion Energy technology and FAQ pages; Kirtley and Milroy 2023). Two
FRC plasmoids, formed by theta-pinch field reversal in opposed formation
sections, are accelerated and merged in a central compression section,
the collision converting their directed kinetic energy into ion heat,
and magnetic compression then does the adiabatic work to burn
conditions. The pulsed-power driver is the only heater. After the burn
the plasma expands against the field, returning driver energy and
charged fusion energy to the coil circuit as work; radiated power,
undirected charged power, and neutrons are not converted.

The design-basis shot is built from three public numbers: the driver
delivers 50 MJ per pulse (the sourced Polaris capacitor bank), the plant
fires at 1 Hz, and Orion, the first plant, is to supply Microsoft at
least 50 MW, which Helion describes as at least 50 MWe after an initial
ramp-up period (Helion FAQ, June 2026). No public source says how many
machines make up that plant. This work takes it as one module; the
solved yield scales inversely with the count, while the cost at fixed
plant size is nearly indifferent to the split (Section 7). The yield per
shot is whatever makes the model turn that shot into 50 MWe at 1 Hz at
the burn point Helion's patent discloses: 128.1 MJ, a gain (fusion yield
over delivered driver energy) of 2.56. The gain is a consistency figure,
not a disclosed measurement. The chamber radius is 0.61 m, the smallest
at which a 10 m cylinder wall survives the shot under the tungsten flash
bound of 1.5 MJ/m^2 per pulse; the Helion device at 1 GWe is 20 modules
at 1 Hz, and in general a plant is an integer number of Helion-class
modules, with the repetition rate and module count solved jointly from
the net-power target under a rep-rate ceiling.

The public record as of September 2026 is D-T fusion on Polaris at 150
million degrees C, with no published yield or recovered electricity,
from Helion, which has withdrawn the term "net electricity" from its own
goals (Helion FAQ, June 2026; Axios, September 2026).

The fuel cycle is the one in Helion's patent (US 11,469,003 B2). The
patent's operating table also fixes the Helion device's burn point: a
plasma with He3/D = 0.158 at 70 keV and 22 T (Helion's stated
compression field of more than 15 T is consistent with that density
through pressure balance), radiating 23% of its fusion power as
bremsstrahlung and releasing 6% as neutrons. Slough (2025), citing the
same patent, restates that mix as the self-sustained cycle's limit, He-3
at roughly 16% of the fuel, and in the same paper leaves D-He3 for a D-T
design, putting the D-He3 gain at equal FRC conditions a factor of 240
below D-T's. The other three devices run deuterium-rich, with 85% of the
fusion events D-D, because He-3 is expensive: bred He-3 undercuts
purchased He-3 at every grade, so the design search picks that mix each
time. The D-D reactions are what close the cycle. Half of them produce a
He-3 atom directly (the prompt branch); the other half produce a triton
(the tritium branch), which is pumped out with the exhaust after the
pulse, separated, and stored on getter beds until it decays into He-3
(12.3 yr half-life). Almost none of the tritium burns before it is
removed (dhe3_f_T = 0 in the basis). The plant therefore has no lithium
anywhere, and its tritium plant is an exhaust-processing and storage
plant.

## 3. Method

**Notation.** 1costingfe model parameters keep their configuration-file
names. dd_frac (dhe3_dd_frac) is the D-D share of primary fusion events
by count, not an ion ratio (the patent's He3/D = 0.158 at 70 keV is
0.49). Three mixes are quoted: Helion's, dd_frac 0.49; the 3:1 D:He-3
mix, 0.31; and the D-rich mix, 0.85, the design search's choice at every
grade. dhe3_f_T is the fraction of bred tritium that burns in-pulse.
burn_fraction and burn_fraction_he3 (bf) are the per-pass burn
probabilities of deuterium and He-3 through the chamber, and
fuel_recovery (fr) the per-pass fraction of unburned fuel the exhaust
loop returns. f_rad is the fraction of fusion power radiated as photons.
eta_dec is the circuit efficiency of inductive recovery, f_pdv the
fraction of the plasma's expansion work that reaches the coils, and
their product the composite recovery; eta_pin is the driver's wall-plug
efficiency. f_rep and max_f_rep are the repetition rate and its ceiling;
cap_shot_lifetime is the capacitor shot life. chi is the plasma-thermal
share of the delivered driver energy and x_s the separatrix-to-coil
radius ratio.

**Cost model.** `1costingfe` is a bottom-up fusion costing framework
organized by cost account (the CAS codes in the tables below). At the
pinned commit it prices linear pulsed concepts as cylinders with the
first-wall heat flux audited against the declared wall class; counts
undirected ash, radiation, and conversion waste in the pulsed wall load;
scales the primary coolant on thermal power; prices the driver per joule
of stored energy and the inductive-conversion account on the energy the
physics path actually returns; credits the tritium store's He-3 return
against He-3 purchases, levelized over the store's build-up (a
study-side scaling of the He-3 price; Section 5.5); and schedules
replacement of the full shot-cycled recovery chain (driver bank,
recovery store, switch stack) at the capacitor shot life.

**Evidence ladder.** The plant environment is held in part and stepped
in part:

- Held at every grade: constant-dollar framing, 2.5-year construction
  (the Siemens Energy combined-cycle gas turbine block precedent), and
  indirects at 8% of direct cost (US DOE/NETL cost guidelines).
- Cost of capital, stepped: 7% real at the design basis and records
  grades (the IEA/NEA 2020 central case), 5% at extrapolations (a
  loan-guarantee blend with precedent), 3% at speculation (the IEA/NEA
  low case, sovereign-class capital). It is the one entry that is
  financing rather than technology, and Figure 1 and the ladder table's
  at-7% column keep it separate.
- Book life, stepped: 30 years through the records grade (the model
  default and the low end of the fusion literature's 30-40 year cluster;
  Böhnlein et al. 2026), 80 years from the extrapolation grade (the US
  DOE hydropower lifespan). An engineering entry: every core component
  is replaced on its own schedule and the unreplaceable structure sees
  negligible fluence.
- Availability, derived: 0.98 outside planned outages, less a routine
  outage every two years, a capacitor-bank swap at the bank's shot life,
  and a wall-and-coil changeout at the displacement-damage tolerance
  (dpa, displacements per atom; 20 dpa through the records grade, 50
  above it): 0.893 at the records device, 0.924 at speculation, at the
  top of the fusion literature's 0.75 to 0.90.

The performance entries step the same way. The records device holds one
of Helion's two unrecorded claims at its evidence-supported value,
per-pulse fuel recovery 0.999 (the fuel-retention analogy to JET with
its ITER-like wall; Brezinsek et al. 2013); the other, the shot, has no
evidence-supported value above zero, so on evidence alone the records
device makes no net power, and it is priced at Helion's shot only so
that a machine exists to cost. The Helion device grants Helion's 0.9999
(four nines) and the shot; the extrapolation and speculation stacks keep
that grant and add the labeled entries listed with the results in
Section 4, the largest being capacitor life 1e9 shots (Pacific Fusion's
derating target for its pulsed-power driver; Langtry et al. 2025). Every
entry carries a source and grade in the evidence ledger
(`docs/ledger.md`, rendered to HTML alongside this page); no
extrapolation entry is a measured record.

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

| device | 1 GWe | 3 GWe | at 7% real, 1 GWe |
|---|---|---|---|
| citable records | 110.4 | 106.1 | 110.4 |
| Helion's requirements | 103.9 | 100.2 | 103.9 |
| extrapolations | 26.1 | 23.0 | 32.7 |
| speculation | 10.6 | 8.4 | 17.8 |

LCOE in $/MWh. The at-7% column reprices each device at a 7% real cost
of capital with everything else unchanged, so the gap between it and the
1 GWe column is what the grade's cheaper money is worth: 6.7 $/MWh at
extrapolations and 7.2 at speculation (6.0 and 6.2 at 3 GWe). The
records and Helion devices already sit at 7%, so their two columns
match. The stack and design behind each row:

- **citable records**: fuel recovery 0.999 (JET analog); 7% real cost of
  capital, 30-year life; Helion's 128 MJ shot granted; optimum: that
  shot at 1 Hz in 10 m x 0.75 m panel-wall modules (25 of them), D-rich
  mix with its tritium plant
- **Helion's requirements**: Helion's configuration (50 MJ driver, 20
  modules in the smallest chamber that survives the shot, Helion's mix
  (dd_frac 0.49) with its 0.23 bremsstrahlung fraction and tritium
  plant; 7% real, 30-year life) granted its two unrecorded claims: the
  128 MJ shot that delivers the 50 MWe module at 1 Hz (a 0.3 to 0.7 s
  burn at the patent point, against Helion's stated pulse) and fuel
  recovery 0.9999
- **extrapolations**: records (with Helion's shot, here graded as the
  patent-implied 0.3 to 0.7 s burn) + capacitor life 1e9, a 3 Hz
  ceiling, a purchasable divertor-class wall, fuel recovery 0.9999, 5%
  real cost of capital and the 80-year civil-works life; optimum: seven
  10 m x 1.5 m panel-wall modules at 2.7 Hz
- **speculation**: extrapolations + 10 Hz, the composite recovery at its
  theory optimum 0.90, capacitors at 0.1 $/J and 1e10 shots, He-3 at 0.5
  M$/kg, 3% real cost of capital; optimum: 300-1000 MJ of fusion yield
  per shot from the same 50 MJ driver (gain 6-20; 500 MJ carried, a 1 to
  3 s burn at the patent point), chosen by the scan, in 30 m x 1.5 m
  chambers

The coil account prices the chamber's coils along the plasma's own
expansion: the field they must hold falls from the compression value at
the burn section as the plasmoid expands down the chamber, so coil cost
grows only as the cube root of chamber length, while the expansion
volume that sets the recoverable fraction grows with radius squared. The
design search therefore trades length for radius, and the minima are
short, fat chambers. Reconciliation brackets the extrapolation device
within 21.2-30.3 $/MWh and the speculation device within 9.9-11.6 $/MWh
at 1 GWe. The D-rich mix is the strict optimum at every grade, because
it is the mix that breeds more He-3 than it burns: the 3:1 mix (dd_frac
0.31) sits 1.9 $/MWh behind at speculation (12.5 $/MWh in a 20 m x 1.5 m
chamber) and 15 $/MWh behind at extrapolations, buying its He-3 at the
stack's price entries, which Section 5.5 shows no market supports.

The records device sits 6.5 $/MWh above Helion's requirements, 110.4
against 103.9, and the evidentiary difference is one claim: Helion's
fourth nine of per-pulse fuel recovery, which the records grade holds at
the JET-supported three nines. At Helion's own configuration that claim
is worth about 49 $/MWh: Helion's mix breeds less He-3 than it burns, so
it keeps buying, and at three nines every He-3 atom that burns costs
nine purchased, against two at four nines. The records device escapes
nearly all of it by running deuterium-rich, where the store covers the
need. The other unrecorded claim, the shot, has no record value to
revert to; both devices grant it. Both are also dominated by scheduled
replacement: the entire shot-cycled recovery chain is replaced on the
capacitor-life schedule, about eight times over a 30-year life at the
1e8-shot record.

![The evidence ladder](figures/fig1_ladder.svg)

*Figure 1: The four devices at 1 and 3 GWe, one machine per evidence
grade, each bar split into the overnight cost recovered straight-line
over the book life (blue), the cost of money, interest during
construction and on the capital (orange), and O&M, fuel and scheduled
replacement (grey). Cost of capital 7% real at the records and Helion
devices, 5% at extrapolations, 3% at speculation; book life 30, 30, 80,
80 years. The records device sits above Helion's requirements because
reverting Helion's fourth nine of fuel recovery is worth about 49 $/MWh
at Helion's mix, nearly all of which the records device's deuterium-rich
mix recovers; the other unrecorded claim, the shot, is granted to every
bar, since its record value is no plant.*

The two cheaper devices differ in kind. The extrapolation device
changes what is bought: a capacitor bank rated for 1e9 shots, a 3 Hz
cadence with the divertor-class wall that makes it admissible, a
fourth nine of per-pulse fuel recovery, and cheaper money over a
longer book life, each a labeled step beyond a record with a physical
argument behind it. The speculation device changes the prices and the
ceilings: a 10 Hz cadence, capacitors at 0.1 $/J that also last 1e10
shots, recovery at the composite's theory optimum, a shot chosen
freely by the scan, He-3 at a quarter of the ledger price, and
sovereign-class money, none with a mechanism behind it. The tornado
below is drawn from the extrapolation device because its entries are
the ones a measurement could confirm or refute; the anatomy after it
is drawn from the speculation device because that is the floor.

One-at-a-time reversion from the extrapolation device ranks the levers:

| parameter reverted | LCOE ($/MWh) | delta ($/MWh) |
|---|---|---|
| cap_shot_lifetime -> 1e8 | 62.8 | +36.7 |
| dhe3_dd_frac -> 0.49 (with its f_rad) | 38.2 | +12.1 |
| max_f_rep -> 1 Hz | 37.2 | +11.1 |
| interest_rate -> 0.07 (financing) | 32.7 | +6.7 |
| fuel_recovery -> 0.999 (JET-analog) | 32.5 | +6.4 |
| lifetime_yr -> 30 | 30.4 | +4.3 |
| eta_dec -> 0.85 | 27.9 | +1.8 |
| f_rad -> 0.23 (incoherent) | 24.6 | -1.5 |
| eta_pin -> 0.95 | 26.7 | +0.6 |
| wall_dpa_tolerance -> 20 | 26.2 | +0.2 |

The capacitor cycle life dominates; the burn mix and the rep rate follow
at a third of its weight; then come the cost of capital (the grey
financing bar, 6.7 $/MWh), the fourth nine of fuel recovery (6.4 $/MWh,
most of it the He-3 bought while the store builds up), and the 80-year
book life (4.3 $/MWh). f_pdv and the shot are absent from the table: the
extrapolation stack leaves f_pdv at the basis 0.80 under a cap that does
not bind, and the shot's record value is no plant. The conversion
efficiencies, once capped as a composite, are worth little at the margin
(an incoherent double-booking of eta_dec = 0.97 with f_pdv = 0.95 would
claim tens of $/MWh and is excluded by construction).

![Tornado from the extrapolation device](figures/fig2_tornado.svg)

*Figure 2: One-at-a-time reversion of each extrapolation entry to its
record value, from the 26.1 $/MWh extrapolation device. Red bars are
favorable reversions, the signature of anti-record entries; the grey
bar is the financing entry (cost of capital 5% to 7%), every other bar
is physics or engineering.*

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
| annualized capital, all-in (3% real, 80 years) | 49/yr | 6.1 |

![What carries the floor](figures/fig3_anatomy.svg)

*Figure 3: Capital accounts carrying the speculation device. The driver
bank, the concept's narrative centerpiece, is the smallest bar; site
infrastructure and the fuel cycle dominate.*

## 5. The He-3 fuel cycle is the load-bearing subsystem

### 5.1 Rates and inventory

At the speculation device the single module runs 7.7e20 D-D and 4.5e20
D-He3 reactions per second; only 1.4e20/s of the D-He3 burns need He-3
from beyond the prompt bred branch, and the tritium store returns
3.9e20/s once it has built up, so the module buys He-3 only during the
build-up. The module breeds tritium at half the D-D rate: 0.55 mg per
shot, 56 kg/yr. The extrapolation stack on Helion's chamber carries 211
MW of plant neutron power and breeds about 78 kg/yr. Store-for-decay
fixes the equilibrium inventory at production rate times the 17.8 yr
mean life: about 1.4 tonnes of tritium, which is 1.3e10 Ci, about 450 kW
of continuous decay heat, roughly 350x ITER's site authorization and 50x
the world's civilian tritium stock. The inventory is intrinsic to He-3
self-supply at this scale; shipping it to a central fuel facility
relocates it (and can hold the reactor site near ITER-class inventory
with weekly pickups) but cannot shrink it. This is why the ledger
refuses the "near-zero licensing" claim alongside the fuel credit, holds
O&M at its baseline, and treats the 200 M$ tritium-plant allowance as
more likely low than high.

### 5.2 The burnup closure

The store-and-decay idealization (dhe3_f_T = 0: no bred triton burns
in-plasma) is not a free choice; it is a claim about pulse kinetics. A
triton born mid-pulse sits in a deuterium-rich plasma at fusion
temperature for the rest of the burn, and D-T reactivity is 27-87x D-D
at 70-20 keV (Bosch and Hale 1992), so each unit of D burnup burns
14-43x as much of the bred tritium. The per-pulse deuterium burnup pins
the integrated exposure x_DD = -ln(1 - f_D) = n_D <sigma v>_DD tau, and
averaging over triton births gives the thermalized-limit in-pulse
tritium burn

    f_T = 1 - (1 - e^-x)/x,  x = (sv_DT / sv_DD) x_DD,

whose only physics input is the reactivity ratio. Two caveats bracket
it: a slowing 1 MeV triton passes through the D-T cross-section
resonance, so beam-target burn can only add to the estimate, while
prompt orbit loss from the plasmoid, whose separatrix sits only a few
ion gyroradii from the field null (the FRC's kinetic parameter s is
small; the triton's gyroradius is centimeter-scale at compression),
truncates it and is the one mechanism that can hold the burn below the
floor. This closure is enforced as coherence constraint 5: any quoted
point whose dhe3_f_T sits materially below the floor is flagged as
coherent only under prompt triton loss.

The basis is the patent's burn point, n_D = 0.75e22 m^-3 at 70 keV, and
Helion's stated pulse, not the patent's confinement time (0.10 to 0.16
s, three to four orders beyond any demonstrated FRC confinement, and the
reason the shot is graded rather than priced). Over a full confinement
period at that point the D burn would be 2.5-3.8% and a thermalized
triton riding it would burn 28-38%, which is the patent's own case for
inter-pulse removal; over a sub-millisecond pulse the burnup is
1.2-2.5e-4 and the in-pulse tritium burn 0.2-0.3%, so dhe3_f_T = 0
satisfies its floor with two orders of margin. Fuel therefore resides in
the machine of order a thousand pulses before burning, and the model
carries the per-pulse pair burn_fraction = 1.2e-4 and burn_fraction_he3
= 4.1e-4 (He-3 burns 3.3x faster per pass), with species-resolved
recycle losses in the fuel account. A recirculating nucleus faces the
same race every pass, burn with probability bf or leak with probability
1 - fr, so its ultimate fate is the geometric series bf / (1 - fr (1 -
bf)), set by the ratio of the two rates:

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
slip a per-pulse reprocessing plant adds (Brezinsek et al. 2013).

### 5.3 The burnup axis

Both species' per-pass burn fractions derive from the same n tau, so the
axis is swept coherently: burn_fraction_he3 scales with burn_fraction at
the fixed 70 keV reactivity ratio (3.3x). Figure 4 shows the speculation
device's LCOE along that axis under both triton fates, at exhaust
recovery 0.99, 0.999, and 0.9999. At the patent burn point the per-pulse
fuel recovery sets the cost almost alone: 10.6 $/MWh at four nines, 12.2
at three, 27.0 at two. The sweep starts at the patent burn point. Moving
right along the axis, toward higher compression density, the recovery
requirement relaxes: above per-pulse burnup of about 1e-3 the three- and
four-nines curves converge near 10.0-10.3 $/MWh on the prompt-loss
branch, and the axis minimum (10.0 $/MWh, at burnup 0.01 to 0.3) sits
about 0.6 $/MWh below the patent burn point; that branch prices the fuel
cycle only: the orbit loss that spares the tritium also removes the D-D
proton, born with the triton's momentum, and the D-He3 proton, with 2.2
times it, about four fifths of the charged fusion energy at the D-rich
mix, so it is a floor on the fuel side, not an operating point. The
thermalized branch turns up past burnup 0.01 as the tritium burn grows
(13-90%), so the triton-fate question reopens exactly where the recovery
question closes. Per-pulse exhaust pumping is priced across the axis and
peaks at the patent burn point (78 M$ per module at the floor: 8300
pumped particles per reaction).

![The burnup axis](figures/fig4_burnup.svg)

*Figure 4: LCOE at the speculation device across the per-pulse
burnup axis under the two triton fates and three exhaust-recovery
grades; the patent-density basis (dotted) is the hardest point for
fuel recovery.*

### 5.4 Neutron damage and the unshieldable throat

The replacement rate of the wall, coils, and vessel shell follows from
the D-T-equivalent neutron wall load and a dpa tolerance. The load
counts 10 dpa per MW yr/m^2 in Fe-based structure, with the 2.45 MeV D-D
flux folded at 0.4; the tolerance is taken at 20 dpa, the edge of the
irradiation database for reduced-activation ferritic-martensitic (RAFM)
steel, and at 50 dpa, the DEMO-class design target. The replacement
costs below scale inversely with the assumed tolerance; at the 200 dpa
the ARIES D-T designs assume they are a quarter of the 50 dpa values.
The event carries both the wall and the close-coupled coils (106 + 14 M$
at the speculation device), since nothing 0.10 m behind the wall
outlives it. At the patent basis the spectrum is pure 2.45 MeV D-D at a
14-MeV-equivalent load of 0.20 MW/m^2, and the replacement cost is
modest (+0.3-1.2 $/MWh at 50-20 dpa). The damage story reopens only in
the high-burnup counterfactuals: if the reactor-point density pushes
per-pulse burnup toward the 0.1 regime with thermalized tritons, the
all-in gap between prompt-loss and thermalized reaches 8-16 $/MWh, and
on the extrapolation stack's divertor-class wall (2.5 M$/m^2, at
Helion's chamber) thermalized high-burnup replacement is prohibitive
(+52 to +134 $/MWh). Keeping the tritium out of the burn is therefore
free insurance at the patent burn point and worth double digits off it.

Shielding cannot buy the machine out of this, because a pulsed
inductive plant pays per pulse for every cubic meter of flux volume
between coil and plasma: W = (B^2/2mu0) x annulus volume, recovered
only at the composite efficiency. The 50 MJ driver at the 22 T basis
field implies about 0.26 m^3 of compression-section flux volume; a
0.4 m shield under the compression coil multiplies the swept annulus
by more than an order of magnitude, growing the store to several
hundred MJ per pulse and dissipating tens of MJ per pulse at composite
0.90: order 100 MW or more of recirculating loss at the speculation
rep rate, and more than the module's output at the extrapolation
composite. The magnetized volume itself, not eddy screening, is the
irreducible cost. Shielding is affordable only where the
guide field is low, far from the burn section, so the coils nearest
the burn are sacrificial, ceramic-insulated, and on the
wall-replacement schedule. The burn is also localized near the
compression section, so the uniform-cylinder audit understates the
local load; a localized audit would roughly double the damage costs.

The replacement schedule has a structural threshold. The wall, coils,
and vessel shell are 155 of about 370 M$ of per-module reactor hardware;
replacement of the wall-and-coil event (120 M$) outspends the module's
own capital service when its interval falls below about 10 years at the
speculation grade's 3% real cost of capital (5 years at 7%). At the
patent basis (D-D spectrum, 0.20 MW/m^2 equivalent) the interval is
about 10 to 25 years at 20 to 50 dpa: a capital asset at the design
target, at the edge of one at the RAFM database edge. That interval also
enters the plant's availability (Section 3): the 84-day changeout every
25 years at the speculation device costs 0.9% of its output, against
every 17 years at the records device's 20 dpa and every 42 years at the
extrapolation device. The consumable-core regime (1-3 year intervals,
half the module's value swapped near-annually) belongs to the
high-burnup thermalized counterfactual, where the core becomes a
swappable cartridge and the plant a manufacturing operation with a waste
stream this study does not price.

### 5.5 The He-3 balance and the observed market

The prompt bred He-3 counts as extra burns, not as supply. The tritium
branch, as large at 0.42 atoms per primary event, returns He-3 from the
store as (1 - e^-t/17.8 yr) builds from startup, and this work credits
that return atom for atom against purchases, levelized over the book
life at the grade's rate. A deuterium-rich plant buys He-3 only until
the return covers its need, about eight years, and its levelized
purchase is 16% of the perpetual one at the extrapolation device, 24% at
the records device's 7% and 30 years, and 11% at speculation; Helion's
mix breeds less than it burns and keeps buying, at 82%. The store's own
capital, inventory and licensing are priced regardless (constraint 4).
Bought in perpetuity at the ledger price instead, He-3 would cost the
four devices 34, 4.5, 7.1 and 1.4 $/MWh more; free, it would save them
10.9, 20.3, 1.4 and 0.2 at their own mixes. Free He-3 also changes the
mix: with the design search re-run at zero price, the extrapolation and
speculation devices leave the D-rich mix for the He-3-rich one (dd_frac
0.13) in shorter 15 m chambers with no tritium plant, at 19.7 and 8.5
$/MWh (17.2 and 6.5 at 3 GWe), so the concession is worth 6.4 and 2.1
$/MWh at 1 GWe.

The price matters because no cheap He-3 exists. The DOE Isotope
Program's 2011 allocation was 600 $/L to federal users and 1,000 $/L to
commercial users (CRS R41419), 4.5 and 7.4 M$/kg, and prices have risen
since. The 2024-2026 transactions sit at 19-22 M$/kg on gram-to-kilogram
volumes, four to five times the 2011 allocation: spot near $2,500/L per
the Edelgas Group, Interlune's agreements with the DOE Isotope Program
and Maybell Quantum "at today's commercial market price", and TAE's
unpriced lunar supply option from Black Moon, with every new entrant
building toward the high price. The 2 M$/kg this study charges sits
below both, and the speculation entry, 0.5 M$/kg, nine times below the
2011 allocation.

At the 2011 allocation the extrapolation device reads 27.8 $/MWh at the
D-rich mix and 67.0 at the 3:1 mix; at the commercial spot, 38.5 and
225; at full self-supply, 24.7. The deuterium-rich machine is nearly
indifferent to the He-3 price, because it buys only during the build-up;
the 3:1-mix machine is not. The credit is coupled to the burnup closure,
because the decay return exists only if the tritium survives the pulse.

One consequence: a kilogram of He-3 burned at the floor produces about
$1.8M of electricity, but sold for $4.5M at the 2011 allocation and
sells for $19-22M today, so an early breeding plant earns more selling
He-3 into the thin cryogenics and quantum market than burning it, until
fleet supply floods that market.

### 5.6 The breeder as the price of He-3

The alternative to self-supply is a dedicated deuterium breeder: a
pure-D power module of the same grade with its He-3 top-up removed, its
prompt He-3 and tritium pumped out every pulse, and its unit cost taken
as module ownership plus a throughput-sized tritium plant plus its net
power at the device's own LCOE, per kilogram delivered
(`scripts/breeder_loop.py`; the tables are in the ledger). It reads the
ledger's price back at the records grade, 2.0 M$/kg co-sited and 2.3
standalone; cannot be reached at the Helion device, where a module that
breeds 5.6 kg/yr costs 6.4 M$/kg; charges about 0.67 M$/kg at the
extrapolation grade; and 0.2 to 0.5 at speculation, where only a fleet
facility selling its power drives the He-3 line toward zero. A
self-supplying device needs the breeder's He-3 only for its build-up, so
re-running each device at its breeder's price moves the ladder little
outside the Helion device: 110 to 112 $/MWh at the records device, 149
to 157 at the Helion device, 25.2 to 25.4 at extrapolations, 10.5 to
10.6 at speculation. The scheme relocates the tritium inventory rather
than shrinking it, and a purpose-designed high-field breeder is unpriced
upside, since at fixed driver energy the D-D yield per shot scales as
the square of the compression field.

## 6. Recovery physics: what the circuit actually gets back

The composite cap (constraint 2) stops the two conversion efficiencies
from being counted twice. This section sets out what else bounds the
recovered energy: the share of the driver energy that thermalizes, the
yield a burn can return, the expansion ratio the chamber allows, and the
axial part of the stroke. A three-shot sequence on Polaris would measure
all four.

**Driver thermalization.** The machine has no auxiliary heating: merging
shock and compression work are the heating, all driver-fed, so the
plasma-thermal share chi of the delivered energy can only return through
the same expansion channel as the fusion heat, at f_pdv, while the model
recovers all of it at the flat inductive efficiency. chi is fixed by the
FRC equilibrium as a function of the separatrix-to-coil radius ratio
alone, chi(x_s) = 1.5 <beta> x_s^2 / (1.5 <beta> x_s^2 + 1 - x_s^2) with
<beta> = 1 - x_s^2/2 (Tuszewski 1988): 0.30, 0.52 and 0.71 at x_s = 0.5,
0.7 and 0.85. The uncaptured loss is worth +1.4 to +3.2 $/MWh at the
extrapolation device across that span, under 0.1 $/MWh at the
speculation device, and order +10 $/MWh at the low-gain Helion device;
it is carried in the reconciliation bands.

**The yield bound.** The same chi bounds the shot. The plasma at peak
compression holds chi E_del, with E_del the driver energy delivered per
pulse (50 MJ), at the energy density of a beta = 1 plasma, 1.5 B^2/2mu0,
and burns at the fusion power density of the burn point, so

    gain <= chi x burn time / breakeven time,

with the breakeven time the ratio of those two densities, the fusion
breakeven time of Lackner et al. (2026); the pulsed gain of Nicolas et
al. (2026), fusion energy over plasma energy, is the same ratio against
their Lawson time. The patent point is n_D 0.75e22 m^-3, He3/D 0.158, 70
keV and 22 T. At Bosch-Hale rates its breakeven time is 86 ms with
thermalized electrons, and 3.7 times shorter if the electrons could be
held at a tenth of the ion temperature. They cannot be held there for
long: the ion-electron equilibration time at that density is about 1 ms,
and Lackner et al. show that the ratio erodes well inside the breakeven
time, so a thermalized state is the realistic assumption for a burning
D-He3 plasma. Helion's reply, that the pulse is over before
equilibration, concedes the timescale. Helion's stated pulse is hundreds
of microseconds to milliseconds (Helion FAQ, June 2026). Against it the
bound reads: a 1 ms burn returns 0.2 to 0.4 MJ from the 50 MJ bank
across x_s 0.5 to 0.85, less than the circuit loses per shot at any
eta_dec in the ladder; the design-basis 128 MJ shot needs 0.3 to 0.7 s,
which falls to the patent table's own tenth-of-a-second class only with
cold electrons throughout; the speculation shot needs 1 to 3 s. The
record on Trenta, the previous prototype, is lifetimes above 1 ms. The
bound also reproduces the co-founder's own D-T design: Slough (2025)
quotes a gain of 9.1 on the FRC energy over a 2 to 5 ms transit at 34.8
T and 15 keV, and at that point's breakeven time the same arithmetic
gives a 3.4 ms burn. This is constraint 7, and it is why the shot is a
graded claim rather than a shared basis; `scripts/yield_bound.py` prints
the bound, and every point the scripts evaluate carries the burn time
its shot implies at x_s 0.7. It is also the thin-cycle argument of
Nicolas et al. in this study's variables: with the plasma holding chi of
the magnetized energy and the burn a fraction of breakeven, the fusion
surplus per pulse is a small fraction of the energy the circuit swings,
and the round-trip circuit efficiency must exceed 1 - gain for any net
work at all. Two independent reconstructions of Helion's reactivity
curve find its fusion-to-bremsstrahlung ratio 3.6 to 9 times too
favorable (Nicolas et al. 2026, Table 1) or about an order of magnitude
(Lackner et al. 2026), which is the provenance of the 0.05 radiated
fraction that constraint 1 withdrew.

**The expansion-ratio bound.** Constraint 6 caps f_pdv at the
adiabatic-stroke bound 1 - (V_i/V_f)^(2/3), with V_i = E_del/(B^2/2mu0),
about 0.26 m^3 at 50 MJ and 22 T. The exponent is the plasma channel's
gamma = 5/3 rather than Helion's lumped plasma-plus-field 1.8, since
field energy is recovered separately through eta_dec, and the isobaric
burn leg makes the true value 1-2 percentage points lower, so the cap is
strict and slightly generous. Applied per point: the extrapolation
device's 10 m x 1.5 m chamber caps f_pdv at 0.98, above its claimed
0.80, and the speculation device's 30 m x 1.5 m chamber caps it at
0.989, just above the claimed 0.947. The large chamber buys expansion
ratio, not merely wall area, and recovery cannot be improved without
more chamber.

The cycle is Diesel-type with an Atkinson over-expansion, the framing of
Helion's own burn-cycle analysis (Kirtley 2024; slides archived in
`docs/sources/`), which quotes about 60% for a constant-pressure burn
and above 90% for optimal cycles. Two published figures sit against it.
Nicolas et al. (2026), whom Helion's FAQ cites for recovery "exceeding
95%", give that number only as an ideal Carnot-form bound and set it
aside on the thin-cycle argument. Slough (2025), the co-founder whose
patent supplies the fuel cycle, derives 40% as the most an ejected FRC
can return in a flux-conserving expansion chamber, where it comes to
rest holding 1.5 pV of thermal energy against the field it has
compressed, and states that an FRC does not free-expand. That is his own
recovery topology, not the discharged compression coil this work's f_pdv
assumes, so it is carried as a risk row rather than a cap: at f_pdv 0.4
the extrapolation device reads 43.0 $/MWh (+16.9) and the speculation
device 14.8 (+4.2). There is no Carnot exemption in any of this: cycle
form, the compression and expansion ratios, and the entropy of the
deliberately irreversible merging set the efficiency, which is what the
composite cap encodes.

**The parallel channel.** Part of the expansion work is axial: the
elongating plasmoid pushes against the end-field gradient and changes
the flux linkage of the end coils, about a fifth of the boundary work by
the FRC adiabatic scalings (Spencer et al. 1983), returned only if those
coils are on the recovery circuit during the stroke. Constraint 6 counts
the whole volume stroke, as Helion's own burn-cycle framework does, so
the axial fifth is not deducted; whether the end circuits return it is a
design question the shot sequence below measures.

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
than only from ordinary inductive coupling in the circuit". Until April
2026 the same page said that no results on energy recovery with plasma
present had been released; the June 2026 rewrite says high-efficiency
magnetic energy recovery has been measured on seven prototypes and gives
no figure.

## 7. Plant architecture: modules, parks, and the small-plant penalty

Two controlled sweeps at the speculation stack (constant gain, constant
wall loading, driver and chamber scaled with module power) separate
module count from plant size. **Module count at fixed plant size is
nearly free, and mid-size modules carry a mild bonus**: a park of 500
MWe modules reads 10.1 $/MWh against the single 1 GWe module's 10.6
$/MWh (the adiabat-priced coils reward smaller compressed volumes; 250
MWe modules read 10.2), and even 50 MWe modules cost only four tenths of
a dollar more (11.0), because buildings, supplementary capital, and
balance of plant price plant totals; the only modularity tax is
per-module fixed items, biting below about 100 MWe. **Standalone plant
size is expensive**:

| plant | LCOE ($/MWh) | $/kW | dominant penalties |
|---|---|---|---|
| 1 GWe | 10.6 | 1488 | - |
| 250 MWe | 17.5 | 2262 | fixed site buildings, staffing^0.5 |
| 50 MWe | 43.2 | 6325 | O&M 17.2 $/MWh (staffing law), 141 M$ of buildings, tritium-plant fixed core |

![Module size, park vs standalone](figures/fig5_plant_size.svg)

*Figure 5: The same physics sold two ways at the full speculative stack.
Module size in a 1 GWe park is nearly free; standalone plant size is
expensive, and the 50 MWe standalone unit costs 4.1x the park floor.*

The penalty decomposes into three mechanisms: about 138 M$ of fixed site
buildings calibrated on fission-class analogs (whether they are the
right comparator for a factory-shipped unit on an industrial pad is an
open question); the P^0.5 staffing law (the Idaho National Laboratory
sodium-fast-reactor staffing basis; no documented record yet supports
remote fleet operation of a fusion-class plant); and the absence of any
fleet-learning term on equipment, the one mechanism that could make
mass-produced small units positively cheaper, which must be anchored
beyond the fleet size the nth-of-a-kind (NOAK) constants already assume
or it double counts. The in-model conclusion is unambiguous: this
concept's economics live in power parks, and a 50 MWe module is a
manufacturing choice the model neither rewards nor punishes at park
scale.

## 8. What crosses $10/MWh, and what carries it

The full speculation stack crosses the target only as a 3 GWe park (8.4
$/MWh; 10.6 at 1 GWe), and the entry that carries it across is its
financing: at the design-basis 7% real cost of capital the same machine reads 14.6 $/MWh
(17.8 at 1 GWe), so the 3% real cost of capital, sovereign-class money
with no mechanism behind it, is worth more than the whole distance to
the target. No physics or engineering entry crosses it on its own, and
the crossing needs the derived availability of 0.92 (at the model
default of 0.85 the park reads 9.0 $/MWh and at 0.95 it reads 8.2, so it
holds at any availability above the default) and Helion's shot granted,
as for every number here (the park's 200 MJ pulses are a burn of half a
second to a second at the patent point). It survives the wall-and-coil
replacement, priced in Section 5.4 on top of the model's figure: 0.4
$/MWh at the 50 dpa tolerance and 1.2 at the demonstrated 20 dpa take
the park to 8.8 to 9.6 $/MWh.

- **He-3 at zero cost** (6.5 $/MWh at 3 GWe): worth 1.9 $/MWh, and it
  changes the machine. The deuterium-rich park gains only 0.2 $/MWh,
  since it buys He-3 only while its store builds up; the design search
  re-run at zero price picks the He-3-rich mix (dd_frac 0.13) in 15 m
  chambers with no tritium plant, at 6.5 $/MWh.
- **Gas-class site and decommissioning analogs** (about 2 $/MWh at 1
  GWe, the whole of the buildings and CAS50 lines): defensible only for
  the 3:1-mix machine, which carries no tritium plant; the D-rich
  machine's tonne-class tritium inventory argues the other way.
- **A real fleet-learning term** on equipment, anchored beyond the NOAK
  reference fleet: the only mechanism that rewards the mass-produced
  small-unit strategy at all.

None of these is in the evidence base at any grade.

## 9. Conclusions and measurement priorities

The cheap numbers rest on a small set of unmeasured properties,
ranked here by the $/MWh they gate:

1. **The shot** (the whole plant): the yield of a burning Polaris pulse
   at its measured burn time, read against constraint 7; Helion's stated
   proof point, energy on the bank from fusion-driven expansion, is the
   same measurement.
2. **Capacitor cost-at-life** (tens of $/MWh): a sourced curve replacing
   the single derating target, resolving the joint optimism of 0.1 $/J
   with 1e10-shot life.
3. **The recovery chain** (2 to 17 $/MWh at the extrapolation grade, the
   top of the range at Slough's 40% ceiling): the Polaris shot triplet,
   whose no-burn deficit says whether f_pdv sits at the flux-conserver
   0.4 or near the adiabatic bound.
4. **Per-pulse burnup, extraction, and fuel recovery** (a few $/MWh at
   the deuterium-rich mix, which supplies its own He-3, tens at Helion's
   mix): the patent fixes the design intent, low per-pulse burnup with
   inter-pulse tritium removal, but a patent is design intent, not a
   measurement; the reactor-point compression density and field, the
   demonstrated per-pulse separation rate, and the per-pass fuel
   recovery (three nines suffice for He-3 self-supply at the
   deuterium-rich mix, four are needed at Helion's) fix the neutron
   spectrum, the wall-replacement schedule, and the fuel-cycle cost
   between them.
5. **A duty-cycle basis for multi-Hz operation** and **a costed
   tritium-plant scope** for the D-rich cycle (single $/MWh each, but
   licensing-defining).

Three caveats survive into the headline:

- The speculation stack is jointly, not just individually, heroic: 0.1
  $/J capacitors and 1e10-shot life together contradict the derating
  physics that connects capacitor cost to life; the composite sits at
  the theory optimum with zero margin; three-nines exhaust recovery
  becomes load-bearing at low burnup; the 500 MJ shot is a burn of
  seconds at the patent point.
- The headline floor is conditional on the patent-basis compression
  field: per-pulse burnup falls as B^2, so a 10 T reactor point adds
  about 2 $/MWh and a 5 T point about 11 $/MWh. It is conditional too on
  the discharged-coil recovery topology: at the 40% ceiling Slough
  (2025) derives for a flux-conserving expansion chamber the speculation
  device adds 4.2 $/MWh and the extrapolation device 16.9 (Section 6).
  The neutron-damage costs are more likely low than high
  (fission-spectrum dpa data, an order of magnitude more helium per dpa
  at 14 MeV, uniform-cylinder averaging over a localized burn).
- Model gaps priced in the bands but excluded from the headline:
  high-voltage DC switch duty, tritium-plant scope, driver
  thermalization, and the wall-and-coil replacement at the dpa
  tolerance, worth 0.4 to 1.2 $/MWh at the 3 GWe park, which takes it
  from 8.4 to 8.8-9.6, still under the target. The main conservatism
  cuts the other way (no thermal bottoming in the basis, worth -4.2
  $/MWh at the extrapolation device).

The constructive reading for the concept: its floor, conditional on
the shot, is low by any thermal-plant standard, its architecture
(factory modules, park deployment, swappable cores) is well matched to
the failure modes the physics imposes, and the measurements that would
move its ladder from speculation to evidence, the shot first among
them, are all available on hardware the developer is already building.

## Reproducibility

Everything here is in the study repository at
[github.com/1cFE/helion_pulsed_frc_tea](https://github.com/1cFE/helion_pulsed_frc_tea):
the four evidence stacks in `config/`, the scripts in `scripts/` that
produce every number, every figure and the HTML renderings of this page
and the ledger (the README says what each one does), the evidence
ledger, the adversarial review, the capacitor evidence, and the Helion
slide and FAQ captures. The cost model is `1costingfe` at commit
44434d9. Sixty regression tests pin all four devices at both plant
sizes, the stack evaluations at Helion's configuration, the design
search's burn mixes on their bremsstrahlung floors, the free-He-3
optimum by mix, the tritium-burn closure, the yield bound with the burn
time every point implies and its D-T cross-check, the recovery ceiling,
the tritium store's He-3 credit, the chi(x_s) anchors, the breeder unit
cost, the availability derivation, the financing ladder, and the
three-part partition of the LCOE behind Figure 1, and fail loudly if the
model moves under this work.

## Conflict of interest

Tal Rubin and Damien Scott are co-founders of a proton-boron-11 fusion
startup.

## References

- Böhnlein, S., et al. (2026). "Too cheap to meter? A stochastic
  analysis of projected future fusion costs." arXiv:2606.26536 (56
  references surveyed; 43 plant-lifetime assumptions with medians of
  30-40 years across maturity levels).
- Bosch, H.-S., and Hale, G. M. (1992). "Improved formulas for fusion
  cross-sections and thermal reactivities." Nuclear Fusion 32, 611.
- Brezinsek, S., et al. (2013). "Fuel retention studies with the ITER-
  Like Wall in JET." Nuclear Fusion 53, 083023.
- Helion Energy. Technology and FAQ pages (helionenergy.com/technology,
  /faq). The FAQ was rewritten between its 20 April and 5 June 2026
  captures; both versions are archived in `docs/sources/` (the earlier
  one for "we have not released results overviewing our energy recovery
  with plasmas present" and "electricity by 2028", the later one for the
  required confinement "on the order of hundreds of microseconds to
  milliseconds", the equilibration reply, the recovery "exceeding 95%"
  citing Nicolas et al., and the proof point for electricity from
  fusion). Microsoft power purchase agreement announcement (2023).
- Axios Pro (2026). "Helion hedges on how soon it expects to sell
  electricity from fusion," 8 September 2026 (the withdrawal of "net
  electricity" from Helion's stated goals).
- Kirtley, D. (2026). Series G final close at $500M, 15 September 2026
  (x.com/dkirtley); initial close of $465M on 4 June 2026 led by Thrive
  Capital at a $15.5B post-money valuation.
- Helion Energy (Slough, J., Kirtley, D., and Pihl, C.). "Advanced fuel
  cycle and fusion reactors utilizing the same," priority 7 February
  2014, filed 6 February 2015, published as US 2017/0011811 (2017),
  granted as US 11,469,003 B2 (11 October 2022): the
  breed-extract-store-decay fuel cycle and its operating table (70 keV,
  22 T, 72 MW at 1 Hz, confinement 0.157, 0.103 and 0.088 s across its
  three columns). Used as design intent, not as a record; see Section
  5.2 and constraint 7.
- IEA/NEA (2020). Projected Costs of Generating Electricity, 2020
  edition (3%, 7%, and 10% real discount rates, 7% central).
- Kirtley, D. (2024). "Fundamental theory of the direct magnetic energy
  recovery in a thermonuclear field reversed configuration system." APS
  DPP 2024, abstract GO05.8; slide captures in `docs/sources/` (the
  composite-recovery figure behind constraint 2 and the Otto/Diesel
  burn-cycle expressions behind Section 6).
- Kirtley, D., and Milroy, R. (2023). "Fundamental scaling of adiabatic
  compression of field reversed configuration thermonuclear fusion
  plasmas." Journal of Fusion Energy 42, 30.
- Lackner, K., Burhenn, R., Fietz, S., von Müller, A., and Ball, J.
  (2026). "Comments on the Paper 'Fundamental Scaling of Adiabatic
  Compression of Field Reversed Configuration Thermonuclear Fusion
  Plasmas'." Journal of Fusion Energy 45, 12 (ion-electron equilibration
  against the fusion breakeven time; Helion's bremsstrahlung about an
  order of magnitude below the standard expression).
- Langtry, A., et al. (2025). "Affordable, manageable, practical Z-pinch
  driver (AMPS)." arXiv:2504.10680 (capacitor derating and shot-life
  target).
- Nicolas, T., Goupil, C., Herbert, E., and Ball, J. (2026). "The
  Challenge for Adiabatically Heated FRC Based D-3He Fusion." Journal of
  Fusion Energy 45, 24 (the pulsed gain as fusion energy over plasma
  energy, the Lawson bound B^2 tau >= 1.4 (2 + 3 T_e/T_i)^2, the
  plasma's 1e-2 share of the magnetized energy and the thin current-flux
  cycle, Table 1 against Helion's reactivity curve).
- Rubin, T. (2026). 1costingfe: a bottom-up fusion power plant cost
  model. Repository at commit `44434d9`.
- Slough, J. (2025). "A compact fusion reactor based on the staged
  compression of a field reversed configuration." Nuclear Fusion 65,
  106019 (open access; the 2026 corrigendum replaces figure 36 only):
  the self-sustained cycle's He-3 fraction of roughly 0.16, citing the
  fuel-cycle patent; the D-T design point (34.8 T, 15 keV, gain 9.1 on
  the FRC energy over a 2 to 5 ms transit); the 40% recovery ceiling of
  a flux-conserving expansion chamber (its equation 18).
- Spencer, R. L., Tuszewski, M., and Linford, R. K. (1983). "Adiabatic
  compression of elongated field-reversed configurations." Physics of
  Fluids 26, 1564 (the FRC adiabatic compression scalings behind the
  axial share of the expansion work).
- Thea Energy (2025). "Overview of the Helios Design: A Practical Planar
  Coil Stellarator Fusion Power Plant." arXiv:2512.08027 (one 84-day
  planned outage every two years; coils shielded to a 40-year minimum
  life).
- Tuszewski, M. (1988). "Field reversed configurations." Nuclear Fusion
  28, 2033 (FRC equilibrium, average-beta theorem, adiabatic scalings).
- US DOE/NETL. Quality Guidelines for Energy System Studies: EPCM
  indirect-cost basis.
- US DOE Water Power Technologies Office. Hydropower Basics (typical
  lifespan 65-85 years).
- Congressional Research Service (2011). "The Helium-3 Shortage: Supply,
  Demand, and Options for Congress," R41419, updated October 6, 2011
  (Table 2: DOE-allocated helium-3 prices, 600 $/L to federal users and
  1,000 $/L to commercial users in 2011).
- Edelgas Group (2024). Helium-3 market pricing, as reported in
  SpaceNews and Newsweek coverage of the Interlune agreements (2025);
  Interlune-DOE Isotope Program and Interlune-Maybell Quantum agreements
  (2025); TAE Technologies and Black Moon Energy Corporation helium-3
  supply option (2026).
- Idaho National Laboratory. Advanced-reactor staffing studies (the
  P^0.5 O&M scaling basis).