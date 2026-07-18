# Stationarity

## What is Stationarity?

A time series is **stationary** if its statistical properties remain constant over time. Specifically:

1. **Constant mean**: The average value doesn't change over time
2. **Constant variance**: The spread of values remains consistent
3. **Constant autocorrelation**: The relationship between values at different lags doesn't depend on when you measure it

## Why Stationarity Matters

Many statistical forecasting methods (ARIMA, ETS) assume stationarity because:

- **Predictable patterns**: Statistical properties that hold in the past will hold in the future
- **Model validity**: Parameter estimates remain meaningful over time
- **Reliable forecasts**: Predictions based on historical patterns stay valid

Non-stationary data can lead to:
- Spurious correlations
- Unreliable forecasts
- Invalid statistical tests

## Types of Non-Stationarity

### Trend Non-Stationarity
The mean changes over time (upward or downward drift).

**Solution**: Differencing or detrending

### Variance Non-Stationarity (Heteroscedasticity)
The variance changes over time (often increases with the level).

**Solution**: Log or Box-Cox transformation

### Seasonal Non-Stationarity
Seasonal patterns that change in magnitude over time.

**Solution**: Seasonal differencing or multiplicative decomposition

## Testing for Stationarity

### Visual Inspection
- Plot the time series and look for trends or changing variance
- Check if the data fluctuates around a constant mean

### Augmented Dickey-Fuller (ADF) Test
The most common statistical test for stationarity.

```python
from statsmodels.tsa.stattools import adfuller

result = adfuller(series)
print(f'ADF Statistic: {result[0]}')
print(f'p-value: {result[1]}')

# If p-value < 0.05, reject null hypothesis (series is stationary)
# If p-value > 0.05, fail to reject (series may be non-stationary)
```

### KPSS Test
Tests the null hypothesis that the series is stationary (opposite of ADF).

```python
from statsmodels.tsa.stattools import kpss

result = kpss(series)
# If p-value < 0.05, series is non-stationary
```

## Making Data Stationary

### Differencing
Subtract the previous observation from the current one:

```python
# First difference (removes trend)
diff_1 = series.diff(1)

# Seasonal difference (removes seasonality)
diff_seasonal = series.diff(12)  # For monthly data with yearly seasonality
```

### Transformations
Apply mathematical transformations to stabilize variance:

- **Log transformation**: `np.log(series)`
- **Square root**: `np.sqrt(series)`
- **Box-Cox**: Finds optimal power transformation

### Detrending
Remove the trend component explicitly:

```python
from scipy.signal import detrend
stationary = detrend(series)
```

## Practical Considerations

- **Machine learning models** (XGBoost, Random Forest) don't require stationarity—they can learn from non-stationary patterns
- **Statistical models** (ARIMA) handle some non-stationarity through integrated (I) component
- Always check residuals for stationarity after fitting a model

## How I did it

In the senior project, both stationarity tests ran inside the EDA step — ADF and KPSS side by side, since they test opposite null hypotheses. KPSS is wrapped in `try/except` because it raises on some inputs, and I didn't want one test to kill the whole EDA run:

```python
# Stationarity tests
print("\nStationarity Tests:")
print("ADF Test: p-value", adfuller(df['Qty'].dropna())[1])
try:
    print("KPSS Test: p-value", kpss(df['Qty'].dropna())[1])
except:
    print("KPSS Test failed")
```

Source: `course-files/09-time-series-forecasting/time-series-forecasting/forecasting-pipeline.py` (`run_eda`)

## Gotchas

- **Run ADF *and* KPSS, not just one.** ADF's null is "non-stationary"; KPSS's null is "stationary." They disagree in informative ways — the case worth catching is ADF failing to reject *and* KPSS rejecting, which points to a series that needs differencing.
- **KPSS throws.** It emits an `InterpolationWarning` and can error on short or oddly-shaped series, which is why the real code guards it with `try/except`. ADF was the reliable one in practice.
- **Stationarity mattered far less than expected for the ML model.** The project's whole conclusion was that XGBoost won *without* any transformation or differencing (`docs/takeaways.md`). The stationarity workflow is essential for SARIMA/ETS but the tree model happily learned from the raw non-stationary series.
