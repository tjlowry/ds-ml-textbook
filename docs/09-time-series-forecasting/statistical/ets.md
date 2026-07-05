# Exponential Smoothing (ETS)

## Overview

Exponential smoothing methods weight observations with exponentially decreasing weights over time—recent observations influence the forecast more than older observations. ETS models are named for their three components: **Error**, **Trend**, and **Seasonality**.

## Core Concept

The exponential smoothing formula for simple exponential smoothing:

```
Forecast = α × (most recent observation) + (1-α) × (previous forecast)
```

Where α (alpha) is the smoothing parameter between 0 and 1:
- **α close to 1**: More weight on recent data (responsive to changes)
- **α close to 0**: More weight on historical data (smoother, more stable)

## ETS Components

### Error (E)
How the model handles forecast errors:
- **Additive (A)**: Errors have constant variance
- **Multiplicative (M)**: Errors vary proportionally with the level

### Trend (T)
The direction of the series:
- **None (N)**: No trend
- **Additive (A)**: Linear trend (constant increase/decrease)
- **Multiplicative (M)**: Exponential trend (percentage growth)
- **Damped (Ad, Md)**: Trend that flattens over time

### Seasonality (S)
Recurring patterns:
- **None (N)**: No seasonality
- **Additive (A)**: Seasonal swings are constant
- **Multiplicative (M)**: Seasonal swings proportional to level

## Common ETS Models

| Model | Name | Use Case |
|-------|------|----------|
| ETS(A,N,N) | Simple Exponential Smoothing | No trend, no seasonality |
| ETS(A,A,N) | Holt's Linear | Trend, no seasonality |
| ETS(A,Ad,N) | Damped Trend | Trend that levels off |
| ETS(A,A,A) | Holt-Winters Additive | Trend + constant seasonality |
| ETS(A,A,M) | Holt-Winters Multiplicative | Trend + proportional seasonality |
| ETS(M,M,M) | Multiplicative Everything | High variation at all levels |

## Implementation

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Holt-Winters with additive trend and multiplicative seasonality
model = ExponentialSmoothing(
    series,
    trend='add',           # 'add', 'mul', or None
    seasonal='mul',        # 'add', 'mul', or None
    seasonal_periods=12    # Period of seasonality
)
fitted = model.fit()

# Forecast
forecast = fitted.forecast(steps=12)

# View smoothing parameters
print(f"Alpha (level): {fitted.params['smoothing_level']}")
print(f"Beta (trend): {fitted.params['smoothing_trend']}")
print(f"Gamma (seasonal): {fitted.params['smoothing_seasonal']}")
```

## Automatic ETS Selection

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Try multiple configurations and select best
best_aic = float('inf')
best_model = None

for trend in ['add', 'mul', None]:
    for seasonal in ['add', 'mul', None]:
        try:
            model = ExponentialSmoothing(
                series,
                trend=trend,
                seasonal=seasonal,
                seasonal_periods=12
            )
            fitted = model.fit()
            if fitted.aic < best_aic:
                best_aic = fitted.aic
                best_model = fitted
        except:
            continue

print(f"Best AIC: {best_aic}")
```

## When ETS Excels

- The time series has **strong trend and/or seasonal components**
- **Recent observations** are more important than historical ones
- Data contains **level shifts** or changing trends
- You need **reliable prediction intervals**
- The series has **multiplicative seasonality** (seasonal variation changes with level)

**Example**: Tourism data with growing seasonal peaks—summer visitors increase each year, and the peaks grow proportionally.

## Damped Trends

Damped trends assume that trends will flatten over time, which is often more realistic for long-term forecasts:

```python
model = ExponentialSmoothing(
    series,
    trend='add',
    damped_trend=True,  # Enable damping
    seasonal='mul',
    seasonal_periods=12
)
fitted = model.fit()
```

Damped trends are especially useful when:
- Forecasting multiple periods ahead
- Growth rates are expected to slow
- You want more conservative long-term predictions

## ETS vs ARIMA

| Aspect | ETS | ARIMA |
|--------|-----|-------|
| Philosophy | Weighted smoothing | Error correction |
| Interpretability | Intuitive components | Statistical terms |
| Seasonality | Built-in | Requires SARIMA |
| Multiplicative patterns | Native support | Requires transformation |
| Prediction intervals | Generally reliable | Can be narrow |
| Auto-selection | Easy | More complex |

## Practical Tips

1. **Check for negative/zero values**: Multiplicative models require positive data
2. **Seasonal period**: Must be correctly specified (12 for monthly, 7 for daily, etc.)
3. **Short series**: ETS needs at least 2 full seasonal cycles
4. **Damped trends**: Usually safer for longer forecast horizons
5. **Initialization**: Use 'estimated' for automatic initialization

```python
model = ExponentialSmoothing(
    series,
    trend='add',
    seasonal='add',
    seasonal_periods=12,
    initialization_method='estimated'  # Let model estimate starting values
)
```

## Diagnostics

```python
# Check residuals
residuals = fitted.resid

# Should be uncorrelated
from statsmodels.graphics.tsaplots import plot_acf
plot_acf(residuals, lags=30)

# Should be normally distributed (approximately)
import matplotlib.pyplot as plt
plt.hist(residuals, bins=30)
```
