"""Single deep tree vs a 200-tree random forest on the same noisy 2-D data.

Synthetic demo (make_moons with noise, seeded) -- NOT from Tyler's coursework.
Visualizes the page's variance-reduction story: one unconstrained tree draws a
brittle, islanded boundary that chases noise; averaging 200 bootstrapped trees
smooths it into a more stable decision surface.

Run:  python make_rf_tree_vs_forest.py
Writes: ../rf-tree-vs-forest.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.datasets import make_moons
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

np.random.seed(0)

PASTEL = ["#BCD8EE", "#F6D5B3"]
EDGE = "#4A4A4A"
TEXT = "#222222"
cmap = ListedColormap(PASTEL)

X, y = make_moons(n_samples=260, noise=0.26, random_state=0)

x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 400),
                     np.linspace(y_min, y_max, 400))
grid = np.c_[xx.ravel(), yy.ravel()]

models = [
    ("Single deep tree  (brittle boundary)",
     DecisionTreeClassifier(random_state=0)),
    ("Random forest, 200 trees  (smoother boundary)",
     RandomForestClassifier(n_estimators=200, random_state=0)),
]

fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.9), sharey=True)
for ax, (title, model) in zip(axes, models):
    model.fit(X, y)
    Z = model.predict(grid).reshape(xx.shape)
    ax.contourf(xx, yy, Z, alpha=0.55, cmap=cmap, levels=[-0.5, 0.5, 1.5])
    for c in range(2):
        m = y == c
        ax.scatter(X[m, 0], X[m, 1], s=26, color=PASTEL[c], edgecolor=EDGE,
                   linewidth=0.6, zorder=3, label=f"class {c}")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("feature 1", fontsize=11, color=TEXT)
    ax.set_title(title, fontsize=11.5, fontweight="bold", color=TEXT)

axes[0].set_ylabel("feature 2", fontsize=11, color=TEXT)
axes[0].legend(fontsize=9, loc="lower right", framealpha=0.95)
fig.suptitle("Bagging trades one brittle boundary for a smoother averaged one "
             "(synthetic two-moons data)",
             fontsize=12.5, fontweight="bold", color=TEXT, y=1.02)

fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "rf-tree-vs-forest.png")
fig.savefig(out, dpi=110, facecolor="white", bbox_inches="tight")
print("wrote", os.path.abspath(out))
