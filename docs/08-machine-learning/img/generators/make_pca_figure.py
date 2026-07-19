"""Two-panel PCA figure for pca.md.

Left:  a seeded correlated 2-D Gaussian point cloud with the two principal axes
       drawn as arrows from the mean, each scaled to sqrt(explained variance)
       (so the long arrow is PC1, the maximum-variance direction).
Right: the explained-variance-ratio scree/bar plot from PCA on the 4-feature
       iris dataset (stated in the caption), showing how quickly the variance is
       captured by the first component or two.

Illustrative synthetic demo (left) + a standard library dataset (right); not
coursework results.

Run:  python make_pca_figure.py
Writes: ../pca-axes-and-scree.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris

BLUE = "#BCD8EE"
GREEN_ACCENT = "#1E7A34"
RED_ACCENT = "#C0392B"
EDGE = "#4A4A4A"
TEXT = "#222222"
SEED = 7

np.random.seed(SEED)

# ---------- Left: correlated 2-D Gaussian + principal axes ----------
mean = np.array([0.0, 0.0])
cov = np.array([[3.0, 2.1],
                [2.1, 2.0]])          # positively correlated
rng = np.random.RandomState(SEED)
pts = rng.multivariate_normal(mean, cov, size=350)

pca = PCA(n_components=2).fit(pts)
center = pts.mean(axis=0)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.5, 5.0))
fig.patch.set_facecolor("white")

axL.scatter(pts[:, 0], pts[:, 1], s=22, color=BLUE,
            edgecolors=EDGE, linewidths=0.35, zorder=1)

arrow_colors = [RED_ACCENT, GREEN_ACCENT]
for i in range(2):
    vec = pca.components_[i]
    length = np.sqrt(pca.explained_variance_[i])   # sqrt(variance) along axis
    tip = center + vec * length * 2.4              # 2.4 = visual scale factor
    axL.annotate("", xy=tip, xytext=center,
                 arrowprops=dict(arrowstyle="-|>", color=arrow_colors[i],
                                 lw=2.6, shrinkA=0, shrinkB=0), zorder=5)
    axL.text(*(center + vec * length * 2.4 * 1.08),
             f"PC{i + 1}\n({pca.explained_variance_ratio_[i] * 100:.0f}% var)",
             color=arrow_colors[i], fontsize=9.5, fontweight="bold",
             ha="center", va="center")

axL.set_aspect("equal")
axL.set_title("Principal axes of a correlated 2-D Gaussian",
              fontsize=12, fontweight="bold", color=TEXT)
axL.set_xlabel("feature 1", fontsize=10, color=TEXT)
axL.set_ylabel("feature 2", fontsize=10, color=TEXT)
axL.tick_params(labelsize=9)
axL.set_axisbelow(True)
axL.grid(color="#ECECEC", lw=0.7)

# ---------- Right: scree / explained-variance bars on iris (4 features) ----------
iris = load_iris()
pca_iris = PCA().fit(iris.data)          # 4 components
evr = pca_iris.explained_variance_ratio_
comps = np.arange(1, len(evr) + 1)

bars = axR.bar(comps, evr * 100, color=BLUE, edgecolor=EDGE, width=0.6,
               label="individual")
axR.plot(comps, np.cumsum(evr) * 100, marker="o", color=GREEN_ACCENT,
         lw=2.0, label="cumulative")
for b, v in zip(bars, evr * 100):
    axR.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v:.0f}%",
             ha="center", va="bottom", fontsize=9, color=TEXT)

axR.set_title("Explained-variance ratio — PCA on iris (4 features)",
              fontsize=12, fontweight="bold", color=TEXT)
axR.set_xlabel("principal component", fontsize=10, color=TEXT)
axR.set_ylabel("variance explained (%)", fontsize=10, color=TEXT)
axR.set_xticks(comps)
axR.set_ylim(0, 108)
axR.tick_params(labelsize=9)
axR.legend(loc="center right", fontsize=9, framealpha=0.9)
axR.set_axisbelow(True)
axR.grid(axis="y", color="#ECECEC", lw=0.7)

fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "pca-axes-and-scree.png")
fig.savefig(out, dpi=110, bbox_inches="tight", facecolor="white")
print("wrote", os.path.abspath(out))
print("iris EVR:", np.round(evr, 3), "cumulative:", np.round(np.cumsum(evr), 3))
