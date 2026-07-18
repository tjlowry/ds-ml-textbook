# Linear Systems

## Overview

A **linear system** `Ax = b` asks: which combination of the columns of `A` produces `b`?
That single question is the spine of the whole chapter — least squares is what you do when
it has *no* exact answer, eigenvectors are special `x` where `Ax` lines up with `x`, and
gradient descent is how you solve it when `A` is too big to factor. This page pins down the
vocabulary (span, basis, rank, the column picture) and the two operations everything downstream
leans on: the **dot product** and **matrix multiplication**.

I reviewed this in MATH 677 Lecture 1 (row reduction and the numerical side of solving
`Ax = b`); the proof-level facts — consistency, span, the Invertible Matrix Theorem — I
first learned in BYU-I MATH 341 and collect in the [theorem reference](theorem-reference.md).

## The column picture

Writing `Ax = b` out by columns is the mental model I keep coming back to:

$$
x_1\mathbf{a}_1 + x_2\mathbf{a}_2 + \dots + x_n\mathbf{a}_n = \mathbf{b}
$$

So `Ax = b` is solvable exactly when `b` lies in the **span of the columns** of `A` (its
column space). Three outcomes, no others:

- **No solution** — `b` is outside the column space (the system is *inconsistent*). This is
  the case that motivates [least squares](least-squares.md).
- **Exactly one** — the columns are linearly independent and `b` is in their span.
- **Infinitely many** — `b` is in the span but the columns are dependent (there are free
  variables).

Which case you are in is read off the pivots after row reduction. The clean summary of all of
this — consistency, independence, invertibility — is the **Invertible Matrix Theorem**, which
I restate in the [theorem reference](theorem-reference.md#invertibility-the-big-equivalence).

## In modern ML

### The dot product is cosine similarity

Every "how similar are these two things?" question in ML is a dot product in disguise. For
unit-normalized vectors, `u · v = cos θ` — the cosine of the angle between them. That is
*exactly* how a retrieval system decides that a query embedding is close to a document
embedding, and how word vectors encode analogy.

![Toy 2-D word embeddings: similar words point in similar directions, so their cosine
similarity is high; unrelated words are near-orthogonal.](img/cosine-similarity-embeddings.png)

Here `king` and `queen` point almost the same way (cosine ≈ 1.0), while `king` and `dog`
are nearly orthogonal (cosine near 0). Scale this from 2-D to 768-D and it is the geometry
behind every embedding search.

### Matrix multiplication is attention

Stack a batch of query vectors into a matrix `Q` and keys into `K`, and the single product
`QKᵀ` computes **every** query-key dot product at once — one number per pair. Softmax the
rows and you have attention weights. This is the core operation in my
[Mini-GPT from scratch](../08-machine-learning/notebooks/mini-gpt-from-scratch.ipynb).

![Causal attention weights: softmax of QKᵀ over the keys, lower-triangular because each
token can only attend to itself and earlier tokens.](img/attention-scores.png)

The lower-triangular shape is the causal mask — token *"sat"* can attend to *"The"*,
*"cat"*, and itself, but not to future words. Every cell is a normalized dot product;
matrix multiplication just does all `n²` of them in one shot.

## Gotchas

- **Consistency is about `b`, dimension is about `A`.** A wide matrix (more unknowns than
  equations) tends toward infinitely many solutions; a tall one (more equations than
  unknowns) tends toward none — hence least squares.
- **Never invert to solve.** `x = A⁻¹b` is a math identity, not an algorithm — forming
  `A⁻¹` is slower and less stable than a factorization (LU/QR) or an iterative solve. MATH
  677 hammered this: solve, don't invert.
- **Dot products need the same basis.** Cosine similarity between two embeddings is only
  meaningful if they came from the *same* model/space — a number falls out regardless, but
  it means nothing across mismatched spaces.

## References

- MATH 677 Lecture 1 — Solving Linear Systems (local:
  `course-files/02-linear-algebra/1+Solving+linear+systems+complete.pdf`).
  Instructor-copyrighted; concept summary only.
- Invertibility, span, and independence theorems: see the
  [theorem reference](theorem-reference.md), re-typeset from my BYU-I MATH 341 theorem list.
