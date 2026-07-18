# Cross-Validation & Splitting

## Summary

An evaluation number is only honest if the data behind it was genuinely unseen. That comes down
to two disciplines: **hold out a test set the model never trains on**, and when you tune
hyperparameters, **don't measure yourself on the data you tuned on**. Cross-validation is the
tool for the second problem — instead of burning a single validation split, you rotate through
*k* folds so every row serves as validation once, and average the score.

The foundational treatment — simple `train_test_split`, three-way train/validation/test splits,
`RandomizedSearchCV(cv=10)` for early stopping vs. final scoring, and the fit-scaler-on-train-only
rule — already lives in
[Machine Learning → ML Overview & Workflow](../08-machine-learning/fundamentals/overview.md#how-i-did-it-the-split-that-makes-validation-honest).
This page points there and adds the one CV variant that page doesn't show: **cross-validation baked
directly into a regularized-regression fit** to pick the penalty strength.

## Where the splitting discipline already lives

The [ch08 overview](../08-machine-learning/fundamentals/overview.md) covers, with real project code:

- A single `train_test_split` on the DS 250 random-forest project.
- A **three-way** train / validation / test split on the STAT 654 XGBoost project, where the
  validation set drives early stopping and the test set is scored exactly once.
- `RandomizedSearchCV(..., cv=10)` — random-search hyperparameter tuning with 10-fold CV inside
  the search.
- The gotchas: fit the scaler on train only, pin `random_state`, never score on tuning data, and
  let the metric follow the setting.

I'm not repeating those — start there for the core discipline.

## How I did it — cross-validation inside the model fit

The ch08 examples use CV as a *separate* tuning loop. The other common shape is CV **built into
the estimator**: scikit-learn's `RidgeCV` and `ElasticNetCV` take a grid of penalty strengths and
internally run k-fold CV to pick the best one during `.fit()`. In my STAT 650 final I used both to
select the regularization strength over a 10-fold split:

```python
import numpy as np
from sklearn.linear_model import RidgeCV, ElasticNetCV

# Ridge: 200 candidate alphas, 10-fold CV picks the best
alphas = np.logspace(-3, 3, 200)
ridge_cv = RidgeCV(alphas=alphas, cv=10, scoring="neg_mean_squared_error")
ridge_cv.fit(X_train_scaled, y_train)

# Elastic Net: a 2-D grid over alpha AND the l1/l2 mix ratio, again 10-fold
elastic_cv = ElasticNetCV(alphas=[0.001, 0.01, 0.1, 1, 10, 100],
                          l1_ratio=[0.1, 0.3, 0.5],
                          cv=10, max_iter=10000, random_state=42)
elastic_cv.fit(X_train_scaled, y_train)
```

Source: `course-files/appendix/Homework/stat650_hw/final/STAT650-F25-Final.ipynb` (my own code)

The idea is the same as a `GridSearchCV` sweep — try a grid of penalties, score each by
cross-validation, keep the winner — but the `...CV` estimators fold it into one object. `RidgeCV`
searches a 1-D grid of `alpha`; `ElasticNetCV` searches a 2-D grid over `alpha` *and* `l1_ratio`
(how much L1 vs. L2 penalty to mix). Both then expose the chosen values (`ridge_cv.alpha_`,
`elastic_cv.l1_ratio_`) and behave like a fitted model. The
[regression-metrics table](regression-and-forecast-metrics.md#how-i-did-it-a-plain-regression-model-bake-off)
that compares these fits against plain OLS and polynomial regression is on the previous page — the
CV here is what makes the ridge/elastic rows a fair, tuned comparison rather than an untuned guess.

## Gotchas

- **CV picks the hyperparameter; the test set still judges the model.** The `cv=10` inside
  `RidgeCV` chooses `alpha` — it does **not** give you an honest generalization estimate for the
  final model. You still score the fitted estimator on a held-out test set the CV never touched.
- **Scale inside the fold, not before it.** Fitting a `StandardScaler` on the full training set and
  *then* cross-validating leaks each fold's validation statistics into its own training — a subtle
  version of the [leakage](leakage-patterns.md) problem. A `Pipeline` that scales inside each fold
  is the clean fix; my exam code scaled once on the training split, which is acceptable for a
  single split but would leak across folds if you're not careful.
- **The grid has to be wide enough to bracket the optimum.** `RidgeCV` can only return an `alpha`
  you gave it. If the best value sits at the edge of your `np.logspace` range, widen the range —
  the "best" is otherwise just the least-bad boundary point.
- **`random_state` matters for CV too.** Fold assignment is a random split. Pin the seed (as the
  `ElasticNetCV` call does) so the chosen hyperparameters are reproducible, not an artifact of how
  the folds happened to land.
