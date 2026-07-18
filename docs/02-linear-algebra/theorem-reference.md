# Theorem Reference

A compact index of the linear-algebra theorems I lean on most, re-typeset in my own wording and
organized by topic. The statements are mathematical facts; the phrasing, grouping, and layout
here are my own. Cross-linked from the topic pages.

*Source: from my BYU-I M341 theorem list (local:
`course-files/02-linear-algebra/Theorem list.pdf`). This is the proof-based first course I took
at BYU-Idaho; the same facts carried straight into MATH 677 at Texas A&M.*

---

## Linear systems and their solutions

- **Unique reduced form.** Every matrix is row-equivalent to exactly one matrix in reduced
  row-echelon form.
- **Consistency.** `Ax = b` is consistent iff no row of an echelon form of the augmented matrix
  reads `[0 … 0 | b]` with `b ≠ 0`. A consistent system has either a unique solution (no free
  variables) or infinitely many (at least one free variable).
- **Three equivalent readings of `Ax = b`.** The matrix equation `Ax = b`, the vector equation
  `x₁a₁ + … + xₙaₙ = b`, and the augmented system `[a₁ … aₙ | b]` all have the same solution set.
- **Solution set structure.** If `Ax = b` is consistent with a particular solution `p`, its full
  solution set is `{p + v_h}`, where `v_h` ranges over all solutions of the homogeneous system
  `Ax = 0`.

## Linear independence and bases

- **Dependence via combinations.** A set of two or more vectors is linearly dependent iff at
  least one vector is a linear combination of the others.
- **Too many vectors.** Any set of more than `n` vectors in `ℝⁿ` is automatically linearly
  dependent. A set containing the zero vector is always dependent.
- **Unique coordinates.** If `𝔅 = {b₁, …, bₙ}` is a basis for `V`, every `x ∈ V` has *exactly
  one* representation `x = c₁b₁ + … + cₙbₙ`. The coordinate map `x ↦ [x]_𝔅` is a one-to-one
  linear map onto `ℝⁿ`.
- **Basis size is fixed.** Any two bases of a finite-dimensional space have the same number of
  vectors (the dimension). In a `p`-dimensional space, any independent set of `p` vectors — or
  any spanning set of `p` vectors — is automatically a basis.

## Invertibility — the big equivalence

The **Invertible Matrix Theorem**: for a square `n × n` matrix `A`, the following are either all
true or all false. This is the single most useful theorem in the subject — it ties together
solving, independence, rank, and eigenvalues.

- `A` is invertible.
- `A` is row-equivalent to `Iₙ`; it has `n` pivot positions.
- `Ax = 0` has only the trivial solution; the columns of `A` are linearly independent.
- `Ax = b` has a (unique) solution for every `b`; the columns span `ℝⁿ` and form a basis.
- The map `x ↦ Ax` is one-to-one and onto.
- `Col A = ℝⁿ`, `rank A = n`, `dim Nul A = 0`.
- `det A ≠ 0`, and `0` is **not** an eigenvalue of `A`.
- `Aᵀ` is invertible.

Related identities: `(A⁻¹)⁻¹ = A`, `(AB)⁻¹ = B⁻¹A⁻¹` (reverse order), `(Aᵀ)⁻¹ = (A⁻¹)ᵀ`. For a
`2 × 2` matrix, `A⁻¹ = 1/(ad − bc) · [[d, −b], [−c, a]]`, invertible iff `ad − bc ≠ 0`.

## Determinants

- **Cofactor expansion** along any row or column computes `det A`.
- **Triangular shortcut.** For a triangular (or diagonal) matrix, `det A` is the product of the
  diagonal entries.
- **Row operations.** Row replacement leaves the determinant unchanged; a row swap flips its
  sign; scaling a row by `k` scales it by `k`.
- **Key identities.** `det Aᵀ = det A`, `det(AB) = (det A)(det B)`, and `A` is invertible iff
  `det A ≠ 0`.

## Subspaces, rank, and dimension

- `Span{v₁, …, v_p}` is always a subspace. So is the null space `Nul A` (a subspace of `ℝⁿ`) and
  the column space `Col A` (a subspace of `ℝᵐ`).
- **Pivot columns of `A` form a basis for `Col A`.**
- **Rank theorem.** `rank A + dim Nul A = n`, where `rank A = dim Col A = dim Row A` equals the
  number of pivot positions.

## Orthogonality, projection, and least squares

- **Dot-product rules.** `u·v = v·u`, distributes over addition, pulls out scalars, and
  `u·u ≥ 0` with equality iff `u = 0`. Vectors are orthogonal iff `‖u + v‖² = ‖u‖² + ‖v‖²`
  (Pythagoras).
- **Orthogonal complements.** `(Row A)^⊥ = Nul A` and `(Col A)^⊥ = Nul Aᵀ`.
- **Orthogonal projection.** Every `y ∈ ℝⁿ` splits uniquely as `y = ŷ + z` with `ŷ` in the
  subspace `W` and `z ⊥ W`. The projection `ŷ` is the **closest point** in `W` to `y`
  (`‖y − ŷ‖ < ‖y − v‖` for all other `v ∈ W`). With an orthonormal basis `U` for `W`,
  `proj_W y = UUᵀy`.
- **Gram-Schmidt** turns any basis of `W` into an orthogonal one; combined with normalization it
  produces the **`A = QR`** factorization (`Q` orthonormal columns, `R` upper-triangular).
- **Least squares (normal equations).** The least-squares solutions of `Ax = b` are exactly the
  solutions of `AᵀAx = Aᵀb`. If the columns of `A` are independent, `AᵀA` is invertible and the
  solution is unique, `x̂ = (AᵀA)⁻¹Aᵀb` — or, more stably, `x̂ = R⁻¹Qᵀb` from the QR
  factorization.
- **Cauchy-Schwarz & triangle inequalities.** `|⟨u, v⟩| ≤ ‖u‖‖v‖` and `‖u + v‖ ≤ ‖u‖ + ‖v‖`.

Used on the [least squares](least-squares.md) page.

## Eigenvalues and diagonalization

- **Triangular eigenvalues.** The eigenvalues of a triangular matrix are its diagonal entries.
- **Independence.** Eigenvectors for *distinct* eigenvalues are linearly independent.
- **Similar matrices** share the same characteristic polynomial, hence the same eigenvalues (with
  multiplicities).
- **Diagonalization.** An `n × n` matrix is diagonalizable iff it has `n` independent eigenvectors;
  then `A = PDP⁻¹` with the eigenvectors as columns of `P` and eigenvalues on `D`. In particular,
  `n` distinct eigenvalues ⇒ diagonalizable.
- **Geometric ≤ algebraic multiplicity.** The dimension of each eigenspace is at most the
  multiplicity of its eigenvalue; `A` is diagonalizable iff the eigenspace dimensions sum to `n`.

Used on the [eigenvalues & eigenvectors](eigenvalues-eigenvectors.md) page.

## Markov chains and steady state

- **Regular stochastic convergence.** If `P` is a regular stochastic matrix, it has a unique
  steady-state vector `q` (with `Pq = q`), and for *any* initial state `x₀` the chain
  `x_{k+1} = P x_k` converges to `q` as `k → ∞`.

This is the finite-state cousin of the [Perron-Frobenius](perron-frobenius.md) result and the
foundation of PageRank.
