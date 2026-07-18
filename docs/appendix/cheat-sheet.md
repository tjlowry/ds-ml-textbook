# Cheat Sheet

A compact, skim-before-an-exam-or-interview reference: the formulas and decision rules
scattered across the chapters, pulled onto one page. Every entry links back to the chapter
that derives it — this page is the *index of formulas and choices*, not the explanation.
For plain-language definitions of terms, see the [Glossary](glossary.md).

*Compiled from published chapter content plus my own condensed ECEN 758 study sheets
(local: `course-files/appendix/Homework/ecen758_hw/ECEN758 Final review.pdf` and
`Midterm review cheat sheet.pdf` — my own hand-made review notes; formulas re-typeset here).*

---

## Linear algebra essentials

| Fact | Formula | Where |
|---|---|---|
| Eigenvector / eigenvalue | $A\mathbf{v} = \lambda\mathbf{v}$ — a direction $A$ only scales | [Eigenvalues](../02-linear-algebra/eigenvalues-eigenvectors.md) |
| Diagonalization | $A = PDP^{-1}$, so $A^{k} = PD^{k}P^{-1}$ (largest $\lambda$ dominates iterations) | [Eigenvalues](../02-linear-algebra/eigenvalues-eigenvectors.md) |
| Power-method convergence | error shrinks by $\lvert\lambda_2/\lambda_1\rvert$ per step; close eigenvalues → slow | [Eigenvalues](../02-linear-algebra/eigenvalues-eigenvectors.md) |
| SVD | $A = U\Sigma V^{\top}$; exists for **any** matrix; $\sigma_1 \ge \sigma_2 \ge \dots \ge 0$ | [SVD](../02-linear-algebra/svd.md) |
| Singular ↔ eigen | $\sigma_i = \sqrt{\lambda_i(A^{\top}A)}$; $V$ = eigenvectors of $A^{\top}A$ (symmetric PSD, so $\lambda \ge 0$) | [SVD](../02-linear-algebra/svd.md) |
| Rank | number of nonzero singular values | [SVD](../02-linear-algebra/svd.md) |
| Best rank-$r$ approx (Eckart–Young) | keep top $r$ singular values; basis of PCA, LoRA, compression | [SVD](../02-linear-algebra/svd.md) |
| Rank theorem | $\operatorname{rank}A + \dim\operatorname{Nul}A = n$ | [Theorem reference](../02-linear-algebra/theorem-reference.md) |
| Orthogonal projection | $\operatorname{proj}_W \mathbf{y} = UU^{\top}\mathbf{y}$ ($U$ orthonormal basis of $W$); closest point in $W$ | [Theorem reference](../02-linear-algebra/theorem-reference.md) |
| Normal equations | $A^{\top}A\,\hat{\mathbf{x}} = A^{\top}\mathbf{b}\Rightarrow \hat{\mathbf{x}} = (A^{\top}A)^{-1}A^{\top}\mathbf{b}$ | [Least squares](../02-linear-algebra/least-squares.md) |
| Solve stably via QR | $\hat{\mathbf{x}} = R^{-1}Q^{\top}\mathbf{b}$ — **don't form $A^{\top}A$**, it squares the condition number ($\kappa(A^{\top}A)=\kappa(A)^2$) | [Least squares](../02-linear-algebra/least-squares.md) |
| Cauchy–Schwarz / triangle | $\lvert\langle u,v\rangle\rvert \le \lVert u\rVert\,\lVert v\rVert$; $\lVert u+v\rVert \le \lVert u\rVert + \lVert v\rVert$ | [Theorem reference](../02-linear-algebra/theorem-reference.md) |
| Gradient-descent step | $\mathbf{x}_{k+1} = \mathbf{x}_k - \alpha\,\nabla f(\mathbf{x}_k)$ | [Gradient descent](../02-linear-algebra/gradient-descent.md) |
| Markov steady state | regular stochastic $P$ has unique $\mathbf{q}$ with $P\mathbf{q}=\mathbf{q}$; any $\mathbf{x}_0$ converges to it | [Theorem reference](../02-linear-algebra/theorem-reference.md) |

**Invertible Matrix Theorem (square $A$, all true or all false):** invertible ⟺ $n$ pivots ⟺
columns independent & span $\mathbb{R}^n$ ⟺ $A\mathbf{x}=\mathbf{0}$ only trivially ⟺
$\det A \ne 0$ ⟺ $0$ is not an eigenvalue. See [Theorem reference](../02-linear-algebra/theorem-reference.md).

---

## Probability & statistics

Only what [Chapter 3](../03-statistics/index.md) actually covers.

| Rule | Formula | Where |
|---|---|---|
| Complement | $P(A^{c}) = 1 - P(A)$ | [Fundamentals](../03-statistics/probability/fundamentals.md) |
| Addition | $P(A\cup B) = P(A)+P(B)-P(A\cap B)$ | [Fundamentals](../03-statistics/probability/fundamentals.md) |
| Multiplication | $P(A\cap B) = P(A)\,P(B\mid A)$ | [Fundamentals](../03-statistics/probability/fundamentals.md) |
| Independence | $P(A\cap B) = P(A)\,P(B)$ | [Fundamentals](../03-statistics/probability/fundamentals.md) |
| Conditional | $P(A\mid B) = \dfrac{P(A\cap B)}{P(B)}$ | [Fundamentals](../03-statistics/probability/fundamentals.md) |
| Bayes | $P(A\mid B) = \dfrac{P(B\mid A)\,P(A)}{P(B)}$ (posterior ∝ likelihood × prior) | [Bayes](../03-statistics/probability/bayes.md) |

**Descriptive:** mean $\mu = \frac1N\sum x_i$; population variance $\sigma^2 = \frac1N\sum(x_i-\mu)^2$;
sample variance $s^2 = \frac{1}{n-1}\sum(x_i-\bar x)^2$ (the $n-1$ corrects estimation bias);
$\text{IQR}=Q_3-Q_1$, outlier fences at $Q_1-1.5\,\text{IQR}$ / $Q_3+1.5\,\text{IQR}$.
See [Central tendency](../03-statistics/descriptive/central-tendency.md) · [Spread](../03-statistics/descriptive/spread.md).

**Distributions** ([Distributions](../03-statistics/descriptive/distributions.md)):

| Name | Density / mass |
|---|---|
| Normal | $f(x)=\dfrac{1}{\sigma\sqrt{2\pi}}\,e^{-\frac{(x-\mu)^2}{2\sigma^2}}$ |
| Binomial | $P(X=k)=\binom{n}{k}p^{k}(1-p)^{n-k}$ |
| Poisson | $P(X=k)=\dfrac{\lambda^{k}e^{-\lambda}}{k!}$ |
| Exponential | $f(x)=\lambda e^{-\lambda x},\; x\ge 0$ |
| Uniform | $f(x)=\dfrac{1}{b-a},\; a\le x\le b$ |

---

## Regression & regularization

| Item | Formula | Where |
|---|---|---|
| OLS slope (simple) | $\hat\beta_1 = \dfrac{S_{XY}}{S_{XX}} = \dfrac{\sum(X_i-\bar X)(Y_i-\bar Y)}{\sum(X_i-\bar X)^2}$ | [Simple linear](../03-statistics/regression/simple-linear.md) |
| OLS (matrix form) | $\hat{\boldsymbol\beta} = (X^{\top}X)^{-1}X^{\top}Y$ | [Multiple linear](../03-statistics/regression/multiple-linear.md) |
| $R^2$ | $R^2 = 1 - \dfrac{SS_{\text{res}}}{SS_{\text{tot}}} = 1 - \dfrac{\sum(Y_i-\hat Y_i)^2}{\sum(Y_i-\bar Y)^2}$ | [Simple linear](../03-statistics/regression/simple-linear.md) |
| Logistic (sigmoid) | $p = \dfrac{1}{1+e^{-(\beta_0+\beta_1X_1+\dots)}}$; logit $\log\frac{p}{1-p}=\beta_0+\sum\beta_jX_j$ | [Logistic](../03-statistics/regression/logistic.md) |
| Odds ratio | one-unit rise in $X_j$ multiplies odds by $e^{\beta_j}$ | [Logistic](../03-statistics/regression/logistic.md) |
| Ridge (L2) | $\min_\beta \lVert Y-X\beta\rVert_2^2 + \lambda\lVert\beta\rVert_2^2$ — shrinks toward 0, keeps all features, good for correlated predictors, makes $X^\top X$ invertible | [Convex optimization](../02-linear-algebra/convex-optimization.md) |
| Lasso (L1) | $\min_\beta \lVert Y-X\beta\rVert_2^2 + \lambda\lVert\beta\rVert_1$ — drives coefficients to exactly 0 (feature selection) | [Compressed sensing](../02-linear-algebra/compressed-sensing.md) |

Larger $\lambda$ → smaller weights, simpler model, higher training error, better generalization
(the bias–variance knob); $\lambda=0$ recovers ordinary least squares. Ridge/Lasso objectives
re-typeset from my ECEN 758 review sheet.

---

## Classification metrics

Confusion matrix at one threshold → TN, FP, FN, TP. Derived on [Logistic Regression → Model
evaluation](../03-statistics/regression/logistic.md#model-evaluation); applied on
[Classification Metrics](../10-model-evaluation/classification-metrics.md).

| Metric | Formula | Reads as |
|---|---|---|
| Accuracy | $\dfrac{TP+TN}{N}$ | fraction correct — trap on imbalanced classes |
| Precision | $\dfrac{TP}{TP+FP}$ | of predicted positives, how many were right (punishes false alarms) |
| Recall / TPR / sensitivity | $\dfrac{TP}{TP+FN}$ | of actual positives, how many were caught (punishes misses) |
| F1 | $2\cdot\dfrac{P\cdot R}{P+R}$ | harmonic mean of precision & recall |
| FPR | $\dfrac{FP}{FP+TN}$ | the ROC x-axis |

**ROC / AUC** ([ROC & AUC](../10-model-evaluation/roc-auc.md)): sweep every threshold, plot TPR vs
FPR. AUC = probability a random positive outranks a random negative. $0.5$ = coin flip, $1.0$ =
perfect separation. Threshold-free, which is why it's the go-to for comparing classifiers.

---

## Forecast metrics

All derived in [Time-Series → Metrics](../09-time-series-forecasting/evaluation/metrics.md).
$n$ points, actual $y$, forecast $\hat y$.

| Metric | Formula | Notes |
|---|---|---|
| MAE | $\frac1n\sum\lvert y-\hat y\rvert$ | same units, robust to outliers |
| MSE | $\frac1n\sum(y-\hat y)^2$ | squared units, very outlier-sensitive |
| RMSE | $\sqrt{\frac1n\sum(y-\hat y)^2}$ | same units, penalizes big errors |
| MAPE | $\frac{100}{n}\sum\frac{\lvert y-\hat y\rvert}{\lvert y\rvert}$ | **undefined at $y=0$** — dies on intermittent demand |
| sMAPE | $\frac{100}{n}\sum\frac{\lvert y-\hat y\rvert}{(\lvert y\rvert+\lvert\hat y\rvert)/2}$ | symmetric version of MAPE |
| MASE | $\dfrac{\frac1n\sum\lvert y-\hat y\rvert}{\text{MAE of in-sample seasonal-naïve}}$ | scale-free; $<1$ beats naïve, $<0.8$ good; the headline metric for distribution demand forecasting |

Always ship a baseline — "beat seasonal naïve" is the bar, and MASE bakes that comparison in.

---

## Model / algorithm chooser

One-line "reach for X when Y." Follow the link for the full treatment.

| Reach for | When | Where |
|---|---|---|
| Linear / logistic regression | interpretable baseline, roughly linear signal, want coefficients you can explain | [Regression](../03-statistics/regression/simple-linear.md) · [Logistic](../03-statistics/regression/logistic.md) |
| k-NN | small data, non-linear boundary, no training budget; lazy and distance-based | [kNN](../08-machine-learning/classification/knn.md) |
| Naïve Bayes | high-dimensional counts (text), fast, features roughly conditionally independent | [Naïve Bayes](../08-machine-learning/classification/naive-bayes.md) |
| Decision tree | need a human-readable rule set; tolerate some overfitting | [Decision trees](../08-machine-learning/classification/decision-trees.md) |
| Random forest | strong tabular default, low tuning, handles mixed features & non-linearity | [Random forests](../08-machine-learning/classification/random-forests.md) |
| Gradient boosting / XGBoost | you want top tabular accuracy and will tune; sequential error-correction | [XGBoost](../08-machine-learning/ensembles/xgboost.md) · [Bagging vs boosting](../08-machine-learning/ensembles/bagging-boosting.md) |
| SVM | clear margin, medium data, kernels for non-linearity; only support vectors matter | [SVM](../08-machine-learning/classification/svm.md) |
| k-means | fast partitioning, roughly spherical clusters, you know $k$ | [k-means](../08-machine-learning/clustering/kmeans.md) |
| Hierarchical clustering | want a dendrogram / nested structure, don't know $k$ up front | [Hierarchical](../08-machine-learning/clustering/hierarchical.md) |
| DBSCAN / density | arbitrary-shaped clusters, need noise/outlier handling, no $k$ | [Density clustering](../08-machine-learning/clustering/density-clustering.md) |
| GMM / EM | soft (probabilistic) cluster assignment, elliptical clusters | [GMM & EM](../08-machine-learning/clustering/gmm-em.md) |
| PCA | reduce dimensions / decorrelate before modeling or plotting | [PCA](../08-machine-learning/dimensionality-reduction/pca.md) |
| CNN | grid-structured input (images); parameter sharing, translation equivariance | [CNNs](../08-machine-learning/deep-learning/cnns.md) |
| Transformer / attention | sequences with long-range dependencies; every token attends to every token | [Transformers](../08-machine-learning/deep-learning/transformers-attention.md) |
| ARIMA / SARIMA | single series, statistical baseline, clear autocorrelation (+ seasonality) | [ARIMA](../09-time-series-forecasting/statistical/arima.md) · [SARIMA](../09-time-series-forecasting/statistical/sarima.md) |
| ETS | trend + seasonality via exponential smoothing, few parameters | [ETS](../09-time-series-forecasting/statistical/ets.md) |
| Tree ensemble for forecasting | many series, rich engineered lag/calendar features, non-linear | [Forecasting with XGBoost](../09-time-series-forecasting/ml/xgboost.md) |
| PINN | solve/close a differential equation with a network; physics as the loss | [PINNs](../12-scientific-ml/pinns.md) |

---

## PageRank & recommender formulas

Formulas re-typeset from my own ECEN 758 review sheet (local:
`course-files/appendix/Homework/ecen758_hw/ECEN758 Final review.pdf`); concepts on
[PageRank](../08-machine-learning/other/pagerank.md) and
[Recommenders](../08-machine-learning/other/recommenders.md).

**PageRank**

| Item | Formula |
|---|---|
| Stochastic adjacency | $M(j,i) = 1/d_i$ if $i$ links to $j$ ($d_i$ = out-degree; column-stochastic) |
| Stationary distribution | $\mathbf{v} = M\mathbf{v}$ — the eigenvector with $\lambda = 1$ |
| Power iteration | $\mathbf{v}_{t+1} = M\mathbf{v}_t$ |
| With taxation (damping) | $\mathbf{v}' = \beta M\mathbf{v} + (1-\beta)\,\mathbf{e}/n,\quad \beta \in [0.8, 0.9]$ — fixes dead ends & spider traps |
| Topic-sensitive | $\mathbf{v}' = \beta M\mathbf{v} + (1-\beta)\,\mathbf{e}_S/\lvert S\rvert$ — teleport into topic set $S$ |

**Recommenders**

| Item | Formula |
|---|---|
| Content-based match | $\cos(x,i) = \dfrac{x\cdot i}{\lVert x\rVert\,\lVert i\rVert}$ (user profile vs item profile) |
| User–user CF | $\hat r_{xu} = \dfrac{\sum_y \operatorname{sim}(x,y)\,r_{yu}}{\sum_y \operatorname{sim}(x,y)}$ |
| Item–item CF | $\hat r_{xi} = \dfrac{\sum_j \operatorname{sim}(i,j)\,r_{xj}}{\sum_j \operatorname{sim}(i,j)}$ |
| Jaccard (binary) | $J(A,B) = \dfrac{\lvert A\cap B\rvert}{\lvert A\cup B\rvert}$ |
| Cosine (rated values) | $\dfrac{r_x\cdot r_y}{\lVert r_x\rVert\,\lVert r_y\rVert}$ |
| Latent factor (UV decomp) | $U_{n\times d}\,V_{d\times m} \approx R_{n\times m}$ — minimize RMSE over observed ratings |

Center ratings (subtract each user's mean) to fight sparsity; watch cold-start and popularity bias.

---

## PINN loss anatomy

A physics-informed net trades labels for a differential equation. For Burgers'
$u_t + u\,u_x - \nu\,u_{xx} = 0$, the loss is a sum of mean-squared terms
([PINNs](../12-scientific-ml/pinns.md)):

$$\mathcal{L} = \underbrace{\tfrac{1}{N_r}\sum_i r(x_r^i,t_r^i)^2}_{\mathcal{L}_r\ \text{physics}}
+ \underbrace{\tfrac{1}{N_0}\sum_i\big(u_\theta(x_0^i,0)-u_0^i\big)^2}_{\mathcal{L}_0\ \text{initial}}
+ \underbrace{\tfrac{1}{N_b}\sum_i u_\theta(x_b^i,t_b^i)^2}_{\mathcal{L}_b\ \text{boundary}}$$

The residual $r = u_t + u\,u_x - \nu\,u_{xx}$ is assembled from autodiff derivatives at
collocation points and should be zero everywhere the network truly solves the equation.
