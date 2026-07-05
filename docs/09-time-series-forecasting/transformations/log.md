# Log Transformation

## Overview

The log transformation compresses large values and spreads out small values, making it useful for data with exponential growth or right-skewed distributions.

## When to Use

- Data shows **exponential growth** patterns
- **Variance increases** with the level of the series
- Distribution is **right-skewed** (long tail on the right)
- You want to convert **multiplicative relationships** to additive

## Mathematical Form

```
y_transformed = log(y)
```

For back-transformation:
```
y_original = exp(y_transformed)
```

## Implementation

```python
import numpy as np
import pandas as pd

# Basic log transformation
df['log_value'] = np.log(df['value'])

# Handle zeros and negative values
def safe_log_transform(series, offset=1):
    """Log transform with offset for non-positive values."""
    min_val = series.min()
    if min_val <= 0:
        offset = abs(min_val) + 1
        print(f"Adding offset of {offset} to handle non-positive values")
    return np.log(series + offset), offset

# Apply
df['log_value'], offset = safe_log_transform(df['value'])

# Back-transform predictions
df['predictions_original'] = np.exp(df['predictions_log']) - offset
```

## Effect on Data

### Before Log Transform
- Mean: 1000
- Std: 500
- Skewness: 2.5 (right-skewed)

### After Log Transform
- Mean: 6.8
- Std: 0.5
- Skewness: 0.3 (approximately symmetric)

## Visual Comparison

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Original distribution
axes[0].hist(df['value'], bins=50)
axes[0].set_title('Original Distribution')

# Log-transformed distribution
axes[1].hist(df['log_value'], bins=50)
axes[1].set_title('Log-Transformed Distribution')

plt.tight_layout()
plt.show()
```

## Important Considerations

### Handling Non-Positive Values

Log is undefined for zero and negative values. Common solutions:

1. **Add constant offset**: `log(y + 1)` or `log(y + c)` where c makes all values positive
2. **Use log1p**: `np.log1p(y)` which computes `log(1 + y)` with better numerical precision
3. **Signed log**: For data with negative values, use `sign(y) * log(|y| + 1)`

### Back-Transformation Bias

When forecasting in log space, the back-transformed mean is biased:

```python
# Naive back-transform (biased)
forecast_biased = np.exp(log_forecast)

# Bias correction (if residuals are normal)
sigma_squared = np.var(log_residuals)
forecast_corrected = np.exp(log_forecast + sigma_squared / 2)
```

## When Log Transformation Helps

| Scenario | Log Transform Effect |
|----------|---------------------|
| Exponential trend | Linearizes the trend |
| Increasing variance | Stabilizes variance |
| Multiplicative seasonality | Converts to additive |
| Right-skewed data | Makes distribution more symmetric |

## When NOT to Use

- Data is already normally distributed
- Series contains zeros or negative values that have meaning
- Relationships are already linear
- Small variance doesn't change with level

## Practical Findings

From empirical testing on retail forecasting data:

> "Transformations didn't universally improve forecasting accuracy for this dataset. The untransformed data ('none' option) performed best for most models."

> "Some models inherently handle non-normal data better than others; XGBoost performed well without transformations."

**Key takeaway**: Don't apply log transformation by default—test whether it actually improves your specific model and data.
