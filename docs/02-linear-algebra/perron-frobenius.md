# Perron-Frobenius

## Overview

**Perron-Frobenius theory** is the reason iterations on non-negative matrices settle down to a
single dominant direction. Its headline: a matrix with all-positive entries has a **real,
positive, strictly-largest eigenvalue** (the *Perron root*), and its eigenvector can be chosen
all-positive. That "one direction wins" guarantee is what makes PageRank converge, what gives a
Markov chain a unique steady state, and what pins down the long-run growth rate of a positive
linear system.

This was a short lecture in MATH 677 (Lecture 5), but it ties the eigenvalue material to
something I use directly — the [PageRank / graph methods](../08-machine-learning/other/pagerank.md)
page in the ML chapter.

## The picture: iterating toward the steady state

A column-stochastic matrix `P` (columns are probability distributions) has Perron root `λ = 1`.
Iterate `x_{k+1} = P x_k` from any starting distribution and you converge to the Perron
eigenvector — the **steady state** `q` with `Pq = q`.

![Three probability curves over 18 iterations of x-next = P x, each starting from a
one-hot state and converging to a dotted horizontal steady-state
level.](img/perron-steady-state.png)

Every starting distribution funnels to the *same* `q` — the steady state doesn't depend on
where you begin, only on `P`. That's the Perron-Frobenius guarantee in action: because `λ = 1`
is strictly dominant, all the other eigen-components decay away and only the Perron direction
survives.

## Why it works

Diagonalize and the point is immediate: `Pᵏ` raises each eigenvalue to the `k`. If the Perron
root `λ₁` is strictly bigger than every other `|λ_i|`, then after enough steps the `λ₁` term
dwarfs the rest and the iteration aligns with the Perron eigenvector. For a stochastic matrix
`λ₁ = 1` and everything else shrinks, so the distribution converges instead of growing or
decaying.

The **spectral radius** `ρ(P) = max|λ_i|` (here equal to the Perron root) also controls
*stability*: an iteration `x_{k+1} = P x_k` blows up when `ρ > 1` and decays when `ρ < 1`.
Gelfand's formula ties this to matrix norms — `ρ(P) = lim ‖Pᵏ‖^{1/k}` — the theoretical
statement that "long-run growth rate = dominant eigenvalue."

## In modern ML

*Consolidated view: [Linear Algebra in ML](linear-algebra-in-ml.md) collects this and the chapter's other ML connections on one page.*

**PageRank is Perron-Frobenius.** The web is a giant column-stochastic transition matrix; the
PageRank vector is its Perron eigenvector — the unique steady-state distribution of a random
surfer. The "damping factor" (teleportation) is a trick to *force* the matrix strictly
positive so Perron-Frobenius applies and the [power method](eigenvalues-eigenvectors.md)
converges to a unique ranking. See [PageRank & Graph Methods](../08-machine-learning/other/pagerank.md).

## Gotchas

- **Positive vs non-negative matters.** Strictly positive matrices get the full theorem;
  merely non-negative ones need an *irreducibility/primitivity* condition (the graph must be
  strongly connected and aperiodic) or you can get multiple or oscillating dominant
  eigenvalues.
- **Convergence speed is the eigenvalue gap.** How fast you reach the steady state is set by
  `|λ₂/λ₁|`, the same ratio that governs the [power method](eigenvalues-eigenvectors.md) — a
  small gap means slow mixing.
- **Column- vs row-stochastic.** Keep track of which convention you're in; it decides whether
  the steady state is a left or right eigenvector.

## References

- MATH 677 Lecture 5 — Perron-Frobenius (local:
  `course-files/02-linear-algebra/5 Perron-Frobenius complete.pdf`). Instructor-copyrighted;
  concept summary only.
- The regular-stochastic-matrix steady-state theorem is restated in the
  [theorem reference](theorem-reference.md#markov-chains-and-steady-state).
