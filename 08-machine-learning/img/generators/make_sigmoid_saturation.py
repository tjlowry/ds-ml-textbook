"""Generate the sigmoid + derivative saturation figure for
deep-learning/neural-network-fundamentals.md.

Plots sigma(z) and its derivative sigma'(z) = sigma(z)(1 - sigma(z)) on one
axis. The saturation regions |z| > 4 are shaded, and the page's worked-example
point z = 4 is marked on both curves. Every annotated number is computed here
and matches the ECEN 758 Assignment 4 hand-derivation on the page:

    sigma(4)  = 0.982
    sigma'(4) = sigma(4)(1 - sigma(4)) = 0.0177   (the "gradient factor")
    that factor shrank the backprop weight update to 0.036 * 0.0177 = 0.00064,
    i.e. about 1 / 0.0177 = 56x smaller than the perceptron rule's 0.036 step.

Run:  python make_sigmoid_saturation.py
Writes: ../sigmoid-saturation.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


z = np.linspace(-8, 8, 801)
s = sigmoid(z)
ds = s * (1 - s)

Z0 = 4.0
s4 = float(sigmoid(Z0))          # 0.9820
ds4 = float(s4 * (1 - s4))       # 0.0177
ratio = 1.0 / ds4                # ~56.6
print(f"sigma(4)={s4:.4f}  sigma'(4)={ds4:.4f}  1/sigma'={ratio:.1f}")
assert round(s4, 3) == 0.982 and round(ds4, 4) == 0.0177

BLUE, ORANGE, GREEN = "#2E6DA4", "#D9822B", "#CBE6C4"
EDGE, TXT, RED = "#4A4A4A", "#222222", "#C0392B"

fig, ax = plt.subplots(figsize=(9.4, 5.6))

# saturation shading |z| > 4
ax.axvspan(-8, -4, color=GREEN, alpha=0.45, lw=0)
ax.axvspan(4, 8, color=GREEN, alpha=0.45, lw=0)
ax.text(-6.0, 0.5, "saturation\n|z| > 4\n(slope → 0)", ha="center", va="center",
        fontsize=9.5, color="#3B6B34", style="italic")
ax.text(6.0, 0.75, "saturation\n|z| > 4\n(slope → 0)", ha="center", va="center",
        fontsize=9.5, color="#3B6B34", style="italic")

# curves
ax.plot(z, s, color=BLUE, lw=2.6, label=r"$\sigma(z)=1/(1+e^{-z})$")
ax.plot(z, ds, color=ORANGE, lw=2.6,
        label=r"$\sigma'(z)=\sigma(z)\,(1-\sigma(z))$")

# reference: max slope 0.25 at z = 0
ax.plot(0, 0.25, "o", color=ORANGE, ms=6, zorder=5)
ax.annotate(r"max slope $\sigma'(0)=0.25$", xy=(0, 0.25), xytext=(-3.4, 0.31),
            fontsize=9.5, color=ORANGE,
            arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.3))

# worked-example markers at z = 4
ax.plot([Z0, Z0], [0, s4], color="#9AA0A6", lw=1.0, ls=(0, (3, 3)), zorder=1)
ax.plot(Z0, s4, "o", color=BLUE, ms=8, zorder=6)
ax.plot(Z0, ds4, "o", color=RED, ms=8, zorder=6)

ax.annotate(rf"$\sigma(4)={s4:.3f}$", xy=(Z0, s4), xytext=(1.0, 0.9),
            fontsize=10.5, color=BLUE, fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.4))

ax.annotate(rf"$\sigma'(4)={ds4:.4f}$" + "\n(tiny slope)",
            xy=(Z0, ds4), xytext=(5.0, 0.20),
            fontsize=10.5, color=RED, fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.4))

# explanatory callout tying to the perceptron-vs-backprop example
ax.text(-7.7, 0.90,
        "Worked example (net input z = 4):\n"
        r"the gradient carries a factor $\sigma'(4)=0.0177$," + "\n"
        "so the backprop update is $0.036\\times0.0177=0.00064$\n"
        r"$\approx 56\times$ smaller than the perceptron step.",
        ha="left", va="top", fontsize=9.5, color=TXT,
        bbox=dict(boxstyle="round,pad=0.5", fc="#F3F3F3", ec="#BFBFBF"))

ax.set_xlim(-8, 8)
ax.set_ylim(0, 1.03)
ax.set_xlabel("pre-activation  z  (= net input)", fontsize=11)
ax.set_ylabel("value", fontsize=11)
ax.set_title("Sigmoid and its derivative: saturation is vanishing-gradient in miniature",
             fontsize=12.5, fontweight="bold", color=TXT)
ax.axhline(0, color="#CCCCCC", lw=0.8)
ax.legend(loc="center right", fontsize=10, framealpha=0.95)
ax.grid(color="#E6E6E6", lw=0.8)
ax.set_axisbelow(True)

fig.patch.set_facecolor("white")
fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "sigmoid-saturation.png")
fig.savefig(out, dpi=110, bbox_inches="tight", facecolor="white")
print("wrote", os.path.abspath(out))
