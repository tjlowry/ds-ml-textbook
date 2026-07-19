"""A small decision tree and the rectangular regions it carves.

Left panel: plot_tree of a depth-3 DecisionTreeClassifier fit on two interpretable
iris features (petal length, petal width). Right panel: the same tree's axis-aligned
decision regions in that feature space, with the data overlaid. Illustrates the
page's point that trees split the space into rectangles you can read off directly.

Run:  python make_decision_tree_and_regions.py
Writes: ../decision-tree-and-regions.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree

np.random.seed(0)

PASTEL = ["#BCD8EE", "#F6D5B3", "#CBE6C4"]
EDGE = "#4A4A4A"
TEXT = "#222222"
cmap = ListedColormap(PASTEL)

iris = load_iris()
X = iris.data[:, 2:4]          # petal length, petal width
y = iris.target
names = ["Setosa", "Versicolor", "Virginica"]
fnames = ["petal length", "petal width"]

clf = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X, y)

fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.2))

# Left: the tree itself. Draw uncolored, then tint each node with the SAME
# pastel palette the regions panel uses, so a class reads as one color across
# both panels (sklearn's filled=True uses an unrelated colormap).
annots = plot_tree(clf, ax=axes[0], feature_names=fnames, class_names=names,
                   filled=False, rounded=True, impurity=False, fontsize=8,
                   proportion=False)
node_values = clf.tree_.value  # (n_nodes, 1, n_classes)
for i, ann in enumerate(annots):
    patch = ann.get_bbox_patch()
    patch.set_facecolor(PASTEL[int(np.argmax(node_values[i][0]))])
    patch.set_edgecolor(EDGE)
    patch.set_linewidth(0.7)
axes[0].set_title("Depth-3 decision tree (iris)", fontsize=12,
                  fontweight="bold", color=TEXT)

# Right: the regions it carves.
ax = axes[1]
x_min, x_max = X[:, 0].min() - 0.4, X[:, 0].max() + 0.4
y_min, y_max = X[:, 1].min() - 0.3, X[:, 1].max() + 0.3
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 400),
                     np.linspace(y_min, y_max, 400))
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
ax.contourf(xx, yy, Z, alpha=0.55, cmap=cmap, levels=[-0.5, 0.5, 1.5, 2.5])
for c in range(3):
    m = y == c
    ax.scatter(X[m, 0], X[m, 1], s=34, color=PASTEL[c], edgecolor=EDGE,
               linewidth=0.6, zorder=3, label=names[c])
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_xlabel("petal length (cm)", fontsize=11, color=TEXT)
ax.set_ylabel("petal width (cm)", fontsize=11, color=TEXT)
ax.set_title("The rectangular regions those splits carve", fontsize=12,
             fontweight="bold", color=TEXT)
ax.legend(fontsize=9, loc="upper left", framealpha=0.95)

fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "decision-tree-and-regions.png")
fig.savefig(out, dpi=110, facecolor="white", bbox_inches="tight")
print("wrote", os.path.abspath(out))
