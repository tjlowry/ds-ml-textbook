"""SVM one-vs-rest hyperplanes on iris (petal length vs sepal width).

Draws the three linear-kernel decision boundaries DIRECTLY from the fitted
coefficients reported in the svm.md worked-example table (ECEN 758 Assignment 4):

    Class       w1(petal len)  w2(sepal wid)  w0(bias)
    Setosa        -1.226          0.669         1.056
    Versicolor    -0.687          0.238         1.497
    Virginica     -3.333          0.952        13.475

Each boundary is  w1*x1 + w2*x2 + w0 = 0, i.e.  x2 = -(w1*x1 + w0)/w2.
No model is refit here on purpose: plotting the table's own numbers guarantees
the figure matches the page.

Run:  python make_svm_ovr_hyperplanes.py
Writes: ../svm-ovr-hyperplanes.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

np.random.seed(0)

# Pastel category fills + strong edge/text colors (house palette).
PASTEL = ["#BCD8EE", "#F6D5B3", "#CBE6C4"]   # setosa, versicolor, virginica
LINE = ["#2C6E9B", "#C0392B", "#1E7A34"]     # boundary line colors
EDGE = "#4A4A4A"
TEXT = "#222222"

iris = load_iris()
# feature order: [sepal length, sepal width, petal length, petal width]
x1 = iris.data[:, 2]   # petal length
x2 = iris.data[:, 1]   # sepal width
y = iris.target
names = ["Setosa", "Versicolor", "Virginica"]

# Published fitted coefficients (from the svm.md table).
coefs = {
    "Setosa":     (-1.226, 0.669, 1.056),
    "Versicolor": (-0.687, 0.238, 1.497),
    "Virginica":  (-3.333, 0.952, 13.475),
}

fig, ax = plt.subplots(figsize=(8.8, 5.2))

for c in range(3):
    m = y == c
    ax.scatter(x1[m], x2[m], s=42, color=PASTEL[c], edgecolor=EDGE,
               linewidth=0.6, label=names[c], zorder=3)

xs = np.linspace(x1.min() - 0.3, x1.max() + 0.3, 200)
for c, name in enumerate(names):
    w1, w2, w0 = coefs[name]
    ys = -(w1 * xs + w0) / w2
    ax.plot(xs, ys, color=LINE[c], lw=2.2, zorder=2,
            label=f"{name}-vs-rest boundary")

ax.set_xlim(x1.min() - 0.3, x1.max() + 0.3)
ax.set_ylim(x2.min() - 0.3, x2.max() + 0.3)
ax.set_xlabel("Petal length  $x_1$ (cm)", fontsize=11, color=TEXT)
ax.set_ylabel("Sepal width  $x_2$ (cm)", fontsize=11, color=TEXT)
ax.set_title("One-vs-rest linear SVM boundaries, drawn from the fitted coefficients",
             fontsize=12, fontweight="bold", color=TEXT)
ax.legend(fontsize=9, loc="center left", bbox_to_anchor=(1.01, 0.5),
          framealpha=0.95)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(color="#e6e6e6", lw=0.8)
ax.set_axisbelow(True)

fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "svm-ovr-hyperplanes.png")
fig.savefig(out, dpi=110, facecolor="white", bbox_inches="tight")
print("wrote", os.path.abspath(out))
