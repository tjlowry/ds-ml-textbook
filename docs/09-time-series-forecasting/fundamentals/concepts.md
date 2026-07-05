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
