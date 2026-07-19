"""Two GMM figures for gmm-em.md, both on the shared clustering dataset.

(a) gmm-shared-data.png  — a 5-component GMM fit with EM. Points are colored by
    *soft* assignment (each point's RGB is its responsibility-weighted blend of
    the component colors, so boundary points look muddy), and each component's
    covariance is drawn as a 2-sigma ellipse.

(b) gmm-em-iterations.png — the SAME fit shown after 1, 3, and 10 EM iterations
    (fixed init + seed, warm_start), so you can watch the ellipses tighten onto
    the blobs as the log-likelihood climbs.

These are re-demos built for this page (the course HW implemented EM by hand on a
1-D / three-coin problem, not this 2-D data). Illustrative synthetic demo.

Run:  python make_gmm_figures.py
Writes: ../gmm-shared-data.png, ../gmm-em-iterations.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
from sklearn.mixture import GaussianMixture

from shared_dataset import make_shared_data, PASTELS, EDGE, TEXT, SEED

np.random.seed(SEED)

X, _ = make_shared_data()
K = 5
COL = np.array([matplotlib.colors.to_rgb(PASTELS[i]) for i in range(K)])


def draw_ellipse(ax, mean, cov, color, nsig=2.0, lw=2.0):
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    vals, vecs = vals[order], vecs[:, order]
    angle = np.degrees(np.arctan2(vecs[1, 0], vecs[0, 0]))
    width, height = 2 * nsig * np.sqrt(vals)
    e = Ellipse(mean, width, height, angle=angle, facecolor=color,
                edgecolor=EDGE, lw=lw, alpha=0.28, zorder=1)
    ax.add_patch(e)
    e2 = Ellipse(mean, width, height, angle=angle, facecolor="none",
                 edgecolor=EDGE, lw=lw, zorder=3)
    ax.add_patch(e2)


# ---------- Figure (a): soft-assignment coloring + ellipses ----------
gm = GaussianMixture(n_components=K, covariance_type="full",
                     random_state=SEED, n_init=5).fit(X)
resp = gm.predict_proba(X)                 # (N, K) responsibilities
point_rgb = np.clip(resp @ COL, 0, 1)      # soft blend of component colors

fig, ax = plt.subplots(figsize=(7.0, 5.2))
fig.patch.set_facecolor("white")

for i in range(K):
    draw_ellipse(ax, gm.means_[i], gm.covariances_[i], PASTELS[i])

ax.scatter(X[:, 0], X[:, 1], s=26, c=point_rgb,
           edgecolors=EDGE, linewidths=0.4, zorder=2)
ax.scatter(gm.means_[:, 0], gm.means_[:, 1], marker="+", s=120,
           color=TEXT, linewidths=1.8, zorder=4)

ax.set_title("5-component GMM: soft assignments + 2σ covariance ellipses",
             fontsize=12, fontweight="bold", color=TEXT)
ax.set_xlabel("feature 1", fontsize=10, color=TEXT)
ax.set_ylabel("feature 2", fontsize=10, color=TEXT)
ax.tick_params(labelsize=9)
ax.set_axisbelow(True)
ax.grid(color="#ECECEC", lw=0.7)

fig.tight_layout()
out_a = os.path.join(os.path.dirname(__file__), "..", "gmm-shared-data.png")
fig.savefig(out_a, dpi=110, bbox_inches="tight", facecolor="white")
print("wrote", os.path.abspath(out_a))

# ---------- Figure (b): EM iterations 1, 3, 10 ----------
# A deliberately loose random-from-data init (fixed seed) so the ellipses start
# broad and visibly tighten as EM runs; by iter 10 the fit reaches essentially
# the same optimum k-means-init reaches immediately.
EM_SEED = 11
iters = [1, 3, 10]
fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6), sharex=True, sharey=True)
fig.patch.set_facecolor("white")

for ax, n_it in zip(axes, iters):
    gm_it = GaussianMixture(n_components=K, covariance_type="full",
                            random_state=EM_SEED, init_params="random_from_data",
                            max_iter=n_it, n_init=1, tol=0)
    gm_it.fit(X)
    labels = gm_it.predict(X)
    ll = gm_it.score(X)  # mean log-likelihood per sample

    for i in range(K):
        draw_ellipse(ax, gm_it.means_[i], gm_it.covariances_[i], PASTELS[i])
    for i in range(K):
        m = labels == i
        ax.scatter(X[m, 0], X[m, 1], s=18, color=PASTELS[i],
                   edgecolors=EDGE, linewidths=0.3, zorder=2)
    ax.scatter(gm_it.means_[:, 0], gm_it.means_[:, 1], marker="+", s=90,
               color=TEXT, linewidths=1.6, zorder=4)
    ax.set_title(f"after {n_it} EM iteration{'s' if n_it > 1 else ''}\n"
                 f"(mean log-lik {ll:.2f})", fontsize=11, color=TEXT)
    ax.set_xlabel("feature 1", fontsize=10, color=TEXT)
    ax.tick_params(labelsize=9)
    ax.set_axisbelow(True)
    ax.grid(color="#ECECEC", lw=0.7)

axes[0].set_ylabel("feature 2", fontsize=10, color=TEXT)
fig.suptitle("EM tightening a 5-component GMM onto the blobs "
             "(fixed random init, same seed)",
             fontsize=12.5, fontweight="bold", color=TEXT, y=1.02)

fig.tight_layout()
out_b = os.path.join(os.path.dirname(__file__), "..", "gmm-em-iterations.png")
fig.savefig(out_b, dpi=110, bbox_inches="tight", facecolor="white")
print("wrote", os.path.abspath(out_b))
