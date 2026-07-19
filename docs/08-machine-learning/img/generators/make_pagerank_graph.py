"""Generate the PageRank directed-graph figure for other/pagerank.md.

A 7-node directed graph drawn by hand (no networkx). Node PageRank values are
computed here with numpy power iteration (damping 0.85) on the graph's own
adjacency matrix, and each node's circle radius is drawn strictly proportional
to its computed PageRank. The graph is designed so node A — with only TWO
in-links, but from the important hubs C and D — outranks node B, which has
THREE in-links but only from the minor leaf pages E, F, G. That is the whole
point of PageRank: who links to you matters more than how many.

Run:  python make_pagerank_graph.py
Writes: ../pagerank-graph.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

# ---- graph definition -----------------------------------------------------
labels = ["A", "B", "C", "D", "E", "F", "G"]
idx = {l: i for i, l in enumerate(labels)}
n = len(labels)

# directed edges (source -> target)
edges = [
    ("A", "C"), ("A", "D"),          # A points up into the two hubs
    ("C", "D"), ("D", "C"),          # hubs mutually reinforce each other
    ("C", "A"), ("D", "A"),          # both hubs point to A  -> A: 2 important in-links
    ("E", "B"), ("F", "B"), ("G", "B"),  # 3 leaves point to B -> many, but minor
    ("B", "E"), ("B", "F"), ("B", "G"),  # B recycles to leaves (no dangling nodes)
    ("E", "C"),                      # bridge so the graph is one connected component
]

# ---- PageRank via power iteration (damping 0.85) --------------------------
M = np.zeros((n, n))                  # column-stochastic: M[to, from]
for s, t in edges:
    M[idx[t], idx[s]] = 1.0
outdeg = M.sum(axis=0)
for j in range(n):
    if outdeg[j] > 0:
        M[:, j] /= outdeg[j]
d = 0.85
r = np.ones(n) / n
for _ in range(500):
    r = d * (M @ r) + (1 - d) / n
r /= r.sum()
pr = {l: r[idx[l]] for l in labels}
print("PageRank values:", {l: round(v, 3) for l, v in pr.items()})
assert pr["A"] > pr["B"], "phenomenon broken: A must outrank B"

# ---- layout (hand-placed positions) --------------------------------------
pos = {
    "C": (2.0, 4.5), "D": (2.0, 1.7), "A": (4.5, 3.1),
    "B": (7.7, 3.1), "E": (10.0, 4.6), "F": (10.5, 3.1), "G": (10.0, 1.6),
}

# role-based pastel colors
BLUE, ORANGE, GREEN, PURPLE = "#BCD8EE", "#F6D5B3", "#CBE6C4", "#E6C9E3"
color = {"A": BLUE, "B": ORANGE, "C": PURPLE, "D": PURPLE,
         "E": GREEN, "F": GREEN, "G": GREEN}
EDGE, TXT = "#4A4A4A", "#222222"
WIN, LOSE = "#1E7A34", "#C0392B"

# circle radius strictly proportional to PageRank (area grows even faster)
RSCALE = 2.4
radius = {l: pr[l] * RSCALE for l in labels}

fig, ax = plt.subplots(figsize=(11.2, 6.2))
ax.set_xlim(0, 12.4)
ax.set_ylim(0, 6.2)
ax.set_aspect("equal")
ax.axis("off")


def draw_arrow(s, t, col=EDGE, lw=1.6, style="-", rad=0.0, z=1):
    x0, y0 = pos[s]
    x1, y1 = pos[t]
    dx, dy = x1 - x0, y1 - y0
    dist = np.hypot(dx, dy)
    ux, uy = dx / dist, dy / dist
    # trim endpoints to circle borders
    sx, sy = x0 + ux * (radius[s] + 0.02), y0 + uy * (radius[s] + 0.02)
    ex, ey = x1 - ux * (radius[t] + 0.06), y1 - uy * (radius[t] + 0.06)
    arr = FancyArrowPatch((sx, sy), (ex, ey),
                          arrowstyle="-|>", mutation_scale=16,
                          lw=lw, color=col, linestyle=style,
                          connectionstyle=f"arc3,rad={rad}", zorder=z)
    ax.add_patch(arr)


# draw edges (bidirectional pairs curved so both arrows are visible)
bidir = {("C", "D"), ("D", "C")}
for s, t in edges:
    if s == "E" and t == "C":
        draw_arrow(s, t, col="#9AA0A6", lw=1.4, style=(0, (4, 3)), rad=-0.32)  # bridge
    elif (s, t) in bidir:
        draw_arrow(s, t, rad=0.18)
    else:
        # curve the A<->hub reciprocal pairs slightly so they don't overlap
        rad = 0.14 if (s, t) in {("A", "C"), ("A", "D")} else (
            -0.14 if (s, t) in {("C", "A"), ("D", "A")} else 0.0)
        draw_arrow(s, t, rad=rad)

# bridge label
ax.text(6.0, 5.55, "bridge (E→C)", fontsize=9, color="#6B6B6B",
        ha="center", style="italic")

# draw nodes + labels
for l in labels:
    x, y = pos[l]
    ec = WIN if l == "A" else (LOSE if l == "B" else EDGE)
    lw = 2.6 if l in ("A", "B") else 1.4
    ax.add_patch(Circle((x, y), radius[l], facecolor=color[l],
                        edgecolor=ec, lw=lw, zorder=5))
    ax.text(x, y, l, ha="center", va="center", fontsize=13,
            fontweight="bold", color=TXT, zorder=6)
    # PageRank value below each node
    ax.text(x, y - radius[l] - 0.24, f"PR={pr[l]:.2f}", ha="center", va="top",
            fontsize=10, color=TXT, zorder=6)

# in-link count tags for the two contrasted nodes
ax.annotate("2 in-links\n(from hubs C, D)", xy=pos["A"], xytext=(4.5, 5.5),
            ha="center", fontsize=9.5, color=WIN, fontweight="bold")
ax.annotate("3 in-links\n(from leaves E, F, G)", xy=pos["B"], xytext=(8.05, 0.75),
            ha="center", fontsize=9.5, color=LOSE, fontweight="bold")

# takeaway callout box
ax.text(6.2, 0.28,
        "Fewer, better-connected in-links win:  A (PR 0.20, 2 hub links)  "
        "outranks  B (PR 0.17, 3 leaf links).",
        ha="center", va="center", fontsize=10.5, color=TXT,
        bbox=dict(boxstyle="round,pad=0.5", fc="#F3F3F3", ec="#BFBFBF"))

ax.set_title("PageRank: importance flows from important linkers "
             "(damping 0.85, power iteration)",
             fontsize=12.5, fontweight="bold", color=TXT, pad=10)

fig.patch.set_facecolor("white")
fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "pagerank-graph.png")
fig.savefig(out, dpi=110, bbox_inches="tight", facecolor="white")
print("wrote", os.path.abspath(out))
