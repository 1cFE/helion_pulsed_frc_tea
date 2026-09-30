"""Paper figures for docs/Helion_writeup.md, computed live from the study machinery.

Outputs SVG (embedded in the writeup) and PNG (inspection) to docs/figures/.
Palette: dataviz reference categorical slots 1-3 (blue/orange/aqua) plus the
diverging red partner for negative tornado bars; light surface; validated.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from pathlib import Path  # noqa: E402

from study import (  # noqa: E402
    DEVICES,
    DEVICE_ORDER,
    N_D_PATENT_M3,
    PLANT_SIZES_MWE,
    VENDOR_PULSE_S,
    apply_records,
    build_model,
    device_fwd,
    lcoe_segments,
    load_config,
    run,
)
from tritium_burn import (  # noqa: E402
    PATENT_CONFINEMENT_S,
    f_t_from_burnup,
    in_pulse_burn_vs_dwell,
)
from yield_bound import bound_table  # noqa: E402

BLUE, ORANGE, AQUA, RED, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#e34948", "#a6a5a1"
INK, INK2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e5e4e0", "#fcfcfb"
FIGDIR = Path(__file__).resolve().parents[1] / "docs" / "figures"

TIERS = (("best_case.yaml",), ("best_case.yaml", "tier2.yaml"),
         ("best_case.yaml", "tier2.yaml", "tier3.yaml"))
TIER2_MIN = DEVICES["extrap"]["overrides"]
TIER3_MIN = DEVICES["spec"]["overrides"]


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


SEGMENTS = (
    ("straight_line", BLUE, "overnight cost recovered straight-line over the book life"),
    ("cost_of_money", ORANGE, "cost of money: interest during construction and on the capital"),
    ("operating", GREY, "O&M, fuel and scheduled replacement"),
)


def fig1_ladder(model, cfg):
    # One device per evidence grade, each bar split into the three parts of
    # its LCOE (study.lcoe_segments), so the financing part of each rung is
    # visible against its physics and engineering.
    rows = []
    for name, label in DEVICE_ORDER:
        for p in PLANT_SIZES_MWE:
            _, fwd = device_fwd(name, p)
            r, d = run(model, fwd)
            rows.append((label, p, d["lcoe"], lcoe_segments(r)))
    labels = [label for _, label in DEVICE_ORDER]
    y_dev = np.arange(len(labels))[::-1]
    fig, ax = plt.subplots(figsize=(7.6, 3.4))
    h = 0.34
    for i, (label, p, lcoe, seg) in enumerate(rows):
        offset = h / 2 + 0.02 if p == PLANT_SIZES_MWE[0] else -(h / 2 + 0.02)
        yy = y_dev[i // len(PLANT_SIZES_MWE)] + offset
        left = 0.0
        for key, color, legend in SEGMENTS:
            ax.barh(yy, seg[key], left=left, height=h, color=color,
                    edgecolor=SURFACE, linewidth=1.2,
                    label=legend if i == 0 else None)
            left += seg[key]
        ax.text(left + 2, yy, f"{lcoe:.1f}   {p / 1000:.0f} GWe",
                va="center", ha="left", fontsize=8, color=INK)
    ax.set_yticks(y_dev, labels)
    ax.set_xlabel("LCOE (\\$/MWh)")
    ax.set_xlim(0, max(r[2] for r in rows) * 1.24)
    ax.legend(frameon=False, loc="lower right", fontsize=7.5, labelcolor=INK)
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
    labels = [f"{k} (financing)" if k == "interest_rate" else k for k, _ in rows]
    deltas = [v for _, v in rows]
    y = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    colors = [GREY if k == "interest_rate" else (BLUE if v >= 0 else RED)
              for k, v in rows]
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


def fig_tritium_burn(model, cfg):
    """The burnup closure against burn time at the patent point: what the
    store-and-decay basis assumes (Helion's stated pulse) against what the
    granted shot needs (constraint 7)."""
    taus = np.logspace(-4, np.log10(3.0), 240)
    f_d, f_t = in_pulse_burn_vs_dwell(taus, N_D_PATENT_M3, 70.0)
    rows = bound_table()
    def span(device):
        r = [x for x in rows if x["device"] == device]
        return (min(x["tau_burn_s"] for x in r), max(x["tau_burn_s"] for x in r),
                r[0]["yield_mj"])
    helion, spec = span("helion"), span("spec")
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    bands = [((1e-4, VENDOR_PULSE_S), "Helion's stated pulse", GREY),
             (PATENT_CONFINEMENT_S, "patent confinement", GREY),
             (helion[:2], f"{helion[2]:.0f} MJ shot", ORANGE),
             (spec[:2], f"{spec[2]:.0f} MJ shot", ORANGE)]
    for (lo, hi), label, color in bands:
        ax.axvspan(lo, hi, color=color, alpha=0.18, linewidth=0)
        ax.text(np.sqrt(lo * hi), 2.2e-5, label, rotation=90, fontsize=7.5,
                color=INK2, ha="center", va="bottom")
    ax.plot(taus, f_t, color=BLUE, linewidth=2,
            label="bred tritium, thermalized limit")
    ax.plot(taus, f_d, color=ORANGE, linewidth=2, linestyle="--",
            label="deuterium")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e-4, 3.0)
    ax.set_ylim(1e-5, 1.0)
    ax.set_yticks([1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0],
                  ["0.001%", "0.01%", "0.1%", "1%", "10%", "100%"])
    ax.set_xlabel("burn time at the patent point (s)")
    ax.set_ylabel("fraction burned in the pulse")
    ax.set_axisbelow(True)
    ax.grid(color=GRID, linewidth=0.8)
    style(ax)
    leg = ax.legend(frameon=False, fontsize=8, labelcolor=INK, loc="upper left")
    save(fig, "fig4_tritium_burn")


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
        ax.set_ylim(0, 30)
        ax.set_yticks([0, 5, 10, 15, 20, 25, 30])
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("per-pulse burn fraction")
        ax.set_axisbelow(True)
        ax.grid(color=GRID, linewidth=0.8)
        style(ax)
    axes[0].set_ylabel("LCOE (\\$/MWh)")
    leg = axes[1].legend(frameon=False, fontsize=8, labelcolor=INK,
                         title="per-pulse fuel recovery", title_fontsize=8,
                         loc="upper right")
    leg.get_title().set_color(INK2)
    save(fig, "fig5_burnup")


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
        (f"first wall, {TIER3_MIN['chamber_length']:.0f} m chamber (C220101)",
         d22["C220101"]),
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


if __name__ == "__main__":
    cfg = load_config("baseline.yaml")
    model = build_model(cfg)
    fig1_ladder(model, cfg)
    fig2_tornado(model, cfg)
    fig_tritium_burn(model, cfg)
    fig3_burnup(model, cfg)
    fig4_anatomy(model, cfg)
