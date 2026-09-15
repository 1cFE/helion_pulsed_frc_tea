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

**The findings, in brief.** Priced bottom-up under seven enforced
physics couplings, the four devices read 151.5, 108.4, 33.6 and
12.0 $/MWh at 1 GWe, from citable records through Helion's own
requirements and labeled extrapolations to speculation. The speculation
park reads 9.7 $/MWh at 3 GWe, and 19.0 and 15.8 $/MWh at the
design-basis 7% real cost of capital, so the public $10/MWh target is
reached by one stack only, the 3 GWe park, and only through 3% real
financing with a derived availability above 0.90. Every number grants
the vendor's shot: 128 MJ of fusion yield from a 50 MJ bank. No record
supports that yield, and it does not fit the pulse the vendor itself
states. Helion puts the pulse at hundreds of microseconds to
milliseconds; at the patent burn point a millisecond burn returns under
half a megajoule, and 128 MJ needs 0.3 to 0.7 s, so on citable records
alone the machine makes no net power. The two largest levers down the
ladder are the capacitor cycle life (1e9 shots, a published target) and
the fourth nine of per-pulse fuel recovery (a patent-implied
extrapolation); the repetition rate and the deuterium-rich burn mix
come next, at about a third of their weight. The fuel cycle, not the
driver, is the load-bearing subsystem, with a tonne-class tritium store
intrinsic to He-3 self-supply. The
measurements that would move the ladder are all available on Polaris,
first among them the yield of a burning shot at its measured dwell.

The costing uses the `1costingfe` bottom-up cost model, built on
publicly available data and labeled extrapolations; the open-source
code is available [here](https://github.com/1cFE/1costingfe),
with detailed documentation
[here](https://files.1cf.energy/1costingfe_paper.pdf).

This work is organized as follows: Section 2 describes Helion's device from the published material.
Section 3 defines four devices that share that architecture and
differ only in the subsystem performance they are granted: citable
records, Helion's own requirements taken at face value, and two
labeled relaxations, extrapolations and speculation, all on one plant
environment and each optimized to its best cost under
enforced physics constraints. Section 4 reports the cost of each of
the four devices. Section 5 deals with the helium-3 economics,
purchased fuel being a fifth of the vendor device's LCOE at first
blush, and works out the He-3 recycling, the system that takes the unburnt fuel out between shots
and stores the bred tritium until it decays into the next He-3, and
Section 6 deals with the recovery of the driver energy through the
expanding plasma and with the bound that the plasma's energy and burn
time put on the yield of a shot, which is where the vendor's shot
parts from the vendor's stated pulse; each is gated by a few
unmeasured plasma properties that the developer's own next machine
could resolve.

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
fires at 1 Hz, and Orion is to supply Microsoft at least 50 MW, which
the vendor describes as at least 50 MWe after an initial ramp-up period
(Helion FAQ, June 2026). No public source says how many machines make
up that plant. This work takes it as one module; the solved yield
scales inversely with the count, while the cost at fixed plant size is
nearly indifferent to the split (Section 7). The yield per shot is
whatever makes the model turn that shot into
50 MWe at 1 Hz at the burn point Helion's patent discloses: 128.1 MJ, a
gain of 2.56. The gain is a consistency figure, not a disclosed
measurement. The chamber radius is 0.61 m, the smallest at which a
10 m cylinder wall survives the shot under the tungsten flash bound of
1.5 MJ/m^2 per pulse; the vendor
device at 1 GWe is 20 modules at 1 Hz, and in general a plant is an
integer number of Helion-class modules, with the repetition rate and
module count solved jointly from the net-power target under a rep-rate
ceiling.

The public record as of September 2026 is D-T fusion on Polaris at
150 million degrees C, with no published yield or recovered
electricity, from a vendor that has withdrawn the term "net
electricity" from its own goals (Helion FAQ, June 2026; Axios,
September 2026).

The fuel cycle is the one in Helion's patent (US 11,469,003 B2). The
patent's operating table also fixes the vendor device's burn point: a
plasma with He3/D = 0.158 at 70 keV and 22 T, radiating 23% of its
fusion power as bremsstrahlung and releasing 6% as neutrons. Slough
(2025), citing the same patent, restates that mix as the self-sustained
cycle's limit, He-3 at roughly 16% of the fuel, and in the same paper
leaves D-He3 for a D-T design, putting the D-He3 gain at equal FRC
conditions a factor of 240 below D-T's. The other
three devices run deuterium-rich, with 85% of the fusion events D-D,
because He-3 is expensive: bred He-3 undercuts purchased He-3 at every
grade, so the design search picks that mix each time. The D-D reactions
are what close the cycle. Half of them produce a He-3 atom directly; the
other half produce a triton, which is pumped out with the exhaust after
the pulse, separated, and stored on getter beds until it decays into
He-3 (12.3 yr half-life). Almost none of the tritium burns before it is
removed (dhe3_f_T = 0 in the basis). The
plant therefore has no lithium anywhere, and its tritium plant is an
exhaust-processing and storage plant.

## 3. Method

**Notation.** 1costingfe model parameters keep their configuration-file
names. dd_frac
(dhe3_dd_frac) is the D-D share of primary fusion events by count, not
an ion ratio (the patent's He3/D = 0.158 at 70 keV is 0.49). dhe3_f_T is the fraction of
bred tritium that burns in-pulse. burn_fraction and burn_fraction_he3
(bf) are the per-pass burn probabilities of deuterium and He-3 through
the chamber, and fuel_recovery (fr) the per-pass fraction of unburned
fuel the exhaust loop returns. f_rad is the fraction of fusion power
radiated as photons. eta_dec is the circuit efficiency of inductive
recovery, f_pdv the fraction of the plasma's expansion work that reaches
the coils, and their product the composite recovery; eta_pin is the
driver's wall-plug efficiency. f_rep and max_f_rep are the repetition
rate and its ceiling; cap_shot_lifetime is the capacitor shot life. chi
is the plasma-thermal share of the delivered driver energy and x_s the
separatrix-to-coil radius ratio.

**Cost model.** `1costingfe` is a bottom-up, account-structured
(CAS-coded) fusion costing framework. At the pinned commit it prices
linear pulsed concepts as cylinders with the first-wall heat flux
audited against the declared wall class; counts undirected ash,
radiation, and conversion waste in the pulsed wall load; scales the
primary coolant on thermal power; prices the driver per joule of stored
energy and the inductive-conversion account on the energy the physics
path actually returns; and schedules replacement of the full
shot-cycled recovery chain (driver bank, recovery store, switch stack)
at the capacitor shot life.

**Evidence ladder.** The plant environment is held in part and stepped
in part:

- Held at every rung: constant-dollar framing, 2.5-year construction
  (Siemens Energy CCGT block precedent), and indirects at 8% of direct
  cost (US DOE/NETL QGESS).
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
  and a wall-and-coil changeout at the dpa tolerance (20 dpa through the
  records grade, 50 above it): 0.896 at the records device, 0.924 at
  speculation, at the top of the fusion literature's 0.75 to 0.90.

The performance entries step the same way. The records device holds two
of the vendor's three unrecorded claims at their evidence-supported
values, per-pulse fuel recovery 0.999 (the JET-ILW retention analogy;
Brezinsek et al. 2013) and the recovery share at the radial-only 0.8 of
the adiabatic work partition; the third, the shot, has no
evidence-supported value above zero, so on evidence alone the records
device makes no net power, and it is priced at the vendor's shot only
so that a machine exists to cost. The Helion device grants the vendor's
0.9999, the full share, and the shot; the extrapolation and speculation
stacks keep that grant and add the labeled entries listed with the
results in Section 4, the largest being capacitor life 1e9 shots (the
Pacific Fusion AMPS derating target; Langtry et al. 2025). Every entry
carries a source and grade in the evidence ledger (`docs/ledger.md`,
rendered to HTML alongside this page); no extrapolation entry is a
measured record.

**Coherence constraints.** Six couplings are enforced by the scripts on
every quoted point, and a seventh, derived in Section 6, is applied to
every quoted point in this text:

1. The radiated fraction is a function of the burn mix through a
   bremsstrahlung floor (f_rad = 0.28 at dd_frac 0.85, not the lean-mix
   0.05).
2. Recovery efficiency is capped as the composite eta_dec x f_pdv (0.80
   through the extrapolation grade, 0.90 at speculation), because the
   only published figure speaks to the product.
3. The wall must survive both its steady flux (within the purchased
   wall class) and its per-shot flash energy (under the tungsten
   millisecond-melt bound).
4. A mix at or above the vendor's catalyzed 0.49 carries its
   tritium-plant consequences, priced as a fuel-handling adder of 50 M$
   fixed plus 0.657 M$ per MW of plant neutron power.
5. The in-plasma tritium burn dhe3_f_T is floored by the burnup closure
   of Section 5.2, so a low-burn claim at high per-pulse burnup is
   flagged as requiring prompt triton loss (at the patent basis the
   floor is 0.002 and the design's zero passes).
6. The expansion-work recovery fraction is derived per point, never
   asserted: f_pdv = min(claim, share x [1 - (V_i/V_f)^(2/3)]) with V_i
   the compressed flux volume at the 22 T basis field, V_f the chamber,
   and share the radial fraction of the boundary work (0.8 at the
   records and extrapolation grades, 1.0 at speculation and at the
   Helion device; Section 6).
7. The shot yield is bounded by the plasma energy and the burn time,
   gain <= chi x burn time / breakeven time, with the breakeven time
   that of the plasma at the burn point, so every quoted point carries
   the burn time its shot implies, and the shot is graded with the rung
   rather than shared as a basis.

**Design search and reconciliation.** Each device except Helion's own
configuration is the argmin of a scan over shot yield (a free
parameter only at speculation, where the scan chooses it; the records
and extrapolation devices keep the design-basis shot), chamber length and
radius, wall class, and burn mix, discarding any design that violates
a constraint.
Reconciliation then brackets each minimum with the model gaps it cannot
price internally (HVDC-class switch duty, the tritium-plant band, the
driver-thermalization derate) and its conservatisms (no thermal
bottoming), yielding an honest band rather than a point.

## 4. Results: the four devices and what carries the floor

| device | 1 GWe | 3 GWe | at 7% real, 1 GWe |
|---|---|---|---|
| citable records | 151.5 | 147.7 | 151.5 |
| Helion's requirements | 108.4 | 104.7 | 108.4 |
| extrapolations | 33.6 | 30.5 | 39.9 |
| speculation | 12.0 | 9.7 | 19.0 |

LCOE in $/MWh. The at-7% column reprices each device at 7% real with
everything else unchanged, so the gap between it and the 1 GWe column is
what the rung's cheaper money is worth: 6.3 $/MWh at extrapolations and
7.1 at speculation (5.7 and 6.1 at 3 GWe). The records and vendor rungs
already sit at 7%, so their two columns match. The stack and design
behind each row:

- **citable records**: fuel recovery 0.999 (JET analog), radial-only
  recovery share; 7% real, 30-year life; the vendor's 128 MJ shot
  granted; optimum: that shot at 1 Hz in 10 m x
  1.0 m panel-wall modules (26 of them), D-rich mix with its tritium
  plant
- **Helion's requirements**: the vendor configuration (50 MJ driver, 20
  modules in the smallest chamber that survives the shot, the patent's
  catalyzed mix dd_frac 0.49 with its 0.23 bremsstrahlung fraction and
  tritium plant; 7% real, 30-year life) granted its three unrecorded
  claims: the 128 MJ shot that delivers the 50 MWe module at 1 Hz (a 0.3
  to 0.7 s burn at the patent point, against the vendor's stated pulse),
  fuel recovery 0.9999, full recovery share
- **extrapolations**: records (with the vendor's shot, here graded as
  the patent-implied 0.3 to 0.7 s burn) + capacitor life 1e9, a 3 Hz
  ceiling, a purchasable divertor-class wall, fuel recovery 0.9999
  (patent-implied fourth nine), 5% real and the 80-year civil-works
  life; optimum: seven 10 m x 1.5 m panel-wall modules at 2.8 Hz
- **speculation**: extrapolations + 10 Hz, axial-channel capture,
  capacitors at 0.1 $/J and 1e10 shots, He-3 at 0.5 M$/kg, 3% real;
  optimum: 300-1000 MJ of fusion yield per shot from the same 50 MJ
  driver (gain 6-20; 500 MJ carried, a 1 to 3 s burn at the patent
  point), chosen by the scan, in 30 m x 1.5 m chambers

With the coils priced along the expansion adiabat, the design search
trades length for radius: fat short chambers buy expansion volume with
less active structure. Reconciliation brackets the extrapolation
device within 26.4-38.9 $/MWh and the speculation device within
11.0-12.9 $/MWh at 1 GWe. The D-rich mix is the strict optimum at every grade: the He-3-lean
mix (dd_frac 0.31) sits 1.1 $/MWh behind at speculation (13.1 $/MWh in
a 20 m x 1.5 m chamber) and 11 $/MWh behind at extrapolations, buying
its He-3 at the stack's price entries, which Section 5.5 shows no
market supports.

The records device tops the ladder, and the reason is exactly three
claims, one of which has no record value to revert to. The headline
gap (151.5 against 108.4 $/MWh) cannot show that by itself, because
the two devices are different machines; the controlled comparison is
to take Helion's machine unchanged and revert its two revertible
unrecorded claims to their record-supported values. That alone raises
its cost by 68%, from 108.4 to 181.9 $/MWh (a counterfactual that also
sits 5% over the wall flash bound on the vendor's 0.61 m chamber, one
reason the records design moves to fat chambers); design freedom
under the record stack (its optimum is already the D-rich mix with
its tritium plant) buys back two fifths of the increase, to
151.5 $/MWh. Reverting the third claim, the shot, leaves no plant,
so every number in the table is conditional on it. The evidence
premium is not
diffuse conservatism but three specific, measurable claims: the shot,
the fourth nine of per-pulse fuel recovery, and the axial share of
the expansion work. On evidence alone the machine makes no net power
and the fuel cycle is uneconomic; the descent begins when the shot
and the recovery extrapolations are granted. The records and Helion
devices are also dominated by scheduled replacement: the entire
shot-cycled recovery chain is replaced on the capacitor-life
schedule, about eight times over their 30-year life at the 1e8-shot
record life.

![The evidence ladder](figures/fig1_ladder.svg)

*Figure 1: The four devices at 1 and 3 GWe, one machine per evidence
grade, each bar split into the overnight cost recovered straight-line
over the book life (blue), the cost of money, interest during
construction and on the capital (orange), and O&M, fuel and scheduled
replacement (grey). Cost of capital 7% real at the records and Helion
devices, 5% at extrapolations, 3% at speculation; book life 30, 30, 80,
80 years. The records device sits above Helion's requirements because
reverting two of the vendor's three unrecorded claims is worth about
74 $/MWh; the third, the shot, is granted to every bar, since its
record value is no plant.*

One-at-a-time reversion from the extrapolation device ranks the levers:

| parameter reverted | LCOE ($/MWh) | delta ($/MWh) |
|---|---|---|
| cap_shot_lifetime -> 1e8 | 70.9 | +37.3 |
| fuel_recovery -> 0.999 (JET-analog) | 64.7 | +31.1 |
| max_f_rep -> 1 Hz | 45.8 | +12.2 |
| dhe3_dd_frac -> 0.49 (with its f_rad) | 44.1 | +10.5 |
| interest_rate -> 0.07 (financing) | 39.9 | +6.3 |
| lifetime_yr -> 30 | 37.6 | +3.9 |
| eta_dec -> 0.85 | 36.4 | +2.8 |
| f_rad -> 0.23 (incoherent) | 32.5 | -1.1 |
| eta_pin -> 0.95 | 34.4 | +0.8 |
| wall_dpa_tolerance -> 20 | 33.8 | +0.2 |

The capacitor cycle life (a published derating target) and the
per-pulse fuel recovery (an extrapolated nine beyond the JET retention
analogy) dominate, the rep rate and the burn mix follow, and the two
environment entries come after them: the cost of capital (the grey
financing bar) is worth 6.3 $/MWh and the 80-year book life 3.9 $/MWh.
f_pdv is absent from the table because it is derived per point under
constraint 6, not a parameter; the shot is absent for the opposite reason,
since its record value is no plant. The conversion
efficiencies, once capped as a composite, are worth little at the
margin (an incoherent double-booking of eta_dec = 0.97 with
f_pdv = 0.95 would claim tens of $/MWh and is excluded by
construction).

![Tornado from the extrapolation device](figures/fig2_tornado.svg)

*Figure 2: One-at-a-time reversion of each extrapolation entry to its
record value, from the 33.6 $/MWh extrapolation device. Red bars are
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
| DEC power electronics (C220109) | 65 | 0.3 |
| adiabat-priced coils (C220103) | 14 | 0.1 |
| O&M (CAS70), levelized in constant dollars | 34/yr | 4.3 |
| fuel (CAS80) | 13/yr | 1.6 |
| annualized capital, all-in (3% real, 80 years) | 49/yr | 6.1 |

![What carries the floor](figures/fig3_anatomy.svg)

*Figure 3: Capital accounts carrying the speculation device. The driver
bank, the concept's narrative centerpiece, is the smallest bar; site
infrastructure and the fuel cycle dominate.*

## 5. The tritium fuel cycle is the load-bearing subsystem

### 5.1 Rates and inventory

At the speculation device the single module runs 7.7e20 D-D and 4.5e20
D-He3 reactions per second; only 1.4e20/s of the D-He3 burns are fed by
purchased He-3, the rest by recycled bred He-3 (cumulative fusion
probability 0.80). The module breeds tritium at half the D-D rate:
0.55 mg per shot, 56 kg/yr. The extrapolation stack on the vendor
chamber carries 232 MW of plant neutron power and breeds about
86 kg/yr. Store-for-decay fixes the
equilibrium inventory at production rate times the 17.8 yr mean life:
about 1.5 tonnes of tritium, which is 1.5e10 Ci, about 490 kW of
continuous decay heat, roughly 380x ITER's site authorization and 55x
the world's civilian tritium stock. The
inventory is intrinsic to He-3 self-supply at this scale; shipping it to
a central fuel facility relocates it (and can hold the reactor site near
ITER-class inventory with weekly pickups) but cannot shrink it. This is
why the ledger refuses the "near-zero licensing" claim alongside the
fuel credit, holds O&M at its baseline, and treats the 200 M$
tritium-plant allowance as more likely low than high.

### 5.2 The burnup closure

The store-and-decay idealization (dhe3_f_T = 0: no bred triton burns
in-plasma) is not a free choice; it is a claim about pulse kinetics. A
triton born mid-pulse sits in a deuterium-rich plasma at fusion
temperature for the remaining dwell, and D-T reactivity is 27-87x D-D
at 70-20 keV (Bosch and Hale 1992), so each unit of D burnup burns
14-43x as much of the bred tritium (the birth-averaged half-ratio). The per-pulse deuterium burnup pins
the integrated exposure x_DD = -ln(1 - f_D) = n_D <sigma v>_DD tau
without requiring density or dwell separately; tritons are born
uniformly in cumulated exposure (their production rate is proportional
to the same n^2 <sigma v> that accumulates it), so averaging over
births gives the thermalized-limit in-pulse tritium burn

    f_T = 1 - (1 - e^-x)/x,  x = (sv_DT / sv_DD) x_DD,

exact for any pulse-shape history at fixed density and temperature
(a varying density reweights triton births; immaterial at the basis
burnup): the reactivity ratio is the only physics input. Two caveats bracket
it: a slowing 1 MeV triton passes through the D-T cross-section
resonance, so beam-target burn can only add to the estimate, while
prompt orbit loss from the small-s plasmoid (the triton's gyroradius
is centimeter-scale at compression) truncates it and is the one
mechanism that can hold the burn below the floor. This closure is
enforced as coherence constraint 5: any quoted point whose dhe3_f_T
sits materially below the floor is flagged as coherent only under
prompt triton loss.

The basis values come from the vendor's fuel-cycle patent (US
2017/0011811, granted as US 11,469,003 B2), whose operating table
(n_D = 0.75e22 m^-3, T = 70 keV, tau = 0.157 s without tritium removal
and 0.103 s with it) states that tritium "may be removed between each
pulse ... prior to undesired D-T reactions taking place". A patent is
design intent, not working physics: its tau implies n tau of
2-3e21 s/m^3 at 70 keV, three to four orders beyond any demonstrated
FRC confinement, so this work uses the table's density and
temperature, which the vendor's stated >15 T compression hardware
corroborates through pressure balance, and never its confinement time
as a fuel-cycle input; the shot, however, implies it,
which is why the shot is graded and the fuel cycle is not priced on
the table's dwell.
The closure on those numbers reproduces the patent's own two-column
structure: over a full confinement period the D burn is 2.5-3.8% and a
thermalized triton riding it would burn 28-38%, the case for
inter-pulse removal; per sub-millisecond pulse the burnup is 1.2-2.5e-4
and the in-pulse tritium burn 0.2-0.3%, so dhe3_f_T = 0 satisfies its
floor with two orders of margin. The same burnup is a dwell of about
0.3 ms, at which the design-basis shot is out of reach by the yield bound:
the low-burnup fuel cycle and the vendor's shot are two different
machines, and this work prices the fuel cycle on the vendor's stated
pulse and carries the shot as the vendor's requirement. Fuel
therefore resides in the machine of order a thousand pulses before
burning, and the model carries the per-pulse pair burn_fraction =
1.2e-4 and burn_fraction_he3 = 4.1e-4 (He-3 burns 3.3x faster per
pass), with species-resolved recycle losses in the fuel account. A
recirculating nucleus faces the same race every pass, burn with
probability bf or leak with probability 1 - fr, so its ultimate fate
is the geometric series bf / (1 - fr (1 - bf)), set by the ratio of
the two rates:

| species (per-pass burn) | fr = 0.99 | fr = 0.999 | fr = 0.9999 |
|---|---|---|---|
| deuterium (1.2e-4) | 1.2% burns | 11% burns | 55% burns |
| He-3 (4.1e-4) | 3.9% burns | 29% burns | 80% burns |

At the four-nines basis, He-3 mostly burns (0.80 is the cumulative
fusion probability the fuel account credits) while deuterium splits
nearly evenly between burning and leaking; at three nines the loop is
primarily a fuel-disposal device, wasting 71% of its He-3, and at two
nines nearly everything leaks. Tritium sees no geometric series at
all: it is extracted to the store on its first pass, so separation
loss hits it once, not compounded. The costs of the residence are the
fuel cycle's load-bearing claims: with per-pulse reprocessing the
unburned-fuel repurchase multiplier is 84x at per-pass recovery 0.99,
9.3x at 0.999, and 1.8x at 0.9999, so four-nines per-pulse recovery
and hertz-rate isotope separation are what the published fuel cycle
actually requires, and the tritium plant is their price. The JET
analogy behind the three-nines record is an analog argument, not a
per-pass record: campaign retention measures co-deposited wall
inventory over many recycles, not single-transit loss, and none of the
separation slip a per-pulse reprocessing plant adds (Brezinsek et al.
2013).

Away from the basis the closure partitions the operating space into
three regimes: low burnup with confined tritons (f_D at or below about
7e-4 keeps f_T under 1%), the regime the patent point occupies, whose
price is the recycle and pumping cost above; high burnup with prompt
triton loss, where the 1.01 MeV triton escapes the small-s plasmoid
before thermalizing and preserves the store at any burnup for about
1 MeV per breeding event; and high burnup with thermalized tritons
(dhe3_f_T = 0.78 at burnup 0.15), where the extrapolation stack at the
vendor chamber reads 49.6 $/MWh and the speculation device 14.1 $/MWh,
plant neutron power rises about 5x with a dominant 14.1 MeV component,
and the decay store shrinks to 0.2-0.3 t. Which regime the
reactor-scale machine occupies is set by its compression density, which
the patent table may understate.

### 5.3 The burnup axis

Both species' per-pass burn fractions derive from the same n tau, so
the axis is swept coherently: burn_fraction_he3 scales with
burn_fraction at the fixed 70 keV reactivity ratio (3.3x). Figure 4
shows the result under both triton fates at exhaust recovery 0.99,
0.999, and 0.9999. At the patent-density basis the recovery nines
carry everything: 12.0 $/MWh at fr = 0.9999, 18.3 at 0.999, 88.9 at
0.99 (the fourth nine is worth 6 $/MWh, the third 71 $/MWh). The
sweep starts at the basis; below it, a lower reactor-point field cuts
per-pulse burnup as B^2 and is the dominant open risk: a 10 T reactor
point adds about 4 $/MWh to the headline floor and a 5 T point about
21 $/MWh. Moving right along the axis, i.e. toward higher compression
density, the
recovery requirement relaxes: above per-pulse burnup of about 3e-3
the three- and four-nines curves converge near 11.0-11.2 $/MWh on
the prompt-loss branch, and the axis minimum (11.0 $/MWh, at burnup 0.15
to 0.3) sits about 1 $/MWh below the basis. The thermalized branch
turns up past burnup 0.01 as the tritium burn grows (13-90%), so the
triton-fate question reopens exactly where the recovery question
closes. Per-pulse exhaust pumping is priced across the axis and peaks
at the basis (78 M$ per module at the floor: 8300 pumped particles
per reaction).

![The burnup axis](figures/fig4_burnup.svg)

*Figure 4: LCOE at the speculation device across the per-pulse
burnup axis under the two triton fates and three exhaust-recovery
grades; the patent-density basis (dotted) is the hardest point for
fuel recovery.*

### 5.4 Neutron damage, the unshieldable throat, and the consumable core

The base model cannot see neutron damage for this concept (its core
lifetime parameter is inert), so the scan reprices it: replacement of the
exposed package is levelized from the 14-MeV-equivalent neutron wall
load (10 dpa per MW yr/m^2 in Fe-based structure; the 2.45 MeV D-D flux
folded at 0.4) at tolerances of 20 dpa (the demonstrated RAFM database
edge) and 50 dpa (the DEMO-class design target). Both sit well below the
1costingfe design basis for D-T steel (200 dpa at 18 MW yr/m^2, the
ARIES figure), so the adders below scale inversely with the tolerance
a reader prefers, and at the design-basis tolerance they are a
quarter of the 50 dpa values. The event carries both
the wall and the close-coupled coils (106 + 14 M$ at the speculation
device), since nothing 0.10 m behind the wall outlives it. At the
patent basis the spectrum is pure 2.45 MeV D-D at a 14-MeV-equivalent
load of 0.20 MW/m^2, and the replacement adder is modest
(+0.3-1.2 $/MWh at 50-20 dpa). The damage story reopens only in the
high-burnup counterfactuals: if the reactor-point density pushes
per-pulse burnup toward the 0.1 regime with thermalized tritons, the
all-in gap between prompt-loss and thermalized reaches 8-16 $/MWh,
and on the extrapolation stack's divertor-class wall (2.5 M$/m^2, at
the vendor chamber) thermalized high-burnup replacement is prohibitive
(+63 to +164 $/MWh). Keeping the tritium out of the burn is therefore free
insurance at the basis and worth double digits off it.

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
local load; a localized audit would roughly double the damage
adders.

The replacement schedule has a structural threshold. The exposed
package (wall, coils, vessel shell) is 155 of about 370 M$ of
per-module reactor hardware; replacement of the wall-and-coil event
(120 M$) outspends the module's own capital service when its interval
falls below about 10 years at the speculation grade's 3% real cost of
capital (5 years at 7%). At the patent basis (D-D spectrum,
0.20 MW/m^2 equivalent) the interval is about 10 to 25 years at 20 to
50 dpa: a capital asset at the design target, at the edge of one at the
RAFM database edge. That interval also enters the plant's availability
(Section 3): the 84-day changeout every 25 years at the speculation
device costs 0.9% of its output, against every 22 years at the records
device's 20 dpa and every 41 years at the extrapolation device. The
consumable-core regime (1-3 year intervals, half the module's value
swapped near-annually) belongs to the high-burnup thermalized
counterfactual. In that regime the coherent design is a swappable
irradiated cartridge with hot-spare bays in a multi-module park (about
one spare module of extra capital) and a few hundred tonnes per year of
activated steel and copper that neither the decommissioning provision
nor the remote-handling account is scoped for; its economics are
marginal-manufacturing economics, where a fleet-learning term would
finally bind on something real.

### 5.5 The He-3 balance and the observed market

The fuel account charges every primary D-He3 event as purchased He-3
(1 - dd_frac per event) and credits prompt bred He-3 through its
species-resolved cumulative recycle fusion probability (0.80 at the
per-pulse basis: He-3 burns out of the loop 3.3x faster per pass than
it leaks). What it never credits is the decay store's He-3 return,
0.42 atoms per primary event, equal to the prompt branch. Without it
the machine imports about 35 kg/yr of He-3; crediting it flips the
plant to a net exporter. The question is not academic. The government
price is the DOE Isotope Program's allocation, 600 $/L to federal users
and 1,000 $/L to commercial users in 2011 (CRS R41419), 4.5 and
7.4 M$/kg, and that is 2011 data: prices have risen substantially
since. The recent commercial transactions (2024-2026: spot near
$2,500/L per the Edelgas Group; Interlune's DOE Isotope Program and
Maybell Quantum agreements priced "at today's commercial market price";
TAE's unpriced Black Moon lunar supply option) sit at 19-22 M$/kg on
gram-to-kilogram volumes, four to five times the 2011 allocation, with
every new entrant building toward the high price. The 2 M$/kg used here
sits below both, and the speculation entry 9x below the 2011
allocation. At the 2011 allocation of 4.5 M$/kg the extrapolation
device reads 44.5 $/MWh at the D-rich mix and 74.7 $/MWh
lean under the model's accounting, at the commercial spot 112 and 259,
against 24.9 $/MWh at the full self-supply limit; the distance between
those numbers is the value of the crediting decision, coupled to
the burnup closure because the decay return exists only if the tritium survives
the pulse. A by-product observation: a kilogram of He-3 burned at the
floor produces about $1.8M of electricity but sold for $4.5M at the
2011 allocation and sells for $19-22M on the commercial market today,
so an early breeding plant maximizes value selling He-3 into the thin
cryogenics and quantum market until fleet supply floods it.

### 5.6 The breeder as the price of He-3

Every device buys the He-3 it does not breed (187, 98, 35, and 25 kg/yr
down the ladder) at the ledger's 2 M$/kg, 0.5 M$/kg at speculation, a
price no market supports. The patent lets the
harvested He-3 fuel "the same or a different fusion reactor", so a
dedicated deuterium breeder can replace that assumption with a
derivation: the purchased He-3 costs what the breeder's ownership,
tritium plant, and power come to per kilogram delivered.
`scripts/breeder_loop.py` prices that breeder per device and re-runs
the device at the result.

**The breeder is the D-rich power module with its He-3 top-up removed.**
At dd_frac 0.85 the device is already 85% D-D by event count.
Formation, merging, and compression act on ion pressure, not on the
species carrying it, so a pure-D fill reaches the same density and
temperature in the same hardware, and its yield is the device yield
scaled by the reactivity ratio at the 70 keV calibration: 0.30 on the
D-rich shots, 0.18 on the vendor's, where removing the He-3 takes more
of the energy with it. Prompt He-3 and tritium are pumped
out every pulse, so each D-D event returns one He-3 atom, half of it
after the 17.8-year mean tritium life (a breeder that burns its prompt
He-3 in place instead is the device minus its purchased 15%, and
exports only the decay half). The expansion chamber stays, because the
thermalized share of the driver energy (Section 6) returns only through
it. The power table is the model's own pulsed chain at the device rep
rate; the per-module cost is the device's own, from the
reactor-plant-equipment share (co-sited in the park) to the full
per-module share (a standalone plant), a conservative basis since a
breeder needs a smaller recovery store and no He-3 injection; the
tritium plant is the constraint-4 adder at its neutron power.

**Neutrons follow the He-3, not the machine.** Half a 2.45 MeV neutron
per D-D event and one He-3 per event make 1.225 MeV of neutron per He-3
bred, 1.31 MW per kg/yr, wherever the breeding happens. The breeder's
neutron fraction is 34% against the D-rich device's 8.6%, but its
fusion power is 0.30 of the device's, so per module it carries the
device's neutron power times 1.18 (the density gain from removing the
He-3 ions) on the same chamber, 0.24 MW/m^2 in 14 MeV equivalent
against the 0.20 of Section 5.4, whose conclusion it inherits: no
shield in the compression section, sacrificial coils on the wall
schedule, worth 0.01-0.04 M$/kg at the speculation breeder. The
fraction bites on the energy balance instead, since a third of the
fusion energy leaves as neutrons the inductive path cannot recover:
the gain is 0.46 on the vendor shot, 0.77 on the extrapolation
device's, 3.0 on the speculation device's.

**Unit cost.** Module cost plus throughput tritium plant plus net power
at the device's own LCOE, divided by the He-3 delivered, with the
device re-run at that price (a fixed point on the power price). The
power term is a cost on the vendor shot, where the breeder consumes
5.5 MW per module, and a credit at the three other grades (3 MW per
module exported on the records shot). Financing the
17.8-year wait at the grade's own cost of capital values the delayed
half at 0.45 of prompt at 7% real (0.53 at 5%, 0.65 at 3%), which
raises the unit cost by 1.4x at the records and vendor grades (where
at the vendor grade the power price feeds back), 1.3x at
extrapolations and 1.2x at speculation.

| device | He-3 bought (kg/yr) | ledger price (M$/kg) | He-3 line at ledger price ($/MWh) | breeder unit cost (M$/kg) | LCOE at breeder price ($/MWh) | ladder LCOE ($/MWh) |
|---|---|---|---|---|---|---|
| citable records | 187 | 2.0 | 47.6 | 1.92-2.18 | 149.6-155.8 | 151.5 |
| Helion's requirements | 98 | 2.0 | 24.8 | 6.5-7.4 | 165-175 | 108.4 |
| extrapolations | 35 | 2.0 | 8.7 | 0.65-0.98 | 27.7-29.1 | 33.6 |
| speculation | 25 | 0.5 | 1.5 | 0.18-0.52 | 11.0-12.0 | 12.0 |

| device | breeder gain | He-3 output per module (kg/yr) | ownership (M$/kg) | tritium plant (M$/kg) | power (MWh/kg) | power at device LCOE (M$/kg) | unit cost (M$/kg) |
|---|---|---|---|---|---|---|---|
| citable records | 1.08 | 13.0 | 2.11 | 0.09 | -1,890 | -0.28 | 1.92 |
| Helion's requirements | 0.46 | 5.6 | 5.16 | 0.09 | +7,790 | +1.28 | 6.53 |
| extrapolations | 0.77 | 27.1 | 0.72 | 0.06 | -4,440 | -0.12 | 0.65 |
| speculation | 3.0 | 133 | 0.27 | 0.04 | -12,000 | -0.13 | 0.18 |

Bands run from a co-sited to a standalone breeder at an equilibrium
store; the breakdown is the co-sited case, power positive when
consumed. The ledger's 2 M$/kg is what a records-grade breeder
charges (1.9 co-sited, 2.2 standalone); at the vendor grade it is
unexplainable by a factor of three, since a module that makes 5.6 kg/yr
costs 5.2 M$/kg to own before its power bill; at the extrapolation
grade a breeder charges about 0.65 M$/kg; and the 0.5 M$/kg speculation
entry sits inside its band, near the top (0.18 co-sited, 0.52
standalone). Each 10 $/MWh on the breeder's power moves the
vendor-grade unit cost by 0.08 M$/kg and the speculation-grade one by
0.12 M$/kg the other way.

**Siting.** At the records and vendor grades a device needs 15-18
breeder modules and siting changes nothing. At the two cheaper grades a
central facility differs from a co-sited breeder in three ways:
granularity (the speculation-grade module makes 133 kg/yr against a
purchase of 25, so a co-sited whole module is five times oversized),
the model's own standalone fixed cost (21-42 M$/yr with the
tritium-plant core: 1.2-1.6 M$/kg over one device's purchase, about
0.1 M$/kg by ten), and power valuation (the speculation breeder exports
12,000 MWh per kilogram, so a facility selling above the park's own
LCOE drives its He-3 line toward zero).

| device | co-sited, marginal (M$/kg) | co-sited, whole modules (M$/kg) | central facility, 1 device | 5 devices | 20 devices |
|---|---|---|---|---|---|
| citable records | 1.92 | 2.03 (15 modules) | 2.23 | 1.97 | 1.93 |
| Helion's requirements | 6.10 | 6.29 (18 modules) | 6.61 | 6.17 | 6.12 |
| extrapolations | 0.63 | 1.06 (2 modules) | 1.78 | 0.84 | 0.69 |
| speculation | 0.17 | 0.98 (1 module) | 1.73 | 0.35 | 0.22 |

One device is one GWe of self-supply plant; power at the ladder LCOE,
so the vendor row reads 6.1 here and 6.5 at its fixed point. A
facility needs about five devices behind it to match a co-sited
breeder at the extrapolation grade and twenty to approach the marginal
price; at the speculation grade the answer is a fleet facility of five
devices or more. Surplus He-3 serves more plants, lets the burners run
leaner (free He-3 makes the lean mix cheaper than the D-rich one, 21.3
against 24.9 $/MWh at the extrapolation grade), or is banked, since
He-3 is stable and tritium can stay in the store. Banking is also the
answer to the decay lag: a fleet growing at rate g receives the delayed
half at lambda/(lambda + g), so breeders must lead the fleet by
1.3-1.6x at 5-20%/yr growth.

Closing the loop the other way, lean power modules fed by breeders
inside the park, gives a similar reading: 28-36 $/MWh at the
extrapolation grade against 33.6, 11-15 at speculation against
12.0, 149-230 at the vendor grade against 108.4. The scheme relocates
the tritium inventory rather than shrinking it (0.5-3.1 t per lean GWe
moves to the breeder site), which is where Section 5.4's swappable
cartridge and a single licensed bulk-tritium site belong. Three
simplifications cut in known directions: the breeder inherits the power
module's cost; a pure-D fill at fixed pressure would carry about 10%
more ions; and at fixed driver energy the D-D yield per shot scales as
the square of the compression field, so a purpose-designed high-field
breeder is unpriced upside.

## 6. Recovery physics: what the circuit actually gets back

The composite cap (constraint 2) already prevents the double-booking of
conversion efficiencies. Two further effects sit beneath it.

**Driver thermalization.** The machine has no auxiliary heating:
merging shock and compression work are the heating, all driver-fed. The
model's conversion path nonetheless recovers the entire delivered
driver energy at the flat inductive efficiency, as if it all remained
in field form. The plasma-thermal share chi can only return through the
same expansion channel as the fusion heat, at f_pdv, on an adiabat
already degraded by the deliberately irreversible merging. chi is not a
free parameter: at peak compression, radial equilibrium and the FRC
average-beta theorem (<beta> = 1 - x_s^2/2; Tuszewski 1988) fix it as
a function of the separatrix-to-coil radius ratio alone,

    chi(x_s) = 1.5 <beta> x_s^2 / (1.5 <beta> x_s^2 + 1 - x_s^2),

giving chi = 0.30 / 0.52 / 0.71 at x_s = 0.5 / 0.7 / 0.85. Fat FRCs
are high-chi machines: good confinement physics pushes the derate up.
The extra recirculating loss eta_dec chi (1 - f_pdv) p_driver is worth
+2.0/+3.4/+4.7 $/MWh at the extrapolation device across that x_s span
(the gain-2.6 machine circulates 986 MW of driver power, and the
radial-only f_pdv widens the uncaptured channel),
+0.03 to +0.08 $/MWh at the speculation device, and order +10 $/MWh
at the low-Q Helion device. It is carried
as a reconciliation adder pending a model-level treatment.

**The yield bound.** The same chi bounds the shot. The plasma at peak
compression holds chi E_del at the energy density of a beta = 1 plasma,
1.5 B^2/2mu0, and burns at the fusion power density of the burn point,
so

    gain <= chi x burn time / breakeven time,

with the breakeven time the ratio of those two densities (Lackner et
al. 2026; the pulsed gain of Nicolas et al. 2026, fusion energy over
plasma energy, is the same ratio against their Lawson time). At the
patent point (n_D 0.75e22 m^-3, He3/D 0.158, 70 keV, 22 T, Bosch-Hale
rates) the breakeven time is 86 ms with thermalized electrons, and
3.7 times shorter if the electrons could be held at a tenth of the ion
temperature, which they cannot be for long: the ion-electron
equilibration time at that density is about 1 ms (Lackner et al. 2026,
who show the ratio erodes well inside the breakeven time and that a
thermalized state is the realistic assumption for a burning D-He3
plasma; the vendor's reply, that the pulse is over before
equilibration, concedes the timescale). Against the vendor's stated
pulse of hundreds of microseconds to milliseconds (Helion FAQ, June
2026) the bound reads: a 1 ms burn returns 0.2 to 0.4 MJ from the
50 MJ bank across x_s 0.5 to 0.85, less than the circuit loses per
shot at any eta_dec in the ladder; the design-basis 128 MJ shot needs
0.3 to 0.7 s, which falls to the patent table's own tenth-of-a-second
class only with cold electrons throughout; the speculation shot needs
1 to 3 s. Trenta's record is lifetimes above 1 ms. The bound also reproduces
the co-founder's own D-T design: Slough (2025) quotes a gain of 9.1 on
the FRC energy over a 2 to 5 ms transit at 34.8 T and 15 keV, and at
that point's breakeven time the same arithmetic gives a 3.4 ms burn.
This is constraint 7, and it is why the shot is a graded claim rather than a
shared basis; `scripts/yield_bound.py` prints the bound, and every
point the scripts evaluate carries the burn time its shot implies at
x_s 0.7. It is also the thin-cycle argument of Nicolas et al. in this
study's variables: with the plasma holding chi of the magnetized
energy and the burn a fraction of breakeven, the fusion surplus per
pulse is a small fraction of the energy the circuit swings, and the
round-trip circuit efficiency must exceed 1 - gain for any net work at
all. Two independent reconstructions of the vendor's reactivity curve
find its fusion-to-bremsstrahlung ratio 3.6 to 9 times too favorable
(Nicolas et al. 2026, Table 1) or about an order of magnitude (Lackner
et al. 2026), which is the provenance of the 0.05 radiated fraction
that constraint 1 withdrew.

**The expansion-ratio bound, and the cycle it belongs to.** The
machine is a heat engine with magnetic pistons: adiabatic magnetic
compression, compression ignition with no external heater, heat
addition at roughly constant pressure (the beta = 1 force balance pins
plasma pressure to the crowbarred field, so fusion heating expands the
plasmoid rather than raising its pressure), adiabatic over-expansion
into a chamber far larger than the compression volume, and open-cycle
exhaust. In engine terms that is a Diesel-type cycle with an Atkinson
expansion stroke, and it is the vendor's own framing: the cited burn
cycle framework (Kirtley 2024; slides archived in `docs/sources/`)
derives fusion-inclusive efficiencies for generalized Otto and Diesel
cycles with the over-expansion as an extra factor, finds the Otto form
independent of gain while the Diesel form carries a gain-dependent
cutoff penalty, and quotes about 60% for a constant-pressure burn and
above 90% for optimal cycles. The vendor's FAQ (June 2026) cites
Nicolas et al. (2026) for recovery "exceeding 95%"; the figure in that
paper is its ideal Carnot-form bound at a temperature ratio of 40 under
full adiabaticity, which the paper then sets aside on the thin-cycle
argument and finds insensitive to the Otto or Diesel choice. Slough
(2025), the co-founder whose patent supplies the fuel cycle, derives
40% as the most an ejected FRC can return in a flux-conserving
expansion chamber, where it comes to rest in equilibrium at a radius
ratio x_s holding 1.5 pV of thermal energy against the field it has
compressed (recoverable share (1 - x_s^2)/(2.5 - x_s^2)), and states
that an FRC does not free-expand. That is his own recovery topology,
not the discharged compression coil this work's f_pdv assumes, so it
is carried as a risk row rather than a cap: at f_pdv 0.4 the
extrapolation device reads 59.3 $/MWh (+25.7) and the speculation
device 18.0 (+6.1). There is no Carnot exemption in this:
the cycle's efficiency is set by its form, its compression and
expansion ratios, and the entropy generated in the deliberately
irreversible merging (the chi derate above), which is what the
composite cap encodes. Constraint 6 enforces the adiabatic-stroke bound
1 - (V_i/V_f)^(2/3), with V_i = E_del/(B^2/2mu0), about 0.26 m^3 at
50 MJ and the 22 T basis field. The exponent is the plasma channel's
gamma = 5/3 rather than the vendor's lumped plasma-plus-field 1.8,
because field energy is recovered separately through eta_dec and the
lumped index would raise the cap; the isobaric burn leg makes the true
Diesel-form value 1-2 percentage points lower, so the enforced
expression is a strict, slightly generous cap. Applied per point: the
extrapolation device's 10 m x 1.5 m chamber delivers a derived f_pdv
of 0.78, and the speculation device's 30 m x 1.5 m chamber supports the
claimed 0.947 (cap 0.989) only because the axial channel is granted
there. The large chamber buys expansion ratio, not merely wall area,
and recovery cannot be improved without more chamber.

**The parallel channel.** The expansion work is not all radial, and the
components couple to the circuit differently. Radial expansion
compresses flux against the main coil: the cleanly captured channel.
Axial elongation pushes the diamagnetic plasmoid against the end-field
gradient, changing flux linkage through the end and adjacent coils:
capturable only if those circuits are switched for recovery during the
stroke, a design choice. Parallel particle streaming along open field
lines (the exhaust) couples to nothing and lands in the undirected
residual. FRC adiabatic scalings (r_s proportional to B^-2/5, length
to B^-1/5; Spencer et al. 1983, Tuszewski 1988, Kirtley and Milroy
2023, and the coupling the vendor's own talk invokes: radial
compression pulls the FRC in axially, per the Spencer scaling) put the
axial share of the boundary work near 1/5, and a self-similar cylinder
bounds it at 1/3. This is the radial share of constraint 6, 0.8 at the
records and extrapolation grades. The share can be raised without
switched circuits: static end-field gradients, which the published
symmetric geometry's high-field end sections already provide, can
suppress the axial channel and force the work radial, at the price of
forced oblateness pressing on the tilt-stability boundary. The
extrapolation-to-speculation recovery step is exactly the claim that
the axial channel is captured or suppressed, priced and measurable on
the shot sequence below.

**Measurement protocol.** A three-shot sequence on Polaris separates
the whole chain: a vacuum shot measures eta_dec alone; a plasma no-burn
shot returns eta_dec[(1 - chi) + chi f_pdv], so its deficit against
vacuum measures chi(1 - f_pdv); a burning shot adds the fusion
composite, and its yield reads constraint 7 directly. This single
protocol prices the composite cap, the thermalization share, the shot,
and (through the wall budget) the rep-rate ceiling; published
excluded-flux radii pin chi per shot in the interim. It is the vendor's
own stated proof point: its FAQ defines demonstrating electricity from
fusion as showing that energy returned to a capacitor bank came from
fusion-driven expansion "rather than only from ordinary inductive
coupling in the circuit". Until April 2026 the same page said that no
results on energy recovery with plasma present had been released; the
June 2026 rewrite says high-efficiency magnetic energy recovery has
been measured on seven prototypes and gives no figure.

## 7. Plant architecture: modules, parks, and the small-plant penalty

Two controlled sweeps at the speculation stack (constant gain, constant wall
loading, driver and chamber scaled with module power) separate module
count from plant size. **Module count at fixed plant size is nearly
free, and mid-size modules carry a mild bonus**: a park of
500 MWe modules reads 11.5 $/MWh against the single 1 GWe module's
12.0 $/MWh (the adiabat-priced coils reward smaller compressed
volumes; 250 MWe modules read 11.6), and even 50 MWe modules cost only
three tenths of a dollar more (12.3), because buildings, supplementary capital, and balance of
plant price plant totals; the only modularity tax is per-module fixed
items, biting below about 100 MWe. **Standalone
plant size is expensive**:

| plant | LCOE ($/MWh) | $/kW | dominant penalties |
|---|---|---|---|
| 1 GWe | 12.0 | 1488 | - |
| 250 MWe | 18.9 | 2262 | fixed site buildings, staffing^0.5 |
| 50 MWe | 44.6 | 6325 | O&M 17.2 $/MWh (staffing law), 141 M$ of buildings, tritium-plant fixed core |

![Module size, park vs standalone](figures/fig5_plant_size.svg)

*Figure 5: The same physics sold two ways at the full speculative
stack. Module size in a 1 GWe park is nearly free; standalone plant
size is expensive, and the 50 MWe standalone unit costs 3.9x the park
floor.*

The penalty decomposes into three mechanisms: about 138 M$ of fixed
site buildings calibrated on fission-class analogs (an analog-class
question for a factory-shipped unit on an industrial pad); the P^0.5
staffing law (INL sodium-fast-reactor staffing basis; no documented
record yet supports remote fleet operation of a fusion-class plant);
and the absence of any fleet-learning term on equipment, the one
mechanism that could make mass-produced small units positively
cheaper, which must be anchored beyond the fleet size the NOAK
constants already assume or it double counts. The in-model conclusion
is unambiguous: this concept's economics live in power parks, and a
50 MWe module is a manufacturing choice the model neither rewards nor
punishes at park scale.

## 8. What reaches $10/MWh, and what carries it

The full speculation stack reaches the target only as a 3 GWe park
(9.7 $/MWh; 12.0 at 1 GWe), and the entry that carries it across is its
financing: at the design-basis 7% real the same machine reads
15.8 $/MWh (19.0 at 1 GWe), so the 3% real cost of capital,
sovereign-class money with no mechanism behind it, is worth more than
the whole distance to the target. No physics or engineering entry
crosses it on its own, and the crossing also needs the derived
availability of 0.92: at the model default of 0.85 the park reads
10.3 $/MWh and at 0.95 it reads 9.5, so the target holds for
availability above about 0.90 and, like every number here, only with
the vendor's shot granted (the park's 200 MJ pulses are a burn of half
a second to a second at the patent point). Beyond the stack, in
decreasing order of plausibility:

- **He-3 at effectively zero cost** (8.2 $/MWh at 3 GWe): a mature
  breeding economy or an external supply two orders below the observed
  market. Section 5.6 prices the breeding economy itself: a
  speculation-grade breeder delivers He-3 at 0.2-0.5 M$/kg, and only a
  fleet facility that sells its power drives the line toward zero.
- **Gas-class site and decommissioning analogs** (about 2 $/MWh at
  1 GWe, the whole of the buildings and CAS50 lines): defensible only
  for the He-3-lean machine; the D-rich machine's tonne-class tritium
  inventory argues the other way.
- **A real fleet-learning term** on equipment, anchored beyond the NOAK
  reference fleet: the only mechanism that rewards the mass-produced
  small-unit strategy at all.

None of these is in the evidence base at any grade.

## 9. Caveats that survive into the headline

- Every number in the ladder grants the vendor's shot, which no record
  supports and whose implied burn is three orders beyond the vendor's
  stated pulse; on evidence alone the machine makes no net power.
- The two cheaper devices carry their tier's cost of capital (5% and
  3% real) and the 80-year civil-works book life; their physics-and-
  engineering reading is the at-7% column, and it is the 3% rate, not a
  technology entry, that takes the 3 GWe park under $10/MWh.
- No extrapolation entry is a measured record: the two co-dominant levers
  (per-pulse fuel recovery, capacitor life) and the next two (rep
  rate, burn mix) are respectively an extrapolated analogy, a
  published target, a roadmap paraphrase, and a sweep endpoint.
- The speculation stack is jointly, not just individually, heroic: 0.1 $/J
  capacitors and 1e10-shot life together contradict the derating
  physics that connects capacitor cost to life; the composite sits at
  the theory optimum with zero margin; three-nines exhaust recovery
  becomes load-bearing at low burnup; the 500 MJ shot is a burn of
  seconds at the patent point.
- The headline floor is conditional on the patent-basis compression
  field: per-pulse burnup falls as B^2, so a 10 T reactor point adds
  about 4 $/MWh and a 5 T point about 21 $/MWh (Section 5.3). It is
  conditional too on the discharged-coil recovery topology: at the 40%
  ceiling Slough (2025) derives for a flux-conserving expansion chamber
  the speculation device adds 6.1 $/MWh and the extrapolation device
  25.7 (Section 6). The
  neutron-damage adders are more likely low than high
  (fission-spectrum dpa data, an order of magnitude more helium per
  dpa at 14 MeV, uniform-cylinder averaging over a localized burn).
- Model gaps priced in the bands but excluded from the headline:
  HVDC-class switch duty, tritium-plant scope, driver thermalization.
  The main conservatism cuts the other way (no thermal bottoming in the
  basis, worth -6.5 $/MWh at the extrapolation device).

## 10. Conclusions and measurement priorities

The cheap numbers rest on a small set of unmeasured properties,
ranked here by the $/MWh they gate:

1. **The shot** (the whole plant): the yield of a burning Polaris
   pulse at its measured dwell, read against constraint 7; the vendor's
   stated proof point, energy on the bank
   from fusion-driven expansion, is the same measurement.
2. **Capacitor cost-at-life** (tens of $/MWh): a sourced curve
   replacing the single derating target, resolving the joint optimism
   of 0.1 $/J with 1e10-shot life.
3. **The recovery chain** (5 to 26 $/MWh at the extrapolation grade,
   the top of the range at Slough's 40% ceiling): the Polaris shot
   triplet, whose no-burn deficit says whether the share sits at the
   flux-conserver 0.4 or the adiabatic 0.8.
4. **Per-pulse burnup, extraction, and fuel recovery** (6-16 $/MWh):
   the patent fixes the design intent, low per-pulse burnup with
   inter-pulse tritium removal, but a patent is design intent, not a
   measurement; the reactor-point compression density and field, the
   demonstrated per-pulse separation rate, and the per-pass fuel
   recovery (four nines required at the published operating point) fix
   the neutron spectrum, the wall-replacement schedule, and the
   fuel-cycle cost between them.
5. **A duty-cycle basis for multi-Hz operation** and **a costed
   tritium-plant scope** for the D-rich cycle (single $/MWh each, but
   licensing-defining).

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
produce every number, every figure and the HTML renderings of this
page and the ledger (the README says what each one does),
the evidence ledger, the adversarial review, the capacitor evidence,
and the vendor slide and FAQ captures. The cost model is `1costingfe` at commit
44434d9. Fifty-one regression tests pin all four devices at both
plant sizes, the stack evaluations at the vendor configuration, the
tritium-burn closure, the yield bound with the burn time every point
implies and its D-T cross-check, the recovery ceiling, the chi(x_s)
anchors, the breeder unit cost, the
availability derivation, the financing ladder, and the three-part
partition of the LCOE behind Figure 1, and fail loudly if the model
moves under this work.

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
  one for "we have not released results overviewing our energy
  recovery with plasmas present" and "electricity by 2028", the later
  one for the required confinement "on the order of hundreds of
  microseconds to milliseconds", the equilibration reply, the recovery
  "exceeding 95%" citing Nicolas et al., and the proof point for
  electricity from fusion). Microsoft power purchase agreement
  announcement (2023).
- Axios Pro (2026). "Helion hedges on how soon it expects to sell
  electricity from fusion," 8 September 2026 (the withdrawal of "net
  electricity" from the vendor's stated goals).
- Kirtley, D. (2026). Series G final close at $500M, 15 September 2026
  (x.com/dkirtley); initial close of $465M on 4 June 2026 led by Thrive
  Capital at a $15.5B post-money valuation.
- Helion Energy (Slough, J., Kirtley, D., and Pihl, C.). "Advanced fuel
  cycle and fusion reactors utilizing the same," priority 7 February
  2014, filed 6 February 2015, published as US 2017/0011811 (2017),
  granted as US 11,469,003 B2 (11 October 2022): the
  breed-extract-store-decay fuel cycle and its operating table (70 keV,
  22 T, 72 MW at 1 Hz, confinement 0.157, 0.103 and 0.088 s across its
  three columns). Used as design intent, not as a record; see
  Section 5.2 and constraint 7.
- IEA/NEA (2020). Projected Costs of Generating Electricity, 2020
  edition (3%, 7%, and 10% real discount rates, 7% central).
- Kirtley, D. (2024). "Fundamental theory of the direct magnetic
  energy recovery in a thermonuclear field reversed configuration
  system." APS DPP 2024, abstract GO05.8; slide captures in
  `docs/sources/` (the composite-recovery figure behind constraint 2
  and the Otto/Diesel burn-cycle expressions behind Section 6).
- Kirtley, D., and Milroy, R. (2023). "Fundamental scaling of
  adiabatic compression of field reversed configuration thermonuclear
  fusion plasmas." Journal of Fusion Energy 42, 30.
- Lackner, K., Burhenn, R., Fietz, S., von Müller, A., and Ball, J.
  (2026). "Comments on the Paper 'Fundamental Scaling of Adiabatic
  Compression of Field Reversed Configuration Thermonuclear Fusion
  Plasmas'." Journal of Fusion Energy 45, 12 (ion-electron
  equilibration against the fusion breakeven time; the vendor's
  bremsstrahlung about an order of magnitude below the standard
  expression).
- Langtry, A., et al. (2025). "Affordable, manageable, practical
  Z-pinch driver (AMPS)." arXiv:2504.10680 (capacitor derating and
  shot-life target).
- Nicolas, T., Goupil, C., Herbert, E., and Ball, J. (2026). "The
  Challenge for Adiabatically Heated FRC Based D-3He Fusion." Journal
  of Fusion Energy 45, 24 (the pulsed gain as fusion energy over plasma
  energy, the Lawson bound B^2 tau >= 1.4 (2 + 3 T_e/T_i)^2, the
  plasma's 1e-2 share of the magnetized energy and the thin
  current-flux cycle, Table 1 against the vendor's reactivity curve).
- Rubin, T. (2026). 1costingfe: a bottom-up fusion power plant cost
  model. Repository at commit `44434d9`.
- Slough, J. (2025). "A compact fusion reactor based on the staged
  compression of a field reversed configuration." Nuclear Fusion 65,
  106019 (open access; the 2026 corrigendum replaces figure 36 only):
  the self-sustained cycle's He-3 fraction of roughly 0.16, citing the
  fuel-cycle patent; the D-T design point (34.8 T, 15 keV, gain 9.1 on
  the FRC energy over a 2 to 5 ms transit); the 40% recovery ceiling of
  a flux-conserving expansion chamber (its equation 18).
- Spencer, R. L., Tuszewski, M., and Linford, R. K. (1983).
  "Adiabatic compression of elongated field-reversed configurations."
  Physics of Fluids 26, 1564 (the FRC adiabatic compression scalings
  behind the radial-axial work partition).
- Thea Energy (2025). "Overview of the Helios Design: A Practical
  Planar Coil Stellarator Fusion Power Plant." arXiv:2512.08027 (one
  84-day planned outage every two years; coils shielded to a 40-year
  minimum life).
- Tuszewski, M. (1988). "Field reversed configurations." Nuclear
  Fusion 28, 2033 (FRC equilibrium, average-beta theorem, adiabatic
  scalings).
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
  Interlune-DOE Isotope Program and Interlune-Maybell Quantum
  agreements (2025); TAE Technologies and Black Moon Energy Corporation
  helium-3 supply option (2026).
- Idaho National Laboratory. Advanced-reactor staffing studies (the
  P^0.5 O&M scaling basis).
