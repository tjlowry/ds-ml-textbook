# Probability Fundamentals

## Overview

Probability is the mathematical framework for quantifying uncertainty. It forms the foundation of statistical inference, allowing us to make decisions under uncertainty and draw conclusions from data.

## Basic Concepts

### Sample Space and Events

The **sample space** ($S$ or $\Omega$) is the set of all possible outcomes of an experiment. An **event** is a subset of the sample space.

```python
import numpy as np
from itertools import product

# Sample space for rolling a die
die_sample_space = {1, 2, 3, 4, 5, 6}
print(f"Die sample space: {die_sample_space}")

# Event: rolling an even number
even_event = {2, 4, 6}
print(f"Event (even): {even_event}")

# Sample space for flipping two coins
coin_sample_space = list(product(['H', 'T'], repeat=2))
print(f"Two coins sample space: {coin_sample_space}")
# Output: [('H', 'H'), ('H', 'T'), ('T', 'H'), ('T', 'T')]
```

### R Implementation

```r
# Sample space for rolling a die
die_sample_space <- 1:6
print(die_sample_space)

# Event: rolling an even number
even_event <- c(2, 4, 6)
print(even_event)

# Sample space for flipping two coins
coin_sample_space <- expand.grid(c("H", "T"), c("H", "T"))
print(coin_sample_space)
```

## Probability Rules

### Axioms of Probability

For any event $A$ in sample space $S$:

1. **Non-negativity**: $P(A) \geq 0$
2. **Normalization**: $P(S) = 1$
3. **Additivity**: For mutually exclusive events $A$ and $B$: $P(A \cup B) = P(A) + P(B)$

### Complement Rule

$$P(A^c) = 1 - P(A)$$

The probability that event $A$ does not occur is one minus the probability that it does.

```python
# Probability of NOT rolling a 6
p_six = 1/6
p_not_six = 1 - p_six
print(f"P(not 6) = {p_not_six:.4f}")  # Output: 0.8333
```

### Addition Rule

For any two events $A$ and $B$:

$$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$

For **mutually exclusive** events (where $P(A \cap B) = 0$):

$$P(A \cup B) = P(A) + P(B)$$

```python
# Example: Drawing a card from a deck
# P(Heart OR Face card) = P(Heart) + P(Face) - P(Heart AND Face)
p_heart = 13/52
p_face = 12/52  # J, Q, K in each of 4 suits
p_heart_and_face = 3/52  # J, Q, K of hearts

p_heart_or_face = p_heart + p_face - p_heart_and_face
print(f"P(Heart or Face) = {p_heart_or_face:.4f}")  # Output: 0.4231
```

### Multiplication Rule

For any two events:

$$P(A \cap B) = P(A) \cdot P(B|A) = P(B) \cdot P(A|B)$$

For **independent** events:

$$P(A \cap B) = P(A) \cdot P(B)$$

```python
# Independent events: Rolling two dice
p_first_six = 1/6
p_second_six = 1/6
p_both_sixes = p_first_six * p_second_six
print(f"P(both sixes) = {p_both_sixes:.4f}")  # Output: 0.0278

# Dependent events: Drawing cards without replacement
# P(two aces) = P(first ace) * P(second ace | first ace)
p_two_aces = (4/52) * (3/51)
print(f"P(two aces without replacement) = {p_two_aces:.4f}")  # Output: 0.0045
```

## Conditional Probability

The probability of event $A$ given that event $B$ has occurred:

$$P(A|B) = \frac{P(A \cap B)}{P(B)}, \quad \text{where } P(B) > 0$$

### Python Implementation

```python
import numpy as np
import pandas as pd

# Example: Medical test scenario
# Data: 1000 people tested for a disease
data = pd.DataFrame({
    'has_disease': [True] * 100 + [False] * 900,
    'test_positive': [True] * 90 + [False] * 10 +  # 90% sensitivity
                     [True] * 45 + [False] * 855    # 5% false positive rate
})

# Calculate conditional probability
# P(Disease | Positive Test)
positive_tests = data[data['test_positive'] == True]
p_disease_given_positive = (
    positive_tests['has_disease'].sum() / len(positive_tests)
)

print(f"P(Disease | Positive) = {p_disease_given_positive:.4f}")
# This demonstrates why positive tests don't always mean disease!

# Using formula directly
p_positive_and_disease = 90/1000  # True positives
p_positive = (90 + 45)/1000       # All positives
p_disease_given_positive_formula = p_positive_and_disease / p_positive
print(f"Using formula: {p_disease_given_positive_formula:.4f}")
```

### R Implementation

```r
# Conditional probability example
# Create contingency table
test_results <- matrix(c(90, 10, 45, 855), nrow = 2, byrow = TRUE,
                       dimnames = list(c("Diseased", "Healthy"),
                                      c("Positive", "Negative")))
print(test_results)

# P(Disease | Positive)
p_disease_given_positive <- test_results["Diseased", "Positive"] /
                            sum(test_results[, "Positive"])
print(paste("P(Disease | Positive) =", round(p_disease_given_positive, 4)))
```

## Independence

Two events $A$ and $B$ are **independent** if:

$$P(A \cap B) = P(A) \cdot P(B)$$

Equivalently, if:
- $P(A|B) = P(A)$
- $P(B|A) = P(B)$

```python
import numpy as np

def test_independence(p_a, p_b, p_a_and_b, tolerance=0.001):
    """Test if two events are approximately independent."""
    expected_if_independent = p_a * p_b
    difference = abs(p_a_and_b - expected_if_independent)

    is_independent = difference < tolerance

    print(f"P(A) = {p_a}")
    print(f"P(B) = {p_b}")
    print(f"P(A and B) observed = {p_a_and_b}")
    print(f"P(A) * P(B) = {expected_if_independent}")
    print(f"Independent: {is_independent}")

    return is_independent

# Example: Are gender and color preference independent?
# From a survey of 200 people
p_male = 100/200
p_blue = 80/200
p_male_and_blue = 45/200

test_independence(p_male, p_blue, p_male_and_blue)
```

## Probability Distributions

### Discrete Probability Distributions

A discrete random variable $X$ takes on a countable number of values. Its probability distribution is described by a **probability mass function (PMF)**:

$$P(X = x) = p(x)$$

Properties:
1. $0 \leq p(x) \leq 1$ for all $x$
2. $\sum_{\text{all } x} p(x) = 1$

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Binomial distribution: n trials, probability p of success
n, p = 10, 0.3
x = np.arange(0, n+1)
binomial_pmf = stats.binom.pmf(x, n, p)

print("Binomial Distribution (n=10, p=0.3)")
print("=" * 40)
for val, prob in zip(x, binomial_pmf):
    print(f"P(X = {val:2d}) = {prob:.4f}")

# Verify probabilities sum to 1
print(f"\nSum of probabilities: {binomial_pmf.sum():.6f}")

# Calculate expected value and variance
expected_value = n * p
variance = n * p * (1 - p)
print(f"\nE[X] = n*p = {expected_value}")
print(f"Var(X) = n*p*(1-p) = {variance}")
```

### R Implementation

```r
# Binomial distribution
n <- 10
p <- 0.3
x <- 0:n

# Calculate PMF
binomial_pmf <- dbinom(x, size = n, prob = p)

# Display probabilities
cat("Binomial Distribution (n=10, p=0.3)\n")
for (i in seq_along(x)) {
  cat(sprintf("P(X = %2d) = %.4f\n", x[i], binomial_pmf[i]))
}

# Verify sum equals 1
cat(sprintf("\nSum of probabilities: %.6f\n", sum(binomial_pmf)))

# Expected value and variance
cat(sprintf("E[X] = %.1f\n", n * p))
cat(sprintf("Var(X) = %.2f\n", n * p * (1 - p)))
```

### Continuous Probability Distributions

A continuous random variable $X$ can take any value in an interval. Its distribution is described by a **probability density function (PDF)**:

$$f(x) \geq 0 \quad \text{and} \quad \int_{-\infty}^{\infty} f(x) \, dx = 1$$

The probability of $X$ falling in an interval is:

$$P(a \leq X \leq b) = \int_a^b f(x) \, dx$$

```python
import numpy as np
from scipy import stats

# Normal distribution
mu, sigma = 100, 15  # Mean and standard deviation

# Create distribution object
normal_dist = stats.norm(loc=mu, scale=sigma)

# Probability calculations
print("Normal Distribution (mu=100, sigma=15)")
print("=" * 45)

# P(X < 85)
p_less_85 = normal_dist.cdf(85)
print(f"P(X < 85) = {p_less_85:.4f}")

# P(X > 115)
p_greater_115 = 1 - normal_dist.cdf(115)
print(f"P(X > 115) = {p_greater_115:.4f}")

# P(85 < X < 115) - within one standard deviation
p_within_1sd = normal_dist.cdf(115) - normal_dist.cdf(85)
print(f"P(85 < X < 115) = {p_within_1sd:.4f}")

# Find value at a given percentile
percentile_90 = normal_dist.ppf(0.90)
print(f"\n90th percentile: {percentile_90:.2f}")

# Z-scores
x_values = [70, 85, 100, 115, 130]
print("\nZ-scores:")
for x in x_values:
    z = (x - mu) / sigma
    print(f"x = {x}: z = {z:.2f}")
```

### R Implementation

```r
# Normal distribution
mu <- 100
sigma <- 15

# P(X < 85)
p_less_85 <- pnorm(85, mean = mu, sd = sigma)
cat(sprintf("P(X < 85) = %.4f\n", p_less_85))

# P(X > 115)
p_greater_115 <- 1 - pnorm(115, mean = mu, sd = sigma)
cat(sprintf("P(X > 115) = %.4f\n", p_greater_115))

# P(85 < X < 115)
p_within_1sd <- pnorm(115, mu, sigma) - pnorm(85, mu, sigma)
cat(sprintf("P(85 < X < 115) = %.4f\n", p_within_1sd))

# 90th percentile
percentile_90 <- qnorm(0.90, mean = mu, sd = sigma)
cat(sprintf("90th percentile: %.2f\n", percentile_90))
```

## Expected Value and Variance

### Expected Value (Mean)

For a discrete random variable:
$$E[X] = \mu = \sum_x x \cdot P(X = x)$$

For a continuous random variable:
$$E[X] = \mu = \int_{-\infty}^{\infty} x \cdot f(x) \, dx$$

### Variance

$$Var(X) = \sigma^2 = E[(X - \mu)^2] = E[X^2] - (E[X])^2$$

### Standard Deviation

$$\sigma = \sqrt{Var(X)}$$

```python
import numpy as np

# Discrete random variable: Fair die roll
outcomes = np.array([1, 2, 3, 4, 5, 6])
probabilities = np.array([1/6] * 6)

# Expected value
expected_value = np.sum(outcomes * probabilities)
print(f"E[X] (die roll) = {expected_value:.4f}")

# Variance
variance = np.sum((outcomes - expected_value)**2 * probabilities)
print(f"Var(X) = {variance:.4f}")

# Standard deviation
std_dev = np.sqrt(variance)
print(f"SD(X) = {std_dev:.4f}")

# Alternative variance calculation: E[X^2] - (E[X])^2
e_x_squared = np.sum(outcomes**2 * probabilities)
variance_alt = e_x_squared - expected_value**2
print(f"\nUsing E[X^2] - (E[X])^2:")
print(f"E[X^2] = {e_x_squared:.4f}")
print(f"Var(X) = {variance_alt:.4f}")
```

### Properties of Expected Value and Variance

```python
import numpy as np

# Properties of expectation and variance
a, b = 3, 5  # Constants
mu_x, var_x = 10, 4  # Mean and variance of X

# For Y = aX + b:
# E[Y] = aE[X] + b
# Var(Y) = a^2 * Var(X)

mu_y = a * mu_x + b
var_y = a**2 * var_x

print("Linear transformation Y = aX + b")
print(f"a = {a}, b = {b}")
print(f"E[X] = {mu_x}, Var(X) = {var_x}")
print(f"\nE[Y] = a*E[X] + b = {mu_y}")
print(f"Var(Y) = a^2 * Var(X) = {var_y}")
print(f"SD(Y) = |a| * SD(X) = {abs(a) * np.sqrt(var_x):.4f}")
```

## Common Probability Distributions

### Bernoulli Distribution

Single trial with success probability $p$:

$$P(X = k) = p^k (1-p)^{1-k}, \quad k \in \{0, 1\}$$

- $E[X] = p$
- $Var(X) = p(1-p)$

### Binomial Distribution

Number of successes in $n$ independent Bernoulli trials:

$$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}$$

- $E[X] = np$
- $Var(X) = np(1-p)$

```python
from scipy import stats

# Binomial: 20 coin flips, P(heads) = 0.5
n, p = 20, 0.5
binom_dist = stats.binom(n, p)

print("Binomial Distribution (n=20, p=0.5)")
print(f"E[X] = {binom_dist.mean():.2f}")
print(f"Var(X) = {binom_dist.var():.2f}")
print(f"P(X = 10) = {binom_dist.pmf(10):.4f}")
print(f"P(X <= 8) = {binom_dist.cdf(8):.4f}")
print(f"P(X >= 12) = {1 - binom_dist.cdf(11):.4f}")
```

### Poisson Distribution

Number of events in a fixed interval when events occur at a constant average rate $\lambda$:

$$P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}$$

- $E[X] = \lambda$
- $Var(X) = \lambda$

```python
from scipy import stats

# Poisson: Average 5 customers per hour
lambda_param = 5
poisson_dist = stats.poisson(lambda_param)

print(f"Poisson Distribution (lambda={lambda_param})")
print(f"E[X] = {poisson_dist.mean():.2f}")
print(f"Var(X) = {poisson_dist.var():.2f}")
print(f"P(X = 5) = {poisson_dist.pmf(5):.4f}")
print(f"P(X <= 3) = {poisson_dist.cdf(3):.4f}")
print(f"P(X >= 8) = {1 - poisson_dist.cdf(7):.4f}")
```

### Normal Distribution

The most important continuous distribution:

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

- $E[X] = \mu$
- $Var(X) = \sigma^2$

### Standard Normal Distribution

When $Z \sim N(0, 1)$:

$$P(Z \leq z) = \Phi(z)$$

Converting any normal to standard normal:

$$Z = \frac{X - \mu}{\sigma}$$

```python
from scipy import stats

# Standard normal distribution
standard_normal = stats.norm(0, 1)

# Common z-values
z_values = [-2.58, -1.96, -1.645, 0, 1.645, 1.96, 2.58]

print("Standard Normal Distribution Probabilities")
print("=" * 50)
for z in z_values:
    p_less = standard_normal.cdf(z)
    print(f"P(Z < {z:6.3f}) = {p_less:.4f}")

print("\nCommon Confidence Levels:")
print(f"90% CI: z = {standard_normal.ppf(0.95):.3f}")
print(f"95% CI: z = {standard_normal.ppf(0.975):.3f}")
print(f"99% CI: z = {standard_normal.ppf(0.995):.3f}")
```

## Law of Large Numbers

As sample size increases, the sample mean converges to the population mean:

$$\bar{X}_n \xrightarrow{P} \mu \quad \text{as} \quad n \to \infty$$

```python
import numpy as np
import matplotlib.pyplot as plt

# Demonstration: Rolling a fair die
np.random.seed(42)

# True expected value
true_mean = 3.5

# Sample sizes
sample_sizes = [10, 50, 100, 500, 1000, 5000, 10000]

print("Law of Large Numbers Demonstration")
print("=" * 45)
print("Rolling a fair die (true mean = 3.5)")
print()

for n in sample_sizes:
    rolls = np.random.randint(1, 7, size=n)
    sample_mean = rolls.mean()
    error = abs(sample_mean - true_mean)
    print(f"n = {n:5d}: sample mean = {sample_mean:.4f}, error = {error:.4f}")
```

## Central Limit Theorem

Regardless of the population distribution, the sampling distribution of the sample mean approaches a normal distribution as sample size increases:

$$\bar{X} \sim N\left(\mu, \frac{\sigma^2}{n}\right) \quad \text{for large } n$$

Or equivalently:

$$\frac{\bar{X} - \mu}{\sigma/\sqrt{n}} \sim N(0, 1) \quad \text{for large } n$$

```python
import numpy as np
from scipy import stats

# Demonstrate CLT with exponential distribution (highly skewed)
np.random.seed(42)

# Population: Exponential with rate 1
population_mean = 1.0
population_std = 1.0

# Generate many sample means
num_samples = 10000

print("Central Limit Theorem Demonstration")
print("=" * 50)
print("Population: Exponential(1) - highly right-skewed")
print(f"Population mean: {population_mean}")
print(f"Population std: {population_std}")
print()

for sample_size in [5, 30, 100]:
    sample_means = []
    for _ in range(num_samples):
        sample = np.random.exponential(1, sample_size)
        sample_means.append(np.mean(sample))

    sample_means = np.array(sample_means)

    # Theoretical values
    theoretical_mean = population_mean
    theoretical_std = population_std / np.sqrt(sample_size)

    print(f"Sample size n = {sample_size}:")
    print(f"  Mean of sample means: {sample_means.mean():.4f} (theoretical: {theoretical_mean:.4f})")
    print(f"  Std of sample means: {sample_means.std():.4f} (theoretical: {theoretical_std:.4f})")

    # Test normality
    _, p_value = stats.normaltest(sample_means)
    print(f"  Normality test p-value: {p_value:.4f}")
    print()
```

### R Implementation

```r
# Central Limit Theorem demonstration
set.seed(42)

# Exponential distribution (skewed)
num_samples <- 10000
population_mean <- 1
population_std <- 1

sample_sizes <- c(5, 30, 100)

cat("Central Limit Theorem Demonstration\n")
cat("Population: Exponential(1) - highly right-skewed\n\n")

for (n in sample_sizes) {
  sample_means <- replicate(num_samples, mean(rexp(n, rate = 1)))

  theoretical_std <- population_std / sqrt(n)

  cat(sprintf("Sample size n = %d:\n", n))
  cat(sprintf("  Mean of sample means: %.4f (theoretical: %.4f)\n",
              mean(sample_means), population_mean))
  cat(sprintf("  Std of sample means: %.4f (theoretical: %.4f)\n\n",
              sd(sample_means), theoretical_std))
}
```

## Summary

Probability fundamentals provide the mathematical foundation for:

1. **Quantifying uncertainty** through probability axioms and rules
2. **Modeling random phenomena** with probability distributions
3. **Making predictions** using expected values and variances
4. **Statistical inference** via the Law of Large Numbers and Central Limit Theorem

Understanding these concepts is essential for:
- Hypothesis testing
- Confidence interval construction
- Regression analysis
- Machine learning algorithms

The key distributions to remember are:
- **Discrete**: Bernoulli, Binomial, Poisson, Geometric
- **Continuous**: Normal, t, Chi-squared, F, Exponential
