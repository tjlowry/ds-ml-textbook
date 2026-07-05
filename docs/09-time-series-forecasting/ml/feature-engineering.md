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
