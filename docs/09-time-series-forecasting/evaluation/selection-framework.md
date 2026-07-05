# Method Selection Framework

## Overview

This framework provides a structured approach to selecting the right forecasting method based on data characteristics and requirements.

## Decision Flowchart

```
START
  │
  ▼
┌─────────────────────────────┐
│ Do you have external        │
│ features to incorporate?    │
└─────────────────────────────┘
  │           │
  No          Yes
  │           │
  ▼           ▼
┌─────────┐ ┌─────────────────┐
│Statistical│ │ Consider ML    │
│ Methods  │ │ (XGBoost, RF)  │
└─────────┘ └─────────────────┘
  │
  ▼
┌─────────────────────────────┐
│ Is there clear seasonality? │
└─────────────────────────────┘
  │           │
  No          Yes
  │           │
  ▼           ▼
┌─────────┐ ┌─────────────────┐
│ ARIMA   │ │ SARIMA or ETS  │
│ or ETS  │ │ (Holt-Winters) │
└─────────┘ └─────────────────┘
```

## Step-by-Step Selection Process

### Step 1: Analyze Your Data

```python
def analyze_time_series(series, seasonal_period=None):
    """Comprehensive time series analysis."""
    from statsmodels.tsa.stattools import adfuller, acf
    from scipy.stats import skew, kurtosis

    print("=== Data Overview ===")
    print(f"Length: {len(series)}")
    print(f"Mean: {series.mean():.2f}")
    print(f"Std: {series.std():.2f}")
    print(f"Min: {series.min():.2f}")
    print(f"Max: {series.max():.2f}")

    print("\n=== Distribution ===")
    print(f"Skewness: {skew(series):.2f}")
    print(f"Kurtosis: {kurtosis(series):.2f}")

    print("\n=== Stationarity ===")
    adf_result = adfuller(series)
    print(f"ADF Statistic: {adf_result[0]:.4f}")
    print(f"p-value: {adf_result[1]:.4f}")
    print(f"Stationary: {'Yes' if adf_result[1] < 0.05 else 'No'}")

    if seasonal_period:
        print(f"\n=== Seasonality (period={seasonal_period}) ===")
        acf_values = acf(series, nlags=seasonal_period*2)
        seasonal_acf = acf_values[seasonal_period]
        print(f"ACF at seasonal lag: {seasonal_acf:.4f}")
        print(f"Strong seasonality: {'Yes' if abs(seasonal_acf) > 0.3 else 'No'}")

analyze_time_series(df['value'], seasonal_period=12)
```

### Step 2: Check Decision Criteria

| Criterion | Check | Implication |
|-----------|-------|-------------|
| **Sample size** | `len(series)` | <100: stat methods; >500: ML viable |
| **Stationarity** | ADF test | Non-stationary: need differencing or ML |
| **Seasonality** | ACF at seasonal lags | Strong: SARIMA/ETS; Weak: ARIMA/ML |
| **Trend** | Visual/decomposition | Present: need trend component |
| **External features** | Domain knowledge | Available: consider ML |
| **Outliers** | IQR or visual | Many: Random Forest more robust |

### Step 3: Run Baseline Models

Always start with simple baselines:

```python
def run_baselines(train, test, seasonal_period=1):
    """Run baseline forecasts."""
    results = {}

    # Naive
    naive_forecast = [train.iloc[-1]] * len(test)
    results['Naive'] = {
        'forecast': naive_forecast,
        'MAE': mean_absolute_error(test, naive_forecast)
    }

    # Seasonal Naive
    if seasonal_period > 1:
        seasonal_naive = [train.iloc[-(seasonal_period - i % seasonal_period)]
                        for i in range(len(test))]
        results['Seasonal Naive'] = {
            'forecast': seasonal_naive,
            'MAE': mean_absolute_error(test, seasonal_naive)
        }

    # Simple Moving Average
    ma_forecast = [train.rolling(7).mean().iloc[-1]] * len(test)
    results['MA(7)'] = {
        'forecast': ma_forecast,
        'MAE': mean_absolute_error(test, ma_forecast)
    }

    return results
```

### Step 4: Test Candidate Models

Based on analysis, test appropriate models:

```python
def test_candidates(train, test, candidates=['arima', 'ets', 'xgboost']):
    """Test candidate forecasting models."""
    results = {}

    if 'arima' in candidates:
        from pmdarima import auto_arima
        model = auto_arima(train, seasonal=False, suppress_warnings=True)
        forecast = model.predict(n_periods=len(test))
        results['ARIMA'] = {
            'model': model,
            'forecast': forecast,
            'MAE': mean_absolute_error(test, forecast)
        }

    if 'sarima' in candidates:
        from pmdarima import auto_arima
        model = auto_arima(train, seasonal=True, m=12, suppress_warnings=True)
        forecast = model.predict(n_periods=len(test))
        results['SARIMA'] = {
            'model': model,
            'forecast': forecast,
            'MAE': mean_absolute_error(test, forecast)
        }

    # Add more candidates as needed...

    return results
```

### Step 5: Compare and Select

```python
def compare_models(results):
    """Compare model performance."""
    comparison = pd.DataFrame([
        {'Model': name, 'MAE': res['MAE']}
        for name, res in results.items()
    ]).sort_values('MAE')

    print("=== Model Comparison ===")
    print(comparison.to_string(index=False))

    best_model = comparison.iloc[0]['Model']
    print(f"\nBest model: {best_model}")

    return best_model
```

## Transformation Decision Framework

Apply transformations only when:

1. ✓ Visual inspection shows **changing variance** over time
2. ✓ Statistical tests confirm **heteroscedasticity**
3. ✓ The data has **strong positive skew**
4. ✓ Model diagnostics show **non-normal residuals**

```python
def should_transform(series):
    """Determine if transformation is needed."""
    from scipy.stats import skew
    from statsmodels.stats.diagnostic import het_breuschpagan

    recommendations = []

    # Check skewness
    s = skew(series)
    if abs(s) > 1:
        recommendations.append(f"Skewness={s:.2f}: Consider log or sqrt transform")

    # Check for increasing variance (simple approach)
    first_half_var = series[:len(series)//2].var()
    second_half_var = series[len(series)//2:].var()
    var_ratio = second_half_var / first_half_var

    if var_ratio > 2:
        recommendations.append(f"Variance ratio={var_ratio:.2f}: Consider log transform")
    elif var_ratio < 0.5:
        recommendations.append(f"Variance ratio={var_ratio:.2f}: Variance decreasing (unusual)")

    if not recommendations:
        recommendations.append("No transformation strongly indicated")

    return recommendations

print(should_transform(df['value']))
```

## Quick Reference Table

| Situation | Primary Choice | Alternative |
|-----------|---------------|-------------|
| Short series, no seasonality | ETS(A,N,N) | ARIMA |
| Short series, clear seasonality | ETS(A,A,A) | SARIMA |
| Medium series, trend + seasonality | SARIMA | ETS |
| Long series, complex patterns | XGBoost | Random Forest |
| Many external features | XGBoost | Random Forest |
| Need prediction intervals | ETS | SARIMA |
| Outlier-heavy data | Random Forest | Robust ETS |
| Multiple seasonalities | Prophet | ML + features |
| Real-time requirements | ETS | Online learning |

## Final Checklist

Before finalizing your model:

- [ ] Compared against naive baseline
- [ ] Tested with proper time-based train/test split
- [ ] Checked residuals for remaining patterns
- [ ] Validated on multiple test periods if possible
- [ ] Considered computational requirements
- [ ] Evaluated prediction interval coverage (if applicable)
- [ ] Documented model selection rationale
