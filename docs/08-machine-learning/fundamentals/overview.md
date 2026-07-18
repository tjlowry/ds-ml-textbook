# ML Overview & Workflow

## Overview

Machine learning splits cleanly into two settings, and almost every page in this chapter
lives in one of them:

- **Supervised** — you have labels (`y`) and learn a mapping `X → y`. Classification
  (discrete `y`) and regression (continuous `y`). Trees, random forests, SVMs, XGBoost,
  and most neural nets here are supervised.
- **Unsupervised** — no labels; you find structure. Clustering (k-means, hierarchical,
  density, GMM) and dimensionality reduction (PCA) are the unsupervised topics.

The ECEN 758 framing I learned it under adds a third practical bucket — **pattern mining**
(frequent itemsets / association rules) and **graph methods** (PageRank) — which are
covered on their own pages.

## The bias-variance tradeoff

Every model choice on the following pages is really a position on one axis: how much the
model is allowed to flex.

- **High bias / underfit** — the model is too simple to capture the signal (a linear
  boundary on a spiral). Train and test error are both high and close.
- **High variance / overfit** — the model memorizes training noise (an unpruned tree, a
  huge MLP on little data). Train error is tiny, test error is large.

The whole game is finding the middle. It shows up concretely on later pages: `max_depth`
and `min_child_weight` in [XGBoost](../ensembles/xgboost.md), the number of trees in a
[random forest](../classification/random-forests.md), and the
[dropout](../deep-learning/neural-network-fundamentals.md) sweep in the MLP project are all
knobs that trade variance for bias.

*Concept framing follows ECEN 758 lectures (Peeples, TAMU); the bias-variance decomposition
itself is standard.*

## How I did it — the split that makes validation honest

The one habit that carries across every supervised project below is: **hold out data the
model never trains on, and only trust the score you get there.** In my DS 250 tree project
it is a single `train_test_split`:

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=1)
clf = RandomForestClassifier().fit(X_train, y_train)
accuracy = metrics.accuracy_score(y_test, clf.predict(X_test))
```

Source: `course-files/08-machine-learning/random_forest_classifier.qmd` (DS 250, BYU-Idaho)

By the STAT 654 XGBoost project the same idea is a **three-way** split — train / validation
/ test — where the validation set drives early stopping and the test set is touched exactly
once, plus cross-validation inside the hyperparameter search:

```python
X_train_full, X_test, y_train_full, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train_full, y_train_full, test_size=0.20, random_state=42)
# RandomizedSearchCV(..., cv=10) tunes on X_train; X_val gates early stopping; X_test scored once
```

Source: `~/Projects/school/tamu-grad/stat654/presentation/654Project2.ipynb`

## How I did it — preprocessing that has to happen first

Distance- and gradient-based models care about feature scale. ECEN 758 HW 1 is where I
worked through the two standard scalers by hand on an age/weight table:

```python
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Min-max: squash each feature to [0, 1]
scaled = MinMaxScaler().fit(df).transform(df)
# Standardize: zero mean, unit variance (z-scores)
standardized = StandardScaler().fit(df).transform(df)
```

Source: `course-files/appendix/Homework/ecen758_hw/HW 1/ECEN758_HW1.ipynb`

The same homework also covered discretizing continuous features into bins (`pd.cut`),
building a contingency table, and testing association with a chi-squared test
(`scipy.stats.chi2_contingency`) — the EDA groundwork that precedes any model.

## Gotchas

- **Scale before you fit distance/gradient models, not after.** kNN, SVM, k-means, PCA,
  and neural nets are all scale-sensitive; trees and forests are not. Fit the scaler on
  **train only**, then apply to test — fitting on the full set leaks test statistics.
- **`random_state` is not optional.** Every split and every stochastic model here pins a
  seed so a re-run reproduces the same numbers. Without it, "my accuracy went up" is noise.
- **Never score on data you tuned on.** The DS 250 project scores on a single held-out
  split; the STAT 654 project separates the validation set (early stopping) from the test
  set (final number) so the reported score isn't optimistic.
- **The metric follows the setting.** Accuracy/precision/recall for classification, RMSE/R²
  for regression, silhouette for clustering — picking the wrong one flatters the wrong
  model.
