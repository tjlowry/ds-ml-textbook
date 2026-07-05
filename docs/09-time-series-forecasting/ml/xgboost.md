# XGBoost for Forecasting

## Overview

XGBoost (eXtreme Gradient Boosting) is a powerful gradient boosting algorithm that has become a go-to choice for time series forecasting, often outperforming traditional statistical methods on complex datasets.

## How XGBoost Works

XGBoost builds an ensemble of decision trees sequentially:

1. **Initial prediction**: Start with a simple prediction (e.g., mean)
2. **Calculate residuals**: Find errors from current prediction
3. **Fit new tree**: Train a tree to predict the residuals
4. **Update prediction**: Add the new tree's predictions (scaled by learning rate)
5. **Repeat**: Continue until stopping criteria met

Each tree corrects errors made by previous trees, using gradient descent to minimize a loss function.

## Key Advantages for Time Series

- **Handles non-linear relationships** and complex interactions
- **Incorporates external features** beyond time (weather, events, economic indicators)
- **Robust to outliers** compared to linear methods
- **Built-in regularization** prevents overfitting
- **No stationarity requirement**—can learn from non-stationary data directly
- **Fast training** even on large datasets

## Implementation

```python
import xgboost as xgb
from sklearn.model_selection import TimeSeriesSplit

# Prepare features (see Feature Engineering chapter)
X = df[feature_columns]
y = df[target_column]

# Time-based split
train_size = int(len(df) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Create and train model
model = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    early_stopping_rounds=10,
    verbose=False
)

# Predict
predictions = model.predict(X_test)
```

## Key Hyperparameters

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `n_estimators` | Number of trees | 100-1000 |
| `max_depth` | Maximum tree depth | 3-10 |
| `learning_rate` | Step size shrinkage | 0.01-0.3 |
| `subsample` | Row sampling ratio | 0.6-1.0 |
| `colsample_bytree` | Feature sampling ratio | 0.6-1.0 |
| `min_child_weight` | Minimum leaf weight | 1-10 |
| `reg_alpha` | L1 regularization | 0-1 |
| `reg_lambda` | L2 regularization | 0-1 |

## Hyperparameter Tuning

```python
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV

# Time series cross-validation
tscv = TimeSeriesSplit(n_splits=5)

# Parameter grid
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.05, 0.1, 0.2],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

# Grid search with time series CV
grid_search = GridSearchCV(
    xgb.XGBRegressor(random_state=42),
    param_grid,
    cv=tscv,
    scoring='neg_mean_absolute_error',
    n_jobs=-1
)

grid_search.fit(X_train, y_train)
print(f"Best parameters: {grid_search.best_params_}")
```

## Feature Importance

Understanding which features drive predictions:

```python
import matplotlib.pyplot as plt

# Get feature importance
importance = model.feature_importances_
feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': importance
}).sort_values('importance', ascending=False)

# Plot top 20 features
plt.figure(figsize=(10, 8))
plt.barh(feature_importance['feature'][:20], feature_importance['importance'][:20])
plt.xlabel('Importance')
plt.title('Top 20 Feature Importances')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
```

## Multi-Step Forecasting

### Recursive Strategy
Predict one step, use prediction as input for next step:

```python
def recursive_forecast(model, last_features, steps, feature_cols):
    """Generate multi-step forecasts recursively."""
    predictions = []
    features = last_features.copy()

    for _ in range(steps):
        # Predict next value
        pred = model.predict(features[feature_cols].values.reshape(1, -1))[0]
        predictions.append(pred)

        # Update features for next prediction
        # Shift lag features and add new prediction
        features = update_features(features, pred)

    return predictions
```

### Direct Strategy
Train separate models for each horizon:

```python
def direct_forecast(X, y, horizons, feature_cols):
    """Train separate models for each forecast horizon."""
    models = {}
    for h in horizons:
        # Shift target by horizon
        y_h = y.shift(-h).dropna()
        X_h = X.iloc[:len(y_h)]

        model = xgb.XGBRegressor()
        model.fit(X_h[feature_cols], y_h)
        models[h] = model

    return models
```

## When XGBoost Excels

- **Multiple external factors** influence the forecast
- The time series has **complex non-linear patterns**
- You have a **large dataset** with many features
- The **relationships between variables change** over time
- There are **multiple seasonalities** or irregular patterns

**Example**: Energy consumption affected by weather, holidays, and economic factors.

## Practical Findings

From a comparative study on retail forecasting:

> "XGBoost consistently outperformed other models on the retail dataset, with the lowest MAE (33.67) and RMSE (47.35) using no transformation. Machine learning approaches demonstrated superior performance compared to traditional statistical methods for this data."

Key insights:
- XGBoost performed best **without** data transformations
- Achieved superior accuracy with **similar computational requirements** to SARIMA
- Proper **train-test splitting** with time-based holdout is essential

## Comparison with Statistical Methods

| Aspect | XGBoost | ARIMA/SARIMA |
|--------|---------|--------------|
| Stationarity | Not required | Required |
| External features | Easily incorporated | Requires ARIMAX |
| Non-linear patterns | Handles well | Cannot capture |
| Interpretability | Feature importance | Model coefficients |
| Prediction intervals | Requires extra work | Built-in |
| Small data | May overfit | Often better |
| Large data | Excels | Slower, may plateau |

## Tips for Success

1. **Feature engineering is key**: XGBoost's performance depends heavily on feature quality
2. **Use early stopping**: Prevents overfitting and reduces training time
3. **Time-based validation**: Never use random splits for time series
4. **Monitor overfitting**: Compare train and validation errors
5. **Consider ensemble**: Combine XGBoost with statistical methods
