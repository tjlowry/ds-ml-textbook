# Multiple Linear Regression

## Overview

Multiple linear regression extends simple linear regression to include multiple predictor variables. It allows us to model complex relationships, control for confounding variables, and understand the unique contribution of each predictor.

## The Model

### Mathematical Formulation

$$Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \cdots + \beta_p X_p + \epsilon$$

Where:
- $Y$ = response variable
- $X_1, X_2, \ldots, X_p$ = predictor variables
- $\beta_0$ = intercept
- $\beta_1, \beta_2, \ldots, \beta_p$ = partial regression coefficients
- $\epsilon$ = error term
- $p$ = number of predictors

### Matrix Notation

$$\mathbf{Y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\epsilon}$$

Where:
- $\mathbf{Y}$ is an $n \times 1$ vector of responses
- $\mathbf{X}$ is an $n \times (p+1)$ design matrix (including intercept column)
- $\boldsymbol{\beta}$ is a $(p+1) \times 1$ vector of coefficients
- $\boldsymbol{\epsilon}$ is an $n \times 1$ vector of errors

### OLS Solution

$$\hat{\boldsymbol{\beta}} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{Y}$$

## Fitting a Multiple Regression Model

### Using statsmodels

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Sample data: House prices
np.random.seed(42)
n = 100

data = pd.DataFrame({
    'sqft': np.random.uniform(1000, 3000, n),
    'bedrooms': np.random.randint(2, 6, n),
    'age': np.random.uniform(0, 50, n),
    'distance_downtown': np.random.uniform(1, 30, n)
})

# Generate price with some noise
data['price'] = (
    50000 +
    150 * data['sqft'] +
    20000 * data['bedrooms'] -
    1000 * data['age'] -
    3000 * data['distance_downtown'] +
    np.random.normal(0, 30000, n)
)

# Fit multiple regression
X = data[['sqft', 'bedrooms', 'age', 'distance_downtown']]
X = sm.add_constant(X)
y = data['price']

model = sm.OLS(y, X).fit()
print(model.summary())
```

### Using scikit-learn

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

# Using the same data
X = data[['sqft', 'bedrooms', 'age', 'distance_downtown']]
y = data['price']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit model
model = LinearRegression()
model.fit(X_train, y_train)

# Results
print("Multiple Linear Regression (scikit-learn)")
print("=" * 50)
print(f"Intercept: {model.intercept_:.2f}")
print("\nCoefficients:")
for name, coef in zip(X.columns, model.coef_):
    print(f"  {name}: {coef:.2f}")

# Evaluate
y_pred = model.predict(X_test)
print(f"\nTest Set Performance:")
print(f"  R-squared: {r2_score(y_test, y_pred):.4f}")
print(f"  RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")
```

## Interpreting Coefficients

### Partial Regression Coefficients

In multiple regression, each coefficient represents the change in Y for a one-unit change in that predictor, **holding all other predictors constant**.

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Recreate model
np.random.seed(42)
n = 100
data = pd.DataFrame({
    'sqft': np.random.uniform(1000, 3000, n),
    'bedrooms': np.random.randint(2, 6, n),
    'age': np.random.uniform(0, 50, n),
    'distance_downtown': np.random.uniform(1, 30, n)
})
data['price'] = (50000 + 150 * data['sqft'] + 20000 * data['bedrooms'] -
                 1000 * data['age'] - 3000 * data['distance_downtown'] +
                 np.random.normal(0, 30000, n))

X = sm.add_constant(data[['sqft', 'bedrooms', 'age', 'distance_downtown']])
model = sm.OLS(data['price'], X).fit()

print("Coefficient Interpretation")
print("=" * 60)

interpretations = {
    'const': 'Base price when all predictors are zero',
    'sqft': 'Price increase per additional square foot',
    'bedrooms': 'Price increase per additional bedroom',
    'age': 'Price change per year of house age',
    'distance_downtown': 'Price change per mile from downtown'
}

for var, coef in zip(model.params.index, model.params.values):
    print(f"\n{var}:")
    print(f"  Coefficient: ${coef:,.2f}")
    print(f"  Interpretation: {interpretations[var]}")
    if var != 'const':
        print(f"  Holding other variables constant, a 1-unit increase in {var}")
        print(f"  is associated with a ${coef:,.2f} change in price.")
```

### Standardized Coefficients (Beta Weights)

Standardized coefficients allow comparison of relative importance when predictors have different scales.

```python
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm

# Standardize variables
def standardize(x):
    return (x - np.mean(x)) / np.std(x)

# Recreate data
np.random.seed(42)
n = 100
data = pd.DataFrame({
    'sqft': np.random.uniform(1000, 3000, n),
    'bedrooms': np.random.randint(2, 6, n),
    'age': np.random.uniform(0, 50, n),
    'distance_downtown': np.random.uniform(1, 30, n)
})
data['price'] = (50000 + 150 * data['sqft'] + 20000 * data['bedrooms'] -
                 1000 * data['age'] - 3000 * data['distance_downtown'] +
                 np.random.normal(0, 30000, n))

# Standardize all variables
data_std = data.apply(standardize)

# Fit model with standardized variables (no intercept needed)
X_std = data_std[['sqft', 'bedrooms', 'age', 'distance_downtown']]
y_std = data_std['price']

model_std = sm.OLS(y_std, X_std).fit()

print("Standardized Coefficients (Beta Weights)")
print("=" * 50)
print("\nThese show relative importance (same scale)")
print("\n" + "-" * 50)

# Sort by absolute value
sorted_coefs = model_std.params.abs().sort_values(ascending=False)

for var in sorted_coefs.index:
    coef = model_std.params[var]
    print(f"{var:<20} {coef:>8.4f} {'*' * int(abs(coef) * 20)}")

print("\nInterpretation: A 1 standard deviation increase in X")
print("is associated with a [coef] standard deviation change in Y.")
```

## Model Evaluation

### R-squared and Adjusted R-squared

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Recreate data and model
np.random.seed(42)
n = 100
data = pd.DataFrame({
    'sqft': np.random.uniform(1000, 3000, n),
    'bedrooms': np.random.randint(2, 6, n),
    'age': np.random.uniform(0, 50, n),
    'distance_downtown': np.random.uniform(1, 30, n)
})
data['price'] = (50000 + 150 * data['sqft'] + 20000 * data['bedrooms'] -
                 1000 * data['age'] - 3000 * data['distance_downtown'] +
                 np.random.normal(0, 30000, n))

X = sm.add_constant(data[['sqft', 'bedrooms', 'age', 'distance_downtown']])
model = sm.OLS(data['price'], X).fit()

print("R-squared Metrics")
print("=" * 50)
print(f"\nR-squared: {model.rsquared:.4f}")
print(f"  {model.rsquared*100:.1f}% of variance in price is explained")
print(f"  by the predictors.")

print(f"\nAdjusted R-squared: {model.rsquared_adj:.4f}")
print(f"  Adjusts for number of predictors.")
print(f"  Penalizes adding unhelpful variables.")

# Formula for adjusted R-squared
n = len(data)
p = 4  # number of predictors
adj_r2_manual = 1 - (1 - model.rsquared) * (n - 1) / (n - p - 1)
print(f"\n  Manual calculation: {adj_r2_manual:.4f}")
```

### F-Test for Overall Model Significance

Tests whether at least one predictor has a non-zero coefficient.

$$H_0: \beta_1 = \beta_2 = \cdots = \beta_p = 0$$
$$H_1: \text{At least one } \beta_j \neq 0$$

```python
import statsmodels.api as sm
import pandas as pd
import numpy as np

# Recreate data and model
np.random.seed(42)
n = 100
data = pd.DataFrame({
    'sqft': np.random.uniform(1000, 3000, n),
    'bedrooms': np.random.randint(2, 6, n),
    'age': np.random.uniform(0, 50, n),
    'distance_downtown': np.random.uniform(1, 30, n)
})
data['price'] = (50000 + 150 * data['sqft'] + 20000 * data['bedrooms'] -
                 1000 * data['age'] - 3000 * data['distance_downtown'] +
                 np.random.normal(0, 30000, n))

X = sm.add_constant(data[['sqft', 'bedrooms', 'age', 'distance_downtown']])
model = sm.OLS(data['price'], X).fit()

print("F-Test for Overall Model")
print("=" * 50)
print(f"\nH0: All coefficients = 0 (model is useless)")
print(f"H1: At least one coefficient != 0")
print(f"\nF-statistic: {model.fvalue:.4f}")
print(f"P-value: {model.f_pvalue:.2e}")

alpha = 0.05
if model.f_pvalue < alpha:
    print(f"\nConclusion: Reject H0 at alpha = {alpha}")
    print("The model has significant predictive power.")
else:
    print(f"\nConclusion: Fail to reject H0")
    print("No significant relationship detected.")
```

### Individual Coefficient Tests

```python
import statsmodels.api as sm
import pandas as pd
import numpy as np

# Recreate data and model
np.random.seed(42)
n = 100
data = pd.DataFrame({
    'sqft': np.random.uniform(1000, 3000, n),
    'bedrooms': np.random.randint(2, 6, n),
    'age': np.random.uniform(0, 50, n),
    'distance_downtown': np.random.uniform(1, 30, n)
})
data['price'] = (50000 + 150 * data['sqft'] + 20000 * data['bedrooms'] -
                 1000 * data['age'] - 3000 * data['distance_downtown'] +
                 np.random.normal(0, 30000, n))

X = sm.add_constant(data[['sqft', 'bedrooms', 'age', 'distance_downtown']])
model = sm.OLS(data['price'], X).fit()

print("Individual Coefficient Tests")
print("=" * 60)
print(f"{'Variable':<20} {'Coef':<12} {'t-stat':<10} {'p-value':<12} {'Sig?':<5}")
print("-" * 60)

alpha = 0.05
for var in model.params.index:
    coef = model.params[var]
    tstat = model.tvalues[var]
    pval = model.pvalues[var]
    sig = "***" if pval < 0.001 else "**" if pval < 0.01 else "*" if pval < 0.05 else ""
    print(f"{var:<20} {coef:<12.2f} {tstat:<10.3f} {pval:<12.4f} {sig:<5}")

print("\n*** p < 0.001, ** p < 0.01, * p < 0.05")
```

## Multicollinearity

### Detection

Multicollinearity occurs when predictors are highly correlated with each other, making it difficult to isolate their individual effects.

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Create data with multicollinearity
np.random.seed(42)
n = 100

data = pd.DataFrame({
    'x1': np.random.normal(0, 1, n),
    'x2': np.random.normal(0, 1, n),
})
# x3 is highly correlated with x1
data['x3'] = data['x1'] + np.random.normal(0, 0.1, n)
data['y'] = 2 + 3*data['x1'] + 1.5*data['x2'] + np.random.normal(0, 1, n)

# Check correlations
print("Correlation Matrix")
print("=" * 40)
print(data[['x1', 'x2', 'x3']].corr().round(3))

# Calculate VIF
X = sm.add_constant(data[['x1', 'x2', 'x3']])
vif_data = pd.DataFrame()
vif_data['Variable'] = X.columns
vif_data['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

print("\n\nVariance Inflation Factors (VIF)")
print("=" * 40)
print(vif_data)
print("\nInterpretation:")
print("  VIF = 1: No correlation with other predictors")
print("  VIF > 5: Moderate multicollinearity")
print("  VIF > 10: Severe multicollinearity - consider removing variable")
```

### Effects of Multicollinearity

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

np.random.seed(42)
n = 100

# Data WITHOUT multicollinearity
data_no_mc = pd.DataFrame({
    'x1': np.random.normal(0, 1, n),
    'x2': np.random.normal(0, 1, n),
})
data_no_mc['y'] = 2 + 3*data_no_mc['x1'] + 1.5*data_no_mc['x2'] + np.random.normal(0, 1, n)

# Data WITH multicollinearity
data_mc = pd.DataFrame({
    'x1': np.random.normal(0, 1, n),
})
data_mc['x2'] = data_mc['x1'] + np.random.normal(0, 0.1, n)  # Highly correlated
data_mc['y'] = 2 + 3*data_mc['x1'] + 1.5*data_mc['x2'] + np.random.normal(0, 1, n)

# Fit both models
X_no_mc = sm.add_constant(data_no_mc[['x1', 'x2']])
model_no_mc = sm.OLS(data_no_mc['y'], X_no_mc).fit()

X_mc = sm.add_constant(data_mc[['x1', 'x2']])
model_mc = sm.OLS(data_mc['y'], X_mc).fit()

print("Effects of Multicollinearity")
print("=" * 60)

print("\nWithout Multicollinearity:")
print(f"  x1 coef: {model_no_mc.params['x1']:.3f} (SE: {model_no_mc.bse['x1']:.3f})")
print(f"  x2 coef: {model_no_mc.params['x2']:.3f} (SE: {model_no_mc.bse['x2']:.3f})")
print(f"  R-squared: {model_no_mc.rsquared:.4f}")

print("\nWith Multicollinearity:")
print(f"  x1 coef: {model_mc.params['x1']:.3f} (SE: {model_mc.bse['x1']:.3f})")
print(f"  x2 coef: {model_mc.params['x2']:.3f} (SE: {model_mc.bse['x2']:.3f})")
print(f"  R-squared: {model_mc.rsquared:.4f}")

print("\nProblems caused by multicollinearity:")
print("  1. Inflated standard errors")
print("  2. Unstable coefficient estimates")
print("  3. Coefficients may have wrong sign")
print("  4. Difficult to interpret individual effects")
print("  Note: R-squared and predictions can still be fine!")
```

## Feature Selection

### Forward Selection

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

def forward_selection(X, y, significance_level=0.05):
    """
    Perform forward stepwise selection based on p-values.
    """
    initial_features = []
    remaining_features = list(X.columns)
    best_features = []

    while remaining_features:
        best_pvalue = 1
        best_feature = None

        for feature in remaining_features:
            features_to_test = initial_features + [feature]
            X_test = sm.add_constant(X[features_to_test])
            model = sm.OLS(y, X_test).fit()
            pvalue = model.pvalues[feature]

            if pvalue < best_pvalue:
                best_pvalue = pvalue
                best_feature = feature

        if best_pvalue < significance_level:
            initial_features.append(best_feature)
            remaining_features.remove(best_feature)
            print(f"Added {best_feature} (p-value: {best_pvalue:.4f})")
        else:
            break

    return initial_features

# Example
np.random.seed(42)
n = 200
data = pd.DataFrame({
    'x1': np.random.normal(0, 1, n),
    'x2': np.random.normal(0, 1, n),
    'x3': np.random.normal(0, 1, n),  # Not significant
    'x4': np.random.normal(0, 1, n),
    'x5': np.random.normal(0, 1, n),  # Not significant
})
data['y'] = 2 + 3*data['x1'] + 1.5*data['x2'] + 2*data['x4'] + np.random.normal(0, 1, n)

X = data[['x1', 'x2', 'x3', 'x4', 'x5']]
y = data['y']

print("Forward Selection")
print("=" * 50)
selected = forward_selection(X, y)
print(f"\nSelected features: {selected}")
```

### Using Information Criteria

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
from itertools import combinations

def evaluate_all_models(X, y):
    """
    Evaluate all possible models and return AIC/BIC.
    """
    features = list(X.columns)
    results = []

    # Try all combinations
    for k in range(1, len(features) + 1):
        for combo in combinations(features, k):
            X_subset = sm.add_constant(X[list(combo)])
            model = sm.OLS(y, X_subset).fit()
            results.append({
                'features': combo,
                'n_features': k,
                'r_squared': model.rsquared,
                'adj_r_squared': model.rsquared_adj,
                'AIC': model.aic,
                'BIC': model.bic
            })

    return pd.DataFrame(results)

# Example with small number of features
np.random.seed(42)
n = 100
data = pd.DataFrame({
    'x1': np.random.normal(0, 1, n),
    'x2': np.random.normal(0, 1, n),
    'x3': np.random.normal(0, 1, n),
    'x4': np.random.normal(0, 1, n),
})
data['y'] = 2 + 3*data['x1'] + 1.5*data['x2'] + np.random.normal(0, 1, n)

X = data[['x1', 'x2', 'x3', 'x4']]
y = data['y']

results = evaluate_all_models(X, y)

print("Model Comparison using Information Criteria")
print("=" * 70)
print("\nTop 5 models by AIC:")
print(results.nsmallest(5, 'AIC')[['features', 'adj_r_squared', 'AIC', 'BIC']])

print("\nTop 5 models by BIC:")
print(results.nsmallest(5, 'BIC')[['features', 'adj_r_squared', 'AIC', 'BIC']])

print("\nNote: Lower AIC/BIC is better")
print("AIC tends to select larger models")
print("BIC penalizes complexity more, selecting simpler models")
```

## Categorical Predictors

### Dummy Variables

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Create data with categorical variable
np.random.seed(42)
n = 150

data = pd.DataFrame({
    'experience': np.random.uniform(1, 20, n),
    'education': np.random.choice(['High School', 'Bachelor', 'Master'], n),
    'salary': np.zeros(n)
})

# Generate salary based on education
base = {'High School': 40000, 'Bachelor': 55000, 'Master': 70000}
for i, row in data.iterrows():
    data.loc[i, 'salary'] = (base[row['education']] +
                             2000 * row['experience'] +
                             np.random.normal(0, 5000))

# Create dummy variables
data_encoded = pd.get_dummies(data, columns=['education'], drop_first=True)

print("Original Data (first 5 rows):")
print(data.head())

print("\n\nWith Dummy Variables:")
print(data_encoded.head())

# Fit model
X = sm.add_constant(data_encoded[['experience', 'education_High School', 'education_Master']])
y = data_encoded['salary']
model = sm.OLS(y, X).fit()

print("\n\nRegression Results:")
print("=" * 60)
print(model.summary())

print("\n\nInterpretation:")
print(f"  Base category: Bachelor's degree")
print(f"  High School effect: ${model.params['education_High School']:,.0f} less than Bachelor")
print(f"  Master's effect: ${model.params['education_Master']:,.0f} more than Bachelor")
```

## Interaction Terms

### Creating and Interpreting Interactions

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Create data where effect of experience depends on education
np.random.seed(42)
n = 200

data = pd.DataFrame({
    'experience': np.random.uniform(0, 20, n),
    'education_years': np.random.choice([12, 16, 18], n),  # HS, Bachelor, Master
})

# Interaction: education amplifies effect of experience
data['salary'] = (30000 +
                  1000 * data['experience'] +
                  3000 * data['education_years'] +
                  200 * data['experience'] * data['education_years'] +  # Interaction
                  np.random.normal(0, 5000, n))

# Model WITHOUT interaction
X_no_int = sm.add_constant(data[['experience', 'education_years']])
model_no_int = sm.OLS(data['salary'], X_no_int).fit()

# Model WITH interaction
data['exp_x_edu'] = data['experience'] * data['education_years']
X_int = sm.add_constant(data[['experience', 'education_years', 'exp_x_edu']])
model_int = sm.OLS(data['salary'], X_int).fit()

print("Model Comparison: With vs Without Interaction")
print("=" * 60)

print("\nWithout Interaction:")
print(f"  R-squared: {model_no_int.rsquared:.4f}")
print(f"  AIC: {model_no_int.aic:.1f}")

print("\nWith Interaction:")
print(f"  R-squared: {model_int.rsquared:.4f}")
print(f"  AIC: {model_int.aic:.1f}")

print("\nInteraction Coefficient:")
print(f"  exp_x_edu: {model_int.params['exp_x_edu']:.2f}")
print(f"  p-value: {model_int.pvalues['exp_x_edu']:.4f}")

print("\nInterpretation:")
print("  The effect of experience on salary depends on education level.")
print("  For each additional year of education, the return to experience")
print(f"  increases by ${model_int.params['exp_x_edu']:.0f} per year.")
```

## Real-World Application

### House Price Prediction

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# Create realistic housing data
np.random.seed(42)
n = 500

data = pd.DataFrame({
    'sqft': np.random.uniform(800, 4000, n),
    'bedrooms': np.random.randint(1, 6, n),
    'bathrooms': np.random.randint(1, 4, n),
    'age': np.random.uniform(0, 80, n),
    'has_garage': np.random.choice([0, 1], n, p=[0.3, 0.7]),
    'neighborhood': np.random.choice(['A', 'B', 'C'], n),
    'lot_size': np.random.uniform(2000, 15000, n)
})

# Generate realistic prices
neighborhood_premium = {'A': 50000, 'B': 0, 'C': -30000}
data['price'] = (
    100000 +
    200 * data['sqft'] +
    25000 * data['bedrooms'] +
    15000 * data['bathrooms'] -
    1500 * data['age'] +
    30000 * data['has_garage'] +
    data['neighborhood'].map(neighborhood_premium) +
    5 * data['lot_size'] +
    np.random.normal(0, 40000, n)
)

# Prepare features
data_model = pd.get_dummies(data, columns=['neighborhood'], drop_first=True)
feature_cols = ['sqft', 'bedrooms', 'bathrooms', 'age', 'has_garage',
                'lot_size', 'neighborhood_B', 'neighborhood_C']

X = data_model[feature_cols]
y = data_model['price']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit model
X_train_const = sm.add_constant(X_train)
X_test_const = sm.add_constant(X_test)

model = sm.OLS(y_train, X_train_const).fit()

print("House Price Prediction Model")
print("=" * 70)
print(model.summary())

# Predictions
y_pred = model.predict(X_test_const)

print("\n\nTest Set Performance:")
print("-" * 40)
print(f"R-squared: {r2_score(y_test, y_pred):.4f}")
print(f"MAE: ${mean_absolute_error(y_test, y_pred):,.0f}")
print(f"RMSE: ${np.sqrt(np.mean((y_test - y_pred)**2)):,.0f}")

# Example prediction
print("\n\nExample Prediction:")
print("-" * 40)
example = pd.DataFrame({
    'const': [1],
    'sqft': [2000],
    'bedrooms': [3],
    'bathrooms': [2],
    'age': [10],
    'has_garage': [1],
    'lot_size': [8000],
    'neighborhood_B': [0],
    'neighborhood_C': [0]
})

pred = model.predict(example)
pred_ci = model.get_prediction(example).summary_frame(alpha=0.05)

print(f"House: 2000 sqft, 3 bed, 2 bath, 10 years old, garage, Neighborhood A")
print(f"Predicted price: ${pred[0]:,.0f}")
print(f"95% CI: [${pred_ci['obs_ci_lower'].values[0]:,.0f}, ${pred_ci['obs_ci_upper'].values[0]:,.0f}]")
```

## Summary

### Key Concepts

| Concept | Description |
|---------|-------------|
| Partial regression coefficient | Effect of X on Y, holding other variables constant |
| R-squared | Proportion of variance explained by all predictors |
| Adjusted R-squared | R-squared adjusted for number of predictors |
| VIF | Measure of multicollinearity (VIF > 10 is problematic) |
| F-test | Tests if model is better than intercept-only |

### Best Practices

1. **Check assumptions** before interpreting results
2. **Examine multicollinearity** using VIF and correlation matrices
3. **Use adjusted R-squared** when comparing models with different numbers of predictors
4. **Consider interactions** when effects might depend on other variables
5. **Validate** on held-out test data
6. **Report confidence intervals** for coefficients, not just point estimates

## How I Did It — MATH 425 (BYU-Idaho)

My multiple-regression analysis used the `CarPrices` data, filtered to one model (the Chevrolet
Cavalier), to ask a two-part question: does **cruise control** change the price, and does it
change how fast the car **depreciates with mileage**? That's a classic **two-line regression** —
a continuous predictor (`Mileage`), an indicator (`Cruise`, 0/1), and their **interaction**:

$$
  \underbrace{Y_i}_{\text{Price}} = \beta_0 + \beta_1 \underbrace{X_{i1}}_{\text{Mileage}}
  + \beta_2 \underbrace{X_{i2}}_{\text{Cruise}} + \beta_3 \underbrace{X_{i1}X_{i2}}_{\text{Interaction}} + \epsilon_i
$$

```r
CarPrices <- filter(CarPrices, Model == "Cavalier")

carlm  <- lm(Price ~ Mileage + Cruise + Mileage:Cruise, data = CarPrices)  # full two-line
summary(carlm) %>% pander()
```

The interaction $\beta_3$ (different depreciation slopes) came back at **p = 0.5872** — not
significant — so I dropped it and refit. In the additive model, the `Cruise` main effect was
still insignificant (**p = 0.2238**), so I dropped that too, landing on a simple regression of
price on mileage alone:

```r
carlm2 <- lm(Price ~ Mileage + Cruise,  data = CarPrices)  # Cruise p = 0.2238 -> drop
carlm3 <- lm(Price ~ Mileage,           data = CarPrices)  # final model
summary(carlm3) %>% pander()
```

Mileage was overwhelmingly significant (**p = 1.299e-16**). The takeaway: for a used Cavalier,
cruise control doesn't move the price in either direction — only mileage does — and these cars
don't hold their value well as they rack up miles.

Source: `~/Projects/school/byui-undergrad/statistics-notebook/Analyses/Linear Regression/CarPrices.Rmd`

### Gotchas

- **Test the interaction before the main effects.** If $\beta_3$ (the interaction) isn't
  significant, remove it *first*, then reassess the main effects — interpreting a main effect
  while a live interaction term is in the model is misleading.
- **Simplify deliberately, one term at a time.** I removed the interaction, refit, *then*
  removed `Cruise` — not both at once — so each p-value was judged in the model it actually
  belonged to.
- **An indicator + interaction is literally two lines.** `Cruise` shifts the intercept and
  `Mileage:Cruise` tilts the slope; picturing it as two fitted lines (cruise vs. no-cruise) is
  what makes the coefficients interpretable.
