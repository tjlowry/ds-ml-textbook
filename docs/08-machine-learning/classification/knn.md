# k-Nearest Neighbors

## Overview

**k-Nearest Neighbors (kNN)** classifies a point by looking at the `k` closest training
points and taking a majority vote. There is no "training" beyond storing the data — all
the work happens at prediction time, which makes it the canonical *lazy*, non-parametric,
instance-based method. It is a strong baseline when the decision boundary is irregular and
the feature space isn't too high-dimensional.

I studied kNN in ECEN 758 (Lecture 12, Bayesian and Nearest-Neighbor Classification) and
used the scikit-learn implementation in the HW 3 classification exercise, but I have not
written a from-scratch kNN — the distance loop and vote are library calls in my work.

## How I did it

In ECEN 758 HW 3 I ran `KNeighborsClassifier` alongside Gaussian Naive Bayes on a labeled
dataset, split by row order, and compared them with confusion matrices and a full metrics
report:

```python
from sklearn.neighbors import KNeighborsClassifier

X_train, X_test = X[:140], X[140:]
y_train, y_test = y[:140], y[140:]

knn = KNeighborsClassifier()          # default k = 5
knn.fit(X_train, y_train)
y_pred_test_knn = knn.predict(X_test)
# evaluated with confusion_matrix + accuracy/precision/recall/f1
```

Source: `course-files/appendix/Homework/ecen758_hw/ecen758_hw3.ipynb`

This is applied use, not a derivation: the concept understanding (why `k` trades bias for
variance, why the distance metric matters) comes from the lecture, and the fit/predict is
scikit-learn.

That bias-variance trade-off is easiest to *see* on a synthetic two-class problem. The
figure below fits `KNeighborsClassifier` on the same seeded two-moons data at two values of
`k` (not from my coursework — a demo built to isolate the effect):

![Two-panel figure of kNN decision boundaries on the same synthetic two-moons dataset. Left panel, k equals 1: a jagged boundary with small isolated islands that wraps individual points, the overfit case. Right panel, k equals 15: a smooth boundary that ignores individual noisy points and follows the overall two-class shape.](../img/knn-k1-vs-k15.png)

At `k=1` every point is its own neighbor, so the boundary is jagged and carves out little
islands around noise — high variance. At `k=15` the vote averages over more neighbors and
the boundary smooths out. That is the dial the first gotcha below is about.

## Gotchas

- **Scale first.** kNN is pure distance, so an unscaled large-magnitude feature dominates
  the neighbor calculation. Standardize before fitting.
- **`k` is a bias-variance dial.** `k=1` overfits (each point is its own neighbor); large
  `k` oversmooths. The default is 5.
- **It doesn't scale to big/high-dimensional data.** Every prediction scans the training
  set, and distances become meaningless as dimensionality grows (curse of dimensionality).
- **Class imbalance skews the vote.** A dominant class wins majority votes near the
  boundary; distance-weighting or resampling helps.

## References

- ECEN 758 Lecture 12 — Bayesian and Nearest-Neighbor Classification (local:
  `course-files/08-machine-learning/758 Lec 12 Bayesian and Nearest Neighbor Classification.pdf`).
  Instructor-copyrighted; concept summary only.
