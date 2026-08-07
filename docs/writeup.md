# How low can a Helion-class pulsed FRC go?

The down-select question this study answers: pushed to the physically
coherent limit of optimism, what is the minimum LCOE of a Helion-like
pulsed inductive-DEC D-He3 plant, and does it reach Helion's own public
$10/MWh (1 cent/kWh) target?

**Answer: the coherent floor is about 16 $/MWh at 1 GWe and 12 $/MWh at
3 GWe, on full tier-3 speculation. The $10 target is not reached by any
internally consistent stack the study can construct; it needs one more
speculation on top of full speculation (He-3 at effectively zero price
brings 3 GWe to 9.5). The evidence-backed numbers are far higher: 86.7 on
records alone, 33.7 on labelled extrapolations.**

All numbers at costingfe `9f86c13`, reproduced by `scripts/tiers.py`,
`scripts/coherent_min.py`, and `scripts/reconciliation.py`; regression
tests pin the ladder in `tests/test_study.py`.

## The ladder

| rung | 1 GWe | 3 GWe | what it contains |
|---|---|---|---|
| design baseline | 119.4 | 114.9 | Helion's implied point: 50 MJ driver, 101.4 MJ yield, 1 Hz, D-rich mix at its bremsstrahlung floor |
| tier 1: records | 86.7 | 83.2 | finance (4.25%), 2.5 yr construction, 8% indirects, availability 0.95 |
| tier 2: extrapolations | 38.3 | 34.2 | cap life 1e9, recovery composite 0.765, 3 Hz on a bought divertor-class wall, D-rich mix with tritium plant |
| tier 3: speculation | 16.8 | 12.8 | 10 Hz, composite 0.90, cap $/J 0.1, cap life 1e10, He-3 at 0.5 M$/kg, 80 yr |

Design optimization under the same evidence (chamber size, wall class, and
yield chosen rather than inherited) improves the last two rungs to **33.7**
(tier 2, 1 GWe) and **16.1 / 12.0** (tier 3, 1 / 3 GWe). Reconciliation
bands (model gaps vs conservatisms): tier 2 in 27.6-38.4, tier 3 in
13.9-17.3 at 1 GWe.

## How to push toward the minimum: what actually works

Ranked by what the tornado and the coherent scan say, the levers that move
a Helion-class machine down the ladder are:

1. **Capacitor cycle life** (+19.7 $/MWh if lost). Not the glamorous knob,
   but the single largest: at the baseline 1e8-shot life the bank is
   replaced about 8 times over plant life and replacement dominates the
   capital service. Everything else in the study presumes this solved to
   1e9; the only support is a published derating target.
2. **Rep rate** (+15.4). Going from 1 to 3 Hz collapses the module count
   from 24 to 8. But rep rate is bought with wall area: the machine that
   supports it is a longer chamber with a panel wall run near its 2 MW/m^2
   qualification, or a divertor-class wall in a short one. Nothing
   MJ-class has ever run at 1 Hz continuously; this is a roadmap band, not
   a spec.
3. **Burn mix** (+12.5). D-rich operation (dd_frac 0.85) cuts the
   purchased He-3 line from about 31 to 9 $/MWh. It is only honest as a
   package: the D-rich plasma radiates twice as much (f_rad 0.28, not
   0.05), breeds 41 kg of tritium a year, and buys a tritium plant. The
   package is still worth +12.5; the incoherent version of it (fuel credit
   without consequences) would claim about 16 and is excluded.
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
6. **Scale** (16.1 to 12.0). The 3 GWe plant amortizes buildings, BOP,
   and CAS50 across modules. This is the same sublinear-BOP effect that
   penalizes the 50 MWe unit Helion actually sells; at 50 MWe the same
   stack prices far above any of these numbers.

## What carries the floor

At the tier-3 minimum (16.1, single 300 MJ module at 5.9 Hz), the
capacitor-driver narrative is spent: the driver bank is 15 M$ of a 641 M$
reactor account. The floor is carried by:

| item | M$ | $/MWh (approx) |
|---|---|---|
| buildings (CAS21) | 286 | 1.6 |
| CAS50 (capitalized supplementary) | 197 | 1.1 |
| fuel handling + tritium plant (C220500) | 240 | 1.3 |
| heat rejection + turbine-plant BOP (CAS24-26) | 170 | 0.9 |
| first wall of the 45 m chamber (C220101) | 109 | 0.6 |
| DEC power electronics (C220109) | 64 | 0.4 |
| O&M (CAS70) | 54/yr | 6.5 |
| annualized capital, all-in | | about 7.8 |

Two of these lines are already flagged program-wide as systematically
biased against small modular units (buildings and BOP scaling,
`down_select/03_costingfe_alignment.md`), which is why the honest answer
to "can this reach 10" is *not quite, and the residual is as much a claim
about the cost model's treatment of small plants as about the concept*.

## What would have to be true to reach $10/MWh

In decreasing order of plausibility, on top of the full tier-3 stack at
3 GWe (12.0):

- **He-3 at effectively zero cost** (9.5): a mature D-D breeding economy
  or an external He-3 supply at two orders below today's price.
- **The small-module BOP/buildings bias resolved in the concept's favor**:
  if CAS21 + CAS50 + CAS24-26 scale like factory-built gas plants rather
  than like nuclear-adjacent civil works, 2-3 $/MWh comes out.
- **A cheaper tritium story**: the 240 M$ fuel-handling line presumes the
  D-rich machine is a bulk tritium facility. If Helion's stored-decay
  fuel cycle licenses and operates lighter than that, about 1 $/MWh
  comes out.

None of these is in the study's evidence base at any tier. Within what the
study can defend: **records support about 87, defensible extrapolation
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
  recovery-store/switch replacement outside CAS72, HVDC-class switch duty,
  tritium-plant scope. Model conservatisms cut the other way (oversized
  recovery store, no thermal bottoming in the basis). The bands in the
  ladder table carry both.

## Relation to the Borealis study

Same framework, same evidence discipline, one ledger harmonized against
the other (divergence table in `docs/ledger.md`). At the speculation tier
the two concepts land within about a dollar of each other at 3 GWe
(Borealis 11.1, this 12.0); at the extrapolation tier the mirror is
materially cheaper (16.9 vs 33.7), chiefly because it needs no
capacitor-life miracle, no tritium plant, and no rep-rate roadmap - its
levers are already in the evidence tiers. On the down-select axis "how
much unpurchasable physics does the cheap number require", the mirror
requires less.
