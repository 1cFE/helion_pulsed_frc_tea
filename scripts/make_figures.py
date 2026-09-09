"""Paper figures for docs/writeup.md, computed live from the study machinery.

Outputs SVG (embedded in the writeup) and PNG (inspection) to docs/figures/.
Palette: dataviz reference categorical slots 1-3 (blue/orange/aqua) plus the
diverging red partner for negative tornado bars; light surface; validated.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from pathlib import Path  # noqa: E402

from study import apply_records, build_model, load_config, run  # noqa: E402
from tritium_burn import f_t_from_burnup  # noqa: E402

BLUE, ORANGE, AQUA, RED = "#2a78d6", "#eb6834", "#1baf7a", "#e34948"
INK, INK2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e5e4e0", "#fcfcfb"
FIGDIR = Path(__file__).resolve().parents[1] / "docs" / "figures"

TIER2_MIN = dict(chamber_length=10.0, plasma_t=1.5, r_bore=1.6, fw_class="panel")
TIER3_MIN = dict(yield_per_shot_mj=500.0, chamber_length=30.0, plasma_t=1.5,
                 r_bore=1.6, fw_class="panel")
TIERS = (("best_case.yaml",), ("best_case.yaml", "tier2.yaml"),
         ("best_case.yaml", "tier2.yaml", "tier3.yaml"))


def style(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.xaxis.label.set_color(INK2)
    ax.yaxis.label.set_color(INK2)
    ax.title.set_color(INK)


def save(fig, name):
    FIGDIR.mkdir(exist_ok=True)
    fig.patch.set_facecolor(SURFACE)
    for ext in ("svg", "png"):
        fig.savefig(FIGDIR / f"{name}.{ext}", dpi=180, bbox_inches="tight",
                    facecolor=SURFACE)
    plt.close(fig)
    print(f"wrote {name}")


def stack(cfg, *tier_cfgs, **over):
    fwd = dict(cfg["forward"])
    for c in tier_cfgs:
        apply_records(fwd, c)
    fwd.update(over)
    return fwd


def fig1_ladder(model, cfg):
    # One device per evidence grade: the records, extrapolation, and
    # speculation devices are their stacks' design-optimized machines;
    # Helion's requirements is the vendor configuration on the design basis.
    TIER1_MIN = dict(dhe3_dd_frac=0.85, f_rad=0.28, chamber_length=10.0,
                     plasma_t=1.0, r_bore=1.1, fw_class="panel")
    # The speculation design is power-dependent: the 500 MJ single-module
    # machine trips the wall audit at 3 GWe when the module count snaps, so
    # the 3 GWe bar uses the coherent 200 MJ design (coherent_min.py footer).
    TIER3_MIN_3GWE = dict(TIER3_MIN, yield_per_shot_mj=200.0)
    rows = [
        ("citable records", TIERS[0], TIER1_MIN, TIER1_MIN),
        ("Helion's requirements", (), {}, {}),
        ("extrapolations", TIERS[1], TIER2_MIN, TIER2_MIN),
        ("speculation", TIERS[2], TIER3_MIN, TIER3_MIN_3GWE),
    ]
    vals = {1000.0: [], 3000.0: []}
    for label, cfgs, over1, over3 in rows:
        for p, over in ((1000.0, over1), (3000.0, over3)):
            _, d = run(model, stack(cfg, *cfgs, net_electric_mw=p, **over))
            vals[p].append(d["lcoe"])
    labels = [r[0] for r in rows]
    y = np.arange(len(labels))[::-1]
    fig, ax = plt.subplots(figsize=(7.2, 2.9))
    h = 0.34
    b1 = ax.barh(y + h / 2 + 0.02, vals[1000.0], height=h, color=BLUE, label="1 GWe")
    b3 = ax.barh(y - h / 2 - 0.02, vals[3000.0], height=h, color=ORANGE, label="3 GWe")
    for bars in (b1, b3):
        for b in bars:
            ax.text(b.get_width() + 2, b.get_y() + b.get_height() / 2,
                    f"{b.get_width():.1f}", va="center", ha="left",
                    fontsize=8, color=INK)
    ax.set_yticks(y, labels)
    ax.set_xlabel("LCOE (\\$/MWh)")
    ax.set_xlim(0, max(vals[1000.0]) * 1.14)
    ax.legend(frameon=False, loc="lower right", labelcolor=INK)
    ax.set_axisbelow(True)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    style(ax)
    save(fig, "fig1_ladder")


def fig2_tornado(model, cfg):
    fwd = stack(cfg, *TIERS[1], **TIER2_MIN)
    _, d0 = run(model, fwd)
    tier1 = stack(cfg, *TIERS[0])
    rows = []
    for knob in load_config("tier2.yaml")["records"]:
        reverted = dict(fwd)
        if knob in tier1:
            reverted[knob] = tier1[knob]
        elif knob == "fw_class":
            reverted[knob] = "panel"
        else:
            reverted.pop(knob, None)
        if knob == "dhe3_dd_frac":
            reverted["f_rad"] = tier1["f_rad"]
        _, dd = run(model, reverted)
        rows.append((knob, dd["lcoe"] - d0["lcoe"]))
    rows.sort(key=lambda r: abs(r[1]))
    labels = [k for k, _ in rows]
    deltas = [v for _, v in rows]
    y = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    colors = [BLUE if v >= 0 else RED for v in deltas]
    bars = ax.barh(y, deltas, height=0.55, color=colors)
    for b, v in zip(bars, deltas):
        ax.text(v + (0.8 if v >= 0 else -0.8), b.get_y() + b.get_height() / 2,
                f"{v:+.1f}", va="center", ha="left" if v >= 0 else "right",
                fontsize=8, color=INK)
    ax.axvline(0, color=INK2, linewidth=1)
    ax.set_yticks(y, labels)
    ax.set_xlabel(f"change in LCOE when reverted to the record value "
                  f"(\\$/MWh, from the {d0['lcoe']:.1f} extrapolation device)")
    ax.set_xlim(min(deltas) - 6, max(deltas) + 7)
    ax.set_axisbelow(True)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    style(ax)
    save(fig, "fig2_tornado")


def fig3_burnup(model, cfg):
    bfs = np.array([1.2e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 0.15, 0.3])
    frs = [(0.99, "recovery 0.99"), (0.999, "0.999"), (0.9999, "0.9999")]
    fwd0 = stack(cfg, *TIERS[2], **TIER3_MIN)
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.2), sharey=True)
    for ax, (branch, title) in zip(
            axes, (("pr", "prompt triton loss"), ("th", "thermalized tritons"))):
        for (fr, lab), color in zip(frs, (BLUE, ORANGE, AQUA)):
            ys = []
            for bf in bfs:
                f_t = 0.0 if branch == "pr" else f_t_from_burnup(bf, 70.0)
                _, d = run(model, dict(
                    fwd0, burn_fraction=bf,
                    burn_fraction_he3=min(0.95, 3.324 * bf),
                    fuel_recovery=fr, dhe3_f_T=f_t))
                ys.append(d["lcoe"])
            ax.plot(bfs, ys, color=color, linewidth=2, marker="o",
                    markersize=4, label=lab)
        ax.axvline(1.2e-4, color=INK2, linewidth=1, linestyle=":")
        ax.text(0.045, 0.97, "patent basis", fontsize=8, color=INK2,
                transform=ax.transAxes, va="top")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_yticks([15, 20, 30, 50, 100, 150],
                      ["15", "20", "30", "50", "100", "150"])
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("per-pulse burn fraction")
        ax.set_axisbelow(True)
        ax.grid(color=GRID, linewidth=0.8)
        style(ax)
    axes[0].set_ylabel("LCOE (\\$/MWh)")
    leg = axes[1].legend(frameon=False, fontsize=8, labelcolor=INK,
                         title="per-pulse fuel recovery", title_fontsize=8,
                         loc="center right")
    leg.get_title().set_color(INK2)
    save(fig, "fig4_burnup")


def fig4_anatomy(model, cfg):
    r, d = run(model, stack(cfg, *TIERS[2], **TIER3_MIN))
    d22 = {k: float(v) for k, v in r.cas22_detail.items()}
    c = r.costs
    items = [
        ("buildings (CAS21)", float(c.cas21)),
        ("fuel handling + tritium plant (C220500)", d22["C220500"]),
        ("CAS50 incl. decommissioning provision", float(c.cas50)),
        ("heat rejection + electrical plant (CAS24-26)",
         float(c.cas24) + float(c.cas25) + float(c.cas26)),
        ("vacuum + per-pulse exhaust pumping (C220106)", d22["C220106"]),
        ("first wall, 30 m chamber (C220101)", d22["C220101"]),
        ("DEC power electronics (C220109)", d22["C220109"]),
        ("driver capacitor bank (C220107)", d22["C220107"]),
    ]
    items.sort(key=lambda kv: kv[1])
    labels = [k for k, _ in items]
    vals = [v for _, v in items]
    y = np.arange(len(items))
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    bars = ax.barh(y, vals, height=0.55, color=BLUE)
    for b, v in zip(bars, vals):
        ax.text(v + 3, b.get_y() + b.get_height() / 2, f"{v:.0f}",
                va="center", ha="left", fontsize=8, color=INK)
    ax.set_yticks(y, labels)
    ax.set_xlabel("capital at the speculation device (M\\$, 1 GWe plant)")
    ax.set_xlim(0, max(vals) * 1.12)
    ax.set_axisbelow(True)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    style(ax)
    save(fig, "fig3_anatomy")


def fig5_plant_size(model, cfg):
    fwd0 = stack(cfg, *TIERS[2], **TIER3_MIN)
    sizes = (50.0, 100.0, 250.0, 500.0, 1000.0)

    def scaled(module_mwe, plant_mwe):
        s = module_mwe / 1000.0
        return dict(fwd0, net_electric_mw=plant_mwe,
                    yield_per_shot_mj=300.0 * s, e_driver_mj=50.0 * s,
                    chamber_length=max(60.0 * s, 3.0), plasma_t=0.75,
                    r_bore=0.85, fw_class="panel")

    stand, park = [], []
    for m in sizes:
        _, d = run(model, scaled(m, m))
        stand.append(d["lcoe"])
        _, d = run(model, scaled(m, 1000.0))
        park.append(d["lcoe"])
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.plot(sizes, stand, color=ORANGE, linewidth=2, marker="o",
            markersize=5, label="standalone plant of one module")
    ax.plot(sizes, park, color=BLUE, linewidth=2, marker="o",
            markersize=5, label="same module in a 1 GWe park")
    ax.text(sizes[0], stand[0] + 2, f"{stand[0]:.1f}", fontsize=8, color=INK)
    ax.text(sizes[0], park[0] - 5, f"{park[0]:.1f}", fontsize=8, color=INK)
    ax.set_xscale("log")
    ax.set_xticks(sizes, [f"{s:.0f}" for s in sizes])
    ax.set_xlabel("module size (MWe)")
    ax.set_ylabel("LCOE (\\$/MWh)")
    ax.legend(frameon=False, fontsize=9, labelcolor=INK)
    ax.set_axisbelow(True)
    ax.grid(color=GRID, linewidth=0.8)
    style(ax)
    save(fig, "fig5_plant_size")


if __name__ == "__main__":
    cfg = load_config("baseline.yaml")
    model = build_model(cfg)
    fig1_ladder(model, cfg)
    fig2_tornado(model, cfg)
    fig3_burnup(model, cfg)
    fig4_anatomy(model, cfg)
    fig5_plant_size(model, cfg)
