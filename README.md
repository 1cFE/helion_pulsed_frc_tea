# Helion-class pulsed FRC TEA study

This repo is a techno-economic analysis (TEA) of a Helion-class pulsed
inductive direct-energy-conversion power plant, no turbine anywhere,
whose burning plasma is a D-He3 field-reversed configuration; it is
built on top of the `costingfe` cost model. The machine basis takes
Helion's own architecture at face value: a 50 MJ capacitor-bank driver
(Polaris, sourced), inductive recovery of driver and expansion-work
energy through the coil circuit (eta_th = 0; radiated and undirected
charged energy is discarded, with a thermal-bottoming add-back carried
in `scripts/reconciliation.py`), copper pulsed coils, in-situ plasmoid
formation, and a per-shot yield solved, not disclosed: the shot at which
the model, at the patent's burn point, delivers Helion's 50 MWe PPA
module at 1 Hz (128 MJ, gain 2.56), fired in the smallest chamber that
survives it (0.61 m plasma radius). 1 GWe is the baseline anchor, built
as an integer count of Helion-class modules; see `config/baseline.yaml`
for the basis rationale.

This study is the down-select's deep dive into the subject of the
second 1cFE blog post ("Direct Energy Conversion for Fusion"): the
concept that post examined at the free-core level is priced here as a
complete plant, and supporting it required extending `costingfe` itself
(per-pulse fuel-cycle semantics, chamber-coupled recovery bounds,
adiabat-priced coils, shot-cycled replacement scope).

The study is a floor hunt: it answers "how low can this concept's LCOE
be pushed, and what would have to be true", against Helion's public
$10/MWh target. Four devices are priced, sharing one architecture and
one plant environment in which build time and indirects are held, the
cost of capital steps with the tiers (7/7/5/3% real), book life is an
engineering entry (30/30/80/80 yr), and availability is derived from
each grade's replacement schedule (Figure 1 and the ladder table's at-7%
column keep the financing part of every grade separate from its physics
and engineering), and differing only in the subsystem performance they
are granted: citable records, Helion's own requirements taken at face
value, labelled extrapolations, and labelled speculation
(`config/baseline.yaml` carries the common basis and Helion's
configuration; the stacks are `config/best_case.yaml`,
`config/tier2.yaml`, `config/tier3.yaml`). Seven physics-coherence
constraints are enforced on every quoted point: the radiated fraction is
coupled to the burn mix through the bremsstrahlung floor, recovery
efficiency is capped as a composite (eta_dec x f_pdv), the wall must
survive its steady flux and per-shot flash energy in the wall class it
is costed at, a D-rich burn mix carries its tritium-plant consequences,
the in-plasma tritium burn is floored by the burnup closure, f_pdv is
capped per point by the chamber's adiabatic expansion bound, and the
shot yield is bounded by the plasma energy and the burn time, so every
point carries the burn time its shot implies. Every device except
Helion's configuration is a constrained design-space scan optimum
(chamber size, wall class, yield, burn mix), not an asserted operating
point.

Headline ladder at 1 GWe: records 110.4, Helion's requirements 103.9,
extrapolations 26.1 (32.7 at 7% real), speculation 10.6 (17.8 at 7%)
$/MWh; at 3 GWe the speculation park reads 8.4 $/MWh (14.6 at 7%), so
the $10 target is crossed by one internally consistent stack and only
through its 3% real cost of capital, not through any physics or
engineering entry; it holds at any availability above the model default.
Every number grants Helion's 128 MJ shot, which no record supports and
which implies a 0.3 to 0.7 s burn against Helion's stated pulse of
hundreds of microseconds to milliseconds. The records device sits 6.5
$/MWh above Helion's requirements: reverting Helion's fourth nine of
per-pulse fuel recovery is worth about 49 $/MWh at Helion's own mix,
nearly all of which the records device's deuterium-rich mix recovers.
See `docs/writeup.md` for the narrative results (`docs/short_writeup.md` is
the half-length version) and `docs/ledger.md` for
record-by-record sourcing, the tornado ranking, and the knob-by-knob
consistency audit against the sister study `borealis_mirror_tea`.

## Requirements

This study depends on `costingfe` from `/mnt/c/Users/talru/1cfe/1costingfe`
at commit `44434d9` or later. That guarantees: linear pulsed concepts are
costed as cylinders with the first-wall flux audited against the declared
`fw_class` (panel/hhf pricing on the real chamber area); pulsed `p_wall`
counts undirected ash plus radiation plus DEC circuit waste; the
rep-rate sizing path (`size_from_power=True`) solves f_rep and the integer
module count off the `max_f_rep` ceiling; the primary coolant account
scales on thermal power; scheduled replacement at `cap_shot_lifetime`
covers the full shot-cycled recovery chain (driver bank plus the
C220109_cap/C220109_switch sub-lines) with its short-life warning; the
inductive-DEC store markup is sized for the physics-returned energy
(f_pdv, 1 - f_rad); the fuel cycle is per-pulse (patent-anchored
burn_fraction 1.2e-4 with species-resolved DHE3 recycle losses, the
JET-analog fuel_recovery 0.999 default, and the 22 T compression-field
basis); and PULSED_FRC coils are priced along the expansion adiabat
(conductor growing as L^(1/3)), so chamber length is active structure.
The ladder regression tests in
`tests/test_study.py` pin the numbers at that commit and fail loudly if
the model moves under the study.

The scripts set `COSTINGFE_BACKEND=numpy` themselves (before importing
`costingfe`), so sensitivities are concrete float64 differences rather
than `jax.grad`, which diverges from the concrete `forward()` on this
study's solver paths.

## Running the study

```bash
cd scripts
python3 run_baseline.py    # design-basis point (Helion's implied point)
python3 tiers.py           # the evidence ladder at 1 and 3 GWe
python3 coherent_min.py    # constrained minimum hunt (the headline numbers)
python3 tornado.py         # one-at-a-time reversion from the extrapolation device
python3 he3_scan.py        # He-3 price x burn-mix sweep, and the free-He-3 optimum re-chosen per mix
python3 breeder_loop.py    # dedicated pure-D breeders in the loop: park LCOE, endogenous He-3 cost
python3 locus_scan.py      # (max_f_rep, yield) surface with coherence flags
python3 module_scan.py     # module-count vs standalone-plant-size sweeps
python3 tritium_burn.py    # in-pulse T burn vs breed rate; dhe3_f_T audit
python3 mix.py             # He3/D ion ratio <-> dd_frac map at the study's mixes
python3 burnup_scan.py     # burn_fraction axis under both triton-fate limits
python3 yield_bound.py     # constraint 7: the shot against the plasma energy and burn time
python3 reconciliation.py  # adders/credits the model cannot price, honest bands
python3 make_figures.py    # paper figures into docs/figures/
python3 make_html.py       # writeup, short writeup and ledger -> outputs/Helion_writeup_notion.html, Helion_short_writeup_notion.html, ledger_notion.html (deterministic, figures embedded)
python3 make_latex.py      # the same three -> outputs/Helion_writeup, Helion_short_writeup and ledger as .tex and .pdf (pandoc + pdflatex, figures as PDF)
python3 -m pytest ../tests # closure, config-integrity, ladder regression
```

Outputs (CSV + console tables) land in `outputs/`, which is gitignored.
