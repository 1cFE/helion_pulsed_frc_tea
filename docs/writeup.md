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
One of the best physical mechanism for directly interacting with the plasma
is inductive recovery: a coil-driven magnetic field compresses the
plasma, and the plasma then expands against that field much as the gas
in an engine expands against a piston.
That is what Helion Energy is building, so this work takes Helion's
published design and results as its starting point and builds the
argument on them.

Helion Energy has made a compelling case to its investors, raising
about $1.5B, and has already secured a power purchase agreement with a
customer. Markedly, it states a long-run ambition of electricity at
1 cent/kWh ($10/MWh), and that figure is what the 1cFE residency at
Astera is set on investigating.

Helion realizes inductive recovery in a pulsed linear device:
coils generate an external axial field, and the plasma
is formed within it as two field-reversed configuration (FRC)
plasmoids. These are accelerated toward each other and merged, the
collision converting their directed kinetic energy into ion heat. The
resulting single hot FRC is then compressed to fusion conditions by
raising the external field. An important feature of the FRC is used
here: radial and axial compression are coupled, so a radial compression of the FRC causes also an axial compression.
The fusion heat released at burn causes an
isobaric expansion. That expansion returns the driver energy and part
of the fusion energy to the capacitor banks through the same coils.
This is a Diesel-type thermodynamic cycle with an Atkinson
over-expansion stroke, because the FRC is allowed to expand past its initial state.

The costing uses the `1costingfe` bottom-up cost model, built on
publicly available data and labeled extrapolations; the open-source
code is available [here](https://github.com/1cFE/1costingfe),
with detailed documentation
[here](https://files.1cf.energy/1costingfe_paper.pdf).

This work is divided into the following parts: in Section 2 we first
describe Helion's device and its subsystem requirements from the
available published material. In Section 3 we define four devices which share that
architecture and differ only in the subsystem performance they are
granted. The first, citable records, grants every subsystem what
existing technology has demonstrated. The second grants the
performance Helion's own materials imply, taken at face value. The
third and fourth, extrapolations and speculation, relax the evidence
standard in two labeled steps. We use the same financing,
construction, and availability estimates for all four devices, enforce
physics constraints, and optimize each device to
its best cost. In Section 4 we report the four costs. Sections 5 and 6
then develop the two
load-bearing subsystems, the tritium fuel cycle and the recovery
physics of the driver energy, each gated by a small set of unmeasured
plasma properties that the developer's own next machine could resolve.

The four devices form a descending ladder. The citable-records device
prices the concept at about 173 $/MWh. The second device, Helion's own
configuration granted its two unrecorded performance claims (the
fourth nine of per-pulse fuel recovery and the axial share of the
expansion work), reads 118.6 $/MWh. The extrapolation device supports
about 41 $/MWh, and the speculation device sets the coherent floor:
16.8 $/MWh at 1 GWe and 13.5 $/MWh at 3 GWe. The $10/MWh target is not reached by any coherent stack,
including He-3 at zero price (10.9 $/MWh at 3 GWe). The floor is carried
by site and support infrastructure (buildings, heat rejection, staffing,
decommissioning) and by the tritium fuel cycle, not by the capacitor
driver; the machine has no turbine island at all.

The fuel cycle is anchored to the vendor's own patent (US 11,469,003
B2), whose operating table (n_D = 0.75e22 m^-3, 70 keV, and a
pressure-balance field of 22 T, adopted as the compression-field basis
and priced into the coils) specifies tritium removal between pulses. At
that point the per-pulse burnup is 1.2e-4 for deuterium and 4.1e-4 for
He-3 and the in-pulse tritium burn is under 1%, so the He-3 supply can
be idealized as self-supplied from stored tritium decay, but fuel
transits the exhaust loop of order 1e3-1e4 times before burning.
Per-pulse isotope separation at the repetition rate and per-pass fuel
recovery of 0.9999 are therefore the load-bearing engineering requirements.
That recovery is graded, not assumed: the JET-ILW retention analogy
supports three nines (0.999), and the patent-implied 0.9999 enters only as a
labeled extrapolation. A lower reactor-point field is the dominant open
risk: burnup falls as B^2, and a 10 T machine adds 6 $/MWh to the
floor, a 5 T machine 32 $/MWh. The He-3 each device buys anyway is
repriced by a dedicated deuterium breeder built from the same module,
which shows the ledger's 2 M$/kg to be an extrapolation-grade number
(Section 5.6). The expansion-work recovery is likewise derived per
design from its chamber's expansion ratio, never asserted (Section 6).

Everything here is reproducible: the four evidence stacks are YAML
configuration files, each figure is produced by a named script, and thirty
regression tests pin the ladder to a fixed revision of the cost model
(see Reproducibility).

## 2. Machine basis

The machine follows Helion's published architecture at face value
(Helion Energy technology and FAQ pages; Kirtley and Milroy 2023). Two
FRC plasmoids are formed by theta-pinch field reversal in opposed
formation sections, accelerated electromagnetically, and merged in a
central compression section, where the collision converts their directed
kinetic energy into ion heat; a subsequent magnetic compression performs
adiabatic work to reach burn conditions. There is no auxiliary heating
system of any kind: the pulsed-power driver is also the heater. After
the burn, the plasma expands against the field, returning driver energy
and charged fusion energy to the coil circuit as work; radiated
power, undirected charged power, and neutrons are not converted
(eta_th = 0 in the machine basis; a bottoming-cycle add-back is carried
in reconciliation). The chamber is a cylinder with copper pulsed coils
whose bore sits 0.10 m behind the first wall; there is no breeding
blanket and no manufactured target (the plasmoid is formed in situ).

The design-basis point takes the driver energy from the sourced Polaris
capacitor bank (50 MJ per pulse) and back-derives the per-shot yield
(101.4 MJ) from the 50 MWe power purchase agreement at 1 Hz, requiring
model consistency with the concept's own conversion parameters rather
than any disclosed measurement. At the vendor's own burn point the
same shot delivers 37 MWe per module at 1 Hz rather than the
agreement's 50, so the 1 GWe plant carries 28 modules; reproducing
50 MWe would need 128 MJ per shot (gain 2.6), which on the vendor's
0.5 m chamber exceeds the wall flash bound. The shot, not the
power-purchase figure, is held as the design point. A 1 GWe plant is
built as an integer number of Helion-class modules, with the
repetition rate and module count solved jointly from the net-power
target under a rep-rate ceiling.

The fuel cycle is Helion's stated one (US 11,469,003 B2), and so is
the vendor device's burn point: the patent's tritium-removal column,
He3/D = 0.158 at T_i = T_e = 70 keV and 22 T, with a bremsstrahlung
fraction of 0.23 and a neutron fraction of 0.06. In the model's terms
that is dd_frac 0.49, where dd_frac is the D-D share of primary fusion
events by count, not an ion ratio (a 1:1 D:He-3 plasma is 0.13, a 3:1
plasma 0.31). Running deuterium-rich (dd_frac 0.85, the mix every
design-optimized device chooses), half the D-D reactions breed tritium.
Near zero of it burns in-pulse (dhe3_f_T near zero, taken as 0 in the
basis; Section 5.2 derives the floor): the exhaust is pumped,
isotope-separated,
and the tritium is stored on getter beds to decay (12.3 yr half-life)
into the He-3 the plant burns, alongside the prompt He-3 from the other
D-D branch, which re-enters the fuel loop with a cumulative recycle
fusion probability set by the per-shot burn fraction and the exhaust
recovery efficiency. The plant therefore has no lithium anywhere; its
tritium plant is an exhaust-processing and storage plant.

## 3. Method

**Notation.** Model knobs keep their configuration-file names. dd_frac
(dhe3_dd_frac) is the D-D share of primary fusion events by count, not
an ion ratio: a 1:1 D:He-3 plasma at 70 keV is 0.13, a 3:1 plasma 0.31,
the patent's He3/D = 0.158 plasma 0.49. dhe3_f_T is the fraction of
bred tritium that burns in-pulse. burn_fraction and burn_fraction_he3
(bf) are the per-pass burn probabilities of deuterium and He-3 through
the chamber, and fuel_recovery (fr) the per-pass fraction of unburned
fuel the exhaust loop returns. f_rad is the fraction of fusion power
radiated as photons. eta_dec is the circuit efficiency of inductive
recovery, f_pdv the fraction of the plasma's expansion work that reaches
the coils, and their product the composite recovery; eta_pin is the
driver's wall-plug efficiency and eta_th the thermal-cycle efficiency,
zero in the machine basis. e_driver and the shot yield are the
per-pulse driver energy delivered and fusion energy released; f_rep and
max_f_rep are the repetition rate and its ceiling; cap_shot_lifetime is
the capacitor shot life; u_he3 is the He-3 price; c_cap is capacitor
capital per joule. chi is the plasma-thermal share of the delivered
driver energy and x_s the separatrix-to-coil radius ratio.

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

**Evidence ladder.** All four devices share a record-sourced plant
environment: financing at 4.25% from a sovereign-backed generation
precedent (Apostoleris et al. 2021), 2.5-year construction (Siemens
Energy CCGT block precedent), 8% indirects (US DOE/NETL QGESS), and
availability 0.95 (US DOE geothermal fleet data, derated for bank-swap
outages). The records device holds the two performance claims that
have no record at their evidence-supported values: per-pulse fuel
recovery 0.999, the value the JET-ILW retention analogy supports
(Brezinsek et al. 2013), and the recovery share at the radial-only 0.8
of the adiabatic work partition. The Helion device grants the vendor's
0.9999 and the full share; the extrapolation and speculation stacks add
the labeled entries listed with the results in Section 4, the largest
being capacitor life 1e9 shots (the Pacific Fusion AMPS derating
target; Langtry et al. 2025). Every entry carries a source and grade in
the evidence ledger (`docs/ledger.md`); no extrapolation entry is a
measured record.

**Coherence constraints.** Six couplings are enforced on every quoted
point: (1) the radiated fraction is a function of the burn mix through a
bremsstrahlung floor (f_rad = 0.28 at dd_frac 0.85, not the lean-mix
0.05); (2) recovery efficiency is capped as the composite
eta_dec x f_pdv (0.80 through the extrapolation grade, 0.90 at
speculation), because the only
published figure speaks to the product; (3) the wall must survive both
its steady flux (within the purchased wall class) and its per-shot flash
energy (under the tungsten millisecond-melt bound); (4) a mix at or
above the vendor's catalyzed 0.49 carries its tritium-plant
consequences, priced as a fuel-handling adder of 50 M$ fixed plus
0.657 M$ per MW of plant neutron power; (5) the in-plasma tritium burn dhe3_f_T
is floored by the burnup closure of Section 5.2, so a low-burn claim at
high per-pulse burnup is flagged as requiring prompt triton loss (at
the patent basis the floor is 0.002 and the design's zero passes);
(6) the expansion-work recovery fraction is derived per point, never
asserted: f_pdv = min(claim, share x [1 - (V_i/V_f)^(2/3)]) with V_i
the compressed flux volume at the 22 T basis field, V_f the chamber,
and share the radial fraction of the boundary work (0.8 at the records
and extrapolation grades, 1.0 at speculation and at the Helion device;
Section 6). Two further audits, developed in Sections 5 and 6, close
the fuel cycle and the driver-energy accounting.

**Design search and reconciliation.** Each device except Helion's own
configuration is the argmin of a scan over shot yield (a free
parameter only at speculation, where the scan chooses it; the records
and extrapolation devices keep the cited shot), chamber length and
radius, wall class, and burn mix, discarding
any design that violates a constraint.
Reconciliation then brackets each minimum with the model gaps it cannot
price internally (HVDC-class switch duty, the tritium-plant band, the
driver-thermalization derate) and its conservatisms (no thermal
bottoming), yielding an honest band rather than a point.

## 4. Results: the four devices and what carries the floor

| device | 1 GWe ($/MWh) | 3 GWe ($/MWh) | stack and design |
|---|---|---|---|
| citable records | 173.0 | 169.6 | fuel recovery 0.999 (JET analog), radial-only recovery share; optimum: the cited 101.4 MJ shot at 1 Hz in 10 m x 1.5 m panel-wall modules, D-rich mix with its tritium plant |
| Helion's requirements | 118.6 | 114.1 | the vendor configuration (50 MJ driver, 101.4 MJ yield, 1 Hz, the patent's catalyzed mix dd_frac 0.49 with its 0.23 bremsstrahlung fraction and tritium plant) granted its two unrecorded claims: fuel recovery 0.9999, full recovery share |
| extrapolations | 41.0 | 37.3 | records + capacitor life 1e9, a 3 Hz ceiling, a purchasable divertor-class wall, fuel recovery 0.9999 (patent-implied fourth nine); optimum: nine of the same modules at 2.9 Hz, panel wall |
| speculation | 16.8 | 13.5 | extrapolations + 10 Hz, axial-channel capture, capacitors at 0.1 $/J and 1e10 shots, He-3 at 0.5 M$/kg, 80-year life; optimum: 300-750 MJ of fusion yield per shot from the same 50 MJ driver (gain 6-15), chosen by the scan, in 30 m x 1.5 m chambers |

With the coils priced along the expansion adiabat, the design search
trades length for radius: fat short chambers buy expansion volume with
less active structure. Reconciliation brackets the extrapolation
device within 31.4-48.8 $/MWh and the speculation device within
15.6-18.1 $/MWh at 1 GWe.

The records device tops the ladder, and the reason is exactly two
claims. The headline gap (173.0 against 118.6 $/MWh) cannot show that
by itself, because the two devices are different machines; the
controlled comparison is to take Helion's machine unchanged and revert
only its two unrecorded claims to their record-supported values. That
alone nearly doubles its cost, from 118.6 to 227.3 $/MWh (a
counterfactual that also sits 4% over the wall flash bound on the
vendor's 0.5 m chamber, one reason the records design moves to fat
chambers); design freedom under the record stack (its optimum is
already the D-rich mix with its tritium plant) buys back half of the
increase, to 173.0 $/MWh. The evidence premium is not diffuse conservatism but two
specific, measurable claims: the fourth nine of per-pulse fuel
recovery and the axial share of the expansion work. On evidence alone
the fuel cycle is uneconomic; the descent begins when the recovery
extrapolations are granted. The records and Helion devices are also dominated by
scheduled replacement: the entire shot-cycled recovery chain is
replaced on the capacitor-life schedule, about eight times over plant
life at the 1e8-shot record life.

![The evidence ladder](figures/fig1_ladder.svg)

*Figure 1: The four devices at 1 and 3 GWe, one machine per evidence
grade; the records device sits above Helion's requirements because
reverting the vendor's two unrecorded claims is worth about 109 $/MWh.*

One-at-a-time reversion from the extrapolation device ranks the levers:

| knob reverted | LCOE ($/MWh) | delta ($/MWh) |
|---|---|---|
| fuel_recovery -> 0.999 (JET-analog) | 84.9 | +43.9 |
| cap_shot_lifetime -> 1e8 | 82.0 | +41.0 |
| dhe3_dd_frac -> 0.49 (with its f_rad) | 56.1 | +15.2 |
| max_f_rep -> 1 Hz | 54.9 | +14.0 |
| eta_dec -> 0.85 | 44.6 | +3.6 |
| f_rad -> 0.23 (incoherent) | 38.6 | -2.4 |
| eta_pin -> 0.95 | 42.1 | +1.2 |

Two levers co-dominate at +41 to +44 $/MWh each: the per-pulse fuel
recovery (an extrapolated nine beyond the JET retention analogy) and
the capacitor cycle life (a published derating target); the rep rate
and the burn-mix package follow (f_pdv is absent from the table
because it is derived per point under constraint 6, not a knob); see
Figure 2. The conversion efficiencies,
once capped as a composite, are worth little at the margin (an
incoherent double-booking of eta_dec = 0.97 with f_pdv = 0.95 would
claim tens of $/MWh and is excluded by construction).

![Tornado from the extrapolation device](figures/fig2_tornado.svg)

*Figure 2: One-at-a-time reversion of each extrapolation entry to its
record value, from the 41.0 $/MWh extrapolation device. Red bars are
favorable reversions, the signature of anti-record entries.*

At the speculation device the capacitor-driver narrative is spent (the bank
is 5 M$ of a 666 M$ reactor account) and the floor is carried by
site and support infrastructure and by the fuel cycle (there is no
turbine island; the heat-rejection and electrical-plant accounts below
are not a steam cycle):

| item | M$ | $/MWh (approx) |
|---|---|---|
| buildings (CAS21) | 286 | 1.6 |
| CAS50, of which decommissioning provision 140 | 198 | 1.1 |
| fuel handling + tritium plant (C220500) | 190 | 1.1 |
| heat rejection + electrical plant (CAS24-26) | 170 | 0.9 |
| vacuum and exhaust (C220106), of which per-pulse pumping 78 | 107 | 0.6 |
| first wall of the 30 m chamber (C220101) | 106 | 0.6 |
| DEC power electronics (C220109) | 66 | 0.4 |
| adiabat-priced coils (C220103) | 14 | 0.1 |
| O&M (CAS70) | 54/yr | 6.4 |
| annualized capital, all-in | | about 7.5 |

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
0.55 mg per shot, 58 kg/yr. The extrapolation device carries 225 MW of plant
neutron power and breeds about 86 kg/yr. Store-for-decay fixes the
equilibrium inventory at production rate times the 17.8 yr mean life:
about 1.5 tonnes of tritium, which is 1.4e10 Ci, about 500 kW of
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
corroborates through pressure balance, and never its confinement time.
The closure on those numbers reproduces the patent's own two-column
structure: over a full confinement period the D burn is 2.5-3.8% and a
thermalized triton riding it would burn 28-38%, the case for
inter-pulse removal; per sub-millisecond pulse the burnup is 1.2-2.5e-4
and the in-pulse tritium burn 0.2-0.3%, so dhe3_f_T = 0 satisfies its
floor with two orders of margin. Fuel
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
vendor chamber reads 62.7 $/MWh and the speculation device 20.1 $/MWh,
plant neutron power rises about 5x with a dominant 14.1 MeV component,
and the decay store shrinks to 0.2-0.3 t. Which regime the
reactor-scale machine occupies is set by its compression density, which
the patent table may understate; Section 5.3 prices the full axis.

### 5.3 The burnup axis

Both species' per-pass burn fractions derive from the same n tau, so
the axis is swept coherently: burn_fraction_he3 scales with
burn_fraction at the fixed 70 keV reactivity ratio (3.3x). Figure 4
shows the result under both triton fates at exhaust recovery 0.99,
0.999, and 0.9999. At the patent-density basis the recovery nines
carry everything: 16.9 $/MWh at fr = 0.9999, 27.3 at 0.999, 147.0 at
0.99 (the fourth nine is worth 10 $/MWh, the third 120 $/MWh). Moving
right along the axis, i.e. toward higher compression density, the
recovery requirement relaxes: above per-pulse burnup of about 3e-3
the three- and four-nines curves converge near 15.8-16.3 $/MWh on
the prompt-loss branch, and the axis minimum (15.7 $/MWh, at burnup 1e-2 to
3e-1) sits about 1.5 $/MWh below the basis. The thermalized branch
turns up past burnup 0.01 as the tritium burn grows (13-90%), so the
triton-fate question reopens exactly where the recovery question
closes. Per-pulse exhaust pumping is priced across the axis and peaks
at the basis (79 M$ per module at the floor: 8300 pumped particles
per reaction).

![The burnup axis](figures/fig4_burnup.svg)

*Figure 4: LCOE at the speculation device across the per-pulse
burnup axis under the two triton fates and three exhaust-recovery
grades; the patent-density basis (dotted) is the hardest point for
fuel recovery.*

### 5.4 Neutron damage, the unshieldable throat, and the consumable core

The base model cannot see neutron damage for this concept (its core
lifetime knob is inert), so the scan reprices it: replacement of the
exposed package is levelized from the 14-MeV-equivalent neutron wall
load (10 dpa per MW yr/m^2 in Fe-based structure; the 2.45 MeV D-D flux
folded at 0.4) at tolerances of 20 dpa (the demonstrated RAFM database
edge) and 50 dpa (the DEMO-class design target). The event carries both
the wall and the close-coupled coils (106 + 14 M$ at the speculation
device), since nothing 0.10 m behind the wall outlives it. At the
patent basis the spectrum is pure 2.45 MeV D-D at a 14-MeV-equivalent
load of 0.20 MW/m^2, and the replacement adder is modest
(+0.3-1.2 $/MWh at 50-20 dpa). The damage story reopens only in the
high-burnup counterfactuals: if the reactor-point density pushes
per-pulse burnup toward the 0.1 regime with thermalized tritons, the
all-in gap between prompt-loss and thermalized reaches 8-17 $/MWh,
and on the extrapolation stack's divertor-class wall (2.5 M$/m^2, at
the vendor chamber) thermalized high-burnup replacement is prohibitive
(+53 to +161 $/MWh). Keeping the tritium out of the burn is therefore free
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
falls below about 8 years. At the patent basis (D-D spectrum,
0.20 MW/m^2 equivalent) the interval is 10-26 years at 20-50 dpa: a
capital asset, though near the line at the RAFM database edge. The
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
the machine imports about 38 kg/yr of He-3; crediting it flips the
plant to a net exporter. The question is not academic,
because the only observed He-3 transactions (2024-2026: spot near
$2,500/L per the Edelgas Group; Interlune's DOE Isotope Program and
Maybell Quantum agreements priced "at today's commercial market
price"; TAE's unpriced Black Moon lunar supply option) sit at
19-22 M$/kg on
gram-to-kilogram volumes, 10x above the baseline price used here and 40x
above the speculation entry, with every new entrant building toward the high
price. At the observed spot the extrapolation device reads 150 $/MWh at the
D-rich mix and 380 $/MWh lean under the model's accounting, against
28.9 $/MWh at the full self-supply limit; the distance between those two numbers is
the value of the crediting decision, coupled to Section 5.2 because the
decay return exists only if the tritium survives the pulse. A
by-product observation: at these prices a kilogram of He-3 burned at
the floor produces about $2M of electricity but sells for $19-22M, so
an early breeding plant maximizes value selling He-3 into the thin
cryogenics and quantum market until fleet supply floods it.

### 5.6 The breeder as the price of He-3

Every device buys the He-3 it does not breed (211, 111, 38, and 26 kg/yr
down the ladder) at the ledger's 2 M$/kg, 0.5 M$/kg at speculation, a
price Section 5.5 shows no market supports. The patent lets the
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
schedule, worth 0.03-0.09 M$/kg at the speculation breeder. The
fraction bites on the energy balance instead, since a third of the
fusion energy leaves as neutrons the inductive path cannot recover:
the gain is 0.36 on the vendor shot, 0.61 on the extrapolation
device's, 3.0 on the speculation device's.

**Unit cost.** Module cost plus throughput tritium plant plus net power
at the device's own LCOE, divided by the He-3 delivered, with the
device re-run at that price (a fixed point on the power price). The
power term is a cost on the vendor shot, where the breeder consumes
7 MW per module, and a credit at the higher grades. Financing the
17.8-year wait at 4.25% values the delayed half at 0.57 of prompt,
which raises the unit cost by 1.27x, 1.4x at the vendor grade where
the power price feeds back.

| device | He-3 bought (kg/yr) | ledger price (M$/kg) | He-3 line at ledger price ($/MWh) | breeder unit cost (M$/kg) | LCOE at breeder price ($/MWh) | ladder LCOE ($/MWh) |
|---|---|---|---|---|---|---|
| citable records | 211 | 2.0 | 67.8 | 2.08-2.30 | 175.8-183.1 | 173.0 |
| Helion's requirements | 111 | 2.0 | 35.6 | 7.7-8.5 | 219-233 | 118.6 |
| extrapolations | 38 | 2.0 | 12.1 | 0.76-1.13 | 33.5-35.7 | 41.0 |
| speculation | 26 | 0.5 | 2.6 | 0.19-0.69 | 15.2-17.8 | 16.8 |

| device | breeder gain | He-3 output per module (kg/yr) | ownership (M$/kg) | tritium plant (M$/kg) | power (MWh/kg) | power at device LCOE (M$/kg) | unit cost (M$/kg) |
|---|---|---|---|---|---|---|---|
| citable records | 0.85 | 10.9 | 2.04 | 0.06 | -83 | -0.01 | 2.08 |
| Helion's requirements | 0.36 | 4.5 | 4.86 | 0.06 | +12,600 | +2.76 | 7.66 |
| extrapolations | 0.61 | 22.5 | 0.80 | 0.06 | -2,960 | -0.10 | 0.76 |
| speculation | 3.0 | 137 | 0.32 | 0.05 | -12,000 | -0.18 | 0.19 |

Bands run from a co-sited to a standalone breeder at an equilibrium
store; the breakdown is the co-sited case, power positive when
consumed. The unit cost is ownership per kilogram plus a power term
whose sign follows the gain. The ledger's 2 M$/kg is what a
records-grade breeder charges; at the vendor grade it is unexplainable
by a factor of four, since a module that makes 4.5 kg/yr costs
4.9 M$/kg to own before its power bill; at the extrapolation grade a
breeder charges about 1 M$/kg; and the 0.5 M$/kg speculation entry
sits inside its band. Each 10 $/MWh on the breeder's power moves the
vendor-grade unit cost by 0.13 M$/kg and the speculation-grade one by
0.12 M$/kg the other way.

**Siting.** At the records and vendor grades a device needs 20-25
breeder modules and siting changes nothing. At the two cheaper grades a
central facility differs from a co-sited breeder in three ways:
granularity (the speculation-grade module makes 137 kg/yr against a
purchase of 26, so a co-sited whole module is five times oversized),
the model's own standalone fixed cost (28-37 M$/yr with the
tritium-plant core: 0.9-1.1 M$/kg over one device's purchase, under
0.1 M$/kg by ten), and power valuation (the speculation breeder exports
12,000 MWh per kilogram, so a facility selling above the park's own
LCOE drives its He-3 line toward zero).

| device | co-sited, marginal (M$/kg) | co-sited, whole modules (M$/kg) | central facility, 1 device | 5 devices | 20 devices |
|---|---|---|---|---|---|
| citable records | 2.08 | 2.17 (20 modules) | 2.33 | 2.13 | 2.09 |
| Helion's requirements | 6.41 | 6.54 (25 modules) | 6.79 | 6.51 | 6.43 |
| extrapolations | 0.74 | 0.98 (2 modules) | 1.86 | 0.99 | 0.80 |
| speculation | 0.17 | 1.03 (1 module) | 2.11 | 0.42 | 0.24 |

One device is one GWe of self-supply plant; power at the ladder LCOE,
so the vendor row reads 6.4 here and 7.7 at its fixed point. A
facility needs about five devices behind it to match a co-sited
breeder at the extrapolation grade and twenty to reach the marginal
price; at the speculation grade the answer is a fleet facility of five
devices or more. Surplus He-3 serves more plants, lets the burners run
leaner (free He-3 makes the lean mix cheaper than the D-rich one, 23.9
against 28.9 $/MWh at the extrapolation grade), or is banked, since
He-3 is stable and tritium can stay in the store. Banking is also the
answer to the decay lag: a fleet growing at rate g receives the delayed
half at lambda/(lambda + g), so breeders must lead the fleet by
1.3-1.6x at 5-20%/yr growth.

Closing the loop the other way, lean power modules fed by breeders
inside the park, gives the same reading: 32-43 $/MWh at the
extrapolation grade against 41.0, 14.5-20.5 at speculation against
16.8, 156-234 at the vendor grade against 118.6. The scheme relocates
the tritium inventory rather than shrinking it (0.5-3.3 t per lean GWe
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
+3.2/+5.4/+7.4 $/MWh at the extrapolation device across that x_s span
(the Q of order 2 machine circulates 1290 MW of driver power, and the
radial-only f_pdv widens the uncaptured channel),
+0.1 $/MWh at the speculation device, and order +10 $/MWh at the
low-Q Helion device. It is carried
as a reconciliation adder pending a model-level treatment.

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
above 90% for optimal cycles. There is no Carnot exemption in this:
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
composite. This single protocol prices the composite cap, the
thermalization share, and (through the wall budget) the rep-rate
ceiling; published excluded-flux radii pin chi per shot in the interim.

## 7. Plant architecture: modules, parks, and the small-plant penalty

Two controlled sweeps at the speculation stack (constant gain, constant wall
loading, driver and chamber scaled with module power) separate module
count from plant size. **Module count at fixed plant size is nearly
free, and mid-size modules carry a mild bonus**: a park of four
250 MWe modules reads 16.3 $/MWh against the single 1 GWe module's
16.8 $/MWh (the adiabat-priced coils reward smaller compressed
volumes), and even thirteen 80 MWe modules cost only a fraction of a
dollar more, because buildings, supplementary capital, and balance of
plant price plant totals; the only modularity tax is per-module fixed
items, biting below about 100 MWe. **Standalone
plant size is expensive**:

| plant | LCOE ($/MWh) | $/kW | dominant penalties |
|---|---|---|---|
| 1 GWe | 16.8 | 1446 | - |
| 250 MWe | 26.8 | 2198 | fixed site buildings, staffing^0.5 |
| 50 MWe | 62.5 | 6136 | O&M 27 $/MWh (staffing law), 141 M$ of buildings, tritium-plant fixed core |

![Module size, park vs standalone](figures/fig5_plant_size.svg)

*Figure 5: The same physics sold two ways at the full speculative
stack. Module size in a 1 GWe park is nearly free; standalone plant
size is expensive, and the 50 MWe standalone unit costs 3.7x the park
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

## 8. What would have to be true to reach $10/MWh

On top of the full speculation stack at 3 GWe (13.5 $/MWh), in decreasing order of
plausibility:

- **He-3 at effectively zero cost** (10.9 $/MWh): a mature breeding
  economy or
  an external supply two orders below the observed market. Even this
  does not break 10 $/MWh, because the tritium plant scales with the breeding
  throughput that funds the credit. Section 5.6 prices the breeding
  economy itself: a speculation-grade breeder delivers He-3 at
  0.2-0.7 M$/kg, and only a fleet facility that sells its power drives
  the line toward zero.
- **Gas-class site and decommissioning analogs** (about 1-1.5 $/MWh):
  defensible only for the He-3-lean machine; the D-rich machine's
  tonne-class tritium inventory argues the other way.
- **A real fleet-learning term** on equipment, anchored beyond the NOAK
  reference fleet: the only mechanism that rewards the mass-produced
  small-unit strategy at all.

None of these is in the evidence base at any grade.

## 9. Caveats that survive into the headline

- No extrapolation entry is a measured record: the two co-dominant levers
  (per-pulse fuel recovery, capacitor life) and the next two (rep
  rate, burn mix) are respectively an extrapolated analogy, a
  published target, a roadmap paraphrase, and a sweep endpoint.
- The speculation stack is jointly, not just individually, heroic: 0.1 $/J
  capacitors and 1e10-shot life together contradict the derating
  physics that connects capacitor cost to life; the composite sits at
  the theory optimum with zero margin; three-nines exhaust recovery
  becomes load-bearing at low burnup.
- The headline floor is conditional on the patent-basis compression
  field: per-pulse burnup falls as B^2, so a 10 T reactor point adds
  about 6 $/MWh and a 5 T point about 32 $/MWh (Section 5.3). The
  neutron-damage adders are more likely low than high
  (fission-spectrum dpa data, an order of magnitude more helium per
  dpa at 14 MeV, uniform-cylinder averaging over a localized burn).
- Model gaps priced in the bands but excluded from the headline:
  HVDC-class switch duty, tritium-plant scope, driver thermalization.
  The main conservatism cuts the other way (no thermal bottoming in the
  basis, worth -8.7 $/MWh at the extrapolation device).

## 10. Relation to the Borealis mirror study

Same framework, same evidence discipline, one ledger harmonized against
the other (knob-by-knob divergence table in `docs/ledger.md`; every
divergence carries a stated physics or technology reason). At the
speculation grade the mirror is 2.4 $/MWh cheaper at 3 GWe (Borealis
11.1 $/MWh, this work 13.5 $/MWh). At the extrapolation grade it is
materially cheaper (16.9 against 41.0 $/MWh), chiefly because it needs no
capacitor-life breakthrough, no tritium plant, and no rep-rate roadmap:
its levers already sit at record and extrapolation grade. On the down-select axis
"how much unpurchasable physics does the cheap number require", the
mirror requires less; on the axis "how large is the speculative
upside", the two are comparable.

## 11. Conclusions and measurement priorities

A Helion-class pulsed inductive plant, priced bottom-up with enforced
physics coherence, bottoms out at about 16.8 $/MWh at 1 GWe and
13.5 $/MWh at 3 GWe on full speculation; the public $10/MWh target is
not reached by any internally consistent stack this work can
construct. The cheap numbers rest on a small set of unmeasured
properties, ranked here by the $/MWh they gate:

1. **Capacitor cost-at-life** (tens of $/MWh): a sourced curve
   replacing the single derating target, resolving the joint optimism
   of 0.1 $/J with 1e10-shot life.
2. **Per-pulse burnup, extraction, and fuel recovery** (5-17 $/MWh):
   the patent fixes the design intent, low per-pulse burnup with
   inter-pulse tritium removal, but a patent is design intent, not a
   measurement; the reactor-point compression density and field, the
   demonstrated per-pulse separation rate, and the per-pass fuel
   recovery (four nines required at the published operating point) fix
   the neutron spectrum, the wall-replacement schedule, and the
   fuel-cycle cost between them.
3. **The recovery chain** (order 5 $/MWh at the extrapolation grade): the Polaris
   vacuum / no-burn / burn shot triplet separates the circuit
   efficiency, the thermalization share chi(1 - f_pdv), and the
   fusion-inclusive composite in one campaign.
4. **A duty-cycle basis for multi-Hz operation** and **a costed
   tritium-plant scope** for the D-rich cycle (single $/MWh each, but
   licensing-defining).

The constructive reading for the concept: its floor is real and low by
any thermal-plant standard, its architecture (factory modules, park
deployment, swappable cores) is well matched to the failure modes the
physics imposes, and the measurements that would move its ladder
from speculation to evidence are all available on hardware the
developer is already building.

## Reproducibility

All quantities in this work are produced by the scripts named in the
text from the configuration files in `config/`, against the `1costingfe`
cost model at commit `44434d9` (which guarantees the cylinder wall
audit, rep-rate sizing, shot-cycled replacement scope,
physics-consistent recovery-store markup, and per-pulse fuel-cycle
semantics this work relies on). Thirty regression tests in `tests/`
pin all four devices at both plant sizes, the stack evaluations at the
vendor configuration, the tritium-burn closure, the chi(x_s)
equilibrium anchors, and the breeder unit cost, and fail loudly if the
model moves under this work.

## References

- Apostoleris, H., et al. (2021). "The view from the sun: revisiting
  record-low solar PPA prices." Progress in Photovoltaics 29.
- Bosch, H.-S., and Hale, G. M. (1992). "Improved formulas for fusion
  cross-sections and thermal reactivities." Nuclear Fusion 32, 611.
- Brezinsek, S., et al. (2013). "Fuel retention studies with the ITER-
  Like Wall in JET." Nuclear Fusion 53, 083023.
- Helion Energy. Technology and FAQ pages (helionenergy.com/technology,
  /faq); Microsoft power purchase agreement announcement (2023); Nucor
  500 MW facility announcement (2024).
- Helion Energy (Slough, J., et al.). "Advanced fuel cycle and fusion
  reactors utilizing the same," published as US 2017/0011811, granted
  as US 11,469,003 B2 (2022): the breed-extract-store-decay fuel cycle
  and its operating table. Used as design intent, not as a record; see
  Section 5.2.
- Kirtley, D. (2024). "Fundamental theory of the direct magnetic
  energy recovery in a thermonuclear field reversed configuration
  system." APS DPP 2024, abstract GO05.8; slide captures in
  `docs/sources/` (the composite-recovery figure behind constraint 2
  and the Otto/Diesel burn-cycle expressions behind Section 6).
- Kirtley, D., and Milroy, R. (2023). "Fundamental scaling of
  adiabatic compression of field reversed configuration thermonuclear
  fusion plasmas." Journal of Fusion Energy 42, 30.
- Langtry, A., et al. (2025). "Affordable, manageable, practical
  Z-pinch driver (AMPS)." arXiv:2504.10680 (capacitor derating and
  shot-life target; MagLIF burn fraction).
- Rubin, T. (2026). 1costingfe: a bottom-up fusion power plant cost
  model. Repository at commit `44434d9`.
- Spencer, R. L., Tuszewski, M., and Linford, R. K. (1983).
  "Adiabatic compression of elongated field-reversed configurations."
  Physics of Fluids 26, 1564 (the FRC adiabatic compression scalings
  behind the radial-axial work partition).
- Tuszewski, M. (1988). "Field reversed configurations." Nuclear
  Fusion 28, 2033 (FRC equilibrium, average-beta theorem, adiabatic
  scalings).
- US DOE/NETL. Quality Guidelines for Energy System Studies: EPCM
  indirect-cost basis.
- US DOE Geothermal Technologies Office. Geothermal FAQ (fleet
  availability).
- Edelgas Group (2024). Helium-3 market pricing, as reported in
  SpaceNews and Newsweek coverage of the Interlune agreements (2025);
  Interlune-DOE Isotope Program and Interlune-Maybell Quantum
  agreements (2025); TAE Technologies and Black Moon Energy Corporation
  helium-3 supply option (2026).
- Idaho National Laboratory. Advanced-reactor staffing studies (the
  P^0.5 O&M scaling basis).
