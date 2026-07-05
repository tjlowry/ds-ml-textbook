# Seasonality & Trends

## Identifying Trends

### Visual Methods
Plot the time series and look for:
- Consistent upward or downward movement
- Level shifts (sudden changes in the mean)
- Changing growth rates

### Moving Averages
Smooth out short-term fluctuations to reveal underlying trends:

```python
# Simple moving average
trend = series.rolling(window=12).mean()  # 12-period moving average
```

### Statistical Decomposition
Separate the series into trend, seasonal, and residual components:

```python
from statsmodels.tsa.seasonal import seasonal_decompose

# Additive decomposition
result = seasonal_decompose(series, model='additive', period=12)
trend = result.trend
seasonal = result.seasonal
residual = result.resid
```

## Types of Trends

| Type | Description | Example |
|------|-------------|---------|
| Linear | Constant rate of change | Population growth in stable region |
| Exponential | Percentage-based growth | Compound interest |
| Logarithmic | Rapid initial growth that slows | Technology adoption |
| Polynomial | Curved, changing direction | Product lifecycle |

## Identifying Seasonality

### Common Seasonal Patterns

| Frequency | Period | Examples |
|-----------|--------|----------|
| Daily | 24 hours | Electricity usage, website traffic |
| Weekly | 7 days | Retail sales, restaurant visits |
| Monthly | ~30 days | Bill payments, subscription renewals |
| Quarterly | 3 months | Financial reporting, tax payments |
| Yearly | 12 months | Holiday sales, weather patterns |

### Detection Methods

#### 1. Visual Inspection
Plot data and look for repeating patterns at regular intervals.

#### 2. Autocorrelation Function (ACF)
Spikes at seasonal lags indicate seasonality:

```python
from statsmodels.graphics.tsaplots import plot_acf

plot_acf(series, lags=36)  # Check for patterns up to 36 periods
```

#### 3. Seasonal Decomposition
Explicitly extract the seasonal component:

```python
from statsmodels.tsa.seasonal import seasonal_decompose

result = seasonal_decompose(series, period=7)  # Weekly seasonality
result.seasonal.plot()
```

#### 4. Periodogram / Spectral Analysis
Identify dominant frequencies in the data:

```python
from scipy.signal import periodogram

frequencies, power = periodogram(series)
# Peaks in power spectrum indicate seasonal frequencies
```

## Additive vs Multiplicative Seasonality

### Additive Seasonality
Seasonal swings are constant regardless of the level:
- December sales always +$10,000 above average
- Use when seasonal magnitude stays the same

```
Y = Trend + Seasonal + Residual
```

### Multiplicative Seasonality
Seasonal swings proportional to the level:
- December sales always +20% above average
- Use when seasonal magnitude grows with the trend

```
Y = Trend × Seasonal × Residual
```

### How to Determine Which to Use

1. **Plot the data**: If seasonal peaks grow over time, use multiplicative
2. **Check ratio of peaks**: If peak-to-trough ratio is constant, use multiplicative
3. **Transform first**: Log transformation converts multiplicative to additive

## Handling Multiple Seasonalities

Some data has multiple seasonal patterns (e.g., daily and weekly):

```python
# Example: Hourly data with daily and weekly patterns
# Period 24 for daily, period 168 (24*7) for weekly

from statsmodels.tsa.seasonal import STL

stl = STL(series, period=24, seasonal=7)
result = stl.fit()
```

## Practical Tips

- **Strong, consistent seasonality**: Seasonal naive or SARIMA often work well
- **Weak or irregular seasonality**: ML models may capture patterns better
- **Multiple seasonalities**: Consider Facebook Prophet or feature engineering for ML
- **Changing seasonality**: Use shorter training windows or adaptive methods
