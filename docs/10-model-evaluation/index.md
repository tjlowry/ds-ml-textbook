# Model Evaluation

## Overview

Every other chapter in this book fits a model. This one asks the harder question: **how do I
know it's any good, and did I measure that honestly?** Model evaluation is where a project
either earns trust or quietly lies to itself — and the difference is usually not the model,
it's the metric and the split.

I think of evaluation as three decisions:

1. **Pick a metric that matches the task and the cost of being wrong.** Regression, forecasting,
   and classification each have their own vocabulary, and within each there are metrics that
   flatter the wrong model if you choose carelessly (accuracy on imbalanced classes, MAPE on
   intermittent demand, RMSE when big misses aren't actually the expensive ones).
2. **Score on data the model never saw** — and never on the data you tuned on. A held-out test
   set is only honest if nothing about it leaked backwards into training.
3. **Assume the number is wrong until you've ruled out leakage.** A test score that looks too
   good usually is. The single most common cause of "great in the notebook, useless in
   production" is that the evaluation was contaminated.

This is a **synthesis chapter** — the metric derivations already live elsewhere in the book,
so instead of re-deriving them I point to where they are and add the layer those pages don't
have: real code computing and *reading* these metrics on my own coursework and project data.

## How this chapter is organized

| Page | What it covers | Where the theory lives |
|---|---|---|
| [Regression & Forecast Metrics](regression-and-forecast-metrics.md) | MAE / RMSE / R² / adjusted R² for plain regression; pointer to the full forecast-metric derivations | [ch09 metrics](../09-time-series-forecasting/evaluation/metrics.md) |
| [Classification Metrics](classification-metrics.md) | Confusion matrix, precision / recall / F1, on real classifiers | [ch03 logistic](../03-statistics/regression/logistic.md) |
| [ROC & AUC](roc-auc.md) | Threshold-free discrimination and how to read the curve | [ch03 logistic](../03-statistics/regression/logistic.md) |
| [Cross-Validation & Splitting](cross-validation-and-splitting.md) | Train/test/val discipline and grid-of-alphas CV | [ch08 overview](../08-machine-learning/fundamentals/overview.md) |
| [Leakage Patterns](leakage-patterns.md) | The signature failure mode — every way evaluation quietly cheats | this chapter |

## The through-line: choosing the metric before you compare

The one habit that ties every page together is picking the metric **before** looking at the
results, because the metric decides the winner. In my
[distribution demand-forecasting work](../09-time-series-forecasting/index.md) the switch from
MAPE to MASE changed which model looked best; in the fish-classification example on the next
pages, accuracy alone would have hidden the one high-value fish the model missed. The metric is
not a formality you report at the end — it's the experiment's definition of success, and it
belongs at the top.

## Notebooks

- [Classification Metrics Demo](notebooks/classification-metrics-demo.ipynb) — logistic
  regression on the public Fish Market dataset, computing a confusion matrix, ROC curve, and
  odds ratios end to end. Rebuilt from my STAT 650 final project.

## Source Materials

This chapter is built from:

- **STAT 650 final project (TAMU)** — a multi-model analysis of the public Kaggle Fish Market
  dataset: regularized regression model comparison (`RidgeCV`/`ElasticNetCV`) and a logistic-
  regression classifier with a full confusion-matrix / ROC / odds-ratio workup. My own code and
  outputs.
- **ECEN 758 HW 3 (TAMU)** — a Gaussian Naive Bayes vs kNN side-by-side comparison scored with
  `classification_report`, cross-linked from the [ch08 classification pages](../08-machine-learning/classification/knn.md).
- **Cross-chapter synthesis** — forecast metrics and the leakage stories already published in
  [ch09](../09-time-series-forecasting/index.md), and the metric definitions in
  [ch03](../03-statistics/regression/logistic.md) and
  [ch08](../08-machine-learning/fundamentals/overview.md).
