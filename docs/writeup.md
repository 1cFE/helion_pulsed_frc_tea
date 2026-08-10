# How low can a Helion-class pulsed FRC go?

The down-select question this study answers: pushed to the physically
coherent limit of optimism, what is the minimum LCOE of a Helion-like
pulsed inductive-DEC D-He3 plant, and does it reach Helion's own public
$10/MWh (1 cent/kWh) target?

**Answer: the coherent floor is about 16 $/MWh at 1 GWe and 12 $/MWh at
3 GWe, on full tier-3 speculation. The $10 target is not reached by any
internally consistent stack the study can construct; even He-3 at zero
price on top of full speculation lands at 10.4 at 3 GWe, because the
tritium plant that funds the He-3 self-supply scales with the throughput
that breeds it. The evidence-backed numbers are far higher: 104.5 on
records alone, 33.9 on labelled extrapolations.**

All numbers at costingfe `ac2d1a8`, reproduced by `scripts/tiers.py`,
`scripts/coherent_min.py`, and `scripts/reconciliation.py`; regression
tests pin the ladder in `tests/test_study.py`.

## The ladder

| rung | 1 GWe | 3 GWe | what it contains |
|---|---|---|---|
| design baseline | 133.3 | 129.8 | Helion's implied point: 50 MJ driver, 101.4 MJ yield, 1 Hz, D-rich mix at its bremsstrahlung floor |
| tier 1: records | 104.5 | 100.9 | finance (4.25%), 2.5 yr construction, 8% indirects, availability 0.95 |
| tier 2: extrapolations | 38.6 | 35.3 | cap life 1e9, recovery composite 0.765, 3 Hz on a bought divertor-class wall, D-rich mix with tritium plant |
| tier 3: speculation | 16.6 | 13.2 | 10 Hz, composite 0.90, cap $/J 0.1, cap life 1e10, He-3 at 0.5 M$/kg, 80 yr |

Design optimization under the same evidence (chamber size, wall class, and
yield chosen rather than inherited) improves the last two rungs to **33.9**
(tier 2, 1 GWe) and **15.8 / 12.4** (tier 3, 1 / 3 GWe). Reconciliation
bands (model gaps vs conservatisms): tier 2 in 27.7-36.2, tier 3 in
14.8-17.1 at 1 GWe. The baseline and tier-1 rungs are dominated by
scheduled replacement: the whole shot-cycled recovery chain (driver bank,
recovery store, switch stack) is replaced on the capacitor-life schedule,
and at the 1e8-shot record life that chain is replaced about 8 times over
plant life.

## How to push toward the minimum: what actually works

Ranked by what the tornado and the coherent scan say, the levers that move
a Helion-class machine down the ladder are:

1. **Capacitor cycle life** (+39.2 $/MWh if lost). Not the glamorous knob,
   but the single largest by a factor of three: at the baseline 1e8-shot
   life the bank, the recovery store, and the switch stack (the whole
   shot-cycled chain) are replaced about 8 times over plant life and
   replacement dominates the capital service. Everything else in the study
   presumes this solved to 1e9; the only support is a published derating
   target.
2. **Burn mix** (+12.9). D-rich operation (dd_frac 0.85) cuts the
   purchased He-3 line from about 31 to 9 $/MWh. It is only honest as a
   package: the D-rich plasma radiates twice as much (f_rad 0.28, not
   0.05), breeds 41 kg of tritium a year, and buys a tritium plant. The
   package is still worth +12.9; the incoherent version of it (fuel credit
   without consequences) would claim about 16 and is excluded.
3. **Rep rate** (+11.4). Going from 1 to 3 Hz collapses the module count
   from 24 to 8. But rep rate is bought with wall area: the machine that
   supports it is a longer chamber with a panel wall run near its 2 MW/m^2
   qualification, or a divertor-class wall in a short one. Nothing
   MJ-class has ever run at 1 Hz continuously; this is a roadmap band, not
   a spec.
4. **Gain, within survivability** (tier 3 only). Yield is the strongest
   structural lever in principle (it raises fusion power at constant
   recirculating drive), and the coherent optimum sits at 200-750 MJ
   shots, about Q = 4-15, in a 45 m chamber - not at Q = 40 in a 10 m one,
   which flash-melts the wall it is costed against. Above about 750 MJ
   the wall constraint forces so much chamber that the gain stops paying.
5. **Recovery efficiency** (+2-3 each). eta_dec and f_pdv are worth
   surprisingly little at the margin once capped as a composite - the
   double-booked version of them (0.97 x 0.95) was worth 38 $/MWh in the
   earlier draft, and that was an artifact of counting one projected
   number twice.
6. **Scale** (15.8 to 12.4). The 3 GWe plant amortizes buildings, fixed
   site costs, and staffing across modules. The tritium plant does *not*
   amortize: it scales with the throughput that breeds the He-3.

## What carries the floor

At the tier-3 minimum (15.8, single 300 MJ module at 5.9 Hz), the
capacitor-driver narrative is spent: the driver bank is 15 M$ of a 641 M$
reactor account. The floor is carried by:

| item | M$ | $/MWh (approx) |
|---|---|---|
| buildings (CAS21) | 286 | 1.6 |
| CAS50 (capitalized supplementary), of which decommissioning provision 140 | 196 | 1.1 |
| fuel handling + tritium plant (C220500) | 203 | 1.2 |
| heat rejection + turbine-plant BOP (CAS24-26) | 170 | 0.9 |
| first wall of the 45 m chamber (C220101) | 109 | 0.6 |
| DEC power electronics (C220109) | 60 | 0.4 |
| O&M (CAS70) | 54/yr | 6.5 |
| annualized capital, all-in | | about 7.5 |

## The tritium system, priced and audited

The machine has no lithium and no breeding blanket; its tritium plant is
an exhaust-processing plant. The D-rich burn breeds tritium through
D+D->T+p, none of it is burned in-plasma (dhe3_f_T = 0), and the exhaust
is pumped, isotope-separated, and stored on getter beds to decay into the
He-3 the plant burns (12.3 yr half-life). Two audits sit on top of that
basis (`scripts/tritium_burn.py`):

- **The dhe3_f_T = 0 idealization holds only for short, thin pulses, and
  the model's own burnup contradicts it.** A triton born mid-pulse burns
  with probability (1/2) n_D <sigma v>_DT tau, and D-T reactivity is
  14-43x D-D at 20-70 keV, so each percent of per-shot D burnup burns
  14-43% of the bred tritium in-plasma. The declared burn_fraction 0.15
  therefore implies 78-93% in-pulse tritium burn if tritons thermalize
  and stay confined; store-and-decay requires either burnup below about
  7e-4 (which multiplies the fuel recycle loss 15x at 99% recovery and
  inflates the pumping throughput two orders) or prompt MeV-triton loss
  from the small-s plasmoid. Priced at the thermalized limit
  (dhe3_f_T = 0.78) the tier-2 rung is 49.1 and the tier-3 minimum 19.0,
  with plant neutron power up 5x at 14.1 MeV, before any repricing of
  the wall and shield for that spectrum. The plant-scale rates behind
  this: at the tier-3 minimum the single module runs 7.1e20 D-D and
  4.6e20 D-He3 reactions per second (three quarters of the D-He3 burns
  fed by recycled bred He-3), breeding 0.30 mg of tritium per shot.
  Sweeping the axis (`scripts/burnup_scan.py`): the 15.8 floor exists
  only at the high-burnup prompt-triton-loss corner; thermalized tritons
  put the coherent optimum at partial burnup (0.01-0.03, 16.6-18.4
  $/MWh), and the store-purist corner costs 19.8 at best. The
  fast-triton confinement question is worth +1 to +4 $/MWh at the floor.

- **The store is a tonne-class tritium inventory.** Store-for-decay fixes
  the equilibrium inventory at production rate x 17.8 yr mean life: about
  1.3 t at the tier-2 rung (1.2e10 Ci, about 410 kW of decay heat,
  roughly 300x ITER's site limit and 45x the world's civilian tritium
  stock). The inventory is intrinsic to the He-3 self-supply strategy at
  this scale, whether it sits on the reactor site or at a central fuel
  facility. It is why the ledger denies the "near-zero licensing" claim
  alongside the fuel credit, holds O&M at baseline, and treats the 200 M$
  tritium-plant allowance as more likely low than high.

## The small-plant penalty, untangled

The program's alignment note (`down_select/03_costingfe_alignment.md`)
flags a bias against "small modular units". Two controlled sweeps at the
tier-3 stack (`scripts/module_scan.py`: family of machines at constant
gain Q_sci = 6 and constant wall loading, driver and chamber scaled with
module power) separate what is actually being charged:

**Module count at fixed plant size is nearly free.** At 1 GWe, going from
one 1-GWe module to thirteen 80-MWe modules costs +2.0 $/MWh (15.8 to
17.9). Buildings, CAS50, and CAS24-26 are exactly flat: they price
plant-total power and do not care how many chambers deliver it. The only
modularity tax is CAS22's per-module fixed items (installation labor,
per-chamber pumping/vessel minima), and it only bites below about 100 MWe
per module.

**Standalone plant size is very expensive.** The same physics sold as a
one-module standalone plant:

| plant | LCOE | $/kW | dominant penalties |
|---|---|---|---|
| 1 GWe | 15.8 | 1373 | - |
| 250 MWe | 26.1 | 2182 | fixed site buildings, staffing^0.5 |
| 50 MWe | 62.8 | 6355 | O&M 27 $/MWh (staffing law), 141 M$ of buildings (2800 $/kW), tritium-plant fixed core |

So the model's "bias" decomposes into three distinct mechanisms:

1. **Fixed site dollars** (about 138 M$ of CAS21 regardless of size: site
   improvements 75, assembly hall 21, maintenance 15, control room 12...).
   These are calibrated on ARIES/fission-class site analogs. Whether a
   factory-shipped 50 MWe unit on a gas-plant pad needs them is an
   analog-class question, not a scaling law - per the program's own rule
   that fission is not the default analog. A gas-class recalibration would
   release roughly 100 M$ (about 0.7 $/MWh at 1 GWe, transformative at
   50 MWe).
2. **The staffing law** (CAS70/CAS40 scale as P^0.5, INL basis). At
   50 MWe this alone is 27 $/MWh. The counter-story is fleet operation
   (one remote operations center serving many sites), which no documented
   record supports today - so under ledger discipline it stays.
3. **No fleet learning.** The one thing mass-producing 50 MWe units
   should earn - a Wright-curve discount on the equipment portion of
   CAS22 - does not exist in the model (`multi_unit_labor_factor` 0.92
   touches installation labor only). This is the alignment note's gap 1,
   and it is the only mechanism that could make the small-unit strategy
   *positively* cheaper rather than merely less penalized. It must be
   anchored carefully: the NOAK unit costs already assume a mature
   industry, so a Wright exponent may only be applied to production beyond
   the fleet size the NOAK constants implicitly price, or it double-counts.

The in-model conclusion is unambiguous either way: this concept's
economics live in power parks - many modules sharing one site, one staff,
one BOP - not in distributed standalone 50 MWe plants. Helion's actual
50 MWe PPA unit, priced standalone at the full tier-3 stack, is a 60+
$/MWh machine in this framework; clustered at the GWe scale the same
hardware is 16.

## What would have to be true to reach $10/MWh

In decreasing order of plausibility, on top of the full tier-3 stack at
3 GWe (12.4):

- **He-3 at effectively zero cost** (10.4): a mature D-D breeding economy
  or an external supply at two orders below the observed market (the only
  transacted prices, 2024-2026, are 19-22 M$/kg on gram-to-kilogram
  volumes; even tier 3's 0.5 M$/kg entry is 40x below them) - and even
  this does not break 10, because the tritium plant scales with breeding
  throughput.
- **Gas-class site and decommissioning analogs** (about 1-1.5 $/MWh): the
  fixed CAS21 site items and the 140 M$ dhe3 decommissioning provision
  recalibrated from fission-adjacent to industrial-plant class. Defensible
  only for the He-3-lean machine; the D-rich machine's tonne-class
  tritium inventory argues the other way.
- **A real fleet-learning term** on CAS22 equipment, anchored beyond the
  NOAK reference fleet: the only mechanism that rewards the mass-produced
  small-unit strategy at all.

None of these is in the study's evidence base at any tier. Within what the
study can defend: **records support about 105, defensible extrapolation
about 34, and coherent speculation bottoms at 16 (1 GWe) / 12 (3 GWe).**

## Caveats that survive into the headline

- The two largest tier-2 levers (cap life, rep rate) and the burn mix are
  respectively a published target, a roadmap paraphrase, and a sweep
  endpoint. No tier-2 entry is a measured record.
- The single most valuable missing measurement is a fusion-inclusive
  round-trip recovery efficiency on Polaris, separating the circuit factor
  from the PdV factor; it gates the composite cap and, through the wall
  budget, the rep-rate ceiling.
- The tier-3 stack is jointly, not just individually, heroic: 0.1 $/J
  capacitors *and* 1e10-shot life contradict the derating physics that
  connects cost to life; the composite recovery sits at the theory optimum
  with zero margin.
- Model gaps the reconciliation prices but the headline excludes:
  HVDC-class switch duty and tritium-plant scope. The main model
  conservatism cuts the other way (no thermal bottoming in the basis).
  The bands in the ladder table carry both.

## Relation to the Borealis study

Same framework, same evidence discipline, one ledger harmonized against
the other (divergence table in `docs/ledger.md`). At the speculation tier
the two concepts land within about a dollar of each other at 3 GWe
(Borealis 11.1, this 12.4); at the extrapolation tier the mirror is
materially cheaper (16.9 vs 33.9), chiefly because it needs no
capacitor-life miracle, no tritium plant, and no rep-rate roadmap - its
levers are already in the evidence tiers. On the down-select axis "how
much unpurchasable physics does the cheap number require", the mirror
requires less.
