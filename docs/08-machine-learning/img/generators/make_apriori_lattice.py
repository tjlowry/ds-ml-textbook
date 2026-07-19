"""Generate the Apriori downward-closure lattice for other/itemset-mining.md.

The full subset lattice over four items {A, B, C, D}, drawn level by level from
singletons (top) down to the full set ABCD (bottom). Singleton {C} is marked
infrequent (red); by the downward-closure / anti-monotonicity property EVERY
superset of {C} is therefore infrequent too, so all of them are greyed out and
struck through -- the pruning that makes Apriori tractable. The surviving
candidates (those containing no infrequent subset) stay green.

The pruned set is computed here ("C" in the itemset label), not hand-listed, so
the picture cannot drift out of sync.

Run:  python make_apriori_lattice.py
Writes: ../apriori-lattice.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

# ---- lattice definition ---------------------------------------------------
levels = {
    1: ["A", "B", "C", "D"],
    2: ["AB", "AC", "AD", "BC", "BD", "CD"],
    3: ["ABC", "ABD", "ACD", "BCD"],
    4: ["ABCD"],
}
INFREQ = "C"                       # the itemset declared infrequent

# hand-placed x positions per level; y decreases as sets grow
xpos = {
    1: [2.0, 4.4, 6.8, 9.2],
    2: [1.2, 2.9, 4.6, 6.3, 8.0, 9.7],
    3: [2.4, 4.7, 7.0, 9.3],
    4: [5.6],
}
ylev = {1: 6.4, 2: 4.7, 3: 3.0, 4: 1.3}

pos = {}
for lvl, sets in levels.items():
    for s, x in zip(sets, xpos[lvl]):
        pos[s] = (x, ylev[lvl])


def is_pruned(s):
    return s != INFREQ and INFREQ in s      # a proper superset of {C}


# ---- colors ---------------------------------------------------------------
GREEN, GREY = "#CBE6C4", "#DADADA"
RED_FILL, RED = "#F3C9C4", "#C0392B"
EDGE, TXT, WIN = "#4A4A4A", "#222222", "#1E7A34"

BW, BH = 1.34, 0.74          # box width / height

fig, ax = plt.subplots(figsize=(11.6, 6.8))
ax.set_xlim(0, 11.2)
ax.set_ylim(0.2, 7.6)
ax.axis("off")


def differ_by_one(a, b):
    """True if set b (larger) is a's superset with exactly one extra element."""
    return len(b) == len(a) + 1 and all(ch in b for ch in a)


# ---- edges (subset -> superset), drawn first so boxes sit on top ----------
for lvl in (1, 2, 3):
    for a in levels[lvl]:
        for b in levels[lvl + 1]:
            if differ_by_one(a, b):
                x0, y0 = pos[a]
                x1, y1 = pos[b]
                pruned_edge = is_pruned(a) or is_pruned(b) or a == INFREQ
                ax.plot([x0, x1], [y0 - BH / 2, y1 + BH / 2],
                        color="#CFCFCF" if pruned_edge else "#9AA0A6",
                        lw=1.0 if pruned_edge else 1.4,
                        ls=(0, (3, 3)) if pruned_edge else "-", zorder=1)

# ---- boxes ----------------------------------------------------------------
for s, (x, y) in pos.items():
    if s == INFREQ:
        fc, ec, lw = RED_FILL, RED, 2.6
    elif is_pruned(s):
        fc, ec, lw = GREY, "#A9A9A9", 1.2
    else:
        fc, ec, lw = GREEN, WIN, 1.6
    box = FancyBboxPatch((x - BW / 2, y - BH / 2), BW, BH,
                         boxstyle="round,pad=0.02,rounding_size=0.10",
                         facecolor=fc, edgecolor=ec, lw=lw, zorder=3)
    ax.add_patch(box)
    label = "{" + ",".join(s) + "}"
    tcol = "#8A8A8A" if is_pruned(s) else TXT
    ax.text(x, y, label, ha="center", va="center", fontsize=11.5,
            fontweight="bold", color=tcol, zorder=4)
    if is_pruned(s):                      # strike-through bar
        ax.plot([x - BW / 2 + 0.14, x + BW / 2 - 0.14], [y, y],
                color=RED, lw=1.6, zorder=5)

# ---- level labels on the left ---------------------------------------------
names = {1: "1-itemsets", 2: "2-itemsets", 3: "3-itemsets", 4: "4-itemset"}
for lvl, y in ylev.items():
    ax.text(0.15, y, names[lvl], ha="left", va="center", fontsize=10,
            color="#6B6B6B", style="italic")

# ---- annotations ----------------------------------------------------------
ax.annotate("{C} is infrequent", xy=pos["C"], xytext=(6.8, 7.35),
            ha="center", fontsize=11, color=RED, fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6))

ax.text(9.9, 6.9,
        "downward closure:\nprune every superset of {C}",
        ha="center", va="center", fontsize=10, color=RED,
        bbox=dict(boxstyle="round,pad=0.45", fc="#FBEFEE", ec=RED, lw=1.4))

# legend
lx, ly = 0.4, 1.35
ax.add_patch(Rectangle((lx, ly), 0.34, 0.34, facecolor=GREEN, edgecolor=WIN, lw=1.4))
ax.text(lx + 0.5, ly + 0.17, "still a candidate (frequent so far)", va="center",
        fontsize=9.5, color="#555")
ax.add_patch(Rectangle((lx, ly - 0.55), 0.34, 0.34, facecolor=GREY, edgecolor="#A9A9A9", lw=1.2))
ax.text(lx + 0.5, ly - 0.38, "pruned (contains infrequent {C})", va="center",
        fontsize=9.5, color="#555")

ax.set_title("Apriori pruning: one infrequent itemset removes its whole "
             "super-lattice",
             fontsize=13, fontweight="bold", color=TXT, y=0.99)

fig.patch.set_facecolor("white")
fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "apriori-lattice.png")
fig.savefig(out, dpi=110, bbox_inches="tight", facecolor="white")
print("wrote", os.path.abspath(out))
print("pruned:", sorted(s for s in pos if is_pruned(s)))
print("kept  :", sorted(s for s in pos if not is_pruned(s) and s != INFREQ))
