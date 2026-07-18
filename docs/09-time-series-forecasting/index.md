# Time Series Forecasting

## Overview

Time series forecasting involves predicting future values based on previously observed values over time. This chapter covers both traditional statistical methods and modern machine learning approaches, along with data transformations and model evaluation techniques.

Everything here is grounded in two of my own projects that sit at opposite ends of the maturity curve:

- **The senior project (BYU-Idaho) — a model-comparison study.** A single-file pipeline that sweeps three aggregation levels (daily/weekly/monthly) x four transformations (none/log/box-cox/sqrt) x five models (Naive, Seasonal Naive, SARIMA, ETS, XGBoost) and reports which combination wins on MAE/RMSE. It is deliberately breadth-first: every classical method side by side on one retail series. Source tree: `course-files/09-time-series-forecasting/time-series-forecasting/` (`forecasting-pipeline.py`, `synthetic-data-generator.py`, `resampling-utilities.py`, `docs/takeaways.md`, `docs/model_info.md`).
- **My distribution demand-forecasting system — production.** A ~5,000-line pipeline that forecasts weekly demand for a distribution business: SBC demand-pattern classification, a leakage-tested feature layer, four models (LightGBM, ARIMA, Croston, Two-Stage) combined with an auto-tuned weighted ensemble, MASE-first evaluation, and ERP/database integration. This is where the school-project ideas grew up. Source tree: `demand-forecast/` (private distribution-forecasting repo; `src/features/`, `src/evaluation/metrics.py`, `src/ensemble/weighted.py`, `docs/technical_summary.md`).

Throughout the chapter, the "How I did it" sections show the real code and the "Gotchas" sections capture what actually went wrong or surprised me. Where a topic has a school-project version and a production version (feature engineering, metrics, ensembling), both are shown so the contrast is visible.

> **Data privacy.** The senior project was graded on a real client demand export and its scale-shifted derivatives (`retail_data.csv`, `daily_sales.csv`) — none of which are synthetic. None of that data, and none of the plots rendered from it, appear anywhere in this chapter. Every committed plot and number is regenerated from the project's own `synthetic-data-generator.py`. Real *code* is shown; real *data* is not.

## Notebooks

- [Senior Project Pipeline](notebooks/senior-project-pipeline.ipynb) — the transform -> feature -> fit -> compare loop running end to end on synthetic data.
- [Distribution Feature Engineering Demo](notebooks/distribution-feature-engineering-demo.ipynb) — the production leakage-safe lag/rolling features and SBC classification, recreated on a synthetic weekly demand panel.

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

This chapter draws on two projects:

- **Senior project (BYU-Idaho):** a forecasting-method comparison study — `course-files/09-time-series-forecasting/time-series-forecasting/`. It actually implemented Naive, Seasonal Naive, SARIMA, ETS, and XGBoost. Note: `docs/outline.md` also *planned* VAR, SVR, LSTM, Transformers, Prophet, NeuralProphet, and Random Forest, but only the five above were built — this chapter reflects what was implemented, not the wishlist.
- **Distribution demand forecasting (client):** the production pipeline — `demand-forecast/` (private distribution-forecasting repo). LightGBM + ARIMA + Croston + Two-Stage ensemble with SBC classification and leakage-tested features.
