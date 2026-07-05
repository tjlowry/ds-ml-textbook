# Measures of Spread (Dispersion)

## Overview

Measures of spread describe how dispersed or scattered data values are around the center. While central tendency tells us about typical values, spread tells us about variability. Understanding spread is essential for assessing data reliability, comparing groups, and making predictions.

## Range

### Concept

The range is the simplest measure of spread: the difference between the maximum and minimum values.

### Formula

$$\text{Range} = x_{\max} - x_{\min}$$

### Properties

- Easy to calculate and interpret
- Extremely sensitive to outliers
- Uses only two data points
- Increases with sample size

### Python Implementation

```python
import numpy as np

data = [15, 22, 29, 31, 38, 42, 55, 61, 78, 85]

range_value = np.max(data) - np.min(data)
# Or equivalently:
range_value = np.ptp(data)  # "peak to peak"

print(f"Range: {range_value}")  # Output: Range: 70
```

## Interquartile Range (IQR)

### Concept

The IQR is the range of the middle 50% of the data, calculated as the difference between the 75th percentile (Q3) and 25th percentile (Q1).

### Formula

$$\text{IQR} = Q_3 - Q_1$$

Where:
- $Q_1$ = 25th percentile (first quartile)
- $Q_3$ = 75th percentile (third quartile)

### Properties

- Robust to outliers
- Describes spread of central data
- Used in box plots
- Foundation for identifying outliers

### Python Implementation

```python
import numpy as np
from scipy import stats

data = [12, 15, 18, 22, 25, 28, 31, 35, 42, 88, 95]

# Calculate quartiles
Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)
IQR = Q3 - Q1

# Using scipy
IQR_scipy = stats.iqr(data)

print(f"Q1: {Q1}")
print(f"Q3: {Q3}")
print(f"IQR: {IQR}")
print(f"IQR (scipy): {IQR_scipy}")

# Outlier detection using IQR
lower_fence = Q1 - 1.5 * IQR
upper_fence = Q3 + 1.5 * IQR

outliers = [x for x in data if x < lower_fence or x > upper_fence]
print(f"\nOutlier fences: [{lower_fence:.1f}, {upper_fence:.1f}]")
print(f"Outliers: {outliers}")
```

## Variance

### Concept

Variance measures the average squared deviation from the mean. It quantifies how far data points are spread from the center.

### Formula

**Population Variance:**
$$\sigma^2 = \frac{1}{N} \sum_{i=1}^{N} (x_i - \mu)^2$$

**Sample Variance (unbiased):**
$$s^2 = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})^2$$

The denominator $(n-1)$ is called "degrees of freedom" and corrects for bias when estimating population variance from a sample.

### Properties

- Always non-negative
- Units are squared (e.g., dollars squared)
- Sensitive to outliers
- Mathematically convenient for theory

### Python Implementation

```python
import numpy as np

data = [4, 8, 6, 5, 3, 7, 9, 5, 6, 7]

# Sample variance (default, ddof=1)
sample_variance = np.var(data, ddof=1)

# Population variance (ddof=0)
population_variance = np.var(data, ddof=0)

# Manual calculation
mean = np.mean(data)
squared_deviations = [(x - mean)**2 for x in data]
manual_variance = sum(squared_deviations) / (len(data) - 1)

print(f"Sample variance: {sample_variance:.4f}")
print(f"Population variance: {population_variance:.4f}")
print(f"Manual calculation: {manual_variance:.4f}")
```

### Why n-1? (Bessel's Correction)

```python
import numpy as np

# Demonstration: sample variance underestimates population variance
np.random.seed(42)
population = np.random.normal(50, 10, 10000)
true_variance = np.var(population, ddof=0)

# Take many samples and compute variances
n_samples = 1000
sample_size = 30

biased_variances = []    # Using n
unbiased_variances = []  # Using n-1

for _ in range(n_samples):
    sample = np.random.choice(population, sample_size, replace=False)
    biased_variances.append(np.var(sample, ddof=0))
    unbiased_variances.append(np.var(sample, ddof=1))

print(f"True population variance: {true_variance:.2f}")
print(f"Mean of biased estimates (n): {np.mean(biased_variances):.2f}")
print(f"Mean of unbiased estimates (n-1): {np.mean(unbiased_variances):.2f}")
# The n-1 version is closer to the true variance on average
```

## Standard Deviation

### Concept

The standard deviation is the square root of the variance. It measures spread in the original units of measurement.

### Formula

**Population Standard Deviation:**
$$\sigma = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (x_i - \mu)^2}$$

**Sample Standard Deviation:**
$$s = \sqrt{\frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})^2}$$

### Properties

- Same units as the original data
- Easier to interpret than variance
- For normal distributions: ~68% of data within 1 SD, ~95% within 2 SD
- Can be used to standardize data (z-scores)

### Python Implementation

```python
import numpy as np

data = [72, 85, 88, 90, 91, 92, 93, 94, 95, 96]

# Calculate standard deviation
sample_std = np.std(data, ddof=1)  # Sample (n-1)
population_std = np.std(data, ddof=0)  # Population (n)

mean = np.mean(data)

print(f"Mean: {mean:.2f}")
print(f"Sample std dev: {sample_std:.2f}")
print(f"Population std dev: {population_std:.2f}")

# Interpretation for normal data
print(f"\nExpected ranges (assuming normality):")
print(f"  68% of data: [{mean - sample_std:.1f}, {mean + sample_std:.1f}]")
print(f"  95% of data: [{mean - 2*sample_std:.1f}, {mean + 2*sample_std:.1f}]")
print(f"  99.7% of data: [{mean - 3*sample_std:.1f}, {mean + 3*sample_std:.1f}]")
```

### Z-Scores (Standardization)

```python
import numpy as np
from scipy import stats

data = [65, 70, 75, 80, 85, 90, 95, 100]

# Calculate z-scores
z_scores = stats.zscore(data, ddof=1)

# Manual calculation
mean = np.mean(data)
std = np.std(data, ddof=1)
z_manual = [(x - mean) / std for x in data]

print("Original | Z-Score")
print("-" * 20)
for orig, z in zip(data, z_scores):
    print(f"   {orig}    |  {z:.2f}")

# Z-scores tell us how many standard deviations from the mean
# A z-score of 2 means the value is 2 standard deviations above the mean
```

## Coefficient of Variation (CV)

### Concept

The CV expresses the standard deviation as a percentage of the mean, allowing comparison of variability between datasets with different units or scales.

### Formula

$$CV = \frac{s}{\bar{x}} \times 100\%$$

### Python Implementation

```python
import numpy as np
from scipy import stats

# Compare variability of two measurements with different scales
heights_cm = [165, 170, 175, 180, 185]  # Heights in cm
weights_kg = [60, 65, 70, 75, 80]        # Weights in kg

cv_heights = (np.std(heights_cm, ddof=1) / np.mean(heights_cm)) * 100
cv_weights = (np.std(weights_kg, ddof=1) / np.mean(weights_kg)) * 100

# Using scipy
cv_scipy_heights = stats.variation(heights_cm, ddof=1) * 100
cv_scipy_weights = stats.variation(weights_kg, ddof=1) * 100

print(f"Heights - Mean: {np.mean(heights_cm):.1f} cm, Std: {np.std(heights_cm, ddof=1):.2f} cm")
print(f"Heights CV: {cv_heights:.2f}%")

print(f"\nWeights - Mean: {np.mean(weights_kg):.1f} kg, Std: {np.std(weights_kg, ddof=1):.2f} kg")
print(f"Weights CV: {cv_weights:.2f}%")

# The CV allows us to compare variability despite different units
```

## Mean Absolute Deviation (MAD)

### Concept

MAD is the average of absolute deviations from the mean. It's more robust to outliers than variance.

### Formula

$$MAD = \frac{1}{n} \sum_{i=1}^{n} |x_i - \bar{x}|$$

### Python Implementation

```python
import numpy as np
from scipy import stats

data = [10, 12, 15, 18, 20, 22, 25, 100]  # Note the outlier

# Mean Absolute Deviation from mean
mean = np.mean(data)
mad_from_mean = np.mean(np.abs(data - mean))

# Median Absolute Deviation (more robust)
median = np.median(data)
mad_from_median = np.median(np.abs(data - median))

# scipy's median_abs_deviation
mad_scipy = stats.median_abs_deviation(data)

print(f"Mean: {mean:.2f}")
print(f"Median: {median:.2f}")
print(f"Std Dev: {np.std(data, ddof=1):.2f}")
print(f"MAD from mean: {mad_from_mean:.2f}")
print(f"MAD from median (scipy): {mad_scipy:.2f}")
```

## Comparing Measures of Spread

```python
import numpy as np
from scipy import stats

# Data without outliers
clean_data = [45, 48, 52, 55, 58, 62, 65, 68, 72, 75]

# Data with outliers
outlier_data = [45, 48, 52, 55, 58, 62, 65, 68, 72, 500]

def spread_summary(data, name):
    print(f"\n{name}")
    print("=" * 40)
    print(f"Range: {np.ptp(data):.2f}")
    print(f"IQR: {stats.iqr(data):.2f}")
    print(f"Variance: {np.var(data, ddof=1):.2f}")
    print(f"Std Dev: {np.std(data, ddof=1):.2f}")
    print(f"CV: {stats.variation(data, ddof=1)*100:.2f}%")
    print(f"MAD: {stats.median_abs_deviation(data):.2f}")

spread_summary(clean_data, "Clean Data")
spread_summary(outlier_data, "Data with Outlier")

# Notice how range, variance, and std dev are heavily affected by the outlier
# while IQR and MAD remain relatively stable
```

## Real-World Applications

### Example 1: Quality Control

```python
import numpy as np
from scipy import stats

# Manufacturing: Bolt diameter measurements (mm)
machine_A = [10.02, 10.01, 9.99, 10.00, 10.01, 9.98, 10.02, 10.00, 9.99, 10.01]
machine_B = [10.05, 9.95, 10.10, 9.90, 10.03, 9.97, 10.08, 9.92, 10.06, 9.94]

target = 10.00  # Target diameter

for name, data in [("Machine A", machine_A), ("Machine B", machine_B)]:
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    cv = stats.variation(data, ddof=1) * 100

    print(f"\n{name}:")
    print(f"  Mean: {mean:.3f} mm (Target: {target})")
    print(f"  Std Dev: {std:.4f} mm")
    print(f"  CV: {cv:.2f}%")
    print(f"  Range: [{min(data):.2f}, {max(data):.2f}]")

# Machine A has lower variability = more consistent output
```

### Example 2: Investment Risk

```python
import numpy as np

# Monthly returns for two stocks (%)
stock_A = [2.1, -1.5, 3.2, 0.8, -0.5, 2.8, 1.2, -2.1, 4.5, 1.8]
stock_B = [0.5, 0.3, 0.8, 0.2, 0.4, 0.6, 0.3, 0.1, 0.7, 0.4]

for name, returns in [("Stock A", stock_A), ("Stock B", stock_B)]:
    mean_return = np.mean(returns)
    volatility = np.std(returns, ddof=1)  # Volatility = standard deviation
    sharpe_like = mean_return / volatility  # Simplified risk-adjusted return

    print(f"\n{name}:")
    print(f"  Mean return: {mean_return:.2f}%")
    print(f"  Volatility (Std Dev): {volatility:.2f}%")
    print(f"  Return/Risk ratio: {sharpe_like:.2f}")

# Stock A has higher returns but also higher risk
# Stock B has lower returns but is more stable
```

### Example 3: Test Score Analysis

```python
import numpy as np
from scipy import stats

# Two classes took the same exam
class_A = [72, 75, 78, 80, 82, 85, 88, 90, 92, 95]
class_B = [65, 70, 75, 80, 85, 90, 95, 100, 55, 60]

for name, scores in [("Class A", class_A), ("Class B", class_B)]:
    print(f"\n{name}:")
    print(f"  Mean: {np.mean(scores):.1f}")
    print(f"  Median: {np.median(scores):.1f}")
    print(f"  Std Dev: {np.std(scores, ddof=1):.1f}")
    print(f"  IQR: {stats.iqr(scores):.1f}")
    print(f"  Range: {np.ptp(scores)}")

# Class A: More homogeneous performance
# Class B: More variable performance (wider ability range)
```

## Summary Table

| Measure | Formula | Robust to Outliers | Units | Use Case |
|---------|---------|-------------------|-------|----------|
| Range | max - min | No | Original | Quick overview |
| IQR | Q3 - Q1 | Yes | Original | Robust spread, box plots |
| Variance | Mean of squared deviations | No | Squared | Statistical theory |
| Std Dev | Square root of variance | No | Original | Most common measure |
| CV | Std Dev / Mean | No | Percentage | Compare across scales |
| MAD | Mean/Median absolute deviation | Yes | Original | Robust alternative to std dev |

## Key Takeaways

1. **Range** is simple but sensitive to outliers
2. **IQR** is robust and useful for identifying outliers
3. **Variance** is mathematically convenient but in squared units
4. **Standard deviation** is the most commonly used measure
5. **CV** allows comparison across different scales
6. **MAD** provides a robust alternative when outliers are present

Always consider the nature of your data and the presence of outliers when choosing a measure of spread.
