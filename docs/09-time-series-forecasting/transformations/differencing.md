# Differencing

## Overview

Differencing transforms a time series by computing the difference between consecutive observations. It's the primary technique for achieving stationarity—removing trends and seasonality from data.

## First Difference

The first difference removes linear trends:

```
y'_t = y_t - y_{t-1}
```

### Implementation

```python
import pandas as pd

# First difference
df['diff_1'] = df['value'].diff(1)

# Check stationarity after differencing
from statsmodels.tsa.stattools import adfuller
result = adfuller(df['diff_1'].dropna())
print(f"ADF Statistic: {result[0]:.4f}")
print(f"p-value: {result[1]:.4f}")
```

## Second Difference

For data with quadratic trends or when first differencing isn't enough:

```
y''_t = y'_t - y'_{t-1} = (y_t - y_{t-1}) - (y_{t-1} - y_{t-2})
```

```python
# Second difference
df['diff_2'] = df['value'].diff(1).diff(1)

# Or equivalently
df['diff_2'] = df['value'].diff(2) - df['value'].diff(1)
```

## Seasonal Differencing

Removes seasonal patterns by subtracting the value from the same season in the previous cycle:

```
y_t - y_{t-m}
```

Where m is the seasonal period.

```python
# Seasonal differencing for monthly data with yearly pattern
df['seasonal_diff'] = df['value'].diff(12)

# For weekly data with yearly pattern
df['seasonal_diff'] = df['value'].diff(52)

# For daily data with weekly pattern
df['seasonal_diff'] = df['value'].diff(7)
```

## Combined Differencing

For data with both trend and seasonality, apply both:

```python
# First difference to remove trend
diff_1 = df['value'].diff(1)

# Then seasonal difference to remove seasonality
diff_1_seasonal = diff_1.diff(12)

# This is equivalent to ARIMA's d=1, D=1
```

## How Much Differencing?

### Under-Differencing
- ACF decays very slowly
- Series still shows trend
- ADF test fails (p-value > 0.05)

### Correct Differencing
- ACF drops quickly
- Series fluctuates around constant mean
- ADF test passes (p-value < 0.05)

### Over-Differencing
- ACF shows negative spike at lag 1
- Introduces artificial patterns
- Increases variance unnecessarily

## Visual Guide

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 1, figsize=(12, 10))

# Original series
axes[0].plot(df['value'])
axes[0].set_title('Original Series')

# First difference
axes[1].plot(df['value'].diff(1))
axes[1].set_title('First Difference')

# Second difference
axes[2].plot(df['value'].diff(1).diff(1))
axes[2].set_title('Second Difference')

plt.tight_layout()
plt.show()
```

## Back-Transformation (Inverse Differencing)

To convert forecasts back to original scale:

### For First Difference
```python
def inverse_difference(forecast, last_value):
    """Invert first differencing."""
    original = [last_value]
    for diff_value in forecast:
        original.append(original[-1] + diff_value)
    return original[1:]

# Get the last observed value before forecast period
last_observed = df['value'].iloc[-1]

# Convert differenced forecast to original scale
forecast_original = inverse_difference(forecast_diff, last_observed)
```

### For Seasonal Difference
```python
def inverse_seasonal_difference(forecast, last_season_values, period):
    """Invert seasonal differencing."""
    original = []
    for i, diff_value in enumerate(forecast):
        # Add back the value from same season in previous cycle
        season_idx = i % period
        original.append(diff_value + last_season_values[season_idx])
    return original

# Get last full season of values
last_season = df['value'].iloc[-12:].values  # For monthly with yearly seasonality

forecast_original = inverse_seasonal_difference(forecast_seasonal_diff, last_season, 12)
```

## Differencing in ARIMA

ARIMA handles differencing internally through the 'd' parameter:

```python
from statsmodels.tsa.arima.model import ARIMA

# ARIMA with d=1 (one difference)
model = ARIMA(df['value'], order=(1, 1, 1))
fitted = model.fit()

# Forecasts are automatically in original scale
forecast = fitted.forecast(steps=10)
```

## Determining the Right d

### Method 1: ADF Test Iteration
```python
from statsmodels.tsa.stattools import adfuller

def find_differencing_order(series, max_d=2):
    """Find minimum differencing order for stationarity."""
    for d in range(max_d + 1):
        if d == 0:
            test_series = series
        else:
            test_series = series.diff(d).dropna()

        result = adfuller(test_series)
        print(f"d={d}: ADF={result[0]:.4f}, p-value={result[1]:.4f}")

        if result[1] < 0.05:
            return d

    return max_d

optimal_d = find_differencing_order(df['value'])
```

### Method 2: ndiffs from pmdarima
```python
from pmdarima.arima.utils import ndiffs

# Find optimal d
d = ndiffs(df['value'], test='adf')
print(f"Recommended d: {d}")

# For seasonal differencing
from pmdarima.arima.utils import nsdiffs
D = nsdiffs(df['value'], m=12, test='ocsb')
print(f"Recommended D: {D}")
```

## Common Pitfalls

| Pitfall | Symptom | Solution |
|---------|---------|----------|
| Over-differencing | High negative ACF at lag 1 | Reduce d |
| Forgetting to invert | Forecasts don't match scale | Apply inverse transform |
| Wrong seasonal period | Seasonality remains after diff | Check m value |
| NaN handling | Errors in calculations | Use `.dropna()` |

## How I did it

Differencing was the fourth branch of `apply_transformations` — and notably the only transform in the sweep whose inverse is `None`:

```python
elif transformation_type == 'diff':
    # Simple differencing
    df_transformed['Qty'] = df_transformed['Qty'].diff().fillna(0)
    # Note: inverse requires cumulative sum when forecasting
    inverse_func = None
```

Source: `course-files/09-time-series-forecasting/time-series-forecasting/forecasting-pipeline.py` (`apply_transformations`)

In practice the project mostly leaned on SARIMA's built-in `d` parameter for differencing rather than this manual branch, because inverting a manual difference back to the original scale requires the last pre-forecast value plus a cumulative sum.

## Gotchas

- **`inverse_func = None` is a landmine.** Every other transform returns a real inverse; `diff` returns `None`. The sweep in `main()` wraps the inverse call in `try/except` and falls back to the un-inverted forecast — which means a differenced forecast is silently evaluated on the *differenced* scale unless you rebuild the level yourself with a cumulative sum. That's why I preferred SARIMA's `d` (it inverts internally) over this branch.
- **`.diff().fillna(0)` fabricates the first row.** The first difference is undefined; filling it with 0 invents a data point. Fine for a quick transform, wrong if that first row matters.
- **Difference vs stationarity is the point.** Differencing is the go-to for *trend* non-stationarity; use *seasonal* differencing (`.diff(m)`) for seasonal non-stationarity, and don't over-difference (a big negative ACF spike at lag 1 is the warning sign).
