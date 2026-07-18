# Yeo-Johnson Transformation

## Overview

The Yeo-Johnson transformation is a modern extension of Box-Cox that works with negative values. It's often the best choice when your data contains zeros or negative numbers.

## Key Advantage Over Box-Cox

| Aspect | Box-Cox | Yeo-Johnson |
|--------|---------|-------------|
| Positive values | ✓ | ✓ |
| Zero values | ✗ | ✓ |
| Negative values | ✗ | ✓ |
| Offset needed | Often | Rarely |

## Mathematical Form

The Yeo-Johnson transformation uses different formulas depending on the sign of the value and the λ parameter:

For y ≥ 0:
- λ ≠ 0: `((y + 1)^λ - 1) / λ`
- λ = 0: `log(y + 1)`

For y < 0:
- λ ≠ 2: `-((-y + 1)^(2-λ) - 1) / (2 - λ)`
- λ = 2: `-log(-y + 1)`

## Implementation

```python
from scipy.stats import yeojohnson
from scipy.special import inv_boxcox
import numpy as np

# Yeo-Johnson works with any real values
transformed, lambda_optimal = yeojohnson(df['value'])
print(f"Optimal lambda: {lambda_optimal:.4f}")

df['yeojohnson_value'] = transformed
```

### Back-Transformation

```python
from scipy.special import inv_boxcox

def inverse_yeojohnson(y, lam):
    """Inverse Yeo-Johnson transformation."""
    y = np.asarray(y)
    result = np.zeros_like(y, dtype=float)

    # For transformed values that came from positive original values
    pos_mask = y >= 0
    if lam == 0:
        result[pos_mask] = np.exp(y[pos_mask]) - 1
    else:
        result[pos_mask] = (y[pos_mask] * lam + 1) ** (1/lam) - 1

    # For transformed values that came from negative original values
    neg_mask = ~pos_mask
    if lam == 2:
        result[neg_mask] = 1 - np.exp(-y[neg_mask])
    else:
        result[neg_mask] = 1 - ((2 - lam) * (-y[neg_mask]) + 1) ** (1/(2-lam))

    return result

# Back-transform predictions
df['predictions_original'] = inverse_yeojohnson(df['predictions_yj'], lambda_optimal)
```

### Using Scikit-Learn

```python
from sklearn.preprocessing import PowerTransformer

# Yeo-Johnson transformer
pt = PowerTransformer(method='yeo-johnson', standardize=True)

# Fit and transform
df['yeojohnson_value'] = pt.fit_transform(df[['value']])

# Back-transform
df['predictions_original'] = pt.inverse_transform(df[['predictions_yj']])

# Get the fitted lambda
print(f"Lambda: {pt.lambdas_[0]:.4f}")
```

## Comparison with Box-Cox

```python
import matplotlib.pyplot as plt
from scipy.stats import boxcox, yeojohnson
import numpy as np

# Create data with some negative values
np.random.seed(42)
data = np.random.normal(100, 50, 1000)  # Some values may be negative

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Original
axes[0].hist(data, bins=50)
axes[0].set_title('Original Distribution')

# Yeo-Johnson (works directly)
yj_transformed, yj_lambda = yeojohnson(data)
axes[1].hist(yj_transformed, bins=50)
axes[1].set_title(f'Yeo-Johnson (λ={yj_lambda:.2f})')

# Box-Cox (needs offset)
offset = abs(data.min()) + 1
bc_transformed, bc_lambda = boxcox(data + offset)
axes[2].hist(bc_transformed, bins=50)
axes[2].set_title(f'Box-Cox with offset (λ={bc_lambda:.2f})')

plt.tight_layout()
plt.show()
```

## When to Use Yeo-Johnson

- Data contains **zero or negative values**
- You want to avoid **arbitrary offset decisions**
- Working with **differenced data** (which often has negative values)
- Data represents **changes or returns** (can be positive or negative)
- You want a **general-purpose** transformation

## Practical Findings

From comparative analysis:

> "Yeo-Johnson Transformation: Modern alternative to Box-Cox that works with negative values. Automatically finds optimal lambda parameter. Often produces better results for complex distributions."

## Feature Scaling Note

When using with scikit-learn's `PowerTransformer`:

```python
# Option 1: Transform and standardize (default)
pt = PowerTransformer(method='yeo-johnson', standardize=True)
# Output has mean=0, std=1

# Option 2: Transform only
pt = PowerTransformer(method='yeo-johnson', standardize=False)
# Output is just transformed, not scaled
```

For time series forecasting, you typically want `standardize=False` to preserve the scale for interpretation.

## Decision Guide

| Data Characteristic | Recommended Transform |
|--------------------|----------------------|
| Strictly positive, strong skew | Box-Cox |
| Contains zeros | Yeo-Johnson |
| Contains negatives | Yeo-Johnson |
| Need interpretable λ | Box-Cox (λ values more intuitive) |
| General purpose | Yeo-Johnson |

## In my projects (honest note)

Neither project actually implemented Yeo-Johnson, so there's no real snippet here. The senior project's `apply_transformations` supported only `log`, `boxcox`, `sqrt`, and `diff` — Yeo-Johnson shows up only as a *conceptual* mention in the project notes:

> "Yeo-Johnson Transformation — Modern alternative to Box-Cox that works with negative values. Automatically finds optimal lambda parameter. Often produces better results for complex distributions."

Source: `course-files/09-time-series-forecasting/time-series-forecasting/docs/takeaways.md`

The code above (scipy `yeojohnson`, sklearn `PowerTransformer`) is the standard API, included for completeness — just flagging that it's reference material, not something I have project code behind.

## Gotchas

- **Where it *would* have earned its keep:** the [Differencing](differencing.md) branch produces negative values, and Box-Cox refuses negatives (needs an offset). Yeo-Johnson handles negatives natively, so "transform the differenced series" is the one spot in this project where reaching for Yeo-Johnson over Box-Cox would have been the cleaner call.
- **`PowerTransformer(standardize=True)` also rescales.** For forecasting you usually want `standardize=False` so the output keeps an interpretable scale — otherwise you've bundled a z-score into your transform.
