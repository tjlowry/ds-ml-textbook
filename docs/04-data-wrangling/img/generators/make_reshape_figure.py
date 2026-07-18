"""Generate the wide<->long (melt/pivot) reshape diagram for tidy-data-reshaping.md.

Run:  python make_reshape_figure.py
Writes: ../tidy-vs-long.png
"""
import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

BLUE = "#3f51b5"      # indigo, matches site accent
GREY = "#5f6368"
LIGHT = "#e8eaf6"
HEAD = "#c5cae9"

def draw_table(ax, x0, y0, headers, rows, colw, rowh=0.5, title="", title_color=GREY):
    ncol = len(headers)
    width = ncol * colw
    nrow = len(rows)
    # title
    ax.text(x0 + width / 2, y0 + rowh * 0.7, title, ha="center", va="bottom",
            fontsize=11, fontweight="bold", color=title_color)
    # header row
    for j, h in enumerate(headers):
        ax.add_patch(plt.Rectangle((x0 + j * colw, y0), colw, rowh,
                                    facecolor=HEAD, edgecolor="white", lw=1.5))
        ax.text(x0 + j * colw + colw / 2, y0 + rowh / 2, h, ha="center", va="center",
                fontsize=9.5, fontweight="bold", color="#1a237e")
    # body
    for i, row in enumerate(rows):
        yy = y0 - (i + 1) * rowh
        for j, val in enumerate(row):
            ax.add_patch(plt.Rectangle((x0 + j * colw, yy), colw, rowh,
                                       facecolor=LIGHT if i % 2 == 0 else "white",
                                       edgecolor="white", lw=1.5))
            ax.text(x0 + j * colw + colw / 2, yy + rowh / 2, str(val),
                    ha="center", va="center", fontsize=9, color="#212121")
    return width, (nrow + 1) * rowh

fig, ax = plt.subplots(figsize=(9.5, 4.6))
ax.set_xlim(0, 11)
ax.set_ylim(0, 5.4)
ax.axis("off")

# WIDE / messy: one column per year
wide_headers = ["country", "1999", "2000"]
wide_rows = [
    ["A", 745, 2666],
    ["B", 37737, 80488],
    ["C", 212258, 213766],
]
draw_table(ax, 0.3, 4.4, wide_headers, wide_rows, colw=1.15, title="WIDE  (values in column names)", title_color="#c62828")

# LONG / tidy: year is its own variable
long_headers = ["country", "year", "cases"]
long_rows = [
    ["A", 1999, 745],
    ["A", 2000, 2666],
    ["B", 1999, 37737],
    ["B", 2000, 80488],
    ["C", 1999, 212258],
    ["C", 2000, 213766],
]
draw_table(ax, 7.0, 4.4, long_headers, long_rows, colw=1.15, title="LONG / TIDY  (one row per obs.)", title_color="#2e7d32")

# arrows between them
arrow_melt = FancyArrowPatch((4.05, 3.5), (6.9, 3.9), arrowstyle="-|>", mutation_scale=18,
                             lw=2.2, color=BLUE, connectionstyle="arc3,rad=-0.15")
arrow_pivot = FancyArrowPatch((6.9, 2.2), (4.05, 2.7), arrowstyle="-|>", mutation_scale=18,
                              lw=2.2, color=GREY, connectionstyle="arc3,rad=-0.15")
ax.add_patch(arrow_melt)
ax.add_patch(arrow_pivot)
ax.text(5.5, 3.95, "df.melt(...)", ha="center", va="bottom", fontsize=10,
        fontweight="bold", color=BLUE)
ax.text(5.5, 2.15, "df.pivot_table(...)", ha="center", va="top", fontsize=10,
        fontweight="bold", color=GREY)

fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "tidy-vs-long.png")
fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
print("wrote", os.path.abspath(out))
