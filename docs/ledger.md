# Evidence ledger

Every non-baseline value adopted in the ladder, with the analog class named
and the reason it applies. Tiers follow the Borealis convention: tier 1 is a
citable record or published bound, tier 2 a labelled extrapolation from a
stated roadmap or physical argument, tier 3 labelled speculation with no
source. "Held at baseline" is the recorded outcome when no defensible value
exists.

Orientation: the machine is a pulsed D-He3 FRC with inductive DEC and no
turbine, 1 GWe as an integer count of Helion-class modules; design basis in
`config/baseline.yaml`, capacitor and pulsed-power evidence in
`docs/capacitor_technology_report.md`, adversarial findings in
`docs/red_team_review.md` (all of whose verdicts are folded into the tier
composition below), narrative answer in `docs/writeup.md`.

All numbers at costingfe `9f86c13` (cylinder geometry + wall-flux audit for
linear pulsed concepts), pinned by the regression tests in
`tests/test_study.py`. The tier stacks are `config/best_case.yaml`,
`config/tier2.yaml`, `config/tier3.yaml`; `scripts/tiers.py` reproduces the
ladder end to end.

Ladder at 1 GWe / 3 GWe (config stacks, concept-YAML chamber):

| rung | 1 GWe | 3 GWe |
|---|---|---|
| design baseline (Helion's implied point) | 119.4 | 114.9 |
| tier 1 records | 86.7 | 83.2 |
| tier 2 extrapolations | 38.3 | 34.2 |
| tier 3 speculation | 16.8 | 12.8 |

Design-optimized coherent minima (chamber, wall class, and burn mix chosen
by `scripts/coherent_min.py` under the physics-consistency constraints in
`scripts/study.py`): **tier 2: 33.7** at 1 GWe; **tier 3: 16.1** at 1 GWe,
**12.0** at 3 GWe. Reconciliation bands around the minima (model gaps and
conservatisms, `scripts/reconciliation.py`): tier 2 within 27.6-38.4, tier 3
within 13.9-17.3 at 1 GWe.

## Coherence constraints (enforced, not advisory)

Four physics couplings from the red-team review are enforced on every
quoted point by `study.coherence_violations`; a stack that violates one is
flagged in the output of every script rather than reported:

1. **f_rad is coupled to the burn mix.** A D-rich plasma radiates more, not
   less: Bosch-Hale + bremsstrahlung at the study calibration (baseline
   f_rad 0.163 at dd_frac 0.314 implies T_i 60-70 keV) gives f_rad about
   0.28 at dd_frac 0.85. `study.f_rad_floor` interpolates the review's
   computed anchors.
2. **Recovery is capped as a composite.** The only published figure on the
   plasma-to-electricity chain (APS DPP24: "optimal burn cycles exceeding
   90% recovery") speaks to the product eta_dec x f_pdv. Tier 2 keeps
   engineering margin (composite <= 0.80); tier 3 takes the theory optimum
   (0.90) with zero margin.
3. **The wall must survive the shot.** Steady flux within the bought
   first-wall class limit (panel 2, hhf 10 MW/m^2), and per-shot flash
   energy under the tungsten millisecond-melt bound (1.5 MJ/m^2, no
   margin).
4. **The D-rich fuel credit travels with its consequences.** Above
   dd_frac 0.5 the machine breeds tens of kg of tritium per year
   (41 kg/yr at 0.85); `study.run` charges a 200 M$ tritium-plant adder on
   C220500 (band 100-300 swept in reconciliation), and O&M stays at the
   baseline 27.5, never at an "aneutronic" discount.

## Tier 1: records and published bounds

| knob | baseline | value | analog class | why it applies | source | grade |
|------|----------|-------|--------------|----------------|--------|-------|
| interest_rate | 0.07 | 0.0425 | Sovereign-backed utility-scale generation with contracted offtake | Same structural argument as the Borealis study: a de-risked NOAK plant with firm long-term offtake can reach the same class of project finance. The licensing leg of the argument is weaker here than the fuel label suggests: at the D-rich burn mix this is a bulk tritium facility (see coherence constraint 4), so "minimal licensing" cannot be claimed alongside the fuel credit. The finance analog survives on the offtake/de-risking argument alone. | Apostoleris et al., Prog. Photovolt. 2021, implied 4.25% WACC from the Dubai MBR3 PPA. | strong |
| inflation_rate | 0.0245 | 0.02 | Developed-economy central-bank targeting | The interest-rate record is only coherent against a credible 2% backdrop. | Federal Reserve longer-run goals statement. | strong |
| construction_time_yr | 6.0 | 2.5 | Large single-block CCGT | Applies more strongly here than to the mirror: the plant is an integer count of factory-built modules, closer to CCGT block construction than to a single large bespoke machine. | Siemens Energy, 1200 MW CCGT block in about 30 months. | strong |
| indirect_fraction | 0.20 | 0.08 | Large industrial/power-plant EPC | Same cost-basis scope as NETL's EPCM line (fraction of total direct cost); 0.08 is the low end of the cited 8-10% band. | US DOE/NETL QGESS. | strong |
| availability | 0.85 | 0.95 | Geothermal baseload, derated for shot-cycled hardware | Geothermal's 97-98% has no analogue for a machine that swaps a multi-thousand-unit capacitor bank every few years (2.7e9 shots fired at the tier-2 point against a 1e9-shot bank). Staggered bank swaps plausibly cost 0.5-1.5%: 0.95 is the defensible figure. DIVERGES from Borealis's 0.98 with this stated technology reason. | US DOE Geothermal FAQs, derated per red-team Finding 9. | moderate |

**Held at baseline in tier 1:**

| knob | why not moved |
|------|---------------|
| lifetime_yr (30) | 80 years is an *anti-record* on this concept at tier-1 capacitor life: replacement accumulates faster than the capital-recovery benefit. Adopted in tier 3, where cap_shot_lifetime is high enough to invert the sign. The clearest case in the study of a record that does not travel between concepts. |
| c_cap_allin_per_joule (0.5) | Already at the optimistic end of its own documented 0.5-4.0 range; the industry statement is that Hz-rate operation still requires a 5-10x cost reduction. No record below the baseline exists. |
| eta_dec (0.85) | The 0.97 an earlier draft placed here is not tier-1-admissible: it is the top of a patent's prophetic circuit-only band (US 2024/0275198 A1), and Helion's "95% proven" statements trace to no-fusion circuit tests. Moved to tier 2 at 0.90 under the composite cap. |
| cap_shot_lifetime (1e8) | The 1e9 figure is a published NOAK *target* (Pacific Fusion AMPS) resting on a vendor-catalog derating extrapolation, not a life test; the largest rep-rated MJ-class precedent is 1.3e4 shots. Tier-2 material by the study's own convention. |

## Tier 2: labelled extrapolations

| knob | baseline | value | basis | grade |
|------|----------|-------|-------|-------|
| cap_shot_lifetime | 1e8 | 1e9 | Pacific Fusion AMPS sec. 4.1: 100 to 35 kV derating projected to reach about 1e9 shots at about 9x lower energy density; GA Series DE cross-check (3e7-3e9 at 20% reversal). At the tier-2 point the plant fires 2.7e9 shots, so the bank is still replaced about 1.7x (charged to CAS72 by the model); the "1e9 outlives the plant" argument holds only below about 1.1 Hz. | published target |
| eta_dec | 0.85 | 0.90 | Bottom of the patent band, circuit-only, no fusion-inclusive measurement. Paired with f_pdv under the composite cap (0.90 x 0.85 = 0.765 <= 0.80). | weak-moderate |
| f_pdv | 0.80 | 0.85 | Consistent with an about 18x adiabatic volume expansion, 1 - (V0/V1)^(2/3); leaves margin for incomplete fusion-product thermalization (14.7 MeV proton slowing time is ms-class at these conditions) and expansion-phase transport. | argued |
| eta_pin | 0.95 | 0.98 | Solid-state pulsed-power wall-plug efficiency; plausible for modern semiconductor switching, no datasheet or Helion statement located. | UNSOURCED |
| max_f_rep | 1.0 | 3.0 | No public Helion statement of a numeric plant rep rate exists (Polaris target about 1/s; Trenta about 1/10 min; the 1-10 Hz band is the concept YAML's roadmap paraphrase). 3 Hz is what the bought wall supports at this tier's recovery parameters; it remains UNSOURCED as a demonstrated cadence (nothing MJ-class has run at 1 Hz continuously). The band top (10 Hz) is tier 3. | UNSOURCED-ROADMAP |
| fw_class | panel | hhf | Machine-design purchase, not a record: divertor-grade monoblock wall (ITER divertor procurement anchor, 2.5 M$/m^2 NOAK, 10 MW/m^2 qualification) over the real 37.7 m^2 cylinder, about 94 M$/module, to make 3 Hz admissible in the concept-YAML chamber. The design-optimized tier-2 minimum instead buys a longer chamber with the cheaper panel wall (see coherent minimum below). | design purchase |
| dhe3_dd_frac | 0.314 | 0.85 | D-rich operation to raise in-situ He-3 breeding and cut the purchased-fuel line; the concept's own stated direction, but 0.85 is the top of a sweep, not a derived operating point. Adopted only jointly with f_rad 0.28 and the tritium-plant adder (coherence constraints 1 and 4). | UNSOURCED |
| f_rad | 0.163 | 0.28 | Bremsstrahlung-consistent radiated fraction at dd_frac 0.85 under the study calibration; relativistic corrections would raise it another 10-25%. Not an optimistic move: this knob *costs* 3.2 $/MWh against the incoherent alternative, and is the price of the fuel credit. | physics floor |

**Held at baseline in tier 2, harmonized with the Borealis ledger:**
om_cost_dhe3 (27.5: already the lowest documented CCGT fixed-O&M figure;
also required by coherence constraint 4), installation_frac (0.14: no
defensible record on the model's cost basis), f_rad as an independent
mover (withdrawn; it is now a coupled variable, not a knob).

## Tier 3: labelled speculation

No entry has a source; each is the optimistic edge of a stated argument or
an explicit leap. See `config/tier3.yaml` for the per-knob notes.

| knob | value | note |
|------|-------|------|
| max_f_rep | 10 | top of the third-party roadmap band; no duty-cycle analysis supports it |
| cap_shot_lifetime | 1e10 | required for coherence with 10 Hz; no source at any price; jointly heroic with the $/J entry below |
| eta_dec x f_pdv | 0.95 x 0.947 = 0.90 | the theory-optimal composite taken at face value, zero engineering margin |
| c_cap_allin_per_joule | 0.1 | below the model's own documented range floor; contradicts the derating physics that buys the cap life above |
| u_he3 | 5e5 $/kg | no fleet-scale He-3 market exists at any price |
| dec_staged_recovery_factor | 0.5 | patent's unquantified "net reduction in cost and size", optimistic edge |
| c_inv_per_kw_net | 50 $/kW | small lever |
| multi_unit_labor_factor | 0.80 | small lever |
| lifetime_yr | 80 | adopted only here, where cap life makes it favourable rather than an anti-record |
| yield_per_shot_mj | solved, not asserted | gain speculation is admitted, but the shot must be survivable in the chamber it is costed in: `coherent_min.py` solves yield and chamber jointly. The optimum is a broad plateau (200-750 MJ in a 45 m x 1.0 m single-module chamber, 2-9 Hz, panel wall at its flux limit). The earlier draft's Q = 40 (2000 MJ) in the 0.5 m x 10 m chamber deposits about 6.7 MJ/m^2 per shot, four times the tungsten flash-melt bound, and is excluded. |

## The coherent minimum, and the $10 question

`scripts/coherent_min.py` searches the design space the machine actually
controls (yield, chamber size, wall class, burn mix) under the coherence
constraints, at each evidence level:

| evidence level | minimum | design at the minimum |
|---|---|---|
| tier 2, 1 GWe | **33.7** | cited shot (101.4 MJ), 8 modules at 2.9 Hz, 20 m x 0.5 m chambers, panel wall at 1.8 MW/m^2, D-rich mix with tritium plant |
| tier 3, 1 GWe | **16.1** | 300 MJ shots (Q about 6), single module at 5.9 Hz, 45 m x 1.0 m chamber, panel wall at 1.9 MW/m^2 |
| tier 3, 3 GWe | **12.0** | 2 such modules at 8.8 Hz, 45 m x 1.5 m chambers |

Reconciliation (`scripts/reconciliation.py`) puts honest bands around
these: recovery-store and switch-stack replacement that CAS72 does not
charge (+2.4 tier 2, +0.0 tier 3), HVDC-class switch repricing (+1.6 /
+0.7), tritium-plant band (+-0.7), against the model's over-sized recovery
store (-2.6 / -1.2) and a thermal-bottoming basis change (-5.1 / -0.4):
tier 2 lands in 27.6-38.4, tier 3 in 13.9-17.3 at 1 GWe.

**The $10/MWh target is not reached by any coherent stack in this study.**
The closest approaches: 12.0 at 3 GWe on full tier-3 speculation, and 9.5
only if He-3 is additionally free (u_he3 = 0), which is one more
speculation than tier 3 already carries. What carries the floor at the
tier-3 minimum is no longer the capacitor bank: it is buildings (CAS21
286 M$), heat rejection and BOP (CAS24-26 about 170 M$), CAS50 (197 M$),
fuel handling plus the tritium plant (240 M$), and the first wall of the
big chamber (109 M$) - the accounts
`down_select/03_costingfe_alignment.md` already flags as carrying a
systematic bias against small modular units. See `docs/writeup.md`.

## Robustness of the tier-2 coherent minimum

One-at-a-time reversion from the 33.7 point (`scripts/tornado.py`):

| knob reverted | LCOE | delta |
|---|---|---|
| cap_shot_lifetime -> 1e8 | 53.4 | +19.7 |
| max_f_rep -> 1 Hz | 49.0 | +15.4 |
| dhe3_dd_frac -> 0.314 (with its f_rad) | 46.2 | +12.5 |
| f_rad -> 0.163 (incoherent: floor violated) | 30.5 | -3.2 |
| eta_dec -> 0.85 | 36.2 | +2.6 |
| f_pdv -> 0.80 | 35.7 | +2.0 |
| eta_pin -> 0.95 | 35.5 | +1.9 |

The three load-bearing tier-2 entries are the capacitor life, the rep
rate, and the burn mix - respectively a published target, an unsourced
roadmap band, and an unsourced sweep endpoint. None is a record. That is
the honest quality of the 33.7 figure.

## Consistency with the Borealis ledger

Both studies price NOAK plants with the same framework, so a knob gets the
same ruling in both unless a physics or technology difference is stated.

| knob | Borealis | Helion | divergence justified by |
|---|---|---|---|
| interest_rate | 0.0425 | 0.0425 | same |
| inflation_rate | 0.02 | 0.02 | same |
| construction_time_yr | 2.5 | 2.5 | same; argument stronger here (factory modules) |
| indirect_fraction | 0.08 | 0.08 | same |
| installation_frac | held 0.14 | held 0.14 | same |
| om_cost | held | held | same; additionally forced here by the tritium facility |
| f_rad_fus / f_rad | held | coupled variable | **stated physics reason**: here f_rad is a function of the burn mix (bremsstrahlung floor), not an independent knob; Borealis's photon fraction is set by its own burn physics and was held |
| availability | 0.98 | 0.95 | **stated technology reason**: shot-cycled capacitor bank replaced about 1.7x over plant life; the geothermal analog has no such outage |
| lifetime_yr | 80 | 30 at tiers 1-2, 80 at tier 3 | **stated technology reason**: capacitor replacement makes 80 yr an anti-record until cap life reaches about 1e10 at the operating rep rate |
| eta_th | 0.53 (combined cycle) | 0 (basis), 0.30 as reconciliation add-back | **stated technology reason**: no thermal conversion path in the machine basis; the rejected-heat stream at tier 2 makes bottoming worth -5 $/MWh, carried as an add-back exactly as Borealis carried its excluded-DEC add-back |
| conductor_cost_rebco | held | not applicable | copper pulsed coils, no HTS |
| fw_class / q_surface_max | hhf / 10 (machine design) | panel or hhf, design-optimized | same treatment: the wall package is machine design, not a record; here the wall is audited in-model against the declared class |
| unsourced first-order inputs | p_input quoted as a range | max_f_rep and yield quoted as a surface (`locus_scan.py`) | same treatment |

## Knobs with no effect

`core_lifetime_dhe3` moves LCOE by exactly zero at every operating point
quoted here. Recorded so it is not mistaken for an untested lever; it is
also why wall replacement had to enter through the coherence constraints
rather than through a lifetime knob the model ignores.

## What the ledger needs next

1. A measured, fusion-inclusive round-trip recovery efficiency on Polaris,
   separating the circuit factor from the PdV factor. It gates the
   composite-recovery entries directly and, through the wall-load budget,
   the honest rep-rate ceiling. Every other open item moves single $/MWh;
   this one moves tens.
2. A duty-cycle analysis for any rep rate above about 1 Hz: switch and
   capacitor cycle life, vacuum recovery at 100-300 ms periods, coil and
   chamber thermal management.
3. A sourced capacitor cost-at-life curve, replacing the single AMPS
   target point and resolving the c_cap / cap_shot_lifetime joint
   optimism the tier-3 stack currently carries.
4. A costed tritium plant scope for the D-rich fuel cycle (the 100-300 M$
   band here is an allowance, not an estimate), including its licensing
   posture.
