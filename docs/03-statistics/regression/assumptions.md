# Regression Assumptions and Diagnostics

## Overview

Regression analysis relies on several key assumptions. When these assumptions are violated, the results may be unreliable. This chapter covers the assumptions for linear regression, how to diagnose violations, and what to do when assumptions are not met.

## The Linear Regression Model

The simple linear regression model assumes:

$$Y_i = \beta_0 + \beta_1 X_i + \epsilon_i$$

where the error terms $\epsilon_i$ follow specific conditions.

## The Five Key Assumptions (LINE + I)

### 1. Linearity

**Assumption**: The relationship between $X$ and $Y$ is linear.

**Mathematical form**: $E[Y|X] = \beta_0 + \beta_1 X$

**Diagnosis**: Residual vs. Fitted plot, partial regression plots

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
from statsmodels.graphics.gofplots import qqplot

# Generate data with linear relationship
np.random.seed(42)
n = 100
X = np.random.uniform(0, 10, n)
y_linear = 2 + 3*X + np.random.normal(0, 2, n)

# Generate data with non-linear relationship
y_nonlinear = 2 + 3*X + 0.5*X**2 + np.random.normal(0, 2, n)

def fit_and_diagnose(X, y, title):
    """Fit regression and create diagnostic plots."""
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()

    # Residuals
    residuals = model.resid
    fitted = model.fittedvalues

    # Create figure
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Residuals vs Fitted
    axes[0].scatter(fitted, residuals, alpha=0.6)
    axes[0].axhline(y=0, color='red', linestyle='--')
    axes[0].set_xlabel('Fitted Values')
    axes[0].set_ylabel('Residuals')
    axes[0].set_title(f'{title}: Residuals vs Fitted')

    # Add lowess smoothing line
    lowess = sm.nonparametric.lowess(residuals, fitted, frac=0.3)
    axes[0].plot(lowess[:, 0], lowess[:, 1], color='orange', linewidth=2)

    # Scatter plot with regression line
    axes[1].scatter(X, y, alpha=0.6)
    axes[1].plot(X, model.fittedvalues, color='red')
    axes[1].set_xlabel('X')
    axes[1].set_ylabel('Y')
    axes[1].set_title(f'{title}: Data and Fit')

    plt.tight_layout()
    return model

print("Checking Linearity Assumption")
print("=" * 50)
print("\nLinear data: residuals should show no pattern")
model_linear = fit_and_diagnose(X, y_linear, "Linear")
print(f"R-squared: {model_linear.rsquared:.4f}")

print("\nNon-linear data: residuals show curved pattern")
model_nonlinear = fit_and_diagnose(X, y_nonlinear, "Non-linear")
print(f"R-squared: {model_nonlinear.rsquared:.4f}")
```

**What to look for**: In the residuals vs. fitted plot, look for a horizontal band centered at zero with no systematic pattern. A curved pattern indicates non-linearity.

### R Implementation for Linearity

```r
# Generate data
set.seed(42)
n <- 100
X <- runif(n, 0, 10)
y_linear <- 2 + 3*X + rnorm(n, 0, 2)
y_nonlinear <- 2 + 3*X + 0.5*X^2 + rnorm(n, 0, 2)

# Fit models
model_linear <- lm(y_linear ~ X)
model_nonlinear <- lm(y_nonlinear ~ X)

# Diagnostic plots
par(mfrow = c(2, 2))
plot(model_linear, which = 1, main = "Linear: Residuals vs Fitted")
plot(model_nonlinear, which = 1, main = "Non-linear: Residuals vs Fitted")
```

### 2. Independence

**Assumption**: The error terms are independent of each other.

**Mathematical form**: $Cov(\epsilon_i, \epsilon_j) = 0$ for $i \neq j$

**Diagnosis**: Durbin-Watson test, residual time series plot

```python
import numpy as np
from statsmodels.stats.stattools import durbin_watson
import statsmodels.api as sm

# Generate independent errors
np.random.seed(42)
n = 100
X = np.random.uniform(0, 10, n)
y_independent = 2 + 3*X + np.random.normal(0, 2, n)

# Generate autocorrelated errors (time series)
errors_auto = np.zeros(n)
errors_auto[0] = np.random.normal(0, 2)
rho = 0.8  # Autocorrelation coefficient
for i in range(1, n):
    errors_auto[i] = rho * errors_auto[i-1] + np.random.normal(0, 2 * np.sqrt(1 - rho**2))
y_autocorrelated = 2 + 3*X + errors_auto

def check_independence(X, y, label):
    """Check independence assumption using Durbin-Watson test."""
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()
    residuals = model.resid

    # Durbin-Watson test
    dw = durbin_watson(residuals)

    print(f"\n{label}:")
    print(f"  Durbin-Watson statistic: {dw:.4f}")
    if dw < 1.5:
        print("  Interpretation: Positive autocorrelation likely (DW < 1.5)")
    elif dw > 2.5:
        print("  Interpretation: Negative autocorrelation likely (DW > 2.5)")
    else:
        print("  Interpretation: No significant autocorrelation (1.5 < DW < 2.5)")

    return model, dw

print("Checking Independence Assumption")
print("=" * 50)

model_ind, dw_ind = check_independence(X, y_independent, "Independent Errors")
model_auto, dw_auto = check_independence(X, y_autocorrelated, "Autocorrelated Errors")
```

**Durbin-Watson Interpretation**:
- DW near 2: No autocorrelation
- DW near 0: Positive autocorrelation
- DW near 4: Negative autocorrelation

### 3. Normality of Errors

**Assumption**: The error terms are normally distributed.

**Mathematical form**: $\epsilon_i \sim N(0, \sigma^2)$

**Diagnosis**: Q-Q plot, Shapiro-Wilk test, histogram of residuals

```python
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.graphics.gofplots import qqplot
import matplotlib.pyplot as plt

np.random.seed(42)
n = 100
X = np.random.uniform(0, 10, n)

# Normal errors
y_normal = 2 + 3*X + np.random.normal(0, 2, n)

# Non-normal errors (heavy-tailed)
y_heavy_tail = 2 + 3*X + np.random.standard_t(df=3, size=n) * 2

# Right-skewed errors
y_skewed = 2 + 3*X + (np.random.exponential(2, n) - 2)

def check_normality(X, y, label):
    """Check normality of residuals."""
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()
    residuals = model.resid

    # Shapiro-Wilk test
    stat, p_value = stats.shapiro(residuals)

    # Q-Q plot
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Histogram
    axes[0].hist(residuals, bins=20, density=True, alpha=0.7, edgecolor='black')
    x_norm = np.linspace(residuals.min(), residuals.max(), 100)
    axes[0].plot(x_norm, stats.norm.pdf(x_norm, residuals.mean(), residuals.std()),
                 'r-', linewidth=2, label='Normal')
    axes[0].set_xlabel('Residuals')
    axes[0].set_ylabel('Density')
    axes[0].set_title(f'{label}: Histogram')
    axes[0].legend()

    # Q-Q plot
    stats.probplot(residuals, dist="norm", plot=axes[1])
    axes[1].set_title(f'{label}: Q-Q Plot')

    plt.tight_layout()

    print(f"\n{label}:")
    print(f"  Shapiro-Wilk statistic: {stat:.4f}")
    print(f"  p-value: {p_value:.4f}")
    if p_value < 0.05:
        print("  Interpretation: Residuals likely NOT normally distributed")
    else:
        print("  Interpretation: No evidence against normality")

    return model

print("Checking Normality Assumption")
print("=" * 50)

model_norm = check_normality(X, y_normal, "Normal Errors")
model_heavy = check_normality(X, y_heavy_tail, "Heavy-Tailed Errors")
model_skew = check_normality(X, y_skewed, "Skewed Errors")
```

### R Implementation for Normality

```r
# Fit model
model <- lm(y ~ X)

# Q-Q plot
library(car)
qqPlot(model$residuals, main = "Q-Q Plot of Residuals")

# Shapiro-Wilk test
shapiro.test(model$residuals)

# Histogram
hist(model$residuals, breaks = 20, freq = FALSE,
     main = "Histogram of Residuals", xlab = "Residuals")
curve(dnorm(x, mean(model$residuals), sd(model$residuals)),
      add = TRUE, col = "red", lwd = 2)
```

### 4. Equal Variance (Homoscedasticity)

**Assumption**: The variance of errors is constant across all levels of X.

**Mathematical form**: $Var(\epsilon_i) = \sigma^2$ for all $i$

**Diagnosis**: Residuals vs. Fitted plot, Scale-Location plot, Breusch-Pagan test

```python
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
import matplotlib.pyplot as plt

np.random.seed(42)
n = 200
X = np.random.uniform(1, 10, n)

# Homoscedastic errors
y_homo = 2 + 3*X + np.random.normal(0, 2, n)

# Heteroscedastic errors (variance increases with X)
y_hetero = 2 + 3*X + np.random.normal(0, 1, n) * X * 0.5

def check_homoscedasticity(X, y, label):
    """Check equal variance assumption."""
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()
    residuals = model.resid
    fitted = model.fittedvalues

    # Breusch-Pagan test
    bp_stat, bp_pvalue, f_stat, f_pvalue = het_breuschpagan(residuals, X_const)

    # Create plots
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Residuals vs Fitted
    axes[0].scatter(fitted, residuals, alpha=0.6)
    axes[0].axhline(y=0, color='red', linestyle='--')
    axes[0].set_xlabel('Fitted Values')
    axes[0].set_ylabel('Residuals')
    axes[0].set_title(f'{label}: Residuals vs Fitted')

    # Scale-Location plot (sqrt of standardized residuals)
    std_residuals = residuals / np.std(residuals)
    sqrt_abs_std_resid = np.sqrt(np.abs(std_residuals))
    axes[1].scatter(fitted, sqrt_abs_std_resid, alpha=0.6)
    lowess = sm.nonparametric.lowess(sqrt_abs_std_resid, fitted, frac=0.3)
    axes[1].plot(lowess[:, 0], lowess[:, 1], color='red', linewidth=2)
    axes[1].set_xlabel('Fitted Values')
    axes[1].set_ylabel('sqrt(|Standardized Residuals|)')
    axes[1].set_title(f'{label}: Scale-Location')

    plt.tight_layout()

    print(f"\n{label}:")
    print(f"  Breusch-Pagan statistic: {bp_stat:.4f}")
    print(f"  p-value: {bp_pvalue:.4f}")
    if bp_pvalue < 0.05:
        print("  Interpretation: Evidence of heteroscedasticity")
    else:
        print("  Interpretation: No significant evidence of heteroscedasticity")

    return model

print("Checking Homoscedasticity Assumption")
print("=" * 50)

model_homo = check_homoscedasticity(X, y_homo, "Homoscedastic")
model_hetero = check_homoscedasticity(X, y_hetero, "Heteroscedastic")
```

### R Implementation for Homoscedasticity

```r
# Fit model
model <- lm(y ~ X)

# Residuals vs Fitted plot
plot(model, which = 1)

# Scale-Location plot
plot(model, which = 3)

# Breusch-Pagan test
library(lmtest)
bptest(model)
```

### 5. No Perfect Multicollinearity (for Multiple Regression)

**Assumption**: Predictor variables are not perfectly linearly related.

**Diagnosis**: Variance Inflation Factor (VIF), correlation matrix

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

np.random.seed(42)
n = 100

# Create predictors with varying levels of collinearity
X1 = np.random.normal(0, 1, n)
X2 = np.random.normal(0, 1, n)
X3 = X1 + np.random.normal(0, 0.1, n)  # Highly correlated with X1
X4 = 2*X1 + 3*X2 + np.random.normal(0, 0.5, n)  # Multicollinear

y = 1 + 2*X1 + 3*X2 + np.random.normal(0, 1, n)

# Create DataFrame
df = pd.DataFrame({'X1': X1, 'X2': X2, 'X3': X3, 'X4': X4, 'y': y})

def calculate_vif(X):
    """Calculate VIF for each predictor."""
    X_with_const = sm.add_constant(X)
    vif_data = pd.DataFrame()
    vif_data['Variable'] = X.columns
    vif_data['VIF'] = [variance_inflation_factor(X_with_const.values, i+1)
                       for i in range(len(X.columns))]
    return vif_data

print("Checking Multicollinearity")
print("=" * 50)

# Correlation matrix
print("\nCorrelation Matrix:")
print(df[['X1', 'X2', 'X3', 'X4']].corr().round(3))

# Model with X1, X2 (no multicollinearity)
print("\nModel with X1, X2 (independent predictors):")
X_good = df[['X1', 'X2']]
vif_good = calculate_vif(X_good)
print(vif_good)
print("VIF < 5: No multicollinearity concern")

# Model with X1, X3 (high collinearity)
print("\nModel with X1, X3 (correlated predictors):")
X_collinear = df[['X1', 'X3']]
vif_collinear = calculate_vif(X_collinear)
print(vif_collinear)

# Model with all predictors
print("\nModel with all predictors (X1, X2, X3, X4):")
X_all = df[['X1', 'X2', 'X3', 'X4']]
vif_all = calculate_vif(X_all)
print(vif_all)
print("\nVIF Interpretation:")
print("  VIF = 1: No correlation")
print("  1 < VIF < 5: Moderate correlation (usually acceptable)")
print("  VIF > 5: High correlation (may be problematic)")
print("  VIF > 10: Severe multicollinearity")
```

### R Implementation for Multicollinearity

```r
# Fit model
model <- lm(y ~ X1 + X2 + X3 + X4, data = df)

# Calculate VIF
library(car)
vif(model)

# Correlation matrix
cor(df[, c("X1", "X2", "X3", "X4")])
```

## Comprehensive Diagnostic Function

```python
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.diagnostic import het_breuschpagan
import matplotlib.pyplot as plt

def comprehensive_regression_diagnostics(X, y, feature_names=None):
    """
    Perform comprehensive regression diagnostics.

    Parameters:
    -----------
    X : array-like
        Predictor variables
    y : array-like
        Response variable
    feature_names : list, optional
        Names of predictor variables

    Returns:
    --------
    dict : Dictionary containing diagnostic results
    """
    X = np.array(X)
    y = np.array(y)

    if X.ndim == 1:
        X = X.reshape(-1, 1)

    if feature_names is None:
        feature_names = [f'X{i+1}' for i in range(X.shape[1])]

    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()
    residuals = model.resid
    fitted = model.fittedvalues

    results = {}

    # 1. Model Summary
    print("=" * 60)
    print("REGRESSION DIAGNOSTICS REPORT")
    print("=" * 60)
    print(f"\nModel: y ~ {' + '.join(feature_names)}")
    print(f"n = {len(y)}, p = {len(feature_names)}")
    print(f"R-squared: {model.rsquared:.4f}")
    print(f"Adjusted R-squared: {model.rsquared_adj:.4f}")

    # 2. Linearity Check (via visual inspection guidance)
    print("\n" + "-" * 60)
    print("1. LINEARITY")
    print("-" * 60)
    print("Check the Residuals vs Fitted plot for non-linear patterns.")
    print("A good plot shows random scatter around y=0.")

    # 3. Independence (Durbin-Watson)
    print("\n" + "-" * 60)
    print("2. INDEPENDENCE")
    print("-" * 60)
    dw_stat = durbin_watson(residuals)
    results['durbin_watson'] = dw_stat
    print(f"Durbin-Watson statistic: {dw_stat:.4f}")
    if dw_stat < 1.5:
        print("WARNING: Possible positive autocorrelation (DW < 1.5)")
    elif dw_stat > 2.5:
        print("WARNING: Possible negative autocorrelation (DW > 2.5)")
    else:
        print("OK: No significant autocorrelation detected (1.5 < DW < 2.5)")

    # 4. Normality (Shapiro-Wilk)
    print("\n" + "-" * 60)
    print("3. NORMALITY OF RESIDUALS")
    print("-" * 60)
    if len(residuals) <= 5000:
        shapiro_stat, shapiro_p = stats.shapiro(residuals)
        results['shapiro_wilk'] = (shapiro_stat, shapiro_p)
        print(f"Shapiro-Wilk test: W = {shapiro_stat:.4f}, p = {shapiro_p:.4f}")
        if shapiro_p < 0.05:
            print("WARNING: Residuals may not be normally distributed (p < 0.05)")
        else:
            print("OK: No significant deviation from normality (p >= 0.05)")
    else:
        print("Sample too large for Shapiro-Wilk. Check Q-Q plot visually.")

    # Skewness and Kurtosis
    skew = stats.skew(residuals)
    kurt = stats.kurtosis(residuals)
    print(f"Skewness: {skew:.4f} (ideal: 0)")
    print(f"Kurtosis: {kurt:.4f} (ideal: 0 for normal)")

    # 5. Homoscedasticity (Breusch-Pagan)
    print("\n" + "-" * 60)
    print("4. HOMOSCEDASTICITY")
    print("-" * 60)
    bp_stat, bp_p, _, _ = het_breuschpagan(residuals, X_const)
    results['breusch_pagan'] = (bp_stat, bp_p)
    print(f"Breusch-Pagan test: LM = {bp_stat:.4f}, p = {bp_p:.4f}")
    if bp_p < 0.05:
        print("WARNING: Evidence of heteroscedasticity (p < 0.05)")
    else:
        print("OK: No significant heteroscedasticity (p >= 0.05)")

    # 6. Create diagnostic plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Residuals vs Fitted
    axes[0, 0].scatter(fitted, residuals, alpha=0.6)
    axes[0, 0].axhline(y=0, color='red', linestyle='--')
    lowess = sm.nonparametric.lowess(residuals, fitted, frac=0.3)
    axes[0, 0].plot(lowess[:, 0], lowess[:, 1], color='orange', linewidth=2)
    axes[0, 0].set_xlabel('Fitted Values')
    axes[0, 0].set_ylabel('Residuals')
    axes[0, 0].set_title('Residuals vs Fitted')

    # Q-Q Plot
    stats.probplot(residuals, dist="norm", plot=axes[0, 1])
    axes[0, 1].set_title('Normal Q-Q Plot')

    # Scale-Location
    std_resid = residuals / np.std(residuals)
    sqrt_abs_std_resid = np.sqrt(np.abs(std_resid))
    axes[1, 0].scatter(fitted, sqrt_abs_std_resid, alpha=0.6)
    lowess2 = sm.nonparametric.lowess(sqrt_abs_std_resid, fitted, frac=0.3)
    axes[1, 0].plot(lowess2[:, 0], lowess2[:, 1], color='red', linewidth=2)
    axes[1, 0].set_xlabel('Fitted Values')
    axes[1, 0].set_ylabel('sqrt(|Standardized Residuals|)')
    axes[1, 0].set_title('Scale-Location')

    # Histogram of residuals
    axes[1, 1].hist(residuals, bins=30, density=True, alpha=0.7, edgecolor='black')
    x_range = np.linspace(residuals.min(), residuals.max(), 100)
    axes[1, 1].plot(x_range, stats.norm.pdf(x_range, residuals.mean(), residuals.std()),
                    'r-', linewidth=2)
    axes[1, 1].set_xlabel('Residuals')
    axes[1, 1].set_ylabel('Density')
    axes[1, 1].set_title('Histogram of Residuals')

    plt.tight_layout()
    plt.suptitle('Regression Diagnostic Plots', y=1.02, fontsize=14)

    print("\n" + "=" * 60)
    print("See diagnostic plots for visual assessment.")
    print("=" * 60)

    results['model'] = model
    return results

# Example usage
np.random.seed(42)
n = 150
X = np.random.uniform(0, 10, n)
y = 2 + 3*X + np.random.normal(0, 2, n)

results = comprehensive_regression_diagnostics(X, y, ['X'])
```

## Remedial Measures

### When Linearity is Violated

1. **Transform the predictor**: $\log(X)$, $\sqrt{X}$, $X^2$
2. **Transform the response**: $\log(Y)$, $\sqrt{Y}$
3. **Add polynomial terms**: $Y = \beta_0 + \beta_1 X + \beta_2 X^2$
4. **Use non-linear regression**

```python
import numpy as np
import statsmodels.api as sm

# Non-linear relationship
np.random.seed(42)
n = 100
X = np.random.uniform(1, 10, n)
y = 2 + 3*np.log(X) + np.random.normal(0, 0.5, n)

# Original model (poor fit)
X_const = sm.add_constant(X)
model_linear = sm.OLS(y, X_const).fit()
print("Linear model R-squared:", model_linear.rsquared.round(4))

# Transform X
X_log = np.log(X)
X_log_const = sm.add_constant(X_log)
model_transformed = sm.OLS(y, X_log_const).fit()
print("Log-transformed model R-squared:", model_transformed.rsquared.round(4))
```

### When Independence is Violated

1. **Use time series methods** (AR, MA, ARIMA)
2. **Add lagged variables**
3. **Use Generalized Least Squares (GLS)**
4. **Use robust standard errors**

### When Normality is Violated

1. **Transform the response**: Box-Cox transformation
2. **Use robust regression**
3. **Use bootstrap for inference**
4. **With large n, rely on Central Limit Theorem**

```python
from scipy import stats
from scipy.special import boxcox

# Skewed response
np.random.seed(42)
y_skewed = np.random.exponential(2, 100)

# Box-Cox transformation
y_transformed, lambda_optimal = stats.boxcox(y_skewed)

print(f"Original skewness: {stats.skew(y_skewed):.4f}")
print(f"Transformed skewness: {stats.skew(y_transformed):.4f}")
print(f"Optimal lambda: {lambda_optimal:.4f}")
```

### When Homoscedasticity is Violated

1. **Transform the response**: $\log(Y)$, $\sqrt{Y}$
2. **Use Weighted Least Squares (WLS)**
3. **Use heteroscedasticity-robust standard errors (HC0, HC3)**

```python
import numpy as np
import statsmodels.api as sm

# Heteroscedastic data
np.random.seed(42)
n = 100
X = np.random.uniform(1, 10, n)
y = 2 + 3*X + np.random.normal(0, 1, n) * X * 0.3

X_const = sm.add_constant(X)
model = sm.OLS(y, X_const).fit()

# Regular standard errors
print("Regular SE for slope:", model.bse[1].round(4))

# Robust standard errors (HC3)
model_robust = sm.OLS(y, X_const).fit(cov_type='HC3')
print("Robust SE for slope:", model_robust.bse[1].round(4))
```

### When Multicollinearity is Present

1. **Remove highly correlated predictors**
2. **Combine correlated variables** (PCA)
3. **Use regularization** (Ridge, Lasso)
4. **Collect more data**

## Summary Checklist

Before trusting regression results, check:

| Assumption | Diagnostic Tool | What to Look For |
|------------|-----------------|------------------|
| Linearity | Residuals vs Fitted | Random scatter, no pattern |
| Independence | Durbin-Watson, ACF plot | DW near 2, no correlation |
| Normality | Q-Q plot, Shapiro-Wilk | Points on diagonal, p > 0.05 |
| Equal Variance | Scale-Location, Breusch-Pagan | Horizontal band, p > 0.05 |
| No Multicollinearity | VIF | VIF < 5 (or < 10) |

### R Quick Reference

```r
# Fit model
model <- lm(y ~ x1 + x2, data = df)

# All diagnostic plots at once
par(mfrow = c(2, 2))
plot(model)

# Individual tests
library(car)
library(lmtest)

# Normality
shapiro.test(model$residuals)
qqPlot(model$residuals)

# Homoscedasticity
bptest(model)

# Autocorrelation
dwtest(model)

# Multicollinearity
vif(model)
```

When assumptions are severely violated, consider:
- Transformations
- Robust methods
- Non-parametric approaches
- Different model classes (GLM, GAM)
