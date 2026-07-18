# ARIMA

## Overview

**ARIMA** (AutoRegressive Integrated Moving Average) is one of the most widely used statistical methods for time series forecasting. It combines three key components to model temporal dependencies.

## Components

### AR (AutoRegressive) - The "p" Parameter
Uses the dependent relationship between an observation and a number of lagged observations.

```
y_t = c + φ₁y_{t-1} + φ₂y_{t-2} + ... + φ_p y_{t-p} + ε_t
```

- **p** = number of lag observations included (the order)
- Models the influence of past values on current values
- High p captures longer-term dependencies

### I (Integrated) - The "d" Parameter
Applies differencing to make the time series stationary.

```
y'_t = y_t - y_{t-1}  (first difference, d=1)
y''_t = y'_t - y'_{t-1}  (second difference, d=2)
```

- **d** = degree of differencing required
- Removes trends and achieves stationarity
- Usually d=1 or d=2 is sufficient

### MA (Moving Average) - The "q" Parameter
Uses the dependency between an observation and residual errors from a moving average model.

```
y_t = c + ε_t + θ₁ε_{t-1} + θ₂ε_{t-2} + ... + θ_q ε_{t-q}
```

- **q** = size of the moving average window
- Models the influence of past forecast errors
- Captures short-term shock effects

## ARIMA(p, d, q) Notation

The full ARIMA model is specified as ARIMA(p, d, q):
- ARIMA(1, 0, 0) = AR(1) model
- ARIMA(0, 0, 1) = MA(1) model
- ARIMA(0, 1, 0) = Random walk
- ARIMA(1, 1, 1) = Common starting point for many series

## Implementation

```python
from statsmodels.tsa.arima.model import ARIMA

# Fit ARIMA model
model = ARIMA(series, order=(1, 1, 1))
fitted = model.fit()

# View summary
print(fitted.summary())

# Make forecast
forecast = fitted.forecast(steps=10)
```

## Selecting p, d, q

### Method 1: ACF/PACF Analysis

1. **Determine d**: Difference until the series is stationary (use ADF test)
2. **Determine p**: Look at PACF cutoff on differenced series
3. **Determine q**: Look at ACF cutoff on differenced series

### Method 2: Auto ARIMA

```python
from pmdarima import auto_arima

# Automatically select best parameters
model = auto_arima(
    series,
    start_p=0, max_p=5,
    start_q=0, max_q=5,
    d=None,  # Let it determine d
    seasonal=False,
    trace=True,
    error_action='ignore',
    suppress_warnings=True
)

print(model.summary())
```

### Method 3: Information Criteria

Compare models using AIC (Akaike Information Criterion) or BIC (Bayesian Information Criterion):

```python
# Lower AIC/BIC = better model
print(f"AIC: {fitted.aic}")
print(f"BIC: {fitted.bic}")
```

## When ARIMA Excels

- Data shows clear **autocorrelation patterns**
- The time series has a **simple underlying structure**
- The series is relatively **stationary** or can be made stationary through differencing
- You need **interpretable decomposition** of temporal dynamics
- Data is **limited** (small to medium datasets)

**Example**: Monthly retail sales with clear temporal dependencies but no strong seasonality.

## Model Diagnostics

After fitting, check residuals:

```python
# Plot diagnostics
fitted.plot_diagnostics(figsize=(12, 8))

# Residuals should be:
# 1. Normally distributed (check histogram/QQ plot)
# 2. No autocorrelation (check ACF of residuals)
# 3. Constant variance (check residuals vs time)
```

### Ljung-Box Test
Test for remaining autocorrelation in residuals:

```python
from statsmodels.stats.diagnostic import acorr_ljungbox

lb_test = acorr_ljungbox(fitted.resid, lags=10)
# p-value > 0.05 suggests no significant autocorrelation remains
```

## Limitations

- Assumes **linear relationships**
- Requires **stationary data** (after differencing)
- Cannot incorporate **external variables** (use ARIMAX for that)
- May struggle with **complex patterns** that ML models can capture
- Limited to **univariate** forecasting

## Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Non-stationarity | ADF test fails | Increase d |
| Autocorrelation in residuals | Ljung-Box fails | Adjust p or q |
| Poor fit | High AIC, bad diagnostics | Try different orders or different model |
| Overfitting | Good training, poor test | Reduce model complexity |

## How I did it

Honest note: the senior project never wrote a *standalone* plain-ARIMA function. It went straight to SARIMA, using statsmodels' `ARIMA` class with a `seasonal_order` — a non-seasonal ARIMA is just that same call with the seasonal term set to `(0,0,0,0)`. The relevant fit lives inside `run_sarima`:

```python
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(train['Qty'], order=best_order,
              seasonal_order=best_seasonal_order)
fitted = model.fit()
forecast = fitted.forecast(steps=len(test))
```

Source: `course-files/09-time-series-forecasting/time-series-forecasting/forecasting-pipeline.py` (`run_sarima`)

In my distribution demand-forecasting production pipeline, ARIMA *is* a first-class model (`src/models/arima_model.py`, auto-ARIMA per stock) and one of the four ensemble members. So the standalone-ARIMA treatment shows up in the production system, not the school project. See the full walkthrough on the [SARIMA page](sarima.md).

## Gotchas

- **Don't claim more than was built.** `docs/outline.md` listed ARIMA (and VAR, SVR, LSTM, Prophet, Random Forest) as candidate methods, but the implemented ARIMA-family model was SARIMA only. This page's general theory is textbook; the project-specific code is the SARIMA call above.
- **`statsmodels` has two ARIMA entry points.** The project used `statsmodels.tsa.arima.model.ARIMA` (which accepts `seasonal_order`), not the older `SARIMAX` shown in some examples — they overlap but the newer `ARIMA` was the one actually wired in.
