# Box-Cox Transformation

## Overview

The Box-Cox transformation automatically finds the optimal power transformation to normalize data. It generalizes several common transformations (log, square root, reciprocal) into a single framework.

## Mathematical Form

For λ ≠ 0:
```
y_transformed = (y^λ - 1) / λ
```

For λ = 0:
```
y_transformed = log(y)
```

## Special Cases of Lambda

| λ (Lambda) | Transformation | Equivalent To |
|------------|----------------|---------------|
| -1 | Reciprocal | 1/y |
| -0.5 | Reciprocal square root | 1/√y |
| 0 | Natural log | log(y) |
| 0.5 | Square root | √y |
| 1 | No transformation | y (linear) |
| 2 | Square | y² |

## Implementation

```python
from scipy.stats import boxcox
from scipy.special import inv_boxcox
import numpy as np

# Data must be strictly positive
# Add offset if necessary
min_val = df['value'].min()
if min_val <= 0:
    offset = abs(min_val) + 1
    data = df['value'] + offset
else:
    offset = 0
    data = df['value']

# Apply Box-Cox transformation
transformed, lambda_optimal = boxcox(data)
print(f"Optimal lambda: {lambda_optimal:.4f}")

# Store for back-transformation
df['boxcox_value'] = transformed

# Back-transform predictions
df['predictions_original'] = inv_boxcox(df['predictions_boxcox'], lambda_optimal) - offset
```

## Finding Optimal Lambda

The optimal λ is found by maximizing the log-likelihood of the transformed data being normally distributed.

```python
from scipy.stats import boxcox_normmax

# Find optimal lambda without transforming
lambda_optimal = boxcox_normmax(data)
print(f"Optimal lambda: {lambda_optimal}")

# Or get both transformation and lambda
transformed, fitted_lambda = boxcox(data)
```

## Visual Comparison

```python
import matplotlib.pyplot as plt
from scipy.stats import boxcox, probplot

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Original data
axes[0, 0].hist(df['value'], bins=50)
axes[0, 0].set_title('Original Distribution')

# Q-Q plot original
probplot(df['value'], plot=axes[0, 1])
axes[0, 1].set_title('Q-Q Plot (Original)')

# Box-Cox transformed
transformed, lam = boxcox(df['value'])
axes[1, 0].hist(transformed, bins=50)
axes[1, 0].set_title(f'Box-Cox Transformed (λ={lam:.3f})')

# Q-Q plot transformed
probplot(transformed, plot=axes[1, 1])
axes[1, 1].set_title('Q-Q Plot (Box-Cox)')

plt.tight_layout()
plt.show()
```

## Requirements and Limitations

### Requirements
- **Strictly positive data**: All values must be > 0
- **Sufficient sample size**: Need enough data for reliable λ estimation

### Handling Non-Positive Values

```python
def box_cox_transform(series):
    """Apply Box-Cox with automatic offset handling."""
    min_val = series.min()

    if min_val <= 0:
        offset = abs(min_val) + 1
        print(f"Adding offset of {offset} for Box-Cox (requires positive values)")
        adjusted_series = series + offset
    else:
        offset = 0
        adjusted_series = series

    transformed, lambda_val = boxcox(adjusted_series)

    return transformed, lambda_val, offset


def inverse_box_cox(transformed, lambda_val, offset=0):
    """Back-transform Box-Cox values."""
    original = inv_boxcox(transformed, lambda_val)
    return original - offset
```

## When Box-Cox Excels

- You want the **data to determine** the best transformation
- Multiple transformations are reasonable candidates
- **Normalizing residuals** for statistical tests
- Preparing data for models that assume normality

## Practical Considerations

### Pros
- **Automatic**: Finds optimal transformation mathematically
- **Flexible**: Adapts to different data characteristics
- **Principled**: Based on maximum likelihood theory

### Cons
- **Requires positive data**: Needs workarounds for zeros/negatives
- **Interpretability**: λ values aren't always intuitive
- **Stability**: λ can be sensitive to outliers

## Practical Findings

From empirical testing:

> "Transformations should be applied selectively based on diagnostic tests rather than by default."

> "The effectiveness of transformations varies by model type—statistical models (ARIMA, ETS) responded differently than machine learning approaches (XGBoost)."

## Decision Framework

Apply Box-Cox transformation only when:

1. **Visual inspection** shows changing variance over time
2. **Statistical tests** confirm heteroscedasticity
3. The data has **strong positive skew**
4. **Model diagnostics** show non-normal residuals

If the optimal λ is close to 1, the transformation isn't adding value—use the original data.
