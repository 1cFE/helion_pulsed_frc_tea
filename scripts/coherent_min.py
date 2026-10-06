"""Constrained minimum-LCOE hunt: the study's answer to "how low can this go".

Instead of asserting a speculative operating point (the earlier draft's
Q = 40 in a chamber that flash-melts at that yield), this scan searches the
design space the machine actually controls - shot yield, chamber size, wall
class, burn mix, and firing rate - under the red-team coherence constraints
(study.py): bremsstrahlung-consistent f_rad, composite recovery cap, steady
wall flux within the bought wall class, per-shot flash energy under
tungsten melt, tritium plant charged whenever the mix is D-rich, and the
shot's implied burn (at the point's own mix) fitting inside the pulse
period at the solved rep rate (constraint 8).

The firing rate is a design choice, not a grant. costingfe sizes a plant by
bisecting f_rep against the per-module net target and solving the integer
module count off the max_f_rep ceiling, so every design it builds fires
just under its ceiling in the fewest modules the ceiling permits. A grade's
granted ceiling (1 Hz at the design basis and records, 3 Hz at
extrapolations, 10 Hz at speculation) is permission, not obligation: the
same plant power can be delivered slower in more modules, which is how a
power-sparse burn mix satisfies constraint 8. The scan therefore evaluates
each (yield, chamber, wall, mix) point at a ladder of effective ceilings
at and below min(granted ceiling, 1 / implied burn), the top of which is
the highest coherent rate, and never above the grant. Cost is not monotone
in the module count (more modules buy more hardware; a slower bank is
replaced fewer times over the book life and the derived availability rises
with it), so the ladder is priced rather than shortcut to the fewest
feasible modules.

Two evidence levels:
- tier2: the extrapolation stack; the shot is the design-basis one
  (config/baseline.yaml: 128.1 MJ, the yield that reproduces the PPA at
  the patent burn point), so the freedoms are geometry, wall class, burn
  mix and rate.
- tier3: the speculation stack; yield is also free (gain speculation),
  because tier 3 already concedes it is unevidenced - but it must still be
  survivable in the chamber it is costed in.

The chamber is resized honestly: the coil bore tracks the plasma radius
(r_bore = plasma_t + gap), and the cylinder wall, vessel, and structure are
repriced by the model at the scanned size.
"""
import csv
import itertools

from costingfe.model import SizingInfeasible

from study import (
    OUTPUT_DIR,
    apply_records,
    build_model,
    coherence_violations,
    duty_bound_rate_hz,
    f_rad_floor,
    load_config,
    run,
)

# Each burn mix sits exactly on its bremsstrahlung floor (constraint 1):
# the concept preset's He-3-rich mix, the 3:1 D:He-3 mix that buys its
# fuel and makes few neutrons, Helion's own mix (the patent's He3/D 0.158,
# the first mix that stores tritium and carries the tritium plant), three
# mixes between it and the D-rich one, and the D-rich mix that breeds
# more He-3 than it burns. Constraint 8 turns the mix into a continuous
# trade (breeding against burn length, paid in firing rate and module
# count), so the grid is dense on the deuterium side.
BURN_BRANCHES = tuple(
    {"dhe3_dd_frac": dd, "f_rad": f_rad_floor(dd)}
    for dd in (0.131, 0.314, 0.488, 0.6, 0.7, 0.8, 0.85)
)
FW_CLASSES = ("panel", "hhf")
LENGTHS_M = (10.0, 15.0, 20.0, 30.0, 45.0, 60.0)
RADII_M = (0.5, 0.75, 1.0, 1.5)
YIELDS_MJ = (128.1, 150.0, 200.0, 300.0, 500.0, 750.0, 1000.0, 1500.0, 2000.0)
# The ladder of effective ceilings at a point, as fractions of the highest
# coherent rate min(granted ceiling, 1 / implied burn). Each step that
# binds forces a larger integer module count; a step that does not bind
# (the previous step's solved rate already sits under it) reproduces the
# previous design and is skipped.
RATE_STEPS = (1.0, 0.9, 0.8, 0.7, 0.6, 0.5)

_VACUUM_T = 0.10


def tier_fwd(tier: str) -> dict:
    base_cfg = load_config("baseline.yaml")
    fwd0 = dict(base_cfg["forward"])
    apply_records(fwd0, "best_case.yaml")
    if tier in ("tier2", "tier3"):
        apply_records(fwd0, "tier2.yaml")
    if tier == "tier3":
        apply_records(fwd0, "tier3.yaml")
    return fwd0


def point_fwd(fwd0, y, length, radius, fw, branch, max_f_rep=None) -> dict:
    fwd = dict(fwd0, **branch)
    fwd["yield_per_shot_mj"] = y
    fwd["chamber_length"] = length
    fwd["plasma_t"] = radius
    fwd["r_bore"] = radius + _VACUUM_T  # coil bore tracks the chamber
    fwd["fw_class"] = fw
    if max_f_rep is not None:
        fwd["max_f_rep"] = max_f_rep
    return fwd


def granted_ceiling_hz(fwd: dict, model) -> float:
    """The rate ceiling the point's stack grants (the concept default when
    no tier record raises it)."""
    return float(fwd.get("max_f_rep", model._eng_defaults["max_f_rep"]))


def rate_ceilings_hz(fwd: dict, model) -> list[float]:
    """The effective ceilings scanned at a point, descending: RATE_STEPS
    times the highest coherent rate, min(granted ceiling, 1 / implied
    burn), the burn read at the reference x_s and the point's own mix as
    study.run reports it; and, where the burn overruns the granted period,
    the grant itself first, so the design the search would build without
    the rate as a lever is priced beside the ones that fit. Never above
    the grant."""
    granted = granted_ceiling_hz(fwd, model)
    e_del = float(fwd.get("e_driver_mj", model._eng_defaults["e_driver_mj"]))
    top = min(granted, duty_bound_rate_hz(fwd, e_del))
    ladder = [top * s for s in RATE_STEPS]
    if top < granted:
        ladder.insert(0, granted)
    return ladder


def rate_designs(model, fwd: dict):
    """The distinct designs a point yields down its rate ladder: (fwd with
    the ceiling set, diagnostics) per binding step. A ceiling the previous
    design's solved rate already clears changes nothing and is skipped; an
    infeasible sizing (net <= 0 at the ceiling) ends the ladder, since
    every lower ceiling is infeasible too."""
    last_f_rep = None
    for ceiling in rate_ceilings_hz(fwd, model):
        if last_f_rep is not None and last_f_rep <= ceiling * (1 + 1e-9):
            continue
        f = dict(fwd, max_f_rep=ceiling)
        try:
            _, diag = run(model, f)
        except SizingInfeasible:
            return
        last_f_rep = diag["f_rep_hz"]
        yield f, diag


def scan(tier: str):
    base_cfg = load_config("baseline.yaml")
    model = build_model(base_cfg)

    fwd0 = tier_fwd(tier)
    yields = YIELDS_MJ if tier == "tier3" else (fwd0["yield_per_shot_mj"],)
    # tier-1 coherence uses the tier-2 cap set (no tier-1-specific caps exist)
    check_tier = "tier2" if tier == "tier1" else tier
    granted = granted_ceiling_hz(fwd0, model)

    rows = []
    for y, length, radius, fw, branch in itertools.product(
        yields, LENGTHS_M, RADII_M, FW_CLASSES, BURN_BRANCHES
    ):
        point = point_fwd(fwd0, y, length, radius, fw, branch)
        for fwd, diag in rate_designs(model, point):
            violations = coherence_violations(fwd, diag, check_tier)
            rows.append(
                dict(
                    tier=tier,
                    yield_mj=y,
                    length_m=length,
                    radius_m=radius,
                    fw_class=fw,
                    dd_frac=branch["dhe3_dd_frac"],
                    granted_hz=granted,
                    max_f_rep=round(fwd["max_f_rep"], 4),
                    lcoe=diag["lcoe"],
                    n_mod=diag["n_mod"],
                    f_rep_hz=round(diag["f_rep_hz"], 3),
                    duty=round(diag["tau_burn_implied_s"] * diag["f_rep_hz"], 3),
                    availability=round(diag["availability"], 4),
                    q_wall_mw_m2=round(diag["q_wall_mw_m2"], 2),
                    e_flash_mj_m2=round(diag["e_flash_mj_m2"], 3),
                    capital_per_kw=round(diag["capital_per_kw"]),
                    coherent=(not violations),
                    violations="; ".join(violations),
                )
            )
    return rows


def at_plant_size(model, tier, r, net_electric_mw):
    """A scan row's design re-sized to another plant power, same shot,
    chamber, mix and ceiling (the integer module count re-snaps)."""
    branch = next(b for b in BURN_BRANCHES if b["dhe3_dd_frac"] == r["dd_frac"])
    fwd = point_fwd(tier_fwd(tier), r["yield_mj"], r["length_m"], r["radius_m"],
                    r["fw_class"], branch, r["max_f_rep"])
    fwd["net_electric_mw"] = net_electric_mw
    try:
        _, d = run(model, fwd)
    except SizingInfeasible:
        return None, ["sizing infeasible"]
    return d, coherence_violations(fwd, d, "tier2" if tier == "tier1" else tier)


def design(r):
    return (f"yield {r['yield_mj']:.0f} MJ, L {r['length_m']:.0f} m, "
            f"r {r['radius_m']:.2f} m, {r['fw_class']} wall, dd {r['dd_frac']:.2f}, "
            f"ceiling {r['max_f_rep']:.2f} Hz")


def sizing(d):
    return (f"n_mod {d['n_mod']}, f_rep {d['f_rep_hz']:.2f} Hz, "
            f"duty {d['tau_burn_implied_s'] * d['f_rep_hz']:.2f}"
            if "tau_burn_implied_s" in d else
            f"n_mod {d['n_mod']}, f_rep {d['f_rep_hz']:.2f} Hz, duty {d['duty']:.2f}")


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)
    all_rows = []
    model3 = build_model(load_config("baseline.yaml"))
    for tier in ("tier1", "tier2", "tier3"):
        rows = scan(tier)
        all_rows.extend(rows)
        ok = [r for r in rows if r["coherent"]]
        ok.sort(key=lambda r: r["lcoe"])
        print(f"\n== {tier}: {len(ok)} coherent of {len(rows)} scanned "
              f"(granted ceiling {rows[0]['granted_hz']:.0f} Hz) ==")
        header = (f"{'LCOE':>6} {'yield':>7} {'L':>5} {'r':>5} {'wall':>6} "
                  f"{'dd':>5} {'ceil':>6} {'n_mod':>5} {'f_rep':>6} {'duty':>5} "
                  f"{'avail':>6} {'q_wall':>6} {'flash':>6}")

        def line(r):
            return (f"{r['lcoe']:>6.1f} {r['yield_mj']:>7.1f} {r['length_m']:>5.0f} "
                    f"{r['radius_m']:>5.2f} {r['fw_class']:>6} {r['dd_frac']:>5.2f} "
                    f"{r['max_f_rep']:>6.2f} {r['n_mod']:>5} {r['f_rep_hz']:>6.2f} "
                    f"{r['duty']:>5.2f} {r['availability']:>6.3f} "
                    f"{r['q_wall_mw_m2']:>6.2f} {r['e_flash_mj_m2']:>6.2f}")

        print(header)
        for r in ok[:10]:
            print(line(r))

        # The mix trade with the rate priced: the best coherent design per
        # burn mix, and beside it the design the search would build at the
        # granted ceiling without the rate as a lever (the best coherent
        # at-grant design, or where none fits, the best that constraint 8
        # alone excludes), with the duty that excludes it.
        print(f"  best coherent design per burn mix, and the same mix at the "
              f"granted ceiling:")
        print("  " + header + f"   {'at grant':>10} {'n_mod':>5} {'f_rep':>6} {'duty':>5}")

        def duty_only(r):
            return all(v.startswith("duty") for v in r["violations"].split("; "))

        for b in BURN_BRANCHES:
            dd = b["dhe3_dd_frac"]
            mix_ok = [r for r in ok if r["dd_frac"] == dd]
            if not mix_ok:
                print(f"  dd {dd:.2f}: no coherent design")
                continue
            best = min(mix_ok, key=lambda r: r["lcoe"])
            at_grant = [r for r in rows if r["dd_frac"] == dd
                        and r["max_f_rep"] == round(r["granted_hz"], 4)
                        and (r["coherent"] or duty_only(r))]
            tail = ""
            if at_grant:
                c = min(at_grant, key=lambda r: (not r["coherent"], r["lcoe"]))
                tail = (f"   {c['lcoe']:>10.1f} {c['n_mod']:>5} {c['f_rep_hz']:>6.2f} "
                        f"{c['duty']:>5.2f}" + ("" if c["coherent"] else " excluded"))
            print("  " + line(best) + tail)

        if ok:
            # The module-count trade at the optimum's own shot, chamber and
            # mix: every rung of its rate ladder, so the writeup can say
            # what each added module costs against the slower bank's
            # longer life and higher availability.
            o = ok[0]
            same = [r for r in rows if all(r[k] == o[k] for k in
                    ("yield_mj", "length_m", "radius_m", "fw_class", "dd_frac"))]
            same.sort(key=lambda r: -r["max_f_rep"])
            print(f"  the rate ladder at the optimum's shot, chamber and mix "
                  f"(ceiling, n_mod, f_rep, duty, availability, LCOE):")
            print("    " + "; ".join(
                f"{r['max_f_rep']:.2f} Hz: {r['n_mod']} at {r['f_rep_hz']:.2f} Hz, "
                f"duty {r['duty']:.2f}, A {r['availability']:.3f}, {r['lcoe']:.1f}"
                + ("" if r["coherent"] else " (excluded)") for r in same))
            # The same designs sold as a 3 GWe park (same module, more of them).
            # Sizing snaps to an integer module count, so a design that is
            # coherent at 1 GWe can trip the wall audit at 3; take the best
            # design that stays coherent at the larger plant, and report
            # the 1 GWe optimum's own 3 GWe reading beside it.
            d3, v3 = at_plant_size(model3, tier, ok[0], 3000.0)
            print(f"  the 1 GWe optimum at 3 GWe: "
                  + (f"LCOE {d3['lcoe']:.1f}, {sizing(d3)}" if d3 else "")
                  + (f"; NOT coherent: {'; '.join(v3)}" if v3 else ""))
            best3 = None
            for cand in ok[:30]:
                d3, v3 = at_plant_size(model3, tier, cand, 3000.0)
                if d3 is None or v3:
                    continue
                if best3 is None or d3["lcoe"] < best3[1]["lcoe"]:
                    best3 = (cand, d3)
            if best3 is not None:
                cand, d3 = best3
                print(f"  best coherent at 3 GWe: LCOE {d3['lcoe']:.1f}, "
                      f"{design(cand)}, {sizing(d3)}")
        # The deuterium-rich branch: its best design under all eight
        # constraints (rate included), and the design it would be at the
        # granted ceiling in the fewest modules, which constraint 8 alone
        # excludes wherever the burn overruns that period.
        d_rich_ok = [r for r in ok if r["dd_frac"] == 0.85]
        if d_rich_ok:
            r = min(d_rich_ok, key=lambda r: r["lcoe"])
            print(f"  best deuterium-rich design under all eight constraints: "
                  f"LCOE {r['lcoe']:.1f}, {design(r)}, {sizing(r)}")
            d3, v3 = at_plant_size(model3, tier, r, 3000.0)
            if d3 is not None:
                print(f"    the same design at 3 GWe: LCOE {d3['lcoe']:.1f}, "
                      f"{sizing(d3)}" + (f" ({'; '.join(v3)})" if v3 else ""))
        d_rich_ceiling = [r for r in rows if r["dd_frac"] == 0.85 and not r["coherent"]
                          and r["max_f_rep"] == round(r["granted_hz"], 4)
                          and all(v.startswith("duty") for v in r["violations"].split("; "))]
        if d_rich_ceiling:
            r = min(d_rich_ceiling, key=lambda r: r["lcoe"])
            print(f"  best deuterium-rich design at the granted ceiling, excluded by "
                  f"constraint 8 alone: LCOE {r['lcoe']:.1f}, {design(r)}, "
                  f"{sizing(r)} ({r['violations']})")
    with open(OUTPUT_DIR / "coherent_min.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(all_rows[0]))
        w.writeheader()
        w.writerows(all_rows)
