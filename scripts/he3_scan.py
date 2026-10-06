"""He-3 price x burn-mix sweep: what the fleet-scale-supply concession is worth.

No defensible record exists for a He-3 price at fleet scale at ANY figure.
The only observed transactions are gram-to-kilogram scale at about
19-22 M$/kg (2024 spot about $2,500/L per Edelgas; Interlune's 2025 DOE
and Maybell agreements reference "today's commercial market price"; the
2026 TAE / Black Moon lunar option discloses no price), so the 2.0e+7
row is the recent commercial-spot anchor; the 4.5e6 row is the DOE
Isotope Program's allocated price (600 $/L to federal users in the 2011
allocation, CRS R41419, the second post's basis; commercial users paid
1,000 $/L), 2011 data that the market has since left several-fold
behind; and the baseline 2e6 $/kg is a concession against both. This sweep shows what each
concession is worth across the burn-mix span, at the tier-2
coherent-minimum machine. f_rad is coupled to the mix via the
bremsstrahlung floor; the tritium adder fires on the D-rich side. The
dd_frac 0.95 column probes how close deeper breeding gets to He-3
self-sufficiency (price-insensitivity is the test). A cell whose point
violates a coherence constraint at that chamber and rep rate (the D-rich
mixes fail constraint 8, their burn longer than the pulse period) is
starred.

A price concession also changes which mix the design search picks, so
the footer re-runs the search at u_he3 = 0 per burn mix (optimum_by_mix,
chamber, wall and firing rate chosen as the design search chooses them)
at the extrapolation and speculation grades and both plant sizes: free
He-3 is priced at the machine it would buy, not at the machine the ledger
price chose.
"""
import csv

from coherent_min import at_plant_size, scan
from study import (
    DEVICE_ORDER,
    DEVICES,
    OUTPUT_DIR,
    apply_records,
    build_model,
    coherence_violations,
    device_fwd,
    f_rad_floor,
    load_config,
    run,
)

U_HE3_USD_KG = (2e7, 4.5e6, 2e6, 1e6, 5e5, 1e5, 0.0)
DD_FRACS = (0.131, 0.314, 0.5, 0.7, 0.8, 0.85, 0.95)
RE_PRICE_TOP_N = 5


def optimum_by_mix(model, u_he3, net_electric_mw=1000.0, tier="tier3",
                   rows=None, **grid):
    """Best coherent design per burn mix at one He-3 price: the
    coherent_min scan (field, bank, gain, chamber, wall and rate ladder
    as the grade grants them, or the narrower `grid` given) re-run with
    u_he3 overridden, so a price concession is priced at the mix, field,
    bank, chamber and rate it would choose rather than at the machine the
    ledger price chose. The 1 GWe grid is scanned in full; a larger plant
    re-prices the top designs per mix, since the integer module count can
    trip the wall audit at size. `rows` short-cuts the scan with one
    already run at this price and grade."""
    overrides = {"u_he3": u_he3}
    if rows is None:
        rows = scan(tier, overrides, **grid)
    rows = [r for r in rows if r["coherent"]]
    out = []
    for dd in sorted({r["dd_frac"] for r in rows}):
        cands = sorted((r for r in rows if r["dd_frac"] == dd), key=lambda r: r["lcoe"])
        best = None
        for r in cands[:RE_PRICE_TOP_N]:
            diag, v = at_plant_size(model, tier, r, net_electric_mw, overrides)
            if diag is None or v:
                continue
            if best is None or diag["lcoe"] < best["lcoe"]:
                best = dict(
                    tier=tier, u_he3=u_he3, plant_mwe=net_electric_mw,
                    dd_frac=dd, f_rad=f_rad_floor(dd),
                    field_t=r["field_t"], bank_mj=r["bank_mj"],
                    yield_mj=r["yield_mj"], length_m=r["length_m"],
                    radius_m=r["radius_m"], fw_class=r["fw_class"],
                    max_f_rep=r["max_f_rep"],
                    lcoe=diag["lcoe"], n_mod=diag["n_mod"],
                    f_rep_hz=round(diag["f_rep_hz"], 3),
                    duty=round(diag["tau_burn_implied_s"] * diag["f_rep_hz"], 3),
                    tritium_adder=diag["tritium_adder_musd"],
                    availability=round(diag["availability"], 3),
                )
        if best is not None:
            out.append(best)
    return out


if __name__ == "__main__":
    cfg = load_config("baseline.yaml")
    model = build_model(cfg)
    fwd0 = dict(cfg["forward"])
    apply_records(fwd0, "best_case.yaml")
    apply_records(fwd0, "tier2.yaml")
    fwd0.update(DEVICES["extrap"]["overrides"])

    # The price x mix table holds the extrapolation device's chamber and
    # rate ceiling (its own duty-bound rate), so a mix whose burn is longer
    # than the device's overruns the period there and is starred; the
    # footer's re-run gives each mix its own rate.
    rows = []
    for u in U_HE3_USD_KG:
        for dd in DD_FRACS:
            fwd = dict(fwd0, u_he3=u, dhe3_dd_frac=dd, f_rad=f_rad_floor(dd))
            _, diag = run(model, fwd)
            violations = coherence_violations(fwd, diag, "tier2")
            rows.append(dict(u_he3=u, dd_frac=dd, f_rad=round(f_rad_floor(dd), 3),
                             lcoe=diag["lcoe"],
                             tritium_adder=diag["tritium_adder_musd"],
                             coherent=(not violations),
                             violations="; ".join(violations)))
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "he3_scan.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{'u_he3 $/kg':>12} " + "".join(f"dd={d:<6}" for d in DD_FRACS))
    for u in U_HE3_USD_KG:
        line = f"{u:>12.0f} "
        for d in DD_FRACS:
            r = next(x for x in rows if x["u_he3"] == u and x["dd_frac"] == d)
            line += f"{r['lcoe']:.1f}{'*' if not r['coherent'] else ' ':<3}"
        print(line)
    print("(* = violates a coherence constraint at that chamber and rep rate)")

    # The He-3 credit per device: the same machine with the decay return
    # withdrawn (bought in perpetuity at the ledger price) and with He-3
    # free, against its credited LCOE. The writeup quotes the two deltas.
    print("\nHe-3 credit per device at 1 GWe (perpetual purchase vs free, own mix):")
    print(f"{'device':>8} {'LCOE':>6} {'perpetual':>10} {'free':>6} {'+perp':>6} {'-free':>6} {'phi':>5}")
    for name, _ in DEVICE_ORDER:
        _, fwd = device_fwd(name, 1000.0)
        _, d = run(model, fwd)
        _, perp = run(model, dict(fwd, he3_decay_return=False))
        _, free = run(model, dict(fwd, u_he3=0.0))
        print(f"{name:>8} {d['lcoe']:>6.1f} {perp['lcoe']:>10.1f} {free['lcoe']:>6.1f} "
              f"{perp['lcoe'] - d['lcoe']:>+6.1f} {d['lcoe'] - free['lcoe']:>+6.1f} "
              f"{d['he3_purchase_fraction']:>5.2f}")

    # Free He-3 priced at the machine it would choose: the design search
    # re-run per burn mix at u_he3 = 0, at the extrapolation and
    # speculation grades and both plant sizes.
    mix_rows = []
    for tier in ("tier2", "tier3"):
        free_rows = scan(tier, {"u_he3": 0.0})
        for mwe in (1000.0, 3000.0):
            mix_rows.extend(optimum_by_mix(model, 0.0, mwe, tier=tier, rows=free_rows))
    with open(OUTPUT_DIR / "he3_free_by_mix.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(mix_rows[0]))
        w.writeheader()
        w.writerows(mix_rows)
    print("\nfree He-3 (u_he3 = 0), best coherent design per burn mix:")
    print(f"{'tier':>6} {'MWe':>5} {'dd':>6} {'LCOE':>6} {'B':>4} {'bank':>5} "
          f"{'yield':>6} {'L':>4} {'r':>5} {'wall':>6} {'ceil':>6} {'n_mod':>5} "
          f"{'f_rep':>6} {'duty':>5} {'T-adder':>8} {'avail':>6}")
    for r in mix_rows:
        print(f"{r['tier']:>6} {r['plant_mwe']:>5.0f} {r['dd_frac']:>6.3f} "
              f"{r['lcoe']:>6.1f} {r['field_t']:>4.0f} {r['bank_mj']:>5.0f} "
              f"{r['yield_mj']:>6.0f} {r['length_m']:>4.0f} "
              f"{r['radius_m']:>5.2f} {r['fw_class']:>6} {r['max_f_rep']:>6.2f} "
              f"{r['n_mod']:>5} {r['f_rep_hz']:>6.2f} {r['duty']:>5.2f} "
              f"{r['tritium_adder']:>8.1f} {r['availability']:>6.3f}")
