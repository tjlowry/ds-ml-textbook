# Regression & Forecast Metrics

## Summary

For a continuous target, the whole evaluation vocabulary is: how far off am I on average
(MAE), how much do big misses hurt (RMSE / MSE), what fraction of the variance did I explain
(R²), and — when the model has many predictors — is that R² inflated just by adding columns
(adjusted R²). These are the same metrics whether or not there's a time axis; the time-series
versions add scale-free and baseline-relative variants on top.

Rather than re-derive them, this page points at the two places the derivations already live and
adds the one example the book didn't yet have: a **plain, non-time-series multi-model regression
comparison** — the reusable "compare N models in one table" pattern.

## Where the derivations already live

**Forecasting context — the full treatment.** MAE, RMSE, MSE, MAPE, sMAPE, relative MAE, and
forecast skill scores are all derived, with sklearn one-liners and a "choose the right metric"
decision table, in
[Time Series → Evaluation Metrics](../09-time-series-forecasting/evaluation/metrics.md). That
page also carries the production story: why my
[distribution demand-forecasting work](../09-time-series-forecasting/evaluation/metrics.md#how-i-did-it)
made **MASE** the headline metric (MAPE is undefined on intermittent demand full of zeros) and
tracks under-/zero-forecast ratios as business-facing diagnostics. If you want the *forecast*
metrics, start there — I'm not duplicating them here.

**Model-comparison and selection framing** lives on the two sibling pages:
[Model Comparison](../09-time-series-forecasting/evaluation/comparison.md) and
[Method Selection Framework](../09-time-series-forecasting/evaluation/selection-framework.md).

## How I did it — a plain regression model bake-off

The forecasting pages are all about a time axis. But the most reusable pattern — **fit several
models on one train/test split and rank them in a single metrics table** — is just as useful for
ordinary regression. In my STAT 650 final I predicted a continuous fish "fullness" target
(`log(Weight / Length1)`) from body-dimension features and compared four regressors head to
head: multiple linear regression, ridge, elastic net, and degree-2 polynomial regression.

Every model was trained on the same 75% split and scored on the same held-out 25%, so the numbers
are comparable:

| Model | Test RMSE | Test R² | Test MAE |
|---|---|---|---|
| Multiple Linear Regression | 0.156 | 0.963 | 0.120 |
| Ridge (`RidgeCV`, cv=10) | 0.156 | 0.963 | 0.121 |
| Elastic Net (`ElasticNetCV`, cv=10) | 0.160 | 0.961 | 0.126 |
| **Polynomial (degree 2)** | **0.121** | **0.978** | **0.089** |

Source: `course-files/appendix/Homework/stat650_hw/final/report.ipynb` (STAT 650 final, Situation 1 — my own results)

The metrics themselves are one-liners; the discipline is computing all of them the same way for
every model:

```python
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np

test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
test_r2   = r2_score(y_test, y_test_pred)
test_mae  = mean_absolute_error(y_test, y_test_pred)
```

Source: `course-files/appendix/Homework/stat650_hw/final/STAT650-F25-Final.ipynb` (my own code)

I also computed **adjusted R²** for each model — R² penalized by the number of predictors — since
with six features plus a Volume interaction term, raw R² can climb just from adding columns.
Polynomial regression won on every metric: it captured the quadratic weight-vs-length relationship
the linear models couldn't, without overfitting (the train/test gap stayed small). The
ridge/elastic-net rows are the interesting control: regularization barely moved the needle here
because the predictors were highly collinear but the signal was strong, so shrinkage had little to
trade against. That's the value of the table — it shows *when* regularization earns its keep, not
just that you tried it.

The cross-validation baked into `RidgeCV`/`ElasticNetCV` (the `cv=10` that picks the
regularization strength) is covered on its own page:
[Cross-Validation & Splitting](cross-validation-and-splitting.md).

## Gotchas

- **R² and adjusted R² disagree for a reason — report the adjusted one for multi-feature models.**
  Raw R² never decreases when you add a predictor, so it rewards kitchen-sink models. Adjusted R²
  docks you for predictors that don't pull their weight; when the two diverge, the gap *is* the
  overfitting signal.
- **RMSE vs MAE can flip the ranking.** RMSE squares the errors, so a model with one big miss can
  lose to a model that's slightly worse on average. Decide whether big misses are actually the
  expensive failure *before* you pick the metric that crowns the winner — the same point the
  [forecast-metrics gotchas](../09-time-series-forecasting/evaluation/metrics.md#gotchas) make.
- **A metric table is only honest if every model saw the same split.** The whole comparison rests
  on one fixed train/test partition applied identically to all four models. Refit the split per
  model and you're comparing luck, not models.
- **Transform-aware targets need transform-aware error.** The fullness target was log-scaled, so
  an RMSE of 0.12 is in log units, not grams. When you transform the target, remember the metric
  lives in the transformed space unless you invert it first.
