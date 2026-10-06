"""Constrained minimum-LCOE hunt: the study's answer to "how low can this go".

Instead of asserting a speculative operating point (the earlier draft's
Q = 40 in a chamber that flash-melts at that yield), this scan searches the
design space the machine actually controls - compression field, driver
bank, shot gain, chamber size, wall class, burn mix, and firing rate -
under the red-team coherence constraints (study.py): bremsstrahlung-
consistent f_rad, composite recovery cap, steady wall flux within the
bought wall class, per-shot flash energy under tungsten melt, tritium
plant charged whenever the mix is D-rich, the shot's implied burn (at the
point's own mix and field) fitting inside the pulse period at the solved
rep rate (constraint 8), and the coil's magnetic pressure within the
grade's coil bound (constraint 9).

The compression field and the driver bank are scanned, graded by the
evidence ladder. The patent's 22 T burn point and Polaris's sourced 50 MJ
bank are the design basis; no record exists above either. The records
grade holds both. The extrapolation grade holds the field at the basis
and lets the bank double: a bank is a count of modular capacitor units,
so a larger one is procurement rather than technology. Speculation scans
the field to 50 T and the bank to four times Polaris, but the coil bound
(constraint 9) is the same at every grade: the basis coil already cycles
at or above the copper-alloy gigacycle band and no higher fatigue basis
is sourced anywhere in this work, so every point above 22 T is excluded
from the devices at every grade and reported as a sensitivity, what a
higher field would be worth on a coil this work cannot price. The burn
point moves with the field: at beta = 1 the density scales as B^2, so
the breakeven time and the implied burn fall as B^-2, the per-pulse
burnup rises as B^2, and the compressed flux volume that caps f_pdv
shrinks as B^-2 and grows with the bank, so the two knobs are coupled
through the chamber rather than scanned as if independent. The bank's
shot keeps the gain: the records and extrapolation grades hold the
design-basis gain (2.56), so the burn the shot implies is unchanged by
the bank and the duty falls with the module power per shot; speculation
frees the gain.

The firing rate is a design choice, not a grant. costingfe sizes a plant by
bisecting f_rep against the per-module net target and solving the integer
module count off the max_f_rep ceiling, so every design it builds fires
just under its ceiling in the fewest modules the ceiling permits. A grade's
granted ceiling (1 Hz at the design basis and records, 3 Hz at
extrapolations, 10 Hz at speculation) is permission, not obligation: the
same plant power can be delivered slower in more modules, which is how a
power-sparse burn mix satisfies constraint 8. The scan therefore evaluates
each point at a ladder of effective ceilings at and below min(granted
ceiling, 1 / implied burn), the top of which is the highest coherent rate,
and never above the grant. Cost is not monotone in the module count (more
modules buy more hardware; a slower bank is replaced fewer times over the
book life and the derived availability rises with it), so the ladder is
priced rather than shortcut to the fewest feasible modules.

The chamber is resized honestly: the coil bore tracks the plasma radius
(r_bore = plasma_t + gap), and the cylinder wall, vessel, and structure are
repriced by the model at the scanned size.
"""
import csv
import itertools
import multiprocessing

from costingfe.model import SizingInfeasible

from study import (
    B_COMPRESSION_T,
    COIL_PRESSURE_BASIS_MPA,
    E_DEL_BASIS_MJ,
    E_FLASH_MELT_MJ_M2,
    GAIN_BASIS,
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
# The compression field and the driver bank, graded (see the module
# docstring): the basis at records; the basis field with a doubled bank at
# extrapolations; the bank to 200 MJ at speculation, where the field is
# scanned to 50 T as a priced sensitivity that the coil bound excludes
# from the device at every grade.
FIELDS_T = {"tier1": (B_COMPRESSION_T,), "tier2": (B_COMPRESSION_T,),
            "tier3": (B_COMPRESSION_T, 30.0, 40.0, 50.0)}
BANKS_MJ = {"tier1": (E_DEL_BASIS_MJ,), "tier2": (E_DEL_BASIS_MJ, 100.0),
            "tier3": (E_DEL_BASIS_MJ, 100.0, 200.0)}
# The shot as a gain on the bank: the design-basis gain alone at the
# records and extrapolation grades; at speculation the gain is free (gain
# speculation), on the sourced bank the same 128 to 2000 MJ shots as a
# yield grid, and it must still be survivable in the chamber it is costed
# in.
GAINS = {"tier1": (GAIN_BASIS,), "tier2": (GAIN_BASIS,),
         "tier3": (GAIN_BASIS, 3.0, 4.0, 6.0, 10.0, 15.0, 20.0, 30.0, 40.0)}
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


def point_fwd(fwd0, y, length, radius, fw, branch, max_f_rep=None,
              b_center=B_COMPRESSION_T, e_driver_mj=E_DEL_BASIS_MJ) -> dict:
    """A scan point: the shot (yield y on the bank e_driver_mj at the
    compression field b_center), the chamber, the wall class, the burn
    mix, and optionally the rate ceiling."""
    fwd = dict(fwd0, **branch)
    fwd["yield_per_shot_mj"] = y
    fwd["e_driver_mj"] = e_driver_mj
    fwd["b_center"] = b_center
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
    burn), the burn read at the reference x_s and the point's own mix,
    field and bank as study.run reports it; and, where the burn overruns
    the granted period, the grant itself first, so the design the search
    would build without the rate as a lever is priced beside the ones
    that fit. Never above the grant."""
    granted = granted_ceiling_hz(fwd, model)
    e_del = float(fwd.get("e_driver_mj", model._eng_defaults["e_driver_mj"]))
    top = min(granted, duty_bound_rate_hz(fwd, e_del))
    ladder = [top * s for s in RATE_STEPS]
    if top < granted:
        ladder.insert(0, granted)
    return ladder


def rate_designs(model, fwd: dict) -> list[tuple[dict, dict]]:
    """The distinct designs a point yields down its rate ladder: (fwd with
    the ceiling set, diagnostics) per binding step. A ceiling the previous
    design's solved rate already clears changes nothing, so the design is
    carried under that lower ceiling (the tightest one it fits, which is
    the ceiling that keeps it coherent when the integer module count
    re-snaps at another plant power); an infeasible sizing (net <= 0 at
    the ceiling) ends the ladder, since every lower ceiling is infeasible
    too; and a per-shot flash the wall cannot survive ends it as well,
    since the flash is a property of the shot in its chamber, not of the
    rate."""
    designs = []
    for ceiling in rate_ceilings_hz(fwd, model):
        if designs and designs[-1][1]["f_rep_hz"] <= ceiling * (1 + 1e-9):
            designs[-1][0]["max_f_rep"] = ceiling
            continue
        f = dict(fwd, max_f_rep=ceiling)
        try:
            _, diag = run(model, f)
        except SizingInfeasible:
            break
        designs.append((f, diag))
        if diag["e_flash_mj_m2"] > E_FLASH_MELT_MJ_M2:
            break
    return designs


def scan_grid(tier: str, fields=None, banks=None, gains=None, lengths=None,
              radii=None, walls=None):
    """The (field, bank, gain, length, radius, wall, mix) points of a
    grade's scan, the grade's graded ranges unless narrowed."""
    return list(itertools.product(
        fields or FIELDS_T[tier], banks or BANKS_MJ[tier],
        gains or GAINS[tier], lengths or LENGTHS_M, radii or RADII_M,
        walls or FW_CLASSES, BURN_BRANCHES))


def point_rows(model, tier, fwd0, point, overrides=None):
    """Every design a scan point yields down its rate ladder, as rows."""
    b_t, e_del, gain, length, radius, fw, branch = point
    y = gain * e_del
    fwd = point_fwd(fwd0, y, length, radius, fw, branch, b_center=b_t,
                    e_driver_mj=e_del)
    if overrides:
        fwd.update(overrides)
    # tier-1 coherence uses the tier-2 cap set (no tier-1-specific caps exist)
    check_tier = "tier2" if tier == "tier1" else tier
    granted = granted_ceiling_hz(fwd0, model)
    rows = []
    for f, diag in rate_designs(model, fwd):
        violations = coherence_violations(f, diag, check_tier)
        rows.append(dict(
            tier=tier,
            field_t=b_t,
            bank_mj=e_del,
            gain=round(gain, 3),
            yield_mj=round(y, 1),
            length_m=length,
            radius_m=radius,
            fw_class=fw,
            dd_frac=branch["dhe3_dd_frac"],
            granted_hz=granted,
            max_f_rep=round(f["max_f_rep"], 4),
            lcoe=diag["lcoe"],
            n_mod=diag["n_mod"],
            f_rep_hz=round(diag["f_rep_hz"], 3),
            duty=round(diag["tau_burn_implied_s"] * diag["f_rep_hz"], 3),
            tau_burn_s=round(diag["tau_burn_implied_s"], 3),
            p_fus_module_mw=round(diag["p_fus_module_mw"], 1),
            availability=round(diag["availability"], 4),
            q_wall_mw_m2=round(diag["q_wall_mw_m2"], 2),
            e_flash_mj_m2=round(diag["e_flash_mj_m2"], 3),
            f_pdv_cap=round(diag["f_pdv_cap"], 3),
            coil_pressure_mpa=round(diag["coil_pressure_mpa"], 1),
            coil_past_basis=diag["coil_pressure_mpa"] > COIL_PRESSURE_BASIS_MPA * (1 + 1e-9),
            capital_per_kw=round(diag["capital_per_kw"]),
            coherent=(not violations),
            violations="; ".join(violations),
        ))
    return rows


_WORKER = {}


def _init_worker(tier, overrides):
    _WORKER["model"] = build_model(load_config("baseline.yaml"))
    _WORKER["tier"] = tier
    _WORKER["fwd0"] = tier_fwd(tier)
    _WORKER["overrides"] = overrides


def _worker_rows(point):
    return point_rows(_WORKER["model"], _WORKER["tier"], _WORKER["fwd0"],
                      point, _WORKER["overrides"])


def scan(tier: str, overrides=None, processes=None, **grid):
    """Every design of a grade's scan (point_rows over scan_grid), in
    parallel; `overrides` are forward entries applied to every point (the
    He-3 price re-runs of scripts/he3_scan.py use it)."""
    points = scan_grid(tier, **grid)
    ctx = multiprocessing.get_context("spawn")  # JAX is loaded: no fork
    with ctx.Pool(processes, initializer=_init_worker, initargs=(tier, overrides)) as pool:
        chunks = pool.map(_worker_rows, points, chunksize=8)
    return [r for rows in chunks for r in rows]


def row_fwd(tier, r, net_electric_mw=1000.0, overrides=None):
    """The forward dict of a scan row at a plant power: same shot, field,
    bank, chamber, mix and ceiling."""
    branch = next(b for b in BURN_BRANCHES if b["dhe3_dd_frac"] == r["dd_frac"])
    fwd = point_fwd(tier_fwd(tier), r["gain"] * r["bank_mj"], r["length_m"],
                    r["radius_m"], r["fw_class"], branch, r["max_f_rep"],
                    b_center=r["field_t"], e_driver_mj=r["bank_mj"])
    if overrides:
        fwd.update(overrides)
    fwd["net_electric_mw"] = net_electric_mw
    return fwd


def at_plant_size(model, tier, r, net_electric_mw, overrides=None):
    """A scan row's design re-sized to another plant power, same shot,
    chamber, mix and ceiling (the integer module count re-snaps)."""
    fwd = row_fwd(tier, r, net_electric_mw, overrides)
    try:
        _, d = run(model, fwd)
    except SizingInfeasible:
        return None, ["sizing infeasible"]
    return d, coherence_violations(fwd, d, "tier2" if tier == "tier1" else tier)


def design(r):
    return (f"{r['field_t']:.0f} T, {r['bank_mj']:.0f} MJ bank, yield "
            f"{r['yield_mj']:.0f} MJ, L {r['length_m']:.0f} m, "
            f"r {r['radius_m']:.2f} m, {r['fw_class']} wall, dd {r['dd_frac']:.2f}, "
            f"ceiling {r['max_f_rep']:.2f} Hz")


def sizing(d):
    return (f"n_mod {d['n_mod']}, f_rep {d['f_rep_hz']:.2f} Hz, "
            f"duty {d['tau_burn_implied_s'] * d['f_rep_hz']:.2f}"
            if "tau_burn_implied_s" in d else
            f"n_mod {d['n_mod']}, f_rep {d['f_rep_hz']:.2f} Hz, duty {d['duty']:.2f}")


HEADER = (f"{'LCOE':>6} {'B':>4} {'bank':>5} {'yield':>7} {'L':>5} {'r':>5} "
          f"{'wall':>6} {'dd':>5} {'ceil':>6} {'n_mod':>5} {'f_rep':>6} "
          f"{'duty':>5} {'avail':>6} {'q_wall':>6} {'flash':>6} {'coil':>6}")


def line(r):
    return (f"{r['lcoe']:>6.1f} {r['field_t']:>4.0f} {r['bank_mj']:>5.0f} "
            f"{r['yield_mj']:>7.1f} {r['length_m']:>5.0f} "
            f"{r['radius_m']:>5.2f} {r['fw_class']:>6} {r['dd_frac']:>5.2f} "
            f"{r['max_f_rep']:>6.2f} {r['n_mod']:>5} {r['f_rep_hz']:>6.2f} "
            f"{r['duty']:>5.2f} {r['availability']:>6.3f} "
            f"{r['q_wall_mw_m2']:>6.2f} {r['e_flash_mj_m2']:>6.2f} "
            f"{r['coil_pressure_mpa']:>6.0f}" + ("*" if r["coil_past_basis"] else " "))


def duty_only(r):
    return all(v.startswith("duty") for v in r["violations"].split("; "))


def coil_only(r):
    """A design the coil bound (constraint 9) alone excludes: coherent in
    every other respect, resting on a coil this work cannot price."""
    return bool(r["violations"]) and all(
        v.startswith("coil pressure") for v in r["violations"].split("; "))


def report(tier, rows, model3):
    ok = [r for r in rows if r["coherent"]]
    ok.sort(key=lambda r: r["lcoe"])
    print(f"\n== {tier}: {len(ok)} coherent of {len(rows)} scanned "
          f"(granted ceiling {rows[0]['granted_hz']:.0f} Hz; fields "
          f"{'/'.join(f'{b:.0f}' for b in FIELDS_T[tier])} T, banks "
          f"{'/'.join(f'{e:.0f}' for e in BANKS_MJ[tier])} MJ; * = coil past "
          f"the {COIL_PRESSURE_BASIS_MPA:.0f} MPa basis, excluded by "
          f"constraint 9 at every grade) ==")
    print(HEADER)
    for r in ok[:10]:
        print(line(r))

    # The field and the bank priced one at a time: the best coherent
    # design at each bank (all fields), and at each field the best design
    # the coil bound alone excludes (a sensitivity, not a device: what a
    # higher field would be worth on a coil this work cannot price), so
    # the writeup can say what scaling each is worth at this grade.
    sens = [r for r in rows if coil_only(r)]
    if len(FIELDS_T[tier]) > 1:
        print("  best design per compression field (above the basis: the "
              "best the coil bound alone excludes, a sensitivity):")
        print("  " + HEADER)
        for b_t in FIELDS_T[tier]:
            pool = ok if b_t == B_COMPRESSION_T else sens
            at = [r for r in pool if r["field_t"] == b_t]
            print("  " + (line(min(at, key=lambda r: r["lcoe"])) if at
                          else f"{b_t:.0f} T: no design"))
    if len(BANKS_MJ[tier]) > 1:
        print("  best coherent design per driver bank:")
        print("  " + HEADER)
        for e in BANKS_MJ[tier]:
            at = [r for r in ok if r["bank_mj"] == e]
            print("  " + (line(min(at, key=lambda r: r["lcoe"])) if at
                          else f"{e:.0f} MJ: no coherent design"))
        if len(FIELDS_T[tier]) > 1:
            print("  best design per (field, bank), the fields above the "
                  "basis coil-excluded:")
            print("  " + HEADER)
            for b_t, e in itertools.product(FIELDS_T[tier], BANKS_MJ[tier]):
                pool = ok if b_t == B_COMPRESSION_T else sens
                at = [r for r in pool if r["field_t"] == b_t and r["bank_mj"] == e]
                if at:
                    print("  " + line(min(at, key=lambda r: r["lcoe"])))

    # The mix trade with the rate priced: the best coherent design per
    # burn mix, and beside it the design the search would build at the
    # granted ceiling without the rate as a lever (the best coherent
    # at-grant design, or where none fits, the best that constraint 8
    # alone excludes), with the duty that excludes it.
    print("  best coherent design per burn mix, and the same mix at the "
          "granted ceiling:")
    print("  " + HEADER + f"   {'at grant':>10} {'n_mod':>5} {'f_rep':>6} {'duty':>5}")
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
        keys = ("field_t", "bank_mj", "gain", "length_m", "radius_m", "fw_class", "dd_frac")
        same = [r for r in rows if all(r[k] == o[k] for k in keys)]
        same.sort(key=lambda r: -r["max_f_rep"])
        print("  the rate ladder at the optimum's shot, chamber and mix "
              "(ceiling, n_mod, f_rep, duty, availability, LCOE):")
        print("    " + "; ".join(
            f"{r['max_f_rep']:.2f} Hz: {r['n_mod']} at {r['f_rep_hz']:.2f} Hz, "
            f"duty {r['duty']:.2f}, A {r['availability']:.3f}, {r['lcoe']:.1f}"
            + ("" if r["coherent"] else " (excluded)") for r in same))
        # The same designs sold as a 3 GWe park (same module, more of them).
        # Sizing snaps to an integer module count, so a design that is
        # coherent at 1 GWe can trip the wall audit at 3; take the best
        # design that stays coherent at the larger plant, and report
        # the 1 GWe optimum's own 3 GWe reading beside it.
        d3_opt, v3 = at_plant_size(model3, tier, ok[0], 3000.0)
        print("  the 1 GWe optimum at 3 GWe: "
              + (f"LCOE {d3_opt['lcoe']:.1f}, {sizing(d3_opt)}" if d3_opt else "")
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
        if o["bank_mj"] > E_DEL_BASIS_MJ:
            # What the scanned bank is worth at this grade: the best
            # coherent design with it held at the sourced Polaris bank.
            held = [r for r in ok if r["bank_mj"] == E_DEL_BASIS_MJ]
            if held:
                h = min(held, key=lambda r: r["lcoe"])
                d3, v3 = at_plant_size(model3, tier, h, 3000.0)
                print(f"  bank held at the basis: LCOE {h['lcoe']:.1f} (+{h['lcoe'] - o['lcoe']:.1f}), "
                      f"{design(h)}, {sizing(h)}"
                      + (f"; at 3 GWe {d3['lcoe']:.1f}, {sizing(d3)}" if d3 and not v3 else ""))
        if len(FIELDS_T[tier]) > 1:
            # What a field above the basis would be worth at this grade,
            # on a coil this work cannot price: the best design at each
            # scanned field that the coil bound alone excludes, against
            # the coherent optimum, at both plant sizes. A sensitivity,
            # not a device.
            print("  the field above the basis, excluded from every device "
                  "by the coil bound (constraint 9), as a sensitivity:")
            for b_t in FIELDS_T[tier]:
                if b_t == B_COMPRESSION_T:
                    continue
                at = [r for r in sens if r["field_t"] == b_t]
                if not at:
                    print(f"    {b_t:.0f} T: no design the coil bound alone excludes")
                    continue
                h = min(at, key=lambda r: r["lcoe"])
                d3, v3 = at_plant_size(model3, tier, h, 3000.0)
                worth3 = (f"; at 3 GWe {d3['lcoe']:.1f} ({d3['lcoe'] - d3_opt['lcoe']:+.1f}), {sizing(d3)}"
                          if d3 and d3_opt and all(v.startswith("coil pressure") for v in v3)
                          else "")
                print(f"    {b_t:.0f} T: LCOE {h['lcoe']:.1f} ({h['lcoe'] - o['lcoe']:+.1f}), "
                      f"{design(h)}, {sizing(h)}, coil {h['coil_pressure_mpa']:.0f} MPa"
                      + worth3)
    # The deuterium-rich branch: its best design under all nine
    # constraints (rate included), and the design it would be at the
    # granted ceiling in the fewest modules, which constraint 8 alone
    # excludes wherever the burn overruns that period.
    d_rich_ok = [r for r in ok if r["dd_frac"] == 0.85]
    if d_rich_ok:
        r = min(d_rich_ok, key=lambda r: r["lcoe"])
        print(f"  best deuterium-rich design under all nine constraints: "
              f"LCOE {r['lcoe']:.1f}, {design(r)}, {sizing(r)}")
        d3, v3 = at_plant_size(model3, tier, r, 3000.0)
        if d3 is not None:
            print(f"    the same design at 3 GWe: LCOE {d3['lcoe']:.1f}, "
                  f"{sizing(d3)}" + (f" ({'; '.join(v3)})" if v3 else ""))
    d_rich_ceiling = [r for r in rows if r["dd_frac"] == 0.85 and not r["coherent"]
                      and r["max_f_rep"] == round(r["granted_hz"], 4)
                      and duty_only(r)]
    if d_rich_ceiling:
        r = min(d_rich_ceiling, key=lambda r: r["lcoe"])
        print(f"  best deuterium-rich design at the granted ceiling, excluded by "
              f"constraint 8 alone: LCOE {r['lcoe']:.1f}, {design(r)}, "
              f"{sizing(r)} ({r['violations']})")
    return ok


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)
    all_rows = []
    model3 = build_model(load_config("baseline.yaml"))
    for tier in ("tier1", "tier2", "tier3"):
        rows = scan(tier)
        all_rows.extend(rows)
        report(tier, rows, model3)
    with open(OUTPUT_DIR / "coherent_min.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(all_rows[0]))
        w.writeheader()
        w.writerows(all_rows)
