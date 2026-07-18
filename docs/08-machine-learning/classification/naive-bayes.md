# Naive Bayes

## Overview

**Naive Bayes** applies Bayes' theorem with a strong ("naive") independence assumption:
it treats every feature as conditionally independent given the class. That assumption is
almost never literally true, yet the classifier is fast, needs little data, and is a
famously good baseline for text/spam problems. **Gaussian** Naive Bayes — the variant I
used — models each continuous feature as a per-class normal distribution.

I studied this in ECEN 758 (Lecture 12) and applied `GaussianNB` in HW 3; I have not
implemented the probability tables from scratch. See the related derivation of Bayes'
theorem in the [Statistics chapter](../../03-statistics/probability/bayes.md).

## How I did it

In HW 3 I fit `GaussianNB` and kNN on the same split and compared them. Naive Bayes is a
one-liner to fit and predict:

```python
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix, classification_report

gnb = GaussianNB()
gnb.fit(X_train, y_train)
y_pred_test_gnb = gnb.predict(X_test)

print(classification_report(y_test, y_pred_test_gnb))
```

Source: `course-files/appendix/Homework/ecen758_hw/ecen758_hw3.ipynb`

The interesting part of the exercise wasn't the API call but the comparison: reading the
train vs test confusion matrices side by side to see where the independence assumption
cost Naive Bayes relative to kNN on that dataset.

## Course notebook

The ECEN 758 Lecture 12 slides link an external worked example of a Naive Bayes spam
classifier:
<https://github.com/Midvel/medium_jupyter_notes/blob/master/naive_bayes_filter/bayes-classificator.ipynb>
(URL extracted from the lecture PDF).

## Gotchas

- **Independence is a lie that often works.** Correlated features get double-counted, which
  can make probability estimates overconfident even when the argmax class is still right.
- **Gaussian NB assumes normal features.** Heavily skewed features break the per-class
  normal fit; transform them first or use a different NB variant.
- **Zero-frequency problem (categorical NB).** An unseen category gives a zero likelihood
  that wipes out the whole product — Laplace/additive smoothing fixes it. (Not an issue for
  the Gaussian variant, which is why I reached for it on continuous features.)

## References

- ECEN 758 Lecture 12 — Bayesian and Nearest-Neighbor Classification (local:
  `course-files/08-machine-learning/758 Lec 12 Bayesian and Nearest Neighbor Classification.pdf`).
  Instructor-copyrighted; concept summary only.
