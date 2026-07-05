# Measures of Central Tendency

## Overview

Central tendency measures describe the "center" or "typical value" of a dataset. The three primary measures are the **mean**, **median**, and **mode**. Each has different properties and is appropriate in different situations.

## Mean (Arithmetic Average)

### Concept

The mean is the sum of all values divided by the number of values. It represents the "balance point" of the data distribution.

### Formula

**Population Mean:**
$$\mu = \frac{1}{N} \sum_{i=1}^{N} x_i$$

**Sample Mean:**
$$\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$$

Where:
- $N$ = population size
- $n$ = sample size
- $x_i$ = individual values

### Properties

- Uses all data points in calculation
- Sensitive to outliers (extreme values)
- The sum of deviations from the mean equals zero: $\sum(x_i - \bar{x}) = 0$
- Minimizes the sum of squared deviations

### Python Implementation

```python
import numpy as np
from scipy import stats

# Sample data
data = [23, 45, 67, 32, 89, 41, 56, 78, 34, 52]

# Calculate mean
mean_numpy = np.mean(data)
mean_builtin = sum(data) / len(data)

print(f"Mean (numpy): {mean_numpy}")
print(f"Mean (manual): {mean_builtin}")
# Output: Mean: 51.7
```

### Weighted Mean

When values have different importance (weights):

$$\bar{x}_w = \frac{\sum_{i=1}^{n} w_i x_i}{\sum_{i=1}^{n} w_i}$$

```python
values = [85, 90, 78, 92]
weights = [0.2, 0.3, 0.2, 0.3]  # Must sum to 1 (or be normalized)

weighted_mean = np.average(values, weights=weights)
print(f"Weighted mean: {weighted_mean}")
# Output: Weighted mean: 87.1
```

## Median

### Concept

The median is the middle value when data is sorted in order. It divides the dataset into two equal halves.

### Formula

For sorted data $x_1, x_2, \ldots, x_n$:

$$\text{Median} = \begin{cases}
x_{(n+1)/2} & \text{if } n \text{ is odd} \\
\frac{x_{n/2} + x_{(n/2)+1}}{2} & \text{if } n \text{ is even}
\end{cases}$$

### Properties

- Robust to outliers (resistant measure)
- Only considers the middle value(s)
- Better for skewed distributions
- Represents the 50th percentile

### Python Implementation

```python
import numpy as np

# Symmetric data
data_symmetric = [10, 20, 30, 40, 50]
median_sym = np.median(data_symmetric)
print(f"Median (symmetric): {median_sym}")  # Output: 30.0

# Data with outlier
data_outlier = [10, 20, 30, 40, 500]
mean_outlier = np.mean(data_outlier)
median_outlier = np.median(data_outlier)

print(f"Mean with outlier: {mean_outlier}")    # Output: 120.0
print(f"Median with outlier: {median_outlier}")  # Output: 30.0
# Median is unaffected by the outlier!
```

## Mode

### Concept

The mode is the most frequently occurring value in a dataset. A dataset can have:
- **No mode** (all values occur equally)
- **One mode** (unimodal)
- **Two modes** (bimodal)
- **Multiple modes** (multimodal)

### Properties

- Only measure applicable to categorical data
- Can identify peaks in distributions
- Not affected by extreme values
- May not exist or may not be unique

### Python Implementation

```python
from scipy import stats
from collections import Counter

# Numerical data
data = [1, 2, 2, 3, 3, 3, 4, 4, 5]

# Using scipy
mode_result = stats.mode(data, keepdims=True)
print(f"Mode: {mode_result.mode[0]}, Count: {mode_result.count[0]}")
# Output: Mode: 3, Count: 3

# Using Counter for multiple modes
def find_modes(data):
    counts = Counter(data)
    max_count = max(counts.values())
    modes = [value for value, count in counts.items() if count == max_count]
    return modes, max_count

# Bimodal data
bimodal_data = [1, 2, 2, 2, 3, 4, 4, 4, 5]
modes, count = find_modes(bimodal_data)
print(f"Modes: {modes}, Count: {count}")
# Output: Modes: [2, 4], Count: 3
```

## Choosing the Right Measure

### Decision Guide

| Situation | Recommended Measure | Reason |
|-----------|-------------------|--------|
| Symmetric distribution, no outliers | Mean | Uses all data efficiently |
| Skewed distribution | Median | Not affected by extreme values |
| Outliers present | Median | Robust to extreme values |
| Categorical data | Mode | Only applicable measure |
| Need mathematical tractability | Mean | Easier for further calculations |
| Income/housing prices | Median | Often right-skewed |

### Relationship in Different Distributions

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Generate different distributions
np.random.seed(42)

# Normal (symmetric)
normal_data = np.random.normal(50, 10, 1000)

# Right-skewed (positive skew)
right_skewed = np.random.exponential(10, 1000)

# Left-skewed (negative skew)
left_skewed = 100 - np.random.exponential(10, 1000)

def compare_measures(data, name):
    mean = np.mean(data)
    median = np.median(data)
    mode = stats.mode(np.round(data), keepdims=True).mode[0]

    print(f"\n{name}:")
    print(f"  Mean:   {mean:.2f}")
    print(f"  Median: {median:.2f}")
    print(f"  Mode:   {mode:.2f}")

    # Relationship
    if mean > median:
        print("  --> Right-skewed (Mean > Median)")
    elif mean < median:
        print("  --> Left-skewed (Mean < Median)")
    else:
        print("  --> Symmetric (Mean = Median)")

compare_measures(normal_data, "Normal Distribution")
compare_measures(right_skewed, "Right-Skewed Distribution")
compare_measures(left_skewed, "Left-Skewed Distribution")
```

## Trimmed Mean

A compromise between mean and median that removes extreme values before calculating:

```python
from scipy import stats

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]

regular_mean = np.mean(data)
trimmed_mean = stats.trim_mean(data, proportiontocut=0.1)  # Trim 10% from each end

print(f"Regular mean: {regular_mean:.2f}")   # Output: 14.50
print(f"Trimmed mean: {trimmed_mean:.2f}")   # Output: 5.50
```

## Real-World Applications

### Example 1: Salary Analysis

```python
import numpy as np
from scipy import stats

# Company salaries (including CEO)
salaries = [45000, 48000, 52000, 55000, 58000,
            62000, 65000, 70000, 75000, 500000]

mean_salary = np.mean(salaries)
median_salary = np.median(salaries)

print(f"Mean salary: ${mean_salary:,.2f}")
print(f"Median salary: ${median_salary:,.2f}")

# Output:
# Mean salary: $103,000.00
# Median salary: $60,000.00

# The median better represents a "typical" salary
# because the CEO's salary skews the mean upward
```

### Example 2: Student Grade Analysis

```python
import numpy as np
from scipy import stats

# Student scores
scores = [72, 85, 88, 90, 91, 92, 93, 94, 95, 96, 97, 98]

mean_score = np.mean(scores)
median_score = np.median(scores)
mode_result = stats.mode(scores, keepdims=True)

print(f"Mean score: {mean_score:.1f}")
print(f"Median score: {median_score:.1f}")
print(f"Grade distribution is approximately normal")
print(f"Mean and median are close, indicating symmetry")
```

### Example 3: Customer Survey (Categorical)

```python
from collections import Counter

# Customer satisfaction ratings
ratings = ['Good', 'Excellent', 'Good', 'Poor', 'Good',
           'Excellent', 'Good', 'Fair', 'Good', 'Excellent']

# Mode is the only appropriate measure for categorical data
rating_counts = Counter(ratings)
mode_rating = rating_counts.most_common(1)[0]

print(f"Most common rating: {mode_rating[0]} ({mode_rating[1]} responses)")
print(f"Full distribution: {dict(rating_counts)}")
```

## Summary

| Measure | Best For | Sensitive to Outliers | Data Type |
|---------|----------|----------------------|-----------|
| Mean | Symmetric distributions | Yes | Numerical |
| Median | Skewed distributions | No | Numerical/Ordinal |
| Mode | Most common value | No | Any (including categorical) |

Understanding when to use each measure is crucial for accurate data description and communication. Always consider the shape of your distribution and the presence of outliers when choosing a measure of central tendency.
