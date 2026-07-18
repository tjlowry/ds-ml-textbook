# Support Vector Machines

## Overview

A **Support Vector Machine (SVM)** finds the hyperplane that separates two classes with the
*maximum margin* — the widest possible gap between the boundary and the nearest points of
each class (the "support vectors"). A soft margin allows some violations for
non-separable data, and the **kernel trick** (RBF, polynomial) lets the same idea carve
nonlinear boundaries by implicitly lifting the data into a higher-dimensional space without
computing the coordinates. SVMs shine on small-to-medium, high-dimensional problems with a
clear margin.

I don't have a *from-scratch* SVM implementation, but I did work SVMs applied to the iris
dataset in ECEN 758 Assignment 4 — fitting a linear-kernel and an RBF-kernel classifier and
reading the hyperplane geometry back out. Those worked problems are below.

## How I did it

*Source: my ECEN 758 Assignment 4 solutions
(`course-files/appendix/Homework/ecen758_hw/Assignment_4_ECEN_758_Solutions.pdf`, my own
work). The task prompts are the instructor's; I've paraphrased them and re-typeset my
solutions.*

### Worked example 1 — the linear-kernel hyperplanes on iris

**Paraphrased task.** Take the iris flower dataset, keep just two features — petal length and
sepal width — and fit a linear-kernel SVM (scikit-learn defaults, `random_state=0`). Write
down the equation of the separating hyperplane for each class.

**How I solved it.** With three classes, scikit-learn fits the SVM one-vs-rest: one linear
boundary per class, each of the form

$$w_1 x_1 + w_2 x_2 + w_0 = 0,$$

where $x_1$ is petal length, $x_2$ is sepal width, $w_1, w_2$ are the learned weights, and
$w_0$ is the bias. Pulling the fitted `coef_` and `intercept_` out of the model gives:

| Class | $w_1$ (petal length) | $w_2$ (sepal width) | $w_0$ (bias) |
|---|---|---|---|
| Setosa | $-1.226$ | $0.669$ | $1.056$ |
| Versicolor | $-0.687$ | $0.238$ | $1.497$ |
| Virginica | $-3.333$ | $0.952$ | $13.475$ |

So the Setosa-vs-rest boundary, for example, is

$$-1.226\,x_1 + 0.669\,x_2 + 1.056 = 0.$$

To classify a new flower you plug it into all three decision functions
$f_c(x) = w_1 x_1 + w_2 x_2 + w_0$ and pick the class with the largest score. Reading the
weights is instructive: petal length ($x_1$) carries the big negative weights in every row, so
it's the feature doing most of the separating — and Virginica's much larger magnitudes
($-3.333$, bias $13.475$) reflect that its boundary sits out at the long-petal end of the
data, far from the origin in feature space.

**The margin, geometrically.** The reason those weights aren't arbitrary is what the SVM
optimizes: it places each hyperplane to maximize the margin. The distance from a point $x$ to
the boundary is $|w^\top x + w_0| / \lVert w \rVert$, and the SVM maximizes the gap
$2/\lVert w \rVert$ subject to every point staying on the correct side (soft-margin: mostly).
Only the closest points — the **support vectors** — actually pin the boundary; move a
far-away point and nothing changes.

### Worked example 2 — switching to an RBF kernel

**Paraphrased task.** Classify the same two-feature iris data with a radial-basis-function
(RBF) kernel and report the bandwidth used.

**How I solved it.** With scikit-learn's default `gamma="scale"`, the RBF bandwidth is set
from the data rather than guessed:

$$\gamma = \frac{1}{n_\text{features}\cdot \operatorname{Var}(X)} \approx 0.283.$$

That $\gamma$ is the whole character of the RBF kernel: it sets how far a single support
vector's influence reaches. A large $\gamma$ makes each point's influence very local (tight,
wiggly boundaries that can overfit); a small $\gamma$ makes it broad and smooth. `"scale"`
picks a sensible middle from the feature variance.

**What changed vs. the linear kernel.** Plotting both decision boundaries, both models
separate the Setosa class cleanly — it's linearly separable from the other two, so the kernel
barely matters there. The difference shows up between Versicolor and Virginica, which overlap:
the **linear kernel can only draw straight boundaries**, while the **RBF kernel bends the
boundary** between clusters of points to follow the overlap. That flexibility is exactly the
kernel trick — the RBF model is fitting a linear boundary in an implicit higher-dimensional
space, which is a curved boundary back in the original two features.

## Gotchas

- **Scale features first.** The margin is defined by distances, so unscaled features
  distort the hyperplane — standardize before fitting.
- **The kernel and `C` are the whole game.** `C` trades margin width against
  misclassification; the RBF `gamma` sets how local each support vector's influence is.
  Both need cross-validation — and note that `gamma="scale"` (used above) reads `gamma` off
  the data variance, which is a reasonable default but still worth tuning.
- **One boundary per class in multi-class.** The three hyperplanes above come from
  scikit-learn's one-vs-rest wrapper; SVM is binary at heart, and the reported `coef_` is a
  row per class, not a single global boundary.
- **Doesn't scale to huge datasets.** Kernel SVMs are roughly quadratic in sample count,
  which is why gradient-boosted trees and neural nets took over most large-scale tabular
  and image tasks.

## References

- ECEN 758 Assignment 4 (my own solutions:
  `course-files/appendix/Homework/ecen758_hw/Assignment_4_ECEN_758_Solutions.pdf`) — the
  linear/RBF iris worked examples above.
- ECEN 758 Lecture 20 — Support Vector Machines (local:
  `course-files/08-machine-learning/758 Lec 20 Support Vector Machines.pdf`).
  Instructor-copyrighted; concept summary only.
