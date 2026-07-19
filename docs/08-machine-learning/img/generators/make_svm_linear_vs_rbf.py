"""Linear vs RBF SVM decision regions on the same two iris features.

Illustrative re-demo for the picture: this refits SVC(kernel="linear") and
SVC(kernel="rbf", gamma="scale") on petal length vs sepal width so the decision
regions can be drawn. These SVC estimators use one-vs-one under the hood (not the
LinearSVC one-vs-rest fit whose coefficients the page tabulates) -- the figure is
here to contrast straight vs curved boundaries, not to reproduce the assignment's
exact model.

Run:  python make_svm_linear_vs_rbf.py
Writes: ../svm-linear-vs-rbf.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.datasets import load_iris
from sklearn.svm import SVC

np.random.seed(0)

PASTEL = ["#BCD8EE", "#F6D5B3", "#CBE6C4"]
EDGE = "#4A4A4A"
TEXT = "#222222"
cmap = ListedColormap(PASTEL)

iris = load_iris()
X = np.column_stack([iris.data[:, 2], iris.data[:, 1]])  # petal length, sepal width
y = iris.target
names = ["Setosa", "Versicolor", "Virginica"]

x_min, x_max = X[:, 0].min() - 0.4, X[:, 0].max() + 0.4
y_min, y_max = X[:, 1].min() - 0.4, X[:, 1].max() + 0.4
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 400),
                     np.linspace(y_min, y_max, 400))
grid = np.c_[xx.ravel(), yy.ravel()]

fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.9), sharey=True)
models = [
    ("Linear kernel  (straight boundaries)", SVC(kernel="linear", random_state=0)),
    ('RBF kernel, gamma="scale"  (curved boundaries)',
     SVC(kernel="rbf", gamma="scale", random_state=0)),
]

for ax, (title, model) in zip(axes, models):
    model.fit(X, y)
    Z = model.predict(grid).reshape(xx.shape)
    ax.contourf(xx, yy, Z, alpha=0.55, cmap=cmap, levels=[-0.5, 0.5, 1.5, 2.5])
    for c in range(3):
        m = y == c
        ax.scatter(X[m, 0], X[m, 1], s=34, color=PASTEL[c], edgecolor=EDGE,
                   linewidth=0.6, label=names[c], zorder=3)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("Petal length (cm)", fontsize=11, color=TEXT)
    ax.set_title(title, fontsize=11, fontweight="bold", color=TEXT)

axes[0].set_ylabel("Sepal width (cm)", fontsize=11, color=TEXT)
axes[0].legend(fontsize=9, loc="upper right", framealpha=0.95)
fig.suptitle("Same iris features, two kernels: SVC decision regions (one-vs-one fit)",
             fontsize=12.5, fontweight="bold", color=TEXT, y=1.02)

fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "svm-linear-vs-rbf.png")
fig.savefig(out, dpi=110, facecolor="white", bbox_inches="tight")
print("wrote", os.path.abspath(out))
