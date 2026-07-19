"""Generate the matrix-factorization schematic for other/recommenders.md.

A user x item ratings grid R (6x5) with a few observed ratings and many empty
(grey "?") cells is approximated by U (6x2, latent user factors) times V^T
(2x5, latent item factors). One empty cell -- User 5 x Item 3 -- is highlighted,
and its predicted rating is shown as the exact dot product of the highlighted U
row and V^T column. All numbers are self-consistent: the observed integer
ratings are the rounded reconstruction U @ V^T, and the highlighted prediction
is the exact (unrounded) dot product printed by this script.

Run:  python make_matrix_factorization.py
Writes: ../matrix-factorization.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

# ---- exact latent factors -------------------------------------------------
U = np.array([[1.8, 0.4], [0.5, 1.9], [1.6, 0.6],
              [0.3, 1.7], [1.2, 1.2], [0.9, 0.5]])   # 6 users x 2 factors
Vt = np.array([[2.0, 0.4, 1.5, 1.9, 0.6],
               [0.5, 2.1, 1.4, 0.3, 1.8]])           # 2 factors x 5 items
R = U @ Vt
Rint = np.round(R).astype(int)

HL_U, HL_I = 4, 2                                     # highlight User5 x Item3
pred = float(U[HL_U] @ Vt[:, HL_I])
print("prediction R_hat[U5,I3] =", round(pred, 2),
      "= %.1f*%.1f + %.1f*%.1f" % (U[HL_U, 0], Vt[0, HL_I], U[HL_U, 1], Vt[1, HL_I]))
assert abs(pred - 3.48) < 1e-9

# observed mask: 1 = show integer rating, 0 = empty "?"  (highlight cell empty)
mask = np.array([
    [1, 1, 0, 1, 0],
    [0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0],
    [1, 1, 0, 0, 1],
    [1, 0, 0, 1, 0],   # (U5,I3) is 0 -> empty, this is the highlighted cell
    [0, 1, 1, 0, 1],
])
assert mask[HL_U, HL_I] == 0

# ---- colors ---------------------------------------------------------------
BLUE, ORANGE = "#BCD8EE", "#F6D5B3"
GREY_FILL, EDGE, TXT = "#E4E4E4", "#4A4A4A", "#222222"
WIN = "#1E7A34"

CELL = 0.66
fig, ax = plt.subplots(figsize=(13.2, 6.6))
ax.set_xlim(0, 20)
ax.set_ylim(0, 10)
ax.set_aspect("equal")
ax.axis("off")


def cell_xy(origin, row, col):
    ox, oy = origin
    return ox + col * CELL, oy - row * CELL   # rows go downward from top


def draw_matrix(origin, nrows, ncols, facecolor,
                value_fn, hl_row=None, hl_col=None):
    ox, oy = origin
    for rr in range(nrows):
        for cc in range(ncols):
            x, y = cell_xy(origin, rr, cc)
            txt, fc = value_fn(rr, cc)
            ax.add_patch(Rectangle((x, y - CELL), CELL, CELL,
                                   facecolor=fc, edgecolor=EDGE, lw=1.1))
            ax.text(x + CELL / 2, y - CELL / 2, txt, ha="center", va="center",
                    fontsize=11, color=TXT if txt != "?" else "#8A8A8A",
                    fontweight="normal")
    # highlight a full row or column with a green frame
    if hl_row is not None:
        x, y = cell_xy(origin, hl_row, 0)
        ax.add_patch(Rectangle((x, y - CELL), ncols * CELL, CELL,
                               fill=False, edgecolor=WIN, lw=2.6, zorder=6))
    if hl_col is not None:
        x, y = cell_xy(origin, 0, hl_col)
        ax.add_patch(Rectangle((x, y - nrows * CELL), CELL, nrows * CELL,
                               fill=False, edgecolor=WIN, lw=2.6, zorder=6))


# ---- R : ratings grid -----------------------------------------------------
R_ORG = (1.4, 8.4)


def r_val(rr, cc):
    if rr == HL_U and cc == HL_I:
        return "?", "#D9F0DC"                      # highlighted unknown cell
    if mask[rr, cc]:
        return str(Rint[rr, cc]), "white"
    return "?", GREY_FILL


draw_matrix(R_ORG, 6, 5, "white", r_val)
# highlighted cell green frame
hx, hy = cell_xy(R_ORG, HL_U, HL_I)
ax.add_patch(Rectangle((hx, hy - CELL), CELL, CELL, fill=False,
                       edgecolor=WIN, lw=2.8, zorder=7))
# row/col headers for R
for cc in range(5):
    x, _ = cell_xy(R_ORG, 0, cc)
    ax.text(x + CELL / 2, R_ORG[1] + 0.22, f"I{cc+1}", ha="center", va="bottom",
            fontsize=10, color=TXT, fontweight="bold")
for rr in range(6):
    _, y = cell_xy(R_ORG, rr, 0)
    ax.text(R_ORG[0] - 0.18, y - CELL / 2, f"U{rr+1}", ha="right", va="center",
            fontsize=10, color=TXT, fontweight="bold")
ax.text(R_ORG[0] + 2.5 * CELL, R_ORG[1] + 0.95, "R  (users x items)",
        ha="center", fontsize=12, fontweight="bold", color=TXT)
# mini legend (top-left, clear of the arrow path): observed vs missing
lx, ly = 0.7, 1.75
ax.add_patch(Rectangle((lx, ly), 0.42, 0.42, facecolor="white", edgecolor=EDGE, lw=1.1))
ax.text(lx + 0.6, ly + 0.21, "observed rating (1-5)", va="center", fontsize=9.5, color="#6B6B6B")
ax.add_patch(Rectangle((lx, ly - 0.7), 0.42, 0.42, facecolor=GREY_FILL, edgecolor=EDGE, lw=1.1))
ax.text(lx + 0.6, ly - 0.49, "?  = missing rating", va="center", fontsize=9.5, color="#6B6B6B")

# approx symbol
ax.text(6.35, 6.4, r"$\approx$", fontsize=30, ha="center", va="center", color=TXT)

# ---- U : user factors (6x2) ----------------------------------------------
U_ORG = (7.4, 8.4)


def u_val(rr, cc):
    return f"{U[rr, cc]:.1f}", BLUE


draw_matrix(U_ORG, 6, 2, BLUE, u_val, hl_row=HL_U)
ax.text(U_ORG[0] + CELL, U_ORG[1] + 0.95, "U  (6x2)", ha="center",
        fontsize=12, fontweight="bold", color=TXT)
ax.text(U_ORG[0] + CELL, U_ORG[1] + 0.30, "2 latent user factors", ha="center",
        fontsize=9.5, color="#6B6B6B", style="italic")

# times symbol
ax.text(9.55, 6.4, r"$\times$", fontsize=26, ha="center", va="center", color=TXT)

# ---- V^T : item factors (2x5) -- vertically centered on U block ----------
VT_ORG = (10.4, 6.4 + CELL)   # top so the 2 rows straddle the middle


def vt_val(rr, cc):
    return f"{Vt[rr, cc]:.1f}", ORANGE


draw_matrix(VT_ORG, 2, 5, ORANGE, vt_val, hl_col=HL_I)
ax.text(VT_ORG[0] + 2.5 * CELL, VT_ORG[1] + 0.55, r"$V^{T}$  (2x5)", ha="center",
        fontsize=12, fontweight="bold", color=TXT)
ax.text(VT_ORG[0] + 2.5 * CELL, VT_ORG[1] - 2 * CELL - 0.30,
        "2 latent item factors", ha="center", fontsize=9.5,
        color="#6B6B6B", style="italic")

# ---- prediction callout ---------------------------------------------------
box = ("Predict the missing (U5, I3) rating = dot product of the highlighted\n"
       "row and column:   U5 . V3  =  (1.2)(1.5) + (1.2)(1.4)  =  1.80 + 1.68  =  3.48")
ax.text(10.3, 1.15, box, ha="center", va="center", fontsize=11, color=TXT,
        bbox=dict(boxstyle="round,pad=0.6", fc="#D9F0DC", ec=WIN, lw=1.8))

# arrow from callout up to the highlighted R cell (routed right of the grid)
ax.add_patch(FancyArrowPatch((5.7, 1.35), (hx + CELL + 0.05, hy - CELL / 2),
             arrowstyle="-|>", mutation_scale=16, lw=1.6, color=WIN,
             connectionstyle="arc3,rad=-0.28"))

ax.set_title("Matrix factorization fills in missing ratings: "
             r"$R \approx U V^{T}$",
             fontsize=13.5, fontweight="bold", color=TXT, y=0.99)

fig.patch.set_facecolor("white")
fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "matrix-factorization.png")
fig.savefig(out, dpi=110, bbox_inches="tight", facecolor="white")
print("wrote", os.path.abspath(out))
