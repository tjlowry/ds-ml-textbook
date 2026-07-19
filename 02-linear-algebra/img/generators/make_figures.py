"""Generate all figures for the Linear Algebra chapter.

These are OUR OWN remakes of key concepts (never screenshots of lecture slides).
Styling follows the repo's dataviz skill: a validated categorical palette, thin
recessive grid/axes, direct labels, legend only for >=2 series.

Run:  python3 docs/02-linear-algebra/img/generators/make_figures.py
Output PNGs land in docs/02-linear-algebra/img/ at dpi 110.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, FancyArrow

# ---- dataviz palette (validated categorical slots + chrome) -----------------
BLUE, GREEN, MAGENTA, YELLOW = "#2a78d6", "#008300", "#e87ba4", "#eda100"
AQUA, ORANGE, VIOLET, RED = "#1baf7a", "#eb6834", "#4a3aa7", "#e34948"
SURFACE, INK, SECOND, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 11, "axes.titlesize": 12, "axes.labelsize": 11,
    "text.color": INK, "axes.labelcolor": INK, "axes.titlecolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.edgecolor": "#c3c2b7", "axes.linewidth": 0.8,
    "grid.color": GRID, "grid.linewidth": 0.8,
    "legend.frameon": False, "figure.dpi": 110, "savefig.dpi": 110,
})

OUT = os.path.join(os.path.dirname(__file__), "..")
def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"  {name}: {os.path.getsize(p)//1024} KB")

def clean(ax, grid=True):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if grid:
        ax.grid(True, alpha=0.6)
    ax.set_axisbelow(True)


# 1. Least squares: projection onto the column space + residual ---------------
def fig_ls_projection():
    from mpl_toolkits.mplot3d import Axes3D  # noqa
    fig = plt.figure(figsize=(7, 4.6))
    ax = fig.add_subplot(111, projection="3d")
    # column space = plane spanned by a1, a2
    a1, a2 = np.array([1.6, 0.2, 0.0]), np.array([0.2, 1.5, 0.0])
    gs = np.linspace(-1, 1, 2)
    S, T = np.meshgrid(gs, gs)
    P = S[..., None] * a1 + T[..., None] * a2
    ax.plot_surface(P[..., 0], P[..., 1], P[..., 2], alpha=0.16,
                    color=BLUE, edgecolor=BLUE, linewidth=0.3)
    b = np.array([0.9, 0.7, 1.25])       # target, off the plane
    bhat = np.array([0.9, 0.7, 0.0])     # orthogonal projection onto plane
    ax.quiver(0, 0, 0, *b, color=RED, lw=2.2, arrow_length_ratio=0.09)
    ax.quiver(0, 0, 0, *bhat, color=GREEN, lw=2.2, arrow_length_ratio=0.12)
    ax.plot(*zip(bhat, b), color=MUTED, lw=1.8, ls="--")
    ax.text(*b, r"  $\mathbf{b}$", color=RED, fontsize=12)
    ax.text(bhat[0], bhat[1], bhat[2] - 0.18, r"$\hat{\mathbf{b}}=A\hat{\mathbf{x}}$",
            color=GREEN, fontsize=11)
    ax.text(0.95, 0.72, 0.62, r"$\mathbf{b}-\hat{\mathbf{b}}$", color=SECOND, fontsize=11)
    ax.text(-0.9, -0.9, 0.03, r"Col $A$", color=BLUE, fontsize=11)
    ax.set_title("Least squares = drop a perpendicular onto the column space")
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.set_box_aspect((1, 1, 0.8))
    ax.view_init(elev=18, azim=-60)
    ax.xaxis.pane.set_alpha(0); ax.yaxis.pane.set_alpha(0); ax.zaxis.pane.set_alpha(0)
    save(fig, "least-squares-projection.png")


# 2. Regression residuals (modern-ML: boosting fits the residual) -------------
def fig_residuals():
    rng = np.random.default_rng(7)
    x = np.linspace(0, 10, 22)
    y = 1.1 * x + 2 + rng.normal(0, 2.2, x.size)
    b1, b0 = np.polyfit(x, y, 1)
    yhat = b0 + b1 * x
    fig, ax = plt.subplots(figsize=(7, 4.4))
    clean(ax)
    for xi, yi, yh in zip(x, y, yhat):
        ax.plot([xi, xi], [yi, yh], color=ORANGE, lw=1.4, alpha=0.8, zorder=1)
    ax.scatter(x, y, s=34, color=BLUE, zorder=3, label="observations")
    ax.plot(x, yhat, color=INK, lw=2, zorder=2, label="least-squares fit")
    ax.plot([], [], color=ORANGE, lw=1.6, label="residual $y-\\hat{y}$")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title("Residuals are the vertical gaps the fit could not explain")
    ax.legend(loc="upper left")
    save(fig, "regression-residuals.png")


# 3. Eigenvectors under a linear map (before/after) ---------------------------
def fig_eigen_transform():
    A = np.array([[2.0, 1.0], [1.0, 2.0]])       # eigvecs (1,1)->3, (1,-1)->1
    w, V = np.linalg.eig(A)
    theta = np.linspace(0, 2 * np.pi, 200)
    circ = np.array([np.cos(theta), np.sin(theta)])
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.0))
    for ax, M, title in ((axes[0], np.eye(2), "before: unit vectors"),
                         (axes[1], A, "after A = [[2, 1], [1, 2]]")):
        pts = M @ circ
        ax.plot(pts[0], pts[1], color=GRID, lw=1.5)
        for i, col in ((0, MAGENTA), (1, ORANGE)):
            v = V[:, i] / np.linalg.norm(V[:, i])
            vt = M @ v
            ax.annotate("", xy=vt, xytext=(0, 0),
                        arrowprops=dict(arrowstyle="-|>", color=col, lw=2.4))
        # a generic (non-eigen) vector rotates off its line
        g = np.array([1.0, 0.15]); gt = M @ g
        ax.annotate("", xy=gt, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.0))
        ax.set_title(title, fontsize=11)
        ax.set_xlim(-3.3, 3.3); ax.set_ylim(-3.3, 3.3)
        ax.set_aspect("equal"); clean(ax)
        ax.axhline(0, color=MUTED, lw=0.6); ax.axvline(0, color=MUTED, lw=0.6)
    axes[1].text(1.7, 1.9, r"$\lambda=3$", color=MAGENTA, fontsize=11)
    axes[1].text(0.7, -1.9, r"$\lambda=1$", color=ORANGE, fontsize=11)
    axes[0].text(-3.1, 2.6, "eigen dirs stay on\ntheir line (magenta, orange);\nblue vector rotates",
                 color=SECOND, fontsize=8.5, va="top")
    fig.suptitle("Eigenvectors keep their direction; the map only rescales them",
                 fontsize=12)
    save(fig, "eigenvectors-transform.png")


# 4. PCA = eigenvectors of the covariance (modern-ML) -------------------------
def fig_pca():
    rng = np.random.default_rng(3)
    cov = np.array([[3.0, 1.6], [1.6, 1.2]])
    L = np.linalg.cholesky(cov)
    X = (L @ rng.normal(size=(2, 260))).T + np.array([4, 3])
    Xc = X - X.mean(0)
    C = np.cov(Xc.T)
    vals, vecs = np.linalg.eigh(C)
    order = np.argsort(vals)[::-1]
    vals, vecs = vals[order], vecs[:, order]
    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    clean(ax)
    ax.scatter(X[:, 0], X[:, 1], s=18, color=BLUE, alpha=0.55)
    m = X.mean(0)
    for k, col, lab in ((0, RED, "PC1"), (1, GREEN, "PC2")):
        d = vecs[:, k] * np.sqrt(vals[k]) * 2.3
        ax.annotate("", xy=m + d, xytext=m,
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.6))
        ax.text(*(m + d * 1.08), f" {lab}", color=col, fontsize=11, weight="bold")
    ax.set_aspect("equal"); ax.set_xlabel("x1"); ax.set_ylabel("x2")
    ax.set_title("PCA directions = eigenvectors of the covariance matrix")
    save(fig, "pca-eigen.png")


# 5. SVD as rotate -> stretch -> rotate ---------------------------------------
def fig_svd():
    A = np.array([[1.4, 0.9], [0.2, 1.3]])
    U, s, Vt = np.linalg.svd(A)
    theta = np.linspace(0, 2 * np.pi, 200)
    circ = np.array([np.cos(theta), np.sin(theta)])
    e = np.array([[1, 0], [0, 1]]).T * 0.0  # placeholder
    basis = np.array([[1.0, 0.0], [0.0, 1.0]]).T
    stages = [(np.eye(2), "unit circle", GRID),
              (Vt, r"after $V^{\top}$ (rotate)", GRID),
              (np.diag(s) @ Vt, r"after $\Sigma V^{\top}$ (stretch)", BLUE),
              (U @ np.diag(s) @ Vt, r"after $U\Sigma V^{\top}=A$", BLUE)]
    fig, axes = plt.subplots(1, 4, figsize=(9.2, 3.0))
    for ax, (M, title, col) in zip(axes, stages):
        pts = M @ circ
        ax.plot(pts[0], pts[1], color=col, lw=1.8)
        for i, bc in ((0, MAGENTA), (1, ORANGE)):
            vt = M @ basis[:, i]
            ax.annotate("", xy=vt, xytext=(0, 0),
                        arrowprops=dict(arrowstyle="-|>", color=bc, lw=2.0))
        ax.set_title(title, fontsize=9.5)
        ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.2, 2.2)
        ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
        for sp in ("top", "right", "bottom", "left"):
            ax.spines[sp].set_color(GRID)
    fig.suptitle("Every matrix is a rotation, then an axis-aligned stretch, then a rotation",
                 fontsize=12, y=1.02)
    save(fig, "svd-geometry.png")


# 6. Low-rank factorization (SVD -> LoRA / embedding compression) -------------
def fig_low_rank():
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.axis("off")
    def block(x, y, w, h, color, label, sub):
        ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=color, alpha=0.20,
                                    edgecolor=color, lw=1.6))
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=13, color=INK)
        ax.text(x + w / 2, y - 0.28, sub, ha="center", va="top",
                fontsize=9, color=SECOND)
    block(0.2, 0.4, 2.2, 2.2, BLUE, r"$W$", "d x d\n= d^2 params")
    ax.text(2.75, 1.5, r"$\approx$", fontsize=20, ha="center", va="center")
    block(3.2, 0.4, 0.7, 2.2, GREEN, r"$B$", "d x r")
    ax.text(4.05, 1.5, r"$\times$", fontsize=16, ha="center", va="center")
    block(4.3, 1.75, 2.2, 0.7, ORANGE, r"$A$", "r x d")
    ax.text(4.9, 0.7, "2 d r params\n(r much less than d)", fontsize=9,
            color=SECOND, ha="center", va="top")
    ax.set_xlim(0, 6.8); ax.set_ylim(-0.3, 3.1)
    ax.set_title("Low-rank factorization: the idea behind LoRA and embedding compression",
                 fontsize=11.5)
    save(fig, "low-rank-approximation.png")


# 7. Gradient descent path on a contour (real run) ----------------------------
def fig_gd_path():
    # anisotropic bowl f = 0.5*(a x^2 + b y^2); real GD steps recorded
    a, b = 1.0, 6.0
    def grad(p): return np.array([a * p[0], b * p[1]])
    x = np.array([4.5, 3.2]); step = 0.28
    path = [x.copy()]
    for _ in range(22):
        x = x - step * grad(x); path.append(x.copy())
    path = np.array(path)
    gx = np.linspace(-5, 5, 200); gy = np.linspace(-4, 4, 200)
    GX, GY = np.meshgrid(gx, gy)
    Z = 0.5 * (a * GX**2 + b * GY**2)
    fig, ax = plt.subplots(figsize=(7, 4.6))
    cs = ax.contour(GX, GY, Z, levels=14, colors=GRID, linewidths=0.8)
    ax.plot(path[:, 0], path[:, 1], "-o", color=BLUE, lw=1.8, ms=5,
            label="GD iterates")
    ax.scatter([0], [0], color=GREEN, s=90, marker="*", zorder=5, label="minimum")
    ax.scatter(path[0, 0], path[0, 1], color=RED, s=50, zorder=5, label="start")
    ax.set_aspect("equal"); clean(ax, grid=False)
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title("Gradient descent zig-zags down the valley (step = 0.28)")
    ax.legend(loc="upper right")
    save(fig, "gradient-descent-path.png")


# 8. Convex vs non-convex -----------------------------------------------------
def fig_convex():
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.8))
    x = np.linspace(-2.4, 2.4, 300)
    # convex
    fc = x**2 + 0.4
    axes[0].plot(x, fc, color=BLUE, lw=2.2)
    p, q = -1.8, 1.5
    axes[0].plot([p, q], [p**2 + 0.4, q**2 + 0.4], color=ORANGE, lw=1.8, ls="--")
    axes[0].scatter([0], [0.4], color=GREEN, s=70, marker="*", zorder=5)
    axes[0].set_title("convex: chord lies above the curve", fontsize=10.5)
    axes[0].text(0, 3.0, "one global min", color=GREEN, ha="center", fontsize=9)
    # non-convex
    fn = 0.35 * x**4 - 1.3 * x**2 + 0.2 * x + 1.2
    axes[1].plot(x, fn, color=BLUE, lw=2.2)
    axes[1].plot([p, q], [0.35*p**4 - 1.3*p**2 + 0.2*p + 1.2,
                          0.35*q**4 - 1.3*q**2 + 0.2*q + 1.2],
                 color=ORANGE, lw=1.8, ls="--")
    axes[1].scatter([-1.40, 1.30], [0.35*1.40**4 - 1.3*1.40**2 - 0.2*1.40 + 1.2,
                                    0.35*1.30**4 - 1.3*1.30**2 + 0.2*1.30 + 1.2],
                    color=RED, s=45, zorder=5)
    axes[1].set_title("non-convex: chord dips below", fontsize=10.5)
    axes[1].text(0, 2.6, "many local minima", color=RED, ha="center", fontsize=9)
    for ax in axes:
        clean(ax); ax.set_xlabel("x"); ax.set_ylabel("f(x)")
    fig.suptitle("Convexity is what makes 'a local min is the global min' true", fontsize=12)
    save(fig, "convex-vs-nonconvex.png")


# 9. L1 vs L2 geometry for sparse recovery ------------------------------------
def fig_l1_l2():
    fig, axes = plt.subplots(1, 2, figsize=(7.8, 4.0))
    # constraint line a1 x + a2 y = c  (all solutions to Ax=b)
    xs = np.linspace(-3, 3, 200)
    a1, a2, c = 1.0, 2.0, 2.0
    yline = (c - a1 * xs) / a2
    for ax in axes:
        ax.plot(xs, yline, color=INK, lw=1.8)
        ax.axhline(0, color=MUTED, lw=0.6); ax.axvline(0, color=MUTED, lw=0.6)
        ax.set_xlim(-2.6, 2.6); ax.set_ylim(-2.4, 2.4); ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
        for s in ("top", "right", "bottom", "left"):
            ax.spines[s].set_color(GRID)
    # L2: smallest circle touching the line -> non-sparse point
    t = c / (a1**2 + a2**2); pL2 = np.array([a1, a2]) * t
    r2 = np.linalg.norm(pL2)
    axes[0].add_patch(Circle((0, 0), r2, fill=False, edgecolor=BLUE, lw=2))
    axes[0].scatter(*pL2, color=BLUE, s=55, zorder=5)
    axes[0].set_title(r"$\ell_2$ ball touches off-axis (dense)", fontsize=10.5)
    # L1: smallest diamond touching the line -> touches on an axis (sparse)
    rL1 = c / max(a1, a2)  # touches at the vertex on the larger-coeff axis
    pL1 = np.array([0.0, c / a2])
    dia = Polygon([[rL1, 0], [0, rL1], [-rL1, 0], [0, -rL1]],
                  closed=True, fill=False, edgecolor=MAGENTA, lw=2)
    axes[1].add_patch(dia)
    axes[1].scatter(*pL1, color=MAGENTA, s=55, zorder=5)
    axes[1].annotate("sparse!\n(x=0)", pL1, textcoords="offset points",
                     xytext=(12, -4), color=MAGENTA, fontsize=9)
    axes[1].set_title(r"$\ell_1$ ball touches at a corner (sparse)", fontsize=10.5)
    fig.suptitle(r"Why $\ell_1$ recovers sparse solutions: its ball has corners on the axes",
                 fontsize=11.5)
    save(fig, "l1-vs-l2-sparse.png")


# 10. Cosine similarity of toy 2-D embeddings ---------------------------------
def fig_cosine():
    words = {"king": (2.6, 2.3), "queen": (2.3, 2.7), "man": (2.5, 0.6),
             "woman": (2.1, 1.0), "cat": (-1.8, 2.2), "dog": (-2.2, 1.9)}
    colors = {"king": BLUE, "queen": BLUE, "man": GREEN, "woman": GREEN,
              "cat": ORANGE, "dog": ORANGE}
    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    clean(ax, grid=True)
    for w, (x, y) in words.items():
        ax.annotate("", xy=(x, y), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=colors[w], lw=2.0))
        ax.text(x * 1.06, y * 1.06, w, color=colors[w], fontsize=11, weight="bold")
    def cos(a, b):
        a, b = np.array(a), np.array(b)
        return a @ b / (np.linalg.norm(a) * np.linalg.norm(b))
    ax.text(-3.4, -1.3,
            f"cos(king, queen) = {cos(words['king'], words['queen']):.2f}\n"
            f"cos(king, dog)   = {cos(words['king'], words['dog']):.2f}",
            fontsize=9.5, color=SECOND, family="monospace")
    ax.axhline(0, color=MUTED, lw=0.6); ax.axvline(0, color=MUTED, lw=0.6)
    ax.set_xlim(-3.6, 3.6); ax.set_ylim(-1.8, 3.4); ax.set_aspect("equal")
    ax.set_title("Cosine similarity = the dot product, angle between embeddings")
    save(fig, "cosine-similarity-embeddings.png")


# 11. Attention scores QK^T (matrix multiplication -> attention) --------------
def fig_attention():
    rng = np.random.default_rng(11)
    toks = ["The", "cat", "sat", "on", "the", "mat"]
    n = len(toks)
    Q = rng.normal(size=(n, 4)); K = rng.normal(size=(n, 4))
    scores = Q @ K.T / np.sqrt(4)
    mask = np.triu(np.ones((n, n)), 1).astype(bool)  # causal
    scores[mask] = -np.inf
    w = np.exp(scores - np.nanmax(scores, 1, keepdims=True))
    w[mask] = 0
    w = w / w.sum(1, keepdims=True)
    fig, ax = plt.subplots(figsize=(5.8, 4.8))
    im = ax.imshow(w, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(n)); ax.set_yticks(range(n))
    ax.set_xticklabels(toks); ax.set_yticklabels(toks)
    ax.set_xlabel("key (attends to)"); ax.set_ylabel("query (from)")
    for i in range(n):
        for j in range(n):
            if not mask[i, j]:
                ax.text(j, i, f"{w[i, j]:.2f}", ha="center", va="center",
                        fontsize=8, color=INK if w[i, j] < 0.6 else SURFACE)
    ax.set_title(r"Attention weights = softmax$(QK^{\top}/\sqrt{d})$")
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.outline.set_edgecolor(GRID)
    save(fig, "attention-scores.png")


# 12. Perron-Frobenius: Markov chain -> steady state --------------------------
def fig_perron():
    P = np.array([[0.85, 0.10, 0.10],
                  [0.10, 0.80, 0.20],
                  [0.05, 0.10, 0.70]])
    x = np.array([1.0, 0.0, 0.0])
    hist = [x.copy()]
    for _ in range(18):
        x = P @ x; hist.append(x.copy())
    hist = np.array(hist)
    w, V = np.linalg.eig(P)
    ss = np.real(V[:, np.argmin(np.abs(w - 1))]); ss = ss / ss.sum()
    fig, ax = plt.subplots(figsize=(7, 4.4))
    clean(ax)
    labels = ["state A", "state B", "state C"]
    cols = [BLUE, GREEN, ORANGE]
    for k in range(3):
        ax.plot(hist[:, k], "-o", color=cols[k], ms=4, lw=1.8, label=labels[k])
        ax.axhline(ss[k], color=cols[k], ls=":", lw=1.2, alpha=0.7)
    ax.set_xlabel("iteration k"); ax.set_ylabel("probability")
    ax.set_title(r"$\mathbf{x}_{k+1}=P\mathbf{x}_k$ converges to the Perron (steady-state) vector")
    ax.legend(loc="center right")
    save(fig, "perron-steady-state.png")


# 13. Word-analogy parallelogram (king - man + woman ~= queen) ----------------
# ILLUSTRATIVE 2-D layout — hand-placed points, NOT a trained embedding.
def fig_word_analogy():
    # Two orthogonal-ish "concept axes" laid out by hand so the arithmetic is exact.
    gender = np.array([2.1, 0.3])      # man -> woman direction
    royalty = np.array([0.3, 2.4])     # commoner -> royal direction
    man = np.array([0.5, 0.6])
    woman = man + gender
    king = man + royalty
    queen = woman + royalty            # = king - man + woman, by construction
    boy = man + np.array([0.0, 1.0])
    girl = boy + gender
    computed = king - man + woman      # the analogy result

    fig, ax = plt.subplots(figsize=(6.8, 5.0))
    clean(ax, grid=True)

    # parallelogram edges: gender edges (blue), royalty edges (green)
    def edge(p, q, color):
        ax.annotate("", xy=q, xytext=p,
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=2.2))
    edge(man, woman, BLUE)             # gender
    edge(king, queen, BLUE)
    edge(man, king, GREEN)             # royalty
    edge(woman, queen, GREEN)
    edge(boy, girl, BLUE)              # a second parallel gender pair

    pts = {"man": man, "woman": woman, "king": king, "queen": queen,
           "boy": boy, "girl": girl}
    off = {"man": (-6, -14), "woman": (6, -14), "king": (-8, 8),
           "queen": (8, 8), "boy": (-6, -14), "girl": (6, -14)}
    for w, p in pts.items():
        ax.scatter(*p, s=44, color=INK, zorder=5)
        ax.annotate(w, p, textcoords="offset points", xytext=off[w],
                    fontsize=11, weight="bold", color=INK)

    # the computed point lands exactly on "queen"
    ax.scatter(*computed, s=220, facecolor="none", edgecolor=RED, lw=2.2,
               zorder=6)
    ax.annotate("king - man + woman", computed, textcoords="offset points",
                xytext=(12, -26), fontsize=10, color=RED, family="monospace")

    # axis captions (the learned "concept directions")
    ax.text(0.30, 0.05, "gender direction ->", transform=ax.transAxes,
            fontsize=9, color=BLUE)
    ax.text(0.02, 0.35, "royalty\ndirection", transform=ax.transAxes,
            fontsize=9, color=GREEN, rotation=90, va="center")

    ax.set_xlim(-0.4, 5.2); ax.set_ylim(-0.4, 5.4); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("Analogy as vector addition: the same offset moves king->queen\n"
                 "and man->woman (illustrative 2-D layout, not a trained model)",
                 fontsize=11)
    save(fig, "word-analogy-parallelogram.png")


# 14. Low-rank parameter count: full W vs rank-r LoRA factors ------------------
def fig_lora_params():
    d, r = 4096, 16
    full = d * d                       # 16,777,216
    lora = 2 * d * r                   #    131,072
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.4, 3.9),
                                    gridspec_kw={"width_ratios": [1.15, 1]})

    # -- left: block schematic, concrete dimensions --
    axL.axis("off")
    def block(x, y, w, h, color, label, sub):
        axL.add_patch(plt.Rectangle((x, y), w, h, facecolor=color, alpha=0.20,
                                    edgecolor=color, lw=1.6))
        axL.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                 fontsize=13, color=INK)
        axL.text(x + w / 2, y - 0.22, sub, ha="center", va="top",
                 fontsize=8.5, color=SECOND)
    block(0.1, 0.3, 2.0, 2.0, BLUE, r"$W$", "4096 x 4096")
    axL.text(2.45, 1.3, r"$\approx$", fontsize=20, ha="center", va="center")
    block(2.8, 0.3, 0.32, 2.0, GREEN, r"$B$", "4096 x 16")
    axL.text(3.35, 1.3, r"$\times$", fontsize=15, ha="center", va="center")
    block(3.6, 1.98, 2.0, 0.32, ORANGE, r"$A$", "16 x 4096")
    axL.set_xlim(0, 5.9); axL.set_ylim(-0.4, 2.7)
    axL.set_title("Freeze $W$, learn the skinny factors $B,A$", fontsize=10.5)

    # -- right: parameter-count magnitude (bar chart) --
    clean(axR, grid=False)
    labels = ["full  W\n(4096 x 4096)", "LoRA  BA\n(rank 16)"]
    vals = [full, lora]
    cols = [BLUE, GREEN]
    ypos = [1, 0]
    axR.barh(ypos, vals, color=cols, height=0.55, zorder=3)
    axR.set_yticks(ypos); axR.set_yticklabels(labels, fontsize=9)
    axR.set_xlim(0, full * 1.18)
    axR.set_xticks([])
    for yp, v in zip(ypos, vals):
        axR.text(v + full * 0.015, yp, f"{v:,}", va="center", fontsize=10,
                 color=INK, weight="bold")
    axR.text(full * 0.5, -0.62,
             f"{full:,} vs {lora:,}  ->  {full/lora:.0f}x fewer parameters",
             ha="center", fontsize=9.5, color=SECOND)
    axR.set_title("Trainable parameters per layer", fontsize=10.5)
    for s in ("left",):
        axR.spines[s].set_visible(False)
    axR.tick_params(length=0)
    fig.suptitle("Low-rank structure: a rank-16 update replaces a 4096x4096 weight matrix",
                 fontsize=12, y=1.02)
    save(fig, "lora-parameter-count.png")


if __name__ == "__main__":
    print("Generating linear-algebra figures...")
    fig_ls_projection()
    fig_residuals()
    fig_eigen_transform()
    fig_pca()
    fig_svd()
    fig_low_rank()
    fig_gd_path()
    fig_convex()
    fig_l1_l2()
    fig_cosine()
    fig_attention()
    fig_perron()
    fig_word_analogy()
    fig_lora_params()
    print("Done.")
