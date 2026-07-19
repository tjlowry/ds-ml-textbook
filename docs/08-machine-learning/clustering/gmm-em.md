# Gaussian Mixture Models & EM

## Overview

A **Gaussian Mixture Model (GMM)** treats the data as coming from a weighted sum of several
Gaussians, each with its own mean, covariance, and mixing weight. Unlike k-means' hard
assignments, a GMM gives *soft* responsibilities — the probability each point belongs to
each component — which makes it a probabilistic, softer generalization of k-means. You fit
it with **Expectation-Maximization (EM)**: alternate between the **E-step** (compute
responsibilities given current parameters) and the **M-step** (re-estimate parameters
weighted by those responsibilities), climbing the log-likelihood each round.

Those two ideas — soft responsibilities and per-component covariance — are what a
GMM adds over k-means. On the same synthetic dataset used across this chapter, a
5-component GMM colors each point by its *soft* blend of component memberships
(boundary points look muddy) and fits a full covariance ellipse per component. It
wraps the three blobs tightly and stretches two broad Gaussians over the moon
region — a reminder that a mixture of Gaussians still models convex components:

![Five-component Gaussian mixture on the shared synthetic dataset: points colored by their soft responsibility-weighted blend of component colors, with a two-sigma covariance ellipse drawn for each of the five components, three tight ellipses over the Gaussian blobs and two large elongated ellipses spanning the two moons](../img/gmm-shared-data.png)

The EM fit itself is iterative. Starting from a deliberately loose random
initialization, the panels below show the same 5-component model after 1, 3, and
10 EM iterations (fixed seed): the ellipses start broad and overlapping, then
tighten onto the blobs as the mean log-likelihood climbs toward its optimum.

![Three-panel figure showing EM refining a five-component GMM after 1, 3, and 10 iterations from a fixed random initialization: the covariance ellipses begin large and overlapping and progressively tighten onto the three Gaussian blobs, with the mean log-likelihood rising from about -4.13 to -3.79 across the panels](../img/gmm-em-iterations.png)

*Both are re-demos built for this page — the ECEN 758 homework implemented EM
by hand on a 1-D three-coin problem, not this 2-D data.*

This is the topic I understand best in the chapter, because ECEN 758 HW 2 had me implement
EM *by hand* — no `sklearn.mixture.GaussianMixture`, just the update equations.

## How I did it

**The mixture log-likelihood** of a two-component 1-D Gaussian mixture, summed over the data:

```python
from scipy.stats import norm

log_likelihood = 0
for x in D:
    mixture_density = pi1 * norm.pdf(x, mu1, sigma1) + pi2 * norm.pdf(x, mu2, sigma2)
    log_likelihood += np.log(mixture_density)
```

**The E-step** — each point's posterior responsibility for each component:

```python
for j in range(n):
    likelihood_C1 = norm.pdf(D[j], mu1, sigma1) * pi1
    likelihood_C2 = norm.pdf(D[j], mu2, sigma2) * pi2
    total = likelihood_C1 + likelihood_C2
    w[j, 0] = likelihood_C1 / total     # responsibility of component 1
    w[j, 1] = likelihood_C2 / total
```

**The M-step** — re-estimate means, variances, and mixing weights, each weighted by the
responsibilities from the E-step:

```python
mu1_new    = np.sum(w[:, 0] * D) / np.sum(w[:, 0])
sigma1_new = np.sqrt(np.sum(w[:, 0] * (D - mu1_new)**2) / np.sum(w[:, 0]))
pi1_new    = np.sum(w[:, 0]) / n
```

Source: `course-files/appendix/Homework/ecen758_hw/HW 2/hw2.ipynb`

The homework then wraps the same E/M logic into a full loop for the classic **three-coin**
latent-variable problem and runs it from two different initializations to show it converges
to the same place — the promoted notebook plots both trajectories.

## Notebook

See the rendered notebook: [GMM & EM From Scratch](../notebooks/gmm-em-from-scratch.ipynb) —
the log-likelihood, one manual E-step/M-step, and the full three-coin EM loop, re-executed
locally.

Re-run locally: `jupyter lab docs/08-machine-learning/notebooks/gmm-em-from-scratch.ipynb`

## Course notebook

ECEN 758 Lectures 8–9 (GMM / EM) both link the *Python Data Science Handbook* GMM notebook:
<https://colab.research.google.com/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/05.12-Gaussian-Mixtures.ipynb>
(URL extracted from the lecture PDFs).

## Gotchas

- **Doing the E/M split by hand is what makes it click.** The single most valuable part was
  writing the responsibility normalization (`likelihood / total`) and the weighted
  parameter updates myself — the `sklearn` call hides exactly the part worth understanding.
- **EM finds a local optimum.** The log-likelihood only ever goes up, but *which* peak
  depends on initialization — hence running the three-coin problem from two starts.
- **Watch for degenerate variances.** A component can collapse onto a single point
  (`sigma → 0`, likelihood → ∞). Real implementations add a small floor / regularization to
  the covariance.
- **Soft beats hard when clusters overlap.** GMM's responsibilities express uncertainty near
  boundaries where k-means would force an arbitrary hard call.

## References

- ECEN 758 Lecture 8 — Gaussian Mixture Models; Lecture 9 — EM Algorithm (local:
  `course-files/08-machine-learning/758 Lec 08 Gaussian Mixture Models (1).pdf`,
  `758 Lec 09 EM Algorithm (1).pdf`). Instructor-copyrighted; concept summary only.
