# Hypothesis Testing

## Overview

Hypothesis testing is a formal framework for making decisions about population parameters based on sample data. It allows us to evaluate claims, test theories, and make inferences while controlling for the risk of incorrect conclusions.

## The Logic of Hypothesis Testing

### Basic Framework

1. **State the hypotheses**: Formulate null and alternative hypotheses
2. **Choose significance level**: Set the acceptable Type I error rate ($\alpha$)
3. **Collect data**: Gather sample data
4. **Calculate test statistic**: Measure how far sample results are from the null hypothesis
5. **Make a decision**: Reject or fail to reject the null hypothesis

### Analogy: The Criminal Trial

| Legal System | Hypothesis Testing |
|-------------|-------------------|
| Defendant | Null hypothesis |
| "Innocent until proven guilty" | Assume H0 is true |
| Evidence | Sample data |
| "Beyond reasonable doubt" | Significance level |
| Guilty verdict | Reject H0 |
| Not guilty verdict | Fail to reject H0 |

## Null and Alternative Hypotheses

### Null Hypothesis (H0)

The null hypothesis is the default position, typically representing "no effect," "no difference," or "status quo."

- Always contains an equality ($=$, $\leq$, or $\geq$)
- What we assume to be true unless evidence suggests otherwise
- The hypothesis we attempt to reject

### Alternative Hypothesis (H1 or Ha)

The alternative hypothesis represents what we're trying to find evidence for.

- Contains an inequality ($\neq$, $<$, or $>$)
- The research hypothesis
- What we conclude if we reject H0

### Types of Tests

```python
# One-tailed vs Two-tailed tests

"""
TWO-TAILED TEST (non-directional):
H0: mu = mu_0
H1: mu != mu_0
Use when: You want to detect any difference from the hypothesized value

ONE-TAILED TEST (directional):
Right-tailed:
    H0: mu <= mu_0
    H1: mu > mu_0
    Use when: You only care about increases

Left-tailed:
    H0: mu >= mu_0
    H1: mu < mu_0
    Use when: You only care about decreases
"""
```

### Python Example: Setting Up Hypotheses

```python
import numpy as np
from scipy import stats

# Example: Testing if a new drug lowers blood pressure
# Population mean with old treatment: 140 mmHg
# Claim: New drug reduces blood pressure

# H0: mu >= 140 (drug doesn't lower blood pressure)
# H1: mu < 140 (drug lowers blood pressure)
# This is a LEFT-TAILED test

mu_0 = 140  # Hypothesized population mean
alpha = 0.05  # Significance level

# Sample data from patients on new drug
sample = [135, 138, 132, 140, 128, 136, 142, 130, 139, 134]
n = len(sample)
x_bar = np.mean(sample)
s = np.std(sample, ddof=1)

print(f"Hypothesized mean (H0): mu >= {mu_0}")
print(f"Sample mean: {x_bar:.2f}")
print(f"Sample std: {s:.2f}")
print(f"Sample size: {n}")
```

## Test Statistics

### Concept

A test statistic measures how far the sample result is from what we'd expect if H0 were true, in standardized units.

### Common Test Statistics

**Z-statistic** (known population $\sigma$):
$$z = \frac{\bar{x} - \mu_0}{\sigma / \sqrt{n}}$$

**t-statistic** (unknown population $\sigma$):
$$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}$$

### Python Implementation

```python
import numpy as np
from scipy import stats

# Continuing the blood pressure example
mu_0 = 140
sample = [135, 138, 132, 140, 128, 136, 142, 130, 139, 134]

n = len(sample)
x_bar = np.mean(sample)
s = np.std(sample, ddof=1)
se = s / np.sqrt(n)  # Standard error

# Calculate t-statistic (since sigma is unknown)
t_stat = (x_bar - mu_0) / se

print(f"Test statistic calculation:")
print(f"  t = ({x_bar:.2f} - {mu_0}) / {se:.4f}")
print(f"  t = {t_stat:.4f}")

# Degrees of freedom
df = n - 1
print(f"  Degrees of freedom: {df}")
```

## Decision Rules

### Critical Value Approach

Compare the test statistic to a critical value from the appropriate distribution.

```python
from scipy import stats

alpha = 0.05
df = 9

# For left-tailed test
critical_value_left = stats.t.ppf(alpha, df)

# For right-tailed test
critical_value_right = stats.t.ppf(1 - alpha, df)

# For two-tailed test
critical_value_two = stats.t.ppf(1 - alpha/2, df)

print("Critical Values (alpha = 0.05, df = 9):")
print(f"  Left-tailed:  t < {critical_value_left:.4f}")
print(f"  Right-tailed: t > {critical_value_right:.4f}")
print(f"  Two-tailed:   |t| > {critical_value_two:.4f}")

# Decision for our example (left-tailed)
t_stat = -2.33
if t_stat < critical_value_left:
    print(f"\nDecision: Reject H0 (t = {t_stat:.2f} < {critical_value_left:.4f})")
else:
    print(f"\nDecision: Fail to reject H0")
```

### P-Value Approach

Calculate the probability of observing results as extreme as (or more extreme than) the sample results, assuming H0 is true.

```python
from scipy import stats

t_stat = -2.33
df = 9
alpha = 0.05

# Left-tailed p-value
p_value_left = stats.t.cdf(t_stat, df)

# Right-tailed p-value
p_value_right = 1 - stats.t.cdf(t_stat, df)

# Two-tailed p-value
p_value_two = 2 * min(stats.t.cdf(t_stat, df), 1 - stats.t.cdf(t_stat, df))

print(f"P-values for t = {t_stat}:")
print(f"  Left-tailed:  {p_value_left:.4f}")
print(f"  Right-tailed: {p_value_right:.4f}")
print(f"  Two-tailed:   {p_value_two:.4f}")

# Decision
print(f"\nDecision (left-tailed, alpha = {alpha}):")
if p_value_left < alpha:
    print(f"  Reject H0 (p = {p_value_left:.4f} < {alpha})")
else:
    print(f"  Fail to reject H0 (p = {p_value_left:.4f} >= {alpha})")
```

## Types of Errors

### Error Types

| | H0 is True | H0 is False |
|----------|------------|-------------|
| **Reject H0** | Type I Error ($\alpha$) | Correct Decision (Power) |
| **Fail to Reject H0** | Correct Decision | Type II Error ($\beta$) |

### Understanding the Errors

```python
"""
Type I Error (False Positive):
- Rejecting H0 when it's actually true
- Probability = alpha (significance level)
- Example: Concluding a drug works when it doesn't

Type II Error (False Negative):
- Failing to reject H0 when it's actually false
- Probability = beta
- Example: Concluding a drug doesn't work when it actually does

Power = 1 - beta:
- Probability of correctly rejecting a false H0
- The ability to detect an effect when one exists
"""

# Power analysis example
from scipy import stats
import numpy as np

def calculate_power(mu_0, mu_true, sigma, n, alpha, alternative='two-sided'):
    """Calculate the power of a one-sample t-test."""
    se = sigma / np.sqrt(n)

    # Effect size
    effect_size = (mu_true - mu_0) / sigma

    # Non-centrality parameter
    ncp = (mu_true - mu_0) / se

    if alternative == 'two-sided':
        critical_low = stats.t.ppf(alpha/2, n-1)
        critical_high = stats.t.ppf(1 - alpha/2, n-1)
        power = 1 - (stats.nct.cdf(critical_high, n-1, ncp) -
                     stats.nct.cdf(critical_low, n-1, ncp))
    elif alternative == 'less':
        critical = stats.t.ppf(alpha, n-1)
        power = stats.nct.cdf(critical, n-1, ncp)
    else:  # 'greater'
        critical = stats.t.ppf(1 - alpha, n-1)
        power = 1 - stats.nct.cdf(critical, n-1, ncp)

    return power, effect_size

# Example: Drug study
mu_0 = 140      # Null hypothesis mean
mu_true = 135   # True mean (if drug works)
sigma = 10      # Population std dev
n = 10          # Sample size
alpha = 0.05

power, effect = calculate_power(mu_0, mu_true, sigma, n, alpha, 'less')
print(f"Power Analysis:")
print(f"  Effect size: {effect:.2f}")
print(f"  Power: {power:.4f}")
print(f"  Beta (Type II error): {1 - power:.4f}")
```

## Common Hypothesis Tests

### One-Sample t-Test

#### Python Implementation

```python
from scipy import stats
import numpy as np

# Test if sample mean differs from hypothesized value
sample = [23, 25, 27, 24, 26, 28, 22, 25, 26, 24]
mu_0 = 22  # Hypothesized population mean

# Perform one-sample t-test
t_stat, p_value = stats.ttest_1samp(sample, mu_0)

print("One-Sample t-Test")
print("=" * 40)
print(f"H0: mu = {mu_0}")
print(f"H1: mu != {mu_0}")
print(f"\nSample mean: {np.mean(sample):.2f}")
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")

alpha = 0.05
if p_value < alpha:
    print(f"\nConclusion: Reject H0 at alpha = {alpha}")
else:
    print(f"\nConclusion: Fail to reject H0 at alpha = {alpha}")
```

#### R Implementation

```r
# One-sample t-test
sample <- c(23, 25, 27, 24, 26, 28, 22, 25, 26, 24)
mu_0 <- 22  # Hypothesized population mean

# Perform the test
result <- t.test(sample, mu = mu_0, alternative = "two.sided", conf.level = 0.95)

# Display results
cat("One-Sample t-Test\n")
cat("=================================\n")
cat(sprintf("H0: mu = %d\n", mu_0))
cat(sprintf("H1: mu != %d\n\n", mu_0))
cat(sprintf("Sample mean: %.2f\n", mean(sample)))
cat(sprintf("t-statistic: %.4f\n", result$statistic))
cat(sprintf("p-value: %.4f\n", result$p.value))
cat(sprintf("95%% CI: (%.2f, %.2f)\n", result$conf.int[1], result$conf.int[2]))

# Or simply print the result object
print(result)
```

### Two-Sample t-Test

#### Python Implementation

```python
from scipy import stats
import numpy as np

# Compare means of two groups
group1 = [23, 25, 27, 24, 26, 28, 22, 25, 26, 24]
group2 = [20, 22, 21, 23, 19, 24, 21, 22, 20, 23]

# Independent samples t-test (assuming equal variances)
t_stat, p_value = stats.ttest_ind(group1, group2)

print("Two-Sample t-Test (Independent)")
print("=" * 40)
print(f"H0: mu1 = mu2")
print(f"H1: mu1 != mu2")
print(f"\nGroup 1 mean: {np.mean(group1):.2f}")
print(f"Group 2 mean: {np.mean(group2):.2f}")
print(f"Difference: {np.mean(group1) - np.mean(group2):.2f}")
print(f"\nt-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")

# Welch's t-test (not assuming equal variances)
t_stat_welch, p_value_welch = stats.ttest_ind(group1, group2, equal_var=False)
print(f"\nWelch's t-test:")
print(f"t-statistic: {t_stat_welch:.4f}")
print(f"p-value: {p_value_welch:.4f}")
```

#### R Implementation

```r
# Two-sample t-test (independent samples)
group1 <- c(23, 25, 27, 24, 26, 28, 22, 25, 26, 24)
group2 <- c(20, 22, 21, 23, 19, 24, 21, 22, 20, 23)

# Option 1: Using formula notation with a data frame
df <- data.frame(
  value = c(group1, group2),
  group = factor(c(rep("Group1", length(group1)), rep("Group2", length(group2))))
)
result <- t.test(value ~ group, data = df, var.equal = FALSE)  # Welch's test (default)

# Option 2: Direct method
result <- t.test(group1, group2, var.equal = FALSE, alternative = "two.sided")

print(result)

# For equal variance assumption (Student's t-test)
result_equal_var <- t.test(group1, group2, var.equal = TRUE)
print(result_equal_var)
```

### Paired t-Test

#### Python Implementation

```python
from scipy import stats
import numpy as np

# Before and after measurements on same subjects
before = [180, 175, 190, 185, 170, 195, 188, 172, 183, 178]
after = [175, 170, 182, 180, 168, 188, 182, 170, 178, 175]

# Paired t-test
t_stat, p_value = stats.ttest_rel(before, after)

differences = np.array(before) - np.array(after)

print("Paired t-Test")
print("=" * 40)
print(f"H0: mu_difference = 0")
print(f"H1: mu_difference != 0")
print(f"\nMean before: {np.mean(before):.2f}")
print(f"Mean after: {np.mean(after):.2f}")
print(f"Mean difference: {np.mean(differences):.2f}")
print(f"\nt-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")
```

#### R Implementation

```r
# Paired t-test
before <- c(180, 175, 190, 185, 170, 195, 188, 172, 183, 178)
after <- c(175, 170, 182, 180, 168, 188, 182, 170, 178, 175)

# Method 1: Using paired = TRUE
result <- t.test(before, after, paired = TRUE, alternative = "two.sided")
print(result)

# Method 2: Compute differences manually and do one-sample t-test
differences <- before - after
result_diff <- t.test(differences, mu = 0)
print(result_diff)

# Display summary statistics
cat(sprintf("Mean before: %.2f\n", mean(before)))
cat(sprintf("Mean after: %.2f\n", mean(after)))
cat(sprintf("Mean difference: %.2f\n", mean(differences)))
```

### Chi-Square Test of Independence

#### Python Implementation

```python
from scipy import stats
import numpy as np

# Contingency table: Treatment vs Outcome
# Rows: Treatment A, Treatment B
# Columns: Improved, No Change, Worsened
observed = np.array([
    [45, 30, 25],   # Treatment A
    [30, 40, 30]    # Treatment B
])

chi2, p_value, dof, expected = stats.chi2_contingency(observed)

print("Chi-Square Test of Independence")
print("=" * 40)
print(f"H0: Treatment and Outcome are independent")
print(f"H1: Treatment and Outcome are associated")
print(f"\nObserved frequencies:")
print(observed)
print(f"\nExpected frequencies (under H0):")
print(np.round(expected, 2))
print(f"\nChi-square statistic: {chi2:.4f}")
print(f"Degrees of freedom: {dof}")
print(f"p-value: {p_value:.4f}")
```

#### R Implementation

```r
# Chi-Square Test of Independence
# Create contingency table
observed <- matrix(c(45, 30, 25,
                     30, 40, 30),
                   nrow = 2, byrow = TRUE,
                   dimnames = list(
                     Treatment = c("Treatment A", "Treatment B"),
                     Outcome = c("Improved", "No Change", "Worsened")
                   ))

print("Observed Frequencies:")
print(observed)

# Perform chi-squared test
result <- chisq.test(observed)
print(result)

# View expected counts
cat("\nExpected Frequencies (under H0):\n")
print(round(result$expected, 2))

# View Pearson residuals (useful for interpretation)
cat("\nPearson Residuals:\n")
print(round(result$residuals, 2))
```

### ANOVA (One-Way)

#### Python Implementation

```python
from scipy import stats
import numpy as np

# Compare means across multiple groups
group_a = [85, 90, 88, 92, 87]
group_b = [78, 82, 80, 85, 79]
group_c = [92, 95, 91, 94, 93]

# One-way ANOVA
f_stat, p_value = stats.f_oneway(group_a, group_b, group_c)

print("One-Way ANOVA")
print("=" * 40)
print(f"H0: mu_A = mu_B = mu_C")
print(f"H1: At least one mean is different")
print(f"\nGroup A mean: {np.mean(group_a):.2f}")
print(f"Group B mean: {np.mean(group_b):.2f}")
print(f"Group C mean: {np.mean(group_c):.2f}")
print(f"\nF-statistic: {f_stat:.4f}")
print(f"p-value: {p_value:.4f}")
```

#### R Implementation

```r
# One-Way ANOVA
# Create data frame
scores <- c(85, 90, 88, 92, 87,   # Group A
            78, 82, 80, 85, 79,   # Group B
            92, 95, 91, 94, 93)   # Group C
groups <- factor(rep(c("A", "B", "C"), each = 5))
df <- data.frame(score = scores, group = groups)

# Perform ANOVA
myaov <- aov(score ~ group, data = df)
summary(myaov)

# View group means
cat("\nGroup Means:\n")
print(tapply(df$score, df$group, mean))

# Check assumptions with diagnostic plots
par(mfrow = c(1, 2))
plot(myaov, which = 1:2)

# If ANOVA is significant, perform post-hoc tests
# Tukey's HSD for pairwise comparisons
TukeyHSD(myaov)
```

## Complete Hypothesis Testing Workflow

```python
from scipy import stats
import numpy as np

def hypothesis_test_workflow(sample, mu_0, alpha=0.05, alternative='two-sided'):
    """
    Complete workflow for one-sample hypothesis test.

    Parameters:
    -----------
    sample : array-like
        Sample data
    mu_0 : float
        Hypothesized population mean
    alpha : float
        Significance level
    alternative : str
        'two-sided', 'less', or 'greater'
    """
    n = len(sample)
    x_bar = np.mean(sample)
    s = np.std(sample, ddof=1)
    se = s / np.sqrt(n)
    df = n - 1

    # Step 1: State hypotheses
    print("STEP 1: State Hypotheses")
    print("-" * 40)
    if alternative == 'two-sided':
        print(f"H0: mu = {mu_0}")
        print(f"H1: mu != {mu_0}")
    elif alternative == 'less':
        print(f"H0: mu >= {mu_0}")
        print(f"H1: mu < {mu_0}")
    else:
        print(f"H0: mu <= {mu_0}")
        print(f"H1: mu > {mu_0}")

    # Step 2: Set significance level
    print(f"\nSTEP 2: Significance Level")
    print("-" * 40)
    print(f"alpha = {alpha}")

    # Step 3: Compute test statistic
    print(f"\nSTEP 3: Compute Test Statistic")
    print("-" * 40)
    t_stat = (x_bar - mu_0) / se
    print(f"Sample mean (x_bar): {x_bar:.4f}")
    print(f"Standard error: {se:.4f}")
    print(f"t-statistic: {t_stat:.4f}")
    print(f"Degrees of freedom: {df}")

    # Step 4: Compute p-value
    print(f"\nSTEP 4: Compute P-Value")
    print("-" * 40)
    if alternative == 'two-sided':
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))
    elif alternative == 'less':
        p_value = stats.t.cdf(t_stat, df)
    else:
        p_value = 1 - stats.t.cdf(t_stat, df)
    print(f"p-value: {p_value:.4f}")

    # Step 5: Make decision
    print(f"\nSTEP 5: Decision")
    print("-" * 40)
    if p_value < alpha:
        print(f"p-value ({p_value:.4f}) < alpha ({alpha})")
        print("Decision: REJECT H0")
        print(f"Conclusion: There is sufficient evidence to conclude that")
        if alternative == 'two-sided':
            print(f"the population mean differs from {mu_0}.")
        elif alternative == 'less':
            print(f"the population mean is less than {mu_0}.")
        else:
            print(f"the population mean is greater than {mu_0}.")
    else:
        print(f"p-value ({p_value:.4f}) >= alpha ({alpha})")
        print("Decision: FAIL TO REJECT H0")
        print(f"Conclusion: There is insufficient evidence to conclude that")
        if alternative == 'two-sided':
            print(f"the population mean differs from {mu_0}.")
        elif alternative == 'less':
            print(f"the population mean is less than {mu_0}.")
        else:
            print(f"the population mean is greater than {mu_0}.")

    return t_stat, p_value

# Example usage
np.random.seed(42)
sample = np.random.normal(25, 5, 30)
t, p = hypothesis_test_workflow(sample, mu_0=22, alpha=0.05, alternative='greater')
```

## Real-World Application

### A/B Testing Example

```python
from scipy import stats
import numpy as np

def ab_test(control, treatment, alpha=0.05):
    """
    Perform A/B test comparing conversion rates.
    """
    n1 = len(control)
    n2 = len(treatment)

    p1 = np.mean(control)  # Control conversion rate
    p2 = np.mean(treatment)  # Treatment conversion rate

    # Pooled proportion
    p_pool = (sum(control) + sum(treatment)) / (n1 + n2)

    # Standard error
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))

    # Z-statistic
    z_stat = (p2 - p1) / se

    # P-value (two-tailed)
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    print("A/B Test Results")
    print("=" * 50)
    print(f"Control:   n = {n1}, conversion rate = {p1:.4f}")
    print(f"Treatment: n = {n2}, conversion rate = {p2:.4f}")
    print(f"Difference: {(p2 - p1)*100:.2f} percentage points")
    print(f"Relative lift: {((p2 - p1) / p1)*100:.2f}%")
    print(f"\nZ-statistic: {z_stat:.4f}")
    print(f"P-value: {p_value:.4f}")

    if p_value < alpha:
        print(f"\nResult: Statistically significant (p < {alpha})")
        if p2 > p1:
            print("Recommendation: Implement the treatment")
        else:
            print("Recommendation: Keep the control")
    else:
        print(f"\nResult: Not statistically significant (p >= {alpha})")
        print("Recommendation: Continue testing or keep the control")

    return z_stat, p_value

# Simulate A/B test data
np.random.seed(42)
control = np.random.binomial(1, 0.10, 1000)      # 10% conversion rate
treatment = np.random.binomial(1, 0.12, 1000)    # 12% conversion rate

ab_test(control, treatment)
```

## Summary

| Aspect | Description |
|--------|-------------|
| **H0** | Null hypothesis - default position, contains equality |
| **H1** | Alternative hypothesis - what we want to show |
| **Alpha** | Significance level - probability of Type I error |
| **Test Statistic** | Standardized measure of how far sample is from H0 |
| **P-value** | Probability of results as extreme as observed, given H0 is true |
| **Type I Error** | Rejecting H0 when it's true (false positive) |
| **Type II Error** | Failing to reject H0 when it's false (false negative) |
| **Power** | Probability of correctly rejecting a false H0 |

### Key Points

1. We never "accept" H0, only fail to reject it
2. Statistical significance does not imply practical significance
3. P-values do not measure the probability that H0 is true
4. Always report effect sizes alongside p-values
5. Consider the context and consequences of both error types

## How I Did It — MATH 425 (BYU-Idaho)

The examples above use synthetic data to show mechanics. Here are the same tests run on real
data in R during MATH 425 (Winter 2024), each with an actual conclusion.

### One-sample t-test — does a drug add sleep?

Using R's built-in `sleep` data (extra hours of sleep for 10 patients on a soporific drug), I
tested whether the mean extra sleep is greater than zero. A Q-Q plot first confirmed the data
were plausibly normal, which is what the one-sample t-test needs:

```r
sleep1 <- sleep[sleep$group == 1, c("ID", "extra")]
qqPlot(sleep1$extra)                                   # normality check first
t.test(sleep1$extra, mu = 0, alternative = "greater")  # H0: mu = 0, Ha: mu > 0
```

The sample averaged **0.75** extra hours, but with **p = 0.1088** I failed to reject $H_0$ —
no evidence the drug reliably increases sleep.

Source: `~/Projects/school/byui-undergrad/statistics-notebook/Analyses/t Tests/Examples/SleepOneSamplet.Rmd`

### Two-sample t-test — reaction time by sex

From the High School Seniors survey I compared reaction times of male vs. female students.
The raw data had extreme typos, so I first filtered to reaction times under 3 seconds
(leaving roughly 150 female and 160 male responses — large enough to lean on the CLT):

```r
HSS2 <- filter(HSS, Reaction_time < 3) %>% na.omit()
t.test(Reaction_time ~ Gender, data = HSS2,
       mu = 0, alternative = "two.sided", conf.int = 0.95) %>% pander()
```

Males looked slightly faster on the boxplot, but **p = 0.1246** — not significant, so I could
not conclude the mean reaction times differ.

Source: `~/Projects/school/byui-undergrad/statistics-notebook/Analyses/t Tests/HighSchoolSeniors.Rmd`

### Chi-squared test of independence — divorce vs. political views

Using the 2021 General Social Survey, I asked whether having been divorced is associated with
political orientation (a 7-point liberal-to-conservative scale):

```r
gss <- filter(gss2021, !is.na(DIVORCE) & !is.na(POLVIEWS))
mytable <- table(gss$POLVIEWS, gss$DIVORCE)

chi <- chisq.test(mytable)
chi                 # test result
chi$expected        # all > 5, so the test is valid
chi$residuals       # largest was only ~1.39
```

Every expected count exceeded 5 (so the chi-squared approximation is valid), and the test gave
**p = 0.4021** — political views and divorce are independent in these data.

Source: `~/Projects/school/byui-undergrad/statistics-notebook/Analyses/Chi Squared Tests/MyChiSquaredTest.Rmd`

### Two-way ANOVA — my own reaction-time experiment

For a two-factor design I collected my own data: **36 attempts** at a reaction-time minigame
in NBA 2K21, crossing two factors — the `hand` used (left/right) and `posture` (sitting/
standing) — with the interaction term:

```r
time.aov <- aov(reaction_time ~ hand + posture + hand:posture, data = ReactionTime)
summary(time.aov) %>% pander()
```

| Effect | p-value | Verdict |
|---|---|---|
| `hand` | 0.7931 | not significant (Left 399.8 ms vs Right 401.5 ms) |
| `posture` | 0.2394 | not significant (Sitting 404.4 ms vs Standing 396.9 ms) |
| `hand:posture` | 0.05495 | borderline — just misses $\alpha = 0.05$ |

None of the effects cleared the 0.05 bar, though the interaction was close enough that I noted
more data (or more factors) would be needed to settle it.

Source: `~/Projects/school/byui-undergrad/statistics-notebook/Analyses/ANOVA/MyTwoWayANOVA.Rmd`

### Gotchas

- **Filter typos before testing, and say so.** The reaction-time data only made sense after
  dropping impossible values; that filtering step is part of the analysis, not a footnote.
- **Check the expected counts for chi-squared.** The test is only trustworthy when expected
  cell counts are (roughly) all $\geq 5$ — I report `chi$expected` every time.
- **A borderline p-value (0.055) is a "fail to reject," not a "trend."** The interaction above
  missed the cutoff; the honest write-up is "not significant, collect more data."
- **Normality is a prerequisite, not an afterthought.** For the one-sample t-test I checked the
  Q-Q plot *before* trusting the p-value; when that check fails, the
  [nonparametric tests](nonparametric.md) are the right move instead.
