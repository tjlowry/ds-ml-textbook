"""Generate the bagging-vs-boosting schematic for ensembles/bagging-boosting.md.

Two panels in the leakage-timeline house style (pastel boxes + arrows):

  Bagging (left)  -- one training set is bootstrap-resampled into independent
  subsets, each grows a tree IN PARALLEL, and the trees are combined by an
  averaged / majority vote. Reduces variance.

  Boosting (right) -- models are trained SEQUENTIALLY; each new model is fit on
  the previous model's residuals / reweighted errors (the arrows carry "errors"
  forward), and the final prediction is a weighted sum. Reduces bias.

Purely schematic (no data, no randomness -> deterministic).

Run:  python make_bagging_boosting.py
Writes: ../bagging-boosting.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BLUE, ORANGE, GREEN = "#BCD8EE", "#F6D5B3", "#CBE6C4"
EDGE, TXT = "#4A4A4A", "#222222"
GREENA, RED = "#1E7A34", "#C0392B"

fig, ax = plt.subplots(figsize=(13.2, 6.8))
ax.set_xlim(0, 13.2)
ax.set_ylim(0, 7.2)
ax.axis("off")


def box(cx, cy, w, h, text, fc, ec=EDGE, fs=10.5, lw=1.4, bold=True):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                 boxstyle="round,pad=0.02,rounding_size=0.08",
                 facecolor=fc, edgecolor=ec, lw=lw, zorder=3))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs,
            color=TXT, fontweight="bold" if bold else "normal", zorder=4)


def arrow(p0, p1, col=EDGE, lw=1.6, rad=0.0, ls="-", z=2):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=15,
                 lw=lw, color=col, connectionstyle=f"arc3,rad={rad}",
                 linestyle=ls, zorder=z))


# =========================== LEFT: BAGGING =================================
ax.text(3.1, 6.85, "Bagging  (bootstrap aggregating)", ha="center",
        fontsize=13, fontweight="bold", color=TXT)
ax.text(3.1, 6.45, "parallel  ·  independent models  ·  reduces variance",
        ha="center", fontsize=9.5, color="#6B6B6B", style="italic")

xs = [1.15, 3.1, 5.05]
box(3.1, 5.7, 3.2, 0.7, "Training set", BLUE)
for x in xs:                                   # bootstrap samples
    arrow((3.1, 5.35), (x, 4.62), rad=0.0)
    box(x, 4.25, 1.55, 0.66, "Bootstrap\nsample", BLUE, fs=9)
for x in xs:                                   # -> trees (parallel, independent)
    arrow((x, 3.92), (x, 3.28))
    box(x, 2.9, 1.55, 0.66, "Tree", ORANGE, fs=10)
for x in xs:                                   # trees -> vote
    arrow((x, 2.57), (3.1, 1.72), rad=0.0)
box(3.1, 1.35, 3.2, 0.72, "Average / majority vote", GREEN, ec=GREENA, lw=1.8)
ax.text(3.1, 0.7, "each tree sees a different resample; votes are combined equally",
        ha="center", fontsize=8.8, color="#6B6B6B", style="italic")

# panel divider
ax.plot([6.6, 6.6], [0.5, 6.6], color="#D0D0D0", lw=1.4, ls=(0, (4, 4)))

# =========================== RIGHT: BOOSTING ==============================
ax.text(9.9, 6.85, "Boosting", ha="center", fontsize=13, fontweight="bold", color=TXT)
ax.text(9.9, 6.45, "sequential  ·  each model fixes the last one's errors  "
        "·  reduces bias", ha="center", fontsize=9.5, color="#6B6B6B", style="italic")

box(9.9, 5.7, 2.5, 0.66, "Training set", BLUE)
ys = [4.75, 3.55, 2.35]
labels = ["Model 1", "Model 2", "Model 3"]
arrow((9.9, 5.37), (9.9, 5.08))
for i, (y, lab) in enumerate(zip(ys, labels)):
    box(9.9, y, 2.3, 0.62, lab, ORANGE)
    if i < len(ys) - 1:
        # main chain arrow carrying residuals to the next model
        arrow((9.9, y - 0.31), (9.9, ys[i + 1] + 0.31), col=RED, lw=2.0)
        ax.text(10.15, (y + ys[i + 1]) / 2, "residuals /\nreweighted errors",
                ha="left", va="center", fontsize=8.6, color=RED, style="italic")
arrow((9.9, ys[-1] - 0.31), (9.9, 1.72))
box(9.9, 1.35, 2.9, 0.72, "Weighted sum", GREEN, ec=GREENA, lw=1.8)
ax.text(9.9, 0.7, "model k is trained on what models 1..k−1 still got wrong",
        ha="center", fontsize=8.8, color="#6B6B6B", style="italic")

ax.set_title("Two ways to combine weak learners into a strong one",
             fontsize=13.5, fontweight="bold", color=TXT, y=1.0)

fig.patch.set_facecolor("white")
fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "bagging-boosting.png")
fig.savefig(out, dpi=110, bbox_inches="tight", facecolor="white")
print("wrote", os.path.abspath(out))
