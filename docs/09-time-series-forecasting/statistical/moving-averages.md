# Moving Averages

## Overview

Moving averages smooth out short-term fluctuations to reveal underlying trends and patterns. They're both a forecasting technique and a data preprocessing tool.

## Simple Moving Average (SMA)

The SMA calculates the unweighted mean of the previous n observations.

```
SMA_t = (y_{t-1} + y_{t-2} + ... + y_{t-n}) / n
```

### Implementation

```python
import pandas as pd

# Calculate 7-day moving average
series['SMA_7'] = series['value'].rolling(window=7).mean()

# Calculate 30-day moving average
series['SMA_30'] = series['value'].rolling(window=30).mean()
```

### Choosing Window Size

| Window Size | Effect | Use Case |
|-------------|--------|----------|
| Small (3-7) | Responsive, more noise | Short-term patterns |
| Medium (10-30) | Balanced | General smoothing |
| Large (50+) | Very smooth, slow to react | Long-term trends |

## Weighted Moving Average (WMA)

Assigns different weights to different observations, typically giving more weight to recent values.

```
WMA_t = (w_1 × y_{t-1} + w_2 × y_{t-2} + ... + w_n × y_{t-n}) / Σw
```

### Implementation

```python
import numpy as np

def weighted_moving_average(series, window, weights=None):
    if weights is None:
        # Linear weights: most recent = highest weight
        weights = np.arange(1, window + 1)

    return series.rolling(window).apply(
        lambda x: np.sum(weights * x) / np.sum(weights)
    )

# Apply WMA
series['WMA_7'] = weighted_moving_average(series['value'], 7)
```

## Exponential Moving Average (EMA)

Weights decrease exponentially, giving much more importance to recent observations.

```
EMA_t = α × y_t + (1-α) × EMA_{t-1}
```

Where α (span parameter) controls the decay rate.

### Implementation

```python
# Pandas EMA with span parameter
# span=10 means approximately the last 10 observations matter most
series['EMA_10'] = series['value'].ewm(span=10).mean()

# Or specify alpha directly
series['EMA_alpha'] = series['value'].ewm(alpha=0.2).mean()
```

### Span vs Alpha Relationship

```
α = 2 / (span + 1)
```

| Span | Alpha | Behavior |
|------|-------|----------|
| 5 | 0.33 | Very responsive |
| 10 | 0.18 | Moderate |
| 20 | 0.095 | Smooth |
| 50 | 0.039 | Very smooth |

## Comparison of Moving Averages

| Type | Weighting | Lag | Smoothness |
|------|-----------|-----|------------|
| SMA | Equal | High | Moderate |
| WMA | Linear | Medium | Moderate |
| EMA | Exponential | Low | Adjustable |

## Using Moving Averages for Forecasting

### Naive MA Forecast

Use the most recent moving average as the forecast:

```python
# Forecast = most recent SMA value
window = 7
sma = series['value'].rolling(window=window).mean()
forecast = sma.iloc[-1]
```

### Double Moving Average (for Trends)

When data has a trend, use two moving averages:

```python
window = 5
sma1 = series['value'].rolling(window).mean()
sma2 = sma1.rolling(window).mean()

# Trend adjustment
a = 2 * sma1 - sma2
b = (2 / (window - 1)) * (sma1 - sma2)

# Forecast m periods ahead
forecast = a + b * m
```

## Moving Averages for Feature Engineering

Moving averages create valuable features for ML models:

```python
def add_ma_features(df, column, windows=[7, 14, 30]):
    for w in windows:
        df[f'SMA_{w}'] = df[column].rolling(window=w).mean()
        df[f'EMA_{w}'] = df[column].ewm(span=w).mean()
        df[f'MA_ratio_{w}'] = df[column] / df[f'SMA_{w}']  # Ratio to MA
    return df
```

Common features:
- **MA value**: Smoothed series
- **Ratio to MA**: Current value / MA (above or below trend)
- **MA crossovers**: Short MA vs Long MA (trend changes)
- **MA slope**: Rate of change of the MA

## Centered vs Trailing Moving Averages

### Trailing (Default)
Uses only past values—what you'd use in real forecasting:

```python
trailing_ma = series.rolling(window=7).mean()
# Value at time t uses observations from t-6 to t
```

### Centered
Uses values before and after—for analysis and decomposition:

```python
centered_ma = series.rolling(window=7, center=True).mean()
# Value at time t uses observations from t-3 to t+3
```

## Practical Applications

### 1. Trend Identification
```python
# Long MA reveals underlying trend
trend = series.rolling(30).mean()
```

### 2. Noise Reduction
```python
# Smooth noisy data before visualization
smoothed = series.ewm(span=10).mean()
```

### 3. Anomaly Detection
```python
# Flag values far from the moving average
ma = series.rolling(20).mean()
std = series.rolling(20).std()
anomalies = abs(series - ma) > 2 * std
```

### 4. Seasonal Adjustment
```python
# Remove seasonal pattern with seasonal-length MA
# For monthly data with yearly seasonality
seasonal_ma = series.rolling(12, center=True).mean()
deseasonalized = series / seasonal_ma  # If multiplicative
```

## Limitations

- **Lag**: Moving averages always lag behind the actual data
- **Window selection**: No universal optimal window size
- **Edge effects**: Missing values at the beginning (and end for centered)
- **Assumes patterns continue**: Cannot adapt to sudden changes
