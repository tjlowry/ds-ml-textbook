# Singular Value Decomposition

## Overview

The **SVD** factors *any* matrix — square or not, invertible or not — as `A = UΣVᵀ`: an
orthogonal rotation `Vᵀ`, an axis-aligned stretch `Σ` (the non-negative **singular values**
on the diagonal), and a second rotation `U`. Where [eigenvectors](eigenvalues-eigenvectors.md)
only exist nicely for special square matrices, the SVD always exists, which makes it the most
useful factorization in the book: least squares, the pseudo-inverse, PCA, low-rank
compression, and matrix rank all fall straight out of it.

MATH 677 Lecture 4 built it geometrically, which is how it finally clicked for me.

## The picture: rotate → stretch → rotate

![Four panels showing a unit circle with two basis arrows being transformed step by step: the
circle, after V-transpose rotates it, after Sigma stretches it into an axis-aligned ellipse,
and after U rotates the ellipse into its final orientation.](img/svd-geometry.png)

Read left to right — this is what *every* matrix does to space:

1. **`Vᵀ` rotates** the input so the special input directions (right singular vectors) line up
   with the axes.
2. **`Σ` stretches** along those axes by the singular values `σ₁ ≥ σ₂ ≥ … ≥ 0`. The unit
   circle becomes an axis-aligned ellipse whose semi-axes *are* the singular values.
3. **`U` rotates** the ellipse into its final orientation (the left singular vectors).

So the singular values measure how much the matrix stretches space in each principal
direction, and the number of nonzero ones is the **rank**. A tiny singular value means an
almost-flat direction — the seed of low-rank approximation.

## In modern ML

*Consolidated view: [Linear Algebra in ML](linear-algebra-in-ml.md) collects this and the chapter's other ML connections on one page.*

### Low-rank approximation: the idea behind LoRA

Keep only the top `r` singular values (zero the rest) and you get the **best rank-`r`
approximation** of `A` — the Eckart-Young theorem. That single fact powers a huge amount of
modern practice: image/embedding compression, denoising, and **LoRA** fine-tuning.

![A schematic: a large d-by-d weight matrix W (d-squared parameters) approximated by the
product of a tall thin d-by-r matrix B and a short wide r-by-d matrix A, using only 2dr
parameters when r is much smaller than d.](img/low-rank-approximation.png)

Instead of updating a full `d×d` weight matrix (`d²` parameters), LoRA freezes `W` and learns
a low-rank correction `BA` with `B` being `d×r` and `A` being `r×d` — only `2dr` parameters
when `r ≪ d`. It's the SVD's "most matrices are approximately low rank" observation turned into
a parameter-efficient training trick. The same low-rank view explains why embedding tables and
recommender factorizations compress so well.

```python
U, s, Vt = np.linalg.svd(A, full_matrices=False)
r = 8                                   # keep the top r singular values
A_r = (U[:, :r] * s[:r]) @ Vt[:r]       # best rank-r approximation of A
```

## Relationship to eigenvectors and PCA

The singular values of `A` are the square roots of the eigenvalues of `AᵀA`, and the right
singular vectors `V` are that matrix's eigenvectors. So running an SVD on centered data gives
the [PCA](../08-machine-learning/dimensionality-reduction/pca.md) directions **without** ever
forming the covariance matrix `AᵀA` — which is numerically better, exactly the "don't square
the condition number" lesson from [least squares](least-squares.md).

## Gotchas

- **Use `full_matrices=False`.** For a tall `m×n` matrix the full `U` is `m×m` and usually
  wasteful; the "economy" SVD gives you the `m×n` piece you actually want.
- **Singular values are sorted and non-negative**, always. Eigenvalues can be negative or
  complex; singular values can't — that's part of why the SVD is so well-behaved.
- **Sign ambiguity in `U`/`V`.** Columns can flip sign (`u_i, v_i → −u_i, −v_i` leaves `A`
  unchanged), so don't rely on the sign of a singular vector being reproducible across
  libraries.
- **Rank is fuzzy in floating point.** "Zero" singular values are really *tiny* ones; pick a
  tolerance relative to `σ₁` rather than testing exact zeros.

## References

- MATH 677 Lecture 4 — Singular Value Decomposition (local:
  `course-files/02-linear-algebra/4 SVD complete (1).pdf`). Instructor-copyrighted; concept
  summary only.
- The Netflix-style low-rank matrix example also appears in MATH 677 Lecture 7 — General
  Optimization (local: `course-files/02-linear-algebra/7 General optimization complete.pdf`).
