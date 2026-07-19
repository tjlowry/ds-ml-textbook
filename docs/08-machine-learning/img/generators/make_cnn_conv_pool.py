"""Generate the convolution + max-pool schematic for deep-learning/cnns.md.

Illustrates the building blocks of the ECEN 758 CIFAR-100 custom CNN described
on the page: 3x3 convolution kernels + ReLU, then 2x2 max-pooling.

  Input 8x8  --(3x3 conv, stride 1, valid)-->  Feature map 6x6  (8-3+1 = 6)
             --(2x2 max-pool, stride 2)------>  Pooled map 3x3   (6/2 = 3)

One 3x3 kernel window on the input is highlighted and mapped by an arrow to the
single feature-map cell it produces; then a 2x2 window on the feature map is
mapped to the single pooled cell it produces. Dimensions are labelled and the
arithmetic is exact. Pure schematic (no data / no randomness).

Run:  python make_cnn_conv_pool.py
Writes: ../cnn-conv-pool.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

# dimension arithmetic (asserted so the labels can never drift)
N_IN, K, POOL = 8, 3, 2
N_FEAT = N_IN - K + 1          # 6
N_POOL = N_FEAT // POOL        # 3
assert (N_FEAT, N_POOL) == (6, 3)

INBLUE, FEATOR, POOLGR = "#EAF2FA", "#FDF0E1", "#EDF6EA"
EDGE, TXT = "#B9C4CE", "#222222"
GRID_IN, GRID_FE, GRID_PO = "#7FA8C9", "#E0A56B", "#8CC084"
CONV, POOLC = "#1E7A34", "#7D3C98"   # conv highlight green, pool highlight purple

CELL = 0.40
MIDY = 4.15

fig, ax = plt.subplots(figsize=(13.6, 6.2))
ax.set_xlim(0, 13.6)
ax.set_ylim(0, 6.2)
ax.set_aspect("equal")
ax.axis("off")


def grid(origin, n, fc, gridc):
    """Draw an n x n grid; origin = top-left corner. Return the origin."""
    ox, oy = origin
    ax.add_patch(Rectangle((ox, oy - n * CELL), n * CELL, n * CELL,
                           facecolor=fc, edgecolor="none", zorder=1))
    for i in range(n + 1):
        ax.plot([ox, ox + n * CELL], [oy - i * CELL, oy - i * CELL],
                color=gridc, lw=0.8, zorder=2)
        ax.plot([ox + i * CELL, ox + i * CELL], [oy, oy - n * CELL],
                color=gridc, lw=0.8, zorder=2)
    return origin


def cell_rect(origin, r0, c0, rows, cols, color, lw=2.6):
    ox, oy = origin
    ax.add_patch(Rectangle((ox + c0 * CELL, oy - (r0 + rows) * CELL),
                           cols * CELL, rows * CELL, fill=False,
                           edgecolor=color, lw=lw, zorder=5))


def center_origin(n, cx):
    """top-left origin so the n x n grid is centered on (cx, MIDY)."""
    return (cx - n * CELL / 2, MIDY + n * CELL / 2)


# --- three stages ----------------------------------------------------------
in_org = center_origin(N_IN, 2.15)
fe_org = center_origin(N_FEAT, 7.0)
po_org = center_origin(N_POOL, 11.4)

grid(in_org, N_IN, INBLUE, GRID_IN)
grid(fe_org, N_FEAT, FEATOR, GRID_FE)
grid(po_org, N_POOL, POOLGR, GRID_PO)

# highlights: 3x3 conv window (top-left) -> feature cell (0,0)
cell_rect(in_org, 0, 0, K, K, CONV)
cell_rect(fe_org, 0, 0, 1, 1, CONV)
# 2x2 pool window (top-left of feature map) -> pooled cell (0,0)
cell_rect(fe_org, 0, 0, POOL, POOL, POOLC)
cell_rect(po_org, 0, 0, 1, 1, POOLC)


def top_right(origin, r0, c0, rows, cols):
    ox, oy = origin
    return (ox + (c0 + cols) * CELL, oy - (r0) * CELL)


def cell_center(origin, r0, c0):
    ox, oy = origin
    return (ox + (c0 + 0.5) * CELL, oy - (r0 + 0.5) * CELL)


# arrow: conv window -> feature cell (0,0)
ax.add_patch(FancyArrowPatch(top_right(in_org, 0, 0, K, K),
             cell_center(fe_org, 0, 0), arrowstyle="-|>", mutation_scale=17,
             lw=2.0, color=CONV, connectionstyle="arc3,rad=-0.18", zorder=6))
# arrow: pool window -> pooled cell (0,0)
ax.add_patch(FancyArrowPatch(top_right(fe_org, 0, 0, POOL, POOL),
             cell_center(po_org, 0, 0), arrowstyle="-|>", mutation_scale=17,
             lw=2.0, color=POOLC, connectionstyle="arc3,rad=-0.18", zorder=6))

# --- stage labels ----------------------------------------------------------
bottom = MIDY - N_IN * CELL / 2 - 0.35
ax.text(2.15, MIDY + N_IN * CELL / 2 + 0.35, "Input  8 x 8", ha="center",
        fontsize=12, fontweight="bold", color=TXT)
ax.text(7.0, MIDY + N_FEAT * CELL / 2 + 0.35, "Feature map  6 x 6", ha="center",
        fontsize=12, fontweight="bold", color=TXT)
ax.text(11.4, MIDY + N_POOL * CELL / 2 + 0.35, "Pooled map  3 x 3", ha="center",
        fontsize=12, fontweight="bold", color=TXT)

# operation captions in the gaps at mid-height (clear of the arrows above)
ax.text(4.55, MIDY - 0.05, "3x3 conv + ReLU\nstride 1, valid\n(8 − 3 + 1 = 6)",
        ha="center", va="center", fontsize=9.8, color=CONV, fontweight="bold")
ax.text(9.35, MIDY - 0.05, "2x2 max-pool\nstride 2\n(6 / 2 = 3)",
        ha="center", va="center", fontsize=9.8, color=POOLC, fontweight="bold")

# per-cell explanations
ax.text(2.15, bottom, "3x3 kernel window (green)", ha="center", fontsize=9,
        color=CONV, style="italic")
ax.text(7.0, bottom, "each window → one cell;\n2x2 pool window (purple)",
        ha="center", fontsize=9, color=TXT, style="italic")
ax.text(11.4, bottom, "max of the 4 → one cell", ha="center", fontsize=9,
        color=POOLC, style="italic")

ax.set_title("Convolution then max-pooling — the building blocks of the "
             "CIFAR-100 CNN (3x3 kernels, ReLU, 2x2 pool)",
             fontsize=12.5, fontweight="bold", color=TXT, y=1.0)

fig.patch.set_facecolor("white")
fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "cnn-conv-pool.png")
fig.savefig(out, dpi=110, bbox_inches="tight", facecolor="white")
print("wrote", os.path.abspath(out))
