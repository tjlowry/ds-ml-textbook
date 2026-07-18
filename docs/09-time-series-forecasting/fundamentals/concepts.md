# Time Series Concepts

## What is a Time Series?

A time series is a sequence of data points collected or recorded at successive points in time, usually at uniform intervals. Examples include:

- Daily stock prices
- Monthly sales figures
- Hourly temperature readings
- Weekly website traffic

## Components of a Time Series

Time series data can be decomposed into four main components:

### 1. Trend
The long-term movement or direction in the data. A trend can be:
- **Upward**: Values generally increasing over time
- **Downward**: Values generally decreasing over time
- **Stationary**: No clear long-term direction

### 2. Seasonality
Regular, predictable patterns that repeat at fixed intervals:
- **Daily**: Rush hour traffic patterns
- **Weekly**: Restaurant sales (higher on weekends)
- **Monthly**: Utility bills
- **Yearly**: Retail sales (holiday spikes)

### 3. Cyclical Patterns
Longer-term fluctuations that don't have a fixed period:
- Business cycles
- Economic expansions and recessions
- Multi-year industry trends

### 4. Irregular/Residual
Random, unpredictable variations that can't be attributed to trend, seasonality, or cycles:
- Unexpected events
- Measurement errors
- Random noise

## Additive vs Multiplicative Decomposition

### Additive Model
```
Y(t) = Trend + Seasonality + Residual
```
Use when seasonal variations are roughly constant regardless of the level of the series.

### Multiplicative Model
```
Y(t) = Trend × Seasonality × Residual
```
Use when seasonal variations change proportionally with the level of the series (e.g., retail sales where holiday spikes grow as the business grows).

## Time Series vs Cross-Sectional Data

| Aspect | Time Series | Cross-Sectional |
|--------|-------------|-----------------|
| Observations | Same entity over time | Different entities at one point |
| Independence | Observations are dependent | Observations often independent |
| Order | Order matters | Order doesn't matter |
| Example | Apple stock price 2020-2024 | Stock prices of 100 companies on Jan 1, 2024 |

## Key Terminology

- **Lag**: A previous time step (lag-1 is the previous observation)
- **Lead**: A future time step
- **Horizon**: How far into the future to forecast
- **Frequency**: How often observations are recorded (daily, weekly, etc.)
- **Window**: A subset of consecutive observations used for calculations

## How I did it

Real series are rarely on a clean, regular grid — the synthetic generator I used deliberately injects missing values and ~3% dropped days precisely because the real retail export had the same messiness. The senior project's fix was a resampling utility: reindex onto a regular frequency, then interpolate the holes.

```python
def resample_time_series(df, qty_col, freq='D', method='linear'):
    """Regularize an irregular series and interpolate missing values."""
    regular_index = pd.date_range(start=df.index.min(),
                                  end=df.index.max(), freq=freq)
    regular_series = df[qty_col].reindex(regular_index)   # gaps -> NaN
    if method in ('pad', 'ffill'):
        filled = regular_series.ffill()
    elif method == 'bfill':
        filled = regular_series.bfill()
    else:
        filled = regular_series.interpolate(method=method)
    out = pd.DataFrame(index=regular_index); out[qty_col] = filled
    return out
```

Source: `course-files/09-time-series-forecasting/time-series-forecasting/resampling-utilities.py` (`resample_time_series`)

My distribution demand-forecasting pipeline does the analogous thing at the aggregation step — daily transactions are summed into weekly totals and missing weeks are filled with zeros, because a gap in the calendar would silently corrupt every lag and rolling feature downstream (`demand-forecast/docs/technical_summary.md`, private distribution-forecasting repo, "Preprocessor").

## Gotchas

- **A DatetimeIndex is assumed everywhere.** The utility raises if the index isn't datetime; the very first preprocessing step in both projects is `pd.to_datetime` + `set_index`.
- **Interpolation vs zero-fill is a domain decision.** For the retail sales series, linear interpolation of a missing day is reasonable. For intermittent distribution demand, a "missing" week almost always means *no sale* — so my distribution-forecasting pipeline fills with **zeros**, not interpolation. Interpolating there would invent demand that never happened.
- **Regularize before EDA and before statistical models.** SARIMA/ETS need a fixed frequency; ACF/decomposition need no NaNs. Doing this first avoids a class of confusing downstream errors.
