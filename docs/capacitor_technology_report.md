# Capacitor and pulsed-power technology report

The pulsed inductive FRC's economics rest on one component class. This report
establishes what that hardware is, what it costs, how long it lasts, and
which of the cost model's treatments of it are defensible.

It plays the role for this study that `wall_material_report.md` played for
the Borealis mirror study: the enabling-technology audit that the ledger's
records are argued against.

## Why this account decides the study

At the design baseline, two accounts are 88% of per-module equipment cost:
`C220109` (direct energy converter) at $49.2M and `C220107` (capacitor bank)
at $26.3M, against $85.9M total. Both are priced from a single constant,
`c_cap_allin_per_joule`. A third constant, `cap_shot_lifetime`, sets the
replacement cadence and swings LCOE from $95.6 to $324.4/MWh across its own
documented range. Nothing else in the machine has that leverage.

## The architecture, from Helion's patents

The cost model treats energy recovery as one capacitor bank sized for the
full returned energy. Helion's patents describe something different, and the
difference is the report's central finding.

### Two-stage storage, and the reason for it

`US 2024/0275198 A1`, "Energy Recovery in Electrical Systems" (Helion Energy,
Kirtley et al.) describes a primary energy-storage component C1 that drives
the coils, and a secondary component C2 acting as an intermediate recovery
point. Energy leaves C1 into the load, accumulates in C2 at reversed
polarity, and transfers back to C1 for the next cycle. The patent's stated
rationale is explicitly economic: the two-capacitor approach gives

> "a net reduction in cost and size compared to the single capacitor that is
> sized to handle full voltage reversal."

That is the design the cost model prices. The model's `delta_cap` sizes one
bank for the whole returned energy at the driver bank's unit cost, which is
the single-capacitor-handling-full-reversal case that the patent identifies
as the more expensive option and designs around.

### Where the surplus actually goes

`US 2025/0292916 A1`, "Apparatus and Methods for Harvesting Energy from an
Axially Expanding Plasma Contained by a Magnetic Field" (Kirtley, C. Pihl,
J. Pihl) gives the export path. C2 temporarily stores energy received from
the magnetic coils; a power converter (DC-to-AC) draws from C2 and delivers
to a load that "can comprise a power grid," through a power conditioner
producing conventional two- or three-phase AC. Transfer from the coils is
resonant, through a choke inductor L2, gated by an opening switch (a MOSFET)
under closed-loop control. The full cycle spans 1 microsecond to 100
milliseconds.

So the export chain is: coils, then C2, then converter, then grid. C2 is a
buffer that accepts a fast charge and discharges to a converter, not a
pulse-discharge bank that fires into a low-inductance load.

This settles the architectural question the study started from. Surplus
energy cannot go straight to the inverter, because the plasma expansion is a
microsecond-scale event and grid-tie conversion is not. But the intermediate
store it must pass through is buffer-duty hardware, in a different and
cheaper component class than the driver bank.

### Switch protection

The recovery path is designed to keep current out of the active switches:
70% and in some configurations up to 98% of total recovery energy is diverted
from the switching elements to forward diodes. Switching elements are named
as SCRs, IGBTs, and IGCTs, rated above 10^3 volts and, in the aggregate
circuit description, above 10^6 amps. Recovery efficiency is claimed at over
90%, with quoted bands of 85-95% and 90-97%.

The model's `eta_dec` of 0.85 therefore sits at or just below the bottom of
the range Helion claims, which is the conservative direction. It remains an
assumption rather than a record: inductive recovery from a translating FRC
has no public-program demonstration, and a patent's claimed range is not a
measurement.

## Cost basis

### What the model uses

`c_cap_allin_per_joule` is 0.5 $/J, documented as "NOAK all-in (caps +
switches + charging + buswork)" with the annotation "Sensitivity range:
0.5-4.0". The operating value sits at the optimistic end of its own stated
range, so the model has no headroom to go cheaper on the single constant that
decides the concept.

### What the market shows

Merchant pulse-rated metallized film runs well above the model's figure.
Distributor pricing on a 180 uF / 450 V part works out near $3/J, and a
long-life (10^9 shot) pulse capacitor above 100 J is quoted near $1/J. Both
figures are weak sources (a distributor calculation and a Usenet posting
respectively) and should be treated as order-of-magnitude only; neither is
adequate to set a record and both are flagged here so they are not cited as
if they were.

The industry-level statement is firmer and points the same way. For
commercial Hz-rate operation, energy storage costs must decrease 5-10 times
and component lifetimes must increase roughly 1,000 times, the latter
attributed to a 2025 IEEE analysis. Those are statements of what has *not*
been achieved.

### Buffer-duty hardware: the price gap is smaller than the duty suggests

The candidate technologies for the C2 role, by cost of stored energy:

| technology | cost | duty limits |
|---|---|---|
| supercapacitor | $10,000/kWh = $0.0028/J, $40/kW | 10^6 cycles; response too slow for the fast end of the transfer window |
| aluminum electrolytic | $0.05-0.10/J | polarized: cannot accept voltage reversal |
| polypropylene film, DC-link duty (450 Vdc) | $0.20-0.50/J | none disqualifying |
| pulse-rated film (model's driver basis) | 0.5 $/J | reference |

The cheap options are disqualified by duty, not by price. Both Helion patents
describe C2 accumulating energy **at reversed polarity** on a transfer that
begins in microseconds. Aluminum electrolytics are polarized and cannot take
reversal at all. Supercapacitors do not respond fast enough at the leading
edge. What remains is film, and DC-link film at $0.20-0.50/J brackets the
model's 0.5 $/J rather than undercutting it by orders of magnitude.

So the saving available from the staged architecture is the patent's own
unquantified "net reduction in cost and size" relative to a single bank rated
for full voltage reversal: a factor plausibly below 2 on the same technology,
not a substitution into a cheaper component class. `delta_cap` is closer to
correct than the duty-class argument alone would suggest.

### Vertical integration

Helion manufactures its own capacitors and ultrahigh-pressure ceramics rather
than buying merchant parts, and is installing assembly-line equipment at its
Omega facility to produce roughly 2,500 capacitor units for the Orion plant,
with production starting late 2026. Merchant pricing therefore may not be the
right basis for this concept at all.

For scale context, General Atomics Electromagnetic Systems is the principal
qualified US manufacturer of high-voltage pulsed-power capacitors, and its
largest production contract was 2,500 units for the Z Refurbishment. One
Helion plant is the size of the largest order the incumbent qualified base
has ever filled. That is an argument for in-house production being necessary,
and simultaneously an argument that the supply chain has never demonstrated
this cost at this volume.

## Lifetime is the binding constraint

Cost per joule is not the number that decides this concept. Shot life is.

A 1 GWe plant at 1 Hz, 30 years, and 0.85 availability fires 8.05 x 10^8
shots. Laboratory pulse capacitors are rated near 17,000 shots, adequate for
facilities firing 200 shots per year. The gap is five orders of magnitude.

The two requirements fight each other, and the tradeoff is quantifiable.
Metallized polypropylene film capacitor life scales with charging field as

```
L / L_0 = (E / E_0) ^ -7.32
```

while energy density scales as E^2, so for a fixed stored energy the
capacitor volume, and hence cost, scales as 1/E^2. Eliminating E between the
two gives cost as a function of demanded life:

```
cost  ∝  L ^ (2 / 7.32)  =  L ^ 0.273
```

Buying the 1,000-fold life increase the industry says is required therefore
costs about 6.6 times more capacitor, before any of the 5-10 times cost
reduction that is also required. The combined ask is roughly 30-65 times
improvement in cost-at-required-life. That is the target Peak Nano and E&P
Technologies are pursuing with nanolayered film, quoted at up to 4 times the
energy density of BOPP and operation to 125 C against BOPP's practical 85 C
ceiling. BOPP itself stores about 2.4 J/cc and derates above its temperature
ceiling, which is a live constraint under repetitive pulsing where self-
heating accumulates between shots.

Ceramic capacitors tolerate higher voltage reversal (above 70%) and reach
shot lives above 10^6 at comparable energy density, which is consistent with
Helion producing ultrahigh-pressure ceramics in house.

### What the model does with this

`cap_shot_lifetime` defaults to 10^8 shots with a documented range of 10^7 to
10^9. The plant needs 8.05 x 10^8, so at the default the bank is replaced
eight times over plant life, and the replacement charge lands in CAS70.
Sensitivity across the documented range, at the design baseline:

| `cap_shot_lifetime` | LCOE ($/MWh) | CAS70 (M$/yr) |
|---|---|---|
| 10^9 | 95.6 | 53.0 |
| 10^8 (default) | 115.1 | 198.5 |
| 10^7 | 324.4 | 1756.9 |

At the default, capacitor replacement alone is a larger annual charge than
most of the plant's capital service. This is the study's dominant single
sensitivity and the ledger must treat it as such.

## Required specifications to reach 1 cent/kWh

The question this report was commissioned to answer: what must the capacitors
achieve, in physics and in cost, for the concept to reach $10/MWh?

The answer is that no capacitor specification is sufficient. LCOE against
`c_cap_allin_per_joule` and `cap_shot_lifetime`, at 1 GWe:

**At the sourced shot point (Q = 2.03), design-baseline economics:**

| $/J \ shots | 10^8 | 10^9 | 10^10 | 10^11 | 10^12 |
|---|---|---|---|---|---|
| 0.50 | 115.1 | 95.6 | 95.6 | 95.6 | 95.6 |
| 0.10 | 75.4 | 71.5 | 71.5 | 71.5 | 71.5 |
| 0.01 | 66.5 | 66.1 | 66.1 | 66.1 | 66.1 |

**At the sourced shot point, record economics and He-3 self-supply:**

| $/J \ shots | 10^8 | 10^9 | 10^10 | 10^11 | 10^12 |
|---|---|---|---|---|---|
| 0.50 | 62.0 | 40.1 | 39.0 | 39.0 | 39.0 |
| 0.10 | 34.6 | 30.3 | 30.0 | 30.0 | 30.0 |
| 0.01 | 28.5 | 28.1 | 28.0 | 28.0 | 28.0 |

**At the model's gain optimum (Q = 40), record economics and He-3
self-supply:**

| $/J \ shots | 10^8 | 10^9 | 10^10 | 10^11 | 10^12 |
|---|---|---|---|---|---|
| 0.50 | 28.1 | 27.3 | 27.2 | 27.2 | 27.2 |
| 0.10 | 23.0 | 22.8 | 22.8 | 22.8 | 22.8 |
| 0.01 | 21.8 | 21.9 | 21.9 | 21.9 | 21.9 |

**Scope warning on the tables below.** They vary only the two capacitor
constants, holding `max_f_rep`, `eta_dec`, `f_pdv`, and `eta_pin` at their
baseline values. Those four are between them worth more than either capacitor
knob (see `docs/writeup.md`, tornado), so these tables answer "what do
capacitors alone buy" and must not be read as a floor for the concept. With
the full ledger applied the machine does reach the target: 17.0 $/MWh on
records plus labelled extrapolations, and 10.0-10.7 $/MWh once tier-3
speculation is included.

Two structural features of these tables matter more than any individual cell.

**Shot life saturates at the plant's own shot count, which is set by rep
rate.** At 1 Hz a 30-year 85%-availability plant fires 8.05e8 shots, so a
10^9-shot bank outlives it and further life buys nothing. That figure is not
transferable to a higher rep rate, and the study's own best case moves the rep
rate: at the 7.45 Hz the tier-2 stack solves, the plant fires 6.9e9 shots, a
10^9 bank is replaced 6.9 times, and the model's short-life warning fires on
this study's own best case. Saturation there needs about 10^10.

So the requirement is bounded but must be quoted together with the rep rate it
assumes: **10^9 shots at 1 Hz, rising to about 10^10 at 10 Hz.** Against a
laboratory rating near 1.7e4 shots the first is the 1000-fold improvement the
industry has identified as necessary and has not achieved; the second is
10,000-fold. The rep-rate lever and the capacitor-life record therefore pull
against each other, and any ladder that adopts both owes an explanation.

**Cost per joule saturates.** Driving the capacitor to $0.01/J with immortal
life still leaves $21.8/MWh when the rest of the machine is held at the
partial best case these tables use. Capacitors alone do not reach the target,
so no capacitor specification should be quoted as the thing that gets there.

What does reach it is the rest of the ledger. The four knobs excluded from
these tables (`max_f_rep` 1 to 10 Hz on Helion's roadmap, `eta_dec` 0.85 to
0.97 at the top of the patent's claimed band, `f_pdv`, `eta_pin`) are worth
about 70 $/MWh between them one-at-a-time, and they collapse the module count
from 24 to 2-3, which is where most of the capital reduction comes from. The
defensible statement is therefore narrower than an earlier draft of this
section claimed:

> The capacitor bank is a first-order cost driver and its shot-life
> requirement is a hard gate, but it is not what stands between this concept
> and 1 cent/kWh. Rep rate, recovery efficiency, and the module count that
> follows from them are.

### What the capacitor requirement actually is

Stated as a specification rather than a direction of travel: **10^9 shots at
operating field, at or below 0.5 \$/J all-in.** Life beyond 10^9 buys nothing
because the bank outlives the plant. Against a laboratory rating near
1.7 x 10^4 shots that is the 1000-fold improvement the industry has
identified as necessary and not achieved, and the derating relationship above
makes it about a 6.6x cost penalty before the 5-10x cost reduction that is
also required.

### The remaining capital, at the partial best case

Held at that partial best case the $1,232/kW residual decomposes as:
buildings (CAS21) $303/kW, CAS50 $192/kW,
`C220200` main heat transfer $186/kW, grid-tie inverter (the surviving part
of `C220109`) $150/kW, CAS24 electrical $90/kW, with the remainder spread
across small accounts.

`C220200` should not be there at all. `cas22.py:703` computes the primary
coolant loop as `166.0 * (p_net_total / ref_net_power_mwe)`, scaled on net
electric power with no gating on whether a thermal conversion path exists.
An `INDUCTIVE_DEC` machine has `eta_th` = 0, no turbine, and `p_pump` = 0,
yet still buys "primary loops + intermediate HX + secondary to steam
generators" sized for a 1 GWe steam plant. The account is over-scoped rather
than wholly spurious, since the machine does need heat rejection for the
radiated fraction and resistive coil losses, but that is a rejection loop and
not a steam-cycle coolant chain. Removing it entirely brings the floor to
about $11/MWh, which is still above target.

`C220200` was subsequently fixed in costingfe: the primary coolant account
now scales on thermal power rather than net electric, so a machine with no
conversion path is no longer charged a steam plant's coolant chain.

The buildings and BOP terms in this residual are where
`down_select/03_costingfe_alignment.md` documents a systematic bias against
small modular units. That bias matters less than it first appeared: once
`max_f_rep` and `eta_dec` are applied the module count falls to 2-3, which is
the regime the sub-linear BOP scaling was penalising in the first place.

## Findings for the cost model

**One root cause, two opposite-signed errors.** Both trace to pricing the
entire recovery path as driver-class pulse hardware on a single constant.

1. `delta_cap` in `C220109` prices the fusion surplus as a single bank rated
   for full voltage reversal, the design Helion's patent names as the more
   expensive option and engineers around with staged C1/C2 storage. The
   available correction is the patent's unquantified "net reduction in cost
   and size", plausibly under a factor of 2, because the reversed-polarity
   microsecond duty disqualifies the cheaper electrolytic and supercapacitor
   classes and leaves film either way. The model is too pessimistic here, but
   by a modest factor, not the order of magnitude the duty-class argument
   first suggested.

2. `c_cap_allin_per_joule` at 0.5 $/J and `cap_shot_lifetime` at 10^8 are
   both at or beyond the optimistic end of their documented ranges, against
   an industry that says the required cost-at-life has not been achieved and
   a plant that needs 8 times the default shot life. The model is too
   optimistic here.

Which dominates is not yet determined and should not be assumed. Resolving
item 1 without item 2 would produce a number that is optimistic twice over.

**Secondary finding.** `eta_dec` of 0.85 is conservative against Helion's
claimed 85-97% recovery, but the claim is patent language, not measurement,
and the mechanism has no public-program demonstration. It stays an assumption
in the machine basis rather than moving to the records tier.

**Third finding, outside the capacitor scope but found here.** `C220200`
prices a steam-plant coolant chain on a machine with no thermal cycle
(`cas22.py:703`, ungated on the conversion path). $186/kW of a $1,232/kW
floor. This belongs in the model as a defect report of its own.

## Open items

- A sourced cost-at-life figure for capacitors qualified above 10^8 shots.
  The `L^0.273` scaling derived here is an inference from two published
  scaling laws, not a quoted price curve, and needs replacing with a vendor
  or program figure.
- Whether in-house production changes the applicable unit cost, and whether
  any Helion disclosure supports a figure. Nothing found so far quantifies
  it.
- Ceramic versus film for the driver bank, given the voltage-reversal duty
  the recovery cycle imposes and Helion's in-house ceramic work.

## Sources

- Helion Energy, `US 2024/0275198 A1`, "Energy Recovery in Electrical
  Systems" (Kirtley et al.).
  https://patents.google.com/patent/US20240275198A1/en
- Helion Energy, `US 2025/0292916 A1`, "Apparatus and Methods for Harvesting
  Energy from an Axially Expanding Plasma Contained by a Magnetic Field"
  (Kirtley, C. Pihl, J. Pihl).
  https://patents.google.com/patent/US20250292916A1/en
- Helion Energy, "Helion's fusion system is (basically) an RLC circuit".
  https://helionenergy.com/articles/helions-fusion-system-is-basically-an-rlc-circuit
- Helion Energy, "Polaris". https://www.helionenergy.com/polaris
- The Fusion Report, "IMGs, Capacitors, and the Supply Chain Gap Facing
  Pulsed Power Fusion" (cost must fall 5-10x; life must rise about 1000x per
  a 2025 IEEE analysis; 17,000-shot lab rating; BOPP 2.4 J/cc and 85 C;
  vendor base).
  https://thefusionreport.substack.com/p/imgs-capacitors-and-the-supply-chain
- Thunder Said Energy, "Supercapacitors: the economics" ($10,000/kWh,
  $40/kW, 10^6 cycles).
  https://thundersaidenergy.com/downloads/supercapacitor-the-economics/
- "Degradation of polypropylene films in metallized film capacitors under
  repetitive intense pulsed electric fields", J. Phys. D.
  https://iopscience.iop.org/article/10.1088/1361-6463/ae8ddc
- "Lifetime investigation and prediction of metallized polypropylene film
  capacitors", Microelectronics Reliability (life exponent m = 7.32).
  https://www.sciencedirect.com/science/article/abs/pii/S0026271413001571
- passive-components.eu, "Peak Nano to Develop Fusion Grade High Energy Film
  Capacitors" (4x BOPP energy density, 125 C, million-shot target).
  https://passive-components.eu/peak-nano-to-develop-fusion-grade-high-energy-film-capacitors/
- GeekWire, "Helion's next big bet is manufacturing fusion power at scale"
  (Omega facility, about 2,500 capacitor units for Orion, production late
  2026).
  https://www.geekwire.com/2025/helions-next-big-bet-is-fusion-power-manufacturing-at-scale-but-tech-uncertainty-remains/
- General Atomics Electromagnetic Systems, capacitor products.
  https://www.ga.com/capacitors/
- eePower, "DC Link Capacitor Technology Comparison: Aluminum Electrolytic
  vs Film Capacitors" (electrolytic about 3x lower cost per unit stored
  energy than polypropylene film; film holds 60-70% of high-voltage DC-link
  share on ripple handling and lifetime).
  https://eepower.com/technical-articles/dc-link-capacitor-technology-comparison-aluminum-electrolytic-vs-film-capacitors/
- Electronic Design, "Selecting Film or Electrolytic Capacitors for
  Power-Conversion Circuits" (electrolytic $0.05-0.10/J, polypropylene film
  $0.20-0.50/J at 450 Vdc).
  https://www.electronicdesign.com/technologies/power/article/21806817/selecting-film-or-electrolytic-capacitors-for-power-conversion-circuits

Weak sources, recorded so they are not mistaken for records: a distributor
calculation giving about $3/J for a 180 uF / 450 V film part, and a Usenet
posting giving about $1/J for long-life (10^9 shot) pulse capacitors above
100 J.
