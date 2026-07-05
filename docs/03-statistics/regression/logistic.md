# Logistic Regression

## Overview

Logistic regression is used when the response variable is binary (0/1, yes/no, success/failure). Unlike linear regression, which predicts a continuous value, logistic regression predicts the probability of belonging to a particular class.

## Why Not Linear Regression?

### The Problem with Linear Regression for Binary Outcomes

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Binary outcome: Pass/Fail based on study hours
np.random.seed(42)
hours = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
passed = np.array([0, 0, 0, 0, 1, 0, 1, 1, 1, 1])

# Fit linear regression
model = LinearRegression()
model.fit(hours.reshape(-1, 1), passed)

# Predictions
hours_range = np.linspace(0, 15, 100)
linear_pred = model.predict(hours_range.reshape(-1, 1))

print("Problems with Linear Regression for Binary Outcomes:")
print("=" * 55)
print(f"\nPrediction for 0 hours: {model.predict([[0]])[0]:.3f}")
print(f"Prediction for 15 hours: {model.predict([[15]])[0]:.3f}")
print("\nIssues:")
print("1. Predictions can be < 0 or > 1 (not valid probabilities)")
print("2. Assumes constant effect of X (not realistic for probabilities)")
print("3. Residuals are not normally distributed")
print("4. Heteroscedasticity is inherent")
```

## The Logistic Model

### Mathematical Formulation

The logistic regression model predicts the log-odds (logit) of the probability:

$$\log\left(\frac{p}{1-p}\right) = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \cdots + \beta_p X_p$$

Where $p = P(Y = 1 | X)$ is the probability of the positive class.

### The Logistic (Sigmoid) Function

Converting log-odds to probability:

$$p = \frac{1}{1 + e^{-(\beta_0 + \beta_1 X_1 + \cdots)}} = \frac{e^{(\beta_0 + \beta_1 X_1 + \cdots)}}{1 + e^{(\beta_0 + \beta_1 X_1 + \cdots)}}$$

```python
import numpy as np

def sigmoid(z):
    """The logistic/sigmoid function."""
    return 1 / (1 + np.exp(-z))

# Demonstrate sigmoid properties
z_values = np.linspace(-6, 6, 100)
probabilities = sigmoid(z_values)

print("Sigmoid Function Properties:")
print("=" * 40)
print(f"sigmoid(-inf) -> {sigmoid(-10):.6f} (approaches 0)")
print(f"sigmoid(0) = {sigmoid(0):.6f} (exactly 0.5)")
print(f"sigmoid(+inf) -> {sigmoid(10):.6f} (approaches 1)")
print("\nThe sigmoid ensures output is always between 0 and 1")
```

## Fitting Logistic Regression

### Using statsmodels

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Create sample data: Predicting customer churn
np.random.seed(42)
n = 500

data = pd.DataFrame({
    'tenure': np.random.uniform(0, 72, n),  # Months with company
    'monthly_charges': np.random.uniform(20, 100, n),
    'total_charges': np.zeros(n),
    'support_calls': np.random.poisson(2, n)
})
data['total_charges'] = data['tenure'] * data['monthly_charges']

# Generate churn probability based on features
log_odds = (-2 - 0.05 * data['tenure'] + 0.03 * data['monthly_charges'] +
            0.3 * data['support_calls'])
prob_churn = 1 / (1 + np.exp(-log_odds))
data['churn'] = np.random.binomial(1, prob_churn)

# Fit logistic regression
X = sm.add_constant(data[['tenure', 'monthly_charges', 'support_calls']])
y = data['churn']

model = sm.Logit(y, X)
results = model.fit()

print(results.summary())
```

### Using scikit-learn

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Using the same data
np.random.seed(42)
n = 500
data = pd.DataFrame({
    'tenure': np.random.uniform(0, 72, n),
    'monthly_charges': np.random.uniform(20, 100, n),
    'support_calls': np.random.poisson(2, n)
})
log_odds = (-2 - 0.05 * data['tenure'] + 0.03 * data['monthly_charges'] +
            0.3 * data['support_calls'])
data['churn'] = np.random.binomial(1, 1 / (1 + np.exp(-log_odds)))

X = data[['tenure', 'monthly_charges', 'support_calls']]
y = data['churn']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit model
model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)

# Results
print("Logistic Regression with scikit-learn")
print("=" * 50)
print(f"\nIntercept: {model.intercept_[0]:.4f}")
print("\nCoefficients:")
for name, coef in zip(X.columns, model.coef_[0]):
    print(f"  {name}: {coef:.4f}")

# Predictions
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
```

## Interpreting Coefficients

### Log-Odds Interpretation

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Recreate model
np.random.seed(42)
n = 500
data = pd.DataFrame({
    'tenure': np.random.uniform(0, 72, n),
    'monthly_charges': np.random.uniform(20, 100, n),
    'support_calls': np.random.poisson(2, n)
})
log_odds = (-2 - 0.05 * data['tenure'] + 0.03 * data['monthly_charges'] +
            0.3 * data['support_calls'])
data['churn'] = np.random.binomial(1, 1 / (1 + np.exp(-log_odds)))

X = sm.add_constant(data[['tenure', 'monthly_charges', 'support_calls']])
y = data['churn']
results = sm.Logit(y, X).fit(disp=0)

print("Coefficient Interpretation")
print("=" * 60)

for var in results.params.index:
    coef = results.params[var]
    print(f"\n{var}:")
    print(f"  Coefficient (log-odds): {coef:.4f}")
    if var != 'const':
        print(f"  For 1-unit increase in {var}:")
        print(f"    - Log-odds of churn changes by {coef:.4f}")
```

### Odds Ratio Interpretation

The odds ratio is $e^\beta$ - a more intuitive interpretation.

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Recreate model
np.random.seed(42)
n = 500
data = pd.DataFrame({
    'tenure': np.random.uniform(0, 72, n),
    'monthly_charges': np.random.uniform(20, 100, n),
    'support_calls': np.random.poisson(2, n)
})
log_odds = (-2 - 0.05 * data['tenure'] + 0.03 * data['monthly_charges'] +
            0.3 * data['support_calls'])
data['churn'] = np.random.binomial(1, 1 / (1 + np.exp(-log_odds)))

X = sm.add_constant(data[['tenure', 'monthly_charges', 'support_calls']])
y = data['churn']
results = sm.Logit(y, X).fit(disp=0)

print("Odds Ratio Interpretation")
print("=" * 60)

# Calculate odds ratios
odds_ratios = np.exp(results.params)
conf_int = np.exp(results.conf_int())

print(f"\n{'Variable':<20} {'Odds Ratio':<12} {'95% CI':<20}")
print("-" * 55)

for var in results.params.index:
    or_val = odds_ratios[var]
    ci_low, ci_high = conf_int.loc[var]
    print(f"{var:<20} {or_val:<12.4f} [{ci_low:.4f}, {ci_high:.4f}]")

print("\nInterpretation:")
print("-" * 55)
for var in ['tenure', 'monthly_charges', 'support_calls']:
    or_val = odds_ratios[var]
    if or_val > 1:
        change = (or_val - 1) * 100
        print(f"{var}: Each 1-unit increase multiplies odds by {or_val:.3f}")
        print(f"         (increases odds of churn by {change:.1f}%)")
    else:
        change = (1 - or_val) * 100
        print(f"{var}: Each 1-unit increase multiplies odds by {or_val:.3f}")
        print(f"         (decreases odds of churn by {change:.1f}%)")
    print()
```

## Model Evaluation

### Confusion Matrix

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Recreate model
np.random.seed(42)
n = 500
data = pd.DataFrame({
    'tenure': np.random.uniform(0, 72, n),
    'monthly_charges': np.random.uniform(20, 100, n),
    'support_calls': np.random.poisson(2, n)
})
log_odds = (-2 - 0.05 * data['tenure'] + 0.03 * data['monthly_charges'] +
            0.3 * data['support_calls'])
data['churn'] = np.random.binomial(1, 1 / (1 + np.exp(-log_odds)))

X = data[['tenure', 'monthly_charges', 'support_calls']]
y = data['churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)

print("Confusion Matrix")
print("=" * 50)
print(f"\n                 Predicted")
print(f"               No Churn  Churn")
print(f"Actual No Churn    {cm[0,0]:<6}  {cm[0,1]:<6}")
print(f"       Churn       {cm[1,0]:<6}  {cm[1,1]:<6}")

# Extract metrics
TN, FP, FN, TP = cm.ravel()

print(f"\nBreakdown:")
print(f"  True Negatives (TN): {TN} - Correctly predicted no churn")
print(f"  True Positives (TP): {TP} - Correctly predicted churn")
print(f"  False Negatives (FN): {FN} - Missed churns (Type II error)")
print(f"  False Positives (FP): {FP} - False alarms (Type I error)")
```

### Performance Metrics

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, confusion_matrix)

# Recreate and fit model
np.random.seed(42)
n = 500
data = pd.DataFrame({
    'tenure': np.random.uniform(0, 72, n),
    'monthly_charges': np.random.uniform(20, 100, n),
    'support_calls': np.random.poisson(2, n)
})
log_odds = (-2 - 0.05 * data['tenure'] + 0.03 * data['monthly_charges'] +
            0.3 * data['support_calls'])
data['churn'] = np.random.binomial(1, 1 / (1 + np.exp(-log_odds)))

X = data[['tenure', 'monthly_charges', 'support_calls']]
y = data['churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# Calculate metrics
print("Classification Metrics")
print("=" * 50)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_prob)

print(f"\nAccuracy:  {accuracy:.4f} - Overall correct predictions")
print(f"Precision: {precision:.4f} - Of predicted churns, how many are correct")
print(f"Recall:    {recall:.4f} - Of actual churns, how many were caught")
print(f"F1 Score:  {f1:.4f} - Harmonic mean of precision and recall")
print(f"AUC-ROC:   {auc:.4f} - Model's ability to discriminate")

# Confusion matrix for reference
cm = confusion_matrix(y_test, y_pred)
TN, FP, FN, TP = cm.ravel()

print(f"\nFormulas:")
print(f"  Accuracy  = (TP + TN) / Total = ({TP} + {TN}) / {len(y_test)} = {accuracy:.4f}")
print(f"  Precision = TP / (TP + FP) = {TP} / ({TP} + {FP}) = {precision:.4f}")
print(f"  Recall    = TP / (TP + FN) = {TP} / ({TP} + {FN}) = {recall:.4f}")
```

### ROC Curve and AUC

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score

# Recreate model
np.random.seed(42)
n = 500
data = pd.DataFrame({
    'tenure': np.random.uniform(0, 72, n),
    'monthly_charges': np.random.uniform(20, 100, n),
    'support_calls': np.random.poisson(2, n)
})
log_odds = (-2 - 0.05 * data['tenure'] + 0.03 * data['monthly_charges'] +
            0.3 * data['support_calls'])
data['churn'] = np.random.binomial(1, 1 / (1 + np.exp(-log_odds)))

X = data[['tenure', 'monthly_charges', 'support_calls']]
y = data['churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)
y_prob = model.predict_proba(X_test)[:, 1]

# ROC curve data
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
auc = roc_auc_score(y_test, y_prob)

print("ROC Curve Analysis")
print("=" * 50)
print(f"\nAUC (Area Under Curve): {auc:.4f}")

print("\nAUC Interpretation:")
print("  0.5 = Random guessing (diagonal line)")
print("  0.7-0.8 = Acceptable discrimination")
print("  0.8-0.9 = Excellent discrimination")
print("  > 0.9 = Outstanding discrimination")

# Show some threshold examples
print("\nThreshold Analysis:")
print(f"{'Threshold':<12} {'FPR':<10} {'TPR (Recall)':<12}")
print("-" * 35)
for i in range(0, len(thresholds), len(thresholds)//5):
    print(f"{thresholds[i]:<12.3f} {fpr[i]:<10.3f} {tpr[i]:<12.3f}")
```

### Threshold Selection

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score

# Recreate model
np.random.seed(42)
n = 500
data = pd.DataFrame({
    'tenure': np.random.uniform(0, 72, n),
    'monthly_charges': np.random.uniform(20, 100, n),
    'support_calls': np.random.poisson(2, n)
})
log_odds = (-2 - 0.05 * data['tenure'] + 0.03 * data['monthly_charges'] +
            0.3 * data['support_calls'])
data['churn'] = np.random.binomial(1, 1 / (1 + np.exp(-log_odds)))

X = data[['tenure', 'monthly_charges', 'support_calls']]
y = data['churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)
y_prob = model.predict_proba(X_test)[:, 1]

# Evaluate different thresholds
print("Threshold Optimization")
print("=" * 60)
print(f"\n{'Threshold':<12} {'Precision':<12} {'Recall':<12} {'F1 Score':<12}")
print("-" * 50)

best_f1 = 0
best_threshold = 0.5

for threshold in np.arange(0.1, 0.9, 0.1):
    y_pred_thresh = (y_prob >= threshold).astype(int)

    # Handle edge cases
    if sum(y_pred_thresh) == 0:
        continue

    prec = precision_score(y_test, y_pred_thresh)
    rec = recall_score(y_test, y_pred_thresh)
    f1 = f1_score(y_test, y_pred_thresh)

    print(f"{threshold:<12.2f} {prec:<12.4f} {rec:<12.4f} {f1:<12.4f}")

    if f1 > best_f1:
        best_f1 = f1
        best_threshold = threshold

print(f"\nBest threshold for F1: {best_threshold:.2f}")

print("\nConsiderations for threshold selection:")
print("  - High precision needed: Higher threshold (fewer false positives)")
print("  - High recall needed: Lower threshold (catch more positives)")
print("  - Balanced: Optimize F1 or use cost-based analysis")
```

## Model Fit Statistics

### Pseudo R-squared

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Recreate data
np.random.seed(42)
n = 500
data = pd.DataFrame({
    'tenure': np.random.uniform(0, 72, n),
    'monthly_charges': np.random.uniform(20, 100, n),
    'support_calls': np.random.poisson(2, n)
})
log_odds = (-2 - 0.05 * data['tenure'] + 0.03 * data['monthly_charges'] +
            0.3 * data['support_calls'])
data['churn'] = np.random.binomial(1, 1 / (1 + np.exp(-log_odds)))

X = sm.add_constant(data[['tenure', 'monthly_charges', 'support_calls']])
y = data['churn']

results = sm.Logit(y, X).fit(disp=0)

print("Model Fit Statistics")
print("=" * 50)
print(f"\nLog-Likelihood: {results.llf:.4f}")
print(f"Null Log-Likelihood: {results.llnull:.4f}")

print(f"\nPseudo R-squared (McFadden): {results.prsquared:.4f}")

# Calculate manually
pseudo_r2 = 1 - (results.llf / results.llnull)
print(f"Manual calculation: {pseudo_r2:.4f}")

print("\nInterpretation:")
print("  Unlike linear R-squared, pseudo R-squared values tend to be lower.")
print("  Values > 0.2 are often considered good fit.")
print(f"  AIC: {results.aic:.2f}")
print(f"  BIC: {results.bic:.2f}")
```

### Likelihood Ratio Test

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

# Fit null model (intercept only) and full model
np.random.seed(42)
n = 500
data = pd.DataFrame({
    'tenure': np.random.uniform(0, 72, n),
    'monthly_charges': np.random.uniform(20, 100, n),
    'support_calls': np.random.poisson(2, n)
})
log_odds = (-2 - 0.05 * data['tenure'] + 0.03 * data['monthly_charges'] +
            0.3 * data['support_calls'])
data['churn'] = np.random.binomial(1, 1 / (1 + np.exp(-log_odds)))

X = sm.add_constant(data[['tenure', 'monthly_charges', 'support_calls']])
y = data['churn']

full_model = sm.Logit(y, X).fit(disp=0)
null_model = sm.Logit(y, sm.add_constant(np.ones(len(y)))).fit(disp=0)

# Likelihood ratio test
lr_stat = -2 * (null_model.llf - full_model.llf)
df = len(full_model.params) - 1  # Difference in parameters
p_value = 1 - stats.chi2.cdf(lr_stat, df)

print("Likelihood Ratio Test")
print("=" * 50)
print(f"\nH0: All coefficients = 0 (null model is sufficient)")
print(f"H1: At least one coefficient != 0")
print(f"\nLR Statistic: {lr_stat:.4f}")
print(f"Degrees of freedom: {df}")
print(f"P-value: {p_value:.6f}")

if p_value < 0.05:
    print("\nConclusion: Reject H0. The model with predictors fits")
    print("significantly better than the null model.")
```

## Multiclass Logistic Regression

### Multinomial Logistic Regression

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Create multiclass data
np.random.seed(42)
n = 600

data = pd.DataFrame({
    'income': np.random.uniform(20000, 150000, n),
    'age': np.random.uniform(18, 70, n),
    'education_years': np.random.randint(10, 22, n)
})

# Generate 3-class outcome (Low, Medium, High risk)
score = (0.5 * (data['income'] - 85000) / 40000 -
         0.3 * (data['age'] - 44) / 15 +
         0.2 * (data['education_years'] - 16) / 3 +
         np.random.normal(0, 0.5, n))

data['risk_category'] = pd.cut(score,
                               bins=[-np.inf, -0.3, 0.3, np.inf],
                               labels=['High', 'Medium', 'Low'])

# Fit multinomial logistic regression
X = data[['income', 'age', 'education_years']]
y = data['risk_category']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(multi_class='multinomial', max_iter=1000, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Multinomial Logistic Regression")
print("=" * 55)
print(f"\nClasses: {model.classes_}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
```

## Real-World Application

### Credit Default Prediction

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

# Create credit data
np.random.seed(42)
n = 1000

data = pd.DataFrame({
    'income': np.random.lognormal(10.5, 0.5, n),
    'debt_ratio': np.random.uniform(0, 1, n),
    'credit_history_years': np.random.uniform(0, 30, n),
    'num_credit_lines': np.random.poisson(5, n),
    'late_payments': np.random.poisson(1, n),
    'employment_years': np.random.uniform(0, 40, n)
})

# Generate default probability
log_odds = (-3
            - 0.00001 * data['income']
            + 2 * data['debt_ratio']
            - 0.1 * data['credit_history_years']
            + 0.1 * data['num_credit_lines']
            + 0.5 * data['late_payments']
            - 0.05 * data['employment_years'])

prob_default = 1 / (1 + np.exp(-log_odds))
data['default'] = np.random.binomial(1, prob_default)

# Train-test split
feature_cols = ['income', 'debt_ratio', 'credit_history_years',
                'num_credit_lines', 'late_payments', 'employment_years']
X = data[feature_cols]
y = data['default']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit model with statsmodels for detailed output
X_train_const = sm.add_constant(X_train)
X_test_const = sm.add_constant(X_test)

model = sm.Logit(y_train, X_train_const).fit(disp=0)

print("Credit Default Prediction Model")
print("=" * 70)
print(model.summary())

# Predictions and evaluation
y_prob = model.predict(X_test_const)
y_pred = (y_prob >= 0.5).astype(int)

print("\n\nModel Performance on Test Set:")
print("=" * 50)
print(f"AUC-ROC: {roc_auc_score(y_test, y_prob):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Odds ratios interpretation
print("\nOdds Ratios and Interpretation:")
print("=" * 60)
odds_ratios = np.exp(model.params)

for var in model.params.index:
    if var == 'const':
        continue
    or_val = odds_ratios[var]
    coef = model.params[var]

    print(f"\n{var}:")
    print(f"  Odds Ratio: {or_val:.4f}")
    if or_val > 1:
        print(f"  Effect: Increases default odds by {(or_val-1)*100:.1f}% per unit increase")
    else:
        print(f"  Effect: Decreases default odds by {(1-or_val)*100:.1f}% per unit increase")
```

## Summary

### Key Concepts

| Concept | Description |
|---------|-------------|
| Log-odds (logit) | $\log(p/(1-p))$ - the quantity being modeled |
| Odds ratio | $e^\beta$ - multiplicative effect on odds |
| Sigmoid function | Converts log-odds to probability |
| AUC-ROC | Model's discriminative ability (0.5 = random, 1 = perfect) |
| Threshold | Cutoff for converting probability to class prediction |

### Comparison of Metrics

| Metric | Focus | When to Prioritize |
|--------|-------|-------------------|
| Accuracy | Overall correctness | Balanced classes |
| Precision | Avoiding false positives | False alarms are costly |
| Recall | Catching positives | Missing positives is costly |
| F1 | Balance precision/recall | Trade-off needed |
| AUC | Overall discrimination | Comparing models |

### Best Practices

1. **Check class balance** - highly imbalanced classes require special handling
2. **Evaluate on test set** - avoid overfitting by using held-out data
3. **Choose threshold carefully** - 0.5 may not be optimal
4. **Report odds ratios** with confidence intervals for interpretation
5. **Consider calibration** - do predicted probabilities match actual rates?
6. **Compare to baseline** - is your model better than simple rules?
