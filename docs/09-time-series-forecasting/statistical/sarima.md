# SARIMA

## Overview

**SARIMA** (Seasonal ARIMA) extends ARIMA by adding seasonal components, allowing it to capture repeating patterns at fixed intervals (like weekly, monthly, or yearly seasonality).

## The Seasonal Extension

SARIMA is denoted as ARIMA(p, d, q)(P, D, Q, m) where:

- **(p, d, q)**: Non-seasonal components (same as ARIMA)
- **(P, D, Q, m)**: Seasonal components
  - **P**: Seasonal autoregressive order
  - **D**: Seasonal differencing order
  - **Q**: Seasonal moving average order
  - **m**: Number of periods per season (e.g., 12 for monthly data with yearly seasonality)

## Seasonal Components Explained

### Seasonal AR (P)
Captures how the current value depends on values from previous seasons:

```
y_t depends on y_{t-m}, y_{t-2m}, ..., y_{t-Pm}
```

Example: January sales influenced by last January's sales.

### Seasonal Differencing (D)
Removes seasonal patterns by subtracting values from the same season in the previous cycle:

```
y'_t = y_t - y_{t-m}
```

### Seasonal MA (Q)
Captures how current errors depend on errors from previous seasons:

```
ε_t influenced by ε_{t-m}, ε_{t-2m}, ..., ε_{t-Qm}
```

## Common SARIMA Configurations

| Data Frequency | Season (m) | Typical Starting Model |
|---------------|------------|------------------------|
| Monthly (yearly pattern) | 12 | ARIMA(1,1,1)(1,1,1,12) |
| Weekly (yearly pattern) | 52 | ARIMA(1,1,1)(1,1,1,52) |
| Daily (weekly pattern) | 7 | ARIMA(1,1,1)(1,1,1,7) |
| Hourly (daily pattern) | 24 | ARIMA(1,1,1)(1,1,1,24) |

## Implementation

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Fit SARIMA model for monthly data with yearly seasonality
model = SARIMAX(
    series,
    order=(1, 1, 1),           # Non-seasonal (p, d, q)
    seasonal_order=(1, 1, 1, 12)  # Seasonal (P, D, Q, m)
)
fitted = model.fit(disp=False)

# View summary
print(fitted.summary())

# Forecast
forecast = fitted.forecast(steps=12)
```

## Automatic Selection with pmdarima

```python
from pmdarima import auto_arima

model = auto_arima(
    series,
    start_p=0, max_p=3,
    start_q=0, max_q=3,
    d=None,
    start_P=0, max_P=2,
    start_Q=0, max_Q=2,
    D=None,
    m=12,  # Seasonal period
    seasonal=True,
    trace=True,
    error_action='ignore',
    suppress_warnings=True,
    stepwise=True
)
```

## When SARIMA Excels

- Data shows **clear seasonal patterns** at regular intervals
- There are **distinct seasonal patterns** (e.g., yearly cycles in monthly data)
- The series is relatively stationary or can be made stationary through differencing
- You need **interpretable decomposition** of trend and seasonality
- You want **prediction intervals** alongside point forecasts

**Example**: Monthly retail sales with consistent yearly seasonal patterns—holiday spikes, summer lulls.

## Determining Seasonal Parameters

### Step 1: Identify the Seasonal Period (m)
- Plot the data and look for repeating patterns
- Check ACF for spikes at regular intervals
- Use domain knowledge (monthly data usually has m=12)

### Step 2: Determine Seasonal Differencing (D)
- If seasonal patterns are unstable, apply seasonal differencing (D=1)
- Check if seasonal_diff = series - series.shift(m) is stationary

### Step 3: Determine P and Q
- Look at ACF/PACF at seasonal lags (m, 2m, 3m, ...)
- Spikes at seasonal lags in PACF suggest P
- Spikes at seasonal lags in ACF suggest Q

## Model Diagnostics

```python
# Check diagnostics
fitted.plot_diagnostics(figsize=(12, 8))

# Examine residual ACF at seasonal lags
from statsmodels.graphics.tsaplots import plot_acf
plot_acf(fitted.resid, lags=36)  # Check for remaining seasonal patterns
```

Residuals should show no significant spikes at seasonal lags.

## Limitations

- **Computational cost**: More parameters means longer fitting time
- **Fixed seasonality**: Assumes seasonal pattern is constant over time
- **Single seasonality**: Standard SARIMA handles only one seasonal period
- **Large m problems**: Weekly data with yearly seasonality (m=52) can be challenging

## Multiple Seasonalities

For data with multiple seasonal patterns (e.g., daily and weekly), consider:

1. **Fourier terms**: Add sine/cosine features at seasonal frequencies
2. **TBATS**: Handles multiple seasonalities natively
3. **Prophet**: Facebook's tool designed for multiple seasonalities
4. **Feature engineering**: Create features for ML models

## Comparison: ARIMA vs SARIMA

| Aspect | ARIMA | SARIMA |
|--------|-------|--------|
| Seasonality | Cannot capture | Explicitly models |
| Parameters | 3 (p, d, q) | 7 (p, d, q, P, D, Q, m) |
| Complexity | Simpler | More complex |
| Use case | Non-seasonal data | Seasonal data |
| Fitting time | Faster | Slower |

## How I did it

SARIMA was the most involved of the statistical models. `run_sarima` picks a seasonal period from the data length, uses `pmdarima.auto_arima` to search orders, fits the chosen model with statsmodels `ARIMA` (using `seasonal_order`), and — importantly — guards against two failure modes: a flat-line forecast and an outright fit exception.

```python
def run_sarima(train, test):
    # Pick a seasonal period from series length
    s_values = [7, 12, 30, 365] if len(train) >= 730 else \
               [7, 12, 30] if len(train) >= 365 else \
               [7] if len(train) >= 52 else [12]
    best_s = s_values[0]

    try:
        from pmdarima import auto_arima
        auto_model = auto_arima(
            train['Qty'], start_p=0, start_q=0, max_p=3, max_q=3, max_d=2,
            start_P=0, start_Q=0, max_P=2, max_Q=2, max_D=1,
            m=best_s, seasonal=True, stepwise=True,
            error_action='ignore', suppress_warnings=True)
        best_order = auto_model.order
        best_seasonal_order = auto_model.seasonal_order
    except ImportError:
        best_order = (1, 1, 1)
        best_seasonal_order = (1, 1, 1, best_s)

    try:
        model = ARIMA(train['Qty'], order=best_order,
                      seasonal_order=best_seasonal_order)
        sarima_model = model.fit()
        forecast = sarima_model.forecast(steps=len(test))

        # Guard: reject a flat-line forecast, retry with different orders
        if np.std(forecast) < 1e-6 * np.std(train['Qty']):
            model = ARIMA(train['Qty'], order=(2, 1, 2),
                          seasonal_order=(1, 1, 1, best_s))
            forecast = model.fit().forecast(steps=len(test))
    except Exception as e:
        forecast = np.array([train['Qty'].iloc[-1]] * len(test))  # naive fallback
    return forecast, run_time, (best_order, best_seasonal_order)
```

Source: `course-files/09-time-series-forecasting/time-series-forecasting/forecasting-pipeline.py` (`run_sarima`)

The [Senior Project Pipeline notebook](../notebooks/senior-project-pipeline.ipynb) runs SARIMA against the synthetic series (with a fixed order for speed instead of the `auto_arima` search). In my distribution demand-forecasting production system, ARIMA is one of four ensemble members and uses auto-ARIMA per stock — it tends to earn its weight on the *smooth* SBC class where trends are clean.

## Gotchas

- **`auto_arima` is the slow part of the whole pipeline.** With `m=365`, the seasonal search is very expensive — this is why the notebook fixes the order and why weekly aggregation (smaller `m`) was often the practical choice.
- **SARIMA can silently predict a flat line.** When the search lands on a degenerate model, `forecast()` returns a near-constant series. The `np.std(forecast) < 1e-6 * np.std(train)` check catches that and retries with `(2,1,2)(1,1,1,s)`; without it you get a "model" that's just a horizontal line.
- **Always wrap the fit.** SARIMA fits throw on ill-conditioned data far more than ETS does, so the code falls back to a naive forecast rather than crashing the sweep.
- **The project has no standalone plain-ARIMA function** — see the [ARIMA page](arima.md). SARIMA with `seasonal_order` was the only ARIMA-family model actually implemented.
