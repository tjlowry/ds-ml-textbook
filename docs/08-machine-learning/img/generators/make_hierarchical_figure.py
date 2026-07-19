"""Two-panel hierarchical-clustering figure for hierarchical.md.

Left:  a Ward dendrogram of a ~40-point subsample of the shared dataset (small
       enough that the leaves are readable), with the cut height drawn as a
       dashed line.
Right: the same subsampled points, colored by cutting the tree into k clusters
       at that height.

Same shared dataset as the k-means / DBSCAN / GMM figures, just subsampled.
Illustrative synthetic demo built for this page.

Run:  python make_hierarchical_figure.py
Writes: ../hierarchical-shared-data.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

from shared_dataset import make_shared_data, PASTELS, EDGE, TEXT, SEED

np.random.seed(SEED)

X, kind = make_shared_data()

# Subsample ~40 points (excluding the uniform noise) so the dendrogram leaves
# stay readable and the tree reflects the blob/moon structure.
rng = np.random.RandomState(SEED)
pool = np.where(kind != 5)[0]
idx = rng.choice(pool, size=40, replace=False)
Xs = X[idx]

Z = linkage(Xs, method="ward")

K = 5
# Cut height: midway between the (K-1)th and Kth largest merge distances.
merge_h = np.sort(Z[:, 2])
cut = (merge_h[-K] + merge_h[-(K + 1)]) / 2.0
labels = fcluster(Z, t=K, criterion="maxclust")

fig, (axd, axs) = plt.subplots(1, 2, figsize=(12.5, 5.0))
fig.patch.set_facecolor("white")

# --- Left: dendrogram ---
# Color links to MATCH the k-cut labels so the two panels share a color scheme:
# a link is colored by its cluster only if every leaf beneath it is in that
# cluster; links above the cut are grey.
n = len(Xs)
ABOVE = "#B0B0B0"
leaf_color = {i: PASTELS[(labels[i] - 1) % len(PASTELS)] for i in range(n)}
link_color = {}
for i, (a, b) in enumerate(Z[:, :2].astype(int)):
    ca = link_color[a] if a >= n else leaf_color[a]
    cb = link_color[b] if b >= n else leaf_color[b]
    link_color[i + n] = ca if ca == cb else ABOVE
dendrogram(Z, ax=axd, leaf_font_size=8,
           link_color_func=lambda k: link_color[k])
axd.axhline(cut, ls="--", lw=1.6, color=EDGE)
axd.text(axd.get_xlim()[1], cut, f"  cut (k={K})", va="center", ha="left",
         fontsize=9, color=EDGE)
axd.set_title("Ward dendrogram of a 40-point subsample",
              fontsize=12, fontweight="bold", color=TEXT)
axd.set_xlabel("point index (leaves)", fontsize=10, color=TEXT)
axd.set_ylabel("merge distance (Ward)", fontsize=10, color=TEXT)
axd.tick_params(labelsize=8)

# --- Right: scatter colored by the k-cut ---
for c in range(1, K + 1):
    m = labels == c
    axs.scatter(Xs[m, 0], Xs[m, 1], s=60, color=PASTELS[(c - 1) % len(PASTELS)],
                edgecolors=EDGE, linewidths=0.5, label=f"cluster {c}")
axs.set_title(f"Same points, tree cut into k={K} clusters",
              fontsize=12, fontweight="bold", color=TEXT)
axs.set_xlabel("feature 1", fontsize=10, color=TEXT)
axs.set_ylabel("feature 2", fontsize=10, color=TEXT)
axs.tick_params(labelsize=9)
axs.legend(loc="lower right", fontsize=8, framealpha=0.9)
axs.set_axisbelow(True)
axs.grid(color="#ECECEC", lw=0.7)

fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "hierarchical-shared-data.png")
fig.savefig(out, dpi=110, bbox_inches="tight", facecolor="white")
print("wrote", os.path.abspath(out))
print(f"cut height={cut:.3f}, cluster sizes:",
      {int(c): int((labels == c).sum()) for c in range(1, K + 1)})
