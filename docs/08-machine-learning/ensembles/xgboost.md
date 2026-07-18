# XGBoost

## Overview

**XGBoost** is a fast, regularized implementation of gradient-boosted decision trees. It
builds trees sequentially, each fitting the residual errors of the ensemble so far, with
built-in L1/L2 regularization, column/row subsampling, and early stopping to keep it from
overfitting. It's my go-to model for tabular regression and classification when I want
accuracy over interpretability.

I used XGBoost as the ML model in a STAT 654 apartment-rent regression project (with a full
hyperparameter search and SHAP interpretation) and again in the PySpark
[ensemble](bagging-boosting.md) capstone.

## How I did it

The STAT 654 project predicts (log) rent from census-tract features. The workflow is a
`RandomizedSearchCV` over a wide grid, then a final model with early stopping on a held-out
validation set:

```python
from xgboost import XGBRegressor
from sklearn.model_selection import RandomizedSearchCV

y = np.log(df["price_overall"])          # model on the log scale
X = pd.get_dummies(df[[...]], drop_first=True)

param_dist = {
    "n_estimators": [100, 200, 300, 500, 800, 1000, 1200],
    "max_depth": [2, 3, 4, 5, 6],
    "learning_rate": [0.01, 0.03, 0.05, 0.1],
    "subsample": [0.6, 0.7, 0.8, 0.9, 1.0],
    "colsample_bytree": [0.6, 0.7, 0.8, 0.9, 1.0],
    "min_child_weight": [1, 3, 5, 7, 10],
    "gamma": [0, 0.1, 0.3, 0.5, 1.0],
    "reg_alpha": [0, 0.01, 0.1, 1, 5, 10],
    "reg_lambda": [0.1, 1, 5, 10, 20, 50, 100],
}

search = RandomizedSearchCV(XGBRegressor(objective="reg:squarederror", random_state=42),
                            param_dist, n_iter=40, scoring="neg_mean_squared_error",
                            cv=10, random_state=42, n_jobs=-1)
search.fit(X_train, y_train)
```

Then refit the best params with **early stopping** so it uses only as many trees as actually
help:

```python
best_model = XGBRegressor(objective="reg:squarederror", random_state=42,
                          early_stopping_rounds=50, **search.best_params_)
best_model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
print(f"Trees used: {best_model.best_iteration + 1} / {search.best_params_['n_estimators']}")
```

Source: `~/Projects/school/tamu-grad/stat654/presentation/654Project2.ipynb`

**Interpretation.** Because gradient boosting is a black box, the project reports three
complementary importance views — the model's built-in `feature_importances_`,
scikit-learn's `permutation_importance`, and SHAP values — rather than trusting any single
one:

```python
from sklearn.inspection import permutation_importance
import shap

perm = permutation_importance(best_model, X_test, y_test, n_repeats=10, random_state=42)
shap_values = shap.Explainer(best_model)(X_test)
shap.summary_plot(shap_values, X_test, max_display=10)
```

Source: `~/Projects/school/tamu-grad/stat654/presentation/654Project2.ipynb`

## Gotchas

- **Model the target on the right scale.** Rent is right-skewed, so I trained on
  `np.log(price)` and exponentiated predictions back — RMSE/MAE were computed in dollars,
  R² on the log scale. Mixing scales silently corrupts the metrics.
- **Early stopping needs its own set.** The validation set that gates `early_stopping_rounds`
  must be separate from both the CV folds and the final test set, or the tree count is tuned
  on data you then report on.
- **`feature_importances_` alone lies.** Gain-based importance favors high-cardinality
  splits; cross-checking with permutation importance and SHAP is what makes the "which
  features matter" story trustworthy.
- **Regularization is why it generalizes.** `reg_alpha`, `reg_lambda`, `gamma`,
  `min_child_weight`, and subsampling are all in the search for a reason — un-regularized
  boosting overfits fast.
