# Confidence Intervals

## Overview

A confidence interval (CI) provides a range of plausible values for a population parameter based on sample data. Unlike a point estimate (a single number), a confidence interval expresses our uncertainty about the true parameter value.

## The Concept of Confidence

### What is a Confidence Interval?

A 95% confidence interval means: if we repeated the sampling process many times and constructed a CI each time, approximately 95% of those intervals would contain the true population parameter.

### Common Misconceptions

```python
"""
WHAT A 95% CI DOES NOT MEAN:
- There is a 95% probability the parameter lies in this interval
- 95% of the data falls within this interval
- The parameter has a 95% chance of being in this specific interval

WHAT A 95% CI DOES MEAN:
- The procedure used to construct the interval will capture
  the true parameter 95% of the time in repeated sampling
- We have 95% confidence in the METHOD, not in any single interval
"""
```

### Demonstration of Confidence Level

```python
import numpy as np
from scipy import stats

# True population parameters
population_mean = 100
population_std = 15
sample_size = 30
confidence_level = 0.95

# Simulate many samples and their confidence intervals
np.random.seed(42)
n_simulations = 1000
intervals_containing_true_mean = 0

for _ in range(n_simulations):
    # Take a sample
    sample = np.random.normal(population_mean, population_std, sample_size)

    # Calculate CI
    sample_mean = np.mean(sample)
    se = stats.sem(sample)
    t_critical = stats.t.ppf((1 + confidence_level) / 2, sample_size - 1)
    ci_lower = sample_mean - t_critical * se
    ci_upper = sample_mean + t_critical * se

    # Check if true mean is in interval
    if ci_lower <= population_mean <= ci_upper:
        intervals_containing_true_mean += 1

coverage_rate = intervals_containing_true_mean / n_simulations
print(f"Theoretical confidence level: {confidence_level * 100}%")
print(f"Actual coverage rate: {coverage_rate * 100}%")
print(f"({intervals_containing_true_mean} out of {n_simulations} intervals)")
```

## Constructing Confidence Intervals

### General Formula

$$\text{CI} = \text{Point Estimate} \pm \text{Critical Value} \times \text{Standard Error}$$

### Components

1. **Point Estimate**: Sample statistic (e.g., sample mean)
2. **Critical Value**: Value from the appropriate distribution (z or t)
3. **Standard Error**: Standard deviation of the sampling distribution

## Confidence Interval for a Mean

### When Population Standard Deviation is Known (Z-interval)

$$\bar{x} \pm z_{\alpha/2} \cdot \frac{\sigma}{\sqrt{n}}$$

```python
import numpy as np
from scipy import stats

# Known population standard deviation
sample = [23, 25, 27, 24, 26, 28, 22, 25, 26, 24]
sigma = 3  # Known population std
confidence_level = 0.95

x_bar = np.mean(sample)
n = len(sample)
se = sigma / np.sqrt(n)

# Critical value from standard normal
z_critical = stats.norm.ppf((1 + confidence_level) / 2)

# Confidence interval
margin_of_error = z_critical * se
ci_lower = x_bar - margin_of_error
ci_upper = x_bar + margin_of_error

print("Z-Interval for Mean (sigma known)")
print("=" * 40)
print(f"Sample mean: {x_bar:.2f}")
print(f"Sample size: {n}")
print(f"Population std (sigma): {sigma}")
print(f"Standard error: {se:.4f}")
print(f"Z critical value: {z_critical:.4f}")
print(f"Margin of error: {margin_of_error:.4f}")
print(f"\n{confidence_level*100:.0f}% CI: ({ci_lower:.2f}, {ci_upper:.2f})")
```

### When Population Standard Deviation is Unknown (t-interval)

$$\bar{x} \pm t_{\alpha/2, n-1} \cdot \frac{s}{\sqrt{n}}$$

```python
import numpy as np
from scipy import stats

sample = [23, 25, 27, 24, 26, 28, 22, 25, 26, 24]
confidence_level = 0.95

x_bar = np.mean(sample)
s = np.std(sample, ddof=1)  # Sample std
n = len(sample)
se = s / np.sqrt(n)
df = n - 1

# Critical value from t-distribution
t_critical = stats.t.ppf((1 + confidence_level) / 2, df)

# Confidence interval
margin_of_error = t_critical * se
ci_lower = x_bar - margin_of_error
ci_upper = x_bar + margin_of_error

print("t-Interval for Mean (sigma unknown)")
print("=" * 40)
print(f"Sample mean: {x_bar:.2f}")
print(f"Sample std (s): {s:.2f}")
print(f"Sample size: {n}")
print(f"Degrees of freedom: {df}")
print(f"Standard error: {se:.4f}")
print(f"t critical value: {t_critical:.4f}")
print(f"Margin of error: {margin_of_error:.4f}")
print(f"\n{confidence_level*100:.0f}% CI: ({ci_lower:.2f}, {ci_upper:.2f})")

# Using scipy's built-in function
ci_scipy = stats.t.interval(confidence_level, df, loc=x_bar, scale=se)
print(f"\nUsing scipy: ({ci_scipy[0]:.2f}, {ci_scipy[1]:.2f})")
```

## Confidence Interval for a Proportion

### Formula

$$\hat{p} \pm z_{\alpha/2} \cdot \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$$

### Python Implementation

```python
import numpy as np
from scipy import stats

# Survey: 340 out of 500 respondents support a policy
successes = 340
n = 500
confidence_level = 0.95

# Sample proportion
p_hat = successes / n

# Standard error of proportion
se = np.sqrt(p_hat * (1 - p_hat) / n)

# Critical value
z_critical = stats.norm.ppf((1 + confidence_level) / 2)

# Confidence interval
margin_of_error = z_critical * se
ci_lower = p_hat - margin_of_error
ci_upper = p_hat + margin_of_error

print("Confidence Interval for Proportion")
print("=" * 40)
print(f"Successes: {successes}")
print(f"Sample size: {n}")
print(f"Sample proportion: {p_hat:.4f}")
print(f"Standard error: {se:.4f}")
print(f"Margin of error: {margin_of_error:.4f}")
print(f"\n{confidence_level*100:.0f}% CI: ({ci_lower:.4f}, {ci_upper:.4f})")
print(f"         or: ({ci_lower*100:.1f}%, {ci_upper*100:.1f}%)")

# Check if normal approximation is valid
if n * p_hat >= 10 and n * (1 - p_hat) >= 10:
    print("\nNormal approximation is valid (np >= 10 and n(1-p) >= 10)")
else:
    print("\nWarning: Normal approximation may not be valid")
```

### Wilson Score Interval (Better for Extreme Proportions)

```python
from scipy import stats
import numpy as np

def wilson_ci(successes, n, confidence=0.95):
    """
    Wilson score interval - better coverage for extreme proportions.
    """
    p_hat = successes / n
    z = stats.norm.ppf((1 + confidence) / 2)

    denominator = 1 + z**2 / n
    center = (p_hat + z**2 / (2*n)) / denominator
    spread = z * np.sqrt((p_hat * (1 - p_hat) + z**2 / (4*n)) / n) / denominator

    return center - spread, center + spread

# Compare methods for extreme proportion
successes = 5
n = 100

# Standard interval
p_hat = successes / n
se = np.sqrt(p_hat * (1 - p_hat) / n)
z = 1.96
ci_standard = (p_hat - z * se, p_hat + z * se)

# Wilson interval
ci_wilson = wilson_ci(successes, n)

print(f"Proportion: {p_hat:.2f} (small)")
print(f"Standard CI: ({ci_standard[0]:.4f}, {ci_standard[1]:.4f})")
print(f"Wilson CI:   ({ci_wilson[0]:.4f}, {ci_wilson[1]:.4f})")
print("\nNote: Wilson CI is preferred when p is near 0 or 1")
```

## Confidence Interval for Difference in Means

### Independent Samples

```python
import numpy as np
from scipy import stats

# Two independent groups
group1 = [23, 25, 27, 24, 26, 28, 22, 25, 26, 24]
group2 = [20, 22, 21, 23, 19, 24, 21, 22, 20, 23]
confidence_level = 0.95

n1, n2 = len(group1), len(group2)
x1_bar, x2_bar = np.mean(group1), np.mean(group2)
s1, s2 = np.std(group1, ddof=1), np.std(group2, ddof=1)

# Pooled standard error (assuming equal variances)
sp = np.sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / (n1 + n2 - 2))
se = sp * np.sqrt(1/n1 + 1/n2)
df = n1 + n2 - 2

# Critical value
t_critical = stats.t.ppf((1 + confidence_level) / 2, df)

# Confidence interval for difference
diff = x1_bar - x2_bar
margin_of_error = t_critical * se
ci_lower = diff - margin_of_error
ci_upper = diff + margin_of_error

print("CI for Difference in Means (Independent)")
print("=" * 45)
print(f"Group 1: mean = {x1_bar:.2f}, std = {s1:.2f}, n = {n1}")
print(f"Group 2: mean = {x2_bar:.2f}, std = {s2:.2f}, n = {n2}")
print(f"Difference (Group 1 - Group 2): {diff:.2f}")
print(f"Standard error: {se:.4f}")
print(f"\n{confidence_level*100:.0f}% CI: ({ci_lower:.2f}, {ci_upper:.2f})")

# Interpretation
if ci_lower > 0:
    print("\nInterpretation: Group 1 mean is significantly higher")
elif ci_upper < 0:
    print("\nInterpretation: Group 1 mean is significantly lower")
else:
    print("\nInterpretation: No significant difference (CI includes 0)")
```

### Paired Samples

```python
import numpy as np
from scipy import stats

# Before and after measurements
before = [180, 175, 190, 185, 170, 195, 188, 172, 183, 178]
after = [175, 170, 182, 180, 168, 188, 182, 170, 178, 175]
confidence_level = 0.95

# Calculate differences
differences = np.array(before) - np.array(after)
n = len(differences)
d_bar = np.mean(differences)
s_d = np.std(differences, ddof=1)
se = s_d / np.sqrt(n)
df = n - 1

# Critical value
t_critical = stats.t.ppf((1 + confidence_level) / 2, df)

# Confidence interval
margin_of_error = t_critical * se
ci_lower = d_bar - margin_of_error
ci_upper = d_bar + margin_of_error

print("CI for Mean Difference (Paired)")
print("=" * 40)
print(f"Mean difference: {d_bar:.2f}")
print(f"Std of differences: {s_d:.2f}")
print(f"Sample size: {n}")
print(f"Standard error: {se:.4f}")
print(f"\n{confidence_level*100:.0f}% CI: ({ci_lower:.2f}, {ci_upper:.2f})")

if ci_lower > 0:
    print("\nInterpretation: Significant decrease after treatment")
elif ci_upper < 0:
    print("\nInterpretation: Significant increase after treatment")
else:
    print("\nInterpretation: No significant change")
```

## Confidence Interval for Variance

### Chi-Square Based Interval

```python
import numpy as np
from scipy import stats

sample = [23, 25, 27, 24, 26, 28, 22, 25, 26, 24, 27, 23]
confidence_level = 0.95

n = len(sample)
s2 = np.var(sample, ddof=1)  # Sample variance
df = n - 1

# Chi-square critical values
chi2_lower = stats.chi2.ppf((1 - confidence_level) / 2, df)
chi2_upper = stats.chi2.ppf((1 + confidence_level) / 2, df)

# Confidence interval for variance
ci_var_lower = (df * s2) / chi2_upper
ci_var_upper = (df * s2) / chi2_lower

# Confidence interval for standard deviation
ci_std_lower = np.sqrt(ci_var_lower)
ci_std_upper = np.sqrt(ci_var_upper)

print("CI for Variance and Standard Deviation")
print("=" * 45)
print(f"Sample variance: {s2:.4f}")
print(f"Sample std dev: {np.sqrt(s2):.4f}")
print(f"Degrees of freedom: {df}")
print(f"\n{confidence_level*100:.0f}% CI for variance: ({ci_var_lower:.4f}, {ci_var_upper:.4f})")
print(f"{confidence_level*100:.0f}% CI for std dev: ({ci_std_lower:.4f}, {ci_std_upper:.4f})")
```

## Factors Affecting Confidence Interval Width

### Demonstration

```python
import numpy as np
from scipy import stats

def calculate_ci_width(n, s, confidence):
    """Calculate CI width for given parameters."""
    se = s / np.sqrt(n)
    t_critical = stats.t.ppf((1 + confidence) / 2, n - 1)
    return 2 * t_critical * se

# Base case
base_n = 30
base_s = 10
base_conf = 0.95

base_width = calculate_ci_width(base_n, base_s, base_conf)
print(f"Base case: n={base_n}, s={base_s}, conf={base_conf}")
print(f"CI Width: {base_width:.2f}")
print("\n" + "=" * 50)

# Effect of sample size
print("\nEffect of Sample Size:")
for n in [10, 30, 100, 500]:
    width = calculate_ci_width(n, base_s, base_conf)
    print(f"  n = {n:3d}: width = {width:.2f}")

# Effect of variability
print("\nEffect of Standard Deviation:")
for s in [5, 10, 20, 40]:
    width = calculate_ci_width(base_n, s, base_conf)
    print(f"  s = {s:2d}: width = {width:.2f}")

# Effect of confidence level
print("\nEffect of Confidence Level:")
for conf in [0.80, 0.90, 0.95, 0.99]:
    width = calculate_ci_width(base_n, base_s, conf)
    print(f"  conf = {conf:.2f}: width = {width:.2f}")
```

### Key Relationships

| Factor | Effect on CI Width |
|--------|-------------------|
| Increase sample size | Decreases width (narrower CI) |
| Increase variability | Increases width (wider CI) |
| Increase confidence level | Increases width (wider CI) |

## Sample Size Determination

### For Estimating a Mean

$$n = \left(\frac{z_{\alpha/2} \cdot \sigma}{E}\right)^2$$

Where $E$ is the desired margin of error.

```python
from scipy import stats
import numpy as np

def sample_size_for_mean(margin_of_error, std_dev, confidence=0.95):
    """
    Calculate required sample size to estimate a mean.

    Parameters:
    -----------
    margin_of_error : float
        Desired margin of error
    std_dev : float
        Estimated population standard deviation
    confidence : float
        Confidence level
    """
    z = stats.norm.ppf((1 + confidence) / 2)
    n = (z * std_dev / margin_of_error) ** 2
    return int(np.ceil(n))

# Example: Estimate mean salary within $2000
margin = 2000
sigma = 15000  # Estimated std dev from pilot study
confidence = 0.95

n_required = sample_size_for_mean(margin, sigma, confidence)
print(f"Sample Size Calculation for Mean")
print("=" * 40)
print(f"Desired margin of error: ${margin}")
print(f"Estimated std dev: ${sigma}")
print(f"Confidence level: {confidence*100}%")
print(f"\nRequired sample size: {n_required}")
```

### For Estimating a Proportion

$$n = \hat{p}(1-\hat{p})\left(\frac{z_{\alpha/2}}{E}\right)^2$$

```python
from scipy import stats
import numpy as np

def sample_size_for_proportion(margin_of_error, p_estimate=0.5, confidence=0.95):
    """
    Calculate required sample size to estimate a proportion.

    Parameters:
    -----------
    margin_of_error : float
        Desired margin of error (as decimal)
    p_estimate : float
        Estimated proportion (use 0.5 for maximum sample size)
    confidence : float
        Confidence level
    """
    z = stats.norm.ppf((1 + confidence) / 2)
    n = p_estimate * (1 - p_estimate) * (z / margin_of_error) ** 2
    return int(np.ceil(n))

# Example: Estimate voter preference within 3 percentage points
margin = 0.03
p_est = 0.5  # Conservative estimate (maximizes n)
confidence = 0.95

n_required = sample_size_for_proportion(margin, p_est, confidence)
print(f"Sample Size Calculation for Proportion")
print("=" * 40)
print(f"Desired margin of error: {margin*100}%")
print(f"Estimated proportion: {p_est}")
print(f"Confidence level: {confidence*100}%")
print(f"\nRequired sample size: {n_required}")

# What if we have a better estimate?
p_est_better = 0.7
n_better = sample_size_for_proportion(margin, p_est_better, confidence)
print(f"\nWith p estimate of {p_est_better}: n = {n_better}")
```

## Interpreting and Reporting Confidence Intervals

### Correct Interpretation

```python
# Example CI: (45.2, 52.8) for mean test score

interpretations = """
CORRECT INTERPRETATIONS:
- We are 95% confident that the true population mean lies between 45.2 and 52.8
- If we repeated this study many times, 95% of the resulting intervals would
  contain the true population mean
- The interval (45.2, 52.8) is one realization of a procedure that captures
  the true mean 95% of the time

INCORRECT INTERPRETATIONS:
- There is a 95% probability that the true mean is between 45.2 and 52.8
  (The true mean is fixed; it either is or isn't in the interval)
- 95% of all test scores fall between 45.2 and 52.8
  (CIs are about the mean, not individual scores)
- The mean will be in this interval 95% of the time
  (The CI is fixed; the mean doesn't move)
"""
print(interpretations)
```

### Reporting Guidelines

```python
# Example: Complete CI report
import numpy as np
from scipy import stats

sample = [72, 85, 88, 90, 91, 92, 93, 94, 95, 96, 97, 98]
confidence = 0.95

mean = np.mean(sample)
se = stats.sem(sample)
n = len(sample)
df = n - 1
t_crit = stats.t.ppf((1 + confidence) / 2, df)
ci = (mean - t_crit * se, mean + t_crit * se)

report = f"""
STATISTICAL REPORT
==================
Sample size: n = {n}
Mean: M = {mean:.2f}
Standard deviation: SD = {np.std(sample, ddof=1):.2f}
Standard error: SE = {se:.2f}
{confidence*100:.0f}% Confidence Interval: [{ci[0]:.2f}, {ci[1]:.2f}]

Written summary:
The mean score was {mean:.2f} (SD = {np.std(sample, ddof=1):.2f}).
The {confidence*100:.0f}% confidence interval for the population mean
ranged from {ci[0]:.2f} to {ci[1]:.2f}.
"""
print(report)
```

## Real-World Applications

### Medical Study Example

```python
import numpy as np
from scipy import stats

# Blood pressure reduction study
reductions = [8, 12, 5, 15, 10, 7, 11, 9, 13, 6, 14, 8, 10, 12, 9]

n = len(reductions)
mean_reduction = np.mean(reductions)
se = stats.sem(reductions)
df = n - 1

# 95% CI
ci_95 = stats.t.interval(0.95, df, loc=mean_reduction, scale=se)

# 99% CI
ci_99 = stats.t.interval(0.99, df, loc=mean_reduction, scale=se)

print("Blood Pressure Reduction Study")
print("=" * 50)
print(f"Sample size: {n} patients")
print(f"Mean reduction: {mean_reduction:.2f} mmHg")
print(f"Standard error: {se:.2f} mmHg")
print(f"\n95% CI: ({ci_95[0]:.2f}, {ci_95[1]:.2f}) mmHg")
print(f"99% CI: ({ci_99[0]:.2f}, {ci_99[1]:.2f}) mmHg")

print("\nClinical interpretation:")
if ci_95[0] > 5:  # Clinically meaningful threshold
    print(f"The treatment produces a clinically meaningful reduction")
    print(f"(lower bound {ci_95[0]:.1f} mmHg exceeds 5 mmHg threshold)")
else:
    print(f"The lower bound includes values below clinical significance")
```

### Quality Control Example

```python
import numpy as np
from scipy import stats

# Product weights (target: 500g)
weights = [498, 502, 501, 497, 503, 499, 500, 502, 498, 501,
           500, 499, 503, 497, 502, 500, 498, 501, 499, 500]

target = 500
tolerance = 5  # Acceptable range: 495-505g

n = len(weights)
mean_weight = np.mean(weights)
se = stats.sem(weights)

# 95% CI for mean
ci = stats.t.interval(0.95, n-1, loc=mean_weight, scale=se)

print("Quality Control: Product Weight Analysis")
print("=" * 50)
print(f"Target weight: {target}g (+/- {tolerance}g)")
print(f"Sample size: {n}")
print(f"Mean weight: {mean_weight:.2f}g")
print(f"95% CI: ({ci[0]:.2f}, {ci[1]:.2f})g")

# Check if process is centered
if ci[0] <= target <= ci[1]:
    print("\n[PASS] Target is within the confidence interval")
    print("Process appears to be centered correctly")
else:
    print("\n[WARNING] Target is outside the confidence interval")
    print("Process may need recalibration")
```

## Summary

| Parameter | Formula | Distribution |
|-----------|---------|--------------|
| Mean (sigma known) | $\bar{x} \pm z_{\alpha/2} \frac{\sigma}{\sqrt{n}}$ | Normal (Z) |
| Mean (sigma unknown) | $\bar{x} \pm t_{\alpha/2} \frac{s}{\sqrt{n}}$ | t-distribution |
| Proportion | $\hat{p} \pm z_{\alpha/2} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$ | Normal (Z) |
| Variance | $\frac{(n-1)s^2}{\chi^2_{\alpha/2}}$ to $\frac{(n-1)s^2}{\chi^2_{1-\alpha/2}}$ | Chi-square |

### Key Takeaways

1. Confidence intervals provide more information than point estimates
2. The confidence level refers to the long-run procedure, not a single interval
3. Wider intervals provide more confidence but less precision
4. Sample size planning can achieve desired precision before data collection
5. Always consider practical significance alongside statistical results

## How I Did It — MATH 425 (BYU-Idaho)

A fun MATH 425 problem tested a piece of folk wisdom: *"measure a child at age 2 and double it
to predict adult height."* Using the `BGSall` data (Berkeley children born 1928–29,
`library(alr4)`), I regressed 18-year height on 2-year height and turned the folk claim into a
hypothesis about the slope — if doubling is right, the slope should be exactly **2**:

```r
mylm <- lm(HT18 ~ HT2, data = BGSall)   # n = 136, so df = 134
summary(mylm)
```

The estimated slope was $b_1 = 1.4441$ with standard error 0.1901. Instead of the default test
against zero, I tested it against 2 by hand:

```r
t  <- (1.4441 - 2) / 0.1901         # = -2.924
2 * pt(-abs(t), 134)                # two-sided p-value = 0.00403
```

With **p = 0.004** I rejected $H_0: \beta_1 = 2$ — the slope is significantly **less** than 2,
so the "double it" rule systematically **over**predicts adult height.

Then the two-interval distinction that trips everyone up. To predict *one specific child's*
adult height I used a **prediction interval** (about individual variation), not a confidence
interval (about the mean response):

```r
# a child measured at 83.82 cm at age 2:
predict(mylm, data.frame(HT2 = 83.82), interval = "prediction")

confint(mylm)   # 95% CIs for the intercept and slope
```

Source: `~/Projects/school/byui-undergrad/MATH425/SkillsQuiz-ConfidenceAndPredictionIntervals.Rmd`

### Gotchas

- **You can test a slope against any value, not just 0.** `summary()` gives you the test
  against zero; for "is the slope 2?" you form $t = (b_1 - 2)/SE$ yourself and compare to
  `pt(..., df)`. Here that turned folk wisdom into a falsifiable claim.
- **Prediction interval ≠ confidence interval.** `interval = "prediction"` (a single new
  observation) is always wider than `interval = "confidence"` (the mean response) because it
  adds the individual error variance on top of the estimation uncertainty. Pick the one that
  matches the question.
- **Watch the df.** With $n = 136$ the reference distribution has 134 degrees of freedom — using
  a z-value instead of $t_{134}$ would understate the interval, especially for smaller samples.
