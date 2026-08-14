# Helion-class pulsed FRC TEA study

This repo is a techno-economic analysis (TEA) of a Helion-class pulsed
D-He3 field-reversed-configuration power plant with inductive direct energy
conversion and no turbine, built on top of the `costingfe` cost model. The
machine basis takes Helion's own architecture at face value: a 50 MJ
capacitor-bank driver (Polaris, sourced), inductive recovery of driver and
PdV energy through the coil circuit (eta_th = 0; radiated and undirected
charged energy is discarded, with a thermal-bottoming add-back carried in
`scripts/reconciliation.py`), copper pulsed coils, in-situ plasmoid
formation, and a per-shot yield back-derived from Helion's 50 MWe PPA claim
rather than from any disclosed measurement. 1 GWe is the baseline anchor,
built as an integer count of Helion-class modules; see
`config/baseline.yaml` for the basis rationale.

The study is a floor hunt: it answers "how low can this concept's LCOE be
pushed, and what would have to be true", against Helion's public $10/MWh
target. The quoted story starts at the design baseline and the evidence
ladder applies records, then labelled extrapolations, then labelled
speculation on top (`config/best_case.yaml`, `config/tier2.yaml`,
`config/tier3.yaml`). Four physics-coherence constraints from the
red-team review (`docs/red_team_review.md`) are enforced on every quoted
point: the radiated fraction is coupled to the burn mix through the
bremsstrahlung floor, recovery efficiency is capped as a composite
(eta_dec x f_pdv), the wall must survive its steady flux and per-shot
flash energy in the wall class it is costed at, and a D-rich burn mix
carries its tritium-plant consequences. The minimum at each evidence
level is then found by a constrained design-space scan (chamber size,
wall class, yield, burn mix), not by asserting an operating point.

Headline: coherent tier-3 speculation bottoms at about 16.8 $/MWh at
1 GWe and 13.5 $/MWh at 3 GWe; the $10 target is not reached by any
internally consistent stack. Records alone price the concept at about
173 $/MWh (above its own design baseline: the recovery reversions
outweigh the finance records); defensible extrapolation about
41 $/MWh. See `docs/writeup.md` for the narrative results
and `docs/ledger.md` for record-by-record sourcing, the tornado ranking,
and the knob-by-knob consistency audit against the sister study
`borealis_mirror_tea`.

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
(f_pdv, 1 - f_rad); and the fuel cycle is per-pulse (patent-anchored
burn_fraction 1.2e-4 with species-resolved DHE3 recycle losses, the
JET-analog fuel_recovery 0.999 default, and the 22 T compression-field
basis); and PULSED_FRC coils are priced along the expansion adiabat
(conductor ~ L^(1/3)), so chamber length is active structure. The ladder regression tests in
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
python3 tornado.py         # one-at-a-time reversion from the tier-2 minimum
python3 he3_scan.py        # He-3 price x burn-mix sweep
python3 locus_scan.py      # (max_f_rep, yield) surface with coherence flags
python3 module_scan.py     # module-count vs standalone-plant-size sweeps
python3 tritium_burn.py    # in-pulse T burn vs breed rate; dhe3_f_T audit
python3 burnup_scan.py     # burn_fraction axis under both triton-fate limits
python3 reconciliation.py  # adders/credits the model cannot price, honest bands
python3 make_figures.py    # paper figures into docs/figures/
python3 -m pytest ../tests # closure, config-integrity, ladder regression
```

Outputs (CSV + console tables) land in `outputs/`, which is gitignored.
