# Scientific Machine Learning & Physics-Informed Neural Networks

## Overview

This chapter is the "what if the physics is part of the loss?" layer of the book. Most
of the rest of these notes fit models to data and let the data speak. **Scientific
machine learning (SciML)** starts from the opposite end: I already know the governing
equation — a differential equation from physics — and I want a neural network whose
*failure to satisfy that equation* is the thing I minimize. A **physics-informed neural
network (PINN)** does exactly that: it puts the PDE residual into the loss, so the
network is trained to obey the physics at a cloud of sampled points rather than to
interpolate a labeled dataset.

It draws on one stream of my own work:

- **ECEN 744 — Scientific Machine Learning (Texas A&M grad, Spring 2026), taught by
  Ulisses Braga-Neto.** A first course in the field: ODE/PDE discretization, automatic
  differentiation, PINNs, self-adaptive PINNs, and physics-informed Bayesian methods. My
  contributions here are the homework (a from-scratch numerical-integrator study,
  re-typeset below), an original PINN demo I wrote for this chapter, and a **final
  project** — a controlled study of which optimizer trains SA-PINNs best, done jointly
  with a project teammate on top of Levi McClenny's public SA-PINN codebase.

The through-line, the same one that runs through the [Linear Algebra](../02-linear-algebra/index.md)
and [Machine Learning](../08-machine-learning/index.md) chapters, is that *training is
still just gradient descent on a loss* — the only new idea is that the loss is built from
**derivatives of the network with respect to its own inputs**, computed by the exact same
automatic differentiation that backprop uses for the weights.

> **Attribution & privacy.** The ECEN 744 lecture slides and the instructor's Burgers
> demo notebook are Braga-Neto's copyrighted course material — this chapter paraphrases
> concepts and **re-derives every result in my own words with my own code and figures; no
> slide text, slide figure, or instructor notebook cell is reproduced here.** The final
> project is joint work: it is built on **Levi McClenny's** public
> [SA-PINN codebase](https://github.com/levimcclenny/SA-PINNs) (named and linked
> throughout), and co-developed with a project teammate whom I refer to only as "my
> project teammate." All PDE benchmarks and datasets shown are public academic benchmarks
> (the Raissi PINNs repository); there is no private or personal data anywhere in this
> chapter.

## Why SciML — where PINNs fit vs. classical numerics

The classical way to solve a PDE is a **mesh**: discretize space and time into a grid,
approximate the derivatives with finite differences (or elements, or spectral modes), and
march forward. It is mature, accurate, and fast — and it is exactly what I use to
*generate the ground truth* for every experiment in this chapter (the
[discretization page](discretization-and-autodiff.md) is that machinery in miniature).
So a PINN is not competing with a finite-difference solver on a clean forward problem —
it will usually lose.

What a PINN buys you is a **mesh-free, differentiable, continuous** solution, and that
changes the calculus on certain problems:

- **Inverse problems.** When part of the equation is *unknown* — a diffusion coefficient,
  a source term — and you have some noisy measurements, a PINN folds "fit the data" and
  "obey the physics" into one loss and estimates the unknown parameter alongside the
  solution. This is the case the instructor's course demo makes (estimating an unknown
  viscosity from sensor data), and it is where PINNs are genuinely competitive.
- **High-dimensional problems** where a grid is exponentially expensive but a network is
  not.
- **A continuous solution you can differentiate anywhere**, for free, after training — no
  interpolation between grid nodes.

The cost is that **training is an optimization problem, and a nasty one**: the loss
surface of a PINN is stiff and ill-conditioned, and plain Adam often stalls far from a
good solution. That single fact is what my final project is about — see the
[optimizer study](optimizer-study.md).

## The pages

1. [Discretization & automatic differentiation](discretization-and-autodiff.md) — the
   classical numerical-integration ladder (Euler → RK4) and the autodiff idea that
   replaces finite differences inside a PINN. *(My ECEN 744 HW1, runnable.)*
2. [How PINNs work](pinns.md) — the residual loss, collocation points, and an **original
   PINN I wrote from scratch** that solves the 1-D Burgers equation.
3. [Self-adaptive PINNs](sa-pinns.md) — the soft-attention weighting that turns the flat
   loss into a saddle-point objective, and why it helps on sharp features.
4. [The optimizer study](optimizer-study.md) — the final project: Adam/L-BFGS vs. a
   learnable meta-optimizer vs. self-scaled quasi-Newton, across four PDEs.
5. [Results & lessons](results-and-lessons.md) — what won, where it didn't, and the
   honest reproducibility caveats.

## Notebooks

- [PINN: Burgers from scratch](notebooks/pinn-burgers-demo.ipynb) — my own small JAX PINN
  solving the forward viscous Burgers equation on a laptop CPU, with the residual built
  by `jax.grad`, a hand-rolled Adam loop, and the resulting solution field.
- [SA-PINN optimizer results](notebooks/sa-pinn-optimizer-results.ipynb) — loads the
  final project's committed result CSVs and replots the optimizer comparison across the
  four PDE benchmarks.

## Key Takeaways

- **The physics goes in the loss.** A PINN's loss is a sum of a PDE-residual term (the
  network must satisfy the equation at sampled *collocation points*) and data terms
  (initial/boundary conditions, or measurements). No labeled solution is required for the
  interior.
- **Autodiff is the whole trick.** `u_t`, `u_x`, `u_xx` are exact derivatives of the
  network output with respect to its inputs — the same automatic differentiation that
  computes `∂loss/∂weights`, pointed at the inputs instead.
- **The optimizer is the bottleneck, not the architecture.** On stiff PDEs, second-order
  and self-scaled quasi-Newton methods reach errors one to four orders of magnitude below
  Adam/L-BFGS — the headline result of my final project.
- **PINNs don't replace solvers.** They earn their keep on inverse and mesh-free
  problems; on a clean forward problem a classical solver is still the right tool (and my
  reference).
