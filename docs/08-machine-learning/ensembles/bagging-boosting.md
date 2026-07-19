# Bagging & Boosting

## Overview

Ensembles combine many weak-ish models into one strong one, and there are two dominant
strategies:

- **Bagging (bootstrap aggregating)** trains models *in parallel* on bootstrap samples and
  averages them. It reduces **variance**. The [random forest](../classification/random-forests.md)
  is bagging applied to decision trees.
- **Boosting** trains models *sequentially*, each one focusing on the errors of the last,
  then adds them with learned weights. It reduces **bias** (and variance). Gradient boosting
  — and its fast implementations like [XGBoost](xgboost.md) and Spark's `GBTRegressor` — is
  the dominant tabular method.

For tabular problems these are almost always my strongest baseline, ahead of a single tree
or a linear model.

The contrast is really about *how* the weak learners are wired together. Bagging trains them
**in parallel** on independent bootstrap resamples and combines them by an equal vote;
boosting trains them **sequentially**, each new model fit on what the previous ones still got
wrong — the arrows literally carry the residuals forward.

![Two-panel schematic. Left, bagging: one training set is bootstrap-resampled into three
independent samples, each grows a tree in parallel, and the trees are combined by an averaged
majority vote (reduces variance). Right, boosting: models are trained in sequence, each one
fed the previous model's residuals / reweighted errors, and combined as a weighted sum
(reduces bias).](../img/bagging-boosting.png)

## How I did it

My clearest side-by-side ensemble project is a **PySpark** model predicting fast-food
median spend per census tract (a BYU-Idaho-area capstone). It trains gradient-boosted trees,
random forests, and XGBoost and compares them:

```python
from pyspark.ml.regression import GBTRegressor, RandomForestRegressor
from pyspark.ml import Pipeline

def train_gbt_model(target_column):
    gbt = GBTRegressor(featuresCol="features", labelCol=target_column,
                       maxDepth=8, maxBins=128, lossType="squared", seed=42)
    pipeline = Pipeline(stages=indexers + encoders + [assembler, gbt])
    return pipeline.fit(train_data)
```

Source: `course-files/08-machine-learning/swampdonkey_ml_model.ipynb` (PySpark; BYU-Idaho
capstone). *Note: this notebook depends on Databricks tables, so it's a worked case study,
not a re-runnable file.*

The Spark `Pipeline` here is the important pattern: string-index and one-hot the categorical
columns, assemble everything into a single `features` vector, then hand it to the ensemble —
all as one fit/transform object so training and serving apply identical preprocessing.

The boosting side gets its own full treatment, with hyperparameter search and interpretation,
on the [XGBoost page](xgboost.md).

## Gotchas

- **Bagging vs boosting is a bias/variance choice.** Overfitting a single tree? Bag it
  (forest). Underfitting? Boost it. They fix opposite problems.
- **Boosting can overfit; bagging basically won't.** Because boosting keeps chasing
  residuals, too many rounds memorizes noise — you need early stopping / a learning rate.
  Forests just plateau.
- **One `Pipeline`, not two code paths.** Doing the encoding inside the Spark/sklearn
  pipeline (rather than separately on train and test) is what prevents train/serve skew.
- **`maxBins` must cover your categoricals.** Spark's tree learners bin features; a
  high-cardinality categorical needs `maxBins` at least as large as its number of
  categories or the fit errors out.
