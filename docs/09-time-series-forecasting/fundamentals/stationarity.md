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
