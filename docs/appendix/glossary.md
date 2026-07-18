# Glossary

A compiled index of terms defined across the chapter pages. Every entry paraphrases a
definition that already exists on the linked page — this glossary doesn't introduce new
explanations, it collects and cross-references the ones written while filling out each
chapter. Follow the link for the full derivation, code, and gotchas.

## A

**ACID** — The transaction guarantees a relational database provides: every write is
atomic, consistent, isolated, and durable. It's the trade-off non-relational stores relax
in exchange for flexibility or horizontal scale. See [Database Types](../07-sql-and-databases/database-types.md).

**ADI (Average Demand Interval)** — The mean number of periods between non-zero sales for
a given item — a measure of *how often* something sells, used alongside CV² to classify
demand patterns. See [Method Selection Framework](../09-time-series-forecasting/evaluation/selection-framework.md).

**ARIMA** — AutoRegressive Integrated Moving Average: a statistical forecasting model that
combines an autoregressive term (p lagged values), a differencing term (d, for
stationarity), and a moving-average term (q lagged forecast errors), notated ARIMA(p,d,q).
See [ARIMA](../09-time-series-forecasting/statistical/arima.md).

**Armijo (Backtracking) Line Search** — A rule for choosing a gradient-descent step size:
accept a step only if it produces "enough" decrease in the objective, shrinking the step by
a fixed factor until that condition holds, rather than guessing a fixed learning rate.
See [Gradient Descent](../02-linear-algebra/gradient-descent.md).

**Attention (Self-Attention)** — The mechanism that replaced recurrence in transformers:
every token looks at every other token and learns how much to attend to each, via
queries dotted with keys, scaled, softmaxed, and used to weight values (scaled dot-product
attention), often run in parallel across multiple heads. See [Transformers & Attention](../08-machine-learning/deep-learning/transformers-attention.md).

**Automatic Differentiation (Autodiff)** — Computing exact derivatives of a function (or
network) with respect to its inputs by mechanically applying the chain rule through the
computation graph, rather than approximating them with finite differences on a grid. It's
the same machinery backprop uses for weights, pointed instead at the inputs. See
[Discretization & Automatic Differentiation](../12-scientific-ml/discretization-and-autodiff.md).

**AUC-ROC** — A model's discriminative ability summarized as the area under the ROC curve:
0.5 means random guessing, 1.0 means perfect separation of the classes. See
[Logistic Regression](../03-statistics/regression/logistic.md).

## B

**Backpropagation** — The training algorithm for a neural network: run a forward pass,
compute a loss, then propagate gradients backward through the chain rule and take a
gradient-descent step on the weights. See [Neural Network Fundamentals](../08-machine-learning/deep-learning/neural-network-fundamentals.md).

**Bagging (Bootstrap Aggregating)** — An ensembling strategy that trains models in
parallel on bootstrap-resampled data and averages their predictions, which reduces
variance. A random forest is bagging applied to decision trees. See
[Bagging & Boosting](../08-machine-learning/ensembles/bagging-boosting.md).

**Bayes' Theorem** — The rule for updating a belief in light of new evidence: it combines
a prior probability, a likelihood of the observed evidence, and a marginal likelihood to
produce a posterior probability. See [Bayesian Probability](../03-statistics/probability/bayes.md).

**Bias-Variance Tradeoff** — The single axis every model-complexity choice sits on: a
model that's too simple underfits (high bias, both train and test error high), while a
model that memorizes training noise overfits (high variance, tiny train error, large test
error). See [ML Overview & Workflow](../08-machine-learning/fundamentals/overview.md).

**Boosting** — An ensembling strategy that trains models sequentially, each one focusing
on the errors of the previous models and combining them with learned weights, which
reduces bias (and variance). Gradient boosting and XGBoost are the dominant tabular
implementations. See [Bagging & Boosting](../08-machine-learning/ensembles/bagging-boosting.md).

**Box-Cox Transformation** — A power transformation that automatically finds the optimal
exponent to normalize a series, generalizing the log and square-root transforms into a
single framework. See [Box-Cox Transformation](../09-time-series-forecasting/transformations/box-cox.md).

## C

**Central Limit Theorem** — Regardless of the population's underlying distribution, the
sampling distribution of the sample mean approaches a normal distribution as sample size
grows. See [Probability Fundamentals](../03-statistics/probability/fundamentals.md).

**Collocation Points** — The interior sample points a physics-informed neural network is
evaluated at that carry no known target value — the only requirement is that the PDE
residual be (close to) zero there. See [How PINNs Work](../12-scientific-ml/pinns.md).

**Compressed Sensing** — Recovering a signal from far fewer measurements than classical
sampling requires, provided the signal is sparse in some basis; minimizing the (convex)
ℓ1 norm recovers the same sparse solution that the combinatorial ℓ0 norm would, under mild
conditions. See [Compressed Sensing](../02-linear-algebra/compressed-sensing.md).

**Confidence Interval** — A range of plausible values for a population parameter built
from sample data; a 95% confidence interval means that if the sampling procedure were
repeated many times, about 95% of the resulting intervals would contain the true
parameter. See [Confidence Intervals](../03-statistics/inference/confidence-intervals.md).

**Confusion Matrix** — A breakdown of a classifier's predictions into true positives, true
negatives, false positives (Type I errors), and false negatives (Type II errors), the raw
material behind precision, recall, and F1. See [Logistic Regression](../03-statistics/regression/logistic.md).

**Convexity (Convex Function / Set)** — A function is convex when the chord between any
two points on its graph never dips below the graph; on a convex objective over a convex
feasible set, every local minimum is the global minimum, so gradient descent can't get
stuck in a bad basin. See [Convex Optimization](../02-linear-algebra/convex-optimization.md).

**CV² (Squared Coefficient of Variation)** — The variance of non-zero demand quantities
relative to their mean, `(std / mean)²`; paired with ADI, it measures *how variable* the
sale amount is once a sale happens. See [Method Selection Framework](../09-time-series-forecasting/evaluation/selection-framework.md).

## D

**DBSCAN / Density-Based Clustering** — Clustering that defines clusters as connected
regions of high point density separated by sparse regions, rather than assuming spherical
clusters or requiring the number of clusters up front; points in low-density regions can be
labeled as noise. See [Density-Based Clustering](../08-machine-learning/clustering/density-clustering.md).

**Decision Tree** — A supervised model that splits the feature space with a sequence of
yes/no questions, choosing at each node the split that most reduces impurity (Gini or
entropy); the result is an interpretable flowchart, at the cost of high variance in a
single deep tree. See [Decision Trees](../08-machine-learning/classification/decision-trees.md).

**Differencing** — Subtracting each observation from the one before it (or from the same
point in the previous seasonal cycle) to remove trend or seasonality and push a series
toward stationarity. See [Differencing](../09-time-series-forecasting/transformations/differencing.md).

**Dynamic Programming (DP)** — The discipline of not solving the same subproblem twice:
when a problem's answer is built from overlapping smaller answers, each one is computed
once, stored, and reused, trading memory for an enormous reduction in recomputation. See
[Dynamic Programming](../02-linear-algebra/dynamic-programming.md).

## E

**Early Stopping** — Halting the training of a boosted-tree ensemble once performance on a
held-out validation set stops improving, so the model uses only as many trees as actually
help and doesn't overfit the training residuals. See [XGBoost](../08-machine-learning/ensembles/xgboost.md).

**Eigenvalue / Eigenvector** — An eigenvector of a matrix is a direction the matrix only
stretches or shrinks rather than rotates (`Av = λv`); the scale factor λ is its eigenvalue.
These are the natural axes of a linear map and underlie PCA, PageRank, and the power
method. See [Eigenvalues & Eigenvectors](../02-linear-algebra/eigenvalues-eigenvectors.md).

**Embedding** — A vector representation of a word, image, or user, arranged so that
geometry encodes meaning: similar things point in similar directions, and directions carry
consistent concepts (e.g. "king − man + woman ≈ queen"). See
[Linear Algebra in Machine Learning](../02-linear-algebra/linear-algebra-in-ml.md).

**ETS (Exponential Smoothing)** — A family of forecasting models, named for their three
components — Error, Trend, Seasonality — that weight recent observations more heavily than
older ones via a smoothing parameter. See [Exponential Smoothing (ETS)](../09-time-series-forecasting/statistical/ets.md).

**Expectation-Maximization (EM)** — The algorithm used to fit a Gaussian Mixture Model: it
alternates between the E-step (computing each point's responsibility for each component
given the current parameters) and the M-step (re-estimating the parameters weighted by
those responsibilities), increasing the log-likelihood each round. See
[Gaussian Mixture Models & EM](../08-machine-learning/clustering/gmm-em.md).

## F

**Feature Scaling** — Rescaling predictors (e.g. min-max squashing to [0, 1], or
standardizing to zero mean and unit variance) so that distance- and gradient-based models
aren't dominated by whichever feature happens to have the largest raw scale. See
[ML Overview & Workflow](../08-machine-learning/fundamentals/overview.md).

**Foreign Key** — A column that references another table's primary key, enforcing that the
referenced row actually exists (referential integrity) — the mechanism that ties normalized
tables back together. See [Schema Design](../07-sql-and-databases/schema-design.md).

**Frequent Itemset Mining** — Finding sets of items that co-occur often in transaction data
("market-basket analysis") and turning them into association rules, scored by support (how
often the itemset appears), confidence (how often the rule holds), and lift (how much more
than chance). See [Frequent Itemset Mining](../08-machine-learning/other/itemset-mining.md).

## G

**Gaussian Mixture Model (GMM)** — A clustering model that treats the data as generated by
a weighted sum of several Gaussians, each with its own mean, covariance, and mixing weight;
unlike k-means it gives each point a soft, probabilistic responsibility for every cluster
instead of a hard assignment. See [Gaussian Mixture Models & EM](../08-machine-learning/clustering/gmm-em.md).

**Gradient Boosting** — Building an ensemble of trees sequentially, where each new tree is
trained to predict the residual errors left by the ensemble so far, and its predictions are
added in, scaled by a learning rate. XGBoost is a fast, regularized implementation with
built-in L1/L2 regularization and early stopping. See [XGBoost](../08-machine-learning/ensembles/xgboost.md).

**Gradient Descent** — An optimization method that minimizes a function by repeatedly
stepping in the direction of steepest decrease (the negative gradient); the step size (or
learning rate) controls how far each step moves, and a poorly-conditioned objective makes
the path zig-zag. See [Gradient Descent](../02-linear-algebra/gradient-descent.md).

**Grammar of Graphics** — A theoretical framework (Wilkinson, 2005) for describing any
statistical graphic as a composition of independent components — data, transformations,
scales, coordinate system, geometric elements, guides, and facets — rather than a fixed
chart type. It's the foundation of ggplot2. See [The Grammar of Graphics](../06-data-visualization/r/grammar-of-graphics.md).

## H

**Hierarchical Clustering** — Building a tree (dendrogram) of nested clusters instead of a
flat partition; the agglomerative (bottom-up) version starts with every point as its own
cluster and repeatedly merges the two closest ones under a chosen linkage rule
(single, complete, average, or Ward), so you don't have to fix the number of clusters in
advance. See [Hierarchical Clustering](../08-machine-learning/clustering/hierarchical.md).

**Homoscedasticity** — The regression assumption that the variance of the errors stays
constant across all levels of the predictor; its violation (heteroscedasticity) is
diagnosed with a residuals-vs-fitted or scale-location plot and the Breusch-Pagan test. See
[Regression Assumptions and Diagnostics](../03-statistics/regression/assumptions.md).

**Hypothesis Testing** — A formal decision framework: state a null hypothesis (the default,
"no effect" position) and an alternative hypothesis, choose a significance level, compute a
test statistic that measures how far the sample is from what the null predicts, and reject
or fail to reject the null accordingly. See [Hypothesis Testing](../03-statistics/inference/hypothesis-testing.md).

## I

**Interquartile Range (IQR)** — The spread of the middle 50% of the data, calculated as the
75th percentile minus the 25th percentile; robust to outliers and the basis of box-plot
whiskers and fence-based outlier detection. See [Measures of Spread (Dispersion)](../03-statistics/descriptive/spread.md).

## J

**Join (Inner / Left)** — The SQL operation that stitches split-apart tables back together
on a shared key; an inner join keeps only rows that match on both sides, while a left join
keeps every row from the left table even when the right side has no match. See
[SQL Essentials](../07-sql-and-databases/sql-essentials.md).

## K

**k-Means** — The workhorse of partitional clustering: pick k, then alternate between
assigning each point to its nearest centroid and recomputing each centroid as the mean of
its members, until assignments stop changing. It assumes roughly spherical, similarly-sized
clusters. See [k-Means](../08-machine-learning/clustering/kmeans.md).

**k-Nearest Neighbors (kNN)** — A lazy, non-parametric classifier that predicts a point's
label by majority vote among its k closest training points; there is no training step
beyond storing the data, so all the work happens at prediction time. See
[k-Nearest Neighbors](../08-machine-learning/classification/knn.md).

## L

**LASSO / ℓ1 Sparsity** — Minimizing the ℓ1 norm (sum of absolute values) of a coefficient
vector drives coefficients exactly to zero, performing automatic feature selection; it's
the convex, tractable stand-in for the combinatorial ℓ0 "count the nonzeros" objective, and
the same geometry behind compressed sensing. See [Compressed Sensing](../02-linear-algebra/compressed-sensing.md).

**Least Squares** — When `Ax = b` has no exact solution, least squares finds the `x̂` that
minimizes `‖Ax − b‖²`; geometrically this is the orthogonal projection of `b` onto the
column space of `A`, and the residual sticks out perpendicular to that subspace. See
[Least Squares](../02-linear-algebra/least-squares.md).

**Log-Odds (Logit)** — The quantity a logistic regression actually models: `log(p / (1-p))`,
the natural log of the odds of the positive class, which is converted back to a probability
by the sigmoid function. See [Logistic Regression](../03-statistics/regression/logistic.md).

**Logistic Regression** — A model for a binary response that predicts the log-odds of
belonging to the positive class as a linear function of the predictors, then squashes that
through a sigmoid to get a probability between 0 and 1 — unlike linear regression, which
can predict invalid values outside [0, 1] for a binary outcome. See
[Logistic Regression](../03-statistics/regression/logistic.md).

**LoRA (Low-Rank Adaptation)** — A fine-tuning technique that freezes a large weight matrix
and learns a low-rank correction (`B` times `A`, with an inner dimension `r` much smaller
than the matrix size) instead of updating every parameter — the same "most matrices are
approximately low rank" idea behind the SVD's low-rank approximation. See
[Singular Value Decomposition](../02-linear-algebra/svd.md).

## M

**MASE (Mean Absolute Scaled Error)** — A forecast-accuracy metric that scales the mean
absolute error by the in-sample error of a seasonal-naive forecast, so it stays meaningful
even for intermittent, mostly-zero demand where MAPE breaks down; below 1.0 beats seasonal
naive, below 0.8 is genuinely good. See [Evaluation Metrics](../09-time-series-forecasting/evaluation/metrics.md).

**Multicollinearity** — When predictor variables are highly correlated with each other,
making it hard to isolate each one's individual effect on the response; diagnosed with the
Variance Inflation Factor or a correlation matrix. See
[Multiple Linear Regression](../03-statistics/regression/multiple-linear.md).

**Multiple Linear Regression** — An extension of simple linear regression to several
predictors at once, letting each partial regression coefficient represent the effect of one
predictor while holding all the others constant. See
[Multiple Linear Regression](../03-statistics/regression/multiple-linear.md).

## N

**Naive Bayes** — A classifier that applies Bayes' theorem with a strong ("naive")
assumption that every feature is conditionally independent given the class; rarely
literally true, but fast, data-efficient, and a strong baseline (the Gaussian variant
models each continuous feature as a per-class normal distribution). See
[Naive Bayes](../08-machine-learning/classification/naive-bayes.md).

**Naive Forecast / Seasonal Naive** — The simplest forecasting baselines: naive uses the
last observed value as the prediction for every future period, while seasonal naive uses
the value from the same point in the previous seasonal cycle. Any more sophisticated model
should beat these to justify its complexity. See [Naive Methods](../09-time-series-forecasting/statistical/naive-methods.md).

**Normal Distribution** — The symmetric, bell-shaped continuous distribution centered on
its mean, defined by a mean and standard deviation, and the limiting distribution the
Central Limit Theorem points toward for sample means. See
[Statistical Distributions](../03-statistics/descriptive/distributions.md).

**Normalization (Database)** — The discipline of not repeating data: instead of storing the
same value on every row that needs it, it's stored once in its own table and referenced by
key, so nothing but the key determines each non-key column (roughly, third normal form).
See [Schema Design](../07-sql-and-databases/schema-design.md).

## O

**Orthogonal Projection** — The point in a subspace closest to a given vector; the least
squares solution is exactly the orthogonal projection of the target vector onto the column
space of the predictor matrix, with the residual perpendicular to that subspace. See
[Least Squares](../02-linear-algebra/least-squares.md).

**Overfitting / Underfitting** — Two failure modes on the bias-variance axis: underfitting
(high bias) means the model is too simple to capture the signal, so train and test error
are both high; overfitting (high variance) means the model has memorized training noise, so
train error is tiny but test error is large. See [ML Overview & Workflow](../08-machine-learning/fundamentals/overview.md).

## P

**p-value** — The probability of observing results as extreme as, or more extreme than,
the data actually collected, assuming the null hypothesis is true. It measures
compatibility with the null, not the probability the null is true. See
[P-Values and Statistical Significance](../03-statistics/inference/p-values.md).

**PageRank** — An algorithm that ranks the nodes of a graph by importance, modeling a
"random surfer" who follows edges at random (with a damping factor for occasionally
teleporting); a node's PageRank is the long-run probability the surfer is there — the
stationary distribution of that walk, computed as the dominant eigenvector of the
transition matrix. See [PageRank & Graph Methods](../08-machine-learning/other/pagerank.md).

**Parameterized Query** — Passing user-supplied values into a SQL statement as placeholders
with a separate argument list, rather than string-formatting them directly into the query
text, so the driver escapes them and closes off SQL-injection. See
[Python & Databases](../07-sql-and-databases/python-and-databases.md).

**PCA (Principal Component Analysis)** — Finds the orthogonal directions of maximum
variance in the data (the eigenvectors of the covariance matrix) and re-expresses points in
that new basis; keeping only the top few components gives a lower-dimensional
representation that preserves most of the variance. See
[Principal Component Analysis](../08-machine-learning/dimensionality-reduction/pca.md).

**Perron-Frobenius Theorem** — A matrix with all-positive entries has a real, positive,
strictly-largest eigenvalue (the Perron root), whose eigenvector can be chosen all-positive
— the guarantee that makes repeated iteration on a positive system converge to a single
dominant direction, which is why PageRank converges. See
[Perron-Frobenius](../02-linear-algebra/perron-frobenius.md).

**PINN (Physics-Informed Neural Network)** — A neural network whose loss includes a PDE
residual term: instead of only matching labeled data, it's trained so that the equation's
residual is (close to) zero at sampled collocation points, alongside ordinary supervised
terms for the initial and boundary conditions. See [How PINNs Work](../12-scientific-ml/pinns.md).

**Positive Semidefinite (Hessian)** — The multivariable analog of "curves up everywhere":
a function's Hessian (matrix of second derivatives) having only non-negative eigenvalues
certifies that the function is convex, so any local minimum found is the global one. See
[Convex Optimization](../02-linear-algebra/convex-optimization.md).

## R

**Random Forest** — An ensemble of decision trees, each trained on a bootstrap sample of
the rows and a random subset of the features at each split; averaging their votes cancels
the high variance of any single tree while keeping most of the signal. See
[Random Forests](../08-machine-learning/classification/random-forests.md).

**Residual** — The gap between an observed value and a model's fitted value — what the
model could not explain. In least squares it's the perpendicular distance from the target
to its projection onto the column space; in gradient boosting, each new tree is trained to
predict the previous ensemble's residuals. See [Least Squares](../02-linear-algebra/least-squares.md).

**R-squared** — The proportion of variance in the response explained by the fitted model,
computed as one minus the ratio of residual to total sum of squares. See
[Simple Linear Regression](../03-statistics/regression/simple-linear.md).

## S

**SA-PINN (Self-Adaptive PINN)** — A physics-informed neural network where every
collocation, boundary, and initial point gets its own trainable weight; the network weights
are trained to minimize the weighted loss while the point-weights are trained to maximize
it (a saddle-point problem), so the weighting automatically concentrates on the points
where the residual is stubbornly large. See [Self-Adaptive PINNs](../12-scientific-ml/sa-pinns.md).

**SARIMA** — Seasonal ARIMA: extends ARIMA with an additional seasonal (P, D, Q, m) block
that captures repeating patterns at a fixed period, on top of the ordinary (p, d, q)
components. See [SARIMA](../09-time-series-forecasting/statistical/sarima.md).

**SBC Classification (Demand Pattern Classes)** — A rule that classifies each item's demand
history into one of four patterns — smooth, erratic, intermittent, or lumpy — based on two
statistics, ADI and CV², so that each class can be routed to the forecasting model best
suited to it (e.g. Croston's method for intermittent demand). See
[Method Selection Framework](../09-time-series-forecasting/evaluation/selection-framework.md).

**SMAPE (Symmetric Mean Absolute Percentage Error)** — A percentage forecast-error metric
that divides the absolute error by the average of the absolute actual and forecast values
(instead of just the actual), which keeps it bounded between 0% and 200% and treats
over- and under-forecasts symmetrically. See [Evaluation Metrics](../09-time-series-forecasting/evaluation/metrics.md).

**Stationarity** — A time series is stationary if its statistical properties — mean,
variance, and autocorrelation structure — stay constant over time; many statistical
forecasting methods (ARIMA, ETS) assume it, and differencing or transformation is the
usual fix when it's violated. See [Stationarity](../09-time-series-forecasting/fundamentals/stationarity.md).

**SVD (Singular Value Decomposition)** — Factors any matrix, square or not, as a rotation,
an axis-aligned stretch (the singular values), and a second rotation (`A = UΣVᵀ`); it
always exists, unlike an eigendecomposition, and underlies least squares, PCA, and low-rank
approximation. See [Singular Value Decomposition](../02-linear-algebra/svd.md).

**SVM (Support Vector Machine)** — Finds the hyperplane that separates two classes with the
maximum margin — the widest gap between the boundary and the nearest points of each class
(the support vectors); a soft margin tolerates some violations, and the kernel trick lets
the same idea carve nonlinear boundaries without explicitly computing a higher-dimensional
mapping. See [Support Vector Machines](../08-machine-learning/classification/svm.md).

## T

**Transformer** — The architecture that replaced recurrent networks with self-attention,
letting every token attend to every other token in one parallel step instead of processing
the sequence step by step; stacked attention and feed-forward blocks are the backbone of
modern language models. See [Transformers & Attention](../08-machine-learning/deep-learning/transformers-attention.md).

**Type I / Type II Error** — A Type I error rejects a true null hypothesis (a false
positive, with probability equal to the significance level α); a Type II error fails to
reject a false null hypothesis (a false negative, with probability β). Power, `1 − β`, is
the probability of correctly detecting a real effect. See
[Hypothesis Testing](../03-statistics/inference/hypothesis-testing.md).

## V

**Variance Inflation Factor (VIF)** — A diagnostic for multicollinearity: it measures how
much a predictor's coefficient variance is inflated by its correlation with the other
predictors, with values above 5 (or 10) flagging a problematic degree of collinearity. See
[Regression Assumptions and Diagnostics](../03-statistics/regression/assumptions.md).

## W

**Window Function (SQL)** — A SQL computation that runs across a set of rows related to the
current row — without collapsing them the way `GROUP BY` does — so every row is kept while
also getting an aggregate, ranking, or running total alongside it. See
[SQL Essentials](../07-sql-and-databases/sql-essentials.md).

## X

**XGBoost** — A fast, regularized implementation of gradient-boosted decision trees: it
builds trees sequentially, each fitting the residual errors of the ensemble so far, with
built-in L1/L2 regularization, row/column subsampling, and early stopping to control
overfitting. See [XGBoost](../08-machine-learning/ensembles/xgboost.md).

## Y

**Yeo-Johnson Transformation** — A power transformation similar to Box-Cox but defined for
zero and negative values as well as positive ones, making it the better default when a
series isn't strictly positive. See
[Yeo-Johnson Transformation](../09-time-series-forecasting/transformations/yeo-johnson.md).
