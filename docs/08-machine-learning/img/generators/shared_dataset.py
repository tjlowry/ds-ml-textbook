"""Shared synthetic 2-D dataset for the clustering-chapter figures.

ONE dataset, four lenses. Every clustering generator in this folder
(kmeans, density-clustering, gmm-em, hierarchical) imports `make_shared_data()`
from here so the same points are re-used across pages — the reader sees a single
toy dataset examined by k-means, DBSCAN, a GMM, and a dendrogram in turn.

The dataset deliberately mixes cluster *shapes* so the different algorithms'
strengths and weaknesses are visible on identical data:

  * 3 compact Gaussian blobs   -> convex, k-means-friendly
  * 2 interleaved half-moons    -> non-convex, breaks centroid methods
  * a sprinkle of uniform noise -> points DBSCAN should flag as noise

Everything is seeded, so re-running any generator reproduces byte-identical
coordinates.

Illustrative synthetic demo built for the textbook — not coursework data.
"""
import numpy as np
from sklearn.datasets import make_blobs, make_moons

SEED = 7

# House palette (kept here so every generator shares it)
PASTELS = ["#BCD8EE", "#F6D5B3", "#CBE6C4", "#E6C9E3", "#D9D2C5"]
ACCENT_RED = "#C0392B"
ACCENT_GREEN = "#1E7A34"
NOISE_GREY = "#9AA0A6"
EDGE = "#4A4A4A"
TEXT = "#222222"


def make_shared_data():
    """Return (X, kind) where X is (N, 2) and `kind` labels the generative
    source of each point: 0/1/2 = blobs, 3/4 = the two moons, 5 = uniform noise.
    `kind` is only for building the figures (e.g. honest captions); the
    clustering algorithms never see it."""
    rng = np.random.RandomState(SEED)

    # --- 3 Gaussian blobs, placed in the upper-left region ---
    blob_centers = np.array([[-5.2, 4.6], [-2.0, 5.6], [-3.6, 2.2]])
    Xb, yb = make_blobs(
        n_samples=[70, 70, 70],
        centers=blob_centers,
        cluster_std=0.45,
        random_state=SEED,
    )

    # --- 2 interleaved moons, placed to the lower-right and scaled up ---
    Xm, ym = make_moons(n_samples=180, noise=0.06, random_state=SEED)
    Xm = Xm * np.array([2.6, 2.6])           # scale
    Xm = Xm + np.array([2.4, -1.2])          # translate away from the blobs

    # --- uniform noise sprinkled across the whole scene ---
    n_noise = 22
    lo = np.array([-7.0, -3.5])
    hi = np.array([8.5, 7.5])
    Xn = rng.uniform(lo, hi, size=(n_noise, 2))

    X = np.vstack([Xb, Xm, Xn])
    kind = np.concatenate([
        yb,                       # 0,1,2
        ym + 3,                   # 3,4
        np.full(n_noise, 5),      # 5
    ])

    # Shuffle so plotting order / algorithm input isn't grouped by source.
    order = rng.permutation(len(X))
    return X[order], kind[order]


if __name__ == "__main__":
    X, kind = make_shared_data()
    print("shared dataset:", X.shape, "points")
    for k, name in enumerate(["blob0", "blob1", "blob2", "moonA", "moonB", "noise"]):
        print(f"  {name}: {(kind == k).sum()}")
