"""DBSCAN on the shared clustering dataset.

Same points as the k-means figure, but density-based clustering recovers the
non-convex moons as whole clusters and flags the sprinkled uniform points as
noise (drawn as red x's). eps / min_samples are chosen so this actually happens
on the shared data — see the printed cluster/noise counts, which the page
caption reports.

Run:  python make_dbscan_figure.py
Writes: ../dbscan-shared-data.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN

from shared_dataset import (make_shared_data, PASTELS, ACCENT_RED, EDGE, TEXT,
                            NOISE_GREY, SEED)

np.random.seed(SEED)

X, _ = make_shared_data()

EPS = 0.55
MIN_SAMPLES = 5
db = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES).fit(X)
labels = db.labels_

cluster_ids = sorted(c for c in set(labels) if c != -1)
n_clusters = len(cluster_ids)
n_noise = int((labels == -1).sum())
print(f"eps={EPS} min_samples={MIN_SAMPLES} -> {n_clusters} clusters, {n_noise} noise points")

fig, ax = plt.subplots(figsize=(7.0, 5.2))
fig.patch.set_facecolor("white")

for i, c in enumerate(cluster_ids):
    m = labels == c
    ax.scatter(X[m, 0], X[m, 1], s=26, color=PASTELS[i % len(PASTELS)],
               edgecolors=EDGE, linewidths=0.4, label=f"cluster {i + 1}")

noise = labels == -1
ax.scatter(X[noise, 0], X[noise, 1], marker="x", s=55,
           color=ACCENT_RED, linewidths=1.6, zorder=5,
           label=f"noise ({n_noise})")

ax.set_title(f"DBSCAN (eps={EPS}, min_samples={MIN_SAMPLES}): "
             f"{n_clusters} clusters + noise",
             fontsize=12, fontweight="bold", color=TEXT)
ax.set_xlabel("feature 1", fontsize=10, color=TEXT)
ax.set_ylabel("feature 2", fontsize=10, color=TEXT)
ax.tick_params(labelsize=9)
ax.legend(loc="lower right", fontsize=8, framealpha=0.9)
ax.set_axisbelow(True)
ax.grid(color="#ECECEC", lw=0.7)

fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "dbscan-shared-data.png")
fig.savefig(out, dpi=110, bbox_inches="tight", facecolor="white")
print("wrote", os.path.abspath(out))
