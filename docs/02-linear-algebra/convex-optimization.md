# Convex Optimization

## Overview

A problem is **convex** when its objective is a convex function over a convex feasible set — and
that single property is what separates optimization you can *trust* from optimization you can
only *hope* about. On a convex function every local minimum is the global minimum, so
[gradient descent](gradient-descent.md) can't get stuck in a bad basin. MATH 677 Lecture 9 made
this precise: convex sets, convex functions, strict convexity, and the second-derivative tests
that certify it.

## The picture: chord above the curve

The clean definition is geometric. A function is **convex** if the straight line (chord) between
any two points on its graph never dips below the graph:

![Two panels. Left: a convex parabola with a chord lying entirely above it and a single global
minimum star. Right: a non-convex double-well curve where the chord cuts below the curve, with
two local minima marked.](img/convex-vs-nonconvex.png)

$$
f\big(t\mathbf{x} + (1-t)\mathbf{y}\big) \;\le\; t f(\mathbf{x}) + (1-t) f(\mathbf{y}),
\qquad t \in [0, 1].
$$

Left panel: the chord stays above, there's one bowl, and any downhill path lands at *the*
minimum. Right panel: the chord dips below the curve — the tell-tale of non-convexity — and now
there are multiple valleys, so where you end up depends on where you start.

**Certifying convexity.** In 1-D, `f'' ≥ 0` everywhere means convex (`f'' > 0` means *strictly*
convex — a unique minimum). In higher dimensions the analog is a **positive semidefinite
Hessian** `∇²f ⪰ 0` — all eigenvalues non-negative, which loops right back to
[eigenvalues](eigenvalues-eigenvectors.md): the Hessian's eigenvalues tell you the curvature in
each principal direction, and convexity is "curves up in every direction."

## Why it matters

- **Local = global.** On a convex problem, the first-order condition `∇f = 0` (plus feasibility)
  is *sufficient* for the global optimum — no restarts, no "did I find the real minimum?" doubt.
- **Strict convexity ⇒ unique.** A strictly convex objective has exactly one minimizer, so the
  answer is well-defined.
- **The feasible set counts too.** Minimizing a convex function over a non-convex set can still
  be hard — you need both halves convex. My projected-gradient
  [notebook](notebooks/projected-gradient-descent.ipynb) uses convex constraint sets (a disk, a
  half-plane) precisely so the projection is well-defined and cheap.

## In modern ML

Most classic ML objectives are deliberately convex — **linear/ridge regression, logistic
regression, and linear SVMs** all minimize a convex loss, which is why they train reliably to a
unique optimum. Regularizers keep them that way: an `ℓ₂` (ridge) penalty *adds* curvature
(makes the Hessian more positive-definite), turning a possibly-flat problem into a strictly
convex one with a unique solution — the same trick that stabilizes the
[least-squares](least-squares.md) normal equations.

Deep networks are the opposite — wildly **non-convex** — which is exactly why the right panel
matters: training is all about finding a *good enough* local minimum (initialization, momentum,
learning-rate schedules) rather than *the* global one.

## Gotchas

- **Convex set ≠ convex function.** You need both: a convex objective *and* a convex feasible
  region. Either one broken and the "local = global" guarantee is gone.
- **`f'' ≥ 0` is a global condition.** A function can curve up near one point and still be
  non-convex overall (the double well) — check the whole domain, or the Hessian's eigenvalues
  everywhere.
- **Convex doesn't mean easy, just trustworthy.** A convex problem can still be large or
  ill-conditioned; convexity guarantees *where* you'll converge, not *how fast* — that's still
  the [gradient descent](gradient-descent.md) conditioning story.

## References

- MATH 677 Lecture 9 — Convex Optimization (local:
  `course-files/02-linear-algebra/9 Convex optimization complete.pdf`). Instructor-copyrighted;
  concept summary only.
