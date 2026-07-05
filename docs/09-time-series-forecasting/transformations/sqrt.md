# Square Root Transformation

## Overview

The square root transformation is a milder alternative to log transformation, useful for moderately skewed data or count data.

## When to Use

- Data is **moderately right-skewed** (less extreme than log-appropriate data)
- Working with **count data** (Poisson-distributed)
- Variance increases with the level but not as dramatically as exponential growth
- Log transformation is too aggressive for your data

## Mathematical Form

```
y_transformed = √y
```

For back-transformation:
```
y_original = y_transformed²
```

## Implementation

```python
import numpy as np

# Basic square root transformation
df['sqrt_value'] = np.sqrt(df['value'])

# Handle negative values
def safe_sqrt_transform(series, offset=0):
    """Square root transform with offset for negative values."""
    min_val = series.min()
    if min_val < 0:
        offset = abs(min_val)
        print(f"Adding offset of {offset} to handle negative values")
    return np.sqrt(series + offset), offset

# Apply
df['sqrt_value'], offset = safe_sqrt_transform(df['value'])

# Back-transform predictions
df['predictions_original'] = df['predictions_sqrt'] ** 2 - offset
```

## Comparison with Log Transformation

| Aspect | Square Root | Log |
|--------|-------------|-----|
| Strength | Mild | Strong |
| Best for | Moderate skew | Strong skew |
| Handles zeros | Yes (√0 = 0) | No (log 0 undefined) |
| Negative values | Requires offset | Requires offset |
| Common use | Count data | Financial/growth data |

## Visual Effect

```python
import matplotlib.pyplot as plt
import numpy as np

# Generate sample skewed data
np.random.seed(42)
data = np.random.exponential(scale=100, size=1000)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].hist(data, bins=50)
axes[0].set_title('Original')

axes[1].hist(np.sqrt(data), bins=50)
axes[1].set_title('Square Root Transform')

axes[2].hist(np.log(data), bins=50)
axes[2].set_title('Log Transform')

plt.tight_layout()
plt.show()
```

## For Count Data

Square root transformation is particularly useful for count data (Poisson distribution), where variance equals the mean:

```python
# Count data example
daily_orders = [5, 12, 3, 8, 15, 2, 20, 7, 11, 4]

# Variance stabilization
sqrt_orders = np.sqrt(daily_orders)
# Variance is now approximately constant
```

## Practical Findings

From comparative studies:

> "Square root transformation showed moderate benefits for SARIMA and ETS models."

The square root transformation occupies a middle ground—gentler than log but still effective at variance stabilization for certain data types.

## Decision Guide

Choose square root when:
1. Log transform over-corrects (makes data left-skewed)
2. Data contains zeros that are meaningful
3. Skewness is moderate (1-2 range)
4. Working with count data
5. You want a reversible transformation that's easy to interpret
