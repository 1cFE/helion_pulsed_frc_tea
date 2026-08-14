# Kirtley APS DPP 2024 (GO05.8): transcribed cycle formulas and verification status

Slide captures: `kirtley_dpp24_otto_slide.png`, `kirtley_dpp24_diesel_slide.png`.

## Generalized Diesel efficiency (transcribed from the slide)

    eta_cp = [ m^(-g) ( -CR m (1+Q)^g + CR^g m^g (1 + Q g) ) ]
             / [ (1+Q) ( CR^g (1 + Q(g-1)) + CR (g-2) ) ]

with g the adiabatic index (1.66 plasma, 1.8 plasma+field), CR the
convergence ratio of the initial adiabatic compression
(CR = x_l^-1 x_s^-2), m = ER/CR the post-extraction to post-merger
volume ratio, and Q = dU/U the charged-particle fractional energy
change of the burn.

## Verification (independent derivation, constant-pressure burn)

Cycle: adiabatic compression by CR; isobaric burn with V3 = (1+Q) V2
(consistent with Q = dU/U at constant pressure); adiabatic expansion to
V4 = m CR V2; stage-4 energy exhausted. In units of U2:

    W_out = U2 + dH - U4 = [ (1 + Q g) - (1+Q)^g (m CR)^(1-g) ] U2

- **Numerator VERIFIED**: the transcribed numerator divided by CR^g
  equals this W_out exactly. At Q = 0 it reduces to
  1 - (m CR)^(1-g): the study's constraint-6 adiabatic-stroke bound
  with m CR the total volume ratio.
- **Denominator OPEN**: the naive input ledger
  W_comp + E_merger + dH = (1 + g Q) U2 does not reproduce the
  transcribed denominator, which carries an extra (g-1) Q^2 term and a
  (2-g)-weighted merger energy. The gap is definitional (what counts
  as input energy, possibly the lumped plasma+field fluid's ledger)
  and material: at g = 5/3, CR = 10, m = 2, Q = 2 the naive accounting
  gives 0.80 against the transcribed 0.51. Resolve against the talk
  (youtu.be/5nHmqk1cI2E) before any numerical use.

## Generalized Otto efficiency (transcribed from the slide)

    eta_cp = [ CR^g ER^(-g) (-ER + ER^g) ] / [ CR^g + CR (g-2) ]

- **Numerator VERIFIED**: it factors to CR^g (1 - ER^(1-g)), the pure
  adiabatic-stroke recovery at the expansion ratio, gain-independent
  as the slide's own note claims; the energy-balance construction for
  a constant-volume burn gives W_out = (1+Q)(1 - ER^(1-g)) U2 against
  naive inputs (1+Q) U2, so gain cancels identically.
- **Cross-check PASSED**: the Diesel transcription at Q = 0 reduces
  exactly to the Otto transcription (numerator and denominator), so
  the two slides are one coherent framework and both transcriptions
  are faithful.
- **Denominator convention localized**: both cycles share the same
  denominator family, reducing to W_comp + (g-1) U_merger, i.e. the
  merger energy enters as P1 V1 rather than U1. Open questions for the
  talk: the reason for the (g-1) merger weight, and the Diesel
  formula's extra (g-1) Q^2 fusion-input term. Under the ordinary
  state definitions this denominator lets eta_cp exceed the naive
  energy-balance efficiency (and nominally unity at large ER). The
  talk does not elaborate on the denominator (checked), so the input
  definition is unresolvable from public material: the >90%
  optimal-cycle claim cannot be independently reproduced and must not
  be used numerically. It survives only as the qualitative statement
  behind the tier-3 composite cap, whose speculation grade already
  reflects this.

## Study usage

The constraint-6 cap uses only the verified stroke bound (the Q = 0 /
numerator limit); no quantity in the study evaluates the full
transcribed formula.
