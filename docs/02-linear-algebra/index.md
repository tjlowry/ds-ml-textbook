# Linear Algebra

## Overview

This chapter is the "why the math actually works" layer under the rest of the book.
Least squares, PCA, gradient descent, attention, PageRank — every one of them is linear
algebra wearing a different hat. I wrote it **visuals-first** on purpose: I learn this
material by *seeing* the geometry (a vector dropping a perpendicular onto a subspace, a
circle stretching into an ellipse), so almost every page leads with a picture I generated
myself rather than a wall of symbols.

It draws on one main stream of my own work:

- **MATH 677 — Computational Linear Algebra (Texas A&M grad).** A numerically-minded second
  course in linear algebra: solving `Ax = b`, least squares and QR, eigenvalue iterations,
  the SVD, Perron-Frobenius theory, and then a run of optimization topics (dynamic
  programming, steepest/gradient descent, convex optimization, compressed sensing). My
  contributions are the handwritten homework (worked examples re-typeset below) and a
  from-scratch **projected gradient descent** solver with an Armijo line search.
- **BYU-Idaho MATH 341 (undergrad).** I took the proof-based first course years earlier. Its
  theorem sheet still travels with me — I've re-typeset it as a
  [theorem reference](theorem-reference.md) in our own wording.

Every "In modern ML" section connects a classical result to something I actually build
elsewhere in this book — cosine similarity to embeddings, `QKᵀ` to the attention in my
[Mini-GPT notebook](../08-machine-learning/notebooks/mini-gpt-from-scratch.ipynb), the SVD
to LoRA, eigenvectors to [PCA](../08-machine-learning/dimensionality-reduction/pca.md).

> **Attribution & privacy.** The MATH 677 lecture slides are the instructor's copyrighted
> course material — this chapter paraphrases concepts and **re-derives every result in my
> own words with my own examples and figures; no slide text or figure is reproduced**. The
> BYU-I MATH 341 theorem statements are mathematical facts, re-typeset here in our own
> layout, not copied from the original sheet. All datasets shown are toy/synthetic.

## Topics

- [Linear Algebra in ML](linear-algebra-in-ml.md) — the consolidated concept map:
  embeddings, attention, low-rank/LoRA, least squares, eigenvectors, and gradient descent
  all in one place, each linking back to its full page.

### Solving and factoring

- [Linear Systems](linear-systems.md) — `Ax = b`, row reduction, and the vector/matrix
  operations everything else is built on.
- [Least Squares](least-squares.md) — the normal equations `AᵀAx = Aᵀb` as an orthogonal
  projection onto the column space.
- [Eigenvalues & Eigenvectors](eigenvalues-eigenvectors.md) — directions a matrix only
  rescales, plus the power method.
- [Singular Value Decomposition](svd.md) — rotate → stretch → rotate, and low-rank
  approximation.
- [Perron-Frobenius](perron-frobenius.md) — why positive matrices have a dominant
  eigenvector (and why PageRank converges).

### Optimization

- [Dynamic Programming](dynamic-programming.md) — trading recomputation for memory, via
  Fibonacci.
- [Gradient Descent](gradient-descent.md) — steepest descent, line search, and my projected
  GD solver.
- [Convex Optimization](convex-optimization.md) — the property that makes "local = global"
  true.
- [Compressed Sensing](compressed-sensing.md) — recovering sparse signals with the `ℓ₁`
  norm.

### Reference

- [Theorem Reference](theorem-reference.md) — the key theorems, organized by topic, in our
  own typesetting.

## Notebooks

- [Projected Gradient Descent](notebooks/projected-gradient-descent.ipynb) — my own
  numpy+sympy solver: projected gradient descent with an Armijo backtracking line search,
  onto a circle and a half-plane constraint, each verified against the closed-form answer
  (MATH 677).

## Key Takeaways

- **Geometry first.** Least squares is a perpendicular; eigenvectors are the axes a map
  doesn't rotate; the SVD is rotate-stretch-rotate. Once I see the picture the formulas stop
  being arbitrary.
- **It's the same handful of ideas everywhere.** Projection, orthogonality, and
  eigen/singular structure reappear as PCA, embeddings, attention, and PageRank.
- **Numerical ≠ symbolic.** MATH 677 is about *how you actually compute* these things
  (iterations, factorizations, line searches), not just that a solution exists.
- **Honest sourcing.** Several topics here are lecture-plus-homework only; where I have no
  code of my own the page says so and re-typesets a worked example from my HW instead.
