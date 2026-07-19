# Recommender Systems

## Overview

A **recommender system** predicts how much a user will like an item they haven't seen, from
past interactions. The two classic families are **collaborative filtering** (learn from the
user–item interaction matrix — users who agreed before will agree again) and
**content-based** filtering (recommend items similar to ones the user liked, using item
features). Modern systems, including mine, blend both and often factor the interaction
matrix into latent user/item embeddings.

That factoring is the heart of the collaborative-filtering family: approximate the sparse
user×item ratings matrix $R$ as a product $U V^{T}$ of low-rank latent factors, then read a
missing rating straight off the dot product of a user row and an item column. The schematic
below works one such prediction end to end — every number is self-consistent, so the
highlighted empty cell's value is exactly the dot product of the highlighted factors.

![Matrix-factorization schematic: a 6×5 user×item ratings grid with several observed integer
ratings and grey missing cells, approximated by U (6×2 latent user factors) times Vᵀ (2×5
latent item factors). The missing User 5 × Item 3 cell is predicted as the dot product of the
highlighted U row (1.2, 1.2) and Vᵀ column (1.5, 1.4): (1.2)(1.5) + (1.2)(1.4) =
3.48.](../img/matrix-factorization.png)

I studied recommenders in ECEN 758 (Lectures 15–16) and built a full hybrid recommender as
a personal project: an NFL-draft prospect recommender that treats GMs/coaches as "users" and
draft prospects as "items."

## How I did it

The project (`~/Projects/personal/nfl_prospect_recommender/`, a structured Python repo with
its own [GitHub remote](https://github.com/tjlowry/nfl_prospect_recommender)) frames the
draft as implicit-feedback collaborative filtering: draft picks are positive signals
weighted by round (a 1st-round pick = high confidence, a 7th-round pick = low). It ensembles
several models — an implicit-feedback matrix factorization, an NMF model, and a Bayesian
model — and weights them by their cross-validated precision.

**Ensemble weighting** — each model's weight is proportional to its cross-validated
Precision@5, normalized to sum to 1:

```python
def compute_ensemble_weights(cv_precision: dict[str, float]) -> dict[str, float]:
    """Weights proportional to each model's Precision@5; sum to 1.0."""
    total = sum(max(v, 0.0) for v in cv_precision.values())
    if total == 0:
        return {k: 1.0 / len(cv_precision) for k in cv_precision}
    return {k: max(v, 0.0) / total for k, v in cv_precision.items()}
```

Source: `~/Projects/personal/nfl_prospect_recommender/src/models/ensemble.py`

**GM-to-GM similarity** combines cosine similarity on the learned latent factors with a
Jaccard similarity on binarized draft patterns (`CosineJ = cosine × Jaccard`) — a
content-plus-collaborative hybrid so two GMs count as similar only if they're close in
*both* latent space and actual pick overlap:

```python
from sklearn.metrics.pairwise import cosine_similarity

def compute_cosine_matrix(result):
    return cosine_similarity(result.user_factors)   # cosine on ALS user embeddings
```

Source: `~/Projects/personal/nfl_prospect_recommender/src/similarity/gm_similarity.py`

The project's signature idea is **coaching-tree inheritance**: a new GM with little draft
history inherits preference priors from their coaching/scouting-tree mentors, and Bayesian
updating gradually shifts weight to their own picks as they accumulate.

## Course notebook

The ECEN 758 Lecture 15 (Recommendation Systems I) slides link a worked MovieLens
recommender:
<https://github.com/risitadas/Recommendation-System-on-MovieLens-Dataset> (URL extracted
from the lecture PDF).

## Gotchas

- **Implicit feedback isn't a rating.** A draft pick means "chosen," not "liked on a 1–5
  scale" — you model *confidence* (weighted by round), and the absence of a pick is weak
  negative signal, not a hard zero.
- **Cold start is the real problem.** A brand-new GM has almost no interactions; the
  coaching-tree prior exists specifically to give the model something to go on until real
  data accumulates.
- **Evaluate with ranking metrics, time-aware.** Precision@K under leave-one-year-out CV
  (not a random split) is what drives the ensemble weights — a random split would leak
  future drafts into the past.
- **Weight models by measured skill, not by hand.** Tying ensemble weights to CV Precision@5
  keeps a weak model from dragging the blend down.

## References

- ECEN 758 Lectures 15–16 — Recommendation Systems I & II (local:
  `course-files/08-machine-learning/758 Lec 15 Recommendation Systems I.pdf`,
  `758 Lec 16 Recommendation Systems II.pdf`). Instructor-copyrighted; concept summary only.
