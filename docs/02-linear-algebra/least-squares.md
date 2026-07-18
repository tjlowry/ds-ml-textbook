# Least Squares

## Overview

When `Ax = b` has **no** exact solution — more equations than unknowns, noisy data — least
squares finds the `x̂` that gets as close as possible: it minimizes `‖Ax − b‖²`. The
geometry is the whole story: `Ax` can only ever land in the column space of `A`, so the best
we can do is the point in that subspace *nearest* `b`, which is the **orthogonal projection**
`b̂`. The error `b − b̂` sticks out perpendicular to the subspace.

I covered this in MATH 677 Lecture 2 (projection, Gram-Schmidt, the normal equations) and
worked it by hand in my homework. It is also the exact math under linear
[regression](../03-statistics/regression/simple-linear.md).

## The picture

![A vector b sitting above a plane (the column space of A); its projection b-hat lies in the
plane and the residual b minus b-hat is a dashed perpendicular line.](img/least-squares-projection.png)

Because the residual is perpendicular to every column of `A`, we get `Aᵀ(b − Ax̂) = 0`,
which rearranges into the **normal equations**:

$$
A^{\top}A\,\hat{\mathbf{x}} = A^{\top}\mathbf{b}
$$

When the columns of `A` are linearly independent, `AᵀA` is invertible and
`x̂ = (AᵀA)⁻¹Aᵀb`. (In practice you solve the normal equations, or better, use a
[QR factorization](svd.md) — forming `AᵀA` squares the condition number.)

## Worked example — the normal equations by hand

*Restated from my own homework: solve the least-squares problem for the tall system*

$$
A = \begin{bmatrix} 1&2\\ 2&3\\ 3&2\\ -1&0\\ -2&1 \end{bmatrix},\qquad
\mathbf{b} = \begin{bmatrix} 1\\2\\0\\-1\\-2 \end{bmatrix}.
$$

Five equations, two unknowns — almost certainly inconsistent, so we go straight to the
normal equations. Forming `AᵀA` and `Aᵀb`:

$$
A^{\top}A = \begin{bmatrix} 19&12\\ 12&18 \end{bmatrix},\qquad
A^{\top}\mathbf{b} = \begin{bmatrix} 10\\ 6 \end{bmatrix}.
$$

Row-reducing `[AᵀA \mid Aᵀb]` (the determinant is `19·18 − 12² = 198`) gives

$$
\hat{\mathbf{x}} = \begin{bmatrix} 6/11\\ -1/33 \end{bmatrix} \approx
\begin{bmatrix} 0.545\\ -0.030 \end{bmatrix}.
$$

That `x̂` doesn't solve any single equation exactly — it is the combination of the two
columns that lands closest to `b`. *Worked in my MATH 677 HW 5 (local:
`course-files/appendix/Homework/math_677_linAlg/HW 5 Written.pdf`).* The same homework also
does the QR-flavored version by hand with **Givens rotations** to triangularize the matrix,
which is the numerically stable way to solve the same problem without ever forming `AᵀA`.

Quick check in numpy:

```python
import numpy as np
A = np.array([[1,2],[2,3],[3,2],[-1,0],[-2,1]])
b = np.array([1,2,0,-1,-2])
xhat = np.linalg.solve(A.T @ A, A.T @ b)   # -> [0.5454..., -0.0303...]
np.linalg.lstsq(A, b, rcond=None)[0]        # same answer, via QR
```

## In modern ML

*Consolidated view: [Linear Algebra in ML](linear-algebra-in-ml.md) collects this and the chapter's other ML connections on one page.*

### Residuals are what's left to explain

Rotate the projection picture into "data space" and the residual `b − b̂` becomes the stack
of **regression residuals** — the vertical gaps between each point and the fitted line.

![Scatter of points with a least-squares line and vertical orange segments marking each
residual — the part of y the line could not explain.](img/regression-residuals.png)

This reframing is the seed of **gradient boosting**: fit a simple model, look at its
residuals, then train the next model to predict *those*. Each round is another least-squares
step against the leftover error. I lean on that idea in the
[bagging & boosting](../08-machine-learning/ensembles/bagging-boosting.md) and
[XGBoost](../08-machine-learning/ensembles/xgboost.md) pages.

## Gotchas

- **Don't form `AᵀA` if you can help it.** It squares the condition number and can turn a
  merely-hard problem into an unstable one. `np.linalg.lstsq` (QR/SVD under the hood) is the
  safe default; the normal equations are for understanding, not production.
- **Independent columns matter.** If the columns of `A` are dependent, `AᵀA` is singular and
  the solution isn't unique — you need a pseudo-inverse (SVD) or regularization.
- **Least squares assumes the error is worth squaring.** Squaring punishes outliers hard; if
  the noise is heavy-tailed, an `ℓ₁`/robust loss fits better (and connects to
  [compressed sensing](compressed-sensing.md)).

## References

- MATH 677 Lecture 2 — Solving Least Squares (local:
  `course-files/02-linear-algebra/2 Solving least squares complete.pdf`).
  Instructor-copyrighted; concept summary only.
- Normal equations & orthogonal projection theorems:
  [theorem reference](theorem-reference.md#orthogonality-projection-and-least-squares).
