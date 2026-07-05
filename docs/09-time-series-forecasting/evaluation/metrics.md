# Evaluation Metrics

## Overview

Choosing the right evaluation metric is crucial for assessing forecast quality. Different metrics emphasize different aspects of forecast accuracy.

## Common Metrics

### Mean Absolute Error (MAE)

The average absolute difference between forecasts and actual values.

```
MAE = (1/n) × Σ|actual - forecast|
```

```python
from sklearn.metrics import mean_absolute_error

mae = mean_absolute_error(actual, forecast)
```

**Properties:**
- Easy to interpret (same units as data)
- Robust to outliers
- Treats all errors equally

**Use when:** You want an intuitive measure of average error magnitude.

### Root Mean Squared Error (RMSE)

The square root of the average squared errors.

```
RMSE = √[(1/n) × Σ(actual - forecast)²]
```

```python
from sklearn.metrics import mean_squared_error
import numpy as np

rmse = np.sqrt(mean_squared_error(actual, forecast))
```

**Properties:**
- Same units as data
- Penalizes large errors more heavily than MAE
- More sensitive to outliers

**Use when:** Large errors are particularly undesirable.

### Mean Absolute Percentage Error (MAPE)

The average absolute percentage error.

```
MAPE = (100/n) × Σ|actual - forecast| / |actual|
```

```python
def mape(actual, forecast):
    """Calculate MAPE, handling zeros."""
    actual = np.array(actual)
    forecast = np.array(forecast)
    # Avoid division by zero
    mask = actual != 0
    return np.mean(np.abs((actual[mask] - forecast[mask]) / actual[mask])) * 100
```

**Properties:**
- Scale-independent (percentage)
- Undefined when actual = 0
- Asymmetric (over-forecasts penalized less than under-forecasts)

**Use when:** Comparing across different scales or communicating to stakeholders.

### Symmetric Mean Absolute Percentage Error (sMAPE)

A symmetric version of MAPE.

```
sMAPE = (100/n) × Σ|actual - forecast| / ((|actual| + |forecast|) / 2)
```

```python
def smape(actual, forecast):
    """Calculate symmetric MAPE."""
    actual = np.array(actual)
    forecast = np.array(forecast)
    denominator = (np.abs(actual) + np.abs(forecast)) / 2
    # Avoid division by zero
    mask = denominator != 0
    return np.mean(np.abs(actual[mask] - forecast[mask]) / denominator[mask]) * 100
```

**Properties:**
- Bounded between 0% and 200%
- Symmetric treatment of over/under forecasts
- Still problematic when both actual and forecast are near zero

**Use when:** You need a percentage metric but MAPE's asymmetry is problematic.

### Mean Squared Error (MSE)

The average squared error (RMSE before taking square root).

```
MSE = (1/n) × Σ(actual - forecast)²
```

```python
from sklearn.metrics import mean_squared_error

mse = mean_squared_error(actual, forecast)
```

**Properties:**
- Not in original units (squared)
- Heavily penalizes large errors
- Useful as a loss function for optimization

**Use when:** Optimizing models (as a loss function) or when large errors are very costly.

## Comparison of Metrics

| Metric | Units | Outlier Sensitivity | Interpretation |
|--------|-------|---------------------|----------------|
| MAE | Same as data | Low | Average error |
| RMSE | Same as data | High | Typical error |
| MSE | Squared | Very High | Error variance |
| MAPE | Percentage | Medium | Relative error |
| sMAPE | Percentage | Medium | Symmetric relative error |

## Calculating All Metrics

```python
def forecast_metrics(actual, forecast):
    """Calculate comprehensive forecast metrics."""
    actual = np.array(actual)
    forecast = np.array(forecast)

    mae = np.mean(np.abs(actual - forecast))
    rmse = np.sqrt(np.mean((actual - forecast) ** 2))
    mse = np.mean((actual - forecast) ** 2)

    # MAPE (avoiding zeros)
    mask = actual != 0
    if mask.sum() > 0:
        mape = np.mean(np.abs((actual[mask] - forecast[mask]) / actual[mask])) * 100
    else:
        mape = np.nan

    # sMAPE
    denominator = (np.abs(actual) + np.abs(forecast)) / 2
    mask = denominator != 0
    if mask.sum() > 0:
        smape = np.mean(np.abs(actual[mask] - forecast[mask]) / denominator[mask]) * 100
    else:
        smape = np.nan

    return {
        'MAE': mae,
        'RMSE': rmse,
        'MSE': mse,
        'MAPE': mape,
        'sMAPE': smape
    }

# Usage
metrics = forecast_metrics(actual, forecast)
for name, value in metrics.items():
    print(f"{name}: {value:.4f}")
```

## Relative Metrics (Skill Scores)

Compare your model against a baseline (e.g., naive forecast).

### Relative MAE
```python
def relative_mae(actual, forecast, baseline_forecast):
    """MAE relative to baseline."""
    model_mae = mean_absolute_error(actual, forecast)
    baseline_mae = mean_absolute_error(actual, baseline_forecast)
    return model_mae / baseline_mae

# < 1 means better than baseline
# > 1 means worse than baseline
```

### Forecast Skill Score
```python
def skill_score(actual, forecast, baseline_forecast):
    """Skill score relative to baseline."""
    model_error = mean_absolute_error(actual, forecast)
    baseline_error = mean_absolute_error(actual, baseline_forecast)
    return 1 - (model_error / baseline_error)

# > 0 means better than baseline
# 0 means same as baseline
# < 0 means worse than baseline
```

## Choosing the Right Metric

| Scenario | Recommended Metric |
|----------|-------------------|
| General purpose | MAE or RMSE |
| Large errors are costly | RMSE or MSE |
| Need percentage interpretation | MAPE or sMAPE |
| Comparing across different scales | MAPE or sMAPE |
| Data contains zeros | MAE, RMSE (avoid MAPE) |
| Communicating to non-technical stakeholders | MAPE |
| Optimization objective | MSE (differentiable) |

## Practical Example

From a retail forecasting comparison:

| Model | MAE | RMSE | Transformation |
|-------|-----|------|----------------|
| XGBoost | 33.67 | 47.35 | None |
| Random Forest | 42.15 | 58.23 | None |
| SARIMA | 45.32 | 62.18 | Square Root |
| ETS | 48.91 | 65.44 | None |
| Naive | 52.33 | 71.22 | None |

XGBoost achieved the lowest MAE and RMSE, indicating best overall performance.
