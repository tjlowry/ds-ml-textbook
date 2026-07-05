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
