# k-Means

## Overview

**k-Means** is the workhorse of representative (partitional) clustering: pick `k`, then
alternate between assigning each point to its nearest centroid and recomputing each
centroid as the mean of its members, until assignments stop changing. It's fast and simple
but assumes roughly spherical, equally-sized clusters and needs `k` up front.

That spherical assumption is easiest to appreciate by breaking it. Below, plain
k-means (`k=5`) runs on an illustrative synthetic mix of three Gaussian blobs, two
interleaved half-moons, and a little uniform noise. Because it partitions space
purely by proximity to the nearest centroid, it recovers the convex blobs cleanly
but slices straight through the two moons — no single centroid can wrap a crescent:

![k-Means with k=5 on a synthetic dataset of three Gaussian blobs plus two interleaved half-moons: the three blobs are each recovered as a clean pastel cluster, while the two moons are cut through the middle by the cluster boundaries, with red X markers at the five centroids](../img/kmeans-shared-data.png)

*Illustrative synthetic demo built for this page. The same seeded dataset is
re-used by the [DBSCAN](density-clustering.md), [GMM](gmm-em.md), and
[hierarchical](hierarchical.md) pages so you can compare how each method handles
the identical blobs-plus-moons.*

I studied representative clustering in ECEN 758 (Lectures 6–7). In HW 3 I used the
**bisecting** k-means variant — which repeatedly splits the worst cluster in two — rather
than plain Lloyd's k-means, so my hands-on code is the bisecting version; the vanilla
algorithm itself I only worked through in the lecture.

## How I did it

In HW 3 I ran `BisectingKMeans` on a small 2-D point set and plotted the four resulting
clusters:

```python
from sklearn.cluster import BisectingKMeans

bisect_kmeans = BisectingKMeans(n_clusters=4, random_state=0)
labels = bisect_kmeans.fit_predict(data)   # data: 11 hand-placed 2-D points
```

Source: `course-files/appendix/Homework/ecen758_hw/ecen758_hw3.ipynb`

Bisecting k-means is a hybrid of k-means and divisive hierarchical clustering: start with
everything in one cluster, then keep splitting the cluster with the highest SSE using
2-means until you have `k`. It tends to produce more balanced clusters than a single global
k-means run.

## Course notebook

The ECEN 758 Lecture 6 (Representative Clustering I) slides link a Colab walkthrough of
k-means:
<https://colab.research.google.com/drive/1EFnFGZr0A4NLRKww34bWg1fY5_vrF0ZK>
(URL extracted from the lecture PDF).

## Gotchas

- **You have to pick `k`.** There's no right answer from the algorithm — use the elbow
  method or a [silhouette](density-clustering.md) score to compare candidates.
- **Initialization matters.** Plain k-means can land in a bad local optimum; `k-means++`
  seeding (and bisecting's split strategy) reduce that. Pin `random_state` for
  reproducibility.
- **Spherical-cluster assumption.** k-Means uses Euclidean distance to a mean, so it fails
  on elongated or non-convex clusters — that's where
  [density-based](density-clustering.md) or [GMM](gmm-em.md) methods take over.
- **Scale-sensitive.** Standardize features first, or the largest-magnitude feature defines
  the clusters.

## References

- ECEN 758 Lectures 6–7 — Representative Clustering I & II (local:
  `course-files/08-machine-learning/758 Lec 06 Representative Clustering I.pdf`,
  `758 Lec 07 Representative Clustering II.pdf`). Instructor-copyrighted; concept summary
  only.
