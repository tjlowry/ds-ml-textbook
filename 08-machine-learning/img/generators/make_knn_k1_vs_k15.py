"""kNN decision boundaries at k=1 vs k=15 on the same synthetic 2-class data.

Synthetic demo (make_moons with noise, seeded) -- NOT from Tyler's coursework.
Shows the bias-variance dial the page describes: k=1 memorizes every point into a
jagged, overfit boundary; k=15 averages more neighbors into a smooth one.

Run:  python make_knn_k1_vs_k15.py
Writes: ../knn-k1-vs-k15.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.datasets import make_moons
from sklearn.neighbors import KNeighborsClassifier

np.random.seed(0)

PASTEL = ["#BCD8EE", "#F6D5B3"]
EDGE = "#4A4A4A"
TEXT = "#222222"
cmap = ListedColormap(PASTEL)

X, y = make_moons(n_samples=220, noise=0.30, random_state=0)

x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 400),
                     np.linspace(y_min, y_max, 400))
grid = np.c_[xx.ravel(), yy.ravel()]

fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.9), sharey=True)
for ax, k, tag in zip(axes, [1, 15],
                      ["k = 1  (jagged, overfit)", "k = 15  (smooth, generalizes)"]):
    clf = KNeighborsClassifier(n_neighbors=k).fit(X, y)
    Z = clf.predict(grid).reshape(xx.shape)
    ax.contourf(xx, yy, Z, alpha=0.55, cmap=cmap, levels=[-0.5, 0.5, 1.5])
    for c in range(2):
        m = y == c
        ax.scatter(X[m, 0], X[m, 1], s=28, color=PASTEL[c], edgecolor=EDGE,
                   linewidth=0.6, zorder=3, label=f"class {c}")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("feature 1", fontsize=11, color=TEXT)
    ax.set_title(tag, fontsize=11.5, fontweight="bold", color=TEXT)

axes[0].set_ylabel("feature 2", fontsize=11, color=TEXT)
axes[0].legend(fontsize=9, loc="lower right", framealpha=0.95)
fig.suptitle("Choosing k trades variance for bias (synthetic two-moons data)",
             fontsize=12.5, fontweight="bold", color=TEXT, y=1.02)

fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "knn-k1-vs-k15.png")
fig.savefig(out, dpi=110, facecolor="white", bbox_inches="tight")
print("wrote", os.path.abspath(out))
