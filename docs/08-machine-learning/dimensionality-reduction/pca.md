# Principal Component Analysis

## Overview

**Principal Component Analysis (PCA)** finds the orthogonal directions of maximum variance
in the data and re-expresses points in that new basis. Keeping only the top few components
gives a lower-dimensional representation that preserves most of the variance — useful for
visualization, denoising, decorrelating features, and speeding up downstream models. It's a
linear method: the components are eigenvectors of the covariance matrix (equivalently, the
right singular vectors from an SVD).

The two panels below show both halves of that idea. On the left, a synthetic
correlated 2-D Gaussian with its two principal axes drawn as arrows from the mean;
each arrow's length is proportional to the square root of the variance it captures,
so the long red PC1 points along the direction of maximum spread and the short
green PC2 sits orthogonal to it. On the right, the `explained_variance_ratio_` —
the payoff number described below — as a scree/bar plot for PCA on the 4-feature
iris dataset, where a single component already accounts for ~92% of the variance:

![Two-panel PCA figure: on the left a correlated 2-D Gaussian point cloud with two arrows from the mean marking the principal axes, a long red PC1 arrow labeled 93 percent variance along the direction of maximum spread and a short orthogonal green PC2 arrow labeled 7 percent; on the right a bar-and-line scree plot of the explained-variance ratio for PCA on the four-feature iris dataset, with the first component at 92 percent and a cumulative line reaching 100 percent by the fourth component](../img/pca-axes-and-scree.png)

*Left panel is an illustrative synthetic demo built for this page; the right panel
is PCA on scikit-learn's iris dataset (4 features).*

I covered PCA in ECEN 758 (Lecture 4, Dimensionality Reduction), implemented it two ways in
HW 1, and used it as a feature-reduction step in our CIFAR-100 group project.

## How I did it

HW 1 does PCA **both** from first principles and via scikit-learn on three 3-D toy datasets
(a swiss roll, spheres, ellipsoids), which is the clearest way to see what the library is
doing under the hood:

```python
# By hand: covariance -> eigendecomposition
cov_matrix = np.cov(data.T)
eigenvals, eigenvecs = np.linalg.eig(cov_matrix)

# With sklearn: project to 2-D and 1-D, inspect variance kept
from sklearn.decomposition import PCA
pca_2d = PCA(n_components=2)
data_2d = pca_2d.fit_transform(data)
print('Explained Variance Ratio:', pca_2d.explained_variance_ratio_)
```

Source: `course-files/appendix/Homework/ecen758_hw/HW 1/ECEN758_HW1.ipynb`

The `explained_variance_ratio_` is the payoff number: it tells you how much of the total
variance each component captures, so you can decide how many to keep. The swiss roll is the
instructive failure case — PCA is linear, so it can't "unroll" a curved manifold, which
motivates nonlinear methods.

**On images.** In our ECEN 758 CIFAR-100 group project, PCA and normalization were used as
dimensionality-reduction / preprocessing steps to reduce the feature space before the
classical models, alongside the HOG features feeding the random forest. Concretely, we
reduced each image to **50 principal components** and then ran t-SNE on top of that to
visualize the classes in 2-D — a standard "PCA-then-t-SNE" pipeline that keeps t-SNE
tractable. The 2-D map showed no clean class clusters, an early signal that 100-way
classification would be hard.

Source: our ECEN 758 CIFAR-100 group project report
(`course-files/appendix/Homework/ecen758_hw/group_project/ecen758_group_report.pdf` and
`CNN_draft2.pdf`)

!!! note "Full case study"
    The full CIFAR-100 project — this PCA/t-SNE step plus the three models that followed —
    is written up on the [CIFAR-100 case-study page](../case-study-cifar100.md).

## Course notebook

The ECEN 758 Lecture 4 slides (and my own HW 1) reference a Colab notebook demoing PCA on
the iris dataset:
<https://colab.research.google.com/drive/1Zy6JAeCUBlXDH3Onc2KAltq6IM4yELHK?usp=sharing>
(URL extracted from the lecture PDF; the same link appears in my HW 1 notebook).

## Gotchas

- **Standardize first.** PCA maximizes variance, so an unscaled large-magnitude feature
  hijacks the first component. Run `StandardScaler` before `PCA` unless the features are
  already comparable.
- **It's linear.** PCA rotates and projects — it can't capture curved structure (the swiss
  roll). For nonlinear manifolds you need t-SNE/UMAP/kernel PCA.
- **Components aren't features you can name.** Each PC is a linear mix of all originals, so
  you trade interpretability for compression.
- **Let `explained_variance_ratio_` set the number of components**, not a guess — keep
  enough PCs to reach the variance threshold you care about (e.g. 90–95%).

## References

- ECEN 758 Lecture 4 — Dimensionality Reduction (local:
  `course-files/08-machine-learning/758 Lec 04 Dimensionality Reduction.pdf`).
  Instructor-copyrighted; concept summary only.
