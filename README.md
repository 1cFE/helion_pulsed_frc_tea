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
engineering entry (60/60/80/80 yr; the 60 is a series-consistency entry,
not a record), and availability is derived from each grade's
replacement schedule (Figure 1 and the ladder table's at-7% column keep
the financing part of every grade separate from its physics and
engineering), and differing only in the subsystem performance they are
granted: citable records, Helion's own requirements taken at face
value, labelled extrapolations, and labelled speculation
(`config/baseline.yaml` carries the common basis and Helion's
configuration; the stacks are `config/best_case.yaml`,
`config/tier2.yaml`, `config/tier3.yaml`). The compression field is a
stepped entry of the same ladder, carried in the tier configs like the
repetition-rate ceiling: the patent's 22 T burn point at the design
basis and records (corroborated in class by Helion's stated compression
field of more than 15 T), 30 T granted at extrapolations (a grant with
no public roadmap behind it), 40 T at speculation (an explicit leap),
each grade's design search free to use any field at or below its grant
and the scan pricing the field one grade ahead as a labelled
sensitivity. The driver bank is a design-search dimension graded the
same way (`scripts/coherent_min.py`): Polaris's sourced 50 MJ at
records, doubled at extrapolations, to 200 MJ at speculation. The burn
point follows the field (density as B^2 at beta = 1, breakeven time as
B^-2, per-pulse burnup as B^2, compressed flux volume as B^-2 and with
the bank). Nine physics-coherence constraints are carried on every
quoted point: the radiated fraction is coupled to the burn mix through
the bremsstrahlung floor, recovery efficiency is capped as a composite
(eta_dec x f_pdv), the wall must survive its steady flux and per-shot
flash energy in the wall class it is costed at, a D-rich burn mix
carries its tritium-plant consequences, the in-plasma tritium burn is
floored by the burnup closure, f_pdv is capped per point by the
chamber's adiabatic expansion bound at the point's own field and bank,
the shot yield is bounded by the plasma energy and the burn time, so
every point carries the burn time its shot implies at its own burn mix
and field, that burn must fit inside the pulse period, which caps one
burn section's fusion power and, with the wall's steady flux, sets the
burn mix and the firing rate together (a grade's granted rate ceiling
is permission, not obligation, and the search fires each device at or
below the lowest of its grant, the duty bound of its own burn and the
wall bound of its own module, in the fewest modules whose rate fits),
and the compression coil's magnetic pressure is audited on every point
and binds nowhere, because the coil that would deliver a granted field
is neither designed nor priced here. Every device except Helion's
configuration is a constrained design-space scan optimum (field, bank,
gain, chamber size, wall class, burn mix, firing rate), not an asserted
operating point.

Headline ladder at 1 GWe: records 112.1, Helion's requirements 105.9,
extrapolations 25.7 (32.6 at 7% real cost of capital), speculation 10.5
(17.6 at 7%) $/MWh; at 3 GWe the speculation park reads 8.2 $/MWh (14.3
at 7%), so one stack reaches the $10 target, as a park, on a 3% real
cost of capital worth 6.1 $/MWh, on a 40 T compression field worth 1.2
against the patent's 22 T (at which the park reads 9.4 and still
crosses), and on a driver bank four times Polaris's worth 0.1. The
field is worth 3.4 $/MWh at the extrapolation grade (25.7 at 30 T
against 29.1 at the basis) and the bank 0.3 there. The coil that would
deliver a granted field is the open item the ladder names: every shot
cycles it from zero to 193, 358 or 637 MPa at the three fields, 1.7 to
5.5 billion times over a book life, no conductor or case has a
gigacycle basis at any of those stresses, and the cost model's coil
account prices it below the 22 T coil (it integrates conductor along an
expansion adiabat that shrinks with the field and carries no
containment term), so the field is graded in the ladder rather than
bounded by the model. Every optimized device runs at the deuterium-rich
end of the mix grid: the records device duty-bound in 25 modules of 10
m x 0.75 m at 0.985 Hz, at 100% of the bound; the extrapolation and
speculation devices wall-bound at their granted fields, 4 modules of 15
m x 1.5 m at 2.37 Hz on the doubled bank and a single 30 m x 1.5 m
module firing 800 MJ shots at 2.23 Hz on the 200 MJ bank, with the
panel wall at 97 and 99.7% of its steady-flux limit. Every one of them
stores a tonne-class tritium inventory. Every number grants Helion's
gain, 128 MJ from a 50 MJ bank, which no record supports and which
implies a 0.3 to 0.7 s burn at the patent point against Helion's stated
pulse of hundreds of microseconds to milliseconds (the speculation
device's 800 MJ shot from its 200 MJ bank at 40 T, a gain of 4.0, needs
0.15 to 0.34 s). The records device sits 6.2 $/MWh above Helion's
requirements: reverting Helion's fourth nine of per-pulse fuel recovery
is worth about 47 $/MWh at Helion's own mix, most of which the records
device recovers by running at the deuterium-rich end of the mix grid,
where the tritium store's He-3 return covers most of its need. See
`docs/Helion_writeup.md` for the narrative results and `docs/ledger.md`
for record-by-record sourcing and the tornado ranking.

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
python3 coherent_min.py    # constrained minimum hunt over field (at or below each grade's grant), bank, gain, chamber, wall, mix and firing rate (the headline numbers; multi-process, a few minutes)
python3 tornado.py         # one-at-a-time reversion from the extrapolation device
python3 he3_scan.py        # He-3 price x burn-mix sweep, and the free-He-3 optimum re-chosen per mix
python3 breeder_loop.py    # dedicated pure-D breeders in the loop: park LCOE, endogenous He-3 cost
python3 locus_scan.py      # (max_f_rep, yield) surface with coherence flags
python3 module_scan.py     # module-count vs standalone-plant-size sweeps
python3 tritium_burn.py    # in-pulse T burn vs breed rate; dhe3_f_T audit
python3 mix.py             # He3/D ion ratio <-> dd_frac map at the study's mixes
python3 burnup_scan.py     # burn_fraction axis under both triton-fate limits
python3 yield_bound.py     # constraints 7 and 8: the shot against the plasma energy and burn time at each device's own field and bank, and the burn against the pulse period across x_s
python3 reconciliation.py  # adders/credits the model cannot price, honest bands
python3 make_figures.py    # paper figures into docs/figures/
python3 make_html.py       # writeup and ledger -> outputs/Helion_writeup_notion.html, ledger_notion.html (deterministic, figures embedded)
python3 make_latex.py      # the same two -> outputs/Helion_writeup and ledger as .tex and .pdf (pandoc + pdflatex, figures as PDF)
python3 -m pytest ../tests # closure, config-integrity, ladder regression
```

Outputs (CSV + console tables) land in `outputs/`, which is gitignored.
