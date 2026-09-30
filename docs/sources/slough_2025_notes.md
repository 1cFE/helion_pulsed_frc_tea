# Slough 2025, source note

J. Slough (MSNW LLC), "A compact fusion reactor based on the staged
compression of a field reversed configuration," Nuclear Fusion 65 (2025)
106019, doi 10.1088/1741-4326/ae034d. Reference [16] in the writeups.
Publisher page read 2026-09-30; the body beyond section 3 was truncated
in that read, which is why two of the four claims below are marked
unverified.

## Verified against the publisher page

**The D-T gain advantage of 240** (writeup Section 5). Verbatim:
"Whatever possible reactor benefit there could be for employing a
partially aneutronic fusion reaction it is highly doubtful that it would
make up for the D-T gain advantage of 240." The factor is derived one
sentence earlier: "From equation (5) the total reduction in fusion
energy gain for D-3He from D-T is therefore (1/7)^2.5 . (0.134/0.25) =
0.004", whose reciprocal is 250; the paper's own prose rounds it to 240,
which is the figure this study quotes.

**The reactor is D-T.** Abstract: "The resulting D-T fusion yield for the
3.5 MJ FRC is 20-40 MJ/pulse", i.e. a gain of 5.7 to 11.4 on the FRC
energy, against the abstract's "fusion gain as large as 10".

**The burn point.** Abstract: "The final stage is a 12 cm diameter, 3-6 m
long confinement and burn chamber with a vacuum field of 7-9 T produced
by external solenoidal coils inside the flux conserving cylinder. The
vacuum field is compressed by the FRC on insertion to 35 T resulting in
fusion gain conditions for the 2-5 ms transit." The transit window and
the field carry the constraint-7 cross-check in Section 6; the 34.8 T
and 15 keV of that cross-check are the paper's design-point values, not
the abstract's rounded 35 T.

## Not yet verified against the page

**The 40% recovery ceiling** (ledger coherence constraint 6, writeup
Section 6, the RISK row in `reconciliation.py`): the bound
(1 - x_s^2)/(2.5 - x_s^2) on the share an ejected FRC returns in a
flux-conserving expansion chamber, cited as equation 18, with the FRC
coming to rest holding 1.5 pV of thermal energy and not free-expanding.
The abstract states only the mechanism: "The final ejection and
expansion of the FRC into a large, low field mirror chamber provides a
mechanism for FRC energy recovery."

**The gain of 9.1** at 34.8 T and 15 keV over the 2 to 5 ms transit
(writeup Section 6, ledger constraint 7). The abstract's 20-40 MJ from
3.5 MJ brackets it.

Both sit in the paper's section 4, which the read did not reach. Neither
is load-bearing for the ladder: the 40% ceiling is priced as a risk row
(+17.4 / +4.2 $/MWh) rather than enforced, and the 9.1 point is a
cross-check on constraint 7, not an input to it.
