# Autocorrelation (ACF/PACF)

## What is Autocorrelation?

Autocorrelation measures how correlated a time series is with lagged versions of itself. It answers: "How much does today's value depend on yesterday's value? Last week's value?"

## Autocorrelation Function (ACF)

The ACF shows the correlation between observations at different lags, including both direct and indirect effects.

### Interpretation
- **Lag 0**: Always 1 (perfect correlation with itself)
- **Lag 1**: Correlation between consecutive observations
- **Lag k**: Correlation between observations k periods apart

### Plotting ACF

```python
from statsmodels.graphics.tsaplots import plot_acf
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 4))
plot_acf(series, lags=40, ax=ax)
plt.show()
```

### Reading ACF Plots

| Pattern | Interpretation |
|---------|----------------|
| Slow decay | Non-stationary data (needs differencing) |
| Spikes at seasonal lags | Seasonality present (e.g., spikes at 12, 24, 36 for monthly data with yearly seasonality) |
| Sharp cutoff after lag q | MA(q) process |
| Exponential decay | AR process |

## Partial Autocorrelation Function (PACF)

The PACF shows the direct correlation between observations at lag k, removing the effects of intermediate lags.

### Why PACF Matters

- ACF at lag 2 includes both: direct effect of lag-2 AND indirect effect through lag-1
- PACF at lag 2 shows only the direct effect of lag-2

### Plotting PACF

```python
from statsmodels.graphics.tsaplots import plot_pacf

fig, ax = plt.subplots(figsize=(10, 4))
plot_pacf(series, lags=40, ax=ax)
plt.show()
```

### Reading PACF Plots

| Pattern | Interpretation |
|---------|----------------|
| Sharp cutoff after lag p | AR(p) process |
| Exponential decay | MA process |
| Spikes at seasonal lags | Seasonal AR component |

## Using ACF/PACF for Model Selection

### ARIMA Order Selection

| ACF | PACF | Model |
|-----|------|-------|
| Cuts off after lag q | Decays gradually | MA(q) |
| Decays gradually | Cuts off after lag p | AR(p) |
| Decays gradually | Decays gradually | ARMA(p,q) |

### Practical Example

```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(14, 4))

plot_acf(series, lags=30, ax=axes[0])
axes[0].set_title('Autocorrelation Function')

plot_pacf(series, lags=30, ax=axes[1])
axes[1].set_title('Partial Autocorrelation Function')

plt.tight_layout()
plt.show()
```

## Significance Bounds

The shaded region in ACF/PACF plots represents the 95% confidence interval:

- Values within the shaded region are not statistically significant
- Values outside indicate significant autocorrelation at that lag

The bounds are approximately ±1.96/√n, where n is the sample size.

## Common Patterns

### Random Walk (Non-Stationary)
- **ACF**: Very slow decay, stays high for many lags
- **PACF**: Single spike at lag 1, then drops to zero
- **Action**: Apply differencing

### White Noise (Stationary, No Pattern)
- **ACF**: All values within confidence bounds (except lag 0)
- **PACF**: All values within confidence bounds
- **Action**: Data is already unpredictable; naive forecast may be best

### Seasonal Data
- **ACF**: Spikes at seasonal lags (e.g., 12, 24, 36 for yearly seasonality)
- **PACF**: Similar spikes at seasonal lags
- **Action**: Use SARIMA or seasonal decomposition

## Diagnostic Use

After fitting a model, check the residuals' ACF:

```python
# Residuals should look like white noise
from statsmodels.graphics.tsaplots import plot_acf

residuals = model.resid
plot_acf(residuals, lags=30)
```

If significant autocorrelation remains in residuals, the model hasn't captured all the temporal structure.

## How I did it

The senior project produced stacked ACF/PACF plots as part of EDA, dropping NaNs first (ACF/PACF choke on missing values):

```python
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(df['Qty'].dropna(), ax=ax1)
plot_pacf(df['Qty'].dropna(), ax=ax2)
```

Source: `course-files/09-time-series-forecasting/time-series-forecasting/forecasting-pipeline.py` (`run_eda`)

Beyond eyeballing the plots, I used the ACF *programmatically* to pick seasonal periods — finding local maxima and ranking them by correlation strength (see `detect_seasonality_periods` on the [Seasonality & Trends](seasonality-trends.md) page). That turns "read the spikes off the chart" into an automatic step.

## Gotchas

- **Drop NaNs first.** `plot_acf` / `plot_pacf` and `acf()` error on missing values; the real code calls `.dropna()` every time. If your series has gaps, regularize and interpolate *before* looking at autocorrelation.
- **`fft=True` for long series.** In `detect_seasonality_periods` the ACF is computed with `acf(..., fft=True)` — much faster once `max_lag` gets into the hundreds.
- **A slowly-decaying ACF is a differencing signal, not a model choice.** On the raw (non-stationary) retail series the ACF stayed high for many lags; that's the cue to difference (or, for the tree model, to just add lag features and move on).
