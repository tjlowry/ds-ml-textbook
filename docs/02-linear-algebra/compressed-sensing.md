# Compressed Sensing

## Overview

**Compressed sensing** recovers a signal from *far fewer* measurements than classical sampling
says you need — provided the signal is **sparse** (mostly zeros) in some basis. It flips the
usual pipeline: instead of sampling everything and then compressing, you take a handful of clever
linear measurements and reconstruct by solving an underdetermined system with a sparsity
preference. MATH 677 closed the term with it (Lecture 10), motivated by MRI (fewer scans → less
time in the machine) and audio.

## The problem

You measure `y = Ax` where `A` is **wide** (fewer rows than columns), so `Ax = y` has infinitely
many solutions — an underdetermined [linear system](linear-systems.md). Which one is "the"
signal? Compressed sensing's answer: the **sparsest** one. Ideally you'd minimize the `ℓ₀`
"norm" (the count of nonzeros), but that's combinatorial and NP-hard. The key result is that
minimizing the **`ℓ₁` norm** — the sum of absolute values — recovers the same sparse solution
under mild conditions, and `ℓ₁` is convex, hence tractable.

$$
\min_{\mathbf{x}} \; \|\mathbf{x}\|_1 \quad \text{subject to} \quad A\mathbf{x} = \mathbf{y}.
$$

## The picture: why `ℓ₁` finds sparse solutions

The whole intuition fits in one diagram. The solution set of `Ax = y` is a line (a flat subspace).
Grow a norm-ball from the origin until it first touches that line — that touch point is the
minimum-norm solution. The *shape* of the ball decides where it touches:

![Two panels sharing a constraint line. Left: an L2 (round) ball grows until it kisses the line
tangentially at an off-axis point (dense solution). Right: an L1 (diamond) ball touches the line
at its top vertex, which lies on an axis, giving a sparse solution with a zero
coordinate.](img/l1-vs-l2-sparse.png)

- The **`ℓ₂` ball is round**, so it usually touches the line at a generic point with *both*
  coordinates nonzero — a **dense** solution.
- The **`ℓ₁` ball is a diamond** with its corners *on the axes*, so it almost always touches at a
  corner — a solution with a **zero** coordinate. That's sparsity, and it's why `ℓ₁` (LASSO,
  basis pursuit) is the workhorse of sparse recovery.

This is the same geometry as **LASSO** regression: the `ℓ₁` penalty drives coefficients exactly
to zero (feature selection), while the `ℓ₂`/ridge penalty only shrinks them.

## In modern ML

*Consolidated view: [Linear Algebra in ML](linear-algebra-in-ml.md) collects this and the chapter's other ML connections on one page.*

The `ℓ₁`-drives-things-to-zero mechanism shows up all over:

- **LASSO / sparse regression** — automatic feature selection, the direct application of this
  diagram to the [regression](../03-statistics/regression/multiple-linear.md) setting.
- **Model & network pruning** — `ℓ₁` regularization pushes weights to exact zero so they can be
  dropped, shrinking models for deployment.
- **Sparse dictionary / autoencoder codes** — an `ℓ₁` penalty on the latent code forces compact,
  mostly-zero representations.

It's the counterpart to the [SVD's](svd.md) low-rank story: low rank compresses by assuming few
*directions* matter; sparsity compresses by assuming few *coordinates* matter.

## Gotchas

- **`ℓ₀` is the honest objective but is NP-hard.** `ℓ₁` is the convex surrogate that provably
  recovers the same answer under conditions like RIP (restricted isometry) — which is why the
  measurement matrix `A` has to be "spread out" (often random), not arbitrary.
- **Sparse *in some basis*.** The signal need not be sparse in its raw form — images are sparse in
  a wavelet basis, not pixel space. You reconstruct in the basis where sparsity lives.
- **`ℓ₁` is convex but not smooth.** The corners that create sparsity are non-differentiable, so
  you need subgradient / proximal methods (soft-thresholding), not plain
  [gradient descent](gradient-descent.md).

## References

- MATH 677 Lecture 10 — Compressed Sensing (local:
  `course-files/02-linear-algebra/10 Compressed sensing complete.pdf`). Instructor-copyrighted;
  concept summary only.
