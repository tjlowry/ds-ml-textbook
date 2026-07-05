# Time Series Forecasting

## Overview

Time series forecasting involves predicting future values based on previously observed values over time. This chapter covers both traditional statistical methods and modern machine learning approaches, along with data transformations and model evaluation techniques.

## Topics

### Fundamentals

- [Time Series Concepts](fundamentals/concepts.md) - Core terminology and components
- [Stationarity](fundamentals/stationarity.md) - Why it matters and how to test for it
- [Seasonality & Trends](fundamentals/seasonality-trends.md) - Identifying patterns in data
- [Autocorrelation (ACF/PACF)](fundamentals/autocorrelation.md) - Understanding temporal dependencies

### Statistical Methods

- [Moving Averages](statistical/moving-averages.md) - Simple smoothing techniques
- [Exponential Smoothing (ETS)](statistical/ets.md) - Error, Trend, Seasonality models
- [ARIMA](statistical/arima.md) - AutoRegressive Integrated Moving Average
- [SARIMA](statistical/sarima.md) - Seasonal ARIMA extension
- [Naive Methods](statistical/naive-methods.md) - Baseline approaches

### Machine Learning for Time Series

- [Feature Engineering for Time Series](ml/feature-engineering.md) - Creating predictive features
- [Random Forest for Forecasting](ml/random-forest.md) - Ensemble tree methods
- [XGBoost for Forecasting](ml/xgboost.md) - Gradient boosting approach

### Data Transformations

- [Log Transformation](transformations/log.md) - Handling right-skewed data
- [Square Root Transformation](transformations/sqrt.md) - Moderate skew correction
- [Box-Cox Transformation](transformations/box-cox.md) - Optimal power transformation
- [Yeo-Johnson Transformation](transformations/yeo-johnson.md) - Handling negative values
- [Differencing](transformations/differencing.md) - Achieving stationarity

### Model Evaluation & Selection

- [Evaluation Metrics](evaluation/metrics.md) - MAE, RMSE, MAPE
- [Model Comparison](evaluation/comparison.md) - Statistical vs ML approaches
- [Method Selection Framework](evaluation/selection-framework.md) - Choosing the right model

## Key Takeaways

- **No single model wins everywhere**: Model performance depends heavily on data characteristics
- **ML models can outperform statistical methods**: XGBoost often achieves superior accuracy on complex datasets
- **Transformations aren't always helpful**: Apply based on diagnostic tests, not by default
- **Baselines matter**: Always compare against naive methods to validate model value

## Source Materials

This chapter is based on a senior project comparing time series forecasting methods across retail datasets, evaluating statistical models (ARIMA, SARIMA, ETS) against machine learning approaches (XGBoost, Random Forest) with various data transformations.
