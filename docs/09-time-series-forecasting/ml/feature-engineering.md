# Feature Engineering for Time Series

## Overview

Machine learning models treat forecasting as a supervised learning problem. Unlike statistical methods that model temporal dependencies directly, ML models require explicit feature engineering to capture time-based patterns.

## Lag Features

Lag features use past values as predictors for the current value.

```python
def create_lag_features(df, column, lags):
    """Create lag features for a time series."""
    for lag in lags:
        df[f'{column}_lag_{lag}'] = df[column].shift(lag)
    return df

# Example: Create lags 1-7 for daily data
df = create_lag_features(df, 'sales', lags=range(1, 8))
```

### Choosing Lag Values

| Data Frequency | Common Lags | Rationale |
|----------------|-------------|-----------|
| Daily | 1, 7, 14, 21, 28 | Yesterday, same weekday |
| Weekly | 1, 4, 13, 52 | Last week, month, quarter, year |
| Monthly | 1, 3, 6, 12 | Last month, quarter, half-year, year |

## Rolling Window Statistics

Capture recent trends and volatility with rolling calculations.

```python
def create_rolling_features(df, column, windows):
    """Create rolling statistics."""
    for w in windows:
        df[f'{column}_roll_mean_{w}'] = df[column].shift(1).rolling(w).mean()
        df[f'{column}_roll_std_{w}'] = df[column].shift(1).rolling(w).std()
        df[f'{column}_roll_min_{w}'] = df[column].shift(1).rolling(w).min()
        df[f'{column}_roll_max_{w}'] = df[column].shift(1).rolling(w).max()
    return df

# Example
df = create_rolling_features(df, 'sales', windows=[7, 14, 30])
```

**Important**: Always use `.shift(1)` before rolling to prevent data leakage—you shouldn't include the current observation in features predicting the current value.

## Calendar Features

Extract time-based features that capture seasonality and patterns.

```python
def create_calendar_features(df, date_column):
    """Create calendar-based features."""
    df['day_of_week'] = df[date_column].dt.dayofweek
    df['day_of_month'] = df[date_column].dt.day
    df['day_of_year'] = df[date_column].dt.dayofyear
    df['week_of_year'] = df[date_column].dt.isocalendar().week
    df['month'] = df[date_column].dt.month
    df['quarter'] = df[date_column].dt.quarter
    df['year'] = df[date_column].dt.year
    df['is_weekend'] = df[date_column].dt.dayofweek.isin([5, 6]).astype(int)
    df['is_month_start'] = df[date_column].dt.is_month_start.astype(int)
    df['is_month_end'] = df[date_column].dt.is_month_end.astype(int)
    return df
```

### Cyclical Encoding

For cyclical features (day of week, month), use sine/cosine encoding:

```python
import numpy as np

def cyclical_encode(df, column, max_val):
    """Encode cyclical features using sin/cos."""
    df[f'{column}_sin'] = np.sin(2 * np.pi * df[column] / max_val)
    df[f'{column}_cos'] = np.cos(2 * np.pi * df[column] / max_val)
    return df

# Day of week (0-6, so max_val=7)
df = cyclical_encode(df, 'day_of_week', 7)

# Month (1-12, so max_val=12)
df = cyclical_encode(df, 'month', 12)
```

This ensures Monday is close to Sunday, December is close to January.

## Holiday Features

```python
from pandas.tseries.holiday import USFederalHolidayCalendar

def create_holiday_features(df, date_column):
    """Add holiday indicators."""
    cal = USFederalHolidayCalendar()
    holidays = cal.holidays(start=df[date_column].min(),
                           end=df[date_column].max())

    df['is_holiday'] = df[date_column].isin(holidays).astype(int)

    # Days until/since holiday
    df['days_to_holiday'] = df[date_column].apply(
        lambda x: min((holidays - x).days, default=999) if (holidays >= x).any() else 999
    )
    return df
```

## Expanding Window Features

For features that use all available history:

```python
def create_expanding_features(df, column):
    """Create expanding window statistics."""
    df[f'{column}_expanding_mean'] = df[column].shift(1).expanding().mean()
    df[f'{column}_expanding_std'] = df[column].shift(1).expanding().std()
    return df
```

## Difference Features

Capture trends and changes:

```python
def create_diff_features(df, column, periods):
    """Create difference features."""
    for p in periods:
        df[f'{column}_diff_{p}'] = df[column].diff(p)
        df[f'{column}_pct_change_{p}'] = df[column].pct_change(p)
    return df

# Change from yesterday, last week, last month
df = create_diff_features(df, 'sales', periods=[1, 7, 30])
```

## Complete Feature Engineering Pipeline

```python
def engineer_features(df, target_column, date_column):
    """Complete feature engineering pipeline."""

    # Sort by date
    df = df.sort_values(date_column).reset_index(drop=True)

    # Lag features
    df = create_lag_features(df, target_column, lags=[1, 2, 3, 7, 14, 21, 28])

    # Rolling features
    df = create_rolling_features(df, target_column, windows=[7, 14, 30])

    # Calendar features
    df = create_calendar_features(df, date_column)

    # Cyclical encoding
    df = cyclical_encode(df, 'day_of_week', 7)
    df = cyclical_encode(df, 'month', 12)

    # Difference features
    df = create_diff_features(df, target_column, periods=[1, 7])

    # Drop rows with NaN from feature creation
    df = df.dropna()

    return df
```

## Avoiding Data Leakage

**Critical**: Features must only use information available at prediction time.

### Common Leakage Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Rolling mean without shift | Includes current value | Use `.shift(1).rolling()` |
| Future calendar features | Knows future dates | Only use past patterns |
| Target encoding without CV | Uses test set info | Use proper CV fold encoding |

### Validation Strategy

Always use time-based splits:

```python
# Correct: Time-based split
train = df[df['date'] < '2023-01-01']
test = df[df['date'] >= '2023-01-01']

# Wrong: Random split (causes leakage)
# train, test = train_test_split(df, test_size=0.2)  # DON'T DO THIS
```

## Feature Selection

Too many features can hurt performance. Consider:

```python
from sklearn.feature_selection import SelectKBest, f_regression

# Select top k features
selector = SelectKBest(f_regression, k=20)
X_selected = selector.fit_transform(X_train, y_train)

# Or use model-based importance
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(X_train, y_train)
importances = pd.Series(model.feature_importances_, index=X_train.columns)
top_features = importances.nlargest(20).index.tolist()
```

## How I did it

This is the topic where the two projects contrast most sharply — the same idea (turn a series into supervised rows) at school-project scale vs production scale.

**School project — one flat function on a single series.** `create_features` builds calendar fields plus two lags and two rolling stats, then drops the NaN rows:

```python
def create_features(df):
    df_features = df.copy()
    df_features['dayofweek'] = df_features.index.dayofweek
    df_features['month'] = df_features.index.month
    df_features['quarter'] = df_features.index.quarter
    df_features['year'] = df_features.index.year
    df_features['dayofyear'] = df_features.index.dayofyear
    df_features['lag_1'] = df_features['Qty'].shift(1)
    df_features['lag_7'] = df_features['Qty'].shift(7)
    df_features['rolling_mean_7'] = df_features['Qty'].rolling(window=7).mean()
    df_features['rolling_std_7'] = df_features['Qty'].rolling(window=7).std()
    return df_features.dropna()
```

Source: `course-files/09-time-series-forecasting/time-series-forecasting/forecasting-pipeline.py` (`create_features`)

**Production — a grouped, config-driven, leakage-tested feature layer.** My distribution demand-forecasting pipeline computes lags *per Stock/Warehouse group*, log-transforms before lagging, and filters out lags longer than 80% of a series' length (dynamic selection). The leakage rule is spelled out in the docstring and enforced by `.shift(lag)`:

```python
# DATA LEAKAGE PREVENTION:
# - Uses pandas .shift(lag) which ONLY looks backward in time
# - lag_1 at time t = demand at time t-1 (previous period)
# - Features are computed per stock/warehouse group independently
result[feature_name] = result.groupby(
    ['Stock', 'Warehouse']
)['_target_for_lag'].shift(lag)
```

Source: `demand-forecast/src/features/lag.py` (private distribution-forecasting repo; `LagFeatureEngineer.transform`)

Rolling features apply `.shift(1)` **before** `.rolling()` so the current period is never inside its own window:

```python
def _calculate_rolling_stat(self, series, window, stat):
    # Create rolling window (shifted to exclude current value)
    rolling = series.shift(1).rolling(window=window, min_periods=self.min_periods)
    if stat == 'mean':  return rolling.mean()
    elif stat == 'std': return rolling.std()
    # ... min / max / median / sum / var
```

Source: `demand-forecast/src/features/rolling.py` (private distribution-forecasting repo; `RollingFeatureEngineer._calculate_rolling_stat`)

The production system also has temporal (cyclic sin/cos), hierarchical (class-level lagged aggregates), and SBC demand-pattern features — ~45 columns in total (`docs/technical_summary.md`).

## Notebook

See the rendered notebook: [Distribution Feature Engineering Demo](../notebooks/distribution-feature-engineering-demo.ipynb) — it recreates the leakage-safe lag/rolling logic on a synthetic weekly demand panel and asserts, the way `tests/test_data_leakage.py` does, that no feature at week *t* uses week *t*'s demand.

Re-run locally: `jupyter lab docs/09-time-series-forecasting/notebooks/distribution-feature-engineering-demo.ipynb`

## Gotchas

- **`.shift(1)` before `.rolling()` is the whole ballgame.** `series.rolling(7).mean()` includes the current value — that's leakage. The correct form is `series.shift(1).rolling(7).mean()`. The school project's `create_features` did *not* shift before rolling (`rolling_mean_7` includes the current row), which is fine-ish when you then split by index but is exactly the bug the production code was written to prevent.
- **Group before you shift on a panel.** With multiple Stock/Warehouse series stacked in one frame, a plain `.shift(1)` leaks the *last row of the previous item* into the *first row of the next*. Production shifts inside `groupby(['Stock','Warehouse'])`.
- **Long lags nuke short series.** A `lag_52` on a 30-week item is all-NaN. Dynamic selection (drop lags > 80% of length) keeps short SKUs usable instead of dropping them entirely.
- **Log-transform before lagging, not after.** Demand is right-skewed; my distribution-forecasting pipeline applies `np.log1p` to the target *before* creating lags so the lag features live in the compressed space the model trains on.
- **`.dropna()` costs you rows.** Every lag/rolling window eats warm-up rows off the front. On short series that adds up fast — another reason dynamic selection matters.
