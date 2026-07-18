# Statistical vs ML Models: A Comparison

## Overview

Choosing between statistical methods (ARIMA, ETS) and machine learning approaches (XGBoost, Random Forest) depends on data characteristics, requirements, and constraints.

## Key Differences

| Aspect | Statistical Models | ML Models |
|--------|-------------------|-----------|
| **Philosophy** | Model temporal dependencies directly | Treat as supervised learning problem |
| **Stationarity** | Usually required | Not required |
| **External features** | Limited (ARIMAX) | Easily incorporated |
| **Non-linear patterns** | Cannot capture | Handle well |
| **Interpretability** | Model coefficients | Feature importance |
| **Prediction intervals** | Built-in | Requires extra work |
| **Data requirements** | Works with less data | Needs more data |
| **Feature engineering** | Minimal | Critical |

## When Statistical Models Excel

### ARIMA/SARIMA
- Data shows clear **autocorrelation patterns**
- The time series has a **simple underlying structure**
- There are **distinct seasonal patterns** at regular intervals
- The series is relatively **stationary** or easily made stationary
- You need **interpretable decomposition** of trend and seasonality
- **Limited data** is available

### Exponential Smoothing (ETS)
- Strong **trend and/or seasonal components**
- **Recent observations** are more important than historical ones
- Data contains **level shifts** or changing trends
- You need **reliable prediction intervals**
- The series has **multiplicative seasonality**

## When ML Models Excel

### XGBoost
- **Multiple external factors** influence the forecast
- The time series has **complex non-linear patterns**
- You have a **large dataset** with many features
- **Relationships between variables change** over time
- There are **multiple seasonalities** or irregular patterns

### Random Forest
- Data contains **outliers or noise**
- You need a **robust model** less prone to overfitting
- **Multiple predictor variables** are available
- **Feature importance analysis** is needed
- The time series has **structural breaks** or regime changes

## Empirical Findings

From a comparative study on retail forecasting data:

### Performance Results

> "XGBoost consistently outperformed other models on the retail dataset, with the lowest MAE (33.67) and RMSE (47.35) using no transformation."

> "Machine learning approaches demonstrated superior performance compared to traditional statistical methods for this data."

### Transformation Impact

> "Transformations didn't universally improve forecasting accuracy for this dataset. The untransformed data ('none' option) performed best for most models."

> "The effectiveness of transformations varies by model type—statistical models (ARIMA, ETS) responded differently than machine learning approaches (XGBoost)."

### Seasonality Detection

> "Seasonal Naive approach performed significantly worse than even simple Naive forecasting, suggesting weak weekly seasonality patterns in the data."

## Decision Framework

### Start with These Questions

1. **How much data do you have?**
   - < 100 observations → Statistical methods
   - > 1000 observations → ML methods likely better

2. **Do you have external features?**
   - No → Statistical methods work fine
   - Yes → ML methods can leverage them

3. **Is the pattern complex/non-linear?**
   - Simple, linear → Statistical methods
   - Complex, non-linear → ML methods

4. **Do you need prediction intervals?**
   - Critical → Statistical methods (built-in)
   - Nice-to-have → Either (ML requires extra work)

5. **How important is interpretability?**
   - Very → Statistical methods
   - Somewhat → Either (ML has feature importance)

### Quick Guide

| Data Characteristic | Recommended Approach |
|--------------------|---------------------|
| Short series, clear seasonality | SARIMA or ETS |
| Long series, many features | XGBoost or Random Forest |
| Need confidence intervals | ETS or ARIMA |
| Multiple seasonalities | ML with feature engineering |
| Real-time/streaming data | Exponential smoothing |
| Non-linear relationships | XGBoost |
| Outlier-heavy data | Random Forest |

## Ensemble Approaches

Combining statistical and ML models often outperforms either alone:

```python
def ensemble_forecast(stat_forecast, ml_forecast, weights=[0.4, 0.6]):
    """Weighted ensemble of statistical and ML forecasts."""
    return weights[0] * stat_forecast + weights[1] * ml_forecast
```

### Finding Optimal Weights

```python
from scipy.optimize import minimize

def optimize_ensemble_weights(stat_forecast, ml_forecast, actual):
    """Find optimal ensemble weights."""
    def objective(weights):
        ensemble = weights[0] * stat_forecast + weights[1] * ml_forecast
        return mean_squared_error(actual, ensemble)

    # Constraint: weights sum to 1
    constraint = {'type': 'eq', 'fun': lambda w: w[0] + w[1] - 1}
    bounds = [(0, 1), (0, 1)]

    result = minimize(objective, [0.5, 0.5], bounds=bounds, constraints=constraint)
    return result.x

weights = optimize_ensemble_weights(sarima_pred, xgb_pred, y_test)
print(f"Optimal weights: SARIMA={weights[0]:.2f}, XGBoost={weights[1]:.2f}")
```

## Summary

- **No single model wins everywhere**—performance depends heavily on data characteristics
- **Always test multiple approaches** and compare on held-out data
- **Baselines matter**—if you can't beat naive, something's wrong
- **Ensemble methods** often provide the best of both worlds
- **Domain knowledge** should guide model selection alongside empirical performance

## How I did it

**School project — a brute-force sweep.** The comparison *was* the project: `main()` loops over 3 aggregation levels x 4 transformations x 5 models, records MAE/RMSE for every cell, and searches for the single best combination:

```python
aggregation_levels = ['D', 'W', 'M']
transformations = [None, 'log', 'boxcox', 'sqrt']
model_names = ['Naive', 'Seasonal Naive', 'SARIMA', 'ETS', 'XGBoost']

# ... after filling aggregation_results[agg][transform] with a metrics table ...
best_overall = {"MAE": float('inf'), "RMSE": float('inf')}
for metric in ['MAE', 'RMSE']:
    for agg_level in aggregation_levels:
        for transform in transformations:
            for model in model_names:
                value = aggregation_results[agg_level][transform_name].loc[model, metric]
                if value < best_overall[metric]:
                    best_overall[metric] = value
                    best_combo[metric] = {'Aggregation': agg_level, 'Model': model,
                                          'Transform': transform_name, 'Value': value}
```

Source: `course-files/09-time-series-forecasting/time-series-forecasting/forecasting-pipeline.py` (`main`)

The [Senior Project Pipeline notebook](../notebooks/senior-project-pipeline.ipynb) runs a compact version of this sweep (a transform x model MAE table) on synthetic data.

**Production — an auto-tuned weighted ensemble instead of "pick one."** My distribution demand-forecasting system doesn't crown a single winner; it *combines* the four models with weights optimized on validation data via `scipy.optimize.minimize`, with per-model min/max bounds so no single model can dominate or vanish:

```python
def objective(weights):
    combined = np.dot(pred_matrix, weights)
    base_loss = np.sqrt(np.mean((combined - y_true) ** 2))   # RMSE
    if self.l2_regularization > 0:                            # discourage extremes
        base_loss += self.l2_regularization * np.sum((weights - 1.0/n_models) ** 2)
    return base_loss

constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}   # weights sum to 1
bounds = [(self.min_weight, self.max_weight)] * n_models          # e.g. 0.05..0.80
result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
```

Source: `demand-forecast/src/ensemble/weighted.py` (private distribution-forecasting repo; `WeightedEnsemble._optimize_weights`)

## Gotchas

- **The sweep is combinatorial and slow.** 3 x 4 x 5 = 60 fits per run, and each SARIMA does an `auto_arima` search — the aggregation loop is what made the full run take real time. Narrow the grid once you see which cells matter.
- **"Best on the holdout" can still be luck.** With a single 3-month holdout, the winning combo is one draw. The production ensemble guards against overfitting-to-one-test-set with min/max weight **bounds** and optional **L2 regularization** toward equal weights — exactly the discipline a single-holdout sweep lacks.
- **Manual/equal weights vs optimized weights.** The school project's `create_weighted_ensemble` used equal (or hand-set) weights; production *learns* them per stock. Equal-weight ensembling is a fine baseline, but auto-tuning is where the ensemble started beating its members.
- **Compare on the *original* scale.** In the sweep, transformed forecasts are inverted before scoring (`original_test = df.loc[test.index]`) — comparing a log-space forecast against raw actuals would make that model look artificially great.
