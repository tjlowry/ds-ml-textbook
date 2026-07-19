"""Generate the CIFAR-100 accuracy-progression figure for case-study-cifar100.md.

The three numbers are the ones our ECEN 758 group actually reported in the draft
write-ups (CNN_draft2.pdf / ecen758_group_report.pdf): random-forest-on-HOG reached
~22%, the custom CNN's first run reached ~52%, against a 1% random-guess floor for
100 balanced classes. CLIP transfer learning was one of our three approaches but the
draft never reported a number for it, so it is deliberately not plotted here.

Run:  python make_cifar100_accuracy_figure.py
Writes: ../cifar100-accuracy-progression.png
"""
import os
import matplotlib.pyplot as plt

BLUE = "#3f51b5"     # indigo, matches site accent
GREY = "#5f6368"
LIGHT = "#c5cae9"

labels = ["Random guess\n(100 classes)", "Random Forest\n+ HOG features", "Custom CNN\n(first run)"]
acc = [1, 22, 52]
colors = [GREY, LIGHT, BLUE]

fig, ax = plt.subplots(figsize=(7.2, 4.2))
bars = ax.bar(labels, acc, color=colors, edgecolor="white", width=0.62)

for b, v in zip(bars, acc):
    ax.text(b.get_x() + b.get_width() / 2, v + 1.2, f"{v}%",
            ha="center", va="bottom", fontsize=12, fontweight="bold",
            color="#1a237e" if v > 1 else GREY)

ax.set_ylabel("Top-1 accuracy on CIFAR-100", fontsize=11)
ax.set_ylim(0, 60)
ax.set_title("Climbing accuracy across our three-step CIFAR-100 progression",
             fontsize=12, fontweight="bold", color="#1a237e")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="x", length=0)
ax.grid(axis="y", color="#e0e0e0", lw=0.8)
ax.set_axisbelow(True)

fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "cifar100-accuracy-progression.png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print("wrote", os.path.abspath(out))
