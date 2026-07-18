# Random Forests

## Overview

A **random forest** is an ensemble of decision trees where each tree is trained on a
bootstrap sample of the rows and a random subset of the features at each split. Averaging
their votes cancels the high variance of any single [tree](decision-trees.md) while keeping
most of the signal — it's *bagging* (bootstrap aggregating) specialized to trees. It is my
default first model on tabular data: strong out of the box, hard to overfit badly, and it
hands you feature importances for free.

I used random forests in the DS 250 house-age project and again in our ECEN 758 CIFAR-100
group project as a classical-ML baseline against the CNN.

## How I did it

The DS 250 client report's final model was a `RandomForestClassifier`, which cleared the
project's 90% accuracy bar:

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score

clf = RandomForestClassifier().fit(X_train, y_train)
y_pred = clf.predict(X_test)

# Accuracy: 0.9042   Precision: 0.925   Recall: 0.916
print("Precision:", round(precision_score(y_test, y_pred), 4))
print("Recall:",    round(recall_score(y_test, y_pred), 4))
```

Source: `course-files/08-machine-learning/random_forest_classifier.qmd` (DS 250, BYU-Idaho)

**Random forest as a baseline on images.** In our ECEN 758 group project we ran a random
forest on top of HOG (Histogram-of-Oriented-Gradients) features as a deliberately simple
starting point before the CNN. With 100 trees it reached about **22% accuracy** on
CIFAR-100 — a real signal over the 1% random-guess rate for 100 classes, and a useful floor
that the [CNN](../deep-learning/cnns.md) then more than doubled.

Source: our ECEN 758 CIFAR-100 group project report
(`course-files/appendix/Homework/ecen758_hw/group_project/CNN_draft2.pdf`)

!!! note "Full case study"
    This forest was one of three approaches we compared on CIFAR-100. The whole
    story — EDA, the CNN that beat it, and the honest lessons — is on the
    [CIFAR-100 case-study page](../case-study-cifar100.md).

## Gotchas

- **Forests fix variance, not bias.** Averaging trees tames overfitting, but if every tree
  is too shallow to capture the pattern, the forest underfits too. It's not magic.
- **Feature engineering still matters on images.** A forest can't see raw pixels usefully —
  the 22% on CIFAR-100 came *after* extracting HOG features. That preprocessing step is why
  a CNN (which learns its own features) wins.
- **Importances can mislead.** Impurity-based importances inflate high-cardinality features;
  permutation importance (see [XGBoost](../ensembles/xgboost.md)) is the more honest read.
- **Defaults are strong but not tuned.** The DS 250 forest used mostly defaults and still
  hit 90%; on harder problems `n_estimators`, `max_depth`, and `max_features` are worth a
  search.

## References

- ECEN 758 Lecture 13 — Decision Tree Classification (bagging/forest concepts) (local:
  `course-files/08-machine-learning/758 Lec 13 Decision Tree Classification.pdf`).
  Instructor-copyrighted; concept summary only.
