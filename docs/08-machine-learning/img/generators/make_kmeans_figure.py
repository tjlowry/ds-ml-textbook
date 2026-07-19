"""k-Means (k=5) on the shared clustering dataset.

Illustrates the page's point: k-means partitions space by proximity to
centroids, so it clusters the convex Gaussian blobs cleanly but slices the two
interleaved moons straight through the middle — a centroid can't wrap a
non-convex shape.

Run:  python make_kmeans_figure.py
Writes: ../kmeans-shared-data.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

from shared_dataset import make_shared_data, PASTELS, ACCENT_RED, EDGE, TEXT, SEED

np.random.seed(SEED)

X, _ = make_shared_data()

k = 5
km = KMeans(n_clusters=k, n_init=10, random_state=SEED)
labels = km.fit_predict(X)
centers = km.cluster_centers_

fig, ax = plt.subplots(figsize=(7.0, 5.2))
fig.patch.set_facecolor("white")

for c in range(k):
    m = labels == c
    ax.scatter(X[m, 0], X[m, 1], s=26, color=PASTELS[c],
               edgecolors=EDGE, linewidths=0.4, label=f"cluster {c + 1}")

ax.scatter(centers[:, 0], centers[:, 1], marker="X", s=210,
           color=ACCENT_RED, edgecolors="white", linewidths=1.5,
           zorder=5, label="centroids")

ax.set_title("k-Means (k=5): clean on the blobs, wrong on the moons",
             fontsize=12, fontweight="bold", color=TEXT)
ax.set_xlabel("feature 1", fontsize=10, color=TEXT)
ax.set_ylabel("feature 2", fontsize=10, color=TEXT)
ax.tick_params(labelsize=9)
ax.legend(loc="lower right", fontsize=8, framealpha=0.9)
ax.set_axisbelow(True)
ax.grid(color="#ECECEC", lw=0.7)

fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "kmeans-shared-data.png")
fig.savefig(out, dpi=110, bbox_inches="tight", facecolor="white")
print("wrote", os.path.abspath(out))
