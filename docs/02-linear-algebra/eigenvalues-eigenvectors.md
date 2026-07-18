# Eigenvalues & Eigenvectors

## Overview

An **eigenvector** of a matrix `A` is a direction the matrix does **not** rotate — it only
stretches or shrinks it: `Av = λv`. The scale factor `λ` is the **eigenvalue**. These are the
natural axes of a linear map: pick them as your coordinate system and the matrix becomes
diagonal, which is why they show up everywhere a repeated linear operation matters — PCA,
PageRank, differential equations, the stability of an iteration.

MATH 677 spent two lectures here (3A and 3B), focused on the *numerical* side: the **power
method** and its variants for actually computing eigenvalues when the matrix is too big to
find roots of the characteristic polynomial. I worked those methods by hand in HW 7.

## The picture

![Left: unit vectors and a circle before the map. Right: after applying A = [[2,1],[1,2]],
the eigenvectors (magenta, orange) still lie on their original lines — one stretched by 3, one
unchanged — while a generic blue vector has rotated off its line.](img/eigenvectors-transform.png)

For `A = [[2, 1], [1, 2]]` the eigenvectors are `(1, 1)` with `λ = 3` and `(1, −1)` with
`λ = 1`. Watch the two eigen-directions: after the map they still point along their original
lines (only the length changed). The generic blue vector, by contrast, gets rotated — it is
*not* an eigenvector. That "stays on its own line" property is the entire definition, made
visible.

When `A` has `n` independent eigenvectors it **diagonalizes** as `A = PDP⁻¹`, with the
eigenvectors as the columns of `P` and the eigenvalues down the diagonal of `D`. Then
`Aᵏ = PDᵏP⁻¹`, so repeated application is just raising each eigenvalue to the `k` — the reason
the *largest* eigenvalue dominates the long-run behavior of any iteration
(see [Perron-Frobenius](perron-frobenius.md)).

## Computing them: the power method

You rarely find eigenvalues by factoring the characteristic polynomial — for big matrices
that's hopeless. Instead you **iterate**: repeatedly multiply a random vector by `A` and
renormalize. Because `A` amplifies the dominant eigen-direction most, the vector swings toward
the top eigenvector, and the growth factor converges to the top eigenvalue.

```python
def power_method(A, iters=100):
    x = np.random.default_rng().normal(size=A.shape[0])
    for _ in range(iters):
        x = A @ x
        x = x / np.linalg.norm(x)      # renormalize so it can't blow up
    lam = x @ (A @ x)                  # Rayleigh quotient -> dominant eigenvalue
    return lam, x
```

To get the *next* eigenvalue you **deflate** — remove the found eigen-direction with a
Householder reflection and run the power method again on the smaller matrix. That
power-method-plus-Householder-deflation loop is exactly what I wrote pseudocode for in the
homework.

## Worked example — how fast does the power method converge?

*Restated from my own homework: the power method's error shrinks by the ratio of the top two
eigenvalues each step, `|λ₂/λ₁|`. If `λ₁ = 8` and `λ₂ = 6`, how many iterations to cut the
error by a factor of 1000?*

Each iteration multiplies the error by `λ₂/λ₁ = 6/8 = 0.75`, so after `k` steps the error is
scaled by `(6/8)ᵏ`. Set that equal to `1/1000` and solve:

$$
\left(\tfrac{6}{8}\right)^{k} = \tfrac{1}{1000}
\;\;\Longrightarrow\;\;
k = \frac{\ln(1/1000)}{\ln(6/8)} \approx 24 \text{ iterations}.
$$

The takeaway is the *ratio*, not the sizes: eigenvalues that are close together (`λ₂/λ₁ → 1`)
make the power method crawl, which is why real solvers add shifting/deflation to spread the
spectrum out. *Worked in my MATH 677 HW 7 (local:
`course-files/appendix/Homework/math_677_linAlg/HW 7 Written.pdf`); the same HW derives the
power-method + Householder-deflation pseudocode and reads eigenvalues off a block-triangular
matrix.*

## In modern ML

*Consolidated view: [Linear Algebra in ML](linear-algebra-in-ml.md) collects this and the chapter's other ML connections on one page.*

### Eigenvectors of the covariance matrix are PCA

Point a cloud of data at its own covariance matrix and the eigenvectors are the **principal
components** — the orthogonal directions of greatest variance, each stretched by its
eigenvalue (the variance along it).

![A 2-D data cloud with two arrows from the mean: PC1 (red) along the long axis of the cloud,
PC2 (green) perpendicular and shorter, each scaled by the square root of its
eigenvalue.](img/pca-eigen.png)

Keep the top few eigenvectors and you have a lower-dimensional representation that preserves
most of the variance — that is [PCA](../08-machine-learning/dimensionality-reduction/pca.md),
which I implemented from scratch (covariance → `np.linalg.eig`) in ECEN 758. The
[SVD](svd.md) gives the same directions without ever forming the covariance matrix.

## Gotchas

- **`np.linalg.eig` vs `eigh`.** Use `eigh` for symmetric/Hermitian matrices (covariance,
  Gram matrices) — it's faster, returns real eigenvalues, and orthonormal eigenvectors. `eig`
  is the general case and can hand back complex values.
- **Not every matrix diagonalizes.** A defective matrix (repeated eigenvalue short on
  independent eigenvectors) has no eigenbasis — that's when you fall back to the
  [SVD](svd.md) or a Jordan/Schur form.
- **Power method only finds the dominant one**, and only if there's a clear gap. Equal-magnitude
  top eigenvalues (e.g. `±λ`) make it oscillate instead of converge.
- **Sign and scale are free.** Eigenvectors are directions — any nonzero multiple is still an
  eigenvector, so libraries return them normalized with an arbitrary sign.

## References

- MATH 677 Lectures 3A & 3B — Eigenvalues and Eigenvectors (local:
  `course-files/02-linear-algebra/3A Eigenvalues and eigenvectors complete.pdf`,
  `3B Eigenvalues and eigenvectors complete.pdf`). Instructor-copyrighted; concept summary
  only.
- Diagonalization & eigenvalue theorems:
  [theorem reference](theorem-reference.md#eigenvalues-and-diagonalization).
