# P-Values and Statistical Significance

## Overview

The p-value is one of the most used (and misused) concepts in statistics. Understanding what p-values actually mean, their limitations, and common misconceptions is essential for properly interpreting statistical results.

## What is a P-Value?

### Definition

The p-value is the probability of observing results as extreme as, or more extreme than, the observed data, **assuming the null hypothesis is true**.

$$p\text{-value} = P(\text{data as extreme or more extreme} \mid H_0 \text{ is true})$$

### Key Points

- P-values assume H0 is true
- They measure compatibility of data with H0
- They do NOT measure the probability that H0 is true
- They do NOT measure the probability that results occurred by chance

### Visual Understanding

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Example: Testing if mean differs from 100
# Sample gives t-statistic of 2.5 with df=29

t_stat = 2.5
df = 29

# Create t-distribution
x = np.linspace(-4, 4, 1000)
y = stats.t.pdf(x, df)

# Calculate p-value (two-tailed)
p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))

print("P-Value Calculation")
print("=" * 40)
print(f"Test statistic: t = {t_stat}")
print(f"Degrees of freedom: {df}")
print(f"P-value (two-tailed): {p_value:.4f}")
print(f"\nInterpretation:")
print(f"If H0 were true, the probability of observing")
print(f"a t-statistic as extreme as {t_stat} is {p_value:.4f}")
```

## Calculating P-Values

### For Different Test Statistics

```python
from scipy import stats
import numpy as np

# Z-test (known population std)
z_stat = 2.1
p_value_z_two = 2 * (1 - stats.norm.cdf(abs(z_stat)))
p_value_z_right = 1 - stats.norm.cdf(z_stat)
p_value_z_left = stats.norm.cdf(z_stat)

print("Z-Test P-Values (z = 2.1)")
print("-" * 30)
print(f"Two-tailed: {p_value_z_two:.4f}")
print(f"Right-tailed: {p_value_z_right:.4f}")
print(f"Left-tailed: {p_value_z_left:.4f}")

# t-test (unknown population std)
t_stat = 2.1
df = 15
p_value_t_two = 2 * (1 - stats.t.cdf(abs(t_stat), df))
p_value_t_right = 1 - stats.t.cdf(t_stat, df)
p_value_t_left = stats.t.cdf(t_stat, df)

print(f"\nt-Test P-Values (t = 2.1, df = {df})")
print("-" * 30)
print(f"Two-tailed: {p_value_t_two:.4f}")
print(f"Right-tailed: {p_value_t_right:.4f}")
print(f"Left-tailed: {p_value_t_left:.4f}")

# Chi-square test
chi2_stat = 15.5
df_chi = 8
p_value_chi = 1 - stats.chi2.cdf(chi2_stat, df_chi)

print(f"\nChi-Square P-Value (chi2 = {chi2_stat}, df = {df_chi})")
print("-" * 30)
print(f"Right-tailed: {p_value_chi:.4f}")

# F-test
f_stat = 3.2
df1, df2 = 5, 20
p_value_f = 1 - stats.f.cdf(f_stat, df1, df2)

print(f"\nF-Test P-Value (F = {f_stat}, df1 = {df1}, df2 = {df2})")
print("-" * 30)
print(f"Right-tailed: {p_value_f:.4f}")
```

### Complete Example with scipy

```python
from scipy import stats
import numpy as np

# One-sample t-test
sample = [23, 25, 27, 24, 26, 28, 22, 25, 26, 24]
mu_0 = 22  # Hypothesized mean

# scipy computes the two-tailed p-value automatically
t_stat, p_value = stats.ttest_1samp(sample, mu_0)

print("One-Sample t-Test")
print("=" * 40)
print(f"H0: mu = {mu_0}")
print(f"H1: mu != {mu_0}")
print(f"\nSample mean: {np.mean(sample):.2f}")
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value (two-tailed): {p_value:.4f}")

# For one-tailed test, divide p-value by 2 (if direction matches)
if t_stat > 0:  # Sample mean > hypothesized mean
    p_right = p_value / 2
    p_left = 1 - p_right
else:
    p_left = p_value / 2
    p_right = 1 - p_left

print(f"\np-value (right-tailed, H1: mu > {mu_0}): {p_right:.4f}")
print(f"p-value (left-tailed, H1: mu < {mu_0}): {p_left:.4f}")
```

## Significance Levels (Alpha)

### Concept

The significance level ($\alpha$) is the threshold for deciding whether a p-value is "small enough" to reject H0.

### Common Significance Levels

```python
significance_levels = """
COMMON ALPHA LEVELS:
====================

alpha = 0.10 (10%)
- Less stringent
- Used in exploratory analysis
- Higher chance of false positives

alpha = 0.05 (5%)
- Most commonly used
- Conventional standard
- "Statistically significant" often means p < 0.05

alpha = 0.01 (1%)
- More stringent
- Used when false positives are costly
- Required in some fields (e.g., particle physics uses ~0.0000003)

DECISION RULE:
- If p-value < alpha: Reject H0 (result is "statistically significant")
- If p-value >= alpha: Fail to reject H0 (result is "not statistically significant")
"""
print(significance_levels)
```

### Choosing Alpha

```python
alpha_guidelines = """
FACTORS IN CHOOSING ALPHA:
===========================

1. CONSEQUENCES OF ERRORS
   - High cost of Type I error (false positive) -> lower alpha
   - High cost of Type II error (false negative) -> higher alpha

2. FIELD CONVENTIONS
   - Medical research: often 0.05 or 0.01
   - Physics: ~0.0000003 (5 sigma)
   - Social sciences: usually 0.05

3. EXPLORATORY VS CONFIRMATORY
   - Exploratory: may use 0.10
   - Confirmatory: typically 0.05 or lower

4. MULTIPLE TESTING
   - Many tests increase false positive rate
   - May need to adjust alpha (Bonferroni, FDR)

IMPORTANT: Set alpha BEFORE analyzing data!
"""
print(alpha_guidelines)
```

## Common Misconceptions

### Misconception 1: P-value is the probability H0 is true

```python
misconception_1 = """
WRONG: "The p-value of 0.03 means there's only a 3% chance the null
        hypothesis is true."

CORRECT: "The p-value of 0.03 means that IF the null hypothesis were true,
          there's a 3% chance of observing results this extreme or more extreme."

The p-value tells us about P(data | H0), not P(H0 | data).
These are NOT the same thing!

Example: If p = 0.03
- We can say: "These results are unlikely under H0"
- We CANNOT say: "There's a 97% chance H1 is true"
"""
print(misconception_1)
```

### Misconception 2: P-value measures effect size

```python
import numpy as np
from scipy import stats

# Demonstration: Same effect, different p-values
effect_size = 5  # True difference between means

# Small sample
np.random.seed(42)
small_sample_1 = np.random.normal(100, 15, 10)
small_sample_2 = np.random.normal(100 + effect_size, 15, 10)
t_small, p_small = stats.ttest_ind(small_sample_1, small_sample_2)

# Large sample
large_sample_1 = np.random.normal(100, 15, 1000)
large_sample_2 = np.random.normal(100 + effect_size, 15, 1000)
t_large, p_large = stats.ttest_ind(large_sample_1, large_sample_2)

print("Same Effect Size, Different P-Values")
print("=" * 50)
print(f"True effect size: {effect_size}")
print(f"\nSmall samples (n=10 each):")
print(f"  Observed difference: {np.mean(small_sample_2) - np.mean(small_sample_1):.2f}")
print(f"  p-value: {p_small:.4f}")

print(f"\nLarge samples (n=1000 each):")
print(f"  Observed difference: {np.mean(large_sample_2) - np.mean(large_sample_1):.2f}")
print(f"  p-value: {p_large:.4f}")

print("\nLesson: P-values depend on BOTH effect size AND sample size!")
print("A small p-value doesn't necessarily mean a large effect.")
```

### Misconception 3: Non-significant means no effect

```python
import numpy as np
from scipy import stats

# Demonstration: Real effect, but not enough power to detect it
np.random.seed(123)

# True effect exists (effect size = 3)
true_effect = 3
sigma = 15
n = 10  # Small sample

group1 = np.random.normal(100, sigma, n)
group2 = np.random.normal(100 + true_effect, sigma, n)

t_stat, p_value = stats.ttest_ind(group1, group2)

print("Non-Significant Does NOT Mean 'No Effect'")
print("=" * 50)
print(f"True effect size: {true_effect}")
print(f"Sample size per group: {n}")
print(f"Observed difference: {np.mean(group2) - np.mean(group1):.2f}")
print(f"p-value: {p_value:.4f}")

if p_value >= 0.05:
    print("\nResult: NOT statistically significant at alpha = 0.05")
    print("\nBUT this doesn't mean there's no effect!")
    print("Possible reasons for non-significance:")
    print("  1. Sample size too small (low power)")
    print("  2. High variability in data")
    print("  3. True effect is small")
    print("\nAbsence of evidence is NOT evidence of absence!")
```

### Misconception 4: Significance equals importance

```python
import numpy as np
from scipy import stats

# Demonstration: Statistically significant but practically meaningless
np.random.seed(42)

# Very small effect, but huge sample
n = 100000
effect = 0.1  # Tiny effect

group1 = np.random.normal(100, 15, n)
group2 = np.random.normal(100 + effect, 15, n)

t_stat, p_value = stats.ttest_ind(group1, group2)

# Effect size (Cohen's d)
pooled_std = np.sqrt((np.var(group1, ddof=1) + np.var(group2, ddof=1)) / 2)
cohens_d = (np.mean(group2) - np.mean(group1)) / pooled_std

print("Statistical vs Practical Significance")
print("=" * 50)
print(f"Sample size per group: {n:,}")
print(f"Observed difference: {np.mean(group2) - np.mean(group1):.4f}")
print(f"p-value: {p_value:.6f}")
print(f"Cohen's d (effect size): {cohens_d:.4f}")

print("\nResult: HIGHLY statistically significant!")
print("But the effect is TINY (d < 0.01)")
print("\nStatistical significance tells you IF there's an effect.")
print("Effect size tells you HOW BIG the effect is.")
print("Always report both!")
```

## Effect Sizes

### Why Report Effect Sizes?

```python
effect_size_importance = """
EFFECT SIZES complement p-values by telling us:
===============================================

1. MAGNITUDE of the effect (how big is the difference?)
2. PRACTICAL SIGNIFICANCE (does it matter in real life?)
3. COMPARABILITY across studies
4. Foundation for META-ANALYSIS

P-VALUE alone cannot tell you:
- Whether the effect is large enough to matter
- Whether results are practically meaningful
- How to compare across different studies
"""
print(effect_size_importance)
```

### Common Effect Size Measures

```python
import numpy as np
from scipy import stats

def cohens_d(group1, group2):
    """Calculate Cohen's d for independent samples."""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std

def cohens_d_paired(before, after):
    """Calculate Cohen's d for paired samples."""
    diff = np.array(after) - np.array(before)
    return np.mean(diff) / np.std(diff, ddof=1)

def eta_squared(f_stat, df_between, df_within):
    """Calculate eta-squared from F-statistic."""
    return (f_stat * df_between) / (f_stat * df_between + df_within)

def r_from_t(t_stat, df):
    """Calculate correlation coefficient r from t-statistic."""
    return np.sqrt(t_stat**2 / (t_stat**2 + df))

# Example calculations
group1 = [23, 25, 27, 24, 26, 28, 22, 25, 26, 24]
group2 = [20, 22, 21, 23, 19, 24, 21, 22, 20, 23]

d = cohens_d(group1, group2)
t_stat, p_value = stats.ttest_ind(group1, group2)
r = r_from_t(t_stat, len(group1) + len(group2) - 2)

print("Effect Size Calculations")
print("=" * 40)
print(f"Mean difference: {np.mean(group1) - np.mean(group2):.2f}")
print(f"Cohen's d: {d:.4f}")
print(f"r (correlation): {r:.4f}")
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")

# Interpretation guidelines
print("\nCohen's d interpretation:")
print("  |d| < 0.2: negligible")
print("  |d| = 0.2: small")
print("  |d| = 0.5: medium")
print("  |d| = 0.8: large")
print(f"\nYour effect size ({abs(d):.2f}): ", end="")
if abs(d) < 0.2:
    print("negligible")
elif abs(d) < 0.5:
    print("small")
elif abs(d) < 0.8:
    print("medium")
else:
    print("large")
```

## Multiple Testing Problem

### The Problem

```python
import numpy as np
from scipy import stats

# Simulation: Multiple tests when H0 is true
np.random.seed(42)
n_tests = 20
alpha = 0.05

# Generate data where H0 is true for all tests
significant_results = 0

print("Multiple Testing Simulation")
print("=" * 50)
print(f"Running {n_tests} tests where H0 is TRUE for all")
print(f"Alpha = {alpha}")
print("\nResults:")

for i in range(n_tests):
    # Two groups from same population (H0 is true)
    group1 = np.random.normal(100, 15, 30)
    group2 = np.random.normal(100, 15, 30)
    t_stat, p_value = stats.ttest_ind(group1, group2)

    if p_value < alpha:
        significant_results += 1
        print(f"  Test {i+1}: p = {p_value:.4f} ** SIGNIFICANT (FALSE POSITIVE)")

print(f"\nTotal false positives: {significant_results} out of {n_tests}")
print(f"Expected false positives: {n_tests * alpha:.1f}")
print(f"Family-wise error rate: {1 - (1-alpha)**n_tests:.4f}")
```

### Corrections for Multiple Testing

```python
from scipy import stats
import numpy as np

# Example p-values from 10 tests
p_values = [0.001, 0.008, 0.039, 0.041, 0.042, 0.06, 0.10, 0.23, 0.45, 0.88]
alpha = 0.05

print("Multiple Testing Corrections")
print("=" * 50)

# 1. Bonferroni correction
bonferroni_alpha = alpha / len(p_values)
bonferroni_sig = [p < bonferroni_alpha for p in p_values]

print(f"\n1. BONFERRONI CORRECTION")
print(f"   Adjusted alpha: {bonferroni_alpha:.4f}")
print(f"   Significant p-values: {sum(bonferroni_sig)}")

# 2. Holm-Bonferroni (step-down)
sorted_indices = np.argsort(p_values)
sorted_p = np.array(p_values)[sorted_indices]
n = len(p_values)

holm_sig = []
for i, p in enumerate(sorted_p):
    adjusted_alpha = alpha / (n - i)
    if p < adjusted_alpha:
        holm_sig.append(True)
    else:
        break

print(f"\n2. HOLM-BONFERRONI (Step-Down)")
print(f"   Significant p-values: {len(holm_sig)}")

# 3. Benjamini-Hochberg (FDR control)
from scipy.stats import false_discovery_control

# Using scipy's implementation
bh_adjusted = false_discovery_control(p_values, method='bh')
bh_sig = [adj < alpha for adj in bh_adjusted]

print(f"\n3. BENJAMINI-HOCHBERG (FDR)")
print(f"   Significant p-values: {sum(bh_sig)}")

# Summary table
print("\n" + "=" * 60)
print("Summary of significant results by method:")
print("-" * 60)
print(f"{'P-value':<10} {'Uncorrected':<12} {'Bonferroni':<12} {'BH (FDR)':<12}")
print("-" * 60)
for i, p in enumerate(p_values):
    uncorr = "Sig" if p < alpha else ""
    bonf = "Sig" if bonferroni_sig[i] else ""
    bh = "Sig" if bh_sig[i] else ""
    print(f"{p:<10.3f} {uncorr:<12} {bonf:<12} {bh:<12}")
```

## Best Practices for Reporting P-Values

### Guidelines

```python
reporting_guidelines = """
BEST PRACTICES FOR REPORTING P-VALUES
=====================================

1. REPORT EXACT P-VALUES
   - Good: "p = 0.023"
   - Bad: "p < 0.05"
   - Exception: Very small p-values can be reported as "p < 0.001"

2. ALWAYS INCLUDE EFFECT SIZES
   - Report Cohen's d, r, or other appropriate effect size
   - Include confidence intervals for effect sizes

3. INCLUDE CONFIDENCE INTERVALS
   - CIs provide more information than p-values alone
   - Show the range of plausible parameter values

4. SPECIFY THE TEST USED
   - "Two-sample t-test, t(28) = 2.45, p = 0.021, d = 0.89"

5. STATE HYPOTHESES CLEARLY
   - Pre-register when possible
   - Distinguish exploratory from confirmatory analyses

6. AVOID DICHOTOMOUS THINKING
   - p = 0.049 and p = 0.051 are essentially the same
   - Report evidence on a continuum

7. CONSIDER PRACTICAL SIGNIFICANCE
   - A "significant" result may be trivially small
   - A "non-significant" result may be practically important

8. ADDRESS MULTIPLE TESTING
   - Report how many tests were conducted
   - Apply appropriate corrections
"""
print(reporting_guidelines)
```

### Example of Good Reporting

```python
import numpy as np
from scipy import stats

# Example study
np.random.seed(42)
treatment = np.random.normal(105, 15, 50)
control = np.random.normal(100, 15, 50)

# Calculations
mean_diff = np.mean(treatment) - np.mean(control)
t_stat, p_value = stats.ttest_ind(treatment, control)

# Effect size
pooled_std = np.sqrt((np.var(treatment, ddof=1) + np.var(control, ddof=1)) / 2)
d = mean_diff / pooled_std

# Confidence interval for mean difference
se = np.sqrt(np.var(treatment, ddof=1)/50 + np.var(control, ddof=1)/50)
df = 50 + 50 - 2
t_crit = stats.t.ppf(0.975, df)
ci = (mean_diff - t_crit * se, mean_diff + t_crit * se)

report = f"""
EXAMPLE OF GOOD STATISTICAL REPORTING
=====================================

Participants in the treatment group (M = {np.mean(treatment):.2f}, SD = {np.std(treatment, ddof=1):.2f})
scored higher than those in the control group (M = {np.mean(control):.2f}, SD = {np.std(control, ddof=1):.2f}).

An independent samples t-test revealed that this difference was statistically
significant, t({df}) = {t_stat:.2f}, p = {p_value:.3f}, with a medium effect size,
Cohen's d = {d:.2f}.

The 95% confidence interval for the mean difference was [{ci[0]:.2f}, {ci[1]:.2f}],
suggesting the treatment produces a reliable improvement of approximately
{mean_diff:.1f} points on average.
"""
print(report)
```

## The P-Value Controversy

### Modern Perspectives

```python
p_value_debate = """
THE P-VALUE DEBATE
==================

CONCERNS WITH P-VALUES:
- Widespread misinterpretation
- Encourages dichotomous thinking (significant vs. not)
- Sensitive to sample size
- Does not measure practical importance
- "P-hacking" and publication bias

AMERICAN STATISTICAL ASSOCIATION (2016) STATEMENT:
1. P-values can indicate incompatibility between data and a model
2. P-values do NOT measure probability that H0 is true
3. Scientific conclusions should not be based solely on p < 0.05
4. Proper inference requires full reporting and transparency
5. P-value does not measure effect size or importance
6. A p-value alone provides limited information

ALTERNATIVES AND COMPLEMENTS:
- Effect sizes with confidence intervals
- Bayesian methods (posterior probabilities, Bayes factors)
- Pre-registration of hypotheses
- Focusing on estimation rather than testing
- Replication studies

MOVING FORWARD:
- Don't ban p-values, but use them correctly
- Always report effect sizes
- Use confidence intervals
- Consider practical significance
- Be transparent about analysis decisions
"""
print(p_value_debate)
```

## Summary

| Concept | Description |
|---------|-------------|
| **P-value** | Probability of data as extreme as observed, given H0 is true |
| **Alpha** | Pre-set threshold for rejecting H0 (typically 0.05) |
| **Significant** | P-value < alpha |
| **Effect size** | Magnitude of the effect (e.g., Cohen's d) |
| **Multiple testing** | Running many tests increases false positive rate |

### Key Takeaways

1. P-values measure compatibility with H0, not probability H0 is true
2. Statistical significance does not imply practical significance
3. Always report effect sizes alongside p-values
4. Non-significant results do not prove no effect exists
5. Be cautious with multiple comparisons
6. Consider confidence intervals as more informative than p-values alone
7. Set alpha before analyzing data, not after seeing results
