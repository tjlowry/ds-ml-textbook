# Simple Linear Regression

## Overview

Simple linear regression models the relationship between two continuous variables by fitting a straight line to the data. It allows us to predict one variable (the response) based on another variable (the predictor) and quantify the strength and direction of their relationship.

## The Model

### Mathematical Formulation

The simple linear regression model is:

$$Y = \beta_0 + \beta_1 X + \epsilon$$

Where:
- $Y$ = response (dependent) variable
- $X$ = predictor (independent) variable
- $\beta_0$ = intercept (value of Y when X = 0)
- $\beta_1$ = slope (change in Y for one unit change in X)
- $\epsilon$ = error term (random variation)

### Fitted Model

The estimated regression equation is:

$$\hat{Y} = \hat{\beta}_0 + \hat{\beta}_1 X$$

Where $\hat{Y}$ is the predicted value and $\hat{\beta}_0$, $\hat{\beta}_1$ are the estimated coefficients.

## Estimating Coefficients

### Ordinary Least Squares (OLS)

OLS minimizes the sum of squared residuals:

$$\text{SSE} = \sum_{i=1}^{n} (Y_i - \hat{Y}_i)^2 = \sum_{i=1}^{n} (Y_i - \hat{\beta}_0 - \hat{\beta}_1 X_i)^2$$

### Formulas

$$\hat{\beta}_1 = \frac{\sum_{i=1}^{n} (X_i - \bar{X})(Y_i - \bar{Y})}{\sum_{i=1}^{n} (X_i - \bar{X})^2} = \frac{S_{XY}}{S_{XX}}$$

$$\hat{\beta}_0 = \bar{Y} - \hat{\beta}_1 \bar{X}$$

### Python Implementation (From Scratch)

```python
import numpy as np

# Sample data
X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
Y = np.array([2.1, 4.2, 5.8, 8.1, 9.5, 12.3, 14.0, 15.8, 18.2, 19.9])

# Calculate means
X_mean = np.mean(X)
Y_mean = np.mean(Y)

# Calculate coefficients
numerator = np.sum((X - X_mean) * (Y - Y_mean))
denominator = np.sum((X - X_mean) ** 2)

beta_1 = numerator / denominator
beta_0 = Y_mean - beta_1 * X_mean

print("Simple Linear Regression (Manual Calculation)")
print("=" * 50)
print(f"Slope (beta_1): {beta_1:.4f}")
print(f"Intercept (beta_0): {beta_0:.4f}")
print(f"\nRegression equation: Y = {beta_0:.4f} + {beta_1:.4f} * X")

# Predictions
Y_pred = beta_0 + beta_1 * X
print(f"\nPredictions for X = 1 to 10:")
for x, y_actual, y_pred in zip(X, Y, Y_pred):
    print(f"  X = {x}: Actual = {y_actual:.1f}, Predicted = {y_pred:.2f}")
```

### Using scipy and statsmodels

```python
import numpy as np
from scipy import stats
import statsmodels.api as sm

X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
Y = np.array([2.1, 4.2, 5.8, 8.1, 9.5, 12.3, 14.0, 15.8, 18.2, 19.9])

# Method 1: scipy.stats.linregress
slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)

print("Using scipy.stats.linregress")
print("-" * 40)
print(f"Slope: {slope:.4f}")
print(f"Intercept: {intercept:.4f}")
print(f"R-squared: {r_value**2:.4f}")
print(f"P-value: {p_value:.6f}")
print(f"Std Error of slope: {std_err:.4f}")

# Method 2: statsmodels (more comprehensive)
X_with_const = sm.add_constant(X)  # Add intercept term
model = sm.OLS(Y, X_with_const)
results = model.fit()

print("\n\nUsing statsmodels")
print("-" * 40)
print(results.summary())
```

### Using scikit-learn

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)
Y = np.array([2.1, 4.2, 5.8, 8.1, 9.5, 12.3, 14.0, 15.8, 18.2, 19.9])

# Fit the model
model = LinearRegression()
model.fit(X, Y)

# Get coefficients
print("Using scikit-learn")
print("-" * 40)
print(f"Slope: {model.coef_[0]:.4f}")
print(f"Intercept: {model.intercept_:.4f}")

# Predictions and metrics
Y_pred = model.predict(X)
print(f"\nR-squared: {r2_score(Y, Y_pred):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(Y, Y_pred)):.4f}")
```

## Interpreting Coefficients

### Slope Interpretation

```python
# Example: Relationship between study hours and exam score
hours = np.array([1, 2, 3, 4, 5, 6, 7, 8])
scores = np.array([52, 58, 65, 71, 78, 82, 89, 95])

slope, intercept, r, p, se = stats.linregress(hours, scores)

print("Coefficient Interpretation Example")
print("=" * 50)
print(f"Model: Score = {intercept:.2f} + {slope:.2f} * Hours")
print(f"\nInterpretation:")
print(f"  Slope ({slope:.2f}): For each additional hour of study,")
print(f"         the exam score increases by {slope:.2f} points on average.")
print(f"\n  Intercept ({intercept:.2f}): A student who studies 0 hours")
print(f"         is predicted to score {intercept:.2f} points.")
print(f"         (Note: May not be meaningful if X=0 is outside data range)")
```

### Coefficient of Determination (R-squared)

$$R^2 = 1 - \frac{SS_{residual}}{SS_{total}} = 1 - \frac{\sum(Y_i - \hat{Y}_i)^2}{\sum(Y_i - \bar{Y})^2}$$

```python
import numpy as np
from scipy import stats

X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
Y = np.array([2.1, 4.2, 5.8, 8.1, 9.5, 12.3, 14.0, 15.8, 18.2, 19.9])

slope, intercept, r, p, se = stats.linregress(X, Y)
Y_pred = intercept + slope * X

# Calculate R-squared manually
SS_total = np.sum((Y - np.mean(Y))**2)
SS_residual = np.sum((Y - Y_pred)**2)
SS_regression = np.sum((Y_pred - np.mean(Y))**2)

R_squared = 1 - SS_residual / SS_total

print("Decomposition of Variance")
print("=" * 50)
print(f"SS Total (variability in Y): {SS_total:.4f}")
print(f"SS Regression (explained by X): {SS_regression:.4f}")
print(f"SS Residual (unexplained): {SS_residual:.4f}")
print(f"\nR-squared: {R_squared:.4f}")
print(f"Correlation (r): {r:.4f}")
print(f"r-squared = r^2: {r**2:.4f}")

print(f"\nInterpretation: {R_squared*100:.1f}% of the variance in Y")
print(f"is explained by the linear relationship with X.")
```

## Residual Analysis

### Calculating Residuals

$$e_i = Y_i - \hat{Y}_i$$

```python
import numpy as np
from scipy import stats

X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
Y = np.array([2.1, 4.2, 5.8, 8.1, 9.5, 12.3, 14.0, 15.8, 18.2, 19.9])

slope, intercept, r, p, se = stats.linregress(X, Y)
Y_pred = intercept + slope * X
residuals = Y - Y_pred

print("Residual Analysis")
print("=" * 50)
print(f"{'X':<5} {'Y':<8} {'Y_pred':<8} {'Residual':<10}")
print("-" * 35)
for x, y, yp, res in zip(X, Y, Y_pred, residuals):
    print(f"{x:<5} {y:<8.2f} {yp:<8.2f} {res:<10.4f}")

print(f"\nSum of residuals: {np.sum(residuals):.6f} (should be ~0)")
print(f"Mean of residuals: {np.mean(residuals):.6f}")
print(f"Std of residuals: {np.std(residuals, ddof=2):.4f}")
```

### Standardized Residuals

```python
import numpy as np
import statsmodels.api as sm

X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
Y = np.array([2.1, 4.2, 5.8, 8.1, 9.5, 12.3, 14.0, 15.8, 18.2, 19.9])

# Fit model with statsmodels for diagnostic tools
X_const = sm.add_constant(X)
model = sm.OLS(Y, X_const).fit()

# Get influence measures
influence = model.get_influence()
standardized_resid = influence.resid_studentized_internal

print("Standardized Residuals")
print("=" * 50)
print("Values > |2| may indicate outliers")
print(f"\n{'X':<5} {'Std Residual':<15} {'Flag':<10}")
print("-" * 30)
for x, sr in zip(X, standardized_resid):
    flag = "OUTLIER?" if abs(sr) > 2 else ""
    print(f"{x:<5} {sr:<15.4f} {flag:<10}")
```

## Hypothesis Testing for Coefficients

### Testing the Slope

$H_0: \beta_1 = 0$ (no linear relationship)
$H_1: \beta_1 \neq 0$ (linear relationship exists)

$$t = \frac{\hat{\beta}_1 - 0}{SE(\hat{\beta}_1)}$$

```python
import numpy as np
from scipy import stats
import statsmodels.api as sm

X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
Y = np.array([2.1, 4.2, 5.8, 8.1, 9.5, 12.3, 14.0, 15.8, 18.2, 19.9])

# Using statsmodels for full inference
X_const = sm.add_constant(X)
model = sm.OLS(Y, X_const).fit()

print("Hypothesis Tests for Coefficients")
print("=" * 50)
print(f"\nIntercept (beta_0):")
print(f"  Estimate: {model.params[0]:.4f}")
print(f"  Std Error: {model.bse[0]:.4f}")
print(f"  t-statistic: {model.tvalues[0]:.4f}")
print(f"  p-value: {model.pvalues[0]:.6f}")

print(f"\nSlope (beta_1):")
print(f"  Estimate: {model.params[1]:.4f}")
print(f"  Std Error: {model.bse[1]:.4f}")
print(f"  t-statistic: {model.tvalues[1]:.4f}")
print(f"  p-value: {model.pvalues[1]:.10f}")

alpha = 0.05
if model.pvalues[1] < alpha:
    print(f"\nConclusion: Reject H0 at alpha = {alpha}")
    print("There is a significant linear relationship between X and Y.")
else:
    print(f"\nConclusion: Fail to reject H0 at alpha = {alpha}")
    print("No significant linear relationship detected.")
```

### Confidence Intervals for Coefficients

```python
import numpy as np
import statsmodels.api as sm

X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
Y = np.array([2.1, 4.2, 5.8, 8.1, 9.5, 12.3, 14.0, 15.8, 18.2, 19.9])

X_const = sm.add_constant(X)
model = sm.OLS(Y, X_const).fit()

# Get confidence intervals
conf_int = model.conf_int(alpha=0.05)

print("95% Confidence Intervals for Coefficients")
print("=" * 50)
print(f"\nIntercept: [{conf_int[0, 0]:.4f}, {conf_int[0, 1]:.4f}]")
print(f"Slope:     [{conf_int[1, 0]:.4f}, {conf_int[1, 1]:.4f}]")
print(f"\nInterpretation: We are 95% confident that the true slope")
print(f"lies between {conf_int[1, 0]:.4f} and {conf_int[1, 1]:.4f}.")
```

## Prediction

### Point Prediction

```python
import numpy as np
import statsmodels.api as sm

X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
Y = np.array([2.1, 4.2, 5.8, 8.1, 9.5, 12.3, 14.0, 15.8, 18.2, 19.9])

X_const = sm.add_constant(X)
model = sm.OLS(Y, X_const).fit()

# Make predictions for new values
X_new = np.array([5, 12, 15])
X_new_const = sm.add_constant(X_new)

predictions = model.predict(X_new_const)

print("Point Predictions")
print("=" * 40)
for x, pred in zip(X_new, predictions):
    print(f"X = {x}: Predicted Y = {pred:.2f}")

# Warning about extrapolation
print(f"\nNote: X = 12 and X = 15 are EXTRAPOLATIONS")
print(f"(outside the range of training data: {X.min()} to {X.max()})")
print("Extrapolation predictions may be unreliable!")
```

### Prediction Intervals vs Confidence Intervals

```python
import numpy as np
import statsmodels.api as sm

X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
Y = np.array([2.1, 4.2, 5.8, 8.1, 9.5, 12.3, 14.0, 15.8, 18.2, 19.9])

X_const = sm.add_constant(X)
model = sm.OLS(Y, X_const).fit()

# Predictions with intervals
X_pred = np.array([5])
X_pred_const = sm.add_constant(X_pred, has_constant='add')

# Get prediction summary
predictions = model.get_prediction(X_pred_const)
summary = predictions.summary_frame(alpha=0.05)

print("Prediction vs Confidence Intervals for X = 5")
print("=" * 55)
print(f"Point prediction: {summary['mean'].values[0]:.4f}")
print(f"\n95% Confidence Interval for MEAN response:")
print(f"  [{summary['mean_ci_lower'].values[0]:.4f}, {summary['mean_ci_upper'].values[0]:.4f}]")
print(f"  -> Where we expect the AVERAGE Y to be at X=5")
print(f"\n95% Prediction Interval for INDIVIDUAL response:")
print(f"  [{summary['obs_ci_lower'].values[0]:.4f}, {summary['obs_ci_upper'].values[0]:.4f}]")
print(f"  -> Where we expect a SINGLE Y observation to be at X=5")

print("\nNote: Prediction intervals are WIDER because they account")
print("for both uncertainty in the mean AND individual variation.")
```

## Model Evaluation

### Comprehensive Model Summary

```python
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import mean_absolute_error, mean_squared_error

X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
Y = np.array([2.1, 4.2, 5.8, 8.1, 9.5, 12.3, 14.0, 15.8, 18.2, 19.9])

X_const = sm.add_constant(X)
model = sm.OLS(Y, X_const).fit()
Y_pred = model.predict(X_const)

print("Model Evaluation Metrics")
print("=" * 50)

# R-squared
print(f"\n1. R-squared: {model.rsquared:.4f}")
print(f"   {model.rsquared*100:.1f}% of variance in Y is explained by X")

# Adjusted R-squared
print(f"\n2. Adjusted R-squared: {model.rsquared_adj:.4f}")
print(f"   (Penalizes for additional predictors)")

# F-statistic
print(f"\n3. F-statistic: {model.fvalue:.4f}")
print(f"   P-value: {model.f_pvalue:.10f}")
print(f"   (Tests if model is better than intercept-only)")

# Error metrics
mae = mean_absolute_error(Y, Y_pred)
mse = mean_squared_error(Y, Y_pred)
rmse = np.sqrt(mse)

print(f"\n4. Error Metrics:")
print(f"   MAE (Mean Absolute Error): {mae:.4f}")
print(f"   MSE (Mean Squared Error): {mse:.4f}")
print(f"   RMSE (Root MSE): {rmse:.4f}")

# Standard error of regression
print(f"\n5. Standard Error of Regression: {np.sqrt(model.mse_resid):.4f}")
print(f"   (Typical prediction error)")
```

## Real-World Application

### Example: Advertising and Sales

```python
import numpy as np
import statsmodels.api as sm
from scipy import stats

# Advertising spend ($1000s) vs Sales ($1000s)
advertising = np.array([10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65])
sales = np.array([15, 22, 28, 35, 40, 48, 52, 58, 65, 70, 78, 82])

# Fit model
X_const = sm.add_constant(advertising)
model = sm.OLS(sales, X_const).fit()

print("Advertising-Sales Regression Analysis")
print("=" * 55)
print(f"\nRegression Equation:")
print(f"  Sales = {model.params[0]:.2f} + {model.params[1]:.4f} * Advertising")

print(f"\nCoefficient Interpretation:")
print(f"  Intercept: Even with $0 advertising, expected sales = ${model.params[0]*1000:,.0f}")
print(f"  Slope: Each additional $1,000 in advertising is associated")
print(f"         with ${model.params[1]*1000:,.0f} increase in sales")

print(f"\nModel Fit:")
print(f"  R-squared: {model.rsquared:.4f}")
print(f"  The model explains {model.rsquared*100:.1f}% of sales variation")

# ROI calculation
roi = model.params[1] - 1  # Return per dollar spent
print(f"\nReturn on Investment:")
print(f"  For every $1 spent on advertising, sales increase by ${model.params[1]:.2f}")
print(f"  ROI = {roi*100:.0f}% return on advertising investment")

# Predictions
new_budget = np.array([70, 80, 100])
new_budget_const = sm.add_constant(new_budget)
predictions = model.get_prediction(new_budget_const)
summary = predictions.summary_frame(alpha=0.05)

print(f"\nSales Predictions:")
print(f"{'Budget ($K)':<15} {'Predicted Sales':<20} {'95% CI':<25}")
print("-" * 60)
for i, budget in enumerate(new_budget):
    pred = summary.iloc[i]
    print(f"${budget}K{'':<10} ${pred['mean']*1000:,.0f}{'':<10} "
          f"[${pred['obs_ci_lower']*1000:,.0f}, ${pred['obs_ci_upper']*1000:,.0f}]")
```

## Summary

### Key Concepts

| Concept | Description |
|---------|-------------|
| $\hat{\beta}_0$ | Intercept - predicted Y when X = 0 |
| $\hat{\beta}_1$ | Slope - change in Y per unit change in X |
| $R^2$ | Proportion of variance explained |
| Residual | Difference between actual and predicted Y |
| Standard Error | Uncertainty in coefficient estimates |

### Key Assumptions

1. **Linearity**: Relationship between X and Y is linear
2. **Independence**: Observations are independent
3. **Normality**: Residuals are normally distributed
4. **Homoscedasticity**: Constant variance of residuals

### When to Use Simple Linear Regression

- One continuous predictor variable
- One continuous response variable
- Linear relationship expected
- Want to predict Y from X or understand X-Y relationship
