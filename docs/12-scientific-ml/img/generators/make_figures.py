"""Generate the figures for the Scientific ML / PINNs chapter.

These are OUR OWN remakes (never screenshots of lecture slides or the paper).
Two of them read the final project's committed result CSVs (copied, and the loss
curves downsampled, into ../../notebooks/data/) and replot them in the book's
dataviz style; the architecture schematic is illustrative/synthetic.

Styling follows the repo's dataviz skill and matches the Linear Algebra chapter:
a validated categorical palette, thin recessive grid/axes, direct labels, a
legend only for >=2 series.

Run:  python3 docs/12-scientific-ml/img/generators/make_figures.py
Output PNGs land in docs/12-scientific-ml/img/ at dpi 110.
"""
import csv
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch

# ---- dataviz palette (validated categorical slots + chrome) -----------------
BLUE, YELLOW, GREEN, MAGENTA = "#2a78d6", "#eda100", "#008300", "#e87ba4"
ORANGE, VIOLET, RED = "#eb6834", "#4a3aa7", "#e34948"
SURFACE, INK, SECOND, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 11, "axes.titlesize": 12, "axes.labelsize": 11,
    "text.color": INK, "axes.labelcolor": INK, "axes.titlecolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.edgecolor": "#c3c2b7", "axes.linewidth": 0.8,
    "grid.color": GRID, "grid.linewidth": 0.8,
    "legend.frameon": False, "figure.dpi": 110, "savefig.dpi": 110,
})

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..")
DATA = os.path.join(HERE, "..", "..", "notebooks", "data")

# Optimizer identity -> fixed categorical hue (never cycled).
OPT_ORDER = ["L-BFGS", "Learnable", "SSBFGS", "SSBroyden2"]
OPT_COLOR = {"L-BFGS": BLUE, "Learnable": YELLOW, "SSBFGS": GREEN, "SSBroyden2": MAGENTA}
PDE_ORDER = ["Burgers", "Helmholtz", "Allen-Cahn", "Kuramoto-Sivashinsky"]
PDE_SHORT = {"Burgers": "Burgers", "Helmholtz": "Helmholtz",
             "Allen-Cahn": "Allen–Cahn", "Kuramoto-Sivashinsky": "Kuramoto–\nSivashinsky"}


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"  {name}: {os.path.getsize(p)//1024} KB")


def clean(ax, grid=True, axis="y"):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if grid:
        ax.grid(True, axis=axis, alpha=0.6)
    ax.set_axisbelow(True)


# 1. PINN architecture + loss-composition schematic (illustrative) -----------
def fig_architecture():
    fig, ax = plt.subplots(figsize=(9.2, 5.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    def node(x, y, r=0.16, c=BLUE):
        ax.add_patch(Circle((x, y), r, facecolor=c, edgecolor="white", lw=1.0, zorder=3))

    def box(x, y, w, h, text, fc, tc=INK, fs=10):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                     boxstyle="round,pad=0.02,rounding_size=0.08",
                     facecolor=fc, edgecolor="#c3c2b7", lw=0.8, zorder=2))
        ax.text(x, y, text, ha="center", va="center", color=tc, fontsize=fs, zorder=4)

    def arrow(x1, y1, x2, y2, c=MUTED, style="-|>", lw=1.4, ls="-"):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                     mutation_scale=12, color=c, lw=lw, linestyle=ls, zorder=1))

    # inputs
    node(0.7, 4.3, c=SECOND)
    node(0.7, 3.3, c=SECOND)
    ax.text(0.32, 4.3, r"$x$", ha="center", va="center", fontsize=13)
    ax.text(0.32, 3.3, r"$t$", ha="center", va="center", fontsize=13)

    # hidden layers (a small tanh MLP)
    layer_x = [2.1, 3.2, 4.3]
    ys = [2.7, 3.35, 4.0, 4.65]
    for lx in layer_x:
        for y in ys:
            node(lx, y, c=BLUE)
    # connections (thin, faint) input -> L1 -> L2 -> L3
    cols = [[(0.7, 4.3), (0.7, 3.3)]] + [[(lx, y) for y in ys] for lx in layer_x]
    for a, b in zip(cols[:-1], cols[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                ax.plot([x1 + 0.16, x2 - 0.16], [y1, y2], color=GRID, lw=0.5, zorder=0)
    ax.text(3.2, 5.15, r"tanh MLP  $u_\theta(x,t)$", ha="center", fontsize=10, color=SECOND)

    # output
    node(5.5, 3.9, r=0.18, c=VIOLET)
    ax.text(5.5, 4.35, r"$\hat u$", ha="center", fontsize=12)
    for y in ys:
        ax.plot([4.3 + 0.16, 5.5 - 0.18], [y, 3.9], color=GRID, lw=0.5, zorder=0)

    # autodiff -> residual
    box(7.55, 3.9, 3.5, 0.9,
        r"autodiff:  $\hat u_t,\ \hat u_x,\ \hat u_{xx}$" + "\n" +
        r"residual $r=\hat u_t+\hat u\,\hat u_x-\nu\,\hat u_{xx}$",
        "#eef4fb", fs=10)
    arrow(5.68, 3.9, 5.78, 3.9)

    # three loss terms (physics residual vs. data terms), both summed into total
    box(1.8, 1.15, 2.3, 0.72, r"$\mathcal{L}_r$  PDE residual" + "\n" + r"at collocation pts",
        "#eafaf1", fs=9)
    box(4.8, 1.15, 2.3, 0.72, r"$\mathcal{L}_b$  boundary" + "\n" + r"$\mathcal{L}_0$  initial data",
        "#fdf3e6", fs=9)
    box(8.2, 1.15, 2.4, 0.72, r"$\mathcal{L}=\mathcal{L}_r+\mathcal{L}_b+\mathcal{L}_0$",
        "#fbeef4", fs=10)

    arrow(7.55, 3.45, 1.95, 1.52, c=GREEN, ls="--")    # residual box -> L_r
    arrow(5.5, 3.65, 4.8, 1.52, c=YELLOW, ls="--")     # network output -> L_b/L_0 (data fit)
    arrow(2.95, 1.15, 3.65, 1.15, c=MUTED)             # L_r  -> total
    arrow(5.95, 1.15, 6.98, 1.15, c=MUTED)             # L_b/L_0 -> total

    # gradient feedback to theta
    arrow(8.2, 1.52, 8.2, 2.55, c=RED, style="-|>", lw=1.4)
    arrow(8.2, 2.55, 3.25, 2.3, c=RED, style="-|>", lw=1.4)
    ax.text(5.9, 2.62, r"$\nabla_\theta\mathcal{L}$  (backprop)", ha="center",
            fontsize=9, color=RED)

    ax.set_title("A physics-informed neural network: one network, a composite loss",
                 loc="left", fontsize=12, color=INK)
    save(fig, "pinn-architecture.png")


def _read_summary():
    rows = []
    with open(os.path.join(DATA, "results_summary_all.csv")) as fh:
        for r in csv.DictReader(fh):
            rows.append(r)
    return rows


# 2. Relative L2 error across PDEs, grouped by optimizer ----------------------
def fig_l2_comparison():
    rows = _read_summary()
    data = {}  # (pde, opt) -> error
    for r in rows:
        data[(r["pde"], r["optimizer"])] = float(r["error_u"])

    fig, ax = plt.subplots(figsize=(9.0, 4.8))
    n_opt = len(OPT_ORDER)
    group_w = 0.8
    bar_w = group_w / n_opt
    xbase = np.arange(len(PDE_ORDER))
    for j, opt in enumerate(OPT_ORDER):
        xs, ys = [], []
        for i, pde in enumerate(PDE_ORDER):
            v = data.get((pde, opt))
            if v is None:
                continue
            xs.append(xbase[i] - group_w / 2 + bar_w * (j + 0.5))
            ys.append(v)
        ax.bar(xs, ys, width=bar_w * 0.9, color=OPT_COLOR[opt], label=opt, zorder=3)

    ax.set_yscale("log")
    ax.set_ylabel(r"relative $L^2$ error  (log scale)")
    ax.set_xticks(xbase)
    ax.set_xticklabels([PDE_SHORT[p] for p in PDE_ORDER])
    clean(ax, grid=True, axis="y")
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.10), fontsize=10)
    fig.suptitle("Self-scaled quasi-Newton wins on 3 of 4 PDEs; Allen–Cahn is the exception",
                 x=0.02, ha="left", fontsize=11.5, color=INK)
    ax.margins(y=0.08)
    save(fig, "optimizer-l2-comparison.png")


# 3. Burgers loss curves: phase 1 (Adam/learnable) + phase 2 (QN) ------------
def _read_curve(name, ycol):
    xs, ys = [], []
    with open(os.path.join(DATA, name)) as fh:
        for r in csv.DictReader(fh):
            xs.append(float(r[list(r.keys())[0]]))
            ys.append(float(r[ycol]))
    return np.array(xs), np.array(ys)


def fig_burgers_loss():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 4.4), sharey=True)
    for opt in OPT_ORDER:
        x1, y1 = _read_curve(f"burgers_phase1_{opt}.csv", "total_loss")
        ax1.plot(x1, y1, color=OPT_COLOR[opt], lw=1.8, label=opt)
        x2, y2 = _read_curve(f"burgers_phase2_{opt}.csv", "loss")
        ax2.plot(x2, y2, color=OPT_COLOR[opt], lw=1.8, label=opt)

    for ax in (ax1, ax2):
        ax.set_yscale("log")
        ax.set_xlabel("iteration")
        clean(ax, grid=True, axis="both")
    ax1.set_ylabel("training loss (log scale)")
    ax1.set_title("Phase 1 — first-order update", loc="left", fontsize=10.5, color=SECOND)
    ax2.set_title("Phase 2 — quasi-Newton refinement", loc="left", fontsize=10.5, color=SECOND)
    ax2.legend(loc="upper right", fontsize=9)
    fig.suptitle("Burgers: the quasi-Newton phase is where SSBFGS / SSBroyden pull away",
                 x=0.02, ha="left", fontsize=11.5, color=INK)
    fig.text(0.02, -0.02,
             "Phase-2 curves are the SciPy L-BFGS / self-scaled QN loss histories; "
             "self-scaled variants hit precision-loss termination in ~1k iters.",
             va="top", fontsize=8.5, color=MUTED)
    save(fig, "burgers-loss-curves.png")


if __name__ == "__main__":
    print("Generating Scientific ML figures ->", os.path.abspath(OUT))
    fig_architecture()
    fig_l2_comparison()
    fig_burgers_loss()
    print("done.")
