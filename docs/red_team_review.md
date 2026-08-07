# Red-team review of the Helion-class pulsed FRC TEA

Independent adversarial review of the ladder in `docs/ledger.md` (design
baseline 113.6 -> tier-1 51.3 -> tier-2 17.0 -> tier-3 10.7 $/MWh at 1 GWe)
and of the supporting `docs/capacitor_technology_report.md`. Written against
the analyst's documents, not as edits to them. All model numbers below were
re-run against `costingfe` at commit `aa81822` with `COSTINGFE_BACKEND=numpy`;
the published ladder reproduces exactly (113.6 / 51.3 / 17.0 / 10.7, and 10.0
at 80 years), so disagreements below are with the inputs and the claims, not
with arithmetic drift.

Verdict vocabulary: **impossible** (physically impossible, internally
inconsistent, or arithmetically wrong), **unsupported** (possible but without
evidence), **fine**.

A reproducibility note up front: the study repo has zero git commits, and
`config/`, `scripts/`, and `docs/writeup.md` referenced throughout the design
doc and ledger do not exist. The ladder was reproducible only by
reconstructing the tier stacks from the ledger's tables. Everything below
should be read with that caveat: the archived repo does not contain the study
it describes.

---

## Finding 1 (Priority 1): `max_f_rep` = 10 Hz

**Claim.** Tier 2 raises the rep-rate ceiling from 1 to 10 Hz on "Helion's
roadmap language", worth -30.7 $/MWh and collapsing n_mod from 24 to 2-3.

**Verdict: unsupported, and internally inconsistent with the machine as
costed.** Not kinematically impossible, but 10 Hz does not survive as a
usable lever.

**Sourcing.** No Helion statement of a 10 Hz plant rep rate exists. Polaris
is targeted at about 1 pulse per second (design capability, not demonstrated
sustained); Trenta's demonstrated cadence was one pulse per 10 minutes;
Scientific American reports the commercial machine as intended to "pulse
about once per second". Press coverage (Fortune, New Atlas) attributes to
Helion a need of roughly 10 Hz to meet the 50 MW Microsoft obligation, which
cuts the other way entirely: if 10 Hz is what the *50 MWe* plant needs, then
the per-shot net output is about 5 MJ, and the model's yield anchor (101.4 MJ
back-derived from 50 MWe *at 1 Hz*) is an order of magnitude too generous.
The ladder cannot have both: it sources yield from the (50 MWe, 1 Hz) branch
and rep rate from the 10 Hz branch, producing a 500 MWe-class module that no
public Helion statement supports.

**Wall-load ceiling.** At the fixed 101.4 MJ shot, the wall receives
(radiation + undirected charged + DEC circuit waste) about 50 MJ per shot at
the design-basis recovery parameters (f_rad 0.163, f_pdv 0.80, eta_dec 0.85),
and about 42 MJ at eta_dec 0.90. On a realistic chamber surface for the
YAML's own geometry (0.5 m plasma radius, 10 m length: about 35 m^2), the
costed `panel` wall class (2 MW/m^2 qualification) allows:

- panel wall, defensible recovery parameters: f_rep <= about 1.4 Hz
- hhf (divertor-monoblock) wall at 10 MW/m^2: f_rep <= about 7 Hz, at an
  uncosted 2.5 M$/m^2 x 35 m^2 = about 87 M$ per module plus its cooling loop

The tier-2 point (f_rep 6.54 Hz solved, p_wall 85.9 MW/module = 2.5 MW/m^2
plus 1.5 MW/m^2 of neutrons) already exceeds its own costed wall class, and
it only comes that close because f_pdv = 0.95 and f_rad = 0.05 suppress the
wall load; both of those values fail independently (Findings 2 and 3). With
corrected recovery parameters the solver runs the same wall at 6-8 MW/m^2.
The 10 Hz lever is therefore not independent: it is only reachable if the
two recovery knobs are simultaneously at values shown below to be
unsupported or impossible. The model never checks this because the wall-flux
audit (`fw_class_q_limit`) only fires when `q_surface_max` is supplied, which
the pulsed path never does.

**Cycle-life at 10 Hz.** 10 Hz x 0.98 availability x 30 yr = 9.3e9 shots,
against the tier-1 "record" life of 1e9: nine bank replacements, plus the
same count on the recovery store and switch stack that the model never
replaces at all (Finding 7). The ledger's own tier-1 argument that 1e9
"outlives the plant and more buys nothing" is written for 1 Hz and is false
at the tier-2 operating point, which fires 6.1e9 shots.

**Other duty limits.** FRC formation/merge/compression/expansion is a
millisecond-class event, so a 100 ms period is kinematically available (the
Helion patent's stated full cycle spans 1 us to 100 ms; 10 Hz sits exactly at
the long edge). Vacuum recovery of about 1.4e21 particles per shot in 100 ms
needs an effective pumping speed of order 500-1000 m^3/s or full directed
capture in the expander tanks, with helium ash that cryopanels pump poorly;
Helion has patents on capture-type divertor pumping but nothing demonstrated
above 1 Hz-class cadence. Circuit dissipation (1 - eta_dec)(E_driver +
E_pdv) f_rep is 100+ MW per module at 10 Hz with eta_dec 0.90, deposited in
the coils, switches, and bank, none of it with a costed cooling system. For
precedent: the largest rep-rated pulsed-power demonstration found is a
Sandia LTD cavity at sub-MJ scale, 0.08 Hz, 1.3e4 shots. Nothing MJ-class
has ever run at 1 Hz continuously, let alone 50 MJ at 10 Hz.

**Defensible treatment.** A supportable ceiling is 1-1.5 Hz with the machine
as costed, or about 3 Hz if the study buys a divertor-class wall and its
cooling loop explicitly. Within the tier-2 stack, 3 Hz instead of 10 Hz is
worth +2.2 $/MWh before the wall hardware is added (17.0 -> 19.2, n_mod 5),
and the wall hardware adds several more (Finding 11). 10 Hz should be
demoted to tier 3.

---

## Finding 2 (Priority 2): `f_pdv` = 0.95 and `eta_dec` = 0.97 double-book one projected number

**Claim.** Tier 2 takes f_pdv = 0.95 (fraction of non-radiated charged
fusion energy appearing as PdV work on the field); tier 1 takes eta_dec =
0.97 (circuit recovery, coil to capacitor). Jointly worth about 38 $/MWh.
The model composes them multiplicatively: `p_recovered = eta_dec * (p_driver
+ f_pdv * p_charged_net)` (`physics.py`, pulsed_dec_forward).

**Verdict: the pair is an internally inconsistent double-use of a single
projected composite figure; f_pdv = 0.95 is additionally physically
implausible on its own.**

**What the sources actually say.**

- The APS DPP24 abstract (GO05.8, Kirtley, Lewis, Pancotti) says direct
  recovery "is projected to significantly exceed thermal energy recovery
  systems, with optimal burn cycles exceeding 90% recovery." This is a
  thermodynamic-cycle projection: the fraction of plasma energy recovered as
  electricity through the whole generalized Otto/Diesel cycle *including*
  "realistic modern circuit components". It is the composite
  eta_dec x f_pdv, for an optimal cycle, in theory, with no experiment.
- The patent (US 2024/0275198 A1, para [0129]) says recovery "can be up to
  90% and higher... between 85% and 95% or between 90% and 97%". This is
  circuit-only ("energy recovered per cycle for this circuit that is not
  consumed by the load"), generic power-electronics boilerplate with
  prophetic language, no measurement, and no tie to fusion-produced energy.
- Helion's public "95% proven" statements trace, where traceable at all, to
  no-fuel or no-fusion circuit tests and magnet efficiency (their own
  diagnostics blog describes exactly that test protocol), never to a
  fusion-inclusive energy balance on Trenta or Polaris.

So the only number that speaks to the plasma-to-electricity chain is the
theory projection "greater than 90% for optimal cycles", and it is the
*product*. The ladder assigns 0.95 to one factor and 0.97 to the other,
whose product (0.92, with driver recovery at 0.97) sits at the theoretical
optimum with zero engineering margin, sourced twice from what is one claim.

**Physics of f_pdv.** For an adiabatic monatomic expansion, the recoverable
fraction of internal energy is 1 - (V0/V1)^(2/3):

- f_pdv = 0.80 requires an 11x volume expansion
- f_pdv = 0.95 requires an 89x volume expansion

and on top of the expansion ratio, 0.95 requires that essentially all fusion
product energy thermalizes into plasma pressure before the expansion ends.
A 14.7 MeV proton's electron-drag slowing time at Helion-class conditions
(n_e 1e22-1e23 m^-3, T_e 20-50 keV) is 0.5-5 ms, comparable to or longer
than the burn-plus-expansion window, and its gyroradius at peak field (about
4 cm at 15 T) is a large fraction of the compressed separatrix radius, so a
non-trivial fraction of product energy is promptly lost or leaves
unthermalized. Transport losses during the expansion (FRC energy confinement
in this regime is anomalous and ms-class at best) come out of the same
budget. 0.80 is already an optimistic engineering value; 0.95 stacks a 89x
expansion, full thermalization, and negligible transport into one number.

**Defensible treatment.** Cap the composite: eta_dec x f_pdv <= 0.80 (for
example eta_dec 0.90, f_pdv 0.85, or 0.85/0.80 as the YAML ships). Within
the tier-2 stack, f_pdv back to 0.80 is +1.6 $/MWh and eta_dec to 0.90 is
+1.0 $/MWh one-at-a-time, but their joint effect with the corrected f_rad
and the wall constraint is much larger (see the corrected ladder). eta_dec
= 0.97 must leave tier 1: a patent's prophetic band top is not a record
under the study's own Borealis convention, as the ledger itself concedes
while keeping the value anyway.

---

## Finding 3: `f_rad` = 0.05 at `dhe3_dd_frac` = 0.85 is below the bremsstrahlung floor

**Claim.** Tier 2 simultaneously moves the burn mix D-rich (dd_frac 0.314 ->
0.85, for He-3 self-supply) and cuts f_rad from 0.163 to 0.05. The ledger
flags the pair as "probably inconsistent" but does not resolve it.

**Verdict: impossible.** Resolved with Bosch-Hale reactivities and
non-relativistic bremsstrahlung (relativistic corrections make it worse by
10-25%): at fixed temperature, making the plasma D-rich enough to put 85% of
primary events in the D-D channel requires n_D/n_He3 of about 30-40, the
D-He3 power term collapses, and the radiated fraction *rises* by a factor
1.6-1.9 relative to the 0.314 mix at any temperature where the concept works
at all:

| T_i (keV), T_e = T_i/2 | f_rad at dd_frac 0.314 | f_rad at dd_frac 0.85 |
|---|---|---|
| 50 | 0.18 | 0.28 |
| 70 | 0.11 | 0.21 |
| 100 | 0.08 | 0.16 |
| 150 (and T_e = 0.3 T_i) | 0.06 | 0.10 |

The study's baseline calibration (f_rad 0.163 at dd_frac 0.314) is
consistent with T_i about 60-70 keV at T_e = T_i/2. Holding that
calibration, the D-rich point carries f_rad about 0.26-0.31, not 0.05.
f_rad = 0.05 is unreachable at dd_frac 0.85 at *any* temperature below 150
keV even with extreme two-temperature operation. (Side finding for
costingfe: the concept YAML's shipped default, f_rad 0.05 at dd_frac 0.131,
is also below the bremsstrahlung floor at reactor temperatures; the floor at
the YAML mix is about 0.08-0.14.)

**Cost.** Within the tier-2 stack, f_rad 0.28 alone is +2.7 $/MWh (17.0 ->
19.7), and it pushes the solved rep rate to 8.7 Hz and the wall to 8.3
MW/m^2, i.e. it also breaks Finding 1's wall budget. The correct tier-2
treatment is: take the D-rich fuel credit only together with f_rad about
0.28 and the neutron/tritium consequences of Finding 4.

---

## Finding 4: the D-rich machine is costed as an aneutronic one

**Claim (implicit across the stack).** O&M cut to 15 M$/yr "aneutronic, no
tritium plant, no turbine island"; fuel handling C220500 = 40 M$; licensing
0.75 yr "near zero"; panel first wall, 5 cm shield, no breeding blanket;
construction and availability analogs (CCGT, geothermal) argued from the
absence of nuclear-grade systems.

**Verdict: internally inconsistent.** One root, many symptoms: the burn mix
that funds the tier-2 fuel savings produces a strongly neutronic, heavily
tritiated machine, and none of the consequences appear in any account.

Computed at the model's own operating points (dhe3_f_T = 0, i.e. bred
tritium extracted, per Helion's stated plan of storing it for He-3 decay):

- Baseline (dd_frac 0.314): 19 kg of tritium bred per year, 56 MW of
  neutrons at plant level.
- Tier 2 (dd_frac 0.85): **41 kg of tritium per year** and **104 MW of
  neutron power** (mostly 2.45 MeV), a neutron wall load of about 1.5
  MW/m^2 on the realistic chamber area, behind which sit 5 cm of shield and
  copper coils.

For scale: a 1 GW-fusion D-T plant burns about 56 kg of tritium per year,
and ITER's site inventory limit is about 4 kg. Helion's own fuel-cycle plan
(tritium collected, purified, stored on getter beds for 12.3-year decay to
He-3) implies a steady-state on-site inventory of tens to hundreds of
kilograms at this production rate. That is a full tritium plant, a
substantial activation and remote-handling burden, wall dpa at a rate that
makes the uncharged `core_lifetime` knob (which the ledger notes moves LCOE
by exactly zero, without alarm) a missing replacement line, and a licensing
posture nothing like "0.75 yr, near zero". The tier-1 analog arguments for
availability (geothermal) and construction time (CCGT, "no nuclear-grade
civil works") are all weakened by the same fact.

**Defensible treatment.** Either run He-3-lean (keep purchased He-3, lose
the 21 $/MWh fuel credit) or cost the D-rich machine honestly: tritium
plant capital of order 100-300 M$, O&M back at or above the 27.5 baseline,
hhf-class or thicker-shielded wall with a replacement schedule, and licensing
assumptions of a tritium-inventory facility. Either branch adds several
$/MWh to tier 2; the stack as published takes the credit from one branch and
the cost basis from the other.

---

## Finding 5: tier-3 gain (Q = 40, 2000 MJ/shot)

**Claim.** Yield 2000 MJ at the 50 MJ driver, at the model's "interior
optimum" Q = 40; worth -47 $/MWh, the largest tier-3 lever.

**Verdict: unsupported by four to five orders of magnitude, and physically
inadmissible in the costed geometry.**

- The published FRC record triple product is 2.3e17 keV m^-3 s (TAE C-2W,
  2021; LSX before it at 7.1e16). Q = 40 in D-He3 needs ignition-class
  confinement, order 1e22-1e23 keV m^-3 s. No FRC measurement is within
  four orders of magnitude; Helion has published no triple product at all.
- The baseline yield (101.4 MJ) is back-derived from Helion's 50 MWe claim
  through this model's own DEC chain, so, as the ledger already concedes,
  neither end of the 101-2000 MJ range is evidence. It is worse than
  unevidenced if the press-reported "10 Hz needed for 50 MW" is real
  (Finding 1): then even 101.4 MJ is 10x high.
- A 2000 MJ shot in the YAML's 0.5 m x 10 m chamber deposits about 230 MJ
  per shot on the wall (6.7 MJ/m^2 in a millisecond-class flash). The
  transient heat-flux factor is about 200 MJ m^-2 s^-1/2, four times the
  melting threshold of tungsten. The single-module tier-3 machine melts its
  own first wall each shot; the wall is costed at $1.6M.
- The Q = 40 "interior optimum" the tier rides is an artifact of `delta_cap`
  growing linearly with yield using the mis-sized store of Finding 7; it is
  a property of the cost model's bookkeeping, not of the machine.

Tier 3 is labelled speculation, which is honest; but it should not be
quoted even as a coherent speculative design point, because the geometry it
is costed in cannot survive it.

---

## Finding 6: capacitor evidence, grades, and the cost-at-life derivation

**Claims.** cap_shot_lifetime 1e9 graded "strong" (tier 1) from Pacific
Fusion AMPS sec. 4.1 with GA cross-check; life scaling L proportional to
E^-7.32 and energy density proportional to E^2 give cost proportional to
L^0.273, so the 1000-fold life increase costs about 6.6x; the bank is "a
hard gate but not the binding constraint".

**Verdicts.**

1. **Grade inflation (unsupported as tier 1).** AMPS 4.1 is explicit
   projection language: derating 100 -> 35 kV "would be expected to"
   increase life from about 1e5 to about 1e9 shots, offered as "an example
   of the first approach", and its citation for the claim is a vendor's
   general catalog (CSI Blue catalog), not a life test. A published *target*
   resting on a catalog extrapolation is tier-2 material under the study's
   own convention. Nothing anywhere has demonstrated 1e9 shots at these
   parameters; the demonstrated rep-rated precedent is 1.3e4 shots at 0.08
   Hz, sub-MJ (Sandia LTD).
2. **Arithmetic inconsistency (wrong).** cost proportional to L^(2/7.32) =
   L^0.273 is derived correctly, and 1000^0.273 = 6.6. But the report's own
   stated gap is 1.7e4 -> 1e9 shots, a factor of 59,000, which by the same
   scaling costs a factor of 20, not 6.6. The "1000x" belongs to a different
   baseline (about 1e6-shot commercial parts). The report mixes the two: "a
   laboratory rating near 1.7e4 shots, that is the 1000-fold improvement" is
   off by a factor of 60 in life. The combined cost-at-life ask is then
   about 100-200x, not the quoted 30-65x.
3. **Exponent risk (unsupported).** The 7.32 exponent is real but is the
   favorable end of the literature; the CERN/Gallay metallized-film work
   fits n about 3.5 and states the fit is validated only between 0.7 and
   1.3 of rated voltage. At n = 3.5 the cost-at-life exponent is L^0.57 and
   the derating penalty explodes. Extrapolating any of these power laws
   over five orders of magnitude in life has no support in the literature.
   The tier-1 combination (1e9 shots AND 0.5 $/J with no energy-density
   penalty) is double-optimistic on its own sources: AMPS buys its 1e9 with
   9x more capacitor volume.
4. **"Saturates at 1e9" (internally inconsistent).** True only at 1 Hz. The
   tier-2 plant fires 6.1e9 shots and replaces the bank six times; the
   tier-2/tier-3 headline numbers depend on rep rates at which the report's
   saturation argument, and the ledger sentence built on it, are false.

The conclusion "hard gate but not the binding constraint" survives in
direction (the recovery/rep-rate knobs are indeed worth more), but its
quantitative support is weaker than stated in both directions.

---

## Finding 7: C220109 store sizing and the missing replacement of the recovery hardware

**Claim under test.** `markup_cap = eta_dec*(1 + q_sci*f_ch) - 1`: the
recovery store is sized for driver energy plus charged fusion energy. The
design doc alleges the surplus is double-counted against the grid inverter.

**Verdicts (one root, opposite-signed symptoms: the recovery path is priced
and replaced on inconsistent bases).**

1. **Store sizing is inconsistent with the model's own physics
   (over-conservative).** `physics.py` returns to the circuit
   eta_dec*(E_driver + f_pdv*(1 - f_rad)*f_ch*Y), but `cas22.py` sizes the
   store for eta_dec*(E_driver + f_ch*Y): the f_pdv and (1 - f_rad) factors
   are dropped, i.e. the bank is bought for charged energy that the same
   model sends to the wall as heat. At the baseline this oversizes the
   fusion term by 1.57x (markup 1.53 vs the physics-consistent 0.98, about
   15 M$/module); at tier-2 values the gap is 11%. This is also what
   manufactures the tier-3 Q = 40 cost optimum.
2. **The inverter is not a double count.** The buffer store (energy-rated)
   and the grid inverter (power-rated) are different hardware and both
   needed; charging both is correct in kind. The design doc's allegation
   does not hold.
3. **CAS72 replaces the wrong subset (under-conservative, larger).**
   Scheduled replacement charges only C220107, the driver bank. The
   recovery store (`delta_cap`, 40-91 M$/module, 1.5x to 18x the driver
   bank) and the switch stack cycle once per shot with the same
   full-reversal duty and the same film physics, and are never replaced. At
   the baseline the cycled-but-unreplaced capital is 42 M$/module against
   26 M$ replaced: CAS72 (157 M$/yr) is understated by roughly 2.6x, about
   +30 $/MWh at the baseline and +3-4 $/MWh at tier 2 if the recovery store
   lives as long as the driver bank.
4. **Switch duty is priced off-class (unsupported, probably large).**
   `delta_switch` = 6% of the cap bank (1.5 M$/module) for a stack that at
   tier 2 commutes about 1.7 GW average power continuously and accumulates
   6e9 deep cycles over plant life. The 6% markup is single-shot pulsed
   practice; GW-class continuous silicon (HVDC valve class) is order
   100 M$/GW, and power-cycling qualification for press-pack devices is
   1e7-1e8 cycles, two orders short, with no replacement line. This account
   deserves the same scrutiny the capacitors got and has had none.

---

## Finding 8: the geometry undercosts the entire reactor core, and no wall constraint exists anywhere

`PULSED_FRC` falls into the MIF spherical branch of `compute_geometry`, so
the "10 m long, 0.5 m radius" machine of the YAML's own comments is costed
as a 0.6 m radius sphere: first wall 4.6 m^2 ($1.6M), and vessel, structure,
and pumping in proportion. The real chamber area is about 35 m^2 (7x), and
the tier points put 2.5-4.3 MW/m^2 average (plus neutrons) onto a wall
qualified, and priced, for 2. The `fw_class_q_limit` audit never fires for
this concept because `q_surface_max` is a mirror-path parameter that the
pulsed path never sets. Consequences: (a) reactor-core hardware is a
near-zero cost line, flattering the "everything is capacitors" narrative;
(b) physics penalties do not feed back into cost, so the solver absorbs bad
recovery values by running the same $1.6M wall harder (visible in the
corrected runs: raising f_rad from 0.05 to 0.28 at tier 2 moves LCOE only
17.0 -> 19.7 while wall flux triples). Fixing the geometry and enforcing the
wall class is the single most important *model* change for this concept:
without it, Findings 1-3 cost almost nothing in-model and the ladder cannot
price the physics it assumes.

---

## Finding 9: availability 0.98

**Verdict: unsupported but minor.** The replacement cost is charged (CAS72,
with a warning), so it is not double-missing; what is missing is the outage
time. At tier 2 each module swaps a 2,500-unit bank every 5 years; staggered,
that is plausibly 0.5-1.5% availability, on top of a geothermal analog that
has no shot-cycled hardware at all. 0.93-0.95 is defensible; 0.98 is not.
Worth about 1-2 $/MWh (0.90 costs +1.7 at tier 2). The deeper problem with
the geothermal analog is Finding 4 (this is a tritium facility).

---

## Finding 10: thermal-only exhaust self-consistency

**Verdict: fine in structure, mispriced in detail.** With eta_th = 0, the
plant rejects p_loss = 276 MW (tier 2 published) to 1.2 GW (corrected tier-2
stack) of low-grade heat at 1 GWe net. After the C220200 fix (coolant loop
now scaled on thermal power) the heat-rejection BOP is present and
reasonably sized (CAS26 about 33 M$ for 1.2 GW rejected is cooling-tower
class). What is not present is the plasma-facing side of that chain: the
actively cooled wall taking the flux (Finding 8) and its replacement
(Finding 4). The decision to discard rather than bottom the heat is a
legitimate machine basis, but at the corrected f_rad the discarded stream is
1.2 GW, which makes the no-bottoming choice itself worth revisiting in the
reconciliation rather than in the headline.

---

## Corrected ladder

Re-running the model with the published tier stacks and this review's
corrections (all at 1 GWe, reproducing configuration):

| rung | LCOE ($/MWh) | n_mod | notes |
|---|---|---|---|
| tier 1 as published | 51.3 | 18 | contains eta_dec 0.97 |
| tier 1 cleaned (eta_dec 0.90, availability 0.95) | 58.0 | 21 | |
| tier 2 as published | 17.0 | 2 | wall 2.5 MW/m^2 on a panel wall |
| tier 2, f_rad 0.28 only | 19.7 | 2 | wall 8.3 MW/m^2, inadmissible |
| tier 2, corrected stack (f_rad 0.28, f_pdv 0.80, eta_dec 0.90, 3 Hz, O&M 27.5, installation 0.14) | 31.0 | 9 | before wall/tritium adders |
| defensible composite (cleaned tier 1 + 3 Hz + hhf wall class + D-rich at f_rad 0.28) | 33.3 | 9 | wall still priced on 4.6 m^2 |
| defensible composite (1.5 Hz, panel wall) | 39.1 | 18 | |

The 33-39 range still excludes the items the model cannot currently price:
the real-area hhf wall (about +87 M$/module at 35 m^2, roughly +6 $/MWh at
9 modules), the tritium plant and its O&M (+2-5), switch-stack realism and
recovery-store replacement (+3-5), and geometry-corrected vessel/structure
(+1-2). Adding them puts the concept at roughly **40-50 $/MWh**. That is
consistent with, and slightly above, the ledger's own honesty check
("minus every UNSOURCED entry: 35.5"), which this review effectively
confirms as the defensible headline before the uncosted hardware.

---

## Summary of verdicts

| item | verdict |
|---|---|
| max_f_rep 10 Hz | unsupported; inconsistent with costed wall, cap life prose, and the yield anchor; ceiling 1-3 Hz |
| f_pdv 0.95 + eta_dec 0.97 | double-use of one projected composite; f_pdv 0.95 physically implausible (89x expansion + full thermalization); cap composite at 0.80 |
| eta_dec 0.97 as tier-1 record | inadmissible; patent prophetic circuit-only band; "95% proven" traces to no-fusion circuit tests |
| f_rad 0.05 at dd_frac 0.85 | impossible (bremsstrahlung floor 0.16-0.31); correct value about 0.26-0.31 at the study's own calibration |
| dd_frac 0.85 consequences | 41 kg/yr tritium, 104 MW neutrons, uncosted everywhere; costing takes the aneutronic branch's cost basis with the D-rich branch's fuel credit |
| Q = 40 / 2000 MJ | unsupported by 4-5 orders vs FRC record; melts the costed wall each shot; optimum is a cost-model artifact |
| cap_shot_lifetime 1e9 "strong" | grade inflated: projection from a vendor catalog; "saturates" claim false at tier-2 rep rates |
| cost proportional to L^0.273 | derivation arithmetic fine; "1000x = 6.6x" inconsistent with the report's own 59,000x gap (correct: 20x); literature exponent risk (n about 3.5) makes it far worse |
| markup_cap (C220109) | over-conservative vs physics.py by f_pdv(1-f_rad) (1.57x at baseline); inverter is not a double count |
| CAS72 replacement scope | under-conservative: recovery store + switches (1.6-18x the driver bank) cycle every shot, never replaced |
| switch stack pricing | unsupported: GW-average duty and 6e9 cycles priced at 6% of the cap bank, no replacement |
| spherical geometry + unenforced wall class | wrong for this concept; root cause of "physics is nearly free" behavior |
| availability 0.98 | unsupported; 0.93-0.95 defensible; about 1-2 $/MWh |
| thermal-only exhaust | fine as a basis post-C220200-fix; wall-side hardware still missing |
| tier-1 finance (4.25%, 2.5 yr build, 8% indirects) | inherited analogs, weakened by the tritium/licensing finding but not re-litigated here |
| repo state | unreproducible as archived (no commits, no configs/scripts); ladder reproduced only by reconstruction |

## Where this concept lands

On evidence that survives scrutiny, this machine prices at roughly **40-50
$/MWh at 1 GWe**: tier-1 finance and construction records (cleaned of the
patent-band eta_dec) on top of the design-basis physics, a 1-3 Hz rep rate,
the bremsstrahlung-consistent radiated fraction, and the neutron/tritium
hardware the D-rich fuel cycle actually requires. That is 4-5x Helion's $10
target and about 2.5x the published tier-2 headline. The 17.0 figure
requires three values this review finds respectively unsupported (10 Hz),
double-booked (0.95 x 0.97), and impossible (f_rad 0.05); the 10.7 figure
additionally requires a gain four orders beyond the FRC record in a chamber
that could not survive it.

The single piece of missing evidence that would most change this estimate is
a **measured, fusion-inclusive round-trip recovery efficiency on Polaris**:
capacitor-to-capacitor, with fusion yield present, separating the circuit
factor from the PdV conversion factor. It gates the two knobs worth 38
$/MWh directly, and through the wall-load budget it also sets the honest
rep-rate ceiling, which is the other structural lever. Every other open item
(capacitor cost-at-life, switch duty, tritium plant scope) moves single
$/MWh; this one number moves tens.
