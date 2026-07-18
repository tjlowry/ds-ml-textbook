# Gradient Descent

## Overview

**Gradient descent** minimizes a function by repeatedly stepping in the direction of steepest
decrease — the negative gradient. It is the workhorse behind essentially all of modern ML
training: too big to solve in closed form, so you iterate. MATH 677 built it up carefully
(Lecture 8, Steepest Descent) — the intuition, the update rule, how to *choose the step size*
with a line search, and how to handle **constraints** by projecting back onto the feasible set.
This is the page with the most of my own code: a from-scratch **projected gradient descent**
solver, promoted to a [notebook](notebooks/projected-gradient-descent.ipynb).

## The update rule and the picture

$$
\mathbf{x}_{k+1} = \mathbf{x}_k - \alpha\,\nabla f(\mathbf{x}_k)
$$

The gradient points uphill, so `−∇f` points downhill; `α` (the step size / learning rate) sets
how far you move. On a stretched-out bowl the path zig-zags — it keeps overshooting across the
narrow direction:

![Contour plot of an anisotropic quadratic bowl with the gradient-descent iterates plotted as
connected dots zig-zagging down the valley from a red start toward a green minimum at the
origin.](img/gradient-descent-path.png)

Those are real iterates from running GD with a fixed step of 0.28. The zig-zag is the classic
symptom of an **ill-conditioned** problem (the bowl is much steeper in one direction than the
other) — the same conditioning idea from [least squares](least-squares.md). Too big a step and
it diverges; too small and it crawls. Choosing `α` well is the whole game.

## Choosing the step: line search

Rather than guess a fixed `α`, a **line search** picks one each step. The **Armijo
(backtracking)** condition accepts a step only if it produces "enough" decrease, and shrinks `α`
by a factor `ρ` until it does:

$$
f(\mathbf{x} + \alpha \mathbf{d}) \le f(\mathbf{x}) + c_1\,\alpha\,\nabla f(\mathbf{x})^{\top}\mathbf{d}
$$

This is exactly the inner loop of my solver below.

## How I did it — projected gradient descent

My own MATH 677 code minimizes `f` subject to a constraint by taking a gradient step and then
**projecting** the result back onto the feasible set (a circle, or a half-plane) before the
line search. Projecting onto a ball of radius `r` is just "if you left the ball, rescale back
to the boundary":

```python
def proj_gradient_circle(f, gradf, x0, r, tol, rho, c1):
    # minimize f over the set x^2 + y^2 <= r^2 via projected gradient descent
    x = x0.copy()
    while True:
        grad = gradf(x)
        x_test = x - grad
        norm_test = np.sqrt(np.dot(x_test, x_test))
        if norm_test > r:                       # left the disk -> project onto boundary
            x_test = (r / norm_test) * x_test
        if np.linalg.norm(x - x_test) < tol:
            break
        d = x_test - x
        alpha = 1.0
        while f(x + alpha * d) > f(x) + c1 * alpha * np.dot(grad, d):   # Armijo backtracking
            alpha = rho * alpha
        x = x + alpha * d
    return x
```

Source: `course-files/02-linear-algebra/proj_gradient.py`

The gradients come from **sympy** (I write `f` symbolically and `lambdify` its derivatives),
and each run is checked against the closed-form optimum. The half-plane version does the same
with a projection onto `{x : nᵀx ≤ c}`. Full walk-through, plots, and the verify-vs-closed-form
comparison are in the notebook.

## Notebook

See the rendered notebook:
[Projected Gradient Descent](notebooks/projected-gradient-descent.ipynb) — my solver run on a
circle constraint and a half-plane constraint, with convergence plotted and every answer checked
against the exact minimizer.

Re-run locally: `jupyter lab docs/02-linear-algebra/notebooks/projected-gradient-descent.ipynb`

## Worked example — steepest descent by hand

*Restated from my own homework: minimize `f(x, y) = x² + 2xy + y²` by steepest descent with a
fixed step `c = 1/3`, starting from `x⁽⁰⁾ = (1, 0)`.*

The gradient is `∇f = (2x + 2y, 2x + 2y)`. At the start `∇f(1, 0) = (2, 2)`, so

$$
\mathbf{x}^{(1)} = \begin{bmatrix}1\\0\end{bmatrix} - \tfrac{1}{3}\begin{bmatrix}2\\2\end{bmatrix}
= \begin{bmatrix}1/3\\-2/3\end{bmatrix}.
$$

At the new point `∇f = (−2/3, −2/3)`, giving

$$
\mathbf{x}^{(2)} = \begin{bmatrix}1/3\\-2/3\end{bmatrix} - \tfrac{1}{3}\begin{bmatrix}-2/3\\-2/3\end{bmatrix}
= \begin{bmatrix}5/9\\-4/9\end{bmatrix}.
$$

Note `f = (x + y)²`, so the whole valley `x + y = 0` is optimal — the iterates march toward that
line. *Worked in my MATH 677 HW 11 (local:
`course-files/appendix/Homework/math_677_linAlg/Hw 11 written.pdf`); the same HW does an Armijo +
curvature (Wolfe) line search by hand — backtracking `α = 1 → ½ → ¼ → …` until both conditions
hold — and several Newton's-method iterations for comparison.*

## In modern ML

Every optimizer I use — SGD, Adam, the whole training loop of the
[neural networks](../08-machine-learning/deep-learning/neural-network-fundamentals.md) and
[Mini-GPT](../08-machine-learning/notebooks/mini-gpt-from-scratch.ipynb) in the ML chapter — is
gradient descent with two upgrades: the gradient comes from **backpropagation** instead of
sympy, and the step size is adapted per-parameter (momentum, RMSProp/Adam) instead of a fixed
`α`. The zig-zag picture above is *why* those adaptive methods exist — they damp the overshoot
in ill-conditioned directions.

## Gotchas

- **Step size is everything.** Too large diverges, too small crawls; a line search or an adaptive
  optimizer removes the guesswork. The zig-zag means the problem is ill-conditioned, not that GD
  is broken.
- **GD finds a *local* min.** On a [convex](convex-optimization.md) function that's the global
  min; on a non-convex loss (any deep net) it's whatever basin you fell into — hence random
  restarts and good initialization.
- **Projection must land in the feasible set.** For a simple set (ball, half-plane, box) the
  projection is closed-form and cheap; for a complicated constraint it can be its own
  optimization problem.
- **Scale your features.** Unequal feature scales *create* the ill-conditioning that makes GD
  zig-zag — standardizing inputs is the cheapest fix.

## References

- MATH 677 Lecture 8 — Steepest Descent (local:
  `course-files/02-linear-algebra/8 Steepest descent complete.pdf`). Instructor-copyrighted;
  concept summary only.
- MATH 677 Lecture 7 — General Optimization (objective functions, real-world framing) (local:
  `course-files/02-linear-algebra/7 General optimization complete.pdf`).
