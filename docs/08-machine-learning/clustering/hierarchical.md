# Hierarchical Clustering

## Overview

**Hierarchical clustering** builds a tree (dendrogram) of nested clusters instead of a flat
partition. *Agglomerative* (bottom-up) starts with every point as its own cluster and
repeatedly merges the two closest clusters; the *linkage* rule defines "closest" —
single-link (nearest pair), complete-link (farthest pair), average, or Ward. You don't have
to commit to `k` in advance: cut the dendrogram at whatever height gives the number of
clusters you want.

I worked through this in ECEN 758 (Lecture 10) and implemented it in HW 3, including a
hand-worked single-link example on a small point set.

## How I did it

HW 3 uses both scikit-learn's `AgglomerativeClustering` and SciPy's `linkage` + `dendrogram`
so I could see the merge order, using L1 (Manhattan / cityblock) distance and single linkage:

```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

# flat labels
clustering = AgglomerativeClustering(metric="l1", linkage="single").fit(data)

# the tree itself, to read the merge heights
Z = linkage(data, method='single', metric='cityblock')
dendrogram(Z, labels=['a','b','c','d','e','f','g','h','i','j','k'])
```

Source: `course-files/appendix/Homework/ecen758_hw/ecen758_hw3.ipynb`

Plotting the dendrogram was the point of the exercise: the y-axis (merge distance) shows
*when* clusters join, so a big vertical gap tells you where to cut for a natural number of
clusters.

## Gotchas

- **Linkage choice changes everything.** Single-link chains points together and is prone to
  "stringy" clusters; complete/Ward give more compact ones. The metric (L1 vs L2) matters
  just as much.
- **It's O(n²) or worse.** Agglomerative clustering compares all pairs — fine for the
  11-point homework, painful for large datasets.
- **The cut is a human decision.** The algorithm gives you the whole tree; *you* pick the
  height/`k`. Read it off the dendrogram's largest gap.
- **No reassignment.** Once two clusters merge they never split — an early bad merge is
  permanent (the opposite tradeoff from k-means, which re-shuffles every iteration).

## References

- ECEN 758 Lecture 10 — Hierarchical Clustering (local:
  `course-files/08-machine-learning/758 Lec 10 Hierarchical Clustering.pdf`).
  Instructor-copyrighted; concept summary only.
