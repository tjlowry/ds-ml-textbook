# Density-Based Clustering

## Overview

**Density-based clustering** defines clusters as connected regions of high point density,
separated by sparse regions. Unlike k-means it doesn't assume spherical clusters, doesn't
need `k` specified up front, and can label low-density points as noise. **DBSCAN** is the
canonical example (core points, reachability, an `eps` radius); **Mean Shift** — the variant
I used — instead slides a kernel window uphill toward the densest point until every window
converges to a mode, and the number of clusters falls out of the bandwidth.

The payoff of not assuming spherical clusters shows up on the same synthetic
dataset the [k-means page](kmeans.md) slices apart. Here DBSCAN (`eps=0.55`,
`min_samples=5`) recovers all five structures — the three Gaussian blobs *and* the
two non-convex moons — as whole clusters, and flags 11 of the sparse points as
noise (red x's) rather than forcing them into a cluster:

![DBSCAN on the shared synthetic dataset with eps=0.55 and min_samples=5: the two interleaved half-moons are each recovered as a complete crescent-shaped cluster alongside the three Gaussian blobs, for five clusters total, while eleven low-density points are marked as noise with red x markers](../img/dbscan-shared-data.png)

*Illustrative synthetic demo built for this page. Those parameters were tuned
until DBSCAN genuinely produced the five-clusters-plus-noise result shown; a
larger `eps` starts merging the moon with a neighboring blob.*

I studied density clustering in ECEN 758 (Lecture 11) and implemented Mean Shift in HW 3
on the iris petals.

## How I did it

HW 3 fits `MeanShift` on two iris features, first with a hand-chosen bandwidth and then with
scikit-learn's bandwidth estimator, scoring each with the silhouette coefficient:

```python
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.metrics import silhouette_score

X = iris.data[:, 2:4]           # petal length, petal width

ms = MeanShift(bandwidth=1).fit(X)
print(silhouette_score(X, ms.labels_))

# let the data choose the bandwidth
bw = estimate_bandwidth(X)
ms_est = MeanShift(bandwidth=bw).fit(X)
print(f"bw≈{bw:.2f}", silhouette_score(X, ms_est.labels_))
```

Source: `course-files/appendix/Homework/ecen758_hw/ecen758_hw3.ipynb`

The exercise was really about the **bandwidth**: it's Mean Shift's one critical knob (the
density-based analog of k-means' `k`). Comparing silhouette scores between a fixed `bw=1`
and the estimated bandwidth showed how sensitive the cluster count is to that choice.

## Gotchas

- **Bandwidth / `eps` is the whole ballgame.** Too small → everything is noise or its own
  cluster; too large → everything merges. `estimate_bandwidth` is a reasonable starting
  point but not gospel.
- **Struggles with varying density.** A single global radius can't handle clusters that are
  dense in one region and sparse in another — a known DBSCAN/Mean Shift weakness.
- **Silhouette is the referee.** Because the cluster count isn't fixed, I leaned on the
  silhouette score to compare parameterizations objectively rather than eyeballing plots.
- **Mean Shift is slow.** Every point climbs to a mode; it's fine on iris, heavy on large
  datasets.

## References

- ECEN 758 Lecture 11 — Density-Based Clustering (local:
  `course-files/08-machine-learning/758 Lec 11 Density_based Clustering (1).pdf`).
  Instructor-copyrighted; concept summary only.
