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

## Study usage

The constraint-6 cap uses only the verified stroke bound (the Q = 0 /
numerator limit); no quantity in the study evaluates the full
transcribed formula.
