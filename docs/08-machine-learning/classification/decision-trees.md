# Decision Trees

## Overview

A **decision tree** splits the feature space with a sequence of yes/no questions, choosing
at each node the split that most reduces impurity (Gini or entropy). The result is a
flowchart you can read top to bottom, which makes trees the most *interpretable* supervised
model — you can literally trace why a prediction was made. The cost is variance: a single
deep tree overfits easily, which is exactly what motivates the
[random forest](random-forests.md) on the next page.

I learned tree induction in ECEN 758 (Lecture 13) and built classification trees in my
DS 250 (BYU-Idaho) client report predicting whether a house was built before 1980.

## How I did it

In the DS 250 project I compared a `DecisionTreeClassifier` and a `RandomForestClassifier`
on the same feature set. The tree is the interpretable baseline:

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

feature_cols = ['gartype_Det', 'arcstyle_ONE-STORY', 'condition_Good', 'numbaths',
                'arcstyle_TWO-STORY', 'stories', 'livearea', 'quality_B', 'quality_C']
X = df[feature_cols]
y = df.before1980

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)

clf = DecisionTreeClassifier().fit(X_train, y_train)
print("Accuracy:", metrics.accuracy_score(y_test, clf.predict(X_test)))
```

Source: `course-files/08-machine-learning/random_forest_classifier.qmd` (DS 250, BYU-Idaho)

I chose the feature set by correlation with the target — keeping only columns whose
correlation with `yrbuilt` was above +0.2 or below −0.2 — so the tree split on features
that actually separated pre-/post-1980 homes (number of stories, living area, bathroom
count).

The reason a tree is the most *interpretable* model is that you can read it as a flowchart
and watch the yes/no splits carve feature space into rectangles. Fitting a small depth-3
tree on two interpretable iris features (petal length and petal width) shows both halves
side by side:

![Two-panel figure. Left panel: a depth-3 decision tree fit on iris, drawn as a flowchart of nodes labeled with their split threshold, sample counts, class counts, and majority class, with nodes tinted blue for Setosa, orange for Versicolor, and green for Virginica. Right panel: the same tree's decision regions in petal length vs petal width space, shown as axis-aligned rectangular pastel blocks in the matching colors with the iris data overlaid.](../img/decision-tree-and-regions.png)

Each split in the flowchart (left) is one horizontal or vertical cut in feature space
(right): `petal width <= 0.8` peels off the Setosa block along the bottom, and the deeper
splits chop the Versicolor/Virginica overlap into rectangles. That axis-aligned,
rectangles-only geometry is the second gotcha below.

## Gotchas

- **A single tree overfits.** Left unconstrained it grows until every leaf is pure, which
  memorizes the training set. Constrain depth / min-samples, or move to an ensemble.
- **Splits are axis-aligned and greedy.** Trees carve the space into rectangles and never
  reconsider an earlier split, so they struggle with diagonal boundaries a linear model
  would nail.
- **Correlation-based feature selection is a blunt tool.** It worked for this project
  (0.90 accuracy), but it only sees linear pairwise relationships — it can drop a feature
  that's only useful in interaction with another.

## References

- ECEN 758 Lecture 13 — Decision Tree Classification (local:
  `course-files/08-machine-learning/758 Lec 13 Decision Tree Classification.pdf`).
  Instructor-copyrighted; concept summary only.
