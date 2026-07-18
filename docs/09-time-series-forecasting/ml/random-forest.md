# Random Forest for Forecasting

## Overview

Random Forest builds multiple decision trees independently using random subsets of data and features, then averages their predictions. For time series, it treats forecasting as a regression problem using engineered temporal features.

## How Random Forest Works

1. **Bootstrap sampling**: Create multiple random samples from training data (with replacement)
2. **Random feature selection**: At each split, consider only a random subset of features
3. **Build trees**: Train a decision tree on each bootstrap sample
4. **Aggregate**: Average predictions from all trees (reduces variance)

## Key Advantages for Time Series

- **Handles non-linear patterns** without explicit specification
- **Robust to outliers** and noise in the data
- **Less prone to overfitting** than single decision trees
- **Feature importance** analysis built-in
- **No stationarity assumption** required
- **Handles structural breaks** or regime changes well

## Implementation

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit

# Prepare features (see Feature Engineering chapter)
X = df[feature_columns]
y = df[target_column]

# Time-based split
train_size = int(len(df) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Create and train model
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    max_features='sqrt',
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)
```

## Key Hyperparameters

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `n_estimators` | Number of trees | 100-500 |
| `max_depth` | Maximum tree depth | 5-30 or None |
| `min_samples_split` | Min samples to split a node | 2-10 |
| `min_samples_leaf` | Min samples in a leaf | 1-5 |
| `max_features` | Features considered per split | 'sqrt', 'log2', 0.5-1.0 |
| `bootstrap` | Whether to use bootstrap samples | True (usually) |

## Hyperparameter Tuning

```python
from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV

# Time series cross-validation
tscv = TimeSeriesSplit(n_splits=5)

# Parameter distributions
param_distributions = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2', 0.5]
}

# Random search with time series CV
random_search = RandomizedSearchCV(
    RandomForestRegressor(random_state=42),
    param_distributions,
    n_iter=50,
    cv=tscv,
    scoring='neg_mean_absolute_error',
    n_jobs=-1,
    random_state=42
)

random_search.fit(X_train, y_train)
print(f"Best parameters: {random_search.best_params_}")
```

## Feature Importance

```python
import matplotlib.pyplot as plt
import pandas as pd

# Get feature importance
importance = model.feature_importances_
feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': importance
}).sort_values('importance', ascending=False)

# Plot
plt.figure(figsize=(10, 8))
plt.barh(feature_importance['feature'][:20], feature_importance['importance'][:20])
plt.xlabel('Importance (Mean Decrease in Impurity)')
plt.title('Top 20 Feature Importances')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
```

### Permutation Importance

More reliable than default importance for correlated features:

```python
from sklearn.inspection import permutation_importance

perm_importance = permutation_importance(
    model, X_test, y_test,
    n_repeats=10,
    random_state=42
)

# Results
perm_importance_df = pd.DataFrame({
    'feature': feature_columns,
    'importance': perm_importance.importances_mean,
    'std': perm_importance.importances_std
}).sort_values('importance', ascending=False)
```

## When Random Forest Excels

- Data contains **outliers or significant noise**
- You need a **robust model** less prone to overfitting
- **Multiple predictor variables** are available
- **Feature importance analysis** is needed
- The time series has **structural breaks** or regime changes

**Example**: Stock price prediction with multiple technical indicators—Random Forest can identify which indicators matter most while remaining robust to noisy data.

## Comparison: Random Forest vs XGBoost

| Aspect | Random Forest | XGBoost |
|--------|--------------|---------|
| Training | Parallel (trees independent) | Sequential (trees depend on previous) |
| Overfitting | Less prone | More prone without tuning |
| Performance | Good baseline | Often slightly better |
| Speed | Faster training | Faster prediction |
| Hyperparameters | Fewer to tune | More to tune |
| Missing values | Requires handling | Handles natively |

## Ensemble with Statistical Methods

Combine Random Forest with statistical forecasts:

```python
# Assuming you have predictions from multiple models
def ensemble_predictions(rf_pred, arima_pred, weights=[0.6, 0.4]):
    """Weighted ensemble of predictions."""
    return weights[0] * rf_pred + weights[1] * arima_pred

# Or use predictions as features
ensemble_features = pd.DataFrame({
    'rf_pred': rf_predictions,
    'arima_pred': arima_predictions,
    'actual': y_test
})

# Train a meta-model
meta_model = RandomForestRegressor(n_estimators=50)
meta_model.fit(ensemble_features[['rf_pred', 'arima_pred']], ensemble_features['actual'])
```

## Out-of-Bag (OOB) Error

Random Forest provides a built-in validation estimate:

```python
model = RandomForestRegressor(
    n_estimators=100,
    oob_score=True,  # Enable OOB scoring
    random_state=42
)
model.fit(X_train, y_train)

print(f"OOB R² Score: {model.oob_score_:.4f}")
```

OOB error uses samples not included in each tree's bootstrap sample for validation—a free estimate of generalization performance.

## Practical Tips

1. **More trees rarely hurt**: Higher `n_estimators` improves stability (diminishing returns after ~200)
2. **Control tree depth**: Deeper trees risk overfitting on time series
3. **Use time-based CV**: Never randomly shuffle time series data
4. **Feature engineering matters**: Random Forest performance depends on good lag and rolling features
5. **Consider computation**: Random Forest can be memory-intensive with many features/samples

## In my projects (honest note)

I did **not** actually build a Random Forest forecaster in either project — so there's no real snippet to show here, and I'm not going to invent one.

- The senior project's plan (`course-files/09-time-series-forecasting/time-series-forecasting/docs/outline.md`) listed Random Forest as a candidate method, and `docs/model_info.md` describes when RF excels, but the only tree-ensemble model that got *implemented* was XGBoost (`run_xgboost`). See the [XGBoost page](xgboost.md).
- My distribution demand-forecasting production system uses gradient-boosted trees (**LightGBM**), not Random Forest, as its primary ML model. The two are close cousins (both tree ensembles), but the production choice was boosting, not bagging.

Everything above the fold on this page is standard RF theory and the sklearn API — correct and useful, just not something I have project code behind. If you want the tree-model code I actually wrote, it's on the [XGBoost page](xgboost.md) (school project) and in the [Feature Engineering notebook](../notebooks/distribution-feature-engineering-demo.ipynb) context (production).

## Gotchas

- **RF vs boosting is a real fork, not a synonym.** When I reached for a tree ensemble, I chose boosting (XGBoost / LightGBM) both times because it edged out on accuracy for these demand series. RF's advantage is robustness/less tuning, not top-line accuracy here.
- **Never random-split a time series for RF.** The same rule as every other model: time-based split only. RF's OOB score is *not* a valid time-series validation estimate because bootstrap sampling shuffles time order.
