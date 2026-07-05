# Statistical Distributions

## Overview

A probability distribution describes how the values of a random variable are spread or distributed. Understanding distributions is fundamental to statistical analysis, as they form the basis for inference, hypothesis testing, and modeling.

## Types of Distributions

- **Discrete distributions**: Variables can only take specific values (counts, categories)
- **Continuous distributions**: Variables can take any value within a range

## Normal (Gaussian) Distribution

### Concept

The normal distribution is the most important continuous distribution in statistics. It's characterized by its symmetric, bell-shaped curve centered around the mean.

### Probability Density Function (PDF)

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

Where:
- $\mu$ = mean (center of distribution)
- $\sigma$ = standard deviation (spread)
- $\sigma^2$ = variance

### Properties

- Symmetric around the mean: $\mu = \text{median} = \text{mode}$
- 68-95-99.7 rule (empirical rule)
- Defined by two parameters: $\mu$ and $\sigma$
- Sum of normal variables is normal
- Central Limit Theorem: sample means approach normal distribution

### Python Implementation

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Create a normal distribution
mu, sigma = 100, 15  # IQ score parameters
normal_dist = stats.norm(loc=mu, scale=sigma)

# Generate random samples
samples = normal_dist.rvs(size=1000, random_state=42)

# Calculate probabilities
print(f"P(X < 115) = {normal_dist.cdf(115):.4f}")
print(f"P(X > 130) = {1 - normal_dist.cdf(130):.4f}")
print(f"P(85 < X < 115) = {normal_dist.cdf(115) - normal_dist.cdf(85):.4f}")

# Find percentiles
print(f"\n90th percentile: {normal_dist.ppf(0.90):.2f}")
print(f"95th percentile: {normal_dist.ppf(0.95):.2f}")

# Verify 68-95-99.7 rule
print(f"\nEmpirical Rule Verification:")
print(f"Within 1 std: {normal_dist.cdf(mu + sigma) - normal_dist.cdf(mu - sigma):.4f}")
print(f"Within 2 std: {normal_dist.cdf(mu + 2*sigma) - normal_dist.cdf(mu - 2*sigma):.4f}")
print(f"Within 3 std: {normal_dist.cdf(mu + 3*sigma) - normal_dist.cdf(mu - 3*sigma):.4f}")
```

### Standard Normal Distribution (Z-Distribution)

```python
from scipy import stats

# Standard normal: mu=0, sigma=1
z_dist = stats.norm(0, 1)

# Common z-score lookups
z_values = [1.645, 1.96, 2.576]
confidence_levels = [0.90, 0.95, 0.99]

print("Critical Z-Values for Confidence Intervals:")
for z, conf in zip(z_values, confidence_levels):
    area = z_dist.cdf(z) - z_dist.cdf(-z)
    print(f"  z = {z:.3f} -> {area*100:.0f}% confidence")

# Convert raw score to z-score
raw_score = 120
mu, sigma = 100, 15
z_score = (raw_score - mu) / sigma
percentile = z_dist.cdf(z_score) * 100
print(f"\nScore of {raw_score}: z = {z_score:.2f}, percentile = {percentile:.1f}%")
```

## Binomial Distribution

### Concept

The binomial distribution models the number of successes in a fixed number of independent trials, each with the same probability of success.

### Probability Mass Function (PMF)

$$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}$$

Where:
- $n$ = number of trials
- $k$ = number of successes
- $p$ = probability of success on each trial
- $\binom{n}{k} = \frac{n!}{k!(n-k)!}$ (binomial coefficient)

### Properties

- Mean: $\mu = np$
- Variance: $\sigma^2 = np(1-p)$
- Approaches normal distribution as $n$ increases (when $np \geq 5$ and $n(1-p) \geq 5$)

### Python Implementation

```python
from scipy import stats
import numpy as np

# Coin flipping example: 10 flips, fair coin
n, p = 10, 0.5
binom_dist = stats.binom(n, p)

# Probability of exactly k heads
for k in range(11):
    prob = binom_dist.pmf(k)
    print(f"P(X = {k:2d}) = {prob:.4f} {'*' * int(prob * 50)}")

print(f"\nMean: {binom_dist.mean():.2f}")
print(f"Variance: {binom_dist.var():.2f}")
print(f"Std Dev: {binom_dist.std():.2f}")

# Cumulative probabilities
print(f"\nP(X <= 3) = {binom_dist.cdf(3):.4f}")
print(f"P(X >= 7) = {1 - binom_dist.cdf(6):.4f}")  # Note: cdf(6) = P(X <= 6)
```

### Real Example: Quality Control

```python
from scipy import stats

# Manufacturing: 2% defect rate, batch of 100 items
n = 100
p = 0.02
binom_dist = stats.binom(n, p)

print("Quality Control Analysis:")
print(f"Expected defects: {binom_dist.mean():.1f}")
print(f"Std Dev: {binom_dist.std():.2f}")

print(f"\nP(0 defects) = {binom_dist.pmf(0):.4f}")
print(f"P(at most 2 defects) = {binom_dist.cdf(2):.4f}")
print(f"P(more than 5 defects) = {1 - binom_dist.cdf(5):.4f}")

# Find threshold for 95% of batches
threshold = binom_dist.ppf(0.95)
print(f"\n95% of batches have at most {threshold:.0f} defects")
```

## Poisson Distribution

### Concept

The Poisson distribution models the number of events occurring in a fixed interval of time or space, when events occur independently at a constant average rate.

### Probability Mass Function

$$P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}$$

Where:
- $\lambda$ = average rate (expected number of events)
- $k$ = number of events (non-negative integer)

### Properties

- Mean: $\mu = \lambda$
- Variance: $\sigma^2 = \lambda$
- Used when: counting events in time/space, events are independent, average rate is constant
- Approximates binomial when $n$ is large and $p$ is small

### Python Implementation

```python
from scipy import stats
import numpy as np

# Website receives average of 5 visitors per minute
lambda_rate = 5
poisson_dist = stats.poisson(lambda_rate)

print("Website Traffic Analysis (lambda = 5 visitors/minute):")
print("\nProbability distribution:")
for k in range(15):
    prob = poisson_dist.pmf(k)
    print(f"P(X = {k:2d}) = {prob:.4f} {'*' * int(prob * 50)}")

print(f"\nMean: {poisson_dist.mean():.2f}")
print(f"Variance: {poisson_dist.var():.2f}")

# Probabilities
print(f"\nP(X = 0) - no visitors = {poisson_dist.pmf(0):.4f}")
print(f"P(X >= 10) - busy minute = {1 - poisson_dist.cdf(9):.4f}")
print(f"P(3 <= X <= 7) = {poisson_dist.cdf(7) - poisson_dist.cdf(2):.4f}")
```

### Real Example: Call Center

```python
from scipy import stats

# Call center: average 20 calls per hour
lambda_rate = 20
poisson_dist = stats.poisson(lambda_rate)

print("Call Center Staffing Analysis:")
print(f"Expected calls per hour: {lambda_rate}")

# How many operators needed to handle 95% of hours?
calls_95 = poisson_dist.ppf(0.95)
print(f"\n95% of hours have at most {calls_95:.0f} calls")
print(f"Staff to handle this load: {int(np.ceil(calls_95 / 4))} operators")
print(f"  (assuming each operator handles 4 calls/hour)")

# Probability of overwhelming the system
max_capacity = 30
print(f"\nP(more than {max_capacity} calls) = {1 - poisson_dist.cdf(max_capacity):.4f}")
```

## Exponential Distribution

### Concept

The exponential distribution models the time between events in a Poisson process. It's the continuous analog of the geometric distribution.

### Probability Density Function

$$f(x) = \lambda e^{-\lambda x} \quad \text{for } x \geq 0$$

### Properties

- Mean: $\mu = 1/\lambda$
- Variance: $\sigma^2 = 1/\lambda^2$
- Memoryless property: $P(X > s + t | X > s) = P(X > t)$

### Python Implementation

```python
from scipy import stats

# Time between customer arrivals: average 1 customer every 5 minutes
mean_time = 5  # minutes
lambda_rate = 1 / mean_time  # rate parameter
exp_dist = stats.expon(scale=mean_time)  # scipy uses scale = 1/lambda

print("Customer Arrival Times:")
print(f"Average time between arrivals: {exp_dist.mean():.1f} minutes")
print(f"Standard deviation: {exp_dist.std():.2f} minutes")

print(f"\nP(wait < 2 min) = {exp_dist.cdf(2):.4f}")
print(f"P(wait > 10 min) = {1 - exp_dist.cdf(10):.4f}")
print(f"P(3 < wait < 7 min) = {exp_dist.cdf(7) - exp_dist.cdf(3):.4f}")

# Percentiles
print(f"\nMedian wait time: {exp_dist.ppf(0.5):.2f} minutes")
print(f"90th percentile: {exp_dist.ppf(0.9):.2f} minutes")
```

## Uniform Distribution

### Concept

In a uniform distribution, all values in the range are equally likely.

### Probability Density Function (Continuous)

$$f(x) = \frac{1}{b-a} \quad \text{for } a \leq x \leq b$$

### Properties

- Mean: $\mu = \frac{a + b}{2}$
- Variance: $\sigma^2 = \frac{(b-a)^2}{12}$

### Python Implementation

```python
from scipy import stats
import numpy as np

# Continuous uniform: random number between 0 and 10
a, b = 0, 10
uniform_dist = stats.uniform(loc=a, scale=b-a)

print("Continuous Uniform Distribution [0, 10]:")
print(f"Mean: {uniform_dist.mean():.2f}")
print(f"Variance: {uniform_dist.var():.2f}")
print(f"Std Dev: {uniform_dist.std():.2f}")

print(f"\nP(X < 3) = {uniform_dist.cdf(3):.4f}")
print(f"P(2 < X < 8) = {uniform_dist.cdf(8) - uniform_dist.cdf(2):.4f}")

# Generate samples
samples = uniform_dist.rvs(size=1000, random_state=42)
print(f"\nSample mean: {np.mean(samples):.2f}")
print(f"Sample std: {np.std(samples):.2f}")
```

## t-Distribution (Student's t)

### Concept

The t-distribution is similar to the normal distribution but with heavier tails. It's used when the population standard deviation is unknown and the sample size is small.

### Properties

- Symmetric around zero
- Defined by degrees of freedom ($\nu$ or $df$)
- Approaches normal distribution as $df \to \infty$
- Heavier tails = more probability in extremes

### Python Implementation

```python
from scipy import stats
import numpy as np

# Compare t-distribution with different df to normal
dfs = [1, 5, 10, 30]
normal = stats.norm(0, 1)

print("Critical Values Comparison (two-tailed, alpha=0.05):")
print(f"Normal (z): {normal.ppf(0.975):.4f}")
for df in dfs:
    t_dist = stats.t(df)
    print(f"t (df={df:2d}): {t_dist.ppf(0.975):.4f}")

# The t critical values are larger, especially for small df
# This accounts for additional uncertainty from estimating sigma

# Practical example: confidence interval
sample = [23, 25, 27, 24, 26, 28, 22, 25, 26, 24]
n = len(sample)
mean = np.mean(sample)
se = stats.sem(sample)  # Standard error

# Using t-distribution
t_critical = stats.t.ppf(0.975, df=n-1)
ci_t = (mean - t_critical * se, mean + t_critical * se)

# Using normal (inappropriate for small n)
z_critical = stats.norm.ppf(0.975)
ci_z = (mean - z_critical * se, mean + z_critical * se)

print(f"\n95% CI using t-distribution: ({ci_t[0]:.2f}, {ci_t[1]:.2f})")
print(f"95% CI using normal (wrong): ({ci_z[0]:.2f}, {ci_z[1]:.2f})")
```

## Chi-Square Distribution

### Concept

The chi-square distribution arises when summing squared standard normal variables. It's used in hypothesis tests for variance and categorical data.

### Properties

- Always non-negative
- Defined by degrees of freedom
- Mean: $\mu = df$
- Variance: $\sigma^2 = 2 \cdot df$
- Right-skewed (approaches normal as $df$ increases)

### Python Implementation

```python
from scipy import stats
import numpy as np

# Chi-square distribution with df=10
df = 10
chi2_dist = stats.chi2(df)

print(f"Chi-square distribution (df={df}):")
print(f"Mean: {chi2_dist.mean():.2f}")
print(f"Variance: {chi2_dist.var():.2f}")
print(f"Mode: {df - 2 if df >= 2 else 0}")

# Critical values for hypothesis testing
alpha_levels = [0.10, 0.05, 0.01]
print("\nCritical values (right-tail):")
for alpha in alpha_levels:
    critical = chi2_dist.ppf(1 - alpha)
    print(f"  alpha = {alpha}: {critical:.3f}")

# Goodness of fit test example
observed = [25, 30, 28, 17]  # Observed frequencies
expected = [25, 25, 25, 25]  # Expected under null hypothesis

chi2_stat, p_value = stats.chisquare(observed, expected)
print(f"\nGoodness of fit test:")
print(f"Chi-square statistic: {chi2_stat:.3f}")
print(f"P-value: {p_value:.4f}")
```

## F-Distribution

### Concept

The F-distribution arises as the ratio of two chi-square distributions divided by their degrees of freedom. It's used in ANOVA and comparing variances.

### Properties

- Always non-negative
- Right-skewed
- Defined by two df parameters: $df_1$ (numerator) and $df_2$ (denominator)

### Python Implementation

```python
from scipy import stats
import numpy as np

# F-distribution
df1, df2 = 5, 20
f_dist = stats.f(df1, df2)

print(f"F-distribution (df1={df1}, df2={df2}):")
print(f"Mean: {f_dist.mean():.3f}")

# Critical values
print("\nCritical values:")
print(f"  F(0.95) = {f_dist.ppf(0.95):.3f}")
print(f"  F(0.99) = {f_dist.ppf(0.99):.3f}")

# Example: Comparing variances of two groups
group1 = np.array([23, 25, 27, 24, 26, 28, 22, 25])
group2 = np.array([30, 32, 28, 35, 31, 29, 33, 34])

f_stat = np.var(group1, ddof=1) / np.var(group2, ddof=1)
p_value = 2 * min(stats.f.cdf(f_stat, len(group1)-1, len(group2)-1),
                  1 - stats.f.cdf(f_stat, len(group1)-1, len(group2)-1))

print(f"\nVariance comparison:")
print(f"Var(group1): {np.var(group1, ddof=1):.2f}")
print(f"Var(group2): {np.var(group2, ddof=1):.2f}")
print(f"F-statistic: {f_stat:.3f}")
print(f"P-value: {p_value:.4f}")
```

## Choosing the Right Distribution

```python
# Decision guide for distribution selection

distribution_guide = """
DISCRETE DISTRIBUTIONS:
-----------------------
Binomial: Fixed n trials, constant p, counting successes
  Example: Number of heads in 10 coin flips

Poisson: Counting events in fixed time/space, rare events
  Example: Number of emails per hour

Geometric: Number of trials until first success
  Example: Number of sales calls until first sale

CONTINUOUS DISTRIBUTIONS:
-------------------------
Normal: Symmetric, bell-shaped, many natural phenomena
  Example: Heights, test scores, measurement errors

Exponential: Time between Poisson events
  Example: Time between customer arrivals

Uniform: All values equally likely
  Example: Random number generator

t-distribution: Like normal but heavier tails, small samples
  Example: Confidence intervals with unknown sigma

Chi-square: Sum of squared normal variables
  Example: Goodness of fit tests, variance tests

F-distribution: Ratio of variances
  Example: ANOVA, comparing group variances
"""
print(distribution_guide)
```

## Real-World Application: Distribution Fitting

```python
from scipy import stats
import numpy as np

# Generate some data and try to identify its distribution
np.random.seed(42)
unknown_data = np.random.exponential(scale=5, size=500)

# Test different distributions
distributions = ['norm', 'expon', 'gamma', 'lognorm']

print("Distribution Fitting Results:")
print("=" * 50)

for dist_name in distributions:
    dist = getattr(stats, dist_name)

    # Fit the distribution
    params = dist.fit(unknown_data)

    # Perform Kolmogorov-Smirnov test
    D, p_value = stats.kstest(unknown_data, dist_name, args=params)

    print(f"\n{dist_name.upper()}:")
    print(f"  Parameters: {[f'{p:.3f}' for p in params]}")
    print(f"  K-S statistic: {D:.4f}")
    print(f"  P-value: {p_value:.4f}")
    print(f"  Fit quality: {'Good' if p_value > 0.05 else 'Poor'}")
```

## Summary Table

| Distribution | Type | Parameters | Mean | Variance | Use Case |
|-------------|------|------------|------|----------|----------|
| Normal | Continuous | $\mu$, $\sigma$ | $\mu$ | $\sigma^2$ | Natural phenomena |
| Binomial | Discrete | $n$, $p$ | $np$ | $np(1-p)$ | Count successes in n trials |
| Poisson | Discrete | $\lambda$ | $\lambda$ | $\lambda$ | Events in time/space |
| Exponential | Continuous | $\lambda$ | $1/\lambda$ | $1/\lambda^2$ | Time between events |
| Uniform | Continuous | $a$, $b$ | $(a+b)/2$ | $(b-a)^2/12$ | Equal probability |
| t | Continuous | $df$ | 0 | $df/(df-2)$ | Small sample inference |
| Chi-square | Continuous | $df$ | $df$ | $2 \cdot df$ | Variance tests |
| F | Continuous | $df_1$, $df_2$ | $df_2/(df_2-2)$ | Complex | Compare variances |

Understanding these distributions is essential for selecting appropriate statistical methods and interpreting results correctly.
