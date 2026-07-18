# Naive Methods

Naive methods serve as essential baselines that any sophisticated model should outperform. If a complex model can't beat a naive approach, it's not adding value.

## Naive Forecast

### Definition
The naive forecast uses the last observed value as the prediction for all future periods.

```python
# Naive forecast: predict the last known value
forecast = [series.iloc[-1]] * forecast_horizon
```

### When Naive Works Well

- The time series is essentially a **random walk**
- Very **short-term forecasts** are needed
- Data is extremely **volatile with no discernible pattern**
- As a **benchmark** for more complex models

**Example**: Daily cryptocurrency prices often behave like random walks, making naive forecasts surprisingly competitive.

### Limitations

- Ignores all historical patterns except the most recent value
- Cannot capture trends or seasonality
- Performs poorly when clear patterns exist

## Seasonal Naive

### Definition
Seasonal naive uses the value from the same period in the previous seasonal cycle.

```python
# Seasonal naive: use value from same period last season
# For weekly seasonality:
forecast_monday = last_monday_value
forecast_tuesday = last_tuesday_value
# etc.
```

### Implementation

```python
def seasonal_naive(series, season_length, horizon):
    """
    Generate seasonal naive forecast.

    Parameters:
    - series: historical data
    - season_length: number of periods in one season (e.g., 7 for weekly, 12 for yearly)
    - horizon: number of periods to forecast
    """
    forecasts = []
    for i in range(horizon):
        # Get value from same position in previous season
        idx = len(series) - season_length + (i % season_length)
        forecasts.append(series.iloc[idx])
    return forecasts
```

### When Seasonal Naive Works Well

- **Strong, consistent seasonality** dominates the series
- **Limited historical data** is available
- The pattern repeats **almost exactly** each season
- Simple forecasting is needed for **planning purposes**

**Example**: Weekly store traffic patterns that follow consistent day-of-week patterns.

### Limitations

- Assumes seasonality is perfectly consistent
- Cannot adapt to changing patterns or trends
- Ignores recent level changes

## Comparison

| Method | Captures Trend | Captures Seasonality | Best For |
|--------|---------------|---------------------|----------|
| Naive | No | No | Random walks, very short-term |
| Seasonal Naive | No | Yes (fixed) | Stable seasonal patterns |

## Using Naive Methods as Baselines

Always compare your model against naive baselines:

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Calculate errors for your model
model_mae = mean_absolute_error(actual, model_forecast)
model_rmse = np.sqrt(mean_squared_error(actual, model_forecast))

# Calculate errors for naive baseline
naive_mae = mean_absolute_error(actual, naive_forecast)
naive_rmse = np.sqrt(mean_squared_error(actual, naive_forecast))

# Skill score: how much better than naive?
skill_score = 1 - (model_mae / naive_mae)
print(f"Skill Score: {skill_score:.2%}")
# Positive = better than naive, Negative = worse than naive
```

## Key Insight

In practice, seasonal naive sometimes outperforms complex models on highly seasonal data. During a senior project comparing forecasting methods on retail data:

> "Seasonal Naive approach performed significantly worse than even simple Naive forecasting, suggesting weak weekly seasonality patterns in the data."

This finding highlights the importance of understanding your data's characteristics before selecting a forecasting method.

## How I did it

Both naive baselines were a single small function. Last-value naive is one line; seasonal naive walks back one weekly cycle per horizon step:

```python
def run_naive_forecast(train, test):
    # Last value forecast
    naive_forecast = np.array([train['Qty'].iloc[-1]] * len(test))

    # Seasonal naive (same day last week)
    seasonal_naive = []
    for i in range(len(test)):
        seasonal_naive.append(train['Qty'].iloc[-(7 + (i % 7))])
    return naive_forecast, seasonal_naive
```

Source: `course-files/09-time-series-forecasting/time-series-forecasting/forecasting-pipeline.py` (`run_naive_forecast`)

My distribution demand-forecasting production pipeline keeps a seasonal-naive path too, but as a **fallback** (`_apply_seasonal_naive_fallback` in `src/pipeline.py`) for stocks where the trained models can't beat it — and it measures everything in MASE, which is literally "how much better than seasonal naive is this?" (MASE < 1.0 means you beat the baseline). The baseline is baked into the metric.

## Gotchas

- **Seasonal naive is *not* a safe default.** The headline finding was that it did *worse* than plain last-value naive, because the retail series had weak weekly seasonality. If the season you assume isn't really there, seasonal naive just injects noise.
- **Index the seasonal lookback carefully.** `iloc[-(7 + (i % 7))]` reaches back exactly one weekly cycle and cycles through the days — off-by-one here silently shifts the whole forecast by a day.
- **Always ship a baseline.** In practice "beat naive" is the bar. The production system enforces this by reporting MASE against seasonal naive for every single stock.
